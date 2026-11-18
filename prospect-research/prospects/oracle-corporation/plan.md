# Plan: Oracle Corporation

*As of 2026-11-18 · services: compensation-strategy, talent-strategy · goal: first meeting (test run) · depth: STANDARD*

No emails were provided, so every question is open and goes to public research.

| # | Question | Status | Known now | Public research should find |
|---|---|---|---|---|
| 1 | Who is the company | open | nothing from the client | legal name, HQ, size (revenue, headcount), segments, CEO(s), CHRO |
| 2 | US footprint | not applicable | US-headquartered (per prospect.md, to verify) | confirm HQ only |
| 3 | Dated signals, last 12 months | open | — | leadership changes, layoffs or restructuring, hiring, AI and cloud-infrastructure investment, earnings priorities |
| 4 | Pain the services address | open | — | pay, retention, skills, workforce-reshaping issues stated in filings or news |
| 5 | What they use today | open | — | compensation committee's independent consultant (proxy); in-house rewards and talent teams |
| 6 | Budget signals and holder | open | — | stock-based compensation scale, restructuring costs, cost-cutting statements |
| 7 | Who decides and how | open | — | compensation committee members, CHRO, how consultants are engaged |
| 8 | Timing | open | — | proxy and say-on-pay calendar, restructuring timelines, pay-transparency laws in states where Oracle hires |
| 9 | Fit per service | written from evidence | — | — |
| 10 | Value hypothesis and hooks | written from evidence | — | — |

Workers: W1 = questions 1–2 plus named public roles (executives, HR leadership, compensation
committee); W2 = question 3; W3 = questions 4–8 for both services.
Test note: `prospect.md` asks for named decision-makers, which the skill gives to a fourth
worker, but STANDARD allows 2–3. Named roles were folded into W1. (Skill wording to fix.)

Context check: no context exists, so no brief can contain any.

## Brief W1: company profile and people
```text
OBJECTIVE
W1: Establish who Oracle Corporation (NYSE: ORCL, oracle.com) is today: legal name, headquarters,
size (latest fiscal-year revenue, total and US headcount), business segments, executive leadership
(CEO or co-CEOs, CFO, chief HR / people officer), and the members of the board's compensation
committee, all from primary sources.

WHY
A consulting firm selling compensation strategy and talent strategy consulting is preparing a
first meeting with Oracle. Your profile anchors the dossier and identifies who would buy these
services. Other workers cover: W2 = dated signals from the last 12 months (layoffs, leadership
changes, investments); W3 = pay and talent issues, the incumbent compensation consultant, budget
and timing. Do not research those.

SCOPE
In: the latest 10-K and the latest DEF 14A proxy statement on SEC EDGAR; Oracle's investor
relations and corporate leadership pages. Headcount as stated in the 10-K (human capital section).
Names in business roles only, each with the source and date.
Out: news about recent events, compensation consultants, pay amounts beyond what is needed to
identify roles.

HOW
- Start from EDGAR (company search for Oracle, CIK via data.sec.gov) and Oracle's investor pages.
- Note the fiscal-year end Oracle uses and the filing dates.
- If HQ has moved or a move is announced, record both, with dates.

OUTPUT
- Evidence: RUN/evidence/W1.jsonl. Notes: RUN/notes/W1.md, with a table: field | value | as-of date | evidence id.

COMMON
RUN = /home/user/researcher/prospect-research/prospects/oracle-corporation/research
As-of date: 2026-11-18. Work from /home/user/researcher.
Cache every page you quote: python3 .claude/skills/research/scripts/fetch_page.py --run-dir RUN <URL>
Quotes must be verbatim from the cached page. Never invent or reconstruct a URL.
Write only RUN/evidence/<W>.jsonl, RUN/notes/<W>.md and RUN/pages/. Everything else is read-only.
github.com pages may return 403 to fetch_page.py. If a host or tool is blocked, name it in your reply; do not fill the gap with guesses.
SOURCE RULES: use Oracle's own site (about, careers, newsroom, investor relations); SEC EDGAR
(sec.gov and the data.sec.gov JSON APIs; at most 10 requests per second; declare a User-Agent;
the 10-K, DEF 14A proxy statement and 8-Ks are the key filings); public job-board APIs; reputable
news. Do NOT automate LinkedIn or the Delaware entity search (both forbid automated tools);
search-engine snippets about them may be recorded only with "verified": false.
People: business role and public statements only.
Budget: at most 12 tool calls. Stop earlier once two searches in a row add nothing new.
Reply with only: (1) the two paths, (2) a summary of at most 300 words, (3) gaps, conflicts, blocked hosts.
```

## Brief W2: recent signals
```text
OBJECTIVE
W2: Find dated, sourced events at Oracle Corporation (NYSE: ORCL, oracle.com) from 2025-11 to
2026-11 that bear on pay or talent: layoffs and restructuring, leadership changes (including HR
leadership), large hiring or data-centre build-outs, AI and cloud-infrastructure strategy and
spending, M&A, and priorities stated on earnings calls.

WHY
A consulting firm selling compensation strategy and talent strategy consulting is preparing a
first meeting with Oracle. Trigger events decide whether and how to open the conversation. Other
workers cover: W1 = company profile, leaders and the compensation committee; W3 = pay and talent
issues in filings, the incumbent compensation consultant, budget and timing. Do not research those.

SCOPE
In: Oracle newsroom and investor releases, 8-K filings (sec.gov), reputable news (wire services,
major business press). Each event with its date and source; newest first.
Out: product announcements with no workforce angle; stock-price commentary.

HOW
- Short broad searches first ("Oracle layoffs 2026", "Oracle restructuring", "Oracle executive
  changes 2026", "Oracle earnings call 2026 headcount"), then the primary source for each event.
- In the first half of the budget, search for evidence that contradicts the obvious narrative
  (e.g. reports that layoffs were reversed or that hiring rose).

OUTPUT
- Evidence: RUN/evidence/W2.jsonl. Notes: RUN/notes/W2.md, with a table: date | event | workforce
  angle | source | evidence id.

COMMON
RUN = /home/user/researcher/prospect-research/prospects/oracle-corporation/research
As-of date: 2026-11-18. Work from /home/user/researcher.
Cache every page you quote: python3 .claude/skills/research/scripts/fetch_page.py --run-dir RUN <URL>
Quotes must be verbatim from the cached page. Never invent or reconstruct a URL.
Write only RUN/evidence/<W>.jsonl, RUN/notes/<W>.md and RUN/pages/. Everything else is read-only.
github.com pages may return 403 to fetch_page.py. If a host or tool is blocked, name it in your reply; do not fill the gap with guesses.
SOURCE RULES: use Oracle's own site (about, careers, newsroom, investor relations); SEC EDGAR
(sec.gov and the data.sec.gov JSON APIs; at most 10 requests per second; declare a User-Agent;
the 10-K, DEF 14A proxy statement and 8-Ks are the key filings); public job-board APIs; reputable
news. Do NOT automate LinkedIn or the Delaware entity search (both forbid automated tools);
search-engine snippets about them may be recorded only with "verified": false.
People: business role and public statements only.
Budget: at most 12 tool calls. Stop earlier once two searches in a row add nothing new.
Reply with only: (1) the two paths, (2) a summary of at most 300 words, (3) gaps, conflicts, blocked hosts.
```

## Brief W3: fit for compensation and talent strategy services
```text
OBJECTIVE
W3: For Oracle Corporation (NYSE: ORCL, oracle.com), find public evidence on two services the
seller offers: (A) compensation strategy consulting (pay philosophy, salary structures, incentive
and equity plans, executive pay, pay equity and pay-transparency compliance) and (B) talent
strategy consulting (workforce planning, skills and reskilling for AI, organisation design,
retention, succession). For each: what pain or initiative exists, what Oracle uses today, budget
signals, who decides and how, and timing.

WHY
The seller is preparing a first meeting with Oracle and must judge which service to lead with.
Other workers cover: W1 = company profile, leaders and the names of compensation committee
members; W2 = dated events in the last 12 months (layoffs, leadership changes). Do not research
those beyond what you need to answer your questions.

SCOPE
In:
- The latest DEF 14A proxy: the compensation committee's independent compensation consultant
  (name, how long engaged, how the committee assesses its independence); the say-on-pay vote
  result(s) and any shareholder or proxy-advisor criticism of executive pay; peer group.
- The latest 10-K: human capital section (headcount, retention, talent programmes), stock-based
  compensation expense, restructuring charges.
- Public reporting on Oracle pay issues: pay-equity litigation, pay-transparency compliance
  (salary ranges in US job postings), employee-sentiment data only from named, dated sources.
- Talent: stated skills or AI reskilling programmes, attrition, hiring focus.
Out: individual employees' pay; sources that require login.

HOW
- Start from the DEF 14A and 10-K on EDGAR; then targeted news searches.
- In the first half of the budget, search for counter-evidence: signs that Oracle handles these
  fully in-house or has a long-standing consultant relationship that makes a switch unlikely.

OUTPUT
- Evidence: RUN/evidence/W3.jsonl. Notes: RUN/notes/W3.md, with two sections (A, B), each with a
  table: question (pain / current provider / budget / decision / timing) | finding | evidence id.

COMMON
RUN = /home/user/researcher/prospect-research/prospects/oracle-corporation/research
As-of date: 2026-11-18. Work from /home/user/researcher.
Cache every page you quote: python3 .claude/skills/research/scripts/fetch_page.py --run-dir RUN <URL>
Quotes must be verbatim from the cached page. Never invent or reconstruct a URL.
Write only RUN/evidence/<W>.jsonl, RUN/notes/<W>.md and RUN/pages/. Everything else is read-only.
github.com pages may return 403 to fetch_page.py. If a host or tool is blocked, name it in your reply; do not fill the gap with guesses.
SOURCE RULES: use Oracle's own site (about, careers, newsroom, investor relations); SEC EDGAR
(sec.gov and the data.sec.gov JSON APIs; at most 10 requests per second; declare a User-Agent;
the 10-K, DEF 14A proxy statement and 8-Ks are the key filings); public job-board APIs; reputable
news. Do NOT automate LinkedIn or the Delaware entity search (both forbid automated tools);
search-engine snippets about them may be recorded only with "verified": false.
People: business role and public statements only.
Budget: at most 12 tool calls. Stop earlier once two searches in a row add nothing new.
Reply with only: (1) the two paths, (2) a summary of at most 300 words, (3) gaps, conflicts, blocked hosts.
```

## Approval
- [x] 2026-11-18: user asked to run the test ("Run please"); treated as `--yes`.
