#!/usr/bin/env python3
"""One-time migration: move the per-page article catalog into shared assets.

Every module page used to inline its own copy of the 166-entry `allCourses`
array plus the dropdown logic. Twelve copies had drifted or gone missing
entirely, which is why the search box was dead on those pages.

This script strips the inline copy from every page and points them all at
assets/modules.js + assets/search.js instead, restoring the search markup on
the pages that lost it.
"""

import glob
import os
import re
import sys

from lib_catalog import ROOT

MARKER = "// ===== DROPDOWN SEARCH FUNCTIONALITY ====="

SEARCH_MARKUP = """
                <!-- Search -->
                <div class="search-input-wrapper rounded-full flex items-center w-full max-w-md px-4 py-2.5 mx-auto md:mx-0">
                    <i class="fas fa-search text-sm"></i>
                    <input type="text" id="appSearchInput" aria-label="Search all articles" placeholder="Search all articles..." class="bg-transparent text-sm focus:outline-none ml-3 w-full font-sans tracking-wide">
                    <div id="searchDropdown" class="search-dropdown"></div>
                </div>
"""

# The stale, JS-less search UI on cnn.html / rnn.html.
DEAD_SEARCH_BLOCK = re.compile(
    r'\n\s*<div class="hidden md:block">\s*'
    r'<div class="search-container">.*?</div>\s*</div>',
    re.S,
)


def strip_inline_catalog(src):
    """Remove the inlined catalog + dropdown logic, leaving the script valid."""
    changed = False
    while MARKER in src:
        i = src.index(MARKER)
        j = src.index("</script>", i)
        src = src[:i] + src[j:]
        changed = True
    # hard_vs_soft_labelling.html has the array without the banner comment.
    m = re.search(r"[ \t]*const allCourses\s*=\s*\[", src)
    if m:
        j = src.index("</script>", m.start())
        src = src[: m.start()] + src[j:]
        changed = True
    return src, changed


def ensure_search_markup(src, path):
    """Guarantee the header contains the canonical search input."""
    if "appSearchInput" in src:
        return src, False

    src = DEAD_SEARCH_BLOCK.sub("", src)

    hs = src.index("<header")
    he = src.index("</header>", hs)
    header = src[hs:he]

    m = re.search(r'<a\s+href="\.\./index\.html"', header)
    if not m:
        raise SystemExit("%s: no logo link found in header" % path)
    close = header.index("</a>", m.start()) + len("</a>")

    header = header[:close] + SEARCH_MARKUP + header[close:]
    return src[:hs] + header + src[he:], True


def ensure_scripts(src, prefix):
    """Load the shared catalog + search behaviour just before </body>."""
    if "assets/search.js" in src:
        return src, False
    tags = (
        '    <script src="%sassets/modules.js"></script>\n'
        '    <script src="%sassets/search.js"></script>\n' % (prefix, prefix)
    )
    i = src.rindex("</body>")
    return src[:i] + tags + src[i:], True


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
    files = [f for f in files if "/assets/" not in f and "/tools/" not in f]
    stats = {"stripped": 0, "markup": 0, "scripts": 0}

    for f in files:
        src = open(f, encoding="utf-8").read()
        orig = src
        rel = os.path.relpath(f, ROOT)
        prefix = "../" * rel.count("/")

        src, a = strip_inline_catalog(src)
        src, b = ensure_search_markup(src, rel)
        src, c = ensure_scripts(src, prefix)

        stats["stripped"] += a
        stats["markup"] += b
        stats["scripts"] += c
        if src != orig:
            open(f, "w", encoding="utf-8").write(src)

    print("pages processed : %d" % len(files))
    print("inline catalogs removed : %d" % stats["stripped"])
    print("search markup restored  : %d" % stats["markup"])
    print("shared scripts added    : %d" % stats["scripts"])


if __name__ == "__main__":
    sys.exit(main())
