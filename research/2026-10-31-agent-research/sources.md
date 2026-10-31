# Sources: how agents should research and plan for delegation

*As of 2026-10-31. Ranked by usefulness to the question, not by popularity.*

**Status:**
- **✓** checked against the original page text on 2026-10-31.
- **~** read by a worker through a fetch tool's summary.
- **⚠** host blocked in this environment; seen only in search snippets.

**Stars** are as shown on each repo page on 2026-10-31. **Last commit** comes from `git log -1`
on a shallow clone made the same day.

## Anthropic primary sources

| # | Source | Date | Status | Evidence | Verdict |
|---|---|---|---|---|---|
| 1 | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | 2025-06-13 | ✓ | Production data: 90.2% (Opus 4 + Sonnet 4, internal eval), 15x tokens, 80%/95% variance, up to 90% faster, failure anecdotes | **The** core source on orchestrator–worker research. Model names are now outdated, but the design advice still holds. |
| 2 | [Cookbook research prompts](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents/prompts) (`research_lead_agent.md`, `research_subagent.md`, `citations_agent.md`) | repo last commit 2026-10-29; file dates not checked | ✓ (raw files) | Prompts behind #1 | The most concrete brief checklist and budget rules anywhere. Uses custom tool names and has an internal 5-call contradiction, so adapt rather than copy. |
| 3 | [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5) | current | ✓ | Model behaviour notes | Required reading: over-delegation, over-verification, length calibration. It updates 2025 advice. |
| 4 | [When to use multi-agent systems (and when not to)](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them) | 2026-01-23 | ✓ | 3–10x tokens; role-split experiment | The best "should I delegate?" guide: three valid reasons, and why splitting by role creates a telephone game. |
| 5 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 2025-09-29 | ✓ | Opinion and design | Subagent returns of 1,000–2,000 tokens, compaction, just-in-time retrieval, context rot. |
| 6 | [Claude Code: sub-agents docs](https://code.claude.com/docs/en/sub-agents) | current | ✓ | Reference | Frontmatter, nesting (three layers), Task→Agent rename (v2.1.63), background tool set. |
| 7 | [Agent SDK: subagents](https://code.claude.com/docs/en/agent-sdk/subagents) | current | ✓ | Reference | What a subagent receives (only the prompt string), concurrency and depth limits, injection scanning. |
| 8 | [Claude Code: best practices](https://code.claude.com/docs/en/best-practices) | current | ✓ | Opinion | The "What you can stop doing" table: no smarter answer from a subagent, but a fresh reviewer helps. |
| 9 | [Multi-agent coordination patterns](https://claude.com/blog/multi-agent-coordination-patterns) | 2026-04-10 | ✓ | Opinion | Five patterns. Start with orchestrator-subagent. A verifier without criteria rubber-stamps. |
| 10 | [Claude Code: dynamic workflows](https://code.claude.com/docs/en/workflows) | current (2026) | ✓ | Reference | The bundled `/deep-research`, limits, and "unverified ≠ refuted". Use it when a task needs dozens of agents. |
| 11 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 2026-01-09 | ✓ | Method | 20–50 tasks from real failures; grade outcomes; give judges an "Unknown" option. |
| 12 | [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) | 2026-03-24 | ✓ (key quotes) | $9 solo vs $200 harness; skeptical-evaluator finding | Separate, skeptical evaluators beat self-critique. |
| 13 | [Claude Code: skills](https://code.claude.com/docs/en/skills) | current | ✓ | Reference | Commands merged into skills, `$ARGUMENTS`, 500-line limit. |
| 14 | [Claude Code: permissions](https://code.claude.com/docs/en/permissions) | current | ✓ | Reference | deny → ask → allow order; `WebFetch(domain:…)`; Bash wildcards. |
| 15 | [Eval awareness in BrowseComp](https://www.anthropic.com/engineering/eval-awareness-browsecomp) | 2026-03-06 | ✓ | 0.87% vs 0.24% unintended solutions | A niche but real risk for search-heavy multi-agent systems. |
| 16 | [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | current | ~ (raw per worker) | Opinion | The "colleague with minimal context" test, and explaining why. The basis for `brief-reviewer`. |
| 17 | [Building a C compiler with parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) | 2026-02-05 | ~ | 16 agents, ~$20k, no orchestrator | Shows lock-based self-selection, and where it fails (one giant task). |
| 18 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 2025-11-26 | ~ | Opinion | Progress files and feature lists for handoffs. Its context-reset advice was later softened. |
| 19 | [Equipping agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | 2025-10-16 | ✓ (date) / ~ | Opinion | Progressive disclosure. Background for how skills load. |
| 20 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 2024-12-19 | ✓ (date) / ~ | Opinion | Older but foundational vocabulary (orchestrator-workers, evaluator-optimizer). |

## Repositories

| # | Repo | Stars | Last commit | Status | What it contains | Verdict |
|---|---|---|---|---|---|---|
| 1 | [tomkd555/research-skill](https://github.com/tomkd555/research-skill) | 0 | 2026-10-30 | ✓ (raw files) | Plugin with `research-collector`, `research-verifier`, `research-team` skill, `fetch_page.py`, quote-check script, `research/{date}-{slug}/` runs | The best research design found despite having no stars: budgets, disconfirm search, script-checked quotes, a verifier that never sees the report. This toolkit's `researcher` and `claim-verifier` follow its shape. |
| 2 | [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) (`deep-research/`) | 1.5k | 2026-10-31 | ✓ (raw) | 36 KB P0–P7 research skill, task-board brief fields, citation registry, anti-pattern list | The richest brief fields (Decision Question, Disconfirming Evidence, Stop Rule) and "notes are routing aids, not authorities". Too long to adopt whole. |
| 3 | [pedrohcgs/claude-code-my-workflow](https://github.com/pedrohcgs/claude-code-my-workflow) | 1.7k (3.1k forks) | 2026-09-27 | ✓ (raw) | 18 agents incl. `claim-verifier`, 37 rules, `research-agent-laws.md`, compaction hooks | The best example of CLAUDE.md, rules, hooks and a verification culture. Injection-safe verifier wording. Ships allow-all permissions: don't copy those. Academic-specific. |
| 4 | [obra/superpowers](https://github.com/obra/superpowers) | 309.5k | 2026-10-21 | ✓ (raw) | `writing-plans`, `subagent-driven-development`, `dispatching-parallel-agents` skills | The reference for plan → fresh subagent per task → review, and decision ledgers. Coding-oriented. |
| 5 | [github/spec-kit](https://github.com/github/spec-kit) | 144.1k | 2026-10-30 | ✓ (raw templates) | spec → plan → tasks command templates, `NEEDS CLARIFICATION`, constitution gate | The canonical spec-driven chain. Heavy for small work (see Böckeler's critique, ⚠). |
| 6 | [wshobson/agents](https://github.com/wshobson/agents) | 42.0k | 2026-10-30 | ✓ (raw) | 94-plugin marketplace, `agent-teams/team-lead.md`, `conductor`, ARCHITECTURE.md | Best on packaging at scale: granular plugins, 150-line context cap, one owner per file. Many of its agents are generic. |
| 7 | [EveryInc/compound-engineering-plugin](https://github.com/EveryInc/compound-engineering-plugin) | 25.8k | 2026-10-30 | ✓ (raw `ce-plan`) | brainstorm → plan → work → review → compound skills | Separates the WHAT from the HOW, with output tiers. Its "default to heavier tier" rule conflicts with tomkd555's. |
| 8 | [anthropics/claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos) (`research-agent/`) | 2.8k | 2026-03-13 | ✓ (raw) | Python SDK lead / researcher / analyst / writer with file handoff and subagent tracking hooks | Useful for the file-handoff layout. **Outdated:** `Task` tool name, all-`haiku`, `bypassPermissions`, no verification. |
| 9 | [anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) | 54.0k | 2026-10-29 | ✓ (prompt files) | `patterns/agents/prompts/`, agent notebooks, `claude_agent_sdk/` | Home of the published research prompts (primary source #2). |
| 10 | [Weizhena/Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills) | 2.4k | 2026-08-23 | ~ (README only) | `/research`, `/research-deep`, `/research-report`, human-in-the-loop outline | A good pattern for "entity × fields" breadth research. Agent files not read. |
| 11 | [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) | not captured | 2026-08-10 | ✓ (README, config) | Supervisor plus parallel researchers, compression step, defaults of 5 concurrent units / 6 iterations / 10 tool calls | The only repo with published benchmark runs (RACE 0.4309–0.4943, tokens and cost). The leaderboard is offline. |
| 12 | [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) | 13.0k | 2026-10-30 | ✓ (Explore prompt) | Extracted built-in prompts (Explore, Plan, general-purpose) | Shows how the built-in read-only agents are framed. A third-party extraction. |
| 13 | [199-biotechnologies/claude-deep-research-skill](https://github.com/199-biotechnologies/claude-deep-research-skill) | 1.2k | 2026-04-11 | ~ (README) | Tiered skill, `validate_report.py`, `verify_citations.py` | A validate-fix-retry loop worth borrowing. Its "outperforms OpenAI/Gemini" claim has no benchmark. |
| 14 | [dimayip/research-agent](https://github.com/dimayip/research-agent) | 0 | 2026-04-30 | ✓ (raw) | Skill port of Anthropic's lead / subagent / citations prompts (Chinese) | A faithful port, but keeps non-Claude-Code tool names. Use the originals (#2) instead. |
| 15 | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 26.2k | 2026-10-30 | ✓ (raw) | Large catalogue of agent files | Correct frontmatter, but the bodies are keyword checklists with no procedure, output contract or stop rule. **Anti-example.** |
| 16 | [OneRedOak/claude-code-workflows](https://github.com/OneRedOak/claude-code-workflows) | 3.9k | 2026-10-08 | ~ (README) | Command + agent + workflow-doc triples (review only) | A tidy packaging idea. Not research. |
| 17 | [automazeio/ccpm](https://github.com/automazeio/ccpm) | 8.4k | 2026-10-19 | ~ (README) | PRD → epic → tasks under `.claude/epics/` | Another spec chain. Nothing new for research. |
| 18 | [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 56.9k | 2026-10-31 | ~ | Curated list | Used only to find repos. |
| 19 | [anthropics/skills](https://github.com/anthropics/skills) | 185.4k | 2026-10-28 | listing only | Official skills plus spec/template | The format reference for skills. Not research-specific. Not read in depth. |

## Papers and independent write-ups (all ⚠: host blocked, snippets only)

| # | Source | Author/org | Date | Evidence | Verdict |
|---|---|---|---|---|---|
| 1 | [Towards a Science of Scaling Agent Systems](https://arxiv.org/abs/2512.08296) | Google Research and MIT | 2025-12 | 180 configs: +80.8% decomposable, −70% sequential; error amplification 17.2x vs 4.4x | The strongest controlled evidence for "it depends on task shape". **Confirm the numbers before quoting them.** |
| 2 | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) | Cemri et al., UC Berkeley | 2025-03 | 14 failure modes; failure rates 41–86.7% across 7 frameworks; verification step +15.6 (units unclear) | The standard failure taxonomy. 2024-era frameworks and models. |
| 3 | Single agent vs multi-agent at equal thinking budget (arXiv 2604.02460) | Tran & Kiela | 2026-04 | Single agent ≥ five multi-agent designs at equal tokens (multi-hop QA) | An important control for "is it just more tokens?". A preprint, and the ID is unconfirmed. |
| 4 | [Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) | Cognition (Walden Yan) | 2025-06 | Opinion, no numbers | The canonical dissent, partly superseded by #5. |
| 5 | [Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working) | Cognition | 2026-04-22 | Opinion | Read-only subagents work; keep writes single-threaded. **Read this one in full.** |
| 6 | [Context Rot](https://www.trychroma.com/research/context-rot) | Chroma | 2025-07 | 18 models degrade with length well before the window fills | A vendor report on 2025-era models. The direction is the point, not the numbers. |
| 7 | [BrowseComp](https://arxiv.org/abs/2504.12516) | OpenAI | 2025-04 | Accuracy scales with browsing effort; poor calibration | The benchmark behind Anthropic's variance analysis. |
| 8 | [WideSearch](https://arxiv.org/abs/2508.07999) | (affiliation unconfirmed) | 2025-08 | Multi-agent > single on broad tasks; best success ~5% | Breadth research is still hard for every system. |
| 9 | [DeepSearchQA](https://arxiv.org/abs/2601.20975) | not captured | 2026-01 | Premature stopping and hedging as failure modes | Supports explicit stop rules in both directions. |
| 10 | [AgentFold](https://arxiv.org/abs/2510.24699) | Ye et al. | 2025-10 | 36.2% BrowseComp at 30B with active context folding | Evidence for agent-controlled compression. |
| 11 | [STORM](https://arxiv.org/abs/2402.14207) | Shao et al., Stanford | 2024-02 | Perspective-guided questions improve coverage | Older. A query-generation idea worth keeping. |
| 12 | [ReWOO](https://arxiv.org/abs/2305.18323) | Xu et al. | 2023-05 | ~5x fewer tokens than ReAct (GPT-3.5 era) | Older. Plan-first works for predictable tool chains. |
| 13 | Cursor: scaling long-running autonomous coding (via [ZenML summary](https://www.zenml.io/llmops-database/scaling-multi-agent-autonomous-coding-systems)) | Cursor | 2026-01 | Self-reported: flat peers failed, planner/worker hierarchy worked | A secondary summary of a vendor claim. Directionally consistent with #5. |
| 14 | Böckeler on Spec Kit (via [dev.to summary](https://dev.to/juliantellez/agentic-harness-what-spec-driven-development-actually-is-1l8p)) | Thoughtworks | 2025 | Opinion | The main critique of spec-driven development: bloat, ignored specs. Original on martinfowler.com not reached. |

## Screened and excluded

- **SEO "best Claude Code agents" listicles and AI-generated roundups:** no primary content.
- **SuperClaude, claude-squad, Ralph variants, RIPER-5, AB Method, gstack, K-Dense
  scientific-agent-skills:** screened; either not research-specific or repeating the spec → plan
  → tasks pattern already covered by spec-kit and superpowers.
- **Gemini and OpenAI Deep Research internals:** nothing first-party was reachable or found.
