# SQ2 notes (as of 2026-11-07; 13 of 15 calls used)

## Answer
Pre-FOMC drift was large in 1994-2011 (>80% of equity premium, SQ2-1) but essentially vanished after 2015 (SQ2-2), though other work says it is uncertainty-conditional (search snippets only). Index straddles lose on average around macro releases except FOMC, where returns are positive in OptionMetrics' summary (SQ2-4): FOMC is the only candidate for "realised beats implied"; CPI/payroll evidence is thin. GEX sign is mechanically related to RV but adds ~nothing beyond VIX/ATM IV in one vendor backtest (SQ2-6).

## Findings
- [E] Drift 1994-2011 large; no later reversal in LM tests (SQ2-1, SQ2-3).
- [E] Drift gone after 2015 (SQ2-2).
- [E] Straddle returns negative on macro days, positive on FOMC (SQ2-4); paper's sample not seen.
- [E] FOMC-day intraday reversal strategy, 0.18% net/event, SR 0.36 (SQ2-5, secondary).
- [E] GEX: -0.36 raw, -0.03 controlled (SQ2-6; vendor, unreviewed).
- [O/unverified, search snippets only, not cached]: Fed IFDP 1376 (downside risk higher for options spanning CPI/FOMC/NFP/GDP; premia tied to inflation uncertainty); Wright NBER w28306 (VRP positive on FOMC days); Nasdaq article (1-day NDX straddle overpriced 10 of 12 FOMC); SSRN 4131740 (~60% of 4-day post-FOMC return reverses before next meeting; 3-day return predicts reversal over 4-30 days, R2~7%); Martineau (reversal ~60bp, none without press conference); Gurkaynak-Kurov-Wolfe (relief rallies after FOMC); OptionMetrics DOOD (gamma predicts overnight gaps only in low VIX); Ni-Pearson-Poteshman-White RFS 2021 (negative gamma amplifies vol; abstract-level); Dalvi-LaFond NYU (short-dated volume share vs term structure); Ignatieva-Ohashi Appl. Econ. 2025 (drift still found); Martello-Ribeiro (drift in high-uncertainty periods).

## Conflicts
Kurov et al. (drift gone after 2015) vs Ignatieva-Ohashi 2025 and Liberty Street 2018 post (drift ~40bp persists on press-conference days) - differ by sample/definition; second not verified. Post-FOMC: reversal (SSRN 4131740, Martineau) vs positive relief rallies (Gurkaynak et al.). OptionMetrics (FOMC straddle positive) vs Nasdaq (FOMC straddle overpriced) - differ by sample/period.

## Not found
CPI/payroll continuation vs reversal; OpEx/index rebalance effects on realised vs implied; direct measurement of 0DTE effect on event-day pricing (only VIX1D anecdotes; McMillan: VIX1D usually a bit above realised range); gamma-regime momentum vs reversal.

## Data sources found
- Cboe VIX1D (launched 2023-04 per search snippet), VIX9D; SqueezeMetrics GEX; Fed FOMC calendar (not fetched).
- Reachable history of CPI/payroll release dates: NOT found (no fetch attempted; bls.gov 403).

## Blocked
papers.ssrn.com (known), skidmore.edu PDF 404, nasdaq.com unreachable; PDFs unsupported by fetch_page (federalreserve.gov IFDP, nber.org w28306, newyorkfed sr512, ou.edu, keio).

## Search log
1 pre-FOMC drift disappeared (disconfirm): 4 sources. 2 implied vol FOMC/CPI/payroll straddle: 5. 3 GEX predictive power (disconfirm): 3. 4 Lucca Moench NY Fed: 2. 5 0DTE FOMC VIX1D: 2. 6 Ni et al gamma: 1. 7 post-FOMC continuation/reversal: 4.
