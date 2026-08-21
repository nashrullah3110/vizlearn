#!/usr/bin/env python3
"""Render /js-lab/ - a full-page JavaScript editor.

The site's tracks are Python and SQL; this is a third scratchpad in the same
mould as /python-lab/ and /sql-lab/, for anyone whose question is "how do I
write JavaScript". No interpreter to download: the browser's own engine is
already here. assets/vizlearn-js.js runs the code in a Web Worker - so an
infinite loop is killed by a timeout instead of freezing the page - and mirrors
the console output into the panel below the editor.

Written whole on every build; no hand-edited regions.
"""

import sys

import lib_tool_page as tool

KEY = "js-lab"

CSS = """
        .vz-lab-grid { display: grid; gap: 1.25rem; grid-template-columns: 1fr; }
        @media (min-width: 1024px) {
            .vz-lab-grid { grid-template-columns: minmax(0, 1fr) 19rem; align-items: start; }
        }
        .vz-lab-grid .js-output { min-height: 150px; }

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

STARTER = '''// Real JavaScript, running on your browser's own engine.
// Nothing is sent to a server.
const tracks = ["Python", "SQL", "Algorithms", "Machine Learning"];
const lengths = tracks.map((t) => t.length);

for (const [i, t] of tracks.entries()) {
  console.log(t.padEnd(20) + " -> " + lengths[i] + " letters");
}

console.log("----");
console.log("longest :", tracks.reduce((a, b) => (b.length > a.length ? b : a)));
console.log("total   :", lengths.reduce((a, b) => a + b, 0));
console.log("shuffle :", tracks.slice().sort(() => Math.random() - 0.5));

// Try editing this, or delete it and write your own.
'''


def body():
    return """
            <div class="vz-js vz-ide" data-vz-js data-vz-ide="js-lab">
                <div class="vz-ide-pane vz-ide-code">
                <script type="text/plain" class="js-src">%(starter)s</script>
                <div class="vz-code-bar">
                    <span class="vz-code-dot"></span><span>main.js</span>
                    <span class="vz-code-lang">JavaScript</span>
                </div>
                <!-- The textarea keeps .js-editor: assets/vizlearn-js.js reads
                     .value off it. The highlighter only layers a <pre> behind it. -->
                <div class="vz-code" data-vz-code="javascript">
                    <div class="vz-code-gutter" aria-hidden="true"></div>
                    <div class="vz-code-scroll">
                        <pre class="vz-code-hl" aria-hidden="true"></pre>
                        <textarea class="vz-code-input js-editor" aria-label="JavaScript code editor"
                                  spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>
                    </div>
                </div>
                <div class="js-controls">
                    <button type="button" class="js-run-btn">Run</button>
                    <button type="button" class="js-reset-btn">Reset</button>
                    <span class="js-status"></span>
                </div>
                </div>
                <div class="vz-ide-split" role="separator" tabindex="0"
                     aria-orientation="vertical" aria-label="Resize editor and output"
                     aria-valuemin="20" aria-valuemax="80" aria-valuenow="50"></div>
                <div class="vz-ide-pane vz-ide-out">
                <div class="vz-console">
                    <div class="vz-console-bar">Output</div>
                    <!-- .js-output stays: vizlearn-js.js writes into it. -->
                    <pre class="vz-console-body js-output" aria-live="polite"
                         data-empty="Press Run to execute this code."></pre>
                </div>
                </div>
            </div>

        <div class="vz-lab-docs">
                <section class="vz-lab-side">
                    <h2>What this is</h2>
                    <p>Your browser&rsquo;s own JavaScript engine, running your code in a
                    worker thread. Nothing is uploaded, and the page works fully
                    offline.</p>
                    <p><code>console.log</code> prints objects as JSON, arrays in full,
                    and the <code>print</code> alias works too.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>What works</h2>
                    <ul>
                        <li>Template literals, arrow functions, destructuring,
                            <code>async</code>/<code>await</code> inside functions.</li>
                        <li>The whole language &mdash; this is the real engine, not a
                            simulator.</li>
                        <li>An infinite loop is stopped after 10 seconds instead of
                            freezing the tab.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>What does not</h2>
                    <ul>
                        <li><code>document</code> and <code>window</code> &mdash; there is
                            no page here, so no DOM.</li>
                        <li>Top-level <code>await</code> &mdash; wrap it in an
                            <code>async</code> function instead.</li>
                        <li>File system access, and <code>input()</code>-style prompts.</li>
                    </ul>
                </section>

                                <section class="vz-lab-side">
                    <h2>How it runs</h2>
                    <p>Your browser already contains a fast JavaScript engine, so there is
                    nothing to download and nothing to compile. The code runs in a worker
                    thread rather than on the page, which means it cannot touch this
                    document, and an accidental infinite loop stops the worker instead of
                    freezing the tab.</p>
                    <p>Because it is the real engine, everything modern JavaScript has is
                    here: <code>let</code> and <code>const</code>, arrow functions,
                    destructuring, spread, classes, template literals, optional chaining,
                    <code>Map</code>, <code>Set</code>, generators and modules-level syntax
                    that does not need imports.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Asynchronous code</h2>
                    <p><code>Promise</code>, <code>async</code> and <code>await</code> all
                    work, as do <code>setTimeout</code> and <code>queueMicrotask</code>. A
                    top-level <code>await</code> is allowed, so you can write
                    <code>const x = await something()</code> without wrapping it in a
                    function.</p>
                    <p>This makes the lab a good place to settle what the event loop
                    actually does. Log something before a promise, inside it, and after it,
                    then predict the order before pressing Run. The result is usually not
                    what people expect the first time, and seeing it is worth more than
                    reading about microtask queues.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>What the console shows</h2>
                    <p><code>console.log</code>, <code>warn</code>, <code>error</code> and
                    <code>info</code> are captured and mirrored into the output panel, and
                    <code>print</code> works as an alias. Objects and arrays are shown in
                    full rather than as <code>[object Object]</code>, which is the usual
                    frustration when debugging in a plain terminal.</p>
                    <p>Errors arrive with their stack, and the three you will meet most are
                    <code>ReferenceError</code> for a name that does not exist,
                    <code>TypeError</code> for calling something that is not a function or
                    reading a property of <code>undefined</code>, and
                    <code>SyntaxError</code> for code that could not be parsed at all.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Things worth trying</h2>
                    <ul>
                        <li>Compare <code>==</code> with <code>===</code> across a few
                            values and see exactly which coercions happen.</li>
                        <li>Log <code>0.1 + 0.2</code>. Floating point is the same
                            everywhere, and seeing it once explains a great many bug
                            reports.</li>
                        <li>Order a mix of <code>setTimeout</code>, a resolved promise and
                            plain statements, and predict the output before running.</li>
                        <li>Use <code>map</code>, <code>filter</code> and
                            <code>reduce</code> on an array, then write the same thing as a
                            loop and decide which reads better.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>Looking for a language lab?</h2>
                    <p>The <a href="%(p)spython-lab/">Python compiler</a> runs real
                    CPython in the same spirit, and the
                    <a href="%(p)ssql-lab/">SQL playground</a> backs a real SQLite
                    database.</p>
                </section>
            </div>
        </div>

""" % {"starter": STARTER.strip(), "p": "%(p)s"}


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, body(), wide=True, app=True))
    print("js lab page               : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
