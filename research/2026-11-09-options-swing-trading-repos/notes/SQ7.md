# SQ7 notes (as of 2026-11-09)

## Answer
No first-hand account (trade count, period, P&L) of a long-call/put system was found or opened. The budget of 10 calls ran out before the Beckmeyer et al. paper text was read. Loss figures remain secondary (CXO Advisory), though an open PDF host for the paper was located.

## Findings
- [E, secondary] CXO Advisory summary: about $70M aggregate retail loss on 0DTE SPX options, daily net loss up from $184k to $358k after May 2022 daily expirations (SQ7-1, quote verified in cached page).

## Accounts table
| URL | date | strategy | holding | platform | period | trades | numbers | repo | grade |
|---|---|---|---|---|---|---|---|---|---|
| none opened | | | | | | | | | |

SQ5 leads (reddit.sentinel-team.org mirror posts): not opened, because I spent no call on them; still unverified, grade C.
Lead seen only as a search result, NOT opened: https://whatworksintrading.substack.com/p/my-put-spread-bots-won-746-of-their . It is a put-SPREAD bot (74.6% win rate, avg cost $155.29 commission / $633.09 with slippage per the search summary). That goes under "not pure long" (credit/debit unclear), so it is not a deep-read candidate and is unverified.

## Beckmeyer, Branger, Gayda paper status
Not reached as text. Candidate open hosts found via search (not read):
- https://wp.lancs.ac.uk/fofi2024/files/2024/04/FoFI-2024-146-Leander-Gayda.pdf (2024 FoFI conference version, same title; may be a later version)
- https://sites.google.com/site/nicolebranger01/working_papers (author page, links to SSRN)
- https://twitter.com/beckmeyerheiner/status/1642068464859848704
The loss figures as the paper states them: not obtained. Only the CXO secondary figures above.
Next step: fetch the Lancaster PDF with WebFetch (fetch_page.py reports PDFs as unsupported).

## Conflicts
None found.

## Not found
First-hand accounts with trade count + period + P&L. HN Algolia: "0DTE bot results" gave 0 hits; "options trading bot" gave only irrelevant stories (2011-2025). A general web search for "I built an options trading bot buying calls" found nothing first-hand.

## Blocked
- fetch_page.py: application/pdf is unsupported (cfr-cologne cfr-25-09.pdf, aeaweb page). WebFetch could not parse the cfr PDF (binary), and it is probably not the Beckmeyer paper.
- SSRN not tried (known blocked).

## Search log (10 calls)
1 Grep SQ5 notes; 2 HN Algolia "0DTE bot results" (0 hits); 3 WebSearch Beckmeyer pdf (secondary sources); 4 Read SQ5 section 1; 5 HN Algolia "options trading bot" (0 relevant); 6 fetch_page x3 (cxoadvisory ok, 2 PDFs unsupported); 7 WebSearch "I built an options trading bot" (1 put-spread Substack); 8 Grep cxoadvisory cache; 9 WebFetch cfr PDF (unreadable); 10 WebSearch Beckmeyer working paper download (found Lancaster PDF and author page). No disconfirm search separate from these.
