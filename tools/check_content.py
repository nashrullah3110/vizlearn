#!/usr/bin/env python3
"""Compare each content file against the article the page shipped with.

Guards the one-way step: content/articles/ was seeded from the live pages,
and from then on the pages are generated from the files. If the seeding lost
a sentence, this is where it shows up - it reports any page whose rendered
content file says less than the committed page did.

    python3 tools/check_content.py            # vs. git HEAD
    python3 tools/check_content.py --min 40   # only losses over 40 words
"""

import html
import os
import re
import subprocess
import sys
from collections import Counter

import prose
from build_articles import card_inner, render
from build_lede import restore
from lib_catalog import ROOT, modules

TAGS = re.compile(r"<[^>]+>")
DROP = ("Run this",)


def words(fragment):
    text = html.unescape(TAGS.sub(" ", fragment))
    for d in DROP:
        text = text.replace(d, " ")
    return Counter(text.split())


def committed(rel):
    out = subprocess.run(["git", "show", "HEAD:" + rel], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode:
        return None
    src = restore(out.stdout)
    span = card_inner(src)
    return src[span[0]:span[1]] if span else None


def main():
    argv = sys.argv[1:]
    floor = int(argv[argv.index("--min") + 1]) if "--min" in argv else 15
    entries = prose.load(ROOT)
    titles = {m["path"]: m["title"] for m in modules()}

    losses = 0
    for rel in sorted(entries):
        old = committed(rel)
        if old is None:
            continue
        new = render("%s: A Practical Guide" % titles.get(rel, rel), entries[rel])
        missing = words(old) - words(new)
        n = sum(missing.values())
        if n > floor:
            losses += 1
            sample = " ".join(sorted(missing)[:12])
            print("  %-60s -%d words  %s" % (rel, n, sample))
    print("pages checked : %d" % len(entries))
    print("with losses   : %d" % losses)
    return 1 if losses else 0


if __name__ == "__main__":
    sys.exit(main())
