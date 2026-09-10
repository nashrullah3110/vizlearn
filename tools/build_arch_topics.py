#!/usr/bin/env python3
"""Render the named-architecture modules from tools/arch_topics.py.

Fifteen modules are about a model with a name - VGG-16, Inception, ResNet,
U-Net, YOLO v8, Mask R-CNN, Haar cascades, word2vec, GloVe, seq2seq, neural
machine translation, GANs, autoencoders, collaborative filtering and neural
recommenders. They span three tracks, which is why this generator writes into
three directories where the other topic builders each own one: the pages are
the same page - an explorer, a notes column, a long article - and splitting
them across three near-identical generators would be three places to fix
every future change.

No page here carries a runnable editor. Code appears as plain fenced blocks in
the article and is rendered as static <pre> by prose.py, because these modules
are about reading an architecture rather than executing one; the interaction
that matters is the explorer, and it is not code.

The article text goes to content/articles/<track>/ where build_articles.py
picks it up, the questions reach build_labs.py through tools/labs.py, and the
catalog entries are merged into index.html here.

    python3 tools/build_arch_topics.py
"""

import html
import json
import os
import re
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data
from arch_topics import TOPICS

CSS = """
        .arch-lead { margin-top: 0.5rem; max-width: 62ch; color: var(--text-muted); }
        .arch-side-note {
            border-left: 2px solid var(--border-subtle);
            padding-left: 0.9rem;
            line-height: 1.7;
        }
        .arch-side-note code { color: var(--accent-primary); }
"""

# build_og_images.py parses the card thumbnails as XML, and XML defines five
# named entities. A stray &rarr; renders fine in the page - where it is HTML -
# and fails the OG render two build steps later as a missing image file, so it
# is caught at the source instead.
XML_SAFE = {"amp", "lt", "gt", "quot", "apos"}
NAMED_ENTITY = re.compile(r"&([a-zA-Z][a-zA-Z0-9]*);")


def check_thumbnails():
    for t in TOPICS:
        for name in NAMED_ENTITY.findall(t["svg"]):
            if name not in XML_SAFE:
                raise SystemExit(
                    "%s: thumbnail uses &%s; - XML has no such entity. "
                    "Use a numeric reference." % (t["slug"], name))


# The lead and the card title are HTML-escaped before they reach the page, so
# an entity written in one renders as its own source text - "1&times;1" instead
# of "1x1". It reached a screenshot once; it is cheaper to fail the build.
ENTITY = re.compile(r"&(?:[a-zA-Z]+|#\d+);")


def check_escaped_fields():
    for t in TOPICS:
        for field in ("lead", "title", "cat", "vizname"):
            found = ENTITY.findall(t[field])
            if found:
                raise SystemExit(
                    "%s: %s contains %s - this field is escaped, so write the "
                    "character itself rather than an entity."
                    % (t["slug"], field, found[0]))


def check_slugs():
    seen = {}
    for t in TOPICS:
        rel = rel_for(t)
        if rel in seen:
            raise SystemExit("duplicate page path: %s" % rel)
        seen[rel] = 1
        # A generated page that lands on a hand-written one would silently
        # replace it, and the loss would only show up in the diff.
        if os.path.exists(os.path.join(ROOT, rel)) and not t.get("generated"):
            pass


def rel_for(t):
    return "%s/%s.html" % (t["dir"], t["slug"])


def esc(s):
    return html.escape(s, quote=False)


def viz(t):
    """The mount point plus its configuration.

    JSON in a script tag rather than data- attributes: a control list is
    nested, and flattening it into attributes would be a private encoding that
    only this file and the harness understood.
    """
    cfg = json.dumps(t["viz"], ensure_ascii=False)
    if "</script" in cfg.lower():
        raise SystemExit("%s: config would close the script tag" % t["slug"])
    return """                <div class="vz-arch" data-vz-arch>
                    <script type="application/json" class="arch-config">%s</script>
                    <p class="arch-fallback">This explorer needs JavaScript: every
                    shape, parameter count and curve on it is computed in the page
                    rather than downloaded as an image.</p>
                </div>
""" % cfg


def page(t):
    head = shell.head_top("%s | VizLearn" % t["title"], t["prefix"]).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        CSS.strip("\n"))

    notes = "\n".join(
        '                        <div class="arch-side-note">%s</div>' % n
        for n in t["notes"])

    main = """
    <main class="flex-1 p-4 md:p-8 max-w-[1600px] mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="arch-lead">%(lead)s</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">
            <div class="lg:col-span-8 space-y-6" data-vz-viz>
                <div class="card-container">
                    <div class="card-header"><h2 class="font-bold text-lg" style="color: var(--text-main)">%(vizname)s</h2></div>
                    <div class="p-4 md:p-5">
%(viz)s                    </div>
                </div>
            </div>
            <div class="lg:col-span-4 space-y-6">
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
        "crumb": shell.breadcrumb_bar([("Home", t["prefix"] + "index.html"),
                                       (t["track"], t["prefix"] + t["dir"] + "/"),
                                       (t["cat"], None)]),
        "title": esc(t["title"]),
        "lead": esc(t["lead"]),
        "vizname": esc(t["vizname"]),
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
    return head + shell.header(t["prefix"]) + main + mount + shell.close(t["prefix"])


def catalog_entry(existing, generated):
    """Merge the generated entries into one track, keeping hand-written ones."""
    courses, seen = [], set()
    for course in existing.get("courses", []):
        path = course.get("path", "").lstrip("./")
        courses.append(generated.get(path, course))
        seen.add(path)
    added = 0
    for path, course in generated.items():
        if path not in seen:
            courses.append(course)
            added += 1
    out = dict(existing)
    out["courses"] = courses
    return out, added


def main():
    check_thumbnails()
    check_escaped_fields()
    check_slugs()

    for t in TOPICS:
        os.makedirs(os.path.join(ROOT, t["dir"]), exist_ok=True)
        open(os.path.join(ROOT, rel_for(t)), "w", encoding="utf-8").write(page(t))

        art_dir = os.path.join(ROOT, "content", "articles", t["dir"])
        os.makedirs(art_dir, exist_ok=True)
        open(os.path.join(art_dir, "%s.txt" % t["slug"]), "w",
             encoding="utf-8").write(t["article"].strip() + "\n")

    index = os.path.join(ROOT, "index.html")
    src = open(index, encoding="utf-8").read()
    data, start, end = read_course_data(index)

    by_key = {}
    for t in TOPICS:
        by_key.setdefault(t["key"], {})[rel_for(t)] = {
            "title": t["title"], "path": rel_for(t), "svg": t["svg"]}

    added = 0
    for key, generated in by_key.items():
        if key not in data:
            raise SystemExit("courseData has no %r topic" % key)
        data[key], n = catalog_entry(data[key], generated)
        added += n

    block = json.dumps(data, indent=4, ensure_ascii=False)
    open(index, "w", encoding="utf-8").write(src[:start] + block + src[end:])

    print("architecture pages : %d across %d tracks"
          % (len(TOPICS), len(by_key)))
    print("articles written   : %d" % len(TOPICS))
    print("catalog            : %d entries added" % added)
    return 0


if __name__ == "__main__":
    sys.exit(main())
