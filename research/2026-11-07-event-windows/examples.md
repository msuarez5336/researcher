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

## 6. H-MOM1 on one ticker: AAPL, 11 June 2024 (real prices, modelled option)

Prices are Nasdaq daily data. Implied vol is Cboe VXAPL × VIX9D/VIX. The option is priced with
Black-Scholes, so it is not a real fill. Costs are k = 0.70 plus $0.70 per contract.

| Check at the 11 June close | Value | Rule | Pass? |
|---|---|---|---|
| Move | 193.12 → 207.15, +7.3% | — | — |
| Size vs AAPL's own 60-day daily σ (1.52%) | **4.6σ** | ≥ 2.5σ | ✓ |
| Earnings that day or the day before | none (it was WWDC week) | none | ✓ |
| Stock-specific? SPY that day | +0.24% = 0.35σ | \|SPY\| < 1σ | ✓ |
| Volume vs 20-day average | 172M = **3.2×** | ≥ 2× | ✓ |
| Close location in the day's range | **1.00** (closed at the high) | ≥ 0.8 for an up move | ✓ |
| VIX vs its trailing year | 12.85, below the 13.45 low-tercile cut | not top tercile | ✓ |

**Trade:** buy an ATM call, 14 DTE, at the close. Model price $3.82 (IV 23.6%), so you pay
$385 per contract with costs. **Sell at the next close** (12 June: 213.07, IV 22.3%). The model
value is $7.21, so you receive $716. **P&L +$331, +86%.** The same call bought on a random day and
held one day averaged +0.4% in 2021–26.

Holding longer (for comparison only): +102% on day 2, +59% on day 3, +154% on day 4, +96% on day 5.
In this case holding paid, but on average it didn't.

**The same rule, other outcomes** (model prices, proxy IV):

| Ticker / date | Move | Next-close P&L | If held 3 days |
|---|---|---|---|
| MSFT 2026-05-29 (call) | +5.5%, 3.1σ, 2.3× volume | **+62%** | −89% (the move reversed) |
| PLTR 2025-08-19 (put) | −9.4%, 3.3σ, 2.2× volume | +4% | −27% |
| PFE 2025-09-12 (put) | −4.0%, 2.7σ, 2.2× volume | **−21%** | −41% |

27 events met all the H-MOM1 conditions in 2021-07 → 2026-11 across the 16 stocks, about 5 a
year. These examples aren't the test. H-MOM1 still needs its chain-data and forward test.
