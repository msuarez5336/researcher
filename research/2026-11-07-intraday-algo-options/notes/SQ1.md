# SQ1 notes (as of 2026-11-07)

## Answer
Best-supported underlying signal is Gao et al. first-half-hour momentum, but it predicts only the last half-hour with R2 about 0.02 (SPY, sample ends 2012-2013), and no study shows a net-of-cost, out-of-sample edge. Opening-range breakout (ORB) and the SPY noise-area strategy show large backtest numbers (in-sample, mostly working papers). An independent 2026 replication finds gross reproduces but net of spread and slippage is about zero. Gap direction is not predictive on average. No evidence found for macro-event or earnings-open signals.

## Findings
- [E] First half-hour (from previous close) predicts last half-hour; stronger on high-vol, high-volume, recession and macro-news days; ten other ETFs too (SQ1-1). Sample 1993-2013.
- [E] SPY OOS R2 0.018; timing rule (long SPY if first half-hour is positive, else cash) 6.3% vs -0.5% gross per year, 1999-2012 (SQ1-2). R2 rises to 0.048 when first-half-hour vol is high (SQ1-3). Fires 1x/day, horizon 30 min (last half-hour), exit at close. Costs not included.
- [E] 5-min ORB on QQQ: 33.2% vs 14.9% CAGR, 2016-2023, zero slippage, 4x leverage (SQ1-4). Exit: stop at opposite end of first bar, or 4PM close (target 10R in the replicator's description, SQ1-7). Fires 1x/day. No OOS.
- [E] Replication on index CFDs 2015-2026: gross +0.131 R matches; net about 0 R (NQ +0.002 R), 4 of 5 negative; edge vs random direction +0.10 to +0.13 R (SQ1-5, SQ1-6). OOS 2021-2026 at most +0.06 R on NQ. Blog, not peer-reviewed.
- [E] Stocks-in-play ORB on 7,000+ stocks 2016-2023: Sharpe 2.81 net of costs for top-20 portfolio (SQ1-8). Filters by abnormal activity or news, so relevant to single-stock choice, but this is a many-position portfolio and in-sample.
- [E] SPY noise-area intraday momentum 2007-2024: 19.6% net per year, Sharpe 1.33, VWAP/noise trailing stop, flat at close (SQ1-9). Entries can be re-checked every 30 min, so it may fire more than 1-2 times a day. In-sample.
- [E] Gap: correlation 0.01 between gap and open-to-close return, SPY 1993-2025 (SQ1-10). Neither fade nor continuation works unconditionally.
- [E] QuantConnect replication of Gao et al. 2015-2020 had a Sharpe below the benchmark (SQ1-11).

## Conflicts
- ORB paper (33% per year) vs replication (net about 0). It holds or fails mainly on the cost assumption (none vs fixed point costs) and sample (2016-2023 vs 2015-2026 incl. negative 2015-2017). The replication is a blog; the original is an SSRN preprint. Neither is peer-reviewed.
- Gao et al.: significant OOS in the paper, but the QuantConnect 2015-2020 replication is weak. Different trading rule, so not a direct contradiction.

## Not found
- Peer-reviewed or independent OOS test of ORB on SPY/QQQ with spread costs.
- Post-2020 test of the Gao predictor with a clean trading rule.
- Underlying-move studies for CPI/jobs releases and earnings opens. FOMC search gave only pre-FOMC drift (Lucca-Moench, via search summary, not cached) and a Fordham thesis. Not extracted.
- VWAP-reversion entry and time-of-day studies: not searched (budget).
- The Gao PDF (www3.nd.edu) returned unsupported, so I used the RePEc abstract. The SSRN Zarattini-Aziz paper was not fetched (SSRN blocked). SQ1-4 quote is verified against the cached CXO summary only, so the paper itself is unverified.

## Blocked
- papers.ssrn.com (per brief, not attempted). www3.nd.edu PDF unsupported by fetch_page.py.

## Search log
1. ORB QQQ Zarattini Aziz (search): 6 new sources.
2. first half-hour predicts last, replication (search): 4.
3. ORB fails after costs (disconfirm): 2 (mql5 replication, critique).
4. Cache fetch of 5 pages (mql5, unisg, repec, cxo): ok; nd.edu PDF unsupported.
5. Overnight gap fade/continuation (search): 1 (CXO gap).
6. FOMC drift (search): 0 usable.
7. Noise area SPY (search): 1. 8. Gao abstract (search): 1 (RePEc). 9. Post-2020 decay (search): 1 (QuantConnect).
10. Cache fetch of 5 more pages and grep: ok. Total 12 of 15 calls used.

## Table
signal | fires when | per day | horizon | instrument | sample | effect size | exit used | costs? | OOS? | grade | source id
First half-hour momentum | 9:30-10:00 return (vs prior close) sets direction | 1 | last half-hour (15:30-16:00) | SPY | 1993-2013 / 1999-2012 | OOS R2 0.018; 6.3% vs -0.5% gross/yr | close | no | yes (paper) | A/C | SQ1-1, SQ1-2, SQ1-3
5-min ORB | enter at 9:35 in direction of first bar | 1 | intraday to close | QQQ | 2016-2023 | 33.2% vs 14.9% CAGR, 4x lev | stop at opposite end of bar; 4PM close | commission only | no | C (SSRN, unverified) | SQ1-4
5-min ORB replication | same | 1 | intraday | NQ/SPX/Dow/DAX/FTSE CFDs | 2015-2026 | gross +0.131 R, net +0.002 R (NQ) | stop at bar end; 10R target or close | yes (fixed points) | partial 2021-26 | C | SQ1-5, SQ1-6, SQ1-7
Stocks-in-play ORB | abnormal-volume stocks, 5-min range break | many (top-20 portfolio) | intraday | 7,000+ US stocks | 2016-2023 | Sharpe 2.81, net total over 1,600% | stop/EOD | yes | no | B | SQ1-8
Noise-area momentum | break of 14-day avg-move band, checked every 30 min | 1+ | intraday | SPY | 2007-2024 | 19.6%/yr, Sharpe 1.33 | VWAP/band trailing stop; flat at close | yes | no | B | SQ1-9
Overnight gap | gap at open | 1 | open-to-close | SPY | 1993-2025 | corr 0.01 (no edge) | n/a | n/a | n/a | C | SQ1-10
