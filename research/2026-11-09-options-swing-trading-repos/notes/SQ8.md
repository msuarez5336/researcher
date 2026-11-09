# SQ8 notes (as of 2026-11-09; stars and pushed_at from GitHub API read 2026-11-09)

## Answer
Topic, README and code routes surfaced two new pure-long-option repos with outcome artifacts: randomwalkhan/Short-Term-Reversal-Strategy (call buying, backtest + live paper log) and carolinehutchins05-prog/options-desk (call screen, modeled-price backtest). Lumiwealth/lumibot holds SPY weekly-call backtest artifacts inside a general framework. Most topic hits (0dte, options-trading) were analytics/GEX tools, premium sellers, spreads or Nifty bots.

## New repos (pure long)
| full_name | strategy | underlyings | holding | platform | data | outcome artifact | headline (author-stated) | costs/fills | stars | last push | tried? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| randomwalkhan/Short-Term-Reversal-Strategy | buy near-ATM ~30 DTE calls after large intraday drop; exit ladder +15/+15/-10 | QQQ-filtered universe + SOXL, UPRO, DRAM (mostly ETF, plus some stocks) | short swing (1-10d, inferred from "next few sessions"; not stated exactly) | paper broker (not confirmed; live paper scans) | not confirmed; Black-Scholes used in exit study | results/reversal_3_3/*_trades.csv, *_equity.csv; results/reversal_3_3_live/live_trades.csv, live_equity.csv (links in README, files not opened) | Reversal 3.3 backtest 2025-04-23..2026-04-23: +690.85%, maxDD -26.42%, win 69.23%, Sharpe 4.32; live paper equity $117,024.80 on 2026-11-06 | unclear (live has liquidity gate, spread<=14%) | 266 | 2026-11-09 | yes: code + backtest + live paper log |
| carolinehutchins05-prog/options-desk | daily screen for liquid trend-aligned single-leg calls (45-60 DTE, delta .50-.55), sell in 3-5 days, +50%/-50% | S&P 500 stocks (503); SPY benchmark | short swing (3-5 days) | none (research log, no broker) | yfinance prices; option prices modeled Black-Scholes | backtest/run_backtest.py, results.json; write-up on GitHub Pages | calls near breakeven after costs; trend puts lost; no proven edge | yes (spread cost, modeled prices) | 0 | 2026-11-09 | yes (backtest numbers, but modeled option prices) |
| Lumiwealth/lumibot (docs/research/2026-09-23-alpaca-options-backtests) | SPY weekly call: buy_to_open Mon 09:35, sell_to_close Fri 15:30 | SPY (ETF) | short swing (1-10d, 4-5 days) | Lumibot backtest on Alpaca/Polygon data | Alpaca, Polygon | *_trades.csv, *_trade_events.csv, README.md, settings.json, decisions.txt | not read | CSV shows trade_cost 0.0 and slippage 0.0 in one run; unclear | not read | not read | framework repo; strategy artifacts yes, but it is a general library, borderline |

## Not pure long (separate)
- Jennycruzy/convex: 0DTE SPY, installed profile is a debit vertical; paper, hackathon. Not ranked.
- AKzar1el/clockcross: COIN vertical spreads, 7-21 DTE; hackathon. Not ranked.
- ProgramComputer/earnings-trade-automation: earnings calendar spreads (Alpaca). Not ranked.
- vilkovgr/0dte-strategies: academic SPXW 0DTE package, mixed structures; August 2026 correction says no strategy has positive net Sharpe (E SQ8-9). Context, mostly spreads/short vol.
- Out of scope/seen: darblinko/spy-0dte-spreads, kapilcdave/floor-insurance-bot (credit spreads), pranay123-stack/spx-spy-strategies (credit), Javier-Garzo/ern-wo-options-backtester (ERN/WealthyOption, likely put selling, not read), giordanoshai/alpaca-0DTE (0DTE Alpaca terminal, README not read, candidate for a later check), Nifty/Kite repos.

## Ranked deep-read candidates
1. randomwalkhan/Short-Term-Reversal-Strategy (backtest trades csv + live trades csv; check fills, costs, data source)
2. Lumiwealth/lumibot weekly-call research README and trades CSVs (verify results, costs)
3. carolinehutchins05-prog/options-desk (results.json; modeled prices, near-breakeven)
4. giordanoshai/alpaca-0DTE (unread; check for outcome artifact)

## Conflicts
randomwalkhan reports +690.85% in one year (self-reported, short window, no confirmed cost model); options-desk reports near-breakeven after costs on 10 years with modeled prices; the 0DTE replication reports no positive net Sharpe once costs are fixed. Conditions differ (strategy, window, cost modeling).

## Not found
No qualifying repos from README search with generic phrases (results were noise, mostly empty descriptions and sub-1-star repos). Code search 'reqSecDefOptParams backtest results' returned IBKR repos (coleholt/Earning_CalenderSpread_IBKR_Bot = calendar spread; not pursued). Code search 'filename:trades.csv option call' hit arsencameron/tradingview-backtest, justus-kapst/algo-trading-project (not opened). Did not open lumibot headline numbers or any CSV beyond the first 2024 lines.

## Blocked
None. Code search was accepted. github.com HTML not used. Note: the results README of options-desk backtest was marked thin by fetch_page (still has text).

## Routes
topic:0dte, topic:options-trading, topic:options-strategies, topic:options-backtesting (all sorted by updated): worked, mostly analytics/spreads. README search: low precision. Code search: 'buy_to_open backtest' gave lumibot; 'OptionLegRequest results' gave many Alpaca bot repos (eddiebelaval/Deepstack, eljo5115/options_trader, Rohan5commit/options-trading-bot, mehpackers13/options-bot, not opened).

## Search log (tool calls: 8 of 10; Bash batches counted as one call each)
1. topic searches x4 (search): ~12 new repos relevant. 2. README searches x2 + code x2 (search): 4 new. 3. Fetch 6 READMEs: 4 read in detail. 4. README searches x4, repo metadata x2, code x2 (search): lumibot CSVs, little else. 5. Fetch result READMEs/CSV. 6. Grep cached README. 7. Print cached heads. 8. lumibot code listing. No disconfirm-specific search; disconfirm evidence came from vilkovgr and options-desk results.
