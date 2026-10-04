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
intro: Columns with names, types and an index. Why that differs from a 2-D array.

## Two structures

`Series` is a one-dimensional array of values **plus an index** of labels.

`DataFrame` is a set of Series sharing one index. Each column has its own dtype.

That second point is the hands-on gap from NumPy. A NumPy array has one dtype for the whole block. A DataFrame has one per column. A table with a name, an age, a score and a flag is four dtypes. That is just the shape real data arrives in.

Convert such a DataFrame to a NumPy array and each column merges to the one type that can hold all of them. Often `object`. This Is a list of pointers with extra steps. That collapse is worth seeing once. It shows why pandas exists rather than all using arrays.

## The index does work you did not ask for

The index looks like row numbers. By default it's `0, 1, 2`. That default hides what it really is. A labelled axis that participates in almost each step.

Two results arrive early and confuse people.

**It lives filtering.** Filter a Series down to two of five rows and the index reads `1, 4`, not `0, 1`. The labels came along. Code that then indexes positionally gets the wrong rows or a `KeyError`.

**Math aligns on it.** Adding two Series matches them up **by label**, not by spot. If the labels are in other orders, pandas reorders for you. If one has a label the other lacks, the result is `NaN` there rather than an error.

That alignment is a genuine feature. It's what makes mixing data from other sources safe. Mismatches surface as NaN rather than as a silent off-by-one. It's also the single most surprising action for anyone arriving from NumPy. Here `+` is strictly spot-based.

The index gets a module of its own next. Nearly each pandas confusion traces back to it.

## Names instead of positions

`df["salary"]` says what it selects. `arr[:, 3]` needs you to note what column 3 was. Breaks silently when a column is inserted.

That isn't a small ergonomic point. It's most of why pandas code lives contact with changing data. Why a group-by is one line rather than a dict, a loop and a choice about missing keys.

## When to use something else

**Plain Python** for small, one-off, non-tabular work. A hundred records processed once doesn't justify the import. A list of dicts is easier to read.

**NumPy** when the data is truly homogeneous and numeric. A mat, an image, a signal. pandas adds per-column bookkeeping you aren't using. Costs both memory and speed for it.

**A DB** when the data doesn't fit in memory, or when a few processes need it at once. pandas assumes one process and one machine.

**Polars or DuckDB** when the data is large and the work is analytical. Both are a lot faster than pandas on big joins and aggregations.

pandas is the right tool for tabular, in-memory, mixed-type data where the questions are column-shaped. Which shows an huge amount of real work.

## The one performance rule

pandas is a thin, convenient layer over compiled code. It's fast while the work happens inside that compiled layer. Slow the moment it has to call back into Python once per row.

`apply`, `iterrows` and a `for` loop over rows all do just that. The last editor measures it. The gap is large enough that it's often the whole speed story of a pandas script.

The rule: express steps on **whole columns**. `df["a"] * 2` operates on the column. `df["a"].apply(lambda v: v * 2)` operates on each value from Python and is far slower for the same result.

There are cases where `apply` is unavoidable. A module later covers them. Most uses of it aren't those cases.

## How this track is organised

The index and pick come first. They cause the most confusion and all else depends on them. Including the copy warning. This Gets a module to itself because nothing else in pandas wastes as much of people's time.

Then cleaning: missing values, copies, strings, types.

Then the aggregation work that is the reason to use pandas at all: group-by, joins, reshaping.

Then time series, reading and writing files, and speed.

each module is short runnable programs rather than one long script. You can change one line and see which rule made which output.

## Where pandas sits

pandas is built **on** NumPy. Underneath each numeric column is a NumPy array. The math that runs on a column is the same compiled code.

What pandas adds is bookkeeping: labels for the rows, names and split types for the columns. A large library of steps that assume your data is a table rather than a mat.

That layering shows both its strengths and its costs. Column math is fast because NumPy is doing it. Anything that has to consult labels, merge dtypes, or fall back to Python objects is slower. That is where pandas code goes wrong.

Above pandas sit the tools that consume it. Scikit-learn takes DataFrames, matplotlib and seaborn plot them. Most data pipelines pass them around. Knowing the layer below and the layer above tells you when to drop down to NumPy for speed and when to hand off fully.

## The vocabulary

A few terms recur constantly, and being precise about them blocks confusion later.

**Series** &mdash; one column: values plus an index, with a single dtype.

**DataFrame** &mdash; a few Series sharing one index.

**Index** &mdash; the labels for the rows. The column names are also an Index.

**dtype** &mdash; the type of one column. `object` often means Python strings.

**Axis** &mdash; `axis=0` is rows, `axis=1` is columns. As in NumPy, the axis you name is often the one being merged or moved along. This Is why `df.sum(axis=0)` gives a total per column.

**NaN / NaT / pd.NA**. Missing markers for floats, datetimes and the nullable types.

## Reading pandas output

Printed output carries more data than it appears to. Reading it saves a great many print statements.

The **dtype line** under a Series tells you what you're holding. `int64` and `float64` are numeric. `object` almost always means strings. `datetime64[ns]` means dates have been parsed.

The **index** is the left-hand column. It isn't row numbers. If it reads `0, 3, 7` rather than `0, 1, 2`, the frame has been filtered and the first labels came along.

`Name:` under a Series gives the column it came from.

`[5 rows x 3 columns]` at the bottom of a truncated frame is the real shape. This Matters when the display has elided the middle.

Three things worth setting in a notebook: `pd.set_option("display.max_columns", None)` to stop columns being hidden, `display.width` to control wrapping. `display.float_format` to stop long decimals dominating a table.

## A first session

The shape of almost each piece of pandas work is the same:

**Load** with `read_csv`, saying what you know about types and dates.

**Look** &mdash; `shape`, `dtypes`, `head`, `info`, `show`, and `value_counts` on the cat columns.

**Clean** &mdash; fix types, handle missing values, norm text, drop or aggregate copies.

**Reshape** &mdash; filter to what matters, join in what is missing, group and aggregate.

**Output** &mdash; a table, a chart, or a file.

Roughly half of real work is in the middle two steps. This Is why this track spends most of its modules there rather than on the aggregation all thinks of as the notable part.

## Two habits worth starting with

**Check after each step that changes the shape.** `len(df)` after a filter or a merge, `df.dtypes` after a load or a concat. Most pandas bugs are silent. The ones that aren't silent are often caught by one of those two lines.

**Prefer clear over clever.** `df.loc[mask, "col"]` over `df[mask]["col"]`, named aggregation over spot-based, `.copy()` where you mean a copy. The clear form is nearly always the one that keeps working when the data changes.

## Questions that come up first

**Do I need to learn NumPy before pandas?**

Not before, but alongside. pandas hides NumPy most of the time. Then leaks it at just the moments that matter. Dtypes, NaN action, broadcasting, views versus copies. each one of those is a NumPy concept wearing a pandas name. The modules that cause the most trouble here are the ones where the NumPy layer shows through.

**Why is my column `object`?**

Because it holds Python objects rather than a uniform numeric type. Almost always strings, at times mixed types from a messy source. It's the single most common cause of both slow code and surprising results. `df.dtypes` is how you find it.

**Why did my ints become floats?**

A missing value. NumPy int arrays can't hold NaN. Pandas promotes the column. The nullable `Int64` type is the fix.

**Why does my filter return an empty frame?**

often a type mismatch &mdash; checking a string column against a number &mdash; or whitespace and case differences in the values. `value_counts()` on the column shows both at once.

**Should I use pandas or SQL?**

If the data lives in a DB and the step is a filter, join or aggregate, do it in SQL and bring back less data. pandas is for what happens after that. For data that never was in a DB.

## What this track assumes

That you can read Python, and that you've met lists and dicts. No statistics, no NumPy, and no prior pandas.

The modules are sorted by dependency rather than by glamour. The index, pick and the copy warning come first because all later depends on them and because they cause the most confusion. Cleaning comes next. That is where most real time goes. Group-by, joins and reshaping come after, because they're what people think pandas is for and they only work properly once the earlier material is in place.

Each module is six short programs and an article. The programs are the point. Changing a value and re-running is the fastest way to find out what a rule really does. A few of them are written so the output clashes with the guess most people would make.

## The shortest useful summary

A DataFrame is columns with names and types, sharing an index.

The index takes part in almost all, including alignment, which is silent.

Pick is `.loc` for labels and `.iloc` for spots.

set goes in one `.loc` call, or through an clear `.copy()`.

steps on whole columns are fast. Anything per row isn't.

And when a result surprises you, the answer is nearly always in `df.dtypes`, `df.shape`, or the index &mdash; in that order.

## A closing note

pandas is a large library, and the temptation is to learn it as a list of methods. That doesn't work well. The methods aren't the hard part.

The hard part is a small number of actions that run through all. The index takes part in steps you didn't ask it to. A column has one dtype and that dtype decides what is possible. Pick returns a thing whose link to the first isn't always given. And anything that runs Python once per row is slow enough to dominate.

Those four explain most of what surprises people, and each has a module here.

The methods, by contrast, are searchable. No one remembers the arg order of `merge` or the exact spelling of each rate alias, and no one needs to.

So the handy thing to take from this track isn't coverage but a set of instincts. Check `dtypes` after loading, check row counts after joining, know whether you're holding a copy. Stay out of per-row Python.
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
intro: The labelled axis that participates in almost each step.

## What it is

each Series and each DataFrame carries an index. An sorted set of labels, one per row. A DataFrame also has an index for its columns.

If you don't supply one, pandas creates a `RangeIndex` of `0, 1, 2, ...`. That default is why the index is easy to overlook. It looks like row numbers. For a freshly created frame it behaves like them.

It isn't row numbers. It's a labelled axis that takes part in pick, alignment, joining, grouping and reshaping. Nearly each pandas action that surprises people is the index doing a thing they didn't ask for.

## Labels stick to rows

Filter a Series of five values down to three and the surviving rows keep their first labels. The result's index might be `1, 3, 4`.

This is correct &mdash; the label finds the row. The row didn't change identity by being selected &mdash; but it breaks spot-based habits at once.

`big[0]` raises `KeyError`, because there's no label `0` any more. `big.iloc[0]` gets the first row by spot. `big.loc[1]` gets the row labelled 1.

Two results worth internalising.

**After filtering, use `iloc` for spot and `loc` for labels**. Know which you mean. The next module is fully about that gap.

**`reset_index(drop=True)` renumbers** when you truly want a fresh `0..n-1`. Without `drop=True`, the old index is kept as a new column. This Is at times what you want and often not.

## set_index and reset_index

`df.set_index("city")` makes the `city` column the index. Lookups by city then work with `.loc`, joins on city become index joins, and grouping by it's cheaper.

`df.reset_index()` reverses it, putting the index back as an plain column and restoring a `RangeIndex`.

Setting a real index is worth doing when you'll look rows up by that key again and again. It isn't worth doing reflexively. An index carries rules. A frame with a `RangeIndex` is simpler to reason about.

## Alignment

This is the action that most sets apart pandas from NumPy, and it's silent.

When two Series are mixed, pandas matches them **by label** before doing anything. Order doesn't matter. A label present in one and absent from the other makes `NaN` rather than an error.

For addition of two quarterly figures indexed by city, that is just right. You want Pune added to Pune, what order the rows arrived in. A city missing from one quarter should be visibly missing rather than silently paired with the wrong row.

It turns a problem when you didn't realise the indexes differed. A common version. You filter a frame, find a column from it. Assign that column back to the first frame. Alignment matches on the filtered labels. The rows you filtered out get `NaN`. Which is arguably the right answer, and is rarely what the author expected.

`.values` or `.to_numpy()` strips the index and forces spot-based action. That is at times the right escape hatch. It silences the safety feature. It deserves a comment when used.

The math methods take `fill_value`: `q1.add(q2, fill_value=0)` treats a missing label as zero rather than passing NaN.

## Duplicates

An index may hold the same label more than once. pandas doesn't prevent it.

The result is that `s["a"]` returns a **scalar** when `a` appears once and a **Series** when it appears twice. Downstream code written against the scalar case fails when a copy appears. Copies often appear in production rather than in the sample used for development.

`s.index.is_unique` checks. `set_index(..., verify_integrity=True)` refuses to build a duplicated index. This Is worth passing when uniqueness is part of what the data means.

`df.index.duplicated()` gives a mask of the repeats. So You can inspect them rather than guess.

## Sorted indexes

`is_monotonic_increasing` tells you whether the index is sorted.

A sorted index allows binary-search lookups. This Matters on large frames.

It's often said that label-range slicing *needs* a sorted index. That isn't quite the rule. The editor above shows it. A **unique** index slices fine what order it's in. Pandas can find each bound unambiguously and take all between them. What it can't do is slice a **non-unique, unsorted** index. There's no single spot for a repeated bound. It raises rather than guessing.

Worth knowing what that slice returns on an unsorted index. All between the two bounds *in the index's own order*. This Isn't numeric order. That is rarely what people intend. `sort_index()` first is still good practice even where it isn't needed.

Note that label slicing with `.loc` is **inclusive of the endpoint**, unlike every other slice in Python. `s.loc[100:200]` includes 200. That is deliberate. With labels there's no "one past the end" to point at. And it's a solid source of off-by-one surprises.

`sort_index()` sorts by the index. `sort_values()` sorts by the data. Both return new objects by default.

## The habits worth forming

Look at the index when a result surprises you. It's the first thing to check, ahead of the values.

Call `reset_index(drop=True)` after filtering when downstream code will think positionally.

Prefer `.loc` and `.iloc` over bare `[]`. That "label" or "spot" is written down rather than inferred.

Use `fill_value` when mixing objects whose labels may not match just.

And check `is_unique` before leaning on a lookup returning one row.

## Kinds of index

The default is a `RangeIndex`. A compact `0, 1, 2, ...` that stores only start, stop and step rather than the values.

`Index` holds any labels: strings, ints, anything hashable.

`DatetimeIndex` holds timestamps and unlocks partial string pick (`s["2024-02"]`) and `resample`.

`CategoricalIndex` holds a fixed set of groups, and is memory-fast for a repeated key.

`MultiIndex` holds a few levels, and is what a group-by on more than one key returns.

You rarely choose between these on purpose. They arrive from what made the object. Knowing which you've shows what steps are on hand.

## The index is not free

`RangeIndex` costs almost nothing. Any other index stores one label per row. A string index over a million rows is a million Python strings. Often larger than the numeric columns it labels.

`df.index.dtype` and `df.memory_usage(deep=True)` show it. `reset_index(drop=True)` discards it and returns to a `RangeIndex`. This Is worth doing when the labels carry no meaning.

That is the hands-on arg for not setting a real index reflexively. It costs memory. It only pays if you really select or join on it.

## Selecting with an index that is not unique

`is_unique` is worth checking before leaning on lookups. The return type of `s[label]` depends on it.

With a unique index, `s["a"]` is a scalar. With a duplicated one it's a Series. Code written against the first case. Math, a compare, passing the value to a function. Breaks on the second. The break happens wherever the value is used rather than at the lookup.

`df.index.duplicated()` gives a mask of the repeats, and `df[df.index.duplicated(keep=False)]` shows each conflicting group.

`verify_integrity=True` on `set_index` refuses to build a duplicated index. Is worth passing when uniqueness is part of what the data means.

## Aligning on purpose

Alignment is often helpful and at times in the way. Three ways to control it:

**Match the indexes** &mdash; `reindex(other.index)` conforms one object to another's labels, filling missing ones with `NaN`. This is alignment made clear rather than silent.

**Drop the index** &mdash; `.values` or `.to_numpy()` gives a plain array with no labels. Steps become spot-based. Use it when you know the order is right and the labels are noise, and comment why.

**Reset both** &mdash; `reset_index(drop=True)` on both sides before mixing, when they should match row-for-row.

The failure this blocks is the one from the previous module. Two objects that *should* line up, whose indexes have drifted apart because one was filtered, silently making `NaN` or a much longer result.

## Index methods worth knowing

An Index behaves like an immutable set. The set steps are at times just what you need:

`a.index.gap(b.index)` &mdash; labels in one and not the other. The fastest way to find out which rows a join would drop.

`a.index.intersection(b.index)` &mdash; the common labels.

`idx.get_loc(label)` &mdash; the spot of a label, for when you truly need to cross from labels to spots.

`idx.str` &mdash; the string accessor works on an Index too. This Is how you clean column names in one formula.

Indexes are immutable. You can't assign into one. You build a new one and attach it. That is deliberate. A mutable index would break the hash-based lookups that make label pick fast.

## When to set a meaningful index

**Set one** when you'll look rows up by that key again and again, join on it more than once, or need time-based pick and `resample`.

**Don't set one** when the key isn't unique, when you only need it once, or when the result is heading to a file or a merge that expects columns.

`reset_index()` is cheap and always on hand. The choice isn't permanent. Which is a good reason not to agonise over it.

## Common index mistakes

**given a filtered frame is renumbered.** It isn't. `reset_index(drop=True)` renumbers.

**Using `[0]` after a filter.** There may be no label 0. `.iloc[0]` is the spot.

**Losing `drop=True`.** `reset_index()` keeps the old index as a new column. This Then travels through each later step as an unwanted `index` column.

**Setting an index and then merging on the column.** After `set_index("id")`, there's no `id` column to merge on. Use `left_index=True`, or reset first.

**given alignment is spot-based.** It's by label. Two Series with the same values in other label orders add to a thing neither of them looks like.

**Skipping copies.** A lookup that returns a Series instead of a scalar breaks downstream code. The break happens away from the lookup.

## Reindexing

`reindex` conforms an object to a given set of labels. Present labels are kept, absent ones are filled with `NaN`. Labels not in the new set are dropped.

That makes it the tool for two jobs.

**Making frames close.** `b.reindex(a.index)` puts `b` on `a`'s labels. A later step aligns just and any mismatch is visible as `NaN` rather than silently reordering.

**Filling out a sparse axis.** Reindexing onto a full date range turns missing days into clear `NaN` rows. This Is what you want before plotting or before a rolling window over rows.

`fill_value=` sets what the gaps become. `method="ffill"` carries values forward. This Needs a sorted index.

`reindex_like(other)` is the shorthand for the first case.

## The index in output

The index is written by `to_csv` unless you pass `index=False`. Read back as an unnamed column unless you pass `index_col=0`. That round-trip mismatch is the origin of the `Unnamed: 0` column that appears in so many datasets.

`to_dict()`, `to_json()` and `to_excel` all have their own views about the index. All of them are worth checking once for any output that another system consumes.

The rule that avoids most of it: if the index is real data, name it and write it on purpose. If it isn't, `reset_index(drop=True)` before writing.

## A working summary

The index is a labelled axis, not row numbers.

It lives filtering, and alignment uses it silently.

`set_index` when you'll select or join on the key again and again. `reset_index(drop=True)` when you won't.

Check `is_unique` before leaning on lookups.

`sort_index()` after building or reshaping anything with a non-trivial index.

And when a result has the wrong number of rows or surprise `NaN`, look at the indexes of the inputs first. That is the cause more often than anything in the step itself.
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

Almost each confusion about making a DataFrame comes from one question: does this input show **columns** or **rows**?

`pd.DataFrame({"a": [1,2,3], "b": [4,5,6]})` shows columns. Each key is a column name and each value is the entire column. This is the most common form and the one to reach for when you've parallel lists.

`pd.DataFrame([{"a":1,"b":4}, {"a":2,"b":5}])` shows rows. Each dict is one record. This is the shape data arrives in from an API or a DB cursor, and pandas handles it right.

Both give the same frame. Knowing which one you're writing blocks a transposed result.

## What each form tolerates

**Dict of columns** needs equal lengths and raises else. This Is a handy check. A **scalar** value is the exception. It broadcasts to each row. `{"a": [1,2,3], "flag": True}` gives a flag column of three `True` values.

**List of dicts** doesn't need the keys to match. Missing keys become `NaN`. The column order follows first appearance across all records. That handling is convenient for messy input and worth watching. A typo in one record's key silently creates a new mostly-empty column rather than raising.

**List of lists** works but names the columns `0, 1, 2`. Pass `columns=` unless you truly want int names. int column names are legal and lead to real confusion later. `df[0]` then means a column and looks like spot-based indexing.

**Dict of scalars** raises, because pandas can't tell whether you meant one row or one column. `pd.DataFrame([d])` means one row. `pd.DataFrame.from_dict(d, orient="index")` means one column. The error is good. Guessing here would be worse.

## read_csv

For real data this is the usual entry point. It does a lot by default. Infers a dtype per column, treats the first line as a header, and parses common missing-value markers.

The args worth knowing early:

`index_col` sets a column as the index during the read rather than later.

`usecols` reads only the columns you name. This Matters on wide files. It saves both time and memory.

`dtype` replaces inference. This is how you stop an identifier column being read as an int and losing its leading zeros. How you read a low-cardinality column straight into `group`.

`parse_dates` converts date columns during the read. This Is faster than converting later.

`nrows` reads a sample. This Is the right way to inspect a large file before committing to it.

It accepts any file-like object. So `io.StringIO` works for testing and for data that is already in memory.

## Type inference and its costs

`read_csv` and the constructors infer types per column. That is often helpful and at times wrong in costly ways.

A column of ints with one missing value turns `float64`. Int arrays can't hold NaN. Identifiers then print as `1001.0`.

A column that is mostly numbers with one stray non-numeric value turns `object`. Each later numeric step on it either fails or silently operates on strings.

Both are worth checking with `df.dtypes` at once after loading. It takes one line and catches a group of bug that else surfaces much later.

## Never grow a frame

`acc.loc[len(acc)] = row` inside a loop reallocates the entire frame on each loop. So did `df.append`. This Is why it was **removed in pandas 2.0** rather than merely deprecated.

The correct pattern is the same as NumPy's. Collect into a Python list and make once at the end. Lists append cheaply. DataFrames don't append at all.

If the pieces are already frames, `pd.concat(list_of_frames)` once at the end is the right call. And `pd.concat` inside a loop is just the same mistake in a other costume.

The last editor measures it. The gap grows with the number of rows. A pattern that seems acceptable on a hundred records turns unusable on a hundred thousand.

## Choosing

**Parallel lists you already have**: dict of columns.

**Records from an API or a cursor**: list of dicts.

**A file**: `read_csv`, with `dtype` and `usecols` set deliberately.

**A NumPy array**: `pd.DataFrame(arr, columns=[...])`, remembering that the array's single dtype applies to every column until you convert.

**One row from a dict**: `pd.DataFrame([d])`.

And in each case, print `df.dtypes` and `df.shape` at once later. Those two lines catch most of what goes wrong at the boundary between raw data and pandas.

## From a NumPy array

`pd.DataFrame(arr, columns=[...])` wraps an array. The array has **one** dtype. Each column starts with that dtype until you convert.

That matters when the array came from a thing that widened it. An array of mixed data is `object`. A DataFrame built from it has each column as `object`. Numeric-looking columns that don't behave by number.

`index=` sets the labels also.

For the reverse direction, `df.to_numpy()` merges back to a single dtype. `df.values` is the older spelling of the same thing.

## From a database or an API

`pd.read_sql(query, link)` runs a query and returns a frame, with column names taken from the result. It accepts a SQLAlchemy link or a raw DBAPI one.

`pd.read_json` handles JSON, and `pd.json_normalize` is the one worth knowing. It flattens **nested** JSON into columns, turning `{"user": {"name": "ana"}}` into a `user.name` column. Most API responses need it, and building the frame by hand from nested dicts is the long way round.

`pd.read_html(url_or_html)` scrapes each table on a page into a list of frames. It's startlingly good for simple pages and needs `lxml` or `bs4` installed.

## Setting the index at creation

Any of the constructors accept `index=`, and `read_csv` accepts `index_col=`.

Doing it at creation is slightly cheaper than `set_index` later. More importantly it docs that the column is a key rather than data.

If the index should be a `DatetimeIndex`, parse the dates in the same call: `read_csv(path, parse_dates=["date"], index_col="date")` gives a time-indexed frame in one step.

## Empty frames, and why they cause trouble

`pd.DataFrame()` is legal and at times handy as a placeholder.

It's a poor starting point for build-up, for two reasons. Growing it row by row is quadratic, as the last editor shows. And its columns have no real dtype. The first `concat` into it can widen all to `object`. At which point the frame is slow and the numeric columns are no longer numeric.

`pd.DataFrame(columns=["a", "b"])` has the same problem with more ceremony.

The pattern to use instead is always the same. Build a **list** of rows or of frames. Make once at the end.

## Checking what you built

Four lines, at once after build, catch most problems at the boundary:

```python
df.shape        # is this the number of rows I expected?
df.dtypes       # did anything become object or float unexpectedly?
df.head()       # does the data look like the data?
df.isna().sum() # where are the gaps?
```

The second is the one that earns its keep. Type inference is where most silent damage happens. It happens just once, at build.

## Choosing a constructor

**Parallel lists you already have** &mdash; a dict of columns.

**Records from an API or a cursor**. A list of dicts, or `json_normalize` if they're nested.

**A file** &mdash; `read_csv`, with `dtype`, `usecols` and `parse_dates` set on purpose.

**A query** &mdash; `read_sql`. This Names the columns for you.

**A NumPy array** &mdash; the constructor with `columns=`, remembering the single dtype.

**One row from a dict** &mdash; `pd.DataFrame([d])`.

**built up pieces** &mdash; a list, then `pd.DataFrame(rows)` or `pd.concat(frames)` once.

In each branch, set the dtype at creation rather than converting later. `astype` allocates a second full frame. Getting it right the first time avoids both the copy and the class of bugs where a column silently isn't the type you assumed.

## Reproducible test frames

Small frames written by hand are how you check that an step does what you think. It's worth having a habit for them.

A dict of columns is the most readable form for a handful of rows. `pd.DataFrame({"a": [1,2,3], "b": list("xyz")})` fits on one line and shows the columns clearly.

For a frame with a exact index, pass `index=` rather than setting it later.

For random test data, seed it: `np.random.default_rng(0)`. Unseeded random test data makes a failing check unreproducible. This Is the opposite of what a test is for.

`pd.util.testing` used to provide frame gens. The supported route now is `pd.testing.assert_frame_equal` for checks, and building the frames yourself.

## Checking two frames match

`pd.testing.assert_frame_equal(a, b)` is the precise compare: values, dtypes, index and column order all have to agree. The error message says which differed.

`check_dtype=False` relaxes the type compare. This Is often needed when one side came through a CSV.

`check_like=True` skips row and column order.

This is what belongs in a test, rather than `a.equals(b)`. When it fails it tells you *what* failed.

## Copy semantics at construction

`pd.DataFrame(some_array)` does **not** always copy. If the array's dtype and layout are usable right, pandas may wrap it. Writing to the frame then writes to the array.

`copy=True` forces a copy. Under copy-on-write this stops mattering. This Is another reason that change is welcome.

`pd.DataFrame(dict_of_series)` aligns the Series on their indexes. This Is easy to forget. Three Series with other labels give a frame with the union of them and `NaN` in the gaps, not three columns side by side.

If you meant "these are parallel columns", reset the indexes first or pass plain lists.

## The construction checklist

Decide whether the input shows rows or columns.

Pass `columns=` if the source has no names.

Set `dtype` at build, above all for identifiers and for ints that may have gaps.

Set `index=` if a column is really a key.

Then check `shape`, `dtypes`, `head()` and `isna().sum()`.

Never grow a frame in a loop.

That is six lines of discipline that prevent most of what the cleaning modules exist to repair.

## A closing note

build is where a frame's types are decided. Types decided badly here cause problems all over later.

The two questions worth answering on purpose are whether the input shows rows or columns. What the dtypes should be. Getting the first wrong gives a transposed frame that is at once obvious. Getting the second wrong gives a frame that looks correct and behaves oddly much later.

`dtype=` at build costs nothing. `astype` later allocates a second copy of each column it touches. By then the leading zeros may already be gone.

The other rule is the one shared with NumPy. Never grow a frame in a loop. Collect into a list and make once. `df.loc[len(df)] = row` and `pd.concat` inside a loop are the same quadratic mistake wearing other syntax. `df.append` was removed rather than merely deprecated because of it.

## One more thing

`pd.DataFrame.from_records` handles an iterable of tuples with a `columns` arg. Accepts an `index` naming one of the fields. It's the constructor that fits a DB cursor most right. Cursors yield tuples rather than dicts.

And `pd.concat` of many small frames is often faster than building one large list of dicts when the pieces are already frames. The rule is to avoid the loop, not to prefer one holder over the other.

## In summary

Decide whether the input shows rows or columns, set the dtypes at build. Check `shape`, `dtypes` and `head` at once later.

Never grow a frame in a loop. Collect into a list and build once. `df.append` was removed rather than deprecated because of just that pattern.
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

Most pandas bugs aren't bugs in pandas. They're assumptions about the data that were never checked. A column that is text where you expected numbers, an identifier that lost its leading zeros, a group with four spellings, a date column that is still strings.

None of these raise. They give plausible output that is wrong. The error surfaces much later, one spot unrelated.

Six calls catch nearly all of it, and together they take under a minute.

## shape and dtypes

`df.shape` gives `(rows, columns)`. It confirms the file loaded as expected. Catches the case where a delimiter was misread and all landed in one column.

`df.dtypes` is the key one. Three failures show up here and nowhere else:

**An identifier read as an int.** `001` turns `1`. The leading zeros are gone permanently. Fix at read time with `dtype={"id": str}`.

**An int column turned float** because one value is missing. NumPy ints can't hold NaN. Pandas promotes. The symptom downstream is ids printing as `1001.0`.

**A numeric column read as `object`** because one row holds a stray non-numeric value. each later numeric step then either fails or silently operates on strings.

Running these two lines at once after loading is the highest-value habit in this module.

## head, tail, sample

Look at the data. Not the summary &mdash; the actual rows.

`head()` shows the first five. That is fine for a random file and misleading for a sorted one, a dated one, or one where the format changes partway through.

`tail()` catches trailing junk: summary rows, blank lines, a footer the exporter added.

`sample(n, random_state=0)` shows the middle. This Is where the surprises often live. Passing `random_state` makes it reproducible. This Matters if you're going to discuss what you saw.

## info

`df.info()` prints dtypes, non-null counts and memory usage together.

The non-null count is the part to read carefully. Compare it against the row count for each column. A column with 400 non-null out of 10,000 rows is in effect empty and any analysis using it's built on 4% of the data.

`memory_usage="deep"` gives the true cost of object columns. This The default underestimates badly because it counts the pointers rather than the strings they point at.

## describe

`df.show()` gives count, mean, standard deviation, min, max and quartiles for **numeric columns only**.

`include="all"` adds text columns, reporting count, unique, top and rate for them instead.

The most handy reading of it's the **mean against the median** (the 50% row). When they're far apart, the spread is skewed or holds outliers. Each mean-based summary you were about to find will mislead. A `mean` of 220 with a `50%` of 30 is telling you a thing key before you've written any analysis.

`min` and `max` are also worth a glance for hopeless values. A minus age, a date in 1900, a price of zero.

## Missing values

`df.isna().sum()` counts them per column. `df.isna().mean()` gives the proportion. This Is easier to judge than a raw count.

`df.isna().any(axis=1).sum()` counts rows affected by any missing value. The number you'd lose to `dropna()`. Often much larger than any single column's count.

Doing this before deciding how to handle missing data means the choice is informed rather than reflexive. Dropping 2% of rows is other from dropping 60%.

## value_counts

For each text or cat column, run `value_counts()`.

It finds, in one line: typos, inconsistent capitalisation, trailing whitespace, surprise groups. Cardinality far higher than expected (often a sign the column is really an identifier).

The last editor shows two cities appearing as four values. `pune`, `Pune`. `pune ` with a trailing space. A group-by on that column would give four groups, and nothing would warn you.

`dropna=False` includes missing values in the count. This Is else invisible here.

`norm=True` gives shares rather than counts. This Is the right form when checking spreads between datasets.

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

It isn't glamorous and it isn't optional. each one of these calls has a exact failure it catches. The option is finding that failure later, in a result you've already shown someone.

## Making the display readable

Default display settings hide things, and hidden data is data you won't check.

`pd.set_option("display.max_columns", None)` stops columns being elided into `...`. This Is the single most handy setting on a wide frame.

`pd.set_option("display.width", 200)` controls wrapping.

`pd.set_option("display.max_rows", 100)` shows more before truncating.

`pd.set_option("display.float_format", "{:.2f}".format)` stops fifteen decimal places dominating each table.

These affect display only, never the data. In a notebook they're worth putting in the first cell.

## Reading info carefully

`df.info()` packs four things into one output, and each deserves a look.

**The row count** in the header, against what you expected from the source.

**Non-Null Count** per column, against that row count. This is the fastest way to find a column that is mostly empty.

**Dtype** per column. `object` on a thing that should be numeric is a problem. `float64` on a thing that should be int often means a missing value.

**Memory usage**, which needs `memory_usage="deep"` to be truthful about text columns.

A column with, say, 400 non-null out of 200,000 rows is in effect empty. Any analysis using it's built on 0.2% of the data. It's better to know that before building the analysis than after presenting it.

## describe, beyond the defaults

`percentiles=[0.01, 0.5, 0.99]` changes which quantiles are shown. The 1st and 99th are often more helpful than the quartiles for spotting outliers.

`include="all"` adds non-numeric columns, reporting `count`, `unique`, `top` and `freq` for them.

`include=["object"]` or `exclude=["number"]` restrict it.

`df.show().T` transposes the result. This Is much easier to read when there are many columns. One row per column instead of one column per column.

Three readings worth making a habit:

**mean against 50%** &mdash; far apart means skew or outliers.

**min and max** &mdash; look for hopeless values: a minus age, a zero price, a date in 1900.

**std of zero** &mdash; a constant column. This Carries no data and is often a sign a thing upstream went wrong.

## Looking at the missing rows, not just counting them

Counting missing values tells you how much. Looking at *which* rows are missing tells you why.

```python
df[df["income"].isna()].head()
```

If those rows share a thing. The same source, the same date range, the same group &mdash; then the data isn't missing at random. Both dropping and imputing will bias the result.

`df.isna().sum(axis=1).value_counts()` shows how many rows have 0, 1, 2... missing values. A long tail means a few badly broken rows. A big spike at one value often means an entire column is absent for a subset of the data.

## Comparing two frames

When a thing changes and you want to know what, three tools:

`df.equals(other)` &mdash; exact, including dtypes.

`df.compare(other)` &mdash; shows only the cells that differ, side by side. It needs same shape and labels. This Makes it right for before-and-after checks on the same data.

`set(a.columns) ^ set(b.columns)` &mdash; the even gap of column names. This Is often where the discrepancy is.

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

That is a minute of work and it answers most of the questions you'd else discover the hard way. What types things are. Here The gaps are. This Groups are messy. Whether the file is what you were told it was.

## Profiling a frame quickly

For a fast total picture beyond `show`, three one-liners cover most of it:

```python
df.nunique().sort_values()                      # cardinality per column
df.isna().mean().sort_values(ascending=False)   # missingness per column
df.memory_usage(deep=True).sort_values(ascending=False)
```

Cardinality is the most under-used of the three. A column with one distinct value carries no data. A column with as many distinct values as rows is an identifier, not a feature. all notable is in between. The ranking tells you which columns are which without opening any of them.

## Checking assumptions explicitly

Looking at data is better than not looking. Asserting is better than looking. An assertion keeps checking after you stop paying focus.

```python
assert df["id"].is_unique
assert df["age"].between(0, 120).all()
assert set(df["status"]) <= {"open", "closed"}
assert df["date"].notna().all()
```

Each of these codes a thing you believe about the data. When the belief stops being true. A new export, a changed upstream system. The script stops rather than making a quietly wrong answer.

That is worth more than any amount of exploratory looking. The looking happens once and the assertions happen each run.

## The shape of a first pass

The order matters, because each step informs the next.

**Shape and dtypes** &mdash; is this the file I think it's?

**head, tail, sample** &mdash; does the data look like data?

**info** &mdash; where are the gaps and how big is this?

**show** &mdash; are there hopeless or extreme values?

**value_counts on cats** &mdash; are the groups what I expect, and how many are there?

**Missingness pattern** &mdash; are the gaps random or structured?

Only then is it worth writing any analysis. each one of these steps has caught, for someone, a problem that would else have surfaced in a result presented to someone else.

## Two habits that pay repeatedly

**Look at the rows you're about to drop.** Before `dropna`, before a filter, before deduplication. `df[mask].head()`. If the rows you're discarding share a pattern, you aren't dropping noise, you're dropping a group.

**Compare counts before and after each step that can change them.** A filter, a merge, a group-by, a concat. One number, checked, catches silent row product and silent row loss. This Between them account for a large share of wrong answers in data work.

## A closing note

each one of these calls exists because someone shipped a wrong answer that one of them would have caught.

The routine is short enough to run without thinking about it. The discipline is to run it **before** writing any analysis rather than after a result looks odd. By the time a number looks wrong, the cheap reasons have been ruled out and the costly debugging has started.

The single highest-value line is `df.dtypes`. It catches the identifier read as an int, the date left as text. The numeric column turned into strings by one stray value. Three failures that give plausible output and no error.

The second is `value_counts` on the cat columns. This Finds the variants that would silently split a group-by.

Neither takes more than a few seconds. Together they answer most of what you need to know about a file you haven't seen before.

## One more thing

`df.head()` and `df.tail()` can be mixed into one view with `pd.concat([df.head(3), df.tail(3)])`. This Shows both ends of a sorted frame at once. handy when the notable rows are the extremes.

And `df.sample(frac=1)` shuffles the whole frame. This Is at times the honest way to look at data that arrived in a real order. The first rows of a sorted file aren't representative of anything.

## In summary

Six calls, run before any analysis, catch most of what goes wrong: `shape`, `dtypes`, `head`/`sample`, `info`, `show`. `value_counts` on the cat columns.

`dtypes` is the one that earns its place. It reveals the identifier read as a number, the date still stored as text. The numeric column turned into strings by a single stray value. Three failures that give plausible output and no error at all.

And an assertion is worth more than a look. The look happens once and the assertion happens each run.
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
intro: Label or spot, and the endpoint rule that differs between them.

## The distinction

`.loc` selects by **label** &mdash; the values in the index.

`.iloc` selects by **spot** &mdash; where the row sits, from 0.

On a freshly created frame the index is `0, 1, 2, ...`. Label and spot are the same number and the two behave the same way. That coincidence is why the gap goes unnoticed until a thing breaks it. A filter, a sort, a join, a `set_index`.

After any of those, `df.loc[0]` and `df.iloc[0]` can refer to other rows. Or `.loc[0]` can raise `KeyError` because no row is labelled 0 any more.

Writing `.loc` or `.iloc` by name, rather than bare `df[...]`, makes the choice visible. Bare brackets guess. The guess changes with the arg type: `df["age"]` is a column, `df[0:2]` is rows by spot, `df[mask]` is rows by rule. Three meanings for one syntax is a lot to hold. The clear accessors cost four characters.

## The endpoint rule

This is the one that catches all.

`df.iloc[1:4]` gives spots 1, 2, 3. The end is **excluded**, just like a list slice.

`df.loc["b":"d"]` gives labels b, c **and d**. The end is **included**.

labels have no natural "one past the end". With spots you can point at index 4 to mean "stop before here". With any labels. Strings, dates, non-contiguous ints. There's no such thing as the label after `d`, so pandas includes it.

The hands-on result: on a default index, `df.loc[1:3]` returns **three** rows and `df.iloc[1:3]` returns **two**. Both look correct in alone.

Label slicing also needs a sorted index when the labels aren't unique or not monotonic. Else it raises rather than guessing.

## Two axes

Both accessors take rows first, then columns:

`df.loc[row_selection, column_selection]`

Each part can be a single value, a list, a slice or (for `.loc`) a boolean mask.

`df.loc[:, "age"]` is a whole column. `df.loc["r2"]` is a whole row, returned as a Series whose index is the column names.

This two-axis form is the one to prefer. Not only for brevity. `df.loc[mask, "col"]` is a single indexing step on a single object. This Is what makes set through it solid. `df[mask]["col"]` is two steps, the first of which may have made a copy. And that is the subject of the next module.

## Boolean masks

Masks go in `.loc`. `df.loc[df["age"] >= 25]` selects matching rows. `df.loc[df["age"] >= 25, ["name", "city"]]` selects matching rows and named columns in one call.

`.iloc` doesn't accept a labelled boolean Series. It will take a plain list or array of booleans. Not a Series. A Series carries an index and `.iloc` is defined to skip labels. Accepting one would be ambiguous. The error is deliberate.

If you need to use a mask positionally, `.to_numpy()` on it strips the index.

## at and iat

For a single cell, `.at` (label) and `.iat` (spot) are faster than `.loc` and `.iloc`. They skip the machinery that handles slices, lists and masks.

The gap is small for one call and large in a loop, as the fifth editor measures.

They also raise if you ask for more than one cell. This Makes them self-documenting. Seeing `.at` in code tells you the author meant just one value.

That said, a loop over cells is often the wrong shape for the problem. `.at` makes a loop faster. Dropping the loop makes it not needed.

## Assignment

The rule is short: **one `.loc` call, with both the row and column pick inside it**.

```python
df.loc[df["age"] < 30, "age"] = 30
```

pandas can see this is a single indexing step on `df` itself. It writes to `df`.

```python
df[df["age"] < 30]["age"] = 30
```

doesn't well work. The first bracket makes a new object. The set may write to that temporary rather than to `df`. Once this raised `SettingWithCopyWarning`. In current pandas it may silently do nothing.

Assigning a column for a subset of rows fills the unselected rows with `NaN`. This Is often what you want and is worth expecting rather than discovering.

## A working summary

Use `.loc` when you mean labels, `.iloc` when you mean spots. Write one of them rather than bare brackets.

note that `.loc` slices include the endpoint.

Put row and column pick in the same call.

Use `.at`/`.iat` for a single cell if you're in a loop. Consider whether the loop should exist.

And after any filter or sort, be aware that spots and labels have parted company. Which is the source of most of the confusion these two accessors exist to prevent.

## What bare brackets do

`df[...]` guesses from the arg, and the guess changes with the type:

`df["age"]` &mdash; a **column**, returned as a Series.

`df[["age", "city"]]` &mdash; a few **columns**, returned as a DataFrame.

`df[0:2]` &mdash; **rows** by spot.

`df["a":"c"]` &mdash; **rows** by label.

`df[mask]` &mdash; **rows** by rule.

Five actions, two axes, one syntax. It reads well for the common case. Selecting a column. And is a genuine source of confusion for all else. The same brackets at times mean rows and at times columns.

`.loc` and `.iloc` drop the guessing. That is the arg for using them even where bare brackets would work.

One result worth knowing: on a Series, `s[0]` is ambiguous when the index is ints. Is `0` a label or a spot? pandas treats it as a **label**. This Raises if there's no label 0 even when there are plenty of rows. This ambiguity is why the spot-based-only accessor exists.

## Callable selection

Both accessors accept a **function** that receives the object and returns a pick:

```python
df.loc[lambda d: d["age"] > 30]
```

That looks like extra syntax for the same thing. It earns its place in a chain. Here `df` may not be the object being selected from:

```python
(df.query("year == 2024")
   .assign(total=lambda d: d["a"] * d["b"])
   .loc[lambda d: d["total"] > 100])
```

Without the lambda, the final `loc` would have to link an mid that doesn't have a name.

## Selecting columns by type or name pattern

`df.select_dtypes(include="number")` picks columns by dtype, and `exclude=` is the inverse. This is how you apply an step to each numeric column without listing them.

`df.filter(like="date")` selects columns whose name holds a substring. `regex=` takes a pattern. `items=` takes an clear list.

Both return a frame, so they compose with all else. They're a lot more robust than a hard-coded column list when the source data gains or loses columns.

## Setting values

The rules for set through `.loc` are worth stating by name. Each has a failure mode.

**A scalar broadcasts**: `df.loc[mask, "col"] = 0` fills every selected row.

**A list or array must match the pick length just**, and goes in positionally.

**A Series aligns on the index**. Labels that aren't in the pick are skipped and labels missing from it become `NaN`.

**A new column created for a subset** leaves `NaN` in the unselected rows.

**The dtype does not widen to fit**: assigning 3.7 into an integer column stores 3. Assigning a string into a numeric column may upcast the whole column to `object`, which is worse.

## Enlargement

`.loc` can create rows and columns that don't exist:

`df.loc["new_row"] = [...]` adds a row. `df.loc[:, "new_col"] = ...` adds a column.

`.iloc` **can't** &mdash; a spot that doesn't exist is an error. There's no sensible spot to create.

Enlargement is convenient for one addition and is the quadratic anti-pattern in a loop. It's the method behind `df.loc[len(df)] = row`. This Is the slow way to build a frame.

## A summary

Use `.loc` for labels and `.iloc` for spots. Write one of them rather than leaning on bare brackets to guess.

note `.loc` slices include the endpoint and `.iloc` slices don't.

Put both picks in one call, above all when assigning.

Use `.at`/`.iat` for a single cell in a loop. Consider whether the loop is needed.

Use `select_dtypes` and `filter` instead of hard-coded column lists when the schema may change.

And after any filter or sort, note that labels and spots have parted company. Which is the confusion these accessors exist to prevent.

## Copy or view, briefly

Whether `.loc` returns a view or a copy is on purpose unspecified. Depends on the inner block layout.

That is the whole reason the copy warning exists. It's why the guidance in this module is phrased as "put both picks in one call" rather than "select and then assign".

Under copy-on-write, picks always behave as copies and the ambiguity disappears. But the one-call rule remains correct, because it's also clearer.

## Selecting a single row or column

`df.loc["r2"]` returns a **Series** whose index is the column names. That means the row's values are forced into one dtype. A row holding an int and a string comes back as `object`. The int is now an object.

That is a real hazard when iterating rows or passing a row to a function. It's the same problem `iterrows` has, for the same reason.

`df.loc[["r2"]]` &mdash; a list rather than a scalar &mdash; returns a one-row **DataFrame** instead, preserving each column's dtype. When the dtypes matter, that is the form to use.

The same gap applies to columns: `df["a"]` is a Series, `df[["a"]]` is a one-column frame.

## Common errors and what they mean

**`KeyError`** on `.loc` &mdash; the label doesn't exist. Often because the frame was filtered and the labels changed, or because the key is a string where you passed an int.

**`IndexError`** on `.iloc` &mdash; the spot is out of range.

**"Can't mask with non-boolean array holding NA / NaN values"**. A `.str` predicate without `na=False`.

**"The truth value of a Series is ambiguous"**. `and`/`or` where `&`/`|` was needed, or a missing pair of parentheses.

**"can't reindex on an axis with copy labels"**. The index has repeats and the step needs uniqueness.

**`SettingWithCopyWarning`** &mdash; two indexing steps on the left of an set.

Each of these has one usual cause. Recognising them saves more time than any amount of general debugging.

## A short reference

`df["col"]` &mdash; one column, as a Series.

`df[["a", "b"]]` &mdash; a few columns, as a frame.

`df.loc[rows, cols]` &mdash; by label, endpoint inclusive.

`df.iloc[rows, cols]` &mdash; by spot, endpoint exclusive.

`df.at[row, col]` / `df.iat[i, j]` &mdash; one cell, fast.

`df.loc[mask]` &mdash; rows by rule.

`df.loc[mask, "col"] = value` &mdash; the only set form worth using.

`df.select_dtypes(...)` / `df.filter(...)` &mdash; columns by type or name pattern.

## A closing note

The gap is small to state and causes a disproportionate amount of confusion. On a freshly loaded frame label and spot are the same number.

They part company the first time anything filters, sorts, joins or reindexes. And from then on `df.loc[0]` and `df.iloc[0]` may be other rows, or `.loc[0]` may raise because no row is labelled 0 any more.

Writing `.loc` or `.iloc` rather than bare brackets makes the choice clear. This Matters because bare brackets guess differently based on what you hand them. A column for a string, rows for a slice, rows for a mask.

The endpoint rule is the other thing to carry: `.loc` slices include the last label, `.iloc` slices don't. On a default index the two forms differ by just one row, and both look correct.

And for set there's only one form worth using. A single `.loc` with the rows and the column both inside it.
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
intro: Masks, isin, between and query, and the parenthesis rule that catches all.
## A mask is a Series

`df["age"] >= 25` doesn't return rows. It returns a boolean Series, one value per row, carrying the same index as the frame.

You then hand that mask to `.loc`, and pandas keeps the rows where it's `True`.

Because the mask is an plain Series, all you know applies to it. `mask.sum()` counts matches. `True` is 1. `mask.mean()` gives the proportion. `~mask` inverts it. It can be stored in a var, named, and reused.

Naming masks is worth doing when a filter has a few parts:

```python
adult = df["age"] >= 18
local = df["city"] == "pune"
recent = df["days"] < 30
df.loc[adult & local & recent]
```

Each name docs a rule, and each can be counted apart when the result is unexpectedly empty. Which is how you find out which clause is doing the damage.

## The parenthesis rule

This is the single most common syntax error in pandas.

`df["age"] > 20 & df["age"] < 35` doesn't mean what it looks like. In Python, `&` binds **tighter** than `>`. This parses as `df["age"] > (20 & df["age"]) < 35`. The result is an error or, worse, a thing plausible.

each rule needs its own parentheses: `(df["age"] > 20) & (df["age"] < 35)`.

The related mistake is `and` instead of `&`. Python's `and` needs a single truth value and a Series has many. It raises "The truth value of a Series is ambiguous". That message always means the same thing: use `&`, and add parentheses.

The three ops are `&` (and), `|` (or), `~` (not). There's no way to make Python's precedence rules cooperate here. Parenthesising turns a reflex.

## isin and between

`df["city"].isin(["pune", "goa"])` is clearer and faster than `(df["city"] == "pune") | (df["city"] == "goa")`. It scales to a list of any length. Including one found at runtime.

`df["age"].between(25, 31)` is inclusive of both ends by default. The `inclusive` arg takes `"both"`, `"left"`, `"right"` or `"neither"`. This Is worth passing by name when the boundary matters. The default isn't what all assumes.

`~` negates either of them.

## Missing values fail everything

each compare involving `NaN` is `False`. That includes `>`, `<`, `==` and `!=`.

The result is exact and easy to miss: `df[df["x"] > 2]` and `df[df["x"] <= 2]` do **not** split the frame. Rows where `x` is missing are absent from both. The two counts don't add up to the row count.

This is often the right default. An unknown value truly doesn't meet a rule. But it means "all else" isn't the same as "the negation of this rule" when missing data is possible.

When missing rows should be handled rather than dropped, say so by name with `isna()`, or fill before filtering.

## query

`df.query("age > 20 and score > 7")` takes the rule as a string.

Inside the string, column names are bare identifiers, `and`/`or`/`not` work most times. No parentheses are needed for precedence. That makes long rules much easier to read than the op form.

`@name` links a Python var: `df.query("age > @cutoff")`.

`in` and `not in` work against lists.

The costs: column names with spaces need backticks, there's no editor autocompletion or type checking inside a string. A typo turns a runtime error rather than a thing a linter catches. `query` also has a small parsing cost per call. This Is irrelevant once and noticeable in a loop.

Use it when a rule is long enough that the op form is hard to read. Use ops else.

## Filtering copies

`df.loc[mask]` returns a **new** frame. The first is untouched. The result keeps the first index labels rather than renumbering.

Both facts matter downstream. The surviving labels mean spot-based code breaks. `reset_index(drop=True)` is the fix when you want a clean `0..n-1`.

That the result is new. And namely that it may be a copy rather than a view of the first &mdash; is what makes assigning into a filtered frame unreliable. That is the subject of the next module. It's the single largest source of confusion in pandas.

## A summary

Build masks with checks, combine with `& | ~`, and parenthesise all.

Prefer `isin` and `between` where they fit. They say what you mean.

note NaN fails each test. So A rule and its negation aren't a split.

Reach for `query` when the formula is long, and for ops when it's short.

And know that the result is a new object whose index came along for the ride.

## Filtering on more than one column

Rules on other columns combine just like rules on one:

```python
df.loc[(df["age"] >= 18) & (df["city"] == "pune")]
```

For a var number of rules. Built from user input, or a config &mdash; combine them programmatically:

```python
from functools import reduce
mask = reduce(lambda a, b: a & b, conditions)
```

`np.logical_and.reduce(rules)` does the same thing. Either is better than building a query string. This Loses type checking and invites injection if any part comes from outside.

## Filtering by index rather than data

`df.loc[["a", "c"]]` selects by label and **raises** if a label is missing.

`df.reindex(["a", "c", "zz"])` selects by label and fills missing ones with `NaN` instead. The gap matters when you're conforming one frame to another's labels and lack is expected.

`df[df.index.isin(wanted)]` filters by membership without needing each label to exist.

`df.index.str.startswith("2024")` works when the labels are strings, since an Index has the `.str` accessor too.

## Filtering with a lookup from another frame

The common task of "keep rows whose key appears in this other table" has two forms.

`df[df["id"].isin(other["id"])]` is the direct one, and it's often what you want. It can't change the row count upward and needs no thought about join semantics.

`df.merge(other[["id"]], on="id")` does the same thing as an inner join. **can** times rows if `other` has copy ids. `isin` can't.

For "keep rows whose key does **not** appear", `~isin` is the whole answer. Here The join equal needs an outer join with an indicator and a filter. This is one of the places `isin` is clearly better than a merge.

## nlargest, sample and head as filters

Not each subset comes from a rule.

`df.nlargest(10, "sales")` &mdash; the top ten by a column, without sorting all.

`df.sample(n=100, random_state=0)` &mdash; a random subset, reproducible with the seed. `frac=0.1` takes a proportion.

`df.head(1000)` &mdash; the first thousand. This Is only real if the order means a thing.

`df.drop_duplicates(subset=["id"])` &mdash; one row per key.

## Performance

Filtering builds a boolean mask the length of the frame, then copies the matching rows. Both cost time scaled to the data.

Three things that help on large frames:

**Combine rules before selecting.** `df[(a) & (b)]` allocates one result. `df[a][b]` allocates two.

**Filter before finding**, not after. each step downstream then touches fewer rows. Often the largest structural win on hand.

**Use a group dtype** for the columns you filter on again and again. compare then runs on int codes rather than strings.

`query` has a small parsing cost per call. This Is irrelevant once and measurable in a loop. It can also use `numexpr` for very large frames. This At times makes it faster than the op form rather than slower.

## The mistakes, collected

**Missing parentheses.** `(a > 1) & (b < 2)`, always.

**`and` instead of `&`.** The "truth value is ambiguous" error always means this.

**Losing `na=False`** on a `.str` predicate. This Raises as soon as the data has a gap.

**given a rule and its negation split the frame.** They don't, when values can be missing.

**Chained set on a filtered frame.** `df[mask]["col"] = x`. The subject of its own module. The most costly mistake here.

**Losing the index came along.** `reset_index(drop=True)` when downstream code thinks positionally.

## Filters that read well

A filter is a statement about the data, and it's worth writing it as one.

Naming masks does most of the work:

```python
is_adult = df["age"] >= 18
in_scope = df["city"].isin(cities)
recent   = df["date"] >= cutoff

df.loc[is_adult & in_scope & recent]
```

Three gains beyond readability: each mask can be counted apart when the result is unexpectedly empty. The masks can be reused for a complementary pick. And the mixing line reads as the sentence it shows.

For a filter that appears in a few places, a small function returning the mask keeps the meaning in one place:

```python
def active(d):
    return (d["status"] == "open") & d["closed_at"].isna()
```

`df.loc[active(df)]` then means the same thing all over. Changing the meaning changes it all over.

## Debugging an empty result

When a filter returns nothing, the cause is nearly always one of five things. They can be checked in about a minute.

**A type mismatch.** `df["id"] == 1` against a string column matches nothing. Check `df["id"].dtype`.

**Whitespace or case.** `df["city"] == "Pune"` against `"pune "`. Check `df["city"].value_counts().head(20)`.

**Missing values.** They fail each compare. So A rule can exclude more than you think.

**An `&` that should be `|`.** Rules that can't be true at once.

**A stale var.** In a notebook, `df` isn't what the cell above assumed.

Counting each rule apart &mdash; `is_adult.sum()`, `in_scope.sum()` &mdash; finds which clause is in charge in one step. This Is far quicker than thinking about the mix.

## Filtering and the copy warning

`sub = df[mask]` makes a new frame whose link to `df` is on purpose unspecified.

Anything you then assign into `sub` may or may not affect `df`. This is the single most common route into the copy warning. It's worth deciding at the point of filtering rather than at the point of set:

`sub = df[mask].copy()` if `sub` is a split dataset.

`df.loc[mask, "col"] = ...` if you meant to change `df`.

Adding `.copy()` to a filter you intend to modify costs seven characters and drops the question fully.

## A closing note

Filtering is the most-used step in pandas and has two persistent gotchas, both syntactic and both cheap to avoid.

Parenthesise each rule, because `&` binds tighter than the compare ops and the unparenthesised version parses into a thing else fully. And use `&`, `|`, `~` rather than `and`, `or`, `not`. This Need a single truth value that a Series can't provide.

The semantic gotcha is missing values. They fail each compare. A rule and its negation don't split the frame. Rows quietly appear in neither half.

Beyond that, the advice is about readability: name your masks when there's more than one. Each can be counted apart when the result is unexpectedly empty. Debugging a filter that returns nothing is nearly always a matter of finding which clause is in charge. Named masks turn that into one line rather than a process of elimination.

## One more thing

`df.query` accepts `engine="python"` for expressions the default parser can't handle. `inplace=True` which, as elsewhere, is best avoided.

## In summary

checks give boolean Series. Combine them with `&`, `|` and `~`, and parenthesise each one.

`isin` and `between` read as the question being asked. `query` earns its place when the formula is long.

Missing values fail each test. So A rule and its negation don't split the frame. And `.copy()` the result if you intend to modify it. This Decides the copy question at the point it arises rather than at the point it bites.
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
intro: Why an set that looks right silently does nothing.

## The problem

```python
df[df["age"] < 30]["age"] = 99
```

This looks like it sets `age` to 99 for the young rows. Often it does nothing at all, and the frame is unchanged.

there are **two** steps here, not one.

`df[df["age"] < 30]` runs first and makes a new object. Then `["age"] = 99` assigns into *that* object. Whether the new object shares memory with `df` decides whether `df` sees the change. And if it doesn't, the write lands on a temporary that is discarded on the next line.

Once pandas noticed this pattern and raised `SettingWithCopyWarning`. The warning is famous for being confusing. It appears where the code looks fine, it at times appears when nothing is wrong. It at times fails to appear when a thing is. In current versions the set may simply do nothing, silently.

## Why pandas cannot just fix it

The obvious question is why pandas doesn't make chained set work.

It can't know, at the time the first bracket runs, that an set is coming. `df[mask]` is an plain formula that returns an object. Python then calls `__setitem__` on that object. By then the data that this was one statement is gone.

Whether the mid is a view or a copy depends on the inner layout. This Depends on the dtypes.

pandas stores columns in **blocks** of like dtype. Selecting a column that happens to be a block of its own can hand back a view. Selecting one column out of a larger same-dtype block has to build a new object.

The editor above shows this, and the direction surprises most people. The **mixed-dtype** frame gives the view. There the int column sits in a block by itself. The all-int frame gives a copy, because its columns share one block.

So the same line of code can work on one frame and not another, or work in development and fail in production when a column's type changes. That unpredictability, not the warning, is the actual problem.

## The rule

**One indexing step, with both picks inside it.**

```python
df.loc[df["age"] < 30, "age"] = 99
```

Here pandas sees a single `__setitem__` on `df` itself, with the rows and column both given. There's no mid object and no ambiguity.

Anything with two sets of brackets to the left of `=` deserves a second look. That includes the variants people reach for:

`df["age"][mask] = 99` &mdash; same problem, other order.

`df[mask]["age"] = 99` &mdash; the classic.

`sub = df[mask]` then later `sub["age"] = 99`. The same thing spread across two statements. This Is how it often appears in real code and why it's harder to spot.

## The subset case

The most common real-world version isn't a one-liner. It's:

```python
sub = df[df["city"] == "pune"]
sub["sales"] = 0
```

Here the intent is truly ambiguous. Did you want a split frame to work on, or did you want to change those rows of `df`?

Both are fair, and the fix is to say which:

```python
sub = df[df["city"] == "pune"].copy()   # a separate frame
df.loc[df["city"] == "pune", "sales"] = 0   # change the original
```

`.copy()` costs seven characters and drops the entire question. It's worth adding by default when you take a subset you intend to modify, even if you're fairly sure it would work without.

## Copy-on-write

pandas is fixing this properly. Under **copy-on-write**, each pick behaves as though it were a copy. Modifying a subset never affects the parent, in any circumstances, with no warning and no dtype-dependent surprises.

To change the first you must say so with `.loc`.

It's the default in pandas 3.0. In 2.x you can switch it on:

```python
pd.options.mode.copy_on_write = True
```

The name refers to the setup, not the action. Pandas still avoids copying data until a thing is really written. It isn't slower and is often faster. It can drop the defensive copies it used to make.

Writing code that assumes copy-on-write today means nothing changes when you upgrade. that means the two habits above. Clear `.copy()`. `.loc` for set. Which are worth having even so.

## If you see the warning

Don't silence it. `pd.options.mode.chained_assignment = None` turns off the message and leaves the bug.

Instead, find the line, and ask which of the two things you meant. The answer is always one of them, and writing it down fixes the code and docs the intent also.

## How to read the warning

The message is famously unhelpful. But It has a structure worth knowing.

*"A value is trying to be set on a copy of a slice from a DataFrame"*. Pandas noticed that the object being written to was made by indexing another object. It can't tell whether the write will pass.

*"Try using .loc[row_indexer, col_indexer] = value instead"*. The fix, stated generically.

Two properties make it frustrating.

It points at the **set**. This May be far from the line that created the mid. `sub = df[mask]` on line 10 and `sub["x"] = 1` on line 40 give a warning on line 40. Line 10 is the cause.

It's a **heuristic**. It can fire when nothing is wrong. It can stay silent when a thing is. That is why "make the warning go away" is the wrong goal. The goal is to know which object you're writing to.

## Why silencing it is worse than the warning

`pd.options.mode.chained_assignment = None` turns off the message.

It doesn't change the action. The write still may or may not reach the first frame. You've simply removed the only signal that there was a question.

You'll see this suggested. It's the wrong fix in each case. It's worth recognising in an existing code as a sign that someone met this problem and didn't resolve it.

## The two-statement version

Most real cases aren't one-liners. They look like this:

```python
recent = df[df["year"] == 2024]
recent["flag"] = recent["sales"] > 100
```

This is harder to spot than the chained form. Each line looks fully fair. It's the shape that appears in real analysis code.

The question to ask is: **is `recent` a split dataset, or a window onto `df`?**

If split: `recent = df[df["year"] == 2024].copy()`.

If a window: don't create it. Write `df.loc[df["year"] == 2024, "flag"] = ...`.

Adding `.copy()` when taking a subset you intend to modify is a cheap default. On a small frame the cost is nothing. On a large one it's a deliberate choice you've now made by name rather than by accident.

## Copy-on-write in more detail

Under CoW, each object behaves as though it owns its data. Modifying a subset never affects its parent. Modifying a parent never affects a subset taken earlier.

The name shows the setup: pandas still shares the underlying arrays. Only copies when a thing is really written. So the promise is about **action**, not about memory. CoW often uses *less* memory than the current default. Pandas can drop the defensive copies it makes today.

Three things change when you enable it:

Chained set **never** works, and pandas raises a `ChainedAssignmentError` rather than warning.

`SettingWithCopyWarning` disappears, because the ambiguity it warned about is gone.

Some code that leaned on a view passing a write will stop working. Which is the migration cost. The reason it's opt-in until pandas 3.0.

Turning it on in a project today is a good way to find out whether your code depends on action that is about to change.

## A checklist

**Two sets of brackets left of `=`**. Rewrite as one `.loc`.

**A subset you'll modify** &mdash; add `.copy()`.

**A warning you don't understand**. Find where the object was created, not where it was written.

**A tempting `chained_assignment = None`** &mdash; don't.

**New code** &mdash; write it as though copy-on-write is on. Soon it will be.

## Why this module exists

No other pandas action wastes as much time. The warning is famous, the reasons are often wrong. The standard advice on forums. Silence it. Leaves the bug in place.

The underlying issue is truly hard: Python tests `df[mask]["col"] = x` as two split steps. By the time the set happens the data that this was one statement is gone. pandas is warning about a thing it can't fix from where it stands.

Understanding that makes the fix obvious rather than any. One indexing step can't be ambiguous. Put both picks in one call.

## The rules, in one place

**One `.loc` for set.** `df.loc[mask, "col"] = value`.

**`.copy()` for a subset you'll modify.** `sub = df[mask].copy()`.

**Never silence the warning.** It drops the signal, not the problem.

**Write as though copy-on-write is on.** It will be, by default, in pandas 3.0.

Those four cover each case. There's no fifth situation needing judgement.

## Recognising it in existing code

Patterns worth searching for in a code you've from parent:

`][` on the same line as `=`. The classic chained set.

`pd.options.mode.chained_assignment = None` &mdash; someone met this and didn't fix it. all downstream of that line is suspect.

`inplace=True` on a subset &mdash; the same problem with other syntax.

A var assigned from a filter and modified later. The two-statement form. This No search finds well and which is the most common version in real code.

## What changes under copy-on-write

Worth being concrete, because "it will be fixed" isn't a plan.

Chained set raises `ChainedAssignmentError` instead of warning. So The failure is loud.

`SettingWithCopyWarning` no longer exists.

Code that leaned on a view passing a write. on purpose or accidentally. Stops working. That is the migration cost. It's why the change is opt-in for a version.

Memory usage often goes **down**, because pandas can stop making defensive copies.

Enabling `pd.options.mode.copy_on_write = True` in a project today is the cheapest way to find out whether any of your code depends on the old action.

## The one-line version

If you note nothing else from this module: **two sets of brackets to the left of an equals sign is a bug**. `.loc` with both picks inside it's the fix.

## A closing note

This is the only module in the track devoted to a warning message. It earns the space by how much time it wastes.

The underlying situation is truly awkward. `df[mask]["col"] = x` is two steps. By the time the set runs, that it was one statement is gone. pandas can't fix it from where it stands. It warns instead. Imperfectly, at times when nothing is wrong and at times not when a thing is.

That imperfection is why "make the warning stop" is the wrong goal. The right goal is to know which object you're writing to. There are only two answers. A split frame you made with `.copy()`, or the first, handled through a single `.loc`.

Copy-on-write drops the ambiguity fully and turns the default in pandas 3.0. Writing code today as though it's already on costs nothing and means the upgrade changes nothing.

## One more thing

`df._is_copy` holds the inner flag that drives the warning. It's private, it shouldn't be leaned on. Knowing it exists at times helps when thinking about why a warning appeared where it did.
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
intro: assign, drop, rename, and the alignment that decides what a new column holds.

## Bracket assignment

`df["total"] = df["qty"] * df["price"]` adds a column at the end.

Two actions are worth stating because neither warns.

A **scalar broadcasts**: `df["currency"] = "INR"` fills each row.

An **existing name is replaced**, silently. There's no protection against overwriting a column by reusing its name. This Is a real hazard in a long script where the column list isn't in front of you.

Column order is insertion order. `insert` is the only way to place one one spot exact.

## assign

`df.assign(total=...)` returns a **new** frame rather than modifying in place.

That makes it chainable, which is its main purpose:

```python
out = (df
       .assign(total=lambda d: d["qty"] * d["price"])
       .assign(cheap=lambda d: d["total"] < 100))
```

The lambda receives the frame **as it's at that point in the chain**. The second `assign` can use the column the first one created. Passing a value right rather than a lambda works too. But Then it's found against the first frame. This Breaks in a chain.

`assign` also keeps the first untouched. This Is worth a thing in a notebook where cells get re-run out of order.

The cost is a copy per call. In a hot loop that matters. In plain analysis code it doesn't. The readability of a chain often wins.

## Alignment decides the contents

This is the part that surprises people, and it's the index rule again.

Assigning a **Series** aligns on the index. If the Series has the same labels in a other order, pandas reorders it to match. Which is correct and isn't what spot-based intuition expects. If the Series is missing some labels, those rows get `NaN`. If it has extra labels, they're dropped.

Assigning a **list** or a NumPy array has no index to align on. It goes in by spot. The length must match just or it raises.

That gap means `df["x"] = some_series` and `df["x"] = some_series.values` can give other columns from the same data. The first is often what you want. The second is the escape hatch when you know the order is right and the labels aren't.

## The filtered-assignment trap

The most common real instance:

```python
sub = df[df["city"] == "pune"]
df["doubled"] = sub["sales"] * 2
```

`sub` has only the Pune rows. The found Series has only those labels. Alignment fills every other row with `NaN`.

pandas did just what it promises. The author expected "find for these rows and leave the others alone". This Is a other step:

```python
df.loc[df["city"] == "pune", "doubled"] = df["sales"] * 2
```

The gap is visible when the column **already exists**. Whole-column set replaces the entire column. Rows absent from the subset are overwritten with `NaN`. Even if they held a just right good value a moment ago. The `.loc` form touches only the selected rows and leaves the rest alone.

When the column does *not* already exist, both forms leave `NaN` in the unselected rows. Creating a column has to put a thing in each row. If you want a default there, create the column first and then overwrite the subset. Which is just what the editor above does.

## Dropping

`df.drop(columns=["b"])` and `df.drop(index=[0])` both return a new frame.

The `axis=` form works and is older. `columns=`/`index=` say what they mean and are worth preferring.

A name that doesn't exist raises `KeyError`. That is often helpful. It catches typos and stale column lists. And `errors="skip"` turns it off when dropping optional columns.

To drop in place, reassign: `df = df.drop(columns=["b"])`. The `inplace=True` arg exists. Is discouraged: it doesn't well avoid a copy, it breaks chaining. It returns `None`. This Makes `df = df.drop(..., inplace=True)` a silent way to destroy your frame.

## Renaming

`df.rename(columns={"a": "alpha"})` takes a mapping, and `columns=str.upper` takes a function applied to each name.

The key quirk: **keys that don't match anything are skipped silently**. A typo in the old name does nothing at all and gives no indication. When a rename appears not to have worked, a misspelled key is the first thing to check.

`df.columns = [...]` replaces each name at once and needs the right length. It's blunter and, for a full rename, clearer.

For cleaning up messy headers, a function is often better than a mapping:

```python
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
```

That handles the whole frame without listing each column. Is worth running on anything that came from a spreadsheet.

## Adding several columns at once

`assign` takes any number of keyword args. They're applied in order. Later ones can use earlier ones:

```python
df.assign(
    total=lambda d: d["qty"] * d["price"],
    with_tax=lambda d: d["total"] * 1.18,
)
```

For column names that aren't valid identifiers. A space, a leading digit. Keyword args won't work. Bracket set is the only option. That is a fair arg for norming column names early.

Assigning a few columns from one step is the case `assign` handles less well. When a function returns a few values per row, a common pattern is:

```python
df[["a", "b"]] = df["text"].str.split("-", expand=True)
```

The right-hand side must have the same number of columns as the left, and the index must align.

## Reordering

Column order is insertion order, and there's no `reorder` method.

Three ways, in growing robustness:

`df[["b", "a", "c"]]` &mdash; select in the order you want. Fails loudly if a name is wrong. This Is often a feature.

`df.insert(pos, name, values)` &mdash; place one column at a spot, in place.

Building the order from what exists:

```python
first = ["id", "date"]
df = df[first + [c for c in df.columns if c not in first]]
```

That pins the columns you care about to the front and keeps the rest, without breaking when the schema changes.

## Removing columns safely

`drop(columns=[...])` raises on a name that doesn't exist. This Catches typos and stale lists.

`errors="skip"` suppresses that, and is right when the columns are truly optional. Dropping debug fields that may or may not be present.

`df.drop(columns=df.filter(like="tmp_").columns)` drops by pattern. This Lives changes in the exact names.

For keeping rather than dropping, selecting is clearer: `df[["a", "b"]]` states what you want rather than what you don't. Doesn't need updating when new unwanted columns appear.

## A note on inplace

Most of these methods take `inplace=True`. It's worth being clear about why it's discouraged.

It does **not** well avoid a copy. The speed arg for it's largely false.

It returns `None`, so `df = df.drop(columns=["a"], inplace=True)` silently sets `df` to `None`. A mistake that is easy to make and confusing to debug.

It breaks method chaining.

And it's on the way out: the pandas team has discussed dropping it. Copy-on-write makes its left rationale weaker.

Reassignment &mdash; `df = df.drop(columns=["a"])` &mdash; is clearer and no slower .

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

This handles trailing spaces, capitals, punctuation and units-in-parentheses in one pass. Doesn't need to know what the columns are called.

Doing it at once after loading means each later link uses predictable names. It drops the class of bug where a column name has an invisible trailing space.

`df.rename(columns=..., errors="raise")` makes a mapping strict. A key that matches nothing raises instead of doing nothing silently. That is worth using when the rename is key.

## Creating columns conditionally

The three standard shapes, none of which needs `apply`:

**Two branches** &mdash; `np.where(cond, a, b)`.

**a few branches** &mdash; `np.select([c1, c2], [v1, v2], default=v3)`, checked in order.

**Numeric bands** &mdash; `pd.cut`.

**A lookup** &mdash; `df["k"].map(mapping)`.

For a column that exists only for some rows, create it with a default first and then overwrite the subset:

```python
df["band"] = "unknown"
df.loc[df["score"] >= 80, "band"] = "high"
```

That avoids the `NaN` that appears when a column is created right for a subset. It makes the default clear rather than implied.

## Types when adding a column

A new column takes its dtype from what you assign. Two cases are worth watching.

Assigning a Python list of ints gives `int64`. Assigning one with a `None` in it gives `object` or `float64`. If the column is meant to be a nullable int, say so: `pd.array([1, None], dtype="Int64")`.

Assigning a string to a subset of a numeric column upcasts the **whole** column to `object`, silently. This Makes each later numeric step on it slow or wrong. If a column may hold either, that is often a sign it should be two columns.

## Dropping rows

`drop(index=[...])` drops by label. This Is fine for a handful of known labels and awkward else.

For a rule, filtering is clearer: `df[~mask]` says "all except". Doesn't need knowing the labels.

`df.drop(df[mask].index)` works and is a longer way of writing the same thing.

`dropna`, `drop_duplicates` and `query` cover the common cases right. Each says what it does in its name.

## A summary

`df["new"] = ...` adds or silently replaces.

`assign` returns a new frame and chains. Use a lambda inside a chain.

Assigning a **Series** aligns on the index. A **list** goes in by spot.

Whole-column set from a subset overwrites the unmatched rows with `NaN`. `.loc` touches only the pick.

`drop(columns=...)` raises on a missing name unless `errors="skip"`.

`rename` skips keys that match nothing. So A typo does nothing at all.

Norm column names once, at load, with a function over `df.columns`.

And prefer reassignment to `inplace=True`. This Doesn't do what its name suggests.

## A closing note

Adding a column looks like the simplest thing in pandas and carries two traps.

The first is silence: assigning to an existing name replaces it without a word. A rename with a misspelled key does nothing without a word. Neither raises. Both are easy to miss in a long script.

The second is alignment. A Series assigned to a column is matched by label, not spot. A value found from a filtered subset fills the unmatched rows with `NaN`. And if the column already existed, it overwrites what was there. A plain list, having no index, goes in positionally instead. Two lines that look equal behave differently.

The defences are small: use `.loc` when you mean "these rows only", check the column list after a rename. Norm column names once at load so that later links are predictable.

## One more thing

`df.pop("col")` drops a column and returns it. This Is at times the clearest way to move a column out of a frame and into a var in one step.

And `df.drop` accepts `level=` for a MultiIndexed frame. A whole outer group can be removed by label without building a mask. Both are small conveniences. Both read better than the two-step options when the intent is just what they show.

## In summary

Adding and dropping columns is mechanically simple. The two things that bite are both about silence.

Nothing warns when you overwrite a column by reusing its name. Nothing warns when a rename key matches nothing. Both leave the frame in a state that looks correct.

And set is governed by alignment: a Series matches on labels, a list matches on spot. A whole-column set found from a subset overwrites each unmatched row with `NaN`. Including rows that held a just right good value a moment before.

Using `.loc` when you mean "these rows only", norming column names once at load. Checking the column list after a rename cover all of it.
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
intro: object, group and the nullable types.

## Why this matters early

A frame that doesn't fit in memory can't be analysed at all. The usual reason a frame is larger than expected isn't the number of rows. It's one or two columns stored in the widest possible type.

Fixing dtypes is often the gap between a dataset that loads and one that doesn't. It takes one line per column.

## object is the expensive one

A column of strings has dtype `object`. That means an array of **pointers**, each leading to a split Python string one spot else in memory.

Two costs follow. The obvious one is memory. A pointer plus a Python string object plus the characters, against a few bytes for a number. The less obvious one is speed. Steps on object columns fall back to per-element Python. This Is the same reason `apply` is slow.

`df.memory_usage()` reports **8 bytes per pointer** and stops there. For a text column that is a wild underestimate. `df.memory_usage(deep=True)` follows the pointers and reports the truth. The gap between the two numbers is often a factor of ten.

`df.info(memory_usage="deep")` gives the same accounting alongside the dtypes.

Always use `deep=True` when looking at a frame with text in it. The shallow number is close to meaningless there.

## category

When a text column has few distinct values scaled to its length. A city, a status, a product code. `group` is the fix.

It stores the distinct values once in a lookup. One small int code per row. A column of 30,000 rows drawn from four cities goes from storing 30,000 strings to storing four strings and 30,000 one-byte codes.

The savings are large, and they compound: group-by and compare on a group are faster too. They operate on the codes.

The rule is repetition. A column where each value is distinct. An email address, a UUID. Costs **more** as a group. You store the codes plus all the first values. The rule of thumb is that it pays when the number of distinct values is well under half the row count. It pays enormously when it's a tiny fraction.

Two actions to know. groups carry an order if you give them one. This Is what makes sorting by a grade or a size work properly. And steps that give a value outside the group set give `NaN` rather than extending the set. This Is at times surprising and often the safer default.

## Downcasting numbers

`int64` holds numbers up to about 9.2 quintillion. A column of ages doesn't need that.

`pd.to_numeric(s, downcast="int")` picks the narrowest signed type that fits. `downcast="unsigned"` does the same for non-minus data, and `downcast="float"` gives `float32`.

The saving is up to 8x for ints and 2x for floats.

The caution is the same as NumPy's: narrow int types **wrap silently** on overflow. Downcast when the range is truly bounded. Ages, day-of-month, a small enum. And leave counters and identifiers alone. An `int8` column that later receives 200 doesn't give you 200.

## Nullable dtypes

The oldest wart in pandas is that a NumPy int array can't represent a missing value. An int column with one gap turns `float64` and identifiers start printing as `1001.0`.

The nullable extension types fix this. `Int64` with a **capital I** is a other dtype from `int64`. It holds ints and missing values together. The missing marker is `pd.NA` rather than `np.nan`.

`Float64`, `boolean` and `string` are the equivalents for the other kinds. The nullable `boolean` is truly handy. Plain `bool` columns also collapse to `object` when they gain a missing value.

They aren't the default, and there are corners where a library downstream expects NumPy types and doesn't handle them. But for identifiers and counts that must not become floats, they're the right answer.

`pd.NA` passes through math like NaN. Checks with it return `pd.NA` rather than `False`. A gap from NaN that matters if you're filtering on such a column.

## Converting safely

`astype(int)` raises on the first value it can't convert. The message doesn't tell you which row.

`pd.to_numeric(s, errors="coerce")` converts what it can and turns the rest into `NaN`. That is often the better tool for real data. It lets you find the offenders:

```python
converted = pd.to_numeric(s, errors="coerce")
bad = s[converted.isna() & s.notna()]
```

Those are the rows that were present and unconvertible. The stray `"N/A"`, the number with a thousands separator, the value with a trailing space.

`errors="raise"` is the default and is right when the data is supposed to be clean and you want to know at once if it isn't.

## A practical routine

After loading anything:

```python
df.info(memory_usage="deep")
```

Then, for each `object` column, `nunique()` against `len(df)`. Anything with heavy repetition turns a `group`. Anything numeric-looking gets `to_numeric`. Anything that is an identifier gets `str` at read time so its leading zeros live.

That is often a handful of lines. On a large frame it routinely cuts memory by more than half.

## Seeing where the memory goes

`df.memory_usage(deep=True).sort_values(ascending=False)` ranks the columns. On most real frames one or two text columns dominate, and all else is noise.

That ranking tells you where to spend effort. Converting a column that holds 2% of the memory isn't worth the risk of changing a dtype.

`df.info(memory_usage="deep")` gives the same data alongside dtypes and null counts. This Is often the more convenient single call.

## Categories in more detail

`astype("group")` builds the group set from the values present.

Two results follow from the set being fixed.

**Assigning a value outside the set fails** or makes `NaN`, based on the step. Adding a new city to a cat column needs `cat.add_categories` first.

**Mixing two cats with other sets** gives `object` unless the sets match. This bites when concatenating frames from other files, each of which saw a other subset of the groups. `pd.api.types.union_categoricals` handles it, or convert after concatenating rather than before.

`cat.set_categories([...], sorted=True)` gives an order. This Is what makes sorting by size or grade work right rather than alphabetically. `cat.as_ordered()` and compare ops then behave as you'd expect.

`cat.remove_unused_categories()` shrinks the set after filtering. This Else keeps each first group and can leave empty groups in a group-by.

Group-by on a cat includes **each** group by default, even absent ones, making rows of zeros. `seen=True` restricts it to groups really present. It's worth passing on purpose since the default has changed across versions.

## What float32 costs

`float32` halves memory and keeps about seven large digits.

For data that came from a sensor with three, that is ample. For building up a long sum it isn't. The fix is to build up in a wider type: `s.sum(dtype="float64")` reads a narrow column and adds in a wide accumulator.

`float16` exists and is rarely a good idea outside deep learning. Three large digits isn't much. Most steps upcast it anyway.

## Nullable types in practice

The extension types &mdash; `Int64`, `Float64`, `boolean`, `string` &mdash; fix the missing-value gaps in the NumPy-backed dtypes.

Three hands-on notes.

`pd.NA` passes through checks as `pd.NA` rather than `False`. Filtering a nullable column so needs care: `df[df["x"] > 1]` drops the missing rows either way. A mask holding `pd.NA` can't always be used right. `.fillna(False)` on the mask is the fix.

Some libraries downstream expect NumPy dtypes and don't handle extension types. Converting back with `astype("float64")` at the boundary is at times needed.

`convert_dtypes()` converts a whole frame to the best on hand nullable types in one call. This Is a quick way to see what it would look like.

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

The threshold is a judgement rather than a rule. Well under half distinct is a clear win. Near half is marginal. Mostly distinct is a loss.

And the general principle from the numpy track applies here too. Set the dtype as early as possible, ideally at read time. Each conversion later allocates a second copy of the column.

## A diagnosis routine

When a frame is unexpectedly large or slow, four lines find the cause:

```python
df.info(memory_usage="deep")
df.memory_usage(deep=True).sort_values(ascending=False).head()
df.select_dtypes("object").nunique()
df.select_dtypes("object").apply(lambda s: s.str.len().mean())
```

The first two find which columns dominate. The third says whether they're picks for `group`. Low cardinality. Or identifiers that won't gain. The fourth shows mean string length. This Shows a column that is large despite having few rows.

Almost always the answer is one or two `object` columns. Almost always one of them should be a group.

## dtype mistakes that cause wrong answers

Memory is the visible cost. These are the ones that change results.

**An identifier read as an int** loses leading zeros. Two other ids can collide once the zeros are gone.

**A numeric column stored as `object`** checks as strings: `"100" < "20"` is True. Sorting, compare and `max` all silently give the wrong answer, and nothing raises.

**A narrow int that overflows** wraps. `int8` holding 200 doesn't hold 200.

**Mixed types in one column** make it `object`. Any aggregation either fails or makes a thing meaningless.

**A float used as a key** in a merge or a group-by. Floating-point equality is unreliable. Two values that print the same way may not match.

Each of these is caught by looking at `dtypes` at once after loading. This Is why that habit appears in three split modules.

## When to convert

**At read time** if you can. `dtype=` in `read_csv`. No extra copy, no window where the column is wrong.

**at once after loading** else, before any analysis. Each later step sees the right types.

**Not again and again.** Each `astype` allocates a full copy of the column. Converting inside a function that runs per group or per file is a common and invisible cost.

## A summary

Text columns hold pointers. Use `deep=True` to see their real size.

`group` for repeated values, and only for repeated values.

Downcast numerics when the range is truly bounded.

`Int64`, `boolean` and `string` hold missing values without changing type.

`to_numeric(errors="coerce")` converts what it can and shows you what it couldn't.

Set types as early as possible. Check `dtypes` right after loading. It's one line and it blocks a group of silent wrongness.

## A closing note

Dtypes are the quiet determinant of whether a pandas script is fast, correct. Able to load its data at all.

The memory story is simple: text columns hold pointers to Python strings and dominate most real frames, `group` merges them when values repeat. Narrow numeric types halve or quarter the rest. Two loops run once after loading routinely cut a frame's footprint in half.

The correctness story matters more. A numeric column stored as `object` checks as strings. `"100" < "20"` is true and each sort and max is silently wrong. An identifier read as an int loses its leading zeros permanently. An int column with one gap turns float. Ids start printing with a decimal point.

None of those raise. All of them are visible in one line of `df.dtypes`, run at once after loading. Which is why that habit appears in a few modules and is worth more than any other single check in this track.
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

pandas has more than one form of "missing", for historical reasons.

`np.nan` is a float. It's what you get in numeric columns. It's why an int column with a gap turns `float64`.

`None` is Python's null. In an `object` column it stays `None`. In a float column it's converted to `NaN` on the way in.

`pd.NA` is the newer, dtype-agnostic marker used by the nullable extension types (`Int64`, `boolean`, `string`).

You rarely need to care which one you've. `isna()` and `notna()` handle all three. Use them rather than `== None` or `== np.nan`, neither of which works. `NaN` isn't equal to anything, including itself.

The one place the gap bites: checks with `pd.NA` return `pd.NA` rather than `False`. Filtering a nullable column can behave differently from filtering a float one.

## Count first

Before choosing a plan, get three numbers:

`df.isna().sum()` &mdash; how many are missing in each column.

`df.isna().mean()` &mdash; the same as a proportion. This Is far easier to judge.

`df.isna().any(axis=1).sum()` &mdash; how many rows would be lost to `dropna()`. This is often much larger than any single column's count. Other rows are missing other things.

Those three numbers make the choice. Dropping 2% of rows is a rounding error. Dropping 40% changes what the dataset is. A column that is 60% empty probably shouldn't be used at all. No amount of imputation fixes that.

## dropna

The default is stricter than most people expect: `df.dropna()` drops a row if **any** value in it's missing.

`how="all"` only drops rows that are fully empty. This Is the right tool for trailing junk from a spreadsheet export.

`thresh=n` keeps rows with at least `n` non-missing values.

`subset=["a", "b"]` only considers those columns. This Is often what you really want. You care that the key fields are present, not that each optional field is.

`axis=1` drops columns rather than rows. This Is the blunt way to drop mostly-empty fields.

## fillna

The code is easy. The choice is a statistical choice, and it isn't neutral.

**Zero** shifts the mean toward zero. For a count where missing truly means none, it's correct. For a reading where missing means unknown, it invents data and biases each summary.

**The mean** preserves the mean by build and **shrinks the variance**. You're adding points with no spread. Anything downstream that cares about dispersion. A standard deviation, a trust interval, a model that weights by variance. Is then quietly wrong. The fourth editor measures this.

**The median** is more robust to outliers and has the same variance problem.

**A sentinel** like `-1` is honest for cat codes but must be documented, or someone will mean it.

**Group-wise fills** &mdash; filling with the mean of the same city, or the same product &mdash; are often better than a global fill. They use data you really have.

## Filling from neighbours

For sorted data, adjacency carries meaning and the neighbouring value is often the best guess.

`ffill()` carries the last known value forward. This is the standard treatment for a sensor reading or a price that is only recorded when it changes.

`bfill()` carries the next value backward.

Both leave an edge unfilled. `ffill` can't fill a leading gap, `bfill` can't fill a trailing one &mdash; which is worth checking rather than given the column is now full.

`limit=n` caps how far a value travels. Without it, a single reading can pass across a gap of any length. This Turns one reading into a hundred fabricated ones.

`interpolate()` fits between the nearby values rather than repeating one. Takes a `method` for the shape of the fit. It needs a real order. It belongs on time series and not on any rows.

Note that `fillna(method="ffill")` is deprecated. `ffill()` is the current spelling.

## Missingness as information

The most often missed point: **why** a value is absent often matters more than what you replace it with.

If a value is missing at random, dropping or imputing is defensible. If it's missing *because of what it would have been*. A sensor that fails at extremes, an income question people skip when the answer is embarrassing, a test not run because the patient was too ill. Then both dropping and imputing bias the result, in opposite directions.

The last editor shows the extreme case: a column that is missing just when another column takes a given value. Filling it with the mean would erase the most helpful thing in the data.

Adding an indicator column &mdash; `df["x_missing"] = df["x"].isna().astype(int)` &mdash; keeps that data while still allowing a fill. It costs one column and is often the single most handy feature in a model built on messy data.

## A working order

Count. Look at *which* rows are missing, not just how many. Ask whether the missingness looks random. Add an indicator if it doesn't. Then choose a fill. Write down which one you used. Because by the time someone asks, the code will have moved on.

## Where missing values come from

Knowing the source often tells you what to do.

**Not collected** &mdash; the question wasn't asked, the sensor wasn't installed. Often missing at random. Dropping is defensible.

**Not applicable** &mdash; a spouse's name for an unmarried person. Not missing at all. A sentinel or a split flag is more honest than `NaN`.

**Failed** &mdash; a sensor error, a timeout. often linked with the value. So not missing at random.

**Created by an step** &mdash; a join that didn't match, an alignment mismatch, a `shift`, a `pct_change` on the first row, a value outside a `cut` range. These are the ones people mistake for data problems when they're really code problems.

That last group is worth checking first. If a column gained missing values partway through a pipeline, the cause is upstream in the code, not in the source data.

## Missing values in operations

Most aggregations **skip** missing values by default: `sum`, `mean`, `max` all use `skipna=True`.

That is other from NumPy. Here A single `NaN` poisons the whole reduction. It's worth knowing because it changes the denominator. `df["x"].mean()` cuts by the number of **present** values, not the row count.

`skipna=False` makes them pass. This Is at times what you want when a missing value should invalidate the result.

`sum()` of an all-missing column returns `0`, not `NaN`. This Is defensible and surprising. `min_count=1` makes it return `NaN` instead.

`groupby` **drops** rows whose key is missing, unless `dropna=False`.

`merge` treats `NaN` keys as non-matching often.

Sorting puts them last even so of direction.

Each of these is fair in alone. Together they mean missing data quietly changes a few numbers at once, and the totals stop merging.

## Filling within groups

A global fill uses the least data on hand. A group fill uses more:

```python
df["temp"] = df["temp"].fillna(df.groupby("city")["temp"].transform("mean"))
```

Each missing temp gets the mean for its own city rather than the mean of all over.

The same pattern works with `median`, with `ffill` inside a group (`df.groupby("id")["v"].ffill()`). With a lookup from another table.

A group fill leaves gaps where a whole group is missing. A global fallback later is often needed:

```python
filled = df.groupby("city")["temp"].transform("mean")
df["temp"] = df["temp"].fillna(filled).fillna(df["temp"].mean())
```

## Documenting what you did

The part that is easy to skip and matters most later.

Record, in the code and in what the output is:

How many values were missing per column, before you touched them.

What you did &mdash; dropped, filled with what, interpolated how.

Whether you added an indicator.

a filled value is the same from a measured one once it's in the frame. Six months later, no one can tell which numbers were seen and which were invented. The analysis can't be copied or corrected.

A frame with an `x_imputed` boolean column carries that data with the data. This Is more robust than a comment.

## The order to work in

Count them. Look at which rows they're in. Decide whether the missingness looks random. Add an indicator if it doesn't. Choose a plan for each column apart. There's no reason the same one suits each column. Record what you did. Then proceed.

## Missing values that pandas created

Worth a split checklist, because these are code problems rather than data problems and the fix is upstream.

**A join that didn't match**. The added columns are `NaN` for unmatched rows. `indicator=True` confirms it.

**Alignment on set** &mdash; a Series with other labels assigned to a column fills the unmatched rows.

**`shift`, `diff`, `pct_change`** &mdash; the first row of each has no predecessor.

**`rolling`** &mdash; leading rows before the window fills.

**`cut` or `qcut`** &mdash; values outside the bin edges.

**`reindex` or `unstack`** &mdash; mixes that didn't occur in the data.

**`resample` upsampling** &mdash; periods with no finding.

If a column gained missing values partway through a pipeline, one of these is the cause. Filling them is treating a symptom.

## Interpolation options

`interpolate()` defaults to `method="linear"`. This Treats the values as evenly spaced even so of the index.

`method="time"` uses the actual time gaps. This Is what you want on an irregular time series. Without it, a value after a three-week gap is weighted the same as one after an hour.

`method="nearest"`, `"polynomial"`, `"spline"` fit other shapes. The last two need an `order`.

`limit_direction` controls whether leading and trailing gaps are filled. By default `interpolate` fills forward only. A leading `NaN` lives.

`limit_area="inside"` restricts filling to gaps between real findings. This Is often the honest choice. Interpolating beyond the ends of your data is extrapolation. It should be a deliberate choice rather than a default.

## Choosing per column

There's no reason one plan suits each column, and treating them uniformly is often wrong.

An **identifier** with gaps is a data problem. The rows probably can't be used.

A **group** can take an clear `"unknown"` level. This Is honest and keeps the rows.

A **count** where missing means none takes zero.

A **reading** takes a group mean, an blending, or nothing. Based on why it's missing.

A **timestamp** rarely takes a fill at all. A missing date often means the event didn't happen.

Writing the choice down per column, in code, is more maintainable than a single `fillna(0)` across the frame. Which is the most common and least defensible choice.

## A summary

`isna()` finds all three markers. Equality never works.

Count per column, as a share, and count the rows you'd lose, before deciding anything.

`dropna()` drops on **any** missing value. `subset=` is often what you want.

Zero shifts the mean. The mean shrinks the variance. Neither is neutral.

`ffill`/`bfill` for sorted data, with a `limit`.

`interpolate(method="time")` for irregular series.

Group fills use data a global fill discards.

Add an indicator when missingness might be helpful &mdash; it often is.

And record what you did. A filled value is the same from a measured one the moment it enters the frame.

## A closing note

Handling missing data is the part of this track where the code is easiest and the choices are hardest.

`isna`, `dropna` and `fillna` take a few minutes to learn. What they can't tell you is whether the values are missing at random, whether the rows you're about to drop share a thing, or whether filling with a mean is defensible for this given column.

Those are questions about the data rather than about pandas. The honest answer is often that missingness is helpful. That a value is absent just because of what it would have been. In that case both dropping and imputing bias the result. An indicator column preserves the signal that filling would erase.

The hands-on min is: count them per column and as a share, look at which rows they're in, choose per column rather than uniformly. Record what you did. Because once a filled value is in the frame, nothing sets apart it from a measured one.
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

`df.duplicated()` returns a boolean Series: `True` for a row that has been seen before, `False` for its first case.

That skew is deliberate. It means `df[~df.duplicated()]` keeps just one of each. `df[df.duplicated()]` shows you what would be removed.

`keep` controls which case is treated as the first:

`keep="first"` (the default) flags each copy after the first.

`keep="last"` flags each copy before the last.

`keep=False` flags **all** of them, including the first. This is the one to use when inspecting. It shows you the full groups rather than half of each.

## subset is the important argument

Whole-row copies &mdash; each column same &mdash; are the easy case and often not the real one.

The question that often matters is whether a **key** is repeated. Two rows with the same customer id and other scores aren't same rows. They may well be a data problem.

`df.duplicated(subset=["id"])` asks that question. Mixed with `keep=False`, it shows you each conflicting group:

```python
df[df.duplicated(subset=["id"], keep=False)].sort_values("id")
```

That is the first thing to run when a key is supposed to be unique and a thing downstream suggests it isn't.

## Order decides what survives

`drop_duplicates` keeps the first matching row **in the frame's current order**.

That order is what the data happened to arrive in. If the rows represent versions of a record and you want the newest, keeping the first is any. It will be right at times and wrong at times. Nothing will tell you which.

Sort on purpose first:

```python
df.sort_values("updated").drop_duplicates(subset=["id"], keep="last")
```

Now "the newest per id" is what the code says. It doesn't depend on how the file was written.

This is one of the most common silent errors in data cleaning. The result always looks plausible. You asked for one row per id and you got one row per id.

## Near-duplicates

Exact matching misses the copies that really occur in real data.

`"Pune"`, `"pune "` and `"PUNE"` are three distinct values to pandas and one city to all else. So are `"Ltd"` and `"Ltd."`, or a name with a double space.

Norm before deduplicating:

```python
df["city"] = df["city"].str.strip().str.lower()
```

`value_counts()` on the column before and after is the quickest way to see how much gap it made. To spot the variants you had not thought of.

For truly fuzzy matching &mdash; misspellings, transpositions &mdash; pandas has nothing built in. The answer is a dedicated library. But stripping and lowercasing catches the large majority of real cases and costs one line.

## Sometimes the repeat is the data

Not each repeated value is an error. Five orders from the same customer are five orders.

The tell is whether the rows carry split data. If the copy rows differ in a real column, dropping them destroys data. The step you want is an aggregation:

```python
orders.groupby("customer", as_index=False).agg(
    orders=("amount", "size"),
    total=("amount", "sum"),
)
```

That merges each customer to one row and keeps what the repeats were telling you.

Reaching for `drop_duplicates` when you meant `groupby` is a quiet way to lose most of a dataset.

## Assert uniqueness where you assume it

`s.is_unique` is a cheap check, and `df.index.is_unique` covers the index.

Where a key is supposed to be unique. Because it's a main key, or because a later merge depends on it. An clear assertion is worth the line:

```python
assert df["id"].is_unique, "id must be unique"
```

The reason is exact: a duplicated key on either side of a `merge` silently times rows. Ten thousand rows join to eleven thousand, no one notices. Each later sum is inflated. `merge(..., validate="one_to_one")` catches it at the join. Asserting earlier catches it closer to the cause.

## Duplicates as a data-quality signal

A copy is rarely just a copy. It often means one of a small number of things. Finding which changes what you should do.

**A repeated load.** The same file processed twice, or an append that ran again. Whole-row copies, exact. Safe to drop.

**A join that times'd rows.** copies in some columns and not others, appearing only after a merge. The fix is at the merge, not here.

**Genuine repeated events.** Two orders from the same customer. Not copies at all. Aggregate rather than drop.

**Multiple versions of a record.** Same key, other timestamps. Keep one. *which* one matters &mdash; sort first.

**Near-copies from inconsistent entry.** Same entity, other spelling. Norm first, or you'll keep both.

Running `df.duplicated().sum()` and `df.duplicated(subset=[key]).sum()` and checking the two numbers often tells you which case you're in.

## Finding what differs

When a key is duplicated but the rows aren't same, the handy question is which columns disagree:

```python
dupes = df[df.duplicated(subset=["id"], keep=False)].sort_values("id")
```

Sorting by the key puts the conflicting rows next to each other. This Makes the differing column obvious by eye on a small number of groups.

For a systematic answer, group by the key and count distinct values per column:

```python
df.groupby("id").nunique().max()
```

Any column with a max above 1 disagrees one spot. That points straight at the columns worth investigating.

## Deduplicating with a rule

"Keep the newest" is the most common rule, and it's two steps:

```python
df.sort_values("updated").drop_duplicates(subset=["id"], keep="last")
```

"Keep the most full" is a other rule and needs a helper column:

```python
df.assign(filled=df.notna().sum(axis=1))
  .sort_values("filled")
  .drop_duplicates(subset=["id"], keep="last")
```

"Merge the rows" &mdash; taking the first non-missing value of each column &mdash; is a group-by:

```python
df.groupby("id", as_index=False).first()
```

`first()` skips missing values, so it mixes partial records rather than picking one. That is often what people really want when they reach for `drop_duplicates`.

## Duplicated columns and index labels

copy **column names** are legal and cause real confusion: `df["a"]` returns a DataFrame rather than a Series when two columns are called `a`.

`df.columns.duplicated()` finds them, and they often arrive from a merge with shared names or a bad header row.

`df.loc[:, ~df.columns.duplicated()]` keeps the first of each.

copy **index labels** have the same problem for row pick. `reset_index(drop=True)` is the usual fix.

## Before a join, always

The single highest-value use of all in this module is the check before a merge:

```python
assert df["id"].is_unique
```

on whichever side is supposed to be unique.

A copy there times rows silently, inflates each later total. Is invisible in the output. Checking costs one line. `merge(..., validate="many_to_one")` makes the check part of the step itself.

## Duplicates and the index

Row copies and **index** copies are other problems with other symptoms.

A duplicated index makes `.loc[label]` return a few rows where code expects one, breaks `reindex`, and makes some joins raise.

`df.index.is_unique` checks it. `df[df.index.duplicated(keep=False)]` shows the offenders. `reset_index(drop=True)` fixes it when the labels carry no meaning.

Duplicated index labels often arrive from `concat` without `ignore_index=True`, or from `explode`, or from a group-by result that was reshaped. None of them warns.

## Fuzzy duplicates

Exact matching finds only the easy cases. Real copy records differ in ways that need judgement:

Whitespace and case &mdash; fixed by norming, and worth doing always.

Punctuation &mdash; `"Ltd"` and `"Ltd."`.

Abbreviations &mdash; `"Street"` and `"St"`.

Transpositions and typos &mdash; truly fuzzy.

other formats for the same value. Phone numbers, dates as text.

pandas handles the first two well and the rest not at all. For the rest, the honest options are a scaling function encoding the domain's rules, or a dedicated record-linkage library. What doesn't work is hoping `drop_duplicates` will catch them.

The hands-on approach: norm aggressively into a **split** key column, deduplicate on that. Keep the first values. That way the matching is clear and the data isn't damaged.

## Counting rather than removing

Before dropping anything, it's worth knowing what the copies represent:

```python
counts = df["id"].value_counts()
counts[counts > 1]
```

If most keys appear once and a few appear twice, that is probably a data-entry issue. If each key appears just three times, the data has a structure you haven't accounted for. Three records per entity, perhaps one per year. And deduplicating would destroy it.

That gap isn't visible from the copy count alone. It changes the correct action fully.

## A summary

`duplicated()` flags repeats but not the first. `keep=False` flags each copy.

`subset=` asks the question that often matters: is the **key** duplicated?

`drop_duplicates` keeps the first in current order. Sort first if which lives matters.

Norm case and whitespace before deduplicating.

Repeated rows carrying split data want `groupby`, not `drop_duplicates`.

`groupby(...).first()` merges partial records rather than picking one.

And assert uniqueness before any merge that depends on it. A duplicated key there times rows and inflates each total downstream.

## A closing note

The word "copy" hides a few other situations. Choosing the right action depends on which one you've.

An exact repeated row from a double load can be dropped without thought. Two versions of a record need a sort and a rule about which lives. Repeated events carrying split data need aggregating, not dropping. Near-copies from inconsistent text need norming first, or they won't be found at all.

The diagnostic that splits them is checking whole-row copies against key copies. If the key repeats but the row doesn't, a thing differs between the copies. That gap is the thing to look at before deciding anything.

And the highest-value use of all here is the check before a join. A duplicated key times rows, inflates each total downstream. Makes output that looks fully fair. One assertion blocks it.

## Two more things worth knowing

`drop_duplicates` accepts `ignore_index=True`, which renumbers the result rather than leaving gaps in the index where rows were removed. Without it the surviving labels are the first ones, which is correct and at times surprising when the result is printed.

`df.duplicated()` checks whole rows including `NaN`. Two rows with a missing value in the same column **do** count as copies of each other. Unlike almost all over else in pandas. Here `NaN` never equals `NaN`. That inconsistency is deliberate and handy here. Two the same way incomplete rows often are copies.

And for finding copies across a subset of columns while keeping the rest, `df.groupby(keys).filter(lambda g. Len(g) > 1)` returns each row belonging to a repeated key. This Is the inspection view that `keep=False` gives more right.

## Deduplicating across sources

The hardest version of this problem isn't copies within one table but the same entity appearing in two.

The steps are always the same, and only the third is hard.

**Norm** both sides into a close key. Case, whitespace, punctuation, and any domain-exact standardisation.

**Match** on the key, with `merge` or `isin`.

**Decide** what to do with near-matches that the key doesn't unify.

pandas handles the first two well. The third is record linkage. It's a truly open problem for messy data. The same person may appear with a other spelling, a maiden name, a typo'd date of birth.

The pragmatic middle ground is to match just on a normed key, count how many records fail to match. Inspect a sample of those. Often a small number of scaling rules. Drop punctuation, standardise abbreviations. Resolves most of them. The rest are truly ambiguous and better flagged for a human than resolved by code.

## In summary

`duplicated` flags each copy but the first. This Is what makes it a drop mask. `keep=False` flags them all. This Is what you want for inspection.

The question that matters is often about the **key** rather than the whole row, and `subset=` asks it.

Sort before dropping, or which row lives is any. Norm text first, or the same value counts as a few. And if the repeated rows carry split data, the step you want is an aggregation, not a deletion.
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

A Series of strings is a column of Python string objects. You could loop over them. `apply(str.strip)` would work. Both are slow and neither reads well.

`.str` exposes the string methods so they apply to the whole column: `s.str.strip()`, `s.str.lower()`, `s.str.len()`.

Each returns a Series, so they chain: `s.str.strip().str.lower().str.replace(" ", "_")`.

The accessor is needed. `s.strip()` isn't the same thing. It either does a thing unrelated to the Series or fails. `strip` isn't a Series method. Losing `.str` is the most common beginner error here. The resulting `AttributeError` at least says so clearly.

## Missing values pass through

`.str` methods return `NaN` for missing input rather than raising or returning an empty string.

That is often right: the uppercase of an unknown value is unknown.

It turns a problem for **predicates**. `s.str.holds("a")` returns `True`, `False` **or `NaN`**. A mask holding `NaN` can't be used to index a frame. Pandas raises "Can't mask with non-boolean array holding NA / NaN values".

The fix is `na=False`. This Decides what a missing value should count as:

```python
df[df["name"].str.contains("ana", na=False)]
```

Pass it each time you filter on a text predicate. `na=True` is at times what you want, when missing should be included.

This is the single most common runtime error in text cleaning. It appears only when the data has a gap. So it often shows up in production rather than on the sample.

## Testing

`holds` searches anywhere in the string. `startswith` and `endswith` anchor. `match` anchors at the start, `fullmatch` at both ends.

**`holds` takes a regular formula by default.** That matters more than it sounds. It means `s.str.holds(".")` matches each non-empty string rather than finding a literal dot. `s.str.holds("a|b")` is an alternation rather than a search for the three characters.

Pass `regex=False` for a literal search. It's also faster.

`case=False` makes the test case-insensitive without a split `.lower()` pass.

`startswith` and `endswith` do **not** take a regex. This Is an inconsistency worth remembering rather than deriving.

## Splitting and extracting

`s.str.split("-")` gives a Series of lists. That is rarely what you want right.

`expand=True` turns it into a DataFrame with one column per piece. This Is how you split a mixed field into real columns. Rows with fewer pieces get `None` in the trailing columns.

`s.str.split("-").str[0]` takes one piece &mdash; the second `.str` indexes into the lists.

`extract` is often better when the structure is known. It takes a regex with capture groups and returns one column per group. Named groups become column names:

```python
s.str.extract(r"(?P<kind>[a-z]+)-(?P<num>\\d+)")
```

Rows that don't match give `NaN` across the row. This Makes non-matching input visible rather than silently mangled.

`extract` returns **text**, even for digits. Convert later with `pd.to_numeric` if you need numbers.

`extractall` returns each match rather than the first, with a MultiIndex.

## Replacing

`s.str.replace(old, new, regex=...)` needs the `regex` arg to be clear in pandas 2. The default changed. Code written against pandas 1 that leaned on the old action can silently do the wrong thing.

Two clean-ups earn their place in almost each script:

Merging whitespace: `s.str.replace(r"\\s+", " ", regex=True).str.strip()`.

Norming column names:

```python
df.columns = (df.columns.str.strip().str.lower()
              .str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_"))
```

That turns `"  First Name "` and `"AGE (years)"` into `first_name` and `age_years`. It handles a whole spreadsheet's worth of inconsistent headers without listing them.

Note `df.columns.str` works too &mdash; the column index is an Index. Index has a `.str` accessor as well.

## The cost

`.str` is a convenience, not a vectorisation.

Object columns hold pointers to Python strings. Each step walks them one at a time in Python. The last editor shows text work running far slower than math on the same number of rows.

Three things help.

**Do it once.** Clean text at load time rather than again and again inside a loop or a function called per group.

**Convert to `group`** when values repeat. steps then run on the small set of distinct values rather than each row.

**Consider the `string` dtype.** `astype("string")` gives the nullable extension type. This Has clearer missing-value semantics than `object` and is where pandas' future tuning work is going.

For very large text columns, the honest answer is that pandas isn't the right tool. The work belongs in a DB or a purpose-built library.

## The cleaning pipeline

Text from the real world needs the same handful of steps almost each time. Doing them in one pass at load time is far better than scattering them through the analysis:

```python
df["city"] = (df["city"]
              .str.strip()
              .str.lower()
              .str.replace(r"\s+", " ", regex=True))
```

Strip the ends, norm case, collapse inner whitespace. That alone resolves most of the "same value counted twice" problems that show up in a group-by.

For text that will be checked or joined on, consider also dropping punctuation and accents. `unicodedata.norm` handles accents. Pandas has no built-in for it. `.str.norm("NFKD")` plus an ASCII encode is the usual idiom.

## Extracting structure

`str.extract` with named groups is the most handy of the extraction methods. It names the outputs:

```python
df[["kind", "num"]] = df["ref"].str.extract(r"(?P<kind>[a-z]+)-(?P<num>\d+)")
```

Rows that don't match give `NaN` across the row. Counting them later tells you how well the pattern fits:

```python
unmatched = df["kind"].isna().sum()
```

That check is worth making. A regex that matches 90% of rows silently discards the other 10%. The only sign is a column with gaps.

`str.extractall` returns each match rather than the first, with a MultiIndex that has a `match` level.

`str.findall` returns a list per row. This Is harder to work with and at times what you want.

## Testing and counting

`str.holds` &mdash; anywhere, regex by default, needs `na=False` for filtering.

`str.startswith` / `str.endswith` &mdash; anchored, **no regex**.

`str.match` &mdash; anchored at the start, regex.

`str.fullmatch` &mdash; anchored at both ends.

`str.count(pattern)` &mdash; how many times a pattern occurs per row.

`str.len` &mdash; length, which is a quick way to spot truncated or padded fields.

A frequent need is "does this hold any of these words":

```python
df["text"].str.contains("|".join(words), case=False, na=False)
```

Building an alternation is fine for a handful of words. For a long list. For whole-word matching, it's worth escaping the parts with `re.escape` and adding word boundaries, or the results will surprise you.

## Splitting into columns

`str.split(sep, expand=True)` gives a DataFrame. Rows with fewer parts get `None` in the trailing columns. Rows with more parts are **truncated** unless you pass `n` to limit the splits.

`n=1` splits only on the first separator. This Is what you want for `key. Value` text where the value may hold the separator.

`str.rsplit` splits from the right. This Handles "all before the last dot" cleanly.

`str.split` returns just three columns. Before, separator, after &mdash; which avoids the var-width problem fully.

## Categorical text

Once text is cleaned, if it repeats, convert it:

```python
df["city"] = df["city"].astype("category")
```

The `.str` accessor still works on a cat column. Pandas applies the step to the **groups** rather than to each row. So `df["city"].str.upper()` on a million rows with four cities does four steps, not a million.

That is the single largest speed-up on hand for repeated text work, and it's a one-line change.

## When to stop using pandas for text

pandas is a fair place to clean and extract from moderate amounts of text. It isn't a text-handling engine.

For token split, stemming, language spotting or anything linguistic, a dedicated library is the right tool.

For very large corpora, the `object` dtype's per-row Python cost dominates. The work belongs in a DB, in Polars, or in a purpose-built pipeline.

The signal is often the profile: if `.str` steps are the slowest part of your script and the frame is large, the answer is a other tool rather than a cleverer regex.

## Regex, briefly

a few `.str` methods take a regular formula. A small vocab covers most data cleaning:

`\d` digit, `\w` word character, `\s` whitespace, `.` any character.

`+` one or more, `*` zero or more, `?` optional.

`^` start, `$` end, `\b` word boundary.

`[abc]` a character set, `[^abc]` its negation.

`(...)` a capture group, `(?P<name>...)` a named one.

`|` alternation.

Two habits prevent most regex trouble in pandas. Use **raw strings**. `r"\d+"`. So backslashes reach the regex engine intact. And test the pattern on a handful of values before applying it to the column. A pattern that matches nothing makes a column of `NaN` rather than an error.

`str.holds(..., regex=False)` and `str.replace(..., regex=False)` are both faster and safer when the pattern is a literal.

## Encoding problems

Text that arrives mangled &mdash; `Ã©` where `é` belongs &mdash; was decoded with the wrong encoding, often at read time.

The fix is at `read_csv`, with `encoding="latin-1"` or `encoding="cp1252"`, not in pandas later. Repairing mojibake after the fact is possible and unreliable.

`df["col"].str.encode("utf-8").str.decode("utf-8")` round-trips text and raises on anything invalid. This Is a way to find the offending rows.

For matching across accented and unaccented spellings, norming with `str.norm("NFKD")` and stripping mixing characters puts both forms into the same shape.

## Performance, restated

Three things make text work faster, in order of effect:

**Convert to `group`** when values repeat. steps then apply to the groups, not the rows.

**Do the cleaning once**, at load time, rather than inside a function called per group or per row.

**Use `regex=False`** where the pattern is a literal.

And the structural point: if `.str` steps dominate the profile on a large frame, pandas is the wrong layer for that work. A DB, Polars, or a purpose-built text pipeline will do it in a fraction of the time.

## A summary

`.str` applies string methods elementwise and chains.

Missing values pass through as `NaN`. Pass `na=False` on any predicate used for filtering.

`holds` is a regex by default. `startswith` isn't a regex at all.

`split(expand=True)` makes columns. `extract` with named groups is often clearer.

`replace` needs an clear `regex=` in pandas 2.

Norm column names and text values once, at load.

Convert repeated text to `group`.

And check how many rows a pattern really matched, rather than given it matched them all.

## A closing note

Text is where pandas is least like an array library and most like plain Python, and both facts show.

`.str` gives you the string methods across a whole column. This Is convenient and reads well. Underneath it's per-element Python over a column of pointers. This Is why text work is an order of magnitude slower than math on the same number of rows.

Two things follow. Clean text **once**, at load, rather than again and again in the middle of a pipeline. And convert repeated values to `group`, after which `.str` steps apply to the handful of distinct values rather than to each row. Often the largest single speed-up on hand, for a one-line change.

The correctness trap is missing values. `.str` predicates return `NaN` rather than `False`. A mask holding `NaN` can't index a frame. `na=False` on each `.str` filter is the habit. Its lack is the error that appears only once the data has a gap.

## One more thing

`str.get(i)` indexes into each string or list. This Is the concise form of `str[i]` and works the same way. It returns `NaN` rather than raising where the index is out of range. This Is often what you want on ragged data.
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
intro: Parsing them, the .dt accessor, and why a text date breaks all downstream.

## They arrive as text

`read_csv` doesn't parse dates unless you tell it to. A date column comes in as `object`. All you do with it's then string action wearing a date's clothes.

Sorting is lexical. For ISO format. `YYYY-MM-DD`. That happens to give the right answer. This Is why the problem often goes unnoticed until the data arrives in another format. `"15/01/2024"` sorts before `"01/03/2024"` as text, and there's no error.

compare has the same problem, as does anything asking for a month, a weekday or a gap in days.

The fix is `pd.to_datetime`, or `parse_dates=["col"]` at read time. This Is faster because it happens during the read.

Checking `df.dtypes` after loading catches this. This Is why it's in the inspection routine.

## Parsing

`pd.to_datetime` is good at guessing, and guessing is the problem.

`05/04/2024` is 5 April in most of the world and 4 May in the United States. pandas has to pick one. It won't always pick yours.

`dayfirst=True` states the rule. Better still, `format="%d/%m/%Y"` states the whole shape. That drops the ambiguity **and** is much faster. Pandas can skip inference fully. On a large column the gap is large enough to notice.

For messy input, `errors="coerce"` turns unparseable values into `NaT` (the datetime equal of NaN) rather than raising on the first bad row. Then `df[df["date"].isna()]` shows you just what failed. This Is far more handy than a traceback naming one value.

`NaT` behaves like NaN: it fails each compare and is caught by `isna()`.

## The .dt accessor

just parallel to `.str`.

`s.dt.year`, `.month`, `.day`, `.hour`, `.minute` pull out parts as ints.

`s.dt.day_name()` and `s.dt.month_name()` give text.

`s.dt.quarter`, `.dayofweek`, `.dayofyear`, `.is_month_end` cover the derived questions that would else need math.

`s.dt.date` drops the time and returns Python `date` objects. Note that this gives an `object` column. This Is often not what you want. `s.dt.norm()` keeps it a proper datetime column set to midnight. Is the better choice for grouping by day.

`s.dt.strftime(fmt)` formats for output, returning text. That is the last step before display, not a thing to do in the middle of a pipeline.

## Arithmetic

Subtracting two datetime columns gives a `timedelta64` column.

`gap.dt.days` gives whole days. `gap.dt.total_seconds()` gives the full duration as a float. This Is what you want for anything sub-day or for converting to any units.

Adding a fixed duration uses `pd.Timedelta(days=30)`.

Adding a **calendar** period uses `pd.DateOffset(months=1)`. The gap matters. A month isn't a fixed number of days. "one month after 31 January" is a calendar question, not an math one. `DateOffset` handles month ends and leap years. `Timedelta` can't. It doesn't know what month it's in.

## DatetimeIndex

Putting the dates in the index unlocks the time-aware pick that makes pandas pleasant for time series.

`s["2024-02"]` selects the whole of February. `s["2024"]` selects the year. This is **partial string indexing**. It works because pandas understands the index is a timeline.

`s["2024-01-10":"2024-01-20"]` slices a range, inclusive of both endpoints as label slicing always is.

`pd.date_range(start, periods=n, freq=...)` builds such an index. The rate aliases are worth knowing: `D` daily, `W` weekly, `ME` month end, `MS` month start, `h` hourly. Note that pandas 2.2 renamed a few of these. `M` became `ME` and `H` became `h`. So older code raises a deprecation warning or an error based on version.

A DatetimeIndex is also what `resample` needs. This Is the subject of a later module.

## Time zones

A timestamp is either **naive** (no zone) or **aware** (a zone attached). The two can't be checked or subtracted. The error when you try is clear.

`s.dt.tz_localize("UTC")` attaches a zone to naive timestamps, asserting what they always meant. `s.dt.tz_convert("Asia/Kolkata")` converts an aware timestamp to another zone.

Getting these backwards is the usual mistake: `tz_localize` on data that is already aware raises. `tz_convert` on naive data raises too.

The rule that causes the fewest problems is to store all in UTC and convert only for display. Mixed-zone data in one column isn't representable as a proper datetime dtype at all. It falls back to `object`. Which is a strong hint that norming early is the right move.

## Parsing performance

Date parsing is one of the slowest parts of loading a large file, and it's almost fully avoidable.

`pd.to_datetime` without a format tries to infer one, per value in the worst case. With `format=` it uses a single known pattern and runs far faster. Often by an order of magnitude on a large column.

`format="ISO8601"` handles the common ISO variants without full inference.

`cache=True` (the default for large inputs) helps enormously when the same date string repeats, as it does in any dataset with many rows per day.

Parsing at read time with `parse_dates=` is faster than parsing later. Pandas can do it while it already has the strings in hand.

## Periods and offsets

`Timestamp` is a point in time. `Period` is a span. A whole month, a quarter, a year.

`s.dt.to_period("M")` converts timestamps to monthly periods. Grouping by that is often more natural than grouping by year and month apart, and it sorts right.

`PeriodIndex` supports math in period units: adding 1 to a monthly period gives the next month, without the day-of-month ambiguity that plagues timestamp math.

Offsets sit between the two. `pd.offsets.MonthEnd(1)`, `BusinessDay(3)`, `Week(weekday=0)` show calendar movements. `df["date"] + pd.offsets.MonthEnd(0)` snaps each date to the end of its month. This Is a common alignment step before joining monthly data.

Business-day offsets understand weekends, and can take a holiday calendar. This Is the sort of thing that is tedious to write by hand and easy to get subtly wrong.

## Components, and the leap-year trap

`.dt.year`, `.month`, `.day` are obvious. Two aren't.

`.dt.isocalendar()` returns ISO year, week and day. This Is what you want for week-based reporting. The ISO year is **not** always the calendar year. The first days of January can belong to the previous ISO year. So grouping by `.dt.year` and ISO week together makes wrong groups at the boundary.

`.dt.dayofweek` is 0 for Monday. `.dt.day_name()` gives the name and respects locale settings.

finding an age or a duration in years by cutting days by 365 is wrong by a day each four years and builds up. For exact calendar differences, subtract periods or use `dateutil.relativedelta`.

## Time zones, in more depth

The rule that avoids nearly all trouble: **store UTC, convert for display**.

`tz_localize` attaches a zone to naive timestamps, asserting what they always meant. It raises on data that is already aware.

`tz_convert` moves an aware timestamp to another zone. It raises on naive data.

Getting these the wrong way round is the usual error. The messages are clear about which you needed.

Two edge cases are worth knowing because they're real and they raise:

**Ambiguous times** &mdash; when clocks go back, an hour occurs twice. `ambiguous="infer"`, `True`, `False`, or `NaT` decides.

**Nonexistent times** &mdash; when clocks go forward, an hour doesn't exist. `nonexistent="shift_forward"` or `NaT` decides.

Both only appear on real local-time data crossing a DST boundary. This Is just when you least want a surprise.

A column mixing time zones can't be a proper datetime dtype and falls back to `object`, losing `.dt` fully. Norming on the way in blocks that.

## A checklist for date columns

Parse them at read time, with an clear format.

Check `dtype` later &mdash; `datetime64[ns]` means it worked, `object` means it didn't.

Check the range with `min()` and `max()`. Dates in 1970 often mean a zero timestamp. Dates in 2099 often mean a sentinel.

Decide on a time zone and apply it once.

Set the index if you'll resample or select by period.

Sort, if anything downstream will `diff`, `shift` or `rolling`.

## Common date mistakes

**Not parsing at all.** The column stays `object`, sorts lexically, and `.dt` raises. Check `dtypes`.

**Letting the format be inferred** on ambiguous data. `05/04` is two other dates based on rule.

**Cutting days by 365** to get years. Wrong by a day each four years, and it builds up.

**Grouping by `.dt.year` and ISO week together.** The ISO year differs from the calendar year at the start of January. The boundary weeks land in the wrong group.

**Mixing naive and aware timestamps.** Raises. This Is the good case. The bad case is a column that falls back to `object` and loses `.dt`.

**Using `.dt.date`** and getting an `object` column. `.dt.norm()` keeps it a datetime.

**given rows are sorted.** `diff` and `rolling` give numbers even so.

## Working with durations

A `timedelta64` column comes from subtracting two datetime columns.

`gap.dt.days` truncates toward zero and discards the remainder. `gap.dt.total_seconds()` keeps all and is the safer basis for converting to any units.

`gap.dt.parts` breaks a duration into days, hours, minutes and so on as split columns.

Durations aggregate: `mean`, `sum` and `show` all work, and print in a readable form.

For business durations &mdash; elapsed working days rather than calendar days &mdash; `np.busday_count` is the tool. It takes a holiday list.

## Generating date ranges

`pd.date_range(start, end)` or `pd.date_range(start, periods=n, freq=...)` builds an axis.

Three uses worth knowing:

**Reindexing onto a full calendar**. So Missing days become clear `NaN` rows rather than being absent.

**Building test data** with a known shape.

**Checking for gaps** &mdash; checking the actual index against a full range shows just which periods are missing:

```python
full = pd.date_range(s.index.min(), s.index.max(), freq="D")
missing = full.difference(s.index)
```

That is a better answer than counting rows, because it names the gaps.

`pd.bdate_range` does the same for business days.

## A summary

Parse at read time with an clear format.

Check the dtype is `datetime64[ns]` later, and check the min and max for sentinel dates.

`.dt` for parts, `strftime` only for display.

`Timedelta` for fixed durations, `DateOffset` for calendar ones.

Store UTC. Convert for display.

Set a `DatetimeIndex` when you need period pick or `resample`.

Sort before anything that checks a row with its neighbour.

And note pandas 2.2 renamed the rate aliases. `M` to `ME`, `H` to `h`. Which is the usual reason a copied example no longer runs.

## A closing note

Dates arrive as text, and all that follows depends on noticing that.

An unparsed date column sorts lexically, can't do math. Has no `.dt`. For ISO-formatted dates the lexical sort happens to be correct. This Is just why the problem often lives until the data arrives in a other format.

Parsing with an clear `format=` drops both the ambiguity between day-first and month-first and most of the parsing cost. This On a large column is large.

After that, the two things worth being deliberate about are time zones and calendar math. Store UTC and convert for display. Mixed-zone columns can't be a proper datetime dtype at all. And use `DateOffset` rather than `Timedelta` when you mean a calendar month. A month isn't a fixed number of days and only one of the two knows that.

Finally, pandas 2.2 renamed the rate aliases. When a copied example stops working, that is often why.
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

`df.sort_values("sales")` sorts by one column. A list sorts by a few, in order. `ascending` takes a matching list so each key can have its own direction:

```python
df.sort_values(["city", "sales"], ascending=[True, False])
```

That is "by city A to Z. Within each city by sales high to low". The shape of most reporting orders.

The result is a **new** frame carrying the first index labels. If downstream code thinks positionally, `reset_index(drop=True)` later.

`kind` selects the method. The default isn't stable. Equal rows can come out in any order. Pass `kind="stable"` when ties must keep their first scaled order. Which matters if you're sorting by a second key after already sorting by a first, rather than passing both keys at once.

## Missing values sort last

`NaN` goes to the **end** in both ascending and descending order. It isn't treated as very large or very small. It's simply put aside.

The result catches people: reversing an ascending sort is **not** the same as sorting descending. The NaNs move scaled to all else.

`na_position="first"` puts them at the front instead. This Is handy when the missing rows are the ones you want to look at.

## sort_index

`sort_index()` orders by the index labels rather than the data. It's what you want after steps that leave the index shuffled. It's needed for label-range slicing on a non-unique index.

`sort_index(axis=1)` orders the **columns** alphabetically. This Is a quick way to make two frames close.

Group-by results already come back sorted by key. An extra `sort_index` there's often redundant.

## nlargest and nsmallest

Sorting 200,000 rows to look at five is wasted work.

`df.nlargest(5, "v")` finds the top five without sorting the rest. The last-but-one editor measures the gap.

Both take a list of columns for tie-breaking. A `keep` arg controlling what happens when the boundary value is tied: `"first"`, `"last"` or `"all"`. `keep="all"` can return more than `n` rows. This Is at times what you want and worth knowing before it surprises you.

For a single extreme value, neither is needed: `df["v"].max()` is a reduction and far cheaper than any sort. `idxmax()` gives the label of the row that holds it. This Is how you get "the row with the highest value" in one step.

## rank

`rank` converts values into spots, and the notable part is what it does with ties.

`method="mean"` (the default) gives tied values the mean of the ranks they span. Two values tied for 2nd and 3rd both get 2.5. That is the statistically standard choice and it makes fractional ranks. This Surprises people expecting ints.

`method="min"` gives both 2 and skips 3. This is contest ranking, the "joint second" of a leaderboard.

`method="max"` gives both 3.

`method="dense"` gives both 2 and makes the next value 3. No gaps. This Is what you want for grouping into levels.

`method="first"` breaks ties by order of appearance, giving strictly distinct int ranks.

`ascending=False` ranks from the top. `pct=True` returns percentiles rather than spots. This Is the quick route to "what fraction of rows are below this one".

`rank` also takes a `na_option`, and by default missing values get `NaN` ranks rather than being placed anywhere.

## The cost

Sorting is `O(n log n)` and allocates a new frame. On a large table it's one of the more costly things you can do.

Three cheaper options cover most reasons people sort:

**An extreme value**: `max`, `min`, `idxmax`, `idxmin` &mdash; a single linear pass.

**A top n**: `nlargest` / `nsmallest`.

**Deduplication order**: sorting is genuinely required here, and it is the one case where sorting before `drop_duplicates` is not optional.

Sort when the order is the actual output. A report, a chart, a file someone will read. else there's often a reduction that answers the same question for a fraction of the cost.

## Sorting by something that is not a column

`key=` applies a function to the sort keys before checking, without changing the data:

```python
df.sort_values("city", key=lambda s: s.str.lower())
```

That sorts case-insensitively while leaving the first values intact. It's much cleaner than adding a helper column, sorting, and dropping it.

For a **custom order** &mdash; small, medium, large &mdash; the right tool is an sorted cat:

```python
df["size"] = pd.Categorical(df["size"], ["small", "medium", "large"], ordered=True)
df.sort_values("size")
```

The order then belongs to the column and applies to each later sort, group-by and compare, rather than being repeated at each call site.

Sorting by string length, by the last character, or by any derived value is `key=` with the right `.str` step.

## Sorting a group-by result

Group-by output arrives sorted by key. often you want it sorted by the value:

```python
df.groupby("city")["sales"].sum().sort_values(ascending=False)
```

`sort=False` on the group-by itself skips the key sort. This Is faster on many groups and gives order of first appearance.

For "the top n within each group", the pattern is a group-wise rank and a filter:

```python
df[df.groupby("city")["sales"].rank(ascending=False) <= 3]
```

`groupby(...).head(3)` also works and takes the first three **rows** of each group in current order. It needs a sort first to mean "the top three".

## Stability, in practice

The default sort isn't stable. So Equal elements can come out in any order.

That matters in two situations.

**A multi-pass sort.** Sorting by one column, then another, only works if the second sort preserves the first sorting. Pass `kind="stable"`, or better, sort by both keys in one call with a list.

**Reproducible output.** Two runs on the same data can order ties differently. This Makes diffs noisy and tests flaky. `kind="stable"` fixes it.

The cost is small enough that using `kind="stable"` by default when the output is checked or written to a file is a fair habit.

## Sorting large frames

Sorting is `O(n log n)` and copies the frame. On a large table it's often the most costly single step in a script.

The options, in order of preference:

**A reduction** &mdash; `max`, `min`, `idxmax`, `idxmin` for an extreme.

**`nlargest` / `nsmallest`** for a top n.

**`sort_index`** if the data is already nearly sorted by that key. It's cheaper than a full value sort.

**Sorting once** and reusing the result, rather than sorting inside a loop or a function called again and again.

And when the sort *is* the output. A report, a leaderboard, a file someone reads. It isn't cost, it's the deliverable.

## Ranking, and what to do with ties

The five methods differ only in tie handling. The right choice depends on what the rank is for.

For a **leaderboard**, `min` gives the familiar "joint second, then fourth".

For **levels or bands**, `dense` avoids gaps.

For a **statistic** &mdash; a rank link, a percentile &mdash; `mean` is the standard choice and is the default for that reason.

For a **fixed sorting** where ties must be broken, `first` uses order of appearance. This Means the result depends on how the frame is sorted.

`pct=True` gives percentile ranks in `[0, 1]`. This Is the quick route to "what fraction of rows are at or below this one" and is close across datasets of other sizes.

## Sorting the columns rather than the rows

`df.sort_index(axis=1)` orders columns alphabetically. This Makes two frames easier to compare and diffs easier to read.

For a deliberate order, pick is clearer: `df[["id", "date", "value"]]`.

For a partial order &mdash; pin some columns to the front, keep the rest &mdash; build the list:

```python
first = ["id", "date"]
df = df[first + [c for c in df.columns if c not in first]]
```

That lives a schema change. Here A hard-coded full list doesn't.

## Sorting for output

When the sort is the deliverable, a few details matter that don't else.

`na_position="first"` when missing rows are what the reader should notice.

`key=` for case-insensitive or natural sorting.

An **sorted cat** for a domain order. Small/medium/large. So each later step uses it too.

`reset_index(drop=True)` if row numbers will be displayed. They read 0, 1, 2 rather than the first labels.

`kind="stable"` so that re-running makes byte-same output. This Matters if the result is committed or diffed.

## Ties, restated

The choice of tie-handling is a choice about meaning, not a detail:

`mean` &mdash; the statistical rule. Makes fractional ranks.

`min` &mdash; contest ranking. Joint second, then fourth.

`dense` &mdash; no gaps. For bands and levels.

`max` &mdash; the pessimistic reading.

`first` &mdash; any but fixed, and dependent on the current row order.

If ranks are shown to people, `min` or `dense` often matches their expectations. If ranks feed a statistic, `mean` is the right default.

## A summary

`sort_values` for data, `sort_index` for labels.

A list of keys with a matching list of directions handles multi-key sorts in one call.

Missing values go last in both directions. So Reversing isn't the same as descending.

`nlargest`/`nsmallest` for a top n. `idxmax`/`idxmin` for a single extreme.

`key=` for derived orderings. Sorted cats for domain orderings.

`kind="stable"` when ties must keep their order or output must be reproducible.

And sorting is costly &mdash; do it once, late. Only when the order is part of the answer.

## A closing note

Sorting is costly and often not needed. This Makes it worth asking what the order is for.

If the answer is "to find the largest", a reduction does it in one pass. If it's "to find the top ten", `nlargest` does it without sorting the rest. If it's "so deduplication keeps the right row", the sort is essential and skipping it makes the result any. If it's "because the output is a report", the sort is the deliverable and its cost is the point.

Ranking is the same step asked differently. Its only real subtlety is ties. The default means them. This Makes fractional ranks and surprises people expecting ints. Leaderboards often want `min`, and bands often want `dense`.

And missing values sort last in both directions. This Means reversing an ascending sort isn't the same as sorting descending. A small skew that makes a wrong answer at the ends.

## One more thing

`sort_values` accepts `ignore_index=True`, which renumbers the result rather than carrying the first labels along. That saves a split `reset_index(drop=True)` when the sorted output is going to be displayed or written with row numbers.

And `nlargest` and `nsmallest` exist on `groupby` objects too. "the top three per group" is `df.groupby("city")["sales"].nlargest(3)`. Which returns a MultiIndexed Series with the group and the first label. Often wants `reset_index` before going anywhere else.

## A note on reproducibility

Output that will be committed to a store, diffed, or checked between runs should be fixed. Sorting is where non-determinism creeps in.

The default sort isn't stable. Tied rows can appear in other orders on other runs or other pandas versions. A file written from that output makes spurious diffs. A test checking it fails intermittently.

`kind="stable"` fixes it, at a cost small enough to skip.

The same applies to group-by. This Sorts keys by default but says nothing about the order of rows within a group. To `drop_duplicates`, whose survivor depends fully on the current order.

For anything whose output is checked, the rule is. Sort by name, sort stably. Make the sort keys enough to find the order uniquely.
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
intro: Split, apply, combine - the step that is the reason to use pandas.

## The three steps

`df.groupby("city")["sales"].sum()` does three things:

**Split** the rows into groups by the key.

**Apply** a function to each group.

**Combine** the results into one object, one row per group.

Almost each question about aggregated data has this shape. Recognising it's most of what makes pandas worth using. The option in plain Python. A dict, a loop, a choice about missing keys, another loop to find the summary. Is a dozen lines that this replaces with one.

## The keys become the index

By default the group keys become the index of the result. That is convenient for lookup and for plotting. It's a surprise if you expected a plain column.

`as_index=False` keeps them as plain columns, giving a result that looks more like a table. `reset_index()` later does the same thing.

Which you want depends on what happens next. If the result feeds a merge or gets written to a file, the flat form is often easier. If you're going to select groups by name, the index form is better.

Results come back **sorted by key**. `sort=False` skips that sort. This Is faster on many groups and gives you the order of first appearance instead.

## The object is lazy

`df.groupby("city")` finds nothing. It returns an object that knows how the rows would be split.

That is why you can inspect it cheaply: `ngroups` counts the groups, `size()` gives rows per group, `get_group(name)` pulls one out. Iterating yields `(name, subframe)` pairs.

Iterating is legitimate for inspection and almost always the wrong way to find a thing. The loop runs Python once per group. This Is the same speed trap as `apply`. If you find yourself building up results in a list inside a groupby loop, there's nearly always an `agg` that does it in one call.

## Several keys

`df.groupby(["city", "year"])` gives one level of index per key, in the order named.

The result is a Series or frame with a **MultiIndex**. This Has its own module later. Two steps cover most direct needs:

`unstack()` moves the last index level into columns, turning a long result into a wide table. Cities down the side, years across the top.

`reset_index()` flattens all back into plain columns.

## Missing keys disappear

This is the action most likely to give a wrong number quietly.

Rows whose group key is `NaN` are **excluded** by default. They aren't put in a split group. They're dropped.

The result is that group totals don't add up to the frame total. Nothing says so. On a frame where 5% of the key column is missing, each aggregate is quietly found on 95% of the data.

`dropna=False` keeps them as a group with a `NaN` key.

The habit worth forming: after any group-by that matters, check that the total of the result matches the total of the input. It's one line and it catches this at once.

## Aggregating

`df.groupby("city").sum(numeric_only=True)` applies one function to each numeric column.

`agg({"sales": "sum", "units": "mean"})` applies a other function per column.

**Named aggregation** is the clearest form and the one to prefer:

```python
df.groupby("city").agg(
    total=("sales", "sum"),
    biggest=("sales", "max"),
    orders=("sales", "size"),
)
```

Each output column is named by name, a few statistics can come from the same input column. The result has flat column names rather than the MultiIndex that a dict-of-lists makes. That last point saves a cleanup step almost each time.

Functions can be strings (`"sum"`, `"mean"`, `"nunique"`), NumPy functions, or your own callables. The strings are fastest. They dispatch to compiled setups rather than calling back into Python.

## size versus count

A gap that matters just where the data is imperfect.

`size()` counts **rows** in each group, including rows with missing values.

`count()` counts **non-missing values**, per column. A group of five rows with two gaps in a column reports three for that column.

`nunique()` counts distinct values.

Using `count` where you meant `size` undercounts wherever data is missing. This Is just where you're least likely to notice.

## Grouping by something that is not a column

`groupby` accepts more than a column name.

**A Series** of the same length groups by its values. This Is how you group by a derived value without adding a column:

```python
df.groupby(df["date"].dt.year)["sales"].sum()
```

**A list of Series** gives multiple keys the same way.

**A function** is applied to each index label and groups by the result.

**`pd.Grouper`** handles time: `groupby(pd.Grouper(key="date", freq="ME"))` groups by month without needing a DatetimeIndex. This Is what makes it handy alongside other keys.

**`level=`** groups by an index level rather than a column.

That flexibility means most "I need to add a column just to group by it" situations don't need the column.

## as_index, sort and dropna

Three args change the shape or content of the result. All three are worth passing on purpose.

`as_index=False` keeps the keys as columns. The result looks like a table rather than an indexed Series. It's often what you want when the output feeds a merge or a file.

`sort=False` skips sorting the keys. On many groups that is a real saving. It gives order of first appearance instead of sorted order.

`dropna=False` keeps rows whose key is missing. The default drops them. This Is the action most likely to give a total that doesn't merge.

`seen=True` matters for cat keys: without it, group-by makes a row for **each** group including absent ones. This Fills the result with zeros.

## Aggregating strings and other non-numerics

`sum` on a string column concatenates. This Is at times handy and often an accident.

The aggregations that really make sense on text:

`"first"` / `"last"` &mdash; a representative value, skipping missing.

`"nunique"` &mdash; how many distinct.

`"count"` &mdash; how many present.

`lambda s: ", ".join(s)` &mdash; collect them into one string.

`list` &mdash; collect them into a list, giving a column of lists. Convenient. It makes the column `object`. It's a display or export step rather than a thing to find on.

`numeric_only=True` on `sum` and `mean` skips non-numeric columns rather than doing a thing surprising with them. It's worth passing by name. The default has changed across versions.

## Group-by is a split, and splits can be expensive

The cost of a group-by is roughly: hashing the keys, sorting or grouping the rows, then applying the aggregation once per group.

Three things make it faster:

**A cat key.** Grouping on int codes beats grouping on strings, often much.

**`sort=False`** when you don't need sorted output.

**A string aggregation name** rather than a lambda. `"sum"` dispatches to compiled code. `lambda s: s.sum()` calls Python once per group.

That last one is the most common avoidable slowdown. `agg("sum")` and `agg(lambda s. S.sum())` give same results and differ by an order of magnitude on many groups.

## Checking a group-by

Two checks catch most errors:

**Do the totals merge?** `result["sales"].sum()` against `df["sales"].sum()`. If they differ, a key was missing and the rows were dropped.

**Is the group count what you expect?** `df.groupby(k).ngroups` against `df[k].nunique()`. If the group count is larger, the key has variants you didn't know about. Whitespace, case, or a type mismatch.

Both are one line, and both catch problems that else surface as a number that is slightly wrong.

## Reading a group-by result

The output shape depends on what you selected and how you aggregated. Knowing which of four shapes you've blocks most downstream confusion.

`df.groupby("k")["v"].sum()` &mdash; a **Series**, indexed by key.

`df.groupby("k")[["v", "w"]].sum()` &mdash; a **DataFrame**, indexed by key.

`df.groupby("k", as_index=False)["v"].sum()` &mdash; a **DataFrame** with the key as a column.

`df.groupby(["k", "j"])["v"].sum()` &mdash; a Series with a **MultiIndex**.

The double-bracket detail is the one people miss. Selecting one column with `["v"]` gives a Series. With `[["v"]]` gives a one-column frame. That gap passes to all after it.

## Aggregations worth knowing

Beyond `sum`, `mean` and `count`:

`nunique` &mdash; distinct values per group. This Answers "how many other products did each customer buy".

`first` / `last` &mdash; skip missing values. So They combine partial records.

`idxmax` / `idxmin` &mdash; the **label** of the extreme row. This Is how you get "the best row per group" rather than just its value: `df.loc[df.groupby("k")["v"].idxmax()]`.

`agg(lambda s: ...)` &mdash; anything else, at the cost of a Python call per group.

`show()` &mdash; a full summary per group, handy for exploration and too wide for a report.

That `idxmax` pattern is worth remembering. It comes up constantly and the obvious options are all worse.

## Empty groups and missing keys

Two other things that both cause totals not to merge.

**Missing keys** &mdash; rows whose group key is `NaN` are dropped unless `dropna=False`.

**Empty groups** &mdash; a cat key makes a row for each group, including ones with no rows, unless `seen=True`.

The first loses data silently. The second adds rows of zeros that were never in the data. Both defaults have changed across versions. This Is a reason to pass them by name rather than lean on the current action.

## A summary

Split, apply, combine &mdash; and the group keys become the index unless you say else.

The object is lazy. Nothing runs until you aggregate.

Missing keys are dropped by default.

Named aggregation gives flat column names and lets one column feed a few statistics.

`size` counts rows, `count` counts non-missing values.

String aggregation names are much faster than lambdas.

`idxmax` plus `.loc` gets the whole extreme row per group.

And check that the group total matches the frame total. One line that catches the most common silent error here.

## A closing note

Group-by is what pandas is for. Most of its surprises are about what silently doesn't appear in the result.

Rows whose key is missing are dropped. cat keys give rows for groups that never occurred. `count` and `size` differ wherever data is missing. Each default is defensible on its own. Together they mean a group-by result can fail to merge with the frame it came from in a few ways at once.

The check that catches all of them is one line. Compare the total of the result against the total of the input. If they differ, a thing was excluded. The reason will be one of the above.

Beyond that, the hands-on advice is to prefer named aggregation. This Makes flat column names and lets one input column feed a few statistics. To use string aggregation names rather than lambdas. This Is the gap between compiled code and a Python call per group.

## One more thing

A groupby object supports `nth(0)`. This Takes the nth row of each group and isn't the same as `first()`: `first()` skips missing values and `nth(0)` doesn't. When a group's first row has a gap, the two give other answers. Which you want depends on whether "first" means the first row or the first on hand value.

`ngroup()` numbers the groups. This Is a compact way to turn a set of keys into a single int label for indexing or plotting.

## In summary

Split, apply, combine &mdash; and the details that decide whether the answer reconciles.

Missing keys are dropped unless you say else. cat keys give rows for groups that never appeared. `size` counts rows and `count` counts values. They differ wherever data is missing.

Named aggregation is the clearest form and gives flat column names. String aggregation names are much faster than lambdas. And checking the result's total against the input's total is one line that catches the most common silent failure.
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
intro: Group statistics broadcast back to each row.

## The shape decides the method

Three group-by steps differ only in the shape of what they return. Choosing between them is nearly always obvious once you ask what shape you want.

`agg` returns **one row per group**. A summary table.

`transform` returns **one row per first row**. A new column.

`filter` returns **a subset of the first rows**. Fewer rows, same columns.

Most confusion here is someone reaching for `agg` when they wanted `transform`, then writing a merge to get back to the first shape.

## transform

`df.groupby("city")["sales"].transform("sum")` gives each row its city's total.

Because the result is aligned with the first frame, it assigns straight back:

```python
df["city_total"] = df.groupby("city")["sales"].transform("sum")
df["share"] = df["sales"] / df["city_total"]
```

Two lines for "what fraction of its city's sales is this row". This Is a question that else needs an aggregation, a rename, a merge and a check that the merge didn't change anything.

That last point is the real arg. The aggregate-then-merge route is three steps, each of which can go wrong. The aggregate can drop `NaN` keys, the merge can times rows if the key isn't unique. The result can come back in a other order. `transform` can't do any of those. It never leaves the first index.

## What transform accepts

A string naming a built-in (`"sum"`, `"mean"`, `"max"`, `"count"`) is fastest. It dispatches to compiled code.

A function that maps a Series to a Series of the same length also works. `transform(lambda s: s - s.mean())` centres within group.

A function returning a **scalar** is broadcast to the whole group. This Is why `transform("sum")` works at all.

What it can't do is change the shape. A function returning a other length raises. This Is the gap between `transform` and `apply` and the reason `transform` is predictable.

Some methods exist right on the groupby object and don't need `transform`: `rank`, `cumsum`, `cumcount`, `shift`, `diff` and `pct_change` all return per-row results already. `g.rank()` is both clearer and faster than `g.transform("rank")`.

## Common uses

**A share of the group total** &mdash; the example above.

**Centring within group** &mdash; `df["v"] - g.transform("mean")`. Standard prep when groups have other baselines.

**Rank within group** &mdash; `g.rank(ascending=False)`. "Where does this row come in its own team."

**Group-wise fill** &mdash; `df["temp"].fillna(g.transform("mean"))`. Filling a missing temp with the mean for that *city* rather than the mean of all over. This Uses data a global fill throws away.

**Flagging outliers scaled to the group**. Checking each value against its group's standard deviation.

## filter

`df.groupby("city").filter(lambda g: len(g) >= 2)` keeps each row belonging to a group with at least two rows.

The predicate receives the whole sub-frame and returns a single `True` or `False`. It's asked once per group. The answer applies to all that group's rows.

The result is **rows**, not groups. The same columns as the input, with whole groups removed.

Common uses: dropping groups with too little data to be real, keeping only customers with more than one order, or dropping groups below a volume threshold.

Note this is a Python callback per group. It's slower than an aggregation. For simple size rules, finding sizes with `transform("size")` and filtering with a boolean mask is faster and does the same thing:

```python
df[df.groupby("city")["sales"].transform("size") >= 2]
```

That form is worth knowing because it composes with other rules, whereas `filter` doesn't.

## A note on apply

`groupby(...).apply(func)` is the general escape hatch, and it can return any shape.

That flexibility costs speed &mdash; it's a Python call per group &mdash; and predictability. The shape of the result depends on what the function returned. In pandas 2.2 it also warns about whether the grouping columns are passed to the function. This Is a sign of how awkward its semantics have become.

Reach for `agg`, `transform` or `filter` first. They cover the large majority of cases, run in compiled code. Return a shape you can predict from the method name alone.

## Ranking and cumulative operations within groups

a few methods on a groupby already return one row per input row. They need no `transform`:

`cumsum`, `cumcount`, `cummax` &mdash; running totals and counters within each group.

`rank` &mdash; spot within the group.

`shift`, `diff`, `pct_change` &mdash; compare with the previous row **of the same group**.

That last set matters more than it looks. `df["v"].diff()` on a frame holding a few entities finds a gap across the boundary between one entity and the next. This Is meaningless. `df.groupby("id")["v"].diff()` doesn't.

Any time you use `shift`, `diff` or `rolling` on panel data. A few entities stacked in one frame. The group-by version is almost certainly the one you want. Using the plain version is a quiet, plausible-looking error.

`cumcount()` numbers the rows within each group from zero. This Is how you take "the first three per group" or label repeat visits.

## Percentages and shares

The single most common `transform` is a share of the group:

```python
df["share"] = df["sales"] / df.groupby("city")["sales"].transform("sum")
```

Two variants worth knowing:

A share of the **whole frame** needs no group-by: `df["sales"] / df["sales"].sum()`.

A share **within a nested group** takes a list of keys: `transform("sum")` on `groupby(["region", "city"])`.

Because the denominator comes back aligned, these compose. You can find a share of city and a share of region in the same frame and compare them.

## Standardising within groups

Centring and scaling scaled to a group is standard prep when groups have other baselines. Other stores, other sensors, other years:

```python
g = df.groupby("store")["sales"]
df["z"] = (df["sales"] - g.transform("mean")) / g.transform("std")
```

Two cautions. A group with one row has a standard deviation of `NaN`. The result is `NaN` for that row rather than zero. And a group with zero variance cuts by zero, giving `inf`. Both are worth handling by name rather than discovering downstream.

## Filtering by a group property

`filter` takes a callback per group. This Is flexible and slow.

For the common cases, a `transform` and a boolean mask is faster and composes better:

```python
df[df.groupby("city")["sales"].transform("size") >= 5]
df[df.groupby("city")["sales"].transform("sum") > 1000]
```

The mask form can be mixed with other rules using `&`. This `filter` can't. It's also easier to reason about. It's the same masking you use all over else.

Reach for `filter` when the predicate truly needs the whole sub-frame. A rule involving a few columns at once, or a statistical test per group.

## Why apply is the last resort

`groupby(...).apply(func)` can return anything. This Is its appeal and its problem.

It's a Python call per group, so it's slow.

The shape of the result depends on what the function returned. This Makes it unpredictable to read.

And in pandas 2.2 it warns about whether the grouping columns are passed to the function. The historical action was ambiguous enough to need changing.

Before using it, check whether the step is:

a summary per group &mdash; `agg`;

a value per row &mdash; `transform`, or a groupby method like `rank` or `cumsum`;

a subset of rows &mdash; a mask built from `transform`, or `filter`;

a few columns from one math &mdash; `agg` with named aggregation.

Those four cover the large majority of cases, run in compiled code. Return a shape you can predict from the method name.

## A worked example

A frequent request: for each customer, how does this order compare with their own mean. Where does it rank among their orders?

```python
g = df.groupby("customer")["amount"]

df["cust_mean"] = g.transform("mean")
df["vs_mean"]   = df["amount"] - df["cust_mean"]
df["rank"]      = g.rank(ascending=False)
df["share"]     = df["amount"] / g.transform("sum")
df["order_no"]  = df.groupby("customer").cumcount() + 1
```

Five columns, no loop, no merge, and each one aligned with the first rows.

Written with an aggregate-and-merge it would be four split summaries and four joins, each of which could change the row count.

## When transform is not enough

`transform` needs the function to return either a scalar or a thing the same length as the group. Two cases fall outside that.

**A other number of rows per group**. Taking the top two per group, say. That is a filter. Rank with `transform` or a groupby method, then mask.

**a few columns from one math**. `transform` operates column by column. A math needing two columns together doesn't fit. `groupby(...).apply` handles it, or restructure so each output column is found apart.

## filter versus a mask

They do the same job with other trade-offs.

`filter(lambda g: ...)` &mdash; the callback sees the whole sub-frame. Any rule is expressible. It's a Python call per group.

`df[df.groupby(k)[c].transform("size") >= n]` &mdash; compiled, faster, and composes with other rules using `&`.

Use the mask for simple rules on a single statistic. This Is most of them. Use `filter` when the predicate truly needs a few columns or a math with no vectorised form.

## A summary

`agg` reduces, `transform` broadcasts, `filter` selects rows.

`transform` assigns straight back, because it keeps the first index.

It replaces aggregate-then-merge, without the risk of changing row count or order.

Group-wise `rank`, `cumsum`, `cumcount`, `shift` and `diff` are methods in their own right &mdash; no `transform` needed.

On panel data, always use the group-wise `shift`/`diff`, or the compare crosses between entities.

Group fills use data a global fill throws away.

And prefer a `transform`-built mask to `filter` for simple size or total rules.

## A closing note

`transform` is the step that drops the most not needed joins from real pandas code.

The pattern it replaces &mdash; aggregate to a summary, rename the column, merge it back &mdash; is three steps, each of which can change the row count or the order. All of which exist only to get a group statistic aligned with the rows it came from. `transform` does that by build. It never leaves the first index.

Once you've it, a family of questions turns one line each. This row's share of its group, its rank within its group, its distance from its group's mean, its group's size as a filter.

`filter` is the less-used sibling and is often better expressed as a mask built from `transform`. This Composes with other rules and runs in compiled code.

Between `agg`, `transform` and a mask, the all-round `apply` is rarely needed. Which is the point. It's the slow and unpredictable one.

## One more thing

`transform` accepts a list of functions in recent pandas, returning one column per function with a nested column index. That is at times convenient and often clearer written as split sets. Each output then has a name you chose.

More handy is that `transform` works on a whole frame, not just one column: `df.groupby("k").transform("mean")` returns a frame of group means for each numeric column at once, aligned with the first rows. Subtracting it centres the entire frame within groups in a single formula.

## In summary

Three steps, distinguished only by the shape they return: `agg` gives one row per group, `transform` one row per input row, `filter` a subset of rows.

`transform` is the one that drops work. It replaces the aggregate-rename-merge pattern with a single formula that can't change the row count or the order.

Prefer the group-by methods that already return per-row results. `rank`, `cumsum`, `cumcount`, `shift`, `diff`. Over `transform` where they apply. Use the group-wise forms on panel data so checks don't cross between entities.
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

The most-used single method in exploratory work. The first thing to run on any cat column.

By default it counts each distinct value and sorts by rate, descending. Three args change what it tells you:

`norm=True` gives proportions rather than counts. This Is what you want when checking two datasets of other sizes.

`dropna=False` includes missing values in the count. Without it, missing data is invisible here. And "invisible" is just the wrong property for the thing you most need to notice.

`sort=False` keeps the values in their natural order rather than by rate. `.sort_index()` later does the same job more by name.

On a DataFrame, `df.value_counts()` counts distinct **mixes** of all columns. This Is a quick way to find duplicated records.

## cut

`pd.cut` turns a numeric column into named bands.

```python
pd.cut(ages, bins=[0, 17, 64, 200], labels=["child", "adult", "senior"])
```

Bins are **right-inclusive** by default. The interval is `(left, right]`. So with an edge at 17, the value 17 is a child and 18 is an adult. `right=False` flips this to `[left, right)`. This Is what you often want for things like age where the rule is "18 and over".

Getting this backwards makes an off-by-one at each boundary, and it doesn't raise.

The result is a **cat** with an order. So It sorts right and groups fast.

## Values outside the bins vanish

Anything below the first edge or above the last turns `NaN`.

This is the failure mode to watch. A minus value, an outlier, a sentinel like `-1` or `9999`. All silently disappear from each count that follows. The totals no longer match the row count.

Two defences. Use `-np.inf` and `np.inf` as the outer edges when the range isn't known in advance. And check `result.notna().sum()` against `len(df)` after binning. This Takes one line and catches it at once.

Passing an int instead of a list. `pd.cut(s, 4)`. Makes four equal-width bins spanning the data. Nothing falls outside. That is safe but rarely gives real boundaries.

## qcut

`pd.cut` makes bands of equal **width**. `pd.qcut` makes bands of equal **count**.

The gap matters when the data is skewed. With a few large outliers, equal-width bins put almost each row in the first bucket and leave the rest nearly empty. Equal-count bins give you quartiles, deciles, or what split you asked for, each with the same number of rows.

Use `cut` when the boundaries have external meaning. Age brackets, price tiers, pass marks. Use `qcut` when you want scaled spot. Top quartile, bottom decile.

`qcut` raises when repeated values make an even split hopeless. `copies="drop"` merges the offending edges and returns fewer bins than requested. This Is often acceptable and worth knowing about before it fails on a column of mostly-zeros.

## crosstab

`pd.crosstab(df["city"], df["plan"])` gives a rate table: cities down the side, plans across the top, counts in the cells.

`margins=True` adds row and column totals.

`norm="index"` gives row percentages, `"columns"` gives column percentages. `True` gives the share of the grand total. Row percentages are often the notable ones. "what proportion of Delhi users are on the paid plan". And aren't the default.

`values=` with `aggfunc=` turns it from a count into any aggregation, at which point it's `pivot_table` with other spelling.

## The general form

`crosstab` is a shortcut. The general tool is group-by:

```python
df.groupby("city")["plan"].value_counts().unstack(fill_value=0)
```

That gives the same table. The long form. Before `unstack`. Is often more handy for further handling. The wide form is better for reading.

Knowing both matters because `crosstab` runs out of road quickly. More than two vars, custom aggregations, or anything feeding another math is easier with group-by. Reach for `crosstab` when you want a table to look at. Group-by when the result has one spot else to go.

## Counting combinations

`df.value_counts()` on a whole frame counts distinct **row** mixes. This Is a fast way to find duplicated records or to see which pairs of groups really occur.

`df[["city", "plan"]].value_counts()` restricts it to two columns and gives a Series with a MultiIndex. The long form of a crosstab.

`norm=True` works here too, giving the share of each mix.

`df.groupby(["city", "plan"]).size()` gives the same numbers with a other name. Is worth knowing because it composes with other group-by steps.

## Binning with meaningful edges

The edges are often the notable choice, and there are three sources for them.

**External meanings** &mdash; age brackets, tax bands, grade boundaries. These come from the domain. `cut` with an clear list is right.

**The data's spread** &mdash; quartiles, deciles. `qcut` with a count.

**Round numbers** &mdash; `np.arange(0, 101, 10)` for ten-point bands. Readable. Often better for exchange than quantiles even when quantiles are statistically neater.

`cut` also accepts an int, giving equal-width bins across the seen range. The boundaries are then any decimals. This Is fine for a quick look and poor for anything anyone reads.

`retbins=True` returns the edges alongside the result. This Is how you apply the *same* bins to another dataset later. key when checking two periods. Bins found apart aren't close.

## Ordered categories from binning

`cut` and `qcut` return an **sorted cat**. That has three handy results.

Sorting works in bin order rather than alphabetically. This Is why `value_counts().sort_index()` makes a sensible table.

compare works: `df[df["band"] > "low"]` is real.

Group-by on the result includes each bin, including empty ones. Which is often wanted in a report and at times surprising. `seen=True` restricts it to occupied bins.

## Histograms

`np.histogram` and `plt.hist` both bin and count in one step. `pd.cut` plus `value_counts` gives the same numbers with labels you control.

The bin count matters more than people expect. Too few hides structure, too many turns the spread into noise. `bins="auto"` in NumPy applies a rule of thumb. Looking at two or three bin counts is often more helpful than trusting one.

For checking spreads between groups, counts are misleading when the groups are other sizes. `norm=True`, or `crosstab(..., norm="index")`, puts them on a close footing.

## The checks worth making

After binning, three lines:

```python
binned.isna().sum()          # how many fell outside the bins
binned.value_counts().sort_index()   # is any bin empty or dominant
len(binned) == len(df)       # nothing lost
```

The first is the one that matters. Values outside the edges become `NaN` silently. Each count after that is found on a subset without saying so.

And when the bins will be reused. On next month's data, or on a test set. Save the edges rather than recomputing them. Bins derived from other data aren't close. Quantile bins in given will differ each time.

## Reusing bins across datasets

Bins found from one dataset don't apply to another. Checking two sets of quantile bins found apart is meaningless &mdash; the boundaries differ.

`retbins=True` returns the edges:

```python
train_binned, edges = pd.cut(train["score"], 4, retbins=True)
test_binned = pd.cut(test["score"], bins=edges)
```

The test data now uses the training boundaries. This Is what makes the two close. Values outside the training range fall outside the bins and become `NaN`. This Is honest. They're outside what the bins show.

The same applies to any before-and-after compare. To production scoring against a model trained earlier. Saving the edges alongside the model is part of saving the model.

## Counting with weights

`value_counts` counts rows. When each row shows a few things. A quantity column, a sampling weight. Counting rows is the wrong number.

`df.groupby("city")["qty"].sum()` is the weighted version.

`np.bincount`-style weighting has no direct `value_counts` equal, and group-by is the general answer.

For crosstabs, `pd.crosstab(a, b, values=c, aggfunc="sum")` weights the cells by another column.

## Cardinality as a diagnostic

`nunique()` against `len(df)` classifies a column in one number:

**1** &mdash; constant. Carries no data.

**2** &mdash; binary.

**Low, scaled to the rows** &mdash; a group. Convert it.

**Close to the row count** &mdash; an identifier. Not a feature.

**Moderate and surprise** &mdash; often a sign of unnormalised text. Here The same value appears in a few spellings.

Running `df.nunique().sort_values()` across a new frame takes a second and tells you what kind of column each one is. This Is the first thing you need to know.

## A summary

`value_counts` first, with `dropna=False` and at times `norm=True`.

`cut` for real boundaries, `qcut` for equal-sized groups.

Bins are right-inclusive by default. `right=False` flips it.

Values outside the edges become `NaN` silently. Use infinite outer edges, and check the count later.

Save the edges when the bins will be reused.

`crosstab` for a table to look at. `groupby` plus `unstack` when the result goes one spot else.

And weight the counts when rows aren't the unit you really mean to count.

## A closing note

Counting is the least glamorous step in pandas and the one that catches the most problems.

`value_counts` on each cat column, run before any analysis, finds the typos, the stray capitals, the trailing spaces and the groups no one mentioned. Each of those would else become a silently split group in an aggregation.

Binning turns smooth data into the groups a question is really about. Age brackets, price tiers, quartiles. The two things to hold onto are that bins are right-inclusive by default. That values outside the edges vanish into `NaN` without a word.

Both are worth checking with one line each. The boundary rule against a value that sits on a boundary. The count of non-missing results against the row count. Together they take a few seconds and prevent an entire class of quietly wrong summaries.

## Two more things worth knowing

`pd.cut` accepts `labels=False`, which returns the **bin number** rather than a label. That is what you want when the bins feed a model or a further math rather than a report. It avoids the cat dtype fully.

`value_counts` has a `bins=` arg that bins and counts in one step for numeric data: `s.value_counts(bins=5)` is `pd.cut` followed by counting. This Is convenient for a quick look at a spread.

And `pd.crosstab` accepts lists for either axis, giving nested rows or columns. `dropna=False` keeps mixes that never occurred. The second is worth knowing when two crosstabs must have the same shape to be checked. Without it, a group absent from one dataset simply doesn't appear. The tables no longer line up.

## Counting for comparison

Counts answer "how many". Checking two groups needs proportions. Raw counts confound size with rate.

A city with twice the group has twice the customers on any plan. Checking the counts says nothing. `norm="index"` on a crosstab, or `value_counts(norm=True)` within a group-by, puts them on the same footing:

```python
(df.groupby("city")["plan"]
   .value_counts(normalize=True)
   .unstack(fill_value=0)
   .round(3))
```

That reads as "what fraction of each city's customers are on each plan". This Is often the question people mean.

The reverse scaling &mdash; `norm="columns"` &mdash; answers a other question: "what fraction of paid customers are in each city". Both are legitimate and they aren't the same. Stating which one a table shows is worth a line of text next to it. The numbers alone don't say.

## In summary

`value_counts` on each cat column is the cheapest diagnostic in pandas. It finds the variants that would else split a group-by silently.

`cut` bands by boundaries you choose and `qcut` by quantiles. The choice depends on whether the boundaries have external meaning or you want equal-sized groups.

Two things to check each time: which rule the bin edges use. They're right-inclusive by default. How many values fell outside the edges, since those become `NaN` without a word and each count later is found on a subset.
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
intro: The escape hatch, what it costs, and the form that often replaces it.

## Three different things

`Series.map` looks each value up in a dict, a Series, or a function. It's for **substitution**.

`Series.apply` calls a function on each value. It's for **math** that has no array form.

`DataFrame.apply` calls a function on each column (`axis=0`) or each row (`axis=1`).

`DataFrame.map` &mdash; formerly `applymap` &mdash; calls a function on each single cell.

They look the same in small examples and aren't. The differences show up in both speed and action with missing values.

## map

`s.map({"a": "apple"})` replaces values by lookup.

Anything not in the mapping turns `NaN`. That is a fair default and often not what people want. A typo in a key silently blanks a column.

`s.map(lookup).fillna(s)` keeps the first where there was no match. This Is often the intended action for a partial rename.

`na_action="skip"` skips missing input rather than passing `NaN` to the function. This Matters when the function would fail on it.

`map` with a dict is fast. It's a lookup rather than a call. `map` with a **function** is just as slow as `apply`.

## What apply costs

`apply` doesn't vectorise anything. It calls your function once per element and assembles the results.

The third editor measures it: on 200,000 rows, `apply` runs roughly an order of magnitude slower than the equal math. Is no faster than a plain list comprehension. Because that is what it's.

There's a persistent belief that `apply` is "the pandas way" and so fast. It's neither. It's the escape hatch for when there's no array formula.

## axis=1 is the expensive one

`df.apply(func, axis=1)` makes a **Series object for each row** and passes it to your function. That is object creation per row on top of the Python call.

It's the single most common reason a pandas script is slow, and it's nearly always replaceable.

The tell is a lambda that indexes into the row: `lambda row: row["a"] * row["b"]`. That is `df["a"] * df["b"]`. This Operates on whole columns in compiled code.

## The replacements

Nearly each row-wise `apply` is one of a handful of patterns:

**A gated** &mdash; `np.where(cond, a, b)`. The vectorised if/else.

**a few rules** &mdash; `np.select([c1, c2], [v1, v2], default=v3)`. checked in order, first match wins.

**A lookup** &mdash; `map` with a dict.

**Numeric bands** &mdash; `pd.cut`.

**String work** &mdash; the `.str` accessor.

**Row-wise math** &mdash; plain column math.

**A group statistic per row** &mdash; `groupby(...).transform(...)`.

Between them these cover the large majority of real cases. When you find yourself writing `apply(axis=1)`, it's worth thirty seconds to check this list first.

## When apply is right

It truly earns its place in a few situations.

**Wrapping an existing scalar function** you can't or shouldn't rewrite. A parser, a checker, a call into another library.

**Per-row logic with no array equal**. A thing that branches on a few columns in a way `np.select` can't express cleanly, or that returns a var number of fields.

**Returning a few columns at once**, by returning a Series from the function, as the last editor shows.

**Small frames**, where the whole step takes microseconds either way and clarity is the only thing that matters.

That last point deserves emphasis. Optimising an `apply` over 200 rows is wasted effort. A readable `apply` can be better code than a clever vectorised formula no one can modify. The question is always whether the frame is large enough for the gap to matter.

## If it must stay a loop

When the logic really is sequential and per-row. The frame is large, pandas isn't the tool. The options are to move the loop into NumPy, compile it with Numba, or restructure the problem.

What is never right is `iterrows`. It's slower than `apply(axis=1)`, it loses dtypes by converting each row to an object Series. There's no situation where it's the best on hand option. `itertuples` is a lot faster if you truly need to iterate, and preserves types.

## DataFrame.map and the applymap rename

`DataFrame.map(func)` applies a function to **each cell**. It was called `applymap` until pandas 2.1. The old name is deprecated.

It's rarely the right tool. Applying a function to each cell of a table often means either the step belongs on exact columns, or the frame should have been reshaped first.

The legitimate uses are formatting for display and elementwise type coercion across a homogeneous frame. Both of which are end-of-pipeline steps.

## Returning several values

A function that returns a Series gives a few columns:

```python
df.apply(lambda r: pd.Series({"a": ..., "b": ...}), axis=1)
```

That works and is slow twice over. A Python call and a Series build per row.

The faster shape is often to find each output column apart with vectorised expressions, even if that means traversing the input more than once. Three passes over a column in compiled code beat one pass in Python by a wide margin.

When the math truly makes a few values at once and can't be split, `zip(*df.apply(...))` or building lists and assigning at the end avoids the Series build.

## result_type and the empty-frame trap

`df.apply(func, axis=1)` on an **empty** frame doesn't call the function at all. Pandas can't infer the result shape. The result is often an empty DataFrame where the code expected an empty Series. The next step fails with a confusing error.

Code that runs `apply` on a frame that may be empty should handle that case by name. The failure appears only when the input happens to be empty. Which is just the edge case least likely to be tested.

`result_type=` controls how a list-returning function is read: `"expand"` makes columns, `"reduce"` keeps a Series.

## Choosing the right escape hatch

When a thing truly can't be vectorised, `apply` isn't the only option. Often not the best one.

**`np.vectorize`** &mdash; despite the name, a loop. It handles broadcasting and dtypes for you, and offers no speed gain.

**A list comprehension over `zip` of the columns**. Often *faster* than `apply(axis=1)`. It skips the per-row Series build. Less idiomatic, measurably quicker.

**`itertuples`** &mdash; fast loop with dtypes preserved, when you need the whole row.

**Numba** &mdash; compiles a numeric loop to machine code. The right answer when the logic is truly sequential and the frame is large.

**Restructuring** &mdash; often the real answer. A loop over rows to look a thing up is a `merge`. A loop to find a group statistic is a `transform`. A loop with a rule is `np.select`.

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

turns:

```python
conds = [
    df["score"] >= 80,
    (df["score"] >= 50) & (df["city"] == "pune"),
    df["score"] >= 50,
]
df["band"] = np.select(conds, ["A", "B", "C"], default="F")
```

The rules are checked in order and the first match wins. This Is just the semantics of the if/elif chain. It's longer to read the first time and orders of magnitude faster. The rules can be built programmatically in a way the function can't.

## The honest summary

`apply` isn't forbidden. It's a Python loop with a pandas-shaped interface. It should be used when that is what you want. Awkward per-row logic, an existing function you can't rewrite, or a frame small enough that the gap is unmeasurable.

The mistake is reaching for it reflexively for math, conditionals and lookups, all of which have vectorised forms that are shorter and faster.

## Mapping with a Series

`map` accepts a Series and a dict. This Makes a lookup table out of another frame:

```python
lookup = ref.set_index("code")["label"]
df["label"] = df["code"].map(lookup)
```

This is often better than a merge for a simple one-column lookup. It can't times rows, it needs no `how` or `validate`. Unmatched codes become `NaN` rather than dropping the row.

The need is that the lookup's index is unique. If it isn't, `map` raises. Which is a better failure than a merge silently duplicating rows.

For a lookup that must bring a few columns, a merge is the right tool.

## Missing values in apply and map

`map` passes `NaN` to the function unless `na_action="skip"`. A function that calls `.lower()` or does math will fail on it. The traceback points at your function rather than at the data.

`apply` does the same.

Two options: guard inside the function, or filter first and assign back through `.loc`. The second is often cleaner. It keeps the function simple:

```python
ok = df["text"].notna()
df.loc[ok, "parsed"] = df.loc[ok, "text"].apply(parse)
```

## Measuring before optimising

`apply` is slow scaled to vectorised steps and fast scaled to nothing at all. Whether it matters depends fully on size.

On a thousand rows, an `apply` takes about a millisecond. Replacing it with `np.select` saves a millisecond and costs readability if the logic is truly branchy.

On a million rows, the same `apply` takes seconds and dominates the script.

The choice rule is to measure the actual frame, not to apply a blanket rule. `%timeit` on the real data answers it in seconds. Often the answer is that this given `apply` is irrelevant and a other line is the problem.

## A summary

`map` for lookups &mdash; dict or Series &mdash; and note unmatched keys become `NaN`.

`apply` on a Series is a loop. On a frame with `axis=1` it's a slower loop.

`DataFrame.map` (formerly `applymap`) touches each cell and is rarely the right tool.

`np.where`, `np.select`, `pd.cut`, `.str` and `transform` replace most row-wise applies.

A list comprehension over `zip` of columns often beats `apply(axis=1)`.

`iterrows` is never the right choice. `itertuples` if you must iterate.

And the size of the frame decides whether any of this matters.

## A closing note

`apply` occupies a strange place: it's the most reached-for method in pandas and rarely the right one.

it looks like the pandas way of doing a thing per row. Pandas has a reputation for speed. It feels like it should be fast. It's a Python loop with a method-call interface, and it's no faster than the list comprehension it replaces.

Nearly each row-wise `apply` is one of a handful of patterns with a vectorised form. A gated is `np.where` or `np.select`, a lookup is `map`, a numeric band is `pd.cut`, string work is `.str`. A group statistic is `transform`.

That said, the honest spot isn't that `apply` is forbidden. On a small frame the gap is unmeasurable. A readable `apply` beats a clever formula no one can modify. The mistake is reaching for it by default rather than deciding. Never measuring whether it matters.

## One more thing

`Series.map` accepts a **function with a default** through `sets.defaultdict`. This Is the neat way to map known values and leave all else at a fallback without a split `fillna`.

And `apply` on a groupby is where `include_groups=False` now matters. In pandas 2.2 the grouping columns are passed to the function by default and that action is being changed. Passing the arg by name is how you write code that behaves the same before and after the change.

## In summary

`map` substitutes, `apply` finds, and both call Python once per element.

Nearly each row-wise `apply` has a vectorised equal. `np.where`, `np.select`, `map`, `pd.cut`, `.str`, `transform`. That is shorter and faster.

`apply` remains the right answer for truly awkward per-row logic, for wrapping a function you can't rewrite. On frames small enough that the gap is unmeasurable. The mistake is reaching for it without deciding. Never measuring whether it matters.
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

Which axis you're joining along decides which axis does the *aligning*. That is the part worth being deliberate about.

Stacking rows aligns the **columns** by name. Stacking columns aligns the **index** by label.

## Stacking rows

The default keeps both frames' index labels. The result can have repeated labels. Two rows both labelled 0.

That is legal, and it breaks things later: `.loc[0]` returns two rows instead of one, and code expecting a scalar fails. It's also invisible until a thing depends on it.

`ignore_index=True` renumbers from 0. Pass it unless the index labels carry meaning you need to keep.

Columns are matched **by name**. A column present in one frame and not the other is filled with `NaN` for the missing rows. The result has the union of all columns. `join="inner"` keeps only columns present in each frame.

The name-matching is a feature: two frames with the same columns in other orders line up right. It's also a trap when a column has been misspelled in one source. You get two columns each half-full rather than an error.

Checking `result.columns` and the `isna()` counts after a concat catches that at once.

## Stacking columns

`axis=1` puts frames side by side, aligning on the index.

If the two frames have other labels, the union is used and gaps become `NaN`. If they've the same labels in a other order, pandas reorders to match. Which is correct and isn't what spot-based intuition expects.

The common mistake is concatenating two frames that *should* match row-for-row but whose indexes have drifted apart, often because one of them was filtered. The result is a frame with far more rows than either input, mostly `NaN`.

If you mean "these are the same rows in the same order", reset both indexes first:

```python
pd.concat([a.reset_index(drop=True), b.reset_index(drop=True)], axis=1)
```

That makes the spot-based intent clear rather than leaning on labels that may not match.

`join="inner"` keeps only rows present in both.

## keys

`pd.concat([jan, feb], keys=["jan", "feb"])` adds an outer index level recording which frame each row came from.

This is how you combine monthly files, or results from a few runs, without losing track of the source. `out.loc["jan"]` selects one back out. `reset_index(level=0)` turns the label into an plain column.

Without `keys`, that data is gone the moment the frames are stacked. Rebuilding it means remembering how many rows each contributed.

## Never concat in a loop

`pd.concat` allocates a new frame and copies all into it. Inside a loop that is quadratic. It's one of the most common speed mistakes in pandas.

Collect the pieces in a Python list and call `concat` **once**:

```python
frames = [process(f) for f in files]
out = pd.concat(frames, ignore_index=True)
```

The last-but-one editor measures the gap. It grows with the number of loops. A pattern that seems fine on ten files turns unusable on a thousand.

## Dtypes shift

When frames disagree about a column's type, the result is promoted to a thing that holds both: `int` plus `float` gives `float`. Anything plus a string gives `object`.

There's a exact version of this worth knowing. Starting with an **empty** frame and concatenating into it. An empty column has no real dtype. Mixing it with real data can widen the result to `object`. At which point the column is slow and no longer numeric.

That is another reason the list-then-concat pattern is better: there's no empty seed frame to poison the types.

After any concat that mixes sources, `result.dtypes` is worth a glance for just this.

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

**Tag the source** before appending. So A row can be traced back to its file. `keys=` does the same thing through the index if you prefer.

**Sort the paths**, so the result is fixed rather than based on filesystem order.

**Concat once**, outside the loop.

The frequent surprise is that the files don't agree. A column renamed halfway through the year, an extra column in later exports. Concat unions the columns and fills the gaps with `NaN`, silently. Checking `df.isna().mean()` later shows at once which columns are only present in some files.

## verify_integrity and sort

`verify_integrity=True` raises if the result would hold copy index labels. It costs a check and blocks a duplicated index passing silently.

`sort=True` sorts the columns alphabetically when frames have other sets. The default leaves them in order of first appearance. This Is often more readable.

## What concat cannot do

`concat` aligns on labels. It does **not** join on values.

Mixing two frames on a shared **key column** is `merge`, not `concat(axis=1)`. Using `concat` for that works only if the key happens to be the index of both frames and both are sorted the same way. This Is a coincidence rather than a design.

The tell is `axis=1` on frames whose indexes weren't on purpose made to match. If you find yourself resetting indexes to make a `concat` line up, you probably wanted `merge`.

## Memory during a concat

`concat` allocates a frame the size of all the inputs mixed. The inputs stay alive until it returns. Peak memory is so roughly twice the final size.

On a large combine that is the binding constraint. There are two ways around it.

**Process and reduce each piece before mixing**. Filter, select columns, aggregate. Concatenating summaries is far cheaper than concatenating raw data.

**Delete the list later** &mdash; `del frames` releases the inputs. This Else stay referenced.

For files larger than memory in total, the answer isn't pandas. Read in chunks and aggregate incrementally, or use Dask, DuckDB or Polars, all of which are built for it.

## A summary

**Same columns, more rows** &mdash; `concat([a, b], ignore_index=True)`.

**Same rows, more columns, aligned by label**. `concat([a, b], axis=1)`, only when the indexes truly match.

**Joining on a key** &mdash; `merge`, not concat.

**Many files** &mdash; a list comprehension and one concat, with a source tag.

**Recording provenance** &mdash; `keys=`, or an clear column.

And later, three checks: the row count, `dtypes`. `isna().mean()`. Between them they catch the mismatched columns, the promoted types and the frames that weren't what you assumed.

## Concat versus merge, decided

The question that settles it: are you adding **rows of the same kind**, or **columns about the same rows**?

Same kind of rows &mdash; this month's data added to last month's &mdash; is `concat`.

Columns about the same rows, matched on a key. Adding customer details to orders &mdash; is `merge`.

`concat(axis=1)` looks like the second but matches on the **index**, not on a key column. It's right only when the indexes were on purpose made to match. This Is rarer than it looks.

If you find yourself resetting indexes so a `concat(axis=1)` lines up, the step you wanted was a merge.

## Checking after a concat

Three lines, and each catches a other failure:

```python
len(out) == sum(len(f) for f in frames)   # nothing lost or duplicated
out.dtypes                                # nothing promoted to object
out.isna().mean()                         # which columns only some files had
```

The third is the one that finds a column renamed partway through a series of files. It appears as two columns, each populated for part of the rows, and the totals look plausible.

## Keys and provenance

`keys=["jan", "feb"]` adds an index level naming the source.

`names=["month"]` names that level, so `reset_index` makes a sensible column name rather than `level_0`.

For a flat result, a column is simpler:

```python
frames = [d.assign(source=name) for name, d in items]
```

Either way, recording where a row came from is worth doing at the moment of mixing. Later the data is gone and rebuilding it means remembering row counts.

## A closing note

`concat` is simple enough that its failures are all about expectations rather than mechanics.

The row-stacking case is nearly always right. The two things to note are `ignore_index=True` and that columns match by name. A renamed column in one file turns two half-full columns rather than an error.

The column-stacking case is the one to be suspicious of. It aligns on the index. Indexes drift apart the moment anything is filtered. If the frames should match row for row, reset both indexes and say so. If they should be matched on a key, the step is a merge.

And the loop rule applies here as all over. Collect the pieces, combine once. It's the same lesson as `np.append` and `df.loc[len(df)]`. It's the single most common avoidable slowdown in code that reads many files.

## Two more things worth knowing

`pd.concat` accepts a **dict** and a list, in which case the keys become the outer index level on its own: `pd.concat({"jan": a, "feb": b})` is the same as passing `keys=`. That reads well when the pieces already live in a dict keyed by their source.

The `axis` arg also accepts the string names `"index"` and `"columns"`. This Are harder to misread than `0` and `1` in code someone else will maintain.

And one action worth expecting: concatenating frames whose columns are in other orders makes the union in order of first appearance, not sorted, unless you pass `sort=True`. Two files exported months apart with the columns reordered will so combine right but present in an order that matches neither. This Is harmless and briefly confusing.

## Combining results, not raw data

The most scalable use of `concat` is on **summaries** rather than on source data.

Reading a hundred files and concatenating them raw builds one frame holding all. Peak memory is roughly twice its final size because the pieces stay alive until the concat returns. Reading each file, reducing it to what the question needs. Concatenating the small results costs a fraction of that and scales to more files than fit in memory.

```python
parts = []
for path in paths:
    d = pd.read_csv(path, usecols=COLS, dtype=DTYPES)
    parts.append(d.groupby("city", as_index=False)["sales"].sum())
out = pd.concat(parts, ignore_index=True).groupby("city", as_index=False).sum()
```

The double aggregation is the pattern: reduce per file, combine, reduce again. It works for sums, counts and maxima. Anything associative. And not for medians or exact distinct counts. This Need the whole dataset at once.

That gap, between aggregations that break down and those that don't, is worth knowing before designing a pipeline around chunked reading.

## In summary

Row stacking aligns columns by name. Column stacking aligns the index by label. Knowing which axis you're joining along tells you which axis is doing the matching. That predicts each surprise this function makes.

Pass `ignore_index=True` unless the labels mean a thing, record provenance with `keys=` or an clear column. Never call it inside a loop.

later, check the row count, the dtypes and the missingness. Between them they catch the mismatched columns, the promoted types. The file whose schema quietly changed.
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
intro: SQL-style joins, and the copy key that silently times your rows.

## The four kinds

`merge` mixes two frames on one or more key columns. `how` decides what happens to keys that appear on only one side.

`inner` &mdash; only keys present in both. **This is the default**. It means unmatched rows are silently discarded.

`left` &mdash; each row from the left frame, with `NaN` where the right had no match. This is often what you want when enriching a table with a lookup: you're adding data, not filtering.

`right` &mdash; the mirror image, and rarely used, since swapping the operands is clearer.

`outer` &mdash; each key from either side.

The default being `inner` is worth remembering. A join that was meant to add a column can quietly drop rows. The only sign is a row count you weren't checking.

## Check what happened

Two habits catch nearly each join problem.

**Compare row counts.** `len(before)` against `len(after)`. If a left join changed the count, a thing is duplicated. If an inner join dropped rows, some keys didn't match.

**Use `indicator=True`.** It adds a `_merge` column with values `left_only`, `right_only` or `both`. `value_counts()` on it summarises the whole join in one line.

That is far better than guessing. It tells you not just that rows went missing but which ones. You can look at them and find out whether the key is misspelled, differently typed, or truly absent.

A frequent cause of a "failed" join is a **dtype mismatch**: `1` as an int on one side and `"1"` as a string on the other never match. Nothing warns. Checking both key columns' dtypes takes a second.

Whitespace and case do the same thing to string keys. This Is why the cleaning modules come before this one.

## The duplicate-key multiplication

This is the most damaging silent bug in pandas.

If a key appears twice on the right, each matching left row is duplicated. Two orders joined to a lookup with a repeated id give three rows. The frame still looks like orders, still has an `amount` column. Each sum found from it's now wrong.

Nothing warns, because a many-to-one join *turning* many-to-many is a legitimate step. Pandas can't know you didn't intend it.

The results are quiet and severe: inflated revenue, double-counted users, a model trained on duplicated rows.

## validate

`validate=` states the link you expect and raises if it doesn't hold:

`"one_to_one"` &mdash; keys unique on both sides.

`"one_to_many"` &mdash; unique on the left.

`"many_to_one"` &mdash; unique on the right. This is the common case for a lookup table. The one worth reaching for by default when joining link data.

`"many_to_many"` &mdash; no constraint. This Is the current action spelled out loud.

Adding it costs one arg and converts an invisible data-corruption bug into a clear exception at the point it happens. On any join that feeds a number someone will act on, it's worth having.

## Different names, colliding names

`left_on` and `right_on` join columns with other names. `left_index=True` / `right_index=True` use the index on that side.

When both frames have a column with the same name that is *not* a key, pandas keeps both and appends `_x` and `_y`.

That is where a subtle error lives: `v_x` and `v_y` both look plausible. Picking the wrong one makes a working analysis of the wrong column. Set `suffixes=("_orders", "_lookup")` so the names say where they came from, or drop the redundant column before merging.

## join

`df.join(other)` is `merge` with the index as the key. It defaults to a **left** join rather than an inner one.

Two other defaults for two similar methods is a genuine wart. When it matters, use `merge` with clear args. `join` is a convenience for the index case.

Index joins are faster than column joins on a sorted, unique index. This Is a reason to `set_index` on a key you join on again and again rather than passing `on=` each time.

## An order of operations

Clean the keys &mdash; type, case, whitespace. Check uniqueness on the side that should be unique. Choose `how` on purpose rather than taking the default. Add `validate`. Compare row counts later.

That sounds like a lot for one step. It's five seconds of typing. Joins are where the costly, silent errors live.

## Joining on several keys

`on=["date", "store"]` joins on a composite key. Both frames need all the named columns. Rows match only when **each** key agrees.

The usual failure is a type mismatch on one of a few keys. The dates match but one side stores the store id as text. The join then returns far fewer rows than expected. `indicator=True` shows a large `left_only` count without saying why.

Checking the dtypes of each key column on both sides takes one line:

```python
print(left[keys].dtypes, right[keys].dtypes, sep="\n")
```

## Joins that filter

Two common intentions are filters rather than enrichments.

**Keep rows whose key exists elsewhere**. A semi-join. pandas has no dedicated method. `df[df["id"].isin(other["id"])]` is the right setup. It can't times rows. This An inner join can.

**Keep rows whose key doesn't exist elsewhere**. An anti-join. `df[~df["id"].isin(other["id"])]`, or an outer join with `indicator=True` filtered to `left_only` when you also want the other side's columns.

Using a merge for either is a common way to add accidental row product.

## Ordered and nearest-match joins

`pd.merge_ordered` merges two sorted frames and can fill forward across the join. This Suits time series with other sampling.

`pd.merge_asof` joins on the **nearest** key rather than an exact match. This Is the standard tool for joining a reading to the most recent preceding link value. A trade to the latest quote, a reading to the last tuning.

Both need sorted inputs and both are much faster than the option of a cross join and a filter. This On real data doesn't fit in memory.

`direction="backward"` (the default), `"forward"` or `"nearest"` and a `handling` control the matching.

## Performance

Merging is roughly `O(n + m)` with hashing, and the hands-on costs are elsewhere:

**Key dtype.** Joining on ints or cats is faster than on strings.

**Index joins.** A sorted, unique index makes `join` faster than a column merge. This Is a reason to `set_index` on a key used again and again.

**Result size.** A many-to-many join can give a frame far larger than either input. Checking the expected size before running it. The product of the group counts. Avoids allocating a thing that doesn't fit.

**Column count.** Selecting only the columns you need from the right frame before merging avoids carrying passengers through the join and into memory.

That last one is the easiest win: `left.merge(right[["id", "label"]], on="id")` rather than merging the whole of `right`.

## A merge checklist

Before:

Clean both key columns &mdash; type, case, whitespace.

Check uniqueness on the side that should be unique.

Select only the columns you need from the right frame.

During:

Choose `how` on purpose. The default is `inner`.

Set `validate` to the link you expect.

Set `suffixes` if column names share.

Add `indicator=True` while developing.

After:

Compare row counts with the input.

Check the `_merge` counts.

Check `isna()` on the newly added columns. A left join that matched nothing gives a column that is fully null. This Is easy to miss and obvious once looked for.

## What to do when a join goes wrong

A structured approach beats guessing, and it takes about a minute.

**Row count changed unexpectedly?** A duplicated key on one side. Check `is_unique` on both, and use `validate`.

**Rows missing?** An inner join with unmatched keys. Switch to `how="left"` and `indicator=True` to see which.

**all unmatched?** A dtype mismatch on the key, or whitespace or case in a string key. Compare `dtypes` and look at a few values from each side.

**New columns fully null?** The join matched no rows, or matched on the wrong column.

**surprise `_x` / `_y` columns?** shared non-key names. Set `suffixes`, or select the columns you need before merging.

The tool for the first three is `indicator=True`. The habit of checking `len(before)` to `len(after)` catches all of them earlier than anything else.

## Joining a summary back to detail

A frequent shape: find a per-group statistic, then attach it to each row.

The merge version works and has three steps and a risk.

The `transform` version has one step and no risk:

```python
df["city_total"] = df.groupby("city")["sales"].transform("sum")
```

Reaching for a merge where a `transform` fits is one of the most common not needed joins. It's worth recognising because the merge route is where the row-product bugs live.

## Set-like operations without a join

a few questions phrased as joins are really membership tests:

"Which of these ids exist in that table?" &mdash; `isin`.

"Which don't?" &mdash; `~isin`.

"What is the share between two key sets?". `a.index.intersection(b.index)`, or set steps on the columns.

All three avoid the join machinery fully and can't change the row count. This Makes them both safer and clearer when the answer is a filter rather than an enrichment.

## A summary

`how="inner"` is the default and drops unmatched rows silently.

`indicator=True` while developing. It shows the result.

`validate=` states the link and turns silent product into an error.

Clean and type-check the key columns first. Most failed joins are dtype or whitespace.

Select only the columns you need from the right frame.

Set `suffixes` when names share.

`join()` merges on the index and defaults to `left`, unlike `merge`.

Use `transform` instead of a self-join for group statistics. `isin` instead of a join for membership.

And compare row counts before and after, each time.

## A closing note

Joins are where the costly, quiet errors live.

An inner join silently drops the rows that didn't match. A duplicated key on either side silently times the rows that did. Neither raises, both give output of the right shape. Each number found later is wrong in a way that looks fair.

Three habits reduce almost all of it to nothing. Check the key columns' dtypes before joining. Most "nothing matched" cases are an int against a string. Pass `validate=` to state the link you expect. And compare the row count before and after, each single time.

Those cost a few seconds and replace the option. This Is discovering months later that a total has been inflated because one link table gained a copy.

And a good share of joins aren't joins at all. A group statistic wants `transform`. A membership test wants `isin`. Both are safer. Neither can change the number of rows.

## One more thing

`merge` accepts `how="cross"`, making each mix of rows from both frames. It's at times what you want. Building a full grid of params, or each store crossed with each date. And it's worth knowing that the result's size is the product of the inputs. This Grows alarmingly fast.

For the common case of filling out a full grid before joining sparse data onto it, `pd.MultiIndex.from_product` and `reindex` are often the better route.

## In summary

The default is an inner join. This Drops unmatched rows without a word. A duplicated key on either side times rows without a word either.

Both are blocked by the same short routine. Clean and type-check the keys, assert uniqueness where you assume it, pass `validate=`. Compare the row count before and after.

And a good number of steps phrased as joins aren't. A group statistic is `transform`. A membership test is `isin`. Both are safer. Neither can change how many rows you've.
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

**Long** (or tidy) has one row per finding, with columns naming the var and holding the value. City, year, sales. Four rows for two cities over two years.

**Wide** has one row per subject and a column per var. Two rows, one per city, with a `2023` and a `2024` column.

Neither is more correct. They suit other purposes. Most real work involves converting between them.

Long form is better for **storage and math**. Adding a year adds rows, not columns. Nothing downstream changes. Group-by works on its own. Missing mixes simply don't appear. DBs and most plotting libraries expect it.

Wide form is better for **reading**. A table with years across the top is what people want to look at. It's what a spreadsheet or a report needs.

## pivot

`df.pivot(index="city", columns="year", values="sales")` goes long to wide.

Three args: what turns the row index, what turns the columns, and what fills the cells.

`pivot` is strict. If a given index/column pair appears more than once, it **raises**. There's no way to decide which value wins. That strictness is a feature. It tells you the data isn't what you assumed rather than silently keeping one row.

## pivot_table

`pivot_table` is the general version: when a cell has a few values, it **aggregates** them.

```python
df.pivot_table(index="city", columns="plan", values="sales", aggfunc="sum")
```

`aggfunc` defaults to `"mean"`. This Is worth knowing before it surprises you. A pivot table of sales that means when you expected a total looks fully plausible.

`fill_value` replaces the `NaN` in empty cells, often with 0.

`margins=True` adds row and column totals, labelled `All`.

A list for `aggfunc` gives a few statistics. A list for `index` or `columns` gives nested axes.

One wart, current as of pandas 2.2: `"size"` inside an `aggfunc` **list** raises `AttributeError`, while `"count"` in the same spot works. `groupby(...).agg(["sum", "size"])` handles it without complaint. Is the fallback when you want a row count alongside other statistics. The gap between the two is the one from the group-by module. `size` counts rows, `count` counts non-missing values.

`pivot_table` is group-by with a nicer layout. Anything it does can be done with `groupby` plus `unstack`. It's worth using when the output is a table for a human.

## melt

`melt` goes wide to long.

```python
wide.melt(id_vars="city", var_name="year", value_name="sales")
```

`id_vars` are the columns to keep as identifiers. all else is unpivoted into two columns. One holding the old column names, one holding the values.

Name both outputs. The defaults are `var` and `value`. This Say nothing and have to be renamed later anyway.

`value_vars` restricts which columns are melted, when you want to unpivot some and keep others as identifiers.

This is the step for data that arrived from a spreadsheet with one column per month. A shape that is convenient to type and painful to find with.

## stack and unstack

The same reshape expressed through the index.

`stack()` moves the innermost **column** level into the index, making the frame taller and narrower. `unstack()` moves the innermost **index** level into the columns.

These are what you reach for after a group-by with a few keys. Here The result already has a MultiIndex. `groupby(["city","year"]).sum().unstack()` gives the wide table right.

`unstack(fill_value=0)` fills the gaps, and `unstack(level=0)` chooses which level moves when there are more than two.

## Which to work in

The hands-on advice is to **keep data long and pivot at the end**.

The reason is maintenance. In wide form, a new year means a new column. Each formula that named the old columns has to change. In long form it means new rows, and nothing changes at all.

Long form also composes with all else in pandas. Group-by, filtering, joins all assume one row per finding.

Pivot when the output is a table someone will read, a chart, or a file for a tool that expects wide. That is a display step. It belongs at the end of the pipeline rather than the middle.

## Tidy data

The long form has a name and a meaning, from Hadley Wickham's tidy data:

Each **var** is a column. Each **finding** is a row. Each type of observational unit is a table.

Data that follows those rules composes with all: group-by, filtering, joins and most plotting libraries all assume it.

The common violations are worth recognising, because each has a standard fix.

**Column headers are values, not var names**. A column per year. Fix with `melt`.

**a few vars in one column**. A `measure` column holding both height and weight. Fix with `pivot`.

**vars in both rows and columns**. Fix with `melt` then `pivot`.

**a few values in one cell**. `"a, b, c"` in one field. Fix with `str.split` and `explode`.

## explode

`df.explode("tags")` turns a column of lists into one row per element, repeating the other columns.

It's the tool for data that arrived with a few values per cell:

```python
df.assign(tag=df["tags"].str.split(",")).explode("tag")
```

Each tag turns its own row, at which point it can be grouped and counted most times.

The inverse is a group-by with `list` or `", ".join` as the aggregation.

`explode` makes copy index labels, so `reset_index(drop=True)` often follows.

## pivot_table in more depth

Beyond the basics, three args do real work.

`aggfunc` accepts a **dict** keyed by column. Other values can be summarised differently in one table.

`index` and `columns` accept **lists**, giving nested axes. Region and city down the side, year and quarter across the top.

`dropna=False` keeps columns that are fully empty. This Matters when the table must have a fixed shape for compare.

`margins_name` renames the `All` row and column.

The output is a frame with a MultiIndex on one or both axes. The flattening step from the MultiIndex module often follows if the result is going anywhere other than the screen.

## Reshaping and memory

Wide data with many empty cells is sparse. Pivoting long data into it can allocate far more than the input.

A long frame with 100,000 rows covering 5,000 users and 3,000 products pivots into a 15,000,000-cell table, most of it `NaN`. The long form held 100,000 values.

That is the main hands-on arg for staying long: the wide form materialises each mix, whether or not it occurred.

When a wide layout is truly needed for a sparse dataset, `pivot_table` with `fill_value=0` at least avoids the float promotion that `NaN` forces. A sparse dtype or a other tool is worth considering past a certain size.

## Which operation, by shape

**Long to wide, no copies** &mdash; `pivot`.

**Long to wide, with aggregation** &mdash; `pivot_table`.

**Wide to long** &mdash; `melt`.

**Column level into index** &mdash; `stack`.

**Index level into columns** &mdash; `unstack`.

**Lists in cells into rows** &mdash; `explode`.

**A rate table of two vars**. `crosstab`, or `groupby` plus `unstack`.

The solid way to choose is to write down the shape you've and the shape you want, in rows and columns. Pick the step that moves one to the other. Reshaping goes wrong when it's attempted by trial and error rather than by naming the target.

## Reshaping for a chart

Most plotting expects one of two shapes. Knowing which saves a lot of trial and error.

`df.plot()` on a **wide** frame draws one line per column, using the index as the x-axis. That is why `groupby(...).unstack().plot()` works so neatly. Unstack makes just that shape.

Seaborn and similar libraries often want **long** data, with columns naming the var and the value. A `hue=` arg doing the splitting.

So the reshape before plotting depends on the library. It's often one call in either direction. Knowing which shape the function wants is faster than adjusting the data until the chart looks right.

## Round-tripping

`melt` then `pivot` returns to where you started, given the identifier columns uniquely find a row. If they don't, `pivot` raises on copies. Which is a handy check that the identifiers are what you thought.

That round trip is a quick way to test an assumption about the data's grain. If `pivot` complains, the key you believed was unique isn't.

## Column names after reshaping

`pivot` and `pivot_table` use the values of the `columns` arg as column names. The result's columns are data. That has two results.

They may not be valid identifiers. A year is an int, a product name may hold spaces. So `df.column_name` won't work and `df["2024"]` may need to be `df[2024]`.

They change when the data changes. Code that names them breaks when a new group appears. This Is the maintenance arg for staying long.

`rename_axis(columns=None)` drops the axis name that pivoting leaves behind. This Else shows up as a stray label above the columns when printing.

## A summary

Long is one row per finding. Wide is one row per subject.

`pivot` for long to wide with unique pairs. `pivot_table` when aggregation is needed.

`melt` for wide to long, naming both output columns.

`stack`/`unstack` do the same through index levels.

`explode` for lists in cells.

Wide materialises each mix, so it can be far larger than the long form.

Work long, pivot at the end, for display.

And when a reshape is confusing, write down the shape you've and the shape you want. The step follows from that. Trial and error rarely settles.

## A closing note

Reshaping is the step people most often approach by trial and error. The one where that approach works worst.

The solid method is to write down the shape you've and the shape you want. What is a row, what is a column. And pick the step that moves between them. Long to wide is `pivot`, or `pivot_table` if any cell would hold more than one value. Wide to long is `melt`. Through the index instead of named columns, it's `stack` and `unstack`.

The default that catches people is `pivot_table`'s `aggfunc="mean"`. A table of sales that quietly means where you expected a total looks fully plausible, and nothing shows else.

And the structural advice is to stay long until the end. Wide data materialises each mix whether it occurred or not. Each new group changes the columns. And so each formula that names them.

## One more thing

`melt` accepts `ignore_index=False`, which keeps the first index rather than renumbering. That matters when the identifiers you want to keep are in the index rather than in columns, since `id_vars` only names columns.

And `wide_to_long` handles the exact case of columns named with a stem and a suffix. `sales_2023`, `sales_2024`. Unpivoting them into a stem column and a suffix column in one call. This Is else a `melt` followed by a `str.extract`.

## In summary

Long form is one row per finding and composes with all. Wide form is one row per subject and reads better.

Convert with `pivot` and `melt`, or through the index with `stack` and `unstack`. Use `pivot_table` when a cell could hold more than one value. Remembering that its `aggfunc` defaults to `mean`.

Work long and pivot at the end. In wide form a new group is a new column. Each formula that named the old columns has to change.
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

Almost no one makes a MultiIndex on purpose. It appears as the result of steps you were doing anyway:

`groupby(["city", "year"])` gives one level per key.

`concat(..., keys=[...])` adds a level naming the source.

`stack()` moves a column level into the index.

`agg` with a few statistics per column gives nested **columns**.

So the hands-on question is rarely "should I build one" and almost always "I have one, now what".

## Selecting

The mental model: a tuple handles the levels in order, the way a nested dict would.

`s.loc["pune"]` selects on the outer level and returns a sub-object with that level dropped.

`s.loc[("pune", 2024)]` handles both levels and returns a scalar.

`s.loc[["pune", "delhi"]]` takes a list of outer keys.

The awkward case is selecting on an **inner** level while taking all from the outer one. Two ways:

`s.xs(2024, level="year")` is the readable form for a single cross-section.

`s.loc[(slice(None), 2024), ]` is the general form. `slice(None)` is the wildcard, needed because you can't write a bare colon inside a tuple. `pd.IndexSlice` makes it look more like normal slicing: `s.loc[pd.IndexSlice[:, 2024]]`.

Pick on inner levels often needs a **sorted** index. `sort_index()` first if you get a `UnsortedIndexError`. As a habit after building one.

## Aggregating over a level

`s.groupby(level="city").sum()` merges one level, keeping the others.

That is often what you want when the keys are already in the index. There's no need to `reset_index` and group by the column again.

`sum(level=...)` used to exist as a shortcut and was removed. `groupby(level=...)` is the current spelling.

`unstack()` moves a level into the columns and is often more handy than aggregating. It turns a two-level Series into a readable two-dimensional table.

## Hierarchical columns

`df.groupby("city").agg({"sales": ["sum", "mean"]})` gives columns that are tuples: `("sales", "sum")`.

Selecting needs the tuple: `out[("sales", "sum")]`.

This is where named aggregation earns its place. `agg(total=("sales", "sum"), avg=("sales", "mean"))` makes flat column names and skips this problem fully.

When you do end up with nested columns, flattening is one line:

```python
out.columns = ["_".join(c).strip("_") for c in out.columns]
```

Losing that step is a common source of confusion later, when a thing downstream can't find a column called `sales` because the column is really `("sales", "sum")`.

## When to keep it, when to flatten

**Keep it** when you're going to select through it, `unstack` it into a table, or aggregate over its levels. For truly nested data. Country/region/city, or a panel indexed by entity and date. It's the right structure and makes those steps natural.

**Flatten it** when the result is leaving pandas or going into an step that doesn't care about tree. A merge, a CSV, a plotting call, a model.

`reset_index()` turns index levels into plain columns. `groupby(..., as_index=False)` avoids creating one in the first place.

The honest summary is that a MultiIndex is powerful and awkward in roughly equal measure. It rewards you when the tree is real and the steps use it. It costs you an extra concept at each step when it's merely an artefact of how the result was found. Most of the time, in plain analysis code, flattening early is the kinder choice.

## Building one deliberately

at times you want a MultiIndex before any group-by:

`pd.MultiIndex.from_tuples([...], names=[...])` &mdash; from clear pairs.

`pd.MultiIndex.from_product([["a","b"], [2023, 2024]])` &mdash; each mix. This Is how you build a full frame to reindex sparse data onto.

`pd.MultiIndex.from_arrays([...])` &mdash; from parallel label arrays.

`df.set_index(["city", "year"])` &mdash; from existing columns. This Is the usual route.

`from_product` plus `reindex` is the standard way to make a sparse panel dense. Build each expected mix, reindex onto it. The missing ones appear as `NaN` rather than being silently absent.

## Sorting matters more here

Pick on inner levels needs a **lexsorted** index. Without it, pandas raises `UnsortedIndexError` or performs badly.

`df.index.is_monotonic_increasing` checks. `sort_index()` fixes.

The habit worth forming is to call `sort_index()` at once after building or reshaping a MultiIndexed object. It's cheap, it drops a class of error. It makes label ranges work.

`df.index.lexsort_depth` reports how many levels are sorted. This Shows why pick works on the first level and fails on the second.

## droplevel, swaplevel, reorder_levels

`droplevel("year")` drops a level fully. Handy after selecting a single value from it leaves a redundant level behind.

`swaplevel(0, 1)` exchanges two levels, and `sort_index()` later is almost always needed for the result to be usable.

`reorder_levels([...])` handles more than two.

These come up after a `groupby` made levels in an order that doesn't suit the next step, and they're cheaper than regrouping.

## Aggregating and selecting together

Two patterns cover most work with a MultiIndexed result.

**Collapse a level**: `df.groupby(level="city").sum()`.

**Move a level to columns**: `df.unstack("year")`, giving a wide table.

`unstack` takes a `level` by name or spot. `fill_value` for the gaps. Chaining `unstack().plot()` is the usual route from a two-key group-by to a chart.

`stack()` reverses it. In recent pandas it has a `future_stack=True` option that changes some edge-case action around missing values. The default is being migrated. Pinning the action by name is worth doing in code that must keep working.

## Should you use one at all

The honest spot: a MultiIndex is the right structure for truly nested data that you'll select through. An not needed complication else.

Signs it's earning its place:

You select by partial key regularly.

You aggregate over one level and keep the others.

You unstack it into tables.

The tree is real &mdash; a panel indexed by entity and time, geography at a few levels.

Signs it isn't:

You at once `reset_index()` after each step that makes one.

You're fighting `UnsortedIndexError` and `slice(None)`.

The result is heading for a merge, a CSV or a plotting call.

In the second case, `as_index=False` on the group-by avoids creating it at all. This Is simpler than creating and flattening.

## Getting values out

A recurring need is turning a MultiIndexed result into a thing plain code can use.

`reset_index()` &mdash; each level turns a column.

`reset_index(level="year")` &mdash; one level turns a column, the rest stay.

`droplevel("year")` &mdash; discard a level fully.

`to_frame()` on the index &mdash; the labels as a frame, for inspection.

`list(df.index)` &mdash; the labels as tuples.

`df.index.get_level_values("city")` &mdash; one level as a flat array. This Is what you want for filtering or for building a mask without resetting anything.

That last one is under-used: `df[df.index.get_level_values("year") == 2024]` filters on a level without any `slice(None)` syntax.

## Column MultiIndexes in particular

nested **columns** cause more day-to-day friction than nested rows. Most code expects flat column names.

They arrive from `agg` with a list of functions, from `pivot_table` with a few value columns, and from `unstack`.

The flattening idiom is worth storing:

```python
df.columns = ["_".join(map(str, c)).strip("_") for c in df.columns]
```

`map(str, ...)` matters because levels are often not strings. A year is an int, and `join` fails on it.

The better answer is often to avoid creating them: **named aggregation** makes flat names right. Is clearer at the call site as well.

## Performance

A MultiIndex is a set of int codes plus level values. It's compact. Often more so than the equal columns. Repeated labels are stored once.

Pick is fast on a lexsorted index and slow else. This Is why `sort_index()` matters here more than elsewhere.

Group-by on index levels is close to group-by on columns.

The costs are in usability rather than speed: more concepts, more edge cases. Code that other people find harder to follow.

## A summary

They arrive from group-by, `concat(keys=)`, `stack` and `agg` rather than being built.

A tuple handles the levels. `xs` takes a cross-section. `slice(None)` is the wildcard.

`sort_index()` after building one, always.

`groupby(level=...)` aggregates over a level.

`unstack` turns a level into columns and is often what you really wanted.

Flatten nested columns with a join over the tuples, or avoid them with named aggregation.

Keep it when the tree is real and you select through it. `reset_index()` when it's an artefact.

## Where it fits

nested indexes are the price of nested questions. A panel of entities over time, sales by region and city and month, a survey by respondent and question. All of these have a natural nesting. A MultiIndex expresses it right.

The friction comes when the nesting is incidental rather than real. A group-by on two keys makes one whether or not you wanted the structure.

The test is whether you'll use the tree. If the next step selects a level, aggregates over one, or unstacks it into a table, keep it. If the next step is a merge, a plot or a file, flatten it and move on.

Neither choice is permanent. `set_index` and `reset_index` are cheap and reversible. The choice can be made per step rather than committed to at the start.

The one thing worth doing always is `sort_index()` after building one. Almost each confusing MultiIndex error traces back to an unsorted index. The fix is a single call that costs nothing on data of plain size.

## Two more things worth knowing

`df.index.names` gives the level names and is writable. An index built without names can be labelled after the fact. Named levels make each later `groupby(level=...)`, `xs` and `unstack` call readable. Unnamed ones force you to count spots.

`pd.IndexSlice` deserves a mention on its own. Written as `idx = pd.IndexSlice`, it turns the awkward `df.loc[(slice(None), 2024), :]` into `df.loc[idx[:, 2024], :]`. This Is close enough to plain slicing to read at a glance.

Finally, a MultiIndex on the **columns** and one on the **rows** can coexist. This Is what `pivot_table` with lists for both `index` and `columns` makes. That is a truly handy shape for a printed report and a truly awkward one to find against. This Is the trade this whole module shows. The structure that displays best is rarely the structure that changes best.

## A worked selection

Putting the pick tools together on one object makes the pattern clearer than any of them alone.

Given sales indexed by `(city, year)`:

`s.loc["pune"]` &mdash; one city, all years, with the city level dropped.

`s.loc[("pune", 2024)]` &mdash; a single value.

`s.loc[["pune", "goa"]]` &mdash; two cities.

`s.xs(2024, level="year")` &mdash; one year, all cities.

`s.loc[pd.IndexSlice[:, 2024]]` &mdash; the same, in slice form.

`s[s.index.get_level_values("year") == 2024]` &mdash; the same again, as an plain mask. The form that composes with other rules.

`s.groupby(level="city").sum()` &mdash; totals per city.

`s.unstack("year")` &mdash; a table, cities down, years across.

Six ways to ask about one year. This Is a fair summary of why MultiIndexes feel heavy. The last two are the ones worth reaching for by default. Aggregate a level, or unstack it into a shape that reads.

## In summary

A MultiIndex arrives from steps you were doing anyway. The handy question is whether to keep it.

Keep it when the tree is real and the next step selects a level, aggregates over one, or unstacks it into a table. Flatten it when the result is heading for a merge, a file or a chart.

Sort it as soon as you build it. Most confusing errors here are an unsorted index. Use `xs` or a mask on `get_level_values` rather than fighting `slice(None)`. And prefer named aggregation. This Avoids nested columns fully rather than needing them to be flattened later.
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

all in this module depends on the frame having a `DatetimeIndex`. `resample` raises without one. Time-based windows have nothing to measure against.

`df.set_index("date")` after `pd.to_datetime` is the usual setup. It's the step people skip before wondering why `resample` won't run.

Once the index is a timeline, pandas can do things that would else need a lot of math. Select a month by name, aggregate by period, window by duration rather than by row count.

## resample

`resample` is group-by where the groups are time periods.

**Downsampling** &mdash; daily to monthly &mdash; aggregates. Takes the same methods as `groupby`: `sum()`, `mean()`, `agg(["sum", "mean"])`.

The rate string is the arg that matters. `D` daily, `W` weekly, `ME` month end, `MS` month start, `QE` quarter end, `YE` year end, `h` hourly, `min` minutely.

Note that pandas 2.2 **renamed** a few of these. `M` became `ME`, `H` became `h`, `T` became `min`. Older code and older tutorials use the old spellings. This Now warn or fail based on version. If a rate string doesn't work, that rename is the likely reason.

The label of each output row is the **end** of the period for `ME`. The start for `MS`. `label=` and `closed=` control which boundary is used and which side is inclusive. They matter when periods must line up with a thing external.

## Upsampling invents rows

Going to a finer rate creates rows that didn't exist, and they start as `NaN`.

`asfreq()` leaves them empty. This Is honest and rarely handy on its own.

`ffill()` carries the last known value forward. That asserts the value **held constant** until the next finding. Correct for a price, a status, a setting.

`interpolate()` fits between the known points. That asserts the value **moved smoothly**. Correct for a temp, a spot, anything smooth.

These are other claims about the world. Choosing between them is a modelling choice rather than a formatting one. Both fabricate data. The question is which fabrication is less wrong for what the number means.

## rolling

`s.rolling(3).mean()` gives a moving mean over the last three **rows**.

The first two results are `NaN`. The window isn't yet full. That is deliberate. A three-row mean found from one row isn't a three-row mean. `min_periods=1` replaces it and starts finding at once. This Is convenient and slightly dishonest at the edges.

`s.rolling("3D")` windows by **time** rather than row count. This is the one to use when findings are irregularly spaced. Three rows might span three days or three months. Only the time-based window means what you said.

`center=True` puts the window around each point rather than behind it. It's right for smoothing a curve for display and wrong for anything predictive. It uses future values.

`expanding()` is a window that grows from the start. A running total or a cumulative mean.

`ewm()` gives fast weighted statistics. Here Recent findings count for more.

## shift, diff, pct_change

`shift(1)` moves each value down one row. Each row can see the previous one. `shift(-1)` looks forward.

`diff()` is `s - s.shift(1)`. `pct_change()` is the scaled version.

These are how you build lagged features, growth rates and change spotting. The first row is always `NaN`. It has no predecessor.

Within groups, use the group-by versions. `df.groupby("id")["v"].diff()`. Or the shift crosses from one entity into another and makes a gap between unrelated rows. That is a common and quiet error in panel data.

## Order is assumed, not checked

each step here &mdash; `shift`, `diff`, `rolling`, `resample` &mdash; assumes the rows are in time order.

pandas does **not** verify it. `diff()` on unsorted data returns numbers, and they're meaningless.

`sort_index()` before any of these on data you didn't sort yourself. It's one line. The failure it blocks makes plausible output rather than an error.

The same applies to duplicated timestamps: two rows for the same instant make `diff` and `rolling` ambiguous. Are often a sign of a data problem worth looking at before aggregating over it.

## Frequency strings

The alias is the arg that decides what `resample` and `date_range` do. Pandas 2.2 renamed a few of them.

`D` day, `B` business day, `W` week (ending Sunday by default, `W-MON` to change it), `MS` month start, `ME` month end, `QS`/`QE` quarter, `YS`/`YE` year, `h` hour, `min` minute, `s` second.

The renames: `M` to `ME`, `H` to `h`, `T` to `min`, `S` to `s`. Older code and most tutorials use the old spellings. This Now warn or fail. When a rate string doesn't work, this is the first thing to check.

Multiples work: `"15min"`, `"2W"`, `"3ME"`.

Anchored offsets pin the boundary: `"W-FRI"` for weeks ending Friday, `"QE-JAN"` for quarters ending in January. This Matters for fiscal years that don't start in January.

## Which label a period gets

`resample("ME")` labels each group with the **end** of the period. `"MS"` with the start.

`label="left"` or `"right"` replaces which boundary names the group. `closed=` decides which end is inclusive.

These matter when the output must line up with a thing made elsewhere. A monthly total labelled 2024-01-31 and one labelled 2024-01-01 are the same number with other index labels, and joining them gives nothing.

Settling on a rule early. Often period start &mdash; saves reconciliation later.

## Grouping by time and something else

`resample` groups by time only. To group by time **and** a group, `pd.Grouper` mixes with plain keys:

```python
df.groupby([pd.Grouper(key="date", freq="ME"), "city"])["sales"].sum()
```

`key=` names the date column. So This works without setting an index. This Is what makes `Grouper` more handy than `resample` .

The result is a MultiIndex, and `unstack("city")` gives the wide table.

## Rolling in more depth

`min_periods` decides how many findings a window needs before making a value. The default for a fixed-size window is the window size. For a time-based window it's 1.

`closed=` controls whether the window includes its endpoints. This Matters for time-based windows where an finding may sit just on the boundary.

`win_type` gives weighted windows &mdash; Gaussian, tri &mdash; for smoothing.

`rolling(...).apply(func, raw=True)` runs a custom function per window. `raw=True` passes a NumPy array rather than a Series and is much faster.

Within groups, `df.groupby("id")["v"].rolling(3).mean()` windows inside each group and returns a MultiIndexed result. This Often needs `droplevel(0)` before it can be assigned back.

## Gaps, and what they hide

A rolling window over rows assumes the rows are evenly spaced. Real time series have gaps. Weekends, outages, missing readings. And a three-row window may span three days or three weeks.

Two fixes:

**Window by time**: `rolling("3D")` means three days whatever the row spacing.

**Regularise first**: `resample("D").mean()` produces a row per day, with `NaN` where there was no data, after which row-based windows mean what they say.

Which is right depends on whether an absent finding should count as missing or simply not exist. That is a modelling question. `resample` forces you to answer it. This Is an arg for doing it early.

## A checklist for time-series work

Parse the dates and check the dtype.

Set a `DatetimeIndex`, or plan to use `pd.Grouper(key=...)`.

`sort_index()`.

Check for duplicated timestamps.

Decide on a time zone, or commit to naive throughout.

Decide whether gaps are missing or absent, and smooth if they're missing.

Then `resample`, `rolling` and `shift` mean what they appear to mean.

## Aligning two series with different frequencies

A common task: daily data and monthly targets, joined for compare.

The wrong approach is a merge on dates. This Matches almost nothing.

The right approach is to bring both to the same rate first:

```python
monthly = daily.resample("MS").sum()
combined = monthly.join(targets)
```

Or, going the other way, upsample the monthly figure and forward-fill it so each day carries its month's target.

Which direction is right depends on the question. Aggregating up loses detail and is often correct for reporting. Spreading down invents precision and is often correct for per-row compare. Either way, the alignment step is clear rather than implied by a join.

`MS` versus `ME` matters here: two monthly series labelled at opposite ends of the month won't join at all.

## Lags and leads for modelling

`shift(1)` gives the previous value. A lag, safe to use as a predictor.

`shift(-1)` gives the next value. A lead. This Is the **target** in a forecasting problem and must never be a feature.

Using a lead as a feature is data leakage. It makes models that score beautifully and fail in production. Because both are one method with a sign, the mistake is easy to make and invisible in the code.

Rolling features have the same hazard: `rolling(3, center=True)` uses future values. For anything predictive, windows must look backwards only. This Is the default without `center`.

Within groups, all of these need the group-wise form, or the lag crosses from one entity to the next.

## Missing periods

A gap in a time series is either "no finding" or "no event". The two need other handling.

`resample("D").sum()` gives 0 for days with no rows. Correct if the series counts events.

`resample("D").mean()` gives `NaN` &mdash; correct if the series measures a thing that existed but wasn't recorded.

Choosing the wrong one makes a series that looks full and is wrong at just the notable points.

`asfreq()` makes the gaps clear without aggregating. This Is the honest first step when you aren't yet sure.

## A summary

A `DatetimeIndex` is the prerequisite for `resample` and time-based windows.

rate aliases were renamed in pandas 2.2 &mdash; `ME`, `h`, `min`.

Downsampling aggregates. Upsampling invents rows that need filling on purpose.

`ffill` asserts a value held. `interpolate` asserts it moved smoothly.

`rolling("3D")` for irregular spacing. `min_periods` for the edges.

`shift(-1)` is a lead and belongs only in a target, never a feature.

Use the group-wise forms on panel data.

`sort_index()` first, always, because none of these check.

## A closing note

Time series work rewards setting things up properly and punishes assumptions.

The setup is short: parse the dates with an clear format, check the dtype, decide on a time zone, set a `DatetimeIndex` if you need period pick. Sort. each step in this module assumes that order and none of them check it. `diff` on unsorted rows returns numbers that mean nothing.

The recurring choice is what a gap means. A day with no rows is either zero events or an unrecorded reading. `resample("D").sum()` and `.mean()` encode those two other answers. Choosing without noticing gives a series that looks full and is wrong just where the notable things happen.

And on panel data &mdash; a few entities stacked in one frame &mdash; `shift`, `diff` and `rolling` must be done within groups, or the compare runs across the boundary from one entity into the next and makes a plausible number from unrelated rows.

## One more thing

`resample` accepts `origin=` and `offset=`. This Control where the period boundaries fall. That matters for data that should be bucketed on a thing other than midnight or the first of the month. A business day starting at 6am, or weeks aligned to a fiscal calendar.
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
intro: read_csv's args, and the ones that prevent a class of bug.

## Inference is convenient and lossy

`read_csv` guesses a dtype per column. That is why it's pleasant to use and why the same three problems appear in almost each project.

**Leading zeros disappear.** An id column of `007`, `008` is read as ints. The zeros are gone permanently. No error. The values still look like ids.

**Dates stay text.** Nothing is parsed as a date unless you ask. The column sorts lexically, `.dt` doesn't work, and date math is down.

**One gap makes a column float.** NumPy ints can't hold `NaN`. A single missing value promotes the whole column, and ids print as `1001.0`.

All three are fixed at read time by saying what you know.

## The arguments that matter

`dtype={"id": str}` keeps identifiers as text. This is the fix for leading zeros. It should be the default for anything that is a code rather than a quantity. Postcodes, account numbers, phone numbers.

`dtype={"amount": "Int64"}` uses the nullable int type. So The column holds gaps without turning float.

`parse_dates=["joined"]` converts during the read. This Is faster than converting after. Add `date_format=` when the format is known and unambiguous.

`usecols=["a", "d"]` reads only the columns you name. On a wide file this saves both time and memory. It's the single most good arg for large data.

`nrows=1000` reads a sample. Always look at a sample of an unseen file before loading all of it. It's how you find out that the delimiter is wrong, or that there are three header rows, or that the file isn't what you were told.

`index_col="id"` sets the index during the read.

`na_values=["missing", "-999"]` adds markers. pandas recognises a standard list. Empty, `NA`, `N/A`, `null`, `NaN` and a few more. But it can't know that this dataset writes `missing`, or that `-999` is a sentinel. Left alone, the text markers make the column `object` and the numeric sentinel is treated as a real value. This Quietly poisons each mean.

`skiprows`, `header=None` and `names=[...]` handle files whose top isn't a clean header row.

`chunksize=n` returns an iterator of frames rather than one frame. This Is how you process a file larger than memory.

## Writing

`to_csv()` writes the index as an unnamed first column by default.

Read that file back and you get a spurious `Unnamed: 0` column. It's harmless, ubiquitous. Fully avoidable: **pass `index=False`** unless the index is real data.

Other args worth knowing: `float_format="%.2f"` controls precision, `columns=` selects what to write, `sep=` changes the delimiter. `encoding="utf-8"` is worth being clear about when the data leaves your machine.

## CSV loses what the frame knew

A CSV is text. all pandas knew about the data is discarded on the way out:

`Int64` turns plain `int64` on the way back, or `float64` if there were gaps.

`group` turns `object`, and the group order is gone.

Datetimes become strings again, unless the reader is told to parse them.

The index turns a column, or vanishes.

That round-trip loss is the arg for a binary format when the data is going to be read back by pandas:

**Parquet** (`to_parquet` / `read_parquet`) preserves dtypes, is columnar, compresses well. Is readable by many tools. It needs `pyarrow` installed. Which is why the editors here use CSV.

**Pickle** (`to_pickle`) preserves all just, including groups and custom objects. Is Python-exact, version-fragile. **runs code on load**. Never unpickle a file you didn't create.

**HDF5** suits very large numeric data with partial reads.

For anything you'll read back yourself, Parquet is often the right answer. For anything a human or another tool must read, CSV is worth its losses. But write down the dtypes one spot. The reader will have to guess just as you did.

## A loading routine

Read a sample with `nrows`. Look at it. Decide the dtypes, the date columns, the missing markers and the columns you really need. Then read the whole file with those args set.

That takes a minute and drops most of what the cleaning modules exist to fix.

## Files that are not quite CSV

Real exports are rarely clean, and `read_csv` has an arg for each common defect.

`sep="\t"` for tab-separated; `sep=None` with `engine="python"` sniffs the delimiter.

`skiprows=3` skips a preamble. `skiprows=lambda i: i % 2` skips selectively.

`header=None` with `names=[...]` handles a file with no header row.

`skipfooter=2` drops trailing summary lines, and needs `engine="python"`.

`thousands=","` parses `1,234` as a number rather than leaving it as text. Without it, a single formatted number makes the whole column `object`.

`decimal=","` handles European decimal commas.

`encoding="latin-1"` when UTF-8 fails. This Is the usual cause of a `UnicodeDecodeError` on files from older Windows tools.

`quotechar` and `escapechar` for embedded delimiters.

`comment="#"` skips comment lines.

When a file won't parse, working through that list is faster than writing a custom reader.

## Reading in chunks

`chunksize=n` returns an iterator of frames rather than one frame:

```python
totals = []
for chunk in pd.read_csv(path, chunksize=100_000):
    totals.append(chunk.groupby("city")["sales"].sum())
result = pd.concat(totals).groupby(level=0).sum()
```

That processes a file larger than memory, given the step can be done piecewise. Sums, counts and group sums can. A median can't, without more work.

The pattern is: reduce each chunk, collect the small results, combine at the end. Collecting the raw chunks and concatenating them defeats the purpose.

## Excel

`pd.read_excel(path, sheet_name="Sheet1")` needs `openpyxl` for `.xlsx`.

`sheet_name=None` reads **each** sheet into a dict of frames. This Is the quickest way to see what a workbook holds.

Excel files carry types, so dates often arrive parsed. But they also carry merged cells, hidden rows and formatting that mean nothing to pandas. A sheet that looks tabular on screen is often not.

`header=`, `usecols="B:D"` and `skiprows=` do the same jobs as in `read_csv`.

Writing a few frames to one workbook uses `pd.ExcelWriter` as a context manager, with one `to_excel` call per sheet.

## Compression and paths

`read_csv` and `to_csv` handle packing transparently from the extension: `.gz`, `.bz2`, `.zip`, `.xz`. A gzipped CSV is often a third of the size and costs little to read.

Both accept URLs and paths. This Is convenient for public datasets and a bad idea in production code. Here The file should be fetched and cached on purpose.

`pathlib.Path` objects work anywhere a path string does.

## Choosing a format

**CSV** &mdash; universal, human-readable, lossy about types, slow to parse. Right when a thing other than pandas must read it.

**Parquet** &mdash; typed, columnar, compressed, fast, readable by many tools. The right default for data pandas will read back. Needs `pyarrow`.

**Pickle** &mdash; preserves all just, Python-only, version-fragile. **runs code on load**. Fine for a short-lived cache you created. Never for input you didn't.

**JSON** &mdash; good for nested data, verbose for tabular, and `json_normalize` handles the flattening.

**HDF5** &mdash; large numeric arrays with partial reads.

**SQL** &mdash; when a few processes need the data, or it outgrows one machine.

The choice is mostly: who reads this next? If the answer is pandas, use Parquet. If it's a person or another tool, use CSV and accept the losses. If it's a system, use a DB.

## Writing for a round trip

If pandas will read the file back, the goal is to lose nothing.

Parquet does that: dtypes, groups and datetimes all live. It's smaller and faster than CSV.

If Parquet is down, CSV plus an clear read specification is the workaround. Record the dtypes alongside the file, and pass them on read:

```python
dtypes = df.dtypes.astype(str).to_dict()
json.dump(dtypes, open("schema.json", "w"))
```

That is clumsy and it works. What doesn't work is given the reader will infer the same types you had. Inference depends on the data and the data changes.

## Validating on load

The most handy place for checks is at once after reading. Here A problem is closest to its cause:

```python
df = pd.read_csv(path, dtype=..., parse_dates=[...])

assert list(df.columns) == expected_columns
assert df["id"].is_unique
assert df["date"].notna().all()
assert len(df) > 0
```

Column-name checks are the highest value of these. An upstream export that renames or reorders columns is common. Without a check the failure appears much later as a `KeyError` or, worse, as a column of the wrong data under the right name.

## Large files

The order to try, as a file grows:

`usecols` and `dtype` &mdash; often enough on its own, and always worth doing first.

`nrows` for development, so the edit-run cycle stays fast.

`chunksize` with per-chunk reduction, when the whole file can't be held.

Parquet, which reads only the columns requested and is far faster to parse.

A DB or DuckDB, when the data outgrows one machine's memory even column-wise.

Reaching for the last option first is a common mistake. `usecols` and `dtype` often make a "too large" file comfortable.

## A summary

`read_csv` infers, and inference loses leading zeros, leaves dates as text, and turns ints with gaps into floats.

`dtype`, `parse_dates`, `usecols` and `na_values` prevent all of that at read time.

Read a sample with `nrows` before committing to a large file.

`to_csv(index=False)` unless the index is data.

CSV loses types. Parquet doesn't.

`allow_pickle`-style trust applies to `read_pickle` too. Never load one you didn't create.

Validate at once after loading, above all the column names.

And for a large file, `usecols` and `dtype` are the first thing to try, not the last.

## A closing note

The boundary between a file and a DataFrame is where most silent damage happens. It's the cheapest place to prevent it.

`read_csv` guesses, and its guesses lose leading zeros, leave dates as text, and turn ints with a single gap into floats. each one of those is fixed by an arg, and each one of them is much harder to fix later. Leading zeros in given are gone for good.

The habit worth building is to read a sample first, look at it, decide the types. Then read the file properly. That takes a minute and replaces an afternoon of confused debugging.

On the way out, `index=False` unless the index is data. Parquet rather than CSV when pandas will be the one reading it back. CSV is a text interchange format. Treating it as a storage format means accepting that all the frame knew about its own types is discarded each time.

## One more thing

`read_csv` accepts a `converters` dict mapping column names to functions, applied during the read. It's slower than `dtype` and handles cases `dtype` can't. Stripping a currency symbol, parsing a bespoke format. Without a split cleaning pass later.

And `to_csv` with no path returns the CSV as a **string** rather than writing a file. This Is how you round-trip through `io.StringIO` in a test, or hand the text to a thing that wants a string rather than a filename.

## In summary

The read is where types are decided. Inference makes three predictable mistakes. Leading zeros lost, dates left as text, ints with a gap turned into floats.

`dtype`, `parse_dates`, `usecols` and `na_values` prevent all three, cost nothing. Are far cheaper than repairing the damage later.

Read a sample first and look at it. Validate the column names on load. Write with `index=False`. And when pandas will be the one reading the file back, use Parquet. CSV discards all the frame knew about itself.
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
intro: Where the time really goes, in the order worth fixing it.

## The order to work in

Pandas speed work is unusually predictable. In descending order of payoff:

1. **Drop per-row Python.** Worth 10&ndash;100x, and it's nearly always the whole problem.
2. **Right-size the dtypes.** Halves or better on memory. Speeds up all that touches the column.
3. **Filter early.** Free, and often the largest structural win.
4. **Reduce copies.** Worth a modest amount, and only in hot paths.
5. **Reach past pandas.** When the data or the method truly doesn't suit it.

Working down that list in order means the large wins come first. Working up it means spending an afternoon on step 4 while a `apply(axis=1)` sits untouched.

## Per-row Python

`df.apply(func, axis=1)`, `iterrows`, and a `for` loop over rows all do the same thing. Call back into the interpreter once per row.

The first editor measures four spellings of the same product. The vectorised form is orders of magnitude faster than `apply(axis=1)`. notably a plain `zip` over two columns beats `apply` comfortably. Because `apply` also builds a Series object per row.

The hands-on rule: if a lambda indexes into a row, the step is column math in disguise.

## iterrows

Worth singling out because it's common and there's no situation where it's the right choice.

It's much slower than `itertuples`, and it **converts each row to a Series**. A row holding an int and a string turns an `object` Series. The int arrives as an object. Code that then does math on it's slower again, and code that checks types breaks.

`itertuples` is faster and preserves dtypes. If you must iterate, use that. Better still, don't iterate.

## dtypes

Covered in its own module, and it belongs here too because memory and speed are the same problem. Less data to move is less time spent moving it.

`group` for repeated text is the biggest single win on most real frames. It speeds up group-by and compare and saving memory. `to_numeric(downcast=...)` narrows numeric columns.

The third editor shows both applied to one frame.

## Filter early

each step costs in proportion to the rows it touches. Filtering to 5% of the data before finding means each later step does 5% of the work.

This is obvious stated plainly and routinely done backwards. A filter reads more on its own at the end of a chain than in the middle of one. `df.assign(...).query(...)` finds for each row and then throws most of them away. `df.query(...).assign(...)` doesn't.

The same applies to columns: `usecols` at read time. Dropping columns you won't use, both reduce all downstream.

## Copies

Most pandas steps return a new object. A chain of three `assign` calls allocates three frames.

That is often the right trade. The chain is readable, doesn't mutate anything. Works well in a notebook. The cost only matters inside a loop or on a frame large enough that allocation dominates.

Two things to know rather than to apply all over. Direct set (`df["b"] = ...`) modifies in place and skips the copy. `inplace=True` on other methods often does **not** avoid a copy despite its name, while breaking chaining and returning `None`. It isn't the tuning it appears to be.

## Measure

The last editor times four steps on the same frame. The ranking isn't what most people would guess. It changes with the data.

`%timeit` in a notebook, or `time.perf_counter` around a block, is enough for most choices. Take the best of a few runs rather than the mean. The slow runs are measuring the machine.

Two rules that save the most wasted effort:

**Profile the real workload.** A small sample has other traits. Other memory pressure, other cache action, at times a other code path.

**Fix the top item and measure again.** The bottleneck moves. The second item on the first list is often no longer second.

And keep the ceiling in view: an step taking 5% of the runtime can't give back more than 5%. Cleverly it's rewritten.

## When to leave pandas

pandas assumes the data fits in memory on one machine. It's optimised for convenience rather than raw speed.

**Polars** is much faster on large joins and aggregations, with a similar model and a lazy engine.

**DuckDB** runs SQL over frames and files. Is great for analytical queries larger than memory.

**Dask** splits frames across cores or machines with a pandas-like API.

**NumPy** right, when the data is homogeneous and you don't need labels.

The signal that it's time is often memory rather than speed. When a frame no longer fits, no amount of tuning inside pandas fixes it.

## Profiling a pandas script

`%timeit` in a notebook and `time.perf_counter` around a block cover most choices.

For a whole script, `cProfile` finds the hot function and `line_profiler` finds the line inside it. Array code often has one line taking most of the time. This Line-level profiling shows at once and function-level profiling hides.

`df.info(memory_usage="deep")` and `memory_profiler` cover the memory side.

Two rules save the most wasted effort. Profile the **real** workload. A small sample has other cache action and at times takes a other code path. And re-profile after each fix, because the bottleneck moves.

## Reducing before combining

The largest structural wins often come from doing less work rather than doing the same work faster.

**Read fewer columns** &mdash; `usecols` at read time.

**Read fewer rows** &mdash; filter during the chunk loop rather than after.

**Aggregate before joining** &mdash; joining two summaries is far cheaper than joining raw tables and summarising later.

**Select columns before merging** &mdash; carrying twenty unused columns through a join costs memory and time.

Each of these changes the size of what all downstream touches. This Compounds through a pipeline in a way that micro-tuning doesn't.

## Categoricals as an optimisation

Converting a repeated string column to `group` helps in four places at once:

Memory, often by an order of magnitude.

Group-by, which then operates on int codes.

Merge, when both sides share the same groups.

`.str` steps, which apply to the groups rather than to each row.

That last one is worth restating: `df["city"].str.upper()` on a million rows with four distinct cities does four steps when the column is cat. A million when it's `object`.

The cost is the conversion itself and the care needed when mixing frames with other group sets.

## Avoiding repeated work

Two patterns that quietly dominate slow scripts:

**Recomputing inside a loop.** A group statistic, a lookup table, a parsed date. Found once outside the loop rather than once per loop.

**Repeated boolean masks.** Building the same mask a few times to select other columns. Build it once, name it, reuse it.

Both are plain programming discipline rather than anything pandas-exact. Both are easy to miss because each single line looks cheap.

## The limits

pandas is single-threaded for most steps, holds all in memory, and is optimised for convenience.

A rough guide to when to look elsewhere:

**Under a million rows** &mdash; pandas is comfortable. Tuning is rarely needed beyond dropping loops.

**One to ten million** &mdash; dtypes and access patterns start to matter. The techniques in this module earn their keep.

**Over ten million, or wider than memory**. The constraint is often memory rather than speed. Polars, DuckDB or Dask are the answer rather than a cleverer pandas formula.

**truly sequential methods** &mdash; Numba or a rewrite, at any size.

Recognising which regime you're in blocks both premature tuning and the opposite mistake of spending days making pandas do a thing it structurally can't.

## A short checklist

Is there a loop over rows? Drop it.

Is anything growing in a loop? Collect and combine once.

Are the dtypes right? groups for repeated text, narrow numerics where bounded.

Is the filter as early as it can be?

Have you measured, or are you guessing?

The first two account for most real slowdowns. Neither needs knowing anything about pandas internals.

## A worked speed-up

A slow script often has one dominant problem. The sequence for finding it's always the same.

Time the whole thing. Time each stage. Find the stage taking most of it. Look at what that stage does per row.

The fixes, in the order they often apply:

A row-wise `apply` turns column math or `np.select`.

A loop building a frame turns a list and one `concat`.

A merge inside a loop turns one merge outside it.

A repeated group statistic turns one `transform`.

An `object` column that should be a group turns one.

A filter at the end moves to the beginning.

Each of those is a small edit with a large effect. Together they account for most of the gap between a script that takes minutes and one that takes seconds.

## Memory, when the frame will not fit

The techniques differ from the speed ones, because the constraint is other.

`usecols` at read time &mdash; never load what you won't use.

`dtype` at read time &mdash; groups and narrow numerics.

`chunksize` &mdash; process and reduce a piece at a time.

`del` and `gc.collect()` &mdash; release intermediates by name in a long-running process.

Avoid keeping both a frame and a transformed copy alive. Reassign rather than naming a new var, when the old one isn't needed.

And check whether the step needs the whole frame at all. Many aggregations can be found chunk-wise and mixed.

## What not to optimise

Some things are already fast and are often rewritten for no gain:

**Column math** &mdash; already compiled.

**Boolean masking** &mdash; already compiled. The cost is the copy, not the compare.

**`groupby` with a string aggregation** &mdash; already compiled.

**Reading a small file** &mdash; measured in milliseconds.

**Anything running once on a small frame.**

Rewriting these makes less readable code and no measurable gain. This Is a bad trade. The reading step exists to prevent just that.

## A summary

Drop per-row Python first. It's often the whole problem.

Never grow a frame in a loop.

Right-size dtypes &mdash; groups and narrow numerics.

Filter early, so all downstream does less.

`itertuples` if you must iterate. Never `iterrows`.

`inplace=True` isn't an tuning.

Measure the real workload, fix the top item, measure again.

And know when the answer is a other tool. When the data doesn't fit, no pandas technique fixes it.

## A closing note

Pandas speed is unusually predictable. This Makes it unusually easy to get right.

Almost each slow script has the same cause: Python running once per row, spelled as `apply(axis=1)`, `iterrows`, or a loop. Dropping it's worth one or two orders of magnitude. Nothing else on the list comes close.

After that the wins are structural rather than clever. Don't grow frames in loops, filter before finding rather than after. Give columns types that fit the data. None of these need knowing anything about pandas internals.

What does need discipline is measuring. The bottleneck is regularly not where it feels like it's. The steps people most often rewrite. Column math, boolean masks, group-by with a string aggregation. Are already compiled and already fast.

And there's a ceiling. When the data no longer fits in memory, no pandas technique fixes it. The answer is Polars, DuckDB, Dask or a DB.
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
intro: Writing a pipeline as one formula.

## What it buys

Most pandas methods return a new object. This Means they compose:

```python
out = (df
       .query("year == 2024")
       .assign(doubled=lambda d: d["sales"] * 2)
       .groupby("city", as_index=False)["doubled"].sum())
```

Three things follow, and they're the actual arg for the style.

**No mid names.** The `tmp`, `tmp2`, `df_clean`, `df_clean2` sequence is where stale-var bugs live. Above all in a notebook where cells run out of order. `df` is no longer what the cell above assumed.

**Nothing is mutated.** The first frame is untouched. Re-running a cell gives the same answer. That alone drops a large class of notebook confusion.

**Each line is one step.** The chain reads top to bottom in the order the work happens. This Nested function calls don't.

The wrapping parentheses are what allow the line breaks. Without them the formula has to fit on one line or carry backslashes.

## assign and the lambda

`assign` is what makes math chainable, and the lambda is what makes `assign` work mid-chain.

`d.assign(b=d["a"] * 10)` finds against the frame **as it was before the chain started**. Inside a chain that is often wrong. If the column it needs was created two steps earlier it raises `KeyError`.

`d.assign(b=lambda d: d["a"] * 10)` receives the frame **at that point**. It sees all earlier steps made.

Use the lambda form by default in a chain. It costs eight characters and drops the class of error fully.

## pipe

Not each step is a pandas method. `pipe` inserts your own function without breaking the chain:

```python
df.pipe(drop_small, threshold=10).pipe(add_share)
```

`df.pipe(f, x)` is just `f(df, x)`. The gain is order. The nested form, `add_share(drop_small(df, 10))`, reads inside out and gets worse with each step.

For this to work, your functions should take a frame as the first arg and return a frame. That is a good shape for them anyway. It makes them testable in alone.

## Debugging

The standard objection to chaining is that you can't see what is happening in the middle. Can't set a breakpoint on a step.

The answer is a pipe that inspects and returns unchanged:

```python
def show(d, label):
    print(label, d.shape, list(d.columns))
    return d
```

Dropped into the chain, it prints the shape at each stage without changing the result. Most chain bugs are a shape or a column name, and that catches both.

For a heavier version, log `d.head()` or write the mid to a file. The principle is the same. A function that returns its input can go anywhere in a chain.

## Where to stop

Chaining is a style, not a virtue, and it stops paying at some length.

**The traceback problem.** When a fifteen-step chain raises `KeyError: 'typo'`, the traceback points at the whole formula. You know it failed. You don't at once know where. The last-but-one editor shows this.

**The reading problem.** A chain is one formula. It has to be understood as a whole. Past a certain length that is harder than reading five named steps.

**The reuse problem.** An mid result needed twice has to be found twice, or the chain has to be broken anyway.

A workable rule: chain a coherent stage. Loading and cleaning, or aggregating and formatting. And give each stage a name.

```python
clean = (raw.pipe(normalise_columns).dropna(subset=["id"]))
summary = (clean.groupby("city").agg(...).sort_values("total"))
```

Two names instead of ten, and each chain is short enough to debug.

## Where it fits

The style suits **load, clean, aggregate** work above all well. That work is on its own a sequence of changes with no branching.

It suits exploratory notebook work, because immutability makes re-running cells safe.

It suits less well anything with branching logic, loops, or steps whose output feeds two other places. At which point named intermediates are simply clearer. There's nothing wrong with using them.

## Which methods chain

Anything returning a DataFrame or Series can be chained. This Is most of the API:

Pick &mdash; `query`, `loc` with a callable, `filter`, `head`, `sample`, `nlargest`.

change &mdash; `assign`, `rename`, `drop`, `astype`, `fillna`, `replace`, `round`.

Reshaping &mdash; `sort_values`, `set_index`, `reset_index`, `melt`, `pivot`, `stack`, `unstack`, `explode`.

Aggregation &mdash; `groupby(...).agg(...)`, `value_counts`, `show`.

Anything else &mdash; `pipe`.

The methods that break a chain are the ones returning `None`. Anything with `inplace=True`. `sort` / `shuffle`-style in-place methods. That is one more reason to avoid `inplace`.

## Naming the stages

The hands-on shape for a real script is a few named stages rather than one long chain:

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

Each stage is short enough to debug, each name says what the data is at that point. The intermediates are on hand for inspection without breaking anything apart.

That structure also tests well: `normalise_columns` and each stage can be checked on its own.

## Chaining and memory

Each step in a chain allocates. A ten-step chain on a large frame allocates ten frames, though earlier ones are freed as it proceeds. Peak memory is roughly two at a time rather than ten.

That is acceptable for most work and worth knowing when the frame is large enough that a single copy is large.

Filtering early in the chain reduces each allocation after it. This Is the same advice as all over else and matters more here because there are more of them.

## Common chaining mistakes

**Losing the lambda in `assign`.** The formula is then checked against the pre-chain frame. Raises if it needs a column made mid-chain.

**Using `inplace=True` in a chain.** Returns `None`, and the next method raises `AttributeError` on `NoneType`.

**given the index lives.** `reset_index(drop=True)` at the point it matters, not at the end.

**A chain that is really two steps.** If an mid is needed twice, the chain has to find it twice or be broken. Break it.

**Debugging by deleting lines.** Better to insert a `pipe` that prints. This Doesn't change the structure.

## When not to chain

Chaining suits linear change. It doesn't suit:

**Branching** &mdash; other handling based on a rule.

**Loops** &mdash; over files, groups or params.

**Reuse** &mdash; an mid needed by two downstream steps.

**Error handling** &mdash; a try/except around one step.

In all four cases, named intermediates are clearer. Reaching for a chain anyway makes code that is harder to read than the thing it replaced.

The style is a tool for the common case of "load, clean, aggregate, output". Here It truly reads better than the option. It isn't a standard to hold all code to.

## A realistic shape for a script

Chaining works best as a few named stages rather than one long formula or a hundred split statements:

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

Each function is testable on its own, each chain is short enough to debug. The top-level line reads as what the script does.

`load(path).pipe(clean).pipe(summarise)` expresses the same thing in chain form. This Reads in order rather than inside out.

## Chaining and notebooks

The style suits notebooks above all well, for a reason worth stating: cells get re-run, out of order, again and again.

A chain doesn't mutate its input. Re-running a cell gives the same result. A sequence of in-place changes doesn't. Running it twice applies the change twice. The frame is now wrong in a way nothing shows.

That failure is common enough that "restart and run all" is standard advice. Chaining drops most of the need for it.

## Readability in practice

A few rules make chains easier to read:

One step per line.

Wrapping parentheses, so no backslashes are needed.

A blank line between logical stages within a long chain.

`pipe` for anything that isn't a pandas method, rather than breaking out.

Names for intermediates at genuine stage boundaries.

And a limit: if you can't see the whole chain on one screen, split it. The point of the style is clarity. A chain that has to be scrolled has stopped giving it.

## A summary

Chaining drops mid names and the stale-var bugs that come with them.

Nothing is mutated, so re-running is safe.

`assign` needs a lambda to see the frame mid-chain.

`pipe` inserts your own functions in reading order.

A `pipe` that prints and returns its input lets you debug without breaking the chain.

Long chains hide which link failed &mdash; name coherent stages instead.

And it's a style for linear change, not a rule for all code. Branching, loops and reuse are clearer with names.

## A closing note

Method chaining is one of the few stylistic choices in pandas that changes how many bugs you write rather than merely how the code looks.

The method isn't elegance. It's that mid names are where stale state lives: `df_clean` that was cleaned by an earlier version of the cell above, `tmp2` that is a filtered copy of `tmp` from before the filter changed. A chain has nowhere for that to hide.

The immutability matters for the same reason. Code that doesn't modify its input makes the same answer on the second run as the first. This Is the property notebooks most often lack.

Against that, a chain is one formula. One formula fails as a unit. The balance is struck by keeping chains to a coherent stage and giving each stage a name. Which is plain good structure, applied to data change.

## Two more things worth knowing

`pipe` has a second form for functions whose frame arg isn't first: `df.pipe((func, "data"), other_arg)` tells pandas which param receives the frame. It's rarely needed. It exists so that third-party functions with awkward signatures can still be chained.

`assign` accepts plain values and lambdas. Mixing the two in one call is legal. The rule is that a plain value is checked once, against the frame as it was before the chain started. A plain value referring to a column made mid-chain will fail. Using lambdas uniformly avoids having to hold that gap in mind.

Finally, chains and comments coexist badly. There's no natural place to explain a step. That is a real arg for named stages. A function name is a comment that can't drift out of date.

## Chaining and testing

One hands-on gain of the named-stage structure is that it makes a pipeline testable without any test framework ceremony.

Each stage takes a frame and returns a frame. Each can be checked on a small hand-built input:

```python
def test_clean():
    raw = pd.DataFrame({"ID": [1, 1, None], "City": [" Pune ", "pune", "goa"]})
    out = clean(raw)
    assert len(out) == 1
    assert list(out["city"]) == ["pune"]
```

That is a genuine unit test of a data change. It's possible only because `clean` is a function rather than a sequence of statements operating on a global `df`.

The same structure makes the pipeline reusable across scripts and notebooks. Makes it obvious where a new step belongs. Chaining, in this reading, is less about elegance than about pushing data changes into functions that can be named, tested and reused. Which is plain software practice arriving one spot it's often skipped.

## In summary

Chaining is a style that suits linear change. This Is most of what data cleaning is.

It drops mid names and the stale-state bugs that live in them, it doesn't mutate its input so re-running is safe. It reads in the order the work happens.

Its costs are real: a failure points at the whole formula, an mid needed twice forces a break. Branching or looping doesn't fit at all.

The detail is named stages of a handful of steps each. This Keeps the gains and makes each stage short enough to debug and small enough to test.
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
