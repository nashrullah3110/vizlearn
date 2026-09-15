# -*- coding: utf-8 -*-
"""The binary search questions.

Plain binary search and the rotated-array variant already live with the list
questions, so these are the three that test whether you understand the
invariant rather than the shape: writing it without an off-by-one, the
duplicate-boundary pair, and searching a space that is not an array at all.

Every `viz` here is built by running the thing it draws - see
tools/interview_viz.py for why that matters.
"""

import bisect as _bisect

from interview_viz import cost_table, frame, marked, pairs, row, cell, viz

BINSEARCH = []


def _q(**kw):
    BINSEARCH.append(kw)


# =========================================================================
# 1. binary search without an off-by-one
# =========================================================================

def _invariant_frames():
    """Recorded by running the half-open search and logging the live range."""
    a = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    lo, hi = 0, len(a)
    out = []
    while lo < hi:
        mid = (lo + hi) // 2
        marks = {j: ("dim" if j < lo or j >= hi else "lo")
                 for j in range(len(a))}
        marks[mid] = "hi"
        goes_right = a[mid] < target
        note = ("range is [%d, %d), so mid = %d and a[mid] = %d. %s"
                % (lo, hi, mid, a[mid],
                   "Too small, so lo = mid + 1 - mid itself is ruled out."
                   if goes_right else
                   "Not too small, so hi = mid - mid stays a candidate."))
        out.append(frame(
            marked(a, marks, {lo: "lo", mid: "mid"}, label="values"),
            note, {"lo": lo, "hi": hi, "width": hi - lo}))
        if goes_right:
            lo = mid + 1
        else:
            hi = mid
    found = lo < len(a) and a[lo] == target
    out.append(frame(
        marked(a, {j: ("hit" if j == lo and found else "dim")
                   for j in range(len(a))}, label="values"),
        "The range is empty, so the loop ends. lo = %d is where the value is "
        "or would go - here a[%d] = %d, so it was found. One final check "
        "distinguishes found from absent." % (lo, lo, a[lo]),
        {"lo": lo, "hi": hi, "width": hi - lo}))
    return viz(out)


_q(
    slug="binary-search-without-an-off-by-one",
    kind="coding",
    level="Easy",
    title="Write binary search without an off-by-one",
    asked="Write binary search. What makes it terminate, and where do the "
          "off-by-one errors come from?",
    desc="Binary search by invariant: a half-open range, why every branch must "
         "strictly shrink it, and the exact combination that loops forever.",
    lead="Keep a <strong>half-open range</strong> <code>[lo, hi)</code> and the "
         "loop writes itself: <code>while lo &lt; hi</code>, "
         "<code>lo = mid + 1</code> or <code>hi = mid</code>. Both branches "
         "strictly shrink the range, which is what guarantees termination "
         "&mdash; and <code>hi = mid</code> with an <em>inclusive</em> "
         "<code>hi</code> is the version that hangs.",
    say="\"I use a half-open range: lo inclusive, hi exclusive, loop while lo "
        "is less than hi. If a[mid] is less than the target, lo becomes mid + "
        "1, otherwise hi becomes mid. Both branches shrink the range strictly, "
        "so it terminates, and at the end lo is the insertion point - one "
        "comparison tells me whether the value is actually there.\"",
    notice=[
        "The range is <code>[lo, hi)</code>: <code>hi</code> is never a "
        "candidate.",
        "<code>lo = mid + 1</code> rules <em>mid</em> out; <code>hi = mid</code> "
        "keeps it.",
        "The loop ends with <code>lo</code> at the insertion point, found or "
        "not.",
    ],
    viz=_invariant_frames(),
    sections=[
        ("The invariant does the work",
         "<p>Binary search is three lines and most people can write a version "
         "that usually works. What separates that from a correct one is being "
         "able to say what is true at the top of every iteration: <em>if the "
         "target is present, it is in <code>[lo, hi)</code></em>.</p>"
         "<p>Everything follows. The loop condition is <code>lo &lt; hi</code>, "
         "because an empty range means the answer is not there. When "
         "<code>a[mid] &lt; target</code>, <code>mid</code> cannot be the "
         "answer, so <code>lo = mid + 1</code> excludes it. Otherwise "
         "<code>mid</code> might be the answer, so <code>hi = mid</code> keeps "
         "it in a half-open range. Neither branch can leave the range the same "
         "size, which is termination.</p>"),
        ("The two combinations that hang",
         "<p>Pair an <strong>inclusive</strong> <code>hi = len(a) - 1</code> "
         "with <code>hi = mid</code> and you have a loop that can stop making "
         "progress: when <code>hi = lo + 1</code>, <code>mid</code> equals "
         "<code>lo</code>, and setting <code>hi = mid</code> changes nothing. "
         "The editor below runs that version under a step cap so you can see "
         "it exhaust its budget rather than hanging the page.</p>"
         "<p>The mirror error is <code>lo = mid</code> instead of "
         "<code>lo = mid + 1</code>, which hangs for the same reason from the "
         "other side. The rule that avoids both: the branch that keeps "
         "<code>mid</code> as a candidate must be the one that moves the "
         "<em>exclusive</em> end.</p>"),
        ("The overflow line, and why Python does not need it",
         "<p>You will see <code>mid = lo + (hi - lo) // 2</code> in every "
         "C and Java implementation, and the reason is real: "
         "<code>lo + hi</code> can exceed the integer width on a large array, "
         "a bug that sat in the JDK for nine years.</p>"
         "<p>Python integers are arbitrary precision, so "
         "<code>(lo + hi) // 2</code> is safe here &mdash; and the editor "
         "prints both forms agreeing at 2<sup>62</sup> to show it. Knowing "
         "<em>why</em> the idiom exists is worth more than using it: it is a "
         "good answer to \"is there anything else to say about this line?\"</p>"),
        ("What to use instead",
         "<p>In real Python, <code>bisect</code>. "
         "<code>bisect_left(a, x)</code> is exactly this loop, written in C, "
         "and it returns the insertion point &mdash; which is strictly more "
         "useful than a boolean, because it answers \"where would it go\" as "
         "well as \"is it there\". The <a href=\"first-and-last-position.html\">"
         "next question</a> is entirely about that.</p>"
         "<p>Write the loop when asked to, and say that you would reach for "
         "<code>bisect</code> in production. Both halves of that answer are "
         "being listened for.</p>"),
    ],
    code={
        "file": "binary_search.py",
        "intro": "The half-open version, the inclusive version that stops "
                 "making progress, and the overflow idiom that Python does not "
                 "need but every other language does.",
        "code": '''def search(a, x):
    """Half-open range [lo, hi). Both branches strictly shrink it."""
    lo, hi = 0, len(a)                 # hi is EXCLUSIVE
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1               # mid is ruled out
        else:
            hi = mid                   # mid is still a candidate
    return lo if lo < len(a) and a[lo] == x else -1


a = list(range(0, 100, 2))
print("a = [0, 2, 4, ..., 98]")
for v in (0, 50, 98, 51):
    print(f"  search(a, {v:>2}) = {search(a, v):>3}", "(-1 means absent)" if search(a, v) < 0 else "")

# The version that stops making progress, run under a cap so it cannot hang.
def stuck(a, x, cap=40):
    lo, hi, steps = 0, len(a) - 1, 0   # hi INCLUSIVE, paired with hi = mid
    while lo < hi and steps < cap:
        steps += 1
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid                   # <- forgot the + 1
        else:
            hi = mid
    return steps

print()
print("the inclusive-hi version with lo = mid:")
print(f"  used all {stuck(a, 51)} of its 40 allowed steps -> it never terminates")
print("  when hi == lo + 1, mid == lo, and neither branch changes anything")

# Termination, stated as the thing that is true every iteration.
print()
print("the invariant: if x is in a, it is in a[lo:hi]")
print("  lo = mid + 1  excludes mid   (a[mid] was too small)")
print("  hi = mid      keeps mid      (hi is exclusive)")
print("  the width hi - lo strictly decreases, so the loop ends")

# The overflow idiom, and why Python is exempt.
lo, hi = 2**62, 2**62 + 4
print()
print("on a huge range:")
print("  (lo + hi) // 2      =", (lo + hi) // 2, " <- fine in Python")
print("  lo + (hi - lo) // 2 =", lo + (hi - lo) // 2, " <- the portable idiom")
print("  same answer:", (lo + hi) // 2 == lo + (hi - lo) // 2)
print("  in C or Java the first overflows; that bug was in the JDK for years")

# And what you would actually use.
import bisect
print()
print("bisect_left is this loop, in C:")
print("  bisect.bisect_left(a, 50) =", bisect.bisect_left(a, 50))
print("  it returns the insertion point, which is more useful than a boolean")
''',
        "walk": [
            ("lo, hi = 0, len(a)",
             "<code>hi</code> starts one past the end because it is exclusive. "
             "That single choice is what makes the rest of the loop write "
             "itself."),
            ("lo = mid + 1",
             "<code>a[mid]</code> was too small, so <code>mid</code> cannot be "
             "the answer and must leave the range. The <code>+ 1</code> is not "
             "optional."),
            ("hi = mid",
             "<code>mid</code> might be the answer, and because <code>hi</code> "
             "is exclusive, setting it to <code>mid</code> keeps "
             "<code>mid</code> in the range while still shrinking it."),
            ("stuck(a, 51)",
             "Run under a step cap on purpose. An inclusive <code>hi</code> "
             "with <code>lo = mid</code> can reach a state where neither end "
             "moves &mdash; the loop is alive and making no progress."),
        ],
        "try": [
            "Change <code>hi = mid</code> to <code>hi = mid - 1</code> in "
            "<code>search</code> and look for the value that is now missed. "
            "The bug is silent, which is why the invariant matters more than "
            "the shape.",
            "Return <code>lo</code> instead of <code>-1</code> on a miss. That "
            "is <code>bisect_left</code>, and it is the version most real "
            "problems want.",
        ],
    },
    check=[
        {"q": "In the half-open form, what does hi mean?",
         "options": ["The last valid index",
                     "One past the last candidate - hi is never itself a candidate",
                     "The midpoint",
                     "The array length minus one"],
         "answer": 1,
         "why": "Exclusive hi is what lets hi = mid keep mid as a candidate "
                "while still shrinking the range."},
        {"q": "Why must one branch be lo = mid + 1 rather than lo = mid?",
         "options": ["For speed",
                     "Because a[mid] was ruled out, and without the +1 the range can stop shrinking",
                     "To handle duplicates",
                     "It makes no difference"],
         "answer": 1,
         "why": "When hi is lo + 1, mid equals lo, so lo = mid leaves the "
                "range unchanged and the loop never ends."},
        {"q": "What does lo hold when the loop exits?",
         "options": ["-1 if absent",
                     "The insertion point: where the value is, or where it would go",
                     "The midpoint of the array",
                     "The array length"],
         "answer": 1,
         "why": "Which is why one extra comparison converts it into found or "
                "not found - and why bisect returns it directly."},
        {"q": "Why does lo + (hi - lo) // 2 appear in C implementations?",
         "options": ["It is faster",
                     "lo + hi can overflow a fixed-width integer; Python's integers cannot",
                     "It handles negative indices",
                     "It rounds differently"],
         "answer": 1,
         "why": "A real bug that sat in the JDK for years. In Python the "
                "simple form is safe, but knowing why the idiom exists is the "
                "point."},
    ],
)


# =========================================================================
# 2. first and last position
# =========================================================================

def _boundary_frames():
    """Recorded from real bisect calls on an array with duplicates."""
    a = [1, 2, 2, 2, 5, 8]
    x = 2
    left = _bisect.bisect_left(a, x)
    right = _bisect.bisect_right(a, x)
    out = [frame(
        marked([str(v) for v in a],
               {j: ("hit" if v == x else "dim") for j, v in enumerate(a)},
               label="values"),
        "Three 2s, at indices 1, 2 and 3. A plain binary search finds *a* 2 - "
        "which one depends on where mid happened to land, so it cannot answer "
        "'first' or 'last'.",
        {"left": left, "right": right, "count": right - left}),
        frame(
        marked([str(v) for v in a],
               {j: ("lo" if j == left else "dim") for j in range(len(a))},
               {left: "left"}, label="values"),
        "bisect_left(a, 2) = %d: the first index where a 2 could be inserted "
        "and keep the array sorted. Everything before it is strictly less "
        "than 2." % left,
        {"left": left, "right": right, "count": right - left}),
        frame(
        marked([str(v) for v in a],
               {j: ("hi" if j == right else "dim") for j in range(len(a))},
               {right: "right"}, label="values"),
        "bisect_right(a, 2) = %d: one past the last 2. Everything from here on "
        "is strictly greater. So the last 2 is at index %d."
        % (right, right - 1),
        {"left": left, "right": right, "count": right - left}),
        frame(
        marked([str(v) for v in a],
               {j: ("done" if left <= j < right else "dim")
                for j in range(len(a))}, label="values"),
        "The pair brackets the run: [%d, %d). Its width, %d, is the count - "
        "which is the third question the same two calls answer."
        % (left, right, right - left),
        {"left": left, "right": right, "count": right - left})]
    absent = _bisect.bisect_left(a, 3)
    out.append(frame(
        marked([str(v) for v in a],
               {j: ("bad" if j == absent else "dim") for j in range(len(a))},
               {absent: "both"}, label="searching for 3"),
        "For a value that is absent, left and right are equal (%d) - the empty "
        "range means not present, and the index is still where it would go."
        % absent,
        {"left": absent, "right": _bisect.bisect_right(a, 3), "count": 0}))
    return viz(out)


_q(
    slug="first-and-last-position",
    kind="coding",
    level="Medium",
    title="First and last position of a target",
    asked="Find the first and last index of a value in a sorted array with "
          "duplicates. O(log n).",
    desc="Boundary binary search with bisect_left and bisect_right: why a "
         "plain search cannot answer 'first', and the three questions the pair "
         "answers at once.",
    lead="A plain binary search finds <em>some</em> occurrence, and which one "
         "depends on where <code>mid</code> landed. The boundaries need two "
         "searches: <code>bisect_left</code> for the first index where the "
         "value could go, <code>bisect_right</code> for one past the last. "
         "Together they bracket the run &mdash; and their difference is the "
         "count.",
    say="\"Two binary searches. bisect_left gives the first index where the "
        "value could be inserted, bisect_right gives one past the last, so the "
        "answer is left and right minus one. If left equals right the value is "
        "absent. Each is O(log n), and the difference between them is the "
        "count, which is usually the next thing I am asked for.\"",
    notice=[
        "A plain search finds an arbitrary occurrence &mdash; that is why this "
        "needs a different loop.",
        "<code>bisect_right</code> is <em>one past</em> the last, so the last "
        "index is <code>right - 1</code>.",
        "When the value is absent the two are equal, which is the "
        "not-found test.",
    ],
    viz=_boundary_frames(),
    sections=[
        ("Why a plain search is not enough",
         "<p>With duplicates, the standard loop stops at whichever occurrence "
         "<code>mid</code> hit first. That is a correct answer to \"is it "
         "there\" and no answer at all to \"where does the run start\" &mdash; "
         "and scanning left from the hit is O(n) in the worst case, which "
         "throws away the reason for using binary search.</p>"
         "<p>The fix is to stop searching for the value and start searching "
         "for the <em>boundary</em>. On finding a match, do not return: keep "
         "going in the direction of the edge you want. That is the only change, "
         "and it is what both <code>bisect</code> functions do.</p>"),
        ("left and right, precisely",
         "<p><code>bisect_left(a, x)</code> returns the first index "
         "<code>i</code> such that <code>a[i] &gt;= x</code>. So everything "
         "before it is strictly less than <code>x</code>, and if "
         "<code>x</code> is present, <code>i</code> is its first "
         "occurrence.</p>"
         "<p><code>bisect_right(a, x)</code> returns the first index "
         "<code>i</code> such that <code>a[i] &gt; x</code>. So it is one past "
         "the last occurrence, and the last index is "
         "<code>right - 1</code>.</p>"
         "<p>Three consequences, and they are why the pair is worth memorising. "
         "<code>left == right</code> means absent. "
         "<code>right - left</code> is the count. And "
         "<code>a[left:right]</code> is the run itself, as a slice.</p>"),
        ("Writing it by hand",
         "<p>The interviewer usually wants the loop, not the import. It is the "
         "half-open search from the "
         "<a href=\"binary-search-without-an-off-by-one.html\">previous "
         "question</a> with one comparison changed:</p>"
         "<pre><code>def lower(a, x):          # bisect_left\n"
         "    lo, hi = 0, len(a)\n"
         "    while lo &lt; hi:\n"
         "        mid = (lo + hi) // 2\n"
         "        if a[mid] &lt; x:  lo = mid + 1\n"
         "        else:            hi = mid\n"
         "    return lo\n\n"
         "def upper(a, x):          # bisect_right\n"
         "    lo, hi = 0, len(a)\n"
         "    while lo &lt; hi:\n"
         "        mid = (lo + hi) // 2\n"
         "        if a[mid] &lt;= x: lo = mid + 1   # &lt;= is the only difference\n"
         "        else:            hi = mid\n"
         "    return lo</code></pre>"
         "<p>One character. <code>&lt;</code> stops at the first element not "
         "less than <code>x</code>; <code>&lt;=</code> steps over every "
         "element equal to it. Being able to point at that character and say "
         "what it does is the whole question.</p>"),
        ("The key= trap",
         "<p><code>bisect</code> gained a <code>key=</code> parameter in Python "
         "3.10, and it behaves differently from <code>sorted(key=...)</code> in "
         "a way that catches people: the <em>needle</em> is not passed through "
         "the key. So searching a list of records by one field means comparing "
         "against the field value directly, not against a record:</p>"
         "<pre><code>i = bisect_left(people, 30, key=lambda p: p.age)"
         "</code></pre>"
         "<p>Before 3.10 the standard workaround was to keep a parallel list "
         "of just the keys and search that &mdash; which is still what you do "
         "when the key is expensive to compute, because <code>key=</code> "
         "calls it on every probe.</p>"),
    ],
    code={
        "file": "boundaries.py",
        "intro": "Both boundaries from bisect and from the hand-written loops, "
                 "the three questions one pair of calls answers, and the "
                 "absent case.",
        "code": '''import bisect

a = [1, 2, 2, 2, 5, 8]
print("a =", a)
print("bisect_left (a, 2) =", bisect.bisect_left(a, 2), " <- first index a 2 could go")
print("bisect_right(a, 2) =", bisect.bisect_right(a, 2), " <- one past the last 2")

def first_last(a, x):
    lo = bisect.bisect_left(a, x)
    if lo == len(a) or a[lo] != x:
        return (-1, -1)
    return (lo, bisect.bisect_right(a, x) - 1)

print()
for x in (2, 5, 3, 9):
    print(f"  first_last(a, {x}) = {first_last(a, x)}")

# The same two calls answer three questions.
left, right = bisect.bisect_left(a, 2), bisect.bisect_right(a, 2)
print()
print("one pair of calls gives:")
print("  first index :", left)
print("  last index  :", right - 1)
print("  count       :", right - left)
print("  the run     :", a[left:right])

# By hand: the two loops differ by one character.
def lower(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:  lo = mid + 1
        else:           hi = mid
    return lo

def upper(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= x: lo = mid + 1      # <= instead of <
        else:           hi = mid
    return lo

print()
print("hand-written agrees with bisect:")
for x in (1, 2, 5, 8, 3):
    print(f"  x={x}  lower {lower(a,x)}=={bisect.bisect_left(a,x)}",
          f" upper {upper(a,x)}=={bisect.bisect_right(a,x)}",
          lower(a,x)==bisect.bisect_left(a,x) and upper(a,x)==bisect.bisect_right(a,x))

# Absent values: equal boundaries, and the index is still useful.
print()
for x in (0, 3, 100):
    l, r = bisect.bisect_left(a, x), bisect.bisect_right(a, x)
    print(f"  x={x:>3}  left={l} right={r}  present:", l != r,
          f" would insert at {l}")

# key= does NOT transform the needle (Python 3.10+).
people = [("ann", 22), ("bob", 30), ("cas", 41)]
i = bisect.bisect_left(people, 30, key=lambda p: p[1])
print()
print("searching records by age with key=:", i, "->", people[i])
print("note the needle is 30, not ('x', 30)")
''',
        "walk": [
            ("if lo == len(a) or a[lo] != x",
             "The not-found test. <code>bisect_left</code> always returns an "
             "insertion point, so it never tells you on its own whether the "
             "value is there."),
            ("bisect.bisect_right(a, x) - 1",
             "The minus one is the whole reason people get this wrong. "
             "<code>bisect_right</code> is one <em>past</em> the run."),
            ("if a[mid] <= x: lo = mid + 1",
             "The single character that turns a lower bound into an upper "
             "bound. <code>&lt;=</code> steps over equal elements instead of "
             "stopping at them."),
            ("bisect_left(people, 30, key=lambda p: p[1])",
             "The needle is the key value, not a record. This is the opposite "
             "of how <code>sorted(key=...)</code> works and it surprises "
             "everybody once."),
        ],
        "try": [
            "Remove the <code>a[lo] != x</code> check and search for 3. You get "
            "<code>(4, 3)</code> &mdash; a last index before the first, which "
            "is what an unguarded insertion point looks like.",
            "Build a parallel list of ages and <code>bisect</code> that instead "
            "of using <code>key=</code>. That is the pre-3.10 idiom and still "
            "the right one when the key is expensive.",
        ],
    },
    check=[
        {"q": "Why can't a plain binary search answer 'first occurrence'?",
         "options": ["It is too slow",
                     "It stops at whichever occurrence mid happened to hit",
                     "It cannot handle duplicates at all",
                     "It returns a boolean"],
         "answer": 1,
         "why": "Any of the duplicates is a valid stopping point, so you have "
                "to search for the boundary instead of the value."},
        {"q": "What does bisect_right return?",
         "options": ["The last occurrence",
                     "One past the last occurrence",
                     "The first occurrence",
                     "The midpoint of the run"],
         "answer": 1,
         "why": "Which is why the last index is right - 1, and why "
                "right - left is the count."},
        {"q": "How do you tell that a value is absent?",
         "options": ["bisect_left returns -1",
                     "bisect_left equals bisect_right - the bracketed range is empty",
                     "It raises ValueError",
                     "bisect_right returns len(a)"],
         "answer": 1,
         "why": "Both return the same insertion point, so the run has zero "
                "width. Neither function ever returns -1."},
        {"q": "What is the only difference between the two hand-written loops?",
         "options": ["The loop condition",
                     "< becomes <=, so equal elements are stepped over rather than stopped at",
                     "One searches backwards",
                     "The initial value of hi"],
         "answer": 1,
         "why": "One character. Being able to point at it and say what it does "
                "is the question."},
    ],
)


# =========================================================================
# 3. binary search on the answer
# =========================================================================

def _predicate_frames():
    """Recorded by running the search over capacities."""
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    D = 5

    def days_needed(capacity):
        days, load = 1, 0
        for w in weights:
            if load + w > capacity:
                days += 1
                load = 0
            load += w
        return days

    lo, hi = max(weights), sum(weights)
    out = []
    while lo < hi:
        mid = (lo + hi) // 2
        d = days_needed(mid)
        ok = d <= D
        span = hi - lo + 1
        out.append(frame(
            pairs([("range of capacities", "[%d, %d]" % (lo, hi)),
                   ("trying capacity", str(mid)),
                   ("days needed", str(d)),
                   ("within %d days?" % D, "yes" if ok else "no")],
                  {"within %d days?" % D: "hit" if ok else "bad"},
                  label="probe %d" % (len(out) + 1)),
            "Capacity %d needs %d days, which is %s. So %s - the range halves "
            "without trying any of the other capacities."
            % (mid, d, "enough" if ok else "too slow",
               "nothing larger than %d can be needed" % mid if ok
               else "anything this small or smaller is ruled out"),
            {"lo": lo, "hi": hi, "candidates": span}))
        if ok:
            hi = mid
        else:
            lo = mid + 1
    out.append(frame(
        pairs([("answer", str(lo)),
               ("days at %d" % lo, str(days_needed(lo))),
               ("days at %d" % (lo - 1), str(days_needed(lo - 1))),
               ("probes used", str(len(out)))],
              {"answer": "hit"}, label="the boundary"),
        "Capacity %d works and %d does not, so %d is the smallest that does. "
        "%d probes instead of %d candidates."
        % (lo, lo - 1, lo, len(out), sum(weights) - max(weights) + 1),
        {"lo": lo, "hi": hi, "candidates": 1}))
    return viz(out)


_q(
    slug="binary-search-on-the-answer",
    kind="coding",
    level="Medium",
    title="Binary search on the answer, not the array",
    asked="Given package weights and D days, what is the smallest ship "
          "capacity that delivers them all in time?",
    desc="Searching a space of answers rather than an array: find the "
          "monotonic predicate, check feasibility in O(n), and binary search "
          "the boundary in O(n log range).",
    lead="There is no array to search here. The trick is that "
         "<em>feasibility is monotonic</em>: if a capacity works, every larger "
         "one works too. So the answers form a sorted sequence of no-no-no-"
         "yes-yes, and binary search finds the boundary &mdash; with an O(n) "
         "feasibility check in place of an array lookup.",
    say="\"I binary search the answer rather than an array. The predicate is "
        "'can this capacity finish in D days', which I can check in one pass, "
        "and it is monotonic - if a capacity works, anything bigger works. So "
        "the feasible capacities are a suffix, and I search for the first one. "
        "Bounds are max weight to total weight, so it is O(n log sum).\"",
    notice=[
        "The thing being searched is a <em>range of answers</em>, not the "
        "input.",
        "Each probe costs a full O(n) pass &mdash; the feasibility check.",
        "The predicate flips exactly once, which is what makes it searchable.",
    ],
    viz=_predicate_frames(),
    sections=[
        ("Recognising it",
         "<p>The tell is a question of the form \"what is the smallest "
         "<em>X</em> such that something is possible\" &mdash; smallest "
         "capacity, minimum speed, fewest days, largest minimum distance. "
         "There is no sorted array in the input, which is why the shape gets "
         "missed.</p>"
         "<p>What is sorted is the <strong>answer space</strong>. If you can "
         "write a function <code>feasible(x)</code> that is "
         "<code>False</code> for every <code>x</code> below the answer and "
         "<code>True</code> for every <code>x</code> at or above it, then the "
         "sequence <code>feasible(lo) ... feasible(hi)</code> is sorted "
         "&mdash; and finding where it flips is exactly binary search.</p>"),
        ("The three things to establish before writing the loop",
         "<p><strong>The predicate.</strong> Here, \"can capacity "
         "<code>c</code> deliver everything in <code>D</code> days?\" Greedily "
         "load until the next package would overflow, then start a new day. "
         "One pass, O(n), and greedy is optimal for it because leaving room "
         "spare can never reduce the day count.</p>"
         "<p><strong>Monotonicity.</strong> A bigger ship cannot need more "
         "days. State it &mdash; this is the step that makes the search valid, "
         "and an interviewer will ask why you are allowed to binary search "
         "something with no array in it.</p>"
         "<p><strong>The bounds.</strong> <code>lo = max(weights)</code>, "
         "because a package must fit in one trip. <code>hi = sum(weights)</code>, "
         "because that always finishes in one day. Getting the low bound wrong "
         "&mdash; starting at 1, or at 0 &mdash; produces a search over "
         "capacities that can never work, and the loop returns an infeasible "
         "answer rather than looping forever, which is worse.</p>"),
        ("Cost, and the shape of it",
         "<p>O(n log(sum &minus; max)): a logarithmic number of probes, each "
         "costing a linear pass. Note that the log is over the "
         "<em>magnitude</em> of the answer range rather than the size of the "
         "input, which is unusual and worth saying &mdash; it means the "
         "complexity depends on the numbers, not just on how many there are.</p>"
         "<p>The editor below prints the probe table. Ten packages give a range "
         "of 46 candidate capacities and the search settles it in five "
         "probes.</p>"),
        ("The same shape, four other questions",
         "<p><strong>Koko eating bananas</strong> &mdash; smallest eating speed "
         "to finish in H hours. Identical, with <code>ceil(pile / speed)</code> "
         "as the per-pile cost.</p>"
         "<p><strong>Split an array into k subarrays</strong> minimising the "
         "largest sum. The predicate is \"can we do it with all parts at most "
         "<code>m</code>\", and it is the same greedy pass.</p>"
         "<p><strong>Aggressive cows / maximum minimum distance</strong> "
         "&mdash; place k items as far apart as possible. The monotonicity "
         "flips direction: large distances are infeasible, so you search for "
         "the last <code>True</code> instead of the first.</p>"
         "<p><strong>The square root of an integer</strong>, or any inverse of "
         "a monotonic function. Once the pattern is visible, \"is there a "
         "monotonic predicate here?\" becomes a routine question to ask of any "
         "minimisation problem.</p>"),
    ],
    code={
        "file": "search_the_answer.py",
        "intro": "The probe table, the monotonicity that licenses the search, "
                 "and the same technique applied to a second problem to show "
                 "it is a shape rather than a trick.",
        "code": '''def min_capacity(weights, D):
    """Smallest ship capacity that delivers every package within D days."""
    def days_needed(capacity):
        days, load = 1, 0
        for w in weights:
            if load + w > capacity:       # greedy: start a new day
                days += 1
                load = 0
            load += w
        return days

    lo, hi = max(weights), sum(weights)   # must fit one package; one day at most
    probes = []
    while lo < hi:
        mid = (lo + hi) // 2
        d = days_needed(mid)
        probes.append((mid, d, d <= D))
        if d <= D:
            hi = mid                      # this works, so nothing larger is needed
        else:
            lo = mid + 1                  # too slow, so rule it and everything below out
    return lo, probes, days_needed


weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
D = 5
answer, probes, days_needed = min_capacity(weights, D)

print("weights:", weights, " D =", D)
print()
print("capacity | days | feasible")
for cap, d, ok in probes:
    print(f"   {cap:>5}  |  {d:>3} | {'yes' if ok else 'no'}")
print()
print("smallest capacity that works:", answer)

# Monotonicity is what licenses the search. Check it explicitly.
print()
print("the predicate flips exactly once:")
for cap in range(answer - 3, answer + 3):
    d = days_needed(cap)
    print(f"  capacity {cap:>2} -> {d} days,",
          "feasible" if d <= D else "not feasible")

candidates = sum(weights) - max(weights) + 1
print()
print(f"brute force: {candidates} capacities from {max(weights)} to {sum(weights)}")
print(f"binary search: {len(probes)} probes, each an O(n) pass")

# The same shape, a different question: minimum eating speed.
import math

def min_speed(piles, hours):
    def hours_needed(speed):
        return sum(math.ceil(p / speed) for p in piles)
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= hours:
            hi = mid
        else:
            lo = mid + 1
    return lo

piles = [30, 11, 23, 4, 20]
print()
print("piles:", piles)
for h in (5, 6, 8):
    s = min_speed(piles, h)
    print(f"  finish in {h} hours -> speed {s:>2}",
          f"(takes {sum(math.ceil(p/s) for p in piles)} hours)")
print("same structure: a monotonic predicate, checked in O(n), searched in log")
''',
        "walk": [
            ("lo, hi = max(weights), sum(weights)",
             "The bounds are part of the answer. Below <code>max</code> no "
             "capacity can work at all, and <code>sum</code> always finishes "
             "in one day, so the boundary is guaranteed to be inside."),
            ("if load + w > capacity: days += 1",
             "The feasibility check, greedy and O(n). Greedy is optimal here "
             "because leaving space unused can never reduce the number of "
             "days."),
            ("hi = mid",
             "A feasible capacity is kept as a candidate, exactly like the "
             "lower-bound search &mdash; you are looking for the first "
             "<code>True</code>, not for any <code>True</code>."),
            ("for cap in range(answer - 3, answer + 3)",
             "Printing the predicate either side of the boundary is how you "
             "check monotonicity rather than assuming it. A predicate that "
             "flips more than once cannot be binary searched."),
        ],
        "try": [
            "Set <code>lo = 1</code> instead of <code>max(weights)</code> and "
            "look at the answer. It is still correct here &mdash; work out why, "
            "and then find an input where it would not be.",
            "Change the question to \"the largest minimum gap when placing k "
            "items\". The monotonicity reverses, so you search for the last "
            "feasible value instead of the first.",
        ],
    },
    check=[
        {"q": "What is being binary searched?",
         "options": ["The array of weights",
                     "The range of possible answers - capacities",
                     "The days",
                     "A sorted copy of the input"],
         "answer": 1,
         "why": "There is no sorted array in the input. What is sorted is the "
                "sequence of feasible/infeasible answers."},
        {"q": "What property must the predicate have?",
         "options": ["It must be O(1)",
                     "It must be monotonic - once true, true for everything larger",
                     "It must be invertible",
                     "It must be exact"],
         "answer": 1,
         "why": "Monotonicity is what makes the answer space sorted, and "
                "without it a probe tells you nothing about the other half."},
        {"q": "What is the complexity?",
         "options": ["O(log n)", "O(n log(range of answers))",
                     "O(n)", "O(n squared)"],
         "answer": 1,
         "why": "Logarithmically many probes, each costing a linear "
                "feasibility pass - and the log is over the magnitude of the "
                "answer range, not over n."},
        {"q": "Why is lo initialised to max(weights)?",
         "options": ["To make the search faster",
                     "Because a single package must fit in one trip, so smaller capacities can never work",
                     "Because it is the answer for D = n",
                     "It is arbitrary"],
         "answer": 1,
         "why": "The bounds have to bracket the boundary. Starting below the "
                "feasible range risks returning an answer that does not work."},
    ],
)
