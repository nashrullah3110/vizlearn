#!/usr/bin/env python3
"""Make the hand-written module pages behave on phones and tablets.

The outer three-column layout was already responsive (`grid-cols-1
lg:grid-cols-12`), so pages did not visibly break. Three things inside them
did, and all three are invisible on a desktop:

  1. **Grids that never collapse.** 122 places declared a bare `grid-cols-2` or
     `grid-cols-3` with no breakpoint, so a three-across panel stayed three
     across at 375px and its contents were squeezed to unreadable.

  2. **The visualisation came last.** On mobile the columns stack in source
     order - controls, then visualisation - so you changed a slider and the
     thing it changed was off-screen below you. The visualisation column is
     tagged here and CSS lifts it above the controls under `lg`.

  3. **Dragging scrolled the page.** Only 40 pages carried
     `.vz-touch-surface`, so on the rest a drag gesture on the canvas was
     claimed by the browser as a scroll and the interaction died halfway. Every
     surface with a pointer handler now gets it.

Idempotent: each rewrite checks for its own output first.
"""

import glob
import os
import re
import sys

from lib_catalog import ROOT, modules

# --------------------------------------------------------------------------
# 1. Grids with no breakpoint
# --------------------------------------------------------------------------

GRID_CLASS = re.compile(r'class="([^"]*\bgrid-cols-(\d+)\b[^"]*)"')
HAS_BREAKPOINT = re.compile(r"\b(sm|md|lg|xl|2xl):grid-cols-")


def responsive_grids(src):
    """Give every bare multi-column grid a single-column mobile base."""
    changed = [0]

    def fix(m):
        cls, n = m.group(1), int(m.group(2))
        if n < 2 or HAS_BREAKPOINT.search(cls):
            return m.group(0)
        # Two and three across become one column on a phone; wider grids are
        # usually small tiles, which survive two across.
        base, bp = ("1", "sm") if n <= 3 else ("2", "md")
        new = re.sub(r"(?<![a-z:-])grid-cols-%d\b" % n,
                     "grid-cols-%s %s:grid-cols-%d" % (base, bp, n), cls, count=1)
        changed[0] += 1
        return 'class="%s"' % new

    return GRID_CLASS.sub(fix, src), changed[0]


# --------------------------------------------------------------------------
# 2. Which column holds the visualisation
# --------------------------------------------------------------------------

COL = re.compile(r'<(div|section|aside|main)\b([^>]*\bclass="[^"]*lg:col-span-\d+[^"]*"[^>]*)>',
                 re.I)
VIZ_EL = re.compile(r'<(svg|canvas)\b[^>]*\bid="', re.I)


def tag_viz_column(src):
    """Mark the grid column that contains the main visualisation.

    Finding it structurally rather than by class name is the only thing that
    works across 166 pages: the column is `lg:col-span-6` on most, but 8, 9 or
    4 on others.
    """
    if "data-vz-viz" in src:
        return src, 0

    with_viz = None
    widest = None

    for m in COL.finditer(src):
        # The column runs to the next column at the same level, near enough for
        # this purpose: we only need to know which one the canvas falls in.
        nxt = COL.search(src, m.end())
        end = nxt.start() if nxt else len(src)
        span = int(re.search(r"lg:col-span-(\d+)", m.group(2)).group(1))

        if widest is None or span > widest[0]:
            widest = (span, m)
        if VIZ_EL.search(src[m.end():end]):
            if with_viz is None or span > with_viz[0]:
                with_viz = (span, m)

    # A column holding an <svg id>/<canvas id> is the visualisation for
    # certain. Where a page renders into tables instead - most of the SQL
    # track - the widest column is the output side and the narrow one is the
    # controls, which is the same ordering decision.
    best = with_viz or widest
    if not best:
        return src, 0

    m = best[1]
    return src[:m.end() - 1] + " data-vz-viz" + src[m.end() - 1:], 1


# --------------------------------------------------------------------------
# 3. Drag surfaces
# --------------------------------------------------------------------------

DRAG_HINT = re.compile(r"pointerdown|mousedown|touchstart", re.I)


def touch_surfaces(src):
    """Add .vz-touch-surface to the drawing surfaces a page drags on.

    Only pages that actually bind a pointer handler get it - the class sets
    `touch-action: none`, which on a page you merely read would stop you
    scrolling with a finger over the picture.
    """
    if not DRAG_HINT.search(src):
        return src, 0

    added = [0]

    def fix(m):
        tag, attrs = m.group(1), m.group(2)
        if "vz-touch-surface" in attrs:
            return m.group(0)
        cm = re.search(r'class="([^"]*)"', attrs)
        if cm:
            attrs = attrs[:cm.start(1)] + (cm.group(1) + " vz-touch-surface").strip() + \
                attrs[cm.end(1):]
        else:
            attrs = attrs.rstrip() + ' class="vz-touch-surface"'
        added[0] += 1
        return "<%s%s>" % (tag, attrs)

    src = re.sub(r'<(svg|canvas)\b([^>]*\bid="[^"]*"[^>]*)>', fix, src, flags=re.I)

    if "vz-touch-surface" in src:
        return src, added[0]

    # A handful of pages bind the drag to a wrapper <div> rather than to the
    # drawing element. Read the id straight out of the listener call.
    targets = set(re.findall(
        r"""getElementById\(\s*['"]([^'"]+)['"]\s*\)[^;]{0,120}?"""
        r"""addEventListener\(\s*['"](?:pointerdown|mousedown|touchstart)""",
        src, re.S))
    for tid in targets:
        pat = re.compile(r'<(div|section)\b([^>]*\bid="%s"[^>]*)>' % re.escape(tid), re.I)
        src, n = pat.subn(fix, src, count=1)

    if "vz-touch-surface" in src:
        return src, added[0]

    # Last resort, for the WebGL pages: the renderer's canvas is created in
    # JavaScript and appended at runtime, so the only thing that exists in the
    # markup is the container it mounts into.
    MOUNT = re.compile(
        r'<div\b([^>]*\bid="[a-z_-]*(?:canvas|grid|scene|three|plot|render)'
        r'[a-z_-]*"[^>]*)>', re.I)
    m = MOUNT.search(src)
    if m:
        src = src[:m.start()] + fix(re.match(r"<(div)\b([^>]*)>", m.group(0))) + src[m.end():]

    return src, added[0]


# --------------------------------------------------------------------------
# 4. Viewport
# --------------------------------------------------------------------------

VIEWPORT = re.compile(r'<meta\s+name="viewport"[^>]*>', re.I)
WANT_VIEWPORT = ('<meta name="viewport" content="width=device-width, '
                 'initial-scale=1.0, viewport-fit=cover">')


def viewport(src):
    m = VIEWPORT.search(src)
    if not m:
        return src, 0
    if m.group(0) == WANT_VIEWPORT:
        return src, 0
    return src[:m.start()] + WANT_VIEWPORT + src[m.end():], 1


# --------------------------------------------------------------------------

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
    files = [f for f in files
             if os.path.basename(os.path.dirname(f)) not in ("tools", "assets", "node_modules")]
    files.append(os.path.join(ROOT, "index.html"))

    grids = viz_cols = surfaces = viewports = 0
    no_viz = []
    mods = {m["path"] for m in modules()}

    for f in files:
        rel = os.path.relpath(f, ROOT)
        src = open(f, encoding="utf-8").read()
        original = src

        src, n = responsive_grids(src)
        grids += n
        src, n = viewport(src)
        viewports += n

        if rel in mods:
            src, n = tag_viz_column(src)
            viz_cols += n
            if not n and "data-vz-viz" not in src:
                no_viz.append(rel)
            src, n = touch_surfaces(src)
            surfaces += n

        if src != original:
            open(f, "w", encoding="utf-8").write(src)

    print("grids given a mobile base : %d" % grids)
    print("viz columns tagged        : %d" % viz_cols)
    print("drag surfaces marked      : %d" % surfaces)
    print("viewport tags updated     : %d" % viewports)
    if no_viz:
        print("\nno visualisation column found on %d page(s) "
              "(they stack in source order):" % len(no_viz))
        for r in no_viz[:15]:
            print("  -", r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
