#!/usr/bin/env python3
"""Fold each interview question's program into its article.

The pages used to carry a `Run it in Python` section below the article: a
full, working program in an editor, with the article above it discussing
similar code in static blocks nobody could run. Same split the Pydantic and
FastAPI tracks had, and the same fix - the program becomes a section of the
article, introduced by the prose, and runnable where it is read.

The article's own fenced blocks stay static, deliberately. Of 210 of them,
five are complete programs; ninety-four define a function and never call it,
and a hundred and eleven are fragments of two or three lines. Turning those
into editors would give a reader a hundred boxes that print nothing and a
hundred more that raise. They are excerpts being discussed, and an excerpt is
not a program.

The insertion point is after the article's first section, so build_lede.py
still lifts an introductory section out as the Overview.

Run once; it is idempotent.

    python3 tools/merge_interview_code.py
"""

import io
import os
import re
import sys

from interview import QUESTIONS
from lib_catalog import ROOT

MARK = "## Run it"


def merged(text, entry):
    block = "%s\n\n%s\n\n```python-run\n%s\n```" % (
        MARK, entry["intro"].strip(), entry["code"].strip())

    # Re-running refreshes the block rather than skipping it. The article
    # holds a copy of the program, so a change in tools/interview_lists.py
    # would otherwise leave the two disagreeing silently - which is exactly
    # how the divide-by-zero in why-is-in-slow-on-a-list survived a fix.
    existing = re.search(r"^## Run it\n\n.*?\n```python-run\n.*?\n```",
                         text, re.S | re.M)
    if existing:
        return text[:existing.start()] + block + text[existing.end():]

    first = text.find("\n## ")
    second = text.find("\n## ", first + 1) if first != -1 else -1
    if second == -1:
        return text.rstrip() + "\n\n" + block + "\n"
    return text[:second] + "\n\n" + block + text[second:]


def main():
    base = os.path.join(ROOT, "content", "articles", "interview")
    done = missing = skipped = 0
    for q in QUESTIONS:
        path = os.path.join(base, "%s.txt" % q["slug"])
        if not os.path.exists(path):
            missing += 1
            print("  no article for %s" % q["slug"])
            continue
        text = io.open(path, encoding="utf-8").read()
        out = merged(text, q["code"])
        if out == text:
            skipped += 1
            continue
        io.open(path, "w", encoding="utf-8").write(out)
        done += 1
    print("articles written  : %d" % done)
    print("already current  : %d" % skipped)
    print("no article file  : %d" % missing)
    return 0


if __name__ == "__main__":
    sys.exit(main())
