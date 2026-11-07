"""Intraday long-option study. Implements study_spec.md (frozen 2026-11-07). Stdlib only.

Usage (from repo root):
    python3 research/2026-11-07-intraday-long-options/study/intraday.py --selftest
    python3 research/2026-11-07-intraday-long-options/study/intraday.py

Reads study/data/ (written by fetch_data.py). Writes results.csv, vrp.csv, trades_sample.csv and
run.log next to this file. Option prices are modelled (Black-Scholes at VIX1D), not observed.
"""
from __future__ import annotations

import csv
import json
import math
import re
import statistics as st
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
NY = ZoneInfo("America/New_York")
START = date(2024, 1, 22)
OOS = date(2025, 6, 1)
MARK_MIN = [0, 60, 120, 180, 240, 300, 360, 390]          # minutes after 09:30 for marks 0..7
MARK_LBL = ["09:30", "10:30", "11:30", "12:30", "13:30", "14:30", "15:30", "16:00"]
BDAY = 405.0                                              # Cboe VIX1D business-day minutes
COMM = 0.007                                              # $0.70 per contract per side
COSTS = ("gross", "k70", "k100", "dps")
FIRST_TRIAL = 1538
TRIAL = FIRST_TRIAL
LOG: list[str] = []


def say(m: str) -> None:
    print(m, flush=True)
    LOG.append(m)


# ------------------------------------------------------------------ data
def hourly(sym: str) -> dict[date, list[float]]:
    j = json.loads((DATA / f"yh_1h_{sym}.json").read_text())["chart"]["result"][0]
    q = j["indicators"]["quote"][0]
    days: dict[date, dict[str, tuple]] = defaultdict(dict)
    for i, ts in enumerate(j["timestamp"]):
        dt = datetime.fromtimestamp(ts, NY)
        if q["open"][i] is None or q["close"][i] is None:
            continue
        days[dt.date()][dt.strftime("%H:%M")] = (q["open"][i], q["close"][i])
    out = {}
    for d, bars in days.items():
        hrs = MARK_LBL[:7]
        if not all(h in bars for h in hrs):
            continue                                       # half-days and gaps excluded
        out[d] = [bars["09:30"][0]] + [bars[h][1] for h in hrs]
    return out


def cboe(name: str) -> dict[date, float]:
    out = {}
    rows = list(csv.reader((DATA / f"cboe_{name}.csv").read_text().splitlines()))
    hdr = [h.strip().upper() for h in rows[0]]
    c = hdr.index("CLOSE")
    for r in rows[1:]:
        try:
            out[datetime.strptime(r[0], "%m/%d/%Y").date()] = float(r[c])
        except (ValueError, IndexError):
            pass
    return out


def nasdaq(tk: str) -> dict[date, tuple[float, float, float, float, float]]:
    rows = json.loads((DATA / f"nq_{tk}.json").read_text())["data"]["tradesTable"]["rows"]
    f = lambda s: float(s.replace("$", "").replace(",", "")) if s not in ("", "N/A", None) else math.nan
    out = {}
    for r in rows:
        d = datetime.strptime(r["date"], "%m/%d/%Y").date()
        out[d] = (f(r["open"]), f(r["high"]), f(r["low"]), f(r["close"]), f(r["volume"]))
    return dict(sorted(out.items()))


def macro_dates() -> dict[str, set[date]]:
    out: dict[str, set[date]] = defaultdict(set)
    for r in csv.DictReader((DATA / "macro_events.csv").read_text().splitlines()):
        out[r["event_code"]].add(date.fromisoformat(r["event_date"]))
    fed = set()
    for pg in ("fed_fomccalendars.htm", "fed_fomchistorical2020.htm"):
        for s in re.findall(r"monetary(\d{8})a\.htm", (DATA / pg).read_text(errors="replace")):
            fed.add(datetime.strptime(s, "%Y%m%d").date())
    lo = date(2022, 1, 1)
    conc = {d for d in out["fomc"] if d >= lo}
    fed = {d for d in fed if lo <= d <= date(2026, 11, 7)}
    if conc != fed:
        say(f"FOMC cross-check mismatch: only Concretum {sorted(conc - fed)}; only Fed {sorted(fed - conc)} -> Fed wins")
    else:
        say(f"FOMC cross-check: {len(fed)} dates match federalreserve.gov")
    out["fomc"] = fed
    return out


def opex_dates(sessions: set[date]) -> set[date]:
    out = set()
    for y in range(2023, 2027):
        for m in range(1, 13):
            d = date(y, m, 1)
            fri = d + timedelta(days=(4 - d.weekday()) % 7 + 14)
            if fri in sessions:
                out.add(fri)
            elif fri - timedelta(days=1) in sessions:
                out.add(fri - timedelta(days=1))
    return out


# ------------------------------------------------------------------ option maths
def ncdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def bs(S: float, K: float, T: float, v: float, cp: int) -> float:
    if T <= 0 or v <= 0:
        return max(0.0, cp * (S - K))
    sd = v * math.sqrt(T)
    d1 = (math.log(S / K) + 0.5 * sd * sd) / sd
    d2 = d1 - sd
    return S * ncdf(d1) - K * ncdf(d2) if cp > 0 else K * ncdf(-d2) - S * ncdf(-d1)


def delta(S: float, K: float, T: float, v: float, cp: int) -> float:
    sd = v * math.sqrt(T)
    d1 = (math.log(S / K) + 0.5 * sd * sd) / sd
    return ncdf(d1) if cp > 0 else ncdf(d1) - 1


def strike_for(S: float, T: float, v: float, cp: int, target: float, step: float = 1.0) -> float:
    atm = round(S / step) * step
    best, bd = atm, 9.0
    for i in range(0, 400):
        K = atm + cp * i * step
        dd = abs(abs(delta(S, K, T, v, cp)) - target)
        if dd < bd:
            best, bd = K, dd
        elif abs(delta(S, K, T, v, cp)) < target:
            break
    return best


def tau(mark: int, dte: int, bday: float = BDAY) -> float:
    return (390 - MARK_MIN[mark]) / (252 * bday) + dte / 252.0


def spread_rate(mark: int) -> float:
    return 0.045 if mark == 0 or mark >= 6 else 0.03


def leg_cost(mid: float, mark: int, mode: str) -> float:
    """Per-leg, per-side cost in $ (half-spread part plus commission)."""
    if mid < 0.005:
        return 0.0                                          # worthless leg: abandoned, no trade
    if mode == "gross":
        return 0.0
    if mode == "dps":
        return 0.045 * mid + COMM
    k = 0.70 if mode == "k70" else 1.0
    s = max(0.01, spread_rate(mark) * mid)
    return (k - 0.5) * s + COMM


# ------------------------------------------------------------------ market state
class Mkt:
    def __init__(self, tk: str, px: dict, vix1d: dict, vix: dict, vxn: dict, daily: dict):
        self.tk, self.px, self.v1, self.daily = tk, px, vix1d, daily
        self.vix, self.vxn = vix, vxn
        self.ddates = sorted(daily)
        self.didx = {d: i for i, d in enumerate(self.ddates)}

    def prev_close(self, d: date) -> float:
        i = self.didx.get(d)
        return self.daily[self.ddates[i - 1]][3] if i else math.nan

    def prev_daily(self, ser: dict, d: date) -> float:
        i = self.didx.get(d)
        return ser.get(self.ddates[i - 1], math.nan) if i else math.nan

    def sigma(self, d: date, mark: int) -> float:
        m = 5 if mark >= 6 else mark                         # frozen window after 15:00
        v = self.v1[d][m] / 100.0
        if self.tk == "QQQ":
            v *= self.prev_daily(self.vxn, d) / self.prev_daily(self.vix, d)
        return v


def legs(m: Mkt, d: date, e: int, side: int, struct: str) -> list[tuple[float, int, int, int]]:
    S, v = m.px[d][e], m.sigma(d, e)
    atm = float(round(S))
    if struct == "A0":
        return [(atm, side, 1, 0)]
    if struct == "A1":
        return [(atm, side, 1, 1)]
    if struct == "O0":
        return [(strike_for(S, tau(e, 0), v, side, 0.30), side, 1, 0)]
    if struct == "D0":
        k2 = strike_for(S, tau(e, 0), v, side, 0.25)
        if k2 == atm:
            k2 = atm + side
        return [(atm, side, 1, 0), (k2, side, -1, 0)]
    if struct == "S0":
        return [(atm, 1, 1, 0), (atm, -1, 1, 0)]
    if struct == "S1":
        return [(atm, 1, 1, 1), (atm, -1, 1, 1)]
    raise ValueError(struct)


def values(m: Mkt, d: date, lg, mark: int) -> list[float]:
    S, v = m.px[d][mark], m.sigma(d, mark)
    return [bs(S, K, tau(mark, dte), v, cp) for K, cp, _, dte in lg]


def trade(m: Mkt, d: date, e: int, side: int, struct: str, exit_rule) -> dict[str, float]:
    """exit_rule: an int mark, 'FP' or 'TS'. Returns net return on debit per cost mode."""
    lg = legs(m, d, e, side, struct)
    v0 = values(m, d, lg, e)
    mid0 = sum(s * x for (_, _, s, _), x in zip(lg, v0))
    if mid0 <= 0.005:
        return {}
    out = {}
    for mode in COSTS:
        cost = mid0 + sum(leg_cost(x, e, mode) for x in v0)

        def proceeds(j):
            vj = values(m, d, lg, j)
            return sum(s * x for (_, _, s, _), x in zip(lg, vj)) - sum(leg_cost(x, j, mode) for x in vj), \
                sum(s * x for (_, _, s, _), x in zip(lg, vj))

        if isinstance(exit_rule, int):
            p, _ = proceeds(exit_rule)
        else:
            p = None
            for j in range(e + 1, 7):
                pj, midj = proceeds(j)
                if exit_rule == "FP" and pj > cost:
                    p = pj
                    break
                if exit_rule == "TS" and (midj >= 1.5 * mid0 or midj <= 0.5 * mid0):
                    p = pj
                    break
            if p is None:
                p, _ = proceeds(6)
        out[mode] = p / cost - 1
    return out


# ------------------------------------------------------------------ stats
def welch(a: list[float], b: list[float]) -> float:
    if len(a) < 2 or len(b) < 2:
        return math.nan
    va, vb = st.variance(a) / len(a), st.variance(b) / len(b)
    return (st.mean(a) - st.mean(b)) / math.sqrt(va + vb) if va + vb > 0 else math.nan


def split(d: date) -> str:
    return "OOS" if d >= OOS else "IS"


ROWS: list[dict] = []
SAMPLE: list[dict] = []


def score(meta: dict, ev: dict[str, list[dict]], base: dict[str, list[dict]]) -> None:
    """ev/base: split -> list of return dicts (per cost mode)."""
    global TRIAL
    row = {"trial": TRIAL, **meta}
    TRIAL += 1
    for sp in ("IS", "OOS"):
        e, b = ev.get(sp, []), base.get(sp, [])
        row[f"n_{sp}"] = len(e)
        row[f"nb_{sp}"] = len(b)
        for mode in COSTS:
            ea = [x[mode] for x in e if mode in x]
            ba = [x[mode] for x in b if mode in x]
            row[f"mean_{sp}_{mode}"] = st.mean(ea) if ea else math.nan
            row[f"exc_{sp}_{mode}"] = (st.mean(ea) - st.mean(ba)) if ea and ba else math.nan
            if mode == "k70":
                row[f"t_{sp}"] = welch(ea, ba)
                row[f"base_{sp}_k70"] = st.mean(ba) if ba else math.nan
    elig = row["n_OOS"] >= 20
    ok = (elig and row["exc_OOS_k70"] >= 0.10 and row["t_OOS"] >= 3
          and row["exc_IS_k70"] > 0 and row["exc_OOS_k100"] > 0)
    row["eligible"], row["pass"] = elig, ok
    ROWS.append(row)


# ------------------------------------------------------------------ Part 1: VRP
def part1(spy: Mkt, days: list[date], types: dict[str, set[date]], vix1d_d: dict, spy_d: dict) -> list[dict]:
    global TRIAL
    out = []
    order = ["all", "fomc", "macro0830", "ism", "opex", "other"]
    for m in range(7):
        for ty in order:
            sel = [d for d in days if d in types[ty]]
            rec = {"trial": TRIAL, "part": "1a", "mark": MARK_LBL[m], "daytype": ty}
            TRIAL += 1
            for sp in ("IS", "OOS", "ALL"):
                s2 = [d for d in sel if sp == "ALL" or split(d) == sp]
                imp = [spy.sigma(d, m) ** 2 * tau(m, 0) for d in s2]
                imp390 = [spy.sigma(d, m) ** 2 * tau(m, 0, 390.0) for d in s2]
                rv = [sum(math.log(spy.px[d][j + 1] / spy.px[d][j]) ** 2 for j in range(m, 7)) for d in s2]
                rec[f"n_{sp}"] = len(s2)
                if s2:
                    rec[f"imp_{sp}"] = st.mean(imp)
                    rec[f"rv_{sp}"] = st.mean(rv)
                    rec[f"ratio_{sp}"] = st.mean(rv) / st.mean(imp)
                    rec[f"ratio390_{sp}"] = st.mean(rv) / st.mean(imp390)
                    rec[f"share_rv_gt_{sp}"] = sum(r > i for r, i in zip(rv, imp)) / len(s2)
            out.append(rec)
    # 1b daily
    dd = sorted(d for d in spy_d if d >= date(2022, 5, 16))
    ds = sorted(spy_d)
    di = {d: i for i, d in enumerate(ds)}
    for kind in ("c2c", "o2c"):
        for ty in order:
            rec = {"trial": TRIAL, "part": "1b", "mark": kind, "daytype": ty}
            TRIAL += 1
            for sp in ("IS", "OOS", "ALL"):
                imp, rv = [], []
                for d in dd:
                    if ty != "all" and d not in types[ty]:
                        continue
                    if sp != "ALL" and ("OOS" if d >= date(2024, 7, 1) else "IS") != sp:
                        continue
                    p = ds[di[d] - 1]
                    if p not in vix1d_d:
                        continue
                    o, _, _, c, _ = spy_d[d]
                    pc = spy_d[p][3]
                    imp.append((vix1d_d[p] / 100) ** 2 / 252)
                    rv.append(math.log(c / pc) ** 2 if kind == "c2c" else math.log(c / o) ** 2)
                rec[f"n_{sp}"] = len(imp)
                if imp:
                    rec[f"imp_{sp}"], rec[f"rv_{sp}"] = st.mean(imp), st.mean(rv)
                    rec[f"ratio_{sp}"] = st.mean(rv) / st.mean(imp)
                    rec[f"share_rv_gt_{sp}"] = sum(r > i for r, i in zip(rv, imp)) / len(imp)
            out.append(rec)
    return out


# ------------------------------------------------------------------ Part 2 helpers
def by_split(items):
    out = defaultdict(list)
    for d, r in items:
        if r:
            out[split(d)].append(r)
    return out


def avg_sides(r1: dict, r2: dict) -> dict:
    return {k: (r1[k] + r2[k]) / 2 for k in COSTS if k in r1 and k in r2}


def directional_cell(m, meta, trig: dict[date, int], elig_days, e, struct, ex):
    ev = by_split((d, trade(m, d, e, s, struct, ex)) for d, s in trig.items())
    base = by_split((d, avg_sides(trade(m, d, e, 1, struct, ex), trade(m, d, e, -1, struct, ex)))
                    for d in elig_days if d not in trig)
    score({**meta, "struct": struct, "entry": MARK_LBL[e], "exit": ex if isinstance(ex, str) else MARK_LBL[ex]}, ev, base)


def straddle_cell(m, meta, sel: list[date], basedays: list[date], e, x, struct):
    ev = by_split((d, trade(m, d, e, 1, struct, x)) for d in sel)
    base = by_split((d, trade(m, d, e, 1, struct, x)) for d in basedays)
    score({**meta, "struct": struct, "entry": MARK_LBL[e], "exit": MARK_LBL[x]}, ev, base)


def rolling(vals: dict[date, float], hist_days: list[date], fn, n=60) -> dict[date, float]:
    out = {}
    for i, d in enumerate(hist_days):
        if i >= n:
            w = [vals[x] for x in hist_days[i - n:i] if not math.isnan(vals[x])]
            if len(w) >= n // 2:
                out[d] = fn(w)
    return out


def pctl(xs, p):
    s = sorted(xs)
    return s[min(len(s) - 1, int(p * len(s)))]


def part2(m: Mkt, days: list[date], types: dict[str, set[date]], hist: list[date]) -> None:
    tk = m.tk
    DIR = ["A0", "O0", "A1", "D0"]
    P = m.px
    # 1c straddles, random-time baseline (other entry marks, same number of bars held)
    for (e, x, name) in [(0, 1, "open"), (1, 6, "day"), (2, 4, "midday"), (5, 6, "power"), (6, 7, "lasthalf")]:
        for struct in ("S0", "S1"):
            ev = by_split((d, trade(m, d, e, 1, struct, x)) for d in days)
            h = x - e
            others = [(a, a + h) for a in range(0, 7) if a != e and a + h <= 6]
            base = by_split((d, {k: st.mean(v) for k, v in _merge([trade(m, d, a, 1, struct, b) for a, b in others]).items()})
                            for d in days)
            score({"part": "1c", "ticker": tk, "window": name, "variant": "all", "struct": struct,
                   "entry": MARK_LBL[e], "exit": MARK_LBL[x]}, ev, base)
    # W1 first hour
    r1 = {d: math.log(P[d][1] / P[d][0]) for d in hist}
    med = rolling({d: abs(v) for d, v in r1.items()}, hist, st.median)
    elig = [d for d in days if d in med]
    for var, sgn in (("cont", 1), ("fade", -1)):
        trig = {d: sgn * (1 if r1[d] > 0 else -1) for d in elig if abs(r1[d]) >= med[d] and r1[d] != 0}
        for ex in (2, 4, 6, "FP", "TS"):
            for s in DIR:
                directional_cell(m, {"part": "W1", "ticker": tk, "window": "first-hour", "variant": var}, trig, elig, 1, s, ex)
    say(f"{tk} W1 done")
    # W2 gap
    g = {d: math.log(P[d][0] / m.prev_close(d)) for d in hist}
    sd = rolling(g, hist, st.stdev)
    elig = [d for d in days if d in sd]
    for var, sgn in (("go", 1), ("fill", -1)):
        trig = {d: sgn * (1 if g[d] > 0 else -1) for d in elig if abs(g[d]) >= sd[d]}
        for e, exits in ((0, (1, 3, 6, "FP", "TS")), (1, (2, 4, 6, "FP", "TS"))):
            for ex in exits:
                for s in DIR:
                    directional_cell(m, {"part": "W2", "ticker": tk, "window": "gap", "variant": var}, trig, elig, e, s, ex)
    say(f"{tk} W2 done")
    # W3 intraday momentum
    r = {d: math.log(P[d][1] / m.prev_close(d)) for d in hist}
    p67 = rolling({d: abs(v) for d, v in r.items()}, hist, lambda w: pctl(w, 0.67))
    elig = [d for d in days if d in p67]
    for s in DIR:
        trig = {d: (1 if r[d] > 0 else -1) for d in elig if r[d] != 0}
        ev = by_split((d, trade(m, d, 6, sd_, s, 7)) for d, sd_ in trig.items())
        base = by_split((d, avg_sides(trade(m, d, 6, 1, s, 7), trade(m, d, 6, -1, s, 7))) for d in trig)
        score({"part": "W3", "ticker": tk, "window": "last-half-hour", "variant": "all", "struct": s,
               "entry": "15:30", "exit": "16:00"}, ev, base)
        trig = {d: (1 if r[d] > 0 else -1) for d in elig if abs(r[d]) >= p67[d] and r[d] != 0}
        directional_cell(m, {"part": "W3", "ticker": tk, "window": "last-half-hour", "variant": "top-tercile"}, trig, elig, 6, s, 7)
    # W4 FOMC
    fomc = [d for d in days if d in types["fomc"]]
    non = [d for d in days if d not in types["fomc"]]
    for s in ("S0", "S1"):
        for x in (5, 6):
            straddle_cell(m, {"part": "W4", "ticker": tk, "window": "fomc", "variant": "straddle"}, fomc, non, 4, x, s)
    for var, sgn in (("cont", 1), ("fade", -1)):
        trig = {d: sgn * (1 if P[d][5] > P[d][4] else -1) for d in fomc if P[d][5] != P[d][4]}
        for s in DIR:
            directional_cell(m, {"part": "W4", "ticker": tk, "window": "fomc", "variant": var}, trig, days, 5, s, 6)
    # W5 08:30 macro
    mac = [d for d in days if d in types["macro0830"]]
    non = [d for d in days if d not in types["macro0830"]]
    for s in ("S0", "S1"):
        for x in (1, 3, 6):
            straddle_cell(m, {"part": "W5", "ticker": tk, "window": "macro0830", "variant": "straddle"}, mac, non, 0, x, s)
    for var, sgn in (("go", 1), ("fill", -1)):
        trig = {d: sgn * (1 if g[d] > 0 else -1) for d in mac if g.get(d, 0) != 0}
        for x in (4, 6):
            for s in DIR:
                directional_cell(m, {"part": "W5", "ticker": tk, "window": "macro0830", "variant": var}, trig, days, 1, s, x)
    # W6 ISM 10:00
    ism = [d for d in days if d in types["ism"]]
    non = [d for d in days if d not in types["ism"]]
    for s in ("S0", "S1"):
        for x in (1, 3):
            straddle_cell(m, {"part": "W6", "ticker": tk, "window": "ism1000", "variant": "straddle"}, ism, non, 0, x, s)
    # W7 OpEx vs other Fridays
    opx = [d for d in days if d in types["opex"]]
    fri = [d for d in days if d.weekday() == 4 and d not in types["opex"]]
    for s in ("S0", "S1"):
        for e in (1, 4):
            straddle_cell(m, {"part": "W7", "ticker": tk, "window": "opex", "variant": "straddle"}, opx, fri, e, 6, s)
    say(f"{tk} W3-W7 done")


def _merge(rs: list[dict]) -> dict[str, list[float]]:
    out = defaultdict(list)
    for r in rs:
        for k, v in r.items():
            out[k].append(v)
    return out


# ------------------------------------------------------------------ Part 3: H-MOM1 day-after
def part3() -> None:
    ev_rows = list(csv.DictReader((DATA / "prior_continuation_events.csv").read_text().splitlines()))
    ev_rows = [r for r in ev_rows if r["k"] == "2.5" and r["type"]]
    pools = {"strict": [r for r in ev_rows if r["type"] == "idio" and r["volume"] == "high"
                        and r["close"] == "strong" and r["vix"] in ("low", "mid")],
             "all": ev_rows}
    daily = {tk: nasdaq(tk) for tk in {r["ticker"] for r in ev_rows}}
    oos3 = date(2021, 7, 1)
    sp3 = lambda d: "OOS" if d >= oos3 else "IS"
    info = {}
    for tk, ser in daily.items():
        ds = [d for d in ser if d >= date(2016, 11, 1)]
        rv = {}
        for i in range(21, len(ds)):
            lr = [math.log(ser[ds[j]][3] / ser[ds[j - 1]][3]) for j in range(i - 19, i + 1)]
            rv[ds[i]] = st.stdev(lr) * math.sqrt(252)
        info[tk] = (ds, {d: i for i, d in enumerate(ds)}, rv)
    say(f"Part 3 events: strict {len(pools['strict'])}, all {len(pools['all'])}")

    def rets(tk, i):
        ds, _, _ = info[tk]
        ser = daily[tk]
        c0, o1, c1 = ser[ds[i]][3], ser[ds[i + 1]][0], ser[ds[i + 1]][3]
        return {"overnight": math.log(o1 / c0), "intraday": math.log(c1 / o1), "full": math.log(c1 / c0)}

    # unconditional means per ticker and split
    um = {}
    for tk in daily:
        ds = info[tk][0]
        acc = defaultdict(list)
        for i in range(21, len(ds) - 1):
            for k, v in rets(tk, i).items():
                acc[(sp3(ds[i]), k)].append(v)
        um[tk] = {k: st.mean(v) for k, v in acc.items()}

    global TRIAL
    for pool, rows in pools.items():
        evs = []
        for r in rows:
            tk, d = r["ticker"], date.fromisoformat(r["date"])
            ds, idx, rv = info[tk]
            if d not in idx or idx[d] + 1 >= len(ds) or d not in rv:
                continue
            evs.append((tk, idx[d], 1 if r["side"] == "C" else -1))
        for k in ("overnight", "intraday", "full"):
            row = {"trial": TRIAL, "part": "3-price", "ticker": pool, "window": "day-after", "variant": k,
                   "struct": "underlying", "entry": "", "exit": ""}
            TRIAL += 1
            for sp in ("IS", "OOS"):
                xs = [s * rets(tk, i)[k] - s * um[tk][(sp, k)] for tk, i, s in evs if sp3(info[tk][0][i]) == sp]
                raw = [s * rets(tk, i)[k] for tk, i, s in evs if sp3(info[tk][0][i]) == sp]
                row[f"n_{sp}"] = len(xs)
                row[f"mean_{sp}_gross"] = st.mean(raw) if raw else math.nan
                row[f"exc_{sp}_gross"] = st.mean(xs) if xs else math.nan
                row[f"t_{sp}"] = (st.mean(xs) / (st.stdev(xs) / math.sqrt(len(xs)))) if len(xs) > 2 else math.nan
            row["eligible"], row["pass"] = row["n_OOS"] >= 20, False
            ROWS.append(row)
        for entry in ("close", "open"):
            for dte in (14, 7):
                def opt(tk, i, s):
                    ds, _, rv = info[tk]
                    ser = daily[tk]
                    d0, d1 = ds[i], ds[i + 1]
                    v = rv[d0] + 0.034
                    if entry == "close":
                        S0, T0 = ser[d0][3], dte / 365
                        T1 = (dte - (d1 - d0).days) / 365
                    else:
                        S0, T0 = ser[d1][0], dte / 365
                        T1 = (dte - 6.5 / 24) / 365
                    S1 = ser[d1][3]
                    K = S0
                    p0, p1 = bs(S0, K, T0, v, s), bs(S1, K, T1, v, s)
                    if p0 <= 0.01:
                        return {}
                    out = {}
                    for mode in COSTS:
                        c = {"gross": 0, "k70": 0.2 * 0.03, "k100": 0.5 * 0.03, "dps": 0.045}[mode]
                        cm = 0 if mode == "gross" else COMM
                        buy = p0 * (1 + c) + cm
                        sell = p1 * (1 - c) - cm if p1 > 0.005 else 0.0
                        out[mode] = sell / buy - 1
                    return out
                ev = defaultdict(list)
                for tk, i, s in evs:
                    r = opt(tk, i, s)
                    if r:
                        ev[sp3(info[tk][0][i])].append(r)
                evset = {(tk, i) for tk, i, _ in evs}
                base = defaultdict(list)
                for tk in daily:
                    ds, _, rv = info[tk]
                    for i in range(21, len(ds) - 1):
                        if (tk, i) in evset or ds[i] not in rv:
                            continue
                        a, b = opt(tk, i, 1), opt(tk, i, -1)
                        if a and b:
                            base[sp3(ds[i])].append(avg_sides(a, b))
                score({"part": "3-opt", "ticker": pool, "window": "day-after", "variant": f"entry-{entry}",
                       "struct": f"ATM{dte}", "entry": entry, "exit": "next close"}, ev, base)
    say("Part 3 done")


# ------------------------------------------------------------------ main
def main() -> None:
    LOG.append(f"run {datetime.now().isoformat(timespec='seconds')}")
    spy_h, qqq_h, v1h = hourly("SPY"), hourly("QQQ"), hourly("VIX1D")
    vix, vxn, v1d = cboe("VIX"), cboe("VXN"), cboe("VIX1D")
    spy_d, qqq_d = nasdaq("SPY"), nasdaq("QQQ")
    md = macro_dates()
    spy = Mkt("SPY", spy_h, v1h, vix, vxn, spy_d)
    qqq = Mkt("QQQ", qqq_h, v1h, vix, vxn, qqq_d)
    days = sorted(d for d in spy_h if d >= START and d in v1h and d in qqq_h and d in spy_d and d in qqq_d
                  and spy.didx.get(d, 0) > 0)
    days = [d for d in days if not math.isnan(qqq.prev_daily(vxn, d)) and not math.isnan(qqq.prev_daily(vix, d))]
    sset = set(spy_d)
    types = {"fomc": md["fomc"], "macro0830": md["cpi"] | md["nfp"], "ism": md["ism_mfg"] | md["ism_services"],
             "opex": opex_dates(sset)}
    types["all"] = set(spy_d)
    special = types["fomc"] | types["macro0830"] | types["ism"] | types["opex"]
    types["other"] = set(spy_d) - special
    say(f"sessions {len(days)} ({days[0]} -> {days[-1]}); IS {sum(d < OOS for d in days)}, OOS {sum(d >= OOS for d in days)}")
    say("day types in sample: " + ", ".join(f"{k} {sum(d in v for d in days)}" for k, v in types.items()))
    vrp = part1(spy, days, types, v1d, spy_d)
    with open(HERE / "vrp.csv", "w", newline="") as f:
        keys = sorted({k for r in vrp for k in r}, key=lambda k: (k not in ("trial", "part", "mark", "daytype"), k))
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(vrp)
    say(f"Part 1a/1b written: {len(vrp)} cells")
    for m, tk in ((spy, "SPY"), (qqq, "QQQ")):
        hist = sorted(d for d in m.px if m.didx.get(d, 0) > 0 and (d < START or d in days))
        part2(m, days, types, hist)
    part3()
    keys = ["trial", "part", "ticker", "window", "variant", "struct", "entry", "exit", "n_IS", "n_OOS",
            "mean_OOS_k70", "base_OOS_k70", "exc_OOS_k70", "t_OOS", "exc_IS_k70", "t_IS", "exc_OOS_k100",
            "exc_OOS_dps", "exc_OOS_gross", "mean_OOS_gross", "mean_IS_k70", "eligible", "pass"]
    with open(HERE / "results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        for r in ROWS:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
    with open(HERE / "trades_sample.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "ticker", "entry", "exit", "side", "struct", "S_entry", "sigma_entry", "legs", "ret_k70"])
        for d in days[:200]:
            side = 1 if spy.px[d][1] > spy.px[d][0] else -1
            lg = legs(spy, d, 1, side, "A0")
            r = trade(spy, d, 1, side, "A0", 4)
            w.writerow([d, "SPY", "10:30", "13:30", side, "A0", f"{spy.px[d][1]:.2f}", f"{spy.sigma(d, 1):.4f}",
                        lg, f"{r.get('k70', math.nan):.4f}"])
    n_el = sum(1 for r in ROWS if r.get("eligible"))
    passed = [r for r in ROWS if r.get("pass")]
    say(f"trading cells {len(ROWS)}, eligible {n_el}, passed {len(passed)}; trials {FIRST_TRIAL}..{TRIAL - 1}")
    for r in passed:
        say(f"PASS #{r['trial']}: {r['part']} {r['ticker']} {r['window']} {r['variant']} {r['struct']} "
            f"{r['entry']}->{r['exit']} exc {r['exc_OOS_k70']:+.3f} t {r['t_OOS']:.2f}")
    (HERE / "run.log").write_text("\n".join(LOG) + "\n")


def selftest() -> None:
    S, K, T, v = 500.0, 500.0, tau(1, 0), 0.15
    c, p = bs(S, K, T, v, 1), bs(S, K, T, v, -1)
    assert abs(c - p) < 1e-9, (c, p)                       # parity at r=0, K=S
    assert abs(c - 0.4 * S * v * math.sqrt(T)) / c < 0.02  # ATM ~ 0.4 S sigma sqrt(T)
    K30 = strike_for(S, T, v, 1, 0.30)
    assert K30 > S and abs(delta(S, K30, T, v, 1) - 0.30) < 0.08, K30
    K30p = strike_for(S, T, v, -1, 0.30)
    assert K30p < S
    assert bs(S, 490, 0, v, 1) == 10.0 and bs(S, 510, 0, v, 1) == 0.0
    assert abs(tau(0, 0) - 390 / (252 * 405)) < 1e-12 and abs(tau(7, 1) - 1 / 252) < 1e-12
    assert abs(leg_cost(1.0, 3, "k70") - (0.2 * 0.03 + COMM)) < 1e-12 and leg_cost(0.0, 3, "k70") == 0.0
    assert abs(leg_cost(0.10, 0, "k100") - (0.5 * 0.01 + COMM)) < 1e-12
    print("selftest ok")


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else main()
