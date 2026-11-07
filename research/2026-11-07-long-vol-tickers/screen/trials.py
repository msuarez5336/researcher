"""Logged sensitivity trials on top of the frozen screen (see screen_spec.md change log).
Trial 2: payoff10 = mean(max(|ln(C_t+10/C_t)| / sigma10_t - 1, 0)), the expected payoff of a
1-sigma strangle priced at recent realised vol, in sigma units. Normal null = 0.1666.
Trial 3: frozen score with a sector cap of 2 semiconductor names.
Reported only; the frozen top 10 in metrics.csv stays the official shortlist."""
import csv, math, statistics as st, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import screen as s
HERE = Path(__file__).parent
SEMIS = {"NVDA", "MU", "AMD", "SMH", "SOXX", "INTC", "AVGO"}
rows = list(csv.DictReader(open(HERE / "metrics.csv")))
out = []
for r in rows:
    b = s.load_ohlc(r["ticker"]); C = [x[4] for x in b]
    lr = [math.nan] + [math.log(C[i] / C[i-1]) for i in range(1, len(C))]
    pay = []
    for t in range(60, len(C) - 21):
        s10 = st.stdev(lr[t-59:t+1]) * math.sqrt(10)
        pay.append(max(abs(math.log(C[t+10] / C[t])) / s10 - 1, 0))
    out.append((r["ticker"], int(r["rank"]), st.mean(pay)))
pr = sorted(out, key=lambda x: -x[2])
with open(HERE / "trial2_payoff10.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["payoff_rank", "ticker", "frozen_rank", "payoff10", "vs_normal_null"])
    for i, (t, fr, p) in enumerate(pr, 1): w.writerow([i, t, fr, f"{p:.4f}", f"{p/0.1666:.2f}"])
capped, n_semi = [], 0
for r in rows:
    if r["ticker"] in SEMIS:
        if n_semi == 2: continue
        n_semi += 1
    capped.append(r["ticker"])
print("trial2 payoff10 (top 12):", [(t, fr, round(p, 3)) for t, fr, p in pr[:12]])
print("trial2 above normal null:", sum(p > 0.1666 for _, _, p in out), "of", len(out))
print("trial3 sector-capped top10:", capped[:10])
