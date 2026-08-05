#!/usr/bin/env python3
"""Site-wide checks. Exits non-zero if anything fails."""

import glob
import json
import os
import re
import sys
from collections import Counter

from lib_catalog import ROOT, SITE, modules
from lib_pages import (STATIC_PAGES, TOOL_ORDER, TOOL_PAGES, TOPIC_ORDER,
                       is_static_page, is_topic_page, page_url, topic_rel)

problems = []


def check(cond, msg):
    if not cond:
        problems.append(msg)


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*", "*.html")))
    files = [f for f in files
             if os.path.basename(os.path.dirname(f)) not in ("tools", "assets", "node_modules")]
    files.append(os.path.join(ROOT, "index.html"))
    files += [os.path.join(ROOT, p) for p in STATIC_PAGES]

    module_paths = {m["path"] for m in modules()}
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
            want = page_url(rel)
            check(cm.group(1) == want,
                  "%s: canonical is %s, expected %s" % (rel, cm.group(1), want))

        # --- breadcrumbs ---
        # Every page but the hub sits under something, and the visible trail
        # was already there; without the JSON-LD a result renders the raw URL.
        if rel != "index.html":
            check('"BreadcrumbList"' in s, "%s: no BreadcrumbList JSON-LD" % rel)

        # --- freshness ---
        if rel != "index.html":
            check('"dateModified"' in s, "%s: JSON-LD has no dateModified" % rel)

        # --- the policy pages must be reachable from everywhere ---
        for target, what in (("privacy.html", "privacy policy"),
                             ("about.html", "about page"),
                             ("contact.html", "contact page")):
            check(target in s, "%s: no link to the %s" % (rel, what))
        check("VIZLEARN:FOOTER:BEGIN" in s, "%s: missing the shared footer" % rel)
        # Generated regions must not nest. They did once: build_module_ui
        # anchored on "<footer", which lands inside the footer's own markers,
        # so the next footer rebuild deleted the module block with it. Only the
        # second build showed the damage, which is exactly why this is checked.
        foot = s.find("VIZLEARN:FOOTER:BEGIN")
        for other in ("VIZLEARN:MODULE:BEGIN", "VIZLEARN:LAB:BEGIN"):
            at = s.find(other)
            if at != -1 and foot != -1:
                check(at < foot, "%s: %s is nested inside the footer block" % (rel, other))
        check(s.count("VIZLEARN:FOOTER:BEGIN") == 1,
              "%s: footer injected more than once" % rel)
        check(s.count("<footer") == 1,
              "%s: %d <footer> elements (expected 1)" % (rel, s.count("<footer")))

        # --- installable ---
        # A manifest that only some pages link is a manifest that only works
        # if you happen to install from the right page.
        check('rel="manifest"' in s, "%s: no manifest link" % rel)

        # --- mobile ---
        check('viewport-fit=cover' in s, "%s: viewport meta not updated" % rel)
        bare = re.findall(r'class="([^"]*)"', s)
        for cls in bare:
            m2 = re.search(r"(?<![a-z:-])grid-cols-(\d+)", cls)
            if m2 and int(m2.group(1)) > 1 and not re.search(r"(sm|md|lg|xl):grid-cols-", cls):
                problems.append("%s: grid-cols-%s with no mobile breakpoint (%s)"
                                % (rel, m2.group(1), cls[:60]))
                break

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
        for script in ("assets/modules.js", "assets/search.js", "assets/vizlearn.js",
                       "assets/vizlearn-lab.js", "assets/vizlearn-state.js",
                       "assets/vizlearn-pwa.js", "assets/vizlearn-keys.js"):
            check(s.count('src="%s%s"' % (prefix, script)) == 1,
                  "%s: expected exactly one <script src> for %s" % (rel, script))
        check("const allCourses" not in s, "%s: still inlines its own catalog" % rel)
        check("appSearchInput" in s or "searchInput" in s, "%s: no search input" % rel)

        # --- module furniture ---
        # Only real modules carry the cheat sheet / related rail / prev-next
        # block. Topic landings and the policy pages are neither.
        if rel in module_paths:
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

            # --- the lab layer ---
            check("VIZLEARN:LAB:BEGIN" in s, "%s: no lab block" % rel)
            check(s.count("VIZLEARN:LAB:BEGIN") == 1,
                  "%s: lab block injected more than once" % rel)
            check("vz-check" in s, "%s: no end-of-module check" % rel)
            check(s.count("VIZLEARN:BYLINE:BEGIN") == 1,
                  "%s: missing or duplicated last-updated byline" % rel)

            lm = re.search(
                r'<script type="application/json" id="vz-lab-data">(.*?)</script>', s, re.S)
            check(bool(lm), "%s: lab block has no config" % rel)
            if lm:
                try:
                    cfg = json.loads(lm.group(1))
                except ValueError as e:
                    problems.append("%s: lab config is not valid JSON (%s)" % (rel, e))
                    cfg = {}
                # Every preset a Run button points at must exist, and every
                # control it names must be on the page - a button that quietly
                # does nothing is worse than no button.
                presets = cfg.get("presets", [])
                for idx in re.findall(r'data-vz-run="(\d+)"', s):
                    check(int(idx) < len(presets),
                          "%s: Run button %s has no preset" % (rel, idx))
                for i, p in enumerate(presets):
                    for item in p.get("set", []):
                        check('id="%s"' % item["id"] in s or 'name="%s"' % item["id"] in s,
                              "%s: preset %d sets unknown control %s" % (rel, i, item["id"]))
                    for cid in p.get("click", []):
                        check('id="%s"' % cid in s,
                              "%s: preset %d clicks unknown button %s" % (rel, i, cid))
                for r in cfg.get("readouts", []):
                    check('id="%s"' % r["id"] in s,
                          "%s: readout %s is not on the page" % (rel, r["id"]))
                # Arrow keys drive real controls; a target that is not on the
                # page would give a keyboard user a focus stop that does
                # nothing, which is worse than no focus stop.
                for role, t in (cfg.get("keys") or {}).items():
                    check('id="%s"' % t["id"] in s,
                          "%s: keyboard %s target %s is not on the page"
                          % (rel, role, t["id"]))

        if "vzIcon(" in s:
            check("assets/icons.js" in s, "%s: uses vzIcon() but does not load icons.js" % rel)

    # --- duplicate titles ---
    for t, n in titles.items():
        check(n == 1, "duplicate <title> used by %d pages: %s" % (n, t))

    # --- catalog vs disk ---
    for m in modules():
        check(os.path.exists(os.path.join(ROOT, m["path"])),
              "catalog points at missing file: %s" % m["path"])

    # --- the PWA files, and that the service worker is current ---
    for name in ("manifest.webmanifest", "sw.js", "offline.html",
                 "assets/icon-192.png", "assets/icon-512.png"):
        check(os.path.exists(os.path.join(ROOT, name)), "%s is missing" % name)

    mf = os.path.join(ROOT, "manifest.webmanifest")
    if os.path.exists(mf):
        try:
            data = json.load(open(mf, encoding="utf-8"))
            for icon in data.get("icons", []):
                p = icon["src"].lstrip("/")
                check(os.path.exists(os.path.join(ROOT, p)),
                      "manifest points at a missing icon: %s" % icon["src"])
        except ValueError as e:
            problems.append("manifest.webmanifest is not valid JSON (%s)" % e)

    swp = os.path.join(ROOT, "sw.js")
    if os.path.exists(swp):
        import build_pwa
        want = "vizlearn-%s" % build_pwa.version()
        got = re.search(r"const CACHE = '([^']+)'", open(swp, encoding="utf-8").read())
        check(bool(got) and got.group(1) == want,
              "sw.js cache name is stale (%s, expected %s) - run npm run pwa"
              % (got.group(1) if got else "none", want))

    # --- sitemap ---
    sm = os.path.join(ROOT, "sitemap.xml")
    check(os.path.exists(sm), "sitemap.xml missing")
    if os.path.exists(sm):
        locs = re.findall(r"<loc>([^<]+)</loc>", open(sm, encoding="utf-8").read())
        # hub + tracks + modules + policy pages + the study tools
        want = (1 + len(TOPIC_ORDER) + len(modules()) + len(STATIC_PAGES)
                + len(TOOL_ORDER))
        check(len(locs) == want, "sitemap has %d urls (expected %d)" % (len(locs), want))
        for loc in locs:
            p = loc.replace(SITE + "/", "") or "index.html"
            # Topic landings are listed directory-style, so map back to disk.
            if p.endswith("/"):
                p += "index.html"
            check(os.path.exists(os.path.join(ROOT, p)), "sitemap url has no file: %s" % loc)

        # Each track must be in there exactly once, as a real URL rather than
        # the `index.html#ml` fragment it used to be.
        for key in TOPIC_ORDER:
            check(page_url(topic_rel(key)) in locs,
                  "sitemap is missing the %s landing page" % key)

    # --- the pages that are not modules exist at all ---
    for key in TOPIC_ORDER:
        check(os.path.exists(os.path.join(ROOT, topic_rel(key))),
              "missing topic landing page: %s" % topic_rel(key))
    for p in STATIC_PAGES:
        check(os.path.exists(os.path.join(ROOT, p)), "missing static page: %s" % p)
    for key in TOOL_ORDER:
        rel = TOOL_PAGES[key]["rel"]
        check(os.path.exists(os.path.join(ROOT, rel)), "missing tool page: %s" % rel)

    # --- the privacy policy has to describe what the pages really load ---
    priv = os.path.join(ROOT, "privacy.html")
    if os.path.exists(priv):
        from build_seo import ADSENSE_CLIENT
        ps = open(priv, encoding="utf-8").read()
        check(ADSENSE_CLIENT in ps,
              "privacy.html does not name the AdSense publisher ID the pages load")
        idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
        ga = re.search(r"gtag/js\?id=([A-Z0-9-]+)", idx)
        if ga:
            check(ga.group(1) in ps,
                  "privacy.html does not name the analytics ID (%s) the pages load"
                  % ga.group(1))

    check(os.path.exists(os.path.join(ROOT, "robots.txt")), "robots.txt missing")

    # --- ads.txt must agree with the AdSense client the pages actually load ---
    ads = os.path.join(ROOT, "ads.txt")
    check(os.path.exists(ads), "ads.txt missing (AdSense will report 'needs ads.txt')")
    if os.path.exists(ads):
        from build_seo import ADSENSE_CLIENT
        pub = ADSENSE_CLIENT.replace("ca-", "")   # ads.txt drops the ca- prefix
        lines = [l.strip() for l in open(ads, encoding="utf-8")
                 if l.strip() and not l.strip().startswith("#")]
        check(any(pub in l for l in lines),
              "ads.txt does not list %s, the publisher ID the pages load" % pub)
        for l in lines:
            fields = [f.strip() for f in l.split(",")]
            check(len(fields) in (3, 4),
                  "ads.txt line has %d fields, expected 3 or 4: %s" % (len(fields), l))
            check(not fields[1].startswith("ca-"),
                  "ads.txt publisher ID must not include the 'ca-' prefix: %s" % l)

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
