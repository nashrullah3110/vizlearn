#!/usr/bin/env python3
"""Name the module's topic in the section headings every module shares.

Across the article regions, 398 modules carried a heading reading exactly
"Recap in one screen", 350 "Questions people ask", 105 "Where it goes wrong",
and a dozen more phrases appeared on 30-90 pages each (content/quality-report.md).
The same heading strings repeated across hundreds of URLs are the signature
a scaled-content classifier looks for, and they tell a reader nothing about
which page they are on.

This rewrites each of those headings to carry the module's topic:

    Questions people ask   ->  Questions people ask about Train-Test Split
    Recap in one screen    ->  Train-Test Split: recap in one screen

The original phrase is always kept whole inside the new heading, because
other steps find sections by it - build_faq_schema.py ("questions people
ask"), build_labs.py (EXP_HEADING, TAKEAWAY_HEAD) - and must keep matching
on a rebuild. The heading's id is left alone, so the in-page table of
contents and any deep link keep working; the TOC entry's text is updated to
match.

Only headings inside the article are touched, and only on modules whose
title makes a usable topic name: the interview track's titles are questions
("Why is a comprehension faster than the same loop?"), which read badly
spliced into a heading, so those pages keep theirs.

Runs late in the build, after build_lede.py has built the table of contents
and build_faq_schema.py has read the Q&A section. Idempotent: a heading that
already names its topic no longer matches a phrase below.
"""

import os
import re
import sys

from lib_catalog import ROOT, modules

# phrase (lower case, as written) -> new heading. {t} is the topic name.
TEMPLATES = {
    "recap in one screen": "{t}: recap in one screen",
    "questions people ask": "Questions people ask about {t}",
    "where it goes wrong": "Where it goes wrong with {t}",
    "things to try": "Things to try with {t}",
    "in one line": "{t} in one line",
    "run it": "Run it: {t} in code",
    "what to remember": "What to remember about {t}",
    "common mistakes": "Common mistakes with {t}",
    "summary": "{t}: summary",
    "mistakes people make": "Mistakes people make with {t}",
    "a closing note": "A closing note on {t}",
    "in summary": "{t}, in summary",
    "worth remembering": "Worth remembering about {t}",
    "the short version": "{t}: the short version",
    "experiments to try": "Experiments to try with {t}",
    "try it yourself": "Try it yourself: {t}",
    "next": "Where to go after {t}",
}

# The article runs from its marker to the first block generated after it.
ARTICLE_START = re.compile(r'<!--\s*auto-article-vizlearn\s*-->|class="vz-article\b')
ARTICLE_END = re.compile(r"<!-- VIZLEARN:(LAB|MODULE|AD-BOTTOM|FOOTER):BEGIN")

HEADING = re.compile(r'<(h[2-4])\b([^>]*)>([^<]+)</\1>')
ID_ATTR = re.compile(r'\bid="([^"]+)"')

# "What Pydantic Is For" is a question without the question mark, and makes
# "Questions people ask about What Pydantic Is For".
QUESTION_START = re.compile(
    r"^(what|why|how|when|which|where|who|is|are|does|do|can|should)\b", re.I)

TITLE_TAIL = re.compile(
    r"\s+(Visuali[sz]er|Visuali[sz]ation|Simulator|Explorer|Method|Classifier)$", re.I)


def topic_name(title):
    """A short name for the module's subject, or None if there is no clean one."""
    t = title.strip()
    if t.endswith("?") or QUESTION_START.match(t):
        return None
    t = re.sub(r"^Interactive\s+(3D\s+)?", "", t)
    t = re.split(r":| — | - | \(|, and ", t)[0].strip()
    t = TITLE_TAIL.sub("", t).strip()
    if not 2 <= len(t) <= 40:
        return None
    return t


def rename(src, topic):
    """(new source, number of headings renamed)."""
    sm = ARTICLE_START.search(src)
    if not sm:
        return src, 0
    em = ARTICLE_END.search(src, sm.end())
    start, end = sm.start(), (em.start() if em else len(src))

    renamed = {}   # heading id -> (old text, new text), for the TOC pass
    count = [0]

    def one(m):
        text = m.group(3).strip()
        tpl = TEMPLATES.get(text.lower())
        # matplotlib's "Common Mistakes" module titles its article with the
        # phrase itself; that heading is the page's name, not a section.
        if not tpl or text.lower() == topic.lower():
            return m.group(0)
        # "Questions people ask about The CAP Theorem" - an article opening
        # a title is only capitalised when the heading starts with it.
        t = topic if tpl.startswith("{t}") else re.sub(r"^The ", "the ", topic)
        new = tpl.format(t=t)
        count[0] += 1
        idm = ID_ATTR.search(m.group(2))
        if idm:
            renamed[idm.group(1)] = (text, new)
        return "<%s%s>%s</%s>" % (m.group(1), m.group(2), new, m.group(1))

    body = HEADING.sub(one, src[start:end])
    out = src[:start] + body + src[end:]

    # The table of contents lists the headings by the same text.
    for hid, (old, new) in renamed.items():
        out = out.replace('<a href="#%s">%s</a>' % (hid, old),
                          '<a href="#%s">%s</a>' % (hid, new))
    return out, count[0]


def main():
    pages = changed = headings = 0
    for m in modules(with_desc=False):
        topic = topic_name(m["title"])
        path = os.path.join(ROOT, m["path"])
        if not topic or not os.path.exists(path):
            continue
        src = open(path, encoding="utf-8").read()
        out, n = rename(src, topic)
        pages += 1
        if out != src:
            open(path, "w", encoding="utf-8").write(out)
            changed += 1
            headings += n
    print("topic headings : %d pages checked, %d rewritten, %d headings" % (pages, changed, headings))
    return 0


if __name__ == "__main__":
    sys.exit(main())
