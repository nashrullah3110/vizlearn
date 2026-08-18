"""The frame every study tool page is rendered into.

/practice/ predates this and builds its own frame; everything added since -
/glossary/, /whats-new/, /map/, /saved/ - shares this one, so the four cannot
drift from each other the way the hand-written module pages did.

A tool page is: the standard shell, a breadcrumb, an h1 + lead read straight
from the page's TOOL_PAGES record, then whatever body the caller renders.
Written whole on every build; there are no hand-edited regions.
"""

import os

import lib_shell as shell
from lib_catalog import ROOT
from lib_pages import TOOL_PAGES, last_modified, pretty_date

PREFIX = "../"

# Shared by more than one tool page: the empty-state panel and the card list
# /glossary/ and /saved/ both render.
COMMON_CSS = """
        .vz-t-wrap { max-width: 980px; margin: 0 auto; width: 100%; }
        .vz-t-panel {
            border: 1px solid var(--border-subtle);
            background: var(--card-bg);
            border-radius: 14px;
            padding: 1.5rem;
        }
        .vz-t-empty {
            border: 1px dashed var(--border-subtle);
            border-radius: 12px;
            padding: 2rem 1.5rem;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
            line-height: 1.7;
        }
        .vz-t-empty a { color: var(--accent-primary); }
        .vz-t-note { margin-top: 1rem; font-size: 0.8rem; color: var(--text-muted); line-height: 1.7; }
"""


def render(key, css, body, wide=False, app=False):
    """Full HTML for the tool page `key`.

    `css` is dropped into the shell's page-specific <style>; `body` is the
    <main> contents. `%(p)s` in `body` is expanded to the root-relative prefix
    so a caller can link to assets without knowing its own depth.

    `app=True` renders the page as a tool rather than a document: no
    breadcrumb, no hero, no reading column, and <main> free to fill the
    viewport. The four labs use it; everything else is a document.
    """
    tool = TOOL_PAGES[key]
    rel = tool["rel"]
    iso = last_modified(rel)

    head = shell.head_top(tool["title"] + " | VizLearn", PREFIX).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        (COMMON_CSS + css).strip("\n"))

    if app:
        # A tool leads with the tool. The title and lead still appear - they
        # are what the page is about, and the only prose a crawler sees above
        # the fold - but as one compact bar rather than a hero block.
        bar = (
            '        <div class="vz-lab-head">\n'
            '            <h1>%s</h1>\n'
            '            <p>%s</p>\n'
            '            <a class="vz-lab-home" href="%sindex.html">&larr; VizLearn</a>\n'
            '        </div>\n' % (tool["title"], tool["lead"], PREFIX)
        )
        main = """
    <main class="flex-1 w-full">
%(bar)s%(body)s
    </main>
""" % {"bar": bar, "body": body % {"p": PREFIX}}
        return (head + shell.header(PREFIX) + main + shell.close(PREFIX)).replace(
            "<body ", "<body data-vz-lab ", 1)

    main = """
    <main class="flex-1 p-4 md:p-8 %(max)s mx-auto w-full">

        <div class="vz-t-wrap">
            <div class="mb-8 animate-fade-in">
                %(crumb)s
                <h1 class="text-3xl md:text-4xl font-bold brand-font tracking-tight" style="color: var(--text-main)">%(title)s</h1>
                <p class="mt-3 max-w-2xl text-base md:text-lg" style="color: var(--text-muted)">%(lead)s</p>
                <p class="vz-doc-updated">Updated <time datetime="%(iso)s">%(nice)s</time></p>
            </div>

%(body)s
        </div>

    </main>
""" % {
        "max": "max-w-7xl" if wide else "max-w-5xl",
        "crumb": shell.breadcrumb_bar([("Home", PREFIX + "index.html"),
                                       (tool["title"], None)]),
        "title": tool["title"],
        "lead": tool["lead"],
        "iso": iso,
        "nice": pretty_date(iso),
        "body": body % {"p": PREFIX},
    }

    return head + shell.header(PREFIX) + main + shell.close(PREFIX)


def write(key, html_text):
    """Write the rendered page to disk, creating its directory."""
    path = os.path.join(ROOT, TOOL_PAGES[key]["rel"])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html_text)
    return TOOL_PAGES[key]["rel"]
