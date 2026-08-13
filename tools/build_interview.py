#!/usr/bin/env python3
"""Render /interview/ - one page per interview question.

Every other track on this site is a set of hand-written pages that the build
decorates. This one is generated whole, because the pages are the same shape
about a hundred times over: the question, the answer, a visualisation that
steps through the mechanism, and the code in a real interpreter.

What each page carries, in reading order:

  * the question as an h1, and the short answer immediately under it - a
    reader who only wants the answer should not have to scroll;
  * a step-through visualisation, driven by frames that were produced by
    running the algorithm (tools/interview_viz.py);
  * the long answer, in the standard .vz-article shape so tools/build_lede.py
    can lift an overview and a table of contents out of it;
  * the editor from /python-lab/ with a working implementation in it;
  * the end-of-module check, which tools/build_labs.py writes from the
    questions in tools/labs.py.

Written whole on every run - there are no hand-edited regions in interview/.
The catalog entry in index.html is patched between markers, so a question
added to the content modules appears in search, on the hub and in the sitemap
without anything being transcribed by hand.

    python3 tools/build_interview.py
"""

import html
import json
import os
import re
import sys

import lib_qpage as qpage
from interview import QUESTIONS, GROUPS
from lib_catalog import ROOT, read_course_data
from lib_pages import TOPICS

DIR = TOPICS["interview"]["dir"]

# --------------------------------------------------------------------------
# The catalog entry in index.html
# --------------------------------------------------------------------------

CAT_BEGIN = '"interview": {'


def catalog_entry():
    courses = []
    for q in QUESTIONS:
        courses.append({
            "title": q["title"],
            "path": qpage.rel_for(q, DIR),
            "svg": q["svg"],
        })
    return {"title": TOPICS["interview"]["title"], "courses": courses}


def patch_index():
    """Add or replace courseData["interview"] in index.html.

    The catalog is the site's single source of truth (lib_catalog reads it),
    so the track has to be in it before search, the hub, the sitemap or the OG
    images know these pages exist.
    """
    path = os.path.join(ROOT, "index.html")
    src = open(path, encoding="utf-8").read()
    data, start, end = read_course_data(path)

    data["interview"] = catalog_entry()
    rendered = json.dumps(data, indent=8, ensure_ascii=False)
    open(path, "w", encoding="utf-8").write(src[:start] + rendered + src[end:])
    return len(data["interview"]["courses"])


def main():
    out_dir = os.path.join(ROOT, DIR)
    os.makedirs(out_dir, exist_ok=True)

    slugs = set()
    for q in QUESTIONS:
        if q["slug"] in slugs:
            raise SystemExit("duplicate slug: %s" % q["slug"])
        slugs.add(q["slug"])
        open(os.path.join(ROOT, qpage.rel_for(q, DIR)), "w", encoding="utf-8").write(
            qpage.page(q, "interview", DIR, GROUPS[q["group"]]["label"]))

    # A page left over from a question that has since been renamed would stay
    # on disk, in the sitemap and in nothing else. Sweep them.
    stale = 0
    keep = {"%s.html" % q["slug"] for q in QUESTIONS} | {"index.html"}
    for name in os.listdir(out_dir):
        if name.endswith(".html") and name not in keep:
            os.remove(os.path.join(out_dir, name))
            stale += 1

    n = patch_index()
    print("interview questions   : %d" % len(QUESTIONS))
    print("catalog entries       : %d" % n)
    if stale:
        print("stale pages removed   : %d" % stale)
    return 0


if __name__ == "__main__":
    sys.exit(main())
