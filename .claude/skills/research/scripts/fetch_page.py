#!/usr/bin/env python3
"""Fetch web pages (or read local files) and cache their plain text in RUN/pages/.

Why: WebFetch returns a model-written summary, so quotes taken from it are often
paraphrased. Quoting from a cached raw copy makes every quote checkable later by
check_quotes.py. Standard library only.

Usage:
  python3 fetch_page.py --run-dir research/2026-10-31-topic URL [URL ...] [--json]

Writes RUN/pages/<host>-<hash>.txt and appends one line per page to
RUN/pages/index.jsonl: {"url", "file", "status", "chars", "fetched_at"}.
status is one of: ok, thin (<800 chars of text), unsupported (not HTML/text),
unreachable (network or HTTP error). A URL already cached as ok is not refetched.
"""
import argparse
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UA = "Mozilla/5.0 (research-toolkit; +https://code.claude.com)"
BLOCK_TAGS = r"</?(p|div|br|li|ul|ol|h[1-6]|tr|td|th|table|section|article|header|footer|pre|blockquote)\b[^>]*>"


def html_to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg)\b.*?</\1>", " ", raw)
    raw = re.sub(r"(?is)<!--.*?-->", " ", raw)
    raw = re.sub(r"(?i)" + BLOCK_TAGS, "\n", raw)
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    lines = [re.sub(r"[ \t\r\f\v]+", " ", ln).strip() for ln in raw.split("\n")]
    text = "\n".join(ln for ln in lines if ln)
    return text


def cache_name(url: str) -> str:
    host = urllib.parse.urlparse(url).netloc or "local"
    host = re.sub(r"[^A-Za-z0-9.-]", "_", host)
    return f"{host}-{hashlib.sha1(url.encode()).hexdigest()[:10]}.txt"


def load_index(path: str) -> dict:
    index = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rec = json.loads(line)
                    index[rec["url"]] = rec
    return index


def fetch(url: str) -> tuple[str, str]:
    """Return (status, text)."""
    if os.path.exists(url):
        with open(url, encoding="utf-8", errors="replace") as f:
            body = f.read()
        text = html_to_text(body) if url.lower().endswith((".html", ".htm")) else body
        return ("ok" if len(text) >= 800 else "thin"), text
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/plain,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            ctype = resp.headers.get("Content-Type", "")
            body = resp.read()
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return "unreachable", f"{type(e).__name__}: {e}"
    if not any(t in ctype for t in ("html", "text", "json", "xml", "markdown")):
        return "unsupported", f"content-type {ctype}"
    charset = re.search(r"charset=([\w-]+)", ctype)
    raw = body.decode(charset.group(1) if charset else "utf-8", errors="replace")
    text = html_to_text(raw) if "html" in ctype else raw
    return ("ok" if len(text) >= 800 else "thin"), text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--json", action="store_true", help="print results as JSON")
    ap.add_argument("urls", nargs="+")
    args = ap.parse_args()

    pages = os.path.join(args.run_dir, "pages")
    os.makedirs(pages, exist_ok=True)
    index_path = os.path.join(pages, "index.jsonl")
    index = load_index(index_path)
    results = []
    for url in args.urls:
        if url in index and index[url]["status"] == "ok":
            results.append({**index[url], "cached": True})
            continue
        status, text = fetch(url)
        name = cache_name(url)
        rec = {
            "url": url,
            "file": os.path.join(pages, name) if status in ("ok", "thin") else None,
            "status": status,
            "chars": len(text) if status in ("ok", "thin") else 0,
            "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        if rec["file"]:
            with open(rec["file"], "w", encoding="utf-8") as f:
                f.write(f"SOURCE: {url}\nFETCHED: {rec['fetched_at']}\n\n{text}\n")
        else:
            rec["error"] = text
        with open(index_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
        results.append(rec)

    if args.json:
        print(json.dumps(results, indent=1))
    else:
        for r in results:
            print(f"{r['status']:<12} {r.get('file') or r.get('error', '')}  {r['url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
