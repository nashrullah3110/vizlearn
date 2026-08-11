#!/usr/bin/env python3
"""Render /html-lab/ - a full-page HTML editor.

The fourth scratchpad (after /python-lab/, /sql-lab/ and /js-lab/): write
markup and see it render, with no tooling and nothing downloaded. The preview
is a sandboxed <iframe> (allow-scripts only), so the page you write is fully
isolated - it cannot reach the site around it, and it cannot reach the
network. assets/vizlearn-html.js forwards the preview's console into the
panel under the editor.

Written whole on every build; no hand-edited regions.
"""

import sys

import lib_tool_page as tool

KEY = "html-lab"

CSS = """
        .vz-lab-grid { display: grid; gap: 1.25rem; grid-template-columns: 1fr; }
        @media (min-width: 1024px) {
            .vz-lab-grid { grid-template-columns: minmax(0, 1fr) 19rem; align-items: start; }
        }
        .vz-lab-grid .html-editor { min-height: 16rem; }

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

STARTER = '''<h1>Hello from the browser</h1>
<p>Edit this markup and press <strong>Run</strong>. The preview is a sandboxed
iframe &mdash; your page cannot touch the site around it, and nothing is sent
to a server.</p>

<button onclick="document.body.style.background = '#fde68a'">Warm it up</button>

<style>
  body { font-family: Georgia, serif; max-width: 34rem; margin: 2rem auto;
         padding: 0 1rem; color: #1f2937; line-height: 1.6; }
  h1 { color: #b45309; }
</style>

<script>
  console.log("This page is alive:", document.title || "an untitled document");
  console.log("Headings:", document.querySelectorAll("h1, h2").length);
</script>
'''


def body():
    # The starter is embedded in a <script type="text/plain"> block, where a
    # literal </script> would end the block early. Escape the closing tag so the
    # browser keeps the whole starter; assets/vizlearn-html.js unescapes it.
    starter = STARTER.strip().replace("</script>", "<\\/script>")
    return """
        <div class="vz-lab-grid">
            <div class="vz-html" data-vz-html>
                <script type="text/plain" class="html-src">%(starter)s</script>
                <div class="vz-code-bar">
                    <span class="vz-code-dot"></span><span>index.html</span>
                    <span class="vz-code-lang">HTML</span>
                </div>
                <!-- The textarea keeps .html-editor: assets/vizlearn-html.js reads
                     .value off it. The highlighter only layers a <pre> behind it. -->
                <div class="vz-code" data-vz-code="html">
                    <div class="vz-code-gutter" aria-hidden="true"></div>
                    <div class="vz-code-scroll">
                        <pre class="vz-code-hl" aria-hidden="true"></pre>
                        <textarea class="vz-code-input html-editor" aria-label="HTML code editor"
                                  spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>
                    </div>
                </div>
                <div class="html-controls">
                    <button type="button" class="html-run-btn">Run</button>
                    <button type="button" class="html-reset-btn">Reset</button>
                    <span class="html-status"></span>
                </div>
                <iframe class="html-preview" sandbox="allow-scripts"
                        title="Live preview of the HTML in the editor"></iframe>
                <div class="vz-console">
                    <div class="vz-console-bar">Console</div>
                    <!-- .html-console stays: vizlearn-html.js writes into it. -->
                    <pre class="vz-console-body html-console" aria-live="polite"
                         data-empty="console.log output from your page appears here."></pre>
                </div>
            </div>

            <div>
                <section class="vz-lab-side">
                    <h2>What this is</h2>
                    <p>Your markup rendered by the browser&rsquo;s own engine in a
                    sandboxed iframe. No tooling, no download, nothing uploaded &mdash;
                    the page works offline.</p>
                    <p>Every <code>Run</code> renders a fresh document, so nothing leaks
                    from one attempt to the next.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>What works</h2>
                    <ul>
                        <li>HTML structure, CSS, and inline <code>&lt;script&gt;</code>
                            &mdash; the real engine.</li>
                        <li><code>console.log</code> from your page appears in the
                            Console panel below the preview.</li>
                        <li>A short fragment like <code>&lt;h1&gt;Hi&lt;/h1&gt;</code>
                            is wrapped into a full document for you.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>What does not</h2>
                    <ul>
                        <li>The preview is a sandbox: it cannot read or change the rest
                            of the site, or your computer&rsquo;s files.</li>
                        <li>Keep images, styles and scripts inline &mdash; the preview
                            makes no network guarantees, and inline assets always work.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>Just the language?</h2>
                    <p>The <a href="%(p)sjs-lab/">JavaScript lab</a> runs code with no
                    markup at all, and the <a href="%(p)spython-lab/">Python compiler</a>
                    covers the other end of the stack.</p>
                </section>
            </div>
        </div>

""" % {"starter": starter, "p": "%(p)s"}


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, body(), wide=True))
    print("html lab page             : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
