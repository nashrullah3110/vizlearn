#!/usr/bin/env python3
"""Generate assets/modules.js from the catalog in index.html.

Run this after adding a module to index.html's courseData; every page picks the
new entry up automatically because they all load this one file.
"""

import json
import os

from lib_catalog import ROOT, modules
from sequence import LEARNING_PATH, LEARNING_PATHS

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

    # Routes resolved from paths to titles so the hub can render one without a
    # second lookup. A stale reference is a build failure, not a dead link.
    by_path = {m["path"]: m for m in modules()}

    def resolve(path_stages, where):
        out = []
        for stage in path_stages:
            items = []
            for p in stage["modules"]:
                m = by_path.get(p)
                if m is None:
                    raise SystemExit("%s references a missing module: %s" % (where, p))
                items.append({"title": m["title"], "path": p, "category": m["category"]})
            out.append({"title": stage["title"], "blurb": stage["blurb"], "modules": items})
        return out

    stages = resolve(LEARNING_PATH, "learning path")
    paths = [{"key": r["key"], "title": r["title"], "blurb": r["blurb"],
              "stages": resolve(r["stages"], "path %s" % r["key"])}
             for r in LEARNING_PATHS]

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(HEADER)
        fh.write("window.VIZLEARN_MODULES = %s;\n\n" % body)
        # VIZLEARN_PATH stays for anything still reading the single route.
        fh.write("window.VIZLEARN_PATH = %s;\n\n"
                 % json.dumps(stages, indent=1, ensure_ascii=False))
        fh.write("window.VIZLEARN_PATHS = %s;\n"
                 % json.dumps(paths, indent=1, ensure_ascii=False))

    print("wrote %s (%d modules, %d routes, %d module references)"
          % (os.path.relpath(OUT, ROOT), len(entries), len(paths),
             sum(len(s["modules"]) for r in paths for s in r["stages"])))


if __name__ == "__main__":
    main()
