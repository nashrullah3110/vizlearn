#!/usr/bin/env python3
"""Site-wide checks. Exits non-zero if anything fails."""

import glob
import json
import os
import re
import sys
from collections import Counter

from lib_catalog import ROOT, SITE, modules

problems = []


def check(cond, msg):
    if not cond:
        problems.append(msg)


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
    files = [f for f in files
             if os.path.basename(os.path.dirname(f)) not in ("tools", "assets", "node_modules")]
    files.append(os.path.join(ROOT, "index.html"))

    titles = Counter()
    for f in files:
        rel = os.path.relpath(f, ROOT)
        prefix = "../" * rel.count("/")
        s = open(f, encoding="utf-8").read()

        # --- no CDN dependencies for CSS/icons ---
        check("cdn.tailwindcss.com" not in s, "%s: still loads the Tailwind CDN" % rel)
        check("font-awesome" not in s, "%s: still loads Font Awesome" % rel)
        check("tailwind.config" not in s, "%s: still has an inline tailwind.config" % rel)
        check("initTailwind" not in s, "%s: still has the initTailwind polling loop" % rel)
        check("<i class=\"fa" not in s, "%s: leftover Font Awesome <i> tag" % rel)
        check("ns0:" not in s, "%s: namespaced SVG tag (ns0:) would not render" % rel)

        # --- document structure ---
        h1 = len(re.findall(r"<h1[\s>]", s))
        check(h1 == 1, "%s: has %d <h1> (expected 1)" % (rel, h1))
        check(s.count("</html>") == 1, "%s: %d </html> tags" % (rel, s.count("</html>")))
        check(s.count("</body>") == 1, "%s: %d </body> tags" % (rel, s.count("</body>")))
        check(s.count("<script") == s.count("</script>"),
              "%s: unbalanced script tags" % rel)

        tm = re.search(r"<title>(.*?)</title>", s, re.S)
        check(bool(tm), "%s: no <title>" % rel)
        if tm:
            titles[tm.group(1).strip()] += 1

        # --- SEO tags ---
        for tag in ('rel="canonical"', "og:image", "og:title", 'name="twitter:card"',
                    'name="description"', "application/ld+json", "assets/vizlearn.css",
                    "assets/favicon.svg"):
            check(tag in s, "%s: missing %s" % (rel, tag))

        # canonical must match the real URL
        cm = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if cm:
            want = SITE + "/" + ("" if rel == "index.html" else rel)
            check(cm.group(1) == want,
                  "%s: canonical is %s, expected %s" % (rel, cm.group(1), want))

        # JSON-LD must parse
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(block)
            except ValueError as e:
                problems.append("%s: invalid JSON-LD (%s)" % (rel, e))

        # OG image must exist on disk
        om = re.search(r'<meta property="og:image" content="([^"]+)"', s)
        if om:
            p = om.group(1).replace(SITE + "/", "")
            check(os.path.exists(os.path.join(ROOT, p)), "%s: og:image missing on disk (%s)" % (rel, p))

        # --- local asset references resolve ---
        for href in re.findall(r'(?:href|src)="((?:\.\./)*(?:assets|favicon)[^"]*)"', s):
            target = os.path.normpath(os.path.join(os.path.dirname(f), href))
            check(os.path.exists(target), "%s: broken asset reference %s" % (rel, href))

        # --- shared runtime wiring (every page, hub included) ---
        for script in ("assets/modules.js", "assets/search.js", "assets/vizlearn.js"):
            check(s.count('src="%s%s"' % (prefix, script)) == 1,
                  "%s: expected exactly one <script src> for %s" % (rel, script))
        check("const allCourses" not in s, "%s: still inlines its own catalog" % rel)
        check("appSearchInput" in s or "searchInput" in s, "%s: no search input" % rel)

        # --- module furniture ---
        if rel != "index.html":
            for marker, what in (
                ("VIZLEARN:MODULE:BEGIN", "cheat sheet / related / prev-next block"),
                ("vz-cheatsheet", "cheat sheet"),
                ("vz-rail", "related rail"),
                ("vz-share-wrap", "share control"),
            ):
                check(marker in s, "%s: missing %s" % (rel, what))

            check(s.count("VIZLEARN:MODULE:BEGIN") == 1,
                  "%s: module block injected more than once" % rel)
            check(s.count("vz-share-wrap") == 1,
                  "%s: share control injected more than once" % rel)

            # every related / prev / next link must resolve
            block = s[s.find("VIZLEARN:MODULE:BEGIN"):s.find("VIZLEARN:MODULE:END")]
            for href in re.findall(r'href="((?:\.\./)*[a-z_0-9-]+/[a-z_0-9.-]+\.html)"', block):
                target = os.path.normpath(os.path.join(os.path.dirname(f), href))
                check(os.path.exists(target),
                      "%s: dead link in module block -> %s" % (rel, href))

            cards = block.count('class="vz-card"')
            check(cards >= 3, "%s: only %d related cards" % (rel, cards))
            check(rel not in re.findall(r'data-vz-path="([^"]+)"', block),
                  "%s: related rail links back to the page itself" % rel)

        if "vzIcon(" in s:
            check("assets/icons.js" in s, "%s: uses vzIcon() but does not load icons.js" % rel)

    # --- duplicate titles ---
    for t, n in titles.items():
        check(n == 1, "duplicate <title> used by %d pages: %s" % (n, t))

    # --- catalog vs disk ---
    for m in modules():
        check(os.path.exists(os.path.join(ROOT, m["path"])),
              "catalog points at missing file: %s" % m["path"])

    # --- sitemap ---
    sm = os.path.join(ROOT, "sitemap.xml")
    check(os.path.exists(sm), "sitemap.xml missing")
    if os.path.exists(sm):
        locs = re.findall(r"<loc>([^<]+)</loc>", open(sm, encoding="utf-8").read())
        check(len(locs) == 167, "sitemap has %d urls (expected 167)" % len(locs))
        for loc in locs:
            p = loc.replace(SITE + "/", "") or "index.html"
            check(os.path.exists(os.path.join(ROOT, p)), "sitemap url has no file: %s" % loc)

    check(os.path.exists(os.path.join(ROOT, "robots.txt")), "robots.txt missing")

    print("checked %d pages" % len(files))
    if problems:
        print("\n%d PROBLEM(S):" % len(problems))
        for p in problems[:60]:
            print("  -", p)
        if len(problems) > 60:
            print("  ... and %d more" % (len(problems) - 60))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
