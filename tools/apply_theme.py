#!/usr/bin/env python3
"""Bring every page onto the theme in tools/theme.py.

The site was built before there was a shared stylesheet, so 177 pages carry
their own inline copy of the design tokens, their own font stack, their own
`*` transition and their own header blur. Those inline blocks load after
assets/vizlearn.css and win, so changing the stylesheet alone would leave the
site half green. This rewrites them in place.

It is surgical rather than wholesale. Only declarations the theme owns are
touched; a module that defines `--plot-grid` or `--neuron-fill` for its own
visualisation keeps them. It is also idempotent: running it twice is the same
as running it once, so it can sit in the build chain.

What it changes per page:

  * the values of the theme's tokens inside `:root` and `body.light-mode`
  * font-family declarations, which become the one monospace stack
  * the `*, *::before, *::after` transition, which is what made switching
    light/dark stutter on a page holding 309 cards
  * the header's backdrop blur, which softened every glyph in it
  * any literal green left over from the old palette

    python3 tools/apply_theme.py [--check]
"""

import glob
import os
import re
import sys

from theme import GREEN_MAP, tokens

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The one place a glyph font is legitimately used: a lock icon drawn with a
# Font Awesome codepoint. Rewriting its font-family would print a box.
FONT_KEEP = "Font Awesome"

# The trailing part of the declaration must not cross a quote, backtick or
# angle bracket: these strings also appear inside JS template literals that
# build HTML, and a greedy tail there eats the literal's terminator. That is
# exactly what broke two pages on the first run.
FONT_DECL = re.compile(
    r"""font-family:\s*'(?:Inter|Space Grotesk|JetBrains Mono)'[^;}'"`<>]*""")
BLOCK = {
    "dark": re.compile(r"(:root\s*\{)([^}]*)(\})"),
    "light": re.compile(r"(body\.light-mode\s*\{)([^}]*)(\})"),
}
DUPE_SCOPED = re.compile(
    r"\n\s*a, button, \.vz-card, \.vz-cta, \.vz-tool-link, \.vz-chip, input, select \{"
    r"[^}]*\}", re.S)
UNIVERSAL_TRANSITION = re.compile(
    r"\*,\s*\*::before,\s*\*::after\s*\{[^}]*transition-property:[^}]*\}", re.S)

SENTINEL = "Deliberately nothing. This used to transition"

SCOPED_TRANSITION = """*, *::before, *::after {
            /* Deliberately nothing. This used to transition background,
               border, colour and shadow on every element for 300ms, which
               meant a light/dark switch asked the browser to interpolate
               every node on the page at once. Transitions below are scoped
               to properties a theme change does not alter. */
            transition-property: none;
        }
        a, button, .vz-card, .vz-cta, .vz-tool-link, .vz-chip, input, select {
            transition-property: transform, opacity;
            transition-duration: 140ms;
            transition-timing-function: cubic-bezier(.2, .8, .2, 1);
        }"""


def rewrite_tokens(css, mode):
    """Replace the values of tokens the theme owns; leave the rest alone."""
    owned = tokens(mode)
    out, changed = css, 0
    for name, value in owned.items():
        pat = re.compile(r"(\n\s*)" + re.escape(name) + r"\s*:[^;]*;")
        new, n = pat.subn(lambda m: "%s%s: %s;" % (m.group(1), name, value), out)
        if n:
            out, changed = new, changed + n
    return out, changed


def process(path):
    src = open(path, encoding="utf-8").read()
    before = src

    for mode, rx in BLOCK.items():
        def swap(m, mode=mode):
            body, _ = rewrite_tokens(m.group(2), mode)
            return m.group(1) + body + m.group(3)
        src = rx.sub(swap, src)

    # One typeface. The Font Awesome declaration is left as it is.
    def font(m):
        return m.group(0) if FONT_KEEP in m.group(0) else "font-family: var(--vz-mono)"
    src = FONT_DECL.sub(font, src)
    src = src.replace("font-family:'JetBrains Mono'", "font-family: var(--vz-mono)")
    # SVG presentation attributes, which are not CSS declarations and so are
    # invisible to FONT_DECL above.
    src = src.replace('font-family="Space Grotesk, sans-serif"', 'font-family="monospace"')

    # Guarded: the replacement's own first half still matches the pattern,
    # so without this every run appends another copy of the scoped block.
    if SENTINEL not in src:
        src = UNIVERSAL_TRANSITION.sub(SCOPED_TRANSITION, src)
    # Collapse any copies an earlier unguarded run left behind.
    src = DUPE_SCOPED.sub(lambda m: m.group(0) if m.start() == src.find(m.group(0)) else "", src)

    # The header sits on an opaque colour, so the blur bought nothing and cost
    # subpixel antialiasing on every glyph in it.
    src = re.sub(r"\s*backdrop-filter:\s*blur\(12px\);", "", src)
    src = re.sub(r"\s*-webkit-backdrop-filter:\s*blur\(12px\);", "", src)

    # Space Grotesk is no longer used anywhere - headings are monospace
    # and the canvas labels were rewritten - so stop paying to download
    # it. Generated pages get the link from lib_shell, which was fixed
    # too; this catches the hand-written ones on every build.
    src = src.replace("family=Space+Grotesk:wght@300;500;700&", "")

    for old, new in GREEN_MAP:
        src = src.replace(old, new)

    if src != before:
        open(path, "w", encoding="utf-8").write(src)
        return True
    return False


def main():
    check = "--check" in sys.argv
    pages = [os.path.join(ROOT, "index.html")]
    pages += sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
    pages = [p for p in pages if "/node_modules/" not in p]

    if check:
        stale = []
        for p in pages:
            s = open(p, encoding="utf-8").read()
            if any(g in s for g, _ in GREEN_MAP if g.startswith("#")):
                stale.append(os.path.relpath(p, ROOT))
        print("pages still carrying an old green literal : %d" % len(stale))
        for p in stale[:10]:
            print("   ", p)
        return 1 if stale else 0

    touched = sum(1 for p in pages if process(p))
    print("pages scanned  : %d" % len(pages))
    print("pages rewritten: %d" % touched)
    return 0


if __name__ == "__main__":
    sys.exit(main())
