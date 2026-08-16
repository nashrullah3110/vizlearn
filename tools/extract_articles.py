#!/usr/bin/env python3
"""Seed content/articles/ from the articles currently on the pages.

Run once per page that has no content file yet. Everything a page already
says is preserved verbatim - this only changes where it is stored, so the
long-form rewrite can start from the existing text instead of replacing it.

    python3 tools/extract_articles.py            # only pages with no file
    python3 tools/extract_articles.py --force    # re-seed everything
"""

import os
import re
import sys

import prose
from build_articles import card_inner
from build_lede import article_body, restore, segments
from lib_catalog import ROOT, modules

H2 = re.compile(r"<h2\b[^>]*>(.*?)</h2>", re.S | re.I)
P = re.compile(r"<p\b[^>]*>(.*?)</p>", re.S | re.I)
H3 = re.compile(r"<h3\b([^>]*)>(.*?)</h3>", re.S | re.I)


def card_head(src):
    """(title, intro) from the article card's header."""
    span = card_inner(src)
    if not span:
        return "", ""
    head = src[span[0]:span[0] + 2000]
    h2 = H2.search(head)
    title = prose.heading_text(h2.group(1)) if h2 else ""
    intro = ""
    if h2:
        p = P.search(head, h2.end())
        if p:
            intro = prose.WS.sub(" ", prose.SVG.sub("", p.group(1))).strip()
    return title, intro


def extract(rel):
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return None
    src = restore(open(path, encoding="utf-8").read())
    body = article_body(src)
    if not body:
        return None

    title, intro = card_head(src)
    preamble, blocks = segments(src, *body)

    out = []
    if preamble:
        lead = prose.to_text(src[preamble[0]:preamble[1]])
        if lead:
            out.append(("Overview", lead))
    for a, b, heading in blocks:
        chunk = src[a:b]
        m = H3.search(chunk)
        if m:
            chunk = chunk[:m.start()] + chunk[m.end():]
        text = prose.to_text(chunk)
        if not heading and not text:
            continue
        out.append((heading or "Overview", text))

    if not out:
        return None

    lines = []
    if title:
        lines.append("title: %s" % title)
    lines.append("intro: %s" % intro)
    for heading, text in out:
        lines.append("")
        lines.append("## %s" % heading)
        lines.append("")
        lines.append(text)
    return "\n".join(lines).rstrip() + "\n"


def main():
    force = "--force" in sys.argv
    base = prose.content_dir(ROOT)
    written = skipped = failed = 0
    for m in modules():
        rel = m["path"]
        out = os.path.join(base, rel[: -len(".html")] + ".txt")
        if os.path.exists(out) and not force:
            skipped += 1
            continue
        text = extract(rel)
        if not text:
            print("  !! no article found in %s" % rel)
            failed += 1
            continue
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(text)
        written += 1
    print("seeded  : %d" % written)
    print("existing: %d" % skipped)
    if failed:
        print("failed  : %d" % failed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
