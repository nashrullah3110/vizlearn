#!/usr/bin/env python3
"""Render the threads-and-processes pages.

Like build_async_topics.py, this builder does NOT own the prose: the articles
live in content/articles/concurrency/*.txt and are the source, injected by
build_articles.py into the auto-article mount below. This script writes the
page shells, mounts one explorer per page, and keeps the courseData entry in
index.html in step. Editors come from the ```python-run fences via
tools/prose.py plus runnable_specs["concurrency"].

    python3 tools/build_concurrency_topics.py

A note that belongs with the track rather than any one page: the browser
interpreter these editors run in has no OS threads, so Thread.start(),
ThreadPoolExecutor, multiprocessing and os.fork all raise. Every runnable
block here therefore demonstrates a *mechanism* that is real single-threaded -
the bytecode an increment compiles to, the lock protocol, the pickle boundary,
the Future state machine - and anything that needs a second thread is shown as
a static block with its output, the way the async track already shows
asyncio.to_thread.
"""
import html
import io
import json
import os
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data

PREFIX = "../"
DIR = "concurrency"
TOPIC_KEY = "concurrency"
CRUMB = "Concurrency"

TOPICS = [
    {"slug": "the_gil_and_what_it_locks", "cat": "The mechanism",
     "widget": "gil", "vizname": "Two threads, one lock on the interpreter",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><rect x="20" y="24" width="54" height="12" rx="3" fill="var(--accent-primary)"/><rect x="86" y="24" width="54" height="12" rx="3" fill="var(--border-subtle)" opacity="0.5"/><rect x="20" y="46" width="54" height="12" rx="3" fill="var(--border-subtle)" opacity="0.5"/><rect x="86" y="46" width="54" height="12" rx="3" fill="var(--accent-primary)"/><rect x="70" y="66" width="20" height="14" rx="3" fill="none" stroke="var(--text-main)" stroke-width="2"/><path d="M75 66 v-5 a5 5 0 0 1 10 0 v5" fill="none" stroke="var(--text-main)" stroke-width="2"/></svg>'},
    {"slug": "race_conditions_in_python", "cat": "The mechanism",
     "widget": "race", "vizname": "Where the switch lands, and what it costs",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><rect x="18" y="30" width="30" height="12" rx="3" fill="var(--accent-primary)" opacity="0.85"/><rect x="52" y="30" width="30" height="12" rx="3" fill="var(--accent-primary)" opacity="0.6"/><rect x="86" y="30" width="30" height="12" rx="3" fill="var(--accent-primary)" opacity="0.35"/><line x1="84" y1="22" x2="84" y2="66" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 3"/><text x="30" y="60" font-size="9" font-family="monospace" fill="var(--text-muted)">read</text><text x="96" y="60" font-size="9" font-family="monospace" fill="#dc2626">write</text></svg>'},
    {"slug": "locks_and_the_ways_they_go_wrong", "cat": "The mechanism",
     "widget": "deadlock", "vizname": "Two locks, two orders, one deadlock",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><circle cx="48" cy="32" r="13" fill="none" stroke="var(--accent-primary)" stroke-width="3"/><circle cx="112" cy="58" r="13" fill="none" stroke="var(--accent-primary)" stroke-width="3"/><path d="M60 38 L100 52" stroke="var(--text-main)" stroke-width="2"/><path d="M100 46 L60 52" stroke="#dc2626" stroke-width="2" stroke-dasharray="4 3"/></svg>'},
    {"slug": "threads_or_processes", "cat": "The tools",
     "widget": "boundary", "vizname": "What crossing a process boundary costs",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><rect x="16" y="22" width="48" height="46" rx="5" fill="var(--accent-primary)" opacity="0.2" stroke="var(--accent-primary)" stroke-width="2"/><rect x="96" y="22" width="48" height="46" rx="5" fill="none" stroke="var(--border-subtle)" stroke-width="2" stroke-dasharray="4 3"/><path d="M68 45 h24 m-7 -5 l7 5 l-7 5" fill="none" stroke="var(--text-main)" stroke-width="2"/><text x="80" y="80" text-anchor="middle" font-size="8" font-family="monospace" fill="var(--text-muted)">pickle</text></svg>'},
    {"slug": "concurrent_futures", "cat": "The tools",
     "widget": "future", "vizname": "A Future, through its four states",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><rect x="14" y="34" width="30" height="18" rx="4" fill="none" stroke="var(--border-subtle)" stroke-width="2"/><rect x="56" y="34" width="30" height="18" rx="4" fill="var(--accent-primary)" opacity="0.5"/><rect x="98" y="34" width="30" height="18" rx="4" fill="var(--accent-primary)"/><path d="M46 43 h8 M88 43 h8" stroke="var(--text-main)" stroke-width="2"/><text x="129" y="66" text-anchor="end" font-size="8" font-family="monospace" fill="var(--text-muted)">result</text></svg>'},
    {"slug": "queues_between_threads", "cat": "The practice",
     "widget": "tqueue", "vizname": "Queue depth, and where put() blocks",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><rect x="28" y="36" width="20" height="20" rx="3" fill="var(--accent-primary)"/><rect x="54" y="36" width="20" height="20" rx="3" fill="var(--accent-primary)" opacity="0.7"/><rect x="80" y="36" width="20" height="20" rx="3" fill="none" stroke="var(--border-subtle)" stroke-width="2"/><path d="M110 46 h16 m-7 -5 l7 5 l-7 5" fill="none" stroke="var(--text-main)" stroke-width="2"/><line x1="104" y1="28" x2="104" y2="64" stroke="#dc2626" stroke-width="2" stroke-dasharray="3 3"/></svg>'},
    {"slug": "choosing_threads_processes_or_async", "cat": "The practice",
     "widget": "speedup", "vizname": "Speed-up against workers, three ways",
     "svg": '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full"><path d="M20 70 L60 40 L100 26 L140 20" fill="none" stroke="var(--accent-primary)" stroke-width="2.5"/><path d="M20 70 L60 58 L100 52 L140 50" fill="none" stroke="var(--text-muted)" stroke-width="2" stroke-dasharray="4 3"/><path d="M20 70 h120" stroke="var(--border-subtle)" stroke-width="1.5"/></svg>'},
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
    viz = """
    <section class="px-4 md:px-8 pb-2 max-w-[1600px] mx-auto w-full">
        <div class="card-container animate-fade-in" data-vz-viz>
            <div class="card-header"><h2 class="font-bold text-lg" style="color: var(--text-main)">%(vizname)s</h2></div>
            <div class="p-4 md:p-5">
                <div class="vz-cc" data-vz-con>
                    <script type="application/json" class="cc-config">%(cfg)s</script>
                    <p class="vz-cc-fallback">This explorer needs JavaScript: every
                    interleaving, cost and speed-up on it is computed in the page
                    rather than downloaded as an image.</p>
                </div>
            </div>
        </div>
    </section>
""" % {"vizname": esc(t["vizname"]),
       "cfg": json.dumps({"widget": t["widget"]}, ensure_ascii=False)}
    mount = """    <!-- auto-article-vizlearn -->
    <section class="px-4 md:px-8 pb-8 max-w-[1600px] mx-auto w-full" data-vz-prose>
        <div class="card-container animate-fade-in">
        </div>
    </section>
"""
    return (head + shell.header(PREFIX) + main + viz + mount
            + shell.close(PREFIX))


def catalog_entry(existing):
    generated = {rel_for(t): {"title": _title_lead(t["slug"])[0],
                              "path": rel_for(t), "svg": t["svg"]}
                 for t in TOPICS}
    courses, seen = [], set()
    for course in existing.get("courses", []):
        path = course.get("path", "").lstrip("./")
        courses.append(generated.get(path, course))
        seen.add(path)
    # Keep the declared order for anything new, rather than dict order.
    for t in TOPICS:
        if rel_for(t) not in seen:
            courses.append(generated[rel_for(t)])
    out = dict(existing)
    out["courses"] = courses
    return out, len([t for t in TOPICS if rel_for(t) not in seen])


def main():
    os.makedirs(os.path.join(ROOT, DIR), exist_ok=True)
    for t in TOPICS:
        io.open(os.path.join(ROOT, rel_for(t)), "w",
                encoding="utf-8").write(page(t))

    index = os.path.join(ROOT, "index.html")
    src = io.open(index, encoding="utf-8").read()
    data, start, end = read_course_data(index)
    if TOPIC_KEY not in data:
        data[TOPIC_KEY] = {"title": "Concurrency", "courses": []}
    data[TOPIC_KEY], added = catalog_entry(data[TOPIC_KEY])
    block = json.dumps(data, indent=4, ensure_ascii=False)
    io.open(index, "w", encoding="utf-8").write(src[:start] + block + src[end:])

    print("concurrency pages : %d" % len(TOPICS))
    print("catalog           : %d added, %d total"
          % (added, len(data[TOPIC_KEY]["courses"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
