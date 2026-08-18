#!/usr/bin/env python3
"""Render the generated Python modules from tools/python_topics.py.

The twelve hand-written Python pages set the shape: breadcrumb, title, lead,
then a two-column layout with runnable editors on the left and a notes column
on the right. These match it, because a reader moving between the two should
not be able to tell which is which.

The page is written whole on every build. The article text is written to
content/articles/python/ where build_articles.py picks it up, and the
questions reach build_labs.py through tools/labs.py, which imports them the
same way it imports the interview track's.

Registers its own catalog entries, so a new topic needs one edit -
python_topics.py - plus its place in sequence.py.

    python3 tools/build_python_topics.py
"""

import html
import json
import os
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data
from lib_pages import last_modified, pretty_date
from python_topics import TOPICS

PREFIX = "../"
DIR = "python"
TOPIC_KEY = "python"

CSS = """
        .py-note {
            border-left: 2px solid var(--border-subtle);
            padding-left: 0.9rem;
            line-height: 1.7;
        }
        .py-note code { color: var(--accent-primary); }
        .vz-pt-lead { margin-top: 0.5rem; max-width: 60ch; color: var(--text-muted); }
"""


def rel_for(t):
    return "%s/%s.html" % (DIR, t["slug"])


def esc(s):
    return html.escape(s, quote=False)


def editor(filename, code):
    if "</script" in code.lower():
        raise SystemExit("%s contains </script and would break out of the tag" % filename)
    """One runnable program: the source, the editor, Run/Reset, the console.

    The markup matches the hand-written pages exactly, because
    assets/vizlearn-python.js binds to these class names and the twelve
    existing pages are what defined them.
    """
    # The code is emitted raw. <script> content is raw text, so entities are
    # not decoded inside it: escaping turned `n > 3` into `n &gt; 3` and
    # `{who:<8}` into a broken format spec, which is a SyntaxError at import
    # and a ValueError at format time. The only sequence that would need
    # escaping here is a literal </script>, which no program contains.
    return """                <div class="vz-py" data-vz-py>
                    <script type="text/plain" class="py-src">%(code)s</script>
                    <div class="vz-code-bar">
                        <span class="vz-code-dot"></span><span>%(file)s</span>
                        <span class="vz-code-lang">Python 3</span>
                    </div>
                    <div class="vz-code" data-vz-code="python">
                        <div class="vz-code-gutter" aria-hidden="true"></div>
                        <div class="vz-code-scroll">
                            <pre class="vz-code-hl" aria-hidden="true"></pre>
                            <textarea class="vz-code-input py-editor" aria-label="Python code editor"
                                      spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>
                        </div>
                    </div>
                    <div class="py-controls">
                        <button type="button" class="py-run-btn">Run</button>
                        <button type="button" class="py-reset-btn">Reset</button>
                        <span class="py-status"></span>
                    </div>
                    <div class="vz-console">
                        <div class="vz-console-bar">Output</div>
                        <pre class="vz-console-body py-output" aria-live="polite"
                             data-empty="Press Run to execute this code."></pre>
                    </div>
                </div>
""" % {"code": code.rstrip(), "file": esc(filename)}


def page(t):
    rel = rel_for(t)
    iso = last_modified(rel)
    head = shell.head_top("%s | VizLearn" % t["title"], PREFIX).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        CSS.strip("\n"))

    editors = "\n".join(
        """            <div class="card-container">
                <div class="card-header"><h2 class="font-bold text-lg" style="color: var(--text-main)">%s</h2></div>
                <div class="p-4 md:p-5">
%s                </div>
            </div>""" % (esc(name), editor(name, code))
        for name, code in t["programs"])

    notes = "\n".join('                        <div class="py-note">%s</div>' % n
                      for n in t["notes"])

    main = """
    <main class="flex-1 p-4 md:p-8 max-w-[1600px] mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="vz-pt-lead">%(lead)s</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">
            <div class="lg:col-span-7 space-y-6" data-vz-viz>
%(editors)s
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
                                       ("Python", PREFIX + DIR + "/"),
                                       (t["cat"], None)]),
        "title": esc(t["title"]),
        "lead": esc(t["lead"]),
        "editors": editors,
        "notes": notes,
    }
    # build_articles.py injects the prose between its own markers, but it
    # needs somewhere to put it: the marker plus an empty prose card, exactly
    # as the hand-written pages carry.
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
    # 1. the pages
    os.makedirs(os.path.join(ROOT, DIR), exist_ok=True)
    for t in TOPICS:
        open(os.path.join(ROOT, rel_for(t)), "w", encoding="utf-8").write(page(t))

    # 2. the articles, where build_articles.py looks for them
    art_dir = os.path.join(ROOT, "content", "articles", DIR)
    os.makedirs(art_dir, exist_ok=True)
    for t in TOPICS:
        open(os.path.join(art_dir, "%s.txt" % t["slug"]), "w",
             encoding="utf-8").write(t["article"].strip() + "\n")

    # 3. the catalog
    index = os.path.join(ROOT, "index.html")
    src = open(index, encoding="utf-8").read()
    data, start, end = read_course_data(index)
    if TOPIC_KEY not in data:
        raise SystemExit("courseData has no %r topic" % TOPIC_KEY)
    data[TOPIC_KEY], added = catalog_entry(data[TOPIC_KEY])
    block = json.dumps(data, indent=4, ensure_ascii=False)
    open(index, "w", encoding="utf-8").write(src[:start] + block + src[end:])

    print("python pages written : %d" % len(TOPICS))
    print("articles written     : %d" % len(TOPICS))
    print("catalog              : %d entries added, %d total in the track"
          % (added, len(data[TOPIC_KEY]["courses"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
