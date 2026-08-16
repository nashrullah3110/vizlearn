#!/usr/bin/env python3
"""Insert new sections into content/articles/ files, in batches.

The long-form rewrite adds sections to articles that already exist, and the
existing text has to stay where it is - the "experiments" section names real
controls on the page, and tools/build_labs.py reads it to build the Run
buttons and the preset it drives them with.

So new prose is written as a batch: a file (or stdin) of

    ==== machine_learning/k_means @before Guided experiments
    ## An everyday version of the same idea
    ...

    ==== machine_learning/k_means @end
    ## Questions people ask
    ...

`@before <heading>` / `@after <heading>` place the block relative to an
existing section, matched on a case-insensitive prefix; `@end` appends;
`@start` puts it first. Reruns replace a section that already exists with the
same heading rather than adding a second copy, so a batch is idempotent.

    python3 tools/splice.py batch.txt
    python3 tools/splice.py < batch.txt
"""

import os
import re
import sys

import prose
from lib_catalog import ROOT

HEAD = re.compile(r"^====\s+(\S+)\s*(@\w+)?\s*(.*)$")
SECTION = re.compile(r"^##\s+(.*?)\s*$")


def split_sections(text):
    """[(heading, body_text)] for a chunk written in the content format."""
    out = []
    heading, buf = None, []
    for line in text.split("\n"):
        m = SECTION.match(line)
        if m:
            if heading is not None:
                out.append((heading, "\n".join(buf).strip("\n")))
            heading, buf = m.group(1), []
        elif heading is not None:
            buf.append(line)
    if heading is not None:
        out.append((heading, "\n".join(buf).strip("\n")))
    return out


def read_file(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    head, body = [], text
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if SECTION.match(line):
            head, body = lines[:i], "\n".join(lines[i:])
            break
    else:
        head, body = lines, ""
    return "\n".join(head).strip("\n"), split_sections(body)


def write_file(path, head, sections):
    parts = [head]
    for heading, body in sections:
        parts.append("\n## %s\n\n%s" % (heading, body.strip("\n")))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts).rstrip() + "\n")


def index_of(sections, needle):
    needle = needle.strip().lower()
    for i, (heading, _b) in enumerate(sections):
        if heading.lower().startswith(needle):
            return i
    return None


# The experiments section is titled a dozen different ways across the site
# ("Try it yourself", "Exploration guide", "Things to try"), and new material
# almost always wants to go in front of it. `@experiments` finds it without
# the caller having to look the exact wording up first.
EXPERIMENTS = re.compile(
    r"(try (it|this|these)|experiment|exploration|explore|guided tour|"
    r"things to try|guided|in the live panel|interactive lab|how to use)", re.I)


def experiments_index(sections):
    for i, (heading, _b) in enumerate(sections):
        if EXPERIMENTS.search(heading):
            return i
    return None


def apply(rel, where, anchor, new):
    path = os.path.join(prose.content_dir(ROOT), rel + ".txt")
    if not os.path.exists(path):
        return "no such content file: %s" % rel
    head, sections = read_file(path)

    # Replacing rather than duplicating keeps a rerun idempotent.
    added = []
    for heading, body in new:
        i = index_of(sections, heading)
        if i is not None and sections[i][0].lower() == heading.lower():
            sections[i] = (heading, body)
        else:
            added.append((heading, body))
    if not added:
        write_file(path, head, sections)
        return None

    if where == "@start":
        at = 0
    elif where == "@experiments":
        at = experiments_index(sections)
        if at is None:
            at = max(len(sections) - 1, 0)   # in front of the closing takeaway
    elif where in ("@before", "@after"):
        at = index_of(sections, anchor)
        if at is None:
            return "%s: no section matching %r" % (rel, anchor)
        if where == "@after":
            at += 1
    else:
        at = len(sections)

    sections[at:at] = added
    write_file(path, head, sections)
    return None


def main():
    src = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 \
        else sys.stdin.read()

    blocks = []
    cur = None
    for line in src.split("\n"):
        m = HEAD.match(line)
        if m:
            cur = [m.group(1), m.group(2) or "@end", m.group(3), []]
            blocks.append(cur)
        elif cur is not None:
            cur[3].append(line)

    errors = []
    touched = set()
    for rel, where, anchor, lines in blocks:
        rel = rel[:-4] if rel.endswith(".txt") else rel
        sections = split_sections("\n".join(lines))
        if not sections:
            errors.append("%s: block has no ## heading" % rel)
            continue
        err = apply(rel, where, anchor, sections)
        if err:
            errors.append(err)
        else:
            touched.add(rel)

    for e in errors:
        print("  !! %s" % e)
    print("spliced: %d file(s), %d block(s)" % (len(touched), len(blocks)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
