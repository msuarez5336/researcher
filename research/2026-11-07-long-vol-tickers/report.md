# Liquid tickers for long options and long strangles

*Research run `research/2026-11-07-long-vol-tickers/` · as of 2026-11-07 · tier: STANDARD ·
extends `research/2026-11-06-options-swing-backtest-spec/report.md` (the v2 spec)*

Tags: [E] evidence (documented or measured), [O] opinion or convention, ✓ verified by a fresh-context
claim-verifier, ~ read via summary or snippet only (unverified). [S] = this run's own screen, reproducible
from `screen/` (Nasdaq daily OHLCV 2016-11 → 2026-11, Cboe volatility indices).

## Top findings
1. **Buying volatility unconditionally lost money on every ticker we could price.** A 10-day ATM straddle priced at the Cboe implied-vol index lost on average, before costs, on all 7 tickers with a usable index:
   - SPY −23%, IWM −16%, QQQ −14%, EWZ −13%, AMZN −12%, GOOGL −10%, AAPL −7%. Every one is significant except AAPL (t = −0.4).
   - The literature agrees. Delta-hedged long equity calls lost about 4.9% of premium in Cao & Han's 1996–2009 sample ✓. In a vendor study, earnings straddles had a 22% win rate and lost 18.5% per trade ✓.
   - [S] (`screen/trial4_straddle_iv.csv`); [E] {C3, C4}
2. **"Compression leads to expansion" is not supported on a 3–10 day horizon.**
   - We found no peer-reviewed, out-of-sample test showing that NR7, Bollinger squeezes or ATR percentiles predict larger ranges in US equities. The practitioner support is at most Crabel's 1990 futures tabulations or in-sample single-stock backtests. [E] ✓ narrowed {C5}
   - In our screen, all 24 tickers showed *less* post-compression range expansion than a random walk does (`expand` 1.04–1.69 against a null of about 1.9). That fits volatility clustering, where low volatility persists in the short run. [S]
   - Straddles entered on squeeze days did *worse* on 5 of 7 tickers. [S] (trial 5)
3. **Cheap implied vol reduces the loss but doesn't remove it.**
   - When implied was below 20-day realised (the Goyal & Saretto condition), straddle losses shrank on every ticker, but stayed negative (−6% to −14%). [S] (trial 5)
   - The academic pockets of positive long-vol returns are cross-sectional and monthly. In Cao & Han the spread strategy falls from about 2% a month at mid to about 1% when paying 50% of the bid-ask spread, and to about zero at 100%. [E] ✓ (C2 narrowed) {C1, C2}
4. **The one strong positive result is earnings straddles where implied was below the historical earnings move.** IVolatility sorted about 9-DTE ATM straddles, bought at the ask at the close before the print and sold at the bid after it, into quintiles by implied move vs *historical* realised move, which is known at entry. The most underpriced quintile earned +36.7% per trade with an 80% win rate. The most overpriced quintile lost 44.5%. This is a self-published vendor study, in-sample, with no out-of-sample test. [E, vendor] ✓ narrowed {C4}
5. **The 10 tickers (frozen screen, official): QQQ, AAPL, NVDA, MU, AMD, SMH, HOOD, TSLA, SOXX, SOFI.**
   - They rank best on liquidity, on how often 10-day moves beat recent realised vol, on the largest swing inside a 10-day window, and on post-compression range. That makes them the best *candidates to test*, not tickers with proven favourable odds.
   - Six of the ten are semiconductors or semi ETFs, so the portfolio rules must cap them.
   - HOOD and SOFI have short histories, the lowest liquidity ranks, and IPO- or SPAC-era jumps in their data. [S]
6. **AAPL is the best candidate for a long-volatility test.** It ranks 2nd and has the smallest straddle loss at implied (−7%, not significant). Its squeeze-day straddles came out about flat (+0.5%). [S]
7. **Most liquid stock and ETF option underlyings (month to 2026-10-30):** SPY 11.7M contracts a day, QQQ 8.7M, NVDA 2.6M, TSLA 2.0M, IWM 1.9M. SPX index options (about 4.9M a day in Q3 2026) are excluded, since they have no stock or ETF underlying. These are secondary, dated rankings. OCC per-symbol data was blocked. [E] ✓ narrowed {C8}

**Bottom line:** no ticker in the liquid universe shows favourable odds for buying options *by
itself*. Implied volatility on average costs more than the move that follows, and that cost is about
7–23% of a 10-day straddle's premium on the names we could measure. A long strangle backtest
should therefore expect a negative baseline and must beat it with an entry filter. For long calls
and puts, the directional signal has to pay that toll as well.

## The shortlist

From `screen/metrics.csv`. Score = mean percentile rank of liquidity, tail10, excur10 and expand.

| # | Ticker | Liquidity rank (of 24) | Largest 10-day swing ÷ recent vol (`excur10`) | Implied − realised (vol pts) | IS→OOS rank | Flags |
|---|---|---|---|---|---|---|
| 1 | QQQ | 2 | 1.10 | +2.8 | 5→1 | straddle at implied −14% |
| 2 | AAPL | 7 | 1.14 | +3.4 | 1→4 | straddle −7% (n.s.); squeeze ≈ flat |
| 3 | NVDA | 3 | 1.11 | n/a | 4→5 | semis |
| 4 | MU | 6 | 1.14 | n/a | 2→6 | semis |
| 5 | AMD | 9 | 1.08 | n/a | 12→3 | semis |
| 6 | SMH | 13 | 1.10 | n/a | 3→13 | semis ETF |
| 7 | HOOD | 21 | 1.17 | n/a | –→7 | short history (2021), low liquidity rank, IPO-period jumps |
| 8 | TSLA | 5 | 1.10 | n/a | 7→11 | |
| 9 | SOXX | 23 | 1.11 | n/a | 8→18 | semis ETF, overlaps SMH |
| 10 | SOFI | 24 | 1.16 | n/a | –→8 | short history (2020), lowest liquidity rank, SPAC jump |

Sensitivity (all logged in `screen_spec.md`; none replace the official list):
- **Sector cap of 2 semis (trial 3):** QQQ, AAPL, NVDA, MU, HOOD, TSLA, SOFI, PFE, AMZN, PLTR. Use this list if the backtest runs as one portfolio.
- **Expected-payoff metric (trial 2):** a 1σ strangle priced at *recent realised* vol would have paid more than the normal-distribution null on 22 of 24 tickers. INTC, ORCL, TSLA, SPY and PFE lead. Fat tails do help long options. Trial 4 shows that implied volatility more than offsets that help on every name we could price.
- SPY and IWM are the most liquid but rank 15th and 17th. Their 10-day moves rarely beat recent vol, and implied is rich (SPY straddle −23%).

## Evidence by theme

### When long options have paid
- **Variance risk premium.** Carr & Wu (RFS 2009) measure it on 5 indexes and 35 stocks. We could read only the abstract, so we have no magnitudes. Our own measurement on the indexed tickers: implied exceeded subsequent 21-day realised by **2.0–4.3 vol points** on average (GOOGL 2.0, QQQ 2.8, IWM 3.3, AAPL 3.4, AMZN 3.6, SPY 3.6, EWZ 4.3). [E] [S]
- **Cross-sectional pockets.** Goyal & Saretto (JFE 2009): buying straddles where historical vol exceeds implied (and selling the reverse) earns a significant monthly return. The abstract gives no magnitude or cost analysis. [E] ✓ {C1}
  - Cao & Han (JFE 2013): delta-hedged returns fall monotonically with idiosyncratic vol ✓. Per a secondary summary of the 2010 working paper, the low-minus-high strategy earns about 2% a month at mid, about 1% after paying 50% of the spread, and about zero at 100%, and the effect is smaller for large caps. [E] ✓ narrowed {C2}
  - The "cheap IV" condition is real, but small, and fragile to costs.
- **Earnings.** IVolatility (vendor, self-published): 9,622 S&P 500 earnings ATM straddles from 2021–2026, using about 9-DTE options bought at the ask at the close before the print and sold at the bid at the close after it. Win rate 22%, mean −18.5%. Sorted by implied vs historical realised move: the most overpriced quintile lost 44.5% per trade, and the most underpriced quintile earned +36.7%. [E] ✓ narrowed {C4}

### Range expansion: what the data says
- Practitioner pages (LuxAlgo on NR4/NR7, StockCharts on BandWidth) present narrow ranges as precursors of expansion. Their support is at most Crabel's 1990 futures tabulations, with no out-of-sample equity test. SentimenTrader's in-sample Best Buy backtest says BandWidth doesn't predict direction. [E] ✓ narrowed {C5}
- Volatility clustering means low volatility tends to persist over days. Mean reversion toward the long-run level works over weeks to months, longer than a 3–10 day hold. [O, SQ2]
- [S] `expand` came in below the random-walk null on all 24 tickers. Squeeze-entry straddles were worse than unconditional on SPY, IWM, AMZN, EWZ and QQQ, about flat on AAPL, and slightly better on GOOGL. A compression entry needs its own out-of-sample proof, and the default expectation is that it hurts.

### Strangle mechanics
- Break-even: in a simplified model (fixed IV, continuous hedging, no costs or financing), a delta-hedged long straddle earns ≈ ½ΓS²(σ²realised − σ²implied)dt. Its variance component is positive when realised exceeds the implied paid, and discrete hedging, costs and IV changes add other terms. The ATM daily break-even move ≈ S·IV/√252. Source is a vendor education page, with the textbook form not reached. [E] ✓ narrowed {C6}
- A strangle has positive vega and decays faster than a straddle. Its break-evens sit further apart, and it is more likely to expire worthless (Fidelity [straddle](https://www.fidelity.com/learning-center/investment-products/options/options-strategy-guide/long-straddle), [strangle](https://www.fidelity.com/learning-center/investment-products/options/options-strategy-guide/long-strangle)). [E] ✓ {C7}

## v2 spec addendum: long strangle (hypothesis S)
Everything in v2 applies unless changed here.
- **Phase 1:** structure = long call + long put, same expiry, **0.25–0.30Δ each leg**. The control is an ATM straddle on the same dates. Earnings windows are excluded unless the hypothesis is the earnings one (S-E below). Universe = the shortlist with a sector cap of 2 semis open at once.
- **Phase 2:** each entry needs the **implied move** (straddle mid ÷ spot, from chain data) and the **trailing realised move** over the same horizon.
- **Phase 3:** both legs pass the liquidity filter. Equity skew makes the put leg richer, so log each leg's cost separately.
- **Phase 4: entry filter (the hypothesis).** Implied move < trailing 10-day realised move × 1.0. The compression flag is tested only as an *additional* filter against this baseline, not as the trigger.
  - Exits: profit at +40% of the total debit, stop at −40%, time exit at 10 trading days or DTE < 21, event exit 1 day before earnings. All four are grid parameters.
  - Variant **S-E (earnings):** buy roughly 5–14-DTE options at the close before the print, only when implied move < the ticker's average historical realised earnings move, and sell at the close after the print. This mirrors the IVolatility setup but tests it out of sample. It is outside the 35–60 DTE frame, so it is a separate hypothesis.
- **Phase 5:** add two controls, random-date entries with the same exits, and trigger-only entries with no IV filter. Report the median trade as well as the mean, since strangles are right-skewed.
  - The hypothesis passes only if it beats **both** controls and the v2 gates at k = 1.0. With two legs, the full spread is paid on both legs, in and out.
  - Start the trial count at 5 (this run's screen trials).

## Where sources disagree
| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Do squeezes predict expansion? | Practitioners: yes (StockCharts, LuxAlgo) | Clustering plus our screen: not over 3–10 days | No source gives a baseline-adjusted effect. Treat it as untested. |
| Is "cheap IV" an edge? | Goyal & Saretto: significant cross-sectional returns | Cao & Han: a related effect vanishes after costs. Our trial 5 stays negative. | Possibly on illiquid single names with low costs. Not on these liquid ETFs and megacaps at k ≥ 0.7. |
| Earnings straddles | IVolatility: −18.5% on average | The same study: +36.7% in the underpriced quintile | The sort used historical moves, so it can be identified at entry. It is still vendor, in-sample and unreplicated. |

## Method and limitations
- 3 researchers (≤15 calls each), 1 stdlib screen (`screen/screen.py`, definitions frozen before the run) plus 4 logged sensitivity trials, and 2 claim-verifier batches (9 claims: 3 supported, 6 narrowed to the verifier's wording, 0 refuted).
- **Implied vol for single stocks:** only the Cboe indices (SPY, QQQ, IWM, AAPL, AMZN, GOOGL, EWZ) give free implied vol. VXTLT's CSV has a different format and wasn't loaded. The indices are 30-day implied vol, while the straddle test holds 10 days, so the term structure adds error. The real test needs chain data (ORATS, per v2).
- **Screen data:** daily bars only, so intraday swings show up only through daily H/L. Earnings are included, which inflates single-stock swing metrics. HOOD and SOFI include IPO- and SPAC-period jumps (flagged). Nasdaq data appears split-adjusted (no split flags on TSLA or NVDA).
- **Liquidity ranks** come from dated secondary snapshots (TradeStation, thetrading.tools). OCC per-symbol data was blocked (theocc.com 403), and per-name open interest and spreads weren't found.
- **Blocked:** papers.ssrn.com, core.ac.uk, mdpi.com (403); cis.upenn.edu (SSL); theocc.com (403); the VXXLE CSV (403); several academic PDFs (unsupported by the fetcher). Carr & Wu and Goyal & Saretto magnitudes are missing for that reason.

## Open questions
- Does the IVolatility "underpriced" earnings quintile (sorted on historical realised moves, so known at entry) hold out of sample, after our k = 0.70 fills and on these 10 tickers? The test is the S-E hypothesis with ORATS earnings data.
- Is AAPL's near-zero squeeze result real or noise? About 570 overlapping days is roughly 57 independent observations. Retest out of sample on chain data.
- Do 0.25Δ strangles behave differently from the ATM straddle proxy used here (skew, gamma profile)? Only chain data can answer that.
- Artifact: https://claude.ai/artifact/4wyLfiaCYxCN2V77Cz5ihs, section "Tickers for long options" (private; source in `../2026-11-06-options-swing-backtest-spec/artifact/index.html`).
