# Code mode / code execution with MCP, and what the token-lean kit should take from it

*Research run `research/2026-11-03-code-mode-mcp-token-efficiency/` · as of 2026-11-03 · tier: STANDARD*

**How to read the tags:**
- **[E]** a measured result or documented behaviour.
- **[O]** a recommendation or opinion.
- **✓** the quote was checked against the cached page.
- **~** read only via a summary or snippet; not checked.
- **self-reported** a vendor's number about its own feature.

Evidence ids (for example `SQ1-12`) point to `evidence/*.jsonl`.

## Top findings

1. **The idea holds up, but the size of the saving depends on how much data or how many tools
   would otherwise pass through the model.** All the measured savings below are input-token
   savings.
   - **Independent, measured:** 78.5% fewer input tokens (165K vs 771K) on GPT-4.1, with both
     approaches succeeding on every task. [E] ([AIMultiple](https://research.aimultiple.com/code-execution-with-mcp),
     2025-12-22; SQ2-1) ✓
   - **Anthropic's own measured figure:** programmatic tool calling cut average tokens 37%
     (43,588 to 27,297) on complex research tasks. [E, self-reported]
     ([Anthropic](https://www.anthropic.com/engineering/advanced-tool-use); SQ1-12) ✓
   - **The headline figures** are a different kind of number:
     - Anthropic's 150,000 to 2,000 (98.7%) is an illustrative example. [E, self-reported]
       (SQ1-2) ✓
     - Cloudflare's 1.17 million to about 1,000 (99.9%) counts tool-definition tokens, not a
       task run. [E, self-reported] (SQ1-35) ✓
2. **It loses on small jobs, and Anthropic's own docs say so.**
   - On tau2-bench, with 1–2 sequential tool calls per turn, programmatic tool calling "left
     scores unchanged and cost roughly 8 percent more". [E]
     ([PTC docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling);
     SQ1-20) ✓
   - Anthropic recommends it for 3 or more dependent calls, large data needing only
     aggregates, filtering, and parallel work. [O] (SQ1-15, SQ1-21) ✓
   - The independent benchmark also found **2.2 times more output tokens**, because the model
     writes code. [E] (SQ2-2) ✓
3. **Claude Code has no built-in "code mode".** It does have the building blocks:
   - **MCP tool search, on by default.** Tool definitions are deferred, so only names load at
     start. [E] (SQ3-1, SQ3-2) ✓
   - **Large MCP results are saved to a file** above 50,000 characters. [E] (SQ3-4) ✓
   - **A PostToolUse hook can replace the tool output Claude sees** (`updatedToolOutput`). [E]
     (SQ3-8) ✓
   - **An OS-level Bash sandbox,** which is off by default. [E] (SQ3-10) ✓

   API programmatic tool calling is a Messages API feature, not a Claude Code setting. [E]
   (SQ3-11) ✓ It doesn't work with Haiku 4.5 (SQ1-19) ✓ or with MCP-connector tools
   (SQ1-22) ✓.
4. **In Claude Code, the practical way to get code mode is "compute, don't read".** The model
   writes a script that calls CLIs or APIs through Bash and prints only the answer.
   - The docs recommend CLIs over MCP servers for context efficiency, and document no way to
     call MCP from Bash. [O] (SQ3-6) ✓
   - `/codify` already does this for repeated tasks. The gap is one-off tasks.
5. **Security is the main cost.** A 2026 paper finds code-execution MCP "significantly reduces
   token usage and execution latency" but "introduces a vastly expanded attack surface", with
   16 attack classes. [E] ([Felendler et al.](https://arxiv.org/abs/2602.15945), arXiv,
   2026-02; SQ2-10) ✓
   - Both vendors run code in sandboxes. [E] (SQ1-4, SQ1-33, SQ1-36) ✓
   - Claude Code's sandbox has to be switched on. (SQ3-10) ✓

## What the pattern is

Both originators describe the same core move.
- **Tools become a code API.** Anthropic presents MCP servers as files in a `./servers/` tree;
  Cloudflare generates a TypeScript API. [E] (SQ1-1, SQ1-31) ✓
- **The model writes code against that API,** in a sandbox. Only what it reads and the final
  result enter context. [E] (SQ1-1, SQ1-33) ✓
- **Intermediate data stays out of context.** For example, a 2-hour meeting transcript would
  otherwise add about 50,000 tokens (illustrative). [E, estimate] (SQ1-3) ✓
- **Control flow runs in code, not in model turns.**
  - Anthropic says 20+ calls in one code block remove 19+ inference passes. This is arithmetic,
    not a timed measurement. [O] (SQ1-14) ✓
  - Conditionals in code save time to first token. [O] (SQ1-5) ✓
- **Extras:**
  - Personal data can be swapped for placeholders before it reaches the model. [O] (SQ1-6) ✓
  - State can be persisted in files.
  - Reusable skills. (SQ1 notes)

**Anthropic ships two related API features** (SQ1-18, SQ1-26–SQ1-29) ✓:
- **Tool Search Tool:** about 77K to 8.7K tokens for 50+ tools, and Opus 4.5 accuracy from
  79.5% to 88.1% on internal MCP evaluations. [E, self-reported] (SQ1-9, SQ1-10) ✓
- **Programmatic Tool Calling (PTC):** Claude writes code that calls your tools inside a code
  execution container. [E] (SQ3-11) ✓

Both launched in beta in November 2025. The 2026-02-17 release notes list them with no beta
header needed.

## How big the savings are, by kind of number

| Source | What was counted | Direct | Code mode | Saving | Kind | Evidence |
|---|---|---|---|---|---|---|
| AIMultiple (GPT-4.1, Bright Data MCP) | input tokens per benchmark run | 771K | 165K | 78.5% (but 2.2× output tokens) | measured, independent, one model | SQ2-1, SQ2-2 ✓ |
| Anthropic PTC | average tokens, complex research tasks | 43,588 | 27,297 | 37% | measured, self-reported; model and task count not stated | SQ1-12 ✓ |
| Anthropic PTC on tau2-bench | cost, 1–2 sequential calls per turn | — | — | **about 8% more** | measured, self-reported | SQ1-20 ✓ |
| Bifrost (Maxim AI gateway) | input tokens vs number of tools | — | — | 58.2% at 96 tools, 84.5% at 251, 92.8% at 508 | measured, vendor self-reported | SQ2-4 ✓ |
| Anthropic Tool Search | context taken by definitions, 50+ tools | about 77K | about 8.7K | 85% | measured, self-reported | SQ1-9 ✓ |
| Cloudflare portal | definition tokens, 52 tools | about 9,400 | about 600 | 94% | self-reported | SQ1-39 ✓ |
| Cloudflare full-API server | definition tokens | 1.17M (hypothetical equivalent) | about 1,000 | 99.9% | counted with tiktoken, self-reported | SQ1-35 ✓ |
| Anthropic progressive disclosure | definition tokens | 150,000 | 2,000 | 98.7% | illustrative example | SQ1-2 ✓ |
| LinkedIn demo (Chinta; trigger for this run) | input tokens, RevOps question | about 94.6K | about 1.2K | about 97% | estimated, "rehearsal runs", screenshot only | — (not checked) |

**Accuracy and latency:**
- **Code actions vs JSON or text actions (CodeAct, ICML 2024):** up to 20 points higher success
  and up to 30% fewer actions across 17 models. [E] (SQ2-6) ✓ This is older but foundational.
- **A 2026 preprint, 14 models on BFCL v4:** PTC matched or beat JSON in **11 of 14** models,
  so 3 of 14 did worse. [E] (SQ2-7, SQ2-8) ✓
  - On chaining tasks, latency was about half for 13 of 14 models.
  - The exception, GPT-5 at 2.8 times baseline latency, is only partly in the cached text. ~
    (SQ2-9)

## When it doesn't pay

- **One or two sequential calls with small results.**
  - Anthropic measured equal scores at about 8% more cost. (SQ1-20) ✓
  - Its docs say the fixed overhead of starting the container and writing the script can cost
    more than it saves. [O] (SQ1-21) ✓
- **Few tools.**
  - Savings shrink as the catalog gets smaller. (SQ2-4) ✓
  - AIMultiple says small deployments may not justify the complexity. [O] (SQ2-5) ✓
- **Some models.** 3 of 14 models were less accurate with PTC. (SQ2-8) ✓
- **Output-heavy runs.** Output tokens rose 2.2 times in the one independent benchmark.
  (SQ2-2) ✓
- **Untrusted inputs without a real sandbox.** See the security finding above. (SQ2-10) ✓

## What Claude Code offers (2026)

| Mechanism | What it does for tokens | How to configure | Limits | Evidence |
|---|---|---|---|---|
| MCP tool search | Loads only tool names until a tool is needed | On by default. `ENABLE_TOOL_SEARCH`: unset or `true` defers all; `auto` loads upfront under 10% of context; `auto:N` sets a custom percent; `false` loads all | Needs Sonnet 4, Opus 4 or Haiku 4.5 and later; not on Azure-hosted Foundry | SQ3-1–SQ3-3 ✓ |
| MCP output limits | Warns at 10K tokens and caps at 25K by default; text over 50,000 characters goes to a file | `MAX_MCP_OUTPUT_TOKENS`; a server can raise its own limit up to 500,000 characters | The 50,000-character file rule ignores `MAX_MCP_OUTPUT_TOKENS` | SQ3-4, SQ3-5 ✓; 10K and 25K from the cached MCP page |
| PostToolUse `updatedToolOutput` | Replaces what Claude sees from any tool | A hook in settings | The tool has already run; OpenTelemetry records the original output | SQ3-8, SQ3-9 ✓ |
| PreToolUse `updatedInput` | Rewrites the command before it runs (for example, adds a filter) | A hook in settings | — | SQ3-9 ✓ |
| Skills with `!` injection and scripts | Script output enters the prompt; the model never runs the gathering steps | `SKILL.md` (this is how `/codify` works) | — | earlier run (`2026-10-31-…parameterized-runs`) |
| Bash sandbox | OS-enforced filesystem and network limits for model-written code | `/sandbox` or `sandbox.enabled`; `network.allowedDomains` | **Off by default** | SQ3-10 ✓ |
| API programmatic tool calling | Code in an Anthropic-managed container calls your tools | Messages API `allowed_callers` with `code_execution_20260120` or later | Not a Claude Code setting; no Haiku 4.5; no MCP-connector tools; no `strict:true`; not ZDR-eligible; 90 s per cell; about 5 min idle reclaim | SQ3-11, SQ1-19, SQ1-22–SQ1-24, SQ1-30 ✓ |
| Measuring tokens | Per-run totals | `claude -p --output-format json`: use **`modelUsage`** for tokens (`usage` undercounts with subagents); `total_cost_usd` is an estimate; OpenTelemetry `claude_code.token.usage` | — | SQ3-12–SQ3-14 ✓ |

## Recommendations for the token-lean kit [O]

These are my synthesis of the evidence above, in priority order. Nothing here has been
implemented yet.

1. **Add a "compute, don't read" token rule** to `kit/token-rules.md`:
   > When a task needs 3 or more dependent tool calls, or reads large data to get a count,
   > total, filter or join, write a short script (Bash, CLI or API) that prints only the
   > answer, and run it. For 1–2 calls with small results, call the tool directly.

   Basis: the thresholds come from SQ1-15, SQ1-20 and SQ1-21. This covers one-off tasks, which
   `/codify` (repeated tasks only) doesn't.
2. **Add an output-trimming hook** (new `kit/hooks/trim-output`). It's a PostToolUse hook that,
   when a Bash or MCP result is over a threshold, saves the full output to a file and passes
   Claude a head/tail summary plus the file path.
   - Basis: SQ3-8 and SQ3-9. It applies the same idea as Claude Code's 50,000-character MCP
     rule (SQ3-4) at a lower threshold, and to Bash too.
   - Caveat: the tool still runs in full, so it saves context tokens, not execution time. Test
     it with `claude-run` before shipping.
3. **Make `claude-run` report tokens, not just cost.** Print input and output tokens from
   `modelUsage`: `usage` undercounts with subagents, and cost is only an estimate (SQ3-12,
   SQ3-13). Report output tokens separately, because code mode can raise them (SQ2-2).
4. **Add a "one-off" path to `/codify`** for a task you won't repeat. Write the script to the
   scratchpad, run it, report the answer, and don't register it in `scripts/INDEX.md`. Keep the
   current repeated-task path as is.
5. **Write down the MCP rules of thumb in the kit README:**
   - keep tool search on (don't set `ENABLE_TOOL_SEARCH=false`);
   - prefer CLIs when one exists;
   - don't raise `MAX_MCP_OUTPUT_TOKENS` to get around big results, script them instead.

   (SQ3-1–SQ3-6)
6. **Recommend the Bash sandbox for model-written scripts that touch the network,** with
   `network.allowedDomains` limited to the APIs used (SQ3-10, SQ2-10). Note in the kit that the
   sandbox is off by default.
7. **Don't build on API programmatic tool calling inside the kit.** It's for apps built on the
   Messages API or the Agent SDK, not Claude Code sessions, and it excludes Haiku 4.5, which the
   kit relies on (SQ3-11, SQ1-19).
8. **Measure before claiming savings.** Run the proposed benchmark (brief §9): one multi-call
   task done directly and with a script, recording turns, `modelUsage` tokens and cost. Then the
   kit's numbers are yours, not a vendor's.

## Where sources disagree

| Question | Position A | Position B | When each holds |
|---|---|---|---|
| How much does it save? | 94–99.9% (Cloudflare definition counts, Anthropic's example, the LinkedIn demo) (SQ1-2, SQ1-35, SQ1-39) | 37% (Anthropic, measured on tasks) and 78.5% (independent) (SQ1-12, SQ2-1) | The high figures count tool **definitions**, or are examples or estimates. Task-level runs save less. Savings grow with tool count and data size (SQ2-4). |
| Tool search or code mode? | Anthropic recommends Tool Search above 10K tokens of definitions or 10+ tools (SQ1-16) | Cloudflare: search needs a maintained search function, and each matched tool still costs tokens (SQ1-38) | Not exclusive. Claude Code already has tool search on by default (SQ3-1); scripting removes intermediate data, which search doesn't. |
| Is a sandbox enough? | Vendors run code in a V8 isolate or a managed container (SQ1-33, SQ1-36, SQ1-24) | The paper finds 16 attack classes and proposes layered defences beyond sandboxing (SQ2-10, SQ2-11) | Sandboxing is necessary but not proven sufficient, especially with untrusted tool outputs. |
| Is it more accurate? | CodeAct: up to +20 points; the preprint: ≥ JSON in 11 of 14 models (SQ2-6, SQ2-7) | 3 of 14 models worse; tau2-bench scores unchanged (SQ2-8, SQ1-20) | Model-dependent. Gains show up on chained, multi-step tasks, not on 1–2 calls. |
| Is Cloudflare's Code Mode the same as Anthropic's PTC? | Cloudflare equates them (SQ1 notes) | Anthropic's PTC runs in an API-managed container with `allowed_callers`; Code Mode is a TypeScript API in a Worker isolate (SQ3-11, SQ1-33) | Same idea, different mechanics. Don't carry one product's limits over to the other. |

## Outdated or superseded material

- **Cloudflare's September 2025 Code Mode** loaded the whole generated API into context and
  listed dynamic browsing as future work (SQ1-34). The February 2026 version replaces this with
  two tools, `search()` and `execute()` (SQ1-35).
- **The beta header `advanced-tool-use-2025-11-20`** (SQ1-18) is no longer needed; see the
  2026-02-17 release notes (SQ1-26, SQ1-27).
- **CodeAct (2024)** predates MCP code mode. It's used here as foundational evidence on
  code-as-action, not as a current benchmark.
- **The LinkedIn numbers** are estimated "rehearsal runs" and were not checked.

## Method and limitations

- **Workers.** Three `researcher` agents in one wave, with 15-call budgets: SQ1 vendors, SQ2
  independent evidence, SQ3 Claude Code. They used about 19, 17 and 14 tool calls.
- **Evidence.** 65 items. `check_quotes.py`: 65 of 65 quotes found verbatim in the cached pages.
  One item (SQ1-25) is marked unverified by its worker; it repeats SQ1-24.
- **Claim check.** Load-bearing claims were checked by fresh-context `claim-verifier` agents (see
  `verdicts/`).
- **Blocked or limited:**
  - github.com returned HTTP 400 to `fetch_page.py`.
  - `gh api` returned HTTP 403 ("GitHub access not enabled for this session") for every
    repository tried, so the open-source implementations are listed by name only, from a
    search snippet, without stars or commit dates: codemode-mcp, lootbox, code-mode-tools,
    mcp_codemode, code2mcp (SQ2 notes).
  - An arXiv PDF was unsupported by the fetch script, so the abstract and HTML pages were used.
  - LinkedIn wasn't tried.
- **Weak spots:**
  - Most savings numbers are vendor-reported.
  - Only one independent task-level benchmark (one model), plus one 14-model preprint.
  - No measurement of debugging turns or of model-written code that fails.

## Open questions

- **How much does the "compute, don't read" rule save in Claude Code itself,** on the owner's
  tasks? This is the benchmark in recommendation 8.
- **Does a PostToolUse trimming hook cut tokens without hurting answers?** It needs an A/B run
  with `claude-run`.
- **Do the open-source code-mode MCP proxies work with Claude Code?** Not checked, because
  GitHub access was blocked.
