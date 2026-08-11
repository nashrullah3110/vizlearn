#!/usr/bin/env python3
"""Make light mode the shipped default.

Dark was the default: `:root` carries the dark tokens and `body.light-mode`
overrides them, with every page deciding at runtime via

    paint(localStorage.getItem('theme') || 'dark')

Flipping that one string is not enough on its own. The theme script runs at the
bottom of the body, so a page whose default is light but whose CSS is dark
would paint dark, finish laying out, and only then flip - a full-page flash on
every load. So three things change together:

  1. `light-mode` ships on the <body> tag, making light the default with no
     JavaScript involved and no flash.
  2. A short script immediately after <body> removes that class when the reader
     has explicitly chosen dark. It runs before any content is parsed, so dark
     readers do not get a light flash either.
  3. The runtime default flips to 'light', including the `=== 'light'` variant
     that some pages use, which defaults to dark implicitly.

The CSS is deliberately untouched. Inverting `:root` would mean rewriting the
token block in assets/vizlearn.css and in 260 inline <style> blocks, and every
`body.light-mode` selector with it - a far larger change for the same result.

Idempotent: re-running finds nothing to do.

    python3 tools/default_light.py
"""

import glob
import os
import re
import sys

from lib_catalog import ROOT

# Runs before any content is parsed, so neither theme flashes the other.
GUARD = ('<script>if(localStorage.getItem("theme")==="dark")'
         'document.body.classList.remove("light-mode");</script>')

BODY = re.compile(r'<body(?P<attrs>[^>]*)>')
CLASS = re.compile(r'class="(?P<v>[^"]*)"')


def patch_body(src):
    """Ship light-mode on <body>, followed by the opt-out guard."""
    m = BODY.search(src)
    if not m or GUARD in src:
        return src, False

    attrs = m.group('attrs')
    cm = CLASS.search(attrs)
    if cm:
        if 'light-mode' in cm.group('v'):
            return src, False
        new_attrs = attrs[:cm.start()] + 'class="%s light-mode"' % cm.group('v') + attrs[cm.end():]
    else:
        new_attrs = attrs + ' class="light-mode"'

    return src[:m.start()] + '<body%s>\n' % new_attrs + GUARD + src[m.end():], True


def patch_default(src):
    """Flip every runtime default from dark to light."""
    before = src
    src = src.replace("localStorage.getItem('theme') || 'dark'",
                      "localStorage.getItem('theme') || 'light'")
    # `=== 'light'` defaults to dark implicitly; invert it rather than leave it.
    src = src.replace("localStorage.getItem('theme') === 'light'",
                      "localStorage.getItem('theme') !== 'dark'")
    return src, src != before


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*.html")))
    files += sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
    files = [f for f in files
             if os.path.basename(os.path.dirname(f)) not in ("node_modules", "tools", "assets")]

    bodies = defaults = 0
    for f in files:
        src = open(f, encoding="utf-8").read()
        src, a = patch_body(src)
        src, b = patch_default(src)
        if a or b:
            open(f, "w", encoding="utf-8").write(src)
        bodies += a
        defaults += b

    print("pages given a light <body>   : %d" % bodies)
    print("pages with the default flipped: %d" % defaults)
    print("pages scanned                 : %d" % len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
