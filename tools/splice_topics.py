#!/usr/bin/env python3
"""Insert sections into the articles that live inside tools/<track>_topics.py.

tools/splice.py edits `content/articles/<track>/<slug>.txt`, and for the older
tracks that file is the source. For the twelve generated tracks it is not: the
prose is the `article=` argument of a `topic(...)` call in
tools/<track>_topics.py, and build_<track>_topics.py writes it out over the
.txt on every build. Editing the .txt there looks like it works, survives right
up until the next `npm run build`, and is then silently gone.

That is not a hypothetical. All 89 of the thin pages in maths, database,
computer_vision, machine_learning and deep_learning are generated ones - the
correspondence is exact, in all five tracks, with no exceptions either way -
because these were the tranche seeded from a template and never given the
long-form pass the hand-written articles got. So expanding them means editing
the generator, and that is what this does.

Same batch format as splice.py, and the section logic is imported from it so
the two cannot drift:

    ==== maths/taylor_series @before Rebuild a function
    ## e to the x, worked by hand
    ...

The article is a plain triple-quoted literal - no track has one containing a
backslash or an embedded triple quote, which is checked before writing - so
the old text is replaced verbatim in the source and the file stays readable
as Python.

    python3 tools/splice_topics.py batch.txt
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import splice
from lib_catalog import ROOT

# track directory -> the module holding its topic() calls
MODULES = {
    "maths": "math_topics",
    "database": "db_topics",
    "computer_vision": "cv_topics",
    "machine_learning": "ml_topics",
    "deep_learning": "dl_topics",
    "python": "python_topics",
    "pydantic": "pydantic_topics",
    "fastapi": "fastapi_topics",
    "numpy": "numpy_topics",
    "pandas": "pandas_topics",
    "matplotlib": "matplotlib_topics",
    "sklearn": "sklearn_topics",
}

_loaded = {}


def articles(track):
    """{slug: article} for one generated track."""
    if track not in _loaded:
        mod = __import__(MODULES[track])
        _loaded[track] = {t["slug"]: t["article"] for t in mod.TOPICS}
    return _loaded[track]


def rebuild(article, where, anchor, new):
    """The article text with `new` sections placed, or (None, error)."""
    lines = article.split("\n")
    head, body = lines, ""
    for i, line in enumerate(lines):
        if splice.SECTION.match(line):
            head, body = lines[:i], "\n".join(lines[i:])
            break
    head = "\n".join(head).strip("\n")
    sections = splice.split_sections(body)

    added = []
    for heading, text in new:
        i = splice.index_of(sections, heading)
        if i is not None and sections[i][0].lower() == heading.lower():
            sections[i] = (heading, text)      # rerun replaces, never duplicates
        else:
            added.append((heading, text))

    if added:
        if where == "@start":
            at = 0
        elif where == "@experiments":
            at = splice.experiments_index(sections)
            if at is None:
                at = max(len(sections) - 1, 0)
        elif where in ("@before", "@after"):
            at = splice.index_of(sections, anchor)
            if at is None:
                return None, "no section matching %r" % anchor
            if where == "@after":
                at += 1
        else:
            at = len(sections)
        sections[at:at] = added

    parts = [head]
    for heading, text in sections:
        parts.append("\n## %s\n\n%s" % (heading, text.strip("\n")))
    return "\n".join(parts).rstrip() + "\n", None


def main():
    src = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 \
        else sys.stdin.read()

    blocks, cur = [], None
    for line in src.split("\n"):
        m = splice.HEAD.match(line)
        if m:
            cur = [m.group(1), m.group(2) or "@end", m.group(3), []]
            blocks.append(cur)
        elif cur is not None:
            cur[3].append(line)

    # Group by module so each source file is read and written once.
    edits, errors = {}, []
    for rel, where, anchor, lines in blocks:
        rel = rel[:-4] if rel.endswith(".txt") else rel
        track, _, slug = rel.partition("/")
        if track not in MODULES:
            errors.append("%s: not a generated track (use tools/splice.py)" % rel)
            continue
        table = articles(track)
        if slug not in table:
            errors.append("%s: no such topic in %s" % (rel, MODULES[track]))
            continue
        new = splice.split_sections("\n".join(lines))
        if not new:
            errors.append("%s: block has no ## heading" % rel)
            continue
        old = edits.get((track, slug), (table[slug], table[slug]))[0]
        fresh, err = rebuild(old, where, anchor, new)
        if err:
            errors.append("%s: %s" % (rel, err))
            continue
        edits[(track, slug)] = (fresh, table[slug])

    touched = set()
    for (track, slug), (fresh, original) in edits.items():
        path = os.path.join(ROOT, "tools", MODULES[track] + ".py")
        text = open(path, encoding="utf-8").read()
        # The literal is written as-is inside """...""", so anything that would
        # need escaping has to be refused rather than silently mangled.
        for bad, why in (("\\", "a backslash"), ('"""', "a triple quote")):
            if bad in fresh:
                errors.append("%s/%s: new text contains %s" % (track, slug, why))
                break
        else:
            n = text.count(original)
            if n != 1:
                errors.append("%s/%s: article text found %d times in %s"
                              % (track, slug, n, os.path.basename(path)))
                continue
            open(path, "w", encoding="utf-8").write(text.replace(original, fresh, 1))
            _loaded[track][slug] = fresh
            touched.add((track, slug))

    for e in errors:
        print("  !! %s" % e)
    files = {t for t, _s in touched}
    print("spliced: %d topic(s) in %d generator(s), %d block(s)"
          % (len(touched), len(files), len(blocks)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
