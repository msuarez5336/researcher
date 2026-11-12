# SQ3 notes: stock-side conditions and option returns (as of 2026-11-12)

## Answer
I found no study in 20 calls that measures outright (unhedged) option-buyer returns conditional on a stock-side setup at 1-6 month maturity. The option-return evidence is on delta-hedged ~50-day at-the-money options (Cao et al.) and on one-month straddles sorted by the option's own past return (Heston et al.). In both, the effects are gross of costs, and the straddle effect is close to zero once the full spread is paid. The working hypothesis (a rebound after a sharp fall is not rewarded in option returns) is not confirmed or refuted. The only direct decline study (Choi-Jayaraman) covers 2-day share rebounds, sample 1996-2004, and finds none for optionable stocks.

## Findings
- [E] After a 10%+ one-day drop, two-day share CAR is -0.24% (optionable NYSE/AMEX) and +0.06% (optionable NASDAQ), vs +0.72% / +0.78% for non-optionable firms. 1996-2004 (pre-2015). Share returns only; horizon far shorter than 1-6 months. SQ3-10, SQ3-11.
- [E] Cao-Han-Tong-Zhan: delta-hedged gains (HEDGED, ~50-day ATM, 1996-2012, mid-price) are higher for stocks with higher past 1-month and 2-12 month returns; the paper says both negatively predict delta-neutral call writing. Past-return variables predict stock returns in the opposite direction. This means a high past return goes with cheaper options, and a prior sharp fall goes with more expensive options, in the hedged sense. Not an outright buyer's return. SQ3-5, SQ3-6, SQ3-7. Also: analyst forecast dispersion and idiosyncratic volatility predict LOWER hedged gains; the effect shrinks with spread assumptions (SQ3-8).
- [E] Heston et al.: straddle returns continue (momentum) over 6-36 month formation of the OPTION's own past return; at 1-2 month formation, static straddles show reversal. Near zero after the full spread. 1996-2019. Condition is option-price-based (SQ2 territory); recorded for context. SQ3-1 to SQ3-4.
- [E] Choy-Wei (Financial Review 2022): hedged option returns for calls and puts are higher near the 52-week high or low. Abstract only; sample, maturity and costs not read (unverified detail). SQ3-9. This is the only item on topic (3).
- [O/unverified, search snippets only] Short-term reversal is concentrated in large, low-volatility stocks (Wei, 1964-2009 US sample) and published anomalies decay after publication (Marrow-Nagel 2024 via Chicago Booth Review summary). Crashes of -20% in a month are about 5% of CRSP stock-months 1996-2021 (a dissertation), which makes them hard to predict. Fodor et al. (J Fin Research 2013) say firm age and size predict extreme returns. Kelly NBER w19375 reports tail risk measure R2 4.5% out of sample. None fetched; verified=false items are not in the evidence file.
- Volatility after a sharp fall: not searched; left to SQ2.

## Table: condition vs effect
| condition | predicted share move | horizon | sample | large stocks? | option returns tested? | id |
|---|---|---|---|---|---|---|
| 10%+ one-day drop | no rebound for optionable stocks (-0.24% / +0.06% 2-day CAR) | 2 days | 1996-2004 (pre-2015) | optionable = larger; yes | no | SQ3-10 |
| Past 1-month / 2-12 month stock return | opposite-sign share effects (reversal/momentum), size not read | 1 month | 1996-2012 (pre-2015) | price >= $5, optionable | yes, hedged only, ~50-day ATM; higher past return goes with higher hedged gain | SQ3-6 |
| Past option (straddle) return | continuation 6-36m; reversal at 1-2m (static) | 1 month hold | 1996-2019 | optionable, spread filter | yes, 1-month ATM straddle, unhedged and hedged; ~0 after full spread | SQ3-1..4 |
| Near 52-week high or low | not read | not read | not read | not read | yes, hedged, calls and puts higher | SQ3-9 |
| Analyst dispersion | not read for shares | 1 month | 1996-2012 | price >= $5 | hedged: higher dispersion goes with lower gain | SQ3-5 |
| Short interest/squeeze, estimate revisions, insider buying, extreme-move prediction (beyond snippets) | not searched / not found | | | | | |

## Recipe table
| signal | exact formula | threshold/ranking | inputs, lookback | publication delay | stocks | option choice | holding | entry/exit prices | data fields | real option data? | id |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Past 1-month return RET(-1,0) | "lagged one month return" (Jegadeesh 1990); formula not stated beyond that | decile sort at month-end, 10-1 spread of hedged call gains | stock return, previous month | not stated | CRSP share codes 10/11, price >= $5 at prior month end, optionable | one call and one put closest to ATM, shortest maturity above 1 month (~47-52 days), moneyness 0.8-1.2, volume>0, bid>0, mid >= $1/8, no dividend before expiry | one month, delta-hedged daily (also to maturity) | bid-ask midpoint; costs tested at 10-100% of quoted spread | stock returns, option bid/ask, delta, volume | yes | SQ3-5, SQ3-6 |
| Past 2-12 month return RET(-12,-2) | cumulative return over 11 months ending at start of previous month | decile sort | 11 months, skipping last month | not stated | as above | as above | as above | as above | as above | yes | SQ3-6 |
| Analyst dispersion DISP | as in Diether-Malloy-Scherbina (2002); exact formula not stated in what I read | decile sort | I/B/E/S | not stated | as above | as above | as above | as above | I/B/E/S forecasts | yes | SQ3-5 |
| Option momentum (straddle return history) | straddle weights proportional to -dP*C and dC*P, summing to 1 (call delta closest 0.5, 0.25-0.75 allowed); return = weighted call/put return held to expiry | quintile sort on average past straddle return; 1-12 month spread 3.64%/month static | formation 1-36 months, at least two thirds of months non-missing | none (own prices) | OptionMetrics common stock, regular monthly cycle, straddle weighted spread <= 50% of value | ATM straddle expiring next month (~1 month) | to expiry (~1 month) | call/put midpoint entry; split-adjusted stock at expiry | option bid/ask, delta, stock price | yes | SQ3-1..4 |
| 52-week high/low proximity | not stated (abstract only) | not stated | not stated | not stated | not stated | not stated | not stated | not stated | not stated | yes | SQ3-9 |
| Drop of 10%+ | one-day price decline of 10% or more; abnormal return from market model fit on days -105 to -6 | event | not applicable | none | NYSE/AMEX/NASDAQ, optionable vs non-optionable matched pairs | none (share returns) | CAR over 2 days | closing prices | CRSP | no | SQ3-10 |

## Conflicts
- Share-level reversal after a drop (non-optionable stocks) vs none for optionable stocks (SQ3-10): depends on option listing and liquidity; the effect is about 2 days only.
- Heston et al. find static straddles reverse at 1-2 month formation but hedged versions continue (SQ3-4): hedging itself is a reversal trade, so hedged and unhedged results disagree. Do not read hedged results as the buyer's return.
- Past-return signals: Cao et al. say higher past return goes with higher hedged gain; so a fallen stock has dearer options, conflicting with a "rebound is cheap to play" idea (hedged only).

## Not found
- Any unhedged, 1-6 month option-return test conditional on a prior sharp decline, 52-week low, short interest, revisions or insider buying.
- The size of 1-6 month share rebound after a large single-stock decline (not reached).
- Short interest/squeezes (one search snippet only), analyst revisions beyond dispersion, insider buying: not searched. Extreme-move prediction: one search, snippets only, nothing fetched.
- Evidence against (decay): one search; Marrow-Nagel and Wei results from snippets only, not verified. No study of decay of option-return predictors found.

## Blocked
- core.ac.uk (403) for the Cao et al. published version; mpra.ub.uni-muenchen.de (reset); papers.ssrn.com (403, in index from another worker). fetch_page.py does not support PDFs: I used WebFetch to download the PDFs, ran pdftotext, saved text in RUN/pages, and appended index entries for them to pages/index.jsonl so check_quotes works (11 of 11 quotes pass). Versions read: Cao et al. April 2016 working paper (ABFER), Heston et al. Sept 2021 draft (SJTU-hosted), Choi-Jayaraman Feb 2008 draft (Georgia Tech).

## Search log
1. "stock return reversal after large price decline option returns" (search): 3 useful sources.
2. "momentum option returns stocks past returns predict delta-hedged..." (search): 4.
3. "momentum reversal ... decayed since publication large stocks" (disconfirm): 2, snippets only.
4. fetch of 4 PDFs: 2 readable.
5. Cao et al./52-week search: 2 new. 6. Short-interest/delta-hedged search: 0 usable new. 7. Extreme jumps/crash search: snippets only.
Also fetched Choy-Wei RePEc page.
