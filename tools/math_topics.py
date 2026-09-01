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

## Same vector, three different bases

Coordinates only mean something relative to a basis. Here one fixed vector is written in three of them, and an orthonormal basis makes the arithmetic trivial.

```python-run
import numpy as np

v = np.array([5.0, 3.0])

bases = {
    "standard  e1,e2":     np.array([[1.0, 0.0], [0.0, 1.0]]),
    "sheared (non-orth.)": np.array([[1.0, 0.0], [1.0, 1.0]]),
    "rotated 45 (orthon.)": np.array([[1, 1], [-1, 1]]) / np.sqrt(2),
}

for name, B in bases.items():
    # columns of B are the basis vectors; solve B @ coords = v
    coords = np.linalg.solve(B, v)
    print("%-22s coords %s   rebuilt %s"
          % (name, np.round(coords, 4), np.round(B @ coords, 4)))
print()

B = bases["rotated 45 (orthon.)"]
print("orthonormal means B.T @ B is the identity:")
print(np.round(B.T @ B, 10))
print()
print("so the coordinates are just dot products -- no solve needed:")
print("  solve      ", np.round(np.linalg.solve(B, v), 6))
print("  B.T @ v    ", np.round(B.T @ v, 6))
print()
print("span: two vectors that point the same way span only a line.")
for pair, label in (([[1, 0], [0, 1]], "independent"),
                    ([[1, 2], [2, 4]], "one is twice the other")):
    M = np.array(pair, dtype=float)
    print("  %-24s rank %d -> spans %dD"
          % (label, np.linalg.matrix_rank(M), np.linalg.matrix_rank(M)))
```

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

## Rebuild a matrix from its biggest pieces

SVD splits any matrix into a stack of rank-one layers ordered by importance. Keeping only the first few is what compression and PCA actually do.

```python-run
import numpy as np

rng = np.random.default_rng(0)
# a matrix that is really rank 2, with a little noise on top
A = np.outer(rng.normal(size=40), rng.normal(size=25)) * 5.0
A += np.outer(rng.normal(size=40), rng.normal(size=25)) * 2.0
A += rng.normal(size=(40, 25)) * 0.05

U, s, Vt = np.linalg.svd(A, full_matrices=False)

print("A is %d x %d" % A.shape)
print("first 8 singular values:", np.round(s[:8], 4))
print()
print("each is the 'size' of one rank-one layer. two are large, the rest are noise.")
print()
total = (s ** 2).sum()
print("%5s %14s %14s %12s" % ("k", "kept variance", "reconstr. err", "numbers stored"))
for k in (1, 2, 3, 5, 10, 25):
    Ak = (U[:, :k] * s[:k]) @ Vt[:k]
    kept = (s[:k] ** 2).sum() / total
    err = np.linalg.norm(A - Ak) / np.linalg.norm(A)
    stored = k * (A.shape[0] + A.shape[1] + 1)
    print("%5d %13.4f%% %14.6f %12d" % (k, 100 * kept, err, stored))
print("%5s %13s %14s %12d" % ("full", "100%", "0", A.size))
print()
print("k=2 stores %d numbers instead of %d and loses almost nothing."
      % (2 * (40 + 25 + 1), A.size))
print()
print("singular values are never negative, and U and V are orthonormal:")
print("  U.T @ U close to I:", np.allclose(U.T @ U, np.eye(U.shape[1])))
print("  V.T @ V close to I:", np.allclose(Vt @ Vt.T, np.eye(Vt.shape[0])))
```

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

## First derivatives in a grid, second derivatives in another

The Jacobian collects every first partial derivative of a vector function; the Hessian collects every second partial of a scalar one. Both are built here numerically and checked against the closed form.

```python-run
import numpy as np

# f: R^2 -> R^3
def f(v):
    x, y = v
    return np.array([x ** 2 * y, 5 * x + np.sin(y), x * y ** 3])

def jacobian(fn, v, h=1e-6):
    base = fn(v)
    cols = []
    for i in range(len(v)):
        step = np.zeros_like(v); step[i] = h
        cols.append((fn(v + step) - base) / h)
    return np.column_stack(cols)

p = np.array([2.0, 1.0])
print("Jacobian of f at (2, 1) -- 3 outputs by 2 inputs")
print(np.round(jacobian(f, p), 4))
print()
x, y = p
print("by hand:")
print(np.round(np.array([[2 * x * y, x ** 2],
                         [5.0,       np.cos(y)],
                         [y ** 3,    3 * x * y ** 2]]), 4))
print()

# g: R^2 -> R
def g(v):
    x, y = v
    return x ** 3 + 2 * x * y ** 2 + y ** 3

def hessian(fn, v, h=1e-4):
    n = len(v)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a, b = np.zeros(n), np.zeros(n)
            a[i] = h; b[j] = h
            H[i, j] = (fn(v + a + b) - fn(v + a) - fn(v + b) + fn(v)) / (h * h)
    return H

H = hessian(g, p)
print("Hessian of g at (2, 1)")
print(np.round(H, 3))
print("it is symmetric:", np.allclose(H, H.T, atol=1e-3))
print()
print("its eigenvalues say what kind of point this is:")
print("  eigenvalues", np.round(np.linalg.eigvalsh(H), 4))
print("  all positive -> a bowl (local minimum)")
print("  all negative -> a dome (local maximum)")
print("  mixed signs  -> a saddle, which is what most 'stuck' training is")
```

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

## One function gradient descent cannot fail on, and one it can

The same optimiser, the same settings, run from many starting points on a convex function and then on a bumpy one. Convexity is the property that makes the starting point irrelevant.

```python-run
import numpy as np

def descend(f, grad, x0, lr=0.05, steps=2000):
    x = float(x0)
    for _ in range(steps):
        x -= lr * grad(x)
    return x

# convex: one bowl
f1    = lambda x: (x - 3.0) ** 2 + 2.0
grad1 = lambda x: 2 * (x - 3.0)

# non-convex: a bowl with ripples
f2    = lambda x: 0.15 * (x - 3.0) ** 2 + 3.0 * np.sin(2.0 * x)
grad2 = lambda x: 0.30 * (x - 3.0) + 6.0 * np.cos(2.0 * x)

starts = [-10.0, -5.0, -1.0, 0.0, 2.0, 6.0, 11.0]

print("convex  f(x) = (x-3)^2 + 2")
for s in starts:
    x = descend(f1, grad1, s)
    print("  start %6.1f -> x %8.4f   f %9.4f" % (s, x, f1(x)))
print("  every start lands in the same place.")
print()

print("non-convex  f(x) = 0.15(x-3)^2 + 3 sin(2x)")
found = []
for s in starts:
    x = descend(f2, grad2, s)
    found.append(round(x, 3))
    print("  start %6.1f -> x %8.4f   f %9.4f" % (s, x, f2(x)))
print("  %d different minima from %d starts." % (len(set(found)), len(starts)))
best = min(found, key=lambda x: f2(x))
print("  best found f = %.4f at x = %.3f; the worst was f = %.4f"
      % (f2(best), best, max(f2(x) for x in found)))
print()
print("a convex function has one minimum and every downhill path finds it.")
print("that is why linear and logistic regression train reproducibly, and")
print("why a neural network gives you a different answer every restart.")
print()
print("the test: a function is convex if the line between any two points on")
print("it never dips below the function.")
for f, name in ((f1, "convex"), (f2, "non-convex")):
    a, b = -2.0, 8.0
    mids = np.linspace(0.05, 0.95, 19)
    chord = [(1 - t) * f(a) + t * f(b) for t in mids]
    curve = [f((1 - t) * a + t * b) for t in mids]
    viol = sum(c < v - 1e-9 for c, v in zip(chord, curve))
    print("  %-11s chord dips below the curve at %d of %d points"
          % (name, viol, len(mids)))
```

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

## Rebuild a function from its derivatives

Terms added one at a time, with the error after each. The approximation is excellent near the expansion point and hopeless far from it.

```python-run
import numpy as np
import math

def taylor_exp(x, terms):
    return sum(x ** k / math.factorial(k) for k in range(terms))

print("e^x built term by term, at x = 0.5")
true = np.exp(0.5)
for t in range(1, 7):
    approx = taylor_exp(0.5, t)
    print("  %d term(s): %.10f   error %.2e" % (t, approx, abs(approx - true)))
print("  exact    : %.10f" % true)
print()
print("the same 6 terms, further from x = 0:")
for x in (0.5, 1.0, 2.0, 5.0, 10.0):
    approx, true = taylor_exp(x, 6), np.exp(x)
    print("  x=%5.1f  approx %14.4f  true %14.4f  relative error %8.2f%%"
          % (x, approx, true, 100 * abs(approx - true) / true))
print()
print("first-order approximations you have already used:")
for x in (0.01, 0.1, 0.5):
    print("  sin(%.2f) = %.6f, and x = %.6f      (error %.2e)"
          % (x, np.sin(x), x, abs(np.sin(x) - x)))
    print("  ln(1+%.2f) = %.6f, and x = %.6f     (error %.2e)"
          % (x, np.log(1 + x), x, abs(np.log(1 + x) - x)))
```

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

## A bet worth taking that usually loses

Expectation and variance computed from the definition, then measured over 400,000 plays. The two numbers say different things, and both matter.

```python-run
import numpy as np

# a bet: 1/6 chance to win 80, else lose 12
outcomes = np.array([80.0, -12.0])
probs    = np.array([1 / 6, 5 / 6])

ev = (outcomes * probs).sum()
var = (probs * (outcomes - ev) ** 2).sum()

print("E[X]   = %.4f" % ev)
print("Var[X] = %.4f   sd = %.4f" % (var, np.sqrt(var)))
print()

rng = np.random.default_rng(1)
draws = rng.choice(outcomes, size=400_000, p=probs)
print("400,000 plays: average %.4f, variance %.4f" % (draws.mean(), draws.var()))
print("               total won: %.0f" % draws.sum())
print()
print("a bet worth taking that still loses most of the time:")
print("  fraction of plays that lost money: %.3f" % (draws < 0).mean())
print()
print("the sd is %.1f -- far bigger than the edge of %.2f."
      % (np.sqrt(var), ev))
print("expectation says play; variance says do not bet the rent on one round.")
```

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

## The three, side by side

One trial, n trials, and counts with no fixed n. The last block shows a binomial with large n and small p turning into a Poisson.

```python-run
import numpy as np

rng = np.random.default_rng(7)

print("Bernoulli(p=0.3): one trial, 0 or 1")
b = (rng.random(200_000) < 0.3).astype(int)
print("  mean %.4f (should be p)   var %.4f (should be p(1-p)=%.4f)"
      % (b.mean(), b.var(), 0.3 * 0.7))
print()

print("Binomial(n=10, p=0.3): how many successes in 10 trials")
k = rng.binomial(10, 0.3, size=200_000)
print("  mean %.4f (np = %.1f)   var %.4f (np(1-p) = %.2f)"
      % (k.mean(), 10 * 0.3, k.var(), 10 * 0.3 * 0.7))
for i in range(0, 8):
    print("   P(k=%d) = %.4f" % (i, (k == i).mean()))
print()

print("Poisson(lam=3): counts in a window, no fixed n")
p = rng.poisson(3.0, size=200_000)
print("  mean %.4f  var %.4f   <- Poisson has mean == variance" % (p.mean(), p.var()))
print()
print("Binomial(n=1000, p=0.003) looks like Poisson(3):")
big = rng.binomial(1000, 0.003, size=200_000)
for i in range(0, 7):
    print("   k=%d  binomial %.4f   poisson %.4f" % (i, (big == i).mean(), (p == i).mean()))
```

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

## Watch it happen

A deliberately lopsided population, and the means of samples drawn from it. The spread of those means shrinks like one over the square root of the sample size.

```python-run
import numpy as np

rng = np.random.default_rng(0)

# A deliberately lopsided population: mostly small values, a long tail.
population = rng.exponential(scale=1.0, size=200_000)
print("population  mean %.3f  median %.3f  max %.1f"
      % (population.mean(), np.median(population), population.max()))
print()
print("means of samples drawn from it:")
print("%8s %10s %10s" % ("n", "mean", "std of means"))
for n in (1, 2, 10, 50, 200):
    means = rng.exponential(1.0, size=(4000, n)).mean(axis=1)
    print("%8d %10.3f %10.3f" % (n, means.mean(), means.std()))
print()
print("1/sqrt(200) = %.3f, which is what the last row should be"
      % (1.0 / np.sqrt(200)))
```

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

## Nobody experiences the mean

Ten thousand response times with a long tail. The mean and the median tell one story; p95 and p99 tell the one your users live in.

```python-run
import numpy as np

rng = np.random.default_rng(2)
# response times in ms: mostly fast, a long tail
ms = np.concatenate([rng.normal(90, 15, 9500), rng.normal(700, 200, 500)])
ms = np.clip(ms, 1, None)

print("10,000 requests")
print("  mean   %7.1f ms" % ms.mean())
print("  median %7.1f ms" % np.median(ms))
print()
for q in (50, 75, 90, 95, 99, 99.9):
    print("  p%-5s %7.1f ms" % (q, np.percentile(ms, q)))
print()
print("the mean sits at %.1f, which %.1f%% of requests are faster than."
      % (ms.mean(), (ms < ms.mean()).mean() * 100))
print("nobody experiences the mean. they experience p95.")
```

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

## The distribution of a statistic, not of the data

Draw a sample, compute its mean, write it down, repeat ten thousand times. What you get is a different distribution from the one you sampled.

```python-run
import numpy as np

rng = np.random.default_rng(0)

# the population: heavily skewed, nothing like a bell curve
population = rng.exponential(scale=10.0, size=1_000_000)
print("population: mean %.3f, sd %.3f, median %.3f"
      % (population.mean(), population.std(), np.median(population)))
print("  it is skewed -- 90th percentile is %.1f, max is %.1f"
      % (np.percentile(population, 90), population.max()))
print()

for n in (2, 10, 50, 200):
    means = population[rng.integers(0, len(population), size=(10_000, n))].mean(axis=1)
    predicted_se = population.std() / np.sqrt(n)
    print("samples of %3d: mean of means %6.3f   sd of means %6.3f "
          "(predicted %6.3f)" % (n, means.mean(), means.std(), predicted_se))
print()
print("two separate facts here:")
print("  the sampling distribution centres on the population mean;")
print("  its spread shrinks like 1/sqrt(n), so 4x the data halves the error.")
print()
print("that sd of the means is what 'standard error' means. it is not the")
print("spread of your data -- it is the spread of the answer you computed.")
```

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

# ---------------------------------------------------------------------------
# 11. Confidence intervals
# ---------------------------------------------------------------------------
topic(
    "confidence_intervals",
    "Confidence Intervals",
    "Inference",
    "Draw a thousand intervals from a known population and count how many "
    "contain the answer. The confidence is a property of the procedure.",
    _svg("".join(_line(28 + (i % 3) * 6, 22 + i * 6, 96 + (i % 4) * 8, 22 + i * 6,
                       A if i == 4 else M, 1.6) for i in range(8))
         + _line(72, 16, 72, 74, A, 1.4, "3 3")
         + _txt(80, 86, "most of them cover it", M, 7)),
    {
        "demo": "confidence",
        "controls": [
            {"key": "n", "label": "Sample size", "type": "range",
             "min": 4, "max": 200, "step": 2, "value": 30},
            {"key": "conf", "label": "Confidence level", "type": "select", "value": "0.95",
             "options": [{"value": "0.80", "label": "80%"},
                         {"value": "0.90", "label": "90%"},
                         {"value": "0.95", "label": "95%"},
                         {"value": "0.99", "label": "99%"}]},
            {"key": "seed", "label": "Redraw", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 7},
        ],
        "fixed": {},
    },
    [
        "A 95% interval does not mean the parameter is 95% likely to be inside "
        "<em>your</em> interval. It is inside or it is not.",
        "It means the <strong>procedure</strong> produces intervals that "
        "contain the parameter 95% of the time.",
        "The width is <code class='mono-font'>z &middot; SE</code>, so it "
        "shrinks like <a href='sampling_distributions.html'>&radic;n</a>.",
        "Higher confidence buys a wider interval and nothing else. A 99% "
        "interval says less about where the answer is, not more.",
    ],
    """
title: Confidence Intervals
intro: What the ninety-five percent actually refers to, demonstrated by drawing a thousand of them.

## The construction

Take a sample, compute its mean, and put an interval around it:

```
mean  +/-  z * (sample SD / sqrt(n))
```

The `z` depends on the confidence level &mdash; 1.96 for 95%. The rest is the
[standard error](sampling_distributions.html).

## What the confidence refers to

Here is the statement people usually give: *there is a 95% probability the true
mean lies in this interval.*

That is wrong, and the visualisation shows why. The population mean is fixed at
10 &mdash; the dashed line. It is not random. Your interval is either side of it
or it is not; there is no probability left once both are determined.

What is random is the **interval**, because it is computed from a random sample.
Draw again and you get a different one. The 95% describes how often that
procedure lands on the truth.

The panel draws forty intervals, from a thousand generated. Most cross the
dashed line; the highlighted few do not. Nothing distinguishes a missing
interval from a covering one when you can only see it from the inside &mdash;
and in practice you have exactly one, and no idea which kind you have.

## The count is real

The readout gives the actual coverage of all thousand. At n = 30 with a 95%
level it lands near 94%, and every part of that gap is instructive.

Drag `n` down to 5 and coverage falls to about 89%. That is not sampling noise.
This page uses a `z` critical value with the sample's *estimated* standard
deviation, and at small `n` that estimate is unreliable enough that the interval
comes out too narrow.

**That is exactly why the t-distribution exists.** Gosset's correction widens
the interval to account for having estimated the SD, and the correction is large
at small `n` and negligible past about 30. Drag `n` upward and watch the gap
close on its own &mdash; the page is demonstrating the problem the t-distribution
solves, rather than quietly using t and hiding it.

## Width and what buys it

Two things set the width.

**The confidence level.** Switch from 95% to 99% and the intervals lengthen
noticeably. A higher level does not locate the parameter better; it hedges more.
A 100% interval would be "somewhere between minus infinity and infinity" &mdash;
perfectly reliable and perfectly useless.

**The sample size**, through `sqrt(n)`. Quadrupling the sample halves the width.

## Reading one properly

**"Between 42% and 48%"** means the procedure that produced it covers the truth
95% of the time.

**A wide interval is a result.** It says the data does not pin the answer down,
which is genuine information rather than a failed experiment.

**Overlapping intervals do not imply no difference.** Two 95% intervals can
overlap while a direct test of their difference is significant. Test the
difference; do not eyeball the bars.

**An interval containing zero** corresponds to a two-sided test not rejecting at
that level. That correspondence is exact, and it is why many people prefer
reporting intervals to reporting
[p-values](hypothesis_testing_and_p_values.html): the interval carries the
effect size and the uncertainty together, where a p-value carries neither.

## Where it goes wrong

**Saying "95% chance the mean is in here."** The parameter is fixed; the
interval is random.

**Using z at small n.** Use t, and this page shows you the cost of not.

**Assuming independence.** Clustered or time-series data has a smaller effective
sample size, and the interval will be too narrow.

**Reporting an interval for a biased estimator.** Coverage is about sampling
variability. A systematically wrong measurement produces a tight interval around
the wrong answer.

## What "95% confident" actually counts

Build a confidence interval a thousand times from a known population and count how often it contains the true mean. The number the interval describes is the procedure, not your one result.

```python-run
import numpy as np

rng = np.random.default_rng(0)
TRUE_MEAN, TRUE_SD, N = 100.0, 15.0, 40

def interval(sample):
    se = sample.std(ddof=1) / np.sqrt(len(sample))
    half = 1.96 * se
    return sample.mean() - half, sample.mean() + half

print("one sample of %d from a population with mean %.0f:" % (N, TRUE_MEAN))
s = rng.normal(TRUE_MEAN, TRUE_SD, N)
lo, hi = interval(s)
print("  sample mean %.2f, 95%% interval (%.2f, %.2f)" % (s.mean(), lo, hi))
print("  contains the true mean:", lo <= TRUE_MEAN <= hi)
print()

hits = 0
trials = 10_000
widths = []
for _ in range(trials):
    s = rng.normal(TRUE_MEAN, TRUE_SD, N)
    lo, hi = interval(s)
    hits += (lo <= TRUE_MEAN <= hi)
    widths.append(hi - lo)
print("%d intervals built the same way:" % trials)
print("  %.2f%% of them contained the true mean" % (100 * hits / trials))
print("  average width %.2f" % np.mean(widths))
print()
print("that is the whole claim. any single interval either contains the mean")
print("or it does not -- there is no 95 percent about it once computed.")
print()
print("it came out a little under 95%. the 1.96 multiplier assumes you know")
print("the population sd; estimating it from 40 points costs you some coverage.")
print("the t distribution corrects exactly that:")
t39 = 2.0227                                   # t multiplier, 39 degrees of freedom
hits_t = 0
for _ in range(trials):
    s2 = rng.normal(TRUE_MEAN, TRUE_SD, N)
    half = t39 * s2.std(ddof=1) / np.sqrt(N)
    hits_t += abs(s2.mean() - TRUE_MEAN) <= half
print("  with t instead of 1.96: %.2f%% coverage" % (100 * hits_t / trials))
print()
print("more data makes the interval narrower, at the usual 1/sqrt(n) rate:")
for n in (10, 40, 160, 640):
    ws = [np.diff(interval(rng.normal(TRUE_MEAN, TRUE_SD, n)))[0] for _ in range(400)]
    print("  n=%4d  average width %.2f" % (n, np.mean(ws)))
```

""",
    [
        {"q": "What does the 95% in a 95% confidence interval describe?",
         "options": ["The probability the parameter is in your interval",
                     "How often the procedure produces intervals that contain the parameter",
                     "The proportion of data inside the interval",
                     "The confidence of the analyst"],
         "answer": 1,
         "why": "The parameter is fixed - it is inside or it is not. What is random is the interval, because it is computed from a random sample."},
        {"q": "Why does a nominal 95% interval cover only about 89% at n = 5 here?",
         "options": ["The random number generator is biased",
                     "It uses a z value with an estimated SD, which is unreliable at small n - the problem the t-distribution fixes",
                     "The population is not normal",
                     "1000 draws is not enough"],
         "answer": 1,
         "why": "The correction is large at small n and negligible past about 30. Dragging n upward closes the gap on its own."},
        {"q": "Two 95% intervals overlap. What follows?",
         "options": ["The difference is not significant",
                     "Nothing directly - a test of the difference can still be significant",
                     "The samples are the same size",
                     "Both contain the true mean"],
         "answer": 1,
         "why": "Overlap of separate intervals is not a test of their difference. Test the difference directly rather than eyeballing the bars."},
    ],
)


# ---------------------------------------------------------------------------
# 12. Hypothesis testing and p-values
# ---------------------------------------------------------------------------
topic(
    "hypothesis_testing_and_p_values",
    "Hypothesis Testing and p-values",
    "Inference",
    "The p-value is a shaded area under an assumption. Move the observation "
    "and watch the area, and the assumption, stay exactly where they were.",
    _svg('<path d="M20 70 C 46 70, 50 22, 72 22 C 94 22, 98 70, 130 70" fill="none" stroke="%s" stroke-width="2"/>' % A
         + '<path d="M104 70 C 114 66, 120 52, 130 70 Z" fill="%s" fill-opacity="0.4" stroke="none"/>' % A
         + _line(104, 18, 104, 74, A, 1.4, "3 3")
         + _txt(80, 86, "the tail, not the truth", M, 7)),
    {
        "demo": "pvalue",
        "controls": [
            {"key": "observed", "label": "Observed statistic", "type": "range",
             "min": -3.5, "max": 3.5, "step": 0.05, "value": 2.10},
            {"key": "tail", "label": "Alternative", "type": "select", "value": "two",
             "options": [{"value": "two", "label": "Two-tailed"},
                         {"value": "one", "label": "One-tailed (greater)"}]},
        ],
    },
    [
        "The curve is the distribution of the test statistic <em>assuming the "
        "null hypothesis is true</em>. Everything else follows from that.",
        "The <strong>p-value</strong> is the shaded area: the probability of a "
        "result at least this extreme, if the null held.",
        "It is not the probability the null is true, and it is not the "
        "probability your result was a fluke.",
        "0.05 is a convention Fisher suggested as a rule of thumb, not a "
        "property of nature.",
    ],
    """
title: Hypothesis Testing and p-values
intro: The most used and most misread number in statistics, defined precisely enough to stop misreading it.

## The machinery

**The null hypothesis** is a specific, boring claim: no effect, no difference,
nothing happening. It is specific on purpose, because a specific claim implies a
distribution for the test statistic.

That distribution is the curve. It is what the statistic would look like across
repeated samples **if the null were true**. Every use of a p-value inherits that
conditional.

**The p-value** is the shaded tail: the probability of a statistic at least as
extreme as the one observed, under the null.

Drag the observed statistic and watch the area shrink as it moves outward. A
large statistic is unusual under the null, so its tail is small &mdash; and a
small tail is what "unlikely, if the null were true" means.

## What it is not

Three misreadings, all common enough to have names.

**Not the probability that the null is true.** The p-value is computed *assuming*
the null. It cannot then tell you how likely the assumption was. Getting from
`P(data | null)` to `P(null | data)` needs [Bayes'
theorem](bayes_theorem.html) and a prior, and the two quantities can differ by
orders of magnitude.

**Not the probability the result was chance.** Same error, differently worded.

**Not a measure of effect size.** With enough data, a difference of no practical
consequence produces a tiny p-value. The p-value answers "is there evidence of
*any* effect", never "is the effect large enough to matter". This is why
[confidence intervals](confidence_intervals.html) are increasingly preferred:
they carry the size and the uncertainty in one object.

## Failing to reject is not accepting

Set the observed statistic near zero. The p-value is large, and the conclusion is
that the data is consistent with the null.

It is **not** that the null is true. A large p-value is produced both by a real
absence of effect and by a study too small to detect one. Distinguishing those
requires [power](type_i_and_type_ii_errors.html), and it is why "no significant
difference" in an underpowered study means almost nothing.

## One tail or two

Switch the alternative. The two-tailed p-value is exactly double the one-tailed
one for the same statistic, because the same area is being counted on both sides.

The choice must be made **before** seeing the data. Deciding afterwards that you
only cared about one direction halves your p-value for free, and that is a
recognised form of cheating rather than a modelling choice.

## Why 0.05 is under attack

The threshold is a convention. Fisher suggested it as a rough guide and
explicitly did not intend it as a decision rule.

The problems are structural.

**p-hacking.** Test enough hypotheses and something crosses 0.05 by chance. At
0.05, one test in twenty does so with no effect present at all.

**Publication bias.** Significant results get published, so the literature
over-represents them, and the effect sizes it reports are inflated.

**The cliff.** p = 0.049 and p = 0.051 are indistinguishable as evidence and are
treated as opposites.

The responses in circulation: report exact p-values rather than thresholds,
report effect sizes and intervals alongside, pre-register the analysis, and
correct for multiple comparisons. Some fields have moved the threshold to 0.005;
others argue for abandoning the dichotomy entirely.

## Where it goes wrong

**Reading p as the probability the null is true.** The central error.

**Treating "not significant" as "no effect."** Check the power.

**Choosing the tail after seeing the data.**

**Running many tests without correction.** Bonferroni is crude and better than
nothing; false discovery rate control is usually the better tool.

## Where p-values come from, and what breaks them

A p-value computed by simulation rather than looked up in a table, then the same test run two hundred times on data with no effect in it at all.

```python-run
import numpy as np
import math

rng = np.random.default_rng(0)

control = rng.normal(0.1000, 0.02, 300)
variant = rng.normal(0.1045, 0.02, 300)
observed = variant.mean() - control.mean()
print("A/B test: control %.4f, variant %.4f, difference %+.4f"
      % (control.mean(), variant.mean(), observed))
print()

# the null hypothesis says the labels do not matter. so shuffle them.
pool = np.concatenate([control, variant])
null_diffs = np.empty(20_000)
for i in range(20_000):
    rng.shuffle(pool)
    null_diffs[i] = pool[300:].mean() - pool[:300].mean()

p = (np.abs(null_diffs) >= abs(observed)).mean()
print("shuffling the labels 20,000 times, so no real effect can survive:")
print("  the shuffled differences spread out to sd %.5f" % null_diffs.std())
print("  %.2f%% of them were at least as big as the one we measured" % (100 * p))
print("  that fraction is the p-value: %.4f" % p)
print()
print("it is NOT the probability the null is true. it is the probability of")
print("data at least this extreme IF the null were true.")
print()

def p_value(a, b):
    d = b.mean() - a.mean()
    se = np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return 2 * (1 - 0.5 * (1 + math.erf(abs(d / se) / np.sqrt(2))))

print("now the failure mode. 1000 tests, no effect in any of them:")
ps = np.array([p_value(rng.normal(0.1, 0.02, 300), rng.normal(0.1, 0.02, 300))
               for _ in range(1000)])
hits = (ps < 0.05).sum()
print("  %d of 1000 came out under 0.05, from pure noise." % hits)
print("  expected: 1000 * 0.05 = 50.0")
print()
print("the smallest few p-values in that batch of nothing:")
for v in np.sort(ps)[:5]:
    print("    %.4f" % v)
print()
print("a 5 percent threshold lets one test in twenty clear it by chance. run")
print("enough metrics and you will always find a winner. that is why the")
print("threshold has to be tightened when you test many things at once:")
print("  Bonferroni for 1000 tests: %.7f" % (0.05 / 1000))
print("  tests still under it: %d" % (ps < 0.05 / 1000).sum())
```

""",
    [
        {"q": "A p-value is the probability of:",
         "options": ["The null hypothesis being true",
                     "A result at least this extreme, assuming the null is true",
                     "The alternative hypothesis being true",
                     "Making a Type I error"],
         "answer": 1,
         "why": "It is computed assuming the null, so it cannot tell you how likely that assumption was. Going the other way needs Bayes' theorem and a prior."},
        {"q": "A study reports p = 0.4. What can you conclude?",
         "options": ["The null hypothesis is true",
                     "The data is consistent with the null - which is also what an underpowered study looks like",
                     "There is no effect",
                     "The sample was too large"],
         "answer": 1,
         "why": "A large p-value is produced both by a real absence of effect and by a study too small to detect one. Distinguishing them requires power."},
        {"q": "Why must the choice of one or two tails be made before seeing the data?",
         "options": ["It changes the test statistic",
                     "Choosing afterwards halves the p-value for free, which is cheating rather than a modelling choice",
                     "Two-tailed tests need more data",
                     "The null hypothesis changes"],
         "answer": 1,
         "why": "The two-tailed p-value is exactly double the one-tailed one for the same statistic, so the decision has to precede the observation."},
    ],
)


# ---------------------------------------------------------------------------
# 13. Type I and Type II errors, and power
# ---------------------------------------------------------------------------
topic(
    "type_i_and_type_ii_errors",
    "Type I and Type II Errors",
    "Inference",
    "Two overlapping distributions and one threshold between them. Every "
    "choice you make trades one error for the other.",
    _svg('<path d="M16 70 C 38 70, 40 30, 58 30 C 76 30, 78 70, 100 70" fill="none" stroke="%s" stroke-width="1.8"/>' % M
         + '<path d="M60 70 C 82 70, 84 34, 102 34 C 120 34, 122 70, 144 70" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + _line(80, 22, 80, 74, A, 1.6, "3 3")
         + _txt(80, 86, "move it either way, pay either way", M, 7)),
    {
        "demo": "power",
        "controls": [
            {"key": "effect", "label": "True effect size", "type": "range",
             "min": 0.0, "max": 1.5, "step": 0.05, "value": 0.50},
            {"key": "n", "label": "Sample size", "type": "range",
             "min": 5, "max": 200, "step": 5, "value": 40},
            {"key": "alpha", "label": "Alpha (Type I rate)", "type": "select", "value": "0.05",
             "options": [{"value": "0.10", "label": "0.10"},
                         {"value": "0.05", "label": "0.05"},
                         {"value": "0.01", "label": "0.01"}]},
        ],
    },
    [
        "<strong>Type I</strong> is a false positive: rejecting a null that was "
        "true. Its rate is &alpha;, and you choose it.",
        "<strong>Type II</strong> is a false negative: failing to reject a null "
        "that was false. Its rate is &beta;, and you mostly do not.",
        "<strong>Power</strong> is 1 &minus; &beta;: the chance of detecting an "
        "effect that is really there.",
        "Moving the threshold trades one for the other. Only more data, or a "
        "larger true effect, improves both.",
    ],
    """
title: Type I and Type II Errors
intro: The two ways a test can be wrong, why you cannot minimise both, and what power actually buys.

## Two curves, one line

The grey curve is the test statistic when the null is true. The orange curve is
the same statistic when the effect is real. They overlap, and the overlap is the
entire problem.

The dashed line is the threshold: above it you reject the null, below it you do
not.

**Type I error** &mdash; the grey area to the right of the line. The null was
true and you rejected it. A false positive.

**Type II error** &mdash; the orange area to the left. The effect was real and
you missed it. A false negative.

**Power** is what is left of the orange curve: `1 - beta`, the probability of
catching a real effect.

## The trade

Change alpha from 0.05 to 0.01. The threshold moves right, the grey tail
shrinks &mdash; and the orange tail grows. Beta rises, power falls.

Move it the other way and the reverse happens.

**You cannot reduce both by moving the line.** That is not a limitation of the
method; it is what "the distributions overlap" means. Any threshold is a
statement about which error you would rather make.

## What actually helps

Two things, and only two.

**More data.** Drag `n` upward. Both curves narrow, because their spread is the
[standard error](sampling_distributions.html) and that falls like `sqrt(n)`. The
overlap shrinks, and both error rates can fall at once. This is the only lever
that improves both without assuming anything.

**A larger true effect.** Drag the effect control. The curves separate. You do
not usually control this, but it is why detecting a large effect needs so much
less data than detecting a small one.

## Choosing alpha honestly

The convention is 0.05, and treating it as fixed is the mistake. The right value
depends on which error costs more.

**A screening test for a treatable disease.** A false negative means missing a
case; a false positive means an unnecessary follow-up. Loosen alpha, gain power.

**A criminal conviction.** The system explicitly prefers false negatives, which
is what "beyond reasonable doubt" encodes.

**Particle physics.** The five-sigma standard is alpha near 3 in 10 million,
because the field has been burned by fluctuations and there is enough data to
afford it.

**A/B testing a button colour.** A wrong call is cheap. Standard thresholds are
generous, and the real risk is running many tests and picking winners.

## Power, before the experiment

Power analysis is the calculation nobody enjoys and everybody should do: given a
target power &mdash; usually 80% &mdash; an alpha, and the smallest effect worth
detecting, how large a sample is required?

Set the effect to 0.2 and watch what `n` has to be before power reaches 80%. The
required sample grows roughly with the inverse square of the effect size, which
is why detecting small effects is so expensive and why so much published work is
underpowered.

An underpowered study is worse than no study. It usually fails to find a real
effect &mdash; and when it does find one, the estimate is inflated, because only
an unusually large sample fluctuation could have crossed the threshold at that
sample size. That is the **winner's curse**, and it is a substantial part of why
published effects shrink on replication.

## Where it goes wrong

**Interpreting a non-significant result as no effect.** Report the power, or the
interval.

**Running the power analysis afterwards.** Post-hoc power computed from the
observed effect is a restatement of the p-value and carries no new information.

**Fixing alpha at 0.05 regardless of costs.** It is a convention.

**Peeking at results and stopping when significant.** This inflates the true
Type I rate far above the nominal one. Sequential testing methods exist and
correct for it.

## Both errors, counted

Lower your threshold and you catch more real effects while raising more false alarms. Here both rates are measured across a sweep, so the trade is visible rather than described.

```python-run
import numpy as np
import math

rng = np.random.default_rng(0)
N = 200
TRIALS = 4000

def p_value(effect):
    a = rng.normal(0.0, 1.0, N)
    b = rng.normal(effect, 1.0, N)
    d = b.mean() - a.mean()
    se = np.sqrt(a.var(ddof=1) / N + b.var(ddof=1) / N)
    z = abs(d / se)
    return 2 * (1 - 0.5 * (1 + math.erf(z / np.sqrt(2))))

null_ps = np.array([p_value(0.00) for _ in range(TRIALS)])   # no effect exists
real_ps = np.array([p_value(0.25) for _ in range(TRIALS)])   # a real effect

print("%10s %18s %18s %10s" % ("threshold", "type I (false alarm)",
                               "type II (missed)", "power"))
for alpha in (0.20, 0.10, 0.05, 0.01, 0.001):
    type1 = (null_ps < alpha).mean()
    type2 = (real_ps >= alpha).mean()
    print("%10.3f %17.3f  %17.3f  %9.3f" % (alpha, type1, type2, 1 - type2))
print()
print("the type I rate tracks the threshold you chose -- that is what alpha is.")
print("tightening it from 0.05 to 0.001 cuts false alarms by 50x and misses")
print("far more real effects. there is no setting that fixes both.")
print()
print("the other lever is sample size:")
for n in (50, 200, 800, 3200):
    N = n
    ps = np.array([p_value(0.25) for _ in range(1500)])
    print("  n=%5d  power at alpha=0.05: %.3f" % (n, (ps < 0.05).mean()))
print()
print("more data lowers the miss rate without touching the false alarm rate.")
print("that is the only way to improve both at once.")
```

""",
    [
        {"q": "You tighten alpha from 0.05 to 0.01. What happens to power?",
         "options": ["It rises", "It falls", "It is unchanged", "It depends on the sample size"],
         "answer": 1,
         "why": "The threshold moves right, shrinking the false-positive tail and growing the false-negative one. Moving the line always trades one error for the other."},
        {"q": "What improves both error rates at once?",
         "options": ["Moving the threshold", "A larger sample, because both curves narrow",
                     "A smaller alpha", "A one-tailed test"],
         "answer": 1,
         "why": "Their spread is the standard error, which falls like root n, so the overlap shrinks. A larger true effect also works, but you rarely control that."},
        {"q": "Why are effects from underpowered studies often inflated?",
         "options": ["The analysis is biased",
                     "Only an unusually large sample fluctuation could cross the threshold at that sample size",
                     "Small samples have larger true effects",
                     "The alpha was too strict"],
         "answer": 1,
         "why": "The winner's curse - and a substantial part of why published effects shrink on replication."},
    ],
)


# ---------------------------------------------------------------------------
# 14. QR decomposition
# ---------------------------------------------------------------------------
topic(
    "qr_decomposition",
    "QR Decomposition and Gram-Schmidt",
    "Linear Algebra",
    "Turn any basis into an orthonormal one by subtracting the part that "
    "already points the wrong way. Watch the subtraction happen.",
    _svg(_line(30, 68, 96, 34, M, 1.8, "4 3") + _line(30, 68, 78, 74, M, 1.8, "4 3")
         + _line(30, 68, 88, 38, A, 2.6) + _line(30, 68, 46, 40, A, 2.6)
         + _line(88, 38, 78, 74, M, 1.4, "2 2")
         + _txt(80, 88, "subtract the overlap, keep the rest", M, 7)),
    {
        "demo": "gramschmidt",
        "controls": [
            {"key": "x1", "label": "a1 x", "type": "range",
             "min": -3, "max": 3, "step": 0.1, "value": 2.0},
            {"key": "y1", "label": "a1 y", "type": "range",
             "min": -2.4, "max": 2.4, "step": 0.1, "value": 0.5},
            {"key": "x2", "label": "a2 x", "type": "range",
             "min": -3, "max": 3, "step": 0.1, "value": 1.0},
            {"key": "y2", "label": "a2 y", "type": "range",
             "min": -2.4, "max": 2.4, "step": 0.1, "value": 1.6},
        ],
    },
    [
        "<code class='mono-font'>A = QR</code>: Q holds an orthonormal basis "
        "for the columns of A, R holds the coefficients that rebuild them.",
        "Gram-Schmidt: normalise the first vector, then subtract from the second "
        "everything that points along the first.",
        "The solid orange line is the <a href='projections.html'>projection</a> "
        "being removed. What remains is perpendicular by construction.",
        "R is upper triangular because the k-th original vector is built only "
        "from the first k orthonormal ones.",
    ],
    """
title: QR Decomposition and Gram-Schmidt
intro: Manufacturing an orthonormal basis, and the factorisation that makes least squares numerically respectable.

## The procedure

Start with vectors that span what you want but are not perpendicular. Gram-
Schmidt makes them perpendicular without changing what they span.

**First vector**: divide by its length. That is `q1` &mdash; same direction,
length 1.

**Second vector**: it points partly along `q1` and partly perpendicular to it.
[Project](projections.html) it onto `q1`, subtract that projection, and what is
left is perpendicular by construction. Normalise it to get `q2`.

The visualisation draws each step. The dashed grey lines are the originals. The
solid orange segment is the projection being removed, and the short dashed line
is the remainder that becomes `q2`. The readout gives `q1 . q2` &mdash; zero to
six decimal places, because it cannot be anything else.

For more vectors the pattern repeats: subtract the components along everything
already fixed, normalise what survives.

## Where R comes from

The projections you subtract are not discarded. Collect them and you have `R`,
and together:

```
A  =  Q R
```

`Q` has the orthonormal vectors as columns; `R` is upper triangular.

`R` is triangular for a structural reason worth seeing: the first original
vector is built from `q1` alone, the second from `q1` and `q2`, the third from
the first three. Nothing is ever built from a `q` that comes later, so
everything below the diagonal is zero.

Drag until the two input vectors nearly align. The remainder shrinks toward zero
and `R` becomes nearly singular &mdash; which is the same near-dependence
[the basis module](basis_span_and_orthogonality.html) warns about, showing up as
a small number on the diagonal.

## Why least squares uses it

The textbook solution to least squares is the normal equations:

```
x  =  (A'A)^-1 A' b
```

Correct, and numerically poor. Forming `A'A` **squares the condition number**.
A matrix with condition number 10&#8310; &mdash; unremarkable for real data
&mdash; becomes 10&#185;&#178;, and in double precision that has consumed most
of the available accuracy before the solve begins.

QR avoids it. Substituting `A = QR` and using `Q'Q = I`:

```
R x  =  Q' b
```

`R` is triangular, so this is solved by back-substitution in one pass, and the
condition number is never squared. That is why `numpy.linalg.lstsq`, R's `lm`
and essentially every serious least-squares routine uses QR or an
[SVD](singular_value_decomposition.html) rather than the formula in the
textbook.

## Classical against modified Gram-Schmidt

The version described above is *classical* Gram-Schmidt, and it is unstable in
floating point: rounding errors mean the later vectors drift away from
orthogonality.

*Modified* Gram-Schmidt subtracts each projection immediately rather than all at
once at the end. Algebraically identical, numerically much better behaved.

Serious implementations use neither, preferring **Householder reflections**,
which build `Q` from a sequence of reflections and are stable regardless of the
input. Gram-Schmidt survives because it is the version you can see, which is why
it is the version on this page.

## Where else it turns up

**The QR algorithm** for eigenvalues repeatedly factors and re-multiplies in the
other order, and the result converges to a triangular matrix whose diagonal
holds the eigenvalues. It is one of the most important numerical algorithms
there is, and it is this decomposition in a loop.

**Orthogonalising features** before regression, to remove collinearity.

**Kalman filters** in square-root form, for the same conditioning reason as
least squares.

## Where it goes wrong

**Classical Gram-Schmidt on ill-conditioned input.** Use the modified version,
or a library.

**Forming A'A because the formula is shorter.** It squares the conditioning.

**Assuming Q is square.** For a tall thin `A`, the economy QR gives a `Q` with
the same shape as `A`, not a full orthogonal matrix.

## Orthogonalise a basis, then solve with it

QR turns any set of columns into an orthonormal set plus the bookkeeping needed to get back. It is how least squares is solved in practice.

```python-run
import numpy as np

A = np.array([[1.0, 1.0, 1.0],
              [1.0, 2.0, 4.0],
              [1.0, 3.0, 9.0],
              [1.0, 4.0, 16.0],
              [1.0, 5.0, 25.0]])

Q, R = np.linalg.qr(A)
print("A is %d x %d, Q is %s, R is %s" % (A.shape + (Q.shape, R.shape)))
print()
print("Q has orthonormal columns -- Q.T @ Q is the identity:")
print(np.round(Q.T @ Q, 10) + 0.0)
print()
print("R is upper triangular (zeros below the diagonal):")
print(np.round(R, 4) + 0.0)
print()
print("and they multiply back to A:", np.allclose(Q @ R, A))
print()

b = np.array([2.1, 3.9, 8.2, 14.1, 22.0])
print("least squares fit of a quadratic to 5 points")
via_qr = np.linalg.solve(R, Q.T @ b)
via_normal = np.linalg.solve(A.T @ A, A.T @ b)
print("  via QR            ", np.round(via_qr, 6))
print("  via normal eqns   ", np.round(via_normal, 6))
print("  numpy's lstsq     ", np.round(np.linalg.lstsq(A, b, rcond=None)[0], 6))
print()
print("all three agree here. QR is preferred because it never forms A.T @ A,")
print("which squares the condition number and throws away precision:")
print("  condition number of A      %.3e" % np.linalg.cond(A))
print("  condition number of A.T@A  %.3e" % np.linalg.cond(A.T @ A))
```

""",
    [
        {"q": "Why is R upper triangular?",
         "options": ["By convention",
                     "The k-th original vector is built only from the first k orthonormal vectors, never a later one",
                     "Because Q is orthogonal",
                     "To make back-substitution possible"],
         "answer": 1,
         "why": "Nothing is ever built from a q that comes later, so everything below the diagonal is zero - which then makes back-substitution possible as a consequence."},
        {"q": "Why do least-squares solvers avoid the normal equations?",
         "options": ["They are slower",
                     "Forming A'A squares the condition number, consuming most of the available precision",
                     "They require a square matrix",
                     "They cannot handle collinearity"],
         "answer": 1,
         "why": "A condition number of 10^6 becomes 10^12. QR gives Rx = Q'b, solved by back-substitution, with the conditioning never squared."},
        {"q": "What does modified Gram-Schmidt change?",
         "options": ["The resulting Q and R",
                     "Nothing algebraically - it subtracts each projection immediately, which is far more stable in floating point",
                     "The order of the input vectors",
                     "It produces a square Q"],
         "answer": 1,
         "why": "Algebraically identical, numerically much better. Serious implementations use Householder reflections instead, which are stable regardless of input."},
    ],
)


# ---------------------------------------------------------------------------
# 15. Cholesky and positive-definiteness
# ---------------------------------------------------------------------------
topic(
    "cholesky_and_positive_definiteness",
    "Cholesky and Positive-Definiteness",
    "Linear Algebra",
    "The square root of a matrix, when one exists. Push the correlation too "
    "far and the factorisation fails &mdash; which is the test.",
    _svg(_box(20, 28, 40, 40, fill=S, stroke=B, sw=1.6) + _txt(40, 52, "C", A, 11)
         + _txt(70, 52, "=", M, 10)
         + '<path d="M84 28 L84 68 L124 68 Z" fill="%s" fill-opacity="0.2" stroke="%s" stroke-width="1.6"/>' % (A, A)
         + _txt(97, 60, "L", A, 10) + _txt(136, 52, "L'", A, 10)
         + _txt(80, 84, "a matrix square root", M, 7)),
    {
        "demo": "cholesky",
        "controls": [
            {"key": "s1", "label": "SD of x", "type": "range",
             "min": 0.3, "max": 2.5, "step": 0.1, "value": 1.4},
            {"key": "s2", "label": "SD of y", "type": "range",
             "min": 0.3, "max": 2.5, "step": 0.1, "value": 0.9},
            {"key": "rho", "label": "Correlation", "type": "range",
             "min": -1.05, "max": 1.05, "step": 0.05, "value": 0.60},
            {"key": "seed", "label": "Resample", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 5},
        ],
    },
    [
        "<code class='mono-font'>C = L L'</code> with L lower triangular. It is "
        "the closest thing a matrix has to a square root.",
        "It exists exactly when the matrix is <strong>positive definite</strong> "
        "&mdash; every eigenvalue strictly greater than zero.",
        "Multiply independent standard normals by L and they come out with "
        "covariance exactly C. That is how correlated noise is generated.",
        "Push the correlation past &plusmn;1 and the factorisation fails. The "
        "failure is the diagnosis, and it is cheap.",
    ],
    """
title: Cholesky and Positive-Definiteness
intro: A matrix square root, what it needs to exist, and why its failure is more useful than its success.

## The factorisation

For a symmetric positive-definite matrix `C` there is a lower triangular `L`
with:

```
C  =  L L'
```

`L` is unique if its diagonal is taken positive, and it is the nearest thing a
matrix has to a square root. For a 2&times;2 it is short enough to write out
whole:

```
L11 = sqrt(C11)
L21 = C21 / L11
L22 = sqrt(C22 - L21^2)
```

That last line carries the whole story. If `C22 - L21^2` is negative there is no
real square root, and the algorithm stops.

## Positive-definite

A symmetric matrix is **positive definite** when `x' C x > 0` for every non-zero
`x`, which is equivalent to all its eigenvalues being strictly positive.

For a covariance matrix this is not a technicality. `x' C x` is the variance of
the combination `x` of your variables, and a variance cannot be negative. A
matrix that fails the test is not describing any distribution that exists.

Drag the correlation control toward &plusmn;1. Past the boundary the readout
reports failure, and the reason is that a correlation of 1.2 is not a thing: no
pair of random variables can be more than perfectly correlated.

**The factorisation failing is the test.** Cholesky costs about `n^3 / 3`
operations, roughly half a general LU factorisation, and about a tenth of what
computing the eigenvalues costs. When a routine needs to know whether a matrix
is positive definite, it attempts a Cholesky and watches for the negative square
root.

## Generating correlated randomness

This is where the factor earns its keep. Take independent standard normals `z`
and compute `L z`. The result has covariance:

```
Cov(Lz)  =  L Cov(z) L'  =  L I L'  =  L L'  =  C
```

Exactly the covariance you asked for. The scatter in the visualisation is
generated this way, and the two orange segments are the columns of `L` &mdash;
the axes the independent noise gets mapped onto.

That single trick underlies Monte Carlo simulation of correlated risk factors,
sampling from a multivariate normal, and the reparameterisation trick in
variational autoencoders.

## Where else it appears

**Gaussian processes.** Fitting one requires solving a system with the kernel
matrix and computing its log-determinant. Cholesky gives both: the solve by
triangular substitution, and the log-determinant as twice the sum of the logs of
`L`'s diagonal. It is the computational core of GP regression.

**Linear systems** with a symmetric positive-definite matrix &mdash; twice as
fast as LU and numerically stable without pivoting.

**Optimisation.** Newton steps need to solve with the
[Hessian](jacobian_and_hessian.html), and a successful Cholesky confirms the
Hessian is positive definite, which confirms the step direction is a descent
direction. A failure signals a saddle, and modified Newton methods react to
exactly that signal.

**Whitening.** `L^-1 x` transforms correlated data into uncorrelated data with
unit variance.

## When it fails on data that should be fine

An estimated covariance matrix can come out not-quite-positive-definite for
reasons that are arithmetic rather than conceptual.

**More variables than observations.** The estimate is singular by construction:
with 100 variables and 50 samples the matrix has rank at most 50.

**Perfectly collinear columns.** One variable is a combination of others, so
some direction has genuinely zero variance.

**Floating point.** A matrix that is positive definite in exact arithmetic can
have a tiny negative eigenvalue after rounding.

The standard repairs: add a small multiple of the identity to the diagonal
&mdash; *jitter*, or *ridge*, and the same idea as
[ridge regression](ridge_and_lasso_regression.html); use a shrinkage estimator
such as Ledoit-Wolf; or clip the negative eigenvalues to zero and reassemble.

## Where it goes wrong

**Passing a non-symmetric matrix.** Most implementations read only one triangle
and will silently return nonsense.

**Treating failure as a bug.** It is usually the data telling you something.

**Adding jitter without recording it.** You have changed the model. Say by how
much.

**Using it on a matrix that is only positive semi-definite.** A zero eigenvalue
gives a zero on `L`'s diagonal, and anything that then divides by it fails.

## Half a matrix, and what it costs to have one

Cholesky finds a triangular L with L @ L.T equal to your matrix -- but only if the matrix is positive definite. Here is what that condition rules out.

```python-run
import numpy as np

A = np.array([[ 4.0,  2.0,  1.0],
              [ 2.0,  5.0,  3.0],
              [ 1.0,  3.0,  6.0]])

print("A is symmetric:", np.allclose(A, A.T))
print("eigenvalues:", np.round(np.linalg.eigvalsh(A), 4), " <- all positive")
print()
L = np.linalg.cholesky(A)
print("L (lower triangular):")
print(np.round(L, 4))
print()
print("L @ L.T rebuilds A:", np.allclose(L @ L.T, A))
print()
print("positive definite means x.T @ A @ x > 0 for every non-zero x:")
rng = np.random.default_rng(0)
vals = [x @ A @ x for x in rng.normal(size=(2000, 3))]
print("  2000 random x: smallest quadratic form %.6f" % min(vals))
print()

B = np.array([[1.0, 2.0],
              [2.0, 1.0]])
print("B = [[1,2],[2,1]] is symmetric but its eigenvalues are",
      np.round(np.linalg.eigvalsh(B), 4))
x = np.array([1.0, -1.0])
print("  x = [1,-1] makes the quadratic form negative: %.1f" % (x @ B @ x))
print("  so no real L can exist -- L @ L.T is always positive semi-definite.")
LB = np.linalg.cholesky(B)
print("  cholesky(B) returns:", LB.ravel())
print("  usable:", not np.isnan(LB).any())
print()
print("  (CPython's numpy raises LinAlgError here; this WASM build hands back")
print("   NaN instead, so check the result rather than relying on an exception.)")
print()
print("this is why covariance matrices are always positive semi-definite:")
print("x.T @ Cov @ x is the variance of a projection, and variance cannot be")
print("negative. it is also how correlated samples are generated:")
z = rng.normal(size=(5, 3))
print(np.round(z @ L.T, 3))
```

""",
    [
        {"q": "When does a Cholesky factorisation exist?",
         "options": ["For every square matrix",
                     "For a symmetric matrix with every eigenvalue strictly positive",
                     "For every symmetric matrix",
                     "For every invertible matrix"],
         "answer": 1,
         "why": "Positive definite means x'Cx > 0 for all non-zero x. For a covariance matrix that quantity is a variance, so a matrix failing the test describes no distribution that exists."},
        {"q": "How do you generate samples with a given covariance C?",
         "options": ["Multiply independent standard normals by L, where C = LL'",
                     "Multiply them by C",
                     "Add C to independent normals",
                     "Take the eigenvalues of C"],
         "answer": 0,
         "why": "Cov(Lz) = L I L' = LL' = C. It underlies Monte Carlo simulation of correlated risk, multivariate normal sampling, and the VAE reparameterisation trick."},
        {"q": "Why is attempting a Cholesky the standard positive-definiteness test?",
         "options": ["It is the only test",
                     "It costs about a third of n^3 - far cheaper than computing eigenvalues - and fails exactly when the property does not hold",
                     "It works on non-symmetric matrices",
                     "It never fails"],
         "answer": 1,
         "why": "About half of an LU and roughly a tenth of an eigendecomposition. Routines that need the answer attempt the factorisation and watch for the negative square root."},
    ],
)


# ---------------------------------------------------------------------------
# 16. Lagrange multipliers
# ---------------------------------------------------------------------------
topic(
    "lagrange_multipliers",
    "Lagrange Multipliers",
    "Calculus",
    "Optimise something while a constraint holds. The answer is where the "
    "level lines just graze the constraint, and lambda is what that costs.",
    _svg('<circle cx="80" cy="46" r="26" fill="none" stroke="%s" stroke-width="2"/>' % A
         + "".join(_line(20, 74 - i * 12, 140, 50 - i * 12, M, 0.9) for i in range(5))
         + _dot(99, 30, A, 4.5)
         + _txt(80, 86, "tangency, not crossing", M, 7)),
    {
        "demo": "lagrange",
        "controls": [
            {"key": "ax", "label": "Objective: weight on x", "type": "range",
             "min": -2, "max": 2, "step": 0.1, "value": 1.2},
            {"key": "ay", "label": "Objective: weight on y", "type": "range",
             "min": -2, "max": 2, "step": 0.1, "value": 0.8},
            {"key": "r", "label": "Constraint radius", "type": "range",
             "min": 0.5, "max": 2.6, "step": 0.1, "value": 1.6},
        ],
    },
    [
        "At an unconstrained optimum the gradient is zero. At a constrained one "
        "it need not be &mdash; it only has to point <em>along</em> the constraint's gradient.",
        "<code class='mono-font'>&nabla;f = &lambda; &nabla;g</code>. That "
        "proportionality is the whole method.",
        "Geometrically: the level line of the objective is tangent to the "
        "constraint. If it crossed, you could slide along and do better.",
        "&lambda; is the <strong>shadow price</strong> &mdash; how much the "
        "optimum improves per unit of loosened constraint.",
    ],
    """
title: Lagrange Multipliers
intro: Optimising under a constraint, and the multiplier that turns out to be worth as much as the answer.

## Why the usual rule stops working

Unconstrained: find where the gradient is zero.

Constrained: that rule fails immediately, because the unconstrained optimum is
usually somewhere the constraint forbids. On the circle above, the objective
increases forever in one direction and its gradient is never zero anywhere.

## The condition

Look at where the level lines meet the circle.

At most points they **cross**. Crossing means you can slide along the circle and
move to a better level line, so you are not at the optimum.

At the optimum they are **tangent** &mdash; touching without crossing. Sliding
either way makes things worse.

Tangency means the two gradients are parallel:

```
grad f  =  lambda * grad g
```

That is the method entire. Solve it together with the constraint itself and you
have the candidate points.

Drag the objective weights and watch the marked point travel around the circle,
staying exactly where the family of parallel lines grazes it.

## The multiplier is the interesting part

`lambda` looks like bookkeeping. It is not: it is the **shadow price** of the
constraint &mdash; the rate at which the optimal value improves as the
constraint is relaxed.

Drag the radius control. The optimum's value rises, and the readout's `lambda`
says how fast per unit of radius.

In economics that is literally a price: how much more profit one more unit of
capacity is worth, and therefore what you should be willing to pay for it. In
machine learning it is the same quantity under different names &mdash; the
regularisation strength in ridge regression, and the dual variables in an SVM
that identify exactly which points are support vectors.

A `lambda` of zero says the constraint is not binding: you would have chosen
that point anyway, and loosening it buys nothing.

## Where it shows up

**Ridge regression.** "Minimise error subject to the coefficients being small"
is a constrained problem; the penalised form everyone actually writes is its
Lagrangian, and the penalty weight is `lambda`.

**Support vector machines.** The dual formulation is Lagrangian, the multipliers
are per-training-point, and the ones that come out non-zero *are* the support
vectors.

**Maximum entropy.** Finding the distribution with the most entropy subject to
matching known moments produces the exponential family, and the multipliers
become its natural parameters.

**PCA.** Maximising variance subject to unit-length direction gives
`Cv = lambda v` &mdash; the multiplier turns out to be the
[eigenvalue](eigenvalues_and_eigenvectors.html).

**Physics and economics** throughout, wherever something is optimised under a
budget.

## Inequalities

Real constraints are often `g(x) <= c` rather than `g(x) = c`, and the extension
is the **KKT conditions**. The addition worth remembering is *complementary
slackness*: for each constraint, either it is tight and its multiplier may be
non-zero, or it is slack and its multiplier is zero.

That is what makes SVMs sparse. Points comfortably on the correct side of the
margin have slack constraints, so their multipliers are zero, so they contribute
nothing to the solution. Only the points pressed against the margin survive.

## Where it goes wrong

**Forgetting it finds stationary points, not maxima.** The condition holds at
constrained minima and saddles too. Check which you have.

**Assuming a solution exists.** An unbounded objective on an unbounded
constraint set has none.

**Reading lambda's sign carelessly.** It depends on how the Lagrangian was
written, and the sign convention differs between texts.

**Skipping the constraint qualification.** The method assumes the constraint
gradients are well behaved at the solution; at a cusp or where constraints are
degenerate it can fail.

## Optimise with a rule you are not allowed to break

The closest point on a line to the origin, found three ways: by brute force, by substitution, and by the multiplier condition. All three agree, and the multiplier turns out to mean something.

```python-run
import numpy as np

# minimise x^2 + y^2  subject to  3x + 4y = 25
def f(x, y):     return x ** 2 + y ** 2
def g(x, y):     return 3 * x + 4 * y - 25

print("brute force along the constraint line:")
xs = np.linspace(-5, 12, 400_001)
ys = (25 - 3 * xs) / 4
vals = f(xs, ys)
i = vals.argmin()
print("  best point (%.4f, %.4f)   f = %.4f" % (xs[i], ys[i], vals[i]))
print()

print("by substitution, then calculus:")
# f(x) = x^2 + ((25-3x)/4)^2
#   df/dx = 2x - 3(25-3x)/8 = 0  ->  16x = 75 - 9x  ->  25x = 75
x_star = 75.0 / 25.0
y_star = (25 - 3 * x_star) / 4
print("  x = %.4f, y = %.4f   f = %.4f" % (x_star, y_star, f(x_star, y_star)))
print()

print("by Lagrange: grad f = lam * grad g, plus the constraint.")
# grad f = (2x, 2y);  grad g = (3, 4)
#   2x = 3 lam ,  2y = 4 lam ,  3x + 4y = 25
A = np.array([[2.0, 0.0, -3.0],
              [0.0, 2.0, -4.0],
              [3.0, 4.0,  0.0]])
b = np.array([0.0, 0.0, 25.0])
x_l, y_l, lam = np.linalg.solve(A, b)
print("  x = %.4f, y = %.4f, lambda = %.4f" % (x_l, y_l, lam))
print("  constraint satisfied: g = %.10f" % g(x_l, y_l))
print()
print("at the solution the two gradients are parallel:")
print("  grad f = %s" % np.round([2 * x_l, 2 * y_l], 4))
print("  grad g = %s   ratio %.4f, %.4f"
      % ([3, 4], 2 * x_l / 3, 2 * y_l / 4))
print()
print("lambda is the price of the constraint -- move the line by one unit")
print("and the optimum value changes by about lambda:")
mins = []
for c in (24.0, 25.0, 26.0):
    xs2 = np.linspace(-5, 12, 200_001)
    best = f(xs2, (c - 3 * xs2) / 4).min()
    mins.append(best)
    print("  3x + 4y = %.0f  ->  minimum f = %.4f" % (c, best))
print("  it went up by %.4f then %.4f; lambda is %.4f"
      % (mins[1] - mins[0], mins[2] - mins[1], lam))
print()
print("that is what a multiplier is for: it tells you how much a constraint")
print("is costing you, which is often more useful than the optimum itself.")
```

""",
    [
        {"q": "At a constrained optimum, what is true of the level line and the constraint?",
         "options": ["They cross at right angles", "They are tangent",
                     "The level line is horizontal", "The gradient is zero"],
         "answer": 1,
         "why": "If they crossed you could slide along the constraint onto a better level line. Tangency means the gradients are parallel, which is the condition."},
        {"q": "What does the multiplier lambda measure?",
         "options": ["The size of the constraint",
                     "How much the optimal value improves per unit of loosened constraint",
                     "The distance to the optimum",
                     "The curvature of the objective"],
         "answer": 1,
         "why": "The shadow price. In economics it is literally what an extra unit of capacity is worth; in ridge regression it is the regularisation strength."},
        {"q": "Why are SVMs sparse?",
         "options": ["The kernel is sparse",
                     "Complementary slackness makes the multiplier zero for every point whose constraint is slack",
                     "Only a few points are stored",
                     "The objective is convex"],
         "answer": 1,
         "why": "Points comfortably on the correct side contribute nothing to the solution. Only the ones pressed against the margin have non-zero multipliers - those are the support vectors."},
    ],
)


# ---------------------------------------------------------------------------
# 17. Jensen's inequality
# ---------------------------------------------------------------------------
topic(
    "jensens_inequality",
    "Jensen's Inequality",
    "Probability",
    "The average of a curve is not the curve of the average. The gap has a "
    "direction, a size, and a great many consequences.",
    _svg('<path d="M20 72 C 52 72, 66 26, 96 20" fill="none" stroke="%s" stroke-width="2"/>' % A
         + _line(30, 68, 96, 20, M, 1.8, "4 3")
         + _dot(63, 44, M, 4) + _dot(63, 54, A, 4)
         + _line(63, 44, 63, 54, A, 1.4)
         + _txt(80, 86, "chord above curve", M, 7)),
    {
        "demo": "jensen",
        "controls": [
            {"key": "curve", "label": "Curvature (negative = concave)", "type": "range",
             "min": -1.0, "max": 1.2, "step": 0.05, "value": 0.80},
            {"key": "spread", "label": "Spread of the distribution", "type": "range",
             "min": 0.0, "max": 1.5, "step": 0.05, "value": 1.10},
        ],
    },
    [
        "For a <strong>convex</strong> f: "
        "<code class='mono-font'>E[f(X)] &ge; f(E[X])</code>. For concave, the "
        "inequality reverses.",
        "Geometrically it is the chord lying above the curve &mdash; the same "
        "picture as <a href='convexity_and_optimisation.html'>convexity</a> itself.",
        "The gap grows with the spread of X and with the curvature of f. It is "
        "zero only if one of them is zero.",
        "It is the reason a log-likelihood can be bounded from below, which is "
        "the reason EM and variational inference work at all.",
    ],
    """
title: Jensen's Inequality
intro: Why averaging before and after a curve gives different answers, and what that difference is used for.

## The statement

For a convex function `f` and a random variable `X`:

```
E[f(X)]  >=  f(E[X])
```

Transform first and average, and you get at least as much as averaging first
and transforming. For a concave function the inequality reverses.

## Why it is obvious once seen

Take a distribution that puts half its weight at each of two points &mdash; the
two grey dots in the visualisation.

`f(E[X])` is the curve evaluated at the midpoint: the orange dot **on** the
curve.

`E[f(X)]` is the average of the two heights: the midpoint of the **chord**, the
lighter dot above.

Convex means the chord lies above the curve. So the chord's midpoint is above
the curve's point, which is the inequality, drawn.

Two controls change the gap. **Curvature**: flatten the function toward a
straight line and the chord lies on the curve, so the gap vanishes &mdash; for a
linear `f`, expectation passes straight through. **Spread**: shrink the
distribution to a point and the two dots merge, and the gap vanishes again.

The gap is zero exactly when the function is linear or the variable is constant,
and grows with both.

## Consequences worth having

**The mean of ratios is not the ratio of means.** `1/x` is convex on the
positives, so `E[1/X] >= 1/E[X]`. Averaging speeds in miles per hour to get
average pace is wrong in a specific, predictable direction, and the same trap
appears in averaging rates, ratios and per-unit costs throughout applied work.

**AM-GM.** Applying Jensen to the concave logarithm gives that the arithmetic
mean is at least the geometric mean, immediately.

**Log-loss and calibration.** `-log` is convex, so averaging log-losses
penalises confident mistakes far more than the raw error rate does. That is a
design choice, and Jensen is why it works.

**Portfolio returns.** Compounding is multiplicative, so the geometric mean is
what you keep and the arithmetic mean is what gets advertised. Volatility drag
is Jensen's gap.

## The one that matters most

Jensen is why **EM** and **variational inference** exist.

Both want to maximise a log-likelihood containing a sum inside a logarithm
&mdash; `log sum_z p(x, z)` &mdash; which does not decompose and cannot be
optimised directly.

The move is to write that sum as an expectation, then use Jensen on the concave
`log` in the other direction:

```
log E[ ... ]  >=  E[ log ... ]
```

The right-hand side is a **lower bound** on the thing you wanted, it decomposes
into terms you can differentiate, and maximising it cannot decrease the true
objective.

That bound is the ELBO &mdash; the evidence lower bound &mdash; and it is the
objective a variational autoencoder trains on. EM alternates between tightening
the bound and maximising it, which is exactly the two steps in
[the Gaussian mixture module](gaussian_mixture_models.html).

The gap between the bound and the truth is the KL divergence between the
approximate posterior and the real one, which ties Jensen directly to
[cross-entropy and KL](cross_entropy_and_kl_divergence.html): non-negativity of
KL *is* Jensen applied to the log.

## Where it goes wrong

**Averaging a transformed quantity and reporting it as the transform of the
average.** Log-scale averages, rates and ratios all bite here.

**Getting the direction wrong.** Convex up, concave down. `log` and `sqrt` are
concave; `exp`, `x^2` and `1/x` (on positives) are convex.

**Assuming the bound is tight.** The ELBO can sit far below the true likelihood,
and a rising ELBO does not prove the likelihood rose by as much.

**Forgetting that equality needs linearity or a constant.** Nothing else gives
it.

## The average of the function is not the function of the average

Three concrete cases where swapping those two operations changes the answer, including the one that quietly costs money.

```python-run
import numpy as np

rng = np.random.default_rng(0)
x = rng.normal(5.0, 2.0, 200_000)

print("for a convex function, E[f(x)] >= f(E[x]):")
for name, f in (("x^2", lambda v: v ** 2),
                ("e^x/50", lambda v: np.exp(v) / 50),
                ("|x-5|", lambda v: np.abs(v - 5.0))):
    print("  f = %-7s E[f(x)] = %10.4f   f(E[x]) = %10.4f   gap %+9.4f"
          % (name, f(x).mean(), f(x.mean()), f(x).mean() - f(x.mean())))
print()
print("for a concave function it flips the other way:")
for name, f in (("log(x) ", lambda v: np.log(np.clip(v, 0.01, None))),
                ("sqrt(x)", lambda v: np.sqrt(np.clip(v, 0.0, None)))):
    print("  f = %-7s E[f(x)] = %10.4f   f(E[x]) = %10.4f   gap %+9.4f"
          % (name, f(x).mean(), f(x.mean()), f(x).mean() - f(x.mean())))
print()
print("the gap is zero only for straight lines:")
f = lambda v: 3 * v + 7
print("  f = %-7s E[f(x)] = %10.4f   f(E[x]) = %10.4f   gap %+9.4f"
      % ("3x+7", f(x).mean(), f(x.mean()), f(x).mean() - f(x.mean())))
print()

print("the expensive version -- returns compound, so they multiply:")
returns = np.array([1.50, 0.60] * 10)          # +50%, then -40%, ten times
print("  arithmetic mean return: %.4f  (looks like a %.0f%% gain per period)"
      % (returns.mean(), 100 * (returns.mean() - 1)))
print("  actually multiplied out: %.4f of your starting money" % returns.prod())
print("  geometric mean:         %.4f" % returns.prod() ** (1 / len(returns)))
print()
print("log is concave, so the average of the logs sits below the log of the")
print("average -- which is exactly the gap between the two 'mean returns'.")
```

""",
    [
        {"q": "For a convex f, which is larger?",
         "options": ["f(E[X])", "E[f(X)]", "They are equal", "It depends on the distribution"],
         "answer": 1,
         "why": "Convex means the chord lies above the curve, so the average of the heights sits above the height at the average. Concave reverses it."},
        {"q": "When is the gap exactly zero?",
         "options": ["When X is normal",
                     "When f is linear, or X is constant",
                     "When the variance is small",
                     "Never"],
         "answer": 1,
         "why": "Flatten the curve to a line and the chord lies on it; shrink the distribution to a point and the two dots merge. Nothing else gives equality."},
        {"q": "How does Jensen make variational inference possible?",
         "options": ["It bounds the variance",
                     "It turns log of an expectation into a tractable lower bound - the ELBO - that decomposes and can be maximised",
                     "It proves convergence of EM",
                     "It removes the latent variables"],
         "answer": 1,
         "why": "log sum_z p(x,z) cannot be optimised directly. Jensen on the concave log gives a bound that does decompose, and maximising it cannot decrease the true objective."},
    ],
)


# ---------------------------------------------------------------------------
# 18. Markov chains
# ---------------------------------------------------------------------------
topic(
    "markov_chains",
    "Markov Chains",
    "Probability",
    "A system that forgets everything except where it is now. Start it "
    "anywhere and it settles in the same place.",
    _svg('<circle cx="34" cy="52" r="13" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + '<circle cx="80" cy="26" r="13" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + '<circle cx="126" cy="52" r="13" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + _line(45, 46, 68, 32, M, 1.2) + _line(92, 32, 115, 46, M, 1.2)
         + _line(47, 56, 113, 56, M, 1.2)
         + _txt(80, 84, "only where you are now", M, 7)),
    {
        "demo": "markov",
        "controls": [
            {"key": "start", "label": "Starting state", "type": "select", "value": "0",
             "options": [{"value": "0", "label": "Start in state A"},
                         {"value": "1", "label": "Start in state B"},
                         {"value": "2", "label": "Start in state C"}]},
            {"key": "a", "label": "Leave A with probability", "type": "range",
             "min": 0.05, "max": 0.95, "step": 0.05, "value": 0.30},
            {"key": "b", "label": "Leave B with probability", "type": "range",
             "min": 0.05, "max": 0.95, "step": 0.05, "value": 0.25},
            {"key": "c", "label": "Leave C with probability", "type": "range",
             "min": 0.05, "max": 0.95, "step": 0.05, "value": 0.40},
        ],
    },
    [
        "The <strong>Markov property</strong>: the next state depends only on "
        "the current one, not on how you arrived.",
        "A <strong>transition matrix</strong> holds the probabilities. Each row "
        "sums to 1, because you must go somewhere.",
        "Iterating it converges to a <strong>stationary distribution</strong> "
        "&mdash; the eigenvector of P' with eigenvalue 1.",
        "Change the starting state and the curves start in different places and "
        "arrive at the same one. That is the point.",
    ],
    """
title: Markov Chains
intro: Memoryless processes, the distribution they settle into, and why so many algorithms are one.

## The property

A process is **Markov** when the next state depends only on the current state,
not on the path that led there. The present screens off the past.

That is a strong assumption and a liberating one. Instead of a history of
arbitrary length you carry one thing &mdash; where you are &mdash; and
everything about the future follows from it.

## The transition matrix

Collect the probabilities into a matrix `P`, where `P[i][j]` is the chance of
moving from state `i` to state `j`. Every row sums to 1, because from any state
you go somewhere, possibly back to where you were.

If the current distribution over states is a row vector `d`, then after one step
it is `d P`. After `k` steps, `d P^k`. That is all the arithmetic there is, and
the visualisation is doing exactly it, forty steps at a time.

## Convergence

Watch the three curves. They start apart &mdash; all the probability on one
state &mdash; and within a few steps they flatten out and stop moving. The
readout shows the last step changing things by around 10&#8315;&#185;&#8304;.

Now change the starting state. The curves begin somewhere completely different
and **arrive at the same values**.

That limit is the **stationary distribution**: the `pi` with `pi P = pi`. Read
as an eigenvector problem, it is the left eigenvector of `P` with eigenvalue 1,
and the [eigenvalue module](eigenvalues_and_eigenvectors.html) is the same
mathematics in another costume.

The convergence is not automatic. It needs the chain to be **irreducible** &mdash;
every state reachable from every other &mdash; and **aperiodic**, not trapped in
a fixed cycle. Drag a transition probability to its minimum and convergence
slows visibly; a chain that could not leave a state at all would never mix.

The speed is governed by the second-largest eigenvalue: the closer it is to 1,
the slower the mixing. That number has a name, the *spectral gap*, and it is
what people mean by a chain mixing slowly.

## Where they appear

**PageRank** is the stationary distribution of a random surfer following links.
The damping factor exists to make the chain irreducible, so a page with no
outbound links cannot swallow all the probability.

**MCMC** &mdash; Metropolis-Hastings, Gibbs sampling, Hamiltonian Monte Carlo
&mdash; runs the idea backwards: construct a chain whose stationary distribution
*is* the posterior you want, run it, and treat the states it visits as samples.
Nearly all Bayesian computation is this.

**Hidden Markov models** put a Markov chain behind observations you can see, and
were the backbone of speech recognition for decades.

**Reinforcement learning.** A Markov decision process is a Markov chain with
actions and rewards attached. The "Markov" in MDP is this property, and it is
what makes value functions of the state alone sufficient.

**n-gram language models** are Markov chains over words &mdash; and their
limitation is precisely the property: a bigram model cannot remember anything
beyond the previous word, which is why long-range coherence needed something
else.

## Where it goes wrong

**Assuming the property holds.** Most real processes have memory. Widening the
state to include recent history restores the property at the cost of a much
larger state space.

**Assuming convergence.** Check irreducibility and aperiodicity.

**Stopping an MCMC run too early.** Samples before the chain has mixed reflect
where you started, which is what burn-in discards and why convergence
diagnostics exist.

**Confusing the stationary distribution with the most likely state.** It is the
long-run fraction of time spent in each state, not a prediction of where the
chain is now.

## Walk the chain to its steady state

A three-state weather chain, stepped forward until the distribution stops moving, then checked against the eigenvector that predicts it.

```python-run
import numpy as np

states = ["sunny", "cloudy", "rainy"]
#  rows: from        to:  sunny cloudy rainy
P = np.array([[0.80, 0.15, 0.05],     # from sunny
              [0.30, 0.45, 0.25],     # from cloudy
              [0.20, 0.35, 0.45]])    # from rainy

print("each row sums to 1:", P.sum(axis=1))
print()

p = np.array([1.0, 0.0, 0.0])         # start certain it is sunny
print("%5s  %8s %8s %8s" % ("step", *states))
for step in range(9):
    print("%5d  %8.4f %8.4f %8.4f" % (step, *p))
    p = p @ P
print()
print("keep going and it stops moving:")
for _ in range(200):
    p = p @ P
print("  steady state %s" % np.round(p, 6))
print()
print("the chain forgets where it started:")
q = np.array([0.0, 0.0, 1.0])          # start certain it is rainy
for _ in range(200):
    q = q @ P
print("  from rainy   %s" % np.round(q, 6))
print()
vals, vecs = np.linalg.eig(P.T)
v = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
print("  left eigenvector for eigenvalue 1: %s" % np.round(v / v.sum(), 6))
```

""",
    [
        {"q": "What does the Markov property say?",
         "options": ["Every state is equally likely",
                     "The next state depends only on the current one, not on the path that led there",
                     "The chain always converges",
                     "Transitions are symmetric"],
         "answer": 1,
         "why": "The present screens off the past, so you carry one thing - where you are - instead of a history of arbitrary length."},
        {"q": "What is the stationary distribution?",
         "options": ["The starting distribution",
                     "The pi satisfying pi P = pi - the left eigenvector of P with eigenvalue 1",
                     "The most likely state",
                     "The uniform distribution"],
         "answer": 1,
         "why": "It is where the chain settles regardless of where it started, provided the chain is irreducible and aperiodic."},
        {"q": "What does MCMC do with this idea?",
         "options": ["Runs it forwards to predict states",
                     "Constructs a chain whose stationary distribution is the posterior it wants, then treats the visited states as samples",
                     "Estimates the transition matrix from data",
                     "Finds the second-largest eigenvalue"],
         "answer": 1,
         "why": "Nearly all Bayesian computation is this, which is also why burn-in and convergence diagnostics matter: early samples reflect the starting point, not the target."},
    ],
)


# ---------------------------------------------------------------------------
# 19. Matrix calculus
# ---------------------------------------------------------------------------
topic(
    "matrix_calculus",
    "Matrix Calculus",
    "Calculus",
    "The handful of derivative identities every gradient in machine learning "
    "is assembled from, and the shape rule that catches the mistakes.",
    _svg(_box(18, 30, 30, 34, fill=S, stroke=B, sw=1.5) + _txt(33, 51, "W", A, 10)
         + _txt(58, 50, "&#8594;", M, 11)
         + _box(72, 30, 30, 34, fill=S, stroke=A, sw=1.5) + _txt(87, 51, "dL", A, 9)
         + _txt(112, 50, "same", M, 7) + _txt(112, 60, "shape", M, 7)
         + _txt(80, 84, "the check that catches everything", M, 7)),
    {
        "demo": "curvature",
        "controls": [
            {"key": "curve", "label": "Quadratic term", "type": "range",
             "min": -1.0, "max": 1.5, "step": 0.05, "value": 0.5},
            {"key": "slope", "label": "Linear term", "type": "range",
             "min": -3, "max": 3, "step": 0.1, "value": 1.0},
            {"key": "at", "label": "Evaluate at x", "type": "range",
             "min": -2.5, "max": 2.5, "step": 0.1, "value": -0.6},
        ],
    },
    [
        "The gradient of a scalar with respect to a matrix has the "
        "<strong>same shape as that matrix</strong>. That single rule catches "
        "most errors.",
        "<code class='mono-font'>d(a'x)/dx = a</code> and "
        "<code class='mono-font'>d(x'Ax)/dx = (A + A')x</code> are the two "
        "identities almost everything else is built from.",
        "For a linear layer <code class='mono-font'>y = Wx</code>, the weight "
        "gradient is <code class='mono-font'>dL/dW = (dL/dy) x'</code> &mdash; an outer product.",
        "The demonstration is the scalar case, because the shapes are the only "
        "thing that changes and the calculus underneath does not.",
    ],
    """
title: Matrix Calculus
intro: The short list of identities behind every gradient you will write, and the dimension check that makes them safe.

## Why it needs its own name

Nothing here is new calculus. Differentiating `x'Ax` is the
[product rule](the_chain_rule.html) and
[partial derivatives](partial_derivatives_and_gradient.html) applied to a sum,
and you could always expand into indices and grind it out.

What matrix calculus adds is **notation that stays compact** as the objects grow,
plus a small collection of identities worth memorising so you never expand
anything.

The demonstration on this page is deliberately one-dimensional. The calculus
underneath is the same in any number of dimensions; it is only the shapes that
change, and the shapes are the part you have to be careful about.

## The shape rule

The single most useful fact, and the one that catches almost every mistake:

**The gradient of a scalar with respect to something has the same shape as that
something.**

A loss is a scalar. Differentiate it by a 784&times;128 weight matrix and the
result is 784&times;128. By a length-128 bias vector, and it is length 128.

This is why gradient descent can write `W -= lr * dW` at all: the update has to
have the same shape as the thing it updates. It is also the fastest debugging
tool available. If a hand-derived gradient comes out the wrong shape, the
derivation is wrong, and you know before running anything.

Two conventions exist for laying out derivatives &mdash; numerator layout and
denominator layout &mdash; and they differ by a transpose. Papers rarely say
which they use. The shape rule resolves it every time: whichever orientation
matches the parameter is the one meant.

## The identities

Almost everything reduces to these:

| Expression | Derivative with respect to x |
|---|---|
| `a'x` | `a` |
| `x'a` | `a` |
| `x'x` | `2x` |
| `x'Ax` | `(A + A')x`, which is `2Ax` when A is symmetric |
| `Ax` (Jacobian) | `A` |

And two more, with respect to a matrix:

| Expression | Derivative with respect to W |
|---|---|
| `a'Wb` | `ab'` |
| `tr(W'A)` | `A` |

The pattern in the first table is worth noticing: they are the matrix versions
of `d(ax)/dx = a` and `d(ax^2)/dx = 2ax`. The `(A + A')` appears because both
copies of `x` in `x'Ax` contribute, and when `A` is symmetric they contribute
identically.

## Working an example

Least squares, from the identities alone.

```
L = ||Ax - b||^2 = (Ax - b)'(Ax - b)
  = x'A'Ax - 2b'Ax + b'b
```

Differentiate term by term. The first is `x'Mx` with `M = A'A`, which is
symmetric, giving `2A'Ax`. The second is linear in `x`, giving `-2A'b`. The
third has no `x`.

```
dL/dx = 2A'Ax - 2A'b
```

Set it to zero and you have the normal equations, `A'Ax = A'b` &mdash; the
formula [the QR module](qr_decomposition.html) then explains why you should not
solve directly.

## The layer everyone needs

For a linear layer `y = Wx + b` with loss `L`:

```
dL/dW  =  (dL/dy) x'        an outer product
dL/db  =  dL/dy
dL/dx  =  W' (dL/dy)        passed back to the previous layer
```

Three lines, and they are the whole of backpropagation through a dense layer.

Check them against the shape rule. If `dL/dy` is `m`-long and `x` is `n`-long,
the outer product is `m`&times;`n` &mdash; the shape of `W`. And `W'` is
`n`&times;`m`, so `W'(dL/dy)` is `n`-long, matching `x`. Every term lands where
it should, and if it does not, something is transposed.

The transpose in that last line is why the backward pass is sometimes described
as running the network in reverse: the same weights, applied the other way
round.

## Where it goes wrong

**Mixing layout conventions mid-derivation.** Pick one, and use the shape rule
to check.

**Forgetting that `x'Ax` gives `(A + A')x`.** The shortcut `2Ax` is only valid
for symmetric `A`.

**Deriving without checking shapes.** It costs seconds and catches most errors.

**Trusting a hand derivative without a numerical check.** Compare against a
finite difference on a small random input. Every framework ships a gradient
checker for this, and it is worth using when writing a custom operation.

## The four gradients you keep meeting

Every rule here is checked numerically rather than quoted. These four cover most of what a backward pass computes.

```python-run
import numpy as np

rng = np.random.default_rng(0)

def num_grad(fn, x, h=1e-6):
    g = np.zeros_like(x)
    it = np.nditer(x, flags=["multi_index"])
    while not it.finished:
        i = it.multi_index
        up, dn = x.copy(), x.copy()
        up[i] += h; dn[i] -= h
        g[i] = (fn(up) - fn(dn)) / (2 * h)
        it.iternext()
    return g

x = rng.normal(size=4)
a = rng.normal(size=4)
A = rng.normal(size=(4, 4))
A = A + A.T                      # symmetric, so the quadratic rule is clean

checks = [
    ("d(a.T x)/dx = a",
     lambda v: a @ v,            lambda v: a),
    ("d(x.T x)/dx = 2x",
     lambda v: v @ v,            lambda v: 2 * v),
    ("d(x.T A x)/dx = 2Ax  (A symmetric)",
     lambda v: v @ A @ v,        lambda v: 2 * A @ v),
    ("d(||x||)/dx = x/||x||",
     lambda v: np.linalg.norm(v), lambda v: v / np.linalg.norm(v)),
]

for name, fn, closed in checks:
    n, c = num_grad(fn, x), closed(x)
    print("%-38s max diff %.2e" % (name, np.abs(n - c).max()))
print()

print("the one that matters most: a linear layer's weight gradient.")
W = rng.normal(size=(3, 4))
inp = rng.normal(size=4)
target = rng.normal(size=3)

def loss(Wm):
    return ((Wm @ inp - target) ** 2).sum()

err = W @ inp - target
closed = 2 * np.outer(err, inp)        # dL/dW
print("  numeric vs outer(2*error, input): max diff %.2e"
      % np.abs(num_grad(loss, W) - closed).max())
print()
print("that outer product is why the weight gradient has the same shape as W,")
print("and why a layer needs both its input and its incoming error to update.")
```

""",
    [
        {"q": "What shape is the gradient of a scalar loss with respect to a 784x128 weight matrix?",
         "options": ["128x784", "784x128", "A scalar", "784x1"],
         "answer": 1,
         "why": "The same shape as the thing differentiated by - which is why W -= lr * dW type-checks, and the fastest way to catch a wrong derivation."},
        {"q": "What is d(x'Ax)/dx?",
         "options": ["Ax", "(A + A')x", "2A", "A'x"],
         "answer": 1,
         "why": "Both copies of x contribute. The familiar 2Ax is the special case where A is symmetric, which is why it works for A'A in least squares."},
        {"q": "For a linear layer y = Wx, what is dL/dW?",
         "options": ["W' times dL/dy", "The outer product (dL/dy) x'",
                     "dL/dy", "x times dL/dy"],
         "answer": 1,
         "why": "An m-long upstream gradient times an n-long input gives an m-by-n outer product - exactly W's shape. The shape rule confirms it immediately."},
    ],
)


# ---------------------------------------------------------------------------
# 20. Combinatorics
# ---------------------------------------------------------------------------
topic(
    "combinatorics",
    "Combinatorics: Permutations and Combinations",
    "Probability",
    "Counting arrangements, counting selections, and the factorial that "
    "separates them.",
    _svg("".join(_box(20 + i * 15, 66 - h, 11, h, fill=S, stroke=B, sw=1)
                 for i, h in enumerate([3, 9, 20, 32, 38, 32, 20, 9, 3]))
         + _txt(80, 84, "how many ways", M, 7)),
    {
        "demo": "counting",
        "controls": [
            {"key": "n", "label": "n (things to choose from)", "type": "range",
             "min": 2, "max": 24, "step": 1, "value": 12},
            {"key": "k", "label": "k (things chosen)", "type": "range",
             "min": 0, "max": 24, "step": 1, "value": 5},
        ],
    },
    [
        "<strong>Permutations</strong> count arrangements &mdash; order "
        "matters. <code class='mono-font'>n! / (n&minus;k)!</code>",
        "<strong>Combinations</strong> count selections &mdash; order does not. "
        "<code class='mono-font'>n! / (k!(n&minus;k)!)</code>",
        "The two differ by exactly <code class='mono-font'>k!</code>: the number "
        "of orders each selection could have arrived in.",
        "The bars are C(n, k) for every k. Symmetric, because choosing k to "
        "keep is choosing n&minus;k to leave.",
    ],
    """
title: Combinatorics: Permutations and Combinations
intro: The counting that probability is built on, and the one question that decides which formula to use.

## The question to ask first

**Does order matter?**

Three medals from eight runners: gold, silver and bronze are different outcomes
depending on who gets which, so order matters. That is a **permutation**.

Three people for a committee from eight: the same three people are the same
committee however you list them. Order does not matter. That is a
**combination**.

Everything else follows from answering that.

## The formulas

**Permutations** of `k` from `n`:

```
P(n, k)  =  n! / (n - k)!
```

There are `n` choices for the first position, `n - 1` for the second, and so on
for `k` positions. The factorial ratio is just that product written compactly.

**Combinations** of `k` from `n`:

```
C(n, k)  =  n! / ( k! (n - k)! )
```

Count the ordered arrangements, then divide by `k!` because each unordered
selection was counted once for every order its members could have appeared in.

The readout makes the relationship concrete: at n = 12, k = 5 the ordered count
is 95,040 and the unordered is 792, and 95,040 / 792 is exactly 120 = 5!.

## Reading the shape

The bars are `C(n, k)` for every `k` from 0 to n.

**Symmetric.** `C(n, k) = C(n, n-k)`, because choosing which `k` to keep is the
same act as choosing which `n - k` to leave.

**Largest in the middle.** There are far more ways to pick half of something
than to pick almost none or almost all.

**Enormous quickly.** Drag `n` to 24 and the middle bar passes two and a half
million. This growth is why brute force over subsets is hopeless past small `n`,
and why the readout switches to scientific notation.

That row of numbers is a row of Pascal's triangle, and the recurrence
`C(n,k) = C(n-1,k-1) + C(n-1,k)` &mdash; either the last item is in your
selection or it is not &mdash; is the standard dynamic-programming way to
compute them without factorials.

## With repetition

A third case, easy to miss. If the same item can be chosen more than once and
order matters &mdash; a 4-digit PIN, where digits may repeat &mdash; the count
is simply `n^k`. The readout gives this alongside.

At n = 10, k = 4 that is 10,000 PINs, against `P(10, 4) = 5,040` if no digit
could repeat.

## Why it matters here

**Binomial probabilities.** The `C(n, k)` in
[the binomial](bernoulli_binomial_poisson.html) is exactly this count &mdash;
the number of orders in which `k` successes could have arrived.

**Hypothesis testing.** Permutation tests build a null distribution by
enumerating or sampling rearrangements of the labels, and the count above says
whether enumeration is feasible.

**Cross-validation.** The number of ways to split data into folds.

**Feature selection.** Choosing `k` features from `n` is `C(n, k)`, which is why
exhaustive search is abandoned almost immediately and greedy or regularised
methods are used instead.

**Complexity arguments.** A great deal of "this is exponential" is this table
growing.

## Where it goes wrong

**Not asking whether order matters.** The commonest error, and it is a factor of
`k!`.

**Computing factorials directly.** `21!` overflows a 64-bit integer, and
`C(n, k)` is usually far smaller than the factorials used to define it. Work in
logarithms, or use the multiplicative recurrence, which is what this page does.

**Forgetting repetition is allowed.** Passwords, dice and sampling with
replacement all permit it.

**Double counting.** When the objects are not all distinguishable the plain
formulas over-count, and the multiset versions are needed instead.

## List them, then count them

Small enough to print every arrangement, so the formulas are checkable rather than memorised.

```python-run
import math
from itertools import permutations, combinations

items = "ABCD"

print("permutations of ABCD taken 2 at a time (order matters):")
perm = list(permutations(items, 2))
print(" ", ["".join(p) for p in perm])
print("  count %d = 4!/(4-2)! = %d" % (len(perm), math.perm(4, 2)))
print()
print("combinations of ABCD taken 2 at a time (order does not):")
comb = list(combinations(items, 2))
print(" ", ["".join(c) for c in comb])
print("  count %d = 4!/(2!*2!) = %d" % (len(comb), math.comb(4, 2)))
print()
print("every combination collapses 2! = 2 permutations:")
print("  %d / %d = %d" % (len(perm), math.factorial(2), len(comb)))
print()
print("this is why the numbers explode:")
for n in (5, 10, 20, 52):
    print("  %2d items: %d orderings, %d hands of 3"
          % (n, math.factorial(n), math.comb(n, 3)))
```

""",
    [
        {"q": "What separates a permutation count from a combination count?",
         "options": ["A factor of n", "A factor of k! - the number of orders each selection could arrive in",
                     "A factor of (n-k)!", "Nothing; they are the same"],
         "answer": 1,
         "why": "At n = 12, k = 5 the ordered count is 95,040 and the unordered is 792, and the ratio is exactly 120 = 5!."},
        {"q": "Why is C(n, k) symmetric in k?",
         "options": ["Because factorials are symmetric",
                     "Choosing which k to keep is the same act as choosing which n-k to leave",
                     "Because the distribution is normal",
                     "It is not symmetric"],
         "answer": 1,
         "why": "The same partition of the set, described from either side - which is why the bars mirror around the middle."},
        {"q": "Why should you not compute C(n, k) from factorials directly?",
         "options": ["The formula is wrong",
                     "21! overflows a 64-bit integer, while C(n, k) is usually far smaller than the factorials defining it",
                     "It is slower",
                     "It only works for small k"],
         "answer": 1,
         "why": "Work in logarithms or use the multiplicative recurrence. Pascal's identity C(n,k) = C(n-1,k-1) + C(n-1,k) is the standard dynamic-programming route."},
    ],
)

CHECKS = {"maths/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS}
