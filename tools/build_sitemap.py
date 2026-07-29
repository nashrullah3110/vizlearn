#!/usr/bin/env python3
"""Generate sitemap.xml and robots.txt.

lastmod comes from each file's last commit date, so re-crawls are driven by
real edits rather than a blanket "today".
"""

import os
import subprocess
import xml.sax.saxutils as sx

from lib_catalog import ROOT, SITE, modules

SITEMAP = os.path.join(ROOT, "sitemap.xml")
ROBOTS = os.path.join(ROOT, "robots.txt")


def last_modified(rel):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except subprocess.CalledProcessError:
        pass
    return subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()


def main():
    entries = [("index.html", "1.0", "weekly")]
    entries += [(m["path"], "0.8", "monthly") for m in modules()]

    rows = []
    for rel, priority, freq in entries:
        loc = SITE + "/" + ("" if rel == "index.html" else rel)
        rows.append(
            "  <url>\n"
            "    <loc>%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n"
            "    <priority>%s</priority>\n"
            "  </url>" % (sx.escape(loc), last_modified(rel), freq, priority)
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

    print("sitemap.xml : %d urls" % len(entries))
    print("robots.txt  : written")


if __name__ == "__main__":
    main()
