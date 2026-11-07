# Practical examples: using the ticker screen and the strangle addendum

As of 2026-11-07. The numbers come from this run's screen on Nasdaq daily data and Cboe vol
indices, reproducible with the commands below. Example 3 uses made-up option quotes for the
arithmetic only.

## 1. Rerun or extend the screen

```bash
python3 research/2026-11-07-long-vol-tickers/screen/screen.py --selftest
```

```bash
python3 research/2026-11-07-long-vol-tickers/screen/screen.py --tickers research/2026-11-07-long-vol-tickers/notes/SQ3_candidates.txt --vol-indices VIX,VXN,RVX,VXAPL,VXAZN,VXGOG,VXGS,VXIBM,GVZ,OVX,VXEEM,VXSLV,VXEWZ,VXFXI,VXEFA
```

```bash
python3 research/2026-11-07-long-vol-tickers/screen/trial4_straddle_iv.py
```

To screen your own tickers, put one per line, most liquid first, in a text file and pass it as
`--tickers`. Any change to the metric definitions is a new trial: log it in `screen_spec.md`.

## 2. Put the 10 into the v2 backtest brief

In the builder brief from the previous run (`../2026-11-06-options-swing-backtest-spec/examples.md`,
Example 2), replace the universe line with:

```text
UNIVERSE
QQQ, AAPL, NVDA, MU, AMD, SMH, HOOD, TSLA, SOXX, SOFI
(research/2026-11-07-long-vol-tickers/screen/metrics.csv, frozen screen).
Portfolio rule: at most 2 open positions across {NVDA, MU, AMD, SMH, SOXX}.
HOOD: start 2021-09 (skip IPO month). SOFI: start 2021-07 (skip SPAC-merger period).
Run hypothesis S (long strangle, report.md "v2 spec addendum") with both controls:
random-date entries and trigger-only entries with no IV filter. Trial count starts at 5.
```

## 3. The strangle entry filter, worked through (illustrative quotes)

AAPL at $230. The 45-DTE chain (made-up numbers) shows:

| Leg | Δ | Bid | Ask |
|---|---|---|---|
| 245 call | 0.27 | 3.10 | 3.20 |
| 215 put | −0.27 | 3.40 | 3.55 |
| 230 call / 230 put (ATM, for the implied move) | 0.50 / −0.50 | 8.05 / 7.60 | 8.20 / 7.75 |

1. **Implied move:** ATM straddle mid = 8.125 + 7.675 = 15.80, or 6.9% of spot, over 45 days. Scaled to 10 trading days (≈14 calendar), 6.9% × √(14/45) ≈ 3.8%.
2. **Trailing realised 10-day move:** take the median |10-day return| over the last year. Suppose it is 4.3%.
3. **Filter:** 3.8% < 4.3% × 1.0, so the trade is allowed. At 4.6% implied it would be blocked.
4. **Cost at k = 0.70:**
   - Call: 3.10 + 0.7 × 0.10 = 3.17.
   - Put: 3.40 + 0.7 × 0.15 = 3.505.
   - Debit = 6.675 × 100 = $667.50, plus 2 legs × $0.70 = **$668.90** per strangle.
5. **Exits:**
   - Profit target +40%: the strangle's bid-side value reaches $936.
   - Stop −40%: value $401.
   - Time: day 10, or DTE < 21.
   - Event: the day before AAPL earnings, so pick an expiry window with no print inside the hold.

Why this filter and not "squeeze": trial 5 shows that buying when implied is below recent realised
cut losses on all 7 priced tickers, while squeeze-day entries were worse on 5 of 7. The filter
still didn't make the trade profitable at index-level implied vol. The backtest has to show it
does with real 0.27Δ quotes.

## 4. Reading the screen columns

| Column | Ask yourself | AAPL value | Read |
|---|---|---|---|
| `tail10` | How often did the 10-day close beat 1σ of recent vol? (Random walk ≈ 0.32–0.36) | 0.329 | Typical |
| `excur10` | The largest swing inside the 10 days, in σ units | 1.14 | Top quartile of the 24 |
| `expand` | Range lift after compression (random walk ≈ 1.9) | 1.45 | Below the null: compression doesn't predict expansion |
| `vrp` | How much implied vol beat what followed | +3.4 pts | Implied is usually rich |
| trial 4 | 10-day straddle at implied, gross | −7% (t −0.4) | The least negative of the 7 |

## 5. When to drop a ticker after the backtest

- Its strangle or long-option results fail the v2 gates at k = 1.0 out of sample, or
- it beats random-date entries only in-sample, or
- its average 0.27Δ spread breaches 8% of mid on more than 20% of entry days (liquidity drift: watch HOOD and SOFI).

## 6. Refresh later

```text
/research Re-rank the most liquid US option underlyings by 1-month ADV as of <date>, re-run
research/2026-11-07-long-vol-tickers/screen with the new list, and compare with metrics.csv.
```
