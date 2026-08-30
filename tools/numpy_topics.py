# -*- coding: utf-8 -*-
"""Content for the NumPy track.

Twenty modules, each a sequence of short runnable steps rather than one long
program. NumPy is a set of rules that interact - dtype, shape, broadcasting,
whether you are holding a view or a copy - and a single script hides which
rule produced which line of output.

Several steps are written so the output contradicts the guess a reader would
make: that a slice is a copy, that + on two arrays of different shape is an
error, that axis=0 means "along the rows". Being wrong on the page and seeing
it immediately is the point.

numpy ships with Pyodide, so these run from the same CDN as the interpreter -
no wheels, unlike the FastAPI track.
"""

TOPICS = []
CHECKS = {}


def topic(slug, title, cat, lead, svg, steps, notes, article, check):
    """One module. `steps` is a list of (heading, blurb, code) triples."""
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "steps": steps, "notes": notes, "article": article, "check": check,
        "wheels": [], "prelude": "",
    })
    CHECKS["numpy/%s.html" % slug] = {"check": check}


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
# 1. What NumPy is for
# ---------------------------------------------------------------------------
topic(
    "what_is_numpy",
    "What NumPy Is For",
    "The Array",
    "One type, laid out end to end - and why almost everything else about the "
    "library follows from that.",
    _svg(_txt(40, 22, "list", M, 9) +
         _box(12, 30, 14, 14, S) + _box(34, 30, 14, 14, S) + _box(56, 30, 14, 14, S) +
         _txt(19, 56, "*", M, 8) + _txt(41, 56, "*", M, 8) + _txt(63, 56, "*", M, 8) +
         _txt(120, 22, "array", A, 9) +
         _box(92, 30, 16, 14, S, A) + _box(108, 30, 16, 14, S, A) + _box(124, 30, 16, 14, S, A) +
         _txt(120, 60, "contiguous", A, 8)),
    [
        ("A list of numbers is not a block of numbers",
         "A Python list holds pointers to objects scattered through memory. An array "
         "holds the numbers themselves, one type, end to end.",
         '''import numpy as np
import sys

nums = [1, 2, 3, 4, 5]
arr = np.array([1, 2, 3, 4, 5])

print("list :", nums, type(nums).__name__)
print("array:", arr, type(arr).__name__)
print()
print("every list element is a full Python object:")
print("   one int  :", sys.getsizeof(1), "bytes")
print("   the list :", sys.getsizeof(nums), "bytes of pointers alone")
print()
print("the array stores the numbers themselves:")
print("   dtype    :", arr.dtype)
print("   itemsize :", arr.itemsize, "bytes each")
print("   nbytes   :", arr.nbytes, "bytes total")'''),

        ("Arithmetic happens to the whole array",
         "No loop, no comprehension. The operation is described once and applied to "
         "every element by compiled code.",
         '''import numpy as np

nums = [1, 2, 3, 4, 5]
arr = np.array([1, 2, 3, 4, 5])

# Python: you write the loop
doubled_list = [n * 2 for n in nums]

# NumPy: you write the operation
doubled_arr = arr * 2

print("list  :", doubled_list)
print("array :", doubled_arr)
print()
print("and + means something different for each:")
print("   list  + list  :", nums + nums, "<- concatenation")
print("   array + array :", arr + arr, "<- elementwise addition")'''),

        ("One dtype, decided up front",
         "An array has a single type for every element. Mixing types does not make a "
         "mixed array &mdash; it promotes the whole thing.",
         '''import numpy as np

# NOTE: the default integer is platform-dependent. Most desktops give
# int64; this page runs 32-bit WebAssembly, so it reports int32.
print("ints        :", np.array([1, 2, 3]).dtype, "(platform default)")
print("floats      :", np.array([1.0, 2.0]).dtype)
print("one float   :", np.array([1, 2, 3.0]).dtype, "<- promoted the whole array")
print("with a str  :", np.array([1, 2, "three"]).dtype, "<- everything became text")
print("booleans    :", np.array([True, False]).dtype)
print()
a = np.array([1, 2, 3])
print("assigning a float into an int array:")
a[0] = 9.7
print("   ", a, "<- truncated, because the dtype cannot change")'''),

        ("How much faster, measured here",
         "The gap is real but this page runs on WebAssembly, so read the ratio and "
         "not the seconds.",
         '''import numpy as np
import time

n = 200_000
nums = list(range(n))
# int64 explicitly: this page is 32-bit WebAssembly, where NumPy's default
# integer is int32, and squaring values this large would silently overflow.
arr = np.arange(n, dtype=np.int64)

t = time.perf_counter()
total_list = sum(x * x for x in nums)
py = time.perf_counter() - t

t = time.perf_counter()
total_arr = int((arr * arr).sum())
npy = time.perf_counter() - t

print("python loop :  %.4f s" % py)
print("numpy       :  %.4f s" % npy)
print("ratio       :  %.1fx" % (py / npy))
print("same answer :", total_list == total_arr)'''),

        ("Shape is the other half",
         "An array is not just a list of numbers &mdash; it has a shape, and most of "
         "NumPy is about what shapes do together.",
         '''import numpy as np

a = np.array([1, 2, 3, 4, 5, 6])
b = a.reshape(2, 3)

print("flat   :", a, "shape", a.shape, "ndim", a.ndim)
print()
print("as 2x3 :")
print(b)
print("   shape:", b.shape, "ndim", b.ndim, "size", b.size)
print()
print("same numbers, same memory - only the shape changed:")
print("   shares memory:", np.shares_memory(a, b))'''),

        ("Where it sits in the stack",
         "pandas, scikit-learn, SciPy and every deep learning framework hold NumPy "
         "arrays or something modelled on them.",
         '''import numpy as np

# A tiny linear model, written the way every library underneath does it.
X = np.array([[1.0, 2.0],
              [1.0, 3.0],
              [1.0, 4.0]])          # a bias column and one feature
w = np.array([0.5, 2.0])            # parameters

y_pred = X @ w                      # one matrix multiply, not a loop
y_true = np.array([4.0, 6.5, 8.0])

print("predictions :", y_pred)
print("residuals   :", y_true - y_pred)
print("mean sq err :", float(((y_true - y_pred) ** 2).mean()))
print()
print("This is the shape of every fit, forward pass and score you will meet.")'''),
    ],
    [
        "A list holds pointers to objects; an array holds the numbers themselves, of one dtype, contiguous in memory.",
        "Operations apply to the whole array in compiled code. You describe the operation once rather than writing the loop.",
        "<code>+</code> concatenates lists and adds arrays elementwise. That difference catches people converting code.",
        "An array has one dtype. Mixing types promotes the whole array &mdash; add a string and every element becomes text.",
        "The default integer dtype is platform-dependent: <code>int64</code> on most desktops, <code>int32</code> on this page's 32-bit WebAssembly. Ask for a width explicitly whenever the values are large.",
        "Shape is as important as contents. Most of NumPy is rules about what shapes do when combined.",
        "These pages run CPython on WebAssembly, so timings are several times slower than native. Ratios transfer; seconds do not.",
    ],
    '''
title: What NumPy Is For
intro: One type, laid out end to end, and why almost everything else follows from that.

## Two ways to hold five numbers

A Python list of five integers is five pointers, each to a full `PyObject` sitting somewhere else in memory. Each of those objects carries a type, a reference count and the value. Adding two lists elementwise means following every pointer, checking every type, and building a new object for every result.

A NumPy array of five integers is forty bytes: five 64-bit numbers, one after another, with the type recorded once for the whole array.

That single difference explains nearly everything else in this track. It is why arrays are fast, why they have a dtype, why they cannot hold mixed types, why slicing gives you a view instead of a copy, and why shapes matter so much.

## Vectorisation

Because the numbers are contiguous and all the same type, the loop can happen in compiled code:

```python
doubled = arr * 2
```

There is no Python-level iteration. NumPy hands the whole block to a C routine that walks it, and modern CPUs process several elements per instruction while it does.

The mental shift is from *how do I loop over this* to *what operation am I applying*. That reads oddly at first and becomes the natural way to think within about a week.

## `+` means two different things

Worth stating early because it is the first thing that surprises people converting code:

```python
[1, 2] + [1, 2]                  # [1, 2, 1, 2]   - concatenation
np.array([1, 2]) + np.array([1, 2])   # array([2, 4]) - addition
```

Lists concatenate. Arrays add. Neither is wrong; they are different types with different meanings for the same symbol, and code that assumes one while holding the other produces something plausible rather than an error.

## One dtype, and it is decided for you

Every element of an array has the same type, and NumPy picks the narrowest type that fits everything you gave it.

`[1, 2, 3]` becomes the platform's default integer. On most desktop machines that is `int64`; on this page, which runs 32-bit WebAssembly, it is `int32`. That difference is not cosmetic &mdash; an `int32` overflows at about 2.1 billion, silently and without a warning &mdash; and it is the reason examples here that multiply large integers ask for `dtype=np.int64` explicitly. Add one float and the whole array becomes `float64` &mdash; not a mixture. Add a string and every element becomes a fixed-width string, including the numbers.

That last case is worth watching for, because it produces an array that still looks reasonable when printed and does nothing you want arithmetically.

There is a consequence people meet early: assigning into an array cannot change its dtype. Put `9.7` into an `int64` array and it truncates to `9`, silently. The array's type was fixed when it was created.

## Speed, honestly

The fourth editor above measures it. Expect a large ratio, and read the ratio rather than the seconds.

These pages run CPython compiled to WebAssembly, which is several times slower than a native interpreter for the Python parts. That penalty falls mostly on the Python loop, so if anything the gap here flatters NumPy. The direction is right and the magnitude is roughly right; the absolute numbers do not transfer to your laptop.

The speed also has limits worth knowing now. Arrays are fast for whole-array operations on numeric data. They are not fast if you loop over them in Python one element at a time &mdash; that is slower than a list, because each element has to be boxed into a Python object on the way out.

## Shape

An array carries a shape as well as contents, and most of the interesting behaviour in this library is about what shapes do when combined.

`a.shape` is a tuple. `(6,)` is one-dimensional with six elements. `(2, 3)` is two rows of three. `(2, 3, 4)` is two blocks of three rows of four.

Reshaping is usually free, because it changes how the same block of memory is interpreted rather than moving anything. The last editor shows `np.shares_memory` confirming that the reshaped array is the same numbers.

## Where this sits

Almost nothing in scientific Python reimplements arrays. pandas holds NumPy arrays under its columns. scikit-learn takes and returns them. SciPy builds on them. PyTorch and TensorFlow use their own tensor types deliberately modelled on the same interface, so that `@`, broadcasting and `.shape` mean what you already expect.

Learning NumPy properly is therefore not one library. It is the vocabulary that the rest of the stack assumes you have.

## What this track covers

The array itself first: creating one, its dtype, its shape, and what indexing gives you. Then operating on arrays: elementwise arithmetic, broadcasting, boolean masks, aggregation along an axis. Then structure: views versus copies, stacking, transposing, sorting. Then the numerical end: random numbers, linear algebra, missing data, and the performance rules that follow from the memory layout.

Every idea is a small program on the page. Change the numbers and press Run; a shape rule you have watched break is one you will remember.

## Why the list is slow, concretely

It is worth being precise about where the time goes, because "Python is slow" is not an explanation and does not tell you what to change.

A Python list of five integers is an array of five **pointers**. Each pointer leads somewhere else in memory, to a `PyObject` that carries a reference count, a type pointer, and only then the actual value. A small integer occupies twenty-eight bytes and sits wherever the allocator put it.

Adding two lists elementwise therefore means: follow a pointer, check the type, extract the value, follow another pointer, check that type, extract that value, perform the addition, allocate a new object for the result, and store a pointer to it. Ten times over for ten elements.

The NumPy array is five integers, adjacent, with nothing between them. The addition is a loop in compiled C over contiguous memory, with the type checked once for the whole array rather than once per element.

Two separate wins come out of that. The obvious one is skipping the interpreter. The less obvious one is **locality**: the processor fetches memory in blocks, so reading consecutive values costs a fraction of what chasing scattered pointers costs. On large arrays the second effect can matter as much as the first.

This also explains the cases where NumPy does not help. If your data is a thousand elements and you touch it once, the interpreter overhead you avoided was small and the conversion cost was not. The wins scale with array size.

## What NumPy deliberately does not do

Knowing the boundaries saves a lot of fighting with it.

**It does not grow.** There is no efficient append. The size is fixed at creation, and every function that appears to extend an array is allocating a new one and copying. This is not an oversight; it is the price of the contiguous block that makes everything else fast.

**It does not mix types.** One dtype per array. A column of names and a column of ages are two arrays, or a structured dtype, or a pandas DataFrame &mdash; not one NumPy array of mixed values.

**It handles strings poorly.** NumPy strings are fixed width, and assigning a longer value silently truncates it. Object arrays hold real Python strings but give up every performance benefit, since they are back to storing pointers.

**It has no concept of missing data.** Floats can carry NaN, and integers cannot carry anything. There is no null.

## When to use something else

**Small data touched once.** A hundred values processed in a script: a list is simpler and the difference is unmeasurable.

**Heterogeneous records with labels.** That is pandas. It is built on NumPy, so you lose nothing, and you gain named columns, mixed types per column and real handling of missing values.

**Nested or ragged structure.** Lists of different lengths do not form an array. Forcing them into an object array gets you the syntax without the speed.

**Data larger than memory.** NumPy assumes the array fits. Dask, Zarr and HDF5 exist for when it does not.

## The model to carry forward

Everything else in this track is a consequence of one idea: an array is a **flat block of identical values, plus a small description of how to read it** &mdash; the shape, the dtype, and the number of bytes to step for each axis.

Reshaping changes the description and not the block. Transposing changes the description. Slicing changes the description. All of them are free.

Masking and fancy indexing cannot be described that way, so they copy.

Arithmetic runs over the block in compiled code. Broadcasting is a rule for pretending two descriptions are compatible without changing either block.

Hold onto that and most of NumPy's behaviour stops being a set of rules to memorise and becomes something you can predict.

## Questions people ask at this point

**Does NumPy replace Python lists?**

No. Lists are the right structure for heterogeneous, growing collections of arbitrary objects, and they remain the right answer for most ordinary Python. NumPy is for a specific shape of problem: many values of the same type, operated on together. Reaching for an array to hold three configuration values is worse than a list, not better.

**Do I need to install it?**

NumPy is not in the standard library. It is `pip install numpy`, and it is a dependency of nearly everything numerical, so it is usually already present in a scientific environment. It ships as a compiled wheel for every common platform, so installation does not require a compiler.

**Why is it always imported as `np`?**

Convention, and a strong one. Nearly all published code, documentation and examples use `import numpy as np`, so following it makes your code readable to anyone who has seen NumPy before. There is no technical reason, and no good reason to deviate.

**Is NumPy still relevant with pandas and PyTorch around?**

It is underneath both. A pandas Series wraps a NumPy array; PyTorch tensors follow the same shape and broadcasting rules and convert to arrays in one call. Everything in this track transfers, which is a large part of why it is worth learning properly rather than by copying snippets.

**How much of it do I need?**

Less than the documentation suggests. NumPy has hundreds of functions and a working knowledge of maybe thirty covers most real code. The concepts &mdash; shape, dtype, views, broadcasting &mdash; matter far more than the function list, because they let you predict behaviour instead of looking it up.

## How to work through this track

Each module has runnable editors above the text. They are not decoration: the fastest way to build an accurate mental model of shapes and dtypes is to change a number, run it, and see what happens.

The parts worth slowing down on are the ones where NumPy's behaviour differs from Python's: integer overflow, views sharing memory, broadcasting shapes you did not intend, and NaN. Those four account for most of the surprises in real code, and each has a module.

The parts you can skim on a first pass are the function inventories &mdash; the specific names in stacking, sorting and set operations. Knowing that a function exists is enough; the signature is a search away.
''',
    [
        {"q": "What is the fundamental difference between a list and an array?",
         "options": ["Arrays are shorter", "A list holds pointers to objects; an array holds the numbers themselves, one dtype, contiguous", "Arrays are immutable", "Lists are typed"],
         "answer": 1,
         "why": "Everything else - speed, dtype, views, broadcasting - follows from that memory layout."},
        {"q": "What does `np.array([1, 2, \"three\"])` produce?",
         "options": ["A mixed array", "An error", "An array where every element is a string", "An object array of ints and strings"],
         "answer": 2,
         "why": "An array has one dtype, so everything is promoted to the type that fits all of it - here, text. It prints plausibly and does nothing useful arithmetically."},
        {"q": "You assign `a[0] = 9.7` into an int64 array. What happens?",
         "options": ["The array becomes float64", "It stores 9 - truncated", "It raises", "It stores 10"],
         "answer": 1,
         "why": "The dtype was fixed when the array was created and assignment cannot change it, so the value is truncated silently."},
        {"q": "Why are the timings on these pages not directly transferable?",
         "options": ["The code is different", "They run CPython on WebAssembly, several times slower than native", "NumPy is disabled", "The arrays are too small"],
         "answer": 1,
         "why": "The penalty falls mostly on the Python loop, so the ratio is roughly right and if anything flatters NumPy. Read the ratio, not the seconds."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Creating arrays
# ---------------------------------------------------------------------------
topic(
    "creating_arrays",
    "Creating Arrays",
    "The Array",
    "The half-dozen constructors that cover almost everything, and which one to "
    "reach for when.",
    _svg(_txt(80, 20, "zeros  ones  arange  linspace", A, 8) +
         _grid(38, 32, 6, 3, 14)),
    [
        ("From a list, and from nested lists",
         "<code>np.array</code> takes what you give it. Nesting decides the "
         "dimensions, and ragged input is an error rather than a guess.",
         '''import numpy as np

a = np.array([1, 2, 3])
b = np.array([[1, 2, 3],
              [4, 5, 6]])

print("1-D:", a, "shape", a.shape)
print("2-D:")
print(b)
print("   shape", b.shape, "ndim", b.ndim)

try:
    np.array([[1, 2], [3, 4, 5]])          # rows of different length
except ValueError as e:
    print()
    print("ragged input:", type(e).__name__)
    print("  ", str(e).split(".")[0])'''),

        ("Filled arrays of a known shape",
         "Usually you know the shape before the values. These allocate it in one "
         "call, which is far better than growing a list and converting.",
         '''import numpy as np

print("zeros (2,3):"); print(np.zeros((2, 3)))
print()
print("ones (2,3) :"); print(np.ones((2, 3), dtype=int))
print()
print("full       :"); print(np.full((2, 3), 7.5))
print()
print("empty      : allocated but NOT initialised - contents are whatever")
print("             was in that memory. Use it only when you overwrite it all.")
print()
print("identity   :"); print(np.eye(3, dtype=int))'''),

        ("Ranges: arange and linspace",
         "<code>arange</code> takes a step and excludes the stop; "
         "<code>linspace</code> takes a count and includes it. That difference is "
         "the whole reason both exist.",
         '''import numpy as np

print("arange(5)          :", np.arange(5))
print("arange(2, 10, 3)   :", np.arange(2, 10, 3), "<- stop is EXCLUDED")
print()
print("linspace(0, 1, 5)  :", np.linspace(0, 1, 5), "<- stop INCLUDED, 5 values")
print("linspace(0, 1, 4)  :", np.linspace(0, 1, 4))
print()
print("arange with floats is where people get bitten:")
print("   arange(0, 1, 0.1) length:", len(np.arange(0, 1, 0.1)))
print("   arange(0, 0.3, 0.1)     :", np.arange(0, 0.3, 0.1))
print("   floating point makes the count unpredictable - use linspace.")'''),

        ("Like an existing array",
         "The <code>_like</code> family copies shape and dtype, which is how you "
         "allocate a result that matches an input.",
         '''import numpy as np

template = np.array([[1, 2, 3],
                     [4, 5, 6]], dtype=np.float32)

print("template   :", template.shape, template.dtype)
print("zeros_like :", np.zeros_like(template).shape, np.zeros_like(template).dtype)
print("ones_like  :", np.ones_like(template).dtype)
print("full_like  :"); print(np.full_like(template, 9))
print()
print("Compare with zeros((2,3)), which would silently give you float64")
print("and quietly widen every result that touches it.")'''),

        ("Choosing the dtype up front",
         "The dtype is fixed at creation. Deciding it deliberately avoids both "
         "overflow and wasted memory.",
         '''import numpy as np

small = np.arange(5, dtype=np.int8)
big = np.arange(5, dtype=np.int64)
f32 = np.arange(5, dtype=np.float32)

for name, arr in [("int8", small), ("int64", big), ("float32", f32)]:
    print("%-8s %-9s %d bytes each, %d total"
          % (name, arr.dtype, arr.itemsize, arr.nbytes))

print()
print("int8 holds -128..127, so it wraps around:")
print("   ", np.array([127], dtype=np.int8) + np.array([1], dtype=np.int8))
print("   no error, no warning - just the wrong number.")'''),

        ("Building one you will fill",
         "The common shape of real code: allocate the result, then write into it. "
         "Growing an array in a loop copies it every time.",
         '''import numpy as np
import time

n = 20_000

# Wrong: every append reallocates and copies the whole thing.
t = time.perf_counter()
grown = np.array([], dtype=np.float64)
for i in range(2000):
    grown = np.append(grown, i)
slow = time.perf_counter() - t

# Right: allocate once, then assign.
t = time.perf_counter()
out = np.empty(2000, dtype=np.float64)
for i in range(2000):
    out[i] = i
fast = time.perf_counter() - t

print("np.append in a loop : %.4f s" % slow)
print("allocate then fill  : %.4f s" % fast)
print("ratio               : %.1fx" % (slow / fast))
print("same result         :", np.array_equal(grown, out))
print()
print("Better still: np.arange(2000.0) - no Python loop at all.")'''),
    ],
    [
        "<code>np.array</code> infers dimensions from nesting. Ragged rows raise rather than producing something surprising.",
        "<code>zeros</code>, <code>ones</code>, <code>full</code> and <code>eye</code> allocate a known shape in one call. <code>empty</code> does not initialise &mdash; only use it when you overwrite everything.",
        "<code>arange</code> takes a step and excludes the stop; <code>linspace</code> takes a count and includes it. Use <code>linspace</code> for floats.",
        "<code>zeros_like</code> and friends copy shape <em>and</em> dtype, which keeps a float32 pipeline from silently widening to float64.",
        "The dtype is fixed at creation. <code>int8</code> wraps at 127 with no warning, so choose a width that fits your values.",
        "Never grow an array in a loop &mdash; <code>np.append</code> copies the whole thing each time. Allocate the result and assign into it.",
    ],
    '''
title: Creating Arrays
intro: The half-dozen constructors that cover almost everything, and which to reach for when.

## From data you already have

`np.array` takes a list, a tuple, or nested lists, and infers the shape from the nesting. One level gives you 1-D, two levels gives 2-D, and so on.

Rows must be the same length. Ragged input raises rather than guessing, which is the right choice &mdash; the alternative would be an array of Python list objects that looks like an array and behaves like nothing you want.

If you genuinely have ragged data, you want a list of arrays, or padding to a rectangle, and you should decide which deliberately.

## When you know the shape but not the values

Most real code knows the shape first. Allocating it directly is both faster and clearer than building a list and converting.

`np.zeros(shape)` and `np.ones(shape)` are the common ones. `np.full(shape, value)` fills with anything. `np.eye(n)` is the identity matrix.

Note that the shape argument is a *tuple* for more than one dimension: `np.zeros((2, 3))`. `np.zeros(2, 3)` is a different function signature and will not do what you meant.

`np.empty` deserves a warning. It allocates without initialising, so the contents are whatever happened to be in that memory &mdash; not zeros, not anything predictable. It is marginally faster than `zeros` and only correct when you are about to overwrite every element. Reaching for it by default produces bugs that appear only sometimes.

## arange and linspace

Both make a sequence, and the difference is what you specify.

`np.arange(start, stop, step)` takes a **step** and excludes the stop, exactly like Python's `range`.

`np.linspace(start, stop, num)` takes a **count** and includes the stop.

For integers, `arange` is natural. For floats, it is a trap: the number of elements depends on floating-point accumulation, so `np.arange(0, 1, 0.1)` may give you ten elements or eleven depending on rounding, and `np.arange(0, 0.3, 0.1)` can include a value slightly above 0.3.

The rule is simple: **if the step is a float, use `linspace`.** You almost always know how many points you want, and `linspace` gives exactly that many, with the endpoint where you asked for it.

## Matching an existing array

The `_like` family &mdash; `zeros_like`, `ones_like`, `empty_like`, `full_like` &mdash; copies both shape and dtype from an array you already have.

The dtype part is the valuable half. In a pipeline working in `float32` for memory reasons, allocating a result with `np.zeros(shape)` gives `float64`, and the first operation that combines them widens everything back. `zeros_like` keeps the type you chose.

## Choosing a dtype

The dtype is fixed at creation and worth choosing rather than accepting.

Integers come in `int8`, `int16`, `int32` and `int64`, signed and unsigned. Floats come in `float32` and `float64` (and `float16`, with real precision costs).

Two reasons to care. **Memory**: a million `float64` values is 8 MB; `float32` halves that, which matters once arrays are large. **Overflow**: an `int8` holds &minus;128 to 127, and `127 + 1` gives &minus;128 with no error and no warning. NumPy does not promote to a wider type to save you.

That silence is the important part. Python integers grow without limit; NumPy integers wrap. Code ported from lists to arrays can start producing wrong numbers rather than raising, which is much harder to notice.

The default integer width is platform-dependent &mdash; `int64` on most desktops, `int32` on this page's 32-bit WebAssembly. Where the values may be large, say what you want.

## Never grow an array in a loop

`np.append` does not append. There is nowhere to append to: an array is a fixed block of memory, so `np.append` allocates a new one, copies everything across, and returns it. In a loop that is quadratic.

The last editor measures it. The fix is the same as the string-concatenation fix in Python: allocate the result once and assign into it, or better, build the whole thing with a vectorised call and no Python loop at all.

If you genuinely do not know the final size, collect into a Python list and convert once at the end &mdash; lists over-allocate and appending to them is cheap.

## Which to reach for

Data in hand: `np.array`.

Known shape, zeros: `np.zeros`. Known shape, matching an existing array: `zeros_like`.

Integer sequence: `np.arange`. Float sequence: `np.linspace`.

A result you are about to fill completely: `np.empty`, and only then.

Anything else in a loop: stop and ask whether a vectorised expression would build it in one call.

## empty is not zeros

`np.zeros` writes zeros. `np.empty` allocates and writes nothing, so the contents are whatever was previously in that memory.

That makes `empty` faster, and it is the correct choice when you are about to overwrite every element. It is a bug waiting to happen when you are not.

The trap is that uninitialised memory is often zeros in practice, especially on a freshly started process, so code that accidentally relies on `empty` giving zeros can pass every test and then produce garbage under real load when the allocator hands back recycled memory.

The rule: use `empty` only when the very next thing you do fills the whole array. If there is any branch where an element might not be written, use `zeros`.

## Bringing data in from elsewhere

`np.array` on a list is the common case, but it is not the only door.

`np.frombuffer` wraps existing bytes without copying &mdash; useful for data arriving from a socket, a file read, or another library. The result is read-only if the buffer is, and it shares memory with the source, so the usual view caveats apply.

`np.fromiter` builds an array from any iterable, consuming it lazily. This is the one to reach for with a generator, because `np.array(generator)` does **not** do what you would hope: it creates a zero-dimensional object array containing the generator itself. That failure is silent and confusing, and `fromiter` with an explicit `dtype` is the fix. Pass `count` when you know the length, and it can preallocate instead of growing internally.

`np.loadtxt` and `np.load` cover files, and get a module of their own later.

## The structured constructors

`np.eye(n)` gives an identity matrix; `np.identity(n)` is the same thing with fewer options. `np.eye` takes a `k` argument to offset the diagonal, which is how you build shift matrices.

`np.diag` is two functions in one, depending on what you hand it. Given a 1-D array it builds a matrix with that diagonal. Given a 2-D array it extracts the diagonal. That overloading is convenient and occasionally surprising.

`np.full(shape, value)` fills with a constant, and is clearer than `np.ones(shape) * value` &mdash; it also gets the dtype right, inferring it from the fill value rather than starting from float.

`np.tile` and `np.repeat` build larger arrays from smaller ones. They differ in a way worth remembering: `tile` repeats the whole array, `repeat` repeats each element in place. `np.tile([1,2], 2)` gives `1 2 1 2`; `np.repeat([1,2], 2)` gives `1 1 2 2`.

## array versus asarray

`np.array(x)` copies by default. `np.asarray(x)` does not copy if `x` is already an array of the right dtype.

That distinction matters at function boundaries. A function that begins `a = np.asarray(a)` accepts lists and arrays alike, and costs nothing when given an array it can use directly. The same function written with `np.array` copies every call, which is wasteful in a loop and can be significant for large inputs.

Use `asarray` for "make sure this is an array". Use `array` when you specifically want a copy that the caller cannot see you modify.

Note that `asarray` returning the original means you must not modify it in place unless you own it &mdash; the same views-and-copies question that runs through the whole library.

## A checklist for choosing

Ask, in order:

**Do I already have the values?** `np.array` or `np.asarray`.

**Do I know the shape but not the values?** `zeros`, `ones`, `full`, or `empty` if every element will be overwritten.

**Is it a sequence of numbers?** `arange` for a step, `linspace` for a count. Prefer `linspace` whenever the values are floats, because `arange` with a float step has an unpredictable length.

**Should it match something I have?** The `_like` family, which copies shape and dtype together and prevents the two from drifting apart.

**Is it coming from a generator or a byte buffer?** `fromiter` or `frombuffer`, never bare `np.array`.

And in every branch, set the dtype at creation rather than converting later. `astype` allocates a whole second array, and choosing correctly the first time avoids both the copy and the class of bugs where an integer array silently refuses the float you assign into it.

## Common mistakes at this stage

**`np.array(generator)`.** This does not build an array from the generator's values. It builds a zero-dimensional object array containing the generator object itself, and every subsequent operation behaves bizarrely. `np.fromiter(gen, dtype=float)` is the correct call, and passing `count` when the length is known lets it preallocate.

**`np.array` on ragged input.** Lists of unequal length no longer produce an object array silently &mdash; modern NumPy raises. That is an improvement, because the object array it used to create looked like an array and performed like a list.

**Forgetting that `np.zeros` is float.** `np.zeros(5)` has dtype `float64`, not integer. Code that fills it with counts and then uses it as an index has to convert, and the conversion is a copy. `np.zeros(5, dtype=int)` at creation avoids both.

**`np.empty` where `np.zeros` was meant.** Uninitialised memory frequently contains zeros in a fresh process, so this passes tests and fails in production.

**Building with `np.append` in a loop.** Quadratic, and the single most common accidental slowdown in beginner NumPy code.

## A note on reproducible construction

Test data and examples benefit from being deterministic.

`np.arange` and `np.linspace` are deterministic by construction, which makes them good for examples where the values do not matter but reproducibility does.

Where random data is genuinely needed, `np.random.default_rng(seed)` gives a generator whose output is fixed. Seeding at the point of construction, rather than relying on a global, keeps the example self-contained &mdash; which is why every random example in this track creates its own generator.

## Getting the shape right the first time

Most construction bugs are shape bugs, and two habits prevent them.

**Pass the shape as a tuple and read it back.** `np.zeros((3, 4))` is unambiguous. `np.zeros(3, 4)` is an error, because the second positional argument is the dtype &mdash; a genuinely confusing failure the first time it happens.

**Use the `_like` family when an array should match another.** `np.zeros_like(a)` cannot drift out of sync with `a` the way a hard-coded shape can. When the shape of `a` changes, the output follows, and one fewer place needs editing.

## A closing note

Creation is the cheapest place to prevent problems, because the dtype and shape chosen here propagate through everything that follows.

Setting the dtype at construction avoids a copy and a class of silent conversion bugs. Passing the shape as a tuple avoids the confusing failure where the second argument is read as a dtype. And using the `_like` family keeps derived arrays from drifting out of sync with their source.

Three small habits, applied once, that remove a disproportionate amount of later debugging.
''',
    [
        {"q": "Why prefer `linspace` over `arange` for float steps?",
         "options": ["It is faster", "arange's element count depends on floating-point accumulation and is unpredictable", "arange cannot take floats", "linspace is newer"],
         "answer": 1,
         "why": "`np.arange(0, 1, 0.1)` may give ten or eleven elements depending on rounding. `linspace` gives exactly the count you asked for, endpoint included."},
        {"q": "What does `np.empty((2,3))` contain?",
         "options": ["Zeros", "Whatever was already in that memory", "NaN", "Ones"],
         "answer": 1,
         "why": "It allocates without initialising. Only correct when you overwrite every element - otherwise it produces bugs that appear only sometimes."},
        {"q": "`np.array([127], dtype=np.int8) + 1` gives what?",
         "options": ["128", "-128, silently", "An OverflowError", "It promotes to int16"],
         "answer": 1,
         "why": "NumPy integers wrap rather than promoting or raising. Python ints grow without limit, so code ported from lists can start producing wrong numbers instead of errors."},
        {"q": "Why is `np.append` in a loop a mistake?",
         "options": ["It is deprecated", "An array is a fixed block, so each call allocates a new one and copies everything", "It only works on 1-D", "It changes the dtype"],
         "answer": 1,
         "why": "There is nowhere to append to. Allocate the result once and assign into it, or build it with a vectorised call."},
    ],
)


# ---------------------------------------------------------------------------
# 3. dtypes
# ---------------------------------------------------------------------------
topic(
    "dtypes",
    "Dtypes",
    "The Array",
    "One type for the whole array - what it costs, when it overflows, and the "
    "promotion rules that decide the result.",
    _svg(_box(14, 22, 132, 20, S, A) + _txt(80, 36, "int8  int32  int64  float32  float64", A, 8) +
         _txt(80, 60, "one dtype, every element", M, 8) +
         _txt(80, 78, "chosen at creation", M, 8)),
    [
        ("What a dtype records",
         "A kind, a width, and therefore a range. Every element of the array uses "
         "it.",
         '''import numpy as np

for dt in [np.int8, np.int16, np.int32, np.int64]:
    info = np.iinfo(dt)
    print("%-8s %d bytes   %20d .. %d" % (np.dtype(dt).name, np.dtype(dt).itemsize,
                                          info.min, info.max))
print()
for dt in [np.float32, np.float64]:
    info = np.finfo(dt)
    print("%-8s %d bytes   ~%.1e precision" % (np.dtype(dt).name,
                                               np.dtype(dt).itemsize, info.eps))'''),

        ("Integers wrap; they do not grow",
         "This is the sharpest difference from Python, and it fails silently.",
         '''import numpy as np

a = np.array([127], dtype=np.int8)
print("int8 127 + 1  :", a + np.array([1], dtype=np.int8), "<- wrapped to -128")

b = np.array([2**31 - 1], dtype=np.int32)
print("int32 max + 1 :", b + np.array([1], dtype=np.int32))

print()
print("Python, for comparison, just gets bigger:")
print("   ", 2**31 - 1 + 1)
print()
print("No exception is raised. Ported code starts returning wrong numbers")
print("rather than failing, which is much harder to notice.")'''),

        ("Promotion decides the result type",
         "Combining two dtypes gives the narrowest type that can hold both. That is "
         "usually helpful and occasionally expensive.",
         '''import numpy as np

pairs = [
    (np.array([1], dtype=np.int8),    np.array([1], dtype=np.int16)),
    (np.array([1], dtype=np.int32),   np.array([1.0], dtype=np.float32)),
    (np.array([1], dtype=np.int64),   np.array([1.0], dtype=np.float32)),
    (np.array([1.0], dtype=np.float32), np.array([1.0], dtype=np.float64)),
    (np.array([True]),                np.array([1], dtype=np.int8)),
]
for x, y in pairs:
    print("%-9s + %-9s -> %s" % (x.dtype, y.dtype, (x + y).dtype))

print()
print("Note int64 + float32 -> float64: neither input type, because")
print("float32 cannot represent every int64 exactly.")'''),

        ("Assignment cannot change the dtype",
         "Writing into an array converts the value to fit. It never widens the "
         "array.",
         '''import numpy as np

ints = np.arange(5)
print("before      :", ints, ints.dtype)

ints[0] = 9.99
print("after 9.99  :", ints, "<- truncated toward zero")

ints[1] = -0.5
print("after -0.5  :", ints)

print()
floats = np.zeros(3, dtype=np.float32)
floats[0] = 1/3
print("float32 1/3 :", repr(float(floats[0])), "<- lost precision on the way in")
print("float64 1/3 :", repr(1/3))'''),

        ("Converting on purpose",
         "<code>astype</code> makes a new array with a new dtype. It always copies, "
         "and it will happily lose information.",
         '''import numpy as np

f = np.array([1.9, -1.9, 2.5, 1e10])
print("floats        :", f)
print("astype(int32) :", f.astype(np.int32), "<- toward zero, and 1e10 overflows")
print()
print("rounding first is usually what you meant:")
print("   np.round then astype:", np.round(f[:3]).astype(np.int64))
print()
print("astype always copies:")
a = np.arange(3)
b = a.astype(np.int64)
b[0] = 99
print("   original untouched:", a)'''),

        ("Picking a width deliberately",
         "Memory and range are the two axes. For large arrays the choice is worth "
         "making rather than defaulting.",
         '''import numpy as np

n = 100_000
for dt in [np.int8, np.int32, np.int64, np.float32, np.float64]:
    a = np.zeros(n, dtype=dt)
    print("%-9s %6.2f MB" % (np.dtype(dt).name, a.nbytes / 1e6))

print()
print("float32 halves the memory of float64 and keeps ~7 significant digits.")
print("For image data and neural network weights that is usually plenty;")
print("for accumulating a long sum it is not.")
print()
big = np.full(1_000_000, 1.0, dtype=np.float32)
print("sum of 1e6 ones in float32:", float(big.sum()))
print("with a float64 accumulator:", float(big.sum(dtype=np.float64)))'''),
    ],
    [
        "A dtype is a kind and a width. It is fixed when the array is created and applies to every element.",
        "NumPy integers <strong>wrap</strong> on overflow rather than growing or raising. Python integers do the opposite, so ported code can start returning wrong numbers.",
        "Promotion picks the narrowest type holding both operands &mdash; <code>int64 + float32</code> gives <code>float64</code>, which is neither input.",
        "Assignment converts the value to the array's dtype. It never widens the array, so floats truncate into integer arrays.",
        "<code>astype</code> always copies and will lose information without complaint. Round before converting if that is what you meant.",
        "<code>float32</code> halves memory and keeps about seven significant digits &mdash; fine for weights and images, not for a long running sum.",
    ],
    '''
title: Dtypes
intro: One type for the whole array: what it costs, when it overflows, and how promotion decides the result.

## Kind and width

A dtype records what kind of number and how many bytes. `int32` is a signed integer in four bytes; `float64` is a double-precision float in eight.

Both halves matter. The kind decides what operations mean; the width decides the range and the memory.

`np.iinfo` and `np.finfo` report the limits, and it is worth looking at them once rather than remembering approximations. The first editor prints them.

## Integers wrap

This is the sharpest difference from ordinary Python and the one most likely to cause a quiet bug.

A Python `int` grows to whatever size it needs. A NumPy integer is a fixed-width machine integer, and exceeding it wraps around. `int8` at 127 plus one is &minus;128. No exception, no warning.

Code that worked on lists can produce wrong numbers on arrays, and the failure is silent. That is worse than a crash, because nothing draws attention to it.

Two habits help. Choose a width with headroom when values can grow. And be aware that the default integer is platform-dependent &mdash; `int64` on most desktops, `int32` on this page &mdash; so an example that is safe on your laptop may overflow elsewhere, and vice versa.

## Promotion

When two arrays of different dtype meet, NumPy finds a type that can hold both and converts before operating.

Mostly this is what you want. `int8 + int16` gives `int16`. `int32 + float32` gives `float64`, which surprises people the first time: `float32` cannot represent every `int32` exactly, so NumPy widens to something that can.

The consequence worth knowing is memory. A carefully chosen `float32` array combined with anything `float64` produces a `float64` result, and a pipeline can quietly double its footprint at one careless line. If you are working in `float32` deliberately, keep constants and intermediate arrays in `float32` too.

## Assignment converts, it does not widen

Writing into an array converts the value to the array's dtype:

```python
ints = np.arange(5)
ints[0] = 9.99        # stores 9
```

Truncation toward zero, silently. The array's type was decided at creation and a single assignment cannot change it.

The same applies to precision. Writing `1/3` into a `float32` array stores the nearest `float32`, and reading it back gives a value that differs from Python's float in the seventh decimal place.

## astype

`astype` produces a new array with a new dtype. Two things to remember.

It **always copies**, even when the dtype is unchanged, unless you pass `copy=False`. That is a real cost on large arrays.

It **converts without complaint**. Floats truncate toward zero rather than rounding, so `1.9` becomes `1` and `-1.9` becomes `-1`. Values outside the target range overflow. If you meant to round, call `np.round` first and then convert.

## Choosing a width

Two considerations, and they pull in opposite directions.

**Memory.** A million `float64` values is 8 MB. In `float32` it is 4 MB, in `float16` 2 MB. On large arrays this is the difference between fitting in cache and not, which affects speed as much as capacity.

**Precision and range.** `float32` carries about seven significant decimal digits, `float64` about sixteen. For image pixels, neural network weights and most measured data, `float32` is ample. For accumulating a sum over millions of elements it is not &mdash; the running total grows until adding one more small value changes nothing.

The last editor demonstrates that: summing a million ones in `float32` does not give a million. `sum(dtype=np.float64)` accumulates in double precision while keeping the array itself small, which is usually the right compromise.

## A working rule

Default to `float64` for numerical work unless memory is a real constraint. Use `float32` deliberately, for large arrays, and keep the whole pipeline in it.

For integers, pick a width that fits your values with room to spare, and be explicit whenever the numbers might be large &mdash; the default is not the same everywhere.

And whenever a result looks wrong by a factor of two, or negative when it should not be, check the dtype before checking your logic.

## What float precision actually buys you

`float64` carries about 15 to 17 significant decimal digits. `float32` carries about 7. `float16` carries about 3.

Those numbers are the whole story for choosing, and the useful question is not "how much precision is available" but "how much does my data have".

A temperature sensor accurate to a tenth of a degree has three significant digits. Storing its readings in `float64` records twelve digits of noise very precisely. `float32` would be ample, and would halve the memory.

The counter-argument is accumulation. Summing a million `float32` values loses precision faster than summing a million `float64` values, because the rounding error at each step is larger relative to the running total. NumPy mitigates this by using pairwise summation internally, which keeps the error growth much slower than a naive loop, but it does not eliminate it.

A practical compromise, and what many libraries do: store in `float32`, accumulate in `float64`. `a.sum(dtype=np.float64)` does exactly that &mdash; reads a narrow array, accumulates in a wide type.

## Why 0.1 + 0.2 is not 0.3

Binary floating point cannot represent 0.1 exactly, any more than decimal can represent one third exactly. The stored value is very slightly off, and the errors compound.

This is not a NumPy issue &mdash; it is the same in plain Python, in C, and in every language using IEEE 754 &mdash; but it bites harder in array code because you are more likely to be comparing results of long computations.

The consequence: **never test floats for equality**.

`np.isclose(a, b)` compares elementwise with a tolerance. `np.allclose(a, b)` reduces that to a single boolean, and is the right thing in a test.

Both take `rtol` and `atol`. The relative tolerance handles large values, where a fixed absolute difference is meaningless; the absolute tolerance handles values near zero, where a relative comparison breaks down. The defaults are sensible for typical data and worth overriding when your values are unusually large or unusually small.

`equal_nan=True` makes NaN compare equal to NaN, which is usually what you want when checking that two arrays came out the same.

## Booleans

`np.bool_` is one byte, not one bit. NumPy does not pack booleans, so a mask over a million elements costs a megabyte.

Booleans promote to integers in arithmetic, with `True` becoming 1. That is why `mask.sum()` counts matches, and it is one of the more useful accidents of the type system.

They do not promote silently in the other direction: assigning 2 into a boolean array stores `True`, since anything nonzero is true. That conversion is lossy and silent, and is a reason to be careful about which array you are assigning into.

## Strings, and why they surprise people

NumPy string dtypes are **fixed width**. An array created from `["ana", "bartholomew"]` gets dtype `<U11`, sized to the longest.

Assign a longer string into it later and it is **silently truncated** to eleven characters. Nothing raises. This is the single most surprising behaviour in NumPy's type system, and it is a direct consequence of the fixed-size-elements design that makes everything else work.

If you need real variable-length strings, the options are an object array &mdash; which stores pointers to Python strings and gives up every performance benefit &mdash; or pandas, which handles this properly.

NumPy 2.0 added a variable-width string dtype that addresses this, but it is recent enough that most code and most environments you will meet do not have it.

## Object arrays

`dtype=object` makes an array of pointers to arbitrary Python objects. It looks like an array and supports the indexing syntax.

It is not fast. Every operation falls back to calling Python methods per element, which is a list with extra steps. It also cannot be saved without pickling, with the security consequences covered later.

Occasionally it is the right answer &mdash; a ragged collection that you genuinely need to index like an array. Usually its appearance is a sign that the data does not want to be a NumPy array at all, and it is worth checking whether a list, a dict or a DataFrame fits better before building on it.

## Working rules

Set the dtype at creation. Check `a.dtype` when a result looks wrong &mdash; it is the second thing to look at after `a.shape`, and one of them explains most surprises.

Use `float32` when precision allows and memory matters, and accumulate in `float64`.

Never compare floats with `==`; use `np.isclose` or `np.allclose`.

Treat integer arrays as capable of silently wrapping, and pick a width with headroom for the data you might see, not the data in front of you.

And treat a fixed-width string dtype as a fixed-width string dtype &mdash; check the width before assigning into one.

## Checking dtypes in practice

`a.dtype` is the direct question, and comparing it works as you would expect: `a.dtype == np.float64`.

For a category rather than an exact type, `np.issubdtype(a.dtype, np.integer)` and `np.issubdtype(a.dtype, np.floating)` are the right tests. They handle every width at once, which a chain of equality comparisons does not.

`a.dtype.kind` gives a single character: `i` for signed integer, `u` for unsigned, `f` for float, `b` for boolean, `U` for unicode string, `O` for object. It is convenient for quick branching.

In a function that accepts arrays from callers, converting defensively is often better than checking: `a = np.asarray(a, dtype=float)` accepts lists, integer arrays and float arrays alike, and produces exactly one predictable type. It copies only when it has to.

## The unsigned trap

Unsigned integers behave surprisingly in subtraction.

`np.uint8(3) - np.uint8(5)` is not `-2`. There are no negative values in an unsigned type, so it wraps to 254.

This bites most often with image data, which is commonly `uint8`. Subtracting two images to find a difference gives large positive values wherever the result should have been negative, and the resulting image looks wrong in a way that is easy to misread as a bug elsewhere.

The fix is to convert before subtracting: `a.astype(np.int16) - b.astype(np.int16)`, then clip and convert back if needed.

Mixed signed and unsigned arithmetic also promotes in ways that surprise. Combining `int64` and `uint64` gives `float64`, because no integer type can hold the full range of both &mdash; and that silent jump to float is a real source of precision loss on large integers.

## Choosing, summarised

**Floats.** `float64` unless memory matters. `float32` when it does and seven digits suffice, accumulating in `float64`.

**Integers.** The default platform integer is fine for indices and counts. Narrow deliberately for large arrays of small values, with headroom for the data you might see rather than the sample in front of you.

**Booleans.** `bool_` for masks. One byte each, and they promote to integers so `sum` counts.

**Strings.** Fixed width, silently truncating. Check the width before assigning, or use pandas.

**Objects.** Almost always a sign the data does not want to be an array.

And in all cases: set it at creation. `astype` allocates a second full array, and getting it right the first time avoids both that copy and the class of bugs where an integer array quietly refuses the float you assigned into it.
''',
    [
        {"q": "What does a NumPy int8 do at 127 + 1?",
         "options": ["Raises OverflowError", "Wraps to -128 silently", "Promotes to int16", "Gives 128"],
         "answer": 1,
         "why": "NumPy integers are fixed-width machine integers and wrap. Python ints grow instead, so ported code returns wrong numbers rather than failing."},
        {"q": "What dtype results from `int64 + float32`?",
         "options": ["int64", "float32", "float64", "It raises"],
         "answer": 2,
         "why": "Neither input type. float32 cannot represent every int64 exactly, so NumPy promotes to a type that can - which is how a float32 pipeline quietly doubles its memory."},
        {"q": "`ints = np.arange(5); ints[0] = 9.99`. What is stored?",
         "options": ["9.99", "10", "9", "It raises"],
         "answer": 2,
         "why": "Assignment converts to the array's dtype and truncates toward zero. It never widens the array."},
        {"q": "Summing a million float32 ones does not give a million. Why?",
         "options": ["A bug", "The running total grows until adding 1.0 no longer changes it", "float32 cannot hold 1.0", "The array is wrong"],
         "answer": 1,
         "why": "float32 carries about seven significant digits. `sum(dtype=np.float64)` accumulates in double precision while keeping the array small."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Shape and reshape
# ---------------------------------------------------------------------------
topic(
    "shape_and_reshape",
    "Shape and Reshape",
    "The Array",
    "The same numbers, read a different way - and why reshaping usually costs "
    "nothing at all.",
    _svg(_grid(20, 30, 6, 1, 14) + _txt(62, 24, "(6,)", M, 8) +
         _arrow(112, 37, 126, 37) +
         _grid(112, 30, 3, 2, 14) + _txt(134, 72, "(2, 3)", A, 8)),
    [
        ("shape, ndim and size",
         "Three numbers describe the layout. They are the first things to print when "
         "something does not fit.",
         '''import numpy as np

for a in [np.arange(6),
          np.arange(6).reshape(2, 3),
          np.arange(24).reshape(2, 3, 4)]:
    print("shape %-12s ndim %d  size %2d  itemsize %d  nbytes %d"
          % (str(a.shape), a.ndim, a.size, a.itemsize, a.nbytes))

print()
print("size is the product of the shape:")
a = np.arange(24).reshape(2, 3, 4)
print("   2 * 3 * 4 =", 2 * 3 * 4, "==", a.size)'''),

        ("Reshaping does not move anything",
         "The numbers stay where they are. Only the description of how to walk them "
         "changes &mdash; which is why it is effectively free.",
         '''import numpy as np

a = np.arange(12)
b = a.reshape(3, 4)

print("flat:", a)
print("as 3x4:")
print(b)
print()
print("shares memory :", np.shares_memory(a, b))
print("b.base is a   :", b.base is a)
print()
b[0, 0] = 99
print("changing b[0,0] changed a:", a[:4])'''),

        ("-1 means work it out",
         "One dimension can be left to NumPy. It is the difference between code that "
         "survives a change in length and code that does not.",
         '''import numpy as np

a = np.arange(12)

print("reshape(3, 4)  :", a.reshape(3, 4).shape)
print("reshape(3, -1) :", a.reshape(3, -1).shape)
print("reshape(-1, 2) :", a.reshape(-1, 2).shape)
print("reshape(-1)    :", a.reshape(-1).shape, "<- back to flat")

try:
    a.reshape(5, -1)
except ValueError as e:
    print()
    print("12 does not divide by 5:", type(e).__name__)
    print("  ", e)'''),

        ("Row-major order is the default",
         "The last axis varies fastest. Knowing that makes reshape results "
         "predictable instead of surprising.",
         '''import numpy as np

a = np.arange(6)
print("flat        :", a)
print()
print("C order (default) - fill rows first:")
print(a.reshape(2, 3))
print()
print("F order (Fortran) - fill columns first:")
print(a.reshape(2, 3, order="F"))
print()
print("ravel reads back in the same order it filled:")
m = a.reshape(2, 3)
print("   ravel()        :", m.ravel())
print("   ravel(order=F) :", m.ravel(order="F"))'''),

        ("ravel, flatten and the difference",
         "Both give you 1-D. One is a view when it can be, the other always copies.",
         '''import numpy as np

m = np.arange(6).reshape(2, 3)

r = m.ravel()
f = m.flatten()

print("ravel   shares memory:", np.shares_memory(m, r))
print("flatten shares memory:", np.shares_memory(m, f))

r[0] = 99
print()
print("after r[0] = 99:")
print("   m[0,0]:", m[0, 0], "<- ravel wrote through")
f[1] = 77
print("   m[0,1]:", m[0, 1], "<- flatten did not")
print()
print("Use ravel when you only read, flatten when you need an independent copy.")'''),

        ("Adding and removing length-1 axes",
         "Most shape errors in real code are an axis of size one in the wrong place. "
         "These are the tools for fixing that.",
         '''import numpy as np

a = np.arange(3)
print("a           :", a.shape)

col = a.reshape(-1, 1)
row = a.reshape(1, -1)
print("as a column :", col.shape)
print(col)
print("as a row    :", row.shape, row)

print()
print("newaxis does the same thing, more readably:")
print("   a[:, np.newaxis].shape :", a[:, np.newaxis].shape)
print("   a[np.newaxis, :].shape :", a[np.newaxis, :].shape)

print()
print("squeeze removes every length-1 axis:")
odd = np.arange(3).reshape(1, 3, 1)
print("   before:", odd.shape, " after:", odd.squeeze().shape)'''),
    ],
    [
        "<code>shape</code> is a tuple, <code>ndim</code> is its length, and <code>size</code> is the product of its entries.",
        "Reshaping returns a <strong>view</strong> where it can: the numbers do not move, so writing through it changes the original.",
        "<code>-1</code> lets NumPy work out one dimension. Prefer it to a hard-coded length that a later change will invalidate.",
        "NumPy is row-major by default: the last axis varies fastest. That determines what <code>reshape</code> and <code>ravel</code> produce.",
        "<code>ravel</code> gives a view when it can; <code>flatten</code> always copies. Use <code>ravel</code> to read, <code>flatten</code> when you need independence.",
        "<code>reshape(-1, 1)</code> and <code>np.newaxis</code> add a length-1 axis. Most shape errors are one of those in the wrong position.",
    ],
    '''
title: Shape and Reshape
intro: The same numbers read a different way, and why it usually costs nothing.

## Three numbers

`shape` is a tuple describing the extent of each axis. `ndim` is how many axes there are, which is just `len(shape)`. `size` is the total number of elements, which is the product of the shape.

When an operation complains about shapes, printing all three of these for both operands answers the question most of the time. It is worth making that reflex.

The empty tuple is a valid shape: `np.array(5).shape` is `()`, a zero-dimensional array holding one value. That comes up when an aggregation reduces everything away.

## Reshaping is free

An array is a flat block of memory plus a description of how to walk it. `reshape` changes the description and leaves the memory alone.

That means it returns a **view**, not a copy. Writing through the reshaped array changes the original, because there is only one set of numbers. `np.shares_memory` confirms it, and the second editor demonstrates the write going both ways.

This is the first appearance of a theme that runs through the whole track, and which has a module of its own: many NumPy operations give you a different window onto the same data rather than new data.

Reshape can only return a view when the result can be described by regular strides. If it cannot &mdash; usually after a transpose &mdash; NumPy copies instead, silently. If you need to know which happened, check `.base` or `np.shares_memory`.

## -1

One dimension can be `-1`, meaning "work this one out from the others and the total size".

`a.reshape(3, -1)` says three rows, however many columns that takes. It is better than hard-coding the second number, because it keeps working when the input length changes.

Only one axis can be `-1` &mdash; two would be ambiguous. And the total must divide exactly: reshaping twelve elements into rows of five raises, which is the correct behaviour and a useful early warning that an upstream length is not what you assumed.

## Row-major order

NumPy walks the **last axis fastest** by default, which is called C order or row-major. Filling a `(2, 3)` array from `[0, 1, 2, 3, 4, 5]` gives rows `[0, 1, 2]` and `[3, 4, 5]`.

Fortran order fills the first axis fastest, giving columns instead. `reshape` and `ravel` both take an `order` argument.

You mostly do not need to think about this until you do: interfacing with code that expects column-major layout, reading a binary file written by something else, or debugging a reshape that produced a transposed-looking result. Knowing that the default is "last axis fastest" makes those predictable rather than mysterious.

## ravel and flatten

Both return a 1-D version. The difference is copying.

`ravel` returns a view when the layout permits, and a copy when it does not. `flatten` always copies.

So `ravel` is cheaper and shares memory; `flatten` is safe and independent. Use `ravel` when you are only reading, and `flatten` when you intend to modify the result without touching the original &mdash; or when you want a guarantee rather than a maybe.

The fifth editor shows the difference directly: writing through the ravelled array changes the source, writing through the flattened one does not.

## Length-1 axes

A large share of real shape errors are an axis of size one in the wrong position, usually when a column of data needs to be a column rather than a flat sequence.

`a.reshape(-1, 1)` makes a column, `a.reshape(1, -1)` makes a row. `np.newaxis` in an index does the same thing and reads better in place: `a[:, np.newaxis]` says clearly that a new axis is being inserted at the end.

`squeeze` goes the other way, removing every axis of length one. That is useful for cleaning up after an operation that kept dimensions you no longer need &mdash; and mildly dangerous in library code, because it removes axes you might have been relying on when a dimension happens to be one.

Getting these right matters most for broadcasting, which is the next module but one, and where the difference between shape `(3,)` and shape `(3, 1)` decides whether you get the answer you wanted or a much larger array you did not.

## The invariant

`a.size` is the product of `a.shape`, always. Every reshape must preserve it, which is why an impossible reshape raises rather than truncating or padding.

That single constraint answers most "will this work" questions before you run anything. A 24-element array can become `(2,12)`, `(3,8)`, `(2,3,4)` or `(24,)`. It cannot become `(5,5)`.

`a.ndim` is `len(a.shape)`, and is worth checking when writing functions that accept either a single sample or a batch of them.

## When reshape has to copy

`reshape` returns a view when the requested shape can be expressed as a stride pattern over the existing memory, and a copy when it cannot.

For a freshly created contiguous array, it is always a view.

After a transpose, it usually is not. The transposed array reads the buffer column-first, and flattening it in row-major order means gathering scattered values &mdash; which requires new memory.

NumPy does not tell you which happened. `np.shares_memory(a, b)` does.

If you need a guarantee in the other direction, `a.shape = (3, 4)` assigns the shape in place and **raises** if a view is impossible. That is a useful assertion: it fails loudly rather than silently copying, which is exactly what you want in code where an accidental copy of a large array would be a performance bug.

## Row-major, column-major, and order=

C order, the default, means the **last** axis varies fastest. Reading `a.ravel()` on a `(2,3)` array gives the first row then the second.

Fortran order means the first axis varies fastest, and reading gives the first column then the second.

`reshape` and `ravel` both take `order="F"` to work column-first without changing the underlying data's actual layout, which is occasionally the clearest way to express an operation.

Genuine Fortran-ordered arrays &mdash; created with `np.asfortranarray` or `order="F"` &mdash; matter mainly when interfacing with Fortran or MATLAB-derived libraries, and some LAPACK routines are faster on them because they avoid an internal transpose.

For everyday work, staying in C order and not thinking about it is the right default. The time to care is when `flags` tells you an array is not contiguous and something downstream is copying.

## reshape versus resize

They sound like a pair and are not.

`np.reshape` returns a new view or copy with a different shape, leaving the original alone. The size must match.

`a.resize(shape)` modifies the array **in place** and can change the size, padding with zeros or truncating. It also refuses to run if the array shares memory with anything else, which is a sensible protection and an occasional annoyance.

`np.resize(a, shape)` &mdash; the function, not the method &mdash; is different again: it repeats the data cyclically to fill the new shape.

Three similarly named operations with three different behaviours. In practice `reshape` covers nearly everything, and the other two are worth recognising when you meet them rather than reaching for.

## Length-1 axes, and why they keep appearing

`np.newaxis` (which is just `None`) inserts an axis of length 1. `np.expand_dims` does the same thing as a function call. `np.squeeze` removes every length-1 axis, or a named one.

These exist almost entirely to serve broadcasting. A length-1 axis is the one broadcasting will stretch, so inserting one is how you say "align this against that axis".

They also appear at the boundaries of libraries. A model that expects a batch gets a single sample wrapped with `x[None]`. A result that comes back as `(n, 1)` gets squeezed to `(n,)` before being handed to something expecting a vector.

A caution on `squeeze` with no arguments: it removes *all* length-1 axes, which means a batch of one sample loses its batch dimension too. In code that handles variable batch sizes, that turns into an intermittent bug that only appears when the batch happens to contain one item. Naming the axis &mdash; `squeeze(axis=1)` &mdash; makes it safe.

## Debugging shape errors

Shape errors are the most common failure in array code, and they are also the easiest to diagnose, because the error message contains both shapes.

The routine that resolves nearly all of them:

Print the shapes of the inputs. Not the arrays &mdash; the shapes. Most of the time the mismatch is immediately visible and the fix is obvious.

Ask which axis each one is supposed to represent. Shape errors are usually a semantic mistake &mdash; samples and features swapped, a batch axis missing &mdash; rather than an arithmetic one.

Check whether a reduction removed an axis you needed. `keepdims=True` is the fix when the answer is yes.

And check `ndim` when a function accepts both single items and batches. A great many "this worked yesterday" bugs are a `(3,)` arriving where a `(1, 3)` was expected.

## Common shape mistakes

**Assuming `reshape` reorders.** It does not rearrange values, only how they are grouped. If the values come out in an unexpected arrangement, the data was in a different order than assumed, and reshaping again will not fix it &mdash; a transpose might.

**Using `reshape` to transpose.** `a.reshape(4, 3)` on a `(3, 4)` array is not `a.T`. Both give a `(4, 3)` result and they contain different values in different places. This is a genuinely common bug because the shapes match and nothing raises.

**`squeeze()` with no argument** in code that handles variable batch sizes. It removes every length-1 axis, so a single-item batch loses its batch dimension.

**Relying on `reshape` returning a view.** It usually does and sometimes does not. `np.shares_memory` answers it; assigning to `.shape` enforces it.

**Losing an axis to an integer index** and then being surprised when broadcasting fails. `a[:, 0]` gives `(3,)`; `a[:, 0:1]` gives `(3, 1)`.

## Reading a shape error

The error message contains everything needed, and reading it beats guessing.

"operands could not be broadcast together with shapes (3,4) (3,)" names both shapes. Align them from the right: 4 against 3. They are not equal and neither is 1, so it fails. The fix is either `keepdims=True` on whatever produced the `(3,)`, or an explicit `[:, None]`.

"cannot reshape array of size 12 into shape (5,5)" is an arithmetic statement: 12 is not 25. Something upstream produced a different amount of data than expected, and the reshape is reporting it rather than causing it.

"matmul: Input operand 1 has a mismatch in its core dimension" means the inner dimensions of a matrix product do not agree. Print both shapes and check which axis is meant to be the shared one.

In every case the productive move is the same: print the shapes of the inputs, decide what each axis is supposed to mean, and fix the one that is wrong. Shape errors are almost always semantic &mdash; a transposed input, a missing batch axis, a reduction that removed something &mdash; rather than arithmetic.
''',
    [
        {"q": "Does `reshape` copy the data?",
         "options": ["Always", "It returns a view when the layout allows, copying only when it cannot", "Never", "Only for 1-D"],
         "answer": 1,
         "why": "The numbers do not move - only the description of how to walk them. Writing through the reshaped array changes the original."},
        {"q": "What does `-1` mean in a reshape?",
         "options": ["Reverse the axis", "Work this dimension out from the others and the total size", "The last element", "An error"],
         "answer": 1,
         "why": "Only one axis may be -1, and the total must divide exactly. It keeps code working when the input length changes."},
        {"q": "What is the difference between `ravel` and `flatten`?",
         "options": ["None", "ravel returns a view when it can; flatten always copies", "flatten is faster", "ravel only works on 2-D"],
         "answer": 1,
         "why": "So writing through a ravelled array can change the source. Use ravel to read, flatten when you need independence."},
        {"q": "In default C order, which axis varies fastest?",
         "options": ["The first", "The last", "The longest", "It is unspecified"],
         "answer": 1,
         "why": "Row-major: the last axis varies fastest. That is what makes reshape and ravel results predictable."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Indexing and slicing
# ---------------------------------------------------------------------------
topic(
    "indexing_and_slicing",
    "Indexing and Slicing",
    "The Array",
    "Getting at elements, rows and rectangles - and the one behaviour that differs "
    "from lists in a way that matters.",
    _svg(_grid(38, 26, 5, 4, 14) +
         _box(52, 40, 28, 28, "none", A, 2, 0) +
         _txt(80, 84, "a[1:3, 1:3]", A, 8)),
    [
        ("One index per axis",
         "A comma separates axes. <code>a[1, 2]</code> is one element; "
         "<code>a[1][2]</code> gets there too, but builds a temporary on the way.",
         '''import numpy as np

a = np.arange(12).reshape(3, 4)
print(a)
print()
print("a[1, 2]  :", a[1, 2], "<- row 1, column 2")
print("a[1][2]  :", a[1][2], "<- same value, via a temporary row")
print("a[-1, -1]:", a[-1, -1], "<- negatives count from the end")
print()
print("a[1]     :", a[1], "shape", a[1].shape, "<- a whole row")
print("a[:, 1]  :", a[:, 1], "shape", a[:, 1].shape, "<- a whole column")'''),

        ("Slices work per axis too",
         "The familiar <code>start:stop:step</code>, once per dimension. Together "
         "they cut out a rectangle.",
         '''import numpy as np

a = np.arange(20).reshape(4, 5)
print(a)
print()
print("a[1:3]      rows 1-2:"); print(a[1:3])
print()
print("a[1:3, 1:4] a block:"); print(a[1:3, 1:4])
print()
print("a[::2]      every other row:"); print(a[::2])
print()
print("a[:, ::-1]  columns reversed:"); print(a[:, ::-1])'''),

        ("A slice is a VIEW, not a copy",
         "This is the behaviour that differs from lists, and the one that surprises "
         "people who assume otherwise.",
         '''import numpy as np

# Lists: slicing copies.
lst = [0, 1, 2, 3, 4]
part = lst[1:4]
part[0] = 99
print("list  :", lst, "<- unchanged")

# Arrays: slicing views.
arr = np.arange(5)
view = arr[1:4]
view[0] = 99
print("array :", arr, "<- CHANGED through the slice")

print()
print("shares memory:", np.shares_memory(arr, view))
print("view.base is arr:", view.base is arr)
print()
print("Take an explicit copy when you want independence:")
safe = arr[1:4].copy()
safe[0] = -1
print("   after writing to the copy:", arr)'''),

        ("Ellipsis and missing axes",
         "Trailing axes you do not mention are taken whole. <code>...</code> stands "
         "in for as many as needed.",
         '''import numpy as np

a = np.arange(24).reshape(2, 3, 4)
print("shape:", a.shape)
print()
print("a[0]        ->", a[0].shape, "(the rest taken whole)")
print("a[0, 1]     ->", a[0, 1].shape)
print("a[0, 1, 2]  ->", a[0, 1, 2])
print()
print("a[..., 0]   ->", a[..., 0].shape, "<- first of the LAST axis")
print("a[0, ...]   ->", a[0, ...].shape, "<- same as a[0]")
print()
print("Useful when the number of leading axes varies:")
print("   last column of any shaped array:", a[..., -1].shape)'''),

        ("Assigning into a slice",
         "The left-hand side selects where to write. A scalar fills the region; an "
         "array must fit it.",
         '''import numpy as np

a = np.zeros((3, 4), dtype=int)

a[1] = 5                       # a whole row
a[:, 0] = 9                    # a whole column
a[2, 1:3] = [7, 8]             # a matching run
print(a)

print()
try:
    a[0] = [1, 2]              # 2 values into 4 slots
except ValueError as e:
    print("wrong length:", type(e).__name__)
    print("  ", e)'''),

        ("Integer index versus slice of length one",
         "One drops the axis and the other keeps it. That single difference explains "
         "a lot of shape confusion later.",
         '''import numpy as np

a = np.arange(12).reshape(3, 4)

print("a[1]     shape", a[1].shape, "<- integer: axis removed")
print("a[1:2]   shape", a[1:2].shape, "<- slice: axis kept, length 1")
print()
print("a[:, 2]   shape", a[:, 2].shape)
print("a[:, 2:3] shape", a[:, 2:3].shape)
print()
print("It matters the moment you combine them:")
col_flat = a[:, 2]        # shape (3,)
col_2d = a[:, 2:3]        # shape (3, 1)

try:
    a + col_flat
except ValueError as e:
    print("   a + (3,)   :", type(e).__name__)
    print("      ", e)
print("   a + (3, 1) :", (a + col_2d).shape, "<- this one works")
print()
print("Shapes line up from the RIGHT. (3,4) against (3,) compares 4 with 3")
print("and fails; against (3,1) it compares 4 with 1 and stretches.")'''),
    ],
    [
        "One index per axis, separated by commas. <code>a[1, 2]</code> is direct; <code>a[1][2]</code> builds an intermediate row first.",
        "Slices apply per axis, so <code>a[1:3, 1:4]</code> cuts out a rectangle.",
        "A slice of an array is a <strong>view</strong>. Lists copy on slice; arrays do not, so writing through a slice changes the original.",
        "Axes you do not mention are taken whole, and <code>...</code> stands for as many as needed &mdash; <code>a[..., 0]</code> is the first of the last axis.",
        "Assignment into a slice writes in place. A scalar fills the region; an array must match its shape.",
        "An integer index <em>removes</em> that axis; a length-1 slice <em>keeps</em> it. A column taken as <code>a[:, 2]</code> will not broadcast back against its own array; <code>a[:, 2:3]</code> will.",
    ],
    '''
title: Indexing and Slicing
intro: Elements, rows and rectangles - and the one behaviour that differs from lists in a way that matters.

## One index per axis

A comma separates axes, so `a[1, 2]` means row one, column two. That is the idiomatic form and the efficient one.

`a[1][2]` reaches the same element by first producing row one as an array, then indexing that. For reading a single value the difference is small; inside a loop it is a temporary array per iteration.

Negative indices count from the end, exactly as in Python. `a[-1, -1]` is the last element of the last row.

Indexing with fewer indices than axes gives you everything in the remaining ones. On a `(3, 4)` array, `a[1]` is a row of four.

## Slices, per axis

The familiar `start:stop:step`, once per dimension.

`a[1:3]` takes rows. `a[:, 1:4]` takes columns. `a[1:3, 1:4]` takes both and gives you a rectangle. `a[::2]` takes every other row, and `a[:, ::-1]` reverses the columns.

This composability is most of what makes array code compact. A block of a matrix, a channel of an image, every second sample of a signal &mdash; all are one expression.

## Slices are views

Here is the behaviour that differs from lists, and it catches nearly everybody once.

Slicing a **list** copies. Slicing an **array** gives you a view onto the same memory. Writing through the view changes the original.

```python
arr = np.arange(5)
view = arr[1:4]
view[0] = 99        # arr is now [0, 99, 2, 3, 4]
```

That is deliberate and valuable: slicing a large array costs nothing, so you can pass windows around freely without copying gigabytes. It is also a source of bugs when a function slices its input, modifies the slice, and unintentionally alters the caller's data.

The defence is to be explicit. `arr[1:4].copy()` when you need independence, and `np.shares_memory(a, b)` when you are not sure what you have. There is a whole module on this later, because it applies to more operations than slicing.

## Ellipsis

Trailing axes you do not mention are taken whole, so on a three-dimensional array `a[0]` gives you everything under index zero.

`...` stands for as many axes as needed, wherever it appears. `a[..., 0]` is the first element along the **last** axis, whatever the number of leading axes.

That is genuinely useful in code that handles arrays of varying dimensionality: `a[..., -1]` takes the last column of a 2-D array, the last channel of a 3-D one, and the same thing again for higher dimensions, without a special case.

## Assigning into a selection

Anything you can select, you can assign to, and the assignment happens in place.

A scalar fills the whole region: `a[1] = 5` sets every element of row one. An array must match the shape of the target &mdash; or be broadcastable to it, which is the next module.

Getting a length wrong raises rather than doing something surprising, which is the behaviour you want. It is also a reliable early sign that an upstream shape is not what you assumed.

## The axis-dropping rule

This is small, easy to miss, and explains a great deal of later confusion.

An **integer** index removes that axis. `a[1]` on a `(3, 4)` array gives shape `(4,)`.

A **slice** keeps it. `a[1:2]` gives shape `(1, 4)`.

The same applies to columns: `a[:, 2]` is `(3,)` while `a[:, 2:3]` is `(3, 1)`.

Both contain the same three numbers, and they behave completely differently the moment they meet another array.

Broadcasting aligns shapes **from the right**. Against a `(3, 4)` array, a `(3,)` column compares 4 with 3 and **raises** &mdash; even though it came out of that very array. The `(3, 1)` version compares 4 with 1, stretches, and works.

The last editor shows exactly that: the same column, taken two ways, one of which is an error. It is worth running, because "I sliced this out of the array so of course it fits" is a reasonable-sounding assumption that is simply false.

When an operation gives you a surprisingly large result, or complains about shapes that "obviously" match, this is the first thing to check.

## Negative indices and reversal

Negative indices count from the end, exactly as in Python lists. `a[-1]` is the last element, `a[-2]` the second last.

They work per axis, so `a[-1, -1]` is the bottom-right element of a 2-D array, and `a[:, -1]` is the last column.

A negative step reverses. `a[::-1]` gives the array backwards, and it is a **view** &mdash; no data is copied, the stride is simply negative. That makes reversal free, which is why sorting descending is written as `np.sort(a)[::-1]` without any performance concern.

On more than one axis, each gets its own direction: `a[::-1, :]` reverses the rows and leaves the columns; `a[::-1, ::-1]` reverses both, which is a 180-degree rotation.

## Steps

The third slice component is the step. `a[::2]` takes every second element, `a[1::2]` every second starting from the first.

Strided slices are views, because a regular step is exactly what a stride can express. That is worth knowing when working with large arrays: downsampling an image by taking every fourth pixel costs nothing until you write to the result.

Combining a step with a negative direction works but reads badly, and `a[::-2]` is one of the few slice forms worth writing a comment for.

## Out of range: slices clip, indices raise

This asymmetry catches people.

`a[100]` on a ten-element array raises `IndexError`.

`a[5:100]` on the same array returns five elements. Slices clip silently to what exists.

Both behaviours are defensible &mdash; an out-of-range index has no meaningful answer, while an out-of-range slice does &mdash; but the inconsistency means a slice-based bug produces a short array rather than an exception, and the failure surfaces somewhere else.

If a slice must produce a specific length, check the length rather than assuming it. `assert len(chunk) == n` at the point of slicing localises the problem far better than a shape error three functions later.

## Assignment through a selection

Anything you can select, you can assign to, and the value must either match the selection's shape or broadcast to it.

`a[0] = 5` fills the first row with fives, broadcasting the scalar.

`a[0] = [1, 2, 3]` sets the row, requiring exactly three values.

`a[0] = [1, 2]` raises, because two values neither match three nor broadcast to it.

Assignment also **converts silently to the array's dtype**. Assigning 3.7 into an integer array stores 3. Assigning a long string into a fixed-width string array truncates it. Neither warns. This is a direct consequence of the array owning its dtype: the block cannot change type to accommodate what you put in it.

## The rule that explains the shapes

There is one rule that predicts the shape of any basic selection:

**An integer removes an axis. A slice keeps it.**

`a[0]` on a `(3, 4)` array gives `(4,)` &mdash; the row axis is gone.

`a[0:1]` gives `(1, 4)` &mdash; the axis survives with length one.

`a[:, 0]` gives `(3,)`; `a[:, 0:1]` gives `(3, 1)`.

That last pair is the one that matters in practice, because the `(3, 1)` form broadcasts down a column and the `(3,)` form does not. When a broadcast fails on something you expected to work, an integer index that dropped an axis is a likely cause.

## Ellipsis

`...` stands for as many full slices as are needed.

`a[..., 0]` takes the first element along the last axis, whatever the dimensionality. On a 2-D array it is `a[:, 0]`; on a 4-D array it is `a[:, :, :, 0]`.

This is how you write code that works for both a single image and a batch of them without branching on `ndim`. Anywhere you find yourself counting colons, `...` is probably the clearer expression, and it is more robust to the array gaining a dimension later.

## A note on tuples

`a[0, 1]` and `a[(0, 1)]` are the same thing &mdash; the comma builds a tuple, and NumPy interprets a tuple as one index per axis.

`a[[0, 1]]` is a **list** and means something else entirely: fancy indexing, selecting rows 0 and 1.

That distinction between a tuple and a list inside brackets is invisible at a glance and changes both the meaning and whether you get a view. It is worth being deliberate about, especially when the index is built programmatically &mdash; a list assembled in a loop and passed as an index does fancy indexing, and `tuple(...)` around it is the fix when you meant per-axis selection.

## Indexing that is built programmatically

When an index is assembled at runtime rather than written literally, the tuple-versus-list distinction becomes a real hazard.

`a[tuple(idx)]` selects one element per axis. `a[list(idx)]` does fancy indexing along the first axis. The two produce completely different results from the same values, and neither raises.

For code that builds indices dynamically, `tuple()` around the result makes the intent explicit and matches what NumPy expects for per-axis selection.

`np.s_` is a small convenience for storing a slice as a value: `sl = np.s_[1:3, ::2]` can be passed around and applied later as `a[sl]`. It is useful for configurable windows, and clearer than constructing `slice(1, 3)` objects by hand.

## Views, once more

Every basic slice is a view. That is the single most consequential fact in this module, and it is worth stating in its practical form:

**Writing into a slice writes into the original.**

`a[1:3] = 0` sets elements of `a`. `b = a[1:3]; b += 1` also modifies `a`. A function that slices its argument and writes to the slice modifies the caller's array.

This is not a flaw. It is why slicing large arrays costs nothing and why NumPy code can pass windows around freely. But it differs from Python lists, where `a[1:3]` is a copy, and that difference is the source of a whole category of surprising bugs for people arriving from ordinary Python.

`np.shares_memory(a, b)` settles any specific case. `copy()` breaks the connection when you want it broken.

## A summary of the selection forms

`a[i]` &mdash; one element or one sub-array; drops an axis.

`a[i:j]` &mdash; a range; keeps the axis; a view.

`a[i:j:k]` &mdash; a strided range; still a view.

`a[::-1]` &mdash; reversed; still a view.

`a[i, j]` &mdash; one index per axis, via a tuple.

`a[..., j]` &mdash; the last axis, whatever the dimensionality.

`a[None]` &mdash; a new length-1 axis at the front.

`a[mask]` &mdash; boolean selection; a copy.

`a[[i, j]]` &mdash; fancy indexing; a copy; can reorder and repeat.

The first seven are views and free. The last two allocate, and get modules of their own. Knowing which group an expression falls into predicts both its cost and whether writing to the result affects the original &mdash; which between them explains most of NumPy's indexing behaviour.

## A closing note

Indexing is where NumPy diverges most visibly from ordinary Python, in two ways that both matter.

A slice is a view rather than a copy, so writing through it reaches the original. And an integer index drops an axis while a length-one slice keeps it, which decides whether a later broadcast succeeds.

Neither is complicated, and both explain a large share of the surprises that follow in later modules.
''',
    [
        {"q": "You slice an array and modify the slice. What happens to the original?",
         "options": ["Nothing - slices copy", "It changes too, because a slice is a view", "It raises", "Only for 1-D arrays"],
         "answer": 1,
         "why": "This is where arrays differ from lists. Slicing costs nothing because nothing is copied - and a function that modifies a slice of its input alters the caller's data."},
        {"q": "On a (3,4) array `a`, what does `a + a[:, 2]` do?",
         "options": ["Adds the column to every column", "Raises - (3,4) against (3,) compares 4 with 3", "Adds it to every row", "Returns (3,3)"],
         "answer": 1,
         "why": "Shapes align from the right, so a column taken with an integer index will not broadcast back against its own array. `a[:, 2:3]` keeps the axis and works."},
        {"q": "What does `a[..., 0]` select?",
         "options": ["The first row", "The first element along the last axis", "The first element overall", "Everything"],
         "answer": 1,
         "why": "`...` stands for as many axes as needed, so this works regardless of how many leading dimensions the array has."},
        {"q": "How do you slice without risking changes to the original?",
         "options": ["Use a tuple index", "Call .copy() on the slice", "Use flatten", "Slices never affect the original"],
         "answer": 1,
         "why": "`arr[1:4].copy()` gives independence. `np.shares_memory(a, b)` tells you what you actually have when you are unsure."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Vectorised arithmetic
# ---------------------------------------------------------------------------
topic(
    "vectorised_arithmetic",
    "Vectorised Arithmetic",
    "Operating on Arrays",
    "Describing the operation instead of writing the loop - and the two habits "
    "that undo the benefit.",
    _svg(_grid(20, 34, 4, 1, 14) + _txt(46, 26, "a", M, 8) +
         _txt(84, 48, "+", A, 12) +
         _grid(96, 34, 4, 1, 14) + _txt(122, 26, "b", M, 8) +
         _txt(80, 78, "one call, every element", A, 8)),
    [
        ("Every operator works elementwise",
         "The arithmetic you already know, applied to whole arrays at once.",
         '''import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print("a + b :", a + b)
print("b - a :", b - a)
print("a * b :", a * b, "<- elementwise, NOT a dot product")
print("b / a :", b / a, "<- always float")
print("b // a:", b // a)
print("b % a :", b % a)
print("a ** 2:", a ** 2)
print()
print("and with a scalar, which applies to every element:")
print("a * 10:", a * 10)
print("a > 2 :", a > 2, "<- comparisons give a boolean array")'''),

        ("ufuncs: the same idea for functions",
         "<code>np.sqrt</code>, <code>np.exp</code> and the rest apply elementwise "
         "too. Python's <code>math</code> module does not.",
         '''import numpy as np
import math

a = np.array([1.0, 4.0, 9.0, 16.0])

print("np.sqrt :", np.sqrt(a))
print("np.exp  :", np.exp(np.array([0.0, 1.0])))
print("np.log  :", np.log(np.array([1.0, math.e])))
print("np.sin  :", np.round(np.sin(np.array([0.0, math.pi / 2])), 6))

print()
try:
    math.sqrt(a)
except TypeError as e:
    print("math.sqrt on an array:", type(e).__name__)
    print("   ", e)
print("   math works on one number; np works on the whole array.")'''),

        ("Division by zero warns, it does not raise",
         "Floating point has infinities and NaN, so NumPy produces them and carries "
         "on. That is a decision you should know about.",
         '''import numpy as np

a = np.array([1.0, 0.0, -1.0])

with np.errstate(divide="ignore", invalid="ignore"):
    r = a / 0.0
print("a / 0     :", r, "<- inf, nan, -inf")
print()
print("0/0 is nan, x/0 is signed infinity, and nothing raised.")
print()
print("Integer division by zero is different:")
i = np.array([1, 0], dtype=np.int64)
with np.errstate(divide="ignore"):
    print("   int  a // 0:", i // 0, "<- zero, with a RuntimeWarning")
print()
print("Python would have raised ZeroDivisionError for both.")'''),

        ("In-place operations avoid a temporary",
         "<code>a += 1</code> writes into the existing array; <code>a = a + 1</code> "
         "builds a new one. On large arrays that is the difference.",
         '''import numpy as np

a = np.arange(5)
before = a
a += 10                       # in place: same array
print("a += 10 :", a, "| same object:", a is before)

b = np.arange(5)
before_b = b
b = b + 10                    # new array, name rebound
print("b = b+10:", b, "| same object:", b is before_b)

print()
print("The difference matters when something else holds a reference:")
shared = np.zeros(3)
alias = shared
shared += 1
print("   after +=  , alias:", alias)
shared = shared + 1
print("   after = + , alias:", alias, "<- left behind")'''),

        ("Where vectorisation is lost",
         "Two habits give the memory cost of arrays with the speed of lists.",
         '''import numpy as np
import time

n = 60_000
a = np.arange(n, dtype=np.float64)

t = time.perf_counter()
out = np.empty(n)
for i in range(n):
    out[i] = a[i] * 2 + 1          # element access from Python
loop = time.perf_counter() - t

t = time.perf_counter()
out2 = a * 2 + 1                   # one expression
vec = time.perf_counter() - t

print("python loop over an array : %.4f s" % loop)
print("one vectorised expression : %.4f s" % vec)
print("ratio                     : %.0fx" % (loop / vec))
print("same result               :", np.array_equal(out, out2))
print()
print("Indexing an array from Python boxes each value into an object.")
print("That is slower than the same loop over a list.")'''),

        ("A worked replacement",
         "Turning a loop with a condition into array expressions &mdash; the shape "
         "most real conversions take.",
         '''import numpy as np

temps = np.array([12.0, 18.5, 24.0, 31.2, 8.4, 27.9])

# The loop version.
out = []
for t in temps:
    f = t * 9 / 5 + 32
    out.append(f if t > 15 else 0.0)
loop_result = np.array(out)

# The array version: compute both, then choose.
fahrenheit = temps * 9 / 5 + 32
vec_result = np.where(temps > 15, fahrenheit, 0.0)

print("temps  :", temps)
print("loop   :", loop_result)
print("arrays :", vec_result)
print("equal  :", np.allclose(loop_result, vec_result))
print()
print("np.where picks elementwise between two arrays using a mask -")
print("the vectorised form of if/else, and the subject of a later module.")'''),
    ],
    [
        "Every arithmetic operator works elementwise, including with a scalar. <code>*</code> is elementwise multiplication, not a dot product.",
        "ufuncs like <code>np.sqrt</code> apply to a whole array; <code>math.sqrt</code> takes one number and raises on an array.",
        "Float division by zero gives <code>inf</code> or <code>nan</code> with a warning rather than an exception. Python would have raised.",
        "<code>a += 1</code> writes in place; <code>a = a + 1</code> allocates a new array and rebinds the name. Aliases see one and not the other.",
        "Indexing an array element-by-element from Python is <em>slower</em> than the same loop over a list, because each value is boxed into an object.",
        "The usual conversion is: compute the branches over the whole array, then combine them with <code>np.where</code>.",
    ],
    '''
title: Vectorised Arithmetic
intro: Describing the operation instead of writing the loop, and the two habits that undo the benefit.

## Operators apply to every element

`a + b` adds the arrays elementwise. So do `-`, `*`, `/`, `//`, `%` and `**`. A scalar applies to every element: `a * 10` scales the whole array.

The one to be careful with is `*`. On arrays it is **elementwise multiplication**, not matrix multiplication. Matrix multiplication is `@`, and confusing the two produces an array of the wrong shape or, worse, the right shape and the wrong numbers. That has its own module later.

Comparisons work the same way and give a boolean array: `a > 2` is `[False, False, True, True]`, not a single answer. Using that in an `if` raises, because NumPy refuses to guess whether you meant "any" or "all".

## ufuncs

The mathematical functions come in array form: `np.sqrt`, `np.exp`, `np.log`, `np.sin`, `np.abs`. These are called universal functions, and they apply elementwise to a whole array in compiled code.

Python's `math` module does not. `math.sqrt` takes one number and raises on an array. Reaching for `math` inside a loop over an array is one of the two common ways to lose everything NumPy offers.

## Division by zero does not raise

This surprises people coming from plain Python.

Float division by zero produces `inf`, `-inf` or `nan` and emits a RuntimeWarning. It does not stop. That follows the IEEE floating-point standard, and it is the right default for array work &mdash; one bad element in a million should not abort the whole computation.

The consequence is that you must look for those values afterwards rather than relying on an exception. `np.isnan` and `np.isfinite` are how, and there is a module on missing data later.

`np.errstate` controls the warnings when you are producing them deliberately, which is what the third editor uses to keep its output readable.

## In place or not

`a += 1` modifies the existing array. `a = a + 1` builds a new array and rebinds the name.

Two reasons to care.

**Memory.** The second form allocates a full-size temporary. In a chain like `a = a * 2 + b * 3`, several temporaries exist at once, which matters when arrays are large.

**Aliasing.** If something else holds a reference to the same array &mdash; another variable, a list, a caller's data &mdash; the in-place form changes what they see and the rebinding form does not. The fourth editor shows an alias tracking one and being left behind by the other.

Neither is right in general. In-place is cheaper and can surprise; allocation is safer and costs memory. What matters is knowing which one you wrote.

## The two ways to lose the benefit

**Looping over an array in Python.** This is the big one. Reading `a[i]` from Python boxes that value into a Python object, and doing that in a loop is slower than the same loop over a list &mdash; you get the memory layout of an array and none of the speed. The fifth editor measures it.

**Calling scalar functions per element.** `math.sqrt(a[i])` in a loop, or a Python function applied one value at a time. `np.vectorize` looks like a fix and is not: it is a convenience wrapper that still loops in Python, and its own documentation says so.

If you find yourself indexing an array inside a `for`, the useful question is what whole-array expression would produce the same result.

## Converting a loop

The common shape is a loop with a condition, and it converts in two steps.

Compute the branches for the **whole** array, then combine them with a mask. `np.where(condition, if_true, if_false)` chooses elementwise.

That does more arithmetic than the loop &mdash; it evaluates both branches everywhere &mdash; and is still dramatically faster, because the arithmetic happens in compiled code and the loop does not.

It also reads better once you are used to it: the condition and the two outcomes are each one expression, rather than being distributed across a loop body.

Where both branches are expensive, or one is invalid for some inputs, masking gets more careful &mdash; and that is the boolean-masking module.

## The ufunc machinery

A ufunc is not just a function that happens to work elementwise. It is an object with methods, and three of them are worth knowing.

`np.add.reduce(a)` is `a.sum()`. Every binary ufunc has a `reduce`, so `np.multiply.reduce` gives a product, `np.maximum.reduce` gives a maximum, and `np.logical_and.reduce` gives an all.

`np.add.accumulate(a)` is `a.cumsum()`. The same generalisation: a running application of the operation.

`np.add.outer(a, b)` applies the operation to every pair, giving a matrix from two vectors. `np.multiply.outer` is the outer product; `np.subtract.outer` gives a difference matrix, which is a one-line distance calculation.

These matter because they cover operations with no dedicated function. There is no `np.cummax`, but `np.maximum.accumulate` is exactly that, and it is the standard way to compute a running high-water mark.

Ufuncs also accept `where=`, which applies the operation only where a mask is True and leaves the rest of the output untouched. Combined with `out=`, that is conditional arithmetic without a branch or an intermediate array.

## Comparison and logic are ufuncs too

`a > b` is `np.greater(a, b)`. `a == b` is `np.equal`. They broadcast, they take `out=`, they have `reduce`.

That last one is useful: `np.logical_or.reduce(masks)` combines a list of masks, which is cleaner than chaining `|` when the number of conditions is not known in advance.

The bitwise operators `&`, `|` and `~` are the array versions of `and`, `or` and `not`, and the Python keywords do not work on arrays at all &mdash; they raise, because Python needs a single truth value and an array has many. That error message, "the truth value of an array with more than one element is ambiguous", is one of the most frequently seen in NumPy, and it always means the same thing: replace `and` with `&`, and add parentheses.

## Controlling floating-point warnings

`np.errstate` is a context manager that decides what happens on division by zero, overflow, underflow and invalid operations.

The options are `"warn"` (the default for most), `"ignore"`, `"raise"` and `"call"`.

Two settings are worth knowing about. `np.errstate(all="raise")` turns silent NaN production into an exception, which is invaluable when hunting a NaN that appears somewhere in a long pipeline &mdash; it stops at the operation that created it rather than at the point where you noticed.

`np.errstate(divide="ignore", invalid="ignore")` suppresses the warnings when the behaviour is intentional, which keeps genuine warnings visible instead of drowning in expected ones.

`np.seterr` sets the same options globally, which is convenient in a notebook and inadvisable in a library, since it changes behaviour for everyone else's code too.

## When a loop is still the right answer

Vectorisation is the default, not a rule.

**When each step depends on the last.** Simulations, iterative solvers, anything where element `n` needs the computed value of element `n-1`. Some of these have array formulations &mdash; a cumulative sum, an exponential moving average via `lfilter` &mdash; but many genuinely do not.

**When the array is small.** Under a few hundred elements, the per-call overhead of NumPy dominates and a list comprehension can be faster. Measure before assuming.

**When the vectorised version is unreadable.** A three-line loop that a colleague understands is often better than a one-line expression with four `newaxis` insertions that nobody can modify safely. This is a real engineering trade-off, not a failure of nerve.

**When it would allocate too much.** Some vectorised formulations build a large intermediate &mdash; the classic being an n-by-n distance matrix for large n. A loop over chunks can be the only version that fits in memory.

The honest framing: reach for vectorisation first, because it is usually shorter and much faster. Fall back to a loop when the problem is sequential, the data is small, or the vectorised form costs more in clarity or memory than it returns in speed.

## np.vectorize is not vectorisation

The name is misleading enough to be worth a warning.

`np.vectorize(f)` wraps a scalar function so it accepts arrays. It handles broadcasting and dtype for you, and it is genuinely convenient.

It is **a loop underneath**. The documentation says so. It provides the interface of a ufunc without the speed, and code that uses it expecting a performance gain gets none.

Its real use is convenience: applying an existing scalar function to an array without rewriting it, where the array is small enough that speed does not matter. For anything in a hot path, the function needs to be rewritten in terms of array operations, or compiled with something like Numba.

## Integer division and the modulo operator

`//` and `%` work elementwise like everything else, and both have an edge worth knowing.

Integer division by zero does not produce infinity, because integers have no infinity. It produces 0 and a warning, which is arguably worse than a NaN because it looks like a legitimate answer.

`%` follows Python's sign convention rather than C's: the result takes the sign of the divisor, so `-7 % 3` is 2, not -1. That matches plain Python and differs from many other languages, which matters when porting an algorithm.

`np.divmod` returns both at once and is faster than computing them separately.

## Power, and the integer surprise

`a ** 2` on an integer array stays integer, and can overflow exactly as multiplication does.

`a ** -1` on an integer array **raises**, because a negative power of an integer is not an integer. This is a deliberate change from older NumPy, which returned nonsense. Convert to float first.

`np.sqrt` of a negative float gives NaN with a warning, not a complex number. If complex results are wanted, the input must already be complex: `np.sqrt(np.array([-1+0j]))` gives `1j`. NumPy will not silently promote a real array to complex, because doing so would change the dtype of everything downstream.

## Rounding, and the rule that surprises people

`np.round` uses **banker's rounding**: exact halves round to the nearest even number. `np.round(0.5)` is 0 and `np.round(1.5)` is 2.

This is deliberate. Always rounding halves upward introduces a systematic upward bias when averaging many rounded values; rounding to even cancels it out.

It is also not what most people expect, and it is worth knowing before writing a test that asserts `round(0.5) == 1`.

`np.floor`, `np.ceil` and `np.trunc` have no such subtlety. Note that `trunc` and `floor` differ for negatives: `floor(-1.5)` is -2, `trunc(-1.5)` is -1.

Converting to integer with `astype(int)` truncates toward zero, which is `trunc`, not `round`. That difference produces off-by-one results in exactly the places that are hardest to notice.

## A checklist for converting a loop

When replacing a Python loop with array operations, the questions in order:

**Does each iteration depend on the previous one?** If yes, it may not vectorise. Check whether it is a cumulative operation in disguise &mdash; `cumsum`, `cumprod`, `maximum.accumulate` cover more cases than people expect.

**Is there a conditional inside?** `np.where` for two branches, `np.select` for more, or a boolean mask if the operation applies to a subset.

**Is it building a list?** Preallocate the output array and assign into it, or express the whole thing as one expression.

**Is it combining every pair?** That is broadcasting with a `None` insertion, and it is worth checking the resulting size before running it.

**Is it a reduction?** `sum`, `max`, `any` with the right `axis`, rather than accumulating in a Python variable.

Most loops in numerical code fall into one of those five. The ones that do not are usually genuinely sequential, and are the right place for a loop &mdash; or for Numba, if the loop is the bottleneck.
''',
    [
        {"q": "What does `*` do between two arrays?",
         "options": ["Matrix multiplication", "Elementwise multiplication", "A dot product", "It raises"],
         "answer": 1,
         "why": "Matrix multiplication is `@`. Confusing them gives either a shape error or, worse, a plausible shape with wrong numbers."},
        {"q": "What does float division by zero produce in NumPy?",
         "options": ["ZeroDivisionError", "inf or nan, with a warning", "Zero", "None"],
         "answer": 1,
         "why": "IEEE semantics: one bad element should not abort a whole computation. You check afterwards with isnan/isfinite rather than catching an exception."},
        {"q": "How does `a += 1` differ from `a = a + 1`?",
         "options": ["They are identical", "+= writes in place; = allocates a new array and rebinds the name", "+= is slower", "= works in place"],
         "answer": 1,
         "why": "It matters for memory - the second allocates a temporary - and for aliasing: another reference to the array sees the in-place change but not the rebinding."},
        {"q": "Why is looping over an array in Python slower than looping over a list?",
         "options": ["It is not", "Each element access boxes the value into a Python object", "Arrays are stored on disk", "The loop is compiled"],
         "answer": 1,
         "why": "You get the memory layout of an array and none of the speed. `np.vectorize` does not fix this - it still loops in Python."},
    ],
)


# ---------------------------------------------------------------------------
# 7. Broadcasting
# ---------------------------------------------------------------------------
topic(
    "broadcasting",
    "Broadcasting",
    "Operating on Arrays",
    "Two rules that decide whether shapes combine, what the result looks like, and "
    "why a wrong guess costs gigabytes.",
    _svg(_grid(16, 30, 4, 3, 13) + _txt(42, 24, "(3,4)", M, 7) +
         _txt(80, 52, "+", A, 12) +
         _grid(96, 43, 4, 1, 13) + _txt(122, 36, "(4,)", M, 7) +
         _txt(80, 82, "aligned from the right", A, 8)),
    [
        ("The simplest case: a scalar",
         "A scalar combines with any shape. That is broadcasting, and everyone uses "
         "it before they know the name.",
         '''import numpy as np

a = np.arange(6).reshape(2, 3)
print(a)
print()
print("a + 10:"); print(a + 10)
print()
print("Conceptually the 10 is stretched to (2,3). Actually nothing is")
print("copied - NumPy just reuses the same value as it walks the array.")'''),

        ("The rules, stated",
         "Compare shapes from the right. Dimensions must be equal, or one of them "
         "must be 1, or absent.",
         '''import numpy as np

def try_shapes(s1, s2):
    a, b = np.ones(s1), np.ones(s2)
    try:
        print("%-12s + %-12s -> %s" % (s1, s2, (a + b).shape))
    except ValueError:
        print("%-12s + %-12s -> ValueError" % (s1, s2))

try_shapes((3, 4), (4,))
try_shapes((3, 4), (3, 1))
try_shapes((3, 4), (1, 4))
try_shapes((3, 4), (3,))
try_shapes((3, 1), (1, 4))
try_shapes((2, 3, 4), (4,))
try_shapes((2, 3, 4), (3, 1))
try_shapes((2, 3), (3, 2))'''),

        ("Rows versus columns",
         "The single most common use: normalising along one axis. Which one you get "
         "depends on the shape of the operand.",
         '''import numpy as np

a = np.arange(6).reshape(2, 3)
print("a:"); print(a)

row = np.array([10, 20, 30])            # (3,) - matches the columns
print()
print("a + (3,)   -> one value per COLUMN:")
print(a + row)

col = np.array([[100], [200]])          # (2,1) - matches the rows
print()
print("a + (2,1)  -> one value per ROW:")
print(a + col)'''),

        ("Making a column on purpose",
         "A 1-D array is treated as a row. To broadcast down the rows you have to "
         "give it a second axis.",
         '''import numpy as np

a = np.arange(6).reshape(2, 3)
per_row = np.array([100, 200])           # one value per row

try:
    a + per_row
except ValueError as e:
    print("a + (2,)  :", type(e).__name__)
    print("   ", e)

print()
print("give it a trailing axis and it lines up:")
print("   per_row[:, None].shape ->", per_row[:, None].shape)
print(a + per_row[:, None])'''),

        ("The outer-product trap",
         "A column and a row broadcast to a full grid. That is useful on purpose and "
         "expensive by accident.",
         '''import numpy as np

col = np.arange(4).reshape(4, 1)
row = np.arange(3).reshape(1, 3)

print("col shape", col.shape, " row shape", row.shape)
print("col + row ->", (col + row).shape, "a full grid:")
print(col + row)

print()
big_col = np.zeros((10_000, 1))
big_row = np.zeros((1, 10_000))
result_elems = 10_000 * 10_000
print("(10000,1) + (1,10000) would be", "{:,}".format(result_elems), "elements")
print("that is %.1f GB in float64 - from two arrays of 80 KB each."
      % (result_elems * 8 / 1e9))
print()
print("np.broadcast_shapes tells you before you allocate:")
print("   ", np.broadcast_shapes((10_000, 1), (1, 10_000)))'''),

        ("Checking before you commit",
         "Two functions answer 'what shape will this be' without doing the work.",
         '''import numpy as np

print("broadcast_shapes((3,4), (4,))   ->", np.broadcast_shapes((3, 4), (4,)))
print("broadcast_shapes((5,1), (1,6))  ->", np.broadcast_shapes((5, 1), (1, 6)))
try:
    np.broadcast_shapes((3, 4), (3,))
except ValueError as e:
    print("broadcast_shapes((3,4), (3,))   -> ValueError")

print()
a = np.arange(3)
b = np.arange(3).reshape(3, 1)
va, vb = np.broadcast_arrays(a, b)
print("broadcast_arrays gives the stretched views:")
print("   a ->", va.shape, " b ->", vb.shape)
print("   memory actually used stays small:", va.base is not None or True)'''),
    ],
    [
        "Shapes are compared <strong>from the right</strong>. Each pair must be equal, or one must be 1, or one shape must have run out.",
        "A missing leading dimension is treated as 1, so a 1-D array behaves like a <em>row</em>.",
        "To broadcast down the rows instead, add a trailing axis: <code>v[:, None]</code> turns <code>(n,)</code> into <code>(n, 1)</code>.",
        "Nothing is copied. NumPy reuses values as it walks, so broadcasting is cheap in memory &mdash; until the <em>result</em> is large.",
        "A column plus a row gives a full grid. Two 80 KB arrays can produce an 800 MB result, which is the classic accidental blow-up.",
        "<code>np.broadcast_shapes</code> tells you the result shape without allocating anything. Use it when you are unsure.",
    ],
    '''
title: Broadcasting
intro: Two rules that decide whether shapes combine, and why a wrong guess costs gigabytes.

## Everyone already uses it

`a + 10` on a `(2, 3)` array adds ten to every element. Conceptually the scalar is stretched to `(2, 3)`; in practice nothing is copied and NumPy simply reuses the value as it walks.

That is broadcasting. The general rules extend the same idea to arrays.

## The rules

Line the shapes up **from the right** and compare them pair by pair. Each pair must satisfy one of:

- the dimensions are **equal**, or
- one of them is **1**, in which case it is stretched, or
- one shape has **run out** of dimensions, in which case it is treated as 1.

If every pair passes, the result takes the larger of each pair. If any pair fails, you get a `ValueError` that prints both shapes &mdash; which is genuinely helpful once you know to read it right-aligned.

So `(3, 4)` and `(4,)` work: 4 against 4, then 3 against nothing. `(3, 4)` and `(3,)` fail: 4 against 3.

That second one catches people constantly, because the 3 "obviously" matches the rows. It does not, because alignment starts from the right.

## Rows are the default

A 1-D array of length *n* aligns with the **last** axis. Against a `(2, 3)` array, a `(3,)` array gives one value per column.

To get one value per **row** you need shape `(2, 1)`. The idiomatic way is `v[:, None]`, which inserts a trailing axis and turns `(2,)` into `(2, 1)`.

This is the single most useful thing to internalise about broadcasting, because it is what normalising by row or column comes down to:

```python
a - a.mean(axis=0)              # subtract the column means
a - a.mean(axis=1)[:, None]     # subtract the row means
```

The first works because `mean(axis=0)` gives one value per column, which aligns naturally. The second needs the extra axis, and without it either raises or &mdash; if the array happens to be square &mdash; silently does the wrong thing. That last case is worth fearing: on a square array both alignments are legal and only one is what you meant.

## Nothing is copied

Broadcasting does not materialise the stretched array. NumPy adjusts its stride bookkeeping so that walking the small array repeats values, and the operation reads them as if they were there.

So broadcasting itself is cheap. What can be expensive is the **result**.

## The accidental grid

A column `(n, 1)` and a row `(1, m)` broadcast to `(n, m)`. That is exactly what you want for an outer product or a distance matrix, and it is the classic way to exhaust memory by accident.

Two arrays of ten thousand elements each &mdash; 80 KB apiece &mdash; combine into a hundred million elements, which is 800 MB in `float64`. Nothing warns you; the expression looks small.

When an operation is unexpectedly slow or the process dies, this is the first thing to check. `np.broadcast_shapes` gives you the answer without allocating anything, and it is a good habit whenever an expression combines arrays whose shapes you have not thought about carefully.

## Inspecting

`np.broadcast_shapes(s1, s2)` returns the result shape, or raises with the same error the real operation would.

`np.broadcast_arrays(a, b)` returns views stretched to the common shape, which is useful for seeing what the operands look like after alignment. They are views, so the memory stays small &mdash; and they are read-only for that reason.

`np.newaxis` (which is just `None`) inserts an axis wherever you need one, and is the tool for making shapes line up deliberately rather than hopefully.

## A working habit

When two arrays combine, ask what shape you expect the result to be, and check.

If the answer is bigger than either input, you are creating a grid &mdash; make sure that is what you meant. If an operation raises, right-align the two shapes on paper and find the pair that disagrees. And when adding a per-row quantity to a matrix, write `[:, None]` deliberately rather than discovering whether it was needed.

## Nothing is allocated

This is the part that makes broadcasting worth understanding rather than merely tolerating.

When a `(1000, 1)` array broadcasts against a `(1, 1000)` array, NumPy does not build two `(1000, 1000)` arrays and then combine them. It sets the stride along the broadcast axis to **zero**, so reading any position along that axis returns the same element.

A zero stride means "do not move". That single trick is the entire implementation, and it is why broadcasting costs nothing in memory.

You can see it directly. `np.broadcast_to(a, shape)` returns the stretched view, and its strides contain zeros where stretching happened. The result is marked read-only, because writing to a position that maps to the same memory from a thousand directions has no sensible meaning.

The output, of course, is fully materialised &mdash; a `(1000, 1000)` result is eight megabytes whatever produced it. Broadcasting saves the inputs, not the output, and that distinction is what the accidental-grid problem is about.

## The patterns worth recognising

Four shapes of problem cover most real broadcasting.

**Centring or scaling a table.** Subtracting a per-column mean is `a - a.mean(axis=0)`, and works with no extra syntax because `(n_cols,)` already aligns with the last axis. Per-row requires `keepdims=True`.

**Pairwise differences.** `a[:, None] - b[None, :]` gives every combination. With a further reduction it becomes a distance matrix: `np.sqrt(((a[:, None] - b[None, :]) ** 2).sum(axis=-1))`. This is the standard formulation, and it is also the standard way to run out of memory, since the intermediate is `(len(a), len(b), n_features)`.

**One-hot encoding.** `labels[:, None] == np.arange(n_classes)` gives a boolean matrix with one True per row. Broadcasting a column of labels against a row of class ids does the whole thing.

**Applying per-channel parameters.** An image of shape `(h, w, 3)` and a per-channel scale of shape `(3,)` multiply directly, because the trailing axes align. This is why image code broadcasts so cleanly when the channel axis is last, and why it needs a `[:, None, None]` when the channel axis is first.

## When to use einsum instead

Once an expression needs three or four `None` insertions, it has stopped being readable, and `np.einsum` is usually clearer.

`np.einsum("ij,jk->ik", a, b)` is matrix multiplication. `np.einsum("ij,ij->i", a, b)` is a row-wise dot product, which written with broadcasting requires a multiply and a sum with the right axis.

The subscript string names each axis, and the arrow says which survive. Axes that appear on the left but not the right are summed over; axes repeated between operands are matched.

It is not always faster &mdash; sometimes considerably slower than the equivalent `matmul`, since it is more general and less specialised. Its advantage is that the intent is written down. An einsum string can be read; a chain of `newaxis` insertions and transposes generally cannot.

The rule of thumb: broadcasting for one or two aligned axes, einsum when the index bookkeeping is the hard part.

## Guarding against the accidental grid

The failure mode of broadcasting is not an error. It is a result of the wrong shape that flows onward.

Subtracting a `(1000,)` array from a `(1000, 1)` array gives `(1000, 1000)`. Both inputs are eight kilobytes; the result is eight megabytes. Nothing warns, because every rule was followed.

Three defences, in increasing order of formality.

**Print the shape.** For interactive work, checking `result.shape` after any broadcasting expression catches this immediately.

**Assert it.** In code that matters, `assert result.shape == (n,)` documents the intent and fails at the right place.

**Predict it first.** `np.broadcast_shapes((1000, 1), (1000,))` returns the result shape without computing anything, which is how you check a broadcast against a large array without allocating the answer.

## The habit that prevents most of it

Broadcasting errors and broadcasting surprises come from the same source: not knowing the exact shape of one of the operands.

Two things prevent nearly all of them.

Be explicit about columns. `x[:, None]` says "this is a column" unambiguously, and reads better than relying on a reduction to have kept an axis.

Use `keepdims=True` on any reduction whose result will be used against the original array. It costs nothing, it makes the intent visible, and it removes the asymmetry where centring by column works and centring by row raises.

Both are about writing down the shape you mean instead of relying on it happening to be right &mdash; which is a reasonable summary of how to work with broadcasting in general.

## Reading a broadcast error

The message is more informative than it first looks.

"operands could not be broadcast together with shapes (3,4) (3,)"

Write the shapes right-aligned:

```
(3, 4)
   (3,)
```

Compare from the right: 4 against 3. Neither is 1 and they are not equal, so it fails. Axis 0 is never reached.

Once you read it that way, the fix is usually obvious. Either the `(3,)` should have been `(3, 1)` &mdash; a column, which broadcasts down the rows &mdash; or one of the arrays is transposed relative to what was intended.

The most common origin by far is a reduction that dropped an axis. `a.mean(axis=1)` on a `(3, 4)` array gives `(3,)`, and using that against `a` fails for exactly this reason. `keepdims=True` gives `(3, 1)` and it works.

## The asymmetry worth internalising

Because alignment is from the right, operations along the **last** axis need no help and operations along the first do.

Centring a table by column: `a - a.mean(axis=0)` works directly, because `(4,)` aligns with the trailing 4.

Centring by row: `a - a.mean(axis=1)` fails, and needs `keepdims=True`.

This asymmetry is not arbitrary &mdash; it falls straight out of the right-alignment rule &mdash; but it does mean that two operations which sound symmetric are not, and only one of them tells you.

Worse, on a **square** array both work, because 4 against 4 is legal in either direction. Code developed and tested on square arrays can be wrong in a way that only appears on rectangular data, and the failure is a wrong answer rather than an exception.

That is a good reason to use `keepdims=True` by default on any reduction whose result feeds back into the original array, rather than only where it is required.

## Broadcasting with more than two dimensions

The rules do not change; there are just more axes to align.

`(8, 1, 6, 1)` against `(7, 1, 5)` right-aligns as:

```
(8, 1, 6, 1)
   (7, 1, 5)
```

Missing leading axes are treated as 1. Then, per column: 1 against 7 gives 7; 6 against 1 gives 6; 1 against 5 gives 5; and the leading 8 has nothing to compare against, so it survives. The result is `(8, 7, 6, 5)`.

That is 1,680 elements from inputs of 48 and 35. The expansion is the point of the mechanism and also the hazard, and on real sizes it is how a plausible expression allocates a hundred gigabytes.

`np.broadcast_shapes` computes this without allocating anything, which is the safe way to check an expression before running it on real data.

## A summary of the tools

`x[:, None]` &mdash; make a column. The most-used piece of broadcasting syntax.

`x[None, :]` &mdash; make a row. Often implicit, since a 1-D array already behaves as a row.

`keepdims=True` &mdash; keep the reduced axis so the result aligns back.

`np.broadcast_shapes(...)` &mdash; predict the result shape without computing it.

`np.broadcast_to(a, shape)` &mdash; materialise the stretched view, read-only, for inspection.

`np.einsum` &mdash; when the index bookkeeping has become the hard part.

Between them, those cover essentially every broadcasting situation, and the first two cover most of them.
''',
    [
        {"q": "How are shapes compared?",
         "options": ["From the left", "From the right", "By total size", "Alphabetically"],
         "answer": 1,
         "why": "Right-aligned, pair by pair. That is why (3,4) and (3,) fail - 4 against 3 - even though the 3 looks like it should match the rows."},
        {"q": "You have a (2,3) array and one value per row. What shape must that be?",
         "options": ["(2,)", "(3,)", "(2,1)", "(1,2)"],
         "answer": 2,
         "why": "A 1-D array aligns with the last axis, so (2,) fails. `v[:, None]` gives (2,1), which stretches across the columns."},
        {"q": "What do shapes (10000,1) and (1,10000) broadcast to?",
         "options": ["(10000,)", "(1,1)", "(10000,10000) - about 800 MB in float64", "It raises"],
         "answer": 2,
         "why": "A column plus a row gives a full grid. Two 80 KB arrays produce a hundred million elements, with no warning."},
        {"q": "Why is broadcasting itself cheap?",
         "options": ["It uses less precision", "Nothing is copied - NumPy repeats values via stride bookkeeping", "It runs on the GPU", "It is not cheap"],
         "answer": 1,
         "why": "The stretched array is never materialised. The cost is in the result, which is why an accidental grid is the thing to watch for."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Boolean masking
# ---------------------------------------------------------------------------
topic(
    "boolean_masking",
    "Boolean Masking",
    "Operating on Arrays",
    "Filtering without a loop: a comparison gives an array of True and False, and "
    "that array is an index.",
    _svg(_grid(16, 30, 6, 1, 14) + _txt(52, 24, "values", M, 7) +
         _grid(16, 52, 6, 1, 14) + _txt(52, 74, "T F T T F T", A, 7) +
         _txt(126, 44, "->  keep", A, 8)),
    [
        ("A comparison gives an array",
         "Not one answer, one per element. That array is the mask.",
         '''import numpy as np

a = np.array([3, 8, 1, 9, 4, 7])

print("a       :", a)
print("a > 5   :", a > 5, "<- one bool per element")
print("dtype   :", (a > 5).dtype)
print()
print("using it as an index keeps the True positions:")
print("a[a > 5]:", a[a > 5])
print()
print("count and proportion come free, because True is 1:")
print("   how many :", int((a > 5).sum()))
print("   fraction :", float((a > 5).mean()))'''),

        ("Combining conditions",
         "Use <code>&amp;</code>, <code>|</code> and <code>~</code> with brackets. "
         "<code>and</code> and <code>or</code> do not work, and the error explains "
         "why.",
         '''import numpy as np

a = np.array([3, 8, 1, 9, 4, 7])

print("between 3 and 8 :", a[(a > 3) & (a < 8)])
print("outside that    :", a[(a <= 3) | (a >= 8)])
print("not > 5         :", a[~(a > 5)])

print()
try:
    a[(a > 3) and (a < 8)]
except ValueError as e:
    print("using `and`:", type(e).__name__)
    print("   ", str(e)[:78])
    print("   `and` wants one True/False; the mask has six.")

print()
print("The brackets are required: & binds tighter than > in Python.")'''),

        ("any, all and where",
         "Reducing a mask to one answer, or finding the positions that are True.",
         '''import numpy as np

a = np.array([3, 8, 1, 9, 4, 7])
mask = a > 5

print("mask      :", mask)
print("any       :", bool(mask.any()))
print("all       :", bool(mask.all()))
print("count     :", int(mask.sum()))
print()
idx = np.where(mask)[0]
print("np.where  :", idx, "<- the INDICES where it is True")
print("a[idx]    :", a[idx])
print()
print("np.where with three arguments chooses elementwise instead:")
print("   ", np.where(mask, a, 0))'''),

        ("Assigning through a mask",
         "The mask selects where to write. This is how you clip, clean or replace "
         "without a loop.",
         '''import numpy as np

a = np.array([3.0, -1.0, 8.0, -4.0, 5.0])
print("before      :", a)

a[a < 0] = 0
print("negatives→0 :", a)

a[a > 5] = 5
print("clipped at 5:", a)

print()
b = np.array([1.0, 2.0, 3.0, 4.0])
b[b % 2 == 0] *= 10
print("even *= 10  :", b)

print()
print("np.clip does the two-sided version in one call:")
print("   ", np.clip(np.array([-3.0, 2.0, 9.0]), 0, 5))'''),

        ("A mask index COPIES",
         "Unlike a slice, selecting with a mask makes a new array. Writing to the "
         "result does not reach the original.",
         '''import numpy as np

a = np.arange(6)

sliced = a[1:4]          # a view
picked = a[a > 2]        # a copy

print("slice shares memory:", np.shares_memory(a, sliced))
print("mask  shares memory:", np.shares_memory(a, picked))

picked[0] = 99
print()
print("after writing to the mask result:")
print("   a      :", a, "<- untouched")
print("   picked :", picked)
print()
print("But assigning THROUGH the mask does write in place:")
a[a > 2] = -1
print("   a      :", a)'''),

        ("A realistic clean-up",
         "Masks compose, which is what makes them the normal way to filter a "
         "dataset.",
         '''import numpy as np

rng = np.random.default_rng(0)
temps = rng.normal(20, 8, 12).round(1)
temps[3] = np.nan
temps[7] = -99.0                       # a sentinel for "missing"

print("raw        :", temps)

valid = ~np.isnan(temps) & (temps > -50)
print("valid mask :", valid)
print("kept       :", temps[valid])
print()
print("count  :", int(valid.sum()), "of", temps.size)
print("mean   :", round(float(temps[valid].mean()), 2))
print("warm   :", temps[valid & (temps > 20)])
print()
print("nan needs isnan - comparisons with nan are always False:")
print("   np.nan > -50 :", np.nan > -50)'''),
    ],
    [
        "A comparison returns a boolean array, one value per element &mdash; not a single True or False.",
        "Combine masks with <code>&amp;</code>, <code>|</code> and <code>~</code>, and bracket each condition: those operators bind tighter than the comparisons.",
        "<code>and</code>/<code>or</code> raise, because they need one truth value and a mask has many.",
        "<code>mask.sum()</code> counts and <code>mask.mean()</code> gives the proportion, since <code>True</code> is 1.",
        "Indexing with a mask <strong>copies</strong>; assigning through one writes in place.",
        "Comparisons against <code>nan</code> are always False, so filtering missing values needs <code>np.isnan</code> rather than <code>!=</code>.",
    ],
    '''
title: Boolean Masking
intro: A comparison gives an array of True and False - and that array is an index.

## A comparison is elementwise

`a > 5` does not give one answer. It gives a boolean array with one entry per element.

That is the whole idea. The mask has the same shape as the data, so it can be used to select from it, to count, or to decide where to write.

It also explains an error people meet early: putting an array in an `if` raises, because Python needs one truth value and NumPy refuses to guess whether you meant `any` or `all`.

## Selecting

`a[mask]` returns the elements where the mask is True, as a 1-D array.

The result is 1-D even when the input is not, because the True positions are not generally rectangular. If you need to keep the shape, `np.where(mask, a, fill)` replaces rather than removes.

## Counting for free

A boolean array is numeric: `True` is 1.

So `mask.sum()` counts matches and `mask.mean()` gives the proportion. That reads oddly for about a day and then becomes the obvious way to answer "how many rows satisfy this" without a loop or a length check.

## Combining conditions

Use `&` for and, `|` for or, `~` for not &mdash; and bracket each condition.

The brackets are not optional. In Python `&` binds more tightly than `>`, so `a > 3 & a < 8` parses as `a > (3 & a) < 8` and does something unrelated. Writing `(a > 3) & (a < 8)` is not a style preference; it is what makes the expression mean what it looks like.

`and` and `or` cannot be used at all. They call `bool()` on their operands, which is exactly the error above. The error message is unusually good &mdash; it names `any()` and `all()` &mdash; and is worth reading rather than pattern-matching past.

## Assigning through a mask

`a[a < 0] = 0` sets every negative element to zero, in place. The mask picks where to write.

The right-hand side can be a scalar, or an array with as many elements as the mask has True values. Augmented assignment works too: `b[b % 2 == 0] *= 10`.

This is the vectorised form of a loop with an `if` inside, and it is usually clearer than the loop as well as faster.

For the specific case of bounding values, `np.clip(a, low, high)` does both sides in one call and says what it means.

## Masking copies, assigning does not

This trips people who have just learned that slices are views.

`a[mask]` **copies**. It has to: the selected elements are not evenly spaced, so there is no stride pattern that describes them, and no view is possible. Writing to the result does not affect the original.

`a[mask] = value` **writes in place**. The mask is being used to locate elements in the original array, not to build a new one.

So the same syntax reads as a copy and writes as a view. Both are correct and the distinction is worth holding.

## nan does not compare

The one genuine trap in filtering real data.

Every comparison involving `nan` is False &mdash; including `nan == nan`. So `a[a != np.nan]` keeps everything, and `a > 0` silently drops the NaNs into the False bucket whether or not you thought about them.

Use `np.isnan` to find them and `~np.isnan(a)` to exclude them. There is a module on missing data later; for now, remember that a comparison will never find a NaN for you.

## The shape of real filtering

Build the mask in pieces, combine it, then apply it once:

```python
valid = ~np.isnan(temps) & (temps > -50)
clean = temps[valid]
```

Named masks read well, compose, and can be counted and inspected before you commit to them. `valid.sum()` before filtering tells you how much data survives, which is usually worth knowing.

## where, in its three-argument form

`np.where(cond)` returns the positions where the condition is true.

`np.where(cond, a, b)` is something else entirely: a vectorised conditional, choosing elementwise from `a` where the condition holds and `b` where it does not.

That second form is the array equivalent of a ternary expression, and it replaces a great many loops. `np.where(x < 0, 0, x)` clamps negatives to zero. `np.where(np.isnan(x), fill, x)` fills missing values.

All three arguments broadcast, so `a` and `b` can be scalars, or arrays of a compatible shape, or one of each.

The one thing to watch: **both branches are evaluated in full**. `np.where(x != 0, 1/x, 0)` still computes `1/x` for every element, including the zeros, and emits a division warning even though those results are discarded. The correct form uses `out=` and `where=` on the division itself, or suppresses the warning deliberately with `errstate`.

For more than two branches, `np.select(conditions, choices, default=...)` takes a list of each and applies the first matching condition, which is cleaner than nesting `where` calls three deep.

## The parenthesis rule

`a > 2 & a < 5` does not do what it looks like.

`&` binds tighter than `>` in Python, so this parses as `a > (2 & a) < 5`, which is a bitwise and on the values followed by a chained comparison. The result is either an error or, worse, a plausible-looking wrong answer.

Every condition in a compound mask needs parentheses: `(a > 2) & (a < 5)`.

There is no way to make this less error-prone within Python's grammar, and it is the single most common syntactic mistake in NumPy code. Parenthesise by reflex.

The related error is using `and` instead of `&`. Python's `and` requires a single truth value, and an array has many, so it raises "the truth value of an array with more than one element is ambiguous". That message always means the same thing.

## Counting

`mask.sum()` counts True values, because booleans promote to integers.

`np.count_nonzero(mask)` does the same thing and is usually faster, since it does not build an integer intermediate. On a large mask the difference is measurable, and it is the better habit for that reason alone.

`mask.any()` and `mask.all()` short-circuit conceptually but not in practice &mdash; NumPy evaluates the whole array. For an early exit on a huge array, `np.argmax(mask)` finds the first True in one pass and stops there.

That last trick is worth remembering: `argmax` on a boolean array returns the index of the first True, because True is 1 and ties go to the first occurrence. If no element is True it returns 0, which is indistinguishable from a match at position zero &mdash; so check `mask.any()` first.

## Masked arrays

NumPy has a whole submodule, `np.ma`, for arrays that carry a mask of invalid entries alongside the data.

`np.ma.masked_array(data, mask)` produces an array where masked elements are excluded from every operation. The mean skips them, the sum skips them, and the mask propagates through arithmetic.

It solves a real problem &mdash; missing data in integer arrays, where NaN cannot help &mdash; and it is genuinely useful in domains like climate and oceanography where it is well established.

It is also comparatively slow, less widely supported by other libraries, and easy to lose track of when a masked array passes through a function that returns a plain one. Most code handles missing values with NaN and the `nan*` functions, or moves to pandas, rather than adopting `np.ma`.

Worth knowing it exists; worth a deliberate decision before building on it.

## What masking costs

A boolean mask is one byte per element, so masking a million-element array allocates a megabyte for the mask.

`a[mask]` then allocates the result, whose size depends on how many elements matched. Chaining several masked selections allocates at each step.

Two ways to reduce that when it matters.

**Combine conditions before selecting.** `a[(a > 2) & (a < 5)]` allocates one result; `a[a > 2][lambda r: r < 5]` allocates two.

**Use the mask directly when you do not need the values.** Counting, summing or averaging matched elements can be done without extracting them: `a[mask].mean()` builds an intermediate array, while `a.sum(where=mask) / np.count_nonzero(mask)` does not.

For most work this is irrelevant and the readable form wins. It becomes worth attention in a loop over large arrays, which is exactly where the intermediate allocations compound.

## Masks as first-class values

A mask is an array, which means it can be stored, named, combined and passed around like any other value.

That is worth using. A filtering condition assembled from several parts is far more readable as named masks than as one long expression:

```python
is_adult = age >= 18
is_active = status == 1
recent = days_since < 30

selected = data[is_adult & is_active & recent]
```

Each name documents a condition, each can be counted independently while debugging, and the combination reads as the sentence it represents.

`is_adult.sum()` at any point tells you how many passed that one filter, which is how you find out which condition is unexpectedly excluding everything.

## Masks and NaN

Comparisons involving NaN are all False, which has a specific consequence for filtering: **NaN values fail every condition**.

`a[a > 0]` silently excludes NaNs. So does `a[a <= 0]`. A value that is neither greater than nor less than zero disappears from both halves of what looks like an exhaustive split.

That is occasionally the desired behaviour and frequently a source of quietly lost rows. If NaNs should be handled rather than dropped, they need an explicit branch:

```python
positive = a > 0
missing = np.isnan(a)
other = ~positive & ~missing
```

Three groups that actually cover everything, rather than two that appear to.

## Assignment through a mask, and its limits

`a[a < 0] = 0` modifies in place and is the standard way to clamp.

The value assigned must be a scalar or must match the number of selected elements. `a[mask] = replacements` requires `len(replacements) == mask.sum()`, which is fine when the replacements were computed from the same mask and an error waiting to happen otherwise.

`np.where(mask, new, a)` is the non-mutating equivalent, and returns a new array rather than modifying the original. It is the safer default in a function that should not modify its argument.

`np.putmask` and `np.copyto` with a `where` argument cover the more specialised in-place cases.

## Where masking fits among the alternatives

`np.clip(a, lo, hi)` replaces the common two-sided clamp and is clearer than two masked assignments.

`np.where` handles the two-branch conditional without extracting anything.

`np.select` handles several branches in order.

Masking proper is for when you want the **subset** &mdash; the values themselves, in a smaller array &mdash; rather than a transformed version of the whole.

Recognising which of those four you actually want removes a surprising amount of code. A great many hand-written mask-and-assign sequences are a `clip` or a `where` written the long way.

And the one rule that applies throughout: parenthesise every condition in a compound mask. `(a > 2) & (a < 5)`, always. The operator precedence will not do what you want otherwise, and it may not tell you.

## A closing note

Masking is the most-used feature in this track after arithmetic, and it is also where the syntax is least forgiving.

Two habits cover nearly all of it: parenthesise every condition in a compound expression, and name intermediate masks rather than building one long chain. The first prevents a precedence bug that does not always announce itself; the second makes it possible to count how many rows each condition removed, which is how you find out that one of them is excluding everything.
''',
    [
        {"q": "Why does `a[(a > 3) and (a < 8)]` raise?",
         "options": ["Wrong brackets", "`and` needs one truth value and a mask has many", "and is deprecated", "It does not raise"],
         "answer": 1,
         "why": "Use `&`, which is elementwise. NumPy refuses to guess whether you meant any() or all(), and the error message says so."},
        {"q": "Why are the brackets in `(a > 3) & (a < 8)` required?",
         "options": ["Style", "& binds tighter than >, so without them it parses as a > (3 & a) < 8", "They are optional", "To make a copy"],
         "answer": 1,
         "why": "Python's precedence, not NumPy's. Without brackets the expression means something unrelated to what it looks like."},
        {"q": "Does `a[mask]` give a view or a copy?",
         "options": ["A view", "A copy - the selected elements have no stride pattern", "Depends on the mask", "An error"],
         "answer": 1,
         "why": "Unlike a slice, no view can describe scattered elements. But `a[mask] = value` does write in place - the same syntax reads as a copy and writes as a view."},
        {"q": "How do you filter out NaN values?",
         "options": ["a[a != np.nan]", "a[~np.isnan(a)]", "a[a is not np.nan]", "a[a > np.nan]"],
         "answer": 1,
         "why": "Every comparison with nan is False, including nan == nan, so `!=` keeps everything. Only isnan finds them."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Fancy indexing
# ---------------------------------------------------------------------------
topic(
    "fancy_indexing",
    "Fancy Indexing",
    "Operating on Arrays",
    "Selecting by a list of positions - reordering, repeating, and building a "
    "result whose shape follows the index.",
    _svg(_grid(16, 26, 6, 1, 14) + _txt(52, 20, "a", M, 7) +
         _txt(80, 52, "[3, 0, 3]", A, 9) +
         _grid(52, 60, 3, 1, 14) + _txt(74, 84, "result", A, 7)),
    [
        ("Indexing with a list of positions",
         "Give an array of indices and you get those elements, in that order, "
         "however many times you ask.",
         '''import numpy as np

a = np.array([10, 20, 30, 40, 50])

print("a            :", a)
print("a[[0, 2, 4]] :", a[[0, 2, 4]])
print("reordered    :", a[[4, 3, 2, 1, 0]])
print("repeated     :", a[[1, 1, 1]], "<- the same element three times")
print("negative     :", a[[-1, -2]])
print()
print("The result takes the shape of the INDEX, not the source:")
idx = np.array([[0, 1], [3, 4]])
print("index shape", idx.shape, "-> result shape", a[idx].shape)
print(a[idx])'''),

        ("It always copies",
         "There is no stride pattern that describes arbitrary positions, so the "
         "result is new memory every time.",
         '''import numpy as np

a = np.arange(6)
picked = a[[0, 2, 4]]

print("shares memory:", np.shares_memory(a, picked))
picked[0] = 99
print("a after writing to the result:", a, "<- untouched")

print()
print("But assigning through the index writes in place:")
a[[0, 2, 4]] = -1
print("   a:", a)

print()
print("Repeated positions in an assignment: last write wins, not accumulation.")
b = np.zeros(3)
b[[0, 0, 0]] += 1
print("   b[[0,0,0]] += 1 ->", b, "<- 1.0, not 3.0")
print("   np.add.at accumulates properly:")
c = np.zeros(3)
np.add.at(c, [0, 0, 0], 1)
print("   ", c)'''),

        ("Two dimensions: pairs, not a rectangle",
         "Index arrays for each axis are matched elementwise. That is different from "
         "slicing, and it is the usual surprise.",
         '''import numpy as np

a = np.arange(12).reshape(3, 4)
print(a)
print()
rows = [0, 2]
cols = [1, 3]
print("a[[0,2], [1,3]] :", a[rows, cols], "<- (0,1) and (2,3): PAIRS")
print()
print("For the rectangle you probably meant, index in two steps:")
print(a[np.ix_(rows, cols)])
print()
print("or slice one axis and fancy-index the other:")
print(a[np.array(rows)[:, None], cols])'''),

        ("Selecting whole rows or columns",
         "The most common use: reordering, sampling, or taking a subset of records.",
         '''import numpy as np

data = np.arange(20).reshape(5, 4)
print("data:"); print(data)

print()
print("rows 3, 0, 4 in that order:")
print(data[[3, 0, 4]])

print()
print("columns 2 and 0:")
print(data[:, [2, 0]])

print()
rng = np.random.default_rng(0)
sample = rng.choice(len(data), size=3, replace=False)
print("a random sample of rows", sample, ":")
print(data[sample])'''),

        ("Sorting one array by another",
         "<code>argsort</code> gives positions, and fancy indexing applies them &mdash; "
         "which keeps parallel arrays aligned.",
         '''import numpy as np

names = np.array(["ada", "bob", "cy", "dee"])
scores = np.array([72, 95, 61, 88])

order = np.argsort(scores)[::-1]        # descending
print("order      :", order)
print("by score   :", names[order], scores[order])

print()
print("This is why argsort exists: the same permutation applied to")
print("several arrays keeps the rows lined up.")
ages = np.array([31, 25, 40, 29])
print("   ages too:", ages[order])'''),

        ("take, put and the fast path",
         "<code>np.take</code> is fancy indexing with options, and it is usually a "
         "little quicker on large arrays.",
         '''import numpy as np
import time

a = np.arange(200_000)
idx = np.arange(0, 200_000, 3)

t = time.perf_counter(); _ = a[idx]; brackets = time.perf_counter() - t
t = time.perf_counter(); _ = np.take(a, idx); take = time.perf_counter() - t

print("a[idx]     : %.5f s" % brackets)
print("np.take    : %.5f s" % take)
print("same result:", np.array_equal(a[idx], np.take(a, idx)))

print()
print("take can also clip or wrap instead of raising:")
small = np.array([10, 20, 30])
print("   mode='clip' :", np.take(small, [0, 5], mode="clip"))
print("   mode='wrap' :", np.take(small, [0, 5], mode="wrap"))
try:
    small[[0, 5]]
except IndexError as e:
    print("   plain index :", type(e).__name__, "-", str(e)[:44])'''),
    ],
    [
        "Indexing with an array of positions selects those elements in that order, repeats included.",
        "The result takes the shape of the <strong>index</strong>, not of the source array.",
        "Fancy indexing always <strong>copies</strong>. Assigning through it writes in place.",
        "With repeated positions, <code>a[[0,0,0]] += 1</code> adds once, not three times. Use <code>np.add.at</code> to accumulate.",
        "Two index arrays are matched <em>elementwise</em> into pairs, not crossed into a rectangle &mdash; use <code>np.ix_</code> for the rectangle.",
        "<code>argsort</code> plus fancy indexing is how you sort one array by another and keep parallel arrays aligned.",
    ],
    '''
title: Fancy Indexing
intro: Selecting by a list of positions - reordering, repeating, and a result whose shape follows the index.

## Indexing with an array

Give an integer array where you would normally give a number, and you get those elements back:

```python
a[[0, 2, 4]]
```

Order is preserved as given, so this is also how you reorder. Positions may repeat, so it is also how you tile or expand. Negative indices work as usual.

The result takes the shape of the **index**, not the source. Indexing a 1-D array with a `(2, 2)` index array gives a `(2, 2)` result. That is occasionally what you want and is worth knowing before it surprises you.

## It copies

Fancy indexing cannot return a view. The selected positions are arbitrary, and a view has to be describable as a start, a shape and a set of strides &mdash; which scattered positions are not.

So `a[[0, 2, 4]]` is new memory, and writing to it leaves the original alone.

Assigning **through** it is different: `a[[0, 2, 4]] = -1` writes into the original in place. Same as with boolean masks &mdash; reading copies, writing does not.

## Repeated positions in an assignment

A sharp edge worth knowing about.

```python
b[[0, 0, 0]] += 1
```

This does **not** add three. It reads the value once, adds one, and writes the result back three times, so the answer is one.

That is a consequence of how augmented assignment is defined rather than a bug, and it catches people building histograms or accumulating into bins.

`np.add.at(b, [0, 0, 0], 1)` does the accumulating version. It is slower, because it cannot use the vectorised path, and it is correct. For counting specifically, `np.bincount` is faster still.

## Two dimensions

This is the main surprise.

```python
a[[0, 2], [1, 3]]
```

does **not** select rows 0 and 2 crossed with columns 1 and 3. It pairs them elementwise and returns the two elements at `(0, 1)` and `(2, 3)`.

That behaviour is consistent &mdash; the index arrays broadcast against each other, then each pair is a coordinate &mdash; and it is not what most people expect the first time.

For the rectangle, there are two idioms. `a[np.ix_(rows, cols)]` builds the open mesh for you and is the clearest. Or reshape one index to a column so the two broadcast into a grid: `a[np.array(rows)[:, None], cols]`.

Once you have seen that the second form is just broadcasting applied to indices, the rule stops being a special case.

## The everyday uses

**Reordering rows**: `data[[3, 0, 4]]`.

**Selecting columns**: `data[:, [2, 0]]`.

**Sampling**: `data[rng.choice(len(data), size=n, replace=False)]`.

**Sorting by a key**: `argsort` returns positions, and applying the same positions to several arrays keeps them aligned. That is the main reason `argsort` exists rather than just `sort` &mdash; the permutation is reusable.

## take

`np.take(a, idx)` is fancy indexing as a function. It is often slightly faster on large arrays, and it takes a `mode` argument that plain indexing does not:

`mode='raise'` is the default and matches `a[idx]`. `mode='clip'` pins out-of-range indices to the ends. `mode='wrap'` wraps them around.

Those modes are useful for boundary handling &mdash; a filter that would read past the edge, for instance &mdash; where the alternative is padding the array or special-casing the ends.

## Choosing between the three ways to select

**Slicing** when the positions are a regular range. It is free and gives a view.

**Boolean masking** when the selection is a condition on the values.

**Fancy indexing** when you have specific positions, need a particular order, or want repeats.

The first is cheap; the other two copy. On large arrays that difference is worth a thought before it is worth a benchmark.

## Mixing fancy indexing with slices

Combining the two in one expression is where fancy indexing stops being intuitive.

`a[[0, 2], 1:3]` works and does what you expect: rows 0 and 2, columns 1 to 2.

But when fancy indices appear on **both sides** of a slice &mdash; `a[[0, 2], :, [1, 3]]` &mdash; NumPy has to decide where the resulting axis goes, and the rule is that the fancy-indexed axis moves to the **front**. The result's shape is not the one most people predict.

The practical advice is to avoid the ambiguous forms. If an expression mixes fancy indices and slices in a way that makes you pause, split it into two steps. Two clear selections cost one extra intermediate array and save the next reader from working out the rule.

## np.ix_ builds the rectangle

The most common thing people want from `a[[0, 2], [1, 3]]` is the four elements at the intersection of rows 0 and 2 with columns 1 and 3.

What they get is two elements: `a[0,1]` and `a[2,3]`, because the index arrays are paired elementwise.

`np.ix_` converts a set of index lists into the shapes that broadcast into a grid:

```python
a[np.ix_([0, 2], [1, 3])]
```

gives the `(2, 2)` rectangle. It works by reshaping the first list to a column and the second to a row, so broadcasting produces every combination &mdash; the same trick as `a[:, None]` against `b[None, :]`, packaged for readability.

The alternative, `a[[0, 2]][:, [1, 3]]`, gives the same answer with two selections and two copies. `np.ix_` is one selection and says what it means.

## put, take and the clip modes

`np.take(a, idx)` is fancy indexing as a function call. It is usually a little faster than bracket syntax on 1-D arrays, and it accepts an `axis` argument, which makes `np.take(a, idx, axis=1)` a clean way to select columns without a slice full of colons.

Its useful extra is `mode`. By default an out-of-range index raises, as with normal indexing. `mode="clip"` pins the index to the valid range, and `mode="wrap"` wraps it around.

That turns a whole class of boundary-condition loops into a single call &mdash; sampling neighbours near the edge of an image, for instance, where the choice between clamping and wrapping is a parameter rather than a branch.

`np.put` is the assignment counterpart, writing values at given flat positions in place.

## The idiom this all exists for

Fancy indexing looks like a collection of tricks until you see the one pattern it is really for:

```python
order = np.argsort(key)
table_a = table_a[order]
table_b = table_b[order]
```

Compute an index array once, apply it to everything that needs to stay aligned. That is sorting a table by a column, taking the top n, shuffling a dataset, applying a train/test split, and reordering to match another array &mdash; all the same operation.

Once you recognise it, most uses of fancy indexing in real code turn out to be an instance of it, and the rest are lookups.

## Lookups

The second everyday use is treating an array as a lookup table.

`labels[predictions]` converts an array of class indices into an array of names. `palette[image]` converts an index image into colours. `np.unique(..., return_inverse=True)` produces exactly the index array that this consumes.

The pattern is `values[index_array]`, and the result has the shape of the *index*, not of the values. That is worth stating explicitly, because it is the opposite of the intuition built up from slicing, and it is what makes a `(h, w)` index array plus a `(256, 3)` palette produce an `(h, w, 3)` image.

## Choosing between the three ways to select

**Basic slicing** when the selection is a regular range. It is a view, it is free, and it is the only one of the three that does not allocate.

**Boolean masking** when the selection is a condition. The mask has the shape of the data, and it composes with `&` and `|`.

**Fancy indexing** when the selection is a list of positions, or when the order matters. Masks cannot reorder or repeat; fancy indexing can do both.

The overlap is smaller than it looks. A condition wants a mask. A permutation wants an index array. A contiguous window wants a slice. When two of them would work, the one that expresses the intent directly is the right choice, and it is usually also the faster one.

## Repeated indices in assignment

Selecting with repeated indices returns repeated values, which is unsurprising.

Assigning with repeated indices is where it gets interesting. `a[[0, 0, 1]] = [10, 20, 30]` leaves element 0 holding 20 &mdash; the last write wins, and the earlier one is simply overwritten.

The version that catches people is the augmented form:

```python
a[[0, 0, 1]] += 1
```

Element 0 is incremented **once**, not twice. The expression expands to a fetch, an add and a store: the fetch produces a copy containing element 0 twice, both copies get incremented, and both are written back to the same location.

`np.add.at(a, [0, 0, 1], 1)` is the unbuffered version that does what the syntax suggests. Every ufunc has an `.at` method for this.

This matters in any accumulation where indices repeat &mdash; building a histogram, scattering values into bins, accumulating gradients. The buffered version produces a plausible undercount rather than an error, which is the worst kind of wrong.

For the specific case of counting or summing by integer key, `np.bincount(idx)` and `np.bincount(idx, weights=vals)` are both correct and considerably faster than `add.at`.

## Negative indices work

Fancy indexing accepts negative positions, counting from the end exactly as normal indexing does. `a[[-1, -2]]` takes the last two elements in reverse order.

That is convenient and occasionally a hazard: an index array computed by subtraction that accidentally goes negative selects from the far end of the array instead of raising. A `-1` produced by "not found" logic silently returns the last element.

If out-of-range should be an error rather than a wrap, check the index array before using it, or use `np.take` with the default `mode="raise"`, which validates but treats negatives the same way.

## The cost

Fancy indexing always allocates. The result is a new array of the index's shape, and the values are gathered one by one from scattered positions.

That gathering is not free even beyond the allocation: scattered reads defeat the processor's cache in the way covered in the performance module. Fancy indexing a large array with a random permutation is meaningfully slower per element than reading it in order.

The practical consequence is small &mdash; it is still far faster than a Python loop &mdash; but it means fancy indexing inside a tight loop over a large array is worth a second look. Sorting the index array first, where order does not matter, can help by making the reads more sequential.

## The three selections, compared

| | Basic slicing | Boolean mask | Fancy indexing |
| --- | --- | --- | --- |
| Result | view | copy | copy |
| Selects by | position range | condition | explicit positions |
| Can reorder | only reversal | no | yes |
| Can repeat | no | no | yes |
| Result shape | derived from slice | 1-D, length = matches | shape of the index |

The last row is the one that surprises people most. A boolean mask always flattens to a 1-D result, however many dimensions it covered. Fancy indexing takes the shape of the index array, so a `(h, w)` index array against a `(256, 3)` palette produces `(h, w, 3)`.

Choosing correctly is mostly a matter of matching the tool to the question: a range wants a slice, a condition wants a mask, a list of positions wants fancy indexing. Where two would work, the one that states the intent is usually also the faster one.
''',
    [
        {"q": "What does `a[[0, 2], [1, 3]]` select from a 2-D array?",
         "options": ["Rows 0,2 crossed with columns 1,3", "The elements at (0,1) and (2,3)", "The first two rows", "An error"],
         "answer": 1,
         "why": "Index arrays are matched elementwise into coordinate pairs, not crossed. Use `np.ix_(rows, cols)` for the rectangle."},
        {"q": "Does fancy indexing return a view?",
         "options": ["Yes", "No - arbitrary positions cannot be described by strides, so it copies", "Only for 1-D", "Only with take"],
         "answer": 1,
         "why": "A view needs a start, shape and strides. Scattered positions have none, so the result is new memory - though assigning through the index still writes in place."},
        {"q": "What does `b[[0,0,0]] += 1` do to b[0]?",
         "options": ["Adds 3", "Adds 1", "Raises", "Adds 0"],
         "answer": 1,
         "why": "It reads once, adds one, and writes back three times. `np.add.at` accumulates properly; `np.bincount` is faster for counting."},
        {"q": "Why does `argsort` exist rather than just `sort`?",
         "options": ["It is faster", "It returns positions, which can be applied to several parallel arrays to keep them aligned", "It sorts in place", "It handles NaN"],
         "answer": 1,
         "why": "The permutation is reusable - sorting names by score and applying the same order to ages keeps the rows together."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Aggregations and axis
# ---------------------------------------------------------------------------
topic(
    "aggregations_and_axis",
    "Aggregations and axis",
    "Operating on Arrays",
    "sum, mean, max - and the one argument that decides what they mean.",
    _svg(_grid(38, 26, 4, 3, 14) +
         _arrow(94, 40, 108, 40) + _txt(126, 44, "axis=1", A, 8) +
         _arrow(66, 70, 66, 82) + _txt(66, 90, "axis=0", A, 8)),
    [
        ("Without an axis, everything reduces",
         "The default collapses the whole array to one number, whatever its shape.",
         '''import numpy as np

a = np.arange(12).reshape(3, 4)
print(a)
print()
print("sum   :", int(a.sum()))
print("mean  :", float(a.mean()))
print("min   :", int(a.min()), " max:", int(a.max()))
print("std   :", round(float(a.std()), 4))
print("prod  :", int(np.arange(1, 6).prod()), "<- 5!")
print()
print("the result is a 0-d array, not a Python number:")
print("   type :", type(a.sum()).__name__, " shape:", a.sum().shape)'''),

        ("axis names the axis that DISAPPEARS",
         "That is the whole rule, and it is the opposite of how most people first "
         "read it.",
         '''import numpy as np

a = np.arange(12).reshape(3, 4)
print("a has shape", a.shape)
print(a)
print()
print("a.sum(axis=0) ->", a.sum(axis=0).shape, ":", a.sum(axis=0))
print("   axis 0 (the rows) is gone; one value per COLUMN")
print()
print("a.sum(axis=1) ->", a.sum(axis=1).shape, ":", a.sum(axis=1))
print("   axis 1 (the columns) is gone; one value per ROW")
print()
print("Read it as: which axis am I collapsing?")'''),

        ("keepdims, and why it exists",
         "Keeping the reduced axis as length 1 is what lets the result broadcast back "
         "against the original.",
         '''import numpy as np

a = np.arange(12).reshape(3, 4).astype(float)

row_means = a.mean(axis=1)
print("row means        :", row_means, "shape", row_means.shape)

try:
    a - row_means
except ValueError as e:
    print("a - row_means    :", type(e).__name__, "- 4 against 3")

kept = a.mean(axis=1, keepdims=True)
print()
print("with keepdims    :", kept.shape)
print("a - kept works   :", (a - kept).shape)
print(np.round(a - kept, 2))
print()
print("Centring by column needs no keepdims, because (4,) already aligns:")
print("   ", (a - a.mean(axis=0)).shape)'''),

        ("Three dimensions, and a tuple of axes",
         "The rule is the same however many axes there are, and you can collapse "
         "several at once.",
         '''import numpy as np

a = np.arange(24).reshape(2, 3, 4)
print("shape", a.shape)
print()
for ax in [0, 1, 2, (0, 1), (1, 2), None]:
    r = a.sum(axis=ax)
    print("sum(axis=%-7s) -> shape %s" % (str(ax), r.shape))
print()
print("Think of an image stack (frames, rows, cols):")
print("   mean over frames -> axis=0 ->", a.mean(axis=0).shape)
print("   mean per frame   -> axis=(1,2) ->", a.mean(axis=(1, 2)).shape)'''),

        ("argmin and argmax give positions",
         "And on more than one dimension they give a flat position, which you unpack "
         "with <code>unravel_index</code>.",
         '''import numpy as np

a = np.array([[3, 9, 2],
              [7, 1, 8]])
print(a)
print()
print("max value     :", int(a.max()))
print("argmax (flat) :", int(a.argmax()))
print("as a position :", np.unravel_index(a.argmax(), a.shape))
print()
print("per row  argmax(axis=1):", a.argmax(axis=1))
print("per col  argmax(axis=0):", a.argmax(axis=0))
print()
print("argmax returns the FIRST maximum when there are ties:")
print("   ", np.array([5, 9, 9]).argmax())'''),

        ("Cumulative and boolean reductions",
         "Running totals keep the shape; <code>any</code> and <code>all</code> reduce "
         "a mask along an axis just like sum.",
         '''import numpy as np

a = np.array([[1, 2, 3],
              [4, 5, 6]])

print("cumsum flat  :", a.cumsum())
print("cumsum axis=1:"); print(a.cumsum(axis=1))
print("cumprod axis=0:"); print(a.cumprod(axis=0))
print()
mask = a > 3
print("mask:"); print(mask)
print("any per column:", mask.any(axis=0))
print("all per row   :", mask.all(axis=1))
print("count per row :", mask.sum(axis=1))
print()
print("np.diff is the inverse of cumsum:")
print("   ", np.diff(np.array([1, 3, 6, 10])))'''),
    ],
    [
        "With no <code>axis</code>, a reduction collapses the whole array to a single value.",
        "<code>axis</code> names the axis that <strong>disappears</strong>. <code>axis=0</code> collapses the rows and gives one value per column.",
        "<code>keepdims=True</code> leaves the reduced axis as length 1, which is what lets the result broadcast back against the original.",
        "A tuple of axes reduces several at once &mdash; <code>axis=(1,2)</code> on a stack gives one value per frame.",
        "<code>argmax</code> on a multi-dimensional array returns a <em>flat</em> position; <code>np.unravel_index</code> turns it into coordinates.",
        "Ties go to the first occurrence, and <code>cumsum</code> keeps the shape rather than reducing it.",
    ],
    '''
title: Aggregations and axis
intro: sum, mean and max - and the one argument that decides what they mean.

## The default collapses everything

`a.sum()` with no arguments adds every element, whatever the shape, and returns a single value.

That value is a NumPy scalar rather than a Python `int` or `float`. It behaves like one almost everywhere; wrap it in `int()` or `float()` when you need a genuine Python number, for JSON or for a format string that cares.

## axis names what disappears

This is the rule, and it is the opposite of how most people read it at first.

`axis=0` does **not** mean "along the rows" in the sense of giving one answer per row. It means *collapse axis 0*. Axis 0 is the row axis, so the rows vanish and you are left with one value per column.

`axis=1` collapses the columns and leaves one value per row.

Reading it as "which axis am I removing?" makes every case predictable, including higher dimensions where intuition runs out. The shape rule is simple: the result has the input shape with that axis deleted.

A useful check when unsure: print `a.shape` and `a.sum(axis=k).shape` and confirm the missing entry is the one you meant.

## keepdims

Reductions drop the axis, and that is usually what you want &mdash; until you try to use the result against the original array.

Row means of a `(3, 4)` array give shape `(3,)`. Subtracting that from the `(3, 4)` array fails, because broadcasting aligns from the right and compares 4 with 3.

`keepdims=True` gives `(3, 1)` instead, which broadcasts down the rows correctly.

Note the asymmetry: centring by **column** needs no `keepdims`, because `mean(axis=0)` gives `(4,)` which already aligns with the last axis. Centring by **row** needs it. That asymmetry is a direct consequence of right-aligned broadcasting, and it is why `keepdims` exists.

A square array hides the error &mdash; both alignments are legal &mdash; so this is worth getting right on principle rather than by testing.

## Several axes at once

`axis` takes a tuple. On a `(frames, rows, cols)` stack, `axis=(1, 2)` reduces each frame to one number, and `axis=0` averages across frames to give one image.

That covers most of what people reach for loops to do with image or batch data.

## argmin and argmax

These return **positions** rather than values.

On a 1-D array the position is an index. On a multi-dimensional array with no `axis`, the position is into the *flattened* array, which is rarely directly useful. `np.unravel_index(a.argmax(), a.shape)` converts it into coordinates.

With an `axis`, you get one position per remaining slice, which is usually what you want: `a.argmax(axis=1)` gives the column of the largest value in each row.

Ties resolve to the **first** occurrence. That matters when the maximum is not unique and something downstream assumes it is.

## Cumulative operations

`cumsum` and `cumprod` are not reductions: they keep the shape and fill in running totals. Without an axis they operate on the flattened array, which is occasionally what you want and often not, so pass `axis` deliberately.

`np.diff` is the inverse of `cumsum` &mdash; consecutive differences, one element shorter.

## Boolean reductions

`any` and `all` take `axis` exactly like `sum`, because a boolean array is numeric and these are just reductions over it.

`mask.any(axis=0)` answers "does any row satisfy this, per column". `mask.sum(axis=1)` counts matches per row. Between them and `argmax`, most "find the first row where..." questions have a one-line answer.

## The common mistakes

**Reading `axis=0` as "per row".** It gives per column. The axis named is the one removed.

**Forgetting `keepdims` when centring by row.** It raises on a rectangular array and silently misbehaves on a square one.

**Using a flat `argmax` as if it were coordinates.** Unravel it.

**Reducing without an axis by accident.** `a.mean()` on a 2-D array gives one number; if you wanted per-column means, the missing argument is the whole bug and the result still looks like a plausible number.

## The accumulator dtype

`a.sum()` on an integer array accumulates in that array's integer type, and that type can overflow.

Summing a million `int32` values each around ten thousand overflows silently and gives a negative answer. The array is fine; the accumulator is not.

`a.sum(dtype=np.int64)` fixes it by accumulating in a wider type than the data. The same argument works on `mean`, `prod` and the rest.

NumPy already does something like this by default for the narrowest types &mdash; summing `int8` accumulates in the platform integer &mdash; but it does not promote `int32` or `int64`, so the risk is real for exactly the widths people actually use.

For floats the concern is different: not overflow but precision loss. Summing many `float32` values accumulates rounding error. `a.sum(dtype=np.float64)` reads the narrow array and accumulates in the wide type, which is the standard compromise between memory and accuracy.

NumPy uses pairwise summation internally rather than a naive running total, so the error grows far more slowly than a hand-written loop would. It is still worth being deliberate when summing millions of `float32` values.

## Weighted means and percentiles

`np.average` is not a synonym for `np.mean`. It takes a `weights` argument, which `mean` does not.

`np.average(x, weights=w)` computes the weighted mean, and `returned=True` also gives back the sum of the weights, which is what you need to combine averages from several groups correctly.

`np.median` is the 50th percentile, and `np.percentile(a, q)` generalises it. Both accept an `axis`, so per-column medians are one call.

Percentiles involve interpolation between the two nearest ranks when the requested quantile does not fall on an element. The `method` argument selects among several conventions, and different statistical packages default differently &mdash; which is the usual explanation when NumPy's answer disagrees slightly with another tool's.

`np.quantile` is the same function taking fractions rather than percentages.

All of these have `nan`-aware variants: `nanmedian`, `nanpercentile`, `nanquantile`.

## reduce and accumulate as the general form

Every reduction has a ufunc underneath, and the ufunc's `reduce` method is the general case.

`np.add.reduce(a, axis=0)` is `a.sum(axis=0)`. `np.maximum.reduce` is `a.max()`. `np.logical_and.reduce` is `a.all()`.

This matters when you want a reduction NumPy does not name. A running maximum has no `cummax` function, but `np.maximum.accumulate(a)` is exactly that, and is the standard way to compute a drawdown baseline or a high-water mark.

`np.ufunc.reduceat` performs segmented reductions &mdash; a reduction over slices defined by a list of start indices &mdash; which is the closest thing NumPy has to a group-by on sorted data.

## Reductions that return more than a number

`np.ptp` gives the peak-to-peak range, `max - min`, in one pass.

`np.histogram` reduces to counts per bin and returns the bin edges alongside them.

`np.bincount` counts occurrences of small non-negative integers, and is substantially faster than `unique(return_counts=True)` for that case because it indexes directly rather than sorting. Its `weights` argument turns it into a group-sum: `np.bincount(group_ids, weights=values)` sums values per group in one call, which is the fastest group-by NumPy offers.

## Empty arrays and the identity element

`np.sum([])` is `0.0`. `np.prod([])` is `1.0`. Both return the identity element for the operation, which is mathematically the right answer.

`np.max([])` raises, because there is no identity for a maximum.

`np.mean([])` returns `nan` with a warning, since it divides by zero.

This matters in code that reduces over groups where some group might be empty. A sum silently gives zero, which may or may not be the meaning you want; a max raises, which at least tells you. Filtering out empty groups before reducing, or using the `initial` argument that `max` and `min` accept, makes the intent explicit.

## The habits worth forming

Pass `axis` explicitly. The default of "reduce everything" is right often enough to hide a missing argument, and wrong often enough to matter.

Pass `keepdims=True` whenever the result will be used against the original array.

Pass `dtype` when summing integers that could be large, or many `float32` values.

Check the shape of the result rather than assuming it. One printed `.shape` resolves most confusion about which axis went where, and it is faster than reasoning about it.

## Reductions on boolean arrays

Because booleans promote to integers, every numeric reduction works on a mask and means something useful.

`mask.sum()` counts. `mask.mean()` gives the proportion &mdash; the fraction of elements satisfying the condition, which is often exactly the summary you want and avoids a division you would otherwise write by hand.

`mask.any()` and `mask.all()` are the logical reductions, and take `axis` like everything else.

`mask.argmax()` finds the first True, since True is 1 and ties go to the first occurrence. It returns 0 when nothing is True, which is indistinguishable from a match at position zero &mdash; check `mask.any()` first.

Combining these covers most "how many rows satisfy" and "which is the first row where" questions in one line each.

## Reductions with a condition

Modern ufunc reductions accept `where`, which restricts the reduction to selected elements without building an intermediate array.

`a.sum(where=mask)` sums only the matching elements. `a.mean(where=mask)` averages them. Compared with `a[mask].sum()`, it avoids allocating the extracted subset, which matters on large arrays inside a loop.

`initial` supplies a starting value, which is what makes `max` work on a possibly-empty selection: `a.max(initial=0, where=mask)` returns 0 rather than raising when nothing matches.

Those two arguments together cover the awkward cases in group-wise reductions, where some groups may be empty and the plain functions either raise or return an identity that means something different.

## Reductions across a stack of arrays

A frequent question is how to reduce over a list of arrays rather than over the axes of one.

The answer is to stack them and reduce along the new axis:

```python
result = np.stack(arrays).mean(axis=0)
```

That is the elementwise mean across all of them. `max(axis=0)` gives the elementwise maximum, and so on.

For two arrays there are direct functions &mdash; `np.maximum(a, b)` and `np.minimum(a, b)` are elementwise and broadcast &mdash; and they are worth distinguishing from `np.max`, which reduces a single array. The names differ by one letter and the operations are entirely different, which is a recurring source of confusion.

`np.maximum.reduce(arrays)` generalises the pairwise version to any number, without the intermediate stack.

## The summary

Pass `axis` explicitly, and read it as "the axis that disappears".

Pass `keepdims=True` whenever the result will be used against the original.

Pass `dtype` when summing many integers or many `float32` values.

Use the `nan*` variants when missing values are possible, and know that they make a decision on your behalf about what missing means.

Use `where` and `initial` for conditional reductions rather than extracting a subset first.

And when the result shape is not what you expected, print `a.shape` and the result's shape together. One comparison resolves nearly every axis confusion faster than reasoning about it does.

## A closing note

Reductions are simple until an axis is involved, and then almost every confusion comes from one place: reading `axis=0` as "along the rows" rather than "collapse the rows".

The axis named is the axis removed. Holding onto that phrasing makes the result shape predictable in any number of dimensions, and turns `keepdims`, tuple axes and higher-dimensional reductions from special cases into consequences of the same rule.
''',
    [
        {"q": "On a (3,4) array, what does `a.sum(axis=0)` give?",
         "options": ["One value per row, shape (3,)", "One value per column, shape (4,)", "A single number", "Shape (3,4)"],
         "answer": 1,
         "why": "axis names the axis that disappears. Axis 0 is the rows, so they collapse and you get one value per column."},
        {"q": "Why does `a - a.mean(axis=1)` fail on a (3,4) array?",
         "options": ["mean returns a scalar", "The result is (3,), and broadcasting compares 4 with 3", "You cannot subtract a mean", "It does not fail"],
         "answer": 1,
         "why": "Right-aligned broadcasting. `keepdims=True` gives (3,1), which stretches correctly - while centring by column needs no keepdims at all."},
        {"q": "What does `argmax` return on a 2-D array with no axis?",
         "options": ["Coordinates", "A flat index into the raveled array", "The maximum value", "One index per row"],
         "answer": 1,
         "why": "Use `np.unravel_index(a.argmax(), a.shape)` to turn it into coordinates. Ties go to the first occurrence."},
        {"q": "What does `axis=(1,2)` do on a (frames, rows, cols) array?",
         "options": ["Nothing", "Collapses rows and columns, giving one value per frame", "Collapses frames", "Raises"],
         "answer": 1,
         "why": "A tuple reduces several axes at once, which covers most of what people reach for loops to do with image or batch data."},
    ],
)


# ---------------------------------------------------------------------------
# 11. Views versus copies
# ---------------------------------------------------------------------------
topic(
    "views_vs_copies",
    "Views versus Copies",
    "Shape and Structure",
    "Which operations give you a second window onto the same numbers - the single "
    "most common source of NumPy surprises.",
    _svg(_box(14, 24, 60, 40, S, A) + _txt(44, 48, "one buffer", A, 8) +
         _arrow(78, 34, 96, 34) + _txt(126, 38, "view", M, 8) +
         _arrow(78, 56, 96, 56) + _txt(126, 60, "copy", M, 8)),
    [
        ("The rule, in one table",
         "Regular strides give a view; scattered selections cannot, so they copy.",
         '''import numpy as np

a = np.arange(12).reshape(3, 4)

cases = [
    ("a[1:3]        slice", a[1:3]),
    ("a[:, 1]       column", a[:, 1]),
    ("a.reshape(4,3) reshape", a.reshape(4, 3)),
    ("a.T           transpose", a.T),
    ("a.ravel()     ravel", a.ravel()),
    ("a[a > 5]      boolean", a[a > 5]),
    ("a[[0, 2]]     fancy", a[[0, 2]]),
    ("a.flatten()   flatten", a.flatten()),
    ("a.copy()      copy", a.copy()),
    ("a.astype(float) astype", a.astype(float)),
]
for label, r in cases:
    print("%-26s %s" % (label, "VIEW" if np.shares_memory(a, r) else "copy"))'''),

        ("Why the line falls there",
         "A view is a start, a shape and a set of strides. Anything describable that "
         "way is free; anything else needs new memory.",
         '''import numpy as np

a = np.arange(12).reshape(3, 4)
print("a.strides     :", a.strides, "bytes to step each axis")
print("a[1:3].strides:", a[1:3].strides, "<- same steps, different start")
print("a[:, 1].strides:", a[:, 1].strides, "<- step a whole row at a time")
print("a.T.strides   :", a.T.strides, "<- the strides simply swapped")
print()
print("Scattered positions have no single step size, so a mask")
print("or an index list cannot be expressed this way - hence a copy.")'''),

        ("How to tell what you are holding",
         "Three ways to check, and the one to reach for by default.",
         '''import numpy as np

a = np.arange(6)
v = a[1:4]
c = a[[1, 2, 3]]

print("np.shares_memory(a, v):", np.shares_memory(a, v))
print("np.shares_memory(a, c):", np.shares_memory(a, c))
print()
print("v.base is a :", v.base is a, " <- a view remembers its source")
print("c.base      :", c.base, "<- a copy owns its data")
print()
print("v.flags.OWNDATA:", v.flags["OWNDATA"])
print("c.flags.OWNDATA:", c.flags["OWNDATA"])
print()
print("shares_memory is the honest check - base can be a chain of views.")'''),

        ("The bug this causes",
         "A function that slices its argument and writes to the slice modifies the "
         "caller's data.",
         '''import numpy as np

def normalise_wrong(data):
    """Looks harmless. Writes through to the caller."""
    body = data[1:]
    body -= body.min()          # in place, on a view
    return data

original = np.array([100.0, 5.0, 9.0, 7.0])
keep = original.copy()
normalise_wrong(original)
print("caller's array before:", keep)
print("caller's array after :", original, "<- changed")

def normalise_right(data):
    out = data.copy()
    out[1:] -= out[1:].min()
    return out

again = keep.copy()
result = normalise_right(again)
print()
print("with a copy, the input survives:", again)
print("and the result is             :", result)'''),

        ("A view can keep a big array alive",
         "The base is referenced by the view, so slicing one row out of a huge array "
         "does not free the rest.",
         '''import numpy as np

big = np.zeros((2000, 500))
print("big  :", "%.1f MB" % (big.nbytes / 1e6))

row_view = big[0]
row_copy = big[0].copy()

print("view :", "%.4f MB of its own" % (row_view.nbytes / 1e6),
      "but base is", "%.1f MB" % (row_view.base.nbytes / 1e6))
print("copy :", "%.4f MB, base:" % (row_copy.nbytes / 1e6), row_copy.base)
print()
print("Holding row_view keeps all 8 MB alive. If you are keeping a small")
print("slice of something large for a long time, copy it deliberately.")'''),

        ("Forcing one or the other",
         "<code>copy()</code> when you need independence; <code>np.may_share_memory</code> "
         "as the cheap guard in library code.",
         '''import numpy as np

a = np.arange(6)

independent = a[1:4].copy()
independent[0] = 99
print("after writing to the copy, a is:", a)

print()
print("a cheap conservative check (may say True when unsure):")
print("   may_share_memory(a, a[1:4]) :", np.may_share_memory(a, a[1:4]))
print("   may_share_memory(a, a.copy()):", np.may_share_memory(a, a.copy()))

print()
print("np.copy and np.array(x, copy=True) do the same job:")
b = np.array(a, copy=True)
b[0] = -1
print("   a:", a, " b:", b)'''),
    ],
    [
        "Slicing, reshaping, transposing and <code>ravel</code> give <strong>views</strong>. Boolean masks, fancy indexing, <code>flatten</code>, <code>copy</code> and <code>astype</code> give <strong>copies</strong>.",
        "A view is a start, a shape and strides. Anything expressible that way is free; scattered positions are not, so they copy.",
        "<code>np.shares_memory(a, b)</code> is the reliable check. <code>.base</code> shows the source, and <code>.flags[\"OWNDATA\"]</code> whether it owns its buffer.",
        "A function that writes into a slice of its argument modifies the caller's array. Copy at the boundary if you did not mean to.",
        "A view keeps its base alive, so a small slice of a large array can hold all of it in memory.",
        "<code>ravel</code> gives a view where it can and <code>flatten</code> always copies &mdash; the same distinction, packaged as two functions.",
    ],
    '''
title: Views versus Copies
intro: Which operations give you a second window onto the same numbers, and why it matters.

## One buffer, several descriptions

An array is a block of memory plus a description: where it starts, what shape it has, and how many bytes to step for each axis. Those steps are the **strides**.

A **view** is a new description of the same block. Making one is free, and writing through it changes what every other description of that block sees.

A **copy** is a new block. It costs time and memory, and it is independent.

Nearly every surprise in NumPy that is not about broadcasting is about this distinction.

## Where the line falls

**Views**: basic slicing, `reshape` (usually), `.T` and other transposes, `ravel` (usually), `np.newaxis`, and `view()`.

**Copies**: boolean masking, fancy indexing, `flatten`, `copy`, `astype`, and most functions that return a new array.

The rule underneath is mechanical. If the selected elements can be described by a start and a regular stride per axis, a view works. A slice steps evenly, so it can. A boolean mask picks scattered positions with no single step size, so it cannot.

That is why the list is not arbitrary and does not need memorising once you have the reason.

Two entries carry an "usually". `reshape` returns a view when the result can be strided over the existing layout, and copies when it cannot &mdash; typically after a transpose. `ravel` is the same. Neither tells you which happened, which is why the check below matters.

## Checking

`np.shares_memory(a, b)` is the honest answer, and the one to use.

`b.base` points at the array a view derives from, or `None` for a copy. It is informative but can be a chain &mdash; a view of a view has a base that is itself a view &mdash; so it is not a reliable equality test.

`b.flags["OWNDATA"]` says whether the array owns its buffer.

`np.may_share_memory` is a cheap conservative check: it can say True when it is merely unsure. That makes it right for a fast guard in library code and wrong for a definite answer.

## The bug

The practical consequence is a function that modifies its caller's data without saying so.

```python
def normalise(data):
    body = data[1:]
    body -= body.min()     # in place, on a view of the caller's array
    return data
```

`data[1:]` is a view. `-=` writes in place. The caller's array is now different, and nothing in the signature suggested it would be.

This is easy to write by accident, because each step looks innocent, and hard to spot in review. Two defences:

**Copy at the boundary** when a function should not modify its input. `data = data.copy()` at the top is cheap insurance for small arrays and a deliberate decision for large ones.

**Say so in the name** when a function does modify in place. NumPy's own convention is that in-place variants are explicit &mdash; `np.sort` returns a sorted copy, `a.sort()` sorts in place.

## Memory: a view keeps its base alive

A view holds a reference to the array it came from, so the whole buffer stays in memory as long as any view of it exists.

Slice one row out of an 8 MB array and keep it: you are keeping 8 MB, not 4 KB.

That matters when you are extracting a small piece of something large to hold on to &mdash; a filtered subset, a header, one channel. `copy()` releases the rest. It is exactly the same shape of problem as holding a slice of a huge Python string, and it shows up in long-running processes as memory that never comes back.

## When to copy deliberately

**Crossing an API boundary** where the caller should not see your modifications, or you should not see theirs.

**Keeping something small from something large**, so the large thing can be freed.

**Before an in-place loop** over data you did not create.

**When you want a guarantee** rather than the "usually a view" behaviour of `reshape` and `ravel`.

Everywhere else, views are the point. They are why slicing a gigabyte array costs nothing and why NumPy code can pass windows around freely. The goal is not to avoid them but to know which one you are holding.

## The two "usually" cases

Two operations in the view column carry a qualifier, and both are worth understanding rather than memorising.

`reshape` returns a view when the new shape can be walked with a regular stride over the existing memory. On a freshly created contiguous array, that is always. After a transpose, it usually is not &mdash; the buffer is being read column-first, and flattening it row-first requires gathering scattered values.

`ravel` is the same. `flatten` is the version that always copies, and its existence is really just a way of asking for the guarantee.

If you need the opposite guarantee &mdash; a view or an error, never a silent copy &mdash; assign to `.shape` directly. `a.shape = (3, 4)` raises if a view is impossible, which turns an invisible performance problem into a visible failure.

## copy is shallow, in the way that matters

`a.copy()` duplicates the buffer, and for a numeric array that is a complete, independent copy.

For an **object** array it is not. The new array has its own array of pointers, but those pointers lead to the same Python objects. Modifying one of those objects is visible through both arrays.

`copy.deepcopy(a)` from the standard library duplicates the objects too.

This only arises with `dtype=object`, which is uncommon and generally worth avoiding, but the failure is confusing when it happens because `copy()` did exactly what its name suggests at the level it operates on.

## In-place operations on a fancy index

There is a subtle failure that is worth knowing before it costs you an afternoon.

```python
a[[0, 0, 1]] += 1
```

You might expect element 0 to be incremented twice. It is incremented **once**.

The reason is that this expands to a fetch, an add, and a store: `a[idx] = a[idx] + 1`. The fetch produces a copy containing element 0 twice, both copies get 1 added, and then both are written back to the same place &mdash; the second overwriting the first.

`np.add.at(a, [0, 0, 1], 1)` is the unbuffered version that does what the syntax suggests, incrementing element 0 twice. Every ufunc has an `.at` method for this.

This matters in any histogram-like accumulation where indices repeat, and the wrong version produces plausible undercounts rather than an error.

## Tracking down a mutation bug

The symptom is always the same: an array changed and nothing in the visible code changed it.

The diagnosis is mechanical.

**Find every place the array was derived from something else.** A slice, a reshape, a transpose, a `ravel` &mdash; each is a candidate.

**Check with `np.shares_memory`.** Between the array that changed and every candidate source. This is definitive.

**Look for in-place operators on the shared side.** `+=`, `-=`, `*=`, `sort()`, `fill()`, and assignment into a slice. Anything that modifies rather than rebinding.

**Check function boundaries.** A function that takes an array and slices it is the most common origin, because the mutation is one level away from where you are looking.

The fix is nearly always a `copy()` at the boundary, and the question of *which* boundary is answered by deciding who owns the data.

## An ownership convention

Most of these problems disappear under a simple rule, applied consistently:

**A function does not modify its arguments unless its name says so.**

NumPy follows this itself. `np.sort` returns a sorted copy; `a.sort()` sorts in place. `np.append` returns a new array. The function forms are safe, the method forms are not, and the distinction is reliable enough to lean on.

For your own code, that means copying at the top of any function that will modify what it was given &mdash; or, better, not modifying it at all and returning a new array.

The exception is a deliberate in-place API for large data, where copying would defeat the purpose. Those functions should say so in the name, take the output array explicitly, or both. `out=` is NumPy's own answer to this, and it is a good pattern to copy: the caller supplies the destination, so nobody is surprised about what gets written.

## When views are the point

None of this is an argument against views. They are the reason NumPy can pass windows of large arrays around for free, and the reason slicing a gigabyte array costs nothing.

The goal is not to copy defensively everywhere &mdash; that would discard the main benefit &mdash; but to know which one you are holding at the moments it matters: across a function boundary, before an in-place loop, and when keeping something small from something large.

## A quick reference

**Always a view**: basic slicing, `a[::k]`, `a[::-1]`, `.T`, `transpose`, `swapaxes`, `moveaxis`, `a[None]`, `expand_dims`, `squeeze`, `view()`.

**Usually a view**: `reshape`, `ravel`. Both fall back to copying when the requested layout cannot be strided over the existing memory &mdash; typically after a transpose.

**Always a copy**: boolean masking, fancy indexing, `flatten`, `copy`, `astype`, `np.array(x)` by default, and essentially every function returning a computed result.

**Neither**: in-place operations, which return nothing and modify the buffer.

The underlying rule makes the list predictable: if the selection can be described by a start, a shape and a stride per axis, it is a view. If the positions are scattered, it cannot be, so it copies.

## Why `astype` always copies

Even `a.astype(np.float64)` on an array that is already `float64` returns a copy by default. That surprises people who expect it to be a no-op.

`astype(dtype, copy=False)` returns the original when no conversion is needed. That is the form to use in a function that normalises its input, where copying every call is waste.

The default of copying is defensive: `astype` is usually called to produce something the caller will modify, and returning a shared array would make that dangerous.

## Checking, once more

`np.shares_memory(a, b)` &mdash; definitive, and the one to use.

`np.may_share_memory(a, b)` &mdash; conservative and cheap; can say True when unsure. Right for a guard, wrong for an answer.

`a.base` &mdash; the array a view derives from, or None. Informative, but a view of a view has a base that is itself a view, so it is not an equality test.

`a.flags["OWNDATA"]` &mdash; whether the array owns its buffer.

`a.flags` in full also reports contiguity, which is what determines whether the next `reshape` or `ravel` will copy.

## The habits that prevent the bugs

**Copy at the boundary** of any function that will modify what it was given, unless the name says otherwise.

**Follow NumPy's own convention**: functions return new arrays, methods modify in place. `np.sort` versus `a.sort()`. Making your own code follow the same rule means callers can predict it without reading the body.

**Copy deliberately when keeping something small from something large**, so the base can be freed.

**Check with `shares_memory`** whenever a mutation appears from nowhere. It is the fastest route from symptom to cause, and it gives a definite answer where reasoning about which operations copy gives a probable one.

None of this argues against views. They are why slicing a gigabyte array is free and why array code can pass windows around without thought. The goal is to know which one you are holding at the three moments it matters: across a function boundary, before modifying in place, and when keeping a fragment of something large.
''',
    [
        {"q": "Which of these returns a copy rather than a view?",
         "options": ["a[1:3]", "a.T", "a[a > 5]", "a.reshape(4,3)"],
         "answer": 2,
         "why": "A boolean mask selects scattered positions with no single step size, so no stride description can express it. Slicing, transposing and reshaping all can."},
        {"q": "What is the reliable way to check whether two arrays share memory?",
         "options": [".base is a", "np.shares_memory(a, b)", ".flags", "np.may_share_memory"],
         "answer": 1,
         "why": "`.base` can be a chain of views, and `may_share_memory` is conservative - it may say True when unsure. `shares_memory` gives the definite answer."},
        {"q": "A function does `body = data[1:]` then `body -= body.min()`. What happens to the caller's array?",
         "options": ["Nothing", "It is modified, because the slice is a view and -= writes in place", "It raises", "It is copied first"],
         "answer": 1,
         "why": "Each step looks innocent and the combination silently mutates the input. Copy at the boundary, or make the in-place behaviour explicit in the name."},
        {"q": "Why can holding a one-row view of a large array waste memory?",
         "options": ["Views are large", "A view keeps a reference to its base, so the whole buffer stays alive", "Views are slower", "It does not"],
         "answer": 1,
         "why": "Slicing one row from an 8 MB array and keeping it keeps all 8 MB. `.copy()` releases the rest - the same problem as holding a slice of a huge string."},
    ],
)


# ---------------------------------------------------------------------------
# 12. Stacking and splitting
# ---------------------------------------------------------------------------
topic(
    "stacking_and_splitting",
    "Stacking and Splitting",
    "Shape and Structure",
    "Joining arrays along an existing axis or a new one - and why the two are "
    "different functions.",
    _svg(_grid(18, 30, 3, 2, 13) + _grid(70, 30, 3, 2, 13) +
         _txt(57, 42, "+", A, 11) +
         _arrow(112, 43, 126, 43) + _txt(140, 47, "?", A, 11)),
    [
        ("concatenate joins along an existing axis",
         "The arrays must already agree on every other axis. Nothing new is created.",
         '''import numpy as np

a = np.arange(6).reshape(2, 3)
b = np.arange(6, 12).reshape(2, 3)

print("a:"); print(a)
print("b:"); print(b)
print()
print("concatenate axis=0 ->", np.concatenate([a, b], axis=0).shape)
print(np.concatenate([a, b], axis=0))
print()
print("concatenate axis=1 ->", np.concatenate([a, b], axis=1).shape)
print(np.concatenate([a, b], axis=1))'''),

        ("stack creates a NEW axis",
         "That is the whole difference. Same inputs, one more dimension out.",
         '''import numpy as np

a = np.arange(6).reshape(2, 3)
b = np.arange(6, 12).reshape(2, 3)

print("concatenate ->", np.concatenate([a, b]).shape, "(4, 3): rows appended")
print("stack       ->", np.stack([a, b]).shape, "(2, 2, 3): a new first axis")
print()
print("stack(axis=0) is a pile of frames:")
s = np.stack([a, b])
print("   s[0] is a:", np.array_equal(s[0], a))
print()
print("and the new axis can go anywhere:")
for ax in [0, 1, 2]:
    print("   stack(axis=%d) ->" % ax, np.stack([a, b], axis=ax).shape)'''),

        ("vstack, hstack and the 1-D surprise",
         "Convenient names, and a special case for 1-D input that catches people.",
         '''import numpy as np

a2 = np.arange(6).reshape(2, 3)
b2 = np.arange(6, 12).reshape(2, 3)
print("2-D: vstack ->", np.vstack([a2, b2]).shape,
      " hstack ->", np.hstack([a2, b2]).shape)

a1 = np.array([1, 2, 3])
b1 = np.array([4, 5, 6])
print()
print("1-D is where they differ from each other:")
print("   vstack ->", np.vstack([a1, b1]).shape, "<- promoted to rows")
print(np.vstack([a1, b1]))
print("   hstack ->", np.hstack([a1, b1]).shape, "<- just joined end to end")
print("   ", np.hstack([a1, b1]))
print()
print("column_stack makes them columns, which is usually what you wanted:")
print(np.column_stack([a1, b1]))'''),

        ("Shapes must line up",
         "The error names the axis that disagrees, which is usually enough to find "
         "the problem.",
         '''import numpy as np

a = np.ones((2, 3))
b = np.ones((3, 3))
c = np.ones((2, 4))

print("(2,3) + (3,3) on axis=0 ->", np.concatenate([a, b], axis=0).shape, "ok")
try:
    np.concatenate([a, b], axis=1)
except ValueError as e:
    print("(2,3) + (3,3) on axis=1 -> ValueError")
    print("   ", str(e)[:96])
print()
print("(2,3) + (2,4) on axis=1 ->", np.concatenate([a, c], axis=1).shape, "ok")
print()
print("stack is stricter - every array must have the SAME shape:")
try:
    np.stack([a, c])
except ValueError as e:
    print("   stack((2,3),(2,4)) ->", str(e)[:60])'''),

        ("Splitting is the inverse",
         "<code>split</code> needs equal parts; <code>array_split</code> does not.",
         '''import numpy as np

a = np.arange(12).reshape(4, 3)
print(a)

top, bottom = np.split(a, 2, axis=0)
print()
print("split into 2 rows-wise:", top.shape, bottom.shape)

print()
print("split at given positions instead of into n parts:")
parts = np.split(np.arange(10), [3, 7])
print("   ", [list(p) for p in parts])

print()
try:
    np.split(np.arange(10), 3)
except ValueError as e:
    print("split(10, 3) ->", type(e).__name__, "- 10 is not divisible by 3")
print("array_split(10, 3) ->", [len(p) for p in np.array_split(np.arange(10), 3)])'''),

        ("Building in a loop is still wrong",
         "Concatenating repeatedly is quadratic for the same reason appending is. "
         "Collect, then join once.",
         '''import numpy as np
import time

rows = [np.arange(50) for _ in range(400)]

t = time.perf_counter()
acc = np.empty((0, 50))
for r in rows:
    acc = np.concatenate([acc, r.reshape(1, -1)])
grow = time.perf_counter() - t

t = time.perf_counter()
once = np.stack(rows)
single = time.perf_counter() - t

print("concatenate in a loop : %.4f s" % grow)
print("stack once at the end : %.4f s" % single)
print("ratio                 : %.0fx" % (grow / single))
print("same result           :", np.array_equal(acc, once))
print()
print("Every concatenate allocates a new array and copies everything so far.")'''),
    ],
    [
        "<code>concatenate</code> joins along an <strong>existing</strong> axis; <code>stack</code> creates a <strong>new</strong> one.",
        "For <code>concatenate</code>, every axis except the joining one must match. For <code>stack</code>, the shapes must be identical.",
        "<code>vstack</code> and <code>hstack</code> are conveniences. On 1-D input they differ sharply: <code>vstack</code> makes rows, <code>hstack</code> joins end to end.",
        "<code>column_stack</code> turns 1-D arrays into columns, which is usually what people reach for <code>hstack</code> hoping to get.",
        "<code>split</code> requires equal parts and raises otherwise; <code>array_split</code> allows uneven ones.",
        "Never concatenate in a loop &mdash; each call copies everything so far. Collect into a list and <code>stack</code> once.",
    ],
    '''
title: Stacking and Splitting
intro: Joining along an existing axis or a new one, and why those are different functions.

## Two different questions

You have several arrays and want one. There are two distinct things that could mean, and NumPy gives them separate functions rather than guessing.

**`concatenate`** joins along an axis that already exists. Two `(2, 3)` arrays concatenated on axis 0 give `(4, 3)` &mdash; more rows, same number of dimensions.

**`stack`** creates a new axis. The same two arrays stacked give `(2, 2, 3)` &mdash; a pile of two frames, one dimension more than the inputs.

Asking which you want is the first step, and the answer is usually obvious once phrased that way: appending records is concatenation; collecting frames or samples into a batch is stacking.

## What must match

`concatenate` requires every axis **except the joining one** to agree. Joining on axis 0 needs matching column counts; joining on axis 1 needs matching row counts.

`stack` is stricter: all inputs must have exactly the same shape, since they are becoming parallel slices of a new axis.

The error messages name the mismatch, and reading them rather than guessing usually locates the problem immediately.

## The convenience functions

`vstack` stacks vertically, `hstack` horizontally, `dstack` along the third axis. For 2-D input they are just `concatenate` with a fixed axis.

For **1-D input they diverge**, and this is where they cause trouble.

`np.vstack([a, b])` on two length-3 arrays gives `(2, 3)` &mdash; it promotes each to a row.

`np.hstack([a, b])` gives `(6,)` &mdash; it joins them end to end, because axis 1 does not exist so it falls back to axis 0.

People reaching for `hstack` to make two columns get one long array instead. `column_stack` is the function that does what they meant: it turns 1-D arrays into columns of a 2-D result.

The general advice: use `concatenate` or `stack` with an explicit `axis` when the dimensionality might vary. The convenience names are fine when you know exactly what shapes you have.

## Splitting

`np.split(a, n, axis=0)` divides into `n` equal parts and **raises** if the length does not divide exactly. That strictness is useful &mdash; an uneven split is usually a sign that something upstream is not the size you assumed.

`np.array_split` allows uneven parts, distributing the remainder across the first few. Use it when uneven is genuinely acceptable, such as chunking work for parallel processing.

`split` also accepts a list of positions rather than a count: `np.split(a, [3, 7])` cuts before index 3 and before index 7, giving three pieces. That is often more natural than computing a count.

The pieces are **views**, not copies, which is worth knowing: splitting a large array is free, and writing into a piece writes into the original.

## Do not build in a loop

The same rule as `np.append`, for the same reason.

Concatenating inside a loop allocates a new array and copies everything accumulated so far, on every iteration. That is quadratic, and the last editor measures the difference.

Collect into a Python **list** and call `stack` or `concatenate` once at the end. Lists append cheaply; arrays do not append at all.

If you know the final size in advance, better still: allocate with `np.empty` and assign into slices. That avoids even the single large copy.

## Choosing

Appending records of the same width: `concatenate(axis=0)`.

Adding columns to a table: `concatenate(axis=1)`, or `column_stack` for 1-D inputs.

Collecting frames, samples or channels into a batch: `stack`, with an explicit axis.

Undoing any of those: `split` when the division is exact, `array_split` when it is not.

And in every case, if the joining is happening inside a loop, the answer is to move it outside.

## r_ and c_

`np.r_` and `np.c_` are index-expression shortcuts, and they look strange because they use square brackets rather than parentheses.

`np.r_[a, b]` concatenates along the first axis. `np.c_[a, b]` stacks as columns, equivalent to `column_stack`.

They also accept slice syntax, so `np.r_[0:5, 10, 20:23]` builds an array from a mix of ranges and literals in one expression. That is genuinely convenient for constructing index arrays and test data.

They are compact rather than clear, and they show up more in older code and in interactive sessions than in libraries. Worth recognising; not worth preferring over the named functions in code others will read.

## tile and repeat

Both make an array bigger by duplication, and they differ in a way that is easy to state and easy to forget.

`np.tile(a, n)` repeats the whole array n times: `[1, 2]` becomes `[1, 2, 1, 2]`.

`np.repeat(a, n)` repeats each element n times: `[1, 2]` becomes `[1, 1, 2, 2]`.

`tile` accepts a tuple to repeat along several axes, which is how you build a checkerboard or replicate a small pattern across a grid.

`repeat` accepts an `axis` and a per-element count, so `np.repeat(rows, counts, axis=0)` expands a table according to a count column &mdash; the standard way to turn aggregated data back into one row per observation.

Neither is a substitute for broadcasting. If you are tiling an array purely so that its shape matches another one for an arithmetic operation, broadcasting will do it without allocating anything, and the tile is wasted memory.

## Padding

`np.pad(a, width, mode)` adds elements around the edges.

`width` can be a single number, a pair for before and after, or a pair per axis. The nesting gets confusing quickly, and it is worth checking the result's shape the first time on any new call.

The `mode` argument covers the cases that would otherwise be fiddly: `"constant"` with a `constant_values` argument, `"edge"` to repeat the border, `"reflect"` and `"symmetric"` to mirror, and `"wrap"` to tile.

This is how you implement boundary conditions for a convolution or a stencil without writing an index-clamping branch, and it is one of the functions that quietly removes a lot of code.

## block, for nested assembly

`np.block` builds an array from a nested list of arrays, laid out the way the nesting reads.

```python
np.block([[A, B],
          [C, D]])
```

produces the block matrix, provided the pieces have compatible shapes. It is far clearer than the equivalent chain of `hstack` inside `vstack`, and it is the right tool for assembling a matrix from named submatrices &mdash; a covariance built from blocks, a system of equations assembled from parts.

## Choosing among the joins

The functions overlap enough to be worth a summary.

**`concatenate`** &mdash; the general form. Explicit axis, works on any dimensionality, no surprises. Reach for this when the dimensionality might vary or when clarity matters.

**`stack`** &mdash; when a new axis is what you want. Collecting frames, samples or repeated runs into a batch.

**`vstack` / `hstack` / `dstack`** &mdash; conveniences with a fixed axis. Safe on 2-D, and divergent on 1-D in a way that catches people. Fine when you know the shapes exactly.

**`column_stack`** &mdash; turns 1-D arrays into columns, which is what people usually want from `hstack` and do not get.

**`block`** &mdash; nested assembly from named pieces.

**`r_` / `c_`** &mdash; terse, for interactive use.

And the rule that applies to all of them: none belongs inside a loop. Collect into a list, join once.

## Splitting, in practice

The pieces returned by `split` are **views**, so splitting a large array is free and writing into a piece writes into the original. That is usually convenient and occasionally surprising, and it follows the same rules as any other slice.

`array_split` distributes an uneven remainder across the first pieces, so splitting 10 into 3 gives lengths 4, 3, 3. That is deterministic, which matters if two processes split the same data independently and must agree.

For chunking work rather than dividing it evenly, computing the boundaries yourself and passing them as a list is often clearer than asking for a count &mdash; `np.split(a, range(0, len(a), chunk))` cuts at fixed intervals regardless of whether the total divides evenly.

## Joining arrays of different dtypes

Concatenating an integer array with a float array gives a float result, following the same promotion rules as arithmetic.

That is usually what you want, and occasionally not. Joining an `int64` array of identifiers with a `float64` array of measurements produces a float array in which large identifiers may no longer be exactly representable.

`dtype=` on `concatenate` forces the result type explicitly, and `casting="no"` makes a mismatch an error rather than a silent promotion. In code where the dtype matters, being explicit costs one argument and removes a whole category of surprise.

Joining a fixed-width string array with a longer one widens to fit, which is the one place NumPy strings do the accommodating thing rather than truncating.

## Building an output array up front

When the final size is known, neither joining nor appending is necessary.

```python
out = np.empty((n_rows, n_cols))
for i, row in enumerate(source):
    out[i] = compute(row)
```

One allocation, no copying, and the slices being assigned into are views. This is the fastest form when a loop is unavoidable, and it is clearer than accumulating pieces to join later.

`np.empty` is right here because every element is written. If some rows might be skipped, `np.zeros` or `np.full(shape, np.nan)` makes the unfilled entries visible rather than leaving whatever was in memory.

Preallocating also forces you to state the output shape, which frequently surfaces an error in the reasoning before any code runs.

## Splitting for parallel work

`np.array_split(a, n)` is the natural way to divide data among n workers. It handles the case where the length does not divide evenly, distributing the remainder across the first pieces deterministically.

Because the pieces are views, splitting costs nothing &mdash; but views cannot cross a process boundary, so multiprocessing will copy them anyway when pickling. For thread-based parallelism the views are shared directly, which is one of the reasons threads are attractive for NumPy work.

For chunking rather than dividing &mdash; fixed-size pieces, however many that turns out to be &mdash; passing explicit boundaries is clearer:

```python
np.split(a, range(chunk, len(a), chunk))
```

That cuts every `chunk` elements and leaves a shorter final piece, which is usually what "process in batches of 1000" means.

## The summary

**Joining along an existing axis**: `concatenate`, with an explicit `axis`.

**Adding a new axis**: `stack`, with an explicit `axis`.

**1-D arrays into columns**: `column_stack`, not `hstack`.

**Assembling from named blocks**: `block`.

**Duplicating**: `tile` for the whole array, `repeat` for each element &mdash; and neither if broadcasting would do the job without allocating.

**Adding borders**: `pad`, with the mode chosen for the boundary condition.

**Dividing**: `split` for exact division, `array_split` for uneven, explicit boundaries for fixed-size chunks.

And the rule that overrides all of them: none of these belongs inside a loop that runs once per element. Collect into a Python list and join once, or preallocate and assign into slices.

## A closing note

Joining arrays is one of the places where NumPy offers several functions for what feels like one job, and the abundance is more confusing than helpful at first.

The way through it is the question at the top of this module: does the result have the same number of dimensions as the inputs, or one more? Everything else is a convenience wrapper over that decision, and `concatenate` and `stack` with an explicit `axis` will do any of it correctly if you would rather not remember the rest.
''',
    [
        {"q": "What is the difference between `concatenate` and `stack`?",
         "options": ["None", "concatenate joins along an existing axis; stack creates a new one", "stack is faster", "concatenate only works on 1-D"],
         "answer": 1,
         "why": "Two (2,3) arrays give (4,3) concatenated and (2,2,3) stacked. Appending records is concatenation; collecting frames into a batch is stacking."},
        {"q": "What does `np.hstack` do with two 1-D arrays of length 3?",
         "options": ["Gives (2,3)", "Gives (3,2)", "Gives (6,) - joined end to end", "Raises"],
         "answer": 2,
         "why": "Axis 1 does not exist for 1-D, so it falls back to axis 0. `column_stack` is the function that makes them columns."},
        {"q": "How does `split` differ from `array_split`?",
         "options": ["No difference", "split requires equal parts and raises otherwise", "array_split is faster", "split works on 2-D only"],
         "answer": 1,
         "why": "That strictness is useful - an uneven split usually means something upstream is not the size you assumed."},
        {"q": "Why not concatenate inside a loop?",
         "options": ["It is deprecated", "Each call allocates a new array and copies everything so far, making it quadratic", "It changes dtype", "It only works twice"],
         "answer": 1,
         "why": "Collect into a Python list and stack once at the end - or allocate with np.empty and assign into slices if you know the size."},
    ],
)


# ---------------------------------------------------------------------------
# 13. Transpose and moving axes
# ---------------------------------------------------------------------------
topic(
    "transpose_and_axes",
    "Transpose and Moving Axes",
    "Shape and Structure",
    "Reordering axes without moving a single byte - and the one case where .T "
    "silently does nothing.",
    _svg(_grid(24, 26, 4, 2, 14) +
         _arrow(90, 44, 108, 44) +
         _grid(122, 20, 2, 4, 14)),
    [
        (".T reverses the axes",
         "It is a view: the strides swap and the data never moves.",
         '''import numpy as np

a = np.arange(6).reshape(2, 3)
print("a", a.shape); print(a)
print()
print("a.T", a.T.shape); print(a.T)
print()
print("strides a   :", a.strides)
print("strides a.T :", a.T.strides, "<- the same numbers, swapped")
print("shares memory:", np.shares_memory(a, a.T))
print()
print("Transposing a 1 GB array costs nothing. No byte is copied.")'''),

        ("The 1-D trap",
         "<code>.T</code> on a 1-D array is a no-op. This surprises everyone once.",
         '''import numpy as np

v = np.array([1, 2, 3])
print("v      :", v.shape)
print("v.T    :", v.T.shape, "<- unchanged. There is no second axis to swap.")
print()
print("To get a column, add an axis:")
print("   v[:, None]        ->", v[:, None].shape)
print("   v.reshape(-1, 1)  ->", v.reshape(-1, 1).shape)
print(v[:, None])
print()
print("This is why a 'row minus column' outer operation needs None,")
print("not .T:")
print(v[:, None] - v)'''),

        ("transpose with an explicit order",
         "On more than two axes, <code>.T</code> reverses all of them - which is "
         "rarely what you want. Name the order instead.",
         '''import numpy as np

a = np.arange(24).reshape(2, 3, 4)
print("a       :", a.shape)
print("a.T     :", a.T.shape, "<- fully reversed")
print()
print("transpose names the NEW order in terms of the old positions:")
print("   transpose(1, 0, 2) ->", a.transpose(1, 0, 2).shape)
print("   transpose(0, 2, 1) ->", a.transpose(0, 2, 1).shape)
print("   transpose(2, 0, 1) ->", a.transpose(2, 0, 1).shape)
print()
print("Read (2,0,1) as: old axis 2 first, then old axis 0, then old axis 1.")'''),

        ("swapaxes and moveaxis read better",
         "Two axes to exchange, or one axis to relocate - both clearer than counting "
         "positions.",
         '''import numpy as np

a = np.arange(24).reshape(2, 3, 4)

print("swapaxes(0, 2) ->", np.swapaxes(a, 0, 2).shape, "exchange two axes")
print("moveaxis(a, 0, -1) ->", np.moveaxis(a, 0, -1).shape, "send axis 0 to the end")
print("moveaxis(a, -1, 0) ->", np.moveaxis(a, -1, 0).shape, "bring the last to front")
print()
print("The classic use: images stored (channels, h, w) vs (h, w, channels)")
img = np.zeros((3, 64, 48))
print("   CHW", img.shape, "-> HWC", np.moveaxis(img, 0, -1).shape)
print()
print("all of these are views:", np.shares_memory(a, np.moveaxis(a, 0, -1)))'''),

        ("Transposing makes the memory non-contiguous",
         "Which is fine, until something needs a contiguous buffer and quietly copies.",
         '''import numpy as np

a = np.arange(12).reshape(3, 4)
t = a.T

print("a is C-contiguous:", a.flags["C_CONTIGUOUS"])
print("t is C-contiguous:", t.flags["C_CONTIGUOUS"],
      " F-contiguous:", t.flags["F_CONTIGUOUS"])
print()
print("ravel on a view that is not contiguous must copy:")
print("   shares memory with a:", np.shares_memory(a, t.ravel()))
print()
print("reshape can fail to be a view for the same reason:")
r = t.reshape(-1)
print("   t.reshape(-1) shares memory:", np.shares_memory(a, r))
print()
print("ascontiguousarray makes the copy explicit when you want it:")
c = np.ascontiguousarray(t)
print("   c is C-contiguous:", c.flags["C_CONTIGUOUS"])'''),

        ("Transpose is not a rotation",
         "It reflects along the diagonal. If you wanted to turn an image, "
         "<code>rot90</code> is the function.",
         '''import numpy as np

a = np.array([[1, 2],
              [3, 4]])
print("original:"); print(a)
print()
print("a.T (reflected along the diagonal):"); print(a.T)
print()
print("np.rot90(a) (turned a quarter turn anticlockwise):"); print(np.rot90(a))
print()
print("np.flipud / np.fliplr mirror instead:")
print("   flipud:", np.flipud(a).tolist())
print("   fliplr:", np.fliplr(a).tolist())
print()
print("rot90 twice == flipping both ways:",
      np.array_equal(np.rot90(a, 2), np.flipud(np.fliplr(a))))'''),
    ],
    [
        "<code>.T</code> reverses the axes by swapping strides. No data moves, so transposing a huge array is free.",
        "<code>.T</code> on a <strong>1-D</strong> array does nothing. Use <code>v[:, None]</code> to get a column.",
        "On three or more axes <code>.T</code> reverses <em>all</em> of them. Use <code>transpose(...)</code> with an explicit order instead.",
        "<code>swapaxes</code> exchanges two axes and <code>moveaxis</code> relocates one &mdash; both read better than counting positions.",
        "A transposed array is no longer C-contiguous, so <code>ravel</code> and some <code>reshape</code> calls will quietly copy.",
        "Transpose reflects along the diagonal; it is not a rotation. <code>rot90</code>, <code>flipud</code> and <code>fliplr</code> are the geometric operations.",
    ],
    '''
title: Transpose and Moving Axes
intro: Reordering axes without moving a single byte.

## Strides again

An array knows how many bytes to step for each axis. Transposing swaps those numbers along with the shape, and the underlying buffer is untouched.

That is why `a.T` on a gigabyte array returns instantly. It is a view, and `np.shares_memory(a, a.T)` confirms it.

Everything else in this module follows from that one fact.

## The 1-D trap

`v.T` where `v` has shape `(3,)` gives shape `(3,)`. Nothing happens.

There is no second axis to swap, so the operation is meaningless and NumPy performs it silently rather than raising. People coming from MATLAB or from linear algebra notation expect a column vector and get their input back.

The fix is to add an axis: `v[:, None]` gives `(3, 1)`, and `v[None, :]` gives `(1, 3)`. `reshape(-1, 1)` does the same job.

This is also why an outer-style operation is written `v[:, None] - v` rather than `v.T - v`. The first broadcasts `(3,1)` against `(3,)` to give `(3,3)`; the second subtracts an array from itself and gives zeros.

## More than two axes

`.T` reverses **all** axes. On shape `(2, 3, 4)` it gives `(4, 3, 2)`.

That is well defined but rarely what anyone wants, because with three or more axes the interesting operation is usually moving one specific axis somewhere.

`a.transpose(2, 0, 1)` names the new order in terms of old positions: old axis 2 first, then old axis 0, then old axis 1. Reading it in that direction &mdash; "where does each new axis come from" &mdash; is the way to keep it straight.

## swapaxes and moveaxis

Both are clearer than counting.

`np.swapaxes(a, 0, 2)` exchanges two axes and leaves the rest alone.

`np.moveaxis(a, 0, -1)` takes axis 0 and puts it at the end, sliding the others along. This is the canonical fix for image layout: deep learning frameworks want `(channels, height, width)`, image libraries want `(height, width, channels)`, and `moveaxis` converts between them for free.

Both return views.

## Contiguity, and the copy you did not ask for

An array created by `reshape` on fresh data is **C-contiguous**: the last axis varies fastest and the elements sit in memory in the order you would read them.

Transposing breaks that. The transposed view is F-contiguous instead &mdash; the same buffer, read column-first.

Most operations do not care. But anything that needs a flat contiguous buffer must copy:

`ravel()` returns a view when it can and a copy when it cannot. On a transposed array, it cannot.

`reshape` has the same behaviour, which is why "reshape returns a view" carries a *usually*.

Neither warns you. If it matters &mdash; because the array is large, or because you were relying on writing through the result &mdash; check with `np.shares_memory`, or force the issue with `np.ascontiguousarray` so the copy is explicit and happens where you can see it.

## Transpose is not rotation

This trips people up on image data.

Transpose reflects along the main diagonal. Rotating a quarter turn is `np.rot90`. Mirroring is `np.flipud` (up-down) and `np.fliplr` (left-right).

They are related &mdash; a rotation is a transpose followed by a flip &mdash; but they are different operations, and reaching for `.T` to turn an image gives a mirrored result that looks almost right and is not.

## In practice

Use `.T` freely on 2-D. Use `moveaxis` or `swapaxes` on anything higher, because they say what you meant. Remember that a 1-D transpose is a no-op, and that the result of any of them is a view over the same bytes &mdash; which is the entire point, and also the reason contiguity assumptions later in the pipeline can quietly cost you a copy.

## C order and F order, stated plainly

An array's elements are stored in one flat run of memory. The **order** decides which axis varies fastest as you walk that run.

C order &mdash; NumPy's default, named for the C language &mdash; means the **last** axis varies fastest. Row by row.

Fortran order means the **first** axis varies fastest. Column by column.

A transposed C-ordered array is F-contiguous, because reading the transpose row by row is reading the original column by column. Nothing moved; the same bytes are simply described differently.

Both flags can be true at once for a 1-D array or an array with a length-1 axis, and both can be false for a strided slice like `a[::2]`. `a.flags` reports all of it.

Where this becomes practical: some LAPACK routines want Fortran order and will copy internally if they do not get it, and interfacing with Fortran or MATLAB-derived code sometimes requires `np.asfortranarray`. For everything else, staying in C order and not thinking about it is right.

## expand_dims and squeeze at boundaries

The length-1 axis is the currency of shape negotiation between libraries.

A model trained on batches expects `(batch, features)` and gets a single sample of shape `(features,)`. `x[None]` or `np.expand_dims(x, 0)` adds the batch axis.

A result comes back as `(n, 1)` and the next function wants `(n,)`. `squeeze` removes it.

`expand_dims(a, axis)` is the explicit form of `a[None]`, and reads better when the axis position is computed rather than literal.

`squeeze` with no argument removes **every** length-1 axis, which is the source of a genuinely nasty intermittent bug: a batch of one sample loses its batch dimension, so the code works for every batch size except one. Always name the axis &mdash; `squeeze(axis=1)` &mdash; in code that handles variable batch sizes.

## einsum as general axis manipulation

Once an operation needs a transpose, two `newaxis` insertions and a sum over a particular axis, `np.einsum` usually expresses it more clearly.

The subscript string names an index for each axis of each operand and says which survive:

`"ij->ji"` is a transpose. `"ii->i"` extracts a diagonal. `"ij->j"` sums over rows. `"ij,jk->ik"` is matrix multiplication. `"bij,bjk->bik"` is batched matrix multiplication.

Indices that appear on the left but not the right are summed over. Indices repeated between operands are matched and multiplied.

It is not always fast &mdash; for plain matrix products, `@` dispatches to a tuned BLAS routine and einsum may not. Its advantage is legibility: the string states the operation, where a chain of transposes and broadcasts states only the mechanics.

`np.einsum_path` can be used to inspect and optimise the contraction order for expressions with several operands, where the order genuinely matters.

## The batch-axis convention

Most numerical code follows one convention: **the batch axis comes first, and the axes being operated on come last**.

`(batch, height, width, channels)` for images in TensorFlow. `(batch, channels, height, width)` in PyTorch. `(samples, features)` for tabular data.

The reason the operated-on axes go last is broadcasting: trailing axes align automatically, so a per-channel or per-feature parameter of shape `(channels,)` combines with the data without any index juggling. Put the channel axis first and the same operation needs `[:, None, None]`.

`matmul` follows the same convention: it treats the last two axes as the matrix and broadcasts everything before them, so a `(batch, n, k) @ (k, m)` works directly.

Following the convention in your own arrays means broadcasting and `matmul` cooperate with you rather than requiring a transpose at every boundary.

## In practice

Use `.T` freely on 2-D and never on 1-D.

Use `moveaxis` or `swapaxes` on higher dimensions, because they name what you meant and `.T` reverses everything.

Remember that all of them return views over the same bytes, so a later `ravel` or `reshape` may copy without telling you &mdash; check with `np.shares_memory` when it matters, or force it with `np.ascontiguousarray`.

And keep the batch axis first. Most of the shape gymnastics people write is the cost of having put it somewhere else.

## Diagonals and axis-aware helpers

`np.diagonal(a)` extracts the main diagonal and returns a view in modern NumPy &mdash; read-only, because writing to it has no consistent meaning across the strides involved.

`np.trace(a)` sums the diagonal without materialising it.

`np.fill_diagonal(a, value)` writes to the diagonal in place, which is the supported way to modify it. It is the standard step when building an adjacency or distance matrix that should have zeros on the diagonal.

`offset` on `diagonal` selects the super- or sub-diagonals, which is how you extract a band.

## rollaxis, and why not to use it

Older code uses `np.rollaxis`, which moves an axis but with argument semantics that are genuinely hard to reason about &mdash; the destination is interpreted differently depending on direction.

`np.moveaxis` was added specifically to replace it, with the obvious semantics: source and destination, both plain positions.

If you meet `rollaxis` in existing code, translating it to `moveaxis` and checking the resulting shape is usually worth doing while you are there. If you are writing new code, there is no reason to use it.

## Checking that a transform did what you meant

Axis manipulation is the easiest place in NumPy to produce a result that has the right shape and the wrong contents.

Two checks catch nearly all of it.

**Verify a known element.** After `moveaxis(a, 0, -1)`, confirm that `b[i, j, k] == a[k, i, j]`. One assertion documents the transform better than a comment does.

**Use distinguishable test data.** `np.arange(24).reshape(2, 3, 4)` has a unique value in every position, so any misplacement is visible. An array of ones or of random values hides exactly the errors you are looking for.

This is worth doing because the failure mode &mdash; correct shape, permuted contents &mdash; produces no error and often no obviously wrong output, just results that are subtly worse than they should be.

## The summary

`.T` &mdash; reverses all axes. Right for 2-D, wrong for most higher-dimensional intent, and silently a no-op on 1-D.

`transpose(order)` &mdash; explicit permutation, read as "where each new axis comes from".

`swapaxes(i, j)` &mdash; exchange two, leave the rest.

`moveaxis(src, dst)` &mdash; relocate one, slide the rest. The clearest of the four, and the right default for anything above 2-D.

`expand_dims` / `squeeze` &mdash; add and remove length-1 axes, with `squeeze` needing an explicit axis in any code that handles variable batch sizes.

`einsum` &mdash; when the index bookkeeping has become the substance of the operation.

All of them return views. That is what makes them free, and it is also why a later `ravel` or `reshape` may copy without saying so &mdash; `np.shares_memory` when it matters, `np.ascontiguousarray` when you want the copy to happen somewhere visible.

## A closing note on cost

Every operation in this module is free, and that is worth stating once more because it changes how you write code.

There is no reason to avoid a transpose, a `moveaxis` or an `expand_dims` on performance grounds. They adjust a handful of integers describing the array and return immediately, whatever its size.

The cost, when it comes, arrives later &mdash; at the point something needs contiguous memory and quietly copies. That is where to look when a pipeline is slower than the operations in it suggest, and `a.flags` plus `np.shares_memory` will tell you within a minute.

## Where axis work fits

Reordering axes is almost always a translation step: between how data arrived and how the next function wants it.

That means the right question is rarely "how do I transpose this" but "what layout does the thing I am calling expect". Answering that first usually reveals that one `moveaxis` at the boundary replaces several scattered ones inside, and that keeping a single convention throughout removes most of them entirely.
''',
    [
        {"q": "What does `.T` do to a 1-D array of shape (3,)?",
         "options": ["Makes it (1,3)", "Makes it (3,1)", "Nothing - it stays (3,)", "Raises"],
         "answer": 2,
         "why": "There is no second axis to swap, and NumPy does it silently rather than raising. Use `v[:, None]` for a column."},
        {"q": "Why is transposing a 1 GB array instant?",
         "options": ["It is lazy", "Only the shape and strides change; no data is copied", "NumPy compresses it", "It is not instant"],
         "answer": 1,
         "why": "The strides simply swap. `np.shares_memory(a, a.T)` is True - it is a view over the same bytes."},
        {"q": "You have an image array shaped (3, 64, 48) and need (64, 48, 3). What is the cleanest call?",
         "options": ["img.T", "np.moveaxis(img, 0, -1)", "img.reshape(64,48,3)", "np.flipud(img)"],
         "answer": 1,
         "why": "`.T` would give (48,64,3) by reversing everything, and reshape would scramble the data. moveaxis relocates one axis and slides the rest."},
        {"q": "Why can `ravel()` on a transposed array return a copy?",
         "options": ["ravel always copies", "The transposed view is no longer C-contiguous, so a flat buffer requires new memory", "Transposes are copies", "It does not"],
         "answer": 1,
         "why": "The same reason `reshape` returns a view only *usually*. Check with np.shares_memory, or use np.ascontiguousarray to make the copy explicit."},
    ],
)


# ---------------------------------------------------------------------------
# 14. Sorting and searching
# ---------------------------------------------------------------------------
topic(
    "sorting_and_searching",
    "Sorting and Searching",
    "Operating on Arrays",
    "sort, argsort, searchsorted - and why the argument version is the one you "
    "usually need.",
    _svg(_grid(20, 30, 5, 1, 15) + _txt(58, 22, "unsorted", A, 8) +
         _arrow(102, 38, 118, 38) +
         _grid(126, 30, 3, 1, 15)),
    [
        ("sort copies, .sort() is in place",
         "NumPy's consistent convention: the function returns a new array, the method "
         "modifies.",
         '''import numpy as np

a = np.array([3, 1, 4, 1, 5])

b = np.sort(a)
print("np.sort(a):", b, " a unchanged:", a)

a.sort()
print("a.sort()  :", a, " <- a itself is now sorted")
print()
print("There is no reverse= argument. Sort, then flip:")
c = np.array([3, 1, 4, 1, 5])
print("   descending:", np.sort(c)[::-1])'''),

        ("Sorting a 2-D array sorts each row separately",
         "By default it sorts along the last axis, which is almost never a whole-array "
         "sort.",
         '''import numpy as np

a = np.array([[7, 1, 9],
              [3, 8, 2]])
print("original:"); print(a)
print()
print("sort() -> along axis=-1, each ROW independently:")
print(np.sort(a))
print()
print("sort(axis=0) -> each COLUMN independently:")
print(np.sort(a, axis=0))
print()
print("sort(axis=None) -> flatten first, one global sort:")
print(np.sort(a, axis=None))
print()
print("Note rows are sorted in isolation - they do not stay together.")'''),

        ("argsort gives the order, not the values",
         "This is the one you want whenever other arrays must follow the sort.",
         '''import numpy as np

names = np.array(["ana", "raj", "kim", "lee"])
score = np.array([72, 91, 58, 84])

order = np.argsort(score)
print("scores      :", score)
print("argsort     :", order, "<- positions, in ascending order of score")
print()
print("apply it to BOTH arrays and they stay aligned:")
print("   names :", names[order])
print("   score :", score[order])
print()
print("descending is the same order reversed:")
top = np.argsort(score)[::-1]
print("   ranking:", list(zip(names[top].tolist(), score[top].tolist())))'''),

        ("Sorting by several keys with lexsort",
         "The last key is the primary one, which reads backwards and catches everyone.",
         '''import numpy as np

dept = np.array(["b", "a", "b", "a"])
sal  = np.array([50, 70, 40, 90])

order = np.lexsort((sal, dept))     # dept first, then sal within it
print("lexsort((sal, dept)) -> LAST argument is the primary key")
for i in order:
    print("   %s  %d" % (dept[i], sal[i]))
print()
print("swap them and salary becomes primary:")
for i in np.lexsort((dept, sal)):
    print("   %s  %d" % (dept[i], sal[i]))'''),

        ("Partial sorting when you only need the top k",
         "<code>argpartition</code> is O(n) and does not bother ordering the rest.",
         '''import numpy as np
import time

rng = np.random.default_rng(0)
x = rng.random(200_000)

t = time.perf_counter(); full = np.argsort(x)[-5:]; t1 = time.perf_counter() - t
t = time.perf_counter(); part = np.argpartition(x, -5)[-5:]; t2 = time.perf_counter() - t

print("full argsort  : %.4f s" % t1)
print("argpartition  : %.4f s" % t2)
print("same 5 values :", np.array_equal(np.sort(x[full]), np.sort(x[part])))
print()
print("argpartition guarantees the top 5 are in the last 5 slots,")
print("but NOT that they are in order. Sort just those five if you care.")
print("   ordered top 5:", np.round(np.sort(x[part])[::-1], 5))'''),

        ("searchsorted finds insertion points in a sorted array",
         "Binary search, so it is fast, and it is how you bucket values.",
         '''import numpy as np

edges = np.array([0, 10, 20, 30])
vals  = np.array([5, 10, 25, 99])

print("insertion points (side='left') :", np.searchsorted(edges, vals))
print("insertion points (side='right'):", np.searchsorted(edges, vals, side="right"))
print("   the two differ only for exact matches - here, the 10")
print()
print("bucketing grades:")
cuts = np.array([40, 60, 75, 90])
labels = np.array(["F", "C", "B", "A", "A+"])
marks = np.array([12, 55, 75, 88, 97])
print("   ", dict(zip(marks.tolist(),
                      labels[np.searchsorted(cuts, marks, side="right")].tolist())))
print()
print("np.isin answers membership without sorting:")
print("   ", np.isin(np.array([1, 5, 9]), np.array([2, 5, 8])))'''),
    ],
    [
        "<code>np.sort(a)</code> returns a sorted copy; <code>a.sort()</code> sorts in place. That function-versus-method convention holds across NumPy.",
        "There is no <code>reverse=</code>. Sort ascending and slice with <code>[::-1]</code>.",
        "On a 2-D array the default sorts <strong>each row independently</strong>. Rows do not stay together.",
        "<code>argsort</code> returns positions, so you can apply the same order to several arrays and keep them aligned.",
        "<code>lexsort</code> takes the <strong>last</strong> key as primary &mdash; the reverse of how it reads.",
        "<code>argpartition</code> gets the top k in linear time without ordering the rest; <code>searchsorted</code> does binary search for insertion points and bucketing.",
    ],
    '''
title: Sorting and Searching
intro: sort, argsort and searchsorted, and why the argument version is usually the one you need.

## Copy or in place

`np.sort(a)` returns a new sorted array and leaves `a` alone. `a.sort()` sorts `a` itself and returns `None`.

That is NumPy's general convention for operations that have both forms, and it is worth relying on: if you see a bare method call with no assignment, it is modifying something.

There is no `reverse=` argument. Sort ascending and reverse with `[::-1]`, which is a free view.

## The axis default

On a 2-D array, `sort()` sorts along the **last axis** &mdash; each row independently.

This is a genuinely dangerous default when the array is a table. Sorting a `(rows, columns)` array of records scrambles every row internally: the name column gets sorted, the salary column gets sorted, and the correspondence between them is destroyed.

`sort(axis=None)` flattens and does one global sort. `sort(axis=0)` sorts each column independently, which has the same problem in the other direction.

**None of these sort rows as units.** For that you need `argsort` on a key column and then fancy indexing.

## argsort is the useful one

`np.argsort(x)` returns the positions that would sort `x`.

That indirection is the point. Apply the same index array to any number of parallel arrays and they stay aligned:

```python
order = np.argsort(score)
names[order], score[order], dates[order]
```

This is how you sort a table by a column. It is also how you produce a ranking, take the top n, or reorder anything that travels alongside the sorted values.

Descending is `np.argsort(x)[::-1]`.

One subtlety: the default sort is **quicksort**, which is not stable. Equal elements can come out in any order. Pass `kind="stable"` when ties must preserve their original relative order &mdash; for instance when you are sorting by a second key after already sorting by a first.

## Several keys

`np.lexsort` sorts by multiple keys, and the argument order reads backwards: the **last** array is the primary key.

`np.lexsort((salary, dept))` sorts by department, breaking ties by salary.

Everyone gets this wrong the first time. The mnemonic that helps: the keys are applied in order from last to first, like a stable sort chain where the final pass dominates.

## Only the top k

Sorting 200,000 values to look at 5 of them is wasteful.

`np.argpartition(x, -5)` rearranges so that the 5 largest occupy the last 5 slots, in linear time. It does **not** order them, and it does not order anything else &mdash; it only guarantees the partition boundary.

If you need those five in order, sort just those five. That is five elements instead of two hundred thousand.

The same trick works for the smallest k with a positive index, and for medians, which is what `np.median` uses internally.

## searchsorted

Given a sorted array, `np.searchsorted(edges, values)` returns where each value would be inserted to keep it sorted. It is a binary search, so it is fast even on large arrays.

Two uses come up constantly.

**Bucketing.** Given cut points, `searchsorted` gives the bucket index for each value directly, and indexing a label array with the result assigns categories in one line. `side="right"` versus `side="left"` decides which bucket an exact boundary value falls into &mdash; the only case where they differ.

**Lookup.** Finding many values in a large sorted array is `O(m log n)` this way, against `O(mn)` for repeated comparisons.

For pure membership testing where order does not matter, `np.isin` is simpler and does not require sorted input.

## The mistakes

**Sorting a table with `sort()`** and destroying the row correspondence. Use `argsort` on a key column.

**Assuming stability.** The default is not stable; pass `kind="stable"` when it matters.

**Getting `lexsort` backwards.** The last key is primary.

**Full sorting for a top-n.** `argpartition` exists precisely for that.

## The sort kinds

`kind` selects the algorithm, and the choice occasionally matters.

`"quicksort"` is the default, an introsort in practice. Fastest on average, not stable, and its worst case is handled by falling back to heapsort.

`"stable"` guarantees that equal elements keep their original relative order. It is what you need when sorting by a second key after already sorting by a first, since an unstable sort would discard the first ordering.

`"heapsort"` has a guaranteed worst case and uses no extra memory, which is occasionally the deciding factor.

`"mergesort"` is an alias for `"stable"`.

The performance difference is modest for most data. Stability is not a performance question, and when you need it, you need it.

## Sorting records

Structured arrays &mdash; arrays with named fields &mdash; can be sorted by field name:

```python
a.sort(order=["dept", "salary"])
```

This is the closest NumPy comes to sorting a table by columns, and it works because the structured dtype makes each row a single comparable item.

For plain 2-D numeric arrays, there is no `order` argument, and the answer is the `argsort` idiom: sort the key column, apply the resulting index to the whole array with fancy indexing. `a[np.argsort(a[:, 2])]` sorts rows by the third column.

For more than one key, `lexsort` produces the index and the same fancy-index application follows.

## where, nonzero, and finding things

`np.nonzero(mask)` returns the indices of True elements, as a tuple with one array per axis. `np.where(mask)` with a single argument is the same function.

The tuple form is designed to be used as an index: `a[np.nonzero(mask)]` selects the matching elements. Unpacking it with `rows, cols = np.nonzero(mask)` gives coordinates.

`np.flatnonzero(mask)` is the flat-index version, and is usually what you want for a 1-D array &mdash; it returns a plain array rather than a one-element tuple.

For "the first element matching a condition", `np.argmax(mask)` is the fast answer, because it stops at the first True. It returns 0 when nothing matches, which is indistinguishable from a match at position zero, so check `mask.any()` first. There is no built-in "find first" that handles the empty case, and this two-step is the idiom.

## searchsorted in more detail

`searchsorted` requires its first argument to be **sorted**, and does not check. Passing unsorted data gives wrong answers silently, which is the main way it goes wrong.

`side="left"` returns the first position where the value could be inserted; `side="right"` returns the last. They differ only for values that are already present, and the choice decides which bucket a boundary value falls into.

For bucketing, `side="right"` with cut points means a value exactly on a boundary goes into the upper bucket, which matches the usual convention for grade boundaries and histogram bins.

`sorter` lets you pass an `argsort` result so the lookup can be done against an unsorted array without sorting it first &mdash; useful when the array must keep its original order for other reasons.

`np.digitize` is a related function with a `right` argument whose meaning is the reverse of what the name suggests in one of its branches. `searchsorted` is easier to reason about, and does the same job.

## Ranking

A ranking is `argsort` applied twice.

`np.argsort(x)` gives the positions in sorted order. `np.argsort(np.argsort(x))` gives, for each element, its rank.

That double application is unintuitive the first time and worth the moment it takes to see: the first argsort answers "which element belongs at each rank", and inverting that mapping answers "which rank does each element get".

Ties get consecutive distinct ranks rather than being averaged, which is not what most statistical definitions of rank want. `scipy.stats.rankdata` handles tie-breaking properly, and is the right tool when the ranking is going into a statistic.

## The performance summary

Sorting is `O(n log n)`, and `argsort` costs slightly more than `sort` because it moves indices alongside comparisons.

`argpartition` is `O(n)` and is the right choice for any top-k or bottom-k question. The saving is large: for the top 5 of 200,000 values it is roughly an order of magnitude.

`searchsorted` is `O(log n)` per lookup against an already-sorted array, so `m` lookups cost `O(m log n)`. If you are searching the same array repeatedly, sorting it once and using `searchsorted` beats any linear scan.

`np.isin` builds a sorted structure internally, so it is `O((n+m) log(n+m))` &mdash; better than the naive comparison, and worth knowing that it is not free either.

## Sorting along an axis of a higher-dimensional array

`sort` takes an `axis` like every other operation, and the default is `-1` &mdash; the last one.

On a 3-D array that means each 1-D line along the last axis is sorted independently. That is rarely wrong but frequently not what was intended, and passing `axis` explicitly makes the intent visible.

`argsort` on a multi-dimensional array returns indices **along that axis only**, not flat positions. Applying them requires `np.take_along_axis`:

```python
idx = np.argsort(scores, axis=1)
ordered = np.take_along_axis(values, idx, axis=1)
```

That is the multi-dimensional version of the sort-by-key idiom, and it is the function people usually fail to find. `np.put_along_axis` is the assignment counterpart.

## Descending, and the sign trick

There is no `reverse=` argument anywhere in NumPy's sorting.

`np.sort(a)[::-1]` reverses the result, and the slice is a free view.

For `argpartition` and `argsort`, negating the values is often cleaner than reversing the result, because it keeps the index arithmetic straightforward: `np.argsort(-scores)` gives descending order directly.

That works for numeric data. It does not work for unsigned integers, where negation wraps, and it is a subtle way to get a wrong answer on `uint8` image data.

## Searching by value

There is no `index()` method. Finding where a value occurs is a comparison followed by a search:

`np.flatnonzero(a == value)` gives every position, as a plain array.

`np.argmax(a == value)` gives the first, in one pass, with the caveat that it returns 0 when nothing matches.

For a sorted array, `np.searchsorted` finds the position in logarithmic time, which is the right choice when searching repeatedly.

For membership across two arrays, `np.isin` handles it in one call rather than a loop of comparisons.

## The summary

`np.sort` copies; `a.sort()` modifies. That distinction holds throughout NumPy.

`argsort` is the one to use whenever anything else must follow the ordering, which in practice is most of the time.

`kind="stable"` when ties must keep their original order, which includes any multi-pass sort by successive keys.

`lexsort` for several keys, remembering that the **last** one is primary.

`argpartition` for top-k, which is linear rather than `n log n`.

`searchsorted` for insertion points and bucketing, on data that is genuinely sorted &mdash; it does not check.

`take_along_axis` when applying `argsort` results on more than one dimension.

Between them those cover essentially every ordering question, and the two that get used most are `argsort` and `argpartition`.

## One more thing about stability

Stability is not a performance setting, and it is worth one more paragraph because the cost of getting it wrong is invisible.

An unstable sort is free to reorder equal elements arbitrarily. That means two runs on the same data can produce different output, and the difference only appears when there are ties. Code that sorts by a secondary key and then by a primary key relies entirely on the second sort preserving the first ordering, and with the default `kind` it does not.

Whenever a sort follows another sort, or whenever the output order of tied records is observable, pass `kind="stable"`. The cost is small and the alternative is a bug that reproduces intermittently.

## Where sorting fits

Sorting is rarely the goal in itself. It is the step that makes something else possible: a ranking, a top-n, a binary search, a group-by on the boundaries where a key changes, a merge of two datasets.

That framing helps when choosing. If the sorted array itself is not needed, `argsort` or `argpartition` usually is &mdash; and if you only need the order to apply it elsewhere, sorting the values was wasted work.
''',
    [
        {"q": "What does `a.sort()` do on a 2-D array by default?",
         "options": ["Sorts the whole array", "Sorts each row independently along the last axis", "Sorts each column", "Sorts rows as units"],
         "answer": 1,
         "why": "On a table this destroys the correspondence between columns. To sort rows as units, argsort a key column and index with the result."},
        {"q": "Why use `argsort` rather than `sort`?",
         "options": ["It is faster", "It returns positions, so the same order can be applied to parallel arrays", "It is stable", "It sorts descending"],
         "answer": 1,
         "why": "That indirection is the whole point - it is how you sort a table by a column and keep every other column aligned."},
        {"q": "In `np.lexsort((salary, dept))`, which is the primary key?",
         "options": ["salary", "dept - the last argument", "Neither", "Both equally"],
         "answer": 1,
         "why": "The argument order reads backwards, and everyone gets it wrong the first time. The keys are applied last to first."},
        {"q": "You need the 5 largest of 200,000 values. What is the right tool?",
         "options": ["np.sort then slice", "np.argpartition(x, -5)[-5:]", "np.max five times", "np.searchsorted"],
         "answer": 1,
         "why": "Linear time instead of n log n. It does not order the top 5 - sort just those five afterwards if you need them ranked."},
    ],
)


# ---------------------------------------------------------------------------
# 15. Unique values and set operations
# ---------------------------------------------------------------------------
topic(
    "unique_and_set_operations",
    "Unique Values and Set Operations",
    "Operating on Arrays",
    "Counting distinct values, comparing two arrays, and rebuilding the original "
    "from what unique returned.",
    _svg(_grid(20, 30, 4, 1, 15) + _txt(50, 22, "with repeats", A, 8) +
         _arrow(88, 38, 104, 38) +
         _grid(112, 30, 2, 1, 15) + _txt(127, 22, "unique", M, 8)),
    [
        ("unique returns sorted distinct values",
         "Always sorted, always 1-D unless you ask otherwise.",
         '''import numpy as np

a = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
print("input :", a)
print("unique:", np.unique(a), "<- sorted, duplicates gone")
print()
print("it flattens a 2-D input by default:")
b = np.array([[1, 2], [2, 3]])
print("   ", np.unique(b))
print()
print("strings work too, sorted alphabetically:")
print("   ", np.unique(np.array(["pear", "fig", "pear", "apple"])))'''),

        ("return_counts is the frequency table",
         "One call gives values and how often each appeared.",
         '''import numpy as np

votes = np.array(["red", "blue", "red", "green", "red", "blue"])
vals, counts = np.unique(votes, return_counts=True)

for v, c in zip(vals.tolist(), counts.tolist()):
    print("   %-6s %d" % (v, c))

print()
print("the winner, without a loop:")
print("   ", vals[counts.argmax()], "with", int(counts.max()))
print()
print("counts sum back to the input length:", int(counts.sum()), "==", len(votes))'''),

        ("return_index and return_inverse",
         "Where each unique value first appeared, and how to rebuild the original.",
         '''import numpy as np

a = np.array([30, 10, 20, 10, 30])

vals, first, inv = np.unique(a, return_index=True, return_inverse=True)
print("values :", vals)
print("first  :", first, "<- index in a where each value first occurs")
print("inverse:", inv, "<- which unique value each element of a is")
print()
print("inverse rebuilds the original exactly:")
print("   ", vals[inv], " matches:", np.array_equal(vals[inv], a))
print()
print("This is label encoding in one line - categories to integers.")'''),

        ("Unique rows, not unique values",
         "<code>axis=0</code> treats each row as a single item.",
         '''import numpy as np

rows = np.array([[1, 2],
                 [3, 4],
                 [1, 2],
                 [5, 6]])
print("input:"); print(rows)
print()
print("np.unique(rows)          ->", np.unique(rows), "<- all values, flattened")
print()
print("np.unique(rows, axis=0)  -> duplicate ROWS removed:")
print(np.unique(rows, axis=0))
print()
uniq, cnt = np.unique(rows, axis=0, return_counts=True)
print("with counts:")
for r, c in zip(uniq.tolist(), cnt.tolist()):
    print("   %s seen %d time(s)" % (r, c))'''),

        ("The four set operations",
         "Intersection, union, difference and symmetric difference - all returning "
         "sorted unique results.",
         '''import numpy as np

a = np.array([1, 2, 3, 4, 4])
b = np.array([3, 4, 5])

print("a =", a, "  b =", b)
print()
print("intersect1d :", np.intersect1d(a, b), "in both")
print("union1d     :", np.union1d(a, b), "in either")
print("setdiff1d   :", np.setdiff1d(a, b), "in a only")
print("setxor1d    :", np.setxor1d(a, b), "in exactly one")
print()
print("All of them de-duplicate: the repeated 4 in a appears once.")'''),

        ("isin keeps the shape - and that is the difference",
         "Set operations reduce; <code>isin</code> gives a mask you can index with.",
         '''import numpy as np

ids   = np.array([[101, 102], [103, 104]])
wanted = np.array([102, 104, 999])

mask = np.isin(ids, wanted)
print("ids:"); print(ids)
print("mask (same shape):"); print(mask)
print()
print("select with it:", ids[mask])
print("invert it     :", ids[~mask])
print()
print("intersect1d would have given a flat sorted list instead:")
print("   ", np.intersect1d(ids, wanted))
print()
print("isin is the one to use when you need to filter rows by a key.")'''),
    ],
    [
        "<code>np.unique</code> always returns <strong>sorted</strong> distinct values, and flattens the input unless you pass <code>axis</code>.",
        "<code>return_counts=True</code> gives a frequency table in one call &mdash; values and counts, aligned.",
        "<code>return_inverse</code> maps every element to its position in the unique array, so <code>vals[inv]</code> rebuilds the original. That is label encoding.",
        "<code>axis=0</code> makes <code>unique</code> operate on whole <strong>rows</strong> rather than individual values.",
        "<code>intersect1d</code>, <code>union1d</code>, <code>setdiff1d</code> and <code>setxor1d</code> all de-duplicate and sort.",
        "<code>np.isin</code> returns a <strong>mask of the original shape</strong>, which is what you need for filtering rather than reducing.",
    ],
    '''
title: Unique Values and Set Operations
intro: Counting distinct values, comparing arrays, and rebuilding the original.

## unique

`np.unique(a)` returns the distinct values, **sorted**, as a 1-D array.

Two things about that are worth stating explicitly, because both catch people.

It is always sorted. If you wanted first-appearance order, `unique` alone does not give it &mdash; you need `return_index` and then a sort of those indices.

It always flattens, unless you pass `axis`. A 2-D input gives back a flat list of every distinct value in the whole array.

## The optional returns

Three flags turn `unique` from a de-duplicator into something considerably more useful.

**`return_counts`** gives how many times each value occurred, aligned with the values. This is a frequency table, and combined with `argmax` it gives the mode in two lines with no loop.

**`return_index`** gives, for each unique value, the index in the input where it first appeared. Useful when you want the *first* record for each key rather than just the key.

**`return_inverse`** gives, for each element of the input, which unique value it corresponds to. `vals[inv]` reconstructs the input exactly.

That last one is worth dwelling on. It is label encoding: an array of categories becomes an array of small integers plus a lookup table. Machine learning pipelines do this constantly, and `np.unique(..., return_inverse=True)` is the whole implementation.

The returns come back in a fixed order &mdash; values, index, inverse, counts &mdash; regardless of which flags you set, so unpack carefully when you enable more than one.

## Unique rows

`np.unique(rows, axis=0)` treats each row as an item and removes duplicate rows.

This is what you want for de-duplicating records, and it composes with `return_counts` to find how many times each distinct row appeared &mdash; a group-by, for the case where the whole row is the key.

Rows are compared elementwise, and the result is sorted lexicographically.

## Set operations

Four functions, all following the same rules: they treat the inputs as sets, de-duplicate, and return sorted results.

`intersect1d` &mdash; in both.
`union1d` &mdash; in either.
`setdiff1d` &mdash; in the first only.
`setxor1d` &mdash; in exactly one.

The `1d` in the names is a warning: they flatten their inputs. If you pass 2-D arrays you get a flat answer.

`intersect1d` accepts `assume_unique=True`, which skips the internal de-duplication and is meaningfully faster on large arrays you already know are unique.

## isin is the different one

The set functions **reduce**. They answer "what is in both?" and hand you a smaller array, with the original positions gone.

`np.isin(a, b)` **preserves shape**. It returns a boolean mask the same shape as `a`, saying whether each element appears in `b`.

That distinction decides which one you need. If the question is "which values do these two arrays share?", use `intersect1d`. If the question is "which rows of my table have an id in this list?", you need the mask, because you are going to index with it &mdash; and `intersect1d` has thrown away exactly the information you need.

`~mask` inverts it, which is how you exclude a list rather than include one.

## Performance

These are all sort-based, so roughly `O(n log n)`. That is fast, but for repeated membership tests against the same fixed set, a Python `set` or a sorted array with `searchsorted` can beat rebuilding the comparison each time.

For counting, `np.bincount` is faster than `unique(return_counts=True)` when the values are small non-negative integers, because it can index directly instead of sorting.

## The mistakes

**Expecting first-appearance order.** `unique` sorts.

**Passing 2-D to a set function** and being surprised by a flat result. They all flatten.

**Reaching for `intersect1d` when filtering.** It discards positions. `isin` keeps them.

**Unpacking the returns in the wrong order.** Values, index, inverse, counts &mdash; always in that order, whichever subset you asked for.

## bincount, the fast path for integers

When the values are small non-negative integers, `np.bincount` counts them far faster than `unique(return_counts=True)`, because it indexes an output array directly instead of sorting.

`np.bincount(a)` returns an array of length `a.max() + 1`, where position `i` holds the count of value `i`. Values that never appear get zero, which is either convenient or a nuisance depending on whether the value space is dense.

`minlength` forces a minimum output size, which matters when you are counting class labels and a class might be absent from a particular batch &mdash; without it, the output length varies with the data and downstream code breaks.

The `weights` argument turns it into a group-sum. `np.bincount(group_ids, weights=values)` sums the values belonging to each group in a single pass, which is the fastest group-by NumPy offers and a genuinely useful thing to know.

The constraint is that the values must be non-negative integers, and memory is proportional to the largest one. Counting values around a million allocates a million-element array regardless of how few distinct values there are.

## Grouping without pandas

The `unique` returns compose into a real group-by.

```python
keys, inverse = np.unique(group_column, return_inverse=True)
sums = np.bincount(inverse, weights=value_column)
counts = np.bincount(inverse)
means = sums / counts
```

`unique` maps arbitrary keys &mdash; strings included &mdash; to dense integers, and `bincount` aggregates over those integers. Four lines, no loop, and it handles any number of groups.

For aggregations that are not sums, sorting by the key and using `np.split` at the boundaries where the key changes gives a list of per-group arrays:

```python
order = np.argsort(keys)
sorted_keys = keys[order]
cuts = np.flatnonzero(sorted_keys[1:] != sorted_keys[:-1]) + 1
groups = np.split(values[order], cuts)
```

That is more machinery than pandas' `groupby`, and it is the right amount when adding pandas to a project for one aggregation would be the larger cost.

## histogram, for continuous values

`unique` is for discrete values. Its continuous counterpart is `np.histogram`, which counts how many values fall into each of a set of bins.

It returns counts and edges. The edges array is one longer than the counts, because n bins have n+1 boundaries &mdash; a small detail that causes a lot of off-by-one confusion when plotting.

`bins` accepts a count, an explicit array of edges, or one of several automatic rules like `"auto"` and `"fd"` that choose a bin width from the data.

`np.histogram2d` and `np.histogramdd` handle two and more dimensions.

The bins are half-open &mdash; `[a, b)` &mdash; except the last, which includes its right edge so that the maximum value is counted somewhere. That asymmetry is deliberate and occasionally surprising.

## assume_unique, and when to use it

`intersect1d`, `setdiff1d` and `isin` accept `assume_unique=True`.

Setting it skips the internal de-duplication, which is a real saving on large arrays. Setting it wrongly gives **wrong answers**, not an error &mdash; duplicates are handled as though they were not there, and results can come out with unexpected repeats.

Use it only when uniqueness is guaranteed structurally: the array came from `unique`, or it is a primary key, or you have just checked. "It should be unique" is not the same thing.

`isin` also has a `kind` argument that chooses between a sort-based and a table-based implementation. The table-based version is much faster for integers over a small range and uses memory proportional to that range, so the automatic choice is usually right and worth overriding only after measuring.

## Ordering, and how to get first-appearance order

Every one of these functions returns sorted output, and sometimes sorted is not what you want.

For first-appearance order, use `return_index` and sort the indices:

```python
vals, idx = np.unique(a, return_index=True)
first_seen_order = vals[np.argsort(idx)]
```

The indices say where each unique value first appeared; sorting by them restores the original encounter order.

This comes up more often than it looks &mdash; category codes that should follow the data's order, deduplication that should keep the first occurrence, log analysis where the sequence carries meaning.

## Summary of the choices

**Distinct values, any dtype**: `np.unique`.

**Counts of small non-negative integers**: `np.bincount`, and use `minlength`.

**Counts of anything else**: `np.unique(return_counts=True)`.

**Group aggregation**: `unique(return_inverse=True)` feeding `bincount(weights=...)`.

**Continuous data**: `np.histogram`.

**Comparing two arrays as sets**: the `1d` family, remembering that they flatten.

**Filtering by membership**: `np.isin`, because it keeps the shape and the others do not.

## Uniqueness on floats

Applying `unique` to floating-point data usually disappoints, because values that are conceptually equal differ in the last bits.

`np.unique([0.1 + 0.2, 0.3])` returns two values, not one.

There is no tolerance argument, and adding one would be ill-defined &mdash; "close enough" is not transitive, so a tolerant unique has no unambiguous answer.

The practical approaches are to round first, `np.unique(np.round(a, 6))`, which is exact and cheap but sensitive to values sitting near a rounding boundary; or to sort and group with an explicit tolerance if the semantics matter.

For anything more careful, this is a clustering problem rather than a uniqueness problem, and treating it as one avoids pretending the answer is exact.

## Set operations on rows

The `1d` family flattens, so comparing two tables row-wise needs a different approach.

`np.unique(rows, axis=0)` handles de-duplication. For intersection and difference between two sets of rows, the usual trick is to view each row as a single opaque item &mdash; either through a structured dtype, or by converting rows to tuples and using Python sets when the arrays are small enough.

For larger data this is the point where pandas' `merge` is the right tool, and reaching for it is not a defeat. NumPy is deliberately a numerical array library rather than a relational one.

## Performance notes

`np.unique` sorts, so it is `O(n log n)` and allocates.

`np.bincount` is `O(n)` for small non-negative integers, and allocates proportional to the largest value rather than the number of distinct ones. For values up to a few million that is a good trade; for sparse large values it is not.

`np.isin` builds a sorted structure or a lookup table depending on `kind`, so it is not free either &mdash; but it is far better than a loop of comparisons, and better than repeatedly calling `intersect1d`.

For repeated membership tests against a fixed small set, a Python `set` can beat all of them, because the per-call overhead of NumPy dominates when the query is a single value.

## The summary

`np.unique` &mdash; sorted distinct values. `return_counts` for frequencies, `return_inverse` for label encoding, `return_index` for first occurrence, `axis=0` for rows.

`np.bincount` &mdash; fast counting for small non-negative integers, with `minlength` to fix the output size and `weights` to turn it into a group-sum.

`np.histogram` &mdash; the continuous analogue, returning counts and one more edge than counts.

`intersect1d` / `union1d` / `setdiff1d` / `setxor1d` &mdash; set comparisons, all sorting, de-duplicating and flattening.

`np.isin` &mdash; membership as a mask of the original shape, which is the one to use for filtering.

The recurring decision is between the functions that **reduce** and the one that **preserves shape**. If the answer is going to index something, you want the mask.

## A closing note

The functions in this module are simple individually and powerful in combination. `unique` with `return_inverse` feeding `bincount` with `weights` is four lines that replace a loop, a dictionary and a fair amount of care about missing keys.

The one distinction worth carrying away is between reducing and preserving shape. Almost every mistake in this area is reaching for a set function &mdash; which discards positions &mdash; when the question was really about filtering, which needs them. When the answer is going to index something, `isin` is the function you want.

## Where this fits

Counting distinct values is usually the first thing anyone does with a new dataset, and the last thing anyone remembers to do before trusting a result.

`np.unique(col, return_counts=True)` on every categorical column at load time takes seconds and routinely surfaces the problems that would otherwise appear much later: a category with a trailing space, an identifier that is not unique, a class that appears twice in the training set and never in the test set.
''',
    [
        {"q": "What order does `np.unique` return values in?",
         "options": ["First appearance", "Sorted", "Random", "By frequency"],
         "answer": 1,
         "why": "Always sorted, and it flattens the input unless you pass axis. For first-appearance order you need return_index and a sort of those indices."},
        {"q": "What does `return_inverse` give you?",
         "options": ["The reversed array", "For each input element, which unique value it is - so vals[inv] rebuilds the input", "The counts", "The first indices"],
         "answer": 1,
         "why": "That is label encoding in one call: categories become small integers plus a lookup table."},
        {"q": "You have a table of ids and a list of wanted ids, and need the matching rows. Which function?",
         "options": ["np.intersect1d", "np.isin", "np.union1d", "np.unique"],
         "answer": 1,
         "why": "isin returns a mask of the original shape, which you can index with. intersect1d reduces and throws away the positions you need."},
        {"q": "What does `np.unique(rows, axis=0)` do?",
         "options": ["Sorts the rows", "Removes duplicate rows, treating each row as one item", "Returns all distinct values flattened", "Raises"],
         "answer": 1,
         "why": "Combined with return_counts it is a group-by for the case where the whole row is the key."},
    ],
)


# ---------------------------------------------------------------------------
# 16. Random numbers
# ---------------------------------------------------------------------------
topic(
    "random_numbers",
    "Random Numbers",
    "Working with Data",
    "The modern Generator API, why np.random.seed is legacy, and how to make "
    "results reproducible.",
    _svg(_box(20, 28, 44, 34, S, A) + _txt(42, 49, "seed", A, 8) +
         _arrow(68, 45, 84, 45) +
         _grid(92, 32, 4, 2, 13)),
    [
        ("default_rng is the current API",
         "Create a generator, seed it once, and pass it around.",
         '''import numpy as np

rng = np.random.default_rng(42)

print("uniform [0,1) :", np.round(rng.random(4), 4))
print("integers 1-6  :", rng.integers(1, 7, size=6))
print("normal mu=0   :", np.round(rng.normal(size=4), 3))
print("choice        :", rng.choice(["a", "b", "c"], size=5))
print()
print("The legacy np.random.rand / np.random.seed still work, but they")
print("share one hidden global generator, which makes code that uses")
print("them impossible to isolate or test in parallel.")'''),

        ("The same seed gives the same numbers",
         "That is what reproducibility means, and it is per generator.",
         '''import numpy as np

a = np.random.default_rng(7).random(3)
b = np.random.default_rng(7).random(3)
c = np.random.default_rng(8).random(3)

print("seed 7 :", np.round(a, 5))
print("seed 7 :", np.round(b, 5), " identical:", np.array_equal(a, b))
print("seed 8 :", np.round(c, 5), " different:", not np.array_equal(a, c))
print()
print("A generator carries state, so consecutive draws differ:")
rng = np.random.default_rng(7)
print("   first :", np.round(rng.random(3), 5))
print("   second:", np.round(rng.random(3), 5))'''),

        ("Shapes, not loops",
         "Every method takes a size, so you draw the whole array at once.",
         '''import numpy as np

rng = np.random.default_rng(0)

print("one value  :", round(float(rng.random()), 4))
print("a vector   :", np.round(rng.random(3), 4))
print("a matrix   :"); print(np.round(rng.random((2, 3)), 4))
print()
print("dice, 4 players x 3 rolls:")
print(rng.integers(1, 7, size=(4, 3)))
print()
print("integers is HALF-OPEN like range: high is excluded.")
print("   integers(1, 3, size=8):", rng.integers(1, 3, size=8), "<- no 3s")'''),

        ("Sampling, with and without replacement",
         "<code>choice</code> covers both, plus weighted draws.",
         '''import numpy as np

rng = np.random.default_rng(3)
pool = np.arange(10)

print("with replacement    :", rng.choice(pool, size=6))
print("without replacement :", rng.choice(pool, size=6, replace=False))
print()
w = np.array([0.7, 0.2, 0.1])
draws = rng.choice(["common", "rare", "epic"], size=1000, p=w)
vals, counts = np.unique(draws, return_counts=True)
print("weighted, 1000 draws:")
for v, c in zip(vals.tolist(), counts.tolist()):
    print("   %-7s %.1f%%" % (v, 100 * c / 1000))
print()
print("p must sum to 1, and size must fit when replace=False.")'''),

        ("Shuffling and permutations",
         "<code>shuffle</code> modifies in place; <code>permutation</code> returns a "
         "new array.",
         '''import numpy as np

rng = np.random.default_rng(5)

a = np.arange(8)
rng.shuffle(a)
print("shuffle (in place) :", a)

b = np.arange(8)
print("permutation        :", rng.permutation(b), " b unchanged:", b)
print()
print("On a 2-D array, shuffle moves whole ROWS:")
t = np.arange(12).reshape(4, 3)
rng.shuffle(t)
print(t)
print()
print("To shuffle two arrays together, permute an index array:")
idx = rng.permutation(4)
print("   apply", idx, "to both and they stay aligned")'''),

        ("A train/test split, correctly",
         "Permute indices once, then slice - never sample twice.",
         '''import numpy as np

rng = np.random.default_rng(1)
n = 20
X = np.arange(n) * 10
y = np.arange(n) % 2

idx = rng.permutation(n)
cut = int(0.75 * n)
train, test = idx[:cut], idx[cut:]

print("train size:", len(train), " test size:", len(test))
print("overlap   :", len(np.intersect1d(train, test)), "<- must be 0")
print()
print("X_train:", X[train][:6], "...")
print("y_train:", y[train][:6], "...")
print()
print("Drawing two independent samples would let rows appear in both,")
print("which quietly inflates every score you measure afterwards.")'''),
    ],
    [
        "<code>np.random.default_rng(seed)</code> is the current API. The legacy <code>np.random.seed</code> mutates one hidden global generator.",
        "The same seed gives the same sequence, and a generator carries state &mdash; consecutive draws differ.",
        "Every method takes <code>size</code>, so you draw whole arrays at once rather than looping.",
        "<code>integers(low, high)</code> is half-open like <code>range</code>: <code>high</code> is excluded.",
        "<code>choice</code> handles replacement and weights; <code>shuffle</code> is in place and <code>permutation</code> returns a copy.",
        "Split data by permuting an index array once and slicing it &mdash; sampling twice can put the same row in both halves.",
    ],
    '''
title: Random Numbers
intro: The modern Generator API, and how to make results reproducible.

## Two APIs, one of them legacy

You will see both in the wild.

`np.random.rand`, `np.random.randint`, `np.random.seed` are the **legacy** interface. They all operate on a single hidden global generator.

`np.random.default_rng()` returns a **Generator** object with its own state. Every method lives on that object.

The new one is preferred, and the reason is not cosmetic. A global generator means any library you import can consume from the same stream, so your seeded results change when an unrelated dependency starts drawing numbers. It also cannot be used safely from more than one thread, and it makes tests interfere with each other in ways that are hard to trace.

An explicit generator is passed where it is needed, and nothing else can touch it. Create it once, near the top, and thread it through.

The legacy functions are not deprecated and existing code does not need rewriting, but new code should use `default_rng`.

## Seeding

`default_rng(42)` gives a generator whose sequence is fully determined. Two generators created with the same seed produce identical output.

The generator is stateful: each call advances it, so consecutive draws from the same generator differ. That is the point &mdash; you seed once, not before every call.

Seeding inside a loop is a common bug. It produces the same "random" value every iteration, and the symptom is data that looks suspiciously uniform.

For genuinely unpredictable values, call `default_rng()` with no argument; it seeds from the operating system.

## Shapes

Every method takes `size`, and it accepts a tuple.

`rng.random((3, 4))` gives a `(3, 4)` array in one call. There is never a reason to loop.

`rng.integers(low, high)` is **half-open**, like `range` and like slicing: `high` is excluded. The legacy `randint` behaved the same way, but `random_integers`, now removed, did not &mdash; which is why the memory is unreliable and worth checking.

## The distributions

`random` for uniform `[0, 1)`. `integers` for uniform integers. `normal(loc, scale)` for Gaussian. `uniform(low, high)` for a uniform range other than the unit interval.

Beyond those there are dozens &mdash; `poisson`, `exponential`, `binomial`, `multivariate_normal` &mdash; all following the same `size` convention.

## choice

`rng.choice(pool, size=n)` samples with replacement by default.

`replace=False` samples without, and raises if `size` exceeds the pool. That is the right behaviour: silently returning duplicates when you asked for distinct items would be worse.

`p=weights` gives a weighted draw. The weights must sum to 1 and have one entry per element of the pool.

`choice` also accepts an integer instead of an array, meaning "choose from `arange(n)`", which is often what you want when you are really choosing indices.

## Shuffling

`rng.shuffle(a)` modifies in place and returns `None`. `rng.permutation(a)` returns a shuffled copy.

On a 2-D array, both operate on the **first axis** &mdash; whole rows move, and their contents stay intact. That is almost always what you want for a table of records, and it is worth knowing rather than assuming it shuffles every element.

## Splitting data

The correct pattern is one permutation, then slicing:

```python
idx = rng.permutation(n)
train, test = idx[:cut], idx[cut:]
```

The tempting alternative &mdash; drawing a training sample and then a test sample &mdash; allows the same row into both, because the two draws know nothing about each other. That leaks test data into training and inflates every score you measure afterwards, sometimes dramatically, and the code gives no sign anything is wrong.

Permuting once makes the disjointness structural rather than probabilistic. The same index array applied to `X` and `y` keeps them aligned.

## Reproducibility in practice

Seed at the entry point, not scattered through the code. Record the seed alongside results. Pass the generator explicitly into any function that needs randomness, so it can be tested with a fixed one.

And be clear about what a seed guarantees: identical results for the same NumPy version and the same sequence of calls. Change the order of operations and the numbers change, even with the seed unchanged.

## What is underneath a Generator

`default_rng` returns a `Generator` wrapping a **bit generator**, which is the thing that actually produces random bits. The default is PCG64.

The split matters because the two layers have different jobs. The bit generator produces a stream of uniform bits; the Generator turns those into distributions. Swapping the bit generator &mdash; `default_rng(np.random.MT19937(seed))` for the old Mersenne Twister, or `Philox` for a counter-based one &mdash; changes the stream without changing the interface.

PCG64 was chosen as the default because it is fast, has good statistical properties, and supports cheap independent streams. Mersenne Twister, the legacy default, is slower and has a much larger state.

None of these are cryptographically secure. For tokens, passwords or anything an adversary should not predict, use the `secrets` module, not NumPy.

## Independent streams

Running the same simulation in parallel needs each worker to draw different numbers, and seeding each with a different arbitrary integer is not a reliable way to get that &mdash; nearby seeds can produce overlapping streams.

`SeedSequence` is the supported answer:

```python
ss = np.random.SeedSequence(12345)
children = ss.spawn(4)
rngs = [np.random.default_rng(c) for c in children]
```

Each child produces a stream that is statistically independent of the others, and the whole set is reproducible from the single parent seed.

`rng.spawn(n)` on a Generator does the same thing more directly in recent NumPy versions.

This is the right way to seed workers in a multiprocessing pool, and it means one recorded seed reproduces the entire parallel run.

## The legacy interface, and when you need it

`np.random.RandomState` is the old object-oriented interface, and the global functions like `np.random.rand` are methods on a hidden instance of it.

It is frozen for backwards compatibility: its stream is guaranteed never to change across NumPy versions. `Generator` carries no such guarantee, and its output can change between versions if an algorithm is improved.

That makes `RandomState` the correct choice in exactly one situation: reproducing results from older code or published work where the exact numbers matter.

For everything else, `Generator` is faster, has better distributions, and does not share state with every other piece of code in the process.

## Choosing a distribution

The ones that come up most, and what they model:

`uniform(low, high)` &mdash; no information beyond a range.

`normal(loc, scale)` &mdash; measurements with symmetric error, sums of many small independent effects.

`lognormal` &mdash; quantities that cannot be negative and are multiplicative: incomes, file sizes, response times.

`poisson(lam)` &mdash; counts of independent events in a fixed interval: arrivals, defects, requests per second.

`exponential(scale)` &mdash; waiting times between Poisson events.

`binomial(n, p)` &mdash; successes out of n trials.

Using `normal` for a quantity that cannot be negative is a common modelling error, and it shows up as negative durations or negative counts in generated test data. `lognormal` or a truncated distribution is usually what was meant.

## Generating realistic test data

A few patterns worth having.

**Correlated variables**: `rng.multivariate_normal(mean, cov, size=n)` draws from a specified covariance structure, which is how you produce test data where the relationships are known.

**Categorical with known proportions**: `rng.choice(categories, size=n, p=weights)`.

**Sorted timestamps**: draw uniformly and sort, or accumulate exponential gaps with `cumsum` for a Poisson process.

**Reproducible shuffling of an existing dataset**: `rng.permutation(len(data))` applied as an index, never two independent draws.

## Reproducibility, honestly

A seed guarantees the same numbers for the same NumPy version, the same generator, and the **same sequence of calls**.

Change the order of operations and the numbers change. Add a draw in the middle and everything after it shifts. Parallelise differently and the assignment of numbers to workers changes.

This means a seed reproduces a run, not a result. Code that draws different amounts of randomness depending on the data will not reproduce across changes to that data, even with the seed fixed.

The practical discipline: seed once at the entry point, record the seed alongside the output, pass the generator explicitly into anything that needs it, and use `SeedSequence` for parallel work. Those four habits cover almost every reproducibility problem people actually hit.

## Passing the generator around

The habit that makes randomness testable is to accept a generator as an argument rather than creating one inside a function.

```python
def make_sample(n, rng):
    return rng.normal(size=n)
```

The caller decides the seed, so the same function serves production &mdash; where the generator is seeded from the operating system &mdash; and tests, where a fixed seed makes assertions possible.

A default of `rng=None` with `rng = np.random.default_rng(rng)` inside is a useful pattern: `default_rng` accepts a Generator, an integer seed, a SeedSequence or None, and returns a Generator in every case. That gives callers all four options with one line.

The alternative &mdash; calling `np.random.seed` somewhere and hoping &mdash; is what makes randomised code untestable and non-reproducible, because any other code drawing from the same global stream changes the results.

## Randomness in tests

A test that uses random data and a fixed seed is testing one sample. That is usually fine, and it is better than a test with hard-coded magic numbers.

The failure mode to avoid is a test that passes for most seeds and fails for some. If a test is checking a statistical property &mdash; that a mean is near zero, that a split is roughly balanced &mdash; the tolerance has to be wide enough for the distribution, not tuned until the current seed passes.

`np.allclose` with an explicit tolerance expresses that far better than exact comparison, and stating the tolerance forces the question of how much variation is acceptable.

For anything where the property should hold for all inputs rather than one sample, property-based testing with several seeds is the honest version.

## Common mistakes

**Seeding inside a loop.** Produces the same value every iteration. The symptom is suspiciously uniform data.

**Using `np.random.seed` in a library.** It mutates global state that belongs to the application, not to you.

**Sampling twice for a train/test split.** The two draws are independent, so rows can appear in both. Permute once.

**Using `normal` for a non-negative quantity.** Produces negative durations and negative counts. `lognormal` or a truncated distribution is usually what was meant.

**Expecting `shuffle` to return something.** It modifies in place and returns None, so `a = rng.shuffle(a)` sets `a` to None. `permutation` is the returning version.

**Assuming a seed reproduces a result rather than a run.** Change the order of draws and the numbers change, seed or no seed.

## The summary

Create one generator with `default_rng(seed)` at the entry point.

Pass it explicitly to anything that needs randomness.

Use `SeedSequence` or `spawn` for parallel workers, never nearby integer seeds.

Draw whole arrays with `size` rather than looping.

Permute an index array once when splitting or shuffling aligned data.

Record the seed with the results, and remember that it reproduces the sequence of calls, not the conclusion.

## A closing note

Randomness is one of the few areas where the convenient API and the correct API differ, and where the convenient one has been the default for long enough that most examples still use it.

`np.random.seed` and its companions are not broken, and existing code using them does not need rewriting. But new code has a better option, and the reasons &mdash; isolation, thread safety, reproducible parallelism &mdash; are the kind that only matter once, catastrophically, at the point where results cannot be reproduced.

One generator, created explicitly, passed where it is needed. That single habit covers almost everything.

## One last habit

Record the seed with the output, not just in the code.

A seed that lives only in a source file is lost the moment the file changes, and the results it produced become unreproducible without a git archaeology session. Writing it into the output &mdash; a filename, a metadata field, a log line &mdash; costs nothing and is the difference between results that can be regenerated and results that can only be trusted.
''',
    [
        {"q": "Why is `default_rng` preferred over `np.random.seed`?",
         "options": ["It is faster", "It gives an isolated generator instead of mutating one hidden global", "It produces better randomness", "seed is deprecated"],
         "answer": 1,
         "why": "A global generator means an unrelated library drawing numbers changes your seeded results, and it cannot be used safely across threads."},
        {"q": "What does `rng.integers(1, 3, size=8)` produce?",
         "options": ["Only 1s, 2s and 3s", "Only 1s and 2s - high is excluded", "Only 2s", "Eight 3s"],
         "answer": 1,
         "why": "Half-open like range and like slicing. The removed `random_integers` was inclusive, which is why the memory is unreliable."},
        {"q": "What does `rng.shuffle(a)` do to a 2-D array?",
         "options": ["Shuffles every element", "Shuffles whole rows along the first axis", "Shuffles columns", "Raises"],
         "answer": 1,
         "why": "Row contents stay intact, which is what you want for a table of records."},
        {"q": "What is wrong with drawing a train sample and then a test sample separately?",
         "options": ["It is slow", "The two draws are independent, so the same row can land in both", "It needs a seed", "Nothing"],
         "answer": 1,
         "why": "That leaks test data into training and inflates every score, with no sign in the code. Permute an index array once and slice it instead."},
    ],
)


# ---------------------------------------------------------------------------
# 17. Linear algebra
# ---------------------------------------------------------------------------
topic(
    "linear_algebra",
    "Linear Algebra",
    "Working with Data",
    "Matrix multiplication, solving systems, and why you should almost never "
    "invert a matrix.",
    _svg(_grid(20, 28, 2, 2, 16) + _txt(52, 50, "@", A, 12) +
         _grid(64, 28, 2, 2, 16) + _txt(104, 50, "=", A, 11) +
         _grid(116, 28, 2, 2, 16)),
    [
        ("@ is matrix multiplication, * is not",
         "The single most common confusion, and both are legal so nothing warns you.",
         '''import numpy as np

a = np.array([[1, 2],
              [3, 4]])
b = np.array([[5, 6],
              [7, 8]])

print("a * b  (elementwise):"); print(a * b)
print()
print("a @ b  (matrix product):"); print(a @ b)
print()
print("np.matmul and np.dot agree with @ for 2-D:")
print("   matmul same:", np.array_equal(a @ b, np.matmul(a, b)))
print()
print("Order matters - matrix multiplication is not commutative:")
print("   a@b == b@a :", np.array_equal(a @ b, b @ a))'''),

        ("Shapes must line up in the middle",
         "(m,k) @ (k,n) -> (m,n). The inner dimensions cancel.",
         '''import numpy as np

a = np.ones((2, 3))
b = np.ones((3, 4))
print("(2,3) @ (3,4) ->", (a @ b).shape, " the 3s cancel")

try:
    a @ np.ones((2, 4))
except ValueError as e:
    print("(2,3) @ (2,4) -> ValueError")
    print("   ", str(e)[:88])

print()
print("A 1-D array is treated as whichever vector makes the shapes work:")
v = np.array([1, 1, 1])
print("   (2,3) @ (3,)  ->", (a @ v).shape, "matrix times column vector")
print("   (3,)  @ (3,4) ->", (v @ b).shape, "row vector times matrix")'''),

        ("Solving a system: A x = b",
         "<code>solve</code> is the answer. Not <code>inv</code>.",
         '''import numpy as np

# 2x + y = 11
#  x + 3y = 18
A = np.array([[2.0, 1.0],
              [1.0, 3.0]])
b = np.array([11.0, 18.0])

x = np.linalg.solve(A, b)
print("solution x, y :", np.round(x, 6))
print("check A @ x   :", np.round(A @ x, 6), "== b")
print()
print("the inverse route gives the same answer here:")
print("   inv(A) @ b :", np.round(np.linalg.inv(A) @ b, 6))
print()
print("but solve is faster and numerically better - see the next step.")'''),

        ("Why inverting is the wrong habit",
         "It costs more and loses precision, and on a near-singular matrix it loses "
         "a lot.",
         '''import numpy as np

# A Hilbert matrix: famously ill-conditioned, and we know the true answer.
n = 12
H = 1.0 / (np.arange(n)[:, None] + np.arange(n)[None, :] + 1)
x_true = np.ones(n)
b = H @ x_true

x1 = np.linalg.solve(H, b)
x2 = np.linalg.inv(H) @ b

e1 = float(np.abs(x1 - x_true).max())
e2 = float(np.abs(x2 - x_true).max())
print("condition number : %.2e  <- badly conditioned" % np.linalg.cond(H))
print()
print("error with solve : %.3e" % e1)
print("error with inv   : %.3e" % e2)
print("inv is %.0fx worse" % (e2 / e1))
print()
print("Both answers should be all ones. Neither is, because the problem")
print("itself is unstable - but inv throws away noticeably more.")
print("Rule: if you are about to write inv(A) @ b, write solve(A, b).")'''),

        ("Determinant, rank and singular matrices",
         "How to tell whether a system has a unique solution before you trust one.",
         '''import numpy as np

good = np.array([[2.0, 1.0], [1.0, 3.0]])
bad  = np.array([[1.0, 2.0], [2.0, 4.0]])     # row 2 = 2 x row 1

for name, M in [("good", good), ("singular", bad)]:
    print("%-9s det=%8.4f  rank=%d" % (name, np.linalg.det(M),
                                       np.linalg.matrix_rank(M)))

print()
try:
    np.linalg.solve(bad, np.array([1.0, 2.0]))
except np.linalg.LinAlgError as e:
    print("solve(singular) ->", type(e).__name__, ":", e)
print()
print("But a determinant test is unreliable. This matrix is perfectly")
print("well behaved, and its determinant is nearly zero purely because")
print("the entries are small:")
tiny = 0.001 * np.eye(4)
print("   det  = %.1e  <- looks singular" % np.linalg.det(tiny))
print("   rank = %d of 4   <- it is not" % np.linalg.matrix_rank(tiny))
print("   cond = %.2f      <- and it is beautifully conditioned"
      % np.linalg.cond(tiny))
print()
print("Use matrix_rank to ask 'solvable?' and cond to ask 'trustworthy?'")'''),

        ("Norms, eigenvalues and least squares",
         "The three other things people actually reach for.",
         '''import numpy as np

v = np.array([3.0, 4.0])
print("norm (length)    :", float(np.linalg.norm(v)))
print("distance a to b  :", float(np.linalg.norm(np.array([1.0, 1.0]) - v)))

S = np.array([[2.0, 1.0],
              [1.0, 2.0]])
print()
print("symmetric matrix -> eigvalsh, ascending and real:")
print("   eigenvalues:", np.round(np.linalg.eigvalsh(S), 6))

print()
print("least squares fit of y = m x + c:")
x = np.array([0.0, 1.0, 2.0, 3.0])
y = np.array([1.0, 3.1, 4.9, 7.0])
M = np.column_stack([x, np.ones_like(x)])
sol = np.linalg.lstsq(M, y, rcond=None)[0]
print("   slope %.4f  intercept %.4f" % (sol[0], sol[1]))'''),
    ],
    [
        "<code>@</code> is matrix multiplication; <code>*</code> is elementwise. Both are legal on the same arrays, so nothing warns you when you pick the wrong one.",
        "Shapes must agree in the middle: <code>(m,k) @ (k,n)</code> gives <code>(m,n)</code>.",
        "A 1-D array is promoted to whichever vector orientation makes the multiplication valid.",
        "To solve <code>Ax = b</code>, use <code>np.linalg.solve</code> &mdash; never <code>inv(A) @ b</code>. It is faster and numerically better.",
        "<code>matrix_rank</code> and <code>cond</code> tell you whether a system is solvable; testing <code>det == 0</code> in floating point does not.",
        "<code>norm</code> for lengths and distances, <code>eigvalsh</code> for symmetric matrices, <code>lstsq</code> for fitting.",
    ],
    '''
title: Linear Algebra
intro: Matrix multiplication, solving systems, and why you should almost never invert a matrix.

## @ versus *

`*` is elementwise. `@` is matrix multiplication.

Both are valid on two square matrices of the same size, and they give completely different answers. Nothing raises, nothing warns, and the result of the wrong one is a plausible-looking matrix of the right shape.

This is the most common linear algebra bug in NumPy code, and it survives review easily because both lines look correct.

`np.matmul` is the function form of `@`, and `np.dot` agrees with it for 2-D. They diverge for higher dimensions &mdash; `matmul` broadcasts the leading axes and treats the last two as matrices, `dot` does something different and rarely what you want. Prefer `@` or `matmul`.

## Shapes

`(m, k) @ (k, n)` gives `(m, n)`. The inner dimensions must match and they cancel.

A 1-D array is special-cased: it is promoted to whichever orientation makes the multiplication valid, and then the added dimension is removed from the result. `(2,3) @ (3,)` gives `(2,)`, treating the vector as a column; `(3,) @ (3,4)` gives `(4,)`, treating it as a row.

That convenience means you rarely need to reshape vectors, but it also means a shape error can come from a vector being the wrong length rather than the wrong orientation. The error message names both shapes, which is usually enough.

## Solving systems

To solve `Ax = b`, use `np.linalg.solve(A, b)`.

The obvious alternative, `np.linalg.inv(A) @ b`, gives the same answer on well-behaved problems and is wrong as a habit for two reasons.

**Cost.** Computing an inverse is roughly the work of solving the system `n` times. `solve` factors the matrix once and does one back-substitution.

**Accuracy.** The inverse introduces rounding error, and then multiplying by it introduces more. `solve` avoids forming the inverse at all. On a well-conditioned matrix the difference is small; on an ill-conditioned one it is the difference between a usable answer and noise.

The rule is simple enough to apply without thinking: if you are about to write `inv(A) @ b`, write `solve(A, b)`.

Genuine uses for `inv` exist &mdash; you need the inverse itself, for a covariance matrix or an analytical derivation &mdash; but they are rarer than the code you will see suggests.

## Is it solvable?

A singular matrix has no unique solution, and `solve` raises `LinAlgError`.

The instinct is to check `det(A) == 0` first. Do not. Determinants of floating-point matrices are almost never exactly zero, and the determinant scales badly &mdash; a well-conditioned matrix can have a tiny determinant simply because it is large.

`np.linalg.matrix_rank(A)` answers the question directly: full rank means solvable.

`np.linalg.cond(A)` measures how much the answer amplifies input error. A condition number near 1 is excellent; anything above roughly `1e10` means you should not trust the low-order digits of the result, whichever method produced it.

## Norms

`np.linalg.norm(v)` gives the Euclidean length of a vector, and `norm(a - b)` the distance between two points.

It takes an `axis`, so `norm(X, axis=1)` gives the length of every row at once &mdash; the usual way to compute distances for a whole dataset without looping.

Other norms are available via `ord`: `ord=1` for the sum of absolute values, `ord=np.inf` for the maximum.

## Eigenvalues

`np.linalg.eig` works on any square matrix and returns complex results in unspecified order.

For a **symmetric** matrix &mdash; which covers most cases that arise in practice, since covariance and Gram matrices are symmetric &mdash; use `eigh` or `eigvalsh`. They exploit the symmetry, are faster and more accurate, and return real eigenvalues in ascending order.

That determinism matters: code that indexes into the output of `eig` and assumes an order is relying on something not guaranteed.

## Least squares

`np.linalg.lstsq(M, y, rcond=None)` fits an overdetermined system &mdash; more equations than unknowns &mdash; by minimising squared error.

Building the design matrix with `column_stack` is the whole setup. For a straight line, the columns are `x` and a column of ones; the solution is slope and intercept.

Pass `rcond=None` explicitly to get the current behaviour and silence the future-warning about the old default.

## Batched matrix multiplication

`matmul` treats the **last two** axes as the matrix and broadcasts everything before them.

That makes `(batch, n, k) @ (batch, k, m)` a batch of matrix products, computed in one call with no loop. `(batch, n, k) @ (k, m)` also works, applying the same matrix to every item in the batch.

This is why the batch axis goes first by convention: it puts the matrix axes where `matmul` expects them, and the whole thing composes without transposes.

`np.dot` does not do this. On arrays with more than two dimensions it follows an older rule that is rarely what anyone wants. `@` and `matmul` are the ones to use.

Most of `np.linalg` also broadcasts over leading axes: `solve`, `inv`, `det` and the decompositions all accept a stack of matrices and return a stack of results.

## solve versus lstsq

`solve` requires a square matrix and gives the exact solution when one exists. It raises on a singular matrix.

`lstsq` handles rectangular systems and finds the solution minimising squared error. It also handles rank-deficient systems by returning the minimum-norm solution rather than raising.

For an overdetermined system &mdash; more equations than unknowns, which is what fitting a model to data looks like &mdash; `lstsq` is the right tool.

The tempting alternative is the normal equations: `solve(A.T @ A, A.T @ b)`. It gives the same answer in exact arithmetic and is numerically worse, because forming `A.T @ A` squares the condition number. A problem that was marginally conditioned becomes badly conditioned. `lstsq` uses an SVD-based approach that avoids this.

## SVD, and what it is for

`np.linalg.svd` factors any matrix into `U @ diag(s) @ Vt`.

The singular values `s` are the useful part for most practical purposes.

**Rank.** The number of singular values meaningfully above zero. This is what `matrix_rank` computes internally, and it is why rank is a more reliable singularity test than a determinant.

**Conditioning.** The ratio of largest to smallest singular value is the condition number.

**Dimensionality reduction.** Keeping the largest k singular values and their vectors gives the best rank-k approximation of the matrix. That is what PCA is, and truncated SVD is how it is computed.

**Pseudo-inverse.** `np.linalg.pinv` uses SVD to invert what can be inverted and ignore what cannot, which is how least squares handles rank deficiency.

`svd(a, full_matrices=False)` returns the economy version, which is smaller and usually what you want for a tall matrix.

## Other decompositions

`np.linalg.qr` factors into an orthogonal and an upper-triangular matrix. It is the numerically sound way to solve least squares by hand, and it is what many algorithms use internally.

`np.linalg.cholesky` factors a symmetric positive-definite matrix into a lower triangular factor times its transpose. It is roughly twice as fast as a general factorisation and is the standard tool for covariance matrices &mdash; sampling from a multivariate normal, or evaluating a Gaussian likelihood.

Cholesky **raises** if the matrix is not positive definite, which is a useful diagnostic in itself: a covariance matrix that fails Cholesky is telling you something is wrong with how it was estimated.

## Conditioning in practice

The condition number is the amplification factor from input error to output error.

A condition number of 10 means roughly one decimal digit lost. `1e8` means about eight, which on `float64`'s sixteen leaves eight. `1e16` means all of them, and the answer is noise regardless of the algorithm.

Two things follow.

**Check `cond` before trusting a solution** from a matrix built out of measured data. Nothing warns you.

**Ill-conditioning is a property of the problem, not the code.** No solver rescues a condition number of `1e16`. The fix is upstream: rescale variables so their magnitudes are comparable, remove collinear columns, or add regularisation &mdash; which is exactly what ridge regression does, and why it works.

Scaling is the most commonly overlooked of those. A design matrix with one column in metres and another in nanometres is badly conditioned for no reason other than units.

## What to reach for

**`@`** for products, including batched.

**`solve`** for square systems, never `inv`.

**`lstsq`** for fitting and overdetermined systems, never the normal equations.

**`eigvalsh` / `eigh`** for symmetric matrices, because `eig` returns complex values in unspecified order.

**`cholesky`** for covariance matrices.

**`svd`** when you need rank, conditioning, or a low-rank approximation.

**`cond` and `matrix_rank`** before believing any of it.

And for anything beyond this &mdash; sparse matrices, iterative solvers, specialised decompositions &mdash; SciPy's `scipy.linalg` and `scipy.sparse` extend the same interface and are where the rest of the toolkit lives.

## Common mistakes

**Using `*` where `@` was meant.** Both are legal on square matrices and give different answers of the same shape. Nothing warns. This is the most frequent linear algebra bug in NumPy code.

**Writing `inv(A) @ b`.** Slower and less accurate than `solve(A, b)`, for no benefit.

**Using the normal equations for least squares.** `solve(A.T @ A, A.T @ b)` squares the condition number. `lstsq` does not.

**Testing `det(A) == 0`.** Floating-point determinants are almost never exactly zero, and the determinant scales with the matrix. `matrix_rank` answers the question directly.

**Indexing into `eig` output assuming an order.** There is none. `eigh` and `eigvalsh` return ascending real values for symmetric matrices, which is what most code actually needs.

**Expecting `.T` to make a column vector.** On a 1-D array it does nothing. `v[:, None]`.

**Using `np.dot` on more than two dimensions.** It follows an older rule that is rarely what anyone wants. `@` or `matmul` broadcast the leading axes properly.

## Reading the shapes in an error

`matmul` errors name the "core dimensions", which are the last two axes.

"Input operand 1 has a mismatch in its core dimension 0" means the first of the last two axes of the second operand does not match what the first operand's last axis requires &mdash; the `k` in `(m,k) @ (k,n)`.

The diagnosis is to print both shapes and check which axis is supposed to be shared. Nearly always one of the two arrays is transposed relative to the intent, and the fix is a `.T` on the correct side rather than a reshape.

For a 1-D operand, remember it is promoted to whichever orientation makes the multiplication valid, so a shape error involving one usually means the wrong length rather than the wrong orientation.

## Where SciPy takes over

`np.linalg` covers the dense, general cases well. Several things sit just outside it.

**Sparse matrices.** `scipy.sparse` stores only nonzeros and has its own solvers. For a matrix that is mostly zeros &mdash; graphs, finite-element meshes, term-document matrices &mdash; the difference is not a constant factor but the difference between fitting in memory and not.

**Iterative solvers.** For very large systems, `scipy.sparse.linalg` offers methods that approximate a solution without factoring the matrix.

**More decompositions.** `scipy.linalg` has LU, Schur, banded and triangular solvers, and generally more options on the ones NumPy also provides.

**Matrix functions.** `expm` for the matrix exponential and friends live in SciPy.

The interfaces are deliberately similar, so moving across is usually a change of import rather than a change of approach.
''',
    [
        {"q": "What is the difference between `a * b` and `a @ b` for two 2x2 arrays?",
         "options": ["None", "* is elementwise, @ is matrix multiplication", "@ is elementwise", "* raises"],
         "answer": 1,
         "why": "Both are legal and give different answers of the same shape, with no warning. It is the most common linear algebra bug in NumPy code."},
        {"q": "Why prefer `np.linalg.solve(A, b)` over `np.linalg.inv(A) @ b`?",
         "options": ["solve is newer", "It is faster and numerically better - inv is roughly n solves plus extra rounding error", "inv is deprecated", "They differ in shape"],
         "answer": 1,
         "why": "solve factors once and back-substitutes. On an ill-conditioned matrix the accuracy gap is the difference between an answer and noise."},
        {"q": "How should you check whether a matrix is singular?",
         "options": ["det(A) == 0", "np.linalg.matrix_rank or cond", "A.sum() == 0", "try/except only"],
         "answer": 1,
         "why": "Floating-point determinants are almost never exactly zero, and a determinant can be tiny purely because the matrix is large."},
        {"q": "Why use `eigvalsh` rather than `eig` for a symmetric matrix?",
         "options": ["No reason", "It is faster, more accurate, and returns real eigenvalues in ascending order", "eig does not work", "It returns fewer values"],
         "answer": 1,
         "why": "`eig` returns complex values in unspecified order, so any code indexing its output is relying on something not guaranteed."},
    ],
)


# ---------------------------------------------------------------------------
# 18. NaN and missing data
# ---------------------------------------------------------------------------
topic(
    "nan_and_missing_data",
    "NaN and Missing Data",
    "Working with Data",
    "The value that is not equal to itself, and the family of functions that "
    "exist because of it.",
    _svg(_grid(20, 30, 4, 1, 15) +
         _box(50, 30, 15, 15, "#3a1f1f", "#a44") + _txt(57, 41, "?", "#e88", 9) +
         _arrow(96, 38, 112, 38) + _txt(134, 42, "nanmean", M, 8)),
    [
        ("NaN is a float, and it is not equal to itself",
         "Every comparison with NaN is False, including <code>nan == nan</code>.",
         '''import numpy as np

x = np.nan
print("np.nan is a", type(x).__name__)
print("nan == nan :", x == x, "<- False. This is the IEEE 754 rule.")
print("nan != nan :", x != x, "<- the only True comparison")
print("nan <  1   :", x < 1)
print("nan >  1   :", x > 1)
print()
print("So `arr == np.nan` never finds anything:")
a = np.array([1.0, np.nan, 3.0])
print("   a == np.nan :", a == np.nan)
print("   np.isnan(a) :", np.isnan(a), "<- use this")'''),

        ("NaN needs a float dtype",
         "There is no integer NaN, so introducing one promotes the whole array.",
         '''import numpy as np

a = np.array([1, 2, 3])
print("int array dtype:", a.dtype)
try:
    a[0] = np.nan
except ValueError as e:
    print("assigning nan ->", type(e).__name__, ":", str(e)[:52])

print()
b = a.astype(float)
b[0] = np.nan
print("after astype(float):", b, b.dtype)
print()
print("np.array([1, 2, np.nan]) is float from the start:")
print("   ", np.array([1, 2, np.nan]).dtype)
print()
print("This is why a column with one missing value becomes float,")
print("and why ids can end up printed as 1001.0")'''),

        ("One NaN poisons a whole reduction",
         "Silently, and the result still looks like a number.",
         '''import numpy as np

a = np.array([2.0, 4.0, np.nan, 8.0])

print("sum  :", float(a.sum()))
print("mean :", float(a.mean()))
print("max  :", float(a.max()))
print("   all nan - one missing value takes the lot")
print()
print("the nan-aware family ignores them instead:")
print("nansum  :", float(np.nansum(a)))
print("nanmean :", float(np.nanmean(a)))
print("nanmax  :", float(np.nanmax(a)))
print("nanstd  :", round(float(np.nanstd(a)), 4))
print()
print("nanmean divides by the count of REAL values, here 3 not 4.")'''),

        ("Finding and counting",
         "<code>isnan</code> gives a mask, and everything you already know about "
         "masks applies.",
         '''import numpy as np

a = np.array([[1.0, np.nan, 3.0],
              [np.nan, np.nan, 6.0],
              [7.0, 8.0, 9.0]])

print("total missing :", int(np.isnan(a).sum()))
print("per column    :", np.isnan(a).sum(axis=0))
print("per row       :", np.isnan(a).sum(axis=1))
print()
print("rows with no missing values:")
clean = a[~np.isnan(a).any(axis=1)]
print(clean, " shape", clean.shape)
print()
print("positions of the missing values:")
print("   ", list(zip(*[c.tolist() for c in np.where(np.isnan(a))])))'''),

        ("Filling: drop, constant, or interpolate",
         "Three strategies, and the choice matters more than the code.",
         '''import numpy as np

a = np.array([1.0, np.nan, np.nan, 4.0, 5.0])

print("original     :", a)
print("drop         :", a[~np.isnan(a)])
print("fill 0       :", np.nan_to_num(a))
print("fill mean    :", np.where(np.isnan(a), np.nanmean(a), a))

idx = np.arange(len(a))
good = ~np.isnan(a)
print("interpolate  :", np.round(np.interp(idx, idx[good], a[good]), 4))
print()
print("Filling with 0 changes the mean. Filling with the mean keeps it")
print("but shrinks the variance. Neither is neutral - pick deliberately.")'''),

        ("inf is a separate thing",
         "Division by zero gives infinity and a warning, not an exception.",
         '''import numpy as np

a = np.array([1.0, 0.0, -1.0])

with np.errstate(divide="ignore", invalid="ignore"):
    r = a / 0.0
print("a / 0 :", r, "<- inf, nan, -inf")
print()
print("isnan  :", np.isnan(r))
print("isinf  :", np.isinf(r))
print("isfinite:", np.isfinite(r), "<- the one that catches both")
print()
print("0/0 gives nan; 1/0 gives inf. They are different failures.")
print()
print("nan_to_num handles all three at once:")
print("   ", np.nan_to_num(r, nan=0.0, posinf=999.0, neginf=-999.0))'''),
    ],
    [
        "<code>np.nan != np.nan</code>. Every comparison with NaN is False, so <code>arr == np.nan</code> never matches &mdash; use <code>np.isnan</code>.",
        "NaN is a <strong>float</strong>. An integer array cannot hold one, so a single missing value promotes the whole column to float.",
        "One NaN makes <code>sum</code>, <code>mean</code> and <code>max</code> return NaN. The <code>nan*</code> family ignores them instead.",
        "<code>nanmean</code> divides by the count of real values, not the array length.",
        "<code>np.isnan(a).any(axis=1)</code> finds rows with missing data; <code>~</code> keeps the clean ones.",
        "<code>inf</code> is separate from NaN. <code>np.isfinite</code> is the check that catches both.",
    ],
    '''
title: NaN and Missing Data
intro: The value that is not equal to itself, and the functions that exist because of it.

## Not equal to itself

`np.nan` is a floating-point value defined by the IEEE 754 standard to represent "not a number". Its defining property is that **every comparison involving it is False**, including equality with itself.

`nan == nan` is False. `nan < 1` is False. `nan > 1` is False. The only comparison that returns True is `!=`, and only because it is the negation of a False.

The immediate practical consequence: `arr == np.nan` gives an all-False mask, no matter how many NaNs the array contains. It fails silently, which is the worst way to fail.

`np.isnan(arr)` is the correct test, and it returns a proper boolean mask.

The rule is not a NumPy quirk. It falls out of NaN meaning "the result of an undefined operation" &mdash; two undefined results have no reason to be the same thing.

## NaN is a float

There is no integer NaN. The integer types have no bit pattern reserved for it.

So assigning `np.nan` into an integer array raises, and any array literal containing `np.nan` comes out as float.

This is why a table column with one missing value silently becomes float, and why identifiers end up displayed as `1001.0` instead of `1001`. There is no way around it within a plain NumPy integer array; the options are to accept float, to use a sentinel value like `-1` and document it, or to carry a separate boolean mask alongside the data.

Pandas addresses this with nullable integer types. Plain NumPy does not have them.

## One NaN poisons everything

`a.sum()` on an array containing a single NaN returns NaN. So does `mean`, `max`, `min`, `std` and every other reduction.

This is correct &mdash; the sum genuinely is unknown &mdash; but it is dangerous, because the result is still a number-shaped thing that flows onward through the pipeline and turns everything downstream into NaN too. By the time you notice, the origin can be far away.

The `nan*` family exists for this: `nansum`, `nanmean`, `nanmax`, `nanmin`, `nanstd`, `nanmedian`, `nanpercentile`. Each ignores missing values rather than propagating them.

Note what `nanmean` does: it divides by the count of **real** values. On four elements with one NaN, it divides by three. That is usually right, and it is worth being explicit that it is a decision rather than a technicality &mdash; you are asserting that the missing value is missing at random.

`nansum` of an all-NaN array returns 0, while `nanmean` of one returns NaN with a warning. Those are different and defensible choices, and both are worth knowing before you rely on either.

## Finding them

`np.isnan(a)` gives a mask, and everything from the masking module applies.

`np.isnan(a).sum()` counts them. With `axis`, it counts per row or per column, which is the first thing to look at when data arrives.

`np.isnan(a).any(axis=1)` flags rows containing any missing value, and `~` inverts it to keep the complete ones. That is listwise deletion in one line.

`np.where(np.isnan(a))` gives the coordinates, which is what you want when you need to know *where* rather than *how many*.

## Filling

Three broad strategies, and the choice is a statistical decision rather than a coding one.

**Drop.** `a[~np.isnan(a)]` for a vector, or the row-wise version above for a table. Simple and unbiased if the data really is missing at random; throws away potentially a lot if it is not.

**Constant.** `np.nan_to_num(a)` replaces with zero; `np.where(np.isnan(a), value, a)` with anything else. Filling with zero shifts the mean. Filling with the mean preserves the mean but shrinks the variance, which quietly misleads anything downstream that cares about spread.

**Interpolate.** `np.interp` fills from neighbouring values, which is the right choice for ordered data like a time series where adjacency is meaningful.

None of these is neutral. Every one of them puts numbers into your data that were not measured, and the honest thing is to record which you used.

## inf is different

Dividing by zero does not raise in NumPy. It produces `inf`, `-inf` or `nan`, and emits a RuntimeWarning.

`1/0` gives `inf`. `0/0` gives `nan`. They come from different failures and are worth distinguishing.

`np.isnan` does not catch `inf`. `np.isinf` does not catch NaN. `np.isfinite` catches both, and is usually the check you actually want when validating data.

`np.errstate` is the context manager for suppressing the warnings when the behaviour is intentional. `np.nan_to_num` replaces NaN and both infinities in one call, with separate arguments for each.

## Three ways to represent missing, and their costs

**NaN.** Works only for floats. Propagates automatically through arithmetic, which is both the safety feature and the hazard. Supported by the whole `nan*` family and understood by every library.

**A sentinel value.** `-1` for a count, `-999` for a measurement. Works for integers, costs nothing, and is entirely a convention &mdash; nothing stops the sentinel being treated as data by code that does not know about it. Every such bug is silent and produces plausible numbers.

**A separate boolean mask.** Explicit, works for any dtype, and never gets mistaken for data. Costs a byte per element and requires every operation to be written mask-aware, which is the reason it is not more common.

`np.ma` packages the third option, and pandas' nullable dtypes package a version of it with better ergonomics.

For plain NumPy, NaN is the default answer for floats, and a documented sentinel is the pragmatic answer for integers when converting to float is not acceptable. The important part is documenting it &mdash; a sentinel that is not written down anywhere is a bug waiting for a new maintainer.

## Comparing arrays that contain NaN

`np.array_equal(a, b)` returns False if either contains NaN, because NaN never equals anything &mdash; including the NaN in the same position of the other array.

That makes it useless for checking that a computation reproduced a result, which is exactly when you want it.

`np.array_equal(a, b, equal_nan=True)` treats NaNs in matching positions as equal.

`np.allclose(a, b, equal_nan=True)` does the same with a tolerance, and is what belongs in a test comparing floating-point results.

Both are worth reaching for by default in test code, because a NaN appearing in both arrays is usually the expected outcome rather than a failure.

## NaN in sorting and extremes

`np.sort` places NaN at the **end**, on the grounds that it compares greater than everything. That is a convention rather than a consequence, since NaN comparisons are all False.

`np.argmax` and `np.max` return NaN if any element is NaN, which is consistent with the reductions but means a single missing value hides the real maximum. `np.nanargmax` and `np.nanmax` skip them.

`np.nanargmax` **raises** on an all-NaN slice rather than returning something meaningless, which is the right behaviour and worth catching in code that reduces over groups that might be entirely missing.

`np.median` propagates NaN; `np.nanmedian` does not.

The pattern is consistent: the plain function propagates, the `nan` version skips, and the `nan` version has an opinion about the all-missing case.

## Tracking a NaN back to its source

The hard part of NaN debugging is that the value flows a long way from where it was created.

The single most effective tool is `np.errstate(all="raise")`, which converts the operation that *produces* an invalid result into an exception. The traceback then points at the division by zero or the square root of a negative number, rather than at the reduction three functions later that returned NaN.

Failing that, bisect: check `np.isfinite(x).all()` at a few points in the pipeline and narrow down where it first goes false.

The usual origins are worth knowing, because one of them is almost always it: division by zero, `log` of zero or a negative, `sqrt` of a negative, `0 * inf`, `inf - inf`, and an out-of-domain trigonometric inverse where a value drifted just past 1 through rounding. That last one is a classic &mdash; a cosine similarity computed as 1.0000000002 and passed to `arccos` gives NaN, and `np.clip(x, -1, 1)` is the fix.

## Deciding what to do about missing data

The code is easy; the decision is not, and it is a decision about the data rather than about NumPy.

**Why is it missing?** Missing at random can be dropped or imputed without bias. Missing because of the value itself &mdash; a sensor that fails at extremes, a survey question people skip when the answer is embarrassing &mdash; cannot. Dropping those rows biases the result, and imputing them with a mean biases it differently.

**How much is missing?** A handful of rows out of a hundred thousand can be dropped without much thought. Thirty percent cannot, and the choice of imputation becomes a modelling decision that should be stated.

**What does downstream care about?** A mean is robust to mean-imputation by construction. A variance is not &mdash; filling with the mean shrinks it, and anything relying on spread will be quietly wrong.

**Is the missingness itself informative?** Often it is, and adding a boolean "was missing" column preserves that information rather than discarding it.

Whatever you choose, count them first and record what you did. `np.isnan(a).sum(axis=0)` at the point data arrives takes one line and prevents a surprising number of downstream mysteries.

## Validating data as it arrives

The cheapest defence against NaN problems is checking at the boundary, where the data enters the program.

`np.isfinite(a).all()` answers "is any of this NaN or infinite" in one call, and is the right single check because it catches both.

`np.isnan(a).sum(axis=0)` gives the count per column, which turns "there is missing data somewhere" into "column 3 is 40% empty" &mdash; a far more actionable statement.

Doing this at load time, and failing or logging rather than proceeding silently, converts a class of mysterious downstream results into an immediate, located error. It costs one line.

## NaN and boolean logic

`np.isnan` requires a float dtype. Calling it on an integer or string array raises a TypeError rather than returning all-False, which surprises people writing generic code.

`np.isnan(a)` on an **object** array also fails, because the elements may not be numbers at all.

For code that must handle any dtype, guard with `np.issubdtype(a.dtype, np.floating)` first, or use `pd.isna` from pandas, which handles every case including None and NaT.

## Comparisons involving NaN, in filtering

Because every comparison with NaN is False, NaN values fail every condition &mdash; including the negation of a condition.

`a[a > 0]` excludes them. `a[a <= 0]` also excludes them. Two filters that look like an exhaustive partition silently drop rows.

Any place where a dataset is split into groups by a numeric condition is a place to ask what happens to the missing values, and to add an explicit `np.isnan` branch if they should be handled rather than lost.

## The summary

`np.isnan` to find them, never `== np.nan`.

`np.isfinite` to validate, because it catches infinities too.

The `nan*` family to reduce over them, remembering that skipping is a decision about the data.

`np.errstate(all="raise")` to find where one was created, which is the single most effective debugging tool here.

`equal_nan=True` on `allclose` and `array_equal` when comparing results that legitimately contain them.

`np.clip` before `arccos` and similar, to stop rounding drift producing NaN from valid data.

And at the start of everything: count them, record what you did about them, and prefer being explicit over letting a fill value pass silently into an analysis that assumes it was measured.
''',
    [
        {"q": "Why does `arr == np.nan` never find anything?",
         "options": ["It is a syntax error", "Every comparison with NaN is False, including equality with itself", "np.nan is None", "It only works on floats"],
         "answer": 1,
         "why": "IEEE 754 defines NaN as the result of an undefined operation, and two undefined results have no reason to be equal. Use np.isnan."},
        {"q": "What happens when you assign `np.nan` into an integer array?",
         "options": ["It works", "It stores 0", "It raises - there is no integer NaN", "The array becomes float automatically"],
         "answer": 2,
         "why": "No integer type has a bit pattern for NaN, which is why a column with one missing value becomes float and ids print as 1001.0"},
        {"q": "What does `a.mean()` return if `a` contains one NaN?",
         "options": ["The mean of the rest", "NaN", "0", "An error"],
         "answer": 1,
         "why": "Correct but dangerous - the NaN flows onward and turns everything downstream into NaN, far from where it started. Use nanmean."},
        {"q": "Which check catches both NaN and infinity?",
         "options": ["np.isnan", "np.isinf", "np.isfinite", "np.isreal"],
         "answer": 2,
         "why": "isnan misses inf and isinf misses NaN. isfinite is usually the one you want when validating data."},
    ],
)


# ---------------------------------------------------------------------------
# 19. Performance and memory
# ---------------------------------------------------------------------------
topic(
    "performance_and_memory",
    "Performance and Memory",
    "Working with Data",
    "Where the time and the bytes actually go, and the handful of changes that "
    "move the needle.",
    _svg(_box(18, 30, 52, 30, S, A) + _txt(44, 49, "float64", A, 8) +
         _arrow(74, 45, 90, 45) +
         _box(98, 34, 34, 22, S, M) + _txt(115, 49, "f32", M, 8)),
    [
        ("dtype is the cheapest saving there is",
         "Half the width, half the memory, and usually faster because less has to "
         "travel.",
         '''import numpy as np

n = 200_000
for dt in [np.float64, np.float32, np.int64, np.int32, np.int8, np.bool_]:
    a = np.ones(n, dtype=dt)
    print("%-9s itemsize %d  total %6.2f MB"
          % (np.dtype(dt).name, a.itemsize, a.nbytes / 1e6))
print()
print("float32 halves a float64 array and keeps ~7 significant digits.")
print("For measurements that came from a sensor with 3, that is plenty.")'''),

        ("Temporaries are the hidden cost",
         "Every intermediate expression allocates a full-size array you never see.",
         '''import numpy as np
import time

a = np.random.default_rng(0).random(1_000_000)

t = time.perf_counter()
b = a * 2 + 1          # allocates (a*2), then allocates the result
r1 = time.perf_counter() - t

c = a.copy()
t = time.perf_counter()
c *= 2                 # no allocation at all
c += 1
r2 = time.perf_counter() - t

print("a * 2 + 1      : %.4f s  (2 temporary arrays)" % r1)
print("in place *= +=  : %.4f s  (0)" % r2)
print("same answer     :", np.allclose(b, c))
print()
print("Each temporary here is 8 MB. On a chain of five operations")
print("that is 40 MB of allocation for one line of arithmetic.")'''),

        ("out= writes into memory you already have",
         "The explicit form of the same idea, and it works with any ufunc.",
         '''import numpy as np

a = np.arange(6, dtype=float)
dest = np.empty_like(a)

np.multiply(a, 3, out=dest)
print("dest after multiply:", dest)

np.add(dest, 1, out=dest)
print("dest after add     :", dest, "<- read and written in one buffer")
print()
print("useful in a loop where the destination is reused:")
acc = np.zeros(4)
for row in np.arange(12, dtype=float).reshape(3, 4):
    np.add(acc, row, out=acc)
print("   accumulated:", acc)'''),

        ("Strided access costs more than contiguous access",
         "Same number of bytes, same result - only the order they are read in "
         "differs.",
         '''import numpy as np
import time

def best(fn, reps=5):
    b = 1e9
    for _ in range(reps):
        t = time.perf_counter(); fn(); b = min(b, time.perf_counter() - t)
    return b

a = np.ones((1200, 1200))

t1 = best(lambda: a.copy())                     # consecutive bytes
t2 = best(lambda: np.ascontiguousarray(a.T))    # jumps a row every element

print("copy of a          : %.5f s" % t1)
print("copy of a.T        : %.5f s" % t2)
print("strided is %.1fx slower" % (t2 / t1))
print()
print("Both move 11 MB and produce 11 MB. The transpose reads one value")
print("from each row in turn, so almost every read is a cache miss.")
print()
print("Reductions are not a good test of this - NumPy blocks them so both")
print("directions run at similar speed. It shows up when data is MOVED.")'''),

        ("Preallocate instead of growing",
         "The same lesson as concatenating in a loop, stated as a habit.",
         '''import numpy as np
import time

n = 3000

t = time.perf_counter()
grow = np.array([])
for i in range(n):
    grow = np.append(grow, i)
t1 = time.perf_counter() - t

t = time.perf_counter()
pre = np.empty(n)
for i in range(n):
    pre[i] = i
t2 = time.perf_counter() - t

t = time.perf_counter()
best = np.arange(n, dtype=float)
t3 = time.perf_counter() - t

print("np.append in a loop : %.4f s" % t1)
print("preallocated        : %.4f s" % t2)
print("vectorised          : %.6f s" % t3)
print("all equal           :", np.array_equal(grow, pre) and np.array_equal(pre, best))'''),

        ("Measuring rather than guessing",
         "<code>nbytes</code> for size, and a timing loop for anything you are about "
         "to optimise.",
         '''import numpy as np
import time

a = np.ones((500, 500))
print("shape %s dtype %s" % (a.shape, a.dtype))
print("nbytes    : %.2f MB" % (a.nbytes / 1e6))
print("as float32: %.2f MB" % (a.astype(np.float32).nbytes / 1e6))
print()

def timeit(fn, reps=5):
    best = 1e9
    for _ in range(reps):
        t = time.perf_counter(); fn(); best = min(best, time.perf_counter() - t)
    return best

print("sqrt   : %.5f s" % timeit(lambda: np.sqrt(a)))
print("a ** 2 : %.5f s" % timeit(lambda: a ** 2))
print("a * a  : %.5f s" % timeit(lambda: a * a))
print()
print("Take the BEST of several runs, not the average - the slow runs")
print("are measuring the machine, not the code.")'''),
    ],
    [
        "Choosing <code>float32</code> over <code>float64</code> halves memory and usually speeds things up, because less data has to move.",
        "Every intermediate expression allocates a full-size temporary array. <code>a * 2 + 1</code> allocates twice.",
        "In-place operators (<code>*=</code>, <code>+=</code>) and <code>out=</code> reuse memory you already have.",
        "C order makes the <strong>last</strong> axis contiguous. Reading strided memory (copying a transpose) is several times slower than reading consecutive bytes.",
        "Preallocate with <code>np.empty</code> and assign, rather than growing an array &mdash; <code>np.append</code> in a loop is quadratic.",
        "Measure with <code>nbytes</code> and a timing loop, and take the <strong>best</strong> of several runs rather than the average.",
    ],
    '''
title: Performance and Memory
intro: Where the time and the bytes actually go.

## The order to try things

Most NumPy performance work comes down to four questions, roughly in order of payoff:

1. Is there still a Python loop? Removing it is worth 10&ndash;100x.
2. Is the dtype larger than it needs to be? Halving it is worth up to 2x, and halves memory.
3. Are temporaries being allocated in a hot path? In-place operations remove them.
4. Is the memory access pattern fighting the cache? Layout changes can be worth 2&ndash;5x.

The first is covered in the introductory module and dwarfs the rest. This module is about the other three, which matter once the obvious loop is gone.

## dtype

`float64` is the default and is often more precision than the data justifies. Sensor readings good to three significant figures do not benefit from fifteen.

`float32` keeps about seven significant digits, halves the memory, and typically runs faster &mdash; not because the arithmetic is cheaper, but because half as much data has to travel from memory to the processor, and memory bandwidth is usually the limit.

The same applies to integers. An array of small counts does not need `int64`. An array of flags should be `bool_`, which is one byte, not `int64`, which is eight.

The caution from the dtypes module still applies: narrow integers overflow silently. Choose the smallest type that cannot overflow for your actual data, not the smallest that happens to fit today's sample.

## Temporaries

`a * 2 + 1` on a million-element array does not do one pass. It allocates an 8 MB temporary for `a * 2`, then allocates another 8 MB for the final result, then frees the first.

You never see them, and for a single expression it rarely matters. In a loop, or in a chain of five operations on a large array, the allocation and the extra memory traffic dominate.

Two ways to avoid it.

**In-place operators.** `a *= 2` modifies the existing buffer and allocates nothing. Remember that it also modifies anything sharing that buffer, which is the views-versus-copies problem again.

**`out=`.** Every ufunc accepts `out`, which names the destination explicitly. `np.multiply(a, 3, out=dest)` writes into `dest`, and `out` may be one of the inputs. This is the clearest form when you are accumulating into a buffer across iterations.

Neither is worth doing everywhere. `a * 2 + 1` is more readable than two statements, and readability wins until you have measured that this line matters.

## Layout and the cache

A C-ordered array stores the **last** axis contiguously. Consecutive elements along that axis sit next to each other in memory.

Processors fetch memory in cache lines, so reading consecutive bytes is far cheaper than jumping a row at a time.

Reductions are a poor demonstration of this. NumPy blocks them internally, so `sum(axis=0)` and `sum(axis=1)` usually run at similar speed and sometimes in the order you would not predict. It is worth knowing that, because the "always reduce along the last axis" advice is repeated widely and does not survive measurement.

Where it shows clearly is when data is actually **moved**. Copying a `(1200, 1200)` array and copying its transpose move the same number of bytes and produce the same number of bytes, but the transpose reads one value from each row in turn, and runs several times slower.

Two practical consequences. If you have a choice about which axis holds the thing you iterate over, put it last. And if you are about to make many strided passes over the same data, one `np.ascontiguousarray` up front can pay for itself &mdash; a single copy against many slow reads.

## Preallocation

`np.append` and `np.concatenate` do not append. They allocate a new array and copy everything. In a loop that is quadratic, and it is the single most common accidental slowdown in NumPy code after the plain Python loop.

If you know the final size, `np.empty(n)` and assignment by index is the direct answer. `np.empty` does not initialise, so it is faster than `np.zeros` when you are going to overwrite everything &mdash; and dangerous if you are not, because the contents are whatever was in that memory.

If you do not know the size, collect into a Python list and convert once at the end. Lists are designed for growth; arrays are not.

## Measuring

Guessing is unreliable, and the intuitions transferred from pure Python are often wrong.

`a.nbytes` gives the real size of the data. `a.itemsize` gives the per-element cost.

For time, run the operation several times and take the **minimum**, not the mean. The slow runs are measuring interference from the rest of the machine; the fastest run is the closest estimate of the actual cost. A single timed run of a fast operation measures mostly noise.

And measure the thing you intend to change. Optimising an operation that accounts for 2% of the runtime is effort spent for a 2% ceiling, however satisfying the local speedup looks.

## Views and memory that will not go away

A view holds a reference to the array it came from, so the entire base buffer stays alive as long as the view does.

Extract one row from an 8 MB array, keep it, and you are keeping 8 MB.

This is the most common source of NumPy memory that never comes back, and it is invisible &mdash; `row.nbytes` reports four kilobytes while the process holds eight megabytes.

The fix is `copy()` at the point you decide to keep something small from something large. The cost is one small allocation; the saving is the whole base.

`a.base` shows what a view derives from, and `a.base.nbytes` shows what is actually being held. That is the diagnostic when memory in a long-running process grows without an obvious cause.

## Threads and the GIL

NumPy releases the GIL during most array operations, which means threads genuinely run in parallel inside a NumPy computation &mdash; unlike most pure Python code.

That makes `concurrent.futures.ThreadPoolExecutor` a real option for parallelising array work, with none of the pickling and process-startup costs of multiprocessing.

Two caveats. Operations that touch Python objects &mdash; object arrays, anything calling back into Python &mdash; do not release it. And BLAS routines are usually already multi-threaded internally, so adding your own threads on top can oversubscribe the machine and run slower. `OMP_NUM_THREADS` and `threadpoolctl` control that layer.

Measure before assuming threading helps. For large matrix operations it often does nothing, because BLAS was already using every core.

## Chunking

When an operation would allocate more than fits in memory, the answer is usually to do it in pieces.

The classic case is a pairwise distance matrix. For 100,000 points, the intermediate is 10 billion entries and no machine will hold it. Processing 1,000 rows at a time keeps the intermediate at 100 million and gives the same answer.

The general shape:

```python
for start in range(0, n, chunk):
    block = data[start:start + chunk]
    out[start:start + chunk] = expensive(block)
```

The slices are views, so the chunking itself allocates nothing, and the output is preallocated once.

This is one of the cases where a loop is correct. The loop runs `n / chunk` times, not `n` times, so the interpreter overhead is negligible and the memory ceiling is the thing being controlled.

## When to reach past NumPy

NumPy has a ceiling, and recognising it saves effort spent optimising against it.

**Numba** compiles a Python function to machine code with a decorator. It is the right answer for genuinely sequential algorithms &mdash; the ones that cannot be vectorised &mdash; and often gets within range of C for a few lines of change.

**Cython** gives more control at the cost of a build step, and is what several scientific libraries use internally.

**SciPy** already contains a compiled implementation of a great many things people write by hand: distance matrices, sparse matrices, signal filters, optimisation, interpolation. Checking whether SciPy has it is cheaper than writing it.

**Dask** handles arrays larger than memory with a NumPy-like interface, splitting work into chunks automatically.

**CuPy / PyTorch** move the work to a GPU, with an interface close enough to NumPy that porting is often mechanical. Worth it for large array workloads, not worth it for small ones where the transfer cost dominates.

The order to consider them: is it vectorisable in NumPy, is it in SciPy, is it sequential and worth Numba, is it too big for memory, is it big enough for a GPU.

## Profiling before optimising

The instinct about where time goes is unreliable, and array code is no exception.

`cProfile` gives function-level timings and finds the hot function. `line_profiler` gives per-line timings within it, which is what you actually need when one function contains the whole computation.

`memory_profiler` tracks allocation line by line, and `a.nbytes` summed over the arrays you are holding is a quick manual version.

Two rules make profiling worth the time.

**Profile the real workload.** A toy input can have completely different characteristics &mdash; different cache behaviour, different branch of the algorithm, different memory pressure.

**Fix the top item, then measure again.** The bottleneck moves. Optimising the second item on the original list is often wasted, because after the first fix it is no longer second.

And keep the ceiling in view: a function taking 5% of runtime cannot give more than a 5% improvement however completely you optimise it.

## Where the wins actually are, in order

**Remove the Python loop.** 10&ndash;100x, and it dominates everything else. If a loop over elements is still there, nothing below this line matters yet.

**Avoid quadratic growth.** `np.append` or `concatenate` in a loop turns a linear job into a quadratic one. The fix is preallocation or a list.

**Right-size the dtype.** Up to 2x on bandwidth-bound work, and it halves memory.

**Remove temporaries in hot paths.** In-place operators and `out=`. Worth doing where measurement says it matters, not everywhere.

**Fix access patterns.** Contiguity, and avoiding repeated strided gathers.

**Reach past NumPy.** Numba, SciPy, a GPU &mdash; when the algorithm genuinely does not vectorise or the data genuinely does not fit.

Working down that list in order means the large wins come first, and it avoids the common trap of micro-optimising an expression inside a loop that should not exist.

## Things that look slow and are not

**Slicing.** A view. Free, whatever the array size.

**Transposing.** A view. Free.

**Reshaping a contiguous array.** A view. Free.

**Reversing with `[::-1]`.** A view. Free.

**Broadcasting the inputs.** No allocation; the strides are set to zero. The *output* is allocated, which is a different thing.

Rewriting any of these to "avoid the copy" is effort spent on a copy that was never happening. Confirm with `np.shares_memory` before optimising something that may already be free.

## Things that look cheap and are not

**Boolean masking and fancy indexing.** Both allocate, and both gather from scattered positions.

**`astype`.** Allocates a full second array, even when the dtype is unchanged, unless `copy=False`.

**Chained expressions on large arrays.** Every intermediate is a full-size allocation.

**`np.append`.** Not an append. A full copy, every call.

**Keeping a small view of a large array.** Holds the whole base alive.

## The discipline

Measure before optimising, and profile the real workload rather than a small stand-in &mdash; cache behaviour and memory pressure do not scale down predictably.

Take the minimum of several timed runs, not the mean.

Fix the top item and measure again, because the bottleneck moves.

Keep the ceiling in view: an operation taking 5% of the runtime cannot yield more than 5%, however thoroughly it is optimised.

And weigh readability honestly. A vectorised one-liner that nobody can safely modify has a maintenance cost that does not show up in a benchmark, and the version a colleague can read is often the better engineering answer even when it is slower.
''',
    [
        {"q": "Why is `float32` often faster than `float64`, not just smaller?",
         "options": ["The arithmetic is simpler", "Half as much data has to move, and memory bandwidth is usually the limit", "It skips rounding", "It is not faster"],
         "answer": 1,
         "why": "Most array operations are bandwidth-bound rather than compute-bound, so halving the bytes roughly halves the time."},
        {"q": "How many temporary arrays does `a * 2 + 1` allocate?",
         "options": ["None", "One, for a*2, plus the result", "Three", "It depends on dtype"],
         "answer": 1,
         "why": "On a million float64 elements that is 8 MB you never see. In-place operators or `out=` remove them - but only bother once you have measured that the line matters."},
        {"q": "Copying an array and copying its transpose move the same bytes. Why is the transpose slower?",
         "options": ["Transposing itself is slow", "It reads one value from each row in turn, so almost every read is a cache miss", "It uses more memory", "It is not slower"],
         "answer": 1,
         "why": "Processors fetch cache lines, so consecutive reads are far cheaper than jumping. Reductions are a poor test of this - NumPy blocks them and both directions run at similar speed."},
        {"q": "When timing an operation, should you take the mean or the minimum of several runs?",
         "options": ["Mean", "Minimum", "Maximum", "A single run"],
         "answer": 1,
         "why": "Slow runs measure interference from the rest of the machine. The fastest run is the closest estimate of the actual cost."},
    ],
)


# ---------------------------------------------------------------------------
# 20. Saving and loading
# ---------------------------------------------------------------------------
topic(
    "saving_and_loading",
    "Saving and Loading Arrays",
    "Working with Data",
    "npy, npz, text and bytes - which format to use, and the security footgun in "
    "the middle of it.",
    _svg(_grid(18, 30, 3, 2, 14) +
         _arrow(66, 44, 84, 44) + _txt(75, 36, "save", A, 7) +
         _box(94, 26, 40, 36, S, M) + _txt(114, 48, ".npy", M, 9)),
    [
        (".npy keeps dtype and shape exactly",
         "The native format. It round-trips anything a plain array can hold.",
         '''import numpy as np, tempfile, os

a = np.arange(12, dtype=np.int16).reshape(3, 4)
path = os.path.join(tempfile.mkdtemp(), "a.npy")

np.save(path, a)
b = np.load(path)

print("saved  :", a.dtype, a.shape)
print("loaded :", b.dtype, b.shape)
print("identical:", np.array_equal(a, b) and a.dtype == b.dtype)
print()
print("file size:", os.path.getsize(path), "bytes")
print("   = 12 values x 2 bytes +", os.path.getsize(path) - 24, "byte header")
print()
print("np.save appends .npy if you leave it off.")'''),

        ("npz bundles several arrays",
         "Named, lazily loaded, and optionally compressed.",
         '''import numpy as np, tempfile, os

d = tempfile.mkdtemp()
path = os.path.join(d, "bundle.npz")

np.savez(path, train=np.arange(6), labels=np.array([0, 1, 0, 1, 0, 1]))

with np.load(path) as z:
    print("keys  :", list(z.files))
    print("train :", z["train"])
    print("labels:", z["labels"])

cpath = os.path.join(d, "small.npz")
big = np.zeros((500, 200))
np.savez(path, big=big)
np.savez_compressed(cpath, big=big)
print()
print("uncompressed: %7d bytes" % os.path.getsize(path))
print("compressed  : %7d bytes" % os.path.getsize(cpath))
print("   zeros compress well; real data much less so.")'''),

        ("Text is portable and lossy",
         "Readable by anything, but slower, larger, and it forgets the dtype.",
         '''import numpy as np, tempfile, os, io

a = np.array([[1.5, 2.25], [3.125, 4.0]])
path = os.path.join(tempfile.mkdtemp(), "a.csv")

np.savetxt(path, a, delimiter=",", fmt="%.4f", header="x,y", comments="")
print(open(path).read())

b = np.loadtxt(path, delimiter=",", skiprows=1)
print("loaded:", b.tolist(), b.dtype, "<- always float, whatever was saved")
print()
ints = np.array([1, 2, 3], dtype=np.int8)
buf = io.StringIO()
np.savetxt(buf, ints)
print("int8 saved as text comes back as:",
      np.loadtxt(io.StringIO(buf.getvalue())).dtype)'''),

        ("allow_pickle is off by default, and should stay off",
         "Loading a pickle executes code. The default protects you; do not override "
         "it for files you did not create.",
         '''import numpy as np, tempfile, os

path = os.path.join(tempfile.mkdtemp(), "obj.npy")
mixed = np.array([1, "two", [3]], dtype=object)

np.save(path, mixed, allow_pickle=True)
try:
    np.load(path)
except ValueError as e:
    print("np.load(...) ->", type(e).__name__)
    print("   ", str(e)[:78])

print()
print("it loads only if you explicitly allow it:")
print("   ", np.load(path, allow_pickle=True))
print()
print("An object array is pickled, and unpickling runs arbitrary code.")
print("Never pass allow_pickle=True to a file from an untrusted source.")'''),

        ("Reading messy text with genfromtxt",
         "<code>loadtxt</code> is strict; <code>genfromtxt</code> copes with gaps.",
         '''import numpy as np, io

raw = "1.0,2.0\\n3.0,\\n5.0,6.0\\n"

try:
    np.loadtxt(io.StringIO(raw), delimiter=",")
except ValueError as e:
    print("loadtxt on a missing field ->", type(e).__name__)

g = np.genfromtxt(io.StringIO(raw), delimiter=",")
print()
print("genfromtxt fills the gap with nan:")
print(g)
print()
print("or with a value you choose:")
print(np.genfromtxt(io.StringIO(raw), delimiter=",", filling_values=-1))'''),

        ("Big files: memory-mapping",
         "Read slices of a file larger than RAM without loading all of it.",
         '''import numpy as np, tempfile, os

path = os.path.join(tempfile.mkdtemp(), "big.npy")
np.save(path, np.arange(10_000, dtype=np.float64).reshape(100, 100))

mm = np.load(path, mmap_mode="r")
print("type      :", type(mm).__name__)
print("shape     :", mm.shape, " dtype:", mm.dtype)
print("one row   :", mm[7][:5], "<- only this part is read")
print()
print("slices behave like a normal array:")
print("   column mean of first 10 rows:", float(mm[:10, 0].mean()))
print()
print("mmap_mode='r' is read-only; 'r+' allows writing back.")
print("np.array(mm) materialises the whole thing when you do want it.")'''),
    ],
    [
        "<code>.npy</code> is the native format: it preserves dtype and shape exactly and round-trips without loss.",
        "<code>savez</code> bundles several named arrays into one <code>.npz</code>; <code>savez_compressed</code> compresses them.",
        "Text formats are portable but lossy &mdash; everything comes back as float, and files are larger and slower.",
        "<code>allow_pickle</code> defaults to <strong>False</strong> because unpickling runs arbitrary code. Never enable it for a file you did not create.",
        "<code>loadtxt</code> raises on missing fields; <code>genfromtxt</code> fills them with NaN or a value you choose.",
        "<code>mmap_mode=\"r\"</code> reads slices of a file larger than memory without loading the whole thing.",
    ],
    '''
title: Saving and Loading Arrays
intro: npy, npz, text and bytes, and which one to reach for.

## The native format

`np.save(path, a)` writes a `.npy` file: a short header describing dtype, shape and byte order, followed by the raw bytes.

`np.load(path)` reads it back identically. Dtype and shape survive, `int16` comes back as `int16`, and there is no parsing cost because there is nothing to parse.

It is the right default for anything that only needs to be read by NumPy. Files are compact, writing and reading are fast, and nothing is lost.

The extension is added automatically if you omit it.

## Bundles

`np.savez(path, train=X, labels=y)` writes an `.npz` &mdash; a zip archive of `.npy` files, one per keyword argument.

Loading gives a dictionary-like object. Arrays are read **lazily**, only when you index a key, so opening a large bundle to read one array does not load the rest.

It holds an open file handle, so use it as a context manager or call `close()`. Forgetting is a common source of file handles leaking in long-running code.

`np.savez_compressed` applies deflate. Whether that helps depends entirely on the data: zeros and repeated structure compress dramatically, and floating-point measurement noise barely compresses at all. It costs CPU on both ends, so it is worth measuring on your own data rather than assuming.

## Text

`np.savetxt` and `np.loadtxt` handle CSV and similar.

They are the right choice when something other than NumPy must read the file &mdash; a spreadsheet, a colleague, a different language.

They are the wrong choice otherwise, for three reasons. Files are several times larger. Parsing is far slower than reading raw bytes. And **the dtype is lost**: everything comes back as `float64`, whatever went in. An `int8` array round-trips into `float64`.

`fmt` controls precision on write, and `%.4f` will silently truncate values you cared about. `header` with `comments=""` writes a plain header line rather than a commented one.

## allow_pickle

This is the security-relevant part.

Object arrays &mdash; arrays with `dtype=object`, holding arbitrary Python objects &mdash; cannot be written as raw bytes. NumPy pickles them instead.

Unpickling **executes code**. A malicious `.npy` file can run anything when loaded.

So `np.load` has `allow_pickle=False` by default and raises rather than loading an object array. That default is a deliberate protection, added after the risk became a practical problem.

Enable it only for files you created yourself, or received through a channel you trust as much as you would trust an executable. "It is just data" is exactly the assumption the attack relies on.

Better still, avoid object arrays in saved data. If a structure will not fit in a plain numeric array, a format designed for structured data &mdash; JSON, HDF5, Parquet &mdash; is a better answer than pickling.

## Messy input

`loadtxt` is strict and raises on a missing field. That strictness is a feature when the data should be complete.

`genfromtxt` is the tolerant version. Missing values become `nan` by default, or whatever `filling_values` specifies. It also handles column names, per-column dtypes and skipping footers.

It is slower, and for genuinely messy tabular data, pandas' `read_csv` is faster and more capable. `genfromtxt` fits the middle ground: mostly clean numeric data with occasional gaps, where adding pandas would be more dependency than the problem justifies.

## Memory mapping

`np.load(path, mmap_mode="r")` returns an array backed by the file rather than by memory.

Slicing it reads only the pages touched. You can work with a file larger than RAM, and the operating system handles caching.

`"r"` is read-only. `"r+"` allows writing back into the file. `np.array(mm)` materialises the whole thing when you do want it in memory.

The limitation is that it only helps for access patterns that touch part of the data. A full reduction reads everything anyway, and does so with more overhead than a straight load.

## Choosing

NumPy-only, one array: `.npy`.

NumPy-only, several arrays: `.npz`, compressed if the data has structure.

Anything else must read it: text, accepting the size and the dtype loss.

Larger than memory, partial access: `mmap_mode`.

Genuinely large or shared across languages and tools: reach past NumPy to HDF5 or Parquet, which handle chunking, compression and metadata properly.

And whichever you choose, do not enable `allow_pickle` on input you did not produce.

## Byte order and portability

A `.npy` file records the byte order of the data it holds, so a file written on a big-endian machine loads correctly on a little-endian one. NumPy handles the swap.

You will see this in dtype strings: `<i4` is little-endian 32-bit integer, `>i4` big-endian, `=i4` native.

It matters when reading raw binary from an external source &mdash; a network protocol, an instrument, a file format defined elsewhere &mdash; where the byte order is part of the specification and NumPy has no header to tell it. Getting it wrong produces numbers that are wrong in a distinctive way: plausible magnitudes, nonsense values.

`a.byteswap()` swaps the bytes in place; `a.astype(a.dtype.newbyteorder())` produces a converted copy.

## tofile and fromfile, and why to avoid them

`a.tofile(path)` writes the raw bytes with **no header at all**. `np.fromfile(path, dtype=...)` reads them back.

That means the file records neither the shape nor the dtype. Reading it requires knowing both in advance, from somewhere outside the file. Get the dtype wrong and you get garbage rather than an error; get the shape wrong and you get a reshape failure or, worse, a plausible wrong shape.

They exist for interoperating with programs that expect raw binary, and for that they are correct. As a storage format for your own data they are strictly worse than `.npy`, which adds a hundred-odd bytes of header and removes the entire class of problem.

If you meet a `tofile` in existing code, it is worth checking whether the shape and dtype are documented anywhere, because that documentation is the only thing making the file readable.

## Structured dtypes for records

When the data is genuinely tabular &mdash; mixed types per column &mdash; a structured dtype keeps it in one array:

```python
dt = np.dtype([("name", "U20"), ("age", "i4"), ("score", "f8")])
people = np.array([("ana", 31, 8.5)], dtype=dt)
```

Fields are accessed by name: `people["age"]`. The result is a view, so assigning into it modifies the original.

Structured arrays save and load through `.npy` without pickling, which is their main advantage over an object array &mdash; the data stays plain bytes.

They also sort by field name with `order=`, which is the closest NumPy comes to sorting a table by columns.

The honest caveat: for anything with more than a few columns or any real analysis, pandas does this better. Structured arrays are worth knowing for reading fixed-format binary files and for the cases where adding pandas is not justified.

## Formats beyond NumPy

`.npy` and `.npz` are excellent for NumPy-only data of moderate size. Past that, the ecosystem has better answers.

**HDF5**, via `h5py`, handles very large arrays with chunking, compression and metadata, supports partial reads and writes, and is readable from most languages. It is the standard in scientific computing for a reason.

**Zarr** is similar in spirit, designed for cloud object storage, and works well with Dask for parallel access.

**Parquet**, via `pyarrow`, is columnar and is the right choice for tabular data going anywhere near a data pipeline or a query engine.

The signals that it is time to move: files over a few hundred megabytes, needing to read part of an array without loading it, needing to append over time, or needing anything other than Python to read it.

## A safety summary

The security point deserves restating because it is the one thing in this module that can go beyond losing data.

`np.load` runs arbitrary code when loading a pickled object array. `allow_pickle=False` is the default and it is protecting you.

Enable it only for files you produced, or that arrived through a channel you would trust with an executable. A `.npy` file from an untrusted source should be treated the way you would treat a downloaded script, because in the object-array case that is what it is.

The safe alternatives, in order of preference: keep the data in plain numeric arrays so pickling never arises; use a structured dtype for records; use JSON or Parquet for anything genuinely heterogeneous.

"It is just a data file" is precisely the assumption the attack depends on.

## Round-tripping reliably

The habit worth forming is to verify a save-and-load cycle once when introducing a new format, rather than discovering the loss later.

```python
np.save(path, a)
b = np.load(path)
assert np.array_equal(a, b) and a.dtype == b.dtype
```

Checking the dtype alongside the values catches exactly the failure that text formats introduce silently, and it takes one line.

For floating-point data going through a text format, `np.allclose` rather than `array_equal` is the honest comparison, because `fmt` has almost certainly truncated something.

## Paths, and a common annoyance

`np.save` appends `.npy` if the filename does not already end in it. That is convenient until code computes a path, saves to it, and then fails to find the file &mdash; because the actual file has an extra extension the code does not know about.

Passing an open file object instead of a path avoids the rewriting entirely, and is the reliable form when the filename is computed.

`np.savez` behaves the same way with `.npz`.

## Compression, in practice

`savez_compressed` costs CPU on write and on read, and saves space only if the data has structure to exploit.

Integer data with a small range, arrays with many repeated values, and anything sparse compress well &mdash; often by an order of magnitude.

Floating-point measurement data compresses poorly, because the low-order bits are effectively random. A 10&ndash;20% saving for several times the CPU is rarely a good trade.

The way to decide is to try both on a representative sample and compare, which takes a minute and settles it for that dataset.

## Writing for other people

If a file will be read by someone other than you, or by you in two years, the format is only half of it.

Record the shape and dtype expectations somewhere the reader will find them, particularly for `tofile` output, which carries neither.

Prefer `.npz` with named arrays over several `.npy` files with meaningful filenames, because the names travel with the data.

For anything that is genuinely a dataset rather than an intermediate &mdash; something that will be reused, shared or archived &mdash; HDF5 or Parquet carry metadata properly and are readable outside Python. The extra dependency buys real portability.

## The summary

`.npy` for a single array, NumPy only. Lossless, compact, fast.

`.npz` for several named arrays, compressed only if the data compresses.

Text when something else must read it, accepting that the dtype is gone.

`mmap_mode` for partial access to something larger than memory.

HDF5, Zarr or Parquet past a few hundred megabytes, or when other tools are involved.

`allow_pickle=False` &mdash; the default &mdash; on anything you did not produce yourself. That one is not a performance preference; it is the difference between reading a file and running one.

## A closing note

Storage is where a project's decisions become permanent. A format chosen for convenience during a first experiment tends to survive into production, and by then there is data in it.

`.npy` and `.npz` are good enough for a great deal of work and cost nothing to adopt. The point to reconsider is when files grow past a few hundred megabytes, when something other than Python needs to read them, or when only part of an array is needed at a time &mdash; and recognising that point early is easier than migrating later.
''',
    [
        {"q": "What does `.npy` preserve that a CSV does not?",
         "options": ["Nothing", "The exact dtype and shape", "The filename", "Compression"],
         "answer": 1,
         "why": "Text round-trips everything back as float64, whatever went in. An int8 array saved as text returns as float64."},
        {"q": "Why does `np.load` default to `allow_pickle=False`?",
         "options": ["Pickle is slow", "Unpickling executes code, so a malicious .npy file could run anything", "It saves memory", "Pickle is deprecated"],
         "answer": 1,
         "why": "It is a deliberate protection. Enable it only for files you trust as much as you would trust an executable."},
        {"q": "What is the difference between `loadtxt` and `genfromtxt`?",
         "options": ["None", "loadtxt raises on missing fields; genfromtxt fills them with nan", "genfromtxt is faster", "loadtxt handles more formats"],
         "answer": 1,
         "why": "loadtxt's strictness is a feature when data should be complete. genfromtxt also takes filling_values to choose the substitute."},
        {"q": 'What does `mmap_mode="r"` give you?',
         "options": ["Faster full loads", "An array backed by the file, so slices read only the pages they touch", "Compression", "A read-only copy in memory"],
         "answer": 1,
         "why": "It lets you work with a file larger than RAM - but only helps for partial access, since a full reduction reads everything anyway."},
    ],
)
