#!/usr/bin/env python3
"""code_mode_bench: measure "compute, don't read" and the trim-output hook on your own machine.

Builds a throwaway project, then runs real `claude -p` calls and records, per run: turns,
input and output tokens (from modelUsage), the CLI's cost estimate, and whether the answer was
right. Four runs per repetition:

  aggregate/direct  read 20 JSON sales files with Read/Glob only, then answer
  aggregate/code    write and run a Python script that computes the answer
  biglog/no-hook    `cat` a 20,000-line log and count ERROR lines
  biglog/hook       the same, with the kit's trim-output hook active (via --settings)

Usage:
  python3 code_mode_bench.py [--model sonnet] [--reps 1] [--out results.jsonl] [--keep]

Costs real tokens: about $0.1-$1 per repetition on Sonnet, depending on the model.
Needs: the claude CLI, logged in. Standard library only.
"""
import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.normpath(os.path.join(HERE, "..", "hooks", "trim-output.py"))
REGIONS = ["North", "South", "East", "West", "Central"]


def build(workdir):
    rng = random.Random(42)
    os.makedirs(os.path.join(workdir, "data"))
    totals = {r: 0.0 for r in REGIONS}
    for f in range(20):
        rows = []
        for i in range(100):
            r = rng.choice(REGIONS)
            units, price = rng.randint(1, 20), round(rng.uniform(5, 200), 2)
            totals[r] += units * price
            rows.append({"id": f * 100 + i, "region": r, "product": f"SKU-{rng.randint(1000, 9999)}",
                         "units": units, "unit_price": price})
        with open(os.path.join(workdir, "data", f"sales_{f:02d}.json"), "w") as fh:
            json.dump(rows, fh)
    best = max(totals, key=totals.get)
    errors = 0
    os.makedirs(os.path.join(workdir, "logs"))
    with open(os.path.join(workdir, "logs", "app.log"), "w") as fh:
        for i in range(20000):
            lvl = "ERROR" if rng.random() < 0.013 else rng.choice(["INFO", "DEBUG", "WARN"])
            errors += lvl == "ERROR"
            fh.write(f"2026-11-03T12:{i // 600 % 60:02d}:{i % 60:02d} {lvl} worker-{i % 7} request {i} done\n")
    with open(os.path.join(workdir, "hook-settings.json"), "w") as fh:
        json.dump({"hooks": {"PostToolUse": [{"matcher": "Bash|mcp__.*", "hooks": [
            {"type": "command", "command": f'python3 "{HOOK}"'}]}]}}, fh)
    return {"aggregate": (best, round(totals[best], 2)), "biglog": errors}


def check(task, truth, answer):
    text = (answer or "").replace(",", "")
    if task == "aggregate":
        region, total = truth
        nums = [float(t) for t in text.replace("$", " ").split() if t.replace(".", "", 1).isdigit()]
        return region.lower() in text.lower() and any(abs(n - total) <= 0.05 for n in nums)
    return str(truth) in text.split() or text.strip() == str(truth)


RUNS = [
    ("aggregate", "direct",
     "Using only the Read and Glob tools (do not write or run any scripts), find which region has the "
     "highest total revenue (units * unit_price) across all files in data/. "
     "Reply with only: REGION TOTAL (total rounded to 2 decimals).",
     ["Read", "Glob"], None),
    ("aggregate", "code",
     "Write and run a short Python script that finds which region has the highest total revenue "
     "(units * unit_price) across all files in data/, printing only the answer. "
     "Reply with only: REGION TOTAL (total rounded to 2 decimals).",
     ["Write", "Bash(python3 *)"], None),
    ("biglog", "no-hook",
     "Run `cat logs/app.log` to look at the log, then tell me how many lines have level ERROR. "
     "Reply with only the number.",
     ["Bash(cat *)", "Bash(grep *)", "Bash(wc *)", "Read"], None),
    ("biglog", "hook",
     "Run `cat logs/app.log` to look at the log, then tell me how many lines have level ERROR. "
     "Reply with only the number.",
     ["Bash(cat *)", "Bash(grep *)", "Bash(wc *)", "Read"], "hook-settings.json"),
]


def run_one(workdir, model, prompt, tools, settings):
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json",
           "--permission-mode", "dontAsk", "--max-turns", "40", "--allowedTools", *tools]
    if settings:
        cmd += ["--settings", os.path.join(workdir, settings)]
    t0 = time.time()
    p = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    secs = round(time.time() - t0, 1)
    try:
        out = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"error": (p.stderr or p.stdout)[-300:], "secs": secs}
    mu = list((out.get("modelUsage") or {}).values())
    s = lambda k: sum(m.get(k, 0) or 0 for m in mu)
    return {"turns": out.get("num_turns"), "secs": secs,
            "tokens_in": s("inputTokens") + s("cacheReadInputTokens") + s("cacheCreationInputTokens"),
            "tokens_out": s("outputTokens"), "cost_usd": out.get("total_cost_usd"),
            "denials": len(out.get("permission_denials") or []), "answer": (out.get("result") or "").strip()[:80],
            "is_error": out.get("is_error")}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--out", default="code_mode_bench_results.jsonl")
    ap.add_argument("--keep", action="store_true", help="keep the throwaway project")
    a = ap.parse_args()
    if not shutil.which("claude"):
        sys.exit("claude CLI not found")
    workdir = tempfile.mkdtemp(prefix="code-mode-bench-")
    truth = build(workdir)
    rows = []
    for rep in range(a.reps):
        for task, variant, prompt, tools, settings in RUNS:
            r = run_one(workdir, a.model, prompt, tools, settings)
            r.update(task=task, variant=variant, rep=rep, model=a.model,
                     correct=check(task, truth[task], r.get("answer")) if "answer" in r else False)
            rows.append(r)
            with open(a.out, "a") as fh:
                fh.write(json.dumps(r) + "\n")
            print(f"{task:9} {variant:8} turns={r.get('turns')} in={r.get('tokens_in')} out={r.get('tokens_out')} "
                  f"cost=${r.get('cost_usd')} correct={r['correct']} denials={r.get('denials')} {r.get('secs')}s",
                  flush=True)
    print(f"\ntruth: {truth}\nresults appended to {a.out}")
    if not a.keep:
        shutil.rmtree(workdir, ignore_errors=True)
    else:
        print(f"project kept at {workdir}")


if __name__ == "__main__":
    main()
