# Research brief: <topic>

<!--
Kick-off document for one research run. The orchestrator fills it in, saves it as
research/<YYYY-MM-DD>-<slug>/brief.md, and shows it to the user before any worker is launched.
Why each section exists is noted in brackets; full reasoning and sources are in
research/2026-10-31-agent-research/report.md.
Delete the comments when you fill it in.
-->

| Field | Value |
|---|---|
| Date (as-of) | YYYY-MM-DD |
| Requested by / for | <who will use the answer> |
| Run folder | `research/YYYY-MM-DD-<slug>/` |
| Tier | QUICK / STANDARD / DEEP <!-- effort scales with the task: see the tier table in .claude/skills/research/SKILL.md --> |
| Budget | <N> workers × <M> tool calls each, <K> verification batches |

## 1. The decision this research feeds
<!-- [Every brief needs the "why": workers generalise from the purpose, not just the instruction.
Anthropic prompting guide; daymade "Decision Question".] -->
<One or two sentences: what will someone do differently depending on the answer?>

## 2. Question and query type
- **Main question:** <one sentence>
- **Query type:** depth-first (one issue, many angles) / breadth-first (independent sub-questions) / straightforward (one focused lookup)
  <!-- [Classify before spawning anything. Anthropic research_lead_agent.md] -->
- **Why this type:** <one line>

## 3. What we already know / assume
<!-- [Stops workers re-finding known facts; names assumptions so they can be challenged.] -->
- Known: <facts with sources>
- Ruled out: <what not to re-investigate>
- Working hypotheses (to be tested, not confirmed): <H1>, <H2>

## 4. Sub-questions
<!-- [One core objective per worker, no overlap; blocking questions first.
Anthropic lead prompt; MAST "specification" failures.] -->
| ID | Sub-question | Depends on | Worker | Parallel group |
|---|---|---|---|---|
| SQ1 | | — | researcher | A |
| SQ2 | | — | researcher | A |
| SQ3 | | SQ1 | researcher | B (after A) |

**Completeness test:** if every worker did its brief perfectly, would the combined results answer
section 2 well enough to support the decision in section 1? <yes / what is missing>

**Overlap test:** could two workers end up running the same searches? <no / how they are separated>

## 5. Scope
- In scope: <period, region, product versions, source types>
- Out of scope: <explicit exclusions> <!-- [stops research drift] -->
- Recency rule: prefer material from <period>; flag anything older or using outdated names.

## 6. Source guidance
- Prefer: <primary sources: papers, official docs, filings, repos, first-hand write-ups>
- Treat with care: <vendor claims about their own product, secondary summaries, benchmark self-reports>
- Avoid: <content farms, SEO listicles, AI-generated roundups>
- Known starting points (verify, don't assume): <URLs>

## 7. Stopping rules
<!-- [Unbounded search is a documented failure: "scouring the web endlessly for nonexistent sources".
Anthropic multi-agent post; DeepSearchQA names premature stopping AND over-padding.] -->
- Per worker: stop at the tool-call budget, or after two searches in a row add no new relevant source.
- Whole run: stop when every sub-question has an answer, a stated "no evidence found", or a
  documented conflict. At most <1|2> follow-up waves.

## 8. Verification plan
- Every quote: `check_quotes.py` against the cached page (deterministic).
- Load-bearing claims (numbers, superlatives, anything the decision rests on): `claim-verifier`
  in batches of ≤5, fresh context, never shown the report.
- Unreachable sources: label the claim *unverified*, don't drop it silently and don't call it refuted.

## 9. Deliverables
| File | Content |
|---|---|
| `brief.md` | this document, as approved |
| `report.md` | findings by theme, top findings first, inline citations, evidence vs opinion, disagreements, limitations |
| `sources.md` | ranked source table with dates and verdicts |
| `notes/` | one notes file per worker |
| `evidence/` | one JSONL file per sub-question (quote, URL, grade) |
| `verdicts/` | claim-verifier output |

## 10. Worker briefs
<!-- One block per worker, written with templates/delegation-plan.md Part B.
Paste them here so the user approves the exact text that will be sent. -->

### Brief SQ1
...

## Approval
- [ ] User approved on <date>, with these changes: <...>
