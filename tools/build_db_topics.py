#!/usr/bin/env python3
"""Render the generated database modules from tools/db_topics.py.

Query coverage on this track was already strong - joins, CTEs, window
functions, execution order. What there was nothing on was schema design and
concurrency: the two places real projects actually come apart.

Each page runs real SQLite in the browser through assets/vizlearn-sql.js, the
same engine as /sql-lab/, seeded with tables built for the module. Nothing here
is a recorded result; the reader can edit any query and get the database's own
answer, including its own error messages.

Two of the modules are about two transactions interleaving, which one
connection cannot demonstrate. Those step through a scripted schedule instead
(assets/vizlearn-dbq.js) and say what each statement would see under the
isolation level chosen.

Registers its own catalog entries, so a new topic needs one edit -
db_topics.py - plus its place in sequence.py.

    python3 tools/build_db_topics.py
"""

import html
import json
import os
import re
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data
from db_topics import TOPICS

PREFIX = "../"
DIR = "database"
TOPIC_KEY = "db"

CSS = """
        .db-note {
            border-left: 2px solid var(--border-subtle);
            padding-left: 0.9rem;
            line-height: 1.7;
        }
        .db-note code { color: var(--accent-primary); }
        .vz-db-lead { margin-top: 0.5rem; max-width: 60ch; color: var(--text-muted); }
"""


# The thumbnails are parsed as SVG by tools/build_og_images.py, and XML defines
# only five named entities. A stray &rarr; or &mdash; renders fine in the page,
# where it is HTML, and fails the OG render with "Entity not defined" - which
# surfaces two build steps later as a missing image. Catch it here instead.
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


def guard(text, what):
    """Raw text inside <script type="text/plain"> is a raw text element, so
    entities are not decoded there and escaping would corrupt the SQL. The one
    sequence that would break out is a literal </script."""
    if "</script" in text.lower():
        raise SystemExit("%s contains </script and would break out of the tag" % what)
    return text


def variants(t):
    if not t.get("variants"):
        return ""
    rows = []
    for i, v in enumerate(t["variants"]):
        rows.append(
            '                        <button type="button" class="db-variant"'
            ' aria-pressed="%s"><span>%s</span>'
            '<script type="text/plain" class="db-variant-sql">%s</script></button>'
            % ("true" if i == 0 else "false", esc(v["label"]),
               guard(v["sql"], t["slug"])))
    return """                    <div class="db-variants" data-vz-dbq>
                        <p class="db-variants-label">%s</p>
%s
                    </div>
""" % (esc(t.get("variants_label", "Same question, different queries")),
       "\n".join(rows))


def sql_block(t):
    return """%(variants)s                    <div class="vz-db-sql" data-vz-sql>
                        <script type="text/plain" class="sql-seed">%(seed)s</script>
                        <div class="vz-code-bar">
                            <span class="vz-code-dot"></span><span>query.sql</span>
                            <span class="vz-code-lang">SQLite</span>
                        </div>
                        <div class="vz-code" data-vz-code="sql">
                            <div class="vz-code-gutter" aria-hidden="true"></div>
                            <div class="vz-code-scroll">
                                <pre class="vz-code-hl" aria-hidden="true"></pre>
                                <textarea class="vz-code-input sql-editor" aria-label="SQL editor"
                                          spellcheck="false" autocapitalize="off"
                                          autocomplete="off">%(starter)s</textarea>
                            </div>
                        </div>
                        <div class="sql-controls">
                            <button type="button" class="sql-btn sql-btn-primary sql-run-btn">Run</button>
                            <button type="button" class="sql-btn sql-reset-btn">Reset database</button>
                            <span class="sql-status" aria-live="polite"></span>
                        </div>
                        <div class="vz-console">
                            <div class="vz-console-bar">Result</div>
                            <div class="vz-console-body sql-result" aria-live="polite"
                                 data-empty="Press Run to execute this query."></div>
                        </div>
                        <div class="sql-schema"></div>
                    </div>
""" % {"variants": variants(t),
       "seed": guard(t["seed"], t["slug"]),
       "starter": esc(t["starter"])}


def timeline_block(t):
    cfg = json.dumps(t["timeline"], ensure_ascii=False)
    if "</script" in cfg.lower():
        raise SystemExit("%s: timeline config would close the script tag" % t["slug"])
    return """                    <div class="vz-db-tl" data-vz-timeline>
                        <script type="application/json" class="db-timeline-config">%s</script>
                        <p class="db-tl-fallback">This module needs JavaScript: it
                        steps through two transactions rather than showing a
                        finished picture.</p>
                    </div>
""" % cfg


def page(t):
    head = shell.head_top("%s | VizLearn" % t["title"], PREFIX).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        CSS.strip("\n"))

    notes = "\n".join('                        <div class="db-note">%s</div>' % n
                      for n in t["notes"])
    body = timeline_block(t) if t.get("timeline") else sql_block(t)

    main = """
    <main class="flex-1 p-4 md:p-8 max-w-[1600px] mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="vz-db-lead">%(lead)s</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">
            <div class="lg:col-span-7 space-y-6" data-vz-viz>
                <div class="card-container">
                    <div class="card-header"><h2 class="font-bold text-lg" style="color: var(--text-main)">%(title)s</h2></div>
                    <div class="p-4 md:p-5">
%(body)s                    </div>
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
                                       ("Databases & SQL", PREFIX + DIR + "/"),
                                       (t["cat"], None)]),
        "title": esc(t["title"]),
        "lead": esc(t["lead"]),
        "body": body,
        "notes": notes,
    }

    mount = """    <!-- auto-article-vizlearn -->
    <section class="px-4 md:px-8 pb-8 max-w-[1600px] mx-auto w-full" data-vz-prose>
        <div class="card-container animate-fade-in">
        </div>
    </section>
"""
    out = head + shell.header(PREFIX) + main + mount + shell.close(PREFIX)
    if not t.get("timeline"):
        # The SQL engine is loaded per page rather than added to build_seo's
        # shared list, the same way /sql-lab/ loads it: it pulls a wasm payload
        # on first Run, and there is no reason to put that decision in front of
        # the 350-odd pages that have no editor on them.
        out = out.replace(
            "</body>",
            '    <script src="%sassets/vizlearn-sql.js" defer></script>\n</body>'
            % PREFIX, 1)
    return out


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

    print("db pages written : %d" % len(TOPICS))
    print("articles written : %d" % len(TOPICS))
    print("catalog          : %d entries added, %d total in the track"
          % (added, len(data[TOPIC_KEY]["courses"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
