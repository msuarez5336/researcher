# Prospect research

A Claude Code setup for researching a client prospect before you pitch. You tell it who the
client is and which of your services you would offer, give it the emails you have exchanged,
and it writes a cited dossier: what the client has told you, what public sources say, how well
each service fits, and what to ask next.

Everything runs locally in this folder. You need [Claude Code](https://code.claude.com/docs)
and Python 3 (standard library only).

## One-time setup
1. Fill in `about-us.md`: who you are, what a good-fit client looks like.
2. Copy `services/_template.md` to one file per service you sell, e.g. `services/audit.md`,
   and fill each in.

## For each prospect
```bash
cd prospect-research
```
```bash
claude
```
The first time, Claude Code asks whether you trust this folder. Accept, so that the
pre-approved commands in `.claude/settings.json` apply.

Then, inside Claude Code:

1. `/new-prospect Acme Corp` creates `prospects/acme-corp/`.
2. Edit `prospects/acme-corp/prospect.md`: website, which services to pitch, the goal.
3. Put your emails with the client in `prospects/acme-corp/context/`. Saved `.eml` or `.mbox`
   files, or text pasted into `.txt` or `.md` files, all work. The folder can stay empty.
4. `/prospect acme-corp` runs the research. It shows a plan first and waits for your OK
   (`/prospect acme-corp --yes` skips the wait).
5. Read `prospects/acme-corp/dossier.md`.
6. When new emails arrive, add them to `context/` and run `/prospect-update acme-corp`.

## What is in a prospect folder
| File | Written by | Content |
|---|---|---|
| `prospect.md` | you | client name, services to pitch, goal |
| `context/` | you | emails and notes; never leaves your machine through git |
| `context-digest.md` | Claude | what the emails tell us, each line tied to a file and date |
| `plan.md` | Claude | which questions are already answered and which get researched |
| `dossier.md` | Claude | the result |
| `sources.md` | Claude | every source, with date and verification status |
| `log.md` | Claude | one line per run |
| `research/` | Claude | evidence, notes and verification output behind the dossier |

## Privacy
- `context/` is in `.gitignore`. If you put this folder on GitHub, your emails are not uploaded.
- The research agents that search the web are given questions, not your emails. See `CLAUDE.md`.
- The dossier and the digest do contain what the client told you. Keep the repo private.

## Layout
```
about-us.md              your company (edit once)
services/                one file per service (edit once, reuse)
prospects/_template/     copied by /new-prospect
prospects/<client>/      one folder per prospect
.claude/skills/          /new-prospect, /prospect, /prospect-update
.claude/agents/          context-reader, researcher, claim-verifier
.claude/settings.json    pre-approves web search and the scripts below
scripts/                 new_prospect.py, emails_to_text.py, fetch_page.py, check_quotes.py, run_status.py
```
`python3 scripts/run_status.py prospects/<client> --quotes` prints a one-screen status of a run.

## Limits
- US prospects: US companies and global companies with a large US presence. The source rules
  in `CLAUDE.md` are US-centred.
- Public sources cover listed companies and federal contractors best. Expect gaps for private
  companies, and expect them to be stated as gaps.
- Notes on privacy law in the dossier are pointers, not legal advice.
- Outlook `.msg` files are not read. Save them as `.eml` or paste the text.
