# Skill search and security scan

As of 2026-11-07. Goal: find third-party skills that could help an intraday / 0DTE long-option
research run, and scan each before any agent reads or runs it. Method as in
`research/2026-11-06-options-swing-backtest-spec/security-scan.md` (branch
`claude/inspiring-cerf-epxwvd`).

## Search
- claude.ai skill catalog (`SearchSkills`: options trading, 0DTE, intraday backtest, market data,
  quant finance): no results.
- claude.ai plugin catalog (`SearchPlugins`, same keywords): Blocksize Market Data (crypto market
  data), Finance (accounting), Data, FXMacroData (FX/macro calendars), others unrelated. None covers
  US option quotes or intraday backtesting. FXMacroData has release calendars but needs an MCP
  connection and an account; not used.
- GitHub (`gh api search/code`, `filename:SKILL.md 0DTE`; `search/repositories`): three candidates
  picked by relevance.

## Method
Sparse clone (`--depth 1 --filter=blob:none`, only the skill folder) into an isolated scratch
directory outside the repo. Nothing imported, installed or executed. A stdlib scanner run with
`python3 -I` grepped every file for network calls, shell/code execution, secret access, writes
outside the project, prompt-injection phrasing, hooks/MCP/`allowed-tools`, obfuscation, hidden
Unicode, HTML comments and order-placement code. Every hit was read by hand.

## Results

| Skill (repo, last commit) | Licence | Files | Hits after manual review | Verdict |
|---|---|---|---|---|
| `0dte-flow` ([mphinance/alpha-skills](https://github.com/mphinance/alpha-skills), 2026-10-26) | LICENSE file present | one SKILL.md (4 KB) | `curl` calls to api.tradier.com reading `$TRADIER_TOKEN`, including a **POST to the orders endpoint**; tells the agent to pull the token from a "VaultGuard" referenced in an AGENTS.md outside the skill | **Not used.** A personal trading playbook for a $75 account; order-placement code and an external secret store are out of place in a research run. No measured evidence. |
| `ib-0dte` ([majiayu000/claude-skill-registry](https://github.com/majiayu000/claude-skill-registry), 2026-11-07) | LICENSE file present | one 597-byte pointer page | links to a registry archive only | **Not a skill.** A pointer to an archived copy; nothing to install. |
| `0dte-trader-skill` + 3 siblings ([senderic/sender-trades](https://github.com/senderic/sender-trades), 2026-09-05) | none found | 4 Markdown files | `trade-execution-skill.md` covers live/paper Alpaca trading and reads Alpaca keys from `.env`; the 0DTE skill reads the author's own pipeline logs and a file under `~/atlas-morning-briefing/` | **Not used.** Tied to the author's private pipeline; no licence; nothing reusable for research. |

## Decision
- Nothing is installed into `.claude/skills/`, and no worker is pointed at these files. The repo's
  own `/research` skill covers the procedure.
- None of the candidates contains measured evidence about intraday option returns, so nothing from
  them enters the research as a claim.
