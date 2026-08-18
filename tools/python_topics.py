# -*- coding: utf-8 -*-
"""Content for the generated Python modules.

The Python track was the thinnest on the site - twelve modules against
Algorithms' forty-one - and the gaps were not obscure corners but whole
categories a beginner meets in their first week: tuples, sets, and everything
about functions past `return`.

These are generated rather than hand-written because ten pages of the same
shape should not be ten opportunities to drift. The shape matches the
hand-written twelve: two runnable programs, a notes column, the article, and
the questions.

Every program here is written to be *run*, not read - each prints something
that answers the question the page is about, and several are deliberately
built so the output contradicts the guess a beginner would make.

The deep-dive labs in dsa/ and the "why is it like that" questions in
interview/ already exist; this track stays on how to write the thing.
"""

TOPICS = []


def topic(slug, title, cat, lead, svg, programs, notes, article, check):
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "programs": programs, "notes": notes, "article": article, "check": check,
    })


A = "var(--accent-primary)"
M = "var(--text-muted)"
B = "var(--border-subtle)"
S = "var(--bg-surface)"


def _svg(body):
    return '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s</svg>' % body


def _box(x, y, w, h, fill="none", stroke=B, sw=2, rx=3):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, fill, stroke, sw))


def _txt(x, y, s, fill=M, size=9, anchor="middle", weight="normal"):
    return ('<text x="%s" y="%s" fill="%s" font-size="%s" font-family="monospace" '
            'text-anchor="%s" font-weight="%s">%s</text>'
            % (x, y, fill, size, anchor, weight, s))


# ---------------------------------------------------------------------------
# 1. Tuples and unpacking
# ---------------------------------------------------------------------------
topic(
    "tuples_and_unpacking",
    "Tuples and Unpacking",
    "Fixed Collections",
    "A sequence that cannot be changed after it is built, and the syntax that "
    "takes one apart in a single line.",
    _svg(_box(18, 32, 54, 26, S) + _txt(45, 49, "(1, 2)", A) +
         '<path d="M78 45 L96 45" stroke="%s" stroke-width="2"/>' % M +
         _box(100, 24, 20, 18, S) + _txt(110, 37, "a") +
         _box(100, 48, 20, 18, S) + _txt(110, 61, "b")),
    [("tuples.py", '''# A tuple is a sequence you cannot change afterwards.
point = (3, 4)
print("point   :", point)
print("first   :", point[0])
print("length  :", len(point))

# Unpacking: give each position a name, in one line.
x, y = point
print("x, y    :", x, y)

# The classic use: swap without a temporary variable.
a, b = 1, 2
a, b = b, a
print("swapped :", a, b)

# Trying to change one raises. Uncomment to see the error.
# point[0] = 99
'''),
     ("why_tuples.py", '''# A tuple can be a dictionary key. A list cannot.
scores = {}
scores[(0, 0)] = "origin"
scores[(1, 2)] = "somewhere else"
print(scores)

try:
    scores[[0, 0]] = "nope"
except TypeError as e:
    print("list as key ->", e)

# Functions return tuples all the time; unpacking reads them nicely.
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([8, 3, 9, 1])
print("low, high:", low, high)

# One-element tuples need the comma. This trips everyone up once.
print(type((5)))    # int  - just brackets
print(type((5,)))   # tuple
'''),
     ],
    ["A tuple is written with commas, not brackets. <code class='mono-font'>1, 2</code> "
     "is already a tuple; the brackets only group it.",
     "Immutable means the tuple cannot be re-pointed, so it can be a dict key "
     "or a set member. A list cannot.",
     "<code class='mono-font'>a, b = b, a</code> builds a tuple on the right, then "
     "unpacks it. That is why the swap needs no temporary.",
     "One element needs a trailing comma: <code class='mono-font'>(5,)</code>. "
     "Without it you have brackets round a number."],
    """title: Tuples and Unpacking: A Practical Guide
intro: A tuple is a sequence that cannot be changed once built. That single restriction is what makes it usable as a dictionary key, safe to hand around, and the natural way to return more than one value.

## The difference that matters

A list and a tuple both hold an ordered run of items, and both index the same way. The difference is one word: a tuple is immutable. Once it exists, no element can be replaced.

point = (3, 4)<br>point[0] = 99&nbsp;&nbsp;# TypeError

That sounds like a limitation and is mostly a guarantee. If you hand a list to a function, the function can change it under you. Hand it a tuple and it cannot.

## Why immutability buys you a dictionary key

A dictionary key has to be hashable, which in practice means it must never change &mdash; if it changed, the dictionary would look for it in the wrong place. Lists are mutable, so they are unhashable, so they cannot be keys. Tuples can.

grid[(2, 3)] = "wall"

That is how you key anything by a coordinate pair, a date triple, or any other small fixed group.

## Unpacking is the point

Unpacking assigns each position to a name in one statement:

x, y = point

It is not a special tuple feature &mdash; it works on any sequence &mdash; but tuples are where you meet it. The number of names must match the number of items, or Python raises `ValueError`, which is a feature: it catches the case where the shape you expected is not the shape you got.

The swap idiom falls straight out of it:

a, b = b, a

The right-hand side is evaluated first, into a tuple, and only then unpacked. No temporary variable, and no ordering bug.

## Returning more than one thing

Python has no special syntax for multiple return values because it does not need any. `return min(xs), max(xs)` returns a tuple, and the caller unpacks it:

low, high = min_max(values)

This reads better than returning a list, because the shape is fixed: exactly two things, in a known order.

## The comma is the tuple

The most common surprise is that brackets do not make a tuple &mdash; commas do.

type((5))&nbsp;&nbsp;&nbsp;# int<br>type((5,))&nbsp;&nbsp;# tuple

A single-element tuple needs the trailing comma. It looks like a typo and is not. This bites when a function is supposed to return one item as a tuple and quietly returns the item instead.

## When to reach for which

Use a list when the collection will grow, shrink or be sorted in place. Use a tuple when the group is fixed at creation and its positions mean something: a coordinate, an RGB colour, a row from a database. If you find yourself never mutating a list, a tuple states that intent and gets you hashability for free.
""",
    [{"q": "Why can a tuple be a dictionary key when a list cannot?",
      "options": ["Tuples are smaller", "Tuples are hashable because they cannot change",
                  "Lists are too slow", "Dictionaries only accept brackets"],
      "answer": 1,
      "why": "A key must hash to the same value forever. A list can change after "
             "insertion, so the dictionary would look in the wrong place; Python "
             "prevents that by making lists unhashable."},
     {"q": "What is `type((5))`?",
      "options": ["tuple", "int", "list", "SyntaxError"],
      "answer": 1,
      "why": "The comma makes a tuple, not the brackets. `(5)` is just 5 in "
             "brackets; `(5,)` is a one-element tuple."},
     {"q": "In `a, b = b, a`, why is no temporary variable needed?",
      "options": ["Python swaps in place", "The right side becomes a tuple first, "
                  "then is unpacked", "Assignment happens left to right",
                  "It only works for numbers"],
      "answer": 1,
      "why": "Python evaluates the whole right-hand side into a tuple before "
             "assigning anything, so both old values are safely captured."}],
)


# ---------------------------------------------------------------------------
# 2. Sets and set operations
# ---------------------------------------------------------------------------
topic(
    "sets_and_set_operations",
    "Sets and Set Operations",
    "Unique Things",
    "A collection with no duplicates and no order, built for membership tests "
    "and for comparing two groups.",
    _svg('<circle cx="62" cy="45" r="26" fill="%s" fill-opacity="0.25" stroke="%s" stroke-width="2"/>' % (A, A) +
         '<circle cx="98" cy="45" r="26" fill="none" stroke="%s" stroke-width="2"/>' % M +
         _txt(46, 49, "A", A) + _txt(114, 49, "B") + _txt(80, 49, "&amp;", A)),
    [("sets.py", '''# A set drops duplicates and does not keep order.
seen = {"red", "green", "red", "blue"}
print("set     :", seen)
print("size    :", len(seen))

# Deduplicating a list is a one-liner.
votes = ["ana", "bo", "ana", "cy", "bo", "ana"]
print("unique  :", set(votes))
print("how many:", len(set(votes)))

# Membership is the reason sets exist.
print("'ana' in votes?", "ana" in set(votes))

# Sets are unordered: no indexing.
try:
    seen[0]
except TypeError as e:
    print("indexing ->", e)
'''),
     ("set_algebra.py", '''# Comparing two groups is what set operators are for.
python = {"ana", "bo", "cy", "dee"}
sql    = {"bo", "dee", "eve"}

print("both       :", python & sql)          # intersection
print("either     :", python | sql)          # union
print("python only:", python - sql)          # difference
print("exactly one:", python ^ sql)          # symmetric difference

# The same thing with loops, for comparison.
both = []
for name in python:
    if name in sql:
        both.append(name)
print("by hand    :", set(both))

# Membership on a big collection: set beats list, decisively.
import time
big_list = list(range(200_000))
big_set = set(big_list)
target = 199_999

t0 = time.perf_counter()
target in big_list
list_ms = (time.perf_counter() - t0) * 1000

t0 = time.perf_counter()
target in big_set
set_ms = (time.perf_counter() - t0) * 1000

print(f"list scan  : {list_ms:.3f} ms")
print(f"set lookup : {set_ms:.3f} ms")
'''),
     ],
    ["<code class='mono-font'>{}</code> is an empty dict, not an empty set. "
     "Use <code class='mono-font'>set()</code>.",
     "No duplicates and no order. If order matters, a set is the wrong container.",
     "<code class='mono-font'>&amp;</code> intersection, <code class='mono-font'>|</code> union, "
     "<code class='mono-font'>-</code> difference, <code class='mono-font'>^</code> in one but not both.",
     "Membership is roughly constant time on a set and a full scan on a list. "
     "That gap is the whole reason to convert."],
    """title: Sets and Set Operations: A Practical Guide
intro: A set holds unique items in no particular order. That trade &mdash; giving up order and duplicates &mdash; buys near-instant membership tests and a small algebra for comparing two groups.

## What a set gives up, and what it buys

Write a set with braces:

seen = {"red", "green", "red", "blue"}

Three items come out, not four: duplicates collapse silently. Print it twice and the order may differ, because there is no order to preserve.

In exchange, `x in some_set` is roughly constant time. On a list, the same question is a scan: Python looks at each element until it finds a match or runs out. On a few dozen items nobody notices. On two hundred thousand, the difference is milliseconds against microseconds, and the second program on this page measures it rather than asserting it.

## Deduplicating

The most common use is removing duplicates:

unique = set(votes)

If you need a list back, wrap it: `list(set(votes))`. If you need the original order kept, a set will not do it &mdash; use `list(dict.fromkeys(votes))`, since dictionaries do preserve insertion order.

## The algebra

Four operators compare two sets, and they read like the English:

python &amp; sql&nbsp;&nbsp;# in both<br>python | sql&nbsp;&nbsp;# in either<br>python - sql&nbsp;&nbsp;# in the first only<br>python ^ sql&nbsp;&nbsp;# in exactly one

Each replaces a loop with an `if` inside it. "Which users have both skills" is one character. Writing it as a loop is not wrong, it is just more code to read and more places to make a mistake.

## The empty-set trap

`{}` is an empty <em>dictionary</em>. It has to be, because dictionaries claimed the braces first. An empty set is `set()`. This is worth remembering because `{}` looks exactly like what you want and behaves nothing like it.

## What cannot go in

Set members must be hashable, for the same reason dictionary keys must be: the set decides where to store something from its hash, so that hash must never change. Numbers, strings and tuples are fine. Lists and dictionaries are not.

## When not to use one

If order matters, if duplicates are meaningful, or if you need to index by position, use a list. A set answers one question extremely well &mdash; "is this in here?" &mdash; and refuses most others.
""",
    [{"q": "What does `{}` create?",
      "options": ["An empty set", "An empty dictionary", "An empty tuple", "A syntax error"],
      "answer": 1,
      "why": "Dictionaries claimed the braces first. An empty set is written "
             "`set()`."},
     {"q": "Why is `x in big_set` so much faster than `x in big_list`?",
      "options": ["Sets are stored sorted", "A set jumps straight to a slot from "
                  "the hash; a list must scan", "Sets are held in memory, lists on disk",
                  "It is not faster"],
      "answer": 1,
      "why": "The hash tells the set roughly where the item would live, so it "
             "checks one place. A list has no such shortcut and compares elements "
             "one by one."},
     {"q": "`{\"a\", \"b\"} ^ {\"b\", \"c\"}` gives what?",
      "options": ["{'b'}", "{'a', 'c'}", "{'a', 'b', 'c'}", "set()"],
      "answer": 1,
      "why": "`^` is symmetric difference: everything in exactly one of the two "
             "sets. 'b' is in both, so it is excluded."}],
)


# ---------------------------------------------------------------------------
# 3. Nested for loops
# ---------------------------------------------------------------------------
topic(
    "nested_for_loops",
    "Nested For Loops",
    "Loops Inside Loops",
    "A loop inside a loop, the grid it walks, and why the work multiplies "
    "rather than adds.",
    _svg("".join(_box(28 + c * 26, 22 + r * 20, 22, 16,
                      A if r == 1 and c <= 1 else S)
                 for r in range(3) for c in range(4))),
    [("nested.py", '''# The inner loop runs completely, once per outer pass.
for row in range(3):
    for col in range(4):
        print(f"row {row} col {col}", end="   ")
    print()          # newline at the end of each row

print()

# Count the passes: 3 outer, 4 inner each -> 12 bodies.
passes = 0
for row in range(3):
    for col in range(4):
        passes += 1
print("inner bodies run:", passes)
'''),
     ("nested_cost.py", '''# Nesting multiplies. Adding does not.
import time

def nested(n):
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1
    return count

def sequential(n):
    count = 0
    for i in range(n):
        count += 1
    for j in range(n):
        count += 1
    return count

for n in (100, 200, 400):
    t0 = time.perf_counter()
    nested(n)
    nested_ms = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter()
    sequential(n)
    seq_ms = (time.perf_counter() - t0) * 1000
    print(f"n={n:4d}  nested {nested(n):7d} bodies {nested_ms:7.2f} ms"
          f"   |  sequential {sequential(n):5d} bodies {seq_ms:6.2f} ms")

print()
print("Doubling n doubles the sequential work and quadruples the nested work.")
'''),
     ],
    ["The inner loop finishes entirely on every single pass of the outer one.",
     "Two nested loops over n items run n&times;n bodies. Doubling n quadruples "
     "the work; it does not double it.",
     "<code class='mono-font'>break</code> leaves only the loop it is in, "
     "the inner one. The outer loop carries on.",
     "If both loops walk the same list, you are usually comparing every pair. "
     "That is often a sign a set or dict would do it in one pass."],
    """title: Nested For Loops: A Practical Guide
intro: A loop inside a loop runs the inner one from the top on every pass of the outer one. That is easy to say and easy to under-estimate: the bodies multiply, they do not add.

## The order things happen

for row in range(3):<br>&nbsp;&nbsp;&nbsp;&nbsp;for col in range(4):<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;print(row, col)

The outer loop takes `row = 0` and then hands control to the inner loop, which runs all four of its passes before the outer loop moves to `row = 1`. Twelve lines print, in row-major order. The inner variable resets each time; the outer one does not.

This is the natural shape for anything two-dimensional: a grid, a table of rows and columns, every pairing of two lists.

## Where the newline goes

A detail that catches people: `print()` after the inner loop, indented to the outer loop, ends the row. Indent it one level further and you get a newline after every cell instead. The indentation is the logic here, not decoration.

## The cost multiplies

One loop over n items runs n bodies. Two nested loops over n items run n&times;n. Put them side by side instead of inside each other and you get 2n. The difference between n&sup2; and 2n is the difference between a program that scales and one that does not:

- n = 100: nested runs 10,000 bodies, sequential runs 200
- n = 400: nested runs 160,000, sequential runs 800

Doubling the input quadruples nested work. The second program on this page times both at three sizes so the shape is visible rather than asserted.

## break only leaves one loop

`break` exits the loop it is written in. Inside a nested pair, that is the inner loop; the outer one continues with its next pass. If you want out of both, the usual answers are to put the loops in a function and `return`, or to set a flag the outer loop checks.

## When nesting is the wrong tool

If both loops walk the same collection, you are comparing every pair, and that is often avoidable. "Does any pair sum to the target?" looks like a natural nested loop and is a single pass with a set. Nesting is right when the two dimensions are genuinely independent &mdash; rows and columns, users and permissions &mdash; and suspicious when they are the same thing twice.
""",
    [{"q": "Two loops nested over the same 500-item list. How many inner bodies run?",
      "options": ["500", "1,000", "250,000", "It depends on the data"],
      "answer": 2,
      "why": "500 outer passes, each running 500 inner passes: 500 x 500 = "
             "250,000. Nesting multiplies."},
     {"q": "A `break` in the inner loop of a nested pair does what?",
      "options": ["Leaves both loops", "Leaves the inner loop only",
                  "Skips to the next inner item", "Raises an error"],
      "answer": 1,
      "why": "break leaves the loop containing it. The outer loop carries on "
             "with its next pass, which surprises people expecting to be out "
             "of both."},
     {"q": "You double the size of the input to a doubly-nested loop. The work:",
      "options": ["Doubles", "Quadruples", "Stays the same", "Grows by 2 bodies"],
      "answer": 1,
      "why": "n squared: doubling n gives (2n) squared = 4 n squared. That is "
             "why nested loops are the first thing to look at when something is "
             "slow."}],
)


# ---------------------------------------------------------------------------
# 4. List comprehensions
# ---------------------------------------------------------------------------
topic(
    "list_comprehensions",
    "List Comprehensions",
    "Building Lists",
    "The loop that builds a list, written as one expression - and the point "
    "at which writing it that way stops helping.",
    _svg(_box(14, 30, 40, 28, S) + _txt(34, 48, "[1,2,3]") +
         '<path d="M58 44 L74 44" stroke="%s" stroke-width="2"/>' % A +
         _txt(88, 36, "x*x", A) +
         '<path d="M102 44 L118 44" stroke="%s" stroke-width="2"/>' % A +
         _box(120, 30, 30, 28, S) + _txt(135, 48, "[1,4,9]", A)),
    [("comprehension.py", '''nums = [1, 2, 3, 4, 5, 6]

# The loop version.
squares = []
for n in nums:
    squares.append(n * n)
print("loop         :", squares)

# The same work as one expression.
squares = [n * n for n in nums]
print("comprehension:", squares)

# With a filter on the end.
evens = [n for n in nums if n % 2 == 0]
print("evens        :", evens)

# Transform and filter together.
big_squares = [n * n for n in nums if n > 3]
print("big squares  :", big_squares)

# It works on anything iterable, not just lists.
print("lengths      :", [len(w) for w in "the quick brown fox".split()])
'''),
     ("comprehension_limits.py", '''# Readability is the real limit. This is fine:
words = ["Ana", "bo", "CY", "dee"]
print([w.lower() for w in words])

# This is a comprehension nobody enjoys reading:
grid = [[1, 2], [3, 4], [5, 6]]
print([n for row in grid for n in row if n % 2])

# The same thing as a loop, which most people read faster:
out = []
for row in grid:
    for n in row:
        if n % 2:
            out.append(n)
print(out)

# A comprehension builds the whole list in memory. A generator does not.
import sys
listcomp = [n * n for n in range(10_000)]
genexp = (n * n for n in range(10_000))
print("list bytes :", sys.getsizeof(listcomp))
print("gen  bytes :", sys.getsizeof(genexp))
print("gen sum    :", sum(n * n for n in range(10_000)))
'''),
     ],
    ["Read it left to right: the expression first, then where the items come "
     "from, then the filter.",
     "The <code class='mono-font'>if</code> at the end filters. There is no "
     "<code class='mono-font'>else</code> there - an else belongs in the "
     "expression at the front.",
     "Nested comprehension order matches the nested loop order: outer first.",
     "Round brackets make a generator instead: same syntax, builds nothing, "
     "ideal inside <code class='mono-font'>sum()</code> or "
     "<code class='mono-font'>any()</code>."],
    """title: List Comprehensions: A Practical Guide
intro: A comprehension is a loop that builds a list, written as a single expression. It is the same work in fewer lines &mdash; and past a certain complexity, in far less readable ones.

## The translation

Nearly every comprehension started life as this shape:

result = []<br>for item in things:<br>&nbsp;&nbsp;&nbsp;&nbsp;result.append(f(item))

which becomes:

result = [f(item) for item in things]

Read it left to right: <em>what to build</em>, then <em>where the items come from</em>. The three moving parts of the loop &mdash; create the list, iterate, append &mdash; collapse into one line where the intent is the first thing you see.

## Filtering

An `if` at the end keeps only some items:

evens = [n for n in nums if n % 2 == 0]

That is the filter position, and it takes no `else`. If you want to choose between two values rather than keep or drop, the conditional goes in the expression at the front instead:

labels = ["even" if n % 2 == 0 else "odd" for n in nums]

Two different `if`s, in two different places, doing two different jobs. Mixing them up is the most common comprehension error.

## Nesting reads outer-first

[n for row in grid for n in row]

The clauses come in the same order as the nested loops would: `for row` outside, `for n` inside. It reads oddly because the expression sits before both, but the order after the expression is exactly the loop order.

One level of nesting is defensible. Two, plus a filter, is a line that will cost you a minute every time you come back to it &mdash; and the loop version costs nothing. The second program on this page puts both side by side and prints the same answer from each.

## Comprehension or generator

Swap the brackets for round ones and you get a generator expression:

total = sum(n * n for n in range(10_000))

The comprehension builds the whole list first &mdash; every element in memory &mdash; then sums it. The generator produces one value at a time and never builds a list at all. When the result is consumed immediately by `sum`, `any`, `max` or a `for`, the generator is the better default, and the size difference is measurable: the page prints both.

## The rule of thumb

Use a comprehension when it fits on one line and reads as a sentence. When you need a second `for`, a filter, and a conditional expression at once, write the loop. Comprehensions are for making simple transformations obvious, not for proving a loop can be compressed.
""",
    [{"q": "Where does the filtering `if` go in a comprehension?",
      "options": ["Before the expression", "At the end, after the for clause",
                  "Anywhere", "Comprehensions cannot filter"],
      "answer": 1,
      "why": "The trailing `if` filters. An `if/else` that chooses between two "
             "values goes in the expression at the front instead - a different "
             "job in a different place."},
     {"q": "What does `(n * n for n in nums)` create?",
      "options": ["A list", "A tuple", "A generator", "A set"],
      "answer": 2,
      "why": "Round brackets make a generator expression, which produces values "
             "one at a time instead of building the whole result in memory."},
     {"q": "In `[n for row in grid for n in row]`, which loop is the outer one?",
      "options": ["`for n in row`", "`for row in grid`", "They run in parallel",
                  "Neither - it is not a nested loop"],
      "answer": 1,
      "why": "The clauses appear in the same order as the nested loops: the "
             "first for is the outer one."}],
)


# ---------------------------------------------------------------------------
# 5. f-strings and formatting
# ---------------------------------------------------------------------------
topic(
    "f_strings_and_formatting",
    "f-strings and Formatting",
    "Readable Output",
    "Putting values inside strings, and the small format language that "
    "controls how each one is printed.",
    _svg(_txt(80, 30, 'f"total: {n:.2f}"', A, 11) +
         '<path d="M80 38 L80 50" stroke="%s" stroke-width="2"/>' % M +
         _box(40, 52, 80, 24, S) + _txt(80, 68, "total: 12.50")),
    [("fstrings.py", '''name = "ana"
score = 91.5678
count = 1234567

# Put an expression in braces. Any expression.
print(f"{name} scored {score}")
print(f"{name.title()} scored {score:.1f}")
print(f"two plus two is {2 + 2}")

# Width and alignment - useful for columns.
rows = [("ana", 91.5), ("bo", 7.25), ("cy", 100.0)]
for who, pts in rows:
    print(f"{who:<8}{pts:>8.2f}")

# Thousands separator, percentage, padding with zeros.
print(f"{count:,}")
print(f"{0.4567:.1%}")
print(f"{7:03d}")

# = prints the expression as well as its value. Very handy when debugging.
total = 42
print(f"{total = }")
'''),
     ("formatting_compare.py", '''# The three ways, oldest to newest.
name, score = "ana", 91.5678

print("concat  : " + name + " scored " + str(round(score, 1)))
print("percent : %s scored %.1f" % (name, score))
print("format  : {} scored {:.1f}".format(name, score))
print("f-string: " + f"{name} scored {score:.1f}")

# Why the f-string wins: the value sits where it is printed.
width, height = 3, 4
print(f"{width} x {height} = {width * height}")

# Formatting is not rounding the number, only how it is shown.
value = 2 / 3
print(f"shown  : {value:.2f}")
print(f"actual : {value}")

# Aligning a small table.
print()
header = f"{'item':<10}{'qty':>5}{'price':>10}"
print(header)
print("-" * len(header))
for item, qty, price in [("apple", 3, 1.5), ("banana", 12, 0.25)]:
    print(f"{item:<10}{qty:>5}{price:>10.2f}")
'''),
     ],
    ["The <code class='mono-font'>f</code> prefix is required. Without it the "
     "braces are just braces.",
     "<code class='mono-font'>:.2f</code> fixes two decimal places, "
     "<code class='mono-font'>:,</code> adds thousands separators, "
     "<code class='mono-font'>:&gt;8</code> right-aligns in eight columns.",
     "Formatting changes what is shown, never the value itself.",
     "<code class='mono-font'>f\"{x = }\"</code> prints both the expression and "
     "its value - the fastest debug print there is."],
    """title: f-strings and Formatting: A Practical Guide
intro: An f-string puts values inside a string where they will appear, and a small format language after each colon controls exactly how they are printed.

## The prefix does the work

f"{name} scored {score}"

The `f` before the quote is what turns braces into slots. Without it you get the literal characters. Inside the braces goes any expression &mdash; a variable, a method call, arithmetic &mdash; evaluated at that point and inserted.

That is the whole idea, and it is why f-strings replaced everything before them: the value appears in the source where it appears in the output. Concatenation with `+` scatters the sentence across quotes and plus signs, and `%` and `.format()` push the values to the end, away from the slots they fill.

## The format spec

After a colon comes a compact language for presentation:

- `:.2f` &mdash; two decimal places
- `:,` &mdash; thousands separators
- `:>8` &mdash; right-align in eight columns; `<` left, `^` centre
- `:03d` &mdash; pad to three digits with zeros
- `:.1%` &mdash; show as a percentage with one decimal

They combine: `{price:>10.2f}` right-aligns in ten columns with two decimals. That is how you get a table whose numbers line up without counting spaces by hand.

## Formatting is not rounding

`f"{value:.2f}"` changes how the number is <em>displayed</em>. The variable is untouched, still carrying every digit it had. This matters when you print a rounded figure and then keep computing with the original: the printed total and the computed total can differ, and the program is not wrong &mdash; the display was never the value.

## The debugging shortcut

f"{total = }"

prints `total = 42` &mdash; the expression and its value. It works for any expression, so `f"{len(items) = }"` prints both the call and its result. It is the fastest way to instrument a function, and it removes the classic mistake of printing a label that no longer matches the variable beside it.

## Which to use

Use f-strings. `%` formatting and `.format()` still work and you will meet them in older code, but they exist now mainly to be read, not written. The one place `.format()` still earns its keep is when the template is stored separately from the values &mdash; a message in a config file, for instance &mdash; because an f-string is evaluated where it is written.
""",
    [{"q": "What does `f\"{2/3:.2f}\"` produce?",
      "options": ["'0.67'", "'0.666666'", "0.67 as a float", "A syntax error"],
      "answer": 0,
      "why": "It produces the string '0.67'. Formatting affects the text "
             "produced, not the underlying value, which still has all its "
             "digits."},
     {"q": "What is `{price:>10.2f}` doing?",
      "options": ["Rounding price to 10 decimals", "Right-aligning in 10 columns "
                  "with 2 decimals", "Multiplying by 10", "Left-aligning in 2 columns"],
      "answer": 1,
      "why": "`>` right-aligns, 10 is the field width, .2f is two decimal "
             "places. Combining them is how columns line up."},
     {"q": "You write `\"{name} scored\"` with no f prefix. What prints?",
      "options": ["The value of name", "The literal text {name} scored",
                  "An error", "An empty string"],
      "answer": 1,
      "why": "Without the f prefix the braces are ordinary characters. This is "
             "a quiet bug: nothing raises, the output is just wrong."}],
)


# ---------------------------------------------------------------------------
# 6. Function arguments
# ---------------------------------------------------------------------------
topic(
    "function_arguments",
    "Function Arguments",
    "Passing Values In",
    "Positional and keyword arguments, default values, and the mutable "
    "default that catches everyone once.",
    _svg(_box(16, 34, 44, 24, S) + _txt(38, 50, "f(a, b)") +
         '<path d="M64 46 L84 46" stroke="%s" stroke-width="2"/>' % A +
         _box(88, 24, 56, 18, S) + _txt(116, 37, "a=1", A) +
         _box(88, 48, 56, 18, S) + _txt(116, 61, "b=2", A)),
    [("arguments.py", '''def greet(name, greeting="Hello", excited=False):
    line = f"{greeting}, {name}"
    return line + "!" if excited else line

# Positional: order matters.
print(greet("ana"))
print(greet("bo", "Hi"))

# Keyword: order does not, and the call says what it means.
print(greet("cy", excited=True))
print(greet(name="dee", greeting="Yo", excited=True))

# Keywords can come in any order once you name them.
print(greet(excited=True, name="eve"))

# Positional arguments must come before keyword ones.
# print(greet(greeting="Hi", "fay"))   # SyntaxError
'''),
     ("mutable_default.py", '''# Default values are evaluated ONCE, when the function is defined.
def add_item(item, basket=[]):
    basket.append(item)
    return basket

print("call 1:", add_item("apple"))
print("call 2:", add_item("banana"))
print("call 3:", add_item("cherry"))
print("-> the same list is reused every time")

# The fix: None as the default, build a fresh one inside.
def add_item_safe(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket

print()
print("safe 1:", add_item_safe("apple"))
print("safe 2:", add_item_safe("banana"))

# Proof that the default object is created once and kept.
print()
print("default id stays the same:", id(add_item.__defaults__[0]))
add_item("date")
print("after another call       :", id(add_item.__defaults__[0]))
'''),
     ],
    ["Positional arguments are matched by order; keyword arguments by name.",
     "In a call, every positional argument must come before any keyword one.",
     "Defaults are evaluated once, at definition time - not on each call.",
     "Never default to a list or dict. Default to "
     "<code class='mono-font'>None</code> and build it inside."],
    """title: Function Arguments: A Practical Guide
intro: Python matches arguments to parameters two ways &mdash; by position and by name &mdash; and gives parameters default values. One of those defaults has a trap in it that every Python programmer meets exactly once.

## Positional and keyword

def greet(name, greeting="Hello"):

`greet("ana")` matches by position: the first argument becomes `name`. `greet("ana", greeting="Hi")` names the second explicitly. Both reach the same function; the difference is what the call site tells a reader.

Keywords earn their place when the value alone is meaningless. `send(msg, True)` tells you nothing; `send(msg, urgent=True)` tells you everything. A boolean argument is almost always worth naming.

One rule: in a call, positional arguments come first. `f(greeting="Hi", "ana")` is a syntax error, because Python cannot tell where the positional one was meant to go.

## Defaults

A parameter with a default becomes optional:

def greet(name, greeting="Hello", excited=False):

Callers supply what they care about and ignore the rest. Defaults must come after all non-default parameters, for the same reason: otherwise a positional call would be ambiguous.

## The mutable default trap

This looks reasonable and is not:

def add_item(item, basket=[]):<br>&nbsp;&nbsp;&nbsp;&nbsp;basket.append(item)<br>&nbsp;&nbsp;&nbsp;&nbsp;return basket

Call it three times with no basket and you get one item, then two, then three &mdash; all in the same list. The reason is a single rule with a large consequence: <strong>default values are evaluated once, when the `def` runs</strong>, not on each call. That one list is created at definition time and reused forever, so every mutation accumulates.

The second program on this page prints the id of the default object before and after a call, to show it really is the same object rather than a new one that happens to have old contents.

The fix is idiomatic and worth memorising:

def add_item(item, basket=None):<br>&nbsp;&nbsp;&nbsp;&nbsp;if basket is None:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;basket = []

`None` is immutable, so there is nothing to accumulate, and the fresh list is built inside the call where it belongs.

Immutable defaults &mdash; numbers, strings, `True`, `None`, tuples &mdash; are all safe. The rule is simply: never default a parameter to a list, dict or set.

## Why this design

It would be possible to re-evaluate defaults on every call, and some languages do. Python evaluates once because a default is just an expression bound at definition time, like any other value in the enclosing scope. Once you know that, the behaviour stops being surprising &mdash; but it is worth knowing before it costs you an afternoon.
""",
    [{"q": "When is a default argument value evaluated?",
      "options": ["On every call", "Once, when the function is defined",
                  "The first time the function is called", "When the module is imported and again per call"],
      "answer": 1,
      "why": "Once, at definition time. That single fact is what makes a mutable "
             "default accumulate across calls."},
     {"q": "What is the fix for `def f(items=[])`?",
      "options": ["Use a tuple instead", "Default to None and build the list inside",
                  "Copy the list at the end", "Nothing - it is fine"],
      "answer": 1,
      "why": "None is immutable so nothing accumulates, and the fresh list is "
             "created inside the call where it belongs."},
     {"q": "Which call is a syntax error?",
      "options": ["f('a', b=2)", "f(a='a', b=2)", "f(b=2, 'a')", "f('a', 2)"],
      "answer": 2,
      "why": "Positional arguments must come before keyword ones; otherwise "
             "Python cannot work out which parameter the positional value was "
             "meant for."}],
)


# ---------------------------------------------------------------------------
# 7. *args and **kwargs
# ---------------------------------------------------------------------------
topic(
    "args_and_kwargs",
    "*args and **kwargs",
    "Any Number of Arguments",
    "Collecting however many arguments a caller passes, and unpacking a list "
    "or dict back into a call.",
    _svg(_txt(30, 30, "1, 2, 3", M) +
         '<path d="M56 34 L74 42" stroke="%s" stroke-width="2"/>' % A +
         _box(78, 32, 34, 20, S) + _txt(95, 46, "*args", A) +
         _txt(30, 66, "a=1, b=2", M) +
         '<path d="M62 62 L74 52" stroke="%s" stroke-width="2"/>' % A),
    [("args_kwargs.py", '''def total(*args):
    print("  args is a tuple:", args)
    return sum(args)

print(total(1, 2, 3))
print(total(5))
print(total())

def describe(**kwargs):
    print("  kwargs is a dict:", kwargs)
    for key, value in kwargs.items():
        print(f"  {key} = {value}")

describe(name="ana", score=91)

# Both together, in the required order.
def report(label, *values, **options):
    print(f"{label}: {values}  options={options}")

report("scores", 91, 78, 85, sort=True, limit=2)
'''),
     ("unpacking_calls.py", '''# The same star, used at the call site, does the opposite:
# it spreads a collection back out into arguments.
def volume(length, width, height):
    return length * width * height

dims = [2, 3, 4]
print("without star:", end=" ")
try:
    print(volume(dims))
except TypeError as e:
    print("TypeError:", e)

print("with star   :", volume(*dims))

settings = {"length": 2, "width": 3, "height": 4}
print("with **     :", volume(**settings))

# Very common use: pass everything straight through to another function.
def logged(func, *args, **kwargs):
    print(f"  calling {func.__name__} with {args} {kwargs}")
    return func(*args, **kwargs)

print("result      :", logged(volume, 2, 3, height=4))

# Unpacking works for building collections too.
a = [1, 2]
b = [3, 4]
print("merged list :", [*a, *b])
print("merged dict :", {**{"x": 1}, **{"y": 2}})
'''),
     ],
    ["<code class='mono-font'>*args</code> collects extra positional arguments "
     "into a tuple; <code class='mono-font'>**kwargs</code> collects extra "
     "keyword ones into a dict.",
     "The names are convention, not syntax. The stars are the syntax.",
     "Order in a definition: normal, then <code class='mono-font'>*args</code>, "
     "then <code class='mono-font'>**kwargs</code>.",
     "At a call site the stars do the reverse - they spread a list or dict "
     "back into arguments."],
    """title: *args and **kwargs: A Practical Guide
intro: One star collects any number of positional arguments into a tuple; two stars collect keyword arguments into a dictionary. At a call site the same stars run in reverse, spreading a collection back out into arguments.

## Collecting

def total(*args):<br>&nbsp;&nbsp;&nbsp;&nbsp;return sum(args)

`total(1, 2, 3)` gives `args = (1, 2, 3)`. `total()` gives `args = ()`. The function accepts any number of positional arguments without knowing in advance how many, and inside it `args` is an ordinary tuple.

Two stars do the same for keyword arguments:

def describe(**kwargs):

`describe(name="ana", score=91)` gives `kwargs = {"name": "ana", "score": 91}` &mdash; an ordinary dict.

The names are pure convention. `*items` and `**options` work identically; the stars carry the meaning. Convention is strong enough here that using different names in a general-purpose helper will raise eyebrows, but in a specific function a descriptive name often reads better.

## Order in a definition

def report(label, *values, **options):

Named parameters first, then `*args`, then `**kwargs`. Python needs the fixed ones before the variable ones so it knows what to bind where.

## Spreading

The same star at a call site does the opposite job:

dims = [2, 3, 4]<br>volume(*dims)&nbsp;&nbsp;&nbsp;&nbsp;# same as volume(2, 3, 4)

Without the star you pass one argument &mdash; the list itself &mdash; and get a `TypeError` about missing parameters. With it, the list is spread across the parameters in order.

`**` does the same for a dict, matching keys to parameter names:

volume(**{"length": 2, "width": 3, "height": 4})

## The pass-through pattern

This is where the two halves meet, and it is by far the most common real use:

def logged(func, *args, **kwargs):<br>&nbsp;&nbsp;&nbsp;&nbsp;print("calling", func.__name__)<br>&nbsp;&nbsp;&nbsp;&nbsp;return func(*args, **kwargs)

`logged` accepts anything and forwards it untouched. It does not need to know the signature of what it is wrapping. Every decorator, every wrapper, every "do this then call that" helper is built on this shape.

## Merging collections

The stars also work when building literals:

[*first, *second]&nbsp;&nbsp;&nbsp;&nbsp;{**defaults, **overrides}

The dict form is a neat way to layer configuration: later keys win, so overrides beat defaults.
""",
    [{"q": "Inside `def f(*args)`, what type is `args`?",
      "options": ["A list", "A tuple", "A dict", "A set"],
      "answer": 1,
      "why": "A tuple. **kwargs gives a dict; *args gives a tuple, which is "
             "immutable and reflects that the arguments are fixed once passed."},
     {"q": "`volume(*[2, 3, 4])` is the same as what?",
      "options": ["volume([2, 3, 4])", "volume(2, 3, 4)", "volume(24)",
                  "A TypeError"],
      "answer": 1,
      "why": "At a call site the star spreads the list across the parameters. "
             "Without it you would pass one argument - the list itself."},
     {"q": "Why does the wrapper pattern use both `*args` and `**kwargs`?",
      "options": ["To be faster", "So it can forward any call without knowing "
                  "the signature", "Because Python requires both",
                  "To sort the arguments"],
      "answer": 1,
      "why": "Together they capture every positional and keyword argument, so "
             "the wrapper forwards whatever it was given to a function whose "
             "parameters it does not need to know."}],
)


# ---------------------------------------------------------------------------
# 8. Variable scope (LEGB)
# ---------------------------------------------------------------------------
topic(
    "variable_scope",
    "Variable Scope",
    "Where Names Live",
    "Which name a piece of code can see, the four places Python looks, and "
    "why assigning inside a function does not change the outside.",
    _svg(_box(10, 18, 140, 56, "none") + _txt(24, 30, "B", M, 8, "start") +
         _box(24, 28, 112, 40, "none") + _txt(38, 40, "G", M, 8, "start") +
         _box(38, 38, 84, 22, "none") + _txt(52, 52, "L", A, 8, "start") +
         _txt(96, 53, "x", A, 10)),
    [("scope.py", '''x = "global"

def show():
    print("inside sees :", x)          # reads the global fine

def shadow():
    x = "local"                        # a NEW local name
    print("inside sees :", x)

show()
shadow()
print("outside still:", x)

# Assigning anywhere in a function makes the name local for the WHOLE
# function - even before the assignment line.
def broken():
    print(x)                           # UnboundLocalError
    x = "too late"

try:
    broken()
except UnboundLocalError as e:
    print("broken() ->", e)
'''),
     ("legb.py", '''# L-E-G-B: local, enclosing, global, builtin. Python stops at the first hit.
name = "global"

def outer():
    name = "enclosing"

    def inner():
        name = "local"
        print("  inner sees   :", name)

    inner()
    print("  outer sees   :", name)

outer()
print("module sees  :", name)

# global lets a function rebind a module-level name.
count = 0

def bump():
    global count
    count += 1

bump(); bump()
print("after 2 bumps:", count)

# nonlocal reaches the enclosing function, not the module.
def counter():
    n = 0
    def step():
        nonlocal n
        n += 1
        return n
    return step

c = counter()
print("closure      :", c(), c(), c())

# The B in LEGB: builtins are the last place Python looks.
print("len is a builtin:", len)
'''),
     ],
    ["Python looks in four places, in order: Local, Enclosing, Global, Builtin.",
     "Reading an outer name works. Assigning creates a local one instead.",
     "One assignment anywhere makes the name local for the whole function - "
     "which is why reading it earlier raises <code class='mono-font'>UnboundLocalError</code>.",
     "<code class='mono-font'>global</code> rebinds a module name; "
     "<code class='mono-font'>nonlocal</code> rebinds the enclosing function's."],
    """title: Variable Scope: A Practical Guide
intro: When Python meets a name, it looks in four places in a fixed order &mdash; local, enclosing, global, builtin &mdash; and stops at the first one that has it. Almost every scope surprise comes from one rule about assignment.

## The four places

LEGB is the order:

- <strong>Local</strong> &mdash; names assigned in the current function
- <strong>Enclosing</strong> &mdash; names in a function that wraps this one
- <strong>Global</strong> &mdash; names at module level
- <strong>Builtin</strong> &mdash; `len`, `print`, `range` and friends

The first match wins, which is why naming a variable `list` or `sum` shadows the builtin for the rest of that scope. It is legal and it will confuse you later.

## Reading is easy, assigning is the trap

A function can read an outer name without ceremony:

x = "global"<br>def show():<br>&nbsp;&nbsp;&nbsp;&nbsp;print(x)&nbsp;&nbsp;# fine

But assigning to that name inside the function does not change the outer one. It creates a new local name that happens to be spelled the same, and it disappears when the function returns.

## The rule that catches everyone

<strong>If a name is assigned anywhere in a function, it is local for the entire function</strong> &mdash; including lines that run before the assignment.

def broken():<br>&nbsp;&nbsp;&nbsp;&nbsp;print(x)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# UnboundLocalError<br>&nbsp;&nbsp;&nbsp;&nbsp;x = "too late"

That `print` looks like it should read the global, and it would have, if the line below it did not exist. Python decides local-or-not when it compiles the function, not while running it. The error message &mdash; "local variable referenced before assignment" &mdash; is precise once you know this, and baffling before.

## global and nonlocal

To rebind rather than shadow, say so:

def bump():<br>&nbsp;&nbsp;&nbsp;&nbsp;global count<br>&nbsp;&nbsp;&nbsp;&nbsp;count += 1

`global` reaches module level. `nonlocal` reaches the nearest enclosing function, which is what makes closures able to keep state:

def counter():<br>&nbsp;&nbsp;&nbsp;&nbsp;n = 0<br>&nbsp;&nbsp;&nbsp;&nbsp;def step():<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;nonlocal n<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;n += 1

Both are worth knowing and neither is worth reaching for often. A function that rebinds globals is a function whose behaviour depends on when you call it, which is exactly the kind of thing that makes bugs hard to find. Returning a value is nearly always better.

## Mutating is not assigning

One clarification that resolves a lot of confusion: `items.append(1)` is not an assignment. It mutates the object the name already points at, so it affects the outer list without needing `global`. `items = [1]` is an assignment, and creates a local. The distinction is the object versus the name.
""",
    [{"q": "What order does Python search for a name?",
      "options": ["Global, Local, Builtin, Enclosing", "Local, Enclosing, Global, Builtin",
                  "Builtin, Global, Enclosing, Local", "Local, Global only"],
      "answer": 1,
      "why": "LEGB. The first match wins, which is why shadowing a builtin like "
             "`list` quietly changes what that name means for the rest of the "
             "scope."},
     {"q": "Why does reading `x` before `x = 1` inside a function raise?",
      "options": ["x was never defined anywhere", "The assignment makes x local "
                  "for the whole function", "print runs before assignment",
                  "It does not raise"],
      "answer": 1,
      "why": "Python decides at compile time that an assigned name is local for "
             "the entire function, so the earlier read refers to a local that "
             "has no value yet."},
     {"q": "`items.append(1)` inside a function affects the outer list. Why no `global`?",
      "options": ["append is special", "It mutates the object rather than "
                  "rebinding the name", "Lists are always global",
                  "It does not actually affect it"],
      "answer": 1,
      "why": "Only assignment creates a local name. Mutating the object the "
             "name already points at needs no declaration."}],
)


# ---------------------------------------------------------------------------
# 9. try / except
# ---------------------------------------------------------------------------
topic(
    "try_and_except",
    "try and except",
    "Handling Failure",
    "Catching the errors you expect, letting through the ones you do not, and "
    "why a bare except is worse than no except at all.",
    _svg('<path d="M28 24 L28 62" stroke="%s" stroke-width="2"/>' % M +
         _txt(28, 18, "try", M, 9) +
         '<path d="M28 44 L96 44" stroke="%s" stroke-width="2" stroke-dasharray="4 3"/>' % A +
         _box(98, 34, 46, 20, S, A) + _txt(121, 48, "except", A)),
    [("try_except.py", '''def to_int(text):
    try:
        return int(text)
    except ValueError:
        return None

for value in ["42", "3.9", "", "seven"]:
    print(f"{value!r:10} -> {to_int(value)}")

# Catch the specific thing you expect.
data = {"a": 1}
try:
    print(data["b"])
except KeyError as e:
    print("missing key:", e)

# else runs when nothing raised; finally always runs.
print()
for text in ["10", "oops"]:
    try:
        n = int(text)
    except ValueError:
        print(f"{text!r}: could not convert")
    else:
        print(f"{text!r}: got {n}")
    finally:
        print(f"{text!r}: finally always runs")
'''),
     ("bare_except.py", '''# A bare except catches EVERYTHING, including your own mistakes.
def risky(values):
    try:
        total = 0
        for v in values:
            total += v
        return totl          # typo - NameError
    except:                  # swallows it silently
        return 0

print("bare except  :", risky([1, 2, 3]), " <- the typo is hidden")

def better(values):
    try:
        return sum(values)
    except TypeError as e:
        print("  TypeError:", e)
        return 0

print("specific     :", better([1, 2, 3]))
print("specific     :", better([1, "two", 3]))

# Catching the exception object gives you the detail.
try:
    1 / 0
except ZeroDivisionError as e:
    print("caught       :", type(e).__name__, "-", e)

# Raise your own when the caller has done something wrong.
def set_age(age):
    if age < 0:
        raise ValueError(f"age cannot be negative, got {age}")
    return age

try:
    set_age(-1)
except ValueError as e:
    print("raised       :", e)
'''),
     ],
    ["Catch the specific exception you expect: "
     "<code class='mono-font'>except ValueError:</code>, not "
     "<code class='mono-font'>except:</code>.",
     "A bare <code class='mono-font'>except</code> also swallows your typos, "
     "turning a crash into wrong output.",
     "<code class='mono-font'>else</code> runs when nothing raised. "
     "<code class='mono-font'>finally</code> runs either way.",
     "<code class='mono-font'>as e</code> gives you the exception object, which "
     "carries the detail worth logging."],
    """title: try and except: A Practical Guide
intro: A try block runs code that might fail; an except block says what to do when a specific failure happens. The difficulty is not the syntax &mdash; it is being disciplined about which failures you actually catch.

## The shape

try:<br>&nbsp;&nbsp;&nbsp;&nbsp;return int(text)<br>except ValueError:<br>&nbsp;&nbsp;&nbsp;&nbsp;return None

If `int()` raises `ValueError`, control jumps to the handler. If it raises anything else, the handler is skipped and the error keeps travelling up. That selectivity is the point.

## Catch what you expect, nothing more

except:&nbsp;&nbsp;&nbsp;&nbsp;# catches everything

This is almost always a mistake. It catches the error you were thinking of, and also your typos, your `NameError`s, your `AttributeError`s from a refactor you half-finished. The program stops crashing and starts producing wrong answers quietly, which is strictly worse: a crash tells you where to look.

The second program on this page has a deliberate typo inside a bare `except`. It returns 0, cheerfully, and nothing anywhere says a name was misspelled.

Name the exception:

except ValueError:<br>except (KeyError, IndexError):<br>except Exception as e:&nbsp;&nbsp;# broad, but at least not BaseException

## as e, and why you want it

except ValueError as e:<br>&nbsp;&nbsp;&nbsp;&nbsp;print("could not convert:", e)

The exception object carries the detail &mdash; which key was missing, which value would not parse. Discarding it and printing "something went wrong" throws away the only part that would have helped.

## else and finally

- `else` runs when the `try` block raised nothing. It keeps the risky line alone in the `try`, so the handler cannot accidentally catch an error from the follow-up code.
- `finally` runs either way, raised or not. It is where cleanup goes.

For files and locks, prefer `with`, which does the same job with less ceremony.

## Raising your own

Handling is half of it. When a caller hands you something impossible, say so:

if age &lt; 0:<br>&nbsp;&nbsp;&nbsp;&nbsp;raise ValueError(f"age cannot be negative, got {age}")

Include the offending value in the message. "Invalid input" costs the next person a debugging session; "got -1" ends it immediately.

## Ask forgiveness, not permission

Python leans toward trying the operation and handling the failure, rather than checking first. Checking `if key in d` before `d[key]` does the lookup twice and still has a gap between the check and the use. Try it and catch `KeyError`; it is faster in the common case and correct in all of them.
""",
    [{"q": "Why is a bare `except:` discouraged?",
      "options": ["It is slower", "It catches your own bugs too, hiding them",
                  "It only works in functions", "It cannot be combined with finally"],
      "answer": 1,
      "why": "It swallows NameError, AttributeError and everything else, so a "
             "typo becomes a wrong answer rather than a crash that tells you "
             "where to look."},
     {"q": "When does an `else` block on a try run?",
      "options": ["Always", "Only when an exception was raised",
                  "Only when no exception was raised", "Never - try has no else"],
      "answer": 2,
      "why": "else runs when the try block completed without raising. It keeps "
             "follow-up code out of the try, so the handler cannot catch errors "
             "from it by accident."},
     {"q": "What does `as e` give you?",
      "options": ["A copy of the try block", "The exception object, with its detail",
                  "The line number only", "A retry counter"],
      "answer": 1,
      "why": "The exception object carries the specifics - which key, which "
             "value - which is the part worth logging."}],
)


# ---------------------------------------------------------------------------
# 10. Classes and objects
# ---------------------------------------------------------------------------
topic(
    "classes_and_objects",
    "Classes and Objects",
    "Your Own Types",
    "Bundling data with the functions that work on it: what a class defines, "
    "what an instance holds, and what self actually is.",
    _svg(_box(52, 14, 56, 20, S, A) + _txt(80, 27, "class", A) +
         '<path d="M80 36 L44 48 M80 36 L80 48 M80 36 L116 48" stroke="%s" stroke-width="1.5"/>' % M +
         _box(26, 50, 36, 18, S) + _txt(44, 63, "a") +
         _box(62, 50, 36, 18, S) + _txt(80, 63, "b") +
         _box(98, 50, 36, 18, S) + _txt(116, 63, "c")),
    [("classes.py", '''class Dog:
    def __init__(self, name, age):
        self.name = name          # each instance gets its own
        self.age = age

    def speak(self):
        return f"{self.name} says woof"

    def human_years(self):
        return self.age * 7

# The class is the template. Each call builds a new instance.
a = Dog("rex", 3)
b = Dog("mia", 5)

print(a.speak())
print(b.speak())
print(a.name, "is", a.human_years(), "in human years")

# Separate objects, separate data.
a.age = 4
print("a.age:", a.age, " b.age:", b.age)

# self is just the instance, passed in for you.
print(a.speak() == Dog.speak(a))
'''),
     ("class_vs_instance.py", '''class Counter:
    total = 0                     # class attribute - ONE, shared

    def __init__(self):
        self.count = 0            # instance attribute - one per object

    def bump(self):
        self.count += 1
        Counter.total += 1

a, b = Counter(), Counter()
a.bump(); a.bump(); b.bump()

print("a.count      :", a.count)
print("b.count      :", b.count)
print("Counter.total:", Counter.total)
print("-> count is per object, total is shared")

# __repr__ decides what you see when you print the object.
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

class NicePoint:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f"NicePoint({self.x}, {self.y})"

print()
print("without __repr__:", Point(1, 2))
print("with __repr__   :", NicePoint(1, 2))
'''),
     ],
    ["The class is the template; each <code class='mono-font'>ClassName(...)</code> "
     "call builds one instance.",
     "<code class='mono-font'>__init__</code> runs on creation and sets up the "
     "instance's own data.",
     "<code class='mono-font'>self</code> is the instance. Python passes it in; "
     "you write it as the first parameter.",
     "Attributes on <code class='mono-font'>self</code> are per object. "
     "Attributes on the class are shared by all of them."],
    """title: Classes and Objects: A Practical Guide
intro: A class bundles data with the functions that operate on it. The class is a template; each instance built from it carries its own copy of the data and shares the behaviour.

## Template and instance

class Dog:<br>&nbsp;&nbsp;&nbsp;&nbsp;def __init__(self, name, age):<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.name = name

`Dog` describes what a dog is. `Dog("rex", 3)` builds one. Build two and they are independent: changing `a.age` leaves `b.age` alone, because each instance has its own attributes.

## What __init__ does

`__init__` runs immediately after the instance is created, and its job is to set up that instance's data. It is not a constructor in the C++ sense &mdash; the object already exists by the time it runs &mdash; but in practice it is where you put everything the object needs to start life.

The double underscores mark it as a name Python itself calls. You almost never call `__init__` directly.

## self is not magic

`self` is the instance, handed to the method as its first argument. Python does this for you: `a.speak()` is `Dog.speak(a)`, and the page prints both to show they are the same call.

The name `self` is convention rather than syntax &mdash; the first parameter could be called anything &mdash; but every Python programmer expects `self`, and using something else will read as a mistake.

Every method that touches instance data needs it, and every attribute belonging to the instance is reached through it. Forgetting `self.` inside a method is the most common early error: you get a local variable that vanishes when the method returns.

## Class attributes are shared

class Counter:<br>&nbsp;&nbsp;&nbsp;&nbsp;total = 0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# one, for everybody<br>&nbsp;&nbsp;&nbsp;&nbsp;def __init__(self):<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;self.count = 0&nbsp;&nbsp;# one per instance

`self.count` belongs to the object. `Counter.total` belongs to the class and every instance sees the same one. This is occasionally what you want &mdash; a registry, a shared cache, a constant &mdash; and is a bug the rest of the time, in the same family as the mutable default argument.

## __repr__ earns its keep immediately

By default, printing an object gives you something like `&lt;__main__.Point object at 0x104...&gt;`, which tells you nothing. Define `__repr__` and you decide:

def __repr__(self):<br>&nbsp;&nbsp;&nbsp;&nbsp;return f"Point({self.x}, {self.y})"

It costs two lines and pays for itself the first time you print a list of them.

## When to write one

Not for everything. If you have a function and some data it operates on, and they keep travelling together &mdash; passed to the same functions, returned in pairs &mdash; a class makes that relationship explicit. If you just need to return two values, a tuple is lighter and clearer.
""",
    [{"q": "What is `self`?",
      "options": ["A reserved keyword", "The instance the method was called on",
                  "The class itself", "A copy of the object"],
      "answer": 1,
      "why": "It is the instance, passed as the first argument. `a.speak()` is "
             "exactly `Dog.speak(a)` - the name self is convention, not syntax."},
     {"q": "`total = 0` written directly in the class body is:",
      "options": ["A separate value per instance", "One value shared by every instance",
                  "A syntax error", "A local variable"],
      "answer": 1,
      "why": "It is a class attribute - one object shared by all instances. "
             "Per-instance data is assigned to self inside __init__."},
     {"q": "You print an object and get `<__main__.Point object at 0x...>`. The fix?",
      "options": ["Define __init__", "Define __repr__", "Use str() instead",
                  "Rename the class"],
      "answer": 1,
      "why": "__repr__ decides how the object shows up when printed or shown in "
             "a list. Two lines, and every debug print afterwards is readable."}],
)


# ---------------------------------------------------------------------------
# 11. Ternary / conditional expressions
# ---------------------------------------------------------------------------
topic(
    "conditional_expressions",
    "Conditional Expressions",
    "if as a Value",
    "Choosing between two values in a single expression, and the point at "
    "which the one-liner stops being clearer than the four lines.",
    _svg('<path d="M80 20 L80 34" stroke="%s" stroke-width="2"/>' % M +
         '<path d="M80 34 L46 50 M80 34 L114 50" stroke="%s" stroke-width="2"/>' % A +
         _box(28, 50, 36, 18, S) + _txt(46, 63, "a", A) +
         _box(96, 50, 36, 18, S) + _txt(114, 63, "b", A)),
    [("ternary.py", '''score = 72

# The statement form: four lines to set one name.
if score >= 50:
    verdict = "pass"
else:
    verdict = "fail"
print("statement :", verdict)

# The expression form: value first, then the condition.
verdict = "pass" if score >= 50 else "fail"
print("expression:", verdict)

# It is an expression, so it can go anywhere a value can.
print("inline    :", f"You {'passed' if score >= 50 else 'failed'}")
print("in a list :", ["even" if n % 2 == 0 else "odd" for n in range(5)])
print("as an arg :", max(score, 60 if score < 60 else 0))

# Reading order: the middle is the condition.
n = -4
print("abs value :", n if n >= 0 else -n)
'''),
     ("ternary_limits.py", '''# Chaining is legal and reads badly. Both of these agree; only one is clear.
def grade_chained(score):
    return "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"

def grade_plain(score):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"

for s in (95, 85, 75, 40):
    print(s, grade_chained(s), grade_plain(s))

# A common bug: `or` is not a substitute for a conditional expression.
def with_or(value):
    return value or "default"

def with_ternary(value):
    return value if value is not None else "default"

print()
for v in ["set", "", 0, None]:
    print(f"{v!r:8} or-> {with_or(v)!r:10} ternary-> {with_ternary(v)!r}")
print("-> `or` also replaces 0 and \\"\\", which are usually real values")
'''),
     ],
    ["Order is value, condition, other value: "
     "<code class='mono-font'>a if cond else b</code>.",
     "It is an expression, so it works inside f-strings, comprehensions and "
     "argument lists.",
     "The <code class='mono-font'>else</code> is mandatory - an expression must "
     "produce a value on every path.",
     "<code class='mono-font'>x or default</code> looks similar and is not: it "
     "also replaces <code class='mono-font'>0</code> and empty strings."],
    """title: Conditional Expressions: A Practical Guide
intro: A conditional expression picks between two values in one line. It is not a shorter if statement &mdash; it is an expression, which means it produces a value and can appear anywhere a value can.

## The order takes a moment

verdict = "pass" if score &gt;= 50 else "fail"

The value comes first, then the condition, then the alternative. Most languages put the condition first, so the shape reads backwards at first. It becomes natural quickly, and the reason for it is that the common case reads as a sentence: "pass, if the score is at least fifty, otherwise fail".

## Where it earns its place

Because it is an expression, it fits where a statement cannot:

f"You {'passed' if ok else 'failed'}"<br>["even" if n % 2 == 0 else "odd" for n in nums]<br>func(timeout if timeout else 30)

Inside an f-string, inside a comprehension, as an argument. A four-line `if` cannot go in any of those places, so the choice is not style &mdash; it is the only form that fits.

## The else is not optional

An expression has to produce a value on every path, so there is no one-armed version. `x = 1 if cond` is a syntax error. If you want "set it only sometimes", that is a statement, and the statement form is what you want.

## Where it stops helping

Chaining is legal:

"A" if s &gt;= 90 else "B" if s &gt;= 80 else "C" if s &gt;= 70 else "F"

and it is the point where the form has outlived its usefulness. The reader has to scan to the end to find the default, and inserting a new band means editing the middle of a long line. The page prints the chained version beside a plain sequence of `if` statements; they agree on every input, and only one of them can be read at a glance.

The rule that holds up: one condition, short values, one line. Two conditions, write the statement.

## The `or` lookalike

This is the most common way the idea goes wrong:

return value or "default"

It looks like "use the default when value is missing", and it is really "use the default when value is falsy" &mdash; which includes `0`, `""`, `[]` and `False`. If `0` is a legitimate value, `or` silently discards it.

return value if value is not None else "default"

says what was meant. The page runs both over `"set"`, `""`, `0` and `None` so the divergence is visible rather than theoretical.
""",
    [{"q": "What does `x = 5 if False` do?",
      "options": ["Sets x to None", "Sets x to False", "Raises SyntaxError",
                  "Leaves x unchanged"],
      "answer": 2,
      "why": "An expression must produce a value on every path, so the else is "
             "mandatory. There is no one-armed conditional expression."},
     {"q": "`value or 'default'` differs from a conditional expression how?",
      "options": ["It is faster", "It also replaces 0, '' and other falsy values",
                  "It only works on strings", "There is no difference"],
      "answer": 1,
      "why": "`or` tests truthiness, not presence. If 0 or an empty string is a "
             "real value in your data, `or` throws it away silently."},
     {"q": "Why can a conditional expression go inside an f-string?",
      "options": ["f-strings allow statements", "Because it is an expression, "
                  "and f-strings interpolate expressions", "It cannot",
                  "Only if bracketed"],
      "answer": 1,
      "why": "f-strings evaluate expressions in their braces. A four-line if "
             "statement is not an expression and cannot appear there."}],
)


# ---------------------------------------------------------------------------
# 12. match / case
# ---------------------------------------------------------------------------
topic(
    "match_and_case",
    "match and case",
    "Structural Matching",
    "Matching a value against patterns rather than testing it with a chain of "
    "conditions - including patterns that destructure as they match.",
    _svg(_box(56, 14, 48, 18, S, A) + _txt(80, 27, "match", A) +
         '<path d="M80 34 L34 46 M80 34 L80 46 M80 34 L126 46" stroke="%s" stroke-width="1.5"/>' % M +
         _box(16, 48, 36, 16, S) + _txt(34, 60, "case") +
         _box(62, 48, 36, 16, S) + _txt(80, 60, "case") +
         _box(108, 48, 36, 16, S) + _txt(126, 60, "_")),
    [("match_basics.py", '''def describe(status):
    match status:
        case 200:
            return "ok"
        case 404:
            return "not found"
        case 500 | 502 | 503:          # several literals in one case
            return "server error"
        case _:                        # the default
            return f"unhandled: {status}"

for code in (200, 404, 503, 418):
    print(code, "->", describe(code))

# The same as an if-chain, for comparison.
def describe_if(status):
    if status == 200:
        return "ok"
    elif status == 404:
        return "not found"
    elif status in (500, 502, 503):
        return "server error"
    else:
        return f"unhandled: {status}"

print()
print("agree:", all(describe(c) == describe_if(c) for c in (200, 404, 503, 418)))
'''),
     ("match_structure.py", '''# The real reason match exists: it takes the shape apart while matching.
def handle(event):
    match event:
        case {"type": "click", "x": x, "y": y}:
            return f"click at {x},{y}"
        case {"type": "key", "key": key}:
            return f"key {key}"
        case [first, *rest]:
            return f"list starting {first}, {len(rest)} more"
        case str() as text:
            return f"a string: {text!r}"
        case _:
            return "unknown"

events = [
    {"type": "click", "x": 10, "y": 20},
    {"type": "key", "key": "esc"},
    [1, 2, 3],
    "hello",
    3.14,
]
for e in events:
    print(f"{str(e)[:34]:36} -> {handle(e)}")

# Guards: a condition attached to a pattern.
def size(n):
    match n:
        case int() if n < 0:
            return "negative"
        case 0:
            return "zero"
        case int() if n < 100:
            return "small"
        case int():
            return "large"

print()
for n in (-5, 0, 42, 1000):
    print(n, "->", size(n))
'''),
     ],
    ["<code class='mono-font'>case _:</code> is the default. Without it, no "
     "match simply falls through and nothing happens.",
     "<code class='mono-font'>|</code> matches several literals in one case.",
     "Patterns bind as they match: "
     "<code class='mono-font'>case {\"x\": x}</code> pulls x out for you.",
     "A bare name matches everything and binds. Use "
     "<code class='mono-font'>case Colour.RED</code> or "
     "<code class='mono-font'>case 200</code>, not a lone variable."],
    """title: match and case: A Practical Guide
intro: match tests a value against patterns rather than conditions. For plain literals it is a tidier if-chain; for structured data it is something an if-chain cannot do at all, because the pattern takes the value apart while matching it.

## The tidy version of an if-chain

match status:<br>&nbsp;&nbsp;&nbsp;&nbsp;case 200:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return "ok"<br>&nbsp;&nbsp;&nbsp;&nbsp;case 500 | 502 | 503:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return "server error"<br>&nbsp;&nbsp;&nbsp;&nbsp;case _:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return "unhandled"

`|` groups alternatives, `_` is the default. The first matching case wins and the rest are skipped &mdash; there is no fall-through and no `break`.

If this were all `match` did it would be barely worth the keyword, and the page prints an if-chain beside it that agrees on every input.

## What it actually adds

case {"type": "click", "x": x, "y": y}:

This matches a dictionary that has a `type` of `"click"`, and in the same breath binds `x` and `y` to the values it found. One line replaces a type check, two key checks and two lookups &mdash; and it cannot go out of step with itself the way that sequence can.

The same applies to sequences:

case [first, *rest]:

matches any list and splits it into head and tail as it goes.

## Guards

A pattern can carry a condition:

case int() if n &lt; 0:

The pattern narrows the shape, the guard narrows the value. Together they express "an integer, and a negative one" in the place where you are already looking.

## The trap: a bare name matches everything

case status:

This does not compare against a variable called `status`. A bare name is a capture pattern: it matches anything and binds the name. It is the single most common `match` mistake, and it fails quietly &mdash; the first case swallows every value.

To compare against a constant, use a dotted name (`case Status.OK:`), a literal, or a guard.

## When to use it

For two or three literal comparisons, `if` is shorter and everyone reads it. Reach for `match` when you are inspecting the *shape* of data &mdash; parsed JSON, events, commands, ASTs &mdash; where the alternative is a stack of `isinstance` checks and key lookups. That is the job it was added for.

`match` needs Python 3.10 or newer.
""",
    [{"q": "What does a bare `case status:` do?",
      "options": ["Compares against the variable status", "Matches anything and "
                  "binds the name status", "Raises an error", "Matches only strings"],
      "answer": 1,
      "why": "A bare name is a capture pattern - it matches everything. This is "
             "the classic match bug, because the first such case swallows every "
             "value and nothing complains."},
     {"q": "What happens when no case matches and there is no `case _`?",
      "options": ["An error is raised", "Nothing happens - it falls through",
                  "The first case runs", "The program exits"],
      "answer": 1,
      "why": "match is not exhaustive by default. With no matching case and no "
             "wildcard, the block simply does nothing."},
     {"q": "`case {\"type\": \"click\", \"x\": x}` does what beyond matching?",
      "options": ["Nothing else", "Binds x to the value found at that key",
                  "Deletes the key", "Converts the dict to a list"],
      "answer": 1,
      "why": "Patterns destructure as they match, which is the main reason match "
             "exists - it replaces a check followed by a separate lookup."}],
)


# ---------------------------------------------------------------------------
# 13. for/else and while/else
# ---------------------------------------------------------------------------
topic(
    "loop_else",
    "for/else and while/else",
    "The Loop's else",
    "An else attached to a loop, which runs only when the loop was never "
    "broken out of - and is misread by almost everyone the first time.",
    _svg('<path d="M40 22 L40 58" stroke="%s" stroke-width="2"/>' % M +
         _txt(40, 16, "for", M, 9) +
         '<path d="M40 58 L40 70 L120 70" stroke="%s" stroke-width="2"/>' % A +
         _box(112, 32, 40, 18, S) + _txt(132, 45, "else", A) +
         '<path d="M40 40 L92 40" stroke="%s" stroke-width="2" stroke-dasharray="3 3"/>' % M +
         _txt(70, 34, "break", M, 8)),
    [("loop_else.py", '''# else runs when the loop finished WITHOUT breaking.
def find(items, target):
    for item in items:
        if item == target:
            print(f"  found {target}")
            break
    else:
        print(f"  {target} is not in the list")

print("search 3 :"); find([1, 2, 3], 3)
print("search 9 :"); find([1, 2, 3], 9)

# The version everybody writes instead, with a flag.
def find_flag(items, target):
    found = False
    for item in items:
        if item == target:
            found = True
            break
    if not found:
        print(f"  {target} is not in the list")

print("with flag:"); find_flag([1, 2, 3], 9)

# An empty loop body never breaks, so else still runs.
for x in []:
    pass
else:
    print("empty loop: else ran")
'''),
     ("loop_else_uses.py", '''# The classic use: a search that has to report failure.
def first_prime_factor(n):
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return i
    else:
        return None      # nothing divided it - n is prime

for n in (15, 17, 91, 97):
    f = first_prime_factor(n)
    print(f"{n:3} -> {'prime' if f is None else f'divisible by {f}'}")

# while/else works the same way.
print()
attempts = 3
while attempts > 0:
    attempts -= 1
    if attempts == 1:
        print("  succeeded with", attempts, "left")
        break
else:
    print("  ran out of attempts")

# And when it never breaks:
print()
attempts = 2
while attempts > 0:
    attempts -= 1
else:
    print("  loop completed, else ran")
'''),
     ],
    ["The <code class='mono-font'>else</code> runs when the loop ended normally - "
     "no <code class='mono-font'>break</code>.",
     "It is not \"else if the loop did not run\". An empty loop still runs the else.",
     "Think of it as <em>nobreak</em>. That is the name it should have had.",
     "It replaces the found = False flag, which is the pattern it exists for."],
    """title: for/else and while/else: A Practical Guide
intro: A loop can have an else. It runs when the loop finished normally &mdash; that is, when no break happened. Almost everyone reads it as "else if the loop did not run", and that is not what it means.

## The rule, exactly

for item in items:<br>&nbsp;&nbsp;&nbsp;&nbsp;if item == target:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;break<br>else:<br>&nbsp;&nbsp;&nbsp;&nbsp;print("not found")

The `else` runs if the loop ran to completion without hitting `break`. Iterate zero times? The else runs. Iterate a million times and finish? The else runs. Break out on the first pass? It does not.

The keyword is badly chosen. If it were called `nobreak`, nobody would ever have been confused by it, and reading it that way in your head is the fastest way to make it click.

## What it replaces

This shape appears constantly:

found = False<br>for item in items:<br>&nbsp;&nbsp;&nbsp;&nbsp;if match(item):<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;found = True<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;break<br>if not found:<br>&nbsp;&nbsp;&nbsp;&nbsp;...

The flag exists only to carry one bit of information past the end of the loop. `for/else` carries it for you: the else block <em>is</em> the "we never found it" branch. One fewer variable, and one fewer chance to forget to set it.

## Where it genuinely reads well

Searching, and primality testing, which is the same shape:

for i in range(2, int(n ** 0.5) + 1):<br>&nbsp;&nbsp;&nbsp;&nbsp;if n % i == 0:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return i<br>else:<br>&nbsp;&nbsp;&nbsp;&nbsp;return None

"Tried every divisor, none worked" is exactly the else branch.

## while/else too

The same rule applies to `while`: the else runs when the condition became false, and not when a `break` ended the loop. That maps onto retry loops neatly &mdash; the else is where "we exhausted every attempt" lives.

## Should you use it

It is a genuine tool and it is also unfamiliar to many readers. Inside a small function whose whole point is the search, it reads well and saves a flag. Buried in a long function among other loops, a comment or a flag may serve the next person better. Knowing it matters more than using it, because you will meet it in other people's code and it must not be a mystery.
""",
    [{"q": "When does a for/else's else block run?",
      "options": ["When the loop body never ran", "When the loop finished without "
                  "a break", "Always", "Only when an exception occurred"],
      "answer": 1,
      "why": "It means nobreak. A loop over an empty sequence never breaks, so "
             "the else still runs - which is why the 'did not run' reading is "
             "wrong."},
     {"q": "What does for/else replace in ordinary code?",
      "options": ["The break statement", "A found = False flag checked after "
                  "the loop", "The range function", "try/except"],
      "answer": 1,
      "why": "The flag exists only to carry 'we never found it' past the loop. "
             "The else block is that branch, without the extra variable."},
     {"q": "`for x in []: pass` followed by `else: print('hi')` prints what?",
      "options": ["Nothing", "hi", "An error", "Depends on Python version"],
      "answer": 1,
      "why": "Zero iterations means zero breaks, so the loop completed normally "
             "and the else runs."}],
)

# ---------------------------------------------------------------------------
# 14. Nested conditionals
# ---------------------------------------------------------------------------
topic(
    "nested_conditionals",
    "Nested Conditionals",
    "Decisions Inside Decisions",
    "An if inside an if, why the indentation climbs so fast, and the guard "
    "clause that flattens most of it back out.",
    _svg('<path d="M30 20 L30 70" stroke="%s" stroke-width="2"/>' % M +
         '<path d="M30 32 L58 32 L58 70" stroke="%s" stroke-width="2"/>' % M +
         '<path d="M58 44 L86 44 L86 70" stroke="%s" stroke-width="2"/>' % A +
         '<path d="M86 56 L114 56" stroke="%s" stroke-width="2"/>' % A +
         _txt(126, 60, "?", A, 12)),
    [("nested_if.py", '''def can_borrow(member, book):
    if member["active"]:
        if member["fines"] == 0:
            if book["available"]:
                return "yes"
            else:
                return "book is out"
        else:
            return "unpaid fines"
    else:
        return "membership inactive"

# The same logic as guard clauses: handle each refusal and leave.
def can_borrow_flat(member, book):
    if not member["active"]:
        return "membership inactive"
    if member["fines"] > 0:
        return "unpaid fines"
    if not book["available"]:
        return "book is out"
    return "yes"

cases = [
    ({"active": True,  "fines": 0}, {"available": True}),
    ({"active": True,  "fines": 5}, {"available": True}),
    ({"active": False, "fines": 0}, {"available": True}),
    ({"active": True,  "fines": 0}, {"available": False}),
]
for m, b in cases:
    print(f"{can_borrow(m, b):20} | {can_borrow_flat(m, b)}")
'''),
     ("combining.py", '''# Nesting is sometimes just an `and` written the long way.
age, member = 20, True

if age >= 18:
    if member:
        print("nested  : allowed")

if age >= 18 and member:
    print("combined: allowed")

# But nesting matters when the branches differ.
def price(age, member):
    if age < 18:
        return 0 if member else 5      # children: free for members
    return 8 if member else 12

for a, m in [(10, True), (10, False), (30, True), (30, False)]:
    print(f"age {a:2} member {str(m):5} -> {price(a, m)}")

# elif is not nesting. These two are different shapes.
def band_elif(n):
    if n > 100: return "high"
    elif n > 50: return "mid"
    else: return "low"

def band_nested(n):
    if n > 50:
        if n > 100:
            return "high"
        return "mid"
    return "low"

print()
print("agree:", all(band_elif(n) == band_nested(n) for n in (10, 60, 200)))
'''),
     ],
    ["If the inner <code class='mono-font'>if</code> is the only thing in the "
     "outer one, <code class='mono-font'>and</code> says the same thing flatter.",
     "A guard clause handles one case and returns, so the rest of the function "
     "stops being indented.",
     "<code class='mono-font'>elif</code> is a chain, not a nest. Same "
     "indentation, one decision.",
     "Three levels of indentation is the usual signal to extract a function."],
    """title: Nested Conditionals: A Practical Guide
intro: An if inside an if is sometimes exactly right and more often a shape that grew. The useful skill is recognising which one you have, because most nesting can be flattened without changing the logic.

## When nesting is just `and`

if age &gt;= 18:<br>&nbsp;&nbsp;&nbsp;&nbsp;if member:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;allow()

If the inner `if` is the entire body of the outer one, and there is no `else` on either, the two conditions are simply both required:

if age &gt;= 18 and member:

Same behaviour, one level of indentation, and the condition reads as one thought instead of two.

## When it genuinely nests

Nesting earns its place when the branches diverge &mdash; when the inner decision only makes sense inside the outer one, and each has its own alternative:

if age &lt; 18:<br>&nbsp;&nbsp;&nbsp;&nbsp;return 0 if member else 5<br>return 8 if member else 12

Here "member" means something different in each branch. That is a real tree, not an accidental one.

## Guard clauses flatten the rest

The most common nested shape is a series of refusals, each with an `else`:

if active:<br>&nbsp;&nbsp;&nbsp;&nbsp;if no_fines:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if available:<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return "yes"

Four levels deep, and the success case &mdash; the thing the function is for &mdash; is buried furthest from the left margin, while every failure sits in an `else` far from the condition that caused it.

Inverted, each failure handles itself and leaves:

if not active:&nbsp;&nbsp;&nbsp;&nbsp;return "membership inactive"<br>if fines &gt; 0:&nbsp;&nbsp;&nbsp;&nbsp;return "unpaid fines"<br>if not available: return "book is out"<br>return "yes"

Now every rule sits beside its own message, the happy path is the last line at zero indentation, and adding a rule is one line rather than another level. The page runs both over the same four cases and prints them side by side, because the point is that the behaviour is identical and only the shape changed.

## elif is not nesting

if n &gt; 100: ... elif n &gt; 50: ... else: ...

An `elif` chain is one decision with several outcomes, all at the same indentation. Reaching for a nested `if` where an `elif` would do is how a flat choice becomes a staircase.

## The rule of thumb

Two levels is normal. Three is worth a second look. Four almost always means either a set of guard clauses waiting to be inverted, or a block that wants to be its own function.
""",
    [{"q": "`if a:` containing only `if b:` with no else is the same as what?",
      "options": ["if a or b:", "if a and b:", "if not a:", "Nothing - it cannot "
                  "be flattened"],
      "answer": 1,
      "why": "Both conditions must hold and nothing else happens, so `and` says "
             "it in one line at one indentation level."},
     {"q": "What is a guard clause?",
      "options": ["A try/except around the function", "An early return that "
                  "handles one case and leaves", "A nested if", "A type check"],
      "answer": 1,
      "why": "It handles a refusal immediately and returns, so the remainder of "
             "the function is not indented inside an else."},
     {"q": "How does an `elif` chain differ from nested ifs?",
      "options": ["It is faster", "It is one decision at one indentation level, "
                  "not a tree", "It cannot have an else", "It only works on numbers"],
      "answer": 1,
      "why": "elif expresses several mutually exclusive outcomes of a single "
             "decision. Nesting expresses decisions that live inside other "
             "decisions."}],
)


# ---------------------------------------------------------------------------
# 15. enumerate()
# ---------------------------------------------------------------------------
topic(
    "enumerate_function",
    "enumerate()",
    "Index and Value",
    "Getting the position alongside the item, without maintaining a counter "
    "or indexing back into the list.",
    _svg("".join(_box(24, 20 + i * 20, 26, 16, S) + _txt(37, 32 + i * 20, str(i), A) +
                 _box(56, 20 + i * 20, 68, 16, S) + _txt(90, 32 + i * 20, v)
                 for i, v in enumerate(["ana", "bo", "cy"]))),
    [("enumerate.py", '''names = ["ana", "bo", "cy"]

# The manual counter: works, and there is a better way.
i = 0
for name in names:
    print(i, name)
    i += 1

print()

# Indexing back in: also works, also noisier.
for i in range(len(names)):
    print(i, names[i])

print()

# enumerate gives both at once.
for i, name in enumerate(names):
    print(i, name)

print()

# start= when humans will read the number.
for n, name in enumerate(names, start=1):
    print(f"{n}. {name}")
'''),
     ("enumerate_uses.py", '''lines = ["alpha", "", "gamma", "delta"]

# Reporting which line was wrong is the classic use.
for n, line in enumerate(lines, start=1):
    if not line.strip():
        print(f"line {n}: empty")

# It works on any iterable, not just lists.
print()
for i, ch in enumerate("hey"):
    print(i, ch)

# What enumerate actually yields: tuples.
print()
print("as a list:", list(enumerate(["a", "b"])))
print("one item :", next(iter(enumerate(["a", "b"]))))

# Unpacking in the for statement is what hides the tuple.
print()
for pair in enumerate(["a", "b"]):
    print("without unpacking:", pair)

# Careful: start= changes the label, not the position.
print()
for n, name in enumerate(["ana", "bo"], start=1):
    print(f"label {n} is at index {n - 1}: {name}")
'''),
     ],
    ["<code class='mono-font'>enumerate</code> yields "
     "<code class='mono-font'>(index, item)</code> tuples; the "
     "<code class='mono-font'>for</code> unpacks them.",
     "<code class='mono-font'>start=1</code> changes the number it reports, not "
     "where it reads from.",
     "It works on any iterable - strings, files, generators - not only lists.",
     "<code class='mono-font'>for i in range(len(x))</code> is the pattern this "
     "replaces."],
    """title: enumerate(): A Practical Guide
intro: enumerate walks a sequence and hands you the position along with the item. It replaces both of the usual workarounds &mdash; a counter you increment by hand, and indexing back into the list.

## The two things it replaces

The counter:

i = 0<br>for name in names:<br>&nbsp;&nbsp;&nbsp;&nbsp;print(i, name)<br>&nbsp;&nbsp;&nbsp;&nbsp;i += 1

and the index:

for i in range(len(names)):<br>&nbsp;&nbsp;&nbsp;&nbsp;print(i, names[i])

Both work. The first has a variable to initialise and remember to increment; forget the increment and the loop runs forever printing zero. The second reads the list twice per pass &mdash; once for the length, once per lookup &mdash; and puts `names[i]` where you wanted `name`.

for i, name in enumerate(names):

says the same thing with neither problem.

## What it actually produces

`enumerate` yields tuples: `(0, "ana")`, `(1, "bo")`. The `for i, name` on the left is ordinary tuple unpacking, which is why the tuples are invisible in normal use. Loop without unpacking and you see them:

for pair in enumerate(names):&nbsp;&nbsp;# (0, 'ana')

`list(enumerate(x))` is the quickest way to see the whole thing at once.

## start= renumbers the label

for n, name in enumerate(names, start=1):

This is for output humans read &mdash; line numbers, ranked lists, steps. It changes the number reported, not the position read: with `start=1`, the item labelled 1 is still `names[0]`. If you use `n` to index back into the list you will be off by one, which is a bug that only shows up on the first and last element.

## It is lazy, and it takes any iterable

`enumerate` does not build a list of pairs. It produces them one at a time as the loop asks, so it works on a file, a generator, or a sequence too large to hold in memory. It also works on strings, giving character positions.

## When you do not need it

If you never use the index, do not ask for it. `for name in names` is the shorter, clearer loop, and reaching for `enumerate` out of habit adds a variable nothing reads.
""",
    [{"q": "What does `enumerate(['a', 'b'])` yield?",
      "options": ["'a', 'b'", "0, 1", "(0, 'a') then (1, 'b')", "A dictionary"],
      "answer": 2,
      "why": "It yields tuples of index and item. The `for i, x` form unpacks "
             "them, which is why the tuples are usually invisible."},
     {"q": "With `enumerate(names, start=1)`, which item does n=1 refer to?",
      "options": ["names[1]", "names[0]", "The last item", "It raises"],
      "answer": 1,
      "why": "start= changes the label only. The first item is still index 0, "
             "so using n to index back into the list is off by one."},
     {"q": "Why prefer enumerate over `for i in range(len(items))`?",
      "options": ["It is the only way to get an index", "It gives the item "
                  "directly instead of indexing back in", "It sorts the list",
                  "range does not work on lists"],
      "answer": 1,
      "why": "You get both the position and the value without a second lookup, "
             "and without an index you could get wrong."}],
)


# ---------------------------------------------------------------------------
# 16. zip()
# ---------------------------------------------------------------------------
topic(
    "zip_function",
    "zip()",
    "Two Lists in Step",
    "Walking two or more sequences together, and the silent truncation when "
    "they are not the same length.",
    _svg("".join(_box(20, 22 + i * 20, 44, 16, S) + _txt(42, 34 + i * 20, v)
                 for i, v in enumerate(["a", "b", "c"])) +
         "".join(_box(96, 22 + i * 20, 44, 16, S) + _txt(118, 34 + i * 20, v, A)
                 for i, v in enumerate(["1", "2"])) +
         '<path d="M66 30 L94 30 M66 50 L94 50" stroke="%s" stroke-width="2"/>' % A +
         '<path d="M66 70 L94 70" stroke="%s" stroke-width="1" stroke-dasharray="3 3"/>' % M),
    [("zip.py", '''names = ["ana", "bo", "cy"]
scores = [91, 78, 85]

# Walk both at once.
for name, score in zip(names, scores):
    print(f"{name:5} {score}")

# The alternative, for comparison.
print()
for i in range(len(names)):
    print(f"{names[i]:5} {scores[i]}")

# More than two is fine.
print()
grades = ["A", "C", "B"]
for name, score, grade in zip(names, scores, grades):
    print(f"{name:5} {score:3} {grade}")

# Building a dict from two lists is the most common one-liner.
print()
print(dict(zip(names, scores)))
'''),
     ("zip_uneven.py", '''# zip stops at the SHORTEST input. Silently.
names = ["ana", "bo", "cy", "dee"]
scores = [91, 78]

print("pairs:", list(zip(names, scores)))
print("-> cy and dee vanished, with no warning")

# strict=True makes the mismatch an error instead (Python 3.10+).
print()
try:
    list(zip(names, scores, strict=True))
except ValueError as e:
    print("strict ->", e)

# zip_longest fills instead of truncating.
from itertools import zip_longest
print()
print("longest:", list(zip_longest(names, scores, fillvalue=0)))

# Unzipping: the same function, with a star.
print()
pairs = [("ana", 91), ("bo", 78)]
who, what = zip(*pairs)
print("who :", who)
print("what:", what)
print("-> and they come back as tuples, not lists")
'''),
     ],
    ["<code class='mono-font'>zip</code> stops at the shortest input and says "
     "nothing about it.",
     "<code class='mono-font'>strict=True</code> raises on a length mismatch "
     "(Python 3.10+).",
     "<code class='mono-font'>dict(zip(keys, values))</code> is the standard way "
     "to build a dict from two lists.",
     "<code class='mono-font'>zip(*pairs)</code> unzips, and hands back tuples."],
    """title: zip(): A Practical Guide
intro: zip walks several sequences in step, yielding one tuple per position. It is the clean answer to "I have two lists that line up" &mdash; with one behaviour worth knowing before it bites.

## The basic shape

for name, score in zip(names, scores):

Each pass gives you the next item from each list. The alternative is `for i in range(len(names))` followed by two lookups, which works and puts an index between you and the values.

It takes any number of iterables:

for name, score, grade in zip(names, scores, grades):

## Building a dict

dict(zip(keys, values))

This is the standard idiom for turning two parallel lists into a mapping, and it is worth recognising on sight because it appears everywhere.

## It truncates, and it does not tell you

This is the part that costs people an afternoon:

zip(["ana", "bo", "cy", "dee"], [91, 78])

gives two pairs. `cy` and `dee` are gone. No error, no warning &mdash; `zip` stops when the shortest input runs out, by design.

When the lists come from the same source that is usually harmless. When one is data and the other is a lookup that quietly returned fewer rows, you get a silently shortened result, which is the worst kind of wrong.

Two ways to be explicit:

zip(a, b, strict=True)&nbsp;&nbsp;# raises ValueError on mismatch (3.10+)<br>zip_longest(a, b, fillvalue=0)&nbsp;&nbsp;# pads instead, from itertools

If the lists are supposed to be the same length, `strict=True` turns a silent bug into an immediate error. That is nearly always the better trade.

## Unzipping

The same function reverses itself with a star:

who, what = zip(*pairs)

`zip(*pairs)` spreads the list of pairs into arguments, so `zip` receives each pair as a separate iterable and re-pairs them by position. The results come back as tuples, not lists &mdash; wrap in `list()` if that matters.

## It is lazy

`zip` returns an iterator, not a list. It produces pairs as they are asked for, which is what lets it work on files and generators. It also means you can only walk it once: consume it in a loop and it is exhausted. `list(zip(...))` when you need to keep the result.
""",
    [{"q": "`zip(['a','b','c'], [1,2])` produces how many pairs?",
      "options": ["3", "2", "An error", "5"],
      "answer": 1,
      "why": "zip stops at the shortest input, silently. 'c' is dropped with no "
             "warning at all, which is why strict=True exists."},
     {"q": "How do you make a length mismatch an error?",
      "options": ["zip_longest", "zip(a, b, strict=True)", "len(a) == len(b)",
                  "You cannot"],
      "answer": 1,
      "why": "strict=True raises ValueError when the inputs differ in length "
             "(Python 3.10+), turning a silent truncation into a visible bug."},
     {"q": "What does `zip(*pairs)` do?",
      "options": ["Sorts the pairs", "Unzips them back into separate sequences",
                  "Removes duplicates", "Nothing useful"],
      "answer": 1,
      "why": "The star spreads the pairs into separate arguments, so zip "
             "re-groups them by position - the inverse of zipping."}],
)


# ---------------------------------------------------------------------------
# 17. sorted() with key=
# ---------------------------------------------------------------------------
topic(
    "sorted_with_key",
    "sorted() with key=",
    "Sorting by Anything",
    "Sorting by a computed value rather than the item itself, and the "
    "difference between sorted() and .sort().",
    _svg("".join(_box(22 + i * 30, 62 - h * 5, 22, 6 + h * 5, S if i != 1 else A)
                 for i, h in enumerate([2, 5, 1, 7]))),
    [("sorted_key.py", '''words = ["banana", "fig", "cherry", "kiwi"]

print("default   :", sorted(words))                 # alphabetical
print("by length :", sorted(words, key=len))        # by a computed value
print("longest   :", sorted(words, key=len, reverse=True))

# key takes a function of one item, returning what to sort ON.
print()
print("last char :", sorted(words, key=lambda w: w[-1]))

people = [("ana", 30), ("bo", 25), ("cy", 35)]
print()
print("by age    :", sorted(people, key=lambda p: p[1]))

# Sorting dicts by a field.
rows = [{"name": "ana", "score": 91}, {"name": "bo", "score": 78}]
print("by score  :", sorted(rows, key=lambda r: r["score"]))

# Tuple keys sort by the first, then the second - a tiebreak for free.
print()
data = [("b", 2), ("a", 2), ("c", 1)]
print("count then name:", sorted(data, key=lambda t: (t[1], t[0])))
'''),
     ("sorted_vs_sort.py", '''nums = [3, 1, 2]

# sorted() returns a NEW list and leaves the original alone.
new = sorted(nums)
print("sorted -> new     :", new, " original:", nums)

# .sort() rearranges in place and returns None.
result = nums.sort()
print(".sort() -> returns:", result, " original:", nums)
print("-> assigning the result of .sort() gives you None, the classic bug")

# Only lists have .sort(). sorted() takes anything iterable.
print()
print("sorted a tuple :", sorted((3, 1, 2)))
print("sorted a string:", sorted("cab"))
print("sorted a dict  :", sorted({"b": 1, "a": 2}))   # sorts the keys

# The sort is stable: equal keys keep their original order.
print()
pairs = [("b", 1), ("a", 1), ("c", 0)]
print("by number only :", sorted(pairs, key=lambda t: t[1]))
print("-> b still before a, because they tied and stability preserved it")
'''),
     ],
    ["<code class='mono-font'>key</code> is a function of one item that returns "
     "the value to sort on.",
     "<code class='mono-font'>sorted()</code> returns a new list; "
     "<code class='mono-font'>.sort()</code> rearranges in place and returns "
     "<code class='mono-font'>None</code>.",
     "Return a tuple from <code class='mono-font'>key</code> to sort by one "
     "field then another.",
     "The sort is stable, so equal keys keep the order they came in."],
    """title: sorted() with key=: A Practical Guide
intro: sorted arranges items by comparing them. key= lets you say what to compare instead &mdash; a length, a field, a computed score &mdash; without touching the items themselves.

## key is a function of one item

sorted(words, key=len)

`key` is called once per item and returns the value to sort on. Here `len` turns each word into its length, and the words come back shortest first. The items in the result are still the words; only the comparison changed.

Anything callable works: a builtin, a lambda, a named function.

sorted(people, key=lambda p: p[1])&nbsp;&nbsp;&nbsp;&nbsp;# by the second element<br>sorted(rows, key=lambda r: r["score"])&nbsp;&nbsp;# by a dict field

## Tuple keys give you tiebreaks

Return a tuple and Python compares the first element, then the second where the first ties:

sorted(data, key=lambda t: (t[1], t[0]))

"By count, then alphabetically" in one expression. Negate a number to reverse just that field: `(-count, name)` sorts by count descending and name ascending, which `reverse=True` cannot express because it flips everything.

## sorted() versus .sort()

new = sorted(nums)&nbsp;&nbsp;# a new list, original untouched<br>nums.sort()&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# rearranges in place, returns None

The trap is writing `nums = nums.sort()`, which assigns `None` and destroys the list. It is a common enough mistake that recognising it is worth more than the rule: if a sort produced `None`, this is why.

`.sort()` exists only on lists. `sorted()` accepts any iterable &mdash; a tuple, a string, a set, a dict (giving its keys) &mdash; and always hands back a list.

## Stability, and why it matters

Python's sort is stable: items that compare equal keep their original relative order. That is what makes multi-pass sorting work. Sort by name, then sort the result by score, and entries with the same score are still in name order. The page shows this directly, sorting only by the number and pointing out that the tied items did not shuffle.

## The performance note

`key` is called exactly once per item, not on every comparison, so an expensive key function is affordable. Doing the same work inside a comparison would cost far more.
""",
    [{"q": "What does `nums = nums.sort()` leave in nums?",
      "options": ["The sorted list", "None", "The original list", "An error"],
      "answer": 1,
      "why": ".sort() sorts in place and returns None, so the assignment "
             "replaces the list with None. Use sorted() if you want a value "
             "back."},
     {"q": "How do you sort by count descending, then name ascending?",
      "options": ["reverse=True", "key=lambda x: (-x.count, x.name)",
                  "Two separate sorts with reverse", "It is not possible"],
      "answer": 1,
      "why": "reverse=True flips every field. Negating just the numeric part of "
             "a tuple key reverses that field alone."},
     {"q": "What does a stable sort guarantee?",
      "options": ["It never crashes", "Items comparing equal keep their original "
                  "order", "It is always fastest", "The list is copied"],
      "answer": 1,
      "why": "Stability is what makes sorting in several passes work: a later "
             "sort does not scramble the order established by an earlier one."}],
)

# ---------------------------------------------------------------------------
# 18. range() with step and negative step
# ---------------------------------------------------------------------------
topic(
    "range_step",
    "range() with step",
    "Counting by Anything",
    "The third argument, counting backwards, and why the stop value is never "
    "one of the numbers you get.",
    _svg('<path d="M18 45 L142 45" stroke="%s" stroke-width="2"/>' % M +
         "".join('<circle cx="%d" cy="45" r="4" fill="%s"/>' % (26 + i * 24, A if i % 2 == 0 else "none")
                 + ('' if i % 2 == 0 else '<circle cx="%d" cy="45" r="4" fill="none" stroke="%s"/>' % (26 + i * 24, M))
                 for i in range(5)) +
         _txt(80, 70, "step 2", M, 9)),
    [("range_step.py", '''print("range(5)        :", list(range(5)))
print("range(2, 6)     :", list(range(2, 6)))
print("range(0, 10, 2) :", list(range(0, 10, 2)))
print("range(1, 10, 3) :", list(range(1, 10, 3)))

# Backwards needs a negative step AND a stop below the start.
print()
print("range(5, 0, -1) :", list(range(5, 0, -1)))
print("range(4, -1, -1):", list(range(4, -1, -1)))    # includes 0
print("range(5, 0)     :", list(range(5, 0)))          # empty - no step given

# The stop is never included. That is why these line up.
print()
items = ["a", "b", "c", "d"]
print("len            :", len(items))
print("range(len)     :", list(range(len(items))))
print("last index     :", len(items) - 1)
'''),
     ("range_reverse.py", '''items = ["a", "b", "c", "d"]

# Three ways to walk backwards. Pick the readable one.
print("reversed()     :", [x for x in reversed(items)])
print("slice [::-1]   :", items[::-1])
print("range backwards:", [items[i] for i in range(len(items) - 1, -1, -1)])

# The off-by-one that catches people: -1 as the stop, to include index 0.
print()
print("stop at 0  :", list(range(3, 0, -1)), " <- misses 0")
print("stop at -1 :", list(range(3, -1, -1)), " <- includes 0")

# range is lazy: it stores three numbers, not the sequence.
import sys
print()
print("range(1_000_000) bytes:", sys.getsizeof(range(1_000_000)))
print("the list version bytes:", sys.getsizeof(list(range(100_000))))

# Membership still works, and is computed rather than searched.
print()
print("999_999 in range(1_000_000):", 999_999 in range(1_000_000))
'''),
     ],
    ["Three arguments: <code class='mono-font'>range(start, stop, step)</code>. "
     "With one, it is the stop.",
     "The stop is never produced. <code class='mono-font'>range(5)</code> ends "
     "at 4.",
     "Counting down needs a negative step and a stop <em>below</em> the start; "
     "to reach index 0, stop at -1.",
     "<code class='mono-font'>reversed(x)</code> or "
     "<code class='mono-font'>x[::-1]</code> usually reads better than a "
     "backwards range."],
    """title: range() with step: A Practical Guide
intro: range takes up to three arguments &mdash; start, stop and step &mdash; and produces numbers without ever building a list. The two things worth internalising are that the stop is excluded, and what that means when counting down.

## The three forms

range(5)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 0 1 2 3 4<br>range(2, 6)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 2 3 4 5<br>range(0, 10, 2)&nbsp;&nbsp;# 0 2 4 6 8

One argument is the stop. Two are start and stop. Three add the step. The step can be any non-zero integer.

## The stop is never included

`range(5)` gives five numbers ending at 4. This looks like an off-by-one waiting to happen and is the opposite: it is what makes `range(len(items))` produce exactly the valid indices of a list, and what makes `range(a, b)` produce `b - a` numbers.

## Counting down

Two things must both be true:

range(5, 0, -1)&nbsp;&nbsp;&nbsp;&nbsp;# 5 4 3 2 1

The step is negative <em>and</em> the stop is below the start. Get one wrong and you get an empty range, not an error &mdash; `range(5, 0)` with no step produces nothing at all, because it is counting up from 5 to 0.

The classic mistake is stopping at 0 when you meant to include it:

range(3, 0, -1)&nbsp;&nbsp;&nbsp;# 3 2 1&nbsp;&nbsp;- misses 0<br>range(3, -1, -1)&nbsp;&nbsp;# 3 2 1 0

To walk a list backwards by index you need `range(len(items) - 1, -1, -1)`, which is three fiddly numbers in a row and exactly why the alternatives exist:

for x in reversed(items):<br>for x in items[::-1]:

Both say "backwards" without arithmetic. Reach for a backwards `range` only when you genuinely need the index.

## It does not build a list

`range(1_000_000)` stores three integers &mdash; start, stop, step &mdash; and computes each value on demand. It is a few dozen bytes whatever the size, which the page prints beside the list version for contrast.

That laziness is also why `x in range(n)` is fast: it does arithmetic rather than searching. It is the one `in` test on a sequence that does not scan.

## Only integers

`range` refuses floats. For a fractional step, build the integers and divide, or use a library. `range(0, 1, 0.1)` is a TypeError, not a rounding problem.
""",
    [{"q": "What does `list(range(5, 0))` give?",
      "options": ["[5, 4, 3, 2, 1]", "[]", "[0, 1, 2, 3, 4]", "An error"],
      "answer": 1,
      "why": "With no step it counts up, and 5 is already past the stop of 0, so "
             "the range is empty. Counting down needs an explicit negative step."},
     {"q": "To walk indices of a 4-item list backwards including 0, you need:",
      "options": ["range(3, 0, -1)", "range(3, -1, -1)", "range(4, 0, -1)",
                  "range(0, 4, -1)"],
      "answer": 1,
      "why": "The stop is excluded, so stopping at -1 is what makes 0 the last "
             "value produced."},
     {"q": "Why is `999_999 in range(1_000_000)` fast?",
      "options": ["The range is cached", "It computes the answer arithmetically "
                  "rather than scanning", "Ranges are sorted", "It is not fast"],
      "answer": 1,
      "why": "A range knows its start, stop and step, so membership is a "
             "calculation. It is the one sequence where `in` does not scan."}],
)


# ---------------------------------------------------------------------------
# 19. Dict and set comprehensions
# ---------------------------------------------------------------------------
topic(
    "dict_and_set_comprehensions",
    "Dict and Set Comprehensions",
    "Building Mappings",
    "The same comprehension syntax that builds lists, building dictionaries "
    "and sets instead.",
    _svg(_box(16, 32, 40, 26, S) + _txt(36, 49, "[...]", M) +
         _box(60, 32, 40, 26, S, A) + _txt(80, 49, "{k:v}", A) +
         _box(104, 32, 40, 26, S) + _txt(124, 49, "{...}", M)),
    [("dict_comprehension.py", '''words = ["apple", "fig", "banana"]

# Dict comprehension: note the key: value in the expression slot.
lengths = {w: len(w) for w in words}
print("lengths :", lengths)

# The loop it replaces.
lengths2 = {}
for w in words:
    lengths2[w] = len(w)
print("by loop :", lengths2)

# Filtering works the same way.
print("long    :", {w: len(w) for w in words if len(w) > 3})

# Inverting a dict.
prices = {"apple": 3, "fig": 5}
print()
print("inverted:", {v: k for k, v in prices.items()})

# Building from two lists - zip again.
print("zipped  :", {k: v for k, v in zip(["a", "b"], [1, 2])})
'''),
     ("set_comprehension.py", '''words = ["apple", "fig", "banana", "kiwi", "plum"]

# Set comprehension: braces, no colon.
print("first letters:", {w[0] for w in words})
print("lengths      :", {len(w) for w in words})
print("-> duplicates collapse, order is not kept")

# Compare the three forms side by side.
nums = [1, 2, 2, 3]
print()
print("list:", [n * n for n in nums])
print("set :", {n * n for n in nums})
print("dict:", {n: n * n for n in nums})

# The empty-braces trap again: {} is a dict.
print()
print("type of {}      :", type({}).__name__)
print("type of set()   :", type(set()).__name__)
print("type of {1}     :", type({1}).__name__)
print("type of {1: 2}  :", type({1: 2}).__name__)

# A later duplicate key wins, silently.
print()
pairs = [("a", 1), ("b", 2), ("a", 3)]
print("dict comp:", {k: v for k, v in pairs})
'''),
     ],
    ["A colon in the expression makes it a dict comprehension; no colon makes "
     "a set.",
     "<code class='mono-font'>{}</code> is still an empty dict. There is no "
     "empty-set literal.",
     "Duplicate keys are not an error - the last one silently wins.",
     "<code class='mono-font'>{v: k for k, v in d.items()}</code> inverts a "
     "dictionary in one line."],
    """title: Dict and Set Comprehensions: A Practical Guide
intro: The comprehension syntax is not a list feature. The same shape builds dictionaries and sets; only the brackets and the expression change.

## Three forms, one idea

[n * n for n in nums]&nbsp;&nbsp;&nbsp;&nbsp;# list<br>{n * n for n in nums}&nbsp;&nbsp;&nbsp;&nbsp;# set<br>{n: n * n for n in nums}&nbsp;# dict

Square brackets build a list. Braces build a set. Braces with a `key: value` in the expression slot build a dict. The `for` clause and any trailing `if` work identically in all three.

## Dict comprehensions

{w: len(w) for w in words}

The colon is the whole difference. Everything before it is the key, everything after is the value, and both are ordinary expressions evaluated per item.

Two patterns come up constantly. Inverting:

{v: k for k, v in prices.items()}

and building from parallel lists:

{k: v for k, v in zip(keys, values)}

though `dict(zip(keys, values))` is shorter when there is no transformation to do.

## Duplicate keys do not complain

{k: v for k, v in [("a", 1), ("a", 3)]}

gives `{"a": 3}`. The later value overwrites the earlier one, with no error and no warning. If the input might contain duplicates and you care, that is something to check for, not something Python will tell you about.

## Set comprehensions

{w[0] for w in words}

Braces without a colon. It deduplicates as it builds, which is the point: "the distinct first letters" is one expression rather than a loop plus a `set()` call.

Remember that a set has no order, so the printed result may not match the input order and should not be relied on.

## The empty-braces trap, again

`{}` is an empty dict &mdash; dictionaries claimed the braces long before sets existed. There is no empty-set literal at all; `set()` is the only way. This is worth repeating because it is the one inconsistency in an otherwise tidy family.

## When to use them

Same rule as list comprehensions: when it fits on a line and reads as a sentence. A dict comprehension with a conditional key expression and a filter is a line you will re-read; a loop is fine, and often kinder.
""",
    [{"q": "What does `{n for n in [1, 2, 2]}` build?",
      "options": ["A list", "A dict", "A set with two items", "A set with three items"],
      "answer": 2,
      "why": "Braces with no colon build a set, and a set deduplicates: {1, 2}."},
     {"q": "`{k: v for k, v in [('a', 1), ('a', 2)]}` gives what?",
      "options": ["{'a': 1}", "{'a': 2}", "An error", "{'a': [1, 2]}"],
      "answer": 1,
      "why": "The later duplicate key silently overwrites the earlier value. "
             "Nothing warns you, which matters when the input might have "
             "duplicates."},
     {"q": "How do you write an empty set comprehension result's type literal?",
      "options": ["{}", "set()", "{,}", "[]"],
      "answer": 1,
      "why": "{} is an empty dict. There is no empty-set literal, so set() is "
             "the only way to write one."}],
)


# ---------------------------------------------------------------------------
# 20. Conditional comprehensions
# ---------------------------------------------------------------------------
topic(
    "conditional_comprehensions",
    "Conditional Comprehensions",
    "Filter or Choose",
    "The two places an if can appear in a comprehension, which does which, "
    "and why only one of them takes an else.",
    _svg(_txt(80, 26, "[ x if c else y   for x in xs   if c ]", A, 8) +
         '<path d="M40 32 L40 42" stroke="%s" stroke-width="2"/>' % A +
         _txt(40, 54, "choose", A, 8) +
         '<path d="M128 32 L128 42" stroke="%s" stroke-width="2"/>' % M +
         _txt(128, 54, "filter", M, 8)),
    [("two_ifs.py", '''nums = [1, 2, 3, 4, 5, 6]

# Trailing if: FILTER. Some items are dropped.
print("filter :", [n for n in nums if n % 2 == 0])
print("  -> 3 items out of 6")

# if/else in the expression: CHOOSE. Every item survives.
print("choose :", ["even" if n % 2 == 0 else "odd" for n in nums])
print("  -> 6 items out of 6")

# Both at once: filter first, then choose for what is left.
print()
print("both   :", ["big" if n > 4 else "small" for n in nums if n % 2 == 0])

# A trailing if cannot take an else - it is a filter, not a choice.
# [n for n in nums if n % 2 == 0 else 0]     # SyntaxError
'''),
     ("comprehension_conditions.py", '''rows = [
    {"name": "ana", "score": 91},
    {"name": "bo",  "score": None},
    {"name": "cy",  "score": 45},
]

# Filter out the missing data, then grade what is left.
graded = ["pass" if r["score"] >= 50 else "fail"
          for r in rows if r["score"] is not None]
print("graded    :", graded)

# Order matters: the filter runs first, so the choice never sees None.
# Swap them and this would raise on bo.

# Multiple filters chain as `and`.
print()
nums = range(1, 21)
print("div by 3+5:", [n for n in nums if n % 3 == 0 if n % 5 == 0])
print("same thing:", [n for n in nums if n % 3 == 0 and n % 5 == 0])

# A filter can also use the walrus to avoid computing twice.
print()
words = ["hi", "hello", "hey", "greetings"]
print("long words:", [w.upper() for w in words if len(w) > 3])

# Nested: the filter attaches to the clause it follows.
grid = [[1, 2], [3, 4], [5, 6]]
print()
print("odd cells :", [n for row in grid for n in row if n % 2])
'''),
     ],
    ["Trailing <code class='mono-font'>if</code> = filter. It drops items and "
     "takes no <code class='mono-font'>else</code>.",
     "<code class='mono-font'>if/else</code> in the expression = choose. Every "
     "item survives, with one of two values.",
     "Written together, the filter runs first: the expression only sees items "
     "that passed.",
     "Two trailing <code class='mono-font'>if</code>s mean the same as one "
     "<code class='mono-font'>and</code>."],
    """title: Conditional Comprehensions: A Practical Guide
intro: A comprehension can carry an if in two different places. They do different jobs, only one of them accepts an else, and mixing them up is the single most common comprehension error.

## Filter: the trailing if

[n for n in nums if n % 2 == 0]

This drops items. Six numbers in, three out. The `if` sits after the `for`, and it takes no `else` &mdash; there is nowhere for an alternative to go, because a filter either keeps an item or does not.

Writing `[n for n in nums if n % 2 == 0 else 0]` is a syntax error, and it is worth trying once so the error message becomes familiar.

## Choose: the conditional expression

["even" if n % 2 == 0 else "odd" for n in nums]

This drops nothing. Six numbers in, six strings out. The `if/else` is part of the <em>expression</em> at the front &mdash; it is the conditional expression from earlier in the track, used inside a comprehension &mdash; so it must be complete, and the `else` is mandatory.

## Together

["big" if n &gt; 4 else "small" for n in nums if n % 2 == 0]

Read it in execution order rather than left to right: take each `n`, keep it only if it is even, then turn what survives into "big" or "small". The filter runs first.

That ordering is not a detail. If the filter is removing `None` values, the expression never sees them:

["pass" if r["score"] &gt;= 50 else "fail"<br>&nbsp;for r in rows if r["score"] is not None]

Swap the two and the comparison raises on the first missing score.

## Several filters

[n for n in nums if n % 3 == 0 if n % 5 == 0]

Chained filters mean the same as one `and`. The `and` version is usually clearer; the chained form is worth recognising because you will meet it.

## In nested comprehensions

[n for row in grid for n in row if n % 2]

A trailing `if` attaches to the clause it follows &mdash; here the inner loop. Placing a filter after the first `for` instead would filter rows rather than cells. When there are two loops and a condition, this is where a comprehension starts costing more to read than it saves, and the loop version is the kinder choice.
""",
    [{"q": "Which position takes an `else`?",
      "options": ["The trailing if", "The if/else in the expression at the front",
                  "Both", "Neither"],
      "answer": 1,
      "why": "The expression must produce a value for every item, so its else is "
             "mandatory. The trailing if is a filter and takes none."},
     {"q": "`[x for x in xs if c]` and `[a if c else b for x in xs]` differ how?",
      "options": ["No difference", "The first can drop items; the second always "
                  "returns one value per item", "The second is faster",
                  "The first requires a list"],
      "answer": 1,
      "why": "Filtering changes how many items come out. Choosing changes what "
             "each item becomes, and the count is unchanged."},
     {"q": "In a comprehension with both, which runs first?",
      "options": ["The expression", "The filter", "They run in parallel",
                  "Undefined"],
      "answer": 1,
      "why": "The filter runs first, so the expression only ever sees items that "
             "passed it - which is what makes filtering out None before "
             "comparing safe."}],
)


# ---------------------------------------------------------------------------
# 21. Type conversion
# ---------------------------------------------------------------------------
topic(
    "type_conversion",
    "Type Conversion",
    "Changing Types",
    "Turning text into numbers and back, what converts silently, and what "
    "raises rather than guessing.",
    _svg(_box(16, 34, 40, 24, S) + _txt(36, 50, '"42"') +
         '<path d="M60 46 L96 46" stroke="%s" stroke-width="2"/>' % A +
         _txt(78, 38, "int()", A, 9) +
         _box(100, 34, 40, 24, S, A) + _txt(120, 50, "42", A)),
    [("conversion.py", '''# The constructors are the conversions.
print("int('42')     :", int("42"))
print("float('3.14') :", float("3.14"))
print("str(42)       :", str(42))
print("bool('')      :", bool(""))
print("list('abc')   :", list("abc"))

# int() will not guess about decimals in a string.
print()
try:
    int("3.9")
except ValueError as e:
    print("int('3.9') ->", e)
print("but int(3.9)  :", int(3.9), "  <- truncates, does not round")
print("round(3.9)    :", round(3.9))

# Reading input always gives you text.
print()
text = "10"
print("text + text   :", text + text)
print("int + int     :", int(text) + int(text))
'''),
     ("conversion_care.py", '''# Some conversions are silent and lossy.
print("int(3.99)   :", int(3.99), " <- toward zero, not nearest")
print("int(-3.99)  :", int(-3.99))
print("round(2.5)  :", round(2.5), " <- banker's rounding, not up")
print("round(3.5)  :", round(3.5))

# float cannot represent every decimal exactly.
print()
print("0.1 + 0.2         :", 0.1 + 0.2)
print("0.1 + 0.2 == 0.3  :", 0.1 + 0.2 == 0.3)
print("round to 2 places :", round(0.1 + 0.2, 2) == 0.3)

# Converting safely: try, do not check.
print()
def to_int(text, default=None):
    try:
        return int(text)
    except (ValueError, TypeError):
        return default

for v in ["42", "3.9", "", None, "  7  "]:
    print(f"  {v!r:8} -> {to_int(v)}")
print("-> int() does tolerate surrounding whitespace")

# bool() has surprising members.
print()
for v in [0, 1, "", "0", [], [0], None, {}]:
    print(f"  bool({v!r:5}) = {bool(v)}")
'''),
     ],
    ["The type names are the conversions: "
     "<code class='mono-font'>int()</code>, <code class='mono-font'>float()</code>, "
     "<code class='mono-font'>str()</code>, <code class='mono-font'>list()</code>.",
     "<code class='mono-font'>int(\"3.9\")</code> raises; "
     "<code class='mono-font'>int(3.9)</code> truncates toward zero.",
     "<code class='mono-font'>round(2.5)</code> is 2, not 3 - it rounds to the "
     "nearest even on a tie.",
     "<code class='mono-font'>bool(\"0\")</code> is True. Any non-empty string is."],
    """title: Type Conversion: A Practical Guide
intro: Python does not convert types behind your back. You ask, using the type name as a function, and it either succeeds or raises &mdash; it will not guess.

## The constructors

int("42")&nbsp;&nbsp;&nbsp;&nbsp;float("3.14")&nbsp;&nbsp;&nbsp;&nbsp;str(42)&nbsp;&nbsp;&nbsp;&nbsp;list("abc")&nbsp;&nbsp;&nbsp;&nbsp;bool("")

Each type's name doubles as its conversion. That is why there is nothing to memorise beyond the types themselves.

## Text in, text out

Anything read from a user, a file or a network arrives as text. `"10" + "10"` is `"1010"`, and no error is raised, because concatenating strings is a perfectly sensible thing to do. Converting is on you:

int(text) + int(text)

This is the single most common source of confusion for beginners, and it is not really about conversion &mdash; it is about noticing that input is always a string.

## int() is strict about strings and loose about floats

int("3.9")&nbsp;&nbsp;# ValueError<br>int(3.9)&nbsp;&nbsp;&nbsp;&nbsp;# 3

From a string, `int` refuses anything that is not a whole number, because guessing which way to go would be a decision it has no business making. From a float, it truncates toward zero &mdash; `int(-3.9)` is `-3`, not `-4`. If you want nearest, say `round`.

It does tolerate surrounding whitespace, which is convenient when parsing scruffy input.

## round() does not round half up

round(2.5)&nbsp;&nbsp;# 2<br>round(3.5)&nbsp;&nbsp;# 4

On an exact tie, Python rounds to the nearest <em>even</em> number. This is deliberate: always rounding halves up biases a long run of numbers upward. It surprises people once, and it is correct.

## Floats are not decimals

0.1 + 0.2 == 0.3&nbsp;&nbsp;# False

Binary floating point cannot represent 0.1 exactly, so the sum is a hair off. This is not a Python quirk; it is how floats work everywhere. Compare with a tolerance, round before comparing, or use `decimal.Decimal` for money.

## Converting safely

Do not check first &mdash; try, and handle the failure:

try:<br>&nbsp;&nbsp;&nbsp;&nbsp;return int(text)<br>except (ValueError, TypeError):<br>&nbsp;&nbsp;&nbsp;&nbsp;return default

`ValueError` covers bad text and `TypeError` covers `None`. Testing `text.isdigit()` first looks tidier and gets negative numbers and whitespace wrong.

## bool() is broader than it looks

`bool("0")` is `True`, because the string is not empty. Falsy values are: `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None` and `False`. Everything else is truthy, including `"False"`.
""",
    [{"q": "What does `int(\"3.9\")` do?",
      "options": ["Returns 3", "Returns 4", "Raises ValueError", "Returns 3.9"],
      "answer": 2,
      "why": "From a string, int refuses anything that is not a whole number. "
             "From a float, int(3.9) truncates to 3 - the two behave "
             "differently on purpose."},
     {"q": "`round(2.5)` returns what?",
      "options": ["3", "2", "2.5", "An error"],
      "answer": 1,
      "why": "Python rounds a tie to the nearest even number, which avoids "
             "biasing a long run of values upward. round(3.5) is 4."},
     {"q": "`bool(\"0\")` is:",
      "options": ["False", "True", "An error", "0"],
      "answer": 1,
      "why": "Only an empty string is falsy. \"0\" has a character in it, so it "
             "is True - a classic bug when reading text input."}],
)


# ---------------------------------------------------------------------------
# 22. None and truthiness
# ---------------------------------------------------------------------------
topic(
    "none_and_truthiness",
    "None and Truthiness",
    "Empty, Missing, False",
    "What counts as false in a condition, how None differs from empty, and "
    "why `is None` is not the same test as `not x`.",
    _svg(_box(14, 30, 42, 28, S) + _txt(35, 47, "None", M) +
         _box(60, 30, 42, 28, S) + _txt(81, 47, '""', M) +
         _box(106, 30, 42, 28, S, A) + _txt(127, 47, "0", A) +
         _txt(80, 72, "all falsy, all different", M, 8)),
    [("truthiness.py", '''# Anything can be used in a condition. These are the falsy values.
falsy = [None, False, 0, 0.0, "", [], {}, set()]
for v in falsy:
    print(f"  bool({v!r:6}) = {bool(v)}")

print()
truthy = ["0", "False", [0], {0: 0}, -1, 0.1]
for v in truthy:
    print(f"  bool({v!r:8}) = {bool(v)}")

# The idiomatic empty test.
items = []
if not items:
    print()
    print("empty list -> `if not items` is the usual test")
'''),
     ("none_vs_empty.py", '''def find(items, target):
    for i, x in enumerate(items):
        if x == target:
            return i
    return None

items = ["a", "b", "c"]

# The bug: index 0 is falsy, so `if not result` treats "found at 0"
# exactly like "not found".
for target in ("a", "z"):
    result = find(items, target)
    if not result:
        print(f"{target!r}: reported as NOT FOUND   (result={result!r})")
    else:
        print(f"{target!r}: found at {result}")

print("-> 'a' was found at index 0 and got reported as missing")

# The fix: test for None specifically.
print()
for target in ("a", "z"):
    result = find(items, target)
    if result is None:
        print(f"{target!r}: not found")
    else:
        print(f"{target!r}: found at {result}")

# Why `is` and not `==`: None is a single object.
print()
print("None is None :", None is None)
print("same object  :", id(None) == id(None))
'''),
     ],
    ["Falsy: <code class='mono-font'>None</code>, "
     "<code class='mono-font'>False</code>, <code class='mono-font'>0</code>, "
     "<code class='mono-font'>0.0</code>, <code class='mono-font'>\"\"</code>, "
     "<code class='mono-font'>[]</code>, <code class='mono-font'>{}</code>, "
     "<code class='mono-font'>set()</code>. Everything else is truthy.",
     "<code class='mono-font'>not x</code> means \"empty or zero or missing\". "
     "<code class='mono-font'>x is None</code> means only \"missing\".",
     "Use <code class='mono-font'>is None</code>, not "
     "<code class='mono-font'>== None</code>: there is exactly one None object.",
     "<code class='mono-font'>if not result</code> on a function that can return "
     "0 is a real bug, not a style question."],
    """title: None and Truthiness: A Practical Guide
intro: Any value can be used in a condition. Knowing which ones count as false, and when that is the wrong question to ask, prevents a class of bug that produces no error at all.

## The falsy values

There are not many, and the list is worth memorising:

None&nbsp;&nbsp;False&nbsp;&nbsp;0&nbsp;&nbsp;0.0&nbsp;&nbsp;""&nbsp;&nbsp;[]&nbsp;&nbsp;{}&nbsp;&nbsp;set()

Everything else is truthy. That includes `"0"`, `"False"`, `[0]` and `-1`, all of which catch people out because they look empty or negative in some sense and are not.

## The idiomatic empty test

if not items:

is how Python asks "is this empty?", and it is preferred over `len(items) == 0` because it works on anything and reads as prose. For a list, a string or a dict, this is right and unremarkable.

## Where it goes wrong

The trouble starts when a value can legitimately be `0` or `""`:

result = find(items, "a")&nbsp;&nbsp;# returns index 0<br>if not result:<br>&nbsp;&nbsp;&nbsp;&nbsp;print("not found")&nbsp;&nbsp;# WRONG

Index 0 is falsy, so "found at the first position" and "not found at all" take the same branch. Nothing raises. The program is simply wrong for one input, and that input is the first element, which many test cases skip.

The page runs exactly this, printing the wrong answer and then the fix.

## `is None` asks a different question

if result is None:

This tests for one specific object, not for emptiness. It is true for `None` and nothing else &mdash; not for `0`, not for `""`. When a function returns "the thing, or None if there isn't one", this is the only correct test.

The rule that follows: use truthiness when you mean "empty or zero or missing, and I treat them the same". Use `is None` when `None` means something distinct from a legitimate empty value.

## Why `is` rather than `==`

There is exactly one `None` object in a running program, so identity is the precise test and it is faster than equality. It also cannot be fooled: a class can define `__eq__` so that `x == None` is true for something that is not `None`. `is` compares the object itself.

The same applies to the two default-argument patterns from earlier in the track: `if basket is None` is correct, and `if not basket` would treat an intentionally empty list as missing.
""",
    [{"q": "Which of these is truthy?",
      "options": ["0", "''", "'0'", "[]"],
      "answer": 2,
      "why": "'0' is a non-empty string, so it is True. Only the empty string is "
             "falsy - which bites when reading text input."},
     {"q": "A function returns an index or None. Why is `if not result` a bug?",
      "options": ["It is slower", "Index 0 is falsy, so a real result is treated "
                  "as missing", "not cannot be used on integers",
                  "It raises on None"],
      "answer": 1,
      "why": "0 and None both take the false branch, so finding something at the "
             "first position reports as not found. Nothing raises; the answer is "
             "just wrong."},
     {"q": "Why `is None` rather than `== None`?",
      "options": ["They are identical", "There is one None object, so identity is "
                  "exact and cannot be overridden", "`==` is deprecated",
                  "`is` works on more types"],
      "answer": 1,
      "why": "None is a singleton, so identity is the precise test. A class can "
             "define __eq__ to make == None true for something that is not None."}],
)


# The MCQ bank, keyed the way tools/labs.py keys everything else.
CHECKS = {
    "python/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS
}
