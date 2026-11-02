#!/usr/bin/env bash
# Build the standalone token-lean-kit folder and zip from this repo.
#
#   kit/package.sh [OUT_DIR]      default OUT_DIR: dist/ (gitignored)
#
# Produces OUT_DIR/token-lean-kit/ and OUT_DIR/token-lean-kit.zip. Unzip anywhere and run
# ./install.sh. The repo stays the single source of truth; this only copies files.
set -euo pipefail

REPO=$(cd "$(dirname "$0")/.." && pwd)
OUT=$(mkdir -p "${1:-$REPO/dist}" && cd "${1:-$REPO/dist}" && pwd)
PKG="$OUT/token-lean-kit"

rm -rf "$PKG" "$PKG.zip"
mkdir -p "$PKG/skills" "$PKG/agents"
cp -R "$REPO/.claude/skills/codify" "$PKG/skills/codify"
cp "$REPO/.claude/agents/haiku-runner.md" "$PKG/agents/"
cp "$REPO/kit/install.sh" "$REPO/kit/token-rules.md" "$REPO/kit/README.md" "$PKG/"
chmod +x "$PKG/install.sh" "$PKG/skills/codify/bin/claude-run"
find "$PKG" -name '__pycache__' -prune -exec rm -rf {} +

python3 - "$OUT" <<'EOF'
import os, sys, zipfile
out = sys.argv[1]
with zipfile.ZipFile(os.path.join(out, "token-lean-kit.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(os.path.join(out, "token-lean-kit")):
        dirs.sort()
        for f in sorted(files):
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, out))  # keeps the executable bits
EOF
echo "Built $PKG and $PKG.zip ($(find "$PKG" -type f | wc -l | tr -d ' ') files)"
