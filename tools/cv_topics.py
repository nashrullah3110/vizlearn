# -*- coding: utf-8 -*-
"""Content for the generated classical image-processing modules.

Twelve of the twenty Computer Vision modules were CNN internals. That is the
middle of the subject with nothing underneath it: a reader could follow what a
feature map is without ever having convolved anything by hand, and the words
"kernel", "threshold" and "dilate" were being used as though they had already
been introduced.

These eight are that missing floor. They are generated rather than
hand-written because they are the same page eight times over - an image, one
or two controls, the result beside it - and the arithmetic they demonstrate
lives together in assets/vizlearn-cv.js where it can be read against itself.

Every source image is drawn in code. Nothing is fetched, so the pages work
offline and no image licence has to be tracked; more usefully, a synthetic
image can be built to contain exactly the feature the module is about - a hard
edge for Sobel, flat regions for thresholding, salt-and-pepper for the median
filter.
"""

TOPICS = []


def topic(slug, title, cat, lead, svg, viz, notes, article, check):
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "viz": viz, "notes": notes, "article": article, "check": check,
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


def _line(x1, y1, x2, y2, stroke=A, sw=1.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, stroke, sw, d))


def _grid(x0, y0, cell, cols, rows, stroke=B, fill="none"):
    out = []
    for r in range(rows):
        for c in range(cols):
            out.append(_box(x0 + c * cell, y0 + r * cell, cell, cell,
                            fill=fill, stroke=stroke, sw=1, rx=0))
    return "".join(out)


# ---------------------------------------------------------------------------
# 1. Convolution kernels by hand
# ---------------------------------------------------------------------------
topic(
    "convolution_kernels",
    "Convolution Kernels by Hand",
    "Filtering",
    "Nine numbers decide whether an image blurs, sharpens or turns into an "
    "outline. Edit them and watch which.",
    _svg(_grid(14, 22, 15, 3, 3, fill=S)
         + _txt(80, 50, "*", A, 16)
         + _box(96, 22, 45, 45, fill=S)
         + _txt(118, 80, "output", M, 8)),
    {
        "op": "kernel",
        "source": "shapes",
        "controls": [
            {"key": "preset", "label": "Kernel", "type": "select", "value": "sobelx",
             "options": [
                 {"value": "identity", "label": "Identity"},
                 {"value": "blur", "label": "Box blur"},
                 {"value": "gaussian", "label": "Gaussian blur"},
                 {"value": "sharpen", "label": "Sharpen"},
                 {"value": "emboss", "label": "Emboss"},
                 {"value": "sobelx", "label": "Sobel X (vertical edges)"},
                 {"value": "sobely", "label": "Sobel Y (horizontal edges)"},
                 {"value": "laplacian", "label": "Laplacian"},
                 {"value": "outline", "label": "Outline"}]},
        ],
        "fixed": {"normalise": True},
    },
    [
        "A kernel is a small grid of weights. The output pixel is the weighted "
        "sum of the input pixel and its neighbours.",
        "If the weights sum to 1 the brightness is preserved. If they sum to 0 "
        "the result is a difference image, centred on grey.",
        "<code class='mono-font'>Sobel X</code> and <code class='mono-font'>Sobel Y</code> "
        "are the same kernel rotated. Each finds edges running across it, not along it.",
        "Every convolutional layer in a CNN does exactly this. The only "
        "difference is that it learns the nine numbers instead of being given them.",
    ],
    """
title: Convolution Kernels by Hand
intro: Nine numbers, one sliding window, and most of classical image processing.

## One operation, many effects

Convolution is a single, simple operation that produces a startling range of
results depending on nine numbers. Take a small grid of weights &mdash; the
**kernel** &mdash; centre it on a pixel, multiply each weight by the pixel
underneath it, and add the products together. That sum is the output pixel.
Slide the kernel one step and do it again.

That is the whole algorithm. Blurring, sharpening, edge detection and
embossing are not different algorithms; they are the same algorithm with
different numbers in the grid.

## Reading a kernel

The identity kernel is the easiest to reason about:

```
0  0  0
0  1  0
0  0  0
```

Every neighbour is multiplied by zero, the centre pixel by one, so the output
is the input unchanged. Now change the centre to 5 and set the four
orthogonal neighbours to &minus;1:

```
 0 -1  0
-1  5 -1
 0 -1  0
```

The centre pixel is amplified and its neighbours are subtracted from it. Where
the neighbourhood is flat, the subtraction cancels the amplification exactly
and nothing happens. Where the centre differs from its surroundings &mdash; at
an edge &mdash; the difference is exaggerated. That is **sharpening**, and it
explains why sharpening amplifies noise: a noisy pixel is, by definition, a
pixel that differs from its neighbours.

## The sum tells you what kind of filter it is

There are two families, and you can tell them apart by adding the weights up.

**Weights summing to 1** preserve average brightness. A box blur of nine ones
divided by nine is the arithmetic mean of the neighbourhood; a Gaussian blur
weights the centre more heavily than the corners. Both keep the image at the
same overall exposure because the total contribution of every pixel is
unchanged.

**Weights summing to 0** produce a difference image. Flat regions become zero,
because a constant multiplied by weights that cancel gives nothing. Only where
the image changes does anything survive. Since a result can be negative, these
filters are usually displayed with 128 added, which is why edge images have
that flat grey background.

| Kernel | Sum | What survives |
|---|---|---|
| Identity | 1 | everything, unchanged |
| Box blur | 1 (after division) | low-frequency detail |
| Sharpen | 1 | everything, with edges exaggerated |
| Sobel | 0 | edges in one direction |
| Laplacian | 0 | edges in every direction |
| Emboss | 1 | a directional shadow |

## Sobel: why there are two of them

The Sobel operator comes as a pair, and the pair is one kernel rotated by
ninety degrees:

```
Sobel X          Sobel Y
-1  0  1        -1 -2 -1
-2  0  2         0  0  0
-1  0  1         1  2  1
```

Sobel X subtracts the column on the left from the column on the right. A
vertical edge &mdash; where left and right differ &mdash; produces a large
value. A horizontal edge produces nothing at all, because left and right are
identical there. Sobel Y is the same argument with rows.

Run each on the visualisation above and the asymmetry is obvious: the vertical
sides of the rectangle appear under Sobel X and vanish under Sobel Y. In
practice the two are combined, usually as the square root of the sum of their
squares, to get an edge strength that does not care about direction.

The middle row being &minus;2, 0, 2 rather than &minus;1, 0, 1 is a small
piece of smoothing built in: the pixel in line with the centre is weighted
more than the diagonals, so a single noisy pixel has less influence than it
would in a pure difference.

## What happens at the border

A kernel centred on a corner pixel has five of its nine cells hanging over the
edge of the image. Something has to be decided, and the three common answers
are to leave the border out (producing a smaller output), to treat the missing
pixels as zero, or to repeat the nearest real pixel outwards. The
visualisation here repeats the edge pixel, which is why the frame stays clean;
zero-padding would darken it. The [padding module](padding_in_cnn.html) works
through what that choice costs inside a network.

## Why this matters for CNNs

Everything above is fixed: someone chose the nine numbers and wrote them down.
A convolutional layer in a neural network performs the identical operation and
differs in exactly one respect &mdash; the nine numbers are parameters, and
gradient descent chooses them.

That is worth sitting with. When people say a CNN "learns to detect edges in
the first layer", they mean that training drives some of the learned kernels
towards something that looks very much like Sobel, because edges turn out to
be a useful thing to measure. Nobody put Sobel there. The architecture only
supplies the sliding window; the content of the window is discovered.

## Where it goes wrong

**Sharpening noise.** Any kernel with negative weights amplifies pixel-to-pixel
variation, and noise is pixel-to-pixel variation. Denoise first, sharpen
second.

**Forgetting to normalise.** A blur kernel of nine ones, applied without
dividing by nine, produces an image nine times too bright &mdash; which, after
clipping at 255, is a white rectangle.

**Assuming bigger is better.** A 3&#215;3 kernel sees a 3&#215;3 region. To
see further you either use a larger kernel, which costs quadratically more
multiplications, or stack several small ones, which is what modern
architectures do and why [receptive field](feature_map_in_cnn.html) is a
concept worth having.

## Slide a 3x3 grid over an image and watch what each one finds

A convolution is a weighted sum repeated at every position. Six classic kernels are applied to the same small image here, with the arithmetic for one output pixel written out in full.

```python-run
import numpy as np

# a small image: a bright square on a dark background, with a diagonal edge
img = np.zeros((9, 9))
img[2:7, 2:7] = 200.0
img[0:3, 6:9] = 120.0
img += np.random.default_rng(0).normal(0, 4, img.shape)
img = np.clip(img, 0, 255)

SHADE = " .:-=+*#%@"
def show(a, label, lo=None, hi=None):
    lo = a.min() if lo is None else lo
    hi = a.max() if hi is None else hi
    rng_ = max(hi - lo, 1e-9)
    print("   %s" % label)
    for row in a:
        print("      " + "".join(SHADE[int(np.clip((v - lo) / rng_, 0, 1) * 9)]
                                 for v in row))

show(img, "the image (%dx%d, values 0-255):" % img.shape)
print()

def convolve(a, k):
    kh, kw = k.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(a, ((ph, ph), (pw, pw)), mode="edge")
    out = np.zeros_like(a, dtype=float)
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            out[i, j] = (padded[i:i + kh, j:j + kw] * k).sum()
    return out

print("ONE OUTPUT PIXEL, written out. take the 3x3 patch at (4,4) and a")
print("simple averaging kernel:")
patch = img[3:6, 3:6]
box = np.ones((3, 3)) / 9
print("   patch:")
for r in patch:
    print("      %s" % np.round(r, 1))
print("   kernel:")
for r in box:
    print("      %s" % np.round(r, 4))
print("   multiply elementwise and sum:")
terms = (patch * box).ravel()
print("      %s" % "  ".join("%.1f" % t for t in terms[:5]))
print("      + ... = %.4f" % terms.sum())
print("   that one number is the output at (4,4). repeat for every pixel.")
print()

kernels = {
    "identity":        np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], float),
    "box blur":        np.ones((3, 3)) / 9,
    "sharpen":         np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], float),
    "sobel x (vert.)": np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float),
    "sobel y (horiz.)": np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], float),
    "laplacian":       np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], float),
}

print("SIX KERNELS on the same image:")
for name, k in kernels.items():
    out = convolve(img, k)
    print()
    print("   %-18s kernel sum %+.1f   output range %+8.1f to %+8.1f"
          % (name, k.sum(), out.min(), out.max()))
    show(np.abs(out) if k.sum() == 0 else out, "")
print()

print("READ THE KERNEL SUMS. that one number tells you what a kernel does:")
for name, k in kernels.items():
    s = k.sum()
    kind = ("preserves brightness" if abs(s - 1) < 1e-9
            else "detects change (flat areas -> 0)" if abs(s) < 1e-9
            else "scales brightness by %.1f" % s)
    print("   %-18s sum %+5.1f  %s" % (name, s, kind))
print()
flat = np.full((9, 9), 100.0)
print("   proof: run each kernel on a completely flat image of 100s:")
for name, k in kernels.items():
    print("      %-18s -> centre pixel %+8.2f" % (name, convolve(flat, k)[4, 4]))
print("   the edge detectors return 0 because there is no edge. that is not")
print("   a coincidence -- a kernel summing to zero cannot respond to a")
print("   constant, only to a difference.")
print()

print("THE TWO SOBELS TOGETHER give gradient magnitude, which is edge")
print("strength regardless of direction:")
gx = convolve(img, kernels["sobel x (vert.)"])
gy = convolve(img, kernels["sobel y (horiz.)"])
mag = np.sqrt(gx ** 2 + gy ** 2)
show(mag, "gradient magnitude:")
print("   the bright ring is the boundary of the square. the interior is")
print("   dark because the interior is flat.")
print()
print("and the angle tells you which way the edge runs:")
ang = np.degrees(np.arctan2(gy, gx))
strong = mag > mag.max() * 0.5
print("   strongest edge pixels and their orientations:")
for (i, j) in list(zip(*np.where(strong)))[:6]:
    print("      (%d,%d) magnitude %7.1f, angle %+7.1f degrees"
          % (i, j, mag[i, j], ang[i, j]))
print()
print("a CNN does not use these. it LEARNS its kernels -- but the early")
print("layers of a trained network reliably rediscover edge and blob")
print("detectors that look very much like the ones above, because those are")
print("what the data rewards.")
```

""",
    [
        {"q": "A kernel's nine weights sum to zero. What does its output look like on a flat, uniform region?",
         "options": ["White", "Black or mid-grey", "Unchanged", "Inverted"],
         "answer": 1,
         "why": "On a flat region every neighbour has the same value, so the weighted sum is that value times zero, which is zero. Displays usually add 128, giving the familiar flat grey."},
        {"q": "Why does Sobel X find vertical edges rather than horizontal ones?",
         "options": ["It scans the image column by column",
                     "It subtracts the left column from the right, and only a vertical edge makes those differ",
                     "It is applied after a rotation",
                     "It uses larger weights"],
         "answer": 1,
         "why": "Across a horizontal edge the left and right columns are identical, so the difference is zero. Only a change in the horizontal direction survives."},
        {"q": "What is the only real difference between this and a CNN's convolutional layer?",
         "options": ["The CNN uses a different arithmetic operation",
                     "The CNN's kernel weights are learned rather than chosen",
                     "The CNN works in colour",
                     "The CNN does not slide the kernel"],
         "answer": 1,
         "why": "The operation is identical. In a CNN the nine numbers are parameters that gradient descent adjusts, which is why early layers often end up resembling edge detectors nobody designed."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Thresholding
# ---------------------------------------------------------------------------
topic(
    "thresholding",
    "Thresholding",
    "Segmentation",
    "One number turns a photograph into a silhouette. Choosing it well is the "
    "whole difficulty.",
    _svg(_box(14, 24, 55, 42, fill=S)
         + _txt(41, 78, "grey", M, 8)
         + _txt(80, 48, "&gt;t", A, 11)
         + _box(92, 24, 55, 42, fill="none", stroke=A)
         + _txt(119, 78, "binary", M, 8)),
    {
        "op": "threshold",
        "source": "shapes",
        "controls": [
            {"key": "threshold", "label": "Threshold", "type": "range",
             "min": 0, "max": 255, "step": 1, "value": 128},
            {"key": "method", "label": "Method", "type": "select", "value": "fixed",
             "options": [{"value": "fixed", "label": "Fixed (use the slider)"},
                         {"value": "otsu", "label": "Otsu (chosen automatically)"}]},
        ],
    },
    [
        "Thresholding maps every pixel to one of two values by comparing it "
        "against a single number.",
        "It throws away almost all the information in the image. That is the "
        "point: what remains is shape.",
        "Otsu's method picks the threshold that best separates the pixels into "
        "two groups, by maximising the variance between them.",
        "A single global threshold fails the moment lighting is uneven. Adaptive "
        "thresholding computes a different value per region.",
    ],
    """
title: Thresholding
intro: The simplest segmentation there is, and the one that fails in the most instructive ways.

## Turning grey into black and white

A greyscale pixel holds one of 256 values. Thresholding replaces it with one
of two: if the value is at least *t*, output white; otherwise output black.

```
output(x, y) = 255 if input(x, y) >= t else 0
```

There is nothing more to the operation. Its interest lies entirely in the
choice of *t*, and in what the result is then used for. After thresholding,
an image is no longer a picture &mdash; it is a **mask**, a statement about
which pixels belong to something and which do not. Counting objects, measuring
areas, finding contours and reading printed text all begin here.

## Watch what the slider destroys

Drag the threshold from 0 to 255 in the visualisation above and three things
happen in order.

At very low values everything is foreground: the whole frame is white, because
every pixel is at least as bright as almost nothing. As the threshold rises,
the darkest regions drop out first &mdash; the dark rectangle goes early. Near
the middle, the bright disc and the light triangle are still foreground while
the background has gone, and the mask actually corresponds to the objects. Push
higher still and the objects themselves start to disappear, brightest last.

The readout shows the percentage of pixels currently classified as foreground.
That number moving smoothly while the *picture* changes abruptly is the thing
worth noticing: there is no single moment where the mask becomes "correct".
Correctness is defined by what you wanted, not by the image.

## Otsu's method

Choosing the threshold by hand does not scale to a thousand images, so the
standard automatic choice is **Otsu's method**. Switch the control above from
Fixed to Otsu and the slider becomes irrelevant.

Otsu treats the problem statistically. Every candidate threshold splits the
pixels into two groups, background and foreground. For each split you can
compute how far apart the two group means are, weighted by how many pixels
each group contains &mdash; the *between-class variance*. Otsu tries all 256
candidates and keeps the one that maximises it.

The intuition is that a good threshold produces two groups that are each
internally consistent and clearly different from one another. A bad threshold
slices through the middle of a group, and the two halves end up with similar
means.

Otsu works well when the histogram is genuinely **bimodal** &mdash; two humps
with a valley between them, one hump for the object and one for the
background. It works badly when it is not: on an image that is 95% background
with a small object, or one where illumination smears the two humps together,
Otsu confidently returns a number that separates nothing.

## Where a global threshold breaks

The assumption underneath everything above is that one number works for the
whole image. It usually does not.

Photograph a page of text with a lamp on one side. The paper on the lit side
is brighter than the *ink* on the dark side. No single threshold can call the
lit paper background and the dark paper background while also calling the dark
ink foreground &mdash; the values overlap, and overlapping values cannot be
separated by a single cut.

The fix is **adaptive thresholding**: compute a local threshold for each pixel
from the mean or the Gaussian-weighted mean of its neighbourhood, then compare
the pixel to that. The lit side gets a high local threshold and the dark side a
low one, and both are read correctly. The cost is a parameter &mdash; the
neighbourhood size &mdash; which has to be larger than the strokes you want to
keep and smaller than the illumination changes you want to remove.

## What comes next

A thresholded mask is rarely clean. It has holes where a highlight fell inside
an object, and speckles where noise crossed the threshold in the background.
The standard follow-up is a morphological open to remove the speckles and a
close to fill the holes, which is exactly what [erosion and
dilation](erosion_and_dilation.html) are for.

## Where it goes wrong

**Thresholding a colour image by brightness.** A saturated red and a mid-grey
can have identical luminance. If colour is what distinguishes your object,
threshold a colour channel &mdash; usually [hue](colour_spaces_rgb_hsv.html)
&mdash; not the greyscale.

**Trusting Otsu on a unimodal histogram.** Check the histogram first. If there
is one hump, there is no valley, and Otsu is returning the midpoint of a
single distribution.

**Thresholding before denoising.** A salt-and-pepper pixel is by definition at
an extreme value, so it survives any threshold. A median filter first costs
almost nothing and removes them entirely.

## Turning grey into black and white, and choosing where

A threshold splits pixels into two classes. Otsu's method picks the split automatically, adaptive thresholding picks a different one per region, and the case where a global threshold fails is easy to construct.

```python-run
import numpy as np

rng = np.random.default_rng(0)

SHADE = " .:-=+*#%@"
def show(a, label):
    print("   %s" % label)
    lo, hi = a.min(), a.max()
    for row in a:
        print("      " + "".join(SHADE[int(np.clip((v - lo) / max(hi - lo, 1e-9), 0, 1) * 9)]
                                 for v in row))

# a document-like image: dark text on a light page, with uneven lighting
H, W = 12, 24
page = np.full((H, W), 200.0)
text = [(2, 3), (2, 4), (2, 5), (3, 3), (4, 3), (4, 4), (4, 5),
        (6, 12), (6, 13), (7, 12), (8, 12), (8, 13),
        (2, 18), (3, 18), (4, 18), (4, 19), (4, 20),
        (8, 4), (8, 5), (9, 4), (9, 5)]
for r, c in text:
    page[r, c] = 40.0
# a lighting gradient: bright on the left, dim on the right
page = page * np.linspace(1.0, 0.13, W)[None, :]
page = np.clip(page + rng.normal(0, 3, page.shape), 0, 255)

show(page, "input: dark marks on a page, lit unevenly from the left")
print("   note the right-hand side is genuinely darker -- the page there is")
print("   dimmer than the INK on the left.")
print("      brightest page pixel on the right : %.0f" % page[:, -6:].max())
print("      darkest ink pixel on the left     : %.0f"
      % min(page[r, c] for r, c in text if c < 8))
print("   no single number can separate ink from page across the whole")
print("   image, and that is the whole problem.")
print()

hist, edges = np.histogram(page, bins=16, range=(0, 256))
print("THE HISTOGRAM, which is what a threshold is chosen from:")
for i, count in enumerate(hist):
    if count:
        print("      %3.0f-%3.0f %5d %s"
              % (edges[i], edges[i + 1], count, "#" * int(40 * count / hist.max())))
print()

def otsu(a, bins=64):
    hist_, edges_ = np.histogram(a, bins=bins, range=(0, 256))
    total = hist_.sum()
    centres = (edges_[:-1] + edges_[1:]) / 2
    best_t, best_var = 0.0, -1.0
    for i in range(1, bins):
        w0 = hist_[:i].sum() / total
        w1 = 1 - w0
        if w0 == 0 or w1 == 0:
            continue
        m0 = (hist_[:i] * centres[:i]).sum() / hist_[:i].sum()
        m1 = (hist_[i:] * centres[i:]).sum() / hist_[i:].sum()
        var = w0 * w1 * (m0 - m1) ** 2
        if var > best_var:
            best_var, best_t = var, centres[i]
    return best_t

t_otsu = otsu(page)
print("OTSU'S METHOD searches every threshold and keeps the one that")
print("maximises the variance BETWEEN the two groups -- equivalently, the")
print("one that minimises the variance within them:")
print("   chosen threshold: %.1f" % t_otsu)
print()

def apply_global(a, t):
    return (a < t).astype(float)

def adaptive(a, block=7, offset=8.0):
    p = np.pad(a, block // 2, mode="edge")
    out = np.zeros_like(a)
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            local = p[i:i + block, j:j + block].mean()
            out[i, j] = 1.0 if a[i, j] < local - offset else 0.0
    return out

truth = np.zeros((H, W))
for r, c in text:
    truth[r, c] = 1.0

results = [("global, threshold 100", apply_global(page, 100.0)),
           ("global, Otsu %.0f" % t_otsu, apply_global(page, t_otsu)),
           ("adaptive, 7x7 local mean", adaptive(page))]
for name, out in results:
    show(out, name)
    tp = int((out * truth).sum())
    fp = int((out * (1 - truth)).sum())
    fn = int(((1 - out) * truth).sum())
    print("      found %d of %d marks, with %d false positives"
          % (tp, int(truth.sum()), fp))
    print()

print("READ THE GLOBAL RESULTS. whatever single number you pick:")
print("%16s %10s %10s %10s" % ("threshold", "found", "missed", "false pos"))
for t in (15, 22, 30, 60, 100, t_otsu):
    out = apply_global(page, t)
    print("%16.0f %10d %10d %10d"
          % (t, int((out * truth).sum()), int(((1 - out) * truth).sum()),
             int((out * (1 - truth)).sum())))
print("   read it as a trade with no good corner. a low threshold keeps the")
print("   page clean and MISSES ink; raising it recovers the ink and starts")
print("   calling the dim page ink too. the two classes overlap once the")
print("   lighting is folded in:")
ink_vals = [page[r, c] for r, c in text]
pg = np.array([page[i, j] for i in range(H) for j in range(W)
               if truth[i, j] == 0])
print("      ink ranges  %.0f to %.0f" % (min(ink_vals), max(ink_vals)))
print("      page ranges %.0f to %.0f" % (pg.min(), pg.max()))
print("      those ranges overlap, and no threshold can undo that.")
print()

out_a = adaptive(page)
print("ADAPTIVE THRESHOLDING compares each pixel to its own neighbourhood")
print("rather than to a global constant:")
print("   found %d of %d, %d false positives"
      % (int((out_a * truth).sum()), int(truth.sum()), int((out_a * (1 - truth)).sum())))
print("   it works because 'darker than the page around me' is true for ink")
print("   everywhere, while 'darker than 100' is only true on the left.")
print()
print("   the two parameters matter:")
for block in (3, 7, 15):
    o = adaptive(page, block)
    print("      block %2d: found %2d, false positives %2d"
          % (block, int((o * truth).sum()), int((o * (1 - truth)).sum())))
print("   the marks here are one or two pixels wide, so even a 3x3 block")
print("   still sees page around them. with thicker strokes a small block")
print("   sits entirely INSIDE the mark, the local mean becomes the ink")
print("   itself, and the middle of the stroke is classified as background")
print("   -- hollow letters. going the other way, a block large enough to")
print("   span the whole lighting gradient degenerates back into a global")
print("   threshold, which is what the rising false positives above show.")
print()
print("the general lesson is not about thresholds. it is that a global")
print("statistic fails whenever the thing you are measuring varies across")
print("the image -- which is also why normalisation layers exist, and why")
print("illumination correction is a standard first step in classical vision.")
```

""",
    [
        {"q": "What does Otsu's method maximise when choosing a threshold?",
         "options": ["The number of foreground pixels",
                     "The variance between the two groups the threshold creates",
                     "The image's overall contrast",
                     "The number of edges detected"],
         "answer": 1,
         "why": "It tries every candidate threshold and keeps the one whose two resulting groups have the most separated means, weighted by group size."},
        {"q": "Why does a single global threshold fail on a page photographed under uneven lighting?",
         "options": ["The camera resolution is too low",
                     "Lit paper can be brighter than ink on the shadowed side, so the values overlap",
                     "Otsu is not being used",
                     "Paper is not perfectly white"],
         "answer": 1,
         "why": "Once background values on one side exceed foreground values on the other, no single cut separates them. Adaptive thresholding computes a local threshold per neighbourhood instead."},
        {"q": "Why should a median filter usually run before thresholding a noisy image?",
         "options": ["It makes the image brighter",
                     "Salt-and-pepper pixels sit at extreme values and survive any threshold",
                     "It is required by Otsu",
                     "It converts the image to greyscale"],
         "answer": 1,
         "why": "Impulse noise is at 0 or 255 by definition, so it lands on one side of every threshold. Removing it first is cheap and leaves the mask clean."},
    ],
)


# ---------------------------------------------------------------------------
# 3. Histograms and equalisation
# ---------------------------------------------------------------------------
topic(
    "histograms_and_equalisation",
    "Histograms and Equalisation",
    "Enhancement",
    "The histogram tells you what an image is made of. Equalisation rewrites "
    "it to use the whole range.",
    _svg("".join(_box(20 + i * 12, 62 - h, 9, h, fill=(A if i in (2, 3) else S), stroke=B, sw=1)
                 for i, h in enumerate([6, 14, 30, 34, 16, 8, 4, 3, 2, 1]))
         + _txt(80, 78, "0 ....... 255", M, 8)),
    {
        "op": "equalise",
        "source": "lowcontrast",
        "histogram": True,
        "controls": [
            {"key": "on", "label": "Equalise", "type": "toggle", "value": True},
        ],
    },
    [
        "A histogram counts how many pixels hold each brightness value. It says "
        "nothing about where they are.",
        "A narrow histogram means low contrast: the image is using a fraction of "
        "the range available to it.",
        "Equalisation applies the cumulative distribution as a lookup table, "
        "stretching crowded regions apart and squeezing empty ones together.",
        "It is a global operation. CLAHE does the same thing per tile, which "
        "avoids amplifying noise in already-flat areas.",
    ],
    """
title: Histograms and Equalisation
intro: What an image is made of, and how to make it use the range it has.

## Counting, not looking

An image histogram is a count: for each of the 256 possible brightness values,
how many pixels hold it. Nothing else. It discards position entirely &mdash; an
image and the same image shuffled into random order have identical histograms.

That sounds like a weakness and is mostly a strength. Exposure, contrast and
the presence of distinct regions are all properties of the *distribution* of
values, not of where they sit, so the histogram is exactly the right summary
for judging them. Photographers read one on the back of a camera for this
reason.

Watch the two histograms under the visualisation above. The input image is
deliberately low in contrast, so its histogram is a narrow spike: almost every
pixel sits between roughly 100 and 160, and the ranges below and above are
empty. Two hundred of the 256 available values are being wasted.

## What a shape means

**A spike in the middle** is low contrast. The image is grey and flat, and
detail exists but the differences are too small to see.

**A wide, flat spread** is high contrast, using the full range.

**Two separated humps** &mdash; a bimodal histogram &mdash; means the image has
two distinct populations of pixel, usually an object and a background. This is
the shape that makes [thresholding](thresholding.html) work, and the valley
between the humps is where the threshold belongs.

**A pile against the right edge** is clipping: pixels that were brighter than
255 have all been recorded as 255. That detail is gone and no amount of
processing brings it back, which is why photographers expose to avoid it.

## How equalisation works

Histogram equalisation asks a specific question: what mapping from old values
to new ones would make the histogram as flat as possible?

The answer is the **cumulative distribution function**. For each value *v*,
compute the fraction of pixels whose value is at most *v*. That fraction is
between 0 and 1; multiply by 255 and you have the new value for *v*.

```
cdf[v] = (number of pixels <= v) / (total pixels)
new[v] = round(cdf[v] * 255)
```

Why this works is worth a moment. If a value is very common, the CDF climbs
steeply across it, so values on either side get mapped far apart &mdash;
crowded regions are spread out. If a range of values is rare or absent, the CDF
is nearly flat there, so that whole range collapses to almost a single output
value. The transformation gives range to where the pixels actually are, and
takes it away from where they are not.

Toggle the control above and watch both the image and the output histogram. The
narrow spike is pulled apart across the full width, and detail that was present
but invisible &mdash; the difference between the triangle and the background
&mdash; becomes plainly visible.

## What it costs

Equalisation is not free, and the costs follow directly from the mechanism.

**It amplifies noise.** In a region that is genuinely flat, the small random
variations between neighbouring pixels are still variations, and stretching the
range stretches them too. A clear sky becomes a mottled one.

**It is global.** One lookup table is computed from the whole image and applied
everywhere. An image that is correctly exposed on the left and dark on the
right gets a compromise that suits neither.

**The result is not natural.** Faces in particular look wrong after
equalisation, because skin tones occupy a narrow band and equalisation
deliberately spreads narrow bands apart.

## CLAHE

The standard fix for the second and third problems is **CLAHE**, Contrast
Limited Adaptive Histogram Equalisation. It divides the image into tiles,
equalises each tile against its own histogram, and interpolates between tiles
so the boundaries do not show. The dark region gets its own aggressive
stretch; the well-exposed region is left more or less alone.

The "contrast limited" half addresses the noise. Before computing the CDF, any
histogram bin taller than a set limit is clipped and the excess redistributed
across the other bins. This caps how steeply the CDF can climb, which caps how
far apart nearly-identical values can be pushed &mdash; and since noise
amplification *is* pushing nearly-identical values apart, capping it directly
limits the damage.

## Where it goes wrong

**Equalising an already well-exposed image.** There is nothing to gain and
noise to lose. Look at the histogram first; if it already spans the range,
leave it alone.

**Equalising each RGB channel separately.** The three channels get three
different mappings, so the colours shift. Convert to a space with a separate
brightness channel, equalise that one channel, and convert back.

**Comparing histograms across images to judge similarity.** Two completely
different photographs can share a histogram. It describes the palette, not the
picture.
""",
    [
        {"q": "What does a histogram tell you nothing about?",
         "options": ["How many pixels are dark",
                     "Where in the image the pixels are",
                     "Whether the image is clipped",
                     "Whether contrast is low"],
         "answer": 1,
         "why": "A histogram is a count per value. An image and a randomly shuffled copy of it have identical histograms, because position is discarded entirely."},
        {"q": "Which function does histogram equalisation use as its lookup table?",
         "options": ["The cumulative distribution function",
                     "The probability density function",
                     "A Gaussian",
                     "The inverse of the histogram"],
         "answer": 0,
         "why": "The fraction of pixels at or below each value, scaled to 0-255. Common values make the CDF climb steeply and so get spread apart; rare values collapse together."},
        {"q": "Why does CLAHE clip the histogram before computing the CDF?",
         "options": ["To make it run faster",
                     "To cap how steeply the CDF can climb, which limits noise amplification",
                     "To remove outlier pixels",
                     "To force the histogram to be bimodal"],
         "answer": 1,
         "why": "A tall bin means a steep CDF, which pushes nearly-identical neighbouring values far apart. That is exactly what noise amplification is, so limiting bin height limits it."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Blur: Gaussian vs median vs bilateral
# ---------------------------------------------------------------------------
topic(
    "blur_gaussian_median_bilateral",
    "Blur: Gaussian, Median and Bilateral",
    "Filtering",
    "Three ways to remove noise. One smears edges, one ignores outliers, one "
    "refuses to cross a boundary.",
    _svg(_box(12, 26, 40, 40, fill=S)
         + _txt(32, 78, "noisy", M, 8)
         + _box(60, 26, 40, 40, fill=S, stroke=A)
         + _txt(80, 78, "gauss", M, 8)
         + _box(108, 26, 40, 40, fill=S, stroke=A)
         + _txt(128, 78, "median", M, 8)),
    {
        "op": "smooth",
        "source": "saltpepper",
        "controls": [
            {"key": "method", "label": "Filter", "type": "select", "value": "median",
             "options": [{"value": "gaussian", "label": "Gaussian"},
                         {"value": "median", "label": "Median"},
                         {"value": "bilateral", "label": "Bilateral"}]},
            {"key": "radius", "label": "Radius", "type": "range",
             "min": 1, "max": 4, "step": 1, "value": 2},
            {"key": "sigma", "label": "Bilateral edge sigma", "type": "range",
             "min": 5, "max": 90, "step": 5, "value": 30},
        ],
    },
    [
        "Gaussian blur is a weighted average. An outlier is included in the "
        "average, so it is spread out rather than removed.",
        "The median filter sorts the neighbourhood and takes the middle value. "
        "An outlier is never the middle value, so it disappears completely.",
        "Bilateral filtering weights neighbours by both distance and similarity, "
        "so it averages within a region but not across a boundary.",
        "The source image here has salt-and-pepper noise, which is the case that "
        "separates the three most clearly.",
    ],
    """
title: Blur: Gaussian, Median and Bilateral
intro: Three smoothing filters, one noisy image, and a clear demonstration of why the choice matters.

## The same job, three different assumptions

All three filters answer the same question &mdash; what should this pixel be,
given its neighbours? &mdash; and they differ in what they assume about how the
pixel got corrupted. That assumption is the whole story, and it is why one
filter can be excellent on one kind of noise and useless on another.

The image in the visualisation carries **salt-and-pepper noise**: isolated
pixels flipped to pure black or pure white. Switch between the three filters
and the difference is not subtle.

## Gaussian: a weighted average

A Gaussian blur replaces each pixel with a weighted mean of its neighbourhood,
where the weights fall off with distance according to a Gaussian curve. The
centre counts most, the corners least.

It is the right filter when the noise is **additive and roughly symmetric**
&mdash; every pixel nudged up or down by a small random amount. Averaging
several such pixels cancels the nudges, because they are as often positive as
negative. Sensor noise in reasonable light behaves like this, and a Gaussian
handles it well.

On salt-and-pepper it fails, and the reason is structural: a mean includes
every value it is given. A single pixel at 255 sitting among neighbours at 40
drags the average up. The filter does not remove the outlier &mdash; it
*spreads* it over the neighbourhood, converting one bright dot into a larger,
dimmer smudge. Increase the radius and the smudges grow rather than vanishing.

The other cost is edges. An edge is a place where neighbouring pixels are
genuinely different, and averaging across it mixes the two sides together. Any
filter based on a plain average must blur edges, because it has no way to know
that an edge is there.

## Median: sorting instead of averaging

The median filter takes the neighbourhood, sorts the values, and outputs the
middle one.

This one change fixes salt-and-pepper completely. To be selected as the median,
a value has to sit in the middle of the sorted list &mdash; and an extreme
value, by definition, sorts to one end. It is never chosen. It is not reduced
or spread; it is simply not selected, and the output takes a value that some
genuine neighbouring pixel actually had.

Set the filter to Median with radius 2 above. The speckles do not fade; they
are gone, and the shapes underneath keep their edges. That edge preservation
is the second benefit: at a boundary, most of the neighbourhood belongs to one
side or the other, so the median comes from the majority side rather than from
a blend of both.

The median is a **non-linear** filter, which means it cannot be expressed as a
convolution kernel and cannot be decomposed into separate horizontal and
vertical passes. It is correspondingly slower, since a sort is required at
every pixel.

## Bilateral: averaging only within a region

The bilateral filter keeps the weighted average but multiplies each weight by a
second factor based on how similar the neighbour's *value* is to the centre
pixel's.

```
weight = spatial(distance) * range(|neighbour - centre|)
```

A neighbour that is nearby and similar gets a large weight. A neighbour that is
nearby but very different &mdash; because it is on the other side of an edge
&mdash; gets a weight close to zero and is effectively excluded.

The result smooths within a region and refuses to smooth across a boundary. It
is what produces the slightly plastic look of smartphone portrait modes: skin
is smoothed heavily while the outline of the face stays sharp.

The edge sigma control sets how different a neighbour has to be before it is
ignored. Turn it low and the filter barely does anything, because almost
everything counts as an edge. Turn it high and the range term stops
discriminating, and you have an ordinary Gaussian blur back.

## Choosing

| Noise | Use | Because |
|---|---|---|
| Small random variation | Gaussian | averaging cancels symmetric errors |
| Isolated extreme pixels | Median | outliers never sort to the middle |
| Any, with edges to protect | Bilateral | dissimilar neighbours are excluded |
| Impulse noise before thresholding | Median | extremes survive every threshold otherwise |

A practical note: these compose. Median first to remove impulses, then a
gentle Gaussian to handle what remains, is a common and effective pipeline.

## Where it goes wrong

**Blurring before edge detection without thinking.** Some blur helps, since
edge detectors amplify noise. Too much removes the edges you were looking for.
The Canny detector builds a Gaussian in for exactly this reason, with a
parameter to control it.

**Using a large median radius on fine detail.** Thin lines narrower than half
the window are a minority in every neighbourhood they appear in, so the median
removes them along with the noise.

**Reaching for bilateral by default.** It is far more expensive than the other
two and has two parameters instead of one. If the edges do not need protecting,
it is a slow Gaussian.
""",
    [
        {"q": "Why does a Gaussian blur fail to remove salt-and-pepper noise?",
         "options": ["The radius is always too small",
                     "A mean includes the outlier, so it is spread rather than removed",
                     "It only works on colour images",
                     "Gaussian weights are negative"],
         "answer": 1,
         "why": "Averaging incorporates every value it is given. A pixel at 255 among neighbours at 40 pulls the mean up, turning one bright dot into a larger dim smudge."},
        {"q": "Why does the median filter remove an outlier completely?",
         "options": ["It clamps values to a range",
                     "An extreme value sorts to one end and is never the middle element",
                     "It replaces outliers with zero",
                     "It detects outliers explicitly"],
         "answer": 1,
         "why": "The output is whichever value sits in the middle of the sorted neighbourhood. An extreme value is at an end by definition, so it is simply never selected."},
        {"q": "What happens to a bilateral filter as its range sigma grows very large?",
         "options": ["It becomes an ordinary Gaussian blur",
                     "It stops doing anything",
                     "It becomes a median filter",
                     "It sharpens the image"],
         "answer": 0,
         "why": "A large range sigma means the similarity term stops discriminating between neighbours, so only the spatial term is left - which is exactly a Gaussian blur."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Erosion and dilation
# ---------------------------------------------------------------------------
topic(
    "erosion_and_dilation",
    "Erosion and Dilation",
    "Morphology",
    "Shrink a shape, grow a shape, and combine the two to remove speckles or "
    "fill holes without moving the boundary.",
    _svg(_box(16, 28, 36, 36, fill=S)
         + _txt(34, 78, "input", M, 8)
         + _box(64, 32, 28, 28, fill=S, stroke=A)
         + _txt(78, 78, "erode", M, 8)
         + _box(102, 24, 44, 44, fill=S, stroke=A)
         + _txt(124, 78, "dilate", M, 8)),
    {
        "op": "morphology",
        "source": "saltpepper",
        "controls": [
            {"key": "method", "label": "Operation", "type": "select", "value": "open",
             "options": [{"value": "none", "label": "None (binary only)"},
                         {"value": "erode", "label": "Erode"},
                         {"value": "dilate", "label": "Dilate"},
                         {"value": "open", "label": "Open (erode then dilate)"},
                         {"value": "close", "label": "Close (dilate then erode)"}]},
            {"key": "radius", "label": "Structuring element", "type": "range",
             "min": 1, "max": 3, "step": 1, "value": 1},
            {"key": "threshold", "label": "Binarise at", "type": "range",
             "min": 0, "max": 255, "step": 1, "value": 128},
        ],
    },
    [
        "Morphology operates on shape. It is defined for binary images, which is "
        "why the threshold control comes first.",
        "Erosion keeps a pixel only if every pixel under the structuring element "
        "is foreground. Shapes shrink and thin features vanish.",
        "Dilation keeps a pixel if any pixel under the element is foreground. "
        "Shapes grow and small gaps close.",
        "Open removes small bright specks; close fills small dark holes. Both "
        "leave the overall size roughly unchanged.",
    ],
    """
title: Erosion and Dilation
intro: The two operations that shape a binary mask, and the four things you build from them.

## Operating on shape, not brightness

Every filter so far has treated the image as a field of numbers. Morphological
operations treat it as a **set of pixels** &mdash; the foreground &mdash; and
ask geometric questions about that set. They are defined for binary images,
which is why the visualisation above thresholds first and why the binarise
control sits alongside the others.

The tool is a **structuring element**: a small shape, usually a square or a
disc, that gets placed over every pixel in turn. What happens next depends on
which of two rules you apply.

## Erosion: every, or nothing

Erosion keeps a foreground pixel only if **every** pixel under the structuring
element is also foreground. One background pixel anywhere under the element and
the centre is turned off.

The consequences follow directly. Boundaries retreat inwards by roughly the
radius of the element, because a pixel near an edge always has some background
under a large enough window. Small isolated specks vanish entirely, since a
speck smaller than the element can never have the element fit inside it. Thin
connections between larger blobs are cut, because a bridge one pixel wide fails
the test everywhere along its length.

Select Erode above and raise the structuring element size. The bright speckles
disappear on the first step; the shapes visibly thin; push it far enough and the
thin bright bar at the bottom of the frame is gone entirely.

## Dilation: any, and it counts

Dilation is erosion's mirror. A pixel becomes foreground if **any** pixel under
the structuring element is foreground.

Boundaries advance outwards. Small holes inside an object fill, because a hole
smaller than the element has foreground on all sides within reach. Nearby blobs
merge as their expanding boundaries meet. The dark speckles that erosion could
not touch disappear here instead.

Erosion and dilation are *duals*: eroding the foreground is exactly dilating the
background. That is not a coincidence to be memorised, it is the same rule seen
from the other side.

## Open and close: the useful pair

Neither operation is much use alone, because both change the size of everything.
Composing them fixes that.

**Opening** is erosion followed by dilation. The erosion removes small bright
specks and thins everything; the dilation grows what survived back to roughly
its original size. Specks that were destroyed do not come back &mdash; there is
nothing left to grow. The net effect is *remove small bright things, leave
everything else about where it was*.

**Closing** is dilation followed by erosion. The dilation fills small dark holes
and joins nearby pieces; the erosion shrinks the result back down. Holes that
were filled stay filled. The net effect is *remove small dark things, leave
everything else about where it was*.

| Operation | Sequence | Removes | Boundary |
|---|---|---|---|
| Erode | &mdash; | bright specks | retreats |
| Dilate | &mdash; | dark holes | advances |
| Open | erode, dilate | bright specks | roughly unchanged |
| Close | dilate, erode | dark holes | roughly unchanged |

Set the control above to Open and compare against Erode at the same size. The
speckles are gone in both, but the shapes under Open are still the size they
started.

## Why this always follows thresholding

A thresholded mask is almost never clean. Noise that happened to cross the
threshold leaves scattered foreground pixels in the background; a highlight
inside an object leaves a hole. Both are small, and both are exactly what open
and close are for.

The standard sequence &mdash; threshold, open to despeckle, close to fill
&mdash; is so common it is worth treating as one step. Only after it does
counting connected components or tracing contours give sensible answers.

## Choosing the element

The size is the parameter that matters, and there is a principle for it: the
structuring element should be **larger than the artefacts you want to remove and
smaller than the features you want to keep**. If a speck is 3 pixels across and
a genuine object is 30, anything between will do. If they are 3 and 5, no size
works and morphology is the wrong tool.

The shape matters less, but not never. A square element treats diagonals
differently from axes; a disc is isotropic; a horizontal line erodes vertical
strokes while leaving horizontal ones alone, which is how table rules are
separated from text in document processing.

## Where it goes wrong

**Applying it to a greyscale image without thinking.** Greyscale morphology is
defined &mdash; erosion becomes a local minimum and dilation a local maximum
&mdash; but it means something different, and results that look plausible may
not be what was intended.

**Using an element that is too large.** It removes the noise and the detail
together. Thin structures are lost first and cannot be recovered.

**Opening when you meant closing.** The mnemonic is that opening removes
*bright* things and closing removes *dark* ones. If your foreground is dark
against a light background, they swap.
""",
    [
        {"q": "Under erosion, when does a foreground pixel survive?",
         "options": ["When any pixel under the structuring element is foreground",
                     "When every pixel under the structuring element is foreground",
                     "When the majority are foreground",
                     "When the centre pixel is foreground"],
         "answer": 1,
         "why": "Erosion is the 'every' rule. One background pixel anywhere under the element turns the centre off, which is why boundaries retreat and thin features are cut."},
        {"q": "Why does opening remove small specks without shrinking the larger shapes?",
         "options": ["It uses a smaller structuring element for the shapes",
                     "The erosion destroys the specks, and the following dilation regrows only what survived",
                     "It detects speck size first",
                     "It operates on the background instead"],
         "answer": 1,
         "why": "Dilation can only grow what is still there. Specks removed by the erosion have nothing left to grow, while larger shapes are restored to roughly their original size."},
        {"q": "How should the structuring element be sized?",
         "options": ["As large as possible",
                     "Larger than the artefacts to remove, smaller than the features to keep",
                     "Always 3x3",
                     "Equal to the image width divided by ten"],
         "answer": 1,
         "why": "That gap is what the operation exploits. If the artefacts and the features are close in size, no element separates them and morphology is the wrong tool."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Colour spaces: RGB vs HSV
# ---------------------------------------------------------------------------
topic(
    "colour_spaces_rgb_hsv",
    "Colour Spaces: RGB and HSV",
    "Colour",
    "Why selecting a colour is hard in RGB and easy in HSV, and what each "
    "channel actually holds.",
    _svg(_box(16, 26, 30, 40, fill=S) + _txt(31, 78, "R G B", M, 8)
         + _txt(66, 50, "&#8594;", A, 13)
         + _box(84, 26, 30, 40, fill=S, stroke=A) + _txt(99, 78, "H S V", M, 8)
         + _box(122, 26, 24, 40, fill="none", stroke=B) + _txt(134, 78, "mask", M, 8)),
    {
        "op": "channel",
        "source": "colour",
        "controls": [
            {"key": "channel", "label": "Channel", "type": "select", "value": "h",
             "options": [{"value": "r", "label": "R - red"},
                         {"value": "g", "label": "G - green"},
                         {"value": "b", "label": "B - blue"},
                         {"value": "h", "label": "H - hue"},
                         {"value": "s", "label": "S - saturation"},
                         {"value": "v", "label": "V - value (brightness)"}]},
        ],
    },
    [
        "RGB stores how much of each primary light to emit. It matches hardware, "
        "not perception.",
        "In RGB, making a colour darker changes all three numbers, so brightness "
        "and colour are entangled.",
        "HSV separates them: hue is which colour, saturation how pure, value how "
        "bright.",
        "Selecting 'anything red' is one range in hue and three coupled ranges in "
        "RGB. That is the whole reason HSV exists.",
    ],
    """
title: Colour Spaces: RGB and HSV
intro: The same pixel, described two ways, and why one of them makes colour selection trivial.

## RGB describes the hardware

A screen produces colour by mixing three lights. RGB records how much of each:
three numbers from 0 to 255, one per primary. It is the natural format for a
display, a camera sensor and a file, and it is what almost every image arrives
in.

It is a poor format for *reasoning* about colour, and the reason is that the
three numbers are not independent in any way a person cares about.

Take a mid red, `(200, 60, 60)`. Make it darker and you get `(120, 36, 36)`
&mdash; all three numbers changed. Make it paler and you get `(220, 140, 140)`
&mdash; all three again. The colour did not change in either case; the
brightness did, and then the purity did, and both operations moved every
channel. There is no single number in RGB that means "how red" or "how bright".

Look at the R, G and B channels in the visualisation above. The red disc is
bright in R, but so is the yellow one, because yellow is red plus green. None
of the three channels isolates a colour, because none of them corresponds to
anything you would name.

## HSV separates the three questions

HSV rewrites the same pixel as three numbers that answer three separate
questions.

**Hue** is which colour, as an angle around a wheel from 0 to 360 degrees. Red
is near 0, green near 120, blue near 240. It is circular, so 359 and 1 are
neighbours.

**Saturation** is how pure the colour is, from 0 to 1. At 0 the pixel is grey
regardless of hue; at 1 it is the most vivid version of that hue available.

**Value** is how bright, from 0 to 1. At 0 the pixel is black regardless of
anything else.

The conversion is arithmetic on the RGB triple &mdash; value is the maximum
channel, saturation is the range between maximum and minimum divided by the
maximum, and hue is determined by which channel is largest and by how the other
two compare. No information is added or lost. It is the same pixel in different
coordinates.

## The thing this makes easy

Switch the visualisation to the H channel. Each disc becomes a flat, uniform
region, and each is a *different* flat region. That is the payoff: within one
object, hue barely varies, even where brightness does. A shadow falling across
a red ball changes V dramatically and leaves H almost alone.

So "find the red object" becomes one comparison:

```
mask = (hue < 15) or (hue > 345)
```

Try to write that in RGB. You need red high, green low, blue low &mdash; but
how high, and relative to what? A dark red has a low R. A pale pink has a high
G and B. The ranges are coupled, they depend on lighting, and every new
lighting condition needs them retuned. This is why colour-based tracking,
chroma keying and skin detection are all done in HSV or a close relative, and
why the technique is old enough to predate the tools you would use for it now.

Saturation earns its place too. Hue is meaningless for a near-grey pixel
&mdash; the arithmetic still produces an angle, but it is determined by tiny
differences and jumps around unstably. A useful mask therefore usually requires
saturation above some floor as well, which reads as "a definite colour, not
just a shade".

| Task | Space | Why |
|---|---|---|
| Storing or displaying | RGB | matches sensors and screens |
| Selecting a colour | HSV | one range in hue |
| Adjusting brightness only | HSV | change V, leave H and S |
| Equalising contrast in colour | HSV or LAB | one brightness channel to equalise |
| Measuring perceptual difference | LAB | distances match what eyes report |

## Where HSV stops being enough

HSV is a convenience, not a perceptual model. Its value channel is simply the
maximum of R, G and B, which does not match how bright a colour looks: pure
yellow and pure blue both have value 1 and are nowhere near equally bright to a
human eye.

When the question is genuinely perceptual &mdash; how different do these two
colours *look*, which of these is closer &mdash; the answer is a space like
**LAB**, built from measurements of human vision so that equal distances
correspond to roughly equal perceived differences. Colour-difference metrics
and palette-matching work there.

## Where it goes wrong

**Forgetting that hue wraps.** Red straddles 0. A naive range test
`10 < hue < 350` selects everything except red. Two tests are needed, or a
rotation of the hue axis first.

**Ignoring saturation.** Grey pixels have an arbitrary hue. A hue-only mask
picks up noise from every washed-out region in the frame.

**Assuming a fixed hue range transfers.** Hue is stable against brightness, not
against the colour of the light source. Photograph the same red object under
tungsten and daylight and the hue moves. White balance first, or calibrate per
scene.

**Reading OpenCV's hue as degrees.** OpenCV stores hue in 0-179 so it fits in a
byte, not 0-359. Half of every published threshold is wrong for this reason.

## The same colour, described two ways

RGB says how much of each light; HSV says which colour, how vivid, how bright. Converting between them by hand shows why one is right for displays and the other for finding a coloured object.

```python-run
import numpy as np

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d == 0:
        h = 0.0
    elif mx == r:
        h = (60 * ((g - b) / d)) % 360
    elif mx == g:
        h = 60 * ((b - r) / d) + 120
    else:
        h = 60 * ((r - g) / d) + 240
    s = 0.0 if mx == 0 else d / mx
    return h, s, mx

swatches = [("pure red", (255, 0, 0)), ("dark red", (128, 0, 0)),
            ("pink", (255, 128, 128)), ("pure green", (0, 255, 0)),
            ("sky blue", (100, 180, 255)), ("white", (255, 255, 255)),
            ("grey", (128, 128, 128)), ("black", (0, 0, 0))]

print("%12s %18s %10s %10s %10s"
      % ("colour", "RGB", "hue (deg)", "sat", "value"))
for name, (r, g, b) in swatches:
    h, s, v = rgb_to_hsv(r, g, b)
    print("%12s %18s %9.0f %10.3f %10.3f" % (name, str((r, g, b)), h, s, v))
print()
print("read the three reds. pure red, dark red and pink have completely")
print("different RGB triples, and the SAME hue of 0 degrees. they differ")
print("only in saturation and value:")
for name in ("pure red", "dark red", "pink"):
    r, g, b = dict(swatches)[name]
    h, s, v = rgb_to_hsv(r, g, b)
    print("   %-10s hue %3.0f, saturation %.2f, value %.2f" % (name, h, s, v))
print("   that is the property the whole colour space exists for.")
print()

print("HUE IS AN ANGLE, so the colours wrap:")
for deg, name in ((0, "red"), (60, "yellow"), (120, "green"),
                  (180, "cyan"), (240, "blue"), (300, "magenta"), (360, "red again")):
    print("   %3d degrees -> %s" % (deg, name))
print("   which means hue arithmetic is circular. the distance between 350")
print("   and 10 degrees is 20, not 340, and code that forgets this splits")
print("   red into two separate ranges:")
for a, b in ((350, 10), (10, 350), (100, 200)):
    naive = abs(a - b)
    circ = min(naive, 360 - naive)
    print("      |%3d - %3d|: naive %3d, circular %3d %s"
          % (a, b, naive, circ, "  <- wrong" if naive != circ else ""))
print()

print("WHY THIS MATTERS FOR SEGMENTING BY COLOUR. take a red object")
print("photographed under three lighting conditions:")
lit = [("bright sun", (255, 40, 40)), ("indoors", (150, 25, 25)),
       ("shadow", (70, 12, 12))]
print("%14s %18s %28s" % ("condition", "RGB", "HSV"))
for name, (r, g, b) in lit:
    h, s, v = rgb_to_hsv(r, g, b)
    print("%14s %18s %10.0f %8.3f %8.3f" % (name, str((r, g, b)), h, s, v))
print()
rgbs = np.array([c for _, c in lit], float)
hsvs = np.array([rgb_to_hsv(*c) for _, c in lit])
print("   spread across the three, per channel:")
print("      RGB: R varies by %3.0f, G by %3.0f, B by %3.0f"
      % tuple(rgbs.max(0) - rgbs.min(0)))
print("      HSV: H varies by %.1f, S by %.3f, V by %.3f"
      % tuple(hsvs.max(0) - hsvs.min(0)))
print("   the hue barely moves. an RGB threshold has to cover a large")
print("   3-D box to catch all three; a hue threshold is one narrow band.")
print()

print("   a red detector in each space, tested on the three lit versions")
print("   plus some things that are NOT the object:")
others = [("skin", (230, 180, 150)), ("orange", (255, 140, 0)),
          ("grey wall", (150, 150, 150)), ("dark blue", (20, 20, 90))]
print("%14s %18s %14s %14s" % ("sample", "RGB", "RGB rule", "hue rule"))
for name, (r, g, b) in lit + others:
    h, s, v = rgb_to_hsv(r, g, b)
    rgb_hit = r > 120 and g < 80 and b < 80          # tuned for bright sun
    hue_hit = (h < 15 or h > 345) and s > 0.5 and v > 0.03
    print("%14s %18s %14s %14s"
          % (name, str((r, g, b)),
             "MATCH" if rgb_hit else "-", "MATCH" if hue_hit else "-"))
print("   the RGB rule was tuned on the bright sample. it survives the")
print("   indoor one and loses the object entirely in shadow, because its")
print("   'R > 120' test is really a brightness test wearing a colour")
print("   costume. the hue rule catches all three appearances of the same")
print("   object and still rejects skin, orange, grey and blue.")
print()

print("THE PRACTICAL SPLIT:")
print("   RGB  -- what a display emits and a sensor records. correct for")
print("           storage, transmission and as a neural network's input.")
print("   HSV  -- separates WHAT COLOUR from HOW BRIGHT, which is what you")
print("           want for thresholding, chroma keying and colour tracking.")
print("   and one caveat: hue is undefined when saturation is 0. a grey")
print("   pixel has no colour to name:")
for name in ("white", "grey", "black"):
    r, g, b = dict(swatches)[name]
    h, s, v = rgb_to_hsv(r, g, b)
    print("      %-8s saturation %.2f -> hue reported as %.0f, and it means"
          % (name, s, h))
    print("      %-8s nothing" % "")
print("   so always gate a hue test on a minimum saturation, or grey pixels")
print("   will match whatever colour you were looking for.")
```

""",
    [
        {"q": "Why is selecting 'anything red' easier in HSV than in RGB?",
         "options": ["HSV uses fewer numbers",
                     "Hue holds the colour alone, so one range covers dark, pale and vivid reds",
                     "RGB cannot represent red",
                     "HSV is higher precision"],
         "answer": 1,
         "why": "In RGB, brightness and purity change all three channels, so a red range is three coupled conditions. In HSV the colour is one number and lighting mostly moves the other two."},
        {"q": "Why should a hue mask usually also require a minimum saturation?",
         "options": ["To make it faster",
                     "Near-grey pixels have an unstable, essentially arbitrary hue",
                     "Saturation is more accurate than hue",
                     "Hue is undefined above 180"],
         "answer": 1,
         "why": "When R, G and B are nearly equal, the hue angle is decided by tiny differences and jumps around. Requiring real saturation means requiring a definite colour."},
        {"q": "What breaks a naive `10 < hue < 350` test for red?",
         "options": ["Hue is circular and red straddles 0",
                     "The range is too wide",
                     "Hue is stored as a float",
                     "Red has no hue"],
         "answer": 0,
         "why": "That test selects everything except red. Because the hue axis wraps, red needs two ranges - near 0 and near 360 - or a rotation of the axis first."},
    ],
)


# ---------------------------------------------------------------------------
# 7. Resizing and interpolation
# ---------------------------------------------------------------------------
topic(
    "resizing_and_interpolation",
    "Resizing and Interpolation",
    "Geometry",
    "Enlarging an image means inventing pixels. How you invent them is the "
    "difference between blocks and mush.",
    _svg(_grid(18, 30, 12, 3, 3, fill=S)
         + _txt(70, 52, "&#8594;", A, 13)
         + _grid(86, 24, 8, 6, 6, fill=S)
         + _txt(80, 80, "one small grid, more pixels", M, 7)),
    {
        "op": "resample",
        "source": "blocks",
        "controls": [
            {"key": "method", "label": "Interpolation", "type": "select", "value": "nearest",
             "options": [{"value": "nearest", "label": "Nearest neighbour"},
                         {"value": "bilinear", "label": "Bilinear"}]},
            {"key": "factor", "label": "Downscale first by", "type": "range",
             "min": 2, "max": 12, "step": 1, "value": 6},
        ],
    },
    [
        "Enlarging cannot add information. It can only decide what to put "
        "between the pixels that exist.",
        "Nearest neighbour copies the closest pixel. Fast, exact for pixel art, "
        "blocky for everything else.",
        "Bilinear takes a weighted average of the four surrounding pixels. "
        "Smoother, and softer.",
        "Shrinking has the opposite problem: sampling without averaging first "
        "produces aliasing, which is why area averaging exists.",
    ],
    """
title: Resizing and Interpolation
intro: What happens between the pixels, and why the answer looks different every time.

## Enlarging invents; shrinking discards

Resizing is two different problems wearing one name.

**Enlarging** asks for pixels that were never measured. A 4&#215;4 image
stretched to 8&#215;8 needs 64 values where 16 exist. The extra 48 have to
come from somewhere, and wherever they come from, they are a guess. No
interpolation method adds information &mdash; the choice is only about which
plausible guess to make.

**Shrinking** has too much data rather than too little, and the risk is
throwing away the wrong parts.

## Nearest neighbour

For each output pixel, work out where it lands in the input and copy whichever
input pixel is closest. That is all.

It is the fastest possible method, and it is **exact** in one important sense:
every output value is a value that genuinely appeared in the input. Nothing is
averaged, so nothing is invented that was not there.

The cost is blockiness. Neighbouring output pixels that map to the same input
pixel are identical, so enlarging produces flat squares with hard steps between
them. Diagonal edges come out as staircases.

That is often exactly right. Pixel art must be scaled with nearest neighbour or
it stops being pixel art. A segmentation mask where pixel value 3 means "road"
must be scaled with nearest neighbour, because averaging 3 and 5 gives 4, which
might mean "building" &mdash; a label is a name, not a quantity, and names do
not average.

## Bilinear

For each output pixel, find the four input pixels surrounding its position and
take a weighted average, with weights from how close the position is to each.
Linear in one direction, then linear in the other; hence bilinear.

Diagonals become smooth, gradients stay gradual, and the staircase disappears.
The cost is softness: an average of neighbours is by definition less extreme
than its inputs, so hard edges are pulled apart into ramps. Enlarge by a large
factor and the result is not blocky but mushy.

Switch between the two above with the downscale factor set high. The same
information is present in both; only the guessing strategy differs, and it is
easy to see that neither is simply better.

**Bicubic** extends the idea to sixteen surrounding pixels with a cubic weight
function. It is sharper than bilinear because the cubic curve overshoots
slightly at edges, adding a small amount of local contrast. Photo editors
default to it for that reason. The overshoot is also its failure mode: it can
produce faint halos beside high-contrast edges.

| Method | Reads | Speed | Good for | Fails at |
|---|---|---|---|---|
| Nearest | 1 pixel | fastest | pixel art, label masks | photographs |
| Bilinear | 4 pixels | fast | general enlargement | large factors |
| Bicubic | 16 pixels | slower | photographs | can halo |
| Area | a block | fast | shrinking | not for enlarging |

## Shrinking is a different failure

To halve an image, it is tempting to keep every second pixel. This is wrong,
and wrong in a way that looks like a bug elsewhere in the program.

Consider a pattern of alternating black and white columns. Keep every second
column and you may get all the black ones &mdash; a solid black image. Shift by
one and you get solid white. Detail finer than the new sampling grid does not
disappear gracefully; it reappears as a completely different, false pattern.
This is **aliasing**, and it is why photographs of striped shirts on video
develop rainbow moiré.

The fix is to average before sampling. **Area interpolation** takes the mean of
every input pixel that falls inside each output pixel's footprint, so nothing
is silently dropped. Gaussian blurring before downsampling achieves the same
end, and is what an image pyramid does at every level.

This matters for machine learning specifically. A dataset resized with a
naive-sampling routine has aliased artefacts that vary with the original
resolution, and a network will happily learn them.

## Where it goes wrong

**Bilinear on a label mask.** Averaging class indices produces indices that
mean something else. Nearest neighbour, always.

**Enlarging to fix a low-resolution input.** Upscaling before feeding a model
adds no information and costs computation. Learned super-resolution is a
different thing entirely &mdash; it hallucinates plausible detail from a prior,
which is useful for viewing and dangerous for measurement.

**Repeated resizes.** Each interpolation softens. Resize once from the original
rather than in steps.

**Ignoring aspect ratio.** Stretching to a square distorts every shape in the
frame. Pad to the target aspect ratio, then resize.
""",
    [
        {"q": "Why must a segmentation mask be resized with nearest neighbour?",
         "options": ["It is faster",
                     "Class indices are names, and averaging two of them can produce a third unrelated class",
                     "Masks are always small",
                     "Bilinear does not work on integers"],
         "answer": 1,
         "why": "Averaging label 3 and label 5 gives 4, which is a different class entirely. Labels are categorical, so only copying is safe."},
        {"q": "What causes aliasing when shrinking an image?",
         "options": ["Using too many bits per pixel",
                     "Sampling without averaging first, so fine detail reappears as a false pattern",
                     "The image being too large",
                     "Bicubic overshoot"],
         "answer": 1,
         "why": "Detail finer than the new sampling grid is not lost gracefully - it beats against the grid and produces a pattern that was never in the scene. Averaging before sampling prevents it."},
        {"q": "Why can bicubic interpolation produce halos near high-contrast edges?",
         "options": ["It reads too few pixels",
                     "Its cubic weight function overshoots slightly, adding local contrast",
                     "It converts to greyscale",
                     "It averages sixteen pixels equally"],
         "answer": 1,
         "why": "The overshoot is what makes bicubic look sharper than bilinear. Beside a strong edge the same overshoot shows up as a faint bright or dark fringe."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Affine transforms
# ---------------------------------------------------------------------------
topic(
    "affine_transforms",
    "Affine Transforms",
    "Geometry",
    "Six numbers rotate, scale, shear and shift an image. Edit them directly "
    "and watch what each one controls.",
    _svg(_box(18, 30, 34, 34, fill=S)
         + _txt(70, 52, "M", A, 13)
         + '<g transform="rotate(-14 118 47)">' + _box(96, 28, 44, 38, fill=S, stroke=A) + '</g>'
         + _txt(80, 80, "one matrix, every rigid change", M, 7)),
    {
        "op": "affine",
        "source": "shapes",
        "controls": [
            {"key": "a", "label": "a (x scale)", "type": "range",
             "min": -2, "max": 2, "step": 0.05, "value": 1},
            {"key": "b", "label": "b (y shear)", "type": "range",
             "min": -1.5, "max": 1.5, "step": 0.05, "value": 0},
            {"key": "c", "label": "c (x shear)", "type": "range",
             "min": -1.5, "max": 1.5, "step": 0.05, "value": 0.35},
            {"key": "d", "label": "d (y scale)", "type": "range",
             "min": -2, "max": 2, "step": 0.05, "value": 1},
            {"key": "e", "label": "e (x shift)", "type": "range",
             "min": -60, "max": 60, "step": 1, "value": 0},
            {"key": "f", "label": "f (y shift)", "type": "range",
             "min": -50, "max": 50, "step": 1, "value": 0},
        ],
    },
    [
        "An affine transform maps straight lines to straight lines and keeps "
        "parallel lines parallel.",
        "The four numbers a, b, c, d do the rotating, scaling and shearing; "
        "e and f do the translating.",
        "The determinant ad &minus; bc is how much area scales by. At zero the "
        "transform collapses the image to a line.",
        "Implementations iterate over the <em>output</em> and look backwards, "
        "because iterating forwards leaves holes.",
    ],
    """
title: Affine Transforms
intro: Six numbers that cover every rotation, scale, shear and shift an image can take.

## One matrix for four operations

Rotating, scaling, shearing and translating look like four separate things.
They are one thing with different numbers in it &mdash; an **affine transform**,
written as a 2&#215;3 matrix:

```
| a  b  e |
| c  d  f |
```

A point at (x, y) moves to (ax + by + e, cx + dy + f). The four numbers a, b, c
and d handle everything that involves direction &mdash; rotation, scale, shear,
flip &mdash; and e and f slide the result sideways and down.

The defining property is in the name: affine transforms preserve straightness
and parallelism. A straight line stays straight, and two parallel lines stay
parallel. Anything you can do to a photograph by moving, turning, stretching or
skewing it is affine. Anything involving perspective &mdash; railway tracks
converging &mdash; is not, because parallel lines stop being parallel.

## What each number does

Set everything to the identity &mdash; a and d at 1, the rest at 0 &mdash; and
the image is unchanged. Then move one at a time.

**a scales horizontally.** At 2 the image doubles in width; at 0.5 it halves;
at &minus;1 it mirrors left-to-right.

**d scales vertically**, the same way.

**c shears in x.** Each row slides sideways in proportion to its distance from
the centre, turning a rectangle into a parallelogram. This is the italic
transformation.

**b shears in y**, tilting columns instead of rows.

**e and f translate**, in pixels, and are the only two that do not interact
with the others.

Rotation is not its own control because it does not need one. A rotation by
&theta; is:

```
a =  cos t    b = -sin t
c =  sin t    d =  cos t
```

Set a and d to 0.87 and c to 0.5 with b at &minus;0.5 and the image turns by
thirty degrees. Rotation is a particular combination of scale and shear, which
is the sort of fact the matrix makes obvious and four separate functions hide.

## The determinant

The readout under the visualisation shows **ad &minus; bc**, the determinant.
It has a direct meaning: it is the factor by which area is multiplied.

A pure rotation has determinant 1, because rotating does not change area.
Doubling both scales gives 4. A negative determinant means the image has been
flipped &mdash; orientation reversed.

At determinant 0 the transform is not invertible, and geometrically it has
collapsed the plane onto a line. Set a and c to the same value with b and d
matching and the image degenerates. Nothing can undo that, because the
information about position along the lost direction is gone.

## Why implementations work backwards

The obvious way to apply a transform is to loop over input pixels, compute
where each lands, and write it there. This produces a broken image.

When the transform enlarges, adjacent input pixels land more than one pixel
apart in the output, leaving gaps that nothing ever writes to &mdash; a
lattice of holes. When it shrinks, several inputs land on the same output and
fight over it.

Real implementations invert the problem. Loop over every **output** pixel, apply
the *inverse* transform to find where it came from in the input, and sample
there. Every output pixel gets written exactly once, so there are no holes, and
the sampling step is an ordinary interpolation problem &mdash; nearest
neighbour or bilinear, with the same trade-offs as
[resizing](resizing_and_interpolation.html).

This is why the code above computes the inverse rather than the forward map,
and why an affine transform needs an interpolation choice at all.

## Where it shows up

**Data augmentation.** Small random rotations, scales and shears applied to
training images teach a network that a cat rotated by ten degrees is still a
cat. It is the cheapest regularisation there is, and it is affine.

**Image registration.** Aligning two photographs of the same scene means finding
the affine transform that best maps one onto the other.

**Document scanning.** Straightening a page photographed at an angle is affine
if the camera was square to the page and projective if it was not, which is why
scanning apps ask you to mark the corners.

## Where it goes wrong

**Expecting to correct perspective.** Affine cannot. A photograph taken from an
angle needs a projective (homography) transform, which has eight parameters and
does not preserve parallelism.

**Composing in the wrong order.** Matrix multiplication does not commute.
Rotate-then-translate and translate-then-rotate give different results, and
which one you meant is usually clear only after seeing the wrong one.

**Rotating about the origin by accident.** The formulas rotate about (0, 0),
which is a corner. Rotating about the centre means translating the centre to the
origin, rotating, and translating back &mdash; three matrices multiplied
together.

**Losing the corners.** A rotated rectangle does not fit in the original frame.
Either accept the clipping or compute the bounding box of the transformed
corners and enlarge the canvas first.
""",
    [
        {"q": "What does the determinant ad - bc of an affine transform tell you?",
         "options": ["The rotation angle",
                     "The factor by which area is scaled",
                     "The translation distance",
                     "The number of pixels lost"],
         "answer": 1,
         "why": "A pure rotation has determinant 1 because area is unchanged. Negative means the image was flipped, and zero means the plane has collapsed onto a line and nothing can invert it."},
        {"q": "Why do implementations iterate over output pixels and apply the inverse transform?",
         "options": ["It is faster",
                     "Iterating forwards leaves unwritten holes when the transform enlarges",
                     "The forward transform is not defined",
                     "It avoids needing interpolation"],
         "answer": 1,
         "why": "Forward mapping scatters input pixels to output positions, leaving gaps under enlargement and collisions under shrinking. Backward mapping writes every output pixel exactly once."},
        {"q": "Which of these is NOT an affine transform?",
         "options": ["Rotation", "Shear", "Perspective correction of a tilted photograph", "Uniform scaling"],
         "answer": 2,
         "why": "Affine transforms keep parallel lines parallel. Perspective makes parallel lines converge, so it needs a projective transform with eight parameters instead of six."},
    ],
)

# ---------------------------------------------------------------------------
# 9. Receptive field
# ---------------------------------------------------------------------------
topic(
    "receptive_field",
    "Receptive Field",
    "CNN Internals",
    "One pixel deep in a network sees a patch of the original image. Work out "
    "how big that patch is, and why stacking beats widening.",
    _svg(_grid(10, 30, 9, 15, 1, fill=S)
         + _grid(37, 46, 9, 9, 1, fill=S)
         + _grid(64, 62, 9, 3, 1, fill=S)
         + _txt(80, 24, "one output, many inputs", M, 8)),
    {
        "diagram": "receptive",
        "controls": [
            {"key": "layers", "label": "Layers", "type": "range",
             "min": 1, "max": 4, "step": 1, "value": 3},
            {"key": "kernel", "label": "Kernel size", "type": "range",
             "min": 3, "max": 7, "step": 2, "value": 3},
            {"key": "stride", "label": "Stride", "type": "range",
             "min": 1, "max": 2, "step": 1, "value": 1},
        ],
    },
    [
        "The receptive field is how much of the <em>original input</em> a single "
        "unit can be influenced by.",
        "With stride 1, each layer adds <code class='mono-font'>k &minus; 1</code> "
        "to the receptive field. Growth is linear in depth.",
        "With stride greater than 1, later layers add more, because each step "
        "covers more original pixels. Growth becomes geometric.",
        "Three stacked 3&#215;3 layers see 7&#215;7 using 27 weights per channel "
        "pair. One 7&#215;7 layer sees the same using 49.",
    ],
    """
title: Receptive Field
intro: How much of the original image a single deep unit can actually see, and why the answer shapes architecture.

## The question

Take one number in the output of a convolutional network's third layer. Change
a pixel in the input image. Does that number change?

For most pixels, no. A convolution is local &mdash; each output depends only on
a small window of its input &mdash; and stacking local operations gives an
output that depends on a larger, but still bounded, region of the original
image. That region is the unit's **receptive field**, and it is the honest
answer to "what can this feature possibly be detecting".

A unit with a 7&#215;7 receptive field cannot detect a face in a 224&#215;224
photograph. It has never seen a face. It has seen a 7&#215;7 patch, and
whatever it responds to has to be visible in one.

## Counting it, one layer at a time

Drag the layers control above and watch the highlighted band widen as it moves
down the diagram. Each row shows how many input pixels the layer above can be
influenced by.

With stride 1 the rule is simple. A single unit sees 1 pixel of its own input.
One `k`&#215;`k` convolution makes that `k`. Another adds `k - 1` more, because
the window's centre already covers what the previous layer covered and each
side extends by `(k-1)/2`. So:

```
r = 1
for each layer:
    r = r + (k - 1)
```

Three 3&#215;3 layers: 1 → 3 → 5 → 7. The growth is **linear in depth**, and
that is slow. A network of twenty 3&#215;3 layers at stride 1 has a receptive
field of 41 pixels &mdash; less than a fifth of a 224-pixel image.

## Stride changes the arithmetic

Set the stride control to 2 and the widening accelerates sharply.

The reason is that stride changes the *spacing* between the positions a layer
looks at, measured in original pixels. Call that spacing the jump. At stride 1
the jump stays 1 forever. At stride 2 it doubles every layer, so a step of one
unit in layer three corresponds to a step of four pixels in the input.

```
r = 1; jump = 1
for each layer:
    r = r + (k - 1) * jump
    jump = jump * stride
```

Now the additions themselves grow, and the receptive field expands
geometrically rather than linearly. This is the real reason architectures
downsample. Pooling and strided convolutions are usually explained as reducing
computation, which they do &mdash; but the more important effect is that they
are the only affordable way to get a deep unit to see the whole image.

## Why 3&#215;3 won everything

Two stacked 3&#215;3 convolutions have the same 5&#215;5 receptive field as
one 5&#215;5 convolution. Three stacked have the same 7&#215;7 as one
7&#215;7. So why not just use the big kernel?

Count the weights, per input/output channel pair:

| Arrangement | Receptive field | Weights |
|---|---|---|
| One 5&#215;5 | 5&#215;5 | 25 |
| Two 3&#215;3 | 5&#215;5 | 18 |
| One 7&#215;7 | 7&#215;7 | 49 |
| Three 3&#215;3 | 7&#215;7 | 27 |

The stack is cheaper, and it has a second advantage that matters more: there is
a non-linearity between the layers. One 7&#215;7 convolution is a single
linear function of its 49 inputs. Three 3&#215;3 convolutions with ReLUs
between them is a composition of three linear functions separated by
non-linearities, which can represent things a single linear map cannot.

VGG made this argument explicitly in 2014 and effectively ended large kernels
in general-purpose vision architectures. Everything since is 3&#215;3 stacks,
with the occasional [1&#215;1](one_by_one_convolutions.html) for channel work.

## Effective versus theoretical

The number the formula gives is the *theoretical* receptive field: the set of
pixels that could in principle affect the output.

The **effective** receptive field is smaller and softer. Contributions from the
edge of the theoretical field pass through fewer paths than contributions from
the centre, and the number of paths falls off roughly like a Gaussian. In
practice a unit is strongly influenced by the middle of its field and barely
influenced by the rim.

The practical consequence is that a network usually needs a theoretical
receptive field noticeably larger than the objects it has to recognise, not
merely equal to them. Dilated convolutions exist largely as a way to buy
receptive field without buying downsampling, which matters when the output has
to stay at full resolution &mdash; segmentation, most obviously.

## Where it goes wrong

**Assuming depth alone is enough.** Twenty stride-1 layers of 3&#215;3 still
only see 41 pixels. Without downsampling or dilation, a deep network can be
blind to anything large.

**Forgetting the input resolution.** A receptive field of 100 pixels covers
half a 224-pixel image and a twentieth of a 2000-pixel one. Resizing the input
silently changes what the architecture can see.

**Reading detection failures as a data problem.** If the model consistently
misses large objects, check the receptive field before collecting more images.

## How much of the image one output pixel can see

A single neuron deep in a network responds to a patch of the original image. Computing that patch's size layer by layer explains most architectural choices -- kernel sizes, depth, dilation and pooling.

```python-run
import numpy as np

print("the recurrence, and it is the whole calculation:")
print("    RF_out = RF_in + (kernel - 1) * jump_in")
print("    jump_out = jump_in * stride")
print("where 'jump' is how far apart two adjacent output pixels are, in")
print("input pixels.")
print()

def trace(layers, label):
    rf, jump = 1, 1
    print("%s" % label)
    print("%8s %10s %8s %8s %14s %12s"
          % ("layer", "type", "kernel", "stride", "receptive field", "jump"))
    print("%8s %10s %8s %8s %14d %12d" % ("input", "-", "-", "-", rf, jump))
    for i, (kind, k, s) in enumerate(layers, 1):
        rf = rf + (k - 1) * jump
        jump = jump * s
        print("%8d %10s %8d %8d %14d %12d" % (i, kind, k, s, rf, jump))
    return rf

rf = trace([("conv", 3, 1)] * 8, "EIGHT 3x3 CONVOLUTIONS, stride 1:")
print("   each layer adds exactly 2. after 8 layers a neuron sees %dx%d."
      % (rf, rf))
print("   growth is LINEAR in depth, which is slow -- to see a 224-pixel")
print("   image you would need %d layers." % ((224 - 1) // 2))
print()

rf = trace([("conv", 3, 1), ("conv", 3, 1), ("pool", 2, 2),
            ("conv", 3, 1), ("conv", 3, 1), ("pool", 2, 2),
            ("conv", 3, 1), ("conv", 3, 1), ("pool", 2, 2)],
           "THE VGG PATTERN -- two convs then a pool, three times:")
print("   %dx%d from 9 layers, against %dx%d from 8 layers without pooling."
      % (rf, rf, 17, 17))
print("   the stride is what accelerates it: after a stride-2 layer every")
print("   subsequent kernel step covers TWICE as much input, so growth")
print("   becomes geometric rather than arithmetic.")
print()

print("TWO 3x3 CONVOLUTIONS vs ONE 5x5. same receptive field, and this is")
print("why 3x3 won:")
for label, layers in (("one 5x5", [("conv", 5, 1)]),
                      ("two 3x3", [("conv", 3, 1), ("conv", 3, 1)])):
    rf_, jump_ = 1, 1
    params = 0
    for _, k, s in layers:
        rf_ += (k - 1) * jump_
        jump_ *= s
        params += k * k * 64 * 64
    print("   %-10s receptive field %dx%d, %s parameters (64->64 channels)"
          % (label, rf_, rf_, "{:,}".format(params)))
print("   the same field for %.0f percent of the parameters -- and two"
      % (100 * (2 * 9) / 25))
print("   non-linearities instead of one, which is the other half of the")
print("   argument.")
print()
for label, layers in (("one 7x7", [("conv", 7, 1)]),
                      ("three 3x3", [("conv", 3, 1)] * 3)):
    rf_, jump_, params = 1, 1, 0
    for _, k, s in layers:
        rf_ += (k - 1) * jump_
        jump_ *= s
        params += k * k * 64 * 64
    print("   %-10s receptive field %dx%d, %s parameters"
          % (label, rf_, rf_, "{:,}".format(params)))
print()

print("DILATION grows the field without adding parameters or losing")
print("resolution. a dilated kernel has gaps:")
for d in (1, 2, 4):
    eff = 3 + (3 - 1) * (d - 1)
    row = []
    for i in range(eff):
        row.append("x" if i % d == 0 else ".")
    print("   dilation %d: 3 weights spanning %d pixels   %s"
          % (d, eff, " ".join(row)))
print()
rf_, jump_ = 1, 1
print("   a stack with doubling dilation, all stride 1:")
print("%8s %10s %16s" % ("layer", "dilation", "receptive field"))
for i, d in enumerate((1, 2, 4, 8, 16), 1):
    eff = 3 + (3 - 1) * (d - 1)
    rf_ += (eff - 1) * jump_
    print("%8d %10d %16d" % (i, d, rf_))
print("   %d pixels from 5 layers and %d weights, with no downsampling at"
      % (rf_, 5 * 9))
print("   all. that is why dilation is the standard tool for segmentation,")
print("   where you need context AND per-pixel output resolution.")
print()

print("THE EFFECTIVE FIELD IS SMALLER THAN THE THEORETICAL ONE. not every")
print("input pixel contributes equally -- the centre is reached by many")
print("paths and the corners by one:")
w = np.array([[1.0]])
for layer in range(4):
    k = np.ones((3, 3))
    new = np.zeros((w.shape[0] + 2, w.shape[1] + 2))
    for i in range(w.shape[0]):
        for j in range(w.shape[1]):
            new[i:i + 3, j:j + 3] += w[i, j] * k
    w = new
w = w / w.max()
print("   contribution weight after 4 layers of 3x3 (theoretical field %dx%d):"
      % w.shape)
for r in w:
    print("      " + "".join("%6.2f" % v for v in r))
centre = w[w.shape[0] // 2, w.shape[1] // 2]
corner = w[0, 0]
print("   the centre pixel has weight %.2f; the corner has %.4f -- a factor"
      % (centre, corner))
print("   of %.0f. the field is gaussian-ish, not a flat square, so the" % (centre / corner))
print("   EFFECTIVE field is roughly the square root of the theoretical one.")
print("   that is a large part of why very deep networks still benefit from")
print("   explicit long-range mechanisms rather than depth alone.")
```

""",
    [
        {"q": "With stride 1, how does the receptive field grow as layers are added?",
         "options": ["Linearly, by k - 1 per layer",
                     "Geometrically, doubling each layer",
                     "By k per layer",
                     "It does not grow"],
         "answer": 0,
         "why": "Each layer's window centre already covers the previous field, so only the (k-1)/2 on each side is new. Three 3x3 layers give 1, 3, 5, 7."},
        {"q": "Why are three stacked 3x3 convolutions usually preferred over one 7x7?",
         "options": ["They are more accurate by definition",
                     "Same receptive field, fewer weights, and non-linearities in between",
                     "7x7 kernels cannot be trained",
                     "They use less memory at inference only"],
         "answer": 1,
         "why": "27 weights against 49 for the same 7x7 field, plus two ReLUs between the layers - so the stack can represent functions a single linear map cannot."},
        {"q": "Why is the effective receptive field smaller than the theoretical one?",
         "options": ["Padding removes the edges",
                     "Edge pixels reach the output through far fewer paths, so their influence falls off",
                     "The formula is an approximation",
                     "Stride reduces it"],
         "answer": 1,
         "why": "The number of paths from an input pixel to the output falls off roughly like a Gaussian away from the centre, so the rim of the theoretical field contributes very little."},
    ],
)


# ---------------------------------------------------------------------------
# 10. 1x1 convolutions
# ---------------------------------------------------------------------------
topic(
    "one_by_one_convolutions",
    "1x1 Convolutions",
    "CNN Internals",
    "A convolution with no spatial extent sounds pointless. It is one of the "
    "most useful layers in modern architectures.",
    _svg("".join('<line x1="46" y1="%d" x2="112" y2="%d" stroke="%s" stroke-width="0.7" stroke-opacity="0.5"/>'
                 % (26 + i * 13, 32 + j * 17, A)
                 for i in range(4) for j in range(3))
         + "".join(_box(34, 20 + i * 13, 12, 10, fill=S) for i in range(4))
         + "".join(_box(112, 26 + j * 17, 12, 12, fill=S, stroke=A) for j in range(3))
         + _txt(80, 84, "channels in, channels out", M, 7)),
    {
        "diagram": "channels",
        "controls": [
            {"key": "cin", "label": "Input channels", "type": "range",
             "min": 2, "max": 8, "step": 1, "value": 6},
            {"key": "cout", "label": "Output channels", "type": "range",
             "min": 1, "max": 8, "step": 1, "value": 3},
        ],
    },
    [
        "A 1&#215;1 convolution looks at one pixel position and <em>all</em> of "
        "its channels. It mixes channels, never neighbours.",
        "It is a fully-connected layer applied identically at every spatial "
        "position, which is why it is written as a convolution at all.",
        "Its main job is changing the channel count &mdash; usually reducing it "
        "before an expensive layer, which is what a bottleneck is.",
        "Weights: <code class='mono-font'>Cin &#215; Cout</code>, against "
        "<code class='mono-font'>9 &#215; Cin &#215; Cout</code> for a 3&#215;3.",
    ],
    """
title: 1x1 Convolutions
intro: A kernel with no spatial extent, and why almost every modern architecture is full of them.

## The operation that looks like nothing

A 3&#215;3 convolution combines a pixel with its eight neighbours. A 1&#215;1
convolution has no neighbours to combine. At first reading it appears to
multiply each pixel by a number, which is a scaling and hardly worth a layer.

That reading forgets the channel dimension, and the channel dimension is where
everything happens.

A feature map is not a grid of numbers; it is a **stack** of grids, one per
channel. A layer with 256 channels holds 256 values at every spatial position.
A 1&#215;1 convolution stands at one position, takes all 256 values there, and
computes a weighted sum of them &mdash; then does it again for each output
channel, and then repeats the whole thing at every position with the same
weights.

So it does not mix neighbours. It mixes **channels**. Drag the two controls
above and watch the connection pattern: every input channel reaches every
output channel, and nothing spatial happens at all.

## It is a fully-connected layer in disguise

Fix one spatial position and the operation is exactly a dense layer: `Cin`
inputs, `Cout` outputs, `Cin × Cout` weights. What makes it a convolution is
that the same dense layer is applied, unchanged, at every position in the map.

That is the same weight-sharing argument that motivates convolution in the
first place. If mixing channels in a particular way is useful at one location,
it is probably useful at all of them, and sharing the weights makes the layer
independent of the input's spatial size.

## What it is actually for

**Changing the channel count.** This is the common case. A 1&#215;1 convolution
is the cheapest possible way to turn 256 channels into 64, or 64 into 256, and
it is why the layer is sometimes called a projection.

**Bottlenecks.** Put a channel reduction before an expensive spatial
convolution and an expansion after it. ResNet's bottleneck block is exactly
this: 1&#215;1 down to 64 channels, 3&#215;3 at 64, 1&#215;1 back up to 256.
The 3&#215;3 &mdash; by far the costliest part &mdash; runs on a quarter of the
channels, and the two 1&#215;1s cost almost nothing by comparison.

Count it. A 3&#215;3 straight from 256 to 256 channels needs
`9 × 256 × 256 ≈ 590,000` weights. The bottleneck version needs
`256×64 + 9×64×64 + 64×256 ≈ 70,000`. Same input and output shape, an eighth of
the parameters, and an extra two non-linearities thrown in.

**Adding non-linearity without touching resolution.** Each 1&#215;1 is followed
by an activation, so a stack of them increases representational depth at
constant spatial size and negligible cost. This was the "network in network"
idea that named the technique.

**Replacing the classifier head.** Global average pooling followed by a
1&#215;1 convolution does the job of a large dense layer with a fraction of the
parameters, and works for any input size.

## The arithmetic

The readout above compares the two counts directly. For `Cin` input and `Cout`
output channels:

| Kernel | Weights | Sees |
|---|---|---|
| 1&#215;1 | Cin &#215; Cout | one position, all channels |
| 3&#215;3 | 9 &#215; Cin &#215; Cout | 3&#215;3 positions, all channels |
| Depthwise 3&#215;3 | 9 &#215; Cin | 3&#215;3 positions, one channel each |

That last row is worth noticing. A **depthwise separable** convolution splits
the work in two: a depthwise 3&#215;3 that mixes neighbours but not channels,
followed by a 1&#215;1 that mixes channels but not neighbours. Together they
approximate a full 3&#215;3 at roughly a ninth of the cost. MobileNet is built
almost entirely from that pair, and half of it is 1&#215;1 convolutions.

## Where it goes wrong

**Expecting spatial work from it.** It cannot smooth, sharpen or find an edge.
If the receptive field needs to grow, a 1&#215;1 contributes nothing &mdash;
its contribution to the [receptive field](receptive_field.html) is exactly
zero.

**Reducing channels too aggressively.** The bottleneck is a genuine information
bottleneck. Squeezing 256 channels to 8 before the spatial convolution saves
computation and can cost more accuracy than it is worth.

**Forgetting the activation.** A 1&#215;1 with no non-linearity after it,
stacked on another linear layer, collapses into a single linear map. Two
matrices multiplied together are one matrix.

## A convolution that looks at one pixel

A 1x1 kernel has no spatial extent at all, which sounds useless. It is a per-pixel linear layer across channels, and it is what makes bottleneck blocks and depthwise-separable convolutions affordable.

```python-run
import numpy as np

rng = np.random.default_rng(0)

H, W, C = 4, 4, 6
x = rng.normal(0, 1.0, (H, W, C))
print("a feature map: %dx%d positions, %d channels each." % (H, W, C))
print("   the vector at position (0,0): %s" % np.round(x[0, 0], 3))
print()

COUT = 3
W1 = rng.normal(0, 0.4, (C, COUT))
out = x @ W1                     # that is the entire operation
print("a 1x1 convolution with %d output channels is a %dx%d matrix applied"
      % (COUT, C, COUT))
print("to every position independently:")
print("   output at (0,0): %s" % np.round(out[0, 0], 3))
print("   by hand:         %s" % np.round(x[0, 0] @ W1, 3))
print("   shape %s -> %s" % (x.shape, out.shape))
print("   the spatial dimensions are untouched. only the channel count")
print("   changed, which is the whole purpose.")
print()

print("IT IS A DENSE LAYER, SHARED ACROSS POSITIONS. proof -- shuffle the")
print("positions and the outputs follow exactly:")
flat = x.reshape(-1, C)
perm = rng.permutation(H * W)
a = (flat @ W1)[perm]
b = flat[perm] @ W1
print("   identical: %s" % np.allclose(a, b))
print("   so it cannot mix information between positions. a 3x3 convolution")
print("   can; this cannot. it only mixes CHANNELS.")
print()

print("USE 1 -- CHANGING THE CHANNEL COUNT CHEAPLY. compare the cost of")
print("reducing 256 channels to 64:")
for kh in (1, 3, 5):
    p = kh * kh * 256 * 64
    print("   %dx%d conv, 256->64 : %12s parameters" % (kh, kh, "{:,}".format(p)))
print("   the 1x1 does the same job for a ninth of a 3x3's cost, because")
print("   there is no spatial window to weight.")
print()

print("USE 2 -- THE BOTTLENECK BLOCK, which is what ResNet-50 is built from.")
print("a 3x3 convolution on 256 channels, done two ways:")
direct = 3 * 3 * 256 * 256
print("   direct 3x3, 256->256                    : %12s"
      % "{:,}".format(direct))
squeeze = 1 * 1 * 256 * 64
middle = 3 * 3 * 64 * 64
expand = 1 * 1 * 64 * 256
total = squeeze + middle + expand
print("   1x1 256->64  (squeeze)                  : %12s" % "{:,}".format(squeeze))
print("   3x3 64->64   (the actual spatial work)  : %12s" % "{:,}".format(middle))
print("   1x1 64->256  (expand)                   : %12s" % "{:,}".format(expand))
print("   %-40s: %12s" % ("bottleneck total", "{:,}".format(total)))
print("   %.1fx fewer parameters, and the expensive 3x3 now runs on 64"
      % (direct / total))
print("   channels instead of 256 -- a %.0fx saving on that layer alone."
      % ((3 * 3 * 256 * 256) / (3 * 3 * 64 * 64)))
print()
print("   and it is still non-linear: there is a ReLU after each of the")
print("   three, so the block is not equivalent to one big convolution.")
print()

print("USE 3 -- CROSS-CHANNEL MIXING. each output channel is a learned")
print("combination of all input channels. here is what one output channel")
print("is made of:")
for j in range(COUT):
    contrib = np.abs(W1[:, j])
    order = np.argsort(-contrib)
    print("   output channel %d draws most on input channels %s"
          % (j, ", ".join("%d (%.2f)" % (i, W1[i, j]) for i in order[:3])))
print("   a 3x3 convolution also mixes channels, but it spends 9 weights per")
print("   pair doing it. if the mixing is all you need, 8 of those 9 are")
print("   wasted.")
print()

print("USE 4 -- MAKING A NETWORK FULLY CONVOLUTIONAL. a dense layer needs a")
print("fixed input size; a 1x1 convolution does not:")
for size in (7, 14, 28):
    feat = rng.normal(size=(size, size, 512))
    logits = feat @ rng.normal(0, 0.1, (512, 10))
    print("   %2dx%-2d input -> logits %s -- one prediction PER POSITION"
          % (size, size, logits.shape))
print("   that is how a classifier becomes a segmenter: replace the final")
print("   dense layer with a 1x1 convolution and it outputs a class map")
print("   instead of a class, at whatever resolution you feed it.")
print()

print("the summary in one line: a 1x1 convolution is the cheapest way to")
print("change how many channels you have, and the only convolution that")
print("does nothing spatial at all.")
```

""",
    [
        {"q": "What does a 1x1 convolution actually combine?",
         "options": ["A pixel and its eight neighbours",
                     "All the channels at a single spatial position",
                     "Every pixel in the feature map",
                     "Two adjacent channels"],
         "answer": 1,
         "why": "It has no spatial extent, so it never touches neighbours. At each position it takes a weighted sum across the whole channel stack, and repeats that with shared weights everywhere."},
        {"q": "Why does a ResNet bottleneck put 1x1 convolutions around the 3x3?",
         "options": ["To increase the receptive field",
                     "So the expensive 3x3 runs on far fewer channels",
                     "To normalise the activations",
                     "To downsample the spatial dimensions"],
         "answer": 1,
         "why": "The 3x3 cost scales with Cin x Cout. Reducing to 64 channels first and expanding after cuts a 590,000-weight block to about 70,000 for the same input and output shape."},
        {"q": "What happens to two stacked 1x1 convolutions with no activation between them?",
         "options": ["They double the receptive field",
                     "They collapse into a single linear map",
                     "They cannot be trained",
                     "They become a 2x2 convolution"],
         "answer": 1,
         "why": "Each is a matrix multiplication at every position. Two matrices multiplied together are one matrix, so the pair has exactly the representational power of one layer."},
    ],
)

# ---------------------------------------------------------------------------
# 11. Depthwise separable convolution
# ---------------------------------------------------------------------------
topic(
    "depthwise_separable_convolution",
    "Depthwise Separable Convolution",
    "Efficiency",
    "Split a convolution into the part that mixes neighbours and the part that "
    "mixes channels. The saving is roughly a factor of nine.",
    _svg(_box(12, 30, 40, 30, fill=S) + _txt(32, 48, "3x3", A, 9)
         + _txt(60, 48, "+", M, 11)
         + _box(70, 30, 40, 30, fill=S) + _txt(90, 48, "1x1", A, 9)
         + _txt(122, 42, "&lt;&lt;", M, 11) + _txt(132, 60, "full", M, 8)
         + _txt(80, 78, "same job, a ninth of the weights", M, 7)),
    {
        "diagram": "separable",
        "controls": [
            {"key": "cin", "label": "Input channels", "type": "range",
             "min": 8, "max": 512, "step": 8, "value": 64},
            {"key": "cout", "label": "Output channels", "type": "range",
             "min": 8, "max": 512, "step": 8, "value": 128},
            {"key": "kernel", "label": "Kernel size", "type": "range",
             "min": 3, "max": 7, "step": 2, "value": 3},
        ],
    },
    [
        "A full convolution mixes neighbours <em>and</em> channels in one step, "
        "which is why it costs <code class='mono-font'>k&sup2; &middot; Cin &middot; Cout</code>.",
        "The depthwise step runs one <code class='mono-font'>k&#215;k</code> "
        "filter per input channel, mixing neighbours only.",
        "The pointwise step is a <code class='mono-font'>1&#215;1</code> "
        "convolution, mixing channels only.",
        "Together they cost <code class='mono-font'>k&sup2;&middot;Cin + Cin&middot;Cout</code>, "
        "which for a 3&#215;3 with many channels is about a ninth.",
    ],
    """
title: Depthwise Separable Convolution
intro: One convolution split into two, and why almost every model that runs on a phone is built from them.

## What a full convolution is doing

A 3&#215;3 convolution from 64 channels to 128 does two jobs at once. At every
output position it looks at a 3&#215;3 spatial neighbourhood, and it combines
all 64 input channels. Each of the 128 output channels needs its own set of
weights for all of that, so the count is:

```
k * k * Cin * Cout  =  3 * 3 * 64 * 128  =  73,728
```

The question that leads to separable convolutions is whether those two jobs
have to be done together.

## Doing them one at a time

**Depthwise.** Run one `k`&#215;`k` filter per input channel, and keep the
channels apart. Channel 7 is convolved with filter 7 and produces channel 7 of
the output. Neighbours are mixed; channels are not. Cost: `k * k * Cin`, so
`9 * 64 = 576`.

**Pointwise.** Follow it with a [1&#215;1
convolution](one_by_one_convolutions.html), which combines all the channels at
each position and has no spatial extent at all. Channels are mixed; neighbours
are not. Cost: `Cin * Cout`, so `64 * 128 = 8,192`.

Together: **8,768** against 73,728 for the same input and output shape. Drag the
controls and the ratio in the readout stays close to 8&ndash;9&#215; wherever
you put them.

## Where the ratio comes from

The saving is

```
    k^2 * Cin * Cout
  ---------------------   =   1 / ( 1/Cout + 1/k^2 )
   k^2 * Cin + Cin * Cout
```

When `Cout` is large the `1/Cout` term nearly vanishes and the ratio approaches
`k^2` &mdash; nine for a 3&#215;3. Set the kernel control to 5 or 7 and the
saving rises toward 25 and 49, which is why separable convolutions matter more
the larger the kernel.

Set output channels to 8 while leaving input at 64 and the ratio falls, because
with few output channels the pointwise step is no longer cheap relative to the
whole. The technique earns its keep in wide layers, which is where the cost was.

## The cost of the saving

It is not free, and pretending otherwise is the usual mistake.

A full convolution can learn any function of a 3&#215;3&#215;`Cin`
neighbourhood. The separable pair cannot: it is restricted to functions that
factor into a spatial part and a channel part. That is a strictly smaller family,
and on the same architecture a separable model usually reaches slightly lower
accuracy per layer.

What makes it worth doing is that the saving is much larger than the loss. With
eight times fewer parameters you can afford more layers, wider layers, or a
model that fits on the device at all &mdash; and the resulting network usually
beats the full-convolution one at equal cost.

## Where it is used

**MobileNet** is built almost entirely from these pairs, and was the paper that
made the technique standard for on-device vision.

**Xception** applied the same argument to Inception, arguing that Inception
modules were already approximating a separable convolution and that the extreme
version worked better.

**EfficientNet** uses inverted residual blocks that expand channels with a
1&#215;1, do the spatial work depthwise, and project back down &mdash; the same
decomposition with an expansion around it.

## A note on speed

Parameter count and wall-clock time are not the same thing. A depthwise
convolution does very little arithmetic per byte of memory it touches, so it is
**memory-bound**, and hardware optimised for dense matrix multiplication does not
reach anything like its peak throughput on one.

An eight-times parameter reduction is therefore often two or three times faster
in practice rather than eight. Still worth having, and worth measuring rather
than assuming.

## Where it goes wrong

**Expecting the speed-up to match the parameter count.** Measure it.

**Using it in the first layer.** With three input channels there is almost
nothing to save, and the restriction costs accuracy where the model can least
afford it.

**Forgetting the non-linearity.** The depthwise and pointwise steps need an
activation between them, or the pair is closer to a single linear map than the
two-stage decomposition it is supposed to be.

## Splitting one convolution into two cheaper ones

A normal convolution mixes space and channels at once. Doing those separately costs a fraction as much, which is the whole idea behind MobileNet -- and this measures both the saving and what it gives up.

```python-run
import numpy as np

rng = np.random.default_rng(0)

def standard(kh, cin, cout):
    return kh * kh * cin * cout

def depthwise(kh, cin):
    return kh * kh * cin          # one kernel per input channel, no mixing

def pointwise(cin, cout):
    return 1 * 1 * cin * cout     # mixes channels, no spatial extent

print("a standard convolution does two jobs in one operation:")
print("   1. combine a spatial neighbourhood  (the kxk window)")
print("   2. combine the channels             (sum over c_in)")
print("and it pays kh*kw*cin*cout weights to do both together.")
print()
print("separating them:")
print("   DEPTHWISE   -- one kxk kernel per input channel, applied to that")
print("                  channel only. no channel mixing at all.")
print("   POINTWISE   -- a 1x1 convolution. all the channel mixing, no")
print("                  spatial extent.")
print()

print("THE SAVING. a 3x3 convolution, various channel counts:")
print("%12s %12s %16s %16s %12s %10s"
      % ("in", "out", "standard", "depthwise+point", "ratio", "1/ratio"))
for cin, cout in ((3, 32), (32, 64), (64, 128), (256, 256), (512, 512)):
    s = standard(3, cin, cout)
    d = depthwise(3, cin) + pointwise(cin, cout)
    print("%12d %12d %16s %16s %12.2fx %10.3f"
          % (cin, cout, "{:,}".format(s), "{:,}".format(d), s / d, d / s))
print()
print("   the ratio converges on 1/(kh*kw) + 1/cout. for a 3x3 with many")
print("   channels that is close to 1/9:")
for cout in (32, 128, 512, 4096):
    r = 1 / 9 + 1 / cout
    print("      cout=%5d -> %.4f of the standard cost (limit %.4f)"
          % (cout, r, 1 / 9))
print("   so a 3x3 depthwise-separable convolution costs roughly one ninth")
print("   of a normal one, and a 5x5 roughly one twenty-fifth.")
print()

H, W, CIN, COUT = 5, 5, 4, 3
x = rng.normal(0, 1.0, (H, W, CIN))

def conv_standard(x, k):
    # k: (3, 3, cin, cout)
    p = np.pad(x, ((1, 1), (1, 1), (0, 0)), mode="constant")
    out = np.zeros((x.shape[0], x.shape[1], k.shape[3]))
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            win = p[i:i + 3, j:j + 3, :]
            for o in range(k.shape[3]):
                out[i, j, o] = (win * k[:, :, :, o]).sum()
    return out

def conv_depthwise(x, kd):
    # kd: (3, 3, cin) -- one kernel per channel
    p = np.pad(x, ((1, 1), (1, 1), (0, 0)), mode="constant")
    out = np.zeros_like(x)
    for c in range(x.shape[2]):
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                out[i, j, c] = (p[i:i + 3, j:j + 3, c] * kd[:, :, c]).sum()
    return out

k_std = rng.normal(0, 0.3, (3, 3, CIN, COUT))
k_dw = rng.normal(0, 0.3, (3, 3, CIN))
k_pw = rng.normal(0, 0.3, (CIN, COUT))

out_std = conv_standard(x, k_std)
out_sep = conv_depthwise(x, k_dw) @ k_pw
print("RUN BOTH on a %dx%dx%d input, %d output channels:" % (H, W, CIN, COUT))
print("   standard          -> %s, %d weights" % (out_std.shape, k_std.size))
print("   depthwise + 1x1   -> %s, %d + %d = %d weights"
      % (out_sep.shape, k_dw.size, k_pw.size, k_dw.size + k_pw.size))
print("   same output shape, %.1fx fewer weights."
      % (k_std.size / (k_dw.size + k_pw.size)))
print()

print("WHAT IT GIVES UP. a standard convolution has an independent kxk")
print("kernel for EVERY (input channel, output channel) pair:")
print("   standard 3x3, %d->%d: %d distinct spatial kernels"
      % (CIN, COUT, CIN * COUT))
print("   depthwise 3x3, %d channels: %d distinct spatial kernels"
      % (CIN, CIN))
print("   so the separable version cannot learn 'detect a horizontal edge in")
print("   channel 2 but a vertical one in channel 2 for a different output'.")
print("   each input channel gets ONE spatial filter, and the pointwise layer")
print("   can only reweight the results.")
print()
print("   measured directly. for ONE input channel, collect the 3x3 kernel")
print("   it uses toward each output channel, as a 9 x %d matrix:" % COUT)
print("%22s %14s %14s" % ("input channel", "standard rank", "separable rank"))
for c in range(CIN):
    m_std = k_std[:, :, c, :].reshape(9, COUT)
    m_sep = k_dw[:, :, c].reshape(9, 1) * k_pw[c][None, :]
    print("%22d %14d %14d"
          % (c, np.linalg.matrix_rank(m_std), np.linalg.matrix_rank(m_sep)))
print("   the separable column is 1 every time, and that is the constraint")
print("   stated exactly: every output channel sees the SAME spatial")
print("   pattern from a given input channel, scaled by a single number.")
print("   the standard version gets an independent pattern for each pair.")
print()
print("SO THE TRADE IS CAPACITY FOR COST, and in practice it is a good one:")
print("   MobileNetV1 traded about %.0f%% of the parameters for a few points"
      % 90)
print("   of ImageNet accuracy, which is exactly the deal you want on a")
print("   phone. the usual repair is to make the network WIDER with the")
print("   savings, which buys much of the accuracy back:")
for width in (1.0, 1.5, 2.0):
    cin, cout = int(256 * width), int(256 * width)
    d = depthwise(3, cin) + pointwise(cin, cout)
    print("      width x%.1f: %s parameters against a standard 256->256's %s"
          % (width, "{:,}".format(d), "{:,}".format(standard(3, 256, 256))))
```

""",
    [
        {"q": "What does the depthwise step mix?",
         "options": ["Channels only", "Neighbours only, keeping channels separate",
                     "Both", "Neither"],
         "answer": 1,
         "why": "One k x k filter per input channel, producing one output channel each. The pointwise 1x1 that follows does the channel mixing."},
        {"q": "Why does the saving approach k squared for wide layers?",
         "options": ["The kernel grows",
                     "The ratio is 1/(1/Cout + 1/k^2), and the 1/Cout term vanishes as Cout grows",
                     "Depthwise convolutions have no weights",
                     "Wide layers use fewer channels"],
         "answer": 1,
         "why": "With many output channels the pointwise cost becomes small relative to the full convolution, leaving the k^2 factor - nine for a 3x3, 49 for a 7x7."},
        {"q": "Why is the wall-clock speed-up usually smaller than the parameter saving?",
         "options": ["The pointwise step dominates",
                     "A depthwise convolution does little arithmetic per byte touched, so it is memory-bound",
                     "It needs more layers",
                     "The weights are stored differently"],
         "answer": 1,
         "why": "Hardware tuned for dense matrix multiplication cannot reach peak throughput on an operation that is starved of arithmetic per memory access."},
    ],
)


# ---------------------------------------------------------------------------
# 12. Dilated convolutions
# ---------------------------------------------------------------------------
topic(
    "dilated_convolutions",
    "Dilated Convolutions",
    "CNN Internals",
    "Spread the same nine weights further apart and the receptive field grows "
    "without any downsampling and without any extra parameters.",
    _svg("".join(_box(20 + i * 16, 36, 10, 10, fill=(S if i % 2 else A), stroke=B, sw=1)
                 for i in range(9))
         + _txt(80, 68, "same nine weights, wider reach", M, 8)),
    {
        "diagram": "dilated",
        "controls": [
            {"key": "dilation", "label": "Dilation rate", "type": "range",
             "min": 1, "max": 4, "step": 1, "value": 2},
            {"key": "layers", "label": "Layers", "type": "range",
             "min": 1, "max": 3, "step": 1, "value": 2},
        ],
    },
    [
        "Dilation inserts gaps between the kernel's taps. A 3&#215;3 at "
        "dilation 2 spans 5&#215;5 while still holding nine weights.",
        "The parameter count does not change. The "
        "<a href='receptive_field.html'>receptive field</a> does.",
        "It buys reach without pooling, so the output stays at full resolution "
        "&mdash; which is what segmentation needs.",
        "Stacking the same rate repeatedly leaves gaps that nothing samples. "
        "Vary the rate instead.",
    ],
    """
title: Dilated Convolutions
intro: How to see further without downsampling, and the gridding artefact that comes with it.

## The problem it solves

A network has two ways to grow its [receptive
field](receptive_field.html): stack more layers, which is slow because growth is
linear, or downsample, which is fast but throws away resolution.

For classification, throwing away resolution is fine &mdash; the answer is one
label. For **segmentation** it is not, because the output has to be the same size
as the input, and detail destroyed by pooling has to be reconstructed by
something.

Dilated convolution is the third way. It grows the receptive field
geometrically, adds no parameters, and does not reduce resolution at all.

## What dilation does

Take a 3&#215;3 kernel. Instead of reading nine adjacent pixels, read nine
pixels spaced `d` apart, leaving gaps between them. The weights are unchanged;
only where they are sampled from moves.

The effective size of a `k`&#215;`k` kernel at dilation `d` is:

```
effective = k + (k - 1) * (d - 1)
```

So a 3&#215;3 at dilation 1 spans 3, at dilation 2 spans 5, at dilation 4 spans
9. Drag the dilation control and the readout confirms it: nine weights, spanning
whatever you asked for.

That is the whole trick, and its appeal is that everything about the layer's cost
is unchanged. Same weights, same number of multiplications, wider view.

## Stacking

Drag the layers control up. Two dilated layers reach further than two ordinary
ones, and the growth compounds, because each layer's reach is measured in the
already-expanded units of the layer beneath it.

The standard arrangement uses a rising sequence &mdash; dilation 1, then 2, then
4, then 8 &mdash; which gives exponential receptive-field growth at constant
resolution. A stack of four such layers sees a 33&#215;33 region using 36
weights per channel pair and no pooling at all.

## The gridding problem

There is a defect, and it follows directly from the gaps.

Stack several layers all at dilation 2, and some input positions are never
sampled by any of them. The kernel taps land on even offsets at every level, so
odd positions in between are simply not read. The output develops a
checkerboard-like inconsistency, and the network is blind to fine detail that
happens to fall in the gaps.

The fix is to vary the rate so that the gaps of one layer are covered by another.
Rates like 1, 2, 5 or 1, 2, 3 are chosen so their sampling patterns interlock,
and the *hybrid dilated convolution* literature is about picking such sequences.
The simple version of the rule: do not repeat the same dilation rate several
times in a row.

## Where it is used

**DeepLab** made dilated convolution central to semantic segmentation, and its
ASPP module runs several rates in parallel and concatenates them, giving the
network several scales at once from one feature map.

**WaveNet** used dilation in one dimension over audio, where the receptive field
has to span thousands of samples and downsampling would destroy the waveform.

**Dense prediction generally** &mdash; depth estimation, optical flow, anything
whose output is an image &mdash; uses it for the same reason segmentation does.

## Where it goes wrong

**Repeating one rate.** Gridding artefacts, and detail that falls in the gaps is
never seen.

**Using it where pooling would do.** For classification, downsampling is cheaper
and reduces computation. Dilation keeps the feature map large, and large feature
maps cost memory at every layer.

**Assuming it is free.** The parameters are free; the memory is not. A network
that never downsamples holds full-resolution activations throughout, which is
often the binding constraint on segmentation models.
""",
    [
        {"q": "How wide does a 3x3 kernel at dilation 3 reach?",
         "options": ["3", "7", "9", "5"],
         "answer": 1,
         "why": "k + (k-1)(d-1) = 3 + 2*2 = 7. Nine weights spanning seven positions - the parameter count is unchanged."},
        {"q": "What causes gridding artefacts?",
         "options": ["Too few weights",
                     "Several layers at the same dilation rate, so some input positions are never sampled by any of them",
                     "Dilation larger than the kernel",
                     "Missing padding"],
         "answer": 1,
         "why": "The taps land on the same offsets at every level, leaving positions in between unread. Varying the rate so the sampling patterns interlock is the fix."},
        {"q": "Why is dilation preferred over pooling in segmentation?",
         "options": ["It is faster",
                     "It grows the receptive field without reducing resolution, and the output must match the input size",
                     "It uses fewer weights than pooling",
                     "Pooling cannot be backpropagated"],
         "answer": 1,
         "why": "Detail destroyed by pooling has to be reconstructed by something. Dilation buys reach while the feature map stays full size - at the cost of memory."},
    ],
)


# ---------------------------------------------------------------------------
# 13. Global average pooling vs flatten
# ---------------------------------------------------------------------------
topic(
    "global_average_pooling",
    "Global Average Pooling against Flatten",
    "CNN Internals",
    "How a feature map becomes a vector, and why one of the two ways costs "
    "fifty times more weights than the other.",
    _svg(_box(14, 26, 40, 40, fill=S) + _txt(34, 78, "7x7x512", M, 7)
         + _txt(64, 46, "&#8594;", A, 12)
         + _box(78, 38, 14, 16, fill=S) + _txt(85, 78, "512", M, 7)
         + _txt(104, 46, "&#8594;", A, 12)
         + _box(120, 40, 26, 12, fill=S, stroke=A) + _txt(133, 78, "classes", M, 7)),
    {
        "diagram": "gap",
        "controls": [
            {"key": "side", "label": "Feature map size", "type": "range",
             "min": 3, "max": 14, "step": 1, "value": 7},
            {"key": "channels", "label": "Channels", "type": "range",
             "min": 32, "max": 1024, "step": 32, "value": 512},
            {"key": "classes", "label": "Classes", "type": "range",
             "min": 2, "max": 1000, "step": 2, "value": 10},
        ],
    },
    [
        "The convolutional part of a network outputs a 3D block. A classifier "
        "needs a vector, so something has to collapse it.",
        "<strong>Flatten</strong> reads every value in order. A "
        "7&#215;7&#215;512 map becomes 25,088 numbers.",
        "<strong>Global average pooling</strong> takes the mean of each channel. "
        "The same map becomes 512 numbers.",
        "Pooling also removes the fixed input size: the mean of a channel is one "
        "number whatever the spatial dimensions were.",
    ],
    """
title: Global Average Pooling against Flatten
intro: The step between the convolutions and the classifier, and why the obvious version wastes most of the model's parameters.

## Two ways to collapse a block

Convolutional layers output a 3D block: height &#215; width &#215; channels. A
classifier needs a single vector. Something has to turn one into the other, and
there are two candidates.

**Flatten** reads every value in the block into one long vector. For a
7&#215;7&#215;512 map that is 25,088 numbers, and the dense layer that follows
needs a weight for each of them per class.

**Global average pooling** takes the mean of each channel over its whole spatial
extent. Every 7&#215;7 slice becomes one number, and the block becomes 512
numbers.

## Count them

Drag the controls and watch the readout. At the defaults &mdash;
7&#215;7&#215;512 into 10 classes:

```
flatten  ->  7 * 7 * 512 * 10  =  250,880 weights
GAP      ->          512 * 10  =    5,120 weights
```

Forty-nine times fewer, and 49 is exactly 7&#215;7. The ratio is always the
spatial area of the feature map, which is why the saving grows as the map gets
larger.

Set classes to 1000, as in ImageNet, and the flattened version needs 25 million
weights in a single layer. Early architectures really did this: **VGG-16 keeps
about 90% of its 138 million parameters in its final dense layers**, and almost
all of that is the first one immediately after the flatten.

## What pooling gives up, and what it buys

Averaging discards **where** in the map each activation was. If channel 7
responds to wheels, flatten preserves that the wheels were at the bottom left,
and GAP records only that there were wheels.

For classification that is usually the right trade. The question is whether a car
is present, not where the wheels sat, and the convolutional layers underneath
have already encoded position-sensitive structure into which channels fire.

Three things are bought in exchange.

**Far fewer parameters**, and therefore much less overfitting. A dense layer with
25 million weights on a dataset of 50,000 images is an invitation to memorise.

**Any input size.** The mean of a channel is one number regardless of the
spatial dimensions, so a GAP network accepts a 224-pixel image or a 400-pixel one
without modification. A flattened network cannot: 25,088 weights expect exactly
25,088 inputs, which is why older models are rigid about input size.

**Interpretability.** With GAP followed by a single dense layer, each class score
is a weighted sum of channel means. That weighting is exactly what Class
Activation Mapping uses to produce a heatmap, and [Grad-CAM](grad_cam.html)
generalises it.

## What replaced the debate

Every modern architecture uses GAP. ResNet, Inception, MobileNet, EfficientNet
and the convolutional stems of hybrid transformers all end with a global pool and
one dense layer.

The exception worth knowing is **Vision Transformers**, which typically use a
dedicated class token instead &mdash; a learned vector that attends to all the
[patches](vision_transformer_patches.html) and carries the summary. Some ViT
variants pool the patch tokens instead and report it works about as well.

## Where it goes wrong

**Pooling too early.** GAP belongs after the last convolutional block. Applied
midway it destroys the spatial structure the remaining layers need.

**Using flatten because a tutorial did.** Most tutorials predate the change.
Check what the parameter count is doing before accepting it.

**Expecting GAP to fix a small feature map.** With a 1&#215;1 map there is
nothing to average and the two are identical.

**Forgetting global max pooling exists.** It takes the maximum instead of the
mean, and for tasks where one strong local response matters more than an average
&mdash; some detection and audio tasks &mdash; it can be the better choice.
""",
    [
        {"q": "How many times fewer weights does GAP need than flatten, for a 7x7 feature map?",
         "options": ["7", "49", "512", "It depends on the number of classes"],
         "answer": 1,
         "why": "The ratio is exactly the spatial area of the map. The number of channels and classes appear in both counts and cancel."},
        {"q": "Why can a GAP network accept any input size?",
         "options": ["It resizes the input",
                     "The mean of a channel is one number whatever the spatial dimensions were",
                     "It uses adaptive convolutions",
                     "The dense layer is optional"],
         "answer": 1,
         "why": "A flattened network's dense layer expects exactly as many inputs as the flatten produced, which fixes the input size. Pooling removes that constraint."},
        {"q": "What does global average pooling discard?",
         "options": ["The channel identity",
                     "Where in the feature map each activation occurred",
                     "The magnitude of the activations",
                     "Half the channels"],
         "answer": 1,
         "why": "It records that a channel fired, not where. For classification that is usually the right trade, since the convolutional layers already encode structure into which channels fire."},
    ],
)


# ---------------------------------------------------------------------------
# 14. Anchor boxes
# ---------------------------------------------------------------------------
topic(
    "anchor_boxes",
    "Anchor Boxes",
    "Detection",
    "Detectors do not invent boxes. They start from a fixed set at every "
    "position and learn how to nudge them.",
    _svg("".join('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="%s" '
                 'stroke-width="1" stroke-dasharray="3 3"/>' % (18 + i * 26, 22, 26, 20, B)
                 for i in range(5))
         + _box(52, 30, 58, 40, fill="none", stroke=A, sw=2)
         + _txt(80, 82, "fixed shapes, learned offsets", M, 7)),
    {
        "diagram": "anchors",
        "controls": [
            {"key": "cell", "label": "Grid cell", "type": "range",
             "min": 0, "max": 23, "step": 1, "value": 8},
            {"key": "scale", "label": "Anchor size", "type": "range",
             "min": 40, "max": 220, "step": 5, "value": 180},
        ],
    },
    [
        "At every position in a feature map the detector places several boxes of "
        "fixed size and aspect ratio.",
        "Each anchor is assigned by <a href='iou_and_non_max_suppression.html'>"
        "IoU</a> against the ground truth: high is positive, low is negative, "
        "and the band between is ignored.",
        "The network predicts an <em>offset</em> from its anchor, not a box. "
        "Regressing a small correction is far easier than regressing coordinates.",
        "Anchor-free detectors predict the box directly from a point, which "
        "removes the tuning but not the assignment problem.",
    ],
    """
title: Anchor Boxes
intro: The prior that turns 'find every object' into 'adjust these boxes slightly', and the assignment rule that trains it.

## Why detectors do not just predict boxes

A detector must output an unknown number of boxes at unknown positions and
sizes. Neural networks are much better at producing a fixed-size output than a
variable-length one, and much better at making a small correction than at
producing a coordinate from nothing.

**Anchors** convert the hard problem into the easy one. Place a fixed set of
reference boxes at every position of a feature map, and ask the network two
things per anchor: is there an object here, and how should this box be adjusted
to fit it?

The output is now a fixed-size tensor, and the regression target is a small
offset instead of an absolute position.

## What the visualisation shows

The dashed grid is the feature map: one set of anchors per cell. The orange
rectangle is a ground-truth object. Drag the cell control to move the anchor set
around, and the size control to change the scale.

Three anchors are drawn at each position, one per aspect ratio &mdash; wide,
square and tall &mdash; because objects come in shapes and one square box fits
few of them. Real detectors use three scales as well, so nine anchors per
position is a common arrangement.

The readout gives the best IoU against the ground truth and what that IoU means
for training.

## The assignment rule

Every anchor gets a label before training, decided by IoU:

| IoU with the best ground-truth box | Label |
|---|---|
| Above ~0.5 | positive &mdash; predict this object, regress the offset |
| Below ~0.3 | negative &mdash; predict background, no box loss |
| In between | ignored &mdash; contributes nothing to the loss |

The ignore band exists because those anchors are genuinely ambiguous, and
forcing them either way teaches the network something untrue.

The page opens on a positive anchor. Drag the size control down and the readout
walks through all three labels &mdash; positive, then ignored, then negative
&mdash; without the ground-truth box moving at all. That transition is where an
anchor stops being useful for an object, and it is why the anchor set has to
match the objects you expect.

## The imbalance nobody warns you about

A detector places tens of thousands of anchors on an image. An image with three
objects makes almost every one of them negative &mdash; ratios of a thousand to
one are normal.

Trained naively, the classification loss is dominated by easy background anchors
and the model learns to say "background" very confidently and nothing else. Three
responses became standard:

**Hard negative mining** &mdash; keep only the worst-scoring negatives so the
ratio stays around 3:1.

**Focal loss** &mdash; down-weight examples the model already gets right, so the
easy negatives stop dominating. This is what RetinaNet introduced, and it is why
one-stage detectors caught up with two-stage ones.

**Two-stage detection** &mdash; a region proposal network filters down to a few
hundred candidates before classification, which sidesteps the imbalance.

## Choosing the anchor set

Anchors are a **prior**, and a wrong prior is expensive. Scales and ratios tuned
for everyday photographs do badly on aerial imagery, where objects are small and
often square, or on text detection, where boxes are extremely wide.

YOLOv2 introduced picking them by running k-means over the ground-truth box
shapes in the training set, using IoU as the distance. That replaced a
hand-tuned guess with a fitted one, and it is still the sensible default when a
dataset's objects are unusual.

## Anchor-free detectors

FCOS, CenterNet and DETR drop anchors entirely. FCOS predicts, for each point
inside an object, the four distances to the box edges. CenterNet predicts object
centres as a heatmap. DETR predicts a fixed set of boxes directly and matches
them to ground truth with a Hungarian assignment.

They remove the anchor hyperparameters, which is a real simplification. What they
do not remove is the assignment problem &mdash; deciding which prediction is
responsible for which object &mdash; which is simply solved differently.

## Where it goes wrong

**Default anchors on unusual data.** Check the IoU distribution of your anchors
against your ground-truth boxes before training.

**Ignoring the imbalance.** Without focal loss or mining, the model predicts
background everywhere and the loss looks fine.

**Too many anchors.** Each one costs memory and computation at every position of
every feature map, and past a point they overlap so much that extra ones add
nothing.
""",
    [
        {"q": "What does the network predict for each anchor?",
         "options": ["Absolute box coordinates",
                     "An offset from that anchor, plus whether an object is present",
                     "A segmentation mask",
                     "The class only"],
         "answer": 1,
         "why": "Regressing a small correction to a known reference box is far easier than producing coordinates from nothing, and it makes the output a fixed-size tensor."},
        {"q": "Why do anchors with middling IoU get ignored rather than labelled?",
         "options": ["To save computation",
                     "They are genuinely ambiguous, and forcing them either way teaches the network something untrue",
                     "They are duplicates",
                     "IoU cannot be computed for them"],
         "answer": 1,
         "why": "An anchor at IoU 0.4 neither clearly covers the object nor clearly misses it. The ignore band keeps that ambiguity out of the loss."},
        {"q": "Why does focal loss exist?",
         "options": ["To speed up training",
                     "Because tens of thousands of anchors are negative, so easy background dominates the loss",
                     "To handle overlapping boxes",
                     "To replace IoU"],
         "answer": 1,
         "why": "It down-weights examples the model already classifies correctly, which is what let one-stage detectors match two-stage ones."},
    ],
)


# ---------------------------------------------------------------------------
# 15. mAP for object detection
# ---------------------------------------------------------------------------
topic(
    "mean_average_precision",
    "Mean Average Precision",
    "Detection",
    "The number every detection paper reports, built from a precision-recall "
    "curve one ranked prediction at a time.",
    _svg(_line(20, 72, 148, 72, B, 1) + _line(20, 72, 20, 16, B, 1)
         + '<path d="M22 22 C 60 26, 90 48, 146 62" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + _txt(96, 34, "AP = area", M, 8)),
    {
        "diagram": "map",
        "controls": [
            {"key": "iou", "label": "IoU threshold for a hit", "type": "range",
             "min": 0.5, "max": 0.95, "step": 0.05, "value": 0.5},
        ],
    },
    [
        "A prediction counts as correct if its "
        "<a href='iou_and_non_max_suppression.html'>IoU</a> with an unmatched "
        "ground-truth box clears a threshold.",
        "Sort every prediction by confidence, walk down the list, and plot "
        "precision against recall as you go.",
        "<strong>AP</strong> is the area under that curve for one class. "
        "<strong>mAP</strong> averages AP across classes.",
        "COCO's headline number averages again over IoU thresholds from 0.50 to "
        "0.95, which is why it is so much lower than the old VOC number.",
    ],
    """
title: Mean Average Precision
intro: How a list of boxes with confidence scores becomes one number, and what that number is not telling you.

## Deciding what counts as correct

Classification has an obvious notion of right. Detection does not: a box that
covers most of an object is partly right, and "partly" has to be resolved before
anything can be counted.

The resolution is a threshold on [IoU](iou_and_non_max_suppression.html). A
prediction is a **true positive** if its IoU with a ground-truth box of the same
class is at least the threshold, and if that ground-truth box has not already
been claimed by a higher-confidence prediction. Otherwise it is a false positive.
Ground-truth boxes nothing matched are false negatives.

That second condition matters. Without it, ten overlapping predictions on one
object would count as ten successes.

## Building the curve

Sort all predictions for a class by confidence, highest first, and walk down the
list. After each one, recompute precision and recall over everything seen so far,
and plot the point.

The curve in the visualisation is exactly that walk, one dot per prediction. It
starts high &mdash; the most confident predictions are usually right &mdash; and
sags as the list goes on, because later predictions are less reliable while the
recall denominator stays fixed.

**Average precision** is the area under that curve. It summarises the whole
ranking rather than performance at one operating point, which is what makes it
useful: a detector that ranks its correct predictions above its incorrect ones
scores well regardless of how its confidences happen to be calibrated.

The exact area calculation has varied. VOC 2007 sampled precision at eleven
recall levels; VOC 2010 onward and COCO interpolate more finely. The differences
are small and the definitions are not interchangeable, which is a reason to
compare numbers only within one convention.

## From AP to mAP

AP is per class. **mAP** is the mean of AP over all classes &mdash; an unweighted
mean, so a class with ten instances counts as much as a class with ten thousand.

That is a deliberate choice and worth knowing. It means mAP is dragged down hard
by rare classes the model handles badly, and a model can improve its mAP more by
fixing one rare class than by getting slightly better at a common one.

## Why COCO's numbers look worse

Drag the IoU control. At 0.5 a loosely fitting box counts as a hit; at 0.9 the
box has to be nearly exact.

VOC reported mAP at IoU 0.5 alone. COCO's headline metric averages mAP over ten
thresholds from 0.50 to 0.95 in steps of 0.05, usually written **mAP@[.5:.95]**.
It rewards precise localisation rather than approximate detection, and it is much
harsher: a detector reporting 0.80 under VOC might report 0.45 under COCO on the
same predictions.

So a COCO mAP and a VOC mAP are different measurements and must never be compared
directly. COCO also reports mAP@0.5 alongside, partly so that comparison remains
possible.

COCO breaks the number down further &mdash; by object size (small, medium,
large) and at fixed detection counts. Those breakdowns are usually more
informative than the headline: "our detector is bad at small objects" is
actionable in a way that "our mAP is 0.42" is not.

## What mAP does not tell you

**It has no threshold.** AP integrates over every confidence level, so it says
nothing about which threshold to deploy. That is a separate decision.

**It ignores the cost of errors.** A missed pedestrian and a spurious traffic
cone count the same.

**It averages away the failures you care about.** A model that is excellent on
19 classes and useless on the 20th can outscore one that is decent on all of
them.

**It says nothing about duplicates before NMS.** mAP is computed on
post-processed output, so a detector that fires many overlapping boxes can look
fine as long as suppression cleans up.

## Where it goes wrong

**Comparing across datasets or conventions.** VOC against COCO, or one AP
interpolation against another, are not comparable.

**Reporting mAP alone.** Report the per-class breakdown; it is where the
information is.

**Tuning NMS to raise mAP.** Easy to do and often makes the deployed detector
worse, because the operating point that maximises an integral over all
thresholds is not the one you ship.
""",
    [
        {"q": "Why must a matched ground-truth box be excluded from later matches?",
         "options": ["To save computation",
                     "Otherwise several overlapping predictions on one object would each count as a success",
                     "IoU cannot be computed twice",
                     "The boxes are consumed by NMS"],
         "answer": 1,
         "why": "Only the highest-confidence prediction claims a ground-truth box; the rest become false positives. Without that rule a detector could inflate its score by firing repeatedly."},
        {"q": "Why is a COCO mAP much lower than a VOC mAP on the same predictions?",
         "options": ["COCO has more classes",
                     "COCO averages over IoU thresholds from 0.50 to 0.95, rewarding precise localisation",
                     "COCO uses a different precision formula",
                     "COCO images are harder"],
         "answer": 1,
         "why": "VOC reported at IoU 0.5 alone. Averaging up to 0.95 demands nearly exact boxes, so the two numbers are different measurements and cannot be compared."},
        {"q": "What does mAP say about which confidence threshold to deploy?",
         "options": ["It gives the optimal threshold",
                     "Nothing - it integrates over every threshold",
                     "It assumes 0.5",
                     "It uses the threshold that maximises F1"],
         "answer": 1,
         "why": "AP summarises the whole ranking. Choosing an operating point is a separate decision, made from the costs of the two kinds of error."},
    ],
)


# ---------------------------------------------------------------------------
# 16. Template matching
# ---------------------------------------------------------------------------
topic(
    "template_matching",
    "Template Matching",
    "Matching",
    "Slide a patch over the image and score every position. The oldest way to "
    "find something, and the reason better ways exist.",
    _svg(_box(14, 24, 88, 46, fill=S)
         + _box(34, 34, 20, 20, fill="none", stroke=A, sw=1.6)
         + _txt(58, 82, "patch, everywhere", M, 7)
         + _box(112, 24, 34, 46, fill=S) + _txt(129, 48, "score", A, 9)),
    {
        "op": "template",
        "source": "shapes",
        "controls": [
            {"key": "tx", "label": "Template x", "type": "range",
             "min": 0, "max": 150, "step": 2, "value": 96},
            {"key": "ty", "label": "Template y", "type": "range",
             "min": 0, "max": 102, "step": 2, "value": 30},
            {"key": "size", "label": "Template size", "type": "range",
             "min": 8, "max": 40, "step": 2, "value": 24},
        ],
    },
    [
        "The template is cut from the image itself, so a perfect match exists "
        "and you can see whether the method finds it.",
        "Normalised cross-correlation subtracts the mean and divides by the "
        "standard deviation on both sides, so it survives lighting changes.",
        "The output is a <strong>response map</strong>: one score per position. "
        "Its brightest point is the match.",
        "It is not invariant to rotation or scale. Turn the object ten degrees "
        "and the correlation collapses.",
    ],
    """
title: Template Matching
intro: The most direct way to find something in an image, and a clear demonstration of why the field moved on.

## The method

Take a patch &mdash; the **template** &mdash; and place it over every possible
position in the image. At each position, score how well the template agrees with
what is underneath. The result is a **response map** with one score per position,
and the highest score is where the template was found.

The template here is cut from the image itself, using the position controls, so
a perfect match is guaranteed to exist. The grey square marks where it came from
and the orange square marks where it was found. Move the controls and they track
each other, with the correlation in the readout staying at 1.000.

## Scoring: why not just subtract?

The obvious score is the sum of squared differences. It works, and it breaks the
moment lighting changes: brighten the image by 20 and every difference grows,
even where the shapes match perfectly.

**Normalised cross-correlation** fixes this by standardising both sides before
comparing &mdash; subtract the mean, divide by the standard deviation, then take
the dot product:

```
NCC = sum( (T - mean_T) * (W - mean_W) ) / ( sd_T * sd_W )
```

Subtracting the means removes any constant brightness offset. Dividing by the
standard deviations removes any constant contrast scaling. What is left measures
**pattern** rather than pixel values, and the result is bounded between
&minus;1 and 1, which makes scores comparable across positions and images.

That is why NCC is the standard choice, and why the response map here is readable
as an image: every value is on the same scale.

## Reading the response map

The bright region around the true match is not a single pixel. It is a blob,
because a template shifted by one pixel still overlaps almost entirely and still
scores well.

That blob is why picking the maximum is not enough in practice. Several nearby
positions all score highly, and returning all of them means returning the same
detection several times. The standard fix is the same one detection uses:
suppress everything within a radius of a stronger response, which is exactly
[non-maximum suppression](iou_and_non_max_suppression.html).

Make the template small &mdash; drag the size control down &mdash; and the map
becomes noisy, with strong responses in places that merely happen to have a
similar local pattern. A small template does not contain enough structure to be
distinctive.

## What it cannot do

The limitations are severe and they are the reason the field developed
alternatives.

**Rotation.** A template rotated by ten degrees no longer aligns, and the
correlation falls sharply. Handling rotation means searching over angles as well
as positions.

**Scale.** The same problem in another dimension. Searching over scales too means
an image pyramid and a much larger search.

**Deformation.** A face is not a rigid patch. Any object that bends, or that
varies between instances, cannot be represented by one template.

**Cost.** Every position &#215; every scale &#215; every angle, each requiring
a full patch comparison, is expensive, though correlation via the FFT helps a
great deal in the translation-only case.

## Where it is still the right tool

Template matching has not disappeared, because when its assumptions hold it is
exact, needs no training data, and is trivially explainable.

Industrial inspection with a fixed camera and fixed part orientation. Finding a
known icon on a screen for UI automation. Aligning scanned documents against a
form. Matching a fixed logo. In all of these, position is the only unknown, which
is precisely the case the method solves.

Where the assumptions fail, the successors are **keypoint matching** &mdash;
[Harris corners](harris_corners.html), SIFT, ORB &mdash; which find distinctive
points and match those, giving rotation and scale invariance for free, and
learned detectors, which handle deformation and appearance variation as well.

## Where it goes wrong

**Sum of squared differences under changing light.** Use NCC.

**Taking the argmax without suppression.** The peak is a blob, not a point.

**A template that is too small.** Not distinctive; the map fills with false
peaks.

**Expecting invariance it does not have.** If the object can rotate or change
size, this is the wrong method, not a method that needs tuning.
""",
    [
        {"q": "Why is normalised cross-correlation preferred over sum of squared differences?",
         "options": ["It is faster",
                     "Standardising both sides removes brightness and contrast changes, so it measures pattern rather than pixel values",
                     "It handles rotation",
                     "It produces integer scores"],
         "answer": 1,
         "why": "Brightening the image by a constant grows every squared difference even where the shapes match perfectly. Subtracting means and dividing by standard deviations removes that."},
        {"q": "Why is the peak in a response map a blob rather than a point?",
         "options": ["The image is blurred",
                     "A template shifted by one pixel still overlaps almost entirely and still scores well",
                     "The correlation is normalised",
                     "The template is too large"],
         "answer": 1,
         "why": "That is why non-maximum suppression is needed: several nearby positions score highly and would otherwise be returned as separate detections of the same thing."},
        {"q": "Which of these does template matching handle natively?",
         "options": ["Rotation", "Scale change", "Translation", "Deformation"],
         "answer": 2,
         "why": "Position is the only unknown it searches over. Rotation and scale require searching those dimensions too, and deformation cannot be represented by a rigid patch at all."},
    ],
)


# ---------------------------------------------------------------------------
# 17. Harris corners
# ---------------------------------------------------------------------------
topic(
    "harris_corners",
    "Harris Corners and Keypoints",
    "Matching",
    "A flat region looks the same from everywhere, an edge looks the same along "
    "itself, and a corner does not. That difference is computable.",
    _svg(_box(16, 26, 40, 40, fill=S) + _txt(36, 78, "flat", M, 7)
         + _box(62, 26, 40, 40, fill=S) + _line(62, 46, 102, 46, B, 2)
         + _txt(82, 78, "edge", M, 7)
         + _box(108, 26, 40, 40, fill=S) + _line(108, 46, 128, 46, A, 2)
         + _line(128, 46, 128, 66, A, 2) + _txt(128, 78, "corner", M, 7)),
    {
        "op": "harris",
        "source": "shapes",
        "controls": [
            {"key": "window", "label": "Window radius", "type": "range",
             "min": 1, "max": 4, "step": 1, "value": 2},
            {"key": "k", "label": "k (sensitivity)", "type": "range",
             "min": 0.02, "max": 0.2, "step": 0.01, "value": 0.05},
            {"key": "threshold", "label": "Response threshold", "type": "range",
             "min": 0.01, "max": 0.6, "step": 0.01, "value": 0.12},
        ],
    },
    [
        "Shift a small window in any direction. On flat ground nothing changes; "
        "along an edge nothing changes; at a corner everything changes.",
        "The <strong>structure tensor</strong> summarises how the gradient "
        "behaves in a window. Two large eigenvalues means a corner.",
        "Harris computes <code class='mono-font'>det(M) &minus; k&middot;trace(M)&sup2;</code>, "
        "which is large when both eigenvalues are, without computing either.",
        "Corners are stable under rotation and moderate lighting change, which "
        "is what makes them useful as landmarks.",
    ],
    """
title: Harris Corners and Keypoints
intro: What makes a point in an image worth remembering, and the determinant that measures it.

## The question behind the detector

To match two photographs of the same scene, you need points you can recognise in
both. Which points are those?

The Harris insight is to ask what happens when you shift a small window slightly
in every direction.

**Flat region.** Shift it anywhere and the contents barely change. There is
nothing to lock onto: this window could be almost anywhere.

**Edge.** Shift it along the edge and nothing changes; shift it across and
everything does. It is locatable in one direction and free to slide in the other
&mdash; the aperture problem.

**Corner.** Shift it in any direction at all and the contents change. Its
position is pinned in both directions, and that is exactly what a landmark needs
to be.

## Making it arithmetic

The change under a small shift is captured by how the image gradient behaves
across the window. Collect the gradients into the **structure tensor**:

```
M  =  [ sum(Ix*Ix)   sum(Ix*Iy) ]
      [ sum(Ix*Iy)   sum(Iy*Iy) ]
```

Its two eigenvalues say how strongly the intensity varies along the two principal
directions:

| &lambda;1 | &lambda;2 | Meaning |
|---|---|---|
| small | small | flat |
| large | small | edge |
| large | large | **corner** |

Computing eigenvalues at every pixel would be slow, so Harris uses a combination
that behaves the same way without them:

```
R  =  det(M) - k * trace(M)^2
     =  (l1*l2) - k*(l1+l2)^2
```

`R` is large and positive only when both eigenvalues are large, strongly negative
at an edge, and near zero on flat ground. The determinant multiplies the
eigenvalues, so one small eigenvalue kills it; the trace term subtracts a penalty
that grows when the two are unbalanced.

`k` sets how strictly that balance is enforced &mdash; conventionally between
0.04 and 0.06. Drag it high in the visualisation and detections thin out to the
sharpest corners; drag it low and edges start to survive.

## Reading the visualisation

Highlighted pixels are those whose response clears the threshold.

Set the threshold low and whole edges light up, which is the failure mode `R` is
designed to avoid, appearing because the threshold is admitting weakly negative
and near-zero responses. Raise it and only the rectangle's four corners and the
triangle's points remain &mdash; the genuinely distinctive positions.

The window radius controls how much context each decision uses. A small window is
sensitive to noise and finds many tiny corners. A large one is stable but blurs
nearby corners into a single response and misses fine structure.

## What it is and is not invariant to

**Rotation: yes.** The eigenvalues of the structure tensor do not depend on the
coordinate frame, so a rotated corner is still a corner with the same response.
This is the property that makes Harris useful for matching.

**Illumination: mostly.** A constant brightness offset does not change gradients
at all. A contrast scaling multiplies them, which scales `R`, so a relative
threshold is needed rather than an absolute one.

**Scale: no.** This is the significant gap. A corner viewed from twice as far is
a smaller corner, and a fixed window either sees only part of it or swamps it
with context.

That gap is what **SIFT** addressed, by searching over scales as well as
positions and recording the scale at which each keypoint is most distinctive,
then describing the local gradient pattern so keypoints can be matched rather
than merely found. **ORB** does something similar much faster using FAST corners
and binary descriptors, which is why it turns up in real-time systems.

## Where corners are used

Panorama stitching, structure from motion, visual SLAM, camera calibration and
image registration all rest on finding the same physical points in several images
and solving for the transform between them. Detection is the first step;
[template matching](template_matching.html) is the alternative that does not
survive rotation.

## Where it goes wrong

**An absolute threshold.** Response scales with contrast, so a threshold tuned on
one image fails on a darker one. Threshold relative to the maximum, as this page
does.

**No non-maximum suppression.** A corner produces a cluster of high responses,
not one pixel.

**Expecting scale invariance.** If the camera distance varies, use a
scale-invariant detector.

**Corners on a blurred image.** Blur destroys the gradients the whole method
depends on, so denoise gently or not at all before detecting.
""",
    [
        {"q": "What distinguishes a corner from an edge in the structure tensor?",
         "options": ["A larger determinant only",
                     "Both eigenvalues are large, rather than one",
                     "The trace is zero",
                     "The gradients point the same way"],
         "answer": 1,
         "why": "An edge has one large eigenvalue and one small one, so the window can slide along it freely. A corner is pinned in both directions."},
        {"q": "Why does Harris compute det(M) - k*trace(M)^2 instead of the eigenvalues?",
         "options": ["It is more accurate",
                     "It behaves the same way - large only when both eigenvalues are large - without the cost of an eigendecomposition per pixel",
                     "Eigenvalues can be complex",
                     "It handles scale"],
         "answer": 1,
         "why": "The determinant is the product of the eigenvalues, so one small one kills it, and the trace term penalises imbalance. k sets how strictly."},
        {"q": "What is Harris NOT invariant to?",
         "options": ["Rotation", "Constant brightness offset", "Scale", "Translation"],
         "answer": 2,
         "why": "A corner viewed from twice the distance is a smaller corner, and a fixed window either sees part of it or swamps it. SIFT addressed this by searching over scales."},
    ],
)


# ---------------------------------------------------------------------------
# 18. Vision Transformer patches
# ---------------------------------------------------------------------------
topic(
    "vision_transformer_patches",
    "Vision Transformer Patches",
    "Architectures",
    "How an image becomes a sequence of tokens, and what that costs when the "
    "patches get smaller.",
    _svg(_grid(28, 22, 17, 6, 3, fill=S)
         + _txt(80, 78, "an image, as a sentence", M, 8)),
    {
        "op": "patches",
        "source": "colour",
        "controls": [
            {"key": "patch", "label": "Patch size", "type": "range",
             "min": 4, "max": 48, "step": 4, "value": 16},
        ],
    },
    [
        "A transformer takes a sequence of vectors. An image is a grid, so it "
        "has to be cut into patches and flattened.",
        "Each patch is flattened to <code class='mono-font'>P&sup2;&#215;3</code> "
        "numbers and projected to the model's width by a single linear layer.",
        "The patch grid <em>is</em> the resolution the model sees. There is no "
        "convolution underneath it.",
        "Attention cost grows with the square of the token count, so halving the "
        "patch size costs sixteen times the attention.",
    ],
    """
title: Vision Transformer Patches
intro: The one step that lets a language architecture read a photograph, and the quadratic cost hiding in it.

## Images are grids; transformers want sequences

A transformer operates on a sequence of vectors and has no built-in notion of
two dimensions. An image is a grid of pixels. Something has to convert one into
the other.

The obvious approach &mdash; one token per pixel &mdash; is impossible. A
224&#215;224 image is 50,176 pixels, and attention costs grow with the square of
the sequence length, so that is 2.5 billion pairwise interactions per layer.

The Vision Transformer's answer is almost aggressively simple: **cut the image
into square patches and treat each patch as a token.**

## The whole preprocessing step

Drag the patch control and watch the grid change. That is genuinely all that
happens to the image before it enters the model:

1. Cut into non-overlapping `P`&#215;`P` patches.
2. Flatten each patch to a vector of `P * P * 3` numbers.
3. Multiply by one learned matrix to get the model width.
4. Add a positional embedding, because otherwise the order is unknown.

At the default of 16 pixels on a 224-pixel image, that is a 14&#215;14 grid,
196 tokens, each starting as 768 raw numbers. The readout gives the same figures
for whatever patch size you choose.

Step 3 is the only learned part, and it is a linear projection with no
non-linearity. Equivalently, it is a convolution with kernel size `P` and stride
`P` &mdash; which is how it is usually implemented, and a nice reminder that the
distinction between "convolutional" and "not" is thinner than the naming
suggests.

## The quadratic cost

Halve the patch size and the token count quadruples, because the grid gains a
factor of two in each dimension. Attention cost goes with the square of the token
count, so it rises **sixteenfold**.

| Patch | Tokens (224px) | Attention cost |
|---|---|---|
| 32 | 49 | 1&#215; |
| 16 | 196 | 16&#215; |
| 8 | 784 | 256&#215; |
| 4 | 3,136 | 4,096&#215; |

That table is the central constraint on ViT design, and it explains a great deal
of what followed. Patch size is not a minor hyperparameter; it is the resolution
at which the model perceives anything, traded directly against compute.

## What is lost inside a patch

A 16&#215;16 patch is compressed to a single vector. Structure within it is not
attended to at all; whatever the projection preserves is what survives.

This is the ViT's real weakness at small scale. A convolutional network has
locality built in &mdash; nearby pixels are processed together by construction
&mdash; and this **inductive bias** matches how images actually work. A ViT has
none of it. Every relationship, including "these two patches are adjacent", must
be learned from data through the positional embeddings.

Which is why the original paper's headline finding was about data. On ImageNet
alone the ViT underperformed a ResNet; pre-trained on 300 million images it
overtook it. With enough data the model learns the structure that convolution
assumes, and gains flexibility convolution does not have.

Two responses followed. **DeiT** showed careful augmentation and distillation
could train a ViT on ImageNet alone. **Swin Transformer** reintroduced locality
by restricting attention to windows and merging patches hierarchically, which
gives back the pyramid a CNN has and makes dense prediction practical.

## Positional embeddings

Attention is permutation-invariant: shuffle the tokens and the output is
shuffled identically, with nothing else changed. Without positional information
a ViT literally cannot tell a photograph from a jigsaw of itself.

The fix is to add a learned vector per position. It is worth appreciating how
weak this is compared with convolution: the model is told "this is position 37"
and must learn from data that position 37 is next to 36 and above 23.

Changing the input resolution changes the number of positions, which is why ViTs
interpolate their positional embeddings when fine-tuned at a different size.

## Where it goes wrong

**Shrinking the patch to gain resolution.** The attention cost is quadratic in
tokens, so this gets expensive faster than expected.

**Training a plain ViT on a small dataset.** Without the inductive bias it needs
either far more data or the DeiT training recipe.

**Forgetting positional embeddings on a resized input.** The count must match,
and interpolation is required.

**Assuming patches must be square and non-overlapping.** Overlapping patches
help; several later architectures use them.
""",
    [
        {"q": "What does the projection step applied to each patch amount to?",
         "options": ["A small CNN",
                     "A single linear layer, equivalently a convolution with kernel and stride both equal to the patch size",
                     "An attention block",
                     "A pooling operation"],
         "answer": 1,
         "why": "It is the only learned part of the patching step and it has no non-linearity - which is why it is usually implemented as a strided convolution."},
        {"q": "Halving the patch size multiplies attention cost by roughly how much?",
         "options": ["2", "4", "16", "8"],
         "answer": 2,
         "why": "Token count quadruples because the grid doubles in each dimension, and attention is quadratic in token count, so cost rises sixteenfold."},
        {"q": "Why did the original ViT underperform a ResNet on ImageNet alone?",
         "options": ["It had fewer parameters",
                     "It has no built-in locality, so relationships convolution assumes must be learned from data",
                     "Attention cannot represent edges",
                     "The patches were too large"],
         "answer": 1,
         "why": "Pre-trained on 300 million images it overtook the ResNet. With enough data it learns the structure convolution assumes, and gains flexibility convolution lacks."},
    ],
)


# ---------------------------------------------------------------------------
# 19. Grad-CAM
# ---------------------------------------------------------------------------
topic(
    "grad_cam",
    "Grad-CAM",
    "Interpretability",
    "Weight each feature map by how much the score depends on it, add them up, "
    "and keep the positive part. That is the heatmap.",
    _svg(_box(12, 24, 30, 20, fill=S) + _txt(27, 38, "map", M, 7)
         + _box(12, 50, 30, 20, fill=S) + _txt(27, 64, "map", M, 7)
         + _txt(52, 48, "&#215;w", A, 9)
         + _box(70, 34, 34, 26, fill=S, stroke=A) + _txt(87, 50, "sum", A, 8)
         + _txt(112, 48, "ReLU", M, 8)
         + _txt(80, 82, "evidence for, not against", M, 7)),
    {
        "diagram": "gradcam",
        "controls": [
            {"key": "w1", "label": "Weight for map 1", "type": "range",
             "min": -1.5, "max": 2, "step": 0.1, "value": 1.2},
            {"key": "w2", "label": "Weight for map 2", "type": "range",
             "min": -1.5, "max": 2, "step": 0.1, "value": 0.6},
            {"key": "w3", "label": "Weight for map 3", "type": "range",
             "min": -1.5, "max": 2, "step": 0.1, "value": -0.8},
        ],
    },
    [
        "The weights are the gradient of the class score with respect to each "
        "feature map, averaged over its spatial positions.",
        "A weight says how much raising that map's activations would raise the "
        "score &mdash; how much the class depends on it.",
        "The final <code class='mono-font'>ReLU</code> is deliberate: it keeps "
        "evidence <em>for</em> the class and discards evidence against it.",
        "The heatmap is the size of the feature map, usually 7&#215;7, and is "
        "upsampled to the image. It is coarse by construction.",
    ],
    """
title: Grad-CAM
intro: A heatmap of which regions a network used, built from gradients it already computes.

## The question

A network says "cat". Which part of the image made it say that?

Grad-CAM answers with a heatmap, and it does so using quantities the network
produces anyway during backpropagation, which is why it works on any
convolutional architecture without retraining or modification.

## The recipe

Take the feature maps from the last convolutional layer &mdash; typically 512 or
2048 of them, each perhaps 7&#215;7. Then:

1. Compute the gradient of the class score with respect to each feature map.
2. Average each gradient over its spatial positions. That number is the map's
   **weight**.
3. Sum the feature maps, weighted by those numbers.
4. Apply a ReLU.
5. Upsample the result to the image size.

Steps 3 and 4 are what the visualisation shows. Three synthetic feature maps sit
on the left, each with its own weight slider, and the combined heatmap is on the
right. The maps are made up; the weighting arithmetic is exactly Grad-CAM's.

## What a weight means

The gradient of the score with respect to a feature map answers: if this map's
activations rose slightly, how much would the class score rise?

A **large positive weight** means the class depends heavily on that map, so
wherever it is active is evidence for the class.

A **negative weight** means the opposite &mdash; that feature argues *against*
this class. Set one of the sliders negative and watch what happens to the
heatmap: the region belonging to that map does not go dark, it simply stops
contributing, because of the ReLU.

## Why the ReLU is there

This is the step people skip and then misread the output.

Without the ReLU the heatmap would contain negative regions, meaning "this area
argued against the class". Grad-CAM discards them deliberately, because the
question being asked is *what supported this prediction* &mdash; and a
visualisation mixing support and opposition in one colour scale is very easy to
misread.

The consequence is that **Grad-CAM never shows you evidence against a class**.
Drag all three sliders negative: the heatmap is empty, not inverted. If you want
to know what argued against a prediction, this is the wrong tool, and running it
on the competing class is usually the practical answer.

## Its limits

**Resolution.** The heatmap has the spatial size of the last convolutional layer,
often 7&#215;7. Upsampling to 224&#215;224 produces a smooth blob, and that
smoothness is interpolation rather than evidence. Grad-CAM cannot tell you which
pixel mattered, only which seventh of the image.

**One layer.** It explains the last convolutional layer. Earlier layers see
different things, and the choice of layer changes the answer.

**Plausibility is not correctness.** A heatmap over the animal's face looks
convincing whether or not the model used the face. Grad-CAM shows what the
gradients say, and there is published work on saliency methods that produce
sensible-looking maps for randomly initialised networks &mdash; so a
reasonable-looking heatmap is not evidence the model is reasoning well.

**It does not survive every architecture unchanged.** Transformers have no final
convolutional layer, so attention rollout or a variant is used instead.

## Relatives

**CAM**, the predecessor, required the architecture to end in [global average
pooling](global_average_pooling.html) followed by one dense layer, and read the
weights straight from that layer. Grad-CAM's contribution was getting the same
weights from gradients instead, which removed the architectural requirement.

**Grad-CAM++** handles several instances of the same class better.
**Score-CAM** drops gradients entirely, measuring each map's importance by
occluding with it and seeing what the score does &mdash; slower, and immune to
gradient saturation.

## Where it goes wrong

**Reading the smooth blob as pixel-level evidence.** It is 7&#215;7,
interpolated.

**Explaining the wrong class.** Run it on the predicted class *and* on the class
you expected; the difference is usually the informative part.

**Treating it as proof.** A plausible heatmap is a hypothesis about the model,
not a verification of it.

**Choosing a layer without saying so.** The layer is a parameter, and the answer
depends on it.
""",
    [
        {"q": "Where does a feature map's weight come from?",
         "options": ["The dense layer's coefficients",
                     "The gradient of the class score with respect to that map, averaged over its spatial positions",
                     "The map's mean activation",
                     "A learned attention head"],
         "answer": 1,
         "why": "It answers how much raising that map's activations would raise the class score. Getting it from gradients is what freed Grad-CAM from CAM's architectural requirement."},
        {"q": "What does the final ReLU do?",
         "options": ["Normalises the heatmap",
                     "Discards evidence against the class, keeping only what supported it",
                     "Removes negative gradients before weighting",
                     "Upsamples the result"],
         "answer": 1,
         "why": "Drag all the weights negative and the heatmap is empty rather than inverted. Grad-CAM cannot show what argued against a prediction; run it on the competing class instead."},
        {"q": "Why is a Grad-CAM heatmap coarse?",
         "options": ["The gradients are approximated",
                     "It has the spatial size of the last convolutional layer, often 7x7, and is interpolated up",
                     "The ReLU removes detail",
                     "It averages over the batch"],
         "answer": 1,
         "why": "The smoothness of the blob is interpolation, not evidence. It can say which seventh of the image mattered, not which pixel."},
    ],
)


# ---------------------------------------------------------------------------
# 20. Instance vs semantic vs panoptic segmentation
# ---------------------------------------------------------------------------
topic(
    "segmentation_tasks",
    "Semantic, Instance and Panoptic Segmentation",
    "Segmentation",
    "Three tasks that all colour in pixels, and differ in exactly two "
    "questions: do objects get separate ids, and does the background count.",
    _svg(_box(14, 26, 40, 40, fill=S) + _txt(34, 78, "semantic", M, 7)
         + _box(60, 26, 40, 40, fill=S, stroke=A) + _txt(80, 78, "instance", M, 7)
         + _box(106, 26, 40, 40, fill=S, stroke=A) + _txt(126, 78, "panoptic", M, 7)),
    {
        "op": "segmentation",
        "source": "shapes",
        "controls": [
            {"key": "task", "label": "Task", "type": "select", "value": "semantic",
             "options": [{"value": "semantic", "label": "Semantic"},
                         {"value": "instance", "label": "Instance"},
                         {"value": "panoptic", "label": "Panoptic"}]},
        ],
    },
    [
        "<strong>Semantic</strong>: every pixel gets a class. Two adjacent cars "
        "are one region called 'car'.",
        "<strong>Instance</strong>: every object gets its own id. The background "
        "is not labelled at all.",
        "<strong>Panoptic</strong>: every pixel gets a class <em>and</em> objects "
        "keep separate ids. Both at once.",
        "The distinction is <strong>things</strong> (countable objects) against "
        "<strong>stuff</strong> (sky, road, grass), which has no instances.",
    ],
    """
title: Semantic, Instance and Panoptic Segmentation
intro: Three tasks, one scene, and the two questions that separate them.

## Two questions

Every segmentation task colours in pixels. What differs is the answer to two
questions:

1. Do two objects of the same class get **separate identities**?
2. Does the **background** get labelled?

Switch between the three settings above and watch the two discs and the
background. That is the entire taxonomy, visible in one scene.

| | Separate ids | Background labelled |
|---|---|---|
| Semantic | no | yes |
| Instance | yes | no |
| Panoptic | yes | yes |

## Things and stuff

The vocabulary that makes this coherent is **things** against **stuff**.

**Things** are countable: people, cars, dogs, bottles. Asking "how many" makes
sense, so instances make sense.

**Stuff** is uncountable: sky, road, grass, water. "How many skies" is not a
question. Stuff has extent but not instances.

Semantic segmentation treats everything as stuff &mdash; it only ever assigns
classes. Instance segmentation only handles things &mdash; it needs something to
count. Panoptic segmentation covers both, which is why it needed a name of its
own.

## Semantic

Every pixel gets a class label. Two overlapping cars are one connected region
labelled "car", and nothing in the output says there were two.

The standard architectures are fully convolutional: U-Net, DeepLab, SegFormer.
The metric is mean IoU per class. This is the right task when what matters is
area rather than count &mdash; how much of this field is diseased, which pixels
are road, what fraction of the scan is tumour.

## Instance

Every object gets its own mask and identity, and pixels belonging to no object
are left unlabelled.

Mask R-CNN is the canonical approach: detect boxes first, then predict a mask
inside each. That ordering has a consequence &mdash; masks can overlap, and a
pixel can belong to two instances, because nothing forces a single answer per
pixel.

This is the right task when counting matters: how many cells, how many people,
which pallet is which.

## Panoptic

Every pixel gets exactly one class, and pixels belonging to things also get an
instance id. Stuff regions get a class and no id.

The word means "everything visible", and the point of the 2018 paper that named
it was that the semantic and instance communities had been solving halves of the
same problem with different metrics and different architectures.

The constraint that makes it harder than running both is **exactly one label per
pixel**. Instance methods produce overlapping masks and semantic methods ignore
instances, so combining them requires resolving conflicts. Panoptic FPN and
Mask2Former do it in one model instead.

Its metric, **PQ**, multiplies a segmentation quality term (mean IoU over matched
segments) by a recognition quality term (an F1 over whether segments were matched
at all), which prevents a method from scoring well by getting the pixels roughly
right while missing objects entirely.

## Choosing

Ask what the output is for.

**Area, no counting** &mdash; semantic. Land cover, tumour extent, drivable
surface.

**Counting or tracking individuals** &mdash; instance. Cell counting, retail
stock, people in a queue.

**A complete scene description** &mdash; panoptic. Autonomous driving needs both
"where is the road" (stuff) and "which car is which" (things), and needs them
consistent.

## Where it goes wrong

**Using semantic segmentation to count.** Two touching objects are one region.
Post-hoc connected components will merge them.

**Expecting instance segmentation to label the background.** It does not; that
is not an oversight.

**Comparing mIoU with PQ.** Different metrics on different tasks.

**Ignoring the one-label constraint.** Merging separate semantic and instance
outputs into a panoptic one requires a conflict rule, and the rule affects the
score.
""",
    [
        {"q": "What is the difference between semantic and panoptic segmentation?",
         "options": ["Panoptic labels the background too",
                     "Panoptic also gives countable objects separate instance ids",
                     "Semantic uses boxes",
                     "Panoptic ignores stuff classes"],
         "answer": 1,
         "why": "Both label every pixel with a class. Only panoptic additionally distinguishes two adjacent cars as two objects rather than one 'car' region."},
        {"q": "Why does instance segmentation not label the background?",
         "options": ["It is too expensive",
                     "It handles only 'things' - countable objects - and stuff like sky has no instances to assign",
                     "The background has no texture",
                     "It is left to a separate model"],
         "answer": 1,
         "why": "Asking 'how many skies' is not a question. Instance methods need something countable, which is exactly why panoptic segmentation needed a name of its own."},
        {"q": "What makes panoptic harder than running a semantic and an instance model together?",
         "options": ["Two models are slower",
                     "Panoptic requires exactly one label per pixel, and instance masks can overlap",
                     "The metrics are incompatible",
                     "Stuff classes cannot be detected"],
         "answer": 1,
         "why": "Mask R-CNN style methods can assign a pixel to two instances. Producing one consistent labelling requires resolving those conflicts, which is what panoptic architectures do directly."},
    ],
)

CHECKS = {"computer_vision/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS}
