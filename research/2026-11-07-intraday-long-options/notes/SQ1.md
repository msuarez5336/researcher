# SQ1 notes (as of 2026-11-07). Budget used: 12 of 15 calls.

*Answer:* Only two windows have peer-reviewed predictive evidence: first-to-last half-hour momentum (R2 about 0.01-0.02; gross, no costs; weak or absent out of sample in 2012-14 and in Rosa's overnight variant) and the overnight/intraday split. Opening-range breakout looks strong in a self-published paper with zero spread and slippage, but an independent 2026 replication nets about zero. I found no rigorous test of gap-fill vs gap-and-go, midday lull, or MOC imbalances as same-day signals.

## 1. Window table
| Window | Mechanism | Best evidence | Sample | Effect size | Costs? | Persistence | Self-reported? |
|---|---|---|---|---|---|---|---|
| Open ORB (5 min) | Stocks in play, news-driven order flow | Zarattini-Barbon-Aziz 2024 (E6, E7) | 2016-2023; 7,000 stocks; QQQ 2016-23 | Top-20 SiP Sharpe 2.81, alpha 36%; QQQ 33.2% vs 14.9% CAGR | Stocks: commission, per abstract; QQQ: commission only, no spread/slippage | Replication 2015-26: out-of-sample 2021-26 +0.06 R NQ at best net (E8, E9) | Yes (working paper by practitioners, B) |
| Gap days | Not found academically | Practitioner write-ups only; unfetched, unrecorded | | | | | Yes |
| First to last half-hour | Rebalancing, late informed trading, gamma hedging | Gao et al JFE 2018 (E1); Baltussen JFE 2021 (E5) | SPY 1993-2013; 60+ futures 1974-2020 | R2 about 0.02; 6.3% vs -0.5% gross annual (E2) | No | Aug 2012-May 2014 corr 0.12, R2 0.014, edge in extremes only (E3); Rosa 2022 overnight variant vanishes out of sample (E4) | No (peer-reviewed); E2/E3 are CXO summaries |
| Midday lull | Not found | Heston et al 2010 is cross-sectional, not a midday result (E11) | | | | | |
| Last hour / MOC | Imbalances, floor brokers | Only search snippets: Morand thesis; "Vestigial Tails?" (NYSE closing auction reversals, 2011-18); a JOF closing-imbalance paper (positive imbalance goes with positive overnight, negative intraday). PDFs unreachable, so unverified, no ids | | | | | |
| Overnight vs intraday | Clienteles; news | Lou-Polk-Skouras 2019 (E10); Glasserman 2025 (E12) | 30 years | Momentum/reversal profits sit entirely in one component with opposite signs | No | n/a | No |

The overnight vs intraday split of the prior run's 2021-26 next-day continuation was not found. Lou et al imply that past intraday returns continue overnight and past overnight returns reverse intraday. This is [O] from a search snippet, unverified.

## 2. Trigger definitions (codable from 5-minute or hourly bars)
- ORB: range = high/low of first 5-min bar (9:30-9:35). Enter long at the open of 9:35 bar if bar close > open, short if below, skip dojis. Stop at the other side of the bar. Exit at 16:00 or target. Stocks in play: relative volume over the prior 14 days at 9:35, top 20 per day, price > $5, ADV > 1M shares. Per the replication blog, R-multiples are used and the stop/target in the replication is a 10R target. Only the replication's description was seen, not the paper. (E8)
- Intraday momentum: r1 = ln(P at 10:00 / previous close), which includes the overnight gap. Take the last half-hour (15:30-16:00) in the direction of r1. A filter on |r1| above a threshold helps (Rosa; E3, E4). Hourly bars cannot resolve 15:30, so use the 15:00 hourly bar as a proxy only.
- Gap: gap = open / previous close - 1, scaled by ATR or stock daily range. Gap fill = traded back to previous close during the session. Define it from intraday bars, not daily highs and lows, which overstate fills.

## 3. Counter-evidence
- E3: weak correlation 0.12 in 2012-14, edge in extreme deciles only, below frictions.
- E4: Rosa, out-of-sample disappearance (overnight variant).
- E8/E9: the ORB edge is about the size of the spread on CFDs. The Zarattini QQQ test has zero slippage (E7). Replication used CFD, not options, and is a self-published blog.
- Gap fill, from a search summary of a tastylive digest, unverified: large gaps fill about 5% within a day; Bulkowski-based full-gap closure fell from 50% to 23%. Not recorded as evidence (page not cached).

## 4. Conflicts
ORB: paper (net Sharpe 2.81 on stocks in play, top 20) vs replication (about 0 net on indices CFDs). They differ in universe (single stocks vs index CFDs), costs, and period. For QQQ itself, the paper shows 33% CAGR with no spread. Intraday momentum: Gao (significant, 1993-2013) vs Rosa/CXO (weak or absent later).

## Not found
Primary evidence on gap-fill vs gap-and-go, midday lull volatility/range (U-shape only inferred), MOC imbalance effect sizes, overnight vs next-session split of continuation after large news moves, post-2020 persistence of Gao et al on SPY.

## Blocked
www1.villanova.edu (SSL error); PDFs unsupported by fetch_page: www3.nd.edu/~zda/intramom.pdf, personal.lse.ac.uk LouPolkSkouras.pdf, afajof.org, conference.nber.org. Full paper tables not read, only abstracts and secondary summaries.

## Search log
1. intraday momentum disappeared replication (disconfirm): 5 new sources. 2. Zarattini ORB (search): 4. 3. Gao et al (search): 2. 4. gap fill academic (search): 0 primary. 5. ORB out-of-sample decay (disconfirm): 2. 6. MOC imbalance (search): 3 snippets only. 7. overnight vs intraday news continuation (search): 3. Fetches: 12 cached pages.
