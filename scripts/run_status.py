#!/usr/bin/env python3
"""run_status: one-screen status of a research run folder, with no model needed.

Usage:
  python3 scripts/run_status.py research/<YYYY-MM-DD>-<slug> [--quotes]

Prints: which deliverables exist, evidence counts per sub-question (grade, verified,
evidence/opinion), cached pages by status, and claim-verifier verdict counts.
--quotes also runs check_quotes.py and prints its summary line.
Exit codes: 0 = printed (gaps are reported, not errors), 1 = not a run folder.
Standard library only.
"""
import argparse
import collections
import glob
import json
import os
import subprocess
import sys

DELIVERABLES = ["brief.md", "report.md", "sources.md"]


def jsonl(path):
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    yield {"_bad_line": n}


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("run_dir")
    p.add_argument("--quotes", action="store_true", help="also run check_quotes.py")
    a = p.parse_args()
    run = a.run_dir.rstrip("/")
    if not os.path.isdir(run):
        print(f"ERROR: {run} is not a directory", file=sys.stderr)
        return 1

    have = [d for d in DELIVERABLES if os.path.isfile(os.path.join(run, d))]
    missing = [d for d in DELIVERABLES if d not in have]
    notes = sorted(os.path.basename(x) for x in glob.glob(os.path.join(run, "notes", "*.md")))
    print(f"run: {run}")
    print(f"files: {', '.join(have) or 'none'}" + (f" | missing: {', '.join(missing)}" if missing else ""))
    print(f"notes: {', '.join(notes) or 'none'}")

    print("evidence: sq | items | A/B/C | verified | evidence/opinion")
    total = 0
    for f in sorted(glob.glob(os.path.join(run, "evidence", "*.jsonl"))):
        items = list(jsonl(f))
        bad = sum(1 for i in items if "_bad_line" in i)
        items = [i for i in items if "_bad_line" not in i]
        g = collections.Counter(i.get("grade", "?") for i in items)
        v = sum(1 for i in items if i.get("verified") is True)
        k = collections.Counter(i.get("kind", "?") for i in items)
        total += len(items)
        line = (f"  {os.path.basename(f)[:-6]} | {len(items)} | {g['A']}/{g['B']}/{g['C']} | "
                f"{v}/{len(items)} | {k['evidence']}/{k['opinion']}")
        print(line + (f" | {bad} unparseable line(s)" if bad else ""))
    print(f"  total | {total}")

    idx = os.path.join(run, "pages", "index.jsonl")
    if os.path.isfile(idx):
        latest = {}
        for r in jsonl(idx):
            if "url" in r:
                latest[r["url"]] = r.get("status", "?")
        st = collections.Counter(latest.values())
        print("pages: " + ", ".join(f"{s}={n}" for s, n in sorted(st.items())))
        for url, s in latest.items():
            if s != "ok":
                print(f"  {s}: {url}")
    else:
        print("pages: no cache")

    verdicts = collections.Counter()
    for f in glob.glob(os.path.join(run, "verdicts", "*.json")):
        try:
            for v in json.load(open(f, encoding="utf-8")):
                verdicts[v.get("verdict", "?")] += 1
        except (json.JSONDecodeError, TypeError):
            verdicts["unparseable-file"] += 1
    batches = len(glob.glob(os.path.join(run, "claims", "*.json")))
    print(f"claims: {batches} batch(es) | verdicts: "
          + (", ".join(f"{k}={n}" for k, n in sorted(verdicts.items())) or "none"))

    if a.quotes:
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                              ".claude", "skills", "research", "scripts", "check_quotes.py")
        r = subprocess.run([sys.executable, script, "--run-dir", run], capture_output=True, text=True)
        lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
        print("quotes: " + (lines[-1] if lines else "no output"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
