#!/usr/bin/env python3
"""Paint every runnable editor's source into the HTML it ships in.

The `.vz-code-hl` <pre> is the layer a reader actually sees - the textarea
over it is drawn in transparent text - and it was authored empty, filled only
when assets/vizlearn-code.js ran. That put every runnable example outside the
document: a crawler that does not execute JavaScript saw an empty <pre> and a
<script type="text/plain">, and neither of those is content. The examples are
the most distinctive writing on the site, which makes them the last thing that
should be missing from the file we serve.

Most editors are painted by whichever generator emits them. This is the
backstop for the rest, and the reason it exists as its own pass:

  * the python/ track's editors were written once by tools/upgrade_py_editors.py
    and live in committed HTML, so no generator rebuilds them and no generator
    can fix them;
  * an emitter added later starts correct without anyone remembering this.

A <pre> is filled from the `.py-src` script or the `.sql-editor` textarea in
its own block. Blocks with no source - the lab and notebook playgrounds, which
open with an empty editor on purpose - are left alone.

Idempotent: an already-painted <pre> is skipped, so re-running changes nothing.
"""

import glob
import html
import os
import re
import sys

from lib_catalog import ROOT

SKIP = ("node_modules/", ".venv/", "tools/", "_verify/")

EMPTY = re.compile(r'(<pre class="vz-code-hl" aria-hidden="true">)(</pre>)')
# The two things a block can carry its source in. Both are matched lazily and
# anchored on the class, so the nearest one before a <pre> is its own.
SOURCE = re.compile(
    r'<script type="text/plain" class="py-src">(.*?)</script>'
    r'|<textarea class="vz-code-input sql-editor"[^>]*>(.*?)</textarea>',
    re.S)


def source_for(src, at):
    """The code belonging to the empty <pre> that starts at `at`, or None.

    The source sits inside the same block, before the <pre>. Taking the
    nearest preceding match is therefore right - but only if no other editor
    intervenes, which is what disqualifies a playground whose own block has
    no source and would otherwise borrow the previous block's.
    """
    best = None
    for m in SOURCE.finditer(src, 0, at):
        best = m
    if best is None:
        return None
    between = src[best.end():at]
    if '<pre class="vz-code-hl"' in between or "</div></div>" in between.replace(" ", ""):
        return None
    code = best.group(1) if best.group(1) is not None else best.group(2)
    # A py-src is raw text; a textarea's content is already escaped. Normalise
    # to plain source, then escape once for the <pre>.
    if best.group(2) is not None:
        code = html.unescape(code)
    return code.strip("\n").rstrip()


def paint(path):
    src = open(path, encoding="utf-8").read()
    if '<pre class="vz-code-hl" aria-hidden="true"></pre>' not in src:
        return 0
    out, last, filled = [], 0, 0
    for m in EMPTY.finditer(src):
        code = source_for(src, m.start())
        if not code:
            continue
        out.append(src[last:m.start()])
        out.append("%s%s\n</pre>" % (m.group(1),
                                     html.escape(code, quote=False)))
        last = m.end()
        filled += 1
    if not filled:
        return 0
    out.append(src[last:])
    open(path, "w", encoding="utf-8").write("".join(out))
    return filled


def main():
    total = pages = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"),
                                 recursive=True)):
        rel = os.path.relpath(path, ROOT)
        if any(rel.startswith(s) for s in SKIP):
            continue
        n = paint(path)
        if n:
            total += n
            pages += 1
    print("code painted : %d editors on %d pages" % (total, pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
