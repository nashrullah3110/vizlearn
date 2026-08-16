# -*- coding: utf-8 -*-
"""The small text format the long-form articles are written in.

`tools/articles.py` holds its articles as Python string literals. That was
fine for sixty pages of a few hundred words; it stops being fine when every
module carries two thousand words, because every quote, backslash and
apostrophe has to survive being a Python literal first and HTML second.

So the long articles live in `content/articles/<track>/<slug>.txt` in the
format below, and this module turns them into the same
`{"intro": ..., "sections": [(heading, html)]}` shape `build_articles.py`
already renders.

    title: A Visual Guide to SQL JOINs        (optional, the card's <h2>)
    intro: One sentence under the title.      (required, the card's deck)

    ## A section heading
    A paragraph. **Bold** and `code` work; so does raw HTML, because the
    seeded articles came from HTML and there is no reason to translate
    markup that already renders.

    - a bullet
    - another

    1. a numbered step
    2. another

    ```sql
    SELECT 1;
    ```

Blank lines separate blocks. A block whose first line starts with `<` is
passed through untouched. Nothing is escaped anywhere: entities like &mdash;
are written directly, which is also how the Python-literal articles do it.
"""

import html
import os
import re

# --------------------------------------------------------------------------
# text -> html
# --------------------------------------------------------------------------

BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
CODE = re.compile(r"`([^`]+)`")


def inline(s):
    """**bold** and `code`, left alone inside a tag's attributes."""
    s = CODE.sub(lambda m: "<code>%s</code>" % m.group(1), s)
    return BOLD.sub(lambda m: "<strong>%s</strong>" % m.group(1), s)


def _list(lines, marker, tag):
    items = []
    for line in lines:
        m = marker.match(line)
        if m:
            items.append(inline(m.group(1).strip()))
        elif items:
            # a wrapped continuation line
            items[-1] += " " + inline(line.strip())
    return "<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % i for i in items), tag)


BULLET = re.compile(r"\s*[-*]\s+(.*)")
NUMBER = re.compile(r"\s*\d+[.)]\s+(.*)")
ROW = re.compile(r"\s*\|(.*)\|\s*$")


def _table(lines):
    rows = []
    for line in lines:
        m = ROW.match(line)
        if not m:
            continue
        # \| is a literal pipe inside a cell - SQL's || concatenation
        # operator would otherwise split one cell into three.
        cells = [c.strip().replace("\\|", "|")
                 for c in re.split(r"(?<!\\)\|", m.group(1))]
        if all(set(c) <= set("-: ") and c for c in cells):
            continue  # the |---|---| separator
        rows.append(cells)
    if not rows:
        return ""
    head = "".join("<th>%s</th>" % inline(c) for c in rows[0])
    body = "".join(
        "<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in r)
        for r in rows[1:]
    )
    return ("<div class=\"vz-table-wrap\"><table><thead><tr>%s</tr></thead>"
            "<tbody>%s</tbody></table></div>" % (head, body))


def _block(lines):
    """One blank-line-separated block of a section."""
    lines = [l for l in lines if l.strip()]
    if not lines:
        return ""
    first = lines[0].lstrip()

    if first.startswith("<"):
        return "\n".join(lines)
    if BULLET.match(lines[0]):
        return _list(lines, BULLET, "ul")
    if NUMBER.match(lines[0]):
        return _list(lines, NUMBER, "ol")
    if ROW.match(lines[0]):
        return _table(lines)

    text = " ".join(l.strip() for l in lines)
    return "<p>%s</p>" % inline(text)


FENCE = re.compile(r"^\s*```(\w*)\s*$")


def body_html(text):
    """The HTML for one section's body."""
    out = []
    buf = []
    fence = None
    for line in text.split("\n"):
        m = FENCE.match(line)
        if fence is not None:
            if m:
                code = html.escape("\n".join(buf))
                cls = ' class="language-%s"' % fence if fence else ""
                out.append("<pre><code%s>%s</code></pre>" % (cls, code))
                buf, fence = [], None
            else:
                buf.append(line)
            continue
        if m:
            out.append(_block(buf))
            buf, fence = [], m.group(1)
            continue
        if line.strip():
            buf.append(line)
        else:
            out.append(_block(buf))
            buf = []
    out.append(_block(buf))
    return "".join(b for b in out if b)


HEADING = re.compile(r"^##\s+(.*?)\s*$")


def parse(text):
    """A content file -> {"title", "intro", "sections"}."""
    meta = {}
    lines = text.replace("\r\n", "\n").split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r"([a-z_]+):\s*(.*)$", line)
        if not m or HEADING.match(line):
            break
        meta[m.group(1)] = m.group(2).strip()
        i += 1

    sections = []
    heading = None
    buf = []
    for line in lines[i:]:
        m = HEADING.match(line)
        if m:
            if heading is not None:
                sections.append((heading, body_html("\n".join(buf))))
            heading, buf = m.group(1), []
        else:
            buf.append(line)
    if heading is not None:
        sections.append((heading, body_html("\n".join(buf))))

    entry = {"intro": meta.get("intro", ""), "sections": sections}
    if meta.get("title"):
        entry["title"] = meta["title"]
    return entry


# --------------------------------------------------------------------------
# html -> text  (used once, to seed the content files from the live pages)
# --------------------------------------------------------------------------

VOID = {"br", "hr", "img", "input", "meta", "link", "source", "path", "circle",
        "rect", "line", "polygon", "polyline", "ellipse", "use", "stop"}
TAG = re.compile(r"<(/?)([a-zA-Z][-a-zA-Z0-9]*)\b[^>]*?(/?)>")


def elements(fragment):
    """(tag, inner_html, outer_html) for each top-level element."""
    return [(t, i, o) for t, i, o, _s, _e in _elements(fragment)]


def _elements(fragment):
    """As elements(), plus each element's (start, end) in the fragment."""
    out = []
    depth = 0
    start = name = None
    inner_from = 0
    for m in TAG.finditer(fragment):
        closing, tag, selfclose = m.group(1), m.group(2).lower(), m.group(3)
        if selfclose or tag in VOID:
            if depth == 0:
                out.append((tag, "", m.group(0), m.start(), m.end()))
            continue
        if not closing:
            if depth == 0:
                start, name, inner_from = m.start(), tag, m.end()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                out.append((name, fragment[inner_from:m.start()],
                            fragment[start:m.end()], start, m.end()))
            if depth < 0:
                depth = 0
    return out


def loose_text(fragment):
    """True if the fragment has text sitting outside any top-level element.

    Those sections are the ones where splitting into blocks would drop
    something - a bare `<strong>Lead-in.</strong> then a sentence` with no
    paragraph around it - so they are copied through as raw HTML instead.
    """
    at = 0
    for _t, _i, _o, s, e in _elements(fragment):
        if fragment[at:s].strip():
            return True
        at = e
    return bool(fragment[at:].strip())


RUN_BTN = re.compile(r'<button class="vz-run"[^>]*>.*?</button>', re.S)
SVG = re.compile(r"<svg\b.*?</svg>", re.S)
WS = re.compile(r"\s+")


def _clean(s):
    return WS.sub(" ", RUN_BTN.sub("", s)).strip()


def _li_lines(inner, marker):
    lines = []
    for tag, item, _outer in elements(inner):
        if tag != "li":
            continue
        lines.append("%s %s" % (marker, _clean(item)))
    return lines


def to_text(fragment):
    """A section body's HTML -> the text format, as losslessly as it can."""
    if loose_text(fragment):
        return _clean(fragment)
    out = []
    for tag, inner, outer in elements(fragment):
        if tag == "p":
            text = _clean(inner)
            # A paragraph opening with an inline tag (<strong>Mistake.</strong>
            # ...) would be read back as a raw-HTML block and lose its <p>,
            # so those keep the wrapper.
            out.append("<p>%s</p>" % text if text.startswith("<") else text)
        elif tag == "ul":
            out.extend(_li_lines(inner, "-"))
        elif tag == "ol":
            out.extend("%d. %s" % (i + 1, l[2:])
                       for i, l in enumerate(_li_lines(inner, "-")))
        elif tag == "pre":
            code = re.sub(r"</?code[^>]*>", "", inner)
            out.append("```")
            out.append(html.unescape(code).strip("\n"))
            out.append("```")
        elif tag == "div":
            nested = to_text(inner)
            if nested.strip():
                out.append(nested)
            continue
        else:
            # tables and anything else: keep the markup as it stands
            out.append(WS.sub(" ", RUN_BTN.sub("", outer)).strip())
        out.append("")
    return "\n".join(out).strip()


def heading_text(h):
    return WS.sub(" ", html.unescape(re.sub(r"<[^>]+>", "", SVG.sub("", h)))).strip()


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------

def content_dir(root):
    return os.path.join(root, "content", "articles")


def load(root):
    """{page path: entry} for every content file under content/articles/."""
    base = content_dir(root)
    out = {}
    for dirpath, _dirs, names in os.walk(base):
        for name in sorted(names):
            if not name.endswith(".txt"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, base)[: -len(".txt")] + ".html"
            with open(path, encoding="utf-8") as fh:
                entry = parse(fh.read())
            if entry["sections"]:
                out[rel.replace(os.sep, "/")] = entry
    return out
