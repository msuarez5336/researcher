#!/usr/bin/env bash
# Install the token-lean kit: the /codify skill, the haiku-runner subagent, the claude-run
# script and the token rules.
#
#   kit/install.sh               personal install into ~/.claude (every project you open)
#   kit/install.sh --project DIR install into DIR/.claude and DIR/CLAUDE.md (commit it to share)
#
# Safe to re-run: files are overwritten with the current version and the token-rules block in
# CLAUDE.md is replaced, not duplicated.
set -euo pipefail

SRC=$(cd "$(dirname "$0")/.." && pwd)
if [ "${1:-}" = "--project" ]; then
  [ -n "${2:-}" ] || { echo "usage: $0 [--project DIR]" >&2; exit 2; }
  PROJ=$(cd "$2" && pwd); DEST="$PROJ/.claude"; CLAUDE_MD="$PROJ/CLAUDE.md"
else
  PROJ=""; DEST="$HOME/.claude"; CLAUDE_MD="$DEST/CLAUDE.md"
fi

mkdir -p "$DEST/skills" "$DEST/agents"
if [ "$SRC/.claude" != "$DEST" ]; then
  rm -rf "$DEST/skills/codify"
  cp -R "$SRC/.claude/skills/codify" "$DEST/skills/codify"
  cp "$SRC/.claude/agents/haiku-runner.md" "$DEST/agents/haiku-runner.md"
fi
chmod +x "$DEST/skills/codify/bin/claude-run"

# Replace (or append) the token-rules block in CLAUDE.md.
touch "$CLAUDE_MD"
python3 - "$CLAUDE_MD" "$SRC/kit/token-rules.md" <<'EOF'
import re, sys
path, block = sys.argv[1], open(sys.argv[2]).read().strip() + "\n"
text = open(path).read()
pat = re.compile(r"<!-- token-rules:start.*?<!-- token-rules:end -->\n?", re.S)
text = pat.sub(lambda m: block, text) if pat.search(text) else text.rstrip("\n") + ("\n\n" if text.strip() else "") + block
open(path, "w").write(text)
EOF

if [ -n "$PROJ" ] && [ ! -f "$PROJ/scripts/INDEX.md" ]; then
  mkdir -p "$PROJ/scripts"
  printf '# Scripts index\n| Script | What it does | Example | Skill |\n|---|---|---|---|\n' > "$PROJ/scripts/INDEX.md"
fi

if [ -z "$PROJ" ]; then
  mkdir -p "$HOME/.local/bin"
  ln -sf "$DEST/skills/codify/bin/claude-run" "$HOME/.local/bin/claude-run"
  echo "Linked claude-run into ~/.local/bin (make sure it is on your PATH)."
fi
echo "Installed into $DEST; token rules in $CLAUDE_MD."
