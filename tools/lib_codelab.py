# -*- coding: utf-8 -*-
"""The embedded Python editor, shared by the dsa/ and interview/ builders.

Both tracks put the same thing on the page - the editor from /python-lab/,
with an implementation in it and a walkthrough beside it - so the markup lives
here rather than in two generators that would drift apart the first time one
of them was fixed.

The contract is assets/vizlearn-python.js's: a `.vz-py` block containing a
`.py-src` script, a `.py-editor` textarea, `.py-run-btn`, `.py-reset-btn`,
`.py-status` and `.py-output`. assets/vizlearn-code.js layers the highlighter
over the same textarea.
"""

import html

ICON = ('<svg class="vz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="m8 9-4 3 4 3"/><path d="m16 9 4 3-4 3"/>'
        '<path d="M13 6l-2 12"/></svg>')


def editor(code, filename):
    """The `.vz-py` block itself.

    `code` is emitted raw on purpose: it lands inside
    <script type="text/plain">, whose content is character data, so an escaped
    `&lt;` would reach the interpreter as those four characters and fail to
    compile.
    """
    code = code.strip("\n")
    if "</script" in code.lower():
        raise ValueError("code contains a closing script tag")

    return (
        '<div class="vz-py" data-vz-py>'
        '<script type="text/plain" class="py-src">%(code)s</script>'
        '<div class="vz-code-bar"><span class="vz-code-dot"></span>'
        '<span>%(file)s</span><span class="vz-code-lang">Python 3</span></div>'
        '<!-- .py-editor stays: assets/vizlearn-python.js reads .value off it. -->'
        '<div class="vz-code" data-vz-code="python">'
        '<div class="vz-code-gutter" aria-hidden="true"></div>'
        '<div class="vz-code-scroll"><pre class="vz-code-hl" aria-hidden="true"></pre>'
        '<textarea class="vz-code-input py-editor" aria-label="Python code editor" '
        'spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>'
        '</div></div>'
        '<div class="py-controls">'
        '<button type="button" class="py-run-btn">Run</button>'
        '<button type="button" class="py-reset-btn">Reset</button>'
        '<span class="py-status"></span></div>'
        '<div class="vz-console"><div class="vz-console-bar">Output</div>'
        '<pre class="vz-console-body py-output" aria-live="polite" '
        'data-empty="Press Run to execute this code."></pre></div>'
        '</div>'
    ) % {"code": code, "file": html.escape(filename)}


def walk_list(walk):
    """The numbered walkthrough. Labels are escaped; notes are authored HTML."""
    out = []
    for label, body in walk:
        out.append('<li class="vz-cl-step"><code class="vz-cl-line">%s</code>'
                   '<span class="vz-cl-note">%s</span></li>'
                   % (html.escape(label), body))
    return "".join(out)


def aside(walk, tries, prefix, heading="How the code works"):
    """The panel beside the editor: walkthrough, edits to try, and a footnote."""
    blocks = ['<section class="vz-cl-side"><h3>%s</h3>'
              '<ol class="vz-cl-walk">%s</ol></section>'
              % (html.escape(heading), walk_list(walk))]

    if tries:
        blocks.append('<section class="vz-cl-side"><h3>Change one thing</h3>'
                      '<ul class="vz-cl-try">%s</ul></section>'
                      % "".join("<li>%s</li>" % t for t in tries))

    blocks.append(
        '<section class="vz-cl-side"><h3>Where this runs</h3>'
        '<p class="vz-cl-note">Real CPython, compiled to WebAssembly and running on '
        'your own machine &mdash; nothing is uploaded. The first run takes a few '
        'seconds while the interpreter downloads; after that it is immediate. Need '
        'more room, or want to paste your own attempt? Use the '
        '<a href="%spython-lab/">Python compiler</a>.</p></section>' % prefix)

    return '<div class="vz-cl-aside">%s</div>' % "".join(blocks)


def section(entry, prefix, intro, heading="Run it in Python"):
    """A complete `Run it in Python` section: intro, editor, walkthrough."""
    return (
        '<section class="vz-codelab" aria-labelledby="vz-codelab-h">'
        '<div class="vz-section-head">%(icon)s<h2 id="vz-codelab-h">%(heading)s</h2>'
        '<span class="vz-rule"></span></div>'
        '<p class="vz-cl-intro">%(intro)s</p>'
        '<div class="vz-cl-grid">%(editor)s%(aside)s</div>'
        '</section>'
    ) % {
        "icon": ICON,
        "heading": html.escape(heading),
        "intro": intro,
        "editor": editor(entry["code"], entry["file"]),
        "aside": aside(entry["walk"], entry.get("try"), prefix),
    }
