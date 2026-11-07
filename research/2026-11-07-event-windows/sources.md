# Sources: event and regime windows for long options

*As of 2026-11-07.* Status: ✓ verified (quote check plus claim-verifier where listed) · ~ summary or
snippet only · [S] this run's reproducible event study.

## Primary and computed
| # | Source | Type | Date | Status | Evidence | Verdict |
|---|---|---|---|---|---|---|
| 1 | Own event study: `study/events.py`, `results.csv`, `events.csv`, `run.log` | [S] | 2026-11-07 | reproducible | Nasdaq OHLCV, Cboe indices, SqueezeMetrics GEX, Fed calendar | The calendar's measurements. See the limitations in report.md. |
| 2 | [Nagel, "Evaporating Liquidity", RFS 25(7)](https://econpapers.repec.org/RePEc:oup:rfinst:v:25:y:2012:i:7:p:2005-2039) | Paper (abstract) | 2012 | ✓ (C2) | SQ1-5 | Reversal profits rise with VIX. |
| 3 | [Kurov, Wolfe & Gilbert, Finance Research Letters 40](https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html) | Paper (abstract) | 2021 | ✓ (C4) | SQ2-2 | Pre-FOMC drift gone after 2015. |
| 4 | [Lucca & Moench, Liberty Street Economics](https://libertystreeteconomics.newyorkfed.org/?p=1112) | NY Fed blog | 2012 | ✓ (C4) | SQ2-1, 2-3 | Origin of the pre-FOMC drift. |
| 5 | [Kanniainen & Magris, arXiv 1810.12200](https://arxiv.org/abs/1810.12200) | Preprint (abstract) | 2018 | quote ✓, cost claim ~ | SQ1-11 | Index IV adjusts gradually after jumps. |

## Secondary and practitioner
| # | Source | Author/org | Date | Status | Verdict |
|---|---|---|---|---|---|
| 1 | [Alpha Architect on Medhat & Schmeling](https://alphaarchitect.com/short-term-momentum/) | Alpha Architect | 2021–22 | ✓ partial (C1) | Liquid stocks continue, illiquid ones reverse. |
| 2 | [CFA digest on Savor (2012)](https://rpc.cfainstitute.org/research/cfa-digest/2013/02/stock-returns-after-major-price-shocks-the-impact-of-information) | CFA Institute | 2013 | ✓ (C3) | No-news shocks reverse. |
| 3 | [OptionMetrics on macro-announcement straddles](https://optionmetrics.com/?p=445) | OptionMetrics | n.d. | ✓ (C5) | FOMC is the one macro event where straddles earned positive returns. The paper's sample isn't shown. |
| 4 | [FlashAlpha GEX 8-year backtest](https://flashalpha.com/articles/gex-dex-vex-chex-8-year-backtest-spy-vix-control) | FlashAlpha (vendor) | n.d. | ✓ (C6) | GEX adds nothing after VIX and IV. |
| 5 | [CFA Institute blog: how well does VIX predict](https://rpc.cfainstitute.org/blogs/enterprising-investor/2024/how-well-does-the-vix-predict-volatility) | CFA Institute | 2024 | ✓ (C7) | VIX lags at panic onset, then overshoots. |
| 6 | [Man Group: views from the floor](https://www.man.com/insights/views-from-the-floor-2021-dec-14) | Man Group | 2021 | ✓ (C8) | Mixed returns after VIX spikes. |
| 7 | [IVolatility: SPY after IV spikes](https://www.ivolatility.com/news/3127) | IVolatility (vendor) | 2026 | ✓ (C9) | 9 spikes; not significant without overlap. |
| 8 | [CXO Advisory on FOMC-day reversal](https://cxoadvisory.com/calendar-effects/stock-market-return-reversal-after-fomc-announcements/) | CXO Advisory | 2020 | ✓ (C10, secondary) | +0.18% per event, 1997–2020. The SSRN original is blocked. |
| 9 | [Alpha Architect: short-term signals](https://alphaarchitect.com/alpha-from-short-term-signals/) | Alpha Architect | n.d. | quote ✓ | Costs swamp short-term signals. |
| 10 | Chan (JFE 2003), Lochstoer & Muir (NBER), Adhikari & Hilliard, Cheng (VIX premium), the JFQA VVIX paper, Li & Zinna | various | various | ~ | Cited for context only; PDFs unreadable or snippet-only. |

## Screened and excluded
- Earnings sources: excluded by user decision.
- bls.gov (403): no CPI or payroll dates, so those windows are untested.
- papers.ssrn.com, core.ac.uk (403); PDFs on NBER, NY Fed, Fed IFDP, JFQA (unsupported by the fetcher).
