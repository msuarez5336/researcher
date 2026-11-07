"""Post-run diagnostics (not trials). Run from repo root after intraday.py.

D1: open-hour 0DTE straddle with the exit priced at the ENTRY sigma (removes VIX1D's intraday
    re-weighting), and the first hour's share of the session's realised variance.
D2: Part 3 price rows, IS and OOS side by side.
"""
import csv
import math
import statistics as st
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import intraday as I  # noqa: E402

spy_h, qqq_h, v1h = I.hourly("SPY"), I.hourly("QQQ"), I.hourly("VIX1D")
vix, vxn = I.cboe("VIX"), I.cboe("VXN")
out = []
for tk, px, dl in (("SPY", spy_h, I.nasdaq("SPY")), ("QQQ", qqq_h, I.nasdaq("QQQ"))):
    m = I.Mkt(tk, px, v1h, vix, vxn, dl)
    days = [d for d in sorted(px) if d >= I.START and d in v1h and m.didx.get(d, 0) > 0
            and not math.isnan(m.prev_daily(vxn, d))]
    for sp in ("IS", "OOS"):
        ds = [d for d in days if I.split(d) == sp]
        r_vix, r_const, share, sig0, sig1 = [], [], [], [], []
        for d in ds:
            S0, S1, s0 = px[d][0], px[d][1], m.sigma(d, 0)
            K = float(round(S0))
            c0 = sum(I.bs(S0, K, I.tau(0, 0), s0, cp) for cp in (1, -1))
            costs0 = sum(I.leg_cost(I.bs(S0, K, I.tau(0, 0), s0, cp), 0, "k70") for cp in (1, -1))
            for sig_exit, acc in ((m.sigma(d, 1), r_vix), (s0, r_const)):
                v = [I.bs(S1, K, I.tau(1, 0), sig_exit, cp) for cp in (1, -1)]
                acc.append((sum(v) - sum(I.leg_cost(x, 1, "k70") for x in v)) / (c0 + costs0) - 1)
            rv = [math.log(px[d][j + 1] / px[d][j]) ** 2 for j in range(7)]
            share.append(rv[0] / sum(rv) if sum(rv) else math.nan)
            sig0.append(s0); sig1.append(m.sigma(d, 1))
        out.append(f"D1 {tk} {sp} n={len(ds)}: open-hour S0 k70 mean, exit at VIX1D(10:30) {st.mean(r_vix):+.3f}; "
                   f"exit at entry sigma {st.mean(r_const):+.3f}; first-hour share of session realised variance "
                   f"{st.mean([x for x in share if not math.isnan(x)]):.3f} (clock share {60/390:.3f}); "
                   f"mean sigma 09:30 {st.mean(sig0):.4f} vs 10:30 {st.mean(sig1):.4f}")
for r in csv.DictReader((HERE / "results.csv").read_text().splitlines()):
    if r["part"] == "3-price":
        out.append(f"D2 #{r['trial']} {r['ticker']} {r['variant']}: n {r['n_IS']}/{r['n_OOS']}  t IS {r['t_IS']} OOS {r['t_OOS']}  "
                   f"raw mean OOS {r['mean_OOS_gross']}  excess OOS {r['exc_OOS_gross']}")
(HERE / "diagnostics.log").write_text("\n".join(out) + "\n")
print("\n".join(out))
