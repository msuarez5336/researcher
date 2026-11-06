# Practical examples: using the v2 spec

As of 2026-11-06. Each example shows one way to put `report.md` (the validated v2 spec) to work.
The numbers in Example 3 come from `examples/spec_rules.py` running on a **made-up illustrative
chain**, not market data. Example 5's results table is a **hypothetical** readout that shows how
to apply the gates. None of this is a claim that any strategy works.

---

## 1. Three hypotheses written in v2 form

Each column is a complete, falsifiable hypothesis. Copy one into the agent brief in Example 2.

| Field | A. SPY oversold bounce | B. QQQ squeeze breakout | C. Post-earnings drift |
|---|---|---|---|
| Universe | SPY | QQQ | S&P 500 members on the event date, options volume > 10k/day |
| Catalyst | Mean reversion: RSI(2) < 10 while close > 200-SMA | Volatility contraction: Bollinger bandwidth at 120-day low, then close > upper band | Earnings gap > +4% that holds through the day-1 close, with an above-consensus earnings surprise |
| IV filter | IV Rank < 50 | IV Rank < 30 | none (IV is crushed after earnings anyway) |
| Structure | Call debit vertical, 0.50Δ / 0.25Δ | Single long call, 0.60–0.70Δ | Single long call, 0.60–0.70Δ |
| Expiry | 35–60 DTE, nearest 45 | 35–60 DTE, nearest 45 | 35–60 DTE, nearest 45 (next earnings is ~60 trading days away, so the Event stop rarely fires) |
| Entry timing | Next snapshot after the signal bar | Next snapshot after the signal bar | Day-2 snapshot (the drift entry, not the gap) |
| Invalidation stop | SPY closes below the signal-bar low | QQQ closes back inside the bands | Stock closes below the day-1 low |
| Profit target | 50% of max spread profit | +35% premium | +35% premium |
| Time stop | 10 trading days or DTE < 21 | same | same |
| Baseline | Same signal on SPY shares | Same signal on QQQ shares | Same signal on the shares |
| Data | ORATS near-EOD (15:46 ET) | ORATS near-EOD | ORATS near-EOD plus an earnings calendar with announcement times (BMO/AMC) |

Why B and C use a single leg and A uses a spread: A expects a small, fast bounce, so selling the
0.25Δ call costs little upside and cuts vega and theta. B and C expect larger moves, and a
spread's cap would truncate exactly the outcomes the hypothesis is betting on.

---

## 2. A brief for the agent that builds the backtest

Paste this to a coding agent, or run `/delegate` on it. It is self-contained on purpose:
the agent sees nothing else.

```text
OBJECTIVE
Build and run a backtest of hypothesis A (SPY oversold bounce, call debit vertical) exactly as
specified in research/2026-11-06-options-swing-backtest-spec/report.md, section "The v2 spec".

WHAT IS FIXED (do not change)
- Rules: report.md "The v2 spec", Phases 1–5, plus column A of examples.md table 1.
- Mechanics: reuse examples/spec_rules.py (select_debit_spread, entry_cost, exit_decision,
  lint_spec). Run lint_spec() on your parameters first; abort if it returns anything.
- Fills: per leg at k=0.70; rerun the whole test at k=1.0. Costs $0.70/contract/side.
- Data: ORATS near-EOD chains with bid/ask, IV and Greeks; execute at the snapshot time.
  Underlying signal from a separate unadjusted equity price series, not the ORATS
  parity-derived price. Open interest: latest record dated before the entry day.

SPLITS AND GRID
- Rolling walk-forward: 3y train / 1y test, step 1y; final holdout = last 2 years, untouched
  until the grid is frozen.
- Grid: DTE {35,45,55} x short delta {0.20,0.25,0.30} x profit target {25,35,50%} = 27 configs.
  Log every config to trials.csv. Report PBO (CSCV) or the deflated Sharpe ratio across all 27.

OUTPUT
- results/A/trades.csv (one row per trade: dates, legs, fills, exit reason, P&L)
- results/A/summary.md: the 6 pass gates from Phase 5, each PASS/FAIL with its number, at k=1.0
  out of sample; the shares-only baseline; the sensitivity heatmap; PBO/DSR.
- Reply with the path and a 200-word summary. Do not tune after seeing the holdout.

STOP IF
- The data lacks bid/ask, or fewer than 30 OOS trades exist: report that and stop.
```

---

## 3. Contract selection, fills and exits, worked through

Run it yourself:

```bash
python3 research/2026-11-06-options-swing-backtest-spec/examples/spec_rules.py
```

Output on the illustrative chain (made-up numbers):

```text
lint(v2 defaults): consistent
lint(v1 values)  : ['entry DTE floor 30 minus DTE stop 21 leaves 9 calendar days, but max hold 15 trading days is ~21: the DTE stop cuts the swing short. Raise entry DTE to >= 42.']

single leg  : 45 DTE 590C delta 0.63
debit spread: +600C (d 0.51) / -620C (d 0.26), 45 DTE
  entry cost, 2 spreads, k=0.5: $1,717.80
  entry cost, 2 spreads, k=0.7: $1,731.80
  entry cost, 2 spreads, k=1.0: $1,752.80

day 6, spread value up $6.00/share: exits fired ['profit'] -> profit
day 10, underlying 589 < 592 stop, spread down $2: fired ['stop', 'time'] -> stop
```

How to read it:
- **Expiry choice:** the 28-DTE row is skipped because it's below the 35-DTE floor. 45 wins over 52 because it is nearer the 45 target.
- **Strike choice:** the 625C (0.21Δ) would have been nearer 0.25Δ on some days, but its OI of 300 fails the ≥ 500 filter, so 620C is used.
- **Fill sensitivity:** going from mid (k = 0.5) to the full spread (k = 1.0) adds $35 to a $1,718 entry, about 2%, on a chain with tight spreads. On a single name with an 8% spread the same step costs about 4% of premium **per leg, each way**. That is why the stress test at k = 1.0 decides the verdict.
- **Exit priority:** on day 10 the stop and the time exit both fire, and Stop is recorded because it ranks higher. That matters for attribution: you learn the thesis was wrong, not just that time ran out.

---

## 4. Checking a variant before spending data budget

Someone proposes "enter at 30 DTE, hold up to 15 days" to cut premium cost. Run the linter before you buy data:

```bash
python3 -c "import sys; sys.path.insert(0,'research/2026-11-06-options-swing-backtest-spec/examples'); import spec_rules as s; print(s.lint_spec({**s.SPEC,'entry_dte':(30,60),'max_hold_days':15}))"
```

It reports the contradiction: the DTE-21 stop would end every trade after about 9 calendar days, so the 15-day hold never happens. Fix it by raising the entry floor or shortening the hold.

---

## 5. Reading a results summary against the gates (hypothetical numbers)

| Gate (OOS, k = 1.0) | Threshold | Hypothetical result | Verdict |
|---|---|---|---|
| Expectancy after costs | > 0 | +$18 / trade | PASS |
| Profit factor | ≥ 1.3 | 1.21 | **FAIL** |
| Trades | ≥ 100 | 142 | PASS |
| Regimes positive | ≥ 2 of 3 | 2018 +, 2020 −, 2022 + | PASS |
| vs shares baseline | higher risk-adjusted return | Sharpe 0.71 vs 0.64 | PASS |
| PBO | < 0.5 (lower is better) | 0.38 | PASS |

**Decision: reject as specified.** One failed gate fails the hypothesis. Don't loosen the
threshold after seeing the result. Look at the sensitivity grid: if profit factor clears 1.3 only
in one cell, that's a peak, not a plateau, and the result is overfit. Any re-test with changed
rules counts as a new trial and goes into the PBO/DSR count.

---

## 6. Choosing a data vendor

| Your situation | Use | Why (from report.md) |
|---|---|---|
| EOD swing entries, want Greeks ready | ORATS near-EOD | 2007+, IV and Greeks included, snapshot 14 min before close |
| Need an exchange-sourced audit trail | Cboe DataShop | NBBO at 15:45 and close, 2012+. Buy the Greeks add-on or compute them. |
| Need intraday execution ("15 min after open") | ORATS 1-min (2020+) or Databento OPRA | Databento lists no IV/Greeks fields, so plan to compute them with one American model |
| Already pay for Massive | Fine for signals and reference data | IV and Greeks are snapshot-only, so for history compute them yourself |

---

## 7. Re-running this research later

Fee schedules and vendor docs change. To refresh only the volatile facts:

```text
/research Re-verify as of <date>: IBKR/Fidelity/tastytrade/Robinhood options fees, FINRA TAF and
SEC Section 31 rates, ORATS and Cboe DataShop snapshot times and history, Massive historical
Greeks availability. Compare with research/2026-11-06-options-swing-backtest-spec/report.md.
```
