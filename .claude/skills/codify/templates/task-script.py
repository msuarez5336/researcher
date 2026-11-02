#!/usr/bin/env python3
"""<name>: <one line on what it computes>.

Usage:
  python3 scripts/<name>.py <args> [--limit N] [--json]

Output is kept compact on purpose: a model may read it on every run.
Exit codes: 0 = success (including "nothing found"), 1 = real failure.
Standard library only.
"""
import argparse
import json
import sys


def compute(args):
    """Do the deterministic work. Return a list of small dicts (or one dict)."""
    items = []
    # ... fetch / parse / filter / count here ...
    return items


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    # p.add_argument("target", help="...")
    p.add_argument("--limit", type=int, default=20, help="max items to print")
    p.add_argument("--json", action="store_true", help="JSON lines instead of text")
    args = p.parse_args()

    try:
        items = compute(args)
    except Exception as e:  # report and fail; a skill using this script aborts cheaply
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    shown = items[: args.limit]
    for it in shown:
        print(json.dumps(it, ensure_ascii=False) if args.json else " | ".join(map(str, it.values())))
    if not items:
        print("none")
    elif len(items) > len(shown):
        print(f"... {len(items) - len(shown)} more (raise --limit)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
