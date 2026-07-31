#!/usr/bin/env python3
"""Make the interactive visualisations work on touchscreens.

36 modules registered only mouse listeners, so on a phone the canvas did
nothing -- despite pages instructing the reader to "add points" or "drag the
slider". Pointer events cover mouse, touch and stylus with the same API
(`clientX`/`clientY` are identical), so the handler bodies need no changes.

Also tags the drag surface with `vz-touch-surface`, which sets
`touch-action: none` so a drag on the canvas is not stolen by page scrolling.

Idempotent: re-running finds nothing left to convert.
"""

import glob
import os
import re
import sys

from lib_catalog import ROOT

# mouse event -> pointer equivalent
EVENTS = {
    "mousedown": "pointerdown",
    "mousemove": "pointermove",
    "mouseup": "pointerup",
    "mouseleave": "pointerleave",
    "mouseenter": "pointerenter",
    "mouseover": "pointerover",
    "mouseout": "pointerout",
}

LISTENER = re.compile(
    r"""(?P<target>[A-Za-z_$][\w$.]*)\.addEventListener\(\s*(?P<q>['"])(?P<ev>%s)(?P=q)"""
    % "|".join(EVENTS)
)

# `const canvas = document.getElementById('svm-canvas')`
GET_BY_ID = re.compile(
    r"""(?:const|let|var)\s+(?P<var>[A-Za-z_$][\w$]*)\s*=\s*document\.getElementById\(\s*['"](?P<id>[^'"]+)['"]"""
)


def convert(src):
    """Swap mouse listeners for pointer listeners. Returns (src, targets, n)."""
    targets = set()
    count = [0]

    def sub(m):
        count[0] += 1
        if m.group("ev") == "mousedown":
            targets.add(m.group("target"))
        return "%s.addEventListener(%s%s%s" % (
            m.group("target"), m.group("q"), EVENTS[m.group("ev")], m.group("q"))

    return LISTENER.sub(sub, src), targets, count[0]


def tag_surfaces(src, targets):
    """Add `vz-touch-surface` to the canvases that begin a drag."""
    var_to_id = {m.group("var"): m.group("id") for m in GET_BY_ID.finditer(src)}
    ids = {var_to_id[t] for t in targets if t in var_to_id}

    # Fall back to every canvas if the variable could not be resolved, but only
    # when the page actually starts a drag somewhere.
    canvases = re.findall(r"<canvas[^>]*>", src)
    if not ids and targets and canvases:
        ids = None  # signal "all canvases"

    tagged = 0

    def add_class(m):
        nonlocal tagged
        tag = m.group(0)
        if "vz-touch-surface" in tag:
            return tag
        cid = re.search(r'id="([^"]+)"', tag)
        if ids is not None and (not cid or cid.group(1) not in ids):
            return tag
        tagged += 1
        if re.search(r'class="([^"]*)"', tag):
            return re.sub(r'class="([^"]*)"', lambda c: 'class="%s vz-touch-surface"' % c.group(1), tag)
        return tag[:-1].rstrip() + ' class="vz-touch-surface">'

    return re.sub(r"<canvas[^>]*>", add_class, src), tagged


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
    files = [f for f in files
             if os.path.basename(os.path.dirname(f)) not in ("tools", "assets", "node_modules")]

    pages = events = surfaces = 0
    for f in files:
        src = open(f, encoding="utf-8").read()
        new, targets, n = convert(src)
        if not n:
            continue
        new, tagged = tag_surfaces(new, targets)
        open(f, "w", encoding="utf-8").write(new)
        pages += 1
        events += n
        surfaces += tagged

    print("pages converted     : %d" % pages)
    print("listeners rewritten : %d" % events)
    print("drag surfaces tagged: %d" % surfaces)
    return 0


if __name__ == "__main__":
    sys.exit(main())
