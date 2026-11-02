# Research toolkit for Claude Code

A reusable setup for running research with Claude Code and for planning work that other agents
carry out. Every design choice here comes from a research run that is stored in this repo:
[research/2026-10-31-agent-research/report.md](research/2026-10-31-agent-research/report.md),
with its sources in [sources.md](research/2026-10-31-agent-research/sources.md).

## Quick start

Open Claude Code in this repo, then:

```text
/research what are the tradeoffs between X and Y for Z?
```

1. **Tier.** Claude picks a tier: QUICK, STANDARD or DEEP. QUICK answers in chat with no agents.
2. **Plan.** For STANDARD and DEEP, Claude writes `research/<date>-<slug>/brief.md` with the
   sub-questions and the exact brief each worker will get. It then **waits for your OK**.
3. **Collect.** Parallel `researcher` agents collect evidence. Each caches the pages it quotes
   and writes `evidence/<SQ>.jsonl` plus `notes/<SQ>.md`.
4. **Check quotes.** `check_quotes.py` checks every quote against the cached page text.
5. **Write.** Claude writes `report.md` by theme, answer first, with evidence/opinion tags,
   disagreements and limitations.
6. **Verify.** `claim-verifier` agents check the load-bearing claims in fresh contexts. They
   never see the draft. Claude then writes `sources.md`.

To plan work for other agents without doing research first:

```text
/delegate migrate the billing service to the new API, using docs/spec.md
```

This writes a delegation plan from [templates/delegation-plan.md](templates/delegation-plan.md):
whether to delegate at all, the decomposition, self-contained briefs, how results come back and
how they get verified.

## What's in the repo

| Path | What it is |
|---|---|
| `.claude/skills/research/SKILL.md` | The `/research` procedure: tiers, plan, approval, collect, check, write, verify |
| `.claude/skills/research/scripts/` | `fetch_page.py` caches page text; `check_quotes.py` checks quotes against the cache (Python 3 stdlib only) |
| `.claude/skills/delegate/SKILL.md` | The `/delegate` procedure for turning a goal into briefs for other agents |
| `.claude/agents/researcher.md` | Worker for one sub-question: budget, disconfirming search, verbatim quotes, file outputs |
| `.claude/agents/claim-verifier.md` | Fresh-context fact-checker with explicit verdicts; never shown the draft |
| `.claude/agents/brief-reviewer.md` | Read-only check that briefs are self-contained, non-overlapping and complete |
| `.claude/skills/codify/` | `/codify`: turn a repeated task into a script plus, if needed, a Haiku skill; `bin/claude-run` for unattended runs |
| `.claude/agents/haiku-runner.md` | Cheap executor (Haiku, low effort) for long or verbose mechanical work |
| `scripts/` | Deterministic helpers, listed in `scripts/INDEX.md` (e.g. `run_status.py` for a research run) |
| `kit/` | `install.sh` and `token-rules.md`: install the token-lean kit for every project |
| `templates/` | `research-brief.md`, `delegation-plan.md`, `report.md`, `sources.md` |
| `config/settings.example.json` | Suggested permissions (see Setup) |
| `CLAUDE.md` | Standing research and delegation rules for every session in this repo |
| `research/` | One folder per run. Cached `pages/` are gitignored. |

## Setup

1. **Permissions (optional).** To stop being asked about web search, web fetch and the two
   scripts on every run, copy the example settings:

   ```bash
   cp config/settings.example.json .claude/settings.json
   ```

   It allows `WebSearch`, `WebFetch` and the two scripts, nothing else. Read it first. To
   restrict fetching to particular sites, replace `WebFetch` with `WebFetch(domain:example.com)`
   entries.
2. **Network.** In cloud sessions, the environment's network policy decides which sites can be
   fetched. If workers report blocked hosts, allow them in the environment's network settings.
   See the [cloud environments network access docs](https://code.claude.com/docs/en/cloud-environments#network-access).
3. **Using it in another project.** Copy `.claude/agents/`, `.claude/skills/` and `templates/`
   into that project, and merge the rules from `CLAUDE.md` into its own.

## Token-lean kit

The kit spends tokens once, with a capable model, so that later runs are cheap. Scripts do
everything with a single right answer for zero tokens. A small model does only the judgment
step, and it reads data a script has already filtered.

```bash
kit/install.sh                    # personal: ~/.claude, available in every project
```

```bash
kit/install.sh --project ../app   # one project: commit its .claude/ to share it
```

Then, in any project:

| You want to… | Do |
|---|---|
| Make a task repeatable | `/codify weekly-prs "summarise merged PRs since a date for the team channel"` |
| Run that task by hand | `/weekly-prs 2026-10-01` (or `python3 scripts/weekly-prs.py …` if no model step was needed) |
| Run it from cron or CI | `claude-run weekly-prs 2026-10-01` (Haiku, 8 turns, $0.50 cap; exits non-zero on denials) |
| Get validated JSON | `claude-run -j schema.json weekly-prs 2026-10-01` |

The token rules installed into `CLAUDE.md`:
- Check `scripts/INDEX.md` before doing mechanical or repeated work.
- Suggest `/codify` when steps repeat.
- Give long mechanical work to `haiku-runner`.
- Never write out what a command can print.
- Filter output before reading it.

Measured in this repo on 2026-11-02 (Claude Code 2.1.316, one run each; costs are the CLI's
client-side estimates):

| Test | Turns | Cost |
|---|---|---|
| Haiku skill fed complete data by its script | 1 | $0.002 first run, $0.0004 repeat |
| Same skill when the script left out data the task needed: Haiku went looking, got denied, and `claude-run` exited 3 | 3 | $0.004 |
| Same skill with `-j` schema validation | 3 | $0.008 |
| Sonnet session delegating one short command to `haiku-runner` | 2 | $0.06, of which Haiku $0.001 |

Lessons from these runs, built into `/codify`:
- The script has to supply everything the model step needs.
- `disallowed-tools` in a skill did not stop tool attempts under `-p`.
- Use schema mode only when a program reads the output.
- Don't delegate a single short command.

## Why it's built this way

Each choice maps to a section of the [report](research/2026-10-31-agent-research/report.md):

| Choice | Based on |
|---|---|
| Tiers with agent and tool-call budgets; QUICK runs no agents | Anthropic's effort-scaling rules; the Opus 5 guide on over-delegation (§1, §2) |
| Brief anatomy, plus completeness and overlap tests | Anthropic's cookbook lead prompt; the vague-brief failure example; daymade and tomkd555 brief fields (§3) |
| Blocking sub-questions first, then fan out; one writer | Anthropic lead prompt; Cognition 2026; LangChain; superpowers (§4) |
| Workers write files and return ≤300 words | Anthropic context-engineering post; Agent SDK docs (§5) |
| Disconfirming search in the first half of the budget | tomkd555 `research-collector`; daymade (§2) |
| Cached pages plus script-checked quotes | Summarising fetch tools paraphrase quotes (observed in the founding run; tomkd555) (§2, §7) |
| Fresh-context verifier with explicit verdicts, never shown the draft | tomkd555 and pedrohcgs verifiers; Anthropic on rubber-stamping verifiers (§7) |
| "Unverifiable" is not "refuted" | Claude Code `/deep-research` workflow docs (§7) |
| No generic "double-check your work" lines | Opus 5 prompting guide (top pattern 10) |
| Approval gate after planning, then no pauses | conductor/ce-plan vs superpowers, reconciled (disagreements table) |

The model choices are opinion, not measured: Sonnet for researchers and the brief reviewer,
Opus for the claim verifier. Change the `model:` lines if your costs or results suggest otherwise.

## When to use something else

- **Quick cited answer with no plan step:** use Claude Code's built-in `/deep-research` workflow.
- **Dozens or hundreds of agents:** use a [dynamic workflow](https://code.claude.com/docs/en/workflows).

## Known gaps

The founding run couldn't reach arXiv and several other non-Anthropic sites, so some numbers in
the report are marked unverified. Re-run verification on those items once the hosts are allowed.
No source measured which brief format works best. Building a small eval set (about 20 real
queries) from your own runs is the way to tune the tiers and agents.
