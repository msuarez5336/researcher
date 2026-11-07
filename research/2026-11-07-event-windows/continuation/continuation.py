"""Continuation study: buy a short-dated option in the direction of a large move. Implements spec.md.

Usage (from repo root):
    python3 research/2026-11-07-event-windows/continuation/continuation.py --selftest
    python3 research/2026-11-07-event-windows/continuation/continuation.py

Reuses ../study/events.py (data loaders, Black-Scholes, earnings cache). Writes results.csv,
events.csv, price_continuation.csv and run.log next to this file. Earnings days are excluded.
"""
from __future__ import annotations

import csv
import json
import math
import statistics as st
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "study"))
import events as E  # noqa: E402

KS = (2.0, 2.5, 3.0)
STRUCTS = {"ATM7": (7, None), "ATM14": (14, None), "ATM30": (30, None), "OTM30d14": (14, 0.30)}
EXITS = ["fix1", "fix2", "fix3", "fix5", "green", "green+1", "green+2", "tp30sl40", "trail"]
COSTS = {"gross": 0.0, "k0.70": 0.006, "k1.00": 0.015}
MAXH = 5
TRIALS_BEFORE = 348
ROWS: list[dict] = []
EVROWS: list[dict] = []


def volumes(tk):
    p = Path(E.screen.DATA) / f"{tk}.json"
    out = {}
    for r in json.loads(p.read_text()):
        try:
            out[datetime.strptime(r["date"], "%m/%d/%Y").date()] = float(str(r["volume"]).replace(",", ""))
        except (KeyError, ValueError):
            pass
    return out


# ------------------------------------------------------------------ option path and exits
def legs_for(S0, T0, iv0, cp, delta):
    if delta is None:
        return [S0]
    return [E.strike_for_delta(S0, T0, iv0, cp, delta)]


def path(S, ivs, cp, dte, delta):
    """S, ivs: lists for d = 0..MAXH. Returns list of option values per day (single leg)."""
    T0 = dte / 365
    K = legs_for(S[0], T0, ivs[0], cp, delta)[0]
    return [E.bs(S[d], K, (dte - d * 7 / 5) / 365, ivs[d], cp) for d in range(len(S))]


def pnl_series(vals, c):
    paid = vals[0] * (1 + c) + E.COMM if c else vals[0]
    if paid <= 0:
        return None
    return [((v * (1 - c) - E.COMM if c else v) - paid) / paid for v in vals]


def apply_exits(pnl, S, direction):
    """pnl: list d = 0..MAXH of P&L if sold at close d. Returns {exit: pnl}."""
    out = {f"fix{h}": pnl[h] for h in (1, 2, 3, 5)}
    g = next((d for d in range(1, MAXH + 1) if pnl[d] > 0), None)
    out["green"] = pnl[g] if g else pnl[MAXH]
    out["green+1"] = pnl[min(g + 1, MAXH)] if g else pnl[MAXH]
    out["green+2"] = pnl[min(g + 2, MAXH)] if g else pnl[MAXH]
    tp = next((d for d in range(1, MAXH + 1) if pnl[d] >= 0.30 or pnl[d] <= -0.40), MAXH)
    out["tp30sl40"] = pnl[tp]
    if g:
        tr = next((d for d in range(g + 1, MAXH + 1) if (S[d] - S[d - 1]) * direction < 0), MAXH)
        out["trail"] = pnl[tr]
    else:
        out["trail"] = pnl[MAXH]
    return out


# ------------------------------------------------------------------ IV models
class Vol:
    def __init__(self, ser, idx, vix, vix9d):
        self.ser, self.idx, self.vix, self.vix9d = ser, idx, vix, vix9d

    def ts(self, i):
        d = self.ser.d[i]
        a, b = self.vix9d.get(d), self.vix.get(d)
        return a / b if a and b else 1.0

    def base(self, i):
        if self.idx is not None:
            v = self.idx.get(self.ser.d[i])
            return v / 100 if v else math.nan
        r = self.ser.rv20[i]
        return (100 * r + E.VRP_PROXY) / 100 if not math.isnan(r) else math.nan

    def at(self, i, dte):
        b = self.base(i)
        return b * self.ts(i) if dte <= 14 else b


def iv_path(vol, e, dte, decay=None, direction=None):
    """IV for d = 0..MAXH from entry index e. Non-indexed event trades use the decay table."""
    if vol.idx is None and decay is not None:
        iv0 = vol.at(e, dte)
        return [iv0] + [iv0 * decay[direction][d] for d in range(1, MAXH + 1)]
    return [vol.at(e + d, dte) for d in range(MAXH + 1)]


# ------------------------------------------------------------------ baseline (random days)
BASE: dict = {}


def baseline(ser, vol, cp, sname, period):
    key = (ser.tk, cp, sname, period)
    if key in BASE:
        return BASE[key]
    dte, delta = STRUCTS[sname]
    acc = {(x, c): [] for x in EXITS for c in COSTS}
    direction = 1 if cp == "C" else -1
    for e in range(62, len(ser.d) - MAXH - 1):
        if E.per(ser, e) != period:
            continue
        ivs = iv_path(vol, e, dte)
        if any(math.isnan(v) for v in ivs):
            continue
        S = ser.C[e:e + MAXH + 1]
        vals = path(S, ivs, cp, dte, delta)
        for c, cv in COSTS.items():
            pn = pnl_series(vals, cv)
            if pn is None:
                continue
            for x, v in apply_exits(pn, S, direction).items():
                acc[(x, c)].append(v)
    BASE[key] = {k: (st.mean(v) if v else math.nan) for k, v in acc.items()}
    return BASE[key]


# ------------------------------------------------------------------ scoring
def score(label, pool, k, sname, exit_, entry, split, items):
    """items: list of (period, {cost: ret}, {cost: base}). One row per cell (scored at k0.70)."""
    row = {"study": "continuation", "pool": pool, "k": k, "structure": sname, "exit": exit_,
           "entry": entry, "split": split, "label": label}
    for c in ("gross", "k0.70", "k1.00"):
        for p in ("IS", "OOS"):
            xs = [r[c] for pp, r, b in items if pp == p and not math.isnan(r[c])]
            ex = [r[c] - b[c] for pp, r, b in items if pp == p and not math.isnan(r[c]) and not math.isnan(b[c])]
            tag = f"{c}_{p}"
            row[f"n_{p}"] = len(xs)
            row[f"mean_{tag}"] = round(st.mean(xs), 4) if xs else ""
            row[f"excess_{tag}"] = round(st.mean(ex), 4) if ex else ""
            row[f"t_{tag}"] = round(E.tstat(ex), 2) if len(ex) >= 3 else ""
            row[f"win_{tag}"] = round(sum(x > 0 for x in xs) / len(xs), 3) if xs else ""
    ok = (row["n_OOS"] >= 30 and row["excess_k0.70_OOS"] != "" and row["excess_k0.70_OOS"] >= 0.10
          and row["t_k0.70_OOS"] != "" and row["t_k0.70_OOS"] >= 3
          and row["excess_k0.70_IS"] != "" and row["excess_k0.70_IS"] > 0
          and row["excess_k1.00_OOS"] != "" and row["excess_k1.00_OOS"] > 0)
    row["promising"] = ok
    ROWS.append(row)


# ------------------------------------------------------------------ main
def main():
    log = [f"run {datetime.now().isoformat(timespec='seconds')}"]
    say = lambda m: print(f"[{datetime.now():%H:%M:%S}] {m}", flush=True)
    tickers = E.ETFS + E.STOCKS
    series = {tk: E.Series(tk) for tk in tickers}
    vix, vix9d = E.vol_index("VIX"), E.vol_index("VIX9D")
    idx = {tk: (E.vol_index(E.IV_MAP[tk]) if tk in E.IV_MAP else None) for tk in tickers}
    vols = {tk: Vol(series[tk], idx[tk], vix, vix9d) for tk in tickers}
    vol_of = {tk: volumes(tk) for tk in tickers}
    spy = series["SPY"]
    say("data loaded")

    def vix_terc(d):
        j = spy.idx.get(d)
        if j is None or j < 253 or d not in vix:
            return "na"
        hist = sorted(vix[x] for x in spy.d[j - 252:j] if x in vix)
        lo, hi = hist[len(hist) // 3], hist[2 * len(hist) // 3]
        return "low" if vix[d] < lo else ("mid" if vix[d] < hi else "high")

    # 1) events per k
    events = {k: [] for k in KS}
    dropped = 0
    for tk in tickers:
        ser = series[tk]; vmap = vol_of[tk]
        for k in KS:
            cand = [i for i in range(63, len(ser.d) - MAXH - 2) if abs(ser.r[i]) >= k * ser.s60[i]]
            for i in E.declustered(cand):
                if tk in E.STOCKS and (tk in E.earnings_on(ser.d[i]) or tk in E.earnings_on(ser.d[i - 1])):
                    dropped += 1
                    continue
                direction = 1 if ser.r[i] > 0 else -1
                clv = ser.clv(i)
                strong = clv >= 0.8 if direction > 0 else clv <= 0.2
                past = [vmap.get(ser.d[j]) for j in range(i - 20, i)]
                past = [x for x in past if x]
                vr = (vmap.get(ser.d[i], 0) / (sum(past) / len(past))) if past else 0
                gap = abs(ser.O[i] - ser.C[i - 1]) / abs(ser.C[i] - ser.C[i - 1]) if ser.C[i] != ser.C[i - 1] else 0
                tags = {"close": "strong" if strong else "faded", "volume": "high" if vr >= 2 else "normal",
                        "gap": "gap-driven" if gap >= 0.5 else "intraday", "vix": vix_terc(ser.d[i])}
                if tk in E.STOCKS:
                    j = spy.idx.get(ser.d[i])
                    rs, ss = spy.r[j], spy.s60[j]
                    tags["type"] = "idio" if abs(rs) < ss else ("market" if rs * ser.r[i] > 0 and abs(rs) > 1.5 * ss else "mixed")
                confirmed = (ser.r[i + 1] * direction) > 0
                events[k].append((tk, i, direction, confirmed, tags))
    say(f"events: {[len(events[k]) for k in KS]}; earnings-dropped {dropped}")

    # 2) IV decay table D(d, direction) from indexed tickers' events (all k, EOD entry)
    dec = {1: [[] for _ in range(MAXH + 1)], -1: [[] for _ in range(MAXH + 1)]}
    for k in KS:
        for tk, i, direction, _, _ in events[k]:
            v = vols[tk]
            if v.idx is None:
                continue
            b0 = v.base(i)
            for d in range(1, MAXH + 1):
                bd = v.base(i + d)
                if not math.isnan(b0) and not math.isnan(bd) and b0 > 0:
                    dec[direction][d].append(bd / b0)
    decay = {s: [1.0] + [st.mean(dec[s][d]) for d in range(1, MAXH + 1)] for s in (1, -1)}
    log.append("IV decay table (mean IV_{t+d}/IV_t, indexed events): up " +
               " ".join(f"d{d}={decay[1][d]:.3f}" for d in range(1, MAXH + 1)) + " | down " +
               " ".join(f"d{d}={decay[-1][d]:.3f}" for d in range(1, MAXH + 1)))

    # 3) price-only continuation
    with open(HERE / "price_continuation.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["k", "pool", "period", "n", "cont_1d", "cont_2d", "cont_3d", "cont_5d", "share_up_1d"])
        for k in KS:
            for pool, members in (("ETFs", E.ETFS), ("stocks", E.STOCKS)):
                for p in ("IS", "OOS", "all"):
                    ev = [(series[tk], i, s) for tk, i, s, _, _ in events[k] if tk in members and (p == "all" or E.per(series[tk], i) == p)]
                    if not ev:
                        continue
                    c = {h: [s * math.log(ser.C[i + h] / ser.C[i]) for ser, i, s in ev] for h in (1, 2, 3, 5)}
                    w.writerow([k, pool, p, len(ev)] + [f"{st.mean(c[h]):+.4f}" for h in (1, 2, 3, 5)] +
                               [f"{sum(x > 0 for x in c[1]) / len(ev):.3f}"])
    say("price continuation written")

    # 4) option trades
    def trade(tk, i, direction, entry, sname):
        ser, v = series[tk], vols[tk]
        e = i if entry == "EOD" else i + 1
        dte, delta = STRUCTS[sname]
        cp = "C" if direction > 0 else "P"
        ivs = iv_path(v, e, dte, decay if v.idx is None else None, direction)
        if any(math.isnan(x) for x in ivs) or e + MAXH >= len(ser.d):
            return None
        S = ser.C[e:e + MAXH + 1]
        vals = path(S, ivs, cp, dte, delta)
        res = {}
        for c, cv in COSTS.items():
            pn = pnl_series(vals, cv)
            if pn is None:
                return None
            for x, val in apply_exits(pn, S, direction).items():
                res.setdefault(x, {})[c] = val
        p = E.per(ser, e)
        b = baseline(ser, v, cp, sname, p)
        return p, res, {x: {c: b[(x, c)] for c in COSTS} for x in EXITS}, cp

    for k in KS:
        for pool, members in (("ETFs", E.ETFS), ("stocks", E.STOCKS)):
            for sname in STRUCTS:
                for entry in ("EOD", "confirmed"):
                    trades = []
                    for tk, i, direction, conf, tags in events[k]:
                        if tk not in members or (entry == "confirmed" and not conf):
                            continue
                        t = trade(tk, i, direction, entry, sname)
                        if t:
                            trades.append((t, tags))
                            if sname == "ATM14" and entry == "EOD":
                                EVROWS.append({"k": k, "ticker": tk, "date": str(series[tk].d[i]), "side": t[3],
                                               "move_sigma": round(abs(series[tk].r[i]) / series[tk].s60[i], 2), **tags,
                                               "pnl_fix2_k0.70": round(t[1]["fix2"]["k0.70"], 4),
                                               "pnl_green_k0.70": round(t[1]["green"]["k0.70"], 4)})
                    for x in EXITS:
                        items = [(t[0], t[1][x], t[2][x]) for t, _ in trades]
                        score("main", pool, k, sname, x, entry, "all", items)
                        if k == 2.5 and entry == "EOD":
                            keys = ["close", "volume", "gap", "vix"] + (["type"] if pool == "stocks" else [])
                            for key in keys:
                                for val in sorted({tg[key] for _, tg in trades}):
                                    if val == "na":
                                        continue
                                    sub = [(t[0], t[1][x], t[2][x]) for t, tg in trades if tg[key] == val]
                                    score("filter", pool, k, sname, x, entry, f"{key}={val}", sub)
            say(f"k={k} scored")

    with open(HERE / "results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(ROWS[0].keys())); w.writeheader(); w.writerows(ROWS)
    keys = sorted({k for r in EVROWS for k in r})
    with open(HERE / "events.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(EVROWS)
    prom = [r for r in ROWS if r["promising"]]
    log.append(f"events per k {[len(events[k]) for k in KS]}; stock events dropped for earnings {dropped}")
    log.append(f"cells scored this run: {len(ROWS)}; cumulative trials: {TRIALS_BEFORE + len(ROWS)}")
    log.append(f"promising cells: {len(prom)}")
    for r in prom:
        log.append(f"  PROMISING {r['pool']} k={r['k']} {r['structure']} {r['exit']} {r['entry']} {r['split']} | "
                   f"OOS excess {r['excess_k0.70_OOS']} t {r['t_k0.70_OOS']} n {r['n_OOS']} | IS {r['excess_k0.70_IS']} | k1.0 OOS {r['excess_k1.00_OOS']}")
    (HERE / "run.log").write_text("\n".join(log) + "\n")
    print("\n".join(log))


def selftest():
    # exits on a hand-made P&L path
    pnl = [0.0, -0.1, 0.05, 0.2, -0.05, 0.4]
    S = [100, 99, 101, 103, 102, 106]
    x = apply_exits(pnl, S, +1)
    assert x["fix1"] == -0.1 and x["fix5"] == 0.4
    assert x["green"] == 0.05 and x["green+1"] == 0.2 and x["green+2"] == -0.05
    assert x["tp30sl40"] == 0.4          # +30% first reached on day 5
    assert x["trail"] == -0.05           # first green day 2, first down close after it is day 4
    # option path: rising underlying helps a call, costs reduce P&L, short DTE decays faster
    vals7 = path([100] * 6, [0.3] * 6, "C", 7, None)
    vals30 = path([100] * 6, [0.3] * 6, "C", 30, None)
    assert vals7[-1] < vals7[0] and (vals7[0] - vals7[-1]) / vals7[0] > (vals30[0] - vals30[-1]) / vals30[0]
    g = pnl_series(path([100, 102, 103, 103, 103, 103], [0.3] * 6, "C", 14, None), 0.0)
    n = pnl_series(path([100, 102, 103, 103, 103, 103], [0.3] * 6, "C", 14, None), 0.006)
    assert g[1] > 0 and n[1] < g[1]
    # 0.30 delta strike is OTM
    K = legs_for(100, 14 / 365, 0.3, "C", 0.30)[0]
    assert K > 100
    print("selftest ok: 7DTE flat 5d decay", round(1 - vals7[-1] / vals7[0], 3), "| 30DTE", round(1 - vals30[-1] / vals30[0], 3))


if __name__ == "__main__":
    selftest() if "--selftest" in sys.argv else main()
