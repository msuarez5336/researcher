"""Reference implementation of the v2 spec's mechanical rules (stdlib only).

Covers what a backtest builder most often gets wrong: contract selection by delta/DTE with
liquidity filters, per-leg fills at a fraction k of the spread, per-contract costs, the exit
hierarchy with a fixed priority, and a linter that catches contradictory spec parameters.

Not a backtester. It has no data loader and no P&L loop. The chain in demo() is made-up
illustrative data, not market data.

Run from the repo root:
    python3 research/2026-11-06-options-swing-backtest-spec/examples/spec_rules.py           # demo
    python3 research/2026-11-06-options-swing-backtest-spec/examples/spec_rules.py --selftest
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field

# ---------------------------------------------------------------- spec parameters (v2 defaults)
SPEC = {
    "entry_dte": (35, 60),        # F1: 30 DTE floor contradicted the 21-DTE exit
    "target_dte": 45,
    "dte_floor": 21,              # time stop: exit when DTE < 21
    "max_hold_days": 10,          # F2: one number, trading days
    "single_leg_delta": (0.60, 0.70),
    "spread_long_delta": 0.50,
    "spread_short_delta": 0.25,
    "max_spread_pct_of_mid": 0.08,
    "min_open_interest": 500,     # use prior-day OI (point in time)
    "fill_k": 0.70,               # F3: buys at bid + k*(ask-bid); stress at 1.0
    "commission_per_contract": 0.65,
    "fees_per_contract": 0.05,    # placeholder; set from report.md section on costs
    "profit_target_spread": 0.50,  # of max profit (F7)
    "profit_target_single": 0.35,  # of premium paid (F7)
    "max_option_loss": 0.50,       # A6 backstop, of premium paid
}

CAL_DAYS_PER_TRADING_DAY = 7 / 5


@dataclass
class Quote:
    symbol: str
    right: str          # "C" or "P"
    strike: float
    dte: int            # calendar days to expiry
    delta: float        # signed: calls > 0, puts < 0
    bid: float
    ask: float
    open_interest: int  # prior-day OI
    standard: bool = True  # False for corporate-action-adjusted contracts (A5)

    @property
    def mid(self) -> float:
        return (self.bid + self.ask) / 2

    @property
    def spread_pct(self) -> float:
        return (self.ask - self.bid) / self.mid if self.mid > 0 else float("inf")


# ---------------------------------------------------------------- contract selection (Phase 3)
def liquid(q: Quote, spec=SPEC) -> bool:
    return (q.standard and q.bid > 0 and q.spread_pct <= spec["max_spread_pct_of_mid"]
            and q.open_interest >= spec["min_open_interest"])


def pick_expiry(chain: list[Quote], spec=SPEC) -> int | None:
    lo, hi = spec["entry_dte"]
    dtes = sorted({q.dte for q in chain if lo <= q.dte <= hi})
    return min(dtes, key=lambda d: abs(d - spec["target_dte"])) if dtes else None


def pick_by_delta(chain, right, target, dte, spec=SPEC) -> Quote | None:
    sign = 1 if right == "C" else -1
    cands = [q for q in chain if q.right == right and q.dte == dte and liquid(q, spec)]
    return min(cands, key=lambda q: abs(sign * q.delta - target), default=None)


def select_single(chain, right="C", spec=SPEC) -> Quote | None:
    dte = pick_expiry(chain, spec)
    lo, hi = spec["single_leg_delta"]
    q = pick_by_delta(chain, right, (lo + hi) / 2, dte, spec) if dte else None
    sign = 1 if right == "C" else -1
    return q if q and lo <= sign * q.delta <= hi else None  # reject if nothing in band


def select_debit_spread(chain, right="C", spec=SPEC) -> tuple[Quote, Quote] | None:
    dte = pick_expiry(chain, spec)
    if dte is None:
        return None
    long = pick_by_delta(chain, right, spec["spread_long_delta"], dte, spec)
    short = pick_by_delta(chain, right, spec["spread_short_delta"], dte, spec)
    if not long or not short or long.strike == short.strike:
        return None
    return long, short


# ---------------------------------------------------------------- fills and costs (Phase 5)
def fill_price(q: Quote, side: str, k: float) -> float:
    """side 'buy' pays bid + k*spread; 'sell' receives ask - k*spread. k=0.5 is mid."""
    width = q.ask - q.bid
    return q.bid + k * width if side == "buy" else q.ask - k * width


def entry_cost(legs: list[tuple[Quote, str]], contracts: int, spec=SPEC, k=None) -> float:
    """Net debit in dollars for opening `legs` [(quote, 'buy'|'sell'), ...], per-leg fills."""
    k = spec["fill_k"] if k is None else k
    net = sum((fill_price(q, s, k) if s == "buy" else -fill_price(q, s, k)) for q, s in legs)
    per_contract_costs = (spec["commission_per_contract"] + spec["fees_per_contract"]) * len(legs)
    return round(net * 100 * contracts + per_contract_costs * contracts, 2)


# ---------------------------------------------------------------- exit hierarchy (Phase 4)
EXIT_PRIORITY = ["event", "stop", "time", "profit"]  # A6: fixed order when several fire


@dataclass
class PositionState:
    structure: str            # "single" or "spread"
    entry_debit: float        # per share, after fills
    max_value: float          # per share; spread width for a debit spread
    value_now: float          # per share, at the exit-check price (bid side for longs)
    underlying_now: float
    invalidation_level: float  # underlying stop (long call: exit if below)
    direction: int            # +1 bullish, -1 bearish
    days_held: int            # trading days
    dte_now: int
    trading_days_to_earnings: int | None = None
    flags: dict = field(default_factory=dict)


def exit_signals(p: PositionState, spec=SPEC) -> list[str]:
    fired = []
    if p.trading_days_to_earnings is not None and p.trading_days_to_earnings <= 1:
        fired.append("event")
    if p.direction * (p.underlying_now - p.invalidation_level) < 0:
        fired.append("stop")
    if p.value_now <= p.entry_debit * (1 - spec["max_option_loss"]):
        fired.append("stop")  # option-value backstop
    if p.days_held >= spec["max_hold_days"] or p.dte_now < spec["dte_floor"]:
        fired.append("time")
    if p.structure == "spread":
        max_profit = p.max_value - p.entry_debit
        if p.value_now - p.entry_debit >= spec["profit_target_spread"] * max_profit:
            fired.append("profit")
    elif p.value_now >= p.entry_debit * (1 + spec["profit_target_single"]):
        fired.append("profit")
    return sorted(set(fired), key=EXIT_PRIORITY.index)


def exit_decision(p: PositionState, spec=SPEC) -> str | None:
    s = exit_signals(p, spec)
    return s[0] if s else None


# ---------------------------------------------------------------- spec linter
def lint_spec(spec=SPEC) -> list[str]:
    """Return contradictions in a parameter set. Empty list means consistent."""
    problems = []
    lo, hi = spec["entry_dte"]
    hold_cal = spec["max_hold_days"] * CAL_DAYS_PER_TRADING_DAY
    if lo - spec["dte_floor"] < hold_cal - 0.5:
        problems.append(
            f"entry DTE floor {lo} minus DTE stop {spec['dte_floor']} leaves {lo - spec['dte_floor']} "
            f"calendar days, but max hold {spec['max_hold_days']} trading days is ~{hold_cal:.0f}: "
            f"the DTE stop cuts the swing short. Raise entry DTE to >= {spec['dte_floor'] + round(hold_cal)}.")
    if not lo <= spec["target_dte"] <= hi:
        problems.append("target DTE outside the entry window")
    if not 0.5 <= spec["fill_k"] <= 1.0:
        problems.append("fill_k below 0.5 assumes fills better than mid; above 1.0 is beyond the quote")
    if spec["spread_short_delta"] >= spec["spread_long_delta"]:
        problems.append("debit spread short leg delta must be below the long leg delta")
    if spec["dte_floor"] <= 0:
        problems.append("no DTE floor: positions can reach expiry, so pin and assignment rules are needed")
    return problems


# ---------------------------------------------------------------- demo
def demo_chain() -> list[Quote]:
    """Illustrative SPY-like call chain. Made-up numbers for the walkthrough, not market data."""
    rows = [  # dte, strike, delta, bid, ask, oi
        (28, 600, 0.52, 9.80, 9.95, 9000),
        (45, 585, 0.68, 22.10, 22.45, 3100),
        (45, 590, 0.63, 19.05, 19.35, 4200),
        (45, 600, 0.51, 13.60, 13.80, 12000),
        (45, 615, 0.32, 6.70, 6.85, 7600),
        (45, 620, 0.26, 5.05, 5.20, 8800),
        (45, 625, 0.21, 3.75, 3.90, 300),    # fails OI filter
        (52, 600, 0.52, 15.10, 15.95, 2500),  # wide spread (5.5%) still passes 8%
    ]
    return [Quote("SPY", "C", s, d, de, b, a, oi) for d, s, de, b, a, oi in rows]


def demo() -> None:
    chain = demo_chain()
    print("lint(v2 defaults):", lint_spec() or "consistent")
    print("lint(v1 values)  :", lint_spec({**SPEC, "entry_dte": (30, 60), "max_hold_days": 15}))
    single = select_single(chain)
    print(f"\nsingle leg  : {single.dte} DTE {single.strike:.0f}C delta {single.delta}")
    long, short = select_debit_spread(chain)
    print(f"debit spread: +{long.strike:.0f}C (d {long.delta}) / -{short.strike:.0f}C (d {short.delta}), {long.dte} DTE")
    for k in (0.5, 0.7, 1.0):
        print(f"  entry cost, 2 spreads, k={k}: ${entry_cost([(long, 'buy'), (short, 'sell')], 2, k=k):,.2f}")
    debit = fill_price(long, "buy", 0.7) - fill_price(short, "sell", 0.7)
    p = PositionState("spread", debit, short.strike - long.strike, debit + 6.0, 608, 592, +1,
                      days_held=6, dte_now=36, trading_days_to_earnings=None)
    print(f"\nday 6, spread value up $6.00/share: exits fired {exit_signals(p)} -> {exit_decision(p)}")
    p.underlying_now, p.days_held, p.value_now = 589, 10, debit - 2.0
    print(f"day 10, underlying 589 < 592 stop, spread down $2: fired {exit_signals(p)} -> {exit_decision(p)}")


def selftest() -> None:
    chain = demo_chain()
    assert lint_spec() == []
    assert lint_spec({**SPEC, "entry_dte": (30, 60)})  # v1 contradiction is caught
    s = select_single(chain)
    assert s.dte == 45 and 0.60 <= s.delta <= 0.70
    long, short = select_debit_spread(chain)
    assert (long.strike, short.strike) == (600, 620)  # 625 rejected on OI
    q = chain[3]
    assert abs(fill_price(q, "buy", 0.5) - q.mid) < 1e-9
    assert fill_price(q, "buy", 1.0) == q.ask and fill_price(q, "sell", 1.0) == q.bid
    assert entry_cost([(long, "buy"), (short, "sell")], 1, k=1.0) > entry_cost(
        [(long, "buy"), (short, "sell")], 1, k=0.5)
    p = PositionState("single", 10.0, 0, 9.0, 99, 100, +1, days_held=3, dte_now=40,
                      trading_days_to_earnings=1)
    assert exit_signals(p) == ["event", "stop"] and exit_decision(p) == "event"
    p = PositionState("single", 10.0, 0, 13.6, 105, 100, +1, days_held=2, dte_now=40)
    assert exit_decision(p) == "profit"
    p = PositionState("single", 10.0, 0, 10.5, 105, 100, +1, days_held=2, dte_now=20)
    assert exit_decision(p) == "time"
    print("selftest: all checks passed")


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else demo()
