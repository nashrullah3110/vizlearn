#!/usr/bin/env python3
"""Render the generated image-processing modules from tools/cv_topics.py.

The hand-written Computer Vision pages set the shape: breadcrumb, title, lead,
then a wide visualisation with a notes column beside it. These match it,
because a reader moving between the two should not be able to tell which is
which.

The page is written whole on every build. The article text goes to
content/articles/computer_vision/ where build_articles.py picks it up, and the
questions reach build_labs.py through tools/labs.py.

Registers its own catalog entries, so a new topic needs one edit -
cv_topics.py - plus its place in sequence.py.

    python3 tools/build_cv_topics.py
"""

import html
import json
import os
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data
from cv_topics import TOPICS

PREFIX = "../"
DIR = "computer_vision"
TOPIC_KEY = "computer-vision"

CSS = """
        .cv-note {
            border-left: 2px solid var(--border-subtle);
            padding-left: 0.9rem;
            line-height: 1.7;
        }
        .cv-note code { color: var(--accent-primary); }
        .vz-cv-lead { margin-top: 0.5rem; max-width: 60ch; color: var(--text-muted); }
"""


def rel_for(t):
    return "%s/%s.html" % (DIR, t["slug"])


def esc(s):
    return html.escape(s, quote=False)


def viz(t):
    """The mount point plus its configuration.

    The config is JSON in a script tag rather than data- attributes: a control
    list is nested, and flattening it into attributes would be a private
    encoding that only this file and the harness understood.
    """
    cfg = json.dumps(t["viz"], ensure_ascii=False)
    if "</script" in cfg.lower():
        raise SystemExit("%s: config would close the script tag" % t["slug"])
    return """                <div class="vz-cv" data-vz-cv>
                    <script type="application/json" class="cv-config">%s</script>
                    <p class="cv-fallback">This module needs JavaScript: the
                    images are computed in the page rather than downloaded.</p>
                </div>
""" % cfg


def page(t):
    head = shell.head_top("%s | VizLearn" % t["title"], PREFIX).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        CSS.strip("\n"))

    notes = "\n".join('                        <div class="cv-note">%s</div>' % n
                      for n in t["notes"])

    main = """
    <main class="flex-1 p-4 md:p-8 max-w-[1600px] mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="vz-cv-lead">%(lead)s</p>
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
                                       ("Computer Vision", PREFIX + DIR + "/"),
                                       (t["cat"], None)]),
        "title": esc(t["title"]),
        "lead": esc(t["lead"]),
        "viz": viz(t),
        "notes": notes,
    }

    # build_articles.py injects the prose between its own markers, but it needs
    # somewhere to put it: the marker plus an empty prose card, exactly as the
    # hand-written pages carry.
    mount = """    <!-- auto-article-vizlearn -->
    <section class="px-4 md:px-8 pb-8 max-w-[1600px] mx-auto w-full" data-vz-prose>
        <div class="card-container animate-fade-in">
        </div>
    </section>
"""
    return head + shell.header(PREFIX) + main + mount + shell.close(PREFIX)


def catalog_entry(existing):
    """Merge the generated entries into courseData, keeping hand-written ones."""
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

    print("cv pages written : %d" % len(TOPICS))
    print("articles written : %d" % len(TOPICS))
    print("catalog          : %d entries added, %d total in the track"
          % (added, len(data[TOPIC_KEY]["courses"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
