#!/usr/bin/env python3
"""Generate assets/modules.js from the catalog in index.html.

Run this after adding a module to index.html's courseData; every page picks the
new entry up automatically because they all load this one file.
"""

import json
import os

from lib_catalog import ROOT, modules
from sequence import LEARNING_PATH

OUT = os.path.join(ROOT, "assets", "modules.js")

HEADER = """/* GENERATED FILE - do not edit by hand.
 * Source: index.html (courseData).  Rebuild: python3 tools/build_catalog.py
 * Every page loads this, so the article list lives in exactly one place.
 */
"""


def main():
    entries = [
        {
            "title": m["title"],
            "path": m["path"],
            "category": m["category"],
            "topic": m["topic"],
            "icon": m["icon"],
            # Carried so search can match on descriptions, not just titles.
            "desc": m["desc"],
        }
        for m in modules()
    ]
    entries.sort(key=lambda e: (e["category"], e["title"]))
    body = json.dumps(entries, indent=1, ensure_ascii=False)

    # The curated beginner route, resolved from paths to titles so the hub can
    # render it without a second lookup.
    by_path = {m["path"]: m for m in modules()}
    stages = []
    for stage in LEARNING_PATH:
        items = []
        for p in stage["modules"]:
            m = by_path.get(p)
            if m is None:
                raise SystemExit("learning path references a missing module: %s" % p)
            items.append({"title": m["title"], "path": p, "category": m["category"]})
        stages.append({"title": stage["title"], "blurb": stage["blurb"], "modules": items})

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(HEADER)
        fh.write("window.VIZLEARN_MODULES = %s;\n\n" % body)
        fh.write("window.VIZLEARN_PATH = %s;\n"
                 % json.dumps(stages, indent=1, ensure_ascii=False))

    print("wrote %s (%d modules, %d learning-path stages)"
          % (os.path.relpath(OUT, ROOT), len(entries), len(stages)))


if __name__ == "__main__":
    main()
