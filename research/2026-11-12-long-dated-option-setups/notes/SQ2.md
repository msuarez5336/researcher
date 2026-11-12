# SQ2 notes (as of 2026-11-12)

## Answer
Published option-return signals are mostly tested on short-dated (about 1-2 month) ATM options, many of them hedged. The one on unhedged bought options I could read (Saretto 2005 WP, a precursor of Goyal-Saretto 2009) shows large gross straddle spreads when ATM IV is low versus its own 12-month IV/RV averages (sample 1996-Jun 2005, before 2015). The hypothesis "low IV vs recent RV means cheap options" is directionally supported. Delta-hedged evidence (vol-of-vol, idiosyncratic vol, term-structure slope) is not a buyer's return. I found no later-sample study read in full and no cost-inclusive replication I could verify.

## Findings
- [E] Low ATM IV vs cross-section and vs own 12m avg IV and RV predicts higher unhedged straddle returns; long-short 12.9%/month, top decile straddles +5.6%/month (SQ2-1). Costs: SQ2-2 says "after controlling for transaction costs" the straddle portfolio was up to 8.8%/month; method for costs not read. Sample ends 2005. Unhedged.
- [E] Result is sensitive: removing day 1 cut long-short 12.9% to 11.6%; profit vanishes if prices are recomputed with the forecast (SQ2-3). Larger in small, value, loser stocks (SQ2-4).
- [E] Vol-of-vol: higher VOV lowers delta-hedged returns; 0.52-1.04%/month spread on hedged written calls (SQ2-5, SQ2-6). Hedged; a seller's/hedged result. Low VOV favours hedged long. Not a buyer's return. Sample/maturity not read.
- [E] Term-structure slope (steeper = higher straddle returns) per Vasquez abstract (SQ2-7). Magnitude not read.
- [E, context] IV changes predict STOCK returns, not option returns (SQ2-8).
- Unverified, from search snippets only (no cache; do not quote):
  - Goyal-Saretto JFE 2009 94(2):310-326: sorts on HV minus ATM IV; long-short straddle and delta-hedged call/put returns significant; a working-paper version reported about 5.3%/month at half-spread and 4.1%/month at full quoted spread (snippet unclear which portfolio). Their sample is thought to be 1996-2006 (not confirmed).
  - Cao-Han JFE 2013 108(1):231-249: delta-hedged option returns fall with idiosyncratic vol; ATM options about 1.5 months to expiry, ~6,000 stocks, Jan 1996-Oct 2009 (WP version); a third-party summary (CXO) says the profit of about 2%/month shrinks to near zero after bid-ask costs. Hedged.
  - Jones & Wang (USC WP): slope across all equity options reportedly does not predict straddle returns, in conflict with Vasquez; excerpt truncated.
  - AEA 2023 abstract: skew and spread predictability largely reflects stock borrow fees (affects stock-return skew results).
  - Garcia-Ares 2025: abnormal option returns cluster around monthly roll/expiry days; insignificant when excluded.
  - O'Donovan-Yu 2024/25 and Hofmann-Thimme-Uhrig-Homburg 2019: transaction costs large relative to hedged long-short option anomalies.

## Conflicts
- Vasquez (slope predicts straddle returns) vs Jones-Wang (slope across all options does not): unresolved, conditions unknown (unverified snippet).
- Saretto/Goyal-Saretto gross returns (6-13%/month) vs cost-adjusted and later critiques (Cao-Han near zero after spreads, Garcia-Ares, O'Donovan-Yu): gross vs net, and sample differences.
- Saretto: forecast beats IV as a vol predictor; a thesis snippet says real-time IV estimates make excess returns largely disappear (unverified).

## Not found / not searched
- Not searched: topic (4) volatility clustering/post-crash and whether options reflect it; topic (6) IV relative to its own history as a standalone signal (only inside Saretto's model); skew (3) as predictor of OPTION returns (only found stock-return skew papers, AEA 2023 snippet).
- Not read: Vasquez maturity and effect size; Cao-Han and Goyal-Saretto published full text (core.ac.uk returned 403).
- No tested 3-6 month maturity results for any signal read; all read results are about 1 month holds on 30-60 day options.
- No unhedged out-of-sample post-2015 result found.

## Table 1: signals
| signal | direction favouring buying | effect size | sample | maturity | hedged? | survives costs? | id |
|---|---|---|---|---|---|---|---|
| Low ATM IV vs own 12m avg IV/RV and cross-section (IV-RV style) | low IV | L-S straddle 12.9%/mo; top decile +5.6%/mo | 1996-Jun 2005 (ends before 2015) | 30-60d, ~1m hold | no (straddles, calls, puts) | partly: up to 8.8%/mo claimed after costs; not verified | SQ2-1,2 |
| Term-structure slope | steeper slope | not read | not read | not read | straddles (unhedged) | not read | SQ2-7 |
| Skew | not searched for option returns | n/a | n/a | n/a | n/a | n/a | SQ2-8 (stock returns only) |
| Clustering after falls | not searched | | | | | | |
| Vol of vol | low VOV (hedged) | 0.52-1.04%/mo quintile spread | not read | not read | delta-hedged | not read | SQ2-5,6 |
| IV vs own history | inside Saretto model: IV below own 12m avg | see row 1 | 1996-2005 | 30-60d | no | see row 1 | SQ2-2 |
| Idiosyncratic vol | low idio vol (hedged) | about 2%/mo, near zero after spreads (unverified) | 1996-2009 | ~1.5m | delta-hedged | no (unverified) | snippet only |

## Table 2: recipes
| signal | formula | rule | inputs, lookback | delay | stocks | option choice | holding | prices | fields | real option data? | id |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Saretto IV forecast | Δiv(t+1)=a+b·iv(t)+g1·(iv(t)−mean12m iv)+g2·(iv(t)−mean12m rv); iv=ln ATM IV (avg of call/put IV), rv=ln realised vol; Fama-MacBeth, out-of-sample forecasts | decile of predicted Δiv; long decile 10 (and short 1 for L-S) | month-start IV; trailing 12-month avg IV and RV | not stated beyond "month beginning"; later test skipped day 1 | OptionMetrics stocks with valid quotes, no size filter stated; avg 134 stocks per decile-month | ATM (moneyness 0.95-1.05), expiry 30-60d (second near-term month) | month start to month end (~21 days) | mid of closing bid and ask | daily bid/ask, IV, strike, expiry; CRSP returns | yes | SQ2-1,2 (read from PDF pp.1-16) |
| Goyal-Saretto HV-IV | sort on HV minus ATM IV (exact windows not read) | deciles | not stated | not stated | not stated | not stated | not stated | not stated | not stated | yes | snippet only |
| Vol-of-vol | std of daily % change of vol over prior month; vol = 30d IV, EGARCH(1,1) 252d, or 5-min realised | quintiles | prior month daily vol | not stated | not stated | delta-hedged calls, daily rebalance | month | not stated | daily IV, deltas (EGARCH/intraday variants need stock data) | yes for implied; no for realised variants | SQ2-5 |
| Term-structure slope | not stated (not read) | high vs low slope | not stated | not stated | not stated | not stated | not stated | not stated | not stated | yes | SQ2-7 |
| Skew, idio vol, clustering | not stated | | | | | | | | | | |

## Blocked
- core.ac.uk (403 on WebFetch). fetch_page.py "unsupported" for PDFs, so PDFs (upenn, NBER, City) were read as images via the saved WebFetch files; their quotes are verified:false because they are not in the cache. Cambridge page cached (abstract only).

## Search log
1. IV vs RV cross-section options (search, several sources); 2. Goyal Saretto (search, +3); 3. weakening/costs (disconfirm, +4 snippets, nothing direct); 4. Cao-Han (search, +2); 5. Goyal-Saretto details (search, no table); 6. skew/term-structure (search, Vasquez, Jones-Wang); plus fetches of 5 PDFs and Cambridge. Budget exhausted.
