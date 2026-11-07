# Practical examples: using the opportunity calendar

As of 2026-11-07. Earnings are excluded throughout. These examples show how to *watch for* and
*test* the windows. None of them is a validated trade.

## 1. Rerun the study

```bash
python3 research/2026-11-07-event-windows/study/events.py --selftest
```

```bash
python3 research/2026-11-07-event-windows/study/events.py
```

The full run takes about 30 minutes, mostly earnings-exclusion lookups, which are cached after the
first run. Results land in `study/results.csv` (one row per cell) and `study/events.csv` (every
event).

## 2. A daily watchlist check (what to look at each close)

| Check at the close | Source | If true |
|---|---|---|
| Did any shortlist stock move > 2.5× its 60-day daily σ, with no earnings today or yesterday? | Nasdaq daily data + earnings calendar | Candidate for **H-C2m**. Check VIX's tercile next. |
| Is VIX in its middle tercile (roughly 15–20 recently)? | Cboe VIX | H-C2m entry condition |
| Is tomorrow an FOMC statement day? | federalreserve.gov calendar | **H-FOMC** straddle, test only |
| Did SPY move > 1.5σ on an FOMC day? | prices | **H-FOMC** reversal, 3-day test |
| Did SPY/QQQ/IWM move > 2.5σ? | prices | **Don't** buy the bounce: −21 pts against random days in our data |
| Did VIX jump ≥ 30% in ≤ 3 days? | Cboe VIX | Expect IV to fall about 1.5 pts over 10 days. Use a spread, not a single leg. |

## 3. Worked example: an H-C2m candidate (illustrative numbers)

MU falls 7.8% on a non-earnings day (a sector downgrade). Its 60-day daily σ is 2.9%, so the move is
2.7σ, which passes. MU didn't report earnings today or yesterday. VIX closes at 17.2, in the middle
tercile.

1. **Structure:** reversal side = calls. 45-DTE 0.50Δ / 0.25Δ call debit spread at the close.
2. **Pricing check:** the post-shock IV on the chain is 58%. Expect it to drift about 1–2 points
   lower over 10 days, which costs the long leg more than the short. The spread keeps the vega hit small.
3. **Exits:** day 10; or +50% of max spread value; or a close below the shock-day low (thesis broken).
4. **Log it** as an H-C2m trial with entry IV, spread width, fills at k = 0.70, and the exit reason.
   Paper-trade until the chain-data backtest passes.

## 4. Brief for the confirmation backtest (paste to a coding agent)

```text
OBJECTIVE
Confirm or reject hypothesis H-C2m from research/2026-11-07-event-windows/report.md using ORATS
chain data (real IV, skew, bid/ask), 2016-11 -> 2026-11.

FIXED
- Trigger: |r_t| > 2.5 * stdev(r over t-60..t-1); no earnings on t or t-1; VIX_t in the middle
  tercile of its trailing 10 years. One event per ticker per 10 trading days.
- Universe: NVDA TSLA MU AAPL INTC AMD AMZN META PLTR GOOGL MSFT AVGO ORCL HOOD PFE SOFI (the 16 stocks studied).
- Structure: reversal-side 0.50/0.25 delta debit spread, 35-60 DTE (nearest 45), at the close snapshot.
- Fills: per leg at k=0.70 and k=1.0 (v2 spec). Exits: day 10 / +50% of max / close beyond shock extreme.
- Control: the same spread on random days with the same side mix.
- Trial count starts at 349 (348 already used). Report it with the result.

PASS IF (out of sample 2021-07 -> 2026-11, k=1.0)
- mean excess over control >= +10 pts with t >= 2, same sign in-sample, n >= 50, and v2 gates pass.

OUTPUT
results/H-C2m/{trades.csv, summary.md}. Reply with the path and a 200-word summary.
```

## 5. Reading a calendar row

"**Watch**" means a positive result in one half of the data only, or t < 2. Don't trade it, and
don't count it as evidence. Re-test it when the regime it depends on returns (e.g. FOMC in an
active hiking cycle). "**Avoid**" means significantly worse than random entries out of sample.
"**No edge**" means indistinguishable from random entries.
