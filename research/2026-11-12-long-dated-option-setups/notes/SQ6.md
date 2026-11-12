# SQ6 notes (as of 2026-11-12)

## Answer
Official sources give free, dated data for short interest (FINRA, 7 business days after settlement), insider filings (SEC EDGAR, filing dates) and the risk-free rate (FRED). Delisting-inclusive adjusted prices, historical index membership and as-first-reported analyst estimates and earnings-session flags are available mainly from paid vendors (Norgate, Sharadar, CRSP/WRDS, I/B/E/S); free equivalents (Yahoo-type feeds, Wikipedia S&P reconstructions) are survivorship-biased or not point-in-time. Earnings dates and analyst estimates are the weakest as-known inputs.

## Table
| data type | source | history | publication delay | as known at the time? | price (date seen) | limits | evidence |
|---|---|---|---|---|---|---|---|
| Adjusted prices incl. delisted | Norgate Data | delisted back to ~1990 (some types) | n/a | prices yes; index constituents yes (vendor) | top tiers only; USD price not retrievable (unverified) | personal licence terms not read | SQ6-15 |
| Same | Sharadar (Nasdaq Data Link / QuantRocket) | 1998 | n/a | n/a | not retrievable | not read | SQ6-11 |
| Same | CRSP | not retrieved | n/a | n/a | not retrieved | institutional | not extracted |
| Same | Yahoo/broker feeds | varies | n/a | no: omit delisted | free | survivorship bias | SQ6-4,5 (not Yahoo-specific; only search snippets, MarketParquet/R-bloggers unfetched) |
| Earnings dates | SEC 8-K (EDGAR) filing time; Sharadar 8-K events | 1993 (Sharadar) | same day | yes: actual date and acceptance time | EDGAR free | gives actual date, not the schedule | SQ6-10,14 |
| Earnings dates | I/B/E/S | n/a | n/a | questionable: dates mislabelled | paid | | SQ6-6 |
| Earnings dates + BMO/AMC | vendor APIs (FlashAlpha, FMP, EODHD, FirstRate from 2000) | varies | n/a | unverified; no history of scheduled vs actual found | not retrieved | | SQ6-18 |
| Short interest | FINRA | not extracted (page says listed and OTC) | 7th business day after the 15th / month-end settlement | yes if lagged by publication date | free | weekly proposal pending (SQ6-3) | SQ6-1,2,3 |
| Analyst estimates | I/B/E/S | n/a | n/a | no: history was edited (1.6%-21.7% records changed between downloads, 2000-2007 downloads) | paid (not retrieved) | | SQ6-7 |
| Insider filings | SEC EDGAR; SEC Insider Transactions data sets | 2006-2026 | Form 4 due 2 business days (secondary source); data sets quarterly | yes (filing date) | free | | SQ6-8,9,10 |
| Insider | Sharadar | 2005 | | vendor | not retrieved | | SQ6-12 |
| Index membership | Sharadar S&P 500 | 1957 | | vendor claim | not retrieved | S&P 500 only | SQ6-13 |
| Index membership | Norgate | n/a | | vendor claim | see above | | SQ6-15 |
| Index membership | Wikipedia reconstruction | ~1990 as built in 2020 | | no official dated file | free | built backward from current list | SQ6-16 |
| Risk-free rate | FRED DTB3 | daily; start date not extracted | next day | yes | free | | SQ6-17 |
| Dividends/splits | not searched separately (price vendors above carry them) | | | | | | |
| Stable identifiers | EDGAR CIK (submissions API); Sharadar permaticker not confirmed; CRSP PERMNO not retrieved | | | | | | SQ6-10 |

## Findings
- [E] FINRA short interest: twice monthly, published 7th business day after settlement (SQ6-1,2).
- [E] SEC insider data sets 2006-2026, quarterly updates (SQ6-8). [O] Form 4 two-day deadline from secondary source (SQ6-9).
- [E] I/B/E/S has two documented as-known problems: mislabelled earnings dates (SQ6-6) and retroactive edits to recommendations (SQ6-7). Edits were to recommendations; edits to EPS forecasts across file versions reported by a 2020 Review of Accounting Studies paper (search snippet only, not recorded).
- [O] Survivorship: delisted stocks must be explicitly included (SQ6-4,5). Measured effect only a secondary single case (SQ6-19, unverified); no peer-reviewed measure found. These are index-momentum equity backtests, not option backtests.
- [O] Free S&P 500 history is a Wikipedia reconstruction (SQ6-16).

## Conflicts
- FINRA: a 2021 FINRA notice (snippet) said FINRA itself disseminated only OTC short interest and exchange-listed went via exchanges; the current FINRA page says listed and OTC. Current page preferred.
- QuantRocket says survivorship bias is not one-directional (snippet); the other examples show inflated results.

## Not found
Official S&P index membership publication; CRSP details and pricing; Sharadar licence and price; Yahoo/Stooq delisted coverage by primary source; dividend/split sources; CIK mapping detail; analyst-estimate sources with original dates other than I/B/E/S (none checked); whether any vendor stores scheduled earnings dates as originally scheduled. Prices not retrievable for all paid vendors, licence limits not read.

## Blocked
archive.nyu.edu (TLS cert error). sec.gov Forms 3-4-5 PDF unsupported by the fetch script, so the Form 4 deadline is not confirmed from the SEC.

## Search log
1. survivorship bias delisted effect (disconfirm): 3 sources. 2. FINRA short interest schedule: 3. 3. earnings dates IBES: 3. 4. Ljungqvist Rewriting History: 2. 5. Norgate: 2. 6. Sharadar: 2. 7. Form 4: 1. 8. Yahoo delisted: 2. 9. earnings API: 3. 10. S&P constituents: 2. Plus 3 cache calls and 2 grep calls. About 20 calls.
