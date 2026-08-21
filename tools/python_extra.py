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

Unpacking is not limited to assignment. It is how a for loop reads pairs:

```python
for name, score in [("ana", 91), ("bo", 78)]:
    print(name, score)
```

Each item is a two-tuple, and the loop unpacks it into two names on the way
in. `dict.items()` yields tuples, which is why `for k, v in d.items()` works
at all, and `enumerate` yields `(index, value)` for the same reason.

A star collects the middle:

```python
first, *rest = [1, 2, 3, 4]      # first = 1, rest = [2, 3, 4]
head, *body, tail = "a b c d".split()
```

The starred name always becomes a list, even when it captures nothing, which
means `rest` is `[]` rather than `None` for a one-item sequence. That is worth
knowing before you write `if rest is None`.

## Where the wrong number of names bites

```python
x, y = (1, 2, 3)
```

raises `ValueError: too many values to unpack`. That looks like an annoyance
and is a safety net: it fires the moment the shape of your data changes. Code
that indexed `point[0]` and `point[1]` would have carried on quietly with a
three-element point and produced wrong answers much later.

The same error appears when a function you expected to return two things
returns one, which is usually the real bug rather than the unpacking.

## Named tuples, when positions stop being obvious

Positional access stops reading well past two or three fields. `record[4]`
tells nobody anything.

```python
from collections import namedtuple

Point = namedtuple("Point", "x y")
p = Point(3, 4)
print(p.x, p[0])        # both work
```

A named tuple is still a tuple - immutable, hashable, unpackable - but its
fields have names. It costs one line and it is the usual answer when a plain
tuple has grown past the point where you can remember what position two was.
""")


add("sets_and_set_operations", """
## Order, and why you cannot rely on it

A set has no order. Printing one twice in the same run usually gives the same
arrangement, which tempts people into depending on it, and that arrangement
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

Dictionaries preserve insertion order, so this is the standard trick for
"unique but in the order I saw them".

## Modifying a set

```python
seen.add("x")          # one item
seen.update(others)    # many
seen.discard("x")      # remove, no error if absent
seen.remove("x")       # remove, KeyError if absent
```

`discard` and `remove` differ only in what happens when the item is not there,
and choosing between them is a small design decision: `remove` says "this
should have been present", `discard` says "get rid of it if it is".

The operators have in-place forms too: `a |= b` adds everything from b, `a &= b`
keeps only what both share.

## A frozen set, for when a set needs to be a key

Sets are mutable, so a set cannot be a dictionary key or a member of another
set. `frozenset` is the immutable version:

```python
groups = {frozenset({"ana", "bo"}): "pair one"}
```

This comes up when the key is genuinely a collection - a set of tags, a group
of users - and you need to look something up by it.

## The cost, concretely

Building a set from a list is one pass, so converting is cheap. The win comes
when you test membership more than once. Converting a list to a set to do a
single lookup is slower than just scanning the list; converting once and then
testing thousands of times is the case the second program on this page
measures, and there the difference is not subtle.
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

When you need the coordinates as well, `enumerate` supplies them at both
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

The function is almost always the right answer: `return` leaves everything, and
the search gets a name.

## When nesting is hiding a better idea

Two loops over the same collection compare every pair, and that is `n squared`
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

The rule of thumb: if the inner loop is searching for something, a set or a
dictionary usually removes it. If the two loops walk genuinely different
things - rows and columns, users and permissions - the nesting is correct and
there is nothing to remove.
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

Read it in the order it executes, which is not the order it is written: take
each `r` from `rows`, keep it if the score clears 50, and collect
`r["name"]`. The expression at the front is applied last, to whatever survives
the filter.

Written as a loop that is four lines and one more variable to name.

## The variable does not leak

```python
squares = [n * n for n in range(5)]
print(n)        # NameError
```

The loop variable belongs to the comprehension and is gone afterwards. That is
a deliberate difference from a `for` statement, whose variable outlives the
loop, and it is the reason a comprehension cannot quietly overwrite an `n` you
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

Braces with a colon give a dictionary; braces without give a set. Both take the
same trailing `if`, and both are worth reaching for when the loop version would
be three lines of `result[key] = value`.
""")


add("f_strings_and_formatting", """
## Formatting a table without counting spaces

Alignment is where the format spec earns its keep. Left-align text, right-align
numbers, and the columns line up whatever the data:

```python
rows = [("apple", 3, 1.5), ("banana", 12, 0.25), ("cherry", 100, 12.0)]
print(f"{'item':<10}{'qty':>5}{'price':>10}")
for item, qty, price in rows:
    print(f"{item:<10}{qty:>5}{price:>10.2f}")
```

`<` left, `>` right, `^` centre, and the number after it is the field width.
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

That is not a special date feature of f-strings; it is `datetime` interpreting
the spec it was given. The same mechanism is why `:.2f` means something to a
float and nothing to a string.

## Quotes inside the braces

Before Python 3.12 you could not reuse the outer quote character inside the
expression:

```python
f"{d['key']}"        # fine: single inside double
f"{d["key"]}"        # SyntaxError before 3.12, allowed after
```

Sticking to the older form costs nothing and works everywhere, which is the
usual reason to keep doing it.

## Escaping a brace

A literal brace is doubled:

```python
print(f"{{not a placeholder}} but {2 + 2} is")
# {not a placeholder} but 4 is
```

This matters when you are generating JSON, CSS or anything else that uses
braces, and it is the first thing to check when an f-string raises a confusing
`KeyError`.
""")


add("function_arguments", """
## Keyword-only parameters

Anything after a bare `*` in the definition can only be passed by name:

```python
def connect(host, *, timeout=30, retries=3):
    ...

connect("db.local", timeout=5)      # fine
connect("db.local", 5)              # TypeError
```

This is how you stop a call site from becoming a row of unlabelled values.
`connect("db.local", 5, 2)` tells a reader nothing; forcing the names makes the
call self-documenting, and it means you can reorder or add options later
without breaking anyone.

The mirror image is `/`, which marks parameters as positional-only. It appears
in the standard library more than in application code.

## Arguments are evaluated at the call

```python
def log(message, when=now()):    # now() runs ONCE, at definition
```

This is the same rule as the mutable default, wearing different clothes. If you
want the current time on each call, compute it inside:

```python
def log(message, when=None):
    if when is None:
        when = now()
```

Any expression in a default - a function call, a list, a dict, an object - is
evaluated once when the `def` statement runs, and the result is reused forever.

## Too many parameters is a design signal

A function with eight parameters is hard to call correctly and hard to change.
Two usual remedies:

- group related arguments into a small object or a dataclass, so `draw(config)`
  replaces `draw(x, y, w, h, colour, border, alpha, z)`
- split the function, because eight parameters often means it is doing more
  than one job

Neither is a rule, but if you are counting arguments on your fingers at the
call site, the call site is telling you something.

## Argument order in the definition

Positional first, then defaults, then `*args`, then keyword-only, then
`**kwargs`. Python enforces most of that, and the error messages are clear when
you get it wrong - unlike the mutable default, which never complains at all.
""")


# --------------------------------------------------------------------------
# Second pass over the first six: the sections above lean on code, and code
# does not count as reading. These add the explanation around it.
# --------------------------------------------------------------------------

def extend(slug, text):
    EXTRA[slug] = EXTRA.get(slug, "") + text.rstrip() + "\n"


extend("tuples_and_unpacking", """
## Why immutability is not just a restriction

It is tempting to read "cannot be changed" as a limitation you work around. In
practice it is a property you rely on. An immutable object can be shared freely
between functions, threads and data structures, because no holder of it can
surprise another holder by editing it. That is why the language reaches for
tuples in exactly the places where a surprise would be expensive: function
arguments arrive as a tuple, exceptions carry their arguments as a tuple, and a
function returning several values returns a tuple rather than a list.

The immutability is shallow, and this catches people. A tuple guarantees that
its slots keep pointing at the same objects; it says nothing about those
objects. A tuple containing a list will happily let you append to that list,
and the tuple is unchanged as far as Python is concerned, because it still
points at the same list. This is also why such a tuple is not hashable: its
contents can change, so any hash computed from them would go stale.

## Choosing between a tuple, a list and a small class

Three options, and the decision is usually about what the positions mean.

A list is right when the items are the same kind of thing and the collection
grows, shrinks or gets sorted: a list of scores, a list of users, a queue of
jobs. Position carries no meaning beyond order.

A tuple is right when the group is fixed at creation and each position means
something specific: a coordinate pair, an RGB colour, a database row. Position
is the meaning, which is exactly why the group must not change length.

A small class or a dataclass takes over when there are more than about three
fields, or when you find yourself writing a comment to remember what position
three was. Names beat positions the moment positions stop being obvious, and a
named tuple is the halfway house that keeps tuple behaviour while adding them.
""")


extend("sets_and_set_operations", """
## What "hashable" is really asking

A set decides where to store an item by computing its hash, so the hash has to
stay the same for as long as the item is in the set. That is the entire reason
lists and dictionaries cannot be set members: they can change, the hash would
change with them, and the set would be looking in the wrong place for something
it definitely contains.

This is not a rule Python invented to be awkward. It falls straight out of how
the lookup works. The same constraint applies to dictionary keys, which is why
the two rules are always taught together, and why the error message mentions
hashability rather than mutability.

Strings, numbers, booleans, `None` and tuples of those are all hashable and can
go in a set. Anything you can mutate cannot.

## Sets in everyday code

Three patterns cover most real uses.

Deduplication is the obvious one: `set(values)` collapses repeats in a single
pass, and wrapping it in `sorted()` gives back a predictable order.

Membership testing is the important one. Any time a loop contains `if x in
something`, ask what `something` is. If it is a list that does not change during
the loop, converting it to a set once before the loop turns a scan into a
lookup, and that single change is often the entire fix for a slow function.

Comparing two collections is the one people forget exists. "Which users are in
both groups", "which required fields are missing", "which files changed" are all
one operator rather than a loop with an `if` inside it, and the operator version
is far harder to get subtly wrong.
""")


extend("nested_for_loops", """
## Reading the cost without timing anything

You can tell the cost of a nested loop by reading it. Count how many times each
loop runs and multiply. Two loops over the same n-item list run n times n. A
loop over n containing a loop over m runs n times m. A loop over n containing a
lookup in a set runs n times, because the lookup does not loop.

That last one is the important case. A nested loop and a loop containing a set
lookup can look almost identical on the page and behave completely differently
at scale, and the difference is invisible on ten items and decisive on ten
thousand.

This is also why the timings on this page are run at three sizes rather than
one. A single measurement tells you how long something took; three tell you how
the time grows, which is the thing that actually matters when your data gets
bigger.

## Depth, and when to stop

Two levels of nesting is ordinary. Three is worth a second look. Four is nearly
always a sign that some of the structure belongs in a function, because by then
nobody can hold all the loop variables in their head at once, and the
indentation alone pushes the real work off the right of the screen.

Pulling the inner loops into a named function costs nothing at runtime and
gives each level a name that says what it is iterating over. It also gives you
`return`, which is the cleanest way out of nested loops there is.
""")


extend("list_comprehensions", """
## What a comprehension is really for

The value of a comprehension is not that it is shorter. It is that it says
"this is a transformation" in a way a loop cannot. A loop that builds a list is
three separate statements - create, iterate, append - and a reader has to hold
all three to work out that nothing else is happening in between. A
comprehension states the shape of the result on the first line, and there is
nowhere for anything else to hide.

That is also the test for whether you should use one. If the body does one
thing to each item, a comprehension expresses it better. If it does several
things, updates something outside itself, or needs a `try`, the loop is not just
acceptable but correct, because those are exactly the things a comprehension
cannot contain and should not be contorted into.

## Building something other than a list

The same syntax makes dictionaries and sets, and swapping the brackets for
round ones makes a generator that builds nothing at all. Choosing between them
is choosing what you need afterwards. If you are going to iterate the result
once and throw it away, the generator does less work and uses a fixed amount of
memory whatever the size of the input. If you need to index it, measure its
length or walk it twice, you need the list.

The habit worth forming is to write the generator version inside `sum`, `any`,
`all`, `min`, `max` and `join`, because those consume exactly once, and to
reach for the list only when the result has a life beyond that line.

## A note on nesting

A comprehension containing a second `for` is a nested loop, and it is subject to
the same multiplication of work described elsewhere on this site. Flattening a
list of lists is a fair use. Comparing every pair of items is not - it is the
same quadratic cost written more compactly, and compactness is the last thing
that helps when something is slow.
""")


extend("f_strings_and_formatting", """
## Why f-strings replaced everything before them

Python has had four ways to build a string with values in it, and the
differences are about where the values sit relative to the text.

Concatenation with `+` scatters the sentence across quotes and plus signs, and
requires `str()` around anything that is not already a string. Percent
formatting moves the values to the end, so reading the sentence means jumping
between the template and the tuple. `str.format` is the same shape with better
syntax. An f-string puts each value exactly where it will appear in the output.

That single property is why the mistakes go away. You cannot pass the arguments
in the wrong order, because there is no separate argument list. You cannot
supply too few, because each slot contains its own expression. And you can read
the line and know what it prints without looking anywhere else.

## What belongs inside the braces

Any expression is legal, which means a great deal is possible and rather less
is wise. A variable, an attribute, a dictionary lookup, a short method call or
a small arithmetic expression all read fine. A nested comprehension or a long
conditional does not: by the time the reader has parsed it they have lost the
sentence it was embedded in.

The rule that holds up is that an f-string should still read as a sentence with
holes in it. When the hole is bigger than the sentence, compute the value on
the line above and give it a name.

## Formatting and correctness

One habit worth keeping: format at the edge, never in the middle. Keep full
precision in your variables and apply `:.2f` only where the value is printed or
written out. Rounding early and then continuing to calculate is how totals stop
matching the numbers above them, and it is a genuinely common source of small,
hard-to-explain discrepancies in reports.
""")


extend("function_arguments", """
## What the signature communicates

A function signature is the part other people read most and change least. It is
worth treating as an interface rather than an accident of how the function grew.

Parameters with no default are requirements: the caller must supply them and the
function cannot work without them. Parameters with defaults are options, and the
default should be the choice that is right most of the time. If you find
yourself writing a default that callers nearly always override, the default is
wrong and it is quietly making every call site longer.

Order matters for reading as much as for the language. Put the thing the
function is about first - the data, the object, the path - and the modifiers
after it. `resize(image, width=800)` reads correctly; `resize(width=800,
image=img)` is legal and reads backwards.

## Passing arguments through

When one function calls another and wants to forward whatever it was given, the
star forms do it without repeating the signature. That is the right tool for
wrappers, decorators and thin adapters, where repeating the parameters would
mean updating two places every time the inner function changes.

It is the wrong tool for a function people call directly. `def process(*args,
**kwargs)` gives the caller no idea what to pass, gives the editor nothing to
complete, and turns a mistake that would have been a clear `TypeError` into a
`KeyError` somewhere deeper. Be explicit at the surface and flexible only where
you are genuinely forwarding.

## Mutable arguments, not just mutable defaults

The default-argument trap gets the attention, but the same underlying fact -
that arguments are passed by reference to the same object - applies to every
call. A function that appends to a list it was given has changed the caller's
list. Sometimes that is the point and should be said in the name: `add_item`,
`update_config`, `sort_in_place`. When it is not the point, copy at the top of
the function or return a new object, and let the caller decide.
""")


add("args_and_kwargs", """
## Where you will actually meet them

Almost every use of `*args` and `**kwargs` in real code falls into one of three
shapes, and recognising them makes the feature far less abstract.

The first is a function that genuinely takes an unknown number of things:
`print`, `max`, `os.path.join`. These are rare to write and common to use.

The second is a wrapper. A decorator, a retry helper, a logging shim - anything
that stands in front of another function and passes the call along. Here the
star forms are not a convenience, they are the only way to write the wrapper
without hard-coding the signature of everything it might wrap.

The third is a subclass extending its parent. `def __init__(self, *args,
extra=None, **kwargs)` accepts whatever the parent accepts, adds one option of
its own, and forwards the rest with `super().__init__(*args, **kwargs)`. This
keeps working when the parent gains a parameter, which is the whole point.

## The cost of being too flexible

A signature of `(*args, **kwargs)` accepts everything, and that is its problem
as well as its purpose. Nobody can tell what the function wants by reading it.
An editor cannot autocomplete the call. A typo in a keyword name no longer
raises a clear `TypeError` about an unexpected argument - it lands silently in
`kwargs` and surfaces later as a missing key, or worse, as a default quietly
being used instead of the value you thought you passed.

So the rule is about position in the system rather than taste. At the surface,
where people call your code directly, name the parameters. In the middle, where
you are forwarding a call you did not construct, use the stars. The further a
function is from a human caller, the more flexibility costs you nothing.

## Reading someone else's signature

When you meet `def f(a, b=1, *args, c, **kwargs)`, read it in the order Python
binds it. `a` is required and positional. `b` is positional with a default.
`args` collects any further positional arguments. `c` comes after `*args`, which
makes it keyword-only and, because it has no default, required by name.
`kwargs` collects the rest.

The one that surprises people is `c`. Anything after `*args` can only be passed
by keyword, whether or not it has a default. That is the mechanism behind
keyword-only parameters, and it is why library authors sometimes write a bare
`*` in a signature: it turns everything after it into a name you have to say
out loud at the call site.
""")


add("variable_scope", """
## Why the rule exists

Deciding local-or-not at compile time looks like an odd choice until you
consider the alternative. If Python worked out scope while running, then whether
a name was local could depend on which branch had executed, and the same line
could mean two different things on two different runs. Instead the compiler
scans the whole function body once: if a name is assigned anywhere in it, that
name is local everywhere in it.

That single rule explains the `UnboundLocalError` that catches everyone. The
read on line one is a read of a local variable, because line five assigns to it,
and the local has no value yet. The error message is precise; it just describes
a decision made before the function ran.

## Closures, and why they are useful

A function defined inside another function can see the enclosing function's
variables, and it keeps seeing them after the outer function has returned. That
combination - an inner function plus the variables it captured - is a closure,
and it is how a function can carry state without a class or a global.

The counter on this page is the small version. The pattern scales to
configuration: a function that builds and returns another function with some
settings already baked in. `make_formatter(currency="GBP")` returns something
you can call many times without repeating the currency.

`nonlocal` exists because assigning inside the inner function would otherwise
create a new local there, exactly as it would at module level. It says "this
name belongs to the function that wraps me", and it is the only way to update
captured state rather than merely read it.

## Globals, and when they stop being harmless

Reading a module-level constant from inside a function is ordinary and fine -
that is what constants are for. Writing to a module-level name from inside a
function is where trouble starts, because the function's behaviour now depends
on what ran before it, and testing it in isolation stops being possible.

The practical test is whether calling the function twice with the same arguments
gives the same answer. If a `global` statement means it does not, the state
probably wants to be a parameter, a return value, or an attribute on an object -
all three of which make the dependency visible in the signature rather than
buried in the body.

## Shadowing builtins

`list`, `dict`, `set`, `id`, `type`, `sum`, `input` and `max` are all ordinary
names that happen to be defined in the builtin scope, and assigning to any of
them inside your code hides the original for the rest of that scope. It is legal
and it produces confusing failures later, usually when something calls `list(x)`
and gets a `TypeError` about your list not being callable.
""")


add("try_and_except", """
## Which exceptions to expect

The instruction to catch specific exceptions is easy to agree with and harder to
follow, because it requires knowing what a piece of code can raise. Three ways
to find out, in order of reliability.

Read the documentation: the standard library is explicit about what its
functions raise, and `int()`, `open()` and `dict` lookups all document theirs.
Run it and see: trigger the failure deliberately once, read the traceback, and
catch what actually appeared. And reason about it: an operation that parses can
raise `ValueError`, one that touches the filesystem can raise `OSError`, one
that indexes can raise `IndexError` or `KeyError`.

Catching `Exception` is the honest middle ground when you genuinely cannot
enumerate them - a plugin boundary, a top-level handler that must not crash the
program - and it is different from a bare `except`, because it still lets
`KeyboardInterrupt` and `SystemExit` through. Those two are how a user stops
your program, and swallowing them is how a program becomes impossible to quit.

## Keep the try block small

A `try` that wraps twenty lines catches errors from all twenty, including ones
you never thought about. If the handler says "could not parse the date", but the
block also contains a database call, then a database failure now reports itself
as a date problem, and the person debugging it starts in the wrong place.

Wrap the line that can fail, and put the follow-up work in `else`. The block
stays honest about what it is handling.

## Failing loudly is usually right

There is a reflex, especially early on, to wrap anything that has ever raised in
a `try` and carry on. It feels defensive. What it actually does is convert a
loud, located failure into a quiet, wrong result that surfaces somewhere else
with no traceback pointing home.

An exception is not automatically a problem to suppress. It is information, and
often the most useful information the program will produce. Handle the ones you
have a real answer for - a missing optional file, a user typing letters into a
number field, a network call worth retrying - and let the rest travel. A crash
in development is a bug report that writes itself.

## Cleanup belongs to `with`

`finally` guarantees that cleanup runs, and for files, locks and connections
there is a better tool: a context manager. `with open(...)` closes the file
whether the block succeeded or raised, without the extra indentation and without
the risk of forgetting. Reach for `finally` when there is no context manager for
what you are doing, and for `with` when there is.
""")


add("classes_and_objects", """
## When a class is the right answer

Not everything should be a class. Python is not a language where you have to
wrap a function in one to run it, and a module full of functions is a perfectly
good design.

The signal that you want a class is data and behaviour travelling together. If
several functions all take the same three arguments, and those three arguments
always change as a group, they are describing one thing that does not have a
name yet. Giving it a name and hanging the functions off it as methods removes
the repetition and makes the relationship explicit.

The opposite signal is a class with one method and no state beyond what that
method was passed. That is a function wearing a costume, and the function is
easier to test, easier to import and easier to read.

## State is the thing to be careful with

An object's attributes are its state, and state is what makes code harder to
reason about, because the answer to "what does this method return" becomes "it
depends what happened earlier". That is not an argument against classes; it is
an argument for keeping state small and obvious.

Two habits help. Set every attribute in `__init__`, even if only to `None`, so
that reading the constructor tells you everything the object holds - attributes
appearing halfway through some other method are how objects become mysterious.
And prefer methods that return new values over methods that quietly mutate the
object, unless mutation is the point and the name says so.

## The underscore convention

Python has no private attributes. A leading underscore - `self._cache` - is a
convention meaning "this is internal, do not rely on it", and nothing enforces
it. That sounds weak and works surprisingly well: it marks the boundary between
what you promise and what you may change, which is all the distinction was ever
for.

A double leading underscore triggers name mangling, which is a different feature
aimed at avoiding clashes in subclasses rather than at privacy. It is rarely
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

That gives you `__init__`, a readable `__repr__` and equality comparison for
free, which is three of the things you would otherwise write by hand and one -
`__repr__` - that people usually skip and then miss the first time they print a
list of them.
""")


add("conditional_expressions", """
## Where it belongs, and where it does not

A conditional expression is at its best when the two values are short, closely
related, and the condition is easy to read. `"pass" if score >= 50 else "fail"`
is a sentence. `compute_full_report(user, opts) if user.is_active and not
user.suspended else default_report()` is not, even though it is legal and does
the same kind of job.

The practical test is whether the line still reads left to right in one pass. If
your eye has to go back to the middle to find the condition, or the line wraps,
the statement form will be clearer and will cost you three extra lines that
nobody has ever regretted.

## In default values and arguments

One place the expression form is genuinely the only option is inside another
expression. Function arguments are the common case:

```python
connect(host, timeout=timeout if timeout else DEFAULT_TIMEOUT)
```

and so are dictionary values, list elements and f-string slots. You cannot put
an `if` statement in any of those, so if the choice has to happen there, this is
how it happens.

Worth noticing in that example: `timeout if timeout else DEFAULT` has the same
falsy-value problem as `or`. If zero is a legitimate timeout meaning "do not
wait", this discards it. `timeout if timeout is not None else DEFAULT` is the
version that survives contact with real data.

## Nesting, and the readable alternative

Chained conditional expressions are the classic overreach, and the reason is
that they invert how people read a decision. A reader looking for the default
case has to scan to the very end of the line, and adding a band means editing
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

The bands are now data, which means they can be changed, tested and displayed
without touching the logic. That is usually the real win, and it is easy to
miss while arguing about one-liners.
""")


add("match_and_case", """
## Why it was added

Python resisted a switch statement for decades on the grounds that a chain of
`if`/`elif` already did the job, and for comparing a value against a few
constants that argument still holds. `match` was not added to replace those.

It was added for structural pattern matching: inspecting the *shape* of data and
pulling it apart in the same step. The code it replaces is a stack of
`isinstance` checks, key lookups and length tests, written in a specific order,
where getting the order wrong or forgetting a check produces a bug that only
appears on unusual input. That pattern shows up constantly in anything that
handles parsed JSON, events, commands or syntax trees.

Once you see it as "destructure and dispatch" rather than "switch", the design
choices stop looking strange.

## Patterns you will use

Literal patterns match constants. Sequence patterns like `[a, b]` or
`[first, *rest]` match lists and tuples of the right shape and bind the parts.
Mapping patterns like `{"type": "click", "x": x}` match dictionaries that
*contain* those keys - extra keys are allowed, which is what makes them useful
against real payloads that carry more than you care about.

Class patterns match an instance and can pull attributes out of it:
`case Point(x=0, y=y)` matches a Point on the y-axis and binds `y`. Combined
with a guard, that covers a surprising amount of dispatch logic in one readable
block.

## The two rules to remember

A bare name captures rather than compares, and it matches everything. If you
want to compare against a constant you have stored somewhere, it must be a
dotted name - `case Status.OK` - or a literal. This is the single most common
`match` bug, and the failure mode is silent: the first such case swallows every
value and the ones below it never run.

And `match` is not exhaustive. If nothing matches and there is no `case _`,
the statement simply does nothing and execution continues. Coming from
languages where the compiler insists on exhaustiveness, that is worth
remembering, because a missing case here is a quiet no-op rather than an error.

## Version, and whether to use it

`match` requires Python 3.10. If your code has to run on anything older, the
`if`/`elif` version is the only option, and for two or three literal
comparisons it is the better one regardless: shorter, universally understood,
and with none of the capture-pattern sharp edges.
""")


add("loop_else", """
## The name is the whole problem

Nothing about the word "else" suggests "if the loop was not broken out of", and
that mismatch is why the feature has a reputation for being confusing rather
than for being useful. The behaviour itself is simple and has no edge cases.

Guido van Rossum has said the keyword was a mistake and that something like
`nobreak` would have been clearer. Reading it that way in your head is genuinely
all it takes; the confusion disappears immediately and does not come back.

## The shape it belongs to

`for/else` fits one specific shape: a search that must report failure. Loop over
candidates, `break` when you find one, and the `else` is the "we got to the end
without finding anything" branch.

That shape appears more often than it first seems - looking up a record,
validating that no item breaks a rule, testing divisibility, scanning for a
delimiter. In each case the alternative is a boolean flag that exists only to
carry one bit of information past the end of the loop, and every flag is a
chance to forget to set it or to check it in the wrong place.

## When not to use it

If the loop has no `break`, the `else` always runs and is therefore pure
decoration - it means exactly the same as putting the code after the loop, but
makes a reader stop and work that out. Delete it.

If the function can simply `return` from inside the loop, that is usually
clearer than either version, because the "not found" case becomes the last line
of the function rather than an attached block:

```python
def find(items, target):
    for item in items:
        if item == target:
            return item
    return None
```

Most searches inside a function are better written this way, which is part of
why `for/else` stays uncommon even among people who know it.

## Knowing it matters more than using it

The reason to learn this feature is that you will read it. It appears in the
standard library and in other people's code, and an unfamiliar construct in
someone else's loop is exactly the kind of thing that makes a reader guess.
Guessing wrong here is easy, because the plain-English reading of "else" is the
opposite of the truth in the case people usually check first - the empty
sequence, where the else still runs.
""")


add("nested_conditionals", """
## Guard clauses, and why they read better

A nested conditional builds a staircase: each condition indents the next, and by
the third level the code that actually does something is a long way from the
left margin. The alternative is to handle the exceptional cases first and leave
early, so the main path stays at the top level.

```python
def borrow(user, book):
    if not user.active:
        return "membership inactive"
    if user.fines > 0:
        return "clear your fines first"
    if not book.available:
        return "already on loan"
    return "enjoy the book"
```

Every line reads as one rule. Adding a rule is one line in the middle; removing
one is deleting a line. The nested version needs re-indenting for either.

The reason this works is that it separates "reasons you cannot" from "what
happens when you can". Those are different kinds of statement, and the staircase
version tangles them together, which is why it gets harder to read exactly as
the number of rules grows.

## When nesting is genuinely right

Guard clauses suit functions, because `return` is what makes them possible.
Inside a loop or a block where you cannot return, the staircase is sometimes
unavoidable - though `continue` plays the same role in a loop that `return`
plays in a function, and is under-used for it.

Nesting is also right when the conditions are genuinely dependent: when the
second question only makes sense if the first was true. `if user is not None:`
followed by `if user.active:` is not a staircase to flatten, it is two questions
where the second would raise without the first.

## Combining with and or

Two shallow conditions can often become one:

```python
if user.active and not user.fines:
```

This is clearer than nesting when the combination is what you mean, and worse
than nesting when you need different responses to each failure - as soon as you
want to tell the user *which* rule stopped them, the conditions have to be
separate again.

Both `and` and `or` short-circuit, which is what makes `if user is not None and
user.active` safe: the second half is never evaluated when the first is false.
That ordering is load-bearing, and swapping the halves turns a working check
into an `AttributeError`.

## Depth as a design signal

Three levels of nested conditions inside a loop inside a function is usually not
a formatting problem, it is a sign that the function is making several different
decisions and would be clearer as two or three named functions. The indentation
is doing you a favour by making that visible.
""")


add("enumerate_function", """
## What it replaces, and why that matters

Before `enumerate`, keeping a counter alongside a loop meant one of two things:
initialising `i = 0` and remembering to increment it at the bottom of the body,
or looping over `range(len(items))` and indexing back into the list.

Both work. Both have a specific failure. The manual counter breaks the moment
the body has an early `continue` above the increment, and the bug is invisible -
the loop still runs, the numbers are just wrong. The `range(len(...))` version
puts an index between you and the value, so every use is `items[i]` rather than
`item`, which is noisier and offers an off-by-one error where none needs to
exist.

`enumerate` removes the counter entirely. There is nothing to forget to
increment and nothing to index.

## The start argument

```python
for n, line in enumerate(lines, start=1):
    print(f"{n}: {line}")
```

Line numbers, question numbers, ranked results and anything else a human reads
usually start at one. Passing `start=1` is better than writing `n + 1` inside
the body, because it states the intent once at the top rather than repeating an
adjustment everywhere the number is used - and it means you cannot apply the
adjustment in one place and forget it in another.

## It works on anything iterable

`enumerate` is not a list feature. It works on strings, files, generators,
dictionary views and anything else you can loop over, and it does not build a
list to do it - it yields pairs as the loop asks for them.

That makes `for n, line in enumerate(f)` a perfectly good way to number the
lines of a file too large to hold in memory, which the `range(len(...))` form
cannot do at all, because there is no length to take.

## Unpacking is doing the work

`enumerate` yields tuples. Writing `for n, item in ...` is tuple unpacking, the
same feature that makes `for k, v in d.items()` work. Occasionally you will see
it left packed:

```python
for pair in enumerate(items):
    print(pair)      # (0, 'a')
```

which is legal and rarely what you want. The unpacked form is the point: it
gives both halves a name at the top of the loop, so the body never has to say
`pair[0]`.

## When you do not need it

If you never use the index, do not ask for one. `for item in items` is the
correct loop, and `for i, item in enumerate(items)` with `i` unused is noise
that a linter will flag. The convention when you need one and not the other is
to name the unused variable `_`.
""")


add("zip_function", """
## Walking two things at once

The job `zip` does is small and comes up constantly: you have two or more
sequences whose positions correspond, and you want to work with matching items
together. Names and scores, keys and values, inputs and expected outputs,
columns and headers.

Without it, the loop goes through indices and reaches back into both lists,
which reintroduces exactly the off-by-one risk that looping over items avoids.
With it, each iteration hands you one item from each and the indices disappear.

## Stopping at the shortest

`zip` stops when its shortest input runs out. This is a genuine design decision
rather than an oversight, and it cuts both ways.

It is convenient when you deliberately pair a finite list against an infinite
generator, because you get exactly as many pairs as the finite side has. It is
dangerous when the two lists were supposed to be the same length and are not,
because the extra items are dropped in silence and the program produces a
short, plausible, wrong answer.

Since Python 3.10 you can ask for the check:

```python
zip(a, b, strict=True)     # ValueError if the lengths differ
```

Use it whenever equal lengths are an assumption rather than a coincidence. If
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

The star spreads the list of pairs into separate arguments, and `zip` then
takes one item from each, which recombines them by position. The results are
tuples rather than lists, which matters only if you intend to mutate them.

## It is lazy

Like `map` and `filter`, `zip` returns an iterator rather than a list. Printing
it shows an object, and consuming it twice gives nothing the second time. In a
`for` loop that is invisible and ideal; the moment you want to keep the result,
wrap it in `list()`.
""")


add("sorted_with_key", """
## What key actually does

`key` takes a function, calls it once on every element, and sorts by whatever
comes back. The original items are what you get out - the key is used for
comparison only, and then discarded.

That single sentence explains most of what people find confusing. The function
is not a comparison between two items; it is a transformation of one item into
something sortable. So `key=len` sorts by length, `key=str.lower` sorts
case-insensitively, and `key=lambda r: r["score"]` sorts records by a field
without changing them.

It also explains why `key` is fast. Each element is transformed once, not once
per comparison, which is why this is preferred over the old `cmp` approach that
Python removed in version 3.

## Sorting by more than one thing

Return a tuple, and the sort compares position by position:

```python
sorted(people, key=lambda p: (p.surname, p.forename))
```

Surname first, forename only where surnames match. This extends to as many
levels as you need, and it is far easier to get right than sorting repeatedly.

Mixing directions is the awkward case, because `reverse=True` applies to the
whole sort. For numbers, negating one component works: `key=lambda p: (-p.score,
p.name)` gives highest score first, then name ascending. For strings there is no
negation, and the usual answer is two stable sorts, applied least significant
first.

## Stability, and why it is useful

Python's sort is stable: items that compare equal keep their original order.
That is what makes the two-pass approach work at all, and it is a guarantee you
can rely on rather than an implementation detail.

## sorted versus .sort

`sorted(x)` returns a new list and leaves the original alone. `x.sort()` reorders
in place and returns `None`. The second is the source of a small, common bug:

```python
names = names.sort()      # names is now None
```

The method returns `None` deliberately, as a signal that it mutated rather than
produced. Every in-place method in the standard library does the same -
`reverse`, `append`, `extend`, `update` - and once you know the convention, the
`None` stops being a surprise and starts being a hint.

## The same key everywhere

`key` is not a sorting feature. `min`, `max` and `itertools.groupby` all take it
and mean the same thing by it, so `max(people, key=lambda p: p.score)` finds the
top scorer without sorting anything - which is both faster and clearer than
sorting and taking the last element.
""")


add("range_step", """
## Counting backwards correctly

A negative step is where `range` trips people, and the reason is that the stop
value is still exclusive. Counting down to and including zero means stopping at
`-1`:

```python
range(3, -1, -1)      # 3 2 1 0
range(3, 0, -1)       # 3 2 1   - zero is missed
```

The rule has not changed - `range` never includes its stop - but with a
descending sequence the exclusive end is below the last value you want rather
than above it, which is exactly the sort of thing that reads correctly and
behaves otherwise.

An empty range is not an error. `range(0, 5, -1)` produces nothing at all,
because the start is already past the stop in the direction of travel. A loop
over it runs zero times and says nothing, so a wrong sign shows up as "the loop
did not happen" rather than as an exception.

## When you want to walk something backwards

For iterating a sequence in reverse, `reversed()` says what it means and needs
no arithmetic:

```python
for item in reversed(items):
```

`items[::-1]` also works and builds a reversed copy first, so it costs memory
proportional to the sequence. `range(len(items) - 1, -1, -1)` works too and is
the version most likely to contain an off-by-one. Prefer `reversed` unless you
specifically need the indices.

## range is not a list

`range(10_000_000)` is instant and takes a few dozen bytes, because it stores
only start, stop and step and computes each value on demand. This is why it can
be enormous, and why printing one shows `range(0, 10)` rather than the numbers.

It is not a generator, though - it can be iterated repeatedly, it knows its own
length, it supports indexing, and `x in range(...)` is a fast arithmetic check
rather than a scan. That combination makes it more useful than a plain generator
and cheaper than a list.

## Slicing shares the same idea

The third argument to a slice is the same step, with the same rules, which is
why `[::2]` takes every second item and `[::-1]` reverses. Learning the
behaviour once covers both, and the exclusive-stop rule is what makes
`a[:n]` and `a[n:]` fit together with no gap and no overlap.
""")


add("dict_and_set_comprehensions", """
## Inverting and filtering a mapping

Two jobs come up so often that the comprehension form is worth memorising as an
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

## Dict comprehensions and duplicate keys

A dict comprehension has no duplicate protection. If the key expression produces
the same key twice, the later value overwrites the earlier one and nothing is
reported. This is the same behaviour as a dict literal with a repeated key, and
it is worth remembering whenever the key is computed rather than taken directly
from a unique field.

If you need to know about collisions, build with a loop and check, or count with
`collections.Counter` first.

## Set comprehensions, and what they are for

A set comprehension is a comprehension whose result must be unique, and the two
common uses are extracting a distinct field and computing a distinct derived
value:

```python
{r["city"] for r in rows}
{len(w) for w in words}
```

Both could be written as `set([...])` around a list comprehension. The direct
form avoids building the intermediate list, and says up front that uniqueness is
the point rather than an afterthought.

## Telling the three apart

The bracket decides everything, and the difference between a dict and a set
comprehension is one colon:

```python
[x for x in it]        # list
{x for x in it}        # set
{x: f(x) for x in it}  # dict
(x for x in it)        # generator
```

This is also why `{}` is an empty dict and not an empty set - the dict form
claimed the braces first, and an empty one has no colon to distinguish it.

## When a loop is still better

The same limit applies as to list comprehensions. One transformation, one
optional filter, one line: use the comprehension. As soon as the value needs
several steps, a `try`, or a condition on the key as well as the value, the loop
version is easier to read and much easier to change later.
""")


add("conditional_comprehensions", """
## Two conditionals, two positions, two jobs

This is the single point worth being certain about, because the two forms look
similar, sit in the same expression, and do different things.

The trailing `if` filters. It decides whether an item appears at all, so the
result can be shorter than the input:

```python
[n for n in nums if n > 0]
```

The leading `if`/`else` chooses a value. Every item still appears, so the result
is always the same length as the input:

```python
[n if n > 0 else 0 for n in nums]
```

A useful way to remember it: the front of a comprehension is the expression that
produces each item, and an expression must always produce something - which is
why the `else` is compulsory there and forbidden at the end.

## Combining both

They can appear together, and the reading order is worth stating explicitly:

```python
["high" if n > 100 else "low" for n in nums if n is not None]
```

The trailing filter runs first, deciding which items survive. The leading
conditional then runs on each survivor, deciding what it becomes. Filter, then
map - even though the map is written first.

Once a line contains both, it is close to the limit of what reads well, and a
second filter or a nested loop pushes it past.

## Filtering out None before working with values

The combination above is not a contrived example; it is the common shape when
data has gaps. Guarding in the filter means the expression at the front never
sees a `None`, which lets it do arithmetic or call methods without a defensive
check:

```python
[r["score"] * 2 for r in rows if r["score"] is not None]
```

Written the other way round - a conditional expression testing for `None` on
every item - the line is longer and still produces an entry for rows that had no
score, which is usually not what was wanted.

## Multiple conditions

Several filters can be chained, and they behave as `and`:

```python
[n for n in nums if n > 0 if n % 2 == 0]
```

which is identical to writing `if n > 0 and n % 2 == 0`. The chained form
occasionally reads better when the conditions test unrelated things; the
combined form is more familiar. Neither is wrong, and consistency within a file
matters more than the choice.

## Where to draw the line

A comprehension carrying a filter, a conditional expression and a nested loop is
a program written on one line. It will be correct and it will cost every future
reader - including you - a slow minute. The loop version is four lines that
never need decoding, and no reviewer has ever objected to it.
""")


add("type_conversion", """
## Conversion is not the same as checking

`int("42")` converts. `isinstance(x, int)` checks. Reaching for the wrong one is
common, and the distinction matters because conversion can fail loudly while a
check never does.

The Python habit is to attempt the conversion inside a `try` rather than to
validate first with a regular expression or a series of `isdigit` calls. The
attempt is the authoritative test - it knows about signs, whitespace, underscores
in numeric literals and every other detail your hand-written check would miss.

```python
def as_int(text, default=None):
    try:
        return int(text)
    except (TypeError, ValueError):
        return default
```

Catching both matters: `ValueError` for text that is not a number,
`TypeError` for `None` or a list arriving where a string was expected.

## The float trap

`int("3.9")` raises, which surprises people who expect it to truncate. The
string is not an integer literal, so the conversion refuses rather than
guessing. `int(3.9)` on an actual float does truncate, toward zero, so `int(-3.9)`
is `-3` rather than `-4`.

If you want rounding rather than truncation, `round` is the function, and it has
its own surprise: it rounds halves to the nearest even number, so `round(2.5)` is
2 and `round(3.5)` is 4. That is deliberate - it avoids the upward bias you get
from always rounding halves up - and it is worth knowing before you conclude
something is broken.

Converting a string that might contain a decimal is a two-step:
`int(float("3.9"))`.

## Truthiness is a conversion too

`bool(x)` follows the same rules as `if x`, which means empty containers, zero
and `None` all convert to `False`. That makes `bool` occasionally useful for
normalising a value, and it makes `bool("False")` a well-known trap: the string
is non-empty, so it is `True`. Parsing a boolean from text needs an explicit
mapping, not a conversion.

## Implicit conversion, and where Python refuses

Python converts numeric types automatically when it can do so without losing
information: `1 + 2.0` gives `3.0`, and comparing an int with a float works as
expected. It refuses to convert between strings and numbers, which is why
`"3" + 4` raises rather than guessing whether you meant `7` or `"34"`.

That refusal is a feature. Languages that do guess produce a class of bug where
a number arrives as a string from a form or a file and everything continues to
work until the arithmetic silently becomes concatenation. In Python that fails
at once, at the line responsible.
""")


add("none_and_truthiness", """
## Absent is not the same as empty

`None` means "there is no value here". An empty string, an empty list and zero
are all values - they just happen to be falsy. Treating the two as
interchangeable is the source of a whole family of quiet bugs.

```python
if not name:          # true for None AND for ""
if name is None:      # true only for None
```

The first is right when you mean "nothing useful to show". The second is right
when you mean "this was never set", and the difference matters the moment an
empty value is legitimate: a comment field left blank, a quantity of zero, a
list with nothing in it yet.

The clearest example is a count. `if not count:` treats zero as missing, so a
genuine result of zero takes the "no data" branch. `if count is None:` does not.

## Why `is` and not `==`

`None` is a singleton: there is exactly one of it in a running program, so
identity and equality give the same answer for it, and identity is both faster
and impossible to override. A class can define `__eq__` to make `x == None`
return anything it likes; nothing can make `x is None` lie.

That is the whole reason the convention exists, and the same reasoning applies
to `True` and `False`, although comparing to those at all is usually redundant -
`if flag:` says it better than `if flag is True:`.

## Functions that return None

A function with no `return` returns `None`, and so does one whose `return` has no
value. This is why forgetting to return a result produces `NoneType` errors
somewhere further along rather than at the function itself.

The in-place methods do it deliberately - `sort`, `reverse`, `append`, `update`
all return `None` to signal that they mutated the object rather than producing a
new one. `x = x.sort()` is the classic result, and the `None` is the library
telling you it did the work already.

## Defaults that respect zero

The `or` shortcut for defaults is common and slightly wrong:

```python
timeout = given or 30          # 0 becomes 30
timeout = 30 if given is None else given
```

The first discards any falsy value, including a deliberate zero or an empty
string. The second only fills in when the value is genuinely absent. When the
domain includes zero, empty text or an empty list as real values - and it usually
does - the second form is the one that behaves.

## Checking emptiness

For containers, the truthiness test is idiomatic and preferred:

```python
if not items:            # yes
if len(items) == 0:      # works, but noisier
```

The exception is when `items` might be `None`, because `not None` is also true.
Then you need to say which case you mean.
""")


add("string_methods", """
## Cleaning input, in order

Text arriving from a person or a file usually needs the same three steps, and
the order is worth doing deliberately.

Strip first, because trailing whitespace and newlines break comparisons in ways
that are invisible on screen. Normalise case next, when the comparison should
ignore it. Only then split or compare.

```python
line.strip().lower().split(",")
```

Chaining works because each method returns a new string, which is the same
immutability that makes forgetting to assign such a common mistake elsewhere.

For case-insensitive comparison across languages, `casefold` is stricter than
`lower` and handles a handful of cases `lower` does not. For English-only text
the difference never shows up.

## Searching without exceptions

Three ways to ask whether something appears in a string, and they differ in what
they give back:

```python
"cat" in text            # True or False
text.find("cat")         # index, or -1
text.index("cat")        # index, or raises ValueError
```

Use `in` when you only want to know. Use `find` when you want the position and
absence is expected. Use `index` when absence is a bug and you want it to say so.
Choosing `find` and then forgetting that `-1` is falsy in a different way from
`0` is a small classic: `if text.find("cat"):` is true when the match is at
position one and false when it is at position zero.

## Splitting text into lines and fields

`splitlines()` handles the newline variants that `split("\\n")` gets wrong on
files written on another operating system. `partition` splits once and always
returns three pieces, which avoids the length check that `split` with a maxsplit
requires:

```python
key, sep, value = line.partition("=")
```

If the separator was absent, `sep` is empty and `value` is empty, and the
unpacking still works - no `IndexError`, no branch.

## Building strings in a loop

Repeated concatenation inside a loop creates a new string every time, because
strings cannot be modified in place. For a handful of pieces that is irrelevant.
For thousands it is genuinely slow, and the fix is to collect and join once:

```python
parts = []
for row in rows:
    parts.append(format(row))
text = "\\n".join(parts)
```

This is the same reason `join` exists as a method on the separator: it is
building the whole result in one pass, which it can only do if it is given all
the pieces at once.
""")


add("input_and_output", """
## Validating in a loop

A single `int(input())` is fine in an example and unusable in a program a person
will actually operate, because the first typo ends it. The shape that works asks
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
error message repeats what was typed, so the person can see the typo. And the
loop only exits on success, so the caller can rely on getting a number.

## Sentinel values and ending a loop

When you do not know how many values are coming, a sentinel ends the input:

```python
while True:
    line = input("value (blank to finish): ").strip()
    if not line:
        break
    values.append(line)
```

An empty line is the usual choice because it is what pressing enter produces. If
blank is a legitimate value, pick something explicit like `done` and say so in
the prompt.

## Reading from a pipe rather than a person

`input` reads a line from standard input, and standard input is not always a
keyboard. If your program is run as `cat data.txt | python script.py`, the same
`input` calls read lines from the file, and an `EOFError` is raised when it runs
out - which is the same error you get if someone presses Ctrl-D.

That is worth handling in anything that might be piped:

```python
try:
    line = input()
except EOFError:
    line = None
```

It is also why this page's first program raises in the browser: there is no
standard input attached at all.

## Printing for people versus printing for programs

Output aimed at a person wants formatting, alignment and separators.
Output aimed at another program wants to be trivially parseable - one record per
line, a consistent separator, no decorative headers.

Mixing the two is what makes a script hard to use in a pipeline. If a program
might be consumed by another, keep the data on standard output and put the
progress messages, prompts and warnings on standard error:

```python
import sys
print("processing...", file=sys.stderr)
print(result)
```

Then `script.py > out.txt` captures exactly the results and leaves the chatter
on screen.
""")


add("slicing_step_negatives", """
## Why the stop is excluded

Excluding the stop looks arbitrary until you notice what it buys. The length of
`a[i:j]` is exactly `j - i`, with no adjustment. `a[:n]` and `a[n:]` split a
sequence with nothing lost and nothing repeated. And `a[i:i]` is empty, which is
the sensible answer for a zero-width slice.

Every one of those becomes an off-by-one special case if the stop is inclusive.
The convention is the same one `range` uses, which is why the two compose so
predictably.

## Slicing does not raise

`a[5:99]` on a three-item list returns what exists, and `a[99:]` returns an empty
list. No exception either way. That is convenient when you are taking "up to
ten" of something and there might be fewer.

It is also a place bugs hide, because an empty slice looks like legitimate data.
A function that slices with a computed index and returns nothing has not
necessarily worked correctly - it may have computed the wrong index and been
silently forgiven. When the index must be valid, index rather than slice, and
let `IndexError` tell you.

## Copies, views and strings

A slice of a list is a shallow copy: a new list holding the same objects. That is
why `b = a[:]` is a copy idiom, and why changing `b[0] = x` leaves `a` alone
while `b[0].append(x)` does not - the outer list is new, the items are shared.

A slice of a string is a new string, because strings are immutable and there is
nothing else it could be. That makes `s[::-1]` a genuine copy in reverse, which
matters only when the string is very large.

## Assigning into a slice

Lists let you assign to a slice, and the replacement need not be the same length:

```python
nums[1:3] = ["a", "b", "c"]     # two items become three
del nums[1:3]                   # or remove them entirely
```

This changes the list in place, including its length, and it is the one part of
slicing that mutates rather than copies. It is worth knowing mainly so that you
recognise it in other people's code, and because it explains why `a[:] = b`
replaces the contents of `a` while `a = b` merely rebinds the name.

## Step with a negative start and stop

Combining a negative step with negative indices is where slices become
write-only. `a[-2::-1]` is "start at the second-to-last, walk backwards to the
beginning" - correct, and not obvious on sight. When a slice needs a comment,
`reversed()` and an explicit loop usually say it better.
""")


add("mutability_and_aliasing", """
## Which types are which

The distinction is worth memorising as a list, because it explains behaviour
across the whole language.

Immutable: `int`, `float`, `bool`, `str`, `bytes`, `tuple`, `frozenset`, `None`.
Mutable: `list`, `dict`, `set`, `bytearray`, and nearly every class you write
yourself.

Every rule about aliasing, dictionary keys, default arguments and copying falls
out of that split. Immutable objects can be shared without risk, which is why
they can be dictionary keys and set members and safe defaults. Mutable objects
cannot.

## Equality and identity

Two separate questions, and Python has an operator for each:

```python
a == b      # do they hold the same value?
a is b      # are they the same object?
```

Two lists with identical contents are equal and are not identical. Confusing the
two produces code that works by accident, particularly with small integers and
short strings, which Python caches: `x = 256; y = 256; x is y` is often `True`,
and the same test with `257` is often `False`. That is an implementation detail
and precisely why `is` should be reserved for `None` and for genuine identity
questions.

## Passing to functions, stated precisely

Python is neither pass-by-value nor pass-by-reference in the C sense. What is
passed is a reference to the object, by value - the function gets its own name
pointing at the caller's object.

So the function can mutate the object and the caller sees it, and the function
can rebind its own name and the caller does not. Both facts come from the same
mechanism, and once you hold "names point at objects" in your head, no further
rule is needed.

## Defensive copies

When a function stores something it was given, it is worth thinking about who
else holds it:

```python
class Basket:
    def __init__(self, items):
        self.items = list(items)     # our own copy
```

Without the copy, the caller's list and the object's list are the same list, and
a later change on either side surprises the other. Copying at the boundary costs
one call and removes an entire category of bug where two parts of a program share
state neither of them knows about.

The same reasoning applies on the way out: returning `self.items` directly hands
callers a handle on your internals. Returning `list(self.items)` or a tuple keeps
the boundary intact.
""")


add("shallow_and_deep_copy", """
## Copying an object, not just a container

`copy.copy` works on your own classes too, and it copies the same way: a new
object whose attributes point at the same values. If an attribute is a list, both
copies share it.

Classes can control this. Defining `__copy__` and `__deepcopy__` lets an object
say how it should be duplicated, which matters when it holds something that
should not be copied at all - an open file, a database connection, a lock. In
practice you rarely write these, but knowing they exist explains why copying some
library objects behaves in ways a plain attribute copy would not.

## Why deepcopy is slower than it looks

`deepcopy` walks the entire object graph, duplicates every mutable thing it
finds, and keeps a record of what it has already copied so that shared references
stay shared and cycles do not become infinite recursion.

That bookkeeping is why it is slow on large structures, and it is also why it is
correct in cases a hand-written recursive copy usually gets wrong. If you have
ever written a recursive copy helper and hit `RecursionError` on data that
referred back to itself, that is the problem `deepcopy` already solved.

## Cheaper alternatives

Often the goal is not a copy at all, but a modified version of something,
without disturbing the original. Several types offer that directly:

```python
new_config = {**defaults, **overrides}    # merged, both untouched
new_items = [*items, extra]               # extended, original untouched
new_point = point._replace(x=5)           # namedtuple
```

Each of these produces a new outer object and leaves the inputs alone, at the
cost of a shallow copy rather than a deep one - which is exactly right when the
contents are immutable.

If the contents are mutable and you find yourself needing `deepcopy` frequently,
that is often a signal that the structure would be better as immutable data:
tuples, frozensets, or small classes that return new instances rather than
mutating themselves.

## A practical rule for configuration

Nested dictionaries loaded from JSON or YAML are the single most common place
this bites, because the nesting is the whole point and `.copy()` looks like it
did the job.

If a function takes a config dict and changes anything inside it, either it
should be documented as doing so, or it should deepcopy first. Silently editing a
nested value in a structure the caller still holds is the sort of bug that gets
diagnosed as "the settings randomly change", which is a long way from where the
mutation actually happened.
""")


add("dictionary_methods", """
## Views, and why they are not lists

`keys()`, `values()` and `items()` return views: live windows onto the
dictionary rather than snapshots of it. Add a key and every existing view
reflects it immediately, because a view holds no data of its own.

That is efficient and it has one consequence worth knowing. Modifying a
dictionary while looping over one of its views raises `RuntimeError:
dictionary changed size during iteration`. The fix is to iterate over a snapshot:

```python
for key in list(d):
    if should_remove(key):
        del d[key]
```

`list(d)` copies the keys first, so the loop is walking its own list and the
dictionary is free to change underneath.

Key and item views also behave like sets, which is occasionally very handy:
`d1.keys() & d2.keys()` gives the keys both dictionaries share, without a loop.

## Order is guaranteed now

Since Python 3.7, dictionaries keep insertion order as a language guarantee
rather than an implementation accident. That is why `dict.fromkeys(items)` is the
standard order-preserving deduplication, and why iterating a dictionary produces
a stable, predictable sequence.

It does not make a dictionary a substitute for a sorted structure - the order is
insertion order, not sorted order - but it does mean you can rely on what you
put in first coming out first.

## Choosing between get, setdefault and defaultdict

Three tools that overlap, and the distinction is about what should happen when a
key is missing.

`get` reads and never writes. Use it when a missing key has a sensible fallback
and you do not want to add anything to the dictionary.

`setdefault` reads and writes: it inserts the default when the key is absent and
returns whatever is now there. Use it for the grouping idiom, where you want the
list to exist so you can append to it.

`defaultdict(list)` moves that behaviour into the dictionary itself, so every
missing key springs into existence on access. Use it when *every* access should
create a default. Its downside is exactly that: a typo'd key lookup silently
creates an empty entry instead of raising, which can mask a bug.

## Merging

```python
merged = {**defaults, **overrides}     # 3.5+
merged = defaults | overrides          # 3.9+
defaults |= overrides                  # in place
```

Later keys win in all three. This is the clean way to layer configuration, and
it beats a loop of `if key not in d` conditions because the precedence is stated
by the order of the operands rather than buried in the logic.
""")


add("nested_data_structures", """
## The shape of data that arrives

Most real data is a list of records, and most records are dictionaries. API
responses, parsed JSON, CSV rows read with `DictReader`, database results - all
the same shape.

Recognising this makes the code predictable. The outer loop takes records; a key
lookup takes a field; an inner loop takes a list-valued field. Three moves cover
almost everything, and they compose to any depth.

The depth itself is the thing to keep an eye on. Two levels are easy to hold in
your head. Four levels of mixed lists and dictionaries is where a small helper
function - `def city_of(record):` - pays for itself immediately, because it gives
the path a name and one place to fix when the shape changes.

## Modifying nested structures

Reading a nested value is safe; writing one is where aliasing matters. If you
copied the outer list shallowly and then edit a dictionary inside it, both copies
change, because they hold the same dictionaries.

That is not a reason to deepcopy everything. It is a reason to decide
deliberately: either the structure is shared and everyone knows it, or you take a
deep copy at the boundary where it enters your code.

## Flattening and grouping

The two transformations that come up constantly are inverses of each other.

Flattening turns a nested structure into a flat one - all languages anyone knows,
all items across all orders - and a nested comprehension or `itertools.chain` does
it in a line.

Grouping turns a flat list into a nested one, keyed by some field.
`setdefault` or `defaultdict(list)` is the idiom, and it is worth writing out
once until it feels automatic, because half of the reporting code anyone ever
writes is a grouping followed by an aggregation.

## JSON is the same shape

`json.load` produces exactly these structures - dictionaries, lists, strings,
numbers, booleans and `None` - which is why working with parsed JSON needs no new
skills beyond this page. `json.dumps(data, indent=2)` prints them back readably,
and is the fastest way to understand something you have just fetched.

The one asymmetry: JSON object keys are always strings. A dictionary keyed by
integers survives the round trip as string keys, which is a small surprise that
shows up when a lookup that worked before saving fails after loading.
""")


add("lambda_map_filter", """
## Why the style guide discourages naming a lambda

`square = lambda n: n * n` works and is discouraged, for a concrete reason
rather than an aesthetic one. A `def` gives the function a name in its own
metadata, so a traceback says `square` instead of `<lambda>`. When something
raises three frames deep, that difference is the gap between reading the
traceback and guessing.

`def` also allows a docstring, type annotations, multiple statements and a
default argument - all of which you will eventually want, and adding any of them
means converting anyway.

The rule that follows: if it needs a name, it needs a `def`.

## Closures in a loop

A classic trap, and it looks like a lambda problem while actually being a scope
one:

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])      # [2, 2, 2]
```

Every lambda captured the *variable* `i`, not its value at the time, and by the
time they run the loop has finished with `i` at 2. Binding the value explicitly
as a default argument fixes it:

```python
funcs = [lambda i=i: i for i in range(3)]   # [0, 1, 2]
```

This is worth recognising because it appears whenever functions are built in a
loop - event handlers, callbacks, partial applications - and the symptom is
always the same: they all behave like the last one.

## functools.partial

When the goal is to fix some arguments of an existing function, `partial` says it
more directly than a lambda:

```python
from functools import partial
to_int = partial(int, base=16)
```

It also produces something introspectable and picklable, which a lambda is not -
relevant the moment multiprocessing is involved, because lambdas cannot be sent
to worker processes.

## Reading functional code

`map` and `filter` are worth knowing well even if you write comprehensions,
because a great deal of existing Python uses them, and because they compose with
the rest of `itertools`. Being able to read `filter(None, values)` - which drops
falsy items, using `None` as "no function" - is more useful than an opinion about
whether you would have written it that way.
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
covers the common case where you want the whole file and do not need to stream
it. For anything iterative, `data.open()` gives you the same file object `open`
would.

`Path` also carries the questions you would otherwise ask the `os` module:
`.exists()`, `.suffix`, `.stem`, `.parent`, `.glob("*.txt")`.

## Encoding is not optional in practice

Text mode decodes bytes into a string using an encoding, and if you do not name
one, Python uses the platform default. That default differs between machines,
which is how a script that works on one computer produces `UnicodeDecodeError` on
another, with data that has not changed.

Naming it removes the whole class of problem:

```python
open(path, encoding="utf-8")
```

If you are handling files you did not create and cannot assume, `errors="replace"`
lets you read something rather than crashing, at the cost of substituting the
bytes it could not decode.

## Writing safely

Writing directly over the only copy of a file has an obvious failure mode: if the
program dies halfway, the original is gone and the replacement is incomplete. The
standard remedy is to write beside it and rename:

```python
tmp = path.with_suffix(".tmp")
tmp.write_text(new_content, encoding="utf-8")
tmp.replace(path)
```

`replace` is atomic on the same filesystem, so a reader sees either the old file
or the new one and never a half-written one.

## Binary mode

Adding `b` - `open(path, "rb")` - skips decoding and gives bytes. That is what
you want for images, archives, and anything you are copying rather than reading.
The mistake in the other direction is more common: opening a text file in binary
mode and then being puzzled that comparisons against strings all fail, because
`b"abc"` and `"abc"` are different types that never compare equal.
""")


add("modules_and_import", """
## What a module actually is

A module is a file, and importing it runs that file top to bottom, once. Every
function definition, class definition and top-level statement executes at that
moment, and the resulting names become attributes of the module object.

That single fact explains several things at once. It explains why top-level code
in a module runs when someone imports it, which is why print statements left at
module level surface in surprising places. It explains why circular imports are a
problem: two modules each trying to finish running before the other can. And it
explains the caching - having run it once, Python keeps the result.

## The `__main__` guard

Because importing runs the file, a script that does work at the top level does
that work when imported too. The guard prevents it:

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

`__name__` is `"__main__"` when the file is run directly and the module's name
when it is imported. So the file can be both a usable script and an importable
module, which is what makes it testable - a test can import `main` without
running it.

## Packages and relative imports

A directory with an `__init__.py` is a package, and modules inside it can import
from each other relatively:

```python
from . import helpers          # same package
from .models import Record     # a module in the same package
```

Relative imports only work inside a package and only when the package is being
imported, not when a file inside it is run directly as a script. That
restriction is behind a large share of `ImportError: attempted relative import
with no known parent package` messages, and the usual answer is to run the module
with `python -m package.module` rather than by path.

## Where Python looks

Imports resolve against `sys.path`, which starts with the directory of the script
being run, then the standard library, then installed packages. The first match
wins, and that ordering is why a local file named `random.py` or `json.py`
shadows the standard library module of the same name and produces errors that
look impossible.

Naming a file after a module you also import is worth avoiding for exactly this
reason - the failure is confusing out of all proportion to the mistake.

## Import cost

Imports are cheap after the first, but the first one runs the whole module. A
library that does substantial work at import time makes every program that
imports it slower to start, which is why heavy setup belongs in a function the
caller chooses to call rather than at module level.
""")


add("generators_and_yield", """
## What "lazy" buys you in practice

Three things, and they are easy to state concretely.

Memory that does not scale with the input: a generator over a ten-million-line
file holds one line, not ten million. Work that is never done: if the consumer
stops after ten items, the generator computed ten, not the whole sequence. And
the ability to represent something that has no end, because nothing is built up
front.

The cost is that you get one pass and no length. If you need `len()`, indexing,
or a second traversal, you need a list, and calling `list()` on the generator is
the explicit way to say so.

## Reading files, the canonical example

```python
def lines_matching(path, needle):
    with open(path, encoding="utf-8") as f:
        for line in f:
            if needle in line:
                yield line.rstrip()
```

The file object is already a generator of lines, and this wraps it in another
that filters. Nothing is read until the caller starts iterating, and only one
line is in memory at a time regardless of file size.

Note the `with` inside the generator: the file stays open across yields and
closes when the generator is exhausted or garbage-collected. That is usually what
you want and is worth being conscious of, because a generator abandoned halfway
holds the file open until it is collected.

## yield from

Delegating to another iterable is one line:

```python
def all_items(groups):
    for group in groups:
        yield from group
```

`yield from group` yields every item of `group` in turn, which is both shorter
and faster than the explicit inner loop, and it becomes genuinely valuable with
recursive structures - walking a tree of nested lists is four lines with
`yield from` and considerably more without.

## Generators and pipelines

Because each stage pulls from the previous one, a chain of generators processes
one item end-to-end before starting the next. Memory stays flat no matter how
many stages there are, and no intermediate lists exist.

This is the shape behind most stream processing in Python: read, filter,
transform, aggregate - each a small generator, composed at the end. The
alternative, building a list at every stage, works fine until the data does not
fit, at which point the pipeline version is the only one that still runs.

## When a list is simply better

Small collections, results you need twice, anything you want to index, and
anything you want to print for debugging. A generator that you immediately wrap
in `list()` has bought nothing, and a comprehension says what you meant more
directly.
""")


add("inheritance", """
## Composition, concretely

"Prefer composition" is common advice and rarely shown. The difference is whether
the other object is *what you are* or *what you have*:

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
methods it chose to expose rather than everything `Engine` happens to define.

The test is substitutability. If code that expects the parent can be handed the
child and keep working, inheritance is honest. If not - if the child overrides
methods to raise, or ignores half of what it inherited - the relationship is not
"is a".

## Abstract base classes

When a parent exists to define an interface rather than to be instantiated,
`abc` makes that explicit:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...
```

Subclasses that forget `area` fail at construction with a clear message, rather
than at some later call site with `AttributeError`. That turns a runtime
surprise into an immediate, located error.

## Duck typing means you often need neither

Python does not require a shared base class for polymorphism. Anything with the
right method works:

```python
def describe(thing):
    return thing.speak()
```

This accepts any object with a `speak` method, related or not. A great deal of
Python code that would need an interface in another language needs nothing here,
which is worth remembering before building a hierarchy to enable something that
already works.

## Multiple inheritance and mixins

Multiple parents are legal, and the reasonable use is a mixin: a small class
providing one capability, with no state of its own and no expectation of being
instantiated - `JSONSerialisableMixin`, `TimestampMixin`.

Deep diamond hierarchies are the unreasonable use. When two parents both define
the same method and both call `super()`, the order of execution depends on the
MRO, and reasoning about it stops being possible for anyone who did not write it.
If you need `__mro__` to work out which code runs, the design has already cost
more than it saved.
""")
