# -*- coding: utf-8 -*-
"""Content for the pandas track.

Modules of short runnable steps rather than one long program. pandas is a
library where the same expression means different things depending on what
the index holds, whether you are looking at a view or a copy, and which of
several near-identical accessors you reached for - and a single long script
hides which rule produced which line.

Several steps are written so the output contradicts the guess a reader would
make: that filtering then assigning works, that a merge keeps every row, that
an index is just row numbers.

pandas ships with Pyodide (2.2.0 there), so these load from the same CDN as
the interpreter rather than needing a wheel.
"""

TOPICS = []
CHECKS = {}

# Importing pandas under Pyodide raises a DeprecationWarning about pyarrow
# becoming a required dependency in pandas 3.0. It is accurate and completely
# irrelevant here, and it is written to stderr - so without this it would be
# the first thing, in red, in the output of every editor on the track.
#
# Importing pandas once with warnings muted puts it in sys.modules, so the
# reader's own "import pandas as pd" is a cache hit and says nothing. Doing it
# this way rather than with a global filter leaves warnings raised by the
# reader's own code visible, which is the point of showing them.
# The editors on the built pages take their prelude from
# tools/runnable_specs.py; this keeps the step-card editors in step with it
# rather than carrying a second, subtly different copy.
from runnable_specs import _pandas_prelude

PRELUDE = _pandas_prelude()


def topic(slug, title, cat, lead, svg, steps, notes, article, check):
    """One module. `steps` is a list of (heading, blurb, code) triples."""
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "steps": steps, "notes": notes, "article": article, "check": check,
        "wheels": [], "prelude": PRELUDE,
    })
    CHECKS["pandas/%s.html" % slug] = {"check": check}


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


def _arrow(x1, y1, x2, y2, stroke=M):
    return '<path d="M%s %s L%s %s" stroke="%s" stroke-width="2"/>' % (x1, y1, x2, y2, stroke)


def _grid(x, y, cols, rows, cell=14, fill="none", stroke=B):
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(_box(x + c * cell, y + r * cell, cell, cell, fill, stroke, 1, 0))
    return "".join(out)




# ---------------------------------------------------------------------------
# 1. What pandas is for
# ---------------------------------------------------------------------------
topic(
    "what_is_pandas",
    "What pandas Is For",
    "Series and Index",
    "Columns with names, types and an index - and why that is a different thing "
    "from a 2-D array.",
    _svg(_grid(14, 28, 3, 3, 15) + _txt(37, 22, "array", M, 8) +
         _arrow(64, 50, 80, 50) +
         _box(88, 28, 22, 45, S, A) + _box(110, 28, 22, 45, S, A) +
         _box(132, 28, 20, 45, S, A) +
         _txt(120, 22, "columns", A, 8)),
    [
        ("A DataFrame is columns, not a grid",
         "Each column has its own dtype. That is the difference from a NumPy array, "
         "and most of what follows comes from it.",
         '''import pandas as pd

df = pd.DataFrame({
    "name": ["ana", "raj", "kim"],
    "age": [31, 25, 40],
    "score": [8.5, 9.1, 7.2],
    "active": [True, False, True],
})
print(df)
print()
print("one dtype per column:")
print(df.dtypes)
print()
print("a NumPy array has ONE dtype for everything. Forcing this to")
print("an array collapses it to the only type that holds all four:")
print("   ", df.to_numpy().dtype)'''),

        ("The index is not row numbers",
         "It looks like 0,1,2 by default, which hides that it is a real labelled axis.",
         '''import pandas as pd

s = pd.Series([10, 20, 30])
print("default index:", list(s.index))

s2 = pd.Series([10, 20, 30], index=["a", "b", "c"])
print("labelled     :", list(s2.index))
print()
print("s2['b'] ->", s2["b"], "  looked up by LABEL, not position")
print()
print("and the label survives filtering:")
big = s2[s2 > 15]
print(big)
print("   the index is still b, c - not 0, 1")
print()
print("That surviving label is why the next module is about the index.")'''),

        ("Operations align on the index",
         "This is the single biggest difference from arrays, and it is silent.",
         '''import pandas as pd

a = pd.Series([1, 2, 3], index=["x", "y", "z"])
b = pd.Series([10, 20, 30], index=["z", "y", "x"])

print("a:", dict(a))
print("b:", dict(b), "<- reversed order")
print()
print("a + b aligns by LABEL, not position:")
print(a + b)
print()
print("x: 1+30, y: 2+20, z: 3+10")
print()
print("NumPy would have added them position by position.")
print("Missing labels become NaN rather than an error:")
c = pd.Series([1, 1], index=["x", "q"])
print(dict(a + c))'''),

        ("Columns carry names all the way through",
         "You select by meaning rather than by remembering that salary is column 3.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "pune", "delhi"],
    "sales": [10, 20, 30, 40],
})

print("total by city, in one line:")
print(df.groupby("city")["sales"].sum())
print()
print("the equivalent in plain Python needs a dict, a loop and a")
print("decision about what to do with a missing key.")
print()
print("column names survive every operation:")
print(list(df.groupby("city")["sales"].sum().index))'''),

        ("Where pandas beats a dict of lists",
         "Not everywhere. It wins when the data is tabular and the questions are "
         "column-shaped.",
         '''import pandas as pd

rows = [
    {"item": "pen", "qty": 3, "price": 10.0},
    {"item": "book", "qty": 1, "price": 250.0},
    {"item": "bag", "qty": 2, "price": 400.0},
]
df = pd.DataFrame(rows)

df["total"] = df["qty"] * df["price"]
print(df)
print()
print("revenue      :", float(df["total"].sum()))
print("mean price   :", round(float(df["price"].mean()), 2))
print("most expensive:", df.loc[df["price"].idxmax(), "item"])
print()
print("For three rows a loop is fine. The argument for pandas is that")
print("this code does not change when there are three million.")'''),

        ("What pandas is not for",
         "Knowing the boundary saves a lot of fighting with it.",
         '''import pandas as pd
import time

n = 20_000
df = pd.DataFrame({"a": range(n)})

t = time.perf_counter()
out = df["a"] * 2 + 1
vec = time.perf_counter() - t

t = time.perf_counter()
out2 = df["a"].apply(lambda v: v * 2 + 1)
loop = time.perf_counter() - t

print("vectorised : %.4f s" % vec)
print("apply      : %.4f s" % loop)
print("ratio      : %.0fx" % (loop / max(vec, 1e-9)))
print("same       :", out.equals(out2))
print()
print("apply is a Python loop wearing a method call. pandas is fast")
print("only while you stay out of per-row Python.")'''),
    ],
    [
        "A DataFrame is a set of <strong>columns</strong>, each with its own dtype, sharing one index &mdash; not a 2-D array.",
        "The <strong>index</strong> is a labelled axis, not row numbers. It survives filtering, and that surprises people.",
        "Arithmetic <strong>aligns on the index</strong>, by label rather than position. Missing labels become NaN instead of raising.",
        "Columns keep their names through every operation, so you select by meaning rather than by position.",
        "Converting a mixed DataFrame to a NumPy array collapses every column to one dtype, usually <code>object</code>.",
        "<code>apply</code> is a Python loop. pandas is fast only while you stay out of per-row Python.",
    ],
    '''
title: What pandas Is For
intro: Columns with names, types and an index, and why that differs from a 2-D array.

## Two structures

`Series` is a one-dimensional array of values **plus an index** of labels.

`DataFrame` is a set of Series sharing one index. Each column has its own dtype.

That second point is the practical difference from NumPy. A NumPy array has one dtype for the whole block; a DataFrame has one per column. A table with a name, an age, a score and a flag is four dtypes, and that is exactly the shape real data arrives in.

Convert such a DataFrame to a NumPy array and every column collapses to the one type that can hold all of them &mdash; usually `object`, which is a list of pointers with extra steps. That collapse is worth seeing once, because it explains why pandas exists rather than everyone using arrays.

## The index does work you did not ask for

The index looks like row numbers, because by default it is `0, 1, 2`. That default hides what it actually is: a labelled axis that participates in almost every operation.

Two consequences arrive early and confuse people.

**It survives filtering.** Filter a Series down to two of five rows and the index reads `1, 4`, not `0, 1`. The labels came along. Code that then indexes positionally gets the wrong rows or a `KeyError`.

**Arithmetic aligns on it.** Adding two Series matches them up **by label**, not by position. If the labels are in different orders, pandas reorders for you. If one has a label the other lacks, the result is `NaN` there rather than an error.

That alignment is a genuine feature &mdash; it is what makes combining data from different sources safe, because mismatches surface as NaN rather than as a silent off-by-one. It is also the single most surprising behaviour for anyone arriving from NumPy, where `+` is strictly positional.

The index gets a module of its own next, because nearly every pandas confusion traces back to it.

## Names instead of positions

`df["salary"]` says what it selects. `arr[:, 3]` requires you to remember what column 3 was, and breaks silently when a column is inserted.

That is not a small ergonomic point. It is most of why pandas code survives contact with changing data, and why a group-by is one line rather than a dict, a loop and a decision about missing keys.

## When to use something else

**Plain Python** for small, one-off, non-tabular work. A hundred records processed once does not justify the import, and a list of dicts is easier to read.

**NumPy** when the data is genuinely homogeneous and numeric &mdash; a matrix, an image, a signal. pandas adds per-column bookkeeping you are not using, and costs both memory and speed for it.

**A database** when the data does not fit in memory, or when several processes need it at once. pandas assumes one process and one machine.

**Polars or DuckDB** when the data is large and the work is analytical. Both are considerably faster than pandas on big joins and aggregations.

pandas is the right tool for tabular, in-memory, mixed-type data where the questions are column-shaped &mdash; which describes an enormous amount of real work.

## The one performance rule

pandas is a thin, convenient layer over compiled code. It is fast while the work happens inside that compiled layer, and slow the moment it has to call back into Python once per row.

`apply`, `iterrows` and a `for` loop over rows all do exactly that. The last editor measures it, and the gap is large enough that it is usually the whole performance story of a pandas script.

The rule: express operations on **whole columns**. `df["a"] * 2` operates on the column; `df["a"].apply(lambda v: v * 2)` operates on each value from Python and is far slower for the identical result.

There are cases where `apply` is unavoidable, and a module later covers them. Most uses of it are not those cases.

## How this track is organised

The index and selection come first, because they cause the most confusion and everything else depends on them &mdash; including the copy warning, which gets a module to itself because nothing else in pandas wastes as much of people's time.

Then cleaning: missing values, duplicates, strings, types.

Then the aggregation work that is the reason to use pandas at all: group-by, joins, reshaping.

Then time series, reading and writing files, and performance.

Every module is short runnable programs rather than one long script, so you can change one line and see which rule produced which output.

## Where pandas sits

pandas is built **on** NumPy. Underneath each numeric column is a NumPy array, and the arithmetic that runs on a column is the same compiled code.

What pandas adds is bookkeeping: labels for the rows, names and separate types for the columns, and a large library of operations that assume your data is a table rather than a matrix.

That layering explains both its strengths and its costs. Column arithmetic is fast because NumPy is doing it. Anything that has to consult labels, reconcile dtypes, or fall back to Python objects is slower, and that is where pandas code goes wrong.

Above pandas sit the tools that consume it: scikit-learn takes DataFrames, matplotlib and seaborn plot them, and most data pipelines pass them around. Knowing the layer below and the layer above tells you when to drop down to NumPy for speed and when to hand off entirely.

## The vocabulary

A few terms recur constantly, and being precise about them prevents confusion later.

**Series** &mdash; one column: values plus an index, with a single dtype.

**DataFrame** &mdash; several Series sharing one index.

**Index** &mdash; the labels for the rows. The column names are also an Index.

**dtype** &mdash; the type of one column. `object` usually means Python strings.

**Axis** &mdash; `axis=0` is rows, `axis=1` is columns. As in NumPy, the axis you name is generally the one being collapsed or moved along, which is why `df.sum(axis=0)` gives a total per column.

**NaN / NaT / pd.NA** &mdash; missing markers for floats, datetimes and the nullable types.

## Reading pandas output

Printed output carries more information than it appears to, and reading it saves a great many print statements.

The **dtype line** under a Series tells you what you are holding. `int64` and `float64` are numeric; `object` almost always means strings; `datetime64[ns]` means dates have been parsed.

The **index** is the left-hand column, and it is not row numbers. If it reads `0, 3, 7` rather than `0, 1, 2`, the frame has been filtered and the original labels came along.

`Name:` under a Series gives the column it came from.

`[5 rows x 3 columns]` at the bottom of a truncated frame is the real shape, which matters when the display has elided the middle.

Three things worth setting in a notebook: `pd.set_option("display.max_columns", None)` to stop columns being hidden, `display.width` to control wrapping, and `display.float_format` to stop long decimals dominating a table.

## A first session

The shape of almost every piece of pandas work is the same:

**Load** with `read_csv`, saying what you know about types and dates.

**Look** &mdash; `shape`, `dtypes`, `head`, `info`, `describe`, and `value_counts` on the categorical columns.

**Clean** &mdash; fix types, handle missing values, normalise text, remove or aggregate duplicates.

**Reshape** &mdash; filter to what matters, join in what is missing, group and aggregate.

**Output** &mdash; a table, a chart, or a file.

Roughly half of real work is in the middle two steps, which is why this track spends most of its modules there rather than on the aggregation everyone thinks of as the interesting part.

## Two habits worth starting with

**Check after every step that changes the shape.** `len(df)` after a filter or a merge, `df.dtypes` after a load or a concat. Most pandas bugs are silent, and the ones that are not silent are usually caught by one of those two lines.

**Prefer explicit over clever.** `df.loc[mask, "col"]` over `df[mask]["col"]`, named aggregation over positional, `.copy()` where you mean a copy. The explicit form is nearly always the one that keeps working when the data changes.

## Questions that come up first

**Do I need to learn NumPy before pandas?**

Not before, but alongside. pandas hides NumPy most of the time, and then leaks it at exactly the moments that matter &mdash; dtypes, NaN behaviour, broadcasting, views versus copies. Every one of those is a NumPy concept wearing a pandas name, and the modules that cause the most trouble here are the ones where the NumPy layer shows through.

**Why is my column `object`?**

Because it holds Python objects rather than a uniform numeric type &mdash; almost always strings, sometimes mixed types from a messy source. It is the single most common cause of both slow code and surprising results, and `df.dtypes` is how you find it.

**Why did my integers become floats?**

A missing value. NumPy integer arrays cannot hold NaN, so pandas promotes the column. The nullable `Int64` type is the fix.

**Why does my filter return an empty frame?**

Usually a type mismatch &mdash; comparing a string column against a number &mdash; or whitespace and case differences in the values. `value_counts()` on the column shows both immediately.

**Should I use pandas or SQL?**

If the data lives in a database and the operation is a filter, join or aggregate, do it in SQL and bring back less data. pandas is for what happens after that, and for data that never was in a database.

## What this track assumes

That you can read Python, and that you have met lists and dicts. No statistics, no NumPy, and no prior pandas.

The modules are ordered by dependency rather than by glamour. The index, selection and the copy warning come first because everything later depends on them and because they cause the most confusion. Cleaning comes next, because that is where most real time goes. Group-by, joins and reshaping come after, because they are what people think pandas is for and they only work properly once the earlier material is in place.

Each module is six short programs and an article. The programs are the point: changing a value and re-running is the fastest way to find out what a rule actually does, and several of them are written so the output contradicts the guess most people would make.

## The shortest useful summary

A DataFrame is columns with names and types, sharing an index.

The index takes part in almost everything, including alignment, which is silent.

Selection is `.loc` for labels and `.iloc` for positions.

Assignment goes in one `.loc` call, or through an explicit `.copy()`.

Operations on whole columns are fast; anything per row is not.

And when a result surprises you, the answer is nearly always in `df.dtypes`, `df.shape`, or the index &mdash; in that order.

## A closing note

pandas is a large library, and the temptation is to learn it as a list of methods. That does not work well, because the methods are not the hard part.

The hard part is a small number of behaviours that run through everything: the index takes part in operations you did not ask it to; a column has one dtype and that dtype decides what is possible; selection returns something whose relationship to the original is not always specified; and anything that runs Python once per row is slow enough to dominate.

Those four explain most of what surprises people, and each has a module here.

The methods, by contrast, are searchable. Nobody remembers the argument order of `merge` or the exact spelling of every frequency alias, and nobody needs to.

So the useful thing to take from this track is not coverage but a set of instincts: check `dtypes` after loading, check row counts after joining, know whether you are holding a copy, and stay out of per-row Python.
''',
    [
        {"q": "What is the main structural difference between a DataFrame and a 2-D NumPy array?",
         "options": ["Size", "Each DataFrame column has its own dtype; an array has one for everything", "DataFrames are faster", "Arrays cannot hold numbers"],
         "answer": 1,
         "why": "Converting a mixed DataFrame to an array collapses every column to the one type that holds them all, usually object - which is why pandas exists."},
        {"q": "Two Series with the same labels in different orders are added. What happens?",
         "options": ["Added position by position", "Aligned by label first, then added", "An error", "Only the first is returned"],
         "answer": 1,
         "why": "Alignment is by label, not position, and missing labels become NaN rather than raising. This is the biggest departure from NumPy."},
        {"q": "After filtering a Series down to 2 of 5 rows, what does the index look like?",
         "options": ["0, 1", "The original labels of the surviving rows", "Empty", "It is dropped"],
         "answer": 1,
         "why": "The labels come along. Code that then indexes positionally gets the wrong rows or a KeyError."},
        {"q": "Why is `df['a'].apply(lambda v: v*2)` slower than `df['a'] * 2`?",
         "options": ["apply copies the data", "apply calls back into Python once per row instead of staying in compiled code", "apply is deprecated", "They are the same speed"],
         "answer": 1,
         "why": "pandas is fast while work stays inside the compiled layer. Per-row Python is usually the entire performance story of a slow pandas script."},
    ],
)


# ---------------------------------------------------------------------------
# 2. The index
# ---------------------------------------------------------------------------
topic(
    "the_index",
    "The Index",
    "Series and Index",
    "The labelled axis that participates in almost every operation - and causes "
    "almost every surprise.",
    _svg(_box(20, 26, 26, 46, S, A) + _txt(33, 22, "index", A, 8) +
         _box(48, 26, 30, 46, S) + _box(78, 26, 30, 46, S) +
         _txt(78, 22, "columns", M, 8) +
         _arrow(33, 78, 93, 78)),
    [
        ("Every Series and DataFrame has one",
         "It is created for you if you do not supply it, which is why it is easy to "
         "forget it exists.",
         '''import pandas as pd

s = pd.Series([10, 20, 30])
print("values:", list(s.values))
print("index :", list(s.index))
print("type  :", type(s.index).__name__)
print()
df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
print("row index :", list(df.index))
print("col index :", list(df.columns), "<- the columns are an Index too")
print()
print("Both axes are Index objects. Anything true of one is true of the other.")'''),

        ("It survives filtering, and that trips people",
         "The labels come with the rows, so the result is no longer 0..n-1.",
         '''import pandas as pd

s = pd.Series([5, 15, 25, 35, 45])
big = s[s > 20]
print("filtered:")
print(big)
print()
print("index is now:", list(big.index), "<- not 0,1,2")
print()
print("so positional thinking breaks:")
try:
    print(big[0])
except KeyError:
    print("   big[0] -> KeyError: there is no label 0 any more")
print()
print("big.iloc[0] ->", big.iloc[0], "  (position)")
print("big.loc[2]  ->", big.loc[2], "  (label)")'''),

        ("reset_index and set_index",
         "Turning the index into a column, and a column into the index.",
         '''import pandas as pd

df = pd.DataFrame({"city": ["pune", "delhi", "goa"], "pop": [3, 19, 2]})
print("default index:", list(df.index))

by_city = df.set_index("city")
print()
print("after set_index('city'):")
print(by_city)
print("   lookup by label:", int(by_city.loc["delhi", "pop"]))

print()
back = by_city.reset_index()
print("reset_index puts it back as a column:", list(back.columns))
print()
print("drop=True throws the old index away instead of keeping it:")
print(list(df[df["pop"] > 2].reset_index(drop=True).index))'''),

        ("Alignment is the reason it matters",
         "Two objects combined are matched on labels first. This is silent and it is "
         "not optional.",
         '''import pandas as pd

q1 = pd.Series([100, 200, 300], index=["pune", "delhi", "goa"])
q2 = pd.Series([10, 20], index=["goa", "pune"])

print("q1 + q2:")
print(q1 + q2)
print()
print("goa got 300+10, pune got 100+20, delhi had no partner -> NaN")
print()
print("To treat a missing label as zero, be explicit:")
print(q1.add(q2, fill_value=0))
print()
print("Alignment is a safety feature - a mismatch shows up as NaN")
print("rather than as a silent off-by-one.")'''),

        ("Duplicate labels are allowed",
         "Which means a single lookup can return several rows, changing the type of "
         "what comes back.",
         '''import pandas as pd

s = pd.Series([1, 2, 3], index=["a", "b", "a"])
print("index has a twice:", list(s.index))
print("is_unique:", s.index.is_unique)
print()
print("s['b'] ->", s["b"], " (a scalar)")
print("s['a'] ->")
print(s["a"], "   <- a Series, not a scalar")
print()
print("Code that assumes a scalar breaks only when a duplicate appears,")
print("which is usually in production rather than in the test data.")
print()
print("verify_integrity=True refuses to build a duplicated index:")
try:
    pd.DataFrame({"k": ["x", "x"], "v": [1, 2]}).set_index("k", verify_integrity=True)
except ValueError as e:
    print("   ", str(e)[:60])'''),

        ("When a label range needs a sorted index",
         "Not as often as people say - it is uniqueness that decides it.",
         '''import pandas as pd

uniq = pd.Series(range(5), index=[30, 10, 40, 20, 50])
print("unique but unsorted:", list(uniq.index))
print("   sorted?", uniq.index.is_monotonic_increasing,
      "  unique?", uniq.index.is_unique)
print("   uniq.loc[10:40] ->", list(uniq.loc[10:40]), "<- works fine")
print()
print("It slices by POSITION of the two bounds, so the order you get")
print("is the order the index is in, not numeric order.")
print()
dup = pd.Series(range(5), index=[3, 1, 4, 1, 5])
print("non-unique AND unsorted:", list(dup.index))
try:
    dup.loc[1:4]
except Exception as e:
    print("   dup.loc[1:4] ->", type(e).__name__)
    print("   ", str(e)[:64])
print()
print("sort_index() fixes it:", list(dup.sort_index().loc[1:4]))'''),
    ],
    [
        "Both axes are <code>Index</code> objects &mdash; the rows and the columns. Anything true of one is true of the other.",
        "The index <strong>survives filtering</strong>, so a filtered result is no longer numbered <code>0..n-1</code>.",
        "<code>set_index</code> promotes a column to the index; <code>reset_index</code> turns it back into a column, and <code>drop=True</code> discards it.",
        "Combining two objects <strong>aligns on labels first</strong>. Unmatched labels become NaN &mdash; use <code>add(other, fill_value=0)</code> to treat them as zero.",
        "Labels may be <strong>duplicated</strong>, and a lookup then returns a Series rather than a scalar.",
        "Slicing by a label <em>range</em> works on any <strong>unique</strong> index, sorted or not &mdash; it is a <em>non-unique</em> unsorted index that raises.",
    ],
    '''
title: The Index
intro: The labelled axis that participates in almost every operation.

## What it is

Every Series and every DataFrame carries an index: an ordered set of labels, one per row. A DataFrame also has an index for its columns.

If you do not supply one, pandas creates a `RangeIndex` of `0, 1, 2, ...`. That default is why the index is easy to overlook &mdash; it looks like row numbers, and for a freshly created frame it behaves like them.

It is not row numbers. It is a labelled axis that takes part in selection, alignment, joining, grouping and reshaping. Nearly every pandas behaviour that surprises people is the index doing something they did not ask for.

## Labels stick to rows

Filter a Series of five values down to three and the surviving rows keep their original labels. The result's index might be `1, 3, 4`.

This is correct &mdash; the label identifies the row, and the row did not change identity by being selected &mdash; but it breaks positional habits immediately.

`big[0]` raises `KeyError`, because there is no label `0` any more. `big.iloc[0]` gets the first row by position. `big.loc[1]` gets the row labelled 1.

Two consequences worth internalising.

**After filtering, use `iloc` for position and `loc` for labels**, and know which you mean. The next module is entirely about that distinction.

**`reset_index(drop=True)` renumbers** when you genuinely want a fresh `0..n-1`. Without `drop=True`, the old index is kept as a new column, which is occasionally what you want and usually not.

## set_index and reset_index

`df.set_index("city")` makes the `city` column the index. Lookups by city then work with `.loc`, joins on city become index joins, and grouping by it is cheaper.

`df.reset_index()` reverses it, putting the index back as an ordinary column and restoring a `RangeIndex`.

Setting a meaningful index is worth doing when you will look rows up by that key repeatedly. It is not worth doing reflexively &mdash; an index carries rules, and a frame with a `RangeIndex` is simpler to reason about.

## Alignment

This is the behaviour that most distinguishes pandas from NumPy, and it is silent.

When two Series are combined, pandas matches them **by label** before doing anything. Order does not matter. A label present in one and absent from the other produces `NaN` rather than an error.

For addition of two quarterly figures indexed by city, that is exactly right: you want Pune added to Pune, whatever order the rows arrived in, and a city missing from one quarter should be visibly missing rather than silently paired with the wrong row.

It becomes a problem when you did not realise the indexes differed. A common version: you filter a frame, compute a column from it, and assign that column back to the original frame. Alignment matches on the filtered labels, so the rows you filtered out get `NaN` &mdash; which is arguably the right answer, and is rarely what the author expected.

`.values` or `.to_numpy()` strips the index and forces positional behaviour. That is occasionally the right escape hatch, and it silences the safety feature, so it deserves a comment when used.

The arithmetic methods take `fill_value`: `q1.add(q2, fill_value=0)` treats a missing label as zero rather than propagating NaN.

## Duplicates

An index may contain the same label more than once. pandas does not prevent it.

The consequence is that `s["a"]` returns a **scalar** when `a` appears once and a **Series** when it appears twice. Downstream code written against the scalar case fails when a duplicate appears, and duplicates usually appear in production rather than in the sample used for development.

`s.index.is_unique` checks. `set_index(..., verify_integrity=True)` refuses to build a duplicated index, which is worth passing when uniqueness is part of what the data means.

`df.index.duplicated()` gives a mask of the repeats, so you can inspect them rather than guess.

## Sorted indexes

`is_monotonic_increasing` tells you whether the index is sorted.

A sorted index allows binary-search lookups, which matters on large frames.

It is often said that label-range slicing *requires* a sorted index. That is not quite the rule, and the editor above shows it: a **unique** index slices fine whatever order it is in, because pandas can find each bound unambiguously and take everything between them. What it cannot do is slice a **non-unique, unsorted** index &mdash; there is no single position for a repeated bound, so it raises rather than guessing.

Worth knowing what that slice returns on an unsorted index: everything between the two bounds *in the index's own order*, which is not numeric order. That is rarely what people intend, so `sort_index()` first is still good practice even where it is not required.

Note that label slicing with `.loc` is **inclusive of the endpoint**, unlike every other slice in Python. `s.loc[100:200]` includes 200. That is deliberate &mdash; with labels there is no "one past the end" to point at &mdash; and it is a reliable source of off-by-one surprises.

`sort_index()` sorts by the index; `sort_values()` sorts by the data. Both return new objects by default.

## The habits worth forming

Look at the index when a result surprises you. It is the first thing to check, ahead of the values.

Call `reset_index(drop=True)` after filtering when downstream code will think positionally.

Prefer `.loc` and `.iloc` over bare `[]`, so that "label" or "position" is written down rather than inferred.

Use `fill_value` when combining objects whose labels may not match exactly.

And check `is_unique` before relying on a lookup returning one row.

## Kinds of index

The default is a `RangeIndex` &mdash; a compact `0, 1, 2, ...` that stores only start, stop and step rather than the values.

`Index` holds arbitrary labels: strings, integers, anything hashable.

`DatetimeIndex` holds timestamps and unlocks partial string selection (`s["2024-02"]`) and `resample`.

`CategoricalIndex` holds a fixed set of categories, and is memory-efficient for a repeated key.

`MultiIndex` holds several levels, and is what a group-by on more than one key returns.

You rarely choose between these deliberately. They arrive from whatever produced the object, and knowing which you have explains what operations are available.

## The index is not free

`RangeIndex` costs almost nothing. Any other index stores one label per row, and a string index over a million rows is a million Python strings &mdash; often larger than the numeric columns it labels.

`df.index.dtype` and `df.memory_usage(deep=True)` show it. `reset_index(drop=True)` discards it and returns to a `RangeIndex`, which is worth doing when the labels carry no meaning.

That is the practical argument for not setting a meaningful index reflexively: it costs memory, and it only pays if you actually select or join on it.

## Selecting with an index that is not unique

`is_unique` is worth checking before relying on lookups, because the return type of `s[label]` depends on it.

With a unique index, `s["a"]` is a scalar. With a duplicated one it is a Series. Code written against the first case &mdash; arithmetic, a comparison, passing the value to a function &mdash; breaks on the second, and the break happens wherever the value is used rather than at the lookup.

`df.index.duplicated()` gives a mask of the repeats, and `df[df.index.duplicated(keep=False)]` shows every conflicting group.

`verify_integrity=True` on `set_index` refuses to build a duplicated index, and is worth passing whenever uniqueness is part of what the data means.

## Aligning on purpose

Alignment is usually helpful and occasionally in the way. Three ways to control it:

**Match the indexes** &mdash; `reindex(other.index)` conforms one object to another's labels, filling missing ones with `NaN`. This is alignment made explicit rather than implicit.

**Drop the index** &mdash; `.values` or `.to_numpy()` gives a plain array with no labels, so operations become positional. Use it when you know the order is right and the labels are noise, and comment why.

**Reset both** &mdash; `reset_index(drop=True)` on both sides before combining, when they should correspond row-for-row.

The failure this prevents is the one from the previous module: two objects that *should* line up, whose indexes have drifted apart because one was filtered, silently producing `NaN` or a much longer result.

## Index methods worth knowing

An Index behaves like an immutable set, and the set operations are occasionally exactly what you need:

`a.index.difference(b.index)` &mdash; labels in one and not the other. The fastest way to find out which rows a join would drop.

`a.index.intersection(b.index)` &mdash; the common labels.

`idx.get_loc(label)` &mdash; the position of a label, for when you genuinely need to cross from labels to positions.

`idx.str` &mdash; the string accessor works on an Index too, which is how you clean column names in one expression.

Indexes are immutable. You cannot assign into one; you build a new one and attach it. That is deliberate, because a mutable index would break the hash-based lookups that make label selection fast.

## When to set a meaningful index

**Set one** when you will look rows up by that key repeatedly, join on it more than once, or need time-based selection and `resample`.

**Do not set one** when the key is not unique, when you only need it once, or when the result is heading to a file or a merge that expects columns.

`reset_index()` is cheap and always available, so the decision is not permanent &mdash; which is a good reason not to agonise over it.

## Common index mistakes

**Assuming a filtered frame is renumbered.** It is not; `reset_index(drop=True)` renumbers.

**Using `[0]` after a filter.** There may be no label 0. `.iloc[0]` is the position.

**Forgetting `drop=True`.** `reset_index()` keeps the old index as a new column, which then travels through every later operation as an unwanted `index` column.

**Setting an index and then merging on the column.** After `set_index("id")`, there is no `id` column to merge on &mdash; use `left_index=True`, or reset first.

**Assuming alignment is positional.** It is by label. Two Series with the same values in different label orders add to something neither of them looks like.

**Ignoring duplicates.** A lookup that returns a Series instead of a scalar breaks downstream code, and the break happens away from the lookup.

## Reindexing

`reindex` conforms an object to a given set of labels: present labels are kept, absent ones are filled with `NaN`, and labels not in the new set are dropped.

That makes it the tool for two jobs.

**Making frames comparable.** `b.reindex(a.index)` puts `b` on `a`'s labels, so a subsequent operation aligns exactly and any mismatch is visible as `NaN` rather than silently reordering.

**Filling out a sparse axis.** Reindexing onto a complete date range turns missing days into explicit `NaN` rows, which is what you want before plotting or before a rolling window over rows.

`fill_value=` sets what the gaps become, and `method="ffill"` carries values forward, which requires a sorted index.

`reindex_like(other)` is the shorthand for the first case.

## The index in output

The index is written by `to_csv` unless you pass `index=False`, and read back as an unnamed column unless you pass `index_col=0`. That round-trip mismatch is the origin of the `Unnamed: 0` column that appears in so many datasets.

`to_dict()`, `to_json()` and `to_excel` all have their own opinions about the index, and all of them are worth checking once for any output that another system consumes.

The rule that avoids most of it: if the index is meaningful data, name it and write it deliberately. If it is not, `reset_index(drop=True)` before writing.

## A working summary

The index is a labelled axis, not row numbers.

It survives filtering, and alignment uses it silently.

`set_index` when you will select or join on the key repeatedly; `reset_index(drop=True)` when you will not.

Check `is_unique` before relying on lookups.

`sort_index()` after building or reshaping anything with a non-trivial index.

And when a result has the wrong number of rows or unexpected `NaN`, look at the indexes of the inputs first. That is the cause more often than anything in the operation itself.
''',
    [
        {"q": "After filtering a Series down to 3 of 5 rows, what is `result[0]` likely to do?",
         "options": ["Return the first row", "Raise KeyError, because label 0 may no longer exist", "Return NaN", "Return all rows"],
         "answer": 1,
         "why": "The surviving rows keep their original labels. Use .iloc[0] for position, or reset_index(drop=True) to renumber."},
        {"q": "Two Series with partly overlapping labels are added. What happens to a label present in only one?",
         "options": ["It is dropped", "It becomes NaN", "It raises", "It is treated as zero"],
         "answer": 1,
         "why": "Alignment is a safety feature - a mismatch surfaces as NaN rather than a silent off-by-one. Use add(other, fill_value=0) to treat it as zero."},
        {"q": "What does `s['a']` return when the label 'a' appears twice in the index?",
         "options": ["The first match", "A Series containing both", "An error", "The last match"],
         "answer": 1,
         "why": "The return type changes with the data, so code written against the scalar case breaks when a duplicate appears - usually in production."},
        {"q": "What does `s.loc[100:200]` include?",
         "options": ["Up to but not including 200", "Both endpoints, including 200", "Only 100", "Positions 100 to 200"],
         "answer": 1,
         "why": "Label slicing is inclusive of the endpoint, unlike every other Python slice. It works on any unique index; only a non-unique unsorted one raises."},
    ],
)


# ---------------------------------------------------------------------------
# 3. Creating DataFrames
# ---------------------------------------------------------------------------
topic(
    "creating_dataframes",
    "Creating DataFrames",
    "Series and Index",
    "From dicts, records, arrays and files - and which orientation each one "
    "assumes.",
    _svg(_txt(30, 24, "dict", M, 8) + _txt(30, 40, "rows", M, 8) +
         _txt(30, 56, "csv", M, 8) +
         _arrow(56, 44, 76, 44) +
         _box(84, 24, 60, 44, S, A) + _txt(114, 50, "DataFrame", A, 8)),
    [
        ("From a dict of columns",
         "The most common form. Each key is a column name, each value the whole "
         "column.",
         '''import pandas as pd

df = pd.DataFrame({
    "item": ["pen", "book", "bag"],
    "qty": [3, 1, 2],
    "price": [10.0, 250.0, 400.0],
})
print(df)
print()
print("the keys became columns:", list(df.columns))
print("lengths must match, or it raises:")
try:
    pd.DataFrame({"a": [1, 2], "b": [1, 2, 3]})
except ValueError as e:
    print("   ", str(e)[:56])
print()
print("a scalar is broadcast to every row, though:")
print(pd.DataFrame({"a": [1, 2, 3], "flag": True}))'''),

        ("From a list of records",
         "One dict per row - the shape data usually arrives in from an API.",
         '''import pandas as pd

rows = [
    {"item": "pen", "qty": 3},
    {"item": "book", "qty": 1},
    {"item": "bag", "qty": 2, "gift": True},
]
df = pd.DataFrame(rows)
print(df)
print()
print("missing keys become NaN rather than an error:")
print(df.dtypes)
print()
print("Note 'gift' became object, because NaN is a float and True is a bool.")
print("Column order follows first appearance across all the records.")'''),

        ("From a list of lists, and why columns= matters",
         "Without names you get integer columns, which is rarely what you want.",
         '''import pandas as pd

data = [["pen", 3], ["book", 1], ["bag", 2]]

print("no names:")
print(pd.DataFrame(data))
print("   columns are", list(pd.DataFrame(data).columns), "<- integers")
print()
print("with names:")
df = pd.DataFrame(data, columns=["item", "qty"])
print(df)
print()
print("an index can be supplied at the same time:")
print(pd.DataFrame(data, columns=["item", "qty"], index=["a", "b", "c"]))'''),

        ("Reading a CSV from text",
         "read_csv is the usual entry point, and it takes any file-like object.",
         '''import pandas as pd
import io

csv = """item,qty,price
pen,3,10.0
book,1,250.0
bag,2,400.0
"""
df = pd.read_csv(io.StringIO(csv))
print(df)
print()
print("types are inferred per column:")
print(df.dtypes)
print()
print("and you can steer it:")
df2 = pd.read_csv(io.StringIO(csv), index_col="item", dtype={"qty": "int8"})
print(df2)
print("qty dtype:", df2["qty"].dtype)'''),

        ("From a Series, and the orientation trap",
         "A dict of scalars gives one row only if you tell it so.",
         '''import pandas as pd

d = {"a": 1, "b": 2, "c": 3}

print("as a Series (the values are rows):")
print(pd.Series(d))
print()
print("pd.DataFrame(d) raises - scalars have no length:")
try:
    pd.DataFrame(d)
except ValueError as e:
    print("   ", str(e)[:52])
print()
print("wrap it in a list to mean 'one row':")
print(pd.DataFrame([d]))
print()
print("or use from_dict with orient='index' to mean 'one column':")
print(pd.DataFrame.from_dict(d, orient="index", columns=["value"]))'''),

        ("Building rows in a loop is the slow way",
         "The same lesson as NumPy: collect, then construct once.",
         '''import pandas as pd
import time

n = 2000

t = time.perf_counter()
acc = pd.DataFrame(columns=["i", "sq"])
for i in range(300):
    acc.loc[len(acc)] = [i, i * i]
grow = time.perf_counter() - t

t = time.perf_counter()
rows = [{"i": i, "sq": i * i} for i in range(300)]
once = pd.DataFrame(rows)
fast = time.perf_counter() - t

print("appending row by row : %.4f s" % grow)
print("build list, then once: %.4f s" % fast)
print("ratio                : %.0fx" % (grow / max(fast, 1e-9)))
print()
print("Each .loc assignment reallocates the whole frame.")
print("df.append() used to be the popular way - it was removed in pandas 2.0.")'''),
    ],
    [
        "A <strong>dict of columns</strong> is the usual form: keys become column names, values become whole columns, and a scalar is broadcast.",
        "A <strong>list of dicts</strong> is one record per row &mdash; missing keys become NaN rather than raising.",
        "A list of lists gives <strong>integer column names</strong> unless you pass <code>columns=</code>.",
        '<code>pd.DataFrame(dict_of_scalars)</code> raises. Wrap it in a list for one row, or use <code>from_dict(orient="index")</code> for one column.',
        "<code>read_csv</code> infers a dtype per column, and takes <code>dtype=</code>, <code>index_col=</code> and <code>usecols=</code> to steer it.",
        "Never build a frame row by row &mdash; each assignment reallocates it. Collect into a list and construct once.",
    ],
    '''
title: Creating DataFrames
intro: From dicts, records, arrays and files, and which orientation each assumes.

## The two orientations

Almost every confusion about constructing a DataFrame comes from one question: does this input describe **columns** or **rows**?

`pd.DataFrame({"a": [1,2,3], "b": [4,5,6]})` describes columns. Each key is a column name and each value is the entire column. This is the most common form and the one to reach for when you have parallel lists.

`pd.DataFrame([{"a":1,"b":4}, {"a":2,"b":5}])` describes rows. Each dict is one record. This is the shape data arrives in from an API or a database cursor, and pandas handles it directly.

Both produce the same frame. Knowing which one you are writing prevents a transposed result.

## What each form tolerates

**Dict of columns** requires equal lengths and raises otherwise, which is a useful check. A **scalar** value is the exception: it broadcasts to every row, so `{"a": [1,2,3], "flag": True}` gives a flag column of three `True` values.

**List of dicts** does not require the keys to match. Missing keys become `NaN`, and the column order follows first appearance across all records. That tolerance is convenient for messy input and worth watching: a typo in one record's key silently creates a new mostly-empty column rather than raising.

**List of lists** works but names the columns `0, 1, 2`. Pass `columns=` unless you genuinely want integer names. Integer column names are legal and lead to real confusion later, because `df[0]` then means a column and looks like positional indexing.

**Dict of scalars** raises, because pandas cannot tell whether you meant one row or one column. `pd.DataFrame([d])` means one row; `pd.DataFrame.from_dict(d, orient="index")` means one column. The error is good &mdash; guessing here would be worse.

## read_csv

For real data this is the usual entry point, and it does a lot by default: infers a dtype per column, treats the first line as a header, and parses common missing-value markers.

The arguments worth knowing early:

`index_col` sets a column as the index during the read rather than afterwards.

`usecols` reads only the columns you name, which matters on wide files &mdash; it saves both time and memory.

`dtype` overrides inference. This is how you stop an identifier column being read as an integer and losing its leading zeros, and how you read a low-cardinality column straight into `category`.

`parse_dates` converts date columns during the read, which is faster than converting afterwards.

`nrows` reads a sample, which is the right way to inspect a large file before committing to it.

It accepts any file-like object, so `io.StringIO` works for testing and for data that is already in memory.

## Type inference and its costs

`read_csv` and the constructors infer types per column. That is usually helpful and occasionally wrong in expensive ways.

A column of integers with one missing value becomes `float64`, because integer arrays cannot hold NaN. Identifiers then print as `1001.0`.

A column that is mostly numbers with one stray non-numeric value becomes `object`, and every subsequent numeric operation on it either fails or silently operates on strings.

Both are worth checking with `df.dtypes` immediately after loading. It takes one line and catches a category of bug that otherwise surfaces much later.

## Never grow a frame

`acc.loc[len(acc)] = row` inside a loop reallocates the entire frame on every iteration. So did `df.append`, which is why it was **removed in pandas 2.0** rather than merely deprecated.

The correct pattern is the same as NumPy's: collect into a Python list and construct once at the end. Lists append cheaply; DataFrames do not append at all.

If the pieces are already frames, `pd.concat(list_of_frames)` once at the end is the right call &mdash; and `pd.concat` inside a loop is exactly the same mistake in a different costume.

The last editor measures it. The gap grows with the number of rows, so a pattern that seems acceptable on a hundred records becomes unusable on a hundred thousand.

## Choosing

**Parallel lists you already have**: dict of columns.

**Records from an API or a cursor**: list of dicts.

**A file**: `read_csv`, with `dtype` and `usecols` set deliberately.

**A NumPy array**: `pd.DataFrame(arr, columns=[...])`, remembering that the array's single dtype applies to every column until you convert.

**One row from a dict**: `pd.DataFrame([d])`.

And in every case, print `df.dtypes` and `df.shape` immediately afterwards. Those two lines catch most of what goes wrong at the boundary between raw data and pandas.

## From a NumPy array

`pd.DataFrame(arr, columns=[...])` wraps an array. The array has **one** dtype, so every column starts with that dtype until you convert.

That matters when the array came from something that widened it. An array of mixed data is `object`, and a DataFrame built from it has every column as `object` &mdash; numeric-looking columns that do not behave numerically.

`index=` sets the labels at the same time.

For the reverse direction, `df.to_numpy()` collapses back to a single dtype, and `df.values` is the older spelling of the same thing.

## From a database or an API

`pd.read_sql(query, connection)` runs a query and returns a frame, with column names taken from the result. It accepts a SQLAlchemy connection or a raw DBAPI one.

`pd.read_json` handles JSON, and `pd.json_normalize` is the one worth knowing: it flattens **nested** JSON into columns, turning `{"user": {"name": "ana"}}` into a `user.name` column. Most API responses need it, and building the frame by hand from nested dicts is the long way round.

`pd.read_html(url_or_html)` scrapes every table on a page into a list of frames. It is startlingly effective for simple pages and needs `lxml` or `bs4` installed.

## Setting the index at creation

Any of the constructors accept `index=`, and `read_csv` accepts `index_col=`.

Doing it at creation is slightly cheaper than `set_index` afterwards, and more importantly it documents that the column is a key rather than data.

If the index should be a `DatetimeIndex`, parse the dates in the same call: `read_csv(path, parse_dates=["date"], index_col="date")` gives a time-indexed frame in one step.

## Empty frames, and why they cause trouble

`pd.DataFrame()` is legal and occasionally useful as a placeholder.

It is a poor starting point for accumulation, for two reasons. Growing it row by row is quadratic, as the last editor shows. And its columns have no meaningful dtype, so the first `concat` into it can widen everything to `object` &mdash; at which point the frame is slow and the numeric columns are no longer numeric.

`pd.DataFrame(columns=["a", "b"])` has the same problem with more ceremony.

The pattern to use instead is always the same: build a **list** of rows or of frames, and construct once at the end.

## Checking what you built

Four lines, immediately after construction, catch most problems at the boundary:

```python
df.shape        # is this the number of rows I expected?
df.dtypes       # did anything become object or float unexpectedly?
df.head()       # does the data look like the data?
df.isna().sum() # where are the gaps?
```

The second is the one that earns its keep. Type inference is where most silent damage happens, and it happens exactly once, at construction.

## Choosing a constructor

**Parallel lists you already have** &mdash; a dict of columns.

**Records from an API or a cursor** &mdash; a list of dicts, or `json_normalize` if they are nested.

**A file** &mdash; `read_csv`, with `dtype`, `usecols` and `parse_dates` set deliberately.

**A query** &mdash; `read_sql`, which names the columns for you.

**A NumPy array** &mdash; the constructor with `columns=`, remembering the single dtype.

**One row from a dict** &mdash; `pd.DataFrame([d])`.

**Accumulated pieces** &mdash; a list, then `pd.DataFrame(rows)` or `pd.concat(frames)` once.

In every branch, set the dtype at creation rather than converting afterwards. `astype` allocates a second full frame, and getting it right the first time avoids both the copy and the class of bugs where a column silently is not the type you assumed.

## Reproducible test frames

Small frames written by hand are how you check that an operation does what you think, and it is worth having a habit for them.

A dict of columns is the most readable form for a handful of rows. `pd.DataFrame({"a": [1,2,3], "b": list("xyz")})` fits on one line and shows the columns clearly.

For a frame with a specific index, pass `index=` rather than setting it afterwards.

For random test data, seed it: `np.random.default_rng(0)`. Unseeded random test data makes a failing check unreproducible, which is the opposite of what a test is for.

`pd.util.testing` used to provide frame generators; the supported route now is `pd.testing.assert_frame_equal` for comparisons, and building the frames yourself.

## Checking two frames match

`pd.testing.assert_frame_equal(a, b)` is the precise comparison: values, dtypes, index and column order all have to agree, and the error message says which differed.

`check_dtype=False` relaxes the type comparison, which is often necessary when one side came through a CSV.

`check_like=True` ignores row and column order.

This is what belongs in a test, rather than `a.equals(b)`, because when it fails it tells you *what* failed.

## Copy semantics at construction

`pd.DataFrame(some_array)` does **not** always copy. If the array's dtype and layout are usable directly, pandas may wrap it, and writing to the frame then writes to the array.

`copy=True` forces a copy. Under copy-on-write this stops mattering, which is another reason that change is welcome.

`pd.DataFrame(dict_of_series)` aligns the Series on their indexes, which is easy to forget: three Series with different labels produce a frame with the union of them and `NaN` in the gaps, not three columns side by side.

If you meant "these are parallel columns", reset the indexes first or pass plain lists.

## The construction checklist

Decide whether the input describes rows or columns.

Pass `columns=` if the source has no names.

Set `dtype` at construction, especially for identifiers and for integers that may have gaps.

Set `index=` if a column is really a key.

Then check `shape`, `dtypes`, `head()` and `isna().sum()`.

Never grow a frame in a loop.

That is six lines of discipline that prevent most of what the cleaning modules exist to repair.

## A closing note

Construction is where a frame's types are decided, and types decided badly here cause problems everywhere afterwards.

The two questions worth answering deliberately are whether the input describes rows or columns, and what the dtypes should be. Getting the first wrong gives a transposed frame that is immediately obvious. Getting the second wrong gives a frame that looks correct and behaves oddly much later.

`dtype=` at construction costs nothing. `astype` afterwards allocates a second copy of every column it touches, and by then the leading zeros may already be gone.

The other rule is the one shared with NumPy: never grow a frame in a loop. Collect into a list and construct once. `df.loc[len(df)] = row` and `pd.concat` inside a loop are the same quadratic mistake wearing different syntax, and `df.append` was removed rather than merely deprecated because of it.

## One more thing

`pd.DataFrame.from_records` handles an iterable of tuples with a `columns` argument, and accepts an `index` naming one of the fields. It is the constructor that fits a database cursor most directly, since cursors yield tuples rather than dicts.

And `pd.concat` of many small frames is usually faster than building one large list of dicts when the pieces are already frames &mdash; the rule is to avoid the loop, not to prefer one container over the other.

## In summary

Decide whether the input describes rows or columns, set the dtypes at construction, and check `shape`, `dtypes` and `head` immediately afterwards.

Never grow a frame in a loop &mdash; collect into a list and build once. `df.append` was removed rather than deprecated because of exactly that pattern.
''',
    [
        {"q": "What does `pd.DataFrame({'a': [1,2,3], 'flag': True})` produce?",
         "options": ["An error", "Three rows, with flag broadcast to True on each", "One row", "A flag column of NaN"],
         "answer": 1,
         "why": "A scalar value is broadcast to every row, while list values must all have matching lengths."},
        {"q": "Why does `pd.DataFrame({'a': 1, 'b': 2})` raise?",
         "options": ["Dicts are not supported", "pandas cannot tell whether you meant one row or one column", "The keys are too short", "It needs an index"],
         "answer": 1,
         "why": "Wrap it in a list for one row, or use from_dict(orient='index') for one column. Guessing would be worse than the error."},
        {"q": "A CSV column of integers has one missing value. What dtype does it get?",
         "options": ["int64", "float64, because integers cannot hold NaN", "object", "category"],
         "answer": 1,
         "why": "This is why identifiers sometimes print as 1001.0. Check df.dtypes right after loading - it takes one line and catches the bug early."},
        {"q": "What happened to `df.append()`?",
         "options": ["It is still the recommended way", "It was removed in pandas 2.0, because it reallocated the whole frame each call", "It was renamed", "It only works on Series"],
         "answer": 1,
         "why": "Collect rows into a Python list and construct once. pd.concat inside a loop is the same mistake in different clothing."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Looking at data
# ---------------------------------------------------------------------------
topic(
    "inspecting_data",
    "Looking at Data",
    "Series and Index",
    "The six calls to make before writing any analysis, and what each one is "
    "actually telling you.",
    _svg(_box(18, 24, 124, 12, S, A) + _txt(80, 33, "shape / dtypes", A, 8) +
         _box(18, 40, 124, 12, S) + _txt(80, 49, "head / info", M, 8) +
         _box(18, 56, 124, 12, S) + _txt(80, 65, "describe / isna", M, 8)),
    [
        ("shape and dtypes first",
         "Two lines that catch most of what goes wrong at the boundary.",
         '''import pandas as pd
import io

csv = """id,name,age,joined
001,ana,31,2021-04-05
002,raj,,2022-01-10
003,kim,40,2020-11-30
"""
df = pd.read_csv(io.StringIO(csv))

print("shape :", df.shape, "(rows, columns)")
print()
print(df.dtypes)
print()
print("Three things to notice, none of which raised:")
print("  id     -> int64, so the leading zeros are gone")
print("  age    -> float64, because one value is missing")
print("  joined -> object, because dates are not parsed by default")'''),

        ("head, tail and sample",
         "Look at the data. The first rows are often not representative.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "day": range(1, 21),
    "sales": list(range(10, 30)),
})
print("head(3):"); print(df.head(3))
print()
print("tail(3):"); print(df.tail(3))
print()
print("sample is the one that shows you the middle:")
print(df.sample(3, random_state=0))
print()
print("head alone hides sorted data, dated data and anything that")
print("changes partway through the file.")'''),

        ("info gives dtypes, nulls and memory together",
         "The single most useful call on an unfamiliar frame.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "a": [1, 2, 3, 4],
    "b": [1.5, np.nan, 3.5, np.nan],
    "c": ["x", "y", "x", None],
})
df.info()
print()
print("Read the Non-Null Count column against the row count:")
print("  b has 2 of 4, c has 3 of 4.")'''),

        ("describe, and what it leaves out",
         "Numeric columns only, unless you ask otherwise.",
         '''import pandas as pd

df = pd.DataFrame({
    "score": [10, 20, 30, 40, 1000],
    "grade": ["a", "b", "a", "c", "a"],
})
print(df.describe())
print()
print("the text column is missing. include='all' brings it in:")
print(df.describe(include="all"))
print()
print("Note the mean of score is 220 - one outlier moved it past every")
print("value but one. Compare mean with the 50% row to spot that.")'''),

        ("Counting missing values",
         "Per column, as a proportion, and which rows are affected.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "a": [1, np.nan, 3, np.nan],
    "b": [1, 2, 3, 4],
    "c": [np.nan, np.nan, np.nan, 4.0],
})
print("missing per column:")
print(df.isna().sum())
print()
print("as a share of rows:")
print((df.isna().mean() * 100).round(1))
print()
print("rows with any missing value:", int(df.isna().any(axis=1).sum()), "of", len(df))
print("rows that are complete     :", int(df.notna().all(axis=1).sum()))'''),

        ("value_counts for the categorical columns",
         "The fastest way to find typos, stray categories and unexpected cardinality.",
         '''import pandas as pd

s = pd.Series(["pune", "delhi", "pune", "Pune", "delhi", "pune ", None])

print(s.value_counts())
print()
print("four spellings of two cities - trailing space and a capital.")
print()
print("dropna=False shows the missing values too:")
print(s.value_counts(dropna=False))
print()
print("normalize gives shares:")
print((s.value_counts(normalize=True) * 100).round(1))
print()
print("nunique:", s.nunique(), " (excludes NaN by default)")'''),
    ],
    [
        "<code>df.shape</code> and <code>df.dtypes</code> are the first two lines to run &mdash; they catch lost leading zeros, unparsed dates and columns turned float by one missing value.",
        "<code>head</code> hides sorted or dated data. <code>sample</code> shows you the middle.",
        "<code>df.info()</code> gives dtypes, non-null counts and memory in one call &mdash; the most useful thing to run on an unfamiliar frame.",
        "<code>describe</code> covers numeric columns only unless you pass <code>include=\"all\"</code>. A mean far from the median means outliers.",
        "<code>df.isna().sum()</code> counts missing per column; <code>.mean()</code> gives the share.",
        "<code>value_counts</code> on text columns finds typos, stray capitals and trailing spaces before they become a broken group-by.",
    ],
    '''
title: Looking at Data
intro: The six calls to make before writing any analysis.

## Why this comes before anything else

Most pandas bugs are not bugs in pandas. They are assumptions about the data that were never checked: a column that is text where you expected numbers, an identifier that lost its leading zeros, a category with four spellings, a date column that is still strings.

None of these raise. They produce plausible output that is wrong, and the error surfaces much later, somewhere unrelated.

Six calls catch nearly all of it, and together they take under a minute.

## shape and dtypes

`df.shape` gives `(rows, columns)`. It confirms the file loaded as expected, and catches the case where a delimiter was misread and everything landed in one column.

`df.dtypes` is the important one. Three failures show up here and nowhere else:

**An identifier read as an integer.** `001` becomes `1`, and the leading zeros are gone permanently. Fix at read time with `dtype={"id": str}`.

**An integer column turned float** because one value is missing. NumPy integers cannot hold NaN, so pandas promotes. The symptom downstream is ids printing as `1001.0`.

**A numeric column read as `object`** because one row contains a stray non-numeric value. Every later numeric operation then either fails or silently operates on strings.

Running these two lines immediately after loading is the highest-value habit in this module.

## head, tail, sample

Look at the data. Not the summary &mdash; the actual rows.

`head()` shows the first five. That is fine for a random file and misleading for a sorted one, a dated one, or one where the format changes partway through.

`tail()` catches trailing junk: summary rows, blank lines, a footer the exporter added.

`sample(n, random_state=0)` shows the middle, which is where the surprises usually live. Passing `random_state` makes it reproducible, which matters if you are going to discuss what you saw.

## info

`df.info()` prints dtypes, non-null counts and memory usage together.

The non-null count is the part to read carefully. Compare it against the row count for each column: a column with 400 non-null out of 10,000 rows is effectively empty and any analysis using it is built on 4% of the data.

`memory_usage="deep"` gives the true cost of object columns, which the default underestimates badly because it counts the pointers rather than the strings they point at.

## describe

`df.describe()` gives count, mean, standard deviation, min, max and quartiles for **numeric columns only**.

`include="all"` adds text columns, reporting count, unique, top and frequency for them instead.

The most useful reading of it is the **mean against the median** (the 50% row). When they are far apart, the distribution is skewed or contains outliers, and every mean-based summary you were about to compute will mislead. A `mean` of 220 with a `50%` of 30 is telling you something important before you have written any analysis.

`min` and `max` are also worth a glance for impossible values: a negative age, a date in 1900, a price of zero.

## Missing values

`df.isna().sum()` counts them per column. `df.isna().mean()` gives the proportion, which is easier to judge than a raw count.

`df.isna().any(axis=1).sum()` counts rows affected by any missing value &mdash; the number you would lose to `dropna()`, and often much larger than any single column's count.

Doing this before deciding how to handle missing data means the decision is informed rather than reflexive. Dropping 2% of rows is different from dropping 60%.

## value_counts

For every text or categorical column, run `value_counts()`.

It finds, in one line: typos, inconsistent capitalisation, trailing whitespace, unexpected categories, and cardinality far higher than expected (often a sign the column is really an identifier).

The last editor shows two cities appearing as four values &mdash; `pune`, `Pune`, and `pune ` with a trailing space. A group-by on that column would produce four groups, and nothing would warn you.

`dropna=False` includes missing values in the count, which is otherwise invisible here.

`normalize=True` gives shares rather than counts, which is the right form when comparing distributions between datasets.

## A starting routine

```python
df.shape
df.dtypes
df.head()
df.sample(5, random_state=0)
df.info()
df.describe(include="all")
df.isna().mean()
```

Then `value_counts()` on each text column.

It is not glamorous and it is not optional. Every one of these calls has a specific failure it catches, and the alternative is finding that failure later, in a result you have already shown someone.

## Making the display readable

Default display settings hide things, and hidden data is data you will not check.

`pd.set_option("display.max_columns", None)` stops columns being elided into `...`, which is the single most useful setting on a wide frame.

`pd.set_option("display.width", 200)` controls wrapping.

`pd.set_option("display.max_rows", 100)` shows more before truncating.

`pd.set_option("display.float_format", "{:.2f}".format)` stops fifteen decimal places dominating every table.

These affect display only, never the data. In a notebook they are worth putting in the first cell.

## Reading info carefully

`df.info()` packs four things into one output, and each deserves a look.

**The row count** in the header, against what you expected from the source.

**Non-Null Count** per column, against that row count. This is the fastest way to find a column that is mostly empty.

**Dtype** per column. `object` on something that should be numeric is a problem; `float64` on something that should be integer usually means a missing value.

**Memory usage**, which needs `memory_usage="deep"` to be truthful about text columns.

A column with, say, 400 non-null out of 200,000 rows is effectively empty. Any analysis using it is built on 0.2% of the data, and it is better to know that before building the analysis than after presenting it.

## describe, beyond the defaults

`percentiles=[0.01, 0.5, 0.99]` changes which quantiles are shown. The 1st and 99th are often more informative than the quartiles for spotting outliers.

`include="all"` adds non-numeric columns, reporting `count`, `unique`, `top` and `freq` for them.

`include=["object"]` or `exclude=["number"]` restrict it.

`df.describe().T` transposes the result, which is much easier to read when there are many columns &mdash; one row per column instead of one column per column.

Three readings worth making a habit:

**mean against 50%** &mdash; far apart means skew or outliers.

**min and max** &mdash; look for impossible values: a negative age, a zero price, a date in 1900.

**std of zero** &mdash; a constant column, which carries no information and is often a sign something upstream went wrong.

## Looking at the missing rows, not just counting them

Counting missing values tells you how much. Looking at *which* rows are missing tells you why.

```python
df[df["income"].isna()].head()
```

If those rows share something &mdash; the same source, the same date range, the same category &mdash; then the data is not missing at random, and both dropping and imputing will bias the result.

`df.isna().sum(axis=1).value_counts()` shows how many rows have 0, 1, 2... missing values. A long tail means a few badly broken rows; a big spike at one value often means an entire column is absent for a subset of the data.

## Comparing two frames

When something changes and you want to know what, three tools:

`df.equals(other)` &mdash; exact, including dtypes.

`df.compare(other)` &mdash; shows only the cells that differ, side by side. It requires identical shape and labels, which makes it right for before-and-after checks on the same data.

`set(a.columns) ^ set(b.columns)` &mdash; the symmetric difference of column names, which is usually where the discrepancy is.

## The routine, as a block

```python
pd.set_option("display.max_columns", None)

df = pd.read_csv(path, nrows=1000)   # a sample first
df.shape
df.dtypes
df.head()
df.sample(5, random_state=0)
df.info(memory_usage="deep")
df.describe(include="all").T
df.isna().mean().sort_values(ascending=False)
for c in df.select_dtypes("object"):
    print(df[c].value_counts(dropna=False).head())
```

That is a minute of work and it answers most of the questions you would otherwise discover the hard way: what types things are, where the gaps are, which categories are messy, and whether the file is what you were told it was.

## Profiling a frame quickly

For a fast overall picture beyond `describe`, three one-liners cover most of it:

```python
df.nunique().sort_values()                      # cardinality per column
df.isna().mean().sort_values(ascending=False)   # missingness per column
df.memory_usage(deep=True).sort_values(ascending=False)
```

Cardinality is the most under-used of the three. A column with one distinct value carries no information. A column with as many distinct values as rows is an identifier, not a feature. Everything interesting is in between, and the ranking tells you which columns are which without opening any of them.

## Checking assumptions explicitly

Looking at data is better than not looking, and asserting is better than looking, because an assertion keeps checking after you stop paying attention.

```python
assert df["id"].is_unique
assert df["age"].between(0, 120).all()
assert set(df["status"]) <= {"open", "closed"}
assert df["date"].notna().all()
```

Each of these encodes something you believe about the data. When the belief stops being true &mdash; a new export, a changed upstream system &mdash; the script stops rather than producing a quietly wrong answer.

That is worth more than any amount of exploratory looking, because the looking happens once and the assertions happen every run.

## The shape of a first pass

The order matters, because each step informs the next.

**Shape and dtypes** &mdash; is this the file I think it is?

**head, tail, sample** &mdash; does the data look like data?

**info** &mdash; where are the gaps and how big is this?

**describe** &mdash; are there impossible or extreme values?

**value_counts on categoricals** &mdash; are the categories what I expect, and how many are there?

**Missingness pattern** &mdash; are the gaps random or structured?

Only then is it worth writing any analysis. Every one of these steps has caught, for someone, a problem that would otherwise have surfaced in a result presented to someone else.

## Two habits that pay repeatedly

**Look at the rows you are about to drop.** Before `dropna`, before a filter, before deduplication &mdash; `df[mask].head()`. If the rows you are discarding share a pattern, you are not removing noise, you are removing a category.

**Compare counts before and after every step that can change them.** A filter, a merge, a group-by, a concat. One number, checked, catches silent row multiplication and silent row loss, which between them account for a large share of wrong answers in data work.

## A closing note

Every one of these calls exists because someone shipped a wrong answer that one of them would have caught.

The routine is short enough to run without thinking about it, and the discipline is to run it **before** writing any analysis rather than after a result looks odd. By the time a number looks wrong, the cheap explanations have been ruled out and the expensive debugging has started.

The single highest-value line is `df.dtypes`. It catches the identifier read as an integer, the date left as text, and the numeric column turned into strings by one stray value &mdash; three failures that produce plausible output and no error.

The second is `value_counts` on the categorical columns, which finds the variants that would silently split a group-by.

Neither takes more than a few seconds, and together they answer most of what you need to know about a file you have not seen before.

## One more thing

`df.head()` and `df.tail()` can be combined into one view with `pd.concat([df.head(3), df.tail(3)])`, which shows both ends of a sorted frame at once &mdash; useful when the interesting rows are the extremes.

And `df.sample(frac=1)` shuffles the whole frame, which is occasionally the honest way to look at data that arrived in a meaningful order, since the first rows of a sorted file are not representative of anything.

## In summary

Six calls, run before any analysis, catch most of what goes wrong: `shape`, `dtypes`, `head`/`sample`, `info`, `describe`, and `value_counts` on the categorical columns.

`dtypes` is the one that earns its place. It reveals the identifier read as a number, the date still stored as text, and the numeric column turned into strings by a single stray value &mdash; three failures that produce plausible output and no error at all.

And an assertion is worth more than a look, because the look happens once and the assertion happens every run.
''',
    [
        {"q": "Why check `df.dtypes` immediately after loading?",
         "options": ["To count rows", "It reveals lost leading zeros, unparsed dates and integer columns turned float", "It is required", "To free memory"],
         "answer": 1,
         "why": "None of those failures raise. They produce plausible output that is wrong, and surface much later somewhere unrelated."},
        {"q": "Why is `head()` alone not enough?",
         "options": ["It is slow", "It hides sorted, dated or partway-changing data - sample() shows the middle", "It only shows one row", "It drops columns"],
         "answer": 1,
         "why": "tail() also catches trailing junk like summary rows or a footer the exporter added."},
        {"q": "What does a mean far from the median tell you in `describe()`?",
         "options": ["Nothing", "The distribution is skewed or has outliers, so mean-based summaries will mislead", "The data is missing", "The dtype is wrong"],
         "answer": 1,
         "why": "A mean of 220 with a 50% of 30 says something important before you write any analysis."},
        {"q": "What does `value_counts()` on a text column typically catch?",
         "options": ["Memory leaks", "Typos, stray capitals and trailing spaces that would silently split a group-by", "Missing dtypes", "Row count"],
         "answer": 1,
         "why": "'pune', 'Pune' and 'pune ' are three groups, and nothing warns you. Pass dropna=False to see missing values too."},
    ],
)


# ---------------------------------------------------------------------------
# 5. loc and iloc
# ---------------------------------------------------------------------------
topic(
    "loc_and_iloc",
    "loc and iloc",
    "Selecting Data",
    "Label or position - and the endpoint rule that differs between them.",
    _svg(_txt(42, 22, ".loc", A, 9) + _txt(42, 36, "label", M, 8) +
         _txt(116, 22, ".iloc", A, 9) + _txt(116, 36, "position", M, 8) +
         _box(20, 46, 44, 26, S, A) + _box(96, 46, 44, 26, S, A)),
    [
        ("loc takes labels, iloc takes positions",
         "On a default index they look identical, which is exactly why the difference "
         "goes unnoticed.",
         '''import pandas as pd

s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print("s.loc['b'] ->", s.loc["b"], " by label")
print("s.iloc[1]  ->", s.iloc[1], " by position")
print()
d = pd.Series([10, 20, 30])
print("with a default index they agree:")
print("   d.loc[1] =", d.loc[1], "  d.iloc[1] =", d.iloc[1])
print()
print("until the index is not 0..n-1:")
r = pd.Series([10, 20, 30], index=[10, 20, 30])
print("   r.loc[10] =", r.loc[10], " <- the LABEL 10")
print("   r.iloc[0] =", r.iloc[0], " <- the FIRST row")'''),

        ("The endpoint rule is different",
         "loc includes the last label; iloc excludes the last position, like every "
         "other Python slice.",
         '''import pandas as pd

s = pd.Series([0, 1, 2, 3, 4], index=list("abcde"))

print("s.loc['b':'d'] ->", list(s.loc["b":"d"]), " 3 items, 'd' INCLUDED")
print("s.iloc[1:4]    ->", list(s.iloc[1:4]), " 3 items, position 4 excluded")
print()
print("With labels there is no 'one past the end' to point at, so loc")
print("has to be inclusive. It catches everyone once.")
print()
n = pd.Series([0, 1, 2, 3, 4])
print("on a default index the two forms differ by one row:")
print("   n.loc[1:3] ->", list(n.loc[1:3]))
print("   n.iloc[1:3] ->", list(n.iloc[1:3]))'''),

        ("Two axes at once",
         "Rows first, then columns - and this is the form to prefer over chained "
         "brackets.",
         '''import pandas as pd

df = pd.DataFrame({
    "name": ["ana", "raj", "kim"],
    "age": [31, 25, 40],
    "city": ["pune", "delhi", "goa"],
}, index=["r1", "r2", "r3"])

print("one cell     :", df.loc["r2", "age"])
print("a whole row  :", dict(df.loc["r2"]))
print("a whole col  :", list(df.loc[:, "age"]))
print()
print("row range and two columns:")
print(df.loc["r1":"r2", ["name", "city"]])
print()
print("by position:")
print(df.iloc[0:2, [0, 2]])'''),

        ("Boolean masks go in loc",
         "And a mask can be combined with a column selection in the same call.",
         '''import pandas as pd

df = pd.DataFrame({
    "name": ["ana", "raj", "kim", "sam"],
    "age": [31, 25, 40, 19],
    "city": ["pune", "delhi", "goa", "pune"],
})

adults = df.loc[df["age"] >= 25]
print("filtered rows:"); print(adults)
print()
print("filter AND pick columns in one call:")
print(df.loc[df["age"] >= 25, ["name", "city"]])
print()
print("iloc will NOT take a boolean Series:")
try:
    df.iloc[df["age"] >= 25]
except Exception as e:
    print("   df.iloc[mask] ->", type(e).__name__)
print("   (it accepts a plain list of bools, but not a labelled Series)")'''),

        ("at and iat for a single value",
         "Faster, and they say 'exactly one cell' out loud.",
         '''import pandas as pd
import time

df = pd.DataFrame({"a": range(1000), "b": range(1000)})

t = time.perf_counter()
for i in range(2000):
    v = df.at[500, "a"]
at_time = time.perf_counter() - t

t = time.perf_counter()
for i in range(2000):
    v = df.loc[500, "a"]
loc_time = time.perf_counter() - t

print("df.at  : %.4f s" % at_time)
print("df.loc : %.4f s" % loc_time)
print("ratio  : %.1fx" % (loc_time / max(at_time, 1e-9)))
print()
print("at takes labels, iat takes positions, and both are scalar-only.")
print("They raise if you ask for more than one cell, which is a feature.")'''),

        ("Assigning through loc is the safe way",
         "One call, one object - the pattern the next module is entirely about.",
         '''import pandas as pd

df = pd.DataFrame({"name": ["ana", "raj", "kim"], "age": [31, 25, 40]})

df.loc[df["age"] < 30, "age"] = 30
print("after a single loc assignment:")
print(df)
print()
print("adding a column for selected rows fills the rest with NaN:")
df.loc[df["age"] > 35, "band"] = "senior"
print(df)
print()
print("The rule: put the row selection and the column selection in ONE")
print("loc call. Two sets of brackets is where trouble starts.")'''),
    ],
    [
        "<code>.loc</code> selects by <strong>label</strong>, <code>.iloc</code> by <strong>position</strong>. On a default index they agree, which hides the difference until the index changes.",
        "<code>.loc</code> slices are <strong>inclusive</strong> of the last label; <code>.iloc</code> slices exclude the last position like every other Python slice.",
        "Both take rows first, then columns: <code>df.loc[rows, cols]</code>.",
        "Boolean masks belong in <code>.loc</code>. <code>.iloc</code> rejects a labelled boolean Series.",
        "<code>.at</code> and <code>.iat</code> read a single cell and are meaningfully faster than <code>.loc</code> in a loop.",
        "Assign through <strong>one</strong> <code>.loc</code> call with both selections in it &mdash; chained brackets are where the copy warning comes from.",
    ],
    '''
title: loc and iloc
intro: Label or position, and the endpoint rule that differs between them.

## The distinction

`.loc` selects by **label** &mdash; the values in the index.

`.iloc` selects by **position** &mdash; where the row sits, from 0.

On a freshly created frame the index is `0, 1, 2, ...`, so label and position are the same number and the two behave identically. That coincidence is why the difference goes unnoticed until something breaks it: a filter, a sort, a join, a `set_index`.

After any of those, `df.loc[0]` and `df.iloc[0]` can refer to different rows &mdash; or `.loc[0]` can raise `KeyError` because no row is labelled 0 any more.

Writing `.loc` or `.iloc` explicitly, rather than bare `df[...]`, makes the choice visible. Bare brackets guess, and the guess changes with the argument type: `df["age"]` is a column, `df[0:2]` is rows by position, `df[mask]` is rows by condition. Three meanings for one syntax is a lot to hold, and the explicit accessors cost four characters.

## The endpoint rule

This is the one that catches everyone.

`df.iloc[1:4]` gives positions 1, 2, 3 &mdash; the end is **excluded**, exactly like a list slice.

`df.loc["b":"d"]` gives labels b, c **and d** &mdash; the end is **included**.

The reason is that labels have no natural "one past the end". With positions you can point at index 4 to mean "stop before here". With arbitrary labels &mdash; strings, dates, non-contiguous integers &mdash; there is no such thing as the label after `d`, so pandas includes it.

The practical consequence: on a default index, `df.loc[1:3]` returns **three** rows and `df.iloc[1:3]` returns **two**. Both look correct in isolation.

Label slicing also requires a sorted index when the labels are not unique or not monotonic; otherwise it raises rather than guessing.

## Two axes

Both accessors take rows first, then columns:

`df.loc[row_selection, column_selection]`

Each part can be a single value, a list, a slice or (for `.loc`) a boolean mask.

`df.loc[:, "age"]` is a whole column. `df.loc["r2"]` is a whole row, returned as a Series whose index is the column names.

This two-axis form is the one to prefer, and not only for brevity. `df.loc[mask, "col"]` is a single indexing operation on a single object, which is what makes assignment through it reliable. `df[mask]["col"]` is two operations, the first of which may have produced a copy &mdash; and that is the subject of the next module.

## Boolean masks

Masks go in `.loc`. `df.loc[df["age"] >= 25]` selects matching rows, and `df.loc[df["age"] >= 25, ["name", "city"]]` selects matching rows and named columns in one call.

`.iloc` does not accept a labelled boolean Series. It will take a plain list or array of booleans, but not a Series, because a Series carries an index and `.iloc` is defined to ignore labels &mdash; accepting one would be ambiguous. The error is deliberate.

If you need to use a mask positionally, `.to_numpy()` on it strips the index.

## at and iat

For a single cell, `.at` (label) and `.iat` (position) are faster than `.loc` and `.iloc`, because they skip the machinery that handles slices, lists and masks.

The difference is small for one call and substantial in a loop, as the fifth editor measures.

They also raise if you ask for more than one cell, which makes them self-documenting: seeing `.at` in code tells you the author meant exactly one value.

That said, a loop over cells is usually the wrong shape for the problem. `.at` makes a loop faster; removing the loop makes it unnecessary.

## Assignment

The rule is short: **one `.loc` call, with both the row and column selection inside it**.

```python
df.loc[df["age"] < 30, "age"] = 30
```

pandas can see this is a single indexing operation on `df` itself, so it writes to `df`.

```python
df[df["age"] < 30]["age"] = 30
```

does not reliably work. The first bracket produces a new object, and the assignment may write to that temporary rather than to `df`. Historically this raised `SettingWithCopyWarning`; in current pandas it may silently do nothing.

Assigning a column for a subset of rows fills the unselected rows with `NaN`, which is usually what you want and is worth expecting rather than discovering.

## A working summary

Use `.loc` when you mean labels, `.iloc` when you mean positions, and write one of them rather than bare brackets.

Remember that `.loc` slices include the endpoint.

Put row and column selection in the same call.

Use `.at`/`.iat` for a single cell if you are in a loop, and consider whether the loop should exist.

And after any filter or sort, be aware that positions and labels have parted company &mdash; which is the source of most of the confusion these two accessors exist to prevent.

## What bare brackets do

`df[...]` guesses from the argument, and the guess changes with the type:

`df["age"]` &mdash; a **column**, returned as a Series.

`df[["age", "city"]]` &mdash; several **columns**, returned as a DataFrame.

`df[0:2]` &mdash; **rows** by position.

`df["a":"c"]` &mdash; **rows** by label.

`df[mask]` &mdash; **rows** by condition.

Five behaviours, two axes, one syntax. It reads well for the common case &mdash; selecting a column &mdash; and is a genuine source of confusion for everything else, because the same brackets sometimes mean rows and sometimes columns.

`.loc` and `.iloc` remove the guessing. That is the argument for using them even where bare brackets would work.

One consequence worth knowing: on a Series, `s[0]` is ambiguous when the index is integers. Is `0` a label or a position? pandas treats it as a **label**, which raises if there is no label 0 even when there are plenty of rows. This ambiguity is why the positional-only accessor exists.

## Callable selection

Both accessors accept a **function** that receives the object and returns a selection:

```python
df.loc[lambda d: d["age"] > 30]
```

That looks like extra syntax for the same thing, and it earns its place in a chain, where `df` may not be the object being selected from:

```python
(df.query("year == 2024")
   .assign(total=lambda d: d["a"] * d["b"])
   .loc[lambda d: d["total"] > 100])
```

Without the lambda, the final `loc` would have to reference an intermediate that does not have a name.

## Selecting columns by type or name pattern

`df.select_dtypes(include="number")` picks columns by dtype, and `exclude=` is the inverse. This is how you apply an operation to every numeric column without listing them.

`df.filter(like="date")` selects columns whose name contains a substring; `regex=` takes a pattern; `items=` takes an explicit list.

Both return a frame, so they compose with everything else. They are considerably more robust than a hard-coded column list when the source data gains or loses columns.

## Setting values

The rules for assignment through `.loc` are worth stating explicitly, because each has a failure mode.

**A scalar broadcasts**: `df.loc[mask, "col"] = 0` fills every selected row.

**A list or array must match the selection length exactly**, and goes in positionally.

**A Series aligns on the index**, so labels that are not in the selection are ignored and labels missing from it become `NaN`.

**A new column created for a subset** leaves `NaN` in the unselected rows.

**The dtype does not widen to fit**: assigning 3.7 into an integer column stores 3. Assigning a string into a numeric column may upcast the whole column to `object`, which is worse.

## Enlargement

`.loc` can create rows and columns that do not exist:

`df.loc["new_row"] = [...]` adds a row. `df.loc[:, "new_col"] = ...` adds a column.

`.iloc` **cannot** &mdash; a position that does not exist is an error, since there is no sensible position to create.

Enlargement is convenient for one addition and is the quadratic anti-pattern in a loop. It is the mechanism behind `df.loc[len(df)] = row`, which is the slow way to build a frame.

## A summary

Use `.loc` for labels and `.iloc` for positions, and write one of them rather than relying on bare brackets to guess.

Remember `.loc` slices include the endpoint and `.iloc` slices do not.

Put both selections in one call, especially when assigning.

Use `.at`/`.iat` for a single cell in a loop, and consider whether the loop is necessary.

Use `select_dtypes` and `filter` instead of hard-coded column lists when the schema may change.

And after any filter or sort, remember that labels and positions have parted company &mdash; which is the confusion these accessors exist to prevent.

## Copy or view, briefly

Whether `.loc` returns a view or a copy is deliberately unspecified, and depends on the internal block layout.

That is the whole reason the copy warning exists, and it is why the guidance in this module is phrased as "put both selections in one call" rather than "select and then assign".

Under copy-on-write, selections always behave as copies and the ambiguity disappears &mdash; but the one-call rule remains correct, because it is also clearer.

## Selecting a single row or column

`df.loc["r2"]` returns a **Series** whose index is the column names. That means the row's values are forced into one dtype: a row containing an integer and a string comes back as `object`, and the integer is now an object.

That is a real hazard when iterating rows or passing a row to a function. It is the same problem `iterrows` has, for the same reason.

`df.loc[["r2"]]` &mdash; a list rather than a scalar &mdash; returns a one-row **DataFrame** instead, preserving each column's dtype. When the dtypes matter, that is the form to use.

The same distinction applies to columns: `df["a"]` is a Series, `df[["a"]]` is a one-column frame.

## Common errors and what they mean

**`KeyError`** on `.loc` &mdash; the label does not exist. Often because the frame was filtered and the labels changed, or because the key is a string where you passed an integer.

**`IndexError`** on `.iloc` &mdash; the position is out of range.

**"Cannot mask with non-boolean array containing NA / NaN values"** &mdash; a `.str` predicate without `na=False`.

**"The truth value of a Series is ambiguous"** &mdash; `and`/`or` where `&`/`|` was needed, or a missing pair of parentheses.

**"cannot reindex on an axis with duplicate labels"** &mdash; the index has repeats and the operation needs uniqueness.

**`SettingWithCopyWarning`** &mdash; two indexing operations on the left of an assignment.

Each of these has one usual cause, and recognising them saves more time than any amount of general debugging.

## A short reference

`df["col"]` &mdash; one column, as a Series.

`df[["a", "b"]]` &mdash; several columns, as a frame.

`df.loc[rows, cols]` &mdash; by label, endpoint inclusive.

`df.iloc[rows, cols]` &mdash; by position, endpoint exclusive.

`df.at[row, col]` / `df.iat[i, j]` &mdash; one cell, fast.

`df.loc[mask]` &mdash; rows by condition.

`df.loc[mask, "col"] = value` &mdash; the only assignment form worth using.

`df.select_dtypes(...)` / `df.filter(...)` &mdash; columns by type or name pattern.

## A closing note

The distinction is small to state and causes a disproportionate amount of confusion, because on a freshly loaded frame label and position are the same number.

They part company the first time anything filters, sorts, joins or reindexes &mdash; and from then on `df.loc[0]` and `df.iloc[0]` may be different rows, or `.loc[0]` may raise because no row is labelled 0 any more.

Writing `.loc` or `.iloc` rather than bare brackets makes the choice explicit, which matters because bare brackets guess differently depending on what you hand them: a column for a string, rows for a slice, rows for a mask.

The endpoint rule is the other thing to carry: `.loc` slices include the last label, `.iloc` slices do not. On a default index the two forms differ by exactly one row, and both look correct.

And for assignment there is only one form worth using &mdash; a single `.loc` with the rows and the column both inside it.
''',
    [
        {"q": "On a default index, how many rows does `df.loc[1:3]` return?",
         "options": ["Two", "Three - .loc includes the endpoint", "Four", "It raises"],
         "answer": 1,
         "why": "df.iloc[1:3] returns two. Labels have no natural 'one past the end', so .loc has to be inclusive."},
        {"q": "Why does `.iloc` reject a boolean Series?",
         "options": ["It is a bug", "A Series carries an index, and .iloc is defined to ignore labels - accepting one would be ambiguous", "Booleans are unsupported", "It only takes integers"],
         "answer": 1,
         "why": "It accepts a plain list or array of booleans. Use .to_numpy() on the mask to strip the index."},
        {"q": "Which assignment reliably modifies `df`?",
         "options": ["df[mask]['col'] = x", "df.loc[mask, 'col'] = x", "df['col'][mask] = x", "All of them"],
         "answer": 1,
         "why": "One .loc call is a single indexing operation on df itself. Chained brackets may write to a temporary and silently do nothing."},
        {"q": "When do `.loc[0]` and `.iloc[0]` refer to different rows?",
         "options": ["Never", "After any filter, sort, join or set_index changes the index", "Only on Series", "Only with strings"],
         "answer": 1,
         "why": "On a fresh frame label and position coincide, which is exactly why the difference goes unnoticed until something breaks it."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Filtering rows
# ---------------------------------------------------------------------------
topic(
    "filtering_rows",
    "Filtering Rows",
    "Selecting Data",
    "Masks, isin, between and query - and the parenthesis rule that catches "
    "everyone once.",
    _svg(_grid(20, 26, 1, 5, 13) + _txt(27, 22, "all", M, 8) +
         _arrow(44, 58, 62, 58) +
         _grid(72, 39, 1, 2, 13) + _txt(79, 22, "kept", A, 8)),
    [
        ("A comparison gives a boolean Series",
         "Which you then hand to loc. The mask keeps the original index.",
         '''import pandas as pd

df = pd.DataFrame({
    "name": ["ana", "raj", "kim", "sam"],
    "age": [31, 25, 40, 19],
})
mask = df["age"] >= 25
print("the mask itself:")
print(mask)
print()
print("used to select:")
print(df.loc[mask])
print()
print("count matches for free, because True is 1:")
print("   matched:", int(mask.sum()), "of", len(mask))'''),

        ("Parentheses are not optional",
         "<code>&</code> binds tighter than <code>&gt;</code>, so the obvious spelling "
         "parses wrongly.",
         '''import pandas as pd

df = pd.DataFrame({"age": [19, 25, 31, 40]})

good = df.loc[(df["age"] > 20) & (df["age"] < 35)]
print("with parentheses:", list(good["age"]))

try:
    df.loc[df["age"] > 20 & df["age"] < 35]
except Exception as e:
    print("without them    :", type(e).__name__)
    print("   ", str(e)[:70])

print()
try:
    df.loc[(df["age"] > 20) and (df["age"] < 35)]
except ValueError as e:
    print("using `and`     : ValueError")
    print("   ", str(e)[:66])
print()
print("Use & | ~ , never and/or/not, and parenthesise every condition.")'''),

        ("isin and between",
         "Clearer than a chain of comparisons, and they read as the question you "
         "are asking.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "goa", "pune"],
    "age": [31, 25, 40, 19],
})

print("isin:")
print(df.loc[df["city"].isin(["pune", "goa"])])
print()
print("between is inclusive on both sides by default:")
print(list(df.loc[df["age"].between(25, 31), "age"]))
print("   exclusive:", list(df.loc[df["age"].between(25, 31, inclusive="neither"), "age"]))
print()
print("negate with ~ :")
print(list(df.loc[~df["city"].isin(["pune"]), "city"]))'''),

        ("Missing values fail every test",
         "So a condition and its opposite can both drop the same row.",
         '''import pandas as pd
import numpy as np

s = pd.Series([1.0, np.nan, 5.0])
print("s > 2 :", list(s > 2))
print("s <= 2:", list(s <= 2))
print("   the NaN row is False in BOTH - it vanishes from either half.")
print()
print("counts:", int((s > 2).sum()), "+", int((s <= 2).sum()), "= 2, not 3")
print()
print("Handle it explicitly when it matters:")
print("   isna :", list(s.isna()))
print("   fillna first:", list(s.fillna(0) > 2))'''),

        ("query, when the expression is long",
         "A string, so column names need no quoting - and no parentheses either.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "goa", "pune"],
    "age": [31, 25, 40, 19],
    "score": [8.5, 9.1, 7.2, 6.0],
})

print(df.query("age > 20 and score > 7"))
print()
print("no parentheses needed, and `and` works here because it is")
print("pandas' own parser rather than Python's operators.")
print()
print("reference a Python variable with @:")
cutoff = 30
print(list(df.query("age > @cutoff")["city"]))
print()
print("in / not in work too:")
print(list(df.query("city in ['pune', 'goa']")["city"]))'''),

        ("Filtering returns a new frame",
         "Which is why assigning into the result is the mistake the next module is "
         "about.",
         '''import pandas as pd

df = pd.DataFrame({"name": ["ana", "raj"], "age": [31, 25]})
sub = df.loc[df["age"] > 30]

print("the filtered frame:")
print(sub)
print()
print("its index kept the original labels:", list(sub.index))
print()
sub2 = df.loc[df["age"] > 30].reset_index(drop=True)
print("reset_index(drop=True) renumbers:", list(sub2.index))
print()
print("Filtering never modifies the original:")
print("   original still has", len(df), "rows")'''),
    ],
    [
        "A comparison produces a boolean Series; pass it to <code>.loc</code>. <code>mask.sum()</code> counts matches for free.",
        "Parenthesise every condition and use <code>&amp; | ~</code>. <code>and</code> raises, and missing parentheses parse wrongly because <code>&amp;</code> binds tighter than <code>&gt;</code>.",
        "<code>isin</code> and <code>between</code> read as the question you are asking; <code>between</code> is inclusive on both ends by default.",
        "<strong>Missing values fail every comparison</strong>, so a condition and its negation can both drop the same row.",
        "<code>query(\"age &gt; 20 and score &gt; 7\")</code> takes a string, needs no parentheses, and uses <code>@name</code> to reference Python variables.",
        "Filtering returns a <strong>new</strong> frame and keeps the original labels &mdash; it never modifies the original.",
    ],
    '''
title: Filtering Rows
intro: Masks, isin, between and query, and the parenthesis rule that catches everyone.

## A mask is a Series

`df["age"] >= 25` does not return rows. It returns a boolean Series, one value per row, carrying the same index as the frame.

You then hand that mask to `.loc`, and pandas keeps the rows where it is `True`.

Because the mask is an ordinary Series, everything you know applies to it. `mask.sum()` counts matches, since `True` is 1. `mask.mean()` gives the proportion. `~mask` inverts it. It can be stored in a variable, named, and reused.

Naming masks is worth doing when a filter has several parts:

```python
adult = df["age"] >= 18
local = df["city"] == "pune"
recent = df["days"] < 30
df.loc[adult & local & recent]
```

Each name documents a condition, and each can be counted separately when the result is unexpectedly empty &mdash; which is how you find out which clause is doing the damage.

## The parenthesis rule

This is the single most common syntax error in pandas.

`df["age"] > 20 & df["age"] < 35` does not mean what it looks like. In Python, `&` binds **tighter** than `>`, so this parses as `df["age"] > (20 & df["age"]) < 35`. The result is an error or, worse, something plausible.

Every condition needs its own parentheses: `(df["age"] > 20) & (df["age"] < 35)`.

The related mistake is `and` instead of `&`. Python's `and` needs a single truth value and a Series has many, so it raises "The truth value of a Series is ambiguous". That message always means the same thing: use `&`, and add parentheses.

The three operators are `&` (and), `|` (or), `~` (not). There is no way to make Python's precedence rules cooperate here, so parenthesising becomes a reflex.

## isin and between

`df["city"].isin(["pune", "goa"])` is clearer and faster than `(df["city"] == "pune") | (df["city"] == "goa")`, and it scales to a list of any length &mdash; including one computed at runtime.

`df["age"].between(25, 31)` is inclusive of both ends by default. The `inclusive` argument takes `"both"`, `"left"`, `"right"` or `"neither"`, which is worth passing explicitly whenever the boundary matters, because the default is not what everyone assumes.

`~` negates either of them.

## Missing values fail everything

Every comparison involving `NaN` is `False`. That includes `>`, `<`, `==` and `!=`.

The consequence is specific and easy to miss: `df[df["x"] > 2]` and `df[df["x"] <= 2]` do **not** partition the frame. Rows where `x` is missing are absent from both, and the two counts do not add up to the row count.

This is usually the right default &mdash; an unknown value genuinely does not satisfy a condition &mdash; but it means "everything else" is not the same as "the negation of this condition" whenever missing data is possible.

When missing rows should be handled rather than dropped, say so explicitly with `isna()`, or fill before filtering.

## query

`df.query("age > 20 and score > 7")` takes the condition as a string.

Inside the string, column names are bare identifiers, `and`/`or`/`not` work normally, and no parentheses are needed for precedence. That makes long conditions much easier to read than the operator form.

`@name` references a Python variable: `df.query("age > @cutoff")`.

`in` and `not in` work against lists.

The costs: column names with spaces need backticks, there is no editor autocompletion or type checking inside a string, and a typo becomes a runtime error rather than something a linter catches. `query` also has a small parsing overhead per call, which is irrelevant once and noticeable in a loop.

Use it when a condition is long enough that the operator form is hard to read. Use operators otherwise.

## Filtering copies

`df.loc[mask]` returns a **new** frame. The original is untouched, and the result keeps the original index labels rather than renumbering.

Both facts matter downstream. The surviving labels mean positional code breaks, and `reset_index(drop=True)` is the fix when you want a clean `0..n-1`.

That the result is new &mdash; and specifically that it may be a copy rather than a view of the original &mdash; is what makes assigning into a filtered frame unreliable. That is the subject of the next module, and it is the single largest source of confusion in pandas.

## A summary

Build masks with comparisons, combine with `& | ~`, and parenthesise everything.

Prefer `isin` and `between` where they fit; they say what you mean.

Remember NaN fails every test, so a condition and its negation are not a partition.

Reach for `query` when the expression is long, and for operators when it is short.

And know that the result is a new object whose index came along for the ride.

## Filtering on more than one column

Conditions on different columns combine exactly like conditions on one:

```python
df.loc[(df["age"] >= 18) & (df["city"] == "pune")]
```

For a variable number of conditions &mdash; built from user input, or a config &mdash; combine them programmatically:

```python
from functools import reduce
mask = reduce(lambda a, b: a & b, conditions)
```

`np.logical_and.reduce(conditions)` does the same thing. Either is better than building a query string, which loses type checking and invites injection if any part comes from outside.

## Filtering by index rather than data

`df.loc[["a", "c"]]` selects by label and **raises** if a label is missing.

`df.reindex(["a", "c", "zz"])` selects by label and fills missing ones with `NaN` instead. The difference matters when you are conforming one frame to another's labels and absence is expected.

`df[df.index.isin(wanted)]` filters by membership without requiring every label to exist.

`df.index.str.startswith("2024")` works when the labels are strings, since an Index has the `.str` accessor too.

## Filtering with a lookup from another frame

The common task of "keep rows whose key appears in this other table" has two forms.

`df[df["id"].isin(other["id"])]` is the direct one, and it is usually what you want. It cannot change the row count upward and needs no thought about join semantics.

`df.merge(other[["id"]], on="id")` does the same thing as an inner join, and **can** multiply rows if `other` has duplicate ids. `isin` cannot.

For "keep rows whose key does **not** appear", `~isin` is the whole answer, where the join equivalent needs an outer join with an indicator and a filter. This is one of the places `isin` is clearly better than a merge.

## nlargest, sample and head as filters

Not every subset comes from a condition.

`df.nlargest(10, "sales")` &mdash; the top ten by a column, without sorting everything.

`df.sample(n=100, random_state=0)` &mdash; a random subset, reproducible with the seed. `frac=0.1` takes a proportion.

`df.head(1000)` &mdash; the first thousand, which is only meaningful if the order means something.

`df.drop_duplicates(subset=["id"])` &mdash; one row per key.

## Performance

Filtering builds a boolean mask the length of the frame, then copies the matching rows. Both cost time proportional to the data.

Three things that help on large frames:

**Combine conditions before selecting.** `df[(a) & (b)]` allocates one result; `df[a][b]` allocates two.

**Filter before computing**, not after. Every operation downstream then touches fewer rows &mdash; usually the largest structural win available.

**Use a category dtype** for the columns you filter on repeatedly. Comparison then runs on integer codes rather than strings.

`query` has a small parsing overhead per call, which is irrelevant once and measurable in a loop. It can also use `numexpr` for very large frames, which occasionally makes it faster than the operator form rather than slower.

## The mistakes, collected

**Missing parentheses.** `(a > 1) & (b < 2)`, always.

**`and` instead of `&`.** The "truth value is ambiguous" error always means this.

**Forgetting `na=False`** on a `.str` predicate, which raises as soon as the data has a gap.

**Assuming a condition and its negation partition the frame.** They do not, when values can be missing.

**Chained assignment on a filtered frame.** `df[mask]["col"] = x` &mdash; the subject of its own module, and the most expensive mistake here.

**Forgetting the index came along.** `reset_index(drop=True)` when downstream code thinks positionally.

## Filters that read well

A filter is a statement about the data, and it is worth writing it as one.

Naming masks does most of the work:

```python
is_adult = df["age"] >= 18
in_scope = df["city"].isin(cities)
recent   = df["date"] >= cutoff

df.loc[is_adult & in_scope & recent]
```

Three benefits beyond readability: each mask can be counted separately when the result is unexpectedly empty; the masks can be reused for a complementary selection; and the combining line reads as the sentence it represents.

For a filter that appears in several places, a small function returning the mask keeps the definition in one place:

```python
def active(d):
    return (d["status"] == "open") & d["closed_at"].isna()
```

`df.loc[active(df)]` then means the same thing everywhere, and changing the definition changes it everywhere.

## Debugging an empty result

When a filter returns nothing, the cause is nearly always one of five things, and they can be checked in about a minute.

**A type mismatch.** `df["id"] == 1` against a string column matches nothing. Check `df["id"].dtype`.

**Whitespace or case.** `df["city"] == "Pune"` against `"pune "`. Check `df["city"].value_counts().head(20)`.

**Missing values.** They fail every comparison, so a condition can exclude more than you think.

**An `&` that should be `|`.** Conditions that cannot be true simultaneously.

**A stale variable.** In a notebook, `df` is not what the cell above assumed.

Counting each condition separately &mdash; `is_adult.sum()`, `in_scope.sum()` &mdash; identifies which clause is responsible in one step, which is far quicker than reasoning about the combination.

## Filtering and the copy warning

`sub = df[mask]` produces a new frame whose relationship to `df` is deliberately unspecified.

Anything you then assign into `sub` may or may not affect `df`. This is the single most common route into the copy warning, and it is worth deciding at the point of filtering rather than at the point of assignment:

`sub = df[mask].copy()` if `sub` is a separate dataset.

`df.loc[mask, "col"] = ...` if you meant to change `df`.

Adding `.copy()` to a filter you intend to modify costs seven characters and removes the question entirely.

## A summary

Build masks with comparisons; combine with `&`, `|`, `~`; parenthesise everything.

Use `isin` and `between` where they fit, and `query` when the expression is long.

Pass `na=False` on `.str` predicates.

Remember that missing values fail every test, so a condition and its negation do not partition the frame.

Name your masks when there is more than one.

And `.copy()` the result if you are going to modify it.

## A closing note

Filtering is the most-used operation in pandas and has two persistent gotchas, both syntactic and both cheap to avoid.

Parenthesise every condition, because `&` binds tighter than the comparison operators and the unparenthesised version parses into something else entirely. And use `&`, `|`, `~` rather than `and`, `or`, `not`, which need a single truth value that a Series cannot provide.

The semantic gotcha is missing values. They fail every comparison, so a condition and its negation do not partition the frame, and rows quietly appear in neither half.

Beyond that, the advice is about readability: name your masks when there is more than one, so each can be counted separately when the result is unexpectedly empty. Debugging a filter that returns nothing is nearly always a matter of finding which clause is responsible, and named masks turn that into one line rather than a process of elimination.

## One more thing

`df.query` accepts `engine="python"` for expressions the default parser cannot handle, and `inplace=True` which, as elsewhere, is best avoided.

## In summary

Comparisons give boolean Series; combine them with `&`, `|` and `~`, and parenthesise every one.

`isin` and `between` read as the question being asked, and `query` earns its place when the expression is long.

Missing values fail every test, so a condition and its negation do not partition the frame. And `.copy()` the result if you intend to modify it, which decides the copy question at the point it arises rather than at the point it bites.
''',
    [
        {"q": "Why does `df[df['age'] > 20 & df['age'] < 35]` fail?",
         "options": ["& is invalid in pandas", "& binds tighter than >, so it parses as df['age'] > (20 & df['age']) < 35", "You must use query", "The columns are wrong"],
         "answer": 1,
         "why": "Python's precedence rules cannot be made to cooperate here, so parenthesising every condition becomes a reflex."},
        {"q": "Do `df[df['x'] > 2]` and `df[df['x'] <= 2]` together cover every row?",
         "options": ["Yes, always", "No - rows where x is NaN fail both comparisons and appear in neither", "Only for integers", "Only if sorted"],
         "answer": 1,
         "why": "Every comparison with NaN is False, so 'everything else' is not the same as 'the negation of this condition' when missing data is possible."},
        {"q": "What does `between(25, 31)` include by default?",
         "options": ["Neither endpoint", "Both endpoints", "Only the left", "Only the right"],
         "answer": 1,
         "why": "The `inclusive` argument takes 'both', 'left', 'right' or 'neither' - worth passing explicitly whenever the boundary matters."},
        {"q": "What does `@` mean inside a `query` string?",
         "options": ["A decorator", "It references a Python variable from the surrounding scope", "A column name", "A comment"],
         "answer": 1,
         "why": "df.query('age > @cutoff') uses the local variable cutoff. Inside the string, bare identifiers are column names."},
    ],
)


# ---------------------------------------------------------------------------
# 7. The copy warning
# ---------------------------------------------------------------------------
topic(
    "the_copy_warning",
    "The Copy Warning",
    "Selecting Data",
    "Why an assignment that looks right silently does nothing - and the one "
    "habit that prevents it.",
    _svg(_box(16, 28, 44, 34, S) + _txt(38, 49, "df", M, 9) +
         _arrow(62, 45, 80, 45) +
         _box(84, 28, 44, 34, S, "#a44") + _txt(106, 45, "copy?", "#e88", 8) +
         _txt(106, 58, "or view?", "#e88", 8)),
    [
        ("The assignment that does nothing",
         "Two sets of brackets, and the write may land on a temporary instead of "
         "your frame.",
         '''import pandas as pd

df = pd.DataFrame({"name": ["ana", "raj", "kim"], "age": [31, 25, 40]})
print("before:", list(df["age"]))

df[df["age"] < 30]["age"] = 99          # chained: two operations

print("after :", list(df["age"]))
print()
print("The frame is unchanged. The write went to the object the first")
print("bracket returned, which was thrown away on the next line.")
print()
print("A SettingWithCopyWarning is printed above this output, in red -")
print("that is pandas telling you the write probably did nothing.")'''),

        ("The same thing in one loc call",
         "One indexing operation on df itself, so pandas knows where to write.",
         '''import pandas as pd

df = pd.DataFrame({"name": ["ana", "raj", "kim"], "age": [31, 25, 40]})
print("before:", list(df["age"]))

df.loc[df["age"] < 30, "age"] = 99

print("after :", list(df["age"]), "<- it worked")
print()
print("The rule: row selection and column selection go in ONE .loc[].")
print("Anything with two sets of brackets on the left of = is suspect.")'''),

        ("Why pandas cannot always tell",
         "Whether a selection is a view or a copy depends on the dtypes involved.",
         '''import pandas as pd

same = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
mixed = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

for name, frame in [("all int", same), ("int + str", mixed)]:
    sub = frame[["a"]]
    sub_is_view = sub._is_view if hasattr(sub, "_is_view") else None
    print("%-10s selecting ['a'] -> _is_view = %s" % (name, sub_is_view))

print()
print("Identical code, opposite answers - and note it is the MIXED")
print("frame that gave the view here, which is the reverse of what")
print("most people guess.")
print()
print("The reason is internal: pandas stores columns in blocks of like")
print("dtype. In the mixed frame 'a' is a block of its own and can be")
print("handed back directly; in the all-int frame it is part of a")
print("larger block, so selecting it has to build something new.")
print()
print("None of that is visible in your code, and it changes when a")
print("column's dtype changes. That is why pandas refuses to guess.")'''),

        ("It bites hardest on a filtered frame",
         "Take a subset, work on it, and the writes may or may not reach the original.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "pune"],
    "sales": [10, 20, 30],
})

sub = df[df["city"] == "pune"]      # a new frame, probably a copy
sub["sales"] = 0                    # writing into it

print("the subset:"); print(sub)
print()
print("the original:"); print(df)
print()
print("Whether df changed is the question you never want to be asking.")
print("If you meant a separate frame, say so with .copy().")'''),

        ("Be explicit: copy() or loc",
         "Decide which one you want, and the ambiguity disappears.",
         '''import pandas as pd

df = pd.DataFrame({"city": ["pune", "delhi", "pune"], "sales": [10, 20, 30]})

# 1. I want a separate frame to work on
sub = df[df["city"] == "pune"].copy()
sub["sales"] = 0
print("after editing an explicit copy, original is untouched:")
print(list(df["sales"]))

# 2. I want to change the original
df.loc[df["city"] == "pune", "sales"] = 0
print()
print("after a single loc assignment, original changed:")
print(list(df["sales"]))
print()
print("Every case is one of those two. Writing which one you meant")
print("costs seven characters and removes the whole problem.")'''),

        ("Copy-on-write, the way out",
         "pandas 3.0 makes every selection behave like a copy. You can switch it on "
         "now.",
         '''import pandas as pd

print("pandas", pd.__version__)

pd.options.mode.copy_on_write = True
df = pd.DataFrame({"a": [1, 2, 3]})
sub = df[df["a"] > 1]
sub["a"] = 0
print()
print("with copy_on_write ON:")
print("   subset :", list(sub["a"]))
print("   original:", list(df["a"]), "<- never affected, no warning")

pd.options.mode.copy_on_write = False
print()
print("Under copy-on-write the rule is simple: a selection NEVER writes")
print("back. To change the original you must say df.loc[...] = ...")
print("It is the default from pandas 3.0 - writing code that way now")
print("means nothing changes when you upgrade.")'''),
    ],
    [
        "<strong>Chained assignment</strong> &mdash; two sets of brackets left of <code>=</code> &mdash; may write to a temporary and silently leave your frame unchanged.",
        "Put the row and column selection in <strong>one</strong> <code>.loc[]</code> call and the write always lands on the frame.",
        "Whether a selection is a view or a copy depends on the internal <strong>block</strong> layout &mdash; and the mixed-dtype frame is the one that gives a view, which is the reverse of what most people guess.",
        "Editing a filtered subset is the usual way this bites &mdash; the writes may or may not reach the original.",
        "Say which you meant: <code>.copy()</code> for a separate frame, <code>.loc[...] = ...</code> to change the original.",
        "<strong>Copy-on-write</strong> makes a selection never write back. It is the default in pandas 3.0 and can be switched on today.",
    ],
    '''
title: The Copy Warning
intro: Why an assignment that looks right silently does nothing.

## The problem

```python
df[df["age"] < 30]["age"] = 99
```

This looks like it sets `age` to 99 for the young rows. Often it does nothing at all, and the frame is unchanged.

The reason is that there are **two** operations here, not one.

`df[df["age"] < 30]` runs first and produces a new object. Then `["age"] = 99` assigns into *that* object. Whether the new object shares memory with `df` decides whether `df` sees the change &mdash; and if it does not, the write lands on a temporary that is discarded on the next line.

Historically pandas noticed this pattern and raised `SettingWithCopyWarning`. The warning is famous for being confusing: it appears where the code looks fine, it sometimes appears when nothing is wrong, and it sometimes fails to appear when something is. In current versions the assignment may simply do nothing, silently.

## Why pandas cannot just fix it

The obvious question is why pandas does not make chained assignment work.

It cannot know, at the time the first bracket runs, that an assignment is coming. `df[mask]` is an ordinary expression that returns an object. Python then calls `__setitem__` on that object. By then the information that this was one statement is gone.

Whether the intermediate is a view or a copy depends on the internal layout, which depends on the dtypes.

pandas stores columns in **blocks** of like dtype. Selecting a column that happens to be a block of its own can hand back a view; selecting one column out of a larger same-dtype block has to build a new object.

The editor above shows this, and the direction surprises most people: the **mixed-dtype** frame gives the view, because there the integer column sits in a block by itself. The all-integer frame gives a copy, because its columns share one block.

So the same line of code can work on one frame and not another, or work in development and fail in production when a column's type changes. That unpredictability, not the warning, is the actual problem.

## The rule

**One indexing operation, with both selections inside it.**

```python
df.loc[df["age"] < 30, "age"] = 99
```

Here pandas sees a single `__setitem__` on `df` itself, with the rows and column both specified. There is no intermediate object and no ambiguity.

Anything with two sets of brackets to the left of `=` deserves a second look. That includes the variants people reach for:

`df["age"][mask] = 99` &mdash; same problem, different order.

`df[mask]["age"] = 99` &mdash; the classic.

`sub = df[mask]` then later `sub["age"] = 99` &mdash; the same thing spread across two statements, which is how it usually appears in real code and why it is harder to spot.

## The subset case

The most common real-world version is not a one-liner. It is:

```python
sub = df[df["city"] == "pune"]
sub["sales"] = 0
```

Here the intent is genuinely ambiguous. Did you want a separate frame to work on, or did you want to change those rows of `df`?

Both are reasonable, and the fix is to say which:

```python
sub = df[df["city"] == "pune"].copy()   # a separate frame
df.loc[df["city"] == "pune", "sales"] = 0   # change the original
```

`.copy()` costs seven characters and removes the entire question. It is worth adding by default whenever you take a subset you intend to modify, even if you are fairly sure it would work without.

## Copy-on-write

pandas is fixing this properly. Under **copy-on-write**, every selection behaves as though it were a copy: modifying a subset never affects the parent, in any circumstances, with no warning and no dtype-dependent surprises.

To change the original you must say so with `.loc`.

It is the default in pandas 3.0. In 2.x you can switch it on:

```python
pd.options.mode.copy_on_write = True
```

The name refers to the implementation, not the behaviour: pandas still avoids copying data until something is actually written, so it is not slower in general and is often faster, because it can drop the defensive copies it used to make.

Writing code that assumes copy-on-write today means nothing changes when you upgrade. In practice that means the two habits above &mdash; explicit `.copy()`, and `.loc` for assignment &mdash; which are worth having regardless.

## If you see the warning

Do not silence it. `pd.options.mode.chained_assignment = None` turns off the message and leaves the bug.

Instead, find the line, and ask which of the two things you meant. The answer is always one of them, and writing it down fixes the code and documents the intent at the same time.

## How to read the warning

The message is famously unhelpful, but it has a structure worth knowing.

*"A value is trying to be set on a copy of a slice from a DataFrame"* &mdash; pandas noticed that the object being written to was produced by indexing another object, and it cannot tell whether the write will propagate.

*"Try using .loc[row_indexer, col_indexer] = value instead"* &mdash; the fix, stated generically.

Two properties make it frustrating.

It points at the **assignment**, which may be far from the line that created the intermediate. `sub = df[mask]` on line 10 and `sub["x"] = 1` on line 40 produce a warning on line 40, and line 10 is the cause.

It is a **heuristic**. It can fire when nothing is wrong, and it can stay silent when something is. That is why "make the warning go away" is the wrong goal &mdash; the goal is to know which object you are writing to.

## Why silencing it is worse than the warning

`pd.options.mode.chained_assignment = None` turns off the message.

It does not change the behaviour. The write still may or may not reach the original frame; you have simply removed the only signal that there was a question.

You will see this suggested. It is the wrong fix in every case, and it is worth recognising in an existing codebase as a sign that someone met this problem and did not resolve it.

## The two-statement version

Most real occurrences are not one-liners. They look like this:

```python
recent = df[df["year"] == 2024]
recent["flag"] = recent["sales"] > 100
```

This is harder to spot than the chained form, because each line looks entirely reasonable, and it is the shape that appears in real analysis code.

The question to ask is: **is `recent` a separate dataset, or a window onto `df`?**

If separate: `recent = df[df["year"] == 2024].copy()`.

If a window: do not create it; write `df.loc[df["year"] == 2024, "flag"] = ...`.

Adding `.copy()` when taking a subset you intend to modify is a cheap default. On a small frame the cost is nothing; on a large one it is a deliberate decision you have now made explicitly rather than by accident.

## Copy-on-write in more detail

Under CoW, every object behaves as though it owns its data. Modifying a subset never affects its parent, and modifying a parent never affects a subset taken earlier.

The name describes the implementation: pandas still shares the underlying arrays, and only copies when something is actually written. So the guarantee is about **behaviour**, not about memory, and in practice CoW often uses *less* memory than the current default, because pandas can drop the defensive copies it makes today.

Three things change when you enable it:

Chained assignment **never** works, and pandas raises a `ChainedAssignmentError` rather than warning.

`SettingWithCopyWarning` disappears, because the ambiguity it warned about is gone.

Some code that relied on a view propagating a write will stop working &mdash; which is the migration cost, and the reason it is opt-in until pandas 3.0.

Turning it on in a project today is a good way to find out whether your code depends on behaviour that is about to change.

## A checklist

**Two sets of brackets left of `=`** &mdash; rewrite as one `.loc`.

**A subset you will modify** &mdash; add `.copy()`.

**A warning you do not understand** &mdash; find where the object was created, not where it was written.

**A tempting `chained_assignment = None`** &mdash; do not.

**New code** &mdash; write it as though copy-on-write is on, because soon it will be.

## Why this module exists

No other pandas behaviour wastes as much time. The warning is famous, the explanations are usually wrong, and the standard advice on forums &mdash; silence it &mdash; leaves the bug in place.

The underlying issue is genuinely hard: Python evaluates `df[mask]["col"] = x` as two separate operations, and by the time the assignment happens the information that this was one statement is gone. pandas is warning about something it cannot fix from where it stands.

Understanding that makes the fix obvious rather than arbitrary. One indexing operation cannot be ambiguous, so put both selections in one call.

## The rules, in one place

**One `.loc` for assignment.** `df.loc[mask, "col"] = value`.

**`.copy()` for a subset you will modify.** `sub = df[mask].copy()`.

**Never silence the warning.** It removes the signal, not the problem.

**Write as though copy-on-write is on.** It will be, by default, in pandas 3.0.

Those four cover every case. There is no fifth situation requiring judgement.

## Recognising it in existing code

Patterns worth searching for in a codebase you have inherited:

`][` on the same line as `=` &mdash; the classic chained assignment.

`pd.options.mode.chained_assignment = None` &mdash; someone met this and did not fix it. Everything downstream of that line is suspect.

`inplace=True` on a subset &mdash; the same problem with different syntax.

A variable assigned from a filter and modified later &mdash; the two-statement form, which no search finds reliably and which is the most common version in real code.

## What changes under copy-on-write

Worth being concrete, because "it will be fixed" is not a plan.

Chained assignment raises `ChainedAssignmentError` instead of warning, so the failure is loud.

`SettingWithCopyWarning` no longer exists.

Code that relied on a view propagating a write &mdash; deliberately or accidentally &mdash; stops working. That is the migration cost, and it is why the change is opt-in for a version.

Memory usage generally goes **down**, because pandas can stop making defensive copies.

Enabling `pd.options.mode.copy_on_write = True` in a project today is the cheapest way to find out whether any of your code depends on the old behaviour.

## The one-line version

If you remember nothing else from this module: **two sets of brackets to the left of an equals sign is a bug**, and `.loc` with both selections inside it is the fix.

## A closing note

This is the only module in the track devoted to a warning message, and it earns the space by how much time it wastes.

The underlying situation is genuinely awkward. `df[mask]["col"] = x` is two operations, and by the time the assignment runs, the fact that it was one statement is gone. pandas cannot fix it from where it stands, so it warns instead &mdash; imperfectly, sometimes when nothing is wrong and sometimes not when something is.

That imperfection is why "make the warning stop" is the wrong goal. The right goal is to know which object you are writing to, and there are only two answers: a separate frame you made with `.copy()`, or the original, addressed through a single `.loc`.

Copy-on-write removes the ambiguity entirely and becomes the default in pandas 3.0. Writing code today as though it is already on costs nothing and means the upgrade changes nothing.

## One more thing

`df._is_copy` holds the internal flag that drives the warning. It is private, it should not be relied on, and knowing it exists occasionally helps when reasoning about why a warning appeared where it did.
''',
    [
        {"q": "Why can `df[mask]['col'] = x` fail to change `df`?",
         "options": ["masks are read-only", "It is two operations - the write may land on a temporary the first bracket returned", "'col' does not exist", "It always works"],
         "answer": 1,
         "why": "By the time Python calls __setitem__ on the intermediate, the information that this was one statement is gone."},
        {"q": "Why can't pandas simply make chained assignment work?",
         "options": ["Nobody has implemented it", "Whether the intermediate is a view or a copy depends on the internal block layout, so behaviour varies with the data", "It is forbidden by Python", "It would be too slow"],
         "answer": 1,
         "why": "Columns are stored in blocks of like dtype, and which case you get is invisible in your code - it changes when a column's dtype changes."},
        {"q": "You take `sub = df[df['city']=='pune']` and intend to edit it separately. What should you add?",
         "options": ["Nothing", ".copy()", ".loc", "reset_index()"],
         "answer": 1,
         "why": "It costs seven characters and removes the ambiguity entirely. Use df.loc[...] = ... instead if you meant to change the original."},
        {"q": "What does copy-on-write change?",
         "options": ["It makes pandas slower", "A selection never writes back to its parent, so you must use .loc to modify the original", "It disables .loc", "It copies every frame immediately"],
         "answer": 1,
         "why": "It is the default in pandas 3.0. The name describes the implementation - data is still not copied until something is written."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Adding and removing columns
# ---------------------------------------------------------------------------
topic(
    "adding_and_dropping",
    "Adding and Removing Columns",
    "Selecting Data",
    "assign, drop, rename - and the alignment that decides what a new column "
    "actually contains.",
    _svg(_box(18, 26, 30, 46, S) + _box(48, 26, 30, 46, S) +
         _box(78, 26, 30, 46, S, A) + _txt(93, 52, "new", A, 8) +
         _txt(63, 20, "existing", M, 8)),
    [
        ("Assigning a new column",
         "Bracket assignment adds it at the end, or replaces it if the name exists.",
         '''import pandas as pd

df = pd.DataFrame({"qty": [3, 1, 2], "price": [10.0, 250.0, 400.0]})

df["total"] = df["qty"] * df["price"]
print(df)
print()
df["currency"] = "INR"            # a scalar fills every row
print("a scalar broadcasts:", list(df["currency"]))
print()
print("assigning an existing name replaces it, silently:")
df["currency"] = "USD"
print("   ", list(df["currency"]))
print()
print("column order is insertion order:", list(df.columns))'''),

        ("assign returns a new frame",
         "Which is what makes it chainable, and what makes it safe.",
         '''import pandas as pd

df = pd.DataFrame({"qty": [3, 1, 2], "price": [10.0, 250.0, 400.0]})

out = (df
       .assign(total=lambda d: d["qty"] * d["price"])
       .assign(cheap=lambda d: d["total"] < 100))
print(out)
print()
print("the original is untouched:", list(df.columns))
print()
print("the lambda sees the frame AS IT IS AT THAT POINT, so the second")
print("assign can use the column the first one created.")'''),

        ("Alignment decides what lands in the column",
         "Assigning a Series matches on the index, not on position.",
         '''import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3]}, index=["x", "y", "z"])

s = pd.Series([100, 200, 300], index=["z", "y", "x"])
df["aligned"] = s
print("assigning a Series with a shuffled index:")
print(df)
print("   x got 300, because alignment is by LABEL")
print()
partial = pd.Series([9, 9], index=["x", "q"])
df["partial"] = partial
print()
print("labels that do not match become NaN:")
print(df[["a", "partial"]])
print()
print("a plain list has no index, so it goes in by POSITION:")
df["by_pos"] = [7, 8, 9]
print(list(df["by_pos"]))'''),

        ("The filtered-assignment trap",
         "Computing from a subset and assigning back wipes every row that was "
         "not in it.",
         '''import pandas as pd

def fresh():
    d = pd.DataFrame({"city": ["pune", "delhi", "pune"], "sales": [10, 20, 30]})
    d["doubled"] = 0            # a column that already has values
    return d

a = fresh()
sub = a[a["city"] == "pune"]
a["doubled"] = sub["sales"] * 2
print("whole-column assign from a subset:")
print(a)
print("   delhi was 0 and is now NaN - the assignment replaced the")
print("   ENTIRE column, and alignment had nothing for that row.")

b = fresh()
b.loc[b["city"] == "pune", "doubled"] = b["sales"] * 2
print()
print("loc assignment touches only the selected rows:")
print(b)
print("   delhi kept its 0.")'''),

        ("Dropping columns and rows",
         "The same method, steered by axis - and it returns a new frame by default.",
         '''import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3, 4], "c": [5, 6]})

print("drop a column:", list(df.drop(columns=["b"]).columns))
print("drop a row   :", list(df.drop(index=[0]).index))
print("original     :", list(df.columns), "<- unchanged")
print()
print("axis= works too, but columns=/index= say what you mean:")
print("   ", list(df.drop("b", axis=1).columns))
print()
print("a missing name raises, unless you say otherwise:")
try:
    df.drop(columns=["zzz"])
except KeyError as e:
    print("    KeyError:", str(e)[:40])
print("   errors='ignore':", list(df.drop(columns=["zzz"], errors="ignore").columns))'''),

        ("Renaming, and inserting in a position",
         "rename takes a mapping; insert is the only way to choose where a column "
         "goes.",
         '''import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

print("rename by mapping:", list(df.rename(columns={"a": "alpha"}).columns))
print("rename by function:", list(df.rename(columns=str.upper).columns))
print()
print("unknown keys are ignored silently - a typo just does nothing:")
print("   ", list(df.rename(columns={"zzz": "nope"}).columns))
print()
df.insert(1, "middle", [9, 9])
print("insert(1, ...) puts it at position 1:")
print(df)
print()
print("reorder by selecting in the order you want:")
print(list(df[["b", "middle", "a"]].columns))'''),
    ],
    [
        "<code>df[\"new\"] = ...</code> adds a column at the end, or <strong>silently replaces</strong> one of the same name.",
        "<code>assign</code> returns a new frame and takes lambdas, so it chains &mdash; and each lambda sees the frame as it is at that point.",
        "Assigning a <strong>Series</strong> aligns on the index; assigning a <strong>list</strong> goes in by position.",
        "Assigning a subset-derived Series to a whole column <strong>overwrites</strong> every unmatched row with NaN, even one that held a value. <code>df.loc[mask, \"col\"] = ...</code> touches only the selected rows.",
        "<code>drop(columns=[...])</code> and <code>drop(index=[...])</code> return a new frame; a missing name raises unless <code>errors=\"ignore\"</code>.",
        "<code>rename</code> ignores keys that do not exist, so a typo does nothing. <code>insert</code> is the only way to choose a column's position.",
    ],
    '''
title: Adding and Removing Columns
intro: assign, drop, rename, and the alignment that decides what a new column contains.

## Bracket assignment

`df["total"] = df["qty"] * df["price"]` adds a column at the end.

Two behaviours are worth stating because neither warns.

A **scalar broadcasts**: `df["currency"] = "INR"` fills every row.

An **existing name is replaced**, silently. There is no protection against overwriting a column by reusing its name, which is a real hazard in a long script where the column list is not in front of you.

Column order is insertion order. `insert` is the only way to place one somewhere specific.

## assign

`df.assign(total=...)` returns a **new** frame rather than modifying in place.

That makes it chainable, which is its main purpose:

```python
out = (df
       .assign(total=lambda d: d["qty"] * d["price"])
       .assign(cheap=lambda d: d["total"] < 100))
```

The lambda receives the frame **as it is at that point in the chain**, so the second `assign` can use the column the first one created. Passing a value directly rather than a lambda works too, but then it is computed against the original frame, which breaks in a chain.

`assign` also keeps the original untouched, which is worth something in a notebook where cells get re-run out of order.

The cost is a copy per call. In a hot loop that matters; in ordinary analysis code it does not, and the readability of a chain usually wins.

## Alignment decides the contents

This is the part that surprises people, and it is the index rule again.

Assigning a **Series** aligns on the index. If the Series has the same labels in a different order, pandas reorders it to match &mdash; which is correct and is not what positional intuition expects. If the Series is missing some labels, those rows get `NaN`. If it has extra labels, they are dropped.

Assigning a **list** or a NumPy array has no index to align on, so it goes in by position, and the length must match exactly or it raises.

That difference means `df["x"] = some_series` and `df["x"] = some_series.values` can produce different columns from the same data. The first is usually what you want; the second is the escape hatch when you know the order is right and the labels are not.

## The filtered-assignment trap

The most common real instance:

```python
sub = df[df["city"] == "pune"]
df["doubled"] = sub["sales"] * 2
```

`sub` has only the Pune rows, so the computed Series has only those labels. Alignment fills every other row with `NaN`.

pandas did exactly what it promises. The author expected "compute for these rows and leave the others alone", which is a different operation:

```python
df.loc[df["city"] == "pune", "doubled"] = df["sales"] * 2
```

The difference is visible whenever the column **already exists**. Whole-column assignment replaces the entire column, so rows absent from the subset are overwritten with `NaN` &mdash; even if they held a perfectly good value a moment ago. The `.loc` form touches only the selected rows and leaves the rest alone.

When the column does *not* already exist, both forms leave `NaN` in the unselected rows, because creating a column has to put something in every row. If you want a default there, create the column first and then overwrite the subset &mdash; which is exactly what the editor above does.

## Dropping

`df.drop(columns=["b"])` and `df.drop(index=[0])` both return a new frame.

The `axis=` form works and is older; `columns=`/`index=` say what they mean and are worth preferring.

A name that does not exist raises `KeyError`. That is usually helpful &mdash; it catches typos and stale column lists &mdash; and `errors="ignore"` turns it off when dropping optional columns.

To drop in place, reassign: `df = df.drop(columns=["b"])`. The `inplace=True` argument exists, and is discouraged: it does not reliably avoid a copy, it breaks chaining, and it returns `None`, which makes `df = df.drop(..., inplace=True)` a silent way to destroy your frame.

## Renaming

`df.rename(columns={"a": "alpha"})` takes a mapping, and `columns=str.upper` takes a function applied to every name.

The important quirk: **keys that do not match anything are ignored silently**. A typo in the old name does nothing at all and gives no indication. When a rename appears not to have worked, a misspelled key is the first thing to check.

`df.columns = [...]` replaces every name at once and requires the right length. It is blunter and, for a full rename, clearer.

For cleaning up messy headers, a function is usually better than a mapping:

```python
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
```

That handles the whole frame without listing every column, and is worth running on anything that came from a spreadsheet.

## Adding several columns at once

`assign` takes any number of keyword arguments, and they are applied in order, so later ones can use earlier ones:

```python
df.assign(
    total=lambda d: d["qty"] * d["price"],
    with_tax=lambda d: d["total"] * 1.18,
)
```

For column names that are not valid identifiers &mdash; a space, a leading digit &mdash; keyword arguments will not work, and bracket assignment is the only option. That is a reasonable argument for normalising column names early.

Assigning several columns from one operation is the case `assign` handles less well. When a function returns several values per row, a common pattern is:

```python
df[["a", "b"]] = df["text"].str.split("-", expand=True)
```

The right-hand side must have the same number of columns as the left, and the index must align.

## Reordering

Column order is insertion order, and there is no `reorder` method.

Three ways, in increasing robustness:

`df[["b", "a", "c"]]` &mdash; select in the order you want. Fails loudly if a name is wrong, which is usually a feature.

`df.insert(pos, name, values)` &mdash; place one column at a position, in place.

Building the order from what exists:

```python
first = ["id", "date"]
df = df[first + [c for c in df.columns if c not in first]]
```

That pins the columns you care about to the front and keeps the rest, without breaking when the schema changes.

## Removing columns safely

`drop(columns=[...])` raises on a name that does not exist, which catches typos and stale lists.

`errors="ignore"` suppresses that, and is right when the columns are genuinely optional &mdash; dropping debug fields that may or may not be present.

`df.drop(columns=df.filter(like="tmp_").columns)` drops by pattern, which survives changes in the exact names.

For keeping rather than dropping, selecting is clearer: `df[["a", "b"]]` states what you want rather than what you do not, and does not need updating when new unwanted columns appear.

## A note on inplace

Most of these methods take `inplace=True`. It is worth being clear about why it is discouraged.

It does **not** reliably avoid a copy, so the performance argument for it is largely false.

It returns `None`, so `df = df.drop(columns=["a"], inplace=True)` silently sets `df` to `None` &mdash; a mistake that is easy to make and confusing to debug.

It breaks method chaining.

And it is on the way out: the pandas team has discussed removing it, and copy-on-write makes its remaining rationale weaker.

Reassignment &mdash; `df = df.drop(columns=["a"])` &mdash; is clearer and no slower in practice.

## Renaming, at scale

For one or two columns, a mapping is fine.

For a whole frame that arrived with human-written headers, a function over the Index is better:

```python
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(r"[^a-z0-9]+", "_", regex=True)
              .str.strip("_"))
```

This handles trailing spaces, capitals, punctuation and units-in-parentheses in one pass, and does not need to know what the columns are called.

Doing it immediately after loading means every later reference uses predictable names, and it removes the class of bug where a column name has an invisible trailing space.

`df.rename(columns=..., errors="raise")` makes a mapping strict, so a key that matches nothing raises instead of doing nothing silently. That is worth using when the rename is important.

## Creating columns conditionally

The three standard shapes, none of which needs `apply`:

**Two branches** &mdash; `np.where(cond, a, b)`.

**Several branches** &mdash; `np.select([c1, c2], [v1, v2], default=v3)`, evaluated in order.

**Numeric bands** &mdash; `pd.cut`.

**A lookup** &mdash; `df["k"].map(mapping)`.

For a column that exists only for some rows, create it with a default first and then overwrite the subset:

```python
df["band"] = "unknown"
df.loc[df["score"] >= 80, "band"] = "high"
```

That avoids the `NaN` that appears when a column is created directly for a subset, and it makes the default explicit rather than implied.

## Types when adding a column

A new column takes its dtype from what you assign. Two cases are worth watching.

Assigning a Python list of integers gives `int64`; assigning one with a `None` in it gives `object` or `float64`. If the column is meant to be a nullable integer, say so: `pd.array([1, None], dtype="Int64")`.

Assigning a string to a subset of a numeric column upcasts the **whole** column to `object`, silently, which makes every later numeric operation on it slow or wrong. If a column may hold either, that is usually a sign it should be two columns.

## Dropping rows

`drop(index=[...])` removes by label, which is fine for a handful of known labels and awkward otherwise.

For a condition, filtering is clearer: `df[~mask]` says "everything except", and does not require knowing the labels.

`df.drop(df[mask].index)` works and is a longer way of writing the same thing.

`dropna`, `drop_duplicates` and `query` cover the common cases directly, and each says what it does in its name.

## A summary

`df["new"] = ...` adds or silently replaces.

`assign` returns a new frame and chains; use a lambda inside a chain.

Assigning a **Series** aligns on the index; a **list** goes in by position.

Whole-column assignment from a subset overwrites the unmatched rows with `NaN`; `.loc` touches only the selection.

`drop(columns=...)` raises on a missing name unless `errors="ignore"`.

`rename` ignores keys that match nothing, so a typo does nothing at all.

Normalise column names once, at load, with a function over `df.columns`.

And prefer reassignment to `inplace=True`, which does not do what its name suggests.

## A closing note

Adding a column looks like the simplest thing in pandas and carries two traps.

The first is silence: assigning to an existing name replaces it without a word, and a rename with a misspelled key does nothing without a word. Neither raises, and both are easy to miss in a long script.

The second is alignment. A Series assigned to a column is matched by label, not position, so a value computed from a filtered subset fills the unmatched rows with `NaN` &mdash; and if the column already existed, it overwrites what was there. A plain list, having no index, goes in positionally instead. Two lines that look equivalent behave differently.

The defences are small: use `.loc` when you mean "these rows only", check the column list after a rename, and normalise column names once at load so that later references are predictable.

## One more thing

`df.pop("col")` removes a column and returns it, which is occasionally the clearest way to move a column out of a frame and into a variable in one step.

And `df.drop` accepts `level=` for a MultiIndexed frame, so a whole outer group can be removed by label without building a mask. Both are small conveniences, and both read better than the two-step alternatives when the intent is exactly what they describe.

## In summary

Adding and removing columns is mechanically simple, and the two things that bite are both about silence.

Nothing warns when you overwrite a column by reusing its name, and nothing warns when a rename key matches nothing. Both leave the frame in a state that looks correct.

And assignment is governed by alignment: a Series matches on labels, a list matches on position, and a whole-column assignment computed from a subset overwrites every unmatched row with `NaN` &mdash; including rows that held a perfectly good value a moment before.

Using `.loc` when you mean "these rows only", normalising column names once at load, and checking the column list after a rename cover all of it.
''',
    [
        {"q": "What happens when you assign to an existing column name?",
         "options": ["It raises", "It is silently replaced", "It creates a duplicate", "It warns"],
         "answer": 1,
         "why": "There is no protection against overwriting a column by reusing its name - a real hazard in a long script."},
        {"q": "You assign a Series whose index is in a different order. What lands in the column?",
         "options": ["The values in their original order", "The values reordered to match the frame's index", "NaN", "An error"],
         "answer": 1,
         "why": "Assigning a Series aligns by label; assigning a plain list goes in by position. That is why .values sometimes gives a different result."},
        {"q": "An existing column holds 0 everywhere. What does `df['x'] = df[mask]['y'] * 2` do to the unmatched rows?",
         "options": ["Leaves them at 0", "Overwrites them with NaN, because it replaces the whole column", "Raises", "Drops them"],
         "answer": 1,
         "why": "Whole-column assignment replaces the entire column and alignment has nothing for those labels. df.loc[mask, 'x'] = ... touches only the selected rows."},
        {"q": "What does `df.rename(columns={'typo': 'new'})` do when 'typo' does not exist?",
         "options": ["Raises KeyError", "Nothing at all, silently", "Creates the column", "Warns"],
         "answer": 1,
         "why": "Unmatched keys are ignored. When a rename appears not to have worked, a misspelled key is the first thing to check."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Dtypes and memory
# ---------------------------------------------------------------------------
topic(
    "dtypes_and_memory",
    "Dtypes and Memory",
    "Cleaning Data",
    "object, category and the nullable types - and why one text column can cost "
    "more than the rest of the frame.",
    _svg(_box(16, 30, 40, 30, S, "#a44") + _txt(36, 49, "object", "#e88", 8) +
         _arrow(60, 45, 78, 45) +
         _box(86, 34, 34, 22, S, A) + _txt(103, 48, "category", A, 7)),
    [
        ("Every column has a dtype",
         "And the ones inferred from messy data are often not the ones you want.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "i": [1, 2, 3],
    "f": [1.5, 2.5, 3.5],
    "s": ["a", "b", "c"],
    "b": [True, False, True],
    "missing_int": [1, 2, np.nan],
})
print(df.dtypes)
print()
print("Two to notice:")
print("  s           -> object: a column of POINTERS to Python strings")
print("  missing_int -> float64: NumPy ints cannot hold NaN")'''),

        ("object columns are expensive",
         "The default memory report does not tell you the truth about them.",
         '''import pandas as pd

n = 30_000
df = pd.DataFrame({
    "num": range(n),
    "city": ["pune", "delhi", "mumbai", "goa"] * (n // 4),
})

shallow = df.memory_usage().sum()
deep = df.memory_usage(deep=True).sum()
print("memory_usage()          : %8.1f KB" % (shallow / 1e3))
print("memory_usage(deep=True) : %8.1f KB" % (deep / 1e3))
print()
print("per column, deep:")
print((df.memory_usage(deep=True) / 1e3).round(1))
print()
print("The shallow number counts 8 bytes per pointer. The deep one")
print("follows the pointers and counts the strings themselves.")'''),

        ("category, for repeated text",
         "Store each distinct value once and keep small integer codes per row.",
         '''import pandas as pd

n = 30_000
s = pd.Series(["pune", "delhi", "mumbai", "goa"] * (n // 4))
c = s.astype("category")

print("object   : %8.1f KB" % (s.memory_usage(deep=True) / 1e3))
print("category : %8.1f KB" % (c.memory_usage(deep=True) / 1e3))
print("saving   : %.0f%%" % (100 * (1 - c.memory_usage(deep=True) /
                                    s.memory_usage(deep=True))))
print()
print("categories:", list(c.cat.categories))
print("codes     :", list(c.cat.codes[:6]), "...")
print()
print("It only pays when values repeat. Unique values per row cost MORE")
print("as a category, because you store the codes as well as the values.")'''),

        ("Downcasting numbers",
         "int64 is the default and is usually far wider than the data needs.",
         '''import pandas as pd
import numpy as np

s = pd.Series(range(50_000))
print("int64 :", s.memory_usage(deep=True) // 1000, "KB")

small = pd.to_numeric(s, downcast="unsigned")
print("downcast:", small.dtype, small.memory_usage(deep=True) // 1000, "KB")
print()
f = pd.Series(np.linspace(0, 1, 50_000))
print("float64:", f.memory_usage(deep=True) // 1000, "KB")
print("float32:", f.astype("float32").memory_usage(deep=True) // 1000, "KB")
print()
print("Downcast only when the range is known and bounded. An int8 column")
print("that later receives 200 wraps or raises, depending on how it got there.")'''),

        ("Nullable dtypes hold integers AND missing",
         "The capital-I Int64 is a different type from int64.",
         '''import pandas as pd
import numpy as np

plain = pd.Series([1, 2, np.nan])
nullable = pd.Series([1, 2, None], dtype="Int64")

print("plain    :", list(plain), plain.dtype, "<- became float")
print("nullable :", list(nullable), nullable.dtype, "<- stayed integer")
print()
print("the missing marker is pd.NA, not NaN:")
print("   nullable[2] is pd.NA:", nullable[2] is pd.NA)
print()
print("arithmetic propagates it:")
print("   ", list(nullable + 1))
print()
print("Use these when an id or a count must not turn into a float.")'''),

        ("Converting safely",
         "astype raises on bad input; to_numeric can be told what to do instead.",
         '''import pandas as pd

s = pd.Series(["1", "2", "oops", "4"])

try:
    s.astype(int)
except ValueError as e:
    print("astype(int) ->", str(e)[:48])

print()
coerced = pd.to_numeric(s, errors="coerce")
print("to_numeric(errors='coerce'):", list(coerced))
print("   the bad value became NaN instead of stopping everything")
print()
print("find what failed:")
print("   rows that would not convert:", list(s[coerced.isna()]))
print()
print("dtype after coercion:", coerced.dtype)'''),
    ],
    [
        "An <code>object</code> column holds <strong>pointers</strong> to Python objects, so <code>memory_usage()</code> undercounts it badly &mdash; use <code>deep=True</code>.",
        "<code>category</code> stores each distinct value once plus a small code per row, and pays off only when values <strong>repeat</strong>.",
        "<code>int64</code> is the default and usually far wider than needed; <code>pd.to_numeric(..., downcast=...)</code> narrows it.",
        "Nullable <strong><code>Int64</code></strong> (capital I) holds integers and missing values together, using <code>pd.NA</code> rather than NaN.",
        "A plain integer column with one missing value becomes <code>float64</code>, which is why ids print as <code>1001.0</code>.",
        "<code>astype</code> raises on bad input; <code>pd.to_numeric(s, errors=\"coerce\")</code> turns the failures into NaN so you can find them.",
    ],
    '''
title: Dtypes and Memory
intro: object, category and the nullable types.

## Why this matters early

A frame that does not fit in memory cannot be analysed at all, and the usual reason a frame is larger than expected is not the number of rows. It is one or two columns stored in the widest possible type.

Fixing dtypes is often the difference between a dataset that loads and one that does not, and it takes one line per column.

## object is the expensive one

A column of strings has dtype `object`. That means an array of **pointers**, each leading to a separate Python string somewhere else in memory.

Two costs follow. The obvious one is memory: a pointer plus a Python string object plus the characters, against a few bytes for a number. The less obvious one is speed &mdash; operations on object columns fall back to per-element Python, which is the same reason `apply` is slow.

`df.memory_usage()` reports **8 bytes per pointer** and stops there. For a text column that is a wild underestimate. `df.memory_usage(deep=True)` follows the pointers and reports the truth, and the gap between the two numbers is often a factor of ten.

`df.info(memory_usage="deep")` gives the same accounting alongside the dtypes.

Always use `deep=True` when looking at a frame with text in it. The shallow number is close to meaningless there.

## category

When a text column has few distinct values relative to its length &mdash; a city, a status, a product code &mdash; `category` is the fix.

It stores the distinct values once in a lookup, and one small integer code per row. A column of 30,000 rows drawn from four cities goes from storing 30,000 strings to storing four strings and 30,000 one-byte codes.

The savings are large, and they compound: group-by and comparison on a category are faster too, because they operate on the codes.

The condition is repetition. A column where every value is distinct &mdash; an email address, a UUID &mdash; costs **more** as a category, because you store the codes in addition to all the original values. The rule of thumb is that it pays when the number of distinct values is well under half the row count, and it pays enormously when it is a tiny fraction.

Two behaviours to know. Categories carry an order if you give them one, which is what makes sorting by a grade or a size work properly. And operations that produce a value outside the category set give `NaN` rather than extending the set, which is occasionally surprising and generally the safer default.

## Downcasting numbers

`int64` holds numbers up to about 9.2 quintillion. A column of ages does not need that.

`pd.to_numeric(s, downcast="integer")` picks the narrowest signed type that fits; `downcast="unsigned"` does the same for non-negative data, and `downcast="float"` gives `float32`.

The saving is up to 8x for integers and 2x for floats.

The caution is the same as NumPy's: narrow integer types **wrap silently** on overflow. Downcast when the range is genuinely bounded &mdash; ages, day-of-month, a small enum &mdash; and leave counters and identifiers alone. An `int8` column that later receives 200 does not give you 200.

## Nullable dtypes

The oldest wart in pandas is that a NumPy integer array cannot represent a missing value, so an integer column with one gap becomes `float64` and identifiers start printing as `1001.0`.

The nullable extension types fix this. `Int64` with a **capital I** is a different dtype from `int64`, and it holds integers and missing values together. The missing marker is `pd.NA` rather than `np.nan`.

`Float64`, `boolean` and `string` are the equivalents for the other kinds. The nullable `boolean` is genuinely useful, because plain `bool` columns also collapse to `object` when they gain a missing value.

They are not the default, and there are corners where a library downstream expects NumPy types and does not handle them. But for identifiers and counts that must not become floats, they are the right answer.

`pd.NA` propagates through arithmetic like NaN, and comparisons with it return `pd.NA` rather than `False` &mdash; a difference from NaN that matters if you are filtering on such a column.

## Converting safely

`astype(int)` raises on the first value it cannot convert, and the message does not tell you which row.

`pd.to_numeric(s, errors="coerce")` converts what it can and turns the rest into `NaN`. That is usually the better tool for real data, because it lets you find the offenders:

```python
converted = pd.to_numeric(s, errors="coerce")
bad = s[converted.isna() & s.notna()]
```

Those are the rows that were present and unconvertible &mdash; the stray `"N/A"`, the number with a thousands separator, the value with a trailing space.

`errors="raise"` is the default and is right when the data is supposed to be clean and you want to know immediately if it is not.

## A practical routine

After loading anything:

```python
df.info(memory_usage="deep")
```

Then, for each `object` column, `nunique()` against `len(df)`. Anything with heavy repetition becomes a `category`. Anything numeric-looking gets `to_numeric`. Anything that is an identifier gets `str` at read time so its leading zeros survive.

That is usually a handful of lines, and on a large frame it routinely cuts memory by more than half.

## Seeing where the memory goes

`df.memory_usage(deep=True).sort_values(ascending=False)` ranks the columns. On most real frames one or two text columns dominate, and everything else is noise.

That ranking tells you where to spend effort. Converting a column that holds 2% of the memory is not worth the risk of changing a dtype.

`df.info(memory_usage="deep")` gives the same information alongside dtypes and null counts, which is usually the more convenient single call.

## Categories in more detail

`astype("category")` builds the category set from the values present.

Two consequences follow from the set being fixed.

**Assigning a value outside the set fails** or produces `NaN`, depending on the operation. Adding a new city to a categorical column requires `cat.add_categories` first.

**Combining two categoricals with different sets** gives `object` unless the sets match. This bites when concatenating frames from different files, each of which saw a different subset of the categories. `pd.api.types.union_categoricals` handles it, or convert after concatenating rather than before.

`cat.set_categories([...], ordered=True)` gives an order, which is what makes sorting by size or grade work correctly rather than alphabetically. `cat.as_ordered()` and comparison operators then behave as you would expect.

`cat.remove_unused_categories()` shrinks the set after filtering, which otherwise keeps every original category and can leave empty groups in a group-by.

Group-by on a categorical includes **every** category by default, even absent ones, producing rows of zeros. `observed=True` restricts it to categories actually present, and it is worth passing deliberately since the default has changed across versions.

## What float32 costs

`float32` halves memory and keeps about seven significant digits.

For data that came from a sensor with three, that is ample. For accumulating a long sum it is not, and the fix is to accumulate in a wider type: `s.sum(dtype="float64")` reads a narrow column and adds in a wide accumulator.

`float16` exists and is rarely a good idea outside deep learning &mdash; three significant digits is not much, and most operations upcast it anyway.

## Nullable types in practice

The extension types &mdash; `Int64`, `Float64`, `boolean`, `string` &mdash; fix the missing-value gaps in the NumPy-backed dtypes.

Three practical notes.

`pd.NA` propagates through comparisons as `pd.NA` rather than `False`. Filtering a nullable column therefore needs care: `df[df["x"] > 1]` drops the missing rows either way, but a mask containing `pd.NA` cannot always be used directly, and `.fillna(False)` on the mask is the fix.

Some libraries downstream expect NumPy dtypes and do not handle extension types. Converting back with `astype("float64")` at the boundary is sometimes necessary.

`convert_dtypes()` converts a whole frame to the best available nullable types in one call, which is a quick way to see what it would look like.

## A conversion routine

After loading, and before anything else:

```python
for c in df.select_dtypes("object"):
    if df[c].nunique() / len(df) < 0.5:
        df[c] = df[c].astype("category")

for c in df.select_dtypes("integer"):
    df[c] = pd.to_numeric(df[c], downcast="integer")
```

Two loops, run once, that routinely halve the memory of a real frame.

The threshold is a judgement rather than a rule. Well under half distinct is a clear win; near half is marginal; mostly distinct is a loss.

And the general principle from the numpy track applies here too: set the dtype as early as possible, ideally at read time, because every conversion afterwards allocates a second copy of the column.

## A diagnosis routine

When a frame is unexpectedly large or slow, four lines find the cause:

```python
df.info(memory_usage="deep")
df.memory_usage(deep=True).sort_values(ascending=False).head()
df.select_dtypes("object").nunique()
df.select_dtypes("object").apply(lambda s: s.str.len().mean())
```

The first two find which columns dominate. The third says whether they are candidates for `category` &mdash; low cardinality &mdash; or identifiers that will not benefit. The fourth shows average string length, which explains a column that is large despite having few rows.

Almost always the answer is one or two `object` columns, and almost always one of them should be a category.

## dtype mistakes that cause wrong answers

Memory is the visible cost. These are the ones that change results.

**An identifier read as an integer** loses leading zeros, and two different ids can collide once the zeros are gone.

**A numeric column stored as `object`** compares as strings: `"100" < "20"` is True. Sorting, comparison and `max` all silently give the wrong answer, and nothing raises.

**A narrow integer that overflows** wraps. `int8` holding 200 does not hold 200.

**Mixed types in one column** make it `object`, and any aggregation either fails or produces something meaningless.

**A float used as a key** in a merge or a group-by. Floating-point equality is unreliable, and two values that print identically may not match.

Each of these is caught by looking at `dtypes` immediately after loading, which is why that habit appears in three separate modules.

## When to convert

**At read time** if you can &mdash; `dtype=` in `read_csv`. No extra copy, no window where the column is wrong.

**Immediately after loading** otherwise, before any analysis, so every later operation sees the right types.

**Not repeatedly.** Each `astype` allocates a full copy of the column. Converting inside a function that runs per group or per file is a common and invisible cost.

## A summary

Text columns hold pointers; use `deep=True` to see their real size.

`category` for repeated values, and only for repeated values.

Downcast numerics when the range is genuinely bounded.

`Int64`, `boolean` and `string` hold missing values without changing type.

`to_numeric(errors="coerce")` converts what it can and shows you what it could not.

Set types as early as possible, and check `dtypes` right after loading &mdash; it is one line and it prevents a category of silent wrongness.

## A closing note

Dtypes are the quiet determinant of whether a pandas script is fast, correct, and able to load its data at all.

The memory story is simple: text columns hold pointers to Python strings and dominate most real frames, `category` collapses them when values repeat, and narrow numeric types halve or quarter the rest. Two loops run once after loading routinely cut a frame's footprint in half.

The correctness story matters more. A numeric column stored as `object` compares as strings, so `"100" < "20"` is true and every sort and maximum is silently wrong. An identifier read as an integer loses its leading zeros permanently. An integer column with one gap becomes float, and ids start printing with a decimal point.

None of those raise. All of them are visible in one line of `df.dtypes`, run immediately after loading &mdash; which is why that habit appears in several modules and is worth more than any other single check in this track.
''',
    [
        {"q": "Why does `memory_usage()` undercount a text column?",
         "options": ["It is buggy", "It counts 8 bytes per pointer without following them to the strings", "Text is compressed", "It ignores the column"],
         "answer": 1,
         "why": "Use deep=True, which follows the pointers. The gap between the two numbers is often a factor of ten."},
        {"q": "When does converting a column to `category` cost more than it saves?",
         "options": ["Never", "When the values are mostly distinct, since you store codes as well as values", "On numeric data only", "When the frame is small"],
         "answer": 1,
         "why": "It pays when distinct values are well under half the row count, and enormously when they are a tiny fraction."},
        {"q": "What is the difference between `int64` and `Int64`?",
         "options": ["Nothing", "Int64 is nullable - it holds integers and missing values together using pd.NA", "Int64 is faster", "Int64 is 128-bit"],
         "answer": 1,
         "why": "It fixes the oldest wart in pandas: a plain integer column with one gap becomes float64, so ids print as 1001.0"},
        {"q": "How do you convert a messy text column to numbers without stopping at the first bad value?",
         "options": ["astype(int)", "pd.to_numeric(s, errors='coerce')", "astype(float)", "s.map(int)"],
         "answer": 1,
         "why": "It turns failures into NaN so you can find them: s[converted.isna() & s.notna()] gives the rows that were present and unconvertible."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Missing data
# ---------------------------------------------------------------------------
topic(
    "missing_data",
    "Missing Data",
    "Cleaning Data",
    "NaN, None and pd.NA - finding them, counting them, and the choice that "
    "matters more than the code.",
    _svg(_grid(20, 30, 5, 1, 15) +
         _box(50, 30, 15, 15, "#3a1f1f", "#a44") +
         _box(80, 30, 15, 15, "#3a1f1f", "#a44") +
         _txt(80, 62, "isna / fillna / dropna", M, 8)),
    [
        ("Three markers, one test",
         "<code>isna</code> catches all of them, whatever the dtype.",
         '''import pandas as pd
import numpy as np

f = pd.Series([1.0, np.nan, 3.0])
o = pd.Series(["a", None, "c"])
n = pd.Series([1, None, 3], dtype="Int64")

for name, s in [("float + NaN", f), ("object + None", o), ("Int64 + NA", n)]:
    print("%-14s dtype %-8s isna: %s" % (name, str(s.dtype), list(s.isna())))

print()
print("None became NaN in the float column:", repr(f[1]))
print("None stayed None in the object column:", repr(o[1]))
print("Int64 uses pd.NA:", repr(n[1]))
print()
print("isna() is the one test that works for all three.")'''),

        ("Counting before deciding",
         "Per column, as a share, and how many rows you would lose.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "a": [1, np.nan, 3, 4, 5],
    "b": [np.nan, np.nan, np.nan, 4, 5],
    "c": [1, 2, 3, 4, 5],
})
print("count per column:"); print(df.isna().sum())
print()
print("share per column:"); print((df.isna().mean() * 100).round(0))
print()
rows_lost = int(df.isna().any(axis=1).sum())
print("rows with any missing :", rows_lost, "of", len(df),
      "(%.0f%%)" % (100 * rows_lost / len(df)))
print()
print("Dropping rows loses 40% here, and column b is 60% empty.")
print("Those two numbers decide the strategy, not a rule of thumb.")'''),

        ("dropna, and how much it takes",
         "The default is stricter than people expect.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "a": [1, np.nan, 3],
    "b": [np.nan, 2, 3],
})
print("original:"); print(df)
print()
print("dropna() drops a row if ANY value is missing:")
print(df.dropna())
print()
print("how='all' only drops rows that are entirely missing:")
print(df.dropna(how="all"))
print()
print("thresh=1 keeps rows with at least 1 real value:")
print(df.dropna(thresh=1))
print()
print("subset limits which columns count:")
print(df.dropna(subset=["a"]))'''),

        ("fillna, and what each choice costs",
         "Filling is never neutral - it puts numbers in that were not measured.",
         '''import pandas as pd
import numpy as np

s = pd.Series([10.0, np.nan, np.nan, 40.0, 50.0])
print("original    :", list(s))
print("mean of real :", round(float(s.mean()), 2))
print()
zero = s.fillna(0)
mean = s.fillna(s.mean())
print("fillna(0)   :", list(zero), " mean now", round(float(zero.mean()), 2))
print("fillna(mean):", [round(v, 1) for v in mean],
      " mean now", round(float(mean.mean()), 2))
print()
print("std of real  :", round(float(s.std()), 2))
print("std after mean-fill:", round(float(mean.std()), 2), "<- shrunk")
print()
print("Zero moves the mean. The mean keeps it and shrinks the spread.")'''),

        ("Filling from neighbours",
         "For ordered data, the value before or after is often the honest guess.",
         '''import pandas as pd
import numpy as np

s = pd.Series([1.0, np.nan, np.nan, 4.0, np.nan],
              index=pd.date_range("2024-01-01", periods=5))

print("original :", [None if pd.isna(v) else v for v in s])
print("ffill    :", list(s.ffill()))
print("bfill    :", list(s.bfill()))
print("interpolate:", [round(v, 2) for v in s.interpolate()])
print()
print("ffill leaves a leading gap unfilled, bfill a trailing one:")
print("   ffill first value:", s.ffill().iloc[0])
print()
print("limit caps how far a fill travels:")
print("   ffill(limit=1):", [None if pd.isna(v) else v for v in s.ffill(limit=1)])'''),

        ("Missing is sometimes the signal",
         "Recording that a value was absent can matter more than replacing it.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "income": [100.0, np.nan, 300.0, np.nan, 500.0],
    "responded": [1, 0, 1, 0, 1],
})
df["income_missing"] = df["income"].isna().astype(int)

print(df)
print()
corr = df["income_missing"].corr(df["responded"])
print("correlation between 'was missing' and 'responded': %.2f" % corr)
print()
print("-1.00 is a perfect NEGATIVE correlation: income is missing")
print("exactly when the person did not respond. Filling it with the")
print("mean would erase the most informative thing in the column.")'''),
    ],
    [
        "<code>NaN</code>, <code>None</code> and <code>pd.NA</code> are three markers; <code>isna()</code> is the one test that catches all of them.",
        "Count before deciding: <code>isna().sum()</code> per column, <code>isna().mean()</code> as a share, and <code>isna().any(axis=1).sum()</code> for rows you would lose.",
        "<code>dropna()</code> drops a row if <strong>any</strong> value is missing. <code>how</code>, <code>thresh</code> and <code>subset</code> loosen that.",
        "Filling with <strong>zero</strong> moves the mean; filling with the <strong>mean</strong> keeps it and shrinks the variance. Neither is neutral.",
        "<code>ffill</code>/<code>bfill</code> carry neighbouring values and take a <code>limit</code>; <code>interpolate</code> fits between them.",
        "Missingness is often <strong>informative</strong> &mdash; an indicator column can carry more signal than any fill value.",
    ],
    '''
title: Missing Data
intro: Finding it, counting it, and the choice that matters more than the code.

## Three markers

pandas has more than one representation of "missing", for historical reasons.

`np.nan` is a float. It is what you get in numeric columns, and it is why an integer column with a gap becomes `float64`.

`None` is Python's null. In an `object` column it stays `None`; in a float column it is converted to `NaN` on the way in.

`pd.NA` is the newer, dtype-agnostic marker used by the nullable extension types (`Int64`, `boolean`, `string`).

You rarely need to care which one you have, because `isna()` and `notna()` handle all three. Use them rather than `== None` or `== np.nan`, neither of which works &mdash; `NaN` is not equal to anything, including itself.

The one place the difference bites: comparisons with `pd.NA` return `pd.NA` rather than `False`, so filtering a nullable column can behave differently from filtering a float one.

## Count first

Before choosing a strategy, get three numbers:

`df.isna().sum()` &mdash; how many are missing in each column.

`df.isna().mean()` &mdash; the same as a proportion, which is far easier to judge.

`df.isna().any(axis=1).sum()` &mdash; how many rows would be lost to `dropna()`. This is usually much larger than any single column's count, because different rows are missing different things.

Those three numbers make the decision. Dropping 2% of rows is a rounding error; dropping 40% changes what the dataset is. A column that is 60% empty probably should not be used at all, and no amount of imputation fixes that.

## dropna

The default is stricter than most people expect: `df.dropna()` drops a row if **any** value in it is missing.

`how="all"` only drops rows that are entirely empty, which is the right tool for trailing junk from a spreadsheet export.

`thresh=n` keeps rows with at least `n` non-missing values.

`subset=["a", "b"]` only considers those columns, which is usually what you actually want &mdash; you care that the key fields are present, not that every optional field is.

`axis=1` drops columns rather than rows, which is the blunt way to remove mostly-empty fields.

## fillna

The code is easy. The choice is a statistical decision, and it is not neutral.

**Zero** shifts the mean toward zero. For a count where missing genuinely means none, it is correct. For a measurement where missing means unknown, it invents data and biases every summary.

**The mean** preserves the mean by construction and **shrinks the variance**, because you are adding points with no spread. Anything downstream that cares about dispersion &mdash; a standard deviation, a confidence interval, a model that weights by variance &mdash; is then quietly wrong. The fourth editor measures this.

**The median** is more robust to outliers and has the same variance problem.

**A sentinel** like `-1` is honest for categorical codes but must be documented, or someone will average it.

**Group-wise fills** &mdash; filling with the mean of the same city, or the same product &mdash; are usually better than a global fill, because they use information you actually have.

## Filling from neighbours

For ordered data, adjacency carries meaning and the neighbouring value is often the best guess.

`ffill()` carries the last known value forward. This is the standard treatment for a sensor reading or a price that is only recorded when it changes.

`bfill()` carries the next value backward.

Both leave an edge unfilled &mdash; `ffill` cannot fill a leading gap, `bfill` cannot fill a trailing one &mdash; which is worth checking rather than assuming the column is now complete.

`limit=n` caps how far a value travels. Without it, a single reading can propagate across a gap of any length, which turns one measurement into a hundred fabricated ones.

`interpolate()` fits between the surrounding values rather than repeating one, and takes a `method` for the shape of the fit. It needs a meaningful order, so it belongs on time series and not on arbitrary rows.

Note that `fillna(method="ffill")` is deprecated; `ffill()` is the current spelling.

## Missingness as information

The most commonly missed point: **why** a value is absent often matters more than what you replace it with.

If a value is missing at random, dropping or imputing is defensible. If it is missing *because of what it would have been* &mdash; a sensor that fails at extremes, an income question people skip when the answer is embarrassing, a test not run because the patient was too ill &mdash; then both dropping and imputing bias the result, in opposite directions.

The last editor shows the extreme case: a column that is missing exactly when another column takes a particular value. Filling it with the mean would erase the most informative thing in the data.

Adding an indicator column &mdash; `df["x_missing"] = df["x"].isna().astype(int)` &mdash; keeps that information while still allowing a fill. It costs one column and is frequently the single most useful feature in a model built on messy data.

## A working order

Count. Look at *which* rows are missing, not just how many. Ask whether the missingness looks random. Add an indicator if it does not. Then choose a fill, and write down which one you used &mdash; because by the time someone asks, the code will have moved on.

## Where missing values come from

Knowing the source usually tells you what to do.

**Not collected** &mdash; the question was not asked, the sensor was not installed. Often missing at random; dropping is defensible.

**Not applicable** &mdash; a spouse's name for an unmarried person. Not missing at all; a sentinel or a separate flag is more honest than `NaN`.

**Failed** &mdash; a sensor error, a timeout. Frequently correlated with the value, and therefore not missing at random.

**Created by an operation** &mdash; a join that did not match, an alignment mismatch, a `shift`, a `pct_change` on the first row, a value outside a `cut` range. These are the ones people mistake for data problems when they are really code problems.

That last category is worth checking first. If a column gained missing values partway through a pipeline, the cause is upstream in the code, not in the source data.

## Missing values in operations

Most aggregations **skip** missing values by default: `sum`, `mean`, `max` all use `skipna=True`.

That is different from NumPy, where a single `NaN` poisons the whole reduction, and it is worth knowing because it changes the denominator. `df["x"].mean()` divides by the number of **present** values, not the row count.

`skipna=False` makes them propagate, which is occasionally what you want when a missing value should invalidate the result.

`sum()` of an all-missing column returns `0`, not `NaN`, which is defensible and surprising. `min_count=1` makes it return `NaN` instead.

`groupby` **drops** rows whose key is missing, unless `dropna=False`.

`merge` treats `NaN` keys as non-matching in most cases.

Sorting puts them last regardless of direction.

Each of these is reasonable in isolation; together they mean missing data quietly changes several numbers at once, and the totals stop reconciling.

## Filling within groups

A global fill uses the least information available. A group fill uses more:

```python
df["temp"] = df["temp"].fillna(df.groupby("city")["temp"].transform("mean"))
```

Each missing temperature gets the mean for its own city rather than the mean of everywhere.

The same pattern works with `median`, with `ffill` inside a group (`df.groupby("id")["v"].ffill()`), and with a lookup from another table.

A group fill leaves gaps where a whole group is missing, so a global fallback afterwards is often needed:

```python
filled = df.groupby("city")["temp"].transform("mean")
df["temp"] = df["temp"].fillna(filled).fillna(df["temp"].mean())
```

## Documenting what you did

The part that is easy to skip and matters most later.

Record, in the code and in whatever the output is:

How many values were missing per column, before you touched them.

What you did &mdash; dropped, filled with what, interpolated how.

Whether you added an indicator.

The reason is that a filled value is indistinguishable from a measured one once it is in the frame. Six months later, nobody can tell which numbers were observed and which were invented, and the analysis cannot be reproduced or corrected.

A frame with an `x_imputed` boolean column carries that information with the data, which is more robust than a comment.

## The order to work in

Count them. Look at which rows they are in. Decide whether the missingness looks random. Add an indicator if it does not. Choose a strategy for each column separately &mdash; there is no reason the same one suits every column. Record what you did. Then proceed.

## Missing values that pandas created

Worth a separate checklist, because these are code problems rather than data problems and the fix is upstream.

**A join that did not match** &mdash; the added columns are `NaN` for unmatched rows. `indicator=True` confirms it.

**Alignment on assignment** &mdash; a Series with different labels assigned to a column fills the unmatched rows.

**`shift`, `diff`, `pct_change`** &mdash; the first row of each has no predecessor.

**`rolling`** &mdash; leading rows before the window fills.

**`cut` or `qcut`** &mdash; values outside the bin edges.

**`reindex` or `unstack`** &mdash; combinations that did not occur in the data.

**`resample` upsampling** &mdash; periods with no observation.

If a column gained missing values partway through a pipeline, one of these is the cause, and filling them is treating a symptom.

## Interpolation options

`interpolate()` defaults to `method="linear"`, which treats the values as evenly spaced regardless of the index.

`method="time"` uses the actual time gaps, which is what you want on an irregular time series &mdash; without it, a value after a three-week gap is weighted the same as one after an hour.

`method="nearest"`, `"polynomial"`, `"spline"` fit other shapes; the last two need an `order`.

`limit_direction` controls whether leading and trailing gaps are filled. By default `interpolate` fills forward only, so a leading `NaN` survives.

`limit_area="inside"` restricts filling to gaps between real observations, which is usually the honest choice &mdash; interpolating beyond the ends of your data is extrapolation, and it should be a deliberate decision rather than a default.

## Choosing per column

There is no reason one strategy suits every column, and treating them uniformly is usually wrong.

An **identifier** with gaps is a data problem; the rows probably cannot be used.

A **category** can take an explicit `"unknown"` level, which is honest and keeps the rows.

A **count** where missing means none takes zero.

A **measurement** takes a group mean, an interpolation, or nothing &mdash; depending on why it is missing.

A **timestamp** rarely takes a fill at all; a missing date usually means the event did not happen.

Writing the decision down per column, in code, is more maintainable than a single `fillna(0)` across the frame &mdash; which is the most common and least defensible choice.

## A summary

`isna()` finds all three markers; equality never works.

Count per column, as a share, and count the rows you would lose, before deciding anything.

`dropna()` drops on **any** missing value; `subset=` is usually what you want.

Zero shifts the mean; the mean shrinks the variance; neither is neutral.

`ffill`/`bfill` for ordered data, with a `limit`.

`interpolate(method="time")` for irregular series.

Group fills use information a global fill discards.

Add an indicator when missingness might be informative &mdash; it often is.

And record what you did, because a filled value is indistinguishable from a measured one the moment it enters the frame.

## A closing note

Handling missing data is the part of this track where the code is easiest and the decisions are hardest.

`isna`, `dropna` and `fillna` take a few minutes to learn. What they cannot tell you is whether the values are missing at random, whether the rows you are about to drop share something, or whether filling with a mean is defensible for this particular column.

Those are questions about the data rather than about pandas, and the honest answer is often that missingness is informative &mdash; that a value is absent precisely because of what it would have been. In that case both dropping and imputing bias the result, and an indicator column preserves the signal that filling would erase.

The practical minimum is: count them per column and as a share, look at which rows they are in, choose per column rather than uniformly, and record what you did &mdash; because once a filled value is in the frame, nothing distinguishes it from a measured one.
''',
    [
        {"q": "Which test finds NaN, None and pd.NA alike?",
         "options": ["== None", "== np.nan", "isna()", "is null"],
         "answer": 2,
         "why": "NaN is not equal to anything including itself, so equality tests never work. isna() handles all three markers."},
        {"q": "What does the default `df.dropna()` do?",
         "options": ["Drops rows that are entirely empty", "Drops a row if any value in it is missing", "Drops columns", "Fills with zero"],
         "answer": 1,
         "why": "Stricter than most people expect. how='all', thresh= and subset= loosen it, and subset is usually what you actually want."},
        {"q": "What does filling with the column mean do to the variance?",
         "options": ["Nothing", "Shrinks it, because the added points have no spread", "Increases it", "Sets it to zero"],
         "answer": 1,
         "why": "The mean is preserved by construction, so it looks harmless - but anything downstream relying on dispersion is quietly wrong."},
        {"q": "Why add an `x_missing` indicator column?",
         "options": ["To save memory", "Because missingness is often informative, and filling erases it", "It is required by pandas", "To speed up dropna"],
         "answer": 1,
         "why": "When a value is missing because of what it would have been, both dropping and imputing bias the result. The indicator keeps that signal."},
    ],
)


# ---------------------------------------------------------------------------
# 11. Duplicates
# ---------------------------------------------------------------------------
topic(
    "duplicates",
    "Duplicates",
    "Cleaning Data",
    "Finding repeated rows, deciding which one to keep, and the subset argument "
    "that does the real work.",
    _svg(_grid(24, 26, 1, 4, 14) + _txt(31, 22, "rows", M, 8) +
         _box(24, 40, 14, 14, "#3a1f1f", "#a44") +
         _arrow(48, 46, 66, 46) +
         _grid(76, 33, 1, 3, 14)),
    [
        ("duplicated flags the repeats, not the original",
         "The first occurrence is False by default, which is what makes it a "
         "drop mask.",
         '''import pandas as pd

df = pd.DataFrame({
    "name": ["ana", "raj", "ana", "kim", "raj"],
    "city": ["pune", "delhi", "pune", "goa", "delhi"],
})
print(df.assign(dup=df.duplicated()))
print()
print("total duplicated rows:", int(df.duplicated().sum()))
print()
print("keep='last' flags the earlier ones instead:")
print(list(df.duplicated(keep="last")))
print("keep=False flags EVERY copy, including the first:")
print(list(df.duplicated(keep=False)))'''),

        ("subset is where the meaning lives",
         "Rows are rarely duplicated in every column - usually just in the key.",
         '''import pandas as pd

df = pd.DataFrame({
    "id": [1, 2, 1, 3],
    "name": ["ana", "raj", "ana", "kim"],
    "score": [10, 20, 99, 30],
})
print(df)
print()
print("whole-row duplicates:", int(df.duplicated().sum()),
      "<- none, the scores differ")
print("duplicate ids       :", int(df.duplicated(subset=["id"]).sum()))
print()
print("That is the real question: is 'id' supposed to be unique?")
print(df[df.duplicated(subset=["id"], keep=False)])'''),

        ("drop_duplicates keeps the first by default",
         "So the row you keep depends on the order the frame happens to be in.",
         '''import pandas as pd

df = pd.DataFrame({
    "id": [1, 1, 2],
    "updated": ["2024-01-01", "2024-06-01", "2024-03-01"],
    "score": [10, 99, 20],
})
print("as loaded:")
print(df.drop_duplicates(subset=["id"]))
print()
print("that kept score 10 - the FIRST row, not the newest.")
print()
best = df.sort_values("updated").drop_duplicates(subset=["id"], keep="last")
print("sort first, then keep='last':")
print(best)
print()
print("Deduplication without an explicit sort is a coin flip.")'''),

        ("Duplicates that are not identical",
         "Whitespace and case make two spellings of the same thing.",
         '''import pandas as pd

s = pd.Series(["Pune", "pune ", "PUNE", "delhi"])
print("raw value_counts:")
print(s.value_counts())
print()
clean = s.str.strip().str.lower()
print("after strip().lower():")
print(clean.value_counts())
print()
print("duplicates before:", int(s.duplicated().sum()))
print("duplicates after :", int(clean.duplicated().sum()))
print()
print("Normalise before deduplicating, or you keep four cities.")'''),

        ("Counting instead of dropping",
         "Sometimes the repeat is the data, and you want it aggregated.",
         '''import pandas as pd

orders = pd.DataFrame({
    "customer": ["ana", "raj", "ana", "ana", "kim"],
    "amount": [100, 200, 50, 75, 300],
})
print("how many rows per customer:")
print(orders["customer"].value_counts())
print()
print("collapse them into one row each:")
print(orders.groupby("customer", as_index=False)
      .agg(orders=("amount", "size"), total=("amount", "sum")))
print()
print("Dropping duplicates here would have thrown away real orders.")'''),

        ("Checking uniqueness as an assertion",
         "Cheaper to state the assumption than to debug the join that breaks later.",
         '''import pandas as pd

df = pd.DataFrame({"id": [1, 2, 3], "v": [10, 20, 30]})
dupe = pd.DataFrame({"id": [1, 2, 2], "v": [10, 20, 30]})

for name, frame in [("clean", df), ("with a repeat", dupe)]:
    unique = frame["id"].is_unique
    print("%-14s id unique: %s" % (name, unique))

print()
print("as a hard check:")
try:
    assert dupe["id"].is_unique, "id must be unique"
except AssertionError as e:
    print("   AssertionError:", e)
print()
print("A duplicated key silently multiplies rows in a merge, which is")
print("the subject of a later module and a very common surprise.")'''),
    ],
    [
        "<code>duplicated()</code> flags repeats but <strong>not the first occurrence</strong>, which is what makes it usable as a drop mask.",
        "<code>keep=\"last\"</code> flags the earlier copies; <code>keep=False</code> flags <strong>every</strong> copy, which is what you want for inspection.",
        "<code>subset=</code> carries the meaning &mdash; the real question is usually whether the <em>key</em> is duplicated, not the whole row.",
        "<code>drop_duplicates</code> keeps the first row in the frame's current order, so <strong>sort first</strong> if which one survives matters.",
        "Normalise case and whitespace before deduplicating, or the same value counts as several.",
        "A duplicated key silently multiplies rows in a later merge &mdash; <code>is_unique</code> is worth asserting where uniqueness is assumed.",
    ],
    '''
title: Duplicates
intro: Finding repeated rows and deciding which one to keep.

## duplicated marks the copies

`df.duplicated()` returns a boolean Series: `True` for a row that has been seen before, `False` for its first occurrence.

That asymmetry is deliberate. It means `df[~df.duplicated()]` keeps exactly one of each, and `df[df.duplicated()]` shows you what would be removed.

`keep` controls which occurrence is treated as the original:

`keep="first"` (the default) flags every copy after the first.

`keep="last"` flags every copy before the last.

`keep=False` flags **all** of them, including the first. This is the one to use when inspecting, because it shows you the complete groups rather than half of each.

## subset is the important argument

Whole-row duplicates &mdash; every column identical &mdash; are the easy case and often not the real one.

The question that usually matters is whether a **key** is repeated. Two rows with the same customer id and different scores are not identical rows, but they may well be a data problem.

`df.duplicated(subset=["id"])` asks that question. Combined with `keep=False`, it shows you every conflicting group:

```python
df[df.duplicated(subset=["id"], keep=False)].sort_values("id")
```

That is the first thing to run when a key is supposed to be unique and something downstream suggests it is not.

## Order decides what survives

`drop_duplicates` keeps the first matching row **in the frame's current order**.

That order is whatever the data happened to arrive in. If the rows represent versions of a record and you want the newest, keeping the first is arbitrary &mdash; it will be right sometimes and wrong sometimes, and nothing will tell you which.

Sort deliberately first:

```python
df.sort_values("updated").drop_duplicates(subset=["id"], keep="last")
```

Now "the newest per id" is what the code says, and it does not depend on how the file was written.

This is one of the most common silent errors in data cleaning, because the result always looks plausible: you asked for one row per id and you got one row per id.

## Near-duplicates

Exact matching misses the duplicates that actually occur in real data.

`"Pune"`, `"pune "` and `"PUNE"` are three distinct values to pandas and one city to everyone else. So are `"Ltd"` and `"Ltd."`, or a name with a double space.

Normalise before deduplicating:

```python
df["city"] = df["city"].str.strip().str.lower()
```

`value_counts()` on the column before and after is the quickest way to see how much difference it made, and to spot the variants you had not thought of.

For genuinely fuzzy matching &mdash; misspellings, transpositions &mdash; pandas has nothing built in, and the answer is a dedicated library. But stripping and lowercasing catches the large majority of real cases and costs one line.

## Sometimes the repeat is the data

Not every repeated value is an error. Five orders from the same customer are five orders.

The tell is whether the rows carry independent information. If the duplicate rows differ in a meaningful column, dropping them destroys data; the operation you want is an aggregation:

```python
orders.groupby("customer", as_index=False).agg(
    orders=("amount", "size"),
    total=("amount", "sum"),
)
```

That collapses each customer to one row and keeps what the repeats were telling you.

Reaching for `drop_duplicates` when you meant `groupby` is a quiet way to lose most of a dataset.

## Assert uniqueness where you assume it

`s.is_unique` is a cheap check, and `df.index.is_unique` covers the index.

Where a key is supposed to be unique &mdash; because it is a primary key, or because a later merge depends on it &mdash; an explicit assertion is worth the line:

```python
assert df["id"].is_unique, "id must be unique"
```

The reason is specific: a duplicated key on either side of a `merge` silently multiplies rows. Ten thousand rows join to eleven thousand, nobody notices, and every subsequent sum is inflated. `merge(..., validate="one_to_one")` catches it at the join, and asserting earlier catches it closer to the cause.

## Duplicates as a data-quality signal

A duplicate is rarely just a duplicate. It usually means one of a small number of things, and identifying which changes what you should do.

**A repeated load.** The same file processed twice, or an append that ran again. Whole-row duplicates, exact. Safe to drop.

**A join that multiplied rows.** Duplicates in some columns and not others, appearing only after a merge. The fix is at the merge, not here.

**Genuine repeated events.** Two orders from the same customer. Not duplicates at all; aggregate rather than drop.

**Multiple versions of a record.** Same key, different timestamps. Keep one, and *which* one matters &mdash; sort first.

**Near-duplicates from inconsistent entry.** Same entity, different spelling. Normalise first, or you will keep both.

Running `df.duplicated().sum()` and `df.duplicated(subset=[key]).sum()` and comparing the two numbers usually tells you which case you are in.

## Finding what differs

When a key is duplicated but the rows are not identical, the useful question is which columns disagree:

```python
dupes = df[df.duplicated(subset=["id"], keep=False)].sort_values("id")
```

Sorting by the key puts the conflicting rows next to each other, which makes the differing column obvious by eye on a small number of groups.

For a systematic answer, group by the key and count distinct values per column:

```python
df.groupby("id").nunique().max()
```

Any column with a maximum above 1 disagrees somewhere. That points straight at the columns worth investigating.

## Deduplicating with a rule

"Keep the newest" is the most common rule, and it is two steps:

```python
df.sort_values("updated").drop_duplicates(subset=["id"], keep="last")
```

"Keep the most complete" is a different rule and needs a helper column:

```python
df.assign(filled=df.notna().sum(axis=1))
  .sort_values("filled")
  .drop_duplicates(subset=["id"], keep="last")
```

"Merge the rows" &mdash; taking the first non-missing value of each column &mdash; is a group-by:

```python
df.groupby("id", as_index=False).first()
```

`first()` skips missing values, so it combines partial records rather than picking one. That is often what people actually want when they reach for `drop_duplicates`.

## Duplicated columns and index labels

Duplicate **column names** are legal and cause real confusion: `df["a"]` returns a DataFrame rather than a Series when two columns are called `a`.

`df.columns.duplicated()` finds them, and they usually arrive from a merge with overlapping names or a bad header row.

`df.loc[:, ~df.columns.duplicated()]` keeps the first of each.

Duplicate **index labels** have the same problem for row selection, and `reset_index(drop=True)` is the usual fix.

## Before a join, always

The single highest-value use of everything in this module is the check before a merge:

```python
assert df["id"].is_unique
```

on whichever side is supposed to be unique.

A duplicate there multiplies rows silently, inflates every subsequent total, and is invisible in the output. Checking costs one line, and `merge(..., validate="many_to_one")` makes the check part of the operation itself.

## Duplicates and the index

Row duplicates and **index** duplicates are different problems with different symptoms.

A duplicated index makes `.loc[label]` return several rows where code expects one, breaks `reindex`, and makes some joins raise.

`df.index.is_unique` checks it; `df[df.index.duplicated(keep=False)]` shows the offenders; `reset_index(drop=True)` fixes it when the labels carry no meaning.

Duplicated index labels usually arrive from `concat` without `ignore_index=True`, or from `explode`, or from a group-by result that was reshaped. None of them warns.

## Fuzzy duplicates

Exact matching finds only the easy cases. Real duplicate records differ in ways that require judgement:

Whitespace and case &mdash; fixed by normalising, and worth doing always.

Punctuation &mdash; `"Ltd"` and `"Ltd."`.

Abbreviations &mdash; `"Street"` and `"St"`.

Transpositions and typos &mdash; genuinely fuzzy.

Different formats for the same value &mdash; phone numbers, dates as text.

pandas handles the first two well and the rest not at all. For the rest, the honest options are a normalisation function encoding the domain's conventions, or a dedicated record-linkage library. What does not work is hoping `drop_duplicates` will catch them.

The practical approach: normalise aggressively into a **separate** key column, deduplicate on that, and keep the original values. That way the matching is explicit and the data is not damaged.

## Counting rather than removing

Before dropping anything, it is worth knowing what the duplicates represent:

```python
counts = df["id"].value_counts()
counts[counts > 1]
```

If most keys appear once and a few appear twice, that is probably a data-entry issue. If every key appears exactly three times, the data has a structure you have not accounted for &mdash; three records per entity, perhaps one per year &mdash; and deduplicating would destroy it.

That distinction is not visible from the duplicate count alone, and it changes the correct action completely.

## A summary

`duplicated()` flags repeats but not the first; `keep=False` flags every copy.

`subset=` asks the question that usually matters: is the **key** duplicated?

`drop_duplicates` keeps the first in current order &mdash; sort first if which survives matters.

Normalise case and whitespace before deduplicating.

Repeated rows carrying independent information want `groupby`, not `drop_duplicates`.

`groupby(...).first()` merges partial records rather than picking one.

And assert uniqueness before any merge that depends on it, because a duplicated key there multiplies rows and inflates every total downstream.

## A closing note

The word "duplicate" hides several different situations, and choosing the right action depends on which one you have.

An exact repeated row from a double load can be dropped without thought. Two versions of a record need a sort and a rule about which survives. Repeated events carrying independent information need aggregating, not dropping. Near-duplicates from inconsistent text need normalising first, or they will not be found at all.

The diagnostic that separates them is comparing whole-row duplicates against key duplicates. If the key repeats but the row does not, something differs between the copies, and that difference is the thing to look at before deciding anything.

And the highest-value use of everything here is the check before a join. A duplicated key multiplies rows, inflates every total downstream, and produces output that looks entirely reasonable. One assertion prevents it.

## Two more things worth knowing

`drop_duplicates` accepts `ignore_index=True`, which renumbers the result rather than leaving gaps in the index where rows were removed. Without it the surviving labels are the original ones, which is correct and occasionally surprising when the result is printed.

`df.duplicated()` compares whole rows including `NaN`, and two rows with a missing value in the same column **do** count as duplicates of each other &mdash; unlike almost everywhere else in pandas, where `NaN` never equals `NaN`. That inconsistency is deliberate and useful here, since two identically incomplete rows usually are duplicates.

And for finding duplicates across a subset of columns while keeping the rest, `df.groupby(keys).filter(lambda g: len(g) > 1)` returns every row belonging to a repeated key, which is the inspection view that `keep=False` gives more directly.

## Deduplicating across sources

The hardest version of this problem is not duplicates within one table but the same entity appearing in two.

The steps are always the same, and only the third is difficult.

**Normalise** both sides into a comparable key &mdash; case, whitespace, punctuation, and any domain-specific standardisation.

**Match** on the key, with `merge` or `isin`.

**Decide** what to do with near-matches that the key does not unify.

pandas handles the first two well. The third is record linkage, and it is a genuinely open problem for messy data: the same person may appear with a different spelling, a maiden name, a typo'd date of birth.

The pragmatic middle ground is to match exactly on a normalised key, count how many records fail to match, and inspect a sample of those. Often a small number of normalisation rules &mdash; drop punctuation, standardise abbreviations &mdash; resolves most of them, and the rest are genuinely ambiguous and better flagged for a human than resolved by code.

## In summary

`duplicated` flags every copy but the first, which is what makes it a drop mask; `keep=False` flags them all, which is what you want for inspection.

The question that matters is usually about the **key** rather than the whole row, and `subset=` asks it.

Sort before dropping, or which row survives is arbitrary. Normalise text first, or the same value counts as several. And if the repeated rows carry independent information, the operation you want is an aggregation, not a deletion.
''',
    [
        {"q": "What does `duplicated()` return for the first occurrence of a repeated row?",
         "options": ["True", "False", "NaN", "It raises"],
         "answer": 1,
         "why": "That asymmetry is what makes df[~df.duplicated()] keep exactly one of each. Use keep=False to flag every copy when inspecting."},
        {"q": "Why sort before `drop_duplicates(subset=['id'])`?",
         "options": ["It is faster", "It keeps the first row in the frame's current order, which is otherwise arbitrary", "It is required", "To avoid NaN"],
         "answer": 1,
         "why": "A silent error: you asked for one row per id and got one row per id, but which one depends on how the file happened to be written."},
        {"q": "Five rows share a customer name but have different amounts. What is usually the right operation?",
         "options": ["drop_duplicates", "groupby and aggregate", "dropna", "Nothing"],
         "answer": 1,
         "why": "The rows carry independent information. Reaching for drop_duplicates when you meant groupby is a quiet way to lose most of a dataset."},
        {"q": "Why assert `df['id'].is_unique` before a merge?",
         "options": ["It speeds up the merge", "A duplicated key silently multiplies rows, inflating every later total", "merge requires it", "It sorts the frame"],
         "answer": 1,
         "why": "Ten thousand rows join to eleven thousand and nobody notices. merge(validate='one_to_one') catches it at the join."},
    ],
)


# ---------------------------------------------------------------------------
# 12. Text columns
# ---------------------------------------------------------------------------
topic(
    "string_methods",
    "Text Columns",
    "Cleaning Data",
    "The .str accessor - vectorised string work without a loop, and what it does "
    "with missing values.",
    _svg(_box(18, 28, 46, 34, S) + _txt(41, 49, '" raj "', M, 8) +
         _arrow(68, 45, 86, 45) + _txt(77, 38, ".str", A, 7) +
         _box(94, 28, 46, 34, S, A) + _txt(117, 49, '"raj"', A, 8)),
    [
        ("The .str accessor applies to every value",
         "The same methods you know from Python, one call for the whole column.",
         '''import pandas as pd

s = pd.Series(["  Ana ", "RAJ", "kim  "])

print("raw      :", list(s))
print("strip    :", list(s.str.strip()))
print("lower    :", list(s.str.lower()))
print("title    :", list(s.str.strip().str.title()))
print("len      :", list(s.str.len()))
print()
print("they chain, because each returns a Series:")
print("   ", list(s.str.strip().str.lower().str.replace("a", "@")))
print()
print("without .str you would be calling a method on the Series itself,")
print("which does something else entirely or fails.")'''),

        ("Missing values pass through",
         "<code>.str</code> returns NaN rather than raising, which is usually what "
         "you want and occasionally hides a problem.",
         '''import pandas as pd
import numpy as np

s = pd.Series(["ana", None, "kim", np.nan])

print("upper   :", list(s.str.upper()))
print("len     :", list(s.str.len()))
print("   the gaps stayed gaps - no error, no empty string")
print()
print("that matters when you filter on the result:")
print("   contains('a') :", list(s.str.contains("a")))
print("   the NaN rows are NaN, not False - and NaN is not a valid mask")
print()
try:
    s[s.str.contains("a")]
except ValueError as e:
    print("   using it directly ->", type(e).__name__, ":", str(e)[:44])
print()
print("na=False is the fix:")
print("   ", list(s[s.str.contains("a", na=False)]))'''),

        ("Testing and finding",
         "contains, startswith and match, and which of them takes a regex.",
         '''import pandas as pd

s = pd.Series(["order-1001", "invoice-22", "order-3", "note"])

print("contains('order') :", list(s.str.contains("order")))
print("startswith('order'):", list(s.str.startswith("order")))
print()
print("contains takes a REGEX by default:")
print("   contains(r'\\\\d{4}') :", list(s.str.contains(r"\\d{4}")))
print("   regex=False for a literal:", list(s.str.contains(".", regex=False)))
print()
print("match anchors at the start, fullmatch at both ends:")
print("   match('order')    :", list(s.str.match("order")))
print("   fullmatch('note') :", list(s.str.fullmatch("note")))'''),

        ("Splitting and extracting",
         "split with expand, and extract for the parts a regex names.",
         '''import pandas as pd

s = pd.Series(["order-1001", "invoice-22", "order-3"])

print("split into columns:")
print(s.str.split("-", expand=True))
print()
print("take one piece:")
print("   ", list(s.str.split("-").str[0]))
print()
print("extract uses capture groups and gives one column each:")
out = s.str.extract(r"(?P<kind>[a-z]+)-(?P<num>\\d+)")
print(out)
print("   dtypes:", dict(out.dtypes.astype(str)))
print("   note num is object - extract returns text, convert if you need numbers")'''),

        ("Replacing, with and without regex",
         "The default changed in pandas 2, so be explicit.",
         '''import pandas as pd

s = pd.Series(["a.b.c", "x.y", "no dots"])

print("literal replace:")
print("   ", list(s.str.replace(".", "-", regex=False)))
print()
print("regex replace:")
print("   ", list(s.str.replace(r"\\.", "-", regex=True)))
print()
print("a common clean-up - collapse runs of whitespace:")
messy = pd.Series(["too   many    spaces", "fine"])
print("   ", list(messy.str.replace(r"\\s+", " ", regex=True)))
print()
print("and tidy up column names in one line:")
df = pd.DataFrame(columns=["  First Name ", "AGE (years)"])
df.columns = (df.columns.str.strip().str.lower()
              .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_"))
print("   ", list(df.columns))'''),

        ("It is convenient, not fast",
         "Under the hood this is still per-element Python.",
         '''import pandas as pd
import time

n = 200_000
s = pd.Series(["value-%d" % i for i in range(n)])

t = time.perf_counter(); a = s.str.len(); str_time = time.perf_counter() - t
t = time.perf_counter(); b = s.str.startswith("value"); sw = time.perf_counter() - t
num = pd.Series(range(n))
t = time.perf_counter(); c = num * 2; num_time = time.perf_counter() - t

print("str.len on %d strings   : %.4f s" % (n, str_time))
print("str.startswith          : %.4f s" % sw)
print("numeric multiply        : %.4f s" % num_time)
print("text is %.0fx slower than arithmetic here" % (str_time / max(num_time, 1e-9)))
print()
print("Object columns store pointers to Python strings, so every")
print("operation walks them one at a time. Convert to category when")
print("the values repeat, and do text work once rather than in a loop.")'''),
    ],
    [
        "<code>.str</code> applies a string method to every value and returns a Series, so the calls chain.",
        "Missing values <strong>pass through as NaN</strong> rather than raising &mdash; and a mask containing NaN cannot be used to index, so pass <code>na=False</code>.",
        "<code>contains</code> takes a <strong>regex by default</strong>; pass <code>regex=False</code> for a literal. <code>match</code> anchors at the start, <code>fullmatch</code> at both ends.",
        "<code>split(expand=True)</code> makes columns; <code>extract</code> with named capture groups makes one column per group.",
        "<code>str.replace</code> needs an explicit <code>regex=</code> in pandas 2 &mdash; the old default changed.",
        "<code>.str</code> is convenient, not fast: object columns are per-element Python, and text work is far slower than arithmetic.",
    ],
    '''
title: Text Columns
intro: The .str accessor, and what it does with missing values.

## Why the accessor exists

A Series of strings is a column of Python string objects. You could loop over them, and `apply(str.strip)` would work, but both are slow and neither reads well.

`.str` exposes the string methods so they apply to the whole column: `s.str.strip()`, `s.str.lower()`, `s.str.len()`.

Each returns a Series, so they chain: `s.str.strip().str.lower().str.replace(" ", "_")`.

The accessor is required. `s.strip()` is not the same thing &mdash; it either does something unrelated to the Series or fails, because `strip` is not a Series method. Forgetting `.str` is the most common beginner error here, and the resulting `AttributeError` at least says so clearly.

## Missing values pass through

`.str` methods return `NaN` for missing input rather than raising or returning an empty string.

That is usually right: the uppercase of an unknown value is unknown.

It becomes a problem for **predicates**. `s.str.contains("a")` returns `True`, `False` **or `NaN`**, and a mask containing `NaN` cannot be used to index a frame &mdash; pandas raises "Cannot mask with non-boolean array containing NA / NaN values".

The fix is `na=False`, which decides what a missing value should count as:

```python
df[df["name"].str.contains("ana", na=False)]
```

Pass it every time you filter on a text predicate. `na=True` is occasionally what you want, when missing should be included.

This is the single most common runtime error in text cleaning, and it appears only when the data has a gap &mdash; so it usually shows up in production rather than on the sample.

## Testing

`contains` searches anywhere in the string. `startswith` and `endswith` anchor. `match` anchors at the start, `fullmatch` at both ends.

**`contains` takes a regular expression by default.** That matters more than it sounds, because it means `s.str.contains(".")` matches every non-empty string rather than finding a literal dot, and `s.str.contains("a|b")` is an alternation rather than a search for the three characters.

Pass `regex=False` for a literal search. It is also faster.

`case=False` makes the test case-insensitive without a separate `.lower()` pass.

`startswith` and `endswith` do **not** take a regex, which is an inconsistency worth remembering rather than deriving.

## Splitting and extracting

`s.str.split("-")` gives a Series of lists. That is rarely what you want directly.

`expand=True` turns it into a DataFrame with one column per piece, which is how you split a combined field into real columns. Rows with fewer pieces get `None` in the trailing columns.

`s.str.split("-").str[0]` takes one piece &mdash; the second `.str` indexes into the lists.

`extract` is usually better when the structure is known. It takes a regex with capture groups and returns one column per group, and named groups become column names:

```python
s.str.extract(r"(?P<kind>[a-z]+)-(?P<num>\\d+)")
```

Rows that do not match give `NaN` across the row, which makes non-matching input visible rather than silently mangled.

`extract` returns **text**, even for digits. Convert afterwards with `pd.to_numeric` if you need numbers.

`extractall` returns every match rather than the first, with a MultiIndex.

## Replacing

`s.str.replace(old, new, regex=...)` requires the `regex` argument to be explicit in pandas 2. The default changed, and code written against pandas 1 that relied on the old behaviour can silently do the wrong thing.

Two clean-ups earn their place in almost every script:

Collapsing whitespace: `s.str.replace(r"\\s+", " ", regex=True).str.strip()`.

Normalising column names:

```python
df.columns = (df.columns.str.strip().str.lower()
              .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_"))
```

That turns `"  First Name "` and `"AGE (years)"` into `first_name` and `age_years`, and it handles a whole spreadsheet's worth of inconsistent headers without listing them.

Note `df.columns.str` works too &mdash; the column index is an Index, and Index has a `.str` accessor as well.

## The cost

`.str` is a convenience, not a vectorisation.

Object columns hold pointers to Python strings, so every operation walks them one at a time in Python. The last editor shows text work running far slower than arithmetic on the same number of rows.

Three things help.

**Do it once.** Clean text at load time rather than repeatedly inside a loop or a function called per group.

**Convert to `category`** when values repeat. Operations then run on the small set of distinct values rather than every row.

**Consider the `string` dtype.** `astype("string")` gives the nullable extension type, which has clearer missing-value semantics than `object` and is where pandas' future optimisation work is going.

For very large text columns, the honest answer is that pandas is not the right tool, and the work belongs in a database or a purpose-built library.

## The cleaning pipeline

Text from the real world needs the same handful of operations almost every time, and doing them in one pass at load time is far better than scattering them through the analysis:

```python
df["city"] = (df["city"]
              .str.strip()
              .str.lower()
              .str.replace(r"\s+", " ", regex=True))
```

Strip the ends, normalise case, collapse internal whitespace. That alone resolves most of the "same value counted twice" problems that show up in a group-by.

For text that will be compared or joined on, consider also removing punctuation and accents. `unicodedata.normalize` handles accents; pandas has no built-in for it, and `.str.normalize("NFKD")` plus an ASCII encode is the usual idiom.

## Extracting structure

`str.extract` with named groups is the most useful of the extraction methods, because it names the outputs:

```python
df[["kind", "num"]] = df["ref"].str.extract(r"(?P<kind>[a-z]+)-(?P<num>\d+)")
```

Rows that do not match give `NaN` across the row, so counting them afterwards tells you how well the pattern fits:

```python
unmatched = df["kind"].isna().sum()
```

That check is worth making. A regex that matches 90% of rows silently discards the other 10%, and the only sign is a column with gaps.

`str.extractall` returns every match rather than the first, with a MultiIndex that has a `match` level.

`str.findall` returns a list per row, which is harder to work with and occasionally what you want.

## Testing and counting

`str.contains` &mdash; anywhere, regex by default, needs `na=False` for filtering.

`str.startswith` / `str.endswith` &mdash; anchored, **no regex**.

`str.match` &mdash; anchored at the start, regex.

`str.fullmatch` &mdash; anchored at both ends.

`str.count(pattern)` &mdash; how many times a pattern occurs per row.

`str.len` &mdash; length, which is a quick way to spot truncated or padded fields.

A frequent need is "does this contain any of these words":

```python
df["text"].str.contains("|".join(words), case=False, na=False)
```

Building an alternation is fine for a handful of words. For a long list, and for whole-word matching, it is worth escaping the parts with `re.escape` and adding word boundaries, or the results will surprise you.

## Splitting into columns

`str.split(sep, expand=True)` gives a DataFrame. Rows with fewer parts get `None` in the trailing columns, and rows with more parts are **truncated** unless you pass `n` to limit the splits.

`n=1` splits only on the first separator, which is what you want for `key: value` text where the value may contain the separator.

`str.rsplit` splits from the right, which handles "everything before the last dot" cleanly.

`str.partition` returns exactly three columns &mdash; before, separator, after &mdash; which avoids the variable-width problem entirely.

## Categorical text

Once text is cleaned, if it repeats, convert it:

```python
df["city"] = df["city"].astype("category")
```

The `.str` accessor still works on a categorical column, and pandas applies the operation to the **categories** rather than to every row &mdash; so `df["city"].str.upper()` on a million rows with four cities does four operations, not a million.

That is the single largest speed-up available for repeated text work, and it is a one-line change.

## When to stop using pandas for text

pandas is a reasonable place to clean and extract from moderate amounts of text. It is not a text-processing engine.

For tokenisation, stemming, language detection or anything linguistic, a dedicated library is the right tool.

For very large corpora, the `object` dtype's per-row Python cost dominates, and the work belongs in a database, in Polars, or in a purpose-built pipeline.

The signal is usually the profile: if `.str` operations are the slowest part of your script and the frame is large, the answer is a different tool rather than a cleverer regex.

## Regex, briefly

Several `.str` methods take a regular expression, and a small vocabulary covers most data cleaning:

`\d` digit, `\w` word character, `\s` whitespace, `.` any character.

`+` one or more, `*` zero or more, `?` optional.

`^` start, `$` end, `\b` word boundary.

`[abc]` a character set, `[^abc]` its negation.

`(...)` a capture group, `(?P<name>...)` a named one.

`|` alternation.

Two habits prevent most regex trouble in pandas. Use **raw strings** &mdash; `r"\d+"` &mdash; so backslashes reach the regex engine intact. And test the pattern on a handful of values before applying it to the column, because a pattern that matches nothing produces a column of `NaN` rather than an error.

`str.contains(..., regex=False)` and `str.replace(..., regex=False)` are both faster and safer when the pattern is a literal.

## Encoding problems

Text that arrives mangled &mdash; `Ã©` where `é` belongs &mdash; was decoded with the wrong encoding, usually at read time.

The fix is at `read_csv`, with `encoding="latin-1"` or `encoding="cp1252"`, not in pandas afterwards. Repairing mojibake after the fact is possible and unreliable.

`df["col"].str.encode("utf-8").str.decode("utf-8")` round-trips text and raises on anything invalid, which is a way to find the offending rows.

For matching across accented and unaccented spellings, normalising with `str.normalize("NFKD")` and stripping combining characters puts both forms into the same shape.

## Performance, restated

Three things make text work faster, in order of effect:

**Convert to `category`** when values repeat. Operations then apply to the categories, not the rows.

**Do the cleaning once**, at load time, rather than inside a function called per group or per row.

**Use `regex=False`** where the pattern is a literal.

And the structural point: if `.str` operations dominate the profile on a large frame, pandas is the wrong layer for that work. A database, Polars, or a purpose-built text pipeline will do it in a fraction of the time.

## A summary

`.str` applies string methods elementwise and chains.

Missing values pass through as `NaN`; pass `na=False` on any predicate used for filtering.

`contains` is a regex by default; `startswith` is not a regex at all.

`split(expand=True)` makes columns; `extract` with named groups is usually clearer.

`replace` needs an explicit `regex=` in pandas 2.

Normalise column names and text values once, at load.

Convert repeated text to `category`.

And check how many rows a pattern actually matched, rather than assuming it matched them all.

## A closing note

Text is where pandas is least like an array library and most like ordinary Python, and both facts show.

`.str` gives you the string methods across a whole column, which is convenient and reads well. Underneath it is per-element Python over a column of pointers, which is why text work is an order of magnitude slower than arithmetic on the same number of rows.

Two things follow. Clean text **once**, at load, rather than repeatedly in the middle of a pipeline. And convert repeated values to `category`, after which `.str` operations apply to the handful of distinct values rather than to every row &mdash; usually the largest single speed-up available, for a one-line change.

The correctness trap is missing values. `.str` predicates return `NaN` rather than `False`, and a mask containing `NaN` cannot index a frame. `na=False` on every `.str` filter is the habit, and its absence is the error that appears only once the data has a gap.

## One more thing

`str.get(i)` indexes into each string or list, which is the concise form of `str[i]` and works the same way. It returns `NaN` rather than raising where the index is out of range, which is usually what you want on ragged data.
''',
    [
        {"q": "Why does `df[df['name'].str.contains('a')]` sometimes raise?",
         "options": ["contains is deprecated", "Missing values make the mask NaN, and a mask with NaN cannot index", "The column is numeric", "It needs regex=True"],
         "answer": 1,
         "why": "Pass na=False every time you filter on a text predicate. The error appears only when the data has a gap, so it surfaces in production."},
        {"q": "What does `s.str.contains('.')` match?",
         "options": ["Strings containing a literal dot", "Every non-empty string, because contains takes a regex by default", "Nothing", "Only dots"],
         "answer": 1,
         "why": "Pass regex=False for a literal search - it is also faster. Note startswith and endswith do not take a regex at all."},
        {"q": "What does `str.extract` return for a row that does not match?",
         "options": ["An empty string", "NaN across the row", "The original value", "It raises"],
         "answer": 1,
         "why": "That makes non-matching input visible rather than silently mangled. Note extract returns text even for digits - convert with pd.to_numeric."},
        {"q": "Why is `.str` slower than arithmetic on the same number of rows?",
         "options": ["It copies the frame", "Object columns hold pointers to Python strings, so operations walk them one at a time", "It uses regex always", "It is not slower"],
         "answer": 1,
         "why": "Clean text once at load time, and convert to category when values repeat so operations run on the distinct values instead."},
    ],
)


# ---------------------------------------------------------------------------
# 13. Dates and times
# ---------------------------------------------------------------------------
topic(
    "datetimes",
    "Dates and Times",
    "Cleaning Data",
    "Parsing them, the .dt accessor, and why a date column read as text breaks "
    "everything downstream.",
    _svg(_box(16, 30, 46, 28, S, "#a44") + _txt(39, 48, '"05/04/24"', "#e88", 7) +
         _arrow(66, 44, 84, 44) +
         _box(92, 30, 50, 28, S, A) + _txt(117, 48, "2024-04-05", A, 7)),
    [
        ("Dates arrive as text",
         "And text sorts and compares the wrong way, silently.",
         '''import pandas as pd

s = pd.Series(["2024-03-01", "2024-01-15", "2024-11-02"])
print("dtype as read:", s.dtype)
print("sorted as text:", list(s.sort_values()))
print("   looks fine - ISO dates happen to sort correctly as text")
print()
bad = pd.Series(["01/03/2024", "15/01/2024", "02/11/2024"])
print("but any other format does not:")
print("   ", list(bad.sort_values()))
print()
d = pd.to_datetime(s)
print("after to_datetime:", d.dtype)
print("   ", list(d.sort_values().dt.strftime("%Y-%m-%d")))'''),

        ("Parsing, and being explicit about format",
         "Ambiguous formats are guessed, and the guess is not always yours.",
         '''import pandas as pd

print("day-first vs month-first is genuinely ambiguous:")
print("   default  :", pd.to_datetime("05/04/2024").strftime("%d %b %Y"))
print("   dayfirst :", pd.to_datetime("05/04/2024", dayfirst=True).strftime("%d %b %Y"))
print()
print("an explicit format removes the guess and is much faster:")
d = pd.to_datetime(["05/04/2024", "06/04/2024"], format="%d/%m/%Y")
print("   ", list(d.strftime("%Y-%m-%d")))
print()
print("bad values stop the parse unless you say otherwise:")
mixed = pd.Series(["2024-01-01", "not a date", "2024-02-01"])
try:
    pd.to_datetime(mixed)
except Exception as e:
    print("    ->", type(e).__name__)
print("   errors='coerce':", list(pd.to_datetime(mixed, errors="coerce")))'''),

        ("The .dt accessor",
         "The same idea as .str, for the parts of a timestamp.",
         '''import pandas as pd

s = pd.to_datetime(pd.Series([
    "2024-01-15 09:30:00", "2024-06-02 18:45:00", "2024-11-30 23:05:00"]))

print("year   :", list(s.dt.year))
print("month  :", list(s.dt.month))
print("day    :", list(s.dt.day))
print("hour   :", list(s.dt.hour))
print("weekday:", list(s.dt.day_name()))
print("quarter:", list(s.dt.quarter))
print()
print("date drops the time part:", list(s.dt.date))
print("normalize keeps it a timestamp at midnight:")
print("   ", list(s.dt.normalize().dt.strftime("%Y-%m-%d %H:%M")))
print()
print("format for output with strftime:")
print("   ", list(s.dt.strftime("%d %b %Y")))'''),

        ("Arithmetic gives durations",
         "Subtracting timestamps produces a Timedelta, which has its own accessor.",
         '''import pandas as pd

start = pd.to_datetime(pd.Series(["2024-01-01", "2024-03-15"]))
end = pd.to_datetime(pd.Series(["2024-01-11", "2024-04-01"]))

gap = end - start
print("difference:", list(gap))
print("dtype     :", gap.dtype)
print()
print("as numbers:")
print("   days   :", list(gap.dt.days))
print("   hours  :", list((gap.dt.total_seconds() / 3600).astype(int)))
print()
print("add a duration:")
print("   ", list((start + pd.Timedelta(days=30)).dt.strftime("%Y-%m-%d")))
print()
print("offsets understand calendars in a way timedeltas do not:")
print("   +1 month:", list((start + pd.DateOffset(months=1)).dt.strftime("%Y-%m-%d")))'''),

        ("A DatetimeIndex unlocks time selection",
         "Put the dates in the index and you can slice by period.",
         '''import pandas as pd
import numpy as np

idx = pd.date_range("2024-01-01", periods=90, freq="D")
s = pd.Series(np.arange(90), index=idx)

print("select a whole month by string:")
print("   len(s['2024-02']) =", len(s["2024-02"]))
print()
print("a range, inclusive of both ends:")
print("   len(s['2024-01-10':'2024-01-20']) =", len(s["2024-01-10":"2024-01-20"]))
print()
print("date_range builds the axis:")
print("   ", list(pd.date_range("2024-01-01", periods=3, freq="ME").strftime("%Y-%m-%d")))
print("   ", list(pd.date_range("2024-01-01", periods=3, freq="W").strftime("%Y-%m-%d")))'''),

        ("Time zones, briefly",
         "Naive and aware timestamps do not mix, and the error is worth meeting once.",
         '''import pandas as pd

naive = pd.to_datetime(pd.Series(["2024-01-01 12:00"]))
aware = naive.dt.tz_localize("UTC")

print("naive:", list(naive.astype(str)))
print("aware:", list(aware.astype(str)))
print()
print("converting to another zone:")
print("   ", list(aware.dt.tz_convert("Asia/Kolkata").astype(str)))
print()
try:
    naive - aware
except Exception as e:
    print("naive - aware ->", type(e).__name__)
    print("   ", str(e)[:62])
print()
print("Pick one and stay there. Storing UTC and converting only for")
print("display is the convention that causes the fewest surprises.")'''),
    ],
    [
        "A date column read as <strong>text</strong> sorts and compares lexically &mdash; which happens to work for ISO dates and fails for every other format.",
        "<code>pd.to_datetime</code> guesses ambiguous formats; pass <code>format=</code> to remove the guess and make it much faster, or <code>dayfirst=True</code>.",
        "<code>errors=\"coerce\"</code> turns unparseable values into <code>NaT</code> instead of stopping the whole parse.",
        "<code>.dt</code> is to timestamps what <code>.str</code> is to text &mdash; <code>year</code>, <code>month</code>, <code>day_name()</code>, <code>quarter</code>, <code>strftime</code>.",
        "Subtracting timestamps gives a <strong>Timedelta</strong>; <code>DateOffset</code> understands calendar months in a way a fixed duration cannot.",
        "A <strong>DatetimeIndex</strong> lets you slice by period &mdash; <code>s[\"2024-02\"]</code> selects a whole month.",
    ],
    '''
title: Dates and Times
intro: Parsing them, the .dt accessor, and why a text date breaks everything downstream.

## They arrive as text

`read_csv` does not parse dates unless you tell it to. A date column comes in as `object`, and everything you do with it is then string behaviour wearing a date's clothes.

Sorting is lexical. For ISO format &mdash; `YYYY-MM-DD` &mdash; that happens to give the right answer, which is why the problem often goes unnoticed until the data arrives in another format. `"15/01/2024"` sorts before `"01/03/2024"` as text, and there is no error.

Comparison has the same problem, as does anything asking for a month, a weekday or a difference in days.

The fix is `pd.to_datetime`, or `parse_dates=["col"]` at read time, which is faster because it happens during the read.

Checking `df.dtypes` after loading catches this, which is why it is in the inspection routine.

## Parsing

`pd.to_datetime` is good at guessing, and guessing is the problem.

`05/04/2024` is 5 April in most of the world and 4 May in the United States. pandas has to pick one, and it will not necessarily pick yours.

`dayfirst=True` states the convention. Better still, `format="%d/%m/%Y"` states the whole shape. That removes the ambiguity **and** is substantially faster, because pandas can skip inference entirely &mdash; on a large column the difference is large enough to notice.

For messy input, `errors="coerce"` turns unparseable values into `NaT` (the datetime equivalent of NaN) rather than raising on the first bad row. Then `df[df["date"].isna()]` shows you exactly what failed, which is far more useful than a traceback naming one value.

`NaT` behaves like NaN: it fails every comparison and is caught by `isna()`.

## The .dt accessor

Exactly parallel to `.str`.

`s.dt.year`, `.month`, `.day`, `.hour`, `.minute` pull out components as integers.

`s.dt.day_name()` and `s.dt.month_name()` give text.

`s.dt.quarter`, `.dayofweek`, `.dayofyear`, `.is_month_end` cover the derived questions that would otherwise need arithmetic.

`s.dt.date` drops the time and returns Python `date` objects &mdash; note that this gives an `object` column, which is usually not what you want. `s.dt.normalize()` keeps it a proper datetime column set to midnight, and is the better choice for grouping by day.

`s.dt.strftime(fmt)` formats for output, returning text. That is the last step before display, not something to do in the middle of a pipeline.

## Arithmetic

Subtracting two datetime columns gives a `timedelta64` column.

`gap.dt.days` gives whole days; `gap.dt.total_seconds()` gives the full duration as a float, which is what you want for anything sub-day or for converting to arbitrary units.

Adding a fixed duration uses `pd.Timedelta(days=30)`.

Adding a **calendar** period uses `pd.DateOffset(months=1)`. The distinction matters: a month is not a fixed number of days, so "one month after 31 January" is a calendar question, not an arithmetic one. `DateOffset` handles month ends and leap years; `Timedelta` cannot, because it does not know what month it is in.

## DatetimeIndex

Putting the dates in the index unlocks the time-aware selection that makes pandas pleasant for time series.

`s["2024-02"]` selects the whole of February. `s["2024"]` selects the year. This is **partial string indexing**, and it works because pandas understands the index is a timeline.

`s["2024-01-10":"2024-01-20"]` slices a range, inclusive of both endpoints as label slicing always is.

`pd.date_range(start, periods=n, freq=...)` builds such an index. The frequency aliases are worth knowing: `D` daily, `W` weekly, `ME` month end, `MS` month start, `h` hourly. Note that pandas 2.2 renamed several of these &mdash; `M` became `ME` and `H` became `h` &mdash; so older code raises a deprecation warning or an error depending on version.

A DatetimeIndex is also what `resample` requires, which is the subject of a later module.

## Time zones

A timestamp is either **naive** (no zone) or **aware** (a zone attached). The two cannot be compared or subtracted, and the error when you try is clear.

`s.dt.tz_localize("UTC")` attaches a zone to naive timestamps, asserting what they always meant. `s.dt.tz_convert("Asia/Kolkata")` converts an aware timestamp to another zone.

Getting these backwards is the usual mistake: `tz_localize` on data that is already aware raises, and `tz_convert` on naive data raises too.

The convention that causes the fewest problems is to store everything in UTC and convert only for display. Mixed-zone data in one column is not representable as a proper datetime dtype at all &mdash; it falls back to `object` &mdash; which is a strong hint that normalising early is the right move.

## Parsing performance

Date parsing is one of the slowest parts of loading a large file, and it is almost entirely avoidable.

`pd.to_datetime` without a format tries to infer one, per value in the worst case. With `format=` it uses a single known pattern and runs far faster &mdash; often by an order of magnitude on a large column.

`format="ISO8601"` handles the common ISO variants without full inference.

`cache=True` (the default for large inputs) helps enormously when the same date string repeats, as it does in any dataset with many rows per day.

Parsing at read time with `parse_dates=` is faster than parsing afterwards, because pandas can do it while it already has the strings in hand.

## Periods and offsets

`Timestamp` is a point in time. `Period` is a span &mdash; a whole month, a quarter, a year.

`s.dt.to_period("M")` converts timestamps to monthly periods. Grouping by that is often more natural than grouping by year and month separately, and it sorts correctly.

`PeriodIndex` supports arithmetic in period units: adding 1 to a monthly period gives the next month, without the day-of-month ambiguity that plagues timestamp arithmetic.

Offsets sit between the two. `pd.offsets.MonthEnd(1)`, `BusinessDay(3)`, `Week(weekday=0)` describe calendar movements. `df["date"] + pd.offsets.MonthEnd(0)` snaps each date to the end of its month, which is a common alignment step before joining monthly data.

Business-day offsets understand weekends, and can take a holiday calendar, which is the sort of thing that is tedious to write by hand and easy to get subtly wrong.

## Components, and the leap-year trap

`.dt.year`, `.month`, `.day` are obvious. Two are not.

`.dt.isocalendar()` returns ISO year, week and day, which is what you want for week-based reporting. The ISO year is **not** always the calendar year &mdash; the first days of January can belong to the previous ISO year &mdash; so grouping by `.dt.year` and ISO week together produces wrong groups at the boundary.

`.dt.dayofweek` is 0 for Monday; `.dt.day_name()` gives the name and respects locale settings.

Computing an age or a duration in years by dividing days by 365 is wrong by a day every four years and accumulates. For exact calendar differences, subtract periods or use `dateutil.relativedelta`.

## Time zones, in more depth

The rule that avoids nearly all trouble: **store UTC, convert for display**.

`tz_localize` attaches a zone to naive timestamps, asserting what they always meant. It raises on data that is already aware.

`tz_convert` moves an aware timestamp to another zone. It raises on naive data.

Getting these the wrong way round is the usual error, and the messages are clear about which you needed.

Two edge cases are worth knowing because they are real and they raise:

**Ambiguous times** &mdash; when clocks go back, an hour occurs twice. `ambiguous="infer"`, `True`, `False`, or `NaT` decides.

**Nonexistent times** &mdash; when clocks go forward, an hour does not exist. `nonexistent="shift_forward"` or `NaT` decides.

Both only appear on real local-time data crossing a DST boundary, which is exactly when you least want a surprise.

A column mixing time zones cannot be a proper datetime dtype and falls back to `object`, losing `.dt` entirely. Normalising on the way in prevents that.

## A checklist for date columns

Parse them at read time, with an explicit format.

Check `dtype` afterwards &mdash; `datetime64[ns]` means it worked, `object` means it did not.

Check the range with `min()` and `max()`. Dates in 1970 usually mean a zero timestamp; dates in 2099 usually mean a sentinel.

Decide on a time zone and apply it once.

Set the index if you will resample or select by period.

Sort, if anything downstream will `diff`, `shift` or `rolling`.

## Common date mistakes

**Not parsing at all.** The column stays `object`, sorts lexically, and `.dt` raises. Check `dtypes`.

**Letting the format be inferred** on ambiguous data. `05/04` is two different dates depending on convention.

**Dividing days by 365** to get years. Wrong by a day every four years, and it accumulates.

**Grouping by `.dt.year` and ISO week together.** The ISO year differs from the calendar year at the start of January, so the boundary weeks land in the wrong group.

**Mixing naive and aware timestamps.** Raises, which is the good case; the bad case is a column that falls back to `object` and loses `.dt`.

**Using `.dt.date`** and getting an `object` column. `.dt.normalize()` keeps it a datetime.

**Assuming rows are sorted.** `diff` and `rolling` produce numbers regardless.

## Working with durations

A `timedelta64` column comes from subtracting two datetime columns.

`gap.dt.days` truncates toward zero and discards the remainder; `gap.dt.total_seconds()` keeps everything and is the safer basis for converting to arbitrary units.

`gap.dt.components` breaks a duration into days, hours, minutes and so on as separate columns.

Durations aggregate: `mean`, `sum` and `describe` all work, and print in a readable form.

For business durations &mdash; elapsed working days rather than calendar days &mdash; `np.busday_count` is the tool, and it takes a holiday list.

## Generating date ranges

`pd.date_range(start, end)` or `pd.date_range(start, periods=n, freq=...)` builds an axis.

Three uses worth knowing:

**Reindexing onto a complete calendar**, so missing days become explicit `NaN` rows rather than being absent.

**Building test data** with a known shape.

**Checking for gaps** &mdash; comparing the actual index against a complete range shows exactly which periods are missing:

```python
full = pd.date_range(s.index.min(), s.index.max(), freq="D")
missing = full.difference(s.index)
```

That is a better answer than counting rows, because it names the gaps.

`pd.bdate_range` does the same for business days.

## A summary

Parse at read time with an explicit format.

Check the dtype is `datetime64[ns]` afterwards, and check the min and max for sentinel dates.

`.dt` for components, `strftime` only for display.

`Timedelta` for fixed durations, `DateOffset` for calendar ones.

Store UTC; convert for display.

Set a `DatetimeIndex` when you need period selection or `resample`.

Sort before anything that compares a row with its neighbour.

And remember pandas 2.2 renamed the frequency aliases &mdash; `M` to `ME`, `H` to `h` &mdash; which is the usual reason a copied example no longer runs.

## A closing note

Dates arrive as text, and everything that follows depends on noticing that.

An unparsed date column sorts lexically, cannot do arithmetic, and has no `.dt`. For ISO-formatted dates the lexical sort happens to be correct, which is precisely why the problem often survives until the data arrives in a different format.

Parsing with an explicit `format=` removes both the ambiguity between day-first and month-first and most of the parsing cost, which on a large column is substantial.

After that, the two things worth being deliberate about are time zones and calendar arithmetic. Store UTC and convert for display, because mixed-zone columns cannot be a proper datetime dtype at all. And use `DateOffset` rather than `Timedelta` when you mean a calendar month, since a month is not a fixed number of days and only one of the two knows that.

Finally, pandas 2.2 renamed the frequency aliases. When a copied example stops working, that is usually why.
''',
    [
        {"q": "Why does a date column read as text often seem to sort correctly?",
         "options": ["pandas parses it silently", "ISO format YYYY-MM-DD happens to sort correctly lexically", "Text always sorts by date", "It does not"],
         "answer": 1,
         "why": "The bug hides until the data arrives in another format - '15/01/2024' sorts before '01/03/2024' as text, with no error."},
        {"q": "Why pass `format=` to `pd.to_datetime`?",
         "options": ["It is required", "It removes the day-first/month-first ambiguity and is substantially faster", "It handles time zones", "It sorts the result"],
         "answer": 1,
         "why": "05/04/2024 is 5 April in most of the world and 4 May in the US, and pandas has to pick one. An explicit format also skips inference."},
        {"q": "What is the difference between `pd.Timedelta(months=1)` and `pd.DateOffset(months=1)`?",
         "options": ["None", "A month is not a fixed duration - only DateOffset understands calendars", "Timedelta is faster", "DateOffset is deprecated"],
         "answer": 1,
         "why": "'One month after 31 January' is a calendar question. Timedelta cannot answer it because it does not know what month it is in."},
        {"q": "What does `s['2024-02']` do on a Series with a DatetimeIndex?",
         "options": ["Raises KeyError", "Selects every row in February 2024", "Returns one row", "Returns the string"],
         "answer": 1,
         "why": "Partial string indexing works because pandas understands the index is a timeline. s['2024'] selects the whole year."},
    ],
)


# ---------------------------------------------------------------------------
# 14. Sorting and ranking
# ---------------------------------------------------------------------------
topic(
    "sorting_and_ranking",
    "Sorting and Ranking",
    "Summarising",
    "sort_values, nlargest and rank - and where the missing values end up.",
    _svg(_grid(22, 24, 1, 4, 13) + _txt(28, 20, "?", M, 8) +
         _arrow(44, 44, 62, 44) +
         _grid(72, 24, 1, 4, 13) + _txt(78, 20, "sorted", A, 8)),
    [
        ("sort_values takes one column or several",
         "And returns a new frame, keeping the original index labels.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "pune", "goa"],
    "sales": [30, 20, 10, 20],
})
print("by sales:")
print(df.sort_values("sales"))
print()
print("descending:")
print(df.sort_values("sales", ascending=False))
print()
print("two keys, with different directions:")
print(df.sort_values(["city", "sales"], ascending=[True, False]))
print()
print("the index came along - reset it if position matters:")
print(list(df.sort_values("sales").index))'''),

        ("Missing values go last, whatever the direction",
         "Which means descending order does not simply reverse ascending order.",
         '''import pandas as pd
import numpy as np

s = pd.Series([3.0, np.nan, 1.0, 2.0])

print("ascending :", list(s.sort_values()))
print("descending:", list(s.sort_values(ascending=False)))
print("   NaN is last in BOTH - it is not treated as large or small")
print()
print("na_position='first' moves it:")
print("   ", list(s.sort_values(na_position="first")))
print()
print("so reversing a sorted result is not the same as sorting descending:")
print("   reversed ascending:", list(s.sort_values()[::-1]))
print("   sorted descending :", list(s.sort_values(ascending=False)))'''),

        ("sort_index versus sort_values",
         "One orders by the labels, the other by the data.",
         '''import pandas as pd

s = pd.Series([10, 30, 20], index=["c", "a", "b"])

print("original      :", dict(s))
print("sort_index()  :", dict(s.sort_index()), "<- by LABEL")
print("sort_values() :", dict(s.sort_values()), "<- by DATA")
print()
df = pd.DataFrame({"b": [1, 2], "a": [3, 4]})
print("sort the columns alphabetically:")
print(df.sort_index(axis=1))
print()
print("sort_index matters after a groupby, which returns")
print("groups in sorted key order already.")'''),

        ("nlargest beats sorting the whole frame",
         "When you only want the top few, do not order the rest.",
         '''import pandas as pd
import numpy as np
import time

rng = np.random.default_rng(0)
df = pd.DataFrame({"v": rng.random(200_000)})

t = time.perf_counter(); a = df.sort_values("v", ascending=False).head(5); t1 = time.perf_counter() - t
t = time.perf_counter(); b = df.nlargest(5, "v"); t2 = time.perf_counter() - t

print("sort then head : %.4f s" % t1)
print("nlargest       : %.4f s" % t2)
print("ratio          : %.1fx" % (t1 / max(t2, 1e-9)))
print("same rows      :", a.index.equals(b.index))
print()
print("nsmallest is the other direction, and both take a column list")
print("for tie-breaking.")'''),

        ("rank, and what to do with ties",
         "The default averages tied ranks, which is often not what a leaderboard wants.",
         '''import pandas as pd

s = pd.Series([10, 20, 20, 40], index=["a", "b", "c", "d"])

for how in ["average", "min", "max", "dense", "first"]:
    print("%-8s :" % how, list(s.rank(method=how).astype(float)))

print()
print("average : the two 20s share rank 2.5")
print("min     : both get 2, and 3 is skipped  (competition ranking)")
print("dense   : both get 2, and the next is 3 (no gaps)")
print("first   : ties broken by order of appearance")
print()
print("descending ranks:", list(s.rank(ascending=False).astype(float)))
print("as a percentage :", [round(v, 2) for v in s.rank(pct=True)])'''),

        ("Sorting is not free",
         "It is n log n and it copies, so do it once and late.",
         '''import pandas as pd
import numpy as np
import time

rng = np.random.default_rng(0)
df = pd.DataFrame({"k": rng.integers(0, 1000, 300_000),
                   "v": rng.random(300_000)})

t = time.perf_counter(); df.sort_values("v"); full = time.perf_counter() - t
t = time.perf_counter(); df["v"].max(); mx = time.perf_counter() - t

print("sort 300k rows : %.4f s" % full)
print("max of a column: %.6f s" % mx)
print("sorting is %.0fx the cost of the reduction" % (full / max(mx, 1e-9)))
print()
print("If you only need the extreme, do not sort. If you need the top n,")
print("use nlargest. Sort when the ORDER itself is the output.")'''),
    ],
    [
        "<code>sort_values</code> takes one or several columns and an <code>ascending</code> list per key; it returns a new frame carrying the original labels.",
        "Missing values sort <strong>last in both directions</strong>, so reversing an ascending sort is not the same as sorting descending.",
        "<code>sort_index</code> orders by label, <code>sort_values</code> by data; <code>sort_index(axis=1)</code> orders the columns.",
        "<code>nlargest(n, col)</code> is much faster than sorting everything and taking the head.",
        "<code>rank</code> defaults to <strong>averaging</strong> ties; <code>min</code> gives competition ranking and <code>dense</code> leaves no gaps.",
        "Sorting is <code>n log n</code> and copies &mdash; use a reduction for an extreme, <code>nlargest</code> for a top n, and sort only when order is the output.",
    ],
    '''
title: Sorting and Ranking
intro: sort_values, nlargest and rank, and where the missing values end up.

## sort_values

`df.sort_values("sales")` sorts by one column. A list sorts by several, in order, and `ascending` takes a matching list so each key can have its own direction:

```python
df.sort_values(["city", "sales"], ascending=[True, False])
```

That is "by city A to Z, and within each city by sales high to low" &mdash; the shape of most reporting orders.

The result is a **new** frame carrying the original index labels. If downstream code thinks positionally, `reset_index(drop=True)` afterwards.

`kind` selects the algorithm. The default is not stable, so equal rows can come out in any order. Pass `kind="stable"` when ties must keep their original relative order &mdash; which matters if you are sorting by a second key after already sorting by a first, rather than passing both keys at once.

## Missing values sort last

`NaN` goes to the **end** in both ascending and descending order. It is not treated as very large or very small; it is simply put aside.

The consequence catches people: reversing an ascending sort is **not** the same as sorting descending, because the NaNs move relative to everything else.

`na_position="first"` puts them at the front instead, which is useful when the missing rows are the ones you want to look at.

## sort_index

`sort_index()` orders by the index labels rather than the data. It is what you want after operations that leave the index shuffled, and it is required for label-range slicing on a non-unique index.

`sort_index(axis=1)` orders the **columns** alphabetically, which is a quick way to make two frames comparable.

Group-by results already come back sorted by key, so an extra `sort_index` there is usually redundant.

## nlargest and nsmallest

Sorting 200,000 rows to look at five is wasted work.

`df.nlargest(5, "v")` finds the top five without ordering the rest, and the last-but-one editor measures the difference.

Both take a list of columns for tie-breaking, and a `keep` argument controlling what happens when the boundary value is tied: `"first"`, `"last"` or `"all"`. `keep="all"` can return more than `n` rows, which is occasionally what you want and worth knowing before it surprises you.

For a single extreme value, neither is needed: `df["v"].max()` is a reduction and far cheaper than any sort. `idxmax()` gives the label of the row that holds it, which is how you get "the row with the highest value" in one step.

## rank

`rank` converts values into positions, and the interesting part is what it does with ties.

`method="average"` (the default) gives tied values the mean of the ranks they span &mdash; two values tied for 2nd and 3rd both get 2.5. That is the statistically conventional choice and it produces fractional ranks, which surprises people expecting integers.

`method="min"` gives both 2 and skips 3. This is competition ranking, the "joint second" of a leaderboard.

`method="max"` gives both 3.

`method="dense"` gives both 2 and makes the next value 3 &mdash; no gaps, which is what you want for grouping into levels.

`method="first"` breaks ties by order of appearance, giving strictly distinct integer ranks.

`ascending=False` ranks from the top. `pct=True` returns percentiles rather than positions, which is the quick route to "what fraction of rows are below this one".

`rank` also takes a `na_option`, and by default missing values get `NaN` ranks rather than being placed anywhere.

## The cost

Sorting is `O(n log n)` and allocates a new frame. On a large table it is one of the more expensive things you can do.

Three cheaper alternatives cover most reasons people sort:

**An extreme value**: `max`, `min`, `idxmax`, `idxmin` &mdash; a single linear pass.

**A top n**: `nlargest` / `nsmallest`.

**Deduplication order**: sorting is genuinely required here, and it is the one case where sorting before `drop_duplicates` is not optional.

Sort when the order is the actual output &mdash; a report, a chart, a file someone will read. Otherwise there is usually a reduction that answers the same question for a fraction of the cost.

## Sorting by something that is not a column

`key=` applies a function to the sort keys before comparing, without changing the data:

```python
df.sort_values("city", key=lambda s: s.str.lower())
```

That sorts case-insensitively while leaving the original values intact. It is much cleaner than adding a helper column, sorting, and dropping it.

For a **custom order** &mdash; small, medium, large &mdash; the right tool is an ordered categorical:

```python
df["size"] = pd.Categorical(df["size"], ["small", "medium", "large"], ordered=True)
df.sort_values("size")
```

The order then belongs to the column and applies to every later sort, group-by and comparison, rather than being repeated at each call site.

Sorting by string length, by the last character, or by any derived value is `key=` with the appropriate `.str` operation.

## Sorting a group-by result

Group-by output arrives sorted by key. Usually you want it sorted by the value:

```python
df.groupby("city")["sales"].sum().sort_values(ascending=False)
```

`sort=False` on the group-by itself skips the key sort, which is faster on many groups and gives order of first appearance.

For "the top n within each group", the pattern is a group-wise rank and a filter:

```python
df[df.groupby("city")["sales"].rank(ascending=False) <= 3]
```

`groupby(...).head(3)` also works and takes the first three **rows** of each group in current order, so it needs a sort first to mean "the top three".

## Stability, in practice

The default sort is not stable, so equal elements can come out in any order.

That matters in two situations.

**A multi-pass sort.** Sorting by one column, then another, only works if the second sort preserves the first ordering. Pass `kind="stable"`, or better, sort by both keys in one call with a list.

**Reproducible output.** Two runs on the same data can order ties differently, which makes diffs noisy and tests flaky. `kind="stable"` fixes it.

The cost is small enough that using `kind="stable"` by default when the output is compared or written to a file is a reasonable habit.

## Sorting large frames

Sorting is `O(n log n)` and copies the frame. On a large table it is often the most expensive single operation in a script.

The alternatives, in order of preference:

**A reduction** &mdash; `max`, `min`, `idxmax`, `idxmin` for an extreme.

**`nlargest` / `nsmallest`** for a top n.

**`sort_index`** if the data is already nearly sorted by that key; it is cheaper than a full value sort.

**Sorting once** and reusing the result, rather than sorting inside a loop or a function called repeatedly.

And when the sort *is* the output &mdash; a report, a leaderboard, a file someone reads &mdash; it is not overhead, it is the deliverable.

## Ranking, and what to do with ties

The five methods differ only in tie handling, and the right choice depends on what the rank is for.

For a **leaderboard**, `min` gives the familiar "joint second, then fourth".

For **levels or bands**, `dense` avoids gaps.

For a **statistic** &mdash; a rank correlation, a percentile &mdash; `average` is the conventional choice and is the default for that reason.

For a **deterministic ordering** where ties must be broken, `first` uses order of appearance, which means the result depends on how the frame is sorted.

`pct=True` gives percentile ranks in `[0, 1]`, which is the quick route to "what fraction of rows are at or below this one" and is comparable across datasets of different sizes.

## Sorting the columns rather than the rows

`df.sort_index(axis=1)` orders columns alphabetically, which makes two frames easier to compare and diffs easier to read.

For a deliberate order, selection is clearer: `df[["id", "date", "value"]]`.

For a partial order &mdash; pin some columns to the front, keep the rest &mdash; build the list:

```python
first = ["id", "date"]
df = df[first + [c for c in df.columns if c not in first]]
```

That survives a schema change, where a hard-coded full list does not.

## Sorting for output

When the sort is the deliverable, a few details matter that do not otherwise.

`na_position="first"` when missing rows are what the reader should notice.

`key=` for case-insensitive or natural ordering.

An **ordered categorical** for a domain order &mdash; small/medium/large &mdash; so every later operation uses it too.

`reset_index(drop=True)` if row numbers will be displayed, so they read 0, 1, 2 rather than the original labels.

`kind="stable"` so that re-running produces byte-identical output, which matters if the result is committed or diffed.

## Ties, restated

The choice of tie-handling is a decision about meaning, not a technicality:

`average` &mdash; the statistical convention; produces fractional ranks.

`min` &mdash; competition ranking; joint second, then fourth.

`dense` &mdash; no gaps; for bands and levels.

`max` &mdash; the pessimistic reading.

`first` &mdash; arbitrary but deterministic, and dependent on the current row order.

If ranks are shown to people, `min` or `dense` usually matches their expectations. If ranks feed a statistic, `average` is the right default.

## A summary

`sort_values` for data, `sort_index` for labels.

A list of keys with a matching list of directions handles multi-key sorts in one call.

Missing values go last in both directions, so reversing is not the same as descending.

`nlargest`/`nsmallest` for a top n; `idxmax`/`idxmin` for a single extreme.

`key=` for derived orderings; ordered categoricals for domain orderings.

`kind="stable"` when ties must keep their order or output must be reproducible.

And sorting is expensive &mdash; do it once, late, and only when the order is part of the answer.

## A closing note

Sorting is expensive and frequently unnecessary, which makes it worth asking what the order is for.

If the answer is "to find the largest", a reduction does it in one pass. If it is "to find the top ten", `nlargest` does it without ordering the rest. If it is "so deduplication keeps the right row", the sort is essential and skipping it makes the result arbitrary. If it is "because the output is a report", the sort is the deliverable and its cost is the point.

Ranking is the same operation asked differently, and its only real subtlety is ties. The default averages them, which produces fractional ranks and surprises people expecting integers; leaderboards usually want `min`, and bands usually want `dense`.

And missing values sort last in both directions, which means reversing an ascending sort is not the same as sorting descending &mdash; a small asymmetry that produces a wrong answer at the ends.

## One more thing

`sort_values` accepts `ignore_index=True`, which renumbers the result rather than carrying the original labels along. That saves a separate `reset_index(drop=True)` when the sorted output is going to be displayed or written with row numbers.

And `nlargest` and `nsmallest` exist on `groupby` objects too, so "the top three per group" is `df.groupby("city")["sales"].nlargest(3)` &mdash; which returns a MultiIndexed Series with the group and the original label, and usually wants `reset_index` before going anywhere else.

## A note on reproducibility

Output that will be committed to a repository, diffed, or compared between runs should be deterministic, and sorting is where non-determinism creeps in.

The default sort is not stable, so tied rows can appear in different orders on different runs or different pandas versions. A file written from that output produces spurious diffs, and a test comparing it fails intermittently.

`kind="stable"` fixes it, at a cost small enough to ignore.

The same applies to group-by, which sorts keys by default but says nothing about the order of rows within a group, and to `drop_duplicates`, whose survivor depends entirely on the current order.

For anything whose output is compared, the rule is: sort explicitly, sort stably, and make the sort keys sufficient to determine the order uniquely.
''',
    [
        {"q": "Where do NaN values go when sorting descending?",
         "options": ["First", "Last, the same as ascending", "They are dropped", "It raises"],
         "answer": 1,
         "why": "They are set aside rather than treated as large or small - which is why reversing an ascending sort is not the same as sorting descending."},
        {"q": "You need the 5 highest rows from 200,000. What is the right call?",
         "options": ["sort_values then head", "nlargest(5, col)", "rank", "max"],
         "answer": 1,
         "why": "It finds the top five without ordering the rest. For a single extreme, idxmax is cheaper still."},
        {"q": "Two values tie. What does the default `rank()` give them?",
         "options": ["Both 2", "The average of the ranks they span, e.g. 2.5", "Both 3", "NaN"],
         "answer": 1,
         "why": "The default is 'average', which produces fractional ranks. Use method='min' for leaderboard-style joint second, or 'dense' for no gaps."},
        {"q": "When is sorting genuinely required rather than avoidable?",
         "options": ["To find a maximum", "Before drop_duplicates, when which row survives matters", "To count rows", "To filter"],
         "answer": 1,
         "why": "drop_duplicates keeps the first row in current order, so without an explicit sort the survivor is arbitrary."},
    ],
)


# ---------------------------------------------------------------------------
# 15. groupby
# ---------------------------------------------------------------------------
topic(
    "groupby_basics",
    "groupby",
    "Summarising",
    "Split, apply, combine - the operation that is the reason to use pandas at "
    "all.",
    _svg(_grid(18, 26, 1, 4, 13) +
         _arrow(38, 46, 54, 32) + _arrow(38, 46, 54, 60) +
         _grid(62, 22, 1, 2, 13) + _grid(62, 54, 1, 2, 13) +
         _arrow(82, 32, 98, 46) + _arrow(82, 60, 98, 46) +
         _grid(106, 39, 1, 2, 13)),
    [
        ("Split, apply, combine",
         "One key, one aggregation, one row per group.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "pune", "goa", "delhi"],
    "sales": [10, 20, 30, 40, 50],
})
print(df.groupby("city")["sales"].sum())
print()
print("the group keys became the INDEX:")
g = df.groupby("city")["sales"].sum()
print("   index:", list(g.index))
print("   type :", type(g).__name__)
print()
print("as_index=False keeps them as a column instead:")
print(df.groupby("city", as_index=False)["sales"].sum())'''),

        ("The object itself is lazy",
         "Nothing is computed until you ask for something.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "pune"],
    "sales": [10, 20, 30],
})
g = df.groupby("city")
print("the object:", type(g).__name__)
print("number of groups:", g.ngroups)
print("sizes:"); print(g.size())
print()
print("look inside one:")
print(g.get_group("pune"))
print()
print("iterate if you must - but an aggregation is nearly always better:")
for name, part in g:
    print("   %-6s %d rows" % (name, len(part)))'''),

        ("Several keys give a hierarchical index",
         "One level per key, in the order you named them.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi", "delhi"],
    "year": [2023, 2024, 2023, 2024],
    "sales": [10, 20, 30, 40],
})
out = df.groupby(["city", "year"])["sales"].sum()
print(out)
print()
print("index levels:", out.index.names)
print()
print("unstack turns the last level into columns:")
print(out.unstack())
print()
print("reset_index gives a flat frame back:")
print(out.reset_index())'''),

        ("Missing keys are dropped by default",
         "Rows whose group key is NaN vanish, and the totals stop adding up.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "city": ["pune", None, "delhi", np.nan],
    "sales": [10, 20, 30, 40],
})
print("total sales in the frame:", int(df["sales"].sum()))
print()
print("default groupby:")
print(df.groupby("city")["sales"].sum())
print("   sums to", int(df.groupby("city")["sales"].sum().sum()), "- 60 went missing")
print()
print("dropna=False keeps them:")
print(df.groupby("city", dropna=False)["sales"].sum())'''),

        ("Aggregating several columns at once",
         "agg with a dict, or named aggregation for clean output names.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "pune", "delhi"],
    "sales": [10, 20, 30, 40],
    "units": [1, 2, 3, 4],
})
print("same function on everything:")
print(df.groupby("city").sum(numeric_only=True))
print()
print("a dict, one entry per column:")
print(df.groupby("city").agg({"sales": "sum", "units": "mean"}))
print()
print("named aggregation - the clearest form:")
print(df.groupby("city").agg(
    total=("sales", "sum"),
    biggest=("sales", "max"),
    orders=("sales", "size"),
))'''),

        ("size versus count",
         "One counts rows, the other counts non-missing values.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi"],
    "sales": [10, np.nan, 30],
})
print("size  - rows per group:")
print(df.groupby("city").size())
print()
print("count - non-missing per column:")
print(df.groupby("city").count())
print()
print("pune has 2 rows but only 1 sales value.")
print()
print("nunique counts DISTINCT values:")
print(df.groupby("city")["sales"].nunique())'''),
    ],
    [
        "<code>groupby</code> splits, applies and combines &mdash; the group keys become the <strong>index</strong> unless you pass <code>as_index=False</code>.",
        "The groupby object is <strong>lazy</strong>; nothing is computed until you aggregate. <code>ngroups</code>, <code>size()</code> and <code>get_group()</code> inspect it.",
        "Several keys give a hierarchical index, one level per key; <code>unstack()</code> turns the last level into columns.",
        "Rows whose key is <strong>missing are dropped by default</strong>, so group totals can silently fail to match the frame total. Pass <code>dropna=False</code>.",
        "<strong>Named aggregation</strong> &mdash; <code>agg(total=(\"sales\", \"sum\"))</code> &mdash; is the clearest form and controls the output names.",
        "<code>size</code> counts <em>rows</em>; <code>count</code> counts <em>non-missing values</em> per column. They differ exactly where data is missing.",
    ],
    '''
title: groupby
intro: Split, apply, combine - the operation that is the reason to use pandas.

## The three steps

`df.groupby("city")["sales"].sum()` does three things:

**Split** the rows into groups by the key.

**Apply** a function to each group.

**Combine** the results into one object, one row per group.

Almost every question about aggregated data has this shape, and recognising it is most of what makes pandas worth using. The alternative in plain Python &mdash; a dict, a loop, a decision about missing keys, another loop to compute the summary &mdash; is a dozen lines that this replaces with one.

## The keys become the index

By default the group keys become the index of the result. That is convenient for lookup and for plotting, and it is a surprise if you expected a plain column.

`as_index=False` keeps them as ordinary columns, giving a result that looks more like a table. `reset_index()` afterwards does the same thing.

Which you want depends on what happens next. If the result feeds a merge or gets written to a file, the flat form is usually easier. If you are going to select groups by name, the index form is better.

Results come back **sorted by key**. `sort=False` skips that sort, which is faster on many groups and gives you the order of first appearance instead.

## The object is lazy

`df.groupby("city")` computes nothing. It returns an object that knows how the rows would be split.

That is why you can inspect it cheaply: `ngroups` counts the groups, `size()` gives rows per group, `get_group(name)` pulls one out, and iterating yields `(name, subframe)` pairs.

Iterating is legitimate for inspection and almost always the wrong way to compute something. The loop runs Python once per group, which is the same performance trap as `apply`. If you find yourself accumulating results in a list inside a groupby loop, there is nearly always an `agg` that does it in one call.

## Several keys

`df.groupby(["city", "year"])` gives one level of index per key, in the order named.

The result is a Series or frame with a **MultiIndex**, which has its own module later. Two operations cover most immediate needs:

`unstack()` moves the last index level into columns, turning a long result into a wide table &mdash; cities down the side, years across the top.

`reset_index()` flattens everything back into ordinary columns.

## Missing keys disappear

This is the behaviour most likely to produce a wrong number quietly.

Rows whose group key is `NaN` are **excluded** by default. They are not put in a separate group; they are dropped.

The result is that group totals do not add up to the frame total, and nothing says so. On a frame where 5% of the key column is missing, every aggregate is quietly computed on 95% of the data.

`dropna=False` keeps them as a group with a `NaN` key.

The habit worth forming: after any group-by that matters, check that the total of the result matches the total of the input. It is one line and it catches this immediately.

## Aggregating

`df.groupby("city").sum(numeric_only=True)` applies one function to every numeric column.

`agg({"sales": "sum", "units": "mean"})` applies a different function per column.

**Named aggregation** is the clearest form and the one to prefer:

```python
df.groupby("city").agg(
    total=("sales", "sum"),
    biggest=("sales", "max"),
    orders=("sales", "size"),
)
```

Each output column is named explicitly, several statistics can come from the same input column, and the result has flat column names rather than the MultiIndex that a dict-of-lists produces. That last point saves a cleanup step almost every time.

Functions can be strings (`"sum"`, `"mean"`, `"nunique"`), NumPy functions, or your own callables. The strings are fastest, because they dispatch to compiled implementations rather than calling back into Python.

## size versus count

A distinction that matters exactly where the data is imperfect.

`size()` counts **rows** in each group, including rows with missing values.

`count()` counts **non-missing values**, per column, so a group of five rows with two gaps in a column reports three for that column.

`nunique()` counts distinct values.

Using `count` where you meant `size` undercounts wherever data is missing, which is precisely where you are least likely to notice.

## Grouping by something that is not a column

`groupby` accepts more than a column name.

**A Series** of the same length groups by its values, which is how you group by a derived value without adding a column:

```python
df.groupby(df["date"].dt.year)["sales"].sum()
```

**A list of Series** gives multiple keys the same way.

**A function** is applied to each index label and groups by the result.

**`pd.Grouper`** handles time: `groupby(pd.Grouper(key="date", freq="ME"))` groups by month without needing a DatetimeIndex, which is what makes it useful alongside other keys.

**`level=`** groups by an index level rather than a column.

That flexibility means most "I need to add a column just to group by it" situations do not need the column.

## as_index, sort and dropna

Three arguments change the shape or content of the result, and all three are worth passing deliberately.

`as_index=False` keeps the keys as columns. The result looks like a table rather than an indexed Series, and it is usually what you want when the output feeds a merge or a file.

`sort=False` skips sorting the keys. On many groups that is a real saving, and it gives order of first appearance instead of sorted order.

`dropna=False` keeps rows whose key is missing. The default drops them, which is the behaviour most likely to produce a total that does not reconcile.

`observed=True` matters for categorical keys: without it, group-by produces a row for **every** category including absent ones, which fills the result with zeros.

## Aggregating strings and other non-numerics

`sum` on a string column concatenates, which is occasionally useful and often an accident.

The aggregations that actually make sense on text:

`"first"` / `"last"` &mdash; a representative value, skipping missing.

`"nunique"` &mdash; how many distinct.

`"count"` &mdash; how many present.

`lambda s: ", ".join(s)` &mdash; collect them into one string.

`list` &mdash; collect them into a list, giving a column of lists. Convenient, and it makes the column `object`, so it is a display or export step rather than something to compute on.

`numeric_only=True` on `sum` and `mean` skips non-numeric columns rather than doing something surprising with them. It is worth passing explicitly, since the default has changed across versions.

## Group-by is a split, and splits can be expensive

The cost of a group-by is roughly: hashing the keys, sorting or grouping the rows, then applying the aggregation once per group.

Three things make it faster:

**A categorical key.** Grouping on integer codes beats grouping on strings, often substantially.

**`sort=False`** when you do not need sorted output.

**A string aggregation name** rather than a lambda. `"sum"` dispatches to compiled code; `lambda s: s.sum()` calls Python once per group.

That last one is the most common avoidable slowdown. `agg("sum")` and `agg(lambda s: s.sum())` produce identical results and differ by an order of magnitude on many groups.

## Checking a group-by

Two checks catch most errors:

**Do the totals reconcile?** `result["sales"].sum()` against `df["sales"].sum()`. If they differ, a key was missing and the rows were dropped.

**Is the group count what you expect?** `df.groupby(k).ngroups` against `df[k].nunique()`. If the group count is larger, the key has variants you did not know about &mdash; whitespace, case, or a type mismatch.

Both are one line, and both catch problems that otherwise surface as a number that is slightly wrong.

## Reading a group-by result

The output shape depends on what you selected and how you aggregated, and knowing which of four shapes you have prevents most downstream confusion.

`df.groupby("k")["v"].sum()` &mdash; a **Series**, indexed by key.

`df.groupby("k")[["v", "w"]].sum()` &mdash; a **DataFrame**, indexed by key.

`df.groupby("k", as_index=False)["v"].sum()` &mdash; a **DataFrame** with the key as a column.

`df.groupby(["k", "j"])["v"].sum()` &mdash; a Series with a **MultiIndex**.

The double-bracket detail is the one people miss: selecting one column with `["v"]` gives a Series, and with `[["v"]]` gives a one-column frame. That difference propagates to everything after it.

## Aggregations worth knowing

Beyond `sum`, `mean` and `count`:

`nunique` &mdash; distinct values per group, which answers "how many different products did each customer buy".

`first` / `last` &mdash; skip missing values, so they combine partial records.

`idxmax` / `idxmin` &mdash; the **label** of the extreme row, which is how you get "the best row per group" rather than just its value: `df.loc[df.groupby("k")["v"].idxmax()]`.

`agg(lambda s: ...)` &mdash; anything else, at the cost of a Python call per group.

`describe()` &mdash; a full summary per group, useful for exploration and too wide for a report.

That `idxmax` pattern is worth remembering; it comes up constantly and the obvious alternatives are all worse.

## Empty groups and missing keys

Two different things that both cause totals not to reconcile.

**Missing keys** &mdash; rows whose group key is `NaN` are dropped unless `dropna=False`.

**Empty groups** &mdash; a categorical key produces a row for every category, including ones with no rows, unless `observed=True`.

The first loses data silently. The second adds rows of zeros that were never in the data. Both defaults have changed across versions, which is a reason to pass them explicitly rather than rely on the current behaviour.

## A summary

Split, apply, combine &mdash; and the group keys become the index unless you say otherwise.

The object is lazy; nothing runs until you aggregate.

Missing keys are dropped by default.

Named aggregation gives flat column names and lets one column feed several statistics.

`size` counts rows, `count` counts non-missing values.

String aggregation names are much faster than lambdas.

`idxmax` plus `.loc` gets the whole extreme row per group.

And check that the group total matches the frame total &mdash; one line that catches the most common silent error here.

## A closing note

Group-by is what pandas is for, and most of its surprises are about what silently does not appear in the result.

Rows whose key is missing are dropped. Categorical keys produce rows for categories that never occurred. `count` and `size` differ wherever data is missing. Each default is defensible on its own, and together they mean a group-by result can fail to reconcile with the frame it came from in several ways at once.

The check that catches all of them is one line: compare the total of the result against the total of the input. If they differ, something was excluded, and the reason will be one of the above.

Beyond that, the practical advice is to prefer named aggregation, which produces flat column names and lets one input column feed several statistics, and to use string aggregation names rather than lambdas, which is the difference between compiled code and a Python call per group.

## One more thing

A groupby object supports `nth(0)`, which takes the nth row of each group and is not the same as `first()`: `first()` skips missing values and `nth(0)` does not. When a group's first row has a gap, the two give different answers, and which you want depends on whether "first" means the first row or the first available value.

`ngroup()` numbers the groups, which is a compact way to turn a set of keys into a single integer label for indexing or plotting.

## In summary

Split, apply, combine &mdash; and the details that decide whether the answer reconciles.

Missing keys are dropped unless you say otherwise. Categorical keys produce rows for categories that never appeared. `size` counts rows and `count` counts values, and they differ wherever data is missing.

Named aggregation is the clearest form and gives flat column names. String aggregation names are much faster than lambdas. And comparing the result's total against the input's total is one line that catches the most common silent failure.
''',
    [
        {"q": "What happens to rows whose group key is NaN?",
         "options": ["They form their own group", "They are dropped by default", "They raise", "They join the first group"],
         "answer": 1,
         "why": "Group totals then quietly fail to match the frame total. Pass dropna=False, and check the totals match after any group-by that matters."},
        {"q": "Why prefer named aggregation over a dict?",
         "options": ["It is faster", "Output columns are named explicitly and come back flat rather than as a MultiIndex", "It handles NaN", "Dicts are deprecated"],
         "answer": 1,
         "why": "It also lets several statistics come from the same input column, and saves a column-flattening step almost every time."},
        {"q": "A group has 5 rows, 2 with a missing sales value. What do `size()` and `count()` report for sales?",
         "options": ["5 and 5", "5 and 3", "3 and 3", "3 and 5"],
         "answer": 1,
         "why": "size counts rows, count counts non-missing values. Using count where you meant size undercounts exactly where data is imperfect."},
        {"q": "Why is iterating over a groupby usually wrong for computing?",
         "options": ["It raises", "It runs Python once per group - the same trap as apply", "It loses the keys", "It sorts wrongly"],
         "answer": 1,
         "why": "Iterating is fine for inspection. If you are accumulating results in a list inside the loop, there is nearly always an agg for it."},
    ],
)


# ---------------------------------------------------------------------------
# 16. transform and filter
# ---------------------------------------------------------------------------
topic(
    "groupby_transform",
    "transform and filter",
    "Summarising",
    "Group statistics broadcast back to every row, and whole groups kept or "
    "dropped.",
    _svg(_grid(20, 24, 1, 4, 13) + _txt(27, 20, "rows", M, 8) +
         _arrow(42, 44, 58, 44) + _txt(50, 36, "agg", M, 7) +
         _grid(66, 37, 1, 2, 13) + _txt(73, 20, "1/group", M, 8) +
         _arrow(88, 44, 104, 44) + _txt(96, 36, "transform", A, 6) +
         _grid(112, 24, 1, 4, 13)),
    [
        ("agg reduces, transform broadcasts",
         "Same statistic, different shape - and transform is the one you can assign "
         "back.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "pune", "delhi"],
    "sales": [10, 20, 30, 40],
})
print("agg gives one row per group:")
print(df.groupby("city")["sales"].sum())
print()
print("transform gives one row per ORIGINAL row:")
print(df.groupby("city")["sales"].transform("sum"))
print()
df["city_total"] = df.groupby("city")["sales"].transform("sum")
df["share"] = (df["sales"] / df["city_total"] * 100).round(1)
print(df)'''),

        ("Why transform beats a merge",
         "The alternative is aggregate then join back, which is three steps and a "
         "chance to lose rows.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "pune"],
    "sales": [10, 20, 30],
})

# the long way
totals = df.groupby("city", as_index=False)["sales"].sum()
totals = totals.rename(columns={"sales": "total"})
merged = df.merge(totals, on="city")
print("aggregate then merge:")
print(merged)

# the short way
df["total"] = df.groupby("city")["sales"].transform("sum")
print()
print("transform:")
print(df)
print()
print("Same answer, one line, and no chance of the merge changing the")
print("row count or the order.")'''),

        ("Centring and ranking within groups",
         "The common uses: a value relative to its own group.",
         '''import pandas as pd

df = pd.DataFrame({
    "team": ["a", "a", "a", "b", "b"],
    "score": [10, 20, 30, 100, 200],
})
g = df.groupby("team")["score"]

df["team_mean"] = g.transform("mean")
df["centred"] = df["score"] - df["team_mean"]
df["rank_in_team"] = g.rank(ascending=False).astype(int)
df["pct_of_team"] = (df["score"] / g.transform("sum") * 100).round(1)

print(df)
print()
print("Every one of these would need a loop or a merge otherwise.")'''),

        ("Filling missing values per group",
         "A group mean is usually a better guess than a global one.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi", "delhi"],
    "temp": [30.0, np.nan, 10.0, np.nan],
})
print("global mean fill:")
print(list(df["temp"].fillna(df["temp"].mean()).round(1)))
print("   both gaps got 20.0, which is right for neither city")
print()
df["filled"] = df["temp"].fillna(df.groupby("city")["temp"].transform("mean"))
print("group mean fill:")
print(df)
print("   pune got 30, delhi got 10")'''),

        ("filter keeps or drops whole groups",
         "The predicate is asked once per group and applies to all its rows.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi", "goa", "goa", "goa"],
    "sales": [10, 20, 5, 1, 2, 3],
})
print("group sizes:"); print(df.groupby("city").size())
print()
big = df.groupby("city").filter(lambda g: len(g) >= 2)
print("groups with at least 2 rows:")
print(big)
print()
print("by an aggregate instead of a count:")
print(df.groupby("city").filter(lambda g: g["sales"].sum() > 6))
print()
print("Note this returns ROWS, not groups - the shape is like the input.")'''),

        ("Choosing between the three",
         "The shape of what you want decides which one you need.",
         '''import pandas as pd

df = pd.DataFrame({"k": ["a", "a", "b"], "v": [1, 2, 3]})

print("rows in :", len(df))
print()
print("agg       ->", len(df.groupby("k")["v"].sum()), "rows (one per group)")
print("transform ->", len(df.groupby("k")["v"].transform("sum")), "rows (one per input row)")
print("filter    ->", len(df.groupby("k").filter(lambda g: len(g) > 1)), "rows (a subset)")
print()
print("Ask: do I want a summary, a new column, or fewer rows?")
print("  a summary   -> agg")
print("  a column    -> transform")
print("  fewer rows  -> filter")'''),
    ],
    [
        "<code>agg</code> reduces to <strong>one row per group</strong>; <code>transform</code> returns <strong>one row per original row</strong>, so it can be assigned straight back as a column.",
        "<code>transform</code> replaces the aggregate-then-merge pattern in one line, with no chance of the join changing the row count or order.",
        "Centring, ranking and computing a share within a group are all <code>transform</code>, and all would otherwise need a loop or a merge.",
        "Filling missing values with a <strong>group</strong> mean uses information a global mean throws away.",
        "<code>filter</code> keeps or drops <strong>whole groups</strong> by a predicate, and returns rows rather than groups.",
        "Choose by output shape: a summary is <code>agg</code>, a new column is <code>transform</code>, fewer rows is <code>filter</code>.",
    ],
    '''
title: transform and filter
intro: Group statistics broadcast back to every row.

## The shape decides the method

Three group-by operations differ only in the shape of what they return, and choosing between them is nearly always obvious once you ask what shape you want.

`agg` returns **one row per group**. A summary table.

`transform` returns **one row per original row**. A new column.

`filter` returns **a subset of the original rows**. Fewer rows, same columns.

Most confusion here is someone reaching for `agg` when they wanted `transform`, then writing a merge to get back to the original shape.

## transform

`df.groupby("city")["sales"].transform("sum")` gives every row its city's total.

Because the result is aligned with the original frame, it assigns straight back:

```python
df["city_total"] = df.groupby("city")["sales"].transform("sum")
df["share"] = df["sales"] / df["city_total"]
```

Two lines for "what fraction of its city's sales is this row", which is a question that otherwise needs an aggregation, a rename, a merge and a check that the merge did not change anything.

That last point is the real argument. The aggregate-then-merge route is three steps, each of which can go wrong: the aggregate can drop `NaN` keys, the merge can multiply rows if the key is not unique, and the result can come back in a different order. `transform` cannot do any of those, because it never leaves the original index.

## What transform accepts

A string naming a built-in (`"sum"`, `"mean"`, `"max"`, `"count"`) is fastest, because it dispatches to compiled code.

A function that maps a Series to a Series of the same length also works &mdash; `transform(lambda s: s - s.mean())` centres within group.

A function returning a **scalar** is broadcast to the whole group, which is why `transform("sum")` works at all.

What it cannot do is change the shape. A function returning a different length raises, which is the difference between `transform` and `apply` and the reason `transform` is predictable.

Some methods exist directly on the groupby object and do not need `transform`: `rank`, `cumsum`, `cumcount`, `shift`, `diff` and `pct_change` all return per-row results already. `g.rank()` is both clearer and faster than `g.transform("rank")`.

## Common uses

**A share of the group total** &mdash; the example above.

**Centring within group** &mdash; `df["v"] - g.transform("mean")`. Standard preprocessing when groups have different baselines.

**Rank within group** &mdash; `g.rank(ascending=False)`. "Where does this row come in its own team."

**Group-wise fill** &mdash; `df["temp"].fillna(g.transform("mean"))`. Filling a missing temperature with the mean for that *city* rather than the mean of everywhere, which uses information a global fill throws away.

**Flagging outliers relative to the group** &mdash; comparing each value against its group's standard deviation.

## filter

`df.groupby("city").filter(lambda g: len(g) >= 2)` keeps every row belonging to a group with at least two rows.

The predicate receives the whole sub-frame and returns a single `True` or `False`. It is asked once per group, and the answer applies to all that group's rows.

The result is **rows**, not groups &mdash; the same columns as the input, with whole groups removed.

Typical uses: dropping groups with too little data to be meaningful, keeping only customers with more than one order, or removing categories below a volume threshold.

Note this is a Python callback per group, so it is slower than an aggregation. For simple size conditions, computing sizes with `transform("size")` and filtering with a boolean mask is faster and does the same thing:

```python
df[df.groupby("city")["sales"].transform("size") >= 2]
```

That form is worth knowing because it composes with other conditions, whereas `filter` does not.

## A note on apply

`groupby(...).apply(func)` is the general escape hatch, and it can return any shape.

That flexibility costs speed &mdash; it is a Python call per group &mdash; and predictability, since the shape of the result depends on what the function returned. In pandas 2.2 it also warns about whether the grouping columns are passed to the function, which is a sign of how awkward its semantics have become.

Reach for `agg`, `transform` or `filter` first. They cover the large majority of cases, run in compiled code, and return a shape you can predict from the method name alone.

## Ranking and cumulative operations within groups

Several methods on a groupby already return one row per input row, so they need no `transform`:

`cumsum`, `cumcount`, `cummax` &mdash; running totals and counters within each group.

`rank` &mdash; position within the group.

`shift`, `diff`, `pct_change` &mdash; comparison with the previous row **of the same group**.

That last set matters more than it looks. `df["v"].diff()` on a frame containing several entities computes a difference across the boundary between one entity and the next, which is meaningless. `df.groupby("id")["v"].diff()` does not.

Any time you use `shift`, `diff` or `rolling` on panel data &mdash; several entities stacked in one frame &mdash; the group-by version is almost certainly the one you want, and using the plain version is a quiet, plausible-looking error.

`cumcount()` numbers the rows within each group from zero, which is how you take "the first three per group" or label repeat visits.

## Percentages and shares

The single most common `transform` is a share of the group:

```python
df["share"] = df["sales"] / df.groupby("city")["sales"].transform("sum")
```

Two variants worth knowing:

A share of the **whole frame** needs no group-by: `df["sales"] / df["sales"].sum()`.

A share **within a nested group** takes a list of keys: `transform("sum")` on `groupby(["region", "city"])`.

Because the denominator comes back aligned, these compose &mdash; you can compute a share of city and a share of region in the same frame and compare them.

## Standardising within groups

Centring and scaling relative to a group is standard preprocessing when groups have different baselines &mdash; different stores, different sensors, different years:

```python
g = df.groupby("store")["sales"]
df["z"] = (df["sales"] - g.transform("mean")) / g.transform("std")
```

Two cautions. A group with one row has a standard deviation of `NaN`, so the result is `NaN` for that row rather than zero. And a group with zero variance divides by zero, giving `inf`. Both are worth handling explicitly rather than discovering downstream.

## Filtering by a group property

`filter` takes a callback per group, which is flexible and slow.

For the common cases, a `transform` and a boolean mask is faster and composes better:

```python
df[df.groupby("city")["sales"].transform("size") >= 5]
df[df.groupby("city")["sales"].transform("sum") > 1000]
```

The mask form can be combined with other conditions using `&`, which `filter` cannot. It is also easier to reason about, because it is the same masking you use everywhere else.

Reach for `filter` when the predicate genuinely needs the whole sub-frame &mdash; a condition involving several columns at once, or a statistical test per group.

## Why apply is the last resort

`groupby(...).apply(func)` can return anything, which is its appeal and its problem.

It is a Python call per group, so it is slow.

The shape of the result depends on what the function returned, which makes it unpredictable to read.

And in pandas 2.2 it warns about whether the grouping columns are passed to the function, because the historical behaviour was ambiguous enough to need changing.

Before using it, check whether the operation is:

a summary per group &mdash; `agg`;

a value per row &mdash; `transform`, or a groupby method like `rank` or `cumsum`;

a subset of rows &mdash; a mask built from `transform`, or `filter`;

several columns from one computation &mdash; `agg` with named aggregation.

Those four cover the large majority of cases, run in compiled code, and return a shape you can predict from the method name.

## A worked example

A frequent request: for each customer, how does this order compare with their own average, and where does it rank among their orders?

```python
g = df.groupby("customer")["amount"]

df["cust_mean"] = g.transform("mean")
df["vs_mean"]   = df["amount"] - df["cust_mean"]
df["rank"]      = g.rank(ascending=False)
df["share"]     = df["amount"] / g.transform("sum")
df["order_no"]  = df.groupby("customer").cumcount() + 1
```

Five columns, no loop, no merge, and every one aligned with the original rows.

Written with an aggregate-and-merge it would be four separate summaries and four joins, each of which could change the row count.

## When transform is not enough

`transform` requires the function to return either a scalar or something the same length as the group. Two cases fall outside that.

**A different number of rows per group** &mdash; taking the top two per group, for instance. That is a filter: rank with `transform` or a groupby method, then mask.

**Several columns from one computation** &mdash; `transform` operates column by column, so a calculation needing two columns together does not fit. `groupby(...).apply` handles it, or restructure so each output column is computed separately.

## filter versus a mask

They do the same job with different trade-offs.

`filter(lambda g: ...)` &mdash; the callback sees the whole sub-frame, so any condition is expressible. It is a Python call per group.

`df[df.groupby(k)[c].transform("size") >= n]` &mdash; compiled, faster, and composes with other conditions using `&`.

Use the mask for simple conditions on a single statistic, which is most of them. Use `filter` when the predicate genuinely needs several columns or a computation with no vectorised form.

## A summary

`agg` reduces, `transform` broadcasts, `filter` selects rows.

`transform` assigns straight back, because it keeps the original index.

It replaces aggregate-then-merge, without the risk of changing row count or order.

Group-wise `rank`, `cumsum`, `cumcount`, `shift` and `diff` are methods in their own right &mdash; no `transform` needed.

On panel data, always use the group-wise `shift`/`diff`, or the comparison crosses between entities.

Group fills use information a global fill throws away.

And prefer a `transform`-built mask to `filter` for simple size or total conditions.

## A closing note

`transform` is the operation that removes the most unnecessary joins from real pandas code.

The pattern it replaces &mdash; aggregate to a summary, rename the column, merge it back &mdash; is three steps, each of which can change the row count or the order, and all of which exist only to get a group statistic aligned with the rows it came from. `transform` does that by construction, because it never leaves the original index.

Once you have it, a family of questions becomes one line each: this row's share of its group, its rank within its group, its distance from its group's mean, its group's size as a filter.

`filter` is the less-used sibling and is usually better expressed as a mask built from `transform`, which composes with other conditions and runs in compiled code.

Between `agg`, `transform` and a mask, the general-purpose `apply` is rarely needed &mdash; which is the point, because it is the slow and unpredictable one.

## One more thing

`transform` accepts a list of functions in recent pandas, returning one column per function with a hierarchical column index. That is occasionally convenient and usually clearer written as separate assignments, since each output then has a name you chose.

More useful is that `transform` works on a whole frame, not just one column: `df.groupby("k").transform("mean")` returns a frame of group means for every numeric column at once, aligned with the original rows. Subtracting it centres the entire frame within groups in a single expression.

## In summary

Three operations, distinguished only by the shape they return: `agg` gives one row per group, `transform` one row per input row, `filter` a subset of rows.

`transform` is the one that removes work, because it replaces the aggregate-rename-merge pattern with a single expression that cannot change the row count or the order.

Prefer the group-by methods that already return per-row results &mdash; `rank`, `cumsum`, `cumcount`, `shift`, `diff` &mdash; over `transform` where they apply, and use the group-wise forms on panel data so comparisons do not cross between entities.
''',
    [
        {"q": "What is the difference between `agg` and `transform`?",
         "options": ["None", "agg returns one row per group; transform returns one row per original row", "transform is faster", "agg works on strings only"],
         "answer": 1,
         "why": "Because transform stays aligned with the original index, it assigns straight back as a column."},
        {"q": "Why is `transform` safer than aggregate-then-merge?",
         "options": ["It is newer", "It never leaves the original index, so it cannot change the row count or order", "It handles strings", "It is lazy"],
         "answer": 1,
         "why": "The merge route can drop NaN keys, multiply rows on a non-unique key, or reorder the result. transform can do none of those."},
        {"q": "What does `groupby(...).filter(pred)` return?",
         "options": ["Groups", "Rows belonging to groups where the predicate was True", "One row per group", "A boolean Series"],
         "answer": 1,
         "why": "The predicate is asked once per group and applies to all its rows. The result has the same columns as the input."},
        {"q": "Why prefer `g.rank()` over `g.transform('rank')`?",
         "options": ["No difference", "rank is already a per-row groupby method - it is clearer and faster", "transform cannot rank", "rank sorts the frame"],
         "answer": 1,
         "why": "cumsum, cumcount, shift, diff and pct_change are the same - they return per-row results without needing transform."},
    ],
)


# ---------------------------------------------------------------------------
# 17. Counting and binning
# ---------------------------------------------------------------------------
topic(
    "counting_and_binning",
    "Counting and Binning",
    "Summarising",
    "value_counts, cut and crosstab - turning raw values into the categories you "
    "actually want to count.",
    _svg(_grid(18, 26, 1, 5, 12) +
         _arrow(36, 52, 54, 52) +
         _box(62, 26, 18, 20, S, A) + _box(62, 48, 18, 20, S, A) +
         _txt(104, 40, "low / high", M, 8)),
    [
        ("value_counts is the first thing to run",
         "Counts, shares, and the missing values you would otherwise not see.",
         '''import pandas as pd
import numpy as np

s = pd.Series(["a", "b", "a", "c", "a", None])

print(s.value_counts())
print()
print("with missing values included:")
print(s.value_counts(dropna=False))
print()
print("as shares:")
print((s.value_counts(normalize=True) * 100).round(1))
print()
print("sorted by label instead of by count:")
print(s.value_counts().sort_index())'''),

        ("cut makes bands from numbers",
         "You choose the edges, and every value lands in exactly one band.",
         '''import pandas as pd

ages = pd.Series([5, 17, 18, 35, 64, 65, 90])

bands = pd.cut(ages, bins=[0, 17, 64, 200],
               labels=["child", "adult", "senior"])
print(pd.DataFrame({"age": ages, "band": bands}))
print()
print("bins are (left, right] - right-inclusive by default,")
print("so 17 is a child and 18 is an adult.")
print()
print("counts per band:")
print(bands.value_counts().sort_index())
print()
print("the result is a category, with an order:")
print("   ", list(bands.cat.categories))'''),

        ("Values outside the bins become NaN",
         "Silently, which is how rows disappear from a summary.",
         '''import pandas as pd

s = pd.Series([-5, 10, 50, 500])
b = pd.cut(s, bins=[0, 100])

print(pd.DataFrame({"value": s, "bin": b.astype(str)}))
print()
print("counted:", int(b.notna().sum()), "of", len(s))
print("   -5 and 500 fall outside 0-100 and became NaN")
print()
print("use open-ended edges when the range is not known:")
import numpy as np
safe = pd.cut(s, bins=[-np.inf, 100, np.inf], labels=["low", "high"])
print("   ", list(safe))'''),

        ("qcut splits by quantile instead",
         "Equal-sized groups rather than equal-width bands.",
         '''import pandas as pd
import numpy as np

s = pd.Series([1, 2, 3, 4, 5, 6, 100, 200])

print("cut - equal WIDTH, so the outliers dominate:")
print(pd.cut(s, 4).value_counts().sort_index())
print()
print("qcut - equal COUNT per bucket:")
print(pd.qcut(s, 4).value_counts().sort_index())
print()
print("with names:")
print(list(pd.qcut(s, 4, labels=["q1", "q2", "q3", "q4"])))
print()
print("qcut raises when there are too many repeats to split evenly -")
print("duplicates='drop' merges the edges instead.")'''),

        ("crosstab counts two things at once",
         "A frequency table of one variable against another.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi", "delhi", "delhi"],
    "plan": ["free", "paid", "free", "free", "paid"],
})
print(pd.crosstab(df["city"], df["plan"]))
print()
print("with totals:")
print(pd.crosstab(df["city"], df["plan"], margins=True))
print()
print("as row percentages:")
print((pd.crosstab(df["city"], df["plan"], normalize="index") * 100).round(0))'''),

        ("Counting into a summary table",
         "value_counts on a group, and the two ways to lay it out.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi", "delhi", "delhi"],
    "plan": ["free", "paid", "free", "free", "paid"],
})
counts = df.groupby("city")["plan"].value_counts()
print("long form:")
print(counts)
print()
print("wide form:")
print(counts.unstack(fill_value=0))
print()
print("which is what crosstab gave you directly - crosstab is the")
print("shortcut, groupby is the general tool.")'''),
    ],
    [
        "<code>value_counts</code> gives counts; <code>normalize=True</code> gives shares and <code>dropna=False</code> reveals the missing values.",
        "<code>pd.cut</code> bands by <strong>edges you choose</strong>, and bins are <code>(left, right]</code> &mdash; right-inclusive.",
        "Values <strong>outside</strong> the bins become NaN silently &mdash; use <code>-np.inf</code> / <code>np.inf</code> edges when the range is unknown.",
        "<code>pd.qcut</code> splits by quantile, giving equal-sized groups rather than equal-width bands.",
        "<code>pd.crosstab</code> counts one variable against another, with <code>margins</code> for totals and <code>normalize</code> for percentages.",
        "<code>groupby(...)[col].value_counts().unstack()</code> is the general form of what crosstab does in one call.",
    ],
    '''
title: Counting and Binning
intro: value_counts, cut and crosstab.

## value_counts

The most-used single method in exploratory work, and the first thing to run on any categorical column.

By default it counts each distinct value and sorts by frequency, descending. Three arguments change what it tells you:

`normalize=True` gives proportions rather than counts, which is what you want when comparing two datasets of different sizes.

`dropna=False` includes missing values in the count. Without it, missing data is invisible here &mdash; and "invisible" is exactly the wrong property for the thing you most need to notice.

`sort=False` keeps the values in their natural order rather than by frequency; `.sort_index()` afterwards does the same job more explicitly.

On a DataFrame, `df.value_counts()` counts distinct **combinations** of all columns, which is a quick way to find duplicated records.

## cut

`pd.cut` turns a numeric column into named bands.

```python
pd.cut(ages, bins=[0, 17, 64, 200], labels=["child", "adult", "senior"])
```

Bins are **right-inclusive** by default &mdash; the interval is `(left, right]`. So with an edge at 17, the value 17 is a child and 18 is an adult. `right=False` flips this to `[left, right)`, which is what you usually want for things like age where the convention is "18 and over".

Getting this backwards produces an off-by-one at every boundary, and it does not raise.

The result is a **categorical** with an order, so it sorts correctly and groups efficiently.

## Values outside the bins vanish

Anything below the first edge or above the last becomes `NaN`.

This is the failure mode to watch. A negative value, an outlier, a sentinel like `-1` or `9999` &mdash; all silently disappear from every count that follows, and the totals no longer match the row count.

Two defences. Use `-np.inf` and `np.inf` as the outer edges when the range is not known in advance. And check `result.notna().sum()` against `len(df)` after binning, which takes one line and catches it immediately.

Passing an integer instead of a list &mdash; `pd.cut(s, 4)` &mdash; makes four equal-width bins spanning the data, so nothing falls outside. That is safe but rarely gives meaningful boundaries.

## qcut

`pd.cut` makes bands of equal **width**. `pd.qcut` makes bands of equal **count**.

The difference matters whenever the data is skewed. With a few large outliers, equal-width bins put almost every row in the first bucket and leave the rest nearly empty. Equal-count bins give you quartiles, deciles, or whatever split you asked for, each with the same number of rows.

Use `cut` when the boundaries have external meaning &mdash; age brackets, price tiers, pass marks. Use `qcut` when you want relative position &mdash; top quartile, bottom decile.

`qcut` raises when repeated values make an even split impossible. `duplicates="drop"` merges the offending edges and returns fewer bins than requested, which is usually acceptable and worth knowing about before it fails on a column of mostly-zeros.

## crosstab

`pd.crosstab(df["city"], df["plan"])` gives a frequency table: cities down the side, plans across the top, counts in the cells.

`margins=True` adds row and column totals.

`normalize="index"` gives row percentages, `"columns"` gives column percentages, and `True` gives the share of the grand total. Row percentages are usually the interesting ones &mdash; "what proportion of Delhi users are on the paid plan" &mdash; and are not the default.

`values=` with `aggfunc=` turns it from a count into any aggregation, at which point it is `pivot_table` with different spelling.

## The general form

`crosstab` is a shortcut. The general tool is group-by:

```python
df.groupby("city")["plan"].value_counts().unstack(fill_value=0)
```

That gives the same table. The long form &mdash; before `unstack` &mdash; is often more useful for further processing, and the wide form is better for reading.

Knowing both matters because `crosstab` runs out of road quickly: more than two variables, custom aggregations, or anything feeding another computation is easier with group-by. Reach for `crosstab` when you want a table to look at, and group-by when the result has somewhere else to go.

## Counting combinations

`df.value_counts()` on a whole frame counts distinct **row** combinations, which is a fast way to find duplicated records or to see which pairs of categories actually occur.

`df[["city", "plan"]].value_counts()` restricts it to two columns and gives a Series with a MultiIndex &mdash; the long form of a crosstab.

`normalize=True` works here too, giving the share of each combination.

`df.groupby(["city", "plan"]).size()` gives the same numbers with a different name, and is worth knowing because it composes with other group-by operations.

## Binning with meaningful edges

The edges are usually the interesting decision, and there are three sources for them.

**External definitions** &mdash; age brackets, tax bands, grade boundaries. These come from the domain, and `cut` with an explicit list is right.

**The data's distribution** &mdash; quartiles, deciles. `qcut` with a count.

**Round numbers** &mdash; `np.arange(0, 101, 10)` for ten-point bands. Readable, and often better for communication than quantiles even when quantiles are statistically neater.

`cut` also accepts an integer, giving equal-width bins across the observed range. The boundaries are then arbitrary decimals, which is fine for a quick look and poor for anything anyone reads.

`retbins=True` returns the edges alongside the result, which is how you apply the *same* bins to another dataset later &mdash; important when comparing two periods, because bins computed separately are not comparable.

## Ordered categories from binning

`cut` and `qcut` return an **ordered categorical**. That has three useful consequences.

Sorting works in bin order rather than alphabetically, which is why `value_counts().sort_index()` produces a sensible table.

Comparison works: `df[df["band"] > "low"]` is meaningful.

Group-by on the result includes every bin, including empty ones &mdash; which is usually desirable in a report and occasionally surprising. `observed=True` restricts it to occupied bins.

## Histograms

`np.histogram` and `plt.hist` both bin and count in one step, and `pd.cut` plus `value_counts` gives the same numbers with labels you control.

The bin count matters more than people expect: too few hides structure, too many turns the distribution into noise. `bins="auto"` in NumPy applies a rule of thumb, and looking at two or three bin counts is usually more informative than trusting one.

For comparing distributions between groups, counts are misleading when the groups are different sizes. `normalize=True`, or `crosstab(..., normalize="index")`, puts them on a comparable footing.

## The checks worth making

After binning, three lines:

```python
binned.isna().sum()          # how many fell outside the bins
binned.value_counts().sort_index()   # is any bin empty or dominant
len(binned) == len(df)       # nothing lost
```

The first is the one that matters. Values outside the edges become `NaN` silently, and every count after that is computed on a subset without saying so.

And when the bins will be reused &mdash; on next month's data, or on a test set &mdash; save the edges rather than recomputing them. Bins derived from different data are not comparable, and quantile bins in particular will differ every time.

## Reusing bins across datasets

Bins computed from one dataset do not apply to another, and comparing two sets of quantile bins computed separately is meaningless &mdash; the boundaries differ.

`retbins=True` returns the edges:

```python
train_binned, edges = pd.cut(train["score"], 4, retbins=True)
test_binned = pd.cut(test["score"], bins=edges)
```

The test data now uses the training boundaries, which is what makes the two comparable. Values outside the training range fall outside the bins and become `NaN`, which is honest &mdash; they are outside what the bins describe.

The same applies to any before-and-after comparison, and to production scoring against a model trained earlier. Saving the edges alongside the model is part of saving the model.

## Counting with weights

`value_counts` counts rows. When each row represents several things &mdash; a quantity column, a sampling weight &mdash; counting rows is the wrong number.

`df.groupby("city")["qty"].sum()` is the weighted version.

`np.bincount`-style weighting has no direct `value_counts` equivalent, and group-by is the general answer.

For crosstabs, `pd.crosstab(a, b, values=c, aggfunc="sum")` weights the cells by another column.

## Cardinality as a diagnostic

`nunique()` against `len(df)` classifies a column in one number:

**1** &mdash; constant; carries no information.

**2** &mdash; binary.

**Low, relative to the rows** &mdash; a category; convert it.

**Close to the row count** &mdash; an identifier; not a feature.

**Moderate and unexpected** &mdash; usually a sign of unnormalised text, where the same value appears in several spellings.

Running `df.nunique().sort_values()` across a new frame takes a second and tells you what kind of column each one is, which is the first thing you need to know.

## A summary

`value_counts` first, with `dropna=False` and sometimes `normalize=True`.

`cut` for meaningful boundaries, `qcut` for equal-sized groups.

Bins are right-inclusive by default; `right=False` flips it.

Values outside the edges become `NaN` silently &mdash; use infinite outer edges, and check the count afterwards.

Save the edges when the bins will be reused.

`crosstab` for a table to look at; `groupby` plus `unstack` when the result goes somewhere else.

And weight the counts when rows are not the unit you actually mean to count.

## A closing note

Counting is the least glamorous operation in pandas and the one that catches the most problems.

`value_counts` on every categorical column, run before any analysis, finds the typos, the stray capitals, the trailing spaces and the categories nobody mentioned. Each of those would otherwise become a silently split group in an aggregation.

Binning turns continuous data into the categories a question is actually about &mdash; age brackets, price tiers, quartiles. The two things to hold onto are that bins are right-inclusive by default, and that values outside the edges vanish into `NaN` without a word.

Both are worth checking with one line each: the boundary convention against a value that sits on a boundary, and the count of non-missing results against the row count. Together they take a few seconds and prevent an entire class of quietly wrong summaries.

## Two more things worth knowing

`pd.cut` accepts `labels=False`, which returns the **bin number** rather than a label. That is what you want when the bins feed a model or a further computation rather than a report, and it avoids the categorical dtype entirely.

`value_counts` has a `bins=` argument that bins and counts in one step for numeric data: `s.value_counts(bins=5)` is `pd.cut` followed by counting, which is convenient for a quick look at a distribution.

And `pd.crosstab` accepts lists for either axis, giving hierarchical rows or columns, and `dropna=False` keeps combinations that never occurred. The second is worth knowing when two crosstabs must have the same shape to be compared &mdash; without it, a category absent from one dataset simply does not appear, and the tables no longer line up.

## Counting for comparison

Counts answer "how many". Comparing two groups needs proportions, because raw counts confound size with rate.

A city with twice the population has twice the customers on any plan, and comparing the counts says nothing. `normalize="index"` on a crosstab, or `value_counts(normalize=True)` within a group-by, puts them on the same footing:

```python
(df.groupby("city")["plan"]
   .value_counts(normalize=True)
   .unstack(fill_value=0)
   .round(3))
```

That reads as "what fraction of each city's customers are on each plan", which is usually the question people mean.

The reverse normalisation &mdash; `normalize="columns"` &mdash; answers a different question: "what fraction of paid customers are in each city". Both are legitimate and they are not interchangeable, and stating which one a table shows is worth a line of text next to it, because the numbers alone do not say.

## In summary

`value_counts` on every categorical column is the cheapest diagnostic in pandas, and it finds the variants that would otherwise split a group-by silently.

`cut` bands by boundaries you choose and `qcut` by quantiles, and the choice depends on whether the boundaries have external meaning or you want equal-sized groups.

Two things to check every time: which convention the bin edges use, since they are right-inclusive by default, and how many values fell outside the edges, since those become `NaN` without a word and every count afterwards is computed on a subset.
''',
    [
        {"q": "In `pd.cut(ages, bins=[0, 17, 64, 200])`, which band does 17 fall into?",
         "options": ["The second", "The first, because bins are right-inclusive (left, right]", "Neither", "It raises"],
         "answer": 1,
         "why": "Pass right=False for [left, right), which is what age conventions usually want. Getting it backwards is an off-by-one at every boundary, and it does not raise."},
        {"q": "What happens to a value below the first bin edge?",
         "options": ["It joins the first bin", "It becomes NaN, silently", "It raises", "It creates a new bin"],
         "answer": 1,
         "why": "Outliers and sentinels disappear from every later count. Use -np.inf/np.inf edges, and check notna().sum() against len(df)."},
        {"q": "When should you use `qcut` rather than `cut`?",
         "options": ["Always", "When you want equal-sized groups rather than equal-width bands - especially on skewed data", "For text columns", "Never"],
         "answer": 1,
         "why": "With a few large outliers, equal-width bins put nearly every row in the first bucket. Use cut when boundaries have external meaning."},
        {"q": "Why pass `dropna=False` to `value_counts`?",
         "options": ["It is faster", "Missing values are otherwise invisible - exactly the wrong property for what you most need to notice", "It sorts the result", "It normalises"],
         "answer": 1,
         "why": "Together with normalize=True for shares, these are the two arguments worth reaching for by default."},
    ],
)


# ---------------------------------------------------------------------------
# 18. apply, map and vectorising
# ---------------------------------------------------------------------------
topic(
    "apply_and_map",
    "apply, map and Vectorising",
    "Summarising",
    "The escape hatch, what it costs, and the vectorised form that usually "
    "replaces it.",
    _svg(_txt(40, 22, "apply", "#e88", 9) +
         _grid(20, 30, 1, 4, 12) + _arrow(40, 54, 40, 66) + _txt(40, 76, "slow", "#e88", 8) +
         _txt(116, 22, "vectorised", A, 8) +
         _box(96, 30, 44, 24, S, A) + _txt(118, 76, "fast", A, 8)),
    [
        ("map replaces values from a dict",
         "The simplest of the three, and it is a lookup rather than a loop you write.",
         '''import pandas as pd

s = pd.Series(["a", "b", "c", "z"])
lookup = {"a": "apple", "b": "banana", "c": "cherry"}

print("map with a dict:")
print(list(s.map(lookup)))
print("   'z' was not in the dict and became NaN")
print()
print("na_action='ignore' skips missing input instead of calling on it:")
print(list(pd.Series(["a", None]).map(lookup, na_action="ignore")))
print()
print("keep unmatched values with a fallback:")
print(list(s.map(lookup).fillna(s)))'''),

        ("apply on a Series runs your function per value",
         "Which is a Python loop, however it is spelled.",
         '''import pandas as pd

s = pd.Series([1, 2, 3, 4])

print("apply:", list(s.apply(lambda v: v * 2 + 1)))
print("vectorised:", list(s * 2 + 1))
print("same:", list(s.apply(lambda v: v * 2 + 1)) == list(s * 2 + 1))
print()
print("apply is not doing anything clever - it calls the function")
print("once per element and collects the results.")
print()
print("it can return anything, which is its only real advantage:")
print("   ", list(s.apply(lambda v: "even" if v % 2 == 0 else "odd")))'''),

        ("What it costs",
         "The same result, an order of magnitude apart.",
         '''import pandas as pd
import numpy as np
import time

n = 200_000
s = pd.Series(np.arange(n))

t = time.perf_counter(); a = s.apply(lambda v: v * 2 + 1); t_apply = time.perf_counter() - t
t = time.perf_counter(); b = s * 2 + 1; t_vec = time.perf_counter() - t
t = time.perf_counter(); c = pd.Series([v * 2 + 1 for v in s]); t_list = time.perf_counter() - t

print("apply             : %.4f s" % t_apply)
print("list comprehension: %.4f s" % t_list)
print("vectorised        : %.4f s" % t_vec)
print("apply is %.0fx slower than vectorised" % (t_apply / max(t_vec, 1e-9)))
print()
print("same values:", a.tolist() == b.tolist() == c.tolist())
print("dtypes     : apply %s, vectorised %s" % (a.dtype, b.dtype))
print("   equals() would say False - it compares dtype too, and going")
print("   through Python ints can widen the result.")'''),

        ("apply on a DataFrame gets whole rows or columns",
         "axis=1 is the row-wise form, and it is the slowest thing here.",
         '''import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})

print("axis=0 (default): the function gets each COLUMN")
print(df.apply(lambda col: col.max() - col.min()))
print()
print("axis=1: the function gets each ROW as a Series")
print(list(df.apply(lambda row: row["a"] * row["b"], axis=1)))
print()
print("but that same result is a single vectorised expression:")
print(list(df["a"] * df["b"]))
print()
print("axis=1 builds a Series object per row. It is the form most")
print("worth removing when a script is slow.")'''),

        ("Replacing the common apply patterns",
         "Almost every row-wise apply has a vectorised equivalent.",
         '''import pandas as pd
import numpy as np

df = pd.DataFrame({"score": [10, 55, 80], "city": ["pune", "delhi", "pune"]})

print("a conditional  ->  np.where")
print("  ", list(np.where(df["score"] >= 50, "pass", "fail")))
print()
print("several conditions  ->  np.select")
conds = [df["score"] >= 80, df["score"] >= 50]
print("  ", list(np.select(conds, ["A", "B"], default="C")))
print()
print("a lookup  ->  map")
print("  ", list(df["city"].map({"pune": 1, "delhi": 2})))
print()
print("bands  ->  pd.cut")
print("  ", list(pd.cut(df["score"], [0, 49, 79, 100], labels=["low", "mid", "high"])))
print()
print("string work  ->  .str")
print("  ", list(df["city"].str.upper()))'''),

        ("When apply is the right answer",
         "It exists for a reason - just not for arithmetic.",
         '''import pandas as pd

df = pd.DataFrame({"text": ["a b c", "d e", "f"]})

# genuinely awkward to vectorise: a per-row parse returning several fields
def parse(row):
    parts = row["text"].split()
    return pd.Series({"first": parts[0], "n": len(parts)})

print(df.apply(parse, axis=1))
print()
print("Reasonable uses:")
print("  - calling an existing scalar function you cannot rewrite")
print("  - per-row logic with no array equivalent")
print("  - small frames, where clarity beats speed")
print()
print("The test: is the frame big enough for the difference to matter?")
print("On 200 rows, apply is fine. On 200,000 it is the bottleneck.")'''),
    ],
    [
        "<code>map</code> looks values up in a dict or Series; unmatched keys become <strong>NaN</strong>, so add a fallback if that is not what you want.",
        "<code>apply</code> on a Series calls your function <strong>once per element</strong> &mdash; a Python loop, however it is spelled.",
        "<code>apply(axis=1)</code> builds a Series per row and is the slowest common pattern in pandas.",
        "Most row-wise applies have a vectorised equivalent: <code>np.where</code>, <code>np.select</code>, <code>map</code>, <code>pd.cut</code>, <code>.str</code>.",
        "<code>apply</code> is legitimate for per-row logic with no array equivalent, for wrapping an existing scalar function, and on small frames.",
        "The test is size: on 200 rows <code>apply</code> is fine; on 200,000 it is usually the bottleneck.",
    ],
    '''
title: apply, map and Vectorising
intro: The escape hatch, what it costs, and the form that usually replaces it.

## Three different things

`Series.map` looks each value up in a dict, a Series, or a function. It is for **substitution**.

`Series.apply` calls a function on each value. It is for **computation** that has no array form.

`DataFrame.apply` calls a function on each column (`axis=0`) or each row (`axis=1`).

`DataFrame.map` &mdash; formerly `applymap` &mdash; calls a function on every individual cell.

They look interchangeable in small examples and are not, and the differences show up in both speed and behaviour with missing values.

## map

`s.map({"a": "apple"})` replaces values by lookup.

Anything not in the mapping becomes `NaN`. That is a reasonable default and frequently not what people want &mdash; a typo in a key silently blanks a column.

`s.map(lookup).fillna(s)` keeps the original where there was no match, which is usually the intended behaviour for a partial rename.

`na_action="ignore"` skips missing input rather than passing `NaN` to the function, which matters when the function would fail on it.

`map` with a dict is fast, because it is a lookup rather than a call. `map` with a **function** is exactly as slow as `apply`.

## What apply costs

`apply` does not vectorise anything. It calls your function once per element and assembles the results.

The third editor measures it: on 200,000 rows, `apply` runs roughly an order of magnitude slower than the equivalent arithmetic, and is no faster than a plain list comprehension &mdash; because that is essentially what it is.

There is a persistent belief that `apply` is "the pandas way" and therefore fast. It is neither. It is the escape hatch for when there is no array expression.

## axis=1 is the expensive one

`df.apply(func, axis=1)` constructs a **Series object for every row** and passes it to your function. That is object creation per row on top of the Python call.

It is the single most common reason a pandas script is slow, and it is nearly always replaceable.

The tell is a lambda that indexes into the row: `lambda row: row["a"] * row["b"]`. That is `df["a"] * df["b"]`, which operates on whole columns in compiled code.

## The replacements

Nearly every row-wise `apply` is one of a handful of patterns:

**A conditional** &mdash; `np.where(cond, a, b)`. The vectorised if/else.

**Several conditions** &mdash; `np.select([c1, c2], [v1, v2], default=v3)`. Evaluated in order, first match wins.

**A lookup** &mdash; `map` with a dict.

**Numeric bands** &mdash; `pd.cut`.

**String work** &mdash; the `.str` accessor.

**Row-wise arithmetic** &mdash; ordinary column arithmetic.

**A group statistic per row** &mdash; `groupby(...).transform(...)`.

Between them these cover the large majority of real cases. When you find yourself writing `apply(axis=1)`, it is worth thirty seconds to check this list first.

## When apply is right

It genuinely earns its place in a few situations.

**Wrapping an existing scalar function** you cannot or should not rewrite &mdash; a parser, a validator, a call into another library.

**Per-row logic with no array equivalent** &mdash; something that branches on several columns in a way `np.select` cannot express cleanly, or that returns a variable number of fields.

**Returning several columns at once**, by returning a Series from the function, as the last editor shows.

**Small frames**, where the whole operation takes microseconds either way and clarity is the only thing that matters.

That last point deserves emphasis. Optimising an `apply` over 200 rows is wasted effort, and a readable `apply` can be better code than a clever vectorised expression nobody can modify. The question is always whether the frame is large enough for the difference to matter.

## If it must stay a loop

When the logic really is sequential and per-row, and the frame is large, pandas is not the tool. The options are to move the loop into NumPy, compile it with Numba, or restructure the problem.

What is never right is `iterrows`. It is slower than `apply(axis=1)`, it loses dtypes by converting each row to an object Series, and there is no situation where it is the best available option. `itertuples` is considerably faster if you genuinely need to iterate, and preserves types.

## DataFrame.map and the applymap rename

`DataFrame.map(func)` applies a function to **every cell**. It was called `applymap` until pandas 2.1, and the old name is deprecated.

It is rarely the right tool. Applying a function to every cell of a table usually means either the operation belongs on specific columns, or the frame should have been reshaped first.

The legitimate uses are formatting for display and elementwise type coercion across a homogeneous frame &mdash; both of which are end-of-pipeline steps.

## Returning several values

A function that returns a Series gives several columns:

```python
df.apply(lambda r: pd.Series({"a": ..., "b": ...}), axis=1)
```

That works and is slow twice over &mdash; a Python call and a Series construction per row.

The faster shape is usually to compute each output column separately with vectorised expressions, even if that means traversing the input more than once. Three passes over a column in compiled code beat one pass in Python by a wide margin.

When the computation genuinely produces several values at once and cannot be split, `zip(*df.apply(...))` or building lists and assigning at the end avoids the Series construction.

## result_type and the empty-frame trap

`df.apply(func, axis=1)` on an **empty** frame does not call the function at all, so pandas cannot infer the result shape. The result is often an empty DataFrame where the code expected an empty Series, and the next operation fails with a confusing error.

Code that runs `apply` on a frame that may be empty should handle that case explicitly, because the failure appears only when the input happens to be empty &mdash; which is exactly the edge case least likely to be tested.

`result_type=` controls how a list-returning function is interpreted: `"expand"` makes columns, `"reduce"` keeps a Series.

## Choosing the right escape hatch

When something genuinely cannot be vectorised, `apply` is not the only option, and often not the best one.

**`np.vectorize`** &mdash; despite the name, a loop. It handles broadcasting and dtypes for you, and offers no speed benefit.

**A list comprehension over `zip` of the columns** &mdash; frequently *faster* than `apply(axis=1)`, because it skips the per-row Series construction. Less idiomatic, measurably quicker.

**`itertuples`** &mdash; fast iteration with dtypes preserved, when you need the whole row.

**Numba** &mdash; compiles a numeric loop to machine code. The right answer when the logic is genuinely sequential and the frame is large.

**Restructuring** &mdash; often the real answer. A loop over rows to look something up is a `merge`. A loop to compute a group statistic is a `transform`. A loop with a condition is `np.select`.

## A worked replacement

A row-wise function with branching:

```python
def band(row):
    if row["score"] >= 80:
        return "A"
    elif row["score"] >= 50:
        return "B" if row["city"] == "pune" else "C"
    return "F"

df["band"] = df.apply(band, axis=1)
```

becomes:

```python
conds = [
    df["score"] >= 80,
    (df["score"] >= 50) & (df["city"] == "pune"),
    df["score"] >= 50,
]
df["band"] = np.select(conds, ["A", "B", "C"], default="F")
```

The conditions are evaluated in order and the first match wins, which is exactly the semantics of the if/elif chain. It is longer to read the first time and orders of magnitude faster, and the conditions can be built programmatically in a way the function cannot.

## The honest summary

`apply` is not forbidden. It is a Python loop with a pandas-shaped interface, and it should be used when that is what you want: awkward per-row logic, an existing function you cannot rewrite, or a frame small enough that the difference is unmeasurable.

The mistake is reaching for it reflexively for arithmetic, conditionals and lookups, all of which have vectorised forms that are shorter as well as faster.

## Mapping with a Series

`map` accepts a Series as well as a dict, which makes a lookup table out of another frame:

```python
lookup = ref.set_index("code")["label"]
df["label"] = df["code"].map(lookup)
```

This is often better than a merge for a simple one-column lookup. It cannot multiply rows, it needs no `how` or `validate`, and unmatched codes become `NaN` rather than dropping the row.

The requirement is that the lookup's index is unique. If it is not, `map` raises &mdash; which is a better failure than a merge silently duplicating rows.

For a lookup that must bring several columns, a merge is the right tool.

## Missing values in apply and map

`map` passes `NaN` to the function unless `na_action="ignore"`. A function that calls `.lower()` or does arithmetic will fail on it, and the traceback points at your function rather than at the data.

`apply` does the same.

Two options: guard inside the function, or filter first and assign back through `.loc`. The second is usually cleaner, because it keeps the function simple:

```python
ok = df["text"].notna()
df.loc[ok, "parsed"] = df.loc[ok, "text"].apply(parse)
```

## Measuring before optimising

`apply` is slow relative to vectorised operations and fast relative to nothing at all. Whether it matters depends entirely on size.

On a thousand rows, an `apply` takes about a millisecond. Replacing it with `np.select` saves a millisecond and costs readability if the logic is genuinely branchy.

On a million rows, the same `apply` takes seconds and dominates the script.

The decision rule is to measure the actual frame, not to apply a blanket rule. `%timeit` on the real data answers it in seconds, and often the answer is that this particular `apply` is irrelevant and a different line is the problem.

## A summary

`map` for lookups &mdash; dict or Series &mdash; and remember unmatched keys become `NaN`.

`apply` on a Series is a loop; on a frame with `axis=1` it is a slower loop.

`DataFrame.map` (formerly `applymap`) touches every cell and is rarely the right tool.

`np.where`, `np.select`, `pd.cut`, `.str` and `transform` replace most row-wise applies.

A list comprehension over `zip` of columns often beats `apply(axis=1)`.

`iterrows` is never the right choice; `itertuples` if you must iterate.

And the size of the frame decides whether any of this matters.

## A closing note

`apply` occupies a strange place: it is the most reached-for method in pandas and rarely the right one.

The reason is that it looks like the pandas way of doing something per row, and pandas has a reputation for speed, so it feels like it should be fast. It is a Python loop with a method-call interface, and it is no faster than the list comprehension it replaces.

Nearly every row-wise `apply` is one of a handful of patterns with a vectorised form: a conditional is `np.where` or `np.select`, a lookup is `map`, a numeric band is `pd.cut`, string work is `.str`, and a group statistic is `transform`.

That said, the honest position is not that `apply` is forbidden. On a small frame the difference is unmeasurable, and a readable `apply` beats a clever expression nobody can modify. The mistake is reaching for it by default rather than deciding, and never measuring whether it matters.

## One more thing

`Series.map` accepts a **function with a default** through `collections.defaultdict`, which is the neat way to map known values and leave everything else at a fallback without a separate `fillna`.

And `apply` on a groupby is where `include_groups=False` now matters: in pandas 2.2 the grouping columns are passed to the function by default and that behaviour is being changed, so passing the argument explicitly is how you write code that behaves the same before and after the change.

## In summary

`map` substitutes, `apply` computes, and both call Python once per element.

Nearly every row-wise `apply` has a vectorised equivalent &mdash; `np.where`, `np.select`, `map`, `pd.cut`, `.str`, `transform` &mdash; that is shorter as well as faster.

`apply` remains the right answer for genuinely awkward per-row logic, for wrapping a function you cannot rewrite, and on frames small enough that the difference is unmeasurable. The mistake is reaching for it without deciding, and never measuring whether it matters.
''',
    [
        {"q": "What happens to a value not present in the dict passed to `map`?",
         "options": ["It is kept", "It becomes NaN", "It raises", "It becomes an empty string"],
         "answer": 1,
         "why": "A typo in a key silently blanks a column. Use .map(lookup).fillna(s) to keep the original where there was no match."},
        {"q": "Why is `df.apply(func, axis=1)` the slowest common pattern?",
         "options": ["It sorts the frame", "It constructs a Series object for every row on top of the Python call", "It copies columns", "It uses regex"],
         "answer": 1,
         "why": "The tell is a lambda indexing into the row - that is column arithmetic, which runs in compiled code."},
        {"q": "What is the vectorised replacement for a two-branch conditional apply?",
         "options": ["map", "np.where(cond, a, b)", "groupby", "pd.cut"],
         "answer": 1,
         "why": "For several conditions, np.select evaluates in order with first match winning. For numeric bands, pd.cut."},
        {"q": "When is `apply` a reasonable choice?",
         "options": ["Never", "Wrapping an existing scalar function, per-row logic with no array form, or a small frame", "For all arithmetic", "Only with axis=1"],
         "answer": 1,
         "why": "Optimising an apply over 200 rows is wasted effort. The question is whether the frame is large enough for the difference to matter."},
    ],
)


# ---------------------------------------------------------------------------
# 19. concat
# ---------------------------------------------------------------------------
topic(
    "concat",
    "Stacking Frames with concat",
    "Combining",
    "Adding rows or columns from another frame - and the index and column "
    "alignment that decides the result.",
    _svg(_box(20, 24, 40, 20, S) + _box(20, 46, 40, 20, S) +
         _txt(40, 20, "stack", M, 8) +
         _arrow(66, 45, 82, 45) +
         _box(90, 24, 40, 42, S, A)),
    [
        ("Stacking rows",
         "The default joins along the index, which for row-stacking means appending.",
         '''import pandas as pd

a = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
b = pd.DataFrame({"x": [3], "y": ["c"]})

out = pd.concat([a, b])
print(out)
print()
print("the index repeated:", list(out.index), "<- both frames kept theirs")
print()
print("ignore_index=True renumbers:")
print(pd.concat([a, b], ignore_index=True))
print()
print("A repeated index is legal and breaks later lookups, so renumber")
print("unless the labels mean something.")'''),

        ("Columns are matched by name",
         "Missing ones are filled with NaN rather than lined up by position.",
         '''import pandas as pd

a = pd.DataFrame({"x": [1], "y": [2]})
b = pd.DataFrame({"y": [3], "z": [4]})

print("union of columns, gaps filled:")
print(pd.concat([a, b], ignore_index=True))
print()
print("join='inner' keeps only the shared columns:")
print(pd.concat([a, b], ignore_index=True, join="inner"))
print()
print("Note the columns matched by NAME - 'y' lined up even though")
print("it is first in one frame and second in the other.")'''),

        ("Stacking columns instead",
         "axis=1 joins side by side, and now the INDEX does the aligning.",
         '''import pandas as pd

a = pd.DataFrame({"x": [1, 2]}, index=["r1", "r2"])
b = pd.DataFrame({"y": [10, 20]}, index=["r2", "r3"])

print("axis=1 aligns on the index:")
print(pd.concat([a, b], axis=1))
print("   r1 has no y, r3 has no x - both became NaN")
print()
print("join='inner' keeps only the rows in both:")
print(pd.concat([a, b], axis=1, join="inner"))
print()
print("If you meant 'these are the same rows in the same order',")
print("reset both indexes first - otherwise labels decide, not position.")'''),

        ("Labelling where each row came from",
         "keys adds a level so the source survives the concat.",
         '''import pandas as pd

jan = pd.DataFrame({"sales": [10, 20]})
feb = pd.DataFrame({"sales": [30]})

out = pd.concat([jan, feb], keys=["jan", "feb"])
print(out)
print()
print("index is now hierarchical:", out.index.names)
print()
print("select one source back out:")
print(out.loc["jan"])
print()
print("or flatten it into a column:")
print(out.reset_index(level=0).rename(columns={"level_0": "month"}))'''),

        ("Concat in a loop is the usual mistake",
         "Each call copies everything so far, exactly like np.append.",
         '''import pandas as pd
import time

pieces = [pd.DataFrame({"v": [i]}) for i in range(400)]

t = time.perf_counter()
acc = pd.DataFrame(columns=["v"])
for p in pieces:
    acc = pd.concat([acc, p], ignore_index=True)
loop = time.perf_counter() - t

t = time.perf_counter()
once = pd.concat(pieces, ignore_index=True)
single = time.perf_counter() - t

print("concat in a loop : %.4f s" % loop)
print("concat once      : %.4f s" % single)
print("ratio            : %.0fx" % (loop / max(single, 1e-9)))
print("same rows        :", len(acc) == len(once))
print()
print("Collect the pieces in a list and call concat once.")'''),

        ("Dtypes can change when frames disagree",
         "A column that is int in one frame and float in another comes back float.",
         '''import pandas as pd
import numpy as np

a = pd.DataFrame({"v": [1, 2]})
b = pd.DataFrame({"v": [3.5]})
c = pd.DataFrame({"v": ["x"]})

print("int + float ->", pd.concat([a, b], ignore_index=True)["v"].dtype)
print("int + str   ->", pd.concat([a, c], ignore_index=True)["v"].dtype)
print()
print("and an empty frame with no dtype can widen everything:")
empty = pd.DataFrame({"v": pd.Series(dtype="object")})
print("   empty(object) + int ->",
      pd.concat([empty, a], ignore_index=True)["v"].dtype)
print()
print("This is why starting with pd.DataFrame() and concatenating into")
print("it is worse than just collecting a list.")'''),
    ],
    [
        "<code>pd.concat</code> stacks rows by default and <strong>keeps both indexes</strong> &mdash; pass <code>ignore_index=True</code> unless the labels mean something.",
        "Columns are matched <strong>by name</strong>, not position; missing ones become NaN, and <code>join=\"inner\"</code> keeps only the shared ones.",
        "<code>axis=1</code> joins side by side, and then the <strong>index</strong> does the aligning &mdash; unmatched rows become NaN.",
        "<code>keys=[...]</code> records which frame each row came from, as an extra index level.",
        "<code>concat</code> inside a loop copies everything so far each time. Collect into a list and concat once.",
        "Dtypes are promoted when frames disagree &mdash; and concatenating into an empty frame can widen a column to <code>object</code>.",
    ],
    '''
title: Stacking Frames with concat
intro: Adding rows or columns from another frame.

## Two directions

`pd.concat([a, b])` stacks **rows**: the result is taller.

`pd.concat([a, b], axis=1)` stacks **columns**: the result is wider.

Which axis you are joining along decides which axis does the *aligning*, and that is the part worth being deliberate about.

Stacking rows aligns the **columns** by name. Stacking columns aligns the **index** by label.

## Stacking rows

The default keeps both frames' index labels, so the result can have repeated labels &mdash; two rows both labelled 0.

That is legal, and it breaks things later: `.loc[0]` returns two rows instead of one, and code expecting a scalar fails. It is also invisible until something depends on it.

`ignore_index=True` renumbers from 0. Pass it unless the index labels carry meaning you need to keep.

Columns are matched **by name**. A column present in one frame and not the other is filled with `NaN` for the missing rows, and the result has the union of all columns. `join="inner"` keeps only columns present in every frame.

The name-matching is a feature: two frames with the same columns in different orders line up correctly. It is also a trap when a column has been misspelled in one source, because you get two columns each half-full rather than an error.

Checking `result.columns` and the `isna()` counts after a concat catches that immediately.

## Stacking columns

`axis=1` puts frames side by side, aligning on the index.

If the two frames have different labels, the union is used and gaps become `NaN`. If they have the same labels in a different order, pandas reorders to match &mdash; which is correct and is not what positional intuition expects.

The common mistake is concatenating two frames that *should* correspond row-for-row but whose indexes have drifted apart, usually because one of them was filtered. The result is a frame with far more rows than either input, mostly `NaN`.

If you mean "these are the same rows in the same order", reset both indexes first:

```python
pd.concat([a.reset_index(drop=True), b.reset_index(drop=True)], axis=1)
```

That makes the positional intent explicit rather than relying on labels that may not match.

`join="inner"` keeps only rows present in both.

## keys

`pd.concat([jan, feb], keys=["jan", "feb"])` adds an outer index level recording which frame each row came from.

This is how you combine monthly files, or results from several runs, without losing track of the source. `out.loc["jan"]` selects one back out, and `reset_index(level=0)` turns the label into an ordinary column.

Without `keys`, that information is gone the moment the frames are stacked, and reconstructing it means remembering how many rows each contributed.

## Never concat in a loop

`pd.concat` allocates a new frame and copies everything into it. Inside a loop that is quadratic, and it is one of the most common performance mistakes in pandas.

Collect the pieces in a Python list and call `concat` **once**:

```python
frames = [process(f) for f in files]
out = pd.concat(frames, ignore_index=True)
```

The last-but-one editor measures the difference. It grows with the number of iterations, so a pattern that seems fine on ten files becomes unusable on a thousand.

## Dtypes shift

When frames disagree about a column's type, the result is promoted to something that holds both: `int` plus `float` gives `float`, and anything plus a string gives `object`.

There is a specific version of this worth knowing: starting with an **empty** frame and concatenating into it. An empty column has no meaningful dtype, and combining it with real data can widen the result to `object` &mdash; at which point the column is slow and no longer numeric.

That is another reason the list-then-concat pattern is better: there is no empty seed frame to poison the types.

After any concat that combines sources, `result.dtypes` is worth a glance for exactly this.

## Combining files

The canonical use is reading many files into one frame:

```python
frames = []
for path in sorted(glob.glob("data/*.csv")):
    d = pd.read_csv(path)
    d["source"] = os.path.basename(path)
    frames.append(d)
df = pd.concat(frames, ignore_index=True)
```

Three details make this robust.

**Tag the source** before appending, so a row can be traced back to its file. `keys=` does the same thing through the index if you prefer.

**Sort the paths**, so the result is deterministic rather than depending on filesystem order.

**Concat once**, outside the loop.

The frequent surprise is that the files do not agree: a column renamed halfway through the year, an extra column in later exports. Concat unions the columns and fills the gaps with `NaN`, silently. Checking `df.isna().mean()` afterwards shows immediately which columns are only present in some files.

## verify_integrity and sort

`verify_integrity=True` raises if the result would contain duplicate index labels. It costs a check and prevents a duplicated index propagating silently.

`sort=True` sorts the columns alphabetically when frames have different sets. The default leaves them in order of first appearance, which is usually more readable.

## What concat cannot do

`concat` aligns on labels. It does **not** join on values.

Combining two frames on a shared **key column** is `merge`, not `concat(axis=1)`. Using `concat` for that works only if the key happens to be the index of both frames and both are sorted the same way, which is a coincidence rather than a design.

The tell is `axis=1` on frames whose indexes were not deliberately made to correspond. If you find yourself resetting indexes to make a `concat` line up, you probably wanted `merge`.

## Memory during a concat

`concat` allocates a frame the size of all the inputs combined, and the inputs stay alive until it returns. Peak memory is therefore roughly twice the final size.

On a large combine that is the binding constraint, and there are two ways around it.

**Process and reduce each piece before combining** &mdash; filter, select columns, aggregate. Concatenating summaries is far cheaper than concatenating raw data.

**Delete the list afterwards** &mdash; `del frames` releases the inputs, which otherwise stay referenced.

For files larger than memory in total, the answer is not pandas: read in chunks and aggregate incrementally, or use Dask, DuckDB or Polars, all of which are built for it.

## A summary

**Same columns, more rows** &mdash; `concat([a, b], ignore_index=True)`.

**Same rows, more columns, aligned by label** &mdash; `concat([a, b], axis=1)`, only when the indexes genuinely correspond.

**Joining on a key** &mdash; `merge`, not concat.

**Many files** &mdash; a list comprehension and one concat, with a source tag.

**Recording provenance** &mdash; `keys=`, or an explicit column.

And afterwards, three checks: the row count, `dtypes`, and `isna().mean()`. Between them they catch the mismatched columns, the promoted types and the frames that were not what you assumed.

## Concat versus merge, decided

The question that settles it: are you adding **rows of the same kind**, or **columns about the same rows**?

Same kind of rows &mdash; this month's data added to last month's &mdash; is `concat`.

Columns about the same rows, matched on a key &mdash; adding customer details to orders &mdash; is `merge`.

`concat(axis=1)` looks like the second but matches on the **index**, not on a key column. It is right only when the indexes were deliberately made to correspond, which is rarer than it looks.

If you find yourself resetting indexes so a `concat(axis=1)` lines up, the operation you wanted was a merge.

## Checking after a concat

Three lines, and each catches a different failure:

```python
len(out) == sum(len(f) for f in frames)   # nothing lost or duplicated
out.dtypes                                # nothing promoted to object
out.isna().mean()                         # which columns only some files had
```

The third is the one that finds a column renamed partway through a series of files. It appears as two columns, each populated for part of the rows, and the totals look plausible.

## Keys and provenance

`keys=["jan", "feb"]` adds an index level naming the source.

`names=["month"]` names that level, so `reset_index` produces a sensible column name rather than `level_0`.

For a flat result, a column is simpler:

```python
frames = [d.assign(source=name) for name, d in items]
```

Either way, recording where a row came from is worth doing at the moment of combining, because afterwards the information is gone and reconstructing it means remembering row counts.

## A summary

`concat` stacks rows by default and columns with `axis=1`.

Row stacking aligns **columns by name**; column stacking aligns the **index by label**.

`ignore_index=True` unless the labels mean something.

`join="inner"` keeps only what is common.

`keys=` records provenance.

Never concat in a loop &mdash; collect and combine once.

Dtypes promote when frames disagree, and an empty seed frame can widen a column to `object`.

And check the row count, the dtypes and the missingness afterwards.

## A closing note

`concat` is simple enough that its failures are all about expectations rather than mechanics.

The row-stacking case is nearly always right, and the two things to remember are `ignore_index=True` and that columns match by name, so a renamed column in one file becomes two half-full columns rather than an error.

The column-stacking case is the one to be suspicious of. It aligns on the index, and indexes drift apart the moment anything is filtered. If the frames should correspond row for row, reset both indexes and say so; if they should be matched on a key, the operation is a merge.

And the loop rule applies here as everywhere: collect the pieces, combine once. It is the same lesson as `np.append` and `df.loc[len(df)]`, and it is the single most common avoidable slowdown in code that reads many files.

## Two more things worth knowing

`pd.concat` accepts a **dict** as well as a list, in which case the keys become the outer index level automatically: `pd.concat({"jan": a, "feb": b})` is the same as passing `keys=`. That reads well when the pieces already live in a dict keyed by their source.

The `axis` argument also accepts the string names `"index"` and `"columns"`, which are harder to misread than `0` and `1` in code someone else will maintain.

And one behaviour worth expecting: concatenating frames whose columns are in different orders produces the union in order of first appearance, not sorted, unless you pass `sort=True`. Two files exported months apart with the columns reordered will therefore combine correctly but present in an order that matches neither, which is harmless and briefly confusing.

## Combining results, not raw data

The most scalable use of `concat` is on **summaries** rather than on source data.

Reading a hundred files and concatenating them raw builds one frame holding everything, and peak memory is roughly twice its final size because the pieces stay alive until the concat returns. Reading each file, reducing it to what the question needs, and concatenating the small results costs a fraction of that and scales to more files than fit in memory.

```python
parts = []
for path in paths:
    d = pd.read_csv(path, usecols=COLS, dtype=DTYPES)
    parts.append(d.groupby("city", as_index=False)["sales"].sum())
out = pd.concat(parts, ignore_index=True).groupby("city", as_index=False).sum()
```

The double aggregation is the pattern: reduce per file, combine, reduce again. It works for sums, counts and maxima &mdash; anything associative &mdash; and not for medians or exact distinct counts, which need the whole dataset at once.

That distinction, between aggregations that decompose and those that do not, is worth knowing before designing a pipeline around chunked reading.

## In summary

Row stacking aligns columns by name; column stacking aligns the index by label. Knowing which axis you are joining along tells you which axis is doing the matching, and that predicts every surprise this function produces.

Pass `ignore_index=True` unless the labels mean something, record provenance with `keys=` or an explicit column, and never call it inside a loop.

Afterwards, check the row count, the dtypes and the missingness &mdash; between them they catch the mismatched columns, the promoted types, and the file whose schema quietly changed.
''',
    [
        {"q": "What does `pd.concat([a, b])` do with the two frames' indexes?",
         "options": ["Renumbers from 0", "Keeps both, so labels can repeat", "Raises on a clash", "Sorts them"],
         "answer": 1,
         "why": "A repeated label is legal and invisible until .loc returns two rows where code expected one. Pass ignore_index=True unless the labels matter."},
        {"q": "When stacking rows, how are columns matched?",
         "options": ["By position", "By name, with missing ones filled with NaN", "Alphabetically", "By dtype"],
         "answer": 1,
         "why": "A feature when column orders differ, and a trap when a name is misspelled in one source - you get two half-full columns rather than an error."},
        {"q": "Two frames should correspond row-for-row but one was filtered. What does `concat(axis=1)` give?",
         "options": ["The correct pairing", "More rows than either input, mostly NaN, because it aligns on labels", "An error", "The first frame only"],
         "answer": 1,
         "why": "Reset both indexes first if you mean 'same rows, same order' - that makes the positional intent explicit."},
        {"q": "Why avoid starting with an empty DataFrame and concatenating into it?",
         "options": ["It is illegal", "It is quadratic, and the empty column's dtype can widen the result to object", "It loses column names", "It sorts the rows"],
         "answer": 1,
         "why": "Collect pieces in a list and concat once - there is then no empty seed frame to poison the dtypes."},
    ],
)


# ---------------------------------------------------------------------------
# 20. merge
# ---------------------------------------------------------------------------
topic(
    "merge_and_join",
    "merge and join",
    "Combining",
    "SQL-style joins - the four kinds, and the duplicate key that silently "
    "multiplies your rows.",
    _svg(_box(16, 30, 40, 30, S) + _txt(36, 49, "left", M, 8) +
         _box(88, 30, 40, 30, S) + _txt(108, 49, "right", M, 8) +
         _box(52, 34, 40, 22, S, A) + _txt(72, 48, "on=key", A, 7)),
    [
        ("The four kinds of join",
         "how= decides which rows survive when a key is missing on one side.",
         '''import pandas as pd

left = pd.DataFrame({"id": [1, 2, 3], "name": ["ana", "raj", "kim"]})
right = pd.DataFrame({"id": [2, 3, 4], "score": [90, 80, 70]})

for how in ["inner", "left", "right", "outer"]:
    out = left.merge(right, on="id", how=how)
    print("%-6s -> %d rows: ids %s" % (how, len(out), sorted(out["id"])))

print()
print("inner: only ids in BOTH (2, 3)")
print("left : every left row, score NaN where unmatched")
print("outer: every id from either side")
print()
print("the default is 'inner', which quietly drops unmatched rows.")'''),

        ("Seeing what matched",
         "indicator= tells you which side each row came from.",
         '''import pandas as pd

left = pd.DataFrame({"id": [1, 2, 3], "name": ["ana", "raj", "kim"]})
right = pd.DataFrame({"id": [2, 3, 4], "score": [90, 80, 70]})

out = left.merge(right, on="id", how="outer", indicator=True)
print(out)
print()
print(out["_merge"].value_counts())
print()
print("This is the first thing to run when a join loses rows you")
print("expected to keep - it names them instead of leaving you to guess.")'''),

        ("A duplicated key multiplies rows",
         "The single most damaging silent bug in pandas.",
         '''import pandas as pd

orders = pd.DataFrame({"id": [1, 2], "amount": [100, 200]})
lookup = pd.DataFrame({"id": [1, 1, 2], "label": ["a", "b", "c"]})

print("orders:", len(orders), "rows   lookup:", len(lookup), "rows")
out = orders.merge(lookup, on="id")
print()
print(out)
print()
print("3 rows out of a 2-row left frame - id 1 matched twice.")
print("total amount before:", int(orders["amount"].sum()))
print("total amount after :", int(out["amount"].sum()), "<- inflated")
print()
print("Nothing warned. Every sum downstream is now wrong.")'''),

        ("validate catches it at the join",
         "State the relationship you expect and let pandas check it.",
         '''import pandas as pd

orders = pd.DataFrame({"id": [1, 2], "amount": [100, 200]})
lookup = pd.DataFrame({"id": [1, 1, 2], "label": ["a", "b", "c"]})

try:
    orders.merge(lookup, on="id", validate="one_to_one")
except Exception as e:
    print("validate='one_to_one' ->", type(e).__name__)
    print("   ", str(e)[:64])
print()
good = pd.DataFrame({"id": [1, 2], "label": ["a", "c"]})
out = orders.merge(good, on="id", validate="one_to_one")
print("with a unique lookup it passes:", len(out), "rows")
print()
print("Options: one_to_one, one_to_many, many_to_one, many_to_many.")
print("Writing the one you expect turns a silent bug into an error.")'''),

        ("Different column names, and overlapping ones",
         "left_on/right_on, and the suffixes that appear when names collide.",
         '''import pandas as pd

a = pd.DataFrame({"user_id": [1, 2], "v": [10, 20]})
b = pd.DataFrame({"id": [1, 2], "v": [99, 98]})

out = a.merge(b, left_on="user_id", right_on="id")
print(out)
print()
print("both frames had a 'v', so pandas suffixed them:")
print("   ", [c for c in out.columns if c.startswith("v")])
print()
print("name them yourself:")
print(list(a.merge(b, left_on="user_id", right_on="id",
                   suffixes=("_a", "_b")).columns))
print()
print("Unnoticed suffixes are how you end up analysing v_x when you")
print("meant v_y. Drop or rename the duplicate before merging.")'''),

        ("Joining on the index",
         "join() is merge with the index as the default key.",
         '''import pandas as pd

a = pd.DataFrame({"v": [1, 2]}, index=["x", "y"])
b = pd.DataFrame({"w": [10, 30]}, index=["x", "z"])

print("join defaults to a LEFT join on the index:")
print(a.join(b))
print()
print("how= works the same way:")
print(a.join(b, how="outer"))
print()
print("merge can do it too, explicitly:")
print(a.merge(b, left_index=True, right_index=True, how="outer"))
print()
print("Index joins are faster on a sorted unique index, which is a")
print("reason to set_index on a key you join on repeatedly.")'''),
    ],
    [
        "<code>how=</code> picks the join: <code>inner</code> (the default, which silently drops unmatched rows), <code>left</code>, <code>right</code>, <code>outer</code>.",
        "<code>indicator=True</code> adds a <code>_merge</code> column naming which side each row came from &mdash; the first thing to run when a join loses rows.",
        "A <strong>duplicated key</strong> multiplies rows and inflates every later total, with no warning.",
        "<code>validate=\"one_to_one\"</code> (or <code>one_to_many</code>, <code>many_to_one</code>) turns that silent bug into an error.",
        "Overlapping column names get <code>_x</code>/<code>_y</code> suffixes &mdash; set <code>suffixes=</code> or drop the duplicate before merging.",
        "<code>join()</code> merges on the index and defaults to a <strong>left</strong> join, where <code>merge</code> defaults to inner.",
    ],
    '''
title: merge and join
intro: SQL-style joins, and the duplicate key that silently multiplies your rows.

## The four kinds

`merge` combines two frames on one or more key columns. `how` decides what happens to keys that appear on only one side.

`inner` &mdash; only keys present in both. **This is the default**, and it means unmatched rows are silently discarded.

`left` &mdash; every row from the left frame, with `NaN` where the right had no match. This is usually what you want when enriching a table with a lookup: you are adding information, not filtering.

`right` &mdash; the mirror image, and rarely used, since swapping the operands is clearer.

`outer` &mdash; every key from either side.

The default being `inner` is worth remembering. A join that was meant to add a column can quietly remove rows, and the only sign is a row count you were not checking.

## Check what happened

Two habits catch nearly every join problem.

**Compare row counts.** `len(before)` against `len(after)`. If a left join changed the count, something is duplicated. If an inner join dropped rows, some keys did not match.

**Use `indicator=True`.** It adds a `_merge` column with values `left_only`, `right_only` or `both`, and `value_counts()` on it summarises the whole join in one line.

That is far better than guessing. It tells you not just that rows went missing but which ones, so you can look at them and find out whether the key is misspelled, differently typed, or genuinely absent.

A frequent cause of a "failed" join is a **dtype mismatch**: `1` as an integer on one side and `"1"` as a string on the other never match, and nothing warns. Checking both key columns' dtypes takes a second.

Whitespace and case do the same thing to string keys, which is why the cleaning modules come before this one.

## The duplicate-key multiplication

This is the most damaging silent bug in pandas.

If a key appears twice on the right, every matching left row is duplicated. Two orders joined to a lookup with a repeated id produce three rows. The frame still looks like orders, still has an `amount` column, and every sum computed from it is now wrong.

Nothing warns, because a many-to-one join *becoming* many-to-many is a legitimate operation &mdash; pandas cannot know you did not intend it.

The consequences are quiet and severe: inflated revenue, double-counted users, a model trained on duplicated rows.

## validate

`validate=` states the relationship you expect and raises if it does not hold:

`"one_to_one"` &mdash; keys unique on both sides.

`"one_to_many"` &mdash; unique on the left.

`"many_to_one"` &mdash; unique on the right. This is the common case for a lookup table, and the one worth reaching for by default when joining reference data.

`"many_to_many"` &mdash; no constraint, which is the current behaviour spelled out loud.

Adding it costs one argument and converts an invisible data-corruption bug into a clear exception at the point it happens. On any join that feeds a number someone will act on, it is worth having.

## Different names, colliding names

`left_on` and `right_on` join columns with different names. `left_index=True` / `right_index=True` use the index on that side.

When both frames have a column with the same name that is *not* a key, pandas keeps both and appends `_x` and `_y`.

That is where a subtle error lives: `v_x` and `v_y` both look plausible, and picking the wrong one produces a working analysis of the wrong column. Set `suffixes=("_orders", "_lookup")` so the names say where they came from, or drop the redundant column before merging.

## join

`df.join(other)` is `merge` with the index as the key, and it defaults to a **left** join rather than an inner one.

Two different defaults for two similar methods is a genuine wart. When it matters, use `merge` with explicit arguments; `join` is a convenience for the index case.

Index joins are faster than column joins on a sorted, unique index, which is a reason to `set_index` on a key you join on repeatedly rather than passing `on=` every time.

## An order of operations

Clean the keys &mdash; type, case, whitespace. Check uniqueness on the side that should be unique. Choose `how` deliberately rather than taking the default. Add `validate`. Compare row counts afterwards.

That sounds like a lot for one operation. It is five seconds of typing, and joins are where the expensive, silent errors live.

## Joining on several keys

`on=["date", "store"]` joins on a composite key. Both frames need all the named columns, and rows match only when **every** key agrees.

The usual failure is a type mismatch on one of several keys &mdash; the dates match but one side stores the store id as text. The join then returns far fewer rows than expected, and `indicator=True` shows a large `left_only` count without saying why.

Checking the dtypes of every key column on both sides takes one line:

```python
print(left[keys].dtypes, right[keys].dtypes, sep="\n")
```

## Joins that filter

Two common intentions are filters rather than enrichments.

**Keep rows whose key exists elsewhere** &mdash; a semi-join. pandas has no dedicated method, and `df[df["id"].isin(other["id"])]` is the right implementation. It cannot multiply rows, which an inner join can.

**Keep rows whose key does not exist elsewhere** &mdash; an anti-join. `df[~df["id"].isin(other["id"])]`, or an outer join with `indicator=True` filtered to `left_only` when you also want the other side's columns.

Using a merge for either is a common way to introduce accidental row multiplication.

## Ordered and nearest-match joins

`pd.merge_ordered` merges two ordered frames and can fill forward across the join, which suits time series with different sampling.

`pd.merge_asof` joins on the **nearest** key rather than an exact match, which is the standard tool for joining a measurement to the most recent preceding reference value &mdash; a trade to the latest quote, a reading to the last calibration.

Both require sorted inputs and both are much faster than the alternative of a cross join and a filter, which on real data does not fit in memory.

`direction="backward"` (the default), `"forward"` or `"nearest"` and a `tolerance` control the matching.

## Performance

Merging is roughly `O(n + m)` with hashing, and the practical costs are elsewhere:

**Key dtype.** Joining on integers or categoricals is faster than on strings.

**Index joins.** A sorted, unique index makes `join` faster than a column merge, which is a reason to `set_index` on a key used repeatedly.

**Result size.** A many-to-many join can produce a frame far larger than either input. Checking the expected size before running it &mdash; the product of the group counts &mdash; avoids allocating something that does not fit.

**Column count.** Selecting only the columns you need from the right frame before merging avoids carrying passengers through the join and into memory.

That last one is the easiest win: `left.merge(right[["id", "label"]], on="id")` rather than merging the whole of `right`.

## A merge checklist

Before:

Clean both key columns &mdash; type, case, whitespace.

Check uniqueness on the side that should be unique.

Select only the columns you need from the right frame.

During:

Choose `how` deliberately; the default is `inner`.

Set `validate` to the relationship you expect.

Set `suffixes` if column names overlap.

Add `indicator=True` while developing.

After:

Compare row counts with the input.

Check the `_merge` counts.

Check `isna()` on the newly added columns &mdash; a left join that matched nothing gives a column that is entirely null, which is easy to miss and obvious once looked for.

## What to do when a join goes wrong

A structured approach beats guessing, and it takes about a minute.

**Row count changed unexpectedly?** A duplicated key on one side. Check `is_unique` on both, and use `validate`.

**Rows missing?** An inner join with unmatched keys. Switch to `how="left"` and `indicator=True` to see which.

**Everything unmatched?** A dtype mismatch on the key, or whitespace or case in a string key. Compare `dtypes` and look at a few values from each side.

**New columns entirely null?** The join matched no rows, or matched on the wrong column.

**Unexpected `_x` / `_y` columns?** Overlapping non-key names. Set `suffixes`, or select the columns you need before merging.

The tool for the first three is `indicator=True`, and the habit of comparing `len(before)` to `len(after)` catches all of them earlier than anything else.

## Joining a summary back to detail

A frequent shape: compute a per-group statistic, then attach it to every row.

The merge version works and has three steps and a risk.

The `transform` version has one step and no risk:

```python
df["city_total"] = df.groupby("city")["sales"].transform("sum")
```

Reaching for a merge where a `transform` fits is one of the most common unnecessary joins, and it is worth recognising because the merge route is where the row-multiplication bugs live.

## Set-like operations without a join

Several questions phrased as joins are really membership tests:

"Which of these ids exist in that table?" &mdash; `isin`.

"Which do not?" &mdash; `~isin`.

"What is the overlap between two key sets?" &mdash; `a.index.intersection(b.index)`, or set operations on the columns.

All three avoid the join machinery entirely and cannot change the row count, which makes them both safer and clearer when the answer is a filter rather than an enrichment.

## A summary

`how="inner"` is the default and drops unmatched rows silently.

`indicator=True` while developing; it explains the result.

`validate=` states the relationship and turns silent multiplication into an error.

Clean and type-check the key columns first &mdash; most failed joins are dtype or whitespace.

Select only the columns you need from the right frame.

Set `suffixes` when names overlap.

`join()` merges on the index and defaults to `left`, unlike `merge`.

Use `transform` instead of a self-join for group statistics, and `isin` instead of a join for membership.

And compare row counts before and after, every time.

## A closing note

Joins are where the expensive, quiet errors live.

An inner join silently drops the rows that did not match. A duplicated key on either side silently multiplies the rows that did. Neither raises, both produce output of the right shape, and every number computed afterwards is wrong in a way that looks reasonable.

Three habits reduce almost all of it to nothing. Check the key columns' dtypes before joining, because most "nothing matched" cases are an integer against a string. Pass `validate=` to state the relationship you expect. And compare the row count before and after, every single time.

Those cost a few seconds and replace the alternative, which is discovering months later that a total has been inflated because one reference table gained a duplicate.

And a good share of joins are not joins at all: a group statistic wants `transform`, and a membership test wants `isin`. Both are safer, because neither can change the number of rows.

## One more thing

`merge` accepts `how="cross"`, producing every combination of rows from both frames. It is occasionally what you want &mdash; building a complete grid of parameters, or every store crossed with every date &mdash; and it is worth knowing that the result's size is the product of the inputs, which grows alarmingly fast.

For the common case of filling out a complete grid before joining sparse data onto it, `pd.MultiIndex.from_product` and `reindex` are usually the better route.

## In summary

The default is an inner join, which drops unmatched rows without a word, and a duplicated key on either side multiplies rows without a word either.

Both are prevented by the same short routine: clean and type-check the keys, assert uniqueness where you assume it, pass `validate=`, and compare the row count before and after.

And a good number of operations phrased as joins are not: a group statistic is `transform`, and a membership test is `isin`. Both are safer, because neither can change how many rows you have.
''',
    [
        {"q": "What is `merge`'s default `how`?",
         "options": ["left", "inner - which silently drops unmatched rows", "outer", "right"],
         "answer": 1,
         "why": "A join meant to add a column can quietly remove rows, and the only sign is a row count you were not checking. Note join() defaults to left instead."},
        {"q": "A key appears twice on the right. What happens?",
         "options": ["It raises", "Every matching left row is duplicated, inflating later totals", "The extra row is dropped", "It becomes NaN"],
         "answer": 1,
         "why": "Nothing warns, because many-to-many is a legitimate operation. validate='many_to_one' turns it into an error."},
        {"q": "A join matches nothing even though the keys look identical. What is the usual cause?",
         "options": ["A pandas bug", "A dtype mismatch - 1 as int never matches '1' as str", "Too many rows", "Missing index"],
         "answer": 1,
         "why": "Whitespace and case do the same to string keys. Check both key columns' dtypes, and use indicator=True to see what matched."},
        {"q": "What does `indicator=True` add?",
         "options": ["A row count", "A _merge column saying whether each row came from left_only, right_only or both", "A validation error", "An index"],
         "answer": 1,
         "why": "value_counts() on it summarises the whole join in one line - far better than guessing why rows went missing."},
    ],
)


# ---------------------------------------------------------------------------
# 21. Reshaping
# ---------------------------------------------------------------------------
topic(
    "pivot_and_melt",
    "Reshaping: pivot and melt",
    "Combining",
    "Long to wide and back - the two shapes tabular data comes in, and when each "
    "one is right.",
    _svg(_box(18, 24, 26, 44, S) + _txt(31, 20, "long", M, 8) +
         _arrow(48, 40, 66, 40) + _txt(57, 34, "pivot", A, 6) +
         _arrow(66, 54, 48, 54) + _txt(57, 66, "melt", A, 6) +
         _box(72, 32, 66, 28, S) + _txt(105, 20, "wide", M, 8)),
    [
        ("Long and wide, the same data",
         "One row per observation, or one row per subject with a column per variable.",
         '''import pandas as pd

long = pd.DataFrame({
    "city": ["pune", "pune", "delhi", "delhi"],
    "year": [2023, 2024, 2023, 2024],
    "sales": [10, 20, 30, 40],
})
print("long - one row per observation:")
print(long)
print()
wide = long.pivot(index="city", columns="year", values="sales")
print("wide - one row per city, one column per year:")
print(wide)
print()
print("Same numbers. Long is better for storage and computation,")
print("wide is better for reading and for a chart.")'''),

        ("melt goes the other way",
         "Column names become values in a variable column.",
         '''import pandas as pd

wide = pd.DataFrame({
    "city": ["pune", "delhi"],
    "2023": [10, 30],
    "2024": [20, 40],
})
print("wide:"); print(wide)
print()
long = wide.melt(id_vars="city", var_name="year", value_name="sales")
print("melted:"); print(long)
print()
print("id_vars are the columns to KEEP as identifiers; everything")
print("else is unpivoted. Naming both output columns is worth doing -")
print("the defaults are 'variable' and 'value'.")'''),

        ("pivot fails on duplicates",
         "Because it has no way to decide which value wins.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi"],
    "year": [2024, 2024, 2024],
    "sales": [10, 20, 30],
})
print("pune/2024 appears twice:")
print(df)
print()
try:
    df.pivot(index="city", columns="year", values="sales")
except ValueError as e:
    print("pivot ->", type(e).__name__)
    print("   ", str(e)[:58])
print()
print("pivot_table aggregates instead of failing:")
print(df.pivot_table(index="city", columns="year", values="sales", aggfunc="sum"))'''),

        ("pivot_table is the general tool",
         "It aggregates, fills and totals - pivot is the strict special case.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi", "delhi"],
    "plan": ["free", "paid", "free", "free"],
    "sales": [10, 20, 30, 40],
})
print(df.pivot_table(index="city", columns="plan", values="sales",
                     aggfunc="sum"))
print()
print("fill the gaps and add totals:")
print(df.pivot_table(index="city", columns="plan", values="sales",
                     aggfunc="sum", fill_value=0, margins=True))
print()
print("several statistics at once:")
print(df.pivot_table(index="city", values="sales", aggfunc=["sum", "mean", "count"]))
print()
try:
    df.pivot_table(index="city", values="sales", aggfunc=["sum", "size"])
except AttributeError as e:
    print("but 'size' in that list raises:", type(e).__name__)
    print("   groupby handles it fine, which is the fallback:")
    print(df.groupby("city")["sales"].agg(["sum", "size"]))'''),

        ("stack and unstack move index levels",
         "The same reshape, expressed through the index rather than columns.",
         '''import pandas as pd

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]}, index=["x", "y"])
print("wide:"); print(df)
print()
s = df.stack()
print("stacked - columns became an index level:")
print(s)
print("   index:", s.index.names, "->", list(s.index)[:2], "...")
print()
print("unstack puts it back:")
print(s.unstack())
print()
print("This is what groupby-with-two-keys plus unstack was doing.")'''),

        ("Which shape to work in",
         "Long for computing, wide for reading - and pandas prefers long.",
         '''import pandas as pd

long = pd.DataFrame({
    "city": ["pune", "pune", "delhi", "delhi"],
    "year": [2023, 2024, 2023, 2024],
    "sales": [10, 20, 30, 40],
})
print("in long form, a new question is one groupby:")
print(long.groupby("year")["sales"].sum())
print()
wide = long.pivot(index="city", columns="year", values="sales")
print("in wide form, the same question needs column arithmetic:")
print(wide.sum())
print()
print("and adding a year means adding a COLUMN in wide form, which")
print("changes every expression that named the old ones.")
print()
print("Keep data long; pivot at the end, for display.")'''),
    ],
    [
        "<strong>Long</strong> is one row per observation; <strong>wide</strong> is one row per subject with a column per variable. Same data, different shape.",
        "<code>pivot</code> goes long to wide; <code>melt</code> goes wide to long with <code>id_vars</code> naming the columns to keep.",
        "<code>pivot</code> <strong>raises</strong> on duplicate index/column pairs, because it cannot choose a winner.",
        "<code>pivot_table</code> aggregates instead, and adds <code>fill_value</code>, <code>margins</code> and several statistics at once.",
        "<code>stack</code> and <code>unstack</code> do the same reshape through index levels rather than named columns.",
        "Work in <strong>long</strong> form and pivot at the end &mdash; adding a category in wide form changes every expression that named the old columns.",
    ],
    '''
title: Reshaping: pivot and melt
intro: Long to wide and back, and when each shape is right.

## Two shapes

The same data can be laid out two ways.

**Long** (or tidy) has one row per observation, with columns naming the variable and holding the value. City, year, sales &mdash; four rows for two cities over two years.

**Wide** has one row per subject and a column per variable. Two rows, one per city, with a `2023` and a `2024` column.

Neither is more correct. They suit different purposes, and most real work involves converting between them.

Long form is better for **storage and computation**. Adding a year adds rows, not columns, so nothing downstream changes. Group-by works naturally. Missing combinations simply do not appear. Databases and most plotting libraries expect it.

Wide form is better for **reading**. A table with years across the top is what people want to look at, and it is what a spreadsheet or a report needs.

## pivot

`df.pivot(index="city", columns="year", values="sales")` goes long to wide.

Three arguments: what becomes the row index, what becomes the columns, and what fills the cells.

`pivot` is strict. If a given index/column pair appears more than once, it **raises**, because there is no way to decide which value wins. That strictness is a feature &mdash; it tells you the data is not what you assumed rather than silently keeping one row.

## pivot_table

`pivot_table` is the general version: when a cell has several values, it **aggregates** them.

```python
df.pivot_table(index="city", columns="plan", values="sales", aggfunc="sum")
```

`aggfunc` defaults to `"mean"`, which is worth knowing before it surprises you &mdash; a pivot table of sales that averages when you expected a total looks entirely plausible.

`fill_value` replaces the `NaN` in empty cells, usually with 0.

`margins=True` adds row and column totals, labelled `All`.

A list for `aggfunc` gives several statistics; a list for `index` or `columns` gives hierarchical axes.

One wart, current as of pandas 2.2: `"size"` inside an `aggfunc` **list** raises `AttributeError`, while `"count"` in the same position works. `groupby(...).agg(["sum", "size"])` handles it without complaint, and is the fallback when you want a row count alongside other statistics. The difference between the two is the one from the group-by module &mdash; `size` counts rows, `count` counts non-missing values.

`pivot_table` is essentially group-by with a nicer layout, and anything it does can be done with `groupby` plus `unstack`. It is worth using when the output is a table for a human.

## melt

`melt` goes wide to long.

```python
wide.melt(id_vars="city", var_name="year", value_name="sales")
```

`id_vars` are the columns to keep as identifiers. Everything else is unpivoted into two columns: one holding the old column names, one holding the values.

Name both outputs. The defaults are `variable` and `value`, which say nothing and have to be renamed later anyway.

`value_vars` restricts which columns are melted, when you want to unpivot some and keep others as identifiers.

This is the operation for data that arrived from a spreadsheet with one column per month &mdash; a shape that is convenient to type and painful to compute with.

## stack and unstack

The same reshape expressed through the index.

`stack()` moves the innermost **column** level into the index, making the frame taller and narrower. `unstack()` moves the innermost **index** level into the columns.

These are what you reach for after a group-by with several keys, where the result already has a MultiIndex. `groupby(["city","year"]).sum().unstack()` gives the wide table directly.

`unstack(fill_value=0)` fills the gaps, and `unstack(level=0)` chooses which level moves when there are more than two.

## Which to work in

The practical advice is to **keep data long and pivot at the end**.

The reason is maintenance. In wide form, a new year means a new column, and every expression that named the old columns has to change. In long form it means new rows, and nothing changes at all.

Long form also composes with everything else in pandas &mdash; group-by, filtering, joins all assume one row per observation.

Pivot when the output is a table someone will read, a chart, or a file for a tool that expects wide. That is a display step, and it belongs at the end of the pipeline rather than the middle.

## Tidy data

The long form has a name and a definition, from Hadley Wickham's tidy data:

Each **variable** is a column. Each **observation** is a row. Each type of observational unit is a table.

Data that follows those rules composes with everything: group-by, filtering, joins and most plotting libraries all assume it.

The common violations are worth recognising, because each has a standard fix.

**Column headers are values, not variable names** &mdash; a column per year. Fix with `melt`.

**Several variables in one column** &mdash; a `measure` column holding both height and weight. Fix with `pivot`.

**Variables in both rows and columns** &mdash; fix with `melt` then `pivot`.

**Several values in one cell** &mdash; `"a, b, c"` in one field. Fix with `str.split` and `explode`.

## explode

`df.explode("tags")` turns a column of lists into one row per element, repeating the other columns.

It is the tool for data that arrived with several values per cell:

```python
df.assign(tag=df["tags"].str.split(",")).explode("tag")
```

Each tag becomes its own row, at which point it can be grouped and counted normally.

The inverse is a group-by with `list` or `", ".join` as the aggregation.

`explode` produces duplicate index labels, so `reset_index(drop=True)` usually follows.

## pivot_table in more depth

Beyond the basics, three arguments do real work.

`aggfunc` accepts a **dict** keyed by column, so different values can be summarised differently in one table.

`index` and `columns` accept **lists**, giving hierarchical axes &mdash; region and city down the side, year and quarter across the top.

`dropna=False` keeps columns that are entirely empty, which matters when the table must have a fixed shape for comparison.

`margins_name` renames the `All` row and column.

The output is a frame with a MultiIndex on one or both axes, so the flattening step from the MultiIndex module usually follows if the result is going anywhere other than the screen.

## Reshaping and memory

Wide data with many empty cells is sparse, and pivoting long data into it can allocate far more than the input.

A long frame with 100,000 rows covering 5,000 users and 3,000 products pivots into a 15,000,000-cell table, most of it `NaN`. The long form held 100,000 values.

That is the main practical argument for staying long: the wide form materialises every combination, whether or not it occurred.

When a wide layout is genuinely needed for a sparse dataset, `pivot_table` with `fill_value=0` at least avoids the float promotion that `NaN` forces, and a sparse dtype or a different tool is worth considering past a certain size.

## Which operation, by shape

**Long to wide, no duplicates** &mdash; `pivot`.

**Long to wide, with aggregation** &mdash; `pivot_table`.

**Wide to long** &mdash; `melt`.

**Column level into index** &mdash; `stack`.

**Index level into columns** &mdash; `unstack`.

**Lists in cells into rows** &mdash; `explode`.

**A frequency table of two variables** &mdash; `crosstab`, or `groupby` plus `unstack`.

The reliable way to choose is to write down the shape you have and the shape you want, in rows and columns, and pick the operation that moves one to the other. Reshaping goes wrong when it is attempted by trial and error rather than by naming the target.

## Reshaping for a chart

Most plotting expects one of two shapes, and knowing which saves a lot of trial and error.

`df.plot()` on a **wide** frame draws one line per column, using the index as the x-axis. That is why `groupby(...).unstack().plot()` works so neatly &mdash; unstack produces exactly that shape.

Seaborn and similar libraries generally want **long** data, with columns naming the variable and the value, and a `hue=` argument doing the splitting.

So the reshape before plotting depends on the library, and it is usually one call in either direction. Knowing which shape the function wants is faster than adjusting the data until the chart looks right.

## Round-tripping

`melt` then `pivot` returns to where you started, provided the identifier columns uniquely determine a row. If they do not, `pivot` raises on duplicates &mdash; which is a useful check that the identifiers are what you thought.

That round trip is a quick way to test an assumption about the data's grain: if `pivot` complains, the key you believed was unique is not.

## Column names after reshaping

`pivot` and `pivot_table` use the values of the `columns` argument as column names, so the result's columns are data. That has two consequences.

They may not be valid identifiers &mdash; a year is an integer, a product name may contain spaces &mdash; so `df.column_name` will not work and `df["2024"]` may need to be `df[2024]`.

They change when the data changes. Code that names them breaks when a new category appears, which is the maintenance argument for staying long.

`rename_axis(columns=None)` removes the axis name that pivoting leaves behind, which otherwise shows up as a stray label above the columns when printing.

## A summary

Long is one row per observation; wide is one row per subject.

`pivot` for long to wide with unique pairs; `pivot_table` when aggregation is needed.

`melt` for wide to long, naming both output columns.

`stack`/`unstack` do the same through index levels.

`explode` for lists in cells.

Wide materialises every combination, so it can be far larger than the long form.

Work long, pivot at the end, for display.

And when a reshape is confusing, write down the shape you have and the shape you want &mdash; the operation follows from that, and trial and error rarely converges.

## A closing note

Reshaping is the operation people most often approach by trial and error, and the one where that approach works worst.

The reliable method is to write down the shape you have and the shape you want &mdash; what is a row, what is a column &mdash; and pick the operation that moves between them. Long to wide is `pivot`, or `pivot_table` if any cell would hold more than one value. Wide to long is `melt`. Through the index instead of named columns, it is `stack` and `unstack`.

The default that catches people is `pivot_table`'s `aggfunc="mean"`. A table of sales that quietly averages where you expected a total looks entirely plausible, and nothing indicates otherwise.

And the structural advice is to stay long until the end. Wide data materialises every combination whether it occurred or not, and every new category changes the columns &mdash; and therefore every expression that names them.

## One more thing

`melt` accepts `ignore_index=False`, which keeps the original index rather than renumbering. That matters when the identifiers you want to keep are in the index rather than in columns, since `id_vars` only names columns.

And `wide_to_long` handles the specific case of columns named with a stem and a suffix &mdash; `sales_2023`, `sales_2024` &mdash; unpivoting them into a stem column and a suffix column in one call, which is otherwise a `melt` followed by a `str.extract`.

## In summary

Long form is one row per observation and composes with everything; wide form is one row per subject and reads better.

Convert with `pivot` and `melt`, or through the index with `stack` and `unstack`, and use `pivot_table` when a cell could hold more than one value &mdash; remembering that its `aggfunc` defaults to `mean`.

Work long and pivot at the end. In wide form a new category is a new column, and every expression that named the old columns has to change.
''',
    [
        {"q": "Why does `pivot` raise on duplicate index/column pairs?",
         "options": ["A limitation", "There is no way to decide which value wins - the strictness tells you the data is not what you assumed", "It is deprecated", "Memory"],
         "answer": 1,
         "why": "pivot_table aggregates instead. Note its aggfunc defaults to 'mean', which looks plausible when you expected a total."},
        {"q": "What does `pivot_table`'s `aggfunc` default to?",
         "options": ["sum", "mean", "count", "first"],
         "answer": 1,
         "why": "Worth knowing before it surprises you - a pivot of sales that averages when you expected a total looks entirely reasonable."},
        {"q": "What are `id_vars` in `melt`?",
         "options": ["The columns to unpivot", "The columns to keep as identifiers, while everything else is unpivoted", "The new column names", "The index"],
         "answer": 1,
         "why": "Name var_name and value_name too - the defaults are 'variable' and 'value', which say nothing."},
        {"q": "Why keep data in long form and pivot only at the end?",
         "options": ["It uses less memory", "Adding a category adds rows, not columns, so no downstream expression changes", "pivot is slow", "Long form sorts better"],
         "answer": 1,
         "why": "In wide form a new year is a new column, and every expression naming the old ones has to change. Long form also composes with groupby and joins."},
    ],
)


# ---------------------------------------------------------------------------
# 22. MultiIndex
# ---------------------------------------------------------------------------
topic(
    "multiindex",
    "The MultiIndex",
    "Combining",
    "More than one level on an axis - where it comes from, how to select through "
    "it, and when to flatten it away.",
    _svg(_txt(30, 30, "pune", M, 8) + _txt(30, 44, "pune", M, 8) +
         _txt(30, 58, "delhi", M, 8) +
         _txt(64, 30, "2023", A, 8) + _txt(64, 44, "2024", A, 8) +
         _txt(64, 58, "2023", A, 8) +
         _box(88, 22, 40, 44, S)),
    [
        ("Where it comes from",
         "You rarely build one on purpose - a groupby with two keys hands you one.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi", "delhi"],
    "year": [2023, 2024, 2023, 2024],
    "sales": [10, 20, 30, 40],
})
out = df.groupby(["city", "year"])["sales"].sum()
print(out)
print()
print("type  :", type(out.index).__name__)
print("names :", out.index.names)
print("levels:", [list(l) for l in out.index.levels])
print()
print("concat with keys= and unstack/stack produce them too.")'''),

        ("Selecting through the levels",
         "A tuple addresses the levels in order; loc takes it.",
         '''import pandas as pd

s = pd.Series([10, 20, 30, 40], index=pd.MultiIndex.from_tuples(
    [("pune", 2023), ("pune", 2024), ("delhi", 2023), ("delhi", 2024)],
    names=["city", "year"]))

print("one outer key gives a sub-Series:")
print(s.loc["pune"])
print()
print("a tuple addresses both levels:", s.loc[("pune", 2024)])
print()
print("a list of outer keys:")
print(list(s.loc[["pune", "delhi"]]))
print()
print("cross-section on an INNER level needs xs:")
print(s.xs(2024, level="year"))'''),

        ("slice(None) is the wildcard",
         "Because you cannot write a bare colon inside a tuple.",
         '''import pandas as pd

s = pd.Series([10, 20, 30, 40], index=pd.MultiIndex.from_tuples(
    [("pune", 2023), ("pune", 2024), ("delhi", 2023), ("delhi", 2024)],
    names=["city", "year"])).sort_index()

print("every city, one year:")
print(s.loc[(slice(None), 2024), ])
print()
print("pd.IndexSlice is the readable spelling:")
idx = pd.IndexSlice
print(s.loc[idx[:, 2024]])
print()
print("Selection on inner levels usually needs a SORTED index:")
print("   is_monotonic_increasing:", s.index.is_monotonic_increasing)'''),

        ("Aggregating over one level",
         "level= collapses a level without going back to a groupby.",
         '''import pandas as pd

s = pd.Series([10, 20, 30, 40], index=pd.MultiIndex.from_tuples(
    [("pune", 2023), ("pune", 2024), ("delhi", 2023), ("delhi", 2024)],
    names=["city", "year"]))

print("total per city:")
print(s.groupby(level="city").sum())
print()
print("total per year:")
print(s.groupby(level="year").sum())
print()
print("both spellings work; level= is the one that reads clearly")
print("when the keys are already in the index.")'''),

        ("Columns can be hierarchical too",
         "Which is what agg with several statistics gives you.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi"],
    "sales": [10, 20, 30],
    "units": [1, 2, 3],
})
out = df.groupby("city").agg({"sales": ["sum", "mean"], "units": "sum"})
print(out)
print()
print("columns are a MultiIndex:", list(out.columns))
print()
print("select with a tuple:", list(out[("sales", "sum")]))
print()
print("flatten them - the step people forget:")
out.columns = ["_".join(c).strip("_") for c in out.columns]
print(list(out.columns))'''),

        ("When to flatten it away",
         "A MultiIndex is powerful and awkward; reset_index is often the kinder answer.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "pune", "delhi"],
    "year": [2023, 2024, 2023],
    "sales": [10, 20, 30],
})
grouped = df.groupby(["city", "year"])["sales"].sum()

print("as a MultiIndex Series:")
print(grouped)
print()
print("reset_index gives an ordinary frame:")
flat = grouped.reset_index()
print(flat)
print()
print("or ask groupby not to make one:")
print(df.groupby(["city", "year"], as_index=False)["sales"].sum())
print()
print("Keep the MultiIndex when you will select through it or unstack.")
print("Flatten it when the result is going into a merge, a file or a chart.")'''),
    ],
    [
        "You rarely build a MultiIndex on purpose &mdash; <code>groupby</code> with several keys, <code>concat(keys=...)</code> and <code>stack</code> all produce one.",
        "A <strong>tuple</strong> addresses the levels in order: <code>s.loc[(\"pune\", 2024)]</code>. <code>xs</code> takes a cross-section on an inner level.",
        "<code>slice(None)</code> is the wildcard, and <code>pd.IndexSlice</code> is its readable spelling. Inner-level selection usually needs a <strong>sorted</strong> index.",
        "<code>groupby(level=\"city\")</code> collapses one level without rebuilding the group-by.",
        "<code>agg</code> with several statistics gives <strong>hierarchical columns</strong> &mdash; flatten them with a join over the tuples.",
        "Keep it when you will select through it or <code>unstack</code>; <code>reset_index</code> when the result feeds a merge, a file or a chart.",
    ],
    '''
title: The MultiIndex
intro: More than one level on an axis, and when to flatten it away.

## It arrives whether you asked or not

Almost nobody constructs a MultiIndex deliberately. It appears as the result of operations you were doing anyway:

`groupby(["city", "year"])` gives one level per key.

`concat(..., keys=[...])` adds a level naming the source.

`stack()` moves a column level into the index.

`agg` with several statistics per column gives hierarchical **columns**.

So the practical question is rarely "should I build one" and almost always "I have one, now what".

## Selecting

The mental model: a tuple addresses the levels in order, the way a nested dictionary would.

`s.loc["pune"]` selects on the outer level and returns a sub-object with that level dropped.

`s.loc[("pune", 2024)]` addresses both levels and returns a scalar.

`s.loc[["pune", "delhi"]]` takes a list of outer keys.

The awkward case is selecting on an **inner** level while taking everything from the outer one. Two ways:

`s.xs(2024, level="year")` is the readable form for a single cross-section.

`s.loc[(slice(None), 2024), ]` is the general form. `slice(None)` is the wildcard, needed because you cannot write a bare colon inside a tuple. `pd.IndexSlice` makes it look more like normal slicing: `s.loc[pd.IndexSlice[:, 2024]]`.

Selection on inner levels generally requires a **sorted** index. `sort_index()` first if you get a `UnsortedIndexError`, and as a habit after building one.

## Aggregating over a level

`s.groupby(level="city").sum()` collapses one level, keeping the others.

That is usually what you want when the keys are already in the index &mdash; there is no need to `reset_index` and group by the column again.

`sum(level=...)` used to exist as a shortcut and was removed; `groupby(level=...)` is the current spelling.

`unstack()` moves a level into the columns and is often more useful than aggregating: it turns a two-level Series into a readable two-dimensional table.

## Hierarchical columns

`df.groupby("city").agg({"sales": ["sum", "mean"]})` gives columns that are tuples: `("sales", "sum")`.

Selecting needs the tuple: `out[("sales", "sum")]`.

This is where named aggregation earns its place. `agg(total=("sales", "sum"), avg=("sales", "mean"))` produces flat column names and skips this problem entirely.

When you do end up with hierarchical columns, flattening is one line:

```python
out.columns = ["_".join(c).strip("_") for c in out.columns]
```

Forgetting that step is a common source of confusion later, when something downstream cannot find a column called `sales` because the column is really `("sales", "sum")`.

## When to keep it, when to flatten

**Keep it** when you are going to select through it, `unstack` it into a table, or aggregate over its levels. For genuinely hierarchical data &mdash; country/region/city, or a panel indexed by entity and date &mdash; it is the right structure and makes those operations natural.

**Flatten it** when the result is leaving pandas or going into an operation that does not care about hierarchy: a merge, a CSV, a plotting call, a model.

`reset_index()` turns index levels into ordinary columns. `groupby(..., as_index=False)` avoids creating one in the first place.

The honest summary is that a MultiIndex is powerful and awkward in roughly equal measure. It rewards you when the hierarchy is real and the operations use it; it costs you an extra concept at every step when it is merely an artefact of how the result was computed. Most of the time, in ordinary analysis code, flattening early is the kinder choice.

## Building one deliberately

Occasionally you want a MultiIndex before any group-by:

`pd.MultiIndex.from_tuples([...], names=[...])` &mdash; from explicit pairs.

`pd.MultiIndex.from_product([["a","b"], [2023, 2024]])` &mdash; every combination, which is how you build a complete frame to reindex sparse data onto.

`pd.MultiIndex.from_arrays([...])` &mdash; from parallel label arrays.

`df.set_index(["city", "year"])` &mdash; from existing columns, which is the usual route.

`from_product` plus `reindex` is the standard way to make a sparse panel dense: build every expected combination, reindex onto it, and the missing ones appear as `NaN` rather than being silently absent.

## Sorting matters more here

Selection on inner levels requires a **lexsorted** index. Without it, pandas raises `UnsortedIndexError` or performs badly.

`df.index.is_monotonic_increasing` checks. `sort_index()` fixes.

The habit worth forming is to call `sort_index()` immediately after building or reshaping a MultiIndexed object. It is cheap, it removes a class of error, and it makes label ranges work.

`df.index.lexsort_depth` reports how many levels are sorted, which explains why selection works on the first level and fails on the second.

## droplevel, swaplevel, reorder_levels

`droplevel("year")` removes a level entirely &mdash; useful after selecting a single value from it leaves a redundant level behind.

`swaplevel(0, 1)` exchanges two levels, and `sort_index()` afterwards is almost always needed for the result to be usable.

`reorder_levels([...])` handles more than two.

These come up after a `groupby` produced levels in an order that does not suit the next step, and they are cheaper than regrouping.

## Aggregating and selecting together

Two patterns cover most work with a MultiIndexed result.

**Collapse a level**: `df.groupby(level="city").sum()`.

**Move a level to columns**: `df.unstack("year")`, giving a wide table.

`unstack` takes a `level` by name or position, and `fill_value` for the gaps. Chaining `unstack().plot()` is the usual route from a two-key group-by to a chart.

`stack()` reverses it. In recent pandas it has a `future_stack=True` option that changes some edge-case behaviour around missing values; the default is being migrated, so pinning the behaviour explicitly is worth doing in code that must keep working.

## Should you use one at all

The honest position: a MultiIndex is the right structure for genuinely hierarchical data that you will select through, and an unnecessary complication otherwise.

Signs it is earning its place:

You select by partial key regularly.

You aggregate over one level and keep the others.

You unstack it into tables.

The hierarchy is real &mdash; a panel indexed by entity and time, geography at several levels.

Signs it is not:

You immediately `reset_index()` after every operation that produces one.

You are fighting `UnsortedIndexError` and `slice(None)`.

The result is heading for a merge, a CSV or a plotting call.

In the second case, `as_index=False` on the group-by avoids creating it at all, which is simpler than creating and flattening.

## Getting values out

A recurring need is turning a MultiIndexed result into something ordinary code can use.

`reset_index()` &mdash; every level becomes a column.

`reset_index(level="year")` &mdash; one level becomes a column, the rest stay.

`droplevel("year")` &mdash; discard a level entirely.

`to_frame()` on the index &mdash; the labels as a frame, for inspection.

`list(df.index)` &mdash; the labels as tuples.

`df.index.get_level_values("city")` &mdash; one level as a flat array, which is what you want for filtering or for building a mask without resetting anything.

That last one is under-used: `df[df.index.get_level_values("year") == 2024]` filters on a level without any `slice(None)` syntax.

## Column MultiIndexes in particular

Hierarchical **columns** cause more day-to-day friction than hierarchical rows, because most code expects flat column names.

They arrive from `agg` with a list of functions, from `pivot_table` with several value columns, and from `unstack`.

The flattening idiom is worth memorising:

```python
df.columns = ["_".join(map(str, c)).strip("_") for c in df.columns]
```

`map(str, ...)` matters because levels are often not strings &mdash; a year is an integer, and `join` fails on it.

The better answer is usually to avoid creating them: **named aggregation** produces flat names directly, and is clearer at the call site as well.

## Performance

A MultiIndex is a set of integer codes plus level values, so it is compact &mdash; often more so than the equivalent columns, because repeated labels are stored once.

Selection is fast on a lexsorted index and slow otherwise, which is why `sort_index()` matters here more than elsewhere.

Group-by on index levels is comparable to group-by on columns.

The costs are in usability rather than speed: more concepts, more edge cases, and code that other people find harder to follow.

## A summary

They arrive from group-by, `concat(keys=)`, `stack` and `agg` rather than being built.

A tuple addresses the levels; `xs` takes a cross-section; `slice(None)` is the wildcard.

`sort_index()` after building one, always.

`groupby(level=...)` aggregates over a level.

`unstack` turns a level into columns and is often what you actually wanted.

Flatten hierarchical columns with a join over the tuples, or avoid them with named aggregation.

Keep it when the hierarchy is real and you select through it; `reset_index()` when it is an artefact.

## Where it fits

Hierarchical indexes are the price of hierarchical questions. A panel of entities over time, sales by region and city and month, a survey by respondent and question &mdash; all of these have a natural nesting, and a MultiIndex expresses it directly.

The friction comes when the nesting is incidental rather than meaningful: a group-by on two keys produces one whether or not you wanted the structure.

The test is whether you will use the hierarchy. If the next operation selects a level, aggregates over one, or unstacks it into a table, keep it. If the next operation is a merge, a plot or a file, flatten it and move on.

Neither choice is permanent. `set_index` and `reset_index` are cheap and reversible, so the decision can be made per step rather than committed to at the start.

The one thing worth doing consistently is `sort_index()` after building one. Almost every confusing MultiIndex error traces back to an unsorted index, and the fix is a single call that costs nothing on data of ordinary size.

## Two more things worth knowing

`df.index.names` gives the level names and is writable, so an index built without names can be labelled after the fact. Named levels make every later `groupby(level=...)`, `xs` and `unstack` call readable, and unnamed ones force you to count positions.

`pd.IndexSlice` deserves a mention on its own. Written as `idx = pd.IndexSlice`, it turns the awkward `df.loc[(slice(None), 2024), :]` into `df.loc[idx[:, 2024], :]`, which is close enough to ordinary slicing to read at a glance.

Finally, a MultiIndex on the **columns** and one on the **rows** can coexist, which is what `pivot_table` with lists for both `index` and `columns` produces. That is a genuinely useful shape for a printed report and a genuinely awkward one to compute against, which is the trade this whole module describes: the structure that displays best is rarely the structure that manipulates best.

## A worked selection

Putting the selection tools together on one object makes the pattern clearer than any of them alone.

Given sales indexed by `(city, year)`:

`s.loc["pune"]` &mdash; one city, all years, with the city level dropped.

`s.loc[("pune", 2024)]` &mdash; a single value.

`s.loc[["pune", "goa"]]` &mdash; two cities.

`s.xs(2024, level="year")` &mdash; one year, all cities.

`s.loc[pd.IndexSlice[:, 2024]]` &mdash; the same, in slice form.

`s[s.index.get_level_values("year") == 2024]` &mdash; the same again, as an ordinary mask, and the form that composes with other conditions.

`s.groupby(level="city").sum()` &mdash; totals per city.

`s.unstack("year")` &mdash; a table, cities down, years across.

Six ways to ask about one year, which is a fair summary of why MultiIndexes feel heavy. The last two are the ones worth reaching for by default: aggregate a level, or unstack it into a shape that reads.

## In summary

A MultiIndex arrives from operations you were doing anyway, and the useful question is whether to keep it.

Keep it when the hierarchy is real and the next step selects a level, aggregates over one, or unstacks it into a table. Flatten it when the result is heading for a merge, a file or a chart.

Sort it as soon as you build it, because most confusing errors here are an unsorted index. Use `xs` or a mask on `get_level_values` rather than fighting `slice(None)`. And prefer named aggregation, which avoids hierarchical columns entirely rather than requiring them to be flattened afterwards.
''',
    [
        {"q": "Where do most MultiIndexes come from?",
         "options": ["Explicit construction", "Operations you were doing anyway - groupby with several keys, concat(keys=), stack, agg", "read_csv", "sort_index"],
         "answer": 1,
         "why": "The practical question is rarely 'should I build one' but 'I have one, now what'."},
        {"q": "How do you select on an inner level while taking everything from the outer?",
         "options": ["s.loc[:, 2024]", "s.xs(2024, level='year') or s.loc[(slice(None), 2024), ]", "s[2024]", "s.iloc[2024]"],
         "answer": 1,
         "why": "slice(None) is the wildcard because you cannot write a bare colon inside a tuple. pd.IndexSlice is its readable spelling."},
        {"q": "What does `agg({'sales': ['sum','mean']})` do to the columns?",
         "options": ["Nothing", "Makes them hierarchical tuples like ('sales','sum')", "Renames them", "Drops one"],
         "answer": 1,
         "why": "Named aggregation - agg(total=('sales','sum')) - produces flat names and skips the problem entirely."},
        {"q": "When should you flatten a MultiIndex with `reset_index`?",
         "options": ["Always immediately", "When the result feeds a merge, a file or a chart rather than being selected through", "Never", "Only for Series"],
         "answer": 1,
         "why": "Keep it when the hierarchy is real and you will select through it or unstack. Flatten when it is merely an artefact of how the result was computed."},
    ],
)


# ---------------------------------------------------------------------------
# 23. Time series
# ---------------------------------------------------------------------------
topic(
    "time_series",
    "Time Series",
    "Working with Data",
    "resample, rolling and shift - the three operations that need the rows to be "
    "in time order.",
    _svg(_grid(18, 44, 8, 1, 11) + _txt(52, 36, "daily", M, 8) +
         _arrow(110, 50, 126, 50) +
         _grid(130, 44, 2, 1, 11) + _txt(140, 36, "monthly", A, 7)),
    [
        ("A DatetimeIndex is the prerequisite",
         "resample and rolling-by-time both need one.",
         '''import pandas as pd
import numpy as np

s = pd.Series(np.arange(10),
              index=pd.date_range("2024-01-01", periods=10, freq="D"))
print(s.head(3))
print()
print("index type:", type(s.index).__name__)
print("frequency :", s.index.freq)
print()
plain = pd.Series(np.arange(10))
try:
    plain.resample("D").sum()
except TypeError as e:
    print("resample without a DatetimeIndex ->", type(e).__name__)
    print("   ", str(e)[:56])'''),

        ("resample changes the frequency",
         "Downsampling aggregates; it is groupby for time.",
         '''import pandas as pd
import numpy as np

idx = pd.date_range("2024-01-01", periods=60, freq="D")
s = pd.Series(np.arange(60), index=idx)

print("daily -> monthly totals:")
print(s.resample("ME").sum())
print()
print("weekly means:")
print(s.resample("W").mean().head(3))
print()
print("several statistics:")
print(s.resample("ME").agg(["sum", "mean", "size"]))'''),

        ("Upsampling creates gaps you must fill",
         "Going finer invents rows, and they start empty.",
         '''import pandas as pd

s = pd.Series([10, 20],
              index=pd.to_datetime(["2024-01-01", "2024-01-04"]))
print("original:"); print(s)
print()
up = s.resample("D").asfreq()
print("daily, unfilled:"); print(up)
print()
print("forward filled:"); print(s.resample("D").ffill())
print()
print("interpolated:"); print(s.resample("D").interpolate())
print()
print("Choose deliberately - ffill asserts the value held, interpolate")
print("asserts it moved smoothly. They are different claims.")'''),

        ("rolling windows",
         "A moving statistic over the last n rows, or the last n days.",
         '''import pandas as pd
import numpy as np

s = pd.Series([1, 2, 3, 4, 5],
              index=pd.date_range("2024-01-01", periods=5, freq="D"))

print("3-row rolling mean:")
print(s.rolling(3).mean())
print("   the first two are NaN - the window is not full yet")
print()
print("min_periods=1 starts immediately:")
print(list(s.rolling(3, min_periods=1).mean()))
print()
print("a time-based window handles irregular gaps:")
print(list(s.rolling("3D").sum()))
print()
print("expanding() is a window that grows from the start:")
print(list(s.expanding().sum()))'''),

        ("shift compares a row with its past",
         "The basis of differences, growth rates and lagged features.",
         '''import pandas as pd

s = pd.Series([100, 110, 121],
              index=pd.date_range("2024-01-01", periods=3, freq="D"))

print("original:", list(s))
print("shift(1) :", list(s.shift(1)), "<- everything moved down one")
print()
print("difference from yesterday:", list(s.diff()))
print("percent change           :", [round(v, 4) if pd.notna(v) else None
                                     for v in s.pct_change()])
print()
print("shift is what makes a lagged feature:")
df = pd.DataFrame({"value": s})
df["yesterday"] = df["value"].shift(1)
print(df)'''),

        ("Order matters, and pandas will not check it",
         "Every operation here assumes the rows are sorted in time.",
         '''import pandas as pd

idx = pd.to_datetime(["2024-01-03", "2024-01-01", "2024-01-02"])
s = pd.Series([30, 10, 20], index=idx)

print("out of order:"); print(s)
print()
print("diff() on unsorted data is meaningless:")
print(list(s.diff()))
print()
print("sorted first:")
print(list(s.sort_index().diff()))
print()
print("pandas did not warn either time. sort_index() before any")
print("shift, diff, rolling or resample on data you did not sort.")'''),
    ],
    [
        "<code>resample</code> and time-based <code>rolling</code> require a <strong>DatetimeIndex</strong> and raise without one.",
        "<code>resample(\"ME\").sum()</code> is group-by for time &mdash; downsampling aggregates, and takes <code>agg</code> like any group-by.",
        "<strong>Upsampling</strong> creates empty rows: <code>ffill</code> asserts the value held, <code>interpolate</code> asserts it moved smoothly. Different claims.",
        "<code>rolling(n)</code> gives NaN until the window fills; <code>min_periods=1</code> starts immediately, and <code>rolling(\"3D\")</code> windows by time.",
        "<code>shift</code>, <code>diff</code> and <code>pct_change</code> compare each row with its past &mdash; the basis of lagged features.",
        "All of these assume the rows are in <strong>time order</strong>, and pandas does not check. <code>sort_index()</code> first.",
    ],
    '''
title: Time Series
intro: resample, rolling and shift.

## The index does the work

Everything in this module depends on the frame having a `DatetimeIndex`. `resample` raises without one, and time-based windows have nothing to measure against.

`df.set_index("date")` after `pd.to_datetime` is the usual setup, and it is the step people skip before wondering why `resample` will not run.

Once the index is a timeline, pandas can do things that would otherwise need a lot of arithmetic: select a month by name, aggregate by period, window by duration rather than by row count.

## resample

`resample` is group-by where the groups are time periods.

**Downsampling** &mdash; daily to monthly &mdash; aggregates, and takes the same methods as `groupby`: `sum()`, `mean()`, `agg(["sum", "mean"])`.

The frequency string is the argument that matters. `D` daily, `W` weekly, `ME` month end, `MS` month start, `QE` quarter end, `YE` year end, `h` hourly, `min` minutely.

Note that pandas 2.2 **renamed** several of these. `M` became `ME`, `H` became `h`, `T` became `min`. Older code and older tutorials use the old spellings, which now warn or fail depending on version. If a frequency string does not work, that rename is the likely reason.

The label of each output row is the **end** of the period for `ME`, and the start for `MS`. `label=` and `closed=` control which boundary is used and which side is inclusive, and they matter when periods must line up with something external.

## Upsampling invents rows

Going to a finer frequency creates rows that did not exist, and they start as `NaN`.

`asfreq()` leaves them empty, which is honest and rarely useful on its own.

`ffill()` carries the last known value forward. That asserts the value **held constant** until the next observation &mdash; correct for a price, a status, a setting.

`interpolate()` fits between the known points. That asserts the value **moved smoothly** &mdash; correct for a temperature, a position, anything continuous.

These are different claims about the world, and choosing between them is a modelling decision rather than a formatting one. Both fabricate data; the question is which fabrication is less wrong for what the number means.

## rolling

`s.rolling(3).mean()` gives a moving average over the last three **rows**.

The first two results are `NaN`, because the window is not yet full. That is deliberate &mdash; a three-row average computed from one row is not a three-row average. `min_periods=1` overrides it and starts computing immediately, which is convenient and slightly dishonest at the edges.

`s.rolling("3D")` windows by **time** rather than row count. This is the one to use when observations are irregularly spaced, because three rows might span three days or three months, and only the time-based window means what you said.

`center=True` puts the window around each point rather than behind it. It is right for smoothing a curve for display and wrong for anything predictive, because it uses future values.

`expanding()` is a window that grows from the start &mdash; a running total or a cumulative mean.

`ewm()` gives exponentially weighted statistics, where recent observations count for more.

## shift, diff, pct_change

`shift(1)` moves every value down one row, so each row can see the previous one. `shift(-1)` looks forward.

`diff()` is `s - s.shift(1)`. `pct_change()` is the relative version.

These are how you build lagged features, growth rates and change detection. The first row is always `NaN`, because it has no predecessor.

Within groups, use the group-by versions &mdash; `df.groupby("id")["v"].diff()` &mdash; or the shift crosses from one entity into another and produces a difference between unrelated rows. That is a common and quiet error in panel data.

## Order is assumed, not checked

Every operation here &mdash; `shift`, `diff`, `rolling`, `resample` &mdash; assumes the rows are in time order.

pandas does **not** verify it. `diff()` on unsorted data returns numbers, and they are meaningless.

`sort_index()` before any of these on data you did not sort yourself. It is one line, and the failure it prevents produces plausible output rather than an error.

The same applies to duplicated timestamps: two rows for the same instant make `diff` and `rolling` ambiguous, and are usually a sign of a data problem worth looking at before aggregating over it.

## Frequency strings

The alias is the argument that decides what `resample` and `date_range` do, and pandas 2.2 renamed several of them.

`D` day, `B` business day, `W` week (ending Sunday by default, `W-MON` to change it), `MS` month start, `ME` month end, `QS`/`QE` quarter, `YS`/`YE` year, `h` hour, `min` minute, `s` second.

The renames: `M` to `ME`, `H` to `h`, `T` to `min`, `S` to `s`. Older code and most tutorials use the old spellings, which now warn or fail. When a frequency string does not work, this is the first thing to check.

Multiples work: `"15min"`, `"2W"`, `"3ME"`.

Anchored offsets pin the boundary: `"W-FRI"` for weeks ending Friday, `"QE-JAN"` for quarters ending in January, which matters for fiscal years that do not start in January.

## Which label a period gets

`resample("ME")` labels each group with the **end** of the period; `"MS"` with the start.

`label="left"` or `"right"` overrides which boundary names the group, and `closed=` decides which end is inclusive.

These matter whenever the output must line up with something produced elsewhere. A monthly total labelled 2024-01-31 and one labelled 2024-01-01 are the same number with different index labels, and joining them gives nothing.

Settling on a convention early &mdash; usually period start &mdash; saves reconciliation later.

## Grouping by time and something else

`resample` groups by time only. To group by time **and** a category, `pd.Grouper` combines with ordinary keys:

```python
df.groupby([pd.Grouper(key="date", freq="ME"), "city"])["sales"].sum()
```

`key=` names the date column, so this works without setting an index, which is what makes `Grouper` more useful than `resample` in practice.

The result is a MultiIndex, and `unstack("city")` gives the wide table.

## Rolling in more depth

`min_periods` decides how many observations a window needs before producing a value. The default for a fixed-size window is the window size; for a time-based window it is 1.

`closed=` controls whether the window includes its endpoints, which matters for time-based windows where an observation may sit exactly on the boundary.

`win_type` gives weighted windows &mdash; Gaussian, triangular &mdash; for smoothing.

`rolling(...).apply(func, raw=True)` runs a custom function per window. `raw=True` passes a NumPy array rather than a Series and is substantially faster.

Within groups, `df.groupby("id")["v"].rolling(3).mean()` windows inside each group and returns a MultiIndexed result, which usually needs `droplevel(0)` before it can be assigned back.

## Gaps, and what they hide

A rolling window over rows assumes the rows are evenly spaced. Real time series have gaps &mdash; weekends, outages, missing readings &mdash; and a three-row window may span three days or three weeks.

Two fixes:

**Window by time**: `rolling("3D")` means three days whatever the row spacing.

**Regularise first**: `resample("D").mean()` produces a row per day, with `NaN` where there was no data, after which row-based windows mean what they say.

Which is right depends on whether an absent observation should count as missing or simply not exist. That is a modelling question, and `resample` forces you to answer it, which is an argument for doing it early.

## A checklist for time-series work

Parse the dates and check the dtype.

Set a `DatetimeIndex`, or plan to use `pd.Grouper(key=...)`.

`sort_index()`.

Check for duplicated timestamps.

Decide on a time zone, or commit to naive throughout.

Decide whether gaps are missing or absent, and regularise if they are missing.

Then `resample`, `rolling` and `shift` mean what they appear to mean.

## Aligning two series with different frequencies

A common task: daily data and monthly targets, joined for comparison.

The wrong approach is a merge on dates, which matches almost nothing.

The right approach is to bring both to the same frequency first:

```python
monthly = daily.resample("MS").sum()
combined = monthly.join(targets)
```

Or, going the other way, upsample the monthly figure and forward-fill it so every day carries its month's target.

Which direction is right depends on the question. Aggregating up loses detail and is usually correct for reporting; spreading down invents precision and is usually correct for per-row comparison. Either way, the alignment step is explicit rather than implied by a join.

`MS` versus `ME` matters here: two monthly series labelled at opposite ends of the month will not join at all.

## Lags and leads for modelling

`shift(1)` gives the previous value &mdash; a lag, safe to use as a predictor.

`shift(-1)` gives the next value &mdash; a lead, which is the **target** in a forecasting problem and must never be a feature.

Using a lead as a feature is data leakage, and it produces models that score beautifully and fail in production. Because both are one method with a sign, the mistake is easy to make and invisible in the code.

Rolling features have the same hazard: `rolling(3, center=True)` uses future values. For anything predictive, windows must look backwards only, which is the default without `center`.

Within groups, all of these need the group-wise form, or the lag crosses from one entity to the next.

## Missing periods

A gap in a time series is either "no observation" or "no event", and the two need different handling.

`resample("D").sum()` gives 0 for days with no rows &mdash; correct if the series counts events.

`resample("D").mean()` gives `NaN` &mdash; correct if the series measures something that existed but was not recorded.

Choosing the wrong one produces a series that looks complete and is wrong at exactly the interesting points.

`asfreq()` makes the gaps explicit without aggregating, which is the honest first step when you are not yet sure.

## A summary

A `DatetimeIndex` is the prerequisite for `resample` and time-based windows.

Frequency aliases were renamed in pandas 2.2 &mdash; `ME`, `h`, `min`.

Downsampling aggregates; upsampling invents rows that need filling deliberately.

`ffill` asserts a value held; `interpolate` asserts it moved smoothly.

`rolling("3D")` for irregular spacing; `min_periods` for the edges.

`shift(-1)` is a lead and belongs only in a target, never a feature.

Use the group-wise forms on panel data.

`sort_index()` first, always, because none of these check.

## A closing note

Time series work rewards setting things up properly and punishes assumptions.

The setup is short: parse the dates with an explicit format, check the dtype, decide on a time zone, set a `DatetimeIndex` if you need period selection, and sort. Every operation in this module assumes that order and none of them check it, so `diff` on unsorted rows returns numbers that mean nothing.

The recurring decision is what a gap means. A day with no rows is either zero events or an unrecorded measurement, and `resample("D").sum()` and `.mean()` encode those two different answers. Choosing without noticing gives a series that looks complete and is wrong exactly where the interesting things happen.

And on panel data &mdash; several entities stacked in one frame &mdash; `shift`, `diff` and `rolling` must be done within groups, or the comparison runs across the boundary from one entity into the next and produces a plausible number from unrelated rows.

## One more thing

`resample` accepts `origin=` and `offset=`, which control where the period boundaries fall. That matters for data that should be bucketed on something other than midnight or the first of the month &mdash; a business day starting at 6am, or weeks aligned to a fiscal calendar.
''',
    [
        {"q": "What does `resample` require?",
         "options": ["A sorted frame", "A DatetimeIndex - it raises without one", "A frequency column", "Numeric data"],
         "answer": 1,
         "why": "df.set_index('date') after pd.to_datetime is the usual setup, and the step people skip before wondering why resample will not run."},
        {"q": "What is the difference between `ffill` and `interpolate` when upsampling?",
         "options": ["None", "ffill asserts the value held constant; interpolate asserts it moved smoothly", "interpolate is faster", "ffill only works on integers"],
         "answer": 1,
         "why": "Different claims about the world. Both fabricate data - the question is which fabrication is less wrong for what the number means."},
        {"q": "Why does `rolling(3).mean()` start with NaN?",
         "options": ["A bug", "The window is not full - a three-row average from one row is not a three-row average", "The data is missing", "It needs sorting"],
         "answer": 1,
         "why": "min_periods=1 overrides it, which is convenient and slightly dishonest at the edges."},
        {"q": "What does pandas do if you call `diff()` on rows that are not in time order?",
         "options": ["Sorts them first", "Returns meaningless numbers without warning", "Raises", "Returns NaN"],
         "answer": 1,
         "why": "Order is assumed, not checked. sort_index() before any shift, diff, rolling or resample on data you did not sort yourself."},
    ],
)


# ---------------------------------------------------------------------------
# 24. Reading and writing
# ---------------------------------------------------------------------------
topic(
    "reading_and_writing",
    "Reading and Writing Files",
    "Working with Data",
    "read_csv's arguments earn their keep - and the ones that prevent a whole "
    "class of bug.",
    _svg(_box(18, 30, 40, 30, S) + _txt(38, 49, "csv", M, 8) +
         _arrow(62, 45, 80, 45) + _txt(71, 38, "read", A, 7) +
         _box(88, 30, 46, 30, S, A) + _txt(111, 49, "DataFrame", A, 7)),
    [
        ("read_csv infers, and inference is where bugs start",
         "Three columns, three wrong guesses, no errors.",
         '''import pandas as pd
import io

csv = """id,joined,amount
007,2024-01-05,1000
008,2024-02-11,
009,2024-03-30,3000
"""
df = pd.read_csv(io.StringIO(csv))
print(df)
print()
print(df.dtypes)
print()
print("id     -> int64  : leading zeros gone, 007 is now 7")
print("joined -> object : still text, so it will sort lexically")
print("amount -> float64: one gap made the whole column float")'''),

        ("Steering it with dtype and parse_dates",
         "Saying what you know is faster and safer than fixing it afterwards.",
         '''import pandas as pd
import io

csv = """id,joined,amount
007,2024-01-05,1000
008,2024-02-11,
009,2024-03-30,3000
"""
df = pd.read_csv(io.StringIO(csv),
                 dtype={"id": str, "amount": "Int64"},
                 parse_dates=["joined"])
print(df)
print()
print(df.dtypes)
print()
print("id stayed '007', joined is a real timestamp, and amount is a")
print("nullable integer that holds the gap without becoming float.")'''),

        ("Only reading what you need",
         "usecols and nrows matter as soon as the file is large.",
         '''import pandas as pd
import io

csv = "a,b,c,d\\n" + "\\n".join("%d,%d,%d,%d" % (i, i, i, i) for i in range(1000))

full = pd.read_csv(io.StringIO(csv))
part = pd.read_csv(io.StringIO(csv), usecols=["a", "d"])

print("all columns :", full.shape, "%.1f KB" % (full.memory_usage(deep=True).sum() / 1e3))
print("two columns :", part.shape, "%.1f KB" % (part.memory_usage(deep=True).sum() / 1e3))
print()
print("peek at a big file before committing to it:")
print(pd.read_csv(io.StringIO(csv), nrows=3))'''),

        ("Missing-value markers",
         "pandas knows the common ones and not yours.",
         '''import pandas as pd
import io

csv = """name,score
ana,10
raj,N/A
kim,missing
sam,-999
"""
df = pd.read_csv(io.StringIO(csv))
print(df)
print("dtype:", df["score"].dtype, "<- object, because of the text markers")
print()
better = pd.read_csv(io.StringIO(csv), na_values=["missing", "-999"])
print(better)
print("dtype:", better["score"].dtype)
print()
print("'N/A' was recognised automatically; 'missing' and -999 were not.")'''),

        ("Writing it back",
         "The index is written by default, which surprises people on the round trip.",
         '''import pandas as pd
import io

df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})

print("to_csv() writes the index as an unnamed first column:")
print(df.to_csv())
print("reading that back gives a stray column:")
print(list(pd.read_csv(io.StringIO(df.to_csv())).columns))
print()
print("index=False is almost always what you want:")
print(df.to_csv(index=False))
print("   round trip:", list(pd.read_csv(io.StringIO(df.to_csv(index=False))).columns))'''),

        ("CSV loses everything the frame knew",
         "Types, categories and the index are all just text on the way out.",
         '''import pandas as pd
import io

df = pd.DataFrame({
    "n": pd.Series([1, 2], dtype="Int64"),
    "c": pd.Series(["a", "b"], dtype="category"),
    "d": pd.to_datetime(["2024-01-01", "2024-02-01"]),
})
print("before:"); print(df.dtypes)
print()
back = pd.read_csv(io.StringIO(df.to_csv(index=False)))
print("after a CSV round trip:"); print(back.dtypes)
print()
print("Int64 became int64, category became object, the date became text.")
print("For anything that must survive, use parquet or pickle - or write")
print("the dtypes down and restore them on read.")'''),
    ],
    [
        "<code>read_csv</code> infers types, and the three usual casualties are <strong>leading zeros</strong>, <strong>unparsed dates</strong> and an integer column turned float by one gap.",
        "<code>dtype=</code>, <code>parse_dates=</code> and <code>Int64</code> fix all three at read time, which is faster than converting afterwards.",
        "<code>usecols</code> and <code>nrows</code> matter as soon as the file is large &mdash; read a sample before committing to the whole thing.",
        "<code>na_values=</code> adds your own missing markers; pandas recognises <code>N/A</code> and friends but not <code>missing</code> or <code>-999</code>.",
        "<code>to_csv()</code> writes the index by default, producing a stray unnamed column on the round trip. Pass <code>index=False</code>.",
        "CSV is <strong>text</strong>: dtypes, categories and dates do not survive. Use parquet when they must.",
    ],
    '''
title: Reading and Writing Files
intro: read_csv's arguments, and the ones that prevent a class of bug.

## Inference is convenient and lossy

`read_csv` guesses a dtype per column. That is why it is pleasant to use and why the same three problems appear in almost every project.

**Leading zeros disappear.** An id column of `007`, `008` is read as integers, and the zeros are gone permanently. No error, and the values still look like ids.

**Dates stay text.** Nothing is parsed as a date unless you ask. The column sorts lexically, `.dt` does not work, and date arithmetic is unavailable.

**One gap makes a column float.** NumPy integers cannot hold `NaN`, so a single missing value promotes the whole column, and ids print as `1001.0`.

All three are fixed at read time by saying what you know.

## The arguments that matter

`dtype={"id": str}` keeps identifiers as text. This is the fix for leading zeros, and it should be the default for anything that is a code rather than a quantity &mdash; postcodes, account numbers, phone numbers.

`dtype={"amount": "Int64"}` uses the nullable integer type, so the column holds gaps without becoming float.

`parse_dates=["joined"]` converts during the read, which is faster than converting after. Add `date_format=` when the format is known and unambiguous.

`usecols=["a", "d"]` reads only the columns you name. On a wide file this saves both time and memory, and it is the single most effective argument for large data.

`nrows=1000` reads a sample. Always look at a sample of an unfamiliar file before loading all of it &mdash; it is how you find out that the delimiter is wrong, or that there are three header rows, or that the file is not what you were told.

`index_col="id"` sets the index during the read.

`na_values=["missing", "-999"]` adds markers. pandas recognises a standard list &mdash; empty, `NA`, `N/A`, `null`, `NaN` and a few more &mdash; but it cannot know that this dataset writes `missing`, or that `-999` is a sentinel. Left alone, the text markers make the column `object` and the numeric sentinel is treated as a real value, which quietly poisons every average.

`skiprows`, `header=None` and `names=[...]` handle files whose top is not a clean header row.

`chunksize=n` returns an iterator of frames rather than one frame, which is how you process a file larger than memory.

## Writing

`to_csv()` writes the index as an unnamed first column by default.

Read that file back and you get a spurious `Unnamed: 0` column. It is harmless, ubiquitous, and entirely avoidable: **pass `index=False`** unless the index is meaningful data.

Other arguments worth knowing: `float_format="%.2f"` controls precision, `columns=` selects what to write, `sep=` changes the delimiter, and `encoding="utf-8"` is worth being explicit about when the data leaves your machine.

## CSV loses what the frame knew

A CSV is text. Everything pandas knew about the data is discarded on the way out:

`Int64` becomes plain `int64` on the way back, or `float64` if there were gaps.

`category` becomes `object`, and the category order is gone.

Datetimes become strings again, unless the reader is told to parse them.

The index becomes a column, or vanishes.

That round-trip loss is the argument for a binary format when the data is going to be read back by pandas:

**Parquet** (`to_parquet` / `read_parquet`) preserves dtypes, is columnar, compresses well, and is readable by many tools. It needs `pyarrow` installed &mdash; which is why the editors here use CSV.

**Pickle** (`to_pickle`) preserves everything exactly, including categories and custom objects, but is Python-specific, version-fragile, and **executes code on load**. Never unpickle a file you did not create.

**HDF5** suits very large numeric data with partial reads.

For anything you will read back yourself, Parquet is usually the right answer. For anything a human or another tool must read, CSV is worth its losses &mdash; but write down the dtypes somewhere, because the reader will have to guess exactly as you did.

## A loading routine

Read a sample with `nrows`. Look at it. Decide the dtypes, the date columns, the missing markers and the columns you actually need. Then read the whole file with those arguments set.

That takes a minute and removes most of what the cleaning modules exist to fix.

## Files that are not quite CSV

Real exports are rarely clean, and `read_csv` has an argument for each common defect.

`sep="\t"` for tab-separated; `sep=None` with `engine="python"` sniffs the delimiter.

`skiprows=3` skips a preamble; `skiprows=lambda i: i % 2` skips selectively.

`header=None` with `names=[...]` handles a file with no header row.

`skipfooter=2` drops trailing summary lines, and requires `engine="python"`.

`thousands=","` parses `1,234` as a number rather than leaving it as text. Without it, a single formatted number makes the whole column `object`.

`decimal=","` handles European decimal commas.

`encoding="latin-1"` when UTF-8 fails, which is the usual cause of a `UnicodeDecodeError` on files from older Windows tools.

`quotechar` and `escapechar` for embedded delimiters.

`comment="#"` ignores comment lines.

When a file will not parse, working through that list is faster than writing a custom reader.

## Reading in chunks

`chunksize=n` returns an iterator of frames rather than one frame:

```python
totals = []
for chunk in pd.read_csv(path, chunksize=100_000):
    totals.append(chunk.groupby("city")["sales"].sum())
result = pd.concat(totals).groupby(level=0).sum()
```

That processes a file larger than memory, provided the operation can be done piecewise. Sums, counts and group sums can; a median cannot, without more work.

The pattern is: reduce each chunk, collect the small results, combine at the end. Collecting the raw chunks and concatenating them defeats the purpose.

## Excel

`pd.read_excel(path, sheet_name="Sheet1")` needs `openpyxl` for `.xlsx`.

`sheet_name=None` reads **every** sheet into a dict of frames, which is the quickest way to see what a workbook contains.

Excel files carry types, so dates usually arrive parsed &mdash; but they also carry merged cells, hidden rows and formatting that mean nothing to pandas, and a sheet that looks tabular on screen is often not.

`header=`, `usecols="B:D"` and `skiprows=` do the same jobs as in `read_csv`.

Writing several frames to one workbook uses `pd.ExcelWriter` as a context manager, with one `to_excel` call per sheet.

## Compression and paths

`read_csv` and `to_csv` handle compression transparently from the extension: `.gz`, `.bz2`, `.zip`, `.xz`. A gzipped CSV is often a third of the size and costs little to read.

Both accept URLs as well as paths, which is convenient for public datasets and a bad idea in production code, where the file should be fetched and cached deliberately.

`pathlib.Path` objects work anywhere a path string does.

## Choosing a format

**CSV** &mdash; universal, human-readable, lossy about types, slow to parse. Right when something other than pandas must read it.

**Parquet** &mdash; typed, columnar, compressed, fast, readable by many tools. The right default for data pandas will read back. Needs `pyarrow`.

**Pickle** &mdash; preserves everything exactly, Python-only, version-fragile, and **executes code on load**. Fine for a short-lived cache you created; never for input you did not.

**JSON** &mdash; good for nested data, verbose for tabular, and `json_normalize` handles the flattening.

**HDF5** &mdash; large numeric arrays with partial reads.

**SQL** &mdash; when several processes need the data, or it outgrows one machine.

The decision is mostly: who reads this next? If the answer is pandas, use Parquet. If it is a person or another tool, use CSV and accept the losses. If it is a system, use a database.

## Writing for a round trip

If pandas will read the file back, the goal is to lose nothing.

Parquet does that: dtypes, categories and datetimes all survive, and it is smaller and faster than CSV.

If Parquet is unavailable, CSV plus an explicit read specification is the workaround &mdash; record the dtypes alongside the file, and pass them on read:

```python
dtypes = df.dtypes.astype(str).to_dict()
json.dump(dtypes, open("schema.json", "w"))
```

That is clumsy and it works. What does not work is assuming the reader will infer the same types you had, because inference depends on the data and the data changes.

## Validating on load

The most useful place for checks is immediately after reading, where a problem is closest to its cause:

```python
df = pd.read_csv(path, dtype=..., parse_dates=[...])

assert list(df.columns) == expected_columns
assert df["id"].is_unique
assert df["date"].notna().all()
assert len(df) > 0
```

Column-name checks are the highest value of these. An upstream export that renames or reorders columns is common, and without a check the failure appears much later as a `KeyError` or, worse, as a column of the wrong data under the right name.

## Large files

The order to try, as a file grows:

`usecols` and `dtype` &mdash; often enough on its own, and always worth doing first.

`nrows` for development, so the edit-run cycle stays fast.

`chunksize` with per-chunk reduction, when the whole file cannot be held.

Parquet, which reads only the columns requested and is far faster to parse.

A database or DuckDB, when the data outgrows one machine's memory even column-wise.

Reaching for the last option first is a common mistake; `usecols` and `dtype` frequently make a "too large" file comfortable.

## A summary

`read_csv` infers, and inference loses leading zeros, leaves dates as text, and turns integers with gaps into floats.

`dtype`, `parse_dates`, `usecols` and `na_values` prevent all of that at read time.

Read a sample with `nrows` before committing to a large file.

`to_csv(index=False)` unless the index is data.

CSV loses types; Parquet does not.

`allow_pickle`-style trust applies to `read_pickle` too &mdash; never load one you did not create.

Validate immediately after loading, especially the column names.

And for a large file, `usecols` and `dtype` are the first thing to try, not the last.

## A closing note

The boundary between a file and a DataFrame is where most silent damage happens, and it is the cheapest place to prevent it.

`read_csv` guesses, and its guesses lose leading zeros, leave dates as text, and turn integers with a single gap into floats. Every one of those is fixed by an argument, and every one of them is much harder to fix later &mdash; leading zeros in particular are gone for good.

The habit worth building is to read a sample first, look at it, decide the types, and then read the file properly. That takes a minute and replaces an afternoon of confused debugging.

On the way out, `index=False` unless the index is data, and Parquet rather than CSV whenever pandas will be the one reading it back. CSV is a text interchange format, and treating it as a storage format means accepting that everything the frame knew about its own types is discarded each time.

## One more thing

`read_csv` accepts a `converters` dict mapping column names to functions, applied during the read. It is slower than `dtype` and handles cases `dtype` cannot &mdash; stripping a currency symbol, parsing a bespoke format &mdash; without a separate cleaning pass afterwards.

And `to_csv` with no path returns the CSV as a **string** rather than writing a file, which is how you round-trip through `io.StringIO` in a test, or hand the text to something that wants a string rather than a filename.

## In summary

The read is where types are decided, and inference makes three predictable mistakes: leading zeros lost, dates left as text, integers with a gap turned into floats.

`dtype`, `parse_dates`, `usecols` and `na_values` prevent all three, cost nothing, and are far cheaper than repairing the damage afterwards.

Read a sample first and look at it. Validate the column names on load. Write with `index=False`. And when pandas will be the one reading the file back, use Parquet, because CSV discards everything the frame knew about itself.
''',
    [
        {"q": "A CSV id column contains 007. What does `read_csv` do by default?",
         "options": ["Keeps it as '007'", "Reads it as the integer 7, losing the zeros permanently", "Raises", "Makes it a category"],
         "answer": 1,
         "why": "dtype={'id': str} at read time is the fix, and should be the default for anything that is a code rather than a quantity."},
        {"q": "Which argument stops one missing value turning an integer column into float?",
         "options": ["na_values", "dtype={'col': 'Int64'} - the nullable integer type", "parse_dates", "usecols"],
         "answer": 1,
         "why": "NumPy integers cannot hold NaN, so a single gap promotes the whole column and ids start printing as 1001.0"},
        {"q": "Why does a round-tripped CSV often gain an `Unnamed: 0` column?",
         "options": ["A pandas bug", "to_csv writes the index by default - pass index=False", "The file was corrupt", "read_csv adds it"],
         "answer": 1,
         "why": "Harmless, ubiquitous and entirely avoidable. Pass index=False unless the index is meaningful data."},
        {"q": "What is lost when a DataFrame round-trips through CSV?",
         "options": ["Nothing", "Dtypes, categories, category order and datetime types - it is all just text", "Only the column names", "Only missing values"],
         "answer": 1,
         "why": "Use parquet when the data will be read back by pandas. CSV is worth its losses when a human or another tool must read it."},
    ],
)


# ---------------------------------------------------------------------------
# 25. Performance
# ---------------------------------------------------------------------------
topic(
    "performance",
    "Performance",
    "Working with Data",
    "Where the time actually goes in a pandas script, in the order worth fixing "
    "it.",
    _svg(_box(18, 26, 40, 12, S, "#a44") + _txt(38, 35, "loops", "#e88", 7) +
         _box(18, 42, 40, 12, S) + _txt(38, 51, "dtypes", M, 7) +
         _box(18, 58, 40, 12, S) + _txt(38, 67, "copies", M, 7) +
         _arrow(64, 48, 80, 48) + _txt(110, 52, "measure first", A, 8)),
    [
        ("Per-row Python is the whole story",
         "Four spellings of the same operation, two orders of magnitude apart.",
         '''import pandas as pd
import numpy as np
import time

n = 100_000
df = pd.DataFrame({"a": np.arange(n), "b": np.arange(n)})

def timed(fn):
    t = time.perf_counter(); fn(); return time.perf_counter() - t

t_iter = timed(lambda: [r.a * r.b for r in df.itertuples()])
t_apply = timed(lambda: df.apply(lambda r: r["a"] * r["b"], axis=1))
t_zip = timed(lambda: [a * b for a, b in zip(df["a"], df["b"])])
t_vec = timed(lambda: df["a"] * df["b"])

print("apply(axis=1)  : %.4f s" % t_apply)
print("itertuples     : %.4f s" % t_iter)
print("zip of columns : %.4f s" % t_zip)
print("vectorised     : %.4f s" % t_vec)
print()
print("vectorised is %.0fx faster than apply(axis=1)" % (t_apply / max(t_vec, 1e-9)))'''),

        ("iterrows is the one never to use",
         "It converts every row to an object Series, losing dtypes on the way.",
         '''import pandas as pd
import numpy as np
import time

df = pd.DataFrame({"a": np.arange(20_000), "b": np.arange(20_000)})

t = time.perf_counter()
for _, row in df.iterrows():
    pass
rows = time.perf_counter() - t

t = time.perf_counter()
for _ in df.itertuples():
    pass
tuples = time.perf_counter() - t

print("iterrows   : %.4f s" % rows)
print("itertuples : %.4f s" % tuples)
print("ratio      : %.0fx" % (rows / max(tuples, 1e-9)))
print()
mixed = pd.DataFrame({"i": [1], "s": ["x"]})
first = next(mixed.iterrows())[1]
print("and iterrows loses the dtypes:", first.dtype,
      "<- the int became object")'''),

        ("dtype is the cheapest memory win",
         "category and downcasting, measured on the same frame.",
         '''import pandas as pd
import numpy as np

n = 100_000
df = pd.DataFrame({
    "city": ["pune", "delhi", "goa", "mumbai"] * (n // 4),
    "count": np.random.default_rng(0).integers(0, 100, n),
})
before = df.memory_usage(deep=True).sum()

df["city"] = df["city"].astype("category")
df["count"] = pd.to_numeric(df["count"], downcast="unsigned")
after = df.memory_usage(deep=True).sum()

print("before : %7.1f KB" % (before / 1e3))
print("after  : %7.1f KB" % (after / 1e3))
print("saved  : %.0f%%" % (100 * (1 - after / before)))
print()
print("dtypes:", dict(df.dtypes.astype(str)))'''),

        ("Filter before you work",
         "Every operation costs in proportion to the rows it touches.",
         '''import pandas as pd
import numpy as np
import time

n = 200_000
rng = np.random.default_rng(0)
df = pd.DataFrame({"keep": rng.random(n) < 0.05, "v": rng.random(n)})

t = time.perf_counter()
a = df.assign(x=df["v"] * 2)[df["keep"]]
late = time.perf_counter() - t

t = time.perf_counter()
sub = df[df["keep"]]
b = sub.assign(x=sub["v"] * 2)
early = time.perf_counter() - t

print("compute then filter : %.4f s" % late)
print("filter then compute : %.4f s" % early)
print("rows kept           : %d of %d" % (len(b), n))
print()
print("Obvious, and routinely done the wrong way round because the")
print("filter reads more naturally at the end of a chain.")'''),

        ("Chained operations each copy",
         "Convenience has a price you can measure.",
         '''import pandas as pd
import numpy as np
import time

n = 200_000
df = pd.DataFrame({"a": np.arange(n, dtype="float64")})

t = time.perf_counter()
out = (df.assign(b=lambda d: d["a"] * 2)
         .assign(c=lambda d: d["b"] + 1)
         .assign(d=lambda d: d["c"] / 3))
chained = time.perf_counter() - t

t = time.perf_counter()
df2 = df.copy()
df2["b"] = df2["a"] * 2
df2["c"] = df2["b"] + 1
df2["d"] = df2["c"] / 3
inplace = time.perf_counter() - t

print("three chained assigns : %.4f s" % chained)
print("three direct assigns  : %.4f s" % inplace)
print("same result           :", np.allclose(out["d"], df2["d"]))
print()
print("Chaining is usually worth its cost for readability. Worth")
print("knowing the cost exists before optimising something else.")'''),

        ("Measure before changing anything",
         "The bottleneck is rarely where it feels like it is.",
         '''import pandas as pd
import numpy as np
import time

n = 100_000
rng = np.random.default_rng(0)
df = pd.DataFrame({
    "k": rng.integers(0, 500, n),
    "t": ["value-%d" % i for i in range(n)],
    "v": rng.random(n),
})

def timed(label, fn):
    t = time.perf_counter(); fn(); d = time.perf_counter() - t
    print("%-22s %.4f s" % (label, d)); return d

a = timed("groupby sum", lambda: df.groupby("k")["v"].sum())
b = timed("sort_values", lambda: df.sort_values("v"))
c = timed("str.upper", lambda: df["t"].str.upper())
d = timed("column arithmetic", lambda: df["v"] * 2)
print()
print("Slowest here: %s" % max([("groupby", a), ("sort", b),
                                ("str", c), ("arith", d)],
                               key=lambda p: p[1])[0])
print("Optimising the arithmetic would have gained nothing.")'''),
    ],
    [
        "<strong>Per-row Python</strong> is nearly always the whole story &mdash; <code>apply(axis=1)</code> is orders of magnitude slower than column arithmetic.",
        "<code>iterrows</code> is the one to never use: it is far slower than <code>itertuples</code> and converts each row to an <code>object</code> Series, losing dtypes.",
        "<code>category</code> for repeated text and <code>to_numeric(downcast=...)</code> for narrow numbers are the cheapest memory wins.",
        "<strong>Filter before you compute</strong> &mdash; every operation costs in proportion to the rows it touches.",
        "Each chained <code>assign</code> copies. Usually worth it for readability, but the cost is real.",
        "<strong>Measure first.</strong> The bottleneck is rarely where it feels like it is, and optimising a fast operation gains nothing.",
    ],
    '''
title: Performance
intro: Where the time actually goes, in the order worth fixing it.

## The order to work in

Pandas performance work is unusually predictable. In descending order of payoff:

1. **Remove per-row Python.** Worth 10&ndash;100x, and it is nearly always the whole problem.
2. **Right-size the dtypes.** Halves or better on memory, and speeds up everything that touches the column.
3. **Filter early.** Free, and often the largest structural win.
4. **Reduce copies.** Worth a modest amount, and only in hot paths.
5. **Reach past pandas.** When the data or the algorithm genuinely does not suit it.

Working down that list in order means the large wins come first. Working up it means spending an afternoon on step 4 while a `apply(axis=1)` sits untouched.

## Per-row Python

`df.apply(func, axis=1)`, `iterrows`, and a `for` loop over rows all do the same thing: call back into the interpreter once per row.

The first editor measures four spellings of the same multiplication. The vectorised form is orders of magnitude faster than `apply(axis=1)`, and interestingly a plain `zip` over two columns beats `apply` comfortably &mdash; because `apply` also builds a Series object per row.

The practical rule: if a lambda indexes into a row, the operation is column arithmetic in disguise.

## iterrows

Worth singling out because it is common and there is no situation where it is the right choice.

It is much slower than `itertuples`, and it **converts each row to a Series**. A row containing an integer and a string becomes an `object` Series, so the integer arrives as an object. Code that then does arithmetic on it is slower again, and code that checks types breaks.

`itertuples` is faster and preserves dtypes. If you must iterate, use that. Better still, do not iterate.

## dtypes

Covered in its own module, and it belongs here too because memory and speed are the same problem: less data to move is less time spent moving it.

`category` for repeated text is the biggest single win on most real frames, and it speeds up group-by and comparison as well as saving memory. `to_numeric(downcast=...)` narrows numeric columns.

The third editor shows both applied to one frame.

## Filter early

Every operation costs in proportion to the rows it touches. Filtering to 5% of the data before computing means every later step does 5% of the work.

This is obvious stated plainly and routinely done backwards, because a filter reads more naturally at the end of a chain than in the middle of one. `df.assign(...).query(...)` computes for every row and then throws most of them away; `df.query(...).assign(...)` does not.

The same applies to columns: `usecols` at read time, and dropping columns you will not use, both reduce everything downstream.

## Copies

Most pandas operations return a new object. A chain of three `assign` calls allocates three frames.

That is usually the right trade &mdash; the chain is readable, does not mutate anything, and works well in a notebook. The cost only matters inside a loop or on a frame large enough that allocation dominates.

Two things to know rather than to apply everywhere: direct assignment (`df["b"] = ...`) modifies in place and skips the copy, and `inplace=True` on other methods generally does **not** avoid a copy despite its name, while breaking chaining and returning `None`. It is not the optimisation it appears to be.

## Measure

The last editor times four operations on the same frame. The ranking is not what most people would guess, and it changes with the data.

`%timeit` in a notebook, or `time.perf_counter` around a block, is enough for most decisions. Take the best of several runs rather than the mean, since the slow runs are measuring the machine.

Two rules that save the most wasted effort:

**Profile the real workload.** A small sample has different characteristics &mdash; different memory pressure, different cache behaviour, sometimes a different code path.

**Fix the top item and measure again.** The bottleneck moves, and the second item on the original list is often no longer second.

And keep the ceiling in view: an operation taking 5% of the runtime cannot give back more than 5%, however cleverly it is rewritten.

## When to leave pandas

pandas assumes the data fits in memory on one machine, and it is optimised for convenience rather than raw speed.

**Polars** is much faster on large joins and aggregations, with a similar model and a lazy engine.

**DuckDB** runs SQL over frames and files, and is excellent for analytical queries larger than memory.

**Dask** partitions frames across cores or machines with a pandas-like API.

**NumPy** directly, when the data is homogeneous and you do not need labels.

The signal that it is time is usually memory rather than speed: when a frame no longer fits, no amount of optimisation inside pandas fixes it.

## Profiling a pandas script

`%timeit` in a notebook and `time.perf_counter` around a block cover most decisions.

For a whole script, `cProfile` finds the hot function and `line_profiler` finds the line inside it. Array code often has one line taking most of the time, which line-level profiling shows immediately and function-level profiling hides.

`df.info(memory_usage="deep")` and `memory_profiler` cover the memory side.

Two rules save the most wasted effort. Profile the **real** workload, because a small sample has different cache behaviour and sometimes takes a different code path. And re-profile after each fix, because the bottleneck moves.

## Reducing before combining

The largest structural wins usually come from doing less work rather than doing the same work faster.

**Read fewer columns** &mdash; `usecols` at read time.

**Read fewer rows** &mdash; filter during the chunk loop rather than after.

**Aggregate before joining** &mdash; joining two summaries is far cheaper than joining raw tables and summarising afterwards.

**Select columns before merging** &mdash; carrying twenty unused columns through a join costs memory and time.

Each of these changes the size of what everything downstream touches, which compounds through a pipeline in a way that micro-optimisation does not.

## Categoricals as an optimisation

Converting a repeated string column to `category` helps in four places at once:

Memory, often by an order of magnitude.

Group-by, which then operates on integer codes.

Merge, when both sides share the same categories.

`.str` operations, which apply to the categories rather than to every row.

That last one is worth restating: `df["city"].str.upper()` on a million rows with four distinct cities does four operations when the column is categorical, and a million when it is `object`.

The cost is the conversion itself and the care needed when combining frames with different category sets.

## Avoiding repeated work

Two patterns that quietly dominate slow scripts:

**Recomputing inside a loop.** A group statistic, a lookup table, a parsed date &mdash; computed once outside the loop rather than once per iteration.

**Repeated boolean masks.** Building the same mask several times to select different columns. Build it once, name it, reuse it.

Both are ordinary programming discipline rather than anything pandas-specific, and both are easy to miss because each individual line looks cheap.

## The limits

pandas is single-threaded for most operations, holds everything in memory, and is optimised for convenience.

A rough guide to when to look elsewhere:

**Under a million rows** &mdash; pandas is comfortable; optimisation is rarely needed beyond removing loops.

**One to ten million** &mdash; dtypes and access patterns start to matter, and the techniques in this module earn their keep.

**Over ten million, or wider than memory** &mdash; the constraint is usually memory rather than speed, and Polars, DuckDB or Dask are the answer rather than a cleverer pandas expression.

**Genuinely sequential algorithms** &mdash; Numba or a rewrite, at any size.

Recognising which regime you are in prevents both premature optimisation and the opposite mistake of spending days making pandas do something it structurally cannot.

## A short checklist

Is there a loop over rows? Remove it.

Is anything growing in a loop? Collect and combine once.

Are the dtypes right? Categories for repeated text, narrow numerics where bounded.

Is the filter as early as it can be?

Have you measured, or are you guessing?

The first two account for most real slowdowns, and neither requires knowing anything about pandas internals.

## A worked speed-up

A slow script usually has one dominant problem, and the sequence for finding it is always the same.

Time the whole thing. Time each stage. Find the stage taking most of it. Look at what that stage does per row.

The fixes, in the order they usually apply:

A row-wise `apply` becomes column arithmetic or `np.select`.

A loop building a frame becomes a list and one `concat`.

A merge inside a loop becomes one merge outside it.

A repeated group statistic becomes one `transform`.

An `object` column that should be a category becomes one.

A filter at the end moves to the beginning.

Each of those is a small edit with a large effect, and together they account for most of the difference between a script that takes minutes and one that takes seconds.

## Memory, when the frame will not fit

The techniques differ from the speed ones, because the constraint is different.

`usecols` at read time &mdash; never load what you will not use.

`dtype` at read time &mdash; categories and narrow numerics.

`chunksize` &mdash; process and reduce a piece at a time.

`del` and `gc.collect()` &mdash; release intermediates explicitly in a long-running process.

Avoid keeping both a frame and a transformed copy alive; reassign rather than naming a new variable, when the old one is not needed.

And check whether the operation needs the whole frame at all. Many aggregations can be computed chunk-wise and combined.

## What not to optimise

Some things are already fast and are commonly rewritten for no gain:

**Column arithmetic** &mdash; already compiled.

**Boolean masking** &mdash; already compiled; the cost is the copy, not the comparison.

**`groupby` with a string aggregation** &mdash; already compiled.

**Reading a small file** &mdash; measured in milliseconds.

**Anything running once on a small frame.**

Rewriting these produces less readable code and no measurable improvement, which is a bad trade. The measurement step exists to prevent exactly that.

## A summary

Remove per-row Python first; it is usually the whole problem.

Never grow a frame in a loop.

Right-size dtypes &mdash; categories and narrow numerics.

Filter early, so everything downstream does less.

`itertuples` if you must iterate; never `iterrows`.

`inplace=True` is not an optimisation.

Measure the real workload, fix the top item, measure again.

And know when the answer is a different tool &mdash; when the data does not fit, no pandas technique fixes it.

## A closing note

Pandas performance is unusually predictable, which makes it unusually easy to get right.

Almost every slow script has the same cause: Python running once per row, spelled as `apply(axis=1)`, `iterrows`, or a loop. Removing it is worth one or two orders of magnitude, and nothing else on the list comes close.

After that the wins are structural rather than clever &mdash; do not grow frames in loops, filter before computing rather than after, and give columns types that fit the data. None of these require knowing anything about pandas internals.

What does require discipline is measuring. The bottleneck is regularly not where it feels like it is, and the operations people most often rewrite &mdash; column arithmetic, boolean masks, group-by with a string aggregation &mdash; are already compiled and already fast.

And there is a ceiling. When the data no longer fits in memory, no pandas technique fixes it, and the answer is Polars, DuckDB, Dask or a database.
''',
    [
        {"q": "What is nearly always the largest performance problem in a pandas script?",
         "options": ["Reading files", "Per-row Python - apply(axis=1), iterrows, or a loop over rows", "Sorting", "Memory fragmentation"],
         "answer": 1,
         "why": "If a lambda indexes into a row, the operation is column arithmetic in disguise. This is worth 10-100x, ahead of everything else."},
        {"q": "Why is `iterrows` never the right choice?",
         "options": ["It is deprecated", "It is far slower than itertuples and converts each row to an object Series, losing dtypes", "It skips rows", "It only works on numeric data"],
         "answer": 1,
         "why": "A row with an int and a string becomes object, so the integer arrives as an object. If you must iterate, use itertuples."},
        {"q": "Why does `df.query(...).assign(...)` usually beat `df.assign(...).query(...)`?",
         "options": ["query is faster", "Filtering first means the computation touches far fewer rows", "assign is deprecated", "They are identical"],
         "answer": 1,
         "why": "Obvious stated plainly and routinely done backwards, because a filter reads more naturally at the end of a chain."},
        {"q": "Does `inplace=True` avoid a copy?",
         "options": ["Yes, always", "Generally no - it also breaks chaining and returns None", "Only for drop", "Only on Series"],
         "answer": 1,
         "why": "It is not the optimisation it appears to be. Direct assignment df['b'] = ... does modify in place and skips the copy."},
    ],
)


# ---------------------------------------------------------------------------
# 26. Method chaining
# ---------------------------------------------------------------------------
topic(
    "method_chaining",
    "Method Chaining",
    "Working with Data",
    "Writing a pipeline as one expression - what it buys, and where to stop.",
    _svg(_box(16, 34, 26, 22, S) + _arrow(44, 45, 56, 45) +
         _box(58, 34, 26, 22, S) + _arrow(86, 45, 98, 45) +
         _box(100, 34, 26, 22, S, A) +
         _txt(70, 74, "one expression", M, 8)),
    [
        ("The same work, two ways",
         "Intermediate names against one expression.",
         '''import pandas as pd

df = pd.DataFrame({
    "city": ["pune", "delhi", "pune", "goa"],
    "sales": [10, 20, 30, 5],
    "year": [2024, 2024, 2023, 2024],
})

# step by step
tmp = df[df["year"] == 2024]
tmp = tmp.assign(doubled=tmp["sales"] * 2)
stepwise = tmp.groupby("city", as_index=False)["doubled"].sum()

# chained
chained = (df
           .query("year == 2024")
           .assign(doubled=lambda d: d["sales"] * 2)
           .groupby("city", as_index=False)["doubled"].sum())

print(chained)
print()
print("identical:", stepwise.equals(chained))
print()
print("No tmp, no tmp2, and no chance of using a stale one.")'''),

        ("lambda is what makes assign chain",
         "It sees the frame at that point, not the one you started with.",
         '''import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3]})

out = (df
       .assign(b=lambda d: d["a"] * 10)
       .assign(c=lambda d: d["b"] + 1))
print(out)
print()
print("the second assign used the column the first one made.")
print()
print("without the lambda it would have to exist already:")
try:
    df.assign(b=df["a"] * 10, c=df["b"] + 1)
except KeyError as e:
    print("   KeyError:", e)'''),

        ("pipe puts your own function in the chain",
         "For steps that are not a pandas method.",
         '''import pandas as pd

def drop_small(d, threshold):
    return d[d["sales"] >= threshold]

def add_share(d):
    return d.assign(share=(d["sales"] / d["sales"].sum() * 100).round(1))

df = pd.DataFrame({"city": ["pune", "delhi", "goa"], "sales": [30, 20, 5]})

out = (df
       .pipe(drop_small, threshold=10)
       .pipe(add_share))
print(out)
print()
print("pipe(f, args) is just f(df, args), written so it reads in order.")
print("Without it the chain has to be turned inside out: add_share(drop_small(df, 10))")'''),

        ("Debugging a chain",
         "The usual objection, and the usual answer.",
         '''import pandas as pd

df = pd.DataFrame({"city": ["pune", "delhi"], "sales": [30, 20]})

def show(d, label):
    print("%-10s shape %s cols %s" % (label, d.shape, list(d.columns)))
    return d

out = (df
       .pipe(show, "start")
       .assign(doubled=lambda d: d["sales"] * 2)
       .pipe(show, "after assign")
       .query("doubled > 40")
       .pipe(show, "after filter"))
print()
print(out)
print()
print("A pipe that prints and returns unchanged lets you see inside")
print("without breaking the chain apart.")'''),

        ("Where chaining stops helping",
         "Long chains hide where things went wrong.",
         '''import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

try:
    (df
     .assign(c=lambda d: d["a"] + d["b"])
     .assign(d=lambda d: d["c"] * 2)
     .assign(e=lambda d: d["typo"] + 1)
     .assign(f=lambda d: d["e"] / 2))
except KeyError as e:
    print("KeyError:", e)
print()
print("The traceback points at the chain, not at which link failed.")
print("Four steps is comfortable. Fifteen is a debugging problem, and")
print("breaking it into two named stages costs nothing.")'''),

        ("A realistic pipeline",
         "Load, clean, aggregate - as one readable expression.",
         '''import pandas as pd
import io

csv = """city,plan,amount
 Pune ,free,10
delhi,paid,20
PUNE,paid,30
goa,free,
"""
out = (pd.read_csv(io.StringIO(csv))
       .assign(city=lambda d: d["city"].str.strip().str.lower())
       .dropna(subset=["amount"])
       .astype({"amount": "int64"})
       .groupby(["city", "plan"], as_index=False)["amount"].sum()
       .sort_values("amount", ascending=False)
       .reset_index(drop=True))
print(out)
print()
print("Six steps, no intermediate names, and each line is one idea.")'''),
    ],
    [
        "Chaining removes intermediate names, and with them the chance of using a stale one.",
        "<code>assign</code> takes a <strong>lambda</strong> so it can see the frame at that point in the chain, including columns earlier steps created.",
        "<code>pipe(f, args)</code> is just <code>f(df, args)</code>, written so a custom step reads in order rather than inside out.",
        "A <code>pipe</code> that prints and returns unchanged lets you inspect a chain without taking it apart.",
        "Long chains hide <em>which</em> link failed &mdash; four steps is comfortable, fifteen is a debugging problem.",
        "The pattern suits load-clean-aggregate work, where each line is one idea and nothing is mutated.",
    ],
    '''
title: Method Chaining
intro: Writing a pipeline as one expression.

## What it buys

Most pandas methods return a new object, which means they compose:

```python
out = (df
       .query("year == 2024")
       .assign(doubled=lambda d: d["sales"] * 2)
       .groupby("city", as_index=False)["doubled"].sum())
```

Three things follow, and they are the actual argument for the style.

**No intermediate names.** The `tmp`, `tmp2`, `df_clean`, `df_clean2` sequence is where stale-variable bugs live &mdash; particularly in a notebook where cells run out of order, and `df` is no longer what the cell above assumed.

**Nothing is mutated.** The original frame is untouched, so re-running a cell gives the same answer. That alone removes a large class of notebook confusion.

**Each line is one operation.** The chain reads top to bottom in the order the work happens, which nested function calls do not.

The wrapping parentheses are what allow the line breaks. Without them the expression has to fit on one line or carry backslashes.

## assign and the lambda

`assign` is what makes computation chainable, and the lambda is what makes `assign` work mid-chain.

`d.assign(b=d["a"] * 10)` computes against the frame **as it was before the chain started**. Inside a chain that is usually wrong, and if the column it needs was created two steps earlier it raises `KeyError`.

`d.assign(b=lambda d: d["a"] * 10)` receives the frame **at that point**, so it sees everything earlier steps produced.

Use the lambda form by default in a chain. It costs eight characters and removes the class of error entirely.

## pipe

Not every step is a pandas method. `pipe` inserts your own function without breaking the chain:

```python
df.pipe(drop_small, threshold=10).pipe(add_share)
```

`df.pipe(f, x)` is exactly `f(df, x)`. The gain is order: the nested form, `add_share(drop_small(df, 10))`, reads inside out and gets worse with every step.

For this to work, your functions should take a frame as the first argument and return a frame. That is a good shape for them anyway &mdash; it makes them testable in isolation.

## Debugging

The standard objection to chaining is that you cannot see what is happening in the middle, and cannot set a breakpoint on a step.

The answer is a pipe that inspects and returns unchanged:

```python
def show(d, label):
    print(label, d.shape, list(d.columns))
    return d
```

Dropped into the chain, it prints the shape at each stage without changing the result. Most chain bugs are a shape or a column name, and that catches both.

For a heavier version, log `d.head()` or write the intermediate to a file. The principle is the same: a function that returns its input can go anywhere in a chain.

## Where to stop

Chaining is a style, not a virtue, and it stops paying at some length.

**The traceback problem.** When a fifteen-step chain raises `KeyError: 'typo'`, the traceback points at the whole expression. You know it failed; you do not immediately know where. The last-but-one editor shows this.

**The reading problem.** A chain is one expression, so it has to be understood as a whole. Past a certain length that is harder than reading five named steps.

**The reuse problem.** An intermediate result needed twice has to be computed twice, or the chain has to be broken anyway.

A workable rule: chain a coherent stage &mdash; loading and cleaning, or aggregating and formatting &mdash; and give each stage a name.

```python
clean = (raw.pipe(normalise_columns).dropna(subset=["id"]))
summary = (clean.groupby("city").agg(...).sort_values("total"))
```

Two names instead of ten, and each chain is short enough to debug.

## Where it fits

The style suits **load, clean, aggregate** work particularly well, because that work is naturally a sequence of transformations with no branching.

It suits exploratory notebook work, because immutability makes re-running cells safe.

It suits less well anything with branching logic, loops, or steps whose output feeds two different places &mdash; at which point named intermediates are simply clearer, and there is nothing wrong with using them.

## Which methods chain

Anything returning a DataFrame or Series can be chained, which is most of the API:

Selection &mdash; `query`, `loc` with a callable, `filter`, `head`, `sample`, `nlargest`.

Modification &mdash; `assign`, `rename`, `drop`, `astype`, `fillna`, `replace`, `round`.

Reshaping &mdash; `sort_values`, `set_index`, `reset_index`, `melt`, `pivot`, `stack`, `unstack`, `explode`.

Aggregation &mdash; `groupby(...).agg(...)`, `value_counts`, `describe`.

Anything else &mdash; `pipe`.

The methods that break a chain are the ones returning `None`: anything with `inplace=True`, and `sort` / `shuffle`-style in-place methods. That is one more reason to avoid `inplace`.

## Naming the stages

The practical shape for a real script is a few named stages rather than one long chain:

```python
raw = pd.read_csv(path, dtype=..., parse_dates=[...])

clean = (raw
         .pipe(normalise_columns)
         .dropna(subset=["id"])
         .astype({"id": "string"}))

summary = (clean
           .query("year == 2024")
           .groupby("city", as_index=False)
           .agg(total=("sales", "sum")))
```

Each stage is short enough to debug, each name says what the data is at that point, and the intermediates are available for inspection without breaking anything apart.

That structure also tests well: `normalise_columns` and each stage can be checked independently.

## Chaining and memory

Each step in a chain allocates. A ten-step chain on a large frame allocates ten frames, though earlier ones are freed as it proceeds, so peak memory is roughly two at a time rather than ten.

That is acceptable for most work and worth knowing when the frame is large enough that a single copy is significant.

Filtering early in the chain reduces every allocation after it, which is the same advice as everywhere else and matters more here because there are more of them.

## Common chaining mistakes

**Forgetting the lambda in `assign`.** The expression is then evaluated against the pre-chain frame, and raises if it needs a column made mid-chain.

**Using `inplace=True` in a chain.** Returns `None`, and the next method raises `AttributeError` on `NoneType`.

**Assuming the index survives.** `reset_index(drop=True)` at the point it matters, not at the end.

**A chain that is really two operations.** If an intermediate is needed twice, the chain has to compute it twice or be broken. Break it.

**Debugging by deleting lines.** Better to insert a `pipe` that prints, which does not change the structure.

## When not to chain

Chaining suits linear transformation. It does not suit:

**Branching** &mdash; different handling depending on a condition.

**Loops** &mdash; over files, groups or parameters.

**Reuse** &mdash; an intermediate needed by two downstream steps.

**Error handling** &mdash; a try/except around one step.

In all four cases, named intermediates are clearer, and reaching for a chain anyway produces code that is harder to read than the thing it replaced.

The style is a tool for the common case of "load, clean, aggregate, output", where it genuinely reads better than the alternative. It is not a standard to hold all code to.

## A realistic shape for a script

Chaining works best as a few named stages rather than one long expression or a hundred separate statements:

```python
def load(path):
    return pd.read_csv(path, dtype=DTYPES, parse_dates=["date"])

def clean(d):
    return (d
            .rename(columns=str.lower)
            .dropna(subset=["id"])
            .assign(city=lambda x: x["city"].str.strip().str.lower())
            .drop_duplicates(subset=["id"], keep="last"))

def summarise(d):
    return (d
            .query("date >= @CUTOFF")
            .groupby("city", as_index=False)
            .agg(total=("sales", "sum"), orders=("sales", "size"))
            .sort_values("total", ascending=False))

result = summarise(clean(load(path)))
```

Each function is testable on its own, each chain is short enough to debug, and the top-level line reads as what the script does.

`load(path).pipe(clean).pipe(summarise)` expresses the same thing in chain form, which reads in order rather than inside out.

## Chaining and notebooks

The style suits notebooks particularly well, for a reason worth stating: cells get re-run, out of order, repeatedly.

A chain does not mutate its input, so re-running a cell gives the same result. A sequence of in-place modifications does not &mdash; running it twice applies the transformation twice, and the frame is now wrong in a way nothing indicates.

That failure is common enough that "restart and run all" is standard advice. Chaining removes most of the need for it.

## Readability in practice

A few conventions make chains easier to read:

One operation per line.

Wrapping parentheses, so no backslashes are needed.

A blank line between logical stages within a long chain.

`pipe` for anything that is not a pandas method, rather than breaking out.

Names for intermediates at genuine stage boundaries.

And a limit: if you cannot see the whole chain on one screen, split it. The point of the style is clarity, and a chain that has to be scrolled has stopped providing it.

## A summary

Chaining removes intermediate names and the stale-variable bugs that come with them.

Nothing is mutated, so re-running is safe.

`assign` needs a lambda to see the frame mid-chain.

`pipe` inserts your own functions in reading order.

A `pipe` that prints and returns its input lets you debug without breaking the chain.

Long chains hide which link failed &mdash; name coherent stages instead.

And it is a style for linear transformation, not a rule for all code; branching, loops and reuse are clearer with names.

## A closing note

Method chaining is one of the few stylistic choices in pandas that changes how many bugs you write rather than merely how the code looks.

The mechanism is not elegance. It is that intermediate names are where stale state lives: `df_clean` that was cleaned by an earlier version of the cell above, `tmp2` that is a filtered copy of `tmp` from before the filter changed. A chain has nowhere for that to hide.

The immutability matters for the same reason. Code that does not modify its input produces the same answer on the second run as the first, which is the property notebooks most often lack.

Against that, a chain is one expression, and one expression fails as a unit. The balance is struck by keeping chains to a coherent stage and giving each stage a name &mdash; which is ordinary good structure, applied to data transformation.

## Two more things worth knowing

`pipe` has a second form for functions whose frame argument is not first: `df.pipe((func, "data"), other_arg)` tells pandas which parameter receives the frame. It is rarely needed, and it exists so that third-party functions with awkward signatures can still be chained.

`assign` accepts plain values as well as lambdas, and mixing the two in one call is legal. The rule is that a plain value is evaluated once, against the frame as it was before the chain started, so a plain value referring to a column made mid-chain will fail. Using lambdas uniformly avoids having to hold that distinction in mind.

Finally, chains and comments coexist badly &mdash; there is no natural place to explain a step. That is a real argument for named stages: a function name is a comment that cannot drift out of date.

## Chaining and testing

One practical benefit of the named-stage structure is that it makes a pipeline testable without any test framework ceremony.

Each stage takes a frame and returns a frame, so each can be checked on a small hand-built input:

```python
def test_clean():
    raw = pd.DataFrame({"ID": [1, 1, None], "City": [" Pune ", "pune", "goa"]})
    out = clean(raw)
    assert len(out) == 1
    assert list(out["city"]) == ["pune"]
```

That is a genuine unit test of a data transformation, and it is possible only because `clean` is a function rather than a sequence of statements operating on a global `df`.

The same structure makes the pipeline reusable across scripts and notebooks, and makes it obvious where a new step belongs. Chaining, in this reading, is less about elegance than about pushing data transformations into functions that can be named, tested and reused &mdash; which is ordinary software practice arriving somewhere it is often skipped.

## In summary

Chaining is a style that suits linear transformation, which is most of what data cleaning is.

It removes intermediate names and the stale-state bugs that live in them, it does not mutate its input so re-running is safe, and it reads in the order the work happens.

Its costs are real: a failure points at the whole expression, an intermediate needed twice forces a break, and branching or looping does not fit at all.

The resolution is named stages of a handful of steps each, which keeps the benefits and makes each stage short enough to debug and small enough to test.
''',
    [
        {"q": "Why does `assign` take a lambda inside a chain?",
         "options": ["Style", "So it sees the frame at that point, including columns earlier steps created", "For speed", "It is required syntax"],
         "answer": 1,
         "why": "Without the lambda the expression is computed against the frame as it was before the chain started, which raises KeyError for a column made two steps earlier."},
        {"q": "What is `df.pipe(f, x)` equivalent to?",
         "options": ["f(x, df)", "f(df, x)", "df.apply(f)", "df.map(f)"],
         "answer": 1,
         "why": "The gain is reading order - the nested form add_share(drop_small(df, 10)) reads inside out and gets worse with every step."},
        {"q": "How do you inspect the middle of a chain without breaking it apart?",
         "options": ["You cannot", "A pipe to a function that prints and returns its input unchanged", "print inside assign", "Split it always"],
         "answer": 1,
         "why": "Most chain bugs are a shape or a column name, and printing d.shape and d.columns at each stage catches both."},
        {"q": "What is the main practical cost of a very long chain?",
         "options": ["Speed", "A traceback points at the whole expression rather than the link that failed", "Memory", "It mutates the original"],
         "answer": 1,
         "why": "Chain a coherent stage and give it a name. Two named stages of five steps are far easier to debug than one of fifteen."},
    ],
)
