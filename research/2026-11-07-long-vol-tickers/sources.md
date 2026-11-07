# Sources: liquid tickers for long options and long strangles

*As of 2026-11-07.* Status: ✓ verified against the original (quote check plus claim-verifier where
listed) · ~ summary/snippet only · ✗ unreachable. [S] = this run's own reproducible screen.

## Primary sources
| # | Source | Type | Date | Status | Evidence | Verdict |
|---|---|---|---|---|---|---|
| 1 | Own screen: `screen/screen.py`, `metrics.csv`, trials 2–5 | [S] computed | 2026-11-07 | reproducible | Nasdaq daily OHLCV, Cboe vol indices | The shortlist, the straddle-at-implied test and the conditional test. Daily bars, 30-day IV proxy. |
| 2 | [Goyal & Saretto, JFE 94(2)](https://econpapers.repec.org/RePEc:eee:jfinec:v:94:y:2009:i:2:p:310-326) | Paper (abstract) | 2009 | ✓ (C1) | SQ1-1 | The RV > IV straddle condition. No magnitudes read. |
| 3 | [Cao & Han, JFE 108(1)](https://econpapers.repec.org/RePEc:eee:jfinec:v:108:y:2013:i:1:p:231-249) | Paper (abstract) | 2013 | ✓ partial (C2) | SQ1-3 | Delta-hedged returns fall with idiosyncratic vol. |
| 4 | [Carr & Wu, RFS 22(3)](https://econpapers.repec.org/RePEc:oup:rfinst:v:22:y:2009:i:3:p:1311-1341) | Paper (abstract) | 2009 | ✓ (abstract only) | SQ1-2 | VRP definition and sample. No magnitudes read. |
| 5 | [IVolatility earnings straddle study](https://www.ivolatility.com/news/3147) | Vendor study (self-published) | 2026 | ✓ partial (C4) | SQ2-9, 2-10 | −18.5% average. The underpriced quintile, sorted ex ante, earned +36.7%. Basis for hypothesis S-E. |
| 6 | Cboe volatility-index CSVs (e.g. [VXAPL](https://cdn.cboe.com/api/global/us_indices/daily_prices/VXAPL_History.csv), [GVZ](https://cdn.cboe.com/api/global/us_indices/daily_prices/GVZ_History.csv), [VIX](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv)) | Exchange data | to 2026-11-06 | ✓ partial (C9) | SQ3-9–11 | The free 30-day implied vol used in trials 4–5. VXXLE gave 403. VXTLT has a different format. |
| 7 | [Fidelity long straddle](https://www.fidelity.com/learning-center/investment-products/options/options-strategy-guide/long-straddle) / [long strangle](https://www.fidelity.com/learning-center/investment-products/options/options-strategy-guide/long-strangle) | Broker education | n.d. | ✓ (C7) | SQ2-7, 2-8 | Vega, decay and break-even mechanics. |

## Secondary and practitioner sources
| # | Source | Author/org | Date | Status | Verdict |
|---|---|---|---|---|---|
| 1 | [TradeStation: top stocks for options trading](https://www.tradestation.com/insights/top-stocks-for-options-trading/) | TradeStation | to 2026-10-30 | ✓ partial (C8) | Stock/ETF liquidity order. Excludes SPX. |
| 2 | [thetrading.tools most active options](https://www.thetrading.tools/most-active-options) | thetrading.tools | 2026-11-06 | ✓ quote | A single-day cross-check of the order. |
| 3 | [CXO Advisory on Cao & Han](https://www.cxoadvisory.com/?p=13193) | CXO Advisory | 2010s | ✓ (C3), partial (C2) | The −4.89% figure and cost sensitivity, from the working paper. |
| 4 | [FlashAlpha gamma scalping guide](https://flashalpha.com/articles/gamma-scalping-complete-guide-delta-hedging) | FlashAlpha (vendor) | n.d. | ✓ partial (C6) | Gamma–theta identity in a simplified model. Use a textbook when reachable. |
| 5 | [LuxAlgo NR4/NR7](https://www.luxalgo.com/library/concept/nr4-nr7-narrow-range-bars.md) | LuxAlgo | n.d. | ✓ partial (C5) | Assertion. Cites Crabel 1990 (futures). |
| 6 | [StockCharts BandWidth](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/bollinger-bandwidth) | StockCharts | n.d. | ✓ partial (C5) | Assertion, no baseline. |
| 7 | [SentimenTrader BandWidth](https://sentimentrader.com/education/technical-indicators/bollinger-bandwidth) | SentimenTrader | 2025 | ✓ quote | In-sample single-stock backtest. |
| 8 | Options Analysis Suite, Cboe industry post, OCC annual volume, Cboe penny class | various | 2025–26 | ~ | Snippet or WebFetch only. Context, not load-bearing. |

## Screened and excluded
- papers.ssrn.com, core.ac.uk, mdpi.com (403); cis.upenn.edu (SSL); several NYU, NBER and LMU PDFs (unsupported): full-paper magnitudes were not read.
- theocc.com (403): no per-symbol OCC volume or open interest.
- tastylive low-IV straddle studies and the ORATS/Nasdaq 2019 long-straddle result: snippet only, pages thin or unreachable, unverified.
- Leveraged ETFs (TQQQ, SOXL) and new or odd symbols (SPCX, DRAM, IREN, CRWV): excluded from the universe by SQ3.
