"""Trial 4: does implied vol over- or under-price 10-day moves?
For each day t with a Cboe vol index value: a 10-trading-day ATM straddle priced at implied costs
about 0.798 * IV * sqrt(10/252) * S (Brenner-Subrahmanyam approximation); it pays |S_t+10 - S_t|.
Gross return = |C_t+10/C_t - 1| / (0.798 * IV * sqrt(10/252)) - 1. No spreads, skew or early exit:
a pricing test, not the 35-60 DTE strategy. Overlapping windows; t-stat uses non-overlapping (every 10th day)."""
import csv, math, statistics as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import screen as s
HERE = Path(__file__).parent
PAIRS = {"SPY": "VIX", "QQQ": "VXN", "IWM": "RVX", "AAPL": "VXAPL", "AMZN": "VXAZN", "GOOGL": "VXGOG",
         "EWZ": "VXEWZ", "TLT": "VXTLT"}
rows = []
for tk, ix in PAIRS.items():
    b = s.load_ohlc(tk); vol = s.load_vol_index(ix)
    rets = []
    for t in range(len(b) - 10):
        iv = vol.get(b[t][0])
        if not iv: continue
        cost = 0.798 * iv / 100 * math.sqrt(10 / 252)
        rets.append(abs(b[t + 10][4] / b[t][4] - 1) / cost - 1)
    if len(rets) < 250:
        rows.append([tk, ix, len(rets), "", "", "", ""]); continue
    nov = rets[::10]
    tstat = st.mean(nov) / (st.stdev(nov) / math.sqrt(len(nov)))
    win = sum(r > 0 for r in rets) / len(rets)
    rows.append([tk, ix, len(rets), f"{st.mean(rets):+.3f}", f"{st.median(rets):+.3f}", f"{win:.3f}", f"{tstat:+.2f}"])
with open(HERE / "trial4_straddle_iv.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ticker", "vol_index", "days", "mean_gross_return", "median", "win_rate", "t_nonoverlap"]); w.writerows(rows)
for r in rows: print(r)
