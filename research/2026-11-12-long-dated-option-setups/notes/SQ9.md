# SQ9 notes (as of 2026-11-12). Budget: roughly 20 calls used.

## Answer
Only three papers were read in original text with method detail: Bali et al. (ML, 1996-2020), Cao-Han-Tong-Zhan (1996-2012) and Heston et al. option momentum (1996-2019). Every one of their results is delta-hedged or straddle based, so none is an outright call/put buyer's return except the static straddle figure in option momentum. Goyal-Saretto and Vasquez could not be obtained as full text (abstract pages only), so their recipe rows are "not stated". Costs: Cao et al. signals and the Bali nonlinear ensemble survive 100% of quoted spread in hedged form; option momentum does not.

## Findings
- [E] Bali et al.: 1996-2020, 12M+ option-month obs, daily delta-hedged, 1-month hold, 273 characteristics; N-En long-short 2.04%/month, L-En 1.30%; 0.67%/month at full effective spread on options and hedge. SQ9-1,2,3
- [E] Implied volatility is the single most important predictor; higher IV predicts lower hedged return (hedged: cheap-vol signal). SQ9-4
- [E] Filters and maturity buckets (<=90 / >90 days) in Bali; the high-ranked decile skews to long-term calls. SQ9-5,6. Bali also has a table by maturity bucket, not extracted (not read in detail).
- [E] Cao et al. (sample ends 2012, before 2015): ~50-day ATM, 8 of 12 stock characteristics give significant decile spreads in hedged call writing; ISSUE 1.46% -> 0.62%/month at 100% spread. SQ9-7..10
- [E] Option momentum (1996-2019): 1-12 month quintile spread 3.64% static straddle, 5.59% daily hedged, near zero after full spread (below-median-spread options). SQ9-11..13
- [O] Vasquez and Goyal-Saretto: abstract-level only. SQ9-14,15
- [E] Disconfirm: Eberbach et al. 2025 simulation shows daily-hedged return tests can produce spurious illiquidity premia. SQ9-16

## Conflicts
- Term structure: Vasquez (abstract: high slope outperforms) vs Jones-Wang. Jones-Wang PDF was unreachable (expired SSL cert, msbfile03.usc.edu), so only a search snippet exists: slope predicts short-term straddle returns in the cross-section, nothing for longer-term straddles, none for average/index level. Unverified; probably a difference in maturity and level (cross-section vs aggregate), not a true contradiction. Not resolved.
- Signs: Cao et al. report call-WRITING returns; a buyer takes the opposite sign. Bali: hedged long-short of predicted returns.

## Signal table
| signal | direction favouring buying | effect size | sample | maturity | hedged? | survives costs? | read in original? | id |
|---|---|---|---|---|---|---|---|---|
| ML ensemble of 273 chars (IV dominant) | low IV, predicted high rank | 2.04%/mo L-S | 1996-2020 | all, >=2 wks; 90-day buckets | delta-hedged daily | 0.67%/mo at 100% spread | yes | 1-6 |
| Idio vol, past returns, profitability, cash, issuance, analyst dispersion | opposite of call-writing sign (not tabulated by me) | ISSUE 1.46%/mo mid; size -3.79% | 1996-2012 (ends before 2015) | ~50 days | delta-hedged, static | 7 of 8 positive at 100% spread | yes | 7-10 |
| Option momentum (past straddle return) | high past straddle return | 3.64% static, 5.59% hedged, quintile 1-12m | 1996-2019 | 1-month straddles to expiry | both | near zero at full spread | yes | 11-13 |
| Term-structure slope | high slope | not read | not read (secondary: 1996-2007) | not read | straddle | not read | abstract only | 14 |
| Realised-minus-implied vol | high gap | not read | not read | not read | straddles + hedged | not read | abstract only | 15 |

## Recipe table
| signal | formula | rule | inputs/lookback | publication delay | stock filter | option choice | holding | entry/exit prices | data fields | real option data? | id |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bali ML | 273 characteristics; models trained expanding window (details not extracted) | decile sort on predicted return | option + stock chars | not stated | options only: IV/Greeks present, no dividend in period, volume in last 7 days, bid>0, mid>=$0.125, rel spread<=50%, 3rd-Friday | all moneyness/maturity >=2 weeks | 1 calendar month or to expiry; daily hedge | quotes at trade start; mid in return, 25-100% spread cost | IV, Greeks, bid/ask, volume, OI, CRSP/Compustat | yes | 1-6 |
| Cao et al. | decile sort on stock characteristic (IVOL = Fama-French residual std; others per paper appendix) | top vs bottom decile, EW/VW | per variable (not extracted) | not stated in my extract | common stock, price>=$5, option volume>0, bid>0, mid>=$1/8, moneyness 0.8-1.2, no dividend | ATM call and put, shortest maturity >1 month (47-52 days) | 1 month, no rehedge | mid-point; cost 10-100% of quoted | OptionMetrics quotes/delta, CRSP, Compustat, IBES | yes | 7-10 |
| Option momentum | average past straddle return over formation window; quintiles | long top, short bottom | lags 1-12 and longer to 36m | not stated | optionable common stock; straddle spread <=50% of value; open interest>0 at start | zero-delta ATM straddle, 1-month, monthly cycle | to expiry | bid-ask midpoint | option quotes, delta, OI, CRSP | yes | 11-13 |
| Term slope | not stated | not stated | not stated | not stated | not stated | not stated | not stated | not stated | not stated | yes | 14 |
| RV minus IV | HV minus ATM IV (per abstract); lookback not stated | deciles | not stated | not stated | not stated | not stated | not stated | not stated | not stated | yes | 15 |

## Not found / not searched
- Goyal-Saretto full text (erim.eur.nl 404; core.ac.uk blocked; SSRN blocked). The 12.9%/5.6% figures remain unverified.
- Vasquez full text, Jones-Wang full text, Choy-Wei, Cao-Han 2013 original, vol-of-vol, skew predictor, post-sharp-fall volatility, IV vs own history: not searched (budget). Bali Table 6 by maturity not extracted.
- Cao et al. per-signal 10-1 values for IVOL, RET, DISP etc.: not extracted.
- Post-2015 replication: Bali (2020 end) is the only later sample; no dedicated replication found. Eberbach et al. 2025 is the only disconfirming item.

## Blocked
msbfile03.usc.edu (expired SSL cert), www.erim.eur.nl (404), core.ac.uk, ssrn (per brief).

## Search log
1 Goyal Saretto pdf (search, 1 new: Purdue abstract). 2 Vasquez pdf (search, Cambridge abstract). 3 ML option return (search, Bali). 4 Goyal Saretto alt (search, 0 new). 5 Jones Wang (disconfirm, snippet). 6 Heston option momentum (search, sjtu pdf). 7 Cao Han Tong Zhan (search, abfer pdf). Fetches: Bali, Hollstein (wrong paper, ignore), Purdue, etc. Eberbach found in prior cache.
