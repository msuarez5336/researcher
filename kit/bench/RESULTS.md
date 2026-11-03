# Benchmark results: compute-don't-read and the trim-output hook

Measured **2026-11-03** in a Claude Code cloud session (Claude Code 2.1.316). Each row is **one
run** (n=1), so read the results as direction and rough size, not as precise figures.
- Token counts come from `modelUsage`: input = uncached + cache read + cache write.
- Costs are the CLI's client-side estimate.
- Each run's input total includes the session's fixed context (system prompt, tool list), which
  is large in this environment. Compare the rows with each other, not with other setups.

Re-run on your own machine with:

```bash
python3 kit/bench/code_mode_bench.py --model sonnet --reps 3
```

## 1. Aggregating 20 JSON files (2,000 sales rows): reading vs a script (Sonnet)

| Variant | Turns | Input tokens | Output tokens | Cost | Time | Correct |
|---|---|---|---|---|---|---|
| Read the files with Read/Glob, no scripts | 22 | 201,698 | 74,943 | $1.15 | 400 s | **no** |
| Write and run a Python script | 4 | 147,043 | 490 | $0.06 | 22 s | yes |

The script was about 18 times cheaper and about 18 times faster, and it was the only correct
answer. Without a script, the model did the arithmetic in its own output, which accounts for most
of the 75K output tokens, and got it wrong. This matches the research: the gain is largest when
the task needs an aggregate over a lot of data.

## 2. Large Bash output: trim-output hook vs none

**20,000-line log (about 1.1 MB, `cat`), Sonnet.** No difference: 111,613 input tokens without
the hook, 111,636 with it, both correct, 3 turns each. Claude Code already saves very large Bash
output to a file itself (`<persisted-output>`) and shows Claude only a preview of about 2K
characters, so the hook had nothing left to save.

**450-line log (about 23K characters, `cat`), Haiku:**

| Variant | Characters Claude saw | Input tokens | Output tokens | Turns | Correct |
|---|---|---|---|---|---|
| No hook | 22,989 | 136,962 | 463 | 3 | yes |
| Hook | 3,301 | 115,503 | 304 | 3 | yes |

The hook cut what Claude saw by 86%, and the whole run's input tokens by 16%, with the same
answer.

**What this means:** the hook pays off for medium outputs, above its 8,000-character threshold
and below Claude Code's own threshold for saving output to a file. Claude Code's exact threshold
wasn't measured; it was above 23K characters here. For very large outputs, Claude Code already
does the job.

## Caveats
- One run per row, in one environment.
- The tasks were built to show the effect: one aggregation task and one log task. Real
  workloads vary.
- The "direct" aggregation prompt forbade scripts. In normal use Claude often writes a script
  anyway; the token rule makes that the default.
