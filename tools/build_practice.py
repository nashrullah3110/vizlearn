#!/usr/bin/env python3
"""Render /practice/ - the spaced-practice page.

Every module already ends with a check, and those answers have been piling up
in localStorage (`vizlearn_checks`) since the lab layer shipped - but only ever
on the page that produced them. This page is the other half: it draws questions
from the modules the reader has actually opened, weighted by what they got
wrong and how long ago.

The question bank is written by tools/build_labs.py into
assets/practice-bank.js, from the same authored questions and page-derived
recall cards the modules themselves carry, so the two can never disagree.

Written whole on every build; there are no hand-edited regions.
"""

import html
import os
import sys

import lib_shell as shell
from lib_catalog import ROOT, modules
from lib_pages import PRACTICE, last_modified, pretty_date

PREFIX = "../"
REL = PRACTICE["rel"]

CSS = """
        .vz-p-wrap { max-width: 900px; margin: 0 auto; width: 100%; }
        .vz-p-panel {
            border: 1px solid var(--border-subtle);
            background: var(--card-bg);
            border-radius: 14px;
            padding: 1.6rem;
        }
        .vz-p-stats {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 1.2rem 0;
        }
        @media (min-width: 640px) { .vz-p-stats { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
        .vz-p-stat {
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 0.85rem;
            text-align: center;
        }
        .vz-p-stat b {
            display: block;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.5rem;
            color: var(--accent-primary);
        }
        .vz-p-stat span {
            font-size: 0.65rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted);
        }
        .vz-p-controls { display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: flex-end; }
        .vz-p-controls label {
            font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em;
            color: var(--text-muted); display: block; margin-bottom: 0.35rem;
        }
        .vz-p-controls select {
            background: var(--bg-surface, var(--card-bg));
            color: var(--text-main);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 0.55rem 0.7rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
        }
        .vz-p-start {
            background: var(--accent-primary); color: #04120a;
            border: none; border-radius: 8px;
            padding: 0.7rem 1.4rem;
            font-weight: 700; font-size: 0.75rem;
            text-transform: uppercase; letter-spacing: 0.06em;
            cursor: pointer;
        }
        .vz-p-meter { height: 6px; border-radius: 3px; background: var(--border-subtle); overflow: hidden; margin-bottom: 1.2rem; }
        .vz-p-meter div { height: 100%; background: var(--accent-primary); width: 0; transition: width 300ms; }
        .vz-p-head { display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.5rem; }
        .vz-p-source { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 0.6rem; }
        .vz-p-source a { color: var(--accent-primary); }
        .vz-p-cat {
            border: 1px solid var(--border-subtle); border-radius: 999px;
            padding: 1px 8px; margin-left: 8px; font-size: 0.65rem;
            text-transform: uppercase; letter-spacing: 0.06em;
        }
        .vz-p-question { font-size: 1.15rem; line-height: 1.5; margin-bottom: 1.1rem; color: var(--text-main); }
        .vz-p-opts { display: flex; flex-direction: column; gap: 0.5rem; }
        .vz-p-opt, .vz-p-reveal {
            text-align: left;
            border: 1px solid var(--border-subtle);
            background: transparent;
            color: var(--text-main);
            border-radius: 10px;
            padding: 0.8rem 1rem;
            font-size: 0.9rem;
            cursor: pointer;
            transition: border-color 200ms, background-color 200ms;
        }
        .vz-p-opt:hover:not(:disabled), .vz-p-reveal:hover { border-color: var(--accent-primary); }
        .vz-p-opt:disabled { cursor: default; opacity: 0.75; }
        .vz-p-opt.is-right { border-color: var(--accent-primary); background: rgba(74, 222, 128, 0.14); opacity: 1; }
        .vz-p-opt.is-wrong { border-color: #ef4444; background: rgba(239, 68, 68, 0.12); opacity: 1; }
        .vz-p-answer { margin-top: 0.9rem; padding: 0.9rem 1rem; border-left: 3px solid var(--accent-primary); background: rgba(74, 222, 128, 0.06); font-size: 0.9rem; line-height: 1.6; }
        .vz-p-grade { display: flex; gap: 0.6rem; margin-top: 0.9rem; }
        .vz-p-grade .vz-p-opt { flex: 1; text-align: center; }
        .vz-p-why { margin-top: 0.9rem; font-size: 0.85rem; line-height: 1.6; color: var(--text-muted); }
        .vz-p-next {
            margin-top: 1.2rem; background: var(--accent-primary); color: #04120a;
            border: none; border-radius: 8px; padding: 0.7rem 1.3rem;
            font-weight: 700; font-size: 0.75rem; text-transform: uppercase;
            letter-spacing: 0.06em; cursor: pointer;
        }
        .vz-p-result { text-align: center; margin-bottom: 1.5rem; }
        .vz-p-big { font-family: 'JetBrains Mono', monospace; font-size: 2.6rem; font-weight: 700; color: var(--accent-primary); }
        .vz-p-h { font-size: 1rem; margin-bottom: 0.6rem; color: var(--text-main); }
        .vz-p-list { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.5rem; }
        .vz-p-list a { color: var(--accent-primary); }
        .vz-p-note { margin-top: 1rem; font-size: 0.8rem; color: var(--text-muted); }
"""

BODY = """
    <main class="flex-1 p-4 md:p-8 max-w-5xl mx-auto w-full">

        <div class="vz-p-wrap">
            <div class="mb-8 animate-fade-in">
                %(crumb)s
                <h1 class="text-3xl md:text-4xl font-bold brand-font tracking-tight" style="color: var(--text-main)">Practice</h1>
                <p class="mt-3 max-w-2xl text-base md:text-lg" style="color: var(--text-muted)">%(lead)s</p>
                <p class="vz-doc-updated">Updated <time datetime="%(iso)s">%(nice)s</time></p>
            </div>

            <section class="vz-p-panel animate-fade-in" id="practice-intro">
                <div class="vz-p-stats">
                    <div class="vz-p-stat"><b id="stat-visited">0</b><span>modules opened</span></div>
                    <div class="vz-p-stat"><b id="stat-bank">0</b><span>questions available</span></div>
                    <div class="vz-p-stat"><b id="stat-asked">0</b><span>practised so far</span></div>
                    <div class="vz-p-stat"><b id="stat-accuracy">&mdash;</b><span>accuracy here</span></div>
                </div>

                <p id="practice-note" style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.6;"></p>

                <div class="vz-p-controls" style="margin-top: 1.4rem;">
                    <div>
                        <label for="scope-select">Draw from</label>
                        <select id="scope-select">
                            <option value="visited" selected>modules I have opened</option>
                            <option value="all">every module</option>
%(tracks)s
                        </select>
                    </div>
                    <div>
                        <label for="length-select">Questions</label>
                        <select id="length-select">
                            <option value="5">5</option>
                            <option value="10" selected>10</option>
                            <option value="20">20</option>
                        </select>
                    </div>
                    <button type="button" class="vz-p-start" id="practice-start">Start</button>
                </div>

                <div id="practice-empty" hidden style="margin-top: 1.2rem; color: var(--text-muted); font-size: 0.9rem;"></div>
            </section>

            <section class="vz-p-panel animate-fade-in" id="practice-run" hidden>
                <div class="vz-p-head">
                    <span id="practice-count">0 / 0</span>
                    <span id="practice-score">0 right</span>
                </div>
                <div class="vz-p-meter"><div id="practice-bar"></div></div>
                <div id="practice-card"></div>
                <button type="button" class="vz-p-next" id="practice-next" hidden>Next question</button>
            </section>

            <section class="vz-p-panel animate-fade-in" id="practice-summary" hidden></section>

            <section class="mt-8" style="color: var(--text-muted); font-size: 0.85rem; line-height: 1.7;">
                <h2 class="text-sm uppercase tracking-widest mb-2" style="color: var(--accent-primary)">How this works</h2>
                <p>Every module ends with a check. Those answers are stored in your browser and
                nowhere else, and this page reads them back: a module you scored badly on, or
                have not seen for a fortnight, is more likely to come up than one you answered
                correctly this morning. Modules you have never been asked about here get a
                nudge upwards too, so the deck does not collapse onto your worst three topics.</p>
                <p>Questions are the modules' own &mdash; the multiple-choice ones where a module
                has authored questions, and recall prompts built from the page's own key
                takeaways everywhere else. Nothing is generated at read time, so an answer here
                cannot drift from the module it came from.</p>
                <p>No account, no backend, nothing leaves this device. Clearing your browser
                storage resets it.</p>
            </section>
        </div>

    </main>

    <script src="%(p)sassets/practice-bank.js"></script>
    <script src="%(p)sassets/practice.js"></script>
"""


def track_options():
    """One <option> per track, in catalog order, with its module count.

    Generated rather than hard-coded so a new track cannot be missing from
    the scope list, and the label cannot disagree with the `cat` the question
    bank actually carries - which is what the runtime filters on.
    """
    seen = []
    counts = {}
    for m in modules():
        cat = m["category"]
        if cat not in counts:
            seen.append(cat)
            counts[cat] = 0
        counts[cat] += 1
    return "\n".join(
        '                            <option value="track:%s">%s only (%d)</option>'
        % (html.escape(cat, quote=True), html.escape(cat), counts[cat])
        for cat in seen
    )


def build():
    parts = [
        shell.head_top(PRACTICE["title"] + " | VizLearn", PREFIX).replace(
            "/* page-specific rules go here; the shared system is in vizlearn.css */",
            CSS.strip("\n")),
        shell.header(PREFIX),
        BODY % {
            "crumb": shell.breadcrumb_bar([("Home", PREFIX + "index.html"),
                                           ("Practice", None)]),
            "lead": PRACTICE["lead"],
            "iso": last_modified(REL),
            "nice": pretty_date(last_modified(REL)),
            "p": PREFIX,
            "tracks": track_options(),
        },
        shell.close(PREFIX),
    ]
    return "".join(parts)


def main():
    path = os.path.join(ROOT, REL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(build())
    print("practice page             : %s" % REL)
    return 0


if __name__ == "__main__":
    sys.exit(main())
