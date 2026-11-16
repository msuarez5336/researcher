---
name: new-prospect
description: Create the folder for a new client prospect from the template. Use for "new prospect", "add a client", "set up <company>".
argument-hint: <client name> [website]
---

# New prospect

Request: $ARGUMENTS

1. Take the client name from the request, and the website if one is given. If there is no
   name, ask for it.
2. Run `python3 scripts/new_prospect.py "<client name>"`, adding `--website <domain>` if given.
   If it reports that the folder exists, say so and stop: don't overwrite a prospect.
3. If `about-us.md` still contains `<OUR_COMPANY>`, or `services/` holds only `_template.md`,
   say that these need filling in first, because every run reads them.
4. Tell the user in at most five lines: the folder created, the lines to fill in
   `prospect.md` (services to pitch must match file names in `services/`), that emails go in
   `context/`, and the command to run next (`/prospect <slug>`).

Do no research here.
