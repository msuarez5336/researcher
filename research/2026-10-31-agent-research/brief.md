# Research brief: how Claude should research and plan for delegation

*This run came before the toolkit existed, so the brief was written in chat, approved there, and
recorded here afterwards. It is a worked example of `templates/research-brief.md`.*

| Field | Value |
|---|---|
| Date (as-of) | 2026-10-31 |
| Requested by / for | Repo owner, to build their own Claude Code research setup |
| Run folder | `research/2026-10-31-agent-research/` |
| Tier | DEEP |
| Budget | 3 workers (Sonnet) × ~40 tool calls; verification by the orchestrator |

## 1. The decision this research feeds
Which patterns, templates and agent/skill definitions should go into a reusable Claude Code
toolkit for research and for delegating work to other agents. The toolkit is this repo.

## 2. Question and query type
- **Main question:** What are current best practices for (1) agent research (search strategy,
  source evaluation, stopping, synthesis) and (2) turning research into plans and briefs that
  other agents can run without extra context?
- **Query type:** breadth-first. Three independent source types with different triage rules.

## 3. Sub-questions (one worker each, all parallel)
| ID | Sub-question | Worker |
|---|---|---|
| A | What do high-signal GitHub setups (agents, skills, commands, CLAUDE.md, spec workflows) actually contain, and how are they packaged for reuse? | researcher (Sonnet) |
| B | What has Anthropic published on research, decomposition, briefs, context, verification, plus current config syntax? | researcher (Sonnet) |
| C | What do papers, other labs and practitioners measure or argue, including dissent? | researcher (Sonnet) |

- **Completeness test:** the six questions (research process, brief contents,
  parallel vs sequential, context, failure modes, verification) each map to at least two workers.
- **Overlap test:** separated by source type. Each brief names the other two workers' scopes.

## 4. Standing rules (sent with every brief)
```text
- Today is 2026-10-31. Prefer 2025–2026 material. Flag anything that looks outdated: pre-Claude-5 model
  names (Claude 3.x/4.x) used as current, the Claude Code "Task" tool (now called "Agent"), deprecated
  APIs/features. Older material is fine if it's foundational, but mark it [OLDER] with its date.
- Cite the original source with a URL for every claim. If you learned it from a listicle, summary or
  awesome-list, follow the link to the original and cite that. If you can't reach the original, mark the
  claim [UNVERIFIED].
- Tag each finding [EVIDENCE] (measured result, eval, documented production outcome, with the number
  and what it was measured on) or [OPINION] (recommendation, experience, assertion).
- When sources disagree, record both positions and the conditions each one applies under.
- Skip SEO filler, AI-generated roundups and vendor marketing that has no specifics.
- Write your full notes to the file path given below as markdown. Your final reply should be only:
  (1) the path, (2) a summary of ≤400 words containing your 5–8 strongest findings, (3) gaps you couldn't
  close. The full detail goes in the file, not the reply.
- Stop when you hit the stopping criteria in your brief or about 40 tool calls, whichever comes first.
  Don't keep searching once new sources are only repeating what you already have.
```

## 5. Worker briefs (as sent, shortened only where marked)

### Brief A: GitHub ecosystem
```text
OBJECTIVE
Find and evaluate the most useful public GitHub repos that show how people set up Claude Code (and
similar agents) to (1) research topics and (2) plan and delegate work to subagents. The output feeds a
curated sources table, ready-to-use templates, and a reusable research-toolkit repo, so concrete file
contents and repo structure matter more than descriptions.

WHY
The user is building a repo they will reuse for all future research with Claude Code. A separate agent
is covering Anthropic's own blog/docs, and another is covering academic papers; don't duplicate them.
Anthropic's GitHub repos ARE in scope for you, as code.

WHAT TO LOOK FOR
.claude/agents/*.md (researcher, planner, orchestrator, reviewer, verifier roles); SKILL.md skills about
research/planning/specs/delegation; .claude/commands/*.md; CLAUDE.md files with delegation or planning
rules; spec- or plan-driven workflows; multi-agent orchestration repos on Claude Code or the Agent SDK;
awesome lists (follow through to the repos). PACKAGING FOR REUSE: directory layout, install steps,
plugin manifests, per-run output folders, shipped permissions and hooks.

HOW
Web search for candidates; read repo pages and raw files with WebFetch. Do NOT use the mcp__github__
tools. Use stars, recent commits and real use as signals, not stars alone.

FOR EACH REPO RECORD
URL | stars | last commit date | what it contains (name the files) | patterns (quote key lines, ≤15 each) |
packaging | why it matters | red flags.

STOPPING CRITERIA
~20 candidates screened, 8–12 read in depth, ≥5 agent/skill files quoted. Stop sooner if repos reuse the
same few templates; say which.

OUTPUT FILE  notes-A-github.md: ranked table · pattern catalogue · packaging patterns · anti-patterns · gaps
```

### Brief B: Anthropic primary sources
```text
OBJECTIVE
Pull together what Anthropic has published (engineering blog, docs, cookbooks, talks) about how agents
should research and how orchestrators should decompose work, write briefs, manage context and combine
results. Exact guidance and exact numbers, verified against the original page.

WHY
The most authoritative sources for Claude's behaviour; they anchor the report, templates and toolkit.
Other agents cover community repos and non-Anthropic papers.

STARTING POINTS (verify each; from memory)
Multi-agent research system post (2025); Building effective agents (Dec 2024, OLDER); Effective context
engineering (2025); posts on tools, Agent Skills, long-running harnesses, Claude Code best practices;
Claude Code docs (subagents, skills, commands, memory, plan mode, hooks); Agent SDK subagents; the
cookbook research prompts; prompt-engineering docs. Sweep the blog index for 2026 additions.

WHAT TO EXTRACT (by question, not by source)
1 research process · 2 delegation briefs · 3 decomposition · 4 context · 5 failure modes ·
6 verification. Plus a CURRENT CONFIG SYNTAX REFERENCE (subagent and SKILL.md frontmatter, command
arguments, commands/skills merger, plugin format, settings.json permissions, CLAUDE.md imports, hooks).

STOPPING CRITERIA  All starting points checked plus an index sweep; every number quoted from the page.
OUTPUT FILE  notes-B-anthropic.md
```

### Brief C: Papers, practitioners and dissent
```text
OBJECTIVE
Find the best non-Anthropic evidence and practitioner experience on (1) how LLM agents should research
and (2) how orchestrators should plan, decompose and delegate, including credible arguments AGAINST
multi-agent delegation.

WHY
The report must separate measured results from opinion and present tradeoffs fairly.

LEADS (verify)
Cognition "Don't build multi-agents" and follow-ups; MAST failure taxonomy; deep-research systems
(OpenAI, Google, LangChain open_deep_research, STORM); plan-and-solve, ReWOO and successors; context
rot measurements; BrowseComp, GAIA, DeepResearch Bench; spec-driven development and brief-writing posts.

STOPPING CRITERIA  10–15 sources in depth, ≥5 with measured results, ≥2 substantive dissents.
OUTPUT FILE  notes-C-papers.md
```

## 6. What happened (for the record)
- All three workers finished, using 69, 54 and 32 tool calls.
- **Worker C was blocked:** the environment's network policy denied arxiv.org, cognition.com,
  openai.com, trychroma.com, research.google, huggingface.co and martinfowler.com. Its findings
  come from search snippets only and are marked ⚠ in the report. The user was told mid-run.
- **The orchestrator re-verified B's summary-sourced numbers** against raw page text. It also
  took repo last-commit dates from shallow clones, because the GitHub API was not available.

## Approval
- [x] User approved in chat on 2026-10-31, asking for Sonnet subagents and a reusable repo as the
  final deliverable.
