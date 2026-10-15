# -*- coding: utf-8 -*-
"""The seven named-architecture modules in the Computer Vision track.

These are the models a reader meets by name long before they meet by
mechanism: they read that a project "uses a ResNet-50 backbone" or "runs
YOLO", and the name carries no information until someone shows them what is
inside it.

Every number quoted in these articles is one the explorer on the page
recomputes from the architecture description, which is the only way to keep an
article and its visualisation from drifting apart. Where a figure comes from a
paper rather than from the page - a benchmark score, a training schedule - it
is attributed in the text.
"""

from arch_common import (entry, svg, box, txt, line, circle, path, stack, A, M, B, S)

TOPICS = []


# ---------------------------------------------------------------------------
# 1. Haar cascades
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "haar_cascade_detection",
    "computer_vision",
    "Haar Cascade Detection Models",
    "Classical detection",
    "Features, the integral image, and the cascade",
    "The face detector that ran in real time in 2001, on hardware slower than "
    "a modern doorbell. Drag a rectangle feature over an image and watch it "
    "respond.",
    svg(box(16, 20, 52, 50, fill=S)
        + box(22, 32, 40, 10, fill=A, sw=0)
        + box(22, 42, 40, 10, fill=M, sw=0)
        + txt(42, 80, "one feature", M, 7)
        + line(74, 45, 88, 45, A, 1.4)
        + stack(94, 26, 12, [38, 30, 22, 14])
        + txt(120, 80, "a cascade", M, 7)),
    {"widget": "haar"},
    [
        "A Haar feature is one number: the average brightness under the white "
        "rectangles minus the average under the black ones.",
        "The <code class='mono-font'>integral image</code> makes any rectangle "
        "sum four array lookups, whatever its size. That is the trick that "
        "made the whole method possible.",
        "The cascade orders classifiers cheapest first. The average window is "
        "rejected after about ten features, not 6,061.",
        "It is scale-invariant by scaling the <em>feature</em>, not the image "
        "&mdash; another consequence of the integral image.",
    ],
    r"""
title: Haar Cascade Detection Models
intro: Three ideas, stacked, that put face spotting on a 700 MHz laptop in 2001.

## The problem is the number of windows

Before deep learning, real-time face detection looked impossible. GPUs were
slow, and a webcam needed answers in 66 milliseconds. The Viola-Jones
detector, published in 2001, solved it with three ideas: cheap features
built from pixel sums, a cascade that rejects most windows after one or two
checks, and a boosting algorithm that selects the right features
automatically. This page walks through each of those ideas.

A finder has to answer one question. Is there a face here? &mdash;
at each spot and each scale in the image. For a 384&times;288 frame,
scanning with a 24&times;24 window at 11 scales gives roughly **180,000
windows**. At 15 frames per second that is 2.7 million classifications each
second, and all of them will be answered "no".

That framing shows the whole design. Viola and Jones did not build an
accurate face classifier and then speed it up. They built a system whose cost
is dominated by how quickly it can say *no*, and then made saying no almost
free.

## Idea one: features that are rectangle differences

A Haar-like feature takes two or more adjacent rectangles, sums the pixel
values inside each, and subtracts. The two-rectangle feature stacked
vertically is a flat edge finder. The three-rectangle feature is a
light band between two dark ones.

Drag the feature in the explorer onto the eye region and the response jumps,
because the eye band really is darker than the cheek below it. Drag it onto
the background and the two halves are nearly equal, so the response merges
toward zero. That is the entire feature. A subtraction &mdash; and it
is chosen for one reason: a rectangle sum can be made free.

There are a lot of these. In a 24&times;24 window, counting each spot and
each size of each prototype gives **more than 160,000 features**, which is
far more numbers than there are pixels in the window. The point isn't that
each one is good. It's that a few hundred of them, chosen well, are.

## Idea two: the integral image

The integral image is a table the same size as the image where each entry
holds the sum of all above and to the left of it:

```
ii(x, y) = sum of i(x', y') for all x' <= x and y' <= y
```

It's built in a single pass. Once it exists, the sum inside *any* axis-aligned
rectangle is:

```
sum = ii(D) - ii(B) - ii(C) + ii(A)
```

where A, B, C, D are the rectangle's four corners. Four lookups, three
math ops, and &mdash; this is the part that matters &mdash;
**the cost doesn't depend on the size of the rectangle**. A 4&times;4 patch
and a 200&times;200 patch cost just the same.

The explorer prints the four corner values and the subtraction for the
rectangle you've placed. Make the feature ten times larger and the four
numbers change. The amount of work doesn't.

Two consequences follow right away. Features of any size are affordable, so
the finder never has to resize the image to handle different face sizes
&mdash; it scales the *feature* instead. This Is a change to four
coords. And a two-rectangle feature costs six lookups rather than
hundreds of additions, which brings the per-window cost into a range where
testing a few hundred features is realistic.

## Idea three: AdaBoost picks the few hundred that matter

Of the 160,000 pick features, almost all are useless. AdaBoost is used as
a feature selector: each round, it picks the single feature and threshold that
best classifies the training set under the current sample weights, then
grows the weight on the examples that feature got wrong so the next round
has to attend to them.

Each selected feature turns a *weak classifier*. A threshold on one
rectangle difference, right maybe 60&ndash;70% of the time. The boosted sum of
a few hundred of them is a strong classifier.

The paper's first two features are worth knowing because they're so
readable. The first checks the eye region against the region just below
it, because the eyes are darker than the upper cheeks. The second checks the
eyes against the bridge of the nose between them, because the bridge is
lighter. Both are placed and sized by the training method, not by a person,
and both are just what a human would have picked.

## The cascade: spend nothing on the easy negatives

A single strong classifier of 200 features applied to 180,000 windows is 36
million feature tests per frame. Too slow. The insight is that
overwhelming majority of windows are trivially not faces &mdash; flat sky,
blank wall &mdash; and don't need 200 features to settle.

So the classifiers are arranged in stages, cheapest first, and a window is
discarded the instant any stage rejects it:

| Stage | Features | Roughly what it removes |
|---|---|---|
| 1 | 2 | about 50% of all windows |
| 2 | 10 | most of what stage 1 let through |
| 3&ndash;5 | 25&ndash;50 each | harder background |
| 6&ndash;38 | 50&ndash;200 each | face-like non-faces |

Each stage is tuned to a very high spotting rate &mdash; around 99.9% &mdash;
and a modest false-positive rate, around 50%. Chained, the spotting rates
times to a thing acceptable (0.999<sup>38</sup> is still about 96%) while
the false-positive rates times to a thing tiny (0.5<sup>38</sup>).

The final finder has **38 stages and 6,061 features**, and the *mean*
window is rejected after about ten feature tests. Move the stage slider
in the explorer and watch the surviving-window count fall off a cliff at the
first stage: that first drop is where the speed comes from, and it costs two
features.

## What it is still good for, and what it is not

Haar cascades aren't competitive with a CNN finder on fit. They're
sensitive to pose &mdash; the classic frontal-face model degrades sharply past
about 15&deg; of rotation &mdash; and to lighting, and they give
trait false positives on textures that happen to hold a
dark-light-dark band.

But they still ship, and for reasons that haven't gone away:

- **They run anywhere.** No GPU, no framework, a few hundred kilobytes of
  model. On a microcontroller or an old browser this is at times the only
  option.
- **They're deterministic and inspectable.** When one fires wrongly you can
  find the feature that did it.
- **They're a training-free dependency.** `cv2.CascadeClassifier` with a
  shipped XML file is three lines and no data collection.

```python
import cv2

detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = detector.detectMultiScale(
    gray,
    scaleFactor=1.1,     # shrink the search window 10% per octave step
    minNeighbors=5,      # how many overlapping hits before it counts
    minSize=(30, 30),
)
```

`scaleFactor` is the scale pyramid: 1.05 is slower and finds more, 1.3 is
faster and misses small faces. `minNeighbors` is the crude non-max
suppression &mdash; raise it to kill false positives, lower it if real faces
are being dropped. Those two knobs are most of what tuning a cascade consists
of.

## Two knobs and the failure each one causes

Almost each complaint about a cascade traces back to `scaleFactor` or
`minNeighbors`, and the two fail in opposite directions.

`scaleFactor` is the ratio between successive search scales. At 1.05 the
finder tries about twenty scales between the smallest and largest face it
looks for. At 1.4 it tries five. The faces that fall *between* two scales are
the ones that get missed. So A large factor is fast and makes the
trait "it saw him last frame and not this one" flicker. There's no
free lunch here: the cost is roughly proportional to the number of scales.

`minNeighbors` is the crude duplicate-removal step. A real face makes a
cluster of shared detections at neighbouring spots and scales, and a
spurious one often makes a single isolated hit. needing a few
shared detections before reporting one so filters most false
positives &mdash; and deletes any real face that only just cleared the cascade,
which is just the small, dark or partly-turned one you wanted. Setting it to
0 returns the raw hits and is worth doing once to see how many there are.

The third setting that matters and gets left at its default is `minSize`. A
finder searching for 20&times;20 faces in a 4K frame is scanning tens of
millions of windows for a thing that is never there. Setting a realistic
floor is often a larger speed-up than either of the other two.

## The line to draw from here

each idea here reappears later in a different costume. The cascade is the
ancestor of the two-stage finder: propose cheaply, verify expensively, which
is just what R-CNN and its descendants do. The integral image is the
ancestor of each "precompute a summed table so the query is O(1)" trick in
vision. And the rectangle features are, in an uncomfortably direct sense, a
hand-designed first convolutional layer &mdash; a small set of local
difference filters, applied all over, whose responses are thresholded and
mixed. The difference is that the next twenty years were spent learning
those filters rather than enumerating them.
## Questions people ask

<strong>Why does it fail on a face that is only slightly turned?</strong> Because the features encode a fixed brightness layout. A dark eye band above a lighter cheek, a light nose bridge between two darker eyes. Rotating the head moves those rectangles scaled to each other and the responses the cascade thresholds on collapse. Past roughly 15&deg; the frontal model degrades sharply. The usual answer is a second cascade trained on profiles rather than a fix to the first.

<strong>Can it find faces smaller than 24&times;24?</strong> No. The search grows the window from the trained size upward and never shrinks below it. 24&times;24 is the floor. Distant faces in a wide shot need the frame upsampled first. Doubling the image quadruples the window count.

<strong>Is the integral image an guess?</strong> No, it's exact. It's a cumulative sum. The four-corner formula recovers any rectangle's total just in int math. The costs are one extra table per frame and a wide enough int type. A 1080p frame of 8-bit pixels sums to about 5&times;10<sup>8</sup>. This Is why these tables are 32-bit or wider.

<strong>Why grayscale?</strong> The feature is a brightness difference. Colour carries nothing it can read. Converting once per frame also makes the integral image a third of the size.

<strong>Why does it fire on things that are obviously not faces?</strong> Each stage is tuned for about 99.9% spotting at roughly 50% false positives. The ensure lives in the product across 38 stages, not in any one of them. And a dark-light-dark band is just what the early features test. Bookshelves and railings truly do excite them. With 180,000 windows per frame even a tiny per-window rate leaves survivors. This Is what `minNeighbors` is for.

<strong>Should I train my own cascade?</strong> Rarely, now. `opencv_traincascade` wants thousands of positives and tens of thousands of negatives and can run for days. The result still inherits the pose sensitivity. If the object is rigid, near-frontal and inference has to be CPU-only it's viable. Or else fine-tuning a small CNN finder is less work and better.

## Recap in one screen

- One feature is a subtraction: the mean under the white rectangles minus the mean under the black ones.
- The integral image makes any rectangle sum four lookups even so of size. This Is why the finder scales the *feature* rather than the image.
- AdaBoost is used as a feature selector over more than 160,000 picks. The shipped finder keeps 6,061 of them across 38 stages.
- The cascade is where the speed lives. Stage one costs two features and drops about half of all windows. The mean window dies after about ten.
- It assumes a fixed brightness layout. It's a controlled-pose finder. All after it learned the filters instead of enumerating them.
""",
    [
        {"q": "Why does the integral image matter so much here?",
         "options": ["It compresses the image",
                     "It makes the sum inside any rectangle cost four lookups, "
                     "regardless of the rectangle's size",
                     "It removes noise before detection",
                     "It converts the image to greyscale"],
         "answer": 1,
         "why": "The sum inside a rectangle is ii(D) - ii(B) - ii(C) + ii(A). "
                "Four lookups, whether the rectangle is 4x4 or 200x200. That is "
                "what makes evaluating features at every scale affordable, and "
                "it is why the detector scales the feature rather than the image."},
        {"q": "What is the cascade actually optimising?",
         "options": ["Accuracy on faces",
                     "The cost of rejecting the overwhelming majority of "
                     "windows that contain no face",
                     "Memory usage",
                     "Robustness to rotation"],
         "answer": 1,
         "why": "Nearly every one of the ~180,000 windows in a frame is not a "
                "face. Ordering classifiers cheapest-first means the average "
                "window is discarded after about ten feature evaluations "
                "instead of all 6,061."},
        {"q": "A stage in the cascade is tuned to about 99.9% detection and "
              "about 50% false positives. Why is such a weak false-positive "
              "rate acceptable?",
         "options": ["Because faces are rare",
                     "Because the rates multiply down the chain: 0.5 to the "
                     "38th is negligible, while 0.999 to the 38th is still "
                     "about 96%",
                     "Because a later stage can undo an earlier rejection",
                     "Because false positives are removed by the integral image"],
         "answer": 1,
         "why": "A cascade multiplies both rates. Keeping each stage's "
                "detection rate extremely high is what protects the final "
                "recall, and the false-positive rate is allowed to be poor per "
                "stage because 38 of them compound."},
        {"q": "What does a Haar feature actually compute?",
         "options": ["A learned convolution",
                     "The difference between the average intensity under its "
                     "white rectangles and under its black ones",
                     "The gradient magnitude at a pixel",
                     "A histogram of oriented gradients"],
         "answer": 1,
         "why": "It is a rectangle difference and nothing more. AdaBoost "
                "chooses which of the 160,000-odd candidate positions, sizes "
                "and shapes are worth keeping, and a threshold on each becomes "
                "a weak classifier."},
    ],
    refs=[("Rapid Object Detection using a Boosted Cascade of Simple Features",
           "Viola & Jones, CVPR 2001", None),
          ("Robust Real-Time Face Detection",
           "Viola & Jones, IJCV 2004", None),
          ("Cascade Classifier", "OpenCV documentation",
           "https://docs.opencv.org/4.x/db/d28/tutorial_cascade_classifier.html")],
    description="Drag a Haar rectangle feature over a face, watch the integral "
                "image sum it in four lookups, and see a cascade discard 24,000 "
                "windows."))


# ---------------------------------------------------------------------------
# 2. VGG-16
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "vgg16_architecture",
    "computer_vision",
    "VGG-16",
    "Classification backbones",
    "The network, layer by layer",
    "Thirteen convolutions and three dense layers. The convolutions do 99% of "
    "the arithmetic and hold 11% of the parameters — open the layer "
    "table and see where each budget goes.",
    svg(stack(14, 24, 9, [42, 42, 34, 34, 26, 26, 26, 18, 18, 18], gap=2)
        + box(126, 30, 10, 30, fill=A, sw=0)
        + box(139, 30, 10, 30, fill=A, sw=0)
        + txt(60, 80, "13 conv", M, 7)
        + txt(134, 80, "3 fc", A, 7)),
    {"widget": "vgg16"},
    [
        "Every convolution is 3&times;3 with stride 1 and padding 1. Nothing "
        "in VGG changes the spatial size except the five max-pools.",
        "Two stacked 3&times;3 layers see the same 5&times;5 window as one "
        "5&times;5 layer, with 18C&sup2; parameters instead of 25C&sup2; and "
        "an extra non-linearity in between.",
        "138 M parameters, of which <strong>123 M are in the three dense "
        "layers</strong>. The first one alone is 102 M.",
        "It is still a common perceptual-loss and style-transfer backbone, "
        "because its features are simple and well understood &mdash; not "
        "because it is efficient.",
    ],
    r"""
title: VGG-16
intro: One kernel size, one stride, sixteen weighted layers. A param budget almost fully in the wrong place.

## The whole design, in one rule

VGG-16 is worth studying not because it is fast &mdash; it is not &mdash; but
because it proved that a simple, repeated structure can beat a complicated
one. Almost every later architecture borrows the idea of stacking small
filters instead of using large ones.

Before VGG, convolutional architectures were a grab bag of kernel sizes:
AlexNet opened with an 11&times;11 stride-4 convolution, followed by 5&times;5s
and then 3&times;3s. Simonyan and Zisserman asked what happens if you fix the
kernel at the smallest size that still has a notion of direction &mdash;
**3&times;3, stride 1, padding 1**. And get depth by stacking rather
than by widening.

That single rule makes the entire network. Spatial size never changes
inside a block, because padding 1 on a 3&times;3 kernel is just
size-preserving. It halves only at the five max-pools. Channels double at each
pool, from 64 to 512, and then stop.

| Block | Convolutions | Channels | Output at 224 |
|---|---|---|---|
| 1 | 2 | 64 | 112 &times; 112 |
| 2 | 2 | 128 | 56 &times; 56 |
| 3 | 3 | 256 | 28 &times; 28 |
| 4 | 3 | 512 | 14 &times; 14 |
| 5 | 3 | 512 | 7 &times; 7 |

Thirteen convolutions, five pools, then flatten 7&times;7&times;512 = 25,088
values into three fully-connected layers of 4096, 4096 and 1000.

## Why two 3x3s beat one 5x5

This is the arg the paper is really about, and it's worth doing in
numbers.

A single 5&times;5 convolution with C input and C output channels has
25C&sup2; params. Two stacked 3&times;3 convolutions have 9C&sup2; +
9C&sup2; = **18C&sup2;** &mdash; 28% fewer &mdash; and their receptive field
is the same: each output of the second layer depends on a 5&times;5 patch of
the input.

Three 3&times;3s reach 7&times;7 with 27C&sup2; params against 49C&sup2;,
a 45% saving. And the stack has two ReLUs inside it where the single large
kernel has none, so the same receptive field is now found by a more
expressive function rather than one linear map.

This is the arg that ended large kernels in vision for a decade. It's
also the arg that later got in part reversed &mdash; ConvNeXt and the
modern large-kernel networks reopened it. But on the terms VGG set:
depth of small kernels is the default, and any of it else needs a reason.

## Where the parameters actually are

Push the layer table in the explorer to the bottom and the numbers stop being
reasonable:

| Layer | Parameters | Share |
|---|---|---|
| All 13 convolutions | 14,714,688 | 10.6% |
| fc6 (25088 &rarr; 4096) | 102,764,544 | 74.3% |
| fc7 (4096 &rarr; 4096) | 16,781,312 | 12.1% |
| fc8 (4096 &rarr; 1000) | 4,097,000 | 3.0% |
| **Total** | **138,357,544** | |

**One layer is three quarters of the model.** fc6 takes the flattened
7&times;7&times;512 feature map and connects each one of its 25,088 values to
each of 4096 outputs. There's no weight sharing and no locality. It's a
dense mat with a hundred million entries, applied once per image.

Now flip to the math view. The convolutions do about 15.3 billion
times-builds up per image and the dense layers about 0.12 billion. So:

- the convolutions are **11% of the params and 99% of the find**;
- the dense layers are **89% of the params and 1% of the find**.

That inversion is the single most handy thing to take from this page. The
param count tells you about memory, download size and overfitting risk.
The MAC count tells you about latency and energy. They aren't the same
number, they aren't even linked here, and quoting one when you meant the
other is a routine source of confusion.

## What one 3x3 layer actually costs

Take `conv3-64` in block 1, at 224&times;224. Its kernel is 3&times;3, it reads
64 channels and writes 64:

```
parameters = 64 x 64 x 3 x 3 + 64 = 36,928
positions  = 224 x 224 = 50,176
MACs       = 36,864 x 50,176 = 1,849,688,064
```

One point eight billion times-builds up from thirty-seven thousand
numbers. The weights are reused at each spot. This Is the entire point of
a convolution and the reason the math and the storage are so far apart.

Now the same sum for fc6:

```
parameters = 25,088 x 4,096 + 4,096 = 102,764,544
positions  = 1
MACs       = 102,760,448
```

A hundred million params used just once each. Selecting any conv layer
in the explorer prints its own version of this math. Selecting a dense
one prints the other kind. Doing it once by hand is what makes the two budgets
stop feeling like the same number.

## What replaced the head, and why

Turn on **Swap the FC head for global mean pooling** in the explorer. The
param count falls from 138 M to about 15 M &mdash; a 9&times; reduction
&mdash; and nothing else about the network changes.

Global mean pooling merges each of the 512 final feature maps to its own
mean, giving 512 numbers with no params at all, and a single 512&rarr;1000
layer finishes the job. GoogLeNet did this in the same year VGG was published;
ResNet did it the year after. It has been standard ever since.

It buys three things beyond size. It drops the layer most prone to
overfitting. It makes the network accept any input detail, because the
pool doesn't care how large the map it's blending is &mdash; whereas fc6
demands just 25,088 inputs. This Is why the first VGG only accepts
224&times;224. And it forces each final feature map to match to a thing
class-relevant on its own. This Is what makes class activation maps work.

Move the input detail slider with the FC head on, and watch the flattened
size &mdash; and so fc6's param count &mdash; change with it. That
dependency is the reason detail was frozen.

## Reading the shape of a network from its table

The layer table is worth reading as a shape rather than a list, because the
same shape recurs in almost each convolutional network built since.

Follow two columns down it. The spatial size goes 224, 112, 56, 28, 14, 7
&mdash; halving five times. The channel count goes 64, 128, 256, 512, 512
&mdash; doubling four times and then stopping. Times them: the tensor at the
first block holds 64 &times; 112&sup2; = 802,816 values, and at the last
512 &times; 7&sup2; = 25,088. The form shrinks by a factor of 32 as
it goes.

That is the whole compression story of a classifier. The input is 150,528
numbers showing colour at spots. The output is 1,000 numbers showing
belief about categories. each block trades some spatial detail for some
semantic width, and the halve-and-double rule is the exchange rate.

The rule isn't any. Halving both spatial dims quarters the number
of spots, and doubling the width quadruples the per-spot cost of a
convolution, so the math per block stays roughly constant while the
info gets steadily more abstract. Move the detail slider and watch
the MAC column: the cost scales with the square of the input size, which is why
detail is the most effective single lever on inference latency, and why
anyone optimising a vision model reaches for it before they reach for a smaller
architecture.

## The two questions to ask of any architecture

VGG is the clearest place to learn a habit that pays off on each model after
it: read the param budget and the math budget as **separate
questions**, and ask which layers dominate each.

Params answer "how large is the file, how much GPU memory does it occupy,
and how much data will it take to fit". Times-builds up answer "how long
does one image take and how much energy does it cost". A layer can dominate one
and be invisible in the other, and VGG's fc6 is the extreme case: three
quarters of the model and under one per cent of the work.

The inversion runs the other way too. A 3&times;3 convolution over 64 channels
has 36,928 params &mdash; nothing &mdash; and applies each one of them at
112&times;112 spots, which is 462 million times-builds up for a layer
you wouldn't notice in a param table.

Once you've the habit, the optimisation advice stops being folklore. If the
model is too large to ship, look at the widest dense layers and the last
stages. If it's too slow, look at the input detail and the early stages.
Those are different problems with different fixes, and confusing them is why
people prune a network for weeks and find it runs at just the same speed.

## VGG's real legacy

As a classifier VGG is obsolete: ResNet-50 gets better ImageNet fit with
a fifth of the params and a quarter of the math. No one should train
one today.

It lives for a different reason. Because the architecture is so plain
&mdash; no residuals, no branches, no norming, just a stack of the same
convolutions &mdash; its mid activations are unusually well behaved,
and a **visual loss** found on VGG features is still the standard
choice in style transfer, super-detail and image generation. When a paper
says it optimises "VGG loss" or "LPIPS with a VGG backbone", this is the
network being used, often only up to `relu3_3` or `relu4_3`, with the
hundred-million-param head discarded fully.

```python
import torch
import torchvision

vgg = torchvision.models.vgg16(weights="IMAGENET1K_V1")

# The 13 convolutions and 5 pools, without the 123 M-parameter classifier.
features = vgg.features[:16].eval()          # up to relu3_3
for p in features.parameters():
    p.requires_grad_(False)

def perceptual_loss(x, y):
    return torch.nn.functional.l1_loss(features(x), features(y))
```

Two details matter in that snippet and both bite people. Slicing `.features`
rather than using the whole model is what drops the dense head, and freezing
the params is what keeps it a *loss* rather than a second network being
trained. And what you feed it must be normed with the ImageNet mean
and standard deviation the weights were trained with, or the features are
being read off a spread the network has never seen.
## Questions people ask

<strong>Why is the input frozen at 224&times;224?</strong> Because fc6 is a dense mat expecting just 25,088 inputs. This Is 7&times;7&times;512. And 7&times;7 is what 224 turns after five halvings. Feed it 256&times;256 and the flatten makes 8&times;8&times;512 = 32,768 values. This Doesn't fit the mat. Global mean pooling drops the constraint fully, which is why each architecture after VGG accepts any detail.

<strong>VGG-16 or VGG-19 &mdash; does the difference matter?</strong> Rarely. VGG-19 adds one convolution to each of the last three blocks and about 20 M params, for a few tenths of a point of ImageNet fit. For visual loss the 16-layer version is the conventional choice and the one most published numbers assume.

<strong>Which param count is right, 138 M or 134 M?</strong> Both get quoted. 138,357,544 includes the 1000-way fc8. Smaller figures often come from a model with the classifier removed or replaced. Check what a count includes before checking two of them.

<strong>Why does it use so much GPU memory for its size?</strong> Because activations, not weights, dominate training memory. The first block holds 64&times;224&times;224 values per image. 3.2 M numbers. And each one is kept for the backward pass, while the 102 M-param fc6 stores 4,096. That is why VGG batch sizes are small though ResNet-50 is deeper.

<strong>Is `relu3_3` or `relu4_3` the right layer for visual loss?</strong> Earlier layers reward matching texture and colour. Later ones reward matching structure and handle texture differences. Style transfer often takes a few at once, super-detail one of those two. There's no correct answer, only a choice about what you want preserved.

<strong>Should I fine-tune VGG for a new task?</strong> You can. It will work. You're paying 138 M params for fit ResNet-50 exceeds at 25.6 M. Reach for VGG when you in detail want its features. A loss, a published check. Not as a default backbone.

## Recap in one screen

- One rule makes the network: 3&times;3, stride 1, padding 1, with the spatial size changing only at the five max-pools.
- Two stacked 3&times;3s match a 5&times;5's receptive field for 18C&sup2; params against 25C&sup2;. Add a non-linearity in between.
- The convolutions are 11% of the params and 99% of the math. The dense head is 89% and 1%. Read the two budgets as separate questions.
- fc6 alone is 102 M params used once per image. Global mean pooling replaces it, cuts the model about 9&times;, and frees the input detail.
- Obsolete as a classifier, still standard as a visual-loss backbone. Sliced before the head, frozen, and fed ImageNet-normed input.
""",
    [
        {"q": "Two stacked 3x3 convolutions replace one 5x5. What do you gain?",
         "options": ["A larger receptive field",
                     "The same receptive field with 18C^2 parameters instead of "
                     "25C^2, and an extra non-linearity in between",
                     "Fewer multiply-accumulates",
                     "Translation invariance"],
         "answer": 1,
         "why": "The receptive field is identical - that is the point. What "
                "changes is 28% fewer parameters and a ReLU in the middle, so "
                "the same window is computed by a more expressive function."},
        {"q": "Where are VGG-16's 138 M parameters?",
         "options": ["Spread evenly across the 16 layers",
                     "Mostly in the 13 convolutions",
                     "89% in the three dense layers, with fc6 alone holding 102 M",
                     "Mostly in the max-pooling layers"],
         "answer": 2,
         "why": "fc6 connects the flattened 25,088-value feature map to 4096 "
                "outputs: 102.7 M parameters in one layer. The convolutions "
                "hold 14.7 M in total, about 11%."},
        {"q": "Which layers do most of the arithmetic?",
         "options": ["The dense layers, since they have most of the parameters",
                     "The convolutions - about 99% of the MACs, despite holding "
                     "11% of the parameters",
                     "The max-pools",
                     "It is split evenly"],
         "answer": 1,
         "why": "A convolution's weights are reused at every spatial position, "
                "so few parameters do enormous work. A dense layer uses each "
                "weight exactly once per image. Parameter count and compute "
                "cost are different budgets."},
        {"q": "Why can the original VGG-16 only accept 224x224 input?",
         "options": ["The convolutions require it",
                     "fc6 expects exactly 25,088 inputs, which is what "
                     "7x7x512 flattens to - a different input size gives a "
                     "different flattened length",
                     "The max-pools require it",
                     "ImageNet images are all that size"],
         "answer": 1,
         "why": "The convolutional tower handles any size. The dense head does "
                "not, because a fully-connected layer's weight matrix has a "
                "fixed input dimension. Replacing it with global average "
                "pooling removes the constraint entirely."},
    ],
    refs=[("Very Deep Convolutional Networks for Large-Scale Image Recognition",
           "Simonyan & Zisserman, ICLR 2015", "https://arxiv.org/abs/1409.1556"),
          ("torchvision.models.vgg16", "PyTorch documentation",
           "https://pytorch.org/vision/stable/models/generated/torchvision.models.vgg16.html")],
    description="Walk VGG-16 layer by layer and see why 89% of its 138 M "
                "parameters sit in three dense layers that do 1% of the work."))


# ---------------------------------------------------------------------------
# 3. InceptionNet
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "inception_architecture",
    "computer_vision",
    "InceptionNet",
    "Classification backbones",
    "The inception module, with and without its bottleneck",
    "Four convolutions run in parallel and their outputs are concatenated. "
    "Turn off the 1×1 bottleneck and watch the cost of one module more "
    "than double.",
    svg(box(66, 12, 28, 12, fill=S)
        + line(80, 24, 28, 38, B, 1.2) + line(80, 24, 60, 38, B, 1.2)
        + line(80, 24, 100, 38, B, 1.2) + line(80, 24, 132, 38, B, 1.2)
        + box(16, 38, 24, 12, fill=S) + box(48, 38, 24, 12, fill=S)
        + box(88, 38, 24, 12, fill=S) + box(120, 38, 24, 12, fill=S)
        + line(28, 50, 80, 64, B, 1.2) + line(60, 50, 80, 64, B, 1.2)
        + line(100, 50, 80, 64, B, 1.2) + line(132, 50, 80, 64, B, 1.2)
        + box(46, 64, 68, 12, fill="none", stroke=A)
        + txt(80, 73, "concat", A, 8)),
    {"widget": "inception"},
    [
        "Every branch keeps the map at the same spatial size. That is the only "
        "reason the four outputs can be concatenated along channels.",
        "A 1&times;1 convolution is a per-pixel linear map across channels. It "
        "changes the channel count and nothing else.",
        "Putting a 1&times;1 in front of the 5&times;5 branch of module 3a cuts "
        "that branch from 120 M to 12 M multiply-accumulates.",
        "GoogLeNet is <strong>6.8 M parameters</strong> against VGG-16's 138 M, "
        "and won ILSVRC 2014 while VGG came second.",
    ],
    r"""
title: InceptionNet
intro: Stop choosing a kernel size. Run a few, concatenate. Use 1x1 convolutions to make that affordable.

## The question the module answers

each convolutional layer forces a choice: 1&times;1, 3&times;3 or
5&times;5? The right answer depends on how large the thing you're looking for
is in that layer's units. This Varies by image, by class and by depth. VGG
answers it by fiat &mdash; always 3&times;3 &mdash; and gets the range of
scales from depth.

Inception refuses the question. Run 1&times;1, 3&times;3, 5&times;5 and a
pooling branch **in parallel on the same input**, and concatenate the results
along the channel axis. The next layer then has all the scales available and
learns which to weight.

This only works because each branch is padded to preserve spatial size. A
1&times;1 with no padding, a 3&times;3 with padding 1 and a 5&times;5 with
padding 2 all leave a 28&times;28 map as 28&times;28, so their outputs stack
cleanly. Concatenation along channels is or else hopeless: you can't
concatenate a 28&times;28 map with a 26&times;26 one.

## The naive version is unaffordable

Take module 3a, the first in GoogLeNet: 192 input channels at 28&times;28,
making 64 + 128 + 32 channels from the three convolutional branches plus
what the pool passes through.

Turn the bottleneck **off** in the explorer and read the branch costs:

| Branch | Multiply-accumulates |
|---|---|
| 1&times;1 &rarr; 64 | 9.6 M |
| 3&times;3 &rarr; 128, reading all 192 channels | 173.4 M |
| 5&times;5 &rarr; 32, reading all 192 channels | 120.4 M |
| **Total** | **303 M** |

Three hundred million times-builds up for **one module**, and there are
nine of them. Worse, the pooling branch passes its 192 input channels straight
through, so the output has 64 + 128 + 32 + 192 = 416 channels &mdash; more than
went in. Stack two of these and the third one is reading 416 channels, then
the fourth is reading even more. The channel count grows without bound and the
cost grows with the *square* of it.

## The 1x1 convolution is the fix

A 1&times;1 convolution has no spatial extent at all. At each pixel it takes
the vector of C input channels and applies a single learned mat to give
C' outputs. It's a per-pixel linear map across channels &mdash; a change of
basis in channel space, applied the same way all over. And its cost is
C &times; C' per pixel.

Put one in front of each costly branch and the math merges:

| Branch | Naive | With a reduction |
|---|---|---|
| 3&times;3 | 192&rarr;128 directly: 173.4 M | 192&rarr;96 then 96&rarr;128: 101.1 M |
| 5&times;5 | 192&rarr;32 directly: 120.4 M | 192&rarr;16 then 16&rarr;32: 12.4 M |
| pool | 192 passed through, 0 M | 192&rarr;32 projection: 4.8 M |

The 5&times;5 branch drops by a factor of ten. A 5&times;5 kernel over
16 channels is a twelfth of the work of the same kernel over 192. And the pool
branch now *shrinks* its channel count instead of growing it, so the module
outputs 256 channels rather than 416 and the next module has less to read.

Total: **128 M against 303 M**, and the output is smaller. Toggle the control
and watch both numbers move together.

## The whole network

The full GoogLeNet stacks nine of these modules with two mid pools,
after a conventional 7&times;7 and 3&times;3 stem. The layer table in the
explorer lists all nine with their real widths from table 1 of the paper.

Two things stand out. The widths aren't a pattern. Module 4d puts 288
channels in its 3&times;3 branch and 64 in its 5&times;5, while 4e puts 320
and 128 &mdash; because they were tuned rather than derived. And the whole
network comes to **6.8 million params** against VGG-16's 138 million, on
about 1.5 billion times-builds up against VGG's 15.5 billion. It won
ILSVRC 2014 classification. VGG came second.

The head is the other half of that story. GoogLeNet ends with global mean
pooling and one 1024&rarr;1000 layer, not with two 4096-wide dense layers. That
choice alone accounts for most of the 20&times; param gap.

The first also carried two **auxiliary classifiers** &mdash; extra softmax
heads hanging off the middle of the network during training, their losses
added at weight 0.3 &mdash; to push grad into the early layers of a network
too deep to train or else. They were removed at inference. Within a year
ResNet solved that problem properly with identity shortcuts, and later
Inception versions dropped the auxiliary heads. The paper's own follow-up
concluded they acted more as regularisers than as grad highways.

## What the family did next

- **Inception-v2/v3** factorised the 5&times;5 into two 3&times;3s, then went
  further and factorised an n&times;n into an n&times;1 followed by a
  1&times;n. It added batch norming and label smoothing. 
- **Inception-v4 and Inception-ResNet** added residual links, which
  sped up training a lot without changing the fit ceiling much
  &mdash; a handy data point about what residuals really buy.
- **Xception** took the factorisation to its limit: if a 1&times;1 handles
  cross-channel mixing and the spatial kernel handles space, do them
  fully apart. That is depthwise separable convolution, and it's the
  basis of MobileNet and of most fast architectures since.

```python
import torch
import torch.nn as nn

class InceptionModule(nn.Module):
    def __init__(self, cin, c1, r3, c3, r5, c5, pp):
        super().__init__()
        self.b1 = nn.Conv2d(cin, c1, 1)
        self.b2 = nn.Sequential(nn.Conv2d(cin, r3, 1), nn.ReLU(inplace=True),
                                nn.Conv2d(r3, c3, 3, padding=1))
        self.b3 = nn.Sequential(nn.Conv2d(cin, r5, 1), nn.ReLU(inplace=True),
                                nn.Conv2d(r5, c5, 5, padding=2))
        self.b4 = nn.Sequential(nn.MaxPool2d(3, stride=1, padding=1),
                                nn.Conv2d(cin, pp, 1))

    def forward(self, x):
        # Padding is chosen per branch so all four leave the map the same size.
        return torch.cat([self.b1(x), self.b2(x), self.b3(x), self.b4(x)], dim=1)

m = InceptionModule(192, 64, 96, 128, 16, 32, 32)   # module 3a
print(sum(p.numel() for p in m.parameters()))       # 163,696
```

Note the padding values: 0, 1 and 2 for kernels 1, 3 and 5. Get one of them
wrong and `torch.cat` raises a shape error on `dim=1` &mdash; which is the
architecture telling you that the branches have to agree spatially, and is
worth triggering once on purpose.

## What it costs to run four branches

There's a cost to the parallel structure that the times-build up count
doesn't show, and it's worth naming because it shows why inception-style
modules fell out of fashion despite being fast on paper.

Four branches means four separate convolution kernels, four separate memory
allocations for their outputs, and a concatenation that has to gather them.
On a GPU, a single large convolution saturates the hardware. Four small ones
launched in sequence each spend part of their time not doing math at all.
The measured latency of an inception module is always worse than its
MAC count predicts, and the gap widens as hardware gets faster, because the
fixed per-launch cost doesn't shrink.

This is the general lesson about speed metrics. Params, MACs and
latency are three different budgets, and an architecture can win on the first
two and lose on the third. Depthwise separable convolutions have the same
problem in a more extreme form: they cut MACs by roughly eight or nine times
and often deliver two or three times the speed, because they're
memory-bandwidth bound rather than math bound.

The hands-on rule that follows: **measure latency on the hardware you'll
deploy to**, and treat MAC counts as a rough guide rather than a guess.
Two networks with the same MAC counts can differ by a factor of three in
milliseconds.

## The idea to keep

The 1&times;1 convolution is the transferable part. It isn't a special case of
a convolution so much as a distinct tool: **it changes the channel count at a
cost linear in channels, without touching space**. Once you can do that
cheaply, costly ops become affordable by sandwiching them between a
map down and a map back up. ResNet's bottleneck block is just
that pattern. So is MobileNet's inverted residual. So Is the feed-forward block
of a transformer, and so is each "reduce, operate, expand" structure you'll
meet from here on.
## Questions people ask

<strong>Why does a 1&times;1 convolution do any of it at all?</strong> Because it isn't spatial. It's a learned mat applied to the channel vector at each pixel. With 192 inputs and 96 outputs it's a 192&times;96 change of basis performed the same way all over. It can discard, combine or duplicate channels. It only looks trivial if you picture convolution as a thing that happens in space.

<strong>Where do the per-branch channel counts come from?</strong> From tuning, not a formula. Table 1 of the paper lists them per module and they aren't a pattern. 4d puts 288 channels in its 3&times;3 branch and 64 in its 5&times;5. This is the part of Inception that didn't generalise. The reason later architectures preferred one repeating block with a width multiplier.

<strong>Is GoogLeNet the same thing as Inception-v1?</strong> Yes. GoogLeNet is the exact 22-layer ILSVRC 2014 entry. Inception is the module and the family. Inception-v3 is the version most people really load. It expects 299&times;299 input rather than 224.

<strong>Why did the auxiliary classifiers go away?</strong> They existed to push grad into the early layers of a network too deep to train or else. Batch norming and then residual links solved that properly. The paper's own follow-up concluded the auxiliary heads had acted as regularisers rather than grad highways. Nothing replaced them because nothing needed to.

<strong>If it has 20&times; fewer params than VGG, why is it not 20&times; faster?</strong> Because params aren't latency. Four branches mean four kernel launches, four output allocations and a gather. The fixed cost per launch doesn't shrink as hardware gets faster. So measured latency is always worse than the MAC count predicts. Depthwise separable convolutions have the same problem more severely.

<strong>Should I use an Inception model today?</strong> For new work, no. A ResNet or a modern fast network is easier to train and better supported. Inception-v3 still matters in one place, though. The Inception Score and FID are defined on its activations. It remains load-bearing infrastructure for generative-model test.

## Recap in one screen

- The module runs 1&times;1, 3&times;3, 5&times;5 and a pool branch in parallel and concatenates along channels. The next layer picks the scale.
- Concatenation needs each branch to preserve spatial size. This Is what the per-branch padding of 0, 1 and 2 is for.
- A 1&times;1 reduction in front of the costly branches cuts module 3a from 303 M to 128 M MACs *and* shrinks its output from 416 to 256 channels.
- The pool branch's map is what stops the channel count growing without bound as modules are stacked.
- GoogLeNet is 6.8 M params against VGG's 138 M, mostly because it ends in global mean pooling. The transferable idea is reduce, operate, expand.
""",
    [
        {"q": "Why must every branch of an inception module preserve the "
              "spatial size?",
         "options": ["To keep the receptive field constant",
                     "Because the outputs are concatenated along the channel "
                     "axis, which requires identical height and width",
                     "To avoid aliasing",
                     "Because the pooling branch has no parameters"],
         "answer": 1,
         "why": "Concatenation on dim=1 requires every other dimension to "
                "match. That is why the 1x1, 3x3 and 5x5 branches use padding "
                "0, 1 and 2 respectively."},
        {"q": "What does a 1x1 convolution actually do?",
         "options": ["Blurs the image",
                     "Applies a learned linear map across channels at each "
                     "pixel independently, changing the channel count and "
                     "nothing spatial",
                     "Downsamples by a factor of 1",
                     "Acts as an identity"],
         "answer": 1,
         "why": "At each pixel it multiplies the C-vector of channels by a "
                "C' x C matrix. That is why it can cut 192 channels to 16 for "
                "a twelfth of the cost of running the 5x5 on all 192."},
        {"q": "In the naive module the pooling branch passes its input "
              "channels straight through. Why is that a problem?",
         "options": ["Pooling loses information",
                     "The output has more channels than the input, so stacked "
                     "modules grow without bound and cost grows quadratically",
                     "It has no parameters to train",
                     "It breaks the concatenation"],
         "answer": 1,
         "why": "192 in, 64 + 128 + 32 + 192 = 416 out. The next module reads "
                "416, the one after that reads more still, and convolution "
                "cost is proportional to input channels times output channels. "
                "The 1x1 projection on the pool branch is what stops it."},
        {"q": "GoogLeNet has 6.8 M parameters to VGG-16's 138 M. What accounts "
              "for most of that gap?",
         "options": ["The inception modules are inherently tiny",
                     "GoogLeNet ends in global average pooling and one dense "
                     "layer, where VGG has two 4096-wide dense layers holding "
                     "119 M parameters",
                     "GoogLeNet is shallower",
                     "GoogLeNet uses fewer channels throughout"],
         "answer": 1,
         "why": "The nine inception modules hold about 5.9 M parameters. VGG's "
                "convolutional tower is 14.7 M - the same order. The 20x gap is "
                "almost entirely the classifier head."},
    ],
    refs=[("Going Deeper with Convolutions", "Szegedy et al., CVPR 2015",
           "https://arxiv.org/abs/1409.4842"),
          ("Rethinking the Inception Architecture for Computer Vision",
           "Szegedy, Vanhoucke, Ioffe, Shlens & Wojna, CVPR 2016",
           "https://arxiv.org/abs/1512.00567"),
          ("Xception: Deep Learning with Depthwise Separable Convolutions",
           "Chollet, CVPR 2017", "https://arxiv.org/abs/1610.02357")],
    description="Run the four inception branches in parallel, then switch off "
                "the 1x1 bottleneck and watch one module jump from 128 M to "
                "303 M MACs."))


# ---------------------------------------------------------------------------
# 4. ResNet
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "resnet_architecture",
    "computer_vision",
    "ResNet",
    "Classification backbones",
    "The family, built from one description",
    "ResNet-18, -34, -50, -101 and -152 are one architecture and a list of "
    "four numbers. Build any of them here and watch the published parameter "
    "count fall out.",
    svg(box(14, 30, 22, 30, fill=S)
        + box(44, 26, 22, 38, fill=S)
        + box(74, 22, 22, 46, fill=S)
        + box(104, 18, 22, 54, fill=S)
        + box(134, 38, 14, 14, fill=S)
        + path("M22 30 C22 8 60 8 60 26", stroke=A, sw=1.6)
        + path("M82 22 C82 4 120 4 120 18", stroke=A, sw=1.6)
        + txt(80, 84, "shortcuts over four stages", M, 7)),
    {"widget": "resnet"},
    [
        "A block computes <code class='mono-font'>y = F(x) + x</code>. The "
        "addition is the whole idea; everything else is bookkeeping around it.",
        "Below 50 layers the block is two 3&times;3 convolutions. At 50 and "
        "above it is 1&times;1 down, 3&times;3 at the narrow width, 1&times;1 "
        "back up &mdash; four times wider out than in.",
        "Each stage halves the map and doubles the width, which keeps the "
        "arithmetic per stage roughly level while the parameters quadruple.",
        "ResNet-50 is <strong>25.56 M parameters and about 4.1 GMACs</strong> "
        "at 224&times;224. The explorer computes both from the description.",
    ],
    r"""
title: ResNet
intro: One block type, four stage depths. The param counts everyone quotes fall straight out of the description.

## Not five architectures, one

ResNet-18, -34, -50, -101 and -152 are often presented as a table of five
models. They're better understood as a single design with two params: the
block type, and how many blocks go in each of four stages.

All else is fixed. The stem is a 7&times;7 stride-2 convolution to 64
channels followed by a 3&times;3 stride-2 max pool, which takes 224&times;224
down to 56&times;56 in two steps. Then four stages at widths 64, 128, 256, 512,
each halving the spatial size and doubling the width. Then global mean
pooling and one dense layer to the class count.

| Model | Blocks per stage | Block type | Parameters | MACs @ 224 |
|---|---|---|---|---|
| ResNet-18 | 2, 2, 2, 2 | basic | 11.69 M | 1.81 G |
| ResNet-34 | 3, 4, 6, 3 | basic | 21.80 M | 3.66 G |
| ResNet-50 | 3, 4, 6, 3 | bottleneck | 25.56 M | 4.09 G |
| ResNet-101 | 3, 4, 23, 3 | bottleneck | 44.55 M | 7.80 G |
| ResNet-152 | 3, 8, 36, 3 | bottleneck | 60.19 M | 11.51 G |

each figure in that table is found by the explorer from the description
above it, not typed in. Change the depth and watch them move. The point of
saying so is that if the math on this page agreed with the paper by
coincidence you'd have no way to tell.

Note the pair 34 and 50: **same block counts, different block type**. Going
from basic to bottleneck adds 16 weighted layers and only 3.8 M params,
because a bottleneck block does its 3&times;3 at a quarter of the width.

## The block, and why the addition is the point

A plain deep network finds `y = F(x)`. A residual block finds:

```
y = F(x) + x
```

`F` is two or three convolutions with norming and ReLU. The `+ x` is an
identity shortcut carrying the input around them unchanged.

The paper's motivation is a minus result, and it's worth stating properly
because it's often mis-stated. A 56-layer plain network had *higher training
error* than a 20-layer one. That isn't overfitting &mdash; overfitting would
show as lower training error and higher test error. It's a **degradation**
problem: the deeper network could in principle represent all the
shallower one does, by making the extra layers find the identity, and
optimisation wasn't finding that answer.

Residual links make the identity the default rather than a thing to be
found. If `F` outputs zero, the block is the identity just, and driving
a stack of weights to zero is a far easier thing for gradient descent to do
than driving them to what configuration happens to copy the input.

The grad arg follows from the same equation. Differentiating,
`dy/dx = dF/dx + 1`. The `+1` means the grad reaching `x` can never be
smaller than the grad at `y` by more than `dF/dx` allows &mdash; there's
always a path back with a deriv of just 1. Deep plain stacks vanish
because each layer times the grad by a thing often less than one,
and a hundred such times is zero. There's no such product along the
shortcut.

## When the shortcut cannot be the identity

`y = F(x) + x` needs `F(x)` and `x` to have the same shape. At the first
block of stages 2, 3 and 4 they don't: the stride is 2, so the spatial size
halves, and the width doubles.

Open stage 2 in the explorer and the shortcut is drawn dashed and labelled
**1&times;1 map**. That is a stride-2 1&times;1 convolution whose only
job is to make the shapes match. It has params, it's trained, and it's
the one place the "clean identity path" arg doesn't truly hold. There
is one per stage and they're a small fraction of the model &mdash; but if you
run a residual block yourself, this is the part that will be wrong.

The other setup detail people get wrong: **don't put a ReLU on the
shortcut path**, and add before the final activation, not after. The paper's
own follow-up on identity mappings tested the options and found that
any of it obstructing the shortcut. A ReLU, a scaling, a gate &mdash;
makes very deep networks harder to train, not easier.

## Where the budget goes

Look at the MACs-per-stage bars in the explorer. They're nearly level across
the four stages, while the param counts quadruple from stage to stage.

That is a direct consequence of the halve-and-double rule. Halving each spatial
dim quarters the number of spots. Doubling the width quadruples the
per-spot cost of a convolution (both input and output channels double). The
two cancel. Meanwhile the param count depends only on the channel counts,
so it goes up by four each time.

The hands-on reading:

- **Early stages are cheap to store and costly to run.** They're what you
  attack for latency &mdash; reducing input detail helps here as n&sup2;.
- **Late stages are costly to store and cheap to run.** They're what you
  attack for model size, and what you replace when fine-tuning on a small
  dataset.
- **A feature-pyramid finder taps all four**. This Is why stage outputs get
  their own names: C2, C3, C4, C5 at strides 4, 8, 16, 32.

## Why it is still the default backbone

ResNet-50 is a decade old and remains the first thing to try for a new vision
task, which is unusual and worth showing. Pretrained weights exist in each
framework. each spotting, segmentation and pose library accepts it. Its
stage strides are the 4/8/16/32 that FPN-style necks assume. It fine-tunes
without drama on small datasets. And its fit is close enough to modern
options that beating it's rarely where the win is.

The follow-up work is worth knowing by name. **ResNeXt** replaced the
bottleneck's 3&times;3 with a grouped convolution, trading width for
"cardinality" at equal cost. **Wide ResNet** showed that at fixed budget, wider
and shallower often beats narrow and deeper. **ResNet-D** and the "bag of
tricks" papers found a further 1&ndash;2% ImageNet fit from changes that
cost almost nothing: a three-convolution stem instead of the 7&times;7, and
moving the stride from the 1&times;1 to the 3&times;3 inside the downsampling
block, which stops the 1&times;1 from discarding three quarters of its input
pixels. That last one is a genuine bug in the first, quietly fixed
all over.

## The stage names you will meet everywhere

The four stages have standard names, and knowing them saves a lot of confusion
when reading spotting and segmentation code.

The output of stage *i* is called **C*i***, at stride 2<sup>i</sup>: C2 at
stride 4, C3 at 8, C4 at 16, C5 at 32. A feature pyramid built on top of them
names its own levels **P2** to **P5** or **P7**. When a config file says
`out_indices=(0, 1, 2, 3)` or `returned_layers=[1, 2, 3, 4]`, it's asking the
backbone to hand back those four tensors instead of a single class vector.

The strides are the part that has hardened into a rule. A spotting neck,
a segmentation decoder and an anchor gen all assume 4/8/16/32, which is
why swapping a backbone for one with a different downsampling schedule often
breaks more than it should. It's also why `dilated` or `atrous` variants
exist: replacing stage 4's stride with a dilation keeps the map at stride 16
while preserving the receptive field, which segmentation wants and
classification doesn't care about.

```python
import torch.nn as nn

class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, cin, width, stride=1):
        super().__init__()
        cout = width * self.expansion
        self.conv1 = nn.Conv2d(cin, width, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(width)
        # Stride on the 3x3, not the 1x1: the ResNet-D fix.
        self.conv2 = nn.Conv2d(width, width, 3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(width)
        self.conv3 = nn.Conv2d(width, cout, 1, bias=False)
        self.bn3 = nn.BatchNorm2d(cout)
        self.relu = nn.ReLU(inplace=True)

        self.down = None
        if stride != 1 or cin != cout:
            self.down = nn.Sequential(
                nn.Conv2d(cin, cout, 1, stride=stride, bias=False),
                nn.BatchNorm2d(cout))

    def forward(self, x):
        identity = x if self.down is None else self.down(x)
        out = self.relu(self.bn1(self.conv1(x)))
        out = self.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        return self.relu(out + identity)     # add first, then activate
```

each convolution is `bias=False` because the batch norm right away after has
its own shift, and two back to back additive constants is one redundant
param per channel. Times that by the whole network and it's where the
"25.50 M or 25.56 M?" discrepancy in param counts often comes from: the
BN params are 53,000 of the total, and whether a count includes them
depends on the tool.
## Questions people ask

<strong>Is the shortcut always the identity?</strong> No. This is the most common misreading. At the first block of stages 2, 3 and 4 the stride is 2 and the width doubles. The shapes can't match and a trained 1&times;1 map carries the shortcut instead. Those maps are the one place the clean-identity arg doesn't truly hold.

<strong>Why `bias=False` on each convolution?</strong> Because the batch norm right away after has its own per-channel shift. A bias would be a second additive constant with no extra expressive power. It also shows part of why published counts disagree: BN's weights and shifts are about 53,000 params in ResNet-50. Whether a tool counts them varies.

<strong>Does the degradation result mean deeper is worse?</strong> It means deeper *plain* stacks were harder to optimise, not smaller in room. The 56-layer network had higher **training** error than the 20-layer one. This Rules out overfitting. Residuals add no room. They make a answer the network could already represent reachable by gradient descent.

<strong>Where does the ReLU go scaled to the addition?</strong> Add first, then activate. The identity-mappings follow-up tested the options and found that any of it sitting on the shortcut path. A ReLU, a scaling, a gate. Makes very deep networks harder to train. Pre-activation sorting is the variant that helps past 200 layers.

<strong>Why is ResNet-50 still the default backbone?</strong> Pretrained weights in each framework, stage strides of 4/8/16/32 that spotting necks and segmentation decoders assume, undramatic fine-tuning on small datasets. Fit close enough to modern options that beating it's rarely where a project's win really is.

<strong>What is the cheapest fit I am leaving on the table?</strong> The bag-of-tricks changes. A three-convolution stem instead of the 7&times;7. Moving the downsampling stride from the 1&times;1 to the 3&times;3 so the 1&times;1 stops discarding three quarters of its input pixels. That second one is a genuine bug in the first, worth 1&ndash;2% ImageNet fit for almost nothing. Shipped in most libraries as the "D" variant.

## Recap in one screen

- One design with two knobs. Block type and blocks per stage. The five famous models are points in that space, not five architectures.
- `y = F(x) + x` makes the identity the default. Differentiating gives `dF/dx + 1`. There's always a path back with deriv just 1.
- Widths 64/128/256/512 with the spatial size halving each time keeps MACs roughly level per stage while params quadruple.
- Early stages are cheap to store and costly to run. Late stages the reverse. That tells you which end to attack for latency and which for size.
- The stage outputs C2&ndash;C5 at strides 4/8/16/32 are a rule the whole spotting ecosystem is built on.
""",
    [
        {"q": "The paper's motivating observation was that a 56-layer plain "
              "network had higher TRAINING error than a 20-layer one. What "
              "does that rule out?",
         "options": ["Vanishing gradients", "Overfitting",
                     "A learning rate that was too high", "Insufficient data"],
         "answer": 1,
         "why": "Overfitting means lower training error and higher test error. "
                "Higher training error with more capacity is a degradation "
                "problem: the deeper network can represent the shallower one "
                "exactly, and optimisation was not finding it."},
        {"q": "Why does y = F(x) + x help the gradient?",
         "options": ["It normalises the activations",
                     "Differentiating gives dF/dx + 1, so there is always a "
                     "path backwards with derivative exactly 1",
                     "It reduces the number of parameters",
                     "It makes the loss convex"],
         "answer": 1,
         "why": "A plain stack multiplies the gradient by each layer's "
                "Jacobian, and a hundred factors below 1 is zero. The additive "
                "shortcut contributes a term of exactly 1 that no depth can "
                "shrink."},
        {"q": "When is the shortcut a 1x1 convolution rather than a plain "
              "identity?",
         "options": ["In every block",
                     "At the first block of a stage, where the stride is 2 or "
                     "the channel count changes, so the shapes would not "
                     "otherwise match",
                     "Only in ResNet-50 and above",
                     "Only during training"],
         "answer": 1,
         "why": "An addition needs matching shapes. Everywhere else in a stage "
                "the shortcut is a genuine identity with no parameters at all."},
        {"q": "ResNet-34 and ResNet-50 have the same block counts (3, 4, 6, 3). "
              "Why is 50 only 3.8 M parameters larger despite 16 more weighted "
              "layers?",
         "options": ["It uses fewer channels",
                     "A bottleneck block runs its 3x3 at a quarter of the "
                     "block's output width, so the expensive convolution is "
                     "much narrower",
                     "It shares weights between stages",
                     "It has no dense layer"],
         "answer": 1,
         "why": "The bottleneck projects down with a 1x1, does the 3x3 at that "
                "narrow width, then projects back up 4x. The 3x3 is the "
                "expensive layer and it never sees the full width."},
    ],
    refs=[("Deep Residual Learning for Image Recognition",
           "He, Zhang, Ren & Sun, CVPR 2016", "https://arxiv.org/abs/1512.03385"),
          ("Identity Mappings in Deep Residual Networks",
           "He, Zhang, Ren & Sun, ECCV 2016", "https://arxiv.org/abs/1603.05027"),
          ("Bag of Tricks for Image Classification with Convolutional Neural Networks",
           "He et al., CVPR 2019", "https://arxiv.org/abs/1812.01187")],
    description="Build ResNet-18 through -152 from one description and watch "
                "25.56 M parameters and 4.1 GMACs fall out of the block counts."))


# ---------------------------------------------------------------------------
# 5. U-Net
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "unet_architecture",
    "computer_vision",
    "U-Net",
    "Segmentation",
    "The U, level by level",
    "Turn the skip connections off and watch the parameter count fall and the "
    "argument for them appear. 572 in, 388 out, and every crop computed.",
    svg(box(20, 18, 26, 12, fill=S) + box(28, 34, 18, 10, fill=S)
        + box(34, 48, 12, 9, fill=S)
        + box(114, 18, 26, 12, fill=S) + box(114, 34, 18, 10, fill=S)
        + box(114, 48, 12, 9, fill=S)
        + line(48, 24, 112, 24, A, 1.2, "3 2")
        + line(48, 39, 112, 39, A, 1.2, "3 2")
        + line(48, 52, 112, 52, A, 1.2, "3 2")
        + box(62, 62, 36, 10, fill="none", stroke=A)
        + txt(80, 84, "skips carry the resolution", M, 7)),
    {"widget": "unet"},
    [
        "The encoder learns <em>what</em> is in the tile and destroys "
        "<em>where</em>. The skips are the only thing that still knows where.",
        "The original uses unpadded convolutions, so 572&times;572 in gives "
        "388&times;388 out and every skip has to be cropped.",
        "31.03 M parameters at the paper's settings &mdash; and the widest "
        "layer, at the bottom of the U, holds a fifth of them.",
        "It won the 2015 ISBI cell-tracking challenge trained on "
        "<strong>30 images</strong>. Heavy elastic augmentation, not scale.",
    ],
    r"""
title: U-Net
intro: An encoder that learns what is in the image, a decoder that puts it back where it was. Four wires between them doing most of the work.

## Segmentation is classification with an address

A classifier answers one question per image. A segmentation network answers one
per pixel: for a 512&times;512 input it must give 262,144 labelled outputs,
each of which needs both *semantic* info (this is cell wall, not
background) and *spatial* info (this exact pixel, not the one next to
it).

Those two needs fight. Semantics needs a large receptive field, which
means pooling, which destroys spatial precision. Precision needs full
detail, which means no pooling, which starves the receptive field. each
segmentation architecture is a way of having both, and U-Net's is the most
direct: get the semantics by pooling all the way down, then get the precision
back by wiring the pre-pooling activations forward.

## The contracting path

Each level is two 3&times;3 convolutions with ReLU, then a 2&times;2 max pool
with stride 2. Channels double at each level: 64, 128, 256, 512, and 1024 at
the bottom.

Follow the level table in the explorer. At the paper's settings, a
572&times;572 tile turns 568&times;568 after two unpadded convolutions, then
284&times;284 after pooling, then 280, then 140, and so on down to 28&times;28
with 1024 channels. Each pooling step quadruples the receptive field of
all after it, which is how a network of 3&times;3 kernels ends up seeing
a large enough zone to know what it's looking at.

The widest layer is at the bottom. Read its param count in the table: at
base 64 it holds around 6 M of the 31 M total, in one place, at the smallest
spatial size. This is the same pattern as ResNet's fourth stage &mdash; deep
and narrow spatially, so wide channels are affordable in find though
they're costly in memory.

## The expanding path, and the crop

Each decoder level does a 2&times;2 up-convolution &mdash; a transposed
convolution that doubles the spatial size and halves the channels &mdash; then
concatenates the matching encoder activation, then two more 3&times;3
convolutions.

The concatenation is the entire point of the architecture. The upsampled tensor
carries 512 channels of semantic summary found from a 68&times;68 view. The
skip carries 512 channels of detail found at 136&times;136, before that view
was thrown away. Concatenating gives these convolutions both, and lets
them learn how to combine them.

Turn **Skip links** off in the explorer. The param count drops
&mdash; the decoder convolutions now read half as many input channels &mdash;
and that is the entire gain. What you lose is stated in the note that
appears: the finest spatial detail available to the decoder is now what
survived four rounds of pooling, a 28&times;28 grid for a 572&times;572 input.
Boundaries come back rounded and blobby, and no amount of decoder room
fixes it, because the info is *gone*, not hidden.

## Valid convolutions, and why the output is smaller

Switch the padding control between **valid** and **same** and watch the output
size change.

The first uses unpadded ("valid") convolutions, so each 3&times;3 eats one
pixel from each border. Over the whole network that adds up: 572&times;572 in,
**388&times;388 out**. The skips so don't line up with the upsampled
tensors either, and each has to be centre-cropped. By 8, 32, 80 and 176
pixels at the four levels, as the table shows.

That looks like an annoyance and is really a deliberate ensure. each
output pixel is found from a zone that was fully present in the
input. There are no border pixels whose context was invented by zero-padding.
For a network run on tiles of a much larger microscopy image, that matters: the
paper's "share-tile" strategy feeds shared tiles and keeps only the
valid central output of each. So A large image is segmented smoothly with no
edge artefacts at the tile joins.

Almost each setup since uses `padding=1` instead, so input and output
are the same size and no cropping is needed. It's simpler and often fine.
The cost is that the outermost pixels are predicted from partly-fabricated
context, which shows up as a thin unreliable border &mdash; often skipped,
at times the source of a bug someone spends a day on.

## Trained on thirty images

U-Net won the 2015 ISBI cell tracking challenge with a training set of **30
images**. That is that made it famous, and it wasn't reached by
architecture alone.

The other half was boost, in detail **elastic deformation**: random
smooth warps of the image and its mask. This Is a realistic model of how
biological tissue really varies. Shift, rotation and flip boost
make images that look like other images from the same microscope. Elastic
deformation makes images that look like other *specimens*. For a domain
with thirty labelled examples, that difference is all.

There's a third piece worth knowing: a **weighted cross-entropy loss** with a
weight map found per image that heavily upweights the narrow gaps between
touching cells. Without it a network trained on this data merges adjacent cells
into one blob, because getting the thin separating line wrong costs almost
nothing in unweighted pixel fit. This is the general lesson: with a class
imbalance of a few thousand to one, the loss has to be told what matters, and
per-pixel fit won't tell it.

```python
import torch
import torch.nn as nn

def block(cin, cout):
    return nn.Sequential(
        nn.Conv2d(cin, cout, 3, padding=1), nn.BatchNorm2d(cout), nn.ReLU(inplace=True),
        nn.Conv2d(cout, cout, 3, padding=1), nn.BatchNorm2d(cout), nn.ReLU(inplace=True))

class UNet(nn.Module):
    def __init__(self, cin=3, classes=2, base=64, depth=4):
        super().__init__()
        chans = [base * 2 ** i for i in range(depth + 1)]
        self.downs = nn.ModuleList()
        for c in chans[:-1]:
            self.downs.append(block(cin, c)); cin = c
        self.bottom = block(chans[-2], chans[-1])
        self.ups = nn.ModuleList()
        self.convs = nn.ModuleList()
        for c in reversed(chans[:-1]):
            self.ups.append(nn.ConvTranspose2d(c * 2, c, 2, stride=2))
            self.convs.append(block(c * 2, c))     # c from the skip + c upsampled
        self.head = nn.Conv2d(base, classes, 1)
        self.pool = nn.MaxPool2d(2)

    def forward(self, x):
        skips = []
        for d in self.downs:
            x = d(x); skips.append(x); x = self.pool(x)
        x = self.bottom(x)
        for up, conv, skip in zip(self.ups, self.convs, reversed(skips)):
            x = up(x)
            x = conv(torch.cat([skip, x], dim=1))   # the skip, concatenated
        return self.head(x)
```

The line to stare at is `block(c * 2, c)` in the decoder. That `c * 2` is the
skip's channels plus the upsampled tensor's channels, and it's what the
explorer's "decoder input" column is reporting. Drop the concatenation and it
turns `block(c, c)` &mdash; which is why turning the skips off saves
params.

## Choosing the depth

The **Levels** control is the one with a real trade behind it, and the level
table is where to read it.

Each level doubles the receptive field of all below it and quarters the
spatial size. Too few levels and the deepest layer has never seen a
zone large enough to spot a structure by its context &mdash; it
will segment texture rather than objects. Too many and the bottom of the U is
a handful of pixels holding a thousand channels. This Is a lot of params
showing very little, and the decoder has more upsampling to invent.

The rule of thumb that comes out of it: the bottom of the U should be roughly
the size of the largest structure you need to reason about, in units of the
bottom's own stride. For 512&times;512 tiles of cell imagery, four levels puts
the bottom at 32&times;32 with a receptive field of about 140 pixels &mdash;
comfortably larger than a cell, comfortably smaller than the tile.

Watch what happens at the extremes in the explorer. Drop to two levels with a
572-pixel tile and the widest layer is only 256 channels. The param count
falls by most of the model. Push to five with a small tile and the valid-
convolution math runs out fully. This The explorer reports rather
than silently making a nonsense number. The tile size has to be
chosen so each pooling step cuts evenly, and that constraint is why the
paper's input is the odd-looking 572 rather than 512.

## What came after

**Focus U-Net** puts a gate on each skip so the decoder can suppress
irrelevant regions the encoder passed forward. **U-Net++** replaces the four
direct skips with a dense nest of mid convolutions, on the arg
that the encoder and decoder features at the same level are semantically
mismatched. **nnU-Net** did a thing more notable: it left the
architecture alone and automated all around it &mdash;
prep, patch size, batch size, boost, postprocessing &mdash; and
beat specialised architectures across dozens of medical benchmarks. That result
is worth sitting with. Ten years on, the strongest arg in the area is
still that a plain U-Net, configured well, is hard to beat.
## Questions people ask

<strong>Concatenate the skip, or add it?</strong> Concatenate, in the first. Adding forces the encoder's detail and the decoder's semantics into the same channels. These convolution can't tell them apart. Concatenating keeps them separate and lets it weigh them. Addition is cheaper and appears in ResNet-style decoders. But It's a different architecture rather than an setup shortcut.

<strong>Why 572&times;572 and not 512?</strong> Because unpadded convolutions shrink the map and each pooling step still has to divide evenly. 572 is chosen so the math lives four levels down and back. With `padding=1` the constraint relaxes to "divisible by 2<sup>levels</sup>". This Is why modern setups use round numbers.

<strong>Valid or same padding?</strong> Same (`padding=1`) unless you're tiling a larger image. Valid convolutions ensure each output pixel had genuine context. This Is what makes the share-tile strategy smooth. Same padding needs no cropping and costs you a thin border predicted partly from zeros.

<strong>Transposed convolution or upsample-then-convolve?</strong> Either works. Transposed convolutions can give checkerboard artefacts when the kernel size isn't divisible by the stride. Bilinear upsampling followed by a 3&times;3 avoids that and carries fewer params. This Is why most current setups choose it.

<strong>Why does my model merge touching objects?</strong> Because an unweighted per-pixel loss barely notices the thin line between them. A few hundred pixels out of a quarter of a million. The paper's answer was a per-image weight map upweighting just those gaps. The modern answers are Dice or focal loss, or predicting the boundary as its own class.

<strong>Does it really only need thirty images?</strong> The result is real. Not from the architecture alone. Elastic deformation is what made it work. A smooth random warp of tissue makes a thing that looks like a different *specimen*. Here Shift and flip only give another photo of the same one. With weak boost, thirty images isn't enough.

## Recap in one screen

- Segmentation needs semantics. This Wants pooling. Precision, which doesn't. U-Net gets both by pooling all the way down and wiring the pre-pooling activations forward.
- Each encoder level is two 3&times;3s then a 2&times;2 pool with channels doubling. Each decoder level up-converts, concatenates the skip, and convolves twice.
- The skips *are* the architecture. Without them the finest detail the decoder can see is what survived four poolings. A 28&times;28 grid for a 572&times;572 tile. And no decoder room recovers it.
- Choose depth so the bottom of the U is roughly the size of the largest structure you must reason about, measured in the bottom's own stride.
- nnU-Net is the result to note: configured well, the plain architecture is still hard to beat.
""",
    [
        {"q": "What do the skip connections carry that the bottom of the U "
              "cannot?",
         "options": ["More channels",
                     "Spatial precision - the activations at full resolution, "
                     "before pooling discarded where things were",
                     "The class labels",
                     "A larger receptive field"],
         "answer": 1,
         "why": "Pooling builds semantics by throwing away location. The "
                "bottom of the U knows what is in the tile and has lost where. "
                "The skip is the only path that still holds the boundary at "
                "full resolution."},
        {"q": "Why does the original U-Net output 388x388 for a 572x572 input?",
         "options": ["It crops the output deliberately",
                     "Its convolutions are unpadded, so every 3x3 removes one "
                     "pixel from each border and the losses accumulate",
                     "The pooling is not exactly by 2",
                     "The skips are cropped"],
         "answer": 1,
         "why": "Valid convolutions shrink the map. The benefit is that every "
                "output pixel is computed from context that was really present "
                "in the input, with no invented zero padding - which is what "
                "makes the overlap-tile strategy seamless."},
        {"q": "Turning the skip connections off reduces the parameter count. "
              "Why is that a bad trade?",
         "options": ["It makes training slower",
                     "The decoder's finest available detail becomes whatever "
                     "survived the pooling, so boundaries cannot be recovered "
                     "at all",
                     "It breaks the receptive field",
                     "It removes the non-linearity"],
         "answer": 1,
         "why": "The saving comes from decoder convolutions reading half as "
                "many input channels. What is lost is information, not "
                "capacity - and lost information cannot be recovered by a "
                "bigger decoder."},
        {"q": "U-Net was trained on 30 images. What made that possible?",
         "options": ["The small parameter count",
                     "Elastic deformation augmentation, which generates "
                     "plausible variation of the specimen rather than of the "
                     "photograph",
                     "Transfer learning from ImageNet",
                     "The skip connections alone"],
         "answer": 1,
         "why": "Flips and shifts produce images from the same specimen. "
                "Elastic warps produce images that look like different "
                "specimens, which is the variation the model actually needs to "
                "generalise over. A weighted loss on the gaps between touching "
                "cells was the other essential piece."},
    ],
    refs=[("U-Net: Convolutional Networks for Biomedical Image Segmentation",
           "Ronneberger, Fischer & Brox, MICCAI 2015",
           "https://arxiv.org/abs/1505.04597"),
          ("nnU-Net: a self-configuring method for deep learning-based "
           "biomedical image segmentation",
           "Isensee et al., Nature Methods 2021", None)],
    description="Walk U-Net level by level: 572 in, 388 out, every skip crop "
                "computed, and the case for skip connections made by turning "
                "them off."))


# ---------------------------------------------------------------------------
# 6. YOLO v8
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "yolov8_detection",
    "computer_vision",
    "YOLO v8",
    "Object detection",
    "8,400 predictions, and the two thresholds that discard them",
    "One forward pass emits every box the model will ever consider. Move the "
    "confidence and NMS thresholds and watch objects appear, duplicate and "
    "vanish.",
    svg(box(12, 16, 60, 58, fill=S)
        + box(20, 26, 24, 40, fill="none", stroke=A, sw=1.6)
        + box(24, 30, 24, 40, fill="none", stroke=M, sw=1)
        + box(84, 16, 60, 58, fill=S)
        + box(94, 26, 24, 40, fill="none", stroke=A, sw=1.8)
        + txt(42, 84, "raw", M, 7) + txt(114, 84, "after NMS", A, 7)),
    {"widget": "yolo"},
    [
        "Three feature levels at strides 8, 16 and 32 give 80&sup2; + 40&sup2; "
        "+ 20&sup2; = <strong>8,400 predictions</strong> at 640&times;640.",
        "v8 is <em>anchor-free</em>. A cell predicts distances to the four box "
        "edges directly, so there are no anchor sizes to tune per dataset.",
        "The box is predicted as four 16-bin distributions and collapsed by "
        "taking the expectation &mdash; that is what the DFL loss trains.",
        "Confidence and NMS thresholds are inference-time knobs. Changing them "
        "changes your metrics without retraining anything.",
    ],
    r"""
title: YOLO v8
intro: One pass, 8,400 pick boxes. Two thresholds that decide which of them you ever see.

## One stage means one pass

A two-stage finder like Faster R-CNN proposes regions, then classifies and
refines each one. A one-stage finder does it in a single forward pass: the
head emits, for each cell of each feature level, a class vector and a box.
Nothing is proposed, nothing is cropped, nothing is re-run.

That is where the speed comes from and also where the awkwardness comes from,
because "each cell of each level" is a lot of boxes and almost all of them
are wrong. At 640&times;640 with three levels:

| Level | Stride | Grid | Predictions |
|---|---|---|---|
| P3 | 8 | 80 &times; 80 | 6,400 |
| P4 | 16 | 40 &times; 40 | 1,600 |
| P5 | 32 | 20 &times; 20 | 400 |
| | | | **8,400** |

Turn on the grid overlay in the explorer to see the three resolutions. P3's
cells are 8 input pixels across. This Is why it's the level that finds small
objects. P5's are 32 across. This Is why it handles large ones. This is the
feature pyramid, and it's the reason a finder can span an order of magnitude
of object size at all.

## Backbone, neck, head

each modern finder has this three-part shape, and it's worth being able to
name the parts.

The **backbone** is a classification network with the classifier removed
&mdash; in v8, a CSPDarknet variant whose repeating unit is the C2f block: a
split, a few bottleneck convolutions, and a concatenation of all the
mid outputs. It makes feature maps at strides 8, 16 and 32.

The **neck** mixes those levels. Semantic info is strongest at stride 32
and spatial precision is strongest at stride 8. So A top-down path carries
semantics down and a bottom-up path carries precision back up &mdash; the PAN
setup, itself a descendant of FPN. Without it, the level that can see
small objects has no idea what they're.

The **head** turns each level into guesses. v8's head is *decoupled*: one
small convolutional branch for classification and a separate one for box
regression, rather than a single branch predicting both. Sharing them makes the
two tasks fight over the same features, and separating them is worth about a
point of mAP for a small amount of find.

## Anchor-free, and what that replaced

Versions 2 through 7 were anchor-based: each cell carried a few prior boxes
of fixed size and aspect ratio, and the network predicted an offset from the
nearest one. That meant a set of anchor dims had to be chosen per dataset
&mdash; often by k-means over the training boxes. And it meant three
or more guesses per cell.

v8 predicts, from each cell, the distances from that cell's centre to the four
edges of the box. No priors, no offsets, one guess per cell. The
setting is gone.

The regression isn't a plain regression, though. Each of the four distances is
predicted as a **spread over 16 bins**. So The box branch emits
4 &times; 16 = 64 channels per cell, and the actual distance is the expectation
of that spread. This is Spread Focal Loss, and the reason for it's
that box edges are truly ambiguous. Where just does a blurred or
occluded boundary lie? &mdash; and a spread can express "probably 12,
possibly 15" where a single number can't. The network's own uncertainty
turns trainable.

There's also no **objectness** score in v8. Older versions predicted "is there
any of it here" apart from "what is it". V8's trust is just the class
score. One fewer output, one fewer loss term, one fewer thing to calibrate.

set during training is handled by **TaskAlignedAssigner**: rather than
a fixed rule about which cell owns which object, it scores each pick by a
combination of its classification trust and its IoU with the ground truth,
and assigns the top few. Cells that are already good at both get the label,
which is a mild form of the network choosing its own oversight.

## The two thresholds

All above is fixed at training time. The two controls in the explorer
aren't &mdash; they're applied after the forward pass, and changing them
changes your reported metrics without retraining any of it.

**trust threshold.** each guess below it's discarded. Push it up in
the explorer and boxes vanish. Push it past 0.55 and the note changes to warn
you, because the objects you lose first are just the hard ones &mdash; small,
occluded, unusual pose &mdash; which are the ones with low scores. A high
threshold makes a demo look clean and makes recall quietly terrible. The
default of 0.25 for visualisation is a display choice. For finding mAP you
use a thing like 0.001, because mAP integrates over the whole
precision-recall curve and truncating it early just throws away area.

**NMS IoU threshold.** a few neighbouring cells will each decide the same
object is theirs, so the head emits a cluster of near-the same boxes. Non-
max suppression sorts by trust, keeps the top box, and deletes
any of it shared it by more than the threshold, per class. Turn NMS off in
the explorer to see the raw cluster.

The threshold is a genuine trade and the "crowd" scene is there to show it.
Set it low, around 0.3, and two people standing close &mdash; who really do
share by more than 0.3. Are treated as duplicates and one is deleted.
Set it high, around 0.9, and duplicates live. There's no value that is
right for both a sparse scene and a dense one. This Is why crowded-scene
spotting has its own literature: Soft-NMS. This Decays scores instead of
deleting, and set-guess models like DETR. This Have no NMS at all because
their loss forbids duplicate guesses in the first place.

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

results = model.predict(
    "street.jpg",
    conf=0.25,     # the confidence cut
    iou=0.7,       # the NMS IoU threshold
    imgsz=640,     # must be a multiple of 32: strides are 8, 16, 32
    max_det=300,
)

for box in results[0].boxes:
    print(model.names[int(box.cls)], float(box.conf), box.xyxy[0].tolist())
```

`imgsz` has to be a multiple of 32 or the three levels don't divide evenly.
Raising it raises small-object recall roughly in proportion to the extra
pixels and costs latency as n&sup2; &mdash; often the single most
effective knob, and the one people forget exists while they tune `conf`.

## Why the model sizes are letters

v8 ships as n, s, m, l and x. Nano through extra-large &mdash; and they
are the same architecture with two multipliers applied: one to the channel
counts and one to the number of repeats in each C2f block. Nothing structural
differs between them.

That matters because it makes the fit/latency trade a dial rather than a
choice of architecture, and because the scaling is predictable: roughly, depth
and width both scale, so params grow faster than latency does. The nano
model is around 3 M params and the extra-large around 68 M, for perhaps
five points of COCO mAP between them.

The hands-on sequence for picking one is the reverse of what people often
do. Start from the latency budget on the actual target hardware, pick the
largest model that fits it, and only then look at fit. Choosing the model
first and optimising afterwards often ends in quantisation and pruning work
that a smaller model would have made unneeded.

## Reading the mismatch counter

The explorer's fourth statistic is **missed / duplicate / false**, recomputed
as you move the sliders. It's worth playing with on purpose, because the
three failure modes have three different causes:

- **Missed** objects mean the trust threshold is too high, or the object
  is smaller than P3 can resolve.
- **Duplicates** mean the NMS threshold is too high, or NMS is off.
- **False positives** mean the trust threshold is too low.

each real tuning session is spent trading these against each other, and mAP is
the single number that summarises the whole curve so you don't have to pick a
point on it until deployment.
## Questions people ask

<strong>Why are there 8,400 guesses for maybe five objects?</strong> Because a one-stage head emits one guess per cell per level. 80&sup2; + 40&sup2; + 20&sup2; = 8,400 cells at 640&times;640. Almost all are background. The trust cut plus NMS reduce them to the handful you see. Nothing is proposed and nothing is cropped. This Is just where the speed comes from.

<strong>What trust threshold should I use?</strong> Two answers for two jobs. For a demo or a production filter, a thing like 0.25. A display choice. For finding mAP, a thing like 0.001. MAP integrates the whole precision-recall curve and a high cut simply discards area. Reporting mAP measured at 0.25 understates your own model.

<strong>Why does it miss small objects?</strong> P3 has stride 8. Its cells are 8 input pixels across and an object a few pixels wide leaves almost no signal at any level. Raising `imgsz` is the fix, roughly in proportion to the extra pixels. Often a bigger win than any threshold change, and it costs latency as n&sup2;.

<strong>Why does my `imgsz` get rounded?</strong> It has to be a multiple of 32 so strides 8, 16 and 32 all divide evenly. That is also why 640 and 1280 are the conventional sizes.

<strong>Two shared people became one box. Is that the model failing?</strong> often not. It's NMS. Two people standing close truly share by more than a 0.3 IoU threshold. One is deleted as a duplicate. Raise the threshold and duplicates live instead. No single value is right for both sparse and crowded scenes. This Is why Soft-NMS and set-guess models like DETR exist.

<strong>How do I choose between n, s, m, l and x?</strong> Backwards from how it's often done. They're one architecture with a width and a depth multiplier. Roughly 3 M to 68 M params for about five points of COCO mAP. So start from the latency budget on the hardware you'll really deploy to, take the largest model that fits, and look at fit last.

## Recap in one screen

- One pass, one guess per cell per level: 6,400 + 1,600 + 400 = 8,400 picks at 640&times;640.
- Backbone, neck, head &mdash; features at strides 8/16/32, a PAN neck carrying semantics down and precision back up. A decoupled head so classification and regression stop fighting over the same features.
- Anchor-free: each cell predicts four edge distances, each as a spread over 16 bins. The box branch emits 64 channels and the model's own uncertainty turns trainable.
- Both thresholds are applied after the forward pass. trust decides what you see. NMS IoU decides what counts as a duplicate. Neither needs retraining.
- Missed means trust too high or the object is below P3's detail, duplicates mean NMS IoU too high, false positives mean trust too low.
""",
    [
        {"q": "Where do the 8,400 predictions at 640x640 come from?",
         "options": ["8,400 anchor boxes",
                     "Three feature levels at strides 8, 16 and 32: "
                     "80^2 + 40^2 + 20^2 cells, one prediction each",
                     "The number of classes times the grid size",
                     "A fixed proposal budget"],
         "answer": 1,
         "why": "v8 is anchor-free, so it is one prediction per cell rather "
                "than several. The three levels exist so that small objects "
                "are found by the fine grid and large ones by the coarse grid."},
        {"q": "What does the box branch actually output per cell?",
         "options": ["Four numbers: x, y, width, height",
                     "Four 16-bin distributions over the distance to each box "
                     "edge, collapsed by taking the expectation",
                     "An offset from the nearest anchor",
                     "A binary mask"],
         "answer": 1,
         "why": "That is Distribution Focal Loss: 4 x 16 = 64 channels. A "
                "distribution can express uncertainty about an ambiguous "
                "boundary in a way a single regressed number cannot."},
        {"q": "You raise the confidence threshold from 0.25 to 0.7 and your "
              "demo looks much cleaner. What has happened to your metrics?",
         "options": ["They have improved",
                     "Precision is up and recall is down, and the objects lost "
                     "first are the hard ones - small, occluded, unusual",
                     "Nothing changed, it is only a display setting",
                     "mAP is unaffected by the confidence threshold"],
         "answer": 1,
         "why": "A high threshold discards everything the model was unsure "
                "about, which is exactly the difficult cases. For computing "
                "mAP you use a very low threshold, because mAP integrates the "
                "whole precision-recall curve."},
        {"q": "Why does lowering the NMS IoU threshold hurt in a crowd?",
         "options": ["It slows NMS down",
                     "Two genuinely distinct people standing close overlap by "
                     "more than a low threshold, so the second is deleted as a "
                     "duplicate of the first",
                     "It increases false positives",
                     "It changes the class scores"],
         "answer": 1,
         "why": "NMS cannot tell a duplicate of one object from two real "
                "overlapping objects; it only sees IoU. That ambiguity is why "
                "Soft-NMS and set-prediction detectors like DETR exist."},
    ],
    refs=[("You Only Look Once: Unified, Real-Time Object Detection",
           "Redmon, Divvala, Girshick & Farhadi, CVPR 2016",
           "https://arxiv.org/abs/1506.02640"),
          ("Generalized Focal Loss: Learning Qualified and Distributed Bounding "
           "Boxes for Dense Object Detection", "Li et al., NeurIPS 2020",
           "https://arxiv.org/abs/2006.04388"),
          ("Ultralytics YOLOv8", "Ultralytics documentation",
           "https://docs.ultralytics.com/models/yolov8/")],
    description="See all 8,400 raw YOLO predictions, then move the confidence "
                "and NMS thresholds and watch objects appear, duplicate and "
                "disappear."))


# ---------------------------------------------------------------------------
# 7. Mask R-CNN
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "mask_rcnn",
    "computer_vision",
    "Mask R-CNN",
    "Instance segmentation",
    "RoIAlign against RoIPool, on a real feature map",
    "The paper's whole contribution is that RoIPool rounds twice and a mask "
    "cannot survive it. Drag a proposal and watch the rounding move it eight "
    "pixels.",
    svg(box(14, 18, 58, 58, fill=S)
        + box(24, 28, 34, 30, fill="none", stroke=A, sw=1.8)
        + box(20, 24, 40, 36, fill="none", stroke=M, sw=1.2, rx=0)
        + txt(43, 86, "rounded vs real", M, 7)
        + box(88, 18, 58, 58, fill=S)
        + line(88, 37, 146, 37, B, 0.8) + line(88, 56, 146, 56, B, 0.8)
        + line(107, 18, 107, 76, B, 0.8) + line(127, 18, 127, 76, B, 0.8)
        + circle(97, 27, 2, A, A, 0) + circle(117, 46, 2, A, A, 0)
        + circle(137, 65, 2, A, A, 0)
        + txt(117, 86, "bilinear samples", A, 7)),
    {"widget": "maskrcnn"},
    [
        "Mask R-CNN is Faster R-CNN plus a third head. The third head only "
        "works because of RoIAlign.",
        "RoIPool rounds twice: once snapping the region to whole cells, once "
        "snapping the bin boundaries. At stride 16 half a cell is 8 pixels.",
        "The mask head predicts <strong>one 28&times;28 mask per class</strong> "
        "and the loss only touches the ground-truth class's channel.",
        "Classification never noticed the misalignment. A per-pixel output "
        "notices immediately &mdash; the paper reports up to a 50% relative "
        "gain on mask AP under strict IoU.",
    ],
    r"""
title: Mask R-CNN
intro: Faster R-CNN with a third head. One fixed rounding bug that is the entire reason the third head works.

## The architecture, in four parts

Mask R-CNN inherits almost all from Faster R-CNN and adds one branch.

1. A **backbone with a feature pyramid**. Often ResNet-50 or -101 with
   FPN &mdash; making feature maps at strides 4, 8, 16 and 32.
2. A **region proposal network** sliding over those maps, emitting a few
   thousand class-agnostic "a thing is here" boxes, cut to around 1,000 by
   NMS.
3. **RoIAlign**, which crops a fixed-size feature patch for each proposal.
4. Three **heads** on that patch: classification, box refinement, and the new
   one, a mask.

The heads are where the param budget sits, and the split is unintuitive:

| Head | Input | Structure | Output | Parameters |
|---|---|---|---|---|
| classification | 7&times;7&times;256 | fc 12544&rarr;1024, fc 1024&rarr;1024 | 81 scores | ~13.9 M |
| box | shares those two fc layers | | 4 &times; 80 offsets | ~0.33 M |
| mask | 14&times;14&times;256 | 4 &times; conv3&times;3(256), deconv, conv1&times;1 | 80 &times; 28 &times; 28 | ~2.64 M |

The mask head is the *cheapest* of the three despite making 62,720 numbers,
because it's fully convolutional and the box head isn't.

## The bug that mattered

RoIPool, inherited from Fast R-CNN, converts an any region of a feature
map into a fixed 7&times;7 grid. It does so with two roundings:

1. The proposal's floating-point coords are snapped to whole feature cells.
2. The 7&times;7 bin boundaries inside that region are snapped to whole cells
   too.

Drag the proposal in the explorer and watch the dashed red box &mdash; what
RoIPool really pools &mdash; jump around the solid orange one, which is what
the RPN proposed. The statistic underneath translates the gap into input
pixels: at stride 16, being half a feature cell out is **8 pixels** in the
first image. At stride 32 it's 16.

For classification this truly doesn't matter. The question "is this a cat"
has the same answer whether your crop is eight pixels off, and the pooled
features are a summary either way. For a mask it matters enormously, because
the output is a per-pixel map that gets pasted back onto the image at that
location. An eight-pixel systematic offset is visible in each single
guess.

## RoIAlign

RoIAlign drops both roundings. The region keeps its floating-point
coords, the bins are cut just, and inside each bin four sample
points are read by **bilinear interpolation** from the four nearest feature
cells &mdash; then averaged.

The dots in the explorer are those sample points. Watch them slide smoothly as
you drag, where the red box jumps in discrete steps.

The smoothness is the technical point, not just an aesthetic one. Bilinear
interpolation is differentiable for the sampling location, so
grads flow back to the box coords. Rounding is a step function whose
deriv is zero all over it's defined. So RoIPool silently cut that path.

The two pooled maps are drawn side by side with their mean abs difference.
Nudge the proposal width by a tenth of a cell: the RoIAlign map barely moves,
the RoIPool map can change a lot. The paper reports that this change
alone raises mask AP by around 10 points scaled on COCO, and by up to 50%
scaled under the strict IoU=0.75 criterion &mdash; where being eight pixels
out is just what decides a match.

## Decoupling mask from class

The second design choice is easy to miss. The mask head predicts **K
separate masks**, one per class, and the loss is only applied to the channel of
the ground-truth class.

The option &mdash; one mask with a per-pixel softmax over classes &mdash;
is what FCN-style semantic segmentation does, and it forces the classes to
compete pixel by pixel. Mask R-CNN doesn't need that contest, because the
classification head has already decided what the object is. Letting the mask
branch answer "which pixels belong to *this* object" on its own of "what
class is it" is worth a few points of AP. It's why the mask branch never
learns to suppress one class in favour of another.

At inference you take the classification head's argmax and read only that
channel's 28&times;28 mask, resize it to the predicted box, and threshold at
0.5. The resize is why instance masks from this family have a characteristically
soft, slightly blobby boundary: the real detail of the answer is 28&times;28
inside the box, but large the box is.

## Which pyramid level a proposal is read from

One detail sits between the RPN and RoIAlign and it's the reason the stride
control on this page has three settings.

With a feature pyramid there are four pick maps to crop from, at strides
4, 8, 16 and 32, and a proposal has to be assigned to one. Cropping a small
object from the stride-32 map would give a region a couple of cells across,
which holds almost nothing. Cropping a large one from stride 4 wastes work
and gives features with too little context.

FPN assigns by size: a proposal of area *A* goes to level
`k = floor(4 + log2(sqrt(A) / 224))`, clamped to the available range. A
224&times;224 proposal &mdash; the ImageNet size, chosen on purpose &mdash;
lands on level 4, at stride 16. any of it smaller drops to a finer level and
any of it larger rises to a coarser one.

Switch the stride control in the explorer and watch the misalignment figure
scale with it. The same half-cell rounding error is 2 pixels at stride 4 and 16
pixels at stride 32. This Is why the coarse levels are where RoIPool hurt
most, and why the effect was largest on just the large objects that a
finder or else finds easy.

## The loss, and the multi-task balance

```
L = L_cls + L_box + L_mask
```

Three terms, equally weighted, plus the RPN's own two. `L_mask` is an mean
binary cross-entropy over the 28&times;28 grid of the correct class's channel
only. It's worth noticing that nothing here is tuned: the paper doesn't
weight the mask loss up or down. This Is unusual for a multi-task network and
suggests the three tasks are truly compatible rather than competing for
room.

```python
import torchvision
from torchvision.models.detection import maskrcnn_resnet50_fpn

model = maskrcnn_resnet50_fpn(weights="DEFAULT").eval()
out = model([image_tensor])[0]

keep = out["scores"] > 0.5
boxes = out["boxes"][keep]           # [N, 4]
masks = out["masks"][keep]           # [N, 1, H, W], already pasted, soft
labels = out["labels"][keep]

binary = masks[:, 0] > 0.5           # the 0.5 threshold, applied explicitly
```

Two things in that snippet catch people. `masks` comes back already resized and
pasted to full image detail, and it's *soft* &mdash; chances, not
booleans &mdash; so a threshold has to be applied, and 0.5 is a choice rather
than a law. And the masks share: this is instance segmentation, so two
instances can both claim a pixel, and resolving that into a single label per
pixel is panoptic segmentation. This Is a different task with a different
metric.

## What it left behind

Mask R-CNN was state of the art in 2017 and is now the baseline that faster
methods are measured against. YOLACT and SOLO give instance masks in one
stage. Mask2Former and the DETR family replace the whole propose-and-crop
structure with set guess and focus, and have no RoIAlign, no NMS and
no anchors at all.

But RoIAlign itself outlived the architecture. Any time you need to read a
feature map at a location that isn't on the grid &mdash; deformable
convolutions, spatial transformers, keypoint heads, the 3-D finders that
project points into image features. The answer is bilinear sampling for
just the reasons here: it's accurate and it's differentiable in the
coord. The lesson generalises past spotting: **if a location is
smooth, don't round it.**
## Questions people ask

<strong>Why did rounding hurt masks but not classification?</strong> Because the two answers have different shapes. "Is this a cat" lives a crop that is eight pixels off. The pooled features are a summary either way. A mask is a per-pixel map pasted back at that location. A systematic eight-pixel offset is visible in each single guess. Same error, very different consequence.

<strong>Why does the grad arg matter as much as the fit one?</strong> Bilinear interpolation is differentiable for the sampling location. Grads reach the box coords. Rounding is a step function whose deriv is zero wherever it's defined. So RoIPool silently severed that path. RoIAlign didn't only reduce an error, it restored a training signal.

<strong>Why are the masks 28&times;28?</strong> That is the mask head's output grid, resized to the predicted box at inference. So the real detail of the answer is 28&times;28 inside the box but large the box is. This Is just why instance masks from this family have soft, slightly blobby boundaries. And why later work raised the grid or refined boundaries apart, as PointRend does.

<strong>Why one mask per class instead of a per-pixel softmax?</strong> Because the classification head has already decided what the object is. The mask branch only has to answer "which pixels belong to this object". A per-pixel softmax makes the classes compete pixel by pixel. What FCN-style semantic segmentation does. And it costs a few points of AP here.

<strong>Why do my masks share?</strong> Because this is instance segmentation. Each instance gets its own free mask and two can both claim a pixel. Forcing one label per pixel is panoptic segmentation, a different task with a different metric. The returned masks are also soft chances. The 0.5 threshold is a choice rather than a law.

<strong>Which pyramid level does a proposal get cropped from?</strong> By area: `k = floor(4 + log2(sqrt(A) / 224))`, clamped to the available levels. A 224&times;224 proposal lands on stride 16. The ImageNet size, chosen on purpose. And smaller objects drop to finer levels. That is why the half-cell rounding error scaled from 2 pixels at stride 4 to 16 at stride 32. Why the damage was worst on the large objects a finder or else finds easy.

## Recap in one screen

- Faster R-CNN plus one branch: an FPN backbone, RPN proposals, an RoIAlign crop, then classification, box and mask heads.
- The mask head is the cheapest of the three despite emitting 62,720 numbers. It's fully convolutional and the box head isn't.
- RoIPool rounded twice &mdash; the region to whole feature cells, then the bin boundaries. At stride 16 half a cell is 8 input pixels.
- RoIAlign keeps the floating-point coords and samples by bilinear interpolation. About 10 points of scaled mask AP. Up to 50% at the strict IoU=0.75.
- The masks are per-class, free, 28&times;28 inside the box, soft, and allowed to share.
- If a location is smooth, don't round it. The idea that outlived the architecture.
""",
    [
        {"q": "RoIPool rounds twice. Where?",
         "options": ["Once on the input image and once on the output",
                     "Once snapping the proposal to whole feature cells, and "
                     "again snapping the bin boundaries inside it",
                     "Once on the class score and once on the box",
                     "Only during training"],
         "answer": 1,
         "why": "Both roundings shift the region that is actually pooled. At "
                "stride 16, half a feature cell of error is eight pixels in "
                "the original image."},
        {"q": "Why did that misalignment not matter for Faster R-CNN?",
         "options": ["Faster R-CNN used a different backbone",
                     "Its outputs are a class and a box - coarse, whole-region "
                     "answers that survive an eight-pixel shift. A per-pixel "
                     "mask does not",
                     "It used RoIAlign already",
                     "It ran at higher resolution"],
         "answer": 1,
         "why": "This is the whole insight of the paper. The same operator was "
                "adequate for two tasks and disqualifying for the third, "
                "because only the third produces an answer per pixel."},
        {"q": "Besides accuracy, what does bilinear sampling give that "
              "rounding does not?",
         "options": ["Lower memory use",
                     "A derivative with respect to the sampling location, so "
                     "gradients can flow back to the box coordinates",
                     "Faster inference",
                     "Scale invariance"],
         "answer": 1,
         "why": "Rounding is a step function with zero derivative almost "
                "everywhere, which silently cuts the gradient path to the "
                "coordinates. Bilinear interpolation is smooth in the "
                "location, which is also why it reappears in deformable "
                "convolutions and spatial transformers."},
        {"q": "The mask head predicts one 28x28 mask per class rather than one "
              "mask with a per-pixel class softmax. Why?",
         "options": ["It is cheaper",
                     "The classification head has already decided the class, so "
                     "the mask branch never has to make classes compete pixel "
                     "by pixel",
                     "Because masks overlap",
                     "To support panoptic segmentation"],
         "answer": 1,
         "why": "Decoupling the two questions is worth several points of AP. "
                "The mask loss only touches the ground-truth class's channel, "
                "so the branch answers 'which pixels are this object' without "
                "also having to answer 'what is it'."},
    ],
    refs=[("Mask R-CNN", "He, Gkioxari, Dollar & Girshick, ICCV 2017",
           "https://arxiv.org/abs/1703.06870"),
          ("Faster R-CNN: Towards Real-Time Object Detection with Region "
           "Proposal Networks", "Ren, He, Girshick & Sun, NeurIPS 2015",
           "https://arxiv.org/abs/1506.01497"),
          ("Feature Pyramid Networks for Object Detection",
           "Lin et al., CVPR 2017", "https://arxiv.org/abs/1612.03144")],
    description="Drag a proposal on a feature map and watch RoIPool's double "
                "rounding move it eight input pixels while RoIAlign samples it "
                "exactly."))
