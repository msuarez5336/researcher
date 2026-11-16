# SQ3 notes (as of 2026-11-16). Not legal advice.

## Answer
Free official US sources (SEC EDGAR, SAM.gov, USAspending, state registries) cover filings, federal contracts and entity facts; the prospect's own site, job pages and press releases fill gaps on private firms. Main limits: EDGAR bars crawlers but allows scripted API use at 10 req/s with a declared User-Agent; SAM.gov needs a free key; LinkedIn forbids automated access by contract. US courts have so far been favourable to public-page scraping under the CFAA, but contract claims remain. California is the one state that fully covers business-contact data; CAN-SPAM covers B2B email.

## Findings
- EDGAR: 10 req/s, no botnets/crawlers, declare User-Agent [E] SQ3-1,2,3. Foreign private issuers file 20-F on EDGAR [E, unverified] SQ3-11.
- SAM.gov opportunities API needs free key, daily caps by role [E] SQ3-4. Exact caps conflict across third-party pages (about 10 vs 1,000 per day); official page says only "limited based on role".
- USAspending API: open, awards data on federal contractors/grantees [E] SQ3-5 (no key stated on page).
- LinkedIn forbids scrapers/bots [E] SQ3-6.
- hiQ v. LinkedIn (9th Cir. Apr 2022): CFAA not applicable to public pages; contract/state claims remain [E] SQ3-7. Meta v. Bright Data (N.D. Cal. Jan 2024): narrow, district-level, Meta dropped suit [E] SQ3-8.
- CCPA B2B exemption lapsed 1 Jan 2023 [E] SQ3-9. Other states (VA, CO) generally exclude B2B data [O, unverified] SQ3-12.
- CAN-SPAM covers B2B email [E] SQ3-10.
- GDPR: no source answers the question directly; likely turns on EU establishment or targeting people in the EU [O, unverified] SQ3-13.

## Table
| source category | example source | facts it gives | access | automated-access terms | US private cos? | foreign HQ cos? | evidence |
|---|---|---|---|---|---|---|---|
| Securities filings | SEC EDGAR (data.sec.gov JSON) | financials, risk factors, officers, subsidiaries | free API, no key | no crawlers; 10 req/s; declare User-Agent | no (public/registered only) | yes if US-listed (20-F/40-F) | SQ3-1,2,3,11 |
| Federal procurement | SAM.gov Opportunities API | bids, agency, NAICS | free key | daily cap by role | partly (registrants/bidders) | only with US contracts | SQ3-4 |
| Federal awards | USAspending API | contracts/grants won | open | none stated on page | partly (federal awardees) | with US awards | SQ3-5 |
| Professional network | LinkedIn | staff, roles, headcount | login; paid API | forbids scrapers/bots | yes | yes | SQ3-6 |
| State registries, own site, jobs, news, funding, tech-stack, review sites | not checked (budget) | | | not verified | | | none |

## Legal limits
- US federal: CFAA, hiQ v. LinkedIn 9th Cir. 2022-04 (public pages not "without authorization"); contract claims survive. Meta v. Bright Data N.D. Cal. 2024-01 (narrow). CAN-SPAM B2B email covered (FTC).
- US state: California CCPA covers business contacts since 2023-01-01 (notice, deletion, opt-out). VA/CO generally exclude B2B (unverified, 2022-23 sources; newer state laws not checked).
- Non-US: GDPR possible via EU establishment or targeting EU persons; unresolved, inference only.

## Conflicts
SAM.gov daily caps differ across third-party pages. Pro-scraping rulings (CFAA) vs platform terms (LinkedIn) hold under different theories: crime statute vs contract.

## Not found
State secretary-of-state registries and terms; job-board, funding (Crunchbase), tech-stack, review-site terms; Companies House/home-country registries; FTC enforcement on prospect data; current (2025-26) scraping rulings; CPPA position on cold outreach; Texas/other data-broker laws; official GDPR text.

## Blocked
None blocked. Budget (15) used up before the items above.

## Search log
1 hiQ/Van Buren (search) 4 sources; 2 EDGAR fetch; 3 CCPA B2B (search); 4 LinkedIn terms; 5 cache 6 pages; 6 GDPR; 7 SAM API; 8 grep; 9 Meta v Bright Data (disconfirm/counter); 10 cache 3 pages; 11 state B2B; 12 20-F; 13 grep checks.
