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
- Prefer CLI tools (`gh`, `jq`, `rg`) over MCP servers when both do the job.
- Keep replies short. Don't restate tool output or narrate the steps you took.
<!-- token-rules:end -->
