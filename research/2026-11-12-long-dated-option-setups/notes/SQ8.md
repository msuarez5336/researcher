# SQ8 notes (as of 2026-11-12)

## Answer
No original paper read in this pass reports unhedged returns to bought single-stock options by maturity beyond three months, and none has a sample ending after 2015 for unhedged buyer returns. The best maturity breakdown is Ni (1996-Jun 2005), 1-, 2- and 3-month calls held to expiry at midpoint, but I could only read it on a secondary page that reproduces her tables (grade C). Costs are large: quoted relative spreads of 23-34% for OTM calls at 20-180 days (1996-2007), and paying the ask turned every Ni strike bin negative.

## Findings
- [E] Ni, midpoint, unhedged, held to expiry, 1996-Jun 2005 (pre-2015), strike/stock bins <=0.85, .85-.95, .95-1.05, 1.05-1.15, >1.15. 1 month: 2.31, 2.50, 1.98, -10.15, -36.86%. 2 months: 2.88, 4.70, 6.34, 1.68, -21.88%. 3 months: 2.64, 4.20, 5.55, 0.39, -23.20%. SQ8-1, SQ8-2, SQ8-4. Secondary reproduction, not the paper.
- [E] Same table at ask, 1 month: -0.97, -2.25, -6.30, -22.54, -46.52%. SQ8-3. So midpoint ITM/ATM gains vanish at ask.
- [E] Bali et al. (1996-2020) results are delta-hedged; average monthly hedged return -0.01%; buckets short <=90 and long >90 days. SQ8-5. Not a buyer's return. Table by bucket not extracted.
- [E] Spreads: relative quoted spread OTM calls 34.02% (20-70 days) and 22.67% (71-180 days), 1996-2007. SQ8-6, SQ8-7. Average dollar spread 22.9c calls, 23.8c puts. SQ8-8.
- [E] Muravyev-Pearson 2003-2006: quoted 8.1c, effective 6.2c, avg price $1.70; timing-adjusted effective spread one-third smaller for the average trade, but that reflects fast traders timing quotes. SQ8-9, SQ8-10. [O-ish] ordinary trader should assume the conventional effective spread, not the adjusted one (my reading, not stated in the lines I read).
- [E] Retail (Nov 2019-Jun 2021): weekly options spread 12.6%, retail loses money; $2.1bn lost at 10-day horizon, mostly trading costs. SQ8-11, SQ8-12.

## Table (a)
| study | sample | maturity | strike distance | call/put | average return | hedged? | costs included? | read in original? | id |
|---|---|---|---|---|---|---|---|---|---|
| Ni | 1996-Jun 2005 (pre-2015) | 1 month, to expiry | K/S >1.15 / 1.05-1.15 / .95-1.05 / .85-.95 / <=.85 | call | -36.86 / -10.15 / 1.98 / 2.50 / 2.31% | no | midpoint only | no, secondary | SQ8-1 |
| Ni | same | 2 months | same bins | call | -21.88 / 1.68 / 6.34 / 4.70 / 2.88% | no | midpoint only | no | SQ8-2 |
| Ni | same | 3 months | same bins | call | -23.20 / 0.39 / 5.55 / 4.20 / 2.64% | no | midpoint only | no | SQ8-2 |
| Ni | same | 1 month | same bins | call | -46.52 / -22.54 / -6.30 / -2.25 / -0.97% | no | ask price | no | SQ8-3 |
| Bali et al. | 1996-2020 | monthly; <=90 vs >90 days | ITM/ATM/OTM | both | mean -0.01% | delta-hedged | no | yes (working paper) | SQ8-5 |
| Bryzgalova et al. | Nov 2019-Jun 2021 | mostly weekly, 10-day horizon | not read | both | aggregate loss $2.1bn | no | yes | yes | SQ8-12 |
| Boyer-Vorkink | not read | 7-day | lottery-like | call | not verified (-35%/wk is a lead only) | no | | no | none |

## Table (b)
| cost measure | size | maturity, strike | sample | id |
|---|---|---|---|---|
| relative quoted spread | 34.02% | 20-70 days, OTM calls | 1996-2007 | SQ8-6 |
| relative quoted spread | 22.67% | 71-180 days, OTM calls | 1996-2007 | SQ8-6 |
| average dollar quoted spread | 22.9c calls, 23.8c puts | all | 1996-2007 | SQ8-8 |
| quoted spread | 8.1c (price avg $1.70) | liquid options, not split | Apr 2003-Oct 2006 | SQ8-9 |
| conventional effective spread | 6.2c | same | same | SQ8-9 |
| timing-adjusted effective spread | one-third below conventional (average trade) | same | same | SQ8-10 |
| retail quoted spread | 12.6% | weekly options | Nov 2019-Jun 2021 | SQ8-11 |

## Conflicts
- Quoted spread (8.1c) vs Christoffersen dollar spread (22.9c): different samples (liquid options 2003-06 vs 341 firms 1996-2007) and definitions. Both pre-2015.
- Ni midpoint shows small positive ITM/ATM returns; at ask they are negative. Which holds depends on fill price.
- Muravyev-Pearson cost-lowering applies to execution-timing traders; retail loses money (Bryzgalova).

## Not found
- Unhedged returns by maturity beyond 3 months; any unhedged sample ending after 2015; puts by strike distance.
- Boyer-Vorkink original (no open copy found; search gave only abstract pages). Ni original (only IDEALS record page cached, no full text).
- Bali et al. raw bucket tables not extracted (budget); they are hedged anyway.
- Not searched: item 3 (implied vs realised variance gap, Driessen et al., Carr-Wu); disconfirming search was run (long-dated single-stock calls, fairly priced) and found nothing for or against beyond Ni and an index-selling study not recorded.

## Blocked
- boots.bc.edu PDF returned 404. Pre-listed blocked hosts not retried.

## Search log
1. Ni pdf (search) 3 new but no PDF. 2. Boyer Vorkink pdf (search) 0 usable. 3. Bali et al ML (search) 1 usable. 4. Muravyev Pearson pdf (search) 3 usable. 5. Long-dated calls fairly priced (disconfirm) 0 usable. 6. Christoffersen pdf (search) 1 usable. 7. Ni table search 1 (reducing-suffering). 8. Raw returns by maturity post-2015 (search) 0 usable (Hu NUS 1996-2013 cached, one-month only, not recorded). Fetches: CFR, IDEALS, BU, mql5, Kellogg, Yuen, au.dk, boots, NUS, reducing-suffering, LBS.
