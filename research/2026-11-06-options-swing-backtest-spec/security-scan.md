# Skill search and security scan

As of 2026-11-06. Goal: find existing skills that could help an options swing-backtest research
run, and scan each one before any agent reads or runs it.

## Search
- claude.ai skill catalog (`SearchSkills`: options backtesting, trading strategy, quant finance,
  backtest): no results.
- claude.ai plugin catalog (`SearchPlugins`): only an accounting-focused "Finance" plugin. Not relevant.
- GitHub code and repository search plus one web search. Four candidates picked by relevance
  and maintenance (last commit within 30 days).

## Method
Sparse clone (`--depth 1 --filter=blob:none`) of only the skill folder, into an isolated scratch
directory outside the repo. Nothing was imported, installed or executed. A static scanner
(stdlib Python, run with `python3 -I`) grepped every file for: network calls, shell or code
execution, secret or credential access, writes outside the project (`~/.claude`, shell rc files,
`settings.json`), prompt-injection phrasing, hooks / MCP servers / `allowed-tools`, obfuscation
(long base64, hex escapes), hidden Unicode (zero-width, bidi), HTML comments, and order-placement
code. Every hit was then read by hand.

## Results

| Skill (repo, last commit) | Licence | Files | Hits after manual review | Verdict |
|---|---|---|---|---|
| `massive-options`, `massive-backtest` ([massive-com/ai](https://github.com/massive-com/ai), 2026-10-28) | MIT | Markdown only; `plugin.json` has no hooks or MCP servers | Documented `curl` calls that read `MASSIVE_API_KEY` from the environment. This is the vendor's own API usage. No auto-install, no hooks. | **Clean.** Useful as a reference on data availability. Needs a paid key, so it can't run here. |
| `backtest-expert` ([tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills), 2026-11-06) | MIT | SKILL.md, 2 references, `evaluate_backtest.py` (stdlib only: argparse, json, math, decimal) | `subprocess` appears only in its unit test, which runs the script itself | **Clean.** The best fit for the validation phase (hypothesis → stress test → out-of-sample (OOS) → decision gates). |
| `backtesting-frameworks` ([wshobson/agents](https://github.com/wshobson/agents), 2026-11-05) | see repo | Markdown only | none | **Clean.** Generic and adds little beyond `backtest-expert`. |
| `swing-options-trader` ([zeroes-ones/Skills](https://github.com/zeroes-ones/Skills), 2026-10-14) | no licence file found | 45 KB SKILL.md plus references, a structural `verify-skill.sh` (grep only) | none that matter (two benign HTML comments) | **Clean but not adopted.** Its performance claims ("1,068-trade backtest") are self-reported and unsourced, and the licence is unclear. |

## Decision
- Nothing is installed into `.claude/skills/`. The repo's own `/research` skill covers the
  procedure, and none of the candidates passes the repo's sourcing bar on its own.
- Two findings from the scanned skills go into the research as **claims to verify**, not facts:
  1. Massive (formerly Polygon.io) says historical Greeks and IV "do not exist on any plan". You
     compute them from the quote. This affects Phase 2.
  2. backtest-expert says: at least 30 trades, 100+ preferred; slippage stressed to 1.5–2×. This
     affects Phase 5.
- Workers are told that skill text is data, not instructions.
