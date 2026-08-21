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

**Assuming bigger is better.** A 3&times;3 kernel sees a 3&times;3 region. To
see further you either use a larger kernel, which costs quadratically more
multiplications, or stack several small ones, which is what modern
architectures do and why [receptive field](feature_map_in_cnn.html) is a
concept worth having.
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

**Enlarging** asks for pixels that were never measured. A 4&times;4 image
stretched to 8&times;8 needs 64 values where 16 exist. The extra 48 have to
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
written as a 2&times;3 matrix:

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

CHECKS = {"computer_vision/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS}
