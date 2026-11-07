"""Trial 5: the trial-4 straddle (10-day ATM, priced at implied, gross) split by entry condition.
  cheap   : IV < 100 * rv20 (implied below trailing 20-day realised; Goyal-Saretto-style condition)
  rich    : IV >= 100 * rv20
  squeeze : 20-day ATR% in bottom 20% of its trailing 120 days (screen_spec 'compressed')
  cheap+squeeze : both
Conditions use only data up to day t. Report mean gross return, n, non-overlapping t-stat."""
import csv, math, statistics as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import screen as s
HERE = Path(__file__).parent
PAIRS = {"SPY": "VIX", "QQQ": "VXN", "IWM": "RVX", "AAPL": "VXAPL", "AMZN": "VXAZN", "GOOGL": "VXGOG", "EWZ": "VXEWZ"}
def summ(x):
    if len(x) < 60: return (len(x), "", "")
    nov = x[::10]
    t = st.mean(nov) / (st.stdev(nov) / math.sqrt(len(nov))) if len(nov) > 2 else float("nan")
    return (len(x), f"{st.mean(x):+.3f}", f"{t:+.2f}")
out = []
for tk, ix in PAIRS.items():
    b = s.load_ohlc(tk); vol = s.load_vol_index(ix)
    C = [x[4] for x in b]; H = [x[2] for x in b]; L = [x[3] for x in b]
    r = [math.nan] + [math.log(C[i] / C[i-1]) for i in range(1, len(C))]
    tr = [math.nan] + [max(H[i]-L[i], abs(H[i]-C[i-1]), abs(L[i]-C[i-1])) for i in range(1, len(C))]
    atrp = [math.nan]*len(C)
    for i in range(20, len(C)): atrp[i] = sum(tr[i-19:i+1]) / 20 / C[i]
    g = {"all": [], "cheap": [], "rich": [], "squeeze": [], "cheap+squeeze": []}
    for t in range(140, len(b) - 10):
        iv = vol.get(b[t][0])
        if not iv: continue
        ret = abs(C[t+10] / C[t] - 1) / (0.798 * iv / 100 * math.sqrt(10/252)) - 1
        rv20 = st.stdev(r[t-19:t+1]) * math.sqrt(252)
        win = atrp[t-119:t+1]; sq = sum(v <= atrp[t] for v in win) / 120 <= 0.20
        cheap = iv / 100 < rv20
        g["all"].append(ret); g["cheap" if cheap else "rich"].append(ret)
        if sq: g["squeeze"].append(ret)
        if sq and cheap: g["cheap+squeeze"].append(ret)
    for k, v in g.items(): out.append([tk, k, *summ(v)])
with open(HERE / "trial5_conditional.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ticker", "condition", "n_days", "mean_gross_return", "t_nonoverlap"]); w.writerows(out)
for tk in PAIRS:
    print(tk.ljust(6), "  ".join(f"{c}:{m or 'n<60'}({n})" for t, c, n, m, _ in out if t == tk))
