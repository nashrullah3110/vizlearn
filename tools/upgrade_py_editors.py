#!/usr/bin/env python3
"""Give the python/ track the same editor as /python-lab/.

The lab got a title bar, a line-number gutter, syntax highlighting and a
terminal-styled console. The twelve module pages kept a bare monospace
textarea, so the same language looked like two different products depending on
which page you landed on.

This rewrites each `.vz-py` block to the markup assets/vizlearn-code.js expects.
Nothing about the runner changes: the textarea keeps `.py-editor` and the
output keeps `.py-output`, which is what assets/vizlearn-python.js binds to.

The blocks are hand-written in the page rather than generated, so this is a
one-time migration rather than a build step. It is idempotent - a block that
already has the wrapper is skipped.

    python3 tools/upgrade_py_editors.py
"""

import glob
import os
import re
import sys

from lib_catalog import ROOT

# Both are distinctive enough to match without a parser, and both appear once
# per .vz-py block.
EDITOR = re.compile(
    r'(?P<indent>[ \t]*)<textarea class="py-editor"([^>]*)></textarea>')
OUTPUT = re.compile(
    r'(?P<indent>[ \t]*)<pre class="py-output" aria-live="polite"></pre>')

EDITOR_NEW = '''%(i)s<div class="vz-code-bar">
%(i)s    <span class="vz-code-dot"></span>
%(i)s    <span class="vz-code-lang">Python 3</span>
%(i)s</div>
%(i)s<!-- .py-editor stays: assets/vizlearn-python.js reads .value off it. -->
%(i)s<div class="vz-code" data-vz-code="python">
%(i)s    <div class="vz-code-gutter" aria-hidden="true"></div>
%(i)s    <div class="vz-code-scroll">
%(i)s        <pre class="vz-code-hl" aria-hidden="true"></pre>
%(i)s        <textarea class="vz-code-input py-editor"%(attrs)s></textarea>
%(i)s    </div>
%(i)s</div>'''

OUTPUT_NEW = '''%(i)s<div class="vz-console">
%(i)s    <div class="vz-console-bar">Output</div>
%(i)s    <pre class="vz-console-body py-output" aria-live="polite"
%(i)s         data-empty="Press Run to execute this code."></pre>
%(i)s</div>'''


def upgrade(src):
    if "vz-code-input" in src:
        return src, 0            # already migrated

    n = 0

    def editor(m):
        nonlocal n
        n += 1
        return EDITOR_NEW % {"i": m.group("indent"), "attrs": m.group(2)}

    def output(m):
        return OUTPUT_NEW % {"i": m.group("indent")}

    src = EDITOR.sub(editor, src)
    src = OUTPUT.sub(output, src)
    return src, n


def main():
    pages = sorted(glob.glob(os.path.join(ROOT, "python", "*.html")))
    files = blocks = 0
    for path in pages:
        src = open(path, encoding="utf-8").read()
        if 'class="vz-py"' not in src:
            continue
        new, n = upgrade(src)
        if n:
            open(path, "w", encoding="utf-8").write(new)
            files += 1
            blocks += n

    print("python module pages upgraded : %d" % files)
    print("editor blocks rewritten      : %d" % blocks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
