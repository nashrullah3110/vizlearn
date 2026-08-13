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
# The hub and the search dropdown want a small SVG per module. The other
# tracks have one hand-drawn per page, which is right for forty pages and
# absurd for a hundred: a reader does not learn anything from a hundred
# different doodles, and they would all be drawn to the same three shapes
# anyway. So each group has a motif, and the variant only shifts which cells
# are filled - enough to tell cards apart in a grid at a glance.
# --------------------------------------------------------------------------

def _art_strings(v):
    cells = []
    for i in range(5):
        on = (i + v) % 3 == 0
        cells.append(
            '<rect x="%d" y="34" width="20" height="22" rx="3" fill="%s" '
            'stroke="var(--accent-primary)" stroke-width="2" opacity="%s"/>'
            % (26 + i * 24, "var(--accent-primary)" if on else "var(--input-bg)",
               "0.85" if on else "1"))
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s'
            '<text x="80" y="76" text-anchor="middle" font-size="9" '
            'font-family="monospace" fill="var(--text-muted)">str</text></svg>'
            % "".join(cells))


def _art_lists(v):
    bars = []
    heights = [(i * 7 + v * 5) % 30 + 12 for i in range(6)]
    for i, h in enumerate(heights):
        bars.append(
            '<rect x="%d" y="%d" width="16" height="%d" rx="2" '
            'fill="var(--accent-primary)" opacity="%.2f"/>'
            % (20 + i * 21, 62 - h, h, 0.35 + 0.1 * (i % 5)))
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s'
            '<line x1="14" y1="64" x2="146" y2="64" stroke="var(--border-subtle)" '
            'stroke-width="2"/></svg>' % "".join(bars))


def _art_dicts(v):
    rows = []
    for i in range(4):
        on = (i + v) % 4 == 0
        rows.append(
            '<rect x="86" y="%d" width="52" height="11" rx="2" fill="var(--accent-primary)" '
            'opacity="%s"/>' % (22 + i * 15, "0.8" if on else "0.2"))
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">'
            '<rect x="16" y="34" width="40" height="18" rx="3" fill="var(--input-bg)" '
            'stroke="var(--text-muted)" stroke-width="2"/>'
            '<text x="36" y="47" text-anchor="middle" font-size="9" font-family="monospace" '
            'fill="var(--text-muted)">key</text>'
            '<path d="M 58 43 L 78 43" stroke="var(--accent-primary)" stroke-width="2"/>'
            '<polygon points="82,43 74,39 74,47" fill="var(--accent-primary)"/>'
            '%s</svg>' % "".join(rows))


# The opening tag matters: index.html inlines card art only when it starts
# with `<svg aria-hidden="true"`, and otherwise wraps it in a data-URI
# <img>. Inside an <img> the SVG is a separate document, so var(--accent-
# primary) resolves to nothing and every shape renders black. xmlns is
# added by whichever inliner uses it.

ART = {"strings": _art_strings, "lists": _art_lists, "dicts": _art_dicts}


def art(group, variant):
    return ART[group](variant)


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
            q["svg"] = art(key, i)
            out.append(q)
    return out


QUESTIONS = _assemble()

# Keyed by page path, for tools/labs.py to merge into LABS so the generated
# check block and the practice bank both pick these up.
CHECKS = {
    "interview/%s.html" % q["slug"]: {"check": q["check"]}
    for q in QUESTIONS if q.get("check")
}
