---
name: delegate
description: Turn a goal (often the output of research) into a delegation plan and self-contained task briefs that subagents, parallel workers or a future session can carry out with no extra context. It decides whether to delegate at all, decomposes the work into parallel and sequential tasks, writes each brief, and sets up how results come back and get verified. Use for "plan this out for agents", "write briefs for subagents", "split this work up", "hand this off to a future session".
argument-hint: <goal, or path to a research report or spec>
---

# Delegate

Goal: $ARGUMENTS

A delegated agent receives exactly one thing from you: its brief. Every failure this skill
guards against comes from that: missing context, overlap with a sibling, no stop rule, or
results nobody checks. Write the plan with `templates/delegation-plan.md` and save it next to
the work it belongs to (for research, `RUN/brief.md`; otherwise `plans/<YYYY-MM-DD>-<slug>.md`).

## 1. Decide whether to delegate

Delegate only when at least one of these holds:
- the pieces are **independent** and sizeable;
- doing them in one context would **flood it** (many pages, long logs);
- you need a **fresh reviewer** who hasn't seen your reasoning;
- a **different setup** helps (other tools, a narrower tool set, a cheaper model).

Don't delegate when:
- the work takes a handful of tool calls;
- steps depend on each other's decisions;
- several agents would **write** the same files or state.

Handing the same task to a subagent doesn't produce a better answer: it produces parallelism
or a fresh pair of eyes, at extra token cost. If one agent can do it, use one.

## 2. Decompose

1. List the tasks, each with **one objective**, its inputs, its output, and what it depends on.
2. Order by dependency: blocking tasks go first, alone; independent tasks go in one parallel
   group, launched in a single message.
3. Give every shared output a **single writer**. Parallel workers stay read-only or write only
   to files they own. When two workers would touch the same file, serialise them, or give the
   file to the orchestrator.
4. Fill in the decomposition table (Part A2) and tick the four checks: no overlap,
   completeness, single writer, budget.

| Work shape | Run it as |
|---|---|
| Independent lookups or investigations (read-heavy) | Parallel workers, one per sub-question |
| Steps that need earlier results | Sequential: one task, its result passed on by path, then the next |
| Many similar items (files, entities) | One worker per batch, identical brief, different inputs |
| Several angles on one hard question | Parallel workers with different methods, then you compare |
| Implementation touching shared code | One writer at a time; fresh agent per task with a review between tasks |
| Review or verification | Fresh agent, explicit criteria, never shown the author's reasoning |

## 3. Write the briefs

Use Part B of the template for each agent. A brief must state:
- **objective**: one sentence;
- **why**: the purpose, and the scopes of the other agents so this one doesn't duplicate them;
- **what's known or ruled out**;
- **scope**: in and out, read-only or which paths it owns;
- **how**: starting points, sources to prefer or avoid, tools;
- **budget and stop rule**, including what to do if blocked;
- **output**: the file path and format, plus a reply of ≤300 words;
- **quality bar**.

Then read each brief as a stranger would. Does it rely on anything said only in this
conversation? Are all paths absolute? Are the tool names real in this environment (`Agent`,
not `Task`)? For plans with three or more agents, or when a wasted run is expensive, run
`brief-reviewer` on the plan file and apply its fixes.

## 4. Context handoff

- Pass large inputs **by path**, not pasted in.
- Have agents write full results to files and reply with the path and a short summary. This
  keeps your own context free for coordinating.
- For work that spans sessions, keep the plan file and a decision ledger (Part A5) up to date,
  so a fresh session can resume from the files alone.

## 5. Get approval, launch, and handle returns

- Show the user the plan and the briefs before launching anything that is costly or hard to undo.
- Launch each parallel group in one message.
- When results come back:
  1. Surface failures and blocked tools to the user.
  2. Run the mechanical checks (scripts, tests).
  3. Have an independent reviewer with explicit criteria check the load-bearing results.
  4. Reopen originals rather than trusting summaries.
  5. Update the ledger, and revise the plan if the results changed the picture.
