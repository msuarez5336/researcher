#!/usr/bin/env python3
"""Create a prospect folder from prospects/_template.

Usage (from the repo root):
  python3 scripts/new_prospect.py "Acme Corp" [--website acme.com]

Creates prospects/acme-corp/ with prospect.md (client name filled in), an empty context/
folder and the research/ subfolders. Refuses to overwrite an existing prospect.
"""
import argparse
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("name", help="client name, e.g. \"Acme Corp\"")
    ap.add_argument("--website", default="")
    a = ap.parse_args()

    slug = slugify(a.name)
    if not slug or slug.startswith("_"):
        print("ERROR: could not make a folder name from that client name", file=sys.stderr)
        return 1
    src = os.path.join(ROOT, "prospects", "_template")
    dst = os.path.join(ROOT, "prospects", slug)
    if os.path.exists(dst):
        print(f"ERROR: prospects/{slug} already exists", file=sys.stderr)
        return 1
    shutil.copytree(src, dst)
    for sub in ("evidence", "notes", "claims", "verdicts"):
        os.makedirs(os.path.join(dst, "research", sub), exist_ok=True)

    path = os.path.join(dst, "prospect.md")
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = text.replace("<CLIENT_NAME>", a.name)
    if a.website:
        text = text.replace("<client.com>", a.website)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"created prospects/{slug}/")
    print(f"next: edit prospects/{slug}/prospect.md, put emails in prospects/{slug}/context/, "
          f"then run /prospect {slug}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
