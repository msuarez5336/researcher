# SQ1 notes (as of 2026-11-03)

## Answer
Both vendors describe the same pattern: stop loading every tool schema and passing every intermediate result through the model. Instead the model writes code against a typed API (files or TypeScript) that runs in a sandbox, so only discovered definitions and final results enter context. Anthropic's headline number (150K to 2K tokens, 98.7%) is an illustrative example, not a benchmark. Its measured figures are 37% fewer tokens for programmatic tool calling and 85% for tool search. Cloudflare reports 99.9% (1.17M to ~1,000 tokens) and 94% (9,400 to 600). All are self-reported. Anthropic's own docs show no benefit, and about 8% higher cost, on sequential single-call workloads.

## Findings
- Mechanism (Anthropic, Nov 4 2025): MCP servers presented as code APIs in a ./servers/ file tree; the agent lists and reads only the files it needs; filtering, loops and conditionals run in the sandbox; state is persisted to files and reusable skills; PII can be tokenized so it never reaches the model. [O] SQ1-1, 5, 6
- Anthropic 150,000 to 2,000 tokens (98.7%) is an example with no stated model or task eval. [E, self-reported] SQ1-2. The 50,000-token meeting transcript is an estimate. SQ1-3
- Anthropic stated cost: sandbox, resource limits, monitoring, operational overhead. [O] SQ1-4
- Advanced tool use (Nov 24 2025): Tool Search 77K to 8.7K tokens (85%); accuracy Opus 4 49 to 74%, Opus 4.5 79.5 to 88.1%. [E, internal] SQ1-9, 10. PTC 43,588 to 27,297 tokens (37%) on complex research tasks, knowledge retrieval 25.6 to 28.5%, GIA 46.5 to 51.2%. [E, internal] SQ1-12, 13. 200KB to 1KB is an illustration. SQ1-11. The post does not give the model, number of tasks or number of tool calls for the PTC figures. Check the original before quoting them.
- Limits stated by Anthropic docs: tau2-bench (1-2 sequential calls per turn) scores unchanged and about +8% cost [E] SQ1-20. No MCP-connector tools, no strict:true, Haiku 4.5 unsupported, not ZDR eligible, 90 s cell limit, ~4 min wait, ~5 min idle container. [E] SQ1-19, 22-25, 31
- Status/dates: PTC and tool search launched in beta Nov 2025 (header advanced-tool-use-2025-11-20) SQ1-18, 28; release notes of 2026-02-17 say no beta header is required for PTC, tool search, tool use examples and code execution SQ1-26, 27. The Claude Platform docs no longer mark PTC as beta, but I did not find an explicit "generally available" label. code_execution_20260120 (REPL state, minimum for PTC) is documented in the 2026-06-18 notes. SQ1-29
- Cloudflare: Sept 26 2025 Code Mode (TypeScript API, V8 isolate, no Internet, bindings only). [O] SQ1-32 to 35. Feb 20 2026 server-side Code Mode, search()+execute(), 1.17M to ~1,000 tokens (99.9%, tiktoken). [E] SQ1-36. Sandbox and its cost: SQ1-37, 38. Portals: 52 tools/9,400 tokens to 2 tools/~600 (94%). [E] SQ1-40; changelog dated 2026-03-26 SQ1-41.

## Table
| source | date | mechanism | number (setup) | stated costs/limits | ids |
|---|---|---|---|---|---|
| Anthropic, Code execution with MCP | 2025-11-04 | MCP as code API files, progressive disclosure, in-sandbox filtering, state, skills, PII tokenization | 150K to 2K tokens (98.7%), illustrative; 50K transcript tokens, estimate | sandbox, limits, monitoring | 1-7 |
| Anthropic, Advanced tool use | 2025-11-24 | tool search, PTC, examples | 77K to 8.7K; 43,588 to 27,297 (37%); Opus 4.5 79.5 to 88.1% (internal) | extra search/code step; beta at launch | 8-18 |
| Claude Platform docs, PTC | 2026-11 (live) | container-based PTC | tau2-bench: unchanged score, ~+8% cost | no MCP connector, no Haiku 4.5, not ZDR, timeouts | 19-25 |
| Release notes | 2025-11 to 2026-06 | status | n/a | beta to no-header 2026-02-17 | 26-30 |
| Cloudflare, Code Mode | 2025-09-26 | TS API + isolate | none | whole API loaded; pricing unfinalized | 32-35 |
| Cloudflare, Code Mode MCP | 2026-02-20 | search()/execute() | 1.17M to ~1,000 (99.9%, tiktoken) | needs sandbox on client side | 36-39 |
| Cloudflare, enterprise MCP / changelog | 2026-03/04 | portal code tool | 9,400 to 600 (94%) | n/a | 40-41 |

## Conflicts
- Cloudflare says its approach is tuned for server-side use with no client changes; Anthropic's pattern is client/agent-side with a sandbox the agent owns. Both claim large savings, but the numbers are not comparable: Cloudflare's are definition-size counts, Anthropic's headline is an example, and its measured PTC figure is 37%.
- Beta status: launch posts say beta; release notes of 2026-02-17 say no beta header. I found no explicit GA label.
- Cloudflare says Code Mode is "implemented in ... Anthropics Claude SDK as Programmatic Tool Calling" (page text); Anthropic's PTC docs describe a different mechanism (API-managed container), so treat the equivalence as Cloudflare's claim.

## Not found
- Cloudflare latency or accuracy numbers for Code Mode; any vendor measurement of bad generated code rates. WorkOS 32%/81% figures are third-party (SQ2), not recorded.
- No Anthropic statement defining when direct tool calls are preferable beyond the "when to use" lists and tau2-bench docs result.
- Code execution tool page and pricing (standalone container billing) not fetched. Release notes state code execution is free with web search/fetch.

## Blocked
None. LinkedIn page already cached by the orchestrator; not used.

## Search log
1. "Code execution with MCP: Building..." (search, 3 new). 2. advanced tool use title (search, 0 official). 3. Cloudflare Code Mode (search, 3). 4. advanced tool use engineering (search, found URL). 5. Cloudflare "better way" (search, found). 6. blog.cloudflare.com domain search (disconfirm/earlier post, 2 new). 7. platform docs PTC limitations (disconfirm, found tau2 result). Plus 4 fetch/grep batches. 14 calls used.
