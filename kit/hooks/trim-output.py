#!/usr/bin/env python3
"""trim-output: a PostToolUse hook that keeps large tool output out of Claude's context.

When a Bash or MCP result is longer than a threshold, it saves the full output to a file and
hands Claude a head and tail plus the file path, so Claude can grep or slice the file instead
of reading all of it. This is the "compute, don't read" idea applied to tool output.

Docs basis (code.claude.com/docs/en/hooks): PostToolUse `updatedToolOutput` replaces what
Claude sees. For Bash the value must keep the tool's shape (stdout, stderr, interrupted,
isImage), or Claude Code ignores it. The tool has already run; only Claude's view changes.

Settings (environment variables):
  TOKEN_KIT_TRIM_CHARS   trim when output is longer than this (default 8000, about 2k tokens)
  TOKEN_KIT_TRIM_KEEP    characters kept from the head and from the tail (default 1500 each)
  TOKEN_KIT_TRIM_DIR     where full outputs are saved (default: <tmp>/claude-tool-output)
Skip trimming for one command by putting the marker `# no-trim` in it.

Never fails a tool call: on any error it exits 0 with no output, so the original result stands.
Standard library only.
"""
import json
import os
import re
import sys
import tempfile

LIMIT = int(os.environ.get("TOKEN_KIT_TRIM_CHARS", "8000"))
KEEP = int(os.environ.get("TOKEN_KIT_TRIM_KEEP", "1500"))
OUT_DIR = os.environ.get("TOKEN_KIT_TRIM_DIR") or os.path.join(tempfile.gettempdir(), "claude-tool-output")


def save(data, session, tool_use_id, suffix):
    d = os.path.join(OUT_DIR, re.sub(r"[^\w.-]", "_", session or "session"))
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, re.sub(r"[^\w.-]", "_", tool_use_id or "output") + suffix)
    with open(path, "w", encoding="utf-8", errors="replace") as f:
        f.write(data)
    return path


def shorten(text, path):
    lines = text.count("\n") + (0 if text.endswith("\n") else 1)
    head, tail = text[:KEEP], text[-KEEP:]
    note = (f"\n... [token-kit: trimmed {len(text) - 2 * KEEP:,} of {len(text):,} chars, "
            f"{lines:,} lines. Full output: {path} . Query it with rg, grep -c, sed -n, head or "
            f"tail instead of printing it; add '# no-trim' to a command to see it whole.] ...\n")
    return head + note + tail


def main():
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    resp = event.get("tool_response")
    session, tuid = event.get("session_id"), event.get("tool_use_id")
    command = json.dumps(event.get("tool_input", {}))
    if "# no-trim" in command or resp is None:
        return

    if tool == "Bash":
        if not isinstance(resp, dict) or resp.get("isImage"):
            return
        out, err = resp.get("stdout") or "", resp.get("stderr") or ""
        if len(out) + len(err) <= LIMIT:
            return
        new = dict(resp)  # keep every field so the shape still matches
        if len(out) > LIMIT // 2:
            new["stdout"] = shorten(out, save(out, session, tuid, ".stdout.txt"))
        if len(err) > LIMIT // 2:
            new["stderr"] = shorten(err, save(err, session, tuid, ".stderr.txt"))
        if new == resp:
            return
    elif tool.startswith("mcp__"):
        if isinstance(resp, str):
            if len(resp) <= LIMIT:
                return
            new = shorten(resp, save(resp, session, tuid, ".txt"))
        elif isinstance(resp, list) and all(isinstance(b, dict) and b.get("type") == "text" for b in resp):
            text = "\n".join(b.get("text", "") for b in resp)
            if len(text) <= LIMIT:
                return
            new = [{"type": "text", "text": shorten(text, save(text, session, tuid, ".txt"))}]
        else:
            return  # images or mixed blocks: leave alone
    else:
        return

    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedToolOutput": new}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
