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


# The MCQ bank, keyed the way tools/labs.py keys everything else.
CHECKS = {
    "python/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS
}
