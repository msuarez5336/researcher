# Token-lean kit for Claude Code

Spend tokens once, with a capable model, so every later run is cheap:
- **Scripts do the deterministic work** (fetching, filtering, counting, formatting) for zero
  tokens.
- **A small model (Haiku) does only the judgment step**, on data a script has already filtered.

## What's inside

| Path | What it does |
|---|---|
| `skills/codify/` | **`/codify <name> "<goal>"`**: splits a task into scriptable and judgment steps, writes and tests `scripts/<name>.py`, and adds a Haiku skill only if a judgment step is left. Registers the script in `scripts/INDEX.md` so later sessions reuse it. |
| `skills/codify/bin/claude-run` | **`claude-run <skill> [args]`**: runs a skill unattended on Haiku with a turn limit and a spending cap. Exits non-zero on errors **or permission denials**; plain `claude -p` can report success there. `-j schema.json` returns validated JSON. |
| `agents/haiku-runner.md` | **`haiku-runner`** subagent: a cheap executor (Haiku, low effort) for long or verbose mechanical work such as test runs, log digging and bulk listings. |
| `token-rules.md` | Short rules added to `CLAUDE.md`: check `scripts/INDEX.md` first, suggest `/codify` when steps repeat, never write out what a command can print, filter output before reading it. |
| `install.sh` | Installs all of the above. |

## Install

Requirements: macOS or Linux (or WSL), `bash`, `python3`, `jq`, and the `claude` CLI.

**For every folder you open (recommended):**

```bash
./install.sh
```

This puts the skill and agent in `~/.claude`, adds the token rules to `~/.claude/CLAUDE.md`
(the rest of that file is left alone), and links `claude-run` into `~/.local/bin`.

**For one project only** (commit its `.claude/` to share it with others):

```bash
./install.sh --project ~/work/my-app
```

Re-run either command to update. To remove the kit:

```bash
./install.sh --uninstall
```

If the files lost their executable bit while unzipping, run `bash install.sh` instead.

## Use

| You want to… | Do |
|---|---|
| Make a task repeatable | `/codify weekly-prs "summarise merged PRs since a date for the team channel"` |
| Run it by hand | `/weekly-prs 2026-10-01`, or `python3 scripts/weekly-prs.py 2026-10-01` if no model step was needed |
| Run it from cron or CI | `claude-run weekly-prs 2026-10-01` (Haiku, 8 turns, $0.50 cap) |
| Use another model or limits | `claude-run -m sonnet -t 4 -b 0.20 weekly-prs 2026-10-01` |
| Get validated JSON | `claude-run -j schema.json weekly-prs 2026-10-01` |
| See what costs tokens | `/context` (what fills the context window), `/usage` (where usage goes) |

Scripts that `/codify` creates live in each project's `scripts/` folder and are listed in
`scripts/INDEX.md`. If a project's `.claude/settings.json` uses an allowlist, add
`"Bash(python3 scripts/*)"` so the scripts can run without a prompt.

## Measured results

Measured on Claude Code 2.1.316, one run each. Costs are the CLI's own client-side estimates.

| Test | Turns | Cost |
|---|---|---|
| Haiku skill fed complete data by its script | 1 | about $0.002 (repeat about $0.0004) |
| Script left out data the task needed, so Haiku went looking, was denied, and `claude-run` exited 3 | 3 | about $0.004 |
| Same skill with `-j` schema validation | 3 | about $0.008 |
| Sonnet session handing one short command to `haiku-runner` | 2 | $0.06 total, of which Haiku $0.001 |

What these runs taught, and `/codify` now enforces:
- **The script must supply everything the model step needs.** Otherwise the model spends turns
  looking for it.
- **Don't rely on `disallowed-tools`.** In a skill, it did not stop tool attempts under `-p`.
- **Use schema mode only when a program reads the output.** It cost about 3 turns instead of 1.
- **Run a single short command directly.** Delegating it costs more than it saves.

Source: github.com/msuarez5336/researcher (`kit/`, `.claude/skills/codify/`, and the research
run `research/2026-10-31-claude-code-parameterized-runs/`).
