#!/usr/bin/env python3
"""Render /saved/ - the bookmarks-and-notes page.

The bookmark control in each module header writes to localStorage
(`vizlearn_saved`) and, like the progress store before /practice/ existed,
that was only ever readable on the page that produced it. This is the other
half: one list of everything bookmarked, with the note left on each, sorted
newest first.

Nothing is rendered at build time - the list only exists in the reader's
browser - so this page ships the shell and assets/saved.js fills it in.

The empty state is the page a first-time reader, and any crawler, actually
sees, so it is a short written guide rather than "Nothing saved yet": what
bookmarks are for, and five modules to start with. It is visible in the
static HTML and saved.js hides it once there is something to list.

Written whole on every build; there are no hand-edited regions.
"""

import sys

import html

import lib_tool_page as tool
from lib_catalog import modules

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
        .vz-s-guide { max-width: 46rem; color: var(--text-muted); line-height: 1.75; font-size: 0.95rem; }
        .vz-s-guide h2 { color: var(--text-main); font-size: 1.25rem; font-weight: 700; margin-bottom: 0.6rem; }
        .vz-s-guide h3 { color: var(--text-main); font-size: 1.02rem; font-weight: 600; margin: 1.4rem 0 0.4rem; }
        .vz-s-guide p { margin-bottom: 0.9rem; }
        .vz-s-guide a { color: var(--accent-primary); }
        .vz-s-start { list-style: decimal; padding-left: 1.3rem; margin-bottom: 1rem; }
        .vz-s-start li { margin-bottom: 0.55rem; }
        .vz-s-start a { font-weight: 600; }
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

            <div class="vz-s-guide" id="saved-empty">
                <h2>How to build a study plan here</h2>
                <p>Nothing is saved in this browser yet. Every module has a
                bookmark button in its header. Use it to keep a module on this
                page, and add a note if you want one: the question you came in
                with, the slider setting that finally made it click, or what to
                go back over. Notes stay attached to the module and show up here,
                newest first.</p>
                <p>The plan that works best is a short one. Pick three to five
                modules that lead into each other, work through them in order,
                and run the experiments in each before you read the explanation
                under it. Then bookmark the ones you will want to return to, not
                every page you opened.</p>
                <h3>Five modules to start with</h3>
                <p>If you are not sure where to begin, these five cover the ideas
                almost everything else on the site assumes. Each one only leans on
                the ones before it.</p>
                <ol class="vz-s-start">%(starters)s</ol>
                <p>From there, the <a href="%(p)sindex.html#learning-path">Learning
                Path</a> continues the same route across tracks, and the
                <a href="%(p)smap/">concept map</a> shows what each module builds
                on. Your progress is tracked automatically as you open modules,
                with or without a bookmark.</p>
            </div>

            <p class="vz-t-note">Bookmarks and notes are stored in this browser
            only &mdash; there is no account and nothing is uploaded. Clearing your
            browser storage clears them.</p>

    <script defer src="%(p)sassets/saved.js"></script>
"""


# The opening of the Learning Path, one module per step and across tracks
# rather than five maths pages in a row. The line under each is why it comes
# where it does.
STARTERS = [
    ("maths/vectors_and_dot_product.html",
     "Data, weights and embeddings are all vectors, and the dot product is the "
     "one operation the rest of the site keeps coming back to."),
    ("maths/derivatives_and_slope.html",
     "Training a model means following a slope downhill. This is where that "
     "slope comes from."),
    ("machine_learning/train_test_split.html",
     "Before fitting anything: how to tell whether a model has learned or has "
     "only memorised."),
    ("machine_learning/linear_regression_with_ols.html",
     "The first real model. Fit a line by hand, then watch least squares do it "
     "properly."),
    ("deep_learning/perceptron.html",
     "One neuron: a weighted sum and a threshold. Every network on the site is "
     "this, stacked."),
]


def starters():
    by_path = {m["path"]: m for m in modules(with_desc=False)}
    return "".join(
        '<li><a href="%%(p)s%s">%s</a> &mdash; %s</li>'
        % (path, html.escape(by_path[path]["title"]), html.escape(why))
        for path, why in STARTERS
    )


def main():
    body = BODY.replace("%(starters)s", starters())
    rel = tool.write(KEY, tool.render(KEY, CSS, body))
    print("saved page                : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
