#!/usr/bin/env python3
"""Render /map/ - how the tracks connect and what each one builds on.

Navigation has only ever been linear: prev/next within a track, and a rail of
four neighbours. Neither shows that Deep Learning's gradient descent rests on
Maths' derivatives, or that four different specialisms fan out of the same
foundation - which is the question someone deciding what to learn next is
actually asking.

Two layers, both derived rather than hand-drawn:

  the spine   LEARNING_PATH from tools/sequence.py: the curated cross-track
              route, five stages, already used by the hub's Learning Path.
  the lanes   SEQUENCE per track, in teaching order, so each lane reads as
              "each of these leans on the ones above it".

Progress is layered on in the browser, from the same localStorage store the
hub and /practice/ read, so the map shows where you actually are.

Written whole on every build; there are no hand-edited regions.
"""

import html
import json
import os
import sys

import lib_tool_page as tool
from lib_catalog import ROOT, modules
from lib_pages import TOPICS, TOPIC_ORDER
from sequence import LEARNING_PATH, SEQUENCE

KEY = "map"
# The runtime lives in assets/vizlearn-map.js; this is only its data.
JS_OUT = os.path.join(ROOT, "assets", "map-data.js")

CSS = """
        .vz-m-controls {
            display: flex; flex-wrap: wrap; gap: 1rem; align-items: center;
            margin-bottom: 1.75rem; font-size: 0.8rem; color: var(--text-muted);
        }
        .vz-m-controls label { display: flex; align-items: center; gap: 0.5rem; cursor: pointer; }
        .vz-m-controls input { accent-color: var(--accent-primary); width: 1rem; height: 1rem; }

        .vz-m-h {
            font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.11em;
            color: var(--accent-primary); margin: 0 0 0.9rem;
        }

        /* --- the spine --- */
        .vz-m-spine { display: grid; gap: 0.75rem; margin-bottom: 3rem; }
        @media (min-width: 900px) { .vz-m-spine { grid-template-columns: repeat(5, 1fr); } }
        .vz-m-stage {
            border: 1px solid var(--border-subtle);
            border-radius: 12px; padding: 0.9rem;
            background: var(--card-bg);
            position: relative;
        }
        .vz-m-stage-n {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.62rem; color: var(--accent-primary);
        }
        .vz-m-stage h3 { font-size: 0.9rem; color: var(--text-main); margin: 0.2rem 0 0.35rem; }
        .vz-m-stage p { font-size: 0.75rem; color: var(--text-muted); line-height: 1.55; margin: 0 0 0.6rem; }

        /* --- lanes --- */
        .vz-m-lane { margin-bottom: 2rem; }
        .vz-m-lane-top {
            display: flex; justify-content: space-between; align-items: baseline;
            gap: 1rem; margin-bottom: 0.6rem;
            padding-bottom: 0.35rem; border-bottom: 1px solid var(--border-subtle);
        }
        .vz-m-lane-top h3 { font-size: 1rem; color: var(--text-main); margin: 0; }
        .vz-m-count {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem; color: var(--text-muted); white-space: nowrap;
        }
        .vz-m-chips { display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; }

        .vz-m-chip {
            display: inline-block;
            border: 1px solid var(--border-subtle);
            border-radius: 999px;
            padding: 0.25rem 0.7rem;
            font-size: 0.78rem;
            color: var(--text-main);
            text-decoration: none;
            white-space: nowrap;
            max-width: 15rem; overflow: hidden; text-overflow: ellipsis;
        }
        .vz-m-chip:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
        .vz-m-chip.is-done {
            background: rgba(74, 222, 128, 0.12);
            border-color: var(--accent-primary);
            color: var(--accent-primary);
        }
        .vz-m-chip.is-done::before { content: "\\2713\\00a0"; }
        /* The arrow is the only thing carrying "builds on" between chips, so it
           is decorative and hidden from the accessibility tree in the markup. */
        .vz-m-arrow { color: var(--text-muted); opacity: 0.4; font-size: 0.7rem; }

        .vz-m-bar {
            height: 4px; border-radius: 2px; background: var(--border-subtle);
            overflow: hidden; margin-top: 0.5rem;
        }
        .vz-m-bar div { height: 100%; background: var(--accent-primary); width: 0; transition: width 300ms; }
"""

BODY = """
            <div class="vz-m-controls">
                <label><input type="checkbox" id="map-hide-done"> Hide modules I have opened</label>
                <span id="map-summary"></span>
            </div>

            <h2 class="vz-m-h">The through-line</h2>
            <p style="font-size:.85rem;color:var(--text-muted);line-height:1.7;margin:-0.4rem 0 1rem">
                One route across the tracks, in the order the ideas depend on each other.
                Everything below is the same modules arranged by track instead.</p>
            <div class="vz-m-spine" id="map-spine"></div>

            <h2 class="vz-m-h">Every track, in teaching order</h2>
            <p style="font-size:.85rem;color:var(--text-muted);line-height:1.7;margin:-0.4rem 0 1.2rem">
                Each module leans on the ones before it in its own lane. Follow a lane
                left to right, or jump in wherever the names stop being familiar.</p>
            <div id="map-lanes"></div>

            <p class="vz-t-note">Ticks come from the modules you have opened on this
            device, the same record the hub and <a href="%(p)spractice/">Practice</a>
            read. Nothing is uploaded.</p>

    <script defer src="%(p)sassets/map-data.js"></script>
    <script defer src="%(p)sassets/vizlearn-map.js"></script>
"""


def graph():
    """The map's data: the spine, then each track's sequence in order."""
    by_path = {m["path"]: m for m in modules()}

    def node(path):
        m = by_path.get(path)
        if not m:
            return None
        return {"path": path, "title": m["title"]}

    spine = []
    for i, stage in enumerate(LEARNING_PATH):
        spine.append({
            "n": i + 1,
            "title": stage["title"],
            "blurb": stage["blurb"],
            "mods": [n for n in (node(p) for p in stage["modules"]) if n],
        })

    lanes = []
    for key in TOPIC_ORDER:
        t = TOPICS[key]
        # SEQUENCE is keyed by the courseData topic key, which is what
        # apply_sequence.py already reorders the catalog with.
        paths = SEQUENCE.get(key) or SEQUENCE.get(t["dir"]) or []
        mods = [n for n in (node(p) for p in paths) if n]
        if not mods:
            continue
        lanes.append({"key": key, "title": t["title"], "mods": mods})

    return {"spine": spine, "lanes": lanes}


def build_js(data):
    return ("/* GENERATED FILE - do not edit by hand.\n"
            " * Source: tools/sequence.py via tools/build_map.py\n"
            " */\n"
            "window.VIZLEARN_MAP = %s;\n" % json.dumps(data, ensure_ascii=False))


def main():
    data = graph()
    rel = tool.write(KEY, tool.render(KEY, CSS, BODY, wide=True))
    open(JS_OUT, "w", encoding="utf-8").write(build_js(data))
    n = sum(len(l["mods"]) for l in data["lanes"])
    print("map page                  : %s (%d lanes, %d modules, %d stages)"
          % (rel, len(data["lanes"]), n, len(data["spine"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
