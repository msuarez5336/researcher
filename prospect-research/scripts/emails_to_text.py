#!/usr/bin/env python3
"""Convert saved emails in a prospect's context/ folder into plain text.

Usage (from the repo root):
  python3 scripts/emails_to_text.py prospects/<slug>

Reads every .eml and .mbox file under prospects/<slug>/context/ and writes one text file per
message to prospects/<slug>/context/_text/, named <date>-<subject>.txt, with From, To, Cc,
Date, Subject and the plain-text body. Attachments are listed by name, not extracted.
Files already converted are skipped. Other file types (.txt, .md, .pdf) need no conversion.
Outlook .msg files are not supported: save them as .eml or paste the text into a .txt file.
"""
import argparse
import email
import email.policy
import email.utils
import glob
import html
import mailbox
import os
import re
import sys


def body_text(msg) -> str:
    part = msg.get_body(preferencelist=("plain", "html"))
    if part is None:
        return ""
    try:
        text = part.get_content()
    except (LookupError, UnicodeDecodeError):
        text = (part.get_payload(decode=True) or b"").decode("utf-8", "replace")
    if part.get_content_type() == "text/html":
        text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
        text = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>", "\n", text)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()


def render(msg, source: str) -> tuple[str, str]:
    date = msg.get("Date", "")
    try:
        day = email.utils.parsedate_to_datetime(date).strftime("%Y-%m-%d")
    except (TypeError, ValueError):
        day = "undated"
    subject = str(msg.get("Subject", "") or "no subject")
    attachments = [p.get_filename() for p in msg.iter_attachments() if p.get_filename()]
    lines = [f"Source file: {source}"]
    for h in ("From", "To", "Cc", "Date", "Subject"):
        if msg.get(h):
            lines.append(f"{h}: {msg.get(h)}")
    if attachments:
        lines.append("Attachments (not extracted): " + ", ".join(attachments))
    lines += ["", body_text(msg)]
    slug = re.sub(r"[^a-z0-9]+", "-", subject.lower()).strip("-")[:50] or "no-subject"
    return f"{day}-{slug}", "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("prospect_dir")
    a = ap.parse_args()
    ctx = os.path.join(a.prospect_dir.rstrip("/"), "context")
    if not os.path.isdir(ctx):
        print(f"ERROR: {ctx} is not a directory", file=sys.stderr)
        return 1
    out = os.path.join(ctx, "_text")
    os.makedirs(out, exist_ok=True)
    done_path = os.path.join(out, ".converted")
    done = set(open(done_path, encoding="utf-8").read().split("\n")) if os.path.exists(done_path) else set()

    messages = []  # (key, source name, message)
    for path in sorted(glob.glob(os.path.join(ctx, "**", "*"), recursive=True)):
        rel = os.path.relpath(path, ctx)
        if rel.startswith("_text") or not os.path.isfile(path):
            continue
        low = path.lower()
        if low.endswith(".eml"):
            with open(path, "rb") as f:
                messages.append((rel, rel, email.message_from_binary_file(f, policy=email.policy.default)))
        elif low.endswith(".mbox"):
            box = mailbox.mbox(path, factory=lambda f: email.message_from_binary_file(f, policy=email.policy.default))
            for i, msg in enumerate(box):
                messages.append((f"{rel}#{i}", f"{rel} (message {i + 1})", msg))
        elif low.endswith(".msg"):
            print(f"skipped {rel}: .msg is not supported; save as .eml or paste into a .txt file")

    written = skipped = 0
    for key, source, msg in messages:
        if key in done:
            skipped += 1
            continue
        name, text = render(msg, source)
        target, n = os.path.join(out, name + ".txt"), 1
        while os.path.exists(target):
            n += 1
            target = os.path.join(out, f"{name}-{n}.txt")
        with open(target, "w", encoding="utf-8") as f:
            f.write(text)
        done.add(key)
        written += 1
    with open(done_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(x for x in done if x)))
    print(f"emails: {written} converted, {skipped} already done, output in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
