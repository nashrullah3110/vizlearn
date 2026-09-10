#!/usr/bin/env python3
"""Render the async-programming pages.

Unlike the numpy/pandas builders, this one does NOT own the prose: the articles
live in content/articles/async_python/*.txt and are the source, injected by
build_articles.py into the auto-article mount below. This script only writes the
page shells and keeps the catalog entry in index.html in step. Editors come from
the ```python-run fences via tools/prose.py + runnable_specs["async_python"].

    python3 tools/build_async_topics.py

Requires courseData in index.html to already have an "async_python" topic.
"""
import html
import io
import json
import os
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data

PREFIX = "../"
DIR = "async_python"
TOPIC_KEY = "async_python"
CRUMB = "Async Python"

# slug, category (breadcrumb leaf / grouping), and the hub card icon. Order here
# is the learning order; reorder to change prev/next.
TOPICS = [
    {"slug": "event_loop_stepped_through", "cat": "Foundations",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><circle cx="80" cy="45" r="26" fill="none" stroke="var(--accent-primary)" stroke-width="4"/><path d="M80 19 l7 -6 l-1 12 z" fill="var(--accent-primary)"/><circle cx="80" cy="45" r="5" fill="var(--text-main)"/></svg>'},
    {"slug": "coroutines_tasks_and_await", "cat": "Foundations",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><rect x="24" y="30" width="40" height="12" rx="3" fill="var(--accent-primary)" opacity="0.9"/><rect x="72" y="30" width="16" height="12" rx="3" fill="var(--bg-surface)" stroke="var(--border-subtle)" stroke-width="2"/><rect x="96" y="30" width="40" height="12" rx="3" fill="var(--accent-primary)" opacity="0.9"/><rect x="24" y="52" width="112" height="12" rx="3" fill="var(--border-subtle)" opacity="0.5"/></svg>'},
    {"slug": "running_work_concurrently", "cat": "Running work",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><rect x="20" y="24" width="70" height="10" rx="3" fill="var(--accent-primary)"/><rect x="20" y="40" width="55" height="10" rx="3" fill="var(--accent-primary)" opacity="0.8"/><rect x="20" y="56" width="40" height="10" rx="3" fill="var(--accent-primary)" opacity="0.6"/><line x1="100" y1="18" x2="100" y2="72" stroke="var(--text-main)" stroke-width="2" stroke-dasharray="4 4"/></svg>'},
    {"slug": "the_blocking_call_that_freezes_the_loop", "cat": "Pitfalls",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><rect x="20" y="38" width="120" height="14" rx="3" fill="var(--border-subtle)" opacity="0.5"/><rect x="70" y="26" width="20" height="38" rx="3" fill="var(--accent-primary)"/><line x1="70" y1="26" x2="90" y2="64" stroke="var(--bg-surface)" stroke-width="3"/></svg>'},
    {"slug": "queues_and_backpressure", "cat": "Patterns",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><rect x="30" y="34" width="22" height="22" rx="3" fill="var(--accent-primary)"/><rect x="58" y="34" width="22" height="22" rx="3" fill="var(--accent-primary)" opacity="0.7"/><rect x="86" y="34" width="22" height="22" rx="3" fill="none" stroke="var(--border-subtle)" stroke-width="2"/><path d="M116 45 l14 0 m-6 -5 l6 5 l-6 5" fill="none" stroke="var(--text-main)" stroke-width="2"/></svg>'},
]


def rel_for(t):
    return "%s/%s.html" % (DIR, t["slug"])


def esc(s):
    return html.escape(s, quote=False)


def _title_lead(slug):
    p = os.path.join(ROOT, "content", "articles", DIR, slug + ".txt")
    title = lead = ""
    for line in io.open(p, encoding="utf-8"):
        if line.startswith("title:") and not title:
            title = line[6:].strip()
        elif line.startswith("intro:") and not lead:
            lead = line[6:].strip()
        if title and lead:
            break
    return title, lead


def page(t):
    title, lead = _title_lead(t["slug"])
    head = shell.head_top("%s | VizLearn" % title, PREFIX)
    main = """
    <main class="flex-1 p-4 md:p-8 max-w-[1600px] mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="vz-pt-lead" style="margin-top:0.5rem;max-width:60ch;color:var(--text-muted)">%(lead)s</p>
        </div>
    </main>
""" % {
        "crumb": shell.breadcrumb_bar([("Home", PREFIX + "index.html"),
                                       (CRUMB, PREFIX + DIR + "/"),
                                       (t["cat"], None)]),
        "title": esc(title),
        "lead": esc(lead),
    }
    mount = """    <!-- auto-article-vizlearn -->
    <section class="px-4 md:px-8 pb-8 max-w-[1600px] mx-auto w-full" data-vz-prose>
        <div class="card-container animate-fade-in">
        </div>
    </section>
"""
    return head + shell.header(PREFIX) + main + mount + shell.close(PREFIX)


def catalog_entry(existing):
    generated = {rel_for(t): {"title": _title_lead(t["slug"])[0],
                              "path": rel_for(t), "svg": t["svg"]}
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
        io.open(os.path.join(ROOT, rel_for(t)), "w", encoding="utf-8").write(page(t))

    index = os.path.join(ROOT, "index.html")
    src = io.open(index, encoding="utf-8").read()
    data, start, end = read_course_data(index)
    if TOPIC_KEY not in data:
        # Self-contained: create the track entry rather than requiring a manual
        # index.html edit first, so a fresh checkout builds without a prep step.
        data[TOPIC_KEY] = {"title": "Async Python", "courses": []}
    data[TOPIC_KEY], added = catalog_entry(data[TOPIC_KEY])
    block = json.dumps(data, indent=4, ensure_ascii=False)
    io.open(index, "w", encoding="utf-8").write(src[:start] + block + src[end:])

    print("async pages written : %d" % len(TOPICS))
    print("catalog             : %d added, %d total"
          % (added, len(data[TOPIC_KEY]["courses"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
