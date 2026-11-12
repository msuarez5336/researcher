# Backtest specification: buying 1–6 month single-stock options

As of 2026-11-12. Built from `report.md` and the recipe tables in `notes/SQ3.md`, `notes/SQ4.md`
and `notes/SQ9.md`. Evidence ids point to `evidence/*.jsonl`. Where the research found no
basis for a choice, the line says **assumption** and the choice is mine, to be revisited.

## 1. What the test must answer

For each candidate condition: when the condition holds, does buying a 1–6 month call (or put)
on that stock earn more than buying the same kind of option with no condition, after realistic
entry and exit prices, on data the condition was not tuned on?

The comparison is always against the unconditional baseline (section 6), not against zero.
Published work gives almost no direct answer for this maturity range (report, finding 1).

## 2. Data layers

| Layer | Needed fields | Source found | Cost seen 2026-11-12 | Gap |
|---|---|---|---|---|
| Option chains, end of day | date, underlying, expiry, strike, call/put, bid, ask, implied volatility, delta, open interest, volume | ORATS 2007– (`SQ5-3`); iVolatility 2005– (`SQ5-6`); FirstRate 2010– (`SQ5-1`); Cboe 2012– (`SQ5-9`) | ORATS $599 one-time, individual licence (`SQ5-4`) | Delisted coverage not stated for ORATS; snapshot is 14 minutes before the close |
| Share prices | date, open/high/low/close, split and dividend adjustments, delisted companies included | Norgate top tiers (`SQ6-15`); Sharadar 1998– (`SQ6-11`) | not retrieved | ORATS does not supply share prices; free feeds reported to omit delisted names |
| Company identifier | an id stable across ticker changes | SEC CIK via EDGAR | free | Mapping between vendors' ids not researched |
| Earnings dates | announcement date, before-open or after-close flag | EDGAR 8-K filing times; some paid APIs carry the flag (`SQ6-18`) | free / varies | No source of the date as originally scheduled |
| Short interest | measurement date, shares short, publication date | FINRA, twice monthly (`SQ6-1`) | free | — |
| Insider transactions | filing date, buyer role, shares, price | SEC EDGAR data sets 2006– (`SQ6-8`) | free | — |
| Index membership by date | index, constituent, start, end | Norgate top tiers (`SQ6-15`) | paid | Free history is a reconstruction (`SQ6-16`) |
| Interest rate | daily short-term rate | FRED DTB3 (`SQ6-17`) | free | — |
| Analyst estimates | estimate, analyst, original date | not sourced | — | Main academic database reported to change between downloads (`SQ6-7`, unverified); defer |

Every row is stored with the date on which it became public. A value is usable in a signal
only from that date: short interest from the 7th business day after its measurement date
(`SQ6-2`); insider data from the filing date; earnings from the announcement date.

**Minimum viable set:** one option-chain history, delisting-inclusive share prices, FINRA short
interest, EDGAR earnings and insider dates, FRED rates. Analyst data is left out of version one.

## 3. Real versus estimated option prices

| Use | Real quotes needed? | Why |
|---|---|---|
| Any condition computed from option prices (section 4, group A) | Yes | The condition does not exist without the quotes |
| Entry and exit prices for the final test of any condition | Yes | No study was found measuring the error of estimated prices (report, finding 8) |
| First-pass screening of stock-side conditions (group B) | No | Estimated prices can rank conditions before data is bought |

Estimation method for first-pass screening (**assumption**; no accuracy evidence found):
1. Price with a standard option model using the stock's realised volatility over the prior
   60 trading days, measured only up to the entry date.
2. Add a fixed mark-up to that volatility. Realised volatility used alone probably underprices
   options on average; the supporting source was seen only in a snippet (`SQ5-16`, unverified).
3. Never use volatility measured over the option's own life: that is information from the
   future (`SQ5-18`).

Known blind spots of estimated prices: the higher implied volatility of out-of-the-money
strikes, the premium before earnings, the rise in implied volatility after a share-price fall,
and bid-ask spreads. The last three bear directly on the rebound-after-a-fall setup, so a
favourable first-pass result for it is weak evidence until repeated on real quotes.

**Calibration step once real data is bought:** for a sample of contracts, compare the estimated
price with the real mid-quote by maturity, strike distance and recent share return, and record
the error. This fills the gap the research could not.

## 4. Signal catalogue

**Group A: needs real option data**

| # | Signal | How to compute | Rule in the source | Evidence | Confidence in recipe |
|---|---|---|---|---|---|
| A1 | Implied volatility against own history | At-the-money implied volatility today minus its 12-month average; the source also uses the 12-month average of realised volatility and the cross-sectional average in a monthly regression | Tenths, monthly; buy the tenth with the largest predicted rise | `SQ10-2`–`SQ10-6` | Read in a 2005 working paper; published version not read |
| A2 | Realised minus implied volatility | Past realised volatility minus at-the-money implied volatility | Tenths | `SQ9-15` | Abstract only; lookback not stated |
| A3 | Implied volatility level | At-the-money implied volatility | Low favours holding options | `SQ9-4` | Direction read; tested hedged |
| A4 | Slope across expiry dates | Longer-dated minus shorter-dated implied volatility | High slope | `SQ9-14` | Abstract only; disputed |
| A5 | Past straddle return | Average monthly straddle return over the prior 1–12 months | Fifths | `SQ9-12`, recipe in `notes/SQ3.md` | Read in original |
| A6 | Option-to-share volume ratio | Option volume divided by share volume | Tenths, weekly; predicts share returns | `SQ4-6` | Formula detail not read |

**Group B: computable without option data**

| # | Signal | How to compute | Rule in the source | Evidence | Confidence in recipe |
|---|---|---|---|---|---|
| B1 | Sharp one-day fall | Close-to-close fall of 10% or more | Event | `SQ3-10` | Read in original; tested on shares over two days only |
| B2 | Past one-month return | Prior month's share return | Tenths | `SQ3-5`, `SQ3-6` | Read; tested hedged |
| B3 | Past 2–12 month return | Cumulative return over 11 months, skipping the latest | Tenths | `SQ3-6` | Read; tested hedged |
| B4 | Distance from 52-week high or low | Price relative to the 52-week extreme | Not stated | `SQ3-9` | Abstract only |
| B5 | Short interest | Shares short over shares outstanding, lagged to publication | Not researched | `SQ6-1`, `SQ6-2` (data only) | No predictive evidence collected |
| B6 | Insider buying | Net insider purchases in a trailing window, by filing date | Not researched | `SQ6-8` (data only) | No predictive evidence collected |
| B7 | Days to next earnings date | Calendar distance at entry | Control variable | `SQ4-1` | Scheduled date not available historically |

B5 and B6 are in the catalogue because the data is free and dated; the research collected no
evidence that they predict anything. Treat them as untested ideas.

## 5. Simulator rules

| Rule | Setting | Basis |
|---|---|---|
| Universe | Optionable US common stocks above a size or option-volume floor, including later-delisted ones | **assumption**; studies filter on share price ≥ $5, option bid > 0, mid ≥ $0.125 (`notes/SQ9.md`) |
| Signal date | Use only rows public by the close of that day | section 2 |
| Entry | Next trading day's quotes | **assumption**, avoids trading on the snapshot that produced the signal; one study found a one-day lag changes results little (`SQ10` source) |
| Contract choice | By target delta and days to expiry, nearest listed contract; test grid: delta 0.50, 0.35, 0.20 × 30–60, 61–120, 121–180 days | **assumption**; the grid mirrors the strike and maturity groups in `SQ8-1`, `SQ8-6` |
| Entry price | Mid plus 75% of half the quoted spread as the main case; also report at mid, at 50% and at the ask | 53% (timed trades, heavily traded options on 39 stocks) to about 75% (conventional measure): `SQ8-9`, `SQ8-10`, `SQ10-5`, `SQ7-6` |
| Exit price | Mid minus 75% of half the spread; intrinsic value if held to expiry | same |
| Exit rule | Report three variants: hold to expiry; fixed holding period of half the days to expiry; exit at a fixed multiple of the premium | **assumption** |
| Liquidity filter | Skip contracts with quoted spread above 50% of mid or zero open interest | filters used in `notes/SQ9.md`, `notes/SQ3.md` |
| Corporate actions | Adjust strikes and share counts for splits; a delisted or acquired stock settles at the last available value | **assumption**; sizes of these errors not found |
| Early exercise | Ignore for bought calls on non-dividend dates; flag contracts spanning an ex-dividend date | **assumption**; studies exclude them (`notes/SQ9.md`) |
| Position size | Equal premium per trade | **assumption**; sizing research not found |

## 6. Test plan

1. **Baseline first.** Unconditional return of each cell in the delta × maturity grid, at mid,
   at 50% and 75% of the spread, and at the ask. Compare with the published figures in the report
   (finding 2) as a check that the simulator is sane on the overlapping years and maturities.
2. **One condition at a time.** For each signal, the difference between trades where it holds
   and the baseline cell, with the whole distribution: mean, median, share of total losses,
   share of trades above 2×, 5× and 10× premium.
3. **Hold back data.** Tune nothing on the final third of the history; run it once at the end.
4. **Count independent periods honestly.** A 3-month hold sampled monthly overlaps; divide the
   t-statistic by the square root of the horizon in sampling periods (`SQ7-9`).
5. **Raise the bar for many trials.** Require a t-statistic above 3.0 before overlap adjustment
   as a first filter (`SQ7-7`, derived for share-market factors), and record how many
   conditions and variants were tried.
6. **Check where it comes from.** Split results by year, by size group and by whether an
   earnings date fell inside the holding period. An effect present in one period only is
   treated as not found.
7. **Combine last.** Only conditions that pass alone are combined.

Suggested order: baseline; A1 and A3 (best supported); B1 (the setup that prompted this work);
then the rest.

## 7. What this specification cannot settle

- Whether any of this is profitable: the research found no direct evidence either way.
- The right statistical treatment for payoffs that are mostly total losses with rare large
  wins: not found. Reporting the full distribution (step 2) is a stopgap.
- Vendor data quality: all coverage claims are the vendors' own.
- Costs after 2007: no measured spread data for recent years was read; the simulator uses the
  quotes in the purchased data, so this resolves itself once data is in hand.
