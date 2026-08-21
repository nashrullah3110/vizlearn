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
            <div class="vz-py vz-ide" data-vz-py data-vz-ide="python-lab">
                <div class="vz-ide-pane vz-ide-code">
                <script type="text/plain" class="py-src">%(starter)s</script>
                <div class="vz-code-bar">
                    <span class="vz-code-dot"></span><span>main.py</span>
                    <span class="vz-code-lang">Python 3</span>
                </div>
                <!-- The textarea keeps .py-editor: assets/vizlearn-python.js reads
                     .value off it. The highlighter only layers a <pre> behind it. -->
                <div class="vz-code" data-vz-code="python">
                    <div class="vz-code-gutter" aria-hidden="true"></div>
                    <div class="vz-code-scroll">
                        <pre class="vz-code-hl" aria-hidden="true"></pre>
                        <textarea class="vz-code-input py-editor" aria-label="Python code editor"
                                  spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>
                    </div>
                </div>
                <div class="py-controls">
                    <button type="button" class="py-run-btn">Run</button>
                    <button type="button" class="py-reset-btn">Reset</button>
                    <span class="py-status"></span>
                </div>
                </div>
                <div class="vz-ide-split" role="separator" tabindex="0"
                     aria-orientation="vertical" aria-label="Resize editor and output"
                     aria-valuemin="20" aria-valuemax="80" aria-valuenow="50"></div>
                <div class="vz-ide-pane vz-ide-out">
                <div class="vz-console">
                    <div class="vz-console-bar">Output</div>
                    <!-- .py-output stays: vizlearn-python.js writes into it. -->
                    <pre class="vz-console-body py-output" aria-live="polite"
                         data-empty="Press Run to execute this code."></pre>
                </div>
                </div>
            </div>

        <div class="vz-lab-docs">
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
                    <h2>How it runs</h2>
                    <p>This is not Python translated into JavaScript. It is CPython itself
                    &mdash; the same interpreter you would install &mdash; compiled to
                    WebAssembly by the Pyodide project and executed by your browser.
                    Semantics match a normal interpreter because it <em>is</em> one.</p>
                    <p>It runs in a worker thread, separate from the page. That is why an
                    accidental infinite loop freezes the output rather than the whole tab,
                    and why the editor stays responsive while your code is running. A run
                    that has not finished within ten seconds is stopped and reported, which
                    is almost always a loop that never exits.</p>
                    <p>The first run downloads the interpreter, which takes a few seconds
                    on a normal connection. After that it is cached, so subsequent runs
                    start immediately, and the page keeps working with no connection at
                    all.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Reading a traceback</h2>
                    <p>Errors appear exactly as they would in a terminal, and they are worth
                    reading from the bottom up. The last line names the exception and the
                    message; the lines above it show the call path that reached it, most
                    recent last.</p>
                    <p>The four you will meet earliest:
                    <code>SyntaxError</code> means the file could not be parsed at all, so
                    nothing ran &mdash; usually a missing bracket or colon on the line
                    <em>before</em> the one reported.
                    <code>NameError</code> means a name was used before it was defined,
                    which is often a typo.
                    <code>TypeError</code> means an operation met a type it cannot handle,
                    such as adding a string to a number.
                    <code>IndentationError</code> means the whitespace does not describe a
                    consistent block.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Files, timing and limits</h2>
                    <p>There is an in-memory filesystem, so <code>open</code>,
                    <code>read</code> and <code>write</code> all work normally. The files
                    are real for the length of the run and gone afterwards, which makes this
                    a genuine place to practise file handling without touching your
                    computer.</p>
                    <p><code>time.perf_counter</code> works and is accurate enough to
                    compare two approaches, though everything runs slower than a native
                    interpreter &mdash; often several times slower. Relative comparisons hold;
                    absolute numbers do not transfer.</p>
                    <p>Recursion is limited by the browser stack, which is smaller than a
                    desktop Python's. Deep recursion raises rather than crashing, and an
                    iterative version will usually run where a recursive one will not.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Things worth trying</h2>
                    <ul>
                        <li>Paste code from anywhere and run it. Nothing is uploaded, so
                            there is no reason not to.</li>
                        <li>Break something deliberately &mdash; index past the end of a list,
                            divide by zero, misspell a method &mdash; and read what comes
                            back. Recognising tracebacks is most of debugging.</li>
                        <li>Compare two approaches with <code>time.perf_counter</code>: a
                            loop against a comprehension, a list against a set for membership
                            tests.</li>
                        <li>Use <code>collections.Counter</code>, <code>itertools</code> and
                            <code>json</code> &mdash; the standard library is all here, and it
                            is larger than most people use.</li>
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
    rel = tool.write(KEY, tool.render(KEY, CSS, body(), wide=True, app=True))
    print("python lab page           : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
