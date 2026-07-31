#!/usr/bin/env python3
"""Reorder courseData in index.html to the teaching order in sequence.py.

courseData order drives prev/next, the related rail and the hub listing, so
this is the single place the learning sequence is defined. Refuses to write
anything if a track's sequence does not exactly match the modules on disk.
"""

import json
import sys

from lib_catalog import INDEX, read_course_data
from sequence import SEQUENCE


def main():
    data, start, end = read_course_data()
    src = open(INDEX, encoding="utf-8").read()

    problems = []
    for topic, courses in data.items():
        have = [c["path"].lstrip("./") for c in courses["courses"]]
        want = SEQUENCE.get(topic)
        if want is None:
            problems.append("no sequence defined for topic %r" % topic)
            continue
        missing = [p for p in have if p not in want]
        unknown = [p for p in want if p not in have]
        if missing:
            problems.append("%s: not in sequence.py -> %s" % (topic, ", ".join(missing)))
        if unknown:
            problems.append("%s: in sequence.py but not on disk -> %s" % (topic, ", ".join(unknown)))

    if problems:
        print("REFUSING TO REORDER:")
        for p in problems:
            print("  -", p)
        return 1

    moved = 0
    for topic, courses in data.items():
        order = {p: i for i, p in enumerate(SEQUENCE[topic])}
        before = [c["path"].lstrip("./") for c in courses["courses"]]
        courses["courses"].sort(key=lambda c: order[c["path"].lstrip("./")])
        after = [c["path"].lstrip("./") for c in courses["courses"]]
        moved += sum(1 for a, b in zip(before, after) if a != b)

    block = json.dumps(data, indent=4, ensure_ascii=False)
    open(INDEX, "w", encoding="utf-8").write(src[:start] + block + src[end:])

    print("tracks resequenced : %d" % len(data))
    print("modules that moved : %d" % moved)
    for topic in data:
        first = data[topic]["courses"][0]["title"]
        print("  %-16s now opens on: %s" % (topic, first))
    return 0


if __name__ == "__main__":
    sys.exit(main())
