#!/usr/bin/env python3
"""Rendered word count per article, shortest first.

Use the output to find pages that may need a completeness review, not as a
pass/fail threshold or a reason to add padding:

    python3 tools/wordcount.py            # every page, shortest first
    python3 tools/wordcount.py maths      # one track
"""

import html
import re
import sys

import prose
from lib_catalog import ROOT

TAGS = re.compile(r"<[^>]+>")
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
    rows = sorted((count(e), r) for r, e in prose.load(ROOT).items()
                  if not args or any(r.startswith(a) for a in args))

    for n, rel in rows:
        print("  %5d  %s" % (n, rel))
    total = sum(n for n, _ in rows)
    print("pages   : %d  (sorted shortest first; counts are diagnostic only)" % len(rows))
    print("words   : %d total, %d average" % (total, total // max(len(rows), 1)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
