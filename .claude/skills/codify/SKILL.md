---
description: Turn a task that will be repeated into a tested script, plus a thin Haiku skill only when a judgment step is left, so later runs spend tokens only on what a script can't do. Use when the user says "make this repeatable", "script this", "codify", or repeats the same mechanical steps.
argument-hint: <name> "<what the task does>"
arguments: [name, goal]
disable-model-invocation: true
---

# Codify `$name`

Goal: $goal

You are paying once, now, with a capable model, so that every later run is cheap: a script does
the deterministic work for zero tokens, and a small model does only the part that needs judgment.
Why each rule exists: the Claude Code docs pages "Manage costs effectively"
(code.claude.com/docs/en/costs) and "Skills" (code.claude.com/docs/en/skills), the live tests in
the README's "Token-lean kit" section, and the research run
`research/2026-10-31-claude-code-parameterized-runs/` (if present in this repo).

## 1. Look before you build
- Read `scripts/INDEX.md` (if it exists) and list `.claude/skills/`. If a script already covers
  part of the goal, extend it instead of writing a second one.
- If you can't say what the inputs and the expected output are, ask the user once, then go on.

## 2. Split the task
Write a short table: step | can a program compute it exactly? | goes to.
- **Script**: fetching, listing, filtering, counting, sorting, diffing, parsing, reformatting,
  validating, templated text, anything with a single right answer.
- **Model**: summarising for a reader, choosing between options, writing prose, explaining.
- If every step is scriptable, there is no model step. Don't add one to "present" the output.

## 3. Write the script
- Start from `${CLAUDE_SKILL_DIR}/templates/task-script.py`. Save to `scripts/$name.py`.
  Python 3 standard library only, unless the repo already depends on something better. A
  one-line shell pipeline may stay a shell script.
- The output must contain **everything the model step needs** (for example, the first lines of
  a file, not just its name). If the model has to go and look, you pay for extra turns.
- Inputs as arguments. Output **compact**: the fewest lines that carry the answer, with a
  `--limit` cap on anything that can grow. That output is what a model will read on every run.
- Exit 0 on success, including "nothing found". Exit non-zero only on a real failure: in a skill,
  a failing injected command aborts the run before the model sees anything, which is the cheap
  way to fail.

## 4. Test the script
Run it on a real input and on an empty or bad one. Report `wc -c` of the output: that's the
context cost per run. Fix it if the output is larger than the task needs.

## 5. Add a skill only if a model step is left
- **No model step:** stop here. The command is `python3 scripts/$name.py …` and costs no tokens.
- **Model step:** write `.claude/skills/$name/SKILL.md` from
  `${CLAUDE_SKILL_DIR}/templates/task-skill.md`. The script runs through `!` injection before
  the model sees the prompt, the skill pins `model: haiku` and `effort: low`, and the task
  section holds only the judgment step with an exact output format.
- Test it once, unattended:
  `${CLAUDE_SKILL_DIR}/bin/claude-run $name <sample args>`.
  It prints the result and, on stderr, the turns, the cost and any permission denials.
  - **Denials or more than 1 turn** mean the model went looking for data: add it to the
    script's output. Don't grant tools. `disallowed-tools` didn't stop these attempts under
    `-p` in testing (v2.1.316), so don't rely on it.
  - **A program will read the output:** pass a JSON Schema with `claude-run -j schema.json`.
    The answer is then validated. In one test it cost about 3 turns instead of 1, so use it
    only when the format must be exact.
  - **Haiku's answer is wrong:** raise the skill to `model: sonnet` and say so. Don't raise
    effort first.

## 6. Register it
- Add one row to `scripts/INDEX.md` (create it with the header below if missing):
  `| scripts/$name.py | what it does | example command | skill: /$name or — |`
- Make sure the project `CLAUDE.md` has this line, and add it if not:
  `Before mechanical or repeated work, check scripts/INDEX.md and run a listed script.`

```markdown
# Scripts index
| Script | What it does | Example | Skill |
|---|---|---|---|
```

## 7. Reply
At most 8 lines: files created, the split (scripted vs. model), how to run it (by hand,
`/$name`, unattended with `claude-run`), output size from step 4, and the cost of the test run
from step 5 if there was one.
