# How Claude should research, and how it should plan work for other agents

*Run `research/2026-10-31-agent-research/` · as of 2026-10-31 · tier: DEEP · sources ranked in [sources.md](sources.md)*

**Tags.** `[E]` evidence: a measured result or documented outcome. `[O]` opinion: a
recommendation or assertion.

**Verification status.**
- **✓** I checked it against the original page text on 2026-10-31.
- **~** A worker read it through a fetch tool's summary. Likely right, but not re-checked.
- **⚠** Only seen in search-result snippets, because the host was blocked in this environment.
  Unverified. See *Method and limitations*.

---

## Top patterns

1. **Decide whether to delegate before deciding how.** Splitting work across agents pays off
   on breadth-first, independent, read-heavy work, and costs a lot of tokens.
   - Anthropic measures 3–10x the tokens of a single agent for equivalent tasks
     [E ✓, [Anthropic, Jan 2026](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)].
   - It names only three situations where multiple agents consistently win: context pollution,
     parallelisable tasks, and specialisation.
   - Independent studies report big gains on decomposable tasks and big losses on sequential ones,
     and parity at equal token budgets [E ⚠, Google/MIT; Tran & Kiela].
   - Current Claude models over-delegate unless told not to [O ✓, [Opus 5 prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)].
2. **Scale effort with explicit tiers and budgets, not adjectives.** Anthropic's production
   rules [O ✓, [multi-agent research post](https://www.anthropic.com/engineering/multi-agent-research-system)]:
   - simple fact-finding: 1 agent, 3–10 tool calls;
   - comparisons: 2–4 subagents, 10–15 calls each;
   - complex research: more than 10 subagents.

   They added these after early agents spawned "50 subagents for simple queries"
   [E, anecdotal ✓].
3. **A brief has a fixed anatomy:** one objective, the purpose, an output format, guidance on
   tools and sources, scope boundaries, and a budget with a stop rule. Two tests go with it:
   - *Completeness:* "IF all the subagents followed their instructions very well, the results
     in aggregate would allow you to give an EXCELLENT answer" [O ✓, Anthropic lead prompt].
   - *Overlap:* vague briefs caused documented duplicate work [E, anecdotal ✓].
4. **Classify the query, then order the work.** Depth-first, breadth-first or straightforward.
   Blocking sub-tasks go first and alone, then the rest fan out in parallel
   [O ✓, [cookbook lead prompt](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents/prompts)].
5. **Search like an expert: start wide, then narrow.**
   - Use short queries and prefer primary sources.
   - Spend one search on evidence that would prove the likely answer wrong.
   - Stop on diminishing returns.

   Unbounded searching and SEO-farm sources are both documented failures
   [E, anecdotal ✓, Anthropic]. Benchmarks name *premature* stopping as a failure too [E ⚠, DeepSearchQA].
6. **Isolate context, return by reference.**
   - A subagent receives only its prompt string [✓, [Agent SDK docs](https://code.claude.com/docs/en/agent-sdk/subagents)].
   - It explores in its own context and returns "a condensed, distilled summary … (often
     1,000–2,000 tokens)" [O ✓, [context engineering post](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)].
   - Full output goes to files that are passed by path.
7. **Parallel readers, one writer.** Every source that discusses this converges here:
   Anthropic's lead synthesises, LangChain dropped parallel report writing [O, via its README ✓],
   Cognition's 2026 revision keeps writes single-threaded [O ⚠], and coding setups serialise
   implementers or give each file one owner [O ✓, superpowers, wshobson].
8. **Verify independently, mechanically first.**
   - Check quotes with a script against cached pages.
   - Then use a fresh-context verifier with explicit verdict criteria that never sees the draft.
   - Unverifiable is not refuted.
   - A verifier with no criteria "will rubber-stamp the generator's output"
     [O ✓, [Anthropic, Apr 2026](https://claude.com/blog/multi-agent-coordination-patterns)].
   - The measured support (validation bottlenecks cut error amplification; adding a
     verification step had the largest effect in MAST) is ⚠.
9. **Notes are routing aids, not authorities.** The lead reopens the original for every
   load-bearing number or quote [O ✓, daymade, pedrohcgs]. In this run, the fetch tool's
   summariser paraphrased "quotes" [E, observed here; tomkd555 reports the same].
10. **Update 2025 advice for 2026 models and tools.**
    - Opus 5 verifies its own work unprompted, so remove "double-check" scaffolding [✓].
    - The `Task` tool is now `Agent` [✓].
    - Custom commands have merged into skills [✓].
    - Subagents can nest three layers deep [✓].
    - Claude Code ships a `/deep-research` workflow [✓].
    - The well-known 90.2% multi-agent gain was measured on Claude Opus 4 and Sonnet 4 [✓].

---

## 1. When to delegate at all

**What Anthropic says** [all ✓]:
- **Three situations.** Multi-agent systems consistently win "when context pollution degrades
  performance, when tasks can run in parallel, and when specialization improves tool selection
  or task focus. Outside these situations, the coordination costs typically exceed the
  benefits" [O, [when-to-use post, Jan 23 2026](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)].
  The same post measured 3–10x token overhead [E], and says the benefit of parallelism is
  "thoroughness, not speed".
- **Token spend explains most of the gain.** In Anthropic's BrowseComp analysis, three factors
  explained 95% of performance variance, and "token usage by itself explains 80%". Multi-agent
  systems "use about 15× more tokens than chats" [E, [multi-agent research post, Jun 13 2025](https://www.anthropic.com/engineering/multi-agent-research-system)].
  The headline result was "a multi-agent system with Claude Opus 4 as the lead agent and Claude
  Sonnet 4 subagents outperformed single-agent Claude Opus 4 by 90.2% on our internal research
  eval" [E, internal eval, older models].
- **Current models over-delegate.** "Claude Opus 5 delegates to subagents more readily than prior
  models … Do not delegate work you can finish yourself in a handful of tool calls, and do not
  use subagents to verify or double-check your own work" [O, [Opus 5 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5)].
- **No smarter answer.** Claude Code's best-practices page says a subagent gives "parallelism or a
  fresh pair of eyes … but not a smarter answer" [O, [best practices](https://code.claude.com/docs/en/best-practices)].
- **Start simple.** For most use cases, "we recommend starting with orchestrator-subagent"
  [O, [coordination patterns, Apr 10 2026](https://claude.com/blog/multi-agent-coordination-patterns)].

**What independent studies report** [all ⚠, from search snippets; numbers to confirm]:
- **Google/MIT, *Towards a Science of Scaling Agent Systems* (Dec 2025).** 180 configurations,
  4 benchmarks, 3 model families. Multi-agent results ranged from **+80.8%** on decomposable
  financial reasoning to **−70%** on sequential planning (PlanCraft). Error amplification was
  **17.2x** for independent parallel agents vs **4.4x** with a centralised orchestrator (single
  agent = 1x) [E ⚠, [arXiv 2512.08296](https://arxiv.org/abs/2512.08296)].
- **Tran & Kiela (Apr 2026).** At equal thinking-token budgets, a single agent matched or beat
  five multi-agent designs on multi-hop QA [E ⚠, preprint, arXiv 2604.02460]. A reviewer
  objects that it assumes the single agent uses its context perfectly.
- **WideSearch (2025).** On broad "fill the table" tasks, multi-agent beat single-agent, but the
  best end-to-end success was only ~5%. Breadth tasks are hard for everyone
  [E ⚠, [arXiv 2508.07999](https://arxiv.org/abs/2508.07999)].

**The dissent and its revision.**
- *Don't Build Multi-Agents* (Cognition, Jun 2025) argued for single-threaded agents: share
  full traces, because "actions carry implicit decisions" [O ⚠].
- Its April 2026 follow-up narrows this: read-only subagents work, provided writes stay
  single-threaded [O ⚠, [cognition.com](https://cognition.com/blog/multi-agents-working)].

**Synthesis.** Once you separate reading from writing, the sources mostly agree.
- Delegate breadth-first, independent, read-heavy work.
- Keep coupled, sequential or write-heavy work in one thread.
- In any comparison, ask whether the "multi-agent win" is really just "more tokens".

## 2. Research process: queries, breadth vs depth, triage, stopping

**Query strategy** [O ✓ unless noted]:
- **Start wide, then narrow.** "Start wide, then narrow down … Agents often default to overly
  long, specific queries that return few results" [Anthropic multi-agent post].
- **Keep queries short.** Anthropic's published subagent prompt says "under 5 words", and to
  broaden when results are sparse [cookbook `research_subagent.md`].
- **Generate queries from several perspectives**, not one: STORM's perspective-guided question
  asking improved outline coverage [E ⚠, [arXiv 2402.14207](https://arxiv.org/abs/2402.14207), 2024].
- **Search for disconfirming evidence.** Spend at least one search on what would make the likely
  answer wrong, in the first half of the budget so it's never the call that gets cut
  [O ✓, tomkd555 `research-collector.md`]. daymade's brief fields include "Disconfirming
  Evidence" and "Load-Bearing Claims".

**Breadth vs depth.**
- **Classify first** [O ✓, cookbook lead prompt]:
  - depth-first: "multiple perspectives on the same issue";
  - breadth-first: "distinct, independent sub-questions";
  - straightforward: "a single focused investigation".
- **Depth-first** gets agents with different *methods or angles*.
- **Breadth-first** gets one agent per sub-question.
- **Straightforward** shouldn't fan out at all.

**Source triage** [O ✓ unless noted]:
- **Prefer original sources.** Human testers found early agents "consistently chose SEO-optimized
  content farms over authoritative but less highly-ranked sources like academic PDFs or personal
  blogs". The fix was source-quality heuristics in the prompt [E, anecdotal, Anthropic].
- **Flag speculation.** The subagent prompt marks future tense, "could/may", projections and
  quoted superlatives.
- **Escalate conflicts.** Conflicts go up to the lead unresolved.
- **Grade by origin** (A primary/peer-reviewed, B vendor/preprint, C media/blog) and label
  self-reported numbers [tomkd555].
- **Source quality is an eval dimension.** Anthropic's research eval scores source quality
  alongside factual and citation accuracy [✓, multi-agent post].
- **Fetch full pages, not snippets** [cookbook subagent prompt]. Quote only from raw page text,
  since summarising fetch tools paraphrase [O ✓, tomkd555; observed in this run].

**Stopping** [O ✓ unless noted]:
- **Budgets.** Anthropic's subagent prompt sets a per-task budget (<5 / ~5 / ~10 / up to 15 calls
  by difficulty), a hard cap of 20 calls / ~100 sources, and "when you are no longer finding new
  relevant information … STOP".
  - *Note:* the same prompt also says "MINIMUM of five distinct tool calls", which contradicts
    its own "under 5" tier [✓]. Pick one budget per tier.
- **Two empty searches.** tomkd555 stops a worker early "once two consecutive searches add no new
  source". Claude Code's workflow docs use a similar rule: stop when "two rounds in a row make no
  progress" [✓, [workflows](https://code.claude.com/docs/en/workflows)].
- **Both directions fail.** DeepSearchQA (Jan 2026) names *premature stopping* and *hedging*
  (padding answers with low-confidence items) as failures [E ⚠, [arXiv 2601.20975](https://arxiv.org/abs/2601.20975)].
  BrowseComp found accuracy rises with browsing effort and that browsing agents are poorly
  calibrated [E ⚠, [arXiv 2504.12516](https://arxiv.org/abs/2504.12516)]. So stop rules should
  be explicit, not left to the agent's confidence.
- **More tokens can have sharply diminishing returns.** LangChain's open_deep_research reports
  RACE **0.4309** at 58.0M tokens / $45.98 with its defaults, vs **0.4344** at 207.0M tokens /
  $87.83 for its leaderboard submission [E ✓, [README](https://github.com/langchain-ai/open_deep_research)].
  The model configurations differ, so this is suggestive only, but it is a useful counterweight
  to "token usage explains 80% of the variance".

## 3. What a good delegation brief contains

**Anthropic's checklist** [O ✓, cookbook `research_lead_agent.md`]:
- "Specific research objectives, ideally just 1 core objective per subagent".
- Expected output format.
- Background context and "how the subagent should contribute to the research plan".
- Key questions.
- Starting points, a definition of reliable sources, and sources to avoid.
- Specific tools.
- "precise scope boundaries to prevent research drift".

The blog version is shorter: "an objective, an output format, guidance on the tools and sources
to use, and clear task boundaries" [✓].

**Why it matters** [E, anecdotal ✓]: "one subagent explored the 2021 automotive chip crisis
while 2 others duplicated work investigating current 2025 supply chains, without an effective
division of labor." MAST's failure taxonomy puts *specification* problems among the largest
failure categories, and a tighter role specification measurably helped on ChatDev [E ⚠; units
inconsistent across digests].

**What practitioners add** [O ✓ unless noted]:
- **A budget and a stop rule** in the brief [tomkd555, daymade "Stop Rule"].
- **A decision question:** what the answer will change [daymade].
- **An output path plus a short reply contract:** file path, then ≤300–400 words
  [tomkd555, daymade, this run].
- **Fail closed on missing inputs:** "return only `{"error": "<the missing items>"}`" [tomkd555],
  because "nobody can answer a question during your run".
- **What's already known or ruled out, and a default for ambiguity** [O ⚠, practitioner posts].
- **The other workers' scopes**, so this one doesn't duplicate them [this run's briefs].
- **The reason behind each constraint.** Claude "can generalize from the explanation" [O ✓,
  Anthropic prompting guide].
- **The stranger test.** "Show your prompt to a colleague with minimal context on the task … If
  they'd be confused, Claude will be too" [O ✓, same guide]. This is what the `brief-reviewer`
  agent automates.

**Subagent descriptions are routing briefs too.** Claude delegates based on each subagent's
`description`. "use proactively" encourages delegation, and combined descriptions over 15,000
tokens trigger a startup warning [✓, [sub-agents docs](https://code.claude.com/docs/en/sub-agents)].

There is **no controlled study** comparing brief formats. Everything above beyond the MAST
intervention is opinion backed by failure anecdotes.

## 4. Decomposition: parallel vs sequential

**Dependencies first** [O ✓, cookbook lead prompt]: "when other tasks will depend on results from
one specific task, always create a subagent to address that blocking task first." For example,
list the EU countries first, then fan out by region.

**Parallel launches** [✓]:
- The lead launches "3-5 subagents in parallel rather than serially" and subagents use tools in
  parallel. Together these "cut research time by up to 90% for complex queries" [E, Anthropic].
- That figure compares parallel with *serial subagents*. It doesn't contradict the claim that
  multi-agent systems "take longer overall than single-agent systems", which compares against
  one agent.

**Typical counts** [O ✓]:
- Anthropic's lead prompt: "default to using 3 subagents for most queries", 5–10 for
  high-complexity tasks, "maximum 20". "Prefer fewer, more capable subagents".
- Claude Code agent teams: "Start with 3-5 teammates".

**Writers need ownership** [O ✓ unless noted]:
- superpowers: "Never dispatch multiple implementation subagents in parallel (conflicts)".
- wshobson's team lead allows parallel implementers with "One owner per file".
- Anthropic's C-compiler project ran 16 agents with no orchestrator, using git-file locks. On one
  giant task "every agent hit the same bug and overwrote the others' fixes". The fix was to
  partition work with an oracle [E ~].

**Don't split by role** [O ✓]. Agents "split by problem type … engage in a 'telephone game'". In
one role-split experiment they "spent more tokens coordinating than executing" [when-to-use post].

**Plan first, or adapt as you go?**
- ReWOO (2023) planned all tool calls up front and reported ~5x token savings vs ReAct
  [E ⚠, older models].
- Open-web research needs replanning when results surprise, which is why both Anthropic's and
  LangChain's systems re-plan between waves.
- Use static plans for predictable tool chains, and adaptive waves for research.

**Scale beyond chat** [✓]: Claude Code's 2026 dynamic workflows are JavaScript files that move
the loop into code. They run up to 16 concurrent agents by default and 1,000 agents per run, and
"Claude's context holds only the final answer" [[workflows](https://code.claude.com/docs/en/workflows)].
Reach for these when a task needs dozens of agents.

## 5. Context: what goes down, what comes back

**What goes down.** "The only content you pass from parent to subagent is the Agent tool's prompt
string, so include any file paths, error messages, or decisions the subagent needs directly in
that prompt" [✓, Agent SDK docs]. Subagents also load the project's CLAUDE.md, but not your
conversation [✓, Agent SDK docs; the `omitClaudeMd` field turns that off].

**What comes back.**
- "intermediate tool calls and results stay inside the subagent; only its final message returns
  to the parent" [✓].
- Aim for 1,000–2,000 tokens [✓, context engineering post].
- Better still, write output to a filesystem and pass "lightweight references back", which
  reduces "the 'game of telephone'" [✓, multi-agent post].
- Every mature repo does this: notes/evidence files plus a short reply [✓, tomkd555, daymade,
  SDK demo].

**Compression** [O]:
- **Anthropic's compaction advice:** "Start by maximizing recall … then iterate to improve
  precision". Tool-result clearing is "one of the safest lightest touch forms of compaction" [✓].
- **Fresh context or compaction?** The prompting guide recommends starting a fresh context rather
  than compacting when state lives in files (progress notes, git) [~].
- **Compression vs full traces.** LangChain compresses researcher findings before they return
  [O, README ✓]. Cognition argues for sharing full traces when decisions interlock [O ⚠].
- **Reconciling them:** compress evidence from read-only workers, keeping pointers to sources;
  pass full context where agents must stay consistent with each other's decisions.

**Long context still degrades.**
- Anthropic: "as the number of tokens in the context window increases, the model's ability to
  accurately recall information from that context decreases" [✓].
- Chroma's *Context Rot* report found degradation well before the window fills, across 18
  (2025-era) models [E ⚠].
- With 1M-token windows "you'll rarely run out of context", but "you can still pay for context
  you don't need" [✓, best practices]. Isolation is now about focus and cost more than capacity.

**Persistence across sessions** [O]:
- Keep a plan or ledger file so work survives compaction and handoffs [✓, superpowers
  "per-plan ledger"; Anthropic's lead saved its plan to memory].
- Use hooks for re-injection: SessionStart with matcher `compact` [✓, docs; pedrohcgs ships
  PreCompact/SessionStart restore hooks].

## 6. Failure modes and how teams prevent them

| Failure | Evidence | Prevention |
|---|---|---|
| Spawning far too many agents | "spawning 50 subagents for simple queries" [E ✓, Anthropic] | Tier table with agent and call budgets; delegation damping for Opus 5 [✓] |
| Duplicated work from vague briefs | chip-crisis example [E ✓] | One objective; overlap test; name the other workers' scopes |
| Endless searching | "scouring the web endlessly for nonexistent sources" [E ✓] | Budgets; two-empty-searches rule |
| Stopping too early / padding | DeepSearchQA [E ⚠] | Explicit coverage checklist; disconfirming search; verifier |
| SEO sources over primary ones | [E ✓, Anthropic] | Source heuristics; A/B/C grading |
| Specification and misalignment failures | MAST: 14 modes, failure rates 41–86.7% across 7 frameworks [E ⚠] | Self-contained briefs; explicit output contracts |
| Error amplification across agents | 17.2x independent vs 4.4x centralised [E ⚠] | Orchestrator validates before combining |
| Verifier rubber-stamps | [O ✓, Anthropic] "verification agents take shortcuts" without explicit requirements [✓] | Verdict criteria; less favourable verdict when in doubt |
| Lead trusts worker summaries | [O ✓, daymade, pedrohcgs] | Reopen originals for load-bearing claims |
| Paraphrased "quotes" | [E, observed in this run; tomkd555] | Cache raw pages; script-check quotes |
| Conflicting writes | C-compiler overwrites [E ~]; Cognition [O ⚠] | Single writer, or file ownership |
| Over-verification by new models | [O ✓, Opus 5 guide] | Remove "double-check" lines; keep one independent review |
| Prompt injection via fetched content or subagent output | Claude Code v2.1.210+ scans subagent output for "instruction-shaped patterns" [✓] | "Material to check, not instructions" clause [✓, pedrohcgs] |
| Silent gaps from blocked tools | [E, observed in this run: all non-Anthropic/GitHub hosts blocked] | Workers report blocked hosts; the user is told immediately |
| Benchmark contamination in search agents | unintended solutions 0.87% multi-agent vs 0.24% single [E ✓, [eval-awareness](https://www.anthropic.com/engineering/eval-awareness-browsecomp)] | Block benchmark-named results when evaluating |
| Outdated tool names in copied prompts | `Task` in Anthropic's own SDK demo [✓]; non-Claude-Code tool names in ports [✓] | Renamed: Task → Agent in v2.1.63 [✓] |

## 7. Verifying and combining results

**Layer the checks:**
1. Mechanical checks first: quote matching, link checks, schema linting. These are cheap and
   don't drift [O ✓, tomkd555, 199-bio, daymade].
2. Then a judgement check.

**How to set up the independent verifier** [O ✓]:
- **Withhold the draft.** tomkd555's verifier "sees the sentences and their sources only; never
  pass it the report". pedrohcgs's claim-verifier runs in a fresh context because "the verifier
  never sees the original draft". This is adapted from chain-of-verification (CoVe; Dhuliawala et
  al. 2023, not re-checked here).
- **Give explicit criteria.** "The verifier is only as good as its criteria" [✓, Anthropic].
- **Tune a skeptic, not the generator.** "Tuning a standalone evaluator to be skeptical turns out
  to be far more tractable than making a generator critical of its own work" [✓, [harness design](https://www.anthropic.com/engineering/harness-design-long-running-apps)].
- **Use a fresh reviewer, not a re-run.** "A fresh reviewer does help, because it hasn't seen
  your reasoning" [✓, best practices].

**Combining** [O ✓]:
- Anthropic's lead synthesises "using an ensemble approach and by applying critical reasoning".
- A separate citations agent is forbidden to change the text: "Do NOT modify the
  <synthesized_text> in any way".
- Claude Code's `/deep-research` "votes on each claim" and filters out claims that don't survive
  cross-checking. Claims it can't check are listed "as unverified instead of counting it as
  refuted" [✓, workflows docs].

**Evaluating the research system itself** [E/O ✓]:
- Anthropic started with "about 20 queries" representing real usage.
- It scored outputs with an LLM judge rubric: factual accuracy, citation accuracy, completeness,
  source quality, tool efficiency. "A single LLM call with a single prompt outputting scores from
  0.0-1.0 and a pass-fail grade was the most consistent and aligned with human judgements". Human
  testers still caught the SEO bias.
- Anthropic's evals guide says "20-50 simple tasks drawn from real failures is a great start".
  It recommends giving judges an "Unknown" option and grading "what the agent produced, not the
  path it took".

## 8. Packaging a reusable setup (current syntax, verified in the docs)

- **Subagents** live in `.claude/agents/*.md` [✓, [sub-agents](https://code.claude.com/docs/en/sub-agents)].
  - Required frontmatter: `name` and `description`. Useful fields: `tools`, `disallowedTools`,
    `model` (an alias or a full ID), `effort`, `maxTurns`, `memory`, `isolation`, `background`.
  - "Claude Code ignores a field it doesn't recognize without reporting an error", so typos fail
    silently.
  - Background subagents (the default) keep only a fixed set of built-in tools, which includes
    WebSearch, WebFetch, Read, Write, Grep, Glob, Bash and ToolSearch.
- **Skills** live in `.claude/skills/<name>/SKILL.md` [✓, [skills](https://code.claude.com/docs/en/skills)].
  - "Custom commands have been merged into skills". `/name` invokes the skill, and `$ARGUMENTS`
    carries the arguments.
  - "Keep SKILL.md under 500 lines". Descriptions are truncated at 1,536 characters in the listing.
- **Permissions** are evaluated "deny, then ask, then allow" [✓]. `WebFetch(domain:…)` scopes
  fetches to a domain. Bash rules take `*` wildcards anywhere.
- **Repo layouts** [O ✓, from the repos]:
  - a plugin marketplace (root `.claude-plugin/marketplace.json` plus `plugins/<name>/…`), used
    by tomkd555, wshobson, EveryInc and superpowers;
  - a fork-this-template repo (pedrohcgs: 3.1k forks vs 1.7k stars);
  - per-run output folders (`research/{YYYYMMDD}-{slug}/` in tomkd555).

  This repo uses the template layout with per-run folders. It can become a plugin later.
- **Size discipline** [O]: wshobson caps context files at ~150 lines. The CLAUDE.md docs say
  "target under 200 lines". The longest skill reviewed (daymade, 36 KB) is hard to port.

## Where sources disagree

| Question | Position A | Position B | When each holds |
|---|---|---|---|
| Delegate at all? | Anthropic 2025 lead prompt: delegate all substantial gathering; Google/MIT +80.8% on decomposable tasks ⚠ | Opus 5 guide: don't delegate small work; Tran & Kiela: single agent ties at equal tokens ⚠; Cognition 2025 ⚠ | A: breadth-first, read-heavy, high-value tasks. B: small, sequential or write-heavy work, or compute-matched comparisons |
| Is parallelism faster? | "cut research time by up to 90%" ✓ | multi-agent "take longer overall" ✓ | A: parallel vs serial subagents. B: multi-agent vs one agent |
| Token multiple | ~15x vs chat ✓ | 3–10x vs single agent ✓ | Different baselines |
| Pass full traces or compress? | Cognition: full traces ⚠ | LangChain/Anthropic: compressed summaries ✓ | Full where decisions interlock; compress for read-only evidence |
| Verification subagents | Anthropic blog: verifiers work with criteria ✓; MAST: verification step helps ⚠ | Opus 5 guide: drop "use a subagent to verify" ✓ | Keep one *independent* reviewer with criteria; drop generic self-double-checks |
| Lead writes the report? | dimayip / Anthropic: lead synthesises ✓ | SDK demo: delegated report-writer ✓ | Lead when synthesis needs cross-source judgement; a writer when formatting is heavy and inputs are files |
| Human checkpoints | superpowers: don't pause between tasks ✓ | conductor, ce-plan: approval gates ✓ | Compatible: gate once at plan approval, then run |
| Default tier when unsure | tomkd555: middle tier ✓ | ce-plan: heavier tier ✓ | Choose based on the cost of being wrong |
| LLM judges | Anthropic research post: single judge matched humans ✓ | Agent SDK blog: "generally not a very robust method" ~ | Judges after calibration against humans; rules first where possible |
| Spec-driven development | spec-kit and others: specs stabilise agents | Böckeler: bloat, ignored specs ⚠ | Long-lived multi-agent work vs small tasks; no measured data either way |

## Outdated or superseded material

- **Model names in 2025 sources.** The 90.2% result (Opus 4 + Sonnet 4), "context window exceeds
  200,000 tokens", and Chroma's Claude 4 / GPT-4.1 results all predate the Claude 5 family and 1M
  windows. Current docs list Fable 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5.
- **Tool and feature changes:**
  - The Task tool became Agent in Claude Code v2.1.63; `Task(...)` still works as an alias.
    Anthropic's own `claude-agent-sdk-demos` research agent still uses `Task`, plus `haiku`
    everywhere and `bypassPermissions`.
  - Subagents could not nest in older docs; they can now, up to three layers deep.
  - `.claude/commands/` has been merged into skills; it still works, but new work should use skills.
- **Superseded advice:**
  - Context resets were introduced to work around Sonnet 4.5's "context anxiety" and later
    dropped [~, harness posts].
  - The best-practices page retires "use subagents to protect your context window" as a default,
    along with "think hard", ALL-CAPS emphasis and "double-check" lines [✓].
- **Ports of Anthropic's research prompts.** These still use `run_blocking_subagent` and
  `complete_task`, which are not Claude Code tools, and the "MINIMUM of five tool calls" rule.
- **Building Effective Agents (Dec 2024).** Foundational (orchestrator-workers,
  evaluator-optimizer, "simplest solution possible"), but older.
- **2023 planning papers.** ReWOO and Plan-and-Solve report numbers from GPT-3/3.5-era models.

## Method and limitations

- **Workers.** Three researcher subagents ran in parallel (Sonnet): GitHub repos, Anthropic
  sources, and papers/practitioners. Their briefs are in [brief.md](brief.md) and their full
  notes in [notes/](notes/).
- **Verification.** I then re-fetched the Anthropic pages and docs as raw text and checked every
  number and quotation marked ✓. I also took repo last-commit dates from shallow clones
  (`git log -1`) and checked LangChain's figures in its README.
- **Network block (main limitation).** This environment's policy blocked arxiv.org,
  cognition.com, openai.com, trychroma.com, research.google, huggingface.co, martinfowler.com and
  blog.langchain.com. So every non-Anthropic paper and essay above is ⚠: taken from search-engine
  snippets, never opened.
  - The direction of those findings is consistent across several snippets and with the Anthropic
    material.
  - The exact numbers (+80.8%, −70%, 17.2x/4.4x, MAST rates and interventions) must be confirmed
    before you rely on them.
  - Several 2026 arXiv IDs came from snippets and are unconfirmed.
  - To close this gap, allow those hosts in the environment's network settings and re-run the
    verification step on the ⚠ items.
- **Star counts** come from the repo pages as fetched on 2026-10-31. The GitHub API was not
  available.
- **No measured evidence on brief quality.** No source measured brief formats directly, and no
  repo publishes an eval of its research quality. Treat everything about templates as
  well-sourced opinion.

## Open questions

- Does a fresh-context claim verifier measurably reduce errors in *this* toolkit's reports?
  Building a 20-query eval set from real runs would answer it.
- What are the right tier budgets for 2026 models, which delegate and verify more readily than
  the 2025 models Anthropic's numbers come from?
- Do the Google/MIT and Tran & Kiela results hold for open-web research rather than QA and
  planning benchmarks?
