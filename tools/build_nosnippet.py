#!/usr/bin/env python3
"""Keep the visualisation's controls and readouts out of search snippets.

Between a module's opening section (build_lede.py) and its article sits the
interactive part: sliders, buttons, key hints, live readouts. Read as text it
is a run of fragments - "Neighbours (k) 3", "Cells probed 1", "← → pick" - and
Google is free to quote any of it as the page's snippet. `data-nosnippet`
tells it not to.

What it does not do: hide anything, or change how the page is indexed or
ranked. It is a snippet hint and nothing more. The page reads exactly as
before; the attribute changes no layout, because nothing is wrapped or moved -
it is added to the opening tags of elements that are already there.

Which elements: every block element that lies wholly between the end of the
opening section and the start of the article, taking the outermost one each
time. When an element holds both part of that stretch and the article (a
grid whose second column is the article, say), it is left alone and its
children are considered instead. The page templates differ (29 shapes across
the modules) but every one has those two landmarks, so this needs no
per-template rules.

Runs after build_lede.py and build_headings.py. Idempotent: it clears its
own marks and recomputes them on every run.
"""

import os
import re
import sys
from html.parser import HTMLParser

from lib_catalog import ROOT, modules

LEDE_END = "<!-- VIZLEARN:LEDE:END -->"
BYLINE_END = "<!-- VIZLEARN:BYLINE:END -->"
ARTICLE_START = re.compile(r'<!--\s*auto-article-vizlearn\s*-->|<[a-z]+\b[^>]*class="vz-article\b')

# The article card's title bar ("Neural Network Visualizer: A Practical
# Guide") sits just before the article inside the same card. It is the
# article's heading, not a control.
KEEP = re.compile(r'class="[^"]*\bcard-header\b')

BLOCKS = {"div", "section", "aside", "nav", "form", "header", "details", "figure", "ul", "ol", "table"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr"}


class Spans(HTMLParser):
    """(tag, start, end, parent index) for every element, by byte offset."""

    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.lines = [0]
        for m in re.finditer("\n", src):
            self.lines.append(m.end())
        self.out = []
        self.stack = []

    def _off(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        start = self._off()
        parent = self.stack[-1] if self.stack else -1
        self.out.append([tag, start, None, parent])
        if tag not in VOID:
            self.stack.append(len(self.out) - 1)

    def handle_startendtag(self, tag, attrs):
        start = self._off()
        parent = self.stack[-1] if self.stack else -1
        self.out.append([tag, start, start, parent])

    def handle_endtag(self, tag):
        end = self._off()
        # Close back to the matching open tag; stray end tags are ignored.
        for k in range(len(self.stack) - 1, -1, -1):
            if self.out[self.stack[k]][0] == tag:
                for idx in self.stack[k:]:
                    self.out[idx][2] = end
                del self.stack[k:]
                return


def targets(src):
    """Offsets of the opening tags to mark, or [] if the page has no landmarks."""
    am = ARTICLE_START.search(src)
    if not am:
        return []
    art = am.start()
    lo = src.find(LEDE_END)
    lo = lo + len(LEDE_END) if lo != -1 else src.find(BYLINE_END)
    if lo == -1 or lo >= art:
        return []

    p = Spans(src)
    p.feed(src)
    p.close()
    els = p.out
    for e in els:   # anything left open runs to the end of the document
        if e[2] is None:
            e[2] = len(src)

    def straddles(i):
        """True if element i opens before the stretch or contains the article."""
        if i == -1:
            return True
        _, s, e, _ = els[i]
        return s < lo or (s <= art < e)

    out = []
    for i, (tag, s, e, parent) in enumerate(els):
        if tag not in BLOCKS or s < lo or e > art:
            continue
        if KEEP.search(src, s, src.index(">", s)):
            continue
        if straddles(parent):
            out.append(s)
    return out


def mark(src):
    # This step owns the attribute on module pages: clear the previous run's
    # marks first, so an element that stops qualifying loses its mark too.
    src = src.replace(" data-nosnippet", "")
    offs = targets(src)
    for s in sorted(offs, reverse=True):
        end = src.index(">", s)
        tag = src[s:end]
        if "data-nosnippet" in tag:
            continue
        # Before a self-closing slash, if there is one.
        at = end - 1 if src[end - 1] == "/" else end
        src = src[:at] + " data-nosnippet" + src[at:]
    return src, len(offs)


def main():
    pages = changed = marked = 0
    for m in modules(with_desc=False):
        path = os.path.join(ROOT, m["path"])
        if not os.path.exists(path):
            continue
        src = open(path, encoding="utf-8").read()
        out, n = mark(src)
        pages += 1
        marked += n
        if out != src:
            open(path, "w", encoding="utf-8").write(out)
            changed += 1
    print("nosnippet : %d pages, %d written, %d interactive blocks marked"
          % (pages, changed, marked))
    return 0


if __name__ == "__main__":
    sys.exit(main())
