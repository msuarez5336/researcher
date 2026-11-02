# SQ3 notes (as of 2026-10-31)

## Answer
Programmatic runs differ from `claude -p` mainly in packaging: the Agent SDK (Python/TS) passes parameters as typed options and returns structured messages; claude-code-action passes them as workflow inputs (`prompt`, `claude_args`) and event triggers; schedules come from cron/GitHub `schedule`, or Anthropic's cloud/Desktop scheduled tasks, while `/loop` is session-scoped only. Use a plain CLI call from cron/shell for simple fixed jobs; use the SDK when a program needs typed results, callbacks, or sessions; use the action when the trigger is a GitHub event.

## Findings
- SDK options mirror CLI flags: max_turns, max_budget_usd, permission_mode, allowed_tools, system_prompt, setting_sources, output_format [E] SQ3-1, SQ3-2, SQ3-3. Default setting_sources loads all filesystem settings (SQ3-2); pass [] for isolation.
- Action: interactive vs automation mode by presence of `prompt` [E] SQ3-4; `claude_args` accepts any CLI arg [E] SQ3-5.
- Scheduled action caveats: tools must be granted; default-branch only; 60-day inactivity disable; bot-actor check [E] SQ3-6, SQ3-7.
- Cost/safety: --max-turns, timeouts, concurrency [O] SQ3-8; max_budget_usd is a client-side estimate that can overshoot [E] SQ3-1; cost visible in JSON total_cost_usd [E] SQ3-12; --bare recommended for scripts [O] SQ3-11.
- Scheduling comparison [O] SQ3-9, SQ3-10: cloud (no machine, fresh clone, 1h min), Desktop (local files), /loop (session-scoped).
- Silent permission failure in headless runs [O, unverified, C] SQ3-13.

| runner | how parameters are passed | when to use | evidence |
|---|---|---|---|
| Agent SDK (Py/TS) | `query(prompt, options=ClaudeAgentOptions(...))`; output_format schema; sessions resume | program needs typed/structured results, budget caps, callbacks | SQ3-1,2,3 |
| claude-code-action | workflow `prompt`, `claude_args`, secrets; trigger = GitHub event or cron | repo events (PR, issue, @claude), daily reports | SQ3-4,5,6,7,8 |
| Cloud/Desktop scheduled tasks | task prompt configured in product | recurring work w/o your terminal (cloud) or with local files (Desktop) | SQ3-9,10 |
| /loop | `/loop 5m <prompt>` | polling inside an open session; not durable | SQ3-9,10 |
| cron + `claude -p` | CLI flags (SQ1); --bare, --output-format json | simple fixed job on your own machine/server | SQ3-11,12 |

## Conflicts
None direct. Third-party claim (SQ3-13) of exit code 0 on denied permissions is unverified against official docs.

## Not found
SDK TypeScript reference page and cloud scheduled task page not read (not fetched); sessions/resume option details only seen in overview snippet. No official failure-case/criticism source; no upstream claude-code-action issue evidence. Whether .claude/commands merged into skills: not checked here (SQ2).

## Blocked
github.com (action README) not attempted; used code.claude.com docs. wmedia.es only from search snippet.

## Search log
- fetch of 5 docs pages (search): 5 new sources.
- WebSearch "claude-code-action CI permission denied runaway cost max-turns problems" (disconfirm): 1 weak new source.
Budget used: ~8 of 15.
