# SQ2 notes (as of 2026-10-31)

## Answer
Custom slash commands have been merged into skills: .claude/commands/x.md and .claude/skills/x/SKILL.md both create /x; old command files still work (SQ2-1, SQ2-3). Arguments are passed as text after /name and substituted via $ARGUMENTS, $ARGUMENTS[N]/$N, or named $name from an `arguments:` frontmatter list. Every run can start with the same settings via settings.json files (managed > --settings > .claude/settings.local.json > .claude/settings.json > ~/.claude/settings.json) and CLAUDE.md files, which `claude -p` also loads (SQ2-16, SQ2-23).

## Findings
- [E] Merge: docs say commands merged into skills, old files keep working (SQ2-1). Changelog lists "Merged slash commands and skills" under 2.1.3 (SQ2-2); the release date is not in the cached text.
- [O] Docs recommend skills for new work; command files lack name/paths frontmatter (SQ2-3).
- [E] Arguments: $ARGUMENTS (SQ2-4), $ARGUMENTS[N] / $N 0-based (SQ2-5), named via `arguments:` (SQ2-6), `argument-hint` for autocomplete (SQ2-7), shell-style quoting (SQ2-8), unmatched placeholder behaviour (SQ2-9).
- [E] Non-interactive: with `claude -p "/skill args"` only the first skill loads and the rest is its arguments (SQ2-10). Project skill allowed-tools applies even in an untrusted folder under -p (SQ2-12).
- [E] Per-command behaviour: allowed-tools pre-approves for one turn only and does not restrict tools (SQ2-11); model override lasts one turn (SQ2-13); disable-model-invocation (SQ2-14); managed policy can ignore skill allowed-tools (SQ2-15). Subagent files can fix tools/model (SQ2-24).
- [E] Settings scopes and precedence (SQ2-16, SQ2-17); commit .claude/settings.json for shared permissions/hooks (SQ2-18) [O]; env vars are not a settings level (SQ2-19).
- [E] CLAUDE.md: loaded every session as context, not enforced (SQ2-20); locations (SQ2-21); concatenated up the directory tree (SQ2-22). `claude -p` loads these unless --bare (SQ2-23).
- [E, unverified] Known problems: arguments: frontmatter not substituted via the Skill tool (open, v2.1.241) (SQ2-25); $ARGUMENTS broke in v2.1.101 (SQ2-26). Both from a search summary of mirror pages only.

## Minimal example (.claude/skills/fix-issue/SKILL.md)
```
---
description: Fix a GitHub issue by number     # description field: not separately traced (see Not found)
argument-hint: [issue-number]                 # SQ2-7
arguments: [issue]                            # SQ2-6
disable-model-invocation: true                # SQ2-14
allowed-tools: Bash(gh *)                     # SQ2-11 (one-turn pre-approval)
---
Fix GitHub issue $issue following our coding standards.   # $issue: SQ2-6; $ARGUMENTS alternative: SQ2-4
```
Invoke interactively: `/fix-issue 123`. Non-interactively: `claude -p "/fix-issue 123"` (SQ2-10). Same effect from .claude/commands/fix-issue.md minus name (SQ2-1, SQ2-3). Safest form: use plain $ARGUMENTS given SQ2-25/26.

## Conflicts
- Docs show substitution working; issue reports show regressions on the Skill-tool path and positional $N in specific versions (SQ2-25/26, unverified). Typed /command with $ARGUMENTS is reportedly most reliable.
- "allowed-tools" sounds like a restriction; docs say it only pre-approves (SQ2-11).

## Not found
- Release date of v2.1.3 (changelog has version headers only in cached text). Exact doc quote for `description` field and for permissions/hooks keys in settings (not traced). Whether bug issues are fixed in current version.

## Blocked
- github.com not used; issue pages seen only as search snippets via claudeissues.com mirrors (unfetched, verified=false).

## Search log
- Bulk fetch skills/settings/memory/slash-commands pages (search/fetch): 4 sources.
- "Claude Code skill $ARGUMENTS not substituted issue" (disconfirm): 2 usable sources (snippets).
- Fetch changelog, sub-agents: 2 sources.
- Budget used: about 6 of 15 calls.
