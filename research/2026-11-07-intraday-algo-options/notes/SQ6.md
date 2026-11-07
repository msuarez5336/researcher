# SQ6 notes: data and backtest method (as of 2026-11-07)

## Answer
Minute-level NBBO history is the practical minimum for backtesting intraday single-option buys. Cboe DataShop Option Intervals (1-minute NBBO, 2012 on) and ThetaData Standard/Pro (tick NBBO, 10-14 years, $80-160/month) cover this. Massive (ex-Polygon) needs the $199 Advanced plan for quotes, Databento's finest NBBO is 1-minute, and ORATS is end-of-day for history. Fill at or near the ask (or ~75% of the spread), reject stale or crossed quotes, and control overfitting with out-of-sample, walk-forward and deflated Sharpe.

## Findings
- [E] Cboe Option Intervals: 1-min or N-min NBBO+size+OHLC+volume, optional IV/Greeks, from Jan 2012 (SQ6-1, 2). Price not published; the cart is quote-based. Quote-size capture changed 2026-06-22 (SQ6-3). SPX underlying needs a $1k/month CGIF licence, SPY/QQQ do not (SQ6-4).
- [E] Cboe Option Trades: every print plus prevailing NBBO, optional per-trade Greeks (SQ6-5). EOD Summary has only 15:45 and close snapshots, so it is unusable for intraday entry (SQ6-6).
- [E] ThetaData individual plans: $40 / $80 / $160 per month; 1-minute only on Value, tick NBBO on Standard/Pro (SQ6-7). The history figure is 6/10/14 years on the pricing page today (SQ6-8). Gaps are documented, and 0DTE deep strikes lose quotes late in the day (SQ6-9, 10).
- [E] Polygon.io is now Massive. Options: $0 / $29 / $79 / $199 per month; quotes only on Advanced; 5+ years there (SQ6-11, 12).
- [E] ORATS: $199/month delayed API, with the Intraday Backtester API and Time & Sales API at +$299 each. History is EOD from 2007, with quotes taken 14 minutes before the close. No real stock prices (SQ6-13, 14, 15).
- [E] Databento OPRA: finest BBO schema cbbo-1m; usage-priced per GB; Standard live plan $199/month (SQ6-16, 17). cbbo-1m about $2/GB and history from Apr 2013 are unverified (SQ6-18).
- [O] ORATS: mid fills are "fantasy"; model single legs at 75% of the spread; closing prints are stale (SQ6-19, 20). Vendor rule of thumb, not measured here.
- [E, unverified] DSR and PBO (CSCV) are the standard overfitting controls (SQ6-21, 22).

## Conflicts
- ThetaData history: pricing page says 6/10/14 years; a search snippet and older marketing say 4/8/12. The pricing page is the one fetched today and is used here.
- Massive/Polygon price: aggregators cite $29/$79/$99/$199 and "custom". The fetched official page gives the figures above.
- Databento cbbo-1m price and 2013 start came from a search snippet only.

## Not found
- Cboe DataShop price (cart is dynamic, shows $0 until selection).
- Databento OPRA historical price page (JS-rendered, thin) and exact history start.
- Massive options history limit for Advanced beyond "5+ years". Massive licence terms for backtest use.
- Open-source framework primary pages: GitHub returned 403 to the cache script. Frameworks are listed from search results only (unverified).
- No independent measurement of mid-vs-ask fill bias; that belongs to SQ5. A dev.to practitioner claim of 30-60% CAGR overstatement was not cached, so it is not recorded.
- Vendor complaint searches: only anecdotal (Trustpilot, Reddit, Databento issue tracker, a Polygon incident Jul 2025). None cached.

## Blocked
- github.com (403 to fetch_page.py): optopsy, QuantConnect Lean, NautilusTrader.
- papers.ssrn.com (per brief). escholarship.org and ioandc.com PDFs: unsupported by the cache script.
- databento.com/pricing and thetadata.net/subscribe returned thin pages.

## Search log
1. Massive options pricing (search): 1 useful lead, 3 vendor pages cached.
2. ThetaData pricing (search): official pricing confirmed.
3. Databento OPRA pricing (search): cbbo-1m lead, unverified.
4. Cboe intervals (search): Option Intervals page found.
5. Open-source options backtest frameworks (search): backtrader, pinkfish, pybroker, mtrader; none options-specific.
6. Options backtest pitfalls (disconfirm: mid fills): ORATS blog.
7. DSR/PBO (search): SSRN and PDF leads, blocked.
8. Vendor data-quality complaints (disconfirm): ThetaData Data Issues doc, Databento tracker.

## Table 1: vendors
| vendor | granularity | history | price (as of 2026-11-07) | licence | grade | source id |
|---|---|---|---|---|---|---|
| Cboe DataShop Option Intervals / LiveVol | 1-min or N-min NBBO + OHLC, optional IV/Greeks | Jan 2012+ | not published (quote cart) | SPX underlying needs CGIF $1k/month+ | A | SQ6-1,2,4 |
| Cboe Option Trades | every trade + NBBO | Jan 2012+ | not published | same | A | SQ6-5 |
| ThetaData | Value 1-min; Standard/Pro tick NBBO + trades | 6/10/14 yrs | $40 / $80 / $160 per month | individual only | B | SQ6-7,8 |
| Massive (ex-Polygon) | minute/second aggs; trades from Developer; quotes Advanced | 2 / 4 / 5+ yrs | $0 / $29 / $79 / $199 per month | individual, non-pro | B | SQ6-11,12 |
| ORATS | EOD (14 min before close), hourly WHAM since 2022; Intraday add-ons | EOD from 2007 | $199/month + $299 add-ons | no stock prices | B | SQ6-13,14,15 |
| Databento OPRA | cbbo-1m NBBO | ~Apr 2013 (unverified) | usage per GB (~$2/GB cbbo-1m, unverified); live $199/month | per plan | B | SQ6-16,17,18 |

## Table 2: frameworks (from search results only; repo pages not cached)
| framework | options support | intraday | source id |
|---|---|---|---|
| backtrader https://github.com/mementum/backtrader | no native options; custom feed needed (unverified) | yes | none (search) |
| pinkfish https://github.com/fja05680/pinkfish | no | daily bars only | none (search) |
| pybroker https://github.com/edtechre/pybroker | no native options (unverified) | yes | none (search) |
| optopsy https://github.com/michaelchu/optopsy | options-specific, mostly EOD (unverified) | unknown | none |
| QuantConnect Lean https://github.com/QuantConnect/Lean | options supported (unverified, from memory) | yes | none |
| ORATS Intraday Backtester API (paid, not open source) | yes | yes | SQ6-13 |
Practical note: a custom pandas loop over vendor 1-minute NBBO may be simpler than adapting these.

## Table 3: pitfalls
| pitfall | effect on results | mitigation | source id |
|---|---|---|---|
| Fill at mid | overstates returns, especially for short-dated options | buy at ask, sell at bid; test 50%/75%/100% of spread | SQ6-19 |
| Closing/stale prints | prices not tradeable | use intraday NBBO; reject crossed, locked, zero-sided or stale quotes | SQ6-20 |
| Missing quote (deep 0DTE strikes late in day) | phantom fills or survivorship | treat missing as no fill; check strike existed that day | SQ6-9,10 |
| Spread ignored on stop exits | stops fill at bid, often wider than the model | model exit at bid plus slippage; delay by one bar | author's reasoning [O] |
| Look-ahead in IV/Greeks/GEX (EOD or 15:45 data used for morning entry) | inflated hit rate | use only values timestamped before the entry bar | SQ6-6, 20 |
| Vendor-changed definitions (Cboe size capture 2026-06-22) | structural break in size-based filters | check for vendor change notes | SQ6-3 |
| Multiple testing / overfitting | best of N rules looks good by chance | OOS holdout, walk-forward, deflated Sharpe, PBO | SQ6-21,22 (unverified) |
