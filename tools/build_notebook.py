#!/usr/bin/env python3
"""Render /notebook/ - a cell-based Python notebook with the data stack.

The other labs run one program in a fresh namespace. A notebook is the
opposite: many small cells sharing one kernel, where cell four depends on the
name cell two bound. That is a different execution model, so it has its own
engine in assets/vizlearn-notebook.js rather than another attribute on the
one-shot runner.

NumPy, pandas and Matplotlib are all Pyodide packages, so they come from the
same CDN as the interpreter - no wheels, unlike /fastapi-lab/. Matplotlib
needs one thing said to it: there is no DOM in a worker, so its default
Pyodide backend cannot attach and it is switched to Agg before pyplot is ever
imported. Figures are then drawn to PNG after each cell and sent up as images.

The starter cells are a worked example rather than a feature tour: one small
table, carried through describe, a filter, a groupby and a chart, so that
running them top to bottom tells a story about the same data.

Written whole on every build; no hand-edited regions.
"""

import html
import sys

import lib_tool_page as tool

KEY = "notebook"

CSS = """
        .vz-nb-wrap { display: grid; gap: 1.25rem; grid-template-columns: 1fr; }
        @media (min-width: 1180px) {
            .vz-nb-wrap { grid-template-columns: minmax(0, 1fr) 19rem; align-items: start; }
        }
        /* A grid item is min-width:auto by default, so it refuses to go
           narrower than its widest line. One long comment in a cell was
           enough to push the notebook 550px past the viewport and take the
           whole page's layout with it. The editor already knows how to
           scroll; it just has to be allowed to be narrow. */
        .vz-nb-wrap > * { min-width: 0; }
        .vz-nb, .vz-nb-cells, .vz-nb-cell, .vz-nb-out { min-width: 0; }

        .vz-nb-bar {
            display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem;
            padding: 0.6rem 0.75rem; margin-bottom: 0.9rem;
            border: 1px solid var(--border-subtle); border-radius: 10px;
            background: var(--card-bg);
        }
        .vz-nb-bar button {
            font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
            letter-spacing: 0.06em; text-transform: uppercase;
            padding: 0.4rem 0.7rem; border-radius: 6px;
            border: 1px solid var(--border-subtle);
            background: var(--input-bg); color: var(--text-main); cursor: pointer;
        }
        .vz-nb-bar button:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
        .vz-nb-status {
            font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
            color: var(--text-muted); margin-left: auto;
        }

        .vz-nb-cell {
            border: 1px solid var(--border-subtle); border-radius: 10px;
            background: var(--card-bg); margin-bottom: 0.9rem; overflow: hidden;
        }
        .vz-nb-cell.is-running { border-color: var(--accent-primary); }
        .vz-nb-head {
            display: flex; align-items: center; gap: 0.5rem;
            padding: 0.35rem 0.6rem; border-bottom: 1px solid var(--border-subtle);
        }
        .vz-nb-count {
            font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
            color: var(--text-muted); min-width: 2.6rem;
        }
        .vz-nb-head button {
            font-family: 'JetBrains Mono', monospace; font-size: 0.68rem;
            padding: 0.2rem 0.5rem; border-radius: 5px;
            border: 1px solid var(--border-subtle);
            background: transparent; color: var(--text-muted); cursor: pointer;
        }
        .vz-nb-head button:hover { border-color: var(--accent-primary); color: var(--accent-primary); }
        .vz-nb-run { margin-left: auto; }

        /* The editor grows with its content: a cell should be as tall as what
           it holds, not a fixed box with a scrollbar of its own. */
        .vz-nb-cell .vz-code { border: 0; border-radius: 0; }
        .vz-nb-cell .vz-code-input, .vz-nb-cell .vz-code-hl {
            min-height: 44px; resize: none;
        }

        .vz-nb-out:empty { display: none; }
        .vz-nb-out {
            border-top: 1px solid var(--border-subtle);
            padding: 0.7rem 0.85rem; background: var(--input-bg);
        }
        .vz-nb-out pre {
            font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
            line-height: 1.55; white-space: pre-wrap; word-break: break-word;
            color: var(--text-main); margin: 0;
        }
        .vz-nb-out pre + pre, .vz-nb-out pre + .vz-nb-table { margin-top: 0.5rem; }
        .vz-nb-stderr { color: #dc2626; }
        :root:not([data-theme="light"]) .vz-nb-stderr { color: #f87171; }
        @media (prefers-color-scheme: dark) {
            :root:not([data-theme="light"]) .vz-nb-stderr { color: #f87171; }
        }
        .vz-nb-value { color: var(--accent-primary); }

        .vz-nb-fig {
            display: block; max-width: 100%; height: auto; margin: 0.6rem 0 0;
            border-radius: 6px; background: #fff;
        }

        /* Pandas ships its own table markup, which knows nothing about this
           site's palette. These rules are what make it look like it belongs. */
        .vz-nb-table { overflow-x: auto; margin-top: 0.6rem; }
        .vz-nb-table table {
            border-collapse: collapse; font-size: 0.78rem;
            font-family: 'JetBrains Mono', monospace; color: var(--text-main);
        }
        .vz-nb-table th, .vz-nb-table td {
            border: 1px solid var(--border-subtle);
            padding: 0.28rem 0.6rem; text-align: right; white-space: nowrap;
        }
        .vz-nb-table thead th { background: var(--card-bg); color: var(--text-muted); font-weight: 700; }
        .vz-nb-table tbody th { background: var(--card-bg); color: var(--text-muted); }

        .vz-lab-side {
            border: 1px solid var(--border-subtle); border-radius: 12px;
            background: var(--card-bg); padding: 1rem 1.1rem;
        }
        .vz-lab-side h2 {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem; font-weight: 700;
            letter-spacing: 0.16em; text-transform: uppercase;
            color: var(--accent-primary); margin-bottom: 0.6rem;
        }
        .vz-lab-side p, .vz-lab-side li {
            font-size: 0.86rem; line-height: 1.6; color: var(--text-muted);
        }
        .vz-lab-side ul { list-style: disc; padding-left: 1.15rem; display: grid; gap: 0.4rem; }
        .vz-lab-side + .vz-lab-side { margin-top: 1rem; }
        .vz-lab-side code {
            font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
            background: var(--input-bg); border: 1px solid var(--border-subtle);
            border-radius: 4px; padding: 0.05em 0.3em; color: var(--text-main);
        }
        .vz-lab-side a { color: var(--accent-primary); text-decoration: none; }
        .vz-lab-side a:hover { text-decoration: underline; }
"""

# One table, carried all the way through. Each cell should be worth running on
# its own, and worth running after the one above it.
CELLS = [
    """# Shift+Enter runs a cell. Names stay put, so cell 2 can use what cell 1 made.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("numpy", np.__version__, "| pandas", pd.__version__)""",

    """# A cell ending in an expression shows its value - no print() needed.
sales = pd.DataFrame({
    "city":   ["Delhi", "Mumbai", "Pune", "Delhi", "Mumbai", "Pune"],
    "month":  ["Jan", "Jan", "Jan", "Feb", "Feb", "Feb"],
    "units":  [120, 195, 74, 138, 172, 96],
    "price":  [249.0, 249.0, 199.0, 249.0, 229.0, 199.0],
})
sales""",

    """# A DataFrame renders as a table, so describe() is readable rather than a wall.
sales["revenue"] = sales["units"] * sales["price"]
sales.describe()""",

    """# Filtering and sorting. Try changing 100 to 150 and running this cell again.
sales[sales["units"] > 100].sort_values("revenue", ascending=False)""",

    """# groupby: the operation pandas exists for.
by_city = sales.groupby("city")["revenue"].sum().sort_values(ascending=False)
by_city""",

    """# Plots appear under the cell. plt.show() is optional here.
fig, ax = plt.subplots(figsize=(6, 3))
by_city.plot(kind="bar", ax=ax, color="#4f7fd4")
ax.set_ylabel("revenue")
ax.set_title("Revenue by city")
ax.tick_params(axis="x", rotation=0)
plt.tight_layout()""",

    """# NumPy on its own: no loop, and the whole array at once.
rng = np.random.default_rng(0)
walk = rng.normal(0, 1, 400).cumsum()

fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(walk, linewidth=1.2, color="#4f7fd4")
ax.axhline(0, color="#999", linewidth=0.8, linestyle="--")
ax.set_title("A random walk, and how far it wanders")
plt.tight_layout()

print("ends at", round(walk[-1], 2), "| furthest", round(np.abs(walk).max(), 2))""",

    """# Your turn. Try sales.pivot_table(index="city", columns="month", values="revenue")
""",
]


def esc(s):
    return html.escape(s, quote=False)


def cell_markup(code, in_template=False):
    """One notebook cell. The template carries the same shape with no source."""
    src = ('<script type="text/plain" class="vz-nb-src">%s</script>\n                        '
           % code.rstrip()) if not in_template else ''
    if "</script" in code.lower():
        raise SystemExit("a starter cell contains </script and would break out of the tag")
    return """<div class="vz-nb-cell">
                        %s<div class="vz-nb-head">
                            <span class="vz-nb-count">[ ]</span>
                            <button type="button" class="vz-nb-del" title="Delete this cell">Del</button>
                            <button type="button" class="vz-nb-run" title="Run this cell (Shift+Enter)">Run</button>
                        </div>
                        <div class="vz-code" data-vz-code="python">
                            <div class="vz-code-gutter" aria-hidden="true"></div>
                            <div class="vz-code-scroll">
                                <pre class="vz-code-hl" aria-hidden="true"></pre>
                                <textarea class="vz-code-input vz-nb-input" aria-label="Notebook cell"
                                          spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>
                            </div>
                        </div>
                        <div class="vz-nb-out"></div>
                    </div>""" % src


def body():
    cells = "\n                    ".join(
        cell_markup(c).replace("%", "%%") for c in CELLS)
    return """
        <div class="vz-nb-wrap">
            <div>
            <div class="vz-nb" data-vz-nb data-vz-packages="numpy,pandas,matplotlib">
                <!-- Cloned by the Add Cell button. Same shape, no source. -->
                <template class="vz-nb-template">%(template)s</template>

                <div class="vz-nb-bar">
                    <button type="button" class="vz-nb-runall">Run all</button>
                    <button type="button" class="vz-nb-add">Add cell</button>
                    <button type="button" class="vz-nb-restart" title="Forget every name and start over">Restart kernel</button>
                    <span class="vz-nb-status"></span>
                </div>

                <div class="vz-nb-cells">
                    %(cells)s
                </div>
            </div>
            </div>

            <div>
                <section class="vz-lab-side">
                    <h2>What this is</h2>
                    <p>A notebook running CPython 3.12 with NumPy, pandas and
                    Matplotlib, all compiled to WebAssembly and executing on your own
                    machine. Nothing is uploaded and there is nothing to install.</p>
                    <p>The first run downloads the interpreter and the three libraries,
                    which takes a while and only happens once per visit.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>How a notebook differs</h2>
                    <p>The other editors on this site run one program in a fresh
                    namespace every time. Here the cells share one kernel: a name bound
                    in cell two is still there in cell five, and running a cell again
                    changes what the cells below it would now see.</p>
                    <p>That is the whole idea, and it is also the classic way to confuse
                    yourself &mdash; output can reflect a definition you have since
                    edited. <code>Restart kernel</code> forgets everything, and
                    <code>Run all</code> from the top proves the notebook still works in
                    the order it is written.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Keys and controls</h2>
                    <ul>
                        <li><code>Shift+Enter</code> runs the cell you are in.</li>
                        <li><code>Run all</code> runs every cell from the top, in order.</li>
                        <li><code>Add cell</code> puts a new one at the bottom.</li>
                        <li>The number beside a cell is the order it last ran in, so
                            you can tell what is stale.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>What renders</h2>
                    <ul>
                        <li>A cell ending in an expression shows that value, with no
                            <code>print()</code>.</li>
                        <li>DataFrames and Series come out as tables.</li>
                        <li>Matplotlib figures appear under the cell as images.
                            <code>plt.show()</code> is optional.</li>
                        <li><code>print()</code> and full tracebacks, as a terminal
                            would show them.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>What does not work</h2>
                    <ul>
                        <li><code>input()</code> &mdash; there is no stdin.</li>
                        <li>Network calls, so no <code>read_csv</code> from a URL. Build
                            a DataFrame from a dict, or paste the data in.</li>
                        <li>Reading files from your computer. There is an in-memory
                            filesystem, so <code>to_csv</code> and <code>read_csv</code>
                            work on paths that live for the session.</li>
                        <li>Libraries beyond these three and the standard library.
                            SciPy, scikit-learn and Seaborn are not loaded.</li>
                        <li><code>%%%%matplotlib inline</code> and other IPython magics.
                            Plots are inline anyway.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>Speed, honestly</h2>
                    <p>WebAssembly runs several times slower than a native interpreter,
                    and everything happens on one core. Vectorised NumPy and pandas
                    still beat a Python loop by the same wide margin here, so the
                    lesson those comparisons teach holds &mdash; but a timing you take
                    on this page is not a timing you can quote for a laptop.</p>
                    <p>A cell is stopped after thirty seconds. That restarts the kernel,
                    which means every name is gone, so reach for <code>Run all</code>
                    after it happens.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Somewhere to start</h2>
                    <ul>
                        <li><code>sales.pivot_table(index="city", columns="month",
                            values="revenue")</code></li>
                        <li>Add a column with <code>np.where</code> and group by it.</li>
                        <li>Plot two series on one axis and give it a legend.</li>
                        <li>Time a Python loop against the NumPy equivalent with
                            <code>time.perf_counter</code>.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>The other editors</h2>
                    <p>The <a href="%(p)spython-lab/">Python compiler</a> runs one script
                    at a time without the libraries, and the
                    <a href="%(p)spython/">Python track</a> teaches the language one idea
                    at a time. For the maths under NumPy, the
                    <a href="%(p)smaths/">Maths track</a> covers vectors and matrices
                    with the same run-it-yourself approach.</p>
                </section>
            </div>
        </div>

""" % {"cells": cells, "template": cell_markup("", in_template=True).replace("%", "%%"), "p": "%(p)s"}


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, body(), wide=True, app=True))
    print("notebook page             : %s (%d starter cells)" % (rel, len(CELLS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
