# Notes B: Anthropic-authored guidance on research, delegation, context, verification

> Worker notes as returned on 2026-10-31, kept for provenance. The verified synthesis is in ../report.md; where these notes and the report differ, the report wins.

Compiled 2026-10-31. Scope: Anthropic-authored material only (engineering blog, claude.com blog, code.claude.com docs, platform.claude.com docs, claude-cookbooks repo).

## Method and verification caveats (read first)

- Tool: WebFetch returns a small-model summary or extraction of the page, not the page. Verification levels used below:
  - **[RAW]** I read the page or file text itself (the fetch returned page text, or I downloaded the file and grepped it). Quotes marked RAW are verbatim.
  - **[VIA-SUMMARY]** The fetch returned a summariser's answer to a targeted prompt. Short quoted phrases and all numbers came from that answer and were not re-checked against the page. Treat these as "likely exact, re-check before publishing in a report".
- RAW sources: the cookbook prompt files (downloaded from raw.githubusercontent.com), the Claude Code docs for permissions, memory, hooks-guide, best-practices, plugins manifest reference, create-marketplace, workflows, agent-teams; the Agent SDK subagents page; the Opus 5 prompting guide; the general prompting best-practices page. VIA-SUMMARY: all anthropic.com/engineering posts, the two claude.com blog posts, sub-agents, skills, permission-modes.
- The engineering index fetch printed paths as `/research/...`; this is a summariser artefact. The real URLs are `https://www.anthropic.com/engineering/<slug>` (confirmed for every post I opened). Two posts redirect to claude.com/blog (see source list).
- Stopped at roughly 40 tool calls. Not opened: the sub-agents page past char 100000, the skills page past char 100000, hooks reference page (only the guide), the other 2025 posts listed in the index (think tool, Desktop Extensions, advanced tool use, code execution with MCP, sandboxing, postmortems, infrastructure noise, AI-resistant evals, auto mode, source-control, containment).

---

## 1. Source list

Format: URL | title | date | what it is for | outdated?

### Core research / orchestration posts

1. https://www.anthropic.com/engineering/multi-agent-research-system | How we built our multi-agent research system | Jun 13, 2025 [VIA-SUMMARY] | THE primary source for lead/subagent research design, effort scaling, token economics, eval method. | Models named (Opus 4 lead, Sonnet 4 subagents) are pre-Claude-5: **[OLDER]**; the 90.2% figure was measured on those models and an internal eval, do not quote as a current-model number. Design guidance still matches the 2026 docs. Async execution was listed as future work; Claude Code now has background subagents and workflows (section 7).
2. https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents/prompts | `research_lead_agent.md`, `research_subagent.md`, `citations_agent.md` [RAW; downloaded] | File dates not retrievable (GitHub API refused for this session) so commit date is [UNVERIFIED]. | The actual published prompts behind post 1. Quoted extensively in section 3. | Prompt uses tools named `run_blocking_subagent`, `complete_task`, `web_search`, `web_fetch` (a custom harness, not Claude Code tool names). The "MINIMUM of five distinct tool calls" and "always deploy at least 1 subagent" rules conflict with 2026 guidance; see section 8.
3. https://www.anthropic.com/engineering/building-effective-agents | Building effective agents | Dec 19, 2024 [VIA-SUMMARY] | Workflow vs agent definitions; orchestrator-workers; evaluator-optimizer; simplicity. | **[OLDER]**, foundational. The page itself says tooling has changed since (summariser noted this). Model names inside are Claude 4.5 era in the current page text.
4. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | Effective context engineering for AI agents | Sep 29, 2025 [VIA-SUMMARY] | Context rot, compaction, note-taking, subagent returns of 1,000-2,000 tokens, just-in-time retrieval. | Concepts current. Claude Code's own docs now say window exhaustion is "rare" with 1M windows (section 8).
5. https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them | When to use multi-agent systems (and when not to) | date not captured [VIA-SUMMARY] | Token multiple 3-10x; three valid reasons; handoff loss; verification-subagent failure mode. | Current.
6. https://claude.com/blog/multi-agent-coordination-patterns | Multi-agent coordination patterns: Five approaches and when to use them | April 10, 2026 [VIA-SUMMARY] | Generator-verifier, orchestrator-subagent, agent teams, message bus, shared state. | Current.
7. https://www.anthropic.com/engineering/building-c-compiler | Building a C compiler with a team of parallel Claudes | Feb 5, 2026 [VIA-SUMMARY] | 16 parallel agents, no orchestrator, git-lock coordination; test-harness design for agents. | Current. Model names not captured.
8. https://www.anthropic.com/engineering/harness-design-long-running-apps | Harness design for long-running application development | Mar 24, 2026 [VIA-SUMMARY] | Planner / generator / evaluator; context resets vs compaction; calibrating a skeptical evaluator; strip harness parts as models improve. | Current; explicitly tracks which parts became dead weight on Opus 4.5 / 4.6.
9. https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | Effective harnesses for long-running agents | Nov 26, 2025 [VIA-SUMMARY] | Initializer + coding-agent split; feature-list JSON; progress file; git. | Mostly current. Context-reset advice later softened by post 8 and by Claude Code docs.
10. https://www.anthropic.com/engineering/managed-agents | Scaling Managed Agents: Decoupling the brain from the hands | Apr 8, 2026 [VIA-SUMMARY] | Session as durable event log outside the context window; "harness assumptions go stale". | Current.
11. https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Demystifying evals for AI agents | Jan 9, 2026 [VIA-SUMMARY] | Grader types; research-agent evals (groundedness, coverage, source quality); 20-50 tasks to start. | Current.
12. https://www.anthropic.com/engineering/writing-tools-for-agents | Writing effective tools for agents, with agents | Sep 11, 2025 [VIA-SUMMARY] | Tool design; 25,000-token cap; response_format enum. | Mentions Claude Sonnet 3.5 SWE-bench result **[OLDER]**; principles current.
13. https://www.anthropic.com/engineering/eval-awareness-browsecomp | Eval awareness in Claude Opus 4.6's BrowseComp performance | Mar 6, 2026 [VIA-SUMMARY] | Multi-agent research runs find leaked benchmark answers more often; mitigation. | Opus 4.6 is pre-5; the mechanism is still relevant to any search-heavy agent.
14. https://claude.com/blog/building-agents-with-the-claude-agent-sdk (redirected from anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) | Building agents with the Claude Agent SDK | Sep 29, 2025 [VIA-SUMMARY] | Gather context / act / verify loop; agentic vs semantic search; verification kinds. | Current.
15. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | Equipping agents for the real world with Agent Skills | Oct 16, 2025 [VIA-SUMMARY] | Progressive disclosure; skill authoring advice. | Current; config syntax lives in the Claude Code skills docs (section 9).

### Docs (code.claude.com is the live host; platform.claude.com/docs/en/agent-sdk/* 307-redirects to it)

16. https://code.claude.com/docs/en/sub-agents | Create custom subagents [VIA-SUMMARY of first 100,000 of 116,219 chars] | current.
17. https://code.claude.com/docs/en/agent-sdk/subagents | Subagents in the SDK [RAW] | current.
18. https://code.claude.com/docs/en/workflows | Orchestrate subagents at scale with dynamic workflows [RAW] | NEW in 2026; bundled `/deep-research`.
19. https://code.claude.com/docs/en/agent-teams | Orchestrate teams of Claude Code sessions [RAW] | experimental.
20. https://code.claude.com/docs/en/best-practices | Best practices for Claude Code [RAW, grepped] | current; contains a "What you can stop doing" table that retires older advice.
21. https://code.claude.com/docs/en/skills, /permissions, /memory, /hooks-guide, /permission-modes, /plugins/manifest-reference, /plugin-marketplaces (redirects to plugins/create-marketplace content) | config references (section 9).
22. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5 | Prompting Claude Opus 5 [RAW]
23. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices | Prompting best practices [RAW, grepped] | lists current models: Fable 5.1, Mythos 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5 etc.
24. https://github.com/anthropics/claude-cookbooks (dirs `patterns/agents/`, `claude_agent_sdk/`, `managed_agents/`, `evals/agentic_search/`, `skills/`) [VIA-SUMMARY of directory listings]. `claude_agent_sdk/research_agent/agent.py` read RAW.

---

## 2. Findings by question

### Q1. Research process: query strategy, breadth vs depth, source quality, stopping, effort budgets

**1.1 Broad-then-narrow and short queries.** [OPINION from published prompt; the blog calls it a principle] Blog principle: "Start with broad queries, then narrow down" (multi-agent post, [VIA-SUMMARY]). The subagent prompt makes this operational [RAW, research_subagent.md]: "Avoid overly specific searches that might have poor hit rates: Use moderately broad queries rather than hyper-specific ones. Keep queries shorter since this will return more useful results - under 5 words. If specific searches yield few results, broaden slightly. Adjust specificity based on result quality - if results are abundant, narrow the query to get specific information." The post lists "Overly long, specific search queries that returned few results" as an observed failure [VIA-SUMMARY].

**1.2 Classify the query: depth-first vs breadth-first vs straightforward.** [OPINION; published prompt, RAW research_lead_agent.md]
- Depth-first: "multiple perspectives on the same issue ... 'going deep' by analyzing a single topic from many angles." Example given: "What really caused the 2008 financial crisis?"
- Breadth-first: "broken into distinct, independent sub-questions ... 'going wide'". Example: "Compare the economic systems of three Nordic countries".
- Straightforward: "can be effectively answered by a single focused investigation". Example: "What is the current population of Tokyo?"
- The lead is told to "Explore several different methods of answering the question (at least 3) and then choose the best method you find" and to "Explicitly state your reasoning on what type of query this question is."

**1.3 Effort budgets (numbers).**
- Blog effort-scaling rules [VIA-SUMMARY]: simple fact-finding "1 agent, 3-10 tool calls"; direct comparisons "2-4 subagents with 10-15 calls each"; complex research "more than 10 subagents" with divided responsibilities. [OPINION embedded in prompts; the post says it embedded these because early agents over-invested.]
- Published lead prompt [RAW] `<subagent_count_guidelines>`: simple = 1 subagent; standard = 2-3; medium = 3-5; high = "5-10 subagents (maximum 20)"; "default to using 3 subagents for most queries"; "Never create more than 20 subagents unless strictly necessary ... Prefer fewer, more capable subagents over many overly narrow ones. More subagents = more overhead."
- Published subagent prompt [RAW]: "determine a 'research budget' - roughly how many tool calls ... simpler tasks like 'when is the tax deadline this year' should result in under 5 tool calls, medium tasks should result in 5 tool calls, hard tasks result in about 10 tool calls, and very difficult or multi-part tasks should result in up to 15 tool calls. Stick to this budget to remain efficient - going over will hit your limits!" Hard cap: "stay under a limit of 20 tool calls and under about 100 sources ... whenever you get to around 15 tool calls or 100 sources, make sure to stop gathering sources". Also "Execute a MINIMUM of five distinct tool calls, up to ten for complex queries. Avoid using more than ten tool calls." (internal inconsistency in the prompt itself: 5-call minimum vs "under 5 tool calls" for simple tasks and 15/20 caps; record both).
- Claude Code workflows doc [RAW] size guidelines: `small` < 5 agents, `medium` < 10, `large` < 50; "Large workflow" warning when "more than 25 agents, or its projected token total passes 1.5 million"; runtime limits "Up to 16 concurrent agents by default", "1,000 agents total per run", "Up to 4,096 items in a single parallel() or pipeline() call".
- Claude Code SDK defaults [RAW agent-sdk/subagents]: depth default 3 layers; concurrency default 20 subagents; cap spend with `max_budget_usd` / `maxBudgetUsd`.
- Agent teams doc [RAW]: "Start with 3-5 teammates for most workflows"; "Having 5-6 tasks per teammate keeps everyone productive"; "Three focused teammates often outperform five scattered ones." [OPINION]

**1.4 Stopping rules.**
- Subagent prompt [RAW]: "Avoid continuing to use tools when you see diminishing returns - when you are no longer finding new relevant information and results are not getting better, STOP using tools and instead compose your final report." and "As soon as you have the necessary information, complete the task rather than wasting time".
- Lead prompt [RAW]: "if you are running out of time or a research process has already taken a very long time, avoid deploying further subagents and instead just start composing the output report immediately."
- Documented failure being prevented [VIA-SUMMARY]: "Endless web searching for nonexistent sources."
- Dynamic-workflow doc [RAW] shows a "stop when new rounds find nothing new" pattern: "stop once two rounds in a row find nothing new" (example prompt).

**1.5 Source quality heuristics.**
- [EVIDENCE, VIA-SUMMARY] Human evaluation of the research system "caught that early agents preferred SEO-optimized content farms over authoritative sources like academic PDFs and personal blogs." (Fix was prompt heuristics for source quality; no number given.)
- Lead prompt [RAW]: tell each subagent "what constitutes reliable information or high-quality sources for this task, and list any unreliable sources to avoid"; example brief says "Prioritize original sources over news aggregators."
- Subagent prompt [RAW] `<think_about_source_quality>`: flag speculative pages: "mentioning predictions, using verbs like 'could' or 'may', narrative driven speculation with future tense, quoted superlatives, financial projections" and "make sure to note this explicitly in the final report, rather than accepting these events as having happened."
- Conflict handling [RAW]: "prioritize based on recency, consistency with other facts, the quality of the sources used ... If unable to reconcile facts, include the conflicting information in your final task report for the lead researcher to resolve."
- Fetch full pages: "use web_fetch to retrieve full results rather than just using search snippets" [RAW].
- General prompting guide [RAW] research block (OPINION): "Provide clear success criteria", "Encourage source verification", and the sample: "Search for this information in a structured way. As you gather data, develop several competing hypotheses. Track your confidence levels in your progress notes to improve calibration. Regularly self-critique your approach and plan. Update a hypothesis tree or research notes file to persist information and provide transparency."
- Eval rubric for source quality: see Q6.

**1.6 Lead does not research; it synthesises.** Lead prompt [RAW]: "your primary role is to coordinate, guide, and synthesize - NOT to conduct primary research yourself" and "All substantial information gathering should be delegated to subagents." But: for simple queries "treat the subagent as an equal collaborator ... try to ensure the subagent handles about half of the work". Contrast Opus 5 guidance in section 8.

### Q2. Delegation briefs

**2.1 Required contents (headline claim).** [OPINION, blog] "Each subagent needs an objective, an output format, guidance on the tools and sources to use, and clear task boundaries." [VIA-SUMMARY, multi-agent post]

**2.2 The expanded checklist in the published lead prompt** [RAW, research_lead_agent.md]: "All instructions for subagents should include the following as appropriate:
- Specific research objectives, ideally just 1 core objective per subagent.
- Expected output format - e.g. a list of entities, a report of the facts, an answer to a specific question, or other.
- Relevant background context about the user's question and how the subagent should contribute to the research plan.
- Key questions to answer as part of the research.
- Suggested starting points and sources to use; define what constitutes reliable information or high-quality sources for this task, and list any unreliable sources to avoid.
- Specific tools that the subagent should use ...
- If needed, precise scope boundaries to prevent research drift."
- Completeness test: "Make sure that IF all the subagents followed their instructions very well, the results in aggregate would allow you to give an EXCELLENT answer to the user's question".
- Non-overlap rule: "Avoid overlap between subagents - every subagent should have distinct, clearly separate tasks, to avoid replicating work unnecessarily and wasting resources."
- Worked example of a good brief (verbatim start): "Research the semiconductor supply chain crisis and its current status as of 2025. Use the web_search and web_fetch tools to gather facts from the internet. Begin by examining recent quarterly reports from major chip manufacturers like TSMC, Samsung, and Intel ... Prioritize original sources over news aggregators. Focus on identifying current bottlenecks ... When research is done, compile your findings into a dense report of the facts ... with specific timelines and quantitative data where available."

**2.3 Documented failure from vague briefs.** [EVIDENCE, anecdotal production observation; no rate given; VIA-SUMMARY] Early lead instructions were vague; one subagent explored the 2021 chip crisis while two others duplicated work on 2025 supply chains. Also from the search-result summary of the same post: vague instructions led subagents to "duplicate searches or misread tasks" (search-engine summary, not re-read).

**2.4 What a subagent actually receives.** [RAW, Agent SDK subagents page] "The only content you pass from parent to subagent is the Agent tool's prompt string, so include any file paths, error messages, or decisions the subagent needs directly in that prompt." The subagent does not get the parent's conversation history, tool results, or the parent's system prompt; it does get its own system prompt plus project CLAUDE.md. [RAW, sub-agents via summary] "It doesn't see your conversation history, the skills you've already invoked, or the files Claude has already read."
- Agent teams [RAW]: "A teammate also receives the spawn prompt from the lead. The lead's conversation history does not carry over." Example spawn prompt includes scope, focus areas, relevant facts ("The app uses JWT tokens stored in httpOnly cookies") and output format ("Report any issues with severity ratings").

**2.5 Subagent description as a routing brief.** [RAW/VIA] "Claude uses each subagent's description to decide when to delegate"; include "use proactively" to encourage delegation; combined subagent descriptions over 15,000 tokens trigger a startup warning.

**2.6 Give the delegation-rate instruction.** [OPINION, RAW Opus 5 guide] See Q3 and section 8: Opus 5 "delegates to subagents more readily"; supply an explicit "when to delegate" paragraph.

**2.7 Verification briefs must demand thoroughness.** [OPINION, VIA-SUMMARY claude.com blog] "Without explicit requirements for comprehensive validation, verification agents take shortcuts" and "A verifier told only to check whether output is good, with no further criteria, will rubber-stamp the generator's output" (coordination-patterns post).

### Q3. Decomposition, parallel vs sequential

- **Parallel speedup.** [EVIDENCE, VIA-SUMMARY] Post says the lead "spawns 3-5 subagents in parallel; subagents use 3+ tools in parallel" and that this "cut research time by up to 90% for complex queries." (Measured on their internal system; no n given in the summary.)
- **Dependency ordering.** [OPINION, RAW lead prompt] "when other tasks will depend on results from one specific task, always create a subagent to address that blocking task first." Worked example: first one subagent lists all EU countries and relevant metrics, then "use the batch tool to run 4 subagents" by region. Depth-first: "Deploy subagents in sequence to explore different methodologies"; breadth-first: "Begin with subagents that will establish key facts or framework information, then deploy subsequent subagents to explore more specific or dependent subtopics."
- **Parallel tool calls.** Lead prompt [RAW]: "You MUST use parallel tool calls for creating multiple subagents (typically running 3 subagents at the same time) at the start of the research, unless it is a straightforward query."
- **While waiting.** "While waiting for a subagent to complete, use your time efficiently by analyzing previous results, updating your research plan" [RAW]. Note the blog admits the lead was synchronous (waits for each batch), a bottleneck; async was future work [VIA-SUMMARY].
- **When parallel is the right call (Claude Code docs).** Sub-agents doc [VIA-SUMMARY]: "For independent investigations, spawn multiple subagents ... This works best when the research paths don't depend on each other." Caveat quote: "Running many subagents that each return detailed results can consume significant context, and each subagent spends tokens of its own". Chaining for dependent steps: "ask Claude to use subagents in sequence. Each subagent completes its task and returns results to Claude, which then passes relevant context to the next subagent." Best-practices page [RAW]: subagents "pay off" for (1) independent pieces in parallel, (2) keeping long output out of main context, (3) a reviewer that hasn't seen the work, (4) fewer tools. Cost: "a fresh subagent first has to gather context your conversation already had, so it can end up slower than doing the task where you are."
- **Only three valid reasons for multi-agent.** [OPINION, VIA-SUMMARY claude.com blog] "when context pollution degrades performance", "when tasks can run in parallel", "when specialization improves tool selection or task focus". "Outside these situations, the coordination costs typically exceed the benefits." "Start with the simplest approach that works, and add complexity only when evidence supports it." Parallel multi-agent "often take longer overall" so the benefit is "thoroughness, not speed" (this contradicts the 90% time cut for the research system; the conditions differ: the 90% is parallel subagents vs the same system run serially, the "longer overall" is multi-agent vs single agent).
- **Do not split by problem type/role.** [OPINION, VIA-SUMMARY] Role-split subagents "spent more tokens on coordination than on actual work"; splitting creates a "telephone game".
- **Pattern choice.** [OPINION, VIA-SUMMARY, Apr 10, 2026 post] "For most use cases, we recommend starting with orchestrator-subagent" ("Use this pattern when task decomposition is clear and subtasks have minimal interdependence"). Alternatives: generator-verifier; agent teams (long-running independent workers); message bus (event-driven); shared state ("Reactive loops ... need first-class termination conditions").
- **Building Effective Agents [OLDER, Dec 2024, VIA-SUMMARY].** Orchestrator-workers: "a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results." Sectioning: "Breaking a task into independent subtasks run in parallel." Voting: "Running the same task multiple times to get diverse outputs." Evaluator-optimizer: "one LLM call generates a response while another provides evaluation and feedback in a loop." Guidance: "finding the simplest solution possible, and only increasing complexity when needed."
- **Dynamic workflows (2026).** [RAW] "A dynamic workflow is a JavaScript script that orchestrates many subagents at once ... Reach for a workflow when a task needs more agents than one conversation can coordinate". Moves the plan into code: "A workflow script holds the loop, the branching, and the intermediate results itself, so Claude's context holds only the final answer." Gives named patterns: independent agents "adversarially review each other's findings before they're reported"; draft a plan from several angles; stop when rounds find nothing new. Table: subagents "A few delegated tasks per turn" vs workflows "Dozens to hundreds of agents per run".
- **Agent teams, competing hypotheses.** [OPINION, RAW agent-teams] "Sequential investigation suffers from anchoring ... With multiple independent investigators actively trying to disprove each other, the theory that survives is much more likely to be the actual root cause." Use teams for "Research and review"; avoid for "sequential tasks, same-file edits, or work with many dependencies".
- **Parallelism with no orchestrator (counter-example).** [EVIDENCE, VIA-SUMMARY, C compiler post Feb 5, 2026] 16 agents, "nearly 2,000 Claude Code sessions" over "two weeks", cost "just under $20,000", "2 billion input tokens" and "140 million output tokens"; no orchestration agent, git-based task locks (`current_tasks/` text files). Failure: on the Linux kernel (one giant task) "every agent hit the same bug and overwrote the others' fixes. Sixteen agents did not help." Fix: use GCC as an oracle for a random subset of files so agents work on different failures in parallel.

### Q4. Context: what is passed down, what comes back, compression, files and memory

- **Return a condensed summary.** [OPINION, VIA-SUMMARY, context-engineering post] A subagent "returns only a condensed, distilled summary of its work", "often 1,000-2,000 tokens", while exploration may use "tens of thousands of tokens or more." Agent SDK doc [RAW]: "intermediate tool calls and results stay inside the subagent; only its final message returns to the parent."
- **Return by reference, not by relay.** [OPINION, VIA-SUMMARY, multi-agent post] "Subagents can write outputs to an external filesystem and pass lightweight references back, reducing information loss ('game of telephone') and token overhead."
- **Lead saves its plan.** [EVIDENCE of a design constraint, VIA-SUMMARY] The lead stores the plan in Memory "because context beyond 200,000 tokens gets truncated." (Window size is a 2025 number; Claude 5 era docs say "Most current models have a 1M-token window", best-practices [RAW].)
- **Long conversations.** [VIA-SUMMARY] Agents summarise completed phases, store essentials externally, and can spawn fresh subagents with clean contexts via careful handoffs.
- **Compaction guidance.** [OPINION, VIA-SUMMARY] "Start by maximizing recall to ensure your compaction prompt captures every relevant piece of information from the trace"; "One of the safest lightest touch forms of compaction is tool result clearing". Structured note-taking: "the agent regularly writes notes persisted to memory outside of the context window."
- **Just-in-time retrieval.** [OPINION, VIA-SUMMARY] Agents "maintain lightweight identifiers (file paths, stored queries, web links, etc.)" and load data at runtime. Context rot: "the model's ability to accurately recall information from that context decreases."
- **Fresh context vs compaction.** [OPINION, RAW prompting guide] "consider starting with a brand new context window rather than using compaction. Claude's latest models are extremely effective at discovering state from the local filesystem. ... Be prescriptive about how it should start: 'Call pwd ...', 'Review progress.txt, tests.json, and the git logs.'" State practice: JSON for structured state, "unstructured text for progress notes", git for checkpoints. Harness post [VIA-SUMMARY]: Sonnet 4.5 had "context anxiety" so resets were needed; Opus 4.5 largely removed it so resets were dropped and compaction used; Managed Agents post: "The resets had become dead weight."
- **Handoff artifacts.** [VIA-SUMMARY] long-running harness: `init.sh`, `claude-progress.txt`, a JSON feature list where only `passes` may change; quote "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." (also quoted in RAW prompting guide). C compiler: "Assume each agent starts in a fresh container with no context. Maintain extensive READMEs and progress files." Print few lines, log detail to a file, put "ERROR" and the reason on one line.
- **Durable event log.** [OPINION, VIA-SUMMARY, Apr 8, 2026] Compaction, memory tools and trimming are "irreversible keep-or-discard choices"; keep the full session as an append-only log outside the window and let the harness decide what to fetch.
- **Claude Code specifics.** [RAW] CLAUDE.md loaded each session; "target under 200 lines per CLAUDE.md file"; auto memory loads "first 200 lines or 25KB". Subagents can have persistent `memory:` (`user`, `project`, `local`). `maxTurns` returns output "marked as partial" which can be resumed. A hook can re-inject context after compaction: SessionStart hook with `"matcher": "compact"`.
- **Tool output sizing.** [EVIDENCE, VIA-SUMMARY, writing-tools post] "For Claude Code, we restrict tool responses to 25,000 tokens by default." `response_format` detailed example 206 tokens vs concise 72 tokens (Slack example "~1/3 of the tokens").

### Q5. Failure modes and prevention

| Failure | Source | Prevention documented |
|---|---|---|
| Spawning too many subagents for simple queries ("spawning 50 subagents for simple queries") | multi-agent post [VIA-SUMMARY] | Effort-scaling rules in lead prompt; `<subagent_count_guidelines>` with max 20 [RAW] |
| Duplicate work from vague tasks (2021 vs 2025 chip crisis example) | multi-agent post [VIA-SUMMARY] | Brief fields in 2.2; non-overlap rule |
| Endless searching for nonexistent sources | same | Tool-call budget and diminishing-returns stop rule |
| SEO content farms preferred over primary sources | same | Source-quality heuristics in prompt |
| Over-long queries with few hits | same | under-5-word queries, broaden when sparse |
| Subagents distracting each other with updates | same | Subagents report only to lead at completion |
| Stateful compounding errors; cannot restart | same | Resume from checkpoints; "rainbow deployments" |
| Lead synchronous bottleneck | same | Listed as future work (async) |
| Context anxiety / early wrap-up (Sonnet 4.5) | harness posts | Context resets, later removed for Opus 4.5 |
| Declaring done too early; marking features done w/o end-to-end test | effective-harnesses [VIA-SUMMARY] | JSON feature list with `passes`; test "as a human user would" via browser automation |
| Self-evaluation skews positive; QA agent "talked itself into approving" issues | harness-design [VIA-SUMMARY] | Separate skeptical evaluator; few-shot calibration; read evaluator logs and revise |
| Verifier rubber-stamping | claude.com blog posts [VIA-SUMMARY] | Explicit criteria; "explicit requirements for comprehensive validation" |
| Orchestrator becomes information bottleneck | coordination-patterns [VIA-SUMMARY] | Evolve to agent teams / shared state when needed |
| Agents overwriting same file/fix | C compiler; agent-teams [RAW] | "Break the work so each teammate owns a different set of files"; oracle partitioning |
| Test output flooding context; "time blindness" | C compiler [VIA-SUMMARY] | Few-line output, `--fast` 1%/10% sampling |
| Verifier solves the wrong problem | C compiler [VIA-SUMMARY] | "the verifier must be nearly perfect" |
| Eval/benchmark contamination in search agents | eval-awareness [VIA-SUMMARY] | Block any search results containing variations of the benchmark name; treat eval integrity "as an ongoing adversarial problem" |
| Subagent output carrying injected instructions | Agent SDK page [RAW] | From v2.1.210 Claude Code "scans the final message for instruction-shaped patterns"; control tags neutralised in place |
| Over-delegation by newer models | Opus 5 guide [RAW] | Delegation paragraph + deterministic caps (section 9) |
| Over-verification by newer models | Opus 5 guide [RAW] | Remove "use a subagent to verify" scaffolding |
| Runaway agent trees / cost | SDK subagents [RAW] | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, `max_budget_usd` |

Numbers on cost of failure/benefit:
- [EVIDENCE, VIA-SUMMARY, multi-agent post] "4x more tokens than chat interactions", multi-agent "about 15x more than chats"; "three factors explained 95% of the performance variance" in the BrowseComp analysis, with "Token usage alone explained 80% of the variance" (tool-call count and model choice the others). Interpretation by the authors (implied): multi-agent works largely because it spends more tokens in parallel.
- [EVIDENCE, VIA-SUMMARY, claude.com blog] "multi-agent implementations typically use 3-10x more tokens than single-agent approaches for equivalent tasks". Conflicts with 15x above; different baselines (chat vs single agent). Record both.
- [EVIDENCE, VIA-SUMMARY, eval-awareness] unintended-solution rate 0.87% multi-agent vs 0.24% single-agent (3.7x); authors hypothesise more tokens and parallel searchers raise the chance that one finds leaked material. Two cases used 40.5 million and 13.4 million tokens.
- [EVIDENCE, VIA-SUMMARY, harness-design] retro game maker (Opus 4.5): solo 20 min / $9; full harness 6 hr / $200 (over 20x more expensive, "clearly better result"). Evaluator "justified only for those tasks" beyond what the model does reliably solo.

### Q6. Verification and combining results

- **Eval method used for the research system.** [EVIDENCE, VIA-SUMMARY] Started with "about 20 queries representing real usage patterns" (small-sample eval; the post argues this is enough early when effects are large). LLM-as-judge rubric: factual accuracy, citation accuracy, completeness, source quality, tool efficiency; "A single call scoring 0.0-1.0 plus pass/fail matched human judgment best." Human evaluation caught the SEO-farm bias. For stateful agents: "End-state evaluation is recommended".
- **Production tuning gain.** [EVIDENCE, VIA-SUMMARY] A tool-testing agent rewrote tool descriptions, giving "40% decrease in task completion time" for later agents.
- **Headline result.** [EVIDENCE, VIA-SUMMARY, OLDER models] Multi-agent (Opus 4 lead + Sonnet 4 subagents) "outperformed single-agent Claude Opus 4 by 90.2%" on their internal research eval.
- **Research-agent eval dimensions.** [OPINION/method, VIA-SUMMARY, Jan 9, 2026] Groundedness (claims supported by retrieved sources), coverage (key facts a good answer must include), source quality (authoritative, "not just the first retrieved"). "20-50 simple tasks drawn from real failures" is enough to start. "grade what the agent produced, not the path it took." LLM graders calibrated against experts; give judges an "Unknown" option; isolated judge per dimension; "A 0% pass rate across many trials most often signals a broken task rather than an incapable agent." pass@k vs pass^k example: 75% per trial gives pass^3 about 42%.
- **LLM-as-judge caveat.** [OPINION, VIA-SUMMARY, SDK blog Sep 29, 2025] "This is generally not a very robust method" but may help when gains are worth the latency; preferred: "clearly defined rules for an output", then visual feedback. Tension with the research post's finding that a single LLM judge call matched humans best; conditions: the research post's rubric was tuned against human eval on 20 queries.
- **Citations as a separate pass.** [RAW, citations_agent.md] A dedicated agent takes the finished report in `<synthesized_text>` and the sources, and must "Do NOT modify the <synthesized_text> in any way ... only add citations"; "ONLY add citations where the source documents directly support claims"; "Avoid citing unnecessarily"; cite "complete thoughts" at sentence end. Output in `<exact_text_with_citation>`.
- **Combine by ensemble + critique.** [OPINION, RAW lead prompt] "Compare the subagent's results and synthesize them using an ensemble approach and by applying critical reasoning." For hard steps, "deploy independent subagents for additional perspectives or approaches." Conflicts get passed up unresolved: "include the conflicting information in your final task report for the lead researcher to resolve."
- **Cross-check pipelines in Claude Code.** [RAW workflows doc] Bundled `/deep-research`: "fans out web searches on a question across several angles, fetches and cross-checks the sources it finds, votes on each claim, and returns a cited report with claims that didn't survive cross-checking filtered out." Claims verifiers could not check "list that claim as unverified instead of counting it as refuted." Requires the WebSearch tool.
- **Fresh-eyes review.** [OPINION, RAW best-practices] "A fresh reviewer does help, because it hasn't seen your reasoning, which is a different thing from delegating." `/code-review` runs "in a fresh subagent that never saw your conversation."
- **Verification subagent pattern.** [OPINION, VIA-SUMMARY] "Verification subagents succeed because they sidestep the telephone game problem"; strongest failure: "marking outputs as passing without thorough testing".
- **Evaluator calibration.** [OPINION/EVIDENCE, VIA-SUMMARY, harness-design] Calibrate the evaluator with few-shot examples and hard thresholds per criterion; "a separate, skeptical evaluator was far more tractable to tune than a self-critical generator."
- **Writer-verifier on Opus 5.** [RAW Opus 5 guide] "Claude Opus 5 coordinates teams of subagents well, with effective writer-verifier patterns and few cases of agents overwriting each other's work." But "If your prompt contains explicit verification instructions ... remove them: instructions like these cause over-verification". Reconciliation in section 8.
- **Output length for reports.** [RAW Opus 5 guide] Add: "Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate."
- **Prompt-writing principles worth reusing in briefs.** [RAW prompting best practices] "Think of Claude as a brilliant but new employee who lacks context ... Key test: Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too." Explain the reason behind constraints ("Your response will be read aloud by a text-to-speech engine, so never use ellipses ..."); "Claude can generalize from the explanation." Put long documents at the top; "Queries at the end can improve response quality by up to 30 percent in tests" ([EVIDENCE] on their tests, no n given). Wrap multi-document inputs in `<documents><document index="1"><source>...</source><document_content>...`.

---

## 3. The published research prompts (cookbook) in brief [RAW]

Path: `patterns/agents/prompts/` in https://github.com/anthropics/claude-cookbooks. (Downloaded and grepped during the run; 23,102 / 9,109 / 2,870 bytes; not committed.)

Structure of `research_lead_agent.md`: `<research_process>` (assessment and breakdown, query-type determination, detailed plan, plan execution, synthesis) -> `<subagent_count_guidelines>` -> `<delegation_instructions>` -> `<answer_formatting>` -> `<use_available_internal_tools>` -> `<use_parallel_tool_calls>` (+ writing guidelines).
`research_subagent.md`: `<research_process>` (plan with budget; OODA-style loop of tool calls with thinking between) -> `<research_guidelines>` -> `<think_about_source_quality>` -> `<use_parallel_tool_calls>` ("invoke 2 relevant tools simultaneously") -> `<maximum_tool_call_limit>` -> final instructions ending with `complete_task`.
Cookbook research agent in the Agent SDK recipes (`claude_agent_sdk/research_agent/agent.py`, `00_The_one_liner_research_agent.ipynb`) [RAW agent.py]: a single agent, `allowed_tools=["WebSearch", "Read"]`, system prompt only about citations ("Always include source URLs as citations ... Group sources in a 'Sources:' section"), `DEFAULT_MODEL = "claude-opus-5-5"`, no subagents defined. So the current cookbook "research agent" is the minimal pattern; the multi-agent prompts are in `patterns/agents/prompts/`. Other relevant recipes (listing only, not opened): `patterns/agents/{orchestrator_workers,evaluator_optimizer,basic_workflows,async_multi_agent_orchestration,latency_multi_agent}.ipynb`, `claude_agent_sdk/08_Dynamic_workflows.ipynb`, `claude_agent_sdk/01_The_chief_of_staff_agent.ipynb` (hooks, plan mode, subagent orchestration), `evals/agentic_search/`, `multimodal/using_sub_agents.ipynb` (Haiku as subagent under Opus; likely older).

---

## 4. Current config syntax reference (verified against the docs on 2026-10-31)

### 4.1 Subagent files
Source: https://code.claude.com/docs/en/sub-agents [VIA-SUMMARY, field table quoted] and https://code.claude.com/docs/en/agent-sdk/subagents [RAW].
- Location and priority (1 highest): managed settings; `--agents` CLI flag; `.claude/agents/` (project); `~/.claude/agents/` (user); plugin `agents/`. "When multiple subagents share the same name, Claude Code uses the one from the higher-priority location."
- Markdown with YAML frontmatter; body is the system prompt. "Only `name` and `description` are required. Multi-word fields use camelCase and must match exactly, because unrecognized fields are ignored without an error."
- Fields (quoted from the docs): `name` ("Unique identifier of at most 256 characters ... Names can't contain `:`"), `description` ("When Claude should delegate to this subagent"), `tools` ("comma-separated string such as `Read, Grep, Bash` or a YAML list. Inherits every tool available to subagents if omitted."), `disallowedTools`, `model` ("`sonnet`, `opus`, `haiku`, `fable`, a full model ID such as `claude-opus-5-5`, or `inherit`"), `permissionMode` (`default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, or `manual`; "Ignored for plugin subagents"), `skills` (full skill content injected at startup; SDK doc: "At most the first 32 distinct names"), `mcpServers`, `hooks` (both ignored for plugin subagents), `memory` (`user`, `project`, `local`), `maxTurns` (output marked partial, resumable), `background` (bool), `isolation` (`worktree`), `color` (red, blue, green, yellow, purple, orange, pink, cyan), plus `initialPrompt`, `effort`, `omitClaudeMd`, `autoCompactWindow`, `experimental` (listed in the table, details not captured).
- Minimal example from the docs:
```
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---
You are a code reviewer. ...
```
- Built-ins: **Explore** ("A fast, read-only agent optimized for searching and analyzing codebases"; thoroughness `quick` / `medium` / `very thorough`), **Plan** (research agent used in plan mode), **general-purpose**. Explore and Plan are one-shot and cannot be resumed.
- **Tool name: "In version 2.1.63, the Task tool was renamed to Agent. Existing `Task(...)` references in settings and agent definitions still work as aliases."** SDK: tool appears as `"Agent"` in `tool_use` blocks "but as `"Task"` in the `system:init` tools list"; match both.
- Restrict spawnable types (only for an agent run as main thread with `claude --agent`): `tools: Agent(worker, researcher), Read, Bash`. Bare `Agent` allows any; omitting `Agent` means no spawning. In a subagent definition the parenthesised list is ignored.
- Nesting: "By default, a subagent can spawn subagents of its own, up to three layers below the main conversation" (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, "Set `1` to turn nesting off"). This corrects the older belief that subagents cannot spawn subagents.
- Concurrency default 20 (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`); spend cap `max_budget_usd`.
- Foreground vs background: subagents Claude spawns from the main conversation "already start in the background" by default; `background: true` pins it. Resume with `SendMessage` using agent ID or name; "Resumed subagents retain their full conversation history".
- SDK programmatic form (`AgentDefinition`): required `description`, `prompt`; optional `tools`, `disallowedTools`, `model`, `skills`, `memory`, `mcpServers`, `maxTurns`, `background`, `effort` (`low|medium|high|xhigh|max|number`), `permissionMode`, etc. Include `"Agent"` in `allowedTools`.
- `Agent(fork)`: a fork copies the conversation instead of starting fresh; block with deny rule `Agent(fork)`.

### 4.2 Skills (and commands)
Source: https://code.claude.com/docs/en/skills [VIA-SUMMARY, first 100,000 of 118,821 chars].
- Layout: `my-skill/SKILL.md` (required), optional `reference.md`, `examples.md`, `scripts/helper.py`. Locations: `~/.claude/skills/<name>/SKILL.md`, `.claude/skills/<name>/SKILL.md`, nested `<subdir>/.claude/skills/...`, plugin `<plugin>/skills/<name>/SKILL.md`, enterprise via managed settings, `--add-dir`.
- "All fields are optional. Only `description` is recommended." Fields: `name` (defaults to directory name), `description`, `when_to_use`, `argument-hint`, `arguments` (named positional), `disable-model-invocation`, `user-invocable`, `allowed-tools` (space/comma string or YAML list), `disallowed-tools`, `model`, `effort` (`low|medium|high|xhigh|max`), `context: fork` (run in a forked subagent context), `agent` (which subagent type with `context: fork`), `background`, `hooks`, `paths` (glob activation), `shell` (`bash` default or `powershell`), `metadata`, `license`, `compatibility`. Booleans accept yes/no/on/off/1/0.
- Size: "combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing"; "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files."
- **Commands merged into skills: "Custom commands have been merged into skills. A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Your existing `.claude/commands/` files keep working."** In plugins: `commands/` is "Flat Markdown command files. Prefer `skills/` for new plugins" [RAW plugins manifest reference].
- Arguments: `$ARGUMENTS` (all), `$ARGUMENTS[N]` (0-based), `$N` shorthand (`$0`, `$1`), `$name` for declared `arguments`; "when no placeholder receives an argument, Claude Code appends them as `ARGUMENTS: <value>`." Example: `Migrate the $0 component from $1 to $2.`
- Dynamic context injection: `` !`<command>` `` inline, or a fenced block opened with ```` ```! ````, runs before content is sent to Claude.
- Open standard: "Claude Code skills follow the Agent Skills open standard" (agentskills.io); progressive disclosure per the Oct 16, 2025 blog (name+description always in system prompt; SKILL.md body when relevant; linked files on demand).
- Bundled commands relevant to research: `/deep-research <question>` (workflow), `/workflows`, `/workflow-authoring` skill, `/code-review`, `/batch`, `/context`, `/usage`, `/effort`, `/goal`, `/loop`.

### 4.3 Plugins and marketplace
Source: https://code.claude.com/docs/en/plugins/manifest-reference [RAW], https://code.claude.com/docs/en/plugins/create-marketplace [RAW] (the old /plugin-marketplaces URL served this content).
- Manifest at `.claude-plugin/plugin.json`; **optional** ("Without it, Claude Code loads the components it finds in the standard layout"). `name` is the only required key; kebab-case; "Claude Code namespaces every component under it, so an agent `reviewer` in plugin `deploy-tools` appears as `deploy-tools:reviewer`." Skills run as `/plugin-name:skill`.
- Reserved names: names starting `claude-`, `anthropic-`, `anthropics-`, `cc-plugin-` error in `claude plugin validate`; so do `claude`, `anthropic`, `claude-code`, etc. (Do not name our repo plugin `claude-research-toolkit`; use e.g. `research-toolkit`.)
- Other fields: `displayName`, `version` ("Setting it keeps users on that version until you change it"), `description`, `author` (object with `name`), `homepage`, `repository`, `license`, `keywords`, `dependencies`, `userConfig`, `skills`, `commands`, `agents`, `hooks`, `mcpServers`, `lspServers`, `outputStyles`, `workflows`, `settings` (only `agent`, `subagentStatusLine` take effect).
- Path rules: every component path "must start with `./`" and stay inside the plugin root. Unrecognised top-level keys are stripped with a validate warning.
- Standard layout: `.claude-plugin/plugin.json`, `skills/<name>/SKILL.md`, `commands/*.md`, `agents/*.md`, `hooks/hooks.json`, `.mcp.json`, `.lsp.json`, `output-styles/`, `workflows/*.js`, `monitors/monitors.json`, `bin/`, `settings.json`. "A `CLAUDE.md` at the plugin root isn't loaded as context ... put them in a skill."
- Plugin `hooks/hooks.json` wraps the event map in a top-level `"hooks"` key (a file with only the event map "fails to load").
- Variables: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`.
- Validate: `claude plugin validate ./my-plugin` (`--strict` turns warnings to failures).
- Marketplace: `.claude-plugin/marketplace.json` requires `name`, `owner`, `plugins` array; each plugin entry needs `name` and `source` (relative path string like `"./plugins/my-first-plugin"`, or objects: `{"source":"github","repo":"org/repo"}`, `git-subdir`, `url`, `archive`, `npm`, `command`). Entry `name` must equal the plugin's manifest name. Add: `claude plugin marketplace add ./my-marketplace` (or `/plugin marketplace add`), install `claude plugin install my-first-plugin@my-marketplace`. Marketplace names such as `claude-plugins-official` are reserved.
- Plugin subagents ignore `permissionMode`, `hooks`, `mcpServers` frontmatter.

### 4.4 Permissions in settings.json (WebSearch / WebFetch / Agent)
Source: https://code.claude.com/docs/en/permissions [RAW, grepped].
- Shape: `{"permissions": {"allow": [...], "ask": [...], "deny": [...], "defaultMode": "plan"}}`.
- Precedence: "Rules are evaluated in order: deny, then ask, then allow. The first match in that order determines the outcome, and rule specificity doesn't change the order." A deny in any scope beats an allow in another.
- `WebFetch(domain:example.com)` matches that host only; `WebFetch(domain:*.example.com)` matches subdomains at any depth "but not `example.com` itself"; `WebFetch(domain:*)` all domains. Bare `WebFetch` is different from `WebFetch(domain:*)` (only the `domain:` form adds to the sandbox network allowlist).
- WebSearch: appears in the tool table ("Web search | WebSearch | Yes ... Permanently per repository"). I found **no specifier syntax** for WebSearch in the sections I read; use the bare name `"WebSearch"`. [UNVERIFIED for any parameterised form]
- Agent: "Use `Agent(AgentName)` rules" e.g. `Agent(Explore)`, `Agent(Plan)`, `Agent(my-custom-agent)`; disable with `{"permissions": {"deny": ["Agent(Explore)"]}}` or `--disallowedTools`. Parameter matching: `Agent(model:opus)`, `Agent(isolation:worktree)`, wildcard `*`, one parameter per rule; "A parameter the model omits is never matched". Workflow tool rules: `Workflow` or `Workflow(<name>)` [RAW workflows doc].
- Project `permissions.allow` rules in `.claude/settings.json` apply only "after you accept the workspace trust dialog".
- Permission-mode names: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. Plan mode: "research and propose changes without making them"; enter with Shift+Tab, `/plan`, or `claude --permission-mode plan`; default via `"permissions": {"defaultMode": "plan"}` in `.claude/settings.json` [VIA-SUMMARY permission-modes]. Docs do not say whether plan mode can spawn subagents (built-in Plan subagent exists "used during plan mode to gather context").
- Composed example for a research project (assembled by me from the documented pieces; not a quoted block):
```json
{
  "permissions": {
    "allow": ["WebSearch", "WebFetch(domain:*)", "Agent(research-worker)"],
    "deny": ["WebFetch(domain:localhost)"]
  }
}
```

### 4.5 Memory / CLAUDE.md
Source: https://code.claude.com/docs/en/memory [RAW, grepped].
- Locations: `./CLAUDE.md` or `./.claude/CLAUDE.md` (project), `./CLAUDE.local.md` (personal, gitignore it), `~/.claude/CLAUDE.md` (user), managed policy file. Files in ancestor directories load at launch, concatenated root-to-cwd; subdirectory CLAUDE.md files load on demand.
- Imports: `@path/to/import`; "Both relative and absolute paths are allowed. Relative paths resolve relative to the file containing the import ... maximum depth of four hops." Imports inside code spans/blocks are skipped (write `` `@README` `` to keep literal). "Imports help you organize a long file but don't reduce its context cost." External imports (outside the working directory) trigger an approval dialog.
- Size: "target under 200 lines per CLAUDE.md file".
- `.claude/rules/*.md` (recursive), path-scoped with frontmatter `paths:`; `claudeMdExcludes` setting; `AGENTS.md` can be read in place of CLAUDE.md. "Claude treats them as context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook".

### 4.6 Hooks relevant to a research workflow
Source: https://code.claude.com/docs/en/hooks-guide [RAW, grepped]; full schema is in /docs/en/hooks (not read).
- Config shape in settings.json: `{"hooks": {"<Event>": [{"matcher": "<regex or empty>", "hooks": [{"type": "command", "command": "..."}]}]}}`. Handler `type` values: `command`, `http`, `prompt` (single-turn LLM evaluation), `agent` (multi-turn verification with tool access, "experimental and may change").
- Events listed in guide include: `SessionStart` (matcher e.g. `compact`), `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `PostToolBatch`, `PermissionRequest`, `Notification`, `Stop`, `SubagentStart`, `SubagentStop` (matcher = agent type, e.g. `general-purpose`, `Explore`, `Plan`, or custom name), `PreCompact` / `PostCompact` (matcher `manual`/`auto`), `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `ConfigChange`, `FileChanged`, `CwdChanged`, `WorktreeCreate/Remove`, `SessionEnd`.
- Exit codes: "Exit 2: write a reason to stderr. Depending on the event, Claude receives it as feedback so it can adjust". Exit 0 on `PreToolUse` "doesn't approve" the call. For `SessionStart`, `UserPromptSubmit`, stdout is added to context.
- Prompt-hook semantics: for `Stop` and `SubagentStop`, `"ok": false` feeds the `reason` back so "Claude keeps working", unless the response sets `"impossible": true`. Useful for a "has the research met its checklist" gate.
- `if` field filters by permission-rule syntax, e.g. `"Bash(git *)"`.
- Re-inject context after compaction: SessionStart hook with `"matcher": "compact"`.
- Hooks do not override deny/ask rules: "PreToolUse hook decisions don't bypass permission rules"; but "A hook that exits with code 2 stops the tool call before permission rules are evaluated".
- Tip from best-practices [RAW]: enforce a verification check via a `Stop` hook; "A line like `Always typecheck before you finish` in this file works most of the time, not every time."

### 4.7 Other 2026 primitives to know
- **Dynamic workflows** [RAW]: saved to `.claude/workflows/` or `~/.claude/workflows/`; a `.js` file with `export const meta = { name, description }` and `agent()`, `pipeline()`, `parallel()`, `phase()`, `log()`, global `args`; `agent(prompt, { schema, label, stallMs })`. Trigger by `ultracode` keyword or "use a workflow". Disable: `"disableWorkflows": true`. Plugin location: `workflows/`. Limits above.
- **Agent teams** [RAW]: experimental; enable `{"env": {"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"}}`; `teammateMode` (`in-process`, `auto`, `tmux`, `iterm2`); team hooks `TeammateIdle`, `TaskCreated`, `TaskCompleted`; "No nested teams"; while enabled, "a subagent that Claude names ... launches as a teammate" (can surprise; set the variable to `0` to stop).
- **Headless**: `claude -p` for scripts; `/goal`, `/loop`, scheduled tasks and routines exist (pages not read).

---

## 5. Outdated / changed items (flagged)

1. **Task tool renamed to Agent** in Claude Code v2.1.63; `Task(...)` still works as an alias in settings and agent definitions; SDK init list still shows `"Task"`. Use `Agent`.
2. **Subagents can now spawn subagents** (default depth 3). Older docs/belief said no nesting. Agent teams still forbid nested teams.
3. **Custom slash commands merged into skills**; `.claude/commands/` still works, but new work should use `skills/<name>/SKILL.md`.
4. **Model names**: the multi-agent post's Opus 4 / Sonnet 4, the Claude 3.5 Sonnet SWE-bench reference, Opus 4.5/4.6 in 2026 harness posts are pre-Claude-5. Current model families per the prompting guide: Fable 5.1, Mythos 5.1, Opus 5.5, Sonnet 5.5, Haiku 5.5 (and Opus 5, Sonnet 5, Haiku 4.5, Opus 4.x still supported). Subagent `model` aliases now include `fable`. Do not quote the 90.2% as a statement about current models.
5. **Context window**: 2025 posts assume ~200k-token windows (the lead saves its plan because ">200,000 tokens gets truncated"). Claude Code docs now: "Most current models have a 1M-token window and compaction happens on its own, so running out is rare." Opus 5: "1M token context window as both the default and the maximum".
6. **Claude Code best-practices "What you can stop doing" table** [RAW] retires: "Use subagents to protect your context window" (still good for parallel work, noisy output, independent review, "but each of those costs extra tokens"); "Delegate to a subagent for a better answer" ("Handing the same task to a subagent doesn't make the answer any better. A fresh reviewer does help"); `think hard` / `be thorough` phrases (effort is the control); "keep going / don't be lazy" lines; ALL CAPS/IMPORTANT emphasis ("piling on emphasis mostly makes Claude over-apply the rule"); describing architecture in CLAUDE.md.
7. **Opus 5 prompting changes** [RAW]: explicit verification and "double-check" instructions now cause over-verification; "use a subagent to verify or double-check your own work" is discouraged; narrow "only report high-severity issues" instructions are followed literally (report everything, filter in a separate pass).
8. **Old April 2025 "Claude Code: Best practices for agentic coding" post** (listed in the engineering index, dated Apr 18, 2025) and the Mar 20, 2025 "think" tool post: **[OLDER], not opened**. Superseded by the current docs page code.claude.com/docs/en/best-practices.
9. **Bash-oriented long-running-harness advice (Nov 2025)**: context resets were a workaround for Sonnet 4.5 "context anxiety" and were dropped for Opus 4.5 (harness-design post, Managed Agents post).
10. `docs.claude.com` and `platform.claude.com/docs/en/agent-sdk/*` now redirect to `code.claude.com/docs/en/...`; update any links in our repo accordingly.

## 6. Disagreements between Anthropic sources (record both, with conditions)

| Topic | Position A | Position B | When each applies |
|---|---|---|---|
| Delegating at all | Research lead prompt: "always deploy at least 1 subagent, even for simple tasks"; all substantial gathering delegated | Opus 5 guide: "Do not delegate work you can finish yourself in a handful of tool calls ... keep spawn counts low"; best-practices: subagents give parallelism or fresh eyes "but not a smarter answer" | A = 2025 custom harness built to force source gathering via a tool boundary and measured on a multi-source research eval. B = 2026 models that delegate eagerly; use when cost matters or tasks small. |
| Verification subagents | claude.com blog: verification subagent useful, especially with weaker orchestrators | Opus 5 guide: remove "use a subagent to verify"; the model verifies unprompted | Use dedicated verifiers when you need independent context (reviewer that hasn't seen reasoning), or a weaker orchestrator; skip duplicative "double-check" prompts on Opus 5. |
| Multi-agent token cost | 15x chats (research post, vs chat) | 3-10x single-agent (claude.com blog) | Different baselines. Both [VIA-SUMMARY]. |
| Parallel = speed? | Research post: up to 90% time cut vs serial subagents | claude.com blog: multi-agent "often take longer overall"; benefit is "thoroughness, not speed" | A compares parallel vs serial subagents; B compares multi-agent vs one agent. |
| Search call minimums | Subagent prompt: MINIMUM five distinct tool calls | Same prompt: simple tasks "under 5 tool calls"; blog: simple fact-finding 3-10 | Internal inconsistency in the prompt; pick explicit budget by tier. |
| Orchestrator needed? | Research post: lead agent plans and synthesises | C compiler post: no orchestrator, agents self-select tasks and lock via git | Orchestrator for interdependent synthesis tasks; lock-based self-selection for large, partitionable, test-verified work. |
| Compaction vs fresh start | Context-engineering post: compaction tuned for recall | Prompting guide: "consider starting with a brand new context window rather than using compaction" when files hold state | Fresh start when state is on disk (progress file, git); compaction when continuity of reasoning matters. |
| LLM judge reliability | Research post: single LLM judge call matched human judgment best | SDK blog: LLM-as-judge "generally not a very robust method" | Judge was calibrated against human eval on ~20 queries; use judges after calibrating, prefer rules first. |

## 7. Practical implications for the toolkit (derived; my inference, not Anthropic quotes) [OPINION]

- Use the lead/subagent brief checklist from section 2.2 as the template header for every delegation: objective (1 per agent), output format, context, key questions, sources and what to avoid, tools, scope boundary, tool-call budget, stop rule.
- Put an effort-tier table in the lead prompt (simple 1 agent / 3-10 calls; comparison 2-4 agents / 10-15 calls each; complex up to ~10, hard cap 20) and ask for a stated query-type classification before spawning.
- Have subagents write findings to files and return a short summary plus the path.
- Use an independent citation/verification pass, with explicit criteria so the verifier cannot rubber-stamp.
- Add a delegation-damping paragraph (Opus 5 text) and set `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` / `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` in project `settings.json` `env` if cost control is wanted.
- For plugin naming avoid the reserved prefixes.

## 8. Gaps / not closed

- Exact quotes for every anthropic.com/engineering post are via a summariser; before quoting numbers in the final report, re-open: multi-agent post (15x, 4x, 95%, 80%, 90%, 40%, 50 subagents), C compiler post, harness-design post ($9 / $200 / $124.70), eval-awareness (0.87% / 0.24%), writing-tools (25,000 tokens).
- Publication dates for the two claude.com blog posts: coordination-patterns = April 10, 2026 (as printed); when-to-use post date not captured.
- Cookbook prompt files: commit dates and whether they match the June 2025 post unchanged could not be checked (GitHub API blocked for this session). The "View all files" listing of `patterns/agents/prompts/` was truncated, so more prompt files may exist.
- Not opened: hooks reference page (full event schemas), `/docs/en/agents` (compare subagents, agent view, teams, workflows), `/docs/en/costs` (agent team token costs), `/docs/en/context-window`, `/docs/en/headless`, `/docs/en/model-config` (effort levels, `ultracode` availability), sub-agents page tail (after char 100000: messaging by name after restart), skills page tail (bundled skills section), Opus 5 effort doc, the other 2025 engineering posts, the Apr 2025 Claude Code best-practices blog, "Claude Code Advanced Patterns" PDF, "Building Effective AI Agents" PDF (resources.anthropic.com), the `08_Dynamic_workflows.ipynb` notebook, `managed_agents/` cookbook.
- No WebSearch permission-rule specifier syntax was found; only bare `WebSearch` confirmed.
- Whether plan mode can spawn subagents is not stated on the permission-modes page (first 100,000 chars).
- No Anthropic-authored source was found that gives a numeric stopping criterion beyond tool-call/source caps (20 calls / ~100 sources) and "diminishing returns" language; no Anthropic number for how many sources are "enough".
- Anthropic conference talks (e.g. AI Engineer / Code with Claude) not searched; claude.com resource PDFs not read.
