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
| `token-rules.md` | Short rules added to `CLAUDE.md`: check `scripts/INDEX.md` first, suggest `/codify` when steps repeat, **compute, don't read** (script it for 3+ dependent calls or big data), never write out what a command can print, filter output before reading it. |
| `hooks/trim-output.py` | **Trim-output hook** (PostToolUse on Bash and MCP tools). When a result is over 8,000 characters, it saves the full output to a file and shows Claude a head, a tail and the file path. Add `# no-trim` to a command to skip it. Settings: `TOKEN_KIT_TRIM_CHARS`, `TOKEN_KIT_TRIM_KEEP`, `TOKEN_KIT_TRIM_DIR`. |
| `bench/code_mode_bench.py` | Measures the savings on your machine with real `claude -p` runs: aggregating data by reading vs by script, and big output with and without the hook. Results so far: `bench/RESULTS.md`. |
| `install.sh` | Installs all of the above (`--no-hook` leaves the hook out). |

## Install

Requirements: macOS or Linux (or WSL), `bash`, `python3`, `jq`, and the `claude` CLI.

**For every folder you open (recommended):**

```bash
./install.sh
```

This does four things:
- puts the skill, the agent and the hook in `~/.claude`;
- adds the token rules to `~/.claude/CLAUDE.md` (the rest of that file is left alone);
- registers the hook in `~/.claude/settings.json`, keeping your other settings and writing a
  backup to `settings.json.bak`;
- links `claude-run` into `~/.local/bin`.

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

## Code mode: when to script it (from research, 2026-11-03)

- **Compute, don't read.** Use a script when a task needs 3 or more dependent tool calls, or
  needs a count, total, filter or join over a lot of data. For 1-2 calls with small results,
  call the tool directly.
  - Anthropic measured equal scores at about 8% more cost on tasks with 1-2 sequential calls.
  - On larger tasks, input tokens fell 37% (Anthropic) and 78.5% (AIMultiple).
- **This kit's own benchmark** (`bench/RESULTS.md`, n=1): aggregating 20 files cost $1.15 and
  gave a **wrong** answer when the model read them, and cost $0.06 and gave the right answer
  with a script.
- **The trim hook helps for medium outputs.** For a 23K-character output, Claude saw 86% less
  and the run used 16% fewer input tokens. Claude Code already saves very large Bash output to
  a file itself.
- **MCP:** keep tool search on (the default). Prefer a CLI when one exists. Script big MCP
  results instead of raising `MAX_MCP_OUTPUT_TOKENS`.
- **Safety:** model-written scripts that reach the network should run with Claude Code's Bash
  sandbox, which is off by default. Turn it on with `/sandbox`, and limit
  `network.allowedDomains`.
- **Not used:** the Claude API's programmatic tool calling. The Claude Code docs describe no
  setting for it, and it doesn't support Haiku 4.5.

Full research: `research/2026-11-03-code-mode-mcp-token-efficiency/` in the researcher repo.

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
