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
        .vz-n-intro { max-width: 68ch; margin-bottom: 2.75rem; }
        .vz-n-intro p {
            font-family: var(--vz-sans);
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text-muted);
            margin-bottom: 0.9rem;
        }
        .vz-n-intro h2 {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-main);
            margin: 1.6rem 0 0.6rem;
        }
        .vz-n-tracks {
            font-family: var(--vz-sans);
            font-size: 0.92rem;
            line-height: 1.65;
            color: var(--text-muted);
            margin: 0 0 0.7rem;
        }
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


WORDS = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
         7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven",
         12: "Twelve"}


def spell(n):
    return WORDS.get(n, str(n))


def track_sentence(day):
    """A written line describing which tracks a day's modules landed in.

    A bare grid of module titles reads as a list of links rather than as a
    record of what happened. Naming the tracks, in order of how much each one
    grew, says the thing the grid only implies.
    """
    counts = defaultdict(int)
    for m in day:
        counts[track_of(m)] += 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    n = len(day)
    if len(ranked) == 1:
        if n == 1:
            return "One new module, in the %s track." % ranked[0][0]
        return "%s new modules, all of them in the %s track." % (spell(n), ranked[0][0])
    parts = ["%s in %s" % (spell(c).lower() if c < 13 else c, t) for t, c in ranked]
    if len(parts) == 2:
        spread = " and ".join(parts)
    else:
        spread = ", ".join(parts[:-1]) + " and " + parts[-1]
    return "%s new modules: %s." % (spell(n), spread)


def track_of(mod):
    for t in TOPICS.values():
        if t["dir"] == mod["dir"]:
            return t["title"]
    return mod.get("category", "")


INTRO = """\
<div class="vz-n-intro">
<p>This is the written record of what VizLearn has become, in the order it
happened. Every entry below is either a set of modules that went live on a
particular day, or a change to how the site itself works &mdash; a new kind of
visualisation, a fix to something that was misleading, a rewrite of a page that
was not carrying its weight.</p>

<h2>Where the dates come from</h2>
<p>The module entries are not maintained by hand. Each module's first commit in
the repository is what dates it, and this page groups modules by that date. That
means a module appears here the moment it actually ships, and the list cannot
quietly drift out of step with the site. The same date drives the published date
on the module's own page, so the two can never disagree.</p>
<p>Everything that is not a module &mdash; the features, the corrections, the
structural changes &mdash; is written by hand, because nothing in the repository
knows why a change was made. Those entries say what changed and, where it
matters, what was wrong before.</p>

<h2>What counts as news</h2>
<p>Modules committed before %(since)s are not listed. They are not new; they are
what the site was when it started, and putting a hundred and eighty of them
under a single date would bury everything that came after. If you are looking
for those, the track pages list every module in the order they are meant to be
read, and the concept map shows how the tracks depend on one another.</p>

<h2>Reading a release</h2>
<p>Each block names its date, says which tracks grew and by how much, and then
lists the individual modules with the track each one belongs to. Every title is
a link straight to the module. Where a release also changed how the site
behaves, those notes sit above the module list.</p>
</div>
"""


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
            block.append('<p class="vz-n-tracks">%s</p>'
                         % html.escape(track_sentence(day)))
            block.append('<div class="vz-n-mods">')
            for m in day:
                block.append('<a class="vz-n-mod" href="../%s">%s<span>%s</span></a>'
                             % (m["path"], html.escape(m["title"]),
                                html.escape(track_of(m))))
            block.append("</div>")

        block.append("</section>")
        out.append("".join(block))

    total = sum(len(v) for v in mods.values())
    return ('%s\n'
            '            <p style="font-family:\'JetBrains Mono\',monospace;font-size:.75rem;'
            'color:var(--text-muted);margin-bottom:1.5rem">%d modules added since %s</p>\n'
            '%s\n'
            '            <p class="vz-t-note">Module additions on this page are read '
            'from the repository history rather than kept by hand, so nothing here can '
            'drift from what actually shipped.</p>\n'
            % (INTRO % {"since": pretty_date(SINCE)}, total, pretty_date(SINCE),
               "\n".join("            " + b for b in out)))


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, build_body()))
    print("whats-new page            : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
