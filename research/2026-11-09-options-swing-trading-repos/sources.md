# Sources: GitHub repos that tried buying options on stocks and indexes

*As of 2026-11-09. Ranked by usefulness to the question, not by popularity.*

Status: ✓ quote checked against the cached original · ~ read via summary, snippet or an
uncached page · ✗ unreachable. Stars are the GitHub API `stargazers_count` read on
2026-11-09, because repo pages are blocked to `curl` in this environment. Last commit is
`git log -1 --format=%cs` on a shallow clone of the default branch.

## Primary sources (papers, official docs, first-party write-ups)

| # | Source | Type | Date | Status | Evidence | Verdict |
|---|---|---|---|---|---|---|
| 1 | [Beckmeyer, Branger, Gayda: "Retail Traders Love 0DTE Options... But Should They?"](https://wp.lancs.ac.uk/fofi2024/files/2024/04/FoFI-2024-146-Leander-Gayda.pdf) | Working paper | 2023-12-15 | ✓ | SQ7-P1 to P4 | Best evidence on retail 0DTE outcomes; use the paper, not press summaries |
| 2 | [Bakshi and Kapadia, "Delta-Hedged Gains and the Negative Market Volatility Risk Premium"](https://ideas.repec.org/a/oup/rfinst/v16y2003i2p527-566.html) | Journal article (abstract) | 2003 | ✓ | SQ5-2 | Background only: delta-hedged positions, old data |
| 3 | [Alpaca: index options via Trading API](https://alpaca.markets/blog/alpaca-launches-index-options-via-trading-api) and [docs](https://docs.alpaca.markets/us/docs/index-options) | Broker blog and docs | read 2026-11-09 | ✓ | SQ3-11 to 14 | Authoritative for Alpaca's index-option support and limits |
| 4 | [IBKR market data subscriptions](https://www.interactivebrokers.com/docs/general/market-data-subscriptions/popular-market-data-subscriptions) | Broker docs | read 2026-11-09 | ✓ | SQ3-3, SQ3-4 | Authoritative for data add-ons; commissions not covered |
| 5 | [schwab-py docs: authentication](https://schwab-py.readthedocs.io/en/latest/auth.html), [order templates](https://schwab-py.readthedocs.io/en/latest/order-templates.html) | Library docs | read 2026-11-09 | ✓ | SQ3-6, SQ3-7 | Use for the 7-day token limit |
| 6 | [Tradier getting started](https://docs.tradier.com/docs/getting-started), [pricing](https://tradier.com/individuals/pricing) | Broker docs | read 2026-11-09 | ✓ | SQ3-16 to 18 | Fee table is internally inconsistent on SPX; check before relying on it |
| 7 | [Tastytrade sandbox docs](https://developer.tastytrade.com/docs/sandbox) | Broker docs | read 2026-11-09 | ✓ | SQ3-10 | Authoritative for sandbox limits |
| 8 | QuantConnect dataset docs: [US index options](https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/algoseek/us-index-options), [US equity options](https://www.quantconnect.com/docs/v2/writing-algorithms/datasets/algoseek/us-equity-options) | Vendor docs | read 2026-11-09 | ✓ | SQ4-1, SQ4-2 | Authoritative for coverage and start date |
| 9 | [ThetaData pricing](https://thetadata.net/pricing) | Vendor pricing | read 2026-11-09 | ✓ | SQ4-15 to 18 | Prices as of the read date |
| 10 | [Cboe DataShop option quotes](https://datashop.cboe.com/option-quotes) | Exchange data shop | read 2026-11-09 | ✓ | SQ4-20 to 22 | Authoritative; per-dataset prices not captured |
| 11 | [Massive options docs](https://massive.com/docs/options/getting-started) | Vendor docs | read 2026-11-09 | ✓ | SQ4-11, SQ4-12 | Use for the trades-only bar limit; prices not captured |
| 12 | [NautilusTrader options docs](https://nautilustrader.io/docs/latest/concepts/options) | Framework docs | read 2026-11-09 | ✓ | SQ4-9 | Feature list only |
| 13 | [Webull OpenAPI docs](https://developer.webull.com/apis/docs/trade-api/overview) | Broker docs | read 2026-11-09 | ✓ | SQ3-20 | Index-option support not stated |

## Repositories

Strategy repos read in code:

| # | Repo | Stars | Last commit | Status | What it contains | Verdict |
|---|---|---|---|---|---|---|
| 1 | `Darson2004/kelly-event-vol` | 0 | 2026-09-30 | ✓ | Earnings straddle study on real exchange quotes with a cost model; states negative variants. MIT. | Study first |
| 2 | `YichengYang-Ethan/0dte-strategy` | 14 | 2026-04-21 | ✓ | SPX 0DTE research with buy-at-ask, sell-at-bid fills and a log of disproved ideas. No licence file. | Study the method |
| 3 | `randomwalkhan/Short-Term-Reversal-Strategy` | 266 | 2026-11-09 | ✓ | ~30-day call strategy, modelled-price backtest, live paper trade log. "All rights reserved". | Study the paper log; do not reuse code; discount the backtest |
| 4 | `milgar7969/alpaca-options-framework` | 27 | 2026-10-30 | ✓ dashboard and README, ~ PDF | SPY 0DTE paper bot on Alpaca with risk limits; results on an external dashboard. MIT. | Study the execution code |
| 5 | `carolinehutchins05-prog/options-desk` | 0 | 2026-11-09 | ✓ | Call screener with a 10-year modelled-price backtest showing no edge. No licence file. | Negative control |
| 6 | `luphillip041-hub/odte-bot` | 0 | 2026-08-11 | ✓ | 0DTE bot whose author reports no long-premium edge. No licence file. | Read the docs only |
| 7 | `vilkovgr/0dte-strategies` | 63 | 2026-08-26 | ✓ | Replication package for a paper; mixed structures; data not fetchable. MIT. | Skip |
| 8 | `erictao947/earnings-vol-study` | 0 | 2026-06-12 | ✓ | Sells straddles before earnings. No licence file. | Out of scope |

Platform repos:

| # | Repo | Stars | Last commit | Status | What it contains | Verdict |
|---|---|---|---|---|---|---|
| 9 | `alpacahq/alpaca-py` | 1,591 | 2026-11-09 | ~ (API metadata) | Official Alpaca SDK. Apache-2.0. | First choice for paper trading |
| 10 | `ib-api-reloaded/ib_async` | 1,787 | 2025-12-06 | ✓ | Successor to `ib_insync`. BSD-2-Clause. Last push 2026-11-04 to another branch. | First choice for Interactive Brokers |
| 11 | `QuantConnect/Lean` | 22,466 | 2026-11-09 | ✓ docs | Backtest and live engine with bundled option data on the cloud platform. Apache-2.0. | Best single place for a costed options backtest; write a custom fill model |
| 12 | `goldspanlabs/optopsy` | 1,514 | 2026-11-04 | ✓ | Options backtester; needs outside data. AGPL-3.0. | Usable with paid data; note the licence |
| 13 | `alexgolec/schwab-py` | 480 | 2025-08-04 | ✓ | Unofficial Schwab wrapper. MIT. Last push 2026-08-26 to another branch. | Usable; weekly re-login |
| 14 | `tastyware/tastytrade` | 259 | 2026-08-07 | ✓ | Unofficial Tastytrade SDK. MIT. | Usable; weak sandbox |
| 15 | `Lumiwealth/lumibot` | 2,219 | 2026-11-05 | ✓ README, ~ issues | Backtest and live framework. GPL-3.0. | Check the open option-backtest issues first |
| 16 | `nautechsystems/nautilus_trader` | 31,416 | 2026-11-10 | ✓ docs, ~ issues | Trading engine with option instruments. LGPL-3.0. | Heavy; option backtesting has open issues |

## Secondary and practitioner sources

| # | Source | Author/org | Date | Status | Verdict |
|---|---|---|---|---|---|
| 1 | [Earnings straddle backtest](https://www.ivolatility.com/news/3147) | IVolatility | read 2026-11-09 | ✓ | Vendor self-report; large sample; sells its own dashboard |
| 2 | [We stopped trading earnings](https://optionalpha.com/we-stopped-trading-earnings-after-we-saw-this-new-research-188320.html) | Option Alpha | read 2026-11-09 | ✓ | Vendor self-report |
| 3 | [Short put spreads, honest 7-year backtest](https://flashalpha.com/articles/vrp-short-put-spreads-honest-7-year-backtest) | FlashAlpha | read 2026-11-09 | ✓ | Selling strategy; use only for the fill-model point |
| 4 | [Backtesting methodology](https://orats.com/university/backtesting-methodology) | ORATS | read 2026-11-09 | ✓ | Vendor; useful slippage assumptions |
| 5 | [LEAN fill model forum thread](https://www.quantconnect.com/forum/discussion/6981/does-lean-engine-check-for-bid-ask-size-during-backtest-for-option-fill/) | QuantConnect staff | old thread | ✓ | Opinion; may be dated |
| 6 | [Press coverage of the 0DTE paper](https://www.wealthmanagement.com/equities/retail-investors-are-in-love-with-same-day-options) and [CXO Advisory summary](https://www.cxoadvisory.com/?p=44172) | Wealth Management, CXO Advisory | 2023 | ✓ | Superseded by the paper itself |
| 7 | [QuantConnect on Webull](https://www.quantconnect.com/docs/v2//cloud-platform/live-trading/brokerages/webull) | QuantConnect | read 2026-11-09 | ✓ | Third party describing Webull; conflicts with Webull's own docs on index options |
| 8 | [Why your backtest lies](https://dev.to/maymay5692/why-your-backtest-lies-i-got-491-returns-in-testing-then-broke-even-in-production-62a) | dev.to author | read 2026-11-09 | ✓ | Opinion; not options-specific; not used for any finding |

## Screened and excluded

- `davidwang0116/QQQ-LEAPS-CALL-INFINITE-ROLL-BACKTEST` (5 stars), `anti31415/qqq-leaps-strategy`
  (1 star), `Kizo07/LEAPS-Stock-Substitute-Backtest` (0 stars): hold 300–800 days, over the
  3-month limit.
- `Jennycruzy/convex`, `AKzar1el/clockcross`, `ProgramComputer/earnings-trade-automation`:
  debit, vertical or calendar spreads, not pure long.
- `jannissio/delphi-alpaca-agent`, `joncovington/MEICAgent`, `alpacahq/options-wheel`:
  premium selling.
- `rus237sell/trade-algo-v2`, `wheelieinvestor/openclaw-bot`, `trevorgordon981/Agentic-Trader`,
  `kaiuribess/Optedge`: no outcome published.
- `Digantdc/swing-trading-ml`: stock selection with a simplified option overlay; not a
  long-option test.
- `himanshisharmaa/Algo-Trading`, `BeharaPavan-coder/nifty50-algo-trading-bot`: Indian index
  options, outside US stocks and indexes.
- Unreachable or unparsed: Reddit search (403), SSRN, `tastyware.dev`, Databento and
  OptionsDX pricing pages (near-empty), a `cfr-cologne.de` working-paper PDF.
- Not opened: `giordanoshai/alpaca-0DTE`, `Javier-Garzo/ern-wo-options-backtester`,
  `pranay123-stack/ibkr-trading-bots`, `jahanzaib-codes/ibkr-ai-trading-bot-gui`,
  `IlJuniorlI/TradingBot`, `jefrnc/ibkr-odte-strategies`, and five code-search hits listed in
  `notes/SQ8.md`.
