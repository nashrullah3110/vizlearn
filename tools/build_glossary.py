#!/usr/bin/env python3
"""Render /glossary/ and the term data the tooltip layer reads.

Two outputs from one source (tools/glossary.py):

  glossary/index.html   the readable list, grouped by first letter
  assets/glossary.js    the same terms as data, for the hover cards that
                        assets/vizlearn-glossary.js puts on article prose

Writing both from one place is the point: a definition shown in a tooltip and
the same definition on the glossary page cannot disagree.

Written whole on every build; there are no hand-edited regions.
"""

import html
import json
import os
import sys

import lib_tool_page as tool
from glossary import entries, match_forms
from lib_catalog import ROOT, modules

KEY = "glossary"
JS_OUT = os.path.join(ROOT, "assets", "glossary.js")

CSS = """
        .vz-g-nav {
            display: flex; flex-wrap: wrap; gap: 0.3rem;
            margin-bottom: 1.5rem;
        }
        .vz-g-nav a {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            padding: 0.2rem 0.5rem;
            border: 1px solid var(--border-subtle);
            border-radius: 6px;
            color: var(--text-muted);
            text-decoration: none;
        }
        .vz-g-nav a:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
        .vz-g-letter {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: var(--accent-primary);
            margin: 2rem 0 0.75rem;
            padding-bottom: 0.3rem;
            border-bottom: 1px solid var(--border-subtle);
        }
        .vz-g-item { padding: 0.85rem 0; border-bottom: 1px dashed var(--border-subtle); }
        .vz-g-term { font-weight: 600; color: var(--text-main); font-size: 0.98rem; }
        .vz-g-def { color: var(--text-muted); font-size: 0.9rem; line-height: 1.7; margin-top: 0.25rem; }
        .vz-g-where { font-size: 0.75rem; margin-top: 0.35rem; }
        .vz-g-where a { color: var(--accent-primary); }
        .vz-g-alias {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem; color: var(--text-muted); opacity: 0.75;
            margin-left: 0.5rem;
        }
"""


def build_body():
    by_path = {m["path"]: m for m in modules()}
    rows = entries()

    letters = []
    for _, term, _, _, _ in rows:
        c = term[0].upper()
        if c not in letters:
            letters.append(c)
    letters.sort()

    nav = "".join('<a href="#letter-%s">%s</a>' % (c, c) for c in letters)

    out = []
    seen_letter = None
    for slug, term, aliases, defn, where in rows:
        c = term[0].upper()
        if c != seen_letter:
            out.append('<h2 class="vz-g-letter" id="letter-%s">%s</h2>' % (c, c))
            seen_letter = c

        alias = ('<span class="vz-g-alias">also: %s</span>'
                 % html.escape(", ".join(aliases))) if aliases else ""

        link = ""
        if where:
            title = by_path.get(where, {}).get("title", where)
            link = ('<p class="vz-g-where">Taught in '
                    '<a href="../%s">%s</a></p>' % (where, html.escape(title)))

        out.append(
            '<div class="vz-g-item" id="term-%s">'
            '<p class="vz-g-term">%s%s</p>'
            '<p class="vz-g-def">%s</p>%s</div>'
            % (slug, html.escape(term), alias, html.escape(defn), link))

    return ('            <nav class="vz-g-nav" aria-label="Jump to letter">%s</nav>\n'
            '            <p class="vz-s-count" style="font-family:\'JetBrains Mono\',monospace;'
            'font-size:.75rem;color:var(--text-muted)">%d terms</p>\n'
            '%s\n'
            '            <p class="vz-t-note">Each definition is deliberately short - '
            'enough to keep reading, not enough to replace the module it links to. '
            'These same definitions appear as hover cards the first time a term shows '
            'up in any article.</p>\n'
            % (nav, len(rows), "\n".join("            " + o for o in out)))


def build_js():
    """The term data, smallest form that the runtime can use."""
    data = []
    for slug, term, aliases, defn, where in entries():
        forms = match_forms(slug, term, aliases)
        # A glossary-only term still belongs on the page; it just never gets
        # auto-marked, so there is nothing for the runtime to do with it.
        if not forms:
            continue
        data.append({
            "slug": slug,
            "term": term,
            "match": forms,
            "def": defn,
            "where": where or "",
        })
    return ("/* GENERATED FILE - do not edit by hand.\n"
            " * Source: tools/glossary.py.  Rebuild: python3 tools/build_glossary.py\n"
            " */\n"
            "window.VIZLEARN_GLOSSARY = %s;\n"
            % json.dumps(data, indent=1, ensure_ascii=False))


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, build_body()))
    open(JS_OUT, "w", encoding="utf-8").write(build_js())
    print("glossary page             : %s (%d terms)" % (rel, len(entries())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
