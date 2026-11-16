# SQ2 notes (as of 2026-11-16)

## Answer
Five documented candidates exist. Two have a reusable input design: Anthropic's sales `account-research` skill (company or domain, with seller ICP and value prop from org context) and wreynoir's `company-enrichment-skill` (domain plus user-written `my-icp.md` and template files). None is a clear drop-in over the owner's /research skill. The closest pattern is "reuse /research with a prospect template", borrowing the account-research section list and the ICP-file fields. LangChain company-researcher is real but stale (last commit 2025-01-26).

## Table
| repo | URL | licence | stars | last commit | input mechanism | takes seller's services? | output | data sources/keys | cites sources? | evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| langchain-ai/company-researcher | https://github.com/langchain-ai/company-researcher | no LICENSE file in tree (unverified) | ~215 (third-party relatedrepos snippet, Jan 2025; page not reachable) | 2025-01-26 | graph inputs: company, extraction_schema (JSON), user_notes | No (only free-text user_notes) | JSON matching the schema | Tavily + Anthropic keys (paid) | No per-claim citations in README; optional include_search_results flag | SQ2-1,2,3 |
| anthropics/knowledge-work-plugins (sales/account-research) | https://github.com/anthropics/knowledge-work-plugins | Apache-2.0 | ~15.5k (secondary: DEV Community listing, not repo page) | 2026-11-13 | skill args: company name or domain, optional contact | Yes, indirectly: ICP, value prop, competitors grounded from org context or one question | brief: CRM status, snapshot, dated signals, contact, ICP fit table, 2-3 hooks, next step | web search; optional enrichment/CRM connectors (MCP) | Yes, "every value is cited" | SQ2-4,5,6 |
| wreynoir/company-enrichment-skill | https://github.com/wreynoir/company-enrichment-skill | MIT (README) | not obtained | 2026-01-27 | slash command `/company-enrichment acme.com` plus ~/.claude/my-icp.md, email template, call script | Yes, via my-icp.md and template files | ICP check, company brief, contacts, drafted outreach, credit count | Tavily, Apollo, Perplexity keys; LeadMagic optional (paid) | not stated in README | SQ2-7,8 |
| guy-hartstein/company-research-agent | https://github.com/guy-hartstein/company-research-agent | Apache-2.0 (LICENSE text) | ~1.9k (meshkore snippet, stale) | 2026-10-26 | web UI / POST /research with company name | No | briefing, PDF export | Tavily; OpenRouter/OpenAI/Gemini; optional MongoDB | "source-backed" per README (quality unchecked) | SQ2-9 |
| zubair-trabzada/ai-sales-team-claude | https://github.com/zubair-trabzada/ai-sales-team-claude | MIT | not obtained | 2026-03-26 | `/sales prospect <url>` | Not seen in what I read (unverified) | PROSPECT-ANALYSIS.md, 5 parallel subagents | WebFetch/WebSearch; Crunchbase/LinkedIn named as source tiers | source priority list; per-claim cites unverified | SQ2-10 |

## Input-file designs (field names as they appear)
1. LangChain: `company`, `extraction_schema` (JSON schema; `title` and `description` required; example fields `company_name`, `founding_year`, `founder_names`, `product_description`, `funding_summary`), `user_notes`. Config: `max_search_queries`, `max_search_results`, `max_reflection_steps`, `include_search_results`. Source: src/agent/configuration.py, README.
2. wreynoir my-icp.md headings: "Target Industries", "Company Size" (Employee Count Range / Sweet Spot, Revenue Range, Funding Stage), "Business Profile Characteristics" (Operational Maturity). Inputs split into my-icp.md, my-cold-email-template.md, my-cold-call-script.md. Anthropic's account-research uses "ICP (industries, size, titles, disqualifiers), value prop, competitors, differentiators" as grounding.

## Findings
- [E] account-research is the closest match to the owner's need: company or domain in, sourced brief with ICP-fit table out (SQ2-4,5,6). The lead that Anthropic ships a sales plugin with account research is confirmed.
- [E] The LangChain lead is confirmed but the repo is old (SQ2-1..3). Output is schema-driven, which is a reusable idea.
- [E] Several tools need paid third-party keys (Tavily, Apollo, Perplexity) (SQ2-7,9).
- [O] None of these has a quote-check or claim-verification step like the owner's /research skill (I saw none in the files read). The README claims "source-backed" without evidence.
- [O] Hallucination risk: a web search surfaced Oppo-team deep-research findings (about 20% of errors from invented content; o3 Deep Research citation accuracy 65.98%), reported by the-decoder.com. I did not cache this page, so it is not in the evidence file. Unify GTM material is vendor opinion.

## Conflicts
- Star counts come from third-party snippets with different dates and are unreliable. Anthropic plugin counts differ by source (11 vs 15 roles).
- The ai-sales-team repo claims "14 skills", "5 parallel agents". I did not check these.

## Not found
- Stars from repo pages (github.com blocked for fetch_page.py). Licence for LangChain repo (no file in tree; may be elsewhere). Whether ai-sales-team takes seller services. Issue reports of bad output for specific repos (not searched in repos). Many other skills (lead-research-assistant, prospect-research-compiler, deanpeters company-research) seen only as search-listing names, unchecked.

## Blocked
- github.com web pages returned 403 via fetch_page.py. Workaround: `git clone --depth 1 --filter=blob:none --no-checkout` into scratch worked; file contents saved as RUN/pages/{lc-,kwp-,wr-,gh-,zt-}* (not fetched URLs; check_quotes may not map them to URLs).

## Search log
1. "Claude Code skill company research prospect github" - search - 6 candidates
2. "langchain-ai company-researcher github" - search - confirmed lead, guy-hartstein
3. "anthropics knowledge-work-plugins sales account research" - search - confirmed lead
4. clone x5 + 3 file-reading calls (git show) - read
5. "AI company research agent hallucinated facts..." - disconfirm - the-decoder, Unify GTM
Budget used: 10 of 15.
