#!/usr/bin/env python3
"""Write one preview of the hub per Phosphor variant.

index.html is read and never written.

The radar is interactive here rather than decorative: every spoke is a real
link to its track, hovering or tab-focusing one lifts it out of the web and
writes the numbers into a readout, and the table beside it drives the same
highlight from the other direction. It is built as inline SVG from the
catalog, so it themes with the page and cannot disagree with the real counts.

    python3 tools/build_phosphor_variants.py
    python3 tools/build_phosphor_variants.py --clean
"""

import html
import math
import os
import sys

from lib_catalog import DIR_META, counts, modules
from phosphor_variants import FIXES_CSS, VARIANTS, css as palette_css

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
MARK = "<!-- VIZLEARN:PHOSPHOR-VARIANT -->"

ANCHOR_SECTIONS = '<main id="course-container"'
ANCHOR_CTA = '<footer class="vz-footer"'


def esc(s):
    return html.escape(str(s))


def track_data():
    mods = modules()
    seen, order = {}, []
    for m in mods:
        d = m["dir"]
        if d not in seen:
            seen[d] = {"dir": d, "label": DIR_META.get(d, (d,))[0], "n": 0,
                       "first": m["path"], "first_title": m["title"]}
            order.append(seen[d])
        seen[d]["n"] += 1
    return sorted(order, key=lambda t: -t["n"])


# --------------------------------------------------------------------------
# Radar
# --------------------------------------------------------------------------

W, H = 880, 640
CX, CY = 440, 312
R = 196


def _pt(i, n, frac):
    ang = -math.pi / 2 + (2 * math.pi * i / n)
    return CX + R * frac * math.cos(ang), CY + R * frac * math.sin(ang)


def radar(tracks):
    n = len(tracks)
    scale = int(math.ceil(tracks[0]["n"] / 10.0) * 10)
    rings = [0.25, 0.5, 0.75, 1.0]

    o = ['<svg class="vzx-radar" viewBox="0 0 %d %d" role="img" '
         'aria-labelledby="vzx-radar-t vzx-radar-d" preserveAspectRatio="xMidYMid meet">' % (W, H),
         '<title id="vzx-radar-t">Modules per track</title>',
         '<desc id="vzx-radar-d">One spoke per track; distance from the centre '
         'is that track\'s module count. Every spoke is a link, and the same '
         'numbers are in the table beside the chart.</desc>']

    for f in rings:
        o.append('<polygon class="vzx-r-ring" points="%s"/>'
                 % " ".join("%.1f,%.1f" % _pt(i, n, f) for i in range(n)))
    for i in range(n):
        x, y = _pt(i, n, 1.0)
        o.append('<line class="vzx-r-spoke" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (CX, CY, x, y))
    for f in rings:
        o.append('<text class="vzx-r-scale" x="%.1f" y="%.1f">%d</text>'
                 % (CX + 7, CY - R * f + 4, int(round(scale * f))))

    pts = [_pt(i, n, t["n"] / float(scale)) for i, t in enumerate(tracks)]
    o.append('<polygon class="vzx-r-area" points="%s"/>'
             % " ".join("%.1f,%.1f" % p for p in pts))

    # One <a> per track: the dot, its label, and a generous invisible hit
    # target, so pointer and keyboard both land on the same thing.
    for i, (t, (px, py)) in enumerate(zip(tracks, pts)):
        lx, ly = _pt(i, n, 1.0)
        dx, dy = lx - CX, ly - CY
        d = math.hypot(dx, dy) or 1
        tx, ty = CX + dx / d * (R + 32), CY + dy / d * (R + 32)
        anchor = "middle" if abs(dx) < 14 else ("start" if dx > 0 else "end")
        o.append(
            '<a class="vzx-r-node" href="%s/" data-track="%s" '
            'aria-label="%s, %d modules">'
            '<line class="vzx-r-lead" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
            '<circle class="vzx-r-hit" cx="%.1f" cy="%.1f" r="26"/>'
            '<circle class="vzx-r-dot" cx="%.1f" cy="%.1f" r="5"/>'
            '<text class="vzx-r-label" x="%.1f" y="%.1f" text-anchor="%s">%s</text>'
            '<text class="vzx-r-num" x="%.1f" y="%.1f" text-anchor="%s">%d</text>'
            '</a>'
            % (esc(t["dir"]), esc(t["dir"]), esc(t["label"]), t["n"],
               CX, CY, px, py, px, py, px, py,
               tx, ty, anchor, esc(t["label"]), tx, ty + 18, anchor, t["n"]))

    o.append("</svg>")
    return "".join(o)


def radar_table(tracks):
    rows = "".join(
        '<tr class="vzx-r-row" data-track="%s">'
        '<th scope="row"><a href="%s/">%s</a></th><td>%d</td></tr>'
        % (esc(t["dir"]), esc(t["dir"]), esc(t["label"]), t["n"]) for t in tracks)
    return ('<table class="vzx-r-table"><caption>Modules per track</caption>'
            '<thead><tr><th scope="col">Track</th><th scope="col">Modules</th></tr></thead>'
            '<tbody>%s</tbody></table>' % rows)


RADAR_JS = """
<script>
(function () {
  // Radar: hover or focus a spoke to lift it out of the web and write it
  // into the readout. The table drives the same highlight the other way.
  var wrap = document.querySelector('.vzx-radar-wrap');
  if (!wrap) return;
  var out = wrap.querySelector('.vzx-r-readout');
  var idle = out ? out.textContent : '';

  function set(key) {
    wrap.querySelectorAll('.vzx-r-node, .vzx-r-row').forEach(function (el) {
      el.classList.toggle('is-on', !!key && el.dataset.track === key);
    });
    wrap.classList.toggle('is-focused', !!key);
    if (!out) return;
    if (!key) { out.textContent = idle; return; }
    var node = wrap.querySelector('.vzx-r-node[data-track="' + key + '"]');
    if (node) out.textContent = node.getAttribute('aria-label');
  }

  wrap.querySelectorAll('.vzx-r-node, .vzx-r-row').forEach(function (el) {
    var key = el.dataset.track;
    el.addEventListener('mouseenter', function () { set(key); });
    el.addEventListener('mouseleave', function () { set(null); });
    el.addEventListener('focusin', function () { set(key); });
    el.addEventListener('focusout', function () { set(null); });
  });
})();

(function () {
  // Theme switch: suppress transitions for the frame in which the class
  // flips, so nothing on the page tries to interpolate its colours.
  var root = document.documentElement;
  function guard() {
    root.classList.add('vz-swapping');
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { root.classList.remove('vz-swapping'); });
    });
  }
  // Capture, so this runs before the hub's own toggle handler.
  document.addEventListener('click', function (e) {
    if (e.target.closest && e.target.closest('#themeToggle, .theme-toggle, [data-theme-toggle]')) guard();
  }, true);
  // Anything else that flips the class is covered too.
  new MutationObserver(guard).observe(document.body, {
    attributes: true, attributeFilter: ['class']
  });
})();
</script>
"""


def tracks_section(tracks, n_mods, n_tracks):
    return (
        '<section class="vzx-sec" aria-labelledby="vzx-tracks-h"><div class="vzx-wrap">'
        '<p class="vzx-kicker">Every track</p>'
        '<h2 class="vzx-h" id="vzx-tracks-h">%d modules across %d tracks</h2>'
        '<p class="vzx-sub">Distance from the centre is the number of modules in '
        'that track. Point at a spoke, or tab through them, to pull one out - '
        'each is a link to that track.</p>'
        '<div class="vzx-radar-wrap">'
        '<div class="vzx-radar-col">%s'
        '<p class="vzx-r-readout" role="status" aria-live="polite">'
        'Hover a spoke for its count</p></div>'
        '%s</div></div></section>'
        % (n_mods, n_tracks, radar(tracks), radar_table(tracks)))


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
    body = "".join(
        '<div class="vzx-step"><span class="vzx-step-n">%d</span>'
        '<div class="vzx-step-body"><h3 class="vzx-step-h">%s</h3>'
        '<p class="vzx-step-p">%s</p></div></div>'
        % (i, esc(t), esc(b)) for i, (t, b) in enumerate(steps, 1))
    return ('<section class="vzx-sec" aria-labelledby="vzx-how-h"><div class="vzx-wrap">'
            '<p class="vzx-kicker">How it works</p>'
            '<h2 class="vzx-h" id="vzx-how-h">Three steps, then you are just using it</h2>'
            '<p class="vzx-sub">No account, no install, nothing gated. Open a page '
            'and it runs.</p><div class="vzx-steps">%s</div></div></section>' % body)


def start_here(tracks):
    want = ["python", "maths", "dsa", "machine_learning", "gen_ai", "interview"]
    by = {t["dir"]: t for t in tracks}
    cards = "".join(
        '<a class="vzx-panel vzx-start-card" href="%s">'
        '<span class="vzx-start-track">%s</span>'
        '<span class="vzx-start-title">%s</span>'
        '<span class="vzx-start-go">Start the track &rarr;</span></a>'
        % (esc(by[d]["first"]), esc(by[d]["label"]), esc(by[d]["first_title"]))
        for d in want if d in by)
    return ('<section class="vzx-sec" aria-labelledby="vzx-start-h"><div class="vzx-wrap">'
            '<p class="vzx-kicker">Start here</p>'
            '<h2 class="vzx-h" id="vzx-start-h">The first page of six tracks</h2>'
            '<p class="vzx-sub">Each of these is the opening module of its track - '
            'the one that assumes the least.</p>'
            '<div class="vzx-start">%s</div></div></section>' % cards)


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
         "thing. It assumes no maths degree and leaves nothing as an exercise "
         "for the reader."),
    ]
    items = "".join(
        '<div class="vzx-panel vzx-faq-item"><h3 class="vzx-faq-q">%s</h3>'
        '<p class="vzx-faq-a">%s</p></div>' % (esc(q), esc(a)) for q, a in qs)
    return ('<section class="vzx-sec" aria-labelledby="vzx-faq-h"><div class="vzx-wrap">'
            '<p class="vzx-kicker">Questions</p>'
            '<h2 class="vzx-h" id="vzx-faq-h">The ones worth answering up front</h2>'
            '<div class="vzx-faq">%s</div></div></section>' % items)


def cta(n_mods):
    return ('<section class="vzx-sec vzx-sec-cta"><div class="vzx-wrap"><div class="vzx-cta">'
            '<h2 class="vzx-h" style="margin-top:0">Open one and push a slider</h2>'
            '<p class="vzx-sub" style="margin:0 auto">That is the whole pitch. %d '
            'modules, all of them running the real computation, none of them asking '
            'you for anything first.</p><div class="vzx-cta-row">'
            '<a class="vzx-btn vzx-btn-solid" href="dsa/big_o_notation.html">Start with Big-O</a>'
            '<a class="vzx-btn vzx-btn-ghost" href="map/">Browse the concept map</a>'
            '</div></div></div></section>' % n_mods)


BASE_CSS = """
    .vzx-wrap { width: 100%; max-width: var(--vz-page, 1600px); margin: 0 auto;
                padding-left: clamp(1rem, 4vw, 2.5rem); padding-right: clamp(1rem, 4vw, 2.5rem); }
    .vzx-steps { display: grid; margin-top: 2.5rem;
                 grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr)); }
    .vzx-step { display: flex; }

    .vzx-radar-wrap { display: grid; gap: 2rem; margin-top: 2rem; align-items: center;
                      grid-template-columns: minmax(0, 1.55fr) minmax(0, 1fr); }
    .vzx-radar { width: 100%; height: auto; display: block; overflow: visible; }
    .vzx-r-ring, .vzx-r-spoke { fill: none; stroke: var(--border-subtle); stroke-width: 1; }
    .vzx-r-area { fill: color-mix(in srgb, var(--accent-primary) 20%, transparent);
                  stroke: var(--accent-primary); stroke-width: 2; stroke-linejoin: round; }
    .vzx-r-scale { fill: var(--text-muted); font-size: 10px; opacity: .7; }

    .vzx-r-node { cursor: pointer; }
    .vzx-r-hit { fill: transparent; }
    .vzx-r-lead { stroke: var(--accent-primary); stroke-width: 0; opacity: 0; }
    .vzx-r-dot { fill: var(--accent-primary); stroke: var(--bg-body); stroke-width: 2; }
    .vzx-r-label { fill: var(--text-main); font-size: 13px; font-weight: 600; }
    .vzx-r-num { fill: var(--accent-primary); font-size: 15px; font-weight: 700; }
    .vzx-r-node, .vzx-r-node * { transition: opacity 140ms ease, stroke-width 140ms ease; }

    /* Everything else steps back so the picked spoke is unmistakable. */
    .vzx-radar-wrap.is-focused .vzx-r-area { opacity: .35; }
    .vzx-radar-wrap.is-focused .vzx-r-node:not(.is-on) { opacity: .38; }
    .vzx-r-node.is-on .vzx-r-lead { stroke-width: 2; opacity: .85; }
    .vzx-r-node.is-on .vzx-r-dot { r: 7.5; }
    .vzx-r-node.is-on .vzx-r-label { fill: var(--accent-primary); }
    .vzx-r-node:focus { outline: none; }
    .vzx-r-node:focus-visible .vzx-r-dot { stroke: var(--accent-primary); stroke-width: 3; }

    .vzx-r-readout { margin: .5rem 0 0; text-align: center; color: var(--text-muted);
                     font-size: .82rem; letter-spacing: .04em; min-height: 1.4em; }
    .vzx-radar-wrap.is-focused .vzx-r-readout { color: var(--accent-primary); font-weight: 700; }

    .vzx-r-table { width: 100%; border-collapse: collapse; font-size: .85rem; }
    .vzx-r-table caption { text-align: left; color: var(--text-muted); font-size: .68rem;
                           letter-spacing: .2em; text-transform: uppercase; padding-bottom: .6rem; }
    .vzx-r-table th, .vzx-r-table td { text-align: left; padding: .5rem;
                                       border-bottom: 1px solid var(--border-subtle); }
    .vzx-r-table thead th { color: var(--text-muted); font-weight: 600; font-size: .7rem;
                            letter-spacing: .12em; text-transform: uppercase; }
    .vzx-r-table td { text-align: right; color: var(--accent-primary); font-weight: 700;
                      font-variant-numeric: tabular-nums; }
    .vzx-r-table tbody th { font-weight: 500; }
    .vzx-r-table a { color: var(--text-main); text-decoration: none; }
    .vzx-r-row { cursor: pointer; }
    .vzx-r-row.is-on { background: color-mix(in srgb, var(--accent-primary) 12%, transparent); }
    .vzx-r-row.is-on a, .vzx-r-row.is-on td { color: var(--accent-primary); }

    .vzx-start { display: grid; gap: 1rem; margin-top: 2.5rem;
                 grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr)); }
    .vzx-start-card { display: flex; flex-direction: column; gap: .4rem; padding: 1.25rem;
                      text-decoration: none; color: inherit; }
    .vzx-start-track { font-size: .66rem; letter-spacing: .16em; text-transform: uppercase;
                       color: var(--accent-primary); font-weight: 700; }
    .vzx-start-title { font-weight: 700; color: var(--text-main); line-height: 1.35; }
    .vzx-start-go { margin-top: auto; padding-top: .7rem; font-size: .8rem; color: var(--text-muted); }

    .vzx-faq { display: grid; gap: 1rem; margin-top: 2.5rem;
               grid-template-columns: repeat(auto-fit, minmax(min(100%, 20rem), 1fr)); }
    .vzx-faq-item { padding: 1.35rem; }
    .vzx-faq-q { font-weight: 700; color: var(--text-main); margin: 0 0 .5rem; font-size: .98rem; }
    .vzx-faq-a { color: var(--text-muted); margin: 0; font-size: .92rem; }

    .vzx-sec-cta { padding-bottom: 5rem; }
    .vzx-cta { padding: 2.75rem 2rem; text-align: center; }
    .vzx-cta .vzx-sub { margin-left: auto; margin-right: auto; }
    .vzx-cta-row { display: flex; gap: .75rem; justify-content: center; flex-wrap: wrap; margin-top: 1.75rem; }
    .vzx-btn { display: inline-flex; align-items: center; gap: .5rem; padding: .7rem 1.4rem;
               font-weight: 700; font-size: .88rem; text-decoration: none; }

    @media (max-width: 900px) {
      .vzx-radar-wrap { grid-template-columns: 1fr; }
      .vzx-r-label { font-size: 15px; }
      .vzx-r-num { font-size: 17px; }
    }
"""

STRAY_GREEN = """
    .bg-brand-400, .bg-green-400, .bg-green-500 { background-color: var(--accent-primary); }
    .bg-brand-400\\/5  { background-color: color-mix(in srgb, var(--accent-primary) 6%, transparent); }
    .bg-brand-400\\/10 { background-color: color-mix(in srgb, var(--accent-primary) 10%, transparent); }
    .bg-brand-400\\/20 { background-color: color-mix(in srgb, var(--accent-primary) 18%, transparent); }
    .text-brand-400, .text-green-500 { color: var(--accent-primary); }
    .border-brand-400\\/10, .border-green-500\\/10,
    .border-brand-400\\/20, .border-green-500\\/20 { border-color: var(--border-subtle); }
    .border-brand-400\\/30 { border-color: var(--border-glow); }
    [class*="shadow-[0_0_"] { box-shadow: none; }
"""


def switcher(cur):
    links = "".join(
        '<a href="theme-phos-%s.html" style="text-decoration:none;padding:.25rem .6rem;'
        'border-radius:4px;%s">%s</a>'
        % (v["slug"],
           "background:var(--accent-primary);color:var(--text-inverse);font-weight:700"
           if v["slug"] == cur["slug"] else "color:inherit", v["name"])
        for v in VARIANTS)
    links += ('<a href="index.html" style="color:inherit;text-decoration:none;'
              'padding:.25rem .6rem;opacity:.7">Live site</a>')
    return ('%s\n<div id="vz-theme-switch" style="position:fixed;left:50%%;bottom:1rem;'
            'transform:translateX(-50%%);z-index:9999;display:flex;gap:.15rem;align-items:center;'
            'padding:.4rem .5rem;border-radius:5px;background:var(--bg-surface);'
            'border:1px solid var(--border-subtle);font-family:var(--vz-mono);'
            'font-size:.72rem;color:var(--text-muted);box-shadow:0 8px 24px rgba(0,0,0,.18);'
            'max-width:calc(100vw - 2rem);flex-wrap:wrap;justify-content:center">'
            '<span style="opacity:.6;padding-left:.35rem">phosphor</span>%s</div>' % (MARK, links))


def build(src, v, sections, closing):
    head = src.find("</head>")
    if head == -1:
        raise SystemExit("index.html has no </head>")
    style = ('%s\n<meta name="robots" content="noindex, nofollow">\n'
             '<style id="vz-phos-variant">\n    /* %s - %s */\n%s\n%s\n%s\n%s\n</style>\n'
             % (MARK, v["name"], v["blurb"], palette_css(v), STRAY_GREEN, BASE_CSS, FIXES_CSS))
    out = src[:head] + style + src[head:]

    for anchor, chunk in ((ANCHOR_SECTIONS, sections), (ANCHOR_CTA, closing)):
        at = out.find(anchor)
        if at == -1:
            raise SystemExit("anchor %r not found in index.html" % anchor)
        out = out[:at] + chunk + "\n    " + out[at:]

    body = out.rfind("</body>")
    out = out[:body] + RADAR_JS + switcher(v) + "\n" + out[body:]
    return out.replace("<title>", "<title>Phosphor %s &middot; " % v["name"], 1)


def main():
    if "--clean" in sys.argv:
        gone = 0
        for v in VARIANTS:
            p = os.path.join(ROOT, "theme-phos-%s.html" % v["slug"])
            if os.path.exists(p):
                os.remove(p)
                gone += 1
        print("phosphor variants removed : %d" % gone)
        return 0

    src = open(INDEX, encoding="utf-8").read()
    if MARK in src:
        raise SystemExit("index.html already contains a variant block - refusing")

    n = counts()
    tracks = track_data()
    sections = (how_it_works() + tracks_section(tracks, n["modules"], n["tracks"])
                + start_here(tracks) + faq())
    closing = cta(n["modules"])

    for v in VARIANTS:
        rel = "theme-phos-%s.html" % v["slug"]
        open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(
            build(src, v, sections, closing))
        print("  %-8s -> %s" % (v["name"], rel))

    print("phosphor variants written : %d" % len(VARIANTS))
    print("index.html                : untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
