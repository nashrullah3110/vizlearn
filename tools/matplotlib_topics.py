# -*- coding: utf-8 -*-
"""Content for the matplotlib track.

Modules of short runnable steps rather than one long program. matplotlib is
two libraries wearing one name - a stateful pyplot interface and an
object-oriented one - and most confusion about it comes from examples that
mix them without saying so. These use the object-oriented form throughout
and explain the other one where it appears.

Every editor draws: the runner collects any open figures after a run and
displays them under the printed output, so a program that plots shows its
plot rather than reporting success silently.

matplotlib ships with Pyodide (3.5.2 there, older than current), so these
load from the same CDN as the interpreter rather than needing a wheel.
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
from runnable_specs import _matplotlib_prelude

PRELUDE = _matplotlib_prelude()


def topic(slug, title, cat, lead, svg, steps, notes, article, check):
    """One module. `steps` is a list of (heading, blurb, code) triples."""
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "steps": steps, "notes": notes, "article": article, "check": check,
        "wheels": [], "prelude": PRELUDE,
    })
    CHECKS["matplotlib/%s.html" % slug] = {"check": check}


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
# 1. What matplotlib is
# ---------------------------------------------------------------------------
topic(
    "what_is_matplotlib",
    "Figure and Axes",
    "The Objects",
    "The two objects everything else hangs off, and the two APIs that confuse "
    "every example you will read.",
    _svg(_box(16, 20, 128, 56, S, M) + _txt(32, 32, "Figure", M, 8, "start") +
         _box(40, 34, 92, 34, S, A) + _txt(86, 54, "Axes", A, 9)),
    [
        ("A figure holds axes; axes hold the plot",
         "Two objects, and almost every method you will use belongs to the second.",
         '''import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5, 3))

ax.plot([1, 2, 3, 4], [10, 25, 18, 30], marker="o")
ax.set_title("one figure, one axes")

print("figure :", type(fig).__name__)
print("axes   :", type(ax).__name__)
print("axes on this figure:", len(fig.axes))
print()
print("'Axes' is singular here - it is one plotting area, not two axis")
print("objects. The x and y axis objects live on it, as ax.xaxis / ax.yaxis.")'''),

        ("The same plot, two ways to write it",
         "The stateful API draws into whatever figure is current; the "
         "object-oriented one asks a specific axes.",
         '''import matplotlib.pyplot as plt

# stateful: plt.* acts on "the current figure"
plt.figure(figsize=(4, 2))
plt.plot([1, 2, 3], [2, 1, 3])
plt.title("stateful")

# object-oriented: you hold the objects
fig, ax = plt.subplots(figsize=(4, 2))
ax.plot([1, 2, 3], [2, 1, 3])
ax.set_title("object-oriented")

print("two figures were created:", len(plt.get_fignums()))
print()
print("Both draw. The second says which axes it is drawing on, which is")
print("why it keeps working once there is more than one.")'''),

        ("Why the stateful API causes trouble",
         "It has a hidden current figure, and that is a global.",
         '''import matplotlib.pyplot as plt

fig1, ax1 = plt.subplots(figsize=(3.5, 2))
ax1.set_title("first")

fig2, ax2 = plt.subplots(figsize=(3.5, 2))
ax2.set_title("second")

# plt.plot goes to the CURRENT figure, which is now fig2
plt.plot([1, 2, 3], [1, 2, 1])

print("current figure number:", plt.gcf().number)
print("fig1 has lines:", len(ax1.lines))
print("fig2 has lines:", len(ax2.lines), "<- the plt.plot landed here")
print()
print("In a script this is merely surprising. In a notebook, where cells")
print("run in any order, 'the current figure' is whatever ran last.")'''),

        ("set_ methods, and the plt equivalents",
         "The object-oriented names are the plt names with <code>set_</code> in "
         "front, mostly.",
         '''import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5, 3))
ax.plot([1, 2, 3], [4, 5, 6])

ax.set_title("title")
ax.set_xlabel("x label")
ax.set_ylabel("y label")
ax.set_xlim(0, 4)

print("plt.title()  -> ax.set_title()")
print("plt.xlabel() -> ax.set_xlabel()")
print("plt.xlim()   -> ax.set_xlim()")
print("plt.plot()   -> ax.plot()      <- no set_ prefix; it draws")
print()
print("ax.set() takes several at once:")
ax.set(title="set several at once", xlabel="x", ylabel="y")
print("   ", ax.get_title())'''),

        ("Every draw call returns something",
         "Usually a list of the artists it created, which you keep when you want "
         "to change them later.",
         '''import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5, 3))

lines = ax.plot([1, 2, 3], [2, 1, 3])
print("ax.plot returns:", type(lines).__name__, "of", len(lines), "->",
      type(lines[0]).__name__)

line = lines[0]                      # the common idiom is  line, = ax.plot(...)
line.set_color("crimson")
line.set_linewidth(3)
line.set_label("renamed later")
ax.legend()

print()
print("Because it returns a list, the comma in 'line, = ax.plot(...)' is")
print("doing real work - it unpacks the single element.")'''),

        ("Figures have to be closed",
         "Each one holds memory until it is, and in a loop that adds up.",
         '''import matplotlib.pyplot as plt

for i in range(3):
    fig, ax = plt.subplots(figsize=(2.5, 1.5))
    ax.set_title("figure %d" % i)

print("open figures:", len(plt.get_fignums()), plt.get_fignums())
print()
plt.close("all")
print("after plt.close('all'):", len(plt.get_fignums()))
print()
print("matplotlib keeps a reference to every figure it makes, so they are")
print("not garbage collected on their own. A loop that draws and saves")
print("without closing will eventually exhaust memory - and warn at 20.")

fig, ax = plt.subplots(figsize=(4, 2))
ax.plot([0, 1], [0, 1])
ax.set_title("this one is left open, so the page shows it")'''),
    ],
    [
        "A <strong>Figure</strong> is the canvas; an <strong>Axes</strong> is one plotting area on it. Almost every method you want belongs to the Axes.",
        "<code>fig, ax = plt.subplots()</code> is the standard opening line &mdash; it makes both and hands them to you.",
        "The <strong>stateful</strong> <code>plt.*</code> API draws into a hidden current figure; the <strong>object-oriented</strong> one names the axes explicitly.",
        "<code>plt.title()</code> becomes <code>ax.set_title()</code>. Drawing methods like <code>plot</code> keep their names.",
        "Draw calls return the artists they created &mdash; <code>line, = ax.plot(...)</code> unpacks the one-element list.",
        "matplotlib keeps a reference to every figure, so they must be <strong>closed</strong>; a drawing loop without <code>plt.close</code> leaks memory and warns at 20.",
    ],
    '''
title: Figure and Axes
intro: The two objects everything hangs off, and the two APIs that confuse every example.

## Two objects

A **Figure** is the whole image: the canvas, its size, its background, and the file it is eventually saved to.

An **Axes** is one plotting area inside it &mdash; the box with the ticks, the data, and the labels.

The name is unfortunate. "Axes" is singular here, and it does not mean "the x and y axes". Those are `ax.xaxis` and `ax.yaxis`, which are objects on the Axes. One figure can hold many Axes, which is what a grid of subplots is.

Nearly everything you want to do belongs to the Axes. Plotting, labelling, limits, ticks, legends and annotation are all `ax.` methods. The Figure handles size, the overall title, layout between subplots, and saving.

`fig, ax = plt.subplots()` creates one of each and returns both. It is the standard first line of almost every matplotlib program, and it is worth using even for a single plot, because it puts you in the API that keeps working when the plot grows.

## Two APIs

Every matplotlib example you find online is written in one of two styles, and mixing them is why so many of them are hard to follow.

**Stateful (pyplot)**: `plt.plot(...)`, `plt.title(...)`, `plt.xlabel(...)`. These act on "the current figure and current axes", which matplotlib tracks internally. It is compact and reads well for a single quick plot.

**Object-oriented**: `ax.plot(...)`, `ax.set_title(...)`. You hold the objects and say which one you mean.

The stateful API is a convenience layer over the object-oriented one. `plt.title` finds the current axes and calls `set_title` on it.

The translation is mechanical: most `plt.foo()` calls become `ax.set_foo()`. The exceptions are the drawing methods &mdash; `plot`, `scatter`, `bar` &mdash; which keep their names because they are actions rather than properties.

## Why the object-oriented form

The current figure is a global variable, with the problems globals always have.

In a script that draws one plot, nothing goes wrong. In a script that draws several, `plt.plot` after creating a second figure lands on the second, whether or not that was the intent. In a notebook, where cells run repeatedly and out of order, "the current figure" is whatever ran last &mdash; which is why plots sometimes appear on the wrong chart or an earlier figure gains a line nobody added.

The object-oriented form has no such ambiguity: `ax1.plot` draws on `ax1`.

It is also the only form that works comfortably with subplots, where there are several axes and no sensible notion of a current one.

This track uses `fig, ax = plt.subplots()` throughout, and mentions the `plt` equivalent where you are likely to meet it in other people's code.

## Artists

Everything drawn is an **Artist**: lines, text, patches, the axes themselves.

Draw calls return the artists they create. `ax.plot` returns a **list** of `Line2D` objects &mdash; a list, because one call can draw several lines &mdash; which is why the idiom is:

```python
line, = ax.plot(x, y)
```

The trailing comma unpacks the single element. Without it, `line` is a list and `line.set_color` fails.

Keeping the artist matters when you want to change it later: `line.set_color("crimson")`, `line.set_label("...")`. For a static plot you can ignore the return value entirely, which is what most code does.

## Closing figures

matplotlib keeps an internal reference to every figure created through pyplot, so they are never garbage collected while that reference exists.

For one plot that does not matter. In a loop &mdash; generating a chart per group, per file, per day &mdash; the figures accumulate, and matplotlib warns after twenty that "more than 20 figures have been opened".

`plt.close(fig)` closes one; `plt.close("all")` closes everything. Any loop that draws should close.

On these pages the runner collects open figures after each run and closes them, which is why an editor that draws shows its plot. That is also why a `plt.close()` at the end of an editor would leave you with no image &mdash; the figure has to still be open when the program finishes.

## Where matplotlib sits

matplotlib is the oldest and most widely used plotting library in Python, and nearly everything else is built on it or interoperates with it. pandas' `.plot`, seaborn, and the plotting in scikit-learn and statsmodels all produce matplotlib objects you can adjust afterwards.

That is the practical argument for learning it even if you mostly use something higher-level: when the convenience wrapper does not do quite what you need, the escape hatch is matplotlib, and it is always available.

Its age also explains its awkward parts. The pyplot interface was designed to feel like MATLAB, the object-oriented API came later, and both are supported forever. Most confusing examples online are simply mixing the two.

## The parts of a figure

Worth naming, because the documentation uses these terms constantly:

**Figure** &mdash; the whole canvas.

**Axes** &mdash; one plotting area. A figure holds one or many.

**Axis** &mdash; the x or y scale on an Axes, with its ticks and label. `ax.xaxis`.

**Artist** &mdash; anything drawn: lines, text, patches, the axes themselves.

**Spines** &mdash; the four lines bounding the plotting area.

**Ticks** &mdash; the marks on an axis, with major and minor variants.

The hierarchy is Figure &rarr; Axes &rarr; Axis &rarr; ticks and labels, and almost every method lives on the Axes.

## Showing a figure

In a **notebook**, figures display automatically when a cell finishes. `%matplotlib inline` is the default in Jupyter and rarely needs stating.

In a **script**, nothing is displayed unless you ask. `plt.show()` opens a window and blocks; `fig.savefig(path)` writes a file. A script that draws and does neither produces nothing, which is a common first surprise.

On **these pages**, the runner collects any figure still open when your program finishes, renders it to a PNG, and shows it under the printed output. That is why the editors here never call `show` or `savefig` &mdash; and why calling `plt.close()` at the end of an editor would leave you with no picture.

## Backends

A **backend** is what matplotlib draws with. Interactive ones open windows; non-interactive ones write files.

`AGG` is the non-interactive raster backend, and it is what these pages use, because a Web Worker has no window to draw into. `matplotlib.use("AGG")` selects it, and that call must come before pyplot is imported &mdash; which is why it is in the page setup rather than in the examples.

You will meet this in two places: on a server with no display, where `AGG` is required, and in a script that hangs on `plt.show()` because it picked an interactive backend it cannot actually use.

## What this track covers

The first modules are the drawing types: lines, scatters, bars, histograms, boxes, images.

Then the parts that make a chart readable: labels, legends, limits, ticks, scales, colour, annotation.

Then layout: subplots, spacing, twin axes, saving.

Then judgement: choosing a chart, common mistakes, and performance when the data is large.

Every module is six short programs, and each one draws. Changing a number and re-running is the fastest way to find out what an argument actually does &mdash; which is worth more here than in most libraries, because matplotlib's argument names are not always guessable.

## Questions people ask first

**Why are there two ways to do everything?**

History. pyplot was written to feel like MATLAB, where there is one implicit figure and commands act on it. The object-oriented API came later and is what pyplot calls underneath. Both are supported permanently, so examples mix them, and that is the main reason matplotlib feels harder than it is.

**Do I need `plt.show()`?**

In a script, yes, unless you are saving to a file. In a notebook, no. On these pages, no &mdash; the runner collects whatever is open.

**Why does my figure look different on someone else's machine?**

A different style, a different `matplotlibrc`, a missing font, or a different backend. The first two are the usual causes and both are silent.

**Should I use seaborn instead?**

For statistical charts, often yes &mdash; it produces matplotlib objects, so nothing is lost. Knowing matplotlib is what lets you adjust what seaborn gives you.

**Why is my chart slow?**

Almost always too many artists, or too many points to be visible. Both have their own module.

## How to read the documentation

matplotlib's documentation is large and organised around the object model, which makes it hard to search until you know the vocabulary.

Three habits help.

Search for the **Axes method**, not the pyplot function &mdash; `Axes.set_xlabel` rather than `plt.xlabel` &mdash; because that page lists the full signature and every keyword.

Read the **Artist** page for the thing you are styling. Most keyword arguments to a drawing call are properties of the artist it creates, so `Line2D` documents everything `plot` accepts beyond its own arguments.

Use the **examples gallery** as a search index. Finding a picture that resembles what you want and reading its source is usually faster than working out what the operation is called.

The API is wide but shallow: a few hundred methods, most of which take the same handful of styling arguments. Once the vocabulary is familiar the documentation becomes navigable.

## In summary

Two objects: a Figure holding one or more Axes. Almost every method you want belongs to the Axes.

Two APIs: the stateful `plt.*` one that draws into a hidden current figure, and the object-oriented one that names the axes. The second is what this track uses, because the first goes wrong the moment there is more than one figure &mdash; which in a notebook is immediately.

`fig, ax = plt.subplots()` is the standard opening line, and the translation from any pyplot example is mechanical: `plt.title` becomes `ax.set_title`, and the drawing methods keep their names.

Draw calls return the artists they create, which you keep when something needs changing later and ignore otherwise.

And figures must be closed, because matplotlib holds a reference to every one until you do.

Everything after this module is either a kind of drawing or a way of making the result readable, and all of it hangs off those two objects.

## A closing note

matplotlib has a reputation for being hard, and most of that comes from two things this module addresses.

The first is the two APIs, and examples that mix them without saying so. Once you know that `plt.title` and `ax.set_title` are the same operation reached differently, most confusing code becomes readable.

The second is that it is a **drawing** library rather than a charting one. It has no opinion about what a good chart is, so it will not stop you, and everything is possible at the cost of nothing being automatic.

That is the right trade for a foundation library, and it is why every higher-level tool in Python either sits on matplotlib or has to reimplement it. Learning it well means the ceiling is never the library.

## Reading the code back

Every chart in this track starts the same way and ends the same way: create a figure and axes, draw with ax methods, label, adjust, and let the runner show it. What changes in the middle is the drawing call and the handful of arguments it takes. Recognising that shape makes the rest of the library a matter of looking up which method and which argument, rather than learning a new pattern each time.
''',
    [
        {"q": "What does 'Axes' refer to in matplotlib?",
         "options": ["The x and y axis objects", "One plotting area inside a figure", "The figure itself", "The tick marks"],
         "answer": 1,
         "why": "The name is unfortunate - it is singular, and the x/y axis objects live on it as ax.xaxis and ax.yaxis."},
        {"q": "Why prefer `ax.plot()` over `plt.plot()`?",
         "options": ["It is faster", "plt draws into a hidden 'current figure', which is a global and goes wrong with several figures or in a notebook", "plt is deprecated", "ax supports more plot types"],
         "answer": 1,
         "why": "In a notebook where cells run out of order, the current figure is whatever ran last - which is why plots sometimes land on the wrong chart."},
        {"q": "Why is there a comma in `line, = ax.plot(x, y)`?",
         "options": ["A typo", "plot returns a list, because one call can draw several lines; the comma unpacks the single element", "It creates a tuple", "It is optional syntax"],
         "answer": 1,
         "why": "Without it, `line` is a list and `line.set_color` fails."},
        {"q": "Why must figures be closed?",
         "options": ["To save the file", "matplotlib keeps a reference to each one, so they are never garbage collected", "To reset the style", "They close themselves"],
         "answer": 1,
         "why": "A loop that draws without closing leaks memory, and matplotlib warns once more than 20 are open."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Line plots
# ---------------------------------------------------------------------------
topic(
    "line_plots",
    "Line Plots",
    "Drawing",
    "plot() and the arguments that do most of the work - style, width, colour "
    "and what happens with missing data.",
    _svg('<polyline points="20,64 48,36 76,50 104,24 136,40" fill="none" '
         'stroke="%s" stroke-width="2.5"/>' % A +
         _box(14, 16, 132, 58, "none", B)),
    [
        ("x and y, or just y",
         "With one argument matplotlib supplies the index as x.",
         '''import matplotlib.pyplot as plt

y = [3, 7, 5, 9, 6]

fig, (a, b) = plt.subplots(1, 2, figsize=(7, 2.5))

a.plot(y)
a.set_title("plot(y) - x is 0,1,2,...")

a2 = [10, 20, 30, 40, 50]
b.plot(a2, y)
b.set_title("plot(x, y)")

print("one argument means y; the x values are range(len(y))")
print("x used on the left :", list(range(len(y))))
print("x used on the right:", a2)'''),

        ("Several lines, and where the colours come from",
         "Each call takes the next colour from the axes' cycle.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, ax = plt.subplots(figsize=(6, 3))
for k in range(4):
    ax.plot(x, np.sin(x + k), label="shift %d" % k)
ax.legend()

cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
print("the default colour cycle:")
for c in cycle[:6]:
    print("   ", c)
print()
print("Four calls took the first four. A fifth would take the fifth,")
print("and the eleventh would wrap around to the first.")'''),

        ("Style, width and colour",
         "The three arguments that turn a default line into a deliberate one.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 6, 40)

fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(x, np.sin(x), color="crimson", linewidth=2.5, label="solid, thick")
ax.plot(x, np.cos(x), color="steelblue", linestyle="--", label="dashed")
ax.plot(x, np.sin(x) * 0.5, color="0.4", linestyle=":", linewidth=2, label="dotted grey")
ax.legend()

print("linestyle: '-' solid, '--' dashed, '-.' dashdot, ':' dotted")
print("color    : a name, a hex string, or '0.4' for a grey level")
print("linewidth: points, default", plt.rcParams["lines.linewidth"])'''),

        ("The format-string shorthand",
         "Compact, common in examples, and worth being able to read.",
         '''import matplotlib.pyplot as plt

x = [1, 2, 3, 4]

fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(x, [1, 4, 2, 5], "r--o", label="'r--o'")
ax.plot(x, [2, 5, 3, 6], "g:s", label="'g:s'")
ax.plot(x, [3, 6, 4, 7], "b-^", label="'b-^'")
ax.legend()

print("A format string packs colour, linestyle and marker into one word:")
print("   r = red, g = green, b = blue, k = black")
print("   -- dashed, : dotted, - solid")
print("   o circle, s square, ^ triangle")
print()
print("It is terse and limited - only eight colours, and no way to set")
print("width. Keyword arguments are clearer for anything real.")'''),

        ("Missing values break the line",
         "NaN leaves a gap rather than drawing through it, which is usually right.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(12)
y = np.array([1, 2, 3, np.nan, np.nan, 6, 7, 8, 9, np.nan, 11, 12], dtype=float)

fig, (a, b) = plt.subplots(1, 2, figsize=(7, 2.5), sharey=True)

a.plot(x, y, marker="o")
a.set_title("with NaN: gaps")

ok = ~np.isnan(y)
b.plot(x[ok], y[ok], marker="o")
b.set_title("dropped: joined through")

print("NaN is not plotted and the line is broken there.")
print("Dropping the points instead draws a line through the gap, which")
print("implies data you do not have. The gap is usually more honest.")'''),

        ("Order matters, and so does zorder",
         "Later calls draw on top, unless you say otherwise.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 200)

fig, (a, b) = plt.subplots(1, 2, figsize=(7, 2.5))

a.fill_between(x, 0, np.sin(x) + 1, color="lightsteelblue")
a.plot(x, np.sin(x) + 1, color="crimson", linewidth=2)
a.set_title("line drawn second")

b.plot(x, np.sin(x) + 1, color="crimson", linewidth=2)
b.fill_between(x, 0, np.sin(x) + 1, color="lightsteelblue")
b.set_title("fill drawn second - line hidden")

print("Same two calls, swapped. The right-hand line is under the fill.")
print()
print("zorder overrides the order: higher draws later.")
print("   line zorder default:", 2.0, " patch default:", 1.0)
print("   so a line normally sits above a fill anyway - unless the fill")
print("   is drawn after it, as on the right.")'''),
    ],
    [
        "<code>ax.plot(y)</code> uses <code>range(len(y))</code> as x; <code>ax.plot(x, y)</code> is explicit.",
        "Each <code>plot</code> call takes the next colour from the axes' <strong>property cycle</strong>, wrapping after ten.",
        "<code>color</code>, <code>linestyle</code> and <code>linewidth</code> do most of the styling; <code>\"0.4\"</code> is a grey level.",
        "The format string <code>\"r--o\"</code> packs colour, style and marker into one word &mdash; terse, limited, and worth being able to read.",
        "<code>NaN</code> leaves a <strong>gap</strong> in the line rather than being interpolated across, which is usually the honest choice.",
        "Later draw calls paint on top; <code>zorder</code> overrides that.",
    ],
    '''
title: Line Plots
intro: plot() and the arguments that do most of the work.

## The signature

`ax.plot(y)` draws `y` against its index. `ax.plot(x, y)` draws one against the other.

That one-argument form is convenient and occasionally misleading &mdash; a plot whose x axis reads 0 to 99 when the data is dated is usually a forgotten x argument rather than a deliberate choice.

`plot` accepts lists, NumPy arrays and pandas Series. With a Series it uses the index as x, which is why plotting a time-indexed Series gives a dated axis for free.

## The colour cycle

Each call to `plot` on the same axes takes the next colour from the **property cycle**, a list of ten colours defined by the current style.

This is why several lines drawn in a loop come out in different colours with no work, and why the eleventh line repeats the first.

`plt.rcParams["axes.prop_cycle"]` holds it. `ax.set_prop_cycle(...)` replaces it for one axes, which is how you enforce a house palette.

Passing an explicit `color` bypasses the cycle without advancing it.

## Styling

Three keywords cover nearly everything:

`color` &mdash; a name (`"crimson"`), a hex string (`"#4c72b0"`), a single letter (`"r"`), a grey level as a string (`"0.4"`), or an RGBA tuple.

`linestyle` &mdash; `"-"` solid, `"--"` dashed, `"-."` dashdot, `":"` dotted, or a dash pattern as a tuple.

`linewidth` &mdash; in points.

Add `alpha` for transparency, which is how you keep many overlapping lines readable, and `marker` to show where the actual data points are.

That last one matters more than it looks: a smooth line through four points implies a lot of data that does not exist. Markers say where the measurements are and let the line be what it is &mdash; a visual aid rather than a claim.

## The format string

`ax.plot(x, y, "r--o")` sets colour, linestyle and marker in one string.

It is worth learning to read because it appears constantly in examples and documentation. It is not worth preferring: it supports only eight colours, cannot set width or alpha, and is opaque to anyone who has not memorised it.

The order within the string does not matter, and any part can be omitted &mdash; `"o"` alone draws markers with no connecting line, which is a scatter plot by another route.

## Missing data

`NaN` values are skipped, and the line is broken where they occur.

This is the right default. A line drawn straight through a gap asserts that the value moved smoothly across it, which is exactly the thing you do not know.

If you want the line joined, dropping the missing points is explicit about it:

```python
ok = ~np.isnan(y)
ax.plot(x[ok], y[ok])
```

Note that `None` behaves like `NaN` here, and a masked array's masked values are also skipped.

For a long series with occasional gaps, the broken line can look noisy; drawing markers as well makes the pattern of missingness visible rather than merely untidy.

## Drawing order

Artists are drawn in the order the calls are made, so later calls sit on top.

`zorder` overrides it. Higher values draw later. The defaults are set so that the usual expectations hold &mdash; patches at 1, lines at 2, text at 3 &mdash; which is why a line normally appears above a filled region even when the fill was drawn second.

Where it matters most is grid lines. `ax.grid()` draws below the data by default, and `ax.set_axisbelow(False)` puts it on top, which is almost never what you want but is occasionally what you get from a style sheet.

## Markers

`marker="o"` draws a symbol at each data point. The common ones are `o` circle, `s` square, `^` triangle, `D` diamond, `.` point, `+` and `x`.

Markers matter more than they look. A smooth line through five points implies a continuous relationship measured densely; markers say where the measurements actually are and let the line be the visual aid it is.

`markevery=10` draws one marker in ten, which keeps the "here are the observations" signal on a dense series without a solid band of symbols.

`markersize`, `markerfacecolor` and `markeredgecolor` style them separately from the line, so a hollow marker is `markerfacecolor="none"`.

## Steps and stems

Not every sequence is a line.

`ax.step(x, y, where="post")` draws a step function, which is correct for anything that holds a value until it changes: a price, a setting, a state. A straight line between the points would claim a gradual transition that did not happen.

`where` takes `"pre"`, `"post"` or `"mid"`, deciding whether the step happens at the start or the end of each interval. Getting it wrong shifts every value by one position, and the chart looks plausible either way.

`ax.stem` draws a vertical line to each point, which suits sparse discrete data.

`ax.fill_between` under a line turns it into an area chart, appropriate when the quantity accumulates to something meaningful and misleading when it does not.

## Multiple lines and readability

Four or five lines on one axes is usually the limit before the chart becomes a tracing exercise.

Beyond that, the options in order of preference are: highlight one and grey the rest, split into small multiples, or reduce to the two lines the chart is actually about.

Where several lines must stay, three things help.

**Direct labels** at the line ends, instead of a legend.

**Ordering the legend** to match the vertical order of the lines at their right-hand end, so the eye can map them without hunting. `ax.legend(handles=...)` in the order you want.

**Varying linestyle** as well as colour, so the chart survives greyscale.

## Interpolation is a claim

A line between two points asserts that the quantity passed through the values in between.

For a temperature sampled hourly, that is reasonable. For monthly sales, the line between January and February is decorative &mdash; nothing happened at "January the 15th" in the data.

That does not make the line wrong; connecting points is how the eye reads a trend, and a scatter of twelve unconnected points is harder to follow. But it is worth knowing that the line is an aid rather than data, which is another argument for markers.

Where the gaps are genuinely large, breaking the line is more honest than spanning them, and that is what leaving the NaN in does for you automatically.

## Performance note

One `plot` call with a large array is fast. Many `plot` calls are slow, because the cost is per artist rather than per point.

Drawing fifty lines in a loop creates fifty artists; where they can be combined, `LineCollection` draws them as one.

That matters at hundreds of lines rather than dozens, and it is covered properly in the performance module.

## A worked example

Turning a default line chart into a finished one is a short, fixed sequence.

```python
fig, ax = plt.subplots(figsize=(7.5, 3.5))

ax.plot(x, y, color="#264653", linewidth=2, marker="o", markersize=4)

ax.set_title("What the chart shows", loc="left", fontsize=12, fontweight="bold")
ax.set_xlabel("Month of 2024")
ax.set_ylabel("Sales (thousands)")

ax.margins(x=0.02)
ax.grid(True, axis="y", alpha=0.3)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
```

Aspect, colour, weight, markers, a title that says something, labelled units, a faint grid on one axis, two spines removed.

Ten lines, none of them clever, and the result looks deliberate. Every one is covered somewhere in this track, and together they are most of what separates a default matplotlib chart from a published one.

## Reading a line chart critically

Three questions worth asking of any line chart, including your own.

**Does the y axis start at zero, and should it?** A line encodes position, so truncation is legitimate &mdash; and it changes the apparent size of every change. If a 2% movement fills the chart, the reader should be able to tell.

**Are the x values evenly spaced?** If the axis is categorical or the points are irregular in time, the slope between points is not a rate, and the eye reads it as one.

**What is between the points?** Twelve monthly observations joined by lines look like a continuous series. The line is an aid; the data is twelve points.

None of these makes a line chart wrong. They are the things a careful reader checks, and knowing them is what lets you draw one that survives the checking.

## In summary

`ax.plot(x, y)` with `color`, `linewidth`, `linestyle` and `marker` covers the great majority of line charts.

The colour cycle supplies distinct colours automatically and wraps after ten, which is well past the point where a line chart has stopped being readable.

NaN breaks the line, which is the honest treatment of a gap.

Markers say where the data actually is, and matter most when the points are few &mdash; a smooth line through five observations claims a lot.

Later calls draw on top, and `zorder` overrides it.

And the finishing sequence is the same every time: an aspect ratio suited to the data, a title that says something, labelled units, a faint grid on one axis, and the top and right spines removed.

## Smoothing

A noisy series is often plotted with a smoothed version over it, and the pairing is more honest than either alone.

The raw series in a pale colour and the rolling mean in a strong one shows both the variation and the trend, and makes clear that the smooth line is derived rather than measured.

Two cautions worth stating on the chart.

**The window is a choice**, and a longer one produces a smoother, more convincing line that is further from the data. Naming it &mdash; "7-day mean" &mdash; is the minimum.

**A centred window uses future values**, which is fine for describing history and wrong for anything presented as a signal available at the time. A trailing window is the honest choice for that case, at the cost of lagging the turns.

Plotting only the smoothed line, without the raw data, is where this becomes misleading, because the reader has no way to judge how much was smoothed away.

## Highlighting within a line chart

A line chart with one important series and several for context is the most common real case, and the treatment is consistent:

```python
for name, y in others.items():
    ax.plot(x, y, color="0.85", linewidth=1, zorder=1)
ax.plot(x, focus_y, color="#264653", linewidth=2.5, zorder=2)
ax.text(x[-1], focus_y[-1], "  " + focus_name, va="center", color="#264653")
```

The grey lines give the range and the shape of the group, so nothing is lost. The dark line is unmistakably the subject. The label at the end removes the legend.

`zorder` ensures the highlighted line is on top regardless of drawing order, which matters when the context lines are drawn in a loop after it.

This pattern is worth having to hand, because it converts the hardest kind of line chart &mdash; many series, one message &mdash; into one of the easiest to read.

## One more thing

`ax.plot` accepts several x/y pairs in one call &mdash; `ax.plot(x, y1, x, y2)` &mdash; which draws both with separate colours from the cycle.

It is compact and gives no way to label the lines individually, so a loop with `label=` is usually better. Worth recognising in existing code, where it appears often.

## The short version

A line chart is the most common chart there is, and the finishing sequence is the same every time: aspect, colour, weight, title, units, a faint grid, two spines removed.

The line itself is an aid rather than data, which is worth remembering when the points are few and the line is doing a lot of implying.

## Reading the code back

A finished line chart is about a dozen calls, and it is worth being able to name what each one is for: the figure size sets the aspect, the plot call sets colour and weight, the title carries the message, the labels carry the units, the margins control the breathing space, the grid supports value reading, and the spine removal takes away what carries nothing. Nothing in that list is optional in the sense of being decorative; each answers a question a reader would otherwise have to ask. Writing them in the same order every time makes the chart quick to produce and quick to review, which is most of why a house function is worth having.
''',
    [
        {"q": "What does `ax.plot(y)` use for the x values?",
         "options": ["Zeros", "range(len(y))", "It raises", "The y values"],
         "answer": 1,
         "why": "An axis reading 0 to 99 when the data is dated is usually a forgotten x argument rather than a choice."},
        {"q": "Why do four lines drawn in a loop come out in different colours?",
         "options": ["Random assignment", "Each call takes the next colour from the axes' property cycle", "matplotlib detects overlap", "They do not"],
         "answer": 1,
         "why": "The cycle holds ten colours, so the eleventh line repeats the first. Passing an explicit color bypasses it without advancing it."},
        {"q": "What does matplotlib do with a NaN in the middle of a line?",
         "options": ["Interpolates across it", "Breaks the line, leaving a gap", "Raises", "Treats it as zero"],
         "answer": 1,
         "why": "The right default - a line drawn through the gap would assert the value moved smoothly across it, which is the thing you do not know."},
        {"q": "Two calls draw a fill and a line over the same region. What decides which is visible?",
         "options": ["Colour", "Call order, unless zorder overrides it", "Alpha", "Line width"],
         "answer": 1,
         "why": "Later calls draw on top. Defaults put patches at 1 and lines at 2, so a line usually sits above a fill drawn before it."},
    ],
)


# ---------------------------------------------------------------------------
# 3. Scatter plots
# ---------------------------------------------------------------------------
topic(
    "scatter_plots",
    "Scatter Plots",
    "Drawing",
    "scatter() versus plot(), and the two extra dimensions you get for free.",
    _svg(_box(14, 16, 132, 58, "none", B) +
         '<circle cx="36" cy="58" r="4" fill="%s"/><circle cx="58" cy="42" r="6" fill="%s"/>'
         '<circle cx="84" cy="50" r="3" fill="%s"/><circle cx="106" cy="30" r="7" fill="%s"/>'
         % (A, A, A, A)),
    [
        ("scatter and plot draw the same dots differently",
         "One makes a collection, the other makes a line with markers and no line.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
x, y = rng.random(30), rng.random(30)

fig, (a, b) = plt.subplots(1, 2, figsize=(7, 3))

a.scatter(x, y)
a.set_title("ax.scatter")

b.plot(x, y, "o")
b.set_title('ax.plot(x, y, "o")')

print("plot with a marker and no linestyle looks identical here.")
print("The difference is what you can vary:")
print("   plot   - every marker the same size and colour")
print("   scatter- size and colour can vary per point")
print()
print("plot is faster for many identical points; scatter is the one")
print("that can encode more than two variables.")'''),

        ("Size as a third variable",
         "<code>s</code> is in points squared, so it scales with area rather than "
         "radius.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
x, y = rng.random(40), rng.random(40)
weight = rng.random(40) * 300

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.scatter(x, y, s=weight, alpha=0.6, edgecolor="black", linewidth=0.5)
ax.set_title("size encodes a third variable")

print("s is area in points**2, not diameter.")
print("So a point with s=400 is twice as WIDE as one with s=100,")
print("and four times the area - which is the point: area is what")
print("the eye compares.")'''),

        ("Colour as a fourth",
         "<code>c</code> takes an array, and then a colorbar explains it.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(2)
x, y = rng.random(60), rng.random(60)
value = x + y

fig, ax = plt.subplots(figsize=(6, 3.5))
sc = ax.scatter(x, y, c=value, cmap="viridis", s=60)
fig.colorbar(sc, ax=ax, label="x + y")
ax.set_title("colour encodes a fourth variable")

print("c= an array   -> mapped through a colormap")
print("color= a name -> one fixed colour for every point")
print()
print("Those two arguments look alike and mean different things, which")
print("is a common source of 'why is my whole plot one colour'.")'''),

        ("Overplotting hides the data",
         "With enough points, a scatter becomes a silhouette.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
n = 5000
x = rng.normal(size=n)
y = x * 0.6 + rng.normal(size=n) * 0.8

fig, (a, b, c) = plt.subplots(1, 3, figsize=(9, 3))

a.scatter(x, y, s=10)
a.set_title("opaque: a blob")

b.scatter(x, y, s=10, alpha=0.05)
b.set_title("alpha=0.05")

c.hexbin(x, y, gridsize=30, cmap="Blues")
c.set_title("hexbin: counts")

print("5000 points. The first tells you the range and nothing else.")
print("alpha shows density; hexbin measures it.")
print("For very large n, hexbin or a 2-D histogram is the honest choice.")'''),

        ("Marker shape, edges and transparency",
         "The arguments that make a dense scatter readable.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(4)

fig, ax = plt.subplots(figsize=(6, 3.5))
for marker, name in [("o", "circle"), ("s", "square"), ("^", "triangle")]:
    ax.scatter(rng.random(15), rng.random(15), marker=marker, s=80,
               alpha=0.7, edgecolor="black", linewidth=0.6, label=name)
ax.legend()

print("marker    : o s ^ v D * + x, and more")
print("edgecolor : an outline separates overlapping points")
print("alpha     : below 1 makes density visible")
print()
print("Shape is a weak encoding - people read three shapes reliably and")
print("not six. Colour and position are much stronger.")'''),

        ("Adding a trend line",
         "Two lines of numpy, and the result is drawn like any other line.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(5)
x = rng.random(50) * 10
y = 2.5 * x + rng.normal(scale=4, size=50) + 3

slope, intercept = np.polyfit(x, y, 1)
xs = np.array([x.min(), x.max()])

fig, ax = plt.subplots(figsize=(6, 3.5))
ax.scatter(x, y, alpha=0.7)
ax.plot(xs, slope * xs + intercept, color="crimson", linewidth=2,
        label="fit: y = %.2fx + %.2f" % (slope, intercept))
ax.legend()

print("slope     : %.3f" % slope)
print("intercept : %.3f" % intercept)
print()
print("polyfit(x, y, 1) is a straight line; 2 is a parabola, and so on.")
print("Drawing the fit over only the observed x range avoids implying")
print("it holds outside the data.")'''),
    ],
    [
        "<code>scatter</code> and <code>plot(x, y, \"o\")</code> look alike; only <code>scatter</code> can vary size and colour <strong>per point</strong>.",
        "<code>s</code> is area in points squared, so doubling the width means four times <code>s</code> &mdash; which is right, because area is what the eye compares.",
        "<code>c=</code> an array is mapped through a colormap; <code>color=</code> a name is one fixed colour. The two are easily confused.",
        "With thousands of points a scatter becomes a silhouette &mdash; <code>alpha</code> shows density and <code>hexbin</code> measures it.",
        "<code>edgecolor</code> separates overlapping points; marker shape is a weak encoding beyond about three categories.",
        "A trend line is <code>np.polyfit</code> plus an ordinary <code>plot</code>, drawn only over the observed range.",
    ],
    '''
title: Scatter Plots
intro: scatter() versus plot(), and the two extra dimensions you get for free.

## Two ways to draw dots

`ax.plot(x, y, "o")` draws markers with no connecting line. `ax.scatter(x, y)` draws a collection of points.

They look identical for a simple case, and they differ in what can vary.

`plot` draws one line object: every marker is the same size and the same colour. That uniformity makes it **faster**, sometimes substantially, for large numbers of identical points.

`scatter` draws a `PathCollection` where size and colour can be arrays, one value per point. That is what makes it a four-dimensional display: x, y, size and colour.

The rule of thumb: `plot` when the points are all alike, `scatter` when they are not.

## Size

`s` is the marker area in **points squared**.

That trips people, because doubling `s` does not double the visual width &mdash; it takes four times `s` to double the width. The default is around 36, meaning six points across.

Area is the right thing to scale, because the eye compares areas rather than radii. A common mistake is passing a raw value as `s` and getting circles that differ far more than the underlying numbers do; scaling into a sensible range first is usually needed.

Very small values disappear and very large ones overlap into a mass, so the useful range is narrow &mdash; roughly 10 to 400 for most plots.

## Colour

`c=` takes an **array** of values, which are mapped through a colormap and can be explained with a colorbar.

`color=` takes a **single** colour applied to every point.

The names are one letter apart and the failure is silent: passing an array to `color` either errors or produces something unintended, and passing a single colour to `c` works but wastes the mechanism. "Why is my whole plot one colour" is nearly always this.

`fig.colorbar(sc, ax=ax)` needs the object `scatter` returned, which is why the return value is captured here where it is ignored elsewhere.

## Overplotting

A scatter with a few hundred points shows the data. With a few thousand it shows the outline of the data, and every point in the middle is hidden behind another.

Three responses, in order of how much they preserve:

`alpha` below 1 makes density visible as darkness. It is the cheapest fix and works up to tens of thousands of points.

Smaller markers help, and combine with alpha.

`hexbin` or `hist2d` bins the points and shows counts, which turns density from something implied into something measured. Past roughly fifty thousand points this is the only honest option, and it is also far faster to draw.

Sampling is a fourth option, and a reasonable one when the shape matters more than the completeness.

## Making it readable

`edgecolor="black"` with a thin `linewidth` outlines each marker, which separates points that overlap. It is the single most effective small improvement to a moderately dense scatter.

Marker shape distinguishes categories, and does so weakly &mdash; readers reliably tell apart about three shapes, not six. Colour and position are much stronger encodings; if you need six categories, small multiples usually beat six shapes on one plot.

## Trend lines

`np.polyfit(x, y, 1)` returns slope and intercept, and the fit is then drawn with an ordinary `plot`.

Two details worth getting right. Draw the line only over the range of the observed x values, so it does not imply the relationship holds beyond the data. And put the coefficients in the legend label, so the chart carries the number rather than requiring the reader to estimate it.

For anything beyond a straight line, `numpy.polynomial` is the modern interface and SciPy or statsmodels give confidence intervals &mdash; at which point the fit is a statistical claim and deserves the surrounding machinery.

## Colour by category

For a categorical variable, plotting one scatter per group is clearer than mapping colours by hand:

```python
for name, sub in groups.items():
    ax.scatter(sub.x, sub.y, label=name, alpha=0.7)
ax.legend()
```

Each call takes the next colour from the cycle and the legend is built from the labels, so nothing has to be assembled manually.

Passing a list of category codes to `c=` works and gives you a continuous colormap applied to arbitrary integers, which implies an ordering the categories do not have &mdash; the same mistake as using a sequential colormap for categories.

## Bubble charts

Encoding a third variable in the marker area produces a bubble chart, and it has a specific weakness: area is read poorly, so the third variable is the least accurately perceived thing on the chart.

Two rules make them work when they are used.

Scale by **area**, not by radius. Passing the raw value as `s` scales by area already, since `s` is area &mdash; but computing a radius and squaring it is a common way to exaggerate differences fourfold.

Provide a **size legend**, since nobody can read an area off a chart without a reference. `ax.legend` can be built from proxy artists at a few representative sizes.

If the third variable is the point of the chart, position or colour will carry it better than size.

## Jitter for discrete values

When one axis is discrete &mdash; a rating from one to five, a day of the week &mdash; points land exactly on top of each other and the density is invisible.

Adding a small random offset separates them:

```python
xj = x + rng.uniform(-0.15, 0.15, len(x))
```

The jitter must be small enough not to blur the categories, and it should be mentioned if the chart is published, because it is a deliberate distortion of position.

`alpha` and marker size do part of the same job and do not move anything.

## Connecting scatter points

`ax.plot(x, y, "-o")` connects points in the order they appear in the array, which for a scatter is usually meaningless and occasionally exactly right.

The case where it is right is a **connected scatter**: two variables measured over time, with the line showing the path through the space. Unemployment against inflation year by year, for instance. Adding an arrow or labelling the first and last point makes the direction readable.

For anything without a natural order, sorting by x before connecting is what turns it into a line chart, and doing it accidentally &mdash; because the data happened to arrive sorted &mdash; produces a chart that implies a sequence that does not exist.

## Density alternatives, in order

As n grows, the sequence of reasonable displays is fairly fixed:

**Under 1,000** &mdash; a plain scatter, with `edgecolor` for separation.

**1,000 to 20,000** &mdash; `alpha` around 0.1&ndash;0.3, smaller markers.

**20,000 to 500,000** &mdash; `hexbin` or `hist2d`, which measure density rather than implying it.

**Above that** &mdash; datashader, or aggregate before plotting.

At every stage the question is the same: can the reader see the middle of the distribution, or only its outline? If only the outline, the display has stopped working regardless of how many points are technically drawn.

## Correlation and what a scatter shows

A scatter is the display for a relationship, and it shows more than a correlation coefficient does.

It shows the **shape** &mdash; linear, curved, stepped &mdash; where a coefficient assumes linearity.

It shows **outliers**, which can create or destroy a correlation on their own.

It shows **clusters**, which a single coefficient averages away, and which usually mean an unmodelled group variable.

It shows **heteroscedasticity** &mdash; spread that changes with x &mdash; which invalidates several standard tests.

Anscombe's quartet is the canonical demonstration: four datasets with identical means, variances and correlation, and four completely different scatters. Plotting first is not a formality.

## Practical defaults

A scatter that works most of the time:

```python
ax.scatter(x, y, s=25, alpha=0.6, edgecolor="white", linewidth=0.4)
```

Moderate size, some transparency, and a thin light edge that separates overlapping points without adding visual weight.

From there the adjustments follow the data: lower alpha and smaller markers as n grows, `hexbin` when the middle stops being visible, colour when there is a third variable worth showing.

For a relationship that will be discussed, adding the fit and putting its slope in the legend saves the reader estimating it &mdash; and forces you to look at whether a straight line is the right model, which the scatter will have already told you.

## In summary

`scatter` when size or colour varies per point, `plot` with a marker when they do not &mdash; the second is faster and there is nothing to gain from the machinery you are not using.

`s` is area, so it scales as the square of the visual width.

`c=` takes an array through a colormap; `color=` takes one colour. The distinction is one letter and produces very different charts.

Overplotting is the recurring problem, and the sequence of answers is alpha, then smaller markers, then hexbin, then aggregation before plotting.

`edgecolor` separates overlapping points and is the cheapest readability fix available.

And a scatter shows things a correlation coefficient cannot: shape, clusters, outliers and changing spread. That is the reason to draw one before computing anything.

## Adding a third dimension well

When a scatter needs to carry a third variable, the options are not equally good.

**Colour, sequential** &mdash; for a continuous third variable. Read reasonably well, and needs a colorbar.

**Colour, categorical** &mdash; for a few discrete levels. Works up to about five before the colours stop separating.

**Small multiples** &mdash; one panel per level of a categorical variable. Better than colour for anything above three levels, because comparing panels is easier than separating overlapping colours.

**Size** &mdash; read poorly, and best reserved for a variable that is context rather than the subject.

**Shape** &mdash; read poorly beyond about three levels.

The pattern is that the two strong channels &mdash; position and panel &mdash; are already used or available, and the weak ones should carry the least important variable. Encoding the most important third variable as size is a common inversion of that.

## Labelling points

A scatter of named entities &mdash; countries, products, customers &mdash; frequently wants some of the points labelled.

Labelling all of them produces an unreadable mass. The useful approaches:

**Label the extremes**, which are what the reader will ask about: the highest, the lowest, the furthest from the fit.

**Label a chosen few** that the accompanying text discusses.

**Label on hover**, which matplotlib does not do well and is a reason to use an interactive library when it matters.

For the first two, offsetting the text so it does not sit on the marker is necessary:

```python
ax.annotate(name, (x[i], y[i]), textcoords="offset points",
            xytext=(5, 4), fontsize=9)
```

With more than about eight labels, overlaps become the problem, and `adjustText` is the usual third-party answer &mdash; or, more simply, labelling fewer points.

## One more thing

`ax.scatter` returns a `PathCollection`, and `set_offsets` updates the point positions without redrawing everything.

That is what makes an animated or interactive scatter efficient, and it is the same reuse principle as `set_ydata` on a line: create the artist once, change its data.

## The short version

A scatter is the display that shows what a summary statistic cannot: shape, clusters, outliers and changing spread.

Its failure mode is density, and the sequence of fixes is fixed &mdash; alpha, smaller markers, hexbin, aggregation. The question at every stage is whether the middle of the distribution is still visible.

## Reading the code back

A working scatter is usually four decisions: marker size, transparency, whether an edge is needed, and whether a third variable is being encoded. Everything else follows from the data. The size and alpha are chosen from the number of points rather than from taste, which is why the same two lines that work for two hundred points fail for twenty thousand, and why the sequence of density fixes in this module is worth having in mind before drawing rather than after.
''',
    [
        {"q": "When does `scatter` do something `plot(x, y, 'o')` cannot?",
         "options": ["Never", "When size or colour needs to vary per point", "When there are many points", "When x is a date"],
         "answer": 1,
         "why": "plot draws one line object with uniform markers, which makes it faster for large numbers of identical points."},
        {"q": "What does `s=400` mean compared with `s=100`?",
         "options": ["Four times as wide", "Twice as wide, four times the area", "Four times the radius", "Four points wide"],
         "answer": 1,
         "why": "s is area in points squared. Scaling area is right, because that is what the eye compares."},
        {"q": "What is the difference between `c=` and `color=` in scatter?",
         "options": ["None", "c takes an array mapped through a colormap; color takes one fixed colour", "color is deprecated", "c is for categories"],
         "answer": 1,
         "why": "One letter apart, and 'why is my whole plot one colour' is nearly always this confusion."},
        {"q": "5000 points produce a solid blob. What is the most honest fix?",
         "options": ["Bigger markers", "alpha for density, or hexbin to actually measure it", "A different colour", "Remove the axes"],
         "answer": 1,
         "why": "Past roughly fifty thousand points, binning is the only honest option - and it is far faster to draw."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Bar charts
# ---------------------------------------------------------------------------
topic(
    "bar_charts",
    "Bar Charts",
    "Drawing",
    "Vertical, horizontal, grouped and stacked - and why the baseline has to "
    "be zero.",
    _svg(_box(14, 16, 132, 58, "none", B) +
         '<rect x="34" y="46" width="14" height="26" fill="%s"/>'
         '<rect x="58" y="30" width="14" height="42" fill="%s"/>'
         '<rect x="82" y="52" width="14" height="20" fill="%s"/>'
         '<rect x="106" y="38" width="14" height="34" fill="%s"/>' % (A, A, A, A)),
    [
        ("bar and barh",
         "Horizontal is usually the better choice when the labels are words.",
         '''import matplotlib.pyplot as plt

names = ["alpha", "beta", "gamma with a long name", "delta"]
vals = [23, 45, 12, 38]

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.bar(names, vals)
a.set_title("bar - labels collide")

b.barh(names, vals)
b.set_title("barh - labels read normally")

print("Category labels are words, and words are wide.")
print("barh gives each one a whole line to sit on, so nothing has to be")
print("rotated or truncated. It is the default worth reaching for.")'''),

        ("Sorting is part of the chart",
         "An unsorted bar chart makes the reader do the comparing.",
         '''import matplotlib.pyplot as plt
import numpy as np

names = np.array(["delhi", "pune", "goa", "mumbai", "jaipur"])
vals = np.array([38, 23, 12, 45, 29])

order = np.argsort(vals)

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))
a.barh(names, vals)
a.set_title("as given")
b.barh(names[order], vals[order])
b.set_title("sorted")

print("Same numbers. The right-hand chart answers 'which is biggest'")
print("at a glance; the left one requires reading every bar.")
print()
print("barh draws from the bottom up, so sorting ascending puts the")
print("largest at the top, which is where the eye starts.")'''),

        ("Labelling the bars",
         "<code>bar_label</code> puts the value on the bar, which often replaces the "
         "axis entirely.",
         '''import matplotlib.pyplot as plt

names = ["alpha", "beta", "gamma"]
vals = [23, 45, 12]

fig, ax = plt.subplots(figsize=(6, 3))
bars = ax.barh(names, vals, color="steelblue")
ax.bar_label(bars, padding=3)
ax.set_xlim(0, 52)

print("bar_label takes the container that bar/barh returned.")
print("fmt='%.1f' formats them; labels=[...] replaces them entirely.")
print()
print("With values on the bars, the x axis is usually redundant -")
print("ax.set_xticks([]) removes it and the chart gets quieter.")'''),

        ("Grouped bars",
         "You position them yourself, which is the part that surprises people.",
         '''import matplotlib.pyplot as plt
import numpy as np

groups = ["q1", "q2", "q3"]
a_vals = [10, 15, 12]
b_vals = [8, 18, 14]

x = np.arange(len(groups))
w = 0.38

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(x - w/2, a_vals, w, label="product a")
ax.bar(x + w/2, b_vals, w, label="product b")
ax.set_xticks(x)
ax.set_xticklabels(groups)
ax.legend()

print("There is no 'grouped bar' function. You compute the offsets:")
print("   x        =", list(x))
print("   left  at =", [round(v - w/2, 2) for v in x])
print("   right at =", [round(v + w/2, 2) for v in x])
print()
print("set_xticks(x) then puts the tick in the middle of each pair.")'''),

        ("Stacked bars, and what they hide",
         "<code>bottom</code> is the running total; only the first segment is easy "
         "to compare.",
         '''import matplotlib.pyplot as plt
import numpy as np

groups = ["q1", "q2", "q3"]
a = np.array([10, 15, 12])
b = np.array([8, 18, 14])
c = np.array([5, 4, 9])

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(groups, a, label="a")
ax.bar(groups, b, bottom=a, label="b")
ax.bar(groups, c, bottom=a + b, label="c")
ax.legend()

print("bottom= is where each segment starts: a, then a+b.")
print()
print("Stacking shows the TOTAL well and the components badly - only")
print("the bottom segment shares a baseline, so only it can be compared")
print("across bars by eye. If the components are the point, group them.")'''),

        ("The baseline must be zero",
         "A truncated bar axis misrepresents the data, and it is easy to do by "
         "accident.",
         '''import matplotlib.pyplot as plt

names = ["a", "b", "c"]
vals = [98, 100, 102]

fig, (p, q) = plt.subplots(1, 2, figsize=(8, 3))

p.bar(names, vals)
p.set_ylim(97, 103)
p.set_title("truncated: b looks half of c")

q.bar(names, vals)
q.set_title("from zero: nearly equal")

print("The numbers are 98, 100 and 102 - a 4% spread.")
print("The left chart makes them look like 1x, 2x and 3x.")
print()
print("A bar encodes value as LENGTH, and length from a non-zero base")
print("is not proportional to the value. Lines may be truncated; bars")
print("may not. If the differences are small, use a line or a dot plot.")'''),
    ],
    [
        "<code>barh</code> is usually better than <code>bar</code> when the categories are words &mdash; each label gets its own line and needs no rotation.",
        "<strong>Sort</strong> the bars unless the category order is meaningful; an unsorted chart makes the reader do the comparing.",
        "<code>ax.bar_label(bars)</code> writes values on the bars, which often makes the value axis redundant.",
        "There is no grouped-bar function &mdash; you offset the positions yourself and then <code>set_xticks</code> to centre the labels.",
        "<code>bottom=</code> stacks segments. Stacking shows totals well and components badly, since only the bottom segment shares a baseline.",
        "A bar's <strong>baseline must be zero</strong>. Length encodes value, so a truncated axis misstates the ratios.",
    ],
    '''
title: Bar Charts
intro: Vertical, horizontal, grouped and stacked, and why the baseline has to be zero.

## bar and barh

`ax.bar(categories, values)` draws vertical bars; `ax.barh` draws horizontal ones.

For categorical data, **horizontal is usually better**, and the reason is typography: category labels are words, words are wide, and a vertical chart has only a bar's width in which to put each one. The usual workarounds &mdash; rotating labels 45 degrees, truncating them, shrinking the font &mdash; all make the chart harder to read.

`barh` gives every label a full line of horizontal space, reading left to right like text.

Vertical bars remain right when the x axis is ordered and quantitative-ish: months, years, bins of a distribution. There the order carries meaning and the labels are short.

## Sorting

Bar charts are read by comparing lengths, and comparison is much easier when the bars are ordered.

Unless the category order means something &mdash; months, sizes, a fixed scale &mdash; sort by value. It costs one line with `np.argsort` and changes the chart from something to be studied into something to be glanced at.

With `barh`, note that bars are drawn from the bottom up, so sorting **ascending** puts the largest bar at the top, which is where the eye starts.

## Labelling

`ax.bar_label(bars)` writes each bar's value at its end. It takes the container returned by `bar` or `barh`, which is why that return value is worth keeping here.

`fmt="%.1f"` controls the format; `labels=[...]` replaces the text entirely, which is how you show percentages or add units.

Once the values are on the bars, the value axis is usually redundant. Removing it &mdash; `ax.set_xticks([])` and hiding the spines &mdash; leaves a chart that is quieter and easier to read. This is one of the few cases where deleting a standard chart element is almost always an improvement.

## Grouped bars

There is no grouped-bar function. You compute the positions.

The pattern is: take `x = np.arange(n_groups)`, choose a bar width `w`, and offset each series by a fraction of it. For two series, `x - w/2` and `x + w/2`. For three, `x - w`, `x`, `x + w`.

Then `ax.set_xticks(x)` and `ax.set_xticklabels(groups)` put one label in the middle of each cluster, because the default ticks would otherwise fall on the individual bars.

Keep the total width of a group below 1 so there is a gap between clusters &mdash; a group of three bars of width 0.25 leaves 0.25 of space, which reads well.

Beyond three or four series per group, the chart stops working, and small multiples are the better answer.

## Stacked bars

`bottom=` gives the starting height of each segment, so each call passes the cumulative sum of everything below it.

Stacking answers one question well &mdash; what is the total &mdash; and another badly. Only the **bottom** segment sits on a common baseline, so only it can be compared across bars by eye. Segments higher up float at different heights, and comparing them is genuinely hard.

So: stack when the total is the message and the breakdown is context. Group when the components are the message. And if the question is really about proportions, a 100% stacked bar &mdash; each column normalised to 1 &mdash; answers it better than either.

## The zero baseline

This is the one rule about bar charts that is not a matter of taste.

A bar represents its value by **length**. If the axis starts at 97, a bar of value 98 has one unit of length and a bar of value 102 has five, so the chart shows a five-fold difference where the data has a 4% one.

Line charts do not have this problem, because a line encodes value by **position**, and position is read against the axis labels. That is why truncating a line chart's y axis is acceptable and truncating a bar chart's is not.

matplotlib will happily let you do it, and it happens by accident whenever `set_ylim` is applied to a bar chart to "zoom in".

If the differences are genuinely small and genuinely interesting, the answer is a different chart &mdash; a line, a dot plot, or a chart of the differences themselves &mdash; not a truncated bar.

## Width and spacing

`width` is in data units, and the default of 0.8 leaves a fifth of the spacing as a gap.

Setting it to 1.0 removes the gaps entirely, which turns a bar chart into something that reads like a histogram &mdash; and that is exactly the distinction the gap communicates. Bars with gaps say "these are separate categories"; bars without say "these are adjacent intervals of a continuous variable".

That is why a histogram has no gaps and a category chart does, and why removing the gap from a category chart is a small lie.

For grouped bars, the arithmetic is: total group width below 1, divided by the number of series. Three series of width 0.27 occupy 0.81 and leave a fifth of a unit between clusters.

## Colour on bars

A bar chart usually needs **one** colour. The categories are already distinguished by position and label, so colouring each bar differently adds nothing and implies a grouping that is not there.

The exception is highlighting: one bar in a strong colour and the rest in grey says which category the chart is about, and is far more effective than an annotation.

```python
colors = ["0.75"] * len(names)
colors[focus] = "crimson"
ax.barh(names, values, color=colors)
```

Colour becomes meaningful again when it encodes a second variable &mdash; above or below target, positive or negative &mdash; and then two colours, not seven.

## Negative values

Bars extending below zero are drawn automatically, and the baseline should be made visible:

```python
ax.axhline(0, color="black", linewidth=0.8)
```

Without it, the zero line is implied by the axis and easy to lose.

Colouring by sign is the standard treatment, and it is one of the few cases where two colours on one series is right:

```python
colors = ["#2a9d8f" if v >= 0 else "#e76f51" for v in values]
```

For a diverging bar chart &mdash; change from a baseline &mdash; sorting by value puts the largest increases and decreases at the two ends, which is usually the most readable arrangement.

## Bars for parts of a whole

A stacked bar normalised so each column sums to 100% answers "what is the composition" better than either a pie or an ordinary stack.

```python
shares = counts / counts.sum(axis=0)
```

Each segment is then a proportion, the columns are directly comparable, and the total &mdash; which is no longer shown &mdash; can go in the axis label or an annotation if it matters.

The remaining weakness is the same as any stack: only the bottom and top segments have a fixed baseline, so middle categories are hard to compare across columns. Ordering the categories so the ones being compared are at the bottom mitigates it.

## Bars are not always right

Two cases where the default choice is wrong.

**Small differences.** A bar's message is its length, and length must be read from zero. If the interesting differences are 2% of the value, a bar chart cannot show them honestly &mdash; a dot plot, or a chart of the differences, can.

**Many categories.** Forty bars is a wall. Sorting helps, and beyond about twenty a dot plot or a lollipop chart uses far less ink per category and stays readable.

`ax.hlines` plus `ax.scatter` builds a lollipop in two lines, and it is often the better display for a long ranked list.

## Labels on and around bars

`ax.bar_label` handles the common case, and its arguments cover most of the rest.

`padding=3` sets the gap in points. `fmt="%.1f%%"` formats. `label_type="center"` puts the value inside the bar rather than beyond its end, which suits stacked segments where there is no free space at the tip.

For stacked bars, calling it once per container labels each segment:

```python
for container in ax.containers:
    ax.bar_label(container, label_type="center", fmt="%.0f")
```

Small segments produce overlapping labels, so filtering to the ones with room is usually necessary &mdash; `labels=[v if v > threshold else "" for v in values]`.

Once values are on the bars, removing the value axis entirely makes the chart quieter and loses nothing.

## The bar chart checklist

Before a bar chart is finished:

**Is it sorted?** Unless the order means something.

**Is it horizontal?** Unless the labels are short or the axis is ordered.

**Does it start at zero?** Always, for bars.

**Is there one colour?** Unless colour encodes something, or one bar is highlighted.

**Are the values labelled?** If so, is the axis now redundant?

**Are there too many bars?** Past about twenty, a dot plot reads better.

**Is the gap between bars visible?** It is what says these are categories rather than intervals.

Seven questions, and a chart that answers all of them well is close to as good as a bar chart gets.

## In summary

Horizontal, sorted, one colour, from zero.

That covers most bar charts, and each part has a reason: horizontal because category labels are words, sorted because the reader should not have to rank them, one colour because position already distinguishes the categories, and from zero because a bar encodes value as length.

`bar_label` puts the numbers on the bars, which often makes the value axis redundant.

Grouped bars need the offsets computed by hand; stacked bars need `bottom` and hide everything above the first segment.

And past about twenty categories, a dot plot or lollipop chart uses far less ink and stays readable, which is worth reaching for rather than shrinking the bars further.

## Bars over time

Bars and lines both show a quantity over time, and the choice says something.

A **line** implies continuity: the quantity existed between the observations and moved smoothly. Right for a measurement sampled repeatedly &mdash; a temperature, a price, a running total.

**Bars** imply discreteness: each period is a separate quantity, and there is nothing between them. Right for a total per period &mdash; monthly revenue, daily counts, quarterly headcount.

Most business time series are period totals and are drawn as lines out of habit. The bar version is frequently more honest and reads no worse.

Two practical points. Bars need the zero baseline, which limits how much detail can be shown when the variation is small relative to the level. And with many periods bars become too thin to read, at which point a line or a step is the practical choice regardless of the semantics.

A step plot is the compromise: discrete like bars, compact like a line.

## One more thing

`ax.barh` draws from the bottom up, so a list passed in ascending order appears with the largest at the top.

That is usually what you want and is the opposite of the intuition from `bar`, where ascending order puts the largest on the right. Sorting ascending and letting `barh` reverse it visually is the idiom.

## The short version

Horizontal, sorted, one colour, from zero &mdash; four defaults that fix most bar charts before anything else is considered.

The zero baseline is the only rule here that is not a matter of taste, because a bar encodes value as length and a truncated axis misstates every ratio on the chart.

## Reading the code back

A bar chart is one call and a handful of decisions made before it: which orientation, what order, one colour or two, whether the values go on the bars, and whether the axis is then needed at all. Those decisions are all made in the data preparation and the argument list rather than in anything clever, which is why bar charts are quick to produce well once the defaults are settled and quick to produce badly when they are not.
''',
    [
        {"q": "Why is `barh` usually better for categorical data?",
         "options": ["It is faster", "Category labels are words, and horizontal bars give each label a full line to sit on", "It uses less ink", "Vertical bars are deprecated"],
         "answer": 1,
         "why": "The alternatives - rotating, truncating, shrinking - all make the chart harder to read."},
        {"q": "How do you draw grouped bars?",
         "options": ["ax.bar(grouped=True)", "Offset the positions yourself and set_xticks to centre the labels", "Use barh", "Stack them"],
         "answer": 1,
         "why": "There is no grouped-bar function. Keep a group's total width below 1 so clusters stay separated."},
        {"q": "What does stacking show badly?",
         "options": ["The total", "The components - only the bottom segment shares a baseline across bars", "The categories", "The colours"],
         "answer": 1,
         "why": "Stack when the total is the message; group when the components are. For proportions, normalise each column to 1."},
        {"q": "Why must a bar chart's axis start at zero, when a line chart's need not?",
         "options": ["Convention", "A bar encodes value as length, and length from a non-zero base is not proportional to the value", "matplotlib requires it", "It does not"],
         "answer": 1,
         "why": "A line encodes value as position, read against the axis labels, so truncating it is acceptable."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Histograms
# ---------------------------------------------------------------------------
topic(
    "histograms",
    "Histograms and Distributions",
    "Drawing",
    "hist() and the bin count that changes what the data appears to say.",
    _svg(_box(14, 16, 132, 58, "none", B) +
         '<rect x="28" y="60" width="12" height="12" fill="%s"/>'
         '<rect x="42" y="44" width="12" height="28" fill="%s"/>'
         '<rect x="56" y="28" width="12" height="44" fill="%s"/>'
         '<rect x="70" y="34" width="12" height="38" fill="%s"/>'
         '<rect x="84" y="50" width="12" height="22" fill="%s"/>'
         '<rect x="98" y="64" width="12" height="8" fill="%s"/>' % ((A,) * 6)),
    [
        ("hist counts values into bins",
         "And returns the counts and edges, which are often worth keeping.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
data = rng.normal(loc=50, scale=12, size=800)

fig, ax = plt.subplots(figsize=(6, 3))
counts, edges, patches = ax.hist(data, bins=20, edgecolor="white")

print("bins requested :", 20)
print("counts         :", len(counts), "values")
print("edges          :", len(edges), "<- one more than the counts")
print()
print("first three bins: %s to %s -> %d" % (round(edges[0], 1), round(edges[1], 1), counts[0]))
print("                  %s to %s -> %d" % (round(edges[1], 1), round(edges[2], 1), counts[1]))
print()
print("Edges outnumber counts by one, because n bins have n+1 boundaries.")'''),

        ("The bin count changes the story",
         "Too few hides structure; too many turns it into noise.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
data = np.concatenate([rng.normal(30, 5, 400), rng.normal(60, 5, 400)])

fig, axes = plt.subplots(1, 4, figsize=(10, 2.6), sharey=True)
for ax, b in zip(axes, [3, 12, 50, 300]):
    ax.hist(data, bins=b, edgecolor="white", linewidth=0.3)
    ax.set_title("bins=%d" % b)

print("The data is genuinely two peaks at 30 and 60.")
print("   3 bins  : one lump - the structure is gone")
print("  12 bins  : both peaks visible")
print("  50 bins  : still clear, more ragged")
print(" 300 bins  : noise; most bins hold 0-5 points")
print()
print("There is no correct answer, which is why looking at two or three")
print("is more honest than trusting one.")'''),

        ("Letting numpy choose",
         "<code>bins=\"auto\"</code> applies a rule of thumb rather than a guess.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(2)
data = rng.normal(size=2000)

fig, ax = plt.subplots(figsize=(6, 3))
counts, edges, _ = ax.hist(data, bins="auto", edgecolor="white")

for rule in ["auto", "sturges", "fd", "scott", "sqrt"]:
    n = len(np.histogram_bin_edges(data, bins=rule)) - 1
    print("%-8s -> %3d bins" % (rule, n))
print()
print("'auto' takes the larger of the Freedman-Diaconis and Sturges")
print("rules. They disagree, which is the honest summary of the problem.")'''),

        ("density instead of counts",
         "Needed to compare groups of different sizes, or to overlay a curve.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
small = rng.normal(0, 1, 200)
large = rng.normal(0, 1, 5000)

fig, (a, b) = plt.subplots(1, 2, figsize=(8, 3))

a.hist(small, bins=25, alpha=0.6, label="n=200")
a.hist(large, bins=25, alpha=0.6, label="n=5000")
a.set_title("counts - incomparable")
a.legend()

b.hist(small, bins=25, density=True, alpha=0.6, label="n=200")
b.hist(large, bins=25, density=True, alpha=0.6, label="n=5000")
b.set_title("density - comparable")
b.legend()

print("Same distribution, different sample sizes.")
print("Counts say the big sample is 25x more likely everywhere.")
print("density=True makes the total area 1, so the shapes overlay.")'''),

        ("Comparing groups",
         "Overlaid with transparency, or side by side - both have costs.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(4)
a_data = rng.normal(45, 8, 600)
b_data = rng.normal(55, 8, 600)

fig, (p, q) = plt.subplots(1, 2, figsize=(9, 3))

p.hist([a_data, b_data], bins=20, label=["a", "b"])
p.set_title("side by side")
p.legend()

q.hist(a_data, bins=20, alpha=0.55, label="a")
q.hist(b_data, bins=20, alpha=0.55, label="b")
q.set_title("overlaid, alpha")
q.legend()

print("A list of arrays draws them side by side within each bin.")
print("Separate calls with alpha overlays them.")
print()
print("Side by side keeps both readable and halves the bin width.")
print("Overlaid keeps the bins but muddles the overlap colour.")
print("For more than three groups, neither works - use small multiples.")'''),

        ("The cumulative view answers different questions",
         "'How many are below x' is easier to read from a step than from bars.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(5)
data = rng.normal(100, 15, 2000)

fig, (a, b) = plt.subplots(1, 2, figsize=(8, 3))

a.hist(data, bins=30, edgecolor="white")
a.set_title("distribution")

b.hist(data, bins=200, density=True, cumulative=True,
       histtype="step", linewidth=2)
b.set_title("cumulative")
b.axhline(0.5, color="crimson", linestyle="--", linewidth=1)

print("median of the data: %.1f" % np.median(data))
print()
print("The cumulative plot reads off quantiles directly: where the")
print("curve crosses 0.5 is the median, 0.9 the 90th percentile.")
print("It also does not depend much on the bin count, which is why")
print("many bins is fine here and misleading on the left.")'''),
    ],
    [
        "<code>hist</code> returns <code>counts, edges, patches</code>; there is always <strong>one more edge than count</strong>.",
        "The <strong>bin count changes the apparent shape</strong> &mdash; too few hides structure, too many turns it into noise. Look at two or three.",
        "<code>bins=\"auto\"</code> applies a rule rather than a guess; the rules disagree, which is an honest summary of the problem.",
        "<code>density=True</code> makes the area sum to 1, which is what lets samples of different sizes be compared.",
        "A <strong>list of arrays</strong> draws groups side by side; separate calls with <code>alpha</code> overlays them.",
        "A <code>cumulative</code> step plot reads off quantiles directly and barely depends on the bin count.",
    ],
    '''
title: Histograms and Distributions
intro: hist() and the bin count that changes what the data appears to say.

## What it returns

`ax.hist(data, bins=20)` returns `counts, edges, patches`.

`counts` has one entry per bin. `edges` has **one more**, because n bins are defined by n+1 boundaries. That off-by-one is the usual confusion when using the return values, and it is the same convention `np.histogram` follows.

`patches` is the collection of rectangles, kept if you want to recolour particular bars &mdash; highlighting a threshold, for instance.

`edgecolor="white"` is worth adding almost always: without it, adjacent bars merge into a single shape and the bin structure disappears.

## Bins decide the story

This is the thing to understand about histograms, and it is not a detail.

The same data with three bins and with three hundred looks like two different datasets. Too few bins smooths away real structure &mdash; a bimodal distribution becomes one lump. Too many turns sampling noise into apparent spikes.

There is no correct number. It depends on the sample size, the underlying shape, and what you are trying to see.

The honest practice is to **look at more than one**. If a feature survives at several bin counts, it is probably real; if it appears only at one, it is probably not.

## The automatic rules

`bins="auto"` uses the larger of two rules:

**Sturges** assumes roughly normal data and scales with `log2(n)`.

**Freedman&ndash;Diaconis** uses the interquartile range and scales with `n^(1/3)`, which handles skew and outliers better.

`"scott"`, `"sqrt"` and `"rice"` are also available. They disagree with each other, sometimes by a factor of several, which is a fair summary of how well-defined the problem is.

`"auto"` is a reasonable default and a starting point rather than an answer.

You can also pass explicit edges: `bins=np.arange(0, 101, 5)` gives fixed 5-unit bins, which is what you want when the boundaries have meaning or when two charts must be comparable.

## density

`density=True` scales the bars so the **total area** is 1 rather than showing raw counts.

Two situations need it.

**Comparing samples of different sizes.** With counts, a sample ten times larger has bars ten times taller everywhere, and the shapes cannot be compared. With density they overlay.

**Overlaying a theoretical curve.** A normal PDF is a density, and it only lines up with a histogram that is also a density.

Note the y axis then reads as density, not proportion, and the values can exceed 1 when the bins are narrow. The area is 1; the height is not a probability.

## Comparing groups

`ax.hist([a, b], bins=20)` &mdash; a list of arrays &mdash; draws them side by side within each bin. Both stay readable, at the cost of halving the effective bin width.

Separate `hist` calls with `alpha` around 0.5 overlay them. The bins keep their width, and the overlap region becomes a blended colour that belongs to neither series.

`histtype="step"` draws outlines only, which overlays cleanly for three or four groups where filled bars would not.

Beyond three groups, none of these work well, and the answer is small multiples: one histogram per group, sharing axes, side by side.

## The cumulative view

`cumulative=True` with `histtype="step"` draws an empirical cumulative distribution.

It answers "what fraction is below x" directly, which is often the actual question &mdash; and quantiles read straight off it, where they must be estimated by eye from a histogram.

It has a further practical advantage: it barely depends on the bin count. Using two hundred bins gives a smooth curve rather than noise, because each bin adds to a running total rather than standing alone. That makes it the more honest display when the bin choice is doing too much work.

## Related displays

`ax.boxplot` summarises a distribution as five numbers, which compares many groups compactly and hides the shape entirely &mdash; a bimodal distribution and a uniform one can produce the same box.

`ax.violinplot` shows an estimated density, which restores the shape at the cost of a smoothing parameter that has the same arbitrariness as the bin count.

`ax.hexbin` and `ax.hist2d` are the two-dimensional versions, for when the question is about the joint distribution rather than a single variable.

## Bin edges you choose

Passing a count lets matplotlib pick the edges, which land on unmemorable numbers like 3.17 to 7.42.

Passing an array puts them where you want:

```python
ax.hist(ages, bins=np.arange(0, 101, 10))
```

Ten-year bands, starting at zero, with boundaries a reader can name. That is almost always better for communication, and it has a second benefit: two histograms drawn with the same explicit edges are directly comparable, where two drawn with `bins=20` are not.

`range=(lo, hi)` limits the extent without fixing the count, which is how you exclude a long tail without dropping the data.

Values exactly on a boundary go into the **right-hand** bin, except at the last edge where the final bin includes both ends.

## Weights

`weights=` gives each observation a multiplier, which covers two common needs.

**Frequency data** &mdash; when the input is already counts per value rather than raw observations.

**Percentages** &mdash; `weights=np.ones(n) / n * 100` makes the y axis read as a percentage of the sample, which is often more useful than either counts or density and is easier to explain than density.

Density has the awkward property that its values depend on the bin width and can exceed 1; a percentage does not.

## Two-dimensional histograms

`ax.hist2d(x, y, bins=50)` bins in both directions and colours the cells by count. `ax.hexbin` does the same with hexagonal bins, which tile more evenly and avoid the visual artefacts of a square grid.

Both replace an overplotted scatter with something that measures density instead of implying it, and both need a colorbar to be readable.

`bins="log"` on hexbin, or `norm=LogNorm()`, handles the usual situation where a few cells hold most of the points and everything else is faint.

## Step histograms for comparison

`histtype="step"` draws the outline only. `histtype="stepfilled"` fills it with transparency.

For comparing three or four distributions, outlines overlay far more cleanly than filled bars: nothing is hidden, and the colours do not blend into a fourth colour that belongs to no series.

Combined with `density=True` it is the standard way to compare distributions of different sizes on one axes.

Beyond four, small multiples remain the answer.

## What a histogram cannot show

A histogram shows a marginal distribution and nothing else.

It cannot show a relationship between two variables, a change over time, or an ordering within the data. Two datasets with identical histograms can be completely different, in the same way that two datasets with identical means can be.

The specific thing it hides is **sequence**: a series that drifts upward over time and one that is stationary produce the same histogram. If the data has an order, a line chart of the values and a histogram of them answer different questions, and the histogram alone can conceal a trend entirely.

## Choosing the bins in practice

A workable procedure, rather than a rule.

Start with `bins="auto"` and look at it. Then try roughly half and roughly double that number and look at those.

If the three agree about the shape, the shape is real and any of them will do; pick round-numbered edges for the final version.

If they disagree, the disagreement is the finding &mdash; there is structure at one scale and not another &mdash; and the chart should show the bin count that corresponds to the question being asked.

For a chart that will be compared with another, fix the edges explicitly with an array. Two histograms with automatically chosen bins are not comparable even when they look it, because the bin widths differ.

And for anything above a few thousand points, a cumulative plot or a density estimate sidesteps the choice entirely, which is often the honest move.

## Related displays, and when to switch

A histogram is one of a family, and it is not always the strongest member.

**Cumulative** &mdash; when the question is about quantiles or thresholds, and to escape the bin-count problem.

**Box plots** &mdash; when comparing more than three groups.

**Violin or KDE** &mdash; when the shape matters and the sample is large.

**Strip plot** &mdash; when the sample is small enough that the observations are the honest display.

**Rug plot** &mdash; tick marks along the axis, added under any of the above, which shows exactly where the data is without a binning choice.

`ax.plot(x, np.zeros_like(x), "|", markersize=12, alpha=0.3)` draws a rug in one line, and combining it with a histogram gives both the shape and the raw positions.

## In summary

The bin count is the whole story: it decides what shape the data appears to have, there is no correct value, and looking at two or three is the only honest approach.

`bins="auto"` is a reasonable start and an argument between two rules rather than an answer.

Explicit edges make two histograms comparable, which automatically chosen bins never are.

`density=True` is what lets samples of different sizes be compared, and its y axis is a density rather than a proportion.

For several groups, side-by-side or step outlines up to three or four, and small multiples beyond that.

And the cumulative view answers quantile questions directly while barely depending on the binning &mdash; often the more honest display when the bin choice is doing too much work.

## What to check on a histogram

Four things, none of which the chart tells you.

**How many observations?** A histogram of thirty looks much like one of thirty thousand, and means far less. Putting `n` in the title or a corner is a one-line fix.

**How many bins, and does the shape survive changing it?** The single most important check.

**Is anything outside the range?** If `range=` was set, or the axis limits were, the excluded values are simply gone.

**Are the bins equal width?** With explicit edges they may not be, and unequal bins with a count axis are misleading &mdash; the area should represent the count, which is what `density=True` handles correctly and a raw count does not.

The last is a genuine trap: a histogram with wide bins at the tail and narrow ones in the middle, plotted as counts, exaggerates the tail. If the bins are unequal, density is the only honest y axis.

## One more thing

`np.histogram` computes the counts without drawing anything, which is useful when the numbers are wanted alongside the chart or when the binning needs checking before it is plotted.

It takes the same `bins` argument and returns counts and edges, so the values behind a histogram can be printed, tested, or written to a file without a second pass over the data.

## The short version

The bin count is a parameter that changes the answer, and it is chosen by default when nobody chooses it deliberately.

Looking at more than one binning, and stating which one the chart uses, is the whole of good practice here &mdash; along with knowing that a cumulative view sidesteps the problem when the question is about quantiles.

## Reading the code back

A histogram is one call whose most important argument is the one people leave out. Passing explicit edges rather than a count makes the chart comparable with another, gives boundaries the reader can name, and forces the binning to be a decision rather than a default. Adding the sample size to the title and an edge colour to the bars costs two more arguments and answers most of what a reader would ask.
''',
    [
        {"q": "Why does `hist` return one more edge than count?",
         "options": ["A bug", "n bins are defined by n+1 boundaries", "It includes a total", "It does not"],
         "answer": 1,
         "why": "The same convention np.histogram follows, and the usual off-by-one when using the return values."},
        {"q": "What is the main risk of choosing a bin count?",
         "options": ["Slow rendering", "Too few hides real structure and too many turns noise into apparent spikes", "Wrong colours", "Missing data"],
         "answer": 1,
         "why": "There is no correct number. Looking at two or three tells you which features are real - a feature that survives several bin counts probably is."},
        {"q": "Why is `density=True` needed to compare two samples of different sizes?",
         "options": ["It is faster", "With counts the larger sample has taller bars everywhere, so the shapes cannot be compared", "It fixes the bins", "It is not needed"],
         "answer": 1,
         "why": "Density makes the total area 1 so the shapes overlay. The y axis then reads as density, and can exceed 1."},
        {"q": "Why does a cumulative histogram tolerate many more bins?",
         "options": ["It is smoothed", "Each bin adds to a running total rather than standing alone, so noise does not show", "It uses fewer points", "It does not"],
         "answer": 1,
         "why": "It also reads off quantiles directly - where the curve crosses 0.5 is the median."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Labels, titles and legends
# ---------------------------------------------------------------------------
topic(
    "labels_and_legends",
    "Labels, Titles and Legends",
    "Making It Readable",
    "The text that turns a plot into something someone else can read.",
    _svg(_box(20, 24, 116, 44, "none", B) +
         _txt(78, 18, "title", A, 9) + _txt(78, 78, "x label", M, 8) +
         _box(96, 28, 34, 14, S, M) + _txt(113, 38, "legend", M, 7)),
    [
        ("The four pieces of text",
         "Title, both axis labels, and a legend when there is more than one series.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 13)
sales = [12, 15, 14, 18, 22, 25, 24, 27, 23, 20, 18, 21]

fig, ax = plt.subplots(figsize=(6.5, 3.5))
ax.plot(x, sales, marker="o", label="2024")
ax.set_title("Monthly sales")
ax.set_xlabel("Month")
ax.set_ylabel("Sales (thousands)")
ax.legend()

print("A chart without units is a chart nobody can act on.")
print("'Sales' could be rupees, units or thousands - the label says.")
print()
print("ax.set() does all of them in one call:")
print('   ax.set(title=..., xlabel=..., ylabel=...)')'''),

        ("legend needs labels to work with",
         "It reads them from the artists; without them it has nothing to show.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)

fig, (a, b) = plt.subplots(1, 2, figsize=(8, 3))

a.plot(x, np.sin(x))
a.plot(x, np.cos(x))
a.legend()                      # nothing is labelled
a.set_title("no labels")

b.plot(x, np.sin(x), label="sin")
b.plot(x, np.cos(x), label="cos")
b.legend()
b.set_title("labelled")

print("The left legend drew nothing, and matplotlib said so - look for")
print("the warning above this output, in red.")
print()
print("A label starting with an underscore is skipped deliberately -")
print("that is how you exclude a helper line from the legend:")
c = a.plot(x, np.sin(x) * 0.2, label="_helper")
print("   labels on the left axes:", [l.get_label() for l in a.lines])'''),

        ("Placing it",
         "<code>loc</code> for inside, <code>bbox_to_anchor</code> for outside.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

for k in range(3):
    a.plot(x, np.sin(x + k), label="series %d" % k)
a.legend(loc="upper right")
a.set_title("loc='upper right'")

for k in range(3):
    b.plot(x, np.sin(x + k), label="series %d" % k)
b.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)
b.set_title("outside")

print("loc takes 'best' (the default), 'upper right', 'lower left',")
print("'center', and the rest of the compass.")
print()
print("'best' searches for the emptiest corner, which costs time on a")
print("busy plot and can move between runs. Naming a corner is stabler.")'''),

        ("Legends cost the reader work",
         "Labelling the lines directly is often better.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
series = {"alpha": np.sin(x), "beta": np.sin(x) + 1.2, "gamma": np.sin(x) - 1.2}

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3.2))

for name, y in series.items():
    a.plot(x, y, label=name)
a.legend()
a.set_title("legend: eye moves back and forth")

for name, y in series.items():
    b.plot(x, y)
    b.text(x[-1] + 0.2, y[-1], name, va="center")
b.set_xlim(0, 12.5)
b.set_title("labelled at the end")

print("A legend makes the reader match a colour to a name and carry it")
print("back to the line. Direct labels remove that step entirely.")
print("It works when the lines end apart; it fails when they converge.")'''),

        ("Titles that say the finding",
         "A descriptive title labels the chart; an assertive one states what it shows.",
         '''import matplotlib.pyplot as plt
import numpy as np

months = np.arange(1, 13)
y = np.array([12, 15, 14, 18, 22, 25, 24, 27, 23, 20, 18, 21])

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3.2))

a.plot(months, y, marker="o")
a.set_title("Sales by month")

b.plot(months, y, marker="o")
b.set_title("Sales peaked in August, then fell 22%", loc="left", fontsize=11)
b.axvline(8, color="crimson", linestyle="--", linewidth=1)

print("The left title names the axes again. The right one tells the")
print("reader what to look at, and the annotation shows where.")
print()
print("loc='left' is worth knowing: a left-aligned title reads like a")
print("headline rather than a caption.")'''),

        ("Figure-level text",
         "For a grid, the labels usually belong to the figure rather than each axes.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)

fig, axes = plt.subplots(2, 2, figsize=(7, 4), sharex=True, sharey=True)
for i, ax in enumerate(axes.flat):
    ax.plot(rng.random(20).cumsum())
    ax.set_title("panel %d" % (i + 1), fontsize=9)

fig.suptitle("One title for the whole figure", fontsize=13)
fig.supxlabel("shared x label")
fig.supylabel("shared y label")
fig.tight_layout()

print("suptitle / supxlabel / supylabel belong to the FIGURE.")
print("With sharex and sharey, repeating the axis label on every panel")
print("is noise - one label for the grid says the same thing.")'''),
    ],
    [
        "Title, both axis labels and a legend are the minimum; <strong>units</strong> in the axis label are what make a number actionable.",
        "<code>legend()</code> reads labels from the artists &mdash; without <code>label=</code> it warns and shows nothing. A leading underscore excludes an artist deliberately.",
        "<code>loc</code> places a legend inside; <code>bbox_to_anchor</code> puts it outside. <code>loc=\"best\"</code> is slow on busy plots and can move between runs.",
        "<strong>Direct labels</strong> on the lines remove the colour-matching step a legend forces on the reader.",
        "A title that states the <strong>finding</strong> is more useful than one that names the axes again; <code>loc=\"left\"</code> makes it read as a headline.",
        "<code>fig.suptitle</code>, <code>supxlabel</code> and <code>supylabel</code> label a whole grid, which beats repeating the same label on every panel.",
    ],
    '''
title: Labels, Titles and Legends
intro: The text that turns a plot into something someone else can read.

## The minimum

Every chart that leaves your screen needs a title, an x label and a y label, and a legend if there is more than one series.

The axis labels carry the part people most often omit: **units**. "Sales" could be rupees, units, thousands or a percentage change, and a reader who has to guess cannot act on the chart. "Sales (&#8377; thousands)" takes four extra characters and removes the question.

`ax.set(title=..., xlabel=..., ylabel=...)` does all three in one call, which is convenient in a chain.

## legend

`ax.legend()` collects the artists on the axes that have a `label` and draws a key.

Artists without a label are skipped, and if nothing has one, matplotlib warns and draws nothing. That warning &mdash; "No artists with labels found" &mdash; is one of the most common in matplotlib and always means the same thing.

A label beginning with an underscore is **deliberately excluded**. That is the mechanism for keeping a helper artist &mdash; a threshold line, a shaded band &mdash; out of the key without giving up labelling it in code.

You can also pass the handles and labels explicitly, `ax.legend(handles, labels)`, which is how you control the order or combine artists from different axes.

## Placement

`loc` names a position: `"upper right"`, `"lower left"`, `"center"`, and the rest.

The default is `"best"`, which searches for the position overlapping the least data. That is convenient and has two costs: it is slow on a plot with many points, and it can put the legend somewhere different when the data changes, which is unwelcome in a figure you are iterating on.

For a legend outside the axes:

```python
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)
```

`bbox_to_anchor` gives a point in axes coordinates &mdash; `(1.02, 1)` is just past the right edge, at the top &mdash; and `loc` says which corner of the legend goes there. Remember to leave room, with `fig.tight_layout()` or a smaller axes, or the legend will be cut off when saved.

`ncol=3` spreads a legend horizontally, which suits one placed above or below the axes.

`frameon=False` removes the box, which usually looks cleaner over a plot with white space.

## Direct labelling

A legend asks the reader to match a colour to a name, hold it in memory, and find the corresponding line. That is real cognitive work, repeated for every series.

Labelling each line at its end removes the step:

```python
ax.text(x[-1] + 0.2, y[-1], name, va="center")
```

It works well when the lines end at different heights, which is common in time series. It fails when they converge, and then a legend is the honest choice.

This is one of the highest-value small improvements available to a line chart, and matplotlib has no built-in for it &mdash; two lines of `text` is the whole implementation.

## Titles that say something

The default habit is a title that names the variables: "Sales by month". The chart already shows that; the axis labels already say it.

A more useful title states the **finding**: "Sales peaked in August, then fell 22%". The reader then knows what they are looking for, and the chart supports the claim rather than posing a question.

`loc="left"` left-aligns the title, which makes it read like a headline rather than a caption. Combined with a slightly larger font and a subtitle in smaller grey text, it is the layout most publications use, and it is a few lines of matplotlib.

Annotating the thing the title mentions &mdash; a vertical line at the peak, a highlighted point &mdash; closes the loop between the words and the picture.

## Figure-level text

With a grid of subplots sharing axes, repeating the same axis label on every panel is noise.

`fig.supxlabel`, `fig.supylabel` and `fig.suptitle` attach text to the figure instead, so one label serves the whole grid.

`fig.tight_layout()` afterwards makes room for them; without it, a suptitle frequently overlaps the top row of panels.

## Text properties

Every text-producing method takes the same styling arguments: `fontsize`, `fontweight`, `color`, `family`, `style`, `alpha`, `rotation`.

A small set of conventions covers most charts:

**Title** &mdash; larger, bold, left-aligned. It is a headline.

**Axis labels** &mdash; default size, sentence case, with units.

**Tick labels** &mdash; smaller and lighter than the data, because they are reference rather than content.

**Annotations** &mdash; the colour of the thing they annotate, which ties them together without an arrow.

`plt.rcParams` holds defaults for all of these &mdash; `axes.titlesize`, `axes.labelsize`, `xtick.labelsize` &mdash; so a house style sets them once rather than per chart.

## Legend contents

`ax.legend()` takes arguments that solve most legend problems.

`ncol=3` spreads it horizontally, which suits a legend above or below the axes and wastes far less vertical space than a single column.

`title="Region"` labels the legend itself, which removes the need to explain the categories elsewhere.

`frameon=False` drops the box. `framealpha=0.8` keeps it but lets the data show through.

`fontsize="small"` shrinks it, appropriate because a legend is reference material rather than content.

`handles` and `labels` given explicitly control both the order and the contents &mdash; how you put the series in the same vertical order they appear on the chart, which makes the mapping obvious.

## Mathematical text

Any text argument accepts mathtext between dollar signs:

```python
ax.set_ylabel(r"Energy ($\mathrm{J\,m^{-2}}$)")
```

The `r` prefix matters, because backslashes are otherwise interpreted by Python before matplotlib sees them.

This is a built-in subset of LaTeX and needs no LaTeX installation. `rcParams["text.usetex"] = True` switches to a real LaTeX renderer for full support, at the cost of requiring LaTeX to be present and slowing rendering considerably.

For units, superscripts and Greek letters &mdash; which is most scientific labelling &mdash; mathtext is enough.

## Multi-line and wrapped text

A long title can be broken with a newline, and the alignment applies to the block:

```python
ax.set_title("A longer headline that\nruns to two lines", loc="left")
```

`linespacing=` adjusts the gap.

A common publication pattern is a bold headline and a lighter subtitle:

```python
ax.set_title("Sales peaked in August", loc="left", fontsize=13, fontweight="bold")
ax.text(0, 1.02, "Monthly, 2024, thousands", transform=ax.transAxes,
        fontsize=9, color="0.4")
```

Two lines, and the chart reads like something published rather than something exported.

## Labels that fix themselves

The most robust label is one computed from the data rather than typed:

```python
ax.set_title("Peak %s: %.0f" % (months[i], y[i]))
ax.legend(title="n = %d" % len(df))
```

A hard-coded number in a title is wrong the first time the data changes, and nothing will tell you. Deriving it means the chart cannot disagree with itself &mdash; which matters most for exactly the charts that get regenerated regularly.

## Where the reader looks

Text placement is not only about fitting; it is about the order things are read.

The **title** is read first, so it should carry the message.

The **direct labels** on the data are read next, if they exist, which is why they beat a legend.

The **axis labels** are consulted when a value needs interpreting.

The **legend** is consulted repeatedly, which is the cost that direct labels remove.

A **caption or source note** is read last, if at all, and belongs in small grey text at the bottom.

Designing in that order &mdash; message, then data labels, then reference material &mdash; produces a chart that can be understood at a glance and interrogated afterwards, which is what a good chart does.

## Common labelling errors

**No units.** The single most common omission, and the one that makes a chart unusable.

**A title that repeats the axes.** "Sales by month" over a chart with "Month" and "Sales" on the axes says nothing new.

**A legend with no title**, where the categories need explaining.

**Labels rotated 45 degrees** when `barh` would have avoided rotation entirely.

**Text that overlaps the data**, with no background box.

**A hard-coded number in the title** that no longer matches the data.

**A legend in `loc="best"`** that moves between runs, making two versions of a figure hard to compare.

All are cheap to fix and all survive into published charts regularly.

## In summary

Title, both axis labels with units, and a legend when there is more than one series &mdash; that is the minimum, and units are the part most often missing.

`legend()` reads labels from the artists, warns when there are none, and skips anything whose label starts with an underscore.

Direct labels on the lines remove the colour-matching a legend imposes, and are worth the two lines of `text` they cost.

A title that states the finding is more useful than one naming the variables, and `loc="left"` makes it read as a headline.

For a grid, `fig.suptitle` and `supxlabel` replace repeating the same label on every panel.

And any number in a label should be computed from the data, because a hard-coded one is wrong the first time the data changes and nothing will say so.

## Writing the title

The title is the most valuable text on a chart and the most often wasted.

Three levels, in increasing usefulness:

**Descriptive** &mdash; "Sales by month". Names the variables the axes already name. Adds nothing.

**Specific** &mdash; "Monthly sales, 2024, all regions". Adds scope, which the reader needs, and belongs in a subtitle rather than the headline.

**Assertive** &mdash; "Sales peaked in August, then fell 22%". States what the chart shows, so the reader knows what to look for and can check the claim against the picture.

The assertive form has a discipline attached: having written it, you have to make sure the chart supports it. That is a useful constraint, and it frequently changes the chart &mdash; highlighting August, annotating the fall, removing series that are not part of the claim.

Where a chart genuinely has no single finding &mdash; an exploratory panel, a reference figure &mdash; the specific form is right, and the absence of a claim is itself informative.

## Subtitles and source notes

Two pieces of text that most charts want and matplotlib has no method for.

A **subtitle** carries the scope that the headline title leaves out &mdash; the period, the units, the population. Placed just under the title in axes coordinates, smaller and grey:

```python
ax.text(0, 1.02, "Monthly, 2024, all regions", transform=ax.transAxes,
        fontsize=9, color="0.4", va="bottom")
```

A **source note** goes at the bottom of the figure, smaller still:

```python
fig.text(0, 0, "Source: internal sales data, extracted 2024-09-01",
         fontsize=8, color="0.5", va="bottom")
```

Both are two lines and both are what makes a chart usable by someone who did not make it. The source note in particular is the difference between a chart that can be checked and one that has to be taken on trust.

## One more thing

`ax.legend(labelcolor="linecolor")` colours each legend label to match its line, which removes the need for the swatch entirely and reads well with `handlelength=0`.

It is a compact treatment that sits between a full legend and direct labelling, and works when the lines converge so that end labels would overlap.

## The short version

Text is what turns a picture of numbers into something someone else can act on, and units are the part most often left out.

A legend is reference material that the reader consults repeatedly; a direct label is read once. Where the lines end apart, the direct label wins, and it costs two lines of `text`.

## Reading the code back

The text on a chart is written in a fixed order: the title says what was found, the axis labels say what the numbers are, and the legend or the direct labels say which series is which. Written in that order, the chart is complete; written in any other, something is usually missing. The most common omission is units, and the most common redundancy is a title that repeats the axis names.
''',
    [
        {"q": "What does `ax.legend()` do when no artist has a label?",
         "options": ["Shows all series", "Warns and draws nothing", "Raises", "Numbers them"],
         "answer": 1,
         "why": "'No artists with labels found' is one of the most common matplotlib warnings and always means this."},
        {"q": "How do you keep a helper line out of the legend?",
         "options": ["Draw it last", "Give its label a leading underscore", "Use alpha", "You cannot"],
         "answer": 1,
         "why": "A deliberate mechanism, so a threshold line can be labelled in code without appearing in the key."},
        {"q": "What is the drawback of `loc='best'`?",
         "options": ["It is ugly", "It is slow on busy plots and can move when the data changes", "It only works on lines", "It is deprecated"],
         "answer": 1,
         "why": "Naming a corner is more stable, which matters in a figure you are iterating on."},
        {"q": "Why is 'Sales peaked in August, then fell 22%' a better title than 'Sales by month'?",
         "options": ["It is longer", "It states the finding, so the reader knows what to look for", "It includes a number", "It is not better"],
         "answer": 1,
         "why": "The axis labels already say what the variables are. loc='left' makes such a title read as a headline."},
    ],
)


# ---------------------------------------------------------------------------
# 7. Axis limits and ticks
# ---------------------------------------------------------------------------
topic(
    "axis_limits_and_ticks",
    "Limits, Ticks and Scales",
    "Making It Readable",
    "Controlling what the axis shows and how it is written - and the log scale "
    "that makes a curve readable.",
    _svg(_box(24, 20, 112, 48, "none", B) +
         _txt(24, 78, "0", M, 7) + _txt(52, 78, "25", M, 7) +
         _txt(80, 78, "50", M, 7) + _txt(108, 78, "75", M, 7) +
         _txt(136, 78, "100", M, 7)),
    [
        ("Limits",
         "Set them to focus, and know what you are hiding.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 200)
y = np.sin(x) + 0.1 * x

fig, (a, b) = plt.subplots(1, 2, figsize=(8, 3))

a.plot(x, y)
a.set_title("automatic")

b.plot(x, y)
b.set_xlim(2, 6)
b.set_ylim(0, 2)
b.set_title("set_xlim / set_ylim")

print("automatic limits:", [round(v, 2) for v in a.get_xlim()])
print("   note they are wider than the data - matplotlib adds a margin")
print()
print("ax.margins(0) removes it; ax.set_xlim(x.min(), x.max()) does too.")
print()
print("Reversing an axis is just giving the limits backwards:")
print("   ax.set_ylim(top, bottom)")'''),

        ("Where the ticks go",
         "<code>set_xticks</code> for positions, and a second argument for the labels.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(12)
y = np.random.default_rng(0).random(12).cumsum()
months = ["jan", "feb", "mar", "apr", "may", "jun",
          "jul", "aug", "sep", "oct", "nov", "dec"]

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.plot(x, y)
a.set_title("default ticks: 0, 2, 4 ...")

b.plot(x, y)
b.set_xticks(x[::2])
b.set_xticklabels([months[i] for i in x[::2]])
b.set_title("named ticks")

print("set_xticks decides the positions; set_xticklabels the text.")
print()
print("Setting labels WITHOUT setting positions is the classic bug:")
print("matplotlib keeps its own tick positions and relabels them, so")
print("the labels end up on the wrong values.")'''),

        ("Formatting tick labels",
         "A formatter changes how numbers are written without changing them.",
         '''import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

x = np.arange(2015, 2025)
y = np.linspace(1.2e6, 4.8e6, 10)

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.plot(x, y)
a.set_title("default: scientific offset")

b.plot(x, y)
b.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: "%.1fM" % (v / 1e6)))
b.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:.0f}"))
b.set_title("formatted")

print("Large numbers get an offset like '1e6' tucked in a corner,")
print("which readers miss. A formatter puts the unit on every label.")
print()
print("FuncFormatter takes (value, position) and returns a string.")
print("PercentFormatter, StrMethodFormatter and EngFormatter cover")
print("most of the rest without writing a function.")'''),

        ("Log scale",
         "For data spanning orders of magnitude, a linear axis shows one thing only.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 11)
y = 2.0 ** x

fig, (a, b) = plt.subplots(1, 2, figsize=(8, 3))

a.plot(x, y, marker="o")
a.set_title("linear: the first 7 are flat")

b.plot(x, y, marker="o")
b.set_yscale("log")
b.set_title("log: a straight line")

print("y goes from 2 to 1024.")
print("On a linear axis the small values are indistinguishable from zero.")
print("On a log axis, exponential growth is a straight line - which is")
print("the point: the shape tells you the growth is exponential.")
print()
print("Log needs positive values. A zero or negative silently drops out.")'''),

        ("Symlog and other scales",
         "When the data crosses zero, or is a proportion.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-100, 100, 400)
y = x ** 3

fig, (a, b) = plt.subplots(1, 2, figsize=(8, 3))

a.plot(x, y)
a.set_yscale("symlog", linthresh=100)
a.set_title("symlog: log either side of 0")

p = np.linspace(0.001, 0.999, 200)
b.plot(p, p / (1 - p))
b.set_yscale("log")
b.set_title("odds on a log axis")

print("symlog is logarithmic away from zero and linear near it, so it")
print("handles data that crosses zero. linthresh sets where it switches.")
print()
import matplotlib.scale as mscale
print("registered scales:", ", ".join(sorted(mscale.get_scale_names())))'''),

        ("Grids and spines",
         "The lines that help, and the ones that only take up ink.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(10)
y = np.random.default_rng(1).random(10).cumsum()

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.plot(x, y, marker="o")
a.grid(True)
a.set_title("default grid, all spines")

b.plot(x, y, marker="o")
b.grid(True, axis="y", alpha=0.4, linewidth=0.8)
b.spines["top"].set_visible(False)
b.spines["right"].set_visible(False)
b.set_title("quieter")

print("A grid is for reading values off the chart. If nobody will do")
print("that, it is decoration - and a faint one on one axis is usually")
print("enough when they will.")
print()
print("The top and right spines enclose the plot and carry no")
print("information. Removing them is the cheapest visual improvement")
print("matplotlib offers.")'''),
    ],
    [
        "matplotlib adds a <strong>margin</strong> beyond the data; <code>ax.margins(0)</code> or explicit limits remove it. Reversing an axis is giving the limits backwards.",
        "<code>set_xticks</code> sets positions and <code>set_xticklabels</code> the text &mdash; setting labels <em>without</em> positions puts them on the wrong values.",
        "A <strong>formatter</strong> changes how numbers are written. Large values otherwise get a <code>1e6</code> offset in the corner that readers miss.",
        "<code>set_yscale(\"log\")</code> turns exponential growth into a straight line; zero and negative values silently drop out.",
        "<code>symlog</code> is logarithmic away from zero and linear near it, for data that crosses zero.",
        "A grid is for reading values off; the <strong>top and right spines</strong> carry no information, and removing them is the cheapest visual improvement available.",
    ],
    '''
title: Limits, Ticks and Scales
intro: Controlling what the axis shows and how it is written.

## Limits

`ax.set_xlim(a, b)` and `ax.set_ylim(a, b)` set the visible range.

By default matplotlib picks limits slightly **wider** than the data, so points do not sit on the frame. `ax.margins(0)` removes that padding, and `ax.margins(x=0.1, y=0.2)` sets it per axis as a fraction.

Passing the limits in reverse order reverses the axis: `ax.set_ylim(100, 0)` puts 100 at the bottom. That is how you draw a rank chart where 1 is best, or a depth profile where zero is the surface.

Two cautions. Setting limits **hides** data rather than removing it &mdash; points outside the range are still there, still counted by anything that reads the data, just not visible. And on a bar chart, changing the y limit away from zero misstates the values, which is the subject of its own module.

`ax.autoscale()` returns to automatic, and `ax.set_xlim(left=0)` sets one end and leaves the other automatic.

## Ticks

`ax.set_xticks(positions)` decides where the ticks go. `ax.set_xticklabels(labels)` decides what they say.

**Setting labels without setting positions is the classic bug.** matplotlib chooses its own positions based on the current view, and `set_xticklabels` simply renames whatever ticks happen to exist. Change the data and the labels stay put, now attached to different values. The symptom is a chart where the labels are subtly wrong and nothing errored.

Always set positions first, or pass both together: `ax.set_xticks(pos, labels)`.

For automatic but controlled ticks, `matplotlib.ticker` has locators: `MaxNLocator(5)` for at most five ticks, `MultipleLocator(0.25)` for every quarter, `LogLocator` for log axes.

`ax.tick_params(axis="x", rotation=45, labelsize=9)` handles rotation and size, which is the usual fix for crowded category labels &mdash; though `barh` is usually the better fix.

## Formatters

A formatter changes how a tick value is **written** without changing the value.

The default for large numbers uses a shared offset &mdash; a small `1e6` in the corner &mdash; which readers routinely miss, so a chart of millions gets read as a chart of single digits.

`FuncFormatter(lambda v, pos: "%.1fM" % (v / 1e6))` puts the unit on every label. The function receives the value and the tick position and returns a string.

The ready-made ones cover most needs: `PercentFormatter`, `StrMethodFormatter("{x:,.0f}")` for thousands separators, `EngFormatter` for SI prefixes, `FormatStrFormatter("%.2f")`.

`ax.ticklabel_format(style="plain")` is the quick way to switch off scientific notation entirely.

## Scales

`ax.set_yscale("log")` is the one that changes what a chart can show.

Data spanning orders of magnitude &mdash; populations, prices, counts, anything growing exponentially &mdash; is unreadable on a linear axis: the small values are pressed against zero and only the largest is visible. On a log axis they separate, and exponential growth becomes a straight line, which is diagnostic in itself.

Two things to know. Log requires **positive** values; zeros and negatives are dropped without an error, so a series that touches zero loses those points silently. And a log axis must be labelled as such, because a reader who assumes linear will misread every distance on it.

`"symlog"` is logarithmic away from zero and linear within a band around it, set by `linthresh`. It handles data that crosses zero, at the cost of a scale that changes character partway along &mdash; which needs explaining to the reader.

`"logit"` suits proportions, stretching the ends near 0 and 1.

## Grids and spines

A grid helps when someone will read values off the chart, and is decoration when they will not.

When it does help, a faint grid on one axis is usually enough: `ax.grid(True, axis="y", alpha=0.4)`. A full dark grid competes with the data for attention.

`ax.set_axisbelow(True)` draws it behind the data, which is normally what you want and is not always the default in a given style.

The **spines** are the four lines around the plot. The top and right ones enclose the area and carry no information:

```python
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
```

Two lines, and the chart immediately looks less like a default. It is the highest ratio of visual improvement to effort in matplotlib, which is why nearly every published-looking style does it.

`ax.spines["left"].set_position(("outward", 10))` detaches the remaining spines slightly, which is a further small refinement.

## Minor ticks

`ax.minorticks_on()` adds unlabelled ticks between the major ones, and `AutoMinorLocator(5)` sets how many.

They give a sense of scale without adding labels, which is useful on a log axis where the spacing between decades is not linear, and on any chart where the reader will estimate intermediate values.

`ax.grid(which="minor", alpha=0.15)` draws a fainter grid at the minor ticks, giving two levels of reference. That is common on engineering charts and usually too much for a presentation.

## Tick direction and appearance

`ax.tick_params` controls everything about ticks in one call:

```python
ax.tick_params(axis="both", direction="in", length=4,
               labelsize=9, colors="0.3")
```

`direction="in"` points the marks inward, which many publication styles prefer because it keeps the outer margin clean.

`which="both"` applies to major and minor together.

`top=False, right=False` removes ticks from the spines you have hidden &mdash; worth doing, since hiding a spine does not remove its ticks and leaving them produces marks floating in space.

## Formatting money, percentages and dates

The three formatters that come up most:

```python
from matplotlib.ticker import PercentFormatter, StrMethodFormatter, FuncFormatter

ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"£{v/1000:.0f}k"))
```

`PercentFormatter(xmax=1)` treats the data as fractions; `xmax=100` treats it as already-percentages. Getting that backwards multiplies everything by a hundred, and the chart still looks plausible.

The thousands separator from `StrMethodFormatter("{x:,.0f}")` is a small change that makes large numbers much faster to read.

## Symmetric limits

For diverging data, limits should usually be symmetric so zero sits in the middle:

```python
lim = max(abs(y.min()), abs(y.max()))
ax.set_ylim(-lim, lim)
```

Without it, a series ranging from &minus;2 to +8 puts zero a fifth of the way up, and the visual centre of the chart is +3 &mdash; which reads as the neutral point even though it is not.

The same reasoning applies to diverging colormaps, and for the same reason.

## Shared limits across charts

Two charts compared side by side must share their limits, whether or not they are subplots of one figure.

Within a figure, `sharey=True` does it. Across figures, compute the range once and apply it to both:

```python
lim = (0, max(a.max(), b.max()) * 1.05)
```

This is the same class of error as unshared subplots and unshared colour scales: the layout invites a comparison the axes do not support. It is easy to miss because each chart is individually correct.

## Tick density

The right number of ticks is fewer than the default in most cases.

Five to eight labelled ticks on an axis is comfortable. Twelve is crowded, and the reader is not using them all.

`MaxNLocator(6)` caps the count while keeping the positions on round numbers, which is usually better than choosing positions by hand because it adapts when the data changes.

`MultipleLocator(25)` forces a fixed interval, which is right when the interval has meaning &mdash; quarters, decades, standard bin widths.

For a categorical axis, every category needs a tick, and if there are too many for the labels to fit, the answer is a different chart rather than smaller text.

## Scales and honesty

A log axis changes what every distance on the chart means, and a reader who does not notice will misread every comparison on it.

Three things make it safe:

**Say so in the axis label** &mdash; "Population (log scale)".

**Use round decade ticks**, so the labels themselves announce the scale: 1, 10, 100, 1000.

**Consider whether the linear version answers the question.** A log scale is right when the data spans orders of magnitude or when relative change is the subject; it is wrong when absolute differences are what matter.

The same applies to any non-linear scale. The chart is not dishonest, but it depends on the reader noticing, and the labelling is what makes them notice.

## Ticks that carry meaning

Tick positions are an editorial choice, not a formatting detail.

Ticks at 0, 25, 50, 75, 100 say the scale is a percentage of something. Ticks at 0, 20, 40, 60, 80, 100 say the same range is being read in twenties. Ticks at the actual data boundaries &mdash; the minimum, the median, the maximum &mdash; say something else again.

Three patterns are worth knowing.

**Round numbers**, which is the default behaviour and right for most continuous scales.

**Meaningful values** &mdash; a target, a threshold, a previous year's figure &mdash; placed explicitly so the reader can see where the data sits relative to them. `ax.set_yticks(list(ax.get_yticks()) + [target])` adds one without losing the rest.

**Only the endpoints**, which is a minimalist treatment that works when the shape matters and precise values do not: `ax.set_yticks([y.min(), y.max()])`.

The last one is worth trying on a chart that feels cluttered. Most charts have more ticks than anyone uses, and each one is a small piece of visual noise competing with the data.

## In summary

Limits control what is visible and hide what is not, silently.

matplotlib adds a 5% margin by default, which is right until the data should reach the edge.

`set_xticks` decides positions and `set_xticklabels` the text, and setting labels without positions attaches them to whatever ticks happen to exist &mdash; a bug that produces a plausible, wrong chart.

Formatters change how numbers read, which matters most for large values that otherwise get a `1e6` offset nobody notices.

A log scale makes exponential growth a straight line and drops zeros without a word, and it must be labelled as logarithmic or every distance on it is misread.

And the top and right spines carry no information; removing them is the cheapest improvement matplotlib offers.

## Limits that adapt

Hard-coded limits are correct until the data changes, which for any chart regenerated regularly is a matter of time.

Three patterns that adapt.

**Anchor one end.** `ax.set_ylim(bottom=0)` fixes zero and lets the top follow the data &mdash; right for anything where zero is meaningful.

**Pad proportionally.** `ax.margins(y=0.15)` leaves headroom as a fraction rather than a fixed amount, so annotations near the top still fit when the values grow.

**Compute from the data.** `lim = max(abs(y.min()), abs(y.max()))` for a symmetric range around zero.

The one to avoid is `set_ylim(0, 100)` on a chart whose data will change, because when a value exceeds 100 the bar is silently clipped and nothing indicates it.

Where a fixed range is genuinely wanted &mdash; comparability across a series of charts &mdash; an assertion that the data fits inside it is worth the line.

## One more thing

`ax.invert_yaxis()` reverses an axis after the fact, which is more readable than passing the limits backwards when the limits are otherwise automatic.

It is the usual way to draw a ranked list with position 1 at the top, and a depth or pressure profile where the surface is at the top &mdash; both cases where the convention of the domain runs opposite to the axis default.

## The short version

Ticks and limits are where a chart quietly decides what the reader can see and how they read it.

Most charts have more ticks than anyone uses, a margin they did not choose, and a top and right spine carrying no information. Removing the excess is not decoration &mdash; it is what leaves the data as the most prominent thing on the chart.

## Reading the code back

Limits, ticks and scale are three separate decisions that are usually left to defaults together. Each has a case for being set: limits when the data should reach the edge or a baseline matters, ticks when the default count is more than anyone will read, and scale when the data spans orders of magnitude. Setting all three deliberately on a chart that matters takes four lines and changes how much work the reader has to do.
''',
    [
        {"q": "Why do automatic limits extend beyond the data?",
         "options": ["A bug", "matplotlib adds a margin so points do not sit on the frame", "To include zero", "For the legend"],
         "answer": 1,
         "why": "ax.margins(0) removes it, and passing limits in reverse order reverses the axis."},
        {"q": "What goes wrong when you call `set_xticklabels` without `set_xticks`?",
         "options": ["Nothing", "matplotlib keeps its own tick positions and renames them, so labels attach to the wrong values", "It raises", "Labels are ignored"],
         "answer": 1,
         "why": "The symptom is a chart whose labels are subtly wrong with no error - set positions first, or pass both together."},
        {"q": "What happens to zero values on a log axis?",
         "options": ["Plotted at the bottom", "Silently dropped", "Raise an error", "Treated as 1"],
         "answer": 1,
         "why": "Log requires positive values. A series that touches zero loses those points without any warning."},
        {"q": "What is the cheapest visual improvement to a default matplotlib chart?",
         "options": ["A different colormap", "Hiding the top and right spines", "A bigger font", "A grid"],
         "answer": 1,
         "why": "Those two lines enclose the plot and carry no information. Nearly every published-looking style removes them."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Subplots
# ---------------------------------------------------------------------------
topic(
    "subplots",
    "Subplots",
    "Layout",
    "Several axes on one figure - the grid, the shared axes, and the layout "
    "that stops them colliding.",
    _svg(_box(18, 20, 54, 24, S, A) + _box(78, 20, 54, 24, S, A) +
         _box(18, 50, 54, 24, S, A) + _box(78, 50, 54, 24, S, A)),
    [
        ("A grid of axes",
         "<code>subplots(rows, cols)</code> returns an array you index or iterate.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)

fig, axes = plt.subplots(2, 3, figsize=(9, 4))
print("axes is a", type(axes).__name__, "of shape", axes.shape)

for i, ax in enumerate(axes.flat):
    ax.plot(rng.random(20).cumsum())
    ax.set_title("panel %d" % i, fontsize=9)

fig.tight_layout()

print()
print("axes[0, 2] is the top-right panel.")
print("axes.flat iterates them in reading order, which is what you want")
print("when the panels correspond to a flat list of things.")
print()
print("With one row or one column it is 1-D; with 1x1 it is a single")
print("Axes, not an array - which is why fig, ax = plt.subplots() works.")'''),

        ("squeeze, and the shape surprise",
         "A 1xN grid gives a 1-D array, which breaks code written for 2-D.",
         '''import matplotlib.pyplot as plt

for r, c in [(1, 1), (1, 3), (3, 1), (2, 2)]:
    fig, axes = plt.subplots(r, c, figsize=(2, 1))
    shape = getattr(axes, "shape", "single Axes")
    print("subplots(%d, %d) -> %s" % (r, c, shape))
    plt.close(fig)

print()
fig, axes = plt.subplots(1, 3, figsize=(6, 1.6), squeeze=False)
print("squeeze=False always gives 2-D:", axes.shape)
print()
print("Code that does axes[0, 1] breaks on a 1-D result. squeeze=False")
print("makes the shape predictable, which matters in a function that")
print("takes the grid size as an argument.")

fig2, ax = plt.subplots(figsize=(4, 2))
ax.plot([0, 1], [1, 0])
ax.set_title("and one figure left open to show")'''),

        ("Sharing axes",
         "So panels can be compared, and the labels stop repeating.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
data = [rng.normal(loc, 1, 200) for loc in (0, 1, 2)]

fig, axes = plt.subplots(1, 3, figsize=(9, 2.6))
for ax, d in zip(axes, data):
    ax.hist(d, bins=20)
fig.suptitle("independent axes - the panels are NOT comparable")

fig2, axes2 = plt.subplots(1, 3, figsize=(9, 2.6), sharex=True, sharey=True)
for ax, d in zip(axes2, data):
    ax.hist(d, bins=20)
fig2.suptitle("sharex/sharey - now they are")

print("Without sharing, each panel scales to its own data, so a taller")
print("bar in one panel can represent a smaller number than a shorter")
print("bar in another. Sharing is what makes a grid a comparison.")
print()
print("It also hides the inner tick labels, which removes clutter.")'''),

        ("Panels of different sizes",
         "<code>gridspec</code> when the grid is not uniform.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(2)

fig = plt.figure(figsize=(8, 4))
gs = fig.add_gridspec(2, 3, height_ratios=[2, 1], width_ratios=[2, 1, 1])

big = fig.add_subplot(gs[0, :])
big.plot(rng.random(80).cumsum())
big.set_title("spans the whole top row")

for i in range(3):
    ax = fig.add_subplot(gs[1, i])
    ax.bar(["a", "b"], rng.random(2))
    ax.set_title("small %d" % i, fontsize=9)

fig.tight_layout()

print("gs[0, :]   - row 0, every column")
print("gs[1, 0]   - row 1, first column")
print("height_ratios makes the top row twice the height of the bottom.")'''),

        ("subplot_mosaic reads better",
         "A picture of the layout, in a string.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)

fig, axd = plt.subplot_mosaic(
    """
    AAB
    CCB
    """,
    figsize=(8, 4))

axd["A"].plot(rng.random(50).cumsum())
axd["A"].set_title("A")
axd["B"].barh(["x", "y", "z"], rng.random(3))
axd["B"].set_title("B")
axd["C"].hist(rng.normal(size=300), bins=20)
axd["C"].set_title("C")
fig.tight_layout()

print("The string IS the layout. Repeated letters span cells.")
print("axd is a dict keyed by the letters, so panels have names")
print("rather than indices - which reads far better than gs[0, :2].")'''),

        ("Making room",
         "<code>tight_layout</code> and <code>constrained_layout</code> both stop "
         "labels colliding.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(4)

fig, axes = plt.subplots(2, 2, figsize=(6, 4))
for ax in axes.flat:
    ax.plot(rng.random(10))
    ax.set_xlabel("a long x label")
    ax.set_ylabel("a long y label")
fig.suptitle("no layout management - labels collide")

fig2, axes2 = plt.subplots(2, 2, figsize=(6, 4), constrained_layout=True)
for ax in axes2.flat:
    ax.plot(rng.random(10))
    ax.set_xlabel("a long x label")
    ax.set_ylabel("a long y label")
fig2.suptitle("constrained_layout=True")

print("tight_layout() is called after drawing and adjusts once.")
print("constrained_layout=True is set at creation and keeps adjusting,")
print("which handles colorbars and suptitles better.")
print()
print("Neither is the default, and a figure that looks fine on screen")
print("and cropped when saved is almost always missing one of them.")'''),
    ],
    [
        "<code>subplots(r, c)</code> returns an <strong>array</strong> of axes; <code>axes.flat</code> iterates in reading order.",
        "The array is 2-D only for a true grid &mdash; <code>1xN</code> gives 1-D and <code>1x1</code> gives a bare Axes. <code>squeeze=False</code> makes it always 2-D.",
        "<code>sharex</code>/<code>sharey</code> are what make a grid a <strong>comparison</strong>; without them each panel scales to its own data.",
        "<code>add_gridspec</code> with <code>height_ratios</code> handles panels of different sizes; <code>gs[0, :]</code> spans a row.",
        "<code>subplot_mosaic</code> takes a picture of the layout as a string and returns a dict keyed by the letters.",
        "<code>tight_layout()</code> or <code>constrained_layout=True</code> stop labels colliding &mdash; a figure cropped when saved is usually missing one.",
    ],
    '''
title: Subplots
intro: Several axes on one figure.

## The grid

`fig, axes = plt.subplots(2, 3)` creates a figure with six axes and returns them as a NumPy array.

`axes[0, 2]` is the top-right panel. `axes.flat` iterates in reading order, which is what you want when the panels correspond to a flat list of categories:

```python
for ax, name in zip(axes.flat, names):
    ...
```

`zip` stops at the shorter of the two, so a grid with more cells than data leaves the extras blank &mdash; visible, and usually worth removing with `ax.remove()` or hiding with `ax.axis("off")`.

## The shape surprise

The returned array's shape is not always what code expects.

`subplots(2, 3)` gives a `(2, 3)` array. `subplots(1, 3)` gives a **1-D** array of three. `subplots(1, 1)` gives a single `Axes`, not an array at all &mdash; which is what makes `fig, ax = plt.subplots()` work.

That is convenient interactively and awkward in a function that takes the grid size as a parameter, because `axes[0, 1]` fails on the 1-D case.

`squeeze=False` forces a 2-D array always. In reusable code it is the right default, and it costs one argument.

## Sharing

`sharex=True` and `sharey=True` make the panels use the same limits.

This is not a cosmetic setting. Without it, every panel autoscales to its own data, so a bar that reaches the top of one panel may represent a smaller number than a shorter bar in the panel beside it. The grid looks like a comparison and is not one.

Sharing also hides the inner tick labels, which removes a great deal of repetition from a grid.

`sharex="col"` and `sharey="row"` share within columns or rows, which suits a matrix where each row is a different quantity.

The trade-off: with shared axes, a panel whose data occupies a small part of the shared range is compressed. When the panels genuinely have different scales, small multiples with independent axes and clearly labelled ranges are more honest &mdash; but then the reader must be told not to compare heights directly.

## Uneven grids

`fig.add_gridspec(rows, cols)` creates a grid you then slice:

```python
gs = fig.add_gridspec(2, 3, height_ratios=[2, 1])
big = fig.add_subplot(gs[0, :])     # whole top row
small = fig.add_subplot(gs[1, 0])   # bottom left
```

`height_ratios` and `width_ratios` make rows and columns different sizes, which is how you give a main chart more space than the supporting ones.

## subplot_mosaic

`plt.subplot_mosaic` takes a **picture** of the layout:

```python
fig, axd = plt.subplot_mosaic("""
    AAB
    CCB
""")
```

Repeated letters span cells, and the result is a dict keyed by the letters. `axd["A"]` is far easier to follow than `gs[0, :2]`, and the layout is visible in the source rather than encoded in slice arithmetic.

A `.` in the string leaves a cell empty.

It is the most readable way to build an uneven layout, and worth preferring wherever it fits.

## Layout

Labels, titles and tick text are drawn outside the axes, and matplotlib does not account for them when placing panels. The result is overlapping labels, or a title running off the top.

Two mechanisms fix it.

`fig.tight_layout()` is called after everything is drawn and adjusts spacing once. It is simple and works for most cases; it can be confused by artists added afterwards, and it does not handle colorbars especially well.

`constrained_layout=True` is set when the figure is created and keeps adjusting as things are added. It handles colorbars, suptitles and legends outside the axes better, and it is the one to reach for on a complex figure.

Neither is on by default. `fig.subplots_adjust(hspace=..., wspace=...)` sets spacing manually when you want precise control.

The symptom of missing layout management is a figure that looks acceptable on screen and comes out cropped when saved &mdash; because `savefig` uses the figure's declared size, not whatever the screen happened to show. `bbox_inches="tight"` on `savefig` is the other half of that fix.

## Removing unused panels

A 3&times;4 grid holding ten charts leaves two empty boxes with ticks and spines, which look like a mistake.

`ax.remove()` deletes the axes entirely. `ax.axis("off")` keeps it but hides everything, which preserves the spacing &mdash; useful when the grid should stay rectangular.

```python
for ax in axes.flat[len(items):]:
    ax.remove()
```

The empty cell is also a reasonable place for a legend or a note, using `ax.axis("off")` and `ax.legend(...)` with handles gathered from the other panels.

## Titles and labels across a grid

With shared axes, per-panel axis labels are repetition. `fig.supxlabel` and `fig.supylabel` label the grid once.

Panel titles remain useful and should be small &mdash; they are identifying the panel, not heading a chart. `fontsize=9` and `loc="left"` reads well.

For a formal figure, lettering the panels is conventional:

```python
for letter, ax in zip("abcdef", axes.flat):
    ax.text(0.02, 0.95, letter, transform=ax.transAxes,
            fontweight="bold", va="top")
```

Axes coordinates, so the letter stays in the corner regardless of the data.

## Iterating in the right order

`axes.flat` iterates row by row, which matches how the panels will be read.

`zip(axes.flat, items)` pairs them and stops at the shorter, which is convenient and silently drops items if the grid is too small. Asserting the sizes match is one line and prevents a chart quietly missing a category:

```python
assert len(items) <= axes.size
```

For a grid indexed by two variables, `axes[i, j]` with explicit loops is clearer than flattening, because the position then carries meaning.

## When not to use subplots

Small multiples are excellent for comparing the **same** measurement across groups.

They are poor when the panels show different quantities on different scales, because the shared layout implies a comparability that the axes do not support. Four panels showing revenue, headcount, latency and satisfaction are four charts that happen to be adjacent, and separating them &mdash; or at least not sharing axes and labelling each scale clearly &mdash; is more honest.

They are also poor past about twelve panels, where each becomes too small to read. At that point the answer is usually to reduce what is being shown, not to shrink the panels further.

## Figure size for a grid

The figure size should scale with the grid. A 2&times;3 grid in the same six inches as a single chart gives panels a third the size, and text that was comfortable becomes proportionally huge.

A reasonable rule is to keep the per-panel size roughly constant:

```python
fig, axes = plt.subplots(nrows, ncols, figsize=(3.2 * ncols, 2.4 * nrows))
```

Then adding a row makes the figure taller rather than making everything smaller.

## Shared axes in detail

`sharex=True` links the axes objects, so changing the limits on one changes all of them &mdash; which is convenient interactively and occasionally surprising in a script, where an autoscale on one panel silently rescales the rest.

`ax.label_outer()` hides the tick labels on inner panels, which `sharex`/`sharey` do automatically but which is needed when you build the grid by hand.

`sharex="col"` links within columns only, which suits a grid where columns are different quantities and rows are groups.

To share afterwards rather than at creation, `ax2.sharex(ax1)` exists, and the older `ax2.get_shared_x_axes().join(ax1, ax2)` appears in existing code.

## A grid that reads

The details that make a grid of panels look considered:

**Consistent panel titles**, small and left-aligned.

**One axis label per grid**, via `supxlabel`/`supylabel`.

**Shared limits**, so the comparison is valid.

**A consistent colour** across panels for the same series, or a single colour if each panel is one thing.

**Empty cells removed**, not left as empty boxes.

**A common annotation style** &mdash; if one panel has a reference line, they all should.

Individually trivial; together they are the difference between a grid that reads as one figure and one that reads as several charts stuck together.

## Building a grid programmatically

Most real grids are generated from data rather than written out, and a few patterns make that robust.

Compute the grid size from the number of items:

```python
n = len(items)
ncols = 3
nrows = math.ceil(n / ncols)
fig, axes = plt.subplots(nrows, ncols, figsize=(3.2 * ncols, 2.4 * nrows),
                         sharex=True, sharey=True, squeeze=False)
```

`squeeze=False` guarantees a 2-D array whatever the numbers work out to, so `axes.flat` always behaves.

Then pair, draw, and clean up the remainder:

```python
for ax, item in zip(axes.flat, items):
    draw(ax, item)
for ax in axes.flat[n:]:
    ax.remove()
```

The figure size scaling with the grid is what keeps the text a constant size relative to each panel, rather than shrinking as rows are added.

And because `zip` stops at the shorter argument, asserting `n <= axes.size` is worth the line &mdash; otherwise a grid that is too small silently drops categories.

## In summary

`subplots(r, c)` returns an array; `axes.flat` iterates in reading order; `squeeze=False` makes the shape predictable.

`sharex` and `sharey` are what turn a grid into a comparison, and without them each panel scales to its own data and the heights mean different things.

`gridspec` and `subplot_mosaic` handle uneven layouts, and the mosaic string is far easier to read than slice arithmetic.

`tight_layout` or `constrained_layout` stop labels colliding, and a figure that saves cropped is usually missing one.

Label the grid once with `supxlabel` rather than every panel, remove unused cells, and scale the figure size with the number of panels.

And small multiples are the right answer far more often than one crowded chart &mdash; they are the display that makes many comparisons possible at once.

## Grids in practice

Three layouts cover nearly all real grids.

**A row of two or three**, for a before-and-after or a small set of related views. Wide, shared y, one shared axis label.

**A square-ish grid**, for small multiples over a categorical variable. Shared both ways, panel titles small, figure size scaled by the grid.

**A main chart plus supporting ones**, built with `subplot_mosaic` or `gridspec` and unequal ratios. The main panel gets two-thirds of the height and the supporting row the rest.

The fourth layout &mdash; a grid of unrelated charts &mdash; is common and usually a mistake. Panels in a grid are read as comparable, and four charts of different quantities on different scales are four figures that happen to be adjacent. Either give them separate figures, or make the difference explicit with clearly labelled independent scales and no shared axes.

The question that decides it: would a reader be right to compare the panels to each other? If yes, share the axes. If no, they probably should not be in a grid.

## Sharing a legend

A grid where every panel repeats the same legend wastes space and attention.

One figure-level legend is the fix:

```python
handles, labels = axes.flat[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=len(labels))
fig.subplots_adjust(bottom=0.15)
```

Handles are taken from any one panel, because they are all the same series, and `fig.legend` places it relative to the figure rather than an axes.

Room has to be made for it, which `constrained_layout` does automatically and `subplots_adjust` does explicitly.

The same applies to a colorbar: one bar serving the whole grid, which also enforces the shared scale the panels need to be comparable.

## One more thing

`fig.align_ylabels()` lines up the y-axis labels across a column of panels, which otherwise sit at different distances from the axes depending on how wide each panel's tick labels are.

It is a small alignment that is very visible once noticed, and `align_xlabels` does the same horizontally. On a grid where the panels have different value ranges, it is the difference between a column of labels that reads as one and one that looks ragged.

## The short version

A grid is a claim that the panels belong together. Sharing the axes is what makes the claim true, and labelling the grid once rather than every panel is what makes it read as one figure.

The three things that most often go wrong are an unshared y axis making incomparable panels look comparable, a figure size that did not grow with the grid so everything is cramped, and empty cells left as bare boxes. All three are one line each.

## Reading the code back

A grid is created in one call and finished in three: share the axes, label the grid once, and remove what is unused. The figure size should be computed from the grid rather than fixed, so adding a row makes the figure taller instead of making every panel smaller. Those four decisions are what separate a grid that reads as one figure from several charts that happen to be adjacent.
''',
    [
        {"q": "What does `plt.subplots(1, 3)` return for the axes?",
         "options": ["A 2-D array", "A 1-D array of three", "A single Axes", "A dict"],
         "answer": 1,
         "why": "1x1 gives a bare Axes, which is what makes `fig, ax = plt.subplots()` work. squeeze=False forces 2-D always."},
        {"q": "Why does `sharey=True` matter for a grid of histograms?",
         "options": ["It is faster", "Without it each panel autoscales, so bar heights are not comparable between panels", "It fixes the bins", "It adds a legend"],
         "answer": 1,
         "why": "The grid looks like a comparison and is not one. Sharing also hides the inner tick labels."},
        {"q": "What does the string in `subplot_mosaic` represent?",
         "options": ["Panel titles", "A picture of the layout, where repeated letters span cells", "Colour codes", "The data"],
         "answer": 1,
         "why": "It returns a dict keyed by the letters, so axd['A'] beats gs[0, :2] for readability."},
        {"q": "A figure looks fine on screen but is cropped when saved. What is missing?",
         "options": ["A higher dpi", "Layout management - tight_layout or constrained_layout, and bbox_inches='tight'", "A larger figsize", "A different format"],
         "answer": 1,
         "why": "savefig uses the figure's declared size, not what the screen showed, and labels are drawn outside the axes."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Colour
# ---------------------------------------------------------------------------
topic(
    "colours_and_colormaps",
    "Colour and Colormaps",
    "Making It Readable",
    "Naming colours, the cycle, and picking a colormap that does not invent "
    "structure.",
    _svg('<rect x="18" y="34" width="22" height="26" fill="#440154"/>'
         '<rect x="40" y="34" width="22" height="26" fill="#3b528b"/>'
         '<rect x="62" y="34" width="22" height="26" fill="#21918c"/>'
         '<rect x="84" y="34" width="22" height="26" fill="#5ec962"/>'
         '<rect x="106" y="34" width="22" height="26" fill="#fde725"/>'),
    [
        ("Ways to name a colour",
         "Five notations, all accepted anywhere a colour is wanted.",
         '''import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 2.5))
options = [
    ("crimson", "a CSS name"),
    ("#4c72b0", "hex"),
    ("C2", "the 3rd colour of the cycle"),
    ("0.55", "a grey level, as a STRING"),
    ((0.2, 0.6, 0.4), "an RGB tuple 0-1"),
]
for i, (c, why) in enumerate(options):
    ax.barh([i], [1], color=c)
    ax.text(1.05, i, "%-14s %s" % (repr(c), why), va="center", fontsize=9)
ax.set_xlim(0, 3.2)
ax.set_yticks([])

print("'0.55' in quotes is a grey level; 0.55 without quotes is a number")
print("and will not work as a colour.")
print()
print("C0-C9 refer to the current cycle, so a chart stays consistent")
print("when the style changes.")'''),

        ("The property cycle",
         "Replace it and every later plot on that axes follows.",
         '''import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

x = np.linspace(0, 10, 60)

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

for k in range(4):
    a.plot(x, np.sin(x + k))
a.set_title("default cycle")

b.set_prop_cycle(cycler(color=["#264653", "#2a9d8f", "#e9c46a", "#e76f51"]))
for k in range(4):
    b.plot(x, np.sin(x + k))
b.set_title("house palette")

print("set_prop_cycle applies to one axes.")
print("plt.rcParams['axes.prop_cycle'] changes it for everything after.")
print()
print("A cycler can vary more than colour:")
print("   cycler(color=[...]) + cycler(linestyle=['-', '--'])")
print("which pairs them, so the chart survives being printed in grey.")'''),

        ("Three kinds of colormap",
         "Picking the wrong kind invents structure that is not in the data.",
         '''import matplotlib.pyplot as plt
import numpy as np

grad = np.linspace(0, 1, 256).reshape(1, -1)
maps = [("viridis", "sequential - low to high"),
        ("coolwarm", "diverging - around a midpoint"),
        ("tab10", "qualitative - unordered categories"),
        ("jet", "avoid: false bands, bad in grey")]

fig, axes = plt.subplots(4, 1, figsize=(7, 3))
for ax, (name, why) in zip(axes, maps):
    ax.imshow(grad, aspect="auto", cmap=name)
    ax.set_yticks([]); ax.set_xticks([])
    ax.set_ylabel(name, rotation=0, ha="right", va="center", fontsize=9)
    ax.text(262, 0, why, va="center", fontsize=8, transform=ax.transData)
fig.tight_layout()

print("sequential  : one direction. Use for magnitudes.")
print("diverging   : two directions from a meaningful centre, like zero.")
print("qualitative : distinct hues, no order. Use for categories.")
print()
print("Using a diverging map for data with no midpoint invents one.")'''),

        ("Why not jet",
         "It is not perceptually uniform, so equal steps in value look unequal.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 256)
grad = x.reshape(1, -1)

fig, axes = plt.subplots(2, 2, figsize=(8, 3))
for ax, cmap in zip(axes.flat[:2], ["jet", "viridis"]):
    ax.imshow(grad, aspect="auto", cmap=cmap)
    ax.set_title(cmap); ax.set_xticks([]); ax.set_yticks([])

for ax, cmap in zip(axes.flat[2:], ["jet", "viridis"]):
    rgb = plt.get_cmap(cmap)(x)[:, :3]
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722])
    ax.plot(x, lum)
    ax.set_title("%s: brightness" % cmap, fontsize=9)
    ax.set_ylim(0, 1)
fig.tight_layout()

print("The lower plots are how bright each colormap is along its range.")
print("viridis rises steadily; jet goes up, down and up again.")
print()
print("That means jet shows features where the data has none - the eye")
print("reads a brightness change as a boundary - and it collapses to")
print("mush when printed in greyscale.")'''),

        ("Colorbars",
         "A colormap without a scale is decoration.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
z = rng.normal(size=(20, 30))

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.imshow(z, cmap="viridis")
a.set_title("no colorbar - the colours mean nothing")

im = b.imshow(z, cmap="viridis")
fig.colorbar(im, ax=b, label="value")
b.set_title("with a scale")

print("fig.colorbar needs the mappable that imshow/scatter/pcolormesh")
print("returned - which is why those return values get captured.")
print()
print("ax= says which axes to steal space from; shrink and pad adjust")
print("the size, and orientation='horizontal' puts it underneath.")'''),

        ("Colour is not the only channel",
         "About one man in twelve cannot distinguish red from green.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 60)

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.plot(x, np.sin(x), color="red", label="red")
a.plot(x, np.cos(x), color="green", label="green")
a.legend(); a.set_title("colour only")

b.plot(x, np.sin(x), color="#0072B2", linestyle="-", marker="o",
       markevery=8, label="solid, circles")
b.plot(x, np.cos(x), color="#E69F00", linestyle="--", marker="s",
       markevery=8, label="dashed, squares")
b.legend(); b.set_title("colour + style + marker")

print("Red against green is the pairing to avoid.")
print("Blue/orange stays distinguishable for nearly everyone, and")
print("varying linestyle as well means the chart still works in")
print("greyscale, in a photocopy, and on a projector.")'''),
    ],
    [
        "Colours accept CSS names, hex, <code>C0</code>&ndash;<code>C9</code> from the cycle, a grey level <strong>as a string</strong>, or an RGB tuple.",
        "<code>set_prop_cycle</code> changes the colours for one axes; a <code>cycler</code> can vary linestyle too, so the chart survives greyscale.",
        "Colormaps are <strong>sequential</strong> (magnitude), <strong>diverging</strong> (around a meaningful centre) or <strong>qualitative</strong> (categories). The wrong kind invents structure.",
        "<code>jet</code> is not perceptually uniform &mdash; its brightness rises and falls, so the eye reads boundaries the data does not have.",
        "A colormap needs a <strong>colorbar</strong>; <code>fig.colorbar</code> takes the mappable that <code>imshow</code> or <code>scatter</code> returned.",
        "Roughly one man in twelve cannot separate red from green &mdash; vary linestyle or marker as well as colour.",
    ],
    '''
title: Colour and Colormaps
intro: Naming colours, the cycle, and picking a colormap that does not invent structure.

## Naming a colour

matplotlib accepts several notations wherever a colour is wanted:

A **CSS name**: `"crimson"`, `"steelblue"`, `"rebeccapurple"`.

**Hex**: `"#4c72b0"`, with an optional alpha suffix.

A **cycle reference**: `"C0"` through `"C9"`, meaning the nth colour of the current property cycle. Using these keeps a figure consistent when the style changes.

A **grey level as a string**: `"0.55"`. The quotes matter &mdash; the bare number `0.55` is not a colour.

An **RGB or RGBA tuple** of floats from 0 to 1.

Single letters `"r"`, `"g"`, `"b"`, `"k"` also work, and are the ones the format-string shorthand uses.

## The property cycle

Each axes has a **property cycle** that supplies the colour for successive plots. The default has ten colours and then repeats.

`ax.set_prop_cycle(cycler(color=[...]))` replaces it for one axes. `plt.rcParams["axes.prop_cycle"]` replaces it globally, which is how you apply a house palette to a whole script.

A `cycler` can carry more than colour:

```python
cycler(color=palette) + cycler(linestyle=["-", "--", ":", "-."])
```

`+` pairs them elementwise, so the first series is the first colour and the first linestyle. That single change makes every chart in a script survive being printed in greyscale, which is worth more than it costs.

`*` gives the outer product instead, cycling every combination.

## Three kinds of colormap

The choice of colormap is a statement about the data, and the wrong one asserts something false.

**Sequential** &mdash; `viridis`, `plasma`, `Blues` &mdash; runs from low to high in one direction. Use for magnitudes: counts, temperatures, concentrations.

**Diverging** &mdash; `coolwarm`, `RdBu`, `BrBG` &mdash; has two directions from a neutral centre. Use when there is a **meaningful midpoint**: zero, an average, a baseline. Applying one to data with no natural centre invents a boundary in the middle of the range.

**Qualitative** &mdash; `tab10`, `Set2` &mdash; is a set of distinct hues with no ordering. Use for categories. Using a sequential map for categories implies an order that does not exist.

**Cyclic** &mdash; `twilight`, `hsv` &mdash; wraps around, for angles and phases.

## Why jet is a problem

`jet` was the default in older tools and still appears everywhere. It is a bad choice, for a reason that is measurable rather than aesthetic.

A good colormap is **perceptually uniform**: equal steps in the data look like equal steps in colour. `viridis` was designed for this, and its brightness increases steadily from one end to the other.

`jet` does not. Its brightness rises, falls and rises again, with a bright band in the middle. The eye reads a sharp brightness change as a boundary, so `jet` shows edges and structure where the data is perfectly smooth &mdash; and hides real gradients in the flat regions.

It also collapses when converted to greyscale, because different values map to the same brightness.

The fourth editor plots the brightness of both, which makes the difference visible rather than assertable.

## Colorbars

A colour-mapped plot without a colorbar is decoration: the reader can see that values differ and not by how much.

`fig.colorbar(mappable, ax=ax)` needs the object returned by the drawing call &mdash; `imshow`, `scatter`, `pcolormesh`, `contourf`. That is why those return values are captured here.

`label=` names the quantity, which is as important as it is on an axis. `shrink` and `pad` adjust size and spacing; `orientation="horizontal"` puts it below.

For a grid of subplots, `fig.colorbar(im, ax=axes.ravel().tolist())` makes one bar serve all panels, which is right when they share a scale &mdash; and they should, or the panels are not comparable.

## Accessibility

Around 8% of men and 0.5% of women have some form of colour vision deficiency, most commonly difficulty separating red from green.

Three habits cover most of it:

**Avoid red against green** as the primary distinction. Blue against orange is distinguishable for almost everyone.

**Vary a second channel** &mdash; linestyle, marker, or position &mdash; so colour is reinforcing rather than carrying the meaning alone.

**Use `viridis` and friends** for continuous data. They were designed to remain monotonic in brightness under common deficiencies, which is why they work in greyscale too.

The greyscale test is a good proxy for all of it: print the chart in black and white, and if it is still readable, it will survive most viewing conditions.

## Transparency

`alpha` runs from 0 to 1 and can be set per artist or baked into a colour as a fourth channel.

Three places it earns its keep: showing density in an overplotted scatter, letting a shaded band sit under a line without hiding it, and de-emphasising context series without changing their colour.

Two cautions. Alpha compounds &mdash; ten overlapping shapes at 0.1 are opaque where they all coincide, which is exactly the density signal you want in a scatter and an unwanted colour shift elsewhere. And transparency is lost when a figure is flattened onto a background, so a chart designed with alpha over white looks different over grey.

## Named palettes

matplotlib ships the `tab10` and `tab20` qualitative sets, and `plt.get_cmap("tab10").colors` gives the list for use in a cycler.

For categorical work, palettes designed for colour-vision deficiency are worth preferring &mdash; the Okabe&ndash;Ito set is eight colours chosen to remain distinguishable under the common deficiencies, and it is a plain list of hex codes you can paste into a cycler.

For sequential data, the perceptually uniform family is `viridis`, `plasma`, `inferno`, `magma` and `cividis`. `cividis` is designed specifically to look the same to viewers with and without colour-vision deficiency.

Appending `_r` to any colormap name reverses it: `viridis_r`.

## Discrete colour from a continuous map

Sampling a continuous colormap gives a graded set for ordered categories:

```python
cmap = plt.get_cmap("viridis")
colors = [cmap(i / (n - 1)) for i in range(n)]
```

That is right when the categories have an **order** &mdash; age bands, quartiles, years &mdash; because the colour then carries the ordering.

It is wrong for unordered categories, where a qualitative palette should be used instead, and it is a common way to imply a sequence that does not exist.

`BoundaryNorm` does the same thing for a mapped plot, banding a continuous scale into discrete steps with a colorbar that shows the boundaries.

## Colorbar placement

The default steals space from the axes it is attached to, which shrinks that panel and misaligns it with its neighbours.

`fig.colorbar(im, ax=axes.ravel().tolist())` spans several panels with one bar, which is right when they share a scale.

`shrink=0.8` and `aspect=30` adjust its proportions; `pad` sets the gap; `location="bottom"` moves it.

For precise control, `fig.add_axes([left, bottom, width, height])` creates a dedicated axes for it in figure coordinates, which is how you get a colorbar that lines up exactly with a grid.

## Backgrounds

`fig.patch` is the figure background and `ax.patch` the axes background, and they are separate.

`ax.set_facecolor("#f7f7f7")` gives the plotting area a light tint, which some styles use to make a white grid readable.

For a dark theme, both need setting along with the text, tick and spine colours &mdash; which is exactly what the `dark_background` style does, and a reason to use a style rather than setting six things by hand.

## Building a palette

A palette for a project needs fewer colours than people expect.

**One** colour, for charts with a single series. Most charts.

**Two**, for a comparison or a before-and-after.

**A greyscale plus one accent**, for highlighting one series among many. This covers more cases than any multi-colour palette.

**Five or six**, for genuinely categorical work, drawn from a set designed for the purpose.

Beyond about six, colour stops distinguishing reliably, and the answer is small multiples rather than more hues.

Add a grey for context elements, a light grey for gridlines, and a dark grey rather than black for text, and that is a complete house palette.

## Testing a colour scheme

Three checks, none of which needs a tool.

**Greyscale.** Convert the figure to greyscale and see whether the series are still distinguishable. If they are not, luminance is not varying and the chart depends entirely on hue.

**Small size.** View the figure at the size it will actually be seen. Colours that separate at full screen frequently do not at thumbnail size.

**Print.** A projector and a printer both compress the range, and colours that differ on a monitor often do not survive either.

Passing all three usually means the encoding is robust, and failing any of them is fixed the same way: vary luminance, and vary a second channel.

## Colour with meaning

The strongest use of colour is when it encodes something the reader already understands.

**Semantic colours** &mdash; red for loss, green for gain, a brand colour for one product &mdash; are read without a legend because the meaning arrives with the hue. They are also culturally specific, and the red/green pairing is the worst possible choice for colour-blind readers, so the convention has to be weighed against accessibility.

**Sequential colour for an ordered variable** &mdash; darker for more &mdash; is read correctly with almost no instruction.

**One accent against grey** is the most reliable of all, because it says "this one" and nothing else.

The weakest use is colour as decoration: seven categories in seven hues because the palette had seven. That asks the reader to learn an arbitrary mapping and consult it repeatedly, and it is usually a sign the chart should be small multiples.

The test is whether removing the colour destroys the chart's meaning or only its appearance. If the former, the colour is doing work and should be chosen carefully. If the latter, it can be simplified away.

## In summary

Colours accept names, hex, `C0`-style cycle references, greys as strings, and RGB tuples.

The property cycle supplies distinct colours automatically, and a cycler can vary linestyle alongside colour so the chart survives greyscale.

Colormaps come in three kinds, and using the wrong kind asserts something false: sequential for magnitude, diverging around a real centre, qualitative for unordered categories.

`jet` fails measurably rather than aesthetically &mdash; its brightness is not monotonic, so it shows edges the data does not have.

A colour-mapped plot needs a colorbar, with a label, and two such plots need a shared scale.

And roughly one man in twelve cannot separate red from green, which is why a second channel is worth varying and why greyscale is a good proxy test for the whole question.

## A closing note

Colour is the most over-used channel in charting and the most rewarding to use sparingly.

The strongest charts usually have one colour, or one colour against grey. Colour that encodes a variable earns its place; colour that distinguishes seven categories nobody needs to distinguish does not.

The technical points matter too &mdash; perceptual uniformity, the right kind of colormap, a centred diverging scale, a colorbar that says what the colours mean &mdash; and they are all in service of the same thing: the reader should be able to work out what a colour means without being told twice.

The greyscale test remains the quickest check on all of it.

## The short version

Colour is the most over-used channel in charting and the most rewarding to use sparingly.

One accent against grey outperforms a seven-hue palette in almost every case, and the greyscale test is the quickest check on whether the encoding survives contact with the real world.

## Reading the code back

Colour decisions are made once for a project and applied through a cycler, not chosen per chart. A palette of five or six for categories, a sequential map for magnitudes, a diverging one for data with a real centre, and a grey for context is a complete set. Anything beyond that is usually a chart that should have been small multiples.
''',
    [
        {"q": "What does the string `'0.55'` mean as a colour?",
         "options": ["55% opacity", "A grey level", "An error", "The 55th colour"],
         "answer": 1,
         "why": "The quotes matter - the bare number 0.55 is not a colour. C0-C9 refer to the current cycle instead."},
        {"q": "When is a diverging colormap the wrong choice?",
         "options": ["Always", "When the data has no meaningful midpoint - it invents a boundary mid-range", "For temperatures", "For negative values"],
         "answer": 1,
         "why": "Sequential for magnitudes, diverging around a real centre like zero, qualitative for unordered categories."},
        {"q": "What is measurably wrong with `jet`?",
         "options": ["Too colourful", "Its brightness rises and falls, so the eye reads boundaries where the data is smooth", "It is slow", "It has too few colours"],
         "answer": 1,
         "why": "It also collapses in greyscale, because different values map to the same brightness. viridis is monotonic in brightness."},
        {"q": "What does `fig.colorbar` need as its first argument?",
         "options": ["The axes", "The mappable returned by imshow, scatter or pcolormesh", "The colormap name", "The data"],
         "answer": 1,
         "why": "Which is why those return values get captured. label= names the quantity, as important as it is on an axis."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Annotation
# ---------------------------------------------------------------------------
topic(
    "annotations",
    "Annotating a Plot",
    "Making It Readable",
    "Text, arrows and reference lines - saying what the chart is for.",
    _svg(_box(14, 16, 132, 58, "none", B) +
         '<polyline points="24,62 52,44 80,50 108,26 134,34" fill="none" stroke="%s" stroke-width="2"/>' % M +
         '<circle cx="108" cy="26" r="4" fill="%s"/>' % A +
         _txt(74, 22, "peak", A, 8) +
         '<path d="M88 22 L102 25" stroke="%s" stroke-width="1.5"/>' % A),
    [
        ("text puts a string at a data point",
         "Coordinates are in data units unless you say otherwise.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 13)
y = np.array([12, 15, 14, 18, 22, 25, 24, 27, 23, 20, 18, 21])

fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.plot(x, y, marker="o")

peak = y.argmax()
ax.text(x[peak], y[peak] + 1, "peak: %d" % y[peak], ha="center", fontsize=10)

print("text(x, y, s) places s at the DATA coordinate (x, y).")
print("ha / va control which part of the text sits there:")
print("   ha = left | center | right")
print("   va = top | center | bottom | baseline")
print()
print("Without them the text starts at the point and runs right, which")
print("is rarely where you want it.")'''),

        ("annotate draws the arrow too",
         "Two coordinates: what you are pointing at, and where the label goes.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 200)
y = np.sin(x) * np.exp(-x / 6)

fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.plot(x, y)

i = y.argmin()
ax.annotate("lowest point",
            xy=(x[i], y[i]),
            xytext=(x[i] + 1.5, y[i] - 0.25),
            arrowprops=dict(arrowstyle="->", color="crimson"),
            fontsize=10)

print("xy      = the point being annotated")
print("xytext  = where the text sits")
print("arrowprops = how they are joined; omit it for no arrow")
print()
print("arrowstyle: '->', '-|>', 'fancy', 'wedge'")
print("connectionstyle='arc3,rad=0.3' curves the arrow, which helps when")
print("a straight one would cross the data.")'''),

        ("Reference lines",
         "A threshold or a mean, drawn across the whole axes.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
x = np.arange(40)
y = rng.normal(100, 15, 40)

fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.plot(x, y, marker="o", markersize=4)

ax.axhline(y.mean(), color="crimson", linestyle="--", linewidth=1,
           label="mean %.1f" % y.mean())
ax.axvline(20, color="grey", linestyle=":", linewidth=1)
ax.axhspan(y.mean() - y.std(), y.mean() + y.std(),
           color="crimson", alpha=0.08, label="+/- 1 sd")
ax.legend()

print("axhline / axvline span the whole axes regardless of the limits.")
print("axhspan / axvspan shade a band.")
print()
print("These stay correct when the data changes, which a hard-coded")
print("plot([0, 40], [mean, mean]) does not.")'''),

        ("Coordinate systems",
         "Data units, axes fractions, or figure fractions - and when each is right.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.plot(x, np.sin(x))

ax.text(5, 0.5, "data coords (5, 0.5)", ha="center", color="crimson")
ax.text(0.02, 0.95, "axes coords (0.02, 0.95)", transform=ax.transAxes,
        va="top", color="steelblue")
fig.text(0.5, 0.01, "figure coords - bottom centre", ha="center", fontsize=8)

print("default          : data coordinates, so the text moves if the")
print("                   limits change")
print("transform=ax.transAxes : 0-1 across the axes, so a corner label")
print("                   stays in the corner whatever the data")
print("fig.text         : 0-1 across the whole figure")
print()
print("A caption or a note belongs in axes or figure coordinates. A")
print("label for a specific point belongs in data coordinates.")'''),

        ("Highlighting a region",
         "Shading is quieter than an arrow and often says more.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(60)
rng = np.random.default_rng(1)
y = rng.normal(0, 1, 60).cumsum() + 20

fig, ax = plt.subplots(figsize=(7, 3.2))
ax.plot(x, y, color="0.3")

ax.axvspan(24, 34, color="crimson", alpha=0.12)
ax.text(29, ax.get_ylim()[1], "incident", ha="center", va="top",
        fontsize=9, color="crimson")

above = y > y.mean()
ax.fill_between(x, y.mean(), y, where=above, alpha=0.25, color="steelblue")

print("axvspan marks a period. fill_between with `where` shades only")
print("the parts meeting a condition.")
print()
print("where= needs interpolate=True if you want the shading to stop")
print("exactly at the crossing rather than at the nearest data point.")'''),

        ("Restraint",
         "Every annotation competes with the data for attention.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 13)
y = np.array([12, 15, 14, 18, 22, 25, 24, 27, 23, 20, 18, 21])

fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.4))

a.plot(x, y, marker="o")
for xi, yi in zip(x, y):
    a.annotate(str(yi), (xi, yi), textcoords="offset points",
               xytext=(0, 6), ha="center", fontsize=8)
a.set_title("every point labelled")

b.plot(x, y, marker="o", color="0.6")
i = y.argmax()
b.plot([x[i]], [y[i]], marker="o", color="crimson", markersize=9)
b.annotate("peak, %d" % y[i], (x[i], y[i]), textcoords="offset points",
           xytext=(8, 4), color="crimson", fontsize=10)
b.set_title("one point highlighted")

print("Twelve labels are twelve things to read. One is a message.")
print()
print("textcoords='offset points' with xytext=(dx, dy) shifts the label")
print("by a fixed distance from the point, which keeps the gap constant")
print("whatever the axis limits are.")'''),
    ],
    [
        "<code>ax.text(x, y, s)</code> places text at a <strong>data</strong> coordinate; <code>ha</code> and <code>va</code> decide which part of the text sits there.",
        "<code>annotate</code> takes <code>xy</code> (the point) and <code>xytext</code> (the label), with <code>arrowprops</code> to join them.",
        "<code>axhline</code>, <code>axvline</code> and <code>axhspan</code> span the axes regardless of limits, and stay correct when the data changes.",
        "<code>transform=ax.transAxes</code> uses 0&ndash;1 axes fractions, so a corner label stays in the corner whatever the data does.",
        "<code>fill_between(..., where=cond)</code> shades only the parts meeting a condition; add <code>interpolate=True</code> to stop at the crossing.",
        "<code>textcoords=\"offset points\"</code> shifts a label a fixed distance from its point, which survives changes to the limits.",
    ],
    '''
title: Annotating a Plot
intro: Text, arrows and reference lines - saying what the chart is for.

## text

`ax.text(x, y, "some words")` places text at a point in **data coordinates**.

`ha` (horizontal alignment) and `va` (vertical alignment) decide which part of the text sits at that point: `ha="center"` centres it, `va="bottom"` puts its bottom edge there. Without them, text starts at the point and runs to the right, which is rarely where you want it.

Because the coordinates are data units, the text moves when the axis limits change &mdash; correct for labelling a data point, wrong for a caption.

## annotate

`ax.annotate` is `text` with two positions and an optional arrow:

```python
ax.annotate("lowest point",
            xy=(x, y),               # the point
            xytext=(x + 1, y - 0.3), # the label
            arrowprops=dict(arrowstyle="->"))
```

Omit `arrowprops` and it is text with an offset. Include it and matplotlib draws a connector.

`arrowstyle` takes `"->"`, `"-|>"`, `"fancy"`, `"wedge"` and others. `connectionstyle="arc3,rad=0.3"` curves the arrow, which is how you route it around the data rather than through it.

`textcoords="offset points"` with `xytext=(dx, dy)` positions the label a fixed number of **points** from the target, instead of at another data coordinate. That is usually what you want: the gap stays constant when the limits change, where a data-coordinate offset would grow or shrink.

## Reference lines

`ax.axhline(value)` draws a horizontal line across the whole axes; `axvline` the vertical equivalent. They span the full width regardless of the current limits, and keep doing so if the limits change.

`axhspan(lo, hi)` and `axvspan` shade a band between two values.

These are better than plotting the line yourself. `ax.plot([0, 40], [mean, mean])` hard-codes the x range, and stops spanning the axes as soon as the data grows.

Typical uses: a target or threshold, a mean, a standard-deviation band, the date of a known event.

Label them &mdash; either through `label=` and a legend, or with text at one end &mdash; because an unexplained line is a question rather than an answer.

## Coordinate systems

Three systems, and choosing correctly is what makes annotations survive changes to the data.

**Data coordinates** (the default) &mdash; for anything attached to a specific value.

**Axes coordinates** &mdash; `transform=ax.transAxes`, running 0 to 1 across the axes. A label at `(0.02, 0.95)` sits just inside the top-left corner whatever the data is. This is right for a panel letter, a note, a sample size.

**Figure coordinates** &mdash; `fig.text(0.5, 0.01, ...)`, running 0 to 1 across the whole figure. Right for a source note or a caption under a grid of panels.

The mistake is putting a corner label in data coordinates: it looks correct until the data changes, then drifts into the middle of the plot or off the edge entirely.

## Shading regions

`fill_between(x, y1, y2)` fills between two curves, or between a curve and a constant.

`where=condition` restricts it to the parts where a boolean array is true &mdash; shading only where a series is above its mean, or above a threshold.

Add `interpolate=True` and the shading stops exactly at the crossing point; without it, it stops at the nearest data point, leaving a small notch. On coarsely sampled data that notch is visible and looks like a mistake.

`fill_between` is also how you draw a confidence band, with the upper and lower bounds as the two curves and `alpha` around 0.2.

## Restraint

This is the part that matters most and is hardest to apply.

Every annotation competes with the data for attention. A chart with twelve labelled points has twelve things to read and no message. A chart with one highlighted point and one label has a message.

The useful question is what the reader should take away, and then annotating **that** and nothing else. Greying the rest of the series and colouring the highlighted part is often more effective than adding an arrow, because it directs attention without adding ink.

If several things genuinely need pointing out, that is usually a sign the chart is trying to say more than one thing, and two charts would each say theirs more clearly.

## Boxes behind text

`bbox=` puts a patch behind a label, which is how you keep text readable over busy data:

```python
ax.text(x, y, "peak", bbox=dict(boxstyle="round,pad=0.3",
                                facecolor="white", alpha=0.8, edgecolor="none"))
```

`boxstyle` takes `"round"`, `"square"`, `"larrow"` and others, with `pad` controlling the margin.

A white box at 80% alpha is the standard treatment for a label that must sit over a line or a filled region. Without it, text over data is legible in the draft and unreadable once the data changes.

## Annotating a specific series

Text placed at the end of a line is the most useful annotation there is, and the position should come from the data:

```python
ax.text(x[-1], y[-1], f"  {name}", va="center", color=line.get_color())
```

Taking the colour from the artist ties the label to its line without repeating a colour constant, and it keeps working when the cycle changes.

The leading spaces are a crude but effective offset; `annotate` with `textcoords="offset points"` is the tidier version.

Leave room for the labels with `ax.set_xlim(right=x.max() * 1.15)`, or they run off the edge.

## Arrows

`arrowprops` is a dict, and the two useful spellings are:

`dict(arrowstyle="->")` &mdash; the modern form, with styles like `"->"`, `"-|>"`, `"fancy"`.

`dict(facecolor="black", shrink=0.05)` &mdash; the older form, which produces a filled arrow.

`connectionstyle="arc3,rad=0.2"` curves the connector. A slight curve often reads better than a straight line, because it does not look like part of the data.

`shrinkA` and `shrinkB` pull the ends back from the text and the target, which stops the arrowhead touching the point it is identifying.

## Guides and callouts

A few patterns recur often enough to be worth naming.

**A threshold with a label at the end**: `axhline` plus text at the right edge in axes coordinates for x and data coordinates for y &mdash; `ax.text(1.01, value, "target", transform=ax.get_yaxis_transform())`.

**A shaded period with a caption at the top**: `axvspan` plus text at `ax.get_ylim()[1]` with `va="top"`.

**A value callout**: a single marker in a strong colour, plus text offset from it.

`ax.get_yaxis_transform()` is the blended transform used above: x in axes fractions, y in data units. Its counterpart `get_xaxis_transform()` does the reverse, and between them they place edge labels that stay put when the data changes.

## Too much of it

The failure mode of annotation is a chart where everything is emphasised, which is the same as nothing being emphasised.

A useful discipline is to write the sentence the chart is meant to support, and then annotate only what that sentence refers to. If the sentence has two clauses about different things, that is two charts.

## Annotation as editing

The most useful way to think about annotation is as **editing** rather than addition.

A chart shows everything in the data equally. Annotation is where you say which part matters &mdash; and the strongest form of that is usually subtraction, not addition: greying the context, thinning the lines that are not the subject, removing the gridlines that are not being read.

A highlighted line with a label at its end and everything else in grey carries more meaning than the same chart with an arrow and a paragraph of text, because the emphasis is in the visual hierarchy rather than in something extra to read.

Add annotation when it names something the reader could not derive; remove weight from everything that is not it.

## Keeping annotations correct

Annotations placed by hand go stale, because the data changes and the coordinates do not.

Three habits keep them honest:

**Compute the position from the data.** `ax.annotate(..., xy=(x[i], y[i]))` with `i = y.argmax()` follows the peak wherever it moves.

**Compute the text from the data.** `f"peak {y.max():.1f}"` cannot disagree with the chart.

**Use axes coordinates for anything not attached to a value.** A corner note in data coordinates drifts as soon as the limits change.

A hard-coded annotation is correct exactly once, and there is nothing to warn you when it stops being.

## Annotating for different readers

How much annotation a chart needs depends entirely on who reads it and how long they have.

**A chart in a presentation** gets one annotation, large, saying the thing the speaker is about to say. Everything else is removed, because the audience has seconds and cannot re-read.

**A chart in a report** can carry two or three, because the reader controls the pace and can look between the chart and the text.

**A chart in an appendix** may carry none, because its job is to be available rather than to argue.

**A chart for yourself** needs none at all.

The common error is annotating a presentation chart like a report chart: four callouts, a legend, a subtitle and a source line, none of which can be read from the back of a room.

Writing the sentence the chart supports, and then annotating only the words in that sentence, resolves it in every case.

## In summary

`text` places a string at a data coordinate, with `ha` and `va` deciding which part of it sits there.

`annotate` adds a second position and an optional arrow, and `textcoords="offset points"` keeps the gap constant when the limits change.

`axhline`, `axvline` and the span functions cover thresholds and periods, and stay correct when the data grows.

`transform=ax.transAxes` is for anything not attached to a value, so a corner note stays in the corner.

`fill_between(..., where=...)` shades a condition, with `interpolate=True` to stop at the crossing.

And the hardest part is restraint: every annotation competes with the data, and a chart with one highlighted point says more than one with twelve labels.

## Text that scales

An annotation sized in points stays the same physical size when the figure changes, which means it occupies a different fraction of a small figure than a large one.

For a figure that will be produced at several sizes, three options:

**Set font sizes in the style** relative to a base `font.size`, so changing one value scales everything together.

**Compute sizes from the figure size**, which is what a house function can do: `fontsize = 4 + fig.get_size_inches()[0]`.

**Draw at the final size** and avoid the problem, which is the recommendation everywhere else in this track.

The failure to avoid is annotating a figure at screen size and then exporting it at a third of that for a document, where a comfortable label becomes unreadable and an arrow becomes a hairline.

Looking at the exported file, at the size it will be seen, is the check that catches all of it.

## One more thing

`ax.annotate` accepts `xycoords` as well as `textcoords`, so the point being annotated can itself be in axes or figure coordinates rather than data ones.

That is how you draw an arrow from a corner note to a data point &mdash; text anchored to the corner in axes coordinates, target in data coordinates &mdash; which stays correct as the data changes.

## The short version

Annotation is where a chart stops showing and starts saying.

The technique is straightforward; the discipline is not. One thing pointed out clearly beats five things labelled, and greying the context is usually more effective than adding an arrow.

## Reading the code back

An annotation has three parts: what is being pointed at, where the label sits, and which coordinate system each uses. Getting the third right is what makes the annotation survive a change in the data, and it is the part most often left to chance. Computing both the position and the text from the data means the chart cannot contradict itself.
''',
    [
        {"q": "What do `ha` and `va` control in `ax.text`?",
         "options": ["The font", "Which part of the text sits at the given point", "The colour", "The rotation"],
         "answer": 1,
         "why": "Without them, text starts at the point and runs right - rarely where you want it."},
        {"q": "What are `xy` and `xytext` in `annotate`?",
         "options": ["Two labels", "The point being annotated, and where the text sits", "x and y data", "Offsets"],
         "answer": 1,
         "why": "arrowprops joins them; omit it for text with an offset and no arrow."},
        {"q": "Why use `axhline` rather than plotting the line yourself?",
         "options": ["It is faster", "It spans the axes regardless of limits, and stays correct when the data changes", "It is coloured differently", "It adds a legend"],
         "answer": 1,
         "why": "ax.plot([0, 40], [mean, mean]) hard-codes the x range and stops spanning as soon as the data grows."},
        {"q": "Where should a corner note like a sample size be placed?",
         "options": ["Data coordinates", "Axes coordinates via transform=ax.transAxes", "Figure coordinates always", "In the title"],
         "answer": 1,
         "why": "A corner label in data coordinates looks right until the data changes, then drifts into the plot or off the edge."},
    ],
)


# ---------------------------------------------------------------------------
# 11. Saving figures
# ---------------------------------------------------------------------------
topic(
    "saving_figures",
    "Saving Figures",
    "Output",
    "savefig, dpi and the arguments that decide whether the file looks like the "
    "screen.",
    _svg(_box(20, 22, 60, 44, S, A) + _txt(50, 48, "figure", A, 8) +
         _arrow(84, 44, 100, 44) +
         _box(106, 26, 34, 36, S, M) + _txt(123, 47, "png", M, 8)),
    [
        ("savefig writes what the figure declares",
         "Not what the screen shows, which is why sizes surprise people.",
         '''import matplotlib.pyplot as plt
import io, os

fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
ax.plot([1, 2, 3], [2, 1, 3])
ax.set_title("6 x 3 inches at 100 dpi")

buf = io.BytesIO()
fig.savefig(buf, format="png")
size = len(buf.getvalue())

print("figsize    :", fig.get_size_inches(), "inches")
print("dpi        :", fig.dpi)
print("pixels     : %d x %d" % (6 * 100, 3 * 100))
print("file bytes :", size)
print()
print("figsize is in INCHES and dpi is dots per inch, so the pixel")
print("dimensions are their product. To get a 1200px wide image, use")
print("figsize=(6, 3) with dpi=200, or figsize=(12, 6) with dpi=100 -")
print("and those two are not the same: the second has smaller text.")'''),

        ("dpi changes apparent text size",
         "Because the text is sized in points, which are physical units.",
         '''import matplotlib.pyplot as plt
import io

for figsize, dpi in [((4, 2), 200), ((8, 4), 100)]:
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.plot([1, 2, 3], [2, 1, 3])
    ax.set_title("figsize=%s dpi=%d" % (figsize, dpi))
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    print("figsize %-8s dpi %3d -> %d x %d px, %5d bytes"
          % (str(figsize), dpi, figsize[0]*dpi, figsize[1]*dpi, len(buf.getvalue())))

print()
print("Both are 800x400. The first has text twice as large relative to")
print("the plot, because 10-point text is 10 points on a 4-inch figure")
print("and 10 points on an 8-inch one.")
print()
print("So: choose figsize for the layout, dpi for the resolution.")'''),

        ("bbox_inches='tight'",
         "The fix for labels cut off at the edge.",
         '''import matplotlib.pyplot as plt
import io

fig, ax = plt.subplots(figsize=(4, 2.5))
ax.plot([1, 2, 3], [2, 1, 3])
ax.set_ylabel("a rather long y axis label")
ax.set_title("title")

plain = io.BytesIO(); fig.savefig(plain, format="png")
tight = io.BytesIO(); fig.savefig(tight, format="png", bbox_inches="tight")

print("default          : %d bytes" % len(plain.getvalue()))
print("bbox_inches tight: %d bytes" % len(tight.getvalue()))
print()
print("'tight' recomputes the bounding box to include everything drawn,")
print("so labels outside the axes are not cropped. It also changes the")
print("output size, which matters if you need an exact pixel count.")
print()
print("pad_inches=0.1 controls the border it leaves.")'''),

        ("Vector or raster",
         "PNG for the web, PDF or SVG for print and for anything to be resized.",
         '''import matplotlib.pyplot as plt
import numpy as np
import io

rng = np.random.default_rng(0)
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(rng.random(200).cumsum())
ax.set_title("200 points")

for fmt in ["png", "pdf", "svg"]:
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt)
    print("%-4s %7d bytes" % (fmt, len(buf.getvalue())))

print()
print("png : pixels. Fixed resolution, small for simple charts.")
print("pdf : vector. Scales to any size, embeds fonts, right for print.")
print("svg : vector, and editable afterwards in Inkscape or a browser.")
print()
print("Vector formats grow with the NUMBER OF ELEMENTS, so a scatter of")
print("100,000 points makes an enormous PDF. Rasterise those layers.")'''),

        ("Transparency and the background",
         "The default is a white background, which is wrong on a dark page.",
         '''import matplotlib.pyplot as plt
import io

fig, ax = plt.subplots(figsize=(5, 2.5))
ax.plot([1, 2, 3], [2, 1, 3], color="crimson", linewidth=2)
ax.set_title("saved three ways")

opts = [
    dict(),
    dict(transparent=True),
    dict(facecolor="#222222"),
]
for o in opts:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", **o)
    print("%-28s %6d bytes" % (str(o) if o else "default (white)", len(buf.getvalue())))

print()
print("transparent=True drops both the figure and axes background, so")
print("the chart sits on whatever is behind it.")
print()
print("Note the TEXT stays dark either way - a transparent figure on a")
print("dark background still needs its text and spines recoloured.")'''),

        ("Saving in a loop",
         "The pattern that works, and the one that exhausts memory.",
         '''import matplotlib.pyplot as plt
import numpy as np
import io

rng = np.random.default_rng(1)

sizes = []
for i in range(5):
    fig, ax = plt.subplots(figsize=(3, 1.6))
    ax.plot(rng.random(30).cumsum())
    ax.set_title("chart %d" % i, fontsize=9)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    sizes.append(len(buf.getvalue()))
    plt.close(fig)                      # <- the important line

print("saved %d charts, sizes: %s" % (len(sizes), sizes))
print("figures still open:", len(plt.get_fignums()))
print()
print("Without plt.close(fig) they all stay open, matplotlib warns")
print("after 20, and a long loop runs out of memory.")

fig, ax = plt.subplots(figsize=(4, 2))
ax.bar(range(5), sizes)
ax.set_title("file sizes")'''),
    ],
    [
        "Pixel size is <code>figsize &times; dpi</code>. <code>figsize</code> is inches, and it decides how large the text looks relative to the plot.",
        "The same pixel dimensions from a small figure at high dpi and a large one at low dpi are <strong>not</strong> equivalent &mdash; text scales differently.",
        "<code>bbox_inches=\"tight\"</code> stops labels being cropped, and changes the output size as a side effect.",
        "PNG for the web; <strong>PDF or SVG</strong> for print or anything that will be resized.",
        "Vector files grow with the <strong>number of elements</strong>, so a huge scatter belongs in a rasterised layer.",
        "<code>transparent=True</code> drops the background, but the <strong>text stays dark</strong> &mdash; a figure for a dark page needs its colours changed too.",
    ],
    '''
title: Saving Figures
intro: savefig, dpi, and the arguments that decide whether the file looks like the screen.

## Size and resolution

A figure has a size in **inches** (`figsize`) and a resolution in **dots per inch** (`dpi`). The saved image is their product in pixels.

`figsize=(6, 3)` at `dpi=100` gives 600&times;300. At `dpi=200` it gives 1200&times;600.

That much is arithmetic. The part that catches people is that **these two are not interchangeable**:

`figsize=(4, 2), dpi=200` &rarr; 800&times;400
`figsize=(8, 4), dpi=100` &rarr; 800&times;400

Same pixels, different-looking charts. Text is sized in **points**, a physical unit, so 10-point text occupies a tenth of an inch either way. On the 4-inch figure that is a large fraction of the width; on the 8-inch one it is half as much.

The rule that follows: choose `figsize` for the **layout** &mdash; how big the text should look relative to the plot &mdash; and `dpi` for the **resolution**. Then scaling up for a high-resolution export changes only sharpness, not proportions.

A common mistake is making a figure bigger to get more detail and finding the text has shrunk relative to everything else.

## bbox_inches

By default `savefig` writes exactly the declared figure area. Labels, titles and legends drawn outside the axes may fall outside it and be cropped.

`bbox_inches="tight"` recomputes the bounding box to include everything drawn. It is the fix for the very common "my y-axis label is missing from the saved file".

Two consequences: the output dimensions are no longer exactly `figsize &times; dpi`, and `pad_inches` controls the margin it leaves. If you need an exact pixel size, use layout management instead and leave the bbox alone.

## Formats

**PNG** is raster: a grid of pixels. Right for the web, for slides, and anywhere the display size is known. Small for simple charts.

**PDF** is vector: shapes and text. Scales to any size without blurring, embeds fonts, and is what a journal or a print process wants.

**SVG** is vector and text-based, so it can be edited afterwards in Inkscape or styled with CSS in a browser.

**JPEG** should be avoided for charts: it is lossy in a way that puts artefacts around sharp edges and text, which is exactly what a chart is made of.

The trade-off with vector formats is that file size grows with the **number of elements**, not the image dimensions. A line chart is tiny; a scatter plot of 100,000 points is an enormous PDF that may take a viewer minutes to render.

`rasterized=True` on a specific artist stores just that layer as pixels while keeping text and axes as vectors, which gives a small file with sharp labels.

## Background

The default background is white for both the figure and the axes.

`transparent=True` makes both transparent, so the chart sits on whatever is behind it. `facecolor="#222"` sets a specific colour.

The catch: transparency changes the background and **not the foreground**. Text, spines and tick labels stay their original dark colour, so a transparent figure dropped onto a dark slide has invisible labels. Making a chart for a dark background means changing the text and line colours too, which is what a dark style sheet does.

## Saving in a loop

The pattern for generating many charts:

```python
for group, data in groups:
    fig, ax = plt.subplots()
    ...
    fig.savefig(f"{group}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
```

`plt.close(fig)` is the line people omit. Without it every figure stays open, matplotlib warns after twenty, and a loop over a few thousand groups exhausts memory.

For output that goes into a document, saving as PDF and letting the document scale it usually beats guessing a dpi.

And `savefig` accepts a file-like object as well as a path, which is how you write straight into a buffer for a web response or a test &mdash; as every editor on this page does, since there is no filesystem to write to.

## dpi in three places

`dpi` appears in the figure, in `savefig`, and in rcParams, and they interact.

`plt.subplots(dpi=100)` sets the figure's own dpi, which affects on-screen size.

`fig.savefig(path, dpi=200)` overrides it for that file.

`rcParams["savefig.dpi"]` sets the default for saving, and defaults to `"figure"`, meaning "use the figure's".

The practical consequence is that a figure looking right on screen can save at a different resolution than expected, and passing `dpi` explicitly at save time removes the question.

Common values: 100 for a quick look, 150&ndash;200 for slides and web, 300 for print, 600 for a journal that asks for it.

## Metadata and reproducibility

`savefig` accepts a `metadata` dict, which for PNG and PDF is written into the file.

Recording the script, the data version and the timestamp there means a chart found later can be traced back:

```python
fig.savefig(path, metadata={"Software": "analysis.py", "Creation Date": stamp})
```

A more visible version is a small caption in figure coordinates giving the source and date, which survives the chart being copied into a document where the file metadata does not follow.

## Vector text and fonts

By default, PDF and SVG output stores text as **text**, which keeps it selectable and searchable, and requires the reader to have the font.

`rcParams["pdf.fonttype"] = 42` embeds the font as TrueType, making the file self-contained at the cost of size. Journals frequently require this, and it is the fix when a submitted figure renders in the wrong typeface.

`rcParams["svg.fonttype"] = "none"` does the opposite for SVG, leaving text as text so it can be styled with CSS in a browser &mdash; useful for the web, wrong for a document.

## Saving several formats

A common pattern is one call per format from the same figure:

```python
for ext in ("png", "pdf"):
    fig.savefig(f"{name}.{ext}", dpi=200, bbox_inches="tight")
```

The figure can be saved any number of times; nothing is consumed. A PNG for the draft and a PDF for the final document, from one drawing pass.

## Buffers rather than files

`savefig` accepts any file-like object:

```python
buf = io.BytesIO()
fig.savefig(buf, format="png")
```

That is how a chart becomes a web response, an email attachment, or a test assertion &mdash; and how these pages work, since the browser has no filesystem to write into.

`format` is required when there is no filename to infer it from, which is the usual first error with this.

## A saving function

For a project producing many figures, a small wrapper enforces consistency:

```python
def save(fig, name, formats=("png", "pdf")):
    for ext in formats:
        fig.savefig(f"figures/{name}.{ext}", dpi=200,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
```

One place to change the dpi, the formats, the background and the padding, and the `close` is not forgotten.

Adding the source script and a timestamp to the metadata, or as a small caption, makes a figure traceable months later &mdash; which is the difference between a chart that can be updated and one that has to be remade.

## Common saving problems

**Labels cut off** &mdash; missing `bbox_inches="tight"` or layout management.

**Blurry in a document** &mdash; a raster format at too low a dpi; use PDF, or 200&ndash;300 dpi.

**Enormous PDF** &mdash; a dense scatter stored as vector; rasterise that layer.

**Wrong font on another machine** &mdash; the font was not embedded; `pdf.fonttype = 42`.

**Invisible text on a dark background** &mdash; `transparent=True` changed the background and not the foreground.

**Different from the screen** &mdash; the screen was a different size; the file is authoritative.

Each has a one-line fix, and all of them are easier to prevent in a saving function than to diagnose per figure.

## Figures in a pipeline

When charts are generated automatically &mdash; a weekly report, a dashboard build, a model evaluation &mdash; a few properties matter more than they do for a one-off.

**Determinism.** The same input should produce the same file. That means seeding any randomness, sorting anything whose order is not guaranteed, and pinning the style rather than inheriting whatever is configured.

**Self-description.** The chart should carry its own date range and source, because it will be found later without its context.

**Failure behaviour.** A chart generated from empty data should produce something explicit rather than an empty axes; a check and a clear message beats a blank rectangle in a report.

**Size predictability.** Labels grow with the data, so `bbox_inches="tight"` and a figure size derived from the number of categories prevent a layout that worked in testing from cropping in production.

None of these is about matplotlib specifically. They are the difference between a chart that runs unattended and one that has to be looked at every week.

## In summary

Pixel size is `figsize &times; dpi`, and `figsize` decides how large the text looks relative to the plot &mdash; so the two are not interchangeable ways of getting the same resolution.

`bbox_inches="tight"` is the fix for cropped labels, and changes the output dimensions as a side effect.

PNG for the web, PDF or SVG for print and anything resized, and never JPEG for a chart.

Vector file size grows with the number of elements, so a dense scatter wants `rasterized=True` on that artist.

`transparent=True` changes the background and not the text, so a chart for a dark page needs its foreground recoloured too.

And in any loop that saves, `plt.close(fig)` &mdash; the figures do not clean themselves up, and the warning arrives long after the memory has started growing.

## Choosing dpi and size together

The two are usually chosen backwards: a default size, then a dpi high enough to look sharp.

The order that works is destination first.

**Print at 300 dpi, one column wide** &rarr; `figsize=(3.4, 2.4)`, `dpi=300`, fonts around 8 points.

**A slide** &rarr; `figsize=(10, 5.6)`, `dpi=150`, fonts 14 or larger.

**A web page at 700 px wide** &rarr; `figsize=(7, 4)`, `dpi=200` for retina displays, then let CSS scale it down.

**A quick look** &rarr; whatever the default is.

Setting the size to the destination means the fonts can be chosen once and are right, and no scaling happens afterwards to disturb the proportions.

The test is whether the figure needs resizing when it arrives where it is going. If it does, it was drawn at the wrong size.

## Checking the output

The saved file is what other people see, and it differs from the screen in ways worth checking once per project rather than per figure.

**Open it at 100%.** Labels that are comfortable in a scaled preview may be too small.

**Check the edges.** Anything drawn outside the axes is the first thing to be cropped.

**Check the background.** A transparent figure over an unexpected background, or a white border around a dark chart.

**Check the file size.** A surprisingly large PDF means a dense artist that should be rasterised.

**Open it in the destination** &mdash; the document, the slide, the page &mdash; because that is where the size and the background are decided.

Doing this once when the saving function is written catches problems that would otherwise recur in every figure the project produces.

## One more thing

`fig.savefig` accepts `pad_inches=0` alongside `bbox_inches="tight"`, which removes the border entirely.

That is what you want for a figure being embedded in a layout that provides its own spacing, and what you do not want for one being viewed on its own, where the border is what stops the labels touching the edge.

## The short version

The saved file is the artefact; the screen is a preview.

Size and dpi are one decision made for the destination, `bbox_inches="tight"` prevents the most common cropping, vector formats need rasterised layers for dense data, and every loop that saves needs to close.

## Reading the code back

A save is one call with four arguments that matter: the format, the dpi, the bounding box and the background. Wrapping them in a project function means they are decided once, applied everywhere, and the close is not forgotten. The check that the output is right is to open the file at full size in the place it will be used.
''',
    [
        {"q": "`figsize=(4,2) dpi=200` and `figsize=(8,4) dpi=100` both give 800x400. How do they differ?",
         "options": ["Not at all", "Text is sized in points, so it looks twice as large relative to the smaller figure", "The second is sharper", "The first is smaller on disk"],
         "answer": 1,
         "why": "Choose figsize for layout and dpi for resolution - then a high-resolution export changes sharpness, not proportions."},
        {"q": "Your saved figure is missing its y-axis label. What fixes it?",
         "options": ["A higher dpi", "bbox_inches='tight'", "A larger dpi", "transparent=True"],
         "answer": 1,
         "why": "savefig writes the declared figure area, and labels drawn outside it get cropped. It also changes the output dimensions."},
        {"q": "Why can a scatter of 100,000 points make a huge PDF?",
         "options": ["PDFs are inefficient", "Vector file size grows with the number of elements, not the image size", "The dpi is too high", "It does not"],
         "answer": 1,
         "why": "rasterized=True on that artist stores it as pixels while keeping text and axes as vectors."},
        {"q": "What does `transparent=True` NOT change?",
         "options": ["The figure background", "The axes background", "The text and spine colours", "The file format"],
         "answer": 2,
         "why": "A transparent figure dropped on a dark slide has invisible labels - a dark background needs the foreground recoloured too."},
    ],
)


# ---------------------------------------------------------------------------
# 12. Dates on an axis
# ---------------------------------------------------------------------------
topic(
    "dates_on_axes",
    "Dates on an Axis",
    "Working with Data",
    "Time series plotting - the locators and formatters that stop the labels "
    "colliding.",
    _svg(_box(18, 20, 124, 44, "none", B) +
         '<polyline points="26,54 50,40 74,46 98,30 130,36" fill="none" stroke="%s" stroke-width="2"/>' % A +
         _txt(38, 76, "Jan", M, 7) + _txt(74, 76, "Apr", M, 7) + _txt(114, 76, "Jul", M, 7)),
    [
        ("Real dates plot as dates",
         "Pass datetimes and matplotlib gives you a date axis for free.",
         '''import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

start = dt.date(2024, 1, 1)
days = [start + dt.timedelta(days=i) for i in range(120)]
y = np.random.default_rng(0).normal(0, 1, 120).cumsum() + 20

fig, (a, b) = plt.subplots(2, 1, figsize=(7, 4))

a.plot(range(120), y)
a.set_title("plotted against 0..119 - the axis says nothing")

b.plot(days, y)
b.set_title("plotted against dates")

print("The x axis type is decided by what you pass in.")
print("Strings are treated as CATEGORIES - one tick per value, in the")
print("order given, which is why a string date axis looks crowded and")
print("ignores gaps between days.")'''),

        ("Strings are not dates",
         "They plot in the order given, evenly spaced, whatever the gaps.",
         '''import matplotlib.pyplot as plt
import datetime as dt

labels = ["2024-01-01", "2024-01-02", "2024-03-01", "2024-03-02"]
real = [dt.date.fromisoformat(s) for s in labels]
y = [1, 2, 3, 4]

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.plot(labels, y, marker="o")
a.set_title("strings: evenly spaced")
a.tick_params(axis="x", rotation=45, labelsize=8)

b.plot(real, y, marker="o")
b.set_title("dates: the two-month gap is visible")
b.tick_params(axis="x", rotation=45, labelsize=8)

print("Two pairs of days, two months apart.")
print("As strings, all four points are equally spaced - the gap vanishes.")
print("As dates, the gap is drawn, which is the whole reason to use a")
print("date axis rather than category labels.")'''),

        ("Locators decide where the ticks go",
         "By month, by week, by day - rather than at arbitrary numbers.",
         '''import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

start = dt.date(2024, 1, 1)
days = [start + dt.timedelta(days=i) for i in range(240)]
y = np.random.default_rng(1).normal(0, 1, 240).cumsum()

fig, (a, b) = plt.subplots(2, 1, figsize=(7.5, 4.5))

a.plot(days, y)
a.set_title("automatic ticks")

b.plot(days, y)
b.xaxis.set_major_locator(mdates.MonthLocator())
b.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
b.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
b.set_title("one major tick per month, minor ticks on Mondays")

print("Locators: YearLocator, MonthLocator, WeekdayLocator, DayLocator,")
print("HourLocator, AutoDateLocator.")
print()
print("MonthLocator(interval=3) gives quarters. DayLocator(bymonthday=1)")
print("gives the first of each month.")'''),

        ("Formatters decide how they read",
         "strftime codes, and a concise formatter that avoids repetition.",
         '''import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

start = dt.datetime(2024, 3, 1)
stamps = [start + dt.timedelta(hours=6 * i) for i in range(80)]
y = np.random.default_rng(2).normal(0, 1, 80).cumsum()

fig, (a, b) = plt.subplots(2, 1, figsize=(7.5, 4.5))

a.plot(stamps, y)
a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
a.tick_params(axis="x", rotation=30, labelsize=8)
a.set_title("full timestamps - repetitive and crowded")

b.plot(stamps, y)
loc = mdates.AutoDateLocator()
b.xaxis.set_major_locator(loc)
b.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))
b.set_title("ConciseDateFormatter")

print("%Y year, %m month number, %b month name, %d day,")
print("%H hour, %M minute")
print()
print("ConciseDateFormatter drops what is repeated - it prints the year")
print("once at the start rather than on every label, which is usually")
print("what you would have written by hand.")'''),

        ("Rotating and thinning labels",
         "When the labels still collide.",
         '''import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

start = dt.date(2024, 1, 1)
days = [start + dt.timedelta(days=i) for i in range(60)]
y = np.random.default_rng(3).normal(0, 1, 60).cumsum()

fig, (a, b) = plt.subplots(2, 1, figsize=(7.5, 4.5))

a.plot(days, y)
a.xaxis.set_major_locator(mdates.DayLocator(interval=2))
a.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
a.set_title("every 2 days - collides")

b.plot(days, y)
b.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
b.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
b.set_title("weekly ticks - readable")

print("Three fixes, in order of preference:")
print("  1. fewer ticks - a coarser locator")
print("  2. shorter labels - '%d %b' rather than '%Y-%m-%d'")
print("  3. rotation - fig.autofmt_xdate() rotates and right-aligns")
print()
print("Rotation is the last resort, because slanted text is harder to")
print("read than horizontal text.")'''),

        ("Marking a period",
         "A date axis takes the same spans and lines as any other.",
         '''import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

start = dt.date(2024, 1, 1)
days = [start + dt.timedelta(days=i) for i in range(150)]
y = np.random.default_rng(4).normal(0, 1, 150).cumsum() + 30

fig, ax = plt.subplots(figsize=(7.5, 3.2))
ax.plot(days, y, color="0.35")

ax.axvspan(dt.date(2024, 3, 1), dt.date(2024, 4, 1),
           color="crimson", alpha=0.12)
ax.axvline(dt.date(2024, 3, 15), color="crimson", linestyle="--", linewidth=1)
ax.text(dt.date(2024, 3, 15), ax.get_ylim()[1], " launch",
        va="top", fontsize=9, color="crimson")

loc = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(loc)
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

print("axvspan and axvline take dates directly, because internally the")
print("axis is numeric - matplotlib stores dates as days since an epoch.")
print()
print("That is also why you can mix: ax.set_xlim takes dates or numbers.")'''),
    ],
    [
        "Pass real <code>date</code> or <code>datetime</code> objects and matplotlib builds a date axis; the type of the x data decides the axis type.",
        "<strong>Strings are categories</strong> &mdash; evenly spaced in the order given, so gaps between dates disappear.",
        "<strong>Locators</strong> place the ticks: <code>MonthLocator</code>, <code>WeekdayLocator</code>, <code>DayLocator</code>, with <code>interval=</code>.",
        "<strong>Formatters</strong> decide how they read; <code>ConciseDateFormatter</code> drops repeated parts like the year.",
        "For colliding labels, prefer <strong>fewer ticks</strong>, then shorter labels, and rotation only as a last resort.",
        "<code>axvspan</code> and <code>axvline</code> take dates directly, because the axis is numeric underneath &mdash; days since an epoch.",
    ],
    '''
title: Dates on an Axis
intro: Time series plotting, and the locators and formatters that stop labels colliding.

## The axis type follows the data

Pass a list of `datetime.date` or `datetime.datetime` objects &mdash; or a pandas `DatetimeIndex`, or NumPy `datetime64` &mdash; and matplotlib recognises them and builds a date axis. Tick positions and labels are then chosen in date units rather than arbitrary numbers.

Pass **strings** and you get something quite different: matplotlib treats them as categories. Each distinct string gets a position, evenly spaced, in the order supplied.

That difference matters more than it sounds. With categories, two readings a day apart and two readings two months apart are drawn the same distance apart. The gap in the data disappears, and the line implies a continuity that is not there.

Since dates from a CSV arrive as strings, this is a common and quiet failure. `pd.to_datetime` before plotting is the fix, and checking the dtype is how you notice.

## Locators

A **locator** decides where ticks go. The date locators think in calendar units:

`YearLocator()`, `MonthLocator()`, `WeekdayLocator(byweekday=MO)`, `DayLocator()`, `HourLocator()`, `MinuteLocator()`.

Each takes an `interval`, so `MonthLocator(interval=3)` gives quarterly ticks, and several take a `by...` argument &mdash; `DayLocator(bymonthday=1)` for the first of each month.

`AutoDateLocator()` chooses based on the visible range, and adapts if the axis is zoomed.

Minor ticks add structure without labels: monthly majors with weekly minors gives a sense of scale without crowding.

## Formatters

A **formatter** decides how a tick reads.

`DateFormatter("%d %b")` uses `strftime` codes: `%Y` four-digit year, `%y` two-digit, `%m` month number, `%b` abbreviated month name, `%d` day, `%H:%M` time.

`ConciseDateFormatter(locator)` is usually the better choice. It drops what is repeated &mdash; printing the year once at the left rather than on every label, and showing only the day number when the month is unchanged. That is what a person would do by hand, and it saves a great deal of horizontal space.

It needs the locator passed to it, because it decides what to omit based on the tick spacing.

## Crowded labels

Date labels collide more than any other kind, because they are long and there are many of them.

Three fixes, in order of preference:

**Fewer ticks.** A coarser locator. Fifteen readable ticks beat forty overlapping ones, and the reader was never going to use all forty.

**Shorter labels.** `"%d %b"` instead of `"%Y-%m-%d"`, or `ConciseDateFormatter`.

**Rotation.** `fig.autofmt_xdate()` rotates the labels and right-aligns them, and also makes room. It works, and slanted text is genuinely harder to read than horizontal text, so it belongs after the other two rather than instead of them.

A wider figure is the fourth option and often the honest one: a year of daily data does not fit legibly in four inches.

## Marking events

`axvline(date)` and `axvspan(start, end)` take dates directly.

That works because the date axis is numeric underneath &mdash; matplotlib converts dates to floating-point days since an epoch, plots the numbers, and formats the labels back into dates. `mdates.date2num` and `num2date` do the conversion explicitly when you need it.

The same fact explains why `set_xlim` accepts either dates or raw numbers, and why arithmetic on the limits works.

## With pandas

A pandas Series with a `DatetimeIndex` plots directly:

```python
ax.plot(series.index, series.values)
```

or `series.plot(ax=ax)`, which uses pandas' own date formatting. The two produce slightly different tick choices, and pandas' version is often good enough that no locator work is needed.

For a DataFrame, `df.plot(ax=ax)` draws every column against the index, which is the fastest route from a time-indexed frame to a chart &mdash; and the subject of a later module.

## Time zones and the axis

matplotlib converts datetimes to numbers using a fixed epoch, and time-zone-aware timestamps are converted to the axis's timezone before plotting.

`rcParams["timezone"]` sets it. If it does not match the data's, the labels are correct times in a different zone, and the shift is a whole number of hours &mdash; large enough to matter and small enough to overlook.

The reliable approach is the one from the pandas track: normalise to a single zone before plotting, and label the axis with which one.

## Gaps and non-trading days

A date axis draws real elapsed time, so a weekend appears as a gap.

For financial data that is usually unwanted: five trading days a week become a line with regular breaks, and a month of data has eight or nine of them.

Two options. Plot against an integer index and label the ticks with the dates, which removes the gaps at the cost of a slightly dishonest axis. Or accept the gaps, which is more truthful about elapsed time.

Which is right depends on whether the chart is about the market's behaviour over trading sessions or about calendar time. Both are defensible; picking without noticing is not.

## Resampling before plotting

A year of per-minute data is half a million points, and a chart seven inches wide has seven hundred pixel columns.

Resampling to a sensible frequency before plotting is usually better than drawing everything:

```python
daily = series.resample("D").mean()
ax.plot(daily.index, daily.values)
```

That is fewer artists, a smaller file, and a chart that looks identical &mdash; because the extra points were never distinguishable.

Where extremes matter, resampling to min and max per period and shading between them keeps the envelope, which is the technique from the performance module.

## Multiple time series with different ranges

Two series covering different date ranges plot happily on one axis, and the shorter one simply occupies part of the width.

That is correct and can mislead, because a series that starts later looks like it began at zero rather than being unobserved. Making the difference explicit &mdash; a note, or a shaded region marking where data exists &mdash; prevents the reading that something changed at that date.

The same applies to a series with a gap in the middle, where the broken line is the honest display and a joined one is not.

## Annotating dates

Every annotation method takes dates directly, because the axis is numeric underneath.

The pattern for marking an event:

```python
ax.axvline(event_date, color="crimson", linestyle="--", linewidth=1)
ax.text(event_date, 1.01, " launch", transform=ax.get_xaxis_transform(),
        rotation=0, fontsize=9, color="crimson")
```

`get_xaxis_transform()` puts x in data units and y in axes fractions, so the label sits just above the plot regardless of the data's range &mdash; which is what you want for an event marker that should stay at the top.

## Reading a time axis

Three things a reader needs from a dated axis, and which are frequently missing.

**The period covered**, which the first and last tick imply and a title states.

**The granularity** &mdash; whether a point is a day, a week or a month &mdash; which markers make explicit and a smooth line hides.

**Whether gaps are real.** A break in a line means missing data; a gap on the axis with the line continuing means the axis is categorical and the elapsed time is not being shown.

Stating the frequency in the title or the axis label &mdash; "Daily", "Monthly average" &mdash; costs a word and answers all three.

## Common date problems

**Labels overlapping** &mdash; too many ticks; use a coarser locator before rotating.

**Dates as categories** &mdash; strings not converted; gaps disappear and the spacing is wrong.

**A shifted axis** &mdash; a time-zone mismatch between the data and `rcParams["timezone"]`.

**Ticks in odd places** &mdash; an automatic locator on an unusual range; name the locator.

**A frequency string that no longer works** &mdash; pandas 2.2 renamed several of them.

**The line breaking at weekends** &mdash; real elapsed time, which is either correct or a reason to plot against an index.

The first two account for most of it, and both are visible immediately.

## Aggregating before plotting

Most time-series charts are better after aggregation than before it.

Per-minute data over a year is half a million points and roughly seven hundred pixel columns. Resampling to daily gives 365 points, a chart that draws instantly, and a picture that is visually identical because the extra points were never separable.

The choice of aggregation is a decision about what the chart is for:

**Mean** for a level &mdash; the typical value in each period.

**Sum** for a quantity &mdash; total sales per week.

**Min and max** shaded as a band, when the extremes are what matter and a mean would hide them.

**Last** for a state or a price, where the value at the end of the period is the meaningful one.

Plotting raw high-frequency data and letting the renderer overplot it is not more honest; it is the same information rendered less legibly, with whatever the overlapping happens to leave visible standing in for a summary you did not choose.

## In summary

Pass real datetimes and matplotlib builds a date axis; pass strings and it builds a categorical one where gaps disappear.

`pd.to_datetime` with an explicit `format` is faster and removes the day-first ambiguity.

Locators place the ticks in calendar units and formatters decide how they read, with `ConciseDateFormatter` dropping the repetition.

For crowded labels, fewer ticks first, shorter labels second, rotation last.

`axvline` and `axvspan` take dates directly, because the axis is numeric underneath.

And pandas 2.2 renamed the frequency aliases &mdash; `ME`, `h`, `min` &mdash; which is the usual reason a copied example stops working.

## Periods rather than instants

Much time-series data is about **periods** rather than points: monthly totals, weekly averages, daily counts.

Plotting a period as a point at its start implies the value occurred at that instant, and a line between two such points implies a smooth transition through the month.

Two displays are more honest for period data.

**Bars**, one per period, which say "this is the total for this interval" and have no between-values.

**A step line**, `ax.step(..., where="post")`, which holds the value across the period and changes at the boundary.

A line is still reasonable when the periods are short relative to the trend and the shape is the point &mdash; but it is a choice, and for something like monthly revenue a bar chart is frequently the better display and rarely the one reached for.

Labelling the axis with the period &mdash; "Month starting" &mdash; removes the remaining ambiguity about which end a point represents.

## A closing note

Time axes carry more conventions than any other kind, and most of the work is in the setup rather than the drawing.

Parse the dates properly, check the dtype, decide on a time zone, sort, and choose a frequency that matches the question. After that, the plotting is the same as any other line chart.

The two failures that matter are plotting strings instead of dates, which silently removes the gaps and misrepresents elapsed time, and letting the locator produce more labels than can be read, which is fixed by asking for fewer rather than by rotating them.

And frequency aliases changed in pandas 2.2, which accounts for a large share of examples that no longer run.

## The short version

A date axis is the difference between a chart of a time series and a chart of some values in order.

Parse properly, sort, choose a frequency that matches the question, and use fewer ticks than the default. The rest follows from the line-chart material.

## Reading the code back

A time-series chart is a line chart with three extra decisions: how the dates were parsed, which locator places the ticks, and which formatter writes them. All three are made before any styling, and getting the first wrong makes the other two irrelevant because the axis is not a timeline at all.
''',
    [
        {"q": "What happens if you plot date strings rather than date objects?",
         "options": ["Nothing different", "They are treated as categories - evenly spaced in the order given, so gaps disappear", "It raises", "They are parsed automatically"],
         "answer": 1,
         "why": "Dates from a CSV arrive as strings, so this is a common quiet failure. The line implies a continuity that is not there."},
        {"q": "What does a locator do?",
         "options": ["Formats the label text", "Decides where the ticks go", "Sets the limits", "Finds the data"],
         "answer": 1,
         "why": "Formatters decide how ticks read; locators decide where they are. Date locators think in calendar units."},
        {"q": "Why is `ConciseDateFormatter` usually better than `DateFormatter`?",
         "options": ["It is faster", "It drops repeated parts - the year appears once rather than on every label", "It rotates labels", "It adds minor ticks"],
         "answer": 1,
         "why": "It needs the locator passed to it, because what it omits depends on the tick spacing."},
        {"q": "Date labels are colliding. What should you try first?",
         "options": ["Rotate them", "Use fewer ticks with a coarser locator", "Shrink the font", "Remove the axis"],
         "answer": 1,
         "why": "Then shorter labels, and rotation last - slanted text is genuinely harder to read than horizontal text."},
    ],
)


# ---------------------------------------------------------------------------
# 13. Error bars and bands
# ---------------------------------------------------------------------------
topic(
    "error_bars_and_bands",
    "Error Bars and Bands",
    "Working with Data",
    "Showing uncertainty - and saying which kind you are showing.",
    _svg(_box(14, 16, 132, 58, "none", B) +
         '<path d="M40 30 L40 58 M34 30 L46 30 M34 58 L46 58" stroke="%s" stroke-width="2"/>' % A +
         '<path d="M76 24 L76 46 M70 24 L82 24 M70 46 L82 46" stroke="%s" stroke-width="2"/>' % A +
         '<path d="M112 38 L112 64 M106 38 L118 38 M106 64 L118 64" stroke="%s" stroke-width="2"/>' % A),
    [
        ("errorbar draws the interval",
         "Symmetric with one array, asymmetric with two rows.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 6)
y = np.array([10, 14, 12, 17, 15], dtype=float)
err = np.array([1.0, 2.0, 1.5, 0.8, 2.5])

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.errorbar(x, y, yerr=err, marker="o", capsize=4)
a.set_title("symmetric")

lo = np.array([0.5, 1.0, 0.8, 0.4, 1.2])
hi = np.array([2.0, 3.0, 1.6, 1.5, 3.0])
b.errorbar(x, y, yerr=[lo, hi], marker="o", capsize=4, color="crimson")
b.set_title("asymmetric: yerr=[lower, upper]")

print("yerr as one array  -> the same distance above and below")
print("yerr as [lo, hi]   -> different distances, given as POSITIVE")
print("                      offsets from the point")
print()
print("capsize adds the end caps; without it the bars are bare lines.")'''),

        ("Bands for continuous data",
         "<code>fill_between</code>, because a bar per point is unreadable on a curve.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 200)
y = np.sin(x)
sd = 0.1 + 0.15 * np.abs(np.cos(x))

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.errorbar(x, y, yerr=sd, alpha=0.4)
a.set_title("200 error bars: a smear")

b.plot(x, y, color="crimson")
b.fill_between(x, y - sd, y + sd, alpha=0.25, color="crimson")
b.set_title("a band")

print("Error bars suit a handful of discrete measurements.")
print("For a curve, fill_between shows the same information and stays")
print("readable at any number of points.")
print()
print("alpha around 0.2-0.3 keeps the central line clearly on top.")'''),

        ("Say which interval it is",
         "Standard deviation, standard error and a confidence interval differ by a "
         "lot.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
n = 40
sample = rng.normal(100, 15, n)

sd = sample.std(ddof=1)
se = sd / np.sqrt(n)
ci = 1.96 * se

fig, ax = plt.subplots(figsize=(6, 3))
for i, (label, half) in enumerate([("sd", sd), ("se", se), ("95% ci", ci)]):
    ax.errorbar([i], [sample.mean()], yerr=[[half], [half]],
                marker="o", capsize=6)
    ax.text(i, sample.mean() + half + 1, "%s: +/-%.1f" % (label, half),
            ha="center", fontsize=9)
ax.set_xticks(range(3))
ax.set_xticklabels(["sd", "se", "95% ci"])
ax.set_title("same data, three intervals")

print("sd     = %.2f  spread of the DATA" % sd)
print("se     = %.2f  uncertainty of the MEAN" % se)
print("95%% ci = %.2f  about 1.96 standard errors" % ci)
print()
print("They differ by a factor of six here. An unlabelled error bar is")
print("uninterpretable, which is why the caption has to say which it is.")'''),

        ("Bars with error bars",
         "The same <code>yerr</code> argument, and the same zero-baseline rule.",
         '''import matplotlib.pyplot as plt
import numpy as np

groups = ["a", "b", "c", "d"]
means = np.array([23, 31, 27, 35], dtype=float)
errs = np.array([3, 5, 2, 4], dtype=float)

fig, ax = plt.subplots(figsize=(6, 3))
ax.bar(groups, means, yerr=errs, capsize=5,
       color="steelblue", edgecolor="black", linewidth=0.5)
ax.set_ylabel("mean (95% ci)")

print("bar takes yerr directly.")
print()
print("error_kw passes styling through to the error bars:")
print("   error_kw=dict(ecolor='0.3', lw=1, capthick=1)")
print()
print("The overlap rule people remember - 'if the bars overlap it is not")
print("significant' - is wrong for confidence intervals of two means.")
print("Non-overlapping implies significance; overlapping does not imply")
print("its absence.")'''),

        ("Showing the data instead",
         "With few points, the observations beat any summary of them.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
groups = {"a": rng.normal(20, 3, 12),
          "b": rng.normal(24, 3, 12),
          "c": rng.normal(22, 9, 12)}

fig, (p, q) = plt.subplots(1, 2, figsize=(9, 3.2), sharey=True)

names = list(groups)
means = [groups[k].mean() for k in names]
sds = [groups[k].std(ddof=1) for k in names]
p.bar(names, means, yerr=sds, capsize=5, color="0.7")
p.set_title("bar + error bar")

for i, k in enumerate(names):
    vals = groups[k]
    p_x = np.full(len(vals), i) + rng.uniform(-0.12, 0.12, len(vals))
    q.scatter(p_x, vals, alpha=0.7, s=25)
    q.hlines(vals.mean(), i - 0.25, i + 0.25, color="crimson", linewidth=2)
q.set_xticks(range(3)); q.set_xticklabels(names)
q.set_title("the points themselves")

print("Group c has three times the spread of the others, and one clear")
print("outlier. The bar chart shows a taller error bar; the strip plot")
print("shows what is actually going on.")
print()
print("Jitter - a small random x offset - stops points overlapping.")'''),

        ("Bands from a model",
         "The prediction and its interval, drawn together.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(2)
x = np.sort(rng.uniform(0, 10, 40))
y = 2.0 * x + 5 + rng.normal(0, 3, 40)

coef = np.polyfit(x, y, 1)
xs = np.linspace(0, 10, 100)
fit = np.polyval(coef, xs)

resid = y - np.polyval(coef, x)
s = resid.std(ddof=2)

fig, ax = plt.subplots(figsize=(6.5, 3.5))
ax.scatter(x, y, alpha=0.7, s=30, label="observations")
ax.plot(xs, fit, color="crimson", linewidth=2, label="fit")
ax.fill_between(xs, fit - 1.96 * s, fit + 1.96 * s,
                color="crimson", alpha=0.15, label="+/-1.96 s")
ax.legend()

print("fit: y = %.2fx + %.2f" % (coef[0], coef[1]))
print("residual sd: %.2f" % s)
print()
print("This band is a rough PREDICTION interval - where new points")
print("should fall. A confidence interval for the LINE is narrower and")
print("bow-shaped, widest at the ends. They are different claims and")
print("get confused constantly.")'''),
    ],
    [
        "<code>errorbar(x, y, yerr=e)</code> is symmetric; <code>yerr=[lo, hi]</code> is asymmetric, given as <strong>positive offsets</strong>.",
        "For a curve, use <code>fill_between</code> &mdash; hundreds of error bars become a smear.",
        "<strong>Standard deviation, standard error and a confidence interval</strong> differ by large factors. An unlabelled interval is uninterpretable.",
        "Bars take <code>yerr</code> directly, and <code>error_kw</code> styles the whiskers.",
        "With few observations, <strong>showing the points</strong> with jitter beats any summary of them.",
        "A <strong>prediction</strong> interval and a <strong>confidence</strong> interval for the fitted line are different claims and are constantly confused.",
    ],
    '''
title: Error Bars and Bands
intro: Showing uncertainty, and saying which kind you are showing.

## errorbar

`ax.errorbar(x, y, yerr=err)` plots points with vertical intervals.

A single array or scalar gives **symmetric** bars &mdash; the same distance above and below. A `(2, n)` array or a list of two arrays gives **asymmetric** ones, with the first row the distance **below** and the second the distance **above**.

Both are given as positive offsets from the point, not as absolute positions. Passing absolute upper and lower bounds is a common mistake and produces enormous bars.

`xerr` does the same horizontally, and both can be used at once.

`capsize` adds the end caps; without it the bars are bare lines, which is harder to read against a busy background. `fmt="o"` sets the marker, and `fmt="none"` draws the bars with no marker at all.

## Bands

Error bars work for a handful of discrete measurements. On a curve with two hundred points they overlap into a grey smear that conveys nothing.

`fill_between(x, low, high)` is the continuous version:

```python
ax.plot(x, y)
ax.fill_between(x, y - sd, y + sd, alpha=0.25)
```

`alpha` around 0.2 to 0.3 keeps the central line clearly on top. Using the same colour for line and band ties them together; using a different one implies they are different series.

`fill_between` also takes `where=` to shade only part of the range, and `step="pre"` for step-like data where a smooth fill would be wrong.

## Say which interval it is

This is the part that matters and is most often skipped.

**Standard deviation** describes the spread of the **data**. It does not shrink as you collect more.

**Standard error** describes the uncertainty of the **mean**. It is the standard deviation divided by the square root of n, so it does shrink.

**A confidence interval** is roughly 1.96 standard errors for a 95% interval on a mean, under assumptions.

**A prediction interval** is where a new observation should fall, and is wider than a confidence interval for the fitted line.

On a sample of forty with a standard deviation of fifteen, these differ by a factor of six. An error bar without a caption saying which one it is cannot be interpreted, and readers reliably assume whichever supports their prior.

Put it in the axis label or the legend: `"mean (95% CI)"` costs nothing.

## Bars with error bars

`ax.bar(x, heights, yerr=errs, capsize=5)` works directly, and `error_kw` passes styling through to the whiskers.

Two cautions specific to bars.

The **zero baseline** rule still applies, and error bars make it more tempting to break, because a truncated axis makes the intervals look more separated.

And the **overlap heuristic** &mdash; "the error bars overlap, so the difference is not significant" &mdash; is wrong for confidence intervals of two means. Non-overlapping intervals do imply a significant difference; overlapping ones do **not** imply the absence of one, because the relevant quantity is the interval around the *difference*, which is narrower than either individual interval suggests. Two 95% intervals can overlap by a fair margin while the difference is still significant.

## Show the data when you can

With a dozen observations per group, a bar and an error bar throw away almost everything: the shape, the outliers, the sample size.

A strip plot &mdash; the individual points with a small random x offset, or "jitter", to stop them overlapping &mdash; shows all of it in the same space. Adding a horizontal line for the mean keeps the summary.

The fifth editor shows a case where two groups have the same mean and very different spreads, one with a clear outlier. The bar chart reports a taller error bar; the points report what happened.

The rule of thumb: under about fifty points per group, show the points. Above that, a box plot or a violin summarises without hiding as much as a bar does.

## Model intervals

Drawing a fit with a band is the standard way to show a model and its uncertainty, and it requires being explicit about which band.

A **confidence band** for the fitted line is narrow in the middle and bow-shaped, widening at the ends where the fit is less constrained.

A **prediction band** for new observations is much wider and roughly parallel to the line, because it includes the residual scatter as well as the uncertainty in the line.

The sixth editor draws the second, approximately. For anything that will be used to make a decision, statsmodels or SciPy compute these properly, and the arithmetic is worth doing rather than approximating.

## Styling error bars

`errorbar` takes separate styling for the line, the markers and the bars:

```python
ax.errorbar(x, y, yerr=e,
            fmt="o", markersize=5,
            ecolor="0.4", elinewidth=1, capsize=4, capthick=1)
```

`fmt="o"` draws markers with no connecting line, which is right when the x values are discrete categories rather than a sequence. `fmt="none"` draws bars only.

`ecolor` lighter than the marker keeps the point as the subject and the interval as context, which is usually the correct emphasis.

`errorevery=5` draws bars on every fifth point, for a dense series where every bar would be a smear but some indication of uncertainty is wanted.

## Asymmetric intervals from quantiles

Real uncertainty is often asymmetric, and quantiles give it directly:

```python
lo = np.percentile(samples, 5, axis=0)
hi = np.percentile(samples, 95, axis=0)
ax.fill_between(x, lo, hi, alpha=0.2)
```

For `errorbar` the same quantiles must be converted to **offsets** from the central value:

```python
yerr = np.vstack([median - lo, hi - median])
```

Forgetting that conversion &mdash; passing the quantiles themselves &mdash; is the most common error here, and produces intervals that are wrong by the magnitude of the data rather than subtly off.

## Several series with intervals

Two series each with a band overlap into something unreadable if both bands are the same weight.

Three things help: low alpha on the bands (0.15 rather than 0.3), matching each band to its line's colour, and drawing all the bands before all the lines so no line is buried.

```python
for name, (y, lo, hi) in series.items():
    ax.fill_between(x, lo, hi, alpha=0.15)
for name, (y, lo, hi) in series.items():
    ax.plot(x, y, label=name)
```

Beyond three series with bands, the bands stop being separable and small multiples are the answer.

## Error bars on log axes

An interval that is symmetric on a linear scale is asymmetric on a log one, and vice versa.

Passing symmetric `yerr` to a log-scaled axis produces a lower bar that is visually much longer than the upper one, which is correct arithmetic and usually not what was intended &mdash; multiplicative uncertainty is normally what you have on a log scale.

The fix is to compute the interval in the space you are plotting: bounds as multiplicative factors, converted to offsets at each point.

A bar reaching below zero on a log axis simply does not draw, which is the visible symptom.

## What the interval is for

An error bar is a claim about repeatability, and it is worth being clear which claim.

"If I did this again, the mean would land in here" is a confidence interval.

"A new observation would land in here" is a prediction interval, and is much wider.

"The data spread this much" is a standard deviation, and does not shrink with more data.

Charts routinely show one and are read as another. The caption is the only thing that resolves it, which is why every editor here labels the interval rather than leaving it to the reader.

## Uncertainty that is not statistical

Not every band is a confidence interval, and saying which kind it is matters as much as the arithmetic.

**A measurement tolerance** &mdash; the instrument's stated accuracy, fixed and known.

**A range across scenarios** &mdash; best and worst case, which is not a probability statement at all.

**A forecast interval** &mdash; widening with horizon, and conditional on the model.

**Observed min and max** &mdash; the actual extremes, which say nothing about what a new observation would do.

Each is a different claim, and drawn identically. The caption is the only thing distinguishing them, which is why an unlabelled band is the most common way a chart overstates what is known.

## Choosing what to show

The decision is what the reader should conclude.

If the question is **"is this difference real?"**, show a confidence interval on the difference, not two intervals on the means &mdash; the eye cannot combine them correctly.

If the question is **"how variable is this?"**, show the spread: a standard deviation, a percentile band, or the points.

If the question is **"what will happen next?"**, show a prediction interval, which is wider than either.

If the sample is small, showing the observations answers all three better than any interval.

The failure to avoid is showing a standard error because it is narrowest and letting it be read as spread, which understates variability by a factor of the square root of n.

## Intervals in a report

An interval on a chart is a claim, and the surrounding text is part of it.

Three things belong in the caption or the axis label, and are almost always omitted:

**Which interval it is** &mdash; standard deviation, standard error, a confidence interval and at what level, or a prediction interval.

**What it assumes** &mdash; normality, independence, a model.

**The sample size**, because an interval from eight observations and one from eight hundred are different kinds of claim even when they are the same width.

"Mean &plusmn; 95% CI, n = 42" in the y label costs nine words and makes the chart interpretable. Without it the reader either assumes the most favourable reading or discounts the interval entirely, and both are worse than being told.

## In summary

`errorbar` for discrete measurements, `fill_between` for a curve &mdash; hundreds of bars become a smear.

`yerr=[lo, hi]` takes positive offsets, not absolute bounds, and getting that wrong produces intervals wrong by the scale of the data.

Standard deviation, standard error and a confidence interval differ by large factors on the same data, and an unlabelled bar cannot be interpreted.

Overlapping confidence intervals do not imply the absence of a significant difference, though non-overlapping ones do imply its presence.

On a log axis, symmetric offsets are asymmetric on screen, and the interval should be computed in the space being plotted.

And with few observations, showing the points beats any summary of them.

## Bands on a forecast

A forecast chart has a specific convention worth following.

The **historical** series is drawn solid; the **forecast** is drawn dashed or in a different shade, so the boundary between observed and predicted is visible without reading the caption.

A **vertical line** at the forecast origin makes it unmissable.

The **band widens** with horizon, because uncertainty grows &mdash; a constant-width band on a forecast is almost always wrong, and it understates the far end.

**Two bands** at different levels &mdash; 50% and 90%, with the inner one darker &mdash; communicate the shape of the uncertainty better than one, and are standard in published forecasts.

And the caption states the model and the interval, because a forecast band is entirely conditional on a model the chart does not show.

Without the vertical line and the style change, a reader takes the whole line as data, which is the most consequential misreading available on this kind of chart.

## The short version

An interval is a claim, and the caption is part of the claim.

Standard deviation, standard error, confidence and prediction intervals differ by large factors on the same data, and drawing them identically without saying which is the most common way a chart overstates what is known.

## Reading the code back

Drawing an interval is one argument. Deciding which interval, computing it correctly as offsets, and saying in the chart which one it is are three separate pieces of work, and only the first is about matplotlib. A band drawn without the other two is a decoration that readers will interpret as a claim.
''',
    [
        {"q": "How is `yerr=[lo, hi]` interpreted?",
         "options": ["Absolute lower and upper bounds", "Positive offsets below and above each point", "Two separate series", "Percentages"],
         "answer": 1,
         "why": "Passing absolute bounds is a common mistake and produces enormous bars."},
        {"q": "Why use `fill_between` rather than error bars on a curve?",
         "options": ["It is faster", "Hundreds of overlapping bars become an unreadable smear", "Error bars need discrete x", "It is more accurate"],
         "answer": 1,
         "why": "alpha around 0.2-0.3 keeps the central line clearly on top, and the same colour ties the band to the line."},
        {"q": "Two 95% confidence intervals for means overlap slightly. What follows?",
         "options": ["The difference is not significant", "Nothing - overlapping does not imply the absence of a significant difference", "They are equal", "The test is invalid"],
         "answer": 1,
         "why": "Non-overlapping does imply significance, but the relevant interval is the one around the difference, which is narrower than either alone."},
        {"q": "You have 12 observations per group. What shows the most?",
         "options": ["A bar with an error bar", "The individual points with jitter, plus a mean line", "A pie chart", "A single number"],
         "answer": 1,
         "why": "A bar and error bar throw away the shape, the outliers and the sample size. Under about fifty points per group, show the points."},
    ],
)


# ---------------------------------------------------------------------------
# 14. Images and heatmaps
# ---------------------------------------------------------------------------
topic(
    "images_and_heatmaps",
    "Images and Heatmaps",
    "Working with Data",
    "imshow and pcolormesh - showing a 2-D array, and the origin that catches "
    "everyone.",
    _svg(_grid(38, 24, 5, 4, 14, S, B) +
         '<rect x="52" y="38" width="14" height="14" fill="%s"/>'
         '<rect x="80" y="24" width="14" height="14" fill="%s"/>' % (A, A)),
    [
        ("imshow draws an array as a grid",
         "Row 0 is at the TOP, because it is drawing an image.",
         '''import matplotlib.pyplot as plt
import numpy as np

z = np.arange(12).reshape(3, 4)

fig, (a, b) = plt.subplots(1, 2, figsize=(8, 3))

im = a.imshow(z, cmap="viridis")
a.set_title('origin="upper" (default)')
fig.colorbar(im, ax=a)

im2 = b.imshow(z, cmap="viridis", origin="lower")
b.set_title('origin="lower"')
fig.colorbar(im2, ax=b)

print("the array:"); print(z)
print()
print("By default z[0, 0] is drawn TOP-LEFT, matching how an image is")
print("stored. For data where the y axis is a quantity, that puts the")
print("smallest y at the top, which is upside down.")
print()
print("origin='lower' is what you want for a matrix of values.")'''),

        ("Aspect and interpolation",
         "Two defaults that suit photographs and not data.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
z = rng.random((6, 30))

fig, (a, b) = plt.subplots(2, 1, figsize=(7, 4))

a.imshow(z, cmap="magma")
a.set_title('default: aspect="equal" - cells are square, plot is thin')

b.imshow(z, cmap="magma", aspect="auto", interpolation="nearest")
b.set_title('aspect="auto" fills the axes')

print("aspect='equal' makes each cell square, so a 6x30 array is drawn")
print("five times wider than tall regardless of the figure.")
print("aspect='auto' stretches it to fill the axes.")
print()
print("interpolation blurs between cells. For a photograph that is")
print("desirable; for a matrix of values it invents intermediate")
print("values that do not exist. Use 'nearest' for data.")'''),

        ("Labelling the cells",
         "A heatmap of a small matrix is a table, and should read like one.",
         '''import matplotlib.pyplot as plt
import numpy as np

rows = ["mon", "tue", "wed"]
cols = ["north", "south", "east", "west"]
z = np.array([[12, 7, 3, 9], [5, 14, 8, 2], [9, 4, 11, 6]])

fig, ax = plt.subplots(figsize=(6, 3))
im = ax.imshow(z, cmap="Blues")

ax.set_xticks(range(len(cols)))
ax.set_xticklabels(cols)
ax.set_yticks(range(len(rows)))
ax.set_yticklabels(rows)

for i in range(z.shape[0]):
    for j in range(z.shape[1]):
        ax.text(j, i, z[i, j], ha="center", va="center",
                color="white" if z[i, j] > z.max() / 2 else "black")
fig.colorbar(im, ax=ax)

print("Note the text index order: ax.text(j, i, ...) - x is the COLUMN.")
print()
print("Choosing the text colour by threshold keeps it readable on both")
print("the light and dark ends of the colormap.")'''),

        ("pcolormesh for uneven grids",
         "When the cells are not all the same size.",
         '''import matplotlib.pyplot as plt
import numpy as np

x_edges = np.array([0, 1, 2, 4, 8, 16], dtype=float)
y_edges = np.array([0, 1, 3, 6], dtype=float)
z = np.arange(15).reshape(3, 5).astype(float)

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.imshow(z, cmap="viridis", origin="lower", aspect="auto")
a.set_title("imshow: cells forced equal")

m = b.pcolormesh(x_edges, y_edges, z, cmap="viridis")
b.set_title("pcolormesh: real coordinates")
fig.colorbar(m, ax=b)

print("imshow assumes a regular grid and ignores the coordinates.")
print("pcolormesh takes the EDGES, so cells can have different widths.")
print()
print("edges outnumber cells by one in each direction:")
print("   x edges:", len(x_edges), "-> columns:", z.shape[1])
print("   y edges:", len(y_edges), "-> rows:", z.shape[0])'''),

        ("Setting the colour range",
         "<code>vmin</code> and <code>vmax</code>, and why two heatmaps otherwise "
         "lie.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
a_data = rng.normal(0, 1, (8, 8))
b_data = rng.normal(0, 1, (8, 8)) * 3

fig, axes = plt.subplots(2, 2, figsize=(8, 5))

for ax, d, t in zip(axes[0], [a_data, b_data], ["sd 1", "sd 3"]):
    im = ax.imshow(d, cmap="coolwarm")
    ax.set_title("%s, own scale" % t, fontsize=9)
    fig.colorbar(im, ax=ax)

for ax, d, t in zip(axes[1], [a_data, b_data], ["sd 1", "sd 3"]):
    im = ax.imshow(d, cmap="coolwarm", vmin=-9, vmax=9)
    ax.set_title("%s, shared scale" % t, fontsize=9)
    fig.colorbar(im, ax=ax)
fig.tight_layout()

print("The top pair look equally variable. They are not - the right")
print("one has three times the spread, and its colorbar says so in")
print("numbers nobody reads.")
print()
print("vmin/vmax force a common scale, which is what makes two")
print("heatmaps comparable. Same rule as sharey for subplots.")'''),

        ("Diverging data needs a centred scale",
         "Or zero ends up somewhere arbitrary in the colormap.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(2)
z = rng.normal(2, 3, (8, 8))          # mostly positive, some negative

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3.2))

im1 = a.imshow(z, cmap="coolwarm")
a.set_title("uncentred: white is not zero")
fig.colorbar(im1, ax=a)

lim = np.abs(z).max()
im2 = b.imshow(z, cmap="coolwarm", vmin=-lim, vmax=lim)
b.set_title("centred: white IS zero")
fig.colorbar(im2, ax=b)

print("data range: %.2f to %.2f" % (z.min(), z.max()))
print()
print("With automatic limits the midpoint of the colormap falls at the")
print("midpoint of the DATA, so white sits at %.2f, not 0." % ((z.min()+z.max())/2))
print("A diverging colormap only means anything when its centre is the")
print("value that matters.")'''),
    ],
    [
        "<code>imshow</code> puts row 0 at the <strong>top</strong>; <code>origin=\"lower\"</code> is what you want for a matrix of values.",
        "<code>aspect=\"equal\"</code> forces square cells &mdash; use <code>aspect=\"auto\"</code> to fill the axes, and <code>interpolation=\"nearest\"</code> so it does not invent intermediate values.",
        "For a small matrix, write the numbers in the cells and pick the text colour by threshold so it reads on both ends of the colormap.",
        "<code>pcolormesh</code> takes cell <strong>edges</strong>, so it handles uneven grids; edges outnumber cells by one per axis.",
        "<code>vmin</code>/<code>vmax</code> force a shared colour scale &mdash; without it two heatmaps are not comparable, the same problem as unshared axes.",
        "A <strong>diverging</strong> colormap needs symmetric limits, or its neutral midpoint lands somewhere arbitrary instead of at zero.",
    ],
    '''
title: Images and Heatmaps
intro: imshow and pcolormesh, and the origin that catches everyone.

## imshow

`ax.imshow(z)` draws a 2-D array as a grid of coloured cells.

Its defaults are chosen for **images**, and three of them are wrong for data.

**Origin.** `z[0, 0]` is drawn at the top-left, because that is where the first pixel of an image goes. For a matrix whose rows are a quantity &mdash; a y axis &mdash; that puts the smallest value at the top, upside down. `origin="lower"` fixes it.

**Aspect.** The default `"equal"` makes every cell square, so a 6&times;30 array is drawn five times wider than tall no matter what figure size you asked for. `aspect="auto"` stretches it to fill the axes.

**Interpolation.** The default smooths between cells. On a photograph that is desirable; on a matrix of values it draws colours that correspond to no data point, which is a small lie. `interpolation="nearest"` gives hard cell edges.

For data, `imshow(z, origin="lower", aspect="auto", interpolation="nearest")` is the honest starting point.

## Labelling cells

A heatmap of a small matrix is a table that has been coloured. It should read like one.

Set the ticks to the row and column names, and write the values into the cells:

```python
for i in range(rows):
    for j in range(cols):
        ax.text(j, i, z[i, j], ha="center", va="center")
```

Note the index order: `ax.text(j, i, ...)`. The first argument is x, which is the **column**. Getting this backwards is the usual bug, and on a square matrix it produces a transposed result that looks plausible.

Choosing the text colour by threshold &mdash; white on dark cells, black on light &mdash; keeps every label readable. Without it, half the numbers vanish into the background at one end of the colormap.

## pcolormesh

`imshow` assumes a regular grid and ignores any coordinates you have.

`pcolormesh(x_edges, y_edges, z)` takes the **edges** of the cells, so they can be unevenly spaced &mdash; logarithmic bins, irregular time intervals, a non-uniform mesh.

The edges outnumber the cells by one in each direction, the same convention as histogram bins. Passing centres instead of edges is the common mistake; matplotlib will accept same-sized arrays and shift everything by half a cell.

`pcolormesh` is slower than `imshow` and much more flexible. For a regular grid, `imshow` is the right tool.

`contourf` is the third option, drawing filled contour bands rather than cells &mdash; appropriate when the underlying field is genuinely continuous and misleading when it is not.

## Shared colour scales

`vmin` and `vmax` set the values at the ends of the colormap.

Without them, each heatmap scales to its own data, exactly like unshared subplot axes. Two heatmaps drawn side by side then use the same colours for different values, and the comparison the layout invites is invalid.

The colorbar does say so, in numbers, and readers do not read them &mdash; they read the colours.

So: whenever two colour-mapped plots will be compared, fix `vmin` and `vmax` across both, or use one shared colorbar.

`norm=` gives finer control &mdash; `LogNorm` for data spanning orders of magnitude, `BoundaryNorm` for discrete bands.

## Centring a diverging map

A diverging colormap has a neutral colour in the middle and two directions away from it. It only means anything if that neutral point sits at the value that matters, usually zero.

With automatic limits, the midpoint of the colormap lands at the midpoint of the **data**. On data ranging from &minus;4 to +10, white sits at +3, and every cell below +3 is coloured as though it were negative.

The fix is symmetric limits:

```python
lim = np.abs(z).max()
ax.imshow(z, cmap="coolwarm", vmin=-lim, vmax=lim)
```

or `TwoSlopeNorm(vcenter=0)` when the two sides genuinely need different ranges.

This is one of the most common quiet errors in heatmaps, because the result looks like a normal chart and asserts something false about the sign of half the data.

## extent for real coordinates

`imshow` numbers the cells from zero by default. `extent=(x0, x1, y0, y1)` maps the array onto real coordinates:

```python
ax.imshow(z, extent=(0, 100, 0, 50), origin="lower", aspect="auto")
```

The four values are the outer edges of the image, not cell centres, which is the usual off-by-half confusion. With `origin="lower"`, `y0` is the bottom.

This is what lets a heatmap be overlaid with a line or a scatter in the same units, and without it any overlay is a half-cell out.

## Masked and missing values

`np.nan` in the array is drawn as the colormap's "bad" colour, which defaults to fully transparent &mdash; so missing cells show whatever is behind them, usually the axes background.

`cmap.set_bad("0.9")` makes them an explicit grey, which is better than transparent because a missing cell then reads as missing rather than as background.

A masked array behaves the same way, and is the more explicit form when the mask is computed separately from the data.

## Aspect and reading order

For a correlation matrix or any square array, `aspect="equal"` is right and is the default.

For a wide array &mdash; time along one axis, a handful of categories along the other &mdash; `aspect="auto"` is necessary, or the figure is drawn at the array's proportions and ignores the size you asked for.

Row order deserves thought. An unordered heatmap makes the reader scan for structure; sorting rows by their mean, or by a clustering, often reveals the pattern the chart is meant to show. That is a data decision made in the plotting code, and it should be stated in the caption if the order is not alphabetical.

## Contours

`ax.contour(z)` draws lines of constant value; `ax.contourf(z)` fills between them.

They suit genuinely continuous fields &mdash; elevation, temperature, a fitted surface &mdash; and imply smoothness, so they are wrong for a matrix of independent measurements where `pcolormesh` is honest.

`levels=` sets the number or the exact values, and `ax.clabel(cs, inline=True)` writes the values on the lines, which often removes the need for a colorbar.

Combining a filled contour with thin contour lines on top is a standard treatment for a field where both the bands and the exact levels matter.

## Annotating a heatmap

For a small matrix, writing values into the cells makes it a table with colour as a visual aid rather than the only encoding.

The threshold trick for text colour is worth restating because it is the difference between a readable and an unreadable heatmap:

```python
color = "white" if z[i, j] > z.max() / 2 else "black"
```

For a diverging map centred on zero, the threshold should be based on distance from the centre rather than from the maximum, or the labels invert on the wrong half.

## Reading a heatmap

Heatmaps are read less accurately than people assume, because colour intensity is a weak encoding.

They are good at showing **patterns**: blocks, gradients, an outlier cell, structure along a diagonal.

They are poor at **values**: nobody reads 0.62 off a colour.

So the rule is that a heatmap should either be about the pattern, or it should have the numbers written in the cells &mdash; at which point it is a table with colour as a guide, which is a genuinely good display for a small matrix.

For a large matrix, the pattern is the only thing available, and ordering the rows and columns &mdash; by cluster, by total, by a meaningful sequence &mdash; is what makes a pattern visible at all.

## Common heatmap mistakes

**Wrong origin** &mdash; row 0 at the top for data whose y axis is a quantity.

**Interpolation on** &mdash; smoothing between cells that are independent measurements.

**Unshared scales** across panels that will be compared.

**An uncentred diverging map**, putting the neutral colour at an arbitrary value.

**No colorbar**, leaving the colours meaningless.

**Text the same colour everywhere**, so half the labels disappear into the background.

**Unordered rows**, hiding whatever structure exists.

All seven are defaults or omissions rather than errors of arithmetic, which is why a heatmap can look professional and communicate nothing.

## Correlation matrices

The most common heatmap in practice, and it has its own conventions.

**Centre the colormap on zero** with symmetric limits, because a correlation of &minus;0.4 and +0.4 should be equally strong in opposite directions. Without it, a matrix of mostly positive correlations puts the neutral colour somewhere arbitrary and the few negatives look far more extreme than they are.

**Use a diverging map** for the same reason.

**Set `vmin=-1, vmax=1`**, so two matrices are comparable and so the colour scale means the same thing in every such chart.

**Mask the upper triangle**, since the matrix is symmetric and half of it is repetition. `np.triu` with `np.nan` and a `set_bad` colour does it.

**Write the numbers in**, if the matrix is small enough, because the exact values are usually what the reader wants.

Those five turn the default output into something readable, and the first three are the ones that affect whether it is accurate.

## In summary

`imshow` has image defaults: row 0 at the top, square cells, and interpolation between them. For data, `origin="lower"`, `aspect="auto"` and `interpolation="nearest"` are the honest settings.

`pcolormesh` takes cell edges and handles uneven grids; edges outnumber cells by one per axis.

`vmin`/`vmax` are what make two heatmaps comparable, and their absence is the same error as unshared subplot axes.

A diverging colormap needs symmetric limits or its neutral point lands at the midpoint of the data rather than at zero.

A colorbar is not optional, and a small matrix is better as a table with the numbers written in.

And row order is a choice: sorting by a meaningful quantity is frequently what makes a pattern visible at all.

## Overlaying on an image

A heatmap or image often needs something drawn on top &mdash; contours, a scatter, a boundary.

The key is that `imshow` sets up a coordinate system, and everything overlaid must use the same one.

With default settings the cells are numbered from zero and a scatter must be in those units. With `extent=`, both use real coordinates and the overlay is straightforward.

Two details catch people. `extent` gives the outer **edges**, so a cell centre is half a cell in from the boundary &mdash; a scatter of cell centres plotted against edge coordinates is offset by half a cell, which looks like a small registration error.

And `origin="lower"` must be consistent between the image and any y coordinates computed for the overlay, or the overlay is flipped relative to the image while both look individually correct.

Drawing a few known points on top is the quickest way to confirm the coordinate system is what you think.

## One more thing

`ax.matshow` is `imshow` with the defaults already set for a matrix: origin at the top with the tick labels along the top edge, which is the convention for displaying a matrix in mathematical notation.

It is convenient for a correlation matrix and confusing for anything with a quantitative y axis, where `imshow(origin="lower")` remains the right call.

## The short version

A heatmap is read for its pattern, not its values, which is why ordering the rows and columns matters as much as the colormap.

The defaults are built for photographs, and three of them &mdash; origin, aspect and interpolation &mdash; are wrong for data. Setting all three explicitly is the honest starting point.

## Reading the code back

A heatmap is one call and four corrections to its defaults: origin, aspect, interpolation and the colour limits. Add a colorbar with a label and, for a small matrix, the values in the cells. That is six lines, and it is the difference between a picture of colours and a readable display of a matrix.
''',
    [
        {"q": "Why does `imshow` put row 0 at the top?",
         "options": ["A bug", "Its defaults are for images, where the first pixel is top-left", "Matrices are stored that way", "It does not"],
         "answer": 1,
         "why": "For a matrix whose rows are a quantity, that is upside down. origin='lower' fixes it."},
        {"q": "Why use `interpolation='nearest'` for data?",
         "options": ["It is faster", "The default smooths between cells, drawing colours that correspond to no data point", "It is sharper", "It handles NaN"],
         "answer": 1,
         "why": "Desirable on a photograph, a small lie on a matrix of values."},
        {"q": "What does `pcolormesh` take that `imshow` does not?",
         "options": ["A colormap", "Cell edges, so the grid can be uneven", "A colorbar", "Labels"],
         "answer": 1,
         "why": "Edges outnumber cells by one per axis. Passing centres instead shifts everything by half a cell."},
        {"q": "Data ranges from -4 to +10 with a diverging colormap and automatic limits. Where is the neutral colour?",
         "options": ["At 0", "At +3, the midpoint of the data", "At -4", "At +10"],
         "answer": 1,
         "why": "Every cell below +3 is then coloured as though negative. Use symmetric vmin/vmax, or TwoSlopeNorm(vcenter=0)."},
    ],
)


# ---------------------------------------------------------------------------
# 15. Styles and rcParams
# ---------------------------------------------------------------------------
topic(
    "styles_and_rcparams",
    "Styles and rcParams",
    "Output",
    "Changing every chart at once, instead of styling each one by hand.",
    _svg(_box(18, 22, 50, 44, S, M) + _txt(43, 48, "default", M, 8) +
         _arrow(72, 44, 88, 44) +
         _box(94, 22, 50, 44, S, A) + _txt(119, 48, "styled", A, 8)),
    [
        ("rcParams is the settings dictionary",
         "Every default lives in it, and changing one changes every later figure.",
         '''import matplotlib.pyplot as plt
import numpy as np

print("some current defaults:")
for k in ["figure.figsize", "lines.linewidth", "axes.grid",
          "font.size", "axes.spines.top"]:
    print("   %-20s %s" % (k, plt.rcParams[k]))
print()
print("total settings:", len(plt.rcParams))

plt.rcParams["lines.linewidth"] = 3
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

fig, ax = plt.subplots(figsize=(6, 2.5))
ax.plot(np.linspace(0, 10, 50), np.sin(np.linspace(0, 10, 50)))
ax.set_title("thick line, no top/right spines - set globally")

plt.rcdefaults()
print()
print("plt.rcdefaults() puts everything back.")'''),

        ("Style sheets are named bundles of settings",
         "One line instead of twenty.",
         '''import matplotlib.pyplot as plt
import numpy as np

print("a few available styles:")
for s in sorted(plt.style.available)[:12]:
    print("   ", s)
print("   ... %d in total" % len(plt.style.available))

x = np.linspace(0, 10, 60)

for name in ["default", "ggplot", "seaborn-v0_8-darkgrid"]:
    if name not in plt.style.available and name != "default":
        continue
    with plt.style.context(name):
        fig, ax = plt.subplots(figsize=(4.5, 2))
        for k in range(3):
            ax.plot(x, np.sin(x + k))
        ax.set_title(name, fontsize=10)

print()
print("plt.style.use(name) applies it from then on.")
print("plt.style.context(name) is a context manager, so it applies to")
print("one block and leaves everything else alone - which is what you")
print("want in a script that also draws other charts.")'''),

        ("Combining styles",
         "A list applies them in order, so later ones override.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 60)

with plt.style.context(["ggplot", {"lines.linewidth": 3,
                                   "axes.facecolor": "white",
                                   "figure.figsize": (6, 2.5)}]):
    fig, ax = plt.subplots()
    for k in range(3):
        ax.plot(x, np.sin(x + k))
    ax.set_title("ggplot, with three settings overridden")

print("A list is applied left to right.")
print("A dict in the list is treated as a set of rcParams, so you can")
print("take a style and change a few things without copying the file.")
print()
print("This is the practical form: a published style for the look, a")
print("dict for the two things it gets wrong for your use.")'''),

        ("A house style, in one place",
         "Define it once and every chart in the project matches.",
         '''import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler

HOUSE = {
    "figure.figsize": (6.5, 3.5),
    "figure.dpi": 110,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.axisbelow": True,
    "lines.linewidth": 2,
    "legend.frameon": False,
    "axes.prop_cycle": cycler(color=["#264653", "#e76f51", "#2a9d8f",
                                     "#e9c46a", "#8ab17d"]),
}

with plt.rc_context(HOUSE):
    x = np.linspace(0, 10, 80)
    fig, ax = plt.subplots()
    for k, name in enumerate(["north", "south", "east"]):
        ax.plot(x, np.sin(x + k) + k * 0.3, label=name)
    ax.set_title("Every chart in the project looks like this")
    ax.set_xlabel("x")
    ax.set_ylabel("value")
    ax.legend()

print("rc_context takes a dict directly, and restores the old settings")
print("on exit. A module-level HOUSE dict plus rc_context is the whole")
print("mechanism for a consistent set of charts.")'''),

        ("What a style cannot fix",
         "Settings control defaults, not the decisions.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
x = rng.normal(size=3000)
y = x * 0.6 + rng.normal(size=3000)

with plt.style.context("ggplot"):
    fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))
    a.scatter(x, y)
    a.set_title("styled, and still unreadable")

    b.scatter(x, y, s=6, alpha=0.15)
    b.set_title("alpha and marker size fixed by hand")

print("Both panels use the same style sheet.")
print("The left one is 3000 opaque markers; no style setting rescues it.")
print()
print("Styles handle fonts, colours, spines and grids. They cannot")
print("choose a chart type, set an alpha appropriate to your n, or")
print("decide what the title should say.")'''),

        ("Fonts",
         "Setting a family, and what happens when it is missing.",
         '''import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

available = sorted({f.name for f in fm.fontManager.ttflist})
print("fonts matplotlib can see here:", len(available))
for name in available[:8]:
    print("   ", name)

print()
print("current family:", plt.rcParams["font.family"],
      "->", plt.rcParams["font.sans-serif"][:3])
print()
print("font.family takes a generic name; font.sans-serif is the list")
print("tried in order. A missing font produces a warning and a")
print("fallback, not an error - so a figure can silently render in a")
print("different typeface on another machine.")

fig, ax = plt.subplots(figsize=(6, 2))
ax.text(0.5, 0.5, "whatever font is available here",
        ha="center", va="center", fontsize=14)
ax.set_xticks([]); ax.set_yticks([])'''),
    ],
    [
        "<code>plt.rcParams</code> holds every default; changing one affects every later figure, and <code>plt.rcdefaults()</code> restores them.",
        "<strong>Style sheets</strong> are named bundles &mdash; <code>plt.style.use</code> applies one globally, <code>plt.style.context</code> for a block only.",
        "A <strong>list</strong> of styles applies left to right, and a dict in the list overrides individual settings.",
        "<code>plt.rc_context(HOUSE)</code> with a module-level dict is the whole mechanism for a consistent project style.",
        "Styles control fonts, colours, spines and grids &mdash; they cannot choose a chart type or pick an alpha appropriate to your data.",
        "A missing font <strong>warns and falls back</strong> rather than failing, so a figure can render in a different typeface elsewhere.",
    ],
    '''
title: Styles and rcParams
intro: Changing every chart at once, instead of styling each one by hand.

## rcParams

`plt.rcParams` is a dictionary of every default matplotlib uses &mdash; several hundred settings covering figure size, fonts, colours, line widths, spines, grids, ticks and saving.

Changing one changes every figure created afterwards:

```python
plt.rcParams["axes.spines.top"] = False
```

The keys are dotted paths mirroring the object structure: `lines.linewidth`, `axes.titlesize`, `xtick.direction`, `savefig.dpi`.

`plt.rcdefaults()` restores everything, which is worth knowing in a notebook where settings accumulate across cells.

The important property is that these are **defaults**, applied when an artist is created. Changing a setting does not affect figures already drawn.

## Style sheets

A style sheet is a named bundle of rcParams.

`plt.style.available` lists them &mdash; `ggplot`, `bmh`, `fivethirtyeight`, `grayscale`, the `seaborn-v0_8-*` family, and several others.

`plt.style.use("ggplot")` applies one from that point on. `with plt.style.context("ggplot"):` applies it to a block and restores the previous settings afterwards, which is what you want in a script that also produces charts in a different style.

Writing your own is a plain text file of `key: value` lines with a `.mplstyle` extension, placed where matplotlib looks for it. For a project, a dict in a module is usually simpler.

## Combining

`plt.style.use(["ggplot", {"lines.linewidth": 3}])` applies items left to right, so later ones win.

A dict in the list is treated as rcParams. That is the practical form for real work: take a published style for its typography and colours, then override the two or three things it gets wrong for your case, without copying and maintaining a whole style file.

## A house style

The pattern that scales to a project:

```python
HOUSE = {
    "figure.figsize": (6.5, 3.5),
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.titlelocation": "left",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "legend.frameon": False,
    "axes.prop_cycle": cycler(color=PALETTE),
}

with plt.rc_context(HOUSE):
    ...
```

`rc_context` takes a dict directly and restores the previous settings on exit.

The settings worth putting in almost any house style are the ones that fix matplotlib's weakest defaults: the top and right spines, a left-aligned bold title, a faint grid drawn below the data, a legend without a frame, and a colour cycle you chose.

That is six lines, and it is the difference between charts that look like matplotlib defaults and charts that look designed.

## What styles cannot do

A style sets defaults. It cannot make decisions.

It will not choose between a bar chart and a line chart. It will not set an `alpha` appropriate to your number of points &mdash; the right value for 100 points is wrong for 100,000. It will not decide the axis should start at zero, or that the title should state a finding, or that three of the seven series should be greyed out.

The fifth editor shows a styled scatter that is still unreadable, because the problem was overplotting and no setting addresses that.

Styling is the last 20% of a chart. The decisions are the rest, and they are the subject of most of this track.

## Fonts

`font.family` takes a generic name &mdash; `sans-serif`, `serif`, `monospace` &mdash; and `font.sans-serif` is the ordered list of actual fonts tried for it.

A font that is not installed produces a **warning and a fallback**, not an error. The figure renders in whatever was available next, which means the same script can produce different-looking output on a different machine, and the only sign is a warning that is easy to miss in a log.

For output that must look identical everywhere, either restrict yourself to fonts you know are present, or embed the font by saving as PDF or SVG with `pdf.fonttype = 42`, which stores the glyphs in the file.

`mathtext` handles LaTeX-style maths in labels without needing LaTeX installed: `r"$\\sigma^2$"` in any text argument.

## Where settings come from

matplotlib reads its defaults in a fixed order, each overriding the last:

The built-in defaults.

A `matplotlibrc` file, found in the current directory, the user's config directory, or the installation.

`plt.style.use(...)`.

Direct assignment to `plt.rcParams`.

Arguments passed to the plotting call itself.

That ordering explains a common confusion: a setting applied in a style sheet is overridden by anything passed explicitly, and a `matplotlibrc` in the working directory silently changes every chart in that project. When a figure looks different on another machine, a `matplotlibrc` is a candidate.

## Settings worth knowing

Beyond the obvious ones, a handful appear in most house styles:

`figure.autolayout: True` &mdash; applies `tight_layout` to every figure automatically.

`axes.titlelocation: left` &mdash; headline-style titles.

`axes.axisbelow: True` &mdash; grid behind the data.

`legend.frameon: False`.

`savefig.bbox: tight` &mdash; makes every save behave as if `bbox_inches="tight"` had been passed, which removes a whole class of cropping bug.

`figure.constrained_layout.use: True` &mdash; the newer alternative to `autolayout`.

`errorbar.capsize: 3` &mdash; caps by default, since the bare-line default is rarely what anyone wants.

## Writing a style file

A `.mplstyle` file is plain text, one `key: value` per line, with `#` comments and no quotes:

```
figure.figsize: 6.5, 3.5
axes.spines.top: False
axes.prop_cycle: cycler('color', ['264653', 'e76f51', '2a9d8f'])
```

Note the colours have no `#` prefix, because `#` starts a comment in this format &mdash; a small trap that produces a confusing parse error.

Placed in `~/.config/matplotlib/stylelib/`, it can be used by name from anywhere.

## Per-project versus per-figure

A project-wide style is right for consistency and wrong when one figure needs to differ.

`plt.rc_context(...)` as a context manager is the middle ground: a project default applied broadly, and a block that overrides it for one figure without leaking.

The failure mode of global settings in a notebook is that they accumulate invisibly across cells, so a figure depends on which cells have been run. `plt.rcdefaults()` at the top of a notebook, followed by the project style, makes it deterministic.

## Style is not design

A style sheet gets the typography, spacing and palette consistent, which is genuinely valuable and is roughly the last fifth of making a chart good.

The other four fifths &mdash; which chart, what to compare, what to leave out, what the title claims, whether the axis starts at zero &mdash; are decisions no setting can make.

That is worth saying explicitly because a good style sheet makes a bad chart look professional, which is not an improvement.

## A minimal house style

The settings that fix matplotlib's weakest defaults, in about ten lines:

```python
HOUSE = {
    "figure.figsize": (7, 4),
    "figure.dpi": 110,
    "savefig.bbox": "tight",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.alpha": 0.3,
    "legend.frameon": False,
    "lines.linewidth": 2,
}
```

Nothing exotic, and every chart in a project drawn under it looks intentional. `savefig.bbox` alone removes the most common cropping complaint.

## Styles and reproducibility

A figure's appearance depends on settings that are not in the plotting code, which is a reproducibility problem.

Three sources of drift: a `matplotlibrc` in the working directory, accumulated `rcParams` changes in a long notebook session, and a style sheet that differs between machines.

Two habits address it.

**Reset explicitly** at the start: `plt.rcdefaults()` followed by the project style. The figure then does not depend on what ran before.

**Apply the style in a context manager** rather than globally, so a figure carries its own appearance rather than inheriting whatever is current.

For a figure that will be regenerated months later, the style belongs in the repository alongside the code, not in a user config directory.

## Style as a decision record

A style sheet is a place to write down decisions once, and that is worth more than the consistency it produces.

Every setting in it encodes a judgement: that titles are left-aligned headlines, that grids are faint and behind the data, that legends have no frame, that this is the palette. Written in a style file, those decisions are visible, reviewable and changeable in one place.

Written into each chart, they are re-decided every time, inconsistently, by whoever is writing that chart.

The practical benefit shows up when something has to change &mdash; a new brand colour, a journal's font requirement, a switch to dark backgrounds for a presentation. With a style, that is one edit. Without it, it is a search through every plotting call in the project.

That is the same argument as any other configuration, and it applies here more than people expect, because chart styling is exactly the kind of thing that gets copy-pasted.

## In summary

`rcParams` holds every default, and changes affect figures created afterwards.

Style sheets bundle them; `plt.style.context` applies one to a block without leaking.

A list applies styles in order, and a dict in the list overrides individual settings &mdash; the practical way to take a published style and fix the two things it gets wrong.

`rc_context` with a module-level dict is the whole mechanism for a project style.

A missing font warns and falls back silently, so figures can look different elsewhere.

And a style is the last fifth of a good chart. It cannot choose the chart type, set an alpha suited to your sample size, or decide what the title should claim &mdash; and it will make a bad chart look professional, which is not the same as making it better.

## Dark backgrounds

A dark theme is not a colour inversion, and doing it by hand usually misses something.

The elements that need changing: the figure background, the axes background, the text colour, the tick colours, the tick label colours, the spine colours, the grid colour, and the property cycle &mdash; because a palette tuned for white is usually too dark on black.

`plt.style.use("dark_background")` does all of it, which is the argument for using a style rather than setting six things.

Two further points. Saturated colours that look right on white are often too intense on black, and desaturating them slightly helps. And `savefig` still writes a white background unless told otherwise, so a dark figure saved with default settings comes out with a white border around a dark plot &mdash; `facecolor=fig.get_facecolor()` fixes it, or setting `savefig.facecolor` in the style.

## Where to keep a style

A project style needs to live somewhere both the code and the people can find.

**A module in the repository** &mdash; `style.py` exporting a dict &mdash; is version-controlled, reviewable, and importable. It is the option that behaves like the rest of the code.

**A `.mplstyle` file in the repository**, applied with a relative path, is equivalent and uses matplotlib's own format.

**A file in the user's config directory** is convenient and invisible to everyone else, which makes figures irreproducible on another machine. It is the wrong place for anything shared.

The repository options also mean the style is part of the diff when it changes, so a figure that suddenly looks different has a commit explaining why.

For a single analysis, a dict at the top of the notebook applied with `rc_context` is enough, and still better than settings scattered through the plotting calls.

## One more thing

`plt.style.use` accepts a URL or a file path as well as a name, so a style can be shared without installing it.

For a team, a style file in a shared repository referenced by relative path gives everyone the same figures without anyone configuring their environment &mdash; and it appears in code review when it changes.

## The short version

A style is a set of decisions written down once, which is worth more than the consistency it produces.

It handles typography, spacing and palette &mdash; roughly the last fifth of a good chart. The other four fifths are choices no setting can make, and a good style applied to a bad chart produces a professional-looking bad chart.

## Reading the code back

A style is a dict applied in a context manager, and its contents are decisions rather than settings. The ones that matter most are the ones fixing matplotlib's weakest defaults: spines, title alignment, grid weight, legend frame and the colour cycle. Six entries covers it, and every chart in the project then starts from a better place.
''',
    [
        {"q": "What does changing `plt.rcParams` affect?",
         "options": ["Every figure, including ones already drawn", "Figures created after the change", "Only the current figure", "Nothing until you call apply()"],
         "answer": 1,
         "why": "They are defaults, applied when an artist is created. plt.rcdefaults() restores them."},
        {"q": "What is the difference between `plt.style.use` and `plt.style.context`?",
         "options": ["None", "context is a context manager that restores the previous settings afterwards", "use is deprecated", "context is faster"],
         "answer": 1,
         "why": "Which is what you want in a script that also produces charts in another style."},
        {"q": "How do you take a style but change two of its settings?",
         "options": ["Copy the style file", "Pass a list: [name, {\"key\": value}] - applied left to right", "You cannot", "Edit rcParams afterwards only"],
         "answer": 1,
         "why": "A dict in the list is treated as rcParams, so you avoid maintaining a whole style file for two overrides."},
        {"q": "What happens when a font named in rcParams is not installed?",
         "options": ["An error", "A warning and a silent fallback to another font", "matplotlib downloads it", "The text is blank"],
         "answer": 1,
         "why": "The same script can produce different-looking output on a different machine, with only an easily-missed warning."},
    ],
)


# ---------------------------------------------------------------------------
# 16. Twin and secondary axes
# ---------------------------------------------------------------------------
topic(
    "twin_axes",
    "Twin and Secondary Axes",
    "Layout",
    "Two scales on one plot - how, and the reasons to think twice.",
    _svg(_box(24, 20, 108, 48, "none", B) +
         _txt(14, 44, "A", A, 9) + _txt(142, 44, "B", "#e76f51", 9) +
         '<polyline points="32,58 60,40 88,48 124,28" fill="none" stroke="%s" stroke-width="2"/>' % A +
         '<polyline points="32,32 60,44 88,36 124,56" fill="none" stroke="#e76f51" stroke-width="2" stroke-dasharray="4 3"/>'),
    [
        ("twinx shares the x axis",
         "A second axes on top of the first, with its own y scale.",
         '''import matplotlib.pyplot as plt
import numpy as np

months = np.arange(1, 13)
revenue = np.array([120, 135, 128, 150, 175, 190, 185, 200, 178, 160, 145, 165])
rate = np.array([2.1, 2.3, 2.0, 2.6, 3.1, 3.4, 3.2, 3.6, 3.0, 2.7, 2.4, 2.9])

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(months, revenue, color="#264653", marker="o", label="revenue")
ax.set_ylabel("revenue (thousands)", color="#264653")
ax.tick_params(axis="y", labelcolor="#264653")

ax2 = ax.twinx()
ax2.plot(months, rate, color="#e76f51", marker="s", linestyle="--", label="rate %")
ax2.set_ylabel("conversion rate (%)", color="#e76f51")
ax2.tick_params(axis="y", labelcolor="#e76f51")

print("twinx() returns a NEW axes sharing the x axis.")
print("Colouring each y label and its ticks to match its line is what")
print("makes the chart readable - without it, nobody knows which")
print("scale belongs to which series.")'''),

        ("The legend problem",
         "Each axes has its own artists, so a single legend needs assembling.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(12)
a_vals = np.linspace(100, 200, 12)
b_vals = np.linspace(3, 1, 12)

fig, (p, q) = plt.subplots(1, 2, figsize=(10, 3.2))

p2 = p.twinx()
p.plot(x, a_vals, color="#264653", label="A")
p2.plot(x, b_vals, color="#e76f51", label="B")
p.legend(loc="upper left")
p2.legend(loc="upper right")
p.set_title("two legends - clumsy")

q2 = q.twinx()
l1, = q.plot(x, a_vals, color="#264653", label="A")
l2, = q2.plot(x, b_vals, color="#e76f51", label="B")
q.legend(handles=[l1, l2], loc="upper center")
q.set_title("one legend, handles collected")

print("ax.legend() only sees artists on that axes.")
print("Collect the handles and pass them explicitly for one legend.")'''),

        ("Why twin axes mislead",
         "The crossing point is an artefact of the two scales you chose.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(10)
a_vals = np.linspace(10, 90, 10)
b_vals = np.linspace(80, 20, 10)

fig, axes = plt.subplots(1, 3, figsize=(10, 3))
for ax, (lo, hi) in zip(axes, [(0, 100), (0, 200), (-50, 100)]):
    ax.plot(x, a_vals, color="#264653")
    a2 = ax.twinx()
    a2.plot(x, b_vals, color="#e76f51", linestyle="--")
    a2.set_ylim(lo, hi)
    ax.set_title("right axis %s" % str((lo, hi)), fontsize=9)

print("The same two series, three choices of right-hand limits.")
print("The lines cross in a different place each time - and in the")
print("third they barely meet at all.")
print()
print("A reader sees 'they crossed in June' as a fact about the data.")
print("It is a fact about the axis limits, which you chose.")'''),

        ("The usual alternatives",
         "Two panels, or one scale after normalising.",
         '''import matplotlib.pyplot as plt
import numpy as np

months = np.arange(1, 13)
revenue = np.array([120, 135, 128, 150, 175, 190, 185, 200, 178, 160, 145, 165],
                   dtype=float)
rate = np.array([2.1, 2.3, 2.0, 2.6, 3.1, 3.4, 3.2, 3.6, 3.0, 2.7, 2.4, 2.9])

fig, (a, b) = plt.subplots(2, 1, figsize=(6.5, 4), sharex=True)
a.plot(months, revenue, color="#264653", marker="o")
a.set_ylabel("revenue")
b.plot(months, rate, color="#e76f51", marker="s")
b.set_ylabel("rate %")
fig.suptitle("stacked panels, shared x")

fig2, ax = plt.subplots(figsize=(6.5, 3))
ax.plot(months, revenue / revenue[0] * 100, color="#264653", marker="o",
        label="revenue")
ax.plot(months, rate / rate[0] * 100, color="#e76f51", marker="s",
        label="rate")
ax.set_ylabel("indexed to January = 100")
ax.legend()
ax2 = None

print("Stacked panels with a shared x compare shapes without inventing")
print("a crossing point.")
print("Indexing both to a common base puts them on ONE axis honestly -")
print("now the crossing means something: relative growth diverged.")'''),

        ("secondary_axis is a different thing",
         "One scale shown in two units, with a conversion between them.",
         '''import matplotlib.pyplot as plt
import numpy as np

days = np.arange(0, 60)
temp_c = 18 + 8 * np.sin(days / 12)

fig, ax = plt.subplots(figsize=(7, 3.2))
ax.plot(days, temp_c, color="#2a9d8f")
ax.set_ylabel("temperature (C)")
ax.set_xlabel("day")

sec = ax.secondary_yaxis("right",
                         functions=(lambda c: c * 9 / 5 + 32,
                                    lambda f: (f - 32) * 5 / 9))
sec.set_ylabel("temperature (F)")

print("secondary_yaxis takes a pair of functions: forward and inverse.")
print()
print("This is NOT a second data series. It is the same data relabelled,")
print("so there is no arbitrary scale choice and nothing to mislead.")
print("Celsius/Fahrenheit, mm/inches, log/linear - all safe.")'''),

        ("When a twin axis is reasonable",
         "Related quantities, honestly labelled, where the shape is the point.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(24)
rng = np.random.default_rng(0)
volume = rng.integers(200, 900, 24)
price = 100 + np.cumsum(rng.normal(0, 1.5, 24))

fig, ax = plt.subplots(figsize=(7.5, 3.5))
ax.bar(x, volume, color="0.85", label="volume")
ax.set_ylabel("volume")
ax.set_ylim(0, volume.max() * 3)          # push the bars down

ax2 = ax.twinx()
ax2.plot(x, price, color="#264653", linewidth=2, label="price")
ax2.set_ylabel("price")

print("Price and volume on one chart is the classic defensible case:")
print("bars in the background as context, a line in front as the")
print("subject. The eye does not try to compare them - one is clearly")
print("secondary.")
print()
print("Setting the bar axis limit high pushes the bars to the bottom,")
print("which reinforces that they are background.")'''),
    ],
    [
        "<code>ax.twinx()</code> returns a new axes sharing the x axis; colour each y label and its ticks to match its series.",
        "Each axes owns its artists, so one legend needs the <strong>handles collected</strong> and passed explicitly.",
        "The point where two twinned series <strong>cross is an artefact</strong> of the limits you chose, and readers read it as a fact.",
        "The honest alternatives are <strong>stacked panels</strong> with a shared x, or <strong>indexing</strong> both series to a common base and using one axis.",
        "<code>secondary_yaxis(functions=(fwd, inv))</code> relabels the <em>same</em> data in another unit &mdash; no arbitrary scale, nothing to mislead.",
        "A twin axis is defensible when one series is clearly <strong>background context</strong> &mdash; volume bars behind a price line.",
    ],
    '''
title: Twin and Secondary Axes
intro: Two scales on one plot, and the reasons to think twice.

## twinx and twiny

`ax2 = ax.twinx()` creates a second axes occupying the same space, sharing the x axis and having its own y axis on the right. `twiny()` is the transpose.

Everything drawn on `ax2` uses the right-hand scale. They are genuinely separate axes objects: separate limits, separate ticks, separate artists.

The one styling step that is not optional is **colour-coding**. Set each y label and its tick labels to match the colour of the series that uses it:

```python
ax.set_ylabel("revenue", color=c1)
ax.tick_params(axis="y", labelcolor=c1)
```

Without it, the reader has two scales and no way to tell which belongs to which line, and the chart is simply unreadable.

## The legend problem

`ax.legend()` collects labelled artists **on that axes only**. With a twin, that means each half of the chart gets its own legend, which looks like a mistake.

Collect the handles and pass them to one call:

```python
l1, = ax.plot(..., label="A")
l2, = ax2.plot(..., label="B")
ax.legend(handles=[l1, l2])
```

Or gather them generically with `ax.get_legend_handles_labels()` on each axes and concatenate.

## Why they mislead

This is the part worth taking seriously.

Two series on independent scales have **no defined relationship**. Where they cross, which is above which, whether they diverge &mdash; all of it depends on the limits you chose for the second axis. Change `ax2.set_ylim` and the crossing moves, or disappears.

The third editor draws the same two series three times with different right-hand limits, and they cross in three different places.

Readers do not see it that way. A crossing looks like an event: "revenue overtook cost in June". It is an artefact of a choice you made, usually without thinking about it, because matplotlib picked the limits automatically.

This is the mechanism behind a large share of misleading charts in the wild, and most of them are not deliberate.

## The alternatives

**Stacked panels** with `sharex=True`. Two small charts, one above the other, sharing the time axis. The shapes can be compared, the levels cannot be confused, and no crossing is implied. This is the right answer most of the time.

**Index both to a common base.** Divide each series by its first value and multiply by 100. Both are then percentages of their own starting point, they share one axis honestly, and a crossing now means something real: relative growth diverged.

**Percentage change** does the same job for series where the level is not meaningful.

**Two charts** side by side, when the series have nothing in common but the time axis.

## secondary_axis

`ax.secondary_yaxis("right", functions=(forward, inverse))` is a different mechanism and does not share the drawbacks.

It shows the **same data** in a second unit, with an explicit conversion. Celsius and Fahrenheit, millimetres and inches, a count and a percentage of a known total.

Because the two scales are related by a function rather than by an arbitrary choice, nothing about the chart can mislead: the line is in one place, and the two axes are two ways of reading the same position.

The functions must be inverses of each other, and matplotlib uses both &mdash; forward to place the ticks, inverse to keep them consistent when the view changes.

`secondary_xaxis` does the same horizontally, which is how you put dates on one side and elapsed days on the other.

## When a twin axis is fine

There is a defensible case, and it is narrower than its popularity suggests.

It works when one series is clearly **background context** rather than a co-equal subject. The standard example is price and volume: volume as pale bars pushed to the bottom of the chart, price as a line in front. Nobody tries to compare a bar height with a line position, because the visual hierarchy makes clear which one is the subject.

Setting the bar axis limit to two or three times the data range pushes the bars down and reinforces that.

The test: if a reader might compare the two series against each other, the twin axis is a hazard. If one is obviously scenery, it is a reasonable use of space.

## Ordering and z-order

The twin axes is created after the original, so its artists draw **on top** by default.

That is usually wrong when the first series is the subject: a background bar series drawn on `ax` ends up behind, which is right, but a line drawn on `ax` is covered by anything on `ax2`.

`ax.set_zorder(ax2.get_zorder() + 1)` moves the first axes in front, and `ax.patch.set_visible(False)` is then required, or its opaque background hides the second axes entirely.

That two-line incantation appears in a great deal of twin-axis code, and it exists because the axes are genuinely stacked rather than merged.

## Grid lines on a twin

Both axes can draw a grid, and two grids at different spacings is visual noise that makes both harder to read.

The convention is to grid only the axes whose scale the reader should use for judging values &mdash; usually the primary one &mdash; and to turn the other off:

```python
ax.grid(True, axis="y", alpha=0.3)
ax2.grid(False)
```

Since `ax2` inherits grid settings from rcParams, turning it off explicitly is necessary when the style enables grids by default.

## Aligning the two scales

A frequent request is to make zero on both axes fall at the same height, so the two series are comparable around a baseline.

There is no built-in for it; it is arithmetic on the limits:

```python
def align_zero(a1, a2):
    l1, h1 = a1.get_ylim(); l2, h2 = a2.get_ylim()
    f = l1 / (l1 - h1)
    a2.set_ylim(bottom=(f * h2) / (f - 1) if f != 1 else l2)
```

Whether that is a good idea is another question. Aligning zero makes the chart look more comparable without making it more comparable &mdash; the scales are still unrelated, and the reader is now more likely to compare them.

## Three axes

`ax.twinx()` twice gives a third scale, with the third spine pushed outward:

```python
ax3 = ax.twinx()
ax3.spines["right"].set_position(("outward", 45))
```

It works, and it is almost always a mistake. Three unrelated scales on one plot is three arbitrary choices, and no amount of colour coding makes the crossings meaningful.

If three series must be shown together, three stacked panels sharing an x axis is the display that does it honestly, and it is not much taller.

## The honest summary

Twin axes exist because people want them, and matplotlib provides them without editorialising.

They are appropriate when one series is context and the other is the subject, when the two quantities are related by something the reader knows, or when a convention in the field makes the pairing familiar.

They are inappropriate when the chart invites a comparison of levels or a reading of the crossing point &mdash; which is most of the time, and is why the alternatives in this module are worth reaching for first.

## How the misreading happens

Worth spelling out, because it is not obvious that anything is wrong.

A reader sees two lines. Lines on a chart normally share a scale, so distance between them means something. Here it does not: the vertical gap is the difference between two arbitrary rescalings.

The crossing is worse. A crossing is a visually salient event, and the reader interprets it as "the quantities became equal" &mdash; which is meaningless when the units differ. Move one axis's limits and the crossing moves, or vanishes.

None of that is signalled. The chart looks like every other two-line chart, and the two y axes are the only clue that the usual reading does not apply.

## If you must

When a twin axis is genuinely the right choice, four things make it as safe as it can be.

**Colour-code both axes** to their series, including the tick labels.

**Make the hierarchy obvious** &mdash; one series as background context, the other as the subject.

**Do not let them cross**, if the limits can reasonably be set to avoid it.

**Say in the caption** that the scales are independent.

And check the alternative honestly first. Most twin-axis charts exist because two series were to hand, not because the comparison needed one plot.

## A decision procedure

When a second scale is proposed, four questions settle it.

**Are the units related by a known conversion?** If yes, `secondary_yaxis` with the conversion functions &mdash; safe, and not really a second series at all.

**Is one series clearly background?** If yes, a twin axis is defensible, with the background pushed down and drawn in a pale colour.

**Would indexing both to a common base answer the question?** Usually yes, and it puts them on one honest axis where crossings mean something.

**Would two stacked panels do?** Almost always yes, and it costs nothing but vertical space.

Only if the first two are no and the second two are genuinely unsuitable is a co-equal twin axis the right answer &mdash; and by that point the reasoning has been made explicit, which is the useful part of the exercise.

## In summary

`twinx` gives a second axes sharing the x axis and its own y scale.

Colour-code both axes to their series, or the chart is unreadable.

One legend requires collecting the handles from both axes.

The crossing point is determined by the limits you chose, and readers treat it as a finding &mdash; which is the whole problem.

`secondary_yaxis` with a function pair is a different and safe mechanism, relabelling one series in another unit.

The honest alternatives are stacked panels sharing an x axis, or indexing both series to a common base.

And a twin axis is reasonable when one series is obviously scenery &mdash; volume behind price &mdash; because then nobody is trying to compare them.

## A worked alternative

Given revenue in thousands and conversion rate in percent over twelve months, the twin-axis version puts them on one plot and invites a comparison that is not defined.

Three alternatives, each answering a slightly different question.

**Stacked panels**, sharing the x axis. Answers "how did each move?" and allows the shapes to be compared without implying anything about levels.

**Indexed to January = 100.** Answers "which grew faster?" and puts both on one honest axis, where a crossing genuinely means relative performance diverged.

**A scatter of one against the other**, coloured or labelled by month. Answers "are they related?" directly, which is usually the underlying question when someone reaches for a twin axis.

That third one is worth considering more often. A twin-axis chart is frequently an attempt to show a relationship using a display designed for showing two time series, and a scatter shows the relationship.

## One more thing

`ax2.set_ylim` should generally be set explicitly on a twin axis rather than left automatic.

The reason is reproducibility rather than aesthetics: automatic limits depend on the data, so a chart regenerated next month has a different second scale and the two lines cross somewhere new. If a reader has seen the earlier version, that looks like a change in the data.

## The short version

A second y axis is the only common chart feature whose main effect is on what the reader wrongly concludes.

Everything else in this track can be done badly; a twin axis is difficult to do well even deliberately, because the ambiguity is in the display rather than in the execution. Reaching for stacked panels or a common index first is the habit worth having.

## Reading the code back

A twin axis is one call and a series of mitigations: colour-code both scales, assemble one legend, fix the limits explicitly, establish a visual hierarchy, and say in the caption that the scales are independent. The length of that list is itself the argument for checking whether stacked panels would do instead.
''',
    [
        {"q": "Why must you colour-code the two y axes on a twin plot?",
         "options": ["It looks nicer", "Otherwise the reader has two scales and no way to tell which belongs to which series", "matplotlib requires it", "To pass accessibility checks"],
         "answer": 1,
         "why": "Set both the label colour and tick_params labelcolor. Without it the chart is simply unreadable."},
        {"q": "What determines where two twinned series cross?",
         "options": ["The data", "The axis limits you chose for the second axis", "The colours", "The order drawn"],
         "answer": 1,
         "why": "Readers see a crossing as an event in the data. It is an artefact of a choice usually made automatically."},
        {"q": "What is the honest alternative to a twin axis?",
         "options": ["A bigger figure", "Stacked panels sharing x, or indexing both series to a common base", "A log scale", "More colours"],
         "answer": 1,
         "why": "Indexing puts them on one axis honestly, and then a crossing means something real - relative growth diverged."},
        {"q": "How does `secondary_yaxis` differ from `twinx`?",
         "options": ["It is newer", "It relabels the same data in another unit via a function pair, so there is no arbitrary scale", "It is on the left", "It shares the y axis"],
         "answer": 1,
         "why": "Celsius/Fahrenheit or mm/inches - the two scales are related by a function, so nothing can mislead."},
    ],
)


# ---------------------------------------------------------------------------
# 17. Distributions: box and violin
# ---------------------------------------------------------------------------
topic(
    "box_and_violin",
    "Box and Violin Plots",
    "Working with Data",
    "Comparing many distributions at once, and what each summary throws away.",
    _svg(_box(14, 16, 132, 58, "none", B) +
         '<rect x="34" y="34" width="16" height="24" fill="none" stroke="%s" stroke-width="2"/>'
         '<path d="M42 22 L42 34 M42 58 L42 68 M34 44 L50 44" stroke="%s" stroke-width="2"/>' % (A, A) +
         '<rect x="74" y="28" width="16" height="30" fill="none" stroke="%s" stroke-width="2"/>'
         '<path d="M82 18 L82 28 M82 58 L82 66 M74 40 L90 40" stroke="%s" stroke-width="2"/>' % (A, A)),
    [
        ("What the box contains",
         "Five numbers, and everything beyond the whiskers drawn individually.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
data = np.concatenate([rng.normal(50, 10, 200), [95, 98, 5]])

fig, ax = plt.subplots(figsize=(5, 3.5))
ax.boxplot([data], vert=True, widths=0.5)
ax.set_xticklabels(["sample"])

q1, med, q3 = np.percentile(data, [25, 50, 75])
iqr = q3 - q1
print("Q1     %.1f" % q1)
print("median %.1f  <- the line in the box" % med)
print("Q3     %.1f" % q3)
print("IQR    %.1f  <- the height of the box" % iqr)
print()
print("whiskers reach the furthest point within 1.5 x IQR:")
print("   lower fence %.1f   upper fence %.1f" % (q1 - 1.5*iqr, q3 + 1.5*iqr))
print("points beyond are drawn individually:", int(((data < q1-1.5*iqr) |
                                                    (data > q3+1.5*iqr)).sum()))'''),

        ("Comparing groups is what it is for",
         "Many distributions in the space one histogram would take.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
groups = [rng.normal(m, s, 150) for m, s in
          [(20, 4), (24, 4), (22, 9), (28, 3), (21, 6)]]
names = list("abcde")

fig, ax = plt.subplots(figsize=(7, 3.2))
bp = ax.boxplot(groups, labels=names, patch_artist=True, widths=0.6)
for patch in bp["boxes"]:
    patch.set_facecolor("#a8dadc")
ax.set_ylabel("value")

print("Five distributions, one glance. A grid of five histograms would")
print("take five times the space and be harder to compare.")
print()
print("patch_artist=True makes the boxes fillable; without it they are")
print("outlines and set_facecolor does nothing.")'''),

        ("What the box hides",
         "Two very different distributions can produce the same box.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(2)
unimodal = rng.normal(50, 12, 600)
bimodal = np.concatenate([rng.normal(32, 5, 300), rng.normal(68, 5, 300)])

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3.2))

a.boxplot([unimodal, bimodal], labels=["unimodal", "bimodal"])
a.set_title("boxes: nearly identical")

b.hist(unimodal, bins=30, alpha=0.6, label="unimodal")
b.hist(bimodal, bins=30, alpha=0.6, label="bimodal")
b.legend()
b.set_title("histograms: not remotely alike")

for name, d in [("unimodal", unimodal), ("bimodal", bimodal)]:
    q1, med, q3 = np.percentile(d, [25, 50, 75])
    print("%-9s Q1 %.1f  med %.1f  Q3 %.1f" % (name, q1, med, q3))
print()
print("A box plot is five numbers. Any distribution with those five")
print("numbers draws the same box, including one with a hole in the")
print("middle.")'''),

        ("Violins show the shape",
         "At the cost of a smoothing parameter you did not choose.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
unimodal = rng.normal(50, 12, 600)
bimodal = np.concatenate([rng.normal(32, 5, 300), rng.normal(68, 5, 300)])

fig, ax = plt.subplots(figsize=(6.5, 3.2))
parts = ax.violinplot([unimodal, bimodal], showmedians=True)
ax.set_xticks([1, 2])
ax.set_xticklabels(["unimodal", "bimodal"])

print("The violin shows the two peaks the box hid.")
print()
print("It is a kernel density estimate, so it has a bandwidth - a")
print("smoothing choice, exactly like a histogram's bin count. The")
print("default is chosen for you and can invent or erase structure.")
print()
print("It also extends past the data at both ends, implying values")
print("that were never observed.")'''),

        ("Showing the points as well",
         "The best of both, when the sample is small enough.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(4)
groups = [rng.normal(m, s, 30) for m, s in [(20, 4), (24, 4), (22, 9)]]
names = ["a", "b", "c"]

fig, ax = plt.subplots(figsize=(6.5, 3.5))
bp = ax.boxplot(groups, labels=names, widths=0.5, showfliers=False,
                medianprops=dict(color="crimson", linewidth=2))
for i, vals in enumerate(groups, start=1):
    x = np.full(len(vals), i) + rng.uniform(-0.09, 0.09, len(vals))
    ax.scatter(x, vals, s=14, alpha=0.6, color="#264653", zorder=3)

print("showfliers=False stops the outliers being drawn twice - once by")
print("the box and once by the scatter.")
print()
print("The box gives the summary, the points give the sample size and")
print("the shape. Under about 50 points per group this is strictly")
print("better than either alone.")'''),

        ("Horizontal, and ordered",
         "The same readability arguments as bar charts apply.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(5)
names = ["north region", "south region", "eastern zone", "west", "central"]
groups = [rng.normal(m, 5, 120) for m in [22, 30, 18, 26, 24]]

order = np.argsort([np.median(g) for g in groups])
ordered = [groups[i] for i in order]
ordered_names = [names[i] for i in order]

fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.boxplot(ordered, labels=ordered_names, vert=False, widths=0.6)
ax.set_xlabel("value")

print("vert=False turns them horizontal, so long category names read")
print("normally - the same argument as barh.")
print()
print("Sorting by median makes the comparison immediate. Unsorted")
print("boxes ask the reader to do the ranking themselves.")'''),
    ],
    [
        "A box is <strong>five numbers</strong>: quartiles, median, and whiskers reaching the furthest point within 1.5&times;IQR. Everything beyond is drawn individually.",
        "Box plots exist to compare <strong>many groups at once</strong> in the space one histogram would take.",
        "Any distribution with the same five numbers draws the <strong>same box</strong> &mdash; including a bimodal one with a hole in the middle.",
        "A <strong>violin</strong> shows the shape, at the cost of a bandwidth you did not choose, and it extends past the observed data.",
        "Overlaying the <strong>points</strong> with jitter restores sample size and shape; <code>showfliers=False</code> stops outliers being drawn twice.",
        "<code>vert=False</code> and sorting by median apply the same readability arguments as <code>barh</code>.",
    ],
    '''
title: Box and Violin Plots
intro: Comparing many distributions at once, and what each summary throws away.

## What a box plot is

Five numbers, drawn:

The **box** spans the first to the third quartile, so it contains the middle half of the data. Its height is the interquartile range.

The **line** inside is the median &mdash; not the mean.

The **whiskers** reach the furthest data point within 1.5&times;IQR of the box. They are not a fixed multiple of anything; they stop at real observations.

Points beyond that are drawn **individually** as outliers.

That 1.5 is a convention, chosen so that roughly 0.7% of normally distributed data falls outside. It has no deeper justification, and matplotlib lets you change it with `whis=`.

## What they are for

Comparing many groups.

Five histograms take five panels and require the reader to move between them. Five boxes sit side by side on one axis, sharing a scale, and the comparison is immediate.

That is the whole argument, and it is a strong one. For one distribution, a histogram is better. For eight, a box plot is much better. Somewhere around three the answer changes.

`patch_artist=True` makes the boxes filled rather than outlines, which is needed before `set_facecolor` does anything &mdash; a common small frustration.

## What they hide

A box plot is a summary, and every summary discards.

Any distribution sharing those five numbers produces an identical box. That includes a **bimodal** distribution &mdash; two clusters with a gap in the middle &mdash; whose median sits in the empty space where no data is.

The third editor draws exactly that: two distributions with nearly identical boxes and completely different shapes.

This is not a hypothetical failure. Bimodality usually means two populations have been mixed, which is often the most important thing in the data, and the box plot conceals it perfectly.

The practical rule: look at a histogram of each group **once** before settling on box plots for the comparison.

## Violin plots

A violin shows an estimated density, mirrored, so the width at any height is how much data is around that value. It shows the bimodality a box hides.

Two honest caveats.

It is a **kernel density estimate**, with a bandwidth that smooths the data. That parameter has exactly the arbitrariness of a histogram's bin count, and matplotlib picks it for you. Too much smoothing merges peaks; too little invents them.

It **extends past the observed data** at both ends, because the kernel has tails. A violin of a strictly positive quantity will happily show density below zero, which is a claim the data does not support.

`showmedians=True` adds the median line; the defaults draw the extrema.

## Showing the points

For small samples, the best display is usually both: a box or violin for the summary, and the individual points with jitter on top.

`showfliers=False` prevents the outliers being drawn twice, once by the box and once by the scatter.

`zorder=3` on the scatter puts the points above the box.

Below roughly fifty points per group this is strictly more informative than either element alone: you get the quartiles and the actual sample. Above a few hundred, the points overplot and the summary is doing the work.

## Layout

`vert=False` draws them horizontally, which lets long category names read normally &mdash; the same argument that makes `barh` preferable to `bar`.

Sorting the groups by median makes the ranking immediate rather than something the reader assembles.

And as with any grouped comparison, the y axis must be shared, which it is by construction here &mdash; that is part of why the display works.

## Notches and confidence

`notch=True` draws a waist around the median whose width approximates a 95% confidence interval for it.

The heuristic it enables is that if two notches do not overlap, the medians differ significantly. That is roughly true and depends on assumptions the plot does not state.

Two practical problems. On small samples the notch can extend beyond the box, producing a folded shape that looks like a rendering error. And the heuristic is exactly the overlap reasoning that is unreliable for error bars, applied to a different statistic.

Useful when comparing many groups quickly; not a substitute for a test.

## Ordering and orientation

The same arguments as bar charts apply.

Sort by median unless the category order means something &mdash; time, size, an experimental sequence.

Use `vert=False` when the labels are words.

And keep the y axis shared, which happens automatically here because all groups share one axes, and is exactly why the display works for comparison.

## Styling the parts

`boxplot` returns a dict of the artists, keyed by `"boxes"`, `"whiskers"`, `"caps"`, `"medians"`, `"fliers"`:

```python
bp = ax.boxplot(data, patch_artist=True)
for b in bp["boxes"]:
    b.set(facecolor="#a8dadc", edgecolor="0.3")
for m in bp["medians"]:
    m.set(color="crimson", linewidth=2)
```

`patch_artist=True` is required before boxes can be filled &mdash; without it they are unfillable outlines and `set_facecolor` does nothing, silently.

The property dicts &mdash; `medianprops`, `boxprops`, `whiskerprops`, `flierprops` &mdash; do the same at call time and are usually tidier.

## Violin internals

`violinplot` returns a dict too, with `"bodies"` and optional `"cmedians"`, `"cmeans"`, `"cbars"`.

By default it draws the extrema and no median, which is an odd choice; `showmedians=True` is nearly always wanted.

`widths` controls the maximum thickness, and `bw_method` the smoothing &mdash; a number, or `"scott"` / `"silverman"`. Halving the bandwidth roughly doubles the visible detail and the visible noise.

Because the two halves are mirror images, one half is redundant. A **half violin** paired with the raw points on the other side uses the space better, and is built by clipping the body path &mdash; more work than it sounds, and worth it for a figure that will be published.

## Choosing between them

**Box** &mdash; many groups, when the quartiles are the summary you want and shape is not expected to be interesting.

**Violin** &mdash; when shape matters and the samples are large enough for a density estimate to mean something, roughly a hundred per group.

**Strip or swarm** &mdash; small samples, where the individual values are the honest display.

**Box plus points** &mdash; the general-purpose answer under about fifty per group.

**Histogram grid** &mdash; when the shapes are the subject and there are few enough groups to give each a panel.

The mistake is treating the box plot as the default for all distribution comparison, which is how bimodality goes unnoticed.

## Outliers

The points beyond the whiskers are labelled outliers, and the label is doing more work than the statistics support.

They are simply points more than 1.5&times;IQR from the box. On normally distributed data about 0.7% of observations qualify, so a sample of a thousand produces seven "outliers" that are nothing of the kind.

On skewed data the rule flags far more, all on one side, which is a property of the distribution rather than of the points.

So: a point beyond a whisker is worth looking at and is not evidence of an error. `showfliers=False` hides them when they are distracting, and `whis=(5, 95)` changes the rule to percentiles, which is often more interpretable.

## Sample size

A box plot looks the same for twelve observations and twelve thousand, which is a real weakness when groups differ in size.

Three ways to show it:

**Width proportional to n** &mdash; `widths=` accepts a list, and scaling by the square root of the count is conventional.

**The count in the tick label** &mdash; `"group a\n(n=12)"`.

**The points overlaid**, which shows the sample size directly.

Without one of these, a group of eight and a group of eight hundred are presented as equally reliable, and the reader has no way to know.

## Ordering and grouping

With more than a handful of groups, the arrangement is most of the chart.

**Sort by median** unless the categories have a natural order. It turns a search into a reading.

**Group related categories together** and separate the groups with space, which `positions=` allows: passing `[1, 2, 3, 5, 6, 7]` leaves a gap between two clusters.

**Use colour for the grouping**, not for the individual boxes, so the colour carries the structure rather than repeating the labels.

**Consider a reference line** &mdash; the overall median, a target &mdash; drawn across the whole axes, which turns each box from an isolated summary into a comparison.

With those, twenty boxes on one chart remains readable. Without them, six is already hard.

## In summary

A box is five numbers, and whiskers reach the furthest point within 1.5&times;IQR rather than a fixed multiple.

The display exists to compare many groups at once, which is what it does better than anything else.

It hides shape, and specifically hides bimodality &mdash; two populations mixed together produce a box that looks unremarkable.

A violin restores the shape and introduces a bandwidth you did not choose, plus tails extending past the observed data.

Under about fifty points per group, showing the points with jitter is more informative than either.

And `patch_artist=True`, `showfliers=False` and `vert=False` are the three arguments that come up most: fillable boxes, no double-drawn outliers, and horizontal layout for wordy labels.

## Beeswarm and the alternatives

A strip plot with random jitter shows every point and lets some of them overlap by chance.

A **beeswarm** places the points deterministically so none overlap, which reads better and is not built into matplotlib &mdash; seaborn's `swarmplot` is the usual route, and it refuses to plot when there are too many points to place, which is a reasonable failure.

A **rain cloud** combines three: a half violin for the shape, a box for the summary, and the points below. It is the most complete display of a distribution comparison and takes the most space, which is the trade.

For most work the ordering is: points if the sample is small, box if there are many groups, box plus points in between, and a violin when the shape is genuinely the question and the samples are large enough to estimate it.

What matters more than the choice is knowing what each one hides, which is the theme of this whole module.

## A closing note

Every distribution display is a compromise between completeness and comparability.

The points show everything and compare badly past a few groups. The box compares many groups and hides the shape. The violin restores the shape and adds a smoothing choice. The histogram shows one distribution well and several badly.

There is no display that does all of it, which is why the useful skill is knowing what each one discards rather than having a favourite.

The specific thing worth remembering: a box plot cannot show bimodality, and bimodality usually means two populations have been mixed &mdash; which is frequently the most important fact about the data. Looking at a histogram of each group once, before settling on boxes for the comparison, costs a minute and prevents the failure this module is mostly about.

## The short version

Both displays trade completeness for comparability, and both hide something specific: the box hides shape, the violin hides its own smoothing choice.

Knowing what each discards is more useful than preferring one, and looking at a histogram of each group once before choosing is what prevents the bimodality failure this module exists to describe.

## Reading the code back

A box plot is one call with three arguments worth passing: patch_artist to make the boxes fillable, showfliers to control the outliers, and vert to choose the orientation. The decisions before it are which groups, in what order, and whether the points should be shown as well - and those are what determine whether the chart works.
''',
    [
        {"q": "What do the whiskers on a matplotlib box plot reach?",
         "options": ["The minimum and maximum", "The furthest data point within 1.5x IQR of the box", "Two standard deviations", "The 5th and 95th percentiles"],
         "answer": 1,
         "why": "They stop at real observations, and points beyond are drawn individually. The 1.5 is a convention, changeable with whis=."},
        {"q": "What can a box plot completely hide?",
         "options": ["Outliers", "Bimodality - two clusters with a gap where the median sits", "The median", "The sample size"],
         "answer": 1,
         "why": "Bimodality usually means two populations have been mixed, which is often the most important thing in the data."},
        {"q": "What is the cost of a violin plot?",
         "options": ["It is slow", "It is a kernel density estimate with a bandwidth you did not choose, and it extends past the observed data", "It hides the median", "It needs many groups"],
         "answer": 1,
         "why": "A violin of a strictly positive quantity will show density below zero - a claim the data does not support."},
        {"q": "Why pass `showfliers=False` when overlaying the raw points?",
         "options": ["To hide outliers", "So outliers are not drawn twice, once by the box and once by the scatter", "It is faster", "To fix the colours"],
         "answer": 1,
         "why": "Below about fifty points per group, box plus points is strictly more informative than either alone."},
    ],
)


# ---------------------------------------------------------------------------
# 18. Plotting from pandas
# ---------------------------------------------------------------------------
topic(
    "plotting_from_pandas",
    "Plotting from pandas",
    "Working with Data",
    "df.plot as a shortcut, and when to drop back to matplotlib.",
    _svg(_box(16, 24, 44, 44, S, M) + _txt(38, 50, "DataFrame", M, 7) +
         _arrow(64, 46, 80, 46) + _txt(72, 38, ".plot", A, 7) +
         _box(88, 24, 56, 44, "none", B) +
         '<polyline points="94,60 108,44 122,50 138,32" fill="none" stroke="%s" stroke-width="2"/>' % A),
    [
        ("df.plot draws every column against the index",
         "One call, and pandas supplies the labels and the legend.",
         '''import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

idx = pd.date_range("2024-01-01", periods=60, freq="D")
rng = np.random.default_rng(0)
df = pd.DataFrame({"north": rng.normal(0, 1, 60).cumsum() + 20,
                   "south": rng.normal(0, 1, 60).cumsum() + 25},
                  index=idx)

ax = df.plot(figsize=(7, 3.2))
ax.set_ylabel("value")

print("df.plot() gave, for free:")
print("   the dates on the x axis (from the index)")
print("   a line per column")
print("   a legend, labelled with the column names")
print()
print("It returns an Axes, so everything you know still applies:")
print("   type:", type(ax).__name__)'''),

        ("It returns an Axes, and takes one",
         "Which is how pandas plots fit into a matplotlib layout.",
         '''import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

rng = np.random.default_rng(1)
df = pd.DataFrame({"a": rng.normal(0, 1, 200), "b": rng.normal(1, 2, 200)})

fig, axes = plt.subplots(1, 2, figsize=(9, 3))

df.plot(kind="hist", bins=30, alpha=0.6, ax=axes[0], legend=True)
axes[0].set_title("pandas hist into a subplot")

df.plot(kind="scatter", x="a", y="b", ax=axes[1], alpha=0.4, s=12)
axes[1].set_title("pandas scatter")

fig.tight_layout()

print("ax= sends the plot to an axes you made.")
print("Without it, pandas creates its own figure - which is why a")
print("df.plot inside a subplot loop draws in the wrong place.")'''),

        ("The kinds",
         "One argument covers most of the chart types.",
         '''import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

rng = np.random.default_rng(2)
df = pd.DataFrame({"a": rng.normal(10, 2, 60), "b": rng.normal(12, 3, 60)})
cat = pd.DataFrame({"value": [23, 45, 12, 38]},
                   index=["alpha", "beta", "gamma", "delta"])

fig, axes = plt.subplots(2, 2, figsize=(9, 5))
cat.plot(kind="bar", ax=axes[0, 0], legend=False, title="bar")
cat.plot(kind="barh", ax=axes[0, 1], legend=False, title="barh")
df.plot(kind="box", ax=axes[1, 0], title="box")
df.plot(kind="area", ax=axes[1, 1], stacked=False, alpha=0.4, title="area")
fig.tight_layout()

print("kind = line bar barh hist box kde area pie scatter hexbin")
print()
print("df.plot.bar() is the same thing with nicer syntax, and gives")
print("autocompletion in an editor.")
print()
try:
    df.plot(kind="kde")
except Exception as e:
    print("kde needs scipy, which is not loaded here:")
    print("   ", type(e).__name__, "-", str(e)[:44])
    print("   Several pandas plot kinds have optional dependencies.")'''),

        ("Grouped and stacked, from a frame",
         "A wide frame is already a grouped bar chart.",
         '''import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({"product a": [10, 15, 12],
                   "product b": [8, 18, 14],
                   "product c": [5, 4, 9]},
                  index=["q1", "q2", "q3"])

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))
df.plot(kind="bar", ax=a, rot=0, title="grouped")
df.plot(kind="bar", stacked=True, ax=b, rot=0, title="stacked")

print("Each COLUMN becomes a series; each ROW becomes a group.")
print()
print("So the shape of the frame decides the chart. If the bars come")
print("out grouped the wrong way, the frame needs transposing or")
print("pivoting - not the plot call changing.")
print()
print("df.T.plot(kind='bar') swaps them.")'''),

        ("subplots=True for small multiples",
         "One panel per column, sharing the x axis.",
         '''import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

idx = pd.date_range("2024-01-01", periods=80, freq="D")
rng = np.random.default_rng(3)
df = pd.DataFrame({c: rng.normal(0, 1, 80).cumsum() + base
                   for c, base in [("north", 20), ("south", 40), ("east", 5)]},
                  index=idx)

axes = df.plot(subplots=True, figsize=(7, 4.5), sharex=True, legend=False)
for ax, name in zip(axes, df.columns):
    ax.set_ylabel(name)

print("subplots=True gives one panel per column and returns an ARRAY")
print("of axes rather than a single one.")
print()
print("Note the y axes are independent by default, so the panels are")
print("not comparable - pass sharey=True when they should be.")'''),

        ("When to drop back to matplotlib",
         "pandas is a shortcut; anything unusual is easier underneath.",
         '''import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

idx = pd.date_range("2024-01-01", periods=60, freq="D")
rng = np.random.default_rng(4)
df = pd.DataFrame({"actual": rng.normal(0, 1, 60).cumsum() + 50}, index=idx)
df["target"] = 52

fig, ax = plt.subplots(figsize=(7.5, 3.5))

df["actual"].plot(ax=ax, color="#264653", linewidth=2, label="actual")
ax.axhline(52, color="crimson", linestyle="--", linewidth=1, label="target")
above = df["actual"] > 52
ax.fill_between(df.index, 52, df["actual"], where=above,
                alpha=0.2, color="#2a9d8f")
i = df["actual"].idxmax()
ax.annotate("peak %.1f" % df["actual"].max(), xy=(i, df["actual"].max()),
            xytext=(10, -20), textcoords="offset points",
            arrowprops=dict(arrowstyle="->"))
ax.legend()

print("pandas drew the line. matplotlib did the threshold, the shading")
print("and the annotation - none of which df.plot exposes.")
print()
print("The two mix freely, because df.plot is a thin wrapper that")
print("returns the same Axes object.")'''),
    ],
    [
        "<code>df.plot()</code> draws every column against the index and supplies labels and a legend from the column names.",
        "It <strong>returns an Axes</strong> and accepts <code>ax=</code>, which is how pandas plots fit into a matplotlib layout.",
        "<code>kind=</code> covers line, bar, barh, hist, box, kde, area, pie, scatter and hexbin; <code>df.plot.bar()</code> is the same with better syntax.",
        "Each <strong>column</strong> is a series and each <strong>row</strong> a group &mdash; so the frame's shape decides the chart, and <code>df.T</code> swaps them.",
        "<code>subplots=True</code> gives one panel per column and returns an <strong>array</strong> of axes; the y axes are independent unless you pass <code>sharey</code>.",
        "pandas is a shortcut for the common cases; annotations, thresholds and shading are easier in matplotlib, and the two mix freely.",
    ],
    '''
title: Plotting from pandas
intro: df.plot as a shortcut, and when to drop back to matplotlib.

## What it does for you

`df.plot()` draws every column as a line against the index, adds a legend labelled with the column names, and formats the x axis appropriately for the index type.

For a time-indexed frame that is a dated axis, sensible tick spacing, one line per column and a legend &mdash; from one call. Doing the same in raw matplotlib is five or six lines.

That is the case for using it: for exploration, and for the common chart types, it is simply faster.

## It is a thin wrapper

The important thing to know is that `df.plot` **returns a matplotlib Axes**, and accepts one through `ax=`.

That means it is not a separate system. Everything in this track applies to the result:

```python
fig, ax = plt.subplots()
df.plot(ax=ax)
ax.set_title(...)
ax.axhline(...)
```

`ax=` also matters for a different reason: without it, pandas creates its **own** figure. A `df.plot` call inside a loop over subplots draws each chart in a new figure rather than the panel you intended, which is a common and confusing result.

## kinds

`kind=` selects the chart: `"line"` (the default), `"bar"`, `"barh"`, `"hist"`, `"box"`, `"kde"`, `"area"`, `"pie"`, `"scatter"`, `"hexbin"`.

`df.plot.bar()` is equivalent and reads better, with the advantage that an editor can autocomplete the method names and their arguments.

`scatter` and `hexbin` need `x=` and `y=` naming columns, since they take two variables rather than plotting everything against the index.

Most keyword arguments are passed through to matplotlib, so `alpha`, `color`, `linewidth` and the rest work as expected.

## The frame's shape is the chart

This is the part that determines whether the output is what you wanted.

Each **column** becomes a series. Each **row** becomes a position on the x axis.

So a frame with quarters as rows and products as columns gives grouped bars with one cluster per quarter. If you wanted one cluster per product, the frame needs transposing &mdash; `df.T.plot(kind="bar")` &mdash; not a different plotting argument.

When a chart comes out grouped the wrong way, the fix is nearly always a `pivot`, a `groupby().unstack()`, or a transpose. That is the reshaping module doing its job: **getting the frame into the right shape is the plotting work**, and the plot call is then trivial.

`stacked=True` stacks bars or areas.

## subplots=True

`df.plot(subplots=True)` gives one panel per column and returns an **array** of axes rather than one.

It is the fastest route to small multiples, and it has a default worth knowing: the y axes are **independent**, so the panels are not comparable. `sharey=True` fixes it, and without it a panel showing a range of 0&ndash;2 sits beside one showing 0&ndash;2000 at the same visual height.

`layout=(2, 3)` arranges them in a grid rather than a column.

## When to drop back

pandas covers the common cases and exposes nothing beyond them.

Reach for matplotlib when you need:

annotations, arrows or text;

reference lines and shaded regions;

a second y axis, or a secondary unit;

fine control of ticks, formatters or scales;

anything drawn conditionally &mdash; highlighting one series, greying the rest.

The good news is that this is not a switch. `df.plot(ax=ax)` for the data and `ax.` methods for everything else is the normal way to work, and it is why the wrapper is worth having.

## And when to leave both

For statistical charts &mdash; faceted grids, regression plots with confidence bands, categorical scatter with built-in jitter &mdash; seaborn sits on top of matplotlib and produces them in one call, returning matplotlib objects you can adjust afterwards.

For interactive charts in a browser, Plotly or Altair. matplotlib's interactivity is limited and not its purpose.

Knowing where matplotlib stops is part of using it well; it is a drawing library that happens to have statistical conveniences, not a statistical graphics system.

## What pandas adds

Beyond convenience, three things are genuinely easier through pandas.

**The index becomes the x axis**, with date formatting handled. That alone removes several lines for any time series.

**Column names become labels**, so the legend is built from the data rather than from a list you maintain separately.

**Groupby output plots directly**: `df.groupby("k")["v"].sum().plot(kind="barh")` goes from raw rows to a chart in one line, because the aggregation produces exactly the index-and-values shape the plot wants.

That last point is the real workflow: reshape until the frame *is* the chart, then plot it.

## Common frame shapes

**A time-indexed frame, one column per series** &rarr; `df.plot()` gives a multi-line chart.

**A frame indexed by category, one column per group** &rarr; `df.plot(kind="bar")` gives grouped bars.

**A long frame** &mdash; one row per observation with a category column &mdash; needs pivoting first: `df.pivot(index=..., columns=..., values=...)`.

**A group-by result with two keys** &rarr; `.unstack()` puts one key into columns, giving the wide shape the plot needs.

Recognising which of these you have, and which the chart needs, is most of the work. The plot call is one line either way.

## Where pandas gets in the way

`df.plot` has its own opinions that occasionally conflict with matplotlib's.

It sets its own tick locators for date axes, which are usually good and are awkward to override afterwards &mdash; setting a matplotlib locator on an axes pandas has already formatted sometimes has no effect, and plotting with `ax.plot(df.index, df[col])` instead gives back full control.

It creates a figure if not given one, which is the `ax=` issue.

And `secondary_y=True` exists and produces a twin axis with all the problems from that module, plus a legend that is harder to assemble.

For anything beyond the standard cases, dropping to `ax.plot(df.index, df["col"])` costs one line and removes the ambiguity about who owns the axes.

## Categorical bar charts

`df.plot(kind="bar")` uses the index as the categories and draws them at integer positions, with the labels rotated 90 degrees by default.

`rot=0` stops the rotation. `kind="barh"` is usually better still, for the reasons in the bar module.

Sorting is a pandas operation, not a plotting one: `df.sort_values("v").plot(kind="barh")`. That is a small example of the general pattern &mdash; the data manipulation belongs in pandas, and the plot call should be trivial.

## Beyond pandas

`df.plot` covers the standard charts. seaborn covers the statistical ones &mdash; faceted grids, regression with bands, categorical scatter with jitter built in &mdash; and returns matplotlib objects, so the same adjustment methods apply afterwards.

The three layers work together: pandas for the data, seaborn for the statistical display, matplotlib for the final control. Knowing which layer a problem belongs to is most of using them well, and the answer for "make this specific thing look right" is almost always the bottom one.

## A complete example

The typical shape of real plotting code, where the data work dominates:

```python
summary = (df
           .query("year == 2024")
           .groupby(["region", "month"], as_index=False)["sales"].sum()
           .pivot(index="month", columns="region", values="sales"))

fig, ax = plt.subplots(figsize=(7.5, 3.5))
summary.plot(ax=ax, linewidth=2)
ax.set_title("Sales by region, 2024", loc="left", fontweight="bold")
ax.set_ylabel("Sales (thousands)")
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
```

Four lines of pandas to get the frame into the shape of the chart, one to draw it, and four to finish it.

That ratio is normal, and it is why reshaping is a plotting skill.

## Pitfalls

**Forgetting `ax=`**, so the plot lands in its own figure.

**The wrong frame shape**, giving bars grouped by the wrong variable.

**Rotated labels by default** on `kind="bar"`, fixed with `rot=0` or by using `barh`.

**`secondary_y=True`**, which is a twin axis with all its problems.

**Assuming shared axes** with `subplots=True`, where the default is independent.

**A datetime index that is really strings**, giving a categorical axis with no gaps.

The last is worth checking with `df.index.dtype` before wondering why the spacing looks wrong.

## The three layers

Real plotting code sits across three libraries, and knowing which one owns a problem saves a lot of searching.

**pandas** owns the data: filtering, grouping, pivoting, resampling. If the chart is grouped by the wrong thing, or the bars are clustered incorrectly, or a date axis is behaving like a category, the fix is here &mdash; in the shape or the dtypes, not in the plot call.

**seaborn** owns statistical display: faceting, regression with bands, categorical scatter with jitter, distribution comparisons. If you are writing twenty lines to build a grid of conditioned plots, this layer already has it.

**matplotlib** owns the drawing: annotations, reference lines, exact ticks, colour control, layout, saving. Everything the other two produce is a matplotlib object, so this layer is always available underneath.

The common mistake is trying to solve a data problem in the plotting call &mdash; adding arguments to `df.plot` to fix a grouping that should have been a `pivot`.

## In summary

`df.plot()` draws every column against the index and builds the legend from the column names.

It returns an Axes and takes one, which is what makes it a shortcut rather than a separate system &mdash; and `ax=` is required, or a plot inside a subplot loop creates its own figure.

The frame's shape is the chart: columns are series, rows are groups, and a chart grouped the wrong way needs a transpose or a pivot.

`subplots=True` gives small multiples and independent y axes unless you say otherwise.

Reach for matplotlib for annotations, thresholds, shading and exact control &mdash; and mix freely, because it is the same Axes object either way.

## Reshaping is the plotting work

The recurring lesson of this module is worth stating on its own.

The plot call is usually one line. The work is getting the frame into a shape where that one line is correct.

**A wide frame** &mdash; one column per series, index as x &mdash; is what a multi-line chart or a grouped bar chart wants.

**A long frame** &mdash; one row per observation &mdash; is what seaborn and most statistical tools want.

**An aggregated frame** &mdash; one row per group &mdash; is what a bar chart of totals wants.

Moving between them is `pivot`, `melt`, `groupby().agg()` and `unstack`, all covered in the pandas track.

When a chart comes out grouped by the wrong variable, or with the series and categories swapped, or with one line where there should be five, the fix is almost never an argument to `plot` &mdash; it is the shape of the frame. Recognising that immediately saves a lot of time reading plotting documentation for something the data work should have solved.

## A closing note

`df.plot` is a shortcut, and its value is proportional to how standard the chart is.

For a quick line chart of a time-indexed frame it is unbeatable: one call, correct axis, legend included. For anything with an annotation, a threshold, a highlighted series or a specific tick format, it stops helping and matplotlib underneath does the work.

The two together are the normal way to write plotting code, and the boundary is not a decision you make once &mdash; `df.plot(ax=ax)` followed by half a dozen `ax.` calls is a perfectly ordinary chart.

What is worth internalising is that most plotting problems are data problems. When the chart is grouped wrongly, or has too many lines, or shows a category as a number, the fix is in the frame.

## The short version

`df.plot` is a shortcut that returns a matplotlib Axes, which is what makes it a convenience rather than a separate system.

Its limits arrive quickly, and the boundary is not a decision made once: `df.plot(ax=ax)` followed by half a dozen `ax.` calls is ordinary code. And most plotting problems are data problems.
''',
    [
        {"q": "What does `df.plot()` use for the x axis?",
         "options": ["The first column", "The index", "Row numbers always", "You must specify it"],
         "answer": 1,
         "why": "Which is why a time-indexed frame gives a dated axis for free, with one line per column and a legend."},
        {"q": "Why pass `ax=` to `df.plot`?",
         "options": ["For speed", "Without it pandas creates its own figure, so a plot inside a subplot loop lands in the wrong place", "It is required", "To set the title"],
         "answer": 1,
         "why": "df.plot returns and accepts a matplotlib Axes, which is what makes the two mix freely."},
        {"q": "Your grouped bars are clustered by the wrong variable. What do you change?",
         "options": ["The kind argument", "The shape of the frame - transpose or pivot it", "The colours", "The legend"],
         "answer": 1,
         "why": "Each column is a series and each row a group, so getting the frame into the right shape is the plotting work."},
        {"q": "What is the default for the y axes with `subplots=True`?",
         "options": ["Shared", "Independent, so the panels are not comparable", "Log scale", "Hidden"],
         "answer": 1,
         "why": "Pass sharey=True, or a panel ranging 0-2 sits beside one ranging 0-2000 at the same visual height."},
    ],
)


# ---------------------------------------------------------------------------
# 19. Choosing a chart
# ---------------------------------------------------------------------------
topic(
    "choosing_a_chart",
    "Choosing a Chart",
    "Design",
    "Matching the display to the question, and the two chart types worth "
    "avoiding.",
    _svg(_box(16, 24, 36, 40, "none", B) +
         '<polyline points="22,56 32,40 42,48" fill="none" stroke="%s" stroke-width="2"/>' % A +
         _box(60, 24, 36, 40, "none", B) +
         '<rect x="66" y="42" width="7" height="18" fill="%s"/><rect x="78" y="34" width="7" height="26" fill="%s"/>' % (A, A) +
         _box(104, 24, 36, 40, "none", B) +
         '<circle cx="114" cy="52" r="3" fill="%s"/><circle cx="126" cy="38" r="3" fill="%s"/>' % (A, A)),
    [
        ("The question decides the chart",
         "Four common questions, four displays.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
fig, axes = plt.subplots(2, 2, figsize=(9, 5))

t = np.arange(40)
axes[0, 0].plot(t, rng.normal(0, 1, 40).cumsum())
axes[0, 0].set_title("change over time -> line")

axes[0, 1].barh(list("abcd"), sorted(rng.integers(5, 40, 4)))
axes[0, 1].set_title("compare categories -> bar")

x = rng.normal(size=200)
axes[1, 0].scatter(x, x * 0.6 + rng.normal(size=200), s=12, alpha=0.5)
axes[1, 0].set_title("relationship -> scatter")

axes[1, 1].hist(rng.normal(size=500), bins=25)
axes[1, 1].set_title("distribution -> histogram")
fig.tight_layout()

print("time      -> line")
print("categories-> bar, horizontal, sorted")
print("relation  -> scatter")
print("spread    -> histogram, box or the points themselves")
print()
print("Most charts are one of these four. Reaching for something more")
print("exotic usually means the question has not been stated yet.")'''),

        ("Pie charts, and why not",
         "Angle is the hardest visual encoding to compare.",
         '''import matplotlib.pyplot as plt
import numpy as np

vals = np.array([23, 21, 19, 20, 17])
names = ["a", "b", "c", "d", "e"]

fig, (p, q) = plt.subplots(1, 2, figsize=(9, 3.4))

p.pie(vals, labels=names, autopct="%.0f%%")
p.set_title("which is largest?")

order = np.argsort(vals)
q.barh([names[i] for i in order], vals[order])
q.set_title("obvious")

print("values:", dict(zip(names, vals)))
print()
print("Five similar slices are genuinely hard to rank by eye, because")
print("people compare angles badly and areas only slightly better.")
print("The same numbers as a sorted bar chart are trivial.")
print()
print("A pie is defensible for two or three parts of an obvious whole.")
print("Beyond that a bar chart is better in every way.")'''),

        ("Dual axes, restated",
         "Included here because it is the other one worth avoiding.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.arange(20)
a_vals = np.linspace(10, 90, 20)
b_vals = np.linspace(80, 20, 20)

fig, (p, q) = plt.subplots(1, 2, figsize=(9, 3.2))

p.plot(x, a_vals, color="#264653")
p2 = p.twinx()
p2.plot(x, b_vals, color="#e76f51")
p2.set_ylim(0, 300)
p.set_title("crossing point is arbitrary")

q.plot(x, a_vals / a_vals[0] * 100, color="#264653", label="A")
q.plot(x, b_vals / b_vals[0] * 100, color="#e76f51", label="B")
q.set_ylabel("indexed to start = 100")
q.legend()
q.set_title("one honest axis")

print("Changing the right-hand limits moves where the lines cross,")
print("and readers treat the crossing as a finding.")
print()
print("Indexing both to a common base gives one axis and a crossing")
print("that means something: relative growth diverged.")'''),

        ("Small multiples beat one busy chart",
         "Seven series on one axes is a hairball; seven panels is a comparison.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)
series = {name: rng.normal(0, 1, 60).cumsum() + 20
          for name in ["a", "b", "c", "d", "e", "f"]}

fig, ax = plt.subplots(figsize=(6.5, 3))
for name, y in series.items():
    ax.plot(y, label=name)
ax.legend(ncol=3, fontsize=8)
ax.set_title("six series, one axes")

fig2, axes = plt.subplots(2, 3, figsize=(8, 3.6), sharex=True, sharey=True)
for ax2, (name, y) in zip(axes.flat, series.items()):
    ax2.plot(y, color="#264653")
    ax2.set_title(name, fontsize=9)
fig2.suptitle("the same data as small multiples")
fig2.tight_layout()

print("The first chart makes you trace six colours through a legend.")
print("The second lets you see each shape and compare across panels,")
print("because sharey means the heights mean the same thing.")'''),

        ("Highlight rather than colour everything",
         "One series in colour, the rest in grey, says what the chart is about.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(2)
names = ["a", "b", "c", "d", "e", "f", "g"]
series = {n: rng.normal(0, 1, 50).cumsum() + 20 for n in names}
focus = "d"

fig, (p, q) = plt.subplots(1, 2, figsize=(10, 3.2), sharey=True)

for n, y in series.items():
    p.plot(y, label=n)
p.legend(ncol=4, fontsize=7)
p.set_title("all seven equally loud")

for n, y in series.items():
    if n == focus:
        continue
    q.plot(y, color="0.8", linewidth=1)
y = series[focus]
q.plot(y, color="crimson", linewidth=2.5)
q.text(len(y) - 1, y[-1], "  " + focus, color="crimson", va="center")
q.set_title("one highlighted, the rest as context")

print("The grey lines still provide the range for comparison.")
print("The coloured one is the subject. Nobody has to read a legend.")'''),

        ("The checklist",
         "What to look at before a chart leaves your screen.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
months = np.arange(1, 13)
y = np.array([12, 15, 14, 18, 22, 25, 24, 27, 23, 20, 18, 21])

fig, ax = plt.subplots(figsize=(7, 3.5))
ax.plot(months, y, marker="o", color="#264653", linewidth=2)
i = y.argmax()
ax.plot(months[i], y[i], marker="o", color="crimson", markersize=10)
ax.set_title("Sales peaked in August, then fell 22%",
             loc="left", fontsize=12, fontweight="bold")
ax.set_xlabel("Month of 2024")
ax.set_ylabel("Sales (thousands)")
ax.set_ylim(0, 30)
ax.grid(True, axis="y", alpha=0.3)
ax.set_axisbelow(True)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

for line in [
    "1. does the title say the finding, not the variables?",
    "2. do the axis labels carry units?",
    "3. is the baseline right - zero for bars?",
    "4. is anything hidden by overplotting?",
    "5. is the ink that is not data doing any work?",
    "6. would it survive greyscale?",
    "7. is there one message, or several fighting?",
]:
    print(line)'''),
    ],
    [
        "Time is a <strong>line</strong>, categories are a <strong>sorted horizontal bar</strong>, relationships are a <strong>scatter</strong>, spread is a <strong>histogram or box</strong>.",
        "<strong>Pie charts</strong> ask readers to compare angles, which they do badly. A sorted bar chart is better in every way beyond two or three slices.",
        "<strong>Dual axes</strong> put the crossing point under your control rather than the data's; index both series instead.",
        "<strong>Small multiples</strong> with shared axes beat six series on one chart &mdash; the reader compares shapes instead of tracing colours.",
        "<strong>Highlighting</strong> one series and greying the rest says what the chart is about without a legend.",
        "Before it leaves your screen: title states the finding, units on the labels, right baseline, nothing hidden, no wasted ink, survives greyscale, one message.",
    ],
    '''
title: Choosing a Chart
intro: Matching the display to the question, and the two chart types worth avoiding.

## Start from the question

Most charts answer one of four questions, and each has a standard display:

**How did this change over time?** A line chart. Time on the x axis, left to right.

**How do these categories compare?** A bar chart &mdash; horizontal, so the labels read, and sorted, so the ranking is immediate.

**Is there a relationship between these two things?** A scatter plot.

**How is this distributed?** A histogram for one group, box plots or the points themselves for several.

That covers the large majority of real charts. When none of them fits, it is usually because the question has not been stated precisely, and stating it identifies the chart.

The corollary: decide the question first. A chart made by plotting the data and then deciding what it shows is usually a chart of several things at once.

## Why encodings matter

Some visual channels are read more accurately than others. Roughly, in order:

**Position** along a common scale &mdash; the most accurate. This is what a line, a scatter and a dot plot use.

**Length** from a common baseline &mdash; nearly as good. Bars.

**Angle and area** &mdash; noticeably worse. Pies, bubbles.

**Colour intensity** &mdash; worse again, and good only for ordering, not for reading values.

That ordering is why a bar chart beats a pie chart, why bubble size should never carry the main message, and why a heatmap needs its numbers written in when the values matter.

## Pie charts

A pie asks the reader to compare angles. With two or three slices of an obvious whole, that is fine, and the shape communicates "parts of a total" immediately.

With five similar slices it fails: ranking them by eye is genuinely difficult, which is why almost every pie chart in the wild has its percentages printed on it &mdash; an admission that the picture is not doing the work.

The same numbers as a sorted horizontal bar chart are trivially readable, and the bar chart also shows the magnitudes rather than only the proportions.

Donut charts are pies with the middle removed, which makes them slightly worse, because the angle is now inferred from an arc.

## Dual axes

The other display worth avoiding, covered fully in its own module.

The short version: two series on independent scales have no defined relationship, so where they cross is determined by the limits you chose. Readers see the crossing as a finding.

Stacked panels sharing an x axis, or indexing both series to a common base, say the same thing without inventing a fact.

## Small multiples

Six series on one axes is a hairball with a legend. The reader traces each colour, loses it in a crossing, and consults the legend repeatedly.

Six small panels, sharing axes, let them see each shape directly and compare across panels. The shared scale is what makes the comparison valid, and the panel title replaces the legend.

This is one of the most reliable improvements available, and matplotlib makes it one call: `plt.subplots(2, 3, sharex=True, sharey=True)`.

The trade-off is that comparing two specific series is harder when they are in different panels. If the chart is about one comparison, put those two on one axes; if it is about the set, use multiples.

## Highlighting

When one series is the subject and the others are context, say so with colour: the subject in a strong colour and heavier line, the rest in light grey.

The grey lines still give the range and the shape of the group, so nothing is lost. The reader's eye goes to the subject immediately, and no legend is needed if the highlighted line is labelled at its end.

This is more effective than an annotation, because it directs attention by contrast rather than by adding another thing to read.

## The checklist

Before a chart leaves your screen:

Does the **title state the finding**, rather than naming the variables?

Do the **axis labels carry units**?

Is the **baseline** right &mdash; zero for bars, and does a truncated line axis need saying?

Is anything **hidden** &mdash; overplotted points, a series behind another, a category off the edge?

Is the **non-data ink** doing work &mdash; the grid, the frame, the legend, the tick marks?

Would it **survive greyscale**, and colour-vision deficiency?

Is there **one message**, or several competing? Two charts each saying one thing beat one saying both.

None of these is about matplotlib, which is the point. The library will draw whatever you ask; the choices are yours, and they are what makes a chart worth looking at.

## Ranking, not just comparing

"Compare categories" splits into two questions that want different charts.

**Which is biggest?** A sorted horizontal bar chart, and nothing else comes close.

**How does each compare with a reference?** A dot plot against a line, or a bar of the difference from the reference, which puts the comparison on the axis instead of asking the reader to subtract.

The second is under-used. A chart of "actual minus target" answers the question directly, where two bars per category makes the reader do the arithmetic.

## Part-to-whole

Four displays, in decreasing order of how well they work.

**Stacked bar normalised to 100%** &mdash; comparable across groups, and readable for four or five parts.

**A single stacked bar** &mdash; fine for one composition with few parts.

**Small multiples of the parts** &mdash; better when the individual trends matter more than the composition.

**A pie** &mdash; two or three parts, and only when "these are shares of one thing" is the message rather than the values.

Treemaps handle many parts and are hard to compare precisely; they suit hierarchy more than proportion.

## Distribution over time

A frequent question with no single good answer.

**A line of the median with a shaded interquartile band** works well and shows the middle and the spread.

**A box plot per period** works when the periods are few.

**A heatmap of time against value bins** shows the full distribution and takes practice to read.

**Individual lines, greyed** &mdash; a spaghetti plot with a highlighted median &mdash; works when the number of entities is modest and their individual paths matter.

The wrong answer is a line of the mean alone, which hides everything that changed about the spread.

## Two variables plus a third

A scatter with colour is the first choice; a scatter with size is second and much weaker.

If the third variable is categorical with few levels, **small multiples** &mdash; one scatter per level, shared axes &mdash; beat colour, because comparing panels is easier than separating overlapping colours.

If it is continuous, colour with a sequential map and a colorbar.

Encoding four variables on one chart is usually a mistake; the fourth becomes decoration, and the chart takes longer to read than two charts would.

## The general rule

Every chart makes the reader do some work, and the choice of chart decides how much.

A sorted bar chart asks them to read a ranking that is already visible. An unsorted one asks them to sort. A pie asks them to compare angles. A dual-axis chart asks them to hold two scales at once. A twelve-line chart asks them to trace colours through a legend.

The best chart is usually the one that has already done the work &mdash; sorted, filtered, highlighted, labelled &mdash; leaving the reader only the conclusion.

## Charts for a specific audience

The same data justifies different charts depending on who is reading.

**For yourself, exploring** &mdash; density, defaults, many panels. Nothing needs labelling because you know what it is, and speed matters more than polish.

**For a colleague** &mdash; labelled, titled, one message per chart, and the caveats visible.

**For a presentation** &mdash; one chart, one message, large text, minimal reference material, and the conclusion in the title. The reader has seconds and cannot zoom.

**For a document** &mdash; sized for the column, with a caption carrying the detail that would clutter the chart.

The mistake is showing an exploratory chart to an audience, which is how a chart with eleven series and no title ends up in a meeting.

## The one-message rule

The most useful constraint in charting is that a chart should say one thing.

It forces the choices: which variable is on which axis, what to highlight, what to leave out, what the title claims.

A chart trying to say three things usually says none, because the reader cannot tell which of the three to look at, and the elements supporting each compete with the others.

Two charts each saying one thing take the same space and communicate more. Splitting is nearly always the right answer when a chart feels crowded, and "what is this chart for?" is the question that resolves most design arguments about it.

## Redesigning a chart

A practical exercise: take a chart that is not working and improve it without changing the data.

The sequence that usually helps, in order:

**State the message in a sentence.** If that is hard, the chart is trying to do more than one thing.

**Remove everything the sentence does not need.** Series, gridlines, the legend if direct labels would do, tick marks, the box around the plot.

**Sort, if the order is arbitrary.**

**Highlight the subject** and grey the rest.

**Put the sentence in the title.**

**Label the thing the sentence refers to.**

Six steps, none of which requires new data, and together they turn a chart that shows the numbers into one that makes the point. Most charts improve substantially and the code gets shorter, because most of the steps remove something.

## In summary

Time is a line, categories are a sorted horizontal bar, relationships are a scatter, distributions are a histogram or a box.

Position is read most accurately, then length; angle and area much less well. That ordering is why bars beat pies and why bubble size should never carry the main message.

Dual axes put the crossing point under your control rather than the data's.

Small multiples beat many series on one chart when the question is about the set; highlighting beats a legend when it is about one.

And the best chart is the one that has already done the reader's work: sorted, filtered, labelled, with the conclusion in the title and nothing else competing for attention.

## A closing note

Everything else in this track is mechanism; this module is the part that decides whether the mechanism was worth using.

The recurring theme is that a chart is a piece of communication, and the reader's effort is the cost. Sorting, filtering, highlighting and labelling all move work from the reader to the author, and the best charts have had the most work moved.

The chart types worth avoiding &mdash; pies with many slices, dual axes, truncated bars &mdash; are all cases where the display asks the reader to do something people do badly, or invites a conclusion the data does not support.

And the most useful single constraint remains the simplest: one chart, one message. Almost every design question resolves once that is decided.

## Reading the code back

Choosing is done before any code: what question, what encoding, what to leave out, what the title will claim. A chart written from those four answers is usually short, because most of the length in plotting code comes from adjusting a display that was not the right one to begin with.
''',
    [
        {"q": "Which visual encoding do people read most accurately?",
         "options": ["Angle", "Position along a common scale", "Area", "Colour intensity"],
         "answer": 1,
         "why": "Length from a common baseline is close behind. Angle and area are noticeably worse, which is why bars beat pies."},
        {"q": "Why do almost all pie charts print their percentages?",
         "options": ["Convention", "Because the picture is not doing the work - angles are hard to compare", "To save space", "For accessibility"],
         "answer": 1,
         "why": "A sorted horizontal bar chart shows the same data readably, and shows magnitudes rather than only proportions."},
        {"q": "When are small multiples better than one chart with six series?",
         "options": ["Never", "When the question is about the set - shared axes make the panels comparable", "Only for time series", "When there is no legend"],
         "answer": 1,
         "why": "If the chart is about one specific comparison, put those two series on one axes instead."},
        {"q": "What is the advantage of greying out all but one series?",
         "options": ["It saves ink", "It directs attention by contrast, and the grey lines still provide the range", "It is faster to draw", "It avoids colormaps"],
         "answer": 1,
         "why": "More effective than an annotation, because it does not add another thing to read."},
    ],
)


# ---------------------------------------------------------------------------
# 20. Performance and large data
# ---------------------------------------------------------------------------
topic(
    "performance",
    "Performance and Large Data",
    "Output",
    "What makes a figure slow, and what to do when there are more points than "
    "pixels.",
    _svg(_box(14, 16, 132, 58, "none", B) +
         _txt(80, 34, "1,000,000", "#e88", 11) + _txt(80, 52, "points", "#e88", 9) +
         _arrow(80, 60, 80, 70)),
    [
        ("Drawing cost grows with artists, not data",
         "One line of a million points is fast; a million lines is not.",
         '''import matplotlib.pyplot as plt
import numpy as np
import time

rng = np.random.default_rng(0)
n = 20_000
x, y = rng.random(n), rng.random(n)

def timed(fn):
    t = time.perf_counter()
    fig = fn()
    fig.canvas.draw()
    d = time.perf_counter() - t
    plt.close(fig)
    return d

# the first draw of the session pays for font and backend setup, which
# would otherwise be billed to whichever test ran first
warm, wax = plt.subplots(figsize=(1, 1))
wax.plot([0, 1], [0, 1])
warm.canvas.draw()
plt.close(warm)

def one_line():
    fig, ax = plt.subplots(figsize=(4, 2)); ax.plot(x, y, linewidth=0.2)
    return fig

def many_calls():
    fig, ax = plt.subplots(figsize=(4, 2))
    for i in range(0, 2000, 1):
        ax.plot(x[i:i+2], y[i:i+2], color="C0")
    return fig

one = timed(one_line)
many = timed(many_calls)
print("1 call, %d points      : %.3f s" % (n, one))
print("2000 calls, 4000 points  : %.3f s" % many)
print("ratio                    : %.1fx" % (many / max(one, 1e-9)))
print()
print("The second draws a FIFTH of the data and takes longer, because")
print("each call creates an artist to manage and draw. Passing arrays")
print("to one call is the single biggest speed factor.")

fig, ax = plt.subplots(figsize=(5, 2.5))
ax.plot(x[:2000], y[:2000], linewidth=0.2)
ax.set_title("one call")'''),

        ("scatter versus plot for many points",
         "The uniform case is faster, because there is less to vary.",
         '''import matplotlib.pyplot as plt
import numpy as np
import time

rng = np.random.default_rng(1)
n = 50_000
x, y = rng.random(n), rng.random(n)

def timed(make):
    t = time.perf_counter()
    fig = make(); fig.canvas.draw()
    d = time.perf_counter() - t
    plt.close(fig); return d

def with_scatter():
    fig, ax = plt.subplots(figsize=(4, 2)); ax.scatter(x, y, s=2); return fig

def with_plot():
    fig, ax = plt.subplots(figsize=(4, 2))
    ax.plot(x, y, "o", markersize=1.5); return fig

print("scatter, %d points : %.3f s" % (n, timed(with_scatter)))
print("plot   , %d points : %.3f s" % (n, timed(with_plot)))
print()
print("scatter carries a per-point size and colour even when they are")
print("all the same. plot draws one uniform collection, so it is")
print("faster - use it when the markers do not need to vary.")

fig, ax = plt.subplots(figsize=(5, 2.5))
ax.plot(x[:5000], y[:5000], "o", markersize=1, alpha=0.3)
ax.set_title("plot with markers")'''),

        ("More points than pixels",
         "Beyond a certain n, the extra points cannot be seen at all.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(2)
n = 200_000
x = np.sort(rng.uniform(0, 100, n))
y = np.sin(x / 5) + rng.normal(0, 0.3, n)

fig, (a, b) = plt.subplots(2, 1, figsize=(7.5, 4))

a.plot(x, y, linewidth=0.3)
a.set_title("%d points" % n)

step = n // 2000
a2 = b.plot(x[::step], y[::step], linewidth=0.8)
b.set_title("every %dth point (%d shown)" % (step, len(x[::step])))

print("A 7-inch figure at 100 dpi is 700 pixels wide.")
print("200,000 points is roughly 285 per pixel column - 284 of which")
print("are drawn on top of each other and cannot be distinguished.")
print()
print("Subsampling changes the file size and the draw time, and the")
print("chart looks the same. It does hide genuine spikes, so for")
print("min/max envelopes, aggregate rather than sample.")'''),

        ("Aggregate rather than sample",
         "Binning preserves the extremes that sampling drops.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(3)
n = 100_000
x = np.linspace(0, 100, n)
y = np.sin(x / 5) + rng.normal(0, 0.2, n)
# 50_001, not 50_000: the step below divides 50_000 exactly, so a
# spike there would survive sampling and the demo would show nothing.
y[50_001] = 6.0

bins = 800
idx = np.arange(n) // (n // bins)
xb = np.array([x[idx == i].mean() for i in range(bins)])
lo = np.array([y[idx == i].min() for i in range(bins)])
hi = np.array([y[idx == i].max() for i in range(bins)])

fig, (a, b) = plt.subplots(2, 1, figsize=(7.5, 4), sharey=True)

step = n // bins
a.plot(x[::step], y[::step], linewidth=0.7)
a.set_title("subsampled - the spike is gone")

b.fill_between(xb, lo, hi, alpha=0.5, linewidth=0)
b.set_title("min/max per bin - the spike survives")

print("There is one real spike of 6.0 at the midpoint.")
print("subsampled maximum: %.2f" % y[::step].max())
print("binned maximum    : %.2f" % hi.max())
print()
print("Sampling drops whatever it does not land on. Binning keeps the")
print("envelope, which is what a reader of a dense series looks at.")'''),

        ("Rasterising a layer",
         "Keeps a vector file small while leaving the text sharp.",
         '''import matplotlib.pyplot as plt
import numpy as np
import io

rng = np.random.default_rng(4)
n = 30_000
x, y = rng.random(n), rng.random(n)

sizes = {}
for raster in (False, True):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.scatter(x, y, s=2, alpha=0.3, rasterized=raster)
    ax.set_title("rasterized=%s" % raster)
    buf = io.BytesIO()
    fig.savefig(buf, format="pdf", dpi=150)
    sizes[raster] = len(buf.getvalue())
    if not raster:
        plt.close(fig)

print("PDF, %d points" % n)
print("   vector      : %8d bytes" % sizes[False])
print("   rasterized  : %8d bytes" % sizes[True])
print("   ratio       : %.0fx smaller" % (sizes[False] / sizes[True]))
print()
print("rasterized=True stores that ARTIST as pixels while axes, ticks")
print("and text stay vector - so the labels are still sharp and the")
print("file opens instantly.")'''),

        ("Loops that draw",
         "The cost is per figure, and the fix is to reuse or close.",
         '''import matplotlib.pyplot as plt
import numpy as np
import time, io

rng = np.random.default_rng(5)

t = time.perf_counter()
for i in range(20):
    fig, ax = plt.subplots(figsize=(3, 1.6))
    ax.plot(rng.random(50))
    buf = io.BytesIO(); fig.savefig(buf, format="png")
    plt.close(fig)
fresh = time.perf_counter() - t

t = time.perf_counter()
fig, ax = plt.subplots(figsize=(3, 1.6))
line, = ax.plot(rng.random(50))
for i in range(20):
    line.set_ydata(rng.random(50))
    ax.relim(); ax.autoscale_view()
    buf = io.BytesIO(); fig.savefig(buf, format="png")
reuse = time.perf_counter() - t
plt.close(fig)

print("new figure each time : %.3f s" % fresh)
print("reuse and set_ydata  : %.3f s" % reuse)
print("ratio                : %.1fx" % (fresh / max(reuse, 1e-9)))
print()
print("Creating a figure is the expensive part. When the layout does")
print("not change, update the artist's data and re-save.")

fig, ax = plt.subplots(figsize=(4, 2))
ax.bar(["fresh", "reuse"], [fresh, reuse])
ax.set_title("seconds for 20 charts")'''),
    ],
    [
        "Cost grows with the number of <strong>artists</strong>, not data points &mdash; one call with arrays beats a loop of calls by a wide margin.",
        "<code>plot</code> with a marker is faster than <code>scatter</code> when size and colour do not vary.",
        "Past a few thousand points there are <strong>more points than pixels</strong>, and the extras cannot be seen at all.",
        "<strong>Subsampling</strong> drops genuine spikes; binning to a min/max envelope keeps them.",
        "<code>rasterized=True</code> stores one artist as pixels while text and axes stay vector &mdash; a much smaller PDF with sharp labels.",
        "Creating a figure is the expensive part of a drawing loop; <strong>reuse</strong> it with <code>set_ydata</code>, or at least <code>close</code> it.",
    ],
    '''
title: Performance and Large Data
intro: What makes a figure slow, and what to do when there are more points than pixels.

## Artists, not data

matplotlib's cost is dominated by the number of **artists** it manages, not the number of data values.

One `plot` call with a million points creates one `Line2D`. A loop making two thousand calls creates two thousand artists, each with its own properties, transform and draw pass &mdash; and that is far slower even with a fraction of the data.

The rule that follows is the same one as NumPy and pandas: **pass arrays, do not loop**. Where a loop is unavoidable, `LineCollection` and its relatives draw many segments as a single artist.

## plot versus scatter

For many points that all look alike, `ax.plot(x, y, "o")` is faster than `ax.scatter(x, y)`.

`scatter` builds a collection that carries a size and colour per point, because that is what it is for. When those do not vary, the machinery is unused and paid for anyway.

So: `scatter` when size or colour encodes something, `plot` when it does not.

## More points than pixels

A seven-inch figure at 100 dpi is 700 pixels wide. Two hundred thousand points is roughly 285 per pixel column, and 284 of them are drawn exactly on top of others.

They cost time and file size and contribute nothing visible.

Reducing them is not a compromise; it is removing something the reader could never see. Two approaches, and the difference matters.

**Subsampling** &mdash; `x[::step]` &mdash; is trivial and drops whatever it does not land on. A single-sample spike disappears. For smooth, dense data that is fine; for anything where extremes matter it is not.

**Aggregating** &mdash; binning by x and drawing the min and max in each bin as a filled band &mdash; keeps the envelope. The chart looks nearly identical to the full data because the envelope is what the eye was reading anyway, and genuine spikes survive.

The fourth editor puts one real spike in the data and shows subsampling losing it while binning keeps it.

For scatter data, the equivalent is `hexbin` or `hist2d`, which replaces overplotted points with measured density.

## File size

Vector formats store every element, so a scatter of 30,000 points is 30,000 objects in the PDF. Such files are slow to open and large.

`rasterized=True` on the artist stores **that layer** as pixels while everything else &mdash; axes, ticks, labels, title &mdash; stays vector:

```python
ax.scatter(x, y, s=2, rasterized=True)
fig.savefig("out.pdf", dpi=200)
```

The result is a small file with sharp text and a pixel-based data layer, which is exactly the right trade for a dense scatter in a document. The `dpi` at save time controls the resolution of the rasterised part.

## Drawing loops

Generating many similar charts &mdash; one per group, per day, per file &mdash; spends most of its time creating figures, not drawing data.

Two levels of fix.

**Close each figure**: `plt.close(fig)`. This is not an optimisation so much as a requirement; without it the figures accumulate, matplotlib warns after twenty, and memory grows without bound.

**Reuse the figure**: create it once, update the artist's data each iteration, and re-save:

```python
line.set_ydata(new_y)
ax.relim(); ax.autoscale_view()
fig.savefig(path)
```

`relim` and `autoscale_view` are needed because setting data does not rescale the axes.

This is meaningfully faster when the layout is identical between charts, and it is the same mechanism animations use.

## When matplotlib is the wrong tool

matplotlib renders once and is not built for interactive exploration of large data.

**Datashader** aggregates hundreds of millions of points into an image, and is the right answer above a few million.

**Plotly, Bokeh, Altair** give pan-and-zoom in a browser, which matplotlib's interactive backends do only awkwardly.

**mpl-scatter-density** and similar handle the dense-scatter case within matplotlib.

The signal is usually the size: if a figure takes more than a few seconds to draw, the answer is a different approach rather than a faster matplotlib.

## Measuring draw time

Timing a matplotlib figure needs care, because the drawing is lazy: creating artists is fast and nothing is rendered until the canvas is drawn.

```python
t = time.perf_counter()
fig.canvas.draw()
elapsed = time.perf_counter() - t
```

Without the explicit `draw()`, the timing measures only object creation and reports numbers far too good.

The first draw of a session also pays for font cache and backend initialisation, which can be a second or more. A warm-up figure before timing anything is the difference between a meaningful comparison and a misleading one &mdash; the editors in this module do exactly that.

## Where the time goes

For a typical figure, in rough order:

**Artist creation** when there are many artists.

**Rendering** the artists to pixels.

**Text layout**, which is more expensive than it sounds &mdash; a chart with hundreds of tick labels or annotations spends real time measuring glyphs.

**Font cache building**, once per environment, and occasionally minutes on first run.

**Saving**, particularly to vector formats with many elements.

The practical consequences: fewer artists, fewer text objects, and rasterised layers for dense data.

## Interactive versus file output

An interactive backend redraws on every pan, zoom and resize, so a figure that takes two seconds to draw is unusable interactively while being perfectly fine as a file.

That changes the trade-off. For a saved figure, drawing a million points slowly once is acceptable. For something a person will manipulate, the point budget is far smaller, and downsampling is not an optimisation but a requirement.

`fig.canvas.draw_idle()` defers a redraw until the event loop is free, which is what interactive tools use to stay responsive.

## Animations

`FuncAnimation` re-renders a figure per frame, so the per-frame cost is what matters.

`blit=True` redraws only the artists that changed, which is much faster and requires the update function to return them.

The same reuse principle as the drawing loop applies: create the artists once, update their data each frame with `set_data`, and never call `plot` inside the update.

## The wider picture

matplotlib is designed for correctness and control rather than throughput, and its limits are reached sooner than people expect &mdash; tens of thousands of artists, or a few million points.

The escape routes, roughly by problem:

**Too many points** &mdash; aggregate, or use datashader.

**Too many artists** &mdash; collections instead of loops.

**Too slow interactively** &mdash; a browser-based library.

**Too many figures** &mdash; reuse, and close.

The one that matters most is the first. Most performance problems in matplotlib are really a display problem: drawing more than the reader can see, which costs time and communicates nothing.

## Font cache and first-run cost

A surprise on a fresh environment: the very first matplotlib figure can take a long time, occasionally minutes, while the font cache is built.

It happens once per environment and is cached afterwards, and it is a common source of "matplotlib is incredibly slow" reports from people who ran it once in a new container.

In a container or CI image, drawing one throwaway figure at build time moves the cost out of the first real run.

`matplotlib.get_cachedir()` shows where it lives, and deleting it forces a rebuild &mdash; which is the fix when a newly installed font is not being found.

## A performance checklist

When a figure is slow, in the order worth checking:

**How many artists?** `len(ax.lines) + len(ax.collections) + len(ax.patches)`. Hundreds is fine; tens of thousands is the problem.

**How many points, against how many pixels?** If it is more than a few per pixel column, the extras are invisible.

**Is it in a loop?** Are figures being closed?

**Is it text?** Hundreds of annotations or tick labels cost real time.

**Is it the save?** Vector output of dense data.

**Is it the first run?** The font cache.

Most slow figures are the first two, and both are fixed by drawing less rather than by drawing faster.

## Budgets

Rough numbers, which are more useful than general advice.

**Artists**: up to a few thousand is comfortable. Tens of thousands is slow. Hundreds of thousands will not finish in a reasonable time.

**Points in one artist**: a million is fine for a line, because it is one object. The renderer handles it far better than a million separate objects.

**Visible resolution**: a 7-inch figure at 100 dpi has 700 columns. Above a few thousand points, most are invisible.

**Text objects**: hundreds are noticeable; thousands dominate.

**Interactive redraw**: anything above about 100 ms per draw feels sluggish when panning.

**Vector output**: above roughly 10,000 elements the file becomes slow to open.

Those thresholds explain most of the practical advice: pass arrays rather than looping, aggregate before plotting, rasterise dense layers, and reuse figures in loops.

## In summary

Cost is driven by artists, not data points, so one call with an array beats a loop of calls by a wide margin.

`plot` beats `scatter` when the markers are uniform.

Past a few thousand points there are more points than pixels, and the extras cost time while communicating nothing.

Subsampling drops genuine extremes; binning to a min/max envelope keeps them, and looks the same.

`rasterized=True` keeps a vector file small while leaving the text sharp.

Creating figures is the expensive part of a drawing loop, so reuse them &mdash; and close them regardless, because matplotlib will not.

And when a figure takes seconds to draw, the answer is usually a different approach rather than a faster matplotlib.

## When to stop optimising

A figure that takes two seconds to draw once, and is then saved, is fine. There is nothing to fix.

The cases that justify effort are narrower than they look:

**A figure regenerated frequently** &mdash; in a dashboard build, a CI job, a loop over thousands of groups. The cost multiplies.

**An interactive figure**, where every pan and zoom pays it again.

**A figure that does not finish**, or exhausts memory, which is a correctness problem rather than a speed one.

**A file too large to open**, which is the vector-scatter case.

Outside those, drawing time is usually a rounding error next to the data work that preceded it, and the effort is better spent on whether the chart says the right thing.

That is worth stating because performance is easy to optimise and easy to over-optimise, and a fast chart nobody can read is not an improvement.

## One more thing

`fig.canvas.draw_idle()` requests a redraw at the next opportunity rather than immediately, which is what keeps an interactive figure responsive when several things change at once.

For a script it makes no difference, since the draw happens at save time either way. It matters in a callback that updates several artists, where an immediate draw per change would render the figure several times for one logical update.

## The short version

Nearly every performance problem in matplotlib is a display problem in disguise: drawing more than the output can show.

Fixing it by drawing less &mdash; aggregating, subsampling with care, rasterising a dense layer &mdash; makes the chart faster and usually more readable at the same time, which is unusual among optimisations.

## Reading the code back

Performance work here is a short list checked in order: is there a loop creating artists, are there more points than pixels, are figures being closed, is the output vector with a dense layer in it. Four questions, and the first two account for nearly everything. None of them requires knowing anything about how matplotlib renders.
''',
    [
        {"q": "What dominates matplotlib's drawing cost?",
         "options": ["The number of data points", "The number of artists", "The figure size", "The colormap"],
         "answer": 1,
         "why": "One plot call with a million points makes one Line2D; two thousand calls make two thousand artists, each drawn separately."},
        {"q": "When is `plot(x, y, 'o')` faster than `scatter`?",
         "options": ["Never", "When size and colour do not vary per point", "For fewer than 100 points", "On log axes"],
         "answer": 1,
         "why": "scatter carries per-point size and colour machinery that is paid for even when unused."},
        {"q": "Why is subsampling risky for a dense series?",
         "options": ["It is slow", "It drops whatever it does not land on, including genuine single-sample spikes", "It changes the colours", "It breaks the axis"],
         "answer": 1,
         "why": "Binning to a min/max envelope keeps the extremes, and the chart looks nearly the same because the envelope is what the eye reads."},
        {"q": "What does `rasterized=True` do to a PDF?",
         "options": ["Rasterises the whole figure", "Stores that artist as pixels while axes and text stay vector", "Compresses the file", "Lowers the dpi"],
         "answer": 1,
         "why": "The right trade for a dense scatter in a document - small file, sharp labels, pixel-based data layer."},
    ],
)


# ---------------------------------------------------------------------------
# 21. Layout and spacing
# ---------------------------------------------------------------------------
topic(
    "layout_and_spacing",
    "Layout and Spacing",
    "Layout",
    "Figure size, margins and the space between panels - the part that decides "
    "whether a chart looks finished.",
    _svg(_box(10, 12, 140, 66, "none", B) +
         _box(24, 26, 48, 24, S, A) + _box(84, 26, 48, 24, S, A) +
         _box(24, 56, 48, 14, S, A) + _box(84, 56, 48, 14, S, A) +
         _txt(78, 88, "margins", M, 7)),
    [
        ("figsize is the aspect ratio decision",
         "A wide figure spreads time; a square one compares two variables.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(0)
t = np.arange(150)
y = rng.normal(0, 1, 150).cumsum()

fig, ax = plt.subplots(figsize=(3.5, 3))
ax.plot(t, y)
ax.set_title("square: crowded")

fig2, ax2 = plt.subplots(figsize=(9, 2.6))
ax2.plot(t, y)
ax2.set_title("wide: the shape is readable")

print("150 points in 3.5 inches is 43 per inch; in 9 inches it is 17.")
print()
print("Time series want width. A scatter comparing two variables wants")
print("to be square, so neither axis is visually privileged.")
print("A ranked bar chart wants height proportional to the number of")
print("bars, not a fixed size.")'''),

        ("Margins around the data",
         "The padding matplotlib adds, and when to remove it.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y = np.sin(x)

fig, (a, b, c) = plt.subplots(1, 3, figsize=(10, 2.6))

a.plot(x, y); a.set_title("default margins")
b.plot(x, y); b.margins(0); b.set_title("margins(0)")
c.plot(x, y); c.margins(x=0, y=0.3); c.set_title("margins(x=0, y=0.3)")

print("default x margin:", plt.rcParams["axes.xmargin"])
print("default y margin:", plt.rcParams["axes.ymargin"])
print()
print("5% each side. It stops points sitting on the frame, and it")
print("means a line that should reach the edge - a filled area, a")
print("time series ending today - stops short of it.")
print()
print("margins(x=0) is the usual fix for a time series.")'''),

        ("Space between panels",
         "<code>hspace</code> and <code>wspace</code>, in units of the panel size.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1)

for hs, ws, title in [(0.05, 0.05, "cramped"), (0.5, 0.4, "roomy")]:
    fig, axes = plt.subplots(2, 2, figsize=(6, 3.4))
    for ax in axes.flat:
        ax.plot(rng.random(20))
        ax.set_xlabel("x"); ax.set_ylabel("y")
    fig.subplots_adjust(hspace=hs, wspace=ws)
    fig.suptitle(title)

print("hspace and wspace are fractions of the average panel size, so")
print("0.4 means 40% of a panel's height as a gap.")
print()
print("They are what tight_layout and constrained_layout set for you.")
print("Setting them by hand is for when you want a specific look, or")
print("when automatic layout fights an annotation you placed.")'''),

        ("Making room for something outside",
         "A legend or a colorbar beside the axes needs space reserved.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 60)

fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3))

for k in range(3):
    a.plot(x, np.sin(x + k), label="series %d" % k)
a.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
a.set_title("legend outside, no room made")

for k in range(3):
    b.plot(x, np.sin(x + k), label="series %d" % k)
b.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
b.set_title("room made")
fig.subplots_adjust(right=0.78)

print("A legend placed outside the axes is drawn outside the FIGURE")
print("too, unless room is made for it.")
print()
print("Three ways: subplots_adjust(right=...), constrained_layout=True,")
print("or bbox_inches='tight' when saving - which expands the file")
print("rather than shrinking the axes.")'''),

        ("Aspect ratio of the data",
         "When one unit of x must equal one unit of y.",
         '''import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0, 2 * np.pi, 200)

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.plot(np.cos(theta), np.sin(theta))
a.set_title("a circle, drawn as an ellipse")

b.plot(np.cos(theta), np.sin(theta))
b.set_aspect("equal")
b.set_title('set_aspect("equal")')

print("The same unit circle. The left one is an ellipse because the")
print("axes box is wider than it is tall and the limits are the same.")
print()
print("set_aspect('equal') ties the two scales together, which matters")
print("for maps, geometry, and anything where a shape means something.")
print("It is wrong for most other charts - it wastes space.")'''),

        ("A finished figure",
         "Every layout decision in one place.",
         '''import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(2)
months = np.arange(1, 13)
series = {"north": rng.normal(0, 1, 12).cumsum() + 20,
          "south": rng.normal(0, 1, 12).cumsum() + 24}

fig, ax = plt.subplots(figsize=(7.5, 3.6), constrained_layout=True)

for name, y in series.items():
    ax.plot(months, y, marker="o", linewidth=2, label=name)
    ax.text(months[-1] + 0.15, y[-1], name, va="center", fontsize=9)

ax.set_xlim(0.6, 13.2)
ax.margins(y=0.15)
ax.set_title("Both regions grew, north faster after June",
             loc="left", fontsize=12, fontweight="bold")
ax.set_xlabel("Month of 2024")
ax.set_ylabel("Index (Jan = 20)")
ax.set_xticks(months)
ax.grid(True, axis="y", alpha=0.3)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)

print("figsize for the aspect, xlim to leave room for the end labels,")
print("margins for breathing space, constrained_layout for the rest.")
print("No legend, because the lines are labelled where they end.")'''),
    ],
    [
        "<code>figsize</code> is an aspect-ratio decision: time series want <strong>width</strong>, two-variable scatters want to be <strong>square</strong>.",
        "matplotlib adds a <strong>5% margin</strong> each side; <code>margins(x=0)</code> is the usual fix for a time series that should reach the edge.",
        "<code>hspace</code>/<code>wspace</code> are fractions of the <strong>panel size</strong>, and are what the automatic layout managers set for you.",
        "A legend placed outside the axes is drawn outside the <strong>figure</strong> too unless room is made with <code>subplots_adjust</code> or <code>constrained_layout</code>.",
        "<code>set_aspect(\"equal\")</code> ties the two scales so a circle is round &mdash; needed for maps and geometry, wasteful elsewhere.",
        "A finished figure is a handful of deliberate choices: size, limits, margins, ticks, grid, spines, and labels where the reader is looking.",
    ],
    '''
title: Layout and Spacing
intro: Figure size, margins and the space between panels.

## figsize is an aspect decision

`figsize=(w, h)` in inches does two things: it sets how large the figure is, and it sets the **shape**.

The shape matters more than the size, because the size is usually adjusted at display time anyway.

**Time series want width.** A hundred and fifty points in three inches is 50 per inch, and the shape of the series is compressed into noise. The same data in nine inches is readable. Wide-and-short &mdash; something like 4:1 &mdash; is a good default for a single time series.

**Two-variable scatters want to be square**, so neither axis is visually privileged and a correlation is not exaggerated by the aspect ratio.

**Ranked bar charts want height proportional to the number of bars.** Twenty categories in three inches gives bars a few pixels apart; the figure should grow with the data.

`figsize` interacts with font size: text is a fixed physical size, so a small figure has proportionally larger text. That is why shrinking a figure to fit a slide makes the labels look enormous, and why the fix is to set both together.

## Margins

matplotlib leaves a 5% margin beyond the data at each end, controlled by `axes.xmargin` and `axes.ymargin`.

It exists so points do not sit exactly on the frame, and it is usually right.

It is wrong when the data should reach the edge: a filled area, a time series ending at today's date, an image. `ax.margins(x=0)` removes it on one axis, and `ax.margins(0)` on both.

`ax.margins(y=0.15)` increases it, which is how you leave room for labels above the highest point without hard-coding limits that break when the data changes.

## Space between panels

`fig.subplots_adjust(hspace=..., wspace=...)` sets the gaps as **fractions of the average panel size**, so `0.4` means a gap of 40% of a panel's height.

It also takes `left`, `right`, `top` and `bottom` as figure fractions, which is how you reserve space at an edge.

These are what `tight_layout` and `constrained_layout` compute for you. Setting them by hand is for when you want a specific look, or when the automatic layout is fighting something you placed manually.

The two automatic options differ: `tight_layout()` runs once after drawing; `constrained_layout=True` is set at creation and keeps adjusting as artists are added, handling colorbars and suptitles better.

## Things outside the axes

A legend positioned with `bbox_to_anchor` outside the axes is drawn outside the **figure** as well, and is simply cut off.

Three fixes:

`fig.subplots_adjust(right=0.78)` shrinks the axes to leave room. Predictable, and you choose the number.

`constrained_layout=True` works it out, including for colorbars.

`bbox_inches="tight"` at save time expands the saved image to include everything. Note this makes the file larger than `figsize` implies, rather than shrinking the axes &mdash; a different result from the other two.

The same applies to long tick labels and axis labels, which is why a rotated date axis so often looks cut off.

## Data aspect ratio

`ax.set_aspect("equal")` makes one unit of x occupy the same distance as one unit of y.

Without it, a circle plotted as `cos`/`sin` comes out an ellipse, because the axes box is wider than it is tall while the limits are the same.

It is required for anything where shape carries meaning: maps, geometry, images, physical layouts. It is wrong for most statistical charts, where the two axes have unrelated units and forcing them equal wastes space.

`ax.set_aspect(2)` sets a specific ratio, and `adjustable="datalim"` changes the limits rather than the box to achieve it.

## Putting it together

The last editor is a finished chart, and every line in it is one of the decisions from this track: an aspect ratio suited to the data, limits that leave room for end labels, margins for breathing space, ticks at meaningful positions, a faint grid below the data, two spines removed, direct labels instead of a legend, and a title that states the finding.

None of it is complicated. It is a dozen lines, applied deliberately, and it is the difference between a default chart and one that looks like someone made it.

## Figure versus axes coordinates

Two coordinate systems place things on a figure, and mixing them up is a common source of misplaced elements.

**Figure coordinates** run 0 to 1 across the whole figure. `fig.text`, `fig.add_axes`, `fig.legend` use them.

**Axes coordinates** run 0 to 1 across one axes. `ax.text(..., transform=ax.transAxes)` uses them.

A note that belongs to the whole figure &mdash; a source line, a caption &mdash; goes in figure coordinates and stays put when panels change. A note about one panel goes in that panel's axes coordinates.

`fig.subplots_adjust` also takes figure coordinates for `left`, `right`, `top` and `bottom`, which is how you reserve a strip at an edge.

## Adding an axes anywhere

`fig.add_axes([left, bottom, width, height])` places an axes at an exact position in figure coordinates, outside the grid entirely.

Two uses come up: an inset showing a zoomed region, and a colorbar positioned precisely rather than stolen from a panel.

`ax.inset_axes([x, y, w, h])` does the same in the parent's coordinates, which is easier for an inset because the position is relative to the panel it belongs to.

`ax.indicate_inset_zoom(inset_ax)` draws the connecting lines between the region and the inset, which is what makes the relationship readable.

## Spacing that reads

A few conventions produce figures that look considered rather than default.

Leave more space **between** groups than within them &mdash; a grid of panels with a `wspace` smaller than the margin around the grid reads as a unit.

Keep the **left margin** wide enough for the y label at its final font size, which is what `constrained_layout` does and hand-tuning frequently gets wrong when the font changes.

Give a **suptitle** room, or it collides with the top row's titles. `fig.suptitle(..., y=1.02)` with `tight_layout` is a common fix and is fragile; `constrained_layout` handles it properly.

Do not centre a title over a grid that has a colorbar on one side, because the visual centre and the geometric centre differ.

## Sizing for a destination

The figure should be sized for where it will be seen.

**A slide** is wide and viewed from a distance: fewer elements, larger text, `figsize` around 10&times;5.6 for 16:9.

**A document column** is narrow: around 3.5 inches wide for a two-column paper, and text sized so that the figure needs no scaling &mdash; scaling a figure in a document is what makes its labels the wrong size relative to the body text.

**A web page** is variable, so a raster at 2&times; the display size and a `max-width` in CSS is the usual approach.

The mistake is drawing at a default size and scaling afterwards, which changes the text size relative to everything else. Sizing at the destination's dimensions and choosing the font accordingly is the fix.

## The last pass

Before a figure is finished, three checks that are all layout:

Is anything cut off at the edges? Save it and look at the file, not the screen.

Is the text a sensible size relative to the figure at its final display size?

Is there enough space that nothing touches anything else &mdash; labels to spines, title to panels, legend to data?

None of these change what the chart says, and all of them change whether it looks like someone finished it.

## Insets

An inset shows a zoomed region or a small companion chart inside the main axes.

```python
inset = ax.inset_axes([0.6, 0.55, 0.35, 0.35])
inset.plot(x, y)
inset.set_xlim(a, b)
ax.indicate_inset_zoom(inset, edgecolor="0.5")
```

The position is in the parent's axes coordinates, so it moves with the panel.

`indicate_inset_zoom` draws the rectangle on the main axes and the connecting lines, which is what makes the relationship legible &mdash; an inset without it is a floating chart the reader has to interpret.

Insets suit a long series with an interesting short window, and a scatter with a dense cluster worth magnifying. They do not suit anything the reader needs to compare precisely with the main axes, because the scales differ.

## Layout that survives regeneration

Hand-tuned spacing breaks when the data changes: a longer label, an extra category, a bigger number needing more room.

Three habits keep a layout robust.

**Prefer `constrained_layout`** over hand-set `subplots_adjust`, because it recomputes rather than remembering.

**Size the figure from the data** &mdash; `figsize=(7, 0.35 * len(categories) + 1)` for a horizontal bar chart grows with the number of bars.

**Use `bbox_inches="tight"` when saving**, so anything that grew is still included.

A figure generated weekly will meet all three problems eventually, and the alternative is adjusting the numbers each time something changes.

## Text size and the destination

The most common layout error is a figure drawn at one size and displayed at another.

Text in matplotlib is specified in **points**, a physical unit. A 10-point label on a 4-inch figure is a quarter of an inch, which is a substantial fraction of the width. The same label on a 10-inch figure is the same quarter inch, and now looks small.

So scaling a figure after the fact changes the relationship between the text and everything else &mdash; which is why a chart shrunk to fit a document column has labels that are suddenly too large, and one enlarged for a slide has labels that are too small.

The fix is to draw at the final size. For a two-column paper, that means a figure about 3.4 inches wide with fonts chosen to be readable at that size. For a slide, something like 10 by 5.6 with fonts around 14 points.

`figsize` and `font.size` are one decision, not two.

## In summary

`figsize` is an aspect-ratio decision: width for time series, square for scatters, height proportional to the number of bars.

Margins default to 5% each side and should be removed when the data is meant to reach the edge.

`hspace`/`wspace` are fractions of panel size, and are what the layout managers compute for you.

Anything outside the axes &mdash; a legend, long labels &mdash; needs room reserved, or it is cut off in the saved file.

`set_aspect("equal")` is required where shape carries meaning and wasteful elsewhere.

And a figure should be drawn at the size it will be displayed, because text is a physical size and scaling afterwards changes everything about the balance.

## A closing note

Layout is the part of charting that gets the least attention and is most visible in the result.

A chart with the right data, the right type and the wrong spacing looks unfinished, and readers register that before they read anything. Labels touching the frame, a title colliding with a panel, a legend crowding the data, text at the wrong size for the display &mdash; all are cheap to fix and all cost credibility.

The mechanisms are few: pick a figure size for the destination, let `constrained_layout` handle the spacing, reserve room for anything outside the axes, and check the saved file rather than the screen.

Doing that consistently is most of the difference between charts that look produced and charts that look exported.

## The short version

Layout gets the least attention and is the most visible in the result.

Size for the destination, let a layout manager handle the spacing, reserve room for anything outside the axes, and look at the saved file. That is most of the difference between charts that look produced and charts that look exported.
''',
    [
        {"q": "What shape suits a single time series?",
         "options": ["Square", "Wide and short", "Tall and narrow", "It does not matter"],
         "answer": 1,
         "why": "Compressing 150 points into three inches turns the shape into noise. Two-variable scatters want to be square instead."},
        {"q": "Why does a filled area chart often need `ax.margins(x=0)`?",
         "options": ["To fix the colours", "matplotlib's default 5% margin stops the fill reaching the edge of the axes", "To share axes", "For the legend"],
         "answer": 1,
         "why": "The margin exists so points do not sit on the frame, which is usually right and wrong for anything meant to reach the edge."},
        {"q": "What happens to a legend placed outside the axes with no other change?",
         "options": ["It moves inside", "It is drawn outside the figure and cut off", "It shrinks", "It raises"],
         "answer": 1,
         "why": "Fix with subplots_adjust, constrained_layout, or bbox_inches='tight' at save time - which expands the file rather than shrinking the axes."},
        {"q": "When do you need `set_aspect('equal')`?",
         "options": ["Always", "When shape carries meaning - maps, geometry, images", "For time series", "For bar charts"],
         "answer": 1,
         "why": "Without it a circle comes out an ellipse. For statistical charts with unrelated units it just wastes space."},
    ],
)


# ---------------------------------------------------------------------------
# 22. Common mistakes
# ---------------------------------------------------------------------------
topic(
    "common_mistakes",
    "Common Mistakes",
    "Design",
    "The errors that produce a chart which looks fine and is not.",
    _svg(_box(14, 16, 132, 58, "none", B) +
         _txt(80, 40, "looks fine", "#e88", 10) +
         _txt(80, 58, "is not", "#e88", 10)),
    [
        ("Nothing appears",
         "Three causes, and how to tell which one you have.",
         '''import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(10, 2.6))

axes[0].plot([], [])
axes[0].set_title("empty data")

x = np.array([1, 2, 3])
y = np.array([np.nan, np.nan, np.nan])
axes[1].plot(x, y, marker="o")
axes[1].set_title("all NaN")

axes[2].plot([1, 2, 3], [1, 2, 3])
axes[2].set_xlim(100, 200)
axes[2].set_title("limits exclude the data")

print("To diagnose an empty plot:")
print("   len(x), len(y)        - is there data at all?")
print("   np.isnan(y).all()     - is it all missing?")
print("   ax.get_xlim()         - is the view somewhere else?")
print("   len(ax.lines)         - did the draw call even happen?")
print()
print("lines on each axes:", [len(a.lines) for a in axes])
print("   all three DREW something; only the data or the view is wrong.")'''),

        ("The plot goes to the wrong axes",
         "Because plt.* uses the current figure, whatever that now is.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 5, 30)

fig, (a, b) = plt.subplots(1, 2, figsize=(8, 2.6))
a.set_title("meant for here")
b.set_title("landed here")

plt.plot(x, np.sin(x))          # goes to the CURRENT axes, which is b

print("lines on the left  :", len(a.lines))
print("lines on the right :", len(b.lines), "<- plt.plot landed here")
print()
print("subplots() makes each axes current in turn, so the last one")
print("created wins. Use a.plot(...) and the question never arises.")'''),

        ("Overlapping labels in a saved file",
         "It looked fine on screen because the screen was a different size.",
         '''import matplotlib.pyplot as plt
import numpy as np
import io

rng = np.random.default_rng(0)
names = ["category number %d" % i for i in range(8)]
vals = rng.integers(5, 40, 8)

fig, ax = plt.subplots(figsize=(4, 2.5))
ax.bar(names, vals)
ax.tick_params(axis="x", rotation=90, labelsize=8)
ax.set_title("cramped")

fig2, ax2 = plt.subplots(figsize=(5, 3.5))
ax2.barh(names, vals)
ax2.set_title("barh, no rotation needed")
fig2.tight_layout()

print("A figure is saved at its declared size, not the size of the")
print("window you were looking at, so a layout that fits on screen")
print("can be cut off in the file.")
print()
print("Fixes: tight_layout, bbox_inches='tight', a bigger figsize, or")
print("a chart type that does not need rotated labels.")'''),

        ("Colours that do not survive",
         "Greyscale is the quickest test of whether the encoding works.",
         '''import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 60)

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

for c, lbl in [("red", "A"), ("green", "B"), ("#8b0000", "C")]:
    a.plot(x, np.sin(x) + hash(lbl) % 3 * 0.4, color=c, label=lbl)
a.legend(); a.set_title("three similar luminances")

styles = [("-", "o"), ("--", "s"), (":", "^")]
for (ls, mk), lbl in zip(styles, "ABC"):
    b.plot(x, np.sin(x) + ord(lbl) % 3 * 0.4, linestyle=ls, marker=mk,
           markevery=10, color="0.25", label=lbl)
b.legend(); b.set_title("style and marker, one colour")

print("Red, green and dark red have similar brightness, so in")
print("greyscale - or to a red-green colour-blind reader - the left")
print("chart has three identical lines.")
print()
print("Varying linestyle and marker means the right chart works with")
print("no colour at all.")'''),

        ("Silent truncation and missing categories",
         "The chart draws happily with part of the data missing.",
         '''import matplotlib.pyplot as plt
import numpy as np

values = np.array([12, 45, 8, 200, 15, 22])
names = list("abcdef")

fig, (a, b) = plt.subplots(1, 2, figsize=(9, 3))

a.bar(names, values)
a.set_ylim(0, 50)
a.set_title("ylim hides d entirely")

b.bar(names, values)
b.set_title("all six visible")

print("Category d is 200. With ylim(0, 50) its bar runs off the top")
print("and looks identical to any other tall bar - the reader has no")
print("way to know it is four times the next largest.")
print()
print("matplotlib does not warn, because clipping is a legitimate")
print("thing to ask for. Check that max(data) is inside get_ylim().")
print()
print("data max: %d   ylim: %s" % (values.max(), a.get_ylim()))'''),

        ("Figures left open",
         "The warning that appears after twenty, and what it means.",
         '''import matplotlib.pyplot as plt
import warnings

plt.close("all")

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    for i in range(22):
        fig, ax = plt.subplots(figsize=(1, 1))
    names = [str(w.category.__name__) for w in caught]

print("figures open:", len(plt.get_fignums()))
print("warnings raised:", names[:1] or "none")
print()
if caught:
    print("message:", str(caught[0].message)[:96])
print()
plt.close("all")
print("after close('all'):", len(plt.get_fignums()))
print()
print("The limit is rcParams['figure.max_open_warning'] and it is a")
print("warning, not an error - a loop will keep going and keep using")
print("memory until something else breaks.")

fig, ax = plt.subplots(figsize=(4, 2))
ax.plot([0, 1], [0, 1])
ax.set_title("one deliberate figure")'''),
    ],
    [
        "An <strong>empty plot</strong> is empty data, all-NaN data, or limits pointing elsewhere &mdash; <code>len(ax.lines)</code> tells you whether the draw happened.",
        "<code>plt.plot</code> lands on the <strong>current</strong> axes, which after <code>subplots()</code> is the last one created. Use <code>ax.plot</code>.",
        "A figure saves at its <strong>declared size</strong>, not the window's, so a layout that fits on screen can be cropped in the file.",
        "Colours of similar <strong>luminance</strong> become identical in greyscale; varying linestyle and marker makes a chart work without colour.",
        "Setting limits that exclude data <strong>clips it silently</strong> &mdash; check <code>max(data)</code> against <code>get_ylim()</code>.",
        "Figures left open warn after twenty and keep consuming memory; <code>plt.close(fig)</code> in any drawing loop.",
    ],
    '''
title: Common Mistakes
intro: The errors that produce a chart which looks fine and is not.

## Nothing appears

Three causes, distinguishable in a few seconds.

**No data.** `len(x)` and `len(y)`. An empty array plots without complaint.

**All missing.** `np.isnan(y).all()`. NaN is skipped, so an all-NaN series draws an empty line object.

**The view is elsewhere.** `ax.get_xlim()` and `get_ylim()`. Limits set before the data was added, or set to the wrong range, put the data outside the visible box.

`len(ax.lines)` distinguishes "the draw call never ran" from "it ran and there is nothing to see", which is usually the fastest thing to check.

A fourth possibility in a script: you never showed or saved the figure. In a notebook figures display automatically; in a script they do not, and `plt.show()` or `savefig` is required.

## The plot lands somewhere else

`plt.plot` draws on the **current** axes. After `plt.subplots(1, 2)`, the current axes is the last one created, so a stray `plt.plot` goes to the right-hand panel regardless of intent.

In a notebook it is worse, because the current figure is whatever the last executed cell created &mdash; which, with out-of-order execution, is not necessarily the one above.

`ax.plot(...)` removes the question. This is the practical reason the object-oriented API is worth the extra characters.

## Cropped output

A figure is saved at the size `figsize` declares, at `dpi` resolution. The window you were looking at has nothing to do with it.

So a chart whose labels fit on screen can be cropped in the file, and the first time this happens it looks like matplotlib lost the label.

`tight_layout()` or `constrained_layout=True` reserve the space. `bbox_inches="tight"` at save time expands the output to include everything.

Rotated tick labels and long y-axis labels are the usual casualties, and a chart type that does not need rotation &mdash; `barh` rather than `bar` &mdash; avoids the problem entirely.

## Colour that does not survive

Colours chosen to be visually distinct are often not distinct in **luminance**, and luminance is what remains in greyscale and what colour-blind readers rely on most.

Red, green and dark red are three obviously different colours with nearly the same brightness. Printed in black and white, they are one colour.

Two habits fix it: use a palette designed for the purpose &mdash; the viridis family, or Okabe&ndash;Ito for categories &mdash; and vary a second channel so colour is reinforcing rather than carrying the meaning.

The greyscale test is quick and catches most of it.

## Silent clipping

Setting limits that exclude data does not warn. The excluded points are simply not drawn, and a bar taller than the axis runs off the top looking like any other tall bar.

That is a serious failure: the reader sees a chart where one category is four times the next largest, and has no way to know.

matplotlib cannot warn about it, because clipping is often exactly what you want &mdash; zooming into a region is a legitimate operation.

The check is one line: compare `max(data)` against `ax.get_ylim()[1]`. Where a value is genuinely off-scale and the chart must stay zoomed, say so with an annotation giving the real number.

The related version is a category filtered out earlier in the pipeline and never noticed, which is why comparing the number of bars against the number of groups is worth doing.

## Figures left open

matplotlib keeps a reference to every figure created through pyplot, so they are never collected while it holds them.

After twenty, it warns: "More than 20 figures have been opened." That is a warning, not an error &mdash; the loop continues, and memory keeps growing until something else fails.

`plt.close(fig)` in the loop. `plt.close("all")` between sections of a notebook.

The threshold is `rcParams["figure.max_open_warning"]`, and raising it to silence the message is the wrong response to a real problem.

## A short list

Use `ax.` methods, not `plt.`.

Check the data before blaming the chart: length, NaN, limits.

Save with layout management, and look at the saved file rather than the screen.

Test in greyscale.

Compare the data's range against the axis limits.

Close figures in loops.

And the one from the design module that outranks all of them: know what the chart is for before drawing it, because none of these checks help a chart that is answering the wrong question.

## Mistakes of interpretation

Beyond the mechanical errors, a set of chart-level mistakes produce output that is technically correct and misleading.

**A truncated bar axis.** Length must be read from zero.

**Dual axes.** The crossing point is a choice, not a finding.

**Unshared axes across panels.** The layout invites a comparison the scales do not support.

**An uncentred diverging colormap.** Half the data is coloured as though it had the opposite sign.

**A line through sparse points.** It asserts values between the observations.

**A pie with many slices.** The reader cannot rank them.

**A mean without a spread.** Two very different distributions look identical.

Each of these is a default that matplotlib will happily produce, which is why they are worth knowing as a list.

## Mistakes of omission

Things whose absence is the error:

No units on the axis labels.

No indication of sample size, when it varies between groups.

No note that an axis is logarithmic, which changes how every distance on it should be read.

No statement of what an error bar represents.

No caption saying when the data is from and what it covers.

These cost a line each and are the difference between a chart that can be acted on and one that has to be asked about.

## Debugging a figure

A routine that resolves most problems quickly:

**Print the data.** Shape, range, count of NaN. Most "the chart is wrong" is "the data is not what I thought".

**Check the artists.** `len(ax.lines)`, `len(ax.patches)`, `len(ax.collections)` &mdash; did the draw call happen?

**Check the view.** `ax.get_xlim()`, `get_ylim()` against the data's range.

**Save it and look at the file**, which is what other people will see.

**Look at it in greyscale**, which catches encoding problems that colour hides.

In that order, because each is cheaper than the next.

## A pre-flight checklist

Before a chart is shared:

Does the title state the finding?

Do the axes have units?

Is the baseline appropriate?

Are the panels comparable, if the layout implies they should be?

Is anything clipped, hidden or overplotted?

Does it work without colour?

Is there one message?

Is the source and date on it?

Eight questions, most answered in seconds, and between them they catch nearly everything in this module.

## The general lesson

matplotlib will draw whatever it is asked. It has no opinion about whether the chart is honest, readable or answering a question anyone asked.

That is the right design for a library and it means the responsibility sits with the person writing the call. The mechanical parts of this track &mdash; the arguments, the objects, the defaults &mdash; are the easy half. The decisions are the half that determines whether the chart was worth drawing.

## Mistakes that look like matplotlib bugs

A few behaviours get reported as bugs and are working as designed.

**A figure appears blank in a script** &mdash; nothing called `show` or `savefig`.

**Colours ignored** &mdash; passing `c=` where `color=` was meant, or a colour list to a function taking a single colour.

**`set_facecolor` doing nothing on a box plot** &mdash; `patch_artist=True` was not passed.

**Ticks reappearing** after being set &mdash; a later autoscale replaced the locator.

**A legend showing one entry for many lines** &mdash; one `label` on a call that drew several.

**Text invisible after `transparent=True`** &mdash; the foreground was never changed.

Each has a one-line fix and none of them raises, which is what makes them frustrating rather than difficult.

## Building the habit

The checks in this module are worth turning into a routine rather than remembering individually.

A short function that draws and then asserts is one way:

```python
def finish(ax, title, xlabel, ylabel):
    ax.set_title(title, loc="left", fontweight="bold")
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    assert ax.get_title(), "no title"
    return ax
```

It enforces the labels, applies the house treatment, and fails if something was skipped.

More generally, the mistakes in this track fall into two groups: things matplotlib will not tell you (clipping, wrong axes, cropped output) and things nobody will tell you (a misleading baseline, an uninterpretable interval, a chart answering the wrong question). The first group is caught by checking; the second only by asking what the chart is for.

## The two kinds of error

It is worth separating them, because they are found in different ways.

**Errors matplotlib could tell you about but does not.** A plot on the wrong axes, a clipped bar, a cropped label, an empty series, a figure never closed. These are mechanical, they have definite answers, and the checks in this module find them in seconds. They are also the ones that produce a chart which is obviously odd once looked at.

**Errors nobody can tell you about.** A truncated baseline, an uncentred diverging scale, a dual axis, a mean without a spread, a chart answering a question nobody asked. These produce output that is technically correct and misleading, and no check catches them because nothing is wrong with the code.

The first kind is fixed by looking at the chart. The second is fixed by asking what the chart claims and whether the data supports it &mdash; which is a different activity, and the one that matters more.

## In summary

An empty plot is empty data, all-NaN data, or limits pointing elsewhere; `len(ax.lines)` says whether the draw happened.

`plt.plot` lands on the current axes, which is rarely the one you meant.

A figure saves at its declared size, so look at the file rather than the screen.

Limits that exclude data clip it silently, and a too-tall bar looks like any other tall bar.

Colours of similar luminance vanish in greyscale.

Figures left open warn after twenty and keep consuming memory.

And the checklist that catches most of it &mdash; title states the finding, units on the labels, correct baseline, nothing hidden, works without colour, one message, source and date &mdash; takes under a minute and is the difference between a chart that is finished and one that is merely drawn.

## A worked debug

A concrete example of the routine, on the most common complaint: "the chart is wrong".

**Look at the data going in.** `df.shape`, `df.head()`, `df.dtypes`, `df.isna().sum()`. About half of all wrong charts are correct renderings of wrong data, and this finds them before any plotting is examined.

**Check the artists.** Did the draw call happen, and how many things did it create? A legend with one entry where five were expected means one call drew five lines with one label.

**Check the view.** Limits against the data's range.

**Check the axes.** Is the plot on the axes you think? `len(ax.lines)` on each.

**Look at the saved file**, not the screen.

**Look at it in greyscale.**

The order matters because each step is cheaper than the next, and the first one resolves the majority. The instinct to start by reading matplotlib documentation is usually the slowest available route.

## The short version

Two kinds of error: the ones matplotlib could report and does not, and the ones nobody can report because nothing is wrong with the code.

The first are found by looking &mdash; at the data, the artists, the limits, the saved file. The second are found by asking what the chart claims and whether the data supports it, which is the harder and more valuable habit.
''',
    [
        {"q": "Your plot is empty. What distinguishes 'the draw never ran' from 'there is nothing to see'?",
         "options": ["The title", "len(ax.lines)", "The figure size", "The dpi"],
         "answer": 1,
         "why": "Then check len(x), np.isnan(y).all(), and ax.get_xlim() - empty data, all-NaN data, and limits pointing elsewhere all draw nothing."},
        {"q": "After `plt.subplots(1, 2)`, where does a stray `plt.plot` land?",
         "options": ["The left panel", "The last axes created - the right panel", "Both", "A new figure"],
         "answer": 1,
         "why": "In a notebook it is worse, because the current figure is whatever the last executed cell made. ax.plot removes the question."},
        {"q": "Why can a chart look fine on screen and be cropped when saved?",
         "options": ["A bug in savefig", "It saves at the declared figsize and dpi, not the window size", "The dpi is too low", "The format is wrong"],
         "answer": 1,
         "why": "Rotated tick labels and long axis labels are the usual casualties. tight_layout or bbox_inches='tight' fix it."},
        {"q": "What happens when axis limits exclude some of the data?",
         "options": ["matplotlib warns", "The data is silently clipped, and a too-tall bar looks like any other tall bar", "The limits expand", "It raises"],
         "answer": 1,
         "why": "matplotlib cannot warn, because zooming is legitimate. Compare max(data) against ax.get_ylim()[1]."},
    ],
)
