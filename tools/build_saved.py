#!/usr/bin/env python3
"""Render /saved/ - the bookmarks-and-notes page.

The bookmark control in each module header writes to localStorage
(`vizlearn_saved`) and, like the progress store before /practice/ existed,
that was only ever readable on the page that produced it. This is the other
half: one list of everything bookmarked, with the note left on each, sorted
newest first.

Nothing is rendered at build time - the list only exists in the reader's
browser - so this page ships the shell and assets/saved.js fills it in.

Written whole on every build; there are no hand-edited regions.
"""

import sys

import lib_tool_page as tool

KEY = "saved"

CSS = """
        .vz-s-item {
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.75rem;
            background: var(--card-bg);
        }
        .vz-s-top { display: flex; justify-content: space-between; gap: 1rem; align-items: baseline; }
        .vz-s-title { font-weight: 600; color: var(--text-main); text-decoration: none; font-size: 1rem; }
        .vz-s-title:hover { color: var(--accent-primary); }
        .vz-s-track {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
            white-space: nowrap;
        }
        .vz-s-note {
            margin-top: 0.6rem;
            padding-left: 0.8rem;
            border-left: 2px solid var(--accent-primary);
            color: var(--text-muted);
            font-size: 0.87rem;
            line-height: 1.65;
            white-space: pre-wrap;
        }
        .vz-s-actions { margin-top: 0.7rem; display: flex; gap: 0.6rem; }
        .vz-s-btn {
            background: transparent;
            border: 1px solid var(--border-subtle);
            color: var(--text-muted);
            border-radius: 7px;
            padding: 0.3rem 0.7rem;
            font-size: 0.7rem;
            cursor: pointer;
        }
        .vz-s-btn:hover { border-color: #ef4444; color: #ef4444; }
        .vz-s-count {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-bottom: 1rem;
        }
"""

BODY = """
            <p class="vz-s-count" id="saved-count"></p>
            <div id="saved-list"></div>

            <div class="vz-t-empty" id="saved-empty" hidden>
                <p>Nothing saved yet.</p>
                <p style="margin-top:.6rem">Open any module and use the bookmark
                button in its header to keep it here, with a note if you want one.
                Start from the <a href="%(p)sindex.html">module list</a>.</p>
            </div>

            <p class="vz-t-note">Bookmarks and notes are stored in this browser
            only &mdash; there is no account and nothing is uploaded. Clearing your
            browser storage clears them.</p>

    <script src="%(p)sassets/saved.js"></script>
"""


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, BODY))
    print("saved page                : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
