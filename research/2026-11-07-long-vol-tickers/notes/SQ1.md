# SQ1 notes (as of 2026-11-07). Budget: 14 of 15 calls used.

## Answer
Long single options/straddles have on average NOT had positive expected returns: delta-hedged long option returns are negative on average (Cao & Han, 1996-2009: long ATM delta-hedged calls -4.89% of option price over ~1.5 months, secondary summary), and the VRP is documented as negative for indices and most single names. Positive-return pockets are cross-sectional (realized vol above implied vol; low idiosyncratic vol), and those spreads shrink to about zero after 50-100% of the bid-ask spread. I could NOT read the primary PDFs for magnitudes (Goyal-Saretto, Carr-Wu); only abstracts are verified.

## Conditions table
| Condition | Effect on long-option returns | Size | Sample | Survives costs? | Screenable from daily prices? |
|---|---|---|---|---|---|
| Unconditional long ATM delta-hedged call (stocks) | Negative | -4.89% of option price over 1.5 mo (SQ1-4, C) | 1996-2009 | n/a (gross negative) | Yes (baseline) |
| Index/ETF long vol (VRP > 0 in sign of seller profit) | Negative; index VRP is the strongest | Not obtained from a primary source; one search snippet said ~3.5 vol points on 30-day S&P variance swaps (unverified, mathfinance.com) | unknown | n/a | Needs IV data |
| RV (historical) > ATM IV | Higher straddle/hedged returns (SQ1-1) | "economically and statistically significant", number not read | Goyal-Saretto 1996-2006 (my recollection, unverified) | Paper claims robust to liquidity; snippet suggested shrinks with spreads (unverified) | Partly: RV from daily prices, but IV needs options data |
| Low idiosyncratic vol underlying | Better (less negative) delta-hedged return; high idio vol is worse (SQ1-3) | ~2%/month long-short at mids | 1996-2009 | No: ~0 after 50-100% of spread (SQ1-5) | Yes (idio vol from daily returns) |
| Larger market cap | Smaller effect (SQ1-6) | n/a | same | n/a | Yes |
| Earnings straddles | Mixed; see Conflicts | ORATS actual/implied move ~85% typical (blog, unverified) | unknown | Govindaraj reports negative after costs (unverified) | Earnings dates yes, implied move needs IV |
| Crisis / RV jump beyond IV | VRP can turn negative (long vol pays) | no figure verified | - | - | Partly (VIX/RV regime from prices) |

## Findings
- [E] Goyal-Saretto abstract: RV-IV sorted strategy significant (SQ1-1).
- [E] Carr-Wu study 5 indexes + 35 stocks (SQ1-2); no figures read.
- [E] Cao-Han: idio vol negative for delta-hedged returns, ~40% reduced by limits-to-arbitrage controls (SQ1-3); level and costs from secondary summary (SQ1-4..6).

## Conflicts
- Goyal-Saretto claims robustness to liquidity; Cao-Han (via CXO) shows profits vanish with 50-100% spread. Different strategies, so not directly comparable.
- Earnings straddles: ORATS (vendor) shows implied > actual typically yet reversal in 2026 seasons; Govindaraj/MDPI snippets not verified. Unresolved.
- Mechanism of Cao-Han disputed (Wang field paper says model simulations replicate it without frictions; from search snippet).

## Not found
Primary-text numbers for the index vs single-stock VRP gap, Goyal-Saretto monthly return and cost analysis, Bakshi-Kapadia, any post-publication decay study, verified earnings-straddle figures, quantified VRP-negative regimes.

## Blocked
papers.ssrn.com 403; mdpi.com 403; www.cis.upenn.edu SSL failure in fetch_page and 503 in WebFetch; PDFs (NYU Carr-Wu, NBER, uni-muenchen, wallstreethorizon) unsupported by fetch_page and unreadable by WebFetch.

## Search log
1 Goyal Saretto (search, 10 srcs) ; 2 Carr Wu VRP (search); 3 option return TC (disconfirm); 4 earnings straddle (search); 5 Cao Han (search); 6 VRP negative regimes (disconfirm). Plus 5 fetch/Bash calls.
