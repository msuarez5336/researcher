# SQ6b notes (as of 2026-11-09; clones in RUN/pages/clones/, shallow, blobless)

## Answer
All four are 0DTE ETF/index repos. Two buy options to open (alpaca-options-framework, odte-bot); one is a research log that tests a long 0.20-delta call (0dte-strategy); one is a paper replication with mixed multi-leg structures (0dte-strategies). None shows a positive, realistically costed options result. Study 0dte-strategy and odte-bot docs for the negative evidence. Use alpaca-options-framework only for execution engineering.

## alpaca-options-framework (0DTE, ETF: SPY) - verdict: study (execution/engineering), skip as an edge
- Last commit 2026-10-30. Licence MIT.
- Buys calls/puts to open. Single-leg limit buy (orders.py:50-68), mid + 2% buffer, 30 s fill timeout, per PDF. [E]
- Entry (config.py:20-35): 09:45-12:00 ET, 3 consecutive 1-min bars in one direction, ROC5 >= 0.0003, ATR5 >= 0.20, strike-proximity zones. The signal itself lives in signals.py/momentum.py.
- Contract: strikes at SPY +/- min(0.6 x 5-day ATR, $4.50), OTM, option price $0.20-$10 (config.py:14-25, strikes.py).
- Exits (config.py:56-74): stop 0.50 x entry, take-profit 1.5 x, peak trail at 88% once +20%, SPY-level ATR stop, time stop 15:25.
- Sizing and risk: $150 risk per trade, $300 daily loss limit, $125 daily profit lock, stop entries after 3 wins in a row (config.py:43-53). No IV, earnings or VIX filter found.
- Results: the PDF (22 pp, July 2026) lists daily paper P&L, 2026-05-20 to 06-17. Clean total -$121, raw +$1,007 (nearly all from one 06-04 ghost-position anomaly) [E, SQ6b-2, verified=false: read from local PDF]. The README's dashboard (104 trades, PF 1.26) is on an external site, not in the repo. No trade CSV in the clone: **results not in repo**. The 104 trades and PF 1.26 are unverified.
- Realism gaps: paper fills on Alpaca, no backtest, parameters tuned live (e.g. noon cutoff set from July losses, SQ6b-1), no commissions modelled, lots of overfit-by-iteration risk. Shadow-mode "twins" (exit_shadow.py, gate_shadow.py) are a good idea but share the same fill model.
- Tried status: runnable code plus post-mortem PDF = tried, but the net outcome is slightly negative.

## 0dte-strategy (0DTE, SPX/SPY; 1DTE archive in tag v1-1dte-archive, not read) - verdict: study (falsification method)
- Last commit 2026-04-21. No LICENSE file found in the clone root.
- Active R0 design is "long gamma" (ATM call/put/butterfly), but per its own docs the R0 was killed (docs/R0_RIP_2026_04_21.md, r0_post_mortem exist; not read in detail). Sell-vol branch archived.
- The PF claim is confirmed in docs/validation_summary_2026_04_21.md: 951 days, pick call with |delta| about 0.20 at 09:45 ET, buy at ask, exit 15:55 bid or stop; no stop WR 18.7% PF 0.97; -40% stop WR 9.7% PF 1.28 with 89.8% stopped; -60% PF 1.11 [E, SQ6b-3, SQ6b-4]. This is an unconditional mechanical baseline, with no signal, so it is not a strategy result. Commissions and any out-of-sample split not seen.
- Realism: ask-in/bid-out is conservative; historical quotes. The stop is checked on what granularity is unknown (not read).
- Results artifacts present: logs/*.md and *.json (baseline reports, intraday day 1-3, R0 checks). README says daily/overnight and intraday MVP "falsified".
- Tried status: yes (runnable, many outcome logs), outcome negative or unconditional only.

## 0dte-strategies (vilkovgr; 0DTE, SPX index via SPXW) - verdict: skip as a trading repo; study as cost-bug cautionary tale
- Last commit 2026-08-26. Licence MIT (Grigory Vilkov).
- It is a paper replication package, not a bot. Seven standard structures: strangle/straddle (long), iron fly/condor (short), risk reversal, put ratio, spreads (docs/agent-context/strategies.md). So it is mixed long and short, not pure long. Only the strangle/straddle is pure long: net Sharpe -0.97 after the fix [E, SQ6b-5].
- Bug: half-spread charged at 1/100 of true size; after the fix "no strategy or basket retains a positive net Sharpe" (README). Gross numbers also moved. Data panels in Git LFS; budget exceeded, so data cannot be fetched. The paper PDF and docs are being revised.
- Realism: 30-minute resolution, bid-ask plus 0.5 bp fee; Cboe data proprietary and not shipped.

## odte-bot (0DTE, ETF: SPY/QQQ) - verdict: study the docs (11 waves of negative results); skip the bot
- Last commit 2026-08-11. No LICENSE file found.
- Buys 0DTE calls/puts (README "How it works"): VWAP + EMA9/21 + RSI signal, |delta| about 0.25 (fallback 0.25-0.40), spread <= 10% of mid, OI > 100; entries 09:35-15:30, max 2 positions, 3% daily-loss halt; exits +50% TP, -40% SL, 15:50 flat. Sizing by equity x risk%. The README says ADX is used in the equity-mode L2 test, not clearly in the options entry; the chop gate claim is partly unconfirmed. Credit-spread mode (spreads.py) also exists: sells premium, out of scope.
- Backtest (backtest.py:46,262,336-359): Black-Scholes with constant IV, 10% slippage each side; real option bars used to re-price (`--validate-options`). docs/backtest_report_v10.md and v10_audit.md: all long-option hypotheses rejected, most cells negative in train and test at 10% fill. The README says "Eleven research waves found no long-premium options edge" [E-ish, SQ6b-6]. The only winner is Monday long shares (+3.7% SPY / +5.5% QQQ test, 2024-01 to 2026-08, 38 test trades each), which is not options.
- Tried status: yes, with reports; outcome negative for options. Not live-tested.

## Conflicts
- alpaca-options-framework README shows PF 1.26 on an external dashboard, but its own PDF shows -$121 clean over 17 sessions. Different windows probably (dashboard unseen), so unresolved.
- 0dte-strategy PF 1.28 (with -40% stop) vs 0.97 (no stop): same trades, stop-dependent; WR drops to 9.7%.

## Not found
- Dashboard data and trade CSV (alpaca); 1DTE archive tag contents (not read); full verification of odte-bot options-trade counts; vilkov per-structure long-only subset beyond strangle/straddle; licence file for 0dte-strategy and odte-bot.

## Blocked
- None. Note: two early bash reads hit a wrong cd and returned the toolkit README; redone with absolute paths. github.com HTML and the external dashboard were not fetched.

## Search log
- No web searches. 12 tool calls on clones, rg and pdftotext reads, 1 fetch_page (4 raw files), 1 evidence write.
