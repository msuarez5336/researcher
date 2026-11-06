# Sources: options swing-trade backtest spec

*As of 2026-11-06. Ranked by usefulness to the question, not by popularity.*

Status: ✓ verified against the original page (quote check plus claim-verifier where listed) ·
~ read via summary/snippet only · ✗ unreachable.

## Primary sources (papers, official docs, first-party write-ups)
| # | Source | Type | Date | Status | Evidence | Verdict |
|---|---|---|---|---|---|---|
| 1 | [Muravyev & Pearson, "Options Trading Costs Are Lower than You Think" (RFS 33(11))](https://ideas.repec.org/a/oup/rfinst/v33y2020i11p4973-5014..html) | Peer-reviewed paper (abstract) | 2020-11 | ✓ (C6) | SQ2-1 | Basis for k = 0.70 base / 1.0 stress. Full tables not read. |
| 2 | [ORATS historical data](https://orats.com/university/historical-data) and [API docs](https://orats.com/docs/historical-data-api) | Vendor docs (self-reported) | 2026-11 | ✓ (C1) | SQ1-1–3 | Default EOD source: 14-min-pre-close snapshot, 2007+, Greeks included. Underlying price is parity-derived. |
| 3 | [Cboe DataShop option quotes](https://datashop.cboe.com/option-quotes) | Exchange docs | 2026-11 | ✓ (C2) | SQ1-4–6 | Exchange-sourced alternative: 15:45 and close, 2012+. |
| 4 | [Databento OPRA dataset](https://databento.com/docs/venues-and-datasets/opra-pillar) | Vendor docs | 2026-11 | ✓ partial (C4) | SQ1-7–9 | Raw OPRA, suffix-marked adjusted contracts, subsampled before 2023-03-28. |
| 5 | [Massive: "Polygon is now Massive"](https://massive.com/blog/polygon-is-now-massive) | First-party announcement | 2025-10-30 | ✓ (C3) | SQ1-10 | Confirms the rename. |
| 6 | [Massive option contract snapshot](https://massive.com/docs/rest/options/snapshots/option-contract-snapshot) | Vendor docs | 2026-11 | ✓ | SQ1-11 | IV and Greeks are snapshot-only. |
| 7 | [Bailey, Borwein, López de Prado & Zhu, "The Probability of Backtest Overfitting"](https://scholarworks.wmich.edu/math_pubs/42) | Peer-reviewed paper (abstract) | 2017 | ✓ (C9) | SQ3-1 | Basis for the PBO/CSCV requirement. Formulas not read (SSRN blocked). |
| 8 | [FINRA fee adjustment schedule](https://www.finra.org/rules-guidance/rule-filings/sr-finra-2024-019/fee-adjustment-schedule) | Regulator | 2026-11-06 | ✓ (C8) | SQ2-10 | Options TAF by year. |
| 9 | [Interactive Brokers options commissions](https://www.interactivebrokers.com/en/pricing/commissions-options.php) | Broker fee page | seen 2026-11-06 | ✓ partial (C7) | SQ2-3, 2-4 | $0.65 applies at premiums ≥ $0.10. OCC clearing $0.025. |
| 10 | [Robinhood trading fees](https://robinhood.com/us/en/support/articles/trading-fees-on-robinhood/) | Broker fee page | seen 2026-11-06 | ✓ (C8) | SQ2-7–9 | SEC fee, TAF pause, OCC/ORF pass-through. |
| 11 | [Fidelity commissions](https://fidelity.com/trading/commissions-margin-rates) | Broker fee page | seen 2026-11-06 | ✓ | SQ2-5 | $0.65, plus $0.50 for professional options traders. |
| 12 | [tastytrade pricing](https://tastytrade.com/pricing/) | Broker fee page | seen 2026-11-06 | ✓ | SQ2-6 | $1 to open, capped at $10 per leg, $0 to close. |
| 13 | [quantstrat `deflatedSharpe`](https://www.rdocumentation.org/packages/quantstrat/versions/0.16.7/topics/deflatedSharpe) | Software docs | n.d. | ✓ | SQ3-5 | A working DSR implementation citing Bailey & López de Prado (2014). |
| 14 | [ThetaData docs](https://docs.thetadata.us/Articles/Getting-Started/Subscriptions.html) | Vendor docs | 2026-11 | ✓ listing / ~ details | SQ1-12, 1-13 | Lists Binomial and EOD Greeks. Start date and timing unverified. |

## Repositories (skills screened; see `security-scan.md`)
| # | Repo | Stars | Last commit | Status | What it contains | Verdict |
|---|---|---|---|---|---|---|
| 1 | [massive-com/ai](https://github.com/massive-com/ai) | not recorded | 2026-10-28 | scanned clean | Vendor skills for the Massive API, incl. options and backtest | Reference only; needs a paid key. |
| 2 | [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | not recorded | 2026-11-06 | scanned clean | `backtest-expert` skill + stdlib evaluator | Good validation checklist; its trade-count rule has no primary source. |
| 3 | [wshobson/agents](https://github.com/wshobson/agents) | not recorded | 2026-11-05 | scanned clean | `backtesting-frameworks` skill | Generic; not needed. |
| 4 | [zeroes-ones/Skills](https://github.com/zeroes-ones/Skills) | not recorded | 2026-10-14 | scanned clean | `swing-options-trader` skill | Not adopted: unsourced performance claims, no licence file. |

## Secondary and practitioner sources
| # | Source | Author/org | Date | Status | Verdict |
|---|---|---|---|---|---|
| 1 | [Options Playbook: open interest](https://optionsplaybook.com/options-introduction/open-interest) | Options Playbook | n.d. | ✓ partial (C5) | Prior-day OI. Some feeds lag an extra day (Alpaca, per the verifier). |
| 2 | [Dividends and their effect on options](https://app.certfuel.com/series7/learn/options/options-fundamentals/dividends-and-their-effect-on-options) | Certfuel (Series 7 prep) | n.d. | ✓ partial (C10) | Necessary condition for early exercise. Replace with OCC or Hull when reachable. |
| 3 | [CXO Advisory summary of López de Prado](https://www.cxoadvisory.com/big-ideas/10-steps-to-becoming-a-better-quant) | CXO Advisory | 2018 | ✓ quote / secondary | Walk-forward criticism and DSR inputs. Opinion. |
| 4 | [tastylive: managing winners](https://www.tastylive.com/definitions/managing-winners) | tastylive (vendor) | n.d. | ✓ quote | 50% "sweet spot": a convention, no figures. |
| 5 | [Thread summarising Muravyev & Pearson](https://threadreaderapp.com/thread/1346160221408829441.html) | social summary | 2021-01 | ✓ quote / grade C | The ~80% of quoted spread figure. Its definition is ambiguous. |
| 6 | [Schwab: ex-dividend dates and dividend risk](https://www.schwab.com/learn/story/ex-dividend-dates-understanding-dividend-risk) | Schwab | n.d. | ~ (page thin, auth error) | Put-extrinsic rule seen in a snippet only. |
| 7 | [Elite Trader thread on minimum trades](https://www.elitetrader.com/et/threads/minimum-number-of-trades-required-for-backtesting-results-to-be-trusted.356588/page-2) | forum | n.d. | ~ | Shows 30/100+ is folklore, not a sourced threshold. |

## Screened and excluded
- theocc.com, papers.ssrn.com, core.ac.uk, optionsclearing.com: blocked (403 or connection reset). OCC open-interest text and the DSR/PBO full papers were not read.
- Saxo and optionmatters.ca early-exercise articles: unreachable.
- The Massive options overview page returned 404.
- IVolatility: not researched (budget).
