# SQ1 notes (as of 2026-11-09). Stars and last push from GitHub search API read 2026-11-09. Evidence ids in brackets.

## Answer
Long-option swing repos with a published outcome exist but are few and mostly tiny (0-5 stars), recent (2026), and mostly BSM-model or event-study research, not live trading. The only one that models real option quotes and costs is Darson2004/kelly-event-vol (long straddle, T-14 before earnings). No repo found with a live or paper trade log. The hypothesis (rare, many without outcomes) holds for this search, which covered about 25 repos from short-query GitHub searches only.

## Table (long option, qualifying or near-qualifying)
| full_name | idea | underlyings | holding | contract rule | platform/data | outcome artifact | headline (author's) | costs | stars | last push | tried? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Darson2004/kelly-event-vol | Long ATM straddle before earnings, Kelly sizing | 42 liquid US stocks (971 events; 1,051 small/mid caps) | short swing (T-14 to pre-print) | ATM straddle, entry T-14/7/3 | OPRA quotes (Databento tcbbo) backtest | results/liquid_2020_2026/T14/summary.json, trades.csv, README table | +6.39%/trade net (n=193, t=2.65); T-7 only +0.24%; median trade -4.9% [1,2] | yes (half-spread + $0.75/contract; measured fills) [3] | 0 | 2026-09-30 | yes: code + backtest on real quotes, honest negatives |
| davidwang0116/QQQ-LEAPS-CALL-INFINITE-ROLL-BACKTEST | Buy QQQ LEAPS calls on 1% gap-down, harvest at delta 0.90, roll | QQQ (ETF) | long swing to long (650-800 DTE, roll at 300) | delta 0.70, DTE 650-800 | Yahoo CSV, BSM/MJD modelled prices | README tables, trade CSVs (qqq_leaps_trades_2020_BSM.csv), trade report md | 2010 start 54.54% CAGR vs 18.61%, MaxDD -74.6%; 2000 start MaxDD -100% [4,5] | unclear (modelled prices) | 5 | 2026-04-21 | yes (modelled, not real chains); holding is over 8 weeks so borderline scope |
| anti31415/qqq-leaps-strategy | RSI<35 + VIX spike buy QQQ LEAPS; Alpaca paper scaffold | QQQ (ETF) | long (about 730 DTE) | delta 0.70 | BS approximation; Alpaca paper scaffold in autotrade/ | backtest_results.md; dte_v1_analysis/ | 15/15 winners, 12.41% annualized, MaxDD -32.97% [6,7] | unclear | 1 | 2026-08-26 | yes (backtest only; paper scaffold has no log seen); 15 trades; over 8 weeks |
| Kizo07/LEAPS-Stock-Substitute-Backtest | LEAPS replacing stock in long/short equity | equities | long | not read | BS on spot, IV proxy | results/ CSVs, 7 research notebooks | V1 -30.1% CAGR vs V0 -6.7%; Sharpe -1.09 [8] | partly (financing, early-exercise premium) | 0 | 2026-09-04 | yes, negative result; mixed long/short book, over 8 weeks |
| Digantdc/swing-trading-ml | 21-day ML stock picks + options overlay | AI/semis stocks | short/long swing (21d) | rule-based selector, simplified BS | yfinance | results/RESULTS.md | Sharpe 1.12 < SMH hold 1.23; "sector beta, not alpha" [9] | stock costs 15bps+10bps; options P&L simplified | 2 | 2026-06-16 | partial: outcome is for the stock model, options overlay mixes strategies incl. iron condor |
| ArnMehta11/Equity_Volatility_Strategy | Long/short ATM straddle around earnings, FOMC, geopolitics | S&P 500 + sector ETFs 2016-2025 | short swing (entry T-3..T+0, exit T+0..T+3) | ATM, delta 0.375-0.625 filters | Polygon.io | README gives method; no headline numbers seen in README (results dir not checked) | none read | unclear | 2 | 2026-05-01 | unclear (long/short both ways; outcome not seen) |

## Signal/dashboard or no outcome (not "tried")
- trevorgordon981/Agentic-Trader (s=4, push 2026-10-09): LLM options swing system, sanitized export, "nothing in this repository claims a return" [10]. No.
- kaiuribess/Optedge (s=3, push 2026-08-02): swing cockpit, 90+ DTE and 365-900 DTE LEAPS lanes, Robinhood review; synthetic/paper-only, no results [11]. No.
- bkinder4243-lang/Screen-Test (s=0, 2026-05-06): long call/put swing screener, Polygon; README has no results, roadmap phases. No.
- olenny-coder/swing-trading-picks, loopnestdev/signal-dashboard, dmitridefreitas-dev/thesis-radar, simonro/ai-research-desk, moneysignalai/prime-flow-ai, Navstertheboi/unusual-options-bot (alerts/paper+SMS), vivaandev/kestrel (journal tool): signal/dashboard/tool, not read, no outcome indicated by description. No.
- erictao947/earnings-vol-study (s=0, 2026-06-12): description says straddle backtest with transaction costs, 639 events, 54 stocks; README not reachable at HEAD/README.md or readme.md (404). Unverified, worth a look. Similar: unniananya/Earnings-Implied-Move-Mispricing (not read).
- archit-stark/Momentum-Strategy (streamlit signals to go long/short the option), DevPradhan/vol_ml (NSE index long CE/PE ML): not read.

## Not pure long / rejected
- Debit/credit or mixed: amitvashis/Option_Strategy (short straddles and calendars) rejected, sells premium.
- Indian NSE (Nifty) option-buying: himanshisharmaa/Algo-Trading (intraday bullish swing, Nifty, not US stocks/index in brief, intraday), BeharaPavan-coder/nifty50-algo-trading-bot (intraday). Index options but intraday; not read.
- deshwalmahesh/NSE-Stock-Scanner, ivrwealth-ui/trading-library: screener / books.
- Pure library or crypto: P0ntix/leapspace-quant (memecoins), NathanCarr10/TNS-Capital (unrelated).
- lorenz-liu/leaps-backtesting, shyamvaidhyanathan/leaps_options_backtester, zhouhowe/PortfolioOptimizer: LEAPS backtesters not read; may deserve a look.

## Ranked deep-read candidates
1. Darson2004/kelly-event-vol: only one with real quotes, measured fills, pre-registered sweep, and negative results stated; short swing.
2. davidwang0116/QQQ-LEAPS-CALL-INFINITE-ROLL-BACKTEST: full trade logs and CSVs, 5 stars; check pricing realism and the -100% drawdown (ETF, long hold).
3. Kizo07/LEAPS-Stock-Substitute-Backtest: negative result with notebooks and CSVs.
4. anti31415/qqq-leaps-strategy: has Alpaca paper scaffold and EOD option-chain study; check for actual paper trades (15 trades is a tiny sample).
5. erictao947/earnings-vol-study: costs-included straddle study; locate its files.
6. ArnMehta11/Equity_Volatility_Strategy: check results dir for numbers.

## For SQ2
himanshisharmaa/Algo-Trading, BeharaPavan-coder/nifty50-algo-trading-bot (intraday Nifty), luphillip041-hub/odte-bot (0DTE Alpaca), pranay123-stack/ibkr-trading-bots (SPX 0DTE).

## Conflicts
- Convention of "edge": Darson2004 finds +6.39%/trade only under one filter and only at T-14 and only in liquid names; ArnMehta11/Digantdc make no net claim. LEAPS repos (davidwang0116 54% CAGR, anti31415 100% win rate) use modelled BSM prices and look much better than Kizo07's costed LEAPS result (-30.1% CAGR); they differ in setup (long-only QQQ dip-buying vs long/short stock substitute) and pricing realism, so they are not directly comparable.

## Not found
No repo with a live or paper trade log for bought calls/puts on a swing horizon. No momentum or breakout call-buying repo with results. No unusual-options-activity follower with a backtest. No post-mortem or shutdown repo specific to option buying (the losses search with "swing" returned nothing); Kizo07, Digantdc and Darson2004 are the nearest negative results.

## Blocked
github.com HTML not used. erictao947/earnings-vol-study README 404 on raw URL. GitHub repo search returned empty for long (6+ word) queries; short queries worked. Only top-10-by-stars results seen per query, so coverage is partial. Stars/push dates not verified against commits. All evidence graded B (README self-reports); the verified flag means quote found in cached page.

## Search log (10 tool calls used before writing; 11 with this file counted separately: 3 empty long-query searches, then short ones)
- 5 long queries (swing/LEAPS/straddle/UOA/delta-DTE): 0 results (search).
- 3 long queries incl. losses/abandoned (disconfirm): 0 results.
- 7 short queries (options swing trading, swing trading long calls, LEAPS backtest, straddle earnings backtest, momentum, UOA bot, alpaca): about 20 new repos.
- Cache 10 READMEs: 9 ok, 1 404.
- Grep results + backtest_results.md fetch: 1 new artifact.
- 6 short loss/journal/overnight queries (disconfirm): 2 new repos, none relevant.
- 5 short queries (flow, earnings straddle, ML, overnight, breakout): 4 new, mostly 0DTE/Indian.
