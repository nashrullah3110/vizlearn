#!/usr/bin/env python3
"""Render the generated maths modules from tools/math_topics.py.

The maths track was the thinnest on the site and the one everything else
leans on. Pages across the site used orthogonality, SVD, convexity and
sampling distributions as though they had been introduced; none of them had.
PCA is the sharpest case - it assumes an eigendecomposition and an SVD, and
only the first was taught anywhere.

These are demonstrations rather than simulations: nothing is fitted, and the
arithmetic is the subject. The SVD is a real decomposition of the matrix on
screen, the central limit page really resamples the population it draws, and
the Taylor series really sums its terms.

Registers its own catalog entries, so a new topic needs one edit -
math_topics.py - plus its place in sequence.py.

    python3 tools/build_math_topics.py
"""

import html
import json
import os
import re
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data
from math_topics import TOPICS

PREFIX = "../"
DIR = "maths"
TOPIC_KEY = "maths"

CSS = """
        .math-note {
            border-left: 2px solid var(--border-subtle);
            padding-left: 0.9rem;
            line-height: 1.7;
        }
        .math-note code { color: var(--accent-primary); }
        .vz-math-lead { margin-top: 0.5rem; max-width: 60ch; color: var(--text-muted); }
"""

# The thumbnails are parsed as SVG by tools/build_og_images.py, and XML defines
# only five named entities. A stray &rarr; renders fine in the page, where it is
# HTML, and fails the OG render two build steps later as a missing image.
XML_SAFE = {"amp", "lt", "gt", "quot", "apos"}
NAMED_ENTITY = re.compile(r"&([a-zA-Z][a-zA-Z0-9]*);")


def check_thumbnails():
    for t in TOPICS:
        for name in NAMED_ENTITY.findall(t["svg"]):
            if name not in XML_SAFE:
                raise SystemExit(
                    "%s: thumbnail uses &%s; - XML has no such entity. "
                    "Use a numeric reference." % (t["slug"], name))


def rel_for(t):
    return "%s/%s.html" % (DIR, t["slug"])


def esc(s):
    return html.escape(s, quote=False)


def viz(t):
    cfg = json.dumps(t["viz"], ensure_ascii=False)
    if "</script" in cfg.lower():
        raise SystemExit("%s: config would close the script tag" % t["slug"])
    return """                <div class="vz-math" data-vz-math>
                    <script type="application/json" class="math-config">%s</script>
                    <p class="math-fallback">This module needs JavaScript: the
                    numbers are computed in the page rather than recorded.</p>
                </div>
""" % cfg


def page(t):
    head = shell.head_top("%s | VizLearn" % t["title"], PREFIX).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        CSS.strip("\n"))

    notes = "\n".join('                        <div class="math-note">%s</div>' % n
                      for n in t["notes"])

    main = """
    <main class="flex-1 p-4 md:p-8 max-w-[1600px] mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="vz-math-lead">%(lead)s</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">
            <div class="lg:col-span-7 space-y-6" data-vz-viz>
                <div class="card-container">
                    <div class="card-header"><h2 class="font-bold text-lg" style="color: var(--text-main)">%(title)s</h2></div>
                    <div class="p-4 md:p-5">
%(viz)s                    </div>
                </div>
            </div>
            <div class="lg:col-span-5 space-y-6">
                <div class="card-container">
                    <div class="card-header"><h3 class="font-bold text-sm uppercase tracking-wide" style="color: var(--text-muted)">Worth knowing</h3></div>
                    <div class="p-5 space-y-4 text-sm" style="color: var(--text-muted)">
%(notes)s
                    </div>
                </div>
            </div>
        </div>
    </main>
""" % {
        "crumb": shell.breadcrumb_bar([("Home", PREFIX + "index.html"),
                                       ("Maths for Machine Learning", PREFIX + DIR + "/"),
                                       (t["cat"], None)]),
        "title": esc(t["title"]),
        "lead": esc(t["lead"]),
        "viz": viz(t),
        "notes": notes,
    }

    mount = """    <!-- auto-article-vizlearn -->
    <section class="px-4 md:px-8 pb-8 max-w-[1600px] mx-auto w-full" data-vz-prose>
        <div class="card-container animate-fade-in">
        </div>
    </section>
"""
    return head + shell.header(PREFIX) + main + mount + shell.close(PREFIX)


def catalog_entry(existing):
    generated = {rel_for(t): {"title": t["title"], "path": rel_for(t), "svg": t["svg"]}
                 for t in TOPICS}
    courses, seen = [], set()
    for course in existing.get("courses", []):
        path = course.get("path", "").lstrip("./")
        courses.append(generated.get(path, course))
        seen.add(path)
    for path, course in generated.items():
        if path not in seen:
            courses.append(course)
    out = dict(existing)
    out["courses"] = courses
    return out, len([p for p in generated if p not in seen])


def main():
    check_thumbnails()
    os.makedirs(os.path.join(ROOT, DIR), exist_ok=True)
    for t in TOPICS:
        open(os.path.join(ROOT, rel_for(t)), "w", encoding="utf-8").write(page(t))

    art_dir = os.path.join(ROOT, "content", "articles", DIR)
    os.makedirs(art_dir, exist_ok=True)
    for t in TOPICS:
        open(os.path.join(art_dir, "%s.txt" % t["slug"]), "w",
             encoding="utf-8").write(t["article"].strip() + "\n")

    index = os.path.join(ROOT, "index.html")
    src = open(index, encoding="utf-8").read()
    data, start, end = read_course_data(index)
    if TOPIC_KEY not in data:
        raise SystemExit("courseData has no %r topic" % TOPIC_KEY)
    data[TOPIC_KEY], added = catalog_entry(data[TOPIC_KEY])
    block = json.dumps(data, indent=4, ensure_ascii=False)
    open(index, "w", encoding="utf-8").write(src[:start] + block + src[end:])

    print("maths pages written : %d" % len(TOPICS))
    print("articles written : %d" % len(TOPICS))
    print("catalog          : %d entries added, %d total in the track"
          % (added, len(data[TOPIC_KEY]["courses"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
