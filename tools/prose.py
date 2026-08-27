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

# Tags that can open a paragraph without making it stop being one.
INLINE_LEAD = re.compile(
    r"<(strong|em|b|i|span|code|a|sup|sub|small|mark|abbr|kbd|u|s)\b",
    re.I)

BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
CODE = re.compile(r"`([^`]+)`")


def code_span(text):
    """The inside of a `backtick span`, made safe to drop into the document.

    Angle brackets have to be escaped or the browser parses them: an article
    that mentioned `<h1>` was emitting a real, empty <h1> element into the
    page, and `<s>` in the tokenisation article was striking through the rest
    of the sentence. `<lambda>` and `<UNK>` were worse - an unknown element
    swallows its own name, so the text simply vanished.

    Ampersands are deliberately left alone. Articles write entities inside
    code spans on purpose - `&lambda;`, `&minus;`, `&lt;map object&gt;` - and
    escaping those would print the entity source instead of the character.
    """
    return text.replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    """**bold** and `code`, left alone inside a tag's attributes."""
    s = CODE.sub(lambda m: "<code>%s</code>" % code_span(m.group(1)), s)
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

    # A block that opens with a *block-level* tag is markup the author wrote
    # and is passed through untouched. A block that merely opens with an
    # inline tag is still a paragraph: 3690 of them across the articles begin
    # with a bold lead-in, and treating those as raw HTML meant they got no
    # <p> wrapper - so they ran into the sentence before them - and never
    # reached inline(), so their backticks printed literally to the reader.
    if first.startswith("<") and not INLINE_LEAD.match(first):
        return "\n".join(lines)
    if BULLET.match(lines[0]):
        return _list(lines, BULLET, "ul")
    if NUMBER.match(lines[0]):
        return _list(lines, NUMBER, "ol")
    if ROW.match(lines[0]):
        return _table(lines)

    text = " ".join(l.strip() for l in lines)
    return "<p>%s</p>" % inline(text)


FENCE = re.compile(r"^\s*```([\w-]*)\s*$")


# Tracks whose articles may contain runnable code.
#
# A ```python-run fence in one of these becomes a real editor rather than a
# static <pre>, which is the whole point: a reader meets the program at the
# moment the prose introduces it, not in a separate slab above the article
# with the prose repeating a non-runnable copy of it further down.
#
# Filled by the track generators (build_pydantic_topics.py and its FastAPI
# sibling) before build_articles.py renders anything.
RUNNABLE = {}


def runnable_editor(code, spec, n):
    """One `.vz-py` block, wired to assets/vizlearn-python.js.

    The source is emitted raw: <script> content is raw text, so entities are
    not decoded inside it and escaping would corrupt the program. The only
    sequence that would need escaping is a literal </script>, checked for
    here because a content file is easier to edit than a generator.
    """
    if "</script" in code.lower():
        raise SystemExit("a runnable block contains </script and would break out")
    attrs = ' data-vz-py data-vz-packages="%s"' % spec.get("packages", "")
    if spec.get("wheels"):
        attrs += ' data-vz-wheels="%s"' % spec["wheels"]
    if spec.get("label"):
        attrs += ' data-vz-label="%s"' % spec["label"]
    pre = ""
    if spec.get("prelude"):
        pre = ('<script type="text/plain" class="py-prelude">%s</script>'
               % spec["prelude"].strip())
    return (
        '<div class="vz-py vz-py-inline"%(attrs)s>'
        '%(pre)s'
        '<script type="text/plain" class="py-src">%(code)s</script>'
        '<div class="vz-code-bar"><span class="vz-code-dot"></span>'
        '<span>%(file)s</span><span class="vz-code-lang">%(lang)s</span></div>'
        '<div class="vz-code" data-vz-code="python">'
        '<div class="vz-code-gutter" aria-hidden="true"></div>'
        '<div class="vz-code-scroll"><pre class="vz-code-hl" aria-hidden="true"></pre>'
        '<textarea class="vz-code-input py-editor" aria-label="Runnable example"'
        ' spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>'
        '</div></div>'
        '<div class="py-controls">'
        '<button type="button" class="py-run-btn">Run</button>'
        '<button type="button" class="py-reset-btn">Reset</button>'
        '<span class="py-status"></span></div>'
        '<div class="vz-console"><div class="vz-console-bar">Output</div>'
        '<pre class="vz-console-body py-output" aria-live="polite"'
        ' data-empty="Press Run to execute this code."></pre></div>'
        '</div>'
    ) % {"attrs": attrs, "pre": pre, "code": code.rstrip(),
         "file": spec.get("filename", "example.py") % n if "%" in
                 spec.get("filename", "example.py") else spec.get("filename", "example.py"),
         "lang": spec.get("label", "Python")}


def body_html(text, spec=None, counter=None):
    """The HTML for one section's body."""
    out = []
    buf = []
    fence = None
    for line in text.split("\n"):
        m = FENCE.match(line)
        if fence is not None:
            if m:
                raw = "\n".join(buf)
                if fence.endswith("-run") and spec:
                    counter[0] += 1
                    out.append(runnable_editor(raw, spec, counter[0]))
                else:
                    cls = ' class="language-%s"' % fence if fence else ""
                    out.append("<pre><code%s>%s</code></pre>"
                               % (cls, html.escape(raw)))
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


def parse(text, spec=None):
    """A content file -> {"title", "intro", "sections"}.

    `spec` describes how a ```lang-run fence should be rendered for this
    track; None means every fence stays a static <pre>.
    """
    counter = [0]
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
                sections.append((heading, body_html("\n".join(buf), spec, counter)))
            # Headings take the same inline pass as body text, or a
            # heading like `The `or` lookalike` prints its backticks.
            # Anchor ids are unaffected: slug() strips tags first.
            heading, buf = inline(m.group(1)), []
        else:
            buf.append(line)
    if heading is not None:
        sections.append((heading, body_html("\n".join(buf), spec, counter)))

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


def _load_specs():
    """Populate RUNNABLE from tools/runnable_specs.py, if it is importable."""
    if RUNNABLE:
        return
    try:
        import runnable_specs
    except ImportError:
        return
    RUNNABLE.update(runnable_specs.resolve())


def load(root):
    """{page path: entry} for every content file under content/articles/."""
    _load_specs()
    base = content_dir(root)
    out = {}
    for dirpath, _dirs, names in os.walk(base):
        for name in sorted(names):
            if not name.endswith(".txt"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, base)[: -len(".txt")] + ".html"
            track = os.path.relpath(dirpath, base).split(os.sep)[0]
            with open(path, encoding="utf-8") as fh:
                entry = parse(fh.read(), RUNNABLE.get(track))
            if entry["sections"]:
                out[rel.replace(os.sep, "/")] = entry
    return out
