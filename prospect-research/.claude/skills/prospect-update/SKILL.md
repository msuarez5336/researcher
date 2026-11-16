---
name: prospect-update
description: Update an existing prospect dossier after new emails or notes were added to its context folder, or to refresh public signals. Reads only what is new and researches only what changed. Use for "update <client>", "new emails from <client>", "refresh the dossier".
argument-hint: <prospect-slug> [--refresh-signals]
---

# Prospect update

Request: $ARGUMENTS

`P` = `prospects/<slug>`, `RUN` = `P/research`. The rules in `CLAUDE.md` apply. This skill
changes an existing dossier; if `P/dossier.md` does not exist, say so and suggest
`/prospect <slug>`.

1. **Find what is new.** The last run's date is the last line of `P/log.md`. List files in
   `P/context/` modified after it (`find P/context -newer P/log.md -type f`), ignoring
   `_text/` and `README.md`. Also reread `P/prospect.md` for changed services or goal.
   If nothing is new and `--refresh-signals` was not given, say so and stop.
2. **Digest the new files.** Launch one `context-reader` with the list of new files and the
   output path `P/research/notes/context-update-<date>.md`. Then merge its content into
   `P/context-digest.md` yourself, under the same headings, keeping every source reference.
3. **Decide what changes.** For each new fact: does it answer an open question, contradict
   something in the dossier, add a person, add a deadline, or raise a new question for public
   research? List these in chat in a short table.
4. **Research only the gaps.** New questions for public research, plus question 3 (recent
   signals, since the last run date) if `--refresh-signals` was given. Do it yourself if it
   takes at most 10 tool calls; otherwise launch one or two `researcher` agents with briefs
   built as in `/prospect` step 3. Nothing from `context/` goes into a brief or a search query.
   New evidence goes to `RUN/evidence/<W>-<date>.jsonl`.
5. **Check quotes** with `python3 scripts/check_quotes.py --run-dir RUN`.
6. **Revise `P/dossier.md`** in place. Put a section at the top:
   `## What changed on <date>`, three to six lines. Update the as-of date, the affected
   sections, the fit assessments if the evidence moved them, and the questions for the next
   conversation (remove the ones now answered). Keep older "What changed" sections below the
   newest, under a `## History` heading at the end.
7. **Verify** any new public claim that a fit assessment or the summary rests on, with one
   `claim-verifier` batch, as in `/prospect` step 8. Skip if there is none.
8. Update `P/sources.md`, append a line to `P/log.md`, and tell the user in at most 8 lines
   what changed.
