# -*- coding: utf-8 -*-
"""The list and array questions.

Conceptual first, because "why is `in` slow on a list?" is the answer to half
the coding problems underneath it. Same shape as tools/interview_strings.py;
see tools/interview.py for the fields each entry carries.
"""

from interview_viz import (frame, linear_scan, marked, pairs, two_pointer_sum,
                           viz)

LISTS = []


def _q(**kw):
    LISTS.append(kw)


# =========================================================================
# Conceptual
# =========================================================================

def _dynamic_array_frames():
    out = [frame(marked(["10", "20", "30", "-", "-", "-", "-", "-"],
                        {i: "done" for i in range(3)}, label="capacity 8"),
                 "Three items in a block sized for eight. The spare slots are "
                 "why append is usually free.",
                 {"len": 3, "capacity": 8})]
    out.append(frame(marked(["10", "20", "30", "40", "-", "-", "-", "-"],
                            {3: "hit"}, label="capacity 8"),
                     "append writes into a slot that already exists: one store, "
                     "no allocation. O(1).",
                     {"len": 4, "capacity": 8}))
    out.append(frame(marked(["10", "20", "30", "40", "50", "60", "70", "80"],
                            {i: "done" for i in range(8)}, label="capacity 8"),
                     "Full. The next append cannot write in place.",
                     {"len": 8, "capacity": 8}))
    out.append(frame(marked(["10", "20", "30", "40", "50", "60", "70", "80",
                             "90", "-", "-", "-", "-", "-", "-", "-"],
                            {8: "hit"}, label="capacity 16"),
                     "A bigger block is allocated and everything is copied over - "
                     "O(n), but only once every doubling. Amortised, append is "
                     "still O(1).",
                     {"len": 9, "capacity": 16}))
    out.append(frame(marked(["5", "10", "20", "30", "40", "50", "60", "70", "80"],
                            {i: "bad" for i in range(1, 9)}, label="insert(0, 5)"),
                     "insert(0, x) has to shift EVERY existing item one slot "
                     "right. That is O(n), and it is the same cost as pop(0).",
                     {"len": 9, "capacity": 16}))
    return viz(out)


_q(
    slug="what-is-a-python-list-underneath",
    kind="concept",
    level="Easy",
    title="What is a Python list underneath?",
    asked="What is a Python list actually implemented as, and why does that "
          "make append O(1) but insert(0, x) O(n)?",
    desc="A Python list is a dynamic array of pointers: why indexing is O(1), "
         "why append is amortised O(1) through over-allocation, and why "
         "inserting at the front is O(n).",
    lead="A <strong>dynamic array of references</strong> &mdash; one contiguous "
         "block of pointers, over-allocated so there is usually spare room. "
         "Indexing is O(1) because the address is computed. <code>append</code> "
         "is amortised O(1) because it usually writes into a spare slot. "
         "<code>insert(0, x)</code> is O(n) because everything has to shift.",
    say="\"It's a dynamic array of pointers, over-allocated. Indexing is O(1) "
        "arithmetic, append is amortised O(1) because growth doubles, and "
        "anything that touches the front is O(n) because the rest has to shift.\"",
    notice=[
        "The spare slots are the reason <code>append</code> is normally free.",
        "The reallocation copies everything &mdash; once per doubling, not per "
        "append.",
        "The last frame is the same cost as <code>pop(0)</code>, in the other "
        "direction.",
    ],
    viz=_dynamic_array_frames(),
    sections=[
        ("An array of pointers, not of objects",
         "<p>The block holds <em>references</em>, all the same size, which is why "
         "one list can hold an int, a string and another list at once. It is "
         "also why <code>sys.getsizeof</code> on a list of a million integers is "
         "far smaller than the integers themselves &mdash; the list only stores "
         "the pointers.</p>"
         "<p>Because the references are contiguous and equally sized, element "
         "<em>i</em> lives at a computable address. That is the whole reason "
         "indexing is O(1) and a <a href=\"../dsa/linked_lists.html\">linked "
         "list</a> is not.</p>"),
        ("Why append is amortised O(1)",
         "<p>CPython allocates more room than the list currently needs. Most "
         "appends write into a spare slot: one store, no allocation. When the "
         "block fills, a larger one is allocated and everything is copied "
         "&mdash; O(n), but only on that one append.</p>"
         "<p>Because the growth is geometric, the copies are rare enough that "
         "the cost spread over n appends is constant each. That is what "
         "\"amortised\" means, and it is worth saying the word: any individual "
         "append can be the expensive one, which matters if you care about "
         "latency rather than throughput.</p>"),
        ("Why the front is expensive",
         "<p><code>insert(0, x)</code> and <code>pop(0)</code> both have to move "
         "every other element one slot, so both are O(n). Doing either in a loop "
         "is O(n&sup2;), and that is the single most common accidental "
         "quadratic in Python &mdash; usually written as a queue.</p>"
         "<p><code>collections.deque</code> is the fix: a doubly linked list of "
         "blocks, O(1) at both ends. It gives up O(1) random access in "
         "exchange, which is almost always the right trade when you only touch "
         "the ends.</p>"),
    ],
    code={
        "file": "list_internals.py",
        "intro": "The over-allocation made visible with <code>sys.getsizeof</code>, "
                 "then the three operations timed against each other so the O(1) "
                 "and the O(n) are numbers rather than claims.",
        "code": '''# A Python list is a dynamic array of references. Everything follows.
import sys, time
from collections import deque

# --- growth is over-allocated, in steps --------------------------------
lst = []
previous = sys.getsizeof(lst)
print("length  bytes   (only the rows where it reallocated)")
for i in range(1, 40):
    lst.append(i)
    size = sys.getsizeof(lst)
    if size != previous:
        print(f"{i:>6}  {size:>5}   <- grew, with room to spare")
        previous = size

# --- the list stores pointers, not the objects -------------------------
numbers = list(range(1000))
print()
print("list of 1000 ints :", sys.getsizeof(numbers), "bytes")
print("one int alone     :", sys.getsizeof(numbers[500]), "bytes")
print("The list holds references; the integers live elsewhere.")

# --- the three costs, measured -----------------------------------------
N = 30_000
print()
print(f"{'operation':>22} {'time':>10}")
for label, make, action in [
    ("append (end)",        list,  lambda c: c.append(1)),
    ("insert(0, x) (front)", list,  lambda c: c.insert(0, 1)),
    ("deque.appendleft",    deque, lambda c: c.appendleft(1)),
]:
    container = make()
    start = time.time()
    for _ in range(N):
        action(container)
    print(f"{label:>22} {time.time() - start:>9.4f}s")

print()
print(f"Same {N:,} operations. insert(0, x) shifts every existing element,")
print("so it is O(n) each and O(n^2) overall. deque is O(1) at both ends.")

# --- indexing does not care how long the list is -----------------------
small, big = list(range(10)), list(range(10_000_000))
print()
for name, data in (("10 items", small), ("10,000,000 items", big)):
    start = time.time()
    for _ in range(100_000):
        _ = data[len(data) // 2]
    print(f"  100,000 index reads on {name:>18}: {time.time() - start:.4f}s")
print("Indexing is address arithmetic. The length never enters into it.")
''',
        "walk": [
            ("sys.getsizeof(lst)",
             "The size jumps in steps, not per item. Those jumps are the "
             "reallocations; between them every append is a single store into "
             "memory that was already reserved."),
            ("append versus insert(0, x)",
             "The same number of operations, wildly different timings. "
             "<code>insert(0, x)</code> moves every existing element one slot, "
             "so n of them is O(n&sup2;)."),
            ("deque.appendleft",
             "A doubly linked list of blocks, so both ends are O(1). It is the "
             "fix for anything that behaves like a queue &mdash; and it gives up "
             "O(1) indexing in return."),
            ("data[len(data) // 2]",
             "Identical timings on ten items and ten million. Address arithmetic "
             "does not care how much is stored, which is precisely what a linked "
             "list cannot offer."),
        ],
        "try": [
            "Double <code>N</code>. The append timing doubles; the "
            "<code>insert(0, x)</code> timing roughly quadruples.",
            "Compare <code>sys.getsizeof</code> for a list of 1,000 integers "
            "against <code>array.array('i', range(1000))</code>. The array "
            "stores values, not pointers.",
        ],
    },
    check=[
        {"q": "A Python list is implemented as:",
         "options": ["A linked list of nodes", "A dynamic array of references",
                     "A hash table", "A balanced tree"],
         "answer": 1,
         "why": "Contiguous, equally sized references, over-allocated. That is "
                "why indexing is O(1) and why the references can point at "
                "objects of any type."},
        {"q": "Why is append 'amortised' O(1) rather than simply O(1)?",
         "options": ["It is always O(1)", "Occasionally it reallocates and "
                     "copies everything, which is O(n)",
                     "It depends on the item", "Because lists are sorted"],
         "answer": 1,
         "why": "Growth is geometric, so the copies are rare enough to average "
                "out - but any individual append can be the expensive one."},
        {"q": "insert(0, x) is O(n) because:",
         "options": ["The list is copied", "Every existing element shifts one "
                     "slot right",
                     "Python checks the type", "It reallocates every time"],
         "answer": 1,
         "why": "Contiguous storage means making room at the front costs a move "
                "of everything after it. deque avoids this entirely."},
    ],
)


def _aliasing_frames():
    out = [frame(pairs([("row", "[0, 0, 0]  @0x1f40")], {"row": "lo"},
                       label="one list object"),
                 "One row object exists.",
                 {"objects": 1})]
    out.append(frame(pairs([("grid[0]", "@0x1f40"), ("grid[1]", "@0x1f40"),
                            ("grid[2]", "@0x1f40")],
                           {"grid[1]": "bad", "grid[2]": "bad"},
                           label="[[0]*3] * 3"),
                     "Multiplying the OUTER list repeats the reference. All "
                     "three rows are the same object.",
                     {"objects": 1}))
    out.append(frame([pairs([("grid[0]", "[9, 0, 0]"), ("grid[1]", "[9, 0, 0]"),
                             ("grid[2]", "[9, 0, 0]")],
                            {k: "bad" for k in ("grid[0]", "grid[1]", "grid[2]")},
                            label="after grid[0][0] = 9")],
                     "Writing to one row wrote to all three, because there is "
                     "only one row.",
                     {"objects": 1}))
    out.append(frame(pairs([("grid[0]", "[9, 0, 0]  @0x1f40"),
                            ("grid[1]", "[0, 0, 0]  @0x2b90"),
                            ("grid[2]", "[0, 0, 0]  @0x3c11")],
                           {"grid[0]": "hit"},
                           label="[[0]*3 for _ in range(3)]"),
                     "The comprehension runs [0]*3 three times, so there are "
                     "three objects and the write lands on one of them.",
                     {"objects": 3}))
    return viz(out)


_q(
    slug="the-nested-list-multiplication-bug",
    kind="concept",
    level="Medium",
    title="Why does [[0]*3]*3 break?",
    asked="What does [[0] * 3] * 3 create, and why does writing to one row "
          "change all of them?",
    desc="List multiplication repeats references, not objects - the classic "
         "grid-initialisation bug, and the difference between shallow and deep "
         "copies.",
    lead="Multiplying a list repeats the <strong>reference</strong>, not the "
         "object. <code>[[0]*3]*3</code> builds one inner list and points at it "
         "three times, so writing to one row writes to all of them. Use a "
         "comprehension &mdash; <code>[[0]*3 for _ in range(3)]</code> &mdash; "
         "which evaluates the inner expression once per row.",
    say="\"List multiplication copies references. There's one inner list and "
        "three pointers to it. A comprehension builds a fresh row each time, "
        "which is what you want.\"",
    notice=[
        "All three rows share one address in the broken version.",
        "One write appears in three places &mdash; nothing was copied.",
        "The comprehension produces three distinct objects.",
    ],
    viz=_aliasing_frames(),
    sections=[
        ("What multiplication actually does",
         "<p><code>[x] * 3</code> builds a list holding the same reference three "
         "times. For immutable contents that is invisible &mdash; "
         "<code>[0] * 3</code> is fine, because you can never mutate a "
         "<code>0</code>. For a mutable inner object it is a trap, because all "
         "three names lead to one object.</p>"
         "<p>The tell is that the bug only appears on <em>write</em>. Building "
         "and printing the grid looks perfect; the first assignment to a cell is "
         "when it falls apart.</p>"),
        ("The same idea, three ways",
         "<p>This is one instance of a general rule: assignment and shallow "
         "copies duplicate references, never the objects behind them.</p>"
         "<p><code>b = a</code> &mdash; another name for the same list. "
         "<code>b = a[:]</code> or <code>list(a)</code> or "
         "<code>copy.copy(a)</code> &mdash; a new outer list holding the same "
         "inner references, so nested contents are still shared. "
         "<code>copy.deepcopy(a)</code> &mdash; new objects all the way down, at "
         "the cost of walking the whole structure.</p>"),
        ("How to spot it in review",
         "<p>Any <code>* n</code> where the repeated element is a list, a dict, "
         "a set or a custom object is suspicious. The same rule explains the "
         "mutable default argument bug: <code>def f(acc=[])</code> creates the "
         "list once, when the function is <em>defined</em>, and every call that "
         "omits the argument shares it.</p>"
         "<p>The fix in both cases is the same &mdash; build the mutable thing "
         "at the moment it is needed rather than once, up front.</p>"),
    ],
    code={
        "file": "aliasing.py",
        "intro": "The broken grid and the correct one side by side with their "
                 "row identities printed, then the three levels of copying, then "
                 "the mutable-default-argument bug that has the same cause.",
        "code": '''# Multiplying a list repeats the REFERENCE, not the object.
import copy

wrong = [[0] * 3] * 3
right = [[0] * 3 for _ in range(3)]

print("wrong row ids:", [hex(id(row)) for row in wrong])
print("right row ids:", [hex(id(row)) for row in right])

wrong[0][0] = 9
right[0][0] = 9
print()
print("wrong after grid[0][0] = 9:", wrong, "  <- all three rows")
print("right after grid[0][0] = 9:", right)

# --- assignment, shallow copy, deep copy -------------------------------
original = [[1, 2], [3, 4]]
same = original                      # another NAME for the same list
shallow = original[:]                # new outer list, SAME inner lists
deep = copy.deepcopy(original)       # new objects all the way down

original[0][0] = 99
print()
print("original:", original)
print("same    :", same,    " (is original:", same is original, ")")
print("shallow :", shallow, " <- the nested list was shared")
print("deep    :", deep,    " <- fully independent")

original.append([5, 6])
print()
print("after appending to original:")
print("  shallow:", shallow, "<- the OUTER list was genuinely copied")

# --- the same cause, wearing a different hat ---------------------------
def broken(item, accumulated=[]):     # evaluated ONCE, at definition time
    accumulated.append(item)
    return accumulated


def fixed(item, accumulated=None):
    if accumulated is None:           # a fresh list per call
        accumulated = []
    accumulated.append(item)
    return accumulated


print()
print("broken('a'):", broken("a"))
print("broken('b'):", broken("b"), "<- 'a' is still there")
print("fixed('a') :", fixed("a"))
print("fixed('b') :", fixed("b"))
''',
        "walk": [
            ("[hex(id(row)) for row in wrong]",
             "Three identical addresses. That single line is the whole "
             "explanation, and it is worth printing in an interview rather than "
             "describing."),
            ("[[0] * 3 for _ in range(3)]",
             "The comprehension evaluates <code>[0] * 3</code> once per "
             "iteration, so each row is a separate object. "
             "<code>[0] * 3</code> itself is safe because integers cannot be "
             "mutated."),
            ("shallow = original[:]",
             "A new outer list holding the <em>same</em> inner references. "
             "Appending to <code>original</code> does not affect it; mutating a "
             "nested list does. Both behaviours are shown."),
            ("def broken(item, accumulated=[])",
             "The default is evaluated once, when the function is defined, so "
             "every call that omits the argument shares one list. Same cause: a "
             "mutable object created once and referenced many times."),
        ],
        "try": [
            "Build the grid with <code>[[0] * 3] * 3</code> and only ever read "
            "from it. It looks completely correct &mdash; the bug needs a write.",
            "Replace <code>deepcopy</code> with <code>copy.copy</code> and "
            "re-run. The nested mutation reappears, which is the difference "
            "between the two in one line.",
        ],
    },
    check=[
        {"q": "[[0] * 3] * 3 creates:",
         "options": ["Three independent rows", "One row, referenced three times",
                     "A 3x3 tuple", "An error"],
         "answer": 1,
         "why": "Multiplication repeats the reference. Writing through any of "
                "the three names is writing to the one object."},
        {"q": "a[:] on a list of lists gives you:",
         "options": ["A full independent copy", "A new outer list holding the "
                     "same inner lists",
                     "The same object", "A tuple"],
         "answer": 1,
         "why": "That is a shallow copy. Nested mutation is still shared; only "
                "copy.deepcopy duplicates all the way down."},
        {"q": "def f(x, acc=[]) misbehaves because the default is evaluated:",
         "options": ["On every call", "Once, when the function is defined",
                     "Only on the first call that omits it", "Never"],
         "answer": 1,
         "why": "One list is created at definition time and shared by every call "
                "that omits the argument. Use None and build inside the function."},
    ],
)


def _membership_frames():
    values = [17, 4, 92, 8, 55, 23, 71, 3]
    out = linear_scan(values, 3, label="list: scan until found")
    out.append(frame(pairs([("hash(3)", "-> slot 5"),
                            ("slot 5 holds", "3"),
                            ("comparisons", "1")],
                           {"comparisons": "hit"}, label="set: compute the slot"),
                     "The set does not scan. It computes where 3 would be and "
                     "looks there - one probe, whatever the size.",
                     {"index": 5, "comparisons": 1}))
    return viz(out)


_q(
    slug="why-is-in-slow-on-a-list",
    kind="concept",
    level="Easy",
    title="Why is `in` slow on a list but fast on a set?",
    asked="What is the complexity of `x in my_list`, and how do you make it "
          "faster?",
    desc="Membership testing is O(n) on a list and O(1) on a set or dict - the "
         "single highest-value one-line optimisation in everyday Python.",
    lead="<code>x in list</code> compares against each element until it finds "
         "one, so it is <strong>O(n)</strong> &mdash; and a miss always costs "
         "the full length. <code>x in set</code> computes where the value would "
         "be and looks there: <strong>O(1)</strong>. Swapping one for the other "
         "is usually a one-character change with a thousandfold effect.",
    say="\"`in` on a list is a linear scan, O(n). On a set or dict it's a hash "
        "lookup, O(1). If I'm testing membership repeatedly I build a set "
        "first - that's O(n) once instead of O(n) every time.\"",
    notice=[
        "The list compares one element at a time and stops at the hit.",
        "A <em>miss</em> checks all of them &mdash; the worst case is the common "
        "case.",
        "The set makes one probe regardless of size.",
    ],
    viz=_membership_frames(),
    sections=[
        ("The two mechanisms",
         "<p>A list has no idea where anything is, so <code>in</code> walks it "
         "comparing element by element. Best case one comparison, worst case n, "
         "and a value that is absent always costs n.</p>"
         "<p>A set stores values in slots chosen from their hashes. "
         "<code>in</code> hashes the value, goes to that slot and compares. The "
         "length of the set does not enter into it &mdash; see "
         "<a href=\"../dsa/hash_tables.html\">hash tables</a> for the "
         "machinery.</p>"),
        ("The shape that turns quadratic",
         "<p>The damage is rarely a single lookup. It is a lookup inside a "
         "loop:</p>"
         "<p><code>for x in candidates: if x in seen_list: ...</code></p>"
         "<p>That is O(n&middot;m). Building a set from <code>seen_list</code> "
         "once, before the loop, makes it O(n + m). This is the most common "
         "accidental quadratic in Python after <code>pop(0)</code>, and it is "
         "invisible in testing because small inputs are fast either way.</p>"),
        ("When a list is still right",
         "<p>Building the set costs O(n) and some memory, so for a single "
         "membership test on a small list it is not worth it. The rule of thumb: "
         "if you will test more than a couple of times, or the collection is "
         "large, convert.</p>"
         "<p>Sets also require hashable elements and lose ordering and "
         "duplicates. If you need order, a dict works as an ordered set since "
         "3.7 &mdash; and <code>dict.fromkeys(seq)</code> deduplicates while "
         "preserving order in one line.</p>"),
    ],
    code={
        "file": "membership.py",
        "intro": "The same membership tests against a list and a set at two "
                 "sizes, then the loop that turns the difference from a curiosity "
                 "into a quadratic.",
        "code": '''# `in` on a list scans. `in` on a set computes. That is the whole story.
import time

for n in (50_000, 500_000):
    as_list = list(range(n))
    as_set = set(as_list)
    probes = [0, n // 2, n - 1, -1]        # first, middle, last, missing

    print(f"n = {n:,}")
    for label, container in (("list", as_list), ("set ", as_set)):
        start = time.time()
        for _ in range(5):
            for p in probes:
                p in container
        print(f"  {label}: {time.time() - start:.4f}s")

# --- where it actually bites -------------------------------------------
haystack = list(range(4_000))
needles = list(range(0, 8_000, 2))

start = time.time()
found = [x for x in needles if x in haystack]          # O(n * m)
slow = time.time() - start

start = time.time()
lookup = set(haystack)                                 # O(n), once
found2 = [x for x in needles if x in lookup]           # O(m)
fast = time.time() - start

print()
print(f"{len(needles):,} lookups against a {len(haystack):,}-item list:")
print(f"  list  : {slow:.4f}s")
print(f"  set   : {fast:.4f}s   ({slow / fast:.0f}x faster)")
print(f"  same answer: {found == found2}")

# --- a set loses order and duplicates; a dict keeps order --------------
items = ["b", "a", "b", "c", "a"]
print()
print("original          :", items)
print("set(items)        :", sorted(set(items)), "- order gone")
print("dict.fromkeys(...):", list(dict.fromkeys(items)), "- deduped, order kept")
''',
        "walk": [
            ("p in as_list",
             "A comparison per element until it matches. The probe for "
             "<code>-1</code> is the worst case and the one that shows the real "
             "cost, because nothing stops it early."),
            ("p in as_set",
             "Hash, jump to the slot, compare. The timings barely move when n "
             "goes up tenfold, which is what O(1) looks like from outside."),
            ("lookup = set(haystack)",
             "Built once, outside the loop. That converts O(n&middot;m) into "
             "O(n + m) and is usually the entire fix."),
            ("dict.fromkeys(items)",
             "Deduplicates while preserving order, because dicts have kept "
             "insertion order since 3.7. A set would lose it."),
        ],
        "try": [
            "Move <code>set(haystack)</code> inside the comprehension. Rebuilding "
            "it per element is worse than the list version &mdash; the point is "
            "building it <em>once</em>.",
            "Try <code>x in some_tuple</code>. Tuples are also linear; "
            "immutability does not buy a faster search.",
        ],
    },
    check=[
        {"q": "x in my_list has complexity:",
         "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
         "answer": 1,
         "why": "A list has no index of its contents, so membership is a linear "
                "scan. A miss always costs the full length."},
        {"q": "Testing membership repeatedly against a large list is best fixed "
              "by:",
         "options": ["Sorting the list first", "Building a set once, before the "
                     "loop",
                     "Using a tuple", "Using enumerate"],
         "answer": 1,
         "why": "O(n) once plus O(1) per lookup, instead of O(n) per lookup. "
                "Building it inside the loop would be worse than not bothering."},
        {"q": "Which deduplicates a list while preserving order?",
         "options": ["set(items)", "list(dict.fromkeys(items))", "sorted(set(items))",
                     "items.unique()"],
         "answer": 1,
         "why": "Dicts have preserved insertion order since 3.7, so their keys "
                "act as an ordered set. A set makes no ordering promise."},
    ],
)


# =========================================================================
# Coding problems
# =========================================================================

def _two_sum_frames():
    values = [2, 7, 11, 15, 3]
    target = 18
    out = []
    seen = {}
    for i, v in enumerate(values):
        need = target - v
        found = need in seen
        marks = {j: ("done" if j < i else "dim") for j in range(len(values))}
        marks[i] = "hit" if found else "lo"
        if found:
            marks[seen[need]] = "hit"
        out.append(frame([marked(values, marks, {i: "i"}, label="values"),
                          pairs(sorted((str(k), str(v2)) for k, v2 in seen.items())
                                or [("(empty)", "-")],
                                {str(need): "hit"} if found else {},
                                label="value -> index seen so far")],
                         "Need %d to reach %d. %s"
                         % (need, target,
                            "Already seen at index %d - done." % seen[need] if found
                            else "Not seen yet, so remember %d -> %d." % (v, i)),
                         {"i": i, "need": need, "stored": len(seen)}))
        if found:
            break
        seen[v] = i
    return viz(out)


_q(
    slug="two-sum",
    kind="coding",
    level="Easy",
    title="Two Sum",
    asked="Find two numbers in a list that add to a target. Return their indices.",
    desc="Two Sum in one pass with a dictionary: why the complement lookup beats "
         "nested loops, and when the sorted two-pointer version is the right "
         "answer instead.",
    lead="One pass with a <strong>dictionary</strong>. For each value, ask "
         "whether its complement <code>target - value</code> has already been "
         "seen; if it has, you have the pair. O(n) time and O(n) space, against "
         "O(n&sup2;) for the nested loops everyone writes first.",
    say="\"One pass with a dict of value to index. For each number I look up "
        "target minus it - if it's there, that's the pair. O(n) time, O(n) "
        "space. If the array were sorted I'd use two pointers instead and drop "
        "the space to O(1).\"",
    notice=[
        "The dictionary only holds values <em>already passed</em>.",
        "Storing after the check is what stops an element pairing with itself.",
        "The answer is found without ever comparing two elements directly.",
    ],
    viz=_two_sum_frames(),
    sections=[
        ("Turning a search into a lookup",
         "<p>The nested-loop version asks \"does any later element pair with "
         "this one?\", which is n&sup2;/2 comparisons. The insight is to invert "
         "it: you know exactly which number you need, so the question becomes "
         "\"have I already seen <code>target - value</code>?\" &mdash; and that "
         "is a dictionary lookup, not a search.</p>"
         "<p>This is the same move as grouping anagrams by a key. Whenever a "
         "problem asks you to find a pair with a known relationship, look for "
         "the version where one member is computed rather than searched for.</p>"),
        ("The two orderings that matter",
         "<p>Check <em>before</em> you store. Storing first lets an element pair "
         "with itself when <code>target</code> is exactly twice it &mdash; "
         "<code>[3]</code> with target 6 returns <code>(0, 0)</code>, which is "
         "wrong.</p>"
         "<p>Store <code>value &rarr; index</code>, not the reverse. The values "
         "are what you look up; the indices are what you return. Duplicates "
         "overwrite, which is fine because any one valid pair is usually "
         "acceptable &mdash; ask, if the question does not say.</p>"),
        ("When to use two pointers instead",
         "<p>If the input is already sorted, converging pointers solve it in "
         "O(n) time and <strong>O(1)</strong> space: too small means move the "
         "left pointer right, too big means move the right pointer left. That is "
         "strictly better on memory.</p>"
         "<p>If it is not sorted, sorting to enable that is O(n&nbsp;log&nbsp;n) "
         "&mdash; worse than the dictionary, and it destroys the original "
         "indices, which the question usually asks for. Say why you are choosing "
         "the dictionary; that reasoning is most of the mark.</p>"),
    ],
    code={
        "file": "two_sum.py",
        "intro": "All three approaches with their operation counts, then the "
                 "self-pairing bug demonstrated by moving one line, and finally "
                 "a size where the quadratic version stops being viable.",
        "code": '''# Two Sum: turn "search for a partner" into "look up a complement".
import time

def brute_force(values, target):
    checks = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            checks += 1
            if values[i] + values[j] == target:
                return (i, j), checks
    return None, checks


def one_pass(values, target):
    seen = {}                                  # value -> index
    checks = 0
    for i, v in enumerate(values):
        checks += 1
        if target - v in seen:                 # CHECK before you store
            return (seen[target - v], i), checks
        seen[v] = i
    return None, checks


def two_pointers(sorted_values, target):
    """O(1) space - but only valid if the input is sorted."""
    lo, hi, checks = 0, len(sorted_values) - 1, 0
    while lo < hi:
        checks += 1
        total = sorted_values[lo] + sorted_values[hi]
        if total == target:
            return (lo, hi), checks
        if total < target:
            lo += 1
        else:
            hi -= 1
    return None, checks


values, target = [2, 7, 11, 15, 3], 18
print("values:", values, " target:", target)
for name, fn in (("brute force", brute_force), ("one pass  ", one_pass)):
    pair, checks = fn(values, target)
    print(f"  {name}: {pair}  ({checks} checks)")

pair, checks = two_pointers(sorted(values), target)
print(f"  two pointers (on the SORTED copy): {pair}  ({checks} checks)")
print("  note the indices refer to the sorted list, not the original")

# --- the ordering bug --------------------------------------------------
def store_first(values, target):
    seen = {}
    for i, v in enumerate(values):
        seen[v] = i                            # stored BEFORE the check
        if target - v in seen:
            return (seen[target - v], i)
    return None

print()
print("[3] with target 6:")
print("  check first:", one_pass([3], 6)[0], "  <- correct: no pair exists")
print("  store first:", store_first([3], 6), "  <- WRONG: 3 paired with itself")

# --- where the quadratic stops being viable ----------------------------
big = list(range(1_800))
print()
for name, fn in (("brute force", brute_force), ("one pass", one_pass)):
    start = time.time()
    _, checks = fn(big, 3_597)                 # a pair near the very end
    print(f"  {name:>11} on {len(big):,} items: {checks:>12,} checks "
          f"in {time.time() - start:.3f}s")
''',
        "walk": [
            ("if target - v in seen:",
             "The complement is computed, not searched for. That single "
             "substitution is what removes the inner loop and the "
             "O(n&sup2;)."),
            ("seen[v] = i   # after the check",
             "Order is load-bearing. Storing first lets a value pair with "
             "itself when the target is double it, which the "
             "<code>[3]</code> case demonstrates."),
            ("seen: value -> index",
             "Values are what you look up; indices are what you return. Getting "
             "this backwards produces a dictionary you cannot query."),
            ("two_pointers(sorted(values), target)",
             "O(1) space, and the indices now refer to the sorted copy. That is "
             "why sorting is the wrong move when the question asks for original "
             "indices."),
        ],
        "try": [
            "Ask for <em>all</em> pairs rather than the first. Store a list of "
            "indices per value, because duplicates currently overwrite.",
            "Extend it to 3Sum: fix one element, then two-pointer the rest. "
            "O(n&sup2;) instead of O(n&sup3;), and the standard follow-up.",
        ],
    },
    check=[
        {"q": "The one-pass solution works by:",
         "options": ["Sorting first", "Looking up the complement target - value "
                     "in a dictionary",
                     "Comparing every pair", "Using binary search"],
         "answer": 1,
         "why": "You know exactly which number you need, so it becomes a lookup "
                "rather than a search. That removes the inner loop."},
        {"q": "Why must you check before storing the current value?",
         "options": ["For speed", "Otherwise an element can pair with itself "
                     "when the target is double it",
                     "Dictionaries reject duplicates", "It does not matter"],
         "answer": 1,
         "why": "[3] with target 6 returns (0, 0) if you store first - a pair "
                "that does not exist."},
        {"q": "When is the two-pointer version preferable to the dictionary?",
         "options": ["Always", "When the input is already sorted and O(1) space "
                     "matters",
                     "When there are duplicates", "When the list is short"],
         "answer": 1,
         "why": "It needs no extra memory, but sorting just to enable it costs "
                "O(n log n) and destroys the original indices the question wants."},
    ],
)


def _kadane_frames():
    values = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    out = []
    best = current = values[0]
    start = end = best_start = 0
    for i in range(1, len(values)):
        v = values[i]
        if current + v < v:
            current, start = v, i
        else:
            current += v
        if current > best:
            best, best_start, end = current, start, i
        marks = {j: ("hit" if best_start <= j <= end else
                     "lo" if start <= j <= i else "dim")
                 for j in range(len(values))}
        out.append(frame(marked(values, marks, {i: "i"}, label="values"),
                         "current run = %d, best so far = %d (%s)."
                         % (current, best, values[best_start:end + 1]),
                         {"current": current, "best": best}))
    out.append(frame(marked(values, {j: ("hit" if best_start <= j <= end else "dim")
                                     for j in range(len(values))},
                            label="values"),
                     "Best subarray %s sums to %d. One pass, two variables, "
                     "nothing stored." % (values[best_start:end + 1], best),
                     {"current": current, "best": best}))
    return viz(out)


_q(
    slug="maximum-subarray-kadane",
    kind="coding",
    level="Medium",
    title="Maximum subarray sum (Kadane)",
    asked="Find the contiguous subarray with the largest sum.",
    desc="Kadane's algorithm in one pass: the single decision at each element, "
         "why it is dynamic programming, and the all-negative edge case.",
    lead="At each element, one decision: <strong>extend</strong> the run you are "
         "on, or <strong>start again</strong> from here. Take whichever gives "
         "the larger sum, and track the best seen. One pass, two variables, "
         "O(n) time and O(1) space.",
    say="\"Kadane. At each element I either extend the current run or start "
        "fresh from that element, whichever is bigger, and I keep the best I've "
        "seen. O(n) time, O(1) space - and I initialise from the first element, "
        "not zero, so all-negative input works.\"",
    notice=[
        "The lighter band is the current run; the solid one is the best so far.",
        "A run restarts whenever carrying the previous sum would hurt.",
        "The best is only updated &mdash; never reduced.",
    ],
    viz=_kadane_frames(),
    sections=[
        ("The one decision",
         "<p>At element <em>i</em> there are exactly two candidates for the best "
         "subarray ending there: the previous best-ending-here extended by "
         "<code>values[i]</code>, or <code>values[i]</code> alone. Take the "
         "larger. Then the global answer is the largest of those per-element "
         "bests.</p>"
         "<p>That is dynamic programming with the table collapsed to a single "
         "variable, because each step only needs the one before it. Saying that "
         "out loud is worth more than the code.</p>"),
        ("The edge case that catches people",
         "<p>Initialise <code>best</code> and <code>current</code> to "
         "<code>values[0]</code>, not to <code>0</code>. Starting at zero means "
         "an all-negative array returns <code>0</code> &mdash; a sum from the "
         "empty subarray, which is usually not allowed.</p>"
         "<p>Ask whether the empty subarray counts. If it does, zero is the "
         "right floor; if not, the first element is. Getting this wrong is the "
         "most common failure on this question, and asking about it is a "
         "positive signal.</p>"),
        ("Returning the indices",
         "<p>The usual follow-up. Track where the current run started, and when "
         "you beat the best, record that start and the current index. Two extra "
         "variables and no change to the complexity &mdash; but you must update "
         "<code>start</code> at the moment you restart, not when you improve.</p>"
         "<p>The other follow-up is divide and conquer: split, solve both halves, "
         "and handle the crossing case separately. O(n&nbsp;log&nbsp;n), worse "
         "than Kadane, and worth knowing because it is the classic example of "
         "the crossing-subproblem pattern.</p>"),
    ],
    code={
        "file": "kadane.py",
        "intro": "Kadane with the running values printed at each element, then "
                 "the index-tracking version, then the zero-initialised variant "
                 "getting an all-negative array wrong.",
        "code": '''# Kadane: extend the current run, or start again from here.

def kadane(values, show=False):
    best = current = values[0]            # NOT zero - see the last section
    for v in values[1:]:
        current = max(v, current + v)     # start fresh, or extend
        best = max(best, current)
        if show:
            print(f"  saw {v:>3}: current={current:>4} best={best:>4}")
    return best


def kadane_with_indices(values):
    best = current = values[0]
    start = best_start = best_end = 0
    for i in range(1, len(values)):
        if current + values[i] < values[i]:
            current, start = values[i], i     # restart: record the new start
        else:
            current += values[i]
        if current > best:                    # improve: record the span
            best, best_start, best_end = current, start, i
    return best, (best_start, best_end)


def kadane_from_zero(values):
    """The version that assumes an empty subarray is allowed."""
    best = current = 0
    for v in values:
        current = max(0, current + v)
        best = max(best, current)
    return best


values = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print("values:", values)
print("max subarray sum:", kadane(values, show=True))

total, (i, j) = kadane_with_indices(values)
print()
print(f"span: indices {i}..{j} = {values[i:j+1]} summing to {total}")

# --- the all-negative case ---------------------------------------------
print()
for sample in ([-3, -1, -7], [-5], [1, 2, 3]):
    proper = kadane(sample)
    from_zero = kadane_from_zero(sample)
    flag = "   <-- 0 is the EMPTY subarray" if proper != from_zero else ""
    print(f"  {str(sample):>14}: kadane={proper:>3}  from-zero={from_zero:>3}{flag}")

print()
print("Ask whether the empty subarray counts. If it does not, initialise")
print("from values[0]; if it does, zero is the right floor.")
''',
        "walk": [
            ("current = max(v, current + v)",
             "The whole algorithm. Either the run continues or it restarts here, "
             "and nothing else is ever a candidate for the best subarray ending "
             "at this element."),
            ("best = max(best, current)",
             "Kept separately, because the best run may have ended several "
             "elements ago. Collapsing these two variables into one is the most "
             "common way to break it."),
            ("best = current = values[0]",
             "Not zero. Starting at zero silently allows the empty subarray, so "
             "an all-negative array returns 0 instead of its least-negative "
             "element."),
            ("current, start = values[i], i",
             "The index version must record the new start at the moment of the "
             "restart, not when the best improves &mdash; by then the "
             "information is gone."),
        ],
        "try": [
            "Run <code>[-3, -1, -7]</code> through both versions. The difference "
            "is entirely the empty-subarray question.",
            "Return the subarray rather than the sum, then check it against "
            "<code>max</code> over every slice on a small input.",
        ],
    },
    check=[
        {"q": "At each element, Kadane chooses between:",
         "options": ["Sorting or not", "Extending the current run or starting "
                     "fresh from this element",
                     "Left half or right half", "Adding or multiplying"],
         "answer": 1,
         "why": "Only those two can be the best subarray ending here. It is "
                "dynamic programming with the table reduced to one variable."},
        {"q": "Initialising best to 0 rather than values[0] breaks:",
         "options": ["Long arrays", "An all-negative array, which returns 0 - "
                     "the empty subarray",
                     "Arrays with duplicates", "Nothing"],
         "answer": 1,
         "why": "Zero is only reachable by choosing nothing at all. Ask whether "
                "the empty subarray is allowed before you commit."},
        {"q": "The space complexity of Kadane is:",
         "options": ["O(n)", "O(1)", "O(log n)", "O(n²)"],
         "answer": 1,
         "why": "Two running values and nothing else. The DP table collapses "
                "because each step depends only on the previous one."},
    ],
)


def _dedupe_frames():
    values = [1, 1, 2, 2, 2, 3, 4, 4, 5]
    out = []
    write = 1
    for read in range(1, len(values)):
        keep = values[read] != values[write - 1]
        if keep:
            values[write] = values[read]
            write += 1
        marks = {j: ("done" if j < write else "dim") for j in range(len(values))}
        marks[read] = "hit" if keep else "bad"
        out.append(frame(marked(list(values), marks,
                                {write - 1: "write", read: "read"}, label="array"),
                         "%s at read=%d: %s" % (values[read], read,
                                                "new, so copy it back to write=%d"
                                                % (write - 1) if keep
                                                else "same as the last kept - skip"),
                         {"read": read, "write": write}))
    out.append(frame(marked(list(values),
                            {j: ("done" if j < write else "bad")
                             for j in range(len(values))}, label="array"),
                     "First %d entries are the answer; the tail is stale data. "
                     "Nothing was allocated." % write,
                     {"read": len(values) - 1, "write": write}))
    return viz(out)


_q(
    slug="remove-duplicates-in-place",
    kind="coding",
    level="Easy",
    title="Remove duplicates from a sorted array in place",
    asked="Remove duplicates from a sorted array in place and return the new "
          "length.",
    desc="The read/write two-pointer pattern: O(1) extra space, why the function "
         "returns a length rather than a list, and what the leftover tail means.",
    lead="Two pointers moving the same way. <strong>Read</strong> scans every "
         "element; <strong>write</strong> marks the end of the kept prefix. When "
         "read finds something new, copy it back to write and advance. O(n) time, "
         "O(1) extra space &mdash; and the function returns a <em>length</em>, "
         "because nothing was reallocated.",
    say="\"Fast and slow pointers. Read scans, write marks the end of the deduped "
        "prefix, and I copy back only when the value differs from the last kept "
        "one. O(n) time, O(1) space, and I return the length because the tail is "
        "stale.\"",
    notice=[
        "<code>write</code> only advances on a genuinely new value.",
        "The comparison is against the last <em>kept</em> element, not the "
        "previous one read.",
        "The tail is left as stale data &mdash; that is why a length is returned.",
    ],
    viz=_dedupe_frames(),
    sections=[
        ("Why sorted matters",
         "<p>Duplicates in a sorted array are adjacent, so \"have I seen this "
         "before?\" collapses to \"is it the same as the last one I kept?\" "
         "&mdash; one comparison, no set, no memory.</p>"
         "<p>On unsorted input this does not work and you need a set, which "
         "costs O(n) space, or a sort first, which costs O(n&nbsp;log&nbsp;n) "
         "time. Say which assumption you are relying on.</p>"),
        ("The read/write pattern",
         "<p><code>read</code> visits every element exactly once. "
         "<code>write</code> lags behind, marking where the next kept element "
         "goes. Because <code>write</code> never overtakes <code>read</code>, "
         "the copy can never clobber something not yet examined &mdash; which is "
         "what makes in-place safe.</p>"
         "<p>Compare against <code>values[write - 1]</code>, the last element "
         "actually kept, not <code>values[read - 1]</code>. On a long run of "
         "duplicates those differ, and the second is wrong.</p>"),
        ("Why it returns a length",
         "<p>Nothing is reallocated, so the array keeps its original size and "
         "everything past <code>write</code> is leftover data. The caller uses "
         "<code>values[:n]</code>. This is the C-style convention the question "
         "comes from, and returning a new list instead would defeat the O(1) "
         "space requirement the question exists to test.</p>"
         "<p>The same pattern solves \"move zeroes to the end\", \"remove all "
         "instances of a value\", and \"allow at most two duplicates\" &mdash; "
         "only the keep condition changes.</p>"),
    ],
    code={
        "file": "dedupe.py",
        "intro": "The two-pointer version with the array printed after each "
                 "write, the same pattern applied to two sibling problems, and "
                 "the off-by-one comparison that looks right and is not.",
        "code": '''# Remove duplicates in place: read scans, write keeps.

def dedupe(values):
    if not values:
        return 0
    write = 1                                  # values[0] is always kept
    for read in range(1, len(values)):
        if values[read] != values[write - 1]:  # against the last KEPT value
            values[write] = values[read]
            write += 1
    return write


values = [1, 1, 2, 2, 2, 3, 4, 4, 5]
original = list(values)
n = dedupe(values)
print("original :", original)
print("deduped  :", values[:n], f"(length {n})")
print("full array:", values, "<- the tail is stale, which is why n is returned")

# --- the comparison people get wrong -----------------------------------
def dedupe_wrong(values):
    if not values:
        return 0
    write = 1
    for read in range(1, len(values)):
        if values[read] != values[read - 1]:   # against the previous READ
            values[write] = values[read]
            write += 1
    return write

print()
for sample in ([1, 1, 2, 2, 2, 3], [1, 2, 2, 3], [5, 5, 5, 5]):
    a, b = list(sample), list(sample)
    na, nb = dedupe(a), dedupe_wrong(b)
    flag = "" if a[:na] == b[:nb] else "   <-- differ"
    print(f"  {str(sample):>18}: correct={a[:na]} other={b[:nb]}{flag}")
print("On sorted input both happen to agree - the difference shows up when")
print("the same pattern is reused on problems where runs are not adjacent.")

# --- the same pattern, two siblings ------------------------------------
def move_zeroes(values):
    write = 0
    for read in range(len(values)):
        if values[read] != 0:
            values[write], values[read] = values[read], values[write]
            write += 1
    return values


def at_most_two(values):
    write = 0
    for v in values:
        if write < 2 or v != values[write - 2]:
            values[write] = v
            write += 1
    return write

print()
print("move zeroes  :", move_zeroes([0, 1, 0, 3, 12]))
dupes = [1, 1, 1, 2, 2, 3]
k = at_most_two(dupes)
print("at most two  :", dupes[:k], "from [1, 1, 1, 2, 2, 3]")
print("Only the keep condition changed.")
''',
        "walk": [
            ("values[read] != values[write - 1]",
             "Compare with the last element actually <em>kept</em>. Using "
             "<code>values[read - 1]</code> instead happens to agree on sorted "
             "input and is the wrong invariant to carry into the variants."),
            ("write += 1 only on a keep",
             "<code>write</code> is the length of the answer so far, which is "
             "why returning it at the end needs no separate counter."),
            ("write never overtakes read",
             "The safety argument for writing into the array you are reading. "
             "Every slot written has already been consumed."),
            ("if write < 2 or v != values[write - 2]:",
             "The at-most-two variant. Same skeleton, one different condition "
             "&mdash; which is what makes this pattern worth recognising rather "
             "than memorising."),
        ],
        "try": [
            "Print the whole array rather than <code>values[:n]</code>. The "
            "stale tail is exactly why the function cannot just return the "
            "array.",
            "Adapt it to remove every instance of a given value. One condition "
            "changes and nothing else does.",
        ],
    },
    check=[
        {"q": "Why does the function return a length rather than a list?",
         "options": ["Lists are slow", "Nothing was reallocated, so the tail "
                     "still holds stale data",
                     "To save memory", "It returns both"],
         "answer": 1,
         "why": "The point of the question is O(1) extra space. Building a new "
                "list would defeat it."},
        {"q": "The current element is compared against:",
         "options": ["values[read - 1]", "values[write - 1], the last element "
                     "kept",
                     "values[0]", "The next element"],
         "answer": 1,
         "why": "The last kept value is the invariant. The other comparison "
                "agrees on sorted input and is the wrong idea to carry forward."},
        {"q": "Writing into the array while reading it is safe because:",
         "options": ["The array is copied", "write never overtakes read, so only "
                     "already-consumed slots are overwritten",
                     "The array is sorted", "Python protects it"],
         "answer": 1,
         "why": "write lags behind by exactly the number of duplicates skipped, "
                "so it can never clobber unread input."},
    ],
)


def _rotate_frames():
    values = [1, 2, 3, 4, 5, 6, 7]
    k = 3
    out = [frame(marked(values, {j: "dim" for j in range(len(values))},
                        label="original"),
                 "Rotate right by %d. The last %d elements should end up at the "
                 "front." % (k, k),
                 {"k": k, "reversals": 0})]

    def rev(a, lo, hi):
        while lo < hi:
            a[lo], a[hi] = a[hi], a[lo]
            lo, hi = lo + 1, hi - 1

    a = list(values)
    rev(a, 0, len(a) - 1)
    out.append(frame(marked(list(a), {j: "lo" for j in range(len(a))},
                            label="reverse everything"),
                     "Reverse the whole array. The right elements are at the "
                     "front now, but each block is backwards.",
                     {"k": k, "reversals": 1}))
    rev(a, 0, k - 1)
    out.append(frame(marked(list(a), {j: "hit" for j in range(k)},
                            label="reverse the first k"),
                     "Reverse the first %d. That block is now correct." % k,
                     {"k": k, "reversals": 2}))
    rev(a, k, len(a) - 1)
    out.append(frame(marked(list(a), {j: "done" for j in range(len(a))},
                            label="reverse the rest"),
                     "Reverse the remainder. Three reversals, no extra array, "
                     "and every element moved exactly twice.",
                     {"k": k, "reversals": 3}))
    return viz(out)


_q(
    slug="rotate-an-array",
    kind="coding",
    level="Medium",
    title="Rotate an array by k",
    asked="Rotate an array right by k positions, in place.",
    desc="The three-reversal rotation trick: O(1) extra space, why k must be "
         "taken modulo n, and the slice version that costs O(n) memory.",
    lead="Reverse the whole array, then reverse the first k, then reverse the "
         "rest. Three passes, every element moved exactly twice, "
         "<strong>O(1) extra space</strong>. The slice version "
         "<code>a[-k:] + a[:-k]</code> is one line and allocates a second array.",
    say="\"Three reversals: whole thing, first k, then the rest. O(n) time, O(1) "
        "space. And k needs to be k % n first, or a k larger than the array "
        "breaks it.\"",
    notice=[
        "After the first reversal the blocks are in the right places, backwards.",
        "Each subsequent reversal fixes one block.",
        "Nothing is allocated &mdash; every step is in-place swapping.",
    ],
    viz=_rotate_frames(),
    sections=[
        ("Why three reversals work",
         "<p>A right rotation by k moves the last k elements to the front and "
         "slides the rest along. Reversing the whole array puts those k at the "
         "front immediately &mdash; but reversed, and the other block reversed "
         "too. Reversing each block separately undoes exactly that.</p>"
         "<p>Total work is 3&middot;n/2 swaps, so O(n) time, and the only "
         "storage is a couple of indices.</p>"),
        ("The modulo, and the empty case",
         "<p><code>k %= n</code> first. A k larger than the array is a rotation "
         "of <code>k % n</code>, and without the modulo the block boundaries go "
         "out of range. A k that is a multiple of n leaves the array unchanged, "
         "which the modulo also handles for free.</p>"
         "<p>Negative k is a left rotation. Python's <code>%</code> already "
         "returns a non-negative result for a positive divisor, so "
         "<code>k %= n</code> converts it correctly &mdash; a detail worth "
         "mentioning because it differs from C.</p>"),
        ("The alternatives",
         "<p><strong>Slicing.</strong> <code>a[-k:] + a[:-k]</code> is the "
         "Pythonic answer, obviously correct, and O(n) extra memory. Give it "
         "first, then offer the in-place version.</p>"
         "<p><strong>Cyclic replacement.</strong> Follow the cycle of positions, "
         "moving each element directly to its destination. It moves every "
         "element exactly once rather than twice, but the number of cycles is "
         "gcd(n, k), so it needs an outer loop and is much easier to get "
         "wrong.</p>"),
    ],
    code={
        "file": "rotate.py",
        "intro": "The three-reversal rotation printed after each step, checked "
                 "against the slice version for every k from 0 to n, including "
                 "the values larger than the array.",
        "code": '''# Rotate right by k: reverse everything, then reverse each block.

def reverse(a, lo, hi):
    while lo < hi:
        a[lo], a[hi] = a[hi], a[lo]
        lo, hi = lo + 1, hi - 1


def rotate(a, k, show=False):
    n = len(a)
    if n == 0:
        return a
    k %= n                       # a k bigger than the array is k % n
    reverse(a, 0, n - 1)
    if show:
        print("  reverse all      :", a)
    reverse(a, 0, k - 1)
    if show:
        print("  reverse first k  :", a)
    reverse(a, k, n - 1)
    if show:
        print("  reverse the rest :", a)
    return a


def rotate_by_slicing(a, k):
    """One line, obviously correct, and O(n) extra memory."""
    if not a:
        return a
    k %= len(a)
    return a[-k:] + a[:-k] if k else a[:]


values = [1, 2, 3, 4, 5, 6, 7]
print("original:", values, " k = 3")
print("in place:", rotate(list(values), 3, show=True))

# Check the in-place version against the obvious one for every k.
print()
print("agreement across k = 0 .. 2n:")
for k in range(0, 2 * len(values) + 1):
    a, b = list(values), list(values)
    same = rotate(a, k) == rotate_by_slicing(b, k)
    print(f"  k={k:>2}: {rotate(list(values), k)}  matches slicing: {same}")

# --- what happens without the modulo -----------------------------------
def rotate_no_modulo(a, k):
    n = len(a)
    reverse(a, 0, n - 1)
    reverse(a, 0, k - 1)
    reverse(a, k, n - 1)
    return a

print()
print("k = 10 on a 7-element array:")
print("  with modulo   :", rotate(list(values), 10))
try:
    print("  without modulo:", rotate_no_modulo(list(values), 10))
except IndexError as e:
    print("  without modulo: IndexError -", e)
print("It does not return a wrong answer; it walks off the end of the array.")
''',
        "walk": [
            ("k %= n",
             "The first line, and the one that is usually missing. A k larger "
             "than the array sends <code>reverse</code> an out-of-range bound "
             "&mdash; it raises rather than returning something wrong, which the "
             "last block demonstrates."),
            ("reverse(a, 0, n - 1)",
             "Puts the last k elements at the front in one pass &mdash; "
             "backwards, along with everything else, which the next two "
             "reversals correct."),
            ("reverse(a, 0, k - 1) then reverse(a, k, n - 1)",
             "Each fixes one block. The boundary is exactly k, which is why the "
             "modulo has to happen before any of this."),
            ("a[-k:] + a[:-k]",
             "The version to offer first. It is correct and readable, and it "
             "allocates a whole second array &mdash; which is the requirement "
             "the question is really about."),
        ],
        "try": [
            "Pass a negative k. Python's <code>%</code> turns it into the "
            "equivalent left rotation for free, unlike C.",
            "Implement the cyclic-replacement version. Every element moves once "
            "instead of twice, and you need gcd(n, k) starting points.",
        ],
    },
    check=[
        {"q": "The three-reversal rotation uses how much extra space?",
         "options": ["O(n)", "O(1)", "O(k)", "O(log n)"],
         "answer": 1,
         "why": "Only a couple of index variables. The slice version allocates a "
                "whole second array."},
        {"q": "Why is `k %= n` needed before the reversals?",
         "options": ["To handle negatives only", "A k larger than the array puts "
                     "the block boundary out of range",
                     "To make it faster", "It is not needed"],
         "answer": 1,
         "why": "Rotating by k and by k % n are the same operation, and without "
                "the modulo the second reversal is given invalid bounds."},
        {"q": "After reversing the whole array, why reverse each block again?",
         "options": ["To undo the rotation", "The blocks are in the right places "
                     "but internally backwards",
                     "To sort them", "To save memory"],
         "answer": 1,
         "why": "One reversal gets the two groups to the correct sides; the "
                "other two restore the order inside each group."},
    ],
)


def _product_frames():
    values = [1, 2, 3, 4]
    out = []
    prefix = [1] * len(values)
    for i in range(1, len(values)):
        prefix[i] = prefix[i - 1] * values[i - 1]
    out.append(frame([marked(values, {j: "dim" for j in range(len(values))},
                             label="values"),
                      marked(prefix, {j: "hit" for j in range(len(prefix))},
                             label="product of everything LEFT")],
                     "Left pass: each cell holds the product of everything "
                     "before it. Nothing to its right has been touched.",
                     {"pass": 1}))
    result = list(prefix)
    running = 1
    for i in range(len(values) - 1, -1, -1):
        result[i] = result[i] * running
        running *= values[i]
        out.append(frame([marked(values, {i: "lo"}, label="values"),
                          marked(list(result), {i: "hit"},
                                 label="left x right so far")],
                         "Right pass at index %d: multiply by %d, the product of "
                         "everything after it." % (i, running // values[i]),
                         {"pass": 2, "running": running}))
    out.append(frame(marked(result, {j: "done" for j in range(len(result))},
                            label="answer"),
                     "Two passes, no division, and the output array is the only "
                     "extra memory used.",
                     {"pass": 2, "running": running}))
    return viz(out)


_q(
    slug="product-of-array-except-self",
    kind="coding",
    level="Medium",
    title="Product of array except self",
    asked="For each element, return the product of every other element - without "
          "using division.",
    desc="Prefix and suffix products in two passes, why the division shortcut "
         "fails on zeros, and how to do it with the output array as the only "
         "extra space.",
    lead="Two passes. The first fills each cell with the product of everything "
         "to its <strong>left</strong>; the second walks backwards multiplying "
         "by a running product of everything to the <strong>right</strong>. O(n) "
         "time, no division, and the output array is the only extra memory.",
    say="\"Prefix products left to right, then a running suffix product right to "
        "left, multiplied into the same array. O(n) time, O(1) extra space "
        "beyond the output - and no division, so zeros are not a special case.\"",
    notice=[
        "After the first pass each cell knows only about its left.",
        "The second pass folds in the right side without a second array.",
        "No element is ever divided &mdash; zeros need no special handling.",
    ],
    viz=_product_frames(),
    sections=[
        ("Why not just divide",
         "<p>Multiply everything, then divide by each element. It is O(n), it is "
         "the first thing everyone says, and the question explicitly forbids it "
         "&mdash; because it breaks on zero. One zero makes every other answer a "
         "division by zero; two zeros make every answer zero.</p>"
         "<p>You can special-case the zero count, and it works. Say that, then "
         "give the prefix/suffix answer, because the point of the question is "
         "the decomposition rather than the arithmetic.</p>"),
        ("The decomposition",
         "<p>The product of everything except element <em>i</em> is "
         "(everything left of i) &times; (everything right of i). Both of those "
         "are cumulative products, and each can be built in one pass.</p>"
         "<p>The trick that gets you to O(1) extra space is to store the left "
         "products directly in the output array, then walk backwards carrying "
         "the right product in a single variable and multiplying it in. No "
         "second array is ever allocated.</p>"),
        ("The pattern to recognise",
         "<p>\"Something about everything except me\" is almost always prefix and "
         "suffix aggregates. The same shape solves trapping rain water (max to "
         "the left and right of each bar), candy distribution, and the "
         "maximum-product subarray.</p>"
         "<p>Note the convention: the leftmost prefix and the rightmost suffix "
         "are both 1, the identity for multiplication. For a sum-based variant "
         "they would be 0. Getting the identity wrong is the usual bug.</p>"),
    ],
    code={
        "file": "product_except_self.py",
        "intro": "The two-pass version with both intermediate states printed, "
                 "checked against the division shortcut &mdash; which is given "
                 "arrays containing one zero and two zeros so you can watch it "
                 "fail.",
        "code": '''# Product of everything except self, without division.

def product_except_self(values):
    n = len(values)
    result = [1] * n

    running = 1                       # everything to the LEFT
    for i in range(n):
        result[i] = running
        running *= values[i]
    print("  after the left pass :", result)

    running = 1                       # everything to the RIGHT
    for i in range(n - 1, -1, -1):
        result[i] *= running
        running *= values[i]
    print("  after the right pass:", result)
    return result


def by_division(values):
    """The forbidden shortcut, and why it is forbidden."""
    total = 1
    for v in values:
        total *= v
    return [total // v for v in values]


values = [1, 2, 3, 4]
print("values:", values)
print("answer:", product_except_self(values))
print("division would give:", by_division(values), "- same, here")

# --- where division falls over -----------------------------------------
print()
for sample in ([1, 2, 0, 4], [0, 2, 0, 4]):
    print(f"values: {sample}")
    print("  prefix/suffix:", product_except_self(sample))
    try:
        print("  by division  :", by_division(sample))
    except ZeroDivisionError as e:
        print("  by division  : ZeroDivisionError -", e)

print()
print("One zero: every other answer needs a division by zero.")
print("Two zeros: every answer is zero, and division cannot see that either.")

# --- the identity matters ----------------------------------------------
print()
print("The first prefix and the last suffix are both 1 - the identity for")
print("multiplication. For a sum-based version they would be 0 instead.")
''',
        "walk": [
            ("result[i] = running  (before the update)",
             "Assign first, then fold in <code>values[i]</code>. Doing it the "
             "other way round includes the element itself, which is precisely "
             "what the question excludes."),
            ("the second loop reuses `result`",
             "The output array carries the left products into the right pass, so "
             "no second array is needed. That is what takes the extra space from "
             "O(n) to O(1)."),
            ("running = 1",
             "The identity for multiplication, so the first prefix and last "
             "suffix contribute nothing. A sum-based variant would start at 0 "
             "&mdash; the usual off-by-identity bug."),
            ("by_division",
             "Kept to be broken. One zero and the division fails; two zeros and "
             "even a special case has to know how many there were."),
        ],
        "try": [
            "Fix the division version by counting zeros first. It works, and "
            "compare how much longer it is than the two-pass one.",
            "Change the operation to addition &mdash; sum of everything except "
            "self. The identity becomes 0 and the structure is unchanged.",
        ],
    },
    check=[
        {"q": "Why is division ruled out?",
         "options": ["It is slow", "A single zero makes every other answer a "
                     "division by zero",
                     "It loses precision", "It needs an extra array"],
         "answer": 1,
         "why": "Two zeros is worse still. You can special-case the zero count, "
                "but the question is really about the prefix/suffix decomposition."},
        {"q": "The extra space beyond the output array is:",
         "options": ["O(n) for the suffix array", "O(1) - the running product is "
                     "a single variable",
                     "O(log n)", "O(n²)"],
         "answer": 1,
         "why": "The left products are stored in the output array itself and the "
                "right product is carried in one variable."},
        {"q": "Why is the running product initialised to 1?",
         "options": ["To avoid zeros", "It is the identity for multiplication, "
                     "so the first prefix contributes nothing",
                     "To count elements", "It could be anything"],
         "answer": 1,
         "why": "A sum-based version of the same pattern would initialise to 0. "
                "Getting the identity wrong is the standard bug."},
    ],
)
