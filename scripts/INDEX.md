# Scripts index
Check here before doing mechanical or repeated work; run a listed script instead of redoing it.
Add a row whenever `/codify` (or you) adds a script.

| Script | What it does | Example | Skill |
|---|---|---|---|
| `scripts/run_status.py` | One-screen status of a research run: deliverables, evidence counts per sub-question, page cache, verdicts | `python3 scripts/run_status.py research/<run> --quotes` | — |
| `.claude/skills/research/scripts/fetch_page.py` | Cache page text for quoting | `python3 .claude/skills/research/scripts/fetch_page.py --run-dir RUN URL` | used by `/research` |
| `.claude/skills/research/scripts/check_quotes.py` | Check every evidence quote against the cached page | `python3 .claude/skills/research/scripts/check_quotes.py --run-dir RUN` | used by `/research` |
| `.claude/skills/codify/bin/claude-run` | Run a skill unattended on Haiku with limits; fail on errors or permission denials | `.claude/skills/codify/bin/claude-run <skill> [args]` | used by `/codify` |
| `backtest/fetch_data.py` | Download daily prices and volatility indexes for the option backtest; rebuild `artifact/data.js` | `python3 backtest/fetch_data.py` | — |
| `backtest/calibrate_iv.py` | Fit and test the implied-volatility estimate; write `artifact/iv_model.js` | `python3 backtest/calibrate_iv.py` | — |
| `backtest/test_engine.js` | Tests for the backtest engine | `node backtest/test_engine.js` | — |
| `backtest/run_cli.js` | Run one backtest configuration and print the comparison | `node backtest/run_cli.js '{"cond":{"metric":"ret1","x":8}}'` | — |
