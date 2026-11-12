# SQ4 notes (as of 2026-11-12)

## Answer
Scheduled earnings are not fully priced for very short straddles: 1996-2010 data show a gross +3.34% mean for ATM straddles bought 3 days before the announcement (SQ4-1). Net of half-spread costs it survives only for 4-10 day expiries and turns to loss as expiry lengthens (SQ4-2), so it does not transfer to 1-6 month options. Option-flow signals (O/S, put-call ratio) predict share returns, but the evidence is stock-side, mostly pre-2010, and the public-data version is weak or eaten by costs (SQ4-7 to SQ4-9). No study of buying 1-6 month options on a flow signal was found.

## Findings
- [E] Earnings straddle, 1996-2010 (ends before 2015): +3.34% gross, 3 days pre to announcement date (SQ4-1). Larger for small, volatile, thinly traded, high-cost stocks (SQ4-3).
- [E] Delta-neutral version: -0.19% daily, -17.1% monthly all-days; positive net only for 4-10 day expiry (1.64% daily net) (SQ4-2). HEDGED, not a buyer's return. Read via CXO summary.
- [E] Chung and Louis: pre-earnings straddles positive; bigger after low prior vol (SQ4-4). Full text not read.
- [E] ORATS self-reported: about +45% in 4 weeks to Feb 2026 versus about -2% over 12 quarters (SQ4-5). A single season shows regimes swing; it does not show a stable edge.
- [E] O/S ratio: 0.34%/week long-short on stocks (SQ4-6). Pan-Poteshman put-call ratio: >40bp next day, >1% next week using proprietary data (SQ4-7); source is non-public information (SQ4-8).
- [E] Baltussen et al: public option metrics gross 9.9% a year, costs wipe it out except the top 100 stocks (net 2.4%, ignoring shorting cost) (SQ4-9).
- [E] Peer news: options reprice peers' implied vol on first-announcer earnings (SQ4-10). This shows pricing happens, not mispricing. No return test found.
- [E] Gamma: Barbon-Buraschi (secondary) finds dealer gamma imbalance linked to lower absolute stock returns (SQ4-12); OptionMetrics finds an index effect only in low-VIX regimes (SQ4-13). Both are about volatility, not a return to option buyers. [O] FlashAlpha SPY backtest says GEX mostly tracks VIX (page cached, not recorded: vendor, index).

## Conflicts
- Gao et al/Chung-Louis (pre-earnings straddle positive) versus the half-spread cost result (SQ4-2) and the MDPI/Govindaraj results (abstracts seen only via search snippets, not recorded): MDPI says gaps between past earnings moves and implied moves predict returns; Govindaraj reportedly finds negative net returns related to implied vol after costs. Positive holds gross, in short expiries, small/illiquid names; negative holds net, in long expiries.
- Pan-Poteshman: signal valid with proprietary signed volume; public-only components reportedly last 1-2 days (search summary only).
- Baltussen: gross profitable, net near zero except the largest stocks.
- Ex-US O/S results are mixed (search summary, unverified).

## Not found / not searched
- Returns to buying 1-6 month options (unhedged) around earnings: not found. Every earnings result is a short-dated straddle.
- Peer or supplier read-across measured in option returns: not found.
- Gamma tied to a return to option buyers: not found.
- Other dated events (FDA, M&A, index additions, spin-offs): not searched.
- Post-2015 out-of-sample test of O/S or put-call signals: not found.
- Full texts of Chung-Louis, Johnson-So, Pan-Poteshman, Baltussen not read, so sample periods, universe filters and strike rules are mostly "not stated".

## Blocked
mdpi.com (403), core.ac.uk (403), link.springer.com (429); PDFs from wallstreethorizon.com, KIT, nber.org/papers/w19590.pdf unsupported by fetch_page. Govindaraj SSRN and MDPI claims therefore not recorded.

## Table: event or flow condition
| condition | what bought and when | measured return | sample | public data then? | costs? | id |
|---|---|---|---|---|---|---|
| Earnings, 3d before to announcement | ATM straddle, unhedged, <=60d expiry (per CXO) | +3.34% mean gross | 1996-2010 | yes (OptionMetrics-type EOD) | no | SQ4-1 |
| Earnings, same, delta-neutral | 4-10d expiry straddle, held to expiry | +1.64%/day net; loss at longer expiry | 1996-2010 | yes | half spread; loss at full spread | SQ4-2 |
| Earnings, 4 weeks to Feb 2026 | straddle, details not stated | about +45% (12-qtr avg about -2%) | 2026 / prior 12 qtrs | yes | not stated | SQ4-5 |
| Low O/S ratio | stock long/short, no options | 0.34%/wk spread | not stated | yes (volume) | not stated | SQ4-6 |
| Low put-call ratio (buyer-initiated open) | stock long/short | >40bp next day, >1% next week | about 1990-2001 | no (proprietary) | no | SQ4-7 |
| Four public option metrics | stock long/short, weekly | 9.9% gross; 2.4% net (top 100) | 1996-2009 | yes, 1-day lag | yes, 0.07% one way, no shorting cost | SQ4-9 |
| Peer earnings | none (IV only) | n/a | not stated | yes | n/a | SQ4-10 |
| Dealer gamma | none (volatility) | n/a | 1996-2017 / 2026 | inferred | n/a | SQ4-12, 13 |

## Recipe table
| signal | formula | rule | inputs/lookback | public delay | stocks | option choice | holding | prices in/out | fields | real option data? | id |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Pre-earnings straddle (Gao, Xing, Zhang) | call+put, same strike/expiry; delta-neutral weights also tested | buy at close 3 (or 1, 5) trading days before scheduled date | earnings dates | date known in advance | not stated (price/size filters not stated); option mid at least $0.125 | moneyness 0.95-1.05, <=60d expiry; best net 4-10d | to announcement day or day after; or to expiry | close bid-ask midpoint | option bid/ask, delta, earnings date | yes | SQ4-1, 2 |
| O/S (Johnson-So) | option volume / stock volume (formula detail not stated here) | lowest vs highest decile | not stated | not stated | not stated | n/a (stock) | weekly returns | not stated | option and stock volume | yes (volume only) | SQ4-6 |
| Put-call ratio (Pan-Poteshman) | puts/calls from buyer-initiated open volume | low vs high | not stated | not public | not stated | n/a | 1 day to 1 week | not stated | signed open-buy volume | yes, non-public | SQ4-7 |
| Four option metrics (Baltussen) | not stated | weekly quintiles on Tuesday close, normalised average | not stated | 1-day lag | 1,250 largest, top 100 | ATM 0.95-1.05, OTM 0.80-0.95 strikes feed metrics | weekly | Wednesday close | option vol, OI, IV | yes | SQ4-9 |
| Peer IV transfer | change in IV, first announcer vs peers | not stated | not stated | same day | not stated | long-duration stronger | n/a | n/a | IV | yes | SQ4-10 |
| Dealer gamma | not stated | not stated | not stated | not stated | not stated | not stated | not stated | not stated | not stated | yes | SQ4-12 |

## Search log
1 straddle earnings (search, ~9 sources); 2 O/S ratio (search, ~6); 3 flow publicly available (disconfirm, ~4); 4 Goyal-Saretto earnings (search, 2); fetch batches 1-3 for caching; 5 Pan-Poteshman (search, 1 new); 6 peer IV (search, 2 new); 7 dealer gamma (search, 4); 8 costs/decay (disconfirm, 3). Used 20 of 20.
