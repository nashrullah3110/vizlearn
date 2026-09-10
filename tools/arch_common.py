# -*- coding: utf-8 -*-
"""Shared scaffolding for the named-architecture modules.

The content itself lives in arch_cv.py, arch_nlp.py and arch_dl.py - one file
per track, because fifteen two-thousand-word articles in a single module is a
file nobody can navigate. This holds the parts they all need: the entry
factory, and the small SVG helpers the card thumbnails are drawn with.

A thumbnail is parsed as XML by build_og_images.py, so it may only use the
five entities XML defines. Write &#8594; rather than &rarr;.
"""

A = "var(--accent-primary)"
M = "var(--text-muted)"
B = "var(--border-subtle)"
S = "var(--bg-surface)"

TRACKS = {
    "computer_vision": ("Computer Vision", "computer-vision", "../"),
    "natural_language_processing": ("NLP", "nlp", "../"),
    "deep_learning": ("Deep Learning", "dl", "../"),
}


def entry(slug, directory, title, cat, vizname, lead, svg, viz, notes,
          article, check, refs=(), description=None):
    """One module. Every field is required except the last two.

    `vizname` is the heading over the explorer card and is deliberately
    separate from the page title: "VGG-16" is the page, "The network, layer by
    layer" is what the box beside it contains.
    """
    track, key, prefix = TRACKS[directory]
    return {
        "slug": slug, "dir": directory, "track": track, "key": key,
        "prefix": prefix, "title": title, "cat": cat, "vizname": vizname,
        "lead": lead, "svg": svg, "viz": viz, "notes": notes,
        "article": article, "check": check, "refs": list(refs),
        "description": description,
    }


def svg(body):
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s</svg>'
            % body)


def box(x, y, w, h, fill="none", stroke=B, sw=2, rx=3):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, fill, stroke, sw))


def txt(x, y, s, fill=M, size=9, anchor="middle", weight="normal"):
    return ('<text x="%s" y="%s" fill="%s" font-size="%s" font-family="monospace" '
            'text-anchor="%s" font-weight="%s">%s</text>'
            % (x, y, fill, size, anchor, weight, s))


def line(x1, y1, x2, y2, stroke=A, sw=1.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, stroke, sw, d))


def circle(cx, cy, r, fill="none", stroke=A, sw=1.6):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (cx, cy, r, fill, stroke, sw))


def path(d, fill="none", stroke=A, sw=1.6, dash=None):
    da = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>'
            % (d, fill, stroke, sw, da))


def stack(x0, y0, w, heights, gap=3, stroke=B, fill=S, sw=1.2):
    """A row of bars - the shape most of these thumbnails want."""
    out, x = [], x0
    for h in heights:
        out.append(box(x, y0 + (max(heights) - h) / 2, w, h,
                       fill=fill, stroke=stroke, sw=sw, rx=1))
        x += w + gap
    return "".join(out)
