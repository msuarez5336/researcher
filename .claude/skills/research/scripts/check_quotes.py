#!/usr/bin/env python3
"""Check that every quote in an evidence file appears verbatim in its cached source page.

Deterministic check, no model judgement: a quote passes only if, after normalising
whitespace, case, quote marks and dashes, it is a substring of the page that
fetch_page.py cached for its URL. Standard library only.

Usage:
  python3 check_quotes.py --run-dir research/2026-10-31-topic [EVIDENCE.jsonl ...]

Defaults to every RUN/evidence/*.jsonl. Each evidence line is a JSON object with at
least: id, claim, quote, url. Optional: page (path to a cached file, used instead of
the index lookup).

Exit code 0 when every item passes, 1 otherwise. Prints one line per failure and a
summary; --json prints the full result list.
"""
import argparse
import glob
import json
import os
import re
import sys

REQUIRED = ("id", "claim", "quote", "url")
MAX_QUOTE_WORDS = 60


def norm(s: str) -> str:
    s = s.lower()
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[‐-―−]", "-", s)
    s = s.replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def load_index(run_dir: str) -> dict:
    path = os.path.join(run_dir, "pages", "index.jsonl")
    index = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    if rec.get("file"):
                        index[rec["url"]] = rec["file"]
    return index


def check_item(item: dict, index: dict, page_cache: dict) -> tuple[str, str]:
    missing = [k for k in REQUIRED if not item.get(k)]
    if missing:
        return "lint", f"missing fields: {', '.join(missing)}"
    quote = item["quote"]
    if "..." in quote or "…" in quote:
        return "lint", "quote joins passages with an ellipsis; split it into two items"
    if len(quote.split()) > MAX_QUOTE_WORDS:
        return "lint", f"quote longer than {MAX_QUOTE_WORDS} words"
    page = item.get("page") or index.get(item["url"])
    if not page or not os.path.exists(page):
        return "no_page", "source not cached; run fetch_page.py on the URL"
    if page not in page_cache:
        with open(page, encoding="utf-8", errors="replace") as f:
            page_cache[page] = norm(f.read())
    if norm(quote) in page_cache[page]:
        return "ok", ""
    return "not_found", "quote not found verbatim in the cached page"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("files", nargs="*")
    args = ap.parse_args()

    files = args.files or sorted(glob.glob(os.path.join(args.run_dir, "evidence", "*.jsonl")))
    if not files:
        print("no evidence files found", file=sys.stderr)
        return 1
    index = load_index(args.run_dir)
    page_cache: dict = {}
    results = []
    for path in files:
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError as e:
                    results.append({"file": path, "line": n, "id": None, "status": "lint", "detail": f"bad JSON: {e}"})
                    continue
                status, detail = check_item(item, index, page_cache)
                results.append({"file": path, "line": n, "id": item.get("id"), "status": status, "detail": detail})

    counts: dict = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    if args.json:
        print(json.dumps({"counts": counts, "results": results}, indent=1))
    else:
        for r in results:
            if r["status"] != "ok":
                print(f"{r['status']:<10} {r['id']}  {r['file']}:{r['line']}  {r['detail']}")
        print("summary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    return 0 if counts.get("ok", 0) == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
