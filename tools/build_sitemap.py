#!/usr/bin/env python3
"""Generate sitemap.xml and robots.txt.

lastmod comes from each file's last commit date, so re-crawls are driven by
real edits rather than a blanket "today".

The map covers four kinds of URL: the hub, one landing per track, every
module, and the about/contact/privacy/terms set. Before the landings
existed a track was only reachable as `index.html#ml`, which is the same URL
as the hub and so could not appear here at all.
"""

import os
import xml.sax.saxutils as sx

from build_seo import NOINDEX
from lib_catalog import ROOT, SITE, modules
from lib_pages import (STATIC_PAGES, TOOL_ORDER, TOOL_PAGES, TOPIC_ORDER,
                       last_modified, page_url, topic_rel)

SITEMAP = os.path.join(ROOT, "sitemap.xml")
ROBOTS = os.path.join(ROOT, "robots.txt")


def entries():
    """(rel, priority, changefreq) in the order they appear in the sitemap."""
    out = [("index.html", "1.0", "weekly")]
    out += [(topic_rel(k), "0.9", "weekly") for k in TOPIC_ORDER]
    out += [(m["path"], "0.8", "monthly") for m in modules()]
    # Policy pages matter for trust and for AdSense review, not for ranking.
    out += [(p, "0.3", "yearly") for p in STATIC_PAGES
            if os.path.exists(os.path.join(ROOT, p))]
    # The study tools - /practice/, /glossary/, /map/ and friends. The ones
    # carrying a noindex are app furniture rather than content; listing a
    # noindexed URL here only asks Google to crawl something it is then told
    # to drop.
    out += [(TOOL_PAGES[k]["rel"], "0.7", "weekly") for k in TOOL_ORDER
            if os.path.exists(os.path.join(ROOT, TOOL_PAGES[k]["rel"]))
            and TOOL_PAGES[k]["rel"] not in NOINDEX]
    return out


def main():
    rows = []
    for rel, priority, freq in entries():
        rows.append(
            "  <url>\n"
            "    <loc>%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n"
            "    <priority>%s</priority>\n"
            "  </url>" % (sx.escape(page_url(rel)), last_modified(rel), freq, priority)
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    open(SITEMAP, "w", encoding="utf-8").write(xml)

    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "# Build tooling and dependencies, not content.\n"
        "Disallow: /tools/\n"
        "Disallow: /node_modules/\n"
        "\n"
        "Sitemap: %s/sitemap.xml\n" % SITE
    )
    open(ROBOTS, "w", encoding="utf-8").write(robots)

    print("sitemap.xml : %d urls" % len(rows))
    print("robots.txt  : written")


if __name__ == "__main__":
    main()
