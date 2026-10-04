# -*- coding: utf-8 -*-
"""Additional article sections for the generated Python modules.

The first pass wrote roughly 300 words per topic, which is enough to explain a
feature and not enough to be worth landing on. These sections take each one to
around 800: a worked example with real values, the mistakes people actually
make, and where the feature sits next to its alternatives.

Kept separate from python_topics.py so neither file becomes unreadable. The
text is appended to each topic's article by slug; a topic with no entry here
simply keeps what it had.
"""

EXTRA = {}


def add(slug, text):
    EXTRA[slug] = text.rstrip() + "\n"


add("tuples_and_unpacking", """
## Unpacking in places you did not expect

Unpacking isn't limited to set. It's how a for loop reads pairs:

```python
for name, score in [("ana", 91), ("bo", 78)]:
    print(name, score)
```

Each item is a two-tuple, and the loop unpacks it into two names on the way
in. `dict.items()` yields tuples. This Is why `for k, v in d.items()` works
at all, and `enumerate` yields `(index, value)` for the same reason.

A star collects the middle:

```python
first, *rest = [1, 2, 3, 4]      # first = 1, rest = [2, 3, 4]
head, *body, tail = "a b c d".split()
```

The starred name always turns a list, even when it captures nothing, which
means `rest` is `[]` rather than `None` for a one-item sequence. That is worth
knowing before you write `if rest is None`.

## Where the wrong number of names bites

```python
x, y = (1, 2, 3)
```

raises `ValueError: too many values to unpack`. That looks like an annoyance
and is a safety net: it fires the moment the shape of your data changes. Code
that indexed `point[0]` and `point[1]` would have carried on quietly with a
three-element point and made wrong answers much later.

The same error appears when a function you expected to return two things
returns one, which is often the real bug rather than the unpacking.

## Named tuples, when positions stop being obvious

Spot-based access stops reading well past two or three fields. `record[4]`
tells no one any of it.

```python
from collections import namedtuple

Point = namedtuple("Point", "x y")
p = Point(3, 4)
print(p.x, p[0])        # both work
```

A named tuple is still a tuple - immutable, hashable, unpackable - but its
fields have names. It costs one line and it's the usual answer when a plain
tuple has grown past the point where you can note what spot two was.
""")


add("sets_and_set_operations", """
## Order, and why you cannot rely on it

A set has no order. Printing one twice in the same run often gives the same
setup, which tempts people into based on it, and that setup
can change between runs or between versions. If you need a stable order, sort
on the way out:

```python
for name in sorted(unique_names):
    ...
```

If you need to keep the order things first appeared, a set is the wrong tool:

```python
list(dict.fromkeys(items))     # de-duplicated, original order kept
```

Dicts preserve insertion order, so this is the standard trick for
"unique but in the order I saw them".

## Modifying a set

```python
seen.add("x")          # one item
seen.update(others)    # many
seen.discard("x")      # remove, no error if absent
seen.remove("x")       # remove, KeyError if absent
```

`discard` and `drop` differ only in what happens when the item isn't there,
and choosing between them is a small design choice: `drop` says "this
should have been present", `discard` says "get rid of it if it's".

The operators have in-place forms too: `a |= b` adds all from b, `a &= b`
keeps only what both share.

## A frozen set, for when a set needs to be a key

Sets are mutable, so a set can't be a dict key or a member of another
set. `frozenset` is the immutable version:

```python
groups = {frozenset({"ana", "bo"}): "pair one"}
```

This comes up when the key is truly a collection - a set of tags, a group
of users - and you need to look a thing up by it.

## The cost, concretely

Building a set from a list is one pass. Converting is cheap. The win comes
when you test membership more than once. Converting a list to a set to do a
single lookup is slower than just scanning the list. Converting once and then
testing thousands of times is the case the second program on this page
measures, and there the difference isn't subtle.
""")


add("nested_for_loops", """
## Reading a grid, row by row

The most common nested loop walks a two-dimensional structure:

```python
grid = [[1, 2, 3], [4, 5, 6]]
for row in grid:
    for value in row:
        print(value, end=" ")
    print()
```

The outer loop takes a row - itself a list - and the inner loop takes the
values in it. Note that the outer variable holds a whole row, not an index,
which is what makes this read better than the `for i in range(len(grid))`
version.

When you need the coords as well, `enumerate` supplies them at both
levels:

```python
for r, row in enumerate(grid):
    for c, value in enumerate(row):
        print(r, c, value)
```

## Breaking out of both

`break` leaves one loop. Three ways to leave two, in order of preference:

```python
def find(grid, target):              # 1. a function, and return
    for row in grid:
        for value in row:
            if value == target:
                return value
```

```python
found = None                         # 2. a flag the outer loop checks
for row in grid:
    for value in row:
        if value == target:
            found = value
            break
    if found is not None:
        break
```

The function is almost always the right answer: `return` leaves all, and
the search gets a name.

## When nesting is hiding a better idea

Two loops over the same collection compare each pair, and that is `n squared`
work for a question that often has a one-pass answer.

```python
for a in nums:                      # every pair - slow
    for b in nums:
        if a + b == target:
            ...
```

```python
seen = set()                        # one pass
for n in nums:
    if target - n in seen:
        ...
    seen.add(n)
```

The rule of thumb: if the inner loop is searching for a thing, a set or a
dict often drops it. If the two loops walk truly different
things - rows and columns, users and permissions - the nesting is correct and
there's nothing to drop.
""")


add("list_comprehensions", """
## A worked example, step by step

Take a list of records and pull out the names of everyone who passed:

```python
rows = [{"name": "ana", "score": 91},
        {"name": "bo", "score": 43},
        {"name": "cy", "score": 68}]

passed = [r["name"] for r in rows if r["score"] >= 50]
```

Read it in the order it executes. This Isn't the order it's written: take
each `r` from `rows`, keep it if the score clears 50, and collect
`r["name"]`. The formula at the front is applied last, to what lives
the filter.

Written as a loop that is four lines and one more variable to name.

## The variable does not leak

```python
squares = [n * n for n in range(5)]
print(n)        # NameError
```

The loop variable belongs to the comprehension and is gone afterwards. That is
a deliberate difference from a `for` statement, whose variable outlives the
loop, and it's the reason a comprehension can't quietly overwrite an `n` you
were using elsewhere.

## Conditional expression versus filter, once more

These two look similar and do different jobs:

```python
[n for n in nums if n > 0]                 # filter: some items are dropped
["pos" if n > 0 else "neg" for n in nums]  # map: every item is kept
```

The first can return a shorter list. The second always returns one item per
input. If you find yourself wanting `if ... else` at the end, you almost
certainly want it at the front instead.

## Building a dict or a set the same way

The syntax generalises:

```python
{w: len(w) for w in words}      # dict comprehension
{len(w) for w in words}         # set comprehension
```

Braces with a colon give a dict. Braces without give a set. Both take the
same trailing `if`, and both are worth reaching for when the loop version would
be three lines of `result[key] = value`.
""")


add("f_strings_and_formatting", """
## Formatting a table without counting spaces

Alignment is where the format spec earns its keep. Left-align text, right-align
numbers, and the columns line up what the data:

```python
rows = [("apple", 3, 1.5), ("banana", 12, 0.25), ("cherry", 100, 12.0)]
print(f"{'item':<10}{'qty':>5}{'price':>10}")
for item, qty, price in rows:
    print(f"{item:<10}{qty:>5}{price:>10.2f}")
```

`<` left, `>` right, `^` centre, and the number after it's the field width.
Numbers right-aligned with a fixed number of decimals is the combination you
will use most, because it puts the decimal points under each other.

## Dates, and why the same syntax works

The spec after the colon is handed to the object being formatted, so types can
define their own:

```python
from datetime import datetime
now = datetime(2026, 8, 20, 14, 30)
print(f"{now:%d %B %Y}")      # 20 August 2026
print(f"{now:%H:%M}")         # 14:30
```

That isn't a special date feature of f-strings. It's `datetime` reading
the spec it was given. The same mechanism is why `:.2f` means a thing to a
float and nothing to a string.

## Quotes inside the braces

Before Python 3.12 you couldn't reuse the outer quote character inside the
formula:

```python
f"{d['key']}"        # fine: single inside double
f"{d["key"]}"        # SyntaxError before 3.12, allowed after
```

Sticking to the older form costs nothing and works all over, which is the
usual reason to keep doing it.

## Escaping a brace

A literal brace is doubled:

```python
print(f"{{not a placeholder}} but {2 + 2} is")
# {not a placeholder} but 4 is
```

This matters when you're making JSON, CSS or any of it else that uses
braces, and it's the first thing to check when an f-string raises a confusing
`KeyError`.
""")


add("function_arguments", """
## Keyword-only parameters

any of it after a bare `*` in the meaning can only be passed by name:

```python
def connect(host, *, timeout=30, retries=3):
    ...

connect("db.local", timeout=5)      # fine
connect("db.local", 5)              # TypeError
```

This is how you stop a call site from turning a row of untagged values.
`connect("db.local", 5, 2)` tells a reader nothing. Forcing the names makes the
call self-documenting, and it means you can reorder or add options later
without breaking anyone.

The mirror image is `/`. This Marks params as spot-based-only. It appears
in the standard library more than in use code.

## Arguments are evaluated at the call

```python
def log(message, when=now()):    # now() runs ONCE, at definition
```

This is the same rule as the mutable default, wearing different clothes. If you
want the current time on each call, find it inside:

```python
def log(message, when=None):
    if when is None:
        when = now()
```

Any formula in a default - a function call, a list, a dict, an object - is
tested once when the `def` statement runs, and the result is reused forever.

## Too many parameters is a design signal

A function with eight params is hard to call right and hard to change.
Two usual remedies:

- group related args into a small object or a dataclass, so `draw(config)`
  replaces `draw(x, y, w, h, colour, border, alpha, z)`
- split the function, because eight params often means it's doing more
  than one job

Neither is a rule, but if you're counting args on your fingers at the
call site, the call site is telling you a thing.

## Argument order in the definition

Spot-based first, then defaults, then `*args`, then keyword-only, then
`**kwargs`. Python enforces most of that, and the error messages are clear when
you get it wrong - unlike the mutable default. This Never complains at all.
""")


# --------------------------------------------------------------------------
# Second pass over the first six: the sections above lean on code, and code
# does not count as reading. These add the explanation around it.
# --------------------------------------------------------------------------

def extend(slug, text):
    EXTRA[slug] = EXTRA.get(slug, "") + text.rstrip() + "\n"


extend("tuples_and_unpacking", """
## Why immutability is not just a restriction

It's tempting to read "can't be changed" as a limitation you work around. In
practice it's a property you lean on. An immutable object can be shared freely
between functions, threads and data structures, because no holder of it can
surprise another holder by editing it. That is why the language reaches for
tuples in just the places where a surprise would be costly: function
args arrive as a tuple, exceptions carry their args as a tuple, and a
function returning a few values returns a tuple rather than a list.

The immutability is shallow, and this catches people. A tuple ensures that
its slots keep pointing at the same objects. It says nothing about those
objects. A tuple holding a list will happily let you append to that list,
and the tuple is unchanged as far as Python is concerned, because it still
points at the same list. This is also why such a tuple isn't hashable: its
contents can change, so any hash found from them would go stale.

## Choosing between a tuple, a list and a small class

Three options, and the choice is often about what the spots mean.

A list is right when the items are the same kind of thing and the collection
grows, shrinks or gets sorted: a list of scores, a list of users, a queue of
jobs. spot carries no meaning beyond order.

A tuple is right when the group is fixed at creation and each spot means
a thing exact: a coord pair, an RGB colour, a DB row. spot
is the meaning, which is just why the group must not change length.

A small class or a dataclass takes over when there are more than about three
fields, or when you find yourself writing a comment to note what spot
three was. Names beat spots the moment spots stop being obvious, and a
named tuple is the halfway house that keeps tuple action while adding them.
""")


extend("sets_and_set_operations", """
## What "hashable" is really asking

A set decides where to store an item by finding its hash. The hash has to
stay the same for if the item is in the set. That is the entire reason
lists and dicts can't be set members: they can change, the hash would
change with them, and the set would be looking in the wrong place for a thing
it definitely holds.

This isn't a rule Python invented to be awkward. It falls straight out of how
the lookup works. The same constraint applies to dict keys, which is why
the two rules are always taught together, and why the error message mentions
hashability rather than mutability.

Strings, numbers, booleans, `None` and tuples of those are all hashable and can
go in a set. any of it you can mutate can't.

## Sets in everyday code

Three patterns cover most real uses.

Deduplication is the obvious one: `set(values)` merges repeats in a single
pass, and wrapping it in `sorted()` gives back a predictable order.

Membership testing is the key one. Any time a loop holds `if x in
a thing`, ask what `a thing` is. If it's a list that doesn't change during
the loop, converting it to a set once before the loop turns a scan into a
lookup, and that single change is often the entire fix for a slow function.

Checking two collections is the one people forget exists. "Which users are in
both groups", "which needed fields are missing", "which files changed" are all
one operator rather than a loop with an `if` inside it, and the operator version
is far harder to get subtly wrong.
""")


extend("nested_for_loops", """
## Reading the cost without timing anything

You can tell the cost of a nested loop by reading it. Count how many times each
loop runs and times. Two loops over the same n-item list run n times n. A
loop over n holding a loop over m runs n times m. A loop over n holding a
lookup in a set runs n times, because the lookup doesn't loop.

That last one is the key case. A nested loop and a loop holding a set
lookup can look almost the same on the page and behave fully differently
at scale, and the difference is invisible on ten items and decisive on ten
thousand.

This is also why the timings on this page are run at three sizes rather than
one. A single reading tells you how long a thing took. Three tell you how
the time grows, which is the thing that really matters when your data gets
bigger.

## Depth, and when to stop

Two levels of nesting is plain. Three is worth a second look. Four is nearly
always a sign that some of the structure belongs in a function, because by then
no one can hold all the loop variables in their head at once, and the
indentation alone pushes the real work off the right of the screen.

Pulling the inner loops into a named function costs nothing at runtime and
gives each level a name that says what it's iterating over. It also gives you
`return`, which is the cleanest way out of nested loops there's.
""")


extend("list_comprehensions", """
## What a comprehension is really for

The value of a comprehension isn't that it's shorter. It's that it says
"this is a change" in a way a loop can't. A loop that builds a list is
three separate statements - create, iterate, append - and a reader has to hold
all three to work out that nothing else is happening in between. A
comprehension states the shape of the result on the first line, and there's
nowhere for any of it else to hide.

That is also the test for whether you should use one. If the body does one
thing to each item, a comprehension expresses it better. If it does a few
things, updates a thing outside itself, or needs a `try`, the loop isn't just
acceptable but correct, because those are just the things a comprehension
can't hold and shouldn't be contorted into.

## A note on nesting

A comprehension holding a second `for` is a nested loop, and it's subject to
the same times of work given elsewhere on this site. Flattening a
list of lists is a fair use. Checking each pair of items isn't - it's the
same quadratic cost written more compactly, and compactness is the last thing
that helps when a thing is slow.
""")


extend("f_strings_and_formatting", """
## Why f-strings replaced everything before them

Python has had four ways to build a string with values in it, and the
differences are about where the values sit scaled to the text.

Concatenation with `+` scatters the sentence across quotes and plus signs, and
needs `str()` around any of it that isn't already a string. Percent
formatting moves the values to the end. So Reading the sentence means jumping
between the template and the tuple. `str.format` is the same shape with better
syntax. An f-string puts each value just where it will appear in the output.

That single property is why the mistakes go away. You can't pass the args
in the wrong order, because there's no separate arg list. You can't
supply too few, because each slot holds its own formula. And you can read
the line and know what it prints without looking anywhere else.

## What belongs inside the braces

Any formula is legal. This Means a great deal is possible and rather less
is wise. A variable, an field, a dict lookup, a short method call or
a small math formula all read fine. A nested comprehension or a long
if-based doesn't: by the time the reader has parsed it they've lost the
sentence it was embedded in.

The rule that holds up is that an f-string should still read as a sentence with
holes in it. When the hole is bigger than the sentence, find the value on
the line above and give it a name.

## Formatting and correctness

One habit worth keeping: format at the edge, never in the middle. Keep full
precision in your variables and apply `:.2f` only where the value is printed or
written out. Rounding early and then continuing to find is how totals stop
matching the numbers above them, and it's a truly common source of small,
hard-to-explain discrepancies in reports.
""")


extend("function_arguments", """
## What the signature communicates

A function signature is the part other people read most and change least. It's
worth treating as an interface rather than an accident of how the function grew.

Params with no default are needs: the caller must supply them and the
function can't work without them. Params with defaults are options, and the
default should be the choice that is right most of the time. If you find
yourself writing a default that callers nearly always override, the default is
wrong and it's quietly making each call site longer.

Order matters for reading as much as for the language. Put the thing the
function is about first - the data, the object, the path - and the modifiers
after it. `resize(image, width=800)` reads right. `resize(width=800,
image=img)` is legal and reads backwards.

## Passing arguments through

When one function calls another and wants to forward what it was given, the
star forms do it without repeating the signature. That is the right tool for
wrappers, decorators and thin adapters. Here Repeating the params would
mean updating two places each time the inner function changes.

It's the wrong tool for a function people call right. `def process(*args,
**kwargs)` gives the caller no idea what to pass, gives the editor nothing to
complete, and turns a mistake that would have been a clear `TypeError` into a
`KeyError` a place deeper. Be clear at the surface and flexible only where
you're truly forwarding.

## Mutable arguments, not just mutable defaults

The default-arg trap gets the focus. But The same underlying fact -
that args are passed by ref to the same object - applies to each
call. A function that appends to a list it was given has changed the caller's
list. at times that is the point and should be said in the name: `add_item`,
`update_config`, `sort_in_place`. When it isn't the point, copy at the top of
the function or return a new object, and let the caller decide.
""")


add("args_and_kwargs", """
## Where you will actually meet them

Almost each use of `*args` and `**kwargs` in real code falls into one of three
shapes, and recognising them makes the feature far less abstract.

The first is a function that truly takes an unknown number of things:
`print`, `max`, `os.path.join`. These are rare to write and common to use.

The second is a wrapper. A decorator, a retry helper, a logging shim - any of it
that stands in front of another function and passes the call along. Here the
star forms aren't a convenience, they're the only way to write the wrapper
without hard-coding the signature of all it might wrap.

The third is a subclass extending its parent. `def __init__(self, *args,
extra=None, **kwargs)` accepts what the parent accepts, adds one option of
its own, and forwards the rest with `super().__init__(*args, **kwargs)`. This
keeps working when the parent gains a param. This Is the whole point.

## The cost of being too flexible

A signature of `(*args, **kwargs)` accepts all, and that is its problem
and its purpose. No one can tell what the function wants by reading it.
An editor can't autocomplete the call. A typo in a keyword name no longer
raises a clear `TypeError` about an unexpected arg - it lands silently in
`kwargs` and surfaces later as a missing key, or worse, as a default quietly
being used instead of the value you thought you passed.

So the rule is about spot in the system rather than taste. At the surface,
where people call your code right, name the params. In the middle, where
you're forwarding a call you didn't make, use the stars. The further a
function is from a human caller, the more flexibility costs you nothing.

## Reading someone else's signature

When you meet `def f(a, b=1, *args, c, **kwargs)`, read it in the order Python
binds it. `a` is needed and spot-based. `b` is spot-based with a default.
`args` collects any further spot-based args. `c` comes after `*args`, which
makes it keyword-only and, because it has no default, needed by name.
`kwargs` collects the rest.

The one that surprises people is `c`. any of it after `*args` can only be passed
by keyword, whether or not it has a default. That is the mechanism behind
keyword-only params, and it's why library authors at times write a bare
`*` in a signature: it turns all after it into a name you've to say
out loud at the call site.
""")


add("variable_scope", """
## Why the rule exists

Deciding local-or-not at compile time looks like an odd choice until you
consider the option. If Python worked out scope while running, then whether
a name was local could depend on which branch had ran, and the same line
could mean two different things on two different runs. Instead the compiler
scans the whole function body once: if a name is assigned anywhere in it, that
name is local all over in it.

That single rule shows the `UnboundLocalError` that catches everyone. The
read on line one is a read of a local variable. Line five assigns to it,
and the local has no value yet. The error message is precise. It just shows
a choice made before the function ran.

## Closures, and why they are useful

A function defined inside another function can see the enclosing function's
variables, and it keeps seeing them after the outer function has returned. That
combination - an inner function plus the variables it captured - is a closure,
and it's how a function can carry state without a class or a global.

The counter on this page is the small version. The pattern scales to
configuration: a function that builds and returns another function with some
settings already baked in. `make_formatter(currency="GBP")` returns a thing
you can call many times without repeating the currency.

`nonlocal` exists because assigning inside the inner function would or else
create a new local there, just as it would at module level. It says "this
name belongs to the function that wraps me", and it's the only way to update
captured state rather than merely read it.

## Globals, and when they stop being harmless

Reading a module-level constant from inside a function is plain and fine -
that is what constants are for. Writing to a module-level name from inside a
function is where trouble starts, because the function's action now depends
on what ran before it, and testing it in alone stops being possible.

The hands-on test is whether calling the function twice with the same args
gives the same answer. If a `global` statement means it doesn't, the state
probably wants to be a param, a return value, or an field on an object -
all three of which make the dependency visible in the signature rather than
buried in the body.

## Shadowing builtins

`list`, `dict`, `set`, `id`, `type`, `sum`, `input` and `max` are all plain
names that happen to be defined in the builtin scope, and assigning to any of
them inside your code hides the first for the rest of that scope. It's legal
and it makes confusing failures later, often when a thing calls `list(x)`
and gets a `TypeError` about your list not being callable.
""")


add("try_and_except", """
## Which exceptions to expect

The instruction to catch exact exceptions is easy to agree with and harder to
follow, because it needs knowing what a piece of code can raise. Three ways
to find out, in order of trust.

Read the docs: the standard library is clear about what its
functions raise, and `int()`, `open()` and `dict` lookups all doc theirs.
Run it and see: trigger the failure on purpose once, read the traceback, and
catch what really appeared. And reason about it: an op that parses can
raise `ValueError`, one that touches the filesystem can raise `OSError`, one
that indexes can raise `IndexError` or `KeyError`.

Catching `Exception` is the honest middle ground when you truly can't
enumerate them - a plugin boundary, a top-level handler that must not crash the
program - and it's different from a bare `except`, because it still lets
`KeyboardInterrupt` and `SystemExit` through. Those two are how a user stops
your program, and swallowing them is how a program turns hopeless to quit.

## Keep the try block small

A `try` that wraps twenty lines catches errors from all twenty, including ones
you never thought about. If the handler says "couldn't parse the date", but the
block also holds a DB call, then a DB failure now reports itself
as a date problem, and the person debugging it starts in the wrong place.

Wrap the line that can fail, and put the follow-up work in `else`. The block
stays honest about what it's handling.

## Failing loudly is usually right

There's a reflex, above all early on, to wrap any of it that has ever raised in
a `try` and carry on. It feels defensive. What it really does is convert a
loud, located failure into a quiet, wrong result that surfaces a place else
with no traceback pointing home.

An exception isn't automatically a problem to suppress. It's info, and
often the most handy info the program will give. Handle the ones you
have a real answer for - a missing optional file, a user typing letters into a
number field, a network call worth retrying - and let the rest travel. A crash
in development is a bug report that writes itself.

## Cleanup belongs to `with`

`finally` ensures that cleanup runs, and for files, locks and links
there's a better tool: a context manager. `with open(...)` closes the file
whether the block succeeded or raised, without the extra indentation and without
the risk of losing. Reach for `finally` when there's no context manager for
what you're doing, and for `with` when there's.
""")


add("classes_and_objects", """
## When a class is the right answer

Not all should be a class. Python isn't a language where you've to
wrap a function in one to run it. A module full of functions is a just right
good design.

The signal that you want a class is data and action travelling together. If
a few functions all take the same three args, and those three args
always change as a group, they're showing one thing that doesn't have a
name yet. Giving it a name and hanging the functions off it as methods drops
the repetition and makes the tie clear.

The opposite signal is a class with one method and no state beyond what that
method was passed. That is a function wearing a costume, and the function is
easier to test, easier to import and easier to read.

## State is the thing to be careful with

An object's fields are its state, and state is what makes code harder to
reason about, because the answer to "what does this method return" turns "it
depends what happened earlier". That isn't an arg against classes. It's
an arg for keeping state small and obvious.

Two habits help. Set each field in `__init__`, even if only to `None`, so
that reading the constructor tells you all the object holds - fields
appearing halfway through some other method are how objects become mysterious.
And prefer methods that return new values over methods that quietly mutate the
object, unless mutation is the point and the name says so.

## The underscore convention

Python has no private fields. A leading underscore - `self._cache` - is a
rule meaning "this is inner, don't lean on it", and nothing enforces
it. That sounds weak and works oddly well: it marks the boundary between
what you promise and what you may change. This Is all the gap was ever
for.

A double leading underscore triggers name mangling. This Is a different feature
aimed at avoiding clashes in subclasses rather than at privacy. It's rarely
what you want.

## Dataclasses, for when it is mostly data

If a class exists chiefly to hold fields, the standard library will write the
boilerplate:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

That gives you `__init__`, a readable `__repr__` and equality check for
free, which is three of the things you'd or else write by hand and one -
`__repr__` - that people often skip and then miss the first time they print a
list of them.
""")


add("conditional_expressions", """
## Where it belongs, and where it does not

A if-based formula is at its best when the two values are short, closely
related, and the rule is easy to read. `"pass" if score >= 50 else "fail"`
is a sentence. `compute_full_report(user, opts) if user.is_active and not
user.suspended else default_report()` isn't, though it's legal and does
the same kind of job.

The hands-on test is whether the line still reads left to right in one pass. If
your eye has to go back to the middle to find the rule, or the line wraps,
the statement form will be clearer and will cost you three extra lines that
no one has ever regretted.

## In default values and arguments

One place the formula form is truly the only option is inside another
formula. Function args are the common case:

```python
connect(host, timeout=timeout if timeout else DEFAULT_TIMEOUT)
```

and so are dict values, list elements and f-string slots. You can't put
an `if` statement in any of those. If the choice has to happen there, this is
how it happens.

Worth noticing in that example: `timeout if timeout else DEFAULT` has the same
falsy-value problem as `or`. If zero is a legitimate timeout meaning "don't
wait", this discards it. `timeout if timeout isn't None else DEFAULT` is the
version that lives contact with real data.

## Nesting, and the readable alternative

Chained if-based expressions are the classic overreach, and the reason is
that they invert how people read a choice. A reader looking for the default
case has to scan to the very end of the line. Adding a band means editing
the middle of a long string of `else`s.

When the mapping is from ranges to values, a small loop over pairs often reads
better than either the chain or a stack of `if`s:

```python
BANDS = [(90, "A"), (80, "B"), (70, "C")]

def grade(score):
    for cutoff, letter in BANDS:
        if score >= cutoff:
            return letter
    return "F"
```

The bands are now data. This Means they can be changed, tested and displayed
without touching the logic. That is often the real win, and it's easy to
miss while arguing about one-liners.
""")


add("match_and_case", """
## Why it was added

Python resisted a switch statement for decades on the grounds that a chain of
`if`/`elif` already did the job, and for checking a value against a few
constants that arg still holds. `match` wasn't added to replace those.

It was added for structural pattern matching: inspecting the *shape* of data and
pulling it apart in the same step. The code it replaces is a stack of
`isinstance` checks, key lookups and length tests, written in a exact order,
where getting the order wrong or losing a check makes a bug that only
appears on unusual input. That pattern shows up constantly in any of it that
handles parsed JSON, events, commands or syntax trees.

Once you see it as "destructure and dispatch" rather than "switch", the design
choices stop looking strange.

## Patterns you will use

Literal patterns match constants. Sequence patterns like `[a, b]` or
`[first, *rest]` match lists and tuples of the right shape and bind the parts.
Mapping patterns like `{"type": "click", "x": x}` match dicts that
*hold* those keys - extra keys are allowed. This Is what makes them handy
against real payloads that carry more than you care about.

Class patterns match an instance and can pull fields out of it:
`case Point(x=0, y=y)` matches a Point on the y-axis and binds `y`. Mixed
with a guard, that covers a surprising amount of dispatch logic in one readable
block.

## The two rules to remember

A bare name captures rather than checks, and it matches all. If you
want to compare against a constant you've stored a place, it must be a
dotted name - `case Status.OK` - or a literal. This is the single most common
`match` bug, and the failure mode is silent: the first such case swallows each
value and the ones below it never run.

And `match` isn't exhaustive. If nothing matches and there's no `case _`,
the statement simply does nothing and run continues. Coming from
languages where the compiler insists on exhaustiveness, that is worth
remembering, because a missing case here is a quiet no-op rather than an error.

## Version, and whether to use it

`match` needs Python 3.10. If your code has to run on any of it older, the
`if`/`elif` version is the only option, and for two or three literal
checks it's the better one even so: shorter, universally understood,
and with none of the capture-pattern sharp edges.
""")


add("loop_else", """
## The name is the whole problem

Nothing about the word "else" suggests "if the loop wasn't broken out of", and
that mismatch is why the feature has a reputation for being confusing rather
than for being handy. The action itself is simple and has no edge cases.

Guido van Rossum has said the keyword was a mistake and that a thing like
`nobreak` would have been clearer. Reading it that way in your head is truly
all it takes. The confusion disappears right away and doesn't come back.

## The shape it belongs to

`for/else` fits one exact shape: a search that must report failure. Loop over
picks, `break` when you find one. The `else` is the "we got to the end
without finding any of it" branch.

That shape appears more often than it first seems - looking up a record,
validating that no item breaks a rule, testing divisibility, scanning for a
delimiter. In each case the option is a boolean flag that exists only to
carry one bit of info past the end of the loop, and each flag is a
chance to forget to set it or to check it in the wrong place.

## When not to use it

If the loop has no `break`, the `else` always runs and is so pure
decoration - it means just the same as putting the code after the loop, but
makes a reader stop and work that out. Delete it.

If the function can simply `return` from inside the loop, that is often
clearer than either version, because the "not found" case turns the last line
of the function rather than an attached block:

```python
def find(items, target):
    for item in items:
        if item == target:
            return item
    return None
```

Most searches inside a function are better written this way. This Is part of
why `for/else` stays uncommon even among people who know it.

## Knowing it matters more than using it

The reason to learn this feature is that you'll read it. It appears in the
standard library and in other people's code, and an unseen make in
someone else's loop is just the kind of thing that makes a reader guess.
Guessing wrong here is easy, because the plain-English reading of "else" is the
opposite of the truth in the case people often check first - the empty
sequence, where the else still runs.
""")


add("nested_conditionals", """
## When nesting is genuinely right

Guard clauses suit functions, because `return` is what makes them possible.
Inside a loop or a block where you can't return, the staircase is at times
unavoidable - though `continue` plays the same role in a loop that `return`
plays in a function, and is under-used for it.

Nesting is also right when the rules are truly dependent: when the
second question only makes sense if the first was true. `if user isn't None:`
followed by `if user.active:` isn't a staircase to flatten, it's two questions
where the second would raise without the first.

## Combining with and or

Two shallow rules can often become one:

```python
if user.active and not user.fines:
```

This is clearer than nesting when the combination is what you mean, and worse
than nesting when you need different responses to each failure - as soon as you
want to tell the user *which* rule stopped them, the rules have to be
separate again.

Both `and` and `or` short-circuit. This Is what makes `if user isn't None and
user.active` safe: the second half is never tested when the first is false.
That sorting is load-bearing, and swapping the halves turns a working check
into an `AttributeError`.

## Depth as a design signal

Three levels of nested rules inside a loop inside a function is often not
a formatting problem, it's a sign that the function is making a few different
choices and would be clearer as two or three named functions. The indentation
is doing you a favour by making that visible.
""")


add("enumerate_function", """
## The start argument

```python
for n, line in enumerate(lines, start=1):
    print(f"{n}: {line}")
```

Line numbers, question numbers, ranked results and any of it else a human reads
often start at one. Passing `start=1` is better than writing `n + 1` inside
the body, because it states the intent once at the top rather than repeating an
adjustment all over the number is used - and it means you can't apply the
adjustment in one place and forget it in another.

## It works on anything iterable

`enumerate` isn't a list feature. It works on strings, files, gens,
dict views and any of it else you can loop over, and it doesn't build a
list to do it - it yields pairs as the loop asks for them.

That makes `for n, line in enumerate(f)` a just right good way to number the
lines of a file too large to hold in memory. This The `range(len(...))` form
can't do at all, because there's no length to take.

## Unpacking is doing the work

`enumerate` yields tuples. Writing `for n, item in ...` is tuple unpacking, the
same feature that makes `for k, v in d.items()` work. At times you'll see
it left packed:

```python
for pair in enumerate(items):
    print(pair)      # (0, 'a')
```

which is legal and rarely what you want. The unpacked form is the point: it
gives both halves a name at the top of the loop. The body never has to say
`pair[0]`.

## When you do not need it

If you never use the index, don't ask for one. `for item in items` is the
correct loop, and `for i, item in enumerate(items)` with `i` unused is noise
that a linter will flag. The rule when you need one and not the other is
to name the unused variable `_`.
""")


add("zip_function", """
## Walking two things at once

The job `zip` does is small and comes up constantly: you've two or more
sequences whose spots match, and you want to work with matching items
together. Names and scores, keys and values, inputs and expected outputs,
columns and headers.

Without it, the loop goes through indices and reaches back into both lists,
which reintroduces just the off-by-one risk that looping over items avoids.
With it, each iteration hands you one item from each and the indices disappear.

## Stopping at the shortest

`zip` stops when its shortest input runs out. This is a genuine design choice
rather than an oversight, and it cuts both ways.

It's convenient when you on purpose pair a finite list against an infinite
gen, because you get just as many pairs as the finite side has. It's
dangerous when the two lists were supposed to be the same length and aren't,
because the extra items are dropped in silence and the program makes a
short, plausible, wrong answer.

Since Python 3.10 you can ask for the check:

```python
zip(a, b, strict=True)     # ValueError if the lengths differ
```

Use it when equal lengths are an assumption rather than a coincidence. If
you want the opposite - pad the short one instead of truncating - `itertools`
has `zip_longest`, which fills with `None` or a value you choose.

## Building a dictionary from two lists

```python
dict(zip(keys, values))
```

This is the standard way to turn parallel lists into a mapping, and it reads
better than any loop version. It appears constantly when handling CSV rows,
where the header row supplies the keys and each data row supplies the values.

## Unzipping

The same function undoes itself, which surprises people:

```python
pairs = [("ana", 91), ("bo", 78)]
names, scores = zip(*pairs)
```

The star spreads the list of pairs into separate args, and `zip` then
takes one item from each. This Recombines them by spot. The results are
tuples rather than lists. This Matters only if you intend to mutate them.

## It is lazy

Like `map` and `filter`, `zip` returns an iterator rather than a list. Printing
it shows an object, and consuming it twice gives nothing the second time. In a
`for` loop that is invisible and ideal. The moment you want to keep the result,
wrap it in `list()`.
""")


add("sorted_with_key", """
## Sorting by more than one thing

Return a tuple, and the sort checks spot by spot:

```python
sorted(people, key=lambda p: (p.surname, p.forename))
```

Surname first, forename only where surnames match. This extends to as many
levels as you need, and it's far easier to get right than sorting again and again.

Mixing directions is the awkward case, because `reverse=True` applies to the
whole sort. For numbers, negating one component works: `key=lambda p: (-p.score,
p.name)` gives highest score first, then name ascending. For strings there's no
negation, and the usual answer is two stable sorts, applied least major
first.

## Why in-place methods return None

`nums.sort()` returning `None` looks like an oversight and is a deliberate
rule that runs through the whole standard library. `list.reverse`,
`list.append`, `list.extend`, `dict.update` and `set.add` all return `None` for
the same reason: they changed the object rather than making a new one, and
returning the object would invite `x = x.sort()`. This Reads as though a new
list came back.

By returning nothing, the method makes that line obviously wrong the moment you
try to use the result. The `None` isn't a missing return value. It's the
signal that the work happened a place else.

Once the rule is familiar it turns a reading aid. A method that returns
`None` mutated a thing. A function that returns a value left its inputs
alone. `sorted`, `reversed`, `sorted`'s relatives in `itertools`, and each
string method follow the second pattern. This Is why none of them ever
surprise you by changing what you passed in.

## The same key everywhere

`key` isn't a sorting feature. `min`, `max` and `itertools.groupby` all take it
and mean the same thing by it. So `max(people, key=lambda p: p.score)` finds the
top scorer without sorting any of it - which is both faster and clearer than
sorting and taking the last element.
""")


add("range_step", """
## Counting backwards correctly

A minus step is where `range` trips people, and the stop
value is still exclusive. Counting down to and including zero means stopping at
`-1`:

```python
range(3, -1, -1)      # 3 2 1 0
range(3, 0, -1)       # 3 2 1   - zero is missed
```

The rule hasn't changed - `range` never includes its stop - but with a
descending sequence the exclusive end is below the last value you want rather
than above it, which is just the sort of thing that reads right and
behaves or else.

An empty range isn't an error. `range(0, 5, -1)` makes nothing at all,
because the start is already past the stop in the direction of travel. A loop
over it runs zero times and says nothing. A wrong sign shows up as "the loop
didn't happen" rather than as an exception.

## When you want to walk something backwards

For iterating a sequence in reverse, `reversed()` says what it means and needs
no math:

```python
for item in reversed(items):
```

`items[::-1]` also works and builds a reversed copy first, so it costs memory
proportional to the sequence. `range(len(items) - 1, -1, -1)` works too and is
the version most likely to hold an off-by-one. Prefer `reversed` unless you
in detail need the indices.

## range is not a list

`range(10_000_000)` is instant and takes a few dozen bytes, because it stores
only start, stop and step and finds each value on demand. This is why it can
be huge, and why printing one shows `range(0, 10)` rather than the numbers.

It isn't a gen, though - it can be iterated again and again, it knows its own
length, it supports indexing, and `x in range(...)` is a fast math check
rather than a scan. That combination makes it more handy than a plain gen
and cheaper than a list.

## Slicing shares the same idea

The third arg to a slice is the same step, with the same rules, which is
why `[::2]` takes each second item and `[::-1]` reverses. Learning the
action once covers both, and the exclusive-stop rule is what makes
`a[:n]` and `a[n:]` fit together with no gap and no share.
""")


add("dict_and_set_comprehensions", """
## Inverting and filtering a mapping

Two jobs come up so often that the comprehension form is worth storing as an
idiom rather than derived each time.

Inverting swaps keys and values:

```python
{v: k for k, v in original.items()}
```

Worth pausing on: this is only lossless if the values were unique. Duplicated
values collapse, and the last one processed wins, silently. If that matters,
group instead of inverting.

Filtering keeps part of a mapping:

```python
{k: v for k, v in config.items() if v is not None}
```

That is the standard way to drop unset options before merging configuration,
and it reads better than building an empty dict and assigning into it.

## Set comprehensions, and what they are for

A set comprehension is a comprehension whose result must be unique, and the two
common uses are extracting a distinct field and finding a distinct derived
value:

```python
{r["city"] for r in rows}
{len(w) for w in words}
```

Both could be written as `set([...])` around a list comprehension. The direct
form avoids building the mid list, and says up front that uniqueness is
the point rather than an afterthought.

## When a loop is still better

The same limit applies as to list comprehensions. One change, one
optional filter, one line: use the comprehension. As soon as the value needs
a few steps, a `try`, or a rule on the key and the value, the loop
version is easier to read and much easier to change later.
""")


add("conditional_comprehensions", """
## Filtering out None before working with values

The combination above isn't a contrived example. It's the common shape when
data has gaps. Guarding in the filter means the formula at the front never
sees a `None`, which lets it do math or call methods without a defensive
check:

```python
[r["score"] * 2 for r in rows if r["score"] is not None]
```

Written the other way round - a if-based formula testing for `None` on
each item - the line is longer and still makes an entry for rows that had no
score, which is often not what was wanted.

## Where to draw the line

A comprehension carrying a filter, a if-based formula and a nested loop is
a program written on one line. It will be correct and it will cost each future
reader - including you - a slow minute. The loop version is four lines that
never need decoding, and no reviewer has ever objected to it.
""")


add("type_conversion", """
## Conversion is not the same as checking

`int("42")` converts. `isinstance(x, int)` checks. Reaching for the wrong one is
common, and the gap matters because conversion can fail loudly while a
check never does.

The Python habit is to attempt the conversion inside a `try` rather than to
validate first with a regular formula or a series of `isdigit` calls. The
attempt is the authoritative test - it knows about signs, whitespace, underscores
in numeric literals and every other detail your hand-written check would miss.

```python
def as_int(text, default=None):
    try:
        return int(text)
    except (TypeError, ValueError):
        return default
```

Catching both matters: `ValueError` for text that isn't a number,
`TypeError` for `None` or a list arriving where a string was expected.

## The float trap

`int("3.9")` raises, which surprises people who expect it to truncate. The
string isn't an int literal, so the conversion refuses rather than
guessing. `int(3.9)` on an actual float does truncate, toward zero, so `int(-3.9)`
is `-3` rather than `-4`.

If you want rounding rather than truncation, `round` is the function, and it has
its own surprise: it rounds halves to the nearest even number, so `round(2.5)` is
2 and `round(3.5)` is 4. That is deliberate - it avoids the upward bias you get
from always rounding halves up - and it's worth knowing before you conclude
a thing is broken.

Converting a string that might hold a decimal is a two-step:
`int(float("3.9"))`.

## Truthiness is a conversion too

`bool(x)` follows the same rules as `if x`. This Means empty containers, zero
and `None` all convert to `False`. That makes `bool` at times handy for
norming a value, and it makes `bool("False")` a well-known trap: the string
is non-empty, so it's `True`. Parsing a boolean from text needs an clear
mapping, not a conversion.

## Implicit conversion, and where Python refuses

Python converts numeric types automatically when it can do so without losing
info: `1 + 2.0` gives `3.0`, and checking an int with a float works as
expected. It refuses to convert between strings and numbers, which is why
`"3" + 4` raises rather than guessing whether you meant `7` or `"34"`.

That refusal is a feature. Languages that do guess give a class of bug where
a number arrives as a string from a form or a file and all continues to
work until the math silently turns concatenation. In Python that fails
at once, at the line in charge.
""")


add("none_and_truthiness", """
## Absent is not the same as empty

`None` means "there's no value here". An empty string, an empty list and zero
are all values - they just happen to be falsy. Treating the two as
the same is the source of a whole family of quiet bugs.

```python
if not name:          # true for None AND for ""
if name is None:      # true only for None
```

The first is right when you mean "nothing handy to show". The second is right
when you mean "this was never set", and the difference matters the moment an
empty value is legitimate: a comment field left blank, a quantity of zero, a
list with nothing in it yet.

The clearest example is a count. `if not count:` treats zero as missing, so a
genuine result of zero takes the "no data" branch. `if count is None:` doesn't.

## Why `is` and not `==`

`None` is a singleton: there's just one of it in a running program, so
identity and equality give the same answer for it, and identity is both faster
and hopeless to override. A class can define `__eq__` to make `x == None`
return any of it it likes. Nothing can make `x is None` lie.

That is the whole reason the rule exists, and the same thinking applies
to `True` and `False`, although checking to those at all is often redundant -
`if flag:` says it better than `if flag is True:`.

## Functions that return None

A function with no `return` returns `None`, and so does one whose `return` has no
value. This is why losing to return a result makes `NoneType` errors
a place further along rather than at the function itself.

The in-place methods do it on purpose - `sort`, `reverse`, `append`, `update`
all return `None` to signal that they mutated the object rather than making a
new one. `x = x.sort()` is the classic result, and the `None` is the library
telling you it did the work already.

## Defaults that respect zero

The `or` shortcut for defaults is common and slightly wrong:

```python
timeout = given or 30          # 0 becomes 30
timeout = 30 if given is None else given
```

The first discards any falsy value, including a deliberate zero or an empty
string. The second only fills in when the value is truly absent. When the
domain includes zero, empty text or an empty list as real values - and it often
does - the second form is the one that behaves.

## Checking emptiness

For containers, the truthiness test is idiomatic and preferred:

```python
if not items:            # yes
if len(items) == 0:      # works, but noisier
```

The exception is when `items` might be `None`. `not None` is also true.
Then you need to say which case you mean.
""")


add("string_methods", """
## Cleaning input, in order

Text arriving from a person or a file often needs the same three steps, and
the order is worth doing on purpose.

Strip first, because trailing whitespace and newlines break checks in ways
that are invisible on screen. Norm case next, when the check should
skip it. Only then split or compare.

```python
line.strip().lower().split(",")
```

Chaining works because each method returns a new string. This Is the same
immutability that makes losing to assign such a common mistake elsewhere.

For case-insensitive check across languages, `casefold` is stricter than
`lower` and handles a handful of cases `lower` doesn't. For English-only text
the difference never shows up.

## Searching without exceptions

Three ways to ask whether a thing appears in a string, and they differ in what
they give back:

```python
"cat" in text            # True or False
text.find("cat")         # index, or -1
text.index("cat")        # index, or raises ValueError
```

Use `in` when you only want to know. Use `find` when you want the spot and
lack is expected. Use `index` when lack is a bug and you want it to say so.
Choosing `find` and then losing that `-1` is falsy in a different way from
`0` is a small classic: `if text.find("cat"):` is true when the match is at
spot one and false when it's at spot zero.

## Splitting text into lines and fields

`splitlines()` handles the newline variants that `split("\\n")` gets wrong on
files written on another operating system. `split` splits once and always
returns three pieces, which avoids the length check that `split` with a maxsplit
needs:

```python
key, sep, value = line.partition("=")
```

If the separator was absent, `sep` is empty and `value` is empty, and the
unpacking still works - no `IndexError`, no branch.

## Building strings in a loop

Repeated concatenation inside a loop creates a new string each time, because
strings can't be modified in place. For a handful of pieces that is irrelevant.
For thousands it's truly slow, and the fix is to collect and join once:

```python
parts = []
for row in rows:
    parts.append(format(row))
text = "\\n".join(parts)
```

This is the same reason `join` exists as a method on the separator: it's
building the whole result in one pass. This It can only do if it's given all
the pieces at once.
""")


add("input_and_output", """
## Validating in a loop

A single `int(input())` is fine in an example and unusable in a program a person
will really operate, because the first typo ends it. The shape that works asks
again:

```python
def ask_int(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print(f"'{raw}' is not a whole number - try again.")
```

Three things are worth copying from that. The prompt says what is wanted. The
error message repeats what was typed. So The person can see the typo. And the
loop only exits on success. So The caller can lean on getting a number.

## Sentinel values and ending a loop

When you don't know how many values are coming, a sentinel ends the input:

```python
while True:
    line = input("value (blank to finish): ").strip()
    if not line:
        break
    values.append(line)
```

An empty line is the usual choice because it's what pressing enter makes. If
blank is a legitimate value, pick a thing clear like `done` and say so in
the prompt.

## Reading from a pipe rather than a person

`input` reads a line from standard input, and standard input isn't always a
keyboard. If your program is run as `cat data.txt | python script.py`, the same
`input` calls read lines from the file, and an `EOFError` is raised when it runs
out - which is the same error you get if someone presses Ctrl-D.

That is worth handling in any of it that might be piped:

```python
try:
    line = input()
except EOFError:
    line = None
```

It's also why this page's first program raises in the browser: there's no
standard input attached at all.

## Printing for people versus printing for programs

Output aimed at a person wants formatting, alignment and separators.
Output aimed at another program wants to be trivially parseable - one record per
line, a steady separator, no decorative headers.

Mixing the two is what makes a script hard to use in a pipeline. If a program
might be consumed by another, keep the data on standard output and put the
progress messages, prompts and warnings on standard error:

```python
import sys
print("processing...", file=sys.stderr)
print(result)
```

Then `script.py > out.txt` captures just the results and leaves the chatter
on screen.
""")


add("slicing_step_negatives", """
## Slicing does not raise

`a[5:99]` on a three-item list returns what exists, and `a[99:]` returns an empty
list. No exception either way. That is convenient when you're taking "up to
ten" of a thing and there might be fewer.

It's also a place bugs hide. An empty slice looks like legitimate data.
A function that slices with a found index and returns nothing hasn't
always worked right - it may have found the wrong index and been
silently forgiven. When the index must be valid, index rather than slice, and
let `IndexError` tell you.

## Copies, views and strings

A slice of a list is a shallow copy: a new list holding the same objects. That is
why `b = a[:]` is a copy idiom. Why changing `b[0] = x` leaves `a` alone
while `b[0].append(x)` doesn't - the outer list is new, the items are shared.

A slice of a string is a new string. Strings are immutable and there's
nothing else it could be. That makes `s[::-1]` a genuine copy in reverse, which
matters only when the string is very large.

## Assigning into a slice

Lists let you assign to a slice. The swap need not be the same length:

```python
nums[1:3] = ["a", "b", "c"]     # two items become three
del nums[1:3]                   # or remove them entirely
```

This changes the list in place, including its length, and it's the one part of
slicing that mutates rather than copies. It's worth knowing mainly so that you
recognise it in other people's code, and because it shows why `a[:] = b`
replaces the contents of `a` while `a = b` merely rebinds the name.

## Step with a negative start and stop

Mixing a minus step with minus indices is where slices become
write-only. `a[-2::-1]` is "start at the second-to-last, walk backwards to the
beginning" - correct, and not obvious on sight. When a slice needs a comment,
`reversed()` and an clear loop often say it better.
""")


add("mutability_and_aliasing", """
## Which types are which

The gap is worth storing as a list, because it shows action
across the whole language.

Immutable: `int`, `float`, `bool`, `str`, `bytes`, `tuple`, `frozenset`, `None`.
Mutable: `list`, `dict`, `set`, `bytearray`, and nearly each class you write
yourself.

each rule about aliasing, dict keys, default args and copying falls
out of that split. Immutable objects can be shared without risk, which is why
they can be dict keys and set members and safe defaults. Mutable objects
can't.

## Equality and identity

Two separate questions, and Python has an operator for each:

```python
a == b      # do they hold the same value?
a is b      # are they the same object?
```

Two lists with the same contents are equal and aren't the same. Confusing the
two makes code that works by accident, above all with small ints and
short strings, which Python caches: `x = 256. Y = 256. X is y` is often `True`,
and the same test with `257` is often `False`. That is an setup detail
and just why `is` should be reserved for `None` and for genuine identity
questions.

## Passing to functions, stated precisely

Python is neither pass-by-value nor pass-by-ref in the C sense. What is
passed is a ref to the object, by value - the function gets its own name
pointing at the caller's object.

So the function can mutate the object and the caller sees it, and the function
can rebind its own name and the caller doesn't. Both facts come from the same
mechanism, and once you hold "names point at objects" in your head, no further
rule is needed.

## Defensive copies

When a function stores a thing it was given, it's worth thinking about who
else holds it:

```python
class Basket:
    def __init__(self, items):
        self.items = list(items)     # our own copy
```

Without the copy, the caller's list and the object's list are the same list, and
a later change on either side surprises the other. Copying at the boundary costs
one call and drops an entire category of bug where two parts of a program share
state neither of them knows about.

The same thinking applies on the way out: returning `self.items` right hands
callers a handle on your internals. Returning `list(self.items)` or a tuple keeps
the boundary intact.
""")


add("shallow_and_deep_copy", """
## Copying an object, not just a container

`copy.copy` works on your own classes too, and it copies the same way: a new
object whose fields point at the same values. If an field is a list, both
copies share it.

Classes can control this. Defining `__copy__` and `__deepcopy__` lets an object
say how it should be duplicated. This Matters when it holds a thing that
shouldn't be copied at all - an open file, a DB link, a lock. In
practice you rarely write these. But Knowing they exist shows why copying some
library objects behaves in ways a plain field copy wouldn't.

## Why deepcopy is slower than it looks

`deepcopy` walks the entire object graph, duplicates each mutable thing it
finds, and keeps a record of what it has already copied so that shared refs
stay shared and cycles don't become infinite recursion.

That bookkeeping is why it's slow on large structures, and it's also why it's
correct in cases a hand-written recursive copy often gets wrong. If you've
ever written a recursive copy helper and hit `RecursionError` on data that
referred back to itself, that is the problem `deepcopy` already solved.

## Cheaper alternatives

Often the goal isn't a copy at all. A modified version of a thing,
without disturbing the first. a few types offer that right:

```python
new_config = {**defaults, **overrides}    # merged, both untouched
new_items = [*items, extra]               # extended, original untouched
new_point = point._replace(x=5)           # namedtuple
```

Each of these makes a new outer object and leaves the inputs alone, at the
cost of a shallow copy rather than a deep one - which is just right when the
contents are immutable.

If the contents are mutable and you find yourself needing `deepcopy` often,
that is often a signal that the structure would be better as immutable data:
tuples, frozensets, or small classes that return new instances rather than
mutating themselves.

## A practical rule for configuration

Nested dicts loaded from JSON or YAML are the single most common place
this bites, because the nesting is the whole point and `.copy()` looks like it
did the job.

If a function takes a config dict and changes any of it inside it, either it
should be documented as doing so, or it should deepcopy first. Silently editing a
nested value in a structure the caller still holds is the sort of bug that gets
diagnosed as "the settings at random change". This Is a long way from where the
mutation really happened.
""")


add("dictionary_methods", """
## Views, and why they are not lists

`keys()`, `values()` and `items()` return views: live windows onto the
dict rather than snapshots of it. Add a key and each existing view
reflects it right away, because a view holds no data of its own.

That is fast and it has one consequence worth knowing. Modifying a
dict while looping over one of its views raises `RuntimeError:
dict changed size during iteration`. The fix is to iterate over a snapshot:

```python
for key in list(d):
    if should_remove(key):
        del d[key]
```

`list(d)` copies the keys first. So The loop is walking its own list and the
dict is free to change underneath.

Key and item views also behave like sets. This Is at times very handy:
`d1.keys() & d2.keys()` gives the keys both dicts share, without a loop.

## Order is guaranteed now

Since Python 3.7, dicts keep insertion order as a language ensure
rather than an setup accident. That is why `dict.fromkeys(items)` is the
standard order-preserving deduplication, and why iterating a dict makes
a stable, predictable sequence.

It doesn't make a dict a substitute for a sorted structure - the order is
insertion order, not sorted order - but it does mean you can lean on what you
put in first coming out first.

## Choosing between get, setdefault and defaultdict

Three tools that share, and the gap is about what should happen when a
key is missing.

`get` reads and never writes. Use it when a missing key has a sensible fallback
and you don't want to add any of it to the dict.

`setdefault` reads and writes: it inserts the default when the key is absent and
returns what is now there. Use it for the grouping idiom. Here You want the
list to exist so you can append to it.

`defaultdict(list)` moves that action into the dict itself, so each
missing key springs into existence on access. Use it when *each* access should
create a default. Its downside is just that: a typo'd key lookup silently
creates an empty entry instead of raising. This Can mask a bug.

## Merging

```python
merged = {**defaults, **overrides}     # 3.5+
merged = defaults | overrides          # 3.9+
defaults |= overrides                  # in place
```

Later keys win in all three. This is the clean way to layer configuration, and
it beats a loop of `if key not in d` rules because the precedence is stated
by the order of the operands rather than buried in the logic.
""")


add("nested_data_structures", """
## The shape of data that arrives

Most real data is a list of records, and most records are dicts. API
responses, parsed JSON, CSV rows read with `DictReader`, DB results - all
the same shape.

Recognising this makes the code predictable. The outer loop takes records. A key
lookup takes a field. An inner loop takes a list-valued field. Three moves cover
almost all, and they compose to any depth.

The depth itself is the thing to keep an eye on. Two levels are easy to hold in
your head. Four levels of mixed lists and dicts is where a small helper
function - `def city_of(record):` - pays for itself right away, because it gives
the path a name and one place to fix when the shape changes.

## Modifying nested structures

Reading a nested value is safe. Writing one is where aliasing matters. If you
copied the outer list shallowly and then edit a dict inside it, both copies
change, because they hold the same dicts.

That isn't a reason to deepcopy all. It's a reason to decide
on purpose: either the structure is shared and everyone knows it, or you take a
deep copy at the boundary where it enters your code.

## Flattening and grouping

The two changes that come up constantly are inverses of each other.

Flattening turns a nested structure into a flat one - all languages anyone knows,
all items across all orders - and a nested comprehension or `itertools.chain` does
it in a line.

Grouping turns a flat list into a nested one, keyed by some field.
`setdefault` or `defaultdict(list)` is the idiom, and it's worth writing out
once until it feels auto, because half of the reporting code anyone ever
writes is a grouping followed by an aggregation.

## JSON is the same shape

`json.load` makes just these structures - dicts, lists, strings,
numbers, booleans and `None` - which is why working with parsed JSON needs no new
skills beyond this page. `json.dumps(data, indent=2)` prints them back readably,
and is the fastest way to understand a thing you've just fetched.

The one skew: JSON object keys are always strings. A dict keyed by
ints lives the round trip as string keys. This Is a small surprise that
shows up when a lookup that worked before saving fails after loading.
""")


add("lambda_map_filter", """
## Why the style guide discourages naming a lambda

`square = lambda n: n * n` works and is discouraged, for a concrete reason
rather than an aesthetic one. A `def` gives the function a name in its own
metadata, so a traceback says `square` instead of `<lambda>`. When a thing
raises three frames deep, that difference is the gap between reading the
traceback and guessing.

`def` also allows a docstring, type annotations, multiple statements and a
default arg - all of which you'll eventually want, and adding any of them
means converting anyway.

The rule that follows: if it needs a name, it needs a `def`.

## Closures in a loop

A classic trap, and it looks like a lambda problem while really being a scope
one:

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])      # [2, 2, 2]
```

each lambda captured the *variable* `i`, not its value at the time, and by the
time they run the loop has finished with `i` at 2. Binding the value by name
as a default arg fixes it:

```python
funcs = [lambda i=i: i for i in range(3)]   # [0, 1, 2]
```

This is worth recognising because it appears when functions are built in a
loop - event handlers, callbacks, partial uses - and the symptom is
always the same: they all behave like the last one.

## functools.partial

When the goal is to fix some args of an existing function, `partial` says it
more right than a lambda:

```python
from functools import partial
to_int = partial(int, base=16)
```

It also makes a thing introspectable and picklable. This A lambda isn't -
relevant the moment multiprocessing is involved, because lambdas can't be sent
to worker processes.

## Reading functional code

`map` and `filter` are worth knowing well even if you write comprehensions,
because a great deal of existing Python uses them, and because they compose with
the rest of `itertools`. Being able to read `filter(None, values)` - which drops
falsy items, using `None` as "no function" - is more handy than an view about
whether you'd have written it that way.
""")


add("files_and_with", """
## Paths, and why pathlib is worth the switch

String concatenation for paths breaks across operating systems and on edge cases
like trailing slashes. `pathlib` handles both and reads better:

```python
from pathlib import Path

data = Path("content") / "articles" / "notes.txt"
text = data.read_text(encoding="utf-8")
```

`read_text` and `write_text` open, read or write, and close in one call, which
covers the common case where you want the whole file and don't need to stream
it. For any of it iterative, `data.open()` gives you the same file object `open`
would.

`Path` also carries the questions you'd or else ask the `os` module:
`.exists()`, `.suffix`, `.stem`, `.parent`, `.glob("*.txt")`.

## Encoding is not optional in practice

Text mode decodes bytes into a string using an encoding, and if you don't name
one, Python uses the platform default. That default differs between machines,
which is how a script that works on one computer makes `UnicodeDecodeError` on
another, with data that hasn't changed.

Naming it drops the whole class of problem:

```python
open(path, encoding="utf-8")
```

If you're handling files you didn't create and can't assume, `errors="replace"`
lets you read a thing rather than crashing, at the cost of substituting the
bytes it couldn't decode.

## Writing safely

Writing right over the only copy of a file has an obvious failure mode: if the
program dies halfway, the first is gone and the swap is incomplete. The
standard remedy is to write beside it and rename:

```python
tmp = path.with_suffix(".tmp")
tmp.write_text(new_content, encoding="utf-8")
tmp.replace(path)
```

`replace` is atomic on the same filesystem. So A reader sees either the old file
or the new one and never a half-written one.

## Binary mode

Adding `b` - `open(path, "rb")` - skips decoding and gives bytes. That is what
you want for images, archives, and any of it you're copying rather than reading.
The mistake in the other direction is more common: opening a text file in binary
mode and then being puzzled that checks against strings all fail, because
`b"abc"` and `"abc"` are different types that never compare equal.
""")


add("modules_and_import", """
## What a module actually is

A module is a file, and importing it runs that file top to bottom, once. each
function meaning, class meaning and top-level statement executes at that
moment, and the resulting names become fields of the module object.

That single fact shows a few things at once. It shows why top-level code
in a module runs when someone imports it. This Is why print statements left at
module level surface in surprising places. It shows why circular imports are a
problem: two modules each trying to finish running before the other can. And it
shows the caching - having run it once, Python keeps the result.

## The `__main__` guard

Because importing runs the file, a script that does work at the top level does
that work when imported too. The guard blocks it:

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

`__name__` is `"__main__"` when the file is run right and the module's name
when it's imported. So the file can be both a usable script and an importable
module, which is what makes it testable - a test can import `main` without
running it.

## Packages and relative imports

A directory with an `__init__.py` is a package, and modules inside it can import
from each other fairly:

```python
from . import helpers          # same package
from .models import Record     # a module in the same package
```

scaled imports only work inside a package and only when the package is being
imported, not when a file inside it's run right as a script. That
restriction is behind a large share of `ImportError: attempted scaled import
with no known parent package` messages, and the usual answer is to run the module
with `python -m package.module` rather than by path.

## Where Python looks

Imports resolve against `sys.path`. This Starts with the directory of the script
being run, then the standard library, then installed packages. The first match
wins, and that sorting is why a local file named `random.py` or `json.py`
shadows the standard library module of the same name and makes errors that
look hopeless.

Naming a file after a module you also import is worth avoiding for just this
reason - the failure is confusing out of all proportion to the mistake.

## Import cost

Imports are cheap after the first. But The first one runs the whole module. A
library that does substantial work at import time makes each program that
imports it slower to start. This Is why heavy setup belongs in a function the
caller chooses to call rather than at module level.
""")


add("generators_and_yield", """
## What "lazy" buys you in practice

Three things, and they're easy to state concretely.

Memory that doesn't scale with the input: a gen over a ten-million-line
file holds one line, not ten million. Work that is never done: if the consumer
stops after ten items, the gen found ten, not the whole sequence. And
the ability to represent a thing that has no end. Nothing is built up
front.

The cost is that you get one pass and no length. If you need `len()`, indexing,
or a second traversal, you need a list, and calling `list()` on the gen is
the clear way to say so.

## Reading files, the canonical example

```python
def lines_matching(path, needle):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if needle in line:
                yield line.rstrip()
```

The file object is already a gen of lines, and this wraps it in another
that filters. Nothing is read until the caller starts iterating, and only one
line is in memory at a time even so of file size.

Note the `with` inside the gen: the file stays open across yields and
closes when the gen is exhausted or garbage-collected. That is often what
you want and is worth being conscious of, because a gen abandoned halfway
holds the file open until it's collected.

## yield from

Delegating to another iterable is one line:

```python
def all_items(groups):
    for group in groups:
        yield from group
```

`yield from group` yields each item of `group` in turn. This Is both shorter
and faster than the clear inner loop, and it turns truly valuable with
recursive structures - walking a tree of nested lists is four lines with
`yield from` and a lot more without.

## Generators and pipelines

Because each stage pulls from the previous one, a chain of gens processes
one item end-to-end before starting the next. Memory stays flat no matter how
many stages there are, and no mid lists exist.

This is the shape behind most stream processing in Python: read, filter,
transform, aggregate - each a small gen, composed at the end. The
option, building a list at each stage, works fine until the data doesn't
fit, at which point the pipeline version is the only one that still runs.

## When a list is simply better

Small collections, results you need twice, any of it you want to index, and
any of it you want to print for debugging. A gen that you right away wrap
in `list()` has bought nothing, and a comprehension says what you meant more
right.
""")


add("inheritance", """
## Composition, concretely

"Prefer composition" is common advice and rarely shown. The difference is whether
the other object is *what you're* or *what you've*:

```python
class Car(Engine):            # inheritance: a Car IS an Engine - wrong
    ...

class Car:                    # composition: a Car HAS an Engine
    def __init__(self, engine):
        self.engine = engine

    def start(self):
        return self.engine.start()
```

The composed version costs one line of delegation and gains a great deal: the
engine can be swapped, tested on its own, or shared, and `Car` exposes only the
methods it chose to expose rather than all `Engine` happens to define.

The test is substitutability. If code that expects the parent can be handed the
child and keep working, inheritance is honest. If not - if the child overrides
methods to raise, or skips half of what it inherited - the tie isn't
"is a".

## Abstract base classes

When a parent exists to define an interface rather than to be instantiated,
`abc` makes that clear:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...
```

Subclasses that forget `area` fail at build with a clear message, rather
than at some later call site with `AttributeError`. That turns a runtime
surprise into an immediate, located error.

## Duck typing means you often need neither

Python doesn't need a shared base class for polymorphism. any of it with the
right method works:

```python
def describe(thing):
    return thing.speak()
```

This accepts any object with a `speak` method, related or not. A great deal of
Python code that would need an interface in another language needs nothing here,
which is worth remembering before building a hierarchy to enable a thing that
already works.

## Multiple inheritance and mixins

Multiple parents are legal, and the reasonable use is a mixin: a small class
giving one capability, with no state of its own and no expectation of being
instantiated - `JSONSerialisableMixin`, `TimestampMixin`.

Deep diamond hierarchies are the unreasonable use. When two parents both define
the same method and both call `super()`, the order of run depends on the
MRO, and thinking about it stops being possible for anyone who didn't write it.
If you need `__mro__` to work out which code runs, the design has already cost
more than it saved.
""")


# --------------------------------------------------------------------------
# Third pass. The sections above bring each topic to roughly 800 words, which
# explains the feature and stops just as the reader starts asking the second
# question. These take each page to around 2000: a worked example whose output
# is printed rather than described, the question people actually arrive with,
# and a recap that fits on one screen.
# --------------------------------------------------------------------------


extend("inheritance", """
## A hierarchy that earns itself

Two classes, where the second truly is a kind of the first and changes one
math:

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def pay(self):
        return self.salary / 12

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r})"


class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus

    def pay(self):
        return super().pay() + self.bonus / 12


staff = [Employee("ana", 60000), Manager("bo", 90000, 12000)]
for person in staff:
    print(person, round(person.pay(), 2))
```

That prints:

```
Employee('ana') 5000.0
Manager('bo') 8500.0
```

Three things in that are worth copying. `Manager.pay` calls `super().pay()`
rather than repeating `self.salary / 12`. So A change to how base pay is
found reaches both classes. `__repr__` uses `type(self).__name__` rather
than the literal string `"Employee"`. So The subclass prints its own name for
free. And the loop doesn't ask what kind of object it has &mdash; it calls
`pay()` and lets each class answer. That last one is the point of the whole
exercise. A loop full of `isinstance` checks has inheritance without the
gain.

## What super() actually does

`super()` is often given as "call the parent". This Is close enough
until it isn't. What it really means is *the next class along in the MRO of the
object's actual type* &mdash; and with one parent those are the same thing, so
the shortcut lives a long time before it breaks.

Here is where it stops being the same thing:

```python
class Base:
    def greet(self):
        return "base"

class Left(Base):
    def greet(self):
        return "left -> " + super().greet()

class Right(Base):
    def greet(self):
        return "right -> " + super().greet()

class Both(Left, Right):
    pass

print(Both().greet())
print([c.__name__ for c in Both.__mro__])
```

The output surprises most people the first time:

```
left -> right -> base
['Both', 'Left', 'Right', 'Base', 'object']
```

`Left.greet` calls `super().greet()` and gets **`Right`**, not `Base` &mdash;
though `Right` is nowhere in `Left`'s meaning. The MRO is found from
the type of the object, and `Both` puts `Right` after `Left`. This is what
makes cooperative multiple inheritance possible: each class does its bit and
delegates onward without knowing who is next.

It's also why `super().__init__(...)` matters even when the parent's
`__init__` looks empty. In a hierarchy someone else may extend later, breaking
the chain breaks classes that don't exist yet.

## Overriding without breaking the parent's promise

An override replaces a method, and any of it holding the parent type keeps
calling it expecting the parent's action. Two rules keep that honest.

**Accept at least what the parent accepted.** If `Animal.feed(self, amount)`
takes an amount, a subclass whose `feed(self)` takes none will fail when
it's used through the parent's interface.

**Return the same kind of thing.** A parent whose `area()` returns a number and
a child whose `area()` returns a string will break the first caller that does
math with it.

The override that breaks both is the one that refuses:

```python
class ReadOnlyList(list):
    def append(self, item):
        raise TypeError("read only")
```

This looks like a reasonable restriction and is a trap. All that accepts
a `list` is entitled to append to one. `ReadOnlyList` isn't a list in any
handy sense &mdash; it just passes `isinstance` checks. If you want a thing
that can't be appended to, don't inherit from a thing that can. Hold a list
and expose only the methods you intend to support.

## isinstance, and when checking the type is the wrong move

`isinstance(x, Animal)` is true for `Animal` and for each subclass, which is
what you almost always want. `type(x) is Animal` is true only for exact
matches, and using it on purpose excludes subclasses &mdash; which is rarely
what anyone means.

Both are worth reaching for less often than people do. A chain like this:

```python
if isinstance(thing, Dog):
    sound = "woof"
elif isinstance(thing, Cat):
    sound = "meow"
```

is inheritance being used for storage while the branching is still done by
hand. The version that scales is a `speak()` method on each class and
`thing.speak()` at the call site: adding a tenth animal then touches one new
class rather than each chain in the codebase.

The honest uses are narrow: validating an arg at a public boundary,
handling truly unrelated types such as "a string or a list of strings", and
writing `__eq__`, which has to decide what it can be checked against.

## Where attributes are found

Overriding is one case of a more general rule, and knowing the rule drops a
whole category of confusion. When you write `obj.thing`, Python looks in the
instance's own dict first, then the class, then each class along the MRO
in order, and raises `AttributeError` if none of them has it.

That sorting shows why assigning to an field on one instance doesn't
affect the others, and why assigning on the class affects each instance that
hasn't set its own:

```python
class Counter:
    total = 0                      # on the class, shared

    def bump(self):
        self.total += 1            # reads class, writes instance


a, b = Counter(), Counter()
a.bump()
print(a.total, b.total, Counter.total)
```

```
1 0 0
```

`self.total += 1` reads `Counter.total` (0, found on the class), adds one, and
*assigns* the result to `a`. This Creates an instance field shadowing the
class one. `b` and the class itself never change. This is the single most
common surprise with class fields, and it isn't a special rule &mdash; it
falls straight out of "reads search the chain, writes always land on the
instance".

The version that truly shares state has to say so:

```python
    def bump(self):
        Counter.total += 1         # or type(self).total
```

And the version that catches people badly is a mutable class field, because
appending to a list is a read followed by a mutation, not an set &mdash;
so each instance really does share it. If each instance needs its own, create
it in `__init__`.

## Extending a built-in, and why it disappoints

Subclassing `dict` or `list` looks like the obvious way to get a container with
one extra action, and it works less well than expected:

```python
class LoudDict(dict):
    def __setitem__(self, key, value):
        print("setting", key)
        super().__setitem__(key, value)


d = LoudDict()
d["a"] = 1              # prints
d.update({"b": 2})      # prints nothing
print(dict(d))
```

```
setting a
{'a': 1, 'b': 2}
```

`update` is built in C and doesn't route through `__setitem__`, so the
override is bypassed. The same applies to `dict(**d)`, `setdefault`, and the
equivalents on `list`. The built-ins aren't written as cooperating Python
methods, and nothing promises they'll call each other.

Two ways out. `collections.UserDict` and `UserList` are pure-Python wrappers
written so that each op does go through the methods you can override.
Or hold a plain `dict` as an field and expose only the ops you mean
to support &mdash; composition again, and often the better answer, because a
container with one unusual rule is rarely a good substitute for the real thing
all over a `dict` is accepted.

## Alternative constructors, and why they take cls

A class often needs more than one way to be built. From a string, from a
row of a file, from a dict. Adding params to `__init__` for each one
gets ugly quickly. A `classmethod` is the usual answer:

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    @classmethod
    def from_text(cls, text):
        x, y = text.split(",")
        return cls(int(x), int(y))

    def __repr__(self):
        return f"{type(self).__name__}({self.x}, {self.y})"


class Point3D(Point):
    pass


print(Point.from_text("3,4"))
print(Point3D.from_text("3,4"))
```

```
Point(3, 4)
Point3D(3, 4)
```

The key detail is `cls`, not `Point`. A classmethod receives the class it
was called on, so `Point3D.from_text` builds a `Point3D` without `Point3D`
writing a line of code. Hard-coding `return Point(...)` would have given a
`Point` from both calls, and the subclass would have silently lost its own
type &mdash; the same failure as hard-coding a name in `__repr__`, from the
same cause.

## Questions people ask

<strong>Do I have to call `super().__init__()`?</strong> Only if the parent's
`__init__` does a thing you need. But it often does, and skipping it
fails later and further away. So Call it unless you've a exact reason not
to.

<strong>Can a subclass add fields the parent knows nothing about?</strong>
Yes, and that is normal. `Manager` adding `bonus` is just the intended use.

<strong>What is the difference between overriding and overloading?</strong>
Overriding is replacing an inherited method. This Python does. Overloading is
a few versions of one function distinguished by arg types, which Python
doesn't have &mdash; default args and `*args` cover the same ground.

<strong>Should all inherit from a common base?</strong> No. That is a
habit from languages where it's needed. Unrelated classes should be
unrelated.

<strong>How deep is too deep?</strong> Three levels is often already a
warning. The cost isn't the depth itself but that finding which class defines
a given method turns a search.

<strong>Why does my subclass print the parent's name?</strong> Because
`__repr__` hard-codes a string. Use `type(self).__name__` and it follows the
actual class.

<strong>Why does `super()` need no args?</strong> Inside a class body Python
supplies the class and the instance for you. The clear
`super(Dog, self)` form is the Python 2 spelling and still works, which is why
you'll see it in older code.

<strong>Can I inherit from a class in another module?</strong> Yes, and it's
normal &mdash; but note that you're now coupled to that class's internals,
so a library's undocumented base class is a risky parent.

## Recap in one screen

- Inherit when the child truly is a kind of the parent and can be used
  anywhere the parent is expected. Or else hold the other object instead.
- `super()` means the next class in the MRO of the object's real type, not
  truly the parent &mdash; which is what makes mixins work.
- Overrides must accept what the parent accepted and return what it returned;
  an override that raises is a sign the tie is wrong.
- Prefer a method call over a chain of `isinstance` checks. That is the
  gain you inherited for.
- `type(self).__name__` in `__repr__` gives each subclass a correct one.
""")


extend("input_and_output", """
## Reading several values from one line

People type more than one thing at a time. `split()` is how you take them
apart. Using a stand-in for the typed line, as the rest of this page does:

```python
raw = "3 12 7"

a, b, c = raw.split()                      # three strings
nums = [int(x) for x in raw.split()]       # three ints
first, *rest = raw.split()                 # "3", ["12", "7"]

print(a, b, c)
print(nums, sum(nums))
print(first, rest)
```

```
3 12 7
[3, 12, 7] 22
3 ['12', '7']
```

`split()` with no arg is the one to reach for: it splits on any run of
whitespace and skips leading and trailing space. So A line typed with two
spaces between values still works. `split(" ")` is the version that doesn't
forgive that, and makes empty strings where the extra spaces were.

The trap is unpacking a line whose length you assumed:

```python
a, b, c = "3 12".split()
# ValueError: not enough values to unpack (expected 3, got 2)
```

The message is precise. This Makes this an easy one to fix &mdash; but it's
raised at the set, so a program that reads ten lines and unpacks each
will stop on the first short one. Where the input comes from a person rather
than a file you control, check the length before unpacking, or collect with a
star and validate.

## A menu loop, end to end

Most small interactive programs are the same shape: show the options, read a
choice, act on it, repeat until they quit. Written once properly it's worth
keeping:

```python
ACTIONS = {"1": "add an item", "2": "list items", "q": "quit"}

def menu(choices):
    for key, label in ACTIONS.items():
        print(f"  {key}) {label}")
    for choice in choices:                 # stands in for input()
        choice = choice.strip().lower()
        if choice == "q":
            print("bye")
            break
        if choice not in ACTIONS:
            print(f"'{choice}' is not an option")
            continue
        print("->", ACTIONS[choice])

menu(["1", "9", "2", "Q"])
```

```
  1) add an item
  2) list items
  q) quit
-> add an item
'9' is not an option
-> list items
bye
```

The details that make it usable rather than merely working: the options are
data in a dict rather than a chain of `elif`. Adding one is a single
line. The choice is stripped and lowercased before any of it looks at it, so
`" Q "` works. An unknown choice says what was typed and loops rather than
crashing. And quitting is an clear option rather than Ctrl-C.

In a real program the `for choice in choices` line turns `while True:` with
`choice = input("choose: ")`. All else stays as it's.

## Why output sometimes appears in the wrong order

Standard output is buffered when it isn't a terminal. Python collects printed
text and writes it in blocks. One system call per line is slow. On
screen this is invisible. Redirect to a file or pipe the program into another
one and it turns visible: output can appear late, and it can appear *after*
things written to standard error. This Isn't buffered the same way.

```python
import sys

print("step 1")                       # buffered
print("warning", file=sys.stderr)     # not buffered
print("step 2", flush=True)           # written immediately
```

Run that on a terminal and the order is what you wrote. Run `python3 s.py > out.txt`
and the warning appears on screen before the file has any of it in it.

`flush=True` forces a write at that point. It's worth using for progress
messages in a long-running script, and for any of it printed just before an
op that might hang &mdash; or else the message you were leaning on to
tell you where it got stuck is still sitting in the buffer.

The same applies to a crash: output already printed but not yet flushed can be
lost if the process dies badly. This Is one of the reasons `logging` is
preferred to `print` once a script grows up.

## Command-line arguments, the other input

`input()` isn't the only way a program receives values, and for any of it you
will run more than once it's the worse one. args typed alongside the
command arrive in `sys.argv`:

```python
import sys

# $ python3 report.py sales.csv 2024
print(sys.argv)          # ['report.py', 'sales.csv', '2024']
name = sys.argv[1] if len(sys.argv) > 1 else "data.csv"
```

`sys.argv[0]` is the script's own name. So The real args start at index 1,
and reading one that wasn't supplied raises `IndexError` &mdash; hence the
length check, or a default.

The difference matters more than it looks. A program driven by `input()` can't
be scripted, scheduled, or re-run with the same values without somebody typing
them again. A program driven by args can be put in a shell script and
repeated just. The rule of thumb: prompt for what a person decides in the
moment, take as an arg any of it the program needs each time it runs.

Once there's more than one or two, `argparse` in the standard library is worth
the twenty minutes &mdash; it gives `--flags`, defaults, type conversion, and a
`--help` message made from the same declaration.

## Making a prompt hard to get wrong

Most bad input is invited by the prompt. Three habits drop most of it:

```python
def ask_yes_no(answer, default=True):
    answer = answer.strip().lower()
    if not answer:
        return default
    return answer in ("y", "yes")


for typed in ["Y", "no", "", "  YES "]:
    print(repr(typed), "->", ask_yes_no(typed))
```

```
'Y' -> True
'no' -> False
'' -> True
'  YES ' -> True
```

**Say what the options are, and which one enter chooses.** A prompt reading
`Continue? [Y/n]` tells the person both, and the capital letter is the
rule for the default.

**Norm before checking.** `strip().lower()` turns four different things a
person might type into one thing your code has to handle.

**Accept the obvious variants.** Someone who types `yes` when you asked for `y`
has answered the question. Refusing them is the program being hard.

The same three apply to any prompt, not just yes/no: show the units, show the
default, and strip the input before you look at it.

## Reading a password without showing it

`input()` echoes what is typed. This Is just wrong for a password. The
standard library has the right tool:

```python
from getpass import getpass

secret = getpass("Password: ")     # typed characters are not displayed
```

It reads from the terminal right rather than from standard input, so it
can't be piped into &mdash; which is a feature. It also falls back to a plain
`input()` with a warning when there's no real terminal, so check the
environment rather than given the characters were hidden.

The rule that goes with it: don't print a secret back out, don't put one in a
default arg, and don't read one from `sys.argv`, because args are
visible to anyone who can list the running processes. For any of it automated,
an environment variable or a file with restricted permissions is the usual
answer, and `os.environ.get("API_KEY")` is how you read it.

## Confirming before something irreversible

When a program is about to delete, overwrite or send a thing, the prompt is
the last line of defence, and a `[y/N]` is a weak one &mdash; people type `y`
by reflex. For truly irreversible actions, ask for a thing that can't be
answered by reflex:

```python
def confirm(typed, expected):
    return typed.strip() == expected


target = "production"
print(confirm("production", target))
print(confirm("y", target))
```

```
True
False
```

needing the name to be typed out makes the person read what they're about to
do. Note that this check is on purpose not lowercased or fuzzy-matched:
all over else on this page the advice is to forgive input, and this is the
one place where being strict is the point.

## Questions people ask

<strong>Why does `input()` return a string when I typed a number?</strong>
Because it reads characters and has no way to know what you meant by them.
`"42"` could be a quantity, a house number or a password.

<strong>How do I read a number without crashing on bad input?</strong> Wrap
`int()` in `try`/`except ValueError` and ask again. The loop earlier on
this page is the standard shape.

<strong>What is the difference between `print(x)` and `print(str(x))`?</strong>
Nothing. `print` calls `str()` on each arg already.

<strong>Why do my strings show up with quotes?</strong> You printed a
container. `print(["a"])` shows the list's `repr`. This Quotes its items;
`print(", ".join(["a"]))` prints them as text.

<strong>How do I print without a newline?</strong> `print(x, end="")`, then a
bare `print()` when the line is finished.

<strong>Can I read all at once instead of line by line?</strong> Yes:
`sys.stdin.read()` for the whole of standard input, or `sys.stdin` iterated
like a file for one line at a time without `input`'s prompt handling.

<strong>Why does my prompt appear after the input on some terminals?</strong>
Because the prompt was printed with `print` and not flushed. `input()`'s own
prompt arg doesn't have this problem. This Is the reason to use it.

<strong>How do I clear the screen or move the cursor?</strong> With terminal
escape codes, or a library like `curses` or `rich`. There's nothing in `print`
itself for it.

<strong>Does `input()` strip the newline?</strong> Yes &mdash; it returns the
line without the trailing newline. But With any spaces the person typed, which
is why `strip()` is still worth calling.

## Recap in one screen

- `input()` always returns a string, and always without the trailing newline.
- Convert by name, and expect the conversion to fail on real input &mdash;
  `try`/`except ValueError` in a loop is the shape that lives a person.
- `split()` with no arg handles ragged whitespace. Unpacking a line
  assumes a length, so check it first.
- `sep` and `end` control what `print` puts between and after its args;
  `file=sys.stderr` separates chatter from results.
- Output is buffered when redirected. `flush=True` for progress messages you
  need to see while the program is still running.
""")


extend("string_methods", """
## replace, and the count nobody passes

`replace` swaps each hit and, like all else here, returns a new
string:

```python
text = "a-b-c-d"
print(text.replace("-", " "))
print(text.replace("-", " ", 2))
print(text)
```

```
a b c d
a b c-d
a-b-c-d
```

The third arg caps how many are replaced, counting from the left, and it
is the one people forget exists. It saves a regular formula
oddly often. The last line is the reminder that `text` itself never
changed.

`count` answers the related question without doing the work: `text.count("-")`
is 3 here, and returns 0 rather than raising when there are none.

## A worked example: cleaning one messy line

Real text arrives with the wrong spacing, the wrong case, and a newline on the
end. The methods on this page compose into a single readable pass:

```python
raw = "  Ana , 91 ,  Physics\\n"

name, score, subject = [f.strip() for f in raw.strip().split(",")]

print(repr(name), int(score), repr(subject))
```

```
'Ana' 91 'Physics'
```

Two strips are doing different jobs and both are needed. The outer
`raw.strip()` drops the leading spaces and the trailing newline from the line
as a whole. The one inside the comprehension drops the spaces around each
field, which the outer one couldn't reach. Splitting first and stripping each
piece is the general shape. Stripping only the whole line leaves `" 91 "`,
which `int()` happens to forgive and a string check doesn't.

`repr()` in the output is there on purpose. Printing a string that still has
a stray space looks the same to one that doesn't. `repr` is how you see
the difference.

## Padding and aligning without counting spaces

```python
rows = [("ana", 91), ("bo", 7), ("caroline", 143)]
for name, n in rows:
    print(name.ljust(10, ".") + str(n).rjust(4))
```

```
ana.......  91
bo........   7
caroline.. 143
```

`ljust`, `rjust` and `center` take a width and an optional fill character.
`zfill` is the special case for numbers: `"7".zfill(3)` gives `"007"`, and it
handles a leading minus sign right. This `rjust(3, "0")` doesn't.

The f-string spellings are `f"{name:<10}"`, `f"{n:>4}"` and `f"{n:^4}"`, and
they're often the better choice because the value and its formatting stay
together. The methods are worth knowing for when the width is found rather
than literal.

## The is-something tests, and the one that lies

```python
print("42".isdigit(), "4.2".isdigit(), "-4".isdigit())
print("42".isdecimal(), "\\u00b2".isdigit(), "\\u00b2".isdecimal())
```

```
True False False
True True False
```

`isdigit` isn't "would `int()` accept this". It rejects a decimal point and a
minus sign, and it accepts superscripts and other numeric characters that
`int()` refuses. `isdecimal` is the stricter one and the closer match to what
people often mean.

The solid test for "is this a number" is to try the conversion:

```python
def is_int(text):
    try:
        int(text)
    except ValueError:
        return False
    return True
```

That handles the minus sign, the nearby whitespace and the underscores
Python allows in numeric literals, all of which the `is` methods get wrong in
one direction or the other. `isalpha`, `isspace` and `isupper` have no such
problem and are safe to use right.

## Why strings are immutable at all

Beginners meet immutability as an inconvenience &mdash; the reason `name.upper()`
seems not to work. It's worth knowing what the language buys with it, because
the same property shows action in a few other places.

A string that can't change can be shared without anyone worrying about who
else holds it. Python takes edge of that constantly: the same short
strings in your source are often the same object in memory, string constants
can be stored once and pointed at from many places. Passing a string to a
function costs nothing even so of its length, because nothing is copied.

It also makes strings hashable, and so usable as dict keys and set
members. A hash is found from the contents. If the contents could change,
the key would end up filed under a hash that no longer matches it, and lookups
would silently fail. This is just why lists can't be keys and tuples can.
each dict you index by name leans on strings being immutable.

The cost is real and narrow: building a string by repeated concatenation is
quadratic, because each step copies all so far. That is the one place
where the design bites, and `join` exists to cover it. all over else, the
ensure that a string you were handed is the string you still have is worth
a lot more than the ability to edit one in place.

## Unicode, and what a character actually is

A Python string is a sequence of Unicode code points, not bytes. For English
text the gap never comes up, and outside English it comes up
right away.

`len("café")` is 4, which is what you'd hope. But the same text can be
written two ways in Unicode. As an `é` code point, or as `e` followed by
a mixing accent &mdash; and in the second form `len` reports 5 while the
text looks the same on screen. `unicodedata.norm("NFC", text)` merges
the second form into the first, and norming before checking is the fix for
"these two strings look the same and aren't equal".

Emoji push this further: many are a few code points joined together, so
slicing a string by index can cut one in half and give a thing that will
not render. If you're truncating text that might hold them, count
grapheme clusters with a library rather than characters.

Encoding is the separate question of how those code points become bytes for a
file or a network. `text.encode("utf-8")` makes `bytes`;
`data.decode("utf-8")` goes back. The errors people hit &mdash;
`UnicodeDecodeError` on reading a file, mojibake like `Ã©` where `é` should be
&mdash; are almost always a file written in one encoding and read in another.
UTF-8 is the right default all over, and giving it by name when
opening files is worth the few extra characters, because the default still
varies by platform.

## When to stop using string methods

The methods on this page handle a great deal, and there's a point past which
they stop being the right tool. The signal is a chain of `split`, `strip`,
`find` and slicing that is getting longer each time the input surprises you.

If the pattern is truly variable &mdash; optional whitespace, options,
repetition, groups you want to capture. That is what regular expressions
are for, and `re.search` with a named group will be shorter and easier to fix
than eight lines of index math. The trade is that a regular formula is
harder to read for anyone who doesn't write them often. It earns its place
only when the string methods have truly run out.

If the text is a known format, don't parse it by hand at all. JSON, CSV, INI
files, dates, URLs and email handles all have a module in the standard
library that has already handled the edge cases you haven't thought of yet:
quoted commas inside a CSV field, escaped characters in JSON, timezone
suffixes, percent-encoding. Hand-rolled parsing of a standard format is the
most solid way to give a program that works on your test file and fails
on real data.

The rule that follows is a simple one. String methods for cleaning and simple
splitting, a parser for any of it with a specification, and regular expressions
for the truly irregular middle ground.

## Questions people ask

<strong>Why does `strip()` not drop a suffix?</strong> Because its arg
is a set of characters to drop from each end, not a string to match. Use
`removesuffix` for the other job.

<strong>Is `+` on strings really slow?</strong> Not for a few pieces. It's
slow inside a loop over thousands. Each `+` builds a whole new string.
Collect into a list and `join` once.

<strong>What is the difference between `find` and `index`?</strong> `find`
returns -1 when absent, `index` raises `ValueError`. Pick based on whether
lack is expected or a bug.

<strong>How do I split on more than one separator?</strong> `re.split` from the
`re` module &mdash; `str.split` takes one separator only.

<strong>Why does `"".join(numbers)` fail?</strong> `join` needs strings.
Convert first: `"".join(str(n) for n in numbers)`.

<strong>Does `lower()` work for each language?</strong> Mostly.
`casefold()` is the more aggressive version intended for caseless check,
and it's what to use when the text isn't ensured to be English.

<strong>How do I check a string against a few endings?</strong>
`endswith` accepts a tuple: `name.endswith((".jpg", ".png"))`.

## Recap in one screen

- each string method returns a new string. If you don't assign the result,
  nothing happened.
- `join` is called on the separator and needs strings. `split()` with no
  arg is the forgiving version.
- `strip` takes characters, not a suffix &mdash; `removeprefix` and
  `removesuffix` exist for that.
- `find` returns -1, `index` raises. `in` is the one to use when you only need
  a yes or no.
- `isdigit` isn't "is a number" &mdash; try the conversion instead.
""")


extend("mutability_and_aliasing", """
## Watching it happen with id()

`id()` returns a number spotting an object for if it exists, which
turns the whole topic from an assertion into a thing you can check:

```python
a = [1, 2]
b = a
before = id(a)

a.append(3)
print("after append :", id(a) == before, b)

a = a + [4]
print("after rebind :", id(a) == before, b)
```

```
after append : True [1, 2, 3]
after rebind : False [1, 2, 3]
```

The first line mutated the object. So The id is unchanged and `b` &mdash; the
other name for that same object. Sees the new item. The second line
built a different list and pointed `a` at it. The id changed and `b` still
refers to the first. This Now has three items rather than four.

each confusing aliasing bug is one of those two lines in disguise.

## The augmented assignment asymmetry

`a += [3]` and `a = a + [3]` look like the same statement written two ways.
For lists they aren't:

```python
a = [1, 2]
b = a
a += [3]
print(a, b)

a = [1, 2]
b = a
a = a + [3]
print(a, b)
```

```
[1, 2, 3] [1, 2, 3]
[1, 2, 3] [1, 2]
```

`+=` on a list calls `__iadd__`. This Extends the existing list in place and
then rebinds the name to that same object. So every other name sees the
change. `a + [3]` builds a new list and only then rebinds, leaving `b` alone.

For numbers, strings and tuples there's no in-place option, so `+=` always
behaves like the second form. This is why `+=` feels steady right up until
the first time it's used on a list that someone else is also holding.

## A tuple is immutable, its contents are not

```python
t = ([1, 2], "fixed")

t[0].append(3)
print(t)

try:
    t[1] = "changed"
except TypeError as e:
    print("TypeError:", e)
```

```
([1, 2, 3], 'fixed')
TypeError: 'tuple' object does not support item assignment
```

The tuple ensures that its slots keep pointing at the same objects. It
promises nothing about those objects. A tuple of lists is so not a
frozen structure, and &mdash; the hands-on consequence &mdash; it can't be
used as a dict key. Hashing it has to hash its contents and lists
are unhashable.

The sharpest corner in the language sits here:

```python
t = ([1],)
try:
    t[0] += [2]
except TypeError as e:
    print("TypeError:", e)
print(t)
```

```
TypeError: 'tuple' object does not support item assignment
([1, 2],)
```

It raised **and** it worked. `t[0] += [2]` extends the list in place, and then
tries to assign the result back into the tuple slot. This Fails. The mutation
has already happened by then. Nothing about this is worth leaning on. It's
worth recognising, because the error message points at the tuple while the
damage is in the list.

## Where this actually bites

The rule is simple and the bugs aren't. In real code the two names for
one object are often far apart. Four shapes account for most of them.

**A shared default.** A function with `def add(item, target=[])` creates that
list once, when the function is defined, and each call that doesn't pass one
uses the same list. Items build up across calls that look free. The
fix is `target=None` and `if target is None: target = []` in the body.

**A configuration dict passed around.** One module reads a settings dict,
tweaks a value "just for its own use", and every other module sees the change.
This is the hardest version to find. The code that made the change and
the code that misbehaves may be in different files with nothing linking them.

**A cached object handed to callers.** A function that builds a list once and
returns the same list each time is fast and dangerous: the first caller to
mutate the result has changed what each later caller receives. Returning a
copy, or a tuple, closes it.

**A class field holding a list.** Written on the class rather than in
`__init__`, it belongs to the class. So Each instance appends to the same one.
Instances that were meant to be free quietly share state.

What the four have in common is that no one wrote `b = a`. The second name
arrived through an arg, a return value, a default or a class body. That is
why "set doesn't copy" is worth internalising rather than storing:
the aliasing is rarely visible on the line where the bug appears.

## A model that fits in your head

Two sentences cover all on this page.

**Names point at objects.** A name isn't storage. It's a label. set
moves a label. a few labels can point at one object, and the object has no
idea how many.

**Some objects can change, and some can't.** If an object can change, then
each label pointing at it sees the change, because there's only one object.
If it can't, the question never arises.

All else follows. Why does mutating a list arg affect the caller?
The param is another label on the same object. Why does `n += 1` inside a
function not affect the caller? ints can't change. So `+=` must build a
new one and move the local label to it. Why is a tuple of lists not frozen? The
tuple's labels can't be moved. The objects they point at can still change.

When a thing surprising happens, the productive question isn't "was this
passed by value or by ref" but "how many names point at this object, and
did that line move a label or change an object". `id()` answers the first half
and the code in front of you answers the second.

## Choosing immutability in your own code

Once the gap is clear, it turns a design choice rather than a fact
about builtins. Making your own objects immutable drops the entire class of
bugs above, and Python gives you a few ways to do it.

A `NamedTuple` or a dataclass declared with `@dataclass(frozen=True)` makes
a class whose fields can't be reassigned after build. Attempting it
raises rather than silently succeeding. This Turns a subtle shared-state bug
into an immediate error at the line that caused it. Both are hashable, so they
can be dict keys and set members, and both give you a readable `repr` for
free.

The pattern that follows is to build a new object rather than edit an existing
one. A method that would have changed `self.total` instead returns a new
instance with the new total, and callers rebind. This costs an allocation and
buys the ensure that nothing you handed to another part of the program can
change underneath it.

It isn't the right default for all. A large object that changes often
&mdash; a buffer being filled, a cache, any of it speed-sensitive &mdash;
is better mutable, and Python's builtins reflect that. The handy habit is to
reach for immutability for the things that travel: configuration, coords,
records read from a file, any of it passed between modules or stored in a
dict. Keep mutability local. Here You can see each name that points at
the object.

## Questions people ask

<strong>How do I copy a list properly?</strong> `list(a)`, `a[:]` or `a.copy()`
for one level. `copy.deepcopy(a)` when the items are themselves mutable and
need copying too.

<strong>Is `is` ever right for checking values?</strong> Only for `None`,
`True` and `False`. All else should use `==`.

<strong>Why did my dict change when I only edited a copy?</strong>
Because the copy was shallow and the value you edited is shared between both
dicts.

<strong>Are function args copied?</strong> No. The function gets another
name for the same object. This Is why mutating a list arg is visible to
the caller.

<strong>Why can a tuple be a dict key but not a list?</strong> Keys must
hash to a stable value, and a list's contents can change. This Would leave it
filed in the wrong place.

<strong>Does `sorted(x)` change `x`?</strong> No, it returns a new list.
`x.sort()` is the in-place one, and it returns `None` &mdash; assigning its
result is a common way to lose a list.

<strong>What about strings, do I need to copy them?</strong> Never. They can't
be changed, so sharing one is always safe.

## Recap in one screen

- A name is a label on an object. Set moves the label and never copies.
- Mutating changes the object each name can see. Rebinding changes one name.
- `+=` mutates in place for lists and rebinds for immutables &mdash; the same
  syntax, two actions.
- Immutable contents can hold mutable objects. So A tuple is only as frozen as
  what is in it.
- Copy at the boundary when you store or return a caller's container.
""")


extend("lambda_map_filter", """
## operator, the module that replaces most lambdas

A large share of the lambdas people write do one of two things: pull out an
item, or pull out an field. The standard library has both, and they're
faster and more readable than the lambda:

```python
from operator import itemgetter

people = [("ana", 91), ("bo", 78), ("cy", 91)]

print(sorted(people, key=itemgetter(1), reverse=True))
print(sorted(people, key=itemgetter(1, 0)))
```

```
[('ana', 91), ('cy', 91), ('bo', 78)]
[('bo', 78), ('ana', 91), ('cy', 91)]
```

`itemgetter(1)` is `lambda p: p[1]` with a name that says what it does, and
`itemgetter(1, 0)` returns a tuple. This Is how you sort by score and then by
name without writing the tuple out. `attrgetter` is the same for objects, and
`methodcaller("lower")` for calling a method on each item.

Note the first result: `ana` comes before `cy` though they tie, because
`sorted` is stable and `ana` was first in the input. That ensure is what
makes sorting twice for a two-level sort work at all.

## reduce, and why it is not a builtin any more

`map` and `filter` survived the move to Python 3 as builtins. `reduce` didn't,
and lives in `functools`:

```python
from functools import reduce

nums = [1, 2, 3, 4]
print(reduce(lambda a, b: a * b, nums))
print(sum(nums), max(nums), any(n > 3 for n in nums))
```

```
24
10 4 True
```

The reason for the demotion is on the second line. Nearly each real use of
`reduce` is a sum, a max, a min, an `any` or an `all`, and each of
those has a builtin that says what it means at a glance. What is left &mdash;
a running product, folding a custom combine function over a sequence &mdash; is
rare enough to be worth an import and a moment's thought from the reader.

If you do reach for it, pass the initial value: `reduce(f, items, 0)` returns
the initial value for an empty sequence instead of raising `TypeError`.

## Where map and filter lead: itertools

`map` and `filter` are the first two of a family. `itertools` holds the rest,
and they share the same property of making items on demand rather than
building lists:

```python
from itertools import islice, chain, takewhile

nums = range(1, 11)

print(list(islice(nums, 3)))
print(list(takewhile(lambda n: n < 4, nums)))
print(list(chain([1, 2], [3, 4])))
```

```
[1, 2, 3]
[1, 2, 3]
[1, 2, 3, 4]
```

`islice` takes the first few of any of it, including an infinite gen.
`takewhile` stops at the first item that fails the test, which is different
from `filter` &mdash; `filter` would carry on and return 1, 2, 3 from the whole
range while `takewhile` stops looking at 4. `chain` walks a few iterables as
one without building a mixed list.

The laziness is the point of all of them. A pipeline of `map`, `filter` and
`islice` over a large file reads only as far as it needs to.

## The three-line version of a common job

Take rows, keep the ones that qualify, transform them, and summarise. Written
with comprehensions, which is what most Python uses:

```python
rows = [("ana", 91), ("bo", 55), ("cy", 78), ("di", 43)]

passed = [name for name, score in rows if score >= 60]
best = max(rows, key=lambda r: r[1])

print(passed)
print(best)
print(f"{len(passed)}/{len(rows)} passed")
```

```
['ana', 'cy']
('ana', 91)
2/4 passed
```

One lambda appears, as a `key=` arg. This Is just the place the
earlier section said it belongs. The filtering and the transforming are done by
the comprehension rather than by `filter` and `map`, and the result reads in
the order it happens.

## What "functional" means here, and what it does not

`lambda`, `map` and `filter` arrive with a reputation attached, and it's worth
separating the handy part from the folklore.

The handy part is that functions are plain values in Python. A function can
be stored in a list, passed as an arg, returned from another function, and
kept in a dict. That is what makes `key=` args, decorators,
callbacks and dispatch tables possible, and it's the single idea behind
all on this page. A lambda isn't a special kind of function. It's the
same object a `def` makes, written inline and left unnamed.

The folklore is that using them makes code functional, and that functional code
is better. Python isn't a functional language and doesn't try to be. It has
no tail-call optimisation, its lambdas are on purpose limited to one
formula, and `reduce` was moved out of the builtins just to discourage
the style. Guido van Rossum's stated preference was that a comprehension or a
plain loop says the same thing more clearly to more readers.

What really transfers from functional programming, and is worth adopting, is
smaller and less glamorous: prefer functions that return a new value over
functions that modify their args. Avoid based on state that isn't
visible in the signature. And keep functions small enough to test on their own.
None of that needs a lambda. A page of `def` statements can follow all three,
and a chain of nested `map` and `filter` calls can violate them all while
looking the part.

## When a comprehension stops being the clearer choice

The advice throughout this page is to reach for a comprehension first, so it's
worth being precise about where that stops holding.

A comprehension is doing too much when it has more than one `for` and a
rule, when the formula at the front needs its own explanation, or when
the whole thing no longer fits on one line without awkward wrapping. At that
point it has become a loop that is harder to read than the loop would have
been, and the honest move is to write the loop. Or to name the inner
step as a function and call it from a simple comprehension.

The other case is when you need a thing a comprehension can't do: a `break`,
an early return, a `try`/`except` around one item, or any of it that has to
happen for its side effect rather than its value. A comprehension built purely
for side effects, with its result thrown away, is a loop wearing the wrong
clothes. Write `for` and let the reader see what is happening.

Nesting deserves its own warning. A comprehension inside another
comprehension's formula is read outer-first and reasoned about
inner-first, which is just the sort of thing that is fine while you're
writing it and unpleasant three months later. Two statements are almost always
better than one clever one.

## Naming things the reader will meet

Two words appear constantly in discussions of this material and are rarely
defined, which makes a lot of or else good explanations hard to follow.

A **higher-order function** is a function that takes a function as an arg
or returns one. `sorted` is higher-order because of `key=`. So are `map`,
`filter`, and each decorator you'll write. There's nothing more to the term
than that.

A **closure** is a function that remembers a value from the scope where it was
created, and keeps working after that scope has finished. The loop trap earlier
on this page is a closure behaving just as given and not as expected: the
lambdas remembered the variable rather than the value it held at the time.

## Questions people ask

<strong>Can a lambda have more than one statement?</strong> No. The body is a
single formula. If you need a statement, you need a `def`.

<strong>Can a lambda have default args?</strong> Yes &mdash;
`lambda x, n=2: x ** n`. And that is also the trick for capturing a loop
variable by value.

<strong>Why does printing `map(...)` show an object?</strong> Because it's a
lazy iterator. Wrap it in `list()` to see the items.

<strong>Is a comprehension faster than `map`?</strong> They're close.
`map(int, items)` with an existing function is often slightly faster;
`map(lambda ..., items)` is often slightly slower. Neither difference is a
reason to choose one.

<strong>What does `filter(None, items)` do?</strong> Drops each falsy item.
`None` in the function slot means "use the item's own truthiness".

<strong>Why can I not pickle a lambda?</strong> Pickling stores a ref by
name and a lambda has none. That is why `multiprocessing` rejects them, and
where `functools.partial` earns its place.

<strong>Do `map` and `filter` work on dicts?</strong> They work on
any of it iterable, and iterating a dict gives its keys. Use
`d.items()` when you want pairs.

## Recap in one screen

- A lambda is a single-formula function. Use one as a `key=` arg and
  write a `def` when it deserves a name.
- `map` and `filter` are lazy iterators. Consume them once, wrap in
  `list()` to keep them.
- Prefer a comprehension by default. `map(existing_function, items)` when it's
  just that shape.
- `operator.itemgetter` and `attrgetter` replace the most common lambdas and
  read better.
- `reduce` lives in `functools` because `sum`, `max`, `any` and `all` already
  cover almost each use of it.
""")


extend("range_step", """
## Why the stop is excluded, and why it is the right choice

"The stop is never included" is easy to store and easy to resent. It's
worth a paragraph on why the language chose it. Once the thinking is
clear the off-by-one errors mostly stop.

A half-open interval &mdash; one that includes the start and excludes the stop
&mdash; has three properties that a closed interval doesn't. The length is the
subtraction: `range(a, b)` makes just `b - a` numbers, with no correction
term to note. The empty case is expressible: `range(3, 3)` is empty, where a
closed interval would have no way to say "nothing" without a special case. And
adjacent ranges join without a gap and without an share: `range(0, 5)` and
`range(5, 10)` between them cover 0 to 9, each number just once, which is
what makes splitting work.

The same choice runs through slicing. This Is why `a[:3]` and `a[3:]`
rebuild the whole list and why `len(a[i:j])` is `j - i`. Learning it once
covers both, and the pattern is deliberate rather than accidental.

The place it still catches people is counting down. Here The exclusive end is
below the last value you want rather than above it. That isn't a different
rule, but it does read differently. This Is why it deserves its own focus.

## Chunking, the most common use of a step

The step exists for a exact job more often than for skipping numbers:
walking a sequence in fixed-size pieces.

```python
items = list("abcdefgh")
size = 3

for i in range(0, len(items), size):
    print(items[i:i + size])
```

```
['a', 'b', 'c']
['d', 'e', 'f']
['g', 'h']
```

The last chunk is short and needs no special handling, because slicing doesn't
complain when the end is past the length. That is the second time on this page
that a rule which looks like leniency turns out to drop a branch.

This shape appears when a thing has a batch limit: rows to insert per
query, items per API request, lines per page. The option is an index and a
counter, which is more code and more places to be wrong by one.

## Floats, and stepping by a fraction

`range(0, 1, 0.1)` raises `TypeError`. This Reads like a limitation and is
closer to a favour. a fractional step builds up error:

```python
x, vals = 0.0, []
while x < 1.0:
    vals.append(x)
    x += 0.1

print(len(vals), vals[-1])
```

```
11 0.9999999999999999
```

Eleven values, where the obvious reading of the loop promises ten, and the last
isn't 0.9. Adding 0.1 again and again compounds the tiny error in showing 0.1
in binary, and after ten additions the running total is a hair under 1.0 &mdash;
so the rule holds one more time than intended. The number of iterations now
depends on rounding error rather than on any of it you wrote.

The solid pattern is to count in ints and divide once at the end:

```python
print([i / 10 for i in range(0, 10, 2)])
```

```
[0.0, 0.2, 0.4, 0.6, 0.8]
```

Each value is found from an exact int rather than from the previous
value, so no error builds up and the number of items is fixed by the `range`.
For any of it more involved, `numpy.arange` and `numpy.linspace` exist, and
`linspace` is the one to prefer because you give it the count rather than the
step.

## The range(len(...)) habit, and what to write instead

A large share of the `range` calls in beginner code are `range(len(items))`,
used to get at the items:

```python
for i in range(len(items)):
    print(items[i])
```

This works and is worth unlearning. It adds an index that nothing needs,
it reads as math rather than as iteration, and it's the version that
makes `IndexError` when the bound is found slightly wrong. `for item in
items` says the same thing with less to get wrong.

The three cases that look like they need it often don't. If you want the
spot alongside the item, `enumerate(items)` gives both. If you're walking
two sequences together, `zip(a, b)` pairs them. If you're checking each item
with the next, `zip(items, items[1:])` gives back to back pairs.

What is left is truly index-based work: writing into a list at a found
spot, stepping by more than one, or walking backwards by index. Those are
real, and they're a small minority.

## Reading a range at a glance

Three questions come up constantly when reading someone else's loop, and all
three have math answers that are worth being able to do without running
any of it.

**How many numbers is that?** For a plus step, it's the distance cut
by the step, rounded up: `range(0, 10, 3)` covers a distance of 10 in steps of
3, giving 4 numbers. The rounding up is what catches people, and it's why
`range(0, 10, 3)` gives four values rather than three.

**What is the last one?** It's the largest value below the stop that you can
reach from the start by whole steps. For `range(0, 10, 3)` that is 9. When the
step cuts the distance just, as in `range(0, 10, 2)`, the last value is
the stop minus the step. 8, not 10 &mdash; because the stop itself is
never included.

**Does it give any of it at all?** Only if the start is on the correct side
of the stop for the direction of travel. Ascending needs `start < stop`,
descending needs `start > stop`. Neither raises when it's wrong. You get an
empty range, and a loop that silently does nothing.

That last one is worth dwelling on. It's the failure mode that costs
the most time. An exception tells you where to look. A loop that runs zero
times leaves no trace at all, and the symptom appears later as an empty result
or an unchanged variable. When a loop appears not to have happened, printing
`list(the_range)` is often a faster diagnosis than reading the math
again.

## Questions people ask

<strong>Why does `range(5, 0)` give nothing?</strong> Because the default
step is 1, so it's counting up from 5 towards 0 and stops right away. You
need `range(5, 0, -1)`.

<strong>Is `range` a gen?</strong> No. It's a lazy sequence: it can be
iterated many times, it has a length, and it supports indexing and slicing. A
gen has none of those.

<strong>How do I get a list from a range?</strong> `list(range(5))`. It's
worth asking whether you need one &mdash; a loop doesn't.

<strong>Why is `x in range(n)` fast?</strong> It does math rather than
scanning, so it's constant time even so of the size of the range.

<strong>Can the step be minus and the start below the stop?</strong> It can
be written, and it makes an empty range. Nothing is raised.

<strong>Does `range` work with very large numbers?</strong> Yes.
`range(10**18)` is created instantly, because nothing is stored but the three
values.

<strong>How do I include the stop?</strong> Add one to it. That is the honest
answer, and `range(1, n + 1)` is how you count from 1 to n.

<strong>Can I slice a range?</strong> Yes, and you get another range back:
`range(10)[2:5]` is `range(2, 5)`. Nothing is materialised.

<strong>Why does `range` compare equal to another range with different
args?</strong> Because ranges compare by the sequence they give, not by
their start, stop and step. `range(0) == range(2, 2)` is `True`. Both are empty.

<strong>Is there a version that includes the stop?</strong> Not in the
standard library. `numpy.linspace` is the closest, and it takes a count rather
than a step, which sidesteps the question.

<strong>What does a minus index do on a range?</strong> The same as on any
sequence: `range(10)[-1]` is 9. It's found rather than looked up, so it's
instant even on an huge range.

<strong>Should I ever store a range in a variable?</strong> Yes, when the same
sequence of numbers is used twice. Unlike a gen it can be iterated again,
so it's safe to reuse.

## Recap in one screen

- One arg is stop, two are start and stop, three add a step. The stop is
  always excluded.
- The half-open interval makes the length a subtraction, lets ranges be empty,
  and lets adjacent ranges tile without gaps.
- Counting down needs both a minus step and a stop below the start, and a
  wrong sign gives an empty range rather than an error.
- `range` refuses floats on purpose. Count in ints and divide once.
- `range(len(items))` is often `enumerate`, `zip`, or just iterating the
  items.
""")


extend("dictionary_methods", """
## Counter, and the four things it gives you

Counting is common enough that the standard library has a dict subclass
for it, and knowing four of its actions drops a lot of hand-written code:

```python
from collections import Counter

text = "the cat and the hat and the bat"
counts = Counter(text.split())

print(counts.most_common(2))
print(counts["the"], counts["dog"])
print(sum(counts.values()))
```

```
[('the', 3), ('and', 2)]
3 0
8
```

First, it counts any of it iterable in one call. So The loop disappears. Second,
`most_common(n)` sorts by count and gives the top n. This Is the question
people really want answered and is or else a `sorted` with a `key`. Third,
a missing key returns 0 rather than raising &mdash; and, unlike `defaultdict`,
it doesn't insert the key on access. So Reading doesn't quietly grow the
dict. Fourth, counters support math: `a + b` merges counts and
`a - b` subtracts them. This Is a neat way to diff two collections.

It's still a dict, so all else on this page applies to it.

## What can be a key, and why

Any object can be a key if it's hashable. This means immutable
all the way down. Strings, numbers, booleans and tuples of those are fine.
Lists, dicts and sets aren't, and a tuple holding a list isn't
either, because hashing it has to hash its contents.

The reason is how a dict works. It finds a hash of the key, uses that
to decide where to store the entry. Looks in the same place later. If a key
could change after insertion, its hash would change, and the entry would be
sitting a place the lookup will never search. Rather than allow that, Python
refuses to hash mutable types at all.

Two consequences are worth knowing. `1`, `1.0` and `True` all hash the same and
compare equal, so they're the *same key*. `{1: "a", True: "b"}` has one
entry. And a tuple key is the standard way to index by more than one thing:
`grid[(row, col)]` is a just right plain dict lookup, and the brackets
around the tuple are optional.

Custom classes are hashable by default, using identity, which means two
distinct instances with the same contents are different keys. If you want them
to be the same key, define `__eq__` and `__hash__` together &mdash; or use a
frozen dataclass, which writes both for you.

## A dictionary instead of a chain of elif

Once functions can be values, a dict replaces a whole shape of code:

```python
def add(a, b): return a + b
def sub(a, b): return a - b

OPS = {"+": add, "-": sub}

print(OPS["+"](3, 4))
print(OPS.get("*", lambda a, b: None)(3, 4))
```

```
7
None
```

Checked with an `if`/`elif` chain, this separates the table of options from the
code that uses it. Adding an op is one dict entry rather than
another branch, the set of valid options can be listed with `OPS.keys()`, and
the same table can drive a help message or validate input.

The pattern generalises well beyond math: handlers keyed by message type,
formatters keyed by file extension, validators keyed by field name. It's the
same idea as the menu earlier in the track, and it's worth reaching for
when a chain of `elif` is checking one value against a list of constants.

Where an `if` chain is still better: when the rules aren't simple equality
&mdash; ranges, combinations, any of it needing `and` &mdash; a dict can't
express the question, and forcing it to is worse than the chain.

## Getting the items out in a useful order

A dict keeps insertion order. This Is rarely the order you want to
report in. `sorted` takes the same `key` arg here as all over else, and
`d.items()` gives it pairs to work with.

Sorting by key is `sorted(d.items())`. This Works because tuples compare
element by element and the key is first. Sorting by value needs a key function
that reaches for the second element &mdash; `key=lambda kv: kv[1]`, or
`key=itemgetter(1)` &mdash; and adding `reverse=True` gives you largest first.
For a top-n rather than a full sort, `heapq.nlargest(3, d.items(), key=...)`
does less work, and `Counter.most_common(3)` does it for you when the values
are counts.

The result is a list of tuples, not a dict. If you need a dict back
in that order, wrap it: `dict(sorted(d.items()))` builds a new one, and since
3.7 the insertion order it gets is the sorted order you just made. This is
the standard way to give a "sorted dict" in Python, and it's worth
knowing that it's a snapshot. Later insertions go on the end, not into
their sorted spot.

One detail that bites when sorting by value: ties come out in what order
they were already in, because `sorted` is stable. That is often what you
want, and when it isn't, the fix is a tuple key that names the tiebreak
by name, such as `key=lambda kv: (-kv[1], kv[0])` for "highest count first,
then alphabetical".

## Comprehensions over dictionaries

The methods on this page and dict comprehensions cover the same ground
from two directions, and knowing which reads better saves a lot of loops.

A comprehension is the right tool when you're building a new dict from
an old one: filtering out entries below a threshold, transforming each value,
swapping keys and values, or building a lookup table from a list of records.
`{k: v for k, v in d.items() if v > 0}` is one line, and the option is
three lines with an accumulator.

The methods are the right tool when you're updating a dict in place, or
when the op has a name &mdash; `update`, `setdefault`, `pop`. Rebuilding
a whole dict with a comprehension to change one entry is
wasteful and reads as though a thing more complicated is happening.

The case where people reach for the wrong one is counting and grouping. A
comprehension can't build up, because each iteration makes an free
entry with no access to what came before. That is just why `Counter`,
`setdefault` and `defaultdict` exist, and why a grouping loop stays a loop.

## Questions people ask

<strong>Is `d.get(k)` the same as `d[k]` with a `try`?</strong> In effect yes,
and `get` is clearer. Use brackets when a missing key means a bug.

<strong>Why did my loop raise "dict changed size during iteration"?</strong>
Because you added or removed a key while iterating a live view. Iterate
`list(d)` instead.

<strong>What is the difference between `update` and `|`?</strong> `update`
modifies in place and returns `None`. `|` returns a new dict and leaves
both operands alone.

<strong>Are dicts sorted?</strong> No. They keep insertion order, which
isn't the same thing. `sorted(d.items())` when you want sorted.

<strong>How do I invert a dict?</strong>
`{v: k for k, v in d.items()}`, remembering that duplicate values collapse
&mdash; the last one wins.

<strong>Is `defaultdict` always better than `setdefault`?</strong> No.
`defaultdict` creates an entry on any missing lookup, including a typo, which
can hide bugs. Use it when each access should create a default.

<strong>How do I get the first key?</strong> `next(iter(d))`. There's no
indexing, because a dict isn't a sequence.

<strong>Can I use `+` to merge two dicts?</strong> No. Use `|` on 3.9 and
later, `{**a, **b}` before that, or `update` for in-place.

<strong>Does `pop` work without a key?</strong> `popitem()` drops and returns
the last inserted pair. This Is handy for draining a dict in a loop.

<strong>How do I count without importing Counter?</strong>
`d[k] = d.get(k, 0) + 1` in a loop. `Counter` is faster and clearer, but the
one-liner is worth knowing for when the import isn't worth it.

<strong>What happens if I use an unhashable key by mistake?</strong> You get
`TypeError: unhashable type: 'list'` at the moment of insertion, which names
the type and is one of the clearer error messages in the language.

<strong>Is there a frozen dict?</strong> Not in the standard library.
`types.MappingProxyType(d)` gives a read-only view of one. This Covers most of
the reasons people want it.

## Recap in one screen

- `get` reads with a fallback, `setdefault` reads and inserts, `defaultdict`
  inserts on each miss &mdash; pick by what should happen to the dict.
- `items()` is the loop you often want. `keys()`, `values()` and `items()`
  are live views, not snapshots.
- Iterate `list(d)` when the loop body might change the dict.
- Keys must be hashable. This Means immutable all the way down. Tuples are
  the standard multi-part key.
- A dict of functions replaces a chain of `elif` that is testing one
  value against constants.
""")


extend("loop_else", """
## The same else, on try

`else` appears in a third place in Python, and seeing it there's what makes the
loop version stop feeling any:

```python
try:
    value = int(text)
except ValueError:
    print("not a number")
else:
    print("parsed", value)
finally:
    print("done")
```

The `else` on a `try` runs when no exception was raised. The `else` on a loop
runs when no `break` happened. In both cases the block means *the thing we were
guarding against didn't occur* &mdash; the exception didn't fire, the search
didn't find an early exit.

Read that way, the loop version is steady with the rest of the language
rather than an oddity bolted on. It's still a badly chosen keyword, because
"else" in an `if` means "the rule was false" and in these two places it
means "the interruption didn't happen". But there's one idea behind both, and
knowing it's easier than storing two unrelated rules.

The `try` version has a second, hands-on reason to exist: it keeps the `try`
block down to the line that can really raise. Code that should only run on
success goes in the `else`. Here It isn't accidentally protected by the
`except`, so an unrelated `ValueError` from the success path isn't silently
caught by a handler meant for the parse.

## A worked example: searching nested data

The shape `for/else` fits is a search that has to report failure, and nesting
is where the flag-based option starts to hurt:

```python
grid = [[1, 2], [3, 4], [5, 6]]

for row in grid:
    if 4 in row:
        print("found in", row)
        break
else:
    print("not found")
```

```
found in [3, 4]
```

Change the target to 9 and the `else` prints "not found". No flag, no variable
that has to be was reset before the loop and checked after it, and the
failure branch sits visually attached to the loop it belongs to.

The equal with a flag is four lines longer and has three places to make a
mistake: losing to reset, losing to set it, and checking it with
the wrong sense. None of those are hard mistakes to avoid, and all of them are
mistakes that get made.

## Where it sits among break and continue

The three of them show what happens to a loop. It helps to hold them
together.

`break` leaves the loop right away, skipping the `else`. It's the only thing
that skips the `else`, which is the entire rule.

`continue` skips the rest of the current iteration and goes on to the next one.
It doesn't affect the `else` at all. A loop that `continue`s each
single time still finishes most times, and the `else` still runs.

`return` inside a loop leaves the function altogether. So The `else` never runs
and neither does any of it after the loop. This is why a search written inside a
function often doesn't need `for/else`: returning early makes the failure
case the last line of the function. This Most readers find easier than an
attached block.

The one that surprises people is the empty sequence. A loop over an empty list
runs zero times, never breaks, and so *does* run its `else`. If you read
`else` as "if the loop didn't run", this is just backwards, and it's the
case worth testing yourself on.

## Reading it in real code

The reason to learn a make you may choose not to write is that you'll
meet it. `for/else` appears in the standard library and in long-lived
codebases, often in just the search-and-report-failure shape given
here, and at times in parsing code where a few loops each have their own
failure branch.

When you meet one, the solid move is to find the `break`. If there's one,
the `else` is the no-break branch and the loop is a search. If there's no
`break` anywhere in the body, the `else` is decoration and means nothing at all
&mdash; and that is worth noticing, because it's often a sign that somebody
wrote it expecting a different action.

## Why it is still in the language

Features this misunderstood often get removed, and this one hasn't been,
which is worth a moment.

It can't be removed without breaking working code, and the amount of Python in
existence that uses it's small but real. More to the point, the action is
not wrong &mdash; it does a thing handy, has no edge cases, and the only
complaint anyone makes is about the keyword. Changing the keyword would break
just as much code as dropping the feature, and adding `nobreak` as a synonym
would mean two ways to write one thing. This The language actively avoids.

So it stays, mildly awkward and at times handy, and the hands-on spot
for anyone learning Python is the one this page has taken throughout: learn to
read it fluently, and make your own choice about writing it. Neither choice is
wrong. What is wrong is meeting one in unseen code and guessing.

## Testing a loop that has one

If you do write `for/else`, it has two paths and both deserve a test, which is
easy to forget because the failure path has no code of its own to point at.

The three cases that matter are: the item is found. So The `break` fires and
the `else` is skipped. The item is absent from a non-empty sequence, so the
loop finishes and the `else` runs. And the sequence is empty, which also runs
the `else`. That third case is the one most likely to be missing from a test
suite and most likely to be wrong in the code. It's the case where the
plain-English reading of "else" and the actual action disagree.

If the empty case should behave differently from the not-found case &mdash; and
at times it should, because "you gave me nothing to search" isn't the same
answer as "I searched and it isn't there" &mdash; then `for/else` can't
express that on its own, and an clear check before the loop is the honest
way to say it.

## Questions people ask

<strong>Does the `else` run if the loop body never executes?</strong> Yes. Zero
iterations means no `break`, so the `else` runs. This is the case most people
guess wrong.

<strong>Does `continue` skip the `else`?</strong> No. Only `break` does.

<strong>Does `return` inside the loop run the `else`?</strong> No &mdash; the
function has already left.

<strong>Does an exception skip the `else`?</strong> Yes, unless it's caught
inside the loop. The exception passes and nothing after the loop runs.

<strong>Can I use `else` on a comprehension?</strong> No. The `else` you can
write inside a comprehension is part of a if-based formula, which is an
unrelated feature.

<strong>Is there an `else` for `while`?</strong> Yes, with the same rule: it
runs when the rule became false, and not when a `break` ended the loop.

<strong>Should I use it in code others will read?</strong> In a short function
where the loop is a search, yes. Buried in a long function, a comment or an
early `return` may serve the next reader better.

<strong>Do other languages have this?</strong> Very few. It comes from a
long-standing idea in structured programming, and Python is the mainstream
language most associated with it. This Is part of why it's unseen.

<strong>Does a linter complain about it?</strong> Some flag a loop `else` with
no `break` in the body. This Is just the case where it means nothing. That
is a handy warning to have switched on.

<strong>Can I use `break` inside a nested loop and reach the outer
`else`?</strong> No. `break` leaves only the loop it's in, so it skips that
loop's `else` and leaves the outer one to finish most times.

## Recap in one screen

- The `else` on a loop runs when the loop finished without a `break` &mdash;
  read it as `nobreak`.
- Zero iterations still counts as finishing. So The `else` runs for an empty
  sequence.
- `continue` doesn't affect it. `break` and `return` are what skip it.
- It replaces the found-flag pattern in searches, dropping a variable and two
  chances to be wrong.
- The same `else` is on `try`, meaning the same thing: the interruption did
  not happen.
""")


extend("files_and_with", """
## A worked example, start to finish

Writing a file, reading it back and summarising it, using the tools from this
page rather than the ones from the `os` module:

```python
from pathlib import Path

path = Path("scores.txt")
path.write_text("ana 91\\nbo 78\\ncy 91\\n", encoding="utf-8")

total = count = 0
for line in path.read_text(encoding="utf-8").splitlines():
    name, score = line.split()
    total += int(score)
    count += 1

print(count, "rows, mean", round(total / count, 1))
```

```
3 rows, mean 86.7
```

`splitlines()` rather than `split("\\n")` because it handles the line endings of
files written on other systems, and because it doesn't leave an empty string
at the end from the final newline. `encoding="utf-8"` appears on both calls,
because the default is the platform's and the platform's isn't yours.

For a file of this size, reading it whole is fine. The version that scales is
the loop over the open file. This Holds one line at a time:

```python
with path.open(encoding="utf-8") as f:
    for line in f:
        name, score = line.split()
```

Both are correct. The difference only matters when the file stops fitting in
memory, which is the point at which it matters a great deal.

## What `with` actually is

`with` isn't special syntax for files. It works with any object building
two methods, and knowing that turns it from a rule into a tool.

An object is a **context manager** if it has `__enter__`, called on the way in,
and `__exit__`, called on the way out. `open` returns one. So Does a lock, a
DB link, a temporary directory, and any of it from `contextlib`.
`__exit__` runs whether the block finished most times, returned, or raised, which
is the ensure the whole make exists to provide.

The `as` name receives what `__enter__` returns. For a file, the
file object itself. That is why `with open(...) as f` gives you `f` and why the
name is optional when the object is only needed for its side effect.

Writing one is a decorator and a `yield`:

```python
from contextlib import contextmanager

@contextmanager
def timer(label):
    import time
    start = time.perf_counter()
    yield
    print(label, round(time.perf_counter() - start, 3))
```

All before the `yield` is setup, all after is cleanup, and the
`yield` is where the body of the `with` runs. This is the same gen
machinery from elsewhere in the track, used for a fully different purpose.

a few managers can share one statement:
`with open(a) as f, open(b, "w") as g:` opens both and closes both, in reverse
order, even if the second `open` raises.

## Do not parse standard formats by hand

The single most common mistake with files is treating a structured format as
plain text. CSV is the usual victim, because it looks like `split(",")` will
work, and it does until a field holds a comma inside quotes &mdash; at which
point the parse silently makes the wrong number of columns.

The standard library has a module for each of the formats you're likely to
meet. `csv` handles quoting, embedded newlines and different delimiters, and
`csv.DictReader` gives you dicts keyed by the header row. `json` handles
escaping, Unicode and nesting, and round-trips to Python types.
`configparser` reads INI files. `sqlite3` is there when a file of records has
started to want queries.

Each of them costs one import and drops an entire category of bug you'd
or else discover on somebody else's data. The rule is worth stating plainly:
if the format has a name, a thing in the standard library already reads it.

## Where file code goes wrong in practice

Four failures account for most of it, and none of them are exotic.

**The path is scaled to the wrong place.** A scaled path is resolved
against the process's working directory, not the script's location, so the same
program works when run from its own folder and fails from anywhere else. If a
file lives beside the script, `Path(__file__).parent / "data.txt"` says so.

**The file is open longer than intended.** A file opened without `with` and
never closed keeps a handle and, on writes, keeps data in a buffer that hasn't
reached the disk. On a short script the interpreter cleans up on exit and the
bug is invisible. In a long-running program it builds up until the process
hits the operating system's limit.

**The encoding was assumed.** This is the failure that travels: it works on the
machine that wrote the file and raises `UnicodeDecodeError` on a colleague's.
Name the encoding on each text-mode open.

**The write wasn't atomic.** A program that dies mid-write leaves a truncated
file where the good one used to be. The write-then-rename pattern earlier on
this page costs two lines and drops the possibility.

## Line endings, and the translation you did not ask for

Text mode does more than decode bytes into characters: it also translates line
endings, and knowing that shows a family of confusing results.

Windows ends lines with carriage-return plus newline. All else uses a
newline alone. Python's text mode hides the difference. On reading, any of the
variants turns a plain newline in your string. This Is why a loop over lines
behaves the same way on each platform. On writing, a newline is translated back
into what the platform uses.

That is almost always what you want, and it has two consequences worth
knowing. First, the string you read isn't byte-for-byte what is in the file,
so a length found from the text can differ from the file size. Second, if
you open a file in binary mode you get no translation at all, and lines end
with what the file really holds. Which is why text read as
binary often shows a trailing carriage return that seems to have come from
nowhere.

The one place it actively causes trouble is the `csv` module, which does its
own line-ending handling. Opening a CSV without `newline=""` lets both layers
translate, and the result is a blank line between each row on Windows. The
documented fix is just that arg, and it's worth passing habitually
rather than discovering the need for it later.

`newline=""` is also what you want when reading a file whose exact line endings
matter &mdash; a diff tool, a formatter, any of it that must write back what it
read without silently changing it.

## Questions people ask

<strong>Do I still need `f.close()` if I use `with`?</strong> No. That is the
entire point of `with`.

<strong>What is the difference between `"w"` and `"a"`?</strong> `"w"` empties
the file the moment it opens. `"a"` keeps what is there and writes at the end.

<strong>How do I check whether a file exists?</strong> `Path(p).exists()`
&mdash; but for opening, prefer to just open it and handle
`FileNotFoundError`, because the file can vanish between the check and the
open.

<strong>Why does my file have blank lines between rows?</strong> On Windows,
opening a CSV without `newline=""` makes doubled line endings. Pass
`newline=""` to `open` when using the `csv` module.

<strong>Can I read a file backwards?</strong> Not right. Read the lines and
reverse them, or seek from the end if the file is too big for that.

<strong>What does `errors="replace"` do?</strong> Substitutes a placeholder for
bytes that can't be decoded. So You get a thing rather than an exception.
handy for salvage, not for data you care about.

<strong>Is `pathlib` slower than string paths?</strong> Marginally, and never
enough to matter next to the file system call that follows.

<strong>Can I open the same file twice?</strong> Yes, and on most systems you
can even open it for reading and writing at once. Whether that is a good idea
is a different question.

<strong>What does `f.seek(0)` do?</strong> Moves the spot back to the
start, which is how you read a file a second time without reopening it.

<strong>Why is my file empty until the program ends?</strong> Because the data
is still in a buffer. Closing the file. Which `with` does &mdash; or
calling `f.flush()` writes it out.

<strong>Should I use `os.path` or `pathlib`?</strong> `pathlib` for new code.
`os.path` isn't deprecated and you'll keep meeting it, so both are worth
reading fluently.

<strong>How do I append to a file that might not exist?</strong> Mode `"a"`
creates it if it's missing, so no check is needed.

## Recap in one screen

- `with` closes the file whether the block ends most times or raises. It's the
  correct way to open one, not a style choice.
- Iterating the file object reads one line at a time and works on files larger
  than memory.
- `"w"` truncates on open. `"a"` appends. `"x"` refuses to overwrite.
- Name `encoding="utf-8"` on each text-mode open, because the default varies
  by machine.
- If the format has a name. CSV, JSON, INI. Use the module rather
  than splitting strings.
""")


extend("sorted_with_key", """
## A worked example: ranking records

The shape that comes up constantly. Sort records by one field, break
ties with another, and print them aligned:

```python
rows = [
    {"name": "ana", "score": 91, "team": "red"},
    {"name": "bo", "score": 78, "team": "blue"},
    {"name": "cy", "score": 91, "team": "blue"},
]

for r in sorted(rows, key=lambda r: (-r["score"], r["name"])):
    print(f"{r['name']:<5}{r['score']:>4}  {r['team']}")
```

```
ana    91  red
cy     91  blue
bo     78  blue
```

The key returns a tuple. So The sort checks scores first and names only where
scores tie. The minus sign reverses the score alone, which `reverse=True` could
not do &mdash; it would have reversed the names as well, putting `cy` before
`ana`.

This is worth having in your fingers, because "highest first, then
alphabetical" is what almost each leaderboard, report and ranking really
wants, and it's one formula rather than a check function.

## Sorting things that cannot be compared

Python refuses to guess an order between unrelated types:

```python
try:
    sorted([3, "1", 2])
except TypeError as e:
    print("TypeError:", e)
```

```
TypeError: '<' not supported between instances of 'str' and 'int'
```

This is deliberate. Languages that allow it give orderings that depend on
setup details, and the resulting bugs are far worse than an exception.
The fix is to say what you mean with a key: `key=str` to sort them as text,
`key=int` if they're all numeric in disguise.

`None` is the version of this that shows up in real data, because a missing
field is very often `None` and `None` can't be checked with any of it. Rather
than filtering the rows out, put the missing ones at one end:

```python
rows = [("ana", 91), ("bo", None), ("cy", 78)]
print(sorted(rows, key=lambda r: (r[1] is None, r[1])))
```

```
[('cy', 78), ('ana', 91), ('bo', None)]
```

The first element of the key is a boolean, and `False` sorts before `True`, so
all with a value comes first and the missing ones collect at the end.
Swap it to `r[1] isn't None` to put them first instead. The second element is
only ever checked between rows that agree on the first, so `None` is never
checked with a number.

## Case, accents and numbers inside strings

Sorting text has three traps that only appear once the data stops being tidy.

**Case.** The default sort is by code point. So Each capital letter sorts
before each lowercase one and `["banana", "Apple"]` comes back with `Apple`
first. `key=str.lower` fixes it, and `key=str.casefold` is the stricter version
for text that isn't ensured to be English.

**Accents.** `é` sorts after `z` by code point. This Is wrong in each
language that uses it. The standard library's `locale.strxfrm` sorts per
to the user's locale, and for any of it serious the `PyICU` library does it
properly. For an inner report, `unicodedata.norm` plus stripping the
mixing marks is often enough.

**Numbers inside names.** `["file10", "file2"]` sorts with `file10` first,
because `1` is before `2` as text. This is the "natural sort" problem, and the
fix is a key that splits the string into text and numeric runs and converts the
numeric ones, so the check happens between ints rather than digits.

All three have the same shape as all else on this page: the data isn't
what you want to compare. So Transform it in the key and leave it alone in the
result.

## What sorting costs, and when not to

Python's sort is Timsort. This Is O(n log n) and a lot
faster than that on data with existing order &mdash; already-sorted input is
close to linear, and so is data made of sorted runs. That isn't an accident;
it was designed for real data. This Is often partly sorted.

The hands-on consequence is that sorting is cheap enough to stop thinking
about at plain sizes. Where it's worth thinking about is when you don't
really need a sorted sequence:

If you want the single largest or smallest item, `max` and `min` take the same
`key` and do it in one pass rather than n log n. If you want the top few,
`heapq.nlargest(k, items, key=...)` beats sorting when k is small scaled to
n. If you want to know whether any of it qualifies, `any` with a gen stops
at the first hit. And if you're sorting the same list again and again inside a
loop, sort it once outside the loop instead.

The one that catches people is sorting to find a max. `sorted(items)[-1]`
is correct, does far more work than needed, and reads less clearly than
`max(items)`.

## Grouping, which needs sorting first

`itertools.groupby` merges runs of equal items into groups, and it's the
most common reason to sort a thing you didn't or else need in order.

The key property is that it only groups *adjacent* items. It walks the
sequence once and starts a new group when the key changes, which means
unsorted input makes a group each time the value changes back and forth
rather than one group per distinct value. Sorting by the same key first is what
makes the grouping complete, and losing to is the single mistake everyone
makes with it once.

```python
from itertools import groupby

rows = [("red", "ana"), ("blue", "bo"), ("red", "cy")]
rows.sort(key=lambda r: r[0])

for team, members in groupby(rows, key=lambda r: r[0]):
    print(team, [m for _, m in members])
```

```
blue ['bo']
red ['ana', 'cy']
```

The same `key` appears twice, in the sort and in the group, and it has to be
the same key for the result to make sense. The second thing to know is that
the groups are iterators over the first sequence, not lists, and they become
invalid once you move to the next group. Which is why the example
materialises each one inside the loop rather than collecting the groups and
using them afterwards.

For grouping without sorting, a `defaultdict(list)` and a single loop is
simpler, doesn't need order, and gives you real lists. `groupby` earns its
place when the data is already sorted, when the sequence is too large to hold,
or when you want the runs rather than the totals.

## Making your own objects sortable

`key=` handles most cases, and at times the sorting belongs to the object
itself rather than to one call site. Then the object should carry it.

Defining `__lt__` is enough for `sorted`, `min` and `max`, because they need
only "is this one less than that one". The other checks &mdash; `<=`, `>`,
`>=` &mdash; are separate methods and aren't inferred. So An object with only
`__lt__` sorts right and raises on `>=`. `functools.total_ordering` fills
the rest in from `__lt__` and `__eq__`, at a small runtime cost.

The shorter route is a dataclass. `@dataclass(order=True)` writes all six
check methods, checking the fields in the order they're declared, which
is just the tuple-key action with the tuple written for you. Fields you
don't want in the check are excluded with
`field(compare=False)`, which is how you keep a name or an id out of the
sorting while leaving it on the object.

The judgement is about where the sorting belongs. If there's one natural
order for the type &mdash; a version number, a date range, a playing card
&mdash; put it on the class and each call site gains. If different callers
want different orders, `key=` at each call site is the honest answer, and
building one in as "the" order will mislead the next reader.

One rule applies whichever you choose: the sorting must be steady with
equality, and it must be total. Objects that compare equal must not also
compare less-than, and each pair must be close. A sort that receives an
inconsistent sorting doesn't raise. It makes a result that is quietly
wrong and changes with the input order.

## Questions people ask

<strong>Can `key` return any of it?</strong> any of it close with itself.
Numbers, strings and tuples of those are the usual choices.

<strong>How do I sort descending by one field and ascending by another?</strong>
Negate the descending one in a tuple key, or do two stable sorts, least
major first.

<strong>Does `sorted` work on a dict?</strong> Yes, and it sorts the keys.
Use `d.items()` when you want pairs.

<strong>Is `reverse=True` the same as reversing afterwards?</strong> Not
just. `reverse=True` keeps ties in their first order. Sorting then
reversing flips the ties too.

<strong>What happened to `cmp`?</strong> Removed in Python 3. If you truly
need a check function, `functools.cmp_to_key` converts one into a key.

<strong>Can I sort a gen?</strong> Yes &mdash; `sorted` accepts any
iterable and returns a list. It has to consume the whole thing to do it.

<strong>Why is my sort not stable?</strong> It's. If tied items appear to
move, the key is distinguishing them in a way you didn't intend.

<strong>Does sorting a list of dicts need a key?</strong> Yes.
Dicts aren't orderable, so without one you get a `TypeError`.

<strong>How large can a list be before sorting is slow?</strong> Far larger
than most programs handle. Sorting a million small items takes well under a
second, and the cost is often dominated by what built the list.

## Recap in one screen

- `key` transforms each item once and sorts on the result. The items you get
  back are unchanged.
- A tuple key gives tiebreaks. Negate a number to reverse one field without
  reversing the rest.
- `sorted` returns a new list, `.sort()` returns `None` &mdash; that `None` is
  the rule for each in-place method.
- The sort is stable. This Is what makes two-pass sorting work.
- `max`, `min`, `heapq.nlargest` and `groupby` take the same `key`. Reach for
  them when you don't need all in order.
""")


extend("generators_and_yield", """
## Watching a pipeline run

The claim that a gen pipeline handles one item at a time end to end is
easier to believe when you can see the order:

```python
def numbers():
    for n in [1, 2, 3]:
        print("  produced", n)
        yield n

def doubled(source):
    for n in source:
        print("    doubled", n * 2)
        yield n * 2

for value in doubled(numbers()):
    print("got", value)
```

```
  produced 1
    doubled 2
got 2
  produced 2
    doubled 4
got 4
  produced 3
    doubled 6
got 6
```

Nothing is batched. `numbers` makes one value, `doubled` transforms that one
value, the loop receives it, and only then does any of it ask for the second.
The list-building equal would have printed all three "made" lines
first, then all three "doubled" lines.

This is the whole arg for gens in six lines of output. Memory stays
flat because only one item is in flight, and if the loop stopped after the
first value, `numbers` would never give the third.

## A generator is an iterator, and what that means

`for` isn't special syntax for lists. It calls `iter()` on what it's
given to get an iterator, then calls `next()` on that again and again until
`StopIteration` is raised, and that exception is what ends the loop.

A gen function returns an object building just that protocol, which
is why it works all over a list does. In a `for`, in `sum`, in
`list()`, in unpacking. It's also why the same object can only be walked once:
an iterator holds a spot, and there's no way to move it backwards.

Seeing the protocol right makes the action concrete:

```python
def two():
    yield 1
    yield 2

g = two()
print(next(g), next(g))
try:
    next(g)
except StopIteration:
    print("exhausted")
```

```
1 2
exhausted
```

Two details follow from this. `iter()` on a list returns a *new* iterator each
time, which is why a list can be looped over again and again. `iter()` on a
gen returns the gen itself. This Is why it can't. And a `return`
inside a gen doesn't return a value to the caller &mdash; it raises
`StopIteration`, and any value goes on the exception rather than to the loop.

## Where generators surprise people

Three actions account for most of the confusion, and all three follow from
laziness.

**Nothing runs until you ask.** Calling a gen function executes none of
its body. If the first line validates an arg and raises, the exception
arrives at the first `next()`, not at the call. Possibly in a fully
different function. Where that matters, split it: a normal function that
validates and then returns the gen.

**The values are found late.** A gen formula that closes over a
variable reads that variable when it runs, not when it was written. Rebind the
variable in between and the gen sees the new value. This Is the same
late-binding action as the lambda-in-a-loop trap.

**Exhaustion is silent.** A second pass over a used gen makes nothing
and raises nothing. The symptom is an empty result far from the cause, and the
diagnosis is almost always that a thing already consumed it &mdash;
often a `sum()` or a `len(list(...))` written for a debugging print.

The habit that avoids all three: decide early whether a thing is a stream or a
collection. If it's a collection, call `list()` on it once and pass the list
around.

## send, throw and close

A gen can also receive values. This Is the feature that made Python's
coroutines possible before `async` existed.

`g.send(value)` resumes the gen and makes the paused `yield` formula
test to `value`, rather than to `None` as it does with `next()`. That turns
the gen from a producer into a thing that can be fed &mdash; the
classic example is a running mean that accepts numbers and yields the mean
so far.

`g.throw(exc)` raises an exception at the point of the `yield`, letting the
gen handle it or clean up. `g.close()` raises `GeneratorExit` there,
which is what lets a `finally` or a `with` inside a gen run its cleanup
when the gen is discarded.

In everyday code you'll use none of these right. They're worth knowing
because they explain things you'll see: why `contextlib.contextmanager` can
turn a gen into a `with` block, why a `with` inside a gen is safe,
and why `async def` looks so much like a gen. It grew out of one.

## Generators against the class you would otherwise write

Before gens, making a sequence lazily meant writing a class with the
iterator protocol on it by hand. Checking the two is the clearest way to see
what `yield` really saves.

The class version has to store its own state as fields, decide in `__next__`
what to do next based on those fields, and raise `StopIteration` itself
when it's finished. any of it with a loop in it turns a state machine: what
was a `for` and an `if` turns into a counter, a flag, and a chain of
if-tests rebuilding where it had got to.

The gen version stores the state silently. The local variables, the
spot in the loop, the depth of the nesting. All of it's the paused
frame, and `yield` is where it pauses. That is why a gen for walking a
nested structure is four lines and the equal class is thirty: recursion
and loops carry the state for you, and a class has to make it clear.

There's still a case for the class. It can hold methods other than iteration,
it can be reset, it can expose its spot, and it can run `__len__` so
that `len()` works. A gen can do none of those. When the object is a
collection with an order, a class is right. When it's a process that makes
values, `yield` is right.

The hands-on version of that rule: if you find yourself writing
`self.index`, `self.buffer` and a `__next__` full of branches, the code you
meant to write is a gen function with a loop in it.

## Questions people ask

<strong>What is the difference between a gen and a list
comprehension?</strong> Brackets. `[x for x in y]` builds a list;
`(x for x in y)` makes values on demand.

<strong>Can I get the length of a gen?</strong> Not without consuming it.
`sum(1 for _ in g)` counts it, and leaves it exhausted.

<strong>Can a gen have a `return`?</strong> Yes, and it ends the
gen. The returned value is attached to `StopIteration` rather than handed
to the loop.

<strong>Are gens faster than lists?</strong> Not per item. They're
faster to start, use far less memory, and avoid work the consumer never asks
for.

<strong>Can I index a gen?</strong> No. Use `itertools.islice` to skip
and take, or build a list.

<strong>What is the difference between `yield` and `yield from`?</strong>
`yield` makes one value. `yield from` makes each value of another
iterable, and passes `send` and `throw` through to it.

<strong>Why does my gen not raise until later?</strong> Because the body
doesn't run until the first value is requested.

<strong>Can I nest gen expressions?</strong> Yes, and the inner one is
consumed lazily too. Readability is often the limit rather than any
technical one.

<strong>Do gens work with `in`?</strong> Yes, and the test consumes the
gen up to the match, leaving the rest. Testing twice won't behave the
way you expect.

<strong>Is a file object a gen?</strong> Not just, but it's an
iterator over lines, which is why `for line in f` works and why it too can only
be walked once without seeking back.

<strong>Can two loops share one gen?</strong> They can consume it between
them, each taking what the other hasn't. That is at times handy and
much more often a bug.

<strong>What happens to a gen I stop halfway?</strong> It stays paused
until it's garbage-collected, at which point `GeneratorExit` is raised inside
it so `finally` blocks and `with` statements can clean up.

## The one-line summary worth carrying

A gen is a function that makes a sequence instead of returning a
value, and it does it one item at a time, on demand, remembering just where
it stopped.

All else on this page is a consequence of that sentence. The memory
saving is because only one item exists at a time. The single pass is because a
paused function can't be rewound. The infinite sequences are because nothing
is built in advance. The late exceptions are because the body hasn't run yet.
And the pipelines work because a gen consuming another gen is
still only asking for one item.

## Recap in one screen

- A gen function returns an object. The body runs only when values are
  asked for.
- One pass, no length, no indexing. Call `list()` when you need any of
  those.
- Memory is flat even so of the size of the sequence. This Is what makes
  infinite sequences and huge files workable.
- A pipeline of gens moves one item end to end at a time, doing no work
  the consumer doesn't ask for.
- `for` works by calling `next()` until `StopIteration`. A gen simply
  runs that protocol.
""")


extend("zip_function", """
## A worked example: comparing two lists

The job `zip` was made for, with `enumerate` supplying the spot so the
report can say where the difference is:

```python
expected = [1, 2, 3]
actual = [1, 5, 3]

for i, (e, a) in enumerate(zip(expected, actual)):
    if e != a:
        print(f"row {i}: expected {e}, got {a}")
```

```
row 1: expected 2, got 5
```

The double unpacking in `for i, (e, a) in` is worth reading slowly.
`enumerate` yields `(index, item)`, and here the item is itself the pair
`zip` made, so the brackets take it apart in the same statement. Written
without them you'd get `i` and a tuple. Would have to index into it on
the next line.

This is the shape behind most check code: diffing two versions of a
record, checking a result against a fixture, lining up a header row with a data
row. Note what it does *not* do. If the lists are different lengths, the
extra rows are never checked, and the report is silently incomplete. That is
the arg for `strict=True` in one sentence.

## Transposing with a star

Mixing the star and `zip` turns rows into columns:

```python
matrix = [[1, 2, 3], [4, 5, 6]]
print(list(zip(*matrix)))
```

```
[(1, 4), (2, 5), (3, 6)]
```

`*mat` passes each row as a separate arg, so `zip` receives two
iterables and takes one item from each in turn. Which is just a
transpose. The result is a list of tuples rather than lists, and the rows must
be the same length or the short one truncates all, both of which are
the plain `zip` rules applied in an unusual place.

This is the same op as unzipping a list of pairs. This Is why both are
written `zip(*a thing)`. A list of pairs *is* a two-column mat, and
transposing it gives you the two columns.

## Where zip removes an index

The value of `zip` is easiest to see by looking at what it replaces. The
index-based version of walking two lists together has to create a counter,
bound it right, and reach back into both lists on each line that uses a
value.

Each of those is a place to be wrong. The counter can start at one. The bound
can use the wrong list's length. This Is fine until the lists differ. The
lookups can be transposed, so that names are read from the scores list. None of
these give an error. They give wrong output, which is worse.

`zip` drops all three at once by handing you the values right. There's no
counter to get wrong, no bound to find, and no lookup to transpose, because
the names arrive already bound to the right variables. This is the same
arg as `for item in items` over `for i in range(len(items))`, applied to
more than one sequence.

The index is still available when you want it. That is what `enumerate`
around a `zip` is for. But now it's there because you asked, rather
than because iteration needed it.

## The other things that produce pairs

`zip` is one of a few things in Python that yield tuples, and they all pair
with the same unpacking syntax. Recognising the family makes a lot of loops
read the same way.

`enumerate(items)` yields `(index, item)`. `dict.items()` yields
`(key, value)`. `zip(a, b)` yields `(a_item, b_item)`. `itertools.pairwise`
yields back to back shared pairs from one sequence. This Is what you want
for checking each item with the next.

All four are consumed the same way: `for x, y in thing`. The unpacking isn't a
feature of any of them. It's the plain tuple unpacking from elsewhere in
the track, applied to what the loop happened to give. That is why
`for k, v in d.items()` works, and why losing `.items()` gives you keys and
a confusing error rather than a helpful one.

They also combine. `zip(a, b, c)` for three sequences, `enumerate(zip(a, b))`
for a spot alongside a pair, `zip(d.keys(), d.values())` for the long way
of writing `d.items()`.

## Parallel lists, and when zip is patching a design problem

`zip` is the right tool for sequences that truly match, and it's also
what lets a questionable data model keep working. So It's worth knowing which
situation you're in.

Two lists are parallel when item *i* of one shows the same thing as item
*i* of the other. Nothing in the language enforces that. It's an rule
living fully in the programmer's head, and each op has to preserve
it: sorting one list without the other breaks it, filtering one breaks it,
appending to one and losing the other breaks it, and none of those raise.

The failure is quiet and it compounds. A sort applied to `names` but not to
`scores` makes output where each name has somebody else's score, and the
program reports it confidently. There's no assertion that could have caught it
without checking against a source of truth that no longer exists.

When the lists are built together and consumed together in one function, that
risk is held and `zip` is just right. When they're stored on an
object, passed between functions or returned from an API, the rule has to
live code that no one has written yet, and the better structure is one list
of records &mdash; tuples, dicts, dataclasses &mdash; where the name and
the score are in the same object and can't be separated.

The tell is a sort. If you find yourself sorting two lists in step, or writing
`zip`, sorting the pairs, and unzipping them again, the data wanted to be pairs
all along.

## Deciding what unequal lengths mean

Three actions are available and the choice is about what a mismatch would
signify in your program. It's worth deciding on purpose rather than taking
the default.

**Truncating is right when one side is truly open-ended.** Pairing a finite
list against an infinite counter, taking as many rows as you've templates,
reading until the shorter source is exhausted. Here stopping at the
shortest is the whole point, and the default does what you want.

**Raising is right when equal lengths are an rule.** Two lists built from
the same source, a header row and a data row, expected and actual results: if
they differ, a thing upstream is broken and each line of output after that
point is suspect. `strict=True` converts a wrong answer into an exception,
which is almost always the better outcome.

**Padding is right when the missing items have a meaning.** Filling absent
values with `None`, zero or a default. So That the shorter list is treated as
incomplete rather than as terminating the whole op.
`itertools.zip_longest` does this, and choosing the fill value is choosing what
"missing" means in the result.

The default is the truncating one. This Means it's the choice you make by not
choosing. On any of it where a mismatch would be a bug, that is the wrong
default, and one keyword arg fixes it.

## Comparing each item with the next

A close scaled of zipping two lists is zipping one list against itself, offset
by one, which pairs each item with its successor.

`zip(items, items[1:])` does it right: the second arg starts one
spot later, so the first pair is items 0 and 1, the second is 1 and 2, and
the whole thing stops one short of the end because the offset list is one
shorter. That truncation is the default action doing just the right
thing for once.

This is the shape for any question about back to back items: are the values
growing, where are the gaps in a sequence of dates, what is the difference
between each reading and the last. Written with indices it needs a loop from 1
to `len(items)` and two lookups per pass. Written this way it's one line and
has no index at all.

Since Python 3.10 `itertools.pairwise(items)` does the same thing without the
slice, which matters when the input is a gen and can't be sliced.

## Questions people ask

<strong>What does `zip` return?</strong> An iterator of tuples. Wrap it in
`list()` to see it or to keep it.

<strong>Can I zip more than two things?</strong> Yes, any number. Each pass
yields a tuple with one item from each.

<strong>What if the lists are different lengths?</strong> It stops at the
shortest, silently. `strict=True` raises instead, from Python 3.10.

<strong>How do I pad the shorter one?</strong> `itertools.zip_longest`, which
fills with `None` or a value you choose.

<strong>Can I zip a dict?</strong> Yes, and you get its keys, because
that is what iterating a dict gives. Use `.items()` for pairs.

<strong>Why did my second loop over a zip do nothing?</strong> Because it's an
iterator and the first loop consumed it. Build a list if you need it twice.

<strong>Does `zip` copy the data?</strong> No. It holds refs and makes
tuples on demand, so it works on gens and infinite sequences.

<strong>Is `zip` the same as a DB join?</strong> No, and the difference
matters. A join matches rows by a key. `zip` matches them by spot, and has
no idea whether the things it paired belong together.

<strong>Can I zip strings?</strong> Yes. A string is iterable, so
`zip("abc", "xyz")` pairs the characters.

## Recap in one screen

- `zip` walks a few iterables in step and yields one tuple per spot,
  which drops the index and all that can go wrong with it.
- It stops at the shortest input without a word. Use `strict=True` when equal
  lengths are an assumption rather than a coincidence.
- `zip(*pairs)` unzips, and `zip(*mat)` transposes &mdash; the same
  op seen from two angles.
- `dict(zip(keys, values))` is the standard way to build a mapping from two
  parallel lists.
- It's lazy, so it works on gens and can only be walked once.
""")


extend("dict_and_set_comprehensions", """
## A worked example: a lookup table and a grouping

The two jobs that send people to a dict comprehension, side by side &mdash;
because only one of them is really a comprehension:

```python
rows = [("ana", "red"), ("bo", "blue"), ("cy", "red")]

team_of = {name: team for name, team in rows}
print(team_of["cy"])

by_team = {}
for name, team in rows:
    by_team.setdefault(team, []).append(name)
print(by_team)
```

```
red
{'red': ['ana', 'cy'], 'blue': ['bo']}
```

The first is a comprehension because each row makes just one entry, and
later rows are allowed to overwrite earlier ones. The second is a loop because
each row *adds to* an entry, and a comprehension can't do that &mdash; each
iteration makes an free key and value, with no access to what the
dict already holds.

That is the cutting line, and it's worth stating as a test: if the value for
a key depends only on the current item, a comprehension works. If it depends on
the other items too &mdash; a count, a list, a running total &mdash; you need a
loop, a `defaultdict`, or a `Counter`.

## Scope, and the variable that does not leak

A comprehension has its own scope. This Is why the loop variable doesn't
live it:

```python
n = "outer"
squares = [n * 2 for n in range(3)]
print(n, squares)
```

```
outer [0, 2, 4]
```

In Python 2 this printed `2`, because the comprehension shared the enclosing
scope and clobbered `n`. Python 3 gave comprehensions their own, which removed
a whole class of accidental overwrites and is the action to lean on.

Two consequences follow. The variable is down afterwards, so a
comprehension can't be used to find a thing you then want to inspect
&mdash; that needs a loop. And the comprehension can still *read* names from
the enclosing scope, which is what makes `[x for x in items if x > threshold]`
work.

The one place this surprises people is inside a class body, where the
comprehension's scope can't see the class's other names. A comprehension in a
class body that refers to another class field raises `NameError`, and the
fix is to find it outside the class or pass it in through the iterable.

## Sets, and the operations that follow

Building a set with a comprehension is often the first half of a job whose
second half is set algebra, and the two together replace a surprising amount of
loop-and-flag code.

`{r["city"] for r in rows}` gives the distinct cities. Once you've two such
sets, `a - b` is "in the first and not the second", `a & b` is "in both", and
`a ^ b` is "in one but not both". Those three answer most of the questions
people write nested loops for: which records are new, which have disappeared,
which are shared.

The comprehension form matters here because it does the deduplication as it
goes. Writing `set([r["city"] for r in rows])` builds the whole list first and
then discards the duplicates. This Is more memory for the same answer. For a
large input the difference is real, and the direct form also states the intent
&mdash; uniqueness is the point, not a cleanup step afterwards.

What you give up is order and indexing. A set has neither, so if the result
feeds a thing that cares about sequence, sort it on the way out:
`sorted({...})` gives a list back in a defined order.

## Nesting, and the two conditionals

Comprehensions have two places a rule can appear, and they do different
things.

A trailing `if` filters &mdash; items that fail it give nothing at all:
`{k: v for k, v in d.items() if v}` drops falsy values. A if-based
formula in the value slot chooses. Each item makes an entry, and
the rule picks what goes in it:
`{k: v or 0 for k, v in d.items()}` keeps each key and substitutes a default.
Reaching for the wrong one gives you either missing keys or unwanted ones, and
the symptom is a dict of the wrong size.

Nesting a second `for` is legal and reads in the order written, outermost
first: `{c for row in grid for c in row}` collects each cell of a grid of
rows. The rule is that the clauses appear in the same order as the equal
nested loops, which is the opposite of the order people guess when they meet it
in someone else's code.

Both features are worth knowing and neither is worth mixing. A comprehension
with two `for` clauses, a filter and a if-based value is a line that has to
be decoded rather than read, and the loop it replaces would have been four
clear lines.

## What is built, and when it matters

The four bracket forms differ in more than the type of the result: they differ
in what exists in memory while they run, and at times that is the deciding
factor.

A list, set or dict comprehension builds the whole result before any of it else
happens. For a thousand items that is irrelevant. For ten million it's the
difference between a program that runs and one that doesn't, and the
gen formula &mdash; round brackets &mdash; is the version that holds
one item at a time.

The rule of thumb is what happens to the result. If it's consumed once, by a
`sum`, a `max`, a `for`, or an `any`, a gen formula does the same job
without materialising any of it: `sum(x * 2 for x in items)` never builds a
list. If it's indexed, iterated twice, measured with `len`, or returned to a
caller who will do any of those, it has to be a real collection.

There's one case where building the mid is a genuine waste and easy
to miss: wrapping a list comprehension in a converter.
`set([f(x) for x in items])` and `dict([(k, f(k)) for k in keys])` both build a
list and right away throw it away. Writing the set or dict comprehension
right skips that fully. This Is one reason those forms exist at all.

The reverse mistake is reaching for a gen formula where a list is
wanted, and then calling `list()` on it. That builds the same list through more
machinery, and the comprehension says it more right.

## Readability, stated as a limit

each section here has hinted at a boundary, and it's worth making clear,
because "use a comprehension when it's clear" is advice that gives no help at
the moment of writing.

A hands-on limit: one `for`, at most one `if`, and an formula short enough
that the whole thing fits on one line without wrapping. That covers the large
majority of genuine uses and makes a thing a reader takes in at a glance.

Past that, the questions to ask are whether a reader could say what the result
holds without tracing it, and whether it can be changed without being
rewritten. A comprehension that needs a comment above it to explain what it
makes has already answered both.

The escape hatch is often a named function. Pulling the formula out into a
function with a real name leaves a comprehension that is one `for` and a
call &mdash; readable again, and the complicated part now has a name, a place
to put a docstring, and a place to test it.

## Questions people ask

<strong>Why does `{}` give a dict and not a set?</strong> Dicts had the
braces first. `set()` is the only way to write an empty set.

<strong>Can I build a frozenset with a comprehension?</strong> Not right.
`frozenset(x for x in items)` wraps a gen formula.

<strong>What happens to duplicate keys?</strong> The last one wins, silently.
Nothing warns you.

<strong>Is a dict comprehension faster than a loop?</strong> Slightly, because
the whole thing runs in one bytecode loop without repeated field lookups.
Not enough to be the reason to choose it.

<strong>Can I use `zip` inside one?</strong> Yes, and
`{k: v for k, v in zip(keys, values)}` is common &mdash; though
`dict(zip(keys, values))` is shorter when nothing is transformed.

<strong>Does the order of a dict comprehension matter?</strong> Yes. The result
keeps insertion order, so the order of the input decides the order of the
output.

<strong>Can I have an `else` without an `if` filter?</strong> Only in the value
slot, as part of a if-based formula. The trailing filter has no `else`.

<strong>Can a comprehension call a function with side effects?</strong> It
can, and it shouldn't. A comprehension whose result is discarded is a loop
written to look like an formula.

<strong>Do comprehensions work in older Python?</strong> List comprehensions
since 2.0, dict and set comprehensions since 2.7 and 3.0. any of it current
supports all of them.

## Recap in one screen

- The brackets choose the type: `[]` list, `{}` set, `{k: v}` dict, `()`
  gen. All else about the syntax is the same.
- A comprehension works when each item makes one free entry. Counting
  and grouping need a loop, `setdefault` or `Counter`.
- Duplicate keys collapse silently, and so do duplicate set members &mdash;
  that is the point of a set and a hazard in a dict.
- The loop variable has its own scope and doesn't leak, except that it can't
  see a class body's other names.
- A trailing `if` filters items out. A if-based formula in the value slot
  keeps them and changes the value.
""")


extend("shallow_and_deep_copy", """
## Watching the difference with is

The rule is one line of output away from being obvious:

```python
import copy

original = {"a": [1, 2]}
shallow = original.copy()
deep = copy.deepcopy(original)

print(original["a"] is shallow["a"])
print(original["a"] is deep["a"])

shallow["a"].append(3)
print(original, deep)
```

```
True
False
{'a': [1, 2, 3]} {'a': [1, 2]}
```

The first two lines are the whole gap. After a shallow copy, the inner
list is *the same object*. After a deep copy it's a new one. The last line is
the consequence: appending through the shallow copy changed the first, and
the deep copy was untouched.

Note that the outer dicts are different objects in both cases. A shallow
copy is a real copy. Adding a new key to `shallow` doesn't affect
`first`. It's only one level deep, and each problem on this page comes
from the level below.

## Where this actually comes up

The trap is rarely met head-on. It arrives through four plain situations.

**Configuration loaded from JSON or YAML.** These are nested dicts by
nature, `.copy()` looks like it did the job, and a function that adjusts one
value has quietly adjusted it for everybody.

**A default that is a nested structure.** A module-level `DEFAULTS` dict copied
shallowly into each new object means each object shares the same inner
dicts. The objects look free and aren't.

**A list of records.** `rows[:]` gives a new list of the same dicts, so
sorting or filtering the copy is safe and editing a record through it isn't.
This is a common one because the copy was made in detail to be safe.

**Undo, or "keep the first for check".** Snapshotting state before a
change is the exact case where a shallow copy fails: the snapshot shares the
mutable parts with the thing that is about to change. So By the time you
compare, both have moved.

The pattern across all four is that the copy was made for safety, and shallow
copying gives that safety only for the top level. If the reason for copying
is "so that changes over here don't affect over there", the question to ask is
how deep the changes go.

## Equality survives copying; identity does not

After any copy, shallow or deep, `copy == first` is `True` and
`copy is first` is `False`. That is the intended action and it's worth
being clear about, because it's how you check that a copy did what you
meant.

For your own classes it holds only if you defined `__eq__`. Without one,
Python checks by identity, so a copy of your object is *not* equal to the
first &mdash; which surprises people who have just written a careful
`__deepcopy__` and find their tests failing on the check rather than the
copy. Defining `__eq__` on a class whose instances get copied around is
in effect needed, and a dataclass writes it for you.

`deepcopy` also preserves structure that a naive copy would flatten. If two
entries in a dict point at the same list, the deep copy has two entries
pointing at one *new* list. The sharing is copied rather than
duplicated. That is often what you want, and it's one more thing a
hand-written recursive copy gets wrong.

## Immutability removes the question

The most solid fix for a copying bug is to not need the copy.

If the structure is built from tuples, frozensets, strings and numbers, then
nothing inside it can change. So Sharing it's safe and a shallow copy is a
complete one. The gap that this whole page is about simply doesn't
arise. That is why no one worries about copying a tuple of strings, and why
`deepcopy` on such a structure is wasted work.

The hands-on version is to make the things that travel immutable. A record
passed between functions is better as a frozen dataclass or a `NamedTuple` than
as a dict: it can't be edited by a function that received it, so no
defensive copy is needed at any boundary. Where a modified version is needed,
`_replace` or `dataclasses.replace` builds a new one and leaves the first
alone.

Keep the mutable structures local. Here Each name pointing at them is visible
in the same function. Then copying turns a choice you make at times
rather than a defence you've to note all over.

## Deciding, in four questions

When you're about to copy a thing and aren't sure which kind you need, the
answer follows from four questions asked in order.

**Does any of it inside it change?** If each item is a number, a string or a
tuple of those, any shallow copy is a complete one. Stop here. This covers most
copying.

**Am I copying so that changes over here don't affect over there?** If the
answer is no &mdash; you're copying to get a list you can sort, or to add one
key &mdash; then a shallow copy of the outer container is just what you
want and nothing more is needed.

**How deep do the changes go?** If the code that follows only touches the top
level, shallow is enough even so of what is nested underneath. If it reaches
into nested structures, each level it reaches has to have been copied.

**Is the structure large or does it hold a thing uncopyable?** `deepcopy` on
a big object graph costs real time, and on an object holding a link, a
file or a lock it either fails or duplicates a thing that should be unique.
Both are signals to restructure rather than to copy harder &mdash; often by
making the shared parts immutable, or by rebuilding the small part you need to
change rather than duplicating the whole.

Most real answers land on shallow, and the ones that don't are often nested
configuration or a snapshot taken for check. Knowing which of those you
are in is more handy than a rule about which function to call.

## Questions people ask

<strong>Is `list(x)` a deep copy?</strong> No. It's one of the shallow ones,
along with `x[:]` and `x.copy()`.

<strong>Does `deepcopy` handle cycles?</strong> Yes. It remembers what it has
already copied, so a structure that refers to itself doesn't cause infinite
recursion.

<strong>Is `deepcopy` slow?</strong> scaled to a shallow copy, a lot.
It walks the whole structure and keeps a record as it goes. For small
structures it doesn't matter.

<strong>How do I copy only two levels?</strong> There's no built-in for that.
A comprehension that shallow-copies each item &mdash;
`{k: v.copy() for k, v in d.items()}`. Is the usual answer.

<strong>Can I stop an field being deep-copied?</strong> Yes, by defining
`__deepcopy__` on the class. This Is how objects holding a link or a
lock avoid duplicating it.

<strong>Does copying a string do any of it?</strong> No. Strings are immutable,
so `copy` returns the same object.

<strong>What about `copy.copy` versus `.copy()`?</strong> The same thing for
builtins. `copy.copy` also works on objects that have no `.copy()` method.

<strong>Does `deepcopy` copy class meanings too?</strong> No. Classes,
functions and modules are treated as atomic and shared rather than duplicated,
which is what you want.

<strong>Is pickling and unpickling a valid deep copy?</strong> It often
makes one, and it's slower and fails on any of it unpicklable. Use
`deepcopy`, which is what it's for.

<strong>Why does copying a nested list "at times" work?</strong> Because it
works when nothing reaches past the top level afterwards. The copy was
always shallow. The code simply had not yet touched the shared part.

<strong>Should a function copy the args it's given?</strong> Only if it
stores them or mutates them. A function that reads a list and returns a result
has no reason to copy any of it, and copying defensively all over costs more
than the bugs it blocks.

<strong>What is the fastest way to copy a flat list?</strong> `x.copy()` and
`x[:]` are equal and both are fast. `list(x)` is the one that also accepts
any iterable, which is at times why it's chosen.

## Recap in one screen

- A shallow copy duplicates the outer container and shares all inside
  it. `first[0] is shallow[0]` is the test.
- Shallow is a complete copy when the contents are immutable. This Is why the
  problem stays hidden for so long.
- `copy.deepcopy` rebuilds the whole structure, preserves shared refs and
  lives cycles &mdash; and costs proportionally.
- The bugs arrive through config dicts, shared defaults, lists of records and
  snapshots, not through code that obviously copies.
- Making the data immutable drops the question fully.
""")


extend("enumerate_function", """
## The off-by-one that start= invites

`start=1` changes the number you're handed and nothing else. The item is still
the same item, and the spot it occupies in the list is still one lower:

```python
names = ["ana", "bo", "cy"]

for n, name in enumerate(names, start=1):
    print(n, name, names[n - 1], names[n] if n < len(names) else "-")
```

```
1 ana ana bo
2 bo bo cy
3 cy cy -
```

The third column is the item, reached right with `n - 1`. The fourth shows
what indexing with `n` gives you: the *next* item, and eventually the end of
the list.

This is why `start=` is for display and not for access. The moment you use the
number both to print and to index, you've two meanings for one variable and
one of them is wrong. If you truly need both, take the real index and add
one where you print it:

```python
for i, name in enumerate(names):
    print(i + 1, name, names[i])
```

Wordier by one character, and it can't be got wrong.

## A worked example: numbering only what matters

The awkward case is numbering output when some items are skipped, because the
enumerate counter keeps advancing whether you used it or not:

```python
lines = ["alpha", "", "beta", "", "gamma"]

shown = 0
for line in lines:
    if not line:
        continue
    shown += 1
    print(shown, line)
```

```
1 alpha
2 beta
3 gamma
```

Written with `enumerate` and a `continue`, the numbers would have come out 1, 3
and 5, because `enumerate` counts spots in the input and not lines
made. Neither is wrong. They answer different questions.

The rule that falls out: `enumerate` numbers the *source*. If you want to
number the *output*, and the loop can skip items, you're back to a counter
&mdash; and that is one of the few left places a manual counter is the
right answer.

A middle ground worth knowing: filter first, then enumerate the result.
`for n, line in enumerate((l for l in lines if l), start=1)` numbers what
lives, and keeps the counter out of the body.

## Both numbers at once

At times you want the spot *and* the item *and* a thing from a second
sequence, which is where `enumerate` and `zip` combine:

```python
names = ["ana", "bo"]
scores = [91, 78]

for i, (name, score) in enumerate(zip(names, scores)):
    print(i, name, score)
```

```
0 ana 91
1 bo 78
```

The brackets around `(name, score)` are doing real work. `enumerate` yields
`(index, item)` where the item is the tuple `zip` made, so the pattern on
the left has to have the same shape: a number, then a pair. Leaving the
brackets out is a `ValueError` about unpacking, and it's one of the clearer
error messages you'll meet.

The order matters too. `zip(enumerate(names), scores)` also works and gives you
`((0, "ana"), 91)`, which unpacks as `for (i, name), score in ...`. Both are
legal. The first reads better because the index stays at the front where a
reader expects it.

## Why wanting the index is usually a question worth checking

`enumerate` makes the index easy to get. This Makes it worth asking, each
time, whether you really need it. A surprising share of loops that ask for a
spot are working around a thing else.

**Checking an item with its neighbour.** The index is being used to reach
`items[i - 1]` or `items[i + 1]`. What you want is back to back pairs, and
`zip(items, items[1:])` or `itertools.pairwise` gives them without any index or
any bounds check at the ends.

**Walking two sequences together.** The index is being used to index both.
`zip` pairs them right, and drops the possibility of the two lookups
disagreeing.

**Building a lookup of where things are.** The loop collects spots into a
dict. A dict comprehension over `enumerate` says it in one line, and
often the real question is "does this hold x" or "which comes first", both
of which have direct answers.

**Modifying the list while walking it.** The index is being used to assign back
with `items[i] = ...`. This works and is the one case where the index is
truly needed &mdash; but building a new list with a comprehension is
often clearer, and dropping items by index while iterating is a bug in
waiting.

What is left after those is the honest use: displaying a number to a person,
reporting which record failed, or writing into a pre-sized structure. Those are
real, and `enumerate` is just right for them.

## Where you will actually meet it

Three situations account for most real uses, and they share a shape: the number
is going a place a human will read it.

**Reporting which line failed.** Parsing a file and validating rows, the index
is what turns "invalid date" into "line 47: invalid date". Without it the error
message is useless on a file of any size, and `start=1` matters because people
count lines from one and so does each text editor.

**Progress through a long job.** `if n % 1000 == 0: print(n)` inside a loop
over a large iterable gives you a heartbeat, and because `enumerate` is lazy it
costs nothing on a stream you're already reading.

**Numbered output.** Menus, ranked results, numbered steps, table rows. Here
the number is presentation. This Is just the case `start=1` exists for
and just the case where using it to index would be wrong.

The common thread is that the index is an output rather than a mechanism. When
the number is being printed, `enumerate` is the tool. When the number is being
used to reach back into the data, there's often a way to get the data
right instead.

## Numbering things that are not lists

`enumerate` takes any iterable, and the notable cases are the ones that are
not sequences, because the spot it hands you means a thing slightly
different in each.

Over a **file**, the number is the line number, and it's the reason
`enumerate(f, start=1)` appears in each script that reports problems in a data
file. Nothing else gives you that number without reading the file twice.

Over a **gen**, the number counts what has been made so far. It's
the only way to know how far a stream has got. A gen has no length
and no spot you can ask for.

Over a **dict**, the number is the spot in insertion order, which is
well defined since Python 3.7 and is at times what you want &mdash;
numbering the entries of a config for display, say.

Over a **set**, the number is the spot in an any order. It's stable
within a single run and must not be leaned on across runs or between machines,
because it depends on hash values. If a number over a set matters, sort it
first and enumerate the sorted result.

Over a **string**, the number is the character spot, which makes
`enumerate(text)` a reasonable way to find where a thing occurs &mdash;
though `str.find` is often the direct answer.

The pattern across all of them is that `enumerate` counts iterations, not
spots in storage. For a list those are the same thing, and for all
else the gap is the whole point.

## The name, and where it came from

"Enumerate" means to list things one by one, and in older languages an
enumerator was the object that walked a collection. Python's `enumerate` keeps
the sense of walking while adding the numbering. This Is why the name is about
the traversal rather than about counting.

It arrived in Python 2.3, and the release note for it's unusually direct about
the motivation: the `range(len(...))` idiom was common, awkward, and a frequent
source of small errors. The feature exists in detail to drop a pattern
people kept writing, which is worth knowing because it tells you what the
intended use is. If your loop looks like the pattern it replaced, use it. If it
doesn't, the index it offers is probably not the thing you need.

## Questions people ask

<strong>Does `enumerate` build a list?</strong> No. It yields pairs on demand,
so it works on files, gens and any of it else iterable.

<strong>Can I use it on a dict?</strong> Yes, and you get spots
alongside keys. `enumerate(d.items())` when you want the pairs too.

<strong>What if I only want the index?</strong> Then you probably want
`range(len(items))` &mdash; but check first, because wanting only the index is
often a sign the loop is doing a thing else.

<strong>How do I name the unused half?</strong> `_` by rule, for either
spot: `for _, item in enumerate(items)` is legal though pointless.

<strong>Does `start=` accept a minus number?</strong> Yes. It's just the
number to begin counting from, and nothing validates it.

<strong>Is `enumerate` slower than a manual counter?</strong> No, it's faster
&mdash; the counting happens in C rather than in a bytecode `+= 1`.

<strong>Can I enumerate backwards?</strong> Not right.
`enumerate(reversed(items))` numbers from zero at the end. To get the first
indices descending, zip a reversed range instead.

<strong>Can I unpack a nested item right?</strong> Yes, with brackets:
`for i, (a, b) in enumerate(pairs)`. The pattern on the left has to match the
shape of what is yielded.

<strong>Why is my counter wrong when I use `continue`?</strong> If it's a
manual counter placed after the `continue`, it never runs for skipped items.
`enumerate` has no such problem, because the counting isn't in your loop body.

<strong>Can I start the count from a thing other than a number?</strong> No.
`start` is added to an int counter. So It has to be an int.

<strong>Is there a version that gives the index from the end?</strong> Not
built in. `zip(range(len(a) - 1, -1, -1), a)` does it. Is a good example of
the math `enumerate` most times saves you.

## Recap in one screen

- `enumerate` yields `(spot, item)`. The `for i, x` on the left is plain
  tuple unpacking.
- It drops both the manual counter and the `range(len(...))` indexing, along
  with the mistakes each invites.
- `start=` changes the label, not the spot. Never use that number to
  index back into the sequence.
- It's lazy and works on any of it iterable, including files too large to hold.
- If the loop skips items and you want to number the output, use a counter;
  `enumerate` counts the input.
""")


extend("nested_data_structures", """
## A worked example: from rows to a report

Most work with nested data is the same journey &mdash; records in, grouped
summary out. Here it's end to end:

```python
orders = [
    {"customer": "ana", "items": [{"name": "pen", "price": 2},
                                  {"name": "pad", "price": 5}]},
    {"customer": "bo", "items": [{"name": "pen", "price": 2}]},
]

totals = {}
for order in orders:
    total = sum(item["price"] for item in order["items"])
    totals[order["customer"]] = totals.get(order["customer"], 0) + total

for customer, total in sorted(totals.items(), key=lambda kv: -kv[1]):
    print(f"{customer:<6}{total:>4}")
```

```
ana      7
bo       2
```

Three moves, each from elsewhere in the track. The gen formula sums a
list-valued field without building an mid list. `totals.get(key, 0)`
builds up without a first-time special case. And `sorted` with a negated key
puts the largest first.

What makes it readable is that each level is handled at one depth. The inner
sum works on one order's items and knows nothing about customers. The outer
loop works on orders and knows nothing about prices. When nested-data code
turns hard to follow, it's almost always because one formula is reaching
through three levels at once.

## Naming the path

The single most handy habit with nested data is refusing to repeat a long path.
`record["user"]["profile"]["display_name"]` written in four places is four
places to update when the API changes. Four chances to typo a key into a
`KeyError` that names only the last one.

A one-line function fixes it:

```python
def display_name(record):
    return record["user"]["profile"]["display_name"]
```

The path now exists once. It has a name that says what it means, so the call
sites read as intent rather than as navigation. It has a place to put a
default or a `try`. And when the shape changes. And it will &mdash;
there's one line to edit.

This is worth doing at two levels of nesting, not four. The instinct to wait
until it gets bad is why it often does.

## Where the shape comes from, and what it costs

Nested data almost always arrives rather than being designed: it's the shape
some API returns, or the shape JSON has, or the shape a DB join made.
That has a consequence worth being deliberate about.

Data in the shape it arrived in is convenient for reading once and awkward for
all else. Nothing validates it. So A missing key is found at the
point of use rather than at the point of parsing. Nothing names it, so each
function that touches it has to know the layout. And nothing stops two parts of
the program disagreeing about whether a field is optional.

The option is to convert at the boundary: read the nested structure once,
pull out what you need, and build objects. Dataclasses, named tuples, or
just flatter dicts with the names you chose. All downstream then
works with a shape you defined, validated once, at a known place.

For a script that reads a file and prints a summary, this is overkill and the
raw structure is fine. For any of it long-lived, converting at the edge is the
difference between a program where a shape change breaks one function and one
where it breaks eleven.

## Depth, and when to stop nesting

Reading nested data is unavoidable. *Building* deeply nested data is a choice,
and often a poor one past two levels.

A dict of dicts of lists is hard to inspect, hard to iterate
without three loops, and hopeless to query except by walking. The option
is often a flat list of records where the nesting turns fields: instead of
`by_region[region][city] = [names]`, a list of
`{"region": ..., "city": ..., "name": ...}` rows.

Flat records are longer to write and enormously easier to work with. They sort
by any field, filter with one comprehension, group by whichever key the current
question needs rather than the one you committed to when you built the
structure, and convert right to CSV or a dataframe. The nesting you really
need can be made on demand with a grouping. This Is three lines.

The heuristic: nest when the structure reflects genuine containment that will
never be queried the other way round. Flatten when you can imagine wanting a
different grouping later &mdash; which, for any of it resembling a report, you
will.

## Failing at the boundary rather than in the middle

The trait problem with nested data is that a shape mistake surfaces
far from where it entered. A key that is missing from an API response is
found three functions later, as a `KeyError` naming a key that looks
correct, in code that has nothing to do with fetching.

The remedy is to check the shape once. Here The data arrives, rather than
defending against it all over afterwards. What that check looks like depends
on how much the data matters.

At the simplest, a few lines that pull out the fields you need and raise a
clear error if they're absent. The error then says "response is missing
`user.profile.name`" at the point of parsing. This Is a diagnosis rather than
a symptom.

A step up, build the values into a dataclass or a `NamedTuple`. build
fails right away if a field is missing, the resulting object has known
fields rather than any keys, and each function downstream can be
written against a shape that is ensured rather than hoped for.

Further still, a validation library &mdash; Pydantic being the common choice
&mdash; declares the expected shape as types and reports each problem at once,
with the path to each. That is worth it when the data comes from outside your
control and the cost of processing a thing malformed is high.

All three are the same idea at different sizes: convert once, at the edge, and
let all inside the boundary assume the data is what it claims to be. The
option &mdash; a `.get` chain at each use site &mdash; spreads the
uncertainty through the whole program and never really resolves it.

## Questions people ask

<strong>How do I get a value a few levels down safely?</strong> Chain `.get`
with `{}` defaults, or wrap the direct path in `try`/`except KeyError` when
lack is truly exceptional.

<strong>Why does `.get("a", {}).get("b")` work but `.get("a").get("b")`
not?</strong> Because the second returns `None` when the key is missing, and
`None` has no `.get`. The `{}` keeps a dict in the chain.

<strong>How do I see the shape of a thing I just parsed?</strong>
`print(json.dumps(data, indent=2))` for JSON-compatible data, and
`pprint.pprint` for any of it else.

<strong>Can I flatten an arbitrarily deep structure?</strong> Yes, with
recursion or a stack &mdash; but if the depth is unknown, that is often a
sign the data wants to be flat records instead.

<strong>Are nested comprehensions read inside-out?</strong> No. The `for`
clauses read left to right in the same order as the equal nested loops.

<strong>Why did my copy of a nested structure change?</strong> Because the copy
was shallow and the inner structures are shared.

<strong>Do JSON keys stay ints?</strong> No. They come back as strings,
which is a common surprise after a save-and-load round trip.

<strong>Should I use dotted access instead of brackets?</strong> Libraries that
turn dicts into field access look convenient and hide typos, since a
missing field and a missing key report differently. A dataclass gives you
the same ergonomics with the checking.

<strong>What is the fastest way to search nested data?</strong> Build an index
once &mdash; a dict keyed by what you search on &mdash; rather than
walking the structure on each lookup.

<strong>Is there a standard way to walk a structure of unknown depth?</strong>
Recursion, with a check on each value for whether it's a dict, a list,
or a leaf. The standard library has no general walker. What to do at
each node depends fully on the task.

## Recap in one screen

- Most real data is a list of records. The moves are index, key lookup, and an
  inner loop, composed to what depth is needed.
- Chain `.get(key, {})` for optional paths, and `try`/`except KeyError` when a
  missing value is exceptional rather than expected.
- Give a repeated path a named function at two levels of nesting, not four.
- Convert at the boundary into shapes you defined, unless the script is small
  enough that the raw structure will do.
- Prefer flat records over deep nesting for any of it you might want to group a
  different way later.
""")


extend("slicing_step_negatives", """
## A worked example: the three arguments together

each rule on this page in one block, with the results printed rather than
given:

```python
s = "abcdefgh"

print(s[2:5])
print(s[-3:])
print(s[::2])
print(s[::-1])
print(s[5:2:-1])
print(s[2:99], repr(s[99:]))
```

```
cde
fgh
aceg
hgfedcba
fed
cdefgh ''
```

Read them in order. `s[2:5]` starts at 2 and stops before 5. `s[-3:]` counts
from the right. `s[::2]` takes each second character from the whole string.
`s[::-1]` reverses. `s[5:2:-1]` walks backwards from 5 down to but not
including 2, which is where the exclusive stop starts feeling strange &mdash;
the item at index 2 is missing from the result though 2 is written on the
left of the colon.

The last line is the forgiveness: an end past the length is clamped, and a
start past the length gives an empty string rather than an error.

## Why a negative step reverses the roles

`s[2:5:-1]` returns nothing, and the reason is worth spelling out because it's
the one part of slicing people store rather than understand.

A slice always moves from the start value towards the stop value, in the
direction the step gives. With a plus step it moves right, so the start
must be to the left of the stop. With a minus step it moves left, so the
start must be to the *right* of the stop. `s[2:5:-1]` asks to begin at 2 and
walk leftwards until it reaches 5. This It never will. So The result is empty
right away.

That also shows the defaults. When the step is minus and you leave the
ends off, the omitted start turns the end of the sequence and the omitted
stop turns "past the beginning". Which is why `s[::-1]` gives you
all reversed, including the first character. Writing `s[::-1]` and
`s[len(s):0:-1]` aren't the same: the second stops before index 0 and drops
the first character.

The hands-on consequence is that there's no way to write "reversed, ending at
the very beginning" with an clear stop. The stop would have to be
-1, and -1 already means the last item. Omitting it's the only way to say it,
which is just why the idiom is `[::-1]` and not a thing more clear.

## Slice objects, and the syntax behind the colons

The bracket syntax is shorthand. `a[1:5:2]` is `a[slice(1, 5, 2)]`, and
`slice` is an plain object you can build, store and pass around.

That is at times handy in its own right. Naming a slice you use
again and again, `HEADER = slice(0, 4)`, makes the call sites say what they mean.
More often it's handy as an explanation. It's why `a[1:5]` and
`a[slice(1, 5)]` behave the same way, why a class can support slicing by
handling a `slice` in its `__getitem__`, and why the ellipsis and comma forms
that NumPy uses are possible at all: `a[1:5, ::2]` passes a tuple of slices,
which plain Python lists reject and NumPy arrays understand.

`indices()` on a slice object resolves it against a length, returning the
concrete start, stop and step after clamping and minus-index conversion.
`slice(1, 99).indices(5)` gives `(1, 5, 1)`. This Is the math the
forgiving action is built on, made visible.

## Slicing is a protocol, not a list feature

All on this page works on any sequence, and knowing that is what makes
the syntax worth learning properly rather than storing for lists.

Strings, tuples, bytes, bytearrays and `range` all slice with the same three
numbers and the same rules, and each returns its own type &mdash; slicing a
tuple gives a tuple, slicing a `range` gives a `range`, found rather than
materialised. `bytes` slicing is how binary formats are parsed, taking a
header, a length field and a payload by offset.

Beyond the builtins, any class can support it by handling a `slice` object in
`__getitem__`, and the libraries that do have extended the idea a lot.
NumPy accepts a tuple of slices, `a[1:5, ::2]`, to take a rectangle out of a
two-dimensional array, and its slices are *views* rather than copies &mdash;
writing into one changes the first. This Is the opposite of the list
action and a genuine trap when moving between them. pandas uses the same
brackets with labels rather than spots in `.loc`. Here The stop is
inclusive, breaking the one rule you had learned to lean on.

The lesson isn't to distrust slicing but to check two things when a new type
supports it: whether the result is a copy or a view, and whether the stop is
excluded. Those two answers differ across the ecosystem and all else
stays the same.

## Idioms worth recognising on sight

A handful of slices appear often enough to read as single symbols rather than
as math. Knowing them saves parsing the numbers each time.

`a[::-1]` reverses. `a[:]` copies a list, and is also the left-hand side of
`a[:] = b`, which replaces the contents of `a` in place rather than rebinding
the name &mdash; the difference that matters when someone else holds a
ref to `a`.

`a[:n]` and `a[n:]` are "the first n" and "all after the first n", and
together they cover the whole sequence just once. `a[-n:]` is the last n,
and `a[:-n]` is all except the last n. This Is how you drop a known
suffix without finding a length.

`a[::n]` takes each nth item, and `a[i::n]` takes each nth starting from `i`
&mdash; the pair of them is how you deinterleave two sequences that were
interleaved into one, with `a[::2]` and `a[1::2]`.

`s[:0]` is an empty sequence of the same type, at times handy as a
starting value when you need "an empty one of what this is" without naming
the type.

## Choosing between an index and a slice

The two look similar and they fail differently. This Is the basis for choosing
between them.

`a[i]` asserts that spot `i` exists. If it doesn't, you get an
`IndexError` naming the problem at the line that caused it. `a[i:i+1]` makes no
such assertion: out of range, it hands back an empty sequence and the program
carries on with nothing.

So the choice is about whether lack is a bug. Taking the first item of a list
that is documented to be non-empty should be `a[0]`, because an empty list
means a thing upstream is wrong and you want to hear about it. Taking "up to
ten results" from a list that might have three should be `a[:10]`, because
having fewer is expected and the clamping is just right.

The mistake in one direction is a crash on data that was always going to be
short. The mistake in the other is a silent empty result that gets reported as
zero, saved as an empty file, or treated as "no matches found" &mdash; and
those are much harder to trace, because there's no error to start from.

One hands-on consequence: when a slice with found bounds returns nothing,
don't assume the data was empty. Print the bounds. An off-by-one that makes
`a[5:5]` looks the same in the output to a list that truly had nothing to
give.

## Questions people ask

<strong>Is `a[:]` the same as `a.copy()`?</strong> For a list, yes &mdash; both
are shallow copies. For a string it returns the same object, since there's
nothing to copy.

<strong>Why does `a[::-1]` work on strings and `a.reverse()` not?</strong>
`reverse` is a list method that mutates, and strings can't be mutated.

<strong>What is the difference between `a[::-1]` and `reversed(a)`?</strong>
The slice builds a new sequence. `reversed` returns a lazy iterator and copies
nothing.

<strong>Can I slice a gen?</strong> No. Use `itertools.islice`, which
takes the same start, stop and step but can't go backwards.

<strong>Does slicing a tuple give a tuple?</strong> Yes. A slice returns the
same type as the thing sliced, for the built-in sequences.

<strong>How do I take each nth item starting from the end?</strong>
`a[::-n]` &mdash; the minus step both reverses and strides.

<strong>Why is `a[1:3] = [1, 2, 3]` allowed?</strong> Because slice set
replaces a section and may change the length. It's the mutating counterpart of
the copying slice.

<strong>Does slicing a list of objects copy the objects?</strong> No. The new
list holds the same objects. This Is the shallow-copy action from elsewhere
in the track.

<strong>Can the step be zero?</strong> No. `a[::0]` raises `ValueError`,
because a step of zero would never advance and the slice would never end.

<strong>Is `a[0:len(a)]` the same as `a[:]`?</strong> Yes, and the shorter form
is preferred &mdash; it doesn't have to find a length that the slice
already handles.

## Recap in one screen

- Three numbers: start, stop, step. The stop is always excluded, just as in
  `range`.
- Minus indices count from the right, and can be mixed freely with plus
  ones.
- A minus step swaps the roles of start and stop. This Is why `s[2:5:-1]`
  is empty and `s[::-1]` reverses.
- Slicing clamps rather than raising. This Is convenient and at times
  hides a wrong index.
- A slice copies. Assigning into a slice mutates, and can change the length.
""")


extend("nested_conditionals", """
## The same logic, four ways

One rule set written four ways. So The difference is shape rather than
action:

```python
def price(age, member):
    if age < 18:
        if member:
            return 0
        else:
            return 5
    else:
        if member:
            return 8
        else:
            return 12


def price_flat(age, member):
    if age < 18 and member:
        return 0
    if age < 18:
        return 5
    if member:
        return 8
    return 12


for age, member in [(10, True), (10, False), (30, True), (30, False)]:
    print(age, member, price(age, member), price_flat(age, member))
```

```
10 True 0 0
10 False 5 5
30 True 8 8
30 False 12 12
```

Both are correct, and which reads better is truly arguable here. The nested
version makes the two-by-two structure visible: two ages, two membership
states, four outcomes. The flat version reads as a list of rules in priority
order, which is how a price list is often written down.

The point of running both is that flattening isn't automatically an
improvement. It's an improvement when the nesting was accidental &mdash; when
the inner `if` was the whole body of the outer one, or when the branches were
refusals. When the nesting reflects a genuine grid of cases, keeping it can be
the honest thing to do.

## Conditions that depend on each other

There's one case where flattening with `and` isn't merely a style choice but
really needed, and it comes from short-circuiting.

```python
user = None
if user is not None and user.active:
    print("never reached, and never raises")
print("fine")
```

```
fine
```

`and` stops as soon as the left side is false, so `user.active` is never
tested. Reverse the two halves and the same line raises `AttributeError`
&mdash; the check that was supposed to protect the access happens after it.

This is why nesting `if user isn't None:` around `if user.active:` and
flattening it to a single `and` are equal: both express "only ask the
second question if the first was true". What is *not* equal is writing
them in the other order, or joining them with `&`. This Tests both sides
unconditionally.

The general shape is worth recognising. Any time one rule establishes that
the next one is safe to ask. Not `None`, non-empty, key present, index
in range &mdash; the order is load-bearing and can't be rearranged for
readability.

## Where the nesting actually came from

Deep if-tests are rarely written that way. They build up, and the history
is often visible in the code.

A function starts with one check. A bug report arrives and someone adds a
second rule inside the first, because that is the smallest possible
change and it doesn't disturb what is already there. Six months and four
reports later there are five levels, each added by someone being careful.

That is worth knowing because it tells you what the fix is. The problem isn't
that a given developer wrote bad code. It's that adding a nested `if` is
always the locally cheapest change, and nothing pushes back. The remedy is to
treat depth as a review signal. When a change would add a fourth level,
that is the moment to restructure, not later.

The restructuring is nearly always one of three moves. Invert the refusals into
guard clauses. Combine rules that were only ever both-needed. Or extract
the inner block into a function with a name. This Resets the indentation and
gives the logic a label also.

## Writing the condition so it reads

Flattening helps only if the resulting rule is readable, and a flattened
rule can easily be worse than the nesting it replaced. Three habits keep
it honest.

**Avoid stacked negatives.** `if not (not active or banned)` is correct and
no one can test it at a glance. De Morgan's rules let you push the negation
inwards &mdash; `not (A or B)` is `not A and not B`. `not (A and B)` is
`not A or not B`. And the version with fewer negations is almost always
the one to keep. Better still, name the plus: `if is_eligible:`.

**Name the compound.** When a rule needs three clauses, assigning it to a
well-named variable on the line before turns the `if` into a sentence.
`can_borrow = user.active and not user.fines and book.available` followed by
`if can_borrow:` reads as intent, and the name shows what the combination
*means* rather than only what it checks.

**Keep checks in a natural order.** `if 0 <= n < 100` reads as a range and
chains right in Python. Here Most languages would need two checks and
an `and`. Writing `if n >= 0 and n < 100` says the same thing with more to
parse.

The underlying test is whether a reader can say what the rule means
without testing it. A staircase of simple rules is at times easier to
read than one flat rule that needs bookkeeping, and when that is true,
the staircase is the right answer.

## Every branch is a case to test

Nesting has a cost that is invisible while writing and obvious while testing:
the number of paths times.

Two nested rules give four combinations. Three give eight. A function with
four levels has sixteen paths through it, and the tests either cover all of
them or leave some untried. And the ones left untried are, by
build, the unusual combinations where the bugs are.

Guard clauses don't drop the combinations. But They change what a test has
to do. Each guard is a single rule with a single outcome, testable on its
own by passing one bad value and checking one message. The final line is the
case where all passed. The tests read as a list matching the guards, and
a new rule adds one test rather than doubling the table.

This is the hands-on arg for flattening, and it's stronger than the
aesthetic one. A shape that makes each rule on its own testable is a shape
where a change to one rule can't silently affect another &mdash; which is
just the property a staircase doesn't have, because each inner branch sits
inside the assumptions of each outer one.

## Extracting the inner block

The third remedy, after mixing and inverting, is to give the inner block a
name. It's the one people reach for last and it's often the best.

When a if-based is deep because the innermost part is doing real work, the
depth is telling you that two jobs are in one function: deciding, and doing.
Moving the inner block into its own function leaves an outer function that
reads as a sequence of choices ending in a call. An inner one that starts
at the left margin with its own name showing what it's for.

The mechanical gain is the indentation reset. The real gain is the name.
A block that was three levels deep and untagged turns a thing with a
title, which forces you to say what it does &mdash; and at times reveals
that you can't, because it was doing two things.

This is also the move that makes the guard-clause style available where it was
not. Guards need `return`, and a block buried in a loop inside a function has
nowhere to return to. Extract it, and the guards become possible inside the new
function.

## Questions people ask

<strong>Is there a limit to how deep nesting can go?</strong> Python allows
about twenty levels before the parser complains. This Is far past the point
where anyone can read it.

<strong>Does flattening change speed?</strong> Not usefully. Both
forms test the same rules in the same order.

<strong>Should I use `elif` or a nested `if`?</strong> `elif` when the
rules are options to each other, nesting when the second question
only makes sense given the first.

<strong>What about `match`?</strong> When the branching is on the shape or
value of one object, `match` often expresses it more right than either
nesting or an `elif` chain.

<strong>Can guard clauses be used outside a function?</strong> `continue` plays
the same role inside a loop, and it's under-used for just this.

<strong>Is an early `return` bad practice?</strong> The single-exit rule comes
from languages with manual cleanup. In Python, early returns make guard clauses
possible and are standard style.

<strong>How do I handle "at least one of these must be true"?</strong> `or`, or
`any()` over a list of rules when there are more than two or three.

<strong>Does an early return make a function harder to debug?</strong> No. A
breakpoint on each guard is as easy as one at the top, and the stack is
shallower when it fires.

<strong>What about rules that are costly to test?</strong> Order
them cheapest first. Short-circuiting means an costly check is skipped
when a cheaper one has already decided the answer.

<strong>Is a dict lookup ever a swap for the whole thing?</strong>
Yes, when each branch is checking one value against a constant. That is the
dispatch table from the dict methods page.

## Recap in one screen

- If the inner `if` is the entire body of the outer one, the two rules are
  an `and`.
- Refusals belong at the top as guard clauses. The main path stays at the
  left margin and each rule sits beside its own message.
- Genuine nesting is when the second question only makes sense given the first
  &mdash; and short-circuiting makes the order load-bearing.
- `elif` is one choice with a few outcomes. Reaching for nesting there
  turns a flat choice into a staircase.
- Three levels is a review signal: combine, invert, or extract a function.
""")


extend("args_and_kwargs", """
## Keyword-only and positional-only, and why they exist

The stars do a second job besides collecting: they mark boundaries in a
signature. Two markers control how callers are allowed to pass args.

A bare `*` makes all after it keyword-only:

```python
def connect(host, *, timeout=30, retries=3):
    return host, timeout, retries


print(connect("db", timeout=5))
try:
    connect("db", 5)
except TypeError as e:
    print("TypeError:", e)
```

```
('db', 5, 3)
TypeError: connect() takes 1 positional argument but 2 were given
```

The reason to want this is readability at the call site. `connect("db", 5, 2)`
tells a reader nothing about what 5 and 2 mean, and it silently changes meaning
if the param order is ever edited. Forcing the names makes the call
self-documenting and makes reordering the params a safe change.

A `/` does the opposite, marking all before it spot-based-only:

```python
def distance(x, y, /):
    return abs(x - y)
```

Now `distance(3, 5)` works and `distance(x=3, y=5)` doesn't. This is rarer,
and the reason is the mirror image: it keeps the param *names* out of the
API, so they can be renamed later without breaking callers. Most builtins are
spot-based-only for just that reason. This Is why `len(obj=x)` fails.

The rule of thumb: make a param keyword-only when its meaning isn't
obvious from the call site. This Means flags, options and
any of it numeric that isn't the main subject.

## What the stars cost you

`*args, **kwargs` accepts all, and the price is paid by each reader and
each tool afterwards.

The signature stops documenting any of it. `def process(*args, **kwargs)` tells
the next person nothing about what to pass. The only way to find out is to
read the body &mdash; and then the body of what it forwards to.

Editors and type checkers lose their grip. Autocompletion has nothing to
suggest, and a type checker can't verify a call it can't see the shape of.
For a codebase using type hints, a star signature is a hole in the coverage
that passes to each caller.

Errors move. A misspelled keyword arg would most times raise
`TypeError: unexpected keyword arg 'timeuot'` at the call, naming the
mistake. Absorbed into `**kwargs` it turns a missing key later, or &mdash;
worse &mdash; a default silently used instead of the value you passed, which
makes wrong output and no error at all.

None of that is an arg against the feature. It's an arg about where
to use it. Wrappers and subclass forwarding need it and pay none of the cost,
because there's no real signature to state. A function people call
right should name its params.

## Unpacking in the other direction

The two stars appear in three places and mean the same thing in all of them,
which is easier to hold on to than three separate rules.

In a **meaning** they collect: `def f(*args)` gathers loose spot-based
args into a tuple.

At a **call site** they spread: `f(*items)` hands each item over as a separate
arg.

In a **literal** they merge: `[*a, *b]` builds one list from two, and
`{**a, **b}` builds one dict from two, with later keys winning.

The last is worth dwelling on because it has quietly become the standard way to
combine collections:

```python
defaults = {"colour": "red", "size": 1}
overrides = {"size": 3}

print({**defaults, **overrides})
print([*"ab", *"cd"])
```

```
{'colour': 'red', 'size': 3}
['a', 'b', 'c', 'd']
```

Both build a new object and leave the originals alone. This Is the difference
from `update` and `extend`. And in set the star runs backwards again:
`first, *rest = items` collects rather than spreads. The star is on the
receiving side.

## A decorator, concretely

The pass-through pattern exists mainly so that decorators can be written, and
seeing one whole makes the pieces click:

```python
import functools

def announce(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("calling", func.__name__, "with", args, kwargs)
        result = func(*args, **kwargs)
        print("->", result)
        return result
    return wrapper


@announce
def add(a, b=0):
    return a + b


print(add(2, b=3))
print(add.__name__)
```

```
calling add with (2,) {'b': 3}
-> 5
5
add
```

Four things are happening. `announce` takes a function and returns a
swap. `wrapper` accepts any of it with `*args, **kwargs`, so it can stand
in front of any function at all. The forwarding call `func(*args, **kwargs)`
spreads them back out, so `add` receives just what the caller wrote. And
`@announce` above `def add` is shorthand for `add = announce(add)`.

`functools.wraps` is the part people leave out and then miss. Without it,
`add.__name__` prints `wrapper`, the docstring is gone, and each traceback
through the decorated function names the wrapper instead of the function. It
copies the spotting fields across, and it's one line.

Note how the args arrive: `2` in `args` and `b=3` in `kwargs`, just as
the caller passed them. The wrapper doesn't know or need to know that `add`
has a param called `b`.

## Asking a function what it accepts

When you do need to know the signature. Validating a plugin, building a
command-line interface, writing a framework &mdash; `inspect` answers it rather
than parsing the source:

`inspect.signature(func)` returns an object listing the params, their
defaults, their kinds (spot-based, keyword-only, `*args`, `**kwargs`) and any
annotations. `sig.bind(*args, **kwargs)` matches a proposed call against it and
raises the same `TypeError` the real call would. This Is how you check
args before doing costly work.

This is also how a decorator can be smarter than pure forwarding. A caching
decorator that wants a stable key needs to know that `f(1)` and `f(a=1)` are
the same call. `sig.bind` plus `apply_defaults` norms both to the same
thing, which no amount of inspecting `args` and `kwargs` right will do.

## The star in assignment

The same star appears in set, and it's worth connecting to the rest
rather than learning apart.

`first, *rest = items` binds the first item and collects all else into a
list. `*most, last = items` does the mirror image. `a, *middle, b = items` takes
both ends and collects what is between them. In each case the starred name gets
a list &mdash; always a list, even when the right-hand side was a tuple or a
string.

This is the collecting sense of the star, the same as in a meaning: the
star marks the name that absorbs but many items are left over. The
spreading sense is what you get on the other side of the equals sign, in a call
or a literal.

Only one star is allowed per set, for the obvious reason that two would
make the split ambiguous. And the non-starred names are still needed: unpacking
`a, *rest = []` raises. There's nothing for `a`, while `*rest, = []`
succeeds and gives an empty list.

## Questions people ask

<strong>Do the names `args` and `kwargs` matter?</strong> No, the stars carry
the meaning. The names are a strong rule -purpose wrappers and
worth replacing with a thing descriptive elsewhere.

<strong>Can I have `*args` without `**kwargs`?</strong> Yes, and the reverse.
They're free.

<strong>What order do they go in?</strong> Named params, then `*args`, then
keyword-only params, then `**kwargs`.

<strong>Is `**kwargs` sorted?</strong> Yes, it's a normal dict and
keeps the order the caller used.

<strong>Can I pass a list where `*args` is expected?</strong> Only with a star:
`f(*items)`. Without it you pass the list as a single arg.

<strong>Why does `f(**d)` fail with "keywords must be strings"?</strong>
Because a dict with non-string keys can't be turned into keyword
args.

<strong>How do I forward all including the function's own new
option?</strong> Take it as keyword-only, and forward `*args, **kwargs`
unchanged: the new option is bound by name and never reaches the wrapped call.

## Recap in one screen

- One star collects spot-based args into a tuple. Two collect keyword
  args into a dict.
- The same stars at a call site spread a collection back into args, and in
  a literal they merge collections.
- A bare `*` in a signature makes what follows keyword-only. A `/` makes what
  precedes it spot-based-only.
- The pass-through `f(*args, **kwargs)` is what makes decorators and wrappers
  possible without knowing any signature.
- A star signature costs docs, tooling and clear errors &mdash; use it
  where there's no real signature to state, not to avoid writing one.
""")


extend("type_conversion", """
## What each constructor actually accepts

The type names double as conversions. Each has its own idea of what it will
take. Seeing them side by side drops most of the surprises:

```python
print(int("  42  "), int("1_000"), int("ff", 16))
print(float("1e3"), float("  .5 "))
print(list("abc"), list({"a": 1}), tuple([1, 2]))
print(str([1, 2]), str(None))
```

```
42 1000 255
1000.0 0.5
['a', 'b', 'c'] ['a'] (1, 2)
[1, 2] None
```

`int` handles nearby whitespace and the underscores Python allows in
numeric literals, and takes a base as a second arg &mdash; which is how
you read hexadecimal, binary and octal from text without writing a parser.

`list` on a dict gives its **keys**, not its items, which catches people
who expected pairs. `list` on a string gives characters, which is at times
what you want and more often a sign that `split` was meant.

`str` never fails. each object has a string form, so `str(x)` always returns
a thing &mdash; which is convenient and means a bug can travel a long way
disguised as text. `str(None)` is the string `"None"`, and a `"None"` written
into a CSV column is a classic way to lose the gap between missing and
present.

## Parsing a boolean from text

There's no conversion for this, and reaching for `bool` is the mistake
everyone makes once:

```python
print(bool("False"), bool("0"), bool(""))
```

```
True True False
```

`bool` on a string asks only whether the string is empty. `"False"` and `"0"`
are both non-empty, so both are `True`. This Is just backwards from what
the text says.

Reading a boolean out of a config file, an environment variable or a form means
deciding what counts, and then saying so:

```python
TRUE = {"1", "true", "yes", "on"}

def as_bool(text):
    return str(text).strip().lower() in TRUE
```

That is a policy rather than a conversion. This Is why the language doesn't
provide one &mdash; different formats disagree about whether `"y"`, `"on"` or
`"enabled"` should count, and about what an unrecognised value means. Deciding
by name is the point.

## Where conversion loses information

Some conversions are exact and some throw info away, and knowing which
is which blocks a family of quiet bugs.

`int(3.9)` discards the fractional part. `int` from a large float loses
precision before it even starts, because the float never held the exact value.
`float(some_big_int)` is worse: ints in Python are unbounded, floats are
not, so a enough large int converts to a float that is merely nearby,
and converting back doesn't return the first.

`str` of a float is lossy in the other direction once, though modern
Python prints the shortest string that round-trips just, so
`float(str(x)) == x` holds.

`set(items)` discards duplicates and order. `dict(pairs)` discards all but the
last value for each repeated key. Neither reports what it dropped, and both are
at times used on purpose for just that effect. Which is why the
loss has to be intentional rather than found.

The habit worth forming: when a conversion narrows. Float to int, list
to set, any of it to `str`. Ask what happens to what doesn't fit. When
it widens, as int to float or str to list, there's often nothing to worry
about.

## The numeric types beyond int and float

`int` and `float` cover most work, and two more exist for cases where floats
give the wrong answer.

`decimal.Decimal` shows numbers in base ten, so `Decimal("0.1") * 3` is
just `Decimal("0.3")` rather than a hair off. It's the right type for
money, invoices, tax and any of it where a result will be checked against a
figure a person found. Build it from a **string**, not a float:
`Decimal(0.1)` faithfully captures the float's error. This Defeats the point.

`fractions.Fraction` holds an exact ratio. So `Fraction(1, 3) * 3` is just
1. It's the right type for exact rational math, and it's slower and
grows in memory as denominators times. So It belongs in maths rather
than in stored data.

Both convert to and from the plain types, and both interoperate with `int`
&mdash; but mixing either with `float` in one formula converts back to
`float` and reintroduces the error you were avoiding. This Is the trap. If a
math is meant to be exact, each value in it has to be the exact type.

`complex` also exists, written `3+4j`, and is truly used in signal
processing and geometry. It's worth knowing mainly so that `j` in a numeric
literal isn't a mystery.

## Convert once, at the edge

The thread running through this page is that conversion is a choice, and the
handy discipline is to make each choice just once. Here The data enters
the program.

A value read from a file, a form, an environment variable or an API is text. If
it's converted at the point of use, each use site repeats the conversion,
each use site has to handle the failure, and the sites will eventually
disagree &mdash; one treats an empty string as zero, another as an error, a
third crashes. The type of the value turns a thing a reader has to infer
from context.

Converting at the boundary means one place decides what a bad value means, and
all after that point works with a real `int`, `date` or `Decimal`. The
error, when it comes, names the input and the field rather than surfacing as a
`TypeError` deep in a math.

This is the same arg as validating nested data at the boundary, and the
same arg for keyword-only params: push the ambiguity to one place, as
early as possible, and let all downstream lean on what it was given.

## The one conversion Python does silently

All on this page says Python refuses to convert without being asked,
which is true with one systematic exception: numeric promotion.

Mixing an `int` and a `float` in an formula converts the `int` to a `float`
first, so `1 + 2.0` gives `3.0` and `1 / 2` gives `0.5` rather than `0`. Mixing
a `bool` with a number treats `True` as 1 and `False` as 0, which is why
`sum([True, False, True])` is 2 &mdash; at times handy for counting how
many rules held, and at times a surprise.

The rule is that Python converts within the numeric tower only, and only in the
widening direction, where nothing is lost. `int` to `float` is allowed. `str`
to any of it isn't. That is why `True + 1` works and `"1" + 1` doesn't, which
looks inconsistent until you see the boundary it's drawing.

The one place the widening does lose a thing is very large ints, where
converting to `float` loses precision though the conversion is nominally
widening. It's the exception to the exception, and it only bites at magnitudes
most programs never reach.

## Questions people ask

<strong>Why does `int("3.9")` fail when `int(3.9)` works?</strong> The string is
not an int literal, so it refuses rather than choosing a rounding
direction. Use `int(float("3.9"))` when you mean truncation.

<strong>How do I convert a list of strings to numbers?</strong>
`[int(x) for x in items]`, or `list(map(int, items))`.

<strong>What is the difference between `str` and `repr`?</strong> `str` is for
people, `repr` is for programmers and aims to be unambiguous. `print` uses
`str`. The interactive prompt and containers use `repr`.

<strong>Why is `0.1 + 0.2` not `0.3`?</strong> Binary floating point can't
represent those decimals just. Use `math.isclose` to compare, or
`decimal.Decimal` for money.

<strong>Does `int()` round or truncate?</strong> Truncates toward zero, so
`int(-3.9)` is `-3`. `round` is the one that rounds.

<strong>How do I convert between a string and bytes?</strong>
`text.encode("utf-8")` and `data.decode("utf-8")`. Both need an encoding, and
guessing is where mojibake comes from.

<strong>Can I convert a dict to a list of pairs?</strong>
`list(d.items())`. Plain `list(d)` gives the keys.

<strong>Should I annotate types instead of converting?</strong> They're
different jobs. An annotation docs and is checked by tools. It doesn't
convert any of it at runtime.

<strong>How do I convert a string to a date?</strong>
`datetime.strptime(text, fmt)` with an clear format, or
`datetime.fromisoformat` for ISO-8601 text. Neither guesses.

<strong>What does `int()` with no arg give?</strong> Zero. each numeric
constructor called with nothing returns its zero value, which is at times
handy as a default factory.

## Recap in one screen

- Each type's name is its conversion. There's nothing extra to store.
- Input is always text, and Python will never convert it for you &mdash; that
  refusal is what makes `"3" + 4` an error rather than a silent bug.
- `int` from a string is strict, `int` from a float truncates toward zero, and
  `round` rounds halves to even.
- `bool` on a string only asks whether it's empty. Parsing a boolean from
  text needs an clear mapping.
- Narrowing conversions lose info silently &mdash; duplicates, order,
  precision, the difference between missing and `"None"`.
""")


extend("conditional_expressions", """
## Seeing the or trap fail

The `or` shorthand and the clear if-based look the same until a
falsy value goes through them:

```python
def with_or(value):
    return value or "default"

def with_cond(value):
    return value if value is not None else "default"

for v in ["set", "", 0, None, False, []]:
    print(repr(v), "->", repr(with_or(v)), repr(with_cond(v)))
```

```
'set' -> 'set' 'set'
'' -> 'default' ''
0 -> 'default' 0
None -> 'default' 'default'
False -> 'default' False
[] -> 'default' []
```

They agree on `"set"` and on `None`, and disagree on all else. `or`
replaces the empty string, the zero, the `False` and the empty list &mdash;
each one of which might be a legitimate value somebody on purpose supplied.

The cases where this matters are plain rather than exotic. A quantity of
zero, an empty search box, a `False` flag the user really turned off, an
empty list meaning "no tags". In each, `or` silently substitutes a default over
the top of a real answer, and the bug reads as "my setting doesn't take
effect".

`or` is still fine when each falsy value truly means "absent" &mdash;
which is most often true for strings that are either a name or nothing. The
discipline is to notice that you're making that claim rather than reaching for
the shorter form by reflex.

## It is an expression, and that is the whole distinction

All on this page follows from one fact: `x if c else y` makes a
value, and `if c:` doesn't.

An formula can go wherever a value can. That is why it works inside an
f-string, as a function arg, as a dict value, inside a comprehension
and on the right of an set. A statement can go in none of those places,
which is why the if-based formula isn't a shorter `if` &mdash; it's the
only form that fits where a value is needed.

The converse is equally firm. An formula must give a value on each path,
which is why the `else` is compulsory and why there's no one-armed version. It
also can't hold statements: no set, no `raise`, no `return` inside
it. If the branches need to *do* a thing rather than *be* a thing, the
statement form is the only option.

This also shows the reading order. `x if c else y` puts the common case
first because the whole thing is a value with a qualification attached, in the
way English does &mdash; "the total, if there's one, or else zero". A
statement starts with the question because it's about control flow, and
control flow starts with a choice.

## The walrus, and the other one-liner

A near neighbour worth distinguishing, because both compress a few lines into
one and they do different things.

`:=`, the walrus operator, assigns *inside* an formula. So A value can be
found and tested in one place:
`if (n := len(items)) > 10:` binds `n` and checks it, and `n` is then
available in the body without a second call. In a comprehension it's the way
to avoid finding a thing twice:
`[y for x in data if (y := f(x)) isn't None]` calls `f` once per item rather
than once in the filter and again in the formula.

The gap from a if-based formula is clean. The walrus is about
*naming* a value you're already finding. The if-based formula is about
*choosing* between two values. They combine happily and neither replaces the
other.

Both share a caution: they earn their place when they drop a genuine
repetition or make a line fit where a statement can't. Used to compress code
that was already clear, both make a reader stop, and neither is worth that.

## Where you will actually meet it

Four places account for nearly each if-based formula in real code, and
all four share the property that a statement couldn't go there.

**Inside an f-string.** `f"{count} item{'s' if count != 1 else ''}"` handles the
plural without building the string in two steps. This is the single most common
use, and it's worth having in your fingers.

**As a default that depends on a thing.**
`timeout=timeout if timeout isn't None else DEFAULT` in an arg list, or
as a dict value in a literal being made.

**Inside a comprehension.** Choosing what each item turns, not
filtering which items appear &mdash; the gap covered elsewhere in the
track.

**As a `key=` arg.** `sorted(rows, key=lambda r: r.score if r.score isn't
None else -1)` puts missing values at one end without filtering them out first.

What none of these have in common with an `if` statement is that they're
making a value in the middle of an formula that is already underway. That
is the whole niche, and reaching for the form outside it. On a line of
its own, assigning to a variable, when a plain `if` would do &mdash; is where
it starts costing readability rather than saving it.

## When the statement is the better tool

The if-based formula isn't a compressed `if`, and treating it as one
makes the code that gives it a bad name. Three signals that the statement
form is what you want.

**The branches do a thing rather than give a thing.** Logging, raising,
assigning to more than one name, calling for a side effect. None of these fit
in an formula, and contorting them to fit. A tuple of calls, an `or`
chain with a function that raises. Makes code that is clever and
unreadable in the same stroke.

**There are more than two outcomes.** A chain of `else`s pushes the default to
the far end of the line and makes inserting a case an edit in the middle of a
string of keywords. A sequence of `if` statements, or a table of thresholds, is
both clearer and easier to change.

**Either branch is long.** Once the line wraps, the reader has to reassemble it
across two lines to find where the rule sits. A four-line `if` costs three
lines no one has ever regretted.

The version of the rule worth keeping: use the formula when you need a
value *here*, in the middle of a thing else. Use the statement when you're
deciding what the program does next.

## Questions people ask

<strong>Why is the rule in the middle?</strong> Because the formula is
a value with a qualification, and putting the common case first makes it read
as a sentence.

<strong>Can I leave out the `else`?</strong> No. An formula must give a
value on each path.

<strong>Can I nest them?</strong> Legally yes, readably no past one level. A
sequence of `if` statements or a table of bands is clearer.

<strong>Is it slower than an `if` statement?</strong> No, they compile to
the same bytecode.

<strong>Can I use it on the left of an set?</strong> No.
`(a if c else b) = 1` isn't valid. Only names and subscripts can be assigned
to.

<strong>What is Python's version of the ternary `?:`?</strong> This is it.
Python spells it with words rather than punctuation, on purpose.

<strong>Can I put a `raise` in one?</strong> No, `raise` is a statement.
There's an idiom using `or` with a function that raises, and it's worse than
writing the `if`.

<strong>Does it short-circuit?</strong> Yes. Only the branch that is chosen is
tested, so the other side can safely be a thing that would fail.

<strong>Can I use it with `and`/`or` in the rule?</strong> Yes, and
brackets are worth adding when you do. The precedence is correct but not
obvious to a reader.

<strong>Does it work in a lambda?</strong> Yes, and it's one of the few ways
to get a choice into one, since a lambda body must be a single formula.

<strong>Is there a null-coalescing operator like `??`?</strong> No. The
clear `x if x isn't None else y` is Python's version, and its verbosity is
deliberate &mdash; it makes you say which falsy values you meant.

<strong>Can the two branches return different types?</strong> Yes, nothing
stops you. Whether the caller can cope with either is a separate question, and
often the answer is that it shouldn't have to.

## Recap in one screen

- `value_if_true if rule else value_if_false` &mdash; the value first, the
  rule second.
- It's an formula, so it fits inside f-strings, comprehensions and arg
  lists where a statement can't.
- The `else` is compulsory, because an formula must always give
  a thing.
- `x or default` replaces each falsy value, not just `None`. Use the clear
  `isn't None` form when zero or empty is legitimate.
- One rule and short values on one line. Past that, write the statement or
  put the bands in a list.
""")


extend("match_and_case", """
## Destructuring in one step

The arg for `match` isn't tidiness, it's that the pattern checks the
shape and pulls the pieces out in the same breath:

```python
events = [
    {"type": "click", "x": 10, "y": 20},
    {"type": "key", "key": "a"},
    {"type": "scroll", "amount": 3, "extra": "ignored"},
    "not a dict",
]

for e in events:
    match e:
        case {"type": "click", "x": x, "y": y}:
            print("click at", x, y)
        case {"type": "key", "key": k}:
            print("key", k)
        case {"type": t}:
            print("other event:", t)
        case _:
            print("unrecognised:", e)
```

```
click at 10 20
key a
other event: scroll
unrecognised: not a dict
```

Three things are worth noticing. The `scroll` event carries an `extra` key that
no pattern mentions, and it still matches. Mapping patterns check that
the named keys are *present*, not that they're the only ones, which is what
makes them usable against real payloads.

The string falls through to `case _`, because a mapping pattern doesn't match
a non-mapping. Written with `if`, that safety would have been an clear
`isinstance(e, dict)` that somebody has to note.

And `x`, `y`, `k` and `t` are bound by the match itself. The equal
`if`-chain needs a key check and a lookup for each, in the right order, with
the lookups repeating what the checks just established.

## The bare name that swallows everything

A bare name in a pattern doesn't compare against that name. It's a **capture
pattern**: it matches any of it at all and binds the name to what it caught.

Python protects you from the obvious form of the mistake. Writing a capture
before other cases is a compile-time error, and the message is unusually
direct:

```
SyntaxError: name capture 'OK' makes remaining patterns unreachable
```

What it can't protect you from is the same mistake in the last spot, where
there are no unreachable patterns to complain about:

```python
OK = 200

for status in [200, 404, 500]:
    match status:
        case 404:
            print(status, "not found")
        case OK:
            print(status, "matched OK")

print("OK is now", OK)
```

```
200 matched OK
404 not found
500 matched OK
OK is now 500
```

500 "matched OK", because `case OK:` matched all the earlier case did
not. And the constant is gone. `OK` was rebound each time the capture
fired, so after the loop it holds 500.

The fix is a dotted name. This Is a **value pattern** and does compare:

```python
class Status:
    OK = 200

for status in [200, 404, 500]:
    match status:
        case 404:
            print(status, "not found")
        case Status.OK:
            print(status, "matched OK")
        case _:
            print(status, "unhandled")
```

```
200 matched OK
404 not found
500 unhandled
```

This is why enums pair so on its own with `match`: `case Colour.RED` is
unambiguous, and an enum gives you the dotted form for nothing. Literals work
too. It's only bare names that capture.

## Not exhaustive, and what that means

Languages that popularised pattern matching often check that each possible
case is handled, and refuse to compile if one is missing. Python doesn't.

If no case matches and there's no `case _`, the `match` statement simply does
nothing and run continues on the next line. No exception, no warning. A
value that falls through leaves no trace, and the symptom appears later as a
result that was never found.

That makes `case _` more key than a default clause often is. Ending
with one that raises &mdash; or at min logs the unhandled value &mdash;
converts a silent no-op into a thing you can find:

```python
        case _:
            raise ValueError(f"unhandled event: {event!r}")
```

The same applies inside a function returning a value: a `match` where each
case returns will return `None` for an unmatched value, which then travels
a place else before failing. Making the fallthrough clear is the habit
worth forming from the first `match` you write.

## Guards, classes and the shapes worth knowing

Beyond literals and mappings, three pattern kinds cover most real use.

**Sequence patterns** match lists and tuples structurally. `case [x]` matches a
one-item sequence, `case [first, *rest]` matches any non-empty one and splits
it, `case []` matches empty. They don't match strings, which is deliberate
&mdash; a string is a sequence of characters and matching it as one is almost
never what anybody means.

**Class patterns** match an instance and can read fields:
`case Point(x=0, y=y)` matches a `Point` whose `x` is zero and binds its `y`.
Dataclasses and named tuples support the spot-based form, `case Point(0, y)`,
via `__match_args__`.

**Guards** attach a rule to a pattern with `if`:
`case [x, y] if x == y` matches a two-item sequence whose items are equal. The
pattern narrows the shape, the guard narrows the values, and a guard that fails
lets the next case try. It doesn't abandon the whole `match`.

The combination is what makes the feature earn its keyword. "A two-element list
of ints where the first is minus" is one line, and the `if`-chain
equal is a length check, two `isinstance` calls and a check in a
exact order.

## A worked example: a small command parser

each pattern kind in one function, doing the job `match` was added for:

```python
def run(command):
    match command.split():
        case ["quit"] | ["exit"]:
            return "goodbye"
        case ["add", *items] if items:
            return f"adding {len(items)}: {', '.join(items)}"
        case ["get", key]:
            return f"looking up {key}"
        case [verb, *_]:
            return f"unknown command: {verb}"
        case _:
            return "say something"


for line in ["quit", "add pen pad", "get colour", "add", "spin around", ""]:
    print(f"{line!r:16} -> {run(line)}")
```

```
'quit'           -> goodbye
'add pen pad'    -> adding 2: pen, pad
'get colour'     -> looking up colour
'add'            -> unknown command: add
'spin around'    -> unknown command: spin
''               -> say something
```

Read the cases in order. The first uses `|` for options, both of which are
one-word sequences. The second matches `add` followed by any number of items
and binds them, with a guard rejecting the case where there are none &mdash;
which is why bare `"add"` falls through to the catch-all verb case rather than
reporting "adding 0". The third needs just two words, so `get` with two
args wouldn't match it.

The fourth is the notable one: `[verb, *_]` matches any non-empty list,
binds the first word and discards the rest with `_`. The last handles the empty
string, whose `split()` gives `[]`. This No sequence pattern with a needed
element can match.

Written as an `if`-chain, each of those turns a length check plus an index
plus a check, in an order that has to be right. Here the shape and the
extraction are the same formula, and a case that doesn't fit simply does
not match.

## Enums, the natural partner

The capture-pattern trap has a structural fix rather than a discipline one: use
an enum, and the problem can't arise.

An enum member is always reached through a dotted name &mdash; `Colour.RED`,
`Status.NOT_FOUND` &mdash; which makes each ref a value pattern by
build. There's no way to accidentally write the bare form, because the
bare form doesn't name any of it.

Two further gains follow. The set of valid values is written down in one
place, so a reader can see what the `match` is dispatching over without
gathering the cases. And because the members are objects rather than ints,
a typo is an `AttributeError` at the point of the mistake rather than a case
that silently never fires.

This is the shape most `match` statements in well-organised code take: an enum
or a set of classes defining the options, and a `match` that handles each
one and ends with a `case _` that raises. Between them, the two make the set of
cases clear and the missing case loud. Getting back most of what the
exhaustiveness checking of other languages gives, without the language doing
it for you.

## Questions people ask

<strong>Is there fall-through like C's switch?</strong> No. The first matching
case runs and the statement ends. No `break` is needed or allowed.

<strong>Can I match on types?</strong> Yes, with a class pattern: `case int():`
matches any int. Note the brackets. `case int:` without them is a
value pattern checking against the type object.

<strong>Does a mapping pattern need exact keys?</strong> No, extra keys are
allowed. Use `**rest` to capture them.

<strong>Can I bind the whole value and its parts?</strong> Yes, with
`as`: `case {"type": "click"} as event`.

<strong>Why does `case [x]` not match a string?</strong> Sequence patterns
on purpose exclude `str`, `bytes` and `bytearray`.

<strong>Is `match` a keyword now?</strong> It's a soft keyword, so existing
code using `match` as a variable name still works.

<strong>Should I convert my `if`-chains?</strong> Only where they're inspecting
shape. For checking one value against a few constants, the chain is fine and
runs on older Python.

<strong>Can a guard ref names bound by the pattern?</strong> Yes, and
that is the usual reason to write one. The pattern binds, then the guard
tests what it bound.

<strong>Is `match` faster than an `if`-chain?</strong> For literals they're
close. For structural patterns it's often faster than the equal
checks, and speed isn't the reason to choose it.

<strong>Can I match against a set of allowed values?</strong> Use `|` between
literals in one case, or a guard with `in` when the collection is built
elsewhere.

## Recap in one screen

- `match` tests patterns, not rules. The pattern checks shape and binds
  parts in one step.
- A bare name captures and matches all. Use a literal or a dotted
  name to compare against a constant.
- Mapping patterns allow extra keys. Sequence patterns never match strings.
- Nothing is exhaustive: an unmatched value falls through silently, so end with
  `case _` that raises or logs.
- Reach for it when inspecting the shape of data, and keep `if`/`elif` for a
  few literal checks. needs Python 3.10.
""")


extend("conditional_comprehensions", """
## Both forms, side by side

The difference is easiest to hold on to as a length:

```python
nums = [1, -2, 3, -4]

print([n for n in nums if n > 0])
print([n if n > 0 else 0 for n in nums])
print([n if n > 0 else 0 for n in nums if n % 2])
```

```
[1, 3]
[1, 0, 3, 0]
[1, 3]
```

The first is a filter: four in, two out. The second is a choice: four in, four
out, with the failures replaced rather than removed. The third has both, and
the reading order is the thing to fix in your head &mdash; the trailing filter
runs first, keeping the odd numbers, and only then does the leading if-based
run on what survived.

Written out as a loop, the order is obvious:

```python
result = []
for n in nums:
    if n % 2:                 # the trailing filter
        result.append(n if n > 0 else 0)
```

The comprehension writes the append formula first and the filter last, which
is the reverse of the order they execute in. That is the single fact that makes
mixed comprehensions hard to read, and it's why one filter and one
if-based is a sensible ceiling.

## Why the else is compulsory in one place and forbidden in the other

This looks like an inconsistency and is a direct consequence of what each `if`
is doing.

The `if` at the front is part of the **formula** that makes each item. An
formula must give a value on each path &mdash; there's nowhere for
"give nothing" to go, because the comprehension is going to append what
it tests to. So the `else` is needed, just as it's in a if-based
formula anywhere else.

The `if` at the end is a **filter clause**, part of the comprehension's
machinery rather than of the formula. It answers one question: does this
item continue to the formula, or not. There's no second branch for an
`else` to introduce, because "not kept" is already the option.

Trying the wrong one is worth doing once so the error is familiar.
`[n for n in nums if n > 0 else 0]` is a `SyntaxError`, and the message points
at the `else`. `[n if n > 0 for n in nums]` is also a `SyntaxError`, because
the formula is incomplete.

## Filtering to make the expression safe

The run order isn't trivia. It's what lets the filter protect the
formula:

```python
rows = [{"score": 50}, {"score": None}, {"score": 90}]

print([r["score"] * 2 for r in rows if r["score"] is not None])
```

```
[100, 180]
```

The `None` row never reaches the times. Swap the two clauses in your
head &mdash; formula first &mdash; and it would raise `TypeError` on the
second row.

This is the standard shape for data with gaps, and it's better than the
option it's often confused with. Writing
`[r["score"] * 2 if r["score"] isn't None else None for r in rows]` makes
an entry for each row, including a `None` in the middle of what is supposed to
be a list of numbers. This Pushes the problem to what consumes the result.

Deciding between them is deciding what a missing value means: filter when the
row shouldn't be in the output, choose when it should be present with a
substitute. Both are legitimate. Picking one by accident isn't.

## Several filters, and the nested case

Chained filters mean `and`:

```python
[n for n in nums if n > 0 if n % 2 == 0]
```

is the same to one filter with `and`. The chained form at times reads
better when the rules are unrelated tests. The mixed form is more
familiar. Neither is wrong.

Nesting is where care is needed. A trailing `if` attaches to the clause
it follows:

```python
[n for row in grid for n in row if n % 2]
```

The filter is after the inner `for`. So It filters cells. Move it up, to
`for row in grid if len(row) > 2 for n in row`, and it filters rows instead.
Both are legal and they mean fully different things, with no visual signal
beyond spot.

The clauses read in the same order as the equal nested loops, outermost
first. That is worth stating because the guess most people make is the
opposite, and the code will run either way while making the wrong answer.

## The same two positions, everywhere

Nothing on this page is exact to lists. Dict comprehensions, set
comprehensions and gen expressions all carry the same two `if` spots
with the same rules, and knowing that means learning it once.

```python
rows = [{"name": "ana", "score": 91}, {"name": "bo", "score": None}]

print({r["name"]: r["score"] for r in rows if r["score"] is not None})
print({r["name"] for r in rows if r["score"]})
print(sum(r["score"] for r in rows if r["score"] is not None))
```

```
{'ana': 91}
{'ana'}
91
```

The filter sits at the end in all three. A if-based formula, when used,
sits at the front &mdash; in the value slot for a dict, in the item slot for a
set or gen. In a dict comprehension it can appear in either the key or
the value, or both. This Is legal and almost always worse than a loop.

The gen formula case is worth calling out because the filter there's
doing a thing the others aren't: it decides which items are ever found at
all. In a list comprehension a filtered-out item costs a test. In a gen
feeding `sum` over a large file, the filter is what stops work from happening.

## When the filter is expensive

The trailing filter runs on each item, and the leading formula runs only on
survivors. That is often the fast way round, and at times it isn't.

If the test itself is costly. A lookup, a regular formula, a parse
&mdash; and the formula needs the same found value, the naive
comprehension does the work twice:

```python
[parse(line) for line in lines if parse(line) is not None]
```

`parse` runs twice for each line that lives. The walrus operator finds
it once and reuses it:

```python
[value for line in lines if (value := parse(line)) is not None]
```

The set happens in the filter, and the name is available to the
formula at the front &mdash; which reads oddly, since the formula is
written first, but follows right from the filter running first.

Before Python 3.8 the idiom was a nested comprehension:
`[v for v in (parse(l) for l in lines) if v isn't None]`, finding the values
in an inner gen and filtering the results. That still works and is
arguably clearer, since it separates the two steps rather than hiding an
set inside a rule.

## The rule, in one line

All on this page reduces to a sentence worth keeping: **the `if` at the
front chooses a value and needs an `else`. The `if` at the end chooses an item
and can't have one.**

If you can only note one consequence of that, make it the length. A
comprehension whose result must be the same length as the input needs the
leading form. One whose result may be shorter needs the trailing form. Asking
"how many items should come out" answers which `if` you want faster than
recalling the syntax rules does.

And when both appear, note they run in the opposite order to the one they
are written in. The filter decides what lives. The formula then decides
what each survivor turns. each confusing mixed comprehension is that
inversion catching someone out.

## Questions people ask

<strong>Which `if` runs first?</strong> The trailing filter, always &mdash;
though the if-based formula is written before it.

<strong>Can I use `else` with the trailing `if`?</strong> No, it's a syntax
error. There's no second branch for a filter.

<strong>Can I filter on the found value rather than the source?</strong> Not
right, without finding it twice. The walrus operator does it in one pass:
`[y for x in data if (y := f(x)) > 0]`.

<strong>Does this work in dict and set comprehensions?</strong> Yes, the same way.
The two spots and their rules are the same in all of them.

<strong>Are two filters slower than one `and`?</strong> No, they compile to the
same thing.

<strong>How many clauses is too many?</strong> One `for`, one filter, and
optionally one if-based formula. Past that, the loop is easier to read
and to change.

<strong>Can the filter ref the loop variable of an outer clause?</strong>
Yes. each clause can see the variables bound by the clauses to its left.

<strong>Can I put the filter before the `for`?</strong> No. The clause order is
fixed: formula, then `for`, then any `if`. The only `if` that comes first is
part of the formula.

<strong>Why does my comprehension raise on some items?</strong> Almost always
because the formula is running on items the filter should have removed
&mdash; or because the filter is testing a thing different from what the
formula uses.

<strong>Is there a way to skip an item from the formula?</strong> No. An
formula must give a thing. So Skipping is the filter's job. That
gap is the reason for the two spots.

<strong>Do comprehensions with filters build the list lazily?</strong> No, a
list comprehension builds the whole thing. Use a gen formula when the
filtering should happen on demand.

<strong>Can I filter on the index?</strong> Only by supplying one:
`[x for i, x in enumerate(items) if i % 2 == 0]`.

## Recap in one screen

- The trailing `if` filters and takes no `else`. The leading `if`/`else`
  chooses and needs one.
- Filter first, then the formula. The opposite of the written order.
- That sorting is what lets a filter guard the formula against `None` or a
  division by zero.
- Chained filters mean `and`. In a nested comprehension a filter attaches to
  the clause it follows.
- One `for`, one filter, one if-based: past that a loop reads better and
  changes more safely.
""")


extend("none_and_truthiness", """
## The find() trap, run

The classic case, with all three answers printed side by side:

```python
def find(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i
    return None


items = ["a", "b"]
for target in ["a", "b", "z"]:
    result = find(items, target)
    print(target, result,
          "not found" if not result else "found",
          "|", "not found" if result is None else "found")
```

```
a 0 not found | found
b 1 found | found
z None not found | not found
```

The middle column is the bug. `find` returned 0. The item *was* found,
at the first spot &mdash; and `not result` reported it as missing. The
right-hand column, testing `is None`, is correct for all three.

Notice which case fails: the first element. A test suite that searches for
a thing in the middle of a list passes. The bug waits for real data where
the match happens to be first. That is the trait shape of truthiness
bugs &mdash; they're correct for most inputs. This Is why they live
review.

## Giving your own objects a truth value

Truthiness isn't a fixed list. Python asks the object, and any class can
answer.

When you write `if obj:`, Python calls `__bool__` if the class defines one. If
it doesn't, it falls back to `__len__` and treats zero as false. If neither
exists, the object is always truthy. Which is why an instance of a plain
class you wrote is true even when it holds nothing.

```python
class Basket:
    def __init__(self, items):
        self.items = items

    def __len__(self):
        return len(self.items)


print(bool(Basket([])), len(Basket([])), bool(Basket([1])))
```

```
False 0 True
```

Defining `__len__` gave the class a sensible truth value for free, which is why
it's the usual choice for any of it container-like. `__bool__` is for objects
that have a notion of empty without a length. A link that is open
or closed, a result that succeeded or failed.

The caution is that this is just the mechanism that makes truthiness
ambiguous. An object that is falsy when empty can't be distinguished from
`None` by `if obj:`, so any code that treats "absent" and "empty" differently
still has to use `is None`. Some libraries make this sharp: a pandas DataFrame
raises rather than guessing when you put it in a rule, on the grounds that
"empty" and "all values false" are both plausible readings.

## When None itself is a valid value

At times `None` is a legitimate value in the data, and then it can't also
mean "absent". The standard answer is a sentinel: a unique object that means
nothing else.

```python
MISSING = object()

def get(mapping, key, default=MISSING):
    if key in mapping:
        return mapping[key]
    if default is MISSING:
        raise KeyError(key)
    return default
```

`object()` creates a thing that is equal only to itself, so `default is
MISSING` is true just when the caller didn't pass a default. Now
`get(d, "k", None)` and `get(d, "k")` mean different things &mdash; the first
supplies `None` as the default, the second asks for an error &mdash; which is
hopeless if `None` is itself the sentinel.

This isn't a common need, and it's worth recognising because the standard
library uses it. `dict.pop` sets apart "no default given" from "default of
`None`" in just this way, and a few libraries expose their sentinel by
name so callers can test against it.

The plainer version of the same idea is a module-level constant with a name
that says what it means. This Reads better in a traceback than
`<object object at 0x...>`.

## Where None comes from

`None` rarely gets written into your data on purpose. It arrives, and knowing
the sources makes it predictable rather than mysterious.

**A function that didn't return.** Any function reaching its end without a
`return` returns `None`, and so does a bare `return`. This is the biggest
source: a function with a `return` inside an `if` and nothing after it returns
`None` for each input that misses the branch, silently.

**An in-place method.** `sort`, `reverse`, `append`, `update` and their
relatives all return `None` on purpose. So `x = x.sort()` replaces a list with
nothing.

**A lookup with a default.** `d.get(k)` returns `None` when the key is absent,
as do `os.environ.get`, `re.match` when the pattern doesn't match, and a great
many library functions that mean "nothing here".

**A DB or JSON null.** `null` in JSON turns `None`, and a nullable
column comes back the same way. This is the one where `None` is truly part
of the data rather than a signal, and where the "absent versus empty"
gap matters most.

**An uninitialised field.** A class that sets `self.result = None` in
`__init__` and fills it in later hands out `None` to any of it that asks too
early.

The pattern across all five is that `None` marks the lack of a value rather
than being one. When it turns up a place unexpected, the productive question
is which of these made it. And the answer is often the first.

## Saying "might be None" out loud

The failure mode of `None` is that it travels. A function returns it, the
caller passes it on, and the `AttributeError: 'NoneType' object has no
field ...` appears three functions away from the one that made it.

Type hints are the cheapest defence, because they make the possibility part of
the signature:

```python
def find_user(name: str) -> User | None:
    ...
```

That says, to a reader and to a type checker, that each caller has to handle
the `None` case. A checker will flag `find_user(x).email` as an error before it
runs. On Python before 3.10 the spelling is `Optional[User]` from `typing`,
which means just the same thing.

The hint changes nothing at runtime, and that is fine. The value is in
making the contract clear. A function whose return type is `User` and which
at times returns `None` is lying, and the fix is either to make the hint
honest or to raise instead of returning nothing.

Raising is often the better answer. If a caller has no sensible response to
"not found", returning `None` just moves the crash a place less helpful.
Returning `None` is right when lack is plain and the caller will branch
on it. Raising is right when lack means a thing has gone wrong.

## Questions people ask

<strong>Is `if x:` faster than `if len(x) > 0:`?</strong> Marginally, and
that isn't the reason to prefer it. It reads better and works on any of it.

<strong>Why is `"False"` true?</strong> Because it's a non-empty string.
Truthiness asks about emptiness, not about meaning.

<strong>Should I write `if x == None`?</strong> No. `is None` is the
rule, is faster, and can't be overridden by a class.

<strong>What is falsy that people forget?</strong> `0.0`, `Decimal(0)`,
`range(0)`, and `datetime.time(0, 0)` in older Python &mdash; midnight was
falsy until 3.5, which caused real bugs.

<strong>How do I test "not None and not empty"?</strong> `if x:` covers both
when `None` and empty should be treated alike. When they shouldn't, say both:
`if x isn't None and len(x):`.

<strong>Does `if not x` work on a gen?</strong> Not usefully. A gen
is always truthy, even if it will give nothing.

<strong>Why does `numpy` raise on `if array:`?</strong> Because an array with
a few elements has no single truth value, and guessing would be wrong half
the time.

<strong>Is `None` the same as `null` in other languages?</strong> It plays the
same role. The difference is that Python's is a real object with a type, so
`type(None)` works and `None.__class__` is `NoneType`.

<strong>Can I subclass `NoneType` or make another `None`?</strong> No.
`NoneType` can't be instantiated. This Is what ensures `is None` is
solid.

<strong>Why does `print(f())` show `None` for my function?</strong> Because the
function returned nothing. often a `return` is missing on one branch.

<strong>How should a function signal "no result"?</strong> Return `None` when
lack is plain and the caller will branch on it. Raise when lack means
a thing has gone wrong and the caller has no sensible option.

<strong>Is there a way to make `None` falsy checks safe?</strong> Not by
changing `None`. The fix is always to say which question you're asking &mdash;
emptiness or lack.

## Recap in one screen

- The falsy values are `None`, `False`, `0`, `0.0`, `""`, `[]`, `{}` and
  `set()`. All else is truthy, including `"0"` and `"False"`.
- `if not x:` means "empty, zero or missing, and I treat them the same".
- `x is None` means "this was never set". Is the only correct test when
  zero or empty is a legitimate value.
- Use `is` for `None` because there's just one of it and `__eq__` can't
  interfere.
- Your own classes get truthiness from `__bool__`, then `__len__`, and are
  or else always true.
""")


extend("try_and_except", """
## A retry loop, whole

The most common real use of `try` outside parsing, with the loop `else` doing
the "we ran out of attempts" branch:

```python
attempts = []

def flaky():
    attempts.append(1)
    if len(attempts) < 3:
        raise ConnectionError("timed out")
    return "ok"


for attempt in range(1, 5):
    try:
        print("result:", flaky())
        break
    except ConnectionError as e:
        print(f"attempt {attempt} failed: {e}")
else:
    print("gave up")
```

```
attempt 1 failed: timed out
attempt 2 failed: timed out
result: ok
```

Four details are worth copying. The `try` holds only the call that can fail,
so a bug in the printing wouldn't be caught as a link problem. The
`except` names one exact exception. So A `TypeError` from a refactor still
crashes loudly. The `as e` keeps the message. This Is the part that tells you
*why* it failed. And the `break` on success means the `else` runs only when
each attempt was used. This Is just the "gave up" case.

In production this would sleep between attempts, with the delay growing each
time, and would only retry errors that are really transient &mdash; a
timeout, yes. A `PermissionError`, never, because retrying it will fail
the same way four more times and delay the real error.

## The hierarchy, and what catching one gets you

Exceptions form a tree, and catching a class catches each subclass beneath it.
That is what makes `except Exception` catch almost all, and it's also
how you catch a handy family without listing its members.

At the top is `BaseException`. right beneath it sit `SystemExit`,
`KeyboardInterrupt` and `GeneratorExit` &mdash; the three that are *not*
errors, but control flow. `Exception` holds all else, and is what you
should catch when you must catch broadly, because it leaves those three alone.
This is the concrete difference between `except Exception:` and a bare
`except:`, and it's the reason the bare form makes a program hopeless to
interrupt with Ctrl-C.

Below `Exception`, the groupings are handy. `OSError` covers
`FileNotFoundError`, `PermissionError`, `IsADirectoryError`, `TimeoutError` and
the rest of the filesystem and network family. So `except OSError` is a
reasonable way to say "any of it the operating system refused".
`ArithmeticError` covers `ZeroDivisionError` and `OverflowError`.
`LookupError` covers `KeyError` and `IndexError`, which is at times just
what you want when reaching into a structure that might be short or missing a
field.

Knowing the tree turns "catch exact exceptions" from a rule into a thing
actionable: catch the narrowest class that covers the failures you really
have an answer for.

## Raising with the cause attached

When you catch an exception and raise a different one, the first is worth
keeping:

```python
try:
    try:
        int("abc")
    except ValueError as exc:
        raise RuntimeError("could not read config") from exc
except RuntimeError as e:
    print(type(e).__name__ + ":", e)
    print("caused by:", type(e.__cause__).__name__)
```

```
RuntimeError: could not read config
caused by: ValueError
```

`from exc` sets `__cause__`, and the printed traceback then shows both:
the low-level failure, the line "The above exception was the direct cause of
these exception", and your higher-level message. You get the *what* and
the *why* in one traceback.

Without `from`, Python still attaches the first as `__context__` and prints
"During handling of the above exception, another exception occurred" &mdash;
which is nearly as handy and reads as accidental rather than deliberate.
`raise ... from None` suppresses it fully. This Is at times right when
the inner error is noise a caller can't act on.

The reason this matters is that translating exceptions is good practice. A
library that lets a raw `KeyError` from its inner dict escape has
leaked its setup. One that raises `ConfigError("missing 'host'") from
exc` has given the caller a thing to catch and the maintainer a thing to
debug.

## Exceptions of your own

Defining one is a single line, and the payoff is that callers can catch just
your failure:

```python
class ConfigError(Exception):
    pass
```

Subclass `Exception`, not `BaseException`. Name it for the problem rather than
the place, and end it with `Error` by rule.

The reason to bother is selectivity. A caller who wants to handle a
configuration problem and let all else through can't do that if you
raised `ValueError`, because `ValueError` is also what `int()` raises three
frames down. A dedicated class makes the handler precise.

A small hierarchy pays off in a library: one base class such as
`ThingError(Exception)`, with exact subclasses beneath it. Callers who want
all catch the base. Callers who care about one case catch the subclass;
and adding a new failure mode later doesn't break either.

Attach the data rather than only formatting it into the message.
An exception that stores `self.path` or `self.field` lets a handler make a
choice, where a handler given only a string has to parse English to find out
what went wrong.

## The middle ground between crashing and swallowing

The advice to let exceptions travel and the need for a program that keeps
running are both real, and the space between them is where `logging` lives.

A handler has three honest choices. Handle it. You know what the failure
means and what to do instead. Translate it. Catch it, raise a thing
more real with `from`, and let it continue upward. Or record it and
re-raise, which is what `logging.exception` is for: it writes the message and
the full traceback to wherever logs go, and a bare `raise` afterwards sends the
exception on its way.

```python
try:
    process(record)
except ValueError:
    logging.exception("skipping record %r", record.id)
    continue
```

That pattern &mdash; log with the traceback, then skip this item and carry on
&mdash; is the correct shape for batch work. Here One bad record shouldn't
end a run over ten thousand. The crucial part is `logging.exception` rather
than `logging.error`, because the first includes the traceback and the second
throws it away.

What isn't an honest choice is `except Exception: pass`. It's the one form
that destroys info without replacing it, and the resulting program does
not fail &mdash; it makes output that is quietly incomplete, which is the
hardest kind of wrong to notice.

## Questions people ask

<strong>What is the difference between `except:` and `except Exception:`?</strong>
The bare form also catches `KeyboardInterrupt` and `SystemExit`, so it stops
Ctrl-C from working. Never use it.

<strong>Can I catch a few exceptions in one handler?</strong> Yes, with a
tuple: `except (KeyError, IndexError) as e:`.

<strong>Does `finally` run if the `try` returns?</strong> Yes. It runs on each
exit path, including `return` and `break`.

<strong>What happens if `finally` itself raises?</strong> Its exception
replaces what was in flight. This Is why `finally` blocks should be
simple.

<strong>How do I re-raise after logging?</strong> A bare `raise` inside the
handler re-raises the current exception with its first traceback intact.

<strong>Should I use exceptions for control flow?</strong> Python does, more
than most languages &mdash; `StopIteration` ends each `for` loop. Use them for
the exceptional path, not as a substitute for an `if`.

<strong>Is try/except slow?</strong> Setting up a `try` is nearly free. Raising
and catching isn't. That is why "ask forgiveness" wins when failures are rare
and loses when they're the common case.

<strong>What is an exception group?</strong> From Python 3.11,
`ExceptionGroup` carries a few exceptions at once &mdash; raised by
concurrent code where more than one task failed &mdash; and `except*` handles
them selectively.

## Recap in one screen

- Catch the narrowest exception you've an answer for. A bare `except:` also
  swallows Ctrl-C.
- Keep the `try` block down to the line that can fail, and put the follow-up in
  `else`.
- `as e` keeps the detail. This Is the part that makes the message handy.
- `raise NewError(...) from exc` preserves the cause, so the traceback shows
  both the what and the why.
- An exception you can't handle is info, not a problem &mdash; letting
  it travel beats a quiet wrong answer.
""")


extend("modules_and_import", """
## Circular imports, and how to break one

Two modules that each import the other give an error that reads as though
a thing is missing when nothing is:

```
ImportError: cannot import name 'Order' from partially initialized module
'models' (most likely due to a circular import)
```

The mechanism follows right from "importing runs the file". Module A starts
running and hits `from B import x`. B starts running and hits
`from A import y` &mdash; but A is only half-finished. `y` doesn't exist on
it yet. Python has A in `sys.modules` already. So It doesn't re-run it. It
hands back the partial module, and the name is missing.

Three fixes, in order of preference.

**Move the shared thing.** If A and B both need `Order`, it belongs in a third
module that both import and neither imports back. Most circular imports are a
missing module rather than an import problem.

**Import inside the function.** Moving `from B import x` into the function that
uses it delays it until both modules have finished loading. This works, and it
hides a dependency from anyone scanning the file. It's a fix rather than a
design.

**Import the module, not the name.** `import B` and then `B.x` at call time
often works where `from B import x` doesn't, because the field is looked
up when used rather than when imported.

The one that doesn't work is reordering the imports. This Often moves the
error rather than dropping it.

## Where installed packages come from

`sys.path` shows where Python looks. It doesn't explain how any of it got
there, and the gap is where most beginner import confusion lives.

`pip install requests` puts the package into the `site-packages` directory of
whichever Python is running `pip`. If you've a few Pythons &mdash; the
system one, one from Homebrew, one from a virtual environment &mdash; then
"pip installed it and Python can't find it" almost always means two different
interpreters. `python3 -m pip install x` avoids that fully by installing
into the interpreter you just named.

A **virtual environment** is a directory holding its own interpreter link
and its own `site-packages`. `python3 -m venv .venv` creates one and activating
it puts its interpreter first on your `PATH`. So `pip` and `python` both refer
to it. The point is alone: two projects can depend on incompatible versions
of the same library without either breaking, and the set of packages a project
needs is a property of the project rather than of your machine.

The hands-on rules are short. One environment per project. Record the
dependencies in a file so the environment can be rebuilt. Never install into
the system Python, which your operating system also uses. And when an import
fails unexpectedly, `python3 -c "import sys. Print(sys.executable)"` tells you
which interpreter you're really running. This Resolves the question faster
than any of it else.

## Organising modules of your own

A module is a file. So Organising code is organising files, and a few
rules save a lot of trouble.

Group by what things *are for*, not by what they're. A `models.py`,
`views.py`, `utils.py` split works until `utils.py` turns the place
all lands. Splitting by feature &mdash; `orders.py`, `billing.py`
&mdash; keeps related code together and keeps the imports between files
shallow.

Keep module-level code to meanings. any of it that runs work, opens files or
makes network calls at import time makes each importer pay for it, including
your test suite. Put it in a function and let the caller decide.

Avoid naming a file after a module you also import. A local `random.py`
shadows the standard library one for your whole program, and the resulting
`AttributeError: module 'random' has no field 'randint'` looks hopeless
until you spot the file.

And watch the direction of dependencies. If A imports B, B shouldn't need A.
When it does, the two are really one module, or there's a third one waiting to
be extracted &mdash; which is the same conclusion the circular-import section
reached from the other direction.

## Reading an import error

Four messages cover nearly each import failure, and each points a place
exact.

`ModuleNotFoundError: No module named 'requests'` means Python looked along
`sys.path` and found nothing. Either it isn't installed, or it's installed
for a different interpreter. Check with `python3 -m pip list` using the same
`python3` that failed.

`ImportError: can't import name 'X' from 'y'` means the module was found and
doesn't hold that name. Either it's a typo, or the version installed is
older than the one you're reading about, or it's a circular import and the
module is only half-loaded &mdash; the message says so when it can.

`AttributeError: module 'x' has no field 'y'` on a standard-library name is
the shadowing case: a file of your own named `x.py` is earlier on the path than
the real module. `print(x.__file__)` spots it right away.

`ImportError: attempted scaled import with no known parent package` means a
file inside a package was run right by path. Run it as
`python -m package.module` instead.

The common thread is that the message sets apart "couldn't find the module"
from "found it, couldn't find the name", and that gap sends you to
fully different places. Reading which of the two you've is most of the
diagnosis.

## Questions people ask

<strong>What is `__init__.py` for?</strong> It marks a directory as a package
and runs when the package is imported. It can be empty, and since Python 3.3 a
package without one mostly works &mdash; but including it avoids surprises.

<strong>Why does `from . import x` fail when I run the file?</strong> scaled
imports need a parent package. This A file run by path doesn't have. Run it
with `python -m package.module`.

<strong>Does `import` run the whole module?</strong> Yes, top to bottom, once
per program.

<strong>How do I reload a module I changed?</strong>
`importlib.reload(module)` in an interactive session. In a script, restart it
&mdash; reloading has enough sharp edges that it isn't worth leaning on.

<strong>Where is a module really loaded from?</strong>
`module.__file__` after importing it. This Is the fastest way to confirm you
have the one you meant.

<strong>Is `import x` inside a function slow?</strong> Only the first time.
After that it's a dict lookup in `sys.modules`.

<strong>What is the difference between a module and a package?</strong> A
module is a file. A package is a directory of modules. Both are imported the
same way.

<strong>Can a module import itself?</strong> It can, and it gets the in part
was reset version from `sys.modules`. There's no good reason to.

<strong>What does `if TYPE_CHECKING:` do?</strong> Guards imports that exist
only for type hints, so they cost nothing at runtime and can't cause a
circular import.

<strong>Should I import inside a function to speed up startup?</strong> Only
for truly heavy optional dependencies. For any of it else the cost is
already paid once and the hidden dependency isn't worth it.

## Recap in one screen

- Importing runs the file once, top to bottom, and caches the result in
  `sys.modules`.
- `import x` keeps the prefix and the provenance. `from x import y` is for one
  or two heavily used names. `import *` hides both and can silently overwrite.
- The `__main__` guard is what lets a file be both a script and an importable
  module.
- Circular imports mean a shared piece belongs in a third module.
- One virtual environment per project, and `python3 -m pip` to be certain which
  interpreter you're installing into.
""")


extend("classes_and_objects", """
## A small class, end to end

All a plain class often needs, in one block:

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError(f"deposit must be positive, got {amount}")
        self.balance += amount
        return self.balance

    def __repr__(self):
        return f"Account({self.owner!r}, {self.balance})"

    def __eq__(self, other):
        if not isinstance(other, Account):
            return NotImplemented
        return (self.owner, self.balance) == (other.owner, other.balance)


a = Account("ana")
a.deposit(50)

print(a)
print(a == Account("ana", 50))

try:
    a.deposit(-5)
except ValueError as e:
    print("ValueError:", e)
```

```
Account('ana', 50)
True
ValueError: deposit must be positive, got -5
```

Four things earn their place. each field is set in `__init__`, so reading
it tells you all the object holds. The method validates its input and
says what it received, not just that a thing was wrong. `__repr__` uses `!r`
on the owner so strings print quoted. This Is what makes a `repr` unambiguous.
And `__eq__` returns `NotImplemented` &mdash; not `False` &mdash; for unrelated
types, which lets Python try the other object's check before giving up.

## The dunder methods worth knowing

Python's protocols are all spelled as double-underscore methods, and defining
them is how your class gets to behave like a built-in type. Six cover most
needs.

`__repr__` is for programmers and should ideally look like the code that would
recreate the object. `__str__` is for users. If you only write one, write
`__repr__`, because `str()` falls back to it and the interactive prompt and
containers use it even so.

`__eq__` decides what equality means. Define it and you almost always want
`__hash__` too, because a class that defines `__eq__` without `__hash__`
turns unhashable and can't go in a set or be a dict key. The pair must
agree: objects that compare equal must hash the same.

`__len__` gives `len()` and, as a side effect, truthiness. `__iter__` makes the
object work in a `for` loop, in unpacking, and in `list()`. `__contains__`
gives `in`, though `__iter__` alone gives a working fallback.

The rest &mdash; math operators, context managers, checks &mdash;
follow the same idea: Python asks the object, and the object answers by having
the method. There's no separate interface to declare. A dataclass writes
`__init__`, `__repr__` and `__eq__` for you. This Is three of the six and the
usual reason to reach for one.

## Properties, for when an attribute needs logic

Python has no tradition of writing `get_x()` and `set_x()` for each field,
because it doesn't need one. Fields start as plain fields, and if one
later needs validation or work, `@property` converts it without changing
a single call site.

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2
```

`c.area` is now found on access and written without brackets, so it reads
like data. A matching `@area.setter` would let it be assigned, often to
validate: raising on a minus radius at the moment it's set rather than
discovering it later in a math.

The key consequence is cultural. In languages where adding validation
means changing each caller, people write accessors for all up front,
just in case. In Python that insurance is unneeded, so the idiomatic style
is a plain field until the day it needs to be more. And the day it
does, nothing outside the class changes.

Use a property when the value is truly field-like: cheap, side-effect
free, and conceptually part of the object's state. If it does real work, makes
a network call, or can fail in notable ways, a method with brackets is
honest about that and a property isn't.

## What makes a class worth reading

The mechanics of a class are simple. The judgement is in what goes on it, and
a few habits separate classes people can use from classes people work around.

**One job, named.** If the class name needs "and" to show it, it
is two classes. A name that is a noun for a thing in the problem &mdash;
`Invoice`, `Link`, `Basket` &mdash; is a better sign than one built from
patterns, like `InvoiceManager` or `DataHandler`, which often means "some
functions I put a place".

**A small surface.** The methods a caller needs should be few and obvious, and
all else should carry a leading underscore. A class with twenty public
methods is asking its callers to learn twenty things, and most of them
often turn out to be steps of two or three real ops.

**Fields that are all set in one place.** `__init__` should establish each
field the object will ever have. Fields that appear halfway through
another method make the object's state depend on call order, which is just
the thing that turns into "it works if you call `load()` first".

**Methods that use `self`.** A method that never touches the instance is a
function that has been filed in the wrong place. Moving it out makes it
testable on its own and shortens the class.

The underlying question is whether the class makes calling code shorter and
clearer than the equal functions would. If it doesn't, the functions were
the right answer, and Python is just right happy with a module full of them.

## Testing one

A class is easy to test when its state is small and its methods return values,
and hard when it's neither &mdash; which makes testability a handy
design signal rather than a separate chore.

The straightforward shape is: make the object, call a method, assert on
what came back or on one field. If that is awkward, the reason is often
one of three things. The constructor does real work, such as opening a file or
making a request, so the object can't be built in a test without the outside
world. The fix is to take the link as an arg rather than creating
it. The method returns nothing and changes a few fields, so the assertion
has to know internals. The fix is often to return the result. Or the outcome
depends on what was called earlier, in which case the test has to replay a
sequence, and that is the sign that the state wants to be smaller.

`__eq__` earns its place here too: it lets a test compare a whole object
against an expected one in a line, instead of asserting on four fields and
missing the fifth.

## Questions people ask

<strong>Why does each method need `self`?</strong> Because
`a.speak()` is `Dog.speak(a)` &mdash; the instance is passed by name rather
than appearing by magic. Python prefers clear.

<strong>What is the difference between a class and an instance
field?</strong> A class field is one object shared by all. An
instance field belongs to one object. set always creates the
instance one.

<strong>Do I need getters and setters?</strong> No. Use plain fields, and
`@property` on the day one needs logic.

<strong>What is `__slots__`?</strong> A declaration of the allowed fields
that saves memory for classes with many instances, at the cost of losing
dynamic fields. Worth it rarely.

<strong>Should I write `__str__` or `__repr__`?</strong> `__repr__` first
&mdash; it's what containers and the prompt use, and `str()` falls back to it.

<strong>What is a `@staticmethod` for?</strong> A function that belongs with
the class conceptually but uses neither the instance nor the class. A module
function is often just as good.

<strong>Why does my object print as an address?</strong> Because it has no
`__repr__`. Two lines fix it permanently.

<strong>Can a class have no methods at all?</strong> Yes, and a dataclass with
only fields is a just right good way to give a group of related values a name
and a readable `repr`.

## Recap in one screen

- A class bundles data with the functions that operate on it. Each instance
  carries its own fields and shares the methods.
- Set each field in `__init__`. So Reading the constructor tells you what
  the object holds.
- `self` is the instance, passed by name &mdash; `a.f()` is `Cls.f(a)`.
- Class fields are shared by each instance. Set through `self`
  always creates an instance field instead.
- `__repr__` costs two lines and pays for itself the first time you print a
  list of them. A dataclass writes it, `__init__` and `__eq__` for you.
""")


extend("nested_for_loops", """
## A worked example: a formatted table

Nested loops and the alignment that makes their output readable:

```python
for row in range(1, 4):
    for col in range(1, 4):
        print(f"{row * col:4}", end="")
    print()
```

```
   1   2   3
   2   4   6
   3   6   9
```

Two details do all the work. `end=""` on the inner `print` keeps the cells on
one line, and the bare `print()` after the inner loop &mdash; indented to the
outer loop &mdash; ends the row. Indent that second `print` one level further
and each cell gets its own line. Drop it and the whole table turns one
long line. The indentation is the logic.

`f"{value:4}"` right-aligns each cell in four characters. This Is what stops
the columns drifting once the numbers reach two digits. Counting spaces by hand
works until the data changes. A width doesn't.

## itertools.product, the flat version

When the nesting exists only to give each combination, `product` flattens
it into one loop:

```python
from itertools import product

print([f"{x}{y}" for x, y in product("ab", [1, 2])])
```

```
['a1', 'a2', 'b1', 'b2']
```

The order is the same as the nested loops it replaces: the last arg varies
fastest, just as the innermost loop does. `product` takes any number of
iterables, and `repeat=` gives the same one a few times &mdash;
`product(range(6), repeat=3)` is each three-dice roll without three levels of
indentation.

It's lazy, so it costs nothing until iterated, and it's the right tool when
the combinations are the point: param sweeps, test mats, each pairing
of two lists. It's the wrong tool when the inner loop depends on the outer one
&mdash; iterating the cells of each row. Here The rows differ in length
&mdash; because `product` pairs fixed sequences and can't look at the outer
value to decide what the inner one should be.

`itertools.combinations` and `permutations` cover the related questions, and
both avoid the nested loop plus index math that would or else be
needed to compare each pair without checking any of it with itself.

## The comprehension form, and its reading order

Nested loops have a comprehension equal, and the clause order is the thing
people get wrong:

```python
grid = [[1, 2], [3, 4]]

print([value for row in grid for value in row])
```

```
[1, 2, 3, 4]
```

The clauses appear in the same order as the equal nested `for` statements
&mdash; outer first, inner second. That is worth stating plainly because the
guess most people make is the opposite, and the wrong order raises a
`NameError` about the inner variable. This At least fails loudly.

What is truly confusing is a *nested comprehension*, where one comprehension
appears inside another's formula: `[[f(x) for x in row] for row in grid]`
makes a list of lists rather than a flat one. Here the reading order really
does invert &mdash; the outer clause is on the right and the inner work on the
left.

Between the two, flattening with two `for` clauses is common and readable, and
a comprehension inside a comprehension is where most people should stop and
write the loop. The rule from elsewhere in the track applies: if it needs
decoding rather than reading, the loop was the better answer.

## Let the data decide the loops

A nested loop is often a description of the data's shape, and when the two
disagree the loop is the thing that is wrong.

If the data is a list of rows and each row is a list of cells, two loops are
correct and the outer variable should be a row rather than an index. If the
data is a flat list and the nesting exists to pair items with each other, the
loops are doing a search and can often be replaced. If the data is a dict
of lists, the outer loop takes `items()` and the inner takes the list, and the
key is available at both levels without any bookkeeping.

The mismatch worth watching for is a nested loop over data that is already
flat. Code that iterates a list of records and then, inside, iterates the same
list to find a matching record is showing a join, and a dict keyed on
the join field turns it into one pass. The nesting was never about the shape of
the data. It was a linear search wearing a loop.

The opposite mismatch is a single loop over data that is truly nested,
often with manual index math to work out where each row starts. That is
a flattened structure being rebuilt by hand, and reshaping the data once
is easier than getting the math right at each use.

The general habit: write the loops that match the structure you've, and if
they're awkward, change the structure rather than the math.

## Measuring, rather than guessing

The cost of a nested loop can be read off the page, and when it matters it's
still worth measuring, because the constant factors aren't visible in the
form.

Two things make a reading handy. Run it at a few input sizes, not one:
a single number tells you how long a thing took. Three tell you how the
time grows, which is the property that decides whether the code lives
larger data. Doubling the input should roughly double a linear loop and
quadruple a nested one, and seeing that ratio confirms which you've.

And measure the thing itself, not the setup. `timeit` exists because a naive
timing includes interpreter warm-up, the cost of building the test data, and
what else happens to be in the block. It runs the snippet many times and
reports the best, which is the number least polluted by all else on the
machine.

The result is often surprising in the handy direction: a nested loop over
fifty items is instant and not worth changing, while a linear loop that does
a thing costly per item can be the real cost. Reading the structure tells
you how it scales. Measuring tells you whether it matters yet.

## Questions people ask

<strong>Can I use the same variable name in both loops?</strong> You can, and
the inner one shadows the outer for the rest of the body. It's legal and
confusing.

<strong>Does `continue` in the inner loop skip the outer one?</strong> No, it
moves to the next inner iteration only.

<strong>How do I break out of both loops?</strong> Put them in a function and
`return`, which is cleaner than any flag.

<strong>Is a nested loop always slow?</strong> No. It's slow when both
loops grow with the input. A loop over n holding a loop over a fixed three
items is linear.

<strong>What if the inner loop needs the outer index?</strong> `enumerate` at
both levels gives you both, without any `range(len(...))`.

<strong>Why does my inner variable still have a value after the loop?</strong>
Because a `for` loop doesn't have its own scope. The last value lives,
unlike in a comprehension.

<strong>Is `product` faster than nested loops?</strong> Slightly, and that is
not the reason to use it. It's flatter to read.

<strong>Should I worry about nesting depth for speed?</strong> Worry
about how many times each loop runs, not how deep they're. Three shallow loops
over three items each is nine iterations.

<strong>Can I nest a comprehension inside a loop?</strong> Yes, and it often
reads well &mdash; the loop handles the structure and the comprehension handles
one row.

<strong>Is there a limit on nesting depth?</strong> Python allows about twenty
levels of indentation, which is far past readability. Treat three as the
hands-on ceiling.

<strong>How do I loop over two grids together?</strong> `zip` the outer
sequences, then loop the pair: `for row_a, row_b in zip(a, b)`.

## Recap in one screen

- The inner loop runs fully on each pass of the outer one. The bodies
  times rather than add.
- Where the trailing `print()` is indented decides where rows end &mdash; the
  indentation is the logic, not the formatting.
- `break` leaves one loop. A function and `return` is the clean way out of
  both.
- Two loops over the same collection is `n` squared. An inner loop that is
  searching can often be replaced by a set or a dict.
- `itertools.product` flattens loops that exist only to give combinations.
""")


extend("variable_scope", """
## Watching the four scopes resolve

LEGB is easier to trust once you've seen it choose:

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        print("inner sees:", x)

    inner()

outer()
print("module sees:", x)
```

```
inner sees: enclosing
module sees: global
```

`inner` never assigns `x`, so it looks outward: not local, so enclosing &mdash;
and it stops there, at `outer`'s `x`, without ever reaching the module-level
one. The module's `x` is untouched, because `outer`'s set created a name
in `outer` rather than changing the global.

Now the version that fails:

```python
def broken():
    print(x)
    x = "too late"

broken()
```

```
UnboundLocalError: cannot access local variable 'x' where it is not associated
with a value
```

There's a just right good global `x`, and the `print` doesn't reach it. The
set on the line *below* made `x` local for the whole function, so the
`print` is reading a local that hasn't been given a value yet.

The wording of that error changed in Python 3.11. Older versions say "local
variable 'x' referenced before set". Both show the same thing, and
the newer one is clearer about it.

## Comprehensions have their own scope, loops do not

Two things that look similar and differ. This Shows a family of small
surprises.

A `for` loop does **not** create a scope. The loop variable is an plain
local, it lives after the loop ends. It overwrites any of it of the same
name. This is why `for i in range(3)` leaves `i` set to 2 afterwards, and why
reusing a name in nested loops silently shadows.

A comprehension **does** create one. Its loop variable lives only inside it,
doesn't leak, and doesn't clobber a name of the same spelling outside. This
changed in Python 3 in detail because the leaking was a common source of
bugs.

The consequence worth remembering is that a comprehension can read enclosing
names but can't see a class body's names. A comprehension written right in
a class body that refers to another class field raises `NameError`, because
the class body isn't a function scope and the comprehension's scope skips
straight past it to the module. It's the one truly strange corner of
Python's scoping, and the fix is to find the value outside the class or pass
it in through the iterable.

## Where scope shows up in practice

The rules are short. The situations where they bite are worth naming.

**A function that "doesn't update" a counter.** Assigning to a module-level
name inside a function creates a local instead. The function appears to run and
the value never changes. `global` fixes it and is often the wrong fix &mdash;
returning the new value and assigning at the call site keeps the dependency
visible.

**A callback that captured the wrong value.** Functions built in a loop capture
the *variable*, not its value. So They all see the final one. Binding it as a
default arg &mdash; `lambda i=i: ...` &mdash; captures at meaning time.
This is the same late-binding action that makes closures handy, seen from
the wrong side.

**A shadowed builtin.** Naming a variable `list`, `dict`, `sum`, `id` or
`input` hides the builtin for the rest of that scope. The failure comes later,
often as `TypeError: 'list' object isn't callable`, at a line that looks
correct.

**A name that only exists at times.** Assigning inside an `if` and reading
after it works when the branch ran and raises `UnboundLocalError` when it did
not. Reset before the branch.

All four are the same rule seen from different angles: set decides where
a name lives, and it decides it for the whole function.

## Why there is no block scope

Coming from C, Java or JavaScript, the most surprising rule is that an `if` or
a `for` doesn't create a scope. A name assigned inside one is visible after
it, and the loop variable outlives the loop.

This is deliberate, and the thinking is the same as all over else in the
language: functions are the unit of encapsulation, and adding a second, finer
kind of scope would mean two sets of rules for readers to hold. A function body
is one namespace, and where in that body a name was first assigned doesn't
change what it refers to.

It has hands-on consequences worth using rather than fighting. A value
found inside an `if` is available afterwards. So The common pattern of
declaring a variable before a branch purely so it exists later is unneeded
&mdash; assign it in both branches instead. A loop can leave its last value
behind on purpose, which is at times the neat way to say "the last item
that matched".

It also has one real hazard: a name assigned only inside a branch that didn't
run doesn't exist, and reading it raises `UnboundLocalError`. The compiler
knows the name is local. So It doesn't fall back to a global of the same
spelling. Resetting before the branch, or assigning on each path, is the
fix &mdash; and the error is at least loud rather than silently reading
a thing from an outer scope.

The one exception, comprehensions, exists just because the leaking there
was a genuine problem rather than a convenience.

## Questions people ask

<strong>Does an `if` or a `for` block create a scope?</strong> No. Only
functions, classes, modules and comprehensions do.

<strong>Can I read a global without declaring it?</strong> Yes. `global` is
only needed to *assign* to one.

<strong>What is the difference between `global` and `nonlocal`?</strong>
`global` reaches module level. `nonlocal` reaches the nearest enclosing
function. `nonlocal` fails if there's no such name.

<strong>Why does `items.append(1)` work without `global`?</strong> Because it
mutates the object rather than rebinding the name. Only set is affected.

<strong>Does a class body count as an enclosing scope?</strong> No, and this is
the exception that surprises people &mdash; methods don't see class-level
names without `self` or the class name.

<strong>Can I list what is in scope?</strong> `locals()` and `globals()` return
dicts of the current names. This Is at times handy for debugging.

<strong>Is shadowing a builtin ever fine?</strong> In a two-line function where
it's obvious, it does no harm. As a habit it costs more than the shorter name
saves.

<strong>Does `del x` drop a name from scope?</strong> It unbinds it, so a
later read raises `NameError` or `UnboundLocalError`. It doesn't reach into an
outer scope.

<strong>Why can a method not see class fields right?</strong> Because a
class body isn't an enclosing scope for its methods. Reach them through
`self.` or the class name.

<strong>What scope does a lambda have?</strong> The same as any function: its
own local scope, with the enclosing one visible. That is why the loop-capture
trap applies to lambdas just as it does to `def`.

## Recap in one screen

- Names resolve local, enclosing, global, builtin &mdash; first match wins.
- If a name is assigned anywhere in a function it's local all over in that
  function, including lines above the set.
- `global` and `nonlocal` rebind rather than shadow, and both are often a
  sign that a return value would be better.
- Mutating isn't assigning: `items.append(x)` needs no declaration,
  `items = [x]` creates a local.
- A `for` loop shares the enclosing scope. A comprehension has its own.
""")


extend("f_strings_and_formatting", """
## A worked example: a receipt

Alignment, decimals and a total, using nothing but the format spec:

```python
items = [("apple", 3, 1.5), ("banana", 12, 0.25)]
total = sum(q * p for _, q, p in items)

print(f"{'item':<10}{'qty':>5}{'each':>8}{'cost':>9}")
for name, qty, price in items:
    print(f"{name:<10}{qty:>5}{price:>8.2f}{qty * price:>9.2f}")
print(f"{'total':<10}{'':>5}{'':>8}{total:>9.2f}")
```

```
item        qty    each     cost
apple         3    1.50     4.50
banana       12    0.25     3.00
total                       7.50
```

The header row uses the same widths as the data rows. This Is what keeps the
labels over their columns &mdash; and it works because a string can take an
alignment and a width just as a number can. `{'':>8}` is an empty string padded
to eight, which is how the total line skips columns without counting spaces.

Text is left-aligned and numbers right-aligned. This Isn't a style preference:
right-aligning numbers puts the decimal points under each other, and that is
what makes a column of figures readable at a glance.

Note that `total` is found from the full-precision prices, not from the
rounded strings. Formatting is applied only where the number is printed, which
is the habit that stops a column of rounded values from failing to add up to
the rounded total.

## The three parts of a replacement field

All inside the braces follows one shape:
`{formula!conversion:format_spec}`, and knowing the three slots shows
a few things that or else look like separate features.

The **formula** is any Python formula, tested at that point.

The **conversion** is `!r`, `!s` or `!a`, applied before formatting. `!r` calls
`repr` instead of `str`. This Is what puts quotes around a string and makes
whitespace visible &mdash; invaluable in a debugging print, because `ana` and
`ana ` look the same without it.

The **format spec** is all after the colon, and it's handed to the
object itself. That is why `:.2f` means a thing to a float, `%d %B %Y` means
a thing to a `datetime`, and neither means any of it to the other.

The spec can hold its own braces. This Is how a width found at runtime
gets in:

```python
name = "ana"
w = 8
print(f"{name!r:>{w}}")
print(f"{3.14159:.{2}f}")
```

```
   'ana'
3.14
```

Nesting one level is allowed and is the standard way to align a table whose
column widths are found from the data rather than written into the source.

## Numbers as people read them

A handful of specs cover almost each number a person will look at.

```python
print(f"{1234567:,}")
print(f"{0.256:.1%}")
print(f"{5:+d}")
```

```
1,234,567
25.6%
+5
```

`,` inserts thousands separators, and `_` does the same with underscores.
`%` times by a hundred and appends the sign. This Is the correct way to
show a proportion &mdash; writing `f"{x * 100:.1f}%"` does the same thing with
one more place to make a mistake. `+` forces a sign on plus numbers, which
matters when the number is a change rather than a quantity.

Two further ones are worth having. `:>10,.2f` mixes alignment, separators
and decimals, which is the full treatment for a money column. And `:g` chooses
between fixed and scientific form based on magnitude. This Is handy when
the range of values is unknown and awful when it isn't, because the column
stops lining up.

For money in detail, note that floats aren't decimals. The formatting
is honest about what it was given. If the math used floats, the rounding
error was already there before the format spec saw it.

## Where formatting belongs in a program

An f-string is a presentation choice, and presentation choices are worth
keeping in one layer rather than scattered through the code that does the work.

The symptom of getting this wrong is a function that returns a string where it
should return a number. `def total(items) -> str` that hands back `"£7.50"`
looks convenient at the call site and has thrown away all else you might
do with the value: adding it to another total, checking it, storing it,
converting the currency. The caller who needs the number now has to parse the
string back, and the parse will eventually meet a thousands separator.

Keep values as values, and format at the point of output. A reporting function
takes numbers and makes the string. The math returns numbers. This is
the same boundary arg as converting input at the edge, run in the opposite
direction: parse on the way in, find in real types, format on the way out.

The second habit is to keep the template near the output rather than near the
data. A dict of format specs per column, applied in the printing loop,
is easy to change when the report changes. Specs scattered through the
functions that found each figure aren't.

There's one honest exception: log messages and error text, where the string
*is* the output and there's nothing downstream to preserve precision for. Even
there, prefer `logging.info("total %s", total)` over an f-string, because the
logger can then skip the formatting fully when the message is filtered out.

## Questions people ask

<strong>Can I use an f-string for a template stored elsewhere?</strong> No, it
is tested where it's written. `str.format` on a stored template is the tool
for that.

<strong>Is an f-string faster than concatenation?</strong> Yes, often
noticeably, because it doesn't build mid strings.

<strong>How do I put a quote inside?</strong> Use the other quote character, or
&mdash; from Python 3.12 &mdash; the same one.

<strong>Can I have a backslash inside the braces?</strong> Not before Python
3.12. Find the value on the line above instead.

<strong>What does `f"{x=}"` do?</strong> Prints the formula text, an equals
sign, and the value's `repr`. It's the fastest debugging print there's.

<strong>Do f-strings work with multi-line strings?</strong> Yes, prefix a
triple-quoted string with `f` and the braces work throughout.

<strong>Is it safe to put user input in one?</strong> For output, yes. Never
build SQL or shell commands this way. Use params, or the injection
is on you.

<strong>Why does my f-string print braces truly?</strong> Because you
doubled them, or because the `f` prefix is missing. Without the prefix the
braces are plain characters.

<strong>Can I format a value whose width I only know at runtime?</strong> Yes,
nest a field in the spec: `f"{value:>{width}}"`.

<strong>What is the difference between `!s` and no conversion?</strong>
Nothing, &mdash; `str` is the default. `!r` is the one worth
typing.

<strong>How do I show a number rounded but keep full precision?</strong> Format
only where you print. The variable is never changed by a format spec, so the
math that follows still uses each digit it had.

<strong>Can I align text and numbers in the same column?</strong> Yes, and it
often reads badly. Give the header the same alignment as the data if you
want them to line up, or left-align both.

## Recap in one screen

- The `f` prefix turns braces into slots holding any formula, tested
  where it appears in the sentence.
- After the colon is a spec handed to the object: `.2f`, `,`, `>8`, `%` and
  `%d %B %Y` all work this way.
- `!r` shows the `repr`. This Is how you see quoting and stray whitespace.
- Formatting changes the display, never the value. Format at the edge
  and keep full precision in the math.
- `f"{value=}"` prints the formula and its value together.
""")


extend("sets_and_set_operations", """
## Comparing two collections, concretely

The operators turn four common questions into four characters:

```python
a = {"ana", "bo", "cy"}
b = {"bo", "cy", "di"}

print(sorted(a & b))
print(sorted(a - b))
print(sorted(a ^ b))
print(a <= b, {"bo"} <= a, a.isdisjoint({"zz"}))
```

```
['bo', 'cy']
['ana']
['ana', 'di']
False True True
```

`&` is "in both", `-` is "in the first only", `^` is "in just one". Each
replaces a loop holding an `if`, and each is far harder to get subtly wrong
than the loop would be. There's no index, no accumulator, and no chance
of testing the wrong direction.

`sorted()` around each result is doing real work: a set has no order, so
printing one right gives an setup you must not depend on. Sorting on
the way out is how you get a stable, readable result.

The last line shows the check operators. `<=` is "is a subset of", so
`{"bo"} <= a` asks whether each member of the left is in the right. `>=` is
the superset direction, and `isdisjoint` asks whether two sets share nothing
&mdash; which is cheaper than building the intersection just to see if it's
empty.

## The questions each operator answers

The algebra is worth reading as English, because that is how you'll recognise
which one you want.

**"Which do they've in common?"** is `a & b`. Shared tags, users in both
groups, fields present in two records.

**"What is in the new one that wasn't in the old one?"** is `new - old`. Added
files, new permissions, keys that appeared. Reverse the operands for what was
removed, and note that this is the operator people most often get the wrong way
round.

**"What changed either way?"** is `a ^ b`. It's the union of both differences,
and it's the right answer for "what isn't the same". This Is often what a
diff wants.

**"Is all needed really present?"** is `needed <= given`, or
equivalently `needed - given` being empty &mdash; and the second version
is more handy because it tells you *which* are missing rather than
just that some are.

**"Do these share at all?"** is `a.isdisjoint(b)`. This Stops at the first
shared item rather than finding the whole intersection.

All five work with the method forms too &mdash; `intersection`, `difference`,
`symmetric_difference`, `issubset` &mdash; and the methods accept any iterable,
where the operators need both sides to be sets. `a & [1, 2]` raises;
`a.intersection([1, 2])` doesn't.

## Where a set fits among the collections

Choosing a container is choosing what you give up, and stating it as a table
makes the choice quick.

A **list** keeps order and duplicates and allows indexing. Membership testing
scans. A **tuple** is the same and immutable. It can be a key. A **set** has
no order, no duplicates and no indexing. Membership is constant time. A
**dict** is a set of keys with a value attached to each, and it inherits
the set's lookup speed for keys.

The choice often comes down to one question: what will you ask this
collection most often? If the answer is "give me item three" or "what order did
these arrive in", it's a list. If the answer is "is this one in here", it's a
set. If the answer is "what is the value for this name", it's a dict.

The case worth noticing is a list that is only ever asked "is this in here?".
That is a set wearing the wrong type, and converting it once before a loop
changes a scan per iteration into a lookup per iteration. It's one of the very
few speed changes that is both trivial to make and often decisive.

The reverse mistake is reaching for a set when duplicates carry meaning.
Counting votes, recording events, keeping a history &mdash; the duplicates
*are* the data, and a set silently deletes them.

## Building one efficiently

Three ways to get a set, and the differences matter once the input is large.

`set(iterable)` is the direct conversion and the one to use when you already
have the items. It's a single pass, and it works on any iterable including a
gen, so `set(line.strip() for line in f)` never builds the mid
list.

A set comprehension, `{f(x) for x in items}`, builds and deduplicates in the
same pass. This is better than `set([f(x) for x in items])`, which makes
the whole list first and then throws it away. The same waste as wrapping
any comprehension in a converter.

Adding in a loop with `add` is right when the items arrive one at a time or the
loop is doing a thing else as well. `update` takes an iterable and adds all
of it, so a loop that only calls `add` is often one `update` in disguise.

The one to avoid is again and again rebuilding: `seen = seen | {x}` inside a loop
creates a whole new set on each iteration. This Turns a linear job into a
quadratic one. `seen.add(x)` modifies in place, and `seen |= other` does the
same for a batch.

## Questions people ask

<strong>Why is `{}` an empty dict?</strong> Dicts had the braces
first. `set()` is the only way to write an empty set.

<strong>Can a set hold a list?</strong> No. Members must be hashable, and
lists can change. Use a tuple, or a `frozenset` for a set of sets.

<strong>Does `set()` preserve order?</strong> No. Use
`list(dict.fromkeys(items))` to deduplicate while keeping first-seen order.

<strong>Is `x in a_set` really constant time?</strong> On average, yes. It
hashes once and looks in one place, even so of size.

<strong>Can I sort a set?</strong> `sorted(s)` returns a list. A set itself has
no order to arrange.

<strong>What is the difference between `drop` and `discard`?</strong>
`drop` raises `KeyError` when the item is absent. `discard` doesn't.

<strong>Are `1` and `True` different set members?</strong> No. They hash the
same and compare equal, so `{1, True}` has one element.

<strong>Can I use a set as a dict value?</strong> Yes. Only keys need to
be hashable. Values can be any of it.

<strong>How do I find duplicates rather than drop them?</strong> Compare the
lengths, or use `collections.Counter` and keep the entries with a count above
one. A set alone tells you they existed, not which.

<strong>Is a set faster than a dict for membership?</strong> They use the
same mechanism, so in effect no. Use a dict when you also need a value
attached.

## Recap in one screen

- A set gives up order and duplicates and buys constant-time membership tests.
- `&`, `|`, `-` and `^` answer "both", "either", "only the first" and "just
  one" without a loop.
- `{}` is an empty dict. `set()` is the empty set.
- Members must be hashable, for the same reason dict keys must be: the
  hash decides where the item is stored.
- A list that is only ever asked "is this in here?" wants to be a set, and the
  conversion is often the whole fix for a slow loop.
""")


extend("function_arguments", """
## Watching the default accumulate

The trap is more lifelike when the shared object is visible:

```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket


print(add_item("a"))
print(add_item("b"))
print(add_item("c"))
print("the default itself:", add_item.__defaults__)
```

```
['a']
['a', 'b']
['a', 'b', 'c']
the default itself: (['a', 'b', 'c'],)
```

The last line is the point. `__defaults__` holds the actual default values, and
the list stored there has grown. It isn't that each call in some way gets
the previous result, it's that there has only ever been one list, created when
`def` ran, and each call has been appending to it.

Nothing about this is a special rule for functions. `basket=[]` is an
formula tested once, at meaning time, just like `x = []` at module
level. The surprise comes from expecting the default to be re-tested on each
call, which nothing in the syntax promises.

The fix, once more, because it's worth having in your fingers:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

`None` can't build up any of it, and the list is built inside the call where
it belongs.

## How a call is matched to a signature

Understanding the binding order makes the error messages readable, and there
are only four steps.

Spot-based args are assigned to params left to right. Then keyword
args are matched by name to what is left. Then any param still
unfilled takes its default. Then, if a param is still unfilled and has no
default, the call fails.

That order shows the errors. `missing 1 needed spot-based arg: 'x'`
means step four found a gap. `got multiple values for arg 'x'` means a
spot-based arg filled `x` in step one and a keyword tried to fill it again
in step two &mdash; which is what happens when you pass the first arg
positionally *and* by name. `got an unexpected keyword arg 'timeuot'`
means step two found no param of that name. This Is the typo case, and is
just the error that `**kwargs` would have swallowed.

Two rules follow from the same sorting. In a call, spot-based args must
come before keyword ones, because Python can't tell where a spot-based one
belongs once names have started. And in a meaning, params with defaults
must come after those without, for the same reason from the other side.

## Saying what a parameter expects

Type hints don't convert or enforce any of it at runtime, and they're still
the cheapest docs a signature can carry:

```python
def greet(name: str, times: int = 1) -> str:
    return f"hello {name} " * times
```

The value is threefold. A reader learns what to pass without reading the body.
An editor can complete and check the call. And a type checker run in CI catches
the mismatch before it ships. Which is the only one of the three that
really blocks any of it.

Two rules are worth adopting with them. Annotate the public functions and
skip the obvious inner ones. Annotations on a two-line helper cost more to
read than they explain. And when a param can be `None`, say so
&mdash; `def find(name: str) -> User | None`. Because that is the case
callers most often forget and the one a checker most usefully flags.

Hints also doc the mutable-default fix nicely: `basket: list | None = None`
states both the type and that omitting it's allowed, which is just
what the `None` sentinel means.

## Choosing the default

A default is a choice about what most callers want, and getting it wrong is
quiet: nothing fails, each call site just gets a little longer.

The test is simple. If most calls override the default, the default is wrong.
Either it should be the value people really pass, or the param should be
needed so that callers have to think about it. A default that exists only
because the param felt like it needed one adds a choice without making one.

Defaults should also be safe rather than convenient. A `timeout=None` meaning
"wait forever" is a default that turns a slow dependency into a hung program;
a finite timeout is the better choice though it can fail. The same
thinking applies to `overwrite=False`, `strict=True` and `retries=0`: when in
doubt, default to the action whose failure is loud.

And a default shouldn't depend on the state of the world. any of it tested
at meaning time &mdash; the current directory, the time, an environment
variable, a config object &mdash; is frozen at import and will be wrong for any
program that changes it afterwards. `None` plus a lookup in the body reads the
value when the call happens. This Is nearly always what was meant.

Finally, prefer a default over an optional param that changes the return
type. A function that returns a number most times and a tuple when
`verbose=True` has two signatures pretending to be one, and each caller has to
know which it triggered.

## Questions people ask

<strong>Are args passed by value or by ref?</strong> Neither, in the
C sense. The function gets another name for the same object, so mutating it's
visible to the caller and rebinding isn't.

<strong>Can a default refer to another param?</strong> No. Defaults are
tested at meaning time, when no args exist. Use `None` and find
it in the body.

<strong>Why must defaults come last?</strong> Or else a spot-based call could
not tell which param a value was for.

<strong>Is a tuple a safe default?</strong> Yes. Tuples are immutable, so there
is nothing to build up.

<strong>How do I force a caller to use names?</strong> Put a bare `*` before
those params in the meaning.

<strong>Can I see a function's defaults?</strong> `f.__defaults__` for
spot-based ones and `f.__kwdefaults__` for keyword-only ones.

<strong>How many params is too many?</strong> When you're counting on your
fingers at the call site. Group them into an object, or split the function.

<strong>Can I make each param keyword-only?</strong> Yes, put the bare `*`
first: `def f(*, a, b)`. Callers must then name both.

<strong>Does the order of keyword args matter?</strong> Not to Python. They
are matched by name, so any order works. Though matching the signature's
order helps a reader.

<strong>Can two params share a default object?</strong> They can, and they
shouldn't if it's mutable, because then both build up into the same thing.

## Recap in one screen

- args match by spot first, then by name. Spot-based ones come first
  in a call and non-default params come first in a meaning.
- Defaults are tested once, when `def` runs. Never default to a list,
  dict or set.
- `None` plus a check in the body is the idiomatic fix, and it reads right
  in a type hint too.
- A bare `*` makes the params after it keyword-only. This Is how a call
  site stops being a row of untagged values.
- The signature is the part others read most. Needed params are
  needs, and a default should be the right choice most of the time.
""")


extend("tuples_and_unpacking", """
## A worked example: taking a row apart

```python
row = ("ana", 91, "physics")

name, score, subject = row
print(f"{name}: {score} in {subject}")

name, *rest = row
print(name, rest)
```

```
ana: 91 in physics
ana [91, 'physics']
```

The first unpacking names all three spots. This Is what you want when the
shape is known and fixed. And if the row ever gains a fourth field, the
`ValueError` tells you at once rather than letting the extra value disappear.

The second collects the tail, and the starred name is a **list** though
the source was a tuple. That skew is deliberate: the collected part has no
fixed length, so it gets the type that handles varying lengths.

The names in the first line are doing the documenting. `row[1]` in code three
screens away means nothing. `score` means a thing. That is the real arg
for unpacking early &mdash; not brevity. But That it converts spots into
names at the point where you still note what the spots were.

## Tuples compare position by position

Check follows the same rule as sorting a dict word: compare the
first elements, and only if they're equal look at the second.

```python
print((1, 2) < (1, 3), (1, 2) < (2, 0), ("a", 2) < ("a", 10))

rows = [("bo", 78), ("ana", 91), ("ana", 43)]
print(sorted(rows))
```

```
True True True
[('ana', 43), ('ana', 91), ('bo', 78)]
```

The second check is the one worth noticing: `(1, 2) < (2, 0)` is true even
though 2 is greater than 0. The first elements already decided it. The
later spots are never consulted once an earlier one differs.

This is just why a tuple works as a sort key. `key=lambda r: (-r.score,
r.name)` sorts by score and breaks ties by name, and it does so because tuple
check stops at the first difference. each multi-level sort in the track
leans on this one rule.

It also means check fails the same way unpacking does when the types do
not line up: `(1, "a") < (1, 2)` raises. Once the first elements tie
Python has to compare a string with an int.

## Tuples you use without noticing

A good deal of Python hands you tuples whether you asked for them or not, and
recognising them shows a few pieces of syntax at once.

A function returning a few values returns a tuple. `return a, b` builds one
and the caller unpacks it. `*args` collects into a tuple, not a list, which is
why you can't append to it inside the function. `dict.items()`, `enumerate`
and `zip` all yield tuples. This Is why `for k, v in ...` works for all three.
An exception carries its args in `e.args`, a tuple. String formatting with
`%` takes one, which is why `"%s" % (value,)` needs that trailing comma.

And the swap, `a, b = b, a`, builds a tuple on the right and unpacks it on the
left &mdash; there's no special swap syntax, just the plain rules applied
in both directions in one statement.

The common thread is that a tuple is Python's way of saying "a fixed group of
things, in order". Wherever the language needs that, it uses one, which is why
learning tuple action pays off far outside the places you write the brackets
yourself.

## Immutable does not mean constant

Two words get used alike and mean different things, and the confusion
causes real bugs.

A tuple is **immutable**: the object can't be changed after it's built. That
is a property of the object.

A name is **rebindable**: `point = (3, 4)` followed by `point = (5, 6)` is
just right legal. The first tuple was never modified. The name now refers to a
different one. Nothing about immutability stops a variable from being pointed
a place else, and Python has no way to prevent that at all &mdash; the
uppercase naming rule for constants is a request, not a rule.

The hands-on consequence is that handing someone a tuple ensures they
can't change *your* object. It doesn't ensure that a name in their code
still refers to it later, and it doesn't make the values inside it constant if
those values are themselves mutable.

This is the same gap as "rebinding versus mutating" from elsewhere in
the track, seen from the other side. Immutability drops one of the two
ops. The other one is always available.

## Questions people ask

<strong>Do I need the brackets?</strong> often not &mdash; the comma makes
the tuple. Brackets are for clarity and for cases where precedence would
or else take over, such as inside a function call.

<strong>How do I make a one-element tuple?</strong> `(5,)` with the trailing
comma. `(5)` is just the number in brackets.

<strong>Can I sort a tuple?</strong> `sorted(t)` returns a list. A tuple can't
be sorted in place, because that would change it.

<strong>Are tuples faster than lists?</strong> Slightly to build and slightly
smaller, and that is rarely the reason to pick one. Pick by whether the
contents should be able to change.

<strong>Can a tuple hold a list?</strong> Yes, and then it isn't hashable
&mdash; so it can't be a dict key, though it's a tuple.

<strong>What does `ValueError: too many values to unpack` mean?</strong> The
right-hand side had more items than you gave names for. often the data
changed shape.

<strong>Is `namedtuple` still worth using?</strong> Yes for a lightweight
immutable record, though a frozen dataclass is often clearer for any of it with
action attached.

<strong>Can I unpack into an existing list element?</strong> Yes &mdash;
`a[0], a[1] = a[1], a[0]` is legal. Is how you swap two spots of a
list in one statement.

<strong>Does unpacking work on a gen?</strong> Yes, and it consumes it.
The count still has to match. It will run the gen to the end to find
out.

<strong>Why is `*args` a tuple rather than a list?</strong> Because the
args are a fixed group by the time the function starts, and making it
immutable stops a function from accidentally altering what it was called with.

## Recap in one screen

- A tuple is a fixed, sorted group whose spots carry meaning. That is what
  makes it hashable and safe to hand around.
- The comma makes the tuple, not the brackets. And a one-element tuple
  needs the trailing comma.
- Unpacking turns spots into names, and a wrong count raises right away
  rather than failing quietly later.
- Check goes spot by spot and stops at the first difference, which
  is what makes tuple sort keys work.
- Immutability is shallow: a tuple holding a list is neither frozen nor
  hashable.
""")


extend("list_comprehensions", """
## What a comprehension cannot contain

The limits aren't any. They follow from a comprehension being an
formula, and knowing them tells you just when to stop trying.

**No statements.** No set with `=`, no `return`, no `raise`, no `pass`.
The walrus `:=` is the one exception, added just because naming an
mid value was the one statement people truly needed.

**No `try`.** If one item might raise, a comprehension can't handle it. The
whole thing fails and you lose the items already processed. A loop with a
`try` inside is the only way to skip the bad ones and keep the rest, and that
is a common enough need that it alone decides the shape of a lot of
data-cleaning code.

**No `break` or `continue`.** A filter can drop items. But Nothing can stop the
iteration early. `itertools.takewhile` covers the `break` case, and the
trailing `if` covers `continue`.

**Nothing handy for side effects.** A comprehension whose result is discarded
&mdash; `[print(x) for x in items]`. Builds a list of `None` to throw
away, and hides that iteration is the point. Write the loop.

Each of those is a signal rather than an obstacle. When you find yourself
wanting one, the answer isn't a cleverer comprehension. It's that the job has
outgrown the form.

## Reading one somebody else wrote

Comprehensions are written left to right and ran in a different order,
which is what makes an unseen one hard to parse. A solid method:

**Find the `for` clauses first.** Read them left to right. They're the loops,
outermost first. Skip all before the first `for` while you do this.

**Then the trailing `if`.** It filters what the loops made, and it runs
before the formula at the front.

**Then the formula.** It applies last, to each surviving item, and it's
what the result holds.

**Finally the brackets.** Square gives a list, braces a set, braces with a
colon a dict, round a gen that hasn't run yet.

So `[f(x) for row in grid for x in row if x]` reads as: for each row in grid,
for each x in row, keep the truthy ones, and collect `f(x)`. Four clauses, read
in the order they execute. This Is right to left except for the formula
that comes first on the page.

The value of having a method is that it also tells you when a comprehension is
too much: if the method takes more than a few seconds, the loop version would
have been read in one pass.

## The cost, and where the loop wins

A comprehension is often a little faster than the equal loop, because
the appending happens in the interpreter's own loop rather than through a
method lookup on each pass. The difference is real and small, and it's almost
never the deciding factor.

Where the difference does matter is memory. A list comprehension over a large
input builds the whole result before any of it else happens. A gen
formula doesn't. For a file with millions of lines, that is the difference
between a program that runs and one that doesn't, and it costs one character
to switch.

Where the loop truly wins is all the previous section listed, plus
one more: debugging. You can put a `print` or a breakpoint inside a loop body.
You can't put one inside a comprehension without changing it into a thing
else. When a change is making the wrong answer and you don't know
why, converting it to a loop for five minutes is often the fastest route to the
cause.

## The shape it replaces, and the one it does not

A comprehension replaces just one loop shape: build an empty collection,
iterate, append a thing derived from each item. Recognising that shape is how
you know a comprehension applies without having to try it.

The tell is that the accumulator is only ever appended to, and the thing
appended depends only on the current item. Nothing reads the accumulator, no
other variable is updated, and the loop body is a single formula.

The shapes it doesn't replace are worth naming, because they look similar.

**Building up.** A running total, a max so far, a count &mdash; any of it
where the next value depends on what came before. Comprehensions have no access
to what they've already made. This Is why `sum`, `max` and `Counter`
exist as separate tools.

**Grouping.** Building a dict of lists needs to append to an entry that
may already exist, which is a read of the accumulator. `setdefault` or
`defaultdict` in a loop is the answer.

**Two outputs.** Splitting one input into two lists in a single pass. A
comprehension makes one collection, so this is either two comprehensions
over the same data or one loop. And the loop reads the input once.

## Questions people ask

<strong>Is a comprehension faster than a loop?</strong> Slightly, for building
a list. Not enough to choose one for that reason.

<strong>Can I use two filters?</strong> Yes, and chained filters mean `and`.

<strong>Why does my nested comprehension have the loops backwards?</strong>
Because the clauses read outer-first, the same order as nested `for`
statements. It's the guess most people get wrong.

<strong>Can I ref the previous item?</strong> Not right. Zip the list
with a shifted copy of itself, or write the loop.

<strong>Does the loop variable leak?</strong> No, a comprehension has its own
scope. A `for` statement doesn't.

<strong>Can I build a list of lists?</strong> Yes, with a comprehension in the
formula slot: `[[f(x) for x in row] for row in grid]`.

<strong>When should I definitely not use one?</strong> When the body needs a
`try`, a `break`, an set, or exists for a side effect.

<strong>Can a comprehension be spread over a few lines?</strong> Yes, and it
often should be &mdash; one clause per line, with the formula on the first,
reads far better than a long single line.

<strong>Is there a limit to how many `for` clauses I can use?</strong> No limit
in the language, and a hands-on one of about two before it stops being
readable.

<strong>Why does a gen formula inside a function call need no extra
brackets?</strong> Because it's the only arg. With more than one
arg, the brackets are needed to say where it ends.

<strong>Should I name the result of a comprehension?</strong> Almost always. A
comprehension passed straight into another call is compact and gives the reader
nothing to hold on to. A name says what the collection is.

## Recap in one screen

- A comprehension states the shape of the result first. This Is what makes it
  clearer than a loop for a plain change.
- The `for` clauses read outermost-first. The trailing filter runs before the
  formula at the front.
- It's an formula, so no statements, no `try`, no `break` &mdash; and those
  limits are the signal to write the loop.
- Round brackets give a gen that builds nothing. This Is the right
  default inside `sum`, `any`, `max` and `join`.
- One `for`, one filter: past that, the loop is easier to read, to change and
  to debug.
""")


# --------------------------------------------------------------------------
# Third pass: where each feature reappears. These tracks were written after
# the sections above, so the pages that most need to point at them - async,
# concurrency, and the interview questions built on the same idea - had no
# way in. One closing section each, at the end of the article.
# --------------------------------------------------------------------------

extend("generators_and_yield", """
## The same pause, one level up

A gen pauses at `yield` and hands control back to whoever called `next`.
A coroutine pauses at `await` and hands control back to the event loop. That is
very nearly the same machinery. A frame kept alive between resumptions
&mdash; and the resemblance isn't a coincidence: `async def` grew out of
gens, and for a few releases you wrote coroutines *as* gens, with
`yield from` standing where `await` now goes.

<p>Two pages take it from here:</p><ul><li><a href="../async_python/coroutines_tasks_and_await.html">Coroutines, tasks. What await really does</a>. The same suspend-and-resume, with a loop deciding who resumes next instead of a <code>for</code> statement.</li><li><a href="../async_python/queues_and_backpressure.html">Queues, producers and backpressure</a>. Lazy production when the consumer sets the pace. This Is what a gen does when the consumer is a loop. What a bounded queue does when the consumer is another task.</li></ul>

Laziness is also the whole point of an interview question that looks like it's
about heaps: <a href="../interview/merge-k-sorted-sequences.html">merging k
sorted sequences</a>. `heapq.merge` returns a gen, and if you're going to
materialise the entire result it's *slower* than concatenating and sorting
&mdash; but it makes the first value in a fraction of a millisecond, which is
the reason to reach for it when the sequences are files you'd rather not
hold in memory all at once.
""")


extend("variable_scope", """
## Scope says who can see a name, not who can see it at the same time

All above assumes one thread of run. Add a second and each rule
still holds &mdash; a call still gets its own local namespace, `global` still
rebinds at module level &mdash; but a question appears that scope can't answer.
Two threads running the same function have separate locals, and *share* each
global, along with each mutable object those locals happen to point at.

That sharing is where the hard bugs live. `counter += 1` on a module-level
int is a read, an add and a write. The other thread can be scheduled in
either gap.

<ul><li><a href="../concurrency/race_conditions_in_python.html">Race rules, and the ops that aren't atomic</a>. That exact increment, run 200,000 times by two threads, losing a countable number of updates.</li><li><a href="../concurrency/locks_and_the_ways_they_go_wrong.html">Locks, and the ways they go wrong</a>. Making a read-modify-write indivisible, plus the deadlock you get free of charge when two locks are taken in two orders.</li></ul>
""")


extend("mutability_and_aliasing", """
## Aliasing across threads is this bug with the timing removed

Two names for one list is a small surprise while you read a function top to
bottom. Two *threads* holding the same alias is the same fact minus the ability
to find it: you can no longer point at the line where the object changed,
because it changed between two of your own lines.

Nothing about mutability is different there. What is different is that "who
else holds a ref to this?" stops being answerable by reading the
enclosing function.

<ul><li><a href="../concurrency/threads_or_processes.html">Threads or processes: what is and isn't shared</a>. Threads alias the whole heap. A process gets a copy. That copy is just why a child's mutation never reaches the parent.</li><li><a href="../concurrency/race_conditions_in_python.html">Race rules. The ops that aren't atomic</a>. What an aliased list looks like when two threads append to it.</li></ul>

The defensive move is the one this page already argues for: copy at the
boundary, or hand over a thing immutable. It's cheaper than a lock, and
unlike a lock it can't be forgotten at one call site.
""")


extend("sorted_with_key", """
## When you do not need the whole thing in order

`sorted(..., key=...)` puts each element in order. This Is more than most
questions ask for. If you only want the largest few, a sort does work you then
discard &mdash; `heapq` does the smaller job, holding k items instead of n.

The gap is measurable rather than asymptotic hand-waving. On a list with many
distinct keys, a full sort took 155.9 ms where `nlargest` took 11.9 ms. On a
list with only a handful of distinct values, the sort *won*. Which way it falls
is a property of the data, not of the form.

<ul><li><a href="../interview/top-k-frequent-elements.html">Top k frequent elements</a>. Count, then a heap of size k, with both timings printed side by side.</li><li><a href="../interview/kth-largest-element.html">Kth largest element</a> &mdash; the same idea reduced to a single value.</li><li><a href="../dsa/heaps_and_priority_queues.html">Heaps and priority queues</a> &mdash; how a heap answers "smallest" in constant time while refusing to tell you any of it about the order of the rest.</li></ul>
""")


extend("files_and_with", """
## with is a protocol, and files are only its most common user

Nothing in `with` is about files. It calls `__enter__`, runs the block, and
calls `__exit__` but the block ends. Which makes it the right shape
for any of it with a matching pair of ops. Open and close. Begin and
commit. Acquire and release.

<ul><li><a href="../concurrency/locks_and_the_ways_they_go_wrong.html">Locks, and the ways they go wrong</a>. <code>with lock:</code> is this page's pattern with a different resource, and the reason to prefer it over <code>acquire()</code> and <code>release()</code> is one you've already met. An exception in the middle of the block still releases.</li></ul>

There's one place `with` won't save you. Opening and reading a file is a
blocking call, and inside an `async def` it stops the event loop rather than
yielding to it &mdash; the `with` block is scoped just right right and the
whole loop is frozen for its duration.

<ul><li><a href="../async_python/the_blocking_call_that_freezes_the_loop.html">The blocking call that freezes the loop</a>. Where the heartbeat stops. Where to put file and CPU work so that it doesn't.</li></ul>
""")
