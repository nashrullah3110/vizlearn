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
intro: One type, laid out end to end. Why almost all else follows from that.

## Two ways to hold five numbers

NumPy exists because Python lists are too slow for numerical work. The difference is not a small percentage. It is often a factor of a hundred. That gap comes from how each structure stores data in memory.

A Python list stores pointers. Each element is a Python object sitting somewhere in memory, with its own type information, reference count, and value. Adding two lists elementwise means following each pointer, checking each type, calling the addition operator, and building a new object for the result. That is a lot of work per number.

A NumPy array stores raw values. Five int64 numbers are forty bytes in a row, with the type recorded once for the whole array. Adding two arrays is a single compiled loop over those bytes. No pointer chasing, no type checking, no object creation. The loop runs in C, not in Python.

That speed difference is the entire reason NumPy exists. Every library that does numerical work in Python -- pandas, scikit-learn, scipy, matplotlib -- builds on NumPy arrays underneath. Learning NumPy means learning the data structure that the whole ecosystem shares.

The cost of that speed is rigidity. Every element has the same type. The array has a fixed size. Appending is expensive. These constraints are what make the compiled loops possible. If every element could be a different type, the code would need the same per-element checks that make lists slow.

This module introduces the array, shows how it differs from a list in memory and in speed, and explains the one-dtype constraint that everything else follows from.


A Python list of five ints is five pointers, each to a full `PyObject` sitting one spot else in memory. Each of those objects carries a type, a link count and the value. Adding two lists elementwise means following each pointer, checking each type. Building a new object for each result.

A NumPy array of five ints is forty bytes. Five 64-bit numbers, one after another, with the type recorded once for the whole array.

That single gap shows nearly all else in this track. It's why arrays are fast, why they've a dtype, why they can't hold mixed types, why slicing gives you a view instead of a copy. Why shapes matter so much.

## Vectorisation

Because the numbers are contiguous and all the same type, the loop can happen in compiled code:

```python
doubled = arr * 2
```

There's no Python-level loop. NumPy hands the whole block to a C routine that walks it. Modern CPUs process a few elements per instruction while it does.

The mental shift is from *how do I loop over this* to *what step am I applying*. That reads oddly at first and turns the natural way to think within about a week.

## `+` means two different things

Worth stating early because it's the first thing that surprises people converting code:

```python
[1, 2] + [1, 2]                  # [1, 2, 1, 2]   - concatenation
np.array([1, 2]) + np.array([1, 2])   # array([2, 4]) - addition
```

Lists concatenate. Arrays add. Neither is wrong. They're other types with other meanings for the same symbol. Code that assumes one while holding the other makes a thing plausible rather than an error.

## One dtype, and it is decided for you

each element of an array has the same type. NumPy picks the narrowest type that fits all you gave it.

`[1, 2, 3]` turns the platform's default int. On most desktop machines that is `int64`. On this page. This Runs 32-bit WebAssembly, it's `int32`. That gap isn't cosmetic. An `int32` overflows at about 2.1 billion, silently and without a warning. And it's the reason examples here that times large ints ask for `dtype=np.int64` by name. Add one float and the whole array turns `float64`. Not a mixture. Add a string and each element turns a fixed-width string, including the numbers.

That last case is worth watching for. It makes an array that still looks fair when printed and does nothing you want arithmetically.

There's a result people meet early: assigning into an array can't change its dtype. Put `9.7` into an `int64` array and it truncates to `9`, silently. The array's type was fixed when it was created.

## Speed, honestly

The fourth editor above measures it. Expect a large ratio. Read the ratio rather than the seconds.

These pages run CPython compiled to WebAssembly. This Is a few times slower than a native interpreter for the Python parts. That fine falls mostly on the Python loop. If anything the gap here flatters NumPy. The direction is right and the magnitude is roughly right. The abs numbers don't transfer to your laptop.

The speed also has limits worth knowing now. Arrays are fast for whole-array steps on numeric data. They aren't fast if you loop over them in Python one element at a time. That is slower than a list. Each element has to be boxed into a Python object on the way out.

## Shape

An array carries a shape and contents. Most of the notable action in this library is about what shapes do when mixed.

`a.shape` is a tuple. `(6,)` is one-dimensional with six elements. `(2, 3)` is two rows of three. `(2, 3, 4)` is two blocks of three rows of four.

Reshaping is often free, because it changes how the same block of memory is read rather than moving anything. The last editor shows `np.shares_memory` confirming that the reshaped array is the same numbers.

## Where this sits

Almost nothing in scientific Python reimplements arrays. pandas holds NumPy arrays under its columns. scikit-learn takes and returns them. SciPy builds on them. PyTorch and TensorFlow use their own tensor types on purpose modelled on the same interface. That `@`, broadcasting and `.shape` mean what you already expect.

Learning NumPy properly is so not one library. It's the vocab that the rest of the stack assumes you've.

## What this track covers

The array itself first: creating one, its dtype, its shape. What indexing gives you. Then operating on arrays: elementwise math, broadcasting, boolean masks, aggregation along an axis. Then structure: views versus copies, stacking, transposing, sorting. Then the numeric end: random numbers, linear algebra, missing data. The speed rules that follow from the memory layout.

each idea is a small program on the page. Change the numbers and press Run. A shape rule you've watched break is one you'll note.

## Why the list is slow, concretely

It's worth being precise about where the time goes. "Python is slow" isn't an reason and doesn't tell you what to change.

A Python list of five ints is an array of five **pointers**. Each pointer leads one spot else in memory, to a `PyObject` that carries a link count, a type pointer. Only then the actual value. A small int occupies twenty-eight bytes and sits wherever the allocator put it.

Adding two lists elementwise so means: follow a pointer, check the type, extract the value, follow another pointer, check that type, extract that value, perform the addition, allocate a new object for the result. Store a pointer to it. Ten times over for ten elements.

The NumPy array is five ints, adjacent, with nothing between them. The addition is a loop in compiled C over contiguous memory, with the type checked once for the whole array rather than once per element.

Two split wins come out of that. The obvious one is skipping the interpreter. The less obvious one is **nearness**. The processor fetches memory in blocks. Reading in a row values costs a fraction of what chasing scattered pointers costs. On large arrays the second effect can matter as much as the first.

This also shows the cases where NumPy doesn't help. If your data is a thousand elements and you touch it once, the interpreter cost you avoided was small and the conversion cost wasn't. The wins scale with array size.

## What NumPy deliberately does not do

Knowing the boundaries saves a lot of fighting with it.

**It doesn't grow.** There's no fast append. The size is fixed at creation. Each function that appears to extend an array is allocating a new one and copying. This isn't an oversight. It's the price of the contiguous block that makes all else fast.

**It doesn't mix types.** One dtype per array. A column of names and a column of ages are two arrays, or a structured dtype, or a pandas DataFrame. Not one NumPy array of mixed values.

**It handles strings poorly.** NumPy strings are fixed width. Assigning a longer value silently truncates it. Object arrays hold real Python strings but give up each speed gain. They're back to storing pointers.

**It has no concept of missing data.** Floats can carry NaN. Ints can't carry anything. There's no null.

## When to use something else

**Small data touched once.** A hundred values processed in a script: a list is simpler and the gap is unmeasurable.

**Heterogeneous records with labels.** That is pandas. It's built on NumPy. You lose nothing. You gain named columns, mixed types per column and real handling of missing values.

**Nested or ragged structure.** Lists of other lengths don't form an array. Forcing them into an object array gets you the syntax without the speed.

**Data larger than memory.** NumPy assumes the array fits. Dask, Zarr and HDF5 exist for when it doesn't.

## The model to carry forward

all else in this track is a result of one idea. An array is a **flat block of same values, plus a small description of how to read it**. The shape, the dtype. The number of bytes to step for each axis.

Reshaping changes the description and not the block. Transposing changes the description. Slicing changes the description. All of them are free.

Masking and fancy indexing can't be given that way, so they copy.

Math runs over the block in compiled code. Broadcasting is a rule for pretending two descriptions are matching without changing either block.

Hold onto that and most of NumPy's action stops being a set of rules to store and turns a thing you can predict.

## Questions people ask at this point

**Does NumPy replace Python lists?**

No. Lists are the right structure for heterogeneous, growing sets of any objects. They remain the right answer for most plain Python. NumPy is for a exact shape of problem. Many values of the same type, operated on together. Reaching for an array to hold three config values is worse than a list, not better.

**Do I need to install it?**

NumPy isn't in the standard library. It's `pip install numpy`. It's a dependency of nearly all numeric. It's often already present in a scientific setting. It ships as a compiled wheel for each common platform. So Installation doesn't need a compiler.

**Why is it always imported as `np`?**

rule, and a strong one. Nearly all published code, docs and examples use `import numpy as np`. Following it makes your code readable to anyone who has seen NumPy before. There's no technical reason, and no good reason to deviate.

**Is NumPy still relevant with pandas and PyTorch around?**

It's underneath both. A pandas Series wraps a NumPy array. PyTorch tensors follow the same shape and broadcasting rules and convert to arrays in one call. all in this track transfers. This Is a large part of why it's worth learning properly rather than by copying snippets.

**How much of it do I need?**

Less than the docs suggests. NumPy has hundreds of functions and a working knowledge of maybe thirty covers most real code. The concepts. Shape, dtype, views, broadcasting. Matter far more than the function list. They let you predict action instead of looking it up.

## How to work through this track

Each module has runnable editors above the text. They aren't decoration. The fastest way to build an accurate mental model of shapes and dtypes is to change a number, run it, and see what happens.

The parts worth slowing down on are the ones where NumPy's action differs from Python's. Int overflow, views sharing memory, broadcasting shapes you didn't intend. NaN. Those four account for most of the surprises in real code, and each has a module.

The parts you can skim on a first pass are the function inventories. The exact names in stacking, sorting and set steps. Knowing that a function exists is enough. The signature is a search away.
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
intro: The half-dozen constructors that cover almost all, and which to reach for when.

## From data you already have

Every NumPy program starts by creating an array. The constructor you choose depends on where the data comes from and what shape you need. Getting the right constructor is a small decision, but the wrong one can give you an array with the wrong dtype, the wrong shape, or the wrong number of dimensions.

The most common path is np.array, which takes a list and infers the shape and dtype from its contents. One level of nesting gives a 1-D array. Two levels give a 2-D array. The rows must be the same length. Ragged input raises a ValueError rather than guessing, which is the right behaviour because the alternative would be an array of Python objects that looks like an array but performs like a list.

When you need an array of a specific size filled with a known value, np.zeros, np.ones and np.full are faster and clearer than building a list first. np.zeros gives you the array in one allocation. Building a list of zeros and then converting it allocates the list, populates it, then allocates the array and copies, for no benefit.

np.arange and np.linspace generate sequences. arange steps by a fixed increment. linspace divides a range into a fixed number of points. The difference matters when you care about the number of points versus the step size. linspace includes the endpoint by default. arange does not. That is a common source of off-by-one errors.

np.empty allocates memory without filling it. The values are whatever happened to be in memory. It is faster than zeros when you plan to overwrite every element immediately. Using it and then reading before writing is a bug.

This module covers np.array, the convenience constructors, sequence generators, and the dtype argument that overrides inference. The examples show the shape and dtype of each result, because checking those two properties is the first thing you should do after creating an array.


`np.array` takes a list, a tuple, or nested lists. Infers the shape from the nesting. One level gives you 1-D, two levels gives 2-D, and so on.

Rows must be the same length. Ragged input raises rather than guessing. This Is the right choice. The option would be an array of Python list objects that looks like an array and behaves like nothing you want.

If you truly have ragged data, you want a list of arrays, or padding to a rectangle. You should decide which on purpose.

## When you know the shape but not the values

Most real code knows the shape first. Allocating it right is both faster and clearer than building a list and converting.

`np.zeros(shape)` and `np.ones(shape)` are the common ones. `np.full(shape, value)` fills with anything. `np.eye(n)` is the identity mat.

Note that the shape arg is a *tuple* for more than one dim: `np.zeros((2, 3))`. `np.zeros(2, 3)` is a other function signature and won't do what you meant.

`np.empty` deserves a warning. It allocates without resetting. The contents are what happened to be in that memory. Not zeros, not anything predictable. It's marginally faster than `zeros` and only correct when you're about to overwrite each element. Reaching for it by default makes bugs that appear only at times.

## arange and linspace

Both make a sequence, and the gap is what you give.

`np.arange(start, stop, step)` takes a **step** and excludes the stop, just like Python's `range`.

`np.linspace(start, stop, num)` takes a **count** and includes the stop.

For ints, `arange` is natural. For floats, it's a trap. The number of elements depends on floating-point build-up. `np.arange(0, 1, 0.1)` may give you ten elements or eleven based on rounding. `np.arange(0, 0.3, 0.1)` can include a value slightly above 0.3.

The rule is simple: **if the step is a float, use `linspace`.** You almost always know how many points you want. `linspace` gives just that many, with the endpoint where you asked for it.

## Matching an existing array

The `_like` family &mdash; `zeros_like`, `ones_like`, `empty_like`, `full_like` &mdash; copies both shape and dtype from an array you already have.

The dtype part is the valuable half. In a pipeline working in `float32` for memory reasons, allocating a result with `np.zeros(shape)` gives `float64`. The first step that mixes them widens all back. `zeros_like` keeps the type you chose.

## Choosing a dtype

The dtype is fixed at creation and worth choosing rather than accepting.

ints come in `int8`, `int16`, `int32` and `int64`, signed and unsigned. Floats come in `float32` and `float64` (and `float16`, with real precision costs).

Two reasons to care. **Memory**: a million `float64` values is 8 MB. `float32` halves that. This Matters once arrays are large. **Overflow**: an `int8` holds &minus;128 to 127. `127 + 1` gives &minus;128 with no error and no warning. NumPy doesn't promote to a wider type to save you.

That silence is the key part. Python ints grow without limit. NumPy ints wrap. Code ported from lists to arrays can start making wrong numbers rather than raising. This Is much harder to notice.

The default int width is platform-dependent. `int64` on most desktops, `int32` on this page's 32-bit WebAssembly. Where the values may be large, say what you want.

## Never grow an array in a loop

`np.append` doesn't append. There's nowhere to append to. An array is a fixed block of memory. `np.append` allocates a new one, copies all across. Returns it. In a loop that is quadratic.

The last editor measures it. The fix is the same as the string-joining fix in Python. Allocate the result once and assign into it, or better, build the whole thing with a vectorised call and no Python loop at all.

If you truly don't know the final size, collect into a Python list and convert once at the end. Lists over-allocate and appending to them is cheap.

## Which to reach for

Data in hand: `np.array`.

Known shape, zeros: `np.zeros`. Known shape, matching an existing array: `zeros_like`.

int sequence: `np.arange`. Float sequence: `np.linspace`.

A result you're about to fill fully: `np.empty`, and only then.

Anything else in a loop: stop and ask whether a vectorised formula would build it in one call.

## empty is not zeros

`np.zeros` writes zeros. `np.empty` allocates and writes nothing. The contents are what was before in that memory.

That makes `empty` faster, and it's the correct choice when you're about to overwrite each element. It's a bug waiting to happen when you aren't.

The trap is that uninitialised memory is often zeros above all on a freshly started process. Code that accidentally leans on `empty` giving zeros can pass each test and then give garbage under real load when the allocator hands back recycled memory.

The rule: use `empty` only when the very next thing you do fills the whole array. If there's any branch where an element might not be written, use `zeros`.

## Bringing data in from elsewhere

`np.array` on a list is the common case. But It isn't the only door.

`np.frombuffer` wraps existing bytes without copying. handy for data arriving from a socket, a file read, or another library. The result is read-only if the buffer is. It shares memory with the source. The usual view caveats apply.

`np.fromiter` builds an array from any iterable, consuming it lazily. This is the one to reach for with a gen. `np.array(gen)` does **not** do what you'd hope. It creates a zero-dimensional object array holding the gen itself. That failure is silent and confusing. `fromiter` with an clear `dtype` is the fix. Pass `count` when you know the length. It can preallocate instead of growing inside.

`np.loadtxt` and `np.load` cover files, and get a module of their own later.

## The structured constructors

`np.eye(n)` gives an identity mat. `np.identity(n)` is the same thing with fewer options. `np.eye` takes a `k` arg to offset the main-line. This Is how you build shift mats.

`np.diag` is two functions in one, based on what you hand it. Given a 1-D array it builds a mat with that main-line. Given a 2-D array it extracts the main-line. That overloading is convenient and at times surprising.

`np.full(shape, value)` fills with a constant. Is clearer than `np.ones(shape) * value`. It also gets the dtype right, inferring it from the fill value rather than starting from float.

`np.tile` and `np.repeat` build larger arrays from smaller ones. They differ in a way worth remembering: `tile` repeats the whole array, `repeat` repeats each element in place. `np.tile([1,2], 2)` gives `1 2 1 2`. `np.repeat([1,2], 2)` gives `1 1 2 2`.

## array versus asarray

`np.array(x)` copies by default. `np.asarray(x)` doesn't copy if `x` is already an array of the right dtype.

That gap matters at function boundaries. A function that begins `a = np.asarray(a)` accepts lists and arrays alike. Costs nothing when given an array it can use right. The same function written with `np.array` copies each call. This Is wasteful in a loop and can be large for large inputs.

Use `asarray` for "make sure this is an array". Use `array` when you namely want a copy that the caller can't see you modify.

Note that `asarray` returning the first means you must not modify it in place unless you own it. The same views-and-copies question that runs through the whole library.

## A checklist for choosing

Ask, in order:

**Do I already have the values?** `np.array` or `np.asarray`.

**Do I know the shape but not the values?** `zeros`, `ones`, `full`, or `empty` if each element will be overwritten.

**Is it a sequence of numbers?** `arange` for a step, `linspace` for a count. Prefer `linspace` when the values are floats. `arange` with a float step has an unpredictable length.

**Should it match a thing I have?** The `_like` family. This Copies shape and dtype together and blocks the two from drifting apart.

**Is it coming from a gen or a byte buffer?** `fromiter` or `frombuffer`, never bare `np.array`.

And in each branch, set the dtype at creation rather than converting later. `astype` allocates a whole second array. Choosing right the first time avoids both the copy and the class of bugs where an int array silently refuses the float you assign into it.

## Common mistakes at this stage

**`np.array(gen)`.** This doesn't build an array from the gen's values. It builds a zero-dimensional object array holding the gen object itself. Each later step behaves bizarrely. `np.fromiter(gen, dtype=float)` is the correct call. Passing `count` when the length is known lets it preallocate.

**`np.array` on ragged input.** Lists of unequal length no longer give an object array silently. Modern NumPy raises. That is an gain. The object array it used to create looked like an array and performed like a list.

**Losing that `np.zeros` is float.** `np.zeros(5)` has dtype `float64`, not int. Code that fills it with counts and then uses it as an index has to convert. The conversion is a copy. `np.zeros(5, dtype=int)` at creation avoids both.

**`np.empty` where `np.zeros` was meant.** Uninitialised memory often holds zeros in a fresh process. This passes tests and fails in production.

**Building with `np.append` in a loop.** Quadratic. The single most common accidental slowdown in beginner NumPy code.

## A note on reproducible construction

Test data and examples gain from being fixed.

`np.arange` and `np.linspace` are fixed by build. This Makes them good for examples where the values don't matter but reproducibility does.

Where random data is truly needed, `np.random.default_rng(seed)` gives a gen whose output is fixed. Seeding at the point of build, rather than leaning on a global, keeps the example self-held. Which is why each random example in this track creates its own gen.

## Getting the shape right the first time

Most build bugs are shape bugs, and two habits prevent them.

**Pass the shape as a tuple and read it back.** `np.zeros((3, 4))` is unambiguous. `np.zeros(3, 4)` is an error. The second spot-based arg is the dtype. A truly confusing failure the first time it happens.

**Use the `_like` family when an array should match another.** `np.zeros_like(a)` can't drift out of sync with `a` the way a hard-coded shape can. When the shape of `a` changes, the output follows. One fewer place needs editing.

## Questions people ask

<strong>What is the difference between np.array and np.asarray?</strong> np.array copies by default, while np.asarray returns the input unchanged if it is already an array of the right dtype. Use asarray in functions that only read their input.

<strong>Should I use arange or linspace for floats?</strong> Use linspace. With a float step, arange can land one element short or over because of rounding, whereas linspace takes the element count and includes the endpoint.

<strong>Is np.empty faster than np.zeros?</strong> Slightly, since it skips filling the memory, but it returns whatever bytes were there. Use it only when you will overwrite every element.

<strong>Why is growing an array with append in a loop slow?</strong> Each append allocates a new array and copies everything. Collect values in a list and convert once, or preallocate with the final shape.

<strong>How do I make an array shaped like another one?</strong> Use zeros_like, ones_like, empty_like or full_like. They copy the shape and dtype of the template.

<strong>What dtype do I get from np.array([1, 2, 3])?</strong> An integer type, usually int64 on Linux and macOS. Add one float to the list and every element becomes float64.

## A closing note

Creation is the cheapest place to prevent problems. The dtype and shape chosen here pass through all that follows.

Setting the dtype at build avoids a copy and a class of silent conversion bugs. Passing the shape as a tuple avoids the confusing failure where the second arg is read as a dtype. And using the `_like` family keeps derived arrays from drifting out of sync with their source.

Three small habits, applied once, that drop a disproportionate amount of later debugging.
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
# float32 holds integers exactly only up to 2**24. Past that, the gap
# between representable values is bigger than 1, so adding 1 does nothing.
edge = np.float32(2 ** 24)
print("2**24 in float32      :", float(edge))
print("   + 1 changes nothing:", float(edge + np.float32(1)) == float(edge))
print()
# and a value that float32 cannot represent exactly accumulates error
vals = np.full(1_000_000, 0.1, dtype=np.float32)
f32 = float(vals.sum())
f64 = float(vals.sum(dtype=np.float64))
print("sum of 1e6 x 0.1")
print("   float32 accumulator: %.6f" % f32)
print("   float64 accumulator: %.6f" % f64)
print("   difference         : %.6f" % abs(f32 - f64))'''),
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
intro: One type for the whole array: what it costs, when it overflows. How promotion decides the result.

## Kind and width

Every element in a NumPy array has the same type. That type is the dtype. It records two things: what kind of number the element is, and how many bytes it occupies. Understanding dtypes is necessary because they control precision, memory usage, and the behaviour of arithmetic operations.

The kind tells you the family: signed integer, unsigned integer, floating point, complex, boolean, or string. The width tells you the size: int8 is one byte, int64 is eight bytes. A wider type holds a larger range of values but uses more memory.

Choosing the right dtype matters for two reasons. First, memory. A column of ages stored as int64 uses eight bytes per value. Stored as int8, it uses one byte. For a million rows, that is the difference between eight megabytes and one megabyte. Multiply by many columns and the savings determine whether the data fits in memory at all.

Second, overflow. An int8 holds values from negative 128 to positive 127. Adding two int8 values that sum to more than 127 wraps around silently. There is no error. The result is wrong. This happens in practice when people downcast aggressively without checking the value range.

Floating-point precision is the other common issue. float32 has about seven decimal digits of precision. float64 has about fifteen. Most scientific computation uses float64 by default. Switching to float32 halves the memory and speeds up some operations, but accumulated rounding errors can change the result. Whether that matters depends on the application.

NumPy infers the dtype from the input. A list of Python ints becomes int64. A list of Python floats becomes float64. A list with one float and the rest ints becomes float64, because the dtype must hold every element. That promotion is silent and worth checking.

This module covers the common dtypes, their ranges and memory costs, how to specify them, and how to convert between them safely. It also covers the structured dtypes that let a single array hold multiple fields per element, like a lightweight record type.


A dtype records what kind of number and how many bytes. `int32` is a signed int in four bytes. `float64` is a double-precision float in eight.

Both halves matter. The kind decides what steps mean. The width decides the range and the memory.

`np.iinfo` and `np.finfo` report the limits. It's worth looking at them once rather than remembering guesses. The first editor prints them.

## Integers wrap

This is the sharpest gap from plain Python and the one most likely to cause a quiet bug.

A Python `int` grows to what size it needs. A NumPy int is a fixed-width machine int. Exceeding it wraps around. `int8` at 127 plus one is &minus;128. No exception, no warning.

Code that worked on lists can give wrong numbers on arrays. The failure is silent. That is worse than a crash. Nothing draws focus to it.

Two habits help. Choose a width with headroom when values can grow. And be aware that the default int is platform-dependent. `int64` on most desktops, `int32` on this page. So an example that is safe on your laptop may overflow elsewhere, and vice versa.

## Promotion

When two arrays of other dtype meet, NumPy finds a type that can hold both and converts before operating.

Mostly this is what you want. `int8 + int16` gives `int16`. `int32 + float32` gives `float64`. This Surprises people the first time: `float32` can't represent each `int32` just. NumPy widens to a thing that can.

The result worth knowing is memory. A carefully chosen `float32` array mixed with anything `float64` makes a `float64` result. A pipeline can quietly double its footprint at one careless line. If you're working in `float32` on purpose, keep constants and mid arrays in `float32` too.

## Assignment converts, it does not widen

Writing into an array converts the value to the array's dtype:

```python
ints = np.arange(5)
ints[0] = 9.99        # stores 9
```

Truncation toward zero, silently. The array's type was decided at creation and a single set can't change it.

The same applies to precision. Writing `1/3` into a `float32` array stores the nearest `float32`. Reading it back gives a value that differs from Python's float in the seventh decimal place.

## astype

`astype` makes a new array with a new dtype. Two things to note.

It **always copies**, even when the dtype is unchanged, unless you pass `copy=False`. That is a real cost on large arrays.

It **converts without complaint**. Floats truncate toward zero rather than rounding. `1.9` turns `1` and `-1.9` turns `-1`. Values outside the target range overflow. If you meant to round, call `np.round` first and then convert.

## Choosing a width

Two considerations, and they pull in opposite directions.

**Memory.** A million `float64` values is 8 MB. In `float32` it's 4 MB, in `float16` 2 MB. On large arrays this is the gap between fitting in cache and not. This Affects speed as much as room.

**Precision and range.** `float32` carries about seven large decimal digits, `float64` about sixteen. For image pixels, neural network weights and most measured data, `float32` is ample. For building up a sum over millions of elements it isn't. The running total grows until adding one more small value changes nothing.

The last editor shows that: summing a million ones in `float32` doesn't give a million. `sum(dtype=np.float64)` builds up in double precision while keeping the array itself small. This Is often the right compromise.

## A working rule

Default to `float64` for numeric work unless memory is a real constraint. Use `float32` on purpose, for large arrays. Keep the whole pipeline in it.

For ints, pick a width that fits your values with room to spare. Be clear when the numbers might be large. The default isn't the same all over.

And when a result looks wrong by a factor of two, or minus when it shouldn't be, check the dtype before checking your logic.

## What float precision actually buys you

`float64` carries about 15 to 17 large decimal digits. `float32` carries about 7. `float16` carries about 3.

Those numbers are the whole story for choosing. The handy question isn't "how much precision is on hand" but "how much does my data have".

A temp sensor accurate to a tenth of a degree has three large digits. Storing its readings in `float64` records twelve digits of noise very just. `float32` would be ample, and would halve the memory.

The counter-arg is build-up. Summing a million `float32` values loses precision faster than summing a million `float64` values. The rounding error at each step is larger scaled to the running total. NumPy mitigates this by using pairwise summation inside. This Keeps the error growth much slower than a naive loop. It doesn't drop it.

A hands-on compromise, and what many libraries do. Store in `float32`, build up in `float64`. `a.sum(dtype=np.float64)` does just that. Reads a narrow array, builds up in a wide type.

## Why 0.1 + 0.2 is not 0.3

Binary floating point can't represent 0.1 just, any more than decimal can represent one third just. The stored value is very slightly off, and the errors compound.

This isn't a NumPy issue. It's the same in plain Python, in C. In each language using IEEE 754. But it bites harder in array code because you're more likely to be checking results of long steps.

The result: **never test floats for equality**.

`np.isclose(a, b)` checks elementwise with a handling. `np.allclose(a, b)` reduces that to a single boolean. Is the right thing in a test.

Both take `rtol` and `atol`. The scaled handling handles large values. Here A fixed abs gap is meaningless. The abs handling handles values near zero. Here A scaled compare breaks down. The defaults are sensible for common data and worth replacing when your values are unusually large or unusually small.

`equal_nan=True` makes NaN compare equal to NaN. This Is often what you want when checking that two arrays came out the same.

## Booleans

`np.bool_` is one byte, not one bit. NumPy doesn't pack booleans. A mask over a million elements costs a megabyte.

Booleans promote to ints in math, with `True` turning 1. That is why `mask.sum()` counts matches. It's one of the more handy accidents of the type system.

They don't promote silently in the other direction. Assigning 2 into a boolean array stores `True`. Anything nonzero is true. That conversion is lossy and silent. Is a reason to be careful about which array you're assigning into.

## Strings, and why they surprise people

NumPy string dtypes are **fixed width**. An array created from `["ana", "bartholomew"]` gets dtype `<U11`, sized to the longest.

Assign a longer string into it later and it's **silently truncated** to eleven characters. Nothing raises. This is the single most surprising action in NumPy's type system. It's a direct result of the fixed-size-elements design that makes all else work.

If you need real var-length strings, the options are an object array. Which stores pointers to Python strings and gives up each speed gain. Or pandas. This Handles this properly.

NumPy 2.0 added a var-width string dtype that handles this. It's recent enough that most code and most settings you'll meet don't have it.

## Object arrays

`dtype=object` makes an array of pointers to any Python objects. It looks like an array and supports the indexing syntax.

It isn't fast. each step falls back to calling Python methods per element. This Is a list with extra steps. It also can't be saved without pickling, with the security results covered later.

at times it's the right answer. A ragged set that you truly need to index like an array. often its appearance is a sign that the data doesn't want to be a NumPy array at all. It's worth checking whether a list, a dict or a DataFrame fits better before building on it.

## Working rules

Set the dtype at creation. Check `a.dtype` when a result looks wrong. It's the second thing to look at after `a.shape`. One of them shows most surprises.

Use `float32` when precision allows and memory matters, and build up in `float64`.

Never compare floats with `==`. Use `np.isclose` or `np.allclose`.

Treat int arrays as capable of silently wrapping. Pick a width with headroom for the data you might see, not the data in front of you.

And treat a fixed-width string dtype as a fixed-width string dtype. Check the width before assigning into one.

## Checking dtypes in practice

`a.dtype` is the direct question, and checking it works as you'd expect: `a.dtype == np.float64`.

For a group rather than an exact type, `np.issubdtype(a.dtype, np.int)` and `np.issubdtype(a.dtype, np.floating)` are the right tests. They handle each width at once. This A chain of equality checks doesn't.

`a.dtype.kind` gives a single character: `i` for signed int, `u` for unsigned, `f` for float, `b` for boolean, `U` for unicode string, `O` for object. It's convenient for quick branching.

In a function that accepts arrays from callers, converting defensively is often better than checking: `a = np.asarray(a, dtype=float)` accepts lists, int arrays and float arrays alike. Makes just one predictable type. It copies only when it has to.

## The unsigned trap

Unsigned ints behave oddly in subtraction.

`np.uint8(3) - np.uint8(5)` isn't `-2`. There are no minus values in an unsigned type. It wraps to 254.

This bites most often with image data. This Is often `uint8`. Subtracting two images to find a gap gives large plus values wherever the result should have been minus. The resulting image looks wrong in a way that is easy to misread as a bug elsewhere.

The fix is to convert before subtracting: `a.astype(np.int16) - b.astype(np.int16)`, then clip and convert back if needed.

Mixed signed and unsigned math also promotes in ways that surprise. Mixing `int64` and `uint64` gives `float64`. No int type can hold the full range of both. And that silent jump to float is a real source of precision loss on large ints.

## Questions people ask

<strong>What is a dtype?</strong> It is the description of how each element's bytes are read: the kind, such as integer or float, and the width in bits. Every element in an array shares one dtype.

<strong>What happens when an integer array overflows?</strong> It wraps around silently. An int8 holding 127 plus 1 becomes -128, with no warning, so pick a width that holds your largest value.

<strong>What is the difference between astype and view?</strong> astype converts the values and returns a new array. view reinterprets the same bytes under another dtype, with no conversion at all.

<strong>Why is 0.1 + 0.2 not equal to 0.3?</strong> Binary floating point cannot store 0.1 or 0.2 exactly. Compare with np.isclose or np.allclose instead of ==.

<strong>Should I use float32 or float64?</strong> float64 is the default and the safe choice. float32 halves memory and is common in deep learning, but it carries only about seven decimal digits.

<strong>Why does mixing int and float give float?</strong> NumPy promotes to the smallest type that can hold both without losing the range. An int and a float therefore produce a float.

## Choosing, summarised

**Floats.** `float64` unless memory matters. `float32` when it does and seven digits suffice, building up in `float64`.

**ints.** The default platform int is fine for indices and counts. Narrow on purpose for large arrays of small values, with headroom for the data you might see rather than the sample in front of you.

**Booleans.** `bool_` for masks. One byte each, and they promote to ints so `sum` counts.

**Strings.** Fixed width, silently truncating. Check the width before assigning, or use pandas.

**Objects.** Almost always a sign the data doesn't want to be an array.

And in all cases: set it at creation. `astype` allocates a second full array. Getting it right the first time avoids both that copy and the class of bugs where an int array quietly refuses the float you assigned into it.
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
intro: The same numbers read a other way, and why it often costs nothing.

## Three numbers

The shape of an array tells you its size along each axis. A 2-D array with three rows and four columns has shape (3, 4). A 1-D array of ten elements has shape (10,). A scalar has an empty shape. These three numbers -- shape, ndim, and size -- are the first things to check when an operation gives an unexpected result.

ndim is the number of axes, which is just the length of the shape tuple. size is the total number of elements, which is the product of the shape entries. Both are derived from shape, but having them as separate attributes makes quick checks easier.

Reshaping changes the shape without changing the data. A (12,) array can become (3, 4) or (2, 6) or (4, 3). The total number of elements must stay the same. Reshape does not move any data in memory. It just changes the description of how the bytes are interpreted. That is why reshape is fast and why the result is a view of the original array.

The negative-one shorthand lets you specify all dimensions but one. reshape(3, -1) on a 12-element array gives (3, 4) because NumPy infers that the missing dimension must be four. This is convenient when one dimension is known and the other depends on the data size.

The distinction between (n,) and (n, 1) matters more than it looks. A 1-D array and a column vector have different numbers of dimensions. Broadcasting rules treat them differently. Some functions return one shape when you expected the other. Knowing the difference prevents a class of shape-mismatch errors.

This module covers shape, ndim, size, reshape, ravel, flatten, and the newaxis trick for adding dimensions. The examples focus on small arrays where you can verify the layout by printing.


`shape` is a tuple showing the extent of each axis. `ndim` is how many axes there are. This Is just `len(shape)`. `size` is the total number of elements. This Is the product of the shape.

When an step complains about shapes, printing all three of these for both operands answers the question most of the time. It's worth making that reflex.

The empty tuple is a valid shape: `np.array(5).shape` is `()`, a zero-dimensional array holding one value. That comes up when an aggregation reduces all away.

## Reshaping is free

An array is a flat block of memory plus a description of how to walk it. `reshape` changes the description and leaves the memory alone.

That means it returns a **view**, not a copy. Writing through the reshaped array changes the first. There's only one set of numbers. `np.shares_memory` confirms it. The second editor shows the write going both ways.

This is the first appearance of a theme that runs through the whole track. Which has a module of its own. Many NumPy steps give you a other window onto the same data rather than new data.

Reshape can only return a view when the result can be given by regular strides. If it can't. Often after a transpose. NumPy copies instead, silently. If you need to know which happened, check `.base` or `np.shares_memory`.

## -1

One dim can be `-1`, meaning "work this one out from the others and the total size".

`a.reshape(3, -1)` says three rows. But Many columns that takes. It's better than hard-coding the second number. It keeps working when the input length changes.

Only one axis can be `-1`. Two would be ambiguous. And the total must divide just. Reshaping twelve elements into rows of five raises. This Is the correct action and a handy early warning that an upstream length isn't what you assumed.

## Row-major order

NumPy walks the **last axis fastest** by default. This Is called C order or row-major. Filling a `(2, 3)` array from `[0, 1, 2, 3, 4, 5]` gives rows `[0, 1, 2]` and `[3, 4, 5]`.

Fortran order fills the first axis fastest, giving columns instead. `reshape` and `ravel` both take an `order` arg.

You mostly don't need to think about this until you do. Interfacing with code that expects column-major layout, reading a binary file written by a thing else, or debugging a reshape that made a transposed-looking result. Knowing that the default is "last axis fastest" makes those predictable rather than mysterious.

## ravel and flatten

Both return a 1-D version. The gap is copying.

`ravel` returns a view when the layout permits. A copy when it doesn't. `flatten` always copies.

So `ravel` is cheaper and shares memory. `flatten` is safe and split. Use `ravel` when you're only reading. `flatten` when you intend to modify the result without touching the first. Or when you want a promise rather than a maybe.

The fifth editor shows the gap right: writing through the ravelled array changes the source, writing through the flattened one doesn't.

## Length-1 axes

A large share of real shape errors are an axis of size one in the wrong spot, often when a column of data needs to be a column rather than a flat sequence.

`a.reshape(-1, 1)` makes a column, `a.reshape(1, -1)` makes a row. `np.newaxis` in an index does the same thing and reads better in place: `a[:, np.newaxis]` says clearly that a new axis is being inserted at the end.

`squeeze` goes the other way, dropping each axis of length one. That is handy for cleaning up after an step that kept dims you no longer need. And mildly dangerous in library code. It drops axes you might have been leaning on when a dim happens to be one.

Getting these right matters most for broadcasting. This Is the next module but one. Where the gap between shape `(3,)` and shape `(3, 1)` decides whether you get the answer you wanted or a much larger array you didn't.

## The invariant

`a.size` is the product of `a.shape`, always. each reshape must preserve it. This Is why an hopeless reshape raises rather than truncating or padding.

That single constraint answers most "will this work" questions before you run anything. A 24-element array can become `(2,12)`, `(3,8)`, `(2,3,4)` or `(24,)`. It can't become `(5,5)`.

`a.ndim` is `len(a.shape)`, and is worth checking when writing functions that accept either a single sample or a batch of them.

## When reshape has to copy

`reshape` returns a view when the requested shape can be expressed as a stride pattern over the existing memory. A copy when it can't.

For a freshly created contiguous array, it's always a view.

After a transpose, it often isn't. The transposed array reads the buffer column-first. Flattening it in row-major order means gathering scattered values. Which needs new memory.

NumPy doesn't tell you which happened. `np.shares_memory(a, b)` does.

If you need a promise in the other direction, `a.shape = (3, 4)` assigns the shape in place and **raises** if a view is hopeless. That is a handy assertion. It fails loudly rather than silently copying. This Is just what you want in code where an accidental copy of a large array would be a speed bug.

## Row-major, column-major, and order=

C order, the default, means the **last** axis varies fastest. Reading `a.ravel()` on a `(2,3)` array gives the first row then the second.

Fortran order means the first axis varies fastest. Reading gives the first column then the second.

`reshape` and `ravel` both take `order="F"` to work column-first without changing the underlying data's actual layout. This Is at times the clearest way to express an step.

Genuine Fortran-sorted arrays &mdash; created with `np.asfortranarray` or `order="F"` &mdash; matter mainly when interfacing with Fortran or MATLAB-derived libraries. Some LAPACK routines are faster on them because they avoid an inner transpose.

For everyday work, staying in C order and not thinking about it's the right default. The time to care is when `flags` tells you an array isn't contiguous and a thing downstream is copying.

## reshape versus resize

They sound like a pair and aren't.

`np.reshape` returns a new view or copy with a other shape, leaving the first alone. The size must match.

`a.resize(shape)` modifies the array **in place** and can change the size, padding with zeros or truncating. It also refuses to run if the array shares memory with anything else. This Is a sensible protection and an occasional annoyance.

`np.resize(a, shape)` &mdash; the function, not the method &mdash; is other again. It repeats the data cyclically to fill the new shape.

Three likewise named steps with three other actions. `reshape` covers nearly all. The other two are worth recognising when you meet them rather than reaching for.

## Length-1 axes, and why they keep appearing

`np.newaxis` (which is just `None`) inserts an axis of length 1. `np.expand_dims` does the same thing as a function call. `np.squeeze` drops each length-1 axis, or a named one.

These exist almost fully to serve broadcasting. A length-1 axis is the one broadcasting will stretch. Inserting one is how you say "align this against that axis".

They also appear at the boundaries of libraries. A model that expects a batch gets a single sample wrapped with `x[None]`. A result that comes back as `(n, 1)` gets squeezed to `(n,)` before being handed to a thing expecting a vector.

A caution on `squeeze` with no args: it drops *all* length-1 axes. This Means a batch of one sample loses its batch dim too. In code that handles var batch sizes, that turns into an intermittent bug that only appears when the batch happens to hold one item. Naming the axis. `squeeze(axis=1)` &mdash; makes it safe.

## Debugging shape errors

Shape errors are the most common failure in array code. They're also the easiest to diagnose. The error message holds both shapes.

The routine that resolves nearly all of them:

Print the shapes of the inputs. Not the arrays. The shapes. Most of the time the mismatch is at once visible and the fix is obvious.

Ask which axis each one is supposed to represent. Shape errors are often a semantic mistake. Samples and features swapped, a batch axis missing. Rather than an math one.

Check whether a reduction removed an axis you needed. `keepdims=True` is the fix when the answer is yes.

And check `ndim` when a function accepts both single items and batches. A great many "this worked yesterday" bugs are a `(3,)` arriving where a `(1, 3)` was expected.

## Common shape mistakes

**given `reshape` reorders.** It doesn't rearrange values, only how they're grouped. If the values come out in an surprise setup, the data was in a other order than assumed. Reshaping again won't fix it &mdash; a transpose might.

**Using `reshape` to transpose.** `a.reshape(4, 3)` on a `(3, 4)` array isn't `a.T`. Both give a `(4, 3)` result and they hold other values in other places. This is a truly common bug because the shapes match and nothing raises.

**`squeeze()` with no arg** in code that handles var batch sizes. It drops each length-1 axis. A single-item batch loses its batch dim.

**Leaning on `reshape` returning a view.** It often does and at times doesn't. `np.shares_memory` answers it. Assigning to `.shape` enforces it.

**Losing an axis to an int index** and then being surprised when broadcasting fails. `a[:, 0]` gives `(3,)`. `a[:, 0:1]` gives `(3, 1)`.

## Questions people ask

<strong>What does -1 mean in reshape?</strong> It asks NumPy to infer that axis length from the total size. a.reshape(-1, 3) gives rows of three, whatever the count.

<strong>Does reshape copy the data?</strong> Usually not, it returns a view when the memory layout allows. If it cannot, such as after certain transposes, it quietly copies.

<strong>What is the difference between ravel and flatten?</strong> ravel returns a view when possible, while flatten always returns a copy. Use flatten only when you need to modify the result independently.

<strong>Why do I get 'cannot reshape array of size 12 into shape (5, 3)'?</strong> The product of the new shape must equal the element count. 5 times 3 is 15, not 12.

<strong>What is a shape of (5,) versus (5, 1)?</strong> The first is a flat vector with one axis. The second is a column with two axes, and the two broadcast very differently.

<strong>How do I add a length-1 axis?</strong> Index with None, as in a[:, None], or call np.expand_dims. reshape also works.

## Reading a shape error

The error message holds all needed, and reading it beats guessing.

"operands couldn't be broadcast together with shapes (3,4) (3,)" names both shapes. Align them from the right: 4 against 3. They aren't equal and neither is 1. It fails. The fix is either `keepdims=True` on what made the `(3,)`, or an clear `[:, None]`.

"can't reshape array of size 12 into shape (5,5)" is an math statement: 12 isn't 25. A thing upstream made a other amount of data than expected. The reshape is reporting it rather than causing it.

"matmul: Input operand 1 has a mismatch in its core dim" means the inner dims of a mat product don't agree. Print both shapes and check which axis is meant to be the shared one.

In each case the productive move is the same. Print the shapes of the inputs, decide what each axis is supposed to mean. Fix the one that is wrong. Shape errors are almost always semantic. A transposed input, a missing batch axis, a reduction that removed a thing &mdash; rather than math.
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
intro: Elements, rows and rectangles - and the one action that differs from lists in a way that matters.
## One index per axis

Indexing a NumPy array works differently from indexing a Python list. The syntax looks similar, but the semantics differ in ways that matter for both correctness and performance.

The fundamental rule is one index per axis, separated by commas. A 2-D array uses two indices: one for the row, one for the column. Writing a[1, 2] gives you the element at row 1, column 2. That comma-separated form is both the idiomatic style and the faster one.

The alternative, a[1][2], works but creates an intermediate array. The first index selects the entire row as a 1-D array. The second index then selects from that temporary. For a single element the overhead is small. Inside a loop it adds up. More importantly, the chained form does not generalize to fancier indexing patterns.

Slicing returns a view, not a copy. A slice like a[0:3, 1:4] gives you a rectangular sub-array that shares memory with the original. Writing to the slice changes the original. That is a deliberate design choice. It saves memory and makes slice assignment a natural way to fill parts of an array.

The combination of integer indexing and slicing in the same expression is allowed. a[:, 2] gives you all rows of column 2 as a 1-D array. a[1, :] gives you all columns of row 1. These mixed forms appear constantly in real code.

Step values work as in Python lists. a[::2] gives every other element. a[::-1] reverses. Both return views. Combining steps across multiple axes selects a regular sub-grid of the array.

This module covers single-element indexing, slicing, step values, and the difference between views and copies in the context of slicing. Understanding these basics makes the next modules on boolean masking and fancy indexing straightforward.


A comma splits axes, so `a[1, 2]` means row one, column two. That is the idiomatic form and the fast one.

`a[1][2]` reaches the same element by first making row one as an array, then indexing that. For reading a single value the gap is small. Inside a loop it's a temporary array per loop.

Minus indices count from the end, just as in Python. `a[-1, -1]` is the last element of the last row.

Indexing with fewer indices than axes gives you all in the left ones. On a `(3, 4)` array, `a[1]` is a row of four.

## Slices, per axis

Indexing and slicing are the operations you perform most often on a NumPy array. They control which elements you read, which you write, and how you carve sub-arrays out of a larger block. Getting them right is the foundation for every later topic.

NumPy extends the familiar Python slice syntax to multiple dimensions. Each axis gets its own start, stop and step, separated by commas. A single expression can select a rectangular block from a matrix, every other row from a 3-D tensor, or a reversed column from a table. That composability is what makes array code compact.

The key difference from Python lists is that a NumPy slice returns a view, not a copy. The slice and the original share the same memory. Writing through the slice changes the original. That behaviour is a deliberate design choice: it saves memory and makes in-place updates natural. But it also means that modifying a slice can change data you thought was separate, which surprises anyone coming from Python lists.

Integer indexing also behaves differently across dimensions. A comma separates axes, so a single expression addresses a specific element without building intermediate arrays. That matters for both readability and performance.

Beyond basic indexing, NumPy supports boolean masks and fancy indexing with arrays of indices. Those are covered in their own modules. The concepts here -- per-axis indexing, slice views, and the comma separator -- are the foundation those later topics build on.

This module covers single-element access, slicing with start, stop and step, mixed integer-and-slice expressions, and the view behaviour that differs from lists. The examples use small arrays where you can verify the result by counting elements.

The familiar `start:stop:step`, once per dim.

`a[1:3]` takes rows. `a[:, 1:4]` takes columns. `a[1:3, 1:4]` takes both and gives you a rectangle. `a[::2]` takes every other row. `a[:, ::-1]` reverses the columns.

This composability is most of what makes array code compact. A block of a mat, a channel of an image, each second sample of a signal. All are one formula.

## Slices are views

Here is the action that differs from lists, and it catches nearly everybody once.

Slicing a **list** copies. Slicing an **array** gives you a view onto the same memory. Writing through the view changes the first.

```python
arr = np.arange(5)
view = arr[1:4]
view[0] = 99        # arr is now [0, 99, 2, 3, 4]
```

That is deliberate and valuable: slicing a large array costs nothing. You can pass windows around freely without copying gigabytes. It's also a source of bugs when a function slices its input, modifies the slice. Unintentionally alters the caller's data.

The defence is to be clear. `arr[1:4].copy()` when you need freedom. `np.shares_memory(a, b)` when you aren't sure what you've. There's a whole module on this later. It applies to more steps than slicing.

## Ellipsis

Trailing axes you don't mention are taken whole. On a three-dimensional array `a[0]` gives you all under index zero.

`...` stands for as many axes as needed, wherever it appears. `a[..., 0]` is the first element along the **last** axis, what the number of leading axes.

That is truly handy in code that handles arrays of varying dimensionality: `a[..., -1]` takes the last column of a 2-D array, the last channel of a 3-D one. The same thing again for higher dims, without a special case.

## Assigning into a selection

Anything you can select, you can assign to, and the set happens in place.

A scalar fills the whole region: `a[1] = 5` sets each element of row one. An array must match the shape of the target. Or be broadcastable to it. This Is the next module.

Getting a length wrong raises rather than doing a thing surprising. This Is the action you want. It's also a solid early sign that an upstream shape isn't what you assumed.

## The axis-dropping rule

This is small, easy to miss, and shows a great deal of later confusion.

An **int** index drops that axis. `a[1]` on a `(3, 4)` array gives shape `(4,)`.

A **slice** keeps it. `a[1:2]` gives shape `(1, 4)`.

The same applies to columns: `a[:, 2]` is `(3,)` while `a[:, 2:3]` is `(3, 1)`.

Both hold the same three numbers. They behave fully differently the moment they meet another array.

Broadcasting aligns shapes **from the right**. Against a `(3, 4)` array, a `(3,)` column checks 4 with 3 and **raises**. though it came out of that very array. The `(3, 1)` version checks 4 with 1, stretches, and works.

The last editor shows just that: the same column, taken two ways, one of which is an error. It's worth running. "I sliced this out of the array so it fits" is a fair-sounding assumption that is simply false.

When an step gives you a oddly large result, or complains about shapes that "obviously" match, this is the first thing to check.

## Negative indices and reversal

Minus indices count from the end, just as in Python lists. `a[-1]` is the last element, `a[-2]` the second last.

They work per axis, so `a[-1, -1]` is the bottom-right element of a 2-D array. `a[:, -1]` is the last column.

A minus step reverses. `a[::-1]` gives the array backwards. It's a **view**. No data is copied, the stride is simply minus. That makes reversal free. This Is why sorting descending is written as `np.sort(a)[::-1]` without any speed concern.

On more than one axis, each gets its own direction: `a[::-1, :]` reverses the rows and leaves the columns. `a[::-1, ::-1]` reverses both. This Is a 180-degree rotation.

## Steps

The third slice part is the step. `a[::2]` takes each second element, `a[1::2]` each second starting from the first.

Strided slices are views, because a regular step is just what a stride can express. That is worth knowing when working with large arrays. Downsampling an image by taking each fourth pixel costs nothing until you write to the result.

Mixing a step with a minus direction works but reads badly. `a[::-2]` is one of the few slice forms worth writing a comment for.

## Out of range: slices clip, indices raise

This skew catches people.

`a[100]` on a ten-element array raises `IndexError`.

`a[5:100]` on the same array returns five elements. Slices clip silently to what exists.

Both actions are defensible &mdash; an out-of-range index has no real answer, while an out-of-range slice does &mdash; but the inconsistency means a slice-based bug makes a short array rather than an exception. The failure surfaces one spot else.

If a slice must give a exact length, check the length rather than given it. `assert len(chunk) == n` at the point of slicing localises the problem far better than a shape error three functions later.

## Assignment through a selection

Anything you can select, you can assign to. The value must either match the pick's shape or broadcast to it.

`a[0] = 5` fills the first row with fives, broadcasting the scalar.

`a[0] = [1, 2, 3]` sets the row, needing just three values.

`a[0] = [1, 2]` raises. Two values neither match three nor broadcast to it.

set also **converts silently to the array's dtype**. Assigning 3.7 into an int array stores 3. Assigning a long string into a fixed-width string array truncates it. Neither warns. This is a direct result of the array owning its dtype. The block can't change type to accommodate what you put in it.

## The rule that explains the shapes

There's one rule that predicts the shape of any basic pick:

**An int drops an axis. A slice keeps it.**

`a[0]` on a `(3, 4)` array gives `(4,)`. The row axis is gone.

`a[0:1]` gives `(1, 4)` &mdash; the axis lives with length one.

`a[:, 0]` gives `(3,)`. `a[:, 0:1]` gives `(3, 1)`.

That last pair is the one that matters because the `(3, 1)` form broadcasts down a column and the `(3,)` form doesn't. When a broadcast fails on a thing you expected to work, an int index that dropped an axis is a likely cause.

## A note on tuples

`a[0, 1]` and `a[(0, 1)]` are the same thing. The comma builds a tuple. NumPy reads a tuple as one index per axis.

`a[[0, 1]]` is a **list** and means a thing else fully: fancy indexing, selecting rows 0 and 1.

That gap between a tuple and a list inside brackets is invisible at a glance and changes both the meaning and whether you get a view. It's worth being deliberate about, above all when the index is built programmatically. A list assembled in a loop and passed as an index does fancy indexing. `tuple(...)` around it's the fix when you meant per-axis pick.

## Indexing that is built programmatically

When an index is assembled at runtime rather than written truly, the tuple-versus-list gap turns a real hazard.

`a[tuple(idx)]` selects one element per axis. `a[list(idx)]` does fancy indexing along the first axis. The two give fully other results from the same values, and neither raises.

For code that builds indices dynamically, `tuple()` around the result makes the intent clear and matches what NumPy expects for per-axis pick.

`np.s_` is a small convenience for storing a slice as a value: `sl = np.s_[1:3, ::2]` can be passed around and applied later as `a[sl]`. It's handy for configurable windows. Clearer than making `slice(1, 3)` objects by hand.

## Views, once more

each basic slice is a view. That is the single most consequential fact in this module. It's worth stating in its hands-on form:

**Writing into a slice writes into the first.**

`a[1:3] = 0` sets elements of `a`. `b = a[1:3]. B += 1` also modifies `a`. A function that slices its arg and writes to the slice modifies the caller's array.

This isn't a flaw. It's why slicing large arrays costs nothing and why NumPy code can pass windows around freely. But it differs from Python lists. Here `a[1:3]` is a copy. That gap is the source of a whole group of surprising bugs for people arriving from plain Python.

`np.shares_memory(a, b)` settles any exact case. `copy()` breaks the link when you want it broken.

## A summary of the selection forms

`a[i]` &mdash; one element or one sub-array. Drops an axis.

`a[i:j]` &mdash; a range. Keeps the axis. A view.

`a[i:j:k]` &mdash; a strided range. Still a view.

`a[::-1]` &mdash; reversed. Still a view.

`a[i, j]` &mdash; one index per axis, via a tuple.

`a[..., j]` &mdash; the last axis, what the dimensionality.

`a[None]` &mdash; a new length-1 axis at the front.

`a[mask]` &mdash; boolean pick. A copy.

`a[[i, j]]` &mdash; fancy indexing. A copy. Can reorder and repeat.

The first seven are views and free. The last two allocate. Get modules of their own. Knowing which group an formula falls into predicts both its cost and whether writing to the result affects the first. Which between them shows most of NumPy's indexing action.

## Questions people ask

<strong>What is the difference between a[1][2] and a[1, 2]?</strong> They give the same value on a 2D array, but a[1][2] builds an intermediate row first. Prefer the comma form, which is faster and works with slices.

<strong>Do slices copy the data?</strong> No, a slice is a view onto the same memory. Changing it changes the original, so call .copy() when you need independence.

<strong>What does a[::-1] do?</strong> It reverses the array along that axis using a negative step. The result is a view, not a copy.

<strong>Why does indexing one row drop a dimension?</strong> An integer index removes that axis, while a slice keeps it. a[1] has shape (n,) but a[1:2] has shape (1, n).

<strong>What does the ellipsis mean in an index?</strong> It stands in for as many full slices as needed. a[..., 0] picks the first entry along the last axis whatever the number of dimensions.

<strong>What happens if a slice goes past the end?</strong> Slices clip silently and never raise. A single integer index out of range does raise an IndexError.

## A closing note

Indexing is where NumPy diverges most visibly from plain Python, in two ways that both matter.

A slice is a view rather than a copy. Writing through it reaches the first. And an int index drops an axis while a length-one slice keeps it. This Decides whether a later broadcast succeeds.

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
print("   start      shared:", shared, " alias:", alias)

shared += 1                   # writes into the buffer both names see
print("   after +=   shared:", shared, " alias:", alias, "<- followed")

shared = shared + 1           # rebinds shared; alias still points at the old
print("   after = +  shared:", shared, " alias:", alias, "<- left behind")'''),

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
intro: showing the step instead of writing the loop. The two habits that undo the gain.

## Operators apply to every element

The defining feature of NumPy arrays is that arithmetic operators work elementwise. Adding two arrays adds corresponding elements. Multiplying by a scalar multiplies every element. There is no loop in Python. The operation happens in compiled code, and the result is a new array of the same shape.

That elementwise behaviour is what makes NumPy fast. The same computation written as a Python loop would be a hundred times slower, because each iteration would need to look up the type of each element, call the operator, and build a new Python object for the result. The NumPy version does none of that. It knows the type once and loops in C.

Every standard arithmetic operator works this way. Addition, subtraction, multiplication, division, integer division, modulus, and exponentiation all apply elementwise. So do comparison operators. a > 5 gives a boolean array with True where the condition holds and False where it does not.

Scalar operands are broadcast automatically. a + 10 adds ten to every element. a * 0.5 halves every element. The scalar is not expanded into a full array. NumPy reuses the value at each step of the compiled loop. That is both faster and more memory-efficient than creating a temporary array of tens.

The one operator that surprises people is the asterisk. On arrays, a * b is elementwise multiplication. It is not matrix multiplication. Matrix multiplication uses the @ operator, or np.dot, or np.matmul. Confusing the two gives an array of the same shape but entirely wrong values, with no error or warning.

This module covers the arithmetic operators, the comparison operators, and the difference between elementwise and matrix multiplication. It also covers the NumPy functions like np.sqrt and np.exp that apply elementwise and replace the math-module equivalents for array inputs.


`a + b` adds the arrays elementwise. So do `-`, `*`, `/`, `//`, `%` and `**`. A scalar applies to each element: `a * 10` scales the whole array.

The one to be careful with is `*`. On arrays it's **elementwise product**, not mat product. mat product is `@`. Confusing the two makes an array of the wrong shape or, worse, the right shape and the wrong numbers. That has its own module later.

checks work the same way and give a boolean array: `a > 2` is `[False, False, True, True]`, not a single answer. Using that in an `if` raises. NumPy refuses to guess whether you meant "any" or "all".

## ufuncs

The math functions come in array form: `np.sqrt`, `np.exp`, `np.log`, `np.sin`, `np.abs`. These are called universal functions. They apply elementwise to a whole array in compiled code.

Python's `math` module doesn't. `math.sqrt` takes one number and raises on an array. Reaching for `math` inside a loop over an array is one of the two common ways to lose all NumPy offers.

## Division by zero does not raise

This surprises people coming from plain Python.

Float division by zero makes `inf`, `-inf` or `nan` and emits a RuntimeWarning. It doesn't stop. That follows the IEEE floating-point standard. It's the right default for array work. One bad element in a million shouldn't abort the whole math.

The result is that you must look for those values later rather than leaning on an exception. `np.isnan` and `np.isfinite` are how. There's a module on missing data later.

`np.errstate` controls the warnings when you're making them on purpose. This Is what the third editor uses to keep its output readable.

## In place or not

`a += 1` modifies the existing array. `a = a + 1` builds a new array and rebinds the name.

Two reasons to care.

**Memory.** The second form allocates a full-size temporary. In a chain like `a = a * 2 + b * 3`, a few temporaries exist at once. This Matters when arrays are large.

**Aliasing.** If a thing else holds a link to the same array. Another var, a list, a caller's data. The in-place form changes what they see and the rebinding form doesn't. The fourth editor shows an alias tracking one and being left behind by the other.

Neither is right . In-place is cheaper and can surprise. Allocation is safer and costs memory. What matters is knowing which one you wrote.

## The two ways to lose the benefit

**Looping over an array in Python.** This is the big one. Reading `a[i]` from Python boxes that value into a Python object. Doing that in a loop is slower than the same loop over a list. You get the memory layout of an array and none of the speed. The fifth editor measures it.

**Calling scalar functions per element.** `math.sqrt(a[i])` in a loop, or a Python function applied one value at a time. `np.vectorize` looks like a fix and isn't. It's a convenience wrapper that still loops in Python. Its own docs says so.

If you find yourself indexing an array inside a `for`, the handy question is what whole-array formula would give the same result.

## Converting a loop

The common shape is a loop with a rule, and it converts in two steps.

Find the branches for the **whole** array, then combine them with a mask. `np.where(rule, if_true, if_false)` chooses elementwise.

That does more math than the loop. It tests both branches all over. And is still sharply faster. The math happens in compiled code and the loop doesn't.

It also reads better once you're used to it. The rule and the two outcomes are each one formula, rather than being spread across a loop body.

Where both branches are costly, or one is invalid for some inputs, masking gets more careful. And that is the boolean-masking module.

## The ufunc machinery

A ufunc isn't just a function that happens to work elementwise. It's an object with methods. Three of them are worth knowing.

`np.add.reduce(a)` is `a.sum()`. each binary ufunc has a `reduce`. `np.times.reduce` gives a product, `np.max.reduce` gives a max, and `np.logical_and.reduce` gives an all.

`np.add.build up(a)` is `a.cumsum()`. The same generalisation: a running use of the step.

`np.add.outer(a, b)` applies the step to each pair, giving a mat from two vectors. `np.times.outer` is the outer product. `np.subtract.outer` gives a gap mat. This Is a one-line distance math.

These matter because they cover steps with no dedicated function. There's no `np.cummax`. `np.max.build up` is just that. It's the standard way to find a running high-water mark.

Ufuncs also accept `where=`. This Applies the step only where a mask is True and leaves the rest of the output untouched. Mixed with `out=`, that is gated math without a branch or an mid array.

## Comparison and logic are ufuncs too

`a > b` is `np.greater(a, b)`. `a == b` is `np.equal`. They broadcast, they take `out=`, they've `reduce`.

That last one is handy: `np.logical_or.reduce(masks)` mixes a list of masks. This Is cleaner than chaining `|` when the number of rules isn't known in advance.

The bitwise ops `&`, `|` and `~` are the array versions of `and`, `or` and `not`. The Python keywords don't work on arrays at all. They raise. Python needs a single truth value and an array has many. That error message, "the truth value of an array with more than one element is ambiguous", is one of the most often seen in NumPy. It always means the same thing: replace `and` with `&`, and add parentheses.

## Controlling floating-point warnings

`np.errstate` is a context manager that decides what happens on division by zero, overflow, underflow and invalid steps.

The options are `"warn"` (the default for most), `"skip"`, `"raise"` and `"call"`.

Two settings are worth knowing about. `np.errstate(all="raise")` turns silent NaN production into an exception. This Is invaluable when hunting a NaN that appears one spot in a long pipeline. It stops at the step that created it rather than at the point where you noticed.

`np.errstate(divide="skip", invalid="skip")` suppresses the warnings when the action is intentional. This Keeps genuine warnings visible instead of drowning in expected ones.

`np.seterr` sets the same options globally. This Is convenient in a notebook and inadvisable in a library. It changes action for all else's code too.

## When a loop is still the right answer

Vectorisation is the default, not a rule.

**When each step depends on the last.** Models, iterative solvers, anything where element `n` needs the found value of element `n-1`. Some of these have array formulations. A cumulative sum, an steep moving mean via `lfilter`. But many truly don't.

**When the array is small.** Under a few hundred elements, the per-call cost of NumPy dominates and a list comprehension can be faster. Measure before given.

**When the vectorised version is unreadable.** A three-line loop that a colleague understands is often better than a one-line formula with four `newaxis` insertions that no one can modify safely. This is a real engineering trade-off, not a failure of nerve.

**When it would allocate too much.** Some vectorised formulations build a large mid. The classic being an n-by-n distance mat for large n. A loop over chunks can be the only version that fits in memory.

The honest framing: reach for vectorisation first. It's often shorter and much faster. Fall back to a loop when the problem is sequential, the data is small, or the vectorised form costs more in clarity or memory than it returns in speed.

## np.vectorize is not vectorisation

The name is misleading enough to be worth a warning.

`np.vectorize(f)` wraps a scalar function so it accepts arrays. It handles broadcasting and dtype for you, and it's truly convenient.

It's **a loop underneath**. The docs says so. It gives the interface of a ufunc without the speed. Code that uses it expecting a speed gain gets none.

Its real use is convenience: applying an existing scalar function to an array without rewriting it. Here The array is small enough that speed doesn't matter. For anything in a hot path, the function needs to be rewritten by array steps, or compiled with something like Numba.

## Integer division and the modulo operator

`//` and `%` work elementwise like all else, and both have an edge worth knowing.

int division by zero doesn't give infinity. Ints have no infinity. It makes 0 and a warning. This Is arguably worse than a NaN because it looks like a legitimate answer.

`%` follows Python's sign rule rather than C's. The result takes the sign of the divisor. `-7 % 3` is 2, not -1. That matches plain Python and differs from many other languages. This Matters when porting an method.

`np.divmod` returns both at once and is faster than finding them apart.

## Power, and the integer surprise

`a ** 2` on an int array stays int. Can overflow just as product does.

`a ** -1` on an int array **raises**. A minus power of an int isn't an int. This is a deliberate change from older NumPy. This Returned nonsense. Convert to float first.

`np.sqrt` of a minus float gives NaN with a warning, not a complex number. If complex results are wanted, the input must already be complex: `np.sqrt(np.array([-1+0j]))` gives `1j`. NumPy won't silently promote a real array to complex. Doing so would change the dtype of all downstream.

## Rounding, and the rule that surprises people

`np.round` uses **banker's rounding**: exact halves round to the nearest even number. `np.round(0.5)` is 0 and `np.round(1.5)` is 2.

This is deliberate. Always rounding halves upward adds a systematic upward bias when blending many rounded values. Rounding to even cancels it out.

It's also not what most people expect. It's worth knowing before writing a test that asserts `round(0.5) == 1`.

`np.floor`, `np.ceil` and `np.trunc` have no such subtlety. Note that `trunc` and `floor` differ for negatives: `floor(-1.5)` is -2, `trunc(-1.5)` is -1.

Converting to int with `astype(int)` truncates toward zero. This Is `trunc`, not `round`. That gap makes off-by-one results in just the places that are hardest to notice.

## Questions people ask

<strong>What does vectorised mean?</strong> The operation applies to the whole array in one call, with the loop done in compiled code. You write a + b instead of looping over elements.

<strong>What is a ufunc?</strong> A universal function, such as np.add or np.exp, that operates element by element and supports broadcasting, out= and dtype arguments.

<strong>Why is x / 0 not an error?</strong> NumPy follows IEEE floating point and returns inf or nan with a warning. Use np.errstate to control or raise on those cases.

<strong>How do I apply a custom Python function?</strong> First try to express it with ufuncs and np.where. np.vectorize only hides the loop and is no faster.

<strong>What does the out argument do?</strong> It writes the result into an existing array instead of allocating a new one. That saves memory and time in repeated calculations.

<strong>Is a / b the same as a // b?</strong> No. / always gives floats, while // is floor division and keeps integer types for integer inputs. Mind the rounding on negative numbers.

## A checklist for converting a loop

When replacing a Python loop with array steps, the questions in order:

**Does each loop depend on the previous one?** If yes, it may not vectorise. Check whether it's a cumulative step in disguise. `cumsum`, `cumprod`, `max.build up` cover more cases than people expect.

**Is there a gated inside?** `np.where` for two branches, `np.select` for more, or a boolean mask if the step applies to a subset.

**Is it building a list?** Preallocate the output array and assign into it, or express the whole thing as one formula.

**Is it mixing each pair?** That is broadcasting with a `None` insertion. It's worth checking the resulting size before running it.

**Is it a reduction?** `sum`, `max`, `any` with the right `axis`, rather than building up in a Python var.

Most loops in numeric code fall into one of those five. The ones that don't are often truly sequential. Are the right place for a loop. Or for Numba, if the loop is the bottleneck.
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

If you have ever added a scalar to an array, you have already used broadcasting. NumPy stretched the scalar to match the shape of the array without creating a copy. That stretch is broadcasting. The general rules extend the same idea to arrays of different shapes.

Broadcasting matters because it eliminates temporary arrays. Without it, adding a bias to every row of a matrix would require you to tile the bias vector into a full matrix first. That tile allocates memory, fills it with copies, and then gets thrown away after the addition. Broadcasting skips all of that. The bias vector is reused in place.

The rules are mechanical. NumPy compares shapes from the trailing axis backward. Two dimensions are compatible if they are equal or if one of them is one. A missing dimension is treated as one. When a dimension is one, that axis is stretched to match the other array. If any pair of dimensions is neither equal nor one, the operation raises a ValueError.

The most common broadcasting patterns cover the cases you encounter daily. A scalar with any array. A 1-D array with a 2-D array along one axis. A column vector with a row vector to produce a 2-D result. Each of these follows the same rules, and once you can predict the output shape, you can write the code without trial and error.

Shape errors from broadcasting are among the clearest error messages in NumPy. The message names the two shapes and says they are not compatible. If you see one, print the shapes of both operands and walk through the rules. The fix is usually a reshape or a newaxis to add the missing dimension.

The common mistake is adding a dimension in the wrong place. A (3,) array broadcast with a (4, 3) array works along columns. The same array reshaped to (3, 1) would broadcast along rows. The position of the one decides the axis of the stretch. Getting that right is the whole skill.

This module covers the broadcasting rules, the common patterns, how to predict the output shape, and how to add dimensions with np.newaxis or reshape to make two arrays compatible.


`a + 10` on a `(2, 3)` array adds ten to each element. Conceptually the scalar is stretched to `(2, 3)`. nothing is copied and NumPy simply reuses the value as it walks.

That is broadcasting. The general rules extend the same idea to arrays.

## The rules

Line the shapes up **from the right** and compare them pair by pair. Each pair must meet one of:

- the dims are **equal**, or
- one of them is **1**, in which case it's stretched, or
- one shape has **run out** of dims, in which case it's treated as 1.

If each pair passes, the result takes the larger of each pair. If any pair fails, you get a `ValueError` that prints both shapes. Which is truly helpful once you know to read it right-aligned.

So `(3, 4)` and `(4,)` work: 4 against 4, then 3 against nothing. `(3, 4)` and `(3,)` fail: 4 against 3.

That second one catches people constantly. The 3 "obviously" matches the rows. It doesn't, because alignment starts from the right.

## Rows are the default

A 1-D array of length *n* aligns with the **last** axis. Against a `(2, 3)` array, a `(3,)` array gives one value per column.

To get one value per **row** you need shape `(2, 1)`. The idiomatic way is `v[:, None]`. This Inserts a trailing axis and turns `(2,)` into `(2, 1)`.

This is the single most handy thing to internalise about broadcasting. It's what norming by row or column comes down to:

```python
a - a.mean(axis=0)              # subtract the column means
a - a.mean(axis=1)[:, None]     # subtract the row means
```

The first works because `mean(axis=0)` gives one value per column. This Aligns on its own. The second needs the extra axis. Without it either raises or. If the array happens to be square. Silently does the wrong thing. That last case is worth fearing. On a square array both alignments are legal and only one is what you meant.

## Nothing is copied

Broadcasting doesn't materialise the stretched array. NumPy adjusts its stride bookkeeping so that walking the small array repeats values. The step reads them as if they were there.

So broadcasting itself is cheap. What can be costly is the **result**.

## The accidental grid

A column `(n, 1)` and a row `(1, m)` broadcast to `(n, m)`. That is just what you want for an outer product or a distance mat. It's the classic way to exhaust memory by accident.

Two arrays of ten thousand elements each. 80 KB apiece. Combine into a hundred million elements. This Is 800 MB in `float64`. Nothing warns you. The formula looks small.

When an step is unexpectedly slow or the process dies, this is the first thing to check. `np.broadcast_shapes` gives you the answer without allocating anything. It's a good habit when an formula mixes arrays whose shapes you haven't thought about carefully.

## Inspecting

`np.broadcast_shapes(s1, s2)` returns the result shape, or raises with the same error the real step would.

`np.broadcast_arrays(a, b)` returns views stretched to the common shape. This Is handy for seeing what the operands look like after alignment. They're views. The memory stays small. And they're read-only for that reason.

`np.newaxis` (which is just `None`) inserts an axis wherever you need one. Is the tool for making shapes line up on purpose rather than hopefully.

## A working habit

When two arrays combine, ask what shape you expect the result to be, and check.

If the answer is bigger than either input, you're creating a grid. Make sure that is what you meant. If an step raises, right-align the two shapes on paper and find the pair that disagrees. And when adding a per-row quantity to a mat, write `[:, None]` on purpose rather than discovering whether it was needed.

## Nothing is allocated

This is the part that makes broadcasting worth understanding rather than merely handling.

When a `(1000, 1)` array broadcasts against a `(1, 1000)` array, NumPy doesn't build two `(1000, 1000)` arrays and then combine them. It sets the stride along the broadcast axis to **zero**. Reading any spot along that axis returns the same element.

A zero stride means "don't move". That single trick is the entire setup. It's why broadcasting costs nothing in memory.

You can see it right. `np.broadcast_to(a, shape)` returns the stretched view. Its strides hold zeros where stretching happened. The result is marked read-only. Writing to a spot that maps to the same memory from a thousand directions has no sensible meaning.

The output, is fully materialised. A `(1000, 1000)` result is eight megabytes what made it. Broadcasting saves the inputs, not the output. That gap is what the accidental-grid problem is about.

## The patterns worth recognising

Four shapes of problem cover most real broadcasting.

**Centring or scaling a table.** Subtracting a per-column mean is `a - a.mean(axis=0)`. Works with no extra syntax because `(n_cols,)` already aligns with the last axis. Per-row needs `keepdims=True`.

**Pairwise differences.** `a[:, None] - b[None, :]` gives each mix. With a further reduction it turns a distance mat: `np.sqrt(((a[:, None] - b[None, :]) ** 2).sum(axis=-1))`. This is the standard formulation. It's also the standard way to run out of memory. The mid is `(len(a), len(b), n_features)`.

**One-hot encoding.** `labels[:, None] == np.arange(n_classes)` gives a boolean mat with one True per row. Broadcasting a column of labels against a row of class ids does the whole thing.

**Applying per-channel params.** An image of shape `(h, w, 3)` and a per-channel scale of shape `(3,)` times right. The trailing axes align. This is why image code broadcasts so cleanly when the channel axis is last. Why it needs a `[:, None, None]` when the channel axis is first.

## When to use einsum instead

Once an formula needs three or four `None` insertions, it has stopped being readable, and `np.einsum` is often clearer.

`np.einsum("ij,jk->ik", a, b)` is mat product. `np.einsum("ij,ij->i", a, b)` is a row-wise dot product. This Written with broadcasting needs a times and a sum with the right axis.

The subscript string names each axis. The arrow says which live. Axes that appear on the left but not the right are summed over. Axes repeated between operands are matched.

It isn't always faster &mdash; at times a lot slower than the equal `matmul`. It's more general and less specialised. Its edge is that the intent is written down. An einsum string can be read. A chain of `newaxis` insertions and transposes often can't.

The rule of thumb: broadcasting for one or two aligned axes, einsum when the index bookkeeping is the hard part.

## Guarding against the accidental grid

The failure mode of broadcasting isn't an error. It's a result of the wrong shape that flows onward.

Subtracting a `(1000,)` array from a `(1000, 1)` array gives `(1000, 1000)`. Both inputs are eight kilobytes. The result is eight megabytes. Nothing warns. Each rule was followed.

Three defences, in growing order of formality.

**Print the shape.** For interactive work, checking `result.shape` after any broadcasting formula catches this at once.

**Assert it.** In code that matters, `assert result.shape == (n,)` docs the intent and fails at the right place.

**Predict it first.** `np.broadcast_shapes((1000, 1), (1000,))` returns the result shape without finding anything. This Is how you check a broadcast against a large array without allocating the answer.

## The habit that prevents most of it

Broadcasting errors and broadcasting surprises come from the same source: not knowing the exact shape of one of the operands.

Two things prevent nearly all of them.

Be clear about columns. `x[:, None]` says "this is a column" unambiguously. Reads better than leaning on a reduction to have kept an axis.

Use `keepdims=True` on any reduction whose result will be used against the first array. It costs nothing, it makes the intent visible. It drops the skew where centring by column works and centring by row raises.

Both are about writing down the shape you mean instead of leaning on it happening to be right. Which is a fair summary of how to work with broadcasting .

## Reading a broadcast error

The message is more helpful than it first looks.

"operands couldn't be broadcast together with shapes (3,4) (3,)"

Write the shapes right-aligned:

```
(3, 4)
   (3,)
```

Compare from the right: 4 against 3. Neither is 1 and they aren't equal. It fails. Axis 0 is never reached.

Once you read it that way, the fix is often obvious. Either the `(3,)` should have been `(3, 1)`. A column. This Broadcasts down the rows. Or one of the arrays is transposed scaled to what was intended.

The most common origin by far is a reduction that dropped an axis. `a.mean(axis=1)` on a `(3, 4)` array gives `(3,)`. Using that against `a` fails for just this reason. `keepdims=True` gives `(3, 1)` and it works.

## The asymmetry worth internalising

Because alignment is from the right, steps along the **last** axis need no help and steps along the first do.

Centring a table by column: `a - a.mean(axis=0)` works right. `(4,)` aligns with the trailing 4.

Centring by row: `a - a.mean(axis=1)` fails, and needs `keepdims=True`.

This skew isn't any &mdash; it falls straight out of the right-alignment rule &mdash; but it does mean that two steps which sound even aren't. Only one of them tells you.

Worse, on a **square** array both work. 4 against 4 is legal in either direction. Code developed and tested on square arrays can be wrong in a way that only appears on rectangular data. The failure is a wrong answer rather than an exception.

That is a good reason to use `keepdims=True` by default on any reduction whose result feeds back into the first array, rather than only where it's needed.

## Broadcasting with more than two dimensions

The rules don't change. There are just more axes to align.

`(8, 1, 6, 1)` against `(7, 1, 5)` right-aligns as:

```
(8, 1, 6, 1)
   (7, 1, 5)
```

Missing leading axes are treated as 1. Then, per column: 1 against 7 gives 7. 6 against 1 gives 6. 1 against 5 gives 5. And the leading 8 has nothing to compare against. It lives. The result is `(8, 7, 6, 5)`.

That is 1,680 elements from inputs of 48 and 35. The expansion is the point of the method and also the hazard. On real sizes it's how a plausible formula allocates a hundred gigabytes.

`np.broadcast_shapes` finds this without allocating anything. This Is the safe way to check an formula before running it on real data.

## Questions people ask

<strong>What are the broadcasting rules?</strong> Compare shapes from the rightmost axis backwards. Two axes are compatible when they are equal or one of them is 1, and a missing leading axis counts as 1.

<strong>Does broadcasting copy the data?</strong> No. NumPy reads the length-1 axis repeatedly using a stride of zero, so the small array is never physically expanded.

<strong>How do I subtract a column mean from each column?</strong> Compute a.mean(axis=0), which has shape (columns,), and subtract it. The shape lines up with the last axis so it broadcasts across the rows.

<strong>How do I subtract a row mean from each row?</strong> Use a.mean(axis=1, keepdims=True), giving shape (rows, 1). Without keepdims the shape is (rows,) and will not line up with the columns.

<strong>What does 'operands could not be broadcast together' mean?</strong> Somewhere a pair of axes differ and neither is 1. Print both shapes, align them from the right, and find the first mismatch.

<strong>How do I build a pairwise table of two vectors?</strong> Add a new axis with None or np.newaxis so one becomes a column. A[:, None] - B[None, :] gives every difference in one shape (len A, len B) array.

## A summary of the tools

`x[:, None]` &mdash; make a column. The most-used piece of broadcasting syntax.

`x[None, :]` &mdash; make a row. Often silent. A 1-D array already behaves as a row.

`keepdims=True` &mdash; keep the reduced axis so the result aligns back.

`np.broadcast_shapes(...)` &mdash; predict the result shape without finding it.

`np.broadcast_to(a, shape)` &mdash; materialise the stretched view, read-only, for inspection.

`np.einsum` &mdash; when the index bookkeeping has become the hard part.

Between them, those cover each broadcasting situation, and the first two cover most of them.
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
intro: A compare gives an array of True and False - and that array is an index.

## A comparison is elementwise

Boolean masking is one of the most used features in NumPy. It lets you select, count, and modify elements based on a condition, without writing a loop. The idea is simple: a comparison produces a boolean array, and that array selects elements from the original.

The comparison step follows the same elementwise rules as arithmetic. a > 5 compares each element to 5 and returns an array of True and False values with the same shape as a. Two arrays of the same shape can be compared elementwise too. a > b gives True wherever the left element exceeds the right one.

The selection step uses the boolean array as an index. a[a > 5] returns a 1-D array containing only the elements where the condition was True. The result is always 1-D because the True positions may not form a regular grid. That is different from slicing, which preserves the shape.

Combining conditions uses the bitwise operators, not the Python keywords. The and keyword does not work on arrays because Python tries to evaluate the whole array as a single boolean, which is ambiguous. The ampersand operator works elementwise. The same applies to the pipe for or and the tilde for not. Every combined condition needs parentheses around each part because bitwise operators bind tighter than comparisons.

Boolean masks are also useful for counting. True is 1 and False is 0. mask.sum() counts the True entries. mask.mean() gives the fraction. np.any(mask) checks whether at least one element is True. np.all(mask) checks whether every element is True.

Assignment through a mask modifies only the selected elements. a[a < 0] = 0 clips negative values to zero. That is a common pattern for cleaning data in place.

This module covers comparisons, selection, combination, counting, and assignment through boolean masks. These operations appear in virtually every NumPy script and carry over directly to pandas, where boolean Series serve the same role.


`a > 5` doesn't give one answer. It gives a boolean array with one entry per element.

That is the whole idea. The mask has the same shape as the data. It can be used to select from it, to count, or to decide where to write.

It also shows an error people meet early. Putting an array in an `if` raises. Python needs one truth value and NumPy refuses to guess whether you meant `any` or `all`.

## Selecting

`a[mask]` returns the elements where the mask is True, as a 1-D array.

The result is 1-D even when the input isn't. The True spots aren't often rectangular. If you need to keep the shape, `np.where(mask, a, fill)` replaces rather than drops.

## Counting for free

A boolean array is numeric: `True` is 1.

So `mask.sum()` counts matches and `mask.mean()` gives the proportion. That reads oddly for about a day and then turns the obvious way to answer "how many rows meet this" without a loop or a length check.

## Combining conditions

Use `&` for and, `|` for or, `~` for not. And bracket each rule.

The brackets aren't optional. In Python `&` binds more tightly than `>`. `a > 3 & a < 8` parses as `a > (3 & a) < 8` and does a thing unrelated. Writing `(a > 3) & (a < 8)` isn't a style preference. It's what makes the formula mean what it looks like.

`and` and `or` can't be used at all. They call `bool()` on their operands. This Is just the error above. The error message is unusually good. It names `any()` and `all()`. And is worth reading rather than pattern-matching past.

## Assigning through a mask

`a[a < 0] = 0` sets each minus element to zero, in place. The mask picks where to write.

The right-hand side can be a scalar, or an array with as many elements as the mask has True values. Boosted set works too: `b[b % 2 == 0] *= 10`.

This is the vectorised form of a loop with an `if` inside. It's often clearer than the loop and faster.

For the exact case of bounding values, `np.clip(a, low, high)` does both sides in one call and says what it means.

## Masking copies, assigning does not

This trips people who have just learned that slices are views.

`a[mask]` **copies**. It has to: the selected elements aren't evenly spaced. There's no stride pattern that shows them. No view is possible. Writing to the result doesn't affect the first.

`a[mask] = value` **writes in place**. The mask is being used to locate elements in the first array, not to build a new one.

So the same syntax reads as a copy and writes as a view. Both are correct and the gap is worth holding.

## nan does not compare

The one genuine trap in filtering real data.

each compare involving `nan` is False. Including `nan == nan`. So `a[a != np.nan]` keeps all. `a > 0` silently drops the NaNs into the False bucket whether or not you thought about them.

Use `np.isnan` to find them and `~np.isnan(a)` to exclude them. There's a module on missing data later. For now, note that a compare will never find a NaN for you.

## The shape of real filtering

Build the mask in pieces, combine it, then apply it once:

```python
valid = ~np.isnan(temps) & (temps > -50)
clean = temps[valid]
```

Named masks read well, compose, and can be counted and inspected before you commit to them. `valid.sum()` before filtering tells you how much data lives. This Is often worth knowing.

## where, in its three-argument form

`np.where(cond)` returns the spots where the rule is true.

`np.where(cond, a, b)` is a thing else fully: a vectorised gated, choosing elementwise from `a` where the rule holds and `b` where it doesn't.

That second form is the array equal of a ternary formula. It replaces a great many loops. `np.where(x < 0, 0, x)` clamps negatives to zero. `np.where(np.isnan(x), fill, x)` fills missing values.

All three args broadcast, so `a` and `b` can be scalars, or arrays of a matching shape, or one of each.

The one thing to watch: **both branches are checked in full**. `np.where(x != 0, 1/x, 0)` still finds `1/x` for each element, including the zeros. Emits a division warning though those results are discarded. The correct form uses `out=` and `where=` on the division itself, or suppresses the warning on purpose with `errstate`.

For more than two branches, `np.select(rules, choices, default=...)` takes a list of each and applies the first matching rule. This Is cleaner than nesting `where` calls three deep.

## The parenthesis rule

`a > 2 & a < 5` doesn't do what it looks like.

`&` binds tighter than `>` in Python. This parses as `a > (2 & a) < 5`. This Is a bitwise and on the values followed by a chained compare. The result is either an error or, worse, a plausible-looking wrong answer.

each rule in a compound mask needs parentheses: `(a > 2) & (a < 5)`.

There's no way to make this less error-prone within Python's grammar. It's the single most common syntactic mistake in NumPy code. Parenthesise by reflex.

The related error is using `and` instead of `&`. Python's `and` needs a single truth value. An array has many. It raises "the truth value of an array with more than one element is ambiguous". That message always means the same thing.

## Counting

`mask.sum()` counts True values, because booleans promote to ints.

`np.count_nonzero(mask)` does the same thing and is often faster. It doesn't build an int mid. On a large mask the gap is measurable. It's the better habit for that reason alone.

`mask.any()` and `mask.all()` short-circuit conceptually but not . NumPy tests the whole array. For an early exit on a huge array, `np.argmax(mask)` finds the first True in one pass and stops there.

That last trick is worth remembering: `argmax` on a boolean array returns the index of the first True. True is 1 and ties go to the first case. If no element is True it returns 0. This Is the same from a match at spot zero. So check `mask.any()` first.

## Masked arrays

NumPy has a whole submodule, `np.ma`, for arrays that carry a mask of invalid entries alongside the data.

`np.ma.masked_array(data, mask)` makes an array where masked elements are excluded from each step. The mean skips them, the sum skips them. The mask passes through math.

It solves a real problem. Missing data in int arrays. Here NaN can't help &mdash; and it's truly handy in domains like climate and oceanography where it's well set.

It's also comparatively slow, less widely supported by other libraries. Easy to lose track of when a masked array passes through a function that returns a plain one. Most code handles missing values with NaN and the `nan*` functions, or moves to pandas, rather than adopting `np.ma`.

Worth knowing it exists. Worth a deliberate choice before building on it.

## What masking costs

A boolean mask is one byte per element. Masking a million-element array allocates a megabyte for the mask.

`a[mask]` then allocates the result, whose size depends on how many elements matched. Chaining a few masked picks allocates at each step.

Two ways to reduce that when it matters.

**Combine rules before selecting.** `a[(a > 2) & (a < 5)]` allocates one result. `a[a > 2][lambda r: r < 5]` allocates two.

**Use the mask right when you don't need the values.** Counting, summing or blending matched elements can be done without extracting them: `a[mask].mean()` builds an mid array, while `a.sum(where=mask) / np.count_nonzero(mask)` doesn't.

For most work this is irrelevant and the readable form wins. It turns worth focus in a loop over large arrays. This Is just where the mid allocations compound.

## Masks as first-class values

A mask is an array. This Means it can be stored, named, mixed and passed around like any other value.

That is worth using. A filtering rule assembled from a few parts is far more readable as named masks than as one long formula:

```python
is_adult = age >= 18
is_active = status == 1
recent = days_since < 30

selected = data[is_adult & is_active & recent]
```

Each name docs a rule, each can be counted on its own while debugging. The mix reads as the sentence it shows.

`is_adult.sum()` at any point tells you how many passed that one filter. This Is how you find out which rule is unexpectedly excluding all.

## Masks and NaN

checks involving NaN are all False. This Has a exact result for filtering: **NaN values fail each rule**.

`a[a > 0]` silently excludes NaNs. So does `a[a <= 0]`. A value that is neither greater than nor less than zero disappears from both halves of what looks like an exhaustive split.

That is at times the desired action and often a source of quietly lost rows. If NaNs should be handled rather than dropped, they need an clear branch:

```python
positive = a > 0
missing = np.isnan(a)
other = ~positive & ~missing
```

Three groups that really cover all, rather than two that appear to.

## Assignment through a mask, and its limits

`a[a < 0] = 0` modifies in place and is the standard way to clamp.

The value assigned must be a scalar or must match the number of selected elements. `a[mask] = swaps` needs `len(swaps) == mask.sum()`. This Is fine when the swaps were found from the same mask and an error waiting to happen else.

`np.where(mask, new, a)` is the non-mutating equal. Returns a new array rather than modifying the first. It's the safer default in a function that shouldn't modify its arg.

`np.putmask` and `np.copyto` with a `where` arg cover the more specialised in-place cases.

## Where masking fits among the alternatives

`np.clip(a, lo, hi)` replaces the common two-sided clamp and is clearer than two masked sets.

`np.where` handles the two-branch gated without extracting anything.

`np.select` handles a few branches in order.

Masking proper is for when you want the **subset**. The values themselves, in a smaller array. Rather than a transformed version of the whole.

Recognising which of those four you really want drops a surprising amount of code. A great many hand-written mask-and-assign sequences are a `clip` or a `where` written the long way.

And the one rule that applies throughout: parenthesise each rule in a compound mask. `(a > 2) & (a < 5)`, always. The op precedence won't do what you want else. It may not tell you.

## Questions people ask

<strong>What is a boolean mask?</strong> It is an array of True and False values with the same shape as the array you are filtering. Indexing with it keeps the elements where the mask is True.

<strong>Does a mask return a view or a copy?</strong> A copy. Reading with a mask builds a new array, but assigning through a mask, as in a[mask] = 0, writes into the original.

<strong>Why do I get an error combining conditions with and?</strong> Python's and and or need a single truth value, and an array has many. Use & and | instead, and wrap each comparison in parentheses because those operators bind tighter than comparisons.

<strong>Why is the result of a[mask] one-dimensional?</strong> The surviving elements may not form a rectangle, so NumPy flattens them. Use np.where or assign through the mask if you need the shape kept.

<strong>How do I count how many elements pass a test?</strong> Call mask.sum() or np.count_nonzero(mask). True counts as 1, so summing a boolean array counts the matches.

<strong>How do I invert a mask?</strong> Use the tilde operator, ~mask. Do not use the word not, which fails on arrays with more than one element.

## A closing note

Masking is the most-used feature in this track after math. It's also where the syntax is least forgiving.

Two habits cover nearly all of it: parenthesise each rule in a compound formula. Name mid masks rather than building one long chain. The first blocks a precedence bug that doesn't always announce itself. The second makes it possible to count how many rows each rule removed. This Is how you find out that one of them is excluding all.
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
intro: Selecting by a list of spots - reordering, repeating. A result whose shape follows the index.
## Indexing with an array

Fancy indexing selects elements by passing an array of indices instead of a single integer or a slice. The result contains the elements at those positions, in the order the indices specify. That order can be anything. You can repeat indices, reverse them, or pick an arbitrary subset.

The key difference from slicing is that fancy indexing always returns a copy, not a view. A slice shares memory with the original array. An index array does not. That distinction matters when you assign through the result. Assigning through a slice modifies the original. Assigning through a fancy index modifies a copy, and the original is unchanged.

Fancy indexing works in multiple dimensions. For a 2-D array, two index arrays select individual elements. a[[0, 2], [1, 3]] gives the elements at (0,1) and (2,3), not a sub-matrix. Getting a sub-matrix requires np.ix_, which turns the two 1-D arrays into an open mesh that selects all combinations.

The combination of fancy indexing and boolean masking is common. You find the indices where a condition holds with np.where, and then use those indices to select from another array. np.where with a single argument returns a tuple of index arrays, one per dimension. np.where with three arguments acts as a vectorised if-else.

argsort returns indices that sort an array. You can use those indices with fancy indexing to reorder the original and any parallel arrays. That is how you sort a matrix by one column: argsort the column, then index the whole matrix with the result.

One pitfall is repeated indices in assignment. a[[0, 0, 0]] += 1 does not increment a[0] three times. It increments it once because the additions are not accumulated. np.add.at is the correct way to accumulate repeated assignments.

This module covers fancy indexing in one and multiple dimensions, the copy-versus-view distinction, np.ix_ for cross-product selection, np.where for conditional selection, and the pitfalls of repeated indices in assignment.


Give an int array where you'd most times give a number. You get those elements back:

```python
a[[0, 2, 4]]
```

Order is preserved as given. So This is also how you reorder. spots may repeat, so it's also how you tile or expand. Minus indices work as usual.

The result takes the shape of the **index**, not the source. Indexing a 1-D array with a `(2, 2)` index array gives a `(2, 2)` result. That is at times what you want and is worth knowing before it surprises you.

## It copies

Fancy indexing can't return a view. The selected spots are any. A view has to be describable as a start, a shape and a set of strides. Which scattered spots aren't.

So `a[[0, 2, 4]]` is new memory, and writing to it leaves the first alone.

Assigning **through** it's other: `a[[0, 2, 4]] = -1` writes into the first in place. Same as with boolean masks. Reading copies, writing doesn't.

## Repeated positions in an assignment

A sharp edge worth knowing about.

```python
b[[0, 0, 0]] += 1
```

This does **not** add three. It reads the value once, adds one. Writes the result back three times. The answer is one.

That is a result of how boosted set is defined rather than a bug. It catches people building histograms or building up into bins.

`np.add.at(b, [0, 0, 0], 1)` does the building up version. It's slower. It can't use the vectorised path. It's correct. For counting namely, `np.bincount` is faster still.

## Two dimensions

This is the main surprise.

```python
a[[0, 2], [1, 3]]
```

does **not** select rows 0 and 2 crossed with columns 1 and 3. It pairs them elementwise and returns the two elements at `(0, 1)` and `(2, 3)`.

That action is steady &mdash; the index arrays broadcast against each other, then each pair is a coord &mdash; and it isn't what most people expect the first time.

For the rectangle, there are two idioms. `a[np.ix_(rows, cols)]` builds the open mesh for you and is the clearest. Or reshape one index to a column so the two broadcast into a grid: `a[np.array(rows)[:, None], cols]`.

Once you've seen that the second form is just broadcasting applied to indices, the rule stops being a special case.

## The everyday uses

**Reordering rows**: `data[[3, 0, 4]]`.

**Selecting columns**: `data[:, [2, 0]]`.

**Sampling**: `data[rng.choice(len(data), size=n, replace=False)]`.

**Sorting by a key**: `argsort` returns positions, and applying the same positions to several arrays keeps them aligned. That is the main reason `argsort` exists rather than just `sort` &mdash; the permutation is reusable.

## take

`np.take(a, idx)` is fancy indexing as a function. It's often slightly faster on large arrays. It takes a `mode` arg that plain indexing doesn't:

`mode='raise'` is the default and matches `a[idx]`. `mode='clip'` pins out-of-range indices to the ends. `mode='wrap'` wraps them around.

Those modes are handy for boundary handling. A filter that would read past the edge, say. Where the option is padding the array or special-casing the ends.

## Mixing fancy indexing with slices

Mixing the two in one formula is where fancy indexing stops being natural.

`a[[0, 2], 1:3]` works and does what you expect: rows 0 and 2, columns 1 to 2.

But when fancy indices appear on **both sides** of a slice. `a[[0, 2], :, [1, 3]]`. NumPy has to decide where the resulting axis goes. The rule is that the fancy-indexed axis moves to the **front**. The result's shape isn't the one most people predict.

The hands-on advice is to avoid the ambiguous forms. If an formula mixes fancy indices and slices in a way that makes you pause, split it into two steps. Two clear picks cost one extra mid array and save the next reader from working out the rule.

## np.ix_ builds the rectangle

The most common thing people want from `a[[0, 2], [1, 3]]` is the four elements at the intersection of rows 0 and 2 with columns 1 and 3.

What they get is two elements: `a[0,1]` and `a[2,3]`. The index arrays are paired elementwise.

`np.ix_` converts a set of index lists into the shapes that broadcast into a grid:

```python
a[np.ix_([0, 2], [1, 3])]
```

gives the `(2, 2)` rectangle. It works by reshaping the first list to a column and the second to a row. Broadcasting makes each mix. The same trick as `a[:, None]` against `b[None, :]`, packaged for readability.

The option, `a[[0, 2]][:, [1, 3]]`, gives the same answer with two picks and two copies. `np.ix_` is one pick and says what it means.

## put, take and the clip modes

`np.take(a, idx)` is fancy indexing as a function call. It's often a little faster than bracket syntax on 1-D arrays. It accepts an `axis` arg. This Makes `np.take(a, idx, axis=1)` a clean way to select columns without a slice full of colons.

Its handy extra is `mode`. By default an out-of-range index raises, as with normal indexing. `mode="clip"` pins the index to the valid range, and `mode="wrap"` wraps it around.

That turns a whole class of boundary-rule loops into a single call. Sampling neighbours near the edge of an image, say. Here The choice between clamping and wrapping is a param rather than a branch.

`np.put` is the set counterpart, writing values at given flat spots in place.

## The idiom this all exists for

Fancy indexing looks like a set of tricks until you see the one pattern it's really for:

```python
order = np.argsort(key)
table_a = table_a[order]
table_b = table_b[order]
```

Find an index array once, apply it to all that needs to stay aligned. That is sorting a table by a column, taking the top n, shuffling a dataset, applying a train/test split. Reordering to match another array. All the same step.

Once you recognise it, most uses of fancy indexing in real code turn out to be an instance of it, and the rest are lookups.

## Lookups

The second everyday use is treating an array as a lookup table.

`labels[guesses]` converts an array of class indices into an array of names. `palette[image]` converts an index image into colours. `np.unique(..., return_inverse=True)` makes just the index array that this consumes.

The pattern is `values[index_array]`, and the result has the shape of the *index*, not of the values. That is worth stating by name. It's the opposite of the intuition built up from slicing, and it's what makes a `(h, w)` index array plus a `(256, 3)` palette give an `(h, w, 3)` image.

## Choosing between the three ways to select

**Basic slicing** when the pick is a regular range. It's a view, it's free. It's the only one of the three that doesn't allocate.

**Boolean masking** when the pick is a rule. The mask has the shape of the data. It composes with `&` and `|`.

**Fancy indexing** when the pick is a list of spots, or when the order matters. Masks can't reorder or repeat. Fancy indexing can do both.

The share is smaller than it looks. A rule wants a mask. A permutation wants an index array. A contiguous window wants a slice. When two of them would work, the one that expresses the intent right is the right choice. It's often also the faster one.

## Repeated indices in assignment

Selecting with repeated indices returns repeated values, which is unsurprising.

Assigning with repeated indices is where it gets notable. `a[[0, 0, 1]] = [10, 20, 30]` leaves element 0 holding 20. The last write wins. The earlier one is simply overwritten.

The version that catches people is the boosted form:

```python
a[[0, 0, 1]] += 1
```

Element 0 is incremented **once**, not twice. The formula expands to a fetch, an add and a store. The fetch makes a copy holding element 0 twice, both copies get incremented. Both are written back to the same location.

`np.add.at(a, [0, 0, 1], 1)` is the unbuffered version that does what the syntax suggests. each ufunc has an `.at` method for this.

This matters in any build-up where indices repeat. Building a histogram, scattering values into bins, building up grads. The buffered version makes a plausible undercount rather than an error. This Is the worst kind of wrong.

For the exact case of counting or summing by int key, `np.bincount(idx)` and `np.bincount(idx, weights=vals)` are both correct and a lot faster than `add.at`.

## Negative indices work

Fancy indexing accepts minus spots, counting from the end just as normal indexing does. `a[[-1, -2]]` takes the last two elements in reverse order.

That is convenient and at times a hazard. An index array found by subtraction that accidentally goes minus selects from the far end of the array instead of raising. A `-1` made by "not found" logic silently returns the last element.

If out-of-range should be an error rather than a wrap, check the index array before using it, or use `np.take` with the default `mode="raise"`. This Validates but treats negatives the same way.

## The cost

Fancy indexing always allocates. The result is a new array of the index's shape. The values are gathered one by one from scattered spots.

That gathering isn't free even beyond the allocation. Scattered reads defeat the processor's cache in the way covered in the speed module. Fancy indexing a large array with a random permutation is usefully slower per element than reading it in order.

The hands-on result is small. It's still far faster than a Python loop &mdash; but it means fancy indexing inside a tight loop over a large array is worth a second look. Sorting the index array first. Here Order doesn't matter, can help by making the reads more sequential.

## Questions people ask

<strong>What is fancy indexing?</strong> Indexing with an array or list of integers instead of a slice. a[[0, 3, 5]] picks those three positions in the order you gave.

<strong>Does fancy indexing return a view?</strong> No, it always returns a copy. Slices give views and fancy indexing does not, which matters when you assign to the result.

<strong>How do two index arrays combine?</strong> They pair up element by element. a[[0, 1], [2, 3]] returns a[0, 2] and a[1, 3], not a 2 by 2 block. Use np.ix_ if you want the block.

<strong>What happens when an index repeats in an assignment?</strong> The last write wins for plain assignment. For counting use np.add.at, which applies every repeated index instead of just one.

<strong>Can I mix a slice and an index array?</strong> Yes, and the slice axis keeps its position. a[:, [0, 2]] gives all rows and columns 0 and 2.

<strong>Are negative indices allowed in the index array?</strong> Yes, they count from the end like normal indexing. Out-of-range values raise an IndexError.

## The three selections, compared

| | Basic slicing | Boolean mask | Fancy indexing |
| --- | --- | --- | --- |
| Result | view | copy | copy |
| Selects by | position range | condition | explicit positions |
| Can reorder | only reversal | no | yes |
| Can repeat | no | no | yes |
| Result shape | derived from slice | 1-D, length = matches | shape of the index |

The last row is the one that surprises people most. A boolean mask always flattens to a 1-D result. But Many dims it covered. Fancy indexing takes the shape of the index array. A `(h, w)` index array against a `(256, 3)` palette makes `(h, w, 3)`.

Choosing right is mostly a matter of matching the tool to the question. A range wants a slice, a rule wants a mask, a list of spots wants fancy indexing. Where two would work, the one that states the intent is often also the faster one.
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
intro: sum, mean and max - and the one arg that decides what they mean.

## The default collapses everything

Aggregation functions reduce an array to a smaller result. sum adds all elements. mean computes the average. min and max find the extremes. By default, each of these operates on the entire array and returns a single number, regardless of the array's shape.

That default is often not what you want. A 2-D array of sales by city and month needs a sum per city, not one grand total. The axis parameter tells the aggregation which dimension to collapse. axis=0 collapses rows, giving one result per column. axis=1 collapses columns, giving one result per row.

The axis convention trips people up because collapsing along axis 0 gives a result with as many entries as there are columns, not as many as there are rows. The way to remember it is that the axis number is the dimension that disappears. axis=0 removes the row dimension. The columns survive.

keepdims preserves the collapsed dimension as a size-one axis instead of removing it. That is useful when you want to broadcast the result back against the original array. A column mean with keepdims=True has shape (1, n) and can be subtracted from the original (m, n) array directly. Without keepdims, the result has shape (n,), and the broadcast rules treat it as a row, not a column.

NumPy provides both function and method forms for most aggregations. np.sum(a) and a.sum() do the same thing. The method form is shorter. The function form accepts array-like inputs that are not yet arrays. Use whichever reads better in context.

Some aggregations have nan-aware variants. np.nansum ignores NaN values instead of propagating them to the result. np.nanmean does the same for the mean. The regular versions return NaN if any element is NaN, which is correct but often not what you want when the NaN represents missing data.

This module covers the common aggregation functions, the axis parameter, keepdims, and the nan-aware variants. The examples use 2-D arrays so that the axis behaviour is visible. Understanding axis here carries over directly to pandas, where the same parameter does the same thing.


`a.sum()` with no args adds each element, what the shape, and returns a single value.

That value is a NumPy scalar rather than a Python `int` or `float`. It behaves like one almost all over. Wrap it in `int()` or `float()` when you need a genuine Python number, for JSON or for a format string that cares.

## axis names what disappears

This is the rule, and it's the opposite of how most people read it at first.

`axis=0` does **not** mean "along the rows" in the sense of giving one answer per row. It means *collapse axis 0*. Axis 0 is the row axis. The rows vanish and you're left with one value per column.

`axis=1` merges the columns and leaves one value per row.

Reading it as "which axis am I dropping?" makes each case predictable, including higher dims where intuition runs out. The shape rule is simple. The result has the input shape with that axis deleted.

A handy check when unsure: print `a.shape` and `a.sum(axis=k).shape` and confirm the missing entry is the one you meant.

## keepdims

Reductions drop the axis, and that is often what you want. Until you try to use the result against the first array.

Row means of a `(3, 4)` array give shape `(3,)`. Subtracting that from the `(3, 4)` array fails. Broadcasting aligns from the right and checks 4 with 3.

`keepdims=True` gives `(3, 1)` instead. This Broadcasts down the rows right.

Note the skew: centring by **column** needs no `keepdims`. `mean(axis=0)` gives `(4,)` which already aligns with the last axis. Centring by **row** needs it. That skew is a direct result of right-aligned broadcasting, and it's why `keepdims` exists.

A square array hides the error. Both alignments are legal. So this is worth getting right on principle rather than by testing.

## Several axes at once

`axis` takes a tuple. On a `(frames, rows, cols)` stack, `axis=(1, 2)` reduces each frame to one number. `axis=0` means across frames to give one image.

That covers most of what people reach for loops to do with image or batch data.

## argmin and argmax

These return **spots** rather than values.

On a 1-D array the spot is an index. On a multi-dimensional array with no `axis`, the spot is into the *flattened* array. This Is rarely right handy. `np.unravel_index(a.argmax(), a.shape)` converts it into coords.

With an `axis`, you get one spot per left slice. This Is often what you want: `a.argmax(axis=1)` gives the column of the largest value in each row.

Ties resolve to the **first** case. That matters when the max isn't unique and a thing downstream assumes it's.

## Cumulative operations

`cumsum` and `cumprod` aren't reductions: they keep the shape and fill in running totals. Without an axis they operate on the flattened array. This Is at times what you want and often not. Pass `axis` on purpose.

`np.diff` is the inverse of `cumsum`. In a row differences, one element shorter.

## Boolean reductions

`any` and `all` take `axis` just like `sum`. A boolean array is numeric and these are just reductions over it.

`mask.any(axis=0)` answers "does any row meet this, per column". `mask.sum(axis=1)` counts matches per row. Between them and `argmax`, most "find the first row where..." questions have a one-line answer.

## The common mistakes

**Reading `axis=0` as "per row".** It gives per column. The axis named is the one removed.

**Losing `keepdims` when centring by row.** It raises on a rectangular array and silently misbehaves on a square one.

**Using a flat `argmax` as if it were coords.** Unravel it.

**Reducing without an axis by accident.** `a.mean()` on a 2-D array gives one number. If you wanted per-column means, the missing arg is the whole bug and the result still looks like a plausible number.

## The accumulator dtype

`a.sum()` on an int array builds up in that array's int type, and that type can overflow.

Summing a million `int32` values each around ten thousand overflows silently and gives a minus answer. The array is fine. The accumulator isn't.

`a.sum(dtype=np.int64)` fixes it by building up in a wider type than the data. The same arg works on `mean`, `prod` and the rest.

NumPy already does something like this by default for the narrowest types. Summing `int8` builds up in the platform int. But it doesn't promote `int32` or `int64`. The risk is real for just the widths people really use.

For floats the concern is other: not overflow but precision loss. Summing many `float32` values builds up rounding error. `a.sum(dtype=np.float64)` reads the narrow array and builds up in the wide type. This Is the standard compromise between memory and score.

NumPy uses pairwise summation inside rather than a naive running total. The error grows far more slowly than a hand-written loop would. It's still worth being deliberate when summing millions of `float32` values.

## Weighted means and percentiles

`np.mean` isn't a synonym for `np.mean`. It takes a `weights` arg, which `mean` doesn't.

`np.mean(x, weights=w)` finds the weighted mean. `returned=True` also gives back the sum of the weights. This Is what you need to combine means from a few groups right.

`np.median` is the 50th percentile, and `np.percentile(a, q)` generalises it. Both accept an `axis`. Per-column medians are one call.

Percentiles involve blending between the two nearest ranks when the requested quantile doesn't fall on an element. The `method` arg selects among a few rules. Other statistical packages default differently. Which is the usual reason when NumPy's answer disagrees slightly with another tool's.

`np.quantile` is the same function taking fractions rather than percentages.

All of these have `nan`-aware variants: `nanmedian`, `nanpercentile`, `nanquantile`.

## reduce and accumulate as the general form

each reduction has a ufunc underneath, and the ufunc's `reduce` method is the general case.

`np.add.reduce(a, axis=0)` is `a.sum(axis=0)`. `np.max.reduce` is `a.max()`. `np.logical_and.reduce` is `a.all()`.

This matters when you want a reduction NumPy doesn't name. A running max has no `cummax` function. `np.max.build up(a)` is just that. Is the standard way to find a drawdown baseline or a high-water mark.

`np.ufunc.reduceat` performs segmented reductions &mdash; a reduction over slices defined by a list of start indices &mdash; which is the closest thing NumPy has to a group-by on sorted data.

## Reductions that return more than a number

`np.ptp` gives the peak-to-peak range, `max - min`, in one pass.

`np.histogram` reduces to counts per bin and returns the bin edges alongside them.

`np.bincount` counts cases of small non-minus ints. Is much faster than `unique(return_counts=True)` for that case because it indexes right rather than sorting. Its `weights` arg turns it into a group-sum: `np.bincount(group_ids, weights=values)` sums values per group in one call. This Is the fastest group-by NumPy offers.

## Empty arrays and the identity element

`np.sum([])` is `0.0`. `np.prod([])` is `1.0`. Both return the identity element for the step. This Is in math the right answer.

`np.max([])` raises, because there's no identity for a max.

`np.mean([])` returns `nan` with a warning, since it cuts by zero.

This matters in code that reduces over groups where some group might be empty. A sum silently gives zero. This May or may not be the meaning you want. A max raises. This At least tells you. Filtering out empty groups before reducing, or using the `initial` arg that `max` and `min` accept, makes the intent clear.

## The habits worth forming

Pass `axis` by name. The default of "reduce all" is right often enough to hide a missing arg. Wrong often enough to matter.

Pass `keepdims=True` when the result will be used against the first array.

Pass `dtype` when summing ints that could be large, or many `float32` values.

Check the shape of the result rather than given it. One printed `.shape` resolves most confusion about which axis went where. It's faster than thinking about it.

## Reductions on boolean arrays

Because booleans promote to ints, each numeric reduction works on a mask and means a thing handy.

`mask.sum()` counts. `mask.mean()` gives the proportion. The fraction of elements meeting the rule. This Is often just the summary you want and avoids a division you'd else write by hand.

`mask.any()` and `mask.all()` are the logical reductions, and take `axis` like all else.

`mask.argmax()` finds the first True, since True is 1 and ties go to the first case. It returns 0 when nothing is True. This Is the same from a match at spot zero &mdash; check `mask.any()` first.

Mixing these covers most "how many rows meet" and "which is the first row where" questions in one line each.

## Reductions with a condition

Modern ufunc reductions accept `where`. This Restricts the reduction to selected elements without building an mid array.

`a.sum(where=mask)` sums only the matching elements. `a.mean(where=mask)` means them. Checked with `a[mask].sum()`, it avoids allocating the extracted subset. This Matters on large arrays inside a loop.

`initial` supplies a starting value. This Is what makes `max` work on a possibly-empty pick: `a.max(initial=0, where=mask)` returns 0 rather than raising when nothing matches.

Those two args together cover the awkward cases in group-wise reductions. Here Some groups may be empty and the plain functions either raise or return an identity that means a thing other.

## Reductions across a stack of arrays

A frequent question is how to reduce over a list of arrays rather than over the axes of one.

The answer is to stack them and reduce along the new axis:

```python
result = np.stack(arrays).mean(axis=0)
```

That is the elementwise mean across all of them. `max(axis=0)` gives the elementwise max, and so on.

For two arrays there are direct functions. `np.max(a, b)` and `np.min(a, b)` are elementwise and broadcast. And they're worth distinguishing from `np.max`. This Reduces a single array. The names differ by one letter and the steps are fully other. This Is a recurring source of confusion.

`np.max.reduce(arrays)` generalises the pairwise version to any number, without the mid stack.

## The summary

Pass `axis` by name, and read it as "the axis that disappears".

Pass `keepdims=True` when the result will be used against the first.

Pass `dtype` when summing many ints or many `float32` values.

Use the `nan*` variants when missing values are possible. Know that they make a choice on your behalf about what missing means.

Use `where` and `initial` for gated reductions rather than extracting a subset first.

And when the result shape isn't what you expected, print `a.shape` and the result's shape together. One compare resolves nearly each axis confusion faster than thinking about it does.

## Questions people ask

<strong>Which axis do I pass to get column sums?</strong> Pass axis=0. The axis you name is the one that disappears, so axis=0 collapses the rows and leaves one number per column.

<strong>Why does my result have the wrong shape after a sum?</strong> The summed axis is removed from the shape. Pass keepdims=True if you want a length-1 axis left in place so the result still broadcasts against the original.

<strong>What does axis=None do?</strong> It reduces over every element and returns a single scalar. That is the default for sum, mean, max and the other reductions.

<strong>How do I get the index of the maximum instead of the value?</strong> Use argmax, which takes the same axis argument. Without an axis it indexes into the flattened array, so use np.unravel_index to turn it back into coordinates.

<strong>Why does np.mean of an array with a NaN return NaN?</strong> NaN propagates through arithmetic, so one NaN poisons the whole reduction. Use nanmean, nansum and friends if you want the missing values skipped.

<strong>Does sum work over several axes at once?</strong> Yes. Pass a tuple such as axis=(0, 1) and both axes are collapsed in one pass.

## A closing note

Reductions are simple until an axis is involved. Then almost each confusion comes from one place. Reading `axis=0` as "along the rows" rather than "collapse the rows".

The axis named is the axis removed. Holding onto that phrasing makes the result shape predictable in any number of dims. Turns `keepdims`, tuple axes and higher-dimensional reductions from special cases into results of the same rule.
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
intro: Which steps give you a second window onto the same numbers, and why it matters.

## One buffer, several descriptions

Understanding views and copies is the single most important thing for writing correct NumPy code. A view shares memory with the original array. A copy has its own memory. The difference is invisible when you only read. It shows up the moment you write.

Every slice creates a view. That means modifying a slice modifies the original array. This is a performance feature. Copying a gigabyte array every time you take a slice would be wasteful. But it is also a correctness hazard. If you pass a slice to a function and that function writes to it, the original array changes. Nothing warns you.

An array is a block of contiguous memory plus a description. The description records the starting address, the shape, the dtype, and the strides. Strides say how many bytes to step for each axis. A view is a new description of the same block. Making a view changes the strides and the shape but not the data. That is why views are free to create. No data is copied.

Transpose is a view. Reshape is a view when the result is contiguous. Fancy indexing is a copy. Boolean indexing is a copy. np.array always creates a copy. np.asarray creates a view when the input is already an array with the right dtype.

The distinction matters for three reasons. First, correctness. Writing through a view changes the original. Writing through a copy does not. Second, memory. Views use no extra memory. Copies double it. Third, performance. Creating a view is instant. Creating a copy takes time proportional to the array size.

np.shares_memory tells you whether two arrays share the same underlying buffer. It is the definitive check. When you are unsure, call it. When debugging an unexpected mutation, call it on every array that might be a view of the one that changed.

This module covers how views are created, how copies are created, how to tell the difference, and how to force a copy when you need one. The examples show mutations propagating through views and stopping at copies.


An array is a block of memory plus a description. Where it starts, what shape it has. How many bytes to step for each axis. Those steps are the **strides**.

A **view** is a new description of the same block. Making one is free. Writing through it changes what every other description of that block sees.

A **copy** is a new block. It costs time and memory, and it's split.

Nearly each surprise in NumPy that isn't about broadcasting is about this gap.

## Where the line falls

**Views**: basic slicing, `reshape` (usually), `.T` and other transposes, `ravel` (usually), `np.newaxis`, and `view()`.

**Copies**: boolean masking, fancy indexing, `flatten`, `copy`, `astype`, and most functions that return a new array.

The rule underneath is rote. If the selected elements can be given by a start and a regular stride per axis, a view works. A slice steps evenly. It can. A boolean mask picks scattered spots with no single step size, so it can't.

That is why the list isn't any and doesn't need storing once you've the reason.

Two entries carry an "often". `reshape` returns a view when the result can be strided over the existing layout. Copies when it can't. Often after a transpose. `ravel` is the same. Neither tells you which happened. This Is why the check below matters.

## Checking

`np.shares_memory(a, b)` is the honest answer, and the one to use.

`b.base` points at the array a view derives from, or `None` for a copy. It's helpful but can be a chain. A view of a view has a base that is itself a view. So it isn't a solid equality test.

`b.flags["OWNDATA"]` says whether the array owns its buffer.

`np.may_share_memory` is a cheap conservative check: it can say True when it's merely unsure. That makes it right for a fast guard in library code and wrong for a definite answer.

## The bug

The hands-on result is a function that modifies its caller's data without saying so.

```python
def normalise(data):
    body = data[1:]
    body -= body.min()     # in place, on a view of the caller's array
    return data
```

`data[1:]` is a view. `-=` writes in place. The caller's array is now other. Nothing in the signature suggested it would be.

This is easy to write by accident. Each step looks innocent. Hard to spot in review. Two defences:

**Copy at the boundary** when a function shouldn't modify its input. `data = data.copy()` at the top is cheap insurance for small arrays and a deliberate choice for large ones.

**Say so in the name** when a function does modify in place. NumPy's own rule is that in-place variants are clear. `np.sort` returns a sorted copy, `a.sort()` sorts in place.

## Memory: a view keeps its base alive

A view holds a link to the array it came from. The whole buffer stays in memory if any view of it exists.

Slice one row out of an 8 MB array and keep it: you're keeping 8 MB, not 4 KB.

That matters when you're extracting a small piece of a thing large to hold on to. A filtered subset, a header, one channel. `copy()` releases the rest. It's just the same shape of problem as holding a slice of a huge Python string. It shows up in long-running processes as memory that never comes back.

## When to copy deliberately

**Crossing an API boundary** where the caller shouldn't see your changes, or you shouldn't see theirs.

**Keeping a thing small from a thing large**. So The large thing can be freed.

**Before an in-place loop** over data you didn't create.

**When you want a promise** rather than the "often a view" action of `reshape` and `ravel`.

all over else, views are the point. They're why slicing a gigabyte array costs nothing and why NumPy code can pass windows around freely. The goal isn't to avoid them but to know which one you're holding.

## The two "usually" cases

Two steps in the view column carry a qualifier. Both are worth understanding rather than storing.

`reshape` returns a view when the new shape can be walked with a regular stride over the existing memory. On a freshly created contiguous array, that is always. After a transpose, it often isn't. The buffer is being read column-first. Flattening it row-first needs gathering scattered values.

`ravel` is the same. `flatten` is the version that always copies. Its existence is really just a way of asking for the promise.

If you need the opposite promise. A view or an error, never a silent copy. Assign to `.shape` right. `a.shape = (3, 4)` raises if a view is hopeless. This Turns an invisible speed problem into a visible failure.

## copy is shallow, in the way that matters

`a.copy()` copies the buffer, and for a numeric array that is a full, split copy.

For an **object** array it isn't. The new array has its own array of pointers. Those pointers lead to the same Python objects. Modifying one of those objects is visible through both arrays.

`copy.deepcopy(a)` from the standard library copies the objects too.

This only arises with `dtype=object`. This Is uncommon and often worth avoiding. The failure is confusing when it happens because `copy()` did just what its name suggests at the level it operates on.

## In-place operations on a fancy index

There's a subtle failure that is worth knowing before it costs you an afternoon.

```python
a[[0, 0, 1]] += 1
```

You might expect element 0 to be incremented twice. It's incremented **once**.

this expands to a fetch, an add. A store: `a[idx] = a[idx] + 1`. The fetch makes a copy holding element 0 twice, both copies get 1 added. Then both are written back to the same place. The second overwriting the first.

`np.add.at(a, [0, 0, 1], 1)` is the unbuffered version that does what the syntax suggests, incrementing element 0 twice. each ufunc has an `.at` method for this.

This matters in any histogram-like build-up where indices repeat. The wrong version makes plausible undercounts rather than an error.

## Tracking down a mutation bug

The symptom is always the same: an array changed and nothing in the visible code changed it.

The diagnosis is rote.

**Find each place the array was derived from a thing else.** A slice, a reshape, a transpose, a `ravel`. Each is a pick.

**Check with `np.shares_memory`.** Between the array that changed and each pick source. This is definitive.

**Look for in-place ops on the shared side.** `+=`, `-=`, `*=`, `sort()`, `fill()`. Set into a slice. Anything that modifies rather than rebinding.

**Check function boundaries.** A function that takes an array and slices it's the most common origin. The mutation is one level away from where you're looking.

The fix is nearly always a `copy()` at the boundary. The question of *which* boundary is answered by deciding who owns the data.

## An ownership convention

Most of these problems disappear under a simple rule, applied always:

**A function doesn't modify its args unless its name says so.**

NumPy follows this itself. `np.sort` returns a sorted copy. `a.sort()` sorts in place. `np.append` returns a new array. The function forms are safe, the method forms aren't. The gap is solid enough to lean on.

For your own code, that means copying at the top of any function that will modify what it was given. Or, better, not modifying it at all and returning a new array.

The exception is a deliberate in-place API for large data. Here Copying would defeat the purpose. Those functions should say so in the name, take the output array by name, or both. `out=` is NumPy's own answer to this. It's a good pattern to copy. The caller supplies the destination. No one is surprised about what gets written.

## When views are the point

None of this is an arg against views. They're the reason NumPy can pass windows of large arrays around for free. The reason slicing a gigabyte array costs nothing.

The goal isn't to copy defensively all over. That would discard the main gain. But to know which one you're holding at the moments it matters. Across a function boundary, before an in-place loop. When keeping a thing small from a thing large.

## A quick reference

**Always a view**: basic slicing, `a[::k]`, `a[::-1]`, `.T`, `transpose`, `swapaxes`, `moveaxis`, `a[None]`, `expand_dims`, `squeeze`, `view()`.

**Usually a view**: `reshape`, `ravel`. Both fall back to copying when the requested layout cannot be strided over the existing memory &mdash; typically after a transpose.

**Always a copy**: boolean masking, fancy indexing, `flatten`, `copy`, `astype`, `np.array(x)` by default, and nearly every function returning a computed result.

**Neither**: in-place operations, which return nothing and modify the buffer.

The underlying rule makes the list predictable: if the pick can be given by a start, a shape and a stride per axis, it's a view. If the spots are scattered, it can't be, so it copies.

## Why `astype` always copies

Even `a.astype(np.float64)` on an array that is already `float64` returns a copy by default. That surprises people who expect it to be a no-op.

`astype(dtype, copy=False)` returns the first when no conversion is needed. That is the form to use in a function that norms its input. Here Copying each call is waste.

The default of copying is defensive: `astype` is often called to give a thing the caller will modify. Returning a shared array would make that dangerous.

## Checking, once more

`np.shares_memory(a, b)` &mdash; definitive, and the one to use.

`np.may_share_memory(a, b)` &mdash; conservative and cheap. Can say True when unsure. Right for a guard, wrong for an answer.

`a.base` &mdash; the array a view derives from, or None. Helpful. But A view of a view has a base that is itself a view. It isn't an equality test.

`a.flags["OWNDATA"]` &mdash; whether the array owns its buffer.

`a.flags` in full also reports contiguity. This Is what finds whether the next `reshape` or `ravel` will copy.

## Questions people ask

<strong>How can I tell whether two arrays share memory?</strong> Use np.shares_memory(a, b), or check b.base is a. A view keeps a reference to the array that owns the data.

<strong>Which operations return views?</strong> Slices, reshape when possible, transpose, ravel when possible, and view. Basic indexing gives views.

<strong>Which operations return copies?</strong> Fancy indexing, boolean masking, flatten, astype and explicit .copy(). Arithmetic always produces a new array.

<strong>Why did changing b change a?</strong> b was a view of a, probably from a slice. Call .copy() when you create b if you want independent data.

<strong>Is a copy always safe?</strong> It is safe but costs memory and time. On big arrays, a stray copy in a loop is a common slow-down.

<strong>What is the pitfall with chained indexing and assignment?</strong> a[mask][0] = 1 assigns into a temporary copy and is lost. Combine the index into one expression such as a[mask] = 1.

## The habits that prevent the bugs

**Copy at the boundary** of any function that will modify what it was given, unless the name says else.

**Follow NumPy's own convention**: functions return new arrays, methods modify in place. `np.sort` versus `a.sort()`. Making your own code follow the same rule means callers can predict it without reading the body.

**Copy on purpose when keeping a thing small from a thing large**. The base can be freed.

**Check with `shares_memory`** when a mutation appears from nowhere. It's the fastest route from symptom to cause. It gives a definite answer where thinking about which steps copy gives a probable one.

None of this argues against views. They're why slicing a gigabyte array is free and why array code can pass windows around without thought. The goal is to know which one you're holding at the three moments it matters. Across a function boundary, before modifying in place. When keeping a fragment of a thing large.
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
intro: Joining along an existing axis or a new one. Why those are other functions.

## Two different questions

Combining arrays is something you do constantly. The data arrives in pieces, and at some point you need a single array that holds all of it. NumPy gives you two families of functions for this, and choosing the wrong one gives you an array with the wrong number of dimensions.

Concatenate joins arrays along an existing axis. Two (3, 4) arrays concatenated on axis 0 give (6, 4). The axis already existed. It just got longer. That is the operation you want when stacking more rows onto a matrix or appending more time steps to a signal.

Stack joins arrays along a new axis. Two (3, 4) arrays stacked give (2, 3, 4). A new axis of length 2 was added at the front. That is the operation you want when collecting separate images into a batch or collecting separate feature vectors into a matrix.

The difference is exactly one dimension. After concatenate, ndim stays the same. After stack, ndim goes up by one. If your result has an unexpected extra dimension, you probably used stack when you meant concatenate, or vice versa.

hstack and vstack are convenience wrappers. vstack is concatenate along axis 0. hstack is concatenate along axis 1. They exist because the axis parameter can be confusing, and "vertical" and "horizontal" are easier to picture. column_stack handles the common case of turning 1-D arrays into columns of a 2-D array.

Splitting is the reverse of stacking. np.split divides an array into equal pieces along an axis. np.array_split handles unequal pieces. hsplit and vsplit are the convenience wrappers. These are less commonly used, but they appear when you need to process chunks of data separately.

This module covers concatenate, stack, hstack, vstack, column_stack, split, and the common patterns for combining and dividing arrays. The examples show the shape of the result in each case, because the shape is the thing you need to verify.


You've a few arrays and want one. There are two distinct things that could mean. NumPy gives them split functions rather than guessing.

**`concatenate`** joins along an axis that already exists. Two `(2, 3)` arrays concatenated on axis 0 give `(4, 3)`. More rows, same number of dims.

**`stack`** creates a new axis. The same two arrays stacked give `(2, 2, 3)`. A pile of two frames, one dim more than the inputs.

Asking which you want is the first step. The answer is often obvious once phrased that way. Appending records is joining. Collecting frames or samples into a batch is stacking.

## What must match

`concatenate` needs each axis **except the joining one** to agree. Joining on axis 0 needs matching column counts. Joining on axis 1 needs matching row counts.

`stack` is stricter: all inputs must have just the same shape. They're turning parallel slices of a new axis.

The error messages name the mismatch. Reading them rather than guessing often locates the problem at once.

## The convenience functions

`vstack` stacks vertically, `hstack` flatly, `dstack` along the third axis. For 2-D input they're just `concatenate` with a fixed axis.

For **1-D input they diverge**, and this is where they cause trouble.

`np.vstack([a, b])` on two length-3 arrays gives `(2, 3)`. It promotes each to a row.

`np.hstack([a, b])` gives `(6,)` &mdash; it joins them end to end. Axis 1 doesn't exist so it falls back to axis 0.

People reaching for `hstack` to make two columns get one long array instead. `column_stack` is the function that does what they meant. It turns 1-D arrays into columns of a 2-D result.

The general advice: use `concatenate` or `stack` with an clear `axis` when the dimensionality might vary. The convenience names are fine when you know just what shapes you've.

## Splitting

`np.split(a, n, axis=0)` cuts into `n` equal parts and **raises** if the length doesn't divide just. That strictness is handy. An uneven split is often a sign that a thing upstream isn't the size you assumed.

`np.array_split` allows uneven parts, distributing the remainder across the first few. Use it when uneven is truly acceptable, such as chunking work for parallel handling.

`split` also accepts a list of spots rather than a count: `np.split(a, [3, 7])` cuts before index 3 and before index 7, giving three pieces. That is often more natural than finding a count.

The pieces are **views**, not copies. This Is worth knowing. Splitting a large array is free. Writing into a piece writes into the first.

## Do not build in a loop

The same rule as `np.append`, for the same reason.

Concatenating inside a loop allocates a new array and copies all built up so far, on each loop. That is quadratic. The last editor measures the gap.

Collect into a Python **list** and call `stack` or `concatenate` once at the end. Lists append cheaply. Arrays don't append at all.

If you know the final size in advance, better still. Allocate with `np.empty` and assign into slices. That avoids even the single large copy.

## Choosing

Appending records of the same width: `concatenate(axis=0)`.

Adding columns to a table: `concatenate(axis=1)`, or `column_stack` for 1-D inputs.

Collecting frames, samples or channels into a batch: `stack`, with an clear axis.

Undoing any of those: `split` when the division is exact, `array_split` when it isn't.

And in each case, if the joining is happening inside a loop, the answer is to move it outside.

## r_ and c_

`np.r_` and `np.c_` are index-formula shortcuts. They look strange because they use square brackets rather than parentheses.

`np.r_[a, b]` concatenates along the first axis. `np.c_[a, b]` stacks as columns, equal to `column_stack`.

They also accept slice syntax. So `np.r_[0:5, 10, 20:23]` builds an array from a mix of ranges and literals in one formula. That is truly convenient for making index arrays and test data.

They're compact rather than clear, and they show up more in older code and in interactive sessions than in libraries. Worth recognising. Not worth preferring over the named functions in code others will read.

## tile and repeat

Both make an array bigger by duplication. They differ in a way that is easy to state and easy to forget.

`np.tile(a, n)` repeats the whole array n times: `[1, 2]` turns `[1, 2, 1, 2]`.

`np.repeat(a, n)` repeats each element n times: `[1, 2]` turns `[1, 1, 2, 2]`.

`tile` accepts a tuple to repeat along a few axes. This Is how you build a checkerboard or replicate a small pattern across a grid.

`repeat` accepts an `axis` and a per-element count. `np.repeat(rows, counts, axis=0)` expands a table per to a count column. The standard way to turn aggregated data back into one row per finding.

Neither is a substitute for broadcasting. If you're tiling an array purely so that its shape matches another one for an math step, broadcasting will do it without allocating anything. The tile is wasted memory.

## Padding

`np.pad(a, width, mode)` adds elements around the edges.

`width` can be a single number, a pair for before and after, or a pair per axis. The nesting gets confusing quickly. It's worth checking the result's shape the first time on any new call.

The `mode` arg covers the cases that would else be fiddly: `"constant"` with a `constant_values` arg, `"edge"` to repeat the border, `"reflect"` and `"even"` to mirror, and `"wrap"` to tile.

This is how you run boundary rules for a conv or a stencil without writing an index-clamping branch. It's one of the functions that quietly drops a lot of code.

## block, for nested assembly

`np.block` builds an array from a nested list of arrays, laid out the way the nesting reads.

```python
np.block([[A, B],
          [C, D]])
```

makes the block mat, given the pieces have matching shapes. It's far clearer than the equal chain of `hstack` inside `vstack`. It's the right tool for assembling a mat from named submatrices. A co-var built from blocks, a system of equations assembled from parts.

## Choosing among the joins

The functions share enough to be worth a summary.

**`concatenate`** &mdash; the general form. clear axis, works on any dimensionality, no surprises. Reach for this when the dimensionality might vary or when clarity matters.

**`stack`** &mdash; when a new axis is what you want. Collecting frames, samples or repeated runs into a batch.

**`vstack` / `hstack` / `dstack`**. Conveniences with a fixed axis. Safe on 2-D. Divergent on 1-D in a way that catches people. Fine when you know the shapes just.

**`column_stack`** &mdash; turns 1-D arrays into columns. This Is what people often want from `hstack` and don't get.

**`block`** &mdash; nested assembly from named pieces.

**`r_` / `c_`** &mdash; terse, for interactive use.

And the rule that applies to all of them: none belongs inside a loop. Collect into a list, join once.

## Splitting, in practice

The pieces returned by `split` are **views**. Splitting a large array is free and writing into a piece writes into the first. That is often convenient and at times surprising. It follows the same rules as any other slice.

`array_split` distributes an uneven remainder across the first pieces. Splitting 10 into 3 gives lengths 4, 3, 3. That is fixed. This Matters if two processes split the same data on its own and must agree.

For chunking work rather than cutting it evenly, finding the boundaries yourself and passing them as a list is often clearer than asking for a count. `np.split(a, range(0, len(a), chunk))` cuts at fixed intervals even so of whether the total cuts evenly.

## Joining arrays of different dtypes

Concatenating an int array with a float array gives a float result, following the same promotion rules as math.

That is often what you want. At times not. Joining an `int64` array of identifiers with a `float64` array of readings makes a float array in which large identifiers may no longer be just representable.

`dtype=` on `concatenate` forces the result type by name. `casting="no"` makes a mismatch an error rather than a silent promotion. In code where the dtype matters, being clear costs one arg and drops a whole group of surprise.

Joining a fixed-width string array with a longer one widens to fit. This Is the one place NumPy strings do the accommodating thing rather than truncating.

## Building an output array up front

When the final size is known, neither joining nor appending is needed.

```python
out = np.empty((n_rows, n_cols))
for i, row in enumerate(source):
    out[i] = compute(row)
```

One allocation, no copying, and the slices being assigned into are views. This is the fastest form when a loop is unavoidable, and it's clearer than building up pieces to join later.

`np.empty` is right here because each element is written. If some rows might be skipped, `np.zeros` or `np.full(shape, np.nan)` makes the unfilled entries visible rather than leaving what was in memory.

Preallocating also forces you to state the output shape. This Often surfaces an error in the thinking before any code runs.

## Splitting for parallel work

`np.array_split(a, n)` is the natural way to divide data among n workers. It handles the case where the length doesn't divide evenly, distributing the remainder across the first pieces deterministically.

Because the pieces are views, splitting costs nothing. But views can't cross a process boundary. Multiprocessing will copy them anyway when pickling. For thread-based parallelism the views are shared right. This Is one of the reasons threads are attractive for NumPy work.

For chunking rather than cutting. Fixed-size pieces. Many that turns out to be &mdash; passing clear boundaries is clearer:

```python
np.split(a, range(chunk, len(a), chunk))
```

That cuts each `chunk` elements and leaves a shorter final piece. This Is often what "process in batches of 1000" means.

## The summary

**Joining along an existing axis**: `concatenate`, with an explicit `axis`.

**Adding a new axis**: `stack`, with an explicit `axis`.

**1-D arrays into columns**: `column_stack`, not `hstack`.

**Assembling from named blocks**: `block`.

**Duplicating**: `tile` for the whole array, `repeat` for each element &mdash; and neither if broadcasting would do the job without allocating.

**Adding borders**: `pad`, with the mode chosen for the boundary condition.

**Dividing**: `split` for exact division, `array_split` for uneven, explicit boundaries for fixed-size chunks.

And the rule that replaces all of them. None of these belongs inside a loop that runs once per element. Collect into a Python list and join once, or preallocate and assign into slices.

## Questions people ask

<strong>What is the difference between concatenate and stack?</strong> concatenate joins along an existing axis. stack creates a new axis, so all inputs must have identical shapes.

<strong>When do I use vstack and hstack?</strong> vstack joins rows, hstack joins columns. They are shortcuts for concatenate on axis 0 and axis 1, with 1D inputs treated as rows.

<strong>Why does concatenate raise a dimension error?</strong> All axes except the one you join along must match. Print the shapes and find the one that differs.

<strong>How do I split an array into equal parts?</strong> np.split(a, n) needs the length to divide evenly. Use np.array_split when it may not, which gives parts of nearly equal size.

<strong>Do the pieces from split share memory?</strong> Yes, they are views into the original. Copy them if you plan to modify one.

<strong>How do I stack many arrays efficiently?</strong> Collect them in a list and make one concatenate call at the end. Repeatedly stacking two at a time copies the growing result each time.

## A closing note

Joining arrays is one of the places where NumPy offers a few functions for what feels like one job. The abundance is more confusing than helpful at first.

The way through it's the question at the top of this module. Does the result have the same number of dims as the inputs, or one more? all else is a convenience wrapper over that choice. `concatenate` and `stack` with an clear `axis` will do any of it right if you'd rather not note the rest.
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

Transposing an array swaps its axes. For a 2-D array, rows become columns and columns become rows. For higher-dimensional arrays, the axes are permuted in a specified order. The operation is instant because no data is moved. NumPy simply changes the strides and the shape in the array description.

That zero-cost property is worth understanding. A 2-D array with shape (1000, 2000) uses the same memory as its transpose. np.shares_memory confirms that the transpose is a view of the original. Writing to the transpose changes the original, because they are the same block of bytes with different descriptions.

The strides tell NumPy how many bytes to step for each axis. A C-contiguous (1000, 2000) float64 array has strides (16000, 8). Each row is 16000 bytes long. Each element within a row is 8 bytes. The transpose swaps the strides to (8, 16000). Now stepping along the first axis moves 8 bytes, which walks through what used to be columns.

For 2-D arrays, the shorthand a.T is the standard notation. For higher dimensions, np.transpose with an axes argument gives you full control. np.swapaxes swaps exactly two axes, which is simpler when that is all you need.

The practical consequence of strides is memory layout. A C-contiguous array has its last axis changing fastest. A Fortran-contiguous array has its first axis changing fastest. A transposed C-contiguous array is Fortran-contiguous. Operations that scan along the wrong axis are slower because they jump through memory instead of walking sequentially.

That performance difference is small for most work. It matters for tight numerical loops and for interoperating with libraries that expect a specific memory order. np.ascontiguousarray copies the data into C order when you need it.

This module covers transpose for 2-D and higher-dimensional arrays, the strides that make it free, the memory-order conventions, and swapaxes and moveaxis for targeted axis manipulation. The examples verify the view property and show how strides change.


An array knows how many bytes to step for each axis. Transposing swaps those numbers along with the shape. The underlying buffer is untouched.

That is why `a.T` on a gigabyte array returns instantly. It's a view, and `np.shares_memory(a, a.T)` confirms it.

all else in this module follows from that one fact.

## The 1-D trap

`v.T` where `v` has shape `(3,)` gives shape `(3,)`. Nothing happens.

There's no second axis to swap. The step is meaningless and NumPy performs it silently rather than raising. People coming from MATLAB or from linear algebra form expect a column vector and get their input back.

The fix is to add an axis: `v[:, None]` gives `(3, 1)`. `v[None, :]` gives `(1, 3)`. `reshape(-1, 1)` does the same job.

This is also why an outer-style step is written `v[:, None] - v` rather than `v.T - v`. The first broadcasts `(3,1)` against `(3,)` to give `(3,3)`. The second subtracts an array from itself and gives zeros.

## More than two axes

`.T` reverses **all** axes. On shape `(2, 3, 4)` it gives `(4, 3, 2)`.

That is well defined but rarely what anyone wants. With three or more axes the notable step is often moving one exact axis one spot.

`a.transpose(2, 0, 1)` names the new order by old spots. Old axis 2 first, then old axis 0, then old axis 1. Reading it in that direction. "where does each new axis come from". Is the way to keep it straight.

## swapaxes and moveaxis

Both are clearer than counting.

`np.swapaxes(a, 0, 2)` exchanges two axes and leaves the rest alone.

`np.moveaxis(a, 0, -1)` takes axis 0 and puts it at the end, sliding the others along. This is the canonical fix for image layout. Deep learning frameworks want `(channels, height, width)`, image libraries want `(height, width, channels)`. `moveaxis` converts between them for free.

Both return views.

## Contiguity, and the copy you did not ask for

An array created by `reshape` on fresh data is **C-contiguous**. The last axis varies fastest and the elements sit in memory in the order you'd read them.

Transposing breaks that. The transposed view is F-contiguous instead. The same buffer, read column-first.

Most steps don't care. But anything that needs a flat contiguous buffer must copy:

`ravel()` returns a view when it can and a copy when it can't. On a transposed array, it can't.

`reshape` has the same action. This Is why "reshape returns a view" carries a *often*.

Neither warns you. If it matters. Because the array is large, or because you were leaning on writing through the result. Check with `np.shares_memory`, or force the issue with `np.ascontiguousarray` so the copy is clear and happens where you can see it.

## Transpose is not rotation

This trips people up on image data.

Transpose reflects along the main main-line. Rotating a quarter turn is `np.rot90`. Mirroring is `np.flipud` (up-down) and `np.fliplr` (left-right).

They're related &mdash; a rotation is a transpose followed by a flip &mdash; but they're other steps. Reaching for `.T` to turn an image gives a mirrored result that looks almost right and isn't.

## C order and F order, stated plainly

An array's elements are stored in one flat run of memory. The **order** decides which axis varies fastest as you walk that run.

C order &mdash; NumPy's default, named for the C language &mdash; means the **last** axis varies fastest. Row by row.

Fortran order means the **first** axis varies fastest. Column by column.

A transposed C-sorted array is F-contiguous. Reading the transpose row by row is reading the first column by column. Nothing moved. The same bytes are simply given differently.

Both flags can be true at once for a 1-D array or an array with a length-1 axis. Both can be false for a strided slice like `a[::2]`. `a.flags` reports all of it.

Where this turns hands-on: some LAPACK routines want Fortran order and will copy inside if they don't get it. Interfacing with Fortran or MATLAB-derived code at times needs `np.asfortranarray`. For all else, staying in C order and not thinking about it's right.

## expand_dims and squeeze at boundaries

The length-1 axis is the currency of shape negotiation between libraries.

A model trained on batches expects `(batch, features)` and gets a single sample of shape `(features,)`. `x[None]` or `np.expand_dims(x, 0)` adds the batch axis.

A result comes back as `(n, 1)` and the next function wants `(n,)`. `squeeze` drops it.

`expand_dims(a, axis)` is the clear form of `a[None]`. Reads better when the axis spot is found rather than literal.

`squeeze` with no arg drops **each** length-1 axis. This Is the source of a truly nasty intermittent bug. A batch of one sample loses its batch dim. The code works for each batch size except one. Always name the axis. `squeeze(axis=1)`. In code that handles var batch sizes.

## einsum as general axis manipulation

Once an step needs a transpose, two `newaxis` insertions and a sum over a given axis, `np.einsum` often expresses it more clearly.

The subscript string names an index for each axis of each operand and says which live:

`"ij->ji"` is a transpose. `"ii->i"` extracts a main-line. `"ij->j"` sums over rows. `"ij,jk->ik"` is mat product. `"bij,bjk->bik"` is batched mat product.

Indices that appear on the left but not the right are summed over. Indices repeated between operands are matched and times'd.

It isn't always fast &mdash; for plain mat products, `@` dispatches to a tuned BLAS routine and einsum may not. Its edge is legibility. The string states the step. Here A chain of transposes and broadcasts states only the mechanics.

`np.einsum_path` can be used to inspect and optimise the contraction order for expressions with a few operands. Here The order truly matters.

## The batch-axis convention

Most numeric code follows one rule: **the batch axis comes first. The axes being operated on come last**.

`(batch, height, width, channels)` for images in TensorFlow. `(batch, channels, height, width)` in PyTorch. `(samples, features)` for tabular data.

The reason the operated-on axes go last is broadcasting. Trailing axes align on its own. A per-channel or per-feature param of shape `(channels,)` mixes with the data without any index juggling. Put the channel axis first and the same step needs `[:, None, None]`.

`matmul` follows the same rule: it treats the last two axes as the mat and broadcasts all before them. A `(batch, n, k) @ (k, m)` works right.

Following the rule in your own arrays means broadcasting and `matmul` cooperate with you rather than needing a transpose at each boundary.

## In practice

Use `.T` freely on 2-D and never on 1-D.

Use `moveaxis` or `swapaxes` on higher dims. They name what you meant and `.T` reverses all.

note that all of them return views over the same bytes. A later `ravel` or `reshape` may copy without telling you. Check with `np.shares_memory` when it matters, or force it with `np.ascontiguousarray`.

And keep the batch axis first. Most of the shape gymnastics people write is the cost of having put it one spot else.

## Diagonals and axis-aware helpers

`np.main-line(a)` extracts the main main-line and returns a view in modern NumPy. Read-only. Writing to it has no steady meaning across the strides involved.

`np.trace(a)` sums the main-line without materialising it.

`np.fill_diagonal(a, value)` writes to the main-line in place. This Is the supported way to modify it. It's the standard step when building an adjacency or distance mat that should have zeros on the main-line.

`offset` on `main-line` selects the super- or sub-diags. This Is how you extract a band.

## rollaxis, and why not to use it

Older code uses `np.rollaxis`. This Moves an axis but with arg semantics that are truly hard to reason about. The destination is read differently based on direction.

`np.moveaxis` was added namely to replace it, with the obvious semantics: source and destination, both plain spots.

If you meet `rollaxis` in existing code, translating it to `moveaxis` and checking the resulting shape is often worth doing while you're there. If you're writing new code, there's no reason to use it.

## Checking that a transform did what you meant

Axis handling is the easiest place in NumPy to give a result that has the right shape and the wrong contents.

Two checks catch nearly all of it.

**Verify a known element.** After `moveaxis(a, 0, -1)`, confirm that `b[i, j, k] == a[k, i, j]`. One assertion docs the transform better than a comment does.

**Use distinguishable test data.** `np.arange(24).reshape(2, 3, 4)` has a unique value in each spot. Any misplacement is visible. An array of ones or of random values hides just the errors you're looking for.

This is worth doing because the failure mode. Correct shape, permuted contents. Makes no error and often no obviously wrong output, just results that are subtly worse than they should be.

## The summary

`.T` &mdash; reverses all axes. Right for 2-D, wrong for most higher-dimensional intent. Silently a no-op on 1-D.

`transpose(order)` &mdash; clear permutation, read as "where each new axis comes from".

`swapaxes(i, j)` &mdash; exchange two, leave the rest.

`moveaxis(src, dst)` &mdash; relocate one, slide the rest. The clearest of the four. The right default for anything above 2-D.

`expand_dims` / `squeeze` &mdash; add and drop length-1 axes, with `squeeze` needing an clear axis in any code that handles var batch sizes.

`einsum` &mdash; when the index bookkeeping has become the substance of the step.

All of them return views. That is what makes them free. It's also why a later `ravel` or `reshape` may copy without saying so. `np.shares_memory` when it matters, `np.ascontiguousarray` when you want the copy to happen one spot visible.

## A closing note on cost

each step in this module is free. That is worth stating once more because it changes how you write code.

There's no reason to avoid a transpose, a `moveaxis` or an `expand_dims` on speed grounds. They adjust a handful of ints showing the array and return at once, what its size.

The cost, when it comes, arrives later. At the point a thing needs contiguous memory and quietly copies. That is where to look when a pipeline is slower than the steps in it suggest. `a.flags` plus `np.shares_memory` will tell you within a minute.

## Questions people ask

<strong>Does transpose copy the data?</strong> No. It returns a view with the strides swapped, so it is instant. Some later operations may then need to copy.

<strong>What does a.T do for a 1D array?</strong> Nothing, because there is only one axis. Turn the vector into a column with a[:, None] if you need a 2D shape.

<strong>How do I transpose a 3D array?</strong> Use a.transpose(order), listing the new axis order, for example a.transpose(2, 0, 1). a.T just reverses all the axes.

<strong>What do swapaxes and moveaxis do?</strong> swapaxes exchanges two axes. moveaxis moves one axis to a new position and leaves the others in order, which is often clearer.

<strong>Why is my transposed array slower to process?</strong> It is no longer C-contiguous, so memory access jumps around. np.ascontiguousarray makes a copy in the order you want.

<strong>How do I turn images from HWC to CHW?</strong> Use np.moveaxis(img, -1, 0) or img.transpose(2, 0, 1). Both are views until you force a copy.

## Where axis work fits

Reordering axes is almost always a translation step: between how data arrived and how the next function wants it.

That means the right question is rarely "how do I transpose this" but "what layout does the thing I am calling expect". Answering that first often reveals that one `moveaxis` at the boundary replaces a few scattered ones inside. That keeping a single rule throughout drops most of them fully.
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
intro: sort, argsort and searchsorted, and why the arg version is often the one you need.

## Copy or in place

NumPy provides two ways to sort an array. np.sort returns a new sorted array. The method a.sort modifies the array in place and returns None. That distinction follows NumPy's general convention: the function form is non-destructive, the method form mutates.

Knowing which one you used matters because in-place sorting on a view changes the underlying array. If you have a slice of a larger array and sort it in place, the original array sees those rows rearranged. That is sometimes the intent and sometimes a bug. The function form avoids the question by always returning a copy.

For multi-dimensional arrays, the axis parameter decides which axis to sort along. The default is the last axis, which sorts each row independently in a 2-D array. axis=0 sorts each column independently. Neither rearranges whole rows or whole columns. If you want to sort rows by the values in one column, you need argsort.

argsort returns the indices that would sort the array. You can then use those indices to reorder both the array and any related arrays in the same way. That pattern is how you sort a matrix by one column while keeping the rows intact.

searchsorted finds insertion points in a sorted array. Given a sorted array and a set of values, it returns the index where each value would go to keep the array sorted. That is useful for binning, for assigning labels to ranges, and for any task where you have boundaries and need to know which bin a value falls into.

partition is a faster alternative when you need only the k smallest or largest values and do not care about their order. It rearranges the array so that the element at position k is where it would be in a fully sorted array, with smaller elements before it and larger elements after. That is an O(n) operation rather than O(n log n).

This module covers sort, argsort, searchsorted, partition, and argpartition. The examples show sorting in one and two dimensions and the relationship between argsort and fancy indexing.


`np.sort(a)` returns a new sorted array and leaves `a` alone. `a.sort()` sorts `a` itself and returns `None`.

That is NumPy's general rule for steps that have both forms. It's worth leaning on. If you see a bare method call with no set, it's modifying a thing.

There's no `reverse=` arg. Sort ascending and reverse with `[::-1]`. This Is a free view.

## The axis default

On a 2-D array, `sort()` sorts along the **last axis**. Each row on its own.

This is a truly dangerous default when the array is a table. Sorting a `(rows, columns)` array of records scrambles each row inside. The name column gets sorted, the salary column gets sorted. The correspondence between them is destroyed.

`sort(axis=None)` flattens and does one global sort. `sort(axis=0)` sorts each column on its own. This Has the same problem in the other direction.

**None of these sort rows as units.** For that you need `argsort` on a key column and then fancy indexing.

## argsort is the useful one

`np.argsort(x)` returns the spots that would sort `x`.

That indirection is the point. Apply the same index array to any number of parallel arrays and they stay aligned:

```python
order = np.argsort(score)
names[order], score[order], dates[order]
```

This is how you sort a table by a column. It's also how you give a ranking, take the top n, or reorder anything that travels alongside the sorted values.

Descending is `np.argsort(x)[::-1]`.

One subtlety: the default sort is **quicksort**. This Isn't stable. Equal elements can come out in any order. Pass `kind="stable"` when ties must preserve their first scaled order. say when you're sorting by a second key after already sorting by a first.

## Several keys

`np.lexsort` sorts by multiple keys, and the arg order reads backwards: the **last** array is the main key.

`np.lexsort((salary, dept))` sorts by department, breaking ties by salary.

all gets this wrong the first time. The mnemonic that helps. The keys are applied in order from last to first, like a stable sort chain where the final pass dominates.

## Only the top k

Sorting 200,000 values to look at 5 of them is wasteful.

`np.argpartition(x, -5)` rearranges so that the 5 largest occupy the last 5 slots, in linear time. It does **not** order them. It doesn't order anything else. It only promises the split boundary.

If you need those five in order, sort just those five. That is five elements instead of two hundred thousand.

The same trick works for the smallest k with a plus index. For medians. This Is what `np.median` uses inside.

## searchsorted

Given a sorted array, `np.searchsorted(edges, values)` returns where each value would be inserted to keep it sorted. It's a binary search. It's fast even on large arrays.

Two uses come up constantly.

**Bucketing.** Given cut points, `searchsorted` gives the bucket index for each value right. Indexing a label array with the result assigns groups in one line. `side="right"` versus `side="left"` decides which bucket an exact boundary value falls into. The only case where they differ.

**Lookup.** Finding many values in a large sorted array is `O(m log n)` this way, against `O(mn)` for repeated checks.

For pure membership testing where order doesn't matter, `np.isin` is simpler and doesn't need sorted input.

## The mistakes

**Sorting a table with `sort()`** and destroying the row correspondence. Use `argsort` on a key column.

**given steadiness.** The default isn't stable. Pass `kind="stable"` when it matters.

**Getting `lexsort` backwards.** The last key is main.

**Full sorting for a top-n.** `argpartition` exists just for that.

## The sort kinds

`kind` selects the method, and the choice at times matters.

`"quicksort"` is the default, an introsort . Fastest on average, not stable. Its worst case is handled by falling back to heapsort.

`"stable"` promises that equal elements keep their first scaled order. It's what you need when sorting by a second key after already sorting by a first. An unstable sort would discard the first sorting.

`"heapsort"` has a sure worst case and uses no extra memory. This Is at times the deciding factor.

`"mergesort"` is an alias for `"stable"`.

The speed gap is modest for most data. Steadiness isn't a speed question. When you need it, you need it.

## Sorting records

Structured arrays &mdash; arrays with named fields &mdash; can be sorted by field name:

```python
a.sort(order=["dept", "salary"])
```

This is the closest NumPy comes to sorting a table by columns. It works because the structured dtype makes each row a single close item.

For plain 2-D numeric arrays, there's no `order` arg. The answer is the `argsort` idiom. Sort the key column, apply the resulting index to the whole array with fancy indexing. `a[np.argsort(a[:, 2])]` sorts rows by the third column.

For more than one key, `lexsort` makes the index and the same fancy-index use follows.

## where, nonzero, and finding things

`np.nonzero(mask)` returns the indices of True elements, as a tuple with one array per axis. `np.where(mask)` with a single arg is the same function.

The tuple form is designed to be used as an index: `a[np.nonzero(mask)]` selects the matching elements. Unpacking it with `rows, cols = np.nonzero(mask)` gives coords.

`np.flatnonzero(mask)` is the flat-index version, and is often what you want for a 1-D array. It returns a plain array rather than a one-element tuple.

For "the first element matching a rule", `np.argmax(mask)` is the fast answer. It stops at the first True. It returns 0 when nothing matches. This Is the same from a match at spot zero. Check `mask.any()` first. There's no built-in "find first" that handles the empty case. This two-step is the idiom.

## searchsorted in more detail

`searchsorted` needs its first arg to be **sorted**. Doesn't check. Passing unsorted data gives wrong answers silently. This Is the main way it goes wrong.

`side="left"` returns the first spot where the value could be inserted. `side="right"` returns the last. They differ only for values that are already present. The choice decides which bucket a boundary value falls into.

For bucketing, `side="right"` with cut points means a value just on a boundary goes into the upper bucket. This Matches the usual rule for grade boundaries and histogram bins.

`sorter` lets you pass an `argsort` result so the lookup can be done against an unsorted array without sorting it first. handy when the array must keep its first order for other reasons.

`np.digitize` is a related function with a `right` arg whose meaning is the reverse of what the name suggests in one of its branches. `searchsorted` is easier to reason about, and does the same job.

## Ranking

A ranking is `argsort` applied twice.

`np.argsort(x)` gives the spots in sorted order. `np.argsort(np.argsort(x))` gives, for each element, its rank.

That double use is unintuitive the first time and worth the moment it takes to see. The first argsort answers "which element belongs at each rank". Inverting that mapping answers "which rank does each element get".

Ties get in a row distinct ranks rather than being averaged. This Isn't what most statistical meanings of rank want. `scipy.stats.rankdata` handles tie-breaking properly. Is the right tool when the ranking is going into a statistic.

## The performance summary

Sorting is `O(n log n)`, and `argsort` costs slightly more than `sort` because it moves indices alongside checks.

`argpartition` is `O(n)` and is the right choice for any top-k or bottom-k question. The saving is large. For the top 5 of 200,000 values it's roughly an order of magnitude.

`searchsorted` is `O(log n)` per lookup against an already-sorted array. `m` lookups cost `O(m log n)`. If you're searching the same array again and again, sorting it once and using `searchsorted` beats any linear scan.

`np.isin` builds a sorted structure inside. It's `O((n+m) log(n+m))`. Better than the naive compare. Worth knowing that it isn't free either.

## Sorting along an axis of a higher-dimensional array

`sort` takes an `axis` like every other step. The default is `-1` &mdash; the last one.

On a 3-D array that means each 1-D line along the last axis is sorted on its own. That is rarely wrong but often not what was intended. Passing `axis` by name makes the intent visible.

`argsort` on a multi-dimensional array returns indices **along that axis only**, not flat spots. Applying them needs `np.take_along_axis`:

```python
idx = np.argsort(scores, axis=1)
ordered = np.take_along_axis(values, idx, axis=1)
```

That is the multi-dimensional version of the sort-by-key idiom. It's the function people often fail to find. `np.put_along_axis` is the set counterpart.

## Descending, and the sign trick

There's no `reverse=` arg anywhere in NumPy's sorting.

`np.sort(a)[::-1]` reverses the result, and the slice is a free view.

For `argpartition` and `argsort`, negating the values is often cleaner than reversing the result. It keeps the index math straightforward: `np.argsort(-scores)` gives descending order right.

That works for numeric data. It doesn't work for unsigned ints. Here Negation wraps. It's a subtle way to get a wrong answer on `uint8` image data.

## Searching by value

There's no `index()` method. Finding where a value occurs is a compare followed by a search:

`np.flatnonzero(a == value)` gives each spot, as a plain array.

`np.argmax(a == value)` gives the first, in one pass, with the caveat that it returns 0 when nothing matches.

For a sorted array, `np.searchsorted` finds the spot in logarithmic time. This Is the right choice when searching again and again.

For membership across two arrays, `np.isin` handles it in one call rather than a loop of checks.

## The summary

`np.sort` copies. `a.sort()` modifies. That gap holds throughout NumPy.

`argsort` is the one to use when anything else must follow the sorting. This is most of the time.

`kind="stable"` when ties must keep their first order. This Includes any multi-pass sort by successive keys.

`lexsort` for a few keys, remembering that the **last** one is main.

`argpartition` for top-k, which is linear rather than `n log n`.

`searchsorted` for insertion points and bucketing, on data that is truly sorted &mdash; it doesn't check.

`take_along_axis` when applying `argsort` results on more than one dim.

Between them those cover each sorting question. The two that get used most are `argsort` and `argpartition`.

## One more thing about stability

Steadiness isn't a speed setting, and it's worth one more paragraph because the cost of getting it wrong is invisible.

An unstable sort is free to reorder equal elements arbitrarily. That means two runs on the same data can give other output. The gap only appears when there are ties. Code that sorts by a secondary key and then by a main key leans fully on the second sort preserving the first sorting. With the default `kind` it doesn't.

When a sort follows another sort, or when the output order of tied records is observable, pass `kind="stable"`. The cost is small and the option is a bug that copies intermittently.

## Questions people ask

<strong>What is the difference between sort and argsort?</strong> sort returns the sorted values, while argsort returns the indices that would sort the array. Use argsort to reorder a second array alongside the first.

<strong>How do I sort in descending order?</strong> Sort ascending and reverse with a[::-1], or negate numeric values. There is no reverse flag on np.sort.

<strong>Does np.sort sort in place?</strong> np.sort returns a copy. The method a.sort() sorts in place and returns None.

<strong>How do I find where to insert a value in a sorted array?</strong> Use np.searchsorted. It does a binary search, so it is far faster than scanning for large arrays.

<strong>How do I get the k largest values quickly?</strong> Use np.partition or argpartition. They place the k-th element correctly without sorting everything, which is faster for large arrays.

<strong>Is the sort stable?</strong> Use kind='stable' to guarantee that equal elements keep their original order. The default quicksort does not promise that.

## Where sorting fits

Sorting is rarely the goal in itself. It's the step that makes a thing else possible. A ranking, a top-n, a binary search, a group-by on the boundaries where a key changes, a merge of two datasets.

That framing helps when choosing. If the sorted array itself isn't needed, `argsort` or `argpartition` often is. And if you only need the order to apply it elsewhere, sorting the values was wasted work.
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
intro: Counting distinct values, checking arrays, and rebuilding the first.

## unique

Finding distinct values is one of the first things you do with categorical or integer data. How many different ids are there? What are the distinct labels? Are there values in one array that are missing from another? NumPy's set operations answer these questions on arrays directly, without converting to Python sets.

np.unique returns the distinct values from an array, sorted. The sorting is not optional. That matters because it means the output order does not match the input order. If you need the values in the order they first appeared, you can use the return_index parameter and sort by those indices, but the default behaviour is sorted output.

Two things about unique catch people. First, it flattens multi-dimensional arrays before finding unique values. A 2-D array of shape (3, 4) gives a 1-D array of unique values, not unique rows. Finding unique rows requires axis=0, which was added later and is less well known. Second, floating-point values that differ by tiny rounding errors are treated as distinct. Rounding before calling unique avoids spurious duplicates.

The return parameters give you extra information without a second pass. return_counts gives the frequency of each unique value. return_index gives the position of the first occurrence. return_inverse gives an array that reconstructs the original from the unique values. These are cheaper than calling unique once and then searching for each value separately.

The set operations -- intersect1d, union1d, setdiff1d, and setxor1d -- work on sorted unique arrays. They answer questions like "which values are in both arrays", "which values are in the first but not the second", and "which values are in exactly one of the two". Each returns a sorted 1-D array.

in1d and its modern replacement isin test membership. Given two arrays, isin returns a boolean array showing which elements of the first are present in the second. That boolean array can be used directly as a mask for filtering.

This module covers unique with its return parameters, the set operations, and isin. The examples show common use cases: deduplication, frequency counting, filtering by membership, and comparing two datasets for overlap.


`np.unique(a)` returns the distinct values, **sorted**, as a 1-D array.

Two things about that are worth stating by name, because both catch people.

It's always sorted. If you wanted first-appearance order, `unique` alone doesn't give it. You need `return_index` and then a sort of those indices.

It always flattens, unless you pass `axis`. A 2-D input gives back a flat list of each distinct value in the whole array.

## The optional returns

Three flags turn `unique` from a de-duplicator into a thing a lot more handy.

**`return_counts`** gives how many times each value occurred, aligned with the values. This is a rate table. Mixed with `argmax` it gives the mode in two lines with no loop.

**`return_index`** gives, for each unique value, the index in the input where it first appeared. handy when you want the *first* record for each key rather than just the key.

**`return_inverse`** gives, for each element of the input. This Unique value it matches to. `vals[inv]` rebuilds the input just.

That last one is worth dwelling on. It's label encoding. An array of groups turns an array of small ints plus a lookup table. Machine learning pipelines do this constantly. `np.unique(..., return_inverse=True)` is the whole setup.

The returns come back in a fixed order. Values, index, inverse, counts. Even so of which flags you set. Unpack carefully when you enable more than one.

## Unique rows

`np.unique(rows, axis=0)` treats each row as an item and drops copy rows.

This is what you want for de-duplicating records. It composes with `return_counts` to find how many times each distinct row appeared. A group-by, for the case where the whole row is the key.

Rows are checked elementwise, and the result is sorted lexicographically.

## Set operations

Four functions, all following the same rules: they treat the inputs as sets, de-copy, and return sorted results.

`intersect1d` &mdash; in both.
`union1d` &mdash; in either.
`setdiff1d` &mdash; in the first only.
`setxor1d` &mdash; in just one.

The `1d` in the names is a warning. They flatten their inputs. If you pass 2-D arrays you get a flat answer.

`intersect1d` accepts `assume_unique=True`, which skips the inner de-duplication and is usefully faster on large arrays you already know are unique.

## isin is the different one

The set functions **reduce**. They answer "what is in both?" and hand you a smaller array, with the first spots gone.

`np.isin(a, b)` **preserves shape**. It returns a boolean mask the same shape as `a`, saying whether each element appears in `b`.

That gap decides which one you need. If the question is "which values do these two arrays share?", use `intersect1d`. If the question is "which rows of my table have an id in this list?", you need the mask. You're going to index with it. And `intersect1d` has thrown away just the data you need.

`~mask` inverts it, which is how you exclude a list rather than include one.

## Performance

These are all sort-based, so roughly `O(n log n)`. That is fast. For repeated membership tests against the same fixed set, a Python `set` or a sorted array with `searchsorted` can beat rebuilding the compare each time.

For counting, `np.bincount` is faster than `unique(return_counts=True)` when the values are small non-minus ints. It can index right instead of sorting.

## The mistakes

**Expecting first-appearance order.** `unique` sorts.

**Passing 2-D to a set function** and being surprised by a flat result. They all flatten.

**Reaching for `intersect1d` when filtering.** It discards spots. `isin` keeps them.

**Unpacking the returns in the wrong order.** Values, index, inverse, counts. Always in that order, whichever subset you asked for.

## bincount, the fast path for integers

When the values are small non-minus ints, `np.bincount` counts them far faster than `unique(return_counts=True)`. It indexes an output array right instead of sorting.

`np.bincount(a)` returns an array of length `a.max() + 1`. Here Spot `i` holds the count of value `i`. Values that never appear get zero. This Is either convenient or a nuisance based on whether the value space is dense.

`minlength` forces a min output size. This Matters when you're counting class labels and a class might be absent from a given batch. Without it, the output length varies with the data and downstream code breaks.

The `weights` arg turns it into a group-sum. `np.bincount(group_ids, weights=values)` sums the values belonging to each group in a single pass. This Is the fastest group-by NumPy offers and a truly handy thing to know.

The constraint is that the values must be non-minus ints. Memory is scaled to the largest one. Counting values around a million allocates a million-element array even so of how few distinct values there are.

## Grouping without pandas

The `unique` returns compose into a real group-by.

```python
keys, inverse = np.unique(group_column, return_inverse=True)
sums = np.bincount(inverse, weights=value_column)
counts = np.bincount(inverse)
means = sums / counts
```

`unique` maps any keys &mdash; strings included &mdash; to dense ints. `bincount` aggregates over those ints. Four lines, no loop. It handles any number of groups.

For aggregations that aren't sums, sorting by the key and using `np.split` at the boundaries where the key changes gives a list of per-group arrays:

```python
order = np.argsort(keys)
sorted_keys = keys[order]
cuts = np.flatnonzero(sorted_keys[1:] != sorted_keys[:-1]) + 1
groups = np.split(values[order], cuts)
```

That is more machinery than pandas' `groupby`. It's the right amount when adding pandas to a project for one aggregation would be the larger cost.

## histogram, for continuous values

`unique` is for discrete values. Its smooth counterpart is `np.histogram`. This Counts how many values fall into each of a set of bins.

It returns counts and edges. The edges array is one longer than the counts. N bins have n+1 boundaries. A small detail that causes a lot of off-by-one confusion when plotting.

`bins` accepts a count, an clear array of edges, or one of a few auto rules like `"auto"` and `"fd"` that choose a bin width from the data.

`np.histogram2d` and `np.histogramdd` handle two and more dims.

The bins are half-open &mdash; `[a, b)` &mdash; except the last. This Includes its right edge so that the max value is counted one spot. That skew is deliberate and at times surprising.

## assume_unique, and when to use it

`intersect1d`, `setdiff1d` and `isin` accept `assume_unique=True`.

Setting it skips the inner de-duplication. This Is a real saving on large arrays. Setting it wrongly gives **wrong answers**, not an error. Copies are handled as though they weren't there. Results can come out with surprise repeats.

Use it only when uniqueness is sure structurally. The array came from `unique`, or it's a main key, or you've just checked. "It should be unique" isn't the same thing.

`isin` also has a `kind` arg that chooses between a sort-based and a table-based setup. The table-based version is much faster for ints over a small range and uses memory scaled to that range. The auto choice is often right and worth replacing only after measuring.

## Ordering, and how to get first-appearance order

each one of these functions returns sorted output. At times sorted isn't what you want.

For first-appearance order, use `return_index` and sort the indices:

```python
vals, idx = np.unique(a, return_index=True)
first_seen_order = vals[np.argsort(idx)]
```

The indices say where each unique value first appeared. Sorting by them restores the first meet order.

This comes up more often than it looks. Group codes that should follow the data's order, deduplication that should keep the first case, log analysis where the sequence carries meaning.

## Summary of the choices

**Distinct values, any dtype**: `np.unique`.

**Counts of small non-negative integers**: `np.bincount`, and use `minlength`.

**Counts of anything else**: `np.unique(return_counts=True)`.

**Group aggregation**: `unique(return_inverse=True)` feeding `bincount(weights=...)`.

**Continuous data**: `np.histogram`.

**Comparing two arrays as sets**: the `1d` family, remembering that they flatten.

**Filtering by membership**: `np.isin`, because it keeps the shape and the others do not.

## Uniqueness on floats

Applying `unique` to floating-point data often disappoints. Values that are conceptually equal differ in the last bits.

`np.unique([0.1 + 0.2, 0.3])` returns two values, not one.

There's no handling arg, and adding one would be ill-defined. "close enough" isn't transitive. A tolerant unique has no unambiguous answer.

The hands-on approaches are to round first, `np.unique(np.round(a, 6))`. This Is exact and cheap but sensitive to values sitting near a rounding boundary. Or to sort and group with an clear handling if the semantics matter.

For anything more careful, this is a clustering problem rather than a uniqueness problem. Treating it as one avoids pretending the answer is exact.

## Set operations on rows

The `1d` family flattens, so checking two tables row-wise needs a other approach.

`np.unique(rows, axis=0)` handles de-duplication. For intersection and gap between two sets of rows, the usual trick is to view each row as a single opaque item. Either through a structured dtype, or by converting rows to tuples and using Python sets when the arrays are small enough.

For larger data this is the point where pandas' `merge` is the right tool. Reaching for it isn't a defeat. NumPy is on purpose a numeric array library rather than a relational one.

## Performance notes

`np.unique` sorts, so it's `O(n log n)` and allocates.

`np.bincount` is `O(n)` for small non-minus ints. Allocates scaled to the largest value rather than the number of distinct ones. For values up to a few million that is a good trade. For sparse large values it isn't.

`np.isin` builds a sorted structure or a lookup table based on `kind`. It isn't free either. But it's far better than a loop of checks. Better than again and again calling `intersect1d`.

For repeated membership tests against a fixed small set, a Python `set` can beat all of them. The per-call cost of NumPy dominates when the query is a single value.

## The summary

`np.unique` &mdash; sorted distinct values. `return_counts` for rates, `return_inverse` for label encoding, `return_index` for first case, `axis=0` for rows.

`np.bincount` &mdash; fast counting for small non-minus ints, with `minlength` to fix the output size and `weights` to turn it into a group-sum.

`np.histogram` &mdash; the smooth analogue, returning counts and one more edge than counts.

`intersect1d` / `union1d` / `setdiff1d` / `setxor1d`. Set checks, all sorting, de-duplicating and flattening.

`np.isin` &mdash; membership as a mask of the first shape. This Is the one to use for filtering.

The recurring choice is between the functions that **reduce** and the one that **preserves shape**. If the answer is going to index a thing, you want the mask.

## A closing note

The functions in this module are simple on their own and powerful in mix. `unique` with `return_inverse` feeding `bincount` with `weights` is four lines that replace a loop, a dict and a fair amount of care about missing keys.

The one gap worth carrying away is between reducing and preserving shape. Almost each mistake in this area is reaching for a set function. Which discards spots. When the question was really about filtering. This Needs them. When the answer is going to index a thing, `isin` is the function you want.

## Questions people ask

<strong>What does np.unique return?</strong> The sorted distinct values. Add return_counts=True for counts and return_inverse=True for the mapping back to the original.

<strong>How do I count occurrences of each value?</strong> Use np.unique(a, return_counts=True). For small non-negative integers np.bincount is faster.

<strong>How do I find common elements of two arrays?</strong> Use np.intersect1d. There are also union1d, setdiff1d and setxor1d for the other set operations.

<strong>What is the quick way to test membership?</strong> np.isin(a, values) returns a boolean array the shape of a. It is the vectorised version of the in operator.

<strong>Does np.unique keep the original order?</strong> No, it sorts. To keep the first-seen order, use return_index=True and sort those indices.

<strong>Can I find unique rows?</strong> Yes, np.unique(a, axis=0) treats each row as one item.

## Where this fits

Counting distinct values is often the first thing anyone does with a new dataset. The last thing anyone remembers to do before trusting a result.

`np.unique(col, return_counts=True)` on each cat column at load time takes seconds and routinely surfaces the problems that would else appear much later. A group with a trailing space, an identifier that isn't unique, a class that appears twice in the training set and never in the test set.
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
intro: The modern gen API, and how to make results reproducible.

## Two APIs, one of them legacy

Random number generation in NumPy has a clear best practice, but the legacy interface still appears in most tutorials and examples. Knowing both is necessary for reading existing code. Using the new one is better for writing new code.

The legacy interface uses module-level functions: np.random.rand, np.random.randint, np.random.normal, np.random.seed. They all share a single hidden global generator. Setting the seed in one place affects every call everywhere. That makes reproducibility fragile. Two libraries that both call np.random.seed can interfere with each other.

The new interface creates explicit generator objects. rng = np.random.default_rng(42) gives you a generator seeded with 42. rng.random, rng.integers, rng.normal are methods on that object. Each generator carries its own state. Two generators with different seeds are independent. That makes testing predictable and parallel code safe.

The method names differ between the two interfaces. The legacy randint includes the low endpoint and excludes the high. The new integers includes both by default. That catches people who switch between the two without reading the signature.

Beyond the interface question, random number generation in NumPy is fast because it generates arrays directly. Calling rng.normal(size=1000000) gives you a million samples in one call. Calling it in a loop, once per iteration, is a hundred times slower. The size parameter is not a convenience. It is the intended way to generate batches.

Distributions beyond uniform and normal are available: exponential, poisson, binomial, beta, gamma, and many others. Each takes the distribution parameters and a size argument. Sampling from a discrete set uses rng.choice, which handles replacement, weights, and multi-dimensional output.

This module covers the new generator API, the most common distributions, shuffling and permutation, and the reasons to avoid the legacy interface in new code. The examples use explicit generators throughout.


You'll see both in the wild.

`np.random.rand`, `np.random.randint`, `np.random.seed` are the **legacy** interface. They all operate on a single hidden global gen.

`np.random.default_rng()` returns a **gen** object with its own state. each method lives on that object.

The new one is preferred, and the reason isn't cosmetic. A global gen means any library you import can consume from the same stream. Your seeded results change when an unrelated dependency starts drawing numbers. It also can't be used safely from more than one thread, and it makes tests interfere with each other in ways that are hard to trace.

An clear gen is passed where it's needed. Nothing else can touch it. Create it once, near the top, and thread it through.

The legacy functions aren't deprecated and existing code doesn't need rewriting. New code should use `default_rng`.

## Seeding

`default_rng(42)` gives a gen whose sequence is fully found. Two gens created with the same seed give same output.

The gen is stateful: each call advances it. In a row draws from the same gen differ. That is the point. You seed once, not before each call.

Seeding inside a loop is a common bug. It makes the same "random" value each loop. The symptom is data that looks oddly uniform.

For truly unpredictable values, call `default_rng()` with no arg. It seeds from the operating system.

## Shapes

each method takes `size`, and it accepts a tuple.

`rng.random((3, 4))` gives a `(3, 4)` array in one call. There's never a reason to loop.

`rng.ints(low, high)` is **half-open**, like `range` and like slicing: `high` is excluded. The legacy `randint` behaved the same way. `random_integers`, now removed, didn't. Which is why the memory is unreliable and worth checking.

## The distributions

`random` for uniform `[0, 1)`. `ints` for uniform ints. `normal(loc, scale)` for Gaussian. `uniform(low, high)` for a uniform range other than the unit interval.

Beyond those there are dozens. `poisson`, `steep`, `binomial`, `multivariate_normal` &mdash; all following the same `size` rule.

## choice

`rng.choice(pool, size=n)` samples with swap by default.

`replace=False` samples without, and raises if `size` exceeds the pool. That is the right action. Silently returning copies when you asked for distinct items would be worse.

`p=weights` gives a weighted draw. The weights must sum to 1 and have one entry per element of the pool.

`choice` also accepts an int instead of an array, meaning "choose from `arange(n)`". This Is often what you want when you're really choosing indices.

## Shuffling

`rng.shuffle(a)` modifies in place and returns `None`. `rng.permutation(a)` returns a shuffled copy.

On a 2-D array, both operate on the **first axis**. Whole rows move. Their contents stay intact. That is almost always what you want for a table of records. It's worth knowing rather than given it shuffles each element.

## Splitting data

The correct pattern is one permutation, then slicing:

```python
idx = rng.permutation(n)
train, test = idx[:cut], idx[cut:]
```

The tempting option &mdash; drawing a training sample and then a test sample &mdash; allows the same row into both. The two draws know nothing about each other. That leaks test data into training and inflates each score you measure later, at times sharply. The code gives no sign anything is wrong.

Permuting once makes the disjointness structural rather than random. The same index array applied to `X` and `y` keeps them aligned.

## Reproducibility in practice

Seed at the entry point, not scattered through the code. Record the seed alongside results. Pass the gen by name into any function that needs noise. It can be tested with a fixed one.

And be clear about what a seed promises. Same results for the same NumPy version and the same sequence of calls. Change the order of steps and the numbers change, even with the seed unchanged.

## What is underneath a Generator

`default_rng` returns a `gen` wrapping a **bit gen**. This Is the thing that really makes random bits. The default is PCG64.

The split matters because the two layers have other jobs. The bit gen makes a stream of uniform bits. The gen turns those into spreads. Swapping the bit gen. `default_rng(np.random.MT19937(seed))` for the old Mersenne Twister, or `Philox` for a counter-based one. Changes the stream without changing the interface.

PCG64 was chosen as the default because it's fast, has good statistical properties. Supports cheap split streams. Mersenne Twister, the legacy default, is slower and has a much larger state.

None of these are cryptographically secure. For tokens, passwords or anything an adversary shouldn't predict, use the `secrets` module, not NumPy.

## Independent streams

Running the same modelling in parallel needs each worker to draw other numbers. Seeding each with a other any int isn't a solid way to get that. Nearby seeds can give shared streams.

`SeedSequence` is the supported answer:

```python
ss = np.random.SeedSequence(12345)
children = ss.spawn(4)
rngs = [np.random.default_rng(c) for c in children]
```

Each child makes a stream that is statistically split of the others. The whole set is reproducible from the single parent seed.

`rng.spawn(n)` on a gen does the same thing more right in recent NumPy versions.

This is the right way to seed workers in a multiprocessing pool. It means one recorded seed copies the entire parallel run.

## The legacy interface, and when you need it

`np.random.RandomState` is the old object-oriented interface. The global functions like `np.random.rand` are methods on a hidden instance of it.

It's frozen for backwards match: its stream is sure never to change across NumPy versions. `gen` carries no such promise. Its output can change between versions if an method is better.

That makes `RandomState` the correct choice in just one situation. Copying results from older code or published work where the exact numbers matter.

For all else, `gen` is faster, has better spreads. Doesn't share state with every other piece of code in the process.

## Choosing a distribution

The ones that come up most, and what they model:

`uniform(low, high)` &mdash; no data beyond a range.

`normal(loc, scale)` &mdash; readings with even error, sums of many small split effects.

`lognormal` &mdash; quantities that can't be minus and are scaling: incomes, file sizes, response times.

`poisson(lam)` &mdash; counts of split events in a fixed interval: arrivals, defects, requests per second.

`steep(scale)` &mdash; waiting times between Poisson events.

`binomial(n, p)` &mdash; successes out of n trials.

Using `normal` for a quantity that can't be minus is a common modelling error. It shows up as minus durations or minus counts in made test data. `lognormal` or a truncated spread is often what was meant.

## Generating realistic test data

A few patterns worth having.

**Correlated variables**: `rng.multivariate_normal(mean, cov, size=n)` draws from a specified covariance structure, which is how you produce test data where the relationships are known.

**Categorical with known proportions**: `rng.choice(categories, size=n, p=weights)`.

**Sorted timestamps**: draw uniformly and sort, or accumulate exponential gaps with `cumsum` for a Poisson process.

**Reproducible shuffling of an existing dataset**: `rng.permutation(len(data))` applied as an index, never two independent draws.

## Reproducibility, honestly

A seed promises the same numbers for the same NumPy version, the same gen. The **same sequence of calls**.

Change the order of steps and the numbers change. Add a draw in the middle and all after it shifts. Parallelise differently and the set of numbers to workers changes.

This means a seed copies a run, not a result. Code that draws other amounts of noise based on the data won't copy across changes to that data, even with the seed fixed.

The hands-on discipline: seed once at the entry point, record the seed alongside the output, pass the gen by name into anything that needs it. Use `SeedSequence` for parallel work. Those four habits cover almost each reproducibility problem people really hit.

## Passing the generator around

The habit that makes noise testable is to accept a gen as an arg rather than creating one inside a function.

```python
def make_sample(n, rng):
    return rng.normal(size=n)
```

The caller decides the seed. So The same function serves production. Where the gen is seeded from the operating system. And tests. Here A fixed seed makes assertions possible.

A default of `rng=None` with `rng = np.random.default_rng(rng)` inside is a handy pattern: `default_rng` accepts a gen, an int seed, a SeedSequence or None. Returns a gen in each case. That gives callers all four options with one line.

The option &mdash; calling `np.random.seed` one spot and hoping &mdash; is what makes randomised code untestable and non-reproducible. Any other code drawing from the same global stream changes the results.

## Randomness in tests

A test that uses random data and a fixed seed is testing one sample. That is often fine. It's better than a test with hard-coded magic numbers.

The failure mode to avoid is a test that passes for most seeds and fails for some. If a test is checking a statistical property. That a mean is near zero, that a split is roughly weighed. The handling has to be wide enough for the spread, not tuned until the current seed passes.

`np.allclose` with an clear handling expresses that far better than exact compare. Stating the handling forces the question of how much variation is acceptable.

For anything where the property should hold for all inputs rather than one sample, property-based testing with a few seeds is the honest version.

## Common mistakes

**Seeding inside a loop.** makes the same value each loop. The symptom is oddly uniform data.

**Using `np.random.seed` in a library.** It mutates global state that belongs to the use, not to you.

**Sampling twice for a train/test split.** The two draws are split. Rows can appear in both. Permute once.

**Using `normal` for a non-minus quantity.** makes minus durations and minus counts. `lognormal` or a truncated spread is often what was meant.

**Expecting `shuffle` to return a thing.** It modifies in place and returns None. `a = rng.shuffle(a)` sets `a` to None. `permutation` is the returning version.

**given a seed copies a result rather than a run.** Change the order of draws and the numbers change, seed or no seed.

## The summary

Create one gen with `default_rng(seed)` at the entry point.

Pass it by name to anything that needs noise.

Use `SeedSequence` or `spawn` for parallel workers, never nearby int seeds.

Draw whole arrays with `size` rather than looping.

Permute an index array once when splitting or shuffling aligned data.

Record the seed with the results. Note that it copies the sequence of calls, not the conclusion.

## A closing note

Noise is one of the few areas where the convenient API and the correct API differ. Where the convenient one has been the default for long enough that most examples still use it.

`np.random.seed` and its companions aren't broken. Existing code using them doesn't need rewriting. But new code has a better option, and the reasons. Alone, thread safety, reproducible parallelism. Are the kind that only matter once, catastrophically, at the point where results can't be copied.

One gen, created by name, passed where it's needed. That single habit covers almost all.

## Questions people ask

<strong>How do I make random results reproducible?</strong> Create a generator with rng = np.random.default_rng(42) and draw from it. The same seed gives the same stream.

<strong>What is wrong with np.random.seed?</strong> It sets hidden global state shared by everything in the process. The newer Generator API keeps state in an object you pass around.

<strong>How do I shuffle or sample without replacement?</strong> Use rng.permutation(n) to shuffle, or rng.choice(a, size=k, replace=False) to sample. rng.shuffle works in place.

<strong>How do I draw from a normal distribution?</strong> Call rng.normal(loc, scale, size). Note that scale is the standard deviation, not the variance.

<strong>Is the output truly random?</strong> It is pseudorandom: deterministic given the seed but statistically well behaved. It is fine for simulation and not for cryptography.

<strong>How do I get independent streams in parallel jobs?</strong> Use SeedSequence.spawn to create child seeds. Do not just add one to the seed for each worker.

## One last habit

Record the seed with the output, not just in the code.

A seed that lives only in a source file is lost the moment the file changes. The results it made become unreproducible without a git archaeology session. Writing it into the output. A filename, a metadata field, a log line. Costs nothing and is the gap between results that can be regenerated and results that can only be trusted.
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
intro: mat product, solving systems, and why you should almost never invert a mat.

## @ versus *

Linear algebra operations in NumPy trip people up because the notation looks almost right but means something different. The asterisk on two matrices gives elementwise multiplication. The at-sign gives matrix multiplication. Both produce valid arrays of plausible shape. Only one is the operation you intended.

Matrix multiplication has its own operator because it is fundamentally different from elementwise operations. Elementwise multiplication pairs corresponding elements and gives a result of the same shape. Matrix multiplication sums products along the inner dimension and gives a result whose shape depends on both inputs. For two (3, 3) arrays, both operations return (3, 3), but the values are entirely different.

The at-sign operator was added in Python 3.5 specifically for this purpose. Before that, you had to write np.dot or np.matmul, which are less readable in expressions with multiple terms. The three forms do the same thing for 2-D arrays. For higher dimensions, matmul and @ broadcast over batch dimensions, while dot does not.

Beyond the product, NumPy provides the common linear algebra operations in the np.linalg module. Solving a linear system is np.linalg.solve, which is faster and more numerically stable than computing the inverse and multiplying. Computing the inverse is np.linalg.inv. Determinant is np.linalg.det. Eigenvalues and eigenvectors are np.linalg.eig or np.linalg.eigh for symmetric matrices.

Checking the result of a linear algebra computation is important because floating-point arithmetic introduces rounding errors. The product of a matrix and its inverse is not exactly the identity matrix. It is close to it. np.allclose checks whether two arrays are equal within a tolerance, and it is the right way to verify such results.

This module covers the @ operator, np.dot, np.linalg.solve, inv, det, eig, and the norm function. The examples use small matrices where you can verify the result by hand. The focus is on the operations that appear in everyday data work, not on the full scope of numerical linear algebra.


`*` is elementwise. `@` is mat product.

Both are valid on two square mats of the same size. They give fully other answers. Nothing raises, nothing warns. The result of the wrong one is a plausible-looking mat of the right shape.

This is the most common linear algebra bug in NumPy code. It lives review easily because both lines look correct.

`np.matmul` is the function form of `@`. `np.dot` agrees with it for 2-D. They diverge for higher dims. `matmul` broadcasts the leading axes and treats the last two as mats, `dot` does a thing other and rarely what you want. Prefer `@` or `matmul`.

## Shapes

`(m, k) @ (k, n)` gives `(m, n)`. The inner dims must match and they cancel.

A 1-D array is special-cased: it's promoted to whichever orientation makes the product valid. Then the added dim is removed from the result. `(2,3) @ (3,)` gives `(2,)`, treating the vector as a column. `(3,) @ (3,4)` gives `(4,)`, treating it as a row.

That convenience means you rarely need to reshape vectors. It also means a shape error can come from a vector being the wrong length rather than the wrong orientation. The error message names both shapes. This Is often enough.

## Solving systems

To solve `Ax = b`, use `np.linalg.solve(A, b)`.

The obvious option, `np.linalg.inv(A) @ b`, gives the same answer on well-behaved problems and is wrong as a habit for two reasons.

**Cost.** finding an inverse is roughly the work of solving the system `n` times. `solve` factors the mat once and does one back-substitution.

**score.** The inverse adds rounding error. Then timesing by it adds more. `solve` avoids forming the inverse at all. On a well-conditioned mat the gap is small. On an ill-conditioned one it's the gap between a usable answer and noise.

The rule is simple enough to apply without thinking: if you're about to write `inv(A) @ b`, write `solve(A, b)`.

Genuine uses for `inv` exist. You need the inverse itself, for a co-var mat or an analytical derivation &mdash; but they're rarer than the code you'll see suggests.

## Is it solvable?

A singular mat has no unique answer, and `solve` raises `LinAlgError`.

The instinct is to check `det(A) == 0` first. Don't. Determinants of floating-point mats are almost never just zero. The determinant scales badly. A well-conditioned mat can have a tiny determinant simply because it's large.

`np.linalg.matrix_rank(A)` answers the question right: full rank means solvable.

`np.linalg.cond(A)` measures how much the answer amplifies input error. A rule number near 1 is great. Anything above roughly `1e10` means you shouldn't trust the low-order digits of the result, whichever method made it.

## Norms

`np.linalg.norm(v)` gives the Euclidean length of a vector. `norm(a - b)` the distance between two points.

It takes an `axis`, so `norm(X, axis=1)` gives the length of each row at once. The usual way to find distances for a whole dataset without looping.

Other norms are on hand via `ord`: `ord=1` for the sum of abs values, `ord=np.inf` for the max.

## Eigenvalues

`np.linalg.eig` works on any square mat and returns complex results in unspecified order.

For a **even** mat &mdash; which covers most cases that arise since co-var and Gram mats are even &mdash; use `eigh` or `eigvalsh`. They exploit the symmetry, are faster and more accurate. Return real eigen-vals in ascending order.

That determinism matters: code that indexes into the output of `eig` and assumes an order is leaning on a thing not sure.

## Least squares

`np.linalg.lstsq(M, y, rcond=None)` fits an overdetermined system. More equations than unknowns. By cutting squared error.

Building the design mat with `column_stack` is the whole setup. For a straight line, the columns are `x` and a column of ones. The answer is slope and intercept.

Pass `rcond=None` by name to get the current action and silence the future-warning about the old default.

## Batched matrix multiplication

`matmul` treats the **last two** axes as the mat and broadcasts all before them.

That makes `(batch, n, k) @ (batch, k, m)` a batch of mat products, found in one call with no loop. `(batch, n, k) @ (k, m)` also works, applying the same mat to each item in the batch.

This is why the batch axis goes first by rule. It puts the mat axes where `matmul` expects them. The whole thing composes without transposes.

`np.dot` doesn't do this. On arrays with more than two dims it follows an older rule that is rarely what anyone wants. `@` and `matmul` are the ones to use.

Most of `np.linalg` also broadcasts over leading axes: `solve`, `inv`, `det` and the breakdowns all accept a stack of mats and return a stack of results.

## solve versus lstsq

`solve` needs a square mat and gives the exact answer when one exists. It raises on a singular mat.

`lstsq` handles rectangular systems and finds the answer cutting squared error. It also handles rank-deficient systems by returning the min-norm answer rather than raising.

For an overdetermined system &mdash; more equations than unknowns. This Is what fitting a model to data looks like &mdash; `lstsq` is the right tool.

The tempting option is the normal equations: `solve(A.T @ A, A.T @ b)`. It gives the same answer in exact math and is by number worse. Forming `A.T @ A` squares the rule number. A problem that was marginally conditioned turns badly conditioned. `lstsq` uses an SVD-based approach that avoids this.

## SVD, and what it is for

`np.linalg.svd` factors any mat into `U @ diag(s) @ Vt`.

The singular values `s` are the handy part for most hands-on purposes.

**Rank.** The number of singular values usefully above zero. This is what `matrix_rank` finds inside. It's why rank is a more solid singularity test than a determinant.

**Conditioning.** The ratio of largest to smallest singular value is the rule number.

**Dimensionality reduction.** Keeping the largest k singular values and their vectors gives the best rank-k guess of the mat. That is what PCA is. Truncated SVD is how it's found.

**Pseudo-inverse.** `np.linalg.pinv` uses SVD to invert what can be inverted and skip what can't. This Is how least squares handles rank deficiency.

`svd(a, full_matrices=False)` returns the economy version. This Is smaller and often what you want for a tall mat.

## Other decompositions

`np.linalg.qr` factors into an perp and an upper-tri mat. It's the by number sound way to solve least squares by hand. It's what many methods use inside.

`np.linalg.cholesky` factors a even plus-definite mat into a lower tri factor times its transpose. It's roughly twice as fast as a general split and is the standard tool for co-var mats. Sampling from a multivariate normal, or checking a Gaussian likelihood.

Cholesky **raises** if the mat isn't positive definite. This Is a handy diagnostic in itself. A co-var mat that fails Cholesky is telling you a thing is wrong with how it was guessed.

## Conditioning in practice

The rule number is the amplification factor from input error to output error.

A rule number of 10 means roughly one decimal digit lost. `1e8` means about eight. This On `float64`'s sixteen leaves eight. `1e16` means all of them. The answer is noise even so of the method.

Two things follow.

**Check `cond` before trusting a answer** from a mat built out of measured data. Nothing warns you.

**Ill-conditioning is a property of the problem, not the code.** No solver rescues a rule number of `1e16`. The fix is upstream. Rescale vars so their magnitudes are close, drop collinear columns, or add fine. Which is just what ridge regression does, and why it works.

Scaling is the most often overlooked of those. A design mat with one column in metres and another in nanometres is badly conditioned for no reason other than units.

## What to reach for

**`@`** for products, including batched.

**`solve`** for square systems, never `inv`.

**`lstsq`** for fitting and overdetermined systems, never the normal equations.

**`eigvalsh` / `eigh`** for even mats. `eig` returns complex values in unspecified order.

**`cholesky`** for co-var mats.

**`svd`** when you need rank, conditioning, or a low-rank guess.

**`cond` and `matrix_rank`** before believing any of it.

And for anything beyond this. Sparse mats, iterative solvers, specialised breakdowns &mdash; SciPy's `scipy.linalg` and `scipy.sparse` extend the same interface and are where the rest of the toolkit lives.

## Common mistakes

**Using `*` where `@` was meant.** Both are legal on square mats and give other answers of the same shape. Nothing warns. This is the most frequent linear algebra bug in NumPy code.

**Writing `inv(A) @ b`.** Slower and less accurate than `solve(A, b)`, for no gain.

**Using the normal equations for least squares.** `solve(A.T @ A, A.T @ b)` squares the rule number. `lstsq` doesn't.

**Testing `det(A) == 0`.** Floating-point determinants are almost never just zero. The determinant scales with the mat. `matrix_rank` answers the question right.

**Indexing into `eig` output given an order.** There's none. `eigh` and `eigvalsh` return ascending real values for even mats. This Is what most code really needs.

**Expecting `.T` to make a column vector.** On a 1-D array it does nothing. `v[:, None]`.

**Using `np.dot` on more than two dims.** It follows an older rule that is rarely what anyone wants. `@` or `matmul` broadcast the leading axes properly.

## Reading the shapes in an error

`matmul` errors name the "core dims". This Are the last two axes.

"Input operand 1 has a mismatch in its core dim 0" means the first of the last two axes of the second operand doesn't match what the first operand's last axis needs. The `k` in `(m,k) @ (k,n)`.

The diagnosis is to print both shapes and check which axis is supposed to be shared. Nearly always one of the two arrays is transposed scaled to the intent. The fix is a `.T` on the correct side rather than a reshape.

For a 1-D operand, note it's promoted to whichever orientation makes the product valid. A shape error involving one often means the wrong length rather than the wrong orientation.

## Questions people ask

<strong>What is the difference between * and @?</strong> The star multiplies element by element. The @ operator is matrix multiplication, which is the one you want for linear algebra.

<strong>Should I use np.linalg.inv to solve Ax = b?</strong> No. Use np.linalg.solve(A, b), which is faster and more accurate than forming the inverse and multiplying.

<strong>How do I check whether a matrix is singular?</strong> Look at np.linalg.matrix_rank or the condition number from np.linalg.cond. A determinant near zero is a weaker test because it depends on scale.

<strong>What do eig and eigh differ in?</strong> eigh is for symmetric or Hermitian matrices. It is faster, returns real eigenvalues in ascending order, and is the right choice for covariance matrices.

<strong>How do I fit a least-squares line?</strong> Use np.linalg.lstsq(A, y, rcond=None). It handles non-square and rank-deficient systems that solve cannot.

<strong>What does np.dot do compared with @?</strong> For 1D and 2D arrays they agree. For higher dimensions they differ, and matmul (@) broadcasts over leading axes, which is usually what you want.

## Where SciPy takes over

`np.linalg` covers the dense, general cases well. a few things sit just outside it.

**Sparse mats.** `scipy.sparse` stores only nonzeros and has its own solvers. For a mat that is mostly zeros. Graphs, finite-element meshes, term-doc mats. The gap isn't a constant factor but the gap between fitting in memory and not.

**Iterative solvers.** For very large systems, `scipy.sparse.linalg` offers methods that rough a answer without factoring the mat.

**More breakdowns.** `scipy.linalg` has LU, Schur, banded and tri solvers. Often more options on the ones NumPy also gives.

**mat functions.** `expm` for the mat steep and friends live in SciPy.

The interfaces are on purpose similar. Moving across is often a change of import rather than a change of approach.
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
intro: The value that isn't equal to itself. The functions that exist because of it.

## Not equal to itself

NaN is a floating-point value defined by the IEEE 754 standard. Its defining property is that every comparison involving NaN returns False, including equality with itself. That property is not a NumPy design choice. It is a rule built into the hardware.

The consequence is that the usual ways of checking for a value do not work. a == np.nan is False even when a is NaN. The in keyword does not find NaN in a list reliably. The only correct way to test for NaN is np.isnan, which was designed to handle the special case. pandas wraps this in pd.isna, which also handles None and pd.NA.

NaN propagates through arithmetic. Any operation that touches a NaN produces NaN. The sum of a thousand numbers plus one NaN is NaN. The mean of a clean dataset with one corrupted entry is NaN. That propagation is a safety feature. It ensures that missing data does not silently disappear from the result. But it also means that a single NaN in a large array can make the entire result useless.

NumPy provides nan-aware aggregation functions for exactly this reason. np.nansum ignores NaN values and sums the rest. np.nanmean computes the mean of the non-NaN values. np.nanstd, np.nanmin, np.nanmax do the same for their respective statistics. The regular versions propagate NaN. The nan-aware versions skip it. Choosing between them depends on whether you want missing data to be loud or quiet.

NaN is a float. Integer arrays cannot hold NaN. If you need missing values in an integer array, you must either use a float dtype and accept the type change, or use a masked array, or use pandas nullable integer types. That limitation is the reason why a pandas integer column with one missing value turns into float64.

This module covers NaN arithmetic, detection with np.isnan, the nan-aware aggregation functions, and the practical consequences for integer and boolean arrays. It also covers np.inf, which behaves differently from NaN in comparisons and arithmetic.


`np.nan` is a floating-point value defined by the IEEE 754 standard to represent "not a number". Its defining property is that **each compare involving it's False**, including equality with itself.

`nan == nan` is False. `nan < 1` is False. `nan > 1` is False. The only compare that returns True is `!=`. Only because it's the negation of a False.

The direct hands-on result: `arr == np.nan` gives an all-False mask, no matter how many NaNs the array holds. It fails silently. This Is the worst way to fail.

`np.isnan(arr)` is the correct test, and it returns a proper boolean mask.

The rule isn't a NumPy quirk. It falls out of NaN meaning "the result of an undefined step". Two undefined results have no reason to be the same thing.

## NaN is a float

There's no int NaN. The int types have no bit pattern reserved for it.

So assigning `np.nan` into an int array raises. Any array literal holding `np.nan` comes out as float.

This is why a table column with one missing value silently turns float. Why identifiers end up displayed as `1001.0` instead of `1001`. There's no way around it within a plain NumPy int array. The options are to accept float, to use a sentinel value like `-1` and doc it, or to carry a split boolean mask alongside the data.

Pandas handles this with nullable int types. Plain NumPy doesn't have them.

## One NaN poisons everything

`a.sum()` on an array holding a single NaN returns NaN. So does `mean`, `max`, `min`, `std` and every other reduction.

This is correct &mdash; the sum truly is unknown &mdash; but it's dangerous. The result is still a number-shaped thing that flows onward through the pipeline and turns all downstream into NaN too. By the time you notice, the origin can be far away.

The `nan*` family exists for this: `nansum`, `nanmean`, `nanmax`, `nanmin`, `nanstd`, `nanmedian`, `nanpercentile`. Each skips missing values rather than passing them.

Note what `nanmean` does: it cuts by the count of **real** values. On four elements with one NaN, it cuts by three. That is often right. It's worth being clear that it's a choice rather than a detail. You're asserting that the missing value is missing at random.

`nansum` of an all-NaN array returns 0, while `nanmean` of one returns NaN with a warning. Those are other and defensible choices. Both are worth knowing before you lean on either.

## Finding them

`np.isnan(a)` gives a mask, and all from the masking module applies.

`np.isnan(a).sum()` counts them. With `axis`, it counts per row or per column. This Is the first thing to look at when data arrives.

`np.isnan(a).any(axis=1)` flags rows holding any missing value. `~` inverts it to keep the full ones. That is listwise deletion in one line.

`np.where(np.isnan(a))` gives the coords. This Is what you want when you need to know *where* rather than *how many*.

## Filling

Three broad plans, and the choice is a statistical choice rather than a coding one.

**Drop.** `a[~np.isnan(a)]` for a vector, or the row-wise version above for a table. Simple and unbiased if the data really is missing at random. Throws away maybe a lot if it isn't.

**Constant.** `np.nan_to_num(a)` replaces with zero. `np.where(np.isnan(a), value, a)` with anything else. Filling with zero shifts the mean. Filling with the mean preserves the mean but shrinks the variance. This Quietly misleads anything downstream that cares about spread.

**Interpolate.** `np.interp` fills from neighbouring values. This Is the right choice for sorted data like a time series where adjacency is real.

None of these is neutral. each one of them puts numbers into your data that weren't measured. The honest thing is to record which you used.

## inf is different

Cutting by zero doesn't raise in NumPy. It makes `inf`, `-inf` or `nan`, and emits a RuntimeWarning.

`1/0` gives `inf`. `0/0` gives `nan`. They come from other failures and are worth distinguishing.

`np.isnan` doesn't catch `inf`. `np.isinf` doesn't catch NaN. `np.isfinite` catches both. Is often the check you really want when checking data.

`np.errstate` is the context manager for suppressing the warnings when the action is intentional. `np.nan_to_num` replaces NaN and both infinities in one call, with split args for each.

## Three ways to represent missing, and their costs

**NaN.** Works only for floats. Passes on its own through math. This Is both the safety feature and the hazard. Supported by the whole `nan*` family and understood by each library.

**A sentinel value.** `-1` for a count, `-999` for a reading. Works for ints, costs nothing. Is fully a rule. Nothing stops the sentinel being treated as data by code that doesn't know about it. each such bug is silent and makes plausible numbers.

**A split boolean mask.** clear, works for any dtype. Never gets mistaken for data. Costs a byte per element and needs each step to be written mask-aware. This Is the reason it isn't more common.

`np.ma` packages the third option, and pandas' nullable dtypes package a version of it with better ergonomics.

For plain NumPy, NaN is the default answer for floats. A documented sentinel is the pragmatic answer for ints when converting to float isn't acceptable. The key part is documenting it. A sentinel that isn't written down anywhere is a bug waiting for a new maintainer.

## Comparing arrays that contain NaN

`np.array_equal(a, b)` returns False if either holds NaN. NaN never equals anything. Including the NaN in the same spot of the other array.

That makes it useless for checking that a math copied a result. This Is just when you want it.

`np.array_equal(a, b, equal_nan=True)` treats NaNs in matching spots as equal.

`np.allclose(a, b, equal_nan=True)` does the same with a handling. Is what belongs in a test checking floating-point results.

Both are worth reaching for by default in test code. A NaN appearing in both arrays is often the expected outcome rather than a failure.

## NaN in sorting and extremes

`np.sort` places NaN at the **end**, on the grounds that it checks greater than all. That is a rule rather than a result. NaN checks are all False.

`np.argmax` and `np.max` return NaN if any element is NaN. This Is steady with the reductions but means a single missing value hides the real max. `np.nanargmax` and `np.nanmax` skip them.

`np.nanargmax` **raises** on an all-NaN slice rather than returning a thing meaningless. This Is the right action and worth catching in code that reduces over groups that might be fully missing.

`np.median` passes NaN. `np.nanmedian` doesn't.

The pattern is steady: the plain function passes, the `nan` version skips. The `nan` version has an view about the all-missing case.

## Tracking a NaN back to its source

The hard part of NaN debugging is that the value flows a long way from where it was created.

The single most good tool is `np.errstate(all="raise")`. This Converts the step that *makes* an invalid result into an exception. The traceback then points at the division by zero or the square root of a minus number, rather than at the reduction three functions later that returned NaN.

Failing that, bisect: check `np.isfinite(x).all()` at a few points in the pipeline and narrow down where it first goes false.

The usual origins are worth knowing. One of them is almost always it. Division by zero, `log` of zero or a minus, `sqrt` of a minus, `0 * inf`, `inf - inf`. An out-of-domain trigonometric inverse where a value drifted just past 1 through rounding. That last one is a classic. A cosine likeness found as 1.0000000002 and passed to `arccos` gives NaN. `np.clip(x, -1, 1)` is the fix.

## Deciding what to do about missing data

The code is easy. The choice isn't. It's a choice about the data rather than about NumPy.

**Why is it missing?** Missing at random can be dropped or imputed without bias. Missing because of the value itself. A sensor that fails at extremes, a survey question people skip when the answer is embarrassing. Can't. Dropping those rows biases the result. Imputing them with a mean biases it differently.

**How much is missing?** A handful of rows out of a hundred thousand can be dropped without much thought. Thirty percent can't. The choice of imputation turns a modelling choice that should be stated.

**What does downstream care about?** A mean is solid to mean-imputation by build. A variance isn't. Filling with the mean shrinks it. Anything leaning on spread will be quietly wrong.

**Is the missingness itself helpful?** Often it's. Adding a boolean "was missing" column preserves that data rather than discarding it.

what you choose, count them first and record what you did. `np.isnan(a).sum(axis=0)` at the point data arrives takes one line and blocks a surprising number of downstream mysteries.

## Validating data as it arrives

The cheapest defence against NaN problems is checking at the boundary. Here The data enters the program.

`np.isfinite(a).all()` answers "is any of this NaN or infinite" in one call. Is the right single check because it catches both.

`np.isnan(a).sum(axis=0)` gives the count per column. This Turns "there's missing data one spot" into "column 3 is 40% empty". A far more actionable statement.

Doing this at load time, and failing or logging rather than proceeding silently, converts a class of mysterious downstream results into an direct, located error. It costs one line.

## NaN and boolean logic

`np.isnan` needs a float dtype. Calling it on an int or string array raises a TypeError rather than returning all-False. This Surprises people writing plain code.

`np.isnan(a)` on an **object** array also fails. The elements may not be numbers at all.

For code that must handle any dtype, guard with `np.issubdtype(a.dtype, np.floating)` first, or use `pd.isna` from pandas. This Handles each case including None and NaT.

## Comparisons involving NaN, in filtering

Because each compare with NaN is False, NaN values fail each rule. Including the negation of a rule.

`a[a > 0]` excludes them. `a[a <= 0]` also excludes them. Two filters that look like an exhaustive split silently drop rows.

Any place where a dataset is split into groups by a numeric rule is a place to ask what happens to the missing values. To add an clear `np.isnan` branch if they should be handled rather than lost.

## Questions people ask

<strong>Why does np.nan == np.nan return False?</strong> NaN is defined as unequal to everything, itself included. Test with np.isnan(x) instead of comparing.

<strong>How do I ignore NaN in a mean?</strong> Use np.nanmean, or the other nan-prefixed reductions such as nansum, nanstd and nanmax.

<strong>Can an integer array hold NaN?</strong> No. NaN is a float, so an integer array cannot represent it. Convert to float, or use a masked array.

<strong>How do I replace NaN with a value?</strong> Use np.nan_to_num(a, nan=0.0), or a[np.isnan(a)] = value. Pick the fill with care, since zero changes the mean.

<strong>What is the difference between nan and inf?</strong> NaN means the value is undefined, such as 0 divided by 0. Inf is an overflow or a divide by a nonzero zero, and it behaves consistently in comparisons.

<strong>Are masked arrays better than NaN?</strong> They suit data where NaN is a valid value or the dtype is integer. For plain float data, NaN with the nan-functions is simpler and quicker.

## The summary

`np.isnan` to find them, never `== np.nan`.

`np.isfinite` to validate, because it catches infinities too.

The `nan*` family to reduce over them, remembering that skipping is a choice about the data.

`np.errstate(all="raise")` to find where one was created. This Is the single most good debugging tool here.

`equal_nan=True` on `allclose` and `array_equal` when checking results that legitimately hold them.

`np.clip` before `arccos` and similar, to stop rounding drift making NaN from valid data.

And at the start of all: count them, record what you did about them. Prefer being clear over letting a fill value pass silently into an analysis that assumes it was measured.
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
intro: Where the time and the bytes really go.

## The order to try things

Performance tuning in NumPy follows a predictable order, and the biggest gains come from the simplest changes. The most expensive mistake is to optimise the wrong thing first.

The first question is whether there is still a Python loop. A for-loop over array elements drops from compiled code into the Python interpreter, which is roughly a hundred times slower. Replacing the loop with a vectorised operation gives you that factor back. Most NumPy performance problems are this problem, and most people skip it to look for fancier solutions.

The second question is dtype width. An array of small integers stored as int64 uses eight times the memory of int8. An array of moderate floats stored as float64 uses twice the memory of float32. Smaller dtypes mean more elements fit in CPU cache at once, and that speeds up every operation that touches the array. The speedup is typically 1.5x to 2x, on top of the memory savings.

The third question is memory layout. Operations that walk through contiguous memory are faster than operations that jump around. A transposed array or a column slice of a C-contiguous array is not contiguous along the access direction. Making a contiguous copy with np.ascontiguousarray before a tight loop can help, but only if the loop is long enough to repay the copy.

The fourth question is temporary arrays. An expression like a * b + c creates a temporary array for a * b, then creates another for the addition. For large arrays, those temporaries cost time and memory. np.multiply(a, b, out=result) reuses an existing array and avoids the allocation. numexpr can fuse the whole expression into one pass.

The fifth and last question is whether NumPy is the right tool. For very large data that does not fit in memory, memory-mapped arrays or chunked processing help. For operations that are hard to vectorise, writing a small C or Cython extension, or using Numba's JIT compiler, can close the gap.

This module works through the list in order, with timing measurements that show the payoff of each step. The point is not just what to do, but what to do first.


Most NumPy speed work comes down to four questions, roughly in order of payoff:

1. Is there still a Python loop? Dropping it's worth 10&ndash;100x.
2. Is the dtype larger than it needs to be? Halving it's worth up to 2x, and halves memory.
3. Are temporaries being allocated in a hot path? In-place steps drop them.
4. Is the memory access pattern fighting the cache? Layout changes can be worth 2&ndash;5x.

The first is covered in the introductory module and dwarfs the rest. This module is about the other three. This Matter once the obvious loop is gone.

## dtype

`float64` is the default and is often more precision than the data justifies. Sensor readings good to three large figures don't gain from fifteen.

`float32` keeps about seven large digits, halves the memory. Often runs faster. Not because the math is cheaper. Because half as much data has to travel from memory to the processor, and memory bandwidth is often the limit.

The same applies to ints. An array of small counts doesn't need `int64`. An array of flags should be `bool_`. This Is one byte, not `int64`, which is eight.

The caution from the dtypes module still applies. Narrow ints overflow silently. Choose the smallest type that can't overflow for your actual data, not the smallest that happens to fit today's sample.

## Temporaries

`a * 2 + 1` on a million-element array doesn't do one pass. It allocates an 8 MB temporary for `a * 2`, then allocates another 8 MB for the final result, then frees the first.

You never see them, and for a single formula it rarely matters. In a loop, or in a chain of five steps on a large array, the allocation and the extra memory traffic dominate.

Two ways to avoid it.

**In-place ops.** `a *= 2` modifies the existing buffer and allocates nothing. note that it also modifies anything sharing that buffer. This Is the views-versus-copies problem again.

**`out=`.** each ufunc accepts `out`. This Names the destination by name. `np.times(a, 3, out=dest)` writes into `dest`. `out` may be one of the inputs. This is the clearest form when you're building up into a buffer across loops.

Neither is worth doing all over. `a * 2 + 1` is more readable than two statements. Readability wins until you've measured that this line matters.

## Layout and the cache

A C-sorted array stores the **last** axis contiguously. in a row elements along that axis sit next to each other in memory.

Processors fetch memory in cache lines. Reading in a row bytes is far cheaper than jumping a row at a time.

Reductions are a poor demo of this. NumPy blocks them inside. `sum(axis=0)` and `sum(axis=1)` often run at similar speed and at times in the order you wouldn't predict. It's worth knowing that. The "always reduce along the last axis" advice is repeated widely and doesn't live reading.

Where it shows clearly is when data is really **moved**. Copying a `(1200, 1200)` array and copying its transpose move the same number of bytes and give the same number of bytes. The transpose reads one value from each row in turn. Runs a few times slower.

Two hands-on results. If you've a choice about which axis holds the thing you iterate over, put it last. And if you're about to make many strided passes over the same data, one `np.ascontiguousarray` up front can pay for itself. A single copy against many slow reads.

## Preallocation

`np.append` and `np.concatenate` don't append. They allocate a new array and copy all. In a loop that is quadratic. It's the single most common accidental slowdown in NumPy code after the plain Python loop.

If you know the final size, `np.empty(n)` and set by index is the direct answer. `np.empty` doesn't reset. It's faster than `np.zeros` when you're going to overwrite all. And dangerous if you aren't. The contents are what was in that memory.

If you don't know the size, collect into a Python list and convert once at the end. Lists are designed for growth. Arrays aren't.

## Measuring

Guessing is unreliable, and the intuitions transferred from pure Python are often wrong.

`a.nbytes` gives the real size of the data. `a.itemsize` gives the per-element cost.

For time, run the step a few times and take the **min**, not the mean. The slow runs are measuring interference from the rest of the machine. The fastest run is the closest guess of the actual cost. A single timed run of a fast step measures mostly noise.

And measure the thing you intend to change. Optimising an step that accounts for 2% of the runtime is effort spent for a 2% ceiling. Meeting the local speedup looks.

## Views and memory that will not go away

A view holds a link to the array it came from. The entire base buffer stays alive if the view does.

Extract one row from an 8 MB array, keep it, and you're keeping 8 MB.

This is the most common source of NumPy memory that never comes back. It's invisible. `row.nbytes` reports four kilobytes while the process holds eight megabytes.

The fix is `copy()` at the point you decide to keep a thing small from a thing large. The cost is one small allocation. The saving is the whole base.

`a.base` shows what a view derives from. `a.base.nbytes` shows what is really being held. That is the diagnostic when memory in a long-running process grows without an obvious cause.

## Threads and the GIL

NumPy releases the GIL during most array steps. This Means threads truly run in parallel inside a NumPy math. Unlike most pure Python code.

That makes `concurrent.futures.ThreadPoolExecutor` a real option for parallelising array work, with none of the pickling and process-startup costs of multiprocessing.

Two caveats. steps that touch Python objects. Object arrays, anything calling back into Python. Don't release it. And BLAS routines are often already multi-threaded inside. Adding your own threads on top can oversubscribe the machine and run slower. `OMP_NUM_THREADS` and `threadpoolctl` control that layer.

Measure before given threading helps. For large mat steps it often does nothing. BLAS was already using each core.

## Chunking

When an step would allocate more than fits in memory, the answer is often to do it in pieces.

The classic case is a pairwise distance mat. For 100,000 points, the mid is 10 billion entries and no machine will hold it. handling 1,000 rows at a time keeps the mid at 100 million and gives the same answer.

The general shape:

```python
for start in range(0, n, chunk):
    block = data[start:start + chunk]
    out[start:start + chunk] = expensive(block)
```

The slices are views, so the chunking itself allocates nothing. The output is preallocated once.

This is one of the cases where a loop is correct. The loop runs `n / chunk` times, not `n` times. The interpreter cost is negligible and the memory ceiling is the thing being controlled.

## When to reach past NumPy

NumPy has a ceiling, and recognising it saves effort spent optimising against it.

**Numba** compiles a Python function to machine code with a decorator. It's the right answer for truly sequential methods. The ones that can't be vectorised. And often gets within range of C for a few lines of change.

**Cython** gives more control at the cost of a build step. Is what a few scientific libraries use inside.

**SciPy** already holds a compiled setup of a great many things people write by hand. Distance mats, sparse mats, signal filters, tuning, blending. Checking whether SciPy has it's cheaper than writing it.

**Dask** handles arrays larger than memory with a NumPy-like interface, splitting work into chunks on its own.

**CuPy / PyTorch** move the work to a GPU, with an interface close enough to NumPy that porting is often rote. Worth it for large array workloads, not worth it for small ones where the transfer cost dominates.

The order to consider them: is it vectorisable in NumPy, is it in SciPy, is it sequential and worth Numba, is it too big for memory, is it big enough for a GPU.

## Profiling before optimising

The instinct about where time goes is unreliable, and array code is no exception.

`cProfile` gives function-level timings and finds the hot function. `line_profiler` gives per-line timings within it. This Is what you really need when one function holds the whole math.

`memory_profiler` tracks allocation line by line. `a.nbytes` summed over the arrays you're holding is a quick manual version.

Two rules make profiling worth the time.

**Profile the real workload.** A toy input can have fully other traits. Other cache action, other branch of the method, other memory pressure.

**Fix the top item, then measure again.** The bottleneck moves. Optimising the second item on the first list is often wasted. After the first fix it's no longer second.

And keep the ceiling in view: a function taking 5% of runtime can't give more than a 5% gain but fully you optimise it.

## Where the wins actually are, in order

**Drop the Python loop.** 10&ndash;100x, and it dominates all else. If a loop over elements is still there, nothing below this line matters yet.

**Avoid quadratic growth.** `np.append` or `concatenate` in a loop turns a linear job into a quadratic one. The fix is preallocation or a list.

**Right-size the dtype.** Up to 2x on bandwidth-bound work, and it halves memory.

**Drop temporaries in hot paths.** In-place ops and `out=`. Worth doing where reading says it matters, not all over.

**Fix access patterns.** Contiguity, and avoiding repeated strided gathers.

**Reach past NumPy.** Numba, SciPy, a GPU. When the method truly doesn't vectorise or the data truly doesn't fit.

Working down that list in order means the large wins come first. It avoids the common trap of micro-optimising an formula inside a loop that shouldn't exist.

## Things that look slow and are not

**Slicing.** A view. Free, what the array size.

**Transposing.** A view. Free.

**Reshaping a contiguous array.** A view. Free.

**Reversing with `[::-1]`.** A view. Free.

**Broadcasting the inputs.** No allocation. The strides are set to zero. The *output* is allocated. This Is a other thing.

Rewriting any of these to "avoid the copy" is effort spent on a copy that was never happening. Confirm with `np.shares_memory` before optimising a thing that may already be free.

## Things that look cheap and are not

**Boolean masking and fancy indexing.** Both allocate, and both gather from scattered spots.

**`astype`.** Allocates a full second array, even when the dtype is unchanged, unless `copy=False`.

**Chained expressions on large arrays.** each mid is a full-size allocation.

**`np.append`.** Not an append. A full copy, each call.

**Keeping a small view of a large array.** Holds the whole base alive.

## The discipline

Measure before optimising, and profile the real workload rather than a small stand-in. Cache action and memory pressure don't scale down predictably.

Take the min of a few timed runs, not the mean.

Fix the top item and measure again, because the bottleneck moves.

Keep the ceiling in view: an step taking 5% of the runtime can't yield more than 5%. Thoroughly it's optimised.

And weigh readability honestly. A vectorised one-liner that no one can safely modify has a maintenance cost that doesn't show up in a benchmark. The version a colleague can read is often the better engineering answer even when it's slower.

## Questions people ask

<strong>Why is a NumPy loop so much faster than a Python loop?</strong> The loop runs in compiled C over contiguous memory, with no per-element Python object overhead or type checks.

<strong>How much memory does an array use?</strong> Read a.nbytes, which is the element count times the item size. The shape and dtype fields add only a small fixed overhead.

<strong>How do I avoid temporary arrays?</strong> Use in-place operators like a += b, or the out= argument on ufuncs. Chained expressions each allocate an intermediate array.

<strong>Does memory layout matter?</strong> Yes. Walking along the contiguous axis is faster because of CPU caching. In a C-ordered array that means iterating over the last axis.

<strong>When should I use float32?</strong> When memory or bandwidth is the limit and you can accept about seven digits of precision. It halves the footprint and often speeds up big operations.

<strong>How do I time code properly?</strong> Use timeit or %timeit, which repeats the run and takes the best result. A single time.time() measurement is noisy.

## The lock behind two of these timings

Some of the numbers above only make sense in the presence of the interpreter lock. It deserves a sentence rather than a hand-wave. CPython holds one lock around bytecode run. Two Python-level threads never execute Python also. But a NumPy call that spends its time in C can *release* that lock while it works. This Is why a large `dot` or a big elementwise step shares across threads and a Python loop over the same array doesn't.

So the vectorised version isn't merely faster. It's differently parallel. That is a property of where the time is spent rather than of NumPy's API.

<ul><li><a href="../concurrency/the_gil_and_what_it_locks.html">The GIL, and what it really locks</a>. Measured. Threads share waiting and don't share finding, and what "releases the GIL" means at the C boundary.</li><li><a href="../concurrency/threads_or_processes.html">Threads or processes: what is and isn't shared</a>. And the cost of moving an array across a process boundary. This For a large array can exceed the work you were trying to parallelise.</li><li><a href="../concurrency/choosing_threads_processes_or_async.html">Choosing threads, processes, or async</a>. The choice with the cases stated rather than implied.</li></ul>
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

NumPy arrays need to be saved to disk and loaded back frequently. Intermediate results, preprocessed datasets, trained model weights, and test fixtures all need persistent storage. NumPy provides its own binary format and also supports text formats for interoperability.

The native format is the .npy file. np.save writes a short header with the dtype, shape, and byte order, followed by the raw bytes of the array. np.load reads it back. The round trip is lossless. The dtype and shape are preserved exactly. An int16 array comes back as int16, not as int64. A (3, 4, 5) array comes back with the same shape. There is no parsing cost because the file is just the bytes.

For multiple arrays, np.savez writes a .npz file, which is a zip archive of .npy files. Each array is stored under a name. np.savez_compressed applies compression, which helps when the data has patterns that compress well, like arrays with many repeated values or many zeros.

Text formats are useful for interoperability with tools that cannot read .npy files. np.savetxt writes a CSV-like format. np.loadtxt reads it back. The round trip is not lossless. Floating-point values are written as text and parsed back, which can change the last decimal digit. Integer arrays come back as floats unless you specify the dtype. Text files are also much larger and much slower to read and write than binary ones.

The choice between formats depends on who will read the file. If the reader is another Python script, .npy is better in every way. If the reader is R, Julia, or a spreadsheet, text or a more portable binary format like HDF5 is necessary. If the file will be version-controlled, text diffs better but takes more space.

np.load with allow_pickle=False is a security consideration. Pickle files can execute arbitrary code on load. The default in current NumPy versions already disables pickle, but older code may not. Never load an untrusted .npy file with allow_pickle=True.

This module covers np.save, np.load, np.savez, np.savetxt, np.loadtxt, and the trade-offs between binary and text formats. The examples show round-trip preservation and the pitfalls of text serialisation.


`np.save(path, a)` writes a `.npy` file: a short header showing dtype, shape and byte order, followed by the raw bytes.

`np.load(path)` reads it back the same way. Dtype and shape live, `int16` comes back as `int16`. There's no parsing cost because there's nothing to parse.

It's the right default for anything that only needs to be read by NumPy. Files are compact, writing and reading are fast, and nothing is lost.

The extension is added on its own if you omit it.

## Bundles

`np.savez(path, train=X, labels=y)` writes an `.npz`. A zip archive of `.npy` files, one per keyword arg.

Loading gives a dict-like object. Arrays are read **lazily**, only when you index a key. Opening a large bundle to read one array doesn't load the rest.

It holds an open file handle. Use it as a context manager or call `close()`. Losing is a common source of file handles leaking in long-running code.

`np.savez_compressed` applies deflate. Whether that helps depends fully on the data. Zeros and repeated structure compress sharply. Floating-point reading noise barely compresses at all. It costs CPU on both ends. It's worth measuring on your own data rather than given.

## Text

`np.savetxt` and `np.loadtxt` handle CSV and similar.

They're the right choice when a thing other than NumPy must read the file. A spreadsheet, a colleague, a other language.

They're the wrong choice else, for three reasons. Files are a few times larger. Parsing is far slower than reading raw bytes. And **the dtype is lost**. All comes back as `float64`, what went in. An `int8` array round-trips into `float64`.

`fmt` controls precision on write, and `%.4f` will silently truncate values you cared about. `header` with `comments=""` writes a plain header line rather than a commented one.

## allow_pickle

This is the security-relevant part.

Object arrays &mdash; arrays with `dtype=object`, holding any Python objects &mdash; can't be written as raw bytes. NumPy pickles them instead.

Unpickling **runs code**. A malicious `.npy` file can run anything when loaded.

So `np.load` has `allow_pickle=False` by default and raises rather than loading an object array. That default is a deliberate protection, added after the risk became a hands-on problem.

Enable it only for files you created yourself, or received through a channel you trust as much as you'd trust an executable. "It's just data" is just the assumption the attack leans on.

Better still, avoid object arrays in saved data. If a structure won't fit in a plain numeric array, a format designed for structured data. JSON, HDF5, Parquet. Is a better answer than pickling.

## Messy input

`loadtxt` is strict and raises on a missing field. That strictness is a feature when the data should be full.

`genfromtxt` is the tolerant version. Missing values become `nan` by default, or what `filling_values` gives. It also handles column names, per-column dtypes and skipping footers.

It's slower, and for truly messy tabular data, pandas' `read_csv` is faster and more capable. `genfromtxt` fits the middle ground. Mostly clean numeric data with occasional gaps. Here Adding pandas would be more dependency than the problem justifies.

## Memory mapping

`np.load(path, mmap_mode="r")` returns an array backed by the file rather than by memory.

Slicing it reads only the pages touched. You can work with a file larger than RAM. The operating system handles caching.

`"r"` is read-only. `"r+"` allows writing back into the file. `np.array(mm)` materialises the whole thing when you do want it in memory.

The limitation is that it only helps for access patterns that touch part of the data. A full reduction reads all anyway. Does so with more cost than a straight load.

## Choosing

NumPy-only, one array: `.npy`.

NumPy-only, a few arrays: `.npz`, compressed if the data has structure.

Anything else must read it: text, accepting the size and the dtype loss.

Larger than memory, partial access: `mmap_mode`.

truly large or shared across languages and tools. Reach past NumPy to HDF5 or Parquet. This Handle chunking, packing and metadata properly.

And whichever you choose, don't enable `allow_pickle` on input you didn't give.

## Byte order and portability

A `.npy` file records the byte order of the data it holds. A file written on a big-endian machine loads right on a little-endian one. NumPy handles the swap.

You'll see this in dtype strings: `<i4` is little-endian 32-bit int, `>i4` big-endian, `=i4` native.

It matters when reading raw binary from an external source. A network protocol, an instrument, a file format defined elsewhere. Where the byte order is part of the specification and NumPy has no header to tell it. Getting it wrong makes numbers that are wrong in a distinctive way: plausible magnitudes, nonsense values.

`a.byteswap()` swaps the bytes in place. `a.astype(a.dtype.newbyteorder())` makes a converted copy.

## tofile and fromfile, and why to avoid them

`a.tofile(path)` writes the raw bytes with **no header at all**. `np.fromfile(path, dtype=...)` reads them back.

That means the file records neither the shape nor the dtype. Reading it needs knowing both in advance, from one spot outside the file. Get the dtype wrong and you get garbage rather than an error. Get the shape wrong and you get a reshape failure or, worse, a plausible wrong shape.

They exist for interoperating with programs that expect raw binary. For that they're correct. As a storage format for your own data they're strictly worse than `.npy`. This Adds a hundred-odd bytes of header and drops the entire class of problem.

If you meet a `tofile` in existing code, it's worth checking whether the shape and dtype are documented anywhere. That docs is the only thing making the file readable.

## Structured dtypes for records

When the data is truly tabular. Mixed types per column. A structured dtype keeps it in one array:

```python
dt = np.dtype([("name", "U20"), ("age", "i4"), ("score", "f8")])
people = np.array([("ana", 31, 8.5)], dtype=dt)
```

Fields are accessed by name: `people["age"]`. The result is a view. Assigning into it modifies the first.

Structured arrays save and load through `.npy` without pickling. This Is their main edge over an object array. The data stays plain bytes.

They also sort by field name with `order=`. This Is the closest NumPy comes to sorting a table by columns.

The honest caveat: for anything with more than a few columns or any real analysis, pandas does this better. Structured arrays are worth knowing for reading fixed-format binary files and for the cases where adding pandas isn't justified.

## Formats beyond NumPy

`.npy` and `.npz` are great for NumPy-only data of moderate size. Past that, the ecosystem has better answers.

**HDF5**, via `h5py`, handles very large arrays with chunking, packing and metadata, supports partial reads and writes. Is readable from most languages. It's the standard in scientific finding for a reason.

**Zarr** is similar in spirit, designed for cloud object storage. Works well with Dask for parallel access.

**Parquet**, via `pyarrow`, is columnar and is the right choice for tabular data going anywhere near a data pipeline or a query engine.

The signals that it's time to move. Files over a few hundred megabytes, needing to read part of an array without loading it, needing to append over time, or needing anything other than Python to read it.

## A safety summary

The security point deserves restating because it's the one thing in this module that can go beyond losing data.

`np.load` runs any code when loading a pickled object array. `allow_pickle=False` is the default and it's protecting you.

Enable it only for files you made, or that arrived through a channel you'd trust with an executable. A `.npy` file from an untrusted source should be treated the way you'd treat a downloaded script. In the object-array case that is what it's.

The safe options, in order of preference: keep the data in plain numeric arrays so pickling never arises. Use a structured dtype for records. Use JSON or Parquet for anything truly heterogeneous.

"It's just a data file" is just the assumption the attack depends on.

## Round-tripping reliably

The habit worth forming is to verify a save-and-load cycle once when adding a new format, rather than discovering the loss later.

```python
np.save(path, a)
b = np.load(path)
assert np.array_equal(a, b) and a.dtype == b.dtype
```

Checking the dtype alongside the values catches just the failure that text formats add silently, and it takes one line.

For floating-point data going through a text format, `np.allclose` rather than `array_equal` is the honest compare. `fmt` has almost certainly truncated a thing.

## Paths, and a common annoyance

`np.save` appends `.npy` if the filename doesn't already end in it. That is convenient until code finds a path, saves to it. Then fails to find the file. Because the actual file has an extra extension the code doesn't know about.

Passing an open file object instead of a path avoids the rewriting fully. Is the solid form when the filename is found.

`np.savez` behaves the same way with `.npz`.

## Compression, in practice

`savez_compressed` costs CPU on write and on read. Saves space only if the data has structure to exploit.

int data with a small range, arrays with many repeated values. Anything sparse compress well. Often by an order of magnitude.

Floating-point reading data compresses poorly. The low-order bits are in effect random. A 10&ndash;20% saving for a few times the CPU is rarely a good trade.

The way to decide is to try both on a representative sample and compare. This Takes a minute and settles it for that dataset.

## Writing for other people

If a file will be read by someone other than you, or by you in two years, the format is only half of it.

Record the shape and dtype expectations one spot the reader will find them, above all for `tofile` output, which carries neither.

Prefer `.npz` with named arrays over a few `.npy` files with real filenames. The names travel with the data.

For anything that is truly a dataset rather than an mid. A thing that will be reused, shared or archived. HDF5 or Parquet carry metadata properly and are readable outside Python. The extra dependency buys real portability.

## The summary

`.npy` for a single array, NumPy only. Lossless, compact, fast.

`.npz` for a few named arrays, compressed only if the data compresses.

Text when a thing else must read it, accepting that the dtype is gone.

`mmap_mode` for partial access to a thing larger than memory.

HDF5, Zarr or Parquet past a few hundred megabytes, or when other tools are involved.

`allow_pickle=False` &mdash; the default &mdash; on anything you didn't give yourself. That one isn't a speed preference. It's the gap between reading a file and running one.

## Questions people ask

<strong>What is the difference between save and savetxt?</strong> save writes a binary .npy file that keeps dtype and shape exactly. savetxt writes readable text, which is bigger, slower and loses precision unless you set the format.

<strong>How do I store several arrays in one file?</strong> Use np.savez, or savez_compressed for smaller files. Loading returns a dict-like object keyed by the names you gave.

<strong>Is it safe to load any .npy file?</strong> Arrays of plain numbers are safe. Object arrays use pickle, so np.load refuses them by default; only set allow_pickle=True for files you trust.

<strong>How do I load a CSV with a header?</strong> Use np.genfromtxt or np.loadtxt with skiprows=1 and delimiter=','. For messy or mixed-type data, pandas is the better tool.

<strong>Can I read a file bigger than memory?</strong> Yes, pass mmap_mode='r' to np.load. The array is mapped from disk and only the pages you touch are read.

<strong>Does loading keep the dtype?</strong> With .npy and .npz, yes, exactly. With text formats you get float64 unless you pass dtype.

## A closing note

Storage is where a project's choices become permanent. A format chosen for convenience during a first test tends to live into production. By then there's data in it.

`.npy` and `.npz` are good enough for a great deal of work and cost nothing to adopt. The point to reconsider is when files grow past a few hundred megabytes, when a thing other than Python needs to read them, or when only part of an array is needed at a time. And recognising that point early is easier than migrating later.
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
