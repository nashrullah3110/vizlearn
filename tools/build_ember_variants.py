#!/usr/bin/env python3
"""Write one preview of the hub per Ember design variant.

index.html is read and never written. Each preview is that file plus:

  * the variant's palette and design CSS, appended before </head> so it wins
    on document order rather than on !important
  * four new sections between the intro band and the track rails, and a
    closing call to action above the footer

The sections are the same words in every variant - only the design moves, so
what is being compared is the design. Their numbers come from the catalog, so
a preview cannot quietly claim a module count the site does not have, and
every link in them points at a page that exists.

    python3 tools/build_ember_variants.py
    python3 tools/build_ember_variants.py --clean
"""

import html
import os
import sys

from ember_variants import VARIANTS
from lib_catalog import DIR_META, counts, modules
from theme_previews import css as palette_css

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
MARK = "<!-- VIZLEARN:EMBER-VARIANT -->"

# Anchors in index.html. Both are plain markup that has been stable across
# every build; if either moves, this fails loudly rather than writing a
# preview with the sections silently missing.
ANCHOR_SECTIONS = '<main id="course-container"'
ANCHOR_CTA = '<footer class="vz-footer"'


def track_data():
    """Every track with its real module count, largest first."""
    mods = modules()
    seen, order = {}, []
    for m in mods:
        if m["dir"] not in seen:
            seen[m["dir"]] = {"dir": m["dir"], "label": DIR_META.get(m["dir"], (m["dir"],))[0],
                              "n": 0, "first": m["path"]}
            order.append(seen[m["dir"]])
        seen[m["dir"]]["n"] += 1
    return sorted(order, key=lambda t: -t["n"])


def esc(s):
    return html.escape(str(s))


def how_it_works():
    steps = [
        ("Pick the idea, not the chapter",
         "Every module is one concept with one visualisation. There is no "
         "chapter to finish before it makes sense, and no order you have to "
         "arrive in."),
        ("Drive it until it breaks",
         "The controls are the point. Set k to 1 and watch KNN overfit, push "
         "the learning rate until descent diverges. Understanding usually "
         "arrives at the failure, not the happy path."),
        ("Read the code that did it",
         "Where it helps, the same page carries a Python editor running the "
         "real thing in your browser. Change a line, run it, see the output "
         "move."),
    ]
    out = ['<section class="vzx-sec" aria-labelledby="vzx-how-h"><div class="vzx-wrap">',
           '<p class="vzx-kicker">How it works</p>',
           '<h2 class="vzx-h" id="vzx-how-h">Three steps, then you are just using it</h2>',
           '<p class="vzx-sub">No account, no install, nothing gated. Open a '
           'page and it runs.</p>',
           '<div class="vzx-steps">']
    for i, (title, body) in enumerate(steps, 1):
        out.append(
            '<div class="vzx-step"><div class="vzx-step-n">%d</div>'
            '<div><h3 class="vzx-step-h">%s</h3><p class="vzx-step-p">%s</p></div></div>'
            % (i, esc(title), esc(body)))
    out.append("</div></div></section>")
    return "".join(out)


def tracks_section(tracks, n_mods, n_tracks):
    top = tracks[0]["n"]
    rows = []
    for i, t in enumerate(tracks, 1):
        rows.append(
            '<a class="vzx-track-row" href="%s/">'
            '<span class="vzx-track-n">%02d</span>'
            '<span class="vzx-track-name">%s</span>'
            '<span class="vzx-bar"><span style="width:%.1f%%"></span></span>'
            '<span class="vzx-track-count">%d</span></a>'
            % (esc(t["dir"]), i, esc(t["label"]), 100.0 * t["n"] / top, t["n"]))
    return (
        '<section class="vzx-sec" aria-labelledby="vzx-tracks-h"><div class="vzx-wrap">'
        '<p class="vzx-kicker">Every track</p>'
        '<h2 class="vzx-h" id="vzx-tracks-h">%d modules across %d tracks</h2>'
        '<p class="vzx-sub">Each track is a sequence: every module leans only '
        'on the ones above it, so you can start at the top or drop in where '
        'you already are.</p>'
        '<div class="vzx-tracks">%s</div></div></section>'
        % (n_mods, n_tracks, "".join(rows)))


def start_here(tracks):
    """First module of a handful of tracks - real pages, in teaching order."""
    want = ["python", "maths", "dsa", "machine_learning", "gen_ai", "interview"]
    by = {t["dir"]: t for t in tracks}
    cards = []
    for d in want:
        t = by.get(d)
        if not t:
            continue
        cards.append(
            '<a class="vzx-panel vzx-start-card" href="%s">'
            '<span class="vzx-start-track">%s</span>'
            '<span class="vzx-start-title">%s</span>'
            '<span class="vzx-start-go">Start the track &rarr;</span></a>'
            % (esc(t["first"]), esc(t["label"]),
               esc(t["first"].split("/")[-1].replace(".html", "").replace("_", " ").replace("-", " ").title())))
    return (
        '<section class="vzx-sec" aria-labelledby="vzx-start-h"><div class="vzx-wrap">'
        '<p class="vzx-kicker">Start here</p>'
        '<h2 class="vzx-h" id="vzx-start-h">The first page of six tracks</h2>'
        '<p class="vzx-sub">Each of these is the opening module of its track - '
        'the one that assumes the least.</p>'
        '<div class="vzx-start">%s</div></div></section>' % "".join(cards))


def faq():
    qs = [
        ("Is it actually free?",
         "Yes, and there is nothing to sign up for. No account, no trial, no "
         "email wall."),
        ("Does the Python really run?",
         "It runs CPython compiled to WebAssembly, in a worker thread in your "
         "browser. Nothing is uploaded and nothing is executed on a server."),
        ("Does it work offline?",
         "The site installs as an app and caches what you have opened, so "
         "pages you have already visited keep working without a connection."),
        ("Who is it for?",
         "Anyone who has read the definition and still cannot picture the "
         "thing. It assumes no maths degree and leaves nothing as an "
         "exercise for the reader."),
    ]
    items = "".join(
        '<div class="vzx-panel vzx-faq-item"><h3 class="vzx-faq-q">%s</h3>'
        '<p class="vzx-faq-a">%s</p></div>' % (esc(q), esc(a)) for q, a in qs)
    return (
        '<section class="vzx-sec" aria-labelledby="vzx-faq-h"><div class="vzx-wrap">'
        '<p class="vzx-kicker">Questions</p>'
        '<h2 class="vzx-h" id="vzx-faq-h">The ones worth answering up front</h2>'
        '<div class="vzx-faq">%s</div></div></section>' % items)


def cta(n_mods):
    return (
        '<section class="vzx-sec vzx-sec-cta"><div class="vzx-wrap">'
        '<div class="vzx-cta">'
        '<h2 class="vzx-h" style="margin-top:0">Open one and push a slider</h2>'
        '<p class="vzx-sub" style="margin:0 auto">That is the whole pitch. '
        '%d modules, all of them running the real computation, none of them '
        'asking you for anything first.</p>'
        '<div class="vzx-cta-row">'
        '<a class="vzx-btn vzx-btn-solid" href="dsa/big_o_notation.html">Start with Big-O</a>'
        '<a class="vzx-btn vzx-btn-ghost" href="map/">Browse the concept map</a>'
        '</div></div></div></section>' % n_mods)


# Layout for the new sections. Deliberately structural only - spacing, grid,
# flow. Every variant restyles the surface of these; none of them has to
# re-solve the layout.
BASE_CSS = """
    .vzx-wrap { width: 100%; max-width: var(--vz-page, 1600px); margin: 0 auto;
                padding-left: clamp(1rem, 4vw, 2.5rem); padding-right: clamp(1rem, 4vw, 2.5rem); }
    .vzx-steps { display: grid; gap: 2rem; margin-top: 2.5rem;
                 grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr)); }
    .vzx-step { display: flex; gap: 1rem; align-items: flex-start; }
    .vzx-step-h { font-weight: 700; margin: .15rem 0 .4rem; color: var(--text-main); font-size: 1.02rem; }
    .vzx-step-p { color: var(--text-muted); font-size: .93rem; line-height: 1.65; margin: 0; }

    .vzx-tracks { margin-top: 2rem; display: flex; flex-direction: column; }
    .vzx-track-row { display: grid; align-items: center; gap: 1rem; padding: .85rem .75rem;
                     text-decoration: none; color: inherit;
                     grid-template-columns: 2.5rem minmax(7rem, 12rem) 1fr auto;
                     transition: background .2s ease; }
    .vzx-track-n { color: var(--text-muted); font-family: ui-monospace, Menlo, monospace; font-size: .85rem; }
    .vzx-track-name { font-weight: 600; color: var(--text-main); }
    .vzx-bar { height: 7px; background: color-mix(in srgb, var(--text-muted) 18%, transparent);
               border-radius: 999px; overflow: hidden; }
    .vzx-bar span { display: block; height: 100%; background: var(--accent-primary); border-radius: 999px; }
    .vzx-track-count { font-family: ui-monospace, Menlo, monospace; color: var(--text-muted);
                       font-size: .85rem; min-width: 2.5rem; text-align: right; }

    .vzx-start { display: grid; gap: 1rem; margin-top: 2.5rem;
                 grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr)); }
    .vzx-start-card { display: flex; flex-direction: column; gap: .35rem; padding: 1.25rem;
                      text-decoration: none; color: inherit; }
    .vzx-start-track { font-size: .68rem; letter-spacing: .16em; text-transform: uppercase;
                       color: var(--accent-primary); font-weight: 700; }
    .vzx-start-title { font-weight: 700; color: var(--text-main); line-height: 1.3; }
    .vzx-start-go { margin-top: auto; padding-top: .6rem; font-size: .82rem; color: var(--text-muted); }

    .vzx-faq { display: grid; gap: 1rem; margin-top: 2.5rem;
               grid-template-columns: repeat(auto-fit, minmax(min(100%, 20rem), 1fr)); }
    .vzx-faq-item { padding: 1.35rem; }
    .vzx-faq-q { font-weight: 700; color: var(--text-main); margin: 0 0 .45rem; font-size: 1rem; }
    .vzx-faq-a { color: var(--text-muted); margin: 0; font-size: .92rem; line-height: 1.65; }

    .vzx-sec-cta { padding-bottom: 5rem; }
    .vzx-cta { padding: 2.5rem 2rem; text-align: center; }
    .vzx-cta .vzx-sub { margin-left: auto; margin-right: auto; }
    .vzx-cta-row { display: flex; gap: .75rem; justify-content: center; flex-wrap: wrap; margin-top: 1.75rem; }
    .vzx-btn { display: inline-flex; align-items: center; gap: .5rem; padding: .7rem 1.4rem;
               border-radius: 999px; font-weight: 700; font-size: .92rem; text-decoration: none;
               transition: transform .15s ease, opacity .15s ease; }
    .vzx-btn:hover { transform: translateY(-1px); }
    .vzx-btn-solid { background: var(--accent-primary); color: var(--text-inverse); }
    .vzx-btn-ghost { border: 1px solid var(--border-subtle); color: var(--text-main); }

    @media (max-width: 640px) {
      .vzx-track-row { grid-template-columns: 2rem 1fr auto; }
      .vzx-bar { display: none; }
    }
"""

STRAY_GREEN = """
    .bg-brand-400, .bg-green-400, .bg-green-500 { background-color: var(--accent-primary); }
    .bg-brand-400\\/5  { background-color: color-mix(in srgb, var(--accent-primary) 5%, transparent); }
    .bg-brand-400\\/10 { background-color: color-mix(in srgb, var(--accent-primary) 10%, transparent); }
    .bg-brand-400\\/20 { background-color: color-mix(in srgb, var(--accent-primary) 20%, transparent); }
    .text-brand-400, .text-green-500 { color: var(--accent-primary); }
    .border-brand-400\\/10, .border-green-500\\/10 { border-color: color-mix(in srgb, var(--accent-primary) 10%, transparent); }
    .border-brand-400\\/20, .border-green-500\\/20 { border-color: color-mix(in srgb, var(--accent-primary) 20%, transparent); }
    .border-brand-400\\/30 { border-color: color-mix(in srgb, var(--accent-primary) 30%, transparent); }
    [class*="shadow-[0_0_"] { box-shadow: 0 0 15px var(--accent-glow); }
"""


def switcher(current):
    links = []
    for v in VARIANTS:
        on = v["slug"] == current["slug"]
        links.append(
            '<a href="theme-ember-%s.html" style="text-decoration:none;padding:.25rem .6rem;'
            'border-radius:999px;%s">%s</a>'
            % (v["slug"],
               "background:var(--accent-primary);color:var(--text-inverse);font-weight:700"
               if on else "color:inherit",
               v["name"]))
    links.append('<a href="index.html" style="color:inherit;text-decoration:none;'
                 'padding:.25rem .6rem;opacity:.7">Live site</a>')
    return (
        '%s\n<div id="vz-theme-switch" style="position:fixed;left:50%%;bottom:1rem;'
        'transform:translateX(-50%%);z-index:9999;display:flex;gap:.15rem;align-items:center;'
        'padding:.4rem .5rem;border-radius:999px;background:var(--bg-glass);'
        'border:1px solid var(--border-subtle);backdrop-filter:blur(12px);'
        '-webkit-backdrop-filter:blur(12px);font-family:ui-monospace,Menlo,monospace;'
        'font-size:.72rem;letter-spacing:.04em;color:var(--text-muted);'
        'box-shadow:0 8px 24px rgba(0,0,0,.28);max-width:calc(100vw - 2rem);'
        'flex-wrap:wrap;justify-content:center">'
        '<span style="opacity:.6;padding-left:.35rem">ember</span>%s</div>'
        % (MARK, "".join(links)))


def build(src, variant, sections, closing):
    head = src.find("</head>")
    if head == -1:
        raise SystemExit("index.html has no </head>")
    style = ('%s\n<meta name="robots" content="noindex, nofollow">\n'
             '<style id="vz-ember-variant">\n'
             '    /* %s - %s */\n%s\n%s\n%s\n%s\n</style>\n'
             % (MARK, variant["name"], variant["blurb"],
                palette_css(variant), STRAY_GREEN, BASE_CSS, variant["css"]))
    out = src[:head] + style + src[head:]

    at = out.find(ANCHOR_SECTIONS)
    if at == -1:
        raise SystemExit("anchor %r not found in index.html" % ANCHOR_SECTIONS)
    out = out[:at] + sections + "\n    " + out[at:]

    at = out.find(ANCHOR_CTA)
    if at == -1:
        raise SystemExit("anchor %r not found in index.html" % ANCHOR_CTA)
    out = out[:at] + closing + "\n    " + out[at:]

    body = out.rfind("</body>")
    out = out[:body] + switcher(variant) + "\n" + out[body:]
    return out.replace("<title>", "<title>Ember %s &middot; " % variant["name"], 1)


def main():
    if "--clean" in sys.argv:
        gone = 0
        for v in VARIANTS:
            p = os.path.join(ROOT, "theme-ember-%s.html" % v["slug"])
            if os.path.exists(p):
                os.remove(p)
                gone += 1
        print("ember variants removed : %d" % gone)
        return 0

    src = open(INDEX, encoding="utf-8").read()
    if MARK in src:
        raise SystemExit("index.html already contains a variant block - refusing")

    n = counts()
    tracks = track_data()
    sections = how_it_works() + tracks_section(tracks, n["modules"], n["tracks"]) \
        + start_here(tracks) + faq()
    closing = cta(n["modules"])

    for v in VARIANTS:
        rel = "theme-ember-%s.html" % v["slug"]
        open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(
            build(src, v, sections, closing))
        print("  %-10s -> %s" % (v["name"], rel))

    print("ember variants written : %d" % len(VARIANTS))
    print("sections added         : how-it-works, tracks, start-here, faq, cta")
    print("index.html             : untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
