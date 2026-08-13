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


def _intervals_frames():
    data = [(1, 3), (2, 6), (8, 10), (9, 12), (15, 18)]
    out = [frame(pairs([("%d-%d" % iv, "unmerged") for iv in data],
                       {}, label="sorted by start"),
                 "Sort by start first. That is what makes one pass enough - an "
                 "interval can only ever overlap the one before it.",
                 {"merged": 0})]
    merged = [list(data[0])]
    for lo, hi in data[1:]:
        touches = lo <= merged[-1][1]
        if touches:
            merged[-1][1] = max(merged[-1][1], hi)
        else:
            merged.append([lo, hi])
        out.append(frame(pairs([("%d-%d" % tuple(m), "kept") for m in merged],
                               {"%d-%d" % tuple(merged[-1]): "hit" if touches else "lo"},
                               label="merged so far"),
                         "%d-%d %s" % (lo, hi,
                                       "overlaps the last one, so extend it to %d."
                                       % merged[-1][1] if touches
                                       else "starts after the last one ends, so open a new interval."),
                         {"merged": len(merged)}))
    return viz(out)


_q(
    slug="merge-intervals",
    kind="coding",
    level="Medium",
    title="Merge overlapping intervals",
    asked="Given a list of intervals, merge the ones that overlap.",
    desc="Sorting by start turns interval merging into a single pass, why "
         "comparing against the last kept interval is enough, and the "
         "touching-versus-overlapping edge case.",
    lead="<strong>Sort by start.</strong> After that an interval can only "
         "overlap the one immediately before it, so a single pass merges "
         "everything: extend the last kept interval if it reaches this one, "
         "otherwise start a new one. O(n&nbsp;log&nbsp;n) for the sort, O(n) "
         "after it.",
    say="\"Sort by start, then sweep. Each interval either extends the last "
        "merged one or starts a new one. The sort dominates, so O(n log n).\"",
    notice=[
        "Sorting is the whole trick &mdash; without it every pair must be compared.",
        "Only the <em>last</em> merged interval is ever checked.",
        "Extending takes the larger end, not this interval's end.",
    ],
    viz=_intervals_frames(),
    sections=[
        ("Why sorting collapses the problem",
         "<p>Unsorted, any interval can overlap any other, so you are looking at "
         "pairs &mdash; O(n&sup2;). Sorted by start, an interval's only possible "
         "overlap is with the merged block immediately behind it, because "
         "everything earlier starts earlier and has already been absorbed.</p>"
         "<p>That reduces the whole thing to one comparison per interval. The "
         "sort costs O(n&nbsp;log&nbsp;n) and dominates.</p>"),
        ("The line people get wrong",
         "<p>When extending, take <code>max(last_end, this_end)</code>, not "
         "<code>this_end</code>. A fully contained interval &mdash; "
         "<code>[1, 10]</code> then <code>[2, 3]</code> &mdash; would otherwise "
         "shrink the merged block to 3 and silently lose everything from 3 to "
         "10.</p>"
         "<p>The other decision is whether touching counts as overlapping. "
         "<code>[1, 3]</code> and <code>[3, 5]</code> merge under "
         "<code>lo &lt;= last_end</code> and stay separate under "
         "<code>&lt;</code>. Both are defensible; ask which the question "
         "wants.</p>"),
        ("What it generalises to",
         "<p>Meeting rooms, calendar conflicts, genome ranges, IP blocks &mdash; "
         "all the same sweep. The variants change only the merge rule: count how "
         "many rooms are needed simultaneously (a sweep line with +1 and "
         "&minus;1 events), insert one interval into an already-merged list, or "
         "find the gaps rather than the blocks.</p>"),
    ],
    code={
        "file": "merge_intervals.py",
        "intro": "The sweep with each decision printed, the contained-interval "
                 "case that breaks the naive extend, and both answers to the "
                 "touching question.",
        "code": '''# Merge overlapping intervals: sort by start, then sweep once.

def merge(intervals, touching_counts=True):
    if not intervals:
        return []
    ordered = sorted(intervals)               # by start, then end
    merged = [list(ordered[0])]
    for lo, hi in ordered[1:]:
        last = merged[-1]
        overlaps = lo <= last[1] if touching_counts else lo < last[1]
        if overlaps:
            last[1] = max(last[1], hi)        # max, NOT hi - see below
        else:
            merged.append([lo, hi])
    return [tuple(m) for m in merged]


data = [(1, 3), (2, 6), (8, 10), (9, 12), (15, 18)]
print("input :", data)
print("merged:", merge(data))

# --- the contained-interval trap ---------------------------------------
def merge_wrong(intervals):
    ordered = sorted(intervals)
    out = [list(ordered[0])]
    for lo, hi in ordered[1:]:
        if lo <= out[-1][1]:
            out[-1][1] = hi                   # loses a contained interval
        else:
            out.append([lo, hi])
    return [tuple(m) for m in out]

contained = [(1, 10), (2, 3), (4, 5)]
print()
print("input        :", contained)
print("with max()   :", merge(contained))
print("without max():", merge_wrong(contained), "  <- 10 was thrown away")

# --- does touching count? ----------------------------------------------
touching = [(1, 3), (3, 5), (6, 8)]
print()
print("input                :", touching)
print("touching merges      :", merge(touching, touching_counts=True))
print("touching stays apart :", merge(touching, touching_counts=False))
print("Both are defensible. Ask which the question wants.")

# --- the sweep-line variant: how many rooms at once? -------------------
def max_overlap(intervals):
    events = []
    for lo, hi in intervals:
        events.append((lo, 1))                # an interval opens
        events.append((hi, -1))               # and closes
    events.sort()
    live = best = 0
    for _, delta in events:
        live += delta
        best = max(best, live)
    return best

print()
print("rooms needed for", data, "->", max_overlap(data))
''',
        "walk": [
            ("sorted(intervals)",
             "The whole reduction. Sorted by start, an interval can only overlap "
             "the merged block directly behind it, so one comparison per "
             "interval replaces comparing every pair."),
            ("last[1] = max(last[1], hi)",
             "The <code>max</code> is load-bearing. <code>[1, 10]</code> followed "
             "by <code>[2, 3]</code> would otherwise shrink the block to 3 and "
             "silently drop everything up to 10."),
            ("lo <= last[1] versus lo < last[1]",
             "Whether <code>[1,3]</code> and <code>[3,5]</code> merge. Both "
             "conventions are used; the question usually implies one, and asking "
             "is a better move than guessing."),
            ("events.sort() in max_overlap",
             "The sweep-line variant: +1 when an interval opens, &minus;1 when it "
             "closes, and the running total is how many are live at once. Same "
             "sort, different question."),
        ],
        "try": [
            "Feed it intervals already sorted by <em>end</em> instead. The sweep "
            "gives wrong answers &mdash; the precondition is specifically sorted "
            "by start.",
            "Write <code>insert(intervals, new)</code> for an already-merged "
            "list. It is O(n) with no sort, and a common follow-up.",
        ],
    },
    check=[
        {"q": "Why does sorting by start make one pass sufficient?",
         "options": ["It removes duplicates", "An interval can then only overlap "
                     "the merged block immediately before it",
                     "It makes the list shorter", "Sorting merges them"],
         "answer": 1,
         "why": "Everything earlier starts earlier and has already been absorbed, "
                "so there is only ever one candidate to compare against."},
        {"q": "Why must the extend use max(last_end, this_end)?",
         "options": ["For speed", "A fully contained interval would otherwise "
                     "shrink the merged block",
                     "To handle negatives", "It does not matter"],
         "answer": 1,
         "why": "[1,10] then [2,3] would set the end to 3 and silently lose "
                "everything from 3 to 10."},
        {"q": "The overall complexity is:",
         "options": ["O(n)", "O(n log n), dominated by the sort", "O(n²)",
                     "O(log n)"],
         "answer": 1,
         "why": "The sweep itself is linear. If the input arrives already sorted, "
                "the whole thing is O(n)."},
    ],
)


def _duplicate_frames():
    values = [3, 1, 3, 4, 2]
    out = [frame(marked(values, {i: "dim" for i in range(len(values))},
                        label="values 1..n in an array of n+1"),
                 "By pigeonhole there must be a duplicate. The trick is finding "
                 "it without a set and without modifying the array.",
                 {"slow": 0, "fast": 0})]
    slow = fast = 0
    for step in range(4):
        slow = values[slow]
        fast = values[values[fast]]
        marks = {i: "dim" for i in range(len(values))}
        marks[slow] = "lo"
        marks[fast] = "hi" if fast != slow else "hit"
        out.append(frame(marked(values, marks, {slow: "slow", fast: "fast"},
                                label="treat each value as a next pointer"),
                         "slow -> index %d, fast -> index %d.%s"
                         % (slow, fast, "  They have met." if slow == fast else ""),
                         {"slow": slow, "fast": fast}))
        if slow == fast:
            break
    finder = 0
    while finder != slow:
        finder = values[finder]
        slow = values[slow]
    out.append(frame(marked(values, {i: ("hit" if values[i] == finder or i == finder
                                         else "dim") for i in range(len(values))},
                            label="values"),
                     "Phase two walks one pointer from the start; they meet at "
                     "the duplicate, %d. O(1) memory, array untouched." % finder,
                     {"slow": slow, "fast": finder}))
    return viz(out)


_q(
    slug="find-the-duplicate-number",
    kind="coding",
    level="Hard",
    title="Find the duplicate number",
    asked="An array of n+1 integers holds values from 1 to n. Find the duplicate "
          "without modifying the array and in O(1) space.",
    desc="Floyd's cycle detection applied to an array: why treating values as "
         "pointers creates a linked list with a loop, and why the easy answers "
         "are ruled out by the constraints.",
    lead="Treat each value as a <strong>pointer to an index</strong>. Because "
         "values are in 1..n and there are n+1 of them, following those pointers "
         "must eventually revisit a node &mdash; and the entrance to that cycle "
         "is the duplicate. Floyd's tortoise and hare finds it in O(n) time and "
         "O(1) space.",
    say="\"The constraints rule out sorting and a set. If you read each value as "
        "a next-pointer, the array is a linked list that must contain a cycle, "
        "and the cycle entrance is the duplicate - so it's Floyd's algorithm.\"",
    notice=[
        "The two pointers move at different speeds until they meet.",
        "Meeting is <em>not</em> the answer &mdash; phase two finds the entrance.",
        "Nothing is written to the array and nothing is allocated.",
    ],
    viz=_duplicate_frames(),
    sections=[
        ("Read the constraints first",
         "<p>The easy answers are all excluded on purpose. A <code>set</code> is "
         "O(n) space. Sorting modifies the array. Marking visited indices by "
         "negating them modifies it too. Each constraint removes one obvious "
         "solution, and what is left is the intended one &mdash; which is why "
         "reading the constraints aloud is a real technique, not a stall.</p>"),
        ("Turning the array into a linked list",
         "<p>Start at index 0 and repeatedly jump to the index named by the "
         "current value. Values are in 1..n, so no jump leaves the array and no "
         "jump lands on index 0 &mdash; index 0 is the start of the chain and "
         "never re-entered.</p>"
         "<p>There are n+1 slots and only n distinct values, so two slots share "
         "a value, so two different nodes point at the same next node. That "
         "shared target is where the chain closes into a loop, and it <em>is</em> "
         "the duplicate value.</p>"),
        ("Why phase two works",
         "<p>Once the pointers meet inside the loop, the distance from the head "
         "to the loop entrance equals the distance from the meeting point to the "
         "entrance. So walking one pointer from the start and one from the "
         "meeting point, one step at a time, makes them meet exactly at the "
         "entrance.</p>"
         "<p>It looks like magic and falls out of the arithmetic. Say that the "
         "same two-phase structure detects a cycle in an actual linked list "
         "&mdash; the interviewer is usually checking whether you recognise the "
         "algorithm rather than whether you can rederive the proof.</p>"),
    ],
    code={
        "file": "find_duplicate.py",
        "intro": "Floyd's two phases with the pointer positions printed, checked "
                 "against a set-based version on random inputs, plus the "
                 "binary-search-on-value alternative.",
        "code": '''# Find the duplicate: values are pointers, so the array is a linked list.
import random

def floyd(values):
    slow = fast = 0
    steps = 0
    while True:                              # phase 1: find a meeting point
        slow = values[slow]
        fast = values[values[fast]]
        steps += 1
        if slow == fast:
            break
    meeting = slow

    finder = 0                               # phase 2: find the entrance
    while finder != slow:
        finder = values[finder]
        slow = values[slow]
        steps += 1
    return finder, meeting, steps


def with_a_set(values):
    """Correct, and O(n) space - which the question forbids."""
    seen = set()
    for v in values:
        if v in seen:
            return v
        seen.add(v)
    return None


def binary_search_on_value(values):
    """O(n log n) time, O(1) space. Counts how many values are <= mid."""
    lo, hi = 1, len(values) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        count = sum(1 for v in values if v <= mid)
        if count > mid:                      # pigeonhole: the duplicate is <= mid
            hi = mid
        else:
            lo = mid + 1
    return lo


data = [3, 1, 3, 4, 2]
answer, meeting, steps = floyd(data)
print("array    :", data)
print("duplicate:", answer, f"(pointers met at index {meeting}, {steps} steps)")
print("array unchanged:", data)

# Agreement across random inputs is the real check.
print()
random.seed(11)
for _ in range(6):
    n = random.randint(4, 12)
    base = list(range(1, n + 1))
    values = base + [random.choice(base)]
    random.shuffle(values)
    a = floyd(values)[0]
    b = with_a_set(values)
    c = binary_search_on_value(values)
    print(f"  n={n:>2}  floyd={a:>2} set={b:>2} binary={c:>2}  agree={a == b == c}")

print()
print("A set is O(n) memory. Sorting modifies the array. Negating visited")
print("indices modifies it too. Each constraint removes one obvious answer.")
''',
        "walk": [
            ("fast = values[values[fast]]",
             "Two jumps to the tortoise's one. Inside a loop the gap closes by "
             "one node per step, so they are guaranteed to meet."),
            ("meeting is not the answer",
             "Phase one only proves a cycle exists and finds <em>a</em> point "
             "inside it. Returning <code>slow</code> here is the most common way "
             "to get this almost right."),
            ("while finder != slow:",
             "Phase two. The distance from the head to the entrance equals the "
             "distance from the meeting point to the entrance, so two pointers "
             "advancing in step converge exactly on it."),
            ("binary_search_on_value",
             "The alternative worth naming: count values &le; mid and use "
             "pigeonhole to pick a half. O(n&nbsp;log&nbsp;n) time, O(1) space, "
             "and much easier to derive under pressure."),
        ],
        "try": [
            "Put the duplicate at both ends &mdash; <code>[2, 3, 4, 2]</code>. "
            "The step count changes and the answer does not.",
            "Return <code>meeting</code> instead of <code>finder</code>. It is "
            "right often enough to pass a careless test and wrong in general.",
        ],
    },
    check=[
        {"q": "Why can the array be treated as a linked list?",
         "options": ["It is sorted", "Every value is a valid index, so each slot "
                     "points to another slot",
                     "It contains no zeros", "It is the same length as its values"],
         "answer": 1,
         "why": "Values are in 1..n, so no jump leaves the array and index 0 is "
                "never re-entered - making it a chain with a guaranteed cycle."},
        {"q": "The meeting point of the two pointers is:",
         "options": ["The duplicate", "Somewhere inside the cycle, not "
                     "necessarily its entrance",
                     "Always index 0", "The array length"],
         "answer": 1,
         "why": "Phase one only proves a cycle exists. Phase two walks from the "
                "head to find the entrance, which is the duplicate."},
        {"q": "Which constraint rules out using a set?",
         "options": ["Do not modify the array", "O(1) space", "O(n) time",
                     "Values are 1..n"],
         "answer": 1,
         "why": "A set is O(n) memory. 'Do not modify' is what rules out sorting "
                "and index-negation instead."},
    ],
)


def _kth_largest_frames():
    values = [17, 4, 92, 8, 55, 23]
    k = 3
    out = []
    heap = []
    for i, v in enumerate(values):
        if len(heap) < k:
            heap.append(v)
            heap.sort()
            note = "Heap not full yet, so %d goes in." % v
            state = "hit"
        elif v > heap[0]:
            dropped = heap[0]
            heap = sorted(heap[1:] + [v])
            note = "%d beats the smallest kept (%d), so swap them." % (v, dropped)
            state = "hit"
        else:
            note = "%d loses to the smallest kept (%d) - discard it." % (v, heap[0])
            state = "bad"
        marks = {j: ("dim" if j > i else "done") for j in range(len(values))}
        marks[i] = state
        out.append(frame([marked(values, marks, {i: "reading"}, label="input"),
                          marked(heap, {0: "lo"}, label="heap of %d (smallest first)" % k)],
                         note, {"kept": len(heap), "kth": heap[0]}))
    out.append(frame(marked(heap, {0: "hit"}, label="final heap"),
                     "The heap holds the %d largest, and its smallest member is "
                     "the %drd largest overall: %d. Only %d values were ever "
                     "stored." % (k, k, heap[0], k),
                     {"kept": len(heap), "kth": heap[0]}))
    return viz(out)


_q(
    slug="kth-largest-element",
    kind="coding",
    level="Medium",
    title="Kth largest element",
    asked="Find the kth largest element in an unsorted array.",
    desc="A min-heap of size k gives O(n log k) and O(k) memory; quickselect "
         "gives O(n) average; sorting gives O(n log n). Which to pick, and why.",
    lead="Keep a <strong>min-heap of size k</strong>. Each value either beats "
         "the smallest kept one and replaces it, or is discarded immediately. "
         "The heap's root is the answer. O(n&nbsp;log&nbsp;k) time and O(k) "
         "memory &mdash; which matters when n is enormous and k is ten.",
    say="\"Min-heap of size k: O(n log k) time, O(k) space. Sorting is O(n log n) "
        "and quickselect is O(n) average but O(n²) worst case. For a stream, or "
        "when n doesn't fit in memory, the heap is the only one that works.\"",
    notice=[
        "The heap never grows beyond k &mdash; that is the memory bound.",
        "A value smaller than the root is discarded without being stored.",
        "The root is always the smallest of the k largest.",
    ],
    viz=_kth_largest_frames(),
    sections=[
        ("Three answers, and the reason to choose",
         "<p><strong>Sort and index.</strong> <code>sorted(a)[-k]</code>. "
         "O(n&nbsp;log&nbsp;n), one line, and the right answer in real code for "
         "any array that fits in memory.</p>"
         "<p><strong>Min-heap of size k.</strong> O(n&nbsp;log&nbsp;k) time and "
         "O(k) memory. The only one that works on a stream, or when n is far "
         "larger than memory.</p>"
         "<p><strong>Quickselect.</strong> O(n) average by partitioning and "
         "recursing into one side only. O(n&sup2;) worst case with a bad pivot, "
         "fixable with a random one.</p>"
         "<p>Interviewers are usually listening for whether you notice the heap "
         "is bounded by k rather than n.</p>"),
        ("Why a min-heap for the largest",
         "<p>It feels backwards and it is the key idea. To keep the k "
         "<em>largest</em> values you need constant-time access to the "
         "<em>smallest</em> of the ones you kept, because that is the one to "
         "evict when something better arrives. A min-heap puts exactly that at "
         "the root.</p>"
         "<p>Once the heap is full, a value below the root cannot be in the top "
         "k, so it is discarded without being stored at all.</p>"),
        ("Quickselect, briefly",
         "<p>Partition around a pivot as quicksort does, then recurse into only "
         "the side containing position k. Because one side is discarded each "
         "time, the expected work is n + n/2 + n/4 + ... = O(n).</p>"
         "<p>Its worst case is O(n&sup2;) on a bad pivot sequence, so pick the "
         "pivot at random. Say that explicitly &mdash; \"quickselect, with a "
         "random pivot\" is a complete answer, and \"quickselect\" alone invites "
         "the follow-up about sorted input.</p>"),
    ],
    code={
        "file": "kth_largest.py",
        "intro": "All three approaches with the number of elements each one "
                 "stores, then timed on a large array so the O(k) memory claim "
                 "and the O(n) average are both visible.",
        "code": '''# Kth largest: sort it, heap it, or partition it.
import heapq, random, time

def by_sorting(values, k):
    return sorted(values)[-k]                    # O(n log n), stores n


def by_heap(values, k):
    """A MIN-heap of size k: its root is the smallest of the k largest."""
    heap = []
    for v in values:
        if len(heap) < k:
            heapq.heappush(heap, v)
        elif v > heap[0]:                        # beats the weakest kept
            heapq.heapreplace(heap, v)           # pop and push in one step
    return heap[0], len(heap)


def quickselect(values, k):
    """O(n) average. Recurse into one side only."""
    target = len(values) - k                     # kth largest = this index sorted
    a = list(values)
    lo, hi = 0, len(a) - 1
    while lo < hi:
        pivot = a[random.randint(lo, hi)]        # random: avoids the O(n^2) case
        i, j = lo, hi
        while i <= j:
            while a[i] < pivot:
                i += 1
            while a[j] > pivot:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i, j = i + 1, j - 1
        if target <= j:
            hi = j
        elif target >= i:
            lo = i
        else:
            break
    return a[target]


random.seed(5)
data = [17, 4, 92, 8, 55, 23]
k = 3
answer, kept = by_heap(data, k)
print("data:", data, " k =", k)
print(f"  sorting     : {by_sorting(data, k)}   (stores {len(data)} values)")
print(f"  min-heap    : {answer}   (stores {kept} values)")
print(f"  quickselect : {quickselect(data, k)}")

# --- the memory claim, at scale ----------------------------------------
big = [random.randint(0, 10_000_000) for _ in range(400_000)]
k = 10
print()
print(f"n = {len(big):,}, k = {k}")
for name, fn in (("sorting", lambda: by_sorting(big, k)),
                 ("min-heap", lambda: by_heap(big, k)[0]),
                 ("quickselect", lambda: quickselect(big, k))):
    start = time.time()
    result = fn()
    print(f"  {name:>12}: {result:>9}  in {time.time() - start:.3f}s")

print()
print(f"The heap held {k} values the whole way. Sorting held {len(big):,},")
print("which is the difference that matters when n does not fit in memory.")
''',
        "walk": [
            ("heapq.heapreplace(heap, v)",
             "Pop the root and push the new value in one operation. Doing it as "
             "a pop then a push costs two sift operations instead of one and is "
             "the usual way to write this slightly wrong."),
            ("elif v > heap[0]",
             "A value below the root cannot be in the top k, so it is discarded "
             "without ever being stored. That test is what keeps the memory at "
             "O(k)."),
            ("a MIN-heap for the LARGEST k",
             "The counterintuitive part. Keeping the k largest requires "
             "constant-time access to the weakest of them, so it can be evicted "
             "&mdash; and a min-heap puts exactly that at the root."),
            ("pivot = a[random.randint(lo, hi)]",
             "Quickselect's worst case is O(n&sup2;) on an adversarial pivot "
             "sequence. Choosing at random makes that vanishingly unlikely, and "
             "saying so out loud is part of the answer."),
        ],
        "try": [
            "Set <code>k = len(big)</code>. The heap now stores everything and "
            "the approach collapses back to sorting &mdash; the win is entirely "
            "in k being small.",
            "Replace <code>heapreplace</code> with a push followed by a pop and "
            "compare the timings. Same answer, more sifting.",
        ],
    },
    check=[
        {"q": "Why a MIN-heap when you want the k LARGEST elements?",
         "options": ["It is faster to build", "Its root is the weakest kept "
                     "value, which is the one to evict",
                     "Max-heaps do not exist in Python", "It sorts as it goes"],
         "answer": 1,
         "why": "You need O(1) access to the smallest of the ones you are "
                "keeping, so a new larger value can replace it immediately."},
        {"q": "The heap approach uses how much memory?",
         "options": ["O(n)", "O(k)", "O(log n)", "O(n log k)"],
         "answer": 1,
         "why": "The heap never exceeds k entries. That is the whole reason to "
                "prefer it when n is huge or arrives as a stream."},
        {"q": "Quickselect's worst case is:",
         "options": ["O(n)", "O(n²), which a random pivot makes very unlikely",
                     "O(n log n)", "O(log n)"],
         "answer": 1,
         "why": "A consistently bad pivot peels off one element at a time. "
                "Saying 'quickselect with a random pivot' pre-empts the follow-up."},
    ],
)


def _rain_frames():
    heights = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    out = []
    lo, hi = 0, len(heights) - 1
    left_max = right_max = total = 0
    steps = 0
    while lo < hi and steps < 6:
        if heights[lo] < heights[hi]:
            left_max = max(left_max, heights[lo])
            total += left_max - heights[lo]
            side, idx, gained = "left", lo, left_max - heights[lo]
            lo += 1
        else:
            right_max = max(right_max, heights[hi])
            total += right_max - heights[hi]
            side, idx, gained = "right", hi, right_max - heights[hi]
            hi -= 1
        marks = {i: ("dim" if i < lo or i > hi else "lo") for i in range(len(heights))}
        marks[idx] = "hit" if gained else "done"
        out.append(frame(marked(heights, marks, {lo: "lo", hi: "hi"}, label="bar heights"),
                         "The %s bar is shorter, so its side is the binding "
                         "constraint: it holds %d unit(s). Running total %d."
                         % (side, gained, total),
                         {"lo": lo, "hi": hi, "water": total}))
        steps += 1
    out.append(frame(marked(heights, {i: "done" for i in range(len(heights))},
                            label="bar heights"),
                     "Each bar was visited once and its water settled "
                     "immediately - no second array of maxima was ever built.",
                     {"lo": lo, "hi": hi, "water": total}))
    return viz(out)


_q(
    slug="trapping-rain-water",
    kind="coding",
    level="Hard",
    title="Trapping rain water",
    asked="Given bar heights, how much water is trapped between them?",
    desc="Water above a bar is set by the smaller of the tallest bars either "
         "side; two pointers compute that in one pass with O(1) space.",
    lead="Water above one bar is <code>min(tallest left, tallest right) &minus; "
         "its own height</code>. The two-pointer version exploits one fact: "
         "whichever side is <strong>shorter</strong> is the binding constraint, "
         "so that side's water can be settled immediately. One pass, O(1) space.",
    say="\"Per bar it's min of the max to the left and the max to the right, "
        "minus its height. Two pointers from both ends: always move the shorter "
        "side, because that side's maximum is what limits it. O(n) time, O(1) "
        "space.\"",
    notice=[
        "Only the shorter side is advanced, and only that side's water is settled.",
        "The running maxima are two integers, not two arrays.",
        "Each bar is visited exactly once.",
    ],
    viz=_rain_frames(),
    sections=[
        ("The per-bar formula",
         "<p>Water sits above a bar up to the level of the lower of the two "
         "walls containing it: <code>min(max to the left, max to the right) "
         "&minus; height</code>, or zero if that is negative.</p>"
         "<p>The direct implementation precomputes both arrays of running "
         "maxima and then sums. That is O(n) time and O(n) space, perfectly "
         "correct, and the right first answer. The two-pointer version removes "
         "the arrays.</p>"),
        ("Why moving the shorter side is safe",
         "<p>Suppose <code>height[lo] &lt; height[hi]</code>. Then whatever the "
         "maxima turn out to be, the left side's is the smaller of the two "
         "&mdash; because there is already a bar at least as tall as "
         "<code>height[hi]</code> on the right. So the water above "
         "<code>lo</code> is decided by <code>left_max</code> alone and can be "
         "settled now, without knowing anything more about the right.</p>"
         "<p>That is the whole argument, and it is worth stating explicitly. "
         "Candidates who write this from memory usually cannot say why moving "
         "the shorter side is the correct choice.</p>"),
        ("The stack alternative",
         "<p>A monotonic decreasing stack also solves it in O(n), filling water "
         "horizontally layer by layer rather than column by column. It is "
         "harder to get right under pressure and worth naming as an "
         "alternative.</p>"
         "<p>The same \"maximum to the left and right of each element\" shape "
         "appears in largest-rectangle-in-a-histogram and stock-span, so "
         "recognising it is worth more than memorising this one solution.</p>"),
    ],
    code={
        "file": "rain_water.py",
        "intro": "The two-pointer sweep against the precomputed-arrays version "
                 "and a brute force, with the extra memory each one uses printed "
                 "&mdash; all three agreeing on every test.",
        "code": '''# Trapping rain water: the shorter side is always the binding constraint.

def brute_force(heights):
    """For each bar, scan both ways for the tallest. O(n^2)."""
    total = 0
    for i in range(len(heights)):
        left = max(heights[:i + 1])
        right = max(heights[i:])
        total += min(left, right) - heights[i]
    return total


def with_arrays(heights):
    """Precompute both running maxima. O(n) time, O(n) space."""
    n = len(heights)
    if not n:
        return 0, 0
    left = [0] * n
    right = [0] * n
    left[0] = heights[0]
    for i in range(1, n):
        left[i] = max(left[i - 1], heights[i])
    right[-1] = heights[-1]
    for i in range(n - 2, -1, -1):
        right[i] = max(right[i + 1], heights[i])
    total = sum(min(left[i], right[i]) - heights[i] for i in range(n))
    return total, 2 * n                       # extra values stored


def two_pointers(heights):
    """O(n) time, O(1) space. Move whichever side is shorter."""
    lo, hi = 0, len(heights) - 1
    left_max = right_max = total = 0
    while lo < hi:
        if heights[lo] < heights[hi]:
            # The left is the smaller wall, so left_max alone decides this bar.
            left_max = max(left_max, heights[lo])
            total += left_max - heights[lo]
            lo += 1
        else:
            right_max = max(right_max, heights[hi])
            total += right_max - heights[hi]
            hi -= 1
    return total, 2                            # two running maxima


data = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print("heights:", data)
print()
brute = brute_force(data)
arrays, arr_mem = with_arrays(data)
pointers, ptr_mem = two_pointers(data)
print(f"  brute force  : {brute:>2}   O(n^2) time")
print(f"  two arrays   : {arrays:>2}   O(n) time, {arr_mem} extra values stored")
print(f"  two pointers : {pointers:>2}   O(n) time, {ptr_mem} extra values stored")
print("  all agree    :", brute == arrays == pointers)

print()
for sample in ([4, 2, 0, 3, 2, 5], [3, 3, 3], [5], [], [2, 1]):
    if not sample:
        print(f"  {str(sample):>18}: 0 (empty)")
        continue
    print(f"  {str(sample):>18}: {two_pointers(sample)[0]}")
print()
print("A flat or descending profile traps nothing - there is no wall to hold it.")
''',
        "walk": [
            ("if heights[lo] < heights[hi]:",
             "The decision the whole approach rests on. The shorter side is "
             "necessarily the smaller of the two maxima, so its water is already "
             "determined."),
            ("total += left_max - heights[lo]",
             "Settled immediately, with no knowledge of the right side. That is "
             "only valid because of the comparison above &mdash; be ready to say "
             "why."),
            ("left_max = max(left_max, heights[lo])",
             "Two integers replace the two arrays of the previous version. The "
             "algorithm is the same; only the bookkeeping shrank."),
            ("while lo < hi",
             "Strictly less than. The two pointers meeting means every bar has "
             "been settled exactly once."),
        ],
        "try": [
            "Feed it a strictly increasing list. The answer is zero &mdash; "
            "there is no right wall to hold anything.",
            "Print <code>lo</code>, <code>hi</code> and both maxima each "
            "iteration and check that the shorter side is always the one that "
            "moves.",
        ],
    },
    check=[
        {"q": "The water above a single bar equals:",
         "options": ["The tallest bar minus its height",
                     "min(tallest to the left, tallest to the right) minus its height",
                     "Its height", "The average of its neighbours"],
         "answer": 1,
         "why": "Water is held by the lower of the two containing walls. Anything "
                "above that level runs off."},
        {"q": "Why is it safe to settle the shorter side's water immediately?",
         "options": ["It is an approximation", "The shorter side is necessarily "
                     "the smaller of the two maxima, so it alone decides",
                     "Water flows left", "It is not safe"],
         "answer": 1,
         "why": "A bar at least as tall already exists on the other side, so the "
                "min is on this side and nothing further can change it."},
        {"q": "The two-pointer version improves on the precomputed-arrays "
              "version in:",
         "options": ["Time", "Space - O(1) instead of O(n)", "Correctness",
                     "Both time and space"],
         "answer": 1,
         "why": "Both are O(n) time. Two running maxima replace two full arrays."},
    ],
)


def _dutch_frames():
    values = [2, 0, 2, 1, 1, 0]
    out = []
    lo, mid, hi = 0, 0, len(values) - 1
    while mid <= hi and len(out) < 7:
        v = values[mid]
        if v == 0:
            values[lo], values[mid] = values[mid], values[lo]
            note = "0 at mid - swap it into the low region and advance both."
            lo, mid = lo + 1, mid + 1
        elif v == 2:
            values[mid], values[hi] = values[hi], values[mid]
            note = ("2 at mid - swap it to the high region. mid does NOT advance: "
                    "the value swapped in has not been looked at.")
            hi -= 1
        else:
            note = "1 at mid - already in the middle region, so just advance."
            mid += 1
        marks = {i: ("done" if i < lo else "bad" if i > hi else "lo")
                 for i in range(len(values))}
        if mid < len(values):
            marks[mid] = "hit"
        out.append(frame(marked(list(values), marks,
                                {lo: "lo", hi: "hi"}, label="array"),
                         note, {"lo": lo, "mid": mid, "hi": hi}))
    out.append(frame(marked(list(values), {i: "done" for i in range(len(values))},
                            label="array"),
                     "Sorted in one pass with three pointers and no counting "
                     "array. Every element was moved at most once.",
                     {"lo": lo, "mid": mid, "hi": hi}))
    return viz(out)


_q(
    slug="sort-colors-dutch-national-flag",
    kind="coding",
    level="Medium",
    title="Sort an array of 0s, 1s and 2s",
    asked="Sort an array containing only 0, 1 and 2 in a single pass, in place.",
    desc="The Dutch national flag partition: three pointers, one pass, and the "
         "one case where the middle pointer must not advance.",
    lead="Three pointers carve the array into four regions: settled 0s, settled "
         "1s, unexamined, and settled 2s. A 0 swaps down, a 2 swaps up, a 1 "
         "stays. One pass, O(1) space &mdash; and the one subtlety is that after "
         "swapping a 2 the middle pointer <strong>must not advance</strong>.",
    say="\"Dutch national flag. Three pointers - low, mid, high. 0 swaps to the "
        "low region and both advance, 2 swaps to the high region and only high "
        "moves, 1 just advances mid. One pass, O(1) space.\"",
    notice=[
        "Four regions: settled 0s, settled 1s, unexamined, settled 2s.",
        "After swapping a 2 down, <code>mid</code> stays &mdash; the incoming "
        "value is unseen.",
        "The loop ends when <code>mid</code> passes <code>hi</code>, not the array end.",
    ],
    viz=_dutch_frames(),
    sections=[
        ("The counting alternative",
         "<p>Count the 0s, 1s and 2s, then overwrite the array. Two passes, "
         "trivially correct, and usually the first answer. The question asks for "
         "one pass to rule it out &mdash; and because counting sort does not "
         "generalise to sorting objects by a three-way key, which the partition "
         "does.</p>"),
        ("The invariant",
         "<p>Everything before <code>lo</code> is 0. Everything from "
         "<code>lo</code> to <code>mid</code> is 1. Everything after "
         "<code>hi</code> is 2. Between <code>mid</code> and <code>hi</code> is "
         "unexamined. The loop restores that invariant on every step and stops "
         "when the unexamined region is empty.</p>"
         "<p>Being able to state the invariant is most of the answer here. "
         "Writing the three branches from memory without it is how the "
         "<code>mid</code> bug appears.</p>"),
        ("The one asymmetry",
         "<p>After swapping a 0 into the low region, the value that came back is "
         "from the region already known to be 1s, so <code>mid</code> can safely "
         "advance. After swapping a 2 into the high region, the value that came "
         "back is from the <em>unexamined</em> region &mdash; so "
         "<code>mid</code> must stay and look at it.</p>"
         "<p>Advancing in both cases is the classic bug: the array comes out "
         "almost sorted, with stray 2s left in the middle. It is exactly what "
         "the question is testing.</p>"),
    ],
    code={
        "file": "sort_colors.py",
        "intro": "The three-way partition with its invariant asserted on every "
                 "iteration, the buggy version that advances mid in both "
                 "branches, and both checked against sorted() on random input.",
        "code": '''# Dutch national flag: three pointers, one pass, four regions.
import random

def sort_colors(values):
    lo, mid, hi = 0, 0, len(values) - 1
    while mid <= hi:
        if values[mid] == 0:
            values[lo], values[mid] = values[mid], values[lo]
            lo += 1
            mid += 1                 # what came back is a known 1 - safe to pass
        elif values[mid] == 2:
            values[mid], values[hi] = values[hi], values[mid]
            hi -= 1                  # mid does NOT move: the new value is unseen
        else:
            mid += 1
        # invariant: [0, lo) is 0s, [lo, mid) is 1s, (hi, end) is 2s
        assert all(v == 0 for v in values[:lo])
        assert all(v == 1 for v in values[lo:mid])
        assert all(v == 2 for v in values[hi + 1:])
    return values


def sort_colors_buggy(values):
    """Advances mid in both swap branches. Almost right."""
    lo, mid, hi = 0, 0, len(values) - 1
    while mid <= hi:
        if values[mid] == 0:
            values[lo], values[mid] = values[mid], values[lo]
            lo += 1
            mid += 1
        elif values[mid] == 2:
            values[mid], values[hi] = values[hi], values[mid]
            hi -= 1
            mid += 1                 # <- the bug
        else:
            mid += 1
    return values


def by_counting(values):
    """Two passes, and it does not generalise to sorting objects by a key."""
    counts = [0, 0, 0]
    for v in values:
        counts[v] += 1
    out = []
    for colour, n in enumerate(counts):
        out.extend([colour] * n)
    return out


data = [2, 0, 2, 1, 1, 0]
print("input       :", data)
print("partitioned :", sort_colors(list(data)))
print("by counting :", by_counting(data))

print()
random.seed(3)
failures = 0
for _ in range(200):
    sample = [random.randint(0, 2) for _ in range(random.randint(0, 12))]
    good = sort_colors(list(sample))
    bad = sort_colors_buggy(list(sample))
    if bad != sorted(sample):
        failures += 1
        if failures == 1:
            print(f"first buggy case: {sample} -> {bad} (want {sorted(sample)})")
    assert good == sorted(sample), sample

print(f"correct version: 200/200 random cases pass")
print(f"buggy version  : {failures}/200 cases wrong - it leaves stray 2s behind")
''',
        "walk": [
            ("mid += 1 after a 0 swap",
             "Safe, because the value swapped back comes from the region already "
             "known to hold 1s. Nothing unexamined arrives at "
             "<code>mid</code>."),
            ("no mid += 1 after a 2 swap",
             "The value swapped back comes from the <em>unexamined</em> region, "
             "so it has to be looked at. Advancing here is the bug the second "
             "function demonstrates on real input."),
            ("while mid <= hi",
             "The loop ends when the unexamined region is empty, not at the end "
             "of the array &mdash; everything past <code>hi</code> is already "
             "settled."),
            ("the three assert lines",
             "The invariant, checked rather than described. Stating it is most "
             "of the answer to this question; writing the branches without it is "
             "how the bug appears."),
        ],
        "try": [
            "Delete the asserts and add a fourth colour. The approach does not "
            "extend &mdash; three-way partitioning is specifically three-way.",
            "Sort objects by a three-way key instead of raw integers. The "
            "partition still works; counting does not.",
        ],
    },
    check=[
        {"q": "After swapping a 2 from mid to the high region, why must mid stay?",
         "options": ["To recount", "The value swapped back is from the "
                     "unexamined region and has not been looked at",
                     "To keep it stable", "It should advance"],
         "answer": 1,
         "why": "After a 0 swap the incoming value is a known 1, so mid can pass "
                "it. After a 2 swap it is unexamined - advancing leaves stray 2s."},
        {"q": "The regions maintained by the invariant are:",
         "options": ["Two", "Four: settled 0s, settled 1s, unexamined, settled 2s",
                     "Three, all settled", "One"],
         "answer": 1,
         "why": "The unexamined region between mid and hi is the one people "
                "forget, and it is why the loop condition is mid <= hi."},
        {"q": "Why is the counting approach not the accepted answer?",
         "options": ["It is wrong", "It takes two passes, and does not "
                     "generalise to sorting objects by a key",
                     "It uses too much memory", "It is slower"],
         "answer": 1,
         "why": "It is correct and simple - give it first. The partition is asked "
                "for because it works on real records, not just on integers."},
    ],
)


def _three_sum_frames():
    values = sorted([-1, 0, 1, 2, -1, -4])
    out = [frame(marked(values, {i: "dim" for i in range(len(values))},
                        label="sorted first"),
                 "Sort first. That is what makes the inner search two pointers "
                 "instead of another loop, and what makes duplicates adjacent.",
                 {"fixed": "-", "found": 0})]
    found = 0
    for i in range(len(values) - 2):
        if i and values[i] == values[i - 1]:
            out.append(frame(marked(values, {j: ("bad" if j == i else "dim")
                                             for j in range(len(values))},
                                    {i: "i"}, label="values"),
                             "values[%d] repeats the previous fixed value - skip "
                             "it, or the same triple is reported twice." % i,
                             {"fixed": values[i], "found": found}))
            continue
        lo, hi = i + 1, len(values) - 1
        while lo < hi and len(out) < 8:
            total = values[i] + values[lo] + values[hi]
            marks = {j: "dim" for j in range(len(values))}
            marks[i] = "lo"
            marks[lo] = marks[hi] = "hi"
            if total == 0:
                marks[i] = marks[lo] = marks[hi] = "hit"
                found += 1
                note = "%d + %d + %d = 0 - a triple." % (values[i], values[lo], values[hi])
                lo, hi = lo + 1, hi - 1
            elif total < 0:
                note = "sum %d is too small, so move lo right." % total
                lo += 1
            else:
                note = "sum %d is too big, so move hi left." % total
                hi -= 1
            out.append(frame(marked(values, marks, {i: "i", lo if lo < len(values) else i: "lo"},
                                    label="values"),
                             note, {"fixed": values[i], "found": found}))
    return viz(out)


_q(
    slug="three-sum",
    kind="coding",
    level="Medium",
    title="3Sum",
    asked="Find all unique triples in an array that sum to zero.",
    desc="Fixing one element and two-pointering the rest gives O(n²) instead of "
         "O(n³), and sorting is what makes deduplication a skip rather than a set.",
    lead="<strong>Sort, then fix one element and two-pointer the rest.</strong> "
         "That turns the third loop into a linear scan, so the whole thing is "
         "O(n&sup2;) rather than O(n&sup3;). Sorting also puts duplicates next to "
         "each other, which is what makes deduplication a cheap skip instead of "
         "a set of tuples.",
    say="\"Sort, then for each index run two pointers over the rest looking for "
        "the complement. O(n²) time, O(1) extra space. Sorting also means "
        "duplicates are adjacent, so I skip them rather than deduplicating at "
        "the end.\"",
    notice=[
        "One element is fixed; the other two converge.",
        "A repeated fixed value is skipped, or the same triple is reported twice.",
        "The pointers only ever move inwards &mdash; that is the linear inner scan.",
    ],
    viz=_three_sum_frames(),
    sections=[
        ("Reducing the third loop",
         "<p>The brute force is three nested loops, O(n&sup3;). Fix the first "
         "element and the problem becomes \"find two numbers summing to "
         "<code>-values[i]</code>\" &mdash; which is Two Sum, and on sorted "
         "input Two Sum is two pointers in O(n).</p>"
         "<p>n iterations of an O(n) inner scan is O(n&sup2;), and the sort is "
         "O(n&nbsp;log&nbsp;n) so it disappears into that. Using a hash map for "
         "the inner search is also O(n&sup2;), and then deduplication is much "
         "harder &mdash; which is the argument for sorting.</p>"),
        ("Deduplication is the real difficulty",
         "<p>Two places need it. Skip a fixed element equal to the previous one, "
         "or every triple starting with that value is emitted twice. And after "
         "recording a triple, advance past any repeats of both pointer values, "
         "or the same triple is found again inside the same scan.</p>"
         "<p>Sorting is what makes both a simple adjacency check. Without it you "
         "would collect triples into a set of sorted tuples &mdash; correct, and "
         "it allocates for every candidate.</p>"),
        ("The early exits worth mentioning",
         "<p>Once <code>values[i] &gt; 0</code> the smallest possible triple is "
         "already positive, so the scan can stop entirely. That is not a "
         "complexity improvement and it is a large constant on real input.</p>"
         "<p>The generalisation is kSum: fix an element and recurse down to the "
         "two-pointer base case, giving O(n^(k&minus;1)). Naming that shows you "
         "see the pattern rather than the single problem.</p>"),
    ],
    code={
        "file": "three_sum.py",
        "intro": "The two-pointer version against brute force with both "
                 "operation counts, and the deduplication removed so you can see "
                 "the duplicate triples it produces.",
        "code": '''# 3Sum: sort, fix one, two-pointer the rest.

def three_sum(values):
    values = sorted(values)
    out, ops = [], 0
    for i in range(len(values) - 2):
        if values[i] > 0:
            break                              # smallest triple already positive
        if i and values[i] == values[i - 1]:
            continue                           # skip a repeated fixed value
        lo, hi = i + 1, len(values) - 1
        while lo < hi:
            ops += 1
            total = values[i] + values[lo] + values[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                out.append((values[i], values[lo], values[hi]))
                lo, hi = lo + 1, hi - 1
                while lo < hi and values[lo] == values[lo - 1]:
                    lo += 1                    # and skip repeated pointer values
                while lo < hi and values[hi] == values[hi + 1]:
                    hi -= 1
    return out, ops


def no_dedup(values):
    """The same scan without any of the skips."""
    values = sorted(values)
    out = []
    for i in range(len(values) - 2):
        lo, hi = i + 1, len(values) - 1
        while lo < hi:
            total = values[i] + values[lo] + values[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                out.append((values[i], values[lo], values[hi]))
                lo, hi = lo + 1, hi - 1
    return out


def brute_force(values):
    out, ops = set(), 0
    n = len(values)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                ops += 1
                if values[i] + values[j] + values[k] == 0:
                    out.add(tuple(sorted((values[i], values[j], values[k]))))
    return sorted(out), ops


data = [-1, 0, 1, 2, -1, -4]
triples, ops = three_sum(data)
brute, brute_ops = brute_force(data)
print("input :", data)
print("triples:", triples, f"({ops} pointer steps)")
print("brute  :", brute, f"({brute_ops} triples examined)")
print("agree  :", sorted(triples) == brute)

print()
dupes = [-2, 0, 0, 2, 2, -2, 0]
print("input with repeats :", dupes)
print("with dedup         :", three_sum(dupes)[0])
print("without dedup      :", no_dedup(dupes))
print("The same triple comes out several times once the skips are gone.")

# --- how the two costs diverge -----------------------------------------
print()
import random
random.seed(4)
for n in (60, 120, 240):
    sample = [random.randint(-50, 50) for _ in range(n)]
    _, fast_ops = three_sum(sample)
    _, slow_ops = brute_force(sample)
    print(f"  n={n:>3}: two pointers {fast_ops:>6,} steps   brute force {slow_ops:>9,}")
''',
        "walk": [
            ("if i and values[i] == values[i - 1]: continue",
             "The first deduplication. Without it, every triple beginning with a "
             "repeated value is emitted once per repeat."),
            ("while lo < hi and values[lo] == values[lo - 1]: lo += 1",
             "The second. After recording a triple, both pointers must move past "
             "any repeats or the same triple is found again in the same scan."),
            ("if values[i] > 0: break",
             "On sorted input, once the fixed element is positive the smallest "
             "possible triple already exceeds zero. Not a complexity change, and "
             "a large constant."),
            ("lo, hi = i + 1, len(values) - 1",
             "The inner search is Two Sum on a sorted range, which is why fixing "
             "one element removes an entire loop rather than just reordering the "
             "work."),
        ],
        "try": [
            "Change the target from 0 to 6 by adjusting the comparisons. The "
            "structure is unchanged; only the constant moves.",
            "Extend it to 4Sum by fixing two elements. O(n&sup3;), and the "
            "deduplication now needs a skip at both fixed levels.",
        ],
    },
    check=[
        {"q": "Fixing one element reduces 3Sum from O(n³) to O(n²) because the "
              "inner search becomes:",
         "options": ["A binary search", "Two Sum, which is O(n) on sorted input",
                     "A hash lookup", "A sort"],
         "answer": 1,
         "why": "n iterations of a linear inner scan is O(n²). The sort is "
                "O(n log n) and disappears into that."},
        {"q": "Why sort rather than use a hash map for the inner search?",
         "options": ["It is faster", "Sorting makes duplicates adjacent, so "
                     "deduplication is a skip rather than a set of tuples",
                     "Hash maps do not work here", "It uses less memory"],
         "answer": 1,
         "why": "Both are O(n²). Deduplication is the real difficulty of this "
                "problem, and adjacency is what makes it cheap."},
        {"q": "How many places need a duplicate skip?",
         "options": ["One - the fixed element", "Two - the fixed element and "
                     "both pointers after a hit",
                     "Three", "None, if you use a set"],
         "answer": 1,
         "why": "Skipping only the fixed value still finds the same triple twice "
                "within one inner scan."},
    ],
)


def _rotated_frames():
    values = [4, 5, 6, 7, 0, 1, 2]
    target = 0
    out = []
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        marks = {i: ("dim" if i < lo or i > hi else "lo") for i in range(len(values))}
        marks[mid] = "hit" if values[mid] == target else "bad"
        left_sorted = values[lo] <= values[mid]
        if values[mid] == target:
            out.append(frame(marked(values, marks, {mid: "mid"}, label="rotated"),
                             "a[mid] = %d is the target." % target,
                             {"lo": lo, "hi": hi, "mid": mid}))
            break
        if left_sorted:
            takes_left = values[lo] <= target < values[mid]
            note = ("Left half %s is sorted, and %d %s in its range - so search %s."
                    % (values[lo:mid + 1], target,
                       "is" if takes_left else "is not",
                       "left" if takes_left else "right"))
            if takes_left:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            takes_right = values[mid] < target <= values[hi]
            note = ("Right half %s is sorted, and %d %s in its range - so search %s."
                    % (values[mid:hi + 1], target,
                       "is" if takes_right else "is not",
                       "right" if takes_right else "left"))
            if takes_right:
                lo = mid + 1
            else:
                hi = mid - 1
        out.append(frame(marked(values, marks, {mid: "mid"}, label="rotated"),
                         note, {"lo": lo, "hi": hi, "mid": mid}))
    return viz(out)


_q(
    slug="search-in-rotated-sorted-array",
    kind="coding",
    level="Medium",
    title="Search in a rotated sorted array",
    asked="A sorted array has been rotated at an unknown pivot. Find a target in "
          "O(log n).",
    desc="Binary search still applies because one half is always sorted - the "
         "trick is deciding which half, and whether the target lies inside it.",
    lead="Binary search still works, because after any rotation <strong>at least "
         "one half is still sorted</strong>. Compare the ends to find which, "
         "then check whether the target falls inside that half's range: if it "
         "does, search there; if not, search the other. Still O(log n).",
    say="\"One half is always sorted - compare a[lo] with a[mid] to see which. "
        "Then check if the target is inside that sorted half's range and discard "
        "accordingly. O(log n), no pre-pass to find the pivot.\"",
    notice=[
        "One side of <code>mid</code> is always in order.",
        "The decision is about the sorted half's <em>range</em>, not about mid alone.",
        "The window halves every step, exactly as in plain binary search.",
    ],
    viz=_rotated_frames(),
    sections=[
        ("Why binary search survives rotation",
         "<p>A rotation splits the array into two sorted runs. Wherever "
         "<code>mid</code> lands, it is inside one of them &mdash; so at least "
         "one of <code>[lo, mid]</code> and <code>[mid, hi]</code> is entirely "
         "in order. That is the invariant the whole solution rests on, and it "
         "holds for any rotation amount including zero.</p>"
         "<p><code>values[lo] &lt;= values[mid]</code> identifies which. Use "
         "<code>&lt;=</code>, not <code>&lt;</code>: when <code>lo == mid</code> "
         "the left half is a single element and is trivially sorted.</p>"),
        ("The decision that follows",
         "<p>Having found a sorted half, you can test membership by range rather "
         "than by searching. If the target lies between that half's endpoints, "
         "it can only be there. If it does not, it can only be in the other "
         "half. Either way one half is discarded per step.</p>"
         "<p>The bounds matter: <code>values[lo] &lt;= target &lt; "
         "values[mid]</code> on the left, and <code>values[mid] &lt; target "
         "&lt;= values[hi]</code> on the right. <code>mid</code> has already "
         "been compared, so it is excluded on both sides.</p>"),
        ("The duplicates variant",
         "<p>With duplicates allowed, <code>values[lo] == values[mid] == "
         "values[hi]</code> tells you nothing about which half is sorted, and "
         "the only safe move is to shrink the window by one. That makes the "
         "worst case O(n) &mdash; and it is a genuine lower bound, not a lazy "
         "implementation.</p>"
         "<p>Saying \"O(log n), but O(n) worst case if duplicates are allowed\" "
         "is the complete answer, and the follow-up interviewers reach for when "
         "the first part goes smoothly.</p>"),
    ],
    code={
        "file": "rotated_search.py",
        "intro": "The search with each decision printed, checked against a "
                 "linear scan at every rotation of the same array, plus the "
                 "duplicates variant and its O(n) case.",
        "code": '''# Search a rotated sorted array: one half is always in order.

def search(values, target, show=False):
    lo, hi = 0, len(values) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if values[mid] == target:
            return mid
        if values[lo] <= values[mid]:                 # left half is sorted
            if values[lo] <= target < values[mid]:
                if show: print(f"    target in sorted left {values[lo:mid+1]}")
                hi = mid - 1
            else:
                if show: print(f"    not in sorted left {values[lo:mid+1]}")
                lo = mid + 1
        else:                                          # right half is sorted
            if values[mid] < target <= values[hi]:
                if show: print(f"    target in sorted right {values[mid:hi+1]}")
                lo = mid + 1
            else:
                if show: print(f"    not in sorted right {values[mid:hi+1]}")
                hi = mid - 1
    return -1


data = [4, 5, 6, 7, 0, 1, 2]
print("array:", data, " looking for 0")
print("index:", search(data, 0, show=True))

# Correct at every rotation, for every value, including absent ones.
print()
base = [0, 1, 2, 4, 5, 6, 7]
failures = 0
for r in range(len(base)):
    rotated = base[r:] + base[:r]
    for target in base + [3, 99]:
        got = search(rotated, target)
        want = rotated.index(target) if target in rotated else -1
        if got != want:
            failures += 1
            print("  MISMATCH", rotated, target, got, want)
print(f"all rotations x all targets: {failures} mismatches")

# --- with duplicates, the guarantee weakens ----------------------------
def search_with_duplicates(values, target):
    lo, hi = 0, len(values) - 1
    steps = 0
    while lo <= hi:
        steps += 1
        mid = (lo + hi) // 2
        if values[mid] == target:
            return mid, steps
        if values[lo] == values[mid] == values[hi]:
            lo += 1                      # cannot tell which half is sorted
            hi -= 1
        elif values[lo] <= values[mid]:
            if values[lo] <= target < values[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if values[mid] < target <= values[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1, steps

print()
nasty = [2] * 12 + [1] + [2] * 12
index, steps = search_with_duplicates(nasty, 1)
print(f"25 elements, almost all equal: found at {index} after {steps} steps")
print("That is O(n), not O(log n) - and it is a real lower bound, because")
print("a[lo] == a[mid] == a[hi] tells you nothing about where the pivot is.")
''',
        "walk": [
            ("if values[lo] <= values[mid]:",
             "Identifies the sorted half. <code>&lt;=</code> rather than "
             "<code>&lt;</code> because when <code>lo == mid</code> the left half "
             "is one element, which is sorted."),
            ("values[lo] <= target < values[mid]",
             "Membership by range, not by search. If the target is inside the "
             "sorted half's endpoints it can only be there; otherwise it can "
             "only be in the other half."),
            ("mid excluded on both sides",
             "<code>hi = mid - 1</code> and <code>lo = mid + 1</code>. "
             "<code>mid</code> has already been compared, and leaving it in the "
             "window is the usual way to write an infinite loop here."),
            ("values[lo] == values[mid] == values[hi]",
             "The duplicates case, where nothing can be deduced and the only "
             "safe move is to shrink by one. That is what makes the worst case "
             "O(n)."),
        ],
        "try": [
            "Rotate by zero &mdash; a plain sorted array. The left half is "
            "always the sorted one and it degenerates to ordinary binary search.",
            "Find the pivot first with its own binary search, then do a normal "
            "search in the right run. Two passes, same complexity, and easier to "
            "reason about.",
        ],
    },
    check=[
        {"q": "Why does binary search still apply after rotation?",
         "options": ["The array is still sorted", "At least one half of the "
                     "window is always in order",
                     "Rotation preserves indices", "It does not - you must sort first"],
         "answer": 1,
         "why": "A rotation makes two sorted runs, so mid always falls inside "
                "one of them. Identifying which is the whole trick."},
        {"q": "Having identified the sorted half, you decide where to search by:",
         "options": ["Comparing the target with mid", "Checking whether the "
                     "target lies within that half's endpoint range",
                     "Searching both halves", "Comparing with a[0]"],
         "answer": 1,
         "why": "In a sorted range, membership is a range check. If it is not in "
                "there, it can only be in the other half."},
        {"q": "With duplicates allowed, the worst case becomes:",
         "options": ["Still O(log n)", "O(n), because a[lo] == a[mid] == a[hi] "
                     "reveals nothing",
                     "O(n log n)", "Impossible"],
         "answer": 1,
         "why": "The only safe move is to shrink the window by one. This is a "
                "genuine lower bound and the standard follow-up question."},
    ],
)


def _window_max_frames():
    values = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    from collections import deque
    dq = deque()
    out = []
    for i, v in enumerate(values):
        dropped = []
        while dq and values[dq[-1]] <= v:
            dropped.append(values[dq.pop()])
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        marks = {j: ("dim" if j > i or j <= i - k else "lo") for j in range(len(values))}
        if dq:
            marks[dq[0]] = "hit"
        note = ("%d arrives. " % v) + (
            "It beats %s, which can never be a maximum again - drop them. "
            % dropped if dropped else "Nothing smaller behind it. ")
        if i >= k - 1:
            note += "Window max is %d." % values[dq[0]]
        out.append(frame([marked(values, marks, {i: "i"}, label="values"),
                          marked([str(values[j]) for j in dq],
                                 {0: "hit"}, label="deque (indices, decreasing)")],
                         note, {"i": i, "max": values[dq[0]] if i >= k - 1 else "-"}))
        if len(out) >= 7:
            break
    return viz(out)


_q(
    slug="sliding-window-maximum",
    kind="coding",
    level="Hard",
    title="Sliding window maximum",
    asked="Return the maximum of every window of size k as it slides along the "
          "array.",
    desc="A monotonic deque keeps the answer at its front in O(n) total, and the "
         "insight is that a smaller value behind a larger one can never be a "
         "maximum again.",
    lead="Keep a <strong>deque of indices whose values are decreasing</strong>. "
         "When a new value arrives, everything smaller behind it is discarded "
         "&mdash; those can never be a maximum again, because the newcomer is "
         "bigger and outlives them. The front is always the current window's "
         "maximum. O(n) total.",
    say="\"Monotonic deque of indices, values decreasing. A new value evicts "
        "everything smaller from the back, because they can never win again. The "
        "front is the answer, and I drop it once it falls out of the window. "
        "Every index is pushed and popped once, so O(n).\"",
    notice=[
        "Smaller values behind a larger one are discarded immediately.",
        "The front is the answer without any scanning.",
        "Indices are stored, not values &mdash; that is how expiry is detected.",
    ],
    viz=_window_max_frames(),
    sections=[
        ("The observation that does the work",
         "<p>If <code>a[j]</code> comes before <code>a[i]</code> and "
         "<code>a[j] &le; a[i]</code>, then <code>a[j]</code> can never be the "
         "maximum of any future window &mdash; every window containing it from "
         "now on also contains the bigger, later <code>a[i]</code>. So it can be "
         "thrown away the moment <code>a[i]</code> arrives.</p>"
         "<p>What survives is a decreasing sequence, and its front is the "
         "maximum of the current window by construction. No scan is ever "
         "needed.</p>"),
        ("Why indices rather than values",
         "<p>The front must be discarded once it falls out of the window, and "
         "that needs its position. Storing values leaves no way to tell an "
         "expired maximum from a current one.</p>"
         "<p>The expiry check is <code>dq[0] &lt;= i - k</code> &mdash; the "
         "front is older than the window's left edge. This is the other place "
         "an off-by-one lives, and it is worth writing out the first window's "
         "indices to check it.</p>"),
        ("Why it is O(n), not O(n·k)",
         "<p>The inner <code>while</code> can pop several entries in one "
         "iteration, which looks quadratic. But each index is pushed exactly "
         "once and popped at most once across the entire run, so the total pops "
         "are bounded by n.</p>"
         "<p>The alternatives are worth naming: recomputing <code>max</code> per "
         "window is O(n&middot;k), and a heap is O(n&nbsp;log&nbsp;k) and needs "
         "lazy deletion because you cannot remove an arbitrary element. The "
         "deque beats both.</p>"),
    ],
    code={
        "file": "window_max.py",
        "intro": "The deque version with its total push and pop counts against "
                 "the recompute-every-window version, on an input sized to make "
                 "O(n) against O(n&middot;k) unmistakable.",
        "code": '''# Sliding window maximum: a deque of indices with decreasing values.
from collections import deque
import time

def window_max(values, k, show=False):
    dq = deque()                             # indices, values decreasing
    out, pushes, pops = [], 0, 0
    for i, v in enumerate(values):
        while dq and values[dq[-1]] <= v:    # smaller behind: can never win
            dq.pop()
            pops += 1
        dq.append(i)
        pushes += 1
        if dq[0] <= i - k:                   # the front has expired
            dq.popleft()
            pops += 1
        if i >= k - 1:
            out.append(values[dq[0]])        # the front IS the maximum
            if show:
                print(f"    window {values[i-k+1:i+1]} -> max {values[dq[0]]}")
    return out, pushes, pops


def recompute(values, k):
    out, comparisons = [], 0
    for i in range(len(values) - k + 1):
        window = values[i:i + k]
        comparisons += len(window)
        out.append(max(window))
    return out, comparisons


values, k = [1, 3, -1, -3, 5, 3, 6, 7], 3
print(f"values {values}, k={k}")
answer, pushes, pops = window_max(values, k, show=True)
print("  maxima:", answer)
print(f"  {pushes} pushes, {pops} pops for {len(values)} elements")
print("  recompute agrees:", recompute(values, k)[0] == answer)

# --- how the two costs diverge as k grows ------------------------------
import random
random.seed(9)
big = [random.randint(0, 1000) for _ in range(15_000)]
print()
print(f"n = {len(big):,}")
for k in (10, 100, 400):
    start = time.time()
    a, pushes, pops = window_max(big, k)
    deque_time = time.time() - start

    start = time.time()
    b, comparisons = recompute(big, k)
    naive_time = time.time() - start

    print(f"  k={k:>4}: deque {deque_time:.3f}s ({pushes + pops:,} ops)   "
          f"recompute {naive_time:.3f}s ({comparisons:,} ops)   same: {a == b}")

print()
print("The deque's operation count barely moves with k. The naive one is")
print("proportional to it, because every window is rebuilt from scratch.")
''',
        "walk": [
            ("while dq and values[dq[-1]] <= v: dq.pop()",
             "The eviction. Anything smaller sitting behind a newer, larger "
             "value is permanently useless, because every future window holding "
             "it also holds the newcomer."),
            ("dq[0] <= i - k",
             "Expiry by position, which is why indices are stored rather than "
             "values. Storing values leaves no way to tell a stale maximum from "
             "a live one."),
            ("out.append(values[dq[0]])",
             "No scan. The deque is decreasing by construction, so its front is "
             "the window maximum &mdash; that is the entire payoff."),
            ("pushes and pops",
             "Each index enters once and leaves at most once, so the totals are "
             "bounded by n however aggressive the inner loop looks. That is the "
             "amortised argument, measured."),
        ],
        "try": [
            "Set <code>k = 1</code>. The deque never holds more than one entry "
            "and the answer is the input &mdash; a good sanity check on the "
            "expiry condition.",
            "Change <code>&lt;=</code> to <code>&lt;</code> in the eviction. "
            "Equal values are now kept, which is still correct and grows the "
            "deque for no benefit.",
        ],
    },
    check=[
        {"q": "Why can a smaller value behind a larger one be discarded?",
         "options": ["To save memory", "Every future window containing it also "
                     "contains the larger, later value",
                     "It is already counted", "It cannot be"],
         "answer": 1,
         "why": "It can never be a maximum again, so keeping it is pure waste. "
                "That observation is the whole algorithm."},
        {"q": "Why store indices in the deque rather than values?",
         "options": ["Indices are smaller", "The front must be expired once it "
                     "falls outside the window, which needs its position",
                     "Values are not hashable", "It makes no difference"],
         "answer": 1,
         "why": "Without positions there is no way to distinguish a stale "
                "maximum from a current one."},
        {"q": "The algorithm is O(n) rather than O(n·k) because:",
         "options": ["k is small", "Each index is pushed once and popped at most "
                     "once across the whole run",
                     "The deque is sorted", "max() is O(1)"],
         "answer": 1,
         "why": "The inner while loop can pop several entries at once, but the "
                "total pops are bounded by n."},
    ],
)


def _containers_frames():
    return viz([
        frame(pairs([("list", "ordered, mutable, O(1) index, O(n) at the front"),
                     ("tuple", "ordered, immutable, hashable if its items are"),
                     ("deque", "O(1) at BOTH ends, O(n) index"),
                     ("array", "packed values, not pointers - far less memory"),
                     ("set", "O(1) membership, no order, no duplicates")],
                    {"list": "lo"}, label="the five"),
              "Five containers, five different trade-offs. The question is "
              "always which operation you do most.",
              {"choices": 5}),
        frame(pairs([("append / pop at the end", "list or deque"),
                     ("insert / pop at the FRONT", "deque - a list is O(n)"),
                     ("random access by index", "list - a deque is O(n)"),
                     ("membership testing", "set or dict"),
                     ("a dictionary key", "tuple - a list is unhashable"),
                     ("millions of numbers", "array or numpy")],
                    {"insert / pop at the FRONT": "hit"}, label="pick by operation"),
              "Choose by the operation you repeat, not by habit. The front of a "
              "list is the one people get wrong.",
              {"choices": 6}),
        frame(pairs([("list of 1000 ints", "~8 KB of pointers + the ints"),
                     ("array('i', ...)", "~4 KB, values packed inline"),
                     ("tuple", "slightly smaller than the list, fixed size")],
                    {"array('i', ...)": "hit"}, label="memory"),
              "A list stores references. An array stores the values themselves, "
              "which is why it is smaller and why it can only hold one type.",
              {"choices": 3}),
    ])


_q(
    slug="list-versus-tuple-versus-deque",
    kind="concept",
    level="Easy",
    title="list vs tuple vs deque vs array — which and why?",
    asked="When would you use a tuple instead of a list? What about deque or "
          "array?",
    desc="Choosing a Python container by the operation you repeat: mutability, "
         "hashability, which end you touch, and where the memory goes.",
    lead="Pick by the operation you do most. <strong>list</strong> for ordered "
         "mutable data with random access; <strong>tuple</strong> when it must "
         "not change or must be a dict key; <strong>deque</strong> when you touch "
         "the front; <strong>array</strong> when you have millions of numbers; "
         "<strong>set</strong> when you only ask \"is it in there?\".",
    say="\"Tuple if it's fixed or needs to be hashable - it can be a dict key, a "
        "list can't. deque if I'm touching the front, because list.pop(0) is "
        "O(n). array or numpy for large numeric data, since a list stores "
        "pointers rather than values.\"",
    notice=[
        "The front of a list is the trap &mdash; O(n), where a deque is O(1).",
        "Hashability is the real tuple/list distinction, not immutability for "
        "its own sake.",
        "An array stores values; a list stores references to them.",
    ],
    viz=_containers_frames(),
    sections=[
        ("tuple versus list",
         "<p>The textbook answer is \"tuples are immutable\", which is true and "
         "not the point. The consequence is that a tuple is <strong>hashable</strong> "
         "(if its contents are), so it can be a dictionary key or a set member "
         "&mdash; which is why coordinates, database rows and cache keys are "
         "tuples.</p>"
         "<p>The secondary signal is meaning. A list is a homogeneous sequence "
         "of unknown length; a tuple is a fixed-size record where position "
         "carries meaning. <code>(x, y)</code> is a point; "
         "<code>[x, y]</code> is two numbers.</p>"),
        ("deque versus list",
         "<p><code>collections.deque</code> is a doubly linked list of blocks, "
         "so <code>appendleft</code> and <code>popleft</code> are O(1) where the "
         "list equivalents are O(n). Any queue, BFS frontier or "
         "\"last N items\" buffer should be a deque.</p>"
         "<p>The trade is random access: <code>d[5000]</code> walks the blocks, "
         "so it is O(n). If you index into the middle, keep the list. A deque "
         "also takes <code>maxlen</code>, which turns it into a fixed-size ring "
         "buffer that discards the oldest entry automatically.</p>"),
        ("array and the memory question",
         "<p>A list holds <em>references</em>, so a list of a million integers is "
         "a million pointers plus a million integer objects. "
         "<code>array.array</code> packs the values inline in one typed block, "
         "which is several times smaller and much friendlier to the cache.</p>"
         "<p>For real numeric work the answer is <code>numpy</code>, which adds "
         "vectorised operations on top of the same packed layout. Mentioning "
         "that a list of numbers is a list of pointers is usually the specific "
         "thing an interviewer is listening for.</p>"),
    ],
    code={
        "file": "containers.py",
        "intro": "The five containers measured rather than described: the "
                 "operation each is fast at, the memory each uses for the same "
                 "thousand integers, and the two errors that pick the container "
                 "for you.",
        "code": '''# Choosing a container: measure the operation you actually repeat.
import sys, time
from array import array
from collections import deque

N = 30_000
print(f"{'operation':>28} {'list':>10} {'deque':>10}")
for label, action_list, action_deque in [
    ("append at the end",  lambda c: c.append(1),   lambda c: c.append(1)),
    ("insert at the front", lambda c: c.insert(0, 1), lambda c: c.appendleft(1)),
]:
    lst, dq = [], deque()
    start = time.time(); [action_list(lst) for _ in range(N)]
    list_time = time.time() - start
    start = time.time(); [action_deque(dq) for _ in range(N)]
    deque_time = time.time() - start
    print(f"{label:>28} {list_time:>9.4f}s {deque_time:>9.4f}s")

# Random access is the other direction.
lst = list(range(N)); dq = deque(range(N))
start = time.time(); [lst[N // 2] for _ in range(100_000)]
print(f"{'index the middle':>28} {time.time() - start:>9.4f}s", end="")
start = time.time(); [dq[N // 2] for _ in range(100_000)]
print(f" {time.time() - start:>9.4f}s   <- deque loses here")

# --- memory: references versus packed values ---------------------------
numbers = list(range(1000))
packed = array("i", range(1000))
as_tuple = tuple(range(1000))
print()
print(f"list  of 1000 ints : {sys.getsizeof(numbers):>6} bytes (references)")
print(f"tuple of 1000 ints : {sys.getsizeof(as_tuple):>6} bytes")
print(f"array of 1000 ints : {sys.getsizeof(packed):>6} bytes (values, packed)")
print("The list does not include the integer objects it points at.")

# --- the two errors that decide it for you -----------------------------
print()
try:
    {[1, 2]: "point"}
except TypeError as e:
    print("list as a dict key  ->", e)
print("tuple as a dict key ->", {(1, 2): "point"})

try:
    (1, 2).append(3)
except AttributeError as e:
    print("tuple.append        ->", e)

# --- deque with maxlen is a ring buffer --------------------------------
print()
recent = deque(maxlen=3)
for event in "abcde":
    recent.append(event)
print("deque(maxlen=3) after abcde:", list(recent), "- oldest dropped for free")
''',
        "walk": [
            ("lst.insert(0, 1) versus dq.appendleft(1)",
             "The same logical operation, O(n) against O(1). Doing it in a loop "
             "is the most common accidental quadratic in Python, and it usually "
             "appears as a hand-rolled queue."),
            ("dq[N // 2]",
             "Where the deque loses. It is a linked list of blocks, so indexing "
             "into the middle walks them. If you index, keep the list."),
            ("sys.getsizeof(numbers) versus the array",
             "A list stores references; an array stores the values. That is why "
             "the array is smaller and why it can hold only one type &mdash; and "
             "it is the specific point interviewers listen for."),
            ("deque(maxlen=3)",
             "A fixed-size ring buffer for free: appending past the limit drops "
             "the oldest. That is the \"last N events\" structure, without any "
             "bookkeeping."),
        ],
        "try": [
            "Compare <code>sys.getsizeof</code> for a list and a tuple of the "
            "same items. The tuple is smaller because it never has to leave "
            "growth room.",
            "Build a numpy array of a million floats and compare with a list. "
            "The gap is much larger than the array module's.",
        ],
    },
    check=[
        {"q": "The most practical difference between a tuple and a list is that "
              "a tuple:",
         "options": ["Is faster", "Is hashable, so it can be a dict key or set "
                     "member",
                     "Uses less memory", "Cannot hold mixed types"],
         "answer": 1,
         "why": "Immutability is the mechanism; hashability is the consequence "
                "you actually reach for. It is why coordinates and cache keys "
                "are tuples."},
        {"q": "You need a queue. Which container?",
         "options": ["list, using pop(0)", "deque, using popleft()", "tuple",
                     "set"],
         "answer": 1,
         "why": "pop(0) shifts every remaining element, so it is O(n) each and "
                "O(n²) overall. deque is O(1) at both ends."},
        {"q": "array.array uses less memory than a list of the same integers "
              "because it:",
         "options": ["Compresses them", "Stores the values inline rather than "
                     "references to objects",
                     "Uses fewer bits per number", "Shares objects"],
         "answer": 1,
         "why": "A list of a million numbers is a million pointers plus a "
                "million objects. The trade is that an array holds one type only."},
    ],
)
