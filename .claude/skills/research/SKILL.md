---
name: research
description: Plan and run a cited, verified research project on any topic. It writes a brief, gets the user's OK, fans out parallel researcher agents with non-overlapping briefs, checks every quote against the cached source, verifies load-bearing claims with a fresh-context verifier, and saves report.md and sources.md in a dated run folder. Use for "research X", "look into", "compare these options", "what's the current best practice for", "find the evidence on". Not for questions about this codebase.
argument-hint: <topic or question>
---

# Research

Research request: $ARGUMENTS

Spend effort on searching and on verifying the claims the answer rests on. Spend none on
re-reading, padding, or agents the task doesn't need. Every step below has a reason; the
evidence behind them is in `research/2026-10-31-agent-research/report.md`.

## 1. Pick a tier

| Tier | When | What runs |
|---|---|---|
| QUICK | One fact, one definition, or a current value; being wrong costs little | You search yourself (≤10 tool calls), cite each source with its URL and date, answer in chat. No run folder, no subagents. |
| STANDARD | A comparison, choice or assessment that feeds one decision | 2–4 sub-questions → 2–4 `researcher` agents, about 10–15 calls each → you write the report → verify load-bearing claims. |
| DEEP | Money or publication depends on it, the topic is contested, or the user asks for depth | 4–8 sub-questions, optional second wave, `brief-reviewer` before launch, every number and ranking verified. |

Default to STANDARD when unsure. Don't spawn agents for work you can finish in a handful of
tool calls. If the purpose, scope or tier is unclear, ask once: one question round of at most
four questions (tier with a recommended option, what the answer will decide, scope, what matters most).

For a fast cited answer without a plan or approval step, Claude Code's bundled `/deep-research`
workflow may be enough. Say so if it fits better.

## 2. Plan (STANDARD and DEEP)

1. Create the run folder `research/<YYYY-MM-DD>-<slug>/` with `notes/`, `evidence/`, `claims/`
   and `verdicts/` subfolders.
2. Classify the query and say why in one line. **Depth-first** means one issue from several
   angles, so give workers different angles or methods. **Breadth-first** means independent
   sub-questions, so give one worker per sub-question. **Straightforward** means one focused
   lookup, so use the QUICK tier.
3. Write `brief.md` from `templates/research-brief.md`: the decision it feeds, sub-questions,
   what's already known, scope, source guidance, stopping rules, verification plan, deliverables.
4. Write one brief per worker from `templates/delegation-plan.md` Part B. A worker receives
   only its brief, so put every path, fact and exclusion it needs into it.
5. Run the two tests and write the answers in `brief.md`:
   - **Completeness:** if every worker did its brief perfectly, could you write an excellent
     answer?
   - **Overlap:** could two workers run the same searches? Separate them by sub-question,
     period, source type or angle, and name the other workers' scopes in each brief.
6. If one sub-question blocks the others (for example, "list the candidates" before
   "evaluate each"), schedule it first, on its own.
7. DEEP only: run `brief-reviewer` on `brief.md` and apply its fixes.

## 3. Get approval

Show the user the plan and the exact worker briefs, then wait for their OK. Apply their edits
to `brief.md` and note the approval at the bottom.

## 4. Collect

- Launch all `researcher` agents of a parallel group in **one message**. Pass `model`
  explicitly if the user asked for one.
- Each brief must state: the sub-question id, `RUN` (absolute path), the evidence path
  `RUN/evidence/<SQ>.jsonl`, the notes path `RUN/notes/<SQ>.md`, the budget, and the reply
  limit (≤300 words).
- While workers run, don't duplicate their searches.
- When they return:
  - If any reports blocked hosts or tools, tell the user which ones, and how it affects
    the results, straight away. Don't fill the gap with guesses.
  - Launch a second wave only if a sub-question is unanswered and the tier allows it.
    Stop when a wave adds nothing new.

## 5. Check quotes (mechanical)

```bash
python3 .claude/skills/research/scripts/check_quotes.py --run-dir RUN
```

For `no_page`, run `fetch_page.py` on the URL and re-check. Treat `not_found` and `lint` as
failures: fix the item from the cached page, or drop it. Items marked `"verified": false`
(source unreachable) stay in the report, labelled as unverified.

## 6. Write the report (you alone)

You are the only writer. Workers' notes are routing aids, not authorities: before relying on
any load-bearing claim, figure, date or quotation, reopen the evidence item and its cached page.

Write `report.md` from `templates/report.md`:
- Answer first: "Top findings", each with an evidence tag and a source.
- Organise by theme, never by source or by worker.
- Tag findings `[E]` (measured, with the number and its setup) or `[O]` (opinion), and mark
  verification status.
- Put disagreements in a table with the conditions under which each side holds. Don't
  silently pick a side.
- List outdated material: old model names, renamed tools, deprecated features.
- End with method and limitations: what couldn't be reached and what that means for the conclusions.
- Match length to what the task needs.

## 7. Verify load-bearing claims

1. Extract the claims the conclusions rest on: every number, ranking, "best/most/first",
   causal claim, and anything in Top findings. Write them to `RUN/claims/batch_<k>.json`,
   at most 5 claims per batch, each with its evidence quotes, URLs and cached page paths.
2. Launch one `claim-verifier` per batch, in parallel. Give it only the batch file, `RUN`
   and the verdict path. **Never pass the report, the brief or the notes.**
3. Apply the verdicts:
   - `supported`: keep the claim as it is.
   - `partial`: use the suggested fix or narrow the claim.
   - `unsupported` or `contradicted`: rewrite the claim or remove it, and mention a
     contradiction in the disagreements section.
   - `unverifiable`: keep the claim, labelled as unverified.

## 8. Deliver

1. Write `sources.md` from `templates/sources.md`: ranked, with dates, verification status and
   a one-line verdict on each source. For GitHub repos, give stars as shown on the repo page
   and the last commit date (`git clone --depth 1 --filter=blob:none --no-checkout URL` then
   `git log -1 --format=%cs`).
2. In chat, tell the user in at most 10 lines: the answer, the run folder, what couldn't be
   verified, and the cost (agents and calls).

## Stop rules

- Worker: stop at the budget, or after two searches in a row add nothing new.
- Run: stop when every sub-question has an answer, an explicit "no evidence found", or a
  documented conflict.
- Never exceed the tier's waves to chase sources that may not exist.

## Failure modes this procedure prevents

| Failure | Prevention |
|---|---|
| Vague briefs leading to duplicated searches | One objective per brief, overlap test, other workers' scopes named |
| 50 agents spawned for a simple question | Tier table; QUICK runs no agents |
| Endless searching | Budgets plus a two-empty-searches stop rule |
| SEO pages preferred over primary sources | Source guidance in briefs, A/B/C grading |
| Paraphrases passed off as quotes | `fetch_page.py` cache plus `check_quotes.py` |
| Lead trusting worker summaries | Reopen the original for load-bearing claims |
| Rubber-stamp verification | Fresh-context verifier with explicit verdict criteria, never shown the draft |
| Silent gaps from blocked hosts | Workers report blocked hosts; the user is told immediately |
| Conflicting edits | One writer (you); workers write only their own files |
