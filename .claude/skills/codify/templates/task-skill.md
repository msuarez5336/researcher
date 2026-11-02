---
description: <What it does, one line>. Run with /<name> <args>.
argument-hint: <args>
disable-model-invocation: true
model: haiku
effort: low
allowed-tools: Bash(python3 scripts/<name>.py *)
---

## Data
Computed and filtered by `scripts/<name>.py` before you were called. It is complete: answer
from it alone, without tools.

!`python3 scripts/<name>.py $ARGUMENTS`

## Task
<Only the judgment step. Example: "From the items above, pick the three that need action this
week and say why in one line each.">

## Output
<Exact format. Example: "A markdown list of 3 items, `- <item>: <reason>`.">
Nothing else: no preamble, no restating the data, no closing summary.
