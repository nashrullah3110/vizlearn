# -*- coding: utf-8 -*-
"""The /interview/ track: one entry per question.

Content lives in the three modules imported at the bottom, split the way the
questions are grouped rather than by any property of the code. This file holds
what they share - the group definitions, the card art, and the assembly that
turns the three lists into one ordered catalog.

Each question is a dict:

    slug      the filename, and therefore the URL - never change one casually
    group     a key of GROUPS
    kind      "concept" or "coding"
    level     optional difficulty shown as a tag
    title     the h1, and the card title in search and on the hub
    asked     the question in the form an interviewer says it
    lead      the short answer, directly under the h1
    desc      the meta description (build_seo reads it from the page)
    say       optional: the sentence to actually say in the room
    notice    optional bullets beside the visualisation
    viz       frames from tools/interview_viz.py
    sections  [(heading, html)] - the long answer
    code      the editor payload: file, intro, code, walk, try
    check     three multiple-choice questions, merged into tools/labs.py

The `code` payload is the same shape tools/code_dsa.py uses, because both go
through tools/lib_codelab.py.
"""

GROUPS = {
    "strings": {
        "label": "Strings",
        "blurb": "Immutability, slicing, scanning, and the quadratic that hides "
                 "in a one-line loop.",
    },
    "lists": {
        "label": "Lists & arrays",
        "blurb": "A dynamic array, and every consequence: indexing, shifting, "
                 "two pointers, prefix sums.",
    },
    "dicts": {
        "label": "Dicts, sets & hashing",
        "blurb": "Hash tables, what they promise, what voids the promise, and "
                 "the problems they collapse.",
    },
}

GROUP_ORDER = ["strings", "lists", "dicts"]


# --------------------------------------------------------------------------
# Card art
#
# One motif per idea rather than one per group. The first version varied a
# single group motif by index, which meant twenty string cards were the same
# five boxes with different squares filled - decoration rather than
# information, and indistinguishable in a grid.
#
# These are drawn from what the question is actually about, so the card says
# something before you read the title: two pointers converging, a window
# sliding, a stack growing, a table being filled. Motifs are shared where the
# technique is shared, which is the point - two two-pointer problems SHOULD
# look alike - and the assignment below keeps adjacent cards distinct.
#
# The opening tag matters: index.html inlines card art only when it starts
# with `<svg aria-hidden="true"`, and otherwise wraps it in a data-URI <img>
# where var(--accent-primary) resolves to nothing and every shape renders
# black.
# --------------------------------------------------------------------------

A = "var(--accent-primary)"
M = "var(--text-muted)"
B = "var(--border-subtle)"
I = "var(--input-bg)"


def _svg(body):
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">'
            '%s</svg>' % body)


def _cells(n, x=0, y=34, w=20, h=22, gap=4, fills=None, stroke=A):
    """A row of n cells; `fills` maps index -> fill colour."""
    fills = fills or {}
    total = n * w + (n - 1) * gap
    x = x or (160 - total) / 2
    out = []
    for i in range(n):
        out.append('<rect x="%.1f" y="%d" width="%d" height="%d" rx="3" fill="%s" '
                   'stroke="%s" stroke-width="2"/>'
                   % (x + i * (w + gap), y, w, h, fills.get(i, I), stroke))
    return "".join(out)


def _arrow(x1, y1, x2, y2, colour=A):
    dx, dy = x2 - x1, y2 - y1
    ln = max((dx * dx + dy * dy) ** 0.5, 0.001)
    ux, uy = dx / ln, dy / ln
    px, py = -uy, ux
    tip = (x2, y2)
    a = (x2 - ux * 7 + px * 4, y2 - uy * 7 + py * 4)
    b = (x2 - ux * 7 - px * 4, y2 - uy * 7 - py * 4)
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
            'stroke-width="2"/><polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" '
            'fill="%s"/>' % (x1, y1, x2 - ux * 6, y2 - uy * 6, colour,
                             tip[0], tip[1], a[0], a[1], b[0], b[1], colour))


def _label(text, x=80, y=78, size=8):
    return ('<text x="%d" y="%d" text-anchor="middle" font-size="%d" '
            'font-family="monospace" fill="%s">%s</text>' % (x, y, size, M, text))


# --- the motifs ---------------------------------------------------------

def m_lock():
    return _svg('<rect x="58" y="42" width="44" height="30" rx="5" fill="%s" '
                'stroke="%s" stroke-width="2"/>'
                '<path d="M 68 42 v -8 a 12 12 0 0 1 24 0 v 8" fill="none" '
                'stroke="%s" stroke-width="3"/>'
                '<circle cx="80" cy="56" r="4" fill="%s"/>' % (I, A, A, A))


def m_slice():
    return _svg(_cells(6, y=32, w=18, h=24) +
                '<rect x="45" y="26" width="48" height="36" rx="4" fill="none" '
                'stroke="%s" stroke-width="2" stroke-dasharray="4 3"/>' % A +
                _label("copy, not a view"))


def m_codepoint():
    return _svg('<rect x="30" y="30" width="30" height="28" rx="4" fill="%s" '
                'stroke="%s" stroke-width="2"/>'
                '<text x="45" y="49" text-anchor="middle" font-size="14" '
                'font-family="monospace" fill="%s">e</text>' % (I, A, A) +
                _arrow(66, 44, 88, 44) +
                _cells(2, x=94, y=32, w=22, h=24, fills={0: A, 1: A}) +
                _label("1 char = 2 bytes"))


def m_bytes():
    return _svg('<rect x="20" y="30" width="52" height="28" rx="4" fill="%s" '
                'stroke="%s" stroke-width="2"/>'
                '<text x="46" y="49" text-anchor="middle" font-size="11" '
                'font-family="monospace" fill="%s">str</text>' % (I, M, M) +
                _arrow(76, 44, 92, 44) +
                '<rect x="96" y="30" width="52" height="28" rx="4" fill="%s" '
                'opacity="0.25" stroke="%s" stroke-width="2"/>'
                '<text x="122" y="49" text-anchor="middle" font-size="11" '
                'font-family="monospace" fill="%s">bytes</text>' % (A, A, A))


def m_identity():
    return _svg('<rect x="60" y="46" width="40" height="24" rx="4" fill="%s" '
                'opacity="0.3" stroke="%s" stroke-width="2"/>' % (A, A) +
                _arrow(40, 26, 70, 44) + _arrow(120, 26, 90, 44) +
                '<circle cx="36" cy="22" r="5" fill="%s"/>'
                '<circle cx="124" cy="22" r="5" fill="%s"/>' % (M, M) +
                _label("two names, one object"))


def m_find():
    return _svg(_cells(6, y=30, w=18, h=24, fills={3: A}) +
                '<circle cx="30" cy="70" r="7" fill="none" stroke="%s" '
                'stroke-width="2"/><line x1="35" y1="75" x2="42" y2="82" '
                'stroke="%s" stroke-width="2"/>' % (M, M) +
                '<text x="120" y="76" font-size="10" font-family="monospace" '
                'fill="%s">-1</text>' % M)


def m_twopointer(v=0):
    lo, hi = 1 + (v % 2), 6 - (v % 2)
    fills = {lo: A, hi: A}
    return _svg(_cells(8, y=34, w=15, h=22, gap=3, fills=fills) +
                _arrow(24 + lo * 18, 26, 24 + lo * 18 + 12, 26) +
                _arrow(24 + hi * 18 + 14, 26, 24 + hi * 18 + 2, 26) +
                _label("two pointers"))


def m_palindrome():
    return _svg(_cells(5, y=34, w=20, h=22, fills={0: A, 4: A}) +
                '<path d="M 40 30 Q 80 12 120 30" fill="none" stroke="%s" '
                'stroke-width="2" stroke-dasharray="3 3"/>' % A +
                _label("mirrored"))


def m_counter(v=0):
    heights = [(i * 6 + v * 4) % 22 + 10 for i in range(5)]
    bars = "".join('<rect x="%d" y="%d" width="16" height="%d" rx="2" fill="%s" '
                   'opacity="%.2f"/>' % (28 + i * 22, 62 - h, h, A, 0.4 + 0.12 * i)
                   for i, h in enumerate(heights))
    return _svg(bars + '<line x1="20" y1="64" x2="140" y2="64" stroke="%s" '
                'stroke-width="2"/>' % B + _label("counts"))


def m_buckets():
    rows = "".join('<rect x="84" y="%d" width="54" height="12" rx="2" fill="%s" '
                   'opacity="%s"/>' % (20 + i * 17, A, "0.8" if i == 1 else "0.3")
                   for i in range(3))
    return _svg('<rect x="18" y="34" width="40" height="20" rx="4" fill="%s" '
                'stroke="%s" stroke-width="2"/>'
                '<text x="38" y="48" text-anchor="middle" font-size="9" '
                'font-family="monospace" fill="%s">key</text>' % (I, M, M) +
                _arrow(62, 44, 80, 44) + rows)


def m_window(v=0):
    start = 1 + (v % 3)
    return _svg(_cells(7, y=34, w=17, h=22, gap=3,
                       fills={start: A, start + 1: A}) +
                '<rect x="%d" y="28" width="46" height="34" rx="4" fill="none" '
                'stroke="%s" stroke-width="2"/>' % (16 + start * 20, A) +
                _label("sliding window"))


def m_stack():
    boxes = "".join('<rect x="52" y="%d" width="56" height="13" rx="3" fill="%s" '
                    'stroke="%s" stroke-width="2"/>' % (60 - i * 16, A if i == 2 else I, A)
                    for i in range(3))
    return _svg(boxes + _arrow(122, 40, 122, 20) + _label("push / pop"))


def m_runlength():
    return _svg(_cells(6, y=30, w=17, h=22, gap=2,
                       fills={0: A, 1: A, 2: A}) +
                _arrow(80, 62, 80, 72, M) +
                '<text x="80" y="86" text-anchor="middle" font-size="9" '
                'font-family="monospace" fill="%s">a3 b1 c2</text>' % A)


def m_prefix():
    widths = [86, 66, 46]
    rows = "".join('<rect x="34" y="%d" width="%d" height="14" rx="3" fill="%s" '
                   'opacity="0.3"/>'
                   '<rect x="34" y="%d" width="28" height="14" rx="3" fill="%s"/>'
                   % (20 + i * 20, w, A, 20 + i * 20, A) for i, w in enumerate(widths))
    return _svg(rows + _label("shared prefix"))


def m_pattern():
    return _svg(_cells(8, y=24, w=15, h=20, gap=3, fills={3: A, 4: A}, stroke=B) +
                _cells(2, x=78, y=52, w=15, h=20, gap=3, fills={0: A, 1: A}) +
                _arrow(60, 62, 74, 62, M) + _label("pattern slides"))


def m_mapping():
    rows = ""
    for i, (a, b) in enumerate((("a", "x"), ("b", "y"))):
        y = 30 + i * 24
        rows += ('<text x="40" y="%d" font-size="12" font-family="monospace" '
                 'fill="%s">%s</text>' % (y + 4, M, a))
        rows += _arrow(52, y, 100, y)
        rows += ('<text x="110" y="%d" font-size="12" font-family="monospace" '
                 'fill="%s">%s</text>' % (y + 4, A, b))
    return _svg(rows + _label("one-to-one"))


def m_expand():
    return _svg(_cells(7, y=34, w=17, h=22, gap=3, fills={3: A}) +
                _arrow(66, 26, 46, 26) + _arrow(94, 26, 114, 26) +
                _label("expand from a centre"))


def m_grid():
    cells = ""
    for r in range(3):
        for c in range(4):
            on = r == c
            cells += ('<rect x="%d" y="%d" width="20" height="16" rx="2" fill="%s" '
                      'stroke="%s" stroke-width="1.5"/>'
                      % (44 + c * 22, 20 + r * 18, A if on else I, B))
    return _svg(cells + _label("dp table"))


def m_array():
    idx = "".join('<text x="%d" y="70" text-anchor="middle" font-size="7" '
                  'font-family="monospace" fill="%s">%d</text>'
                  % (32 + i * 24, M, i) for i in range(5))
    return _svg(_cells(5, y=32, w=20, h=24, gap=4) + idx +
                _label("contiguous, indexed", y=84, size=7))


def m_alias():
    return _svg('<rect x="58" y="48" width="44" height="22" rx="4" fill="%s" '
                'opacity="0.3" stroke="%s" stroke-width="2"/>' % (A, A) +
                _arrow(28, 24, 66, 46) + _arrow(80, 22, 80, 46) +
                _arrow(132, 24, 94, 46) + _label("one object, three names"))


def m_scan():
    return _svg(_cells(7, y=34, w=17, h=22, gap=3,
                       fills={0: A, 1: A, 2: A, 3: A}) +
                _arrow(24, 26, 100, 26, M) + _label("O(n) every time"))


def m_pair():
    return _svg(_cells(6, y=34, w=18, h=22, gap=3, fills={1: A, 4: A}) +
                '<path d="M 47 30 Q 80 10 110 30" fill="none" stroke="%s" '
                'stroke-width="2"/>' % A +
                '<text x="80" y="80" text-anchor="middle" font-size="10" '
                'font-family="monospace" fill="%s">a + b = t</text>' % A)


def m_running():
    pts = [(24, 62), (44, 48), (64, 54), (84, 32), (104, 38), (124, 22)]
    line = " ".join("%d,%d" % p for p in pts)
    dots = "".join('<circle cx="%d" cy="%d" r="3" fill="%s"/>' % (x, y, A)
                   for x, y in pts)
    return _svg('<polyline points="%s" fill="none" stroke="%s" stroke-width="2"/>'
                % (line, A) + dots + _label("running best"))


def m_dedupe():
    return _svg(_cells(6, y=34, w=18, h=22, gap=3, fills={0: A, 3: A}) +
                '<line x1="46" y1="32" x2="66" y2="58" stroke="%s" stroke-width="2"/>'
                '<line x1="88" y1="32" x2="108" y2="58" stroke="%s" stroke-width="2"/>'
                % (M, M) + _label("duplicates dropped"))


def m_rotate():
    return _svg('<path d="M 80 22 a 26 26 0 1 1 -18 7" fill="none" stroke="%s" '
                'stroke-width="3"/>' % A + _arrow(62, 29, 56, 42) +
                _cells(3, x=52, y=36, w=18, h=18, gap=4, fills={1: A}) +
                _label("rotate by k"))


def m_prefixsuffix():
    return _svg('<rect x="20" y="30" width="52" height="16" rx="3" fill="%s" '
                'opacity="0.75"/>' % A +
                '<rect x="88" y="30" width="52" height="16" rx="3" fill="%s" '
                'opacity="0.35"/>' % A +
                '<text x="46" y="60" text-anchor="middle" font-size="8" '
                'font-family="monospace" fill="%s">left</text>'
                '<text x="114" y="60" text-anchor="middle" font-size="8" '
                'font-family="monospace" fill="%s">right</text>' % (M, M) +
                _label("prefix x suffix", y=78))


def m_intervals():
    bars = [(22, 24, 56), (40, 40, 48), (30, 56, 70), (80, 72, 46)]
    out = "".join('<rect x="%d" y="%d" width="%d" height="12" rx="3" fill="%s" '
                  'opacity="%.2f"/>' % (x, y, w, A, 0.4 + 0.15 * i)
                  for i, (x, y, w) in enumerate(bars))
    return _svg(out + _label("merge overlaps"))


def m_cycle():
    return _svg('<circle cx="96" cy="46" r="22" fill="none" stroke="%s" '
                'stroke-width="2.5"/>' % A +
                '<circle cx="30" cy="46" r="5" fill="%s"/>' % M +
                '<line x1="36" y1="46" x2="72" y2="46" stroke="%s" '
                'stroke-width="2"/>' % M +
                '<circle cx="74" cy="46" r="4" fill="%s"/>' % A +
                _label("a loop in the chain"))


def m_heap():
    return _svg('<line x1="80" y1="26" x2="56" y2="50" stroke="%s" stroke-width="2"/>'
                '<line x1="80" y1="26" x2="104" y2="50" stroke="%s" stroke-width="2"/>'
                % (B, B) +
                '<circle cx="80" cy="26" r="11" fill="%s" stroke="%s" stroke-width="2"/>'
                '<circle cx="56" cy="52" r="9" fill="%s" stroke="%s" stroke-width="2"/>'
                '<circle cx="104" cy="52" r="9" fill="%s" stroke="%s" stroke-width="2"/>'
                % (A, A, I, A, I, A) + _label("heap of k", y=76))


def m_water():
    bars = [14, 30, 10, 38, 22, 34, 16]
    out = ""
    for i, h in enumerate(bars):
        out += ('<rect x="%d" y="%d" width="16" height="%d" fill="%s" opacity="0.8"/>'
                % (22 + i * 18, 64 - h, h, M))
    out += ('<rect x="76" y="30" width="34" height="12" fill="%s" opacity="0.45"/>'
            % A)
    return _svg(out + '<line x1="16" y1="64" x2="144" y2="64" stroke="%s" '
                'stroke-width="2"/>' % B)


def m_flag():
    out = ""
    for i, colour in enumerate([A, M, A]):
        op = ["0.85", "0.35", "0.2"][i]
        out += ('<rect x="%d" y="34" width="38" height="24" rx="3" fill="%s" '
                'opacity="%s"/>' % (14 + i * 44, colour, op))
    return _svg(out + _label("0  ·  1  ·  2"))


def m_triple():
    return _svg(_cells(7, y=34, w=17, h=22, gap=3, fills={0: A, 3: A, 6: A}) +
                '<path d="M 24 30 Q 80 8 138 30" fill="none" stroke="%s" '
                'stroke-width="2"/>' % A + _label("three that sum"))


def m_rotated():
    pts = [(24, 58), (44, 48), (64, 38), (84, 62), (104, 52), (124, 42)]
    line = " ".join("%d,%d" % p for p in pts)
    return _svg('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.5"/>'
                % (line, A) +
                '<line x1="74" y1="20" x2="74" y2="70" stroke="%s" '
                'stroke-width="2" stroke-dasharray="4 3"/>' % M +
                _label("pivot"))


def m_deque():
    return _svg(_cells(4, y=34, w=20, h=22, gap=4, fills={0: A, 3: A}) +
                _arrow(30, 26, 16, 26) + _arrow(130, 26, 144, 26) +
                _label("O(1) at both ends"))


def m_hashtable():
    slots = "".join('<rect x="%d" y="%d" width="46" height="11" rx="2" fill="%s" '
                    'stroke="%s" stroke-width="1.5"/>'
                    % (96, 18 + i * 15, A if i == 1 else I, B) for i in range(4))
    return _svg('<rect x="16" y="34" width="34" height="18" rx="4" fill="%s" '
                'stroke="%s" stroke-width="2"/>' % (I, M) +
                '<text x="33" y="47" text-anchor="middle" font-size="8" '
                'font-family="monospace" fill="%s">key</text>' % M +
                _arrow(54, 43, 90, 43) + slots)


def m_hashable():
    return _svg('<rect x="46" y="40" width="34" height="24" rx="4" fill="%s" '
                'stroke="%s" stroke-width="2"/>' % (I, A) +
                '<path d="M 54 40 v -6 a 9 9 0 0 1 18 0 v 6" fill="none" '
                'stroke="%s" stroke-width="2.5"/>' % A +
                '<rect x="92" y="40" width="34" height="24" rx="4" fill="none" '
                'stroke="%s" stroke-width="2" stroke-dasharray="4 3"/>' % M +
                '<line x1="96" y1="42" x2="122" y2="62" stroke="%s" '
                'stroke-width="2"/>' % M + _label("hashable only"))


def m_quadratic():
    return _svg('<path d="M 22 66 Q 96 66 134 18" fill="none" stroke="%s" '
                'stroke-width="2.5"/>' % A +
                '<line x1="22" y1="18" x2="22" y2="66" stroke="%s" stroke-width="2"/>'
                '<line x1="22" y1="66" x2="138" y2="66" stroke="%s" stroke-width="2"/>'
                % (B, B) +
                '<text x="120" y="34" font-size="10" font-family="monospace" '
                'fill="%s">n²</text>' % A)


def m_lru():
    boxes = "".join('<rect x="%d" y="36" width="28" height="20" rx="4" fill="%s" '
                    'stroke="%s" stroke-width="2"/>' % (18 + i * 34, A if i == 0 else I, A)
                    for i in range(4))
    return _svg(boxes + _arrow(126, 46, 148, 46, M) +
                _label("evict the oldest"))


def m_consecutive():
    return _svg(_cells(6, y=34, w=18, h=22, gap=3,
                       fills={1: A, 2: A, 3: A}) +
                '<text x="80" y="80" text-anchor="middle" font-size="9" '
                'font-family="monospace" fill="%s">3 4 5</text>' % A)


def m_sets():
    return _svg('<circle cx="64" cy="44" r="26" fill="%s" opacity="0.25" '
                'stroke="%s" stroke-width="2"/>' % (A, A) +
                '<circle cx="96" cy="44" r="26" fill="%s" opacity="0.25" '
                'stroke="%s" stroke-width="2"/>' % (A, A) +
                _label("union / intersection"))


def m_mutate():
    return _svg(_cells(5, y=32, w=20, h=22, gap=4, fills={2: A}) +
                '<line x1="86" y1="26" x2="86" y2="62" stroke="#dc2626" '
                'stroke-width="2.5"/>' +
                '<text x="80" y="80" text-anchor="middle" font-size="9" '
                'font-family="monospace" fill="%s">mutating mid-loop</text>' % M)


def m_memo():
    return _svg('<line x1="80" y1="24" x2="54" y2="48" stroke="%s" stroke-width="2"/>'
                '<line x1="80" y1="24" x2="106" y2="48" stroke="%s" stroke-width="2"/>'
                '<line x1="54" y1="48" x2="40" y2="68" stroke="%s" stroke-width="2"/>'
                % (B, B, B) +
                '<circle cx="80" cy="24" r="9" fill="%s"/>' % A +
                '<circle cx="54" cy="48" r="8" fill="%s"/>' % A +
                '<circle cx="106" cy="48" r="8" fill="%s" opacity="0.25" '
                'stroke="%s" stroke-width="2"/>' % (A, A) +
                '<circle cx="40" cy="68" r="7" fill="%s" opacity="0.25" '
                'stroke="%s" stroke-width="2"/>' % (A, A) +
                _label("cached, not recomputed", y=84, size=7))


def m_prefixmap():
    return _svg(_cells(6, y=26, w=18, h=18, gap=3, fills={1: A, 4: A}) +
                _arrow(80, 48, 80, 60, M) +
                '<rect x="46" y="62" width="68" height="14" rx="3" fill="%s" '
                'opacity="0.3" stroke="%s" stroke-width="1.5"/>' % (A, A) +
                '<text x="80" y="73" text-anchor="middle" font-size="8" '
                'font-family="monospace" fill="%s">prefix -> count</text>' % A)


MOTIFS = {
    "lock": m_lock, "slice": m_slice, "codepoint": m_codepoint, "bytes": m_bytes,
    "identity": m_identity, "find": m_find, "palindrome": m_palindrome,
    "counter": m_counter, "buckets": m_buckets, "stack": m_stack,
    "runlength": m_runlength, "prefix": m_prefix, "pattern": m_pattern,
    "mapping": m_mapping, "expand": m_expand, "grid": m_grid, "array": m_array,
    "alias": m_alias, "scan": m_scan, "pair": m_pair, "running": m_running,
    "dedupe": m_dedupe, "rotate": m_rotate, "prefixsuffix": m_prefixsuffix,
    "intervals": m_intervals, "cycle": m_cycle, "heap": m_heap, "water": m_water,
    "flag": m_flag, "triple": m_triple, "rotated": m_rotated, "deque": m_deque,
    "hashtable": m_hashtable, "hashable": m_hashable, "quadratic": m_quadratic,
    "lru": m_lru, "consecutive": m_consecutive, "sets": m_sets,
    "mutate": m_mutate, "memo": m_memo, "prefixmap": m_prefixmap,
}

# Motifs taking a variant argument, so two questions sharing a technique still
# differ on the card.
VARIED = {"twopointer": m_twopointer, "window": m_window, "counter": m_counter}

# slug -> motif. Chosen from what the question is about; the ordering below
# follows the catalog, so neighbours can be kept distinct by eye.
CARD = {
    # strings
    "why-are-python-strings-immutable": "lock",
    "what-does-string-slicing-cost": "slice",
    "does-len-count-characters-or-bytes": "codepoint",
    "str-versus-bytes-in-python": "bytes",
    "string-interning-and-the-is-operator": "identity",
    "find-versus-index-on-strings": "find",
    "reverse-a-string": ("twopointer", 0),
    "valid-palindrome": "palindrome",
    "valid-anagram": ("counter", 0),
    "group-anagrams": "buckets",
    "longest-substring-without-repeating-characters": ("window", 0),
    "first-non-repeating-character": ("counter", 2),
    "valid-parentheses": "stack",
    "string-compression": "runlength",
    "longest-common-prefix": "prefix",
    "implement-substring-search": "pattern",
    "isomorphic-strings": "mapping",
    "longest-palindromic-substring": "expand",
    "edit-distance": "grid",
    "minimum-window-substring": ("window", 2),
    # lists
    "what-is-a-python-list-underneath": "array",
    "the-nested-list-multiplication-bug": "alias",
    "why-is-in-slow-on-a-list": "scan",
    "two-sum": "pair",
    "maximum-subarray-kadane": "running",
    "remove-duplicates-in-place": "dedupe",
    "rotate-an-array": "rotate",
    "product-of-array-except-self": "prefixsuffix",
    "merge-intervals": "intervals",
    "find-the-duplicate-number": "cycle",
    "kth-largest-element": "heap",
    "trapping-rain-water": "water",
    "sort-colors-dutch-national-flag": "flag",
    "three-sum": "triple",
    "search-in-rotated-sorted-array": "rotated",
    "sliding-window-maximum": ("window", 1),
    "list-versus-tuple-versus-deque": "deque",
    # dicts
    "how-does-a-python-dict-work": "hashtable",
    "why-must-dict-keys-be-hashable": "hashable",
    "counting-with-dictionaries": ("counter", 1),
    "accidental-quadratic-complexity": "quadratic",
    "design-an-lru-cache": "lru",
    "longest-consecutive-sequence": "consecutive",
    "subarray-sum-equals-k": "prefixmap",
    "sets-versus-lists-and-deduplication": "sets",
    "modifying-a-collection-while-iterating": "mutate",
    "memoisation-with-a-dictionary": "memo",
    "design-a-hashmap": "buckets",
    "grouping-and-inverting-dictionaries": "mapping",
}


def art(slug):
    """The card image for one question, or a neutral fallback."""
    spec = CARD.get(slug)
    if spec is None:
        return m_array()
    if isinstance(spec, tuple):
        return VARIED[spec[0]](spec[1])
    return MOTIFS[spec]()


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------

def _assemble():
    from interview_strings import STRINGS
    from interview_lists import LISTS
    from interview_dicts import DICTS

    by_group = {"strings": STRINGS, "lists": LISTS, "dicts": DICTS}
    out = []
    for key in GROUP_ORDER:
        for i, q in enumerate(by_group[key]):
            q = dict(q)
            q["group"] = key
            q.setdefault("kind", "concept")
            q["svg"] = art(q["slug"])
            out.append(q)
    return out


QUESTIONS = _assemble()

# Keyed by page path, for tools/labs.py to merge into LABS so the generated
# check block and the practice bank both pick these up.
CHECKS = {
    "interview/%s.html" % q["slug"]: {"check": q["check"]}
    for q in QUESTIONS if q.get("check")
}
