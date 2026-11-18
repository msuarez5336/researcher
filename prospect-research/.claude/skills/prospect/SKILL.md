---
name: prospect
description: Research one client prospect end to end. Reads the prospect file and the emails in its context folder, plans which questions public research must answer, runs parallel researchers, checks quotes, verifies key claims and writes a cited dossier. Use for "research <client>", "run the prospect", "prepare for the meeting with <client>".
argument-hint: <prospect-slug> [--yes]
---

# Prospect research

Request: $ARGUMENTS

`P` = `prospects/<slug>` and `RUN` = `P/research`. The rules in `CLAUDE.md` apply throughout,
above all: confidential context never goes into a search query or a researcher's brief.

## 1. Read the inputs
- Read `P/prospect.md`, `about-us.md` and each `services/<name>.md` it lists.
- Stop and say exactly what is missing if: `P` does not exist (suggest `/new-prospect`); the
  client name, website or services list still holds `<ANGLE BRACKET>` placeholders; a listed
  service has no file; `about-us.md` is unfilled. Other "unknown" lines are fine.
- If `P/dossier.md` already exists, say so and suggest `/prospect-update <slug>`; continue
  only if the user wants a fresh run.
- Create `RUN/evidence`, `RUN/notes`, `RUN/claims`, `RUN/verdicts` if absent.

## 2. Digest the context
- If `P/context/` holds anything besides `README.md`, launch one `context-reader` agent:
  prospect folder `P`, scope "all files", output `P/context-digest.md`. Then read the digest.
- If it is empty, write a one-line `P/context-digest.md` saying no context was provided.

## 3. Plan
Map what is known onto the question list below. Write `P/plan.md` with:
- a table: question | status (answered by the client / partly / open) | what we know and from
  where | what public research should find;
- the worker briefs, in full, as they will be sent;
- the depth and budget.

Questions. Service-independent:
1. Who is the company: legal name, parent and ownership, industry, size, leadership.
2. US footprint (non-US headquarters only): US entity, locations, headcount, US leadership,
   and whether decisions on these services are made in the US.
3. Dated signals from the last 6–12 months: leadership changes, funding, M&A, earnings
   priorities, launches, layoffs, expansion, regulatory events.

Per service being pitched:
4. Pain or initiative the service addresses, and the cost of not acting.
5. What they use today: a named vendor, an in-house team or nothing.
6. Budget signals and the likely budget holder.
7. Who is involved in the decision and how the company buys.
8. Timing: a deadline or event that makes this urgent.

Written by you from the evidence, not researched: 9. fit per service against `about-us.md`;
10. value hypothesis and hooks.

Even where the client has answered a question, public research still checks it: a mismatch
between what they said and what is public is one of the most useful findings.

Depth, from `prospect.md`:
| Depth | Workers | Calls each | Verification |
|---|---|---|---|
| QUICK | none; you search yourself, at most 10 calls | — | quote check only |
| STANDARD | 2–3 | 12 | one batch of up to 5 claims |
| DEEP | 3–4 | 15 | two batches |

Workers: W1 = questions 1–2; W2 = question 3; W3 = questions 4–8 for all services (split
into two workers at DEEP when there are three or more services); W4 = named decision-makers,
only if `prospect.md` says yes. At STANDARD, W4 counts toward the three-worker cap: fold named
decision-makers into W1 instead (W1 already covers leadership). Workers must not overlap: name the others' scopes in each brief.

Each worker brief is self-contained and holds:
- the objective and why it matters;
- the client's name, website, headquarters and ticker;
- for W3, the service descriptions from `services/` (these are the seller's own material and
  may be shared), but **nothing from the digest**. Turn what the client said into neutral
  questions: write "find what vendor they use for payroll", never "they told us they are
  unhappy with <vendor>";
- the source rules from `CLAUDE.md`, copied in;
- for a listed company: take every number (headcount, revenue, restructuring costs, pay
  figures) from the SEC filing itself, not from press coverage of it; press is for dating
  events and for what filings don't say;
- `RUN` as an absolute path, the evidence path `RUN/evidence/<W>.jsonl`, the notes path
  `RUN/notes/<W>.md`, the budget, the stop rule (two searches in a row add nothing), the
  reply limit (300 words) and the as-of date.

Before going on, reread each brief once for anything that came from `context/`. Remove it.

## 4. Approval
Show the plan table and the briefs, then wait for the user's OK. Skip the wait if the request
includes `--yes`. Record the approval, or `--yes`, at the bottom of `plan.md`.

## 5. Collect
- Launch all `researcher` agents in one message.
- When they return, tell the user straight away about any blocked host or tool.
- One follow-up worker is allowed at DEEP if a question is unanswered. Otherwise record the gap.

## 6. Check quotes
Run `python3 scripts/check_quotes.py --run-dir RUN`. For `no_page`, run
`python3 scripts/fetch_page.py --run-dir RUN <URL>` and re-check. Fix or drop `not_found` and
`lint` items. Items marked `"verified": false` stay, labelled unverified.

## 7. Write the dossier
You are the only writer. Reopen the evidence item and its cached page before relying on any
number, date, name or quotation; worker notes are pointers. Write `P/dossier.md`:

```markdown
# <Client>: prospect dossier
*As of <date> · services: <list> · goal: <goal> · depth: <depth>*
Tags: [said] told to us, cited to a context file · [public] cited to a URL ·
[inference] our reading · ✓ verified · ~ snippet only, not verified.

## Summary
<five lines at most: who they are, the strongest reason to pitch, the biggest risk, fit per
service in a word, the next step>

## What they have told us
## Company snapshot
## US footprint            (non-US headquarters only)
## Recent signals          (dated, newest first)
## Fit by service
### <service>
| Criterion | Evidence | Assessment |
Fit: strong / moderate / poor, with one sentence of reasoning.
Value hypothesis: <their stated or public priority> → <what the service changes>.
Hooks: 2–3 specific, sourced openers.
## Where the emails and public sources disagree
## People                  (only if requested)
## Questions for the next conversation
<what desk research could not answer: success metrics, who will champion the purchase, and
every open row from the plan>
## Not found or not verified
```

Fit criteria: the good-fit traits and disqualifiers in `about-us.md`, a need for the service,
a buyer who matches the service file, and timing. A criterion with no evidence says
"no evidence", not a guess.

## 8. Verify
Extract the claims the summary and the fit assessments rest on: numbers, dates, names in
roles, vendor names, anything marked strong or poor. Use public claims only; claims from
`context/` are not sent to the verifier. Write them to `RUN/claims/batch_<k>.json`, at most 5
per batch, each as `{"cid", "claim", "evidence": [{"id", "quote", "url", "page"}]}`. Launch
one `claim-verifier` per batch with only the batch file, `RUN` and the verdict path
`RUN/verdicts/batch_<k>.json`. Apply the verdicts: keep `supported`; narrow `partial`;
rewrite or remove `unsupported` and `contradicted`; label `unverifiable`.

## 9. Deliver
- Write `P/sources.md`: every source, with type, date, status (✓ / ~ / unreachable) and a
  one-line verdict. Context files are listed separately from public sources.
- Append one line to `P/log.md`: date, depth, files of context read, workers and calls,
  what could not be verified.
- In chat, at most 10 lines: the summary, the path to the dossier, the gaps, the cost.
