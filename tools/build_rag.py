#!/usr/bin/env python3
"""Generate the RAG and LLM-serving pages inside gen_ai/.

The gen_ai/ track is hand-written, and stays that way. These pages are added
alongside those: same track, same URL space, but generated from
tools/rag_topics.py through the shared page shape in tools/lib_qpage.py, so
each one carries a step-through visualisation, the article, a runnable
implementation and an end-of-module check without any of it being transcribed
by hand.

The catalog entry is *merged* rather than replaced. courseData["gen-ai"]
already lists the 24 hand-written modules, and overwriting it would delete
them from search, the hub and the sitemap while leaving the files on disk.

Run after tools/build_articles.py and before tools/build_labs.py, for the same
reason tools/build_interview.py does.

    python3 tools/build_rag.py
"""

import json
import os
import sys

import lib_qpage as qpage
from lib_catalog import ROOT, read_course_data
from lib_pages import TOPICS
from rag_topics import TOPICS as ENTRIES

TRACK = "gen-ai"
DIR = TOPICS[TRACK]["dir"]


def catalog_entry(existing):
    """Merge the generated pages into the track's existing course list.

    Keyed by path so a rebuild updates a generated entry in place rather than
    appending a second copy, and so a hand-written module is never touched.
    """
    generated = {
        qpage.rel_for(t, DIR): {"title": t["title"],
                                "path": qpage.rel_for(t, DIR),
                                "svg": t["svg"]}
        for t in ENTRIES
    }

    courses = []
    seen = set()
    for course in existing.get("courses", []):
        path = course.get("path")
        courses.append(generated.get(path, course))
        seen.add(path)
    for path, course in generated.items():
        if path not in seen:
            courses.append(course)

    return {"title": existing.get("title", TOPICS[TRACK]["title"]),
            "courses": courses}


def patch_index():
    path = os.path.join(ROOT, "index.html")
    src = open(path, encoding="utf-8").read()
    data, start, end = read_course_data(path)
    before = len(data.get(TRACK, {}).get("courses", []))
    data[TRACK] = catalog_entry(data.get(TRACK, {}))
    after = len(data[TRACK]["courses"])

    rendered = json.dumps(data, indent=8, ensure_ascii=False)
    open(path, "w", encoding="utf-8").write(src[:start] + rendered + src[end:])
    return before, after


def main():
    slugs = set()
    for t in ENTRIES:
        if t["slug"] in slugs:
            raise SystemExit("duplicate slug: %s" % t["slug"])
        slugs.add(t["slug"])
        rel = qpage.rel_for(t, DIR)
        open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(
            qpage.page(t, TRACK, DIR, t.get("group_label", "")))

    before, after = patch_index()
    print("rag pages written     : %d" % len(ENTRIES))
    print("gen-ai catalog        : %d -> %d entries" % (before, after))
    return 0


if __name__ == "__main__":
    sys.exit(main())
