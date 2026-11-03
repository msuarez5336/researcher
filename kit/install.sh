#!/usr/bin/env bash
# Install the token-lean kit for Claude Code: the /codify skill, the haiku-runner subagent,
# the claude-run script, the token rules and the trim-output hook.
#
#   ./install.sh                     personal: ~/.claude, so it works in every folder
#   ./install.sh --project DIR       one project: DIR/.claude and DIR/CLAUDE.md
#   ./install.sh --no-hook           install without the trim-output hook (or remove it)
#   ./install.sh --uninstall         remove the personal install
#   ./install.sh --uninstall --project DIR
#
# Works from the researcher repo (kit/install.sh) or from the standalone token-lean-kit folder.
# Safe to re-run: files are replaced with this version, and the token-rules block in CLAUDE.md
# is replaced, not duplicated. Your other CLAUDE.md content is left alone. The hook is added to
# settings.json next to your own settings; a backup (settings.json.bak) is written first.
# Needs: bash, python3. claude-run also needs jq and the claude CLI.
set -euo pipefail

HERE=$(cd "$(dirname "$0")" && pwd)
if [ -d "$HERE/skills/codify" ]; then          # standalone folder
  SKILL_SRC="$HERE/skills/codify"; AGENT_SRC="$HERE/agents/haiku-runner.md"
else                                            # researcher repo
  SKILL_SRC="$HERE/../.claude/skills/codify"; AGENT_SRC="$HERE/../.claude/agents/haiku-runner.md"
fi
RULES_SRC="$HERE/token-rules.md"
HOOK_SRC="$HERE/hooks/trim-output.py"

usage() { sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
UNINSTALL=0 PROJ="" HOOK=1
while [ $# -gt 0 ]; do
  case $1 in
    --uninstall) UNINSTALL=1 ;;
    --no-hook) HOOK=0 ;;
    --project) [ -n "${2:-}" ] || usage; PROJ=$(cd "$2" && pwd); shift ;;
    -h|--help) usage ;;
    *) echo "unknown option: $1" >&2; usage ;;
  esac
  shift
done
if [ -n "$PROJ" ]; then
  DEST="$PROJ/.claude"; CLAUDE_MD="$PROJ/CLAUDE.md"
  HOOK_CMD='python3 "${CLAUDE_PROJECT_DIR}/.claude/hooks/token-kit-trim-output.py"'
else
  DEST="$HOME/.claude"; CLAUDE_MD="$DEST/CLAUDE.md"
  HOOK_CMD='python3 "$HOME/.claude/hooks/token-kit-trim-output.py"'
fi
SETTINGS="$DEST/settings.json"

command -v python3 >/dev/null || { echo "install: python3 is required" >&2; exit 1; }

# Replace, append or (with "remove") strip the token-rules block in CLAUDE.md.
rules_block() {
  python3 - "$CLAUDE_MD" "$RULES_SRC" "$1" <<'PY'
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
PY
}

# Add ("install") or remove the trim-output hook in settings.json, leaving every other setting
# alone. The kit's entry is recognised by the file name token-kit-trim-output.py.
hook_entry() {
  python3 - "$SETTINGS" "$1" "$HOOK_CMD" <<'PY'
import json, os, shutil, sys
path, mode, cmd = sys.argv[1:4]
data = {}
if os.path.exists(path):
    raw = open(path).read()
    try:
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        sys.exit(f"install: {path} is not valid JSON; fix it, or re-run with --no-hook")
    shutil.copyfile(path, path + ".bak")
hooks = data.setdefault("hooks", {})
post = hooks.setdefault("PostToolUse", [])
mine = lambda h: "token-kit-trim-output.py" in str(h.get("command", ""))
for group in post:
    group["hooks"] = [h for h in group.get("hooks", []) if not mine(h)]
post[:] = [g for g in post if g.get("hooks")]
if mode == "install":
    post.append({"matcher": "Bash|mcp__.*", "hooks": [{"type": "command", "command": cmd}]})
if not post:
    hooks.pop("PostToolUse")
if not hooks:
    data.pop("hooks")
if data or os.path.exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
PY
}

if [ "$UNINSTALL" = 1 ]; then
  [ "$SKILL_SRC" -ef "$DEST/skills/codify" ] && { echo "install: refusing to uninstall the kit's own source" >&2; exit 1; }
  rm -rf "$DEST/skills/codify" "$DEST/agents/haiku-runner.md" "$DEST/hooks/token-kit-trim-output.py"
  [ -f "$CLAUDE_MD" ] && rules_block remove
  [ -f "$SETTINGS" ] && hook_entry remove
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

if [ "$HOOK" = 1 ]; then
  mkdir -p "$DEST/hooks"
  cp "$HOOK_SRC" "$DEST/hooks/token-kit-trim-output.py"
  hook_entry install
  HOOK_MSG="trim-output hook registered in $SETTINGS"
else
  rm -f "$DEST/hooks/token-kit-trim-output.py"
  [ -f "$SETTINGS" ] && hook_entry remove
  HOOK_MSG="no hook"
fi

if [ -n "$PROJ" ] && [ ! -f "$PROJ/scripts/INDEX.md" ]; then
  mkdir -p "$PROJ/scripts"
  printf '# Scripts index\n| Script | What it does | Example | Skill |\n|---|---|---|---|\n' > "$PROJ/scripts/INDEX.md"
fi

echo "Installed into $DEST; token rules in $CLAUDE_MD; $HOOK_MSG."
if [ -z "$PROJ" ]; then
  mkdir -p "$HOME/.local/bin"
  ln -sf "$DEST/skills/codify/bin/claude-run" "$HOME/.local/bin/claude-run"
  case ":$PATH:" in *":$HOME/.local/bin:"*) ;; *) echo "Add ~/.local/bin to your PATH to use claude-run." ;; esac
fi
for t in jq claude; do command -v $t >/dev/null || echo "Note: $t not found; claude-run needs it."; done
