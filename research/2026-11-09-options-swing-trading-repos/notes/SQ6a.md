# SQ6a notes (as of 2026-11-09; shallow clones in pages/clones/, nothing run)

Answer: Of four repos, only kelly-event-vol and Short-Term-Reversal-Strategy (and, with modelled prices, options-desk) buy options to open. earnings-vol-study SELLS straddles (out of scope). Only kelly-event-vol tests on real quotes with explicit costs; the other two use Black-Scholes modelled prices.

## Darson2004/kelly-event-vol  [long straddle, short-swing/long-swing boundary]
- Practices: buys ATM straddle at T-14 (also T-7, T-3), exits last close before the print (event_bt/engine.py ~L298-305); signal ratio_avg_rm <= 0.90 (README); fills at mid +/- phi*half-spread, phi=0.5, plus $0.75/contract/side, 4 sides round trip (engine.py L397-436); Kelly sizing (docs/KELLY_RESEARCH.md); data = Databento OPRA cbbo-1m 15:44-15:48 ET (README, event_bt/DATA_SPEC.md). Holding 14 days -> label long swing (>10 days) at T-14; T-7 variant short swing.
- Results [E]: +6.39%/trade net, n=193, t=2.65, 42 liquid names, 971 events, 2020-09..2026-08, 5 of 6 years positive (SQ6a-1). T-7: +0.24% (SQ6a-2). Walk-forward model +0.01%. Small caps -17.3% net. Median trade -4.9%; top decile = 36% of abs P&L. Files: results/liquid_2020_2026/T14/*.csv, T7/. No drawdown or benchmark given.
- Realism gaps: exit-leg fill unmeasured, flips at phi 0.605 (SQ6a-3); liquid panel seen in aggregate before signal hunt (descriptive-only); sealed holdout unopened and not in repo; synthetic selftest check 6 fails at default size (README).
- Tried: yes (code + results CSVs + tcbbo fill study). Last commit 2026-09-30. Licence MIT.
- Verdict: STUDY (best-evidenced; honest negatives).

## randomwalkhan/Short-Term-Reversal-Strategy  [long calls, short swing]
- Practices: near-ATM calls ~30 DTE (TRADING_DTE_AT_ENTRY=30, SQ6a-6), exits +10%/+15% take-profit, -10% stop (backtest_reversal_2_4_calls.py L29-31, SQ6a-7); live uses +15/+15/-10 (README); filters: 60d lookback, matched_signals>=10, drop>0.5%, trailing P/E<140, trend gate, timing score 0.5 (README). Live paper adds liquidity gate OI>=110, vol>=20, spread<=14% (README 3.4.4). Option price in backtest = bs_call with sigma from "Sigma Ann" (fallback 0.60) (SQ6a-5); I found no commission/slippage/spread term in the backtest scripts (rg on 2_4 and 3_3 scripts). Backtest holds via day-1/day-2 targets -> short swing.
- Results [E]: reversal_3_3_official: +690.85% total, max DD -26.42%, 117 trades, win 69.2% (SQ6a-4). No period stated in the summary row; no benchmark. Live paper log: results/reversal_3_3_live/live_trades.csv (134 rows) with fills from contract symbols, e.g. AVGO 2026-03-24 to 03-26, -11.9%; the live dashboard shows equity $117,024.80 on 2026-11-06 (README; live paper only, start capital not read).
- Realism gaps: backtest on modelled BS prices with no spread cost; strategy parameters evolved over ~20 versions on the same history (self-flagged overfit scripts exist: analyze_reversal_2_4_overfitting.py, RESEARCH_GUARDRAILS.md); +690.85% is not comparable to live.
- Tried: yes (code, trade CSVs, live log). Last commit 2026-11-09. Licence: "All rights reserved" (LICENSE), so no reuse rights.
- Verdict: STUDY (live log and overfit checks); do not reuse code.

## carolinehutchins05-prog/options-desk  [long calls/puts, short swing]
- Practices: call signal = close above rising 50d MA, RSI(14) 45-70, no 52w high in last 3 sessions; contract delta 0.55, 30 calendar DTE (45 sensitivity), IV proxy <40%, break-even within 3% of spot, theta<5%/day; entry next open; exit first close at +50% else close of 5th session; 2% half-spread each way (backtest/run_backtest.py docstring, SQ6a-8, 9). Brief said 45-60 DTE: the backtest uses 30 (45 as sensitivity); 45-60 not confirmed in backtest code.
- Results [E]: 503 stocks, 2015-06-01..2026-10-26; calls screen n=117,754, mean -0.37% per trade, median -7.4%, win 45.2%, target hit 26.4%, 95% CI [-2.7%, +1.9%], no better than all-stock-days (edge -0.02%) (backtest/results.json). SPY buy-and-hold total return 3.53 (353%). "Near breakeven" confirmed; the repo itself says "after costs the calls break even and the puts lose" (research/backtest.md).
- Realism gaps: BS prices from 30d realised vol, constant IV, no crush/expansion; survivorship (SQ6a-10); spread/OI/volume/earnings gates not tested. Rest of repo is a daily web board (publish.sh, archive/*verdict.md), not a trade log; no fills found.
- Tried: backtest yes (negative result); live log no. Last commit 2026-11-09. Licence: none found in clone.
- Verdict: STUDY as an honest negative control; skip for edge.

## erictao947/earnings-vol-study  [SELLS straddles: out of scope]
- phase7_backtest.py sells an ATM straddle before earnings and buys it back after (SQ6a-11). Stopped here. Data: DoltHub; 164 usable events of 639 attempted; results: mid +0.70%, half-spread +0.23%, full-spread -0.24% per event (data/backtest_results.json) - these are short-vol returns, not long-option evidence. Last commit 2026-06-12. No licence file.
- Verdict: SKIP (premium-selling).

## Conflicts
- Reversal +690.85% (modelled prices, no spread) vs options-desk modelled calls ~-0.4%/trade after 2% half-spread: costs and rule differ, neither on real quotes. kelly is the only real-quote test.

## Not found
- Reversal backtest period/dates and benchmark; live start capital; options-desk delta/DTE 45-60 in code; kelly drawdown/benchmark.

## Blocked
- None. (github.com HTML not used; raw.githubusercontent.com worked; fetch_page marked reversal summary CSV "thin" but text matched.)

## Search log
- No web searches; 11 tool calls: clones, repo reads via rg/head, one fetch_page batch, one quote-check grep, one write.
