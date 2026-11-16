# SQ3b notes (as of 2026-11-16; not legal advice)

## Answer
Legal points A-C verified (A and C from primary pages, B from law-firm commentary only). Delaware's entity search forbids data mining and automated tools; Greenhouse's public job-board GET API needs no key. Sources 3, 4 and 5 and the California registry were not reached within the budget.

## Legal points
- A. Form 20-F is filed on EDGAR [E]: SEC says FPIs file annual reports on Form 20-F and filings go through EDGAR (SQ3b-1, SQ3b-2). https://www.sec.gov/divisions/corpfin/internatl/foreign-private-issuers-overview.shtml
- B. Most state comprehensive privacy laws exclude commercial/employment-context individuals; California is still the exception, per Foley April 2026 [O, commentary] (SQ3b-3, SQ3b-4). Statute texts not read. A search summary also said Indiana, Kentucky and Rhode Island laws took effect 1 Jan 2026 (not cached, unverified).
- C. GDPR Art. 3(2): applies to non-EU controllers/processors when processing relates to offering goods/services to, or monitoring behaviour of, people in the Union [E] (SQ3b-5, gdpr-info.eu reproduction, grade B). The EDPB Guidelines 3/2018 PDF could not be cached (one URL 404; the other is a PDF, "unsupported"). Search snippet only (unverified): mere website accessibility from the EU is not enough (Recital 23).

## Table
| Category | Example source | Facts | Access | Automated-access terms | Evidence |
|---|---|---|---|---|---|
| State registry | Delaware Division of Corporations entity search | name, file number, basic entity details (status/good standing paid, per snippet) | open web form, no API/bulk per vendor Kyckr | "strictly prohibits mining data"; automated tools may cause suspension | SQ3b-6, 7, 9 |
| State registry | California SOS; any official multi-state search | not reached | - | - | none |
| Job postings | Greenhouse Job Board API | public jobs, departments, offices | free, no key for GET | no auth for GET; ToS not read | SQ3b-8 |
| Funding data | SEC Form D (EDGAR) | not reached | - | covered by known EDGAR rules | none |
| Tech stack | - | not reached | - | - | none |
| News | - | not reached | - | - | none |

## Conflicts
None direct. Apify "Delaware scraper" actors exist (search results), but the official page prohibits automated tools.

## Not found / not reached
California SOS terms; official multi-state registry (none found); Delaware "108 Bulk Data services" rule (PDF URL contained spaces, fetch script crashed; contents unknown); Lever/Ashby/Workable terms; Form D; BuiltWith/Wappalyzer/Open-source detection; news APIs (GDELT etc.). 2025-26 scraping ruling: only blog reports on Google v. SerpApi (SQ3b-10, unverified); X Corp v. Bright Data counterclaims reported by media snippets, not verified.

## Blocked
edpb.europa.eu PDFs (404 / unsupported PDF type). fetch_page.py crashes on URLs with spaces. WebFetch not used.

## Search log
1 20-F (search, 0 primary), 2 state B2B exemption (search, 2 useful), 3 EDPB guideline (search), 4 2025 scraping ruling (search), 5 sec.gov 20-F (search, 1 primary), 6 GDPR Art 3 (search), 7 Delaware (search), 8 Greenhouse (search). 7 fetch/Bash caching calls. Disconfirmation: Delaware/Apify scrapers vs official prohibition; no 2026 California exemption reinstatement found.
