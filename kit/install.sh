#!/usr/bin/env bash
# Install the token-lean kit for Claude Code: the /codify skill, the haiku-runner subagent,
# the claude-run script and the token rules.
#
#   ./install.sh                     personal: ~/.claude, so it works in every folder
#   ./install.sh --project DIR       one project: DIR/.claude and DIR/CLAUDE.md
#   ./install.sh --uninstall         remove the personal install
#   ./install.sh --uninstall --project DIR
#
# Works from the researcher repo (kit/install.sh) or from the standalone token-lean-kit folder.
# Safe to re-run: files are replaced with this version, and the token-rules block in CLAUDE.md
# is replaced, not duplicated. Your other CLAUDE.md content is left alone.
# Needs: bash, python3. claude-run also needs jq and the claude CLI.
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
if [ -d "$HERE/skills/codify" ]; then          # standalone folder
  SKILL_SRC="$HERE/skills/codify"; AGENT_SRC="$HERE/agents/haiku-runner.md"
else                                            # researcher repo
  SKILL_SRC="$HERE/../.claude/skills/codify"; AGENT_SRC="$HERE/../.claude/agents/haiku-runner.md"
fi
RULES_SRC="$HERE/token-rules.md"

usage() { sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
UNINSTALL=0 PROJ=""
while [ $# -gt 0 ]; do
  case $1 in
    --uninstall) UNINSTALL=1 ;;
    --project) [ -n "${2:-}" ] || usage; PROJ=$(cd "$2" && pwd); shift ;;
    -h|--help) usage ;;
    *) echo "unknown option: $1" >&2; usage ;;
  esac
  shift
done
if [ -n "$PROJ" ]; then DEST="$PROJ/.claude"; CLAUDE_MD="$PROJ/CLAUDE.md"
else DEST="$HOME/.claude"; CLAUDE_MD="$DEST/CLAUDE.md"; fi

command -v python3 >/dev/null || { echo "install: python3 is required" >&2; exit 1; }

# Replace, append or (with "remove") strip the token-rules block in CLAUDE.md.
rules_block() {
  python3 - "$CLAUDE_MD" "$RULES_SRC" "$1" <<'EOF'
import os, re, sys
path, src, mode = sys.argv[1:4]
text = open(path).read() if os.path.exists(path) else ""
pat = re.compile(r"\n*<!-- token-rules:start.*?<!-- token-rules:end -->\n?", re.S)
if mode == "remove":
    text = pat.sub("\n", text).strip("\n")
    text = text + "\n" if text else ""
else:
    block = open(src).read().strip() + "\n"
    if pat.search(text):
        text = pat.sub(lambda m: ("\n\n" if m.start() else "") + block, text, count=1)
    else:
        text = text.rstrip("\n") + ("\n\n" if text.strip() else "") + block
if text or os.path.exists(path):
    open(path, "w").write(text)
EOF
}

if [ "$UNINSTALL" = 1 ]; then
  [ "$SKILL_SRC" -ef "$DEST/skills/codify" ] && { echo "install: refusing to uninstall the kit's own source" >&2; exit 1; }
  rm -rf "$DEST/skills/codify" "$DEST/agents/haiku-runner.md"
  [ -f "$CLAUDE_MD" ] && rules_block remove
  if [ -z "$PROJ" ] && [ -L "$HOME/.local/bin/claude-run" ]; then rm "$HOME/.local/bin/claude-run"; fi
  echo "Removed the kit from $DEST (scripts/INDEX.md and your scripts are kept)."
  exit 0
fi

mkdir -p "$DEST/skills" "$DEST/agents"
if ! [ "$SKILL_SRC" -ef "$DEST/skills/codify" ]; then
  rm -rf "$DEST/skills/codify"
  cp -R "$SKILL_SRC" "$DEST/skills/codify"
  cp "$AGENT_SRC" "$DEST/agents/haiku-runner.md"
fi
chmod +x "$DEST/skills/codify/bin/claude-run"
mkdir -p "$(dirname "$CLAUDE_MD")"
rules_block install

if [ -n "$PROJ" ] && [ ! -f "$PROJ/scripts/INDEX.md" ]; then
  mkdir -p "$PROJ/scripts"
  printf '# Scripts index\n| Script | What it does | Example | Skill |\n|---|---|---|---|\n' > "$PROJ/scripts/INDEX.md"
fi

echo "Installed into $DEST; token rules in $CLAUDE_MD."
if [ -z "$PROJ" ]; then
  mkdir -p "$HOME/.local/bin"
  ln -sf "$DEST/skills/codify/bin/claude-run" "$HOME/.local/bin/claude-run"
  case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) echo "Add ~/.local/bin to your PATH to use claude-run." ;; esac
fi
for t in jq claude; do command -v $t >/dev/null || echo "Note: $t not found; claude-run needs it."; done
