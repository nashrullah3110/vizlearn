#!/usr/bin/env python3
"""Render /python-lab/ - a full-page Python editor.

The python/ track already runs real CPython: assets/vizlearn-python.js loads
Pyodide into a Web Worker and wires any `.vz-py` block on the page. Every page
already loads it. So this page is almost entirely markup - it supplies one
large block against the same contract rather than reimplementing anything.

The difference from a module page is scope. A module's editor is three lines
next to an explanation; this is a scratchpad you can paste a whole script into,
with a starter that shows the interpreter is genuinely Python and not a
simulation.

Written whole on every build; no hand-edited regions.
"""

import sys

import lib_tool_page as tool

KEY = "python-lab"

CSS = """
        .vz-lab-grid { display: grid; gap: 1.25rem; grid-template-columns: 1fr; }
        @media (min-width: 1024px) {
            .vz-lab-grid { grid-template-columns: minmax(0, 1fr) 19rem; align-items: start; }
        }
        /* The editor is the point of the page, so it gets real height rather
           than the few lines a module needs beside its prose. */
        .vz-lab-grid .py-editor { min-height: 340px; font-size: 0.9rem; }
        .vz-lab-grid .py-output { min-height: 150px; }

        .vz-lab-side {
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            background: var(--card-bg);
            padding: 1rem 1.1rem;
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

STARTER = '''# Real Python, running in your browser. Nothing is sent to a server.
from collections import Counter
import math

words = "the quick brown fox jumps over the lazy dog the fox".split()
counts = Counter(words)

for word, n in counts.most_common(3):
    print(f"{word:>6} x{n}")

print()
print("unique words :", len(counts))
print("sqrt(2)      :", round(math.sqrt(2), 6))

# Try editing this, or delete it and write your own.
'''


def body():
    return """
        <div class="vz-lab-grid">
            <div class="vz-py" data-vz-py>
                <script type="text/plain" class="py-src">%(starter)s</script>
                <textarea class="py-editor" aria-label="Python code editor" spellcheck="false"></textarea>
                <div class="py-controls">
                    <button type="button" class="py-run-btn">Run</button>
                    <button type="button" class="py-reset-btn">Reset</button>
                    <span class="py-status"></span>
                </div>
                <pre class="py-output" aria-live="polite"></pre>
            </div>

            <div>
                <section class="vz-lab-side">
                    <h2>What this is</h2>
                    <p>CPython compiled to WebAssembly, running on your own machine. Your
                    code is never uploaded, and the page works offline once it has loaded
                    the interpreter.</p>
                    <p>The first <code>Run</code> takes a few seconds while the interpreter
                    downloads. Every run after that is immediate.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>What works</h2>
                    <ul>
                        <li>The standard library &mdash; <code>math</code>, <code>json</code>,
                            <code>re</code>, <code>collections</code>, <code>itertools</code>,
                            <code>datetime</code> and the rest.</li>
                        <li><code>print</code>, f-strings, comprehensions, classes, generators.</li>
                        <li>Tracebacks, in full. A mistake here reads exactly as it would in a terminal.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>What does not</h2>
                    <ul>
                        <li><code>input()</code> &mdash; there is no stdin to read from.</li>
                        <li>Reading or writing files on your computer.</li>
                        <li>Network calls, and packages that need to be installed.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>Learning Python?</h2>
                    <p>The <a href="%(p)spython/">Python track</a> teaches it one idea at a
                    time, each with an editor like this one beside the explanation &mdash;
                    starting at <a href="%(p)spython/hello_python.html">your first print
                    statement</a>.</p>
                </section>
            </div>
        </div>
""" % {"starter": STARTER.strip(), "p": "%(p)s"}


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, body(), wide=True))
    print("python lab page           : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
