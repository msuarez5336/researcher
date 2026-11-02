# Sources: running Claude Code repeatedly with parameters

*As of 2026-10-31. Ranked by usefulness to the question, not by popularity. The official docs
pages carry no visible publication date. "2026-10-31" is the date they were fetched, and they
reflect Claude Code v2.1.3xx-era behaviour (v2.1.302 is the newest version they mention).*

Status: ✓ verified against the cached original · ~ read via summary or snippet only · ✗ unreachable.

## Primary sources (official documentation)
| # | Source | Type | Date | Status | Evidence | Verdict |
|---|---|---|---|---|---|---|
| 1 | [Run Claude Code programmatically (headless)](https://code.claude.com/docs/en/headless) | Official docs | fetched 2026-10-31 | ✓ | SQ1-1–SQ1-12, SQ1-16, SQ1-19, SQ1-21, SQ1-22, SQ2-23, SQ3-11, SQ3-12, LEAD-1 | The core source for scripted runs: input, output, exit codes, permissions, `--bare`. Read it first. |
| 2 | [Skills](https://code.claude.com/docs/en/skills) | Official docs | fetched 2026-10-31 | ✓ | SQ2-1, SQ2-3–SQ2-15 | The authority on argument syntax and frontmatter, and on the commands-into-skills merge. |
| 3 | [CLI reference](https://code.claude.com/docs/en/cli-reference) | Official docs | fetched 2026-10-31 | ✓ | SQ1-13–SQ1-15, SQ1-17, SQ1-18, SQ1-20 | Full flag list; use it to look up exact flag names. |
| 4 | [GitHub Actions](https://code.claude.com/docs/en/github-actions) | Official docs | fetched 2026-10-31 | ✓ | SQ3-4–SQ3-8 | Action modes, `claude_args`, scheduled-run caveats. Used in place of the blocked action README. |
| 5 | [Settings](https://code.claude.com/docs/en/settings) | Official docs | fetched 2026-10-31 | ✓ | SQ2-16–SQ2-19 | Scope precedence; use it when deciding where a fixed setting belongs. |
| 6 | [Scheduled tasks](https://code.claude.com/docs/en/scheduled-tasks) | Official docs | fetched 2026-10-31 | ✓ | SQ3-9, SQ3-10 | Compares cloud, Desktop and `/loop`. |
| 7 | [Agent SDK Python reference](https://platform.claude.com/docs/en/agent-sdk/python) | Official docs | fetched 2026-10-31 | ✓ | SQ3-1, SQ3-2 | `ClaudeAgentOptions` fields. The TypeScript reference was not read. |
| 8 | [Memory / CLAUDE.md](https://code.claude.com/docs/en/memory) | Official docs | fetched 2026-10-31 | ✓ | SQ2-20–SQ2-22 | How CLAUDE.md loads; context, not enforcement. |
| 9 | [Agent SDK structured outputs](https://platform.claude.com/docs/en/agent-sdk/structured-outputs) | Official docs | fetched 2026-10-31 | ✓ | SQ3-3 | `output_format` / `structured_output`. |
| 10 | [Subagents](https://code.claude.com/docs/en/sub-agents) | Official docs | fetched 2026-10-31 | ✓ | SQ2-24 | Only the `tools`/`model` fields were used. |
| 11 | [Changelog](https://code.claude.com/docs/en/changelog) | Official changelog | fetched 2026-10-31 | ✓ | SQ2-2 | Dates the merge to v2.1.3; release date not in the cached text. |
| 12 | [Agent SDK overview](https://platform.claude.com/docs/en/agent-sdk/overview) | Official docs | fetched 2026-10-31 | ✓ (cached, no quotes taken) | none | Orientation only. |

## Repositories
| # | Repo | Stars | Last commit | Status | What it contains | Verdict |
|---|---|---|---|---|---|---|
| 1 | [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | not read | not read | ✗ HTTP 403 to `fetch_page.py`; no clone attempted | The official GitHub Action | Not used. Its behaviour is taken from the official docs page (primary source 4). |

## Secondary and practitioner sources
| # | Source | Author/org | Date | Status | Verdict |
|---|---|---|---|---|---|
| 1 | [Claude Code: dangerously-skip-permissions silent failure](https://wmedia.es/en/tips/claude-code-dangerously-skip-permissions-silent-failure) | Wmedia | 2026-07-31 | ✓ | Grade C, but describes a test it ran (exit 0 despite denials). Consistent with the official `permission_denials` docs. Use it as a warning, not a spec. |
| 2 | claudeissues.com copies of Claude Code GitHub issues on argument substitution | third-party copy of GitHub issues | 2026 | ~ (search snippets only) | Leads only. Not fetched, because the originals are on the blocked github.com. Dropped from evidence. |
| 3 | Third-party CLI reference claiming `--dangerously-skip-permissions` is required to avoid hangs | unknown | unknown | ~ (search snippet only) | Contradicted for v2.1.302+ by primary source 1. Probably describes older versions. |

## Screened and excluded
- [Slash commands](https://code.claude.com/docs/en/slash-commands) and
  [Costs](https://code.claude.com/docs/en/costs): cached; nothing quoted beyond what the skills
  and headless pages already state.
- dev.to and similar tutorial posts surfaced in the pitfall searches: weak, unclear dates, and
  not needed once the official docs covered the behaviour.
