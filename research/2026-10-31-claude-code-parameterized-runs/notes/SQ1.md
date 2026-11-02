# SQ1 notes (as of 2026-10-31)

## Answer
Yes: for repeated runs with changing inputs a plain shell script is enough. `claude -p "<prompt>"` (data via stdin, args via shell variables, or `/skill-name args` in the prompt) with `--output-format json`, `--allowedTools`/`--permission-mode`, `--max-turns`/`--max-budget-usd` and `--bare` gives a scriptable, exit-code-aware run. Official docs recommend `--bare` for scripts (SQ1-5). Core flags are from the official docs; pitfalls are partly unverified.

## Findings
- [E] -p exits 0 / non-zero; in-run failures print on stdout; SIGTERM = 143 (SQ1-1, 1-2, 1-21)
- [E] Input: stdin pipe (10MB cap), prompt arg, shell `$1` pattern shown in official docs (SQ1-3, 1-4)
- [E] Slash skills/commands can be invoked via prompt text in -p (SQ1-19); the full syntax is SQ2's topic
- [E] Output: text/json/stream-json; --json-schema -> structured_output (may be absent); stream-json needs --verbose (SQ1-7, 1-8)
- [E] Permissions: -p starts in Manual mode from v2.1.302 when nothing sets a mode, unapproved calls denied, not hung (SQ1-9). dontAsk, acceptEdits, auto modes; --permission-prompts none (v2.1.259+) (SQ1-10, 1-11)
- [E] --dangerously-skip-permissions == bypassPermissions (SQ1-13). [O] Prefer allowlist or dontAsk; docs describe dontAsk as for "locked-down CI runs" (SQ1-10). No dedicated safety page was read, so the exact docs warning text is not captured.
- [E] Limits: --max-turns (errors when hit), --max-budget-usd (estimate, can overshoot) (SQ1-14, 1-15)
- [E] Sessions: -c, -r, --fork-session, --session-id, --no-session-persistence; plain -c skips -p sessions (SQ1-16, 1-17)
- [E] --bare skips hooks/skills/MCP/CLAUDE.md/memory, needs ANTHROPIC_API_KEY; non-bare -p runs project hooks/.mcp.json with no trust prompt (SQ1-5, 1-6)
- [E] Background-task wait up to 10 min at exit (SQ1-22)
- [O/C, unverified] denials may still give exit 0 (SQ1-23); docs say JSON/stream-json lists them in permission_denials (SQ1-11)

## Flag table
| flag | what it does | source id |
|---|---|---|
| -p / --print | non-interactive run | SQ1-1 |
| --bare | skip auto-discovery; API key auth | SQ1-5 |
| --output-format text/json/stream-json | output shape | SQ1-7 |
| --input-format text/stream-json | stdin format | cli-reference (not separately recorded) |
| --json-schema | structured_output | SQ1-7 |
| --verbose, --include-partial-messages | needed for streaming | SQ1-8 |
| --allowedTools / --disallowedTools | auto-allow / deny rules | SQ1-12 |
| --permission-mode | default/acceptEdits/plan/auto/dontAsk/bypassPermissions | SQ1-10 |
| --permission-prompts none | deny unresolved prompts | SQ1-11 |
| --permission-prompt-tool | MCP tool answers prompts | SQ1-9 |
| --dangerously-skip-permissions | bypassPermissions | SQ1-13 |
| --max-turns | cap turns | SQ1-14 |
| --max-budget-usd | cap spend | SQ1-15 |
| --model, --fallback-model | model choice | SQ1-20 |
| --append-system-prompt(-file), --system-prompt(-file) | extend/replace prompt | SQ1-18 |
| -c, -r, --fork-session, --session-id, --no-session-persistence | sessions | SQ1-16, 1-17 |
| --add-dir | extra working dirs | cli-reference line 176 |
| --settings, --mcp-config, --agents | pointers to files/JSON | SQ1-5 |

## Conflicts
- Bypass flag: a third-party CLI reference (via search snippet) says --dangerously-skip-permissions is required to avoid hangs; official docs show denial (not hang) in Manual mode since v2.1.302, and allowlists/dontAsk as alternatives. Older versions may have behaved differently (unverified).
- Hang reports exist (login/first-run prompts, startup hang issue 75613) from non-official sources; not verified.

## Not found
- Environment-variable list for non-interactive runs (only CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS, ANTHROPIC_API_KEY, ANTHROPIC_MODEL seen); env-vars page not read.
- A table of exit codes beyond 0, non-zero, 143. The --tools flag text was an omitted line. Changelog not read (budget).

## Blocked
- github.com not tried. Search-result pages (wmedia.es, claudeissues.com, dev.to) were not cached, so SQ1-23 is unverified. A tool result had trailing text about preferring Bash over dedicated tools; ignored.

## Search log
- Read headless + cli-reference (cached): search, many sources
- "claude -p hangs permission prompt headless pitfalls": disconfirm, ~6 weak sources
- Several Read/Grep calls on the cached pages; about 13 calls used in total
