# SQ2 notes (as of 2026-11-06)

*Answer:* Muravyev & Pearson (RFS 2020) is the origin of H1: timing traders pay <40% of conventional effective spread, average trader about 25% less. The summary thread says conventional effective spread is ~80% of quoted (0.8 of full quoted spread, i.e. 0.4 of half-spread... see conflict). Retail and multi-leg fills were not measured by any source I could verify. Recommended base k=0.65-0.75 is not contradicted, but k=0.5 is defensible only for timing/sophisticated flow. Keep k=1.0 as stress. Cost ~ $0.65 commission + ~$0.05-0.10 fees per contract.

## Fill-evidence table
| Source | Measure | Number | Setup | Period | Id |
|---|---|---|---|---|---|
| Muravyev & Pearson, RFS 33(11) 2020 (A) | effective spread, timers vs conventional | <40% of conventional; avg 25% lower | US equity options, high-frequency quotes | see paper (not retrieved) | SQ2-1 |
| Thread summary of same paper (C) | conventional effective/quoted | ~80% | midpoint-based | same | SQ2-2 |
| AEA 2023 abstract (search snippet only, unverified) | auction price improvement | 50.42% of half spread | option auctions | unknown | none |

## Fee table (date seen 2026-11-06)
| Broker/fee | $/contract | Id |
|---|---|---|
| IBKR Pro tiered, <=10k/mo | 0.65 (min $1/order); 0.25-0.50 lower tiers | 3 |
| IBKR OCC clearing | 0.025 | 4 |
| IBKR CAT | 0.0003 | 3 |
| Fidelity | 0.65 (+0.50 if Professional Options Trader) | 5 |
| tastytrade | 1.00 open, cap $10/leg, $0 close | 6 |
| Robinhood | 0 commission; combined OCC/ORF pass-through 0.04; CAT 0.0003 | 9 |
| Schwab | 0.65 (search snippets only, page was thin; unverified) | none |
| FINRA TAF (sells) | 0.00329 for 2026, paused 2026-10-01 to 12-31 | 8, 10 |
| SEC Sec.31 (sells) | $20.60 per $1M principal since 2026-04-04 (~$0.0000206 x value) | 7 |
| ORF | exchange-specific; search snippets show roughly 0.0014-0.02 per side, changed 2026-07-01 (not verified) | none |

## Recommendation
k base 0.70 (keep 0.65-0.75), stress 1.0, add optional k=0.5 optimistic case. Wide-spread names and multi-leg should use k>=0.8 (no evidence; judgement). Cost: commission 0.65 plus about 0.05 regulatory/clearing (OCC 0.025 + ORF ~0.01-0.02 + CAT) = ~$0.70/contract per side; pro accounts at Fidelity $1.15. SEC fee on sells ~ $2.06 per $100k premium; trivial.

*Conflicts:* the "80% of quoted" figure is from a secondary thread; if effective spread is defined as 2x|price-mid| the ratio is relative to the full quoted spread, so the k for average trade is ~0.8 under conventional measure and ~0.6 after one-quarter reduction. This supports k=0.65-0.75 for average flow only. ORF figures vary by exchange.
*Not found:* retail- or multi-leg-specific realised/quoted ratios (Bogousslavsky-Muravyev "Anatomy of Retail Option Trading" not retrieved); evidence retail fills worse than mid; OCC fee schedule (OCC host reset); Schwab verified page; FINRA SR-2026-021 PDF (unsupported); Robinhood-US ORF details.
*Blocked:* core.ac.uk 403; optionsclearing.com reset; finra section-1 404; PDFs unsupported by fetch script; schwab.com thin.
*Search log:* M&P paper (search, 3 new); multi-leg price improvement (search, vendor material only); ORF 2026 (search, exchange filings); retail worse than mid (disconfirm, 1 working paper); TAF/OCC/SEC (search); Bogousslavsky (search, nothing new); Schwab (search). Budget used about 13 of 15.
