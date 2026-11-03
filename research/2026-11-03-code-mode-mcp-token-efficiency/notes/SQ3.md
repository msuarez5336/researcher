# SQ3 notes (as of 2026-11-03)
## Answer
Claude Code natively supports: MCP tool deferral (tool search, on by default), MCP output caps with save-to-file, PostToolUse updatedToolOutput / PreToolUse updatedInput to trim output, an opt-in OS sandbox for Bash, and cost/usage measurement. It documents no in-product code mode (no route for a Bash script to call an MCP server); the documented route is CLIs/APIs from scripts. Programmatic tool calling is a Messages API feature (code execution container), not a Claude Code setting.

## Findings
- Tool search default-on, deferred definitions [E] SQ3-1; ENABLE_TOOL_SEARCH values [E] SQ3-2; model/platform limits [E] SQ3-3.
- Output caps: 25k tokens default, warn at 10k (cached page, line ~445, not separately recorded); save-to-file at 50k chars unaffected by env var [E] SQ3-4; server opt-in up to 500k chars [E] SQ3-5.
- CLI over MCP [O] SQ3-6; hooks as preprocessors [O] SQ3-7.
- PostToolUse updatedToolOutput [E] SQ3-8; caveats (tool already ran, telemetry sees original) [E] SQ3-9. Hook additionalContext/stdout capped at 10,000 chars (hooks page, unrecorded).
- Sandbox [E] SQ3-10. Programmatic tool calling [E] SQ3-11.
- Measurement: SQ3-12..14; /context shows context consumers and /usage shows session tokens (costs page, lines 111-113, 320; unrecorded as quotes).

## Table
| mechanism | token effect | configure | limits/version | ids |
|---|---|---|---|---|
| MCP tool search | defers tool definitions; only names load | ENABLE_TOOL_SEARCH = unset/true/auto/auto:N/false | Sonnet4/Opus4/Haiku4.5+; not Azure Foundry; off under CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS; alwaysLoad needs v2.1.285+ | SQ3-1..3 |
| MCP output limits | caps/persists big results to file | MAX_MCP_OUTPUT_TOKENS; _meta anthropic/maxResultSizeChars | 25k tokens default; 50k chars file; 500k ceiling | SQ3-4,5 |
| CLI instead of MCP | no per-tool listing | use gh/aws/gcloud via Bash | docs advice | SQ3-6 |
| PostToolUse hook | replaces result Claude sees | hooks.PostToolUse, updatedToolOutput | tool already ran; must match output shape | SQ3-8,9 |
| PreToolUse hook | rewrites command (e.g. test filter) | updatedInput | docs example | SQ3-7 |
| Bash sandbox | safe running of model-written scripts | /sandbox, sandbox.enabled, network.allowedDomains, filesystem.allowWrite | off by default | SQ3-10 |
| Programmatic tool calling | tool calls in container, only result returns | API: allowed_callers + code_execution_20260120 | Messages API; Not ZDR/HIPAA eligible; Haiku 4.5 unsupported; containers idle ~5 min | SQ3-11 |
| Measurement | tokens/cost per task | claude -p --output-format json; OTEL | estimates not bill; use modelUsage | SQ3-12..14 |

## Conflicts
Community README (unverified, via search snippet, glama.ai ptc-mcp) says Claude Code lacks API PTC and offers MCP-proxy workarounds; consistent with docs silence. Not recorded as evidence.
## Not found
Official doc of a Bash script calling an MCP server; Agent SDK doc stating PTC works in Claude Code; measured token savings from tool search (docs give none here); exact json field list in headless page (not fetched).
## Blocked
None (github not needed).
## Search log
Fetched hooks, sandboxing, costs, monitoring-usage, PTC, cost-tracking (6). Search PTC docs (1 new); search "PTC not supported in Claude Code" (disconfirm; community only); search headless json fields (1 new). Budget about 14.
