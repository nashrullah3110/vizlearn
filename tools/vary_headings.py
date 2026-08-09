#!/usr/bin/env python3
"""One-time migration: vary the section headings on the hand-written pages.

Counted across the article regions, 133 pages opened their experiments with
"Interactive Exploration Guide", 131 closed with "Key Takeaway" and 62 opened
with "Quick Context" - the same skeleton, word for word, on more than half the
site. That is a machine-readable signature of templated content, and it is
what a scaled-content classifier keys on.

Scope is deliberately the hand-written pages only. The pages generated from
articles_*.py already draw their headings from varied pools, and rewriting
them here would be undone by the next `npm run build`.

This changes labels, not structure - it is worth being clear that the sections
underneath still follow a common shape. It removes the exact-string signature;
it does not by itself make the pages structurally different.

Run once:  python3 tools/vary_headings.py
"""

import hashlib
import os
import re
import sys

from articles import ARTICLES
from lib_catalog import ROOT, modules

# Every replacement for an experiments heading has to keep matching
# build_labs.EXP_HEADING, or the run buttons stop being wired to that list.
POOLS = {
    "experiments": [
        "Guided experiments",
        "Experiments to try",
        "Things to try",
        "Try it yourself",
        "Exploration guide",
        "Guided tour",
    ],
    "context": [
        "The idea in brief",
        "Start here",
        "What this is",
        "Before the details",
        "Context first",
        "The problem it solves",
    ],
    "takeaway": [
        "In one line",
        "What to remember",
        "Worth remembering",
        "Summing up",
        "The short of it",
        "Where that leaves you",
    ],
    "mistakes": [
        "Common mistakes",
        "Where this goes wrong",
        "What trips people up",
        "Traps worth knowing",
        "Failure modes",
    ],
}

# Which pool each templated heading belongs to, matched case-insensitively on
# the stripped text.
TEMPLATED = {
    "interactive exploration guide": "experiments",
    "guided experiments": "experiments",
    "guided experiments with the visualizer": "experiments",
    "quick context": "context",
    "key takeaway": "takeaway",
    "key takeaways": "takeaway",
    "what usually goes wrong": "mistakes",
    "common mistakes": "mistakes",
}

H3 = re.compile(r"(<h3\b[^>]*>)(.*?)(</h3>)", re.S)
TAGS = re.compile(r"<[^>]+>")


def text_of(s):
    return re.sub(r"\s+", " ", TAGS.sub("", s)).strip()


def pick(pool, rel, used):
    """Deterministic per page, but never repeat a heading within one page."""
    opts = POOLS[pool]
    seed = int(hashlib.md5((rel + pool).encode()).hexdigest(), 16)
    for i in range(len(opts)):
        cand = opts[(seed + i) % len(opts)]
        if cand.lower() not in used:
            return cand
    return opts[seed % len(opts)]


def process(rel):
    path = os.path.join(ROOT, rel)
    src = open(path, encoding="utf-8").read()

    # Only the article region; the visualisation panels use h3 for control
    # legends and those are not prose headings.
    start = src.find("<!-- auto-article-vizlearn -->")
    if start == -1:
        start = 0
    end = src.find("<!-- VIZLEARN:MODULE:BEGIN")
    if end == -1:
        end = len(src)

    used = {text_of(m.group(2)).lower() for m in H3.finditer(src, start, end)}
    changed = 0
    out, last = [], start

    for m in H3.finditer(src, start, end):
        title = text_of(m.group(2))
        pool = TEMPLATED.get(title.lower().rstrip(":?. "))
        if not pool:
            continue
        new = pick(pool, rel, used)
        used.discard(title.lower())
        used.add(new.lower())
        out.append(src[last:m.start()])
        out.append(m.group(1) + new + m.group(3))
        last = m.end()
        changed += 1

    if not changed:
        return 0
    out.append(src[last:])
    # `out` begins at `start`, so the untouched head is prepended once.
    open(path, "w", encoding="utf-8").write(src[:start] + "".join(out))
    return changed


def main():
    pages = changed = 0
    for m in modules():
        rel = m["path"]
        if rel in ARTICLES:
            continue          # generated from articles_*.py, already varied
        n = process(rel)
        if n:
            pages += 1
            changed += n
    print("hand-written pages retitled : %d" % pages)
    print("headings changed            : %d" % changed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
