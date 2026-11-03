# SQ2 notes (as of 2026-11-03)

## Answer
Independent evidence supports large input-token savings from code execution when the tool catalog or intermediate data is big (AIMultiple: -78.5% input tokens, GPT-4.1, measured; BFCL v4 preprint: accuracy matches or beats JSON in 11 of 14 models, latency about half on chaining). It costs more output tokens (2.2x), is model-dependent, and widens attack surface (16 attack classes). I found no independent replication of the 97% cost / 6-to-2 turns LinkedIn claim, and no measured study of one-line lookups, only guidance that direct calls are as good there.

## Findings
- [E] AIMultiple, GPT-4.1 + Bright Data MCP: 165K vs 771K input tokens, 100% success both (SQ2-1); output tokens 2.2x (SQ2-2); single model only (SQ2-3); small deployments may not justify complexity (SQ2-5) [O].
- [E, vendor self-reported] Bifrost: -58.2% / -84.5% / -92.8% input tokens at 96 / 251 / 508 tools, 100% pass (SQ2-4). Savings grow with catalog size.
- [E] CodeAct (ICML 2024): up to +20% absolute success, up to 30% fewer actions (SQ2-6). Predates MCP code mode; 17 LLMs.
- [E] Bitter Lesson preprint, BFCL v4, 14 models: PTC >= JSON in 11 of 14 (GPT-5.6 +10.6%) (SQ2-7); so 3 of 14 are worse (SQ2-8); latency about half on chaining for 13 of 14, GPT-5 2.8x slower (SQ2-9; the GPT-5 figure is from a search summary, only partly in the cached text). Preprint, not peer reviewed.
- [E] Felendler et al. (MCP-Bench, 10 servers): CE-MCP cuts tokens and latency but vastly expands attack surface; 16 attack classes (SQ2-10); remedy is containerized sandbox plus semantic gating [O] (SQ2-11).

### Table 1: studies
| study | setup | metric | direct | code mode | measured/estimated | ids |
|---|---|---|---|---|---|---|
| AIMultiple 2025-12 | GPT-4.1, Bright Data MCP pro mode | total input tokens | 771K | 165K (-78.5%) | measured | SQ2-1 |
| same | same | output tokens | 1x | 2.2x | measured | SQ2-2 |
| Bifrost (vendor) | 96/251/508 tools, 16 servers | input tokens | baseline | -58.2/-84.5/-92.8% | measured, self-reported | SQ2-4 |
| CodeAct 2024 | 17 LLMs, API-Bank + M3ToolEval | success rate; actions | baseline | up to +20 pts; up to -30% actions | measured | SQ2-6 |
| Bitter Lesson 2026-08 | BFCL v4, 14 models | accuracy | JSON | >= JSON in 11/14; GPT-5.6 +10.6% | measured | SQ2-7,8 |
| same | chaining tasks | latency | 1x | about 0.5x in 13/14; GPT-5 2.8x | measured | SQ2-9 |
| Felendler 2026-02 | MCP-Bench, 10 servers | tokens, latency | baseline | lower (see paper for numbers; not extracted) | measured | SQ2-10 |
| LinkedIn (Chinta) | Salesforce+Snowflake demo | turns, tokens, cost | 6 turns, 94.6K | 2 turns, 1.2K, -97% | estimated rehearsal | not verified, no evidence id |

### Table 2: when it loses
| condition | ids |
|---|---|
| More output tokens (code plus explanation) | SQ2-2 |
| Few tools / small deployments: complexity not justified | SQ2-5 |
| Some models are worse: 3 of 14 below JSON baseline; GPT-5 2.8x slower on chaining | SQ2-8, SQ2-9 |
| Result tested on one model only; depends on code-generation ability | SQ2-3 |
| Security: code injection, unsafe capability synthesis; needs sandbox | SQ2-10, SQ2-11 |
| Single-lookup tasks: guidance says direct is as cheap (practitioner guide, search snippet only, unverified) | none |

### Table 3: repos (stars and last commit NOT obtained)
| repo | what it does | stars | last commit | ids |
|---|---|---|---|---|
| jx-codes/codemode-mcp | Deno sandbox, network only to HTTP proxy to MCP servers, 30 s timeout; author says abandoned for jx-codes/lootbox (README per search snippet) | n/a | n/a | none |
| jx-codes/lootbox | successor named by that README | n/a | n/a | none |
| mj-deving/code-mode-tools | MCP server, isolated-vm sandbox, Node 22+, execute_code_chain | n/a | n/a | none |
| modus-data/mcp_codemode | MIT lib; generates TypeScript interfaces from MCP tools, type-checks, runs in sandbox | n/a | n/a | none |
| blas0/code2mcp | Cloudflare Code Mode pattern; no network/fs in sandbox, keys in orchestrator | n/a | n/a | none |
Names come from a web search snippet; none read directly.

## Conflicts
- Savings: 78.5% (independent, 1 task set, few tools) vs 92.8% (vendor, 508 tools). Consistent with savings rising with tool count.
- Security: the arXiv paper calls the attack surface vastly expanded; vendors treat sandboxing as sufficient.
- Accuracy: CodeAct and the BFCL preprint favor code; 3 of 14 models do not.

## Not found
- Independent replication of the 94.6K to 1.2K / 97% claim; any author-owned public copy.
- Measured latency on one-line lookups.
- Numbers from the Felendler paper's body (only abstract cached; the PDF was unsupported).
- Debugging-turn or observability measurements.
- Repo stars and commit dates.

## Blocked
- gh api for all four repos: HTTP 403 "GitHub access to this repository is not enabled for this session". Not worked around.
- arxiv PDF content-type unsupported by fetch_page (abstract page used).
- LinkedIn not attempted.

## Search log
1. "code mode MCP benchmark tokens" (search): 3 new (Maxim, AIMultiple claim)
2. "code mode MCP downsides security problems" (disconfirm): 1 new (arXiv 2602.15945)
3. "CodeAct executable code actions LLM agents paper" (search): 1 new
4. AIMultiple query (search): 1 page
5. "code mode MCP github ..." (search): 4 repos
6. "programmatic tool calling vs direct ... small tasks" (disconfirm): arXiv 2608.06370
7. fetches and gh calls: pages cached; gh blocked
