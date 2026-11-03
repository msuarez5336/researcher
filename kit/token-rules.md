<!-- token-rules:start (installed by kit/install.sh; edit the source in the researcher repo) -->
## Token rules
- Before mechanical or repeated work, check `scripts/INDEX.md` and run a listed script.
- If you do the same mechanical steps a second time, suggest `/codify <name> "<goal>"`.
- Give long or verbose mechanical work (test or build runs, log digging, many-file listings,
  bulk reformatting) to the `haiku-runner` subagent. A single short command is cheaper to run
  directly. Keep design, debugging and writing here.
- Don't write out text a command can produce (lists, counts, diffs, tables from data): run
  the command and show its output.
- Filter before reading: `rg`, `head`, `jq`, `--name-only`, failures-only test output. Never
  read a whole large file or log.
- Compute, don't read: for 3+ dependent tool calls, or large data where you need a count, total,
  filter or join, write a short script (CLI or API) that prints only the answer, and run it.
  For 1-2 calls with small results, call the tool directly; a script costs more there.
- Prefer CLI tools (`gh`, `jq`, `rg`) over MCP servers when both do the job. Keep MCP tool
  search on, and script big MCP results rather than raising `MAX_MCP_OUTPUT_TOKENS`.
- Output marked `[token-kit: trimmed ...]` was saved to a file: query that file, don't re-print it.
- Keep replies short. Don't restate tool output or narrate the steps you took.
<!-- token-rules:end -->
