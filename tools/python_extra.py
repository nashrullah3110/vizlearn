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

## Why in-place methods return None

`nums.sort()` returning `None` looks like an oversight and is a deliberate
convention that runs through the whole standard library. `list.reverse`,
`list.append`, `list.extend`, `dict.update` and `set.add` all return `None` for
the same reason: they changed the object rather than producing a new one, and
returning the object would invite `x = x.sort()`, which reads as though a new
list came back.

By returning nothing, the method makes that line obviously wrong the moment you
try to use the result. The `None` is not a missing return value; it is the
signal that the work happened somewhere else.

Once the convention is familiar it becomes a reading aid. A method that returns
`None` mutated something. A function that returns a value left its inputs
alone. `sorted`, `reversed`, `sorted`'s relatives in `itertools`, and every
string method follow the second pattern, which is why none of them ever
surprise you by changing what you passed in.

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

## When a loop is still better

The same limit applies as to list comprehensions. One transformation, one
optional filter, one line: use the comprehension. As soon as the value needs
several steps, a `try`, or a condition on the key as well as the value, the loop
version is easier to read and much easier to change later.
""")


add("conditional_comprehensions", """
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


# --------------------------------------------------------------------------
# Third pass. The sections above bring each topic to roughly 800 words, which
# explains the feature and stops just as the reader starts asking the second
# question. These take each page to around 2000: a worked example whose output
# is printed rather than described, the question people actually arrive with,
# and a recap that fits on one screen.
# --------------------------------------------------------------------------


extend("inheritance", """
## A hierarchy that earns itself

Two classes, where the second genuinely is a kind of the first and changes one
calculation:

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
rather than repeating `self.salary / 12`, so a change to how base pay is
computed reaches both classes. `__repr__` uses `type(self).__name__` rather
than the literal string `"Employee"`, so the subclass prints its own name for
free. And the loop does not ask what kind of object it has &mdash; it calls
`pay()` and lets each class answer. That last one is the point of the whole
exercise; a loop full of `isinstance` checks has inheritance without the
benefit.

## What super() actually does

`super()` is usually described as "call the parent", which is close enough
until it isn't. What it really means is *the next class along in the MRO of the
object's actual type* &mdash; and with one parent those are the same thing, so
the shortcut survives a long time before it breaks.

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
even though `Right` is nowhere in `Left`'s definition. The MRO is computed from
the type of the object, and `Both` puts `Right` after `Left`. This is what
makes cooperative multiple inheritance possible: each class does its bit and
delegates onward without knowing who is next.

It is also why `super().__init__(...)` matters even when the parent's
`__init__` looks empty. In a hierarchy someone else may extend later, breaking
the chain breaks classes that do not exist yet.

## Overriding without breaking the parent's promise

An override replaces a method, and anything holding the parent type keeps
calling it expecting the parent's behaviour. Two rules keep that honest.

**Accept at least what the parent accepted.** If `Animal.feed(self, amount)`
takes an amount, a subclass whose `feed(self)` takes none will fail whenever
it is used through the parent's interface.

**Return the same kind of thing.** A parent whose `area()` returns a number and
a child whose `area()` returns a string will break the first caller that does
arithmetic with it.

The override that breaks both is the one that refuses:

```python
class ReadOnlyList(list):
    def append(self, item):
        raise TypeError("read only")
```

This looks like a reasonable restriction and is a trap. Everything that accepts
a `list` is entitled to append to one, so `ReadOnlyList` is not a list in any
useful sense &mdash; it just passes `isinstance` checks. If you want something
that cannot be appended to, do not inherit from something that can; hold a list
and expose only the methods you intend to support.

## isinstance, and when checking the type is the wrong move

`isinstance(x, Animal)` is true for `Animal` and for every subclass, which is
what you almost always want. `type(x) is Animal` is true only for exact
matches, and using it deliberately excludes subclasses &mdash; which is rarely
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
class rather than every chain in the codebase.

The honest uses are narrow: validating an argument at a public boundary,
handling genuinely unrelated types such as "a string or a list of strings", and
writing `__eq__`, which has to decide what it can be compared against.

## Where attributes are found

Overriding is one case of a more general rule, and knowing the rule removes a
whole category of confusion. When you write `obj.thing`, Python looks in the
instance's own dictionary first, then the class, then each class along the MRO
in order, and raises `AttributeError` if none of them has it.

That ordering explains why assigning to an attribute on one instance does not
affect the others, and why assigning on the class affects every instance that
has not set its own:

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
*assigns* the result to `a`, which creates an instance attribute shadowing the
class one. `b` and the class itself never change. This is the single most
common surprise with class attributes, and it is not a special rule &mdash; it
falls straight out of "reads search the chain, writes always land on the
instance".

The version that genuinely shares state has to say so:

```python
    def bump(self):
        Counter.total += 1         # or type(self).total
```

And the version that catches people badly is a mutable class attribute, because
appending to a list is a read followed by a mutation, not an assignment &mdash;
so every instance really does share it. If each instance needs its own, create
it in `__init__`.

## Extending a built-in, and why it disappoints

Subclassing `dict` or `list` looks like the obvious way to get a container with
one extra behaviour, and it works less well than expected:

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

`update` is implemented in C and does not route through `__setitem__`, so the
override is bypassed. The same applies to `dict(**d)`, `setdefault`, and the
equivalents on `list`. The built-ins are not written as cooperating Python
methods, and nothing promises they will call each other.

Two ways out. `collections.UserDict` and `UserList` are pure-Python wrappers
written so that every operation does go through the methods you can override.
Or hold a plain `dict` as an attribute and expose only the operations you mean
to support &mdash; composition again, and usually the better answer, because a
container with one unusual rule is rarely a good substitute for the real thing
everywhere a `dict` is accepted.

## Alternative constructors, and why they take cls

A class often needs more than one way to be built &mdash; from a string, from a
row of a file, from a dictionary. Adding parameters to `__init__` for each one
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

The important detail is `cls`, not `Point`. A classmethod receives the class it
was called on, so `Point3D.from_text` builds a `Point3D` without `Point3D`
writing a line of code. Hard-coding `return Point(...)` would have given a
`Point` from both calls, and the subclass would have silently lost its own
type &mdash; the same failure as hard-coding a name in `__repr__`, from the
same cause.

## Questions people ask

<strong>Do I have to call `super().__init__()`?</strong> Only if the parent's
`__init__` does something you need &mdash; but it usually does, and skipping it
fails later and further away, so call it unless you have a specific reason not
to.

<strong>Can a subclass add attributes the parent knows nothing about?</strong>
Yes, and that is normal. `Manager` adding `bonus` is exactly the intended use.

<strong>What is the difference between overriding and overloading?</strong>
Overriding is replacing an inherited method, which Python does. Overloading is
several versions of one function distinguished by argument types, which Python
does not have &mdash; default arguments and `*args` cover the same ground.

<strong>Should everything inherit from a common base?</strong> No. That is a
habit from languages where it is required. Unrelated classes should be
unrelated.

<strong>How deep is too deep?</strong> Three levels is usually already a
warning. The cost is not the depth itself but that finding which class defines
a given method becomes a search.

<strong>Why does my subclass print the parent's name?</strong> Because
`__repr__` hard-codes a string. Use `type(self).__name__` and it follows the
actual class.

<strong>Why does `super()` need no arguments?</strong> Inside a class body Python
supplies the class and the instance for you. The explicit
`super(Dog, self)` form is the Python 2 spelling and still works, which is why
you will see it in older code.

<strong>Can I inherit from a class in another module?</strong> Yes, and it is
normal &mdash; but remember that you are now coupled to that class's internals,
so a library's undocumented base class is a risky parent.

## Recap in one screen

- Inherit when the child genuinely is a kind of the parent and can be used
  anywhere the parent is expected; otherwise hold the other object instead.
- `super()` means the next class in the MRO of the object's real type, not
  literally the parent &mdash; which is what makes mixins work.
- Overrides must accept what the parent accepted and return what it returned;
  an override that raises is a sign the relationship is wrong.
- Prefer a method call over a chain of `isinstance` checks; that is the
  benefit you inherited for.
- `type(self).__name__` in `__repr__` gives every subclass a correct one.
""")


extend("input_and_output", """
## Reading several values from one line

People type more than one thing at a time, and `split()` is how you take them
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

`split()` with no argument is the one to reach for: it splits on any run of
whitespace and ignores leading and trailing space, so a line typed with two
spaces between values still works. `split(" ")` is the version that does not
forgive that, and produces empty strings where the extra spaces were.

The trap is unpacking a line whose length you assumed:

```python
a, b, c = "3 12".split()
# ValueError: not enough values to unpack (expected 3, got 2)
```

The message is precise, which makes this an easy one to fix &mdash; but it is
raised at the assignment, so a program that reads ten lines and unpacks each
will stop on the first short one. Where the input comes from a person rather
than a file you control, check the length before unpacking, or collect with a
star and validate.

## A menu loop, end to end

Most small interactive programs are the same shape: show the options, read a
choice, act on it, repeat until they quit. Written once properly it is worth
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
data in a dictionary rather than a chain of `elif`, so adding one is a single
line; the choice is stripped and lowercased before anything looks at it, so
`" Q "` works; an unknown choice says what was typed and loops rather than
crashing; and quitting is an explicit option rather than Ctrl-C.

In a real program the `for choice in choices` line becomes `while True:` with
`choice = input("choose: ")`. Everything else stays as it is.

## Why output sometimes appears in the wrong order

Standard output is buffered when it is not a terminal. Python collects printed
text and writes it in blocks, because one system call per line is slow. On
screen this is invisible. Redirect to a file or pipe the program into another
one and it becomes visible: output can appear late, and it can appear *after*
things written to standard error, which is not buffered the same way.

```python
import sys

print("step 1")                       # buffered
print("warning", file=sys.stderr)     # not buffered
print("step 2", flush=True)           # written immediately
```

Run that on a terminal and the order is what you wrote. Run `python3 s.py > out.txt`
and the warning appears on screen before the file has anything in it.

`flush=True` forces a write at that point. It is worth using for progress
messages in a long-running script, and for anything printed just before an
operation that might hang &mdash; otherwise the message you were relying on to
tell you where it got stuck is still sitting in the buffer.

The same applies to a crash: output already printed but not yet flushed can be
lost if the process dies badly, which is one of the reasons `logging` is
preferred to `print` once a script grows up.

## Command-line arguments, the other input

`input()` is not the only way a program receives values, and for anything you
will run more than once it is the worse one. Arguments typed alongside the
command arrive in `sys.argv`:

```python
import sys

# $ python3 report.py sales.csv 2024
print(sys.argv)          # ['report.py', 'sales.csv', '2024']
name = sys.argv[1] if len(sys.argv) > 1 else "data.csv"
```

`sys.argv[0]` is the script's own name, so the real arguments start at index 1,
and reading one that was not supplied raises `IndexError` &mdash; hence the
length check, or a default.

The difference matters more than it looks. A program driven by `input()` cannot
be scripted, scheduled, or re-run with the same values without somebody typing
them again. A program driven by arguments can be put in a shell script and
repeated exactly. The rule of thumb: prompt for what a person decides in the
moment, take as an argument anything the program needs every time it runs.

Once there is more than one or two, `argparse` in the standard library is worth
the twenty minutes &mdash; it gives `--flags`, defaults, type conversion, and a
`--help` message generated from the same declaration.

## Making a prompt hard to get wrong

Most bad input is invited by the prompt. Three habits remove most of it:

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
convention for the default.

**Normalise before comparing.** `strip().lower()` turns four different things a
person might type into one thing your code has to handle.

**Accept the obvious variants.** Someone who types `yes` when you asked for `y`
has answered the question; refusing them is the program being difficult.

The same three apply to any prompt, not just yes/no: show the units, show the
default, and strip the input before you look at it.

## Reading a password without showing it

`input()` echoes what is typed, which is exactly wrong for a password. The
standard library has the right tool:

```python
from getpass import getpass

secret = getpass("Password: ")     # typed characters are not displayed
```

It reads from the terminal directly rather than from standard input, so it
cannot be piped into &mdash; which is a feature. It also falls back to a plain
`input()` with a warning when there is no real terminal, so check the
environment rather than assuming the characters were hidden.

The rule that goes with it: do not print a secret back out, do not put one in a
default argument, and do not read one from `sys.argv`, because arguments are
visible to anyone who can list the running processes. For anything automated,
an environment variable or a file with restricted permissions is the usual
answer, and `os.environ.get("API_KEY")` is how you read it.

## Confirming before something irreversible

When a program is about to delete, overwrite or send something, the prompt is
the last line of defence, and a `[y/N]` is a weak one &mdash; people type `y`
by reflex. For genuinely irreversible actions, ask for something that cannot be
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

Requiring the name to be typed out makes the person read what they are about to
do. Note that this comparison is deliberately not lowercased or fuzzy-matched:
everywhere else on this page the advice is to forgive input, and this is the
one place where being strict is the point.

## Questions people ask

<strong>Why does `input()` return a string when I typed a number?</strong>
Because it reads characters and has no way to know what you meant by them.
`"42"` could be a quantity, a house number or a password.

<strong>How do I read a number without crashing on bad input?</strong> Wrap
`int()` in `try`/`except ValueError` and ask again &mdash; the loop earlier on
this page is the standard shape.

<strong>What is the difference between `print(x)` and `print(str(x))`?</strong>
Nothing. `print` calls `str()` on each argument already.

<strong>Why do my strings show up with quotes?</strong> You printed a
container. `print(["a"])` shows the list's `repr`, which quotes its items;
`print(", ".join(["a"]))` prints them as text.

<strong>How do I print without a newline?</strong> `print(x, end="")`, then a
bare `print()` when the line is finished.

<strong>Can I read everything at once instead of line by line?</strong> Yes:
`sys.stdin.read()` for the whole of standard input, or `sys.stdin` iterated
like a file for one line at a time without `input`'s prompt handling.

<strong>Why does my prompt appear after the input on some terminals?</strong>
Because the prompt was printed with `print` and not flushed. `input()`'s own
prompt argument does not have this problem, which is the reason to use it.

<strong>How do I clear the screen or move the cursor?</strong> With terminal
escape codes, or a library like `curses` or `rich`. There is nothing in `print`
itself for it.

<strong>Does `input()` strip the newline?</strong> Yes &mdash; it returns the
line without the trailing newline, but with any spaces the person typed, which
is why `strip()` is still worth calling.

## Recap in one screen

- `input()` always returns a string, and always without the trailing newline.
- Convert explicitly, and expect the conversion to fail on real input &mdash;
  `try`/`except ValueError` in a loop is the shape that survives a person.
- `split()` with no argument handles ragged whitespace; unpacking a line
  assumes a length, so check it first.
- `sep` and `end` control what `print` puts between and after its arguments;
  `file=sys.stderr` separates chatter from results.
- Output is buffered when redirected. `flush=True` for progress messages you
  need to see while the program is still running.
""")


extend("string_methods", """
## replace, and the count nobody passes

`replace` swaps every occurrence and, like everything else here, returns a new
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

The third argument caps how many are replaced, counting from the left, and it
is the one people forget exists &mdash; it saves a regular expression
surprisingly often. The last line is the reminder that `text` itself never
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
`raw.strip()` removes the leading spaces and the trailing newline from the line
as a whole. The one inside the comprehension removes the spaces around each
field, which the outer one could not reach. Splitting first and stripping each
piece is the general shape; stripping only the whole line leaves `" 91 "`,
which `int()` happens to forgive and a string comparison does not.

`repr()` in the output is there deliberately. Printing a string that still has
a stray space looks identical to one that does not, and `repr` is how you see
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
handles a leading minus sign correctly, which `rjust(3, "0")` does not.

The f-string spellings are `f"{name:<10}"`, `f"{n:>4}"` and `f"{n:^4}"`, and
they are usually the better choice because the value and its formatting stay
together. The methods are worth knowing for when the width is computed rather
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

`isdigit` is not "would `int()` accept this". It rejects a decimal point and a
minus sign, and it accepts superscripts and other numeric characters that
`int()` refuses. `isdecimal` is the stricter one and the closer match to what
people usually mean.

The reliable test for "is this a number" is to try the conversion:

```python
def is_int(text):
    try:
        int(text)
    except ValueError:
        return False
    return True
```

That handles the minus sign, the surrounding whitespace and the underscores
Python allows in numeric literals, all of which the `is` methods get wrong in
one direction or the other. `isalpha`, `isspace` and `isupper` have no such
problem and are safe to use directly.

## Why strings are immutable at all

Beginners meet immutability as an inconvenience &mdash; the reason `name.upper()`
seems not to work. It is worth knowing what the language buys with it, because
the same property explains behaviour in several other places.

A string that cannot change can be shared without anyone worrying about who
else holds it. Python takes advantage of that constantly: identical short
strings in your source are often the same object in memory, string constants
can be stored once and pointed at from many places, and passing a string to a
function costs nothing regardless of its length, because nothing is copied.

It also makes strings hashable, and therefore usable as dictionary keys and set
members. A hash is computed from the contents; if the contents could change,
the key would end up filed under a hash that no longer matches it, and lookups
would silently fail. This is exactly why lists cannot be keys and tuples can.
Every dictionary you index by name relies on strings being immutable.

The cost is real and narrow: building a string by repeated concatenation is
quadratic, because each step copies everything so far. That is the one place
where the design bites, and `join` exists to cover it. Everywhere else, the
guarantee that a string you were handed is the string you still have is worth
considerably more than the ability to edit one in place.

## Unicode, and what a character actually is

A Python string is a sequence of Unicode code points, not bytes. For English
text the distinction never comes up, and outside English it comes up
immediately.

`len("café")` is 4, which is what you would hope. But the same text can be
written two ways in Unicode &mdash; as an `é` code point, or as `e` followed by
a combining accent &mdash; and in the second form `len` reports 5 while the
text looks identical on screen. `unicodedata.normalize("NFC", text)` collapses
the second form into the first, and normalising before comparing is the fix for
"these two strings look the same and are not equal".

Emoji push this further: many are several code points joined together, so
slicing a string by index can cut one in half and produce something that will
not render. If you are truncating text that might contain them, count
grapheme clusters with a library rather than characters.

Encoding is the separate question of how those code points become bytes for a
file or a network. `text.encode("utf-8")` produces `bytes`;
`data.decode("utf-8")` goes back. The errors people hit &mdash;
`UnicodeDecodeError` on reading a file, mojibake like `Ã©` where `é` should be
&mdash; are almost always a file written in one encoding and read in another.
UTF-8 is the right default everywhere, and specifying it explicitly when
opening files is worth the few extra characters, because the default still
varies by platform.

## When to stop using string methods

The methods on this page handle a great deal, and there is a point past which
they stop being the right tool. The signal is a chain of `split`, `strip`,
`find` and slicing that is getting longer each time the input surprises you.

If the pattern is genuinely variable &mdash; optional whitespace, alternatives,
repetition, groups you want to capture &mdash; that is what regular expressions
are for, and `re.search` with a named group will be shorter and easier to fix
than eight lines of index arithmetic. The trade is that a regular expression is
harder to read for anyone who does not write them often, so it earns its place
only when the string methods have genuinely run out.

If the text is a known format, do not parse it by hand at all. JSON, CSV, INI
files, dates, URLs and email addresses all have a module in the standard
library that has already handled the edge cases you have not thought of yet:
quoted commas inside a CSV field, escaped characters in JSON, timezone
suffixes, percent-encoding. Hand-rolled parsing of a standard format is the
most reliable way to produce a program that works on your test file and fails
on real data.

The rule that follows is a simple one. String methods for cleaning and simple
splitting, a parser for anything with a specification, and regular expressions
for the genuinely irregular middle ground.

## Questions people ask

<strong>Why does `strip()` not remove a suffix?</strong> Because its argument
is a set of characters to remove from each end, not a string to match. Use
`removesuffix` for the other job.

<strong>Is `+` on strings actually slow?</strong> Not for a few pieces. It is
slow inside a loop over thousands, because each `+` builds a whole new string.
Collect into a list and `join` once.

<strong>What is the difference between `find` and `index`?</strong> `find`
returns -1 when absent, `index` raises `ValueError`. Pick based on whether
absence is expected or a bug.

<strong>How do I split on more than one separator?</strong> `re.split` from the
`re` module &mdash; `str.split` takes one separator only.

<strong>Why does `"".join(numbers)` fail?</strong> `join` requires strings.
Convert first: `"".join(str(n) for n in numbers)`.

<strong>Does `lower()` work for every language?</strong> Mostly.
`casefold()` is the more aggressive version intended for caseless comparison,
and it is what to use when the text is not guaranteed to be English.

<strong>How do I check a string against several endings?</strong>
`endswith` accepts a tuple: `name.endswith((".jpg", ".png"))`.

## Recap in one screen

- Every string method returns a new string; if you do not assign the result,
  nothing happened.
- `join` is called on the separator and needs strings; `split()` with no
  argument is the forgiving version.
- `strip` takes characters, not a suffix &mdash; `removeprefix` and
  `removesuffix` exist for that.
- `find` returns -1, `index` raises; `in` is the one to use when you only need
  a yes or no.
- `isdigit` is not "is a number" &mdash; try the conversion instead.
""")


extend("mutability_and_aliasing", """
## Watching it happen with id()

`id()` returns a number identifying an object for as long as it exists, which
turns the whole topic from an assertion into something you can check:

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

The first line mutated the object, so the id is unchanged and `b` &mdash; the
other name for that same object &mdash; sees the new item. The second line
built a different list and pointed `a` at it, so the id changed and `b` still
refers to the original, which now has three items rather than four.

Every confusing aliasing bug is one of those two lines in disguise.

## The augmented assignment asymmetry

`a += [3]` and `a = a + [3]` look like the same statement written two ways.
For lists they are not:

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

`+=` on a list calls `__iadd__`, which extends the existing list in place and
then rebinds the name to that same object &mdash; so every other name sees the
change. `a + [3]` builds a new list and only then rebinds, leaving `b` alone.

For numbers, strings and tuples there is no in-place option, so `+=` always
behaves like the second form. This is why `+=` feels consistent right up until
the first time it is used on a list that someone else is also holding.

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

The tuple guarantees that its slots keep pointing at the same objects. It
promises nothing about those objects. A tuple of lists is therefore not a
frozen structure, and &mdash; the practical consequence &mdash; it cannot be
used as a dictionary key, because hashing it has to hash its contents and lists
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
tries to assign the result back into the tuple slot, which fails. The mutation
has already happened by then. Nothing about this is worth relying on; it is
worth recognising, because the error message points at the tuple while the
damage is in the list.

## Where this actually bites

The rule is simple and the bugs are not, because in real code the two names for
one object are usually far apart. Four shapes account for most of them.

**A shared default.** A function with `def add(item, target=[])` creates that
list once, when the function is defined, and every call that does not pass one
uses the same list. Items accumulate across calls that look independent. The
fix is `target=None` and `if target is None: target = []` in the body.

**A configuration dictionary passed around.** One module reads a settings dict,
tweaks a value "just for its own use", and every other module sees the change.
This is the hardest version to find, because the code that made the change and
the code that misbehaves may be in different files with nothing linking them.

**A cached object handed to callers.** A function that builds a list once and
returns the same list every time is fast and dangerous: the first caller to
mutate the result has changed what every later caller receives. Returning a
copy, or a tuple, closes it.

**A class attribute holding a list.** Written on the class rather than in
`__init__`, it belongs to the class, so every instance appends to the same one.
Instances that were meant to be independent quietly share state.

What the four have in common is that nobody wrote `b = a`. The second name
arrived through an argument, a return value, a default or a class body. That is
why "assignment does not copy" is worth internalising rather than memorising:
the aliasing is rarely visible on the line where the bug appears.

## A model that fits in your head

Two sentences cover everything on this page.

**Names point at objects.** A name is not storage; it is a label. Assignment
moves a label. Several labels can point at one object, and the object has no
idea how many.

**Some objects can change, and some cannot.** If an object can change, then
every label pointing at it sees the change, because there is only one object.
If it cannot, the question never arises.

Everything else follows. Why does mutating a list argument affect the caller?
The parameter is another label on the same object. Why does `n += 1` inside a
function not affect the caller? Integers cannot change, so `+=` must build a
new one and move the local label to it. Why is a tuple of lists not frozen? The
tuple's labels cannot be moved; the objects they point at can still change.

When something surprising happens, the productive question is not "was this
passed by value or by reference" but "how many names point at this object, and
did that line move a label or change an object". `id()` answers the first half
and the code in front of you answers the second.

## Choosing immutability in your own code

Once the distinction is clear, it becomes a design decision rather than a fact
about builtins. Making your own objects immutable removes the entire class of
bugs above, and Python gives you a few ways to do it.

A `NamedTuple` or a dataclass declared with `@dataclass(frozen=True)` produces
a class whose attributes cannot be reassigned after construction. Attempting it
raises rather than silently succeeding, which turns a subtle shared-state bug
into an immediate error at the line that caused it. Both are hashable, so they
can be dictionary keys and set members, and both give you a readable `repr` for
free.

The pattern that follows is to build a new object rather than edit an existing
one. A method that would have changed `self.total` instead returns a new
instance with the new total, and callers rebind. This costs an allocation and
buys the guarantee that nothing you handed to another part of the program can
change underneath it.

It is not the right default for everything. A large object that changes often
&mdash; a buffer being filled, a cache, anything performance-sensitive &mdash;
is better mutable, and Python's builtins reflect that. The useful habit is to
reach for immutability for the things that travel: configuration, coordinates,
records read from a file, anything passed between modules or stored in a
dictionary. Keep mutability local, where you can see every name that points at
the object.

## Questions people ask

<strong>How do I copy a list properly?</strong> `list(a)`, `a[:]` or `a.copy()`
for one level. `copy.deepcopy(a)` when the items are themselves mutable and
need copying too.

<strong>Is `is` ever right for comparing values?</strong> Only for `None`,
`True` and `False`. Everything else should use `==`.

<strong>Why did my dictionary change when I only edited a copy?</strong>
Because the copy was shallow and the value you edited is shared between both
dictionaries.

<strong>Are function arguments copied?</strong> No. The function gets another
name for the same object, which is why mutating a list argument is visible to
the caller.

<strong>Why can a tuple be a dictionary key but not a list?</strong> Keys must
hash to a stable value, and a list's contents can change, which would leave it
filed in the wrong place.

<strong>Does `sorted(x)` change `x`?</strong> No, it returns a new list.
`x.sort()` is the in-place one, and it returns `None` &mdash; assigning its
result is a common way to lose a list.

<strong>What about strings, do I need to copy them?</strong> Never. They cannot
be changed, so sharing one is always safe.

## Recap in one screen

- A name is a label on an object; assignment moves the label and never copies.
- Mutating changes the object every name can see; rebinding changes one name.
- `+=` mutates in place for lists and rebinds for immutables &mdash; the same
  syntax, two behaviours.
- Immutable contents can hold mutable objects, so a tuple is only as frozen as
  what is in it.
- Copy at the boundary when you store or return a caller's container.
""")


extend("lambda_map_filter", """
## operator, the module that replaces most lambdas

A large share of the lambdas people write do one of two things: pull out an
item, or pull out an attribute. The standard library has both, and they are
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
`itemgetter(1, 0)` returns a tuple, which is how you sort by score and then by
name without writing the tuple out. `attrgetter` is the same for objects, and
`methodcaller("lower")` for calling a method on each item.

Note the first result: `ana` comes before `cy` even though they tie, because
`sorted` is stable and `ana` was first in the input. That guarantee is what
makes sorting twice for a two-level sort work at all.

## reduce, and why it is not a builtin any more

`map` and `filter` survived the move to Python 3 as builtins. `reduce` did not,
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

The reason for the demotion is on the second line. Nearly every real use of
`reduce` is a sum, a maximum, a minimum, an `any` or an `all`, and each of
those has a builtin that says what it means at a glance. What is left &mdash;
a running product, folding a custom combine function over a sequence &mdash; is
rare enough to be worth an import and a moment's thought from the reader.

If you do reach for it, pass the initial value: `reduce(f, items, 0)` returns
the initial value for an empty sequence instead of raising `TypeError`.

## Where map and filter lead: itertools

`map` and `filter` are the first two of a family. `itertools` holds the rest,
and they share the same property of producing items on demand rather than
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

`islice` takes the first few of anything, including an infinite generator.
`takewhile` stops at the first item that fails the test, which is different
from `filter` &mdash; `filter` would carry on and return 1, 2, 3 from the whole
range while `takewhile` stops looking at 4. `chain` walks several iterables as
one without building a combined list.

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

One lambda appears, as a `key=` argument, which is exactly the place the
earlier section said it belongs. The filtering and the transforming are done by
the comprehension rather than by `filter` and `map`, and the result reads in
the order it happens.

## What "functional" means here, and what it does not

`lambda`, `map` and `filter` arrive with a reputation attached, and it is worth
separating the useful part from the folklore.

The useful part is that functions are ordinary values in Python. A function can
be stored in a list, passed as an argument, returned from another function, and
kept in a dictionary. That is what makes `key=` arguments, decorators,
callbacks and dispatch tables possible, and it is the single idea behind
everything on this page. A lambda is not a special kind of function; it is the
same object a `def` produces, written inline and left unnamed.

The folklore is that using them makes code functional, and that functional code
is better. Python is not a functional language and does not try to be. It has
no tail-call optimisation, its lambdas are deliberately limited to one
expression, and `reduce` was moved out of the builtins precisely to discourage
the style. Guido van Rossum's stated preference was that a comprehension or a
plain loop says the same thing more clearly to more readers.

What actually transfers from functional programming, and is worth adopting, is
smaller and less glamorous: prefer functions that return a new value over
functions that modify their arguments; avoid depending on state that is not
visible in the signature; and keep functions small enough to test on their own.
None of that requires a lambda. A page of `def` statements can follow all three,
and a chain of nested `map` and `filter` calls can violate them all while
looking the part.

## When a comprehension stops being the clearer choice

The advice throughout this page is to reach for a comprehension first, so it is
worth being precise about where that stops holding.

A comprehension is doing too much when it has more than one `for` and a
condition, when the expression at the front needs its own explanation, or when
the whole thing no longer fits on one line without awkward wrapping. At that
point it has become a loop that is harder to read than the loop would have
been, and the honest move is to write the loop &mdash; or to name the inner
step as a function and call it from a simple comprehension.

The other case is when you need something a comprehension cannot do: a `break`,
an early return, a `try`/`except` around one item, or anything that has to
happen for its side effect rather than its value. A comprehension built purely
for side effects, with its result thrown away, is a loop wearing the wrong
clothes; write `for` and let the reader see what is happening.

Nesting deserves its own warning. A comprehension inside another
comprehension's expression is read outer-first and reasoned about
inner-first, which is exactly the sort of thing that is fine while you are
writing it and unpleasant three months later. Two statements are almost always
better than one clever one.

## Naming things the reader will meet

Two words appear constantly in discussions of this material and are rarely
defined, which makes a lot of otherwise good explanations hard to follow.

A **higher-order function** is a function that takes a function as an argument
or returns one. `sorted` is higher-order because of `key=`; so are `map`,
`filter`, and every decorator you will write. There is nothing more to the term
than that.

A **closure** is a function that remembers a value from the scope where it was
created, and keeps working after that scope has finished. The loop trap earlier
on this page is a closure behaving exactly as specified and not as expected: the
lambdas remembered the variable rather than the value it held at the time.

## Questions people ask

<strong>Can a lambda have more than one statement?</strong> No. The body is a
single expression. If you need a statement, you need a `def`.

<strong>Can a lambda have default arguments?</strong> Yes &mdash;
`lambda x, n=2: x ** n` &mdash; and that is also the trick for capturing a loop
variable by value.

<strong>Why does printing `map(...)` show an object?</strong> Because it is a
lazy iterator. Wrap it in `list()` to see the items.

<strong>Is a comprehension faster than `map`?</strong> They are close.
`map(int, items)` with an existing function is usually slightly faster;
`map(lambda ..., items)` is usually slightly slower. Neither difference is a
reason to choose one.

<strong>What does `filter(None, items)` do?</strong> Drops every falsy item.
`None` in the function slot means "use the item's own truthiness".

<strong>Why can I not pickle a lambda?</strong> Pickling stores a reference by
name and a lambda has none. That is why `multiprocessing` rejects them, and
where `functools.partial` earns its place.

<strong>Do `map` and `filter` work on dictionaries?</strong> They work on
anything iterable, and iterating a dictionary gives its keys. Use
`d.items()` when you want pairs.

## Recap in one screen

- A lambda is a single-expression function; use one as a `key=` argument and
  write a `def` whenever it deserves a name.
- `map` and `filter` are lazy iterators &mdash; consume them once, wrap in
  `list()` to keep them.
- Prefer a comprehension by default; `map(existing_function, items)` when it is
  exactly that shape.
- `operator.itemgetter` and `attrgetter` replace the most common lambdas and
  read better.
- `reduce` lives in `functools` because `sum`, `max`, `any` and `all` already
  cover almost every use of it.
""")


extend("range_step", """
## Why the stop is excluded, and why it is the right choice

"The stop is never included" is easy to memorise and easy to resent. It is
worth a paragraph on why the language chose it, because once the reasoning is
clear the off-by-one errors mostly stop.

A half-open interval &mdash; one that includes the start and excludes the stop
&mdash; has three properties that a closed interval does not. The length is the
subtraction: `range(a, b)` produces exactly `b - a` numbers, with no correction
term to remember. The empty case is expressible: `range(3, 3)` is empty, where a
closed interval would have no way to say "nothing" without a special case. And
adjacent ranges join without a gap and without an overlap: `range(0, 5)` and
`range(5, 10)` between them cover 0 to 9, each number exactly once, which is
what makes splitting work.

The same choice runs through slicing, which is why `a[:3]` and `a[3:]`
reconstruct the whole list and why `len(a[i:j])` is `j - i`. Learning it once
covers both, and the pattern is deliberate rather than accidental.

The place it still catches people is counting down, where the exclusive end is
below the last value you want rather than above it. That is not a different
rule, but it does read differently, which is why it deserves its own attention.

## Chunking, the most common use of a step

The step exists for a specific job more often than for skipping numbers:
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

The last chunk is short and needs no special handling, because slicing does not
complain when the end is past the length. That is the second time on this page
that a rule which looks like leniency turns out to remove a branch.

This shape appears whenever something has a batch limit: rows to insert per
query, items per API request, lines per page. The alternative is an index and a
counter, which is more code and more places to be wrong by one.

## Floats, and stepping by a fraction

`range(0, 1, 0.1)` raises `TypeError`, which reads like a limitation and is
closer to a favour. The reason is that a fractional step accumulates error:

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
is not 0.9. Adding 0.1 repeatedly compounds the tiny error in representing 0.1
in binary, and after ten additions the running total is a hair under 1.0 &mdash;
so the condition holds one more time than intended. The number of iterations now
depends on rounding error rather than on anything you wrote.

The reliable pattern is to count in integers and divide once at the end:

```python
print([i / 10 for i in range(0, 10, 2)])
```

```
[0.0, 0.2, 0.4, 0.6, 0.8]
```

Each value is computed from an exact integer rather than from the previous
value, so no error accumulates and the number of items is fixed by the `range`.
For anything more involved, `numpy.arange` and `numpy.linspace` exist, and
`linspace` is the one to prefer because you give it the count rather than the
step.

## The range(len(...)) habit, and what to write instead

A large share of the `range` calls in beginner code are `range(len(items))`,
used to get at the items:

```python
for i in range(len(items)):
    print(items[i])
```

This works and is worth unlearning. It introduces an index that nothing needs,
it reads as arithmetic rather than as iteration, and it is the version that
produces `IndexError` when the bound is computed slightly wrong. `for item in
items` says the same thing with less to get wrong.

The three cases that look like they need it usually do not. If you want the
position alongside the item, `enumerate(items)` gives both. If you are walking
two sequences together, `zip(a, b)` pairs them. If you are comparing each item
with the next, `zip(items, items[1:])` gives consecutive pairs.

What is left is genuinely index-based work: writing into a list at a computed
position, stepping by more than one, or walking backwards by index. Those are
real, and they are a small minority.

## Reading a range at a glance

Three questions come up constantly when reading someone else's loop, and all
three have arithmetic answers that are worth being able to do without running
anything.

**How many numbers is that?** For a positive step, it is the distance divided
by the step, rounded up: `range(0, 10, 3)` covers a distance of 10 in steps of
3, giving 4 numbers. The rounding up is what catches people, and it is why
`range(0, 10, 3)` gives four values rather than three.

**What is the last one?** It is the largest value below the stop that you can
reach from the start by whole steps. For `range(0, 10, 3)` that is 9. When the
step divides the distance exactly, as in `range(0, 10, 2)`, the last value is
the stop minus the step &mdash; 8, not 10 &mdash; because the stop itself is
never included.

**Does it produce anything at all?** Only if the start is on the correct side
of the stop for the direction of travel. Ascending needs `start < stop`,
descending needs `start > stop`. Neither raises when it is wrong; you get an
empty range, and a loop that silently does nothing.

That last one is worth dwelling on, because it is the failure mode that costs
the most time. An exception tells you where to look. A loop that runs zero
times leaves no trace at all, and the symptom appears later as an empty result
or an unchanged variable. When a loop appears not to have happened, printing
`list(the_range)` is usually a faster diagnosis than reading the arithmetic
again.

## Questions people ask

<strong>Why does `range(5, 0)` produce nothing?</strong> Because the default
step is 1, so it is counting up from 5 towards 0 and stops immediately. You
need `range(5, 0, -1)`.

<strong>Is `range` a generator?</strong> No. It is a lazy sequence: it can be
iterated many times, it has a length, and it supports indexing and slicing. A
generator has none of those.

<strong>How do I get a list from a range?</strong> `list(range(5))`. It is
worth asking whether you need one &mdash; a loop does not.

<strong>Why is `x in range(n)` fast?</strong> It does arithmetic rather than
scanning, so it is constant time regardless of the size of the range.

<strong>Can the step be negative and the start below the stop?</strong> It can
be written, and it produces an empty range. Nothing is raised.

<strong>Does `range` work with very large numbers?</strong> Yes.
`range(10**18)` is created instantly, because nothing is stored but the three
values.

<strong>How do I include the stop?</strong> Add one to it. That is the honest
answer, and `range(1, n + 1)` is how you count from 1 to n.

<strong>Can I slice a range?</strong> Yes, and you get another range back:
`range(10)[2:5]` is `range(2, 5)`. Nothing is materialised.

<strong>Why does `range` compare equal to another range with different
arguments?</strong> Because ranges compare by the sequence they produce, not by
their start, stop and step. `range(0) == range(2, 2)` is `True`; both are empty.

<strong>Is there a version that includes the stop?</strong> Not in the
standard library. `numpy.linspace` is the closest, and it takes a count rather
than a step, which sidesteps the question.

<strong>What does a negative index do on a range?</strong> The same as on any
sequence: `range(10)[-1]` is 9. It is computed rather than looked up, so it is
instant even on an enormous range.

<strong>Should I ever store a range in a variable?</strong> Yes, when the same
sequence of numbers is used twice. Unlike a generator it can be iterated again,
so it is safe to reuse.

## Recap in one screen

- One argument is stop, two are start and stop, three add a step; the stop is
  always excluded.
- The half-open interval makes the length a subtraction, lets ranges be empty,
  and lets adjacent ranges tile without gaps.
- Counting down needs both a negative step and a stop below the start, and a
  wrong sign gives an empty range rather than an error.
- `range` refuses floats on purpose; count in integers and divide once.
- `range(len(items))` is usually `enumerate`, `zip`, or just iterating the
  items.
""")


extend("dictionary_methods", """
## Counter, and the four things it gives you

Counting is common enough that the standard library has a dictionary subclass
for it, and knowing four of its behaviours removes a lot of hand-written code:

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

First, it counts anything iterable in one call, so the loop disappears. Second,
`most_common(n)` sorts by count and gives the top n, which is the question
people actually want answered and is otherwise a `sorted` with a `key`. Third,
a missing key returns 0 rather than raising &mdash; and, unlike `defaultdict`,
it does not insert the key on access, so reading does not quietly grow the
dictionary. Fourth, counters support arithmetic: `a + b` merges counts and
`a - b` subtracts them, which is a neat way to diff two collections.

It is still a dictionary, so everything else on this page applies to it.

## What can be a key, and why

Any object can be a key if it is hashable, which in practice means immutable
all the way down. Strings, numbers, booleans and tuples of those are fine.
Lists, dictionaries and sets are not, and a tuple containing a list is not
either, because hashing it has to hash its contents.

The reason is how a dictionary works. It computes a hash of the key, uses that
to decide where to store the entry, and looks in the same place later. If a key
could change after insertion, its hash would change, and the entry would be
sitting somewhere the lookup will never search. Rather than allow that, Python
refuses to hash mutable types at all.

Two consequences are worth knowing. `1`, `1.0` and `True` all hash the same and
compare equal, so they are the *same key* &mdash; `{1: "a", True: "b"}` has one
entry. And a tuple key is the standard way to index by more than one thing:
`grid[(row, col)]` is a perfectly ordinary dictionary lookup, and the brackets
around the tuple are optional.

Custom classes are hashable by default, using identity, which means two
distinct instances with identical contents are different keys. If you want them
to be the same key, define `__eq__` and `__hash__` together &mdash; or use a
frozen dataclass, which writes both for you.

## A dictionary instead of a chain of elif

Once functions can be values, a dictionary replaces a whole shape of code:

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

Compared with an `if`/`elif` chain, this separates the table of options from the
code that uses it. Adding an operation is one dictionary entry rather than
another branch, the set of valid options can be listed with `OPS.keys()`, and
the same table can drive a help message or validate input.

The pattern generalises well beyond arithmetic: handlers keyed by message type,
formatters keyed by file extension, validators keyed by field name. It is the
same idea as the menu earlier in the track, and it is worth reaching for
whenever a chain of `elif` is comparing one value against a list of constants.

Where an `if` chain is still better: when the conditions are not simple equality
&mdash; ranges, combinations, anything needing `and` &mdash; a dictionary cannot
express the question, and forcing it to is worse than the chain.

## Getting the items out in a useful order

A dictionary keeps insertion order, which is rarely the order you want to
report in. `sorted` takes the same `key` argument here as everywhere else, and
`d.items()` gives it pairs to work with.

Sorting by key is `sorted(d.items())`, which works because tuples compare
element by element and the key is first. Sorting by value needs a key function
that reaches for the second element &mdash; `key=lambda kv: kv[1]`, or
`key=itemgetter(1)` &mdash; and adding `reverse=True` gives you largest first.
For a top-n rather than a full sort, `heapq.nlargest(3, d.items(), key=...)`
does less work, and `Counter.most_common(3)` does it for you when the values
are counts.

The result is a list of tuples, not a dictionary. If you need a dictionary back
in that order, wrap it: `dict(sorted(d.items()))` builds a new one, and since
3.7 the insertion order it gets is the sorted order you just produced. This is
the standard way to produce a "sorted dictionary" in Python, and it is worth
knowing that it is a snapshot &mdash; later insertions go on the end, not into
their sorted position.

One detail that bites when sorting by value: ties come out in whatever order
they were already in, because `sorted` is stable. That is usually what you
want, and when it is not, the fix is a tuple key that names the tiebreak
explicitly, such as `key=lambda kv: (-kv[1], kv[0])` for "highest count first,
then alphabetical".

## Comprehensions over dictionaries

The methods on this page and dictionary comprehensions cover the same ground
from two directions, and knowing which reads better saves a lot of loops.

A comprehension is the right tool when you are building a new dictionary from
an old one: filtering out entries below a threshold, transforming every value,
swapping keys and values, or building a lookup table from a list of records.
`{k: v for k, v in d.items() if v > 0}` is one line, and the alternative is
three lines with an accumulator.

The methods are the right tool when you are updating a dictionary in place, or
when the operation has a name &mdash; `update`, `setdefault`, `pop`. Rebuilding
a whole dictionary with a comprehension in order to change one entry is
wasteful and reads as though something more complicated is happening.

The case where people reach for the wrong one is counting and grouping. A
comprehension cannot accumulate, because each iteration produces an independent
entry with no access to what came before. That is exactly why `Counter`,
`setdefault` and `defaultdict` exist, and why a grouping loop stays a loop.

## Questions people ask

<strong>Is `d.get(k)` the same as `d[k]` with a `try`?</strong> Effectively yes,
and `get` is clearer. Use brackets when a missing key means a bug.

<strong>Why did my loop raise "dictionary changed size during iteration"?</strong>
Because you added or removed a key while iterating a live view. Iterate
`list(d)` instead.

<strong>What is the difference between `update` and `|`?</strong> `update`
modifies in place and returns `None`; `|` returns a new dictionary and leaves
both operands alone.

<strong>Are dictionaries sorted?</strong> No. They keep insertion order, which
is not the same thing. `sorted(d.items())` when you want sorted.

<strong>How do I invert a dictionary?</strong>
`{v: k for k, v in d.items()}`, remembering that duplicate values collapse
&mdash; the last one wins.

<strong>Is `defaultdict` always better than `setdefault`?</strong> No.
`defaultdict` creates an entry on any missing lookup, including a typo, which
can hide bugs. Use it when every access should create a default.

<strong>How do I get the first key?</strong> `next(iter(d))`. There is no
indexing, because a dictionary is not a sequence.

<strong>Can I use `+` to merge two dictionaries?</strong> No. Use `|` on 3.9 and
later, `{**a, **b}` before that, or `update` for in-place.

<strong>Does `pop` work without a key?</strong> `popitem()` removes and returns
the last inserted pair, which is useful for draining a dictionary in a loop.

<strong>How do I count without importing Counter?</strong>
`d[k] = d.get(k, 0) + 1` in a loop. `Counter` is faster and clearer, but the
one-liner is worth knowing for when the import is not worth it.

<strong>What happens if I use an unhashable key by mistake?</strong> You get
`TypeError: unhashable type: 'list'` at the moment of insertion, which names
the type and is one of the clearer error messages in the language.

<strong>Is there a frozen dictionary?</strong> Not in the standard library.
`types.MappingProxyType(d)` gives a read-only view of one, which covers most of
the reasons people want it.

## Recap in one screen

- `get` reads with a fallback, `setdefault` reads and inserts, `defaultdict`
  inserts on every miss &mdash; pick by what should happen to the dictionary.
- `items()` is the loop you usually want; `keys()`, `values()` and `items()`
  are live views, not snapshots.
- Iterate `list(d)` whenever the loop body might change the dictionary.
- Keys must be hashable, which means immutable all the way down; tuples are
  the standard multi-part key.
- A dictionary of functions replaces a chain of `elif` that is testing one
  value against constants.
""")


extend("loop_else", """
## The same else, on try

`else` appears in a third place in Python, and seeing it there is what makes the
loop version stop feeling arbitrary:

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
guarding against did not occur* &mdash; the exception did not fire, the search
did not find an early exit.

Read that way, the loop version is consistent with the rest of the language
rather than an oddity bolted on. It is still a badly chosen keyword, because
"else" in an `if` means "the condition was false" and in these two places it
means "the interruption did not happen". But there is one idea behind both, and
knowing it is easier than memorising two unrelated rules.

The `try` version has a second, practical reason to exist: it keeps the `try`
block down to the line that can actually raise. Code that should only run on
success goes in the `else`, where it is not accidentally protected by the
`except`, so an unrelated `ValueError` from the success path is not silently
caught by a handler meant for the parse.

## A worked example: searching nested data

The shape `for/else` fits is a search that has to report failure, and nesting
is where the flag-based alternative starts to hurt:

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
that has to be initialised before the loop and checked after it, and the
failure branch sits visually attached to the loop it belongs to.

The equivalent with a flag is four lines longer and has three places to make a
mistake: forgetting to initialise, forgetting to set it, and checking it with
the wrong sense. None of those are hard mistakes to avoid, and all of them are
mistakes that get made.

## Where it sits among break and continue

The three of them describe what happens to a loop, and it helps to hold them
together.

`break` leaves the loop immediately, skipping the `else`. It is the only thing
that skips the `else`, which is the entire rule.

`continue` skips the rest of the current iteration and goes on to the next one.
It does not affect the `else` at all &mdash; a loop that `continue`s every
single time still finishes normally, and the `else` still runs.

`return` inside a loop leaves the function altogether, so the `else` never runs
and neither does anything after the loop. This is why a search written inside a
function usually does not need `for/else`: returning early makes the failure
case the last line of the function, which most readers find easier than an
attached block.

The one that surprises people is the empty sequence. A loop over an empty list
runs zero times, never breaks, and therefore *does* run its `else`. If you read
`else` as "if the loop did not run", this is precisely backwards, and it is the
case worth testing yourself on.

## Reading it in real code

The reason to learn a construct you may choose not to write is that you will
meet it. `for/else` appears in the standard library and in long-lived
codebases, usually in exactly the search-and-report-failure shape described
here, and occasionally in parsing code where several loops each have their own
failure branch.

When you meet one, the reliable move is to find the `break`. If there is one,
the `else` is the no-break branch and the loop is a search. If there is no
`break` anywhere in the body, the `else` is decoration and means nothing at all
&mdash; and that is worth noticing, because it is usually a sign that somebody
wrote it expecting a different behaviour.

## Why it is still in the language

Features this misunderstood usually get removed, and this one has not been,
which is worth a moment.

It cannot be removed without breaking working code, and the amount of Python in
existence that uses it is small but real. More to the point, the behaviour is
not wrong &mdash; it does something useful, has no edge cases, and the only
complaint anyone makes is about the keyword. Changing the keyword would break
just as much code as removing the feature, and adding `nobreak` as a synonym
would mean two ways to write one thing, which the language actively avoids.

So it stays, mildly awkward and occasionally useful, and the practical position
for anyone learning Python is the one this page has taken throughout: learn to
read it fluently, and make your own choice about writing it. Neither choice is
wrong. What is wrong is meeting one in unfamiliar code and guessing.

## Testing a loop that has one

If you do write `for/else`, it has two paths and both deserve a test, which is
easy to forget because the failure path has no code of its own to point at.

The three cases that matter are: the item is found, so the `break` fires and
the `else` is skipped; the item is absent from a non-empty sequence, so the
loop finishes and the `else` runs; and the sequence is empty, which also runs
the `else`. That third case is the one most likely to be missing from a test
suite and most likely to be wrong in the code, because it is the case where the
plain-English reading of "else" and the actual behaviour disagree.

If the empty case should behave differently from the not-found case &mdash; and
sometimes it should, because "you gave me nothing to search" is not the same
answer as "I searched and it is not there" &mdash; then `for/else` cannot
express that on its own, and an explicit check before the loop is the honest
way to say it.

## Questions people ask

<strong>Does the `else` run if the loop body never executes?</strong> Yes. Zero
iterations means no `break`, so the `else` runs. This is the case most people
guess wrong.

<strong>Does `continue` skip the `else`?</strong> No. Only `break` does.

<strong>Does `return` inside the loop run the `else`?</strong> No &mdash; the
function has already left.

<strong>Does an exception skip the `else`?</strong> Yes, unless it is caught
inside the loop. The exception propagates and nothing after the loop runs.

<strong>Can I use `else` on a comprehension?</strong> No. The `else` you can
write inside a comprehension is part of a conditional expression, which is an
unrelated feature.

<strong>Is there an `else` for `while`?</strong> Yes, with the same rule: it
runs when the condition became false, and not when a `break` ended the loop.

<strong>Should I use it in code others will read?</strong> In a short function
where the loop is a search, yes. Buried in a long function, a comment or an
early `return` may serve the next reader better.

<strong>Do other languages have this?</strong> Very few. It comes from a
long-standing idea in structured programming, and Python is the mainstream
language most associated with it, which is part of why it is unfamiliar.

<strong>Does a linter complain about it?</strong> Some flag a loop `else` with
no `break` in the body, which is exactly the case where it means nothing. That
is a useful warning to have switched on.

<strong>Can I use `break` inside a nested loop and reach the outer
`else`?</strong> No. `break` leaves only the loop it is in, so it skips that
loop's `else` and leaves the outer one to finish normally.

## Recap in one screen

- The `else` on a loop runs when the loop finished without a `break` &mdash;
  read it as `nobreak`.
- Zero iterations still counts as finishing, so the `else` runs for an empty
  sequence.
- `continue` does not affect it; `break` and `return` are what skip it.
- It replaces the found-flag pattern in searches, removing a variable and two
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
files written on other systems, and because it does not leave an empty string
at the end from the final newline. `encoding="utf-8"` appears on both calls,
because the default is the platform's and the platform's is not yours.

For a file of this size, reading it whole is fine. The version that scales is
the loop over the open file, which holds one line at a time:

```python
with path.open(encoding="utf-8") as f:
    for line in f:
        name, score = line.split()
```

Both are correct. The difference only matters when the file stops fitting in
memory, which is the point at which it matters a great deal.

## What `with` actually is

`with` is not special syntax for files. It works with any object implementing
two methods, and knowing that turns it from a rule into a tool.

An object is a **context manager** if it has `__enter__`, called on the way in,
and `__exit__`, called on the way out. `open` returns one, so does a lock, a
database connection, a temporary directory, and anything from `contextlib`.
`__exit__` runs whether the block finished normally, returned, or raised, which
is the guarantee the whole construct exists to provide.

The `as` name receives whatever `__enter__` returns &mdash; for a file, the
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

Everything before the `yield` is setup, everything after is cleanup, and the
`yield` is where the body of the `with` runs. This is the same generator
machinery from elsewhere in the track, used for a completely different purpose.

Several managers can share one statement:
`with open(a) as f, open(b, "w") as g:` opens both and closes both, in reverse
order, even if the second `open` raises.

## Do not parse standard formats by hand

The single most common mistake with files is treating a structured format as
plain text. CSV is the usual victim, because it looks like `split(",")` will
work, and it does until a field contains a comma inside quotes &mdash; at which
point the parse silently produces the wrong number of columns.

The standard library has a module for each of the formats you are likely to
meet. `csv` handles quoting, embedded newlines and different delimiters, and
`csv.DictReader` gives you dictionaries keyed by the header row. `json` handles
escaping, Unicode and nesting, and round-trips to Python types.
`configparser` reads INI files. `sqlite3` is there when a file of records has
started to want queries.

Each of them costs one import and removes an entire category of bug you would
otherwise discover on somebody else's data. The rule is worth stating plainly:
if the format has a name, something in the standard library already reads it.

## Where file code goes wrong in practice

Four failures account for most of it, and none of them are exotic.

**The path is relative to the wrong place.** A relative path is resolved
against the process's working directory, not the script's location, so the same
program works when run from its own folder and fails from anywhere else. If a
file lives beside the script, `Path(__file__).parent / "data.txt"` says so.

**The file is open longer than intended.** A file opened without `with` and
never closed keeps a handle and, on writes, keeps data in a buffer that has not
reached the disk. On a short script the interpreter cleans up on exit and the
bug is invisible; in a long-running program it accumulates until the process
hits the operating system's limit.

**The encoding was assumed.** This is the failure that travels: it works on the
machine that wrote the file and raises `UnicodeDecodeError` on a colleague's.
Name the encoding on every text-mode open.

**The write was not atomic.** A program that dies mid-write leaves a truncated
file where the good one used to be. The write-then-rename pattern earlier on
this page costs two lines and removes the possibility.

## Line endings, and the translation you did not ask for

Text mode does more than decode bytes into characters: it also translates line
endings, and knowing that explains a family of confusing results.

Windows ends lines with carriage-return plus newline; everything else uses a
newline alone. Python's text mode hides the difference. On reading, any of the
variants becomes a plain newline in your string, which is why a loop over lines
behaves identically on every platform. On writing, a newline is translated back
into whatever the platform uses.

That is almost always what you want, and it has two consequences worth
knowing. First, the string you read is not byte-for-byte what is in the file,
so a length computed from the text can differ from the file size. Second, if
you open a file in binary mode you get no translation at all, and lines end
with whatever the file actually contains &mdash; which is why text read as
binary often shows a trailing carriage return that seems to have come from
nowhere.

The one place it actively causes trouble is the `csv` module, which does its
own line-ending handling. Opening a CSV without `newline=""` lets both layers
translate, and the result is a blank line between every row on Windows. The
documented fix is exactly that argument, and it is worth passing habitually
rather than discovering the need for it later.

`newline=""` is also what you want when reading a file whose exact line endings
matter &mdash; a diff tool, a formatter, anything that must write back what it
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
opening a CSV without `newline=""` produces doubled line endings. Pass
`newline=""` to `open` when using the `csv` module.

<strong>Can I read a file backwards?</strong> Not directly. Read the lines and
reverse them, or seek from the end if the file is too big for that.

<strong>What does `errors="replace"` do?</strong> Substitutes a placeholder for
bytes that cannot be decoded, so you get something rather than an exception.
Useful for salvage, not for data you care about.

<strong>Is `pathlib` slower than string paths?</strong> Marginally, and never
enough to matter next to the file system call that follows.

<strong>Can I open the same file twice?</strong> Yes, and on most systems you
can even open it for reading and writing at once. Whether that is a good idea
is a different question.

<strong>What does `f.seek(0)` do?</strong> Moves the position back to the
start, which is how you read a file a second time without reopening it.

<strong>Why is my file empty until the program ends?</strong> Because the data
is still in a buffer. Closing the file &mdash; which `with` does &mdash; or
calling `f.flush()` writes it out.

<strong>Should I use `os.path` or `pathlib`?</strong> `pathlib` for new code.
`os.path` is not deprecated and you will keep meeting it, so both are worth
reading fluently.

<strong>How do I append to a file that might not exist?</strong> Mode `"a"`
creates it if it is missing, so no check is needed.

## Recap in one screen

- `with` closes the file whether the block ends normally or raises; it is the
  correct way to open one, not a style choice.
- Iterating the file object reads one line at a time and works on files larger
  than memory.
- `"w"` truncates on open; `"a"` appends; `"x"` refuses to overwrite.
- Name `encoding="utf-8"` on every text-mode open, because the default varies
  by machine.
- If the format has a name &mdash; CSV, JSON, INI &mdash; use the module rather
  than splitting strings.
""")


extend("sorted_with_key", """
## A worked example: ranking records

The shape that comes up constantly &mdash; sort records by one field, break
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

The key returns a tuple, so the sort compares scores first and names only where
scores tie. The minus sign reverses the score alone, which `reverse=True` could
not do &mdash; it would have reversed the names as well, putting `cy` before
`ana`.

This is worth having in your fingers, because "highest first, then
alphabetical" is what almost every leaderboard, report and ranking actually
wants, and it is one expression rather than a comparison function.

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

This is deliberate. Languages that allow it produce orderings that depend on
implementation details, and the resulting bugs are far worse than an exception.
The fix is to say what you mean with a key: `key=str` to sort them as text,
`key=int` if they are all numeric in disguise.

`None` is the version of this that shows up in real data, because a missing
field is very often `None` and `None` cannot be compared with anything. Rather
than filtering the rows out, put the missing ones at one end:

```python
rows = [("ana", 91), ("bo", None), ("cy", 78)]
print(sorted(rows, key=lambda r: (r[1] is None, r[1])))
```

```
[('cy', 78), ('ana', 91), ('bo', None)]
```

The first element of the key is a boolean, and `False` sorts before `True`, so
everything with a value comes first and the missing ones collect at the end.
Swap it to `r[1] is not None` to put them first instead. The second element is
only ever compared between rows that agree on the first, so `None` is never
compared with a number.

## Case, accents and numbers inside strings

Sorting text has three traps that only appear once the data stops being tidy.

**Case.** The default sort is by code point, so every capital letter sorts
before every lowercase one and `["banana", "Apple"]` comes back with `Apple`
first. `key=str.lower` fixes it, and `key=str.casefold` is the stricter version
for text that is not guaranteed to be English.

**Accents.** `é` sorts after `z` by code point, which is wrong in every
language that uses it. The standard library's `locale.strxfrm` sorts according
to the user's locale, and for anything serious the `PyICU` library does it
properly. For an internal report, `unicodedata.normalize` plus stripping the
combining marks is often enough.

**Numbers inside names.** `["file10", "file2"]` sorts with `file10` first,
because `1` is before `2` as text. This is the "natural sort" problem, and the
fix is a key that splits the string into text and numeric runs and converts the
numeric ones, so the comparison happens between integers rather than digits.

All three have the same shape as everything else on this page: the data is not
what you want to compare, so transform it in the key and leave it alone in the
result.

## What sorting costs, and when not to

Python's sort is Timsort, which is O(n log n) in general and considerably
faster than that on data with existing order &mdash; already-sorted input is
close to linear, and so is data made of sorted runs. That is not an accident;
it was designed for real data, which is usually partly ordered.

The practical consequence is that sorting is cheap enough to stop thinking
about at ordinary sizes. Where it is worth thinking about is when you do not
actually need a sorted sequence:

If you want the single largest or smallest item, `max` and `min` take the same
`key` and do it in one pass rather than n log n. If you want the top few,
`heapq.nlargest(k, items, key=...)` beats sorting when k is small relative to
n. If you want to know whether anything qualifies, `any` with a generator stops
at the first hit. And if you are sorting the same list repeatedly inside a
loop, sort it once outside the loop instead.

The one that catches people is sorting to find a maximum. `sorted(items)[-1]`
is correct, does far more work than necessary, and reads less clearly than
`max(items)`.

## Grouping, which needs sorting first

`itertools.groupby` collapses runs of equal items into groups, and it is the
most common reason to sort something you did not otherwise need in order.

The important property is that it only groups *adjacent* items. It walks the
sequence once and starts a new group whenever the key changes, which means
unsorted input produces a group every time the value changes back and forth
rather than one group per distinct value. Sorting by the same key first is what
makes the grouping complete, and forgetting to is the single mistake everyone
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
the groups are iterators over the original sequence, not lists, and they become
invalid once you move to the next group &mdash; which is why the example
materialises each one inside the loop rather than collecting the groups and
using them afterwards.

For grouping without sorting, a `defaultdict(list)` and a single loop is
simpler, does not require order, and gives you real lists. `groupby` earns its
place when the data is already sorted, when the sequence is too large to hold,
or when you want the runs rather than the totals.

## Making your own objects sortable

`key=` handles most cases, and occasionally the ordering belongs to the object
itself rather than to one call site. Then the object should carry it.

Defining `__lt__` is enough for `sorted`, `min` and `max`, because they need
only "is this one less than that one". The other comparisons &mdash; `<=`, `>`,
`>=` &mdash; are separate methods and are not inferred, so an object with only
`__lt__` sorts correctly and raises on `>=`. `functools.total_ordering` fills
the rest in from `__lt__` and `__eq__`, at a small runtime cost.

The shorter route is a dataclass. `@dataclass(order=True)` writes all six
comparison methods, comparing the fields in the order they are declared, which
is exactly the tuple-key behaviour with the tuple written for you. Fields you
do not want in the comparison are excluded with
`field(compare=False)`, which is how you keep a name or an id out of the
ordering while leaving it on the object.

The judgement is about where the ordering belongs. If there is one natural
order for the type &mdash; a version number, a date range, a playing card
&mdash; put it on the class and every call site benefits. If different callers
want different orders, `key=` at each call site is the honest answer, and
building one in as "the" order will mislead the next reader.

One rule applies whichever you choose: the ordering must be consistent with
equality, and it must be total. Objects that compare equal must not also
compare less-than, and every pair must be comparable. A sort that receives an
inconsistent ordering does not raise; it produces a result that is quietly
wrong and changes with the input order.

## Questions people ask

<strong>Can `key` return anything?</strong> Anything comparable with itself.
Numbers, strings and tuples of those are the usual choices.

<strong>How do I sort descending by one field and ascending by another?</strong>
Negate the descending one in a tuple key, or do two stable sorts, least
significant first.

<strong>Does `sorted` work on a dictionary?</strong> Yes, and it sorts the keys.
Use `d.items()` when you want pairs.

<strong>Is `reverse=True` the same as reversing afterwards?</strong> Not
exactly. `reverse=True` keeps ties in their original order; sorting then
reversing flips the ties too.

<strong>What happened to `cmp`?</strong> Removed in Python 3. If you genuinely
need a comparison function, `functools.cmp_to_key` converts one into a key.

<strong>Can I sort a generator?</strong> Yes &mdash; `sorted` accepts any
iterable and returns a list. It has to consume the whole thing to do it.

<strong>Why is my sort not stable?</strong> It is. If tied items appear to
move, the key is distinguishing them in a way you did not intend.

<strong>Does sorting a list of dictionaries need a key?</strong> Yes.
Dictionaries are not orderable, so without one you get a `TypeError`.

<strong>How large can a list be before sorting is slow?</strong> Far larger
than most programs handle. Sorting a million small items takes well under a
second, and the cost is usually dominated by whatever built the list.

## Recap in one screen

- `key` transforms each item once and sorts on the result; the items you get
  back are unchanged.
- A tuple key gives tiebreaks; negate a number to reverse one field without
  reversing the rest.
- `sorted` returns a new list, `.sort()` returns `None` &mdash; that `None` is
  the convention for every in-place method.
- The sort is stable, which is what makes two-pass sorting work.
- `max`, `min`, `heapq.nlargest` and `groupby` take the same `key`; reach for
  them when you do not need everything in order.
""")


extend("generators_and_yield", """
## Watching a pipeline run

The claim that a generator pipeline handles one item at a time end to end is
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

Nothing is batched. `numbers` produces one value, `doubled` transforms that one
value, the loop receives it, and only then does anything ask for the second.
The list-building equivalent would have printed all three "produced" lines
first, then all three "doubled" lines.

This is the whole argument for generators in six lines of output. Memory stays
flat because only one item is in flight, and if the loop stopped after the
first value, `numbers` would never produce the third.

## A generator is an iterator, and what that means

`for` is not special syntax for lists. It calls `iter()` on whatever it is
given to get an iterator, then calls `next()` on that repeatedly until
`StopIteration` is raised, and that exception is what ends the loop.

A generator function returns an object implementing exactly that protocol, which
is why it works everywhere a list does &mdash; in a `for`, in `sum`, in
`list()`, in unpacking. It is also why the same object can only be walked once:
an iterator holds a position, and there is no way to move it backwards.

Seeing the protocol directly makes the behaviour concrete:

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
time, which is why a list can be looped over repeatedly; `iter()` on a
generator returns the generator itself, which is why it cannot. And a `return`
inside a generator does not return a value to the caller &mdash; it raises
`StopIteration`, and any value goes on the exception rather than to the loop.

## Where generators surprise people

Three behaviours account for most of the confusion, and all three follow from
laziness.

**Nothing runs until you ask.** Calling a generator function executes none of
its body. If the first line validates an argument and raises, the exception
arrives at the first `next()`, not at the call &mdash; possibly in a completely
different function. Where that matters, split it: a normal function that
validates and then returns the generator.

**The values are computed late.** A generator expression that closes over a
variable reads that variable when it runs, not when it was written. Rebind the
variable in between and the generator sees the new value, which is the same
late-binding behaviour as the lambda-in-a-loop trap.

**Exhaustion is silent.** A second pass over a used generator produces nothing
and raises nothing. The symptom is an empty result far from the cause, and the
diagnosis is almost always that something already consumed it &mdash;
frequently a `sum()` or a `len(list(...))` written for a debugging print.

The habit that avoids all three: decide early whether a thing is a stream or a
collection. If it is a collection, call `list()` on it once and pass the list
around.

## send, throw and close

A generator can also receive values, which is the feature that made Python's
coroutines possible before `async` existed.

`g.send(value)` resumes the generator and makes the paused `yield` expression
evaluate to `value`, rather than to `None` as it does with `next()`. That turns
the generator from a producer into something that can be fed &mdash; the
classic example is a running average that accepts numbers and yields the mean
so far.

`g.throw(exc)` raises an exception at the point of the `yield`, letting the
generator handle it or clean up. `g.close()` raises `GeneratorExit` there,
which is what lets a `finally` or a `with` inside a generator run its cleanup
when the generator is discarded.

In everyday code you will use none of these directly. They are worth knowing
because they explain things you will see: why `contextlib.contextmanager` can
turn a generator into a `with` block, why a `with` inside a generator is safe,
and why `async def` looks so much like a generator &mdash; it grew out of one.

## Generators against the class you would otherwise write

Before generators, producing a sequence lazily meant writing a class with the
iterator protocol on it by hand. Comparing the two is the clearest way to see
what `yield` actually saves.

The class version has to store its own state as attributes, decide in `__next__`
what to do next based on those attributes, and raise `StopIteration` itself
when it is finished. Anything with a loop in it becomes a state machine: what
was a `for` and an `if` turns into a counter, a flag, and a chain of
conditionals reconstructing where it had got to.

The generator version stores the state implicitly. The local variables, the
position in the loop, the depth of the nesting &mdash; all of it is the paused
frame, and `yield` is where it pauses. That is why a generator for walking a
nested structure is four lines and the equivalent class is thirty: recursion
and loops carry the state for you, and a class has to make it explicit.

There is still a case for the class. It can hold methods other than iteration,
it can be reset, it can expose its position, and it can implement `__len__` so
that `len()` works. A generator can do none of those. When the object is a
collection with an order, a class is right; when it is a process that produces
values, `yield` is right.

The practical version of that rule: if you find yourself writing
`self.index`, `self.buffer` and a `__next__` full of branches, the code you
meant to write is a generator function with a loop in it.

## Questions people ask

<strong>What is the difference between a generator and a list
comprehension?</strong> Brackets. `[x for x in y]` builds a list;
`(x for x in y)` produces values on demand.

<strong>Can I get the length of a generator?</strong> Not without consuming it.
`sum(1 for _ in g)` counts it, and leaves it exhausted.

<strong>Can a generator have a `return`?</strong> Yes, and it ends the
generator. The returned value is attached to `StopIteration` rather than handed
to the loop.

<strong>Are generators faster than lists?</strong> Not per item. They are
faster to start, use far less memory, and avoid work the consumer never asks
for.

<strong>Can I index a generator?</strong> No. Use `itertools.islice` to skip
and take, or build a list.

<strong>What is the difference between `yield` and `yield from`?</strong>
`yield` produces one value; `yield from` produces every value of another
iterable, and passes `send` and `throw` through to it.

<strong>Why does my generator not raise until later?</strong> Because the body
does not run until the first value is requested.

<strong>Can I nest generator expressions?</strong> Yes, and the inner one is
consumed lazily too. Readability is usually the limit rather than any
technical one.

<strong>Do generators work with `in`?</strong> Yes, and the test consumes the
generator up to the match, leaving the rest. Testing twice will not behave the
way you expect.

<strong>Is a file object a generator?</strong> Not exactly, but it is an
iterator over lines, which is why `for line in f` works and why it too can only
be walked once without seeking back.

<strong>Can two loops share one generator?</strong> They can consume it between
them, each taking whatever the other has not. That is occasionally useful and
much more often a bug.

<strong>What happens to a generator I stop halfway?</strong> It stays paused
until it is garbage-collected, at which point `GeneratorExit` is raised inside
it so `finally` blocks and `with` statements can clean up.

## The one-line summary worth carrying

A generator is a function that produces a sequence instead of returning a
value, and it does it one item at a time, on demand, remembering exactly where
it stopped.

Everything else on this page is a consequence of that sentence. The memory
saving is because only one item exists at a time. The single pass is because a
paused function cannot be rewound. The infinite sequences are because nothing
is built in advance. The late exceptions are because the body has not run yet.
And the pipelines work because a generator consuming another generator is
still only asking for one item.

## Recap in one screen

- A generator function returns an object; the body runs only when values are
  asked for.
- One pass, no length, no indexing &mdash; call `list()` when you need any of
  those.
- Memory is flat regardless of the size of the sequence, which is what makes
  infinite sequences and huge files workable.
- A pipeline of generators moves one item end to end at a time, doing no work
  the consumer does not ask for.
- `for` works by calling `next()` until `StopIteration`; a generator simply
  implements that protocol.
""")


extend("zip_function", """
## A worked example: comparing two lists

The job `zip` was made for, with `enumerate` supplying the position so the
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
`zip` produced, so the brackets take it apart in the same statement. Written
without them you would get `i` and a tuple, and would have to index into it on
the next line.

This is the shape behind most comparison code: diffing two versions of a
record, checking a result against a fixture, lining up a header row with a data
row. Note what it does *not* do &mdash; if the lists are different lengths, the
extra rows are never examined, and the report is silently incomplete. That is
the argument for `strict=True` in one sentence.

## Transposing with a star

Combining the star and `zip` turns rows into columns:

```python
matrix = [[1, 2, 3], [4, 5, 6]]
print(list(zip(*matrix)))
```

```
[(1, 4), (2, 5), (3, 6)]
```

`*matrix` passes each row as a separate argument, so `zip` receives two
iterables and takes one item from each in turn &mdash; which is exactly a
transpose. The result is a list of tuples rather than lists, and the rows must
be the same length or the short one truncates everything, both of which are
the ordinary `zip` rules applied in an unusual place.

This is the same operation as unzipping a list of pairs, which is why both are
written `zip(*something)`. A list of pairs *is* a two-column matrix, and
transposing it gives you the two columns.

## Where zip removes an index

The value of `zip` is easiest to see by looking at what it replaces. The
index-based version of walking two lists together has to create a counter,
bound it correctly, and reach back into both lists on every line that uses a
value.

Each of those is a place to be wrong. The counter can start at one. The bound
can use the wrong list's length, which is fine until the lists differ. The
lookups can be transposed, so that names are read from the scores list. None of
these produce an error; they produce wrong output, which is worse.

`zip` removes all three at once by handing you the values directly. There is no
counter to get wrong, no bound to compute, and no lookup to transpose, because
the names arrive already bound to the right variables. This is the same
argument as `for item in items` over `for i in range(len(items))`, applied to
more than one sequence.

The index is still available when you want it &mdash; that is what `enumerate`
around a `zip` is for &mdash; but now it is there because you asked, rather
than because iteration required it.

## The other things that produce pairs

`zip` is one of several things in Python that yield tuples, and they all pair
with the same unpacking syntax. Recognising the family makes a lot of loops
read the same way.

`enumerate(items)` yields `(index, item)`. `dict.items()` yields
`(key, value)`. `zip(a, b)` yields `(a_item, b_item)`. `itertools.pairwise`
yields consecutive overlapping pairs from one sequence, which is what you want
for comparing each item with the next.

All four are consumed identically: `for x, y in thing`. The unpacking is not a
feature of any of them; it is the ordinary tuple unpacking from elsewhere in
the track, applied to whatever the loop happened to produce. That is why
`for k, v in d.items()` works, and why forgetting `.items()` gives you keys and
a confusing error rather than a helpful one.

They also combine. `zip(a, b, c)` for three sequences, `enumerate(zip(a, b))`
for a position alongside a pair, `zip(d.keys(), d.values())` for the long way
of writing `d.items()`.

## Parallel lists, and when zip is patching a design problem

`zip` is the right tool for sequences that genuinely correspond, and it is also
what lets a questionable data model keep working, so it is worth knowing which
situation you are in.

Two lists are parallel when item *i* of one describes the same thing as item
*i* of the other. Nothing in the language enforces that. It is an invariant
living entirely in the programmer's head, and every operation has to preserve
it: sorting one list without the other breaks it, filtering one breaks it,
appending to one and forgetting the other breaks it, and none of those raise.

The failure is quiet and it compounds. A sort applied to `names` but not to
`scores` produces output where every name has somebody else's score, and the
program reports it confidently. There is no assertion that could have caught it
without comparing against a source of truth that no longer exists.

When the lists are built together and consumed together in one function, that
risk is contained and `zip` is exactly right. When they are stored on an
object, passed between functions or returned from an API, the invariant has to
survive code that nobody has written yet, and the better structure is one list
of records &mdash; tuples, dictionaries, dataclasses &mdash; where the name and
the score are in the same object and cannot be separated.

The tell is a sort. If you find yourself sorting two lists in step, or writing
`zip`, sorting the pairs, and unzipping them again, the data wanted to be pairs
all along.

## Deciding what unequal lengths mean

Three behaviours are available and the choice is about what a mismatch would
signify in your program. It is worth deciding deliberately rather than taking
the default.

**Truncating is right when one side is genuinely open-ended.** Pairing a finite
list against an infinite counter, taking as many rows as you have templates,
reading until the shorter source is exhausted &mdash; here stopping at the
shortest is the whole point, and the default does what you want.

**Raising is right when equal lengths are an invariant.** Two lists built from
the same source, a header row and a data row, expected and actual results: if
they differ, something upstream is broken and every line of output after that
point is suspect. `strict=True` converts a wrong answer into an exception,
which is almost always the better outcome.

**Padding is right when the missing items have a meaning.** Filling absent
values with `None`, zero or a default, so that the shorter list is treated as
incomplete rather than as terminating the whole operation.
`itertools.zip_longest` does this, and choosing the fill value is choosing what
"missing" means in the result.

The default is the truncating one, which means it is the choice you make by not
choosing. On anything where a mismatch would be a bug, that is the wrong
default, and one keyword argument fixes it.

## Comparing each item with the next

A close relative of zipping two lists is zipping one list against itself, offset
by one, which pairs every item with its successor.

`zip(items, items[1:])` does it directly: the second argument starts one
position later, so the first pair is items 0 and 1, the second is 1 and 2, and
the whole thing stops one short of the end because the offset list is one
shorter. That truncation is the default behaviour doing exactly the right
thing for once.

This is the shape for any question about consecutive items: are the values
increasing, where are the gaps in a sequence of dates, what is the difference
between each reading and the last. Written with indices it needs a loop from 1
to `len(items)` and two lookups per pass; written this way it is one line and
has no index at all.

Since Python 3.10 `itertools.pairwise(items)` does the same thing without the
slice, which matters when the input is a generator and cannot be sliced.

## Questions people ask

<strong>What does `zip` return?</strong> An iterator of tuples. Wrap it in
`list()` to see it or to keep it.

<strong>Can I zip more than two things?</strong> Yes, any number. Each pass
yields a tuple with one item from each.

<strong>What if the lists are different lengths?</strong> It stops at the
shortest, silently. `strict=True` raises instead, from Python 3.10.

<strong>How do I pad the shorter one?</strong> `itertools.zip_longest`, which
fills with `None` or a value you choose.

<strong>Can I zip a dictionary?</strong> Yes, and you get its keys, because
that is what iterating a dictionary gives. Use `.items()` for pairs.

<strong>Why did my second loop over a zip do nothing?</strong> Because it is an
iterator and the first loop consumed it. Build a list if you need it twice.

<strong>Does `zip` copy the data?</strong> No. It holds references and produces
tuples on demand, so it works on generators and infinite sequences.

<strong>Is `zip` the same as a database join?</strong> No, and the difference
matters. A join matches rows by a key; `zip` matches them by position, and has
no idea whether the things it paired belong together.

<strong>Can I zip strings?</strong> Yes. A string is iterable, so
`zip("abc", "xyz")` pairs the characters.

## Recap in one screen

- `zip` walks several iterables in step and yields one tuple per position,
  which removes the index and everything that can go wrong with it.
- It stops at the shortest input without a word; use `strict=True` when equal
  lengths are an assumption rather than a coincidence.
- `zip(*pairs)` unzips, and `zip(*matrix)` transposes &mdash; the same
  operation seen from two angles.
- `dict(zip(keys, values))` is the standard way to build a mapping from two
  parallel lists.
- It is lazy, so it works on generators and can only be walked once.
""")


extend("dict_and_set_comprehensions", """
## A worked example: a lookup table and a grouping

The two jobs that send people to a dict comprehension, side by side &mdash;
because only one of them is actually a comprehension:

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

The first is a comprehension because each row produces exactly one entry, and
later rows are allowed to overwrite earlier ones. The second is a loop because
each row *adds to* an entry, and a comprehension cannot do that &mdash; every
iteration produces an independent key and value, with no access to what the
dictionary already holds.

That is the dividing line, and it is worth stating as a test: if the value for
a key depends only on the current item, a comprehension works. If it depends on
the other items too &mdash; a count, a list, a running total &mdash; you need a
loop, a `defaultdict`, or a `Counter`.

## Scope, and the variable that does not leak

A comprehension has its own scope, which is why the loop variable does not
survive it:

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
a whole class of accidental overwrites and is the behaviour to rely on.

Two consequences follow. The variable is unavailable afterwards, so a
comprehension cannot be used to compute something you then want to inspect
&mdash; that needs a loop. And the comprehension can still *read* names from
the enclosing scope, which is what makes `[x for x in items if x > threshold]`
work.

The one place this surprises people is inside a class body, where the
comprehension's scope cannot see the class's other names. A comprehension in a
class body that refers to another class attribute raises `NameError`, and the
fix is to compute it outside the class or pass it in through the iterable.

## Sets, and the operations that follow

Building a set with a comprehension is usually the first half of a job whose
second half is set algebra, and the two together replace a surprising amount of
loop-and-flag code.

`{r["city"] for r in rows}` gives the distinct cities. Once you have two such
sets, `a - b` is "in the first and not the second", `a & b` is "in both", and
`a ^ b` is "in one but not both". Those three answer most of the questions
people write nested loops for: which records are new, which have disappeared,
which are shared.

The comprehension form matters here because it does the deduplication as it
goes. Writing `set([r["city"] for r in rows])` builds the whole list first and
then discards the duplicates, which is more memory for the same answer. For a
large input the difference is real, and the direct form also states the intent
&mdash; uniqueness is the point, not a cleanup step afterwards.

What you give up is order and indexing. A set has neither, so if the result
feeds something that cares about sequence, sort it on the way out:
`sorted({...})` gives a list back in a defined order.

## Nesting, and the two conditionals

Comprehensions have two places a condition can appear, and they do different
things.

A trailing `if` filters &mdash; items that fail it produce nothing at all:
`{k: v for k, v in d.items() if v}` drops falsy values. A conditional
expression in the value slot chooses &mdash; every item produces an entry, and
the condition picks what goes in it:
`{k: v or 0 for k, v in d.items()}` keeps every key and substitutes a default.
Reaching for the wrong one gives you either missing keys or unwanted ones, and
the symptom is a dictionary of the wrong size.

Nesting a second `for` is legal and reads in the order written, outermost
first: `{c for row in grid for c in row}` collects every cell of a grid of
rows. The rule is that the clauses appear in the same order as the equivalent
nested loops, which is the opposite of the order people guess when they meet it
in someone else's code.

Both features are worth knowing and neither is worth combining. A comprehension
with two `for` clauses, a filter and a conditional value is a line that has to
be decoded rather than read, and the loop it replaces would have been four
clear lines.

## What is built, and when it matters

The four bracket forms differ in more than the type of the result: they differ
in what exists in memory while they run, and occasionally that is the deciding
factor.

A list, set or dict comprehension builds the whole result before anything else
happens. For a thousand items that is irrelevant. For ten million it is the
difference between a program that runs and one that does not, and the
generator expression &mdash; round brackets &mdash; is the version that holds
one item at a time.

The rule of thumb is what happens to the result. If it is consumed once, by a
`sum`, a `max`, a `for`, or an `any`, a generator expression does the same job
without materialising anything: `sum(x * 2 for x in items)` never builds a
list. If it is indexed, iterated twice, measured with `len`, or returned to a
caller who will do any of those, it has to be a real collection.

There is one case where building the intermediate is a genuine waste and easy
to miss: wrapping a list comprehension in a converter.
`set([f(x) for x in items])` and `dict([(k, f(k)) for k in keys])` both build a
list and immediately throw it away. Writing the set or dict comprehension
directly skips that entirely, which is one reason those forms exist at all.

The reverse mistake is reaching for a generator expression where a list is
wanted, and then calling `list()` on it. That builds the same list through more
machinery, and the comprehension says it more directly.

## Readability, stated as a limit

Every section here has hinted at a boundary, and it is worth making explicit,
because "use a comprehension when it is clear" is advice that gives no help at
the moment of writing.

A practical limit: one `for`, at most one `if`, and an expression short enough
that the whole thing fits on one line without wrapping. That covers the large
majority of genuine uses and produces something a reader takes in at a glance.

Past that, the questions to ask are whether a reader could say what the result
contains without tracing it, and whether it can be changed without being
rewritten. A comprehension that needs a comment above it to explain what it
produces has already answered both.

The escape hatch is usually a named function. Pulling the expression out into a
function with a meaningful name leaves a comprehension that is one `for` and a
call &mdash; readable again, and the complicated part now has a name, a place
to put a docstring, and somewhere to test it.

## Questions people ask

<strong>Why does `{}` give a dict and not a set?</strong> Dictionaries had the
braces first. `set()` is the only way to write an empty set.

<strong>Can I build a frozenset with a comprehension?</strong> Not directly.
`frozenset(x for x in items)` wraps a generator expression.

<strong>What happens to duplicate keys?</strong> The last one wins, silently.
Nothing warns you.

<strong>Is a dict comprehension faster than a loop?</strong> Slightly, because
the whole thing runs in one bytecode loop without repeated attribute lookups.
Not enough to be the reason to choose it.

<strong>Can I use `zip` inside one?</strong> Yes, and
`{k: v for k, v in zip(keys, values)}` is common &mdash; though
`dict(zip(keys, values))` is shorter when nothing is transformed.

<strong>Does the order of a dict comprehension matter?</strong> Yes. The result
keeps insertion order, so the order of the input decides the order of the
output.

<strong>Can I have an `else` without an `if` filter?</strong> Only in the value
slot, as part of a conditional expression. The trailing filter has no `else`.

<strong>Can a comprehension call a function with side effects?</strong> It
can, and it should not. A comprehension whose result is discarded is a loop
written to look like an expression.

<strong>Do comprehensions work in older Python?</strong> List comprehensions
since 2.0, dict and set comprehensions since 2.7 and 3.0. Anything current
supports all of them.

## Recap in one screen

- The brackets choose the type: `[]` list, `{}` set, `{k: v}` dict, `()`
  generator. Everything else about the syntax is identical.
- A comprehension works when each item produces one independent entry; counting
  and grouping need a loop, `setdefault` or `Counter`.
- Duplicate keys collapse silently, and so do duplicate set members &mdash;
  that is the point of a set and a hazard in a dict.
- The loop variable has its own scope and does not leak, except that it cannot
  see a class body's other names.
- A trailing `if` filters items out; a conditional expression in the value slot
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

The first two lines are the whole distinction. After a shallow copy, the inner
list is *the same object*; after a deep copy it is a new one. The last line is
the consequence: appending through the shallow copy changed the original, and
the deep copy was untouched.

Note that the outer dictionaries are different objects in both cases. A shallow
copy is a real copy &mdash; adding a new key to `shallow` does not affect
`original`. It is only one level deep, and every problem on this page comes
from the level below.

## Where this actually comes up

The trap is rarely met head-on. It arrives through four ordinary situations.

**Configuration loaded from JSON or YAML.** These are nested dictionaries by
nature, `.copy()` looks like it did the job, and a function that adjusts one
value has quietly adjusted it for everybody.

**A default that is a nested structure.** A module-level `DEFAULTS` dict copied
shallowly into each new object means every object shares the same inner
dictionaries. The objects look independent and are not.

**A list of records.** `rows[:]` gives a new list of the same dictionaries, so
sorting or filtering the copy is safe and editing a record through it is not.
This is a common one because the copy was made specifically to be safe.

**Undo, or "keep the original for comparison".** Snapshotting state before a
change is the exact case where a shallow copy fails: the snapshot shares the
mutable parts with the thing that is about to change, so by the time you
compare, both have moved.

The pattern across all four is that the copy was made for safety, and shallow
copying provides that safety only for the top level. If the reason for copying
is "so that changes over here do not affect over there", the question to ask is
how deep the changes go.

## Equality survives copying; identity does not

After any copy, shallow or deep, `copy == original` is `True` and
`copy is original` is `False`. That is the intended behaviour and it is worth
being explicit about, because it is how you check that a copy did what you
meant.

For your own classes it holds only if you defined `__eq__`. Without one,
Python compares by identity, so a copy of your object is *not* equal to the
original &mdash; which surprises people who have just written a careful
`__deepcopy__` and find their tests failing on the comparison rather than the
copy. Defining `__eq__` on a class whose instances get copied around is
effectively required, and a dataclass writes it for you.

`deepcopy` also preserves structure that a naive copy would flatten. If two
entries in a dictionary point at the same list, the deep copy has two entries
pointing at one *new* list &mdash; the sharing is reproduced rather than
duplicated. That is usually what you want, and it is one more thing a
hand-written recursive copy gets wrong.

## Immutability removes the question

The most reliable fix for a copying bug is to not need the copy.

If the structure is built from tuples, frozensets, strings and numbers, then
nothing inside it can change, so sharing it is safe and a shallow copy is a
complete one. The distinction that this whole page is about simply does not
arise. That is why nobody worries about copying a tuple of strings, and why
`deepcopy` on such a structure is wasted work.

The practical version is to make the things that travel immutable. A record
passed between functions is better as a frozen dataclass or a `NamedTuple` than
as a dictionary: it cannot be edited by a function that received it, so no
defensive copy is needed at any boundary. Where a modified version is required,
`_replace` or `dataclasses.replace` builds a new one and leaves the original
alone.

Keep the mutable structures local, where every name pointing at them is visible
in the same function. Then copying becomes a decision you make occasionally
rather than a defence you have to remember everywhere.

## Deciding, in four questions

When you are about to copy something and are not sure which kind you need, the
answer follows from four questions asked in order.

**Does anything inside it change?** If every item is a number, a string or a
tuple of those, any shallow copy is a complete one. Stop here; this covers most
copying.

**Am I copying so that changes over here do not affect over there?** If the
answer is no &mdash; you are copying to get a list you can sort, or to add one
key &mdash; then a shallow copy of the outer container is exactly what you
want and nothing more is needed.

**How deep do the changes go?** If the code that follows only touches the top
level, shallow is enough regardless of what is nested underneath. If it reaches
into nested structures, every level it reaches has to have been copied.

**Is the structure large or does it hold something uncopyable?** `deepcopy` on
a big object graph costs real time, and on an object holding a connection, a
file or a lock it either fails or duplicates something that should be unique.
Both are signals to restructure rather than to copy harder &mdash; usually by
making the shared parts immutable, or by rebuilding the small part you need to
change rather than duplicating the whole.

Most real answers land on shallow, and the ones that do not are usually nested
configuration or a snapshot taken for comparison. Knowing which of those you
are in is more useful than a rule about which function to call.

## Questions people ask

<strong>Is `list(x)` a deep copy?</strong> No. It is one of the shallow ones,
along with `x[:]` and `x.copy()`.

<strong>Does `deepcopy` handle cycles?</strong> Yes. It remembers what it has
already copied, so a structure that refers to itself does not cause infinite
recursion.

<strong>Is `deepcopy` slow?</strong> Relative to a shallow copy, considerably.
It walks the whole structure and keeps a record as it goes. For small
structures it does not matter.

<strong>How do I copy only two levels?</strong> There is no built-in for that.
A comprehension that shallow-copies each item &mdash;
`{k: v.copy() for k, v in d.items()}` &mdash; is the usual answer.

<strong>Can I stop an attribute being deep-copied?</strong> Yes, by defining
`__deepcopy__` on the class, which is how objects holding a connection or a
lock avoid duplicating it.

<strong>Does copying a string do anything?</strong> No. Strings are immutable,
so `copy` returns the same object.

<strong>What about `copy.copy` versus `.copy()`?</strong> The same thing for
builtins. `copy.copy` also works on objects that have no `.copy()` method.

<strong>Does `deepcopy` copy class definitions too?</strong> No. Classes,
functions and modules are treated as atomic and shared rather than duplicated,
which is what you want.

<strong>Is pickling and unpickling a valid deep copy?</strong> It usually
produces one, and it is slower and fails on anything unpicklable. Use
`deepcopy`, which is what it is for.

<strong>Why does copying a nested list "sometimes" work?</strong> Because it
works whenever nothing reaches past the top level afterwards. The copy was
always shallow; the code simply had not yet touched the shared part.

<strong>Should a function copy the arguments it is given?</strong> Only if it
stores them or mutates them. A function that reads a list and returns a result
has no reason to copy anything, and copying defensively everywhere costs more
than the bugs it prevents.

<strong>What is the fastest way to copy a flat list?</strong> `x.copy()` and
`x[:]` are equivalent and both are fast. `list(x)` is the one that also accepts
any iterable, which is occasionally why it is chosen.

## Recap in one screen

- A shallow copy duplicates the outer container and shares everything inside
  it; `original[0] is shallow[0]` is the test.
- Shallow is a complete copy when the contents are immutable, which is why the
  problem stays hidden for so long.
- `copy.deepcopy` rebuilds the whole structure, preserves shared references and
  survives cycles &mdash; and costs proportionally.
- The bugs arrive through config dicts, shared defaults, lists of records and
  snapshots, not through code that obviously copies.
- Making the data immutable removes the question entirely.
""")


extend("enumerate_function", """
## The off-by-one that start= invites

`start=1` changes the number you are handed and nothing else. The item is still
the same item, and the position it occupies in the list is still one lower:

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

The third column is the item, reached correctly with `n - 1`. The fourth shows
what indexing with `n` gives you: the *next* item, and eventually the end of
the list.

This is why `start=` is for display and not for access. The moment you use the
number both to print and to index, you have two meanings for one variable and
one of them is wrong. If you genuinely need both, take the real index and add
one where you print it:

```python
for i, name in enumerate(names):
    print(i + 1, name, names[i])
```

Wordier by one character, and it cannot be got wrong.

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
and 5, because `enumerate` counts positions in the input and not lines
produced. Neither is wrong; they answer different questions.

The rule that falls out: `enumerate` numbers the *source*. If you want to
number the *output*, and the loop can skip items, you are back to a counter
&mdash; and that is one of the few remaining places a manual counter is the
right answer.

A middle ground worth knowing: filter first, then enumerate the result.
`for n, line in enumerate((l for l in lines if l), start=1)` numbers what
survives, and keeps the counter out of the body.

## Both numbers at once

Occasionally you want the position *and* the item *and* something from a second
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
`(index, item)` where the item is the tuple `zip` produced, so the pattern on
the left has to have the same shape: a number, then a pair. Leaving the
brackets out is a `ValueError` about unpacking, and it is one of the clearer
error messages you will meet.

The order matters too. `zip(enumerate(names), scores)` also works and gives you
`((0, "ana"), 91)`, which unpacks as `for (i, name), score in ...`. Both are
legal; the first reads better because the index stays at the front where a
reader expects it.

## Why wanting the index is usually a question worth checking

`enumerate` makes the index easy to get, which makes it worth asking, each
time, whether you actually need it. A surprising share of loops that ask for a
position are working around something else.

**Comparing an item with its neighbour.** The index is being used to reach
`items[i - 1]` or `items[i + 1]`. What you want is consecutive pairs, and
`zip(items, items[1:])` or `itertools.pairwise` gives them without any index or
any bounds check at the ends.

**Walking two sequences together.** The index is being used to index both.
`zip` pairs them directly, and removes the possibility of the two lookups
disagreeing.

**Building a lookup of where things are.** The loop collects positions into a
dictionary. A dict comprehension over `enumerate` says it in one line, and
often the real question is "does this contain x" or "which comes first", both
of which have direct answers.

**Modifying the list while walking it.** The index is being used to assign back
with `items[i] = ...`. This works and is the one case where the index is
genuinely required &mdash; but building a new list with a comprehension is
usually clearer, and removing items by index while iterating is a bug in
waiting.

What is left after those is the honest use: displaying a number to a person,
reporting which record failed, or writing into a pre-sized structure. Those are
real, and `enumerate` is exactly right for them.

## Where you will actually meet it

Three situations account for most real uses, and they share a shape: the number
is going somewhere a human will read it.

**Reporting which line failed.** Parsing a file and validating rows, the index
is what turns "invalid date" into "line 47: invalid date". Without it the error
message is useless on a file of any size, and `start=1` matters because people
count lines from one and so does every text editor.

**Progress through a long job.** `if n % 1000 == 0: print(n)` inside a loop
over a large iterable gives you a heartbeat, and because `enumerate` is lazy it
costs nothing on a stream you are already reading.

**Numbered output.** Menus, ranked results, numbered steps, table rows. Here
the number is presentation, which is precisely the case `start=1` exists for
and precisely the case where using it to index would be wrong.

The common thread is that the index is an output rather than a mechanism. When
the number is being printed, `enumerate` is the tool. When the number is being
used to reach back into the data, there is usually a way to get the data
directly instead.

## Numbering things that are not lists

`enumerate` takes any iterable, and the interesting cases are the ones that are
not sequences, because the position it hands you means something slightly
different in each.

Over a **file**, the number is the line number, and it is the reason
`enumerate(f, start=1)` appears in every script that reports problems in a data
file. Nothing else gives you that number without reading the file twice.

Over a **generator**, the number counts what has been produced so far. It is
the only way to know how far a stream has got, since a generator has no length
and no position you can ask for.

Over a **dictionary**, the number is the position in insertion order, which is
well defined since Python 3.7 and is occasionally what you want &mdash;
numbering the entries of a config for display, say.

Over a **set**, the number is the position in an arbitrary order. It is stable
within a single run and must not be relied on across runs or between machines,
because it depends on hash values. If a number over a set matters, sort it
first and enumerate the sorted result.

Over a **string**, the number is the character position, which makes
`enumerate(text)` a reasonable way to find where something occurs &mdash;
though `str.find` is usually the direct answer.

The pattern across all of them is that `enumerate` counts iterations, not
positions in storage. For a list those are the same thing, and for everything
else the distinction is the whole point.

## The name, and where it came from

"Enumerate" means to list things one by one, and in older languages an
enumerator was the object that walked a collection. Python's `enumerate` keeps
the sense of walking while adding the numbering, which is why the name is about
the traversal rather than about counting.

It arrived in Python 2.3, and the release note for it is unusually direct about
the motivation: the `range(len(...))` idiom was common, awkward, and a frequent
source of small errors. The feature exists specifically to remove a pattern
people kept writing, which is worth knowing because it tells you what the
intended use is. If your loop looks like the pattern it replaced, use it. If it
does not, the index it offers is probably not the thing you need.

## Questions people ask

<strong>Does `enumerate` build a list?</strong> No. It yields pairs on demand,
so it works on files, generators and anything else iterable.

<strong>Can I use it on a dictionary?</strong> Yes, and you get positions
alongside keys. `enumerate(d.items())` when you want the pairs too.

<strong>What if I only want the index?</strong> Then you probably want
`range(len(items))` &mdash; but check first, because wanting only the index is
usually a sign the loop is doing something else.

<strong>How do I name the unused half?</strong> `_` by convention, for either
position: `for _, item in enumerate(items)` is legal though pointless.

<strong>Does `start=` accept a negative number?</strong> Yes. It is just the
number to begin counting from, and nothing validates it.

<strong>Is `enumerate` slower than a manual counter?</strong> No, it is faster
&mdash; the counting happens in C rather than in a bytecode `+= 1`.

<strong>Can I enumerate backwards?</strong> Not directly.
`enumerate(reversed(items))` numbers from zero at the end; to get the original
indices descending, zip a reversed range instead.

<strong>Can I unpack a nested item directly?</strong> Yes, with brackets:
`for i, (a, b) in enumerate(pairs)`. The pattern on the left has to match the
shape of what is yielded.

<strong>Why is my counter wrong when I use `continue`?</strong> If it is a
manual counter placed after the `continue`, it never runs for skipped items.
`enumerate` has no such problem, because the counting is not in your loop body.

<strong>Can I start the count from something other than a number?</strong> No.
`start` is added to an integer counter, so it has to be an integer.

<strong>Is there a version that gives the index from the end?</strong> Not
built in. `zip(range(len(a) - 1, -1, -1), a)` does it, and is a good example of
the arithmetic `enumerate` normally saves you.

## Recap in one screen

- `enumerate` yields `(position, item)`; the `for i, x` on the left is ordinary
  tuple unpacking.
- It removes both the manual counter and the `range(len(...))` indexing, along
  with the mistakes each invites.
- `start=` changes the label, not the position &mdash; never use that number to
  index back into the sequence.
- It is lazy and works on anything iterable, including files too large to hold.
- If the loop skips items and you want to number the output, use a counter;
  `enumerate` counts the input.
""")


extend("nested_data_structures", """
## A worked example: from rows to a report

Most work with nested data is the same journey &mdash; records in, grouped
summary out. Here it is end to end:

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

Three moves, each from elsewhere in the track. The generator expression sums a
list-valued field without building an intermediate list. `totals.get(key, 0)`
accumulates without a first-time special case. And `sorted` with a negated key
puts the largest first.

What makes it readable is that each level is handled at one depth. The inner
sum works on one order's items and knows nothing about customers; the outer
loop works on orders and knows nothing about prices. When nested-data code
becomes hard to follow, it is almost always because one expression is reaching
through three levels at once.

## Naming the path

The single most useful habit with nested data is refusing to repeat a long path.
`record["user"]["profile"]["display_name"]` written in four places is four
places to update when the API changes, and four chances to typo a key into a
`KeyError` that names only the last one.

A one-line function fixes it:

```python
def display_name(record):
    return record["user"]["profile"]["display_name"]
```

The path now exists once. It has a name that says what it means, so the call
sites read as intent rather than as navigation. It has somewhere to put a
default or a `try`. And when the shape changes &mdash; and it will &mdash;
there is one line to edit.

This is worth doing at two levels of nesting, not four. The instinct to wait
until it gets bad is why it usually does.

## Where the shape comes from, and what it costs

Nested data almost always arrives rather than being designed: it is the shape
some API returns, or the shape JSON has, or the shape a database join produced.
That has a consequence worth being deliberate about.

Data in the shape it arrived in is convenient for reading once and awkward for
everything else. Nothing validates it, so a missing key is discovered at the
point of use rather than at the point of parsing. Nothing names it, so every
function that touches it has to know the layout. And nothing stops two parts of
the program disagreeing about whether a field is optional.

The alternative is to convert at the boundary: read the nested structure once,
pull out what you need, and build objects &mdash; dataclasses, named tuples, or
just flatter dictionaries with the names you chose. Everything downstream then
works with a shape you defined, validated once, at a known place.

For a script that reads a file and prints a summary, this is overkill and the
raw structure is fine. For anything long-lived, converting at the edge is the
difference between a program where a shape change breaks one function and one
where it breaks eleven.

## Depth, and when to stop nesting

Reading nested data is unavoidable. *Building* deeply nested data is a choice,
and usually a poor one past two levels.

A dictionary of dictionaries of lists is hard to inspect, hard to iterate
without three loops, and impossible to query except by walking. The alternative
is usually a flat list of records where the nesting becomes fields: instead of
`by_region[region][city] = [names]`, a list of
`{"region": ..., "city": ..., "name": ...}` rows.

Flat records are longer to write and enormously easier to work with. They sort
by any field, filter with one comprehension, group by whichever key the current
question needs rather than the one you committed to when you built the
structure, and convert directly to CSV or a dataframe. The nesting you actually
need can be produced on demand with a grouping, which is three lines.

The heuristic: nest when the structure reflects genuine containment that will
never be queried the other way round. Flatten when you can imagine wanting a
different grouping later &mdash; which, for anything resembling a report, you
will.

## Failing at the boundary rather than in the middle

The characteristic problem with nested data is that a shape mistake surfaces
far from where it entered. A key that is missing from an API response is
discovered three functions later, as a `KeyError` naming a key that looks
correct, in code that has nothing to do with fetching.

The remedy is to check the shape once, where the data arrives, rather than
defending against it everywhere afterwards. What that check looks like depends
on how much the data matters.

At the simplest, a few lines that pull out the fields you need and raise a
clear error if they are absent. The error then says "response is missing
`user.profile.name`" at the point of parsing, which is a diagnosis rather than
a symptom.

A step up, build the values into a dataclass or a `NamedTuple`. Construction
fails immediately if a field is missing, the resulting object has known
attributes rather than arbitrary keys, and every function downstream can be
written against a shape that is guaranteed rather than hoped for.

Further still, a validation library &mdash; Pydantic being the common choice
&mdash; declares the expected shape as types and reports every problem at once,
with the path to each. That is worth it when the data comes from outside your
control and the cost of processing something malformed is high.

All three are the same idea at different sizes: convert once, at the edge, and
let everything inside the boundary assume the data is what it claims to be. The
alternative &mdash; a `.get` chain at every use site &mdash; spreads the
uncertainty through the whole program and never actually resolves it.

## Questions people ask

<strong>How do I get a value several levels down safely?</strong> Chain `.get`
with `{}` defaults, or wrap the direct path in `try`/`except KeyError` when
absence is genuinely exceptional.

<strong>Why does `.get("a", {}).get("b")` work but `.get("a").get("b")`
not?</strong> Because the second returns `None` when the key is missing, and
`None` has no `.get`. The `{}` keeps a dictionary in the chain.

<strong>How do I see the shape of something I just parsed?</strong>
`print(json.dumps(data, indent=2))` for JSON-compatible data, and
`pprint.pprint` for anything else.

<strong>Can I flatten an arbitrarily deep structure?</strong> Yes, with
recursion or a stack &mdash; but if the depth is unknown, that is usually a
sign the data wants to be flat records instead.

<strong>Are nested comprehensions read inside-out?</strong> No. The `for`
clauses read left to right in the same order as the equivalent nested loops.

<strong>Why did my copy of a nested structure change?</strong> Because the copy
was shallow and the inner structures are shared.

<strong>Do JSON keys stay integers?</strong> No. They come back as strings,
which is a common surprise after a save-and-load round trip.

<strong>Should I use dotted access instead of brackets?</strong> Libraries that
turn dictionaries into attribute access look convenient and hide typos, since a
missing attribute and a missing key report differently. A dataclass gives you
the same ergonomics with the checking.

<strong>What is the fastest way to search nested data?</strong> Build an index
once &mdash; a dictionary keyed by whatever you search on &mdash; rather than
walking the structure on every lookup.

<strong>Is there a standard way to walk a structure of unknown depth?</strong>
Recursion, with a check on each value for whether it is a dictionary, a list,
or a leaf. The standard library has no general walker, because what to do at
each node depends entirely on the task.

## Recap in one screen

- Most real data is a list of records; the moves are index, key lookup, and an
  inner loop, composed to whatever depth is needed.
- Chain `.get(key, {})` for optional paths, and `try`/`except KeyError` when a
  missing value is exceptional rather than expected.
- Give a repeated path a named function at two levels of nesting, not four.
- Convert at the boundary into shapes you defined, unless the script is small
  enough that the raw structure will do.
- Prefer flat records over deep nesting for anything you might want to group a
  different way later.
""")


extend("slicing_step_negatives", """
## A worked example: the three arguments together

Every rule on this page in one block, with the results printed rather than
described:

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
from the right. `s[::2]` takes every second character from the whole string.
`s[::-1]` reverses. `s[5:2:-1]` walks backwards from 5 down to but not
including 2, which is where the exclusive stop starts feeling strange &mdash;
the item at index 2 is missing from the result even though 2 is written on the
left of the colon.

The last line is the forgiveness: an end past the length is clamped, and a
start past the length gives an empty string rather than an error.

## Why a negative step reverses the roles

`s[2:5:-1]` returns nothing, and the reason is worth spelling out because it is
the one part of slicing people memorise rather than understand.

A slice always moves from the start value towards the stop value, in the
direction the step specifies. With a positive step it moves right, so the start
must be to the left of the stop. With a negative step it moves left, so the
start must be to the *right* of the stop. `s[2:5:-1]` asks to begin at 2 and
walk leftwards until it reaches 5, which it never will, so the result is empty
immediately.

That also explains the defaults. When the step is negative and you leave the
ends off, the omitted start becomes the end of the sequence and the omitted
stop becomes "past the beginning" &mdash; which is why `s[::-1]` gives you
everything reversed, including the first character. Writing `s[::-1]` and
`s[len(s):0:-1]` are not the same: the second stops before index 0 and drops
the first character.

The practical consequence is that there is no way to write "reversed, ending at
the very beginning" with an explicit stop, because the stop would have to be
-1, and -1 already means the last item. Omitting it is the only way to say it,
which is exactly why the idiom is `[::-1]` and not something more explicit.

## Slice objects, and the syntax behind the colons

The bracket syntax is shorthand. `a[1:5:2]` is `a[slice(1, 5, 2)]`, and
`slice` is an ordinary object you can build, store and pass around.

That is occasionally useful in its own right &mdash; naming a slice you use
repeatedly, `HEADER = slice(0, 4)`, makes the call sites say what they mean.
More often it is useful as an explanation. It is why `a[1:5]` and
`a[slice(1, 5)]` behave identically, why a class can support slicing by
handling a `slice` in its `__getitem__`, and why the ellipsis and comma forms
that NumPy uses are possible at all: `a[1:5, ::2]` passes a tuple of slices,
which plain Python lists reject and NumPy arrays understand.

`indices()` on a slice object resolves it against a length, returning the
concrete start, stop and step after clamping and negative-index conversion.
`slice(1, 99).indices(5)` gives `(1, 5, 1)`, which is the arithmetic the
forgiving behaviour is built on, made visible.

## Slicing is a protocol, not a list feature

Everything on this page works on any sequence, and knowing that is what makes
the syntax worth learning properly rather than memorising for lists.

Strings, tuples, bytes, bytearrays and `range` all slice with the same three
numbers and the same rules, and each returns its own type &mdash; slicing a
tuple gives a tuple, slicing a `range` gives a `range`, computed rather than
materialised. `bytes` slicing is how binary formats are parsed, taking a
header, a length field and a payload by offset.

Beyond the builtins, any class can support it by handling a `slice` object in
`__getitem__`, and the libraries that do have extended the idea considerably.
NumPy accepts a tuple of slices, `a[1:5, ::2]`, to take a rectangle out of a
two-dimensional array, and its slices are *views* rather than copies &mdash;
writing into one changes the original, which is the opposite of the list
behaviour and a genuine trap when moving between them. pandas uses the same
brackets with labels rather than positions in `.loc`, where the stop is
inclusive, breaking the one rule you had learned to rely on.

The lesson is not to distrust slicing but to check two things when a new type
supports it: whether the result is a copy or a view, and whether the stop is
excluded. Those two answers differ across the ecosystem and everything else
stays the same.

## Idioms worth recognising on sight

A handful of slices appear often enough to read as single symbols rather than
as arithmetic. Knowing them saves parsing the numbers every time.

`a[::-1]` reverses. `a[:]` copies a list, and is also the left-hand side of
`a[:] = b`, which replaces the contents of `a` in place rather than rebinding
the name &mdash; the difference that matters when someone else holds a
reference to `a`.

`a[:n]` and `a[n:]` are "the first n" and "everything after the first n", and
together they cover the whole sequence exactly once. `a[-n:]` is the last n,
and `a[:-n]` is everything except the last n, which is how you drop a known
suffix without computing a length.

`a[::n]` takes every nth item, and `a[i::n]` takes every nth starting from `i`
&mdash; the pair of them is how you deinterleave two sequences that were
interleaved into one, with `a[::2]` and `a[1::2]`.

`s[:0]` is an empty sequence of the same type, occasionally useful as a
starting value when you need "an empty one of whatever this is" without naming
the type.

## Choosing between an index and a slice

The two look similar and they fail differently, which is the basis for choosing
between them.

`a[i]` asserts that position `i` exists. If it does not, you get an
`IndexError` naming the problem at the line that caused it. `a[i:i+1]` makes no
such assertion: out of range, it hands back an empty sequence and the program
carries on with nothing.

So the choice is about whether absence is a bug. Taking the first item of a list
that is documented to be non-empty should be `a[0]`, because an empty list
means something upstream is wrong and you want to hear about it. Taking "up to
ten results" from a list that might have three should be `a[:10]`, because
having fewer is expected and the clamping is exactly right.

The mistake in one direction is a crash on data that was always going to be
short. The mistake in the other is a silent empty result that gets reported as
zero, saved as an empty file, or treated as "no matches found" &mdash; and
those are much harder to trace, because there is no error to start from.

One practical consequence: when a slice with computed bounds returns nothing,
do not assume the data was empty. Print the bounds. An off-by-one that produces
`a[5:5]` looks identical in the output to a list that genuinely had nothing to
give.

## Questions people ask

<strong>Is `a[:]` the same as `a.copy()`?</strong> For a list, yes &mdash; both
are shallow copies. For a string it returns the same object, since there is
nothing to copy.

<strong>Why does `a[::-1]` work on strings and `a.reverse()` not?</strong>
`reverse` is a list method that mutates, and strings cannot be mutated.

<strong>What is the difference between `a[::-1]` and `reversed(a)`?</strong>
The slice builds a new sequence; `reversed` returns a lazy iterator and copies
nothing.

<strong>Can I slice a generator?</strong> No. Use `itertools.islice`, which
takes the same start, stop and step but cannot go backwards.

<strong>Does slicing a tuple give a tuple?</strong> Yes. A slice returns the
same type as the thing sliced, for the built-in sequences.

<strong>How do I take every nth item starting from the end?</strong>
`a[::-n]` &mdash; the negative step both reverses and strides.

<strong>Why is `a[1:3] = [1, 2, 3]` allowed?</strong> Because slice assignment
replaces a section and may change the length. It is the mutating counterpart of
the copying slice.

<strong>Does slicing a list of objects copy the objects?</strong> No. The new
list holds the same objects, which is the shallow-copy behaviour from elsewhere
in the track.

<strong>Can the step be zero?</strong> No. `a[::0]` raises `ValueError`,
because a step of zero would never advance and the slice would never end.

<strong>Is `a[0:len(a)]` the same as `a[:]`?</strong> Yes, and the shorter form
is preferred &mdash; it does not have to compute a length that the slice
already handles.

## Recap in one screen

- Three numbers: start, stop, step; the stop is always excluded, exactly as in
  `range`.
- Negative indices count from the right, and can be mixed freely with positive
  ones.
- A negative step swaps the roles of start and stop, which is why `s[2:5:-1]`
  is empty and `s[::-1]` reverses.
- Slicing clamps rather than raising, which is convenient and occasionally
  hides a wrong index.
- A slice copies; assigning into a slice mutates, and can change the length.
""")


extend("nested_conditionals", """
## The same logic, four ways

One rule set written four ways, so the difference is shape rather than
behaviour:

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

Both are correct, and which reads better is genuinely arguable here. The nested
version makes the two-by-two structure visible: two ages, two membership
states, four outcomes. The flat version reads as a list of rules in priority
order, which is how a price list is usually written down.

The point of running both is that flattening is not automatically an
improvement. It is an improvement when the nesting was accidental &mdash; when
the inner `if` was the whole body of the outer one, or when the branches were
refusals. When the nesting reflects a genuine grid of cases, keeping it can be
the honest thing to do.

## Conditions that depend on each other

There is one case where flattening with `and` is not merely a style choice but
actually required, and it comes from short-circuiting.

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
evaluated. Reverse the two halves and the same line raises `AttributeError`
&mdash; the check that was supposed to protect the access happens after it.

This is why nesting `if user is not None:` around `if user.active:` and
flattening it to a single `and` are equivalent: both express "only ask the
second question if the first was true". What is *not* equivalent is writing
them in the other order, or joining them with `&`, which evaluates both sides
unconditionally.

The general shape is worth recognising. Any time one condition establishes that
the next one is safe to ask &mdash; not `None`, non-empty, key present, index
in range &mdash; the order is load-bearing and cannot be rearranged for
readability.

## Where the nesting actually came from

Deep conditionals are rarely written that way. They accumulate, and the history
is usually visible in the code.

A function starts with one check. A bug report arrives and someone adds a
second condition inside the first, because that is the smallest possible
change and it does not disturb what is already there. Six months and four
reports later there are five levels, each added by someone being careful.

That is worth knowing because it tells you what the fix is. The problem is not
that a particular developer wrote bad code; it is that adding a nested `if` is
always the locally cheapest change, and nothing pushes back. The remedy is to
treat depth as a review signal &mdash; when a change would add a fourth level,
that is the moment to restructure, not later.

The restructuring is nearly always one of three moves. Invert the refusals into
guard clauses. Combine conditions that were only ever both-required. Or extract
the inner block into a function with a name, which resets the indentation and
gives the logic a label at the same time.

## Writing the condition so it reads

Flattening helps only if the resulting condition is readable, and a flattened
condition can easily be worse than the nesting it replaced. Three habits keep
it honest.

**Avoid stacked negatives.** `if not (not active or banned)` is correct and
nobody can evaluate it at a glance. De Morgan's rules let you push the negation
inwards &mdash; `not (A or B)` is `not A and not B`, and `not (A and B)` is
`not A or not B` &mdash; and the version with fewer negations is almost always
the one to keep. Better still, name the positive: `if is_eligible:`.

**Name the compound.** When a condition needs three clauses, assigning it to a
well-named variable on the line before turns the `if` into a sentence.
`can_borrow = user.active and not user.fines and book.available` followed by
`if can_borrow:` reads as intent, and the name explains what the combination
*means* rather than only what it checks.

**Keep comparisons in a natural order.** `if 0 <= n < 100` reads as a range and
chains correctly in Python, where most languages would need two comparisons and
an `and`. Writing `if n >= 0 and n < 100` says the same thing with more to
parse.

The underlying test is whether a reader can say what the condition means
without evaluating it. A staircase of simple conditions is sometimes easier to
read than one flat condition that requires bookkeeping, and when that is true,
the staircase is the right answer.

## Every branch is a case to test

Nesting has a cost that is invisible while writing and obvious while testing:
the number of paths multiplies.

Two nested conditions give four combinations. Three give eight. A function with
four levels has sixteen paths through it, and the tests either cover all of
them or leave some untried &mdash; and the ones left untried are, by
construction, the unusual combinations where the bugs are.

Guard clauses do not remove the combinations, but they change what a test has
to do. Each guard is a single condition with a single outcome, testable on its
own by passing one bad value and checking one message. The final line is the
case where everything passed. The tests read as a list matching the guards, and
a new rule adds one test rather than doubling the table.

This is the practical argument for flattening, and it is stronger than the
aesthetic one. A shape that makes each rule independently testable is a shape
where a change to one rule cannot silently affect another &mdash; which is
exactly the property a staircase does not have, because every inner branch sits
inside the assumptions of every outer one.

## Extracting the inner block

The third remedy, after combining and inverting, is to give the inner block a
name. It is the one people reach for last and it is often the best.

When a conditional is deep because the innermost part is doing real work, the
depth is telling you that two jobs are in one function: deciding, and doing.
Moving the inner block into its own function leaves an outer function that
reads as a sequence of decisions ending in a call, and an inner one that starts
at the left margin with its own name explaining what it is for.

The mechanical benefit is the indentation reset. The real benefit is the name.
A block that was three levels deep and unlabelled becomes something with a
title, which forces you to say what it does &mdash; and occasionally reveals
that you cannot, because it was doing two things.

This is also the move that makes the guard-clause style available where it was
not. Guards need `return`, and a block buried in a loop inside a function has
nowhere to return to; extract it, and the guards become possible inside the new
function.

## Questions people ask

<strong>Is there a limit to how deep nesting can go?</strong> Python allows
about twenty levels before the parser complains, which is far past the point
where anyone can read it.

<strong>Does flattening change performance?</strong> Not meaningfully. Both
forms evaluate the same conditions in the same order.

<strong>Should I use `elif` or a nested `if`?</strong> `elif` when the
conditions are alternatives to each other, nesting when the second question
only makes sense given the first.

<strong>What about `match`?</strong> When the branching is on the shape or
value of one object, `match` often expresses it more directly than either
nesting or an `elif` chain.

<strong>Can guard clauses be used outside a function?</strong> `continue` plays
the same role inside a loop, and it is under-used for exactly this.

<strong>Is an early `return` bad practice?</strong> The single-exit rule comes
from languages with manual cleanup. In Python, early returns make guard clauses
possible and are standard style.

<strong>How do I handle "at least one of these must be true"?</strong> `or`, or
`any()` over a list of conditions when there are more than two or three.

<strong>Does an early return make a function harder to debug?</strong> No. A
breakpoint on each guard is as easy as one at the top, and the stack is
shallower when it fires.

<strong>What about conditions that are expensive to evaluate?</strong> Order
them cheapest first. Short-circuiting means an expensive check is skipped
whenever a cheaper one has already decided the answer.

<strong>Is a dictionary lookup ever a replacement for the whole thing?</strong>
Yes, when every branch is comparing one value against a constant. That is the
dispatch table from the dictionary methods page.

## Recap in one screen

- If the inner `if` is the entire body of the outer one, the two conditions are
  an `and`.
- Refusals belong at the top as guard clauses, so the main path stays at the
  left margin and each rule sits beside its own message.
- Genuine nesting is when the second question only makes sense given the first
  &mdash; and short-circuiting makes the order load-bearing.
- `elif` is one decision with several outcomes; reaching for nesting there
  turns a flat choice into a staircase.
- Three levels is a review signal: combine, invert, or extract a function.
""")


extend("args_and_kwargs", """
## Keyword-only and positional-only, and why they exist

The stars do a second job besides collecting: they mark boundaries in a
signature. Two markers control how callers are allowed to pass arguments.

A bare `*` makes everything after it keyword-only:

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
if the parameter order is ever edited. Forcing the names makes the call
self-documenting and makes reordering the parameters a safe change.

A `/` does the opposite, marking everything before it positional-only:

```python
def distance(x, y, /):
    return abs(x - y)
```

Now `distance(3, 5)` works and `distance(x=3, y=5)` does not. This is rarer,
and the reason is the mirror image: it keeps the parameter *names* out of the
API, so they can be renamed later without breaking callers. Most builtins are
positional-only for exactly that reason, which is why `len(obj=x)` fails.

The rule of thumb: make a parameter keyword-only when its meaning is not
obvious from the call site, which in practice means flags, options and
anything numeric that is not the main subject.

## What the stars cost you

`*args, **kwargs` accepts everything, and the price is paid by every reader and
every tool afterwards.

The signature stops documenting anything. `def process(*args, **kwargs)` tells
the next person nothing about what to pass, and the only way to find out is to
read the body &mdash; and then the body of whatever it forwards to.

Editors and type checkers lose their grip. Autocompletion has nothing to
suggest, and a type checker cannot verify a call it cannot see the shape of.
For a codebase using type hints, a star signature is a hole in the coverage
that propagates to every caller.

Errors move. A misspelled keyword argument would normally raise
`TypeError: unexpected keyword argument 'timeuot'` at the call, naming the
mistake. Absorbed into `**kwargs` it becomes a missing key later, or &mdash;
worse &mdash; a default silently used instead of the value you passed, which
produces wrong output and no error at all.

None of that is an argument against the feature; it is an argument about where
to use it. Wrappers and subclass forwarding need it and pay none of the cost,
because there is no meaningful signature to state. A function people call
directly should name its parameters.

## Unpacking in the other direction

The two stars appear in three places and mean the same thing in all of them,
which is easier to hold on to than three separate rules.

In a **definition** they collect: `def f(*args)` gathers loose positional
arguments into a tuple.

At a **call site** they spread: `f(*items)` hands each item over as a separate
argument.

In a **literal** they merge: `[*a, *b]` builds one list from two, and
`{**a, **b}` builds one dictionary from two, with later keys winning.

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

Both build a new object and leave the originals alone, which is the difference
from `update` and `extend`. And in assignment the star runs backwards again:
`first, *rest = items` collects rather than spreads, because the star is on the
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
replacement. `wrapper` accepts anything with `*args, **kwargs`, so it can stand
in front of any function at all. The forwarding call `func(*args, **kwargs)`
spreads them back out, so `add` receives exactly what the caller wrote. And
`@announce` above `def add` is shorthand for `add = announce(add)`.

`functools.wraps` is the part people leave out and then miss. Without it,
`add.__name__` prints `wrapper`, the docstring is gone, and every traceback
through the decorated function names the wrapper instead of the function. It
copies the identifying attributes across, and it is one line.

Note how the arguments arrive: `2` in `args` and `b=3` in `kwargs`, exactly as
the caller passed them. The wrapper does not know or need to know that `add`
has a parameter called `b`.

## Asking a function what it accepts

When you do need to know the signature &mdash; validating a plugin, building a
command-line interface, writing a framework &mdash; `inspect` answers it rather
than parsing the source:

`inspect.signature(func)` returns an object listing the parameters, their
defaults, their kinds (positional, keyword-only, `*args`, `**kwargs`) and any
annotations. `sig.bind(*args, **kwargs)` matches a proposed call against it and
raises the same `TypeError` the real call would, which is how you check
arguments before doing expensive work.

This is also how a decorator can be smarter than pure forwarding. A caching
decorator that wants a stable key needs to know that `f(1)` and `f(a=1)` are
the same call; `sig.bind` plus `apply_defaults` normalises both to the same
thing, which no amount of inspecting `args` and `kwargs` directly will do.

## The star in assignment

The same star appears in assignment, and it is worth connecting to the rest
rather than learning separately.

`first, *rest = items` binds the first item and collects everything else into a
list. `*most, last = items` does the mirror image. `a, *middle, b = items` takes
both ends and collects what is between them. In each case the starred name gets
a list &mdash; always a list, even when the right-hand side was a tuple or a
string.

This is the collecting sense of the star, the same as in a definition: the
star marks the name that absorbs however many items are left over. The
spreading sense is what you get on the other side of the equals sign, in a call
or a literal.

Only one star is allowed per assignment, for the obvious reason that two would
make the split ambiguous. And the non-starred names are still required: unpacking
`a, *rest = []` raises, because there is nothing for `a`, while `*rest, = []`
succeeds and gives an empty list.

## Questions people ask

<strong>Do the names `args` and `kwargs` matter?</strong> No, the stars carry
the meaning. The names are a strong convention in general-purpose wrappers and
worth replacing with something descriptive elsewhere.

<strong>Can I have `*args` without `**kwargs`?</strong> Yes, and the reverse.
They are independent.

<strong>What order do they go in?</strong> Named parameters, then `*args`, then
keyword-only parameters, then `**kwargs`.

<strong>Is `**kwargs` ordered?</strong> Yes, it is a normal dictionary and
keeps the order the caller used.

<strong>Can I pass a list where `*args` is expected?</strong> Only with a star:
`f(*items)`. Without it you pass the list as a single argument.

<strong>Why does `f(**d)` fail with "keywords must be strings"?</strong>
Because a dictionary with non-string keys cannot be turned into keyword
arguments.

<strong>How do I forward everything including the function's own new
option?</strong> Take it as keyword-only, and forward `*args, **kwargs`
unchanged: the new option is bound by name and never reaches the wrapped call.

## Recap in one screen

- One star collects positional arguments into a tuple; two collect keyword
  arguments into a dictionary.
- The same stars at a call site spread a collection back into arguments, and in
  a literal they merge collections.
- A bare `*` in a signature makes what follows keyword-only; a `/` makes what
  precedes it positional-only.
- The pass-through `f(*args, **kwargs)` is what makes decorators and wrappers
  possible without knowing any signature.
- A star signature costs documentation, tooling and clear errors &mdash; use it
  where there is no meaningful signature to state, not to avoid writing one.
""")


extend("type_conversion", """
## What each constructor actually accepts

The type names double as conversions, and each has its own idea of what it will
take. Seeing them side by side removes most of the surprises:

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

`int` tolerates surrounding whitespace and the underscores Python allows in
numeric literals, and takes a base as a second argument &mdash; which is how
you read hexadecimal, binary and octal from text without writing a parser.

`list` on a dictionary gives its **keys**, not its items, which catches people
who expected pairs. `list` on a string gives characters, which is occasionally
what you want and more often a sign that `split` was meant.

`str` never fails. Every object has a string form, so `str(x)` always returns
something &mdash; which is convenient and means a bug can travel a long way
disguised as text. `str(None)` is the string `"None"`, and a `"None"` written
into a CSV column is a classic way to lose the distinction between missing and
present.

## Parsing a boolean from text

There is no conversion for this, and reaching for `bool` is the mistake
everyone makes once:

```python
print(bool("False"), bool("0"), bool(""))
```

```
True True False
```

`bool` on a string asks only whether the string is empty. `"False"` and `"0"`
are both non-empty, so both are `True`, which is precisely backwards from what
the text says.

Reading a boolean out of a config file, an environment variable or a form means
deciding what counts, and then saying so:

```python
TRUE = {"1", "true", "yes", "on"}

def as_bool(text):
    return str(text).strip().lower() in TRUE
```

That is a policy rather than a conversion, which is why the language does not
provide one &mdash; different formats disagree about whether `"y"`, `"on"` or
`"enabled"` should count, and about what an unrecognised value means. Deciding
explicitly is the point.

## Where conversion loses information

Some conversions are exact and some throw information away, and knowing which
is which prevents a family of quiet bugs.

`int(3.9)` discards the fractional part. `int` from a large float loses
precision before it even starts, because the float never held the exact value.
`float(some_big_int)` is worse: integers in Python are unbounded, floats are
not, so a sufficiently large integer converts to a float that is merely nearby,
and converting back does not return the original.

`str` of a float is lossy in the other direction historically, though modern
Python prints the shortest string that round-trips exactly, so
`float(str(x)) == x` holds.

`set(items)` discards duplicates and order. `dict(pairs)` discards all but the
last value for each repeated key. Neither reports what it dropped, and both are
sometimes used deliberately for exactly that effect &mdash; which is why the
loss has to be intentional rather than discovered.

The habit worth forming: when a conversion narrows &mdash; float to int, list
to set, anything to `str` &mdash; ask what happens to what does not fit. When
it widens, as int to float or str to list, there is usually nothing to worry
about.

## The numeric types beyond int and float

`int` and `float` cover most work, and two more exist for cases where floats
give the wrong answer.

`decimal.Decimal` represents numbers in base ten, so `Decimal("0.1") * 3` is
exactly `Decimal("0.3")` rather than a hair off. It is the right type for
money, invoices, tax and anything where a result will be compared against a
figure a person calculated. Build it from a **string**, not a float:
`Decimal(0.1)` faithfully captures the float's error, which defeats the point.

`fractions.Fraction` holds an exact ratio, so `Fraction(1, 3) * 3` is exactly
1. It is the right type for exact rational arithmetic, and it is slower and
grows in memory as denominators multiply, so it belongs in calculations rather
than in stored data.

Both convert to and from the ordinary types, and both interoperate with `int`
&mdash; but mixing either with `float` in one expression converts back to
`float` and reintroduces the error you were avoiding, which is the trap. If a
calculation is meant to be exact, every value in it has to be the exact type.

`complex` also exists, written `3+4j`, and is genuinely used in signal
processing and geometry. It is worth knowing mainly so that `j` in a numeric
literal is not a mystery.

## Convert once, at the edge

The thread running through this page is that conversion is a decision, and the
useful discipline is to make each decision exactly once, where the data enters
the program.

A value read from a file, a form, an environment variable or an API is text. If
it is converted at the point of use, every use site repeats the conversion,
every use site has to handle the failure, and the sites will eventually
disagree &mdash; one treats an empty string as zero, another as an error, a
third crashes. The type of the value becomes something a reader has to infer
from context.

Converting at the boundary means one place decides what a bad value means, and
everything after that point works with a real `int`, `date` or `Decimal`. The
error, when it comes, names the input and the field rather than surfacing as a
`TypeError` deep in a calculation.

This is the same argument as validating nested data at the boundary, and the
same argument for keyword-only parameters: push the ambiguity to one place, as
early as possible, and let everything downstream rely on what it was given.

## The one conversion Python does silently

Everything on this page says Python refuses to convert without being asked,
which is true with one systematic exception: numeric promotion.

Mixing an `int` and a `float` in an expression converts the `int` to a `float`
first, so `1 + 2.0` gives `3.0` and `1 / 2` gives `0.5` rather than `0`. Mixing
a `bool` with a number treats `True` as 1 and `False` as 0, which is why
`sum([True, False, True])` is 2 &mdash; occasionally useful for counting how
many conditions held, and occasionally a surprise.

The rule is that Python converts within the numeric tower only, and only in the
widening direction, where nothing is lost. `int` to `float` is allowed; `str`
to anything is not. That is why `True + 1` works and `"1" + 1` does not, which
looks inconsistent until you see the boundary it is drawing.

The one place the widening does lose something is very large integers, where
converting to `float` loses precision even though the conversion is nominally
widening. It is the exception to the exception, and it only bites at magnitudes
most programs never reach.

## Questions people ask

<strong>Why does `int("3.9")` fail when `int(3.9)` works?</strong> The string is
not an integer literal, so it refuses rather than choosing a rounding
direction. Use `int(float("3.9"))` when you mean truncation.

<strong>How do I convert a list of strings to numbers?</strong>
`[int(x) for x in items]`, or `list(map(int, items))`.

<strong>What is the difference between `str` and `repr`?</strong> `str` is for
people, `repr` is for programmers and aims to be unambiguous. `print` uses
`str`; the interactive prompt and containers use `repr`.

<strong>Why is `0.1 + 0.2` not `0.3`?</strong> Binary floating point cannot
represent those decimals exactly. Use `math.isclose` to compare, or
`decimal.Decimal` for money.

<strong>Does `int()` round or truncate?</strong> Truncates toward zero, so
`int(-3.9)` is `-3`. `round` is the one that rounds.

<strong>How do I convert between a string and bytes?</strong>
`text.encode("utf-8")` and `data.decode("utf-8")`. Both need an encoding, and
guessing is where mojibake comes from.

<strong>Can I convert a dictionary to a list of pairs?</strong>
`list(d.items())`. Plain `list(d)` gives the keys.

<strong>Should I annotate types instead of converting?</strong> They are
different jobs. An annotation documents and is checked by tools; it does not
convert anything at runtime.

<strong>How do I convert a string to a date?</strong>
`datetime.strptime(text, fmt)` with an explicit format, or
`datetime.fromisoformat` for ISO-8601 text. Neither guesses.

<strong>What does `int()` with no argument give?</strong> Zero. Every numeric
constructor called with nothing returns its zero value, which is occasionally
useful as a default factory.

## Recap in one screen

- Each type's name is its conversion; there is nothing extra to memorise.
- Input is always text, and Python will never convert it for you &mdash; that
  refusal is what makes `"3" + 4` an error rather than a silent bug.
- `int` from a string is strict, `int` from a float truncates toward zero, and
  `round` rounds halves to even.
- `bool` on a string only asks whether it is empty, so parsing a boolean from
  text needs an explicit mapping.
- Narrowing conversions lose information silently &mdash; duplicates, order,
  precision, the difference between missing and `"None"`.
""")


extend("conditional_expressions", """
## Seeing the or trap fail

The `or` shorthand and the explicit conditional look interchangeable until a
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

They agree on `"set"` and on `None`, and disagree on everything else. `or`
replaces the empty string, the zero, the `False` and the empty list &mdash;
every one of which might be a legitimate value somebody deliberately supplied.

The cases where this matters are ordinary rather than exotic. A quantity of
zero, an empty search box, a `False` flag the user actually turned off, an
empty list meaning "no tags". In each, `or` silently substitutes a default over
the top of a real answer, and the bug reads as "my setting does not take
effect".

`or` is still fine when every falsy value genuinely means "absent" &mdash;
which is most often true for strings that are either a name or nothing. The
discipline is to notice that you are making that claim rather than reaching for
the shorter form by reflex.

## It is an expression, and that is the whole distinction

Everything on this page follows from one fact: `x if c else y` produces a
value, and `if c:` does not.

An expression can go wherever a value can. That is why it works inside an
f-string, as a function argument, as a dictionary value, inside a comprehension
and on the right of an assignment. A statement can go in none of those places,
which is why the conditional expression is not a shorter `if` &mdash; it is the
only form that fits where a value is required.

The converse is equally firm. An expression must produce a value on every path,
which is why the `else` is compulsory and why there is no one-armed version. It
also cannot contain statements: no assignment, no `raise`, no `return` inside
it. If the branches need to *do* something rather than *be* something, the
statement form is the only option.

This also explains the reading order. `x if c else y` puts the common case
first because the whole thing is a value with a qualification attached, in the
way English does &mdash; "the total, if there is one, otherwise zero". A
statement starts with the question because it is about control flow, and
control flow starts with a decision.

## The walrus, and the other one-liner

A near neighbour worth distinguishing, because both compress a few lines into
one and they do different things.

`:=`, the walrus operator, assigns *inside* an expression, so a value can be
computed and tested in one place:
`if (n := len(items)) > 10:` binds `n` and compares it, and `n` is then
available in the body without a second call. In a comprehension it is the way
to avoid computing something twice:
`[y for x in data if (y := f(x)) is not None]` calls `f` once per item rather
than once in the filter and again in the expression.

The distinction from a conditional expression is clean. The walrus is about
*naming* a value you are already computing; the conditional expression is about
*choosing* between two values. They combine happily and neither replaces the
other.

Both share a caution: they earn their place when they remove a genuine
repetition or make a line fit where a statement cannot. Used to compress code
that was already clear, both make a reader stop, and neither is worth that.

## Where you will actually meet it

Four places account for nearly every conditional expression in real code, and
all four share the property that a statement could not go there.

**Inside an f-string.** `f"{count} item{'s' if count != 1 else ''}"` handles the
plural without building the string in two steps. This is the single most common
use, and it is worth having in your fingers.

**As a default that depends on something.**
`timeout=timeout if timeout is not None else DEFAULT` in an argument list, or
as a dictionary value in a literal being constructed.

**Inside a comprehension.** Choosing what each item becomes, as opposed to
filtering which items appear &mdash; the distinction covered elsewhere in the
track.

**As a `key=` argument.** `sorted(rows, key=lambda r: r.score if r.score is not
None else -1)` puts missing values at one end without filtering them out first.

What none of these have in common with an `if` statement is that they are
producing a value in the middle of an expression that is already underway. That
is the whole niche, and reaching for the form outside it &mdash; on a line of
its own, assigning to a variable, when a plain `if` would do &mdash; is where
it starts costing readability rather than saving it.

## When the statement is the better tool

The conditional expression is not a compressed `if`, and treating it as one
produces the code that gives it a bad name. Three signals that the statement
form is what you want.

**The branches do something rather than produce something.** Logging, raising,
assigning to more than one name, calling for a side effect. None of these fit
in an expression, and contorting them to fit &mdash; a tuple of calls, an `or`
chain with a function that raises &mdash; produces code that is clever and
unreadable in the same stroke.

**There are more than two outcomes.** A chain of `else`s pushes the default to
the far end of the line and makes inserting a case an edit in the middle of a
string of keywords. A sequence of `if` statements, or a table of thresholds, is
both clearer and easier to change.

**Either branch is long.** Once the line wraps, the reader has to reassemble it
across two lines to find where the condition sits. A four-line `if` costs three
lines nobody has ever regretted.

The version of the rule worth keeping: use the expression when you need a
value *here*, in the middle of something else. Use the statement when you are
deciding what the program does next.

## Questions people ask

<strong>Why is the condition in the middle?</strong> Because the expression is
a value with a qualification, and putting the common case first makes it read
as a sentence.

<strong>Can I leave out the `else`?</strong> No. An expression must produce a
value on every path.

<strong>Can I nest them?</strong> Legally yes, readably no past one level. A
sequence of `if` statements or a table of bands is clearer.

<strong>Is it slower than an `if` statement?</strong> No, they compile to
essentially the same bytecode.

<strong>Can I use it on the left of an assignment?</strong> No.
`(a if c else b) = 1` is not valid; only names and subscripts can be assigned
to.

<strong>What is Python's version of the ternary `?:`?</strong> This is it.
Python spells it with words rather than punctuation, deliberately.

<strong>Can I put a `raise` in one?</strong> No, `raise` is a statement.
There is an idiom using `or` with a function that raises, and it is worse than
writing the `if`.

<strong>Does it short-circuit?</strong> Yes. Only the branch that is chosen is
evaluated, so the other side can safely be something that would fail.

<strong>Can I use it with `and`/`or` in the condition?</strong> Yes, and
brackets are worth adding when you do &mdash; the precedence is correct but not
obvious to a reader.

<strong>Does it work in a lambda?</strong> Yes, and it is one of the few ways
to get a decision into one, since a lambda body must be a single expression.

<strong>Is there a null-coalescing operator like `??`?</strong> No. The
explicit `x if x is not None else y` is Python's version, and its verbosity is
deliberate &mdash; it makes you say which falsy values you meant.

<strong>Can the two branches return different types?</strong> Yes, nothing
stops you. Whether the caller can cope with either is a separate question, and
usually the answer is that it should not have to.

## Recap in one screen

- `value_if_true if condition else value_if_false` &mdash; the value first, the
  condition second.
- It is an expression, so it fits inside f-strings, comprehensions and argument
  lists where a statement cannot.
- The `else` is compulsory, because an expression must always produce
  something.
- `x or default` replaces every falsy value, not just `None`; use the explicit
  `is not None` form when zero or empty is legitimate.
- One condition and short values on one line; past that, write the statement or
  put the bands in a list.
""")


extend("match_and_case", """
## Destructuring in one step

The argument for `match` is not tidiness, it is that the pattern checks the
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
no pattern mentions, and it still matches &mdash; mapping patterns check that
the named keys are *present*, not that they are the only ones, which is what
makes them usable against real payloads.

The string falls through to `case _`, because a mapping pattern does not match
a non-mapping. Written with `if`, that safety would have been an explicit
`isinstance(e, dict)` that somebody has to remember.

And `x`, `y`, `k` and `t` are bound by the match itself. The equivalent
`if`-chain needs a key check and a lookup for each, in the right order, with
the lookups repeating what the checks just established.

## The bare name that swallows everything

A bare name in a pattern does not compare against that name. It is a **capture
pattern**: it matches anything at all and binds the name to whatever it caught.

Python protects you from the obvious form of the mistake. Writing a capture
before other cases is a compile-time error, and the message is unusually
direct:

```
SyntaxError: name capture 'OK' makes remaining patterns unreachable
```

What it cannot protect you from is the same mistake in the last position, where
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

500 "matched OK", because `case OK:` matched everything the earlier case did
not. And the constant is gone &mdash; `OK` was rebound each time the capture
fired, so after the loop it holds 500.

The fix is a dotted name, which is a **value pattern** and does compare:

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

This is why enums pair so naturally with `match`: `case Colour.RED` is
unambiguous, and an enum gives you the dotted form for nothing. Literals work
too. It is only bare names that capture.

## Not exhaustive, and what that means

Languages that popularised pattern matching usually check that every possible
case is handled, and refuse to compile if one is missing. Python does not.

If no case matches and there is no `case _`, the `match` statement simply does
nothing and execution continues on the next line. No exception, no warning. A
value that falls through leaves no trace, and the symptom appears later as a
result that was never computed.

That makes `case _` more important than a default clause usually is. Ending
with one that raises &mdash; or at minimum logs the unhandled value &mdash;
converts a silent no-op into something you can find:

```python
        case _:
            raise ValueError(f"unhandled event: {event!r}")
```

The same applies inside a function returning a value: a `match` where every
case returns will return `None` for an unmatched value, which then travels
somewhere else before failing. Making the fallthrough explicit is the habit
worth forming from the first `match` you write.

## Guards, classes and the shapes worth knowing

Beyond literals and mappings, three pattern kinds cover most real use.

**Sequence patterns** match lists and tuples structurally. `case [x]` matches a
one-item sequence, `case [first, *rest]` matches any non-empty one and splits
it, `case []` matches empty. They do not match strings, which is deliberate
&mdash; a string is a sequence of characters and matching it as one is almost
never what anybody means.

**Class patterns** match an instance and can read attributes:
`case Point(x=0, y=y)` matches a `Point` whose `x` is zero and binds its `y`.
Dataclasses and named tuples support the positional form, `case Point(0, y)`,
via `__match_args__`.

**Guards** attach a condition to a pattern with `if`:
`case [x, y] if x == y` matches a two-item sequence whose items are equal. The
pattern narrows the shape, the guard narrows the values, and a guard that fails
lets the next case try &mdash; it does not abandon the whole `match`.

The combination is what makes the feature earn its keyword. "A two-element list
of integers where the first is negative" is one line, and the `if`-chain
equivalent is a length check, two `isinstance` calls and a comparison in a
specific order.

## A worked example: a small command parser

Every pattern kind in one function, doing the job `match` was added for:

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

Read the cases in order. The first uses `|` for alternatives, both of which are
one-word sequences. The second matches `add` followed by any number of items
and binds them, with a guard rejecting the case where there are none &mdash;
which is why bare `"add"` falls through to the catch-all verb case rather than
reporting "adding 0". The third requires exactly two words, so `get` with two
arguments would not match it.

The fourth is the interesting one: `[verb, *_]` matches any non-empty list,
binds the first word and discards the rest with `_`. The last handles the empty
string, whose `split()` gives `[]`, which no sequence pattern with a required
element can match.

Written as an `if`-chain, each of those becomes a length check plus an index
plus a comparison, in an order that has to be right. Here the shape and the
extraction are the same expression, and a case that does not fit simply does
not match.

## Enums, the natural partner

The capture-pattern trap has a structural fix rather than a discipline one: use
an enum, and the problem cannot arise.

An enum member is always reached through a dotted name &mdash; `Colour.RED`,
`Status.NOT_FOUND` &mdash; which makes every reference a value pattern by
construction. There is no way to accidentally write the bare form, because the
bare form does not name anything.

Two further benefits follow. The set of valid values is written down in one
place, so a reader can see what the `match` is dispatching over without
gathering the cases. And because the members are objects rather than integers,
a typo is an `AttributeError` at the point of the mistake rather than a case
that silently never fires.

This is the shape most `match` statements in well-organised code take: an enum
or a set of classes defining the alternatives, and a `match` that handles each
one and ends with a `case _` that raises. Between them, the two make the set of
cases explicit and the missing case loud &mdash; recovering most of what the
exhaustiveness checking of other languages provides, without the language doing
it for you.

## Questions people ask

<strong>Is there fall-through like C's switch?</strong> No. The first matching
case runs and the statement ends. No `break` is needed or allowed.

<strong>Can I match on types?</strong> Yes, with a class pattern: `case int():`
matches any integer. Note the brackets &mdash; `case int:` without them is a
value pattern comparing against the type object.

<strong>Does a mapping pattern require exact keys?</strong> No, extra keys are
allowed. Use `**rest` to capture them.

<strong>Can I bind the whole value as well as its parts?</strong> Yes, with
`as`: `case {"type": "click"} as event`.

<strong>Why does `case [x]` not match a string?</strong> Sequence patterns
deliberately exclude `str`, `bytes` and `bytearray`.

<strong>Is `match` a keyword now?</strong> It is a soft keyword, so existing
code using `match` as a variable name still works.

<strong>Should I convert my `if`-chains?</strong> Only where they are inspecting
shape. For comparing one value against a few constants, the chain is fine and
runs on older Python.

<strong>Can a guard reference names bound by the pattern?</strong> Yes, and
that is the usual reason to write one &mdash; the pattern binds, then the guard
tests what it bound.

<strong>Is `match` faster than an `if`-chain?</strong> For literals they are
comparable. For structural patterns it is usually faster than the equivalent
checks, and speed is not the reason to choose it.

<strong>Can I match against a set of allowed values?</strong> Use `|` between
literals in one case, or a guard with `in` when the collection is built
elsewhere.

## Recap in one screen

- `match` tests patterns, not conditions; the pattern checks shape and binds
  parts in one step.
- A bare name captures and matches everything &mdash; use a literal or a dotted
  name to compare against a constant.
- Mapping patterns allow extra keys; sequence patterns never match strings.
- Nothing is exhaustive: an unmatched value falls through silently, so end with
  `case _` that raises or logs.
- Reach for it when inspecting the shape of data, and keep `if`/`elif` for a
  few literal comparisons. Requires Python 3.10.
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
runs first, keeping the odd numbers, and only then does the leading conditional
run on what survived.

Written out as a loop, the order is obvious:

```python
result = []
for n in nums:
    if n % 2:                 # the trailing filter
        result.append(n if n > 0 else 0)
```

The comprehension writes the append expression first and the filter last, which
is the reverse of the order they execute in. That is the single fact that makes
combined comprehensions hard to read, and it is why one filter and one
conditional is a sensible ceiling.

## Why the else is compulsory in one place and forbidden in the other

This looks like an inconsistency and is a direct consequence of what each `if`
is doing.

The `if` at the front is part of the **expression** that produces each item. An
expression must produce a value on every path &mdash; there is nowhere for
"produce nothing" to go, because the comprehension is going to append whatever
it evaluates to. So the `else` is required, exactly as it is in a conditional
expression anywhere else.

The `if` at the end is a **filter clause**, part of the comprehension's
machinery rather than of the expression. It answers one question: does this
item continue to the expression, or not. There is no second branch for an
`else` to introduce, because "not kept" is already the alternative.

Trying the wrong one is worth doing once so the error is familiar.
`[n for n in nums if n > 0 else 0]` is a `SyntaxError`, and the message points
at the `else`. `[n if n > 0 for n in nums]` is also a `SyntaxError`, because
the expression is incomplete.

## Filtering to make the expression safe

The execution order is not trivia; it is what lets the filter protect the
expression:

```python
rows = [{"score": 50}, {"score": None}, {"score": 90}]

print([r["score"] * 2 for r in rows if r["score"] is not None])
```

```
[100, 180]
```

The `None` row never reaches the multiplication. Swap the two clauses in your
head &mdash; expression first &mdash; and it would raise `TypeError` on the
second row.

This is the standard shape for data with gaps, and it is better than the
alternative it is often confused with. Writing
`[r["score"] * 2 if r["score"] is not None else None for r in rows]` produces
an entry for every row, including a `None` in the middle of what is supposed to
be a list of numbers, which pushes the problem to whatever consumes the result.

Deciding between them is deciding what a missing value means: filter when the
row should not be in the output, choose when it should be present with a
substitute. Both are legitimate; picking one by accident is not.

## Several filters, and the nested case

Chained filters mean `and`:

```python
[n for n in nums if n > 0 if n % 2 == 0]
```

is identical to one filter with `and`. The chained form occasionally reads
better when the conditions are unrelated tests; the combined form is more
familiar. Neither is wrong.

Nesting is where care is needed, because a trailing `if` attaches to the clause
it follows:

```python
[n for row in grid for n in row if n % 2]
```

The filter is after the inner `for`, so it filters cells. Move it up, to
`for row in grid if len(row) > 2 for n in row`, and it filters rows instead.
Both are legal and they mean entirely different things, with no visual signal
beyond position.

The clauses read in the same order as the equivalent nested loops, outermost
first. That is worth stating because the guess most people make is the
opposite, and the code will run either way while producing the wrong answer.

## The same two positions, everywhere

Nothing on this page is specific to lists. Dict comprehensions, set
comprehensions and generator expressions all carry the same two `if` positions
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

The filter sits at the end in all three. A conditional expression, when used,
sits at the front &mdash; in the value slot for a dict, in the item slot for a
set or generator. In a dict comprehension it can appear in either the key or
the value, or both, which is legal and almost always worse than a loop.

The generator expression case is worth calling out because the filter there is
doing something the others are not: it decides which items are ever computed at
all. In a list comprehension a filtered-out item costs a test; in a generator
feeding `sum` over a large file, the filter is what stops work from happening.

## When the filter is expensive

The trailing filter runs on every item, and the leading expression runs only on
survivors. That is usually the efficient way round, and occasionally it is not.

If the test itself is costly &mdash; a lookup, a regular expression, a parse
&mdash; and the expression needs the same computed value, the naive
comprehension does the work twice:

```python
[parse(line) for line in lines if parse(line) is not None]
```

`parse` runs twice for every line that survives. The walrus operator computes
it once and reuses it:

```python
[value for line in lines if (value := parse(line)) is not None]
```

The assignment happens in the filter, and the name is available to the
expression at the front &mdash; which reads oddly, since the expression is
written first, but follows directly from the filter running first.

Before Python 3.8 the idiom was a nested comprehension:
`[v for v in (parse(l) for l in lines) if v is not None]`, computing the values
in an inner generator and filtering the results. That still works and is
arguably clearer, since it separates the two steps rather than hiding an
assignment inside a condition.

## The rule, in one line

Everything on this page reduces to a sentence worth keeping: **the `if` at the
front chooses a value and needs an `else`; the `if` at the end chooses an item
and cannot have one.**

If you can only remember one consequence of that, make it the length. A
comprehension whose result must be the same length as the input needs the
leading form. One whose result may be shorter needs the trailing form. Asking
"how many items should come out" answers which `if` you want faster than
recalling the syntax rules does.

And when both appear, remember they run in the opposite order to the one they
are written in. The filter decides what survives; the expression then decides
what each survivor becomes. Every confusing combined comprehension is that
inversion catching someone out.

## Questions people ask

<strong>Which `if` runs first?</strong> The trailing filter, always &mdash;
even though the conditional expression is written before it.

<strong>Can I use `else` with the trailing `if`?</strong> No, it is a syntax
error. There is no second branch for a filter.

<strong>Can I filter on the computed value rather than the source?</strong> Not
directly, without computing it twice. The walrus operator does it in one pass:
`[y for x in data if (y := f(x)) > 0]`.

<strong>Does this work in dict and set comprehensions?</strong> Yes, identically.
The two positions and their rules are the same in all of them.

<strong>Are two filters slower than one `and`?</strong> No, they compile to the
same thing.

<strong>How many clauses is too many?</strong> One `for`, one filter, and
optionally one conditional expression. Past that, the loop is easier to read
and to change.

<strong>Can the filter reference the loop variable of an outer clause?</strong>
Yes. Every clause can see the variables bound by the clauses to its left.

<strong>Can I put the filter before the `for`?</strong> No. The clause order is
fixed: expression, then `for`, then any `if`. The only `if` that comes first is
part of the expression.

<strong>Why does my comprehension raise on some items?</strong> Almost always
because the expression is running on items the filter should have removed
&mdash; or because the filter is testing something different from what the
expression uses.

<strong>Is there a way to skip an item from the expression?</strong> No. An
expression must produce something, so skipping is the filter's job. That
separation is the reason for the two positions.

<strong>Do comprehensions with filters build the list lazily?</strong> No, a
list comprehension builds the whole thing. Use a generator expression when the
filtering should happen on demand.

<strong>Can I filter on the index?</strong> Only by supplying one:
`[x for i, x in enumerate(items) if i % 2 == 0]`.

## Recap in one screen

- The trailing `if` filters and takes no `else`; the leading `if`/`else`
  chooses and requires one.
- Filter first, then the expression &mdash; the opposite of the written order.
- That ordering is what lets a filter guard the expression against `None` or a
  division by zero.
- Chained filters mean `and`; in a nested comprehension a filter attaches to
  the clause it follows.
- One `for`, one filter, one conditional: past that a loop reads better and
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

The middle column is the bug. `find` returned 0 &mdash; the item *was* found,
at the first position &mdash; and `not result` reported it as missing. The
right-hand column, testing `is None`, is correct for all three.

Notice which case fails: the first element. A test suite that searches for
something in the middle of a list passes, and the bug waits for real data where
the match happens to be first. That is the characteristic shape of truthiness
bugs &mdash; they are correct for most inputs, which is why they survive
review.

## Giving your own objects a truth value

Truthiness is not a fixed list. Python asks the object, and any class can
answer.

When you write `if obj:`, Python calls `__bool__` if the class defines one. If
it does not, it falls back to `__len__` and treats zero as false. If neither
exists, the object is always truthy &mdash; which is why an instance of a plain
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
it is the usual choice for anything container-like. `__bool__` is for objects
that have a notion of empty without a length &mdash; a connection that is open
or closed, a result that succeeded or failed.

The caution is that this is exactly the mechanism that makes truthiness
ambiguous. An object that is falsy when empty cannot be distinguished from
`None` by `if obj:`, so any code that treats "absent" and "empty" differently
still has to use `is None`. Some libraries make this sharp: a pandas DataFrame
raises rather than guessing when you put it in a condition, on the grounds that
"empty" and "all values false" are both plausible readings.

## When None itself is a valid value

Occasionally `None` is a legitimate value in the data, and then it cannot also
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

`object()` creates something that is equal only to itself, so `default is
MISSING` is true exactly when the caller did not pass a default. Now
`get(d, "k", None)` and `get(d, "k")` mean different things &mdash; the first
supplies `None` as the default, the second asks for an error &mdash; which is
impossible if `None` is itself the sentinel.

This is not a common need, and it is worth recognising because the standard
library uses it. `dict.pop` distinguishes "no default given" from "default of
`None`" in exactly this way, and several libraries expose their sentinel by
name so callers can test against it.

The plainer version of the same idea is a module-level constant with a name
that says what it means, which reads better in a traceback than
`<object object at 0x...>`.

## Where None comes from

`None` rarely gets written into your data deliberately. It arrives, and knowing
the sources makes it predictable rather than mysterious.

**A function that did not return.** Any function reaching its end without a
`return` returns `None`, and so does a bare `return`. This is the biggest
source: a function with a `return` inside an `if` and nothing after it returns
`None` for every input that misses the branch, silently.

**An in-place method.** `sort`, `reverse`, `append`, `update` and their
relatives all return `None` on purpose, so `x = x.sort()` replaces a list with
nothing.

**A lookup with a default.** `d.get(k)` returns `None` when the key is absent,
as do `os.environ.get`, `re.match` when the pattern does not match, and a great
many library functions that mean "nothing here".

**A database or JSON null.** `null` in JSON becomes `None`, and a nullable
column comes back the same way. This is the one where `None` is genuinely part
of the data rather than a signal, and where the "absent versus empty"
distinction matters most.

**An uninitialised attribute.** A class that sets `self.result = None` in
`__init__` and fills it in later hands out `None` to anything that asks too
early.

The pattern across all five is that `None` marks the absence of a value rather
than being one. When it turns up somewhere unexpected, the productive question
is which of these produced it &mdash; and the answer is usually the first.

## Saying "might be None" out loud

The failure mode of `None` is that it travels. A function returns it, the
caller passes it on, and the `AttributeError: 'NoneType' object has no
attribute ...` appears three functions away from the one that produced it.

Type hints are the cheapest defence, because they make the possibility part of
the signature:

```python
def find_user(name: str) -> User | None:
    ...
```

That says, to a reader and to a type checker, that every caller has to handle
the `None` case. A checker will flag `find_user(x).email` as an error before it
runs. On Python before 3.10 the spelling is `Optional[User]` from `typing`,
which means exactly the same thing.

The hint changes nothing at runtime, and that is fine &mdash; the value is in
making the contract explicit. A function whose return type is `User` and which
sometimes returns `None` is lying, and the fix is either to make the hint
honest or to raise instead of returning nothing.

Raising is often the better answer. If a caller has no sensible response to
"not found", returning `None` just moves the crash somewhere less informative.
Returning `None` is right when absence is ordinary and the caller will branch
on it; raising is right when absence means something has gone wrong.

## Questions people ask

<strong>Is `if x:` faster than `if len(x) > 0:`?</strong> Marginally, and
that is not the reason to prefer it. It reads better and works on anything.

<strong>Why is `"False"` true?</strong> Because it is a non-empty string.
Truthiness asks about emptiness, not about meaning.

<strong>Should I write `if x == None`?</strong> No. `is None` is the
convention, is faster, and cannot be overridden by a class.

<strong>What is falsy that people forget?</strong> `0.0`, `Decimal(0)`,
`range(0)`, and `datetime.time(0, 0)` in older Python &mdash; midnight was
falsy until 3.5, which caused real bugs.

<strong>How do I test "not None and not empty"?</strong> `if x:` covers both
when `None` and empty should be treated alike. When they should not, say both:
`if x is not None and len(x):`.

<strong>Does `if not x` work on a generator?</strong> Not usefully. A generator
is always truthy, even if it will produce nothing.

<strong>Why does `numpy` raise on `if array:`?</strong> Because an array with
several elements has no single truth value, and guessing would be wrong half
the time.

<strong>Is `None` the same as `null` in other languages?</strong> It plays the
same role. The difference is that Python's is a real object with a type, so
`type(None)` works and `None.__class__` is `NoneType`.

<strong>Can I subclass `NoneType` or make another `None`?</strong> No.
`NoneType` cannot be instantiated, which is what guarantees `is None` is
reliable.

<strong>Why does `print(f())` show `None` for my function?</strong> Because the
function returned nothing. Usually a `return` is missing on one branch.

<strong>How should a function signal "no result"?</strong> Return `None` when
absence is ordinary and the caller will branch on it. Raise when absence means
something has gone wrong and the caller has no sensible alternative.

<strong>Is there a way to make `None` falsy checks safe?</strong> Not by
changing `None`. The fix is always to say which question you are asking &mdash;
emptiness or absence.

## Recap in one screen

- The falsy values are `None`, `False`, `0`, `0.0`, `""`, `[]`, `{}` and
  `set()`; everything else is truthy, including `"0"` and `"False"`.
- `if not x:` means "empty, zero or missing, and I treat them the same".
- `x is None` means "this was never set", and is the only correct test when
  zero or empty is a legitimate value.
- Use `is` for `None` because there is exactly one of it and `__eq__` cannot
  interfere.
- Your own classes get truthiness from `__bool__`, then `__len__`, and are
  otherwise always true.
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

Four details are worth copying. The `try` contains only the call that can fail,
so a bug in the printing would not be caught as a connection problem. The
`except` names one specific exception, so a `TypeError` from a refactor still
crashes loudly. The `as e` keeps the message, which is the part that tells you
*why* it failed. And the `break` on success means the `else` runs only when
every attempt was used, which is exactly the "gave up" case.

In production this would sleep between attempts, with the delay growing each
time, and would only retry errors that are actually transient &mdash; a
timeout, yes; a `PermissionError`, never, because retrying it will fail
identically four more times and delay the real error.

## The hierarchy, and what catching one gets you

Exceptions form a tree, and catching a class catches every subclass beneath it.
That is what makes `except Exception` catch almost everything, and it is also
how you catch a useful family without listing its members.

At the top is `BaseException`. Directly beneath it sit `SystemExit`,
`KeyboardInterrupt` and `GeneratorExit` &mdash; the three that are *not*
errors, but control flow. `Exception` holds everything else, and is what you
should catch when you must catch broadly, because it leaves those three alone.
This is the concrete difference between `except Exception:` and a bare
`except:`, and it is the reason the bare form makes a program impossible to
interrupt with Ctrl-C.

Below `Exception`, the groupings are useful. `OSError` covers
`FileNotFoundError`, `PermissionError`, `IsADirectoryError`, `TimeoutError` and
the rest of the filesystem and network family, so `except OSError` is a
reasonable way to say "anything the operating system refused".
`ArithmeticError` covers `ZeroDivisionError` and `OverflowError`.
`LookupError` covers `KeyError` and `IndexError`, which is occasionally exactly
what you want when reaching into a structure that might be short or missing a
field.

Knowing the tree turns "catch specific exceptions" from a rule into something
actionable: catch the narrowest class that covers the failures you actually
have an answer for.

## Raising with the cause attached

When you catch an exception and raise a different one, the original is worth
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
the following exception", and your higher-level message. You get the *what* and
the *why* in one traceback.

Without `from`, Python still attaches the original as `__context__` and prints
"During handling of the above exception, another exception occurred" &mdash;
which is nearly as useful and reads as accidental rather than deliberate.
`raise ... from None` suppresses it entirely, which is occasionally right when
the internal error is noise a caller cannot act on.

The reason this matters is that translating exceptions is good practice. A
library that lets a raw `KeyError` from its internal dictionary escape has
leaked its implementation; one that raises `ConfigError("missing 'host'") from
exc` has given the caller something to catch and the maintainer something to
debug.

## Exceptions of your own

Defining one is a single line, and the payoff is that callers can catch exactly
your failure:

```python
class ConfigError(Exception):
    pass
```

Subclass `Exception`, not `BaseException`. Name it for the problem rather than
the place, and end it with `Error` by convention.

The reason to bother is selectivity. A caller who wants to handle a
configuration problem and let everything else through cannot do that if you
raised `ValueError`, because `ValueError` is also what `int()` raises three
frames down. A dedicated class makes the handler precise.

A small hierarchy pays off in a library: one base class such as
`ThingError(Exception)`, with specific subclasses beneath it. Callers who want
everything catch the base; callers who care about one case catch the subclass;
and adding a new failure mode later does not break either.

Attach the data rather than only formatting it into the message.
An exception that stores `self.path` or `self.field` lets a handler make a
decision, where a handler given only a string has to parse English to find out
what went wrong.

## The middle ground between crashing and swallowing

The advice to let exceptions travel and the need for a program that keeps
running are both real, and the space between them is where `logging` lives.

A handler has three honest choices. Handle it &mdash; you know what the failure
means and what to do instead. Translate it &mdash; catch it, raise something
more meaningful with `from`, and let it continue upward. Or record it and
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
&mdash; is the correct shape for batch work, where one bad record should not
end a run over ten thousand. The crucial part is `logging.exception` rather
than `logging.error`, because the first includes the traceback and the second
throws it away.

What is not an honest choice is `except Exception: pass`. It is the one form
that destroys information without replacing it, and the resulting program does
not fail &mdash; it produces output that is quietly incomplete, which is the
hardest kind of wrong to notice.

## Questions people ask

<strong>What is the difference between `except:` and `except Exception:`?</strong>
The bare form also catches `KeyboardInterrupt` and `SystemExit`, so it stops
Ctrl-C from working. Never use it.

<strong>Can I catch several exceptions in one handler?</strong> Yes, with a
tuple: `except (KeyError, IndexError) as e:`.

<strong>Does `finally` run if the `try` returns?</strong> Yes. It runs on every
exit path, including `return` and `break`.

<strong>What happens if `finally` itself raises?</strong> Its exception
replaces whatever was in flight, which is why `finally` blocks should be
simple.

<strong>How do I re-raise after logging?</strong> A bare `raise` inside the
handler re-raises the current exception with its original traceback intact.

<strong>Should I use exceptions for control flow?</strong> Python does, more
than most languages &mdash; `StopIteration` ends every `for` loop. Use them for
the exceptional path, not as a substitute for an `if`.

<strong>Is try/except slow?</strong> Setting up a `try` is nearly free; raising
and catching is not. That is why "ask forgiveness" wins when failures are rare
and loses when they are the common case.

<strong>What is an exception group?</strong> From Python 3.11,
`ExceptionGroup` carries several exceptions at once &mdash; raised by
concurrent code where more than one task failed &mdash; and `except*` handles
them selectively.

## Recap in one screen

- Catch the narrowest exception you have an answer for; a bare `except:` also
  swallows Ctrl-C.
- Keep the `try` block down to the line that can fail, and put the follow-up in
  `else`.
- `as e` keeps the detail, which is the part that makes the message useful.
- `raise NewError(...) from exc` preserves the cause, so the traceback shows
  both the what and the why.
- An exception you cannot handle is information, not a problem &mdash; letting
  it travel beats a quiet wrong answer.
""")


extend("modules_and_import", """
## Circular imports, and how to break one

Two modules that each import the other produce an error that reads as though
something is missing when nothing is:

```
ImportError: cannot import name 'Order' from partially initialized module
'models' (most likely due to a circular import)
```

The mechanism follows directly from "importing runs the file". Module A starts
running and hits `from B import x`. B starts running and hits
`from A import y` &mdash; but A is only half-finished, so `y` does not exist on
it yet. Python has A in `sys.modules` already, so it does not re-run it; it
hands back the partial module, and the name is missing.

Three fixes, in order of preference.

**Move the shared thing.** If A and B both need `Order`, it belongs in a third
module that both import and neither imports back. Most circular imports are a
missing module rather than an import problem.

**Import inside the function.** Moving `from B import x` into the function that
uses it delays it until both modules have finished loading. This works, and it
hides a dependency from anyone scanning the file, so it is a fix rather than a
design.

**Import the module, not the name.** `import B` and then `B.x` at call time
often works where `from B import x` does not, because the attribute is looked
up when used rather than when imported.

The one that does not work is reordering the imports, which usually moves the
error rather than removing it.

## Where installed packages come from

`sys.path` explains where Python looks; it does not explain how anything got
there, and the gap is where most beginner import confusion lives.

`pip install requests` puts the package into the `site-packages` directory of
whichever Python is running `pip`. If you have several Pythons &mdash; the
system one, one from Homebrew, one from a virtual environment &mdash; then
"pip installed it and Python cannot find it" almost always means two different
interpreters. `python3 -m pip install x` avoids that entirely by installing
into the interpreter you just named.

A **virtual environment** is a directory containing its own interpreter link
and its own `site-packages`. `python3 -m venv .venv` creates one and activating
it puts its interpreter first on your `PATH`, so `pip` and `python` both refer
to it. The point is isolation: two projects can depend on incompatible versions
of the same library without either breaking, and the set of packages a project
needs is a property of the project rather than of your machine.

The practical rules are short. One environment per project. Record the
dependencies in a file so the environment can be rebuilt. Never install into
the system Python, which your operating system also uses. And when an import
fails unexpectedly, `python3 -c "import sys; print(sys.executable)"` tells you
which interpreter you are actually running, which resolves the question faster
than anything else.

## Organising modules of your own

A module is a file, so organising code is organising files, and a few
conventions save a lot of trouble.

Group by what things *are for*, not by what they are. A `models.py`,
`views.py`, `utils.py` split works until `utils.py` becomes the place
everything lands. Splitting by feature &mdash; `orders.py`, `billing.py`
&mdash; keeps related code together and keeps the imports between files
shallow.

Keep module-level code to definitions. Anything that runs work, opens files or
makes network calls at import time makes every importer pay for it, including
your test suite. Put it in a function and let the caller decide.

Avoid naming a file after a module you also import. A local `random.py`
shadows the standard library one for your whole program, and the resulting
`AttributeError: module 'random' has no attribute 'randint'` looks impossible
until you spot the file.

And watch the direction of dependencies. If A imports B, B should not need A.
When it does, the two are really one module, or there is a third one waiting to
be extracted &mdash; which is the same conclusion the circular-import section
reached from the other direction.

## Reading an import error

Four messages cover nearly every import failure, and each points somewhere
specific.

`ModuleNotFoundError: No module named 'requests'` means Python looked along
`sys.path` and found nothing. Either it is not installed, or it is installed
for a different interpreter. Check with `python3 -m pip list` using the same
`python3` that failed.

`ImportError: cannot import name 'X' from 'y'` means the module was found and
does not contain that name. Either it is a typo, or the version installed is
older than the one you are reading about, or it is a circular import and the
module is only half-loaded &mdash; the message says so when it can.

`AttributeError: module 'x' has no attribute 'y'` on a standard-library name is
the shadowing case: a file of your own named `x.py` is earlier on the path than
the real module. `print(x.__file__)` identifies it immediately.

`ImportError: attempted relative import with no known parent package` means a
file inside a package was run directly by path. Run it as
`python -m package.module` instead.

The common thread is that the message distinguishes "could not find the module"
from "found it, could not find the name", and that distinction sends you to
completely different places. Reading which of the two you have is most of the
diagnosis.

## Questions people ask

<strong>What is `__init__.py` for?</strong> It marks a directory as a package
and runs when the package is imported. It can be empty, and since Python 3.3 a
package without one mostly works &mdash; but including it avoids surprises.

<strong>Why does `from . import x` fail when I run the file?</strong> Relative
imports need a parent package, which a file run by path does not have. Run it
with `python -m package.module`.

<strong>Does `import` run the whole module?</strong> Yes, top to bottom, once
per program.

<strong>How do I reload a module I changed?</strong>
`importlib.reload(module)` in an interactive session. In a script, restart it
&mdash; reloading has enough sharp edges that it is not worth relying on.

<strong>Where is a module actually loaded from?</strong>
`module.__file__` after importing it, which is the fastest way to confirm you
have the one you meant.

<strong>Is `import x` inside a function slow?</strong> Only the first time.
After that it is a dictionary lookup in `sys.modules`.

<strong>What is the difference between a module and a package?</strong> A
module is a file; a package is a directory of modules. Both are imported the
same way.

<strong>Can a module import itself?</strong> It can, and it gets the partially
initialised version from `sys.modules`. There is no good reason to.

<strong>What does `if TYPE_CHECKING:` do?</strong> Guards imports that exist
only for type hints, so they cost nothing at runtime and cannot cause a
circular import.

<strong>Should I import inside a function to speed up startup?</strong> Only
for genuinely heavy optional dependencies. For anything else the cost is
already paid once and the hidden dependency is not worth it.

## Recap in one screen

- Importing runs the file once, top to bottom, and caches the result in
  `sys.modules`.
- `import x` keeps the prefix and the provenance; `from x import y` is for one
  or two heavily used names; `import *` hides both and can silently overwrite.
- The `__main__` guard is what lets a file be both a script and an importable
  module.
- Circular imports mean a shared piece belongs in a third module.
- One virtual environment per project, and `python3 -m pip` to be certain which
  interpreter you are installing into.
""")


extend("classes_and_objects", """
## A small class, end to end

Everything a plain class usually needs, in one block:

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

Four things earn their place. Every attribute is set in `__init__`, so reading
it tells you everything the object holds. The method validates its input and
says what it received, not just that something was wrong. `__repr__` uses `!r`
on the owner so strings print quoted, which is what makes a `repr` unambiguous.
And `__eq__` returns `NotImplemented` &mdash; not `False` &mdash; for unrelated
types, which lets Python try the other object's comparison before giving up.

## The dunder methods worth knowing

Python's protocols are all spelled as double-underscore methods, and defining
them is how your class gets to behave like a built-in type. Six cover most
needs.

`__repr__` is for programmers and should ideally look like the code that would
recreate the object. `__str__` is for users; if you only write one, write
`__repr__`, because `str()` falls back to it and the interactive prompt and
containers use it regardless.

`__eq__` decides what equality means. Define it and you almost always want
`__hash__` too, because a class that defines `__eq__` without `__hash__`
becomes unhashable and cannot go in a set or be a dictionary key. The pair must
agree: objects that compare equal must hash the same.

`__len__` gives `len()` and, as a side effect, truthiness. `__iter__` makes the
object work in a `for` loop, in unpacking, and in `list()`. `__contains__`
gives `in`, though `__iter__` alone provides a working fallback.

The rest &mdash; arithmetic operators, context managers, comparisons &mdash;
follow the same idea: Python asks the object, and the object answers by having
the method. There is no separate interface to declare. A dataclass writes
`__init__`, `__repr__` and `__eq__` for you, which is three of the six and the
usual reason to reach for one.

## Properties, for when an attribute needs logic

Python has no tradition of writing `get_x()` and `set_x()` for every field,
because it does not need one. Attributes start as plain attributes, and if one
later needs validation or computation, `@property` converts it without changing
a single call site.

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2
```

`c.area` is now computed on access and written without brackets, so it reads
like data. A matching `@area.setter` would let it be assigned, typically to
validate: raising on a negative radius at the moment it is set rather than
discovering it later in a calculation.

The important consequence is cultural. In languages where adding validation
means changing every caller, people write accessors for everything up front,
just in case. In Python that insurance is unnecessary, so the idiomatic style
is a plain attribute until the day it needs to be more &mdash; and the day it
does, nothing outside the class changes.

Use a property when the value is genuinely attribute-like: cheap, side-effect
free, and conceptually part of the object's state. If it does real work, makes
a network call, or can fail in interesting ways, a method with brackets is
honest about that and a property is not.

## What makes a class worth reading

The mechanics of a class are simple; the judgement is in what goes on it, and
a few habits separate classes people can use from classes people work around.

**One responsibility, named.** If the class name needs "and" to describe it, it
is two classes. A name that is a noun for a thing in the problem &mdash;
`Invoice`, `Connection`, `Basket` &mdash; is a better sign than one built from
patterns, like `InvoiceManager` or `DataHandler`, which usually means "some
functions I put somewhere".

**A small surface.** The methods a caller needs should be few and obvious, and
everything else should carry a leading underscore. A class with twenty public
methods is asking its callers to learn twenty things, and most of them
generally turn out to be steps of two or three real operations.

**Attributes that are all set in one place.** `__init__` should establish every
attribute the object will ever have. Attributes that appear halfway through
another method make the object's state depend on call order, which is exactly
the thing that turns into "it works if you call `load()` first".

**Methods that use `self`.** A method that never touches the instance is a
function that has been filed in the wrong place. Moving it out makes it
testable on its own and shortens the class.

The underlying question is whether the class makes calling code shorter and
clearer than the equivalent functions would. If it does not, the functions were
the right answer, and Python is perfectly happy with a module full of them.

## Testing one

A class is easy to test when its state is small and its methods return values,
and difficult when it is neither &mdash; which makes testability a useful
design signal rather than a separate chore.

The straightforward shape is: construct the object, call a method, assert on
what came back or on one attribute. If that is awkward, the reason is usually
one of three things. The constructor does real work, such as opening a file or
making a request, so the object cannot be built in a test without the outside
world; the fix is to take the connection as an argument rather than creating
it. The method returns nothing and changes several attributes, so the assertion
has to know internals; the fix is usually to return the result. Or the outcome
depends on what was called earlier, in which case the test has to replay a
sequence, and that is the sign that the state wants to be smaller.

`__eq__` earns its place here too: it lets a test compare a whole object
against an expected one in a line, instead of asserting on four attributes and
missing the fifth.

## Questions people ask

<strong>Why does every method need `self`?</strong> Because
`a.speak()` is `Dog.speak(a)` &mdash; the instance is passed explicitly rather
than appearing by magic. Python prefers explicit.

<strong>What is the difference between a class and an instance
attribute?</strong> A class attribute is one object shared by everything; an
instance attribute belongs to one object. Assignment always creates the
instance one.

<strong>Do I need getters and setters?</strong> No. Use plain attributes, and
`@property` on the day one needs logic.

<strong>What is `__slots__`?</strong> A declaration of the allowed attributes
that saves memory for classes with many instances, at the cost of losing
dynamic attributes. Worth it rarely.

<strong>Should I write `__str__` or `__repr__`?</strong> `__repr__` first
&mdash; it is what containers and the prompt use, and `str()` falls back to it.

<strong>What is a `@staticmethod` for?</strong> A function that belongs with
the class conceptually but uses neither the instance nor the class. A module
function is often just as good.

<strong>Why does my object print as an address?</strong> Because it has no
`__repr__`. Two lines fix it permanently.

<strong>Can a class have no methods at all?</strong> Yes, and a dataclass with
only fields is a perfectly good way to give a group of related values a name
and a readable `repr`.

## Recap in one screen

- A class bundles data with the functions that operate on it; each instance
  carries its own attributes and shares the methods.
- Set every attribute in `__init__`, so reading the constructor tells you what
  the object holds.
- `self` is the instance, passed explicitly &mdash; `a.f()` is `Cls.f(a)`.
- Class attributes are shared by every instance; assignment through `self`
  always creates an instance attribute instead.
- `__repr__` costs two lines and pays for itself the first time you print a
  list of them; a dataclass writes it, `__init__` and `__eq__` for you.
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
and every cell gets its own line; remove it and the whole table becomes one
long line. The indentation is the logic.

`f"{value:4}"` right-aligns each cell in four characters, which is what stops
the columns drifting once the numbers reach two digits. Counting spaces by hand
works until the data changes; a width does not.

## itertools.product, the flat version

When the nesting exists only to produce every combination, `product` flattens
it into one loop:

```python
from itertools import product

print([f"{x}{y}" for x, y in product("ab", [1, 2])])
```

```
['a1', 'a2', 'b1', 'b2']
```

The order is the same as the nested loops it replaces: the last argument varies
fastest, exactly as the innermost loop does. `product` takes any number of
iterables, and `repeat=` gives the same one several times &mdash;
`product(range(6), repeat=3)` is every three-dice roll without three levels of
indentation.

It is lazy, so it costs nothing until iterated, and it is the right tool when
the combinations are the point: parameter sweeps, test matrices, every pairing
of two lists. It is the wrong tool when the inner loop depends on the outer one
&mdash; iterating the cells of each row, where the rows differ in length
&mdash; because `product` pairs fixed sequences and cannot look at the outer
value to decide what the inner one should be.

`itertools.combinations` and `permutations` cover the related questions, and
both avoid the nested loop plus index arithmetic that would otherwise be
needed to compare every pair without comparing anything with itself.

## The comprehension form, and its reading order

Nested loops have a comprehension equivalent, and the clause order is the thing
people get wrong:

```python
grid = [[1, 2], [3, 4]]

print([value for row in grid for value in row])
```

```
[1, 2, 3, 4]
```

The clauses appear in the same order as the equivalent nested `for` statements
&mdash; outer first, inner second. That is worth stating plainly because the
guess most people make is the opposite, and the wrong order raises a
`NameError` about the inner variable, which at least fails loudly.

What is genuinely confusing is a *nested comprehension*, where one comprehension
appears inside another's expression: `[[f(x) for x in row] for row in grid]`
produces a list of lists rather than a flat one. Here the reading order really
does invert &mdash; the outer clause is on the right and the inner work on the
left.

Between the two, flattening with two `for` clauses is common and readable, and
a comprehension inside a comprehension is where most people should stop and
write the loop. The rule from elsewhere in the track applies: if it needs
decoding rather than reading, the loop was the better answer.

## Let the data decide the loops

A nested loop is usually a description of the data's shape, and when the two
disagree the loop is the thing that is wrong.

If the data is a list of rows and each row is a list of cells, two loops are
correct and the outer variable should be a row rather than an index. If the
data is a flat list and the nesting exists to pair items with each other, the
loops are doing a search and can often be replaced. If the data is a dictionary
of lists, the outer loop takes `items()` and the inner takes the list, and the
key is available at both levels without any bookkeeping.

The mismatch worth watching for is a nested loop over data that is already
flat. Code that iterates a list of records and then, inside, iterates the same
list to find a matching record is describing a join, and a dictionary keyed on
the join field turns it into one pass. The nesting was never about the shape of
the data; it was a linear search wearing a loop.

The opposite mismatch is a single loop over data that is genuinely nested,
usually with manual index arithmetic to work out where each row starts. That is
a flattened structure being reconstructed by hand, and reshaping the data once
is easier than getting the arithmetic right at every use.

The general habit: write the loops that match the structure you have, and if
they are awkward, change the structure rather than the arithmetic.

## Measuring, rather than guessing

The cost of a nested loop can be read off the page, and when it matters it is
still worth measuring, because the constant factors are not visible in the
notation.

Two things make a measurement useful. Run it at several input sizes, not one:
a single number tells you how long something took, and three tell you how the
time grows, which is the property that decides whether the code survives
larger data. Doubling the input should roughly double a linear loop and
quadruple a nested one, and seeing that ratio confirms which you have.

And measure the thing itself, not the setup. `timeit` exists because a naive
timing includes interpreter warm-up, the cost of building the test data, and
whatever else happens to be in the block. It runs the snippet many times and
reports the best, which is the number least polluted by everything else on the
machine.

The result is often surprising in the useful direction: a nested loop over
fifty items is instant and not worth changing, while a linear loop that does
something expensive per item can be the real cost. Reading the structure tells
you how it scales; measuring tells you whether it matters yet.

## Questions people ask

<strong>Can I use the same variable name in both loops?</strong> You can, and
the inner one shadows the outer for the rest of the body. It is legal and
confusing.

<strong>Does `continue` in the inner loop skip the outer one?</strong> No, it
moves to the next inner iteration only.

<strong>How do I break out of both loops?</strong> Put them in a function and
`return`, which is cleaner than any flag.

<strong>Is a nested loop always slow?</strong> No &mdash; it is slow when both
loops grow with the input. A loop over n containing a loop over a fixed three
items is linear.

<strong>What if the inner loop needs the outer index?</strong> `enumerate` at
both levels gives you both, without any `range(len(...))`.

<strong>Why does my inner variable still have a value after the loop?</strong>
Because a `for` loop does not have its own scope. The last value survives,
unlike in a comprehension.

<strong>Is `product` faster than nested loops?</strong> Slightly, and that is
not the reason to use it. It is flatter to read.

<strong>Should I worry about nesting depth for performance?</strong> Worry
about how many times each loop runs, not how deep they are. Three shallow loops
over three items each is nine iterations.

<strong>Can I nest a comprehension inside a loop?</strong> Yes, and it often
reads well &mdash; the loop handles the structure and the comprehension handles
one row.

<strong>Is there a limit on nesting depth?</strong> Python allows about twenty
levels of indentation, which is far past readability. Treat three as the
practical ceiling.

<strong>How do I loop over two grids together?</strong> `zip` the outer
sequences, then loop the pair: `for row_a, row_b in zip(a, b)`.

## Recap in one screen

- The inner loop runs completely on every pass of the outer one; the bodies
  multiply rather than add.
- Where the trailing `print()` is indented decides where rows end &mdash; the
  indentation is the logic, not the formatting.
- `break` leaves one loop; a function and `return` is the clean way out of
  both.
- Two loops over the same collection is `n` squared, and an inner loop that is
  searching can usually be replaced by a set or a dictionary.
- `itertools.product` flattens loops that exist only to produce combinations.
""")


extend("variable_scope", """
## Watching the four scopes resolve

LEGB is easier to trust once you have seen it choose:

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
one. The module's `x` is untouched, because `outer`'s assignment created a name
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

There is a perfectly good global `x`, and the `print` does not reach it. The
assignment on the line *below* made `x` local for the whole function, so the
`print` is reading a local that has not been given a value yet.

The wording of that error changed in Python 3.11; older versions say "local
variable 'x' referenced before assignment". Both describe the same thing, and
the newer one is clearer about it.

## Comprehensions have their own scope, loops do not

Two things that look similar and differ, which explains a family of small
surprises.

A `for` loop does **not** create a scope. The loop variable is an ordinary
local, it survives after the loop ends, and it overwrites anything of the same
name. This is why `for i in range(3)` leaves `i` set to 2 afterwards, and why
reusing a name in nested loops silently shadows.

A comprehension **does** create one. Its loop variable lives only inside it,
does not leak, and does not clobber a name of the same spelling outside. This
changed in Python 3 specifically because the leaking was a common source of
bugs.

The consequence worth remembering is that a comprehension can read enclosing
names but cannot see a class body's names. A comprehension written directly in
a class body that refers to another class attribute raises `NameError`, because
the class body is not a function scope and the comprehension's scope skips
straight past it to the module. It is the one genuinely strange corner of
Python's scoping, and the fix is to compute the value outside the class or pass
it in through the iterable.

## Where scope shows up in practice

The rules are short; the situations where they bite are worth naming.

**A function that "does not update" a counter.** Assigning to a module-level
name inside a function creates a local instead. The function appears to run and
the value never changes. `global` fixes it and is usually the wrong fix &mdash;
returning the new value and assigning at the call site keeps the dependency
visible.

**A callback that captured the wrong value.** Functions built in a loop capture
the *variable*, not its value, so they all see the final one. Binding it as a
default argument &mdash; `lambda i=i: ...` &mdash; captures at definition time.
This is the same late-binding behaviour that makes closures useful, seen from
the wrong side.

**A shadowed builtin.** Naming a variable `list`, `dict`, `sum`, `id` or
`input` hides the builtin for the rest of that scope. The failure comes later,
usually as `TypeError: 'list' object is not callable`, at a line that looks
correct.

**A name that only exists sometimes.** Assigning inside an `if` and reading
after it works when the branch ran and raises `UnboundLocalError` when it did
not. Initialise before the branch.

All four are the same rule seen from different angles: assignment decides where
a name lives, and it decides it for the whole function.

## Why there is no block scope

Coming from C, Java or JavaScript, the most surprising rule is that an `if` or
a `for` does not create a scope. A name assigned inside one is visible after
it, and the loop variable outlives the loop.

This is deliberate, and the reasoning is the same as everywhere else in the
language: functions are the unit of encapsulation, and adding a second, finer
kind of scope would mean two sets of rules for readers to hold. A function body
is one namespace, and where in that body a name was first assigned does not
change what it refers to.

It has practical consequences worth using rather than fighting. A value
computed inside an `if` is available afterwards, so the common pattern of
declaring a variable before a branch purely so it exists later is unnecessary
&mdash; assign it in both branches instead. A loop can leave its last value
behind on purpose, which is occasionally the neat way to say "the last item
that matched".

It also has one real hazard: a name assigned only inside a branch that did not
run does not exist, and reading it raises `UnboundLocalError`. The compiler
knows the name is local, so it does not fall back to a global of the same
spelling. Initialising before the branch, or assigning on every path, is the
fix &mdash; and the error is at least loud rather than silently reading
something from an outer scope.

The one exception, comprehensions, exists precisely because the leaking there
was a genuine problem rather than a convenience.

## Questions people ask

<strong>Does an `if` or a `for` block create a scope?</strong> No. Only
functions, classes, modules and comprehensions do.

<strong>Can I read a global without declaring it?</strong> Yes. `global` is
only needed to *assign* to one.

<strong>What is the difference between `global` and `nonlocal`?</strong>
`global` reaches module level; `nonlocal` reaches the nearest enclosing
function. `nonlocal` fails if there is no such name.

<strong>Why does `items.append(1)` work without `global`?</strong> Because it
mutates the object rather than rebinding the name. Only assignment is affected.

<strong>Does a class body count as an enclosing scope?</strong> No, and this is
the exception that surprises people &mdash; methods do not see class-level
names without `self` or the class name.

<strong>Can I list what is in scope?</strong> `locals()` and `globals()` return
dictionaries of the current names, which is occasionally useful for debugging.

<strong>Is shadowing a builtin ever fine?</strong> In a two-line function where
it is obvious, it does no harm. As a habit it costs more than the shorter name
saves.

<strong>Does `del x` remove a name from scope?</strong> It unbinds it, so a
later read raises `NameError` or `UnboundLocalError`. It does not reach into an
outer scope.

<strong>Why can a method not see class attributes directly?</strong> Because a
class body is not an enclosing scope for its methods. Reach them through
`self.` or the class name.

<strong>What scope does a lambda have?</strong> The same as any function: its
own local scope, with the enclosing one visible. That is why the loop-capture
trap applies to lambdas exactly as it does to `def`.

## Recap in one screen

- Names resolve local, enclosing, global, builtin &mdash; first match wins.
- If a name is assigned anywhere in a function it is local everywhere in that
  function, including lines above the assignment.
- `global` and `nonlocal` rebind rather than shadow, and both are usually a
  sign that a return value would be better.
- Mutating is not assigning: `items.append(x)` needs no declaration,
  `items = [x]` creates a local.
- A `for` loop shares the enclosing scope; a comprehension has its own.
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

The header row uses the same widths as the data rows, which is what keeps the
labels over their columns &mdash; and it works because a string can take an
alignment and a width just as a number can. `{'':>8}` is an empty string padded
to eight, which is how the total line skips columns without counting spaces.

Text is left-aligned and numbers right-aligned, which is not a style preference:
right-aligning numbers puts the decimal points under each other, and that is
what makes a column of figures readable at a glance.

Note that `total` is computed from the full-precision prices, not from the
rounded strings. Formatting is applied only where the number is printed, which
is the habit that stops a column of rounded values from failing to add up to
the rounded total.

## The three parts of a replacement field

Everything inside the braces follows one shape:
`{expression!conversion:format_spec}`, and knowing the three slots explains
several things that otherwise look like separate features.

The **expression** is any Python expression, evaluated at that point.

The **conversion** is `!r`, `!s` or `!a`, applied before formatting. `!r` calls
`repr` instead of `str`, which is what puts quotes around a string and makes
whitespace visible &mdash; invaluable in a debugging print, because `ana` and
`ana ` look identical without it.

The **format spec** is everything after the colon, and it is handed to the
object itself. That is why `:.2f` means something to a float, `%d %B %Y` means
something to a `datetime`, and neither means anything to the other.

The spec can contain its own braces, which is how a width computed at runtime
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
column widths are calculated from the data rather than written into the source.

## Numbers as people read them

A handful of specs cover almost every number a person will look at.

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
`%` multiplies by a hundred and appends the sign, which is the correct way to
show a proportion &mdash; writing `f"{x * 100:.1f}%"` does the same thing with
one more place to make a mistake. `+` forces a sign on positive numbers, which
matters when the number is a change rather than a quantity.

Two further ones are worth having. `:>10,.2f` combines alignment, separators
and decimals, which is the full treatment for a money column. And `:g` chooses
between fixed and scientific notation based on magnitude, which is useful when
the range of values is unknown and awful when it is not, because the column
stops lining up.

For money specifically, remember that floats are not decimals. The formatting
is honest about what it was given; if the arithmetic used floats, the rounding
error was already there before the format spec saw it.

## Where formatting belongs in a program

An f-string is a presentation decision, and presentation decisions are worth
keeping in one layer rather than scattered through the code that does the work.

The symptom of getting this wrong is a function that returns a string where it
should return a number. `def total(items) -> str` that hands back `"£7.50"`
looks convenient at the call site and has thrown away everything else you might
do with the value: adding it to another total, comparing it, storing it,
converting the currency. The caller who needs the number now has to parse the
string back, and the parse will eventually meet a thousands separator.

Keep values as values, and format at the point of output. A reporting function
takes numbers and produces the string; the calculation returns numbers. This is
the same boundary argument as converting input at the edge, run in the opposite
direction: parse on the way in, compute in real types, format on the way out.

The second habit is to keep the template near the output rather than near the
data. A dictionary of format specs per column, applied in the printing loop,
is easy to change when the report changes. Specs scattered through the
functions that computed each figure are not.

There is one honest exception: log messages and error text, where the string
*is* the output and there is nothing downstream to preserve precision for. Even
there, prefer `logging.info("total %s", total)` over an f-string, because the
logger can then skip the formatting entirely when the message is filtered out.

## Questions people ask

<strong>Can I use an f-string for a template stored elsewhere?</strong> No, it
is evaluated where it is written. `str.format` on a stored template is the tool
for that.

<strong>Is an f-string faster than concatenation?</strong> Yes, usually
noticeably, because it does not build intermediate strings.

<strong>How do I put a quote inside?</strong> Use the other quote character, or
&mdash; from Python 3.12 &mdash; the same one.

<strong>Can I have a backslash inside the braces?</strong> Not before Python
3.12. Compute the value on the line above instead.

<strong>What does `f"{x=}"` do?</strong> Prints the expression text, an equals
sign, and the value's `repr`. It is the fastest debugging print there is.

<strong>Do f-strings work with multi-line strings?</strong> Yes, prefix a
triple-quoted string with `f` and the braces work throughout.

<strong>Is it safe to put user input in one?</strong> For output, yes. Never
build SQL or shell commands this way &mdash; use parameters, or the injection
is on you.

<strong>Why does my f-string print braces literally?</strong> Because you
doubled them, or because the `f` prefix is missing. Without the prefix the
braces are ordinary characters.

<strong>Can I format a value whose width I only know at runtime?</strong> Yes,
nest a field in the spec: `f"{value:>{width}}"`.

<strong>What is the difference between `!s` and no conversion?</strong>
Nothing, in practice &mdash; `str` is the default. `!r` is the one worth
typing.

<strong>How do I show a number rounded but keep full precision?</strong> Format
only where you print. The variable is never changed by a format spec, so the
arithmetic that follows still uses every digit it had.

<strong>Can I align text and numbers in the same column?</strong> Yes, and it
usually reads badly. Give the header the same alignment as the data if you
want them to line up, or left-align both.

## Recap in one screen

- The `f` prefix turns braces into slots holding any expression, evaluated
  where it appears in the sentence.
- After the colon is a spec handed to the object: `.2f`, `,`, `>8`, `%` and
  `%d %B %Y` all work this way.
- `!r` shows the `repr`, which is how you see quoting and stray whitespace.
- Formatting changes the display, never the value &mdash; format at the edge
  and keep full precision in the arithmetic.
- `f"{value=}"` prints the expression and its value together.
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

`&` is "in both", `-` is "in the first only", `^` is "in exactly one". Each
replaces a loop containing an `if`, and each is far harder to get subtly wrong
than the loop would be &mdash; there is no index, no accumulator, and no chance
of testing the wrong direction.

`sorted()` around each result is doing real work: a set has no order, so
printing one directly gives an arrangement you must not depend on. Sorting on
the way out is how you get a stable, readable result.

The last line shows the comparison operators. `<=` is "is a subset of", so
`{"bo"} <= a` asks whether every member of the left is in the right. `>=` is
the superset direction, and `isdisjoint` asks whether two sets share nothing
&mdash; which is cheaper than building the intersection just to see if it is
empty.

## The questions each operator answers

The algebra is worth reading as English, because that is how you will recognise
which one you want.

**"Which do they have in common?"** is `a & b`. Shared tags, users in both
groups, fields present in two records.

**"What is in the new one that was not in the old one?"** is `new - old`. Added
files, new permissions, keys that appeared. Reverse the operands for what was
removed, and note that this is the operator people most often get the wrong way
round.

**"What changed either way?"** is `a ^ b`. It is the union of both differences,
and it is the right answer for "what is not the same", which is usually what a
diff wants.

**"Is everything required actually present?"** is `required <= provided`, or
equivalently `required - provided` being empty &mdash; and the second version
is more useful in practice because it tells you *which* are missing rather than
just that some are.

**"Do these overlap at all?"** is `a.isdisjoint(b)`, which stops at the first
shared item rather than computing the whole intersection.

All five work with the method forms too &mdash; `intersection`, `difference`,
`symmetric_difference`, `issubset` &mdash; and the methods accept any iterable,
where the operators require both sides to be sets. `a & [1, 2]` raises;
`a.intersection([1, 2])` does not.

## Where a set fits among the collections

Choosing a container is choosing what you give up, and stating it as a table
makes the decision quick.

A **list** keeps order and duplicates and allows indexing; membership testing
scans. A **tuple** is the same and immutable, so it can be a key. A **set** has
no order, no duplicates and no indexing; membership is constant time. A
**dictionary** is a set of keys with a value attached to each, and it inherits
the set's lookup speed for keys.

The decision usually comes down to one question: what will you ask this
collection most often? If the answer is "give me item three" or "what order did
these arrive in", it is a list. If the answer is "is this one in here", it is a
set. If the answer is "what is the value for this name", it is a dictionary.

The case worth noticing is a list that is only ever asked "is this in here?".
That is a set wearing the wrong type, and converting it once before a loop
changes a scan per iteration into a lookup per iteration. It is one of the very
few performance changes that is both trivial to make and frequently decisive.

The reverse mistake is reaching for a set when duplicates carry meaning.
Counting votes, recording events, keeping a history &mdash; the duplicates
*are* the data, and a set silently deletes them.

## Building one efficiently

Three ways to get a set, and the differences matter once the input is large.

`set(iterable)` is the direct conversion and the one to use when you already
have the items. It is a single pass, and it works on any iterable including a
generator, so `set(line.strip() for line in f)` never builds the intermediate
list.

A set comprehension, `{f(x) for x in items}`, builds and deduplicates in the
same pass. This is better than `set([f(x) for x in items])`, which constructs
the whole list first and then throws it away &mdash; the same waste as wrapping
any comprehension in a converter.

Adding in a loop with `add` is right when the items arrive one at a time or the
loop is doing something else as well. `update` takes an iterable and adds all
of it, so a loop that only calls `add` is usually one `update` in disguise.

The one to avoid is repeatedly rebuilding: `seen = seen | {x}` inside a loop
creates a whole new set on every iteration, which turns a linear job into a
quadratic one. `seen.add(x)` modifies in place, and `seen |= other` does the
same for a batch.

## Questions people ask

<strong>Why is `{}` an empty dictionary?</strong> Dictionaries had the braces
first. `set()` is the only way to write an empty set.

<strong>Can a set contain a list?</strong> No. Members must be hashable, and
lists can change. Use a tuple, or a `frozenset` for a set of sets.

<strong>Does `set()` preserve order?</strong> No. Use
`list(dict.fromkeys(items))` to deduplicate while keeping first-seen order.

<strong>Is `x in a_set` really constant time?</strong> On average, yes. It
hashes once and looks in one place, regardless of size.

<strong>Can I sort a set?</strong> `sorted(s)` returns a list. A set itself has
no order to arrange.

<strong>What is the difference between `remove` and `discard`?</strong>
`remove` raises `KeyError` when the item is absent; `discard` does not.

<strong>Are `1` and `True` different set members?</strong> No. They hash the
same and compare equal, so `{1, True}` has one element.

<strong>Can I use a set as a dictionary value?</strong> Yes. Only keys need to
be hashable; values can be anything.

<strong>How do I find duplicates rather than remove them?</strong> Compare the
lengths, or use `collections.Counter` and keep the entries with a count above
one. A set alone tells you they existed, not which.

<strong>Is a set faster than a dictionary for membership?</strong> They use the
same mechanism, so effectively no. Use a dictionary when you also need a value
attached.

## Recap in one screen

- A set gives up order and duplicates and buys constant-time membership tests.
- `&`, `|`, `-` and `^` answer "both", "either", "only the first" and "exactly
  one" without a loop.
- `{}` is an empty dictionary; `set()` is the empty set.
- Members must be hashable, for the same reason dictionary keys must be: the
  hash decides where the item is stored.
- A list that is only ever asked "is this in here?" wants to be a set, and the
  conversion is often the whole fix for a slow loop.
""")


extend("function_arguments", """
## Watching the default accumulate

The trap is more convincing when the shared object is visible:

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
the list stored there has grown &mdash; it is not that each call somehow gets
the previous result, it is that there has only ever been one list, created when
`def` ran, and every call has been appending to it.

Nothing about this is a special rule for functions. `basket=[]` is an
expression evaluated once, at definition time, exactly like `x = []` at module
level. The surprise comes from expecting the default to be re-evaluated on each
call, which nothing in the syntax promises.

The fix, once more, because it is worth having in your fingers:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

`None` cannot accumulate anything, and the list is built inside the call where
it belongs.

## How a call is matched to a signature

Understanding the binding order makes the error messages readable, and there
are only four steps.

Positional arguments are assigned to parameters left to right. Then keyword
arguments are matched by name to whatever is left. Then any parameter still
unfilled takes its default. Then, if a parameter is still unfilled and has no
default, the call fails.

That order explains the errors. `missing 1 required positional argument: 'x'`
means step four found a gap. `got multiple values for argument 'x'` means a
positional argument filled `x` in step one and a keyword tried to fill it again
in step two &mdash; which is what happens when you pass the first argument
positionally *and* by name. `got an unexpected keyword argument 'timeuot'`
means step two found no parameter of that name, which is the typo case, and is
exactly the error that `**kwargs` would have swallowed.

Two rules follow from the same ordering. In a call, positional arguments must
come before keyword ones, because Python cannot tell where a positional one
belongs once names have started. And in a definition, parameters with defaults
must come after those without, for the same reason from the other side.

## Saying what a parameter expects

Type hints do not convert or enforce anything at runtime, and they are still
the cheapest documentation a signature can carry:

```python
def greet(name: str, times: int = 1) -> str:
    return f"hello {name} " * times
```

The value is threefold. A reader learns what to pass without reading the body.
An editor can complete and check the call. And a type checker run in CI catches
the mismatch before it ships &mdash; which is the only one of the three that
actually prevents anything.

Two conventions are worth adopting with them. Annotate the public functions and
skip the obvious internal ones; annotations on a two-line helper cost more to
read than they explain. And when a parameter can be `None`, say so
&mdash; `def find(name: str) -> User | None` &mdash; because that is the case
callers most often forget and the one a checker most usefully flags.

Hints also document the mutable-default fix nicely: `basket: list | None = None`
states both the type and the fact that omitting it is allowed, which is exactly
what the `None` sentinel means.

## Choosing the default

A default is a decision about what most callers want, and getting it wrong is
quiet: nothing fails, every call site just gets a little longer.

The test is simple. If most calls override the default, the default is wrong.
Either it should be the value people actually pass, or the parameter should be
required so that callers have to think about it. A default that exists only
because the parameter felt like it needed one adds a choice without making one.

Defaults should also be safe rather than convenient. A `timeout=None` meaning
"wait forever" is a default that turns a slow dependency into a hung program;
a finite timeout is the better choice even though it can fail. The same
reasoning applies to `overwrite=False`, `strict=True` and `retries=0`: when in
doubt, default to the behaviour whose failure is loud.

And a default should not depend on the state of the world. Anything evaluated
at definition time &mdash; the current directory, the time, an environment
variable, a config object &mdash; is frozen at import and will be wrong for any
program that changes it afterwards. `None` plus a lookup in the body reads the
value when the call happens, which is nearly always what was meant.

Finally, prefer a default over an optional parameter that changes the return
type. A function that returns a number normally and a tuple when
`verbose=True` has two signatures pretending to be one, and every caller has to
know which it triggered.

## Questions people ask

<strong>Are arguments passed by value or by reference?</strong> Neither, in the
C sense. The function gets another name for the same object, so mutating it is
visible to the caller and rebinding is not.

<strong>Can a default refer to another parameter?</strong> No. Defaults are
evaluated at definition time, when no arguments exist. Use `None` and compute
it in the body.

<strong>Why must defaults come last?</strong> Otherwise a positional call could
not tell which parameter a value was for.

<strong>Is a tuple a safe default?</strong> Yes. Tuples are immutable, so there
is nothing to accumulate.

<strong>How do I force a caller to use names?</strong> Put a bare `*` before
those parameters in the definition.

<strong>Can I see a function's defaults?</strong> `f.__defaults__` for
positional ones and `f.__kwdefaults__` for keyword-only ones.

<strong>How many parameters is too many?</strong> When you are counting on your
fingers at the call site. Group them into an object, or split the function.

<strong>Can I make every parameter keyword-only?</strong> Yes, put the bare `*`
first: `def f(*, a, b)`. Callers must then name both.

<strong>Does the order of keyword arguments matter?</strong> Not to Python. They
are matched by name, so any order works &mdash; though matching the signature's
order helps a reader.

<strong>Can two parameters share a default object?</strong> They can, and they
should not if it is mutable, because then both accumulate into the same thing.

## Recap in one screen

- Arguments match by position first, then by name; positional ones come first
  in a call and non-default parameters come first in a definition.
- Defaults are evaluated once, when `def` runs &mdash; never default to a list,
  dict or set.
- `None` plus a check in the body is the idiomatic fix, and it reads correctly
  in a type hint too.
- A bare `*` makes the parameters after it keyword-only, which is how a call
  site stops being a row of unlabelled values.
- The signature is the part others read most; required parameters are
  requirements, and a default should be the right choice most of the time.
""")
