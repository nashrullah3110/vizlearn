#!/usr/bin/env python3
"""Render /whats-new/ - what has been added, newest first.

Twelve modules shipped in two days recently and there was no way for a
returning reader to see any of it short of re-scanning eight carousels.

Module additions are derived, not hand-listed: every module's first commit
date already drives its article:published_time, and this groups by that same
date. A module therefore appears here the moment it is committed, and the page
cannot drift from what actually shipped. Everything that is not a module - the
features, the fixes - comes from tools/changelog.py, because nothing in the
catalog knows about those.

Written whole on every build; there are no hand-edited regions.
"""

import html
import sys
from collections import defaultdict

import lib_tool_page as tool
from changelog import CHANGES
from lib_catalog import modules
from lib_pages import TOPICS, first_published, pretty_date

KEY = "whats-new"

# Modules committed before the site had a public history are not "news"; they
# are what the site was when it started. Listing 180 of them under one date
# would bury everything that came after.
SINCE = "2026-08-01"

CSS = """
        .vz-n-release { margin-bottom: 2.5rem; }
        .vz-n-date {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent-primary);
        }
        .vz-n-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-main);
            margin: 0.3rem 0 0.8rem;
        }
        .vz-n-list { list-style: none; padding: 0; margin: 0 0 1rem; }
        .vz-n-list li {
            position: relative;
            padding-left: 1.1rem;
            margin-bottom: 0.5rem;
            color: var(--text-muted);
            font-size: 0.9rem;
            line-height: 1.65;
        }
        .vz-n-list li::before {
            content: "";
            position: absolute;
            left: 0; top: 0.62em;
            width: 5px; height: 5px;
            border-radius: 50%;
            background: var(--accent-primary);
            opacity: 0.7;
        }
        .vz-n-mods {
            display: flex; flex-wrap: wrap; gap: 0.4rem;
            margin-top: 0.3rem;
        }
        .vz-n-mod {
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 0.3rem 0.65rem;
            font-size: 0.8rem;
            color: var(--text-main);
            text-decoration: none;
        }
        .vz-n-mod:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
        .vz-n-mod span {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-muted);
            margin-left: 0.45rem;
        }
        .vz-n-sub {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: var(--text-muted);
            margin: 0.9rem 0 0.4rem;
        }
"""


def modules_by_date():
    """{date: [module, ...]} for everything first committed on or after SINCE."""
    out = defaultdict(list)
    for m in modules():
        d = first_published(m["path"])
        if d and d >= SINCE:
            out[d].append(m)
    return out


def track_of(mod):
    for t in TOPICS.values():
        if t["dir"] == mod["dir"]:
            return t["title"]
    return mod.get("category", "")


def build_body():
    mods = modules_by_date()
    notes = {d: (title, lines) for d, title, lines in CHANGES}

    # Every date that has either kind of news, newest first.
    dates = sorted(set(list(mods) + list(notes)), reverse=True)

    out = []
    for d in dates:
        title, lines = notes.get(d, ("New modules", []))
        block = ['<section class="vz-n-release">',
                 '<p class="vz-n-date">%s</p>' % html.escape(pretty_date(d)),
                 '<h2 class="vz-n-title">%s</h2>' % html.escape(title)]

        if lines:
            block.append('<ul class="vz-n-list">')
            block += ['<li>%s</li>' % html.escape(x) for x in lines]
            block.append("</ul>")

        day = sorted(mods.get(d, []), key=lambda m: m["title"])
        if day:
            block.append('<p class="vz-n-sub">%d new module%s</p>'
                         % (len(day), "" if len(day) == 1 else "s"))
            block.append('<div class="vz-n-mods">')
            for m in day:
                block.append('<a class="vz-n-mod" href="../%s">%s<span>%s</span></a>'
                             % (m["path"], html.escape(m["title"]),
                                html.escape(track_of(m))))
            block.append("</div>")

        block.append("</section>")
        out.append("".join(block))

    total = sum(len(v) for v in mods.values())
    return ('            <p style="font-family:\'JetBrains Mono\',monospace;font-size:.75rem;'
            'color:var(--text-muted);margin-bottom:1.5rem">%d modules added since %s</p>\n'
            '%s\n'
            '            <p class="vz-t-note">Module additions on this page are read '
            'from the repository history rather than kept by hand, so nothing here can '
            'drift from what actually shipped.</p>\n'
            % (total, pretty_date(SINCE),
               "\n".join("            " + b for b in out)))


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, build_body()))
    print("whats-new page            : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
