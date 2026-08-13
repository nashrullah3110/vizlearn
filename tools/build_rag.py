#!/usr/bin/env python3
"""Generate the RAG and LLM-serving pages inside gen_ai/.

These match the shape of the hand-written modules in the same track, because
mixing two page designs inside one track is worse than either design: a
Parameters panel on the left, a visualisation in the middle that recomputes as
you move a control, a readout on the right, then the written guide underneath.

Specifically, and unlike the /interview/ pages, there is NO embedded Python
editor and no authored multiple-choice block. tools/build_labs.py adds the
same end-of-module check the rest of the track gets, built from each page's
own "Things to try" section and key takeaway.

The arithmetic lives in assets/vizlearn-ragviz.js rather than here: each page
declares its controls and names a model, and the numbers are computed in the
reader's browser. That is the same guarantee the hand-written modules give -
what is on screen is the computation, not a picture of it.

The catalog entry is MERGED rather than replaced. courseData["gen-ai"] lists
the hand-written modules too, and overwriting it would remove them from
search, the hub and the sitemap while leaving the files on disk.

Run after tools/build_articles.py and before tools/build_labs.py.

    python3 tools/build_rag.py
"""

import html
import json
import os
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data
from lib_pages import TOPICS
from rag_topics import TOPICS as ENTRIES, WIDGETS

TRACK = "gen-ai"
DIR = TOPICS[TRACK]["dir"]
PREFIX = "../"

CSS = """
        .vz-rv-control + .vz-rv-control { margin-top: 1.15rem; }
        .vz-rv-chead {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 0.5rem; gap: 0.5rem;
        }
        .vz-rv-clabel {
            font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.04em; color: var(--text-muted);
        }
        .vz-rv-cvalue {
            font-family: 'JetBrains Mono', ui-monospace, monospace;
            font-size: 0.8rem; font-weight: 700; color: var(--accent-primary);
        }
        .vz-rv-control input[type="range"] { width: 100%; }
        .vz-rv-control select {
            width: 100%; padding: 0.45rem 0.6rem; border-radius: 8px;
            border: 1px solid var(--border-subtle); background: var(--input-bg);
            color: var(--text-main); font-size: 0.85rem;
        }
        .vz-rv-toggle {
            width: 100%; text-align: left; padding: 0.6rem 0.8rem;
            border-radius: 9px; border: 1px solid var(--border-subtle);
            background: var(--input-bg); color: var(--text-muted);
            font-size: 0.78rem; font-weight: 600; cursor: pointer;
            min-height: 44px;
        }
        .vz-rv-toggle.is-on {
            border-color: var(--accent-primary); color: var(--accent-primary);
            background: var(--accent-glow, rgba(34, 197, 94, 0.1));
        }

        .vz-rv-row { margin-bottom: 0.9rem; }
        .vz-rv-rowhead {
            display: flex; justify-content: space-between; align-items: baseline;
            gap: 0.75rem; margin-bottom: 0.3rem;
        }
        .vz-rv-label {
            font-size: 0.82rem; color: var(--text-main); overflow-wrap: anywhere;
        }
        .vz-rv-value {
            font-family: 'JetBrains Mono', ui-monospace, monospace;
            font-size: 0.8rem; font-weight: 700; color: var(--accent-primary);
            flex: 0 0 auto;
        }
        .vz-rv-track {
            height: 8px; border-radius: 999px; background: var(--input-bg);
            border: 1px solid var(--border-subtle); overflow: hidden;
        }
        .vz-rv-fill {
            height: 100%; background: var(--accent-primary);
            transition: width 0.18s ease;
        }
        .vz-rv-tag {
            display: inline-block; margin-top: 0.28rem;
            font-family: 'JetBrains Mono', ui-monospace, monospace;
            font-size: 0.66rem; color: var(--text-muted);
        }
        .vz-rv-row.is-hit .vz-rv-label { font-weight: 700; }
        .vz-rv-row.is-dim { opacity: 0.45; }
        .vz-rv-row.is-bad .vz-rv-fill { background: #dc2626; }
        .vz-rv-row.is-bad .vz-rv-value { color: #dc2626; }
        .vz-rv-row.is-done .vz-rv-fill { opacity: 0.65; }

        .vz-rv-stat {
            display: flex; justify-content: space-between; gap: 0.6rem;
            padding: 0.3rem 0; border-bottom: 1px solid var(--border-subtle);
            font-size: 0.8rem;
        }
        .vz-rv-stat:last-child { border-bottom: 0; }
        .vz-rv-stat-k { color: var(--text-muted); }
        .vz-rv-stat-v {
            font-family: 'JetBrains Mono', ui-monospace, monospace;
            color: var(--text-main); font-weight: 700; text-align: right;
        }
        .vz-rv-note { font-size: 0.78rem; line-height: 1.65; color: var(--text-muted); }
"""


def rel_for(entry):
    return "%s/%s.html" % (DIR, entry["slug"])


def card(title, body, extra=""):
    return ('<div class="card-container"><div class="card-header%s">'
            '<h3 class="font-bold text-sm uppercase tracking-wide" '
            'style="color: var(--accent-primary)">%s</h3>%s</div>%s</div>'
            % (" flex items-center justify-between" if extra else "",
               html.escape(title), extra, body))


def widget(entry):
    """The three-column interactive block, matching the hand-written modules."""
    spec = WIDGETS[entry["slug"]]
    data = json.dumps({"controls": spec["controls"], "data": spec.get("data", {})},
                      ensure_ascii=False, separators=(",", ":"))
    if "</script" in data.lower():
        raise ValueError("%s: widget spec contains a closing script tag" % entry["slug"])

    watch = "".join("<li>%s</li>" % w for w in entry.get("notice", []))

    return """
        <div class="vz-rv grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in"
             data-vz-rv data-model="%(model)s">
            <script type="application/json" class="vz-rv-data">%(data)s</script>
            <div class="lg:col-span-3 space-y-6">
                %(controls)s
            </div>
            <div class="lg:col-span-6 space-y-6" data-vz-viz>
                %(bars)s
            </div>
            <div class="lg:col-span-3 space-y-6">
                %(stats)s
                %(watch)s
            </div>
        </div>
""" % {
        "model": html.escape(spec["model"]),
        "data": data,
        "controls": card("Parameters", '<div class="p-5 vz-rv-controls"></div>'),
        "bars": card("Visualisation", '<div class="p-5 vz-rv-bars"></div>',
                     '<span class="mono-font text-xs vz-rv-badge" '
                     'style="color: var(--text-muted)">&mdash;</span>'),
        "stats": card("Readout", '<div class="p-5 vz-rv-stats"></div>'
                                 '<div class="px-5 pb-5">'
                                 '<p class="vz-rv-note"></p></div>'),
        "watch": card("What to watch", '<div class="p-5"><ul class="vz-rv-watch '
                      'text-xs leading-relaxed space-y-2" '
                      'style="color: var(--text-muted)">%s</ul></div>' % watch)
        if watch else "",
    }


def article(entry):
    body = []
    for heading, text in entry["sections"]:
        body.append("<div><h3>%s</h3>%s</div>" % (html.escape(heading), text))

    return """
        <!-- auto-article-vizlearn -->
        <section class="mt-12 animate-fade-in" data-vz-prose>
            <div class="card-container">
                <div class="card-header">
                    <h2 class="font-bold text-xl md:text-2xl" style="color: var(--text-main)">%(title)s</h2>
                    <p class="mt-2 text-sm" style="color: var(--text-muted)">%(sub)s</p>
                </div>
                <div class="vz-article p-5 md:p-7 space-y-7 text-sm md:text-base leading-7" style="color: var(--text-main)">
                    <!-- VIZLEARN:LEDE:SLOT -->
                    %(body)s
                </div>
            </div>
        </section>
""" % {"title": html.escape(entry["title"] + ": A Practical Guide"),
       "sub": html.escape(entry["asked"]),
       "body": "\n                    ".join(body)}


def page(entry):
    head = shell.head_top("%s | VizLearn" % entry["title"], PREFIX).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        CSS.strip("\n"))

    main = """
    <main class="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="mt-2 max-w-2xl" style="color: var(--text-muted)">%(lead)s</p>
        </div>
%(widget)s
%(article)s
    </main>
""" % {
        "crumb": shell.breadcrumb_bar([
            ("Home", PREFIX + "index.html"),
            (TOPICS[TRACK]["title"], PREFIX + DIR + "/"),
            (entry["title"], None)]),
        "title": html.escape(entry["title"]),
        "lead": entry["lead"],
        "widget": widget(entry),
        "article": article(entry),
    }

    return head + shell.header(PREFIX) + main + shell.close(PREFIX)


# --------------------------------------------------------------------------
# Catalog
# --------------------------------------------------------------------------

def catalog_entry(existing):
    """Merge the generated pages into the track's existing course list.

    Keyed by path so a rebuild updates a generated entry in place rather than
    appending a duplicate, and so a hand-written module is never touched.
    """
    generated = {rel_for(t): {"title": t["title"], "path": rel_for(t),
                              "svg": t["svg"]} for t in ENTRIES}
    courses, seen = [], set()
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
    for entry in ENTRIES:
        if entry["slug"] in slugs:
            raise SystemExit("duplicate slug: %s" % entry["slug"])
        slugs.add(entry["slug"])
        open(os.path.join(ROOT, rel_for(entry)), "w", encoding="utf-8").write(page(entry))

    before, after = patch_index()
    print("rag pages written     : %d" % len(ENTRIES))
    print("gen-ai catalog        : %d -> %d entries" % (before, after))
    return 0


if __name__ == "__main__":
    sys.exit(main())
