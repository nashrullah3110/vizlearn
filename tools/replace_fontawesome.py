#!/usr/bin/env python3
"""Replace every Font Awesome <i> tag with an equivalent inline <svg>.

Drops two render-blocking CDN requests (~110 KB of CSS plus ~260 KB of webfonts)
in exchange for path data inlined at each use site. Path data comes straight
out of the @fortawesome/fontawesome-free package, so the glyphs are identical
to what the CDN was serving; FA5 names are resolved through the alias table.
"""

import glob
import json
import os
import re
import sys
from xml.etree import ElementTree as ET

from lib_catalog import ROOT

FA = os.path.join(ROOT, "node_modules", "@fortawesome", "fontawesome-free")
META = os.path.join(FA, "metadata", "icon-families.json")

# Without this, ElementTree serialises children of an SVG root as <ns0:path>,
# which browsers will not render inside HTML.
ET.register_namespace("", "http://www.w3.org/2000/svg")

# Class tokens that are styling modifiers, not icon names.
MODIFIERS = {
    "lg", "xs", "sm", "2x", "3x", "4x", "5x", "fw", "spin", "pulse", "beat",
    "shake", "bounce", "fade", "flip", "flip-horizontal", "flip-vertical",
    "flip-both", "rotate-90", "rotate-180", "rotate-270", "stack", "stack-1x",
    "stack-2x", "inverse", "border", "pull-left", "pull-right", "li",
    "spin-pulse", "spin-reverse", "beat-fade",
}

STYLE_DIR = {"fas": "solid", "fa-solid": "solid", "far": "regular",
             "fa-regular": "regular", "fab": "brands", "fa-brands": "brands"}


def load_aliases():
    meta = json.load(open(META, encoding="utf-8"))
    alias = {}
    for name, entry in meta.items():
        for a in entry.get("aliases", {}).get("names", []) or []:
            alias.setdefault(a, name)
    return alias


ALIAS = load_aliases()
_cache = {}


def svg_body(style, name):
    """Return (viewBox, inner-markup) for an icon, or None if unavailable."""
    key = (style, name)
    if key in _cache:
        return _cache[key]

    candidates = [name, ALIAS.get(name, "")]
    order = [style] + [s for s in ("solid", "brands", "regular") if s != style]

    for cand in filter(None, candidates):
        for st in order:
            p = os.path.join(FA, "svgs", st, cand + ".svg")
            if not os.path.exists(p):
                continue
            root = ET.parse(p).getroot()
            view = root.get("viewBox", "0 0 512 512")
            inner = "".join(
                ET.tostring(c, encoding="unicode").replace(
                    ' xmlns="http://www.w3.org/2000/svg"', "")
                for c in root
            )
            inner = re.sub(r"\s*/>", "/>", inner).strip()
            _cache[key] = (view, inner)
            return _cache[key]

    _cache[key] = None
    return None


I_TAG = re.compile(r'<i\s+([^>]*?)class="([^"]*?)"([^>]*?)>\s*</i>', re.S)
I_TAG_SELF = re.compile(r'<i\s+([^>]*?)class="([^"]*?)"([^>]*?)/>', re.S)

missing = {}


def convert(match):
    pre, classes, post = match.group(1), match.group(2), match.group(3)
    tokens = classes.split()

    style = None
    icon = None
    keep = []
    for t in tokens:
        if t in STYLE_DIR:
            style = STYLE_DIR[t]
        elif t.startswith("fa-"):
            bare = t[3:]
            if bare in MODIFIERS:
                if bare == "lg":
                    keep.append("vz-icon-lg")
                elif bare in ("spin", "spin-pulse"):
                    keep.append("vz-spin")
                # other modifiers have no visual role once inlined
            elif icon is None:
                icon = bare
            else:
                keep.append(t)
        elif t == "fa":
            style = style or "solid"
        else:
            keep.append(t)

    if icon is None:
        return match.group(0)

    got = svg_body(style or "solid", icon)
    if got is None:
        missing[icon] = missing.get(icon, 0) + 1
        return match.group(0)

    view, inner = got
    cls = " ".join(["vz-icon"] + keep)
    attrs = (pre + post).strip()
    attrs = re.sub(r"\baria-hidden=\"[^\"]*\"", "", attrs).strip()
    attrs = (" " + attrs) if attrs else ""
    return ('<svg class="%s" viewBox="%s" fill="currentColor" aria-hidden="true" '
            'xmlns="http://www.w3.org/2000/svg"%s>%s</svg>' % (cls, view, attrs, inner))


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
    files = [f for f in files if os.path.basename(os.path.dirname(f)) not in ("tools", "assets", "node_modules")]
    files.append(os.path.join(ROOT, "index.html"))

    total = 0
    touched = 0
    for f in files:
        src = open(f, encoding="utf-8").read()
        new, n1 = I_TAG.subn(convert, src)
        new, n2 = I_TAG_SELF.subn(convert, new)
        if new != src:
            open(f, "w", encoding="utf-8").write(new)
            touched += 1
        total += n1 + n2

    print("files rewritten : %d" % touched)
    print("icons inlined   : %d" % total)
    if missing:
        print("\nUNRESOLVED (left as <i>, needs manual attention):")
        for k, v in sorted(missing.items(), key=lambda x: -x[1]):
            print("  fa-%-30s %d" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
