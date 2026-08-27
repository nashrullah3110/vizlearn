#!/usr/bin/env python3
"""Rendered word count per article, shortest first.

The long-form target is 2000+ words a page, so this is the worklist:

    python3 tools/wordcount.py            # every page under target
    python3 tools/wordcount.py maths      # one track
    python3 tools/wordcount.py --all      # everything, including done
"""

import html
import re
import sys

import prose
from lib_catalog import ROOT

TAGS = re.compile(r"<[^>]+>")
TARGET = 2000

# Code is not prose. The Pydantic and FastAPI articles carry their examples
# inline - a runnable editor holds its program in a <script> and a static
# block in a <pre> - and counting those made a 900-word article report as
# 7,000, so both tracks silently vanished from this worklist.
CODE = re.compile(
    r"<pre\b.*?</pre>|<script\b.*?</script>|<textarea\b.*?</textarea>",
    re.S | re.I)


def count(entry):
    text = entry.get("intro", "")
    for heading, body in entry["sections"]:
        text += " " + heading + " " + body
    text = CODE.sub(" ", text)
    return len(html.unescape(TAGS.sub(" ", text)).split())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    show_all = "--all" in sys.argv
    rows = sorted((count(e), r) for r, e in prose.load(ROOT).items()
                  if not args or any(r.startswith(a) for a in args))

    under = [r for r in rows if r[0] < TARGET]
    for n, rel in (rows if show_all else under):
        print("  %5d  %s" % (n, rel))
    done = len(rows) - len(under)
    total = sum(n for n, _ in rows)
    print("pages   : %d  (%d at target, %d to go)" % (len(rows), done, len(under)))
    print("words   : %d total, %d average" % (total, total // max(len(rows), 1)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
