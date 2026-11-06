# Spec review: options swing-trade backtest instructions (v1 → v2)

As of 2026-11-06. This review checks the user's 5-phase spec on three questions: is anything
missing that a backtest cannot run without, does any rule contradict another, and is any rule
unnecessary? Items marked **[verify SQn]** depend on facts the research run checks. The final
spec in `report.md` uses the verified values.

## Verdict
The structure holds. Most rules belong. Cut 4 items, fix 7 inconsistencies, and add 6 missing
items. Without the additions the backtest can't produce an equity curve or a pass/fail decision.

## Cut (not needed or never fires)
| # | Item | Why cut |
|---|---|---|
| C1 | Phase 4 pin-risk rule "force-close on expiration Friday" | The 21-DTE time stop closes every position long before expiry, so this rule never fires. Keep one assertion in code (`assert dte_at_exit >= 21`) instead of a rule. |
| C2 | Phase 1 "sells premium (credit spreads, iron condors)" as an option in the same test | Phase 3 has no strike, width or management rules for short premium. Test one archetype per hypothesis: v2 = long premium / debit spreads. A credit-spread test needs its own rule set (short Δ, width, max loss) and is a separate hypothesis. |
| C3 | Phase 2 "OPRA" listed as a provider | OPRA is the consolidated feed that vendors redistribute, not a data provider. List vendors only. **[verify SQ1]** |
| C4 | Phase 2 intro rhetoric ("Most retail backtests fail…") and Phase 3 "Unlike stock trading…" | Explanation, not a rule. Move it to a one-line rationale. |

## Fix (internal contradictions)
| # | Problem | Fix |
|---|---|---|
| F1 | Entry at **30** DTE plus time stop at **DTE < 21** leaves only ~9 calendar days, but the hold is up to 10–15 trading days (~14–21 calendar days). | Entry window **35–60 DTE** (target 45). A 10-trading-day hold (~14 calendar days) from the 35-DTE floor ends at about 21 DTE, so the two stops coincide. From the 45-DTE target it ends at about 31 DTE, so the full hold fits. Whichever stop fires first wins. |
| F2 | Horizon given three ways: 3–15 days (Phase 1), "5–10 day swing" (Phase 3), "10 days" (Phase 4). | One number: max hold **10 trading days**. The signal's expected horizon is 3–10. |
| F3 | Fill rule is self-contradictory: "mid minus 25–50% of spread" ≠ "65–75% of the spread from the bid". | Buys fill at **bid + k·(ask−bid)** and sells at **ask − k·(ask−bid)**, with base k = 0.65–0.75 (mid + 15–25% of spread) and a stress test at k = 1.0 (full spread). Apply k **per leg** for spreads. **[verify SQ2]** |
| F4 | "Walk-forward" is used for a single 60/40 split. Those are different methods, and a single chronological split may leave a whole regime (e.g. 2020 crash) in-sample only. | Rolling or anchored walk-forward windows (e.g. 3y train / 1y test, stepping 1y), **plus** one final untouched holdout. Name the regimes each window covers. **[verify SQ3]** |
| F5 | Execution "15 min after the open / before the close" needs **intraday** quotes, but Phase 2 allows EOD data. | If the data is EOD, execute at the vendor's snapshot time (record it). Intraday timing rules apply only with intraday NBBO. **[verify SQ1: snapshot times]** |
| F6 | Phase 2 requires vendor Greeks *or* a model, but leaves the choice open. Some vendors may not ship historical Greeks at all. | Use vendor IV/Greeks where they exist. Otherwise compute with one named model (Bjerksund-Stensland 2002 for American) **with a named rate curve and dividend inputs**. Never mix the two. **[verify SQ1]** |
| F7 | Profit target "50% of max profit **or** +35% option value" mixes two structures. | Debit spread: 50% of max profit. Long single option: +35% premium (test 25/35/50 in the sensitivity grid). |

## Add (missing, the backtest can't run or can't be judged without them)
| # | Missing item | Add |
|---|---|---|
| A1 | **Falsifiable pass/fail criteria**, written before running | e.g. OOS expectancy > 0 after costs at k = 1.0, profit factor ≥ 1.3, ≥ 100 OOS trades (30 absolute minimum), max drawdown ≤ X%, positive in ≥ 2 of 3 regimes. **[verify SQ3: trade-count and overfitting guidance]** |
| A2 | **Position sizing and portfolio rules** | Risk a fixed % of equity at max loss per trade (debit paid), max concurrent positions, and max per underlying. Without these there is no equity curve and no drawdown figure. |
| A3 | **Baseline / control** | Run the same signal on the underlying shares, with the same holding rules. If the options version doesn't beat the share version after costs, the option structure adds nothing. |
| A4 | **Multiple-testing control** | Log every configuration tried. Report a deflated Sharpe ratio or the probability of backtest overfitting (PBO), not the best cell. **[verify SQ3]** |
| A5 | **Point-in-time universe and data hygiene** | Use historical index membership (not today's S&P 500) and unadjusted underlying prices for strike/Δ maths. Exclude non-standard (corporate-action-adjusted) contracts. Open interest (OI) is known only as of the prior day. **[verify SQ1]** |
| A6 | **Exit evaluation and gap handling** | Say when exits are checked (EOD snapshot or intraday), which exit wins if two fire on the same bar (Event > Stop > Time > Profit), and that a gap through the stop fills at the next available quote, not at the stop level. Add a hard max loss on the option (e.g. −50% premium) as a backstop to the underlying-based stop. |

## Keep (sound as written)
Liquidity universe; catalyst list; Δ/DTE coordinates instead of fixed strikes; 0.60–0.70Δ single
leg or 0.50/0.25Δ debit vertical; spread ≤ 5–8% of mid and OI ≥ 500; signal vs execution
separation; underlying-based stop; event stop before earnings; ex-dividend force-close of ITM short
calls **[verify SQ3: exact early-exercise condition]**; per-contract commissions **[verify SQ2]**;
parameter-sensitivity surface.
