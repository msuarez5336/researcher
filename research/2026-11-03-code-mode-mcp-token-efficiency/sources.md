# Sources: code mode / code execution with MCP, for the token-lean kit

*As of 2026-11-03. Ranked by usefulness to the kit decision.*
- **Status:** ✓ quote checked against the cached page · ~ read only via a summary or snippet ·
  ✗ unreachable.

## Primary sources: vendors and official docs
| # | Source | Type | Date | Status | Evidence | Verdict |
|---|---|---|---|---|---|---|
| 1 | [Anthropic docs: Programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling) | Official API docs | read 2026-11 | ✓ | SQ1-19–SQ1-25 | The best source on *when not to use it* (the tau2-bench result, fixed overhead) and on limits (no Haiku 4.5, no MCP-connector tools, not ZDR-eligible). |
| 2 | [Claude Code docs: MCP](https://code.claude.com/docs/en/mcp) | Official docs | read 2026-11 | ✓ | SQ3-1–SQ3-5 | Tool search defaults and thresholds, and the output limits. Essential for the kit. |
| 3 | [Claude Code docs: Hooks](https://code.claude.com/docs/en/hooks) | Official docs | read 2026-11 | ✓ | SQ3-8, SQ3-9 | `updatedToolOutput`, the basis for the proposed trimming hook. |
| 4 | [Anthropic: Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) | Engineering blog | 2025-11-24 | ✓ | SQ1-8–SQ1-18 | Has the measured 37% PTC figure and the tool-search numbers, both self-reported. Clear "when to use" guidance. |
| 5 | [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) | Engineering blog | 2025-11-04 | ✓ | SQ1-1–SQ1-7 | The original description of the pattern. Its 98.7% is an illustrative example, so don't quote it as a benchmark. |
| 6 | [Claude Code docs: Agent SDK cost tracking](https://code.claude.com/docs/en/agent-sdk/cost-tracking) | Official docs | read 2026-11 | ✓ | SQ3-12, SQ3-13 | `modelUsage` versus `usage`. Directly relevant to `claude-run`. |
| 7 | [Claude Code docs: Sandboxing](https://code.claude.com/docs/en/sandboxing) | Official docs | read 2026-11 | ✓ | SQ3-10 | Off by default; the safety basis for model-written scripts. |
| 8 | [Claude Code docs: Costs](https://code.claude.com/docs/en/costs) | Official docs | read 2026-11 | ✓ | SQ3-6, SQ3-7 | CLIs over MCP; hooks for preprocessing. |
| 9 | [Claude Code docs: Monitoring usage](https://code.claude.com/docs/en/monitoring-usage) | Official docs | read 2026-11 | ✓ | SQ3-14 | OpenTelemetry token metrics, for future measurement. |
| 10 | [Anthropic API release notes](https://platform.claude.com/docs/en/release-notes/overview) | Official release notes | read 2026-11 | ✓ | SQ1-26–SQ1-30 | Dates the move from beta to no beta header, and the code execution tool versions. |
| 11 | [Anthropic docs: PTC (alternate URL)](https://platform.claude.com/docs/agents-and-tools/tool-use/programmatic-tool-calling) | Official API docs | read 2026-11 | ✓ | SQ3-11 | The same topic as #1 at a different path. |
| 12 | [Cloudflare: Code Mode MCP (Feb 2026)](https://blog.cloudflare.com/code-mode-mcp/) | Vendor blog | 2026-02-20 | ✓ | SQ1-35–SQ1-38 | The 99.9% figure counts definition tokens. Useful critique of tool search. Self-reported. |
| 13 | [Cloudflare: Code Mode (Sept 2025)](https://blog.cloudflare.com/code-mode) | Vendor blog | 2025-09-26 | ✓ | SQ1-31–SQ1-34 | The original Code Mode post. Partly superseded by #12. |
| 14 | [Cloudflare: enterprise MCP](https://blog.cloudflare.com/enterprise-mcp) | Vendor blog | 2026-04 | ✓ | SQ1-39 | 94% on its internal portal, self-reported. |
| 15 | [Cloudflare changelog: MCP portal Code Mode](https://developers.cloudflare.com/changelog/post/2026-03-26-mcp-portal-code-mode/index.md) | Official changelog | 2026-03-26 | ✓ | SQ1-40 | Shipping status only. |

## Independent evidence and papers
| # | Source | Type | Date | Status | Evidence | Verdict |
|---|---|---|---|---|---|---|
| 16 | [AIMultiple: code execution with MCP](https://research.aimultiple.com/code-execution-with-mcp) | Independent benchmark | 2025-12-22 | ✓ | SQ2-1–SQ2-3, SQ2-5 | The only independent task-level measurement found: 78.5% input saved, 2.2× output. One model (GPT-4.1). |
| 17 | [Felendler et al., arXiv 2602.15945](https://arxiv.org/abs/2602.15945) | Preprint (security) | 2026-02-17 | ✓ (abstract) | SQ2-10, SQ2-11 | The key counterweight on security. Only the abstract was read, because the PDF was unsupported by the fetch script. |
| 18 | ["Bitter Lesson of Tool Calling", arXiv 2608.06370](https://arxiv.org/abs/2608.06370) ([HTML](https://arxiv.org/html/2608.06370)) | Preprint, 14 models on BFCL v4 | 2026-08-06 | ✓ / ~ (GPT-5 latency figure) | SQ2-7–SQ2-9 | Multi-model accuracy and latency. Not peer-reviewed. |
| 19 | [CodeAct, arXiv 2402.01030 (ICML 2024)](https://arxiv.org/html/2402.01030v4) | Peer-reviewed paper | 2024-06 | ✓ | SQ2-6 | Foundational evidence for code-as-action; older. |
| 20 | [Maxim AI / Bifrost: cutting MCP token costs](https://www.getmaxim.ai/articles/cutting-mcp-token-costs-by-92-at-500-tools/) | Vendor article | unknown | ✓ | SQ2-4 | Shows savings growing with tool count; self-reported. |

## Practitioner and trigger material
| # | Source | Author/org | Date | Status | Verdict |
|---|---|---|---|---|---|
| 21 | LinkedIn post on Code Mode (screenshot from the owner) | Teja Reddy Chinta | about 2026-11-02 | ~ (screenshot only; login-walled) | The trigger for this run. Its numbers are estimates from rehearsal runs; not checked. |

## Unreachable or limited (✗)
- **github.com:** HTTP 400 to `fetch_page.py`.
- **`gh api`:** HTTP 403 ("GitHub access not enabled for this session") for every repository
  tried. Repositories named only in a search snippet, with stars and commits not obtained:
  codemode-mcp, lootbox, code-mode-tools, mcp_codemode, code2mcp.
- **arxiv.org PDF (2602.15945):** unsupported by the fetch script; the abstract page was used.
- **A glama.ai README** saying Claude Code lacks programmatic tool calling: search snippet only,
  in the SQ3 notes, not used as evidence.

## Screened and excluded
- SEO explainers that restate Anthropic's post without new data.
