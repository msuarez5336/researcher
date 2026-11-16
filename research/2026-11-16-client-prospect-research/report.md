# Setting up client-prospect research from one editable file

*Research run `research/2026-11-16-client-prospect-research/` · as of 2026-11-16 · tier: STANDARD ·
scope: B2B prospects in the US (US companies, and global companies with a large US presence)*

Tags: [E] documented fact or stated terms · [O] opinion or recommendation · ✓ verified against
the cached original · ~ read only via a summary or snippet, not verified. Evidence ids (e.g.
`SQ2-4`) point to `evidence/*.jsonl`. Legal points record what sources say; they are not legal advice.

## Top findings

1. **Build the setup on this repo's `/research` skill with a prospect input file; no existing
   repo is a better starting point.** Of five projects checked, the closest is Anthropic's
   `account-research` skill, which takes a company name or domain and scores fit against the
   seller's ideal-customer profile, value proposition and competitors. None of the five was seen
   to check quotes or verify claims, which this repo already does. [E for what each repo takes;
   O for the recommendation] ([knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins); SQ2-4–SQ2-6) ✓
2. **The file needs more than a client name and a service list.** Only the "who is the company"
   block is the same for every service. Everything else (pain, current vendor, budget holder,
   who decides, procurement hurdles, timing) depends on the service, so each service entry must
   say what it does, what problem it solves, who buys it and what it replaces. [O, built on
   MEDDPICC and BANT definitions] ([Altify](https://altify.com/blog/meddpicc-enterprise-sellers-qualification/),
   [Pipedrive](https://www.pipedrive.com/en/blog/bant); SQ1-1–SQ1-6) ✓
3. **A draft of that file is in [`prospect-file.draft.md`](prospect-file.draft.md).** It has
   `<CLIENT_NAME>` and `<SERVICE_n_NAME>` placeholders, a rarely-changed "about us" block, and a
   fixed list of ten questions. [O]
4. **Free official US sources cover public companies and federal contractors well, and private
   companies poorly.** SEC EDGAR has JSON APIs with a stated limit of 10 requests per second;
   foreign-headquartered companies listed in the US file Form 20-F there. USAspending and
   SAM.gov cover federal awards and tenders. No official multi-state company registry was found.
   [E] ([SEC](https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data),
   [SEC foreign issuers](https://www.sec.gov/divisions/corpfin/internatl/foreign-private-issuers-overview.shtml);
   SQ3-1–SQ3-5, SQ3b-1, SQ3b-2) ✓
5. **Two obvious sources must not be automated: LinkedIn and the Delaware entity search.** Both
   state a ban on automated tools. [E] ([LinkedIn](https://www.linkedin.com/help/linkedin/answer/a1341387),
   [Delaware](https://icis.corp.delaware.gov/eCorp/EntitySearch/NameSearch.aspx); SQ3-6, SQ3b-6, SQ3b-7) ✓
6. **Researching named people is the legally sensitive part, and California is the state to
   watch.** A 2026 law-firm survey says most state privacy laws exclude business contacts, while
   California covers them (its B2B exemption lapsed on 1 January 2023). CAN-SPAM has no B2B
   exception for email. [E, law-firm commentary and FTC guidance]
   ([Foley, 2026-04](https://www.foley.com/insights/publications/2026/04/the-compliance-tightrope-balancing-uniformity-and-precision-across-u-s-state-consumer-privacy-laws/),
   [FTC](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business); SQ3b-3, SQ3b-4, SQ3-9, SQ3-10) ✓

## What to know about a prospect

MEDDPICC and BANT are deal-qualification frameworks, but their criteria work as a research
question list. MEDDPICC has eight criteria: Metrics, Economic Buyer, Decision Criteria, Decision
Process, Paper Process, Identify Pain, Champion and Competition (SQ1-1 ✓). BANT has four:
Budget, Authority, Need, Timeline (SQ1-6 ✓). Mapped to desk research:

| Question | Same for every service? | Where it comes from |
|---|---|---|
| Who is the company: name, parent, ownership, industry, size, leadership | Yes | practitioner checklists (SQ1-9, SQ1-13) |
| US footprint of a non-US company: US entity, US leadership, where buying is decided | Yes | **no source found; my judgement** |
| Dated signals: new leaders, funding, M&A, earnings priorities | Gathered once, read per service | new leaders as a trigger (SQ1-9); earnings calls (SQ1-11) |
| Pain or initiative, with the cost of not acting | No | MEDDPICC Identify Pain (SQ1-4); BANT Need |
| What they use today: vendor, in-house, nothing | No | MEDDPICC Competition includes status quo and build-in-house (SQ1-5); displacement vs greenfield (SQ1-10) |
| Budget signals and budget holder | No | MEDDPICC Economic Buyer (SQ1-2); BANT Budget |
| Who is involved in the decision | No | BANT Authority, reframed as "who is involved" (SQ1-8) |
| Procurement, legal, security steps | No | MEDDPICC Paper Process (SQ1-3) |
| Timing or deadline | No | BANT Timeline |
| Value hypothesis: a stated priority mapped to the service | No | practitioner checklist (SQ1-12) |

All of the above are [O]: definitions and advice from vendors and practitioners, verified ✓ as
quotes. Metrics and Champion need a live conversation, so the draft file lists them as
questions for the meeting (my inference).

A commercial-services vendor states that generic checklists do not fit services
([Convex](https://www.convex.com/blog/pre-call-research-checklist-commercial-services-sales); SQ1-13 ✓, [O]).
That supports making the service description part of the input.

**No measured evidence was found that deeper research raises win or reply rates.** The one
figure seen, a vendor survey in which 91.6% of respondents said research affected call success,
is a perception, and its quote was not in the cached page (SQ1-14 ~).

## Existing repos

Last-commit dates are from shallow clones on 2026-11-16. Star counts could not be read from the
repo pages (`github.com` blocked), so none is given.

| Repo | Last commit | Input | Seller's services an input? | Needs paid keys? | Evidence |
|---|---|---|---|---|---|
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (`sales/skills/account-research`), Apache-2.0 | 2026-11-13 | company name or domain; optional contact | Indirectly: ICP, value prop, competitors from org context, or one question | No; web search suffices, connectors optional | SQ2-4–6 ✓ |
| [wreynoir/company-enrichment-skill](https://github.com/wreynoir/company-enrichment-skill), MIT | 2026-01-27 | `/company-enrichment acme.com` plus `my-icp.md`, email template, call script | Yes, via `my-icp.md` | Yes: Tavily, Apollo, Perplexity | SQ2-7, SQ2-8 ✓ |
| [langchain-ai/company-researcher](https://github.com/langchain-ai/company-researcher), no licence file seen | 2025-01-26 (stale) | `company`, JSON `extraction_schema`, `user_notes` | No | Yes: Tavily, Anthropic | SQ2-1–3 ✓ |
| [guy-hartstein/company-research-agent](https://github.com/guy-hartstein/company-research-agent), Apache-2.0 | 2026-10-26 | company name via web UI or API | No | Yes: Tavily plus an LLM key | SQ2-9 ✓ |
| [zubair-trabzada/ai-sales-team-claude](https://github.com/zubair-trabzada/ai-sales-team-claude), MIT | 2026-03-26 | `/sales prospect <url>` | Not confirmed | Not confirmed | SQ2-10 ✓ |

What is worth borrowing:
- From `account-research`: its output sections (company snapshot, dated and sourced signals,
  a fit table with evidence per criterion, 2–3 specific hooks, next step) and its rules that
  every value is cited and inference is labelled (SQ2-4–6).
- From `company-enrichment-skill`: keeping the seller's profile in a separate user-edited file,
  with headings Target Industries, Company Size and Business Profile Characteristics (SQ2-8).
- From `company-researcher`: letting a schema define the output fields (SQ2-1, SQ2-2).

Neither borrowed design has a per-service block; the fit is scored against one seller profile.
That part is new in the draft file.

## Sources a run can use

| Source | Gives | Access | Stated terms | Evidence |
|---|---|---|---|---|
| SEC EDGAR (`data.sec.gov` APIs) | filings of US-listed companies; Form 20-F for foreign issuers | open, no key mentioned | max 10 requests/second; no crawling; declare a User-Agent | SQ3-1–3, SQ3b-1, SQ3b-2 ✓ |
| USAspending API | federal contracts and grants a company received | open | none stated on the page | SQ3-5 ✓ |
| SAM.gov Opportunities API | federal tenders | free key | daily cap varies by account role | SQ3-4 ✓ |
| Greenhouse Job Board API | open roles (hiring as a signal), for companies using Greenhouse | open, no authentication for GET | — | SQ3b-8 ✓ |
| Company's own site | about, careers, press, investor pages | open web | per site | not researched |
| LinkedIn | people and roles | **do not automate** | scrapers, crawlers, bots, scripts forbidden | SQ3-6 ✓ |
| Delaware entity search | entity registration | **do not automate** | data mining prohibited; automated tools may lead to suspension | SQ3b-6, SQ3b-7 ✓ |

Legal points, as stated by the sources:
- Scraping public pages: the Ninth Circuit (hiQ v. LinkedIn, April 2022) read the federal
  computer-fraud law as not reaching public websites, per law-firm commentary; contract claims
  remain possible ([Proskauer](https://www.proskauer.com/blog/taking-cue-from-the-supreme-courts-van-buren-decision-ninth-circuit-releases-new-opinion-holding-scraping-of-publicly-available-website-data-falls-outside-of-cfaa); SQ3-7 ✓, commentary).
  So a site's terms still matter even where the page is public.
- State privacy laws and business contacts: see Top finding 6.
- GDPR: Article 3(2) covers a non-EU company when its processing relates to offering goods or
  services to people in the EU or monitoring their behaviour there
  ([text](https://gdpr-info.eu/art-3-gdpr/); SQ3b-5 ✓). Whether that reaches a US seller
  researching EU-based staff of a global company was not answered by any source found. Keeping
  people research to US-based staff avoids the question (my inference).

## Recommended setup for this repo [O]

1. Add `templates/prospect.md` from `prospect-file.draft.md`. One copy per client in `prospects/`.
2. Add a `/prospect <file>` skill that reads the file and runs the existing `/research`
   procedure with fixed sub-questions: company profile and US footprint; signals; one
   sub-question per service (questions 4–10 of the file); optionally decision-makers.
3. Use the `account-research` output sections for the report, and keep this repo's quote
   check and claim verification.
4. Put the source rules from the table above into the worker briefs.
5. Run it interactively as `/prospect prospects/<client>.md`, or unattended with
   `claude -p`, as documented in `research/2026-10-31-claude-code-parameterized-runs/report.md`.

## Where sources disagree
| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Which framework to use | BANT: four quick checks (SQ1-6) | BANT is outdated; use buying-committee frameworks such as MEDDPICC (SQ1-7, vendor opinion) | BANT for small, single-buyer deals; MEDDPICC for complex purchases with several decision-makers. The draft file takes the union. |
| SAM.gov daily request cap | about 10 per day (third-party pages ~) | about 1,000 per day (third-party pages ~) | The official page says only that caps vary by role (SQ3-4 ✓). |

## Outdated or superseded material
- `langchain-ai/company-researcher`: last commit 2025-01-26; treat as a design reference only.
- California B2B commentary from 2022 is superseded for other states by the 2026 Foley survey.

## Method and limitations
- 4 researchers (3 planned plus 1 follow-up on data sources), 15 tool calls each; 2 claim
  verifiers on 10 claims. Quote check: 31 quotes pass against cached pages; the 10 repo quotes
  pass against cloned repo files.
- Blocked: `umbrex.com` (403); `github.com` pages for the caching script (repo files read from
  clones instead; no star counts); an EDPB guidance PDF could not be cached.
- Not covered within budget: California and other state registries, SEC Form D and other
  funding data, technology-stack detection, news APIs, job boards other than Greenhouse,
  review sites, home-country registries. The source table is therefore a starting set, not complete.
- SPIN, Challenger and the original MEDDIC were found only in secondary summaries and are not used.
- Unverified items kept out of the findings: the 91.6% survey figure (SQ1-14), Virginia and
  Colorado specifics (SQ3-12), a reported 2025 Google v. SerpApi case.
- Other prospect-research skills seen only as names in search listings were not checked.

## Open questions
- Which free sources cover private US companies well enough? Needs a follow-up on state
  registries, Form D and news feeds.
- How to establish where a global company makes US buying decisions; no source found.
- Does the draft file produce a usable report? Test it on one real prospect before building the skill.
