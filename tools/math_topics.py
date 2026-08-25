# -*- coding: utf-8 -*-
"""Content for the generated maths modules.

Twenty-seven modules, and only four of them linked to from anywhere else on
the site - which is the wrong shape for the track everything depends on.
Pages elsewhere used orthogonality, SVD, convexity, quantiles and sampling
distributions as though they had been introduced. None of them had. PCA is
the sharpest case: it assumes an eigendecomposition and an SVD, and only the
first was taught.

These ten are that missing floor. They are demonstrations rather than
simulations - nothing is fitted, and the arithmetic is the point. The SVD on
the page is a real decomposition of the matrix the reader is editing, the
central limit page really resamples the population it draws, and the
convexity page really runs gradient descent and really gets stuck.

The plotting and the RNG live in assets/vizlearn-plot.js, shared with the
machine learning harness; the demonstrations are in assets/vizlearn-math.js.
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


def _dot(x, y, fill=M, r=2.6):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (x, y, r, fill)


def _line(x1, y1, x2, y2, stroke=A, sw=1.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, stroke, sw, d))


def _axes():
    return _line(20, 72, 148, 72, B, 1) + _line(20, 72, 20, 16, B, 1)



# ---------------------------------------------------------------------------
# 1. Basis, span and orthogonality
# ---------------------------------------------------------------------------
topic(
    "basis_span_and_orthogonality",
    "Basis, Span and Orthogonality",
    "Linear Algebra",
    "Two vectors either reach every point in the plane or they reach a single "
    "line. Drag them and watch the moment it collapses.",
    _svg(_line(30, 66, 92, 30, A, 2) + _line(30, 66, 76, 74, M, 2)
         + '<path d="M30 66 L92 30 L138 38 L76 74 Z" fill="%s" fill-opacity="0.18" stroke="none"/>' % A
         + _txt(80, 86, "what two vectors reach", M, 7)),
    {
        "demo": "basis",
        "drag": {"xr": [-4, 4], "yr": [-3, 3],
                 "hint": "Drag on the chart to move whichever vector tip is nearer."},
        "controls": [
            {"key": "x1", "label": "v1 x", "type": "range",
             "min": -4, "max": 4, "step": 0.1, "value": 2.0},
            {"key": "y1", "label": "v1 y", "type": "range",
             "min": -3, "max": 3, "step": 0.1, "value": 0.4},
            {"key": "x2", "label": "v2 x", "type": "range",
             "min": -4, "max": 4, "step": 0.1, "value": 0.6},
            {"key": "y2", "label": "v2 y", "type": "range",
             "min": -3, "max": 3, "step": 0.1, "value": 1.8},
        ],
    },
    [
        "The <strong>span</strong> of a set of vectors is everything you can "
        "reach by scaling and adding them.",
        "Two vectors in the plane span the whole plane <em>unless</em> they lie "
        "on the same line, in which case they span only that line.",
        "The shaded parallelogram is the <a href='determinant.html'>determinant</a>. "
        "It hits zero exactly when the span collapses.",
        "<strong>Orthogonal</strong> means the dot product is zero. It is not "
        "required for a basis, but it makes every calculation easier.",
    ],
    """
title: Basis, Span and Orthogonality
intro: What a set of vectors can reach, when it stops reaching everything, and why perpendicular is worth so much.

## Span

Given some vectors, the **span** is every point you can reach by scaling them
and adding the results. Nothing more exotic than that: pick a multiple of each,
add them up, and see where you land.

Two vectors in the plane usually span the whole plane. Any point you name can
be written as some amount of the first plus some amount of the second, and the
visualisation shows the shaded parallelogram they generate.

Usually &mdash; but not always. Drag one vector until it lines up with the
other and the parallelogram flattens to nothing. Now every combination lands
on a single line, and most of the plane has become unreachable. The vectors
are **linearly dependent**: one is a multiple of the other, so the second adds
no direction the first did not already have.

## The determinant is the test

You do not have to eyeball it. The readout gives the determinant, which is the
signed area of that parallelogram, and it reaches zero exactly when the span
collapses.

That is the same number the [determinant module](determinant.html) covers as an
area scale factor, seen from another side. A matrix whose determinant is zero
squashes the plane onto a line, which is precisely why it has no inverse:
several inputs land on the same output, so nothing can undo it.

## Basis

A **basis** is a set of vectors that spans the space and is linearly
independent &mdash; enough to reach everything, with nothing redundant.

Both halves matter. Too few vectors and you cannot reach everything. Too many
and the representation stops being unique, because there is more than one way
to write the same point. A basis is the exact amount.

Once you have one, every point in the space has exactly one set of coordinates
in it. That is the whole reason coordinates work at all, and it is why
"[change of basis](matrix_as_transformation.html)" is a meaningful operation
rather than a rearrangement.

The plane needs exactly two vectors in any basis; three-dimensional space needs
three. That count is the **dimension**, and it does not depend on which basis
you choose.

## Orthogonality

Two vectors are **orthogonal** when their [dot
product](vectors_and_dot_product.html) is zero &mdash; the algebraic way of
saying they meet at a right angle. Drag until the readout says so.

Orthogonality is not required for a basis. The default pair above is a
perfectly good basis and is nowhere near perpendicular. But an orthogonal basis
is worth reaching for, because finding the coordinates of a point becomes a
matter of taking one dot product per axis instead of solving a system of
equations.

An **orthonormal** basis adds that every vector has length 1. Then the matrix
whose columns are those vectors has a remarkable property: its inverse is its
transpose. Undoing the transformation costs nothing at all, which is why
orthonormal bases turn up wherever numerical stability matters.

The standard basis &mdash; (1, 0) and (0, 1) &mdash; is orthonormal, which is
why ordinary coordinates feel so natural.

## Where this shows up

**PCA** finds an orthonormal basis aligned with the directions of greatest
variance in the data. The orthogonality is the point: the components do not
overlap, so each one describes something the others do not.

**[SVD](singular_value_decomposition.html)** produces two orthonormal bases,
one for the input space and one for the output.

**QR decomposition** exists to manufacture an orthonormal basis from an
arbitrary one, and least-squares solvers use it because the resulting system is
far better conditioned than the direct approach.

**Fourier and wavelet transforms** are changes into an orthogonal basis chosen
so the interesting structure shows up in a few coordinates.

## Where it goes wrong

**Nearly dependent vectors.** A determinant of exactly zero is easy to spot; a
determinant of 0.001 is the same problem wearing a disguise. The basis still
technically works, and everything computed in it is numerically unstable. The
[condition number](singular_value_decomposition.html) is how you measure it.

**Assuming orthogonal means independent.** It does &mdash; orthogonal non-zero
vectors are always independent. The converse fails, and that is the direction
people assume.

**Forgetting to normalise.** Orthogonal gives you the easy inverse only when
the vectors also have length 1.
""",
    [
        {"q": "Two vectors in the plane have determinant zero. What do they span?",
         "options": ["The whole plane", "A line through the origin", "A single point", "Nothing"],
         "answer": 1,
         "why": "The parallelogram has collapsed, so one vector is a multiple of the other and adds no new direction. Every combination lands on one line."},
        {"q": "What does an orthonormal basis buy you?",
         "options": ["A larger span",
                     "The matrix of those vectors has its transpose as its inverse",
                     "A non-zero determinant",
                     "Fewer vectors are needed"],
         "answer": 1,
         "why": "Undoing the transformation becomes free, which is why orthonormal bases turn up wherever numerical stability matters."},
        {"q": "Why is a determinant of 0.001 a problem even though it is not zero?",
         "options": ["It makes the span smaller",
                     "The basis is nearly dependent, so anything computed in it is numerically unstable",
                     "It cannot be inverted",
                     "It means the vectors are orthogonal"],
         "answer": 1,
         "why": "Exact zero is easy to catch. Nearly zero is the same problem in disguise, and the condition number is how it is measured."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Singular Value Decomposition
# ---------------------------------------------------------------------------
topic(
    "singular_value_decomposition",
    "Singular Value Decomposition",
    "Linear Algebra",
    "Every matrix, however ugly, is a rotation then a stretch then another "
    "rotation. Step through the three and watch it happen.",
    _svg('<circle cx="34" cy="46" r="18" fill="none" stroke="%s" stroke-width="2"/>' % M
         + _txt(60, 50, "&#8594;", A, 12)
         + '<ellipse cx="104" cy="46" rx="30" ry="13" transform="rotate(-18 104 46)" fill="none" stroke="%s" stroke-width="2"/>' % A
         + _txt(80, 82, "a circle becomes an ellipse", M, 7)),
    {
        "demo": "svd",
        "controls": [
            {"key": "stage", "label": "Stage", "type": "select", "value": "full",
             "options": [{"value": "input", "label": "1. The unit circle"},
                         {"value": "rotate1", "label": "2. After V' (rotate)"},
                         {"value": "stretch", "label": "3. After Sigma (stretch)"},
                         {"value": "full", "label": "4. After U (rotate) - the whole matrix"}]},
            {"key": "a", "label": "matrix a", "type": "range",
             "min": -2.5, "max": 2.5, "step": 0.1, "value": 1.6},
            {"key": "b", "label": "matrix b", "type": "range",
             "min": -2.5, "max": 2.5, "step": 0.1, "value": 0.8},
            {"key": "c", "label": "matrix c", "type": "range",
             "min": -2.5, "max": 2.5, "step": 0.1, "value": 0.3},
            {"key": "d", "label": "matrix d", "type": "range",
             "min": -2.5, "max": 2.5, "step": 0.1, "value": 1.1},
        ],
    },
    [
        "Any matrix factors as <code class='mono-font'>A = U &Sigma; V'</code>: "
        "rotate, stretch along the axes, rotate again.",
        "The <strong>singular values</strong> in &Sigma; are the stretch factors, "
        "always non-negative and always in descending order.",
        "Unlike <a href='eigenvalues_and_eigenvectors.html'>eigenvectors</a>, an "
        "SVD exists for <em>every</em> matrix &mdash; non-square ones included.",
        "The <strong>condition number</strong> is the largest singular value "
        "divided by the smallest. Large means the matrix is near-singular.",
    ],
    """
title: Singular Value Decomposition
intro: The factorisation that works on every matrix, and the one worth knowing if you only learn one.

## What every matrix does

Take the unit circle and apply any 2&times;2 matrix. The result is always an
ellipse. Not sometimes &mdash; always, for every matrix there is.

That is a strong claim, and the SVD is the reason it holds. Every matrix can be
written as three operations in sequence:

```
A  =  U  Sigma  V'
```

Read right to left, which is the order they apply:

**V'** rotates. A rotation does nothing to a circle, which is why stage 2 in the
visualisation looks identical to stage 1 &mdash; but watch the two spokes, which
do move. It is choosing which directions are about to be stretched.

**Sigma** stretches along the axes, by the **singular values**. This is where
the circle becomes an ellipse.

**U** rotates the ellipse into its final orientation.

Step through the four stages above and the claim stops being abstract. Whatever
you set the four matrix entries to, the shape at stage 3 is an axis-aligned
ellipse, every time.

## The singular values

They are the lengths of the ellipse's semi-axes, always non-negative, and
conventionally listed largest first.

**The largest** is how much the matrix can stretch any vector &mdash; its gain
in the worst case.

**The smallest** is how much it can squash one.

**Their ratio** is the **condition number**, and it is the single most useful
number in the readout. A condition number near 1 means the matrix treats all
directions roughly alike. A large one means it nearly flattens some direction,
and solving anything involving that matrix will amplify error along it. Drag the
entries until the two singular values are far apart and watch the ellipse become
a sliver.

**A zero singular value** means the matrix genuinely flattens a direction: the
ellipse degenerates to a line segment, the matrix is singular, and it has no
inverse.

## Why not eigenvectors

The [eigendecomposition](eigenvalues_and_eigenvectors.html) is the more famous
factorisation, and the SVD is the more useful one, for three reasons.

**It always exists.** Eigendecomposition requires a square matrix, and even
then not every square matrix has one. The SVD exists for every matrix of every
shape, including a 1000&times;3.

**Its bases are orthonormal.** Eigenvectors need not be perpendicular, and when
they are nearly parallel the decomposition is numerically fragile. U and V are
[orthonormal](basis_span_and_orthogonality.html) by construction.

**Its values are real and non-negative.** Eigenvalues of a real matrix can be
complex. Singular values never are.

For a symmetric positive-definite matrix the two coincide, which is why they
are so often confused.

## Low-rank approximation

The property that makes the SVD indispensable: keep only the largest *k*
singular values, set the rest to zero, and multiply back. The result is
provably the best rank-*k* approximation of the original matrix, in the
least-squares sense. Not a good one &mdash; the best.

That single fact underwrites a surprising amount:

**PCA** is the SVD of the mean-centred data matrix. The principal components
are the right singular vectors and the explained variances are the squared
singular values, which is why any PCA implementation you look inside is calling
an SVD.

**Image compression** keeps the top singular values of the pixel matrix.

**Latent semantic analysis** factors a term-document matrix and reads the
retained dimensions as topics.

**Recommender systems** factor a sparse user-item matrix into a low-rank
product.

**Noise reduction** works on the assumption that signal concentrates in the
large singular values and noise spreads through the small ones.

## Where it goes wrong

**Forgetting to centre before PCA.** Without subtracting the mean, the first
component points at the mean rather than at the direction of greatest variance.

**Reading a condition number as an error.** It is a sensitivity: it says how
much input error can be amplified, not how much has been.

**Assuming singular values are eigenvalues.** They are the eigenvalues of A'A,
square-rooted. Not the same object, and not equal except in special cases.

**Computing the full SVD when you want the top few.** For a large sparse matrix
a truncated solver is orders of magnitude cheaper.
""",
    [
        {"q": "What shape does the unit circle become under any 2x2 matrix?",
         "options": ["Another circle", "An ellipse", "A parallelogram", "It depends on the matrix"],
         "answer": 1,
         "why": "Always an ellipse - that is what the SVD asserts. Rotate, stretch along the axes, rotate again, and stage 3 is an axis-aligned ellipse for every matrix."},
        {"q": "What does a large condition number tell you?",
         "options": ["The matrix is large",
                     "The matrix nearly flattens some direction, so solving with it amplifies error",
                     "The determinant is negative",
                     "The singular values are complex"],
         "answer": 1,
         "why": "It is the largest singular value over the smallest. Near 1 means all directions are treated alike; large means the ellipse is a sliver."},
        {"q": "Why is the SVD preferred over an eigendecomposition?",
         "options": ["It is faster",
                     "It exists for every matrix of every shape, and its bases are orthonormal",
                     "Its values can be complex",
                     "It does not require centring"],
         "answer": 1,
         "why": "Eigendecomposition needs a square matrix and does not always exist even then; eigenvectors need not be perpendicular. Singular values are always real and non-negative."},
    ],
)


# ---------------------------------------------------------------------------
# 3. Jacobian and Hessian
# ---------------------------------------------------------------------------
topic(
    "jacobian_and_hessian",
    "The Jacobian and the Hessian",
    "Calculus",
    "The first derivative says which way is downhill. The second says how far "
    "you can safely go.",
    _svg('<path d="M20 70 C 50 70, 58 24, 80 24 C 102 24, 110 70, 140 70" fill="none" stroke="%s" stroke-width="2"/>' % A
         + _line(44, 66, 84, 30, M, 1.6, "4 3")
         + _dot(62, 44, A, 3.4)
         + _txt(80, 84, "slope, and the bend under it", M, 7)),
    {
        "demo": "curvature",
        "controls": [
            {"key": "curve", "label": "Curvature (second derivative / 2)", "type": "range",
             "min": -1.0, "max": 1.5, "step": 0.05, "value": 0.6},
            {"key": "slope", "label": "Linear term", "type": "range",
             "min": -3, "max": 3, "step": 0.1, "value": -0.8},
            {"key": "at", "label": "Evaluate at x", "type": "range",
             "min": -2.5, "max": 2.5, "step": 0.1, "value": 1.2},
        ],
    },
    [
        "The <strong>gradient</strong> collects the first partial derivatives: "
        "one number per input, saying which way is uphill.",
        "The <strong>Jacobian</strong> generalises it to functions with several "
        "outputs &mdash; one row per output, one column per input.",
        "The <strong>Hessian</strong> collects the second derivatives. It "
        "describes curvature: how the gradient itself changes.",
        "Backpropagation is repeated Jacobian multiplication, done right to left "
        "because that keeps the intermediate object a vector rather than a matrix.",
    ],
    """
title: The Jacobian and the Hessian
intro: The two matrices of derivatives every optimiser is built on, and why one of them is almost never computed.

## From one derivative to a table of them

For a function of one variable the derivative is one number: the slope. The
[chain rule](the_chain_rule.html) and
[partial derivatives](partial_derivatives_and_gradient.html) modules cover
that ground.

Real functions have many inputs and often many outputs, and the derivatives
have to be organised.

**The gradient** applies when there are many inputs and one output &mdash; a
loss function. It is a vector holding one partial derivative per input, and it
points in the direction of steepest increase.

**The Jacobian** applies when there are many outputs too. It is a matrix with
one row per output and one column per input, entry (i, j) being how much output
*i* changes when input *j* moves. A gradient is a Jacobian with one row.

**The Hessian** is the matrix of second derivatives of a single-output
function: entry (i, j) is the derivative of the *i*-th partial derivative with
respect to input *j*. It describes how the gradient changes as you move.

## What curvature buys you

The visualisation is one-dimensional, where the gradient and the Hessian are
each a single number, so the relationship is visible without any matrix
notation.

The dashed line is the tangent &mdash; the first derivative. It says which way
is downhill and how steeply, and it says nothing at all about how long that
remains true.

The second derivative is the missing piece. Drag the curvature control:

**Large positive curvature** is a tight valley. The gradient changes quickly, so
a big step overshoots and lands on the far wall.

**Small positive curvature** is a shallow bowl. The gradient stays roughly
constant, so a big step is safe and a small one wastes time.

That is exactly the information a step size wants, and it is why an optimiser
that knows the curvature can choose its own step instead of being handed a
learning rate.

**Negative curvature** is a maximum in that direction. Descent will accelerate
away from it, which is usually what you want and is why saddle points are less
dangerous in practice than they sound.

For a multivariable function the Hessian's eigenvalues carry the same
information per direction: all positive is a minimum, all negative a maximum,
mixed signs a saddle.

## Newton's method, and why nobody runs it on a network

Knowing the curvature suggests an obvious improvement over gradient descent:
step by the gradient scaled by the inverse Hessian rather than by a fixed
learning rate. That is **Newton's method**, and near a minimum it converges
quadratically &mdash; roughly doubling the correct digits each iteration, where
gradient descent plods.

It is not used for neural networks, for a reason that is pure arithmetic.

A model with *n* parameters has a Hessian with *n*&sup2; entries. At a million
parameters that is 10&sup1;&sup2; numbers to store, and inverting it costs
about *n*&sup3;. For a model with a billion parameters the Hessian does not fit
in the observable universe, let alone in memory.

So the field uses approximations. **L-BFGS** keeps a low-rank estimate built
from recent gradients. **Adam** and its relatives keep a diagonal estimate
&mdash; one number per parameter rather than a full matrix &mdash; which is why
they adapt a per-parameter step size and why they work at scale. Adam is
sometimes described as a diagonal approximation to second-order optimisation,
and that is a fair reading of what it does.

## Backpropagation is Jacobians

Every layer of a network is a function with many inputs and many outputs, so
each has a Jacobian. The chain rule says the derivative of the whole network is
the product of them all.

The order of that multiplication is the whole trick. Multiplying left to right
&mdash; forward mode &mdash; keeps a full matrix at every step. Multiplying
right to left &mdash; reverse mode, which is backpropagation &mdash; starts
from the scalar loss, so every intermediate stays a **vector**.

That is why training is affordable. The cost of a backward pass is a small
multiple of a forward pass, regardless of how many parameters there are,
because no Jacobian is ever formed in full.

## Where it goes wrong

**Trying to compute a Hessian for a large model.** It does not fit. Use a
diagonal or low-rank approximation.

**Assuming a zero gradient means a minimum.** It means a stationary point. The
Hessian's eigenvalues tell you which kind.

**Confusing the Jacobian with the gradient.** The gradient is the special case
of one output. Frameworks expose `jacobian` and `grad` separately for exactly
this reason.

**Expecting second-order methods to be a drop-in win.** They shine on small,
well-conditioned problems and on batch objectives, not on stochastic
mini-batch training where the curvature estimate is noise.
""",
    [
        {"q": "What does the Hessian tell you that the gradient does not?",
         "options": ["Which direction is downhill",
                     "How quickly the gradient changes, and therefore how far a step can safely go",
                     "The value of the function",
                     "Whether the function is continuous"],
         "answer": 1,
         "why": "The tangent says which way and how steeply; it says nothing about how long that remains true. Curvature is exactly what a step size wants to know."},
        {"q": "Why is Newton's method not used to train large neural networks?",
         "options": ["It converges too slowly",
                     "The Hessian has n^2 entries and costs about n^3 to invert, which is impossible at a million parameters",
                     "It requires a convex loss",
                     "It cannot handle mini-batches"],
         "answer": 1,
         "why": "Near a minimum it converges quadratically, which is far better than gradient descent - it is purely the arithmetic that rules it out. Adam keeps a diagonal approximation instead."},
        {"q": "Why does backpropagation multiply Jacobians right to left?",
         "options": ["It is more numerically stable",
                     "Starting from the scalar loss keeps every intermediate a vector rather than a full matrix",
                     "The chain rule requires that order",
                     "It allows parallelism"],
         "answer": 1,
         "why": "Left to right would carry a full matrix at every step. Reverse mode is why a backward pass costs a small multiple of a forward pass at any parameter count."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Convexity
# ---------------------------------------------------------------------------
topic(
    "convexity_and_optimisation",
    "Convexity and Optimisation Landscapes",
    "Calculus",
    "One slider turns a bowl into a mountain range. Watch gradient descent "
    "succeed, then watch the same algorithm get stuck.",
    _svg('<path d="M18 26 C 40 74, 56 40, 74 62 C 92 78, 104 34, 142 28" fill="none" stroke="%s" stroke-width="2"/>' % A
         + _dot(74, 62, A, 3.6) + _dot(40, 62, M, 3)
         + _txt(80, 84, "which minimum you find", M, 7)),
    {
        "demo": "convexity",
        "controls": [
            {"key": "bumpiness", "label": "Bumpiness (0 = convex)", "type": "range",
             "min": 0.0, "max": 0.8, "step": 0.02, "value": 0.35},
            {"key": "start", "label": "Starting point", "type": "range",
             "min": -4.5, "max": 4.5, "step": 0.1, "value": 3.4},
            {"key": "lr", "label": "Learning rate", "type": "range",
             "min": 0.02, "max": 0.6, "step": 0.01, "value": 0.12},
        ],
    },
    [
        "A function is <strong>convex</strong> if the straight line between any "
        "two points on it never dips below the curve.",
        "Convex means every local minimum is the global minimum. There is "
        "nowhere to get stuck.",
        "Set bumpiness to zero and every starting point finds the same answer. "
        "Raise it and the starting point decides.",
        "Neural network losses are wildly non-convex, and train well anyway "
        "&mdash; which needed explaining, and largely has been.",
    ],
    """
title: Convexity and Optimisation Landscapes
intro: The property that makes optimisation easy, what happens without it, and why deep learning works regardless.

## The definition

A function is **convex** if, for any two points on it, the straight line
joining them lies on or above the curve. A bowl is convex. A mountain range is
not.

The equivalent statement in calculus: the second derivative is non-negative
everywhere. In many dimensions, the [Hessian](jacobian_and_hessian.html) is
positive semi-definite &mdash; all its eigenvalues at least zero.

## Why it matters so much

One consequence carries the entire subject: **in a convex function, every local
minimum is the global minimum.**

If you find a point where the gradient is zero and the curvature is positive,
you are done. Not "probably done" &mdash; done, with a proof.

Set the bumpiness control to zero and try every starting point on the slider.
Every one converges to the same place. The initialisation does not matter, the
run is reproducible, and there is a guarantee at the end of it.

Now raise bumpiness. The curve grows local minima, and the starting point
starts deciding the answer. Move the start slider at a fixed bumpiness and
watch the final position jump between basins &mdash; same function, same
algorithm, same learning rate, different answer.

## What convexity buys, concretely

**Guaranteed convergence** to the global optimum, with known rates.

**Reproducibility.** No dependence on initialisation or on the order the data
arrived in.

**Certificates.** You can prove a solution is optimal rather than hoping.

**Reliable stopping.** A small gradient really does mean you have arrived.

This is why linear regression, logistic regression, SVMs with convex loss,
ridge and lasso are all so well behaved. Their objectives are convex, and the
solvers come with theory rather than folklore.

## And yet deep learning works

Neural network losses are about as non-convex as functions get: millions of
dimensions, vast numbers of stationary points, no guarantees at all. By the
argument above, training should be a lottery.

It is not, and the explanation that emerged is worth knowing.

**Saddle points, not local minima, dominate.** In high dimensions, a stationary
point needs *every* eigenvalue of the Hessian to be positive to be a local
minimum. With millions of dimensions that is vanishingly unlikely; almost every
stationary point has some negative direction, making it a saddle. Saddles are
escapable &mdash; the gradient points away along the negative direction, and
noise from mini-batching helps you find it.

**The minima that exist are mostly similar.** Empirically, the many minima of a
large network reach comparable loss. Which one you land in matters less than
the fact that you landed.

**Overparameterisation flattens the landscape.** Wider networks have more paths
down, and the loss surface becomes easier rather than harder as capacity grows
&mdash; which is the opposite of the intuition.

## The learning rate

The third control demonstrates a separate failure that is often blamed on
non-convexity.

Turn the learning rate up with bumpiness at zero &mdash; a perfectly convex
bowl &mdash; and descent still misbehaves, bouncing between the walls or
diverging entirely. Convexity guarantees a unique minimum exists; it does not
guarantee your step size will find it.

The safe step depends on curvature, which is what
[the Hessian](jacobian_and_hessian.html) measures and what adaptive optimisers
estimate.

## Where it goes wrong

**Assuming a convex loss makes the whole problem convex.** Squared error is
convex in the predictions and non-convex in the weights of a network. What
matters is convexity in the parameters being optimised.

**Blaming non-convexity for a divergent run.** Check the learning rate first;
it is usually that.

**Running once and trusting the result on a non-convex problem.** Several
starts, or a schedule with restarts, is the minimum diligence.

**Expecting convex theory to transfer.** Convergence rates for convex problems
say nothing about a deep network.
""",
    [
        {"q": "What is the defining consequence of convexity for optimisation?",
         "options": ["The gradient is always positive",
                     "Every local minimum is the global minimum",
                     "The function has one input",
                     "Gradient descent converges in one step"],
         "answer": 1,
         "why": "Find a stationary point with positive curvature and you are done, with a proof. That is why linear and logistic regression are so well behaved."},
        {"q": "Why are saddle points more common than local minima in high dimensions?",
         "options": ["Gradients are larger there",
                     "A local minimum needs every Hessian eigenvalue positive, which is vanishingly unlikely across millions of dimensions",
                     "Saddle points attract gradient descent",
                     "Local minima require convexity"],
         "answer": 1,
         "why": "Almost every stationary point has some negative direction, making it escapable - and mini-batch noise helps find that direction."},
        {"q": "Descent diverges on a perfectly convex bowl. What is the likely cause?",
         "options": ["The function is secretly non-convex",
                     "The learning rate is too large for the curvature",
                     "The starting point is wrong",
                     "There are several minima"],
         "answer": 1,
         "why": "Convexity guarantees a unique minimum exists; it says nothing about whether your step size will find it. The safe step depends on curvature."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Taylor series
# ---------------------------------------------------------------------------
topic(
    "taylor_series",
    "Taylor Series",
    "Calculus",
    "Approximate any smooth curve by a polynomial that agrees with it at one "
    "point. Add terms and watch the agreement spread.",
    _svg('<path d="M18 60 C 44 24, 62 24, 80 44 C 98 64, 116 64, 142 34" fill="none" stroke="%s" stroke-width="2"/>' % M
         + '<path d="M18 78 C 44 30, 62 26, 80 44 C 98 62, 112 74, 142 88" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + _dot(80, 44, A, 3.6)
         + _txt(80, 84, "exact here, drifting away", M, 7)),
    {
        "demo": "taylor",
        "controls": [
            {"key": "fn", "label": "Function", "type": "select", "value": "sin",
             "options": [{"value": "sin", "label": "sin(x)"},
                         {"value": "exp", "label": "exp(x)"},
                         {"value": "runge", "label": "1 / (1 + x squared)"}]},
            {"key": "terms", "label": "Terms kept", "type": "range",
             "min": 0, "max": 8, "step": 1, "value": 5},
            {"key": "about", "label": "Expand about x =", "type": "range",
             "min": -3, "max": 3, "step": 0.25, "value": 0},
        ],
    },
    [
        "The series matches the function's value, then its slope, then its "
        "curvature, then the rate of change of curvature, and so on.",
        "Each term buys accuracy <em>near the expansion point</em>. None of them "
        "buys accuracy far from it.",
        "One term is a constant. Two is the tangent line. Three is the "
        "quadratic every optimiser secretly uses.",
        "Move the expansion point and the region of agreement moves with it. "
        "It is a local statement, always.",
    ],
    """
title: Taylor Series
intro: Replacing a hard function with a polynomial, and being precise about where that is allowed.

## The construction

Pick a point. Build a polynomial that agrees with the function there, then also
agrees with its slope, then its curvature, then the next derivative, and so on.

```
f(x)  ~  f(a) + f'(a)(x-a) + f''(a)(x-a)^2/2! + f'''(a)(x-a)^3/3! + ...
```

Each term pins down one more derivative at `a`. The factorials are there
because differentiating `(x-a)^k` repeatedly produces `k!`, and dividing by it
cancels exactly.

Set the terms control to 0 and step it upward. At 0 you have a horizontal line
at the right height. At 1, the tangent. At 2, a parabola that also has the
right bend. Each step hugs the curve a little further out.

## Local, and only local

The readout gives how far the approximation stays within 0.1 of the truth, and
this is the number worth watching.

More terms extend the range. They do not make it infinite, and the extension
gets slower. The polynomial agrees perfectly at the expansion point and gets
worse with distance, always &mdash; the whole construction is built from
information at a single point, so it cannot know anything about elsewhere.

Move the expansion point and the region of agreement moves with it. That is the
right mental model: a Taylor series is a statement about a neighbourhood.

## Where it earns its keep

**Second-order optimisation.** Newton's method is exactly the two-term
expansion of the loss: approximate it as a quadratic near the current point,
jump to that quadratic's minimum, repeat. Everything in
[the Hessian module](jacobian_and_hessian.html) is this idea.

**Small-angle approximations.** `sin(x) ~ x` for small `x` is the one-term
expansion, and it is why pendulum equations are solvable at all.

**Backpropagation's justification.** The chain rule is exact, but the argument
that a small weight change produces a proportional loss change is a first-order
expansion.

**Numerical methods.** Finite differences, Runge-Kutta integrators and most
error bounds are derived by expanding and discarding.

**exp, log, sin in a standard library.** Not looked up in a table; evaluated
from a truncated series with a range reduction in front of it.

## Where it fails

Switch the function control to `1 / (1 + x squared)`.

This function is smooth everywhere on the real line &mdash; no kinks, no
asymptotes, differentiable as many times as you like. Yet expand it about 0 and
add terms, and beyond about x = 1 the approximation does not merely fail to
improve; it gets **worse** with every term added.

The reason is invisible from the real line. Viewed over the complex numbers the
function has poles at *i* and *&minus;i*, distance 1 from the origin, and the
radius of convergence is the distance to the nearest singularity wherever it
sits. That radius is 1, and no number of real terms escapes it.

This is the Runge phenomenon, and its lesson is practical: **smooth on the reals
does not mean a Taylor series converges everywhere.** Adding terms is not
always progress.

## Where it goes wrong

**Extrapolating far from the expansion point.** The error grows with distance,
and past the radius of convergence it grows without bound.

**Assuming more terms is always better.** Not past the radius, and not
numerically &mdash; high-order terms involve large factorials and cancelling
quantities, which loses precision in floating point.

**Expanding about the wrong point.** Expand about where you will evaluate. A
series about 0 is the wrong tool for estimating at x = 5.

**Forgetting smoothness is required.** The function needs derivatives of every
order at the expansion point. `|x|` has none at 0, so there is no series there.
""",
    [
        {"q": "What does the second term of a Taylor series give you?",
         "options": ["The value at the point", "The tangent line",
                     "The curvature", "The radius of convergence"],
         "answer": 1,
         "why": "One term is a constant at the right height; two is the tangent; three is the quadratic that also has the right bend - which is what Newton's method optimises."},
        {"q": "Why does the series for 1/(1+x^2) stop improving beyond x = 1?",
         "options": ["The function is not smooth there",
                     "It has complex poles at distance 1 from the origin, which sets the radius of convergence",
                     "Floating point runs out of precision",
                     "The derivatives become zero"],
         "answer": 1,
         "why": "The function is perfectly smooth on the real line. The radius is the distance to the nearest singularity wherever it sits, including off the real line."},
        {"q": "A Taylor series is a statement about:",
         "options": ["The whole function", "A neighbourhood of the expansion point",
                     "The function's maximum", "Its integral"],
         "answer": 1,
         "why": "It is built entirely from derivatives at one point, so it cannot know anything about elsewhere. Move the expansion point and the region of agreement moves with it."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Expectation and variance
# ---------------------------------------------------------------------------
topic(
    "expectation_and_variance",
    "Expectation and Variance",
    "Probability",
    "Load a die face by face and watch the two numbers that summarise any "
    "random quantity move.",
    _svg("".join(_box(22 + i * 21, 66 - h, 15, h, fill=S, stroke=B, sw=1)
                 for i, h in enumerate([12, 14, 16, 18, 20, 34]))
         + _line(112, 18, 112, 70, A, 1.6, "4 3")
         + _txt(80, 84, "the balance point", M, 7)),
    {
        "demo": "expectation",
        "controls": [
            {"key": "w1", "label": "Weight on 1", "type": "range",
             "min": 0, "max": 6, "step": 1, "value": 1},
            {"key": "w2", "label": "Weight on 2", "type": "range",
             "min": 0, "max": 6, "step": 1, "value": 1},
            {"key": "w3", "label": "Weight on 3", "type": "range",
             "min": 0, "max": 6, "step": 1, "value": 1},
            {"key": "w4", "label": "Weight on 4", "type": "range",
             "min": 0, "max": 6, "step": 1, "value": 1},
            {"key": "w5", "label": "Weight on 5", "type": "range",
             "min": 0, "max": 6, "step": 1, "value": 1},
            {"key": "w6", "label": "Weight on 6", "type": "range",
             "min": 0, "max": 6, "step": 1, "value": 3},
        ],
    },
    [
        "<strong>Expectation</strong> is the probability-weighted average: "
        "<code class='mono-font'>E[X] = &Sigma; x &middot; P(x)</code>.",
        "It is a balance point, not a prediction. A fair die has E[X] = 3.5, "
        "a value it can never roll.",
        "<strong>Variance</strong> is the expected squared distance from the "
        "mean: <code class='mono-font'>E[(X &minus; &mu;)&sup2;]</code>.",
        "Expectation is linear no matter what. Variance only adds across "
        "<em>independent</em> variables &mdash; a distinction that matters constantly.",
    ],
    """
title: Expectation and Variance
intro: The two numbers that summarise a random quantity, and the rules for combining them.

## Expectation

The **expectation** of a random variable is each value it can take, weighted by
how likely that value is:

```
E[X]  =  sum over x of  x * P(X = x)
```

The [mean, mode and median module](mean_mode_and_median.html) covers the mean
of a dataset you have. This is the mean of a distribution you have not sampled
&mdash; what the average would settle to given enough draws.

Load the die above and watch E[X] move. Put all the weight on 6 and it becomes
6. Spread it evenly and it becomes 3.5.

3.5 is the case worth pausing on: a fair die has expectation 3.5, and no die
has ever rolled a 3.5. **The expectation is a balance point, not a
prediction.** The distribution would balance on a pin at that value, and that
is all the word means.

## Variance

Expectation alone says nothing about spread. Two very different dice can share
one. **Variance** measures the spread:

```
Var(X)  =  E[(X - mu)^2]
```

The expected squared distance from the mean. Squaring is what stops the
positive and negative deviations cancelling, and it is why the units come out
squared &mdash; variance of a height in metres is in metres squared, which is
meaningless as a length. Taking the square root gives the **standard
deviation**, back in the original units, which is why that is the number
usually reported.

The identity worth memorising is:

```
Var(X)  =  E[X^2] - (E[X])^2
```

The mean of the squares minus the square of the mean. It is how variance is
computed in one pass over data, and it is also the source of a classic
numerical bug: with large values and small variance, the two terms are nearly
equal and subtracting them destroys precision. Welford's algorithm exists to
avoid exactly this.

## Combining them

The rules for expectation are as good as rules get:

```
E[aX + b]   = a E[X] + b
E[X + Y]    = E[X] + E[Y]        always
```

That second line holds **whether or not X and Y are independent**. Linearity of
expectation is unconditional, and it is the reason a surprising number of
counting arguments are one line long.

Variance is stricter:

```
Var(aX + b)  = a^2 Var(X)          note: b vanishes, a is squared
Var(X + Y)   = Var(X) + Var(Y)     only if X and Y are independent
```

Shifting a distribution does not change its spread, which is why `b` disappears.
Scaling by `a` scales the variance by `a`&sup2;, because variance is in squared
units.

The independence condition on the sum is where mistakes live. If X and Y move
together, the covariance term reappears:

```
Var(X + Y) = Var(X) + Var(Y) + 2 Cov(X, Y)
```

The [covariance module](covariance_and_correlation.html) covers that term.

## Where it shows up

**The standard error.** The mean of *n* independent draws has variance
&sigma;&sup2;/n, straight from the rules above. Its square root is
&sigma;/&radic;n, which is the whole content of
[the sampling distribution](sampling_distributions.html).

**Bias-variance decomposition.** Expected squared error splits into bias
squared plus variance plus irreducible noise, using the identity above.

**Portfolio diversification.** Combining assets reduces variance only when they
are not perfectly correlated &mdash; the covariance term again.

**Bagging.** Averaging *n* models reduces variance by *n* only if their errors
are independent, which is why random forests work to decorrelate their trees.

## Where it goes wrong

**Treating the expectation as a likely value.** It need not be attainable at
all.

**Adding variances of correlated variables.** The commonest error in this
material.

**Forgetting the square on the scale factor.** Doubling a variable quadruples
its variance.

**Assuming a variance exists.** Some distributions have none &mdash; the Cauchy
has neither a finite variance nor a finite mean, and sample averages of Cauchy
draws never settle.
""",
    [
        {"q": "A fair die has E[X] = 3.5. What does that tell you?",
         "options": ["3.5 is the most likely roll",
                     "It is the balance point of the distribution, and need not be attainable",
                     "Half the rolls are below 3.5",
                     "The variance is 3.5"],
         "answer": 1,
         "why": "No die has ever rolled a 3.5. The expectation is where the distribution would balance on a pin, not a prediction of any single outcome."},
        {"q": "When does Var(X + Y) = Var(X) + Var(Y)?",
         "options": ["Always",
                     "Only when X and Y are independent",
                     "Only when both are normal",
                     "Only when the means are equal"],
         "answer": 1,
         "why": "Expectation adds unconditionally; variance does not. Otherwise a covariance term appears - which is why diversification and bagging both depend on decorrelation."},
        {"q": "Why is Var(X) = E[X^2] - (E[X])^2 numerically dangerous?",
         "options": ["It needs two passes over the data",
                     "With large values and small variance the two terms nearly cancel, destroying precision",
                     "It can return a negative number in exact arithmetic",
                     "It assumes independence"],
         "answer": 1,
         "why": "It is the one-pass formula, and the subtraction of two nearly equal large numbers is what Welford's algorithm exists to avoid."},
    ],
)


# ---------------------------------------------------------------------------
# 7. Bernoulli, binomial and Poisson
# ---------------------------------------------------------------------------
topic(
    "bernoulli_binomial_poisson",
    "Bernoulli, Binomial and Poisson",
    "Probability",
    "One trial, then n trials, then the limit as n runs away. Three "
    "distributions built from the same coin.",
    _svg("".join(_box(24 + i * 15, 66 - h, 11, h, fill=S, stroke=B, sw=1)
                 for i, h in enumerate([4, 10, 20, 32, 38, 30, 18, 8]))
         + _txt(80, 84, "counts, not measurements", M, 7)),
    {
        "demo": "discrete",
        "controls": [
            {"key": "kind", "label": "Distribution", "type": "select", "value": "binomial",
             "options": [{"value": "bernoulli", "label": "Bernoulli - one trial"},
                         {"value": "binomial", "label": "Binomial - n trials"},
                         {"value": "poisson", "label": "Poisson - the limit"}]},
            {"key": "n", "label": "n (binomial)", "type": "range",
             "min": 1, "max": 60, "step": 1, "value": 20},
            {"key": "p", "label": "p (success probability)", "type": "range",
             "min": 0.02, "max": 0.98, "step": 0.02, "value": 0.30},
            {"key": "lam", "label": "lambda (Poisson rate)", "type": "range",
             "min": 0.5, "max": 20, "step": 0.5, "value": 3.0},
        ],
    },
    [
        "<strong>Bernoulli</strong>: one trial, one parameter. Success with "
        "probability p, failure otherwise.",
        "<strong>Binomial</strong>: how many successes in n independent "
        "Bernoulli trials. Mean np, variance np(1&minus;p).",
        "<strong>Poisson</strong>: the binomial's limit as n grows and p shrinks "
        "with np held fixed. Counts of rare events in a fixed window.",
        "A Poisson has mean and variance both equal to &lambda;. Real count data "
        "is often more spread than that, which is a diagnosis, not a nuisance.",
    ],
    """
title: Bernoulli, Binomial and Poisson
intro: The three distributions behind every count, and how each is built from the one before it.

## Bernoulli: the atom

One trial, two outcomes, one parameter. Success with probability `p`, failure
with probability `1 - p`.

Mean `p`, variance `p(1-p)`. That variance is worth a moment: it is largest at
`p = 0.5` and falls to zero at either end, which says something obvious once
stated &mdash; an event that always happens, or never does, is not random at
all. Drag `p` to 0.02 with Bernoulli selected and watch the variance in the
readout collapse.

Every coin flip, click-or-not, churn-or-not and pass-or-fail is a Bernoulli
trial, and it is the atom the other two are assembled from.

## Binomial: counting the successes

Run `n` independent Bernoulli trials with the same `p` and count the successes.
That count is **binomial**.

```
P(k successes)  =  C(n, k) * p^k * (1-p)^(n-k)
```

The three factors read directly: `p^k` for the successes, `(1-p)^(n-k)` for the
failures, and `C(n, k)` for the number of orders they could have arrived in.

Mean `np`, variance `np(1-p)` &mdash; both straight from
[the rules for combining](expectation_and_variance.html) `n` independent
Bernoulli variables.

Drag `n` upward and the shape becomes recognisably bell-like. That is
[the central limit theorem](central_limit_theorem.html) arriving: a binomial is
a sum of independent variables, so it must tend to normal. It is why the normal
approximation to the binomial exists, and why it needs `np` and `n(1-p)` both
comfortably above about 10 &mdash; near the edges the binomial is skewed and the
symmetric normal fits badly.

**The independence and constant-`p` assumptions are load-bearing.** Ten coin
flips are binomial. Ten cards drawn without replacement are not, because `p`
changes as the deck depletes; that is the hypergeometric distribution.

## Poisson: the limit

Now let `n` grow and `p` shrink together, keeping `np = lambda` fixed. Many
trials, each very unlikely, with a stable expected count.

The binomial converges to the **Poisson**:

```
P(k)  =  e^(-lambda) * lambda^k / k!
```

`n` and `p` have vanished; only their product survives. That is what makes it
useful. You rarely know how many opportunities there were for an event to occur
&mdash; how many people *could* have visited the site this minute &mdash; but
you can measure the rate.

So Poisson models counts in a fixed window: arrivals per minute, defects per
batch, mutations per genome, goals per match.

Set the distribution to Poisson and compare against a binomial with `n = 60`
and `p = 0.05`. Both have mean 3, and the shapes are nearly identical. That is
the limit at work.

## The Poisson's signature, and its trap

A Poisson has **mean and variance both equal to lambda**. One parameter fixes
both, and there is no way to have a Poisson with mean 3 and variance 10.

Real count data very often has variance well above its mean &mdash;
**overdispersion**. Website visits cluster, defects come in bad batches,
accidents cluster around conditions. The Poisson assumes events are independent
and the rate is constant, and clustering violates both.

Overdispersion is a finding, not an annoyance: it says something is varying that
the model treats as fixed. The usual response is a **negative binomial**, which
adds a second parameter and lets the rate itself be random.

## Where they show up

**A/B testing.** Conversions are binomial; the test is about two `p` values.

**Queueing.** Poisson arrivals are the standard assumption behind almost all
queueing theory.

**Rare-event modelling.** Failures, fraud, defects.

**Naive Bayes for text.** Multinomial and Bernoulli variants correspond exactly
to counting words and to noting presence or absence.

**Class imbalance.** A rare positive class is a small `p`, and the variance of
your estimate of it is `p(1-p)/n` &mdash; which is why rare classes need so
much more data before a rate estimate settles.

## Where it goes wrong

**Applying a binomial to sampling without replacement.** `p` changes; use the
hypergeometric.

**Assuming Poisson without checking dispersion.** Compare the sample variance
against the sample mean before anything else.

**Using the normal approximation near p = 0 or 1.** The binomial is skewed
there; the approximation is not.

**Forgetting the fixed window.** A Poisson rate is per unit of something. Double
the window and lambda doubles.
""",
    [
        {"q": "Why is a Bernoulli variance largest at p = 0.5?",
         "options": ["Because the mean is largest there",
                     "An event that always or never happens is not random, so spread must fall to zero at either end",
                     "Because the distribution is symmetric there",
                     "It is not - variance is constant"],
         "answer": 1,
         "why": "p(1-p) peaks at 0.5 and collapses at both extremes, which is the arithmetic saying something obvious about certainty."},
        {"q": "What survives when a binomial becomes a Poisson?",
         "options": ["n only", "p only", "Their product np", "Neither"],
         "answer": 2,
         "why": "n grows and p shrinks with np fixed, and only lambda = np appears in the result. That is what makes Poisson usable when you know the rate but not the number of opportunities."},
        {"q": "Your count data has mean 4 and variance 12. What does that suggest?",
         "options": ["A Poisson fits well",
                     "Overdispersion - events are clustering, violating the constant-rate assumption",
                     "The mean is miscalculated",
                     "The window is too small"],
         "answer": 1,
         "why": "A Poisson forces mean and variance to be equal. Variance well above the mean is a finding: something is varying that the model treats as fixed. A negative binomial adds that second parameter."},
    ],
)


# ---------------------------------------------------------------------------
# 8. The Central Limit Theorem
# ---------------------------------------------------------------------------
topic(
    "central_limit_theorem",
    "The Central Limit Theorem",
    "Probability",
    "Sample from a population that looks nothing like a bell curve. The "
    "averages come out as one anyway.",
    _svg("".join(_box(20 + i * 11, 66 - h, 8, h, fill=S, stroke=B, sw=1)
                 for i, h in enumerate([26, 30, 8, 6, 24, 28, 10]))
         + _txt(52, 84, "population", M, 7)
         + '<path d="M104 66 C 116 66, 118 26, 128 26 C 138 26, 140 66, 150 66" fill="none" stroke="%s" stroke-width="2"/>' % A
         + _txt(128, 84, "its means", M, 7)),
    {
        "demo": "clt",
        "canvases": 2,
        "captions": ["The population - two humps and a tail",
                     "The distribution of its sample means"],
        "controls": [
            {"key": "n", "label": "Sample size n", "type": "range",
             "min": 1, "max": 80, "step": 1, "value": 30},
            {"key": "seed", "label": "Resample", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 12},
        ],
    },
    [
        "The theorem is about the distribution of the <em>sample mean</em>, not "
        "about the population and not about the sample.",
        "Whatever the population's shape, the sample means tend to normal as n "
        "grows &mdash; provided the population has a finite variance.",
        "The spread of the means is <code class='mono-font'>&sigma;/&radic;n</code>, "
        "which is why quadrupling n only halves the uncertainty.",
        "At n = 1 the means are just the population. Drag n up and watch the "
        "shape reorganise itself.",
    ],
    """
title: The Central Limit Theorem
intro: Why the normal distribution turns up everywhere, stated precisely enough to know when it does not.

## What the theorem says

Take repeated samples of size `n` from any population with a finite mean and
variance. Compute each sample's mean. Those means have a distribution of their
own, and as `n` grows it approaches a normal distribution &mdash; with mean
equal to the population mean and standard deviation `sigma / sqrt(n)`.

The population's own shape does not appear in that statement anywhere. It can
be skewed, bimodal, discrete, or wildly irregular.

The population above is deliberately unpleasant: two separate humps and a long
tail. Nothing about it is bell-shaped. Set `n` to 1 and the right-hand panel is
that same shape, because a sample of one *is* a draw from the population.

Now drag `n` upward. By 5 the two humps have merged. By 30 the right-hand panel
is a clean bell, and the fitted normal curve sits on top of the resampled
histogram. Nothing about the population changed.

## Three things it is not

**Not "large samples are normally distributed."** The sample is not normal; it
looks like the population, because that is what it is drawn from. It is the
*mean* that goes normal.

**Not "everything is normal."** Heights are roughly normal because they are the
sum of many small independent influences. Incomes are not normal and no amount
of data makes them so.

**Not a licence to ignore the population.** It describes the sampling
distribution of a statistic, not the data.

## The square root

The standard deviation of the sample mean &mdash; the **standard error** &mdash;
is `sigma / sqrt(n)`. The square root is the practical heart of the theorem.

To halve your uncertainty you must **quadruple** your sample. To divide it by
ten you need a hundred times the data. Precision gets expensive fast, and this
single fact governs how large a survey has to be, how long an A/B test must run
and why polls stubbornly report margins of around three percent.

[The sampling distribution module](sampling_distributions.html) plots that decay
directly.

## How large is large enough

The usual rule of thumb is `n = 30`, and like all such rules it is a summary of
something more specific.

**Near-symmetric population**: convergence is fast, and 10 may do.

**Strongly skewed**: 30 is not enough. Heavily skewed populations can need
hundreds before the mean is convincingly normal.

**Heavy tails**: worse still, and there is a limit case below.

The honest procedure is the one on this page: resample and look. Drag `n` and
find where the histogram stops looking lumpy for *your* population.

## When it fails outright

The theorem requires a **finite variance**, and that condition is not decorative.

The Cauchy distribution has none &mdash; nor a finite mean. Average `n` Cauchy
draws and you get another Cauchy, with exactly the same spread as one draw. No
amount of averaging concentrates anything. The sample mean of a million draws is
no better than the first.

Heavy-tailed distributions that do have a finite variance still converge, but
slowly enough to matter. Financial returns are the standard cautionary example:
methods that assume normality of averages understate the chance of extreme
outcomes, because convergence has not really happened at the sample sizes in
use.

## Where it shows up

**Confidence intervals and t-tests** assume the sampling distribution of the
mean is normal. That assumption is this theorem.

**A/B testing**: a conversion rate is a mean of Bernoulli draws.

**Bootstrapping** exists partly to avoid needing it when it does not hold.

**Measurement error** is often modelled as normal because it is the sum of many
small independent errors.

## Where it goes wrong

**Applying it to the data instead of the statistic.** Extremely common.

**Trusting n = 30 on skewed data.** Check.

**Assuming it applies to the maximum or the variance.** It is about sums and
means. Extreme values have their own limit theory, and a different family of
limiting distributions.

**Ignoring dependence.** The classical version needs independent draws. Time
series data usually is not independent, and the effective sample size is
smaller than the count.
""",
    [
        {"q": "What exactly becomes normal?",
         "options": ["The population", "The sample",
                     "The distribution of the sample mean across repeated samples",
                     "The variance"],
         "answer": 2,
         "why": "The sample looks like the population, because that is what it is drawn from. It is the mean that goes normal, and the population's shape does not appear in the statement."},
        {"q": "You want to halve your uncertainty about a mean. What must you do?",
         "options": ["Double the sample", "Quadruple the sample",
                     "Halve the sample", "Nothing - it is fixed by the population"],
         "answer": 1,
         "why": "The standard error is sigma over root n. That square root is why precision gets expensive and why polls stubbornly report margins of about three percent."},
        {"q": "For which population does the theorem fail entirely?",
         "options": ["A bimodal one", "A skewed one",
                     "A Cauchy distribution, which has no finite variance", "A discrete one"],
         "answer": 2,
         "why": "Average n Cauchy draws and you get another Cauchy with the same spread as one draw. Bimodal and skewed populations converge - just more slowly."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Quantiles and percentiles
# ---------------------------------------------------------------------------
topic(
    "quantiles_and_percentiles",
    "Quantiles and Percentiles",
    "Statistics",
    "Cut a distribution into equal-sized groups. The box plot is what you get "
    "when you draw the cuts.",
    _svg(_line(24, 46, 46, 46, M, 1.6) + _line(112, 46, 138, 46, M, 1.6)
         + _box(46, 34, 66, 24, fill=S, stroke=A, sw=1.6)
         + _line(74, 34, 74, 58, A, 2.4)
         + _dot(142, 46, A, 3)
         + _txt(80, 78, "median, quartiles, whiskers", M, 7)),
    {
        "demo": "quantiles",
        "canvases": 2,
        "captions": ["The sample, with the three quartiles marked",
                     "The same thing as a box plot"],
        "controls": [
            {"key": "n", "label": "Sample size", "type": "range",
             "min": 20, "max": 600, "step": 20, "value": 200},
            {"key": "seed", "label": "Resample", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 7},
        ],
    },
    [
        "The <strong>q-th quantile</strong> is the value below which a fraction "
        "q of the data falls. The median is q = 0.5.",
        "<strong>Percentiles</strong> are the same thing on a 0-100 scale. "
        "Quartiles cut at 25, 50 and 75.",
        "The <strong>IQR</strong> is Q3 &minus; Q1: the range covering the "
        "middle half, and a spread measure that ignores outliers entirely.",
        "Whiskers reach the furthest points within 1.5 IQR of the box. Anything "
        "beyond is drawn individually &mdash; a convention, not a test.",
    ],
    """
title: Quantiles and Percentiles
intro: Describing a distribution by where its values sit rather than by averaging them.

## The definition

The **q-th quantile** is the value below which a fraction `q` of the data falls.
The 0.5 quantile is the median: half below, half above. The 0.9 quantile is the
value 90% of the data sits below.

**Percentiles** are the same idea on a 0&ndash;100 scale &mdash; the 90th
percentile is the 0.9 quantile. **Quartiles** cut at 25, 50 and 75, dividing the
data into four equal groups. **Deciles** cut into ten.

## Why not just use the mean

A mean is a balance point, and it moves when anything moves. A quantile depends
only on **order**, and that makes it robust.

Add a single enormous value to a dataset and the mean shifts, possibly a lot.
The median barely moves at all &mdash; the new value is simply "one more above
the middle", regardless of how far above.

That is why median income is reported rather than mean income, why latency is
reported at percentiles, and why the [box plot](#) below exists.

The **IQR** &mdash; Q3 minus Q1 &mdash; is the spread measure that follows from
the same idea. It covers the middle half of the data, and it is unaffected by
anything in the tails. Standard deviation, being built from squared distances
from the mean, is the opposite: one extreme value moves it substantially.

## Reading the box plot

The second panel is assembled from the quartiles in the first, and every part
of it has a definition:

**The box** spans Q1 to Q3, so it contains the middle 50% of the data.

**The line inside** is the median. Its position within the box shows skew: off
centre means the distribution leans.

**The whiskers** reach the furthest data points still within 1.5 &times; IQR of
the box edge.

**The dots** are everything beyond that.

The 1.5 is a **convention**, not a test. It comes from Tukey, and for a normal
distribution it flags about 0.7% of points. Points beyond it are worth
inspecting, and calling them "outliers" makes a claim the rule cannot support
&mdash; a skewed distribution produces them by construction rather than by
error.

Increase the sample size and the number of flagged points grows roughly in
proportion. That alone shows the rule is descriptive.

## Percentiles in practice

**Latency.** Nobody reports mean response time, because one slow request buried
in a million is invisible in a mean and obvious at p99. Services are specified
at p50, p95, p99 and p999 precisely because the tail is what users notice.

A trap follows immediately: **percentiles do not average.** The p99 of two
servers is not the mean of their p99s. Aggregating percentiles requires the
underlying distributions or a structure like a t-digest.

**Quantile regression** predicts a chosen quantile rather than the mean. Useful
when the cost of over- and under-prediction differ, or when you want a
prediction interval directly.

**Quantile binning** turns a continuous feature into equal-sized buckets, which
is robust to skew in a way that equal-width binning is not.

**Feature scaling.** `QuantileTransformer` maps a feature to a uniform or normal
distribution through its quantiles, and is unaffected by outliers in a way
standardisation is not.

## A wrinkle worth knowing

There is no single agreed definition of a sample quantile. With 10 data points,
"the value below which 25% falls" does not land on an observation, and there are
several defensible interpolations. NumPy offers nine methods; R offers the same
nine; the defaults differ between languages, and between `numpy.percentile` and
some SQL engines.

For large samples the differences are negligible. For small ones they are not,
and two tools can legitimately report different quartiles for identical data.

## Where it goes wrong

**Averaging percentiles.** The single most common error, and it always
understates the tail.

**Reading whisker points as errors.** The rule is a drawing convention.

**Comparing box plots of very different sample sizes.** More data means more
flagged points, mechanically.

**Assuming your language's default matches another's.** State the method when it
matters.
""",
    [
        {"q": "Why is the median unaffected by adding one enormous value?",
         "options": ["It is recomputed from the mean",
                     "It depends only on order, so a new extreme value is just 'one more above the middle'",
                     "Outliers are removed first",
                     "It uses the IQR"],
         "answer": 1,
         "why": "A mean is a balance point and moves when anything moves. That robustness is why median income is reported rather than mean income."},
        {"q": "What do the whiskers on a box plot reach?",
         "options": ["The minimum and maximum",
                     "The furthest points within 1.5 times the IQR of the box",
                     "Two standard deviations",
                     "The 5th and 95th percentiles"],
         "answer": 1,
         "why": "The 1.5 is a Tukey convention, not a test. For a normal distribution it flags about 0.7% of points, and a skewed distribution produces them by construction."},
        {"q": "Why can you not average the p99 of two servers?",
         "options": ["The samples are different sizes",
                     "Percentiles are not linear - aggregating them needs the underlying distributions",
                     "p99 is not a percentile",
                     "The servers are not independent"],
         "answer": 1,
         "why": "It is the commonest error in latency reporting and it always understates the tail. Structures like t-digest exist to aggregate quantiles properly."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Sampling distributions and standard error
# ---------------------------------------------------------------------------
topic(
    "sampling_distributions",
    "Sampling Distributions and Standard Error",
    "Statistics",
    "A statistic computed from a sample is itself random. Its spread has a "
    "name, a formula, and a square root that governs every survey ever run.",
    _svg('<path d="M20 68 C 46 68, 50 22, 72 22 C 94 22, 98 68, 124 68" fill="none" stroke="%s" stroke-width="2"/>' % A
         + _line(72, 20, 72, 70, M, 1, "3 3")
         + _line(52, 74, 92, 74, M, 1.4)
         + _txt(80, 86, "how far the estimate wanders", M, 7)),
    {
        "demo": "sampling",
        "canvases": 2,
        "captions": ["The sample means, resampled many times",
                     "How the standard error falls with n"],
        "controls": [
            {"key": "n", "label": "Sample size n", "type": "range",
             "min": 4, "max": 200, "step": 4, "value": 32},
            {"key": "reps", "label": "Samples drawn", "type": "range",
             "min": 100, "max": 2000, "step": 100, "value": 800},
            {"key": "seed", "label": "Resample", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 5},
        ],
    },
    [
        "A <strong>sampling distribution</strong> is the distribution of a "
        "statistic across every sample you could have drawn.",
        "The <strong>standard error</strong> is its standard deviation. For a "
        "mean it is <code class='mono-font'>&sigma;/&radic;n</code>.",
        "Standard deviation describes the <em>data</em>. Standard error "
        "describes an <em>estimate</em>. They are not interchangeable.",
        "The right-hand curve is why precision is expensive: it flattens, and "
        "every further gain costs four times the data.",
    ],
    """
title: Sampling Distributions and Standard Error
intro: The idea that makes every confidence interval and every p-value mean something.

## The statistic is random too

You draw a sample and compute its mean. Draw a different sample and you get a
different mean. The statistic is itself a random quantity, and it has a
distribution: the **sampling distribution**.

This is the conceptual step everything in inference rests on. It is also the one
that is easy to skip, because in practice you only ever draw one sample and
never see the distribution at all &mdash; you reason about what *would* happen
across the samples you did not take.

The left panel makes it visible by actually doing it: 800 samples drawn, each
mean plotted. That histogram is the sampling distribution of the mean, and it is
the object confidence intervals describe.

## Standard error

The standard deviation of a sampling distribution is the **standard error**. For
a sample mean:

```
SE  =  sigma / sqrt(n)
```

This follows directly from the [rules for
variance](expectation_and_variance.html): the variance of a sum of `n`
independent draws is `n * sigma^2`, dividing by `n` to make the mean scales
variance by `1/n^2`, leaving `sigma^2 / n`, and the square root gives the
formula.

Watch the readout as you drag `n`: the observed spread of the 800 means tracks
the predicted `sigma / sqrt(n)` closely. That is not a coincidence being
illustrated &mdash; it is an identity being checked.

## Standard deviation is not standard error

These get confused constantly, and the distinction is not subtle.

**Standard deviation** describes the spread of the **data**. It is a property of
the population, and collecting more data does not reduce it &mdash; more careful
measurement might, but more measurements will not.

**Standard error** describes the spread of an **estimate**. It shrinks as `n`
grows, because a larger sample pins the estimate down better.

A useful test: if the number would change when you collect more data *of the
same kind*, it is a standard error. If it would not, it is a standard deviation.

An error bar on a chart could be either, and the two say completely different
things. Charts that do not label which are unreadable.

## The square root, again

The right-hand panel plots `sigma / sqrt(n)` against `n`, and its shape is the
practical content of this page.

It falls steeply at first &mdash; going from 4 samples to 16 halves the error.
Then it flattens. Going from 100 to 400 halves it again, at the cost of three
hundred more observations.

**Every halving of uncertainty costs four times the data.** That is why national
polls settle around 1,000 respondents: the marginal precision per person
collapses past that point, and the remaining error is dominated by sampling bias
rather than sampling noise anyway.

More data cannot fix a biased sample. A poll of 100,000 people who all answer
the same badly-worded question is precisely wrong.

## Beyond the mean

Every statistic has a sampling distribution, not only the mean. Medians,
variances, correlations and regression coefficients all have one, and the
formulas are usually harder or unavailable.

**The bootstrap** exists for exactly this. Resample your data with replacement,
recompute the statistic, repeat thousands of times, and the spread of the
results estimates the sampling distribution &mdash; with no formula and almost
no assumptions. It is the same operation this page performs, run on your own
sample instead of on a known population.

## Where it shows up

**Confidence intervals** are built directly from the standard error.

**t-tests and z-tests** compare an observed difference against the standard
error of that difference.

**Cross-validation** variance is the sampling distribution of a performance
estimate, which is why a single fold's accuracy is a point with error bars
around it.

**A/B test duration** is a standard error calculation before it is anything
else.

## Where it goes wrong

**Reporting SD when you mean SE, or the reverse.** Label your error bars.

**Assuming independence.** The `sqrt(n)` assumes independent draws. Clustered or
time-series data has a smaller effective `n`.

**Treating a large sample as accurate.** It is precise. Accuracy is a separate
question, and bias does not shrink with `n`.

**Using the formula for statistics that do not have one.** Bootstrap instead.
""",
    [
        {"q": "What is a sampling distribution?",
         "options": ["The distribution of the data in one sample",
                     "The distribution of a statistic across all the samples you could have drawn",
                     "The distribution of the population",
                     "The distribution of the residuals"],
         "answer": 1,
         "why": "You only ever draw one sample, so you reason about what would happen across the samples you did not take. It is the object a confidence interval describes."},
        {"q": "Which shrinks as you collect more data?",
         "options": ["The standard deviation of the population",
                     "The standard error of the estimate",
                     "Both", "Neither"],
         "answer": 1,
         "why": "SD describes the data and is a property of the population. SE describes an estimate. If the number would change when you collect more data of the same kind, it is a standard error."},
        {"q": "Why do national polls settle around 1,000 respondents?",
         "options": ["It is a legal requirement",
                     "The sqrt(n) curve flattens, so further precision costs four times the data and bias dominates anyway",
                     "Larger samples become biased",
                     "The central limit theorem requires it"],
         "answer": 1,
         "why": "Every halving of uncertainty costs four times the data. Past that point the remaining error is dominated by sampling bias, which more data cannot fix."},
    ],
)

CHECKS = {"maths/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS}
