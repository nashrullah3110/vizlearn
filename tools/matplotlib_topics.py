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
intro: The two objects all hangs off, and the two APIs that confuse each example.

## Two objects

A **Figure** is the whole image: the canvas, its size, its background. The file it's eventually saved to.

An **Axes** is one plotting area inside it. The box with the ticks, the data, and the labels.

The name is unfortunate. "Axes" is singular here. It doesn't mean "the x and y axes". Those are `ax.xaxis` and `ax.yaxis`. This Are objects on the Axes. One figure can hold many Axes. This Is what a grid of subplots is.

Nearly all you want to do belongs to the Axes. Plotting, labelling, limits, ticks, legends and annotation are all `ax.` methods. The Figure handles size, the total title, layout between subplots, and saving.

`fig, ax = plt.subplots()` creates one of each and returns both. It's the standard first line of almost each matplotlib program. It's worth using even for a single plot. It puts you in the API that keeps working when the plot grows.

## Two APIs

each matplotlib example you find online is written in one of two styles. Mixing them is why so many of them are hard to follow.

**Stateful (pyplot)**: `plt.plot(...)`, `plt.title(...)`, `plt.xlabel(...)`. These act on "the current figure and current axes", which matplotlib tracks internally. It is compact and reads well for a single quick plot.

**Object-oriented**: `ax.plot(...)`, `ax.set_title(...)`. You hold the objects and say which one you mean.

The stateful API is a convenience layer over the object-oriented one. `plt.title` finds the current axes and calls `set_title` on it.

The translation is rote: most `plt.foo()` calls become `ax.set_foo()`. The exceptions are the drawing methods. `plot`, `scatter`, `bar`. Which keep their names because they're actions rather than properties.

## Why the object-oriented form

The current figure is a global var, with the problems globals always have.

In a script that draws one plot, nothing goes wrong. In a script that draws a few, `plt.plot` after creating a second figure lands on the second, whether or not that was the intent. In a notebook. Here Cells run again and again and out of order, "the current figure" is what ran last. Which is why plots at times appear on the wrong chart or an earlier figure gains a line no one added.

The object-oriented form has no such ambiguity: `ax1.plot` draws on `ax1`.

It's also the only form that works comfortably with subplots. Here There are a few axes and no sensible notion of a current one.

This track uses `fig, ax = plt.subplots()` throughout. Mentions the `plt` equal where you're likely to meet it in other people's code.

## Artists

all drawn is an **Artist**: lines, text, patches, the axes themselves.

Draw calls return the artists they create. `ax.plot` returns a **list** of `Line2D` objects. A list. One call can draw a few lines. Which is why the idiom is:

```python
line, = ax.plot(x, y)
```

The trailing comma unpacks the single element. Without it, `line` is a list and `line.set_color` fails.

Keeping the artist matters when you want to change it later: `line.set_color("crimson")`, `line.set_label("...")`. For a static plot you can skip the return value fully. This Is what most code does.

## Closing figures

matplotlib keeps an inner link to each figure created through pyplot. They're never garbage collected while that link exists.

For one plot that doesn't matter. In a loop. Making a chart per group, per file, per day. The figures build up. Matplotlib warns after twenty that "more than 20 figures have been opened".

`plt.close(fig)` closes one. `plt.close("all")` closes all. Any loop that draws should close.

On these pages the runner collects open figures after each run and closes them. This Is why an editor that draws shows its plot. That is also why a `plt.close()` at the end of an editor would leave you with no image. The figure has to still be open when the program finishes.

## Where matplotlib sits

matplotlib is the oldest and most widely used plotting library in Python. Nearly all else is built on it or interoperates with it. pandas' `.plot`, seaborn. The plotting in scikit-learn and statsmodels all give matplotlib objects you can adjust later.

That is the hands-on arg for learning it even if you mostly use a thing higher-level. When the convenience wrapper doesn't do quite what you need, the escape hatch is matplotlib, and it's always on hand.

Its age also shows its awkward parts. The pyplot interface was designed to feel like MATLAB, the object-oriented API came later. Both are supported forever. Most confusing examples online are simply mixing the two.

## The parts of a figure

Worth naming, because the docs uses these terms constantly:

**Figure** &mdash; the whole canvas.

**Axes** &mdash; one plotting area. A figure holds one or many.

**Axis** &mdash; the x or y scale on an Axes, with its ticks and label. `ax.xaxis`.

**Artist** &mdash; anything drawn: lines, text, patches, the axes themselves.

**Spines** &mdash; the four lines bounding the plotting area.

**Ticks** &mdash; the marks on an axis, with major and minor variants.

The tree is Figure &rarr; Axes &rarr; Axis &rarr; ticks and labels. Almost each method lives on the Axes.

## Showing a figure

In a **notebook**, figures display on its own when a cell finishes. `%matplotlib inline` is the default in Jupyter and rarely needs stating.

In a **script**, nothing is displayed unless you ask. `plt.show()` opens a window and blocks. `fig.savefig(path)` writes a file. A script that draws and does neither makes nothing. This Is a common first surprise.

On **these pages**, the runner collects any figure still open when your program finishes, renders it to a PNG. Shows it under the printed output. That is why the editors here never call `show` or `savefig`. And why calling `plt.close()` at the end of an editor would leave you with no picture.

## Backends

A **backend** is what matplotlib draws with. Interactive ones open windows. Non-interactive ones write files.

`AGG` is the non-interactive raster backend. It's what these pages use. A Web Worker has no window to draw into. `matplotlib.use("AGG")` selects it, and that call must come before pyplot is imported. Which is why it's in the page setup rather than in the examples.

You'll meet this in two places: on a server with no display. Here `AGG` is needed. In a script that hangs on `plt.show()` because it picked an interactive backend it can't really use.

## What this track covers

The first modules are the drawing types: lines, scatters, bars, histograms, boxes, images.

Then the parts that make a chart readable: labels, legends, limits, ticks, scales, colour, annotation.

Then layout: subplots, spacing, twin axes, saving.

Then judgement: choosing a chart, common mistakes, and speed when the data is large.

each module is six short programs. Each one draws. Changing a number and re-running is the fastest way to find out what an arg really does. Which is worth more here than in most libraries. Matplotlib's arg names aren't always guessable.

## Questions people ask first

**Why are there two ways to do all?**

History. pyplot was written to feel like MATLAB. Here There's one silent figure and commands act on it. The object-oriented API came later and is what pyplot calls underneath. Both are supported permanently. Examples mix them. That is the main reason matplotlib feels harder than it's.

**Do I need `plt.show()`?**

In a script, yes, unless you're saving to a file. In a notebook, no. On these pages, no. The runner collects what is open.

**Why does my figure look other on someone else's machine?**

A other style, a other `matplotlibrc`, a missing font, or a other backend. The first two are the usual causes and both are silent.

**Should I use seaborn instead?**

For statistical charts, often yes. It makes matplotlib objects. Nothing is lost. Knowing matplotlib is what lets you adjust what seaborn gives you.

**Why is my chart slow?**

Almost always too many artists, or too many points to be visible. Both have their own module.

## How to read the documentation

matplotlib's docs is large and organised around the object model. This Makes it hard to search until you know the vocab.

Three habits help.

Search for the **Axes method**, not the pyplot function. `Axes.set_xlabel` rather than `plt.xlabel`. Because that page lists the full signature and each keyword.

Read the **Artist** page for the thing you're styling. Most keyword args to a drawing call are properties of the artist it creates. `Line2D` docs all `plot` accepts beyond its own args.

Use the **examples gallery** as a search index. Finding a picture that resembles what you want and reading its source is often faster than working out what the step is called.

The API is wide but shallow: a few hundred methods, most of which take the same handful of styling args. Once the vocab is familiar the docs turns navigable.

## In summary

Two objects: a Figure holding one or more Axes. Almost each method you want belongs to the Axes.

Two APIs: the stateful `plt.*` one that draws into a hidden current figure. The object-oriented one that names the axes. The second is what this track uses. The first goes wrong the moment there's more than one figure. Which in a notebook is at once.

`fig, ax = plt.subplots()` is the standard opening line. The translation from any pyplot example is rote: `plt.title` turns `ax.set_title`. The drawing methods keep their names.

Draw calls return the artists they create. This You keep when a thing needs changing later and skip else.

And figures must be closed. Matplotlib holds a link to each one until you do.

all after this module is either a kind of drawing or a way of making the result readable. All of it hangs off those two objects.

## A closing note

matplotlib has a reputation for being hard. Most of that comes from two things this module handles.

The first is the two APIs. Examples that mix them without saying so. Once you know that `plt.title` and `ax.set_title` are the same step reached differently, most confusing code turns readable.

The second is that it's a **drawing** library rather than a charting one. It has no view about what a good chart is. It won't stop you. All is possible at the cost of nothing being auto.

That is the right trade for a foundation library. It's why each higher-level tool in Python either sits on matplotlib or has to reimplement it. Learning it well means the ceiling is never the library.

## Reading the code back

each chart in this track starts the same way and ends the same way. Create a figure and axes, draw with ax methods, label, adjust. Let the runner show it. What changes in the middle is the drawing call and the handful of args it takes. Recognising that shape makes the rest of the library a matter of looking up which method and which arg, rather than learning a new pattern each time.
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
intro: plot() and the args that do most of the work.

## The signature

`ax.plot(y)` draws `y` against its index. `ax.plot(x, y)` draws one against the other.

That one-arg form is convenient and at times misleading. A plot whose x axis reads 0 to 99 when the data is dated is often a forgotten x arg rather than a deliberate choice.

`plot` accepts lists, NumPy arrays and pandas Series. With a Series it uses the index as x. This Is why plotting a time-indexed Series gives a dated axis for free.

## The colour cycle

Each call to `plot` on the same axes takes the next colour from the **property cycle**, a list of ten colours defined by the current style.

This is why a few lines drawn in a loop come out in other colours with no work. Why the eleventh line repeats the first.

`plt.rcParams["axes.prop_cycle"]` holds it. `ax.set_prop_cycle(...)` replaces it for one axes. This Is how you enforce a house palette.

Passing an clear `color` bypasses the cycle without advancing it.

## Styling

Three keywords cover nearly all:

`color` &mdash; a name (`"crimson"`), a hex string (`"#4c72b0"`), a single letter (`"r"`), a grey level as a string (`"0.4"`), or an RGBA tuple.

`linestyle` &mdash; `"-"` solid, `"--"` dashed, `"-."` dashdot, `":"` dotted, or a dash pattern as a tuple.

`linewidth` &mdash; in points.

Add `alpha` for transparency. This Is how you keep many shared lines readable. `marker` to show where the actual data points are.

That last one matters more than it looks. A smooth line through four points implies a lot of data that doesn't exist. Markers say where the readings are and let the line be what it's. A visual aid rather than a claim.

## The format string

`ax.plot(x, y, "r--o")` sets colour, linestyle and marker in one string.

It's worth learning to read because it appears constantly in examples and docs. It isn't worth preferring. It supports only eight colours, can't set width or alpha. Is opaque to anyone who hasn't stored it.

The order within the string doesn't matter. Any part can be omitted. `"o"` alone draws markers with no connecting line. This Is a scatter plot by another route.

## Missing data

`NaN` values are skipped, and the line is broken where they occur.

This is the right default. A line drawn straight through a gap asserts that the value moved smoothly across it. This Is just the thing you don't know.

If you want the line joined, dropping the missing points is clear about it:

```python
ok = ~np.isnan(y)
ax.plot(x[ok], y[ok])
```

Note that `None` behaves like `NaN` here. A masked array's masked values are also skipped.

For a long series with occasional gaps, the broken line can look noisy. Drawing markers as well makes the pattern of missingness visible rather than merely untidy.

## Drawing order

Artists are drawn in the order the calls are made. Later calls sit on top.

`zorder` replaces it. Higher values draw later. The defaults are set so that the usual expectations hold. Patches at 1, lines at 2, text at 3. Which is why a line most times appears above a filled region even when the fill was drawn second.

Where it matters most is grid lines. `ax.grid()` draws below the data by default. `ax.set_axisbelow(False)` puts it on top. This Is almost never what you want but is at times what you get from a style sheet.

## Markers

`marker="o"` draws a symbol at each data point. The common ones are `o` circle, `s` square, `^` triangle, `D` diamond, `.` point, `+` and `x`.

Markers matter more than they look. A smooth line through five points implies a smooth link measured densely. Markers say where the readings really are and let the line be the visual aid it's.

`markevery=10` draws one marker in ten. This Keeps the "here are the findings" signal on a dense series without a solid band of symbols.

`markersize`, `markerfacecolor` and `markeredgecolor` style them apart from the line. A hollow marker is `markerfacecolor="none"`.

## Steps and stems

Not each sequence is a line.

`ax.step(x, y, where="post")` draws a step function. This Is correct for anything that holds a value until it changes. A price, a setting, a state. A straight line between the points would claim a gradual transition that didn't happen.

`where` takes `"pre"`, `"post"` or `"mid"`, deciding whether the step happens at the start or the end of each interval. Getting it wrong shifts each value by one spot. The chart looks plausible either way.

`ax.stem` draws a vertical line to each point. This Suits sparse discrete data.

`ax.fill_between` under a line turns it into an area chart, right when the quantity builds up to a thing real and misleading when it doesn't.

## Multiple lines and readability

Four or five lines on one axes is often the limit before the chart turns a tracing exercise.

Beyond that, the options in order of preference are. Highlight one and grey the rest, split into small multiples, or reduce to the two lines the chart is really about.

Where a few lines must stay, three things help.

**Direct labels** at the line ends, instead of a legend.

**Sorting the legend** to match the vertical order of the lines at their right-hand end. The eye can map them without hunting. `ax.legend(handles=...)` in the order you want.

**Varying linestyle** and colour, so the chart lives greyscale.

## Interpolation is a claim

A line between two points asserts that the quantity passed through the values in between.

For a temp sampled hourly, that is fair. For monthly sales, the line between January and February is decorative. Nothing happened at "January the 15th" in the data.

That doesn't make the line wrong. Connecting points is how the eye reads a trend. A scatter of twelve unconnected points is harder to follow. But it's worth knowing that the line is an aid rather than data. This Is another arg for markers.

Where the gaps are truly large, breaking the line is more honest than spanning them. That is what leaving the NaN in does for you on its own.

## Performance note

One `plot` call with a large array is fast. Many `plot` calls are slow. The cost is per artist rather than per point.

Drawing fifty lines in a loop creates fifty artists. Where they can be mixed, `LineCollection` draws them as one.

That matters at hundreds of lines rather than dozens. It's covered properly in the speed module.

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

Aspect, colour, weight, markers, a title that says a thing, labelled units, a faint grid on one axis, two spines removed.

Ten lines, none of them clever. The result looks deliberate. each one is covered one spot in this track, and together they're most of what splits a default matplotlib chart from a published one.

## Reading a line chart critically

Three questions worth asking of any line chart, including your own.

**Does the y axis start at zero. Should it?** A line codes spot. Truncation is legitimate. And it changes the apparent size of each change. If a 2% movement fills the chart, the reader should be able to tell.

**Are the x values evenly spaced?** If the axis is cat or the points are irregular in time, the slope between points isn't a rate. The eye reads it as one.

**What is between the points?** Twelve monthly findings joined by lines look like a smooth series. The line is an aid. The data is twelve points.

None of these makes a line chart wrong. They're the things a careful reader checks. Knowing them is what lets you draw one that lives the checking.

## In summary

`ax.plot(x, y)` with `color`, `linewidth`, `linestyle` and `marker` covers the great majority of line charts.

The colour cycle supplies distinct colours on its own and wraps after ten. This Is well past the point where a line chart has stopped being readable.

NaN breaks the line. This Is the honest treatment of a gap.

Markers say where the data really is. Matter most when the points are few. A smooth line through five findings claims a lot.

Later calls draw on top, and `zorder` replaces it.

And the finishing sequence is the same each time. An aspect ratio suited to the data, a title that says a thing, labelled units, a faint grid on one axis. The top and right spines removed.

## Smoothing

A noisy series is often plotted with a smoothed version over it. The pairing is more honest than either alone.

The raw series in a pale colour and the rolling mean in a strong one shows both the variation and the trend. Makes clear that the smooth line is derived rather than measured.

Two cautions worth stating on the chart.

**The window is a choice**, and a longer one makes a smoother, more lifelike line that is further from the data. Naming it. "7-day mean" &mdash; is the min.

**A centred window uses future values**. This Is fine for showing history and wrong for anything presented as a signal on hand at the time. A trailing window is the honest choice for that case, at the cost of lagging the turns.

Plotting only the smoothed line, without the raw data, is where this turns misleading. The reader has no way to judge how much was smoothed away.

## Highlighting within a line chart

A line chart with one key series and a few for context is the most common real case, and the treatment is steady:

```python
for name, y in others.items():
    ax.plot(x, y, color="0.85", linewidth=1, zorder=1)
ax.plot(x, focus_y, color="#264653", linewidth=2.5, zorder=2)
ax.text(x[-1], focus_y[-1], "  " + focus_name, va="center", color="#264653")
```

The grey lines give the range and the shape of the group. Nothing is lost. The dark line is unmistakably the subject. The label at the end drops the legend.

`zorder` ensures the highlighted line is on top even so of drawing order. This Matters when the context lines are drawn in a loop after it.

This pattern is worth having to hand. It converts the hardest kind of line chart. Many series, one message. Into one of the easiest to read.

## One more thing

`ax.plot` accepts a few x/y pairs in one call. `ax.plot(x, y1, x, y2)`. Which draws both with split colours from the cycle.

It's compact and gives no way to label the lines on their own. A loop with `label=` is often better. Worth recognising in existing code. Here It appears often.

## The short version

A line chart is the most common chart there's. The finishing sequence is the same each time. Aspect, colour, weight, title, units, a faint grid, two spines removed.

The line itself is an aid rather than data. This Is worth remembering when the points are few and the line is doing a lot of implying.

## Reading the code back

A finished line chart is about a dozen calls. It's worth being able to name what each one is for. The figure size sets the aspect, the plot call sets colour and weight, the title carries the message, the labels carry the units, the margins control the breathing space, the grid supports value reading. The spine removal takes away what carries nothing. Nothing in that list is optional in the sense of being decorative. Each answers a question a reader would else have to ask. Writing them in the same order each time makes the chart quick to give and quick to review. This Is most of why a house function is worth having.
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
intro: scatter() versus plot(), and the two extra dims you get for free.

## Two ways to draw dots

`ax.plot(x, y, "o")` draws markers with no connecting line. `ax.scatter(x, y)` draws a set of points.

They look same for a simple case, and they differ in what can vary.

`plot` draws one line object: each marker is the same size and the same colour. That uniformity makes it **faster**, at times much, for large numbers of same points.

`scatter` draws a `PathCollection` where size and colour can be arrays, one value per point. That is what makes it a four-dimensional display: x, y, size and colour.

The rule of thumb: `plot` when the points are all alike, `scatter` when they aren't.

## Size

`s` is the marker area in **points squared**.

That trips people, because doubling `s` doesn't double the visual width. It takes four times `s` to double the width. The default is around 36, meaning six points across.

Area is the right thing to scale. The eye checks areas rather than radii. A common mistake is passing a raw value as `s` and getting circles that differ far more than the underlying numbers do. Scaling into a sensible range first is often needed.

Very small values disappear and very large ones share into a mass. The handy range is narrow. Roughly 10 to 400 for most plots.

## Colour

`c=` takes an **array** of values. This Are mapped through a colormap and can be shown with a colorbar.

`color=` takes a **single** colour applied to each point.

The names are one letter apart and the failure is silent. Passing an array to `color` either errors or makes a thing unintended. Passing a single colour to `c` works but wastes the method. "Why is my whole plot one colour" is nearly always this.

`fig.colorbar(sc, ax=ax)` needs the object `scatter` returned. This Is why the return value is captured here where it's skipped elsewhere.

## Overplotting

A scatter with a few hundred points shows the data. With a few thousand it shows the outline of the data. Each point in the middle is hidden behind another.

Three responses, in order of how much they preserve:

`alpha` below 1 makes density visible as darkness. It's the cheapest fix and works up to tens of thousands of points.

Smaller markers help, and combine with alpha.

`hexbin` or `hist2d` bins the points and shows counts. This Turns density from a thing implied into a thing measured. Past roughly fifty thousand points this is the only honest option. It's also far faster to draw.

Sampling is a fourth option, and a fair one when the shape matters more than the completeness.

## Making it readable

`edgecolor="black"` with a thin `linewidth` outlines each marker. This Splits points that share. It's the single most good small gain to a moderately dense scatter.

Marker shape sets apart groups, and does so weakly. Readers well tell apart about three shapes, not six. Colour and spot are much stronger encodings. If you need six groups, small multiples often beat six shapes on one plot.

## Trend lines

`np.polyfit(x, y, 1)` returns slope and intercept. The fit is then drawn with an plain `plot`.

Two details worth getting right. Draw the line only over the range of the seen x values. It doesn't imply the link holds beyond the data. And put the coeffs in the legend label. So The chart carries the number rather than needing the reader to guess it.

For anything beyond a straight line, `numpy.polynomial` is the modern interface and SciPy or statsmodels give trust intervals. At which point the fit is a statistical claim and deserves the nearby machinery.

## Colour by category

For a cat var, plotting one scatter per group is clearer than mapping colours by hand:

```python
for name, sub in groups.items():
    ax.scatter(sub.x, sub.y, label=name, alpha=0.7)
ax.legend()
```

Each call takes the next colour from the cycle and the legend is built from the labels. Nothing has to be assembled manually.

Passing a list of group codes to `c=` works and gives you a smooth colormap applied to any ints. This Implies an sorting the groups don't have. The same mistake as using a sequential colormap for groups.

## Bubble charts

Encoding a third var in the marker area makes a bubble chart. It has a exact weakness. Area is read poorly. The third var is the least accurately seen thing on the chart.

Two rules make them work when they're used.

Scale by **area**, not by radius. Passing the raw value as `s` scales by area already. `s` is area. But finding a radius and squaring it's a common way to exaggerate differences fourfold.

Provide a **size legend**, since no one can read an area off a chart without a link. `ax.legend` can be built from proxy artists at a few representative sizes.

If the third var is the point of the chart, spot or colour will carry it better than size.

## Jitter for discrete values

When one axis is discrete. A rating from one to five, a day of the week &mdash; points land just on top of each other and the density is invisible.

Adding a small random offset splits them:

```python
xj = x + rng.uniform(-0.15, 0.15, len(x))
```

The jitter must be small enough not to blur the groups. It should be mentioned if the chart is published. It's a deliberate distortion of spot.

`alpha` and marker size do part of the same job and don't move anything.

## Connecting scatter points

`ax.plot(x, y, "-o")` connects points in the order they appear in the array. This For a scatter is often meaningless and at times just right.

The case where it's right is a **connected scatter**. Two vars measured over time, with the line showing the path through the space. Unemployment against inflation year by year, say. Adding an arrow or labelling the first and last point makes the direction readable.

For anything without a natural order, sorting by x before connecting is what turns it into a line chart. Doing it accidentally. Because the data happened to arrive sorted. Makes a chart that implies a sequence that doesn't exist.

## Density alternatives, in order

As n grows, the sequence of fair displays is fairly fixed:

**Under 1,000** &mdash; a plain scatter, with `edgecolor` for split.

**1,000 to 20,000** &mdash; `alpha` around 0.1&ndash;0.3, smaller markers.

**20,000 to 500,000** &mdash; `hexbin` or `hist2d`. This Measure density rather than implying it.

**Above that** &mdash; datashader, or aggregate before plotting.

At each stage the question is the same. Can the reader see the middle of the spread, or only its outline? If only the outline, the display has stopped working even so of how many points are strictly drawn.

## Correlation and what a scatter shows

A scatter is the display for a link. It shows more than a link coeff does.

It shows the **shape** &mdash; linear, curved, stepped &mdash; where a coeff assumes linearity.

It shows **outliers**, which can create or destroy a link on their own.

It shows **clusters**, which a single coeff means away. Which often mean an unmodelled group var.

It shows **heteroscedasticity** &mdash; spread that changes with x &mdash; which invalidates a few standard tests.

Anscombe's quartet is the canonical demo: four datasets with same means, variances and link. Four fully other scatters. Plotting first isn't a formality.

## Practical defaults

A scatter that works most of the time:

```python
ax.scatter(x, y, s=25, alpha=0.6, edgecolor="white", linewidth=0.4)
```

Moderate size, some transparency, and a thin light edge that splits shared points without adding visual weight.

From there the adjustments follow the data: lower alpha and smaller markers as n grows, `hexbin` when the middle stops being visible, colour when there's a third var worth showing.

For a link that will be discussed, adding the fit and putting its slope in the legend saves the reader guessing it. And forces you to look at whether a straight line is the right model. This The scatter will have already told you.

## In summary

`scatter` when size or colour varies per point, `plot` with a marker when they don't. The second is faster and there's nothing to gain from the machinery you aren't using.

`s` is area, so it scales as the square of the visual width.

`c=` takes an array through a colormap. `color=` takes one colour. The gap is one letter and makes very other charts.

Overplotting is the recurring problem, and the sequence of answers is alpha, then smaller markers, then hexbin, then aggregation before plotting.

`edgecolor` splits shared points and is the cheapest readability fix on hand.

And a scatter shows things a link coeff can't. Shape, clusters, outliers and changing spread. That is the reason to draw one before finding anything.

## Adding a third dimension well

When a scatter needs to carry a third var, the options aren't equally good.

**Colour, sequential** &mdash; for a smooth third var. Read fairly well, and needs a colorbar.

**Colour, cat** &mdash; for a few discrete levels. Works up to about five before the colours stop separating.

**Small multiples** &mdash; one panel per level of a cat var. Better than colour for anything above three levels. Checking panels is easier than separating shared colours.

**Size** &mdash; read poorly, and best reserved for a var that is context rather than the subject.

**Shape** &mdash; read poorly beyond about three levels.

The pattern is that the two strong channels. Spot and panel. Are already used or on hand. The weak ones should carry the least key var. Encoding the most key third var as size is a common inversion of that.

## Labelling points

A scatter of named entities. Countries, products, customers &mdash; often wants some of the points labelled.

Labelling all of them makes an unreadable mass. The handy approaches:

**Label the extremes**, which are what the reader will ask about: the highest, the lowest, the furthest from the fit.

**Label a chosen few** that the pairing text discusses.

**Label on hover**, which matplotlib doesn't do well and is a reason to use an interactive library when it matters.

For the first two, offsetting the text so it doesn't sit on the marker is needed:

```python
ax.annotate(name, (x[i], y[i]), textcoords="offset points",
            xytext=(5, 4), fontsize=9)
```

With more than about eight labels, shares become the problem. `adjustText` is the usual third-party answer. Or, more simply, labelling fewer points.

## One more thing

`ax.scatter` returns a `PathCollection`, and `set_offsets` updates the point spots without redrawing all.

That is what makes an animated or interactive scatter fast. It's the same reuse principle as `set_ydata` on a line: create the artist once, change its data.

## The short version

A scatter is the display that shows what a summary statistic can't: shape, clusters, outliers and changing spread.

Its failure mode is density, and the sequence of fixes is fixed. Alpha, smaller markers, hexbin, aggregation. The question at each stage is whether the middle of the spread is still visible.

## Reading the code back

A working scatter is often four choices: marker size, transparency, whether an edge is needed. Whether a third var is being coded. all else follows from the data. The size and alpha are chosen from the number of points rather than from taste. This Is why the same two lines that work for two hundred points fail for twenty thousand. Why the sequence of density fixes in this module is worth having in mind before drawing rather than after.
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
intro: Vertical, flat, grouped and stacked, and why the baseline has to be zero.

## bar and barh

`ax.bar(groups, values)` draws vertical bars. `ax.barh` draws flat ones.

For cat data, **flat is often better**. The reason is typography. Group labels are words, words are wide, and a vertical chart has only a bar's width in which to put each one. The usual workarounds. Rotating labels 45 degrees, truncating them, shrinking the font. All make the chart harder to read.

`barh` gives each label a full line of flat space, reading left to right like text.

Vertical bars remain right when the x axis is sorted and quantitative-ish. Months, years, bins of a spread. There the order carries meaning and the labels are short.

## Sorting

Bar charts are read by checking lengths. Compare is much easier when the bars are sorted.

Unless the group order means a thing. Months, sizes, a fixed scale. Sort by value. It costs one line with `np.argsort` and changes the chart from a thing to be studied into a thing to be glanced at.

With `barh`, note that bars are drawn from the bottom up. Sorting **ascending** puts the largest bar at the top. This Is where the eye starts.

## Labelling

`ax.bar_label(bars)` writes each bar's value at its end. It takes the holder returned by `bar` or `barh`. This Is why that return value is worth keeping here.

`fmt="%.1f"` controls the format. `labels=[...]` replaces the text fully. This Is how you show percentages or add units.

Once the values are on the bars, the value axis is often redundant. Dropping it. `ax.set_xticks([])` and hiding the spines. Leaves a chart that is quieter and easier to read. This is one of the few cases where deleting a standard chart element is almost always an gain.

## Grouped bars

There's no grouped-bar function. You find the spots.

The pattern is: take `x = np.arange(n_groups)`, choose a bar width `w`. Offset each series by a fraction of it. For two series, `x - w/2` and `x + w/2`. For three, `x - w`, `x`, `x + w`.

Then `ax.set_xticks(x)` and `ax.set_xticklabels(groups)` put one label in the middle of each cluster. The default ticks would else fall on the single bars.

Keep the total width of a group below 1 so there's a gap between clusters. A group of three bars of width 0.25 leaves 0.25 of space, which reads well.

Beyond three or four series per group, the chart stops working. Small multiples are the better answer.

## Stacked bars

`bottom=` gives the starting height of each segment. Each call passes the cumulative sum of all below it.

Stacking answers one question well. What is the total &mdash; and another badly. Only the **bottom** segment sits on a common baseline. Only it can be checked across bars by eye. Segments higher up float at other heights. Checking them is truly hard.

So: stack when the total is the message and the breakdown is context. Group when the parts are the message. And if the question is really about proportions, a 100% stacked bar. Each column normed to 1. Answers it better than either.

## The zero baseline

This is the one rule about bar charts that isn't a matter of taste.

A bar shows its value by **length**. If the axis starts at 97, a bar of value 98 has one unit of length and a bar of value 102 has five. The chart shows a five-fold gap where the data has a 4% one.

Line charts don't have this problem. A line codes value by **spot**. Spot is read against the axis labels. That is why truncating a line chart's y axis is acceptable and truncating a bar chart's isn't.

matplotlib will happily let you do it. It happens by accident when `set_ylim` is applied to a bar chart to "zoom in".

If the differences are truly small and truly notable, the answer is a other chart. A line, a dot plot, or a chart of the differences themselves. Not a truncated bar.

## Width and spacing

`width` is in data units, and the default of 0.8 leaves a fifth of the spacing as a gap.

Setting it to 1.0 drops the gaps fully. This Turns a bar chart into a thing that reads like a histogram. And that is just the gap the gap sends. Bars with gaps say "these are split groups". Bars without say "these are adjacent intervals of a smooth var".

That is why a histogram has no gaps and a group chart does. Why dropping the gap from a group chart is a small lie.

For grouped bars, the math is: total group width below 1, cut by the number of series. Three series of width 0.27 occupy 0.81 and leave a fifth of a unit between clusters.

## Colour on bars

A bar chart often needs **one** colour. The groups are already distinguished by spot and label. Colouring each bar differently adds nothing and implies a grouping that isn't there.

The exception is highlighting: one bar in a strong colour and the rest in grey says which group the chart is about. Is far more good than an annotation.

```python
colors = ["0.75"] * len(names)
colors[focus] = "crimson"
ax.barh(names, values, color=colors)
```

Colour turns real again when it codes a second var. Above or below target, plus or minus. And then two colours, not seven.

## Negative values

Bars extending below zero are drawn on its own. The baseline should be made visible:

```python
ax.axhline(0, color="black", linewidth=0.8)
```

Without it, the zero line is implied by the axis and easy to lose.

Colouring by sign is the standard treatment. It's one of the few cases where two colours on one series is right:

```python
colors = ["#2a9d8f" if v >= 0 else "#e76f51" for v in values]
```

For a diverging bar chart. Change from a baseline &mdash; sorting by value puts the largest grows and falls at the two ends. This Is often the most readable setup.

## Bars for parts of a whole

A stacked bar normed so each column sums to 100% answers "what is the composition" better than either a pie or an plain stack.

```python
shares = counts / counts.sum(axis=0)
```

Each segment is then a proportion, the columns are right close. The total. Which is no longer shown. Can go in the axis label or an annotation if it matters.

The left weakness is the same as any stack. Only the bottom and top segments have a fixed baseline. Middle groups are hard to compare across columns. Sorting the groups so the ones being checked are at the bottom mitigates it.

## Bars are not always right

Two cases where the default choice is wrong.

**Small differences.** A bar's message is its length. Length must be read from zero. If the notable differences are 2% of the value, a bar chart can't show them honestly. A dot plot, or a chart of the differences, can.

**Many groups.** Forty bars is a wall. Sorting helps. Beyond about twenty a dot plot or a lollipop chart uses far less ink per group and stays readable.

`ax.hlines` plus `ax.scatter` builds a lollipop in two lines. It's often the better display for a long ranked list.

## Labels on and around bars

`ax.bar_label` handles the common case, and its args cover most of the rest.

`padding=3` sets the gap in points. `fmt="%.1f%%"` formats. `label_type="center"` puts the value inside the bar rather than beyond its end. This Suits stacked segments where there's no free space at the tip.

For stacked bars, calling it once per holder labels each segment:

```python
for container in ax.containers:
    ax.bar_label(container, label_type="center", fmt="%.0f")
```

Small segments give shared labels. So Filtering to the ones with room is often needed. `labels=[v if v > threshold else "" for v in values]`.

Once values are on the bars, dropping the value axis fully makes the chart quieter and loses nothing.

## The bar chart checklist

Before a bar chart is finished:

**Is it sorted?** Unless the order means a thing.

**Is it flat?** Unless the labels are short or the axis is sorted.

**Does it start at zero?** Always, for bars.

**Is there one colour?** Unless colour codes a thing, or one bar is highlighted.

**Are the values labelled?** If so, is the axis now redundant?

**Are there too many bars?** Past about twenty, a dot plot reads better.

**Is the gap between bars visible?** It's what says these are groups rather than intervals.

Seven questions, and a chart that answers all of them well is close to as good as a bar chart gets.

## In summary

Flat, sorted, one colour, from zero.

That covers most bar charts, and each part has a reason. Flat because group labels are words, sorted because the reader shouldn't have to rank them, one colour because spot already sets apart the groups, and from zero because a bar codes value as length.

`bar_label` puts the numbers on the bars. This Often makes the value axis redundant.

Grouped bars need the offsets found by hand. Stacked bars need `bottom` and hide all above the first segment.

And past about twenty groups, a dot plot or lollipop chart uses far less ink and stays readable. This Is worth reaching for rather than shrinking the bars further.

## Bars over time

Bars and lines both show a quantity over time, and the choice says a thing.

A **line** implies continuity: the quantity existed between the findings and moved smoothly. Right for a reading sampled again and again. A temp, a price, a running total.

**Bars** imply discreteness: each period is a split quantity. There's nothing between them. Right for a total per period. Monthly revenue, daily counts, quarterly headcount.

Most business time series are period totals and are drawn as lines out of habit. The bar version is often more honest and reads no worse.

Two hands-on points. Bars need the zero baseline. This Limits how much detail can be shown when the variation is small scaled to the level. And with many periods bars become too thin to read, at which point a line or a step is the hands-on choice even so of the semantics.

A step plot is the compromise: discrete like bars, compact like a line.

## One more thing

`ax.barh` draws from the bottom up. A list passed in ascending order appears with the largest at the top.

That is often what you want and is the opposite of the intuition from `bar`. Here Ascending order puts the largest on the right. Sorting ascending and letting `barh` reverse it visually is the idiom.

## The short version

Flat, sorted, one colour, from zero. Four defaults that fix most bar charts before anything else is seen as.

The zero baseline is the only rule here that isn't a matter of taste. A bar codes value as length and a truncated axis misstates each ratio on the chart.

## Reading the code back

A bar chart is one call and a handful of choices made before it. Which orientation, what order, one colour or two, whether the values go on the bars. Whether the axis is then needed at all. Those choices are all made in the data preparation and the arg list rather than in anything clever. This Is why bar charts are quick to give well once the defaults are settled and quick to give badly when they aren't.
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

`counts` has one entry per bin. `edges` has **one more**. N bins are defined by n+1 boundaries. That off-by-one is the usual confusion when using the return values. It's the same rule `np.histogram` follows.

`patches` is the set of rectangles, kept if you want to recolour given bars. Highlighting a threshold, say.

`edgecolor="white"` is worth adding almost always: without it, adjacent bars merge into a single shape and the bin structure disappears.

## Bins decide the story

This is the thing to understand about histograms, and it isn't a detail.

The same data with three bins and with three hundred looks like two other datasets. Too few bins smooths away real structure. A bimodal spread turns one lump. Too many turns sampling noise into apparent spikes.

There's no correct number. It depends on the sample size, the underlying shape. What you're trying to see.

The honest practice is to **look at more than one**. If a feature lives at a few bin counts, it's probably real. If it appears only at one, it's probably not.

## The automatic rules

`bins="auto"` uses the larger of two rules:

**Sturges** assumes roughly normal data and scales with `log2(n)`.

**Freedman&ndash;Diaconis** uses the interquartile range and scales with `n^(1/3)`. This Handles skew and outliers better.

`"scott"`, `"sqrt"` and `"rice"` are also on hand. They disagree with each other, at times by a factor of a few. This Is a fair summary of how well-defined the problem is.

`"auto"` is a fair default and a starting point rather than an answer.

You can also pass clear edges: `bins=np.arange(0, 101, 5)` gives fixed 5-unit bins. This Is what you want when the boundaries have meaning or when two charts must be close.

## density

`density=True` scales the bars so the **total area** is 1 rather than showing raw counts.

Two situations need it.

**Checking samples of other sizes.** With counts, a sample ten times larger has bars ten times taller all over. The shapes can't be checked. With density they overlay.

**Overlaying a theoretical curve.** A normal PDF is a density. It only lines up with a histogram that is also a density.

Note the y axis then reads as density, not proportion. The values can exceed 1 when the bins are narrow. The area is 1. The height isn't a chance.

## Comparing groups

`ax.hist([a, b], bins=20)` &mdash; a list of arrays &mdash; draws them side by side within each bin. Both stay readable, at the cost of halving the good bin width.

split `hist` calls with `alpha` around 0.5 overlay them. The bins keep their width. The share region turns a blended colour that belongs to neither series.

`histtype="step"` draws outlines only. This Overlays cleanly for three or four groups where filled bars wouldn't.

Beyond three groups, none of these work well. The answer is small multiples. One histogram per group, sharing axes, side by side.

## The cumulative view

`cumulative=True` with `histtype="step"` draws an empirical cumulative spread.

It answers "what fraction is below x" right. This Is often the actual question. And quantiles read straight off it. Here They must be guessed by eye from a histogram.

It has a further hands-on edge: it barely depends on the bin count. Using two hundred bins gives a smooth curve rather than noise. Each bin adds to a running total rather than standing alone. That makes it the more honest display when the bin choice is doing too much work.

## Related displays

`ax.boxplot` summarises a spread as five numbers. This Checks many groups compactly and hides the shape fully. A bimodal spread and a uniform one can give the same box.

`ax.violinplot` shows an guessed density. This Restores the shape at the cost of a smoothing param that has the same arbitrariness as the bin count.

`ax.hexbin` and `ax.hist2d` are the two-dimensional versions, for when the question is about the joint spread rather than a single var.

## Bin edges you choose

Passing a count lets matplotlib pick the edges. This Land on unmemorable numbers like 3.17 to 7.42.

Passing an array puts them where you want:

```python
ax.hist(ages, bins=np.arange(0, 101, 10))
```

Ten-year bands, starting at zero, with boundaries a reader can name. That is almost always better for exchange. It has a second gain. Two histograms drawn with the same clear edges are right close. Here Two drawn with `bins=20` aren't.

`range=(lo, hi)` limits the extent without fixing the count. This Is how you exclude a long tail without dropping the data.

Values just on a boundary go into the **right-hand** bin, except at the last edge where the final bin includes both ends.

## Weights

`weights=` gives each finding a multiplier. This Covers two common needs.

**rate data** &mdash; when the input is already counts per value rather than raw findings.

**Percentages** &mdash; `weights=np.ones(n) / n * 100` makes the y axis read as a percentage of the sample. This Is often more handy than either counts or density and is easier to explain than density.

Density has the awkward property that its values depend on the bin width and can exceed 1. A percentage doesn't.

## Two-dimensional histograms

`ax.hist2d(x, y, bins=50)` bins in both directions and colours the cells by count. `ax.hexbin` does the same with hexagonal bins. This Tile more evenly and avoid the visual artefacts of a square grid.

Both replace an overplotted scatter with a thing that measures density instead of implying it. Both need a colorbar to be readable.

`bins="log"` on hexbin, or `norm=LogNorm()`, handles the usual situation where a few cells hold most of the points and all else is faint.

## Step histograms for comparison

`histtype="step"` draws the outline only. `histtype="stepfilled"` fills it with transparency.

For checking three or four spreads, outlines overlay far more cleanly than filled bars. Nothing is hidden. The colours don't blend into a fourth colour that belongs to no series.

Mixed with `density=True` it's the standard way to compare spreads of other sizes on one axes.

Beyond four, small multiples remain the answer.

## What a histogram cannot show

A histogram shows a marginal spread and nothing else.

It can't show a link between two vars, a change over time, or an sorting within the data. Two datasets with same histograms can be fully other, in the same way that two datasets with same means can be.

The exact thing it hides is **sequence**: a series that drifts upward over time and one that is stationary give the same histogram. If the data has an order, a line chart of the values and a histogram of them answer other questions. The histogram alone can conceal a trend fully.

## Choosing the bins in practice

A workable method, rather than a rule.

Start with `bins="auto"` and look at it. Then try roughly half and roughly double that number and look at those.

If the three agree about the shape, the shape is real and any of them will do. Pick round-numbered edges for the final version.

If they disagree, the disagreement is the finding. There's structure at one scale and not another. And the chart should show the bin count that matches to the question being asked.

For a chart that will be checked with another, fix the edges by name with an array. Two histograms with on its own chosen bins aren't close even when they look it. The bin widths differ.

And for anything above a few thousand points, a cumulative plot or a density guess sidesteps the choice fully. This Is often the honest move.

## Related displays, and when to switch

A histogram is one of a family, and it isn't always the strongest member.

**Cumulative** &mdash; when the question is about quantiles or thresholds. To escape the bin-count problem.

**Box plots** &mdash; when checking more than three groups.

**Violin or KDE** &mdash; when the shape matters and the sample is large.

**Strip plot** &mdash; when the sample is small enough that the findings are the honest display.

**Rug plot** &mdash; tick marks along the axis, added under any of the above. This Shows just where the data is without a binning choice.

`ax.plot(x, np.zeros_like(x), "|", markersize=12, alpha=0.3)` draws a rug in one line. Mixing it with a histogram gives both the shape and the raw spots.

## In summary

The bin count is the whole story: it decides what shape the data appears to have, there's no correct value. Looking at two or three is the only honest approach.

`bins="auto"` is a fair start and an arg between two rules rather than an answer.

clear edges make two histograms close. This On its own chosen bins never are.

`density=True` is what lets samples of other sizes be checked. Its y axis is a density rather than a proportion.

For a few groups, side-by-side or step outlines up to three or four, and small multiples beyond that.

And the cumulative view answers quantile questions right while barely based on the binning. Often the more honest display when the bin choice is doing too much work.

## What to check on a histogram

Four things, none of which the chart tells you.

**How many findings?** A histogram of thirty looks much like one of thirty thousand. Means far less. Putting `n` in the title or a corner is a one-line fix.

**How many bins, and does the shape live changing it?** The single most key check.

**Is anything outside the range?** If `range=` was set, or the axis limits were, the excluded values are simply gone.

**Are the bins equal width?** With clear edges they may not be. Unequal bins with a count axis are misleading. The area should represent the count. This Is what `density=True` handles right and a raw count doesn't.

The last is a genuine trap: a histogram with wide bins at the tail and narrow ones in the middle, plotted as counts, exaggerates the tail. If the bins are unequal, density is the only honest y axis.

## One more thing

`np.histogram` finds the counts without drawing anything. This Is handy when the numbers are wanted alongside the chart or when the binning needs checking before it's plotted.

It takes the same `bins` arg and returns counts and edges. The values behind a histogram can be printed, tested, or written to a file without a second pass over the data.

## The short version

The bin count is a param that changes the answer. It's chosen by default when no one chooses it on purpose.

Looking at more than one binning. Stating which one the chart uses, is the whole of good practice here. Along with knowing that a cumulative view sidesteps the problem when the question is about quantiles.

## Reading the code back

A histogram is one call whose most key arg is the one people leave out. Passing clear edges rather than a count makes the chart close with another, gives boundaries the reader can name. Forces the binning to be a choice rather than a default. Adding the sample size to the title and an edge colour to the bars costs two more args and answers most of what a reader would ask.
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
intro: The text that turns a plot into a thing someone else can read.

## The minimum

each chart that leaves your screen needs a title, an x label and a y label. A legend if there's more than one series.

The axis labels carry the part people most often omit: **units**. "Sales" could be rupees, units, thousands or a percentage change. A reader who has to guess can't act on the chart. "Sales (&#8377. Thousands)" takes four extra characters and drops the question.

`ax.set(title=..., xlabel=..., ylabel=...)` does all three in one call. This Is convenient in a chain.

## legend

`ax.legend()` collects the artists on the axes that have a `label` and draws a key.

Artists without a label are skipped. If nothing has one, matplotlib warns and draws nothing. That warning. "No artists with labels found". Is one of the most common in matplotlib and always means the same thing.

A label beginning with an underscore is **on purpose excluded**. That is the method for keeping a helper artist. A threshold line, a shaded band. Out of the key without giving up labelling it in code.

You can also pass the handles and labels by name, `ax.legend(handles, labels)`. This Is how you control the order or combine artists from other axes.

## Placement

`loc` names a spot: `"upper right"`, `"lower left"`, `"center"`, and the rest.

The default is `"best"`. This Searches for the spot shared the least data. That is convenient and has two costs. It's slow on a plot with many points. It can put the legend one spot other when the data changes, which is unwelcome in a figure you're iterating on.

For a legend outside the axes:

```python
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0)
```

`bbox_to_anchor` gives a point in axes coords. `(1.02, 1)` is just past the right edge, at the top. And `loc` says which corner of the legend goes there. note to leave room, with `fig.tight_layout()` or a smaller axes, or the legend will be cut off when saved.

`ncol=3` spreads a legend flatly. This Suits one placed above or below the axes.

`frameon=False` drops the box. This Often looks cleaner over a plot with white space.

## Direct labelling

A legend asks the reader to match a colour to a name, hold it in memory. Find the matching line. That is real cognitive work, repeated for each series.

Labelling each line at its end drops the step:

```python
ax.text(x[-1] + 0.2, y[-1], name, va="center")
```

It works well when the lines end at other heights. This Is common in time series. It fails when they settle. Then a legend is the honest choice.

This is one of the highest-value small gains on hand to a line chart. Matplotlib has no built-in for it. Two lines of `text` is the whole setup.

## Titles that say something

The default habit is a title that names the vars: "Sales by month". The chart already shows that. The axis labels already say it.

A more handy title states the **finding**: "Sales peaked in August, then fell 22%". The reader then knows what they're looking for. The chart supports the claim rather than posing a question.

`loc="left"` left-aligns the title. This Makes it read like a headline rather than a caption. Mixed with a slightly larger font and a subtitle in smaller grey text, it's the layout most publications use. It's a few lines of matplotlib.

Annotating the thing the title mentions. A vertical line at the peak, a highlighted point. Closes the loop between the words and the picture.

## Figure-level text

With a grid of subplots sharing axes, repeating the same axis label on each panel is noise.

`fig.supxlabel`, `fig.supylabel` and `fig.suptitle` attach text to the figure instead. One label serves the whole grid.

`fig.tight_layout()` later makes room for them. Without it, a suptitle often shares the top row of panels.

## Text properties

each text-making method takes the same styling args: `fontsize`, `fontweight`, `color`, `family`, `style`, `alpha`, `rotation`.

A small set of rules covers most charts:

**Title** &mdash; larger, bold, left-aligned. It's a headline.

**Axis labels** &mdash; default size, sentence case, with units.

**Tick labels** &mdash; smaller and lighter than the data. They're link rather than content.

**Annotations** &mdash; the colour of the thing they annotate. This Ties them together without an arrow.

`plt.rcParams` holds defaults for all of these. `axes.titlesize`, `axes.labelsize`, `xtick.labelsize`. So a house style sets them once rather than per chart.

## Legend contents

`ax.legend()` takes args that solve most legend problems.

`ncol=3` spreads it flatly. This Suits a legend above or below the axes and wastes far less vertical space than a single column.

`title="Region"` labels the legend itself. This Drops the need to explain the groups elsewhere.

`frameon=False` drops the box. `framealpha=0.8` keeps it but lets the data show through.

`fontsize="small"` shrinks it, right because a legend is link material rather than content.

`handles` and `labels` given by name control both the order and the contents. How you put the series in the same vertical order they appear on the chart. This Makes the mapping obvious.

## Mathematical text

Any text arg accepts mathtext between dollar signs:

```python
ax.set_ylabel(r"Energy ($\mathrm{J\,m^{-2}}$)")
```

The `r` prefix matters, because backslashes are else read by Python before matplotlib sees them.

This is a built-in subset of LaTeX and needs no LaTeX installation. `rcParams["text.usetex"] = True` switches to a real LaTeX renderer for full support, at the cost of needing LaTeX to be present and slowing rendering a lot.

For units, superscripts and Greek letters. Which is most scientific labelling &mdash; mathtext is enough.

## Multi-line and wrapped text

A long title can be broken with a newline. The alignment applies to the block:

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

Two lines, and the chart reads like a thing published rather than a thing exported.

## Labels that fix themselves

The most robust label is one found from the data rather than typed:

```python
ax.set_title("Peak %s: %.0f" % (months[i], y[i]))
ax.legend(title="n = %d" % len(df))
```

A hard-coded number in a title is wrong the first time the data changes. Nothing will tell you. Deriving it means the chart can't disagree with itself. Which matters most for just the charts that get regenerated regularly.

## Where the reader looks

Text placement isn't only about fitting. It's about the order things are read.

The **title** is read first, so it should carry the message.

The **direct labels** on the data are read next, if they exist. This Is why they beat a legend.

The **axis labels** are consulted when a value needs reading.

The **legend** is consulted again and again. This Is the cost that direct labels drop.

A **caption or source note** is read last, if at all. Belongs in small grey text at the bottom.

Designing in that order &mdash; message, then data labels, then link material &mdash; makes a chart that can be understood at a glance and interrogated later. This Is what a good chart does.

## Common labelling errors

**No units.** The single most common omission, and the one that makes a chart unusable.

**A title that repeats the axes.** "Sales by month" over a chart with "Month" and "Sales" on the axes says nothing new.

**A legend with no title**. Here The groups need showing.

**Labels rotated 45 degrees** when `barh` would have avoided rotation fully.

**Text that shares the data**, with no background box.

**A hard-coded number in the title** that no longer matches the data.

**A legend in `loc="best"`** that moves between runs, making two versions of a figure hard to compare.

All are cheap to fix and all live into published charts regularly.

## In summary

Title, both axis labels with units. A legend when there's more than one series. That is the min, and units are the part most often missing.

`legend()` reads labels from the artists, warns when there are none. Skips anything whose label starts with an underscore.

Direct labels on the lines drop the colour-matching a legend imposes. Are worth the two lines of `text` they cost.

A title that states the finding is more handy than one naming the vars. `loc="left"` makes it read as a headline.

For a grid, `fig.suptitle` and `supxlabel` replace repeating the same label on each panel.

And any number in a label should be found from the data. A hard-coded one is wrong the first time the data changes and nothing will say so.

## Writing the title

The title is the most valuable text on a chart and the most often wasted.

Three levels, in growing usefulness:

**Descriptive** &mdash; "Sales by month". Names the vars the axes already name. Adds nothing.

**exact** &mdash; "Monthly sales, 2024, all regions". Adds scope. This The reader needs. Belongs in a subtitle rather than the headline.

**Assertive** &mdash; "Sales peaked in August, then fell 22%". States what the chart shows. The reader knows what to look for and can check the claim against the picture.

The assertive form has a discipline attached: having written it, you've to make sure the chart supports it. That is a handy constraint. It often changes the chart. Highlighting August, annotating the fall, dropping series that aren't part of the claim.

Where a chart truly has no single finding. An exploratory panel, a link figure. The exact form is right. The lack of a claim is itself helpful.

## Subtitles and source notes

Two pieces of text that most charts want and matplotlib has no method for.

A **subtitle** carries the scope that the headline title leaves out. The period, the units, the group. Placed just under the title in axes coords, smaller and grey:

```python
ax.text(0, 1.02, "Monthly, 2024, all regions", transform=ax.transAxes,
        fontsize=9, color="0.4", va="bottom")
```

A **source note** goes at the bottom of the figure, smaller still:

```python
fig.text(0, 0, "Source: internal sales data, extracted 2024-09-01",
         fontsize=8, color="0.5", va="bottom")
```

Both are two lines and both are what makes a chart usable by someone who didn't make it. The source note in given is the gap between a chart that can be checked and one that has to be taken on trust.

## One more thing

`ax.legend(labelcolor="linecolor")` colours each legend label to match its line. This Drops the need for the swatch fully and reads well with `handlelength=0`.

It's a compact treatment that sits between a full legend and direct labelling. Works when the lines settle so that end labels would share.

## The short version

Text is what turns a picture of numbers into a thing someone else can act on. Units are the part most often left out.

A legend is link material that the reader consults again and again. A direct label is read once. Where the lines end apart, the direct label wins. It costs two lines of `text`.

## Reading the code back

The text on a chart is written in a fixed order. The title says what was found, the axis labels say what the numbers are. The legend or the direct labels say which series is which. Written in that order, the chart is full. Written in any other, a thing is often missing. The most common omission is units. The most common redundancy is a title that repeats the axis names.
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
intro: Controlling what the axis shows and how it's written.

## Limits

`ax.set_xlim(a, b)` and `ax.set_ylim(a, b)` set the visible range.

By default matplotlib picks limits slightly **wider** than the data. Points don't sit on the frame. `ax.margins(0)` drops that padding. `ax.margins(x=0.1, y=0.2)` sets it per axis as a fraction.

Passing the limits in reverse order reverses the axis: `ax.set_ylim(100, 0)` puts 100 at the bottom. That is how you draw a rank chart where 1 is best, or a depth profile where zero is the surface.

Two cautions. Setting limits **hides** data rather than dropping it. Points outside the range are still there, still counted by anything that reads the data, just not visible. And on a bar chart, changing the y limit away from zero misstates the values. This Is the subject of its own module.

`ax.autoscale()` returns to auto, and `ax.set_xlim(left=0)` sets one end and leaves the other auto.

## Ticks

`ax.set_xticks(spots)` decides where the ticks go. `ax.set_xticklabels(labels)` decides what they say.

**Setting labels without setting spots is the classic bug.** matplotlib chooses its own spots based on the current view. `set_xticklabels` simply renames what ticks happen to exist. Change the data and the labels stay put, now attached to other values. The symptom is a chart where the labels are subtly wrong and nothing errored.

Always set spots first, or pass both together: `ax.set_xticks(pos, labels)`.

For auto but controlled ticks, `matplotlib.ticker` has locators: `MaxNLocator(5)` for at most five ticks, `MultipleLocator(0.25)` for each quarter, `LogLocator` for log axes.

`ax.tick_params(axis="x", rotation=45, labelsize=9)` handles rotation and size. This Is the usual fix for crowded group labels. Though `barh` is often the better fix.

## Formatters

A formatter changes how a tick value is **written** without changing the value.

The default for large numbers uses a shared offset. A small `1e6` in the corner. Which readers routinely miss. A chart of millions gets read as a chart of single digits.

`FuncFormatter(lambda v, pos: "%.1fM" % (v / 1e6))` puts the unit on each label. The function receives the value and the tick spot and returns a string.

The ready-made ones cover most needs: `PercentFormatter`, `StrMethodFormatter("{x:,.0f}")` for thousands separators, `EngFormatter` for SI prefixes, `FormatStrFormatter("%.2f")`.

`ax.ticklabel_format(style="plain")` is the quick way to switch off scientific form fully.

## Scales

`ax.set_yscale("log")` is the one that changes what a chart can show.

Data spanning orders of magnitude. Groups, prices, counts, anything growing fast &mdash; is unreadable on a linear axis. The small values are pressed against zero and only the largest is visible. On a log axis they split. Steep growth turns a straight line. This Is diagnostic in itself.

Two things to know. Log needs **plus** values. Zeros and negatives are dropped without an error. A series that touches zero loses those points silently. And a log axis must be labelled as such. A reader who assumes linear will misread each distance on it.

`"symlog"` is logarithmic away from zero and linear within a band around it, set by `linthresh`. It handles data that crosses zero, at the cost of a scale that changes character partway along. Which needs showing to the reader.

`"logit"` suits proportions, stretching the ends near 0 and 1.

## Grids and spines

A grid helps when someone will read values off the chart. Is decoration when they won't.

When it does help, a faint grid on one axis is often enough: `ax.grid(True, axis="y", alpha=0.4)`. A full dark grid competes with the data for focus.

`ax.set_axisbelow(True)` draws it behind the data. This Is most times what you want and isn't always the default in a given style.

The **spines** are the four lines around the plot. The top and right ones enclose the area and carry no data:

```python
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
```

Two lines, and the chart at once looks less like a default. It's the highest ratio of visual gain to effort in matplotlib. This Is why nearly each published-looking style does it.

`ax.spines["left"].set_position(("outward", 10))` detaches the left spines slightly. This Is a further small refinement.

## Minor ticks

`ax.minorticks_on()` adds untagged ticks between the major ones, and `AutoMinorLocator(5)` sets how many.

They give a sense of scale without adding labels. This Is handy on a log axis where the spacing between decades isn't linear. On any chart where the reader will guess mid values.

`ax.grid(which="minor", alpha=0.15)` draws a fainter grid at the minor ticks, giving two levels of link. That is common on engineering charts and often too much for a presentation.

## Tick direction and appearance

`ax.tick_params` controls all about ticks in one call:

```python
ax.tick_params(axis="both", direction="in", length=4,
               labelsize=9, colors="0.3")
```

`direction="in"` points the marks inward. This Many publication styles prefer because it keeps the outer margin clean.

`which="both"` applies to major and minor together.

`top=False, right=False` drops ticks from the spines you've hidden. Worth doing. Hiding a spine doesn't drop its ticks and leaving them makes marks floating in space.

## Formatting money, percentages and dates

The three formatters that come up most:

```python
from matplotlib.ticker import PercentFormatter, StrMethodFormatter, FuncFormatter

ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"£{v/1000:.0f}k"))
```

`PercentFormatter(xmax=1)` treats the data as fractions. `xmax=100` treats it as already-percentages. Getting that backwards times all by a hundred. The chart still looks plausible.

The thousands separator from `StrMethodFormatter("{x:,.0f}")` is a small change that makes large numbers much faster to read.

## Symmetric limits

For diverging data, limits should often be even so zero sits in the middle:

```python
lim = max(abs(y.min()), abs(y.max()))
ax.set_ylim(-lim, lim)
```

Without it, a series ranging from &minus;2 to +8 puts zero a fifth of the way up. The visual centre of the chart is +3. Which reads as the neutral point though it isn't.

The same thinking applies to diverging colormaps, and for the same reason.

## Shared limits across charts

Two charts checked side by side must share their limits, whether or not they're subplots of one figure.

Within a figure, `sharey=True` does it. Across figures, find the range once and apply it to both:

```python
lim = (0, max(a.max(), b.max()) * 1.05)
```

This is the same class of error as unshared subplots and unshared colour scales. The layout invites a compare the axes don't support. It's easy to miss because each chart is on their own correct.

## Tick density

The right number of ticks is fewer than the default often.

Five to eight labelled ticks on an axis is comfortable. Twelve is crowded. The reader isn't using them all.

`MaxNLocator(6)` caps the count while keeping the spots on round numbers. This Is often better than choosing spots by hand because it adapts when the data changes.

`MultipleLocator(25)` forces a fixed interval. This Is right when the interval has meaning. Quarters, decades, standard bin widths.

For a cat axis, each group needs a tick. If there are too many for the labels to fit, the answer is a other chart rather than smaller text.

## Scales and honesty

A log axis changes what each distance on the chart means. A reader who doesn't notice will misread each compare on it.

Three things make it safe:

**Say so in the axis label** &mdash; "Group (log scale)".

**Use round decade ticks**, so the labels themselves announce the scale: 1, 10, 100, 1000.

**Consider whether the linear version answers the question.** A log scale is right when the data spans orders of magnitude or when scaled change is the subject. It's wrong when abs differences are what matter.

The same applies to any non-linear scale. The chart isn't dishonest. It depends on the reader noticing. The labelling is what makes them notice.

## Ticks that carry meaning

Tick spots are an editorial choice, not a formatting detail.

Ticks at 0, 25, 50, 75, 100 say the scale is a percentage of a thing. Ticks at 0, 20, 40, 60, 80, 100 say the same range is being read in twenties. Ticks at the actual data boundaries. The min, the median, the max. Say a thing else again.

Three patterns are worth knowing.

**Round numbers**, which is the default action and right for most smooth scales.

**Real values** &mdash; a target, a threshold, a previous year's figure &mdash; placed by name so the reader can see where the data sits scaled to them. `ax.set_yticks(list(ax.get_yticks()) + [target])` adds one without losing the rest.

**Only the endpoints**, which is a minimalist treatment that works when the shape matters and precise values don't: `ax.set_yticks([y.min(), y.max()])`.

The last one is worth trying on a chart that feels cluttered. Most charts have more ticks than anyone uses. Each one is a small piece of visual noise competing with the data.

## In summary

Limits control what is visible and hide what isn't, silently.

matplotlib adds a 5% margin by default. This Is right until the data should reach the edge.

`set_xticks` decides spots and `set_xticklabels` the text. Setting labels without spots attaches them to what ticks happen to exist. A bug that makes a plausible, wrong chart.

Formatters change how numbers read. This Matters most for large values that else get a `1e6` offset no one notices.

A log scale makes steep growth a straight line and drops zeros without a word. It must be labelled as logarithmic or each distance on it's misread.

And the top and right spines carry no data. Dropping them is the cheapest gain matplotlib offers.

## Limits that adapt

Hard-coded limits are correct until the data changes. This For any chart regenerated regularly is a matter of time.

Three patterns that adapt.

**Anchor one end.** `ax.set_ylim(bottom=0)` fixes zero and lets the top follow the data. Right for anything where zero is real.

**Pad proportionally.** `ax.margins(y=0.15)` leaves headroom as a fraction rather than a fixed amount. Annotations near the top still fit when the values grow.

**Find from the data.** `lim = max(abs(y.min()), abs(y.max()))` for a even range around zero.

The one to avoid is `set_ylim(0, 100)` on a chart whose data will change. When a value exceeds 100 the bar is silently clipped and nothing shows it.

Where a fixed range is truly wanted. Comparability across a series of charts. An assertion that the data fits inside it's worth the line.

## One more thing

`ax.invert_yaxis()` reverses an axis after the fact. This Is more readable than passing the limits backwards when the limits are else auto.

It's the usual way to draw a ranked list with spot 1 at the top. A depth or pressure profile where the surface is at the top. Both cases where the rule of the domain runs opposite to the axis default.

## The short version

Ticks and limits are where a chart quietly decides what the reader can see and how they read it.

Most charts have more ticks than anyone uses, a margin they didn't choose. A top and right spine carrying no data. Dropping the excess isn't decoration. It's what leaves the data as the most prominent thing on the chart.

## Reading the code back

Limits, ticks and scale are three split choices that are often left to defaults together. Each has a case for being set. Limits when the data should reach the edge or a baseline matters, ticks when the default count is more than anyone will read. Scale when the data spans orders of magnitude. Setting all three on purpose on a chart that matters takes four lines and changes how much work the reader has to do.
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
intro: a few axes on one figure.

## The grid

`fig, axes = plt.subplots(2, 3)` creates a figure with six axes and returns them as a NumPy array.

`axes[0, 2]` is the top-right panel. `axes.flat` iterates in reading order. This Is what you want when the panels match to a flat list of groups:

```python
for ax, name in zip(axes.flat, names):
    ...
```

`zip` stops at the shorter of the two. A grid with more cells than data leaves the extras blank. Visible. Often worth dropping with `ax.drop()` or hiding with `ax.axis("off")`.

## The shape surprise

The returned array's shape isn't always what code expects.

`subplots(2, 3)` gives a `(2, 3)` array. `subplots(1, 3)` gives a **1-D** array of three. `subplots(1, 1)` gives a single `Axes`, not an array at all. Which is what makes `fig, ax = plt.subplots()` work.

That is convenient interactively and awkward in a function that takes the grid size as a param. `axes[0, 1]` fails on the 1-D case.

`squeeze=False` forces a 2-D array always. In reusable code it's the right default, and it costs one arg.

## Sharing

`sharex=True` and `sharey=True` make the panels use the same limits.

This isn't a cosmetic setting. Without it, each panel autoscales to its own data. A bar that reaches the top of one panel may represent a smaller number than a shorter bar in the panel beside it. The grid looks like a compare and isn't one.

Sharing also hides the inner tick labels. This Drops a great deal of repetition from a grid.

`sharex="col"` and `sharey="row"` share within columns or rows. This Suits a mat where each row is a other quantity.

The trade-off: with shared axes, a panel whose data occupies a small part of the shared range is compressed. When the panels truly have other scales, small multiples with split axes and clearly labelled ranges are more honest. But then the reader must be told not to compare heights right.

## Uneven grids

`fig.add_gridspec(rows, cols)` creates a grid you then slice:

```python
gs = fig.add_gridspec(2, 3, height_ratios=[2, 1])
big = fig.add_subplot(gs[0, :])     # whole top row
small = fig.add_subplot(gs[1, 0])   # bottom left
```

`height_ratios` and `width_ratios` make rows and columns other sizes. This Is how you give a main chart more space than the supporting ones.

## subplot_mosaic

`plt.subplot_mosaic` takes a **picture** of the layout:

```python
fig, axd = plt.subplot_mosaic("""
    AAB
    CCB
""")
```

Repeated letters span cells, and the result is a dict keyed by the letters. `axd["A"]` is far easier to follow than `gs[0, :2]`, and the layout is visible in the source rather than coded in slice math.

A `.` in the string leaves a cell empty.

It's the most readable way to build an uneven layout. Worth preferring wherever it fits.

## Layout

Labels, titles and tick text are drawn outside the axes. Matplotlib doesn't account for them when placing panels. The result is shared labels, or a title running off the top.

Two methods fix it.

`fig.tight_layout()` is called after all is drawn and adjusts spacing once. It's simple and works for most cases. It can be confused by artists added later. It doesn't handle colorbars above all well.

`constrained_layout=True` is set when the figure is created and keeps adjusting as things are added. It handles colorbars, suptitles and legends outside the axes better. It's the one to reach for on a complex figure.

Neither is on by default. `fig.subplots_adjust(hspace=..., wspace=...)` sets spacing manually when you want precise control.

The symptom of missing layout management is a figure that looks acceptable on screen and comes out cropped when saved. Because `savefig` uses the figure's declared size, not what the screen happened to show. `bbox_inches="tight"` on `savefig` is the other half of that fix.

## Removing unused panels

A 3&times;4 grid holding ten charts leaves two empty boxes with ticks and spines. This Look like a mistake.

`ax.drop()` deletes the axes fully. `ax.axis("off")` keeps it but hides all. This Preserves the spacing. handy when the grid should stay rectangular.

```python
for ax in axes.flat[len(items):]:
    ax.remove()
```

The empty cell is also a fair place for a legend or a note, using `ax.axis("off")` and `ax.legend(...)` with handles gathered from the other panels.

## Titles and labels across a grid

With shared axes, per-panel axis labels are repetition. `fig.supxlabel` and `fig.supylabel` label the grid once.

Panel titles remain handy and should be small. They're finding the panel, not heading a chart. `fontsize=9` and `loc="left"` reads well.

For a formal figure, lettering the panels is standard:

```python
for letter, ax in zip("abcdef", axes.flat):
    ax.text(0.02, 0.95, letter, transform=ax.transAxes,
            fontweight="bold", va="top")
```

Axes coords, so the letter stays in the corner even so of the data.

## Iterating in the right order

`axes.flat` iterates row by row. This Matches how the panels will be read.

`zip(axes.flat, items)` pairs them and stops at the shorter. This Is convenient and silently drops items if the grid is too small. Asserting the sizes match is one line and blocks a chart quietly missing a group:

```python
assert len(items) <= axes.size
```

For a grid indexed by two vars, `axes[i, j]` with clear loops is clearer than flattening. The spot then carries meaning.

## When not to use subplots

Small multiples are great for checking the **same** reading across groups.

They're poor when the panels show other quantities on other scales. The shared layout implies a comparability that the axes don't support. Four panels showing revenue, headcount, delay and satisfaction are four charts that happen to be adjacent. Separating them. Or at least not sharing axes and labelling each scale clearly &mdash; is more honest.

They're also poor past about twelve panels. Here Each turns too small to read. At that point the answer is often to reduce what is being shown, not to shrink the panels further.

## Figure size for a grid

The figure size should scale with the grid. A 2&times;3 grid in the same six inches as a single chart gives panels a third the size. Text that was comfortable turns proportionally huge.

A fair rule is to keep the per-panel size roughly constant:

```python
fig, axes = plt.subplots(nrows, ncols, figsize=(3.2 * ncols, 2.4 * nrows))
```

Then adding a row makes the figure taller rather than making all smaller.

## Shared axes in detail

`sharex=True` links the axes objects. So Changing the limits on one changes all of them. Which is convenient interactively and at times surprising in a script. Here An autoscale on one panel silently rescales the rest.

`ax.label_outer()` hides the tick labels on inner panels. This `sharex`/`sharey` do on its own but which is needed when you build the grid by hand.

`sharex="col"` links within columns only. This Suits a grid where columns are other quantities and rows are groups.

To share later rather than at creation, `ax2.sharex(ax1)` exists. The older `ax2.get_shared_x_axes().join(ax1, ax2)` appears in existing code.

## A grid that reads

The details that make a grid of panels look seen as:

**steady panel titles**, small and left-aligned.

**One axis label per grid**, via `supxlabel`/`supylabel`.

**Shared limits**, so the compare is valid.

**A steady colour** across panels for the same series, or a single colour if each panel is one thing.

**Empty cells removed**, not left as empty boxes.

**A common annotation style** &mdash; if one panel has a link line, they all should.

On their own trivial. Together they're the gap between a grid that reads as one figure and one that reads as a few charts stuck together.

## Building a grid programmatically

Most real grids are made from data rather than written out. A few patterns make that robust.

Find the grid size from the number of items:

```python
n = len(items)
ncols = 3
nrows = math.ceil(n / ncols)
fig, axes = plt.subplots(nrows, ncols, figsize=(3.2 * ncols, 2.4 * nrows),
                         sharex=True, sharey=True, squeeze=False)
```

`squeeze=False` promises a 2-D array what the numbers work out to, so `axes.flat` always behaves.

Then pair, draw, and clean up the remainder:

```python
for ax, item in zip(axes.flat, items):
    draw(ax, item)
for ax in axes.flat[n:]:
    ax.remove()
```

The figure size scaling with the grid is what keeps the text a constant size scaled to each panel, rather than shrinking as rows are added.

And because `zip` stops at the shorter arg, asserting `n <= axes.size` is worth the line. Else a grid that is too small silently drops groups.

## In summary

`subplots(r, c)` returns an array. `axes.flat` iterates in reading order. `squeeze=False` makes the shape predictable.

`sharex` and `sharey` are what turn a grid into a compare. Without them each panel scales to its own data and the heights mean other things.

`gridspec` and `subplot_mosaic` handle uneven layouts. The mosaic string is far easier to read than slice math.

`tight_layout` or `constrained_layout` stop labels colliding. A figure that saves cropped is often missing one.

Label the grid once with `supxlabel` rather than each panel, drop unused cells. Scale the figure size with the number of panels.

And small multiples are the right answer far more often than one crowded chart. They're the display that makes many checks possible at once.

## Grids in practice

Three layouts cover nearly all real grids.

**A row of two or three**, for a before-and-after or a small set of related views. Wide, shared y, one shared axis label.

**A square-ish grid**, for small multiples over a cat var. Shared both ways, panel titles small, figure size scaled by the grid.

**A main chart plus supporting ones**, built with `subplot_mosaic` or `gridspec` and unequal ratios. The main panel gets two-thirds of the height and the supporting row the rest.

The fourth layout &mdash; a grid of unrelated charts &mdash; is common and often a mistake. Panels in a grid are read as close. Four charts of other quantities on other scales are four figures that happen to be adjacent. Either give them split figures, or make the gap clear with clearly labelled split scales and no shared axes.

The question that decides it: would a reader be right to compare the panels to each other? If yes, share the axes. If no, they probably shouldn't be in a grid.

## Sharing a legend

A grid where each panel repeats the same legend wastes space and focus.

One figure-level legend is the fix:

```python
handles, labels = axes.flat[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=len(labels))
fig.subplots_adjust(bottom=0.15)
```

Handles are taken from any one panel. They're all the same series. `fig.legend` places it scaled to the figure rather than an axes.

Room has to be made for it. This `constrained_layout` does on its own and `subplots_adjust` does by name.

The same applies to a colorbar: one bar serving the whole grid. This Also enforces the shared scale the panels need to be close.

## One more thing

`fig.align_ylabels()` lines up the y-axis labels across a column of panels. This Else sit at other distances from the axes based on how wide each panel's tick labels are.

It's a small alignment that is very visible once noticed. `align_xlabels` does the same flatly. On a grid where the panels have other value ranges, it's the gap between a column of labels that reads as one and one that looks ragged.

## The short version

A grid is a claim that the panels belong together. Sharing the axes is what makes the claim true. Labelling the grid once rather than each panel is what makes it read as one figure.

The three things that most often go wrong are an unshared y axis making incomparable panels look close, a figure size that didn't grow with the grid so all is cramped. Empty cells left as bare boxes. All three are one line each.

## Reading the code back

A grid is created in one call and finished in three. Share the axes, label the grid once. Drop what is unused. The figure size should be found from the grid rather than fixed. Adding a row makes the figure taller instead of making each panel smaller. Those four choices are what split a grid that reads as one figure from a few charts that happen to be adjacent.
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
intro: Naming colours, the cycle, and picking a colormap that doesn't invent structure.

## Naming a colour

matplotlib accepts a few notations wherever a colour is wanted:

A **CSS name**: `"crimson"`, `"steelblue"`, `"rebeccapurple"`.

**Hex**: `"#4c72b0"`, with an optional alpha suffix.

A **cycle link**: `"C0"` through `"C9"`, meaning the nth colour of the current property cycle. Using these keeps a figure steady when the style changes.

A **grey level as a string**: `"0.55"`. The quotes matter. The bare number `0.55` isn't a colour.

An **RGB or RGBA tuple** of floats from 0 to 1.

Single letters `"r"`, `"g"`, `"b"`, `"k"` also work. Are the ones the format-string shorthand uses.

## The property cycle

Each axes has a **property cycle** that supplies the colour for successive plots. The default has ten colours and then repeats.

`ax.set_prop_cycle(cycler(color=[...]))` replaces it for one axes. `plt.rcParams["axes.prop_cycle"]` replaces it globally. This Is how you apply a house palette to a whole script.

A `cycler` can carry more than colour:

```python
cycler(color=palette) + cycler(linestyle=["-", "--", ":", "-."])
```

`+` pairs them elementwise, so the first series is the first colour and the first linestyle. That single change makes each chart in a script live being printed in greyscale. This Is worth more than it costs.

`*` gives the outer product instead, cycling each mix.

## Three kinds of colormap

The choice of colormap is a statement about the data. The wrong one asserts a thing false.

**Sequential** &mdash; `viridis`, `plasma`, `Blues` &mdash; runs from low to high in one direction. Use for magnitudes: counts, temperatures, concentrations.

**Diverging** &mdash; `coolwarm`, `RdBu`, `BrBG` &mdash; has two directions from a neutral centre. Use when there's a **real midpoint**. Zero, an mean, a baseline. Applying one to data with no natural centre invents a boundary in the middle of the range.

**Qualitative** &mdash; `tab10`, `Set2` &mdash; is a set of distinct hues with no sorting. Use for groups. Using a sequential map for groups implies an order that doesn't exist.

**Cyclic** &mdash; `twilight`, `hsv` &mdash; wraps around, for angles and phases.

## Why jet is a problem

`jet` was the default in older tools and still appears all over. It's a bad choice, for a reason that is measurable rather than aesthetic.

A good colormap is **perceptually uniform**: equal steps in the data look like equal steps in colour. `viridis` was designed for this. Its brightness grows steadily from one end to the other.

`jet` doesn't. Its brightness rises, falls and rises again, with a bright band in the middle. The eye reads a sharp brightness change as a boundary. `jet` shows edges and structure where the data is just right smooth. And hides real grads in the flat regions.

It also merges when converted to greyscale. Other values map to the same brightness.

The fourth editor plots the brightness of both. This Makes the gap visible rather than assertable.

## Colorbars

A colour-mapped plot without a colorbar is decoration: the reader can see that values differ and not by how much.

`fig.colorbar(mappable, ax=ax)` needs the object returned by the drawing call. `imshow`, `scatter`, `pcolormesh`, `contourf`. That is why those return values are captured here.

`label=` names the quantity. This Is as key as it's on an axis. `shrink` and `pad` adjust size and spacing. `orientation="flat"` puts it below.

For a grid of subplots, `fig.colorbar(im, ax=axes.ravel().tolist())` makes one bar serve all panels. This Is right when they share a scale. And they should, or the panels aren't close.

## Accessibility

Around 8% of men and 0.5% of women have some form of colour vision deficiency, most often trouble separating red from green.

Three habits cover most of it:

**Avoid red against green** as the main gap. Blue against orange is distinguishable for almost all.

**Vary a second channel** &mdash; linestyle, marker, or spot &mdash; so colour is reinforcing rather than carrying the meaning alone.

**Use `viridis` and friends** for smooth data. They were designed to remain monotonic in brightness under common deficiencies. This Is why they work in greyscale too.

The greyscale test is a good proxy for all of it. Print the chart in black and white. If it's still readable, it will live most viewing rules.

## Transparency

`alpha` runs from 0 to 1 and can be set per artist or baked into a colour as a fourth channel.

Three places it earns its keep: showing density in an overplotted scatter, letting a shaded band sit under a line without hiding it. De-emphasising context series without changing their colour.

Two cautions. Alpha compounds &mdash; ten shared shapes at 0.1 are opaque where they all coincide. This Is just the density signal you want in a scatter and an unwanted colour shift elsewhere. And transparency is lost when a figure is flattened onto a background. A chart designed with alpha over white looks other over grey.

## Named palettes

matplotlib ships the `tab10` and `tab20` qualitative sets. `plt.get_cmap("tab10").colors` gives the list for use in a cycler.

For cat work, palettes designed for colour-vision deficiency are worth preferring. The Okabe&ndash;Ito set is eight colours chosen to remain distinguishable under the common deficiencies. It's a plain list of hex codes you can paste into a cycler.

For sequential data, the perceptually uniform family is `viridis`, `plasma`, `inferno`, `magma` and `cividis`. `cividis` is designed namely to look the same to viewers with and without colour-vision deficiency.

Appending `_r` to any colormap name reverses it: `viridis_r`.

## Discrete colour from a continuous map

Sampling a smooth colormap gives a graded set for sorted groups:

```python
cmap = plt.get_cmap("viridis")
colors = [cmap(i / (n - 1)) for i in range(n)]
```

That is right when the groups have an **order**. Age bands, quartiles, years. Because the colour then carries the sorting.

It's wrong for unordered groups. Here A qualitative palette should be used instead. It's a common way to imply a sequence that doesn't exist.

`BoundaryNorm` does the same thing for a mapped plot, banding a smooth scale into discrete steps with a colorbar that shows the boundaries.

## Colorbar placement

The default steals space from the axes it's attached to. This Shrinks that panel and misaligns it with its neighbours.

`fig.colorbar(im, ax=axes.ravel().tolist())` spans a few panels with one bar. This Is right when they share a scale.

`shrink=0.8` and `aspect=30` adjust its proportions. `pad` sets the gap. `location="bottom"` moves it.

For precise control, `fig.add_axes([left, bottom, width, height])` creates a dedicated axes for it in figure coords. This Is how you get a colorbar that lines up just with a grid.

## Backgrounds

`fig.patch` is the figure background and `ax.patch` the axes background, and they're split.

`ax.set_facecolor("#f7f7f7")` gives the plotting area a light tint. This Some styles use to make a white grid readable.

For a dark theme, both need setting along with the text, tick and spine colours. Which is just what the `dark_background` style does. A reason to use a style rather than setting six things by hand.

## Building a palette

A palette for a project needs fewer colours than people expect.

**One** colour, for charts with a single series. Most charts.

**Two**, for a compare or a before-and-after.

**A greyscale plus one accent**, for highlighting one series among many. This covers more cases than any multi-colour palette.

**Five or six**, for truly cat work, drawn from a set designed for the purpose.

Beyond about six, colour stops distinguishing well. The answer is small multiples rather than more hues.

Add a grey for context elements, a light grey for gridlines. A dark grey rather than black for text. That is a full house palette.

## Testing a colour scheme

Three checks, none of which needs a tool.

**Greyscale.** Convert the figure to greyscale and see whether the series are still distinguishable. If they aren't, luminance isn't varying and the chart depends fully on hue.

**Small size.** View the figure at the size it will really be seen. Colours that split at full screen often don't at thumbnail size.

**Print.** A projector and a printer both compress the range. Colours that differ on a monitor often don't live either.

Passing all three often means the encoding is robust. Failing any of them is fixed the same way: vary luminance, and vary a second channel.

## Colour with meaning

The strongest use of colour is when it codes a thing the reader already understands.

**Semantic colours** &mdash; red for loss, green for gain, a brand colour for one product &mdash; are read without a legend because the meaning arrives with the hue. They're also culturally exact. The red/green pairing is the worst possible choice for colour-blind readers. The rule has to be weighed against accessibility.

**Sequential colour for an sorted var**. Darker for more. Is read right with almost no instruction.

**One accent against grey** is the most solid of all. It says "this one" and nothing else.

The weakest use is colour as decoration: seven groups in seven hues because the palette had seven. That asks the reader to learn an any mapping and consult it again and again. It's often a sign the chart should be small multiples.

The test is whether dropping the colour destroys the chart's meaning or only its appearance. If the former, the colour is doing work and should be chosen carefully. If the latter, it can be simplified away.

## In summary

Colours accept names, hex, `C0`-style cycle links, greys as strings, and RGB tuples.

The property cycle supplies distinct colours on its own. A cycler can vary linestyle alongside colour so the chart lives greyscale.

Colormaps come in three kinds, and using the wrong kind asserts a thing false. Sequential for magnitude, diverging around a real centre, qualitative for unordered groups.

`jet` fails measurably rather than aesthetically. Its brightness isn't monotonic. It shows edges the data doesn't have.

A colour-mapped plot needs a colorbar, with a label. Two such plots need a shared scale.

And roughly one man in twelve can't split red from green. This Is why a second channel is worth varying and why greyscale is a good proxy test for the whole question.

## A closing note

Colour is the most over-used channel in charting and the most rewarding to use sparingly.

The strongest charts often have one colour, or one colour against grey. Colour that codes a var earns its place. Colour that sets apart seven groups no one needs to set apart doesn't.

The technical points matter too. Visual uniformity, the right kind of colormap, a centred diverging scale, a colorbar that says what the colours mean &mdash; and they're all in service of the same thing. The reader should be able to work out what a colour means without being told twice.

The greyscale test remains the quickest check on all of it.

## The short version

Colour is the most over-used channel in charting and the most rewarding to use sparingly.

One accent against grey beats a seven-hue palette in almost each case. The greyscale test is the quickest check on whether the encoding lives contact with the real world.

## Reading the code back

Colour choices are made once for a project and applied through a cycler, not chosen per chart. A palette of five or six for groups, a sequential map for magnitudes, a diverging one for data with a real centre. A grey for context is a full set. Anything beyond that is often a chart that should have been small multiples.
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
intro: Text, arrows and link lines - saying what the chart is for.

## text

`ax.text(x, y, "some words")` places text at a point in **data coords**.

`ha` (flat alignment) and `va` (vertical alignment) decide which part of the text sits at that point: `ha="center"` centres it, `va="bottom"` puts its bottom edge there. Without them, text starts at the point and runs to the right. This Is rarely where you want it.

Because the coords are data units, the text moves when the axis limits change. Correct for labelling a data point, wrong for a caption.

## annotate

`ax.annotate` is `text` with two spots and an optional arrow:

```python
ax.annotate("lowest point",
            xy=(x, y),               # the point
            xytext=(x + 1, y - 0.3), # the label
            arrowprops=dict(arrowstyle="->"))
```

Omit `arrowprops` and it's text with an offset. Include it and matplotlib draws a connector.

`arrowstyle` takes `"->"`, `"-|>"`, `"fancy"`, `"wedge"` and others. `connectionstyle="arc3,rad=0.3"` curves the arrow. This Is how you route it around the data rather than through it.

`textcoords="offset points"` with `xytext=(dx, dy)` spots the label a fixed number of **points** from the target, instead of at another data coord. That is often what you want. The gap stays constant when the limits change. Here A data-coord offset would grow or shrink.

## Reference lines

`ax.axhline(value)` draws a flat line across the whole axes. `axvline` the vertical equal. They span the full width even so of the current limits. Keep doing so if the limits change.

`axhspan(lo, hi)` and `axvspan` shade a band between two values.

These are better than plotting the line yourself. `ax.plot([0, 40], [mean, mean])` hard-codes the x range. Stops spanning the axes as soon as the data grows.

Common uses: a target or threshold, a mean, a standard-deviation band, the date of a known event.

Label them &mdash; either through `label=` and a legend, or with text at one end &mdash; because an unexplained line is a question rather than an answer.

## Coordinate systems

Three systems, and choosing right is what makes annotations live changes to the data.

**Data coords** (the default) &mdash; for anything attached to a exact value.

**Axes coords** &mdash; `transform=ax.transAxes`, running 0 to 1 across the axes. A label at `(0.02, 0.95)` sits just inside the top-left corner what the data is. This is right for a panel letter, a note, a sample size.

**Figure coords** &mdash; `fig.text(0.5, 0.01, ...)`, running 0 to 1 across the whole figure. Right for a source note or a caption under a grid of panels.

The mistake is putting a corner label in data coords. It looks correct until the data changes, then drifts into the middle of the plot or off the edge fully.

## Shading regions

`fill_between(x, y1, y2)` fills between two curves, or between a curve and a constant.

`where=rule` restricts it to the parts where a boolean array is true. Shading only where a series is above its mean, or above a threshold.

Add `interpolate=True` and the shading stops just at the crossing point. Without it, it stops at the nearest data point, leaving a small notch. On coarsely sampled data that notch is visible and looks like a mistake.

`fill_between` is also how you draw a trust band, with the upper and lower bounds as the two curves and `alpha` around 0.2.

## Restraint

This is the part that matters most and is hardest to apply.

each annotation competes with the data for focus. A chart with twelve labelled points has twelve things to read and no message. A chart with one highlighted point and one label has a message.

The handy question is what the reader should take away. Then annotating **that** and nothing else. Greying the rest of the series and colouring the highlighted part is often more good than adding an arrow. It directs focus without adding ink.

If a few things truly need pointing out, that is often a sign the chart is trying to say more than one thing. Two charts would each say theirs more clearly.

## Boxes behind text

`bbox=` puts a patch behind a label. This Is how you keep text readable over busy data:

```python
ax.text(x, y, "peak", bbox=dict(boxstyle="round,pad=0.3",
                                facecolor="white", alpha=0.8, edgecolor="none"))
```

`boxstyle` takes `"round"`, `"square"`, `"larrow"` and others, with `pad` controlling the margin.

A white box at 80% alpha is the standard treatment for a label that must sit over a line or a filled region. Without it, text over data is legible in the draft and unreadable once the data changes.

## Annotating a specific series

Text placed at the end of a line is the most handy annotation there's. The spot should come from the data:

```python
ax.text(x[-1], y[-1], f"  {name}", va="center", color=line.get_color())
```

Taking the colour from the artist ties the label to its line without repeating a colour constant. It keeps working when the cycle changes.

The leading spaces are a crude but good offset. `annotate` with `textcoords="offset points"` is the tidier version.

Leave room for the labels with `ax.set_xlim(right=x.max() * 1.15)`, or they run off the edge.

## Arrows

`arrowprops` is a dict, and the two handy spellings are:

`dict(arrowstyle="->")` &mdash; the modern form, with styles like `"->"`, `"-|>"`, `"fancy"`.

`dict(facecolor="black", shrink=0.05)` &mdash; the older form. This Makes a filled arrow.

`connectionstyle="arc3,rad=0.2"` curves the connector. A slight curve often reads better than a straight line. It doesn't look like part of the data.

`shrinkA` and `shrinkB` pull the ends back from the text and the target. This Stops the arrowhead touching the point it's finding.

## Guides and callouts

A few patterns recur often enough to be worth naming.

**A threshold with a label at the end**: `axhline` plus text at the right edge in axes coordinates for x and data coordinates for y &mdash; `ax.text(1.01, value, "target", transform=ax.get_yaxis_transform())`.

**A shaded period with a caption at the top**: `axvspan` plus text at `ax.get_ylim()[1]` with `va="top"`.

**A value callout**: a single marker in a strong colour, plus text offset from it.

`ax.get_yaxis_transform()` is the blended transform used above: x in axes fractions, y in data units. Its counterpart `get_xaxis_transform()` does the reverse. Between them they place edge labels that stay put when the data changes.

## Too much of it

The failure mode of annotation is a chart where all is emphasised. This Is the same as nothing being emphasised.

A handy discipline is to write the sentence the chart is meant to support. Then annotate only what that sentence refers to. If the sentence has two clauses about other things, that is two charts.

## Annotation as editing

The most handy way to think about annotation is as **editing** rather than addition.

A chart shows all in the data equally. Annotation is where you say which part matters. And the strongest form of that is often subtraction, not addition. Greying the context, thinning the lines that aren't the subject, dropping the gridlines that aren't being read.

A highlighted line with a label at its end and all else in grey carries more meaning than the same chart with an arrow and a paragraph of text. The emphasis is in the visual tree rather than in a thing extra to read.

Add annotation when it names a thing the reader couldn't derive. Drop weight from all that isn't it.

## Keeping annotations correct

Annotations placed by hand go stale. The data changes and the coords don't.

Three habits keep them honest:

**Find the spot from the data.** `ax.annotate(..., xy=(x[i], y[i]))` with `i = y.argmax()` follows the peak wherever it moves.

**Find the text from the data.** `f"peak {y.max():.1f}"` can't disagree with the chart.

**Use axes coords for anything not attached to a value.** A corner note in data coords drifts as soon as the limits change.

A hard-coded annotation is correct just once. There's nothing to warn you when it stops being.

## Annotating for different readers

How much annotation a chart needs depends fully on who reads it and how long they've.

**A chart in a presentation** gets one annotation, large, saying the thing the speaker is about to say. all else is removed. The audience has seconds and can't re-read.

**A chart in a report** can carry two or three. The reader controls the pace and can look between the chart and the text.

**A chart in an appendix** may carry none. Its job is to be on hand rather than to argue.

**A chart for yourself** needs none at all.

The common error is annotating a presentation chart like a report chart. Four callouts, a legend, a subtitle and a source line, none of which can be read from the back of a room.

Writing the sentence the chart supports. Then annotating only the words in that sentence, resolves it in each case.

## In summary

`text` places a string at a data coord, with `ha` and `va` deciding which part of it sits there.

`annotate` adds a second spot and an optional arrow. `textcoords="offset points"` keeps the gap constant when the limits change.

`axhline`, `axvline` and the span functions cover thresholds and periods. Stay correct when the data grows.

`transform=ax.transAxes` is for anything not attached to a value. A corner note stays in the corner.

`fill_between(..., where=...)` shades a rule, with `interpolate=True` to stop at the crossing.

And the hardest part is restraint: each annotation competes with the data. A chart with one highlighted point says more than one with twelve labels.

## Text that scales

An annotation sized in points stays the same physical size when the figure changes. This Means it occupies a other fraction of a small figure than a large one.

For a figure that will be made at a few sizes, three options:

**Set font sizes in the style** scaled to a base `font.size`. Changing one value scales all together.

**Find sizes from the figure size**. This Is what a house function can do: `fontsize = 4 + fig.get_size_inches()[0]`.

**Draw at the final size** and avoid the problem. This Is the recommendation all over else in this track.

The failure to avoid is annotating a figure at screen size and then exporting it at a third of that for a doc. Here A comfortable label turns unreadable and an arrow turns a hairline.

Looking at the exported file, at the size it will be seen, is the check that catches all of it.

## One more thing

`ax.annotate` accepts `xycoords` and `textcoords`. So The point being annotated can itself be in axes or figure coords rather than data ones.

That is how you draw an arrow from a corner note to a data point. Text anchored to the corner in axes coords, target in data coords. Which stays correct as the data changes.

## The short version

Annotation is where a chart stops showing and starts saying.

The technique is straightforward. The discipline isn't. One thing pointed out clearly beats five things labelled. Greying the context is often more good than adding an arrow.

## Reading the code back

An annotation has three parts: what is being pointed at. Here The label sits. Which coord system each uses. Getting the third right is what makes the annotation live a change in the data. It's the part most often left to chance. finding both the spot and the text from the data means the chart can't contradict itself.
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
intro: savefig, dpi, and the args that decide whether the file looks like the screen.

## Size and resolution

A figure has a size in **inches** (`figsize`) and a detail in **dots per inch** (`dpi`). The saved image is their product in pixels.

`figsize=(6, 3)` at `dpi=100` gives 600&times;300. At `dpi=200` it gives 1200&times;600.

That much is math. The part that catches people is that **these two aren't the same**:

`figsize=(4, 2), dpi=200` &rarr; 800&times;400
`figsize=(8, 4), dpi=100` &rarr; 800&times;400

Same pixels, other-looking charts. Text is sized in **points**, a physical unit. 10-point text occupies a tenth of an inch either way. On the 4-inch figure that is a large fraction of the width. On the 8-inch one it's half as much.

The rule that follows: choose `figsize` for the **layout**. How big the text should look scaled to the plot. And `dpi` for the **detail**. Then scaling up for a high-detail export changes only sharpness, not proportions.

A common mistake is making a figure bigger to get more detail and finding the text has shrunk scaled to all else.

## bbox_inches

By default `savefig` writes just the declared figure area. Labels, titles and legends drawn outside the axes may fall outside it and be cropped.

`bbox_inches="tight"` recomputes the bounding box to include all drawn. It's the fix for the very common "my y-axis label is missing from the saved file".

Two results: the output dims are no longer just `figsize &times; dpi`. `pad_inches` controls the margin it leaves. If you need an exact pixel size, use layout management instead and leave the bbox alone.

## Formats

**PNG** is raster: a grid of pixels. Right for the web, for slides. Anywhere the display size is known. Small for simple charts.

**PDF** is vector: shapes and text. Scales to any size without blurring, embeds fonts. Is what a journal or a print process wants.

**SVG** is vector and text-based. So It can be edited later in Inkscape or styled with CSS in a browser.

**JPEG** should be avoided for charts: it's lossy in a way that puts artefacts around sharp edges and text. This Is just what a chart is made of.

The trade-off with vector formats is that file size grows with the **number of elements**, not the image dims. A line chart is tiny. A scatter plot of 100,000 points is an huge PDF that may take a viewer minutes to render.

`rasterized=True` on a exact artist stores just that layer as pixels while keeping text and axes as vectors. This Gives a small file with sharp labels.

## Background

The default background is white for both the figure and the axes.

`transparent=True` makes both transparent, so the chart sits on what is behind it. `facecolor="#222"` sets a exact colour.

The catch: transparency changes the background and **not the foreground**. Text, spines and tick labels stay their first dark colour. A transparent figure dropped onto a dark slide has invisible labels. Making a chart for a dark background means changing the text and line colours too. This Is what a dark style sheet does.

## Saving in a loop

The pattern for making many charts:

```python
for group, data in groups:
    fig, ax = plt.subplots()
    ...
    fig.savefig(f"{group}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
```

`plt.close(fig)` is the line people omit. Without it each figure stays open, matplotlib warns after twenty. A loop over a few thousand groups exhausts memory.

For output that goes into a doc, saving as PDF and letting the doc scale it often beats guessing a dpi.

And `savefig` accepts a file-like object and a path. This Is how you write straight into a buffer for a web response or a test. As each editor on this page does. There's no filesystem to write to.

## dpi in three places

`dpi` appears in the figure, in `savefig`, and in rcParams, and they interact.

`plt.subplots(dpi=100)` sets the figure's own dpi. This Affects on-screen size.

`fig.savefig(path, dpi=200)` replaces it for that file.

`rcParams["savefig.dpi"]` sets the default for saving, and defaults to `"figure"`, meaning "use the figure's".

The hands-on result is that a figure looking right on screen can save at a other detail than expected. Passing `dpi` by name at save time drops the question.

Common values: 100 for a quick look, 150&ndash;200 for slides and web, 300 for print, 600 for a journal that asks for it.

## Metadata and reproducibility

`savefig` accepts a `metadata` dict. This For PNG and PDF is written into the file.

Recording the script, the data version and the timestamp there means a chart found later can be traced back:

```python
fig.savefig(path, metadata={"Software": "analysis.py", "Creation Date": stamp})
```

A more visible version is a small caption in figure coords giving the source and date. This Lives the chart being copied into a doc where the file metadata doesn't follow.

## Vector text and fonts

By default, PDF and SVG output stores text as **text**. This Keeps it selectable and searchable. Needs the reader to have the font.

`rcParams["pdf.fonttype"] = 42` embeds the font as TrueType, making the file self-held at the cost of size. Journals often need this. It's the fix when a submitted figure renders in the wrong typeface.

`rcParams["svg.fonttype"] = "none"` does the opposite for SVG, leaving text as text so it can be styled with CSS in a browser. handy for the web, wrong for a doc.

## Saving several formats

A common pattern is one call per format from the same figure:

```python
for ext in ("png", "pdf"):
    fig.savefig(f"{name}.{ext}", dpi=200, bbox_inches="tight")
```

The figure can be saved any number of times. Nothing is consumed. A PNG for the draft and a PDF for the final doc, from one drawing pass.

## Buffers rather than files

`savefig` accepts any file-like object:

```python
buf = io.BytesIO()
fig.savefig(buf, format="png")
```

That is how a chart turns a web response, an email attachment, or a test assertion. And how these pages work. The browser has no filesystem to write into.

`format` is needed when there's no filename to infer it from. This Is the usual first error with this.

## A saving function

For a project making many figures, a small wrapper enforces agreement:

```python
def save(fig, name, formats=("png", "pdf")):
    for ext in formats:
        fig.savefig(f"figures/{name}.{ext}", dpi=200,
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
```

One place to change the dpi, the formats, the background and the padding, and the `close` isn't forgotten.

Adding the source script and a timestamp to the metadata, or as a small caption, makes a figure traceable months later. Which is the gap between a chart that can be updated and one that has to be remade.

## Common saving problems

**Labels cut off** &mdash; missing `bbox_inches="tight"` or layout management.

**Blurry in a doc** &mdash; a raster format at too low a dpi. Use PDF, or 200&ndash;300 dpi.

**Huge PDF** &mdash; a dense scatter stored as vector. Rasterise that layer.

**Wrong font on another machine**. The font wasn't embedded. `pdf.fonttype = 42`.

**Invisible text on a dark background**. `transparent=True` changed the background and not the foreground.

**other from the screen** &mdash; the screen was a other size. The file is authoritative.

Each has a one-line fix, and all of them are easier to prevent in a saving function than to diagnose per figure.

## Figures in a pipeline

When charts are made on its own. A weekly report, a dashboard build, a model check. A few properties matter more than they do for a one-off.

**Determinism.** The same input should give the same file. That means seeding any noise, sorting anything whose order isn't sure. Pinning the style rather than taking from what is configured.

**Self-description.** The chart should carry its own date range and source. It will be found later without its context.

**Failure action.** A chart made from empty data should give a thing clear rather than an empty axes. A check and a clear message beats a blank rectangle in a report.

**Size predictability.** Labels grow with the data. `bbox_inches="tight"` and a figure size derived from the number of groups prevent a layout that worked in testing from cropping in production.

None of these is about matplotlib namely. They're the gap between a chart that runs unattended and one that has to be looked at each week.

## In summary

Pixel size is `figsize &times; dpi`. `figsize` decides how large the text looks scaled to the plot. So the two aren't the same ways of getting the same detail.

`bbox_inches="tight"` is the fix for cropped labels. Changes the output dims as a side effect.

PNG for the web, PDF or SVG for print and anything resized. Never JPEG for a chart.

Vector file size grows with the number of elements. A dense scatter wants `rasterized=True` on that artist.

`transparent=True` changes the background and not the text. A chart for a dark page needs its foreground recoloured too.

And in any loop that saves, `plt.close(fig)`. The figures don't clean themselves up. The warning arrives long after the memory has started growing.

## Choosing dpi and size together

The two are often chosen backwards: a default size, then a dpi high enough to look sharp.

The order that works is destination first.

**Print at 300 dpi, one column wide** &rarr; `figsize=(3.4, 2.4)`, `dpi=300`, fonts around 8 points.

**A slide** &rarr; `figsize=(10, 5.6)`, `dpi=150`, fonts 14 or larger.

**A web page at 700 px wide** &rarr; `figsize=(7, 4)`, `dpi=200` for retina displays, then let CSS scale it down.

**A quick look** &rarr; what the default is.

Setting the size to the destination means the fonts can be chosen once and are right. No scaling happens later to disturb the proportions.

The test is whether the figure needs resizing when it arrives where it's going. If it does, it was drawn at the wrong size.

## Checking the output

The saved file is what other people see. It differs from the screen in ways worth checking once per project rather than per figure.

**Open it at 100%.** Labels that are comfortable in a scaled preview may be too small.

**Check the edges.** Anything drawn outside the axes is the first thing to be cropped.

**Check the background.** A transparent figure over an surprise background, or a white border around a dark chart.

**Check the file size.** A oddly large PDF means a dense artist that should be rasterised.

**Open it in the destination**. The doc, the slide, the page &mdash; because that is where the size and the background are decided.

Doing this once when the saving function is written catches problems that would else recur in each figure the project makes.

## One more thing

`fig.savefig` accepts `pad_inches=0` alongside `bbox_inches="tight"`. This Drops the border fully.

That is what you want for a figure being embedded in a layout that gives its own spacing. What you don't want for one being viewed on its own. Here The border is what stops the labels touching the edge.

## The short version

The saved file is the artefact. The screen is a preview.

Size and dpi are one choice made for the destination, `bbox_inches="tight"` blocks the most common cropping, vector formats need rasterised layers for dense data. Each loop that saves needs to close.

## Reading the code back

A save is one call with four args that matter. The format, the dpi, the bounding box and the background. Wrapping them in a project function means they're decided once, applied all over. The close isn't forgotten. The check that the output is right is to open the file at full size in the place it will be used.
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

Pass a list of `datetime.date` or `datetime.datetime` objects. Or a pandas `DatetimeIndex`, or NumPy `datetime64`. And matplotlib recognises them and builds a date axis. Tick spots and labels are then chosen in date units rather than any numbers.

Pass **strings** and you get a thing quite other. Matplotlib treats them as groups. Each distinct string gets a spot, evenly spaced, in the order supplied.

That gap matters more than it sounds. With groups, two readings a day apart and two readings two months apart are drawn the same distance apart. The gap in the data disappears. The line implies a continuity that isn't there.

Since dates from a CSV arrive as strings, this is a common and quiet failure. `pd.to_datetime` before plotting is the fix. Checking the dtype is how you notice.

## Locators

A **locator** decides where ticks go. The date locators think in calendar units:

`YearLocator()`, `MonthLocator()`, `WeekdayLocator(byweekday=MO)`, `DayLocator()`, `HourLocator()`, `MinuteLocator()`.

Each takes an `interval`, so `MonthLocator(interval=3)` gives quarterly ticks. A few take a `by...` arg. `DayLocator(bymonthday=1)` for the first of each month.

`AutoDateLocator()` chooses based on the visible range, and adapts if the axis is zoomed.

Minor ticks add structure without labels: monthly majors with weekly minors gives a sense of scale without crowding.

## Formatters

A **formatter** decides how a tick reads.

`DateFormatter("%d %b")` uses `strftime` codes: `%Y` four-digit year, `%y` two-digit, `%m` month number, `%b` abbreviated month name, `%d` day, `%H:%M` time.

`ConciseDateFormatter(locator)` is often the better choice. It drops what is repeated. Printing the year once at the left rather than on each label. Showing only the day number when the month is unchanged. That is what a person would do by hand. It saves a great deal of flat space.

It needs the locator passed to it. It decides what to omit based on the tick spacing.

## Crowded labels

Date labels collide more than any other kind. They're long and there are many of them.

Three fixes, in order of preference:

**Fewer ticks.** A coarser locator. Fifteen readable ticks beat forty shared ones. The reader was never going to use all forty.

**Shorter labels.** `"%d %b"` instead of `"%Y-%m-%d"`, or `ConciseDateFormatter`.

**Rotation.** `fig.autofmt_xdate()` rotates the labels and right-aligns them. Also makes room. It works, and slanted text is truly harder to read than flat text. It belongs after the other two rather than instead of them.

A wider figure is the fourth option and often the honest one. A year of daily data doesn't fit legibly in four inches.

## Marking events

`axvline(date)` and `axvspan(start, end)` take dates right.

That works because the date axis is numeric underneath. Matplotlib converts dates to floating-point days since an epoch, plots the numbers. Formats the labels back into dates. `mdates.date2num` and `num2date` do the conversion by name when you need it.

The same fact shows why `set_xlim` accepts either dates or raw numbers. Why math on the limits works.

## With pandas

A pandas Series with a `DatetimeIndex` plots right:

```python
ax.plot(series.index, series.values)
```

or `series.plot(ax=ax)`, which uses pandas' own date formatting. The two give slightly other tick choices. Pandas' version is often good enough that no locator work is needed.

For a DataFrame, `df.plot(ax=ax)` draws each column against the index. This Is the fastest route from a time-indexed frame to a chart. And the subject of a later module.

## Time zones and the axis

matplotlib converts datetimes to numbers using a fixed epoch. Time-zone-aware timestamps are converted to the axis's timezone before plotting.

`rcParams["timezone"]` sets it. If it doesn't match the data's, the labels are correct times in a other zone. The shift is a whole number of hours. Large enough to matter and small enough to overlook.

The solid approach is the one from the pandas track. Norm to a single zone before plotting. Label the axis with which one.

## Gaps and non-trading days

A date axis draws real elapsed time. So A weekend appears as a gap.

For money data that is often unwanted: five trading days a week become a line with regular breaks. A month of data has eight or nine of them.

Two options. Plot against an int index and label the ticks with the dates. This Drops the gaps at the cost of a slightly dishonest axis. Or accept the gaps. This Is more truthful about elapsed time.

Which is right depends on whether the chart is about the market's action over trading sessions or about calendar time. Both are defensible. Picking without noticing isn't.

## Resampling before plotting

A year of per-minute data is half a million points. A chart seven inches wide has seven hundred pixel columns.

Resampling to a sensible rate before plotting is often better than drawing all:

```python
daily = series.resample("D").mean()
ax.plot(daily.index, daily.values)
```

That is fewer artists, a smaller file. A chart that looks same. Because the extra points were never distinguishable.

Where extremes matter, resampling to min and max per period and shading between them keeps the envelope. This Is the technique from the speed module.

## Multiple time series with different ranges

Two series covering other date ranges plot happily on one axis. The shorter one simply occupies part of the width.

That is correct and can mislead. A series that starts later looks like it began at zero rather than being unobserved. Making the gap clear. A note, or a shaded region marking where data exists. Blocks the reading that a thing changed at that date.

The same applies to a series with a gap in the middle. Here The broken line is the honest display and a joined one isn't.

## Annotating dates

each annotation method takes dates right, because the axis is numeric underneath.

The pattern for marking an event:

```python
ax.axvline(event_date, color="crimson", linestyle="--", linewidth=1)
ax.text(event_date, 1.01, " launch", transform=ax.get_xaxis_transform(),
        rotation=0, fontsize=9, color="crimson")
```

`get_xaxis_transform()` puts x in data units and y in axes fractions. The label sits just above the plot even so of the data's range. Which is what you want for an event marker that should stay at the top.

## Reading a time axis

Three things a reader needs from a dated axis, and which are often missing.

**The period covered**, which the first and last tick imply and a title states.

**The granularity** &mdash; whether a point is a day, a week or a month &mdash; which markers make clear and a smooth line hides.

**Whether gaps are real.** A break in a line means missing data. A gap on the axis with the line continuing means the axis is cat and the elapsed time isn't being shown.

Stating the rate in the title or the axis label. "Daily", "Monthly mean". Costs a word and answers all three.

## Common date problems

**Labels shared** &mdash; too many ticks. Use a coarser locator before rotating.

**Dates as groups** &mdash; strings not converted. Gaps disappear and the spacing is wrong.

**A shifted axis** &mdash; a time-zone mismatch between the data and `rcParams["timezone"]`.

**Ticks in odd places** &mdash; an auto locator on an unusual range. Name the locator.

**A rate string that no longer works**. Pandas 2.2 renamed a few of them.

**The line breaking at weekends**. Real elapsed time. This Is either correct or a reason to plot against an index.

The first two account for most of it, and both are visible at once.

## Aggregating before plotting

Most time-series charts are better after aggregation than before it.

Per-minute data over a year is half a million points and roughly seven hundred pixel columns. Resampling to daily gives 365 points, a chart that draws instantly. A picture that is visually same because the extra points were never separable.

The choice of aggregation is a choice about what the chart is for:

**Mean** for a level &mdash; the common value in each period.

**Sum** for a quantity &mdash; total sales per week.

**Min and max** shaded as a band, when the extremes are what matter and a mean would hide them.

**Last** for a state or a price. Here The value at the end of the period is the real one.

Plotting raw high-rate data and letting the renderer overplot it isn't more honest. It's the same data rendered less legibly, with what the shared happens to leave visible standing in for a summary you didn't choose.

## In summary

Pass real datetimes and matplotlib builds a date axis. Pass strings and it builds a cat one where gaps disappear.

`pd.to_datetime` with an clear `format` is faster and drops the day-first ambiguity.

Locators place the ticks in calendar units and formatters decide how they read, with `ConciseDateFormatter` dropping the repetition.

For crowded labels, fewer ticks first, shorter labels second, rotation last.

`axvline` and `axvspan` take dates right, because the axis is numeric underneath.

And pandas 2.2 renamed the rate aliases. `ME`, `h`, `min`. Which is the usual reason a copied example stops working.

## Periods rather than instants

Much time-series data is about **periods** rather than points: monthly totals, weekly means, daily counts.

Plotting a period as a point at its start implies the value occurred at that instant. A line between two such points implies a smooth transition through the month.

Two displays are more honest for period data.

**Bars**, one per period. This Say "this is the total for this interval" and have no between-values.

**A step line**, `ax.step(..., where="post")`. This Holds the value across the period and changes at the boundary.

A line is still fair when the periods are short scaled to the trend and the shape is the point. But it's a choice. For something like monthly revenue a bar chart is often the better display and rarely the one reached for.

Labelling the axis with the period. "Month starting". Drops the left ambiguity about which end a point shows.

## A closing note

Time axes carry more rules than any other kind. Most of the work is in the setup rather than the drawing.

Parse the dates properly, check the dtype, decide on a time zone, sort. Choose a rate that matches the question. After that, the plotting is the same as any other line chart.

The two failures that matter are plotting strings instead of dates. This Silently drops the gaps and misrepresents elapsed time. Letting the locator give more labels than can be read. This Is fixed by asking for fewer rather than by rotating them.

And rate aliases changed in pandas 2.2. This Accounts for a large share of examples that no longer run.

## The short version

A date axis is the gap between a chart of a time series and a chart of some values in order.

Parse properly, sort, choose a rate that matches the question. Use fewer ticks than the default. The rest follows from the line-chart material.

## Reading the code back

A time-series chart is a line chart with three extra choices. How the dates were parsed. This Locator places the ticks. Which formatter writes them. All three are made before any styling. Getting the first wrong makes the other two irrelevant because the axis isn't a timeline at all.
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
intro: Showing uncertainty, and saying which kind you're showing.

## errorbar

`ax.errorbar(x, y, yerr=err)` plots points with vertical intervals.

A single array or scalar gives **even** bars. The same distance above and below. A `(2, n)` array or a list of two arrays gives **skewed** ones, with the first row the distance **below** and the second the distance **above**.

Both are given as plus offsets from the point, not as abs spots. Passing abs upper and lower bounds is a common mistake and makes huge bars.

`xerr` does the same flatly, and both can be used at once.

`capsize` adds the end caps. Without it the bars are bare lines. This Is harder to read against a busy background. `fmt="o"` sets the marker. `fmt="none"` draws the bars with no marker at all.

## Bands

Error bars work for a handful of discrete readings. On a curve with two hundred points they share into a grey smear that conveys nothing.

`fill_between(x, low, high)` is the smooth version:

```python
ax.plot(x, y)
ax.fill_between(x, y - sd, y + sd, alpha=0.25)
```

`alpha` around 0.2 to 0.3 keeps the central line clearly on top. Using the same colour for line and band ties them together. Using a other one implies they're other series.

`fill_between` also takes `where=` to shade only part of the range. `step="pre"` for step-like data where a smooth fill would be wrong.

## Say which interval it is

This is the part that matters and is most often skipped.

**Standard deviation** shows the spread of the **data**. It doesn't shrink as you collect more.

**Standard error** shows the uncertainty of the **mean**. It's the standard deviation cut by the square root of n, so it does shrink.

**A trust interval** is roughly 1.96 standard errors for a 95% interval on a mean, under assumptions.

**A guess interval** is where a new finding should fall. Is wider than a trust interval for the fitted line.

On a sample of forty with a standard deviation of fifteen, these differ by a factor of six. An error bar without a caption saying which one it's can't be read. Readers well assume whichever supports their prior.

Put it in the axis label or the legend: `"mean (95% CI)"` costs nothing.

## Bars with error bars

`ax.bar(x, heights, yerr=errs, capsize=5)` works right, and `error_kw` passes styling through to the whiskers.

Two cautions exact to bars.

The **zero baseline** rule still applies. Error bars make it more tempting to break. A truncated axis makes the intervals look more split.

And the **share heuristic** &mdash; "the error bars share. The gap isn't large" &mdash; is wrong for trust intervals of two means. Non-shared intervals do imply a large gap. shared ones do **not** imply the lack of one. The relevant quantity is the interval around the *gap*. This Is narrower than either single interval suggests. Two 95% intervals can share by a fair margin while the gap is still large.

## Show the data when you can

With a dozen findings per group, a bar and an error bar throw away almost all: the shape, the outliers, the sample size.

A strip plot &mdash; the single points with a small random x offset, or "jitter", to stop them shared &mdash; shows all of it in the same space. Adding a flat line for the mean keeps the summary.

The fifth editor shows a case where two groups have the same mean and very other spreads, one with a clear outlier. The bar chart reports a taller error bar. The points report what happened.

The rule of thumb: under about fifty points per group, show the points. Above that, a box plot or a violin summarises without hiding as much as a bar does.

## Model intervals

Drawing a fit with a band is the standard way to show a model and its uncertainty. It needs being clear about which band.

A **trust band** for the fitted line is narrow in the middle and bow-shaped, widening at the ends where the fit is less constrained.

A **guess band** for new findings is much wider and roughly parallel to the line. It includes the residual scatter and the uncertainty in the line.

The sixth editor draws the second, about. For anything that will be used to make a choice, statsmodels or SciPy find these properly. The math is worth doing rather than approximating.

## Styling error bars

`errorbar` takes split styling for the line, the markers and the bars:

```python
ax.errorbar(x, y, yerr=e,
            fmt="o", markersize=5,
            ecolor="0.4", elinewidth=1, capsize=4, capthick=1)
```

`fmt="o"` draws markers with no connecting line. This Is right when the x values are discrete groups rather than a sequence. `fmt="none"` draws bars only.

`ecolor` lighter than the marker keeps the point as the subject and the interval as context. This Is often the correct emphasis.

`errorevery=5` draws bars on each fifth point, for a dense series where each bar would be a smear but some indication of uncertainty is wanted.

## Asymmetric intervals from quantiles

Real uncertainty is often skewed, and quantiles give it right:

```python
lo = np.percentile(samples, 5, axis=0)
hi = np.percentile(samples, 95, axis=0)
ax.fill_between(x, lo, hi, alpha=0.2)
```

For `errorbar` the same quantiles must be converted to **offsets** from the central value:

```python
yerr = np.vstack([median - lo, hi - median])
```

Losing that conversion &mdash; passing the quantiles themselves &mdash; is the most common error here. Makes intervals that are wrong by the magnitude of the data rather than subtly off.

## Several series with intervals

Two series each with a band share into a thing unreadable if both bands are the same weight.

Three things help: low alpha on the bands (0.15 rather than 0.3), matching each band to its line's colour. Drawing all the bands before all the lines so no line is buried.

```python
for name, (y, lo, hi) in series.items():
    ax.fill_between(x, lo, hi, alpha=0.15)
for name, (y, lo, hi) in series.items():
    ax.plot(x, y, label=name)
```

Beyond three series with bands, the bands stop being separable and small multiples are the answer.

## Error bars on log axes

An interval that is even on a linear scale is skewed on a log one, and vice versa.

Passing even `yerr` to a log-scaled axis makes a lower bar that is visually much longer than the upper one. This Is correct math and often not what was intended. Scaling uncertainty is most times what you've on a log scale.

The fix is to find the interval in the space you're plotting. Bounds as scaling factors, converted to offsets at each point.

A bar reaching below zero on a log axis simply doesn't draw. This Is the visible symptom.

## What the interval is for

An error bar is a claim about repeatability, and it's worth being clear which claim.

"If I did this again, the mean would land in here" is a trust interval.

"A new finding would land in here" is a guess interval, and is much wider.

"The data spread this much" is a standard deviation, and doesn't shrink with more data.

Charts routinely show one and are read as another. The caption is the only thing that resolves it. This Is why each editor here labels the interval rather than leaving it to the reader.

## Uncertainty that is not statistical

Not each band is a trust interval. Saying which kind it's matters as much as the math.

**A reading handling** &mdash; the instrument's stated score, fixed and known.

**A range across cases** &mdash; best and worst case. This Isn't a chance statement at all.

**A forecast interval** &mdash; widening with horizon, and gated on the model.

**Seen min and max** &mdash; the actual extremes. This Say nothing about what a new finding would do.

Each is a other claim, and drawn the same way. The caption is the only thing distinguishing them. This Is why an untagged band is the most common way a chart overstates what is known.

## Choosing what to show

The choice is what the reader should conclude.

If the question is **"is this gap real?"**, show a trust interval on the gap, not two intervals on the means. The eye can't combine them right.

If the question is **"how var is this?"**, show the spread: a standard deviation, a percentile band, or the points.

If the question is **"what will happen next?"**, show a guess interval. This Is wider than either.

If the sample is small, showing the findings answers all three better than any interval.

The failure to avoid is showing a standard error because it's narrowest and letting it be read as spread. This Understates spread by a factor of the square root of n.

## Intervals in a report

An interval on a chart is a claim. The nearby text is part of it.

Three things belong in the caption or the axis label, and are almost always omitted:

**Which interval it's** &mdash; standard deviation, standard error, a trust interval and at what level, or a guess interval.

**What it assumes** &mdash; normality, freedom, a model.

**The sample size**, because an interval from eight findings and one from eight hundred are other kinds of claim even when they're the same width.

"Mean &plusmn; 95% CI, n = 42" in the y label costs nine words and makes the chart readable. Without it the reader either assumes the most favourable reading or discounts the interval fully. Both are worse than being told.

## In summary

`errorbar` for discrete readings, `fill_between` for a curve. Hundreds of bars become a smear.

`yerr=[lo, hi]` takes plus offsets, not abs bounds. Getting that wrong makes intervals wrong by the scale of the data.

Standard deviation, standard error and a trust interval differ by large factors on the same data. An untagged bar can't be read.

shared trust intervals don't imply the lack of a large gap, though non-shared ones do imply its presence.

On a log axis, even offsets are skewed on screen. The interval should be found in the space being plotted.

And with few findings, showing the points beats any summary of them.

## Bands on a forecast

A forecast chart has a exact rule worth following.

The **historical** series is drawn solid. The **forecast** is drawn dashed or in a other shade. The boundary between seen and predicted is visible without reading the caption.

A **vertical line** at the forecast origin makes it unmissable.

The **band widens** with horizon. Uncertainty grows. A constant-width band on a forecast is almost always wrong. It understates the far end.

**Two bands** at other levels. 50% and 90%, with the inner one darker &mdash; send the shape of the uncertainty better than one. Are standard in published forecasts.

And the caption states the model and the interval. A forecast band is fully gated on a model the chart doesn't show.

Without the vertical line and the style change, a reader takes the whole line as data. This Is the most consequential misreading on hand on this kind of chart.

## The short version

An interval is a claim, and the caption is part of the claim.

Standard deviation, standard error, trust and guess intervals differ by large factors on the same data. Drawing them the same way without saying which is the most common way a chart overstates what is known.

## Reading the code back

Drawing an interval is one arg. Deciding which interval, finding it right as offsets. Saying in the chart which one it's are three split pieces of work. Only the first is about matplotlib. A band drawn without the other two is a decoration that readers will read as a claim.
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
intro: imshow and pcolormesh, and the origin that catches all.

## imshow

`ax.imshow(z)` draws a 2-D array as a grid of coloured cells.

Its defaults are chosen for **images**, and three of them are wrong for data.

**Origin.** `z[0, 0]` is drawn at the top-left. That is where the first pixel of an image goes. For a mat whose rows are a quantity. A y axis. That puts the smallest value at the top, upside down. `origin="lower"` fixes it.

**Aspect.** The default `"equal"` makes each cell square. A 6&times;30 array is drawn five times wider than tall no matter what figure size you asked for. `aspect="auto"` stretches it to fill the axes.

**blending.** The default smooths between cells. On a photo that is wanted. On a mat of values it draws colours that match to no data point. This Is a small lie. `blending="nearest"` gives hard cell edges.

For data, `imshow(z, origin="lower", aspect="auto", blending="nearest")` is the honest starting point.

## Labelling cells

A heatmap of a small mat is a table that has been coloured. It should read like one.

Set the ticks to the row and column names. Write the values into the cells:

```python
for i in range(rows):
    for j in range(cols):
        ax.text(j, i, z[i, j], ha="center", va="center")
```

Note the index order: `ax.text(j, i, ...)`. The first arg is x. This Is the **column**. Getting this backwards is the usual bug. On a square mat it makes a transposed result that looks plausible.

Choosing the text colour by threshold. White on dark cells, black on light. Keeps each label readable. Without it, half the numbers vanish into the background at one end of the colormap.

## pcolormesh

`imshow` assumes a regular grid and skips any coords you've.

`pcolormesh(x_edges, y_edges, z)` takes the **edges** of the cells. They can be unevenly spaced. Logarithmic bins, irregular time intervals, a non-uniform mesh.

The edges outnumber the cells by one in each direction, the same rule as histogram bins. Passing centres instead of edges is the common mistake. Matplotlib will accept same-sized arrays and shift all by half a cell.

`pcolormesh` is slower than `imshow` and much more flexible. For a regular grid, `imshow` is the right tool.

`contourf` is the third option, drawing filled contour bands rather than cells. Right when the underlying field is truly smooth and misleading when it isn't.

## Shared colour scales

`vmin` and `vmax` set the values at the ends of the colormap.

Without them, each heatmap scales to its own data, just like unshared subplot axes. Two heatmaps drawn side by side then use the same colours for other values. The compare the layout invites is invalid.

The colorbar does say so, in numbers. Readers don't read them. They read the colours.

So: when two colour-mapped plots will be checked, fix `vmin` and `vmax` across both, or use one shared colorbar.

`norm=` gives finer control &mdash; `LogNorm` for data spanning orders of magnitude, `BoundaryNorm` for discrete bands.

## Centring a diverging map

A diverging colormap has a neutral colour in the middle and two directions away from it. It only means anything if that neutral point sits at the value that matters, often zero.

With auto limits, the midpoint of the colormap lands at the midpoint of the **data**. On data ranging from &minus;4 to +10, white sits at +3. Each cell below +3 is coloured as though it were minus.

The fix is even limits:

```python
lim = np.abs(z).max()
ax.imshow(z, cmap="coolwarm", vmin=-lim, vmax=lim)
```

or `TwoSlopeNorm(vcenter=0)` when the two sides truly need other ranges.

This is one of the most common quiet errors in heatmaps. The result looks like a normal chart and asserts a thing false about the sign of half the data.

## extent for real coordinates

`imshow` numbers the cells from zero by default. `extent=(x0, x1, y0, y1)` maps the array onto real coords:

```python
ax.imshow(z, extent=(0, 100, 0, 50), origin="lower", aspect="auto")
```

The four values are the outer edges of the image, not cell centres. This Is the usual off-by-half confusion. With `origin="lower"`, `y0` is the bottom.

This is what lets a heatmap be overlaid with a line or a scatter in the same units. Without it any overlay is a half-cell out.

## Masked and missing values

`np.nan` in the array is drawn as the colormap's "bad" colour. This Defaults to fully transparent. So missing cells show what is behind them, often the axes background.

`cmap.set_bad("0.9")` makes them an clear grey. This Is better than transparent because a missing cell then reads as missing rather than as background.

A masked array behaves the same way. Is the more clear form when the mask is found apart from the data.

## Aspect and reading order

For a link mat or any square array, `aspect="equal"` is right and is the default.

For a wide array &mdash; time along one axis, a handful of groups along the other &mdash; `aspect="auto"` is needed, or the figure is drawn at the array's proportions and skips the size you asked for.

Row order deserves thought. An unordered heatmap makes the reader scan for structure. Sorting rows by their mean, or by a clustering, often reveals the pattern the chart is meant to show. That is a data choice made in the plotting code. It should be stated in the caption if the order isn't alphabetical.

## Contours

`ax.contour(z)` draws lines of constant value. `ax.contourf(z)` fills between them.

They suit truly smooth fields. Elevation, temp, a fitted surface &mdash; and imply smoothness. They're wrong for a mat of split readings where `pcolormesh` is honest.

`levels=` sets the number or the exact values. `ax.clabel(cs, inline=True)` writes the values on the lines. This Often drops the need for a colorbar.

Mixing a filled contour with thin contour lines on top is a standard treatment for a field where both the bands and the exact levels matter.

## Annotating a heatmap

For a small mat, writing values into the cells makes it a table with colour as a visual aid rather than the only encoding.

The threshold trick for text colour is worth restating because it's the gap between a readable and an unreadable heatmap:

```python
color = "white" if z[i, j] > z.max() / 2 else "black"
```

For a diverging map centred on zero, the threshold should be based on distance from the centre rather than from the max, or the labels invert on the wrong half.

## Reading a heatmap

Heatmaps are read less accurately than people assume. Colour intensity is a weak encoding.

They're good at showing **patterns**: blocks, grads, an outlier cell, structure along a main-line.

They're poor at **values**: no one reads 0.62 off a colour.

So the rule is that a heatmap should either be about the pattern, or it should have the numbers written in the cells. At which point it's a table with colour as a guide. This Is a truly good display for a small mat.

For a large mat, the pattern is the only thing on hand. Sorting the rows and columns. By cluster, by total, by a real sequence. Is what makes a pattern visible at all.

## Common heatmap mistakes

**Wrong origin** &mdash; row 0 at the top for data whose y axis is a quantity.

**blending on** &mdash; smoothing between cells that are split readings.

**Unshared scales** across panels that will be checked.

**An uncentred diverging map**, putting the neutral colour at an any value.

**No colorbar**, leaving the colours meaningless.

**Text the same colour all over**. So Half the labels disappear into the background.

**Unordered rows**, hiding what structure exists.

All seven are defaults or omissions rather than errors of math. This Is why a heatmap can look professional and send nothing.

## Correlation matrices

The most common heatmap and it has its own rules.

**Centre the colormap on zero** with even limits. A link of &minus;0.4 and +0.4 should be equally strong in opposite directions. Without it, a mat of mostly plus links puts the neutral colour one spot any and the few negatives look far more extreme than they're.

**Use a diverging map** for the same reason.

**Set `vmin=-1, vmax=1`**, so two mats are close and so the colour scale means the same thing in each such chart.

**Mask the upper triangle**, since the mat is even and half of it's repetition. `np.triu` with `np.nan` and a `set_bad` colour does it.

**Write the numbers in**, if the mat is small enough. The exact values are often what the reader wants.

Those five turn the default output into a thing readable. The first three are the ones that affect whether it's accurate.

## In summary

`imshow` has image defaults: row 0 at the top, square cells. Blending between them. For data, `origin="lower"`, `aspect="auto"` and `blending="nearest"` are the honest settings.

`pcolormesh` takes cell edges and handles uneven grids. Edges outnumber cells by one per axis.

`vmin`/`vmax` are what make two heatmaps close. Their lack is the same error as unshared subplot axes.

A diverging colormap needs even limits or its neutral point lands at the midpoint of the data rather than at zero.

A colorbar isn't optional, and a small mat is better as a table with the numbers written in.

And row order is a choice: sorting by a real quantity is often what makes a pattern visible at all.

## Overlaying on an image

A heatmap or image often needs a thing drawn on top. Contours, a scatter, a boundary.

The key is that `imshow` sets up a coord system. All overlaid must use the same one.

With default settings the cells are numbered from zero and a scatter must be in those units. With `extent=`, both use real coords and the overlay is straightforward.

Two details catch people. `extent` gives the outer **edges**. A cell centre is half a cell in from the boundary. A scatter of cell centres plotted against edge coords is offset by half a cell. This Looks like a small registration error.

And `origin="lower"` must be steady between the image and any y coords found for the overlay, or the overlay is flipped scaled to the image while both look on their own correct.

Drawing a few known points on top is the quickest way to confirm the coord system is what you think.

## One more thing

`ax.matshow` is `imshow` with the defaults already set for a mat. Origin at the top with the tick labels along the top edge. This Is the rule for displaying a mat in math form.

It's convenient for a link mat and confusing for anything with a quantitative y axis. Here `imshow(origin="lower")` remains the right call.

## The short version

A heatmap is read for its pattern, not its values. This Is why sorting the rows and columns matters as much as the colormap.

The defaults are built for photos. Three of them. Origin, aspect and blending. Are wrong for data. Setting all three by name is the honest starting point.

## Reading the code back

A heatmap is one call and four corrections to its defaults. Origin, aspect, blending and the colour limits. Add a colorbar with a label and, for a small mat, the values in the cells. That is six lines. It's the gap between a picture of colours and a readable display of a mat.
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
intro: Changing each chart at once, instead of styling each one by hand.

## rcParams

`plt.rcParams` is a dict of each default matplotlib uses. A few hundred settings covering figure size, fonts, colours, line widths, spines, grids, ticks and saving.

Changing one changes each figure created later:

```python
plt.rcParams["axes.spines.top"] = False
```

The keys are dotted paths mirroring the object structure: `lines.linewidth`, `axes.titlesize`, `xtick.direction`, `savefig.dpi`.

`plt.rcdefaults()` restores all, which is worth knowing in a notebook where settings build up across cells.

The key property is that these are **defaults**, applied when an artist is created. Changing a setting doesn't affect figures already drawn.

## Style sheets

A style sheet is a named bundle of rcParams.

`plt.style.on hand` lists them &mdash; `ggplot`, `bmh`, `fivethirtyeight`, `grayscale`, the `seaborn-v0_8-*` family, and a few others.

`plt.style.use("ggplot")` applies one from that point on. `with plt.style.context("ggplot"):` applies it to a block and restores the previous settings later. This Is what you want in a script that also makes charts in a other style.

Writing your own is a plain text file of `key. Value` lines with a `.mplstyle` extension, placed where matplotlib looks for it. For a project, a dict in a module is often simpler.

## Combining

`plt.style.use(["ggplot", {"lines.linewidth": 3}])` applies items left to right, so later ones win.

A dict in the list is treated as rcParams. That is the hands-on form for real work. Take a published style for its typography and colours, then replace the two or three things it gets wrong for your case, without copying and keeping a whole style file.

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

`rc_context` takes a dict right and restores the previous settings on exit.

The settings worth putting in almost any house style are the ones that fix matplotlib's weakest defaults. The top and right spines, a left-aligned bold title, a faint grid drawn below the data, a legend without a frame. A colour cycle you chose.

That is six lines, and it's the gap between charts that look like matplotlib defaults and charts that look designed.

## What styles cannot do

A style sets defaults. It can't make choices.

It won't choose between a bar chart and a line chart. It won't set an `alpha` right to your number of points. The right value for 100 points is wrong for 100,000. It won't decide the axis should start at zero, or that the title should state a finding, or that three of the seven series should be greyed out.

The fifth editor shows a styled scatter that is still unreadable. The problem was overplotting and no setting handles that.

Styling is the last 20% of a chart. The choices are the rest. They're the subject of most of this track.

## Fonts

`font.family` takes a plain name. `sans-serif`, `serif`, `monospace` &mdash; and `font.sans-serif` is the sorted list of actual fonts tried for it.

A font that isn't installed makes a **warning and a fallback**, not an error. The figure renders in what was on hand next. This Means the same script can give other-looking output on a other machine. The only sign is a warning that is easy to miss in a log.

For output that must look same all over, either restrict yourself to fonts you know are present, or embed the font by saving as PDF or SVG with `pdf.fonttype = 42`. This Stores the glyphs in the file.

`mathtext` handles LaTeX-style maths in labels without needing LaTeX installed: `r"$\\sigma^2$"` in any text arg.

## Where settings come from

matplotlib reads its defaults in a fixed order, each replacing the last:

The built-in defaults.

A `matplotlibrc` file, found in the current folder, the user's config folder, or the installation.

`plt.style.use(...)`.

Direct set to `plt.rcParams`.

args passed to the plotting call itself.

That sorting shows a common confusion: a setting applied in a style sheet is overridden by anything passed by name. A `matplotlibrc` in the working folder silently changes each chart in that project. When a figure looks other on another machine, a `matplotlibrc` is a pick.

## Settings worth knowing

Beyond the obvious ones, a handful appear in most house styles:

`figure.autolayout: True` &mdash; applies `tight_layout` to each figure on its own.

`axes.titlelocation: left` &mdash; headline-style titles.

`axes.axisbelow: True` &mdash; grid behind the data.

`legend.frameon: False`.

`savefig.bbox: tight` &mdash; makes each save behave as if `bbox_inches="tight"` had been passed. This Drops a whole class of cropping bug.

`figure.constrained_layout.use: True` &mdash; the newer option to `autolayout`.

`errorbar.capsize: 3` &mdash; caps by default, since the bare-line default is rarely what anyone wants.

## Writing a style file

A `.mplstyle` file is plain text, one `key: value` per line, with `#` comments and no quotes:

```
figure.figsize: 6.5, 3.5
axes.spines.top: False
axes.prop_cycle: cycler('color', ['264653', 'e76f51', '2a9d8f'])
```

Note the colours have no `#` prefix. `#` starts a comment in this format. A small trap that makes a confusing parse error.

Placed in `~/.config/matplotlib/stylelib/`, it can be used by name from anywhere.

## Per-project versus per-figure

A project-wide style is right for agreement and wrong when one figure needs to differ.

`plt.rc_context(...)` as a context manager is the middle ground. A project default applied broadly. A block that replaces it for one figure without leaking.

The failure mode of global settings in a notebook is that they build up invisibly across cells. A figure depends on which cells have been run. `plt.rcdefaults()` at the top of a notebook, followed by the project style, makes it fixed.

## Style is not design

A style sheet gets the typography, spacing and palette steady. This Is truly valuable and is roughly the last fifth of making a chart good.

The other four fifths &mdash; which chart, what to compare, what to leave out, what the title claims, whether the axis starts at zero &mdash; are choices no setting can make.

That is worth saying by name because a good style sheet makes a bad chart look professional. This Isn't an gain.

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

Nothing exotic, and each chart in a project drawn under it looks intentional. `savefig.bbox` alone drops the most common cropping complaint.

## Styles and reproducibility

A figure's appearance depends on settings that aren't in the plotting code. This Is a reproducibility problem.

Three sources of drift: a `matplotlibrc` in the working folder, built up `rcParams` changes in a long notebook session. A style sheet that differs between machines.

Two habits address it.

**Reset by name** at the start: `plt.rcdefaults()` followed by the project style. The figure then doesn't depend on what ran before.

**Apply the style in a context manager** rather than globally. A figure carries its own appearance rather than taking from what is current.

For a figure that will be regenerated months later, the style belongs in the store alongside the code, not in a user config folder.

## Style as a decision record

A style sheet is a place to write down choices once. That is worth more than the agreement it makes.

each setting in it codes a judgement: that titles are left-aligned headlines, that grids are faint and behind the data, that legends have no frame, that this is the palette. Written in a style file, those choices are visible, reviewable and changeable in one place.

Written into each chart, they're re-decided each time, inconsistently, by whoever is writing that chart.

The hands-on gain shows up when a thing has to change. A new brand colour, a journal's font need, a switch to dark backgrounds for a presentation. With a style, that is one edit. Without it, it's a search through each plotting call in the project.

That is the same arg as any other config. It applies here more than people expect. Chart styling is just the kind of thing that gets copy-pasted.

## In summary

`rcParams` holds each default, and changes affect figures created later.

Style sheets bundle them. `plt.style.context` applies one to a block without leaking.

A list applies styles in order. A dict in the list replaces single settings. The hands-on way to take a published style and fix the two things it gets wrong.

`rc_context` with a module-level dict is the whole method for a project style.

A missing font warns and falls back silently. So Figures can look other elsewhere.

And a style is the last fifth of a good chart. It can't choose the chart type, set an alpha suited to your sample size, or decide what the title should claim. And it will make a bad chart look professional. This Isn't the same as making it better.

## Dark backgrounds

A dark theme isn't a colour inversion, and doing it by hand often misses a thing.

The elements that need changing: the figure background, the axes background, the text colour, the tick colours, the tick label colours, the spine colours, the grid colour. The property cycle. Because a palette tuned for white is often too dark on black.

`plt.style.use("dark_background")` does all of it. This Is the arg for using a style rather than setting six things.

Two further points. Saturated colours that look right on white are often too intense on black. Desaturating them slightly helps. And `savefig` still writes a white background unless told else. A dark figure saved with default settings comes out with a white border around a dark plot. `facecolor=fig.get_facecolor()` fixes it, or setting `savefig.facecolor` in the style.

## Where to keep a style

A project style needs to live one spot both the code and the people can find.

**A module in the store**. `style.py` exporting a dict &mdash; is version-controlled, reviewable. Importable. It's the option that behaves like the rest of the code.

**A `.mplstyle` file in the store**, applied with a scaled path, is equal and uses matplotlib's own format.

**A file in the user's config folder** is convenient and invisible to all else. This Makes figures irreproducible on another machine. It's the wrong place for anything shared.

The store options also mean the style is part of the diff when it changes. A figure that suddenly looks other has a commit showing why.

For a single analysis, a dict at the top of the notebook applied with `rc_context` is enough. Still better than settings scattered through the plotting calls.

## One more thing

`plt.style.use` accepts a URL or a file path and a name. A style can be shared without installing it.

For a team, a style file in a shared store referenced by scaled path gives all the same figures without anyone configuring their setting. And it appears in code review when it changes.

## The short version

A style is a set of choices written down once. This Is worth more than the agreement it makes.

It handles typography, spacing and palette. Roughly the last fifth of a good chart. The other four fifths are choices no setting can make. A good style applied to a bad chart makes a professional-looking bad chart.

## Reading the code back

A style is a dict applied in a context manager. Its contents are choices rather than settings. The ones that matter most are the ones fixing matplotlib's weakest defaults. Spines, title alignment, grid weight, legend frame and the colour cycle. Six entries covers it. Each chart in the project then starts from a better place.
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

all drawn on `ax2` uses the right-hand scale. They're truly split axes objects: split limits, split ticks, split artists.

The one styling step that isn't optional is **colour-coding**. Set each y label and its tick labels to match the colour of the series that uses it:

```python
ax.set_ylabel("revenue", color=c1)
ax.tick_params(axis="y", labelcolor=c1)
```

Without it, the reader has two scales and no way to tell which belongs to which line. The chart is simply unreadable.

## The legend problem

`ax.legend()` collects labelled artists **on that axes only**. With a twin, that means each half of the chart gets its own legend. This Looks like a mistake.

Collect the handles and pass them to one call:

```python
l1, = ax.plot(..., label="A")
l2, = ax2.plot(..., label="B")
ax.legend(handles=[l1, l2])
```

Or gather them generically with `ax.get_legend_handles_labels()` on each axes and concatenate.

## Why they mislead

This is the part worth taking seriously.

Two series on split scales have **no defined link**. Where they cross. This Is above which, whether they diverge. All of it depends on the limits you chose for the second axis. Change `ax2.set_ylim` and the crossing moves, or disappears.

The third editor draws the same two series three times with other right-hand limits. They cross in three other places.

Readers don't see it that way. A crossing looks like an event: "revenue overtook cost in June". It's an artefact of a choice you made, often without thinking about it. Matplotlib picked the limits on its own.

This is the method behind a large share of misleading charts in the wild. Most of them aren't deliberate.

## The alternatives

**Stacked panels** with `sharex=True`. Two small charts, one above the other, sharing the time axis. The shapes can be checked, the levels can't be confused. No crossing is implied. This is the right answer most of the time.

**Index both to a common base.** Divide each series by its first value and times by 100. Both are then percentages of their own starting point, they share one axis honestly. A crossing now means a thing real: scaled growth diverged.

**Percentage change** does the same job for series where the level isn't real.

**Two charts** side by side, when the series have nothing in common but the time axis.

## secondary_axis

`ax.secondary_yaxis("right", functions=(forward, inverse))` is a other method and doesn't share the drawbacks.

It shows the **same data** in a second unit, with an clear conversion. Celsius and Fahrenheit, millimetres and inches, a count and a percentage of a known total.

Because the two scales are related by a function rather than by an any choice, nothing about the chart can mislead. The line is in one place. The two axes are two ways of reading the same spot.

The functions must be inverses of each other. Matplotlib uses both. Forward to place the ticks, inverse to keep them steady when the view changes.

`secondary_xaxis` does the same flatly. This Is how you put dates on one side and elapsed days on the other.

## When a twin axis is fine

There's a defensible case, and it's narrower than its popularity suggests.

It works when one series is clearly **background context** rather than a co-equal subject. The standard example is price and volume. Volume as pale bars pushed to the bottom of the chart, price as a line in front. No one tries to compare a bar height with a line spot. The visual tree makes clear which one is the subject.

Setting the bar axis limit to two or three times the data range pushes the bars down and reinforces that.

The test: if a reader might compare the two series against each other, the twin axis is a hazard. If one is obviously scenery, it's a fair use of space.

## Ordering and z-order

The twin axes is created after the first. Its artists draw **on top** by default.

That is often wrong when the first series is the subject. A background bar series drawn on `ax` ends up behind. This Is right. A line drawn on `ax` is covered by anything on `ax2`.

`ax.set_zorder(ax2.get_zorder() + 1)` moves the first axes in front. `ax.patch.set_visible(False)` is then needed, or its opaque background hides the second axes fully.

That two-line incantation appears in a great deal of twin-axis code. It exists because the axes are truly stacked rather than merged.

## Grid lines on a twin

Both axes can draw a grid. Two grids at other spacings is visual noise that makes both harder to read.

The rule is to grid only the axes whose scale the reader should use for judging values. Often the main one. And to turn the other off:

```python
ax.grid(True, axis="y", alpha=0.3)
ax2.grid(False)
```

Since `ax2` takes from grid settings from rcParams, turning it off by name is needed when the style enables grids by default.

## Aligning the two scales

A frequent request is to make zero on both axes fall at the same height. The two series are close around a baseline.

There's no built-in for it. It's math on the limits:

```python
def align_zero(a1, a2):
    l1, h1 = a1.get_ylim(); l2, h2 = a2.get_ylim()
    f = l1 / (l1 - h1)
    a2.set_ylim(bottom=(f * h2) / (f - 1) if f != 1 else l2)
```

Whether that is a good idea is another question. Aligning zero makes the chart look more close without making it more close. The scales are still unrelated. The reader is now more likely to compare them.

## Three axes

`ax.twinx()` twice gives a third scale, with the third spine pushed outward:

```python
ax3 = ax.twinx()
ax3.spines["right"].set_position(("outward", 45))
```

It works, and it's almost always a mistake. Three unrelated scales on one plot is three any choices, and no amount of colour coding makes the crossings real.

If three series must be shown together, three stacked panels sharing an x axis is the display that does it honestly, and it isn't much taller.

## The honest summary

Twin axes exist because people want them, and matplotlib gives them without editorialising.

They're right when one series is context and the other is the subject, when the two quantities are related by a thing the reader knows, or when a rule in the field makes the pairing familiar.

They're inappropriate when the chart invites a compare of levels or a reading of the crossing point. Which is most of the time. Is why the options in this module are worth reaching for first.

## How the misreading happens

Worth spelling out, because it isn't obvious that anything is wrong.

A reader sees two lines. Lines on a chart most times share a scale. Distance between them means a thing. Here it doesn't. The vertical gap is the gap between two any rescalings.

The crossing is worse. A crossing is a visually salient event. The reader reads it as "the quantities became equal". Which is meaningless when the units differ. Move one axis's limits and the crossing moves, or vanishes.

None of that is signalled. The chart looks like every other two-line chart. The two y axes are the only clue that the usual reading doesn't apply.

## If you must

When a twin axis is truly the right choice, four things make it as safe as it can be.

**Colour-code both axes** to their series, including the tick labels.

**Make the tree obvious** &mdash; one series as background context, the other as the subject.

**Don't let them cross**, if the limits can fairly be set to avoid it.

**Say in the caption** that the scales are split.

And check the option honestly first. Most twin-axis charts exist because two series were to hand, not because the compare needed one plot.

## A decision procedure

When a second scale is proposed, four questions settle it.

**Are the units related by a known conversion?** If yes, `secondary_yaxis` with the conversion functions. Safe. Not really a second series at all.

**Is one series clearly background?** If yes, a twin axis is defensible, with the background pushed down and drawn in a pale colour.

**Would indexing both to a common base answer the question?** often yes. It puts them on one honest axis where crossings mean a thing.

**Would two stacked panels do?** Almost always yes, and it costs nothing but vertical space.

Only if the first two are no and the second two are truly unsuitable is a co-equal twin axis the right answer. And by that point the thinking has been made clear. This Is the handy part of the exercise.

## In summary

`twinx` gives a second axes sharing the x axis and its own y scale.

Colour-code both axes to their series, or the chart is unreadable.

One legend needs collecting the handles from both axes.

The crossing point is found by the limits you chose. Readers treat it as a finding. Which is the whole problem.

`secondary_yaxis` with a function pair is a other and safe method, relabelling one series in another unit.

The honest options are stacked panels sharing an x axis, or indexing both series to a common base.

And a twin axis is fair when one series is obviously scenery. Volume behind price. Because then no one is trying to compare them.

## A worked alternative

Given revenue in thousands and conversion rate in percent over twelve months, the twin-axis version puts them on one plot and invites a compare that isn't defined.

Three options, each answering a slightly other question.

**Stacked panels**, sharing the x axis. Answers "how did each move?" and allows the shapes to be checked without implying anything about levels.

**Indexed to January = 100.** Answers "which grew faster?" and puts both on one honest axis. Here A crossing truly means scaled speed diverged.

**A scatter of one against the other**, coloured or labelled by month. Answers "are they related?" right. This Is often the underlying question when someone reaches for a twin axis.

That third one is worth considering more often. A twin-axis chart is often an attempt to show a link using a display designed for showing two time series. A scatter shows the link.

## One more thing

`ax2.set_ylim` should often be set by name on a twin axis rather than left auto.

The reason is reproducibility rather than aesthetics: auto limits depend on the data. A chart regenerated next month has a other second scale and the two lines cross one spot new. If a reader has seen the earlier version, that looks like a change in the data.

## The short version

A second y axis is the only common chart feature whose main effect is on what the reader wrongly concludes.

all else in this track can be done badly. A twin axis is hard to do well even on purpose. The ambiguity is in the display rather than in the run. Reaching for stacked panels or a common index first is the habit worth having.

## Reading the code back

A twin axis is one call and a series of mitigations. Colour-code both scales, assemble one legend, fix the limits by name, establish a visual tree. Say in the caption that the scales are split. The length of that list is itself the arg for checking whether stacked panels would do instead.
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
intro: Checking many spreads at once, and what each summary throws away.

## What a box plot is

Five numbers, drawn:

The **box** spans the first to the third quartile. It holds the middle half of the data. Its height is the interquartile range.

The **line** inside is the median &mdash; not the mean.

The **whiskers** reach the furthest data point within 1.5&times;IQR of the box. They aren't a fixed multiple of anything. They stop at real findings.

Points beyond that are drawn **on their own** as outliers.

That 1.5 is a rule, chosen so that roughly 0.7% of most times spread data falls outside. It has no deeper justification. Matplotlib lets you change it with `whis=`.

## What they are for

Checking many groups.

Five histograms take five panels and need the reader to move between them. Five boxes sit side by side on one axis, sharing a scale, and the compare is direct.

That is the whole arg, and it's a strong one. For one spread, a histogram is better. For eight, a box plot is much better. one spot around three the answer changes.

`patch_artist=True` makes the boxes filled rather than outlines. This Is needed before `set_facecolor` does anything. A common small frustration.

## What they hide

A box plot is a summary, and each summary discards.

Any spread sharing those five numbers makes an same box. That includes a **bimodal** spread. Two clusters with a gap in the middle. Whose median sits in the empty space where no data is.

The third editor draws just that: two spreads with nearly same boxes and fully other shapes.

This isn't a hypothetical failure. Bimodality often means two groups have been mixed. This Is often the most key thing in the data. The box plot conceals it just right.

The hands-on rule: look at a histogram of each group **once** before settling on box plots for the compare.

## Violin plots

A violin shows an guessed density, mirrored. The width at any height is how much data is around that value. It shows the bimodality a box hides.

Two honest caveats.

It's a **kernel density guess**, with a bandwidth that smooths the data. That param has just the arbitrariness of a histogram's bin count. Matplotlib picks it for you. Too much smoothing merges peaks. Too little invents them.

It **extends past the seen data** at both ends. The kernel has tails. A violin of a strictly plus quantity will happily show density below zero. This Is a claim the data doesn't support.

`showmedians=True` adds the median line. The defaults draw the extrema.

## Showing the points

For small samples, the best display is often both. A box or violin for the summary. The single points with jitter on top.

`showfliers=False` blocks the outliers being drawn twice, once by the box and once by the scatter.

`zorder=3` on the scatter puts the points above the box.

Below roughly fifty points per group this is strictly more helpful than either element alone. You get the quartiles and the actual sample. Above a few hundred, the points overplot and the summary is doing the work.

## Layout

`vert=False` draws them flatly. This Lets long group names read most times. The same arg that makes `barh` preferable to `bar`.

Sorting the groups by median makes the ranking direct rather than a thing the reader assembles.

And as with any grouped compare, the y axis must be shared. This It's by build here. That is part of why the display works.

## Notches and confidence

`notch=True` draws a waist around the median whose width approximates a 95% trust interval for it.

The heuristic it enables is that if two notches don't share, the medians differ much. That is roughly true and depends on assumptions the plot doesn't state.

Two hands-on problems. On small samples the notch can extend beyond the box, making a folded shape that looks like a rendering error. And the heuristic is just the share thinking that is unreliable for error bars, applied to a other statistic.

handy when checking many groups quickly. Not a substitute for a test.

## Ordering and orientation

The same args as bar charts apply.

Sort by median unless the group order means a thing. Time, size, an test sequence.

Use `vert=False` when the labels are words.

And keep the y axis shared. This Happens on its own here because all groups share one axes. Is just why the display works for compare.

## Styling the parts

`boxplot` returns a dict of the artists, keyed by `"boxes"`, `"whiskers"`, `"caps"`, `"medians"`, `"fliers"`:

```python
bp = ax.boxplot(data, patch_artist=True)
for b in bp["boxes"]:
    b.set(facecolor="#a8dadc", edgecolor="0.3")
for m in bp["medians"]:
    m.set(color="crimson", linewidth=2)
```

`patch_artist=True` is needed before boxes can be filled. Without it they're unfillable outlines and `set_facecolor` does nothing, silently.

The property dicts &mdash; `medianprops`, `boxprops`, `whiskerprops`, `flierprops` &mdash; do the same at call time and are often tidier.

## Violin internals

`violinplot` returns a dict too, with `"bodies"` and optional `"cmedians"`, `"cmeans"`, `"cbars"`.

By default it draws the extrema and no median. This Is an odd choice. `showmedians=True` is nearly always wanted.

`widths` controls the max thickness, and `bw_method` the smoothing. A number, or `"scott"` / `"silverman"`. Halving the bandwidth roughly doubles the visible detail and the visible noise.

Because the two halves are mirror images, one half is redundant. A **half violin** paired with the raw points on the other side uses the space better. Is built by clipping the body path. More work than it sounds. Worth it for a figure that will be published.

## Choosing between them

**Box** &mdash; many groups, when the quartiles are the summary you want and shape isn't expected to be notable.

**Violin** &mdash; when shape matters and the samples are large enough for a density guess to mean a thing, roughly a hundred per group.

**Strip or swarm** &mdash; small samples. Here The single values are the honest display.

**Box plus points** &mdash; the all-round answer under about fifty per group.

**Histogram grid** &mdash; when the shapes are the subject and there are few enough groups to give each a panel.

The mistake is treating the box plot as the default for all spread compare. This Is how bimodality goes unnoticed.

## Outliers

The points beyond the whiskers are labelled outliers. The label is doing more work than the statistics support.

They're simply points more than 1.5&times;IQR from the box. On most times spread data about 0.7% of findings qualify. A sample of a thousand makes seven "outliers" that are nothing of the kind.

On skewed data the rule flags far more, all on one side. This Is a property of the spread rather than of the points.

So: a point beyond a whisker is worth looking at and isn't evidence of an error. `showfliers=False` hides them when they're distracting. `whis=(5, 95)` changes the rule to percentiles. This Is often more readable.

## Sample size

A box plot looks the same for twelve findings and twelve thousand. This Is a real weakness when groups differ in size.

Three ways to show it:

**Width scaled to n** &mdash; `widths=` accepts a list. Scaling by the square root of the count is standard.

**The count in the tick label** &mdash; `"group a\n(n=12)"`.

**The points overlaid**, which shows the sample size right.

Without one of these, a group of eight and a group of eight hundred are presented as equally solid. The reader has no way to know.

## Ordering and grouping

With more than a handful of groups, the setup is most of the chart.

**Sort by median** unless the groups have a natural order. It turns a search into a reading.

**Group related groups together** and split the groups with space. This `spots=` allows. Passing `[1, 2, 3, 5, 6, 7]` leaves a gap between two clusters.

**Use colour for the grouping**, not for the single boxes. The colour carries the structure rather than repeating the labels.

**Consider a link line** &mdash; the total median, a target &mdash; drawn across the whole axes. This Turns each box from an isolated summary into a compare.

With those, twenty boxes on one chart remains readable. Without them, six is already hard.

## In summary

A box is five numbers, and whiskers reach the furthest point within 1.5&times;IQR rather than a fixed multiple.

The display exists to compare many groups at once. This Is what it does better than anything else.

It hides shape, and namely hides bimodality. Two groups mixed together give a box that looks plain.

A violin restores the shape and adds a bandwidth you didn't choose, plus tails extending past the seen data.

Under about fifty points per group, showing the points with jitter is more helpful than either.

And `patch_artist=True`, `showfliers=False` and `vert=False` are the three args that come up most. Fillable boxes, no double-drawn outliers. Flat layout for wordy labels.

## Beeswarm and the alternatives

A strip plot with random jitter shows each point and lets some of them share by chance.

A **beeswarm** places the points deterministically so none share. This Reads better and isn't built into matplotlib. Seaborn's `swarmplot` is the usual route. It refuses to plot when there are too many points to place. This Is a fair failure.

A **rain cloud** mixes three: a half violin for the shape, a box for the summary. The points below. It's the most full display of a spread compare and takes the most space. This Is the trade.

For most work the sorting is: points if the sample is small, box if there are many groups, box plus points in between. A violin when the shape is truly the question and the samples are large enough to guess it.

What matters more than the choice is knowing what each one hides. This Is the theme of this whole module.

## A closing note

each spread display is a compromise between completeness and comparability.

The points show all and compare badly past a few groups. The box checks many groups and hides the shape. The violin restores the shape and adds a smoothing choice. The histogram shows one spread well and a few badly.

There's no display that does all of it. This Is why the handy skill is knowing what each one discards rather than having a favourite.

The exact thing worth remembering: a box plot can't show bimodality. Bimodality often means two groups have been mixed. Which is often the most key fact about the data. Looking at a histogram of each group once, before settling on boxes for the compare, costs a minute and blocks the failure this module is mostly about.

## The short version

Both displays trade completeness for comparability. Both hide a thing exact. The box hides shape, the violin hides its own smoothing choice.

Knowing what each discards is more handy than preferring one. Looking at a histogram of each group once before choosing is what blocks the bimodality failure this module exists to show.

## Reading the code back

A box plot is one call with three args worth passing. Patch_artist to make the boxes fillable, showfliers to control the outliers. Vert to choose the orientation. The choices before it are which groups, in what order. Whether the points should be shown as well - and those are what find whether the chart works.
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

`df.plot()` draws each column as a line against the index, adds a legend labelled with the column names. Formats the x axis rightly for the index type.

For a time-indexed frame that is a dated axis, sensible tick spacing, one line per column and a legend. From one call. Doing the same in raw matplotlib is five or six lines.

That is the case for using it: for exploration. For the common chart types, it's simply faster.

## It is a thin wrapper

The key thing to know is that `df.plot` **returns a matplotlib Axes**, and accepts one through `ax=`.

That means it isn't a split system. all in this track applies to the result:

```python
fig, ax = plt.subplots()
df.plot(ax=ax)
ax.set_title(...)
ax.axhline(...)
```

`ax=` also matters for a other reason: without it, pandas creates its **own** figure. A `df.plot` call inside a loop over subplots draws each chart in a new figure rather than the panel you intended. This Is a common and confusing result.

## kinds

`kind=` selects the chart: `"line"` (the default), `"bar"`, `"barh"`, `"hist"`, `"box"`, `"kde"`, `"area"`, `"pie"`, `"scatter"`, `"hexbin"`.

`df.plot.bar()` is equal and reads better, with the edge that an editor can autocomplete the method names and their args.

`scatter` and `hexbin` need `x=` and `y=` naming columns. They take two vars rather than plotting all against the index.

Most keyword args are passed through to matplotlib. `alpha`, `color`, `linewidth` and the rest work as expected.

## The frame's shape is the chart

This is the part that finds whether the output is what you wanted.

Each **column** turns a series. Each **row** turns a spot on the x axis.

So a frame with quarters as rows and products as columns gives grouped bars with one cluster per quarter. If you wanted one cluster per product, the frame needs transposing. `df.T.plot(kind="bar")`. Not a other plotting arg.

When a chart comes out grouped the wrong way, the fix is nearly always a `pivot`, a `groupby().unstack()`, or a transpose. That is the reshaping module doing its job: **getting the frame into the right shape is the plotting work**. The plot call is then trivial.

`stacked=True` stacks bars or areas.

## subplots=True

`df.plot(subplots=True)` gives one panel per column and returns an **array** of axes rather than one.

It's the fastest route to small multiples. It has a default worth knowing. The y axes are **split**. The panels aren't close. `sharey=True` fixes it, and without it a panel showing a range of 0&ndash;2 sits beside one showing 0&ndash;2000 at the same visual height.

`layout=(2, 3)` arranges them in a grid rather than a column.

## When to drop back

pandas covers the common cases and exposes nothing beyond them.

Reach for matplotlib when you need:

annotations, arrows or text;

link lines and shaded regions;

a second y axis, or a secondary unit;

fine control of ticks, formatters or scales;

anything drawn conditionally &mdash; highlighting one series, greying the rest.

The good news is that this isn't a switch. `df.plot(ax=ax)` for the data and `ax.` methods for all else is the normal way to work. It's why the wrapper is worth having.

## And when to leave both

For statistical charts &mdash; faceted grids, regression plots with trust bands, cat scatter with built-in jitter &mdash; seaborn sits on top of matplotlib and makes them in one call, returning matplotlib objects you can adjust later.

For interactive charts in a browser, Plotly or Altair. matplotlib's interactivity is limited and not its purpose.

Knowing where matplotlib stops is part of using it well. It's a drawing library that happens to have statistical conveniences, not a statistical graphics system.

## What pandas adds

Beyond convenience, three things are truly easier through pandas.

**The index turns the x axis**, with date formatting handled. That alone drops a few lines for any time series.

**Column names become labels**, so the legend is built from the data rather than from a list you maintain apart.

**Groupby output plots directly**: `df.groupby("k")["v"].sum().plot(kind="barh")` goes from raw rows to a chart in one line, because the aggregation produces exactly the index-and-values shape the plot wants.

That last point is the real workflow: reshape until the frame *is* the chart, then plot it.

## Common frame shapes

**A time-indexed frame, one column per series** &rarr; `df.plot()` gives a multi-line chart.

**A frame indexed by group, one column per group** &rarr; `df.plot(kind="bar")` gives grouped bars.

**A long frame** &mdash; one row per finding with a group column &mdash; needs pivoting first: `df.pivot(index=..., columns=..., values=...)`.

**A group-by result with two keys** &rarr; `.unstack()` puts one key into columns, giving the wide shape the plot needs.

Recognising which of these you've, and which the chart needs, is most of the work. The plot call is one line either way.

## Where pandas gets in the way

`df.plot` has its own views that at times conflict with matplotlib's.

It sets its own tick locators for date axes. This Are often good and are awkward to replace later. Setting a matplotlib locator on an axes pandas has already formatted at times has no effect. Plotting with `ax.plot(df.index, df[col])` instead gives back full control.

It creates a figure if not given one. This Is the `ax=` issue.

And `secondary_y=True` exists and makes a twin axis with all the problems from that module, plus a legend that is harder to assemble.

For anything beyond the standard cases, dropping to `ax.plot(df.index, df["col"])` costs one line and drops the ambiguity about who owns the axes.

## Categorical bar charts

`df.plot(kind="bar")` uses the index as the groups and draws them at int spots, with the labels rotated 90 degrees by default.

`rot=0` stops the rotation. `kind="barh"` is often better still, for the reasons in the bar module.

Sorting is a pandas step, not a plotting one: `df.sort_values("v").plot(kind="barh")`. That is a small example of the general pattern. The data handling belongs in pandas. The plot call should be trivial.

## Beyond pandas

`df.plot` covers the standard charts. seaborn covers the statistical ones. Faceted grids, regression with bands, cat scatter with jitter built in. And returns matplotlib objects. The same adjustment methods apply later.

The three layers work together: pandas for the data, seaborn for the statistical display, matplotlib for the final control. Knowing which layer a problem belongs to is most of using them well. The answer for "make this exact thing look right" is almost always the bottom one.

## A complete example

The common shape of real plotting code. Here The data work dominates:

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

That ratio is normal, and it's why reshaping is a plotting skill.

## Pitfalls

**Losing `ax=`**, so the plot lands in its own figure.

**The wrong frame shape**, giving bars grouped by the wrong var.

**Rotated labels by default** on `kind="bar"`, fixed with `rot=0` or by using `barh`.

**`secondary_y=True`**, which is a twin axis with all its problems.

**given shared axes** with `subplots=True`. Here The default is split.

**A datetime index that is really strings**, giving a cat axis with no gaps.

The last is worth checking with `df.index.dtype` before wondering why the spacing looks wrong.

## The three layers

Real plotting code sits across three libraries. Knowing which one owns a problem saves a lot of searching.

**pandas** owns the data: filtering, grouping, pivoting, resampling. If the chart is grouped by the wrong thing, or the bars are clustered incorrectly, or a date axis is behaving like a group, the fix is here. In the shape or the dtypes, not in the plot call.

**seaborn** owns statistical display: faceting, regression with bands, cat scatter with jitter, spread checks. If you're writing twenty lines to build a grid of conditioned plots, this layer already has it.

**matplotlib** owns the drawing: annotations, link lines, exact ticks, colour control, layout, saving. all the other two give is a matplotlib object. This layer is always on hand underneath.

The common mistake is trying to solve a data problem in the plotting call. Adding args to `df.plot` to fix a grouping that should have been a `pivot`.

## In summary

`df.plot()` draws each column against the index and builds the legend from the column names.

It returns an Axes and takes one. This Is what makes it a shortcut rather than a split system. And `ax=` is needed, or a plot inside a subplot loop creates its own figure.

The frame's shape is the chart: columns are series, rows are groups. A chart grouped the wrong way needs a transpose or a pivot.

`subplots=True` gives small multiples and split y axes unless you say else.

Reach for matplotlib for annotations, thresholds, shading and exact control. And mix freely. It's the same Axes object either way.

## Reshaping is the plotting work

The recurring lesson of this module is worth stating on its own.

The plot call is often one line. The work is getting the frame into a shape where that one line is correct.

**A wide frame** &mdash; one column per series, index as x &mdash; is what a multi-line chart or a grouped bar chart wants.

**A long frame** &mdash; one row per finding &mdash; is what seaborn and most statistical tools want.

**An aggregated frame** &mdash; one row per group &mdash; is what a bar chart of totals wants.

Moving between them is `pivot`, `melt`, `groupby().agg()` and `unstack`, all covered in the pandas track.

When a chart comes out grouped by the wrong var, or with the series and groups swapped, or with one line where there should be five, the fix is almost never an arg to `plot`. It's the shape of the frame. Recognising that at once saves a lot of time reading plotting docs for a thing the data work should have solved.

## A closing note

`df.plot` is a shortcut, and its value is scaled to how standard the chart is.

For a quick line chart of a time-indexed frame it's unbeatable. One call, correct axis, legend included. For anything with an annotation, a threshold, a highlighted series or a exact tick format, it stops helping and matplotlib underneath does the work.

The two together are the normal way to write plotting code. The boundary isn't a choice you make once. `df.plot(ax=ax)` followed by half a dozen `ax.` calls is a just right plain chart.

What is worth internalising is that most plotting problems are data problems. When the chart is grouped wrongly, or has too many lines, or shows a group as a number, the fix is in the frame.

## The short version

`df.plot` is a shortcut that returns a matplotlib Axes. This Is what makes it a convenience rather than a split system.

Its limits arrive quickly, and the boundary isn't a choice made once: `df.plot(ax=ax)` followed by half a dozen `ax.` calls is plain code. And most plotting problems are data problems.
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

**How do these groups compare?** A bar chart. Flat. The labels read. Sorted. So The ranking is direct.

**Is there a link between these two things?** A scatter plot.

**How is this spread?** A histogram for one group, box plots or the points themselves for a few.

That covers the large majority of real charts. When none of them fits, it's often because the question hasn't been stated just. Stating it finds the chart.

The corollary: decide the question first. A chart made by plotting the data and then deciding what it shows is often a chart of a few things at once.

## Why encodings matter

Some visual channels are read more accurately than others. Roughly, in order:

**spot** along a common scale. The most accurate. This is what a line, a scatter and a dot plot use.

**Length** from a common baseline &mdash; nearly as good. Bars.

**Angle and area** &mdash; noticeably worse. Pies, bubbles.

**Colour intensity** &mdash; worse again, and good only for sorting, not for reading values.

That sorting is why a bar chart beats a pie chart, why bubble size should never carry the main message. Why a heatmap needs its numbers written in when the values matter.

## Pie charts

A pie asks the reader to compare angles. With two or three slices of an obvious whole, that is fine. The shape sends "parts of a total" at once.

With five similar slices it fails: ranking them by eye is truly hard. This Is why almost each pie chart in the wild has its percentages printed on it. An admission that the picture isn't doing the work.

The same numbers as a sorted flat bar chart are trivially readable. The bar chart also shows the magnitudes rather than only the proportions.

Donut charts are pies with the middle removed. This Makes them slightly worse. The angle is now inferred from an arc.

## Dual axes

The other display worth avoiding, covered fully in its own module.

The short version: two series on split scales have no defined link. Where they cross is found by the limits you chose. Readers see the crossing as a finding.

Stacked panels sharing an x axis, or indexing both series to a common base, say the same thing without inventing a fact.

## Small multiples

Six series on one axes is a hairball with a legend. The reader traces each colour, loses it in a crossing, and consults the legend again and again.

Six small panels, sharing axes, let them see each shape right and compare across panels. The shared scale is what makes the compare valid. The panel title replaces the legend.

This is one of the most solid gains on hand. Matplotlib makes it one call: `plt.subplots(2, 3, sharex=True, sharey=True)`.

The trade-off is that checking two exact series is harder when they're in other panels. If the chart is about one compare, put those two on one axes. If it's about the set, use multiples.

## Highlighting

When one series is the subject and the others are context, say so with colour. The subject in a strong colour and heavier line, the rest in light grey.

The grey lines still give the range and the shape of the group. Nothing is lost. The reader's eye goes to the subject at once. No legend is needed if the highlighted line is labelled at its end.

This is more good than an annotation. It directs focus by contrast rather than by adding another thing to read.

## The checklist

Before a chart leaves your screen:

Does the **title state the finding**, rather than naming the vars?

Do the **axis labels carry units**?

Is the **baseline** right &mdash; zero for bars. Does a truncated line axis need saying?

Is anything **hidden** &mdash; overplotted points, a series behind another, a group off the edge?

Is the **non-data ink** doing work. The grid, the frame, the legend, the tick marks?

Would it **live greyscale**, and colour-vision deficiency?

Is there **one message**, or a few competing? Two charts each saying one thing beat one saying both.

None of these is about matplotlib. This Is the point. The library will draw what you ask. The choices are yours. They're what makes a chart worth looking at.

## Ranking, not just comparing

"Compare groups" splits into two questions that want other charts.

**Which is biggest?** A sorted flat bar chart, and nothing else comes close.

**How does each compare with a link?** A dot plot against a line, or a bar of the gap from the link. This Puts the compare on the axis instead of asking the reader to subtract.

The second is under-used. A chart of "actual minus target" answers the question right. Here Two bars per group makes the reader do the math.

## Part-to-whole

Four displays, in falling order of how well they work.

**Stacked bar normed to 100%**. Close across groups. Readable for four or five parts.

**A single stacked bar** &mdash; fine for one composition with few parts.

**Small multiples of the parts**. Better when the single trends matter more than the composition.

**A pie** &mdash; two or three parts. Only when "these are shares of one thing" is the message rather than the values.

Treemaps handle many parts and are hard to compare just. They suit tree more than proportion.

## Distribution over time

A frequent question with no single good answer.

**A line of the median with a shaded interquartile band** works well and shows the middle and the spread.

**A box plot per period** works when the periods are few.

**A heatmap of time against value bins** shows the full spread and takes practice to read.

**Single lines, greyed** &mdash; a spaghetti plot with a highlighted median &mdash; works when the number of entities is modest and their single paths matter.

The wrong answer is a line of the mean alone. This Hides all that changed about the spread.

## Two variables plus a third

A scatter with colour is the first choice. A scatter with size is second and much weaker.

If the third var is cat with few levels, **small multiples**. One scatter per level, shared axes. Beat colour. Checking panels is easier than separating shared colours.

If it's smooth, colour with a sequential map and a colorbar.

Encoding four vars on one chart is often a mistake. The fourth turns decoration. The chart takes longer to read than two charts would.

## The general rule

each chart makes the reader do some work. The choice of chart decides how much.

A sorted bar chart asks them to read a ranking that is already visible. An unsorted one asks them to sort. A pie asks them to compare angles. A dual-axis chart asks them to hold two scales at once. A twelve-line chart asks them to trace colours through a legend.

The best chart is often the one that has already done the work. Sorted, filtered, highlighted, labelled. Leaving the reader only the conclusion.

## Charts for a specific audience

The same data justifies other charts based on who is reading.

**For yourself, exploring** &mdash; density, defaults, many panels. Nothing needs labelling because you know what it's. Speed matters more than polish.

**For a colleague** &mdash; labelled, titled, one message per chart, and the caveats visible.

**For a presentation** &mdash; one chart, one message, large text, minimal link material. The conclusion in the title. The reader has seconds and can't zoom.

**For a doc** &mdash; sized for the column, with a caption carrying the detail that would clutter the chart.

The mistake is showing an exploratory chart to an audience. This Is how a chart with eleven series and no title ends up in a meeting.

## The one-message rule

The most handy constraint in charting is that a chart should say one thing.

It forces the choices: which var is on which axis, what to highlight, what to leave out, what the title claims.

A chart trying to say three things often says none. The reader can't tell which of the three to look at. The elements supporting each compete with the others.

Two charts each saying one thing take the same space and send more. Splitting is nearly always the right answer when a chart feels crowded. "what is this chart for?" is the question that resolves most design args about it.

## Redesigning a chart

A hands-on exercise: take a chart that isn't working and improve it without changing the data.

The sequence that often helps, in order:

**State the message in a sentence.** If that is hard, the chart is trying to do more than one thing.

**Drop all the sentence doesn't need.** Series, gridlines, the legend if direct labels would do, tick marks, the box around the plot.

**Sort, if the order is any.**

**Highlight the subject** and grey the rest.

**Put the sentence in the title.**

**Label the thing the sentence refers to.**

Six steps, none of which needs new data. Together they turn a chart that shows the numbers into one that makes the point. Most charts improve much and the code gets shorter. Most of the steps drop a thing.

## In summary

Time is a line, groups are a sorted flat bar, links are a scatter, spreads are a histogram or a box.

spot is read most accurately, then length. Angle and area much less well. That sorting is why bars beat pies and why bubble size should never carry the main message.

Dual axes put the crossing point under your control rather than the data's.

Small multiples beat many series on one chart when the question is about the set. Highlighting beats a legend when it's about one.

And the best chart is the one that has already done the reader's work. Sorted, filtered, labelled, with the conclusion in the title and nothing else competing for focus.

## A closing note

all else in this track is method. This module is the part that decides whether the method was worth using.

The recurring theme is that a chart is a piece of exchange. The reader's effort is the cost. Sorting, filtering, highlighting and labelling all move work from the reader to the author. The best charts have had the most work moved.

The chart types worth avoiding. Pies with many slices, dual axes, truncated bars &mdash; are all cases where the display asks the reader to do a thing people do badly, or invites a conclusion the data doesn't support.

And the most handy single constraint remains the simplest. One chart, one message. Almost each design question resolves once that is decided.

## Reading the code back

Choosing is done before any code: what question, what encoding, what to leave out, what the title will claim. A chart written from those four answers is often short. Most of the length in plotting code comes from adjusting a display that wasn't the right one to begin with.
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
intro: What makes a figure slow. What to do when there are more points than pixels.

## Artists, not data

matplotlib's cost is dominated by the number of **artists** it manages, not the number of data values.

One `plot` call with a million points creates one `Line2D`. A loop making two thousand calls creates two thousand artists, each with its own properties, transform and draw pass. And that is far slower even with a fraction of the data.

The rule that follows is the same one as NumPy and pandas: **pass arrays, don't loop**. Where a loop is unavoidable, `LineCollection` and its relatives draw many segments as a single artist.

## plot versus scatter

For many points that all look alike, `ax.plot(x, y, "o")` is faster than `ax.scatter(x, y)`.

`scatter` builds a set that carries a size and colour per point. That is what it's for. When those don't vary, the machinery is unused and paid for anyway.

So: `scatter` when size or colour codes a thing, `plot` when it doesn't.

## More points than pixels

A seven-inch figure at 100 dpi is 700 pixels wide. Two hundred thousand points is roughly 285 per pixel column. 284 of them are drawn just on top of others.

They cost time and file size and contribute nothing visible.

Reducing them isn't a compromise. It's dropping a thing the reader could never see. Two approaches, and the gap matters.

**Subsampling** &mdash; `x[::step]` &mdash; is trivial and drops what it doesn't land on. A single-sample spike disappears. For smooth, dense data that is fine. For anything where extremes matter it isn't.

**Aggregating** &mdash; binning by x and drawing the min and max in each bin as a filled band &mdash; keeps the envelope. The chart looks nearly same to the full data because the envelope is what the eye was reading anyway, and genuine spikes live.

The fourth editor puts one real spike in the data and shows subsampling losing it while binning keeps it.

For scatter data, the equal is `hexbin` or `hist2d`. This Replaces overplotted points with measured density.

## File size

Vector formats store each element. So A scatter of 30,000 points is 30,000 objects in the PDF. Such files are slow to open and large.

`rasterized=True` on the artist stores **that layer** as pixels while all else. Axes, ticks, labels, title &mdash; stays vector:

```python
ax.scatter(x, y, s=2, rasterized=True)
fig.savefig("out.pdf", dpi=200)
```

The result is a small file with sharp text and a pixel-based data layer. This Is just the right trade for a dense scatter in a doc. The `dpi` at save time controls the detail of the rasterised part.

## Drawing loops

making many similar charts &mdash; one per group, per day, per file &mdash; spends most of its time creating figures, not drawing data.

Two levels of fix.

**Close each figure**: `plt.close(fig)`. This is not an optimisation so much as a requirement; without it the figures accumulate, matplotlib warns after twenty, and memory grows without bound.

**Reuse the figure**: create it once, update the artist's data each iteration, and re-save:

```python
line.set_ydata(new_y)
ax.relim(); ax.autoscale_view()
fig.savefig(path)
```

`relim` and `autoscale_view` are needed because setting data doesn't rescale the axes.

This is usefully faster when the layout is same between charts. It's the same method animations use.

## When matplotlib is the wrong tool

matplotlib renders once and isn't built for interactive exploration of large data.

**Datashader** aggregates hundreds of millions of points into an image. Is the right answer above a few million.

**Plotly, Bokeh, Altair** give pan-and-zoom in a browser. This Matplotlib's interactive backends do only awkwardly.

**mpl-scatter-density** and similar handle the dense-scatter case within matplotlib.

The signal is often the size: if a figure takes more than a few seconds to draw, the answer is a other approach rather than a faster matplotlib.

## Measuring draw time

Timing a matplotlib figure needs care. The drawing is lazy. Creating artists is fast and nothing is rendered until the canvas is drawn.

```python
t = time.perf_counter()
fig.canvas.draw()
elapsed = time.perf_counter() - t
```

Without the clear `draw()`, the timing measures only object creation and reports numbers far too good.

The first draw of a session also pays for font cache and backend init. This Can be a second or more. A warm-up figure before timing anything is the gap between a real compare and a misleading one. The editors in this module do just that.

## Where the time goes

For a common figure, in rough order:

**Artist creation** when there are many artists.

**Rendering** the artists to pixels.

**Text layout**, which is more costly than it sounds. A chart with hundreds of tick labels or annotations spends real time measuring glyphs.

**Font cache building**, once per setting, and at times minutes on first run.

**Saving**, above all to vector formats with many elements.

The hands-on results: fewer artists, fewer text objects, and rasterised layers for dense data.

## Interactive versus file output

An interactive backend redraws on each pan, zoom and resize. A figure that takes two seconds to draw is unusable interactively while being just right fine as a file.

That changes the trade-off. For a saved figure, drawing a million points slowly once is acceptable. For a thing a person will change, the point budget is far smaller. Downsampling isn't an tuning but a need.

`fig.canvas.draw_idle()` defers a redraw until the event loop is free. This Is what interactive tools use to stay responsive.

## Animations

`FuncAnimation` re-renders a figure per frame. So The per-frame cost is what matters.

`blit=True` redraws only the artists that changed. This Is much faster and needs the update function to return them.

The same reuse principle as the drawing loop applies. Create the artists once, update their data each frame with `set_data`. Never call `plot` inside the update.

## The wider picture

matplotlib is designed for correctness and control rather than throughput. Its limits are reached sooner than people expect. Tens of thousands of artists, or a few million points.

The escape routes, roughly by problem:

**Too many points** &mdash; aggregate, or use datashader.

**Too many artists** &mdash; sets instead of loops.

**Too slow interactively** &mdash; a browser-based library.

**Too many figures** &mdash; reuse, and close.

The one that matters most is the first. Most speed problems in matplotlib are really a display problem. Drawing more than the reader can see. This Costs time and sends nothing.

## Font cache and first-run cost

A surprise on a fresh setting: the very first matplotlib figure can take a long time, at times minutes, while the font cache is built.

It happens once per setting and is cached later. It's a common source of "matplotlib is incredibly slow" reports from people who ran it once in a new holder.

In a holder or CI image, drawing one throwaway figure at build time moves the cost out of the first real run.

`matplotlib.get_cachedir()` shows where it lives, and deleting it forces a rebuild. Which is the fix when a newly installed font isn't being found.

## A performance checklist

When a figure is slow, in the order worth checking:

**How many artists?** `len(ax.lines) + len(ax.sets) + len(ax.patches)`. Hundreds is fine. Tens of thousands is the problem.

**How many points, against how many pixels?** If it's more than a few per pixel column, the extras are invisible.

**Is it in a loop?** Are figures being closed?

**Is it text?** Hundreds of annotations or tick labels cost real time.

**Is it the save?** Vector output of dense data.

**Is it the first run?** The font cache.

Most slow figures are the first two. Both are fixed by drawing less rather than by drawing faster.

## Budgets

Rough numbers, which are more handy than general advice.

**Artists**: up to a few thousand is comfortable. Tens of thousands is slow. Hundreds of thousands will not finish in a reasonable time.

**Points in one artist**: a million is fine for a line, because it is one object. The renderer handles it far better than a million separate objects.

**Visible resolution**: a 7-inch figure at 100 dpi has 700 columns. Above a few thousand points, most are invisible.

**Text objects**: hundreds are noticeable; thousands dominate.

**Interactive redraw**: anything above about 100 ms per draw feels sluggish when panning.

**Vector output**: above roughly 10,000 elements the file becomes slow to open.

Those thresholds explain most of the hands-on advice. Pass arrays rather than looping, aggregate before plotting, rasterise dense layers, and reuse figures in loops.

## In summary

Cost is driven by artists, not data points. One call with an array beats a loop of calls by a wide margin.

`plot` beats `scatter` when the markers are uniform.

Past a few thousand points there are more points than pixels. The extras cost time while communicating nothing.

Subsampling drops genuine extremes. Binning to a min/max envelope keeps them, and looks the same.

`rasterized=True` keeps a vector file small while leaving the text sharp.

Creating figures is the costly part of a drawing loop. Reuse them. And close them even so, because matplotlib won't.

And when a figure takes seconds to draw, the answer is often a other approach rather than a faster matplotlib.

## When to stop optimising

A figure that takes two seconds to draw once. Is then saved, is fine. There's nothing to fix.

The cases that justify effort are narrower than they look:

**A figure regenerated often** &mdash; in a dashboard build, a CI job, a loop over thousands of groups. The cost times.

**An interactive figure**, where each pan and zoom pays it again.

**A figure that doesn't finish**, or exhausts memory. This Is a correctness problem rather than a speed one.

**A file too large to open**. This Is the vector-scatter case.

Outside those, drawing time is often a rounding error next to the data work that preceded it. The effort is better spent on whether the chart says the right thing.

That is worth stating because speed is easy to optimise and easy to over-optimise. A fast chart no one can read isn't an gain.

## One more thing

`fig.canvas.draw_idle()` requests a redraw at the next opportunity rather than at once. This Is what keeps an interactive figure responsive when a few things change at once.

For a script it makes no gap. The draw happens at save time either way. It matters in a callback that updates a few artists. Here An direct draw per change would render the figure a few times for one logical update.

## The short version

Nearly each speed problem in matplotlib is a display problem in disguise: drawing more than the output can show.

Fixing it by drawing less. Aggregating, subsampling with care, rasterising a dense layer &mdash; makes the chart faster and often more readable also. This Is unusual among optimisations.

## Reading the code back

speed work here is a short list checked in order. Is there a loop creating artists, are there more points than pixels, are figures being closed, is the output vector with a dense layer in it. Four questions. The first two account for nearly all. None of them needs knowing anything about how matplotlib renders.
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

The shape matters more than the size. The size is often adjusted at display time anyway.

**Time series want width.** A hundred and fifty points in three inches is 50 per inch. The shape of the series is compressed into noise. The same data in nine inches is readable. Wide-and-short. Something like 4:1. Is a good default for a single time series.

**Two-var scatters want to be square**. Neither axis is visually privileged and a link isn't exaggerated by the aspect ratio.

**Ranked bar charts want height scaled to the number of bars.** Twenty groups in three inches gives bars a few pixels apart. The figure should grow with the data.

`figsize` interacts with font size: text is a fixed physical size. A small figure has proportionally larger text. That is why shrinking a figure to fit a slide makes the labels look huge. Why the fix is to set both together.

## Margins

matplotlib leaves a 5% margin beyond the data at each end, controlled by `axes.xmargin` and `axes.ymargin`.

It exists so points don't sit just on the frame, and it's often right.

It's wrong when the data should reach the edge. A filled area, a time series ending at today's date, an image. `ax.margins(x=0)` drops it on one axis, and `ax.margins(0)` on both.

`ax.margins(y=0.15)` grows it, which is how you leave room for labels above the highest point without hard-coding limits that break when the data changes.

## Space between panels

`fig.subplots_adjust(hspace=..., wspace=...)` sets the gaps as **fractions of the mean panel size**. `0.4` means a gap of 40% of a panel's height.

It also takes `left`, `right`, `top` and `bottom` as figure fractions. This Is how you reserve space at an edge.

These are what `tight_layout` and `constrained_layout` find for you. Setting them by hand is for when you want a exact look, or when the auto layout is fighting a thing you placed manually.

The two auto options differ: `tight_layout()` runs once after drawing. `constrained_layout=True` is set at creation and keeps adjusting as artists are added, handling colorbars and suptitles better.

## Things outside the axes

A legend positioned with `bbox_to_anchor` outside the axes is drawn outside the **figure** as well, and is simply cut off.

Three fixes:

`fig.subplots_adjust(right=0.78)` shrinks the axes to leave room. Predictable, and you choose the number.

`constrained_layout=True` works it out, including for colorbars.

`bbox_inches="tight"` at save time expands the saved image to include all. Note this makes the file larger than `figsize` implies, rather than shrinking the axes. A other result from the other two.

The same applies to long tick labels and axis labels. This Is why a rotated date axis so often looks cut off.

## Data aspect ratio

`ax.set_aspect("equal")` makes one unit of x occupy the same distance as one unit of y.

Without it, a circle plotted as `cos`/`sin` comes out an ellipse. The axes box is wider than it's tall while the limits are the same.

It's needed for anything where shape carries meaning. Maps, geometry, images, physical layouts. It's wrong for most statistical charts. Here The two axes have unrelated units and forcing them equal wastes space.

`ax.set_aspect(2)` sets a exact ratio, and `adjustable="datalim"` changes the limits rather than the box to achieve it.

## Putting it together

The last editor is a finished chart. Each line in it's one of the choices from this track. An aspect ratio suited to the data, limits that leave room for end labels, margins for breathing space, ticks at real spots, a faint grid below the data, two spines removed, direct labels instead of a legend, and a title that states the finding.

None of it's complicated. It's a dozen lines, applied on purpose. It's the gap between a default chart and one that looks like someone made it.

## Figure versus axes coordinates

Two coord systems place things on a figure. Mixing them up is a common source of misplaced elements.

**Figure coords** run 0 to 1 across the whole figure. `fig.text`, `fig.add_axes`, `fig.legend` use them.

**Axes coords** run 0 to 1 across one axes. `ax.text(..., transform=ax.transAxes)` uses them.

A note that belongs to the whole figure. A source line, a caption. Goes in figure coords and stays put when panels change. A note about one panel goes in that panel's axes coords.

`fig.subplots_adjust` also takes figure coords for `left`, `right`, `top` and `bottom`. This Is how you reserve a strip at an edge.

## Adding an axes anywhere

`fig.add_axes([left, bottom, width, height])` places an axes at an exact spot in figure coords, outside the grid fully.

Two uses come up: an inset showing a zoomed region. A colorbar positioned just rather than stolen from a panel.

`ax.inset_axes([x, y, w, h])` does the same in the parent's coords. This Is easier for an inset because the spot is scaled to the panel it belongs to.

`ax.indicate_inset_zoom(inset_ax)` draws the connecting lines between the region and the inset. This Is what makes the link readable.

## Spacing that reads

A few rules give figures that look seen as rather than default.

Leave more space **between** groups than within them. A grid of panels with a `wspace` smaller than the margin around the grid reads as a unit.

Keep the **left margin** wide enough for the y label at its final font size. This Is what `constrained_layout` does and hand-tuning often gets wrong when the font changes.

Give a **suptitle** room, or it collides with the top row's titles. `fig.suptitle(..., y=1.02)` with `tight_layout` is a common fix and is fragile. `constrained_layout` handles it properly.

Don't centre a title over a grid that has a colorbar on one side. The visual centre and the geometric centre differ.

## Sizing for a destination

The figure should be sized for where it will be seen.

**A slide** is wide and viewed from a distance: fewer elements, larger text, `figsize` around 10&times;5.6 for 16:9.

**A doc column** is narrow: around 3.5 inches wide for a two-column paper. Text sized so that the figure needs no scaling. Scaling a figure in a doc is what makes its labels the wrong size scaled to the body text.

**A web page** is var. So A raster at 2&times; the display size and a `max-width` in CSS is the usual approach.

The mistake is drawing at a default size and scaling later. This Changes the text size scaled to all else. Sizing at the destination's dims and choosing the font so is the fix.

## The last pass

Before a figure is finished, three checks that are all layout:

Is anything cut off at the edges? Save it and look at the file, not the screen.

Is the text a sensible size scaled to the figure at its final display size?

Is there enough space that nothing touches anything else. Labels to spines, title to panels, legend to data?

None of these change what the chart says. All of them change whether it looks like someone finished it.

## Insets

An inset shows a zoomed region or a small companion chart inside the main axes.

```python
inset = ax.inset_axes([0.6, 0.55, 0.35, 0.35])
inset.plot(x, y)
inset.set_xlim(a, b)
ax.indicate_inset_zoom(inset, edgecolor="0.5")
```

The spot is in the parent's axes coords. So It moves with the panel.

`indicate_inset_zoom` draws the rectangle on the main axes and the connecting lines. This Is what makes the link legible. An inset without it's a floating chart the reader has to read.

Insets suit a long series with an notable short window. A scatter with a dense cluster worth magnifying. They don't suit anything the reader needs to compare just with the main axes, because the scales differ.

## Layout that survives regeneration

Hand-tuned spacing breaks when the data changes: a longer label, an extra group, a bigger number needing more room.

Three habits keep a layout robust.

**Prefer `constrained_layout`** over hand-set `subplots_adjust`, because it recomputes rather than remembering.

**Size the figure from the data**. `figsize=(7, 0.35 * len(groups) + 1)` for a flat bar chart grows with the number of bars.

**Use `bbox_inches="tight"` when saving**, so anything that grew is still included.

A figure made weekly will meet all three problems eventually. The option is adjusting the numbers each time a thing changes.

## Text size and the destination

The most common layout error is a figure drawn at one size and displayed at another.

Text in matplotlib is given in **points**, a physical unit. A 10-point label on a 4-inch figure is a quarter of an inch. This Is a large fraction of the width. The same label on a 10-inch figure is the same quarter inch, and now looks small.

So scaling a figure after the fact changes the link between the text and all else. Which is why a chart shrunk to fit a doc column has labels that are suddenly too large. One enlarged for a slide has labels that are too small.

The fix is to draw at the final size. For a two-column paper, that means a figure about 3.4 inches wide with fonts chosen to be readable at that size. For a slide, something like 10 by 5.6 with fonts around 14 points.

`figsize` and `font.size` are one choice, not two.

## In summary

`figsize` is an aspect-ratio choice: width for time series, square for scatters, height scaled to the number of bars.

Margins default to 5% each side and should be removed when the data is meant to reach the edge.

`hspace`/`wspace` are fractions of panel size, and are what the layout managers find for you.

Anything outside the axes &mdash; a legend, long labels &mdash; needs room reserved, or it's cut off in the saved file.

`set_aspect("equal")` is needed where shape carries meaning and wasteful elsewhere.

And a figure should be drawn at the size it will be displayed. Text is a physical size and scaling later changes all about the balance.

## A closing note

Layout is the part of charting that gets the least focus and is most visible in the result.

A chart with the right data, the right type and the wrong spacing looks unfinished. Readers register that before they read anything. Labels touching the frame, a title colliding with a panel, a legend crowding the data, text at the wrong size for the display. All are cheap to fix and all cost credibility.

The methods are few: pick a figure size for the destination, let `constrained_layout` handle the spacing, reserve room for anything outside the axes. Check the saved file rather than the screen.

Doing that always is most of the gap between charts that look made and charts that look exported.

## The short version

Layout gets the least focus and is the most visible in the result.

Size for the destination, let a layout manager handle the spacing, reserve room for anything outside the axes. Look at the saved file. That is most of the gap between charts that look made and charts that look exported.
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
intro: The errors that give a chart which looks fine and isn't.

## Nothing appears

Three causes, distinguishable in a few seconds.

**No data.** `len(x)` and `len(y)`. An empty array plots without complaint.

**All missing.** `np.isnan(y).all()`. NaN is skipped. So An all-NaN series draws an empty line object.

**The view is elsewhere.** `ax.get_xlim()` and `get_ylim()`. Limits set before the data was added, or set to the wrong range, put the data outside the visible box.

`len(ax.lines)` sets apart "the draw call never ran" from "it ran and there's nothing to see". This Is often the fastest thing to check.

A fourth possibility in a script: you never showed or saved the figure. In a notebook figures display on its own. In a script they don't. `plt.show()` or `savefig` is needed.

## The plot lands somewhere else

`plt.plot` draws on the **current** axes. After `plt.subplots(1, 2)`, the current axes is the last one created. A stray `plt.plot` goes to the right-hand panel even so of intent.

In a notebook it's worse. The current figure is what the last ran cell created. Which, with out-of-order run, isn't always the one above.

`ax.plot(...)` drops the question. This is the hands-on reason the object-oriented API is worth the extra characters.

## Cropped output

A figure is saved at the size `figsize` declares, at `dpi` detail. The window you were looking at has nothing to do with it.

So a chart whose labels fit on screen can be cropped in the file. The first time this happens it looks like matplotlib lost the label.

`tight_layout()` or `constrained_layout=True` reserve the space. `bbox_inches="tight"` at save time expands the output to include all.

Rotated tick labels and long y-axis labels are the usual casualties. A chart type that doesn't need rotation. `barh` rather than `bar`. Avoids the problem fully.

## Colour that does not survive

Colours chosen to be visually distinct are often not distinct in **luminance**. Luminance is what remains in greyscale and what colour-blind readers lean on most.

Red, green and dark red are three obviously other colours with nearly the same brightness. Printed in black and white, they're one colour.

Two habits fix it: use a palette designed for the purpose. The viridis family, or Okabe&ndash;Ito for groups. And vary a second channel so colour is reinforcing rather than carrying the meaning.

The greyscale test is quick and catches most of it.

## Silent clipping

Setting limits that exclude data doesn't warn. The excluded points are simply not drawn. A bar taller than the axis runs off the top looking like any other tall bar.

That is a serious failure: the reader sees a chart where one group is four times the next largest. Has no way to know.

matplotlib can't warn about it. Clipping is often just what you want. Zooming into a region is a legitimate step.

The check is one line: compare `max(data)` against `ax.get_ylim()[1]`. Where a value is truly off-scale and the chart must stay zoomed, say so with an annotation giving the real number.

The related version is a group filtered out earlier in the pipeline and never noticed. This Is why checking the number of bars against the number of groups is worth doing.

## Figures left open

matplotlib keeps a link to each figure created through pyplot. They're never collected while it holds them.

After twenty, it warns: "More than 20 figures have been opened." That is a warning, not an error. The loop continues. Memory keeps growing until a thing else fails.

`plt.close(fig)` in the loop. `plt.close("all")` between sections of a notebook.

The threshold is `rcParams["figure.max_open_warning"]`, and raising it to silence the message is the wrong response to a real problem.

## A short list

Use `ax.` methods, not `plt.`.

Check the data before blaming the chart: length, NaN, limits.

Save with layout management, and look at the saved file rather than the screen.

Test in greyscale.

Compare the data's range against the axis limits.

Close figures in loops.

And the one from the design module that outranks all of them. Know what the chart is for before drawing it. None of these checks help a chart that is answering the wrong question.

## Mistakes of interpretation

Beyond the rote errors, a set of chart-level mistakes give output that is strictly correct and misleading.

**A truncated bar axis.** Length must be read from zero.

**Dual axes.** The crossing point is a choice, not a finding.

**Unshared axes across panels.** The layout invites a compare the scales don't support.

**An uncentred diverging colormap.** Half the data is coloured as though it had the opposite sign.

**A line through sparse points.** It asserts values between the findings.

**A pie with many slices.** The reader can't rank them.

**A mean without a spread.** Two very other spreads look same.

Each of these is a default that matplotlib will happily give. This Is why they're worth knowing as a list.

## Mistakes of omission

Things whose lack is the error:

No units on the axis labels.

No indication of sample size, when it varies between groups.

No note that an axis is logarithmic. This Changes how each distance on it should be read.

No statement of what an error bar shows.

No caption saying when the data is from and what it covers.

These cost a line each and are the gap between a chart that can be acted on and one that has to be asked about.

## Debugging a figure

A routine that resolves most problems quickly:

**Print the data.** Shape, range, count of NaN. Most "the chart is wrong" is "the data isn't what I thought".

**Check the artists.** `len(ax.lines)`, `len(ax.patches)`, `len(ax.sets)`. Did the draw call happen?

**Check the view.** `ax.get_xlim()`, `get_ylim()` against the data's range.

**Save it and look at the file**. This Is what other people will see.

**Look at it in greyscale**. This Catches encoding problems that colour hides.

In that order, because each is cheaper than the next.

## A pre-flight checklist

Before a chart is shared:

Does the title state the finding?

Do the axes have units?

Is the baseline right?

Are the panels close, if the layout implies they should be?

Is anything clipped, hidden or overplotted?

Does it work without colour?

Is there one message?

Is the source and date on it?

Eight questions, most answered in seconds. Between them they catch nearly all in this module.

## The general lesson

matplotlib will draw what it's asked. It has no view about whether the chart is honest, readable or answering a question anyone asked.

That is the right design for a library and it means the job sits with the person writing the call. The rote parts of this track. The args, the objects, the defaults. Are the easy half. The choices are the half that finds whether the chart was worth drawing.

## Mistakes that look like matplotlib bugs

A few actions get reported as bugs and are working as designed.

**A figure appears blank in a script**. Nothing called `show` or `savefig`.

**Colours skipped** &mdash; passing `c=` where `color=` was meant, or a colour list to a function taking a single colour.

**`set_facecolor` doing nothing on a box plot** &mdash; `patch_artist=True` wasn't passed.

**Ticks reappearing** after being set. A later autoscale replaced the locator.

**A legend showing one entry for many lines**. One `label` on a call that drew a few.

**Text invisible after `transparent=True`** &mdash; the foreground was never changed.

Each has a one-line fix and none of them raises. This Is what makes them frustrating rather than hard.

## Building the habit

The checks in this module are worth turning into a routine rather than remembering on their own.

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

It enforces the labels, applies the house treatment, and fails if a thing was skipped.

More often, the mistakes in this track fall into two groups. Things matplotlib won't tell you (clipping, wrong axes, cropped output) and things no one will tell you (a misleading baseline, an uninterpretable interval, a chart answering the wrong question). The first group is caught by checking. The second only by asking what the chart is for.

## The two kinds of error

It's worth separating them, because they're found in other ways.

**Errors matplotlib could tell you about but doesn't.** A plot on the wrong axes, a clipped bar, a cropped label, an empty series, a figure never closed. These are rote, they've definite answers. The checks in this module find them in seconds. They're also the ones that give a chart which is obviously odd once looked at.

**Errors no one can tell you about.** A truncated baseline, an uncentred diverging scale, a dual axis, a mean without a spread, a chart answering a question no one asked. These give output that is strictly correct and misleading. No check catches them because nothing is wrong with the code.

The first kind is fixed by looking at the chart. The second is fixed by asking what the chart claims and whether the data supports it. Which is a other activity. The one that matters more.

## In summary

An empty plot is empty data, all-NaN data, or limits pointing elsewhere. `len(ax.lines)` says whether the draw happened.

`plt.plot` lands on the current axes. This Is rarely the one you meant.

A figure saves at its declared size. Look at the file rather than the screen.

Limits that exclude data clip it silently. A too-tall bar looks like any other tall bar.

Colours of similar luminance vanish in greyscale.

Figures left open warn after twenty and keep consuming memory.

And the checklist that catches most of it. Title states the finding, units on the labels, correct baseline, nothing hidden, works without colour, one message, source and date. Takes under a minute and is the gap between a chart that is finished and one that is merely drawn.

## A worked debug

A concrete example of the routine, on the most common complaint: "the chart is wrong".

**Look at the data going in.** `df.shape`, `df.head()`, `df.dtypes`, `df.isna().sum()`. About half of all wrong charts are correct renderings of wrong data. This finds them before any plotting is checked.

**Check the artists.** Did the draw call happen. How many things did it create? A legend with one entry where five were expected means one call drew five lines with one label.

**Check the view.** Limits against the data's range.

**Check the axes.** Is the plot on the axes you think? `len(ax.lines)` on each.

**Look at the saved file**, not the screen.

**Look at it in greyscale.**

The order matters because each step is cheaper than the next. The first one resolves the majority. The instinct to start by reading matplotlib docs is often the slowest on hand route.

## The short version

Two kinds of error: the ones matplotlib could report and doesn't. The ones no one can report because nothing is wrong with the code.

The first are found by looking. At the data, the artists, the limits, the saved file. The second are found by asking what the chart claims and whether the data supports it. This Is the harder and more valuable habit.
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
