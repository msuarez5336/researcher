# Notes C: non-Anthropic evidence on LLM research agents and orchestrator delegation

> Worker notes as returned on 2026-10-31, kept for provenance. The verified synthesis is in ../report.md; where these notes and the report differ, the report wins.

Compiled 2026-10-31.

## READ THIS FIRST: method limitation

- WebFetch could not reach any external host in this session. cognition.ai, arxiv.org, blog.langchain.com, huggingface.co, alphaxiv.org and trychroma.com all failed DNS ("outside allowed network domains"). I stopped after the 4th and 5th different host failed, as the tool error instructed.
- Every claim below therefore comes from WebSearch result summaries, which are model-written digests of the pages. I did NOT read any primary source in full. The "10-15 sources read in depth" stopping criterion was NOT met.
- Each claim is tagged with its original URL. If a number appeared only in a secondary write-up (blog, Medium, substack), it is marked [UNVERIFIED-2nd]. Where the search digest itself flagged conflicting numbers, I say so.
- Action for caller: allow arxiv.org, cognition.com (note: the live domain is cognition.com, not cognition.ai), blog.langchain.com / langchain.com, research.google, trychroma.com and martinfowler.com in the session network settings, then re-run the verification list in "Gaps".
- Evidence-strength key: A = peer-reviewed or arXiv with controlled measurement, but not opened by me; B = vendor or lab self-reported numbers; C = practitioner experience; D = only seen in secondary summaries.

## 1. Source table

| # | Source | URL | Authors/org | Date | Type | Strength |
|---|---|---|---|---|---|---|
| 1 | Don't Build Multi-Agents | https://cognition.com/blog/dont-build-multi-agents | Walden Yan, Cognition | Jun 2025 | Practitioner essay (dissent) | C (no numbers) |
| 2 | Multi-Agents: What's Actually Working | https://cognition.com/blog/multi-agents-working | Walden Yan, Cognition | 2026-04-22 | Practitioner follow-up (revision) | C |
| 3 | Towards a Science of Scaling Agent Systems | https://arxiv.org/pdf/2512.08296 ; blog https://research.google/blog/towards-a-science-of-scaling-agent-systems-when-and-why-agent-systems-work/ | Kim, Gu et al., Google Research and MIT | Dec 2025 | Controlled study, 180 configs | A |
| 4 | Why Do Multi-Agent LLM Systems Fail? (MAST) | https://arxiv.org/abs/2503.13657 | Cemri, Pan, Yang et al., UC Berkeley (NeurIPS 2025 per secondary source) | Mar 2025 | Failure taxonomy from traces | A |
| 5 | Single-agent vs multi-agent at equal thinking-token budget | arXiv 2604.02460 (found via https://beancount.io/bean-labs/research-logs/2026/05/31/single-agent-outperforms-multi-agent-equal-token-budget) | Tran and Kiela | Apr 2026 | Preprint, controlled comparison | A- (preprint, under review) |
| 6 | Related equal-cost papers: https://arxiv.org/pdf/2609.04217 ; https://arxiv.org/pdf/2601.17311 ; https://arxiv.org/html/2610.27488 | as listed | various | Jan-Oct 2026 | Preprints | D (titles and one-line digests only) |
| 7 | Cursor, Scaling long-running autonomous coding | cursor.com post, mirrored/summarized at https://www.zenml.io/llmops-database/scaling-multi-agent-autonomous-coding-systems | Cursor | 2026-01-14 | Production write-up | C/B, via secondary summaries (not opened) |
| 8 | LangChain open_deep_research | https://github.com/langchain-ai/open_deep_research ; https://www.langchain.com/blog/open-deep-research | LangChain | 2025 | Open implementation + self-reported benchmark | B |
| 9 | Chroma, Context Rot | https://www.trychroma.com/research/context-rot (repo https://github.com/chroma-core/context-rot) | Chroma | Jul 2025 | Technical report, 18 models | A-/B (details via secondary summaries) |
| 10 | Lost in the Middle [OLDER, 2023] | https://arxiv.org/abs/2307.03172 | Liu et al., Stanford (TACL 2024) | Jul 2023 | Peer-reviewed | A |
| 11 | BrowseComp | https://arxiv.org/abs/2504.12516 ; https://openai.com/index/browsecomp/ | Wei et al., OpenAI | Apr 2025 | Benchmark paper | A/B (self-reported) |
| 12 | WideSearch | https://arxiv.org/pdf/2508.07999 (ICLR 2026) | ByteDance-affiliated authors [UNVERIFIED affiliation] | Aug 2025 | Benchmark | A |
| 13 | DeepSearchQA | https://arxiv.org/html/2601.20975 | not captured | Jan 2026 | Benchmark | A (abstract-level only) |
| 14 | DeepResearch Bench | https://github.com/Ayanami0730/deep_research_bench | Ayanami0730 et al. | Jun 2025, repo updated 2026 | Benchmark | A/B |
| 15 | AgentFold | https://arxiv.org/abs/2510.24699 | Rui Ye et al. | Oct 2025 (ICLR 2026) | Method + eval | A- |
| 16 | ReWOO [OLDER, 2023] | https://arxiv.org/abs/2305.18323 | Xu et al. | May 2023 | Method + eval | A (self-reported, GPT-3.5 era) |
| 17 | Plan-and-Solve [OLDER, 2023] | https://arxiv.org/abs/2305.04091 | Wang et al. (ACL 2023) | May 2023 | Prompting method | A (GPT-3 era) |
| 18 | STORM [OLDER, 2024] | https://arxiv.org/abs/2402.14207 | Shao et al., Stanford | Feb 2024 | Method + eval | A (numbers not captured) |
| 19 | Spec Kit critique | martinfowler.com article by Birgitta Boeckeler (original NOT reached), digest via https://dev.to/juliantellez/agentic-harness-what-spec-driven-development-actually-is-1l8p | Thoughtworks | 2025 | Practitioner review | C |
| 20 | Orchestrating coding agents / Code Agent Orchestra | https://addyosmani.com/blog/code-agent-orchestra/ ; https://talks.addy.ie/oreilly-codecon-march-2026/ | Addy Osmani | Mar 2026 | Practitioner | C (leads only, not opened) |
| 21 | Deep Research: A Survey of Autonomous Research Agents | https://arxiv.org/html/2508.12752v1 | not captured | Aug 2025 | Survey | A- |

## 2. Findings by theme

### 2.1 Parallel vs sequential decomposition, and whether to delegate at all

- [EVIDENCE] Google/MIT, 180 controlled configurations, 4 benchmarks (Finance Agent, BrowseComp-Plus, PlanCraft, Workbench), 3 LLM families (OpenAI, Google, Anthropic). Multi-agent vs single-agent relative change ranged from +80.8% on decomposable financial reasoning to -70.0% on sequential planning (PlanCraft). A Hugging Face digest says all multi-agent variants lost 39-70% on sequential tasks. Source: https://arxiv.org/pdf/2512.08296 (via https://ui.adsabs.harvard.edu/abs/2025arXiv251208296K/abstract and a search digest). Limits: relative, not absolute, change. The "~45% single-agent baseline" threshold above which coordination stops paying is from secondary digests [UNVERIFIED-2nd]. The "predicts best strategy for 87% of held-out configs" claim is the authors' own.
- [EVIDENCE] Error amplification by topology (same paper): single 1.0x, centralized (orchestrator) 4.4x, hybrid 5.1x, decentralized 7.8x, independent parallel 17.2x. Digest cites Table 5 and the Google blog. Mechanism proposed: a validation bottleneck catches errors before they propagate. The 17.2x / 4.4x pair is on the Google blog; the 7.8x and 5.1x values are from a secondary digest [UNVERIFIED-2nd].
  Maps to: if you do parallelize, route through a verifying orchestrator rather than letting workers run independently.
- [EVIDENCE] Tran and Kiela (arXiv 2604.02460, Apr 2026): at equal thinking-token budgets (100-10,000), a single agent matched or beat five multi-agent variants (sequential, subtask-parallel, parallel-roles, debate, ensemble) on multi-hop QA (FRAMES, MuSiQue 4-hop). Multi-agent variants also spent more tokens. Theory via the Data Processing Inequality (communication loses information). Limits: preprint under review; one reviewer notes the result assumes the single agent uses its context perfectly, and reported token counts did not always match visible reasoning length. Task is multi-hop reasoning, not open-ended web research. Source: https://beancount.io/bean-labs/research-logs/2026/05/31/single-agent-outperforms-multi-agent-equal-token-budget [UNVERIFIED-2nd; primary arXiv not opened].
- [EVIDENCE, weak] Follow-ups in the same direction: "At Equal Inference Cost, Multi-Agent Structure Does Not Beat a Single Frozen Agent" (https://arxiv.org/pdf/2609.04217), "Phase Transition for Budgeted Multi-Agent Synergy" (https://arxiv.org/pdf/2601.17311), and a financial-review comparison where the team used 2.2-2.4x the single agent's tokens (https://arxiv.org/html/2610.27488). I saw only titles and one-line digests. Treat as pointers [UNVERIFIED].
- [EVIDENCE] The counter-direction: on WideSearch (200 questions, broad table-building tasks) multi-agent beat single-agent, attributed to a planner splitting a broad query into parallel sub-tasks while single agents break questions down too early and leave gaps. Best end-to-end success was only 5-7% depending on paper version (arXiv v1 vs ICLR abstract). Source: https://arxiv.org/pdf/2508.07999; the "multi-agent beats single" detail is from a search digest [UNVERIFIED-2nd]. Also see DeepWideSearch, mean success 2.39% (https://arxiv.org/pdf/2510.20168).
- [OPINION/production] Cursor (Jan 2026): flat peer agents coordinating through shared files and locks failed (lock hogging, risk-averse agents, churn). A planner/worker hierarchy worked: planners explore and create tasks (can spawn sub-planners), workers take one task and do not coordinate with each other; hundreds of workers, about a week, over a million lines claimed. Model choice mattered per role (GPT-5.2 was better at long autonomous work). Still treated as draft needing human review. Source: https://www.zenml.io/llmops-database/scaling-multi-agent-autonomous-coding-systems and mirrors [UNVERIFIED-2nd; cursor.com original not opened; scale figures are vendor claims with no quality metric].
- [OPINION/production] LangChain open_deep_research: supervisor decides if a brief splits into independent sub-topics and spawns parallel researchers with isolated contexts; defaults cap 6 supervisor rounds and 10 tool calls per researcher; sub-agents compress findings before returning. They dropped parallel report writing: multi-agent for research only, then one writer after all research is in, worked better. Source: https://github.com/langchain-ai/open_deep_research and https://www.langchain.com/blog/open-deep-research (via search digest). Self-reported RACE 0.4344 (#6 on the Deep Research Bench leaderboard, 2025-08-02). The leaderboard has since gone offline, and a newer 0.4943 with GPT-5 is also self-reported. No controlled single-vs-multi comparison was published.

Synthesis for the toolkit: the measured evidence says parallel multi-agent helps when the task is breadth-first and subtasks are independent (financial decomposition, WideSearch), and hurts when steps depend on each other or when total compute is held equal. The practitioner convergence is "parallel readers, single writer."

### 2.2 The dissent: arguments against multi-agent delegation

- [OPINION] Cognition, "Don't Build Multi-Agents" (Jun 2025). Two principles, per multiple secondary quotes: (1) share context, and share full agent traces, not just individual messages; (2) actions carry implicit decisions, and conflicting decisions carry bad results. Example: a Flappy Bird clone split into background and bird subtasks yields mismatched pieces. Recommendation: default to a single-threaded linear agent; use a compression model for long histories. No quantitative eval in the post. Source: https://cognition.com/blog/dont-build-multi-agents (excerpts via search; page not opened).
- [OPINION, revision] Cognition, "Multi-Agents: What's Actually Working" (2026-04-22). Original warning still holds for parallel writer swarms. What works: writes stay single-threaded; extra agents add intelligence, not actions; one main loop owns state, subagents are narrow stateless workers; most deployed multi-agent setups are read-only subagents (search, code search); coherence breaks when peers share memory. Sources: https://cognition.com/blog/multi-agents-working ; https://x.com/walden_yan/status/2047054554433462360 ; https://knomit.io/blog/consensus-by-merge/ (digests only). Note the caller should read this one in full, since it supersedes the 2025 essay.
- [EVIDENCE] Equal-budget results (2.1) and the sequential-task degradation (Google/MIT) are the measured counterpart to Cognition's opinion. They support "don't parallelize dependent work" and "check whether you are just spending more tokens."
- [EVIDENCE] The MAST finding (2.5) says most multi-agent failures are organizational (specification, misalignment, verification), not raw model weakness.
- [Conditions] Dissent applies chiefly to coding/state-mutating tasks with tightly coupled decisions. Pro-multi-agent results apply to read-heavy, breadth-first, independent subtasks. The sources do not actually contradict each other once the write/read split is made explicit.

### 2.3 Research process: planning, query generation, stopping

- [EVIDENCE, OLDER] ReWOO (May 2023): plan all tool calls up front, then fill observations. Reported 5x token efficiency and +4% accuracy on HotpotQA vs ReAct; robust to tool failure. Secondary cost figure about $3.97 vs $19.59 per 1,000 queries [UNVERIFIED-2nd]. Limits: GPT-3.5 era, static plans can't adapt to surprising results. Source: https://arxiv.org/abs/2305.18323.
- [EVIDENCE, OLDER] Plan-and-Solve (ACL 2023): "devise a plan, then carry it out" prompt; on GSM8K error analysis, semantic-misunderstanding errors 27%, missing-step 12%, calculation 7%; PS+ gave about +6.3% over zero-shot CoT across six arithmetic sets [UNVERIFIED-2nd figure]. GPT-3 text-davinci-003. Plan-first prompting fixes missing-step errors but not misunderstanding. Source: https://arxiv.org/abs/2305.04091. Little relevance to modern reasoning models, which plan internally.
- [EVIDENCE, OLDER] STORM (2024): perspective-guided question asking (mine perspectives from related articles, simulate writer-expert conversations grounded in search) improves outline coverage and entity recall vs direct prompting; evaluated on FreshWiki with Wikipedia-editor feedback. I did not capture the numbers. Weak on narrow or emerging topics with few related articles. Source: https://arxiv.org/abs/2402.14207. Maps to: generate queries from several explicit perspectives rather than one.
- [EVIDENCE] DeepSearchQA (Jan 2026): frames stopping as a core skill (judge whether the retrieved set is exhaustive). Reported failures: premature stopping (under-retrieval) and hedging (padding answers with low-confidence items to inflate recall). Source: https://arxiv.org/html/2601.20975 (abstract-level only). Companion: a paper on stagnating deep-research agents proposes a criteria-coverage controller that detects stalled loops and forces a new query (https://arxiv.org/pdf/2608.15191) [UNVERIFIED, abstract only].
- [EVIDENCE] BrowseComp (Apr 2025, OpenAI): Deep Research 51.5%; o1 without browsing 9.9%; GPT-4o 0.6% without and 1.9% with browsing. Accuracy rose with more browsing effort and with parallel sampling plus confidence voting (best-of-N best). Browsing models were worse calibrated. Limits: Deep Research was trained on BrowseComp-like data, so it is not a clean held-out test; the model comparison confounds browsing with training. Source: https://arxiv.org/abs/2504.12516, https://openai.com/index/browsecomp/ (via digest). Mean effort scaling: more tool calls and samples help on hard lookup, which is evidence for scaling effort with task difficulty.
- [EVIDENCE] AgentFold (Oct 2025): active "folding" of context at variable scales; AgentFold-30B-A3B 36.2% BrowseComp, 47.3% BrowseComp-ZH with SFT only. Digests add 62.1% WideSearch, 67.0% GAIA, context growth 3.5k to 7k tokens over 100 turns, and gains continuing to 256 turns [UNVERIFIED-2nd]. Source: https://arxiv.org/abs/2510.24699. Maps to context compression: summarize on a schedule the agent controls, keep recent detail, don't discard irreversibly.
- [OPINION] Practitioner guide claims OpenAI Deep Research asks clarifying questions before planning (https://blog.promptlayer.com/how-to-build-your-own-deep-research/, not confirmed by OpenAI docs) [UNVERIFIED].
- Gemini Deep Research planning/stopping: nothing retrieved [GAP].

### 2.4 Context passing, compression, context engineering

- [EVIDENCE] Chroma Context Rot (Jul 2025): 18 models (incl. GPT-4.1, Claude 4, Gemini 2.5, Qwen3); performance degrades with input length even on simple tasks, well before the window fills; harder when needle-question similarity is lower; distractors compound (Claude models tended to abstain, GPT models to hallucinate); a shuffled haystack beat a coherent one; on LongMemEval a focused ~300-token prompt beat the full ~113K-token prompt containing the answer. Source: https://www.trychroma.com/research/context-rot. All numbers via secondary summaries [UNVERIFIED-2nd]; model names are 2025-era (Claude 4 etc.), so the models are outdated in October 2026 though the direction of the finding is the point. Chroma is a vector-DB vendor with an interest in retrieval; treat as B.
- [EVIDENCE, OLDER] Lost in the Middle (2023, TACL 2024): accuracy highest when relevant text is at start or end of context, lowest in the middle, on multi-doc QA and key-value retrieval; persists in long-context models. Source: https://arxiv.org/abs/2307.03172. Foundational but pre-dates current models; don't assume the U-curve holds unchanged.
- [OPINION + tension] Cognition says pass full traces; LangChain's design has researchers compress findings before returning to the supervisor; Tran and Kiela argue decomposition loses information in transit. Chroma suggests big contexts rot. Reconciliation: pass the full trace where decisions are interdependent and writes are happening; compress where subagents are read-only and the output is evidence. Compressing with pointers back to sources (see 2.6) seems to be the common practice.

### 2.5 Failure modes

- [EVIDENCE] MAST (Cemri et al., arXiv 2503.13657): 14 failure modes in 3 groups (system design/specification, inter-agent misalignment, task verification), annotated from traces of 7 open-source multi-agent frameworks (about 1,600 traces in the released dataset; the core human-annotated analysis is smaller, about 150, per one digest). Failure rates 41% to 86.7% across systems. Category shares differ by source (41.8/36.9/21.3 vs 44.2/32.3/23.5 percent), so do not quote them without checking the paper. Common modes include step repetition and not recognizing when to stop. Human annotator kappa 0.88; the LLM-judge pipeline reported 94% accuracy, kappa 0.77 with few-shot (0.58 o1 zero-shot) per secondary digests. ChatDev interventions: +15.6 for a verification step and +9.4 for tighter role specs (unit, percentage points vs relative, is inconsistent across sources). Authors argue better models alone won't fix it. Limits: open-source frameworks of 2024 vintage and older models; intervention test is small. Source: https://arxiv.org/abs/2503.13657 (digests via search).
- [EVIDENCE] DeepSearchQA: premature stopping and hedging (2.3).
- [EVIDENCE] Cursor: lock-based peer coordination failure (2.1) [UNVERIFIED-2nd].
- [OPINION] Cognition: conflicting implicit decisions among parallel writers (2.2).
- Production silent-failure taxonomies exist (https://arxiv.org/pdf/2606.14589, https://arxiv.org/pdf/2606.08162) [UNVERIFIED, titles only].

### 2.6 Brief contents and delegation hygiene (practitioner, no controlled evidence)

- [OPINION] What a delegation brief should hold, per 2026 practitioner notes (leads from search digest; originals not opened): goal and why it matters; what is already known or ruled out; where to start; scope limits (read-only? which directories); output format; definition of done; a stated default for ambiguity or an instruction to stop and report (subagents cannot ask mid-task); request a summary plus evidence pointers (file:line, command with exit code) so claims are cheap to spot-check; read the real diff, not the agent's summary; send fixes back to the same agent to preserve its context; a two-level structure keeps the orchestrator's context clean. Sources to read in full: https://addyosmani.com/blog/code-agent-orchestra/, https://spring.io/blog/2026/01/27/spring-ai-agentic-patterns-4-task-subagents/, https://dev.to/kasundsilva/orchestrating-sub-agents-for-cost-efficient-engineering-1pl3.
- MAST's +9.4 role-specification gain is the only measured support for "better briefs help."
- [OPINION] Spec-driven development (Boeckeler / Thoughtworks via digest, original at martinfowler.com not reached): Spec Kit is "spec-first only, not spec-anchored"; output bloat of repetitive markdown ("I'd rather review code than all these markdown files"); agents still ignored the spec and regenerated classes the research step had already catalogued; checklist compliance is judged by the model with no enforcement; risk of repeating model-driven-development rigidity; "spec" may become a synonym for "detailed prompt." Practitioners also say it is too heavy for small fixes and worth it for long-lived, multi-agent, traceability-heavy work. Source: https://dev.to/juliantellez/agentic-harness-what-spec-driven-development-actually-is-1l8p (secondary). No measured outcomes found anywhere on SDD.

### 2.7 Verification

- [EVIDENCE] Google/MIT: validation bottleneck in a centralized topology cuts error amplification from 17.2x to 4.4x (2.1). MAST: adding a verification step helped most (+15.6, units uncertain).
- [EVIDENCE] Citation fabrication is documented in deep-research outputs: an audit found a cited claim that did not match its source in an OpenAI Deep Research report, and OpenAI's agent showed a lower hallucinated-URL rate than Gemini 2.5 Pro Deep Research in one 2026 study, cause unknown. Sources: https://arxiv.org/pdf/2603.03299 and https://arxiv.org/pdf/2508.15804 (digests only) [UNVERIFIED].
- [EVIDENCE] BrowseComp: browsing agents are overconfident when wrong (calibration), so self-reported confidence is a poor check.
- DeepResearch Bench FACT metric (citation accuracy and number of effective citations) and RACE (comprehensiveness, depth, instruction-following, readability) exist as measures. The repo notes the judge model changed (GPT-5.4-mini for FACT), so scores across time are not comparable. Source: https://github.com/Ayanami0730/deep_research_bench. Note RACE is LLM-judged, so it is itself unverified.

## 3. Disagreements and tradeoffs

| Question | Position A | Position B | Conditions |
|---|---|---|---|
| Multi-agent at all? | Cognition 2025: default to single thread. Tran/Kiela 2026: single agent wins at equal tokens | Google/MIT: +80.8% on decomposable tasks; WideSearch: multi-agent beats single on broad tasks | A holds for sequential, coupled, write-heavy work and compute-matched comparisons; B for independent, breadth-first, read-heavy work |
| Has Cognition changed its mind? | 2025: don't build | 2026-04: read-only subagents work if writes stay single-threaded | Same author, so the position is narrowed, not reversed |
| Pass full traces vs compress | Cognition: full traces | LangChain/AgentFold: compress findings; Chroma: long context rots | Full where decisions interlock; compress for read-only evidence gathering |
| Plan up front vs adaptive | ReWOO: plan first, 5x cheaper (2023) | Stagnation/stopping papers and STORM-style iteration need replanning | Static plans for predictable tool chains; adaptive for open web research |
| Is the comparison fair? | Multi-agent papers often use more tokens | Equal-budget papers may favor single agent via assumptions (perfect context use) | Always report tokens and calls, not just accuracy |
| Spec-driven development | Advocates: specs stabilize agents | Boeckeler: bloat, ignored specs, waterfall feel | Long-lived multi-agent work vs small tasks; no measured data either way |

## 4. Outdated items

- ReWOO (2023, GPT-3.5), Plan-and-Solve (2023, GPT-3), Lost in the Middle (2023), STORM (2024) are [OLDER]: foundational ideas, but numbers come from models far weaker than current ones.
- Chroma Context Rot tested Claude 4 / GPT-4.1 / Gemini 2.5: pre-Claude-5 models, so its numbers should not be treated as current model behavior.
- MAST traces come from 2024-era frameworks and models.
- DeepResearch Bench and Open Deep Research leaderboards: the Open Deep Research #6 ranking is a 2025 snapshot and the leaderboard is offline; the benchmark's judge model has changed.
- Cognition's 2025 "Don't Build Multi-Agents" is superseded in part by its own 2026-04-22 follow-up.
- Cursor's GPT-5.2 model-choice remarks are model-version specific.
- Several arXiv IDs returned by search (e.g. 2609.04217, 2610.27488, 2608.15191) have 2026 month prefixes consistent with today's date; I could not confirm them, and some search metadata looked inconsistent.

## 5. Gaps (what I could not close)

1. No primary source was read in full (network block). Re-verify at least: the Cognition posts (both), arXiv 2512.08296 Table 5 and the 45% threshold, arXiv 2503.13657 category percentages and intervention units, arXiv 2604.02460, the Chroma report, the Cursor post, and the LangChain open_deep_research write-up.
2. Gemini Deep Research and OpenAI Deep Research internals (planning, stopping): only third-party commentary; no system card text retrieved.
3. GAIA results and effort-scaling curves: not searched; BrowseComp-Plus numbers not found.
4. DeepResearch Bench paper's own findings and numbers not captured.
5. STORM numeric results not captured.
6. No measured study of brief quality (what to put in a delegation prompt) beyond MAST's role-specification intervention; no measured study of spec-driven development.
7. No independent replication found for ReWOO's 5x or for any LangChain/Cursor self-reported figure.
8. LangChain's "How and when to build multi-agent systems" (the likely direct reply to Cognition) was not retrieved; only its title was confirmed.
9. Rebuttals of Cognition: I found none that argue for peer-style parallel writers; the main counter-evidence is the WideSearch / Google-MIT data on read-heavy decomposable tasks, not an explicit rebuttal essay.
