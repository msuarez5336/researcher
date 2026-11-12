# SQ1 notes (as of 2026-11-12)

## Answer
Unhedged buyers of one-month, out-of-the-money single-stock calls lost money on average in 1996-2009 samples (-28% for calls >15% OTM per Ni), and returns worsen as the strike rises. Lottery-like (high-skew) options, mostly short-dated and far OTM, earn the worst returns, and puts are worse than calls. I found no measured unhedged average by maturity for 1-6 months, so the working hypothesis (smaller loss at 1-6 months) is untested here; the only maturity evidence (Boyer-Vorkink) says the effect is strongest near expiry, which is consistent with it but unquantified. All numbers come from secondary (CXO) summaries, not the papers.

## Findings
- [E] 1-month calls, 1996-2005, unhedged, midpoint: -28% for >15% OTM; worse with higher strike; ATM/ITM positive at midpoint but possibly not at ask (SQ1-1, SQ1-2). Sample ends before 2015.
- [E] Delta-hedged calls lose 4.89% of option price over 1.5 months to expiry, 1996-2009 (HEDGED, not buyer's return) (SQ1-3). Fixed-cost friction wipes out the long-short hedged strategy (SQ1-4).
- [E] Lottery-like options: 7-day calls high-skew quintile -35.4%/week vs +1.4% low-skew; puts -60.6% vs -5.6% (SQ1-5). Sample ends 2009 (before 2015). Demand evidence (SQ1-6).
- [O, unverified, search snippet only] Variance risk premium: Driessen-Maenhout-Vilkov (JF 2009) report a large negative index VRP but no significant individual-stock VRP on average (S&P 100 constituents); correlation risk is the explanation. A 2020 AEA conference paper reports a positive average individual VRP; a Cologne paper finds few stocks with significant VRP. Not read; PDF could not be parsed by WebFetch.
- [E, unverified, snippet] Retail: Bryzgalova, Pavlova, Sikorskaya (JF 2023), Oct/Nov 2019-Jun 2021, ETF and single-stock options, retail lost >$4bn after costs; spreads 12-28%; half of wholesaler volume in options expiring within a week (via evidenceinvestor.com blog). Costs included. Mostly short-dated, so not 1-6 month evidence.

## Table
| study | sample | maturity | strike distance | call/put | avg return | hedged? | costs? | id |
|---|---|---|---|---|---|---|---|---|
| Ni 2008 (via CXO) | 1996-2005 | 1 month, held to expiry | >15% OTM | call | -28% | no | midpoint only | SQ1-1 |
| Ni 2008 | same | 1 month | rising strike | call | declines with strike; ATM/ITM positive at midpoint | no | midpoint only | SQ1-2 |
| Goyal-Saretto type (via CXO) | 1996-2009 | 1.5 months to expiry | ATM-ish | call | -4.89% of option price | yes, delta-hedged | partly gross | SQ1-3 |
| Boyer-Vorkink (via CXO) | ~1996-2009 | 7 days | high skew (far OTM) | call / put | -35.4% / -60.6% per week | no | no fees, midpoint | SQ1-5 |
| Driessen et al 2009 | not read | not read | n/a | n/a | no significant individual VRP | n/a | n/a | not recorded |

## Conflicts
- Midpoint vs ask: ATM calls look positive at midpoint (Ni via CXO) but CXO says ask pricing may erase it (SQ1-2).
- Individual-stock VRP: DMV say insignificant on average; a 2020 AEA paper says positive average (unverified). Differences likely in sample and measurement.

## Not found
Unhedged average returns by maturity in the 1-6 month range; put returns by strike distance for 1-6 months; any post-2015 sample; study finding single-stock calls fairly priced or profitable (disconfirm search found only ATM positive at midpoint). Topic 3 (lottery demand) only via Boyer-Vorkink summary. Retail: one search done.

## Blocked
core.ac.uk (403). nber.org and kops.uni-konstanz.de, netspar.nl PDFs unsupported by fetch_page; WebFetch could not parse PDFs. The kops PDF was Constantinides et al (index options, not relevant). Ni (2008), Goyal-Saretto, Boyer-Vorkink originals not read; evidence relies on CXO Advisory summaries (grade C).

## Search log
1. returns buying options by moneyness/maturity (search): CXO pages. 2. Bondarenko/Coval-Shumway (search): index only. 3. Goyal-Saretto/Bakshi-Kapadia (search): abstracts. 4. Boyer-Vorkink (search). 5. fairly priced/profitable calls (disconfirm): no new source. 6. Bali-Murray/Ni/Coval (search). 7. DMV VRP (search). 8. retail losses (search). 9. Goyal-Saretto details (search): nothing new. Plus 3 fetch batches, 1 Read, 1 Grep set, 2 WebFetch PDFs; budget slightly exceeded (~22 calls).
