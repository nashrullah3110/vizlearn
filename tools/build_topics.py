#!/usr/bin/env python3
"""One landing page per track, at /<dir>/.

Before this, a track only existed as `index.html#ml`. A fragment is not a URL:
Google saw eight tracks collapsed into one page, so nothing on the site could
rank for "machine learning visualization" or "algorithm visualizer" except the
hub, competing with itself.

Each generated page carries the track's own copy, the full ordered module list
as real anchors, and CollectionPage + ItemList structured data. Written whole
on every build - these files have no hand-edited regions.
"""

import html
import os
import sys

import lib_shell as shell
from lib_catalog import ROOT, by_topic
from lib_pages import TOPICS, TOPIC_ORDER, last_modified, pretty_date, topic_rel

PREFIX = "../"


def card(mod):
    art = mod["svg"].strip()
    if art.startswith("<svg") and "xmlns=" not in art:
        art = art.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    return (
        '<li class="vz-tcard-wrap">'
        '<a class="vz-tcard" href="%s%s" data-vz-path="%s">'
        '<span class="vz-tcard-art">%s</span>'
        '<span class="vz-tcard-body">'
        '<span class="vz-tcard-step">%02d</span>'
        '<span class="vz-tcard-title">%s</span>'
        '<span class="vz-tcard-desc">%s</span>'
        "</span></a></li>"
        % (PREFIX, mod["path"], html.escape(mod["path"]), art,
           mod["index"] + 1, html.escape(mod["title"]),
           html.escape(mod["desc"] or ""))
    )


def other_tracks(key):
    out = []
    for k in TOPIC_ORDER:
        if k == key:
            continue
        out.append('<a class="vz-chip" href="%s%s/">%s</a>'
                   % (PREFIX, TOPICS[k]["dir"], html.escape(TOPICS[k]["title"])))
    return "".join(out)


def build(key, mods):
    t = TOPICS[key]
    rel = topic_rel(key)
    title = "%s - Interactive Visualizations | VizLearn" % t["title"]

    intro = "".join('<p>%s</p>' % html.escape(p) for p in t["intro"])
    first = mods[0]

    parts = [shell.head_top(title, PREFIX), shell.header(PREFIX)]

    parts.append("""
    <main class="flex-1 p-4 md:p-8 max-w-7xl mx-auto w-full">

        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-5xl font-bold brand-font tracking-tight" style="color: var(--text-main)">%(h1)s</h1>
            <p class="mt-3 max-w-3xl text-base md:text-lg" style="color: var(--text-muted)">%(lead)s</p>
            <div class="vz-topic-meta">
                <span><strong>%(count)d</strong> modules</span>
                <span>Free, no login</span>
                <span>Updated %(updated)s</span>
            </div>
            <div class="vz-topic-cta">
                <a class="vz-btn vz-btn-primary" href="%(p)s%(firstpath)s">Start with %(firsttitle)s</a>
            </div>
        </div>

        <section class="vz-topic-intro" aria-labelledby="vz-about-h">
            <h2 id="vz-about-h">About this track</h2>
            %(intro)s
        </section>

        <section class="vz-topic-list" aria-labelledby="vz-mods-h">
            <div class="vz-section-head">
                <h2 id="vz-mods-h">All %(count)d modules, in teaching order</h2>
                <span class="vz-rule"></span>
            </div>
            <ol class="vz-tgrid">%(cards)s</ol>
        </section>

        <section class="vz-topic-more" aria-labelledby="vz-more-h">
            <h2 id="vz-more-h">Other tracks</h2>
            <div class="vz-chips">%(others)s</div>
        </section>

    </main>
""" % {
        "crumb": shell.breadcrumb_bar([("Home", PREFIX + "index.html"), (t["title"], None)]),
        "h1": html.escape(t["h1"]),
        "lead": html.escape(t["lead"]),
        "count": len(mods),
        "updated": pretty_date(last_modified(rel)),
        "p": PREFIX,
        "firstpath": first["path"],
        "firsttitle": html.escape(first["title"]),
        "intro": intro,
        "cards": "".join(card(m) for m in mods),
        "others": other_tracks(key),
    })

    parts.append(shell.close(PREFIX))
    return "".join(parts)


def main():
    groups = by_topic()
    written = 0
    for key in TOPIC_ORDER:
        mods = groups.get(key)
        if not mods:
            print("  !! no modules for topic %s" % key)
            continue
        rel = topic_rel(key)
        path = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(build(key, mods))
        written += 1
    print("topic landing pages : %d" % written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
