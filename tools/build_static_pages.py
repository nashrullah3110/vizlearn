#!/usr/bin/env python3
"""Render about.html, contact.html, privacy.html and terms.html.

The site had none of these. That was already a gap; it became a problem the
day the pages started loading AdSense, because a site running ads with no
privacy policy is one of the standard reasons AdSense review fails - and,
separately, because readers are owed the disclosure.

Copy lives in tools/static_pages.py. Written whole on every build.
"""

import html
import os
import sys

import lib_shell as shell
from lib_catalog import ROOT
from lib_catalog import counts
from lib_pages import STATIC_TITLES, last_modified, pretty_date
from static_pages import PAGES

PREFIX = ""


def build(rel, page, numbers):
    """`numbers` fills the %(modules)d / %(tracks)d placeholders in the copy,
    so a total quoted on the about page can never drift from the catalog."""
    title = "%s | VizLearn" % STATIC_TITLES[rel]
    parts = [shell.head_top(title, PREFIX), shell.header(PREFIX)]

    body = []
    for heading, content in page["sections"]:
        body.append(
            '<section class="vz-doc-section">'
            '<h2>%s</h2>%s</section>' % (html.escape(heading), content % numbers)
        )

    toc = "".join(
        '<li><a href="#%s">%s</a></li>' % (slug(h), html.escape(h))
        for h, _ in page["sections"]
    )

    parts.append("""
    <main class="flex-1 p-4 md:p-8 max-w-4xl mx-auto w-full">

        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold brand-font tracking-tight" style="color: var(--text-main)">%(h1)s</h1>
            <p class="mt-3 max-w-2xl text-base md:text-lg" style="color: var(--text-muted)">%(lead)s</p>
            <p class="vz-doc-updated">Last updated <time datetime="%(iso)s">%(nice)s</time></p>
        </div>

        <nav class="vz-doc-toc" aria-label="On this page">
            <h2>On this page</h2>
            <ul>%(toc)s</ul>
        </nav>

        <article class="vz-doc">%(body)s</article>

    </main>
""" % {
        "crumb": shell.breadcrumb_bar([("Home", "index.html"),
                                       (STATIC_TITLES[rel], None)]),
        "h1": html.escape(page["h1"]),
        "lead": html.escape(page["lead"] % numbers),
        "iso": last_modified(rel),
        "nice": pretty_date(last_modified(rel)),
        "toc": toc,
        "body": "".join(body),
    })

    parts.append(shell.close(PREFIX))
    out = "".join(parts)

    # Give each section a stable id so the table of contents resolves.
    for heading, _ in page["sections"]:
        out = out.replace('<section class="vz-doc-section"><h2>%s</h2>' % html.escape(heading),
                          '<section class="vz-doc-section" id="%s"><h2>%s</h2>'
                          % (slug(heading), html.escape(heading)), 1)
    return out


def slug(heading):
    keep = [c.lower() if c.isalnum() else "-" for c in heading]
    s = "".join(keep)
    while "--" in s:
        s = s.replace("--", "-")
    return s.strip("-")


def main():
    written = 0
    numbers = counts()
    for rel, page in PAGES.items():
        open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(
            build(rel, page, numbers))
        written += 1
    print("static pages : %d" % written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
