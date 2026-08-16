#!/usr/bin/env python3
"""Write one preview of the hub per candidate palette, for side-by-side review.

index.html is not touched and not read from anywhere but here. Each preview is
a byte-for-byte copy of it with two things added before </head>:

  * an override for the theme tokens, which wins purely by coming later than
    the block index.html already defines
  * a switcher so the palettes can be flipped between without going back to
    the address bar

Written to the site root rather than a subdirectory because the hub is full of
root-relative links; one level down and every card, asset and icon would 404.
The previews are excluded from the sitemap by construction (it is built from
the catalog) and from the audit (it globs one level down), and they carry a
noindex of their own in case one is ever deployed by accident.

    python3 tools/build_theme_previews.py

Delete them with --clean once a palette is chosen.
"""

import os
import sys

from theme_previews import THEMES, css

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")

MARK = "<!-- VIZLEARN:THEME-PREVIEW -->"


def rel_for(theme):
    return "theme-%s.html" % theme["slug"]


def switcher(current):
    links = []
    for t in THEMES:
        on = t["slug"] == current["slug"]
        links.append(
            '<a href="%s" style="color:%s;text-decoration:none;padding:.25rem .6rem;'
            'border-radius:999px;%s">%s</a>'
            % (rel_for(t),
               "#fff" if on else "inherit",
               "background:var(--accent-primary);color:var(--text-inverse);font-weight:600"
               if on else "",
               t["name"])
        )
    links.append('<a href="index.html" style="color:inherit;text-decoration:none;'
                 'padding:.25rem .6rem;border-radius:999px;opacity:.75">Current (green)</a>')

    return (
        '%s\n<div id="vz-theme-switch" style="position:fixed;left:50%%;bottom:1rem;'
        'transform:translateX(-50%%);z-index:9999;display:flex;gap:.15rem;'
        'align-items:center;padding:.4rem .5rem;border-radius:999px;'
        'background:var(--bg-glass);border:1px solid var(--border-subtle);'
        'backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);'
        'font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.72rem;'
        'letter-spacing:.04em;color:var(--text-muted);'
        'box-shadow:0 8px 24px rgba(0,0,0,.25);max-width:calc(100vw - 2rem);'
        'flex-wrap:wrap;justify-content:center">'
        '<span style="opacity:.6;padding-left:.35rem">preview</span>%s</div>'
        % (MARK, "".join(links))
    )


# A handful of things on the hub are painted with Tailwind's green scale
# directly instead of through the tokens - the logo dot, the pill fills, the
# hairline borders, the glows. Left alone they stay green while everything
# around them moves, which makes a candidate look broken rather than
# different. Mapped here so a preview is an honest look at the palette.
# The `brand` scale in tailwind.config.js is the green palette under another
# name, and it is used with opacity modifiers, so these cannot all collapse to
# a solid accent - a 5% wash would become a solid block. color-mix keeps each
# alpha and follows --accent-primary through the light/dark switch on its own.
def _mix(pct):
    return "color-mix(in srgb, var(--accent-primary) %d%%, transparent)" % pct


STRAY_GREEN = """
    .bg-brand-400,
    .bg-green-400,
    .bg-green-500 {{ background-color: var(--accent-primary); }}
    .bg-brand-400\\\\/5 {{ background-color: {p5}; }}
    .bg-brand-400\\\\/10 {{ background-color: {p10}; }}
    .bg-brand-400\\\\/20 {{ background-color: {p20}; }}

    .text-brand-400,
    .text-green-500 {{ color: var(--accent-primary); }}

    .border-brand-400\\\\/10,
    .border-green-500\\\\/10 {{ border-color: {p10}; }}
    .border-brand-400\\\\/20,
    .border-green-500\\\\/20 {{ border-color: {p20}; }}
    .border-brand-400\\\\/30 {{ border-color: {p30}; }}

    [class*="shadow-[0_0_"] {{ box-shadow: 0 0 15px var(--accent-glow); }}
""".format(p5=_mix(5), p10=_mix(10), p20=_mix(20), p30=_mix(30))


def head_block(theme):
    return (
        '%s\n<meta name="robots" content="noindex, nofollow">\n'
        '<style id="vz-theme-preview">\n'
        '    /* %s - %s\n'
        '     * Overrides the palette index.html defines above. Same selectors,\n'
        '     * later in the document, so these win without !important. */\n'
        '%s\n%s\n'
        '</style>\n' % (MARK, theme["name"], theme["blurb"], css(theme), STRAY_GREEN)
    )


def build(src, theme):
    head_at = src.find("</head>")
    if head_at == -1:
        raise SystemExit("index.html has no </head>")
    out = src[:head_at] + head_block(theme) + src[head_at:]

    body_at = out.rfind("</body>")
    if body_at == -1:
        raise SystemExit("index.html has no </body>")
    out = out[:body_at] + switcher(theme) + "\n" + out[body_at:]

    # The tab title is the only way to tell two screenshots apart later.
    return out.replace("<title>", "<title>%s theme &middot; " % theme["name"], 1)


def main():
    clean = "--clean" in sys.argv
    if clean:
        gone = 0
        for t in THEMES:
            p = os.path.join(ROOT, rel_for(t))
            if os.path.exists(p):
                os.remove(p)
                gone += 1
        print("theme previews removed : %d" % gone)
        return 0

    src = open(INDEX, encoding="utf-8").read()
    if MARK in src:
        raise SystemExit("index.html already contains a preview block - refusing")

    for t in THEMES:
        open(os.path.join(ROOT, rel_for(t)), "w", encoding="utf-8").write(build(src, t))
        print("  %-14s -> %s" % (t["name"], rel_for(t)))

    print("theme previews written : %d" % len(THEMES))
    print("index.html             : untouched")
    return 0


if __name__ == "__main__":
    sys.exit(main())
