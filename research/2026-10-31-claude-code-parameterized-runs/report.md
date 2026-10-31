# Running Claude Code repeatedly with parameters

*Research run `research/2026-10-31-claude-code-parameterized-runs/` · as of 2026-10-31 · tier: STANDARD*

Tags: [E] documented behaviour or measured outcome · [O] recommendation or opinion ·
✓ verified against the cached original · ~ read only via a summary or snippet, not verified.
Sources are the official Claude Code and Agent SDK docs as served on 2026-10-31 unless marked
otherwise. Evidence ids (e.g. `SQ1-5`) point to `evidence/*.jsonl`.

## Top findings

1. **Write the task once as a skill that takes arguments, then call it from wherever you are.**
   Custom slash commands have been merged into skills: `.claude/commands/x.md` and
   `.claude/skills/x/SKILL.md` both create `/x`, and old command files keep working. Inside the
   file, `$ARGUMENTS`, `$0`/`$1`… or named `$issue` pick up what you type after `/x`.
   [E] ([skills](https://code.claude.com/docs/en/skills); SQ2-1, SQ2-4–SQ2-6) ✓
2. **The same skill runs unattended with `claude -p "/x arg1 arg2"`.** In print mode only the
   first skill on the line loads and the rest of the line becomes its arguments. Put fixed
   settings (allowed tools, permission mode, turn and budget limits, output format) on the
   command line or in a checked-in `.claude/settings.json`. [E]
   ([skills](https://code.claude.com/docs/en/skills), [headless](https://code.claude.com/docs/en/headless);
   SQ2-10, SQ1-19, SQ2-18) ✓
3. **`--bare` is the documented recommendation for scripts, but it turns off skill discovery.**
   Bare mode skips auto-discovery of hooks, skills, commands, subagents, plugins, MCP servers,
   CLAUDE.md and auto memory. Some of these can be passed back explicitly: `--mcp-config`, and
   skills in folders named with `--add-dir`. Bare mode never uses a subscription login. On the
   Anthropic API it needs `ANTHROPIC_API_KEY` or an `apiKeyHelper`; Bedrock, Agent Platform and
   Foundry keep using their own credentials. So choose: bare mode with the prompt inlined (or in
   a file via `--append-system-prompt-file`), or normal mode with `/skill`.
   [E] ([headless](https://code.claude.com/docs/en/headless); SQ1-5) ✓ (narrowed after verifier
   verdict `partial`)
4. **Unattended runs no longer hang on permission prompts; they deny instead, and a denied run
   can still look successful.** Since v2.1.302 a `claude -p` run with no permission mode starts in
   Manual mode, where unapproved calls are denied. The exception is a run with
   `--permission-prompt-tool` set, which waits for that tool's answer. A practitioner test found such runs still exit
   0 with `"subtype": "success"`. Denials are listed in `permission_denials`, so a script should
   check that field. [E] ([headless](https://code.claude.com/docs/en/headless); SQ1-9, LEAD-1) ✓ ·
   exit-0 behaviour: [E, grade C] ([wmedia.es, 2026-07-31](https://wmedia.es/en/tips/claude-code-dangerously-skip-permissions-silent-failure); SQ1-23) ✓
5. **Pick the runner by who starts the run.** You at the keyboard: a skill. A shell script or
   cron: `claude -p`. A program that needs typed results: the Agent SDK. A GitHub event or a
   GitHub cron: `claude-code-action` with a `prompt` input. A recurring job without your machine:
   a cloud scheduled task. `/loop` lasts only as long as the session. [O, built on E]
   (SQ3-4, SQ3-9, SQ3-10) ✓

## Which setup for which situation

| You want to… | Use | Parameters go in | Evidence |
|---|---|---|---|
| Re-run a task by hand with different inputs | Skill in `.claude/skills/<name>/SKILL.md` (or a legacy command file) | Text after `/name`; `$ARGUMENTS`, `$N`, named `$arg` | SQ2-1, SQ2-4–SQ2-7 |
| Run it from a shell script, Makefile or cron | `claude -p` | Shell variables in the prompt, stdin (≤10MB), `/skill args` in the prompt, flags | SQ1-3, SQ1-4, SQ2-10 |
| Call it from Python/TypeScript and use the result | Claude Agent SDK, `query()` + `ClaudeAgentOptions` | Typed options that mirror the CLI flags; JSON Schema via `output_format` | SQ3-1–SQ3-3 |
| Run it on PRs, issues or a GitHub schedule | `anthropics/claude-code-action` | Workflow `prompt` input plus `claude_args` (any CLI flag) | SQ3-4–SQ3-8 |
| Run it on a timer without your laptop | Cloud scheduled task (minimum interval 1 hour, fresh clone) | The task's prompt | SQ3-9 |
| Run it on a timer with your local files | Desktop scheduled task | The task's prompt | SQ3-9 |
| Poll something while you work | `/loop 5m <prompt or skill>` | Interval and prompt; ends with the session | SQ3-10 |

## The reusable task: skills with arguments

- **Where the file lives.** `.claude/skills/<name>/SKILL.md` (project, commit it) or the same
  path under `~/.claude/` (personal). A `.claude/commands/<name>.md` file is the older format; it
  still works and takes the same frontmatter except `name` and `paths`, but the docs prefer skills
  for new work. [E] (SQ2-1, SQ2-3) ✓ The changelog records the merge under v2.1.3; its release
  date was not in the cached text. (SQ2-2) ✓
- **Argument syntax.** [E] All from [skills](https://code.claude.com/docs/en/skills) ✓
  - `$ARGUMENTS` is everything typed after the name. If the file has no placeholder, Claude Code
    appends `ARGUMENTS: <value>` to the prompt. (SQ2-4)
  - `$ARGUMENTS[N]` or `$N` gives one argument, counting from 0. (SQ2-5)
  - `arguments: [issue, branch]` in the frontmatter gives named `$issue`, `$branch`. (SQ2-6)
  - Quoting is shell-style: `/x "two words" next`. (SQ2-8)
  - An unmatched `$N` stays literal; an unmatched named argument becomes an empty string. (SQ2-9)
  - `argument-hint: [issue-number]` only shows a hint in autocomplete. (SQ2-7)
- **Frontmatter that sounds stronger than it is.** [E] ✓
  - `allowed-tools` pre-approves the listed tools for the turn that invokes the skill. It does
    not restrict the others; your permission settings still govern them. (SQ2-11)
  - `model` switches the model for that turn only. (SQ2-13)
  - `disable-model-invocation: true` keeps the skill user-only, so Claude won't run it on its
    own. (SQ2-14)
  - Managed settings with `allowManagedPermissionRulesOnly` make project and personal skills'
    `allowed-tools` ignored (v2.1.282+). (SQ2-15)
  - To fix the tools or model for a whole delegated task, a subagent file has `tools`,
    `disallowedTools` and `model` fields. (SQ2-24)

Minimal example (each element traced in `notes/SQ2.md`):

```markdown
---
description: Summarise a file for a given audience
argument-hint: [path] [audience]
arguments: [path, audience]
disable-model-invocation: true
allowed-tools: Read
---
Read $path and write a one-page summary for $audience.
```

Run it as `/summarise docs/spec.md "new engineers"` in a session, or
`claude -p '/summarise docs/spec.md "new engineers"' --allowedTools Read --output-format json`
from a shell.

## Making every run start the same way

- **Settings files.** [E] ([settings](https://code.claude.com/docs/en/settings); SQ2-16,
  SQ2-17) ✓ When the same key is set in several places, the highest level wins, in this order:
  1. managed settings
  2. command line (`--settings`)
  3. `.claude/settings.local.json`
  4. `.claude/settings.json`
  5. `~/.claude/settings.json`

  Committing `.claude/settings.json` gives everyone who clones the repo the same permissions,
  hooks and plugins. (SQ2-18) ✓ Environment variables are not a level in this stack; whether
  the shell or a settings file wins is decided per variable. (SQ2-19) ✓
- **CLAUDE.md is context, not configuration.** It loads at the start of every conversation.
  Files from the working directory upward are concatenated rather than overriding each other.
  It is not enforced; to block an action, use a PreToolUse hook.
  [E] ([memory](https://code.claude.com/docs/en/memory); SQ2-20–SQ2-22) ✓
- **`claude -p` loads all of this too** (hooks, skills, commands, CLAUDE.md, `.mcp.json`)
  unless `--bare` is set. In bare mode, `--settings` still supplies a settings file explicitly.
  [E] (SQ2-23, SQ1-5) ✓

## Scripted runs: `claude -p` flags that matter

All from [headless](https://code.claude.com/docs/en/headless) and
[cli-reference](https://code.claude.com/docs/en/cli-reference); full table in `notes/SQ1.md`.

- **Input.** [E] ✓
  - The prompt is an argument, and data can be piped on stdin (10MB cap; larger data should go
    in a file the prompt names). (SQ1-3)
  - The docs' own example is a `review.sh` that takes `$1` and pipes data in. (SQ1-4)
- **Exit status.** [E] ✓
  - Exit 0 on success, non-zero on failure, 143 on SIGTERM. (SQ1-1, SQ1-21)
  - Failures inside the run, such as missing auth, are printed on stdout, not stderr. (SQ1-2)
- **Output.** [E] ✓
  - `--output-format json` returns the result, `session_id` and `total_cost_usd`. (SQ1-7,
    SQ3-12)
  - `--json-schema` adds a `structured_output` field. It can be missing, so check for it.
    (SQ1-7)
  - `stream-json` needs `--verbose`. (SQ1-8)
- **Permissions.** [E] ✓
  - `--allowedTools "Bash(git diff *)"` uses permission-rule syntax. (SQ1-12)
  - `--permission-mode` takes default, acceptEdits, plan, auto, dontAsk or bypassPermissions;
    dontAsk denies anything that would prompt. (SQ1-10)
  - `--permission-prompts none` (v2.1.259+) denies prompts and tells Claude not to retry them.
    (SQ1-11)
  - `--dangerously-skip-permissions` is the same as bypassPermissions. (SQ1-13)
- **Limits.** [E] ✓
  - `--max-turns` stops the run with an error when it reaches the limit. (SQ1-14)
  - `--max-budget-usd` caps a client-side cost estimate and can be exceeded, so leave headroom.
    (SQ1-15, SQ3-1)
- **Prompt and model.** [E] ✓
  - `--append-system-prompt(-file)` adds to the default system prompt; `--system-prompt(-file)`
    replaces it. (SQ1-18)
  - `--model` and an ordered `--fallback-model` choose the model. (SQ1-20)
- **Sessions.** [E] ✓
  - `-r <id>`, `--session-id <uuid>`, `--fork-session` and `--no-session-persistence` control
    sessions. (SQ1-16)
  - Plain `claude --continue` skips sessions created by `-p`, so repeated or parallel runs
    should pass explicit session IDs. (SQ1-17)
- **Background work.** A run can stay open up to 10 idle minutes waiting for background work;
  `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS` changes the limit. [E] (SQ1-22) ✓

A safe template for an unattended run:

```bash
claude -p "/summarise $1 \"$2\"" \
  --allowedTools "Read" --permission-mode dontAsk \
  --max-turns 10 --max-budget-usd 1 --output-format json \
  | jq -e '(.permission_denials // []) | length == 0'
```

## Programmatic and automated runners

- **Agent SDK.** [E] ([Python reference](https://platform.claude.com/docs/en/agent-sdk/python);
  SQ3-1–SQ3-3) ✓
  - `ClaudeAgentOptions` carries the same parameters as the CLI: `max_turns`, `max_budget_usd`,
    `permission_mode`, `allowed_tools`, `system_prompt` and `output_format`.
  - `setting_sources` loads all filesystem settings by default. Pass `[]` to isolate a run from
    user, project and local settings.
  - Structured output comes back in `structured_output`.
  - [O] Worth it over `claude -p` when a program needs typed results, callbacks or sessions.
- **GitHub Actions.** [E] ([github-actions](https://code.claude.com/docs/en/github-actions);
  SQ3-4–SQ3-8) ✓
  - With a `prompt` input the action runs in automation mode on any trigger, cron included.
    Without one it waits for an `@claude` mention. `claude_args` passes any CLI flag.
  - Scheduled runs get no shell or GitHub API access until you grant tools. They run from the
    default branch only, and public-repo schedules are disabled after 60 days without activity.
  - Bot actors are rejected unless listed in `allowed_bots`.
  - Cost controls: `--max-turns`, workflow timeouts and concurrency limits.
- **Scheduling.** [E] ([scheduled-tasks](https://code.claude.com/docs/en/scheduled-tasks); SQ3-9,
  SQ3-10) ✓
  - Cloud tasks need no machine or open session (fresh clone, minimum interval 1 hour).
  - Desktop tasks run on your machine and can use local files.
  - `/loop` lasts only as long as the session. For anything that must outlive the session, the
    docs point to cloud or Desktop tasks or GitHub Actions.

## Pitfalls for unattended runs

- **Denied is not failed.** Denied calls don't fail the run (Top finding 4), so check
  `permission_denials`. [E] (LEAD-1, SQ1-23) ✓
- **Repo content runs without asking.** Without `--bare`, `claude -p` runs a repository's hooks
  and connects its `.mcp.json` servers with no trust dialog, even in a folder you never trusted.
  Use `--bare`, or run only on repos you trust. [E] (SQ1-6) ✓ Project skills' `allowed-tools`
  also apply in an untrusted folder under `-p`. (SQ2-12) ✓
- **Cost figures are estimates.** `total_cost_usd` and budget caps are client-side estimates
  that can differ from the bill. [E] (SQ1-15, SQ3-12) ✓

## Where sources disagree

| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Is `--dangerously-skip-permissions` needed to stop `-p` hanging? | A third-party CLI reference says yes (~, search snippet only, not cached; SQ1 notes) | Official docs: Manual mode denies instead of waiting; allowlists, `dontAsk` or `--permission-prompts none` are the alternatives (SQ1-9–SQ1-11) ✓ | B for v2.1.302+ (and v2.1.259+ for `--permission-prompts`). A may describe older versions; not checked. |
| Does argument substitution always work? | Docs describe `$ARGUMENTS`, `$N` and named arguments as working (SQ2-4–SQ2-6) ✓ | Issue reports: named `arguments:` not substituted when a skill is run through the Skill tool (reported against v2.1.241, open), and `$ARGUMENTS` broken in v2.1.101 (later closed) (~, search snippets of a third-party mirror of GitHub issues; dropped from evidence) | Typing `/name args` yourself with `$ARGUMENTS` is the documented path. When Claude invokes the skill itself, test that named arguments arrive. |

## Outdated or superseded material

- **Custom slash commands in `.claude/commands/`.** Merged into skills (changelog v2.1.3). They
  still work, but older guides that treat them as a separate system are out of date. (SQ2-1,
  SQ2-2)
- **"Claude Code SDK".** Now the Claude Agent SDK; guides using the old name may show old option
  names. (Agent SDK overview, cached)
- **Guides that say `-p` waits on permission prompts.** Behaviour changed with Manual mode
  (v2.1.302). (SQ1-9)
- **`--bare` as an opt-in.** The docs say it will become the default for `-p` in a future
  release, so scripts that rely on CLAUDE.md or skills loading in `-p` should not count on that
  lasting. (SQ1-5)

## Method and limitations

- **Workers.** Three `researcher` agents (SQ1 CLI, SQ2 files on disk, SQ3 runners), 15-call
  budget each. They used about 13, 6 and 8 calls. One wave.
- **Quote check.** `check_quotes.py`: 61 of 61 quotes found verbatim in the cached pages, after
  two quote-less items (SQ2-25, SQ2-26) were dropped and one page (wmedia.es) was cached.
- **Claim check.** Two fresh-context `claim-verifier` agents checked 10 load-bearing claims
  (`claims/batch_1.json`, `claims/batch_2.json`).
  - Result: 9 supported, 1 partial (the `--bare` claim, now narrowed), 0 unsupported,
    contradicted or unverifiable.
  - The exit-0-despite-denials detail rests on one practitioner test (wmedia.es); the official
    docs confirm only that runs continue and that denials are listed.
- **Blocked.** `github.com` returned HTTP 403 to `fetch_page.py`, so the `claude-code-action`
  README and the GitHub issue threads were not read. Action details come from Anthropic's
  GitHub Actions docs page instead. The two issue reports above stay unverified. They were not
  fetched from a third-party mirror, so as not to get around the block.
- **Not read.** The TypeScript SDK reference, the environment-variables page, and the full
  changelog. The release date of v2.1.3 is unknown.
- **Cache format.** The docs pages were cached as their raw page bundle. Quotes were matched
  against that text, so the passages are verbatim but sometimes hard to read in the cache.

## Open questions

- Whether the named-argument substitution bug via the Skill tool is fixed in the current version.
  To find out, read the GitHub issue once github.com is reachable, or test it locally.
- Whether `--bare` becoming the default for `-p` will also disable `/skill` invocation in
  scripts. Watch the changelog.
