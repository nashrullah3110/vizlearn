# -*- coding: utf-8 -*-
"""The page shape shared by the generated question/topic tracks.

/interview/ and the generated gen_ai/ pages are the same document: a title and
a short answer, a step-through visualisation, the long-form article, and the
editor from /python-lab/ with something runnable in it. Only the track and the
tag row differ, so the markup lives here rather than in two builders that would
drift the first time one of them was fixed.

Callers supply an entry dict - see tools/interview.py for the fields - plus the
track key from lib_pages.TOPICS and the directory it is written into.
"""

import html
import json

import lib_codelab as codelab
import lib_shell as shell
from lib_pages import TOPICS, last_modified, pretty_date

PREFIX = "../"

CSS = """
        .vz-iq-lead {
            font-size: 1rem;
            line-height: 1.75;
            color: var(--text-muted);
            max-width: 68ch;
            margin-top: 0.9rem;
        }
        .vz-iq-lead strong { color: var(--text-main); }
        .vz-iq-lead code {
            font-family: 'JetBrains Mono', ui-monospace, monospace;
            font-size: 0.85em;
            background: var(--input-bg);
            border: 1px solid var(--border-subtle);
            border-radius: 4px;
            padding: 0.05em 0.3em;
            color: var(--text-main);
        }
        .vz-iq-tags { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.9rem; }
        .vz-iq-tag {
            font-family: 'JetBrains Mono', ui-monospace, monospace;
            font-size: 0.64rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            border: 1px solid var(--border-subtle);
            color: var(--text-muted);
        }
        .vz-iq-tag-hard { color: var(--accent-primary); border-color: var(--accent-primary); }

        .vz-iq-grid { display: grid; gap: 1.25rem; grid-template-columns: 1fr; }
        @media (min-width: 1024px) {
            .vz-iq-grid { grid-template-columns: minmax(0, 1fr) 20rem; align-items: start; }
        }
        .vz-iq-note {
            border: 1px solid var(--border-subtle);
            border-radius: 0.9rem;
            background: var(--card-bg);
            padding: 1rem 1.1rem;
        }
        .vz-iq-note h3 {
            font-family: 'JetBrains Mono', ui-monospace, monospace;
            font-size: 0.68rem; font-weight: 700;
            letter-spacing: 0.16em; text-transform: uppercase;
            color: var(--accent-primary); margin-bottom: 0.7rem;
        }
        .vz-iq-note p, .vz-iq-note li {
            font-size: 0.84rem; line-height: 1.65; color: var(--text-muted);
        }
        .vz-iq-note ul { list-style: disc; padding-left: 1.15rem; display: grid; gap: 0.45rem; }
        .vz-iq-note + .vz-iq-note { margin-top: 1rem; }
        .vz-iq-note code {
            font-family: 'JetBrains Mono', ui-monospace, monospace;
            font-size: 0.82em; color: var(--text-main);
            font-variant-ligatures: none;
        }
        .vz-iq-note strong { color: var(--text-main); }
"""

EYE = ('<svg class="vz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
       'aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z"/>'
       '<circle cx="12" cy="12" r="3"/></svg>')


def rel_for(q, directory):
    return "%s/%s.html" % (directory, q["slug"])


# --------------------------------------------------------------------------
# Page pieces
# --------------------------------------------------------------------------

def tags(q, group_label):
    out = []
    if group_label:
        out.append('<span class="vz-iq-tag">%s</span>' % html.escape(group_label))
    kind = q.get("kind")
    if kind:
        out.append('<span class="vz-iq-tag">%s</span>'
                   % ("Coding problem" if kind == "coding" else "Conceptual"))
    level = q.get("level")
    if level:
        out.append('<span class="vz-iq-tag%s">%s</span>'
                   % (" vz-iq-tag-hard" if level == "Hard" else "", html.escape(level)))
    return '<div class="vz-iq-tags">%s</div>' % "".join(out)


def visual(q):
    """The step player, plus the panel that says what to watch for."""
    data = json.dumps(q["viz"], ensure_ascii=False, separators=(",", ":"))
    if "</script" in data.lower():
        raise ValueError("%s: frame data contains a closing script tag" % q["slug"])

    notice = "".join("<li>%s</li>" % n for n in q.get("notice", []))
    notice_block = ('<section class="vz-iq-note"><h3>What to watch</h3>'
                    '<ul>%s</ul></section>' % notice) if notice else ""

    # Its own class rather than .vz-codelab, which it originally borrowed for
    # the sizing. Sharing the class meant `document.querySelector('.vz-codelab')`
    # found the visualisation instead of the editor - harmless on the page and
    # confusing for anything scripting it.
    return """
        <section class="vz-ivsec" aria-labelledby="vz-iq-viz-h">
            <div class="vz-section-head">%(eye)s<h2 id="vz-iq-viz-h">Step through it</h2>
            <span class="vz-rule"></span></div>
            <div class="vz-iq-grid">
                <div class="vz-iv" data-vz-iv tabindex="0" aria-label="Step-through visualisation">
                    <script type="application/json" class="vz-iv-data">%(data)s</script>
                    <div class="vz-iv-panel">
                        <div class="vz-iv-stage"></div>
                        <div class="vz-iv-reads"></div>
                        <p class="vz-iv-caption" aria-live="polite"></p>
                        <input class="vz-iv-scrub" type="range" min="0" value="0"
                               aria-label="Step position">
                        <div class="vz-iv-controls">
                            <button type="button" class="vz-iv-btn vz-iv-back">Back</button>
                            <button type="button" class="vz-iv-btn vz-iv-btn-primary vz-iv-step">Step</button>
                            <button type="button" class="vz-iv-btn vz-iv-play"
                                    aria-pressed="false">Auto-run</button>
                            <button type="button" class="vz-iv-btn vz-iv-reset">Reset</button>
                            <span class="vz-iv-count"></span>
                        </div>
                    </div>
                </div>
                <div>%(notice)s%(answer)s</div>
            </div>
        </section>
""" % {"eye": EYE, "data": data, "notice": notice_block,
       "answer": '<section class="vz-iq-note"><h3>Say this out loud</h3><p>%s</p></section>'
                 % q["say"] if q.get("say") else ""}


def article(q):
    body = []
    for heading, text in q["sections"]:
        body.append("<div><h3>%s</h3>%s</div>" % (html.escape(heading), text))

    return """
    <!-- auto-article-vizlearn -->
    <section class="px-4 md:px-8 pb-8 max-w-[1600px] mx-auto w-full" data-vz-prose>
        <div class="card-container animate-fade-in">
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
""" % {"title": html.escape(q["title"]), "sub": html.escape(q["asked"]),
       "body": "\n                ".join(body)}


def page(q, track_key, directory, group_label=""):
    rel = rel_for(q, directory)
    iso = last_modified(rel)
    head = shell.head_top("%s | VizLearn" % q["title"], PREFIX).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        CSS.strip("\n"))

    main = """
    <main class="flex-1 p-4 md:p-8 max-w-[1600px] mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="vz-iq-lead">%(lead)s</p>
            %(tags)s
        </div>
%(visual)s
    </main>
%(article)s
%(code)s
""" % {
        "crumb": shell.breadcrumb_bar([
            ("Home", PREFIX + "index.html"),
            (TOPICS[track_key]["title"], PREFIX + directory + "/"),
            (q["title"], None)]),
        "title": html.escape(q["title"]),
        "lead": q["lead"],
        "tags": tags(q, group_label),
        "visual": visual(q),
        "article": article(q),
        "code": codelab.section(q["code"], PREFIX, q["code"]["intro"]),
    }

    # `iso` is read here rather than left to build_seo so a page that has not
    # changed keeps its date across rebuilds.
    assert iso and pretty_date(iso)
    return head + shell.header(PREFIX) + main + shell.close(PREFIX)


