# Option setup grid search: finalists

Written by `node backtest/search.js report` from `results.csv`, `finalists.json`, `stress.json` and `holdout.json`. Grid fixed 2026-11-12; search period 20091001 to 20201231; holdout 20210101 onwards.

## The short answer

4 cell(s) passed all seven checks on the search period. Their holdout figures are in the table below. They are candidates for checking on real option prices, not evidence of profit.

## What was tried

- **14256 cells**: 264 setups (66 single conditions, and each of them combined with a calm market, a fearful market, or a market that fell 5% in a month) × 54 option choices (call or put; delta 0.5, 0.35, 0.2; 60, 90 or 180 days; held to expiry, sold at half-life, or sold on doubling).
- 14202 cells produced trades, 54 had no trades, 0 failed to run. No threshold had to be adjusted.
- **The bar**: a tAdj of **4.64** or more. tAdj measures how far the setup's average return sits above the ordinary-day average, in units of its own noise, after allowing for overlapping trades. A single test usually uses about 2; trying 14256 combinations needs 4.64 to keep the chance of even one lucky pass at about 5%.

## How many cleared each check

| Check | Cells passing |
|---|---|
| a. at least 300 trades over at least 60 months | 9126 |
| a and b. also tAdj ≥ 4.64 | 35 |
| a–c. also neighbouring thresholds agree (same sign, tAdj ≥ 2) | 33 |
| a–d. also positive in ≥ 70% of years, with ≥ 8 usable years | 33 |
| a–e. also positive with any one sector removed | 33 |
| a–g. also positive paying the whole spread, and with volatility +10 points at entry | 4 |
| Finalists kept (at most 10, at most 2 per setup) | 4 |

**Expected by chance.** If no setup had any real effect and the cells were independent, about 0.025 cells in total would clear the bar on the upside (0.05 counting both directions), so effectively none. 35 cleared it on the upside and 14 were as far below ordinary days as the bar is above.
For scale, with the usual single-test threshold of 2: 1888 of the 9126 cells that passed check a had tAdj ≥ 2 and 249 had tAdj ≤ −2; chance alone would give about 208 each way. The cells are far from independent (the same trades appear in many of them), so these counts are a rough guide only.

## Finalists

Each row pair is one finalist: search period first, holdout second. "Excess" is the setup's average return minus the ordinary-day average of the same calendar year. "Lost everything" is the share of trades that lost at least 99% of the premium.

| # | Setup | Option | Period | Trades | Average return | Ordinary-day average | Excess | tAdj | Lost everything |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 30% or more below its 52-week high | call, delta 0.35, 60 days, sold at double or held to expiry | search | 4506 | +29.8% | −10.6% | +43.2% | 5.50 | 44% |
| | | | holdout | 4482 | +19.4% | −5.5% | +29.7% | 3.70 | 49% |
| 2 | 40% or more below its 52-week high | call, delta 0.2, 60 days, sold at double or held to expiry | search | 1890 | +45.3% | −21.8% | +69.3% | 5.06 | 48% |
| | | | holdout | 2124 | +29.9% | −9.8% | +46.2% | 2.74 | 51% |
| 3 | 30% or more below its 52-week high | call, delta 0.35, 90 days, sold at double or held to expiry | search | 4512 | +29.8% | −12.7% | +44.8% | 4.74 | 42% |
| | | | holdout | 4395 | +13.8% | −8.8% | +27.8% | 2.71 | 50% |
| 4 | fell 15% or more in a month AND the market was fearful (VIX in the highest 33% of its past year) | call, delta 0.2, 90 days, sold at double or held to expiry | search | 1940 | +32.5% | −25.7% | +59.6% | 4.65 | 46% |
| | | | holdout | 1704 | +27.2% | −14.6% | +47.1% | 2.41 | 51% |

### Checks passed only narrowly

"Narrow" here means: fewer than 360 trades or 72 months; tAdj within 10% of the bar; a neighbour's tAdj under 2.5; positive years under 80% or only 8–9 usable years; or a stress test (sector removed, whole spread paid, volatility +10) that leaves less than half of the excess.

1. 30% or more below its 52-week high — call, delta 0.35, 60 days, sold at double or held to expiry: g (excess +4.9% with volatility +10 at entry).
2. 40% or more below its 52-week high — call, delta 0.2, 60 days, sold at double or held to expiry: b (tAdj 5.06); g (excess +17.6% with volatility +10 at entry).
3. 30% or more below its 52-week high — call, delta 0.35, 90 days, sold at double or held to expiry: b (tAdj 4.74); g (excess +6.1% with volatility +10 at entry).
4. fell 15% or more in a month AND the market was fearful (VIX in the highest 33% of its past year) — call, delta 0.2, 90 days, sold at double or held to expiry: b (tAdj 4.65); g (excess +2.6% with volatility +10 at entry).

33 cell(s) passed checks a–d and were put through e–g; 29 of them are not finalists (failed e–g or dropped by the per-setup cap). Details are in `stress.json`.

## Closest failures

The 5 cells that came closest: cells that passed a–d but failed a later check first, then cells with enough trades and a positive excess, ordered by how many of checks b, c, d they passed and then by tAdj (at most 2 per setup). Checks e–g were run for these too. All figures are from the search period.

| Setup | Option | Trades | Average return | Ordinary-day average | Excess | tAdj | Lost everything | Years positive | Excess, whole spread | Excess, volatility +10 | Worst excess with one sector removed | Checks failed |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 30% or more below its 52-week high | call, delta 0.2, 60 days, sold at double or held to expiry | 4471 | +26.8% | −21.8% | +51.1% | 6.66 | 53% | 12 of 12 | +50.8% | −5.4% | +48.9% (Health Care) | g |
| 20% or more below its 52-week high | call, delta 0.2, 60 days, sold at double or held to expiry | 10156 | +6.6% | −21.8% | +31.1% | 5.71 | 60% | 12 of 12 | +30.8% | −23.0% | +29.6% (Consumer Staples) | g |
| 12-month return (skipping the latest month) at least +80% | call, delta 0.2, 60 days, sold at double or held to expiry | 2630 | +21.0% | −21.8% | +41.7% | 5.62 | 54% | 12 of 12 | +41.7% | −20.0% | +38.8% (Consumer Discretionary) | g |
| 30% or more below its 52-week high | call, delta 0.2, 60 days, sold at half-life | 4471 | +27.8% | −15.1% | +45.0% | 5.42 | 8% | 12 of 12 | +44.1% | −13.7% | +42.0% (Industrials) | g |
| 20% or more below its 52-week high | call, delta 0.2, 60 days, sold at half-life | 10156 | +11.3% | −15.1% | +28.8% | 5.39 | 8% | 12 of 12 | +28.3% | −27.5% | +27.3% (Communication Services) | g |

Check letters: a enough trades and months; b tAdj at the bar; c neighbouring thresholds agree; d consistent across years; e survives removing any sector; f survives paying the whole spread; g survives higher volatility at entry.

Highest tAdj among cells with enough trades: 6.66 (30% or more below its 52-week high; call, delta 0.2, 60 days, sold at double or held to expiry). Lowest: −5.72 (within 1% of its 52-week high; call, delta 0.2, 60 days, sold at half-life).

## What this does and does not show

- **Option prices are estimates.** No real option quotes were used. Prices come from a formula fed with a volatility estimated from each stock's recent swings and the VIX. A result here ranks ideas; it does not show what a real trade would have paid or returned.
- **The stocks are survivors and recent winners.** The 200 stocks are 2026 S&P 500 members chosen by 2026 trading activity. Companies that failed or shrank are missing, which flatters calls.
- **No earnings dates.** Real options cost more ahead of earnings; the estimate does not know when earnings fall.
- **After sharp falls the estimate is too cheap.** Real option prices jump faster than the estimate, which flatters fall-and-rebound setups. Check g probes this but does not correct it.
- **The holdout is not perfectly fresh.** The owner has already looked at 2021–2026 on the page for the one-day-fall setup, so for that setup the holdout is not an untouched test.
- **Search-period trades run past the period's end.** A trade entered in late 2020 is closed in 2021, so the last few months of search-period trades use early-2021 prices. Holdout trades are separate trades entered from 2021.
- **Stress test g** raises volatility by 10 points at entry for the setup trades only; the ordinary-day trades keep the default estimate.
- A finalist is a candidate for checking on real option prices, not evidence of profit. "None found" means none met this standard on estimated prices, not that no setup can work. Nothing here is trading advice.
