# SQ2 notes: 0DTE / next-day long-option repos with outcomes (as of 2026-11-09; stars and pushed_at read via API 2026-11-09)

**Answer:** Few public repos both buy 0DTE calls/puts and publish an outcome. Only one clearly qualifies as "tried": milgar7969/alpaca-options-framework, with a paper-trading dashboard of 104 trades, 48.1% win rate, +$539 net, simulated fills. YichengYang-Ethan/0dte-strategy is a research repo with a falsification log and backtests, not a profitable bot. The hypothesis (long 0DTE repos with outcomes are rare) is consistent with what I found, but the search was thin (about 11 of 15 calls; many multi-word GitHub queries returned zero results).

## Table (long 0DTE / 1DTE)
| full_name | strategy | underlyings | contract rule | entry/exit | platform | data | outcome artifact | headline numbers (author) | fills modelled | stars | last push (API) | tried? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| milgar7969/alpaca-options-framework | SPY 0DTE "gamma explosion" long call/put, SPY-level stop, peak trail, TP | SPY (ETF) | 0DTE; strike/delta not read (Alpaca returns null Greeks, proxy delta used) | intraday, avg hold 4.7 min, entries ~09:45-11:00 | Alpaca paper | Alpaca 1-min SPY bars + streamed option quotes | dashboard page https://milgar7969.github.io/spy-0dte-dashboard/ ; 22-page PDF manual with post-mortems (PDF not read) | 30d to 2026-11-09: 104 trades, 50W/54L, win 48.1%, net +$539, PF 1.26, EV +$5.18/trade, 14/20 green days (E1) | No: paper simulated fills (E2) | 27 | 2026-10-30 | YES: runnable signals.py (E3) + trade summary. Paper only; ~$5 EV on 5-min holds is fill-sensitive |
| YichengYang-Ethan/0dte-strategy | GEX/Vanna research; current plan long-gamma ATM call/put/butterfly; earlier 1DTE SPY 0.70 delta call swing | SPX/SPY | 0DTE ~0.20 delta call (baseline); 1DTE 0.70 delta | 09:45 entry at ask, 15:55 exit at bid (baseline) | none live | Theta Data 1-min OPRA, 952 days 2022-07 to 2026-04 | docs/validation_summary_2026_04_21.md, logs/, DAILY_LOG.md, GPT_PRO_*.md | Unconditional 0.20 delta call: PF 0.97 no stop, 1.28 with -40% stop (E5); 1DTE long call wrapper ate ~41% of edge (E6); intraday direction baselines "DEAD" | Yes for baseline (ask-in/bid-out) | 14 | 2026-04-21 | PARTIAL: backtest and falsification artifacts, no profitable bot, no live trades. Valuable negative result |
| rus237sell/trade-algo-v2 | "Scalp City" VWAP/50-EMA/ORB 1-min scalper, buys ATM 0DTE call/put, ATR exits, daily +$500/-$1000 halt, flat 15:45 | QQQ, SPY, IWM (ETFs) | 0DTE ATM | 1.5x ATR target, 1.0x ATR stop | Tradier / Alpaca paper | Alpaca free 1-min (~15-min delayed) | none published; trades.jsonl ledger and status.py exist as code | none | unclear (broker reconciliation code) | 1 | 2026-11-09 | NO: README says paper only, no live trades, backtest pending (E7, E8) |
| wheelieinvestor/openclaw-bot | QQQ 0DTE opening-range breakout + VWAP + rel. volume, Claude/Perplexity macro filter | QQQ (ETF) | 0DTE, delta 0.30-0.40, budget <= $250 | signal from 09:50, hard close 12:00, -30% stop, +40% TP1, 25% trail | Public.com API | 6s quote polling; yfinance for backtest | none found (backtest.py exists) | none | limit at ask with retries (E9) | 1 | 2026-03-27 | NO: no outcome artifact found |
| IlJuniorlI/TradingBot | Schwab intraday bot, 14 strategies incl. 0DTE ETF options | ETFs/stocks | not read | not read | Schwab | TradingView screener | none seen in README head | none read | unclear | 10 | 2026-11-09 | UNKNOWN: README head only |
| jahanzaib-codes/ibkr-ai-trading-bot-gui | XGBoost + VWAP/RSI/MACD 0DTE option bot, 3-tier TP ladder | not stated | not read | TP +25/+75/+150% | IBKR | not read | README names milestone2_trade_log.csv and gui_backtest_log.csv as outputs (names only; not confirmed in repo) | none | unclear | 22 | 2026-11-08 | UNKNOWN: no numbers in README |
| jefrnc/ibkr-odte-strategies | 0DTE breakout on high-vol stocks/ETFs plus separate earnings straddle (<=5 days) | stocks, ETFs | not read | not read | IBKR | ib_insync / yfinance | backtest engine code only | none | unclear | 17 | 2026-08-11 | NO: no outcome artifact seen |

## Not pure long / out of scope
- jannissio/delphi-alpaca-agent (0 stars, pushed 2026-09-03): sells same-day SPY iron condors; rejected (sells premium). Its README cites that 0DTE premium selling has about zero expected value after costs.
- joncovington/MEICAgent: iron condors, rejected from description.
- No 0DTE debit-spread repos examined.

## Ranked deep-read candidates
1. milgar7969/alpaca-options-framework: only repo with live-updating trade stats and losing-day post-mortems; check signals.py, risk.py, PDF, and any trade CSV. Fills simulated.
2. YichengYang-Ethan/0dte-strategy: best-documented negative results with ask-in/bid-out fills; GPT_PRO_ROUND3.md, DAILY_LOG.md, logs/.
3. jahanzaib-codes/ibkr-ai-trading-bot-gui: check whether log CSVs and metrics exist (unconfirmed).
4. IlJuniorlI/TradingBot: check CHANGELOG/configs for 0DTE results (unconfirmed).
5. rus237sell/trade-algo-v2: only if a trades.jsonl or results file appears; actively pushed.
6. jefrnc/ibkr-odte-strategies: weak, backtest code only.

## Conflicts
- milgar7969 reports a positive paper result (PF 1.26) while YichengYang's unconditional baseline gives PF 0.97 without stop and 1.28 with a -40% stop (bought at ask, sold at bid, 09:45-15:55 hold, no signal). Setups differ: ~5-min scalps on simulated paper fills vs full-day holds on historical quotes. Neither is live money.
- milgar7969's observe-only ORB shadow filter would have changed P&L by -$52 over 20 days (dashboard), i.e. no benefit shown.

## For SQ1
- YichengYang-Ethan/0dte-strategy tag v1-1dte-archive (1DTE SPY 0.70 delta call EOD-to-next-EOD) is 1DTE and so counts here; flagged for overlap.
- No other multi-day repos met.

## Not found
- Repos reporting abandonment, shutdown or losses for 0DTE long options via GitHub repo search ("lost money", "post-mortem" queries returned nothing). Closest disconfirming item is YichengYang's falsification log.
- GEX-signal repos that buy options with outcomes other than YichengYang (Darthreign/gex-dashboard is a dashboard, not read).
- Code search returned empty for several repos, so file lists are incomplete.

## Blocked
- None blocked. Dashboard figures were fetched 2026-11-09 and will change.

## Search log
1. '0dte options bot' (search): ~15 repos. 2. '0dte calls puts backtest' (search): 0. 3. '0dte scalping SPY options bot': 1. 4. GEX buy calls puts: 0. 5. 0dte lost money abandoned (disconfirm): 0. 6. ORB: 1. 7. ML/LLM: 0. 8. paper results: 0. 9. post-mortem / SPX ML / momentum / journal / backtest queries: 0. 10. LLM agent: 1 (delphi, rejected). Plus README reads, code search, dashboard fetch. Budget used: about 11 of 15.
