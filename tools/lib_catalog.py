"""Shared helpers for reading the VizLearn module catalog out of index.html.

index.html holds the single source of truth (`courseData`). Every build script
in tools/ reads it through here so the catalog is never transcribed by hand.
"""

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")

SITE = "https://vizlearn.in"

# directory on disk -> (display label, icon key)
DIR_META = {
    "machine_learning": ("Machine Learning", "brain"),
    "deep_learning": ("Deep Learning", "network"),
    "dsa": ("Algorithms", "layers"),
    "natural_language_processing": ("NLP", "comments"),
    "computer_vision": ("Computer Vision", "eye"),
    "database": ("Database", "database"),
    "gen_ai": ("Gen AI", "robot"),
    "maths": ("Maths", "sigma"),
    "python": ("Python", "code"),
    "interview": ("Interview", "interview"),
}


def _extract_object(src, start_idx):
    """Return the balanced {...} literal beginning at/after start_idx."""
    j = src.index("{", start_idx)
    depth, k, in_str, esc = 0, j, False, False
    while k < len(src):
        c = src[k]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return j, k + 1
        k += 1
    raise ValueError("unbalanced object literal")


def read_course_data(path=INDEX):
    """Parse `courseData = {...}` out of index.html. Returns (dict, start, end).

    index.html also contains `let courseData = {};`, so take the largest
    balanced literal rather than the first one.
    """
    src = open(path, encoding="utf-8").read()
    best = None
    for m in re.finditer(r"courseData\s*=\s*\n?\s*\{", src):
        start, end = _extract_object(src, m.start())
        if best is None or (end - start) > (best[1] - best[0]):
            best = (start, end)
    if best is None:
        raise SystemExit("courseData not found in index.html")
    start, end = best
    return json.loads(src[start:end]), start, end


DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)

try:
    from descriptions import DESCRIPTIONS as _OVERRIDES
except ImportError:  # running from another cwd
    _OVERRIDES = {}


def page_description(rel):
    """The description for a module page.

    Hand-written entries in descriptions.py win over whatever the page
    currently declares, so the search catalog, the social cards and the page's
    own <meta> can never disagree. build_seo.py writes the same value back into
    the HTML.
    """
    if rel in _OVERRIDES:
        return _OVERRIDES[rel]
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return ""
    m = DESC_RE.search(open(p, encoding="utf-8").read())
    if not m:
        return ""
    import html as _html
    return _html.unescape(m.group(1)).strip()


def modules(path=INDEX, with_desc=True):
    """Flat list of every module with its topic, directory and display metadata.

    Order within a topic follows courseData, which is also the order used for
    prev/next -- reorder courseData to change the learning sequence.
    """
    data, _, _ = read_course_data(path)
    out = []
    for topic_key, topic in data.items():
        for i, course in enumerate(topic["courses"]):
            rel = course["path"].lstrip("./")
            directory = rel.split("/")[0]
            label, icon = DIR_META.get(directory, (topic["title"], "book"))
            out.append(
                {
                    "title": course["title"],
                    "path": rel,
                    "dir": directory,
                    "topic": topic_key,
                    "topic_title": topic["title"],
                    "category": label,
                    "icon": icon,
                    "index": i,
                    "svg": course.get("svg", ""),
                    "desc": page_description(rel) if with_desc else "",
                }
            )
    return out


def by_topic(path=INDEX):
    """{topic_key: [modules in catalog order]}"""
    groups = {}
    for m in modules(path):
        groups.setdefault(m["topic"], []).append(m)
    return groups


def all_pages(path=INDEX):
    """Every routable page: index.html plus each module."""
    return ["index.html"] + [m["path"] for m in modules(path)]
