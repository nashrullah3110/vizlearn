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
intro: What a set of vectors can reach, when it stops reaching all. Why at right angles is worth so much.

## Span

Given some vectors, the **span** is each point you can reach by scaling them
and adding the results. Nothing more exotic than that: pick a multiple of each,
add them up, and see where you land.

Two vectors in the plane often span the whole plane. Any point you name can
be written as some amount of the first plus some amount of the second, and the
visualisation shows the shaded parallelogram they make.

often &mdash; but not always. Drag one vector until it lines up with the
other and the parallelogram flattens to nothing. Now each combination lands
on a single line, and most of the plane has become unreachable. The vectors
are **linearly dependent**: one is a multiple of the other, so the second adds
no direction the first didn't already have.

## The determinant is the test

You don't have to eyeball it. The readout gives the determinant, which is the
signed area of that parallelogram, and it reaches zero just when the span
merges.

That is the same number the [determinant module](determinant.html) covers as an
area scale factor, seen from another side. A mat whose determinant is zero
squashes the plane onto a line. This Is just why it has no inverse:
a few inputs land on the same output. So Nothing can undo it.

## Basis

A **basis** is a set of vectors that spans the space and is linearly
free &mdash; enough to reach all, with nothing redundant.

Both halves matter. Too few vectors and you can't reach all. Too many
and the form stops being unique, because there's more than one way
to write the same point. A basis is the exact amount.

Once you've one, each point in the space has just one set of coords
in it. That is the whole reason coords work at all, and it's why
"[change of basis](matrix_as_transformation.html)" is a real op
rather than a rearrangement.

The plane needs just two vectors in any basis. Three-dimensional space needs
three. That count is the **dim**, and it doesn't depend on which basis
you choose.

## Orthogonality

Two vectors are **perp** when their [dot
product](vectors_and_dot_product.html) is zero &mdash; the algebraic way of
saying they meet at a right angle. Drag until the readout says so.

Perpness isn't needed for a basis. The default pair above is a
just right good basis and is nowhere near at right angles. But an perp basis
is worth reaching for, because finding the coords of a point turns a
matter of taking one dot product per axis instead of solving a system of
equations.

An **unit-perp** basis adds that each vector has length 1. Then the mat
whose columns are those vectors has a remarkable property: its inverse is its
transpose. Undoing the change costs nothing at all, which is why
unit-perp bases turn up wherever numeric steadiness matters.

The standard basis &mdash; (1, 0) and (0, 1) &mdash; is unit-perp, which is
why plain coords feel so natural.

## Where this shows up

**PCA** finds an unit-perp basis aligned with the directions of greatest
variance in the data. The perpness is the point: the components don't
share, so each one shows a thing the others don't.

**[SVD](singular_value_decomposition.html)** makes two unit-perp bases,
one for the input space and one for the output.

**QR breakdown** exists to manufacture an unit-perp basis from an
any one, and least-squares solvers use it because the resulting system is
far better conditioned than the direct approach.

**Fourier and wavelet transforms** are changes into an perp basis chosen
so the notable structure shows up in a few coords.

## Coordinates, with and without orthogonality

The payoff of an perp basis is concrete: coords become dot products
instead of a system of equations. Take the point `p = (5, 5)` and two bases.

In the plain basis `b1 = (2, 1)`, `b2 = (1, 3)`, finding coords
`c1, c2` with `c1 b1 + c2 b2 = p` means solving

`2c1 + c2 = 5` and `c1 + 3c2 = 5` &rarr; `c1 = 2, c2 = 1`.

That is a `2&times;2` system. In `n` dims it's an `n&times;n` solve.

In the unit-perp basis `q1 = (1, 1)/&radic;2`, `q2 = (1, &minus;1)/&radic;2`,
each coord is a single dot product:

|coordinate|computation|value|
|---|---|---|
|c1|p &middot; q1 = (5+5)/&radic;2|&asymp; 7.07|
|c2|p &middot; q2 = (5&minus;5)/&radic;2|0|

No system to solve &mdash; one dot product per axis, because the axes don't
interfere. This is why an unit-perp basis is worth making (that is what
[QR](qr_decomposition.html) does): the mat of its vectors has its transpose as
its inverse, so projecting onto it and rebuilding from it both cost a single
times, and that is the property numeric methods reach for when steadiness
matters.

The determinant is the warning the coords give before they fail. It's the
signed area of the parallelogram the basis vectors span, and it reaches zero
just when they line up and the span merges to a line &mdash; at which point
most of the plane turns unreachable and no coords exist for it. A
determinant of 0.001 is that same collapse nearly arrived: the basis still
strictly works, but rebuilding a point from its coords cuts by that
tiny number and amplifies each rounding error. This Is the numeric face of the
near-dependence an unit-perp basis is built to avoid.

## Where it goes wrong

**Nearly dependent vectors.** A determinant of just zero is easy to spot. A
determinant of 0.001 is the same problem wearing a disguise. The basis still
strictly works, and all found in it's by number unstable. The
[rule number](singular_value_decomposition.html) is how you measure it.

**given perp means free.** It does &mdash; perp non-zero
vectors are always free. The converse fails, and that is the direction
people assume.

**Losing to norm.** perp gives you the easy inverse only when
the vectors also have length 1.

## Questions people ask

<strong>What is the span of a set of vectors?</strong> It is every vector you can reach by scaling the set and adding the results. Two independent vectors in 3D span a plane, not the whole space.

<strong>How do I tell whether vectors are linearly independent?</strong> Put them in a matrix as columns and check its rank, or its determinant when the matrix is square. Full rank means independent.

<strong>What makes a set of vectors a basis?</strong> They must be linearly independent and span the space. That gives each vector in the space exactly one set of coordinates.

<strong>Are orthogonal vectors always independent?</strong> Yes, provided none of them is the zero vector. Nonzero orthogonal vectors can never be written in terms of one another.

<strong>Why prefer an orthonormal basis?</strong> Coordinates become plain dot products, with no system to solve, and lengths and angles are preserved. That is why PCA, QR and SVD all aim for one.

<strong>Does a vector space have one basis or many?</strong> Many, but they all contain the same number of vectors. That count is the dimension of the space.

## Same vector, three different bases

coords only mean a thing scaled to a basis. Here one fixed vector is written in three of them. An unit-perp basis makes the math trivial.

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
intro: The factorisation that works on each mat. The one worth knowing if you only learn one.

## What every matrix does

Take the unit circle and apply any 2&times;2 mat. The result is always an
ellipse. Not at times &mdash; always, for each mat there's.

That is a strong claim, and the SVD is the reason it holds. each mat can be
written as three ops in sequence:

```
A  =  U  Sigma  V'
```

Read right to left. This Is the order they apply:

**V'** rotates. A rotation does nothing to a circle. This Is why stage 2 in the
visualisation looks the same to stage 1. But watch the two spokes, which
do move. It's choosing which directions are about to be stretched.

**Sigma** stretches along the axes, by the **singular values**. This is where
the circle turns an ellipse.

**U** rotates the ellipse into its final orientation.

Step through the four stages above and the claim stops being abstract. What
you set the four mat entries to, the shape at stage 3 is an axis-aligned
ellipse, each time.

## The singular values

They're the lengths of the ellipse's semi-axes, always non-minus, and
usually listed largest first.

**The largest** is how much the mat can stretch any vector &mdash; its gain
in the worst case.

**The smallest** is how much it can squash one.

**Their ratio** is the **rule number**, and it's the single most handy
number in the readout. A rule number near 1 means the mat treats all
directions roughly alike. A large one means it nearly flattens some direction,
and solving any of it involving that mat will amplify error along it. Drag the
entries until the two singular values are far apart and watch the ellipse become
a sliver.

**A zero singular value** means the mat truly flattens a direction: the
ellipse collapses to a line segment, the mat is singular, and it has no
inverse.

## Why not eigenvectors

The [eigendecomposition](eigenvalues_and_eigenvectors.html) is the more famous
factorisation, and the SVD is the more handy one, for three reasons.

**It always exists.** Eigendecomposition needs a square mat, and even
then not each square mat has one. The SVD exists for each mat of each
shape, including a 1000&times;3.

**Its bases are unit-perp.** Eigenvectors need not be at right angles, and when
they're nearly parallel the breakdown is by number fragile. U and V are
[unit-perp](basis_span_and_orthogonality.html) by build.

**Its values are real and non-minus.** Eigenvals of a real mat can be
complex. Singular values never are.

For a even plus-definite mat the two coincide. This Is why they
are so often confused.

## Low-rank approximation

The property that makes the SVD indispensable: keep only the largest *k*
singular values, set the rest to zero, and times back. The result is
provably the best rank-*k* guess of the first mat, in the
least-squares sense. Not a good one &mdash; the best.

That single fact underwrites a surprising amount:

**PCA** is the SVD of the mean-centred data mat. The principal components
are the right singular vectors and the shown variances are the squared
singular values, which is why any PCA setup you look inside is calling
an SVD.

**Image compression** keeps the top singular values of the pixel mat.

**Latent semantic analysis** factors a term-doc mat and reads the
retained dims as topics.

**Recommender systems** factor a sparse user-item mat into a low-rank
product.

**Noise reduction** works on the assumption that signal focuses in the
large singular values and noise spreads through the small ones.

## Singular values by hand, from A'A

You rarely find an SVD on paper. But Seeing where the singular values come
from drops the mystery. The singular values of `A` are the square roots of the
eigenvals of `A'A`. Take `A = [[3, 0], [4, 5]]`:

`A'A = [[9 + 16,  20], [20,  25]] = [[25, 20], [20, 25]]`.

A even `2&times;2` `[[a, b], [b, a]]` has eigenvals `a + b` and
`a &minus; b`, here `45` and `5`. So the singular values are:

|singular value|from|
|---|---|
|&sigma;&#8321; = &radic;45 &asymp; 6.708|the largest stretch A applies|
|&sigma;&#8322; = &radic;5 &asymp; 2.236|the smallest|

Their ratio, `&radic;(45/5) = 3`, is the rule number: `A` stretches its most
sensitive direction three times more than its least. That is why the unit circle
turns an ellipse with semi-axes 6.708 and 2.236, and why the singular values
are always real and non-minus. They're square roots of eigenvals of
`A'A`, which is even positive semi-definite for any `A`. Eigenvals of `A`
itself could be complex or minus. The SVD's numbers never are, which is half
the reason it's the factorisation to reach for.

This is the machinery under PCA. This Is nothing more than the SVD of the
mean-centred data: the principal directions are the right singular vectors and the
variance each shows is its singular value squared. Keeping only the largest few
&mdash; setting the small singular values to zero and timesing back &mdash;
gives the provably best low-rank guess of the data. This Is the same
op behind image compression, latent-semantic analysis and recommender
factorisations. The small singular values are where noise focuses, so
dropping them often sharpens the signal rather than degrading it.

## Where it goes wrong

**Losing to centre before PCA.** Without subtracting the mean, the first
component points at the mean rather than at the direction of greatest variance.

**Reading a rule number as an error.** It's a sensitivity: it says how
much input error can be amplified, not how much has been.

**given singular values are eigenvals.** They're the eigenvals of A'A,
square-rooted. Not the same object, and not equal except in special cases.

**finding the full SVD when you want the top few.** For a large sparse mat
a truncated solver is orders of magnitude cheaper.

## Questions people ask

<strong>What does the SVD actually give me?</strong> It factors any matrix as U times S times V transpose: a rotation, a stretch along the axes, and another rotation. The singular values in S say how much stretch each direction gets.

<strong>How is SVD different from eigendecomposition?</strong> SVD works on any matrix, including non-square ones, and uses orthogonal factors. Eigendecomposition needs a square matrix and may not have orthogonal eigenvectors.

<strong>How do I get the best low-rank approximation?</strong> Keep the k largest singular values and zero the rest. The Eckart-Young theorem says no other rank-k matrix is closer in the Frobenius or spectral norm.

<strong>How does SVD relate to PCA?</strong> PCA on centred data is the SVD of that data matrix. The right singular vectors are the principal directions and squared singular values give the variances.

<strong>What does a tiny singular value tell me?</strong> The matrix is nearly rank-deficient in that direction. A large ratio of biggest to smallest signals an ill-conditioned problem.

<strong>Is SVD expensive?</strong> Full SVD costs about the cube of the smaller dimension. For large matrices use truncated or randomised SVD to get only the top k components.

## Rebuild a matrix from its biggest pieces

SVD splits any mat into a stack of rank-one layers sorted by importance. Keeping only the first few is what compression and PCA really do.

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
intro: The two mats of derivs each tuner is built on. Why one of them is almost never found.

## From one derivative to a table of them

For a function of one variable the deriv is one number: the slope. The
[chain rule](the_chain_rule.html) and
[partial derivs](partial_derivatives_and_gradient.html) modules cover
that ground.

Real functions have many inputs and often many outputs, and the derivs
have to be organised.

**The grad** applies when there are many inputs and one output &mdash; a
loss function. It's a vector holding one partial deriv per input, and it
points in the direction of steepest grow.

**The Jacobian** applies when there are many outputs too. It's a mat with
one row per output and one column per input, entry (i, j) being how much output
*i* changes when input *j* moves. A grad is a Jacobian with one row.

**The Hessian** is the mat of second derivs of a single-output
function: entry (i, j) is the deriv of the *i*-th partial deriv with
respect to input *j*. It shows how the grad changes as you move.

## What curvature buys you

The visualisation is one-dimensional. Here The grad and the Hessian are
each a single number, so the tie is visible without any mat
form.

The dashed line is the tangent. The first deriv. It says which way
is downhill and how steeply, and it says nothing at all about how long that
remains true.

The second deriv is the missing piece. Drag the curvature control:

**Large plus curvature** is a tight valley. The grad changes quickly, so
a big step overshoots and lands on the far wall.

**Small plus curvature** is a shallow bowl. The grad stays roughly
constant, so a big step is safe and a small one wastes time.

That is just the info a step size wants, and it's why an tuner
that knows the curvature can choose its own step instead of being handed a
learning rate.

**Minus curvature** is a max in that direction. Descent will accelerate
away from it, which is often what you want and is why saddle points are less
dangerous than they sound.

For a multivariable function the Hessian's eigenvals carry the same
info per direction: all plus is a min, all minus a max,
mixed signs a saddle.

## Newton's method, and why nobody runs it on a network

Knowing the curvature suggests an obvious improvement over gradient descent:
step by the grad scaled by the inverse Hessian rather than by a fixed
learning rate. That is **Newton's method**, and near a min it settles
as n&sup2; &mdash; roughly doubling the correct digits each iteration, where
gradient descent plods.

It isn't used for neural networks, for a reason that is pure math.

A model with *n* params has a Hessian with *n*&sup2; entries. At a million
params that is 10&sup1;&sup2; numbers to store, and inverting it costs
about *n*&sup3;. For a model with a billion params the Hessian doesn't fit
in the observable universe, let alone in memory.

So the field uses guesses. **L-BFGS** keeps a low-rank guess built
from recent grads. **Adam** and its relatives keep a main-line guess
&mdash; one number per param rather than a full mat &mdash; which is why
they adapt a per-param step size and why they work at scale. Adam is
at times given as a main-line guess to second-order optimisation,
and that is a fair reading of what it does.

## Backpropagation is Jacobians

each layer of a network is a function with many inputs and many outputs, so
each has a Jacobian. The chain rule says the deriv of the whole network is
the product of them all.

The order of that times is the whole trick. Timesing left to right
&mdash; forward mode &mdash; keeps a full mat at each step. Timesing
right to left &mdash; reverse mode. This Is backpropagation &mdash; starts
from the scalar loss, so each mid stays a **vector**.

That is why training is affordable. The cost of a backward pass is a small
multiple of a forward pass, even so of how many params there are,
because no Jacobian is ever formed in full.

## The curvature test, on two functions

In one dim a plus second deriv means a min and a minus one
a max. In many dims the Hessian's *eigenvals* play that role, and two
small examples show the whole classification.

`f = x&sup2; + xy + y&sup2;` has Hessian `[[2, 1], [1, 2]]`, whose eigenvals are
`2 + 1 = 3` and `2 &minus; 1 = 1`. Both plus. each direction curves
upward, so the stationary point at the origin is a genuine min.

`f = x&sup2; &minus; y&sup2;` has Hessian `[[2, 0], [0, &minus;2]]`, eigenvals
`2` and `&minus;2`.

|function|Hessian eigenvalues|the origin is|
|---|---|---|
|x&sup2; + xy + y&sup2;|3, 1 (all positive)|a minimum|
|x&sup2; &minus; y&sup2;|2, &minus;2 (mixed sign)|a saddle|

The mixed sign is the saddle: up along `x`, down along `y`, so the grad is
zero without it being any kind of extremum. This is just the test
[Cholesky](cholesky_and_positive_definiteness.html) performs cheaply &mdash; a
good factorisation means all eigenvals are plus, confirming a min
&mdash; and it's why, in the millions of dims of a network, stationary
points are almost always saddles: needing *each* eigenval plus at once
turns vanishingly unlikely.

## Where it goes wrong

**Trying to find a Hessian for a large model.** It doesn't fit. Use a
main-line or low-rank guess.

**given a zero grad means a min.** It means a stationary point. The
Hessian's eigenvals tell you which kind.

**Confusing the Jacobian with the grad.** The grad is the special case
of one output. Frameworks expose `jacobian` and `grad` apart for just
this reason.

**Expecting second-order methods to be a drop-in win.** They shine on small,
well-conditioned problems and on batch goals, not on stochastic
mini-batch training where the curvature estimate is noise.

## Questions people ask

<strong>What is the Jacobian?</strong> It is the matrix of all first partial derivatives of a vector-valued function. Row i holds the gradient of output i, so it is the best linear approximation near a point.

<strong>What is the Hessian?</strong> It is the matrix of second partial derivatives of a scalar function. It describes the curvature in every direction.

<strong>What does the Hessian tell me at a critical point?</strong> If it is positive definite you have a local minimum, negative definite a local maximum, and mixed signs a saddle point.

<strong>Why is the Hessian rarely used in deep learning?</strong> It has one entry per pair of parameters. A network with a million parameters would need a trillion-entry matrix, so first-order methods and approximations win.

<strong>How is the Jacobian used in backpropagation?</strong> Each layer's backward pass multiplies the incoming gradient by that layer's Jacobian. Frameworks do it without ever forming the full matrix.

<strong>Is the Hessian the Jacobian of something?</strong> Yes, it is the Jacobian of the gradient. That is why it is symmetric when the second derivatives are continuous.

## First derivatives in a grid, second derivatives in another

The Jacobian collects each first partial deriv of a vector function. The Hessian collects each second partial of a scalar one. Both are built here by number and checked against the closed form.

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
x, y = p
print("\nby hand:")
print(np.round(np.array([[2*x*y, x**2], [5.0, np.cos(y)], [y**3, 3*x*y**2]]), 4))
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
eigs = np.round(np.linalg.eigvalsh(H), 4)
print("eigenvalues %s -> %s" % (eigs,
      "bowl (minimum)" if all(eigs > 0) else "saddle or dome"))
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
intro: The property that makes optimisation easy, what happens without it. Why deep learning works even so.

## The definition

A function is **convex** if, for any two points on it, the straight line
joining them lies on or above the curve. A bowl is convex. A mountain range is
not.

The equal statement in calculus: the second deriv is non-minus
all over. In many dims, the [Hessian](jacobian_and_hessian.html) is
positive semi-definite &mdash; all its eigenvals at least zero.

## Why it matters so much

One consequence carries the entire subject: **in a convex function, each local
min is the global min.**

If you find a point where the grad is zero and the curvature is plus,
you're done. Not "probably done" &mdash; done, with a proof.

Set the bumpiness control to zero and try each starting point on the slider.
each one settles to the same place. The init doesn't matter, the
run is reproducible, and there's a ensure at the end of it.

Now raise bumpiness. The curve grows local minima, and the starting point
starts deciding the answer. Move the start slider at a fixed bumpiness and
watch the final spot jump between basins &mdash; same function, same
method, same learning rate, different answer.

## What convexity buys, concretely

**Ensured settling** to the global optimum, with known rates.

**Reproducibility.** No dependence on init or on the order the data
arrived in.

**Certificates.** You can prove a answer is best rather than hoping.

**Solid stopping.** A small grad really does mean you've arrived.

This is why linear regression, logistic regression, SVMs with convex loss,
ridge and lasso are all so well behaved. Their goals are convex, and the
solvers come with theory rather than folklore.

## And yet deep learning works

Neural network losses are about as non-convex as functions get: millions of
dims, vast numbers of stationary points, no ensures at all. By the
arg above, training should be a lottery.

It isn't, and the explanation that emerged is worth knowing.

**Saddle points, not local minima, dominate.** In high dims, a stationary
point needs *each* eigenval of the Hessian to be plus to be a local
min. With millions of dims that is vanishingly unlikely. Almost each
stationary point has some minus direction, making it a saddle. Saddles are
escapable &mdash; the grad points away along the minus direction, and
noise from mini-batching helps you find it.

**The minima that exist are mostly similar.** Empirically, the many minima of a
large network reach close loss. Which one you land in matters less than
that you landed.

**Overparameterisation flattens the landscape.** Wider networks have more paths
down, and the loss surface turns easier rather than harder as room grows
&mdash; which is the opposite of the intuition.

## The learning rate

The third control shows a separate failure that is often blamed on
non-convexity.

Turn the learning rate up with bumpiness at zero. A just right convex
bowl &mdash; and descent still misbehaves, bouncing between the walls or
diverging fully. Convexity ensures a unique min exists. It doesn't
ensure your step size will find it.

The safe step depends on curvature, which is what
[the Hessian](jacobian_and_hessian.html) measures and what adaptive tuners
guess.

## The chord test, on numbers

Convexity has a meaning you can check by hand: the straight line between any
two points on the curve must lie on or above it. Take `f(x) = x&sup2;` and the
points at `x = &minus;2` and `x = 4`.

The chord's height at the midpoint is the mean of the endpoint values:
`(f(&minus;2) + f(4)) / 2 = (4 + 16)/2 = 10`. The curve's height at that same
midpoint, `x = 1`, is `f(1) = 1`.

|at the midpoint x = 1|value|
|---|---|
|the chord|10|
|the curve|1|

The chord sits above the curve, by 9. It does so for *each* pair of points
you pick &mdash; that is what makes `x&sup2;` convex, and why a single downhill
walk finds its one min. Now try the same on `f(x) = 0.15x&sup2; + 3sin(2x)`:
between two well-chosen points the chord dips *below* the curve, because the
ripples bulge upward past the straight line. One such dip is enough to disqualify
convexity, and it's just the bulge a descent path can get stuck behind. The
test isn't a metaphor. It's an inequality you can test at any two points.

The consequence is the one that separates the well-behaved models from the rest.
Because `x&sup2;`-shaped goals pass the chord test all over, linear
regression, logistic regression and SVMs with convex loss have a single min
that each downhill path reaches. The answer doesn't depend on where you
start. The rippled function fails the test a place, and that single failure is
enough to trap a descent path in a basin that depends fully on its starting
point, which is why a neural network gives a different answer on each restart.

And yet deep networks train anyway, because in millions of dims almost
each stationary point is a saddle rather than a trap &mdash; a genuine min
needs each Hessian eigenval plus at once. This Is vanishingly unlikely
&mdash; and mini-batch noise slides the tuner off the saddles it meets.

## Where it goes wrong

**given a convex loss makes the whole problem convex.** Squared error is
convex in the guesses and non-convex in the weights of a network. What
matters is convexity in the params being optimised.

**Blaming non-convexity for a divergent run.** Check the learning rate first;
it's often that.

**Running once and trusting the result on a non-convex problem.** a few
starts, or a schedule with restarts, is the min diligence.

**Expecting convex theory to transfer.** Settling rates for convex problems
say nothing about a deep network.

## Questions people ask

<strong>What is a convex function?</strong> One where the line segment between any two points on its graph lies on or above the graph. A bowl is convex and a double hump is not.

<strong>Why does convexity matter?</strong> Every local minimum of a convex function is a global minimum. Gradient descent with a sensible step size cannot get stuck.

<strong>How do I check convexity?</strong> For a twice-differentiable function, check that the Hessian is positive semi-definite everywhere. In one dimension, check that the second derivative is not negative.

<strong>Is a neural network loss convex?</strong> No, it has many saddle points and local minima. Training works anyway because the minima found in practice tend to be nearly as good as each other.

<strong>What is the effect of the learning rate?</strong> Too small and progress crawls, too large and the iterates overshoot or diverge. On a quadratic, anything above twice the inverse of the largest curvature diverges.

<strong>Are convex problems always easy?</strong> They are reliably solvable, but size still matters. Convex problems with huge data need stochastic or specialised methods.

## One function gradient descent cannot fail on, and one it can

The same tuner, the same settings, run from many starting points on a convex function and then on a bumpy one. Convexity is the property that makes the starting point irrelevant.

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
best = min(found, key=lambda x: f2(x))
print("  %d distinct minima.  best f=%.4f at x=%.3f" % (len(set(found)), f2(best), best))
print()
print("convex: one minimum, every path finds it. non-convex: many.")
print("test: the chord between any two points never dips below the curve.")
mids = np.linspace(0.05, 0.95, 19)
for fn, name in ((f1, "convex"), (f2, "non-convex")):
    chord = [(1-t)*fn(-2)+t*fn(8) for t in mids]
    curve = [fn((1-t)*-2+t*8) for t in mids]
    viol = sum(c < v-1e-9 for c, v in zip(chord, curve))
    print("  %-11s chord below curve at %d of %d points" % (name, viol, len(mids)))
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
    """title: Taylor Series
intro: Replacing a hard function with a polynomial. Being precise about where that is allowed.

## The construction

Pick a point. Build a polynomial that agrees with the function there, then also
agrees with its slope, then its curvature, then the next deriv, and so on.

```
f(x)  ~  f(a) + f'(a)(x-a) + f''(a)(x-a)^2/2! + f'''(a)(x-a)^3/3! + ...
```

Each term pins down one more deriv at `a`. The factorials are there
because differentiating `(x-a)^k` again and again makes `k!`, and cutting by it
cancels just.

Set the terms control to 0 and step it upward. At 0 you've a flat line
at the right height. At 1, the tangent. At 2, a parabola that also has the
right bend. Each step hugs the curve a little further out.

## Local, and only local

The readout gives how far the guess stays within 0.1 of the truth, and
this is the number worth watching.

More terms extend the range. They don't make it infinite, and the extension
gets slower. The polynomial agrees just right at the expansion point and gets
worse with distance, always &mdash; the whole build is built from
info at a single point. So It can't know any of it about elsewhere.

Move the expansion point and the region of match moves with it. That is the
right mental model: a Taylor series is a statement about a zone.

## Where it earns its keep

**Second-order optimisation.** Newton's method is just the two-term
expansion of the loss: rough it as a quadratic near the current point,
jump to that quadratic's min, repeat. All in
[the Hessian module](jacobian_and_hessian.html) is this idea.

**Small-angle guesses.** `sin(x) ~ x` for small `x` is the one-term
expansion, and it's why pendulum equations are solvable at all.

**Backpropagation's justification.** The chain rule is exact, but the arg
that a small weight change makes a proportional loss change is a first-order
expansion.

**numeric methods.** Finite differences, Runge-Kutta integrators and most
error bounds are derived by expanding and discarding.

**exp, log, sin in a standard library.** Not looked up in a table. Tested
from a truncated series with a range reduction in front of it.

## Where it fails

Switch the function control to `1 / (1 + x squared)`.

This function is smooth all over on the real line &mdash; no kinks, no
asymptotes, differentiable as many times as you like. Yet expand it about 0 and
add terms, and beyond about x = 1 the guess doesn't merely fail to
improve. It gets **worse** with each term added.

The reason is invisible from the real line. Viewed over the complex numbers the
function has poles at *i* and *&minus;i*, distance 1 from the origin, and the
radius of settling is the distance to the nearest singularity wherever it
sits. That radius is 1, and no number of real terms escapes it.

This is the Runge effect, and its lesson is hands-on: **smooth on the reals
doesn't mean a Taylor series settles all over.** Adding terms isn't
always progress.

## Where it goes wrong

**Extrapolating far from the expansion point.** The error grows with distance,
and past the radius of settling it grows without bound.

**given more terms is always better.** Not past the radius, and not
by number &mdash; high-order terms involve large factorials and cancelling
quantities, which loses precision in floating point.

**Expanding about the wrong point.** Expand about where you'll test. A
series about 0 is the wrong tool for guessing at x = 5.

**Losing smoothness is needed.** The function needs derivs of each
order at the expansion point. `|x|` has none at 0. There's no series there.

## e to the x, worked by hand

Expand `e^x` about `a = 0`. each deriv of `e^x` is `e^x`, and `e^0 = 1`,
so each coeff is `1/k!` and the series is as clean as they come:

```
e^x  ~  1 + x + x^2/2 + x^3/6 + x^4/24 + ...
```

Test it at `x = 1`. Here The true value is 2.718282, adding one term at a
time:

|terms|value|error|
|---|---|---|
|1|1.0000|1.7183|
|2|2.0000|0.7183|
|3|2.5000|0.2183|
|4|2.6667|0.0516|
|5|2.7083|0.0099|
|6|2.7167|0.0016|

Six terms and the error is under a tenth of a percent. Now the *same six terms*
at `x = 3`, where the truth is 20.0855:

|terms|value|error|
|---|---|---|
|1|1.000|19.09|
|2|4.000|16.09|
|3|8.500|11.59|
|4|13.000|7.09|
|5|16.375|3.71|
|6|18.400|1.69|

Still 8% out. The reason is visible in the term itself: the `k`-th term is
`x^k / k!`, so the numerator grows like `3^k` while the factorial doesn't
overtake it until `k` passes 3. Near the expansion point the terms shrink from
the start. Far from it they **grow first and shrink later**, and you've to
push through that bulge before the series is any use. Matching at `x = 3` the
fit six terms gave at `x = 1` takes eleven.

That is the whole "local, and only local" claim, in numbers: the same
polynomial, unchanged, is great at one distance and unusable at three times
it. It's also why real setups do **range reduction** first &mdash;
`e^3` is found as `e^0.25` raised to a power, not by expanding at 3.

## Questions people ask

**Taylor or Maclaurin?** A Maclaurin series is a Taylor series with the
expansion point at zero. That is the entire difference, and it's why the two
words are used almost alike.

**How many terms do I need?** What makes the first term you dropped small
enough. For a well-behaved alternating series the remainder is bounded by the
size of that next term. This Makes it a truly hands-on stopping rule.
Or else use the Lagrange remainder. This Bounds the error by the largest
`(n+1)`-th deriv anywhere between the expansion point and where you're
testing &mdash; and that bound is why the error grows with distance.

**Why does 1/(1 + x&sup2;) break at x = 1 when it's smooth all over?**
Because the real line is the wrong place to look. Allow complex numbers and the
function blows up at `x = i` and `x = -i`, both at distance 1 from the origin.
A power series settles inside a *disc* reaching the nearest singularity in the
complex plane, so the radius here is 1 even so of how well behaved the
function looks on the reals. The failure is real. The cause is elsewhere.

**Is the Taylor polynomial the best polynomial guess?** No, and this
surprises people. It's the best one *at the expansion point*, where it matches
as many derivs as it has terms. Across an interval it's often beaten
comfortably by a minimax or Chebyshev fit. This Spreads the error evenly
instead of concentrating fit at one spot. numeric libraries use those,
not Taylor, for just this reason.

**Does a Taylor series always settle to the function?** Not always. The
standard counterexample is `e^(-1/x^2)` extended by zero at the origin: each
deriv there's 0, so its series is the same way 0. This Agrees with the
function at just one point. Smooth isn't enough. The property that makes the
series work is called being *analytic*.

## Rebuild a function from its derivatives

Terms added one at a time, with the error after each. The guess is great near the expansion point and hopeless far from it.

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
    """title: Expectation and Variance
intro: The two numbers that summarise a random quantity, and the rules for mixing them.

## Expectation

The **expectation** of a random variable is each value it can take, weighted by
how likely that value is:

```
E[X]  =  sum over x of  x * P(X = x)
```

The [mean, mode and median module](mean_mode_and_median.html) covers the mean
of a dataset you've. This is the mean of a spread you haven't sampled
&mdash; what the mean would settle to given enough draws.

Load the die above and watch E[X] move. Put all the weight on 6 and it turns
6. Spread it evenly and it turns 3.5.

3.5 is the case worth pausing on: a fair die has expectation 3.5, and no die
has ever rolled a 3.5. **The expectation is a balance point, not a
guess.** The spread would balance on a pin at that value, and that
is all the word means.

## Variance

Expectation alone says nothing about spread. Two very different dice can share
one. **Variance** measures the spread:

```
Var(X)  =  E[(X - mu)^2]
```

The expected squared distance from the mean. Squaring is what stops the
plus and minus deviations cancelling, and it's why the units come out
squared &mdash; variance of a height in metres is in metres squared, which is
meaningless as a length. Taking the square root gives the **standard
deviation**, back in the first units. This Is why that is the number
often reported.

The identity worth storing is:

```
Var(X)  =  E[X^2] - (E[X])^2
```

The mean of the squares minus the square of the mean. It's how variance is
found in one pass over data, and it's also the source of a classic
numeric bug: with large values and small variance, the two terms are nearly
equal and subtracting them destroys precision. Welford's method exists to
avoid just this.

## Combining them

The rules for expectation are as good as rules get:

```
E[aX + b]   = a E[X] + b
E[X + Y]    = E[X] + E[Y]        always
```

That second line holds **whether or not X and Y are free**. Linearity of
expectation is plain, and it's the reason a surprising number of
counting args are one line long.

Variance is stricter:

```
Var(aX + b)  = a^2 Var(X)          note: b vanishes, a is squared
Var(X + Y)   = Var(X) + Var(Y)     only if X and Y are independent
```

Shifting a spread doesn't change its spread. This Is why `b` disappears.
Scaling by `a` scales the variance by `a`&sup2;, because variance is in squared
units.

The freedom rule on the sum is where mistakes live. If X and Y move
together, the covariance term reappears:

```
Var(X + Y) = Var(X) + Var(Y) + 2 Cov(X, Y)
```

The [covariance module](covariance_and_correlation.html) covers that term.

## Where it shows up

**The standard error.** The mean of *n* free draws has variance
&sigma;&sup2;/n, straight from the rules above. Its square root is
&sigma;/&radic;n, which is the whole content of
[the sampling spread](sampling_distributions.html).

**Bias-variance breakdown.** Expected squared error splits into bias
squared plus variance plus irreducible noise, using the identity above.

**Portfolio diversification.** Mixing assets reduces variance only when they
aren't just right linked &mdash; the covariance term again.

**Bagging.** Blending *n* models reduces variance by *n* only if their errors
are free, which is why random forests work to decorrelate their trees.

## Where it goes wrong

**Treating the expectation as a likely value.** It need not be attainable at
all.

**Adding variances of linked variables.** The commonest error in this
material.

**Losing the square on the scale factor.** Doubling a variable quadruples
its variance.

**given a variance exists.** Some spreads have none &mdash; the Cauchy
has neither a finite variance nor a finite mean, and sample means of Cauchy
draws never settle.

## Both numbers, worked by hand

Five cards, drawn one at a time with each card equally likely. They're marked
1, 1, 2, 5 and 11.

Build the table. `P(x)` is how often that value appears out of five, and the
last two columns are what the two formulas need:

|x|P(x)|x P(x)|x&sup2; P(x)|
|---|---|---|---|
|1|2/5|0.4|0.4|
|2|1/5|0.4|0.8|
|5|1/5|1.0|5.0|
|11|1/5|2.2|24.2|
|**total**|**1**|**4.0**|**30.4**|

The third column sums to the expectation: **E[X] = 4.0**. Note that no card is
marked 4. The fourth sums to **E[X&sup2;] = 30.4**, and the one-pass identity
gives the variance straight away:

```
Var(X)  =  E[X^2] - (E[X])^2  =  30.4 - 16  =  14.4
```

Now the same number from the meaning, `E[(X - mu)^2]`, squaring each
distance from 4 and weighting it:

```
(1  - 4)^2 = 9    weight 2/5   ->  3.6
(2  - 4)^2 = 4    weight 1/5   ->  0.8
(5  - 4)^2 = 1    weight 1/5   ->  0.2
(11 - 4)^2 = 49   weight 1/5   ->  9.8
                               -------
                                  14.4
```

The same 14.4, by a different route. The standard deviation is
&radic;14.4 = **3.79** &mdash; almost as large as the mean itself, which is the
honest summary of this deck: the mean is 4. The single 11 does most of
the work.

The two routes cost differently. The meaning needs the mean before it can
start, so it's two passes over the data. The identity needs only running totals
of `x` and `x`&sup2;, so it's one. Which is why it's the one that gets
built, and why the precision trap above is worth knowing about.

## Questions people ask

**Why square the deviations instead of taking abs values?** You can, and
that gives the mean abs deviation. This Is a just right good measure of
spread. Squaring wins on grounds of convenience rather than truth: it's
differentiable all over, it makes the variance of a sum break down into a sum
of variances, and it makes the identity above. abs values give none of
those, which is why almost each result in this material is stated for variance.

**Does the expectation have to be a value the variable can take?** No, and
often it isn't. A fair die means 3.5. The deck above means 4 without
holding a 4. Expectation is a balance point of the spread, not a
forecast of any single draw.

**Why does sample variance divide by n &minus; 1?** Because the sample mean is
itself guessed from the same data, and it sits closer to the data than the
true mean does &mdash; it's the value that *cuts* the sum of squared
deviations, so squared distances measured from it are systematically too small.
Cutting by `n - 1` instead of `n` corrects that bias just. With the true
mean known, `n` would be right.

**When can I add variances?** Only when the variables are free, or at
least unlinked. Or else the covariance term is truly there and
dropping it will mislead you, almost always in the direction of thinking you
have less risk than you do.

**Variance or standard deviation in a report?** Standard deviation, nearly
always, because it's in the same units as the data and can be checked to the
mean. Variance is the quantity the algebra is easier in. This Is why it appears
in the derivations and rarely in the conclusions.

## A bet worth taking that usually loses

Expectation and variance found from the meaning, then measured over 400,000 plays. The two numbers say different things, and both matter.

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
intro: The three spreads behind each count. How each is built from the one before it.

## Bernoulli: the atom

One trial, two outcomes, one param. Success with chance `p`, failure
with chance `1 - p`.

Mean `p`, variance `p(1-p)`. That variance is worth a moment: it's largest at
`p = 0.5` and falls to zero at either end. This Says a thing obvious once
stated &mdash; an event that always happens, or never does, isn't random at
all. Drag `p` to 0.02 with Bernoulli selected and watch the variance in the
readout collapse.

each coin flip, click-or-not, churn-or-not and pass-or-fail is a Bernoulli
trial, and it's the atom the other two are assembled from.

## Binomial: counting the successes

Run `n` free Bernoulli trials with the same `p` and count the successes.
That count is **binomial**.

```
P(k successes)  =  C(n, k) * p^k * (1-p)^(n-k)
```

The three factors read right: `p^k` for the successes, `(1-p)^(n-k)` for the
failures, and `C(n, k)` for the number of orders they could have arrived in.

Mean `np`, variance `np(1-p)` &mdash; both straight from
[the rules for mixing](expectation_and_variance.html) `n` free
Bernoulli variables.

Drag `n` upward and the shape turns recognisably bell-like. That is
[the central limit theorem](central_limit_theorem.html) arriving: a binomial is
a sum of free variables. So It must tend to normal. It's why the normal
guess to the binomial exists, and why it needs `np` and `n(1-p)` both
comfortably above about 10 &mdash; near the edges the binomial is skewed and the
even normal fits badly.

**The freedom and constant-`p` assumptions are load-bearing.** Ten coin
flips are binomial. Ten cards drawn without swap aren't, because `p`
changes as the deck depletes. That is the hypergeometric spread.

## Poisson: the limit

Now let `n` grow and `p` shrink together, keeping `np = lambda` fixed. Many
trials, each very unlikely, with a stable expected count.

The binomial settles to the **Poisson**:

```
P(k)  =  e^(-lambda) * lambda^k / k!
```

`n` and `p` have vanished. Only their product lives. That is what makes it
handy. You rarely know how many opportunities there were for an event to occur
&mdash; how many people *could* have visited the site this minute &mdash; but
you can measure the rate.

So Poisson models counts in a fixed window: arrivals per minute, defects per
batch, mutations per genome, goals per match.

Set the spread to Poisson and compare against a binomial with `n = 60`
and `p = 0.05`. Both have mean 3. The shapes are nearly the same. That is
the limit at work.

## The Poisson's signature, and its trap

A Poisson has **mean and variance both equal to lambda**. One param fixes
both, and there's no way to have a Poisson with mean 3 and variance 10.

Real count data very often has variance well above its mean &mdash;
**overdispersion**. Website visits cluster, defects come in bad batches,
accidents cluster around rules. The Poisson assumes events are free
and the rate is constant, and clustering violates both.

Overdispersion is a finding, not an annoyance: it says a thing is varying that
the model treats as fixed. The usual response is a **minus binomial**, which
adds a second param and lets the rate itself be random.

## Where they show up

**A/B testing.** Conversions are binomial. The test is about two `p` values.

**Queueing.** Poisson arrivals are the standard assumption behind almost all
queueing theory.

**Rare-event modelling.** Failures, fraud, defects.

**Naive Bayes for text.** Multinomial and Bernoulli variants match just
to counting words and to noting presence or lack.

**Class imbalance.** A rare positive class is a small `p`, and the variance of
your guess of it's `p(1-p)/n`. Which is why rare classes need so
much more data before a rate guess settles.

## The binomial formula, worked

The formula is best trusted by testing it. Five trials, success chance
0.3, `P(k) = C(5, k) &middot; 0.3^k &middot; 0.7^(5&minus;k)`:

|k|C(5, k)|P(k)|
|---|---|---|
|0|1|0.1681|
|1|5|0.3601|
|2|10|0.3087|
|3|10|0.1323|
|4|5|0.0283|
|5|1|0.0024|

The most likely single outcome is one success, not the mean of 1.5, because the
spread is skewed at `p = 0.3`. The chances sum to just 1 &mdash;
they must, since some number of successes between 0 and 5 always happens &mdash;
and the mean `&Sigma; k&middot;P(k)` works out to `np = 1.5`. The three factors
each do one job: `0.3^k` for the successes, `0.7^(5&minus;k)` for the failures,
and `C(5, k)` for the number of orders in which those successes could have
arrived. Drop the `C(5, k)` and you'd have the chance of one *exact*
sequence. It's there because you asked how many successes, not which trials.

Push `n` up and `p` down together, holding `np` fixed, and this same formula
slides into the Poisson: the single `n` and `p` vanish and only their product
lives, which is why Poisson models counts when you know the rate but not the
number of chances &mdash; arrivals per minute, defects per batch. The signature to
check is that a Poisson forces mean and variance equal. Real counts often have
variance well above the mean (overdispersion), and that gap is a finding, not
noise &mdash; it says a thing the model treats as fixed is really varying.

When overdispersion is real, the usual fix is a minus binomial, which adds a
second param and lets the rate itself vary rather than forcing mean and
variance to be equal &mdash; the Poisson's rigidity is just what it relaxes.

## Where it goes wrong

**Applying a binomial to sampling without swap.** `p` changes. Use the
hypergeometric.

**given Poisson without checking dispersion.** Compare the sample variance
against the sample mean before any of it else.

**Using the normal guess near p = 0 or 1.** The binomial is skewed
there. The guess isn't.

**Losing the fixed window.** A Poisson rate is per unit of a thing. Double
the window and lambda doubles.

## Questions people ask

<strong>What is a Bernoulli trial?</strong> A single experiment with two outcomes, success with probability p and failure otherwise. Its mean is p and its variance is p times (1 - p).

<strong>When is a count binomial?</strong> When you run a fixed number n of independent trials with the same success probability p. The count of successes has mean np and variance np(1 - p).

<strong>When is a count Poisson?</strong> When events arrive independently at a steady average rate and you count them in a window. The mean and the variance are both equal to the rate.

<strong>When does the binomial turn into a Poisson?</strong> When n is large and p is small, with np held fixed. Rare events across many chances are close to Poisson.

<strong>How do I tell if my data is Poisson?</strong> Check that the variance is near the mean. Variance well above the mean is overdispersion, and a negative binomial usually fits better.

<strong>What if the trials are not independent?</strong> Then the binomial variance is wrong. Clustered outcomes, such as patients in one hospital, spread more than the formula predicts.

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
intro: Why the normal spread turns up all over, stated just enough to know when it doesn't.

## What the theorem says

Take repeated samples of size `n` from any group with a finite mean and
variance. Find each sample's mean. Those means have a distribution of their
own, and as `n` grows it approaches a normal spread &mdash; with mean
equal to the group mean and standard deviation `sigma / sqrt(n)`.

The group's own shape doesn't appear in that statement anywhere. It can
be skewed, bimodal, discrete, or wildly irregular.

The group above is on purpose unpleasant: two separate humps and a long
tail. Nothing about it's bell-shaped. Set `n` to 1 and the right-hand panel is
that same shape, because a sample of one *is* a draw from the group.

Now drag `n` upward. By 5 the two humps have merged. By 30 the right-hand panel
is a clean bell, and the fitted normal curve sits on top of the resampled
histogram. Nothing about the group changed.

## Three things it is not

**Not "large samples are most times spread."** The sample isn't normal. It
looks like the group, because that is what it's drawn from. It's the
*mean* that goes normal.

**Not "all is normal."** Heights are roughly normal because they're the
sum of many small free sways. Incomes aren't normal and no amount
of data makes them so.

**Not a licence to skip the group.** It shows the sampling
distribution of a statistic, not the data.

## The square root

The standard deviation of the sample mean. The **standard error** &mdash;
is `sigma / sqrt(n)`. The square root is the hands-on heart of the theorem.

To halve your uncertainty you must **quadruple** your sample. To divide it by
ten you need a hundred times the data. Precision gets costly fast, and this
single fact governs how large a survey has to be, how long an A/B test must run
and why polls stubbornly report margins of around three percent.

[The sampling spread module](sampling_distributions.html) plots that decay
right.

## How large is large enough

The usual rule of thumb is `n = 30`. Like all such rules it's a summary of
a thing more exact.

**Near-symmetric population**: convergence is fast, and 10 may do.

**Strongly skewed**: 30 is not enough. Heavily skewed populations can need
hundreds before the mean is convincingly normal.

**Heavy tails**: worse still, and there is a limit case below.

The honest method is the one on this page: resample and look. Drag `n` and
find where the histogram stops looking lumpy for *your* group.

## When it fails outright

The theorem needs a **finite variance**, and that rule isn't decorative.

The Cauchy spread has none. Nor a finite mean. Mean `n` Cauchy
draws and you get another Cauchy, with just the same spread as one draw. No
amount of blending focuses any of it. The sample mean of a million draws is
no better than the first.

Heavy-tailed spreads that do have a finite variance still settle, but
slowly enough to matter. Money returns are the standard cautionary example:
methods that assume normality of means understate the chance of extreme
outcomes, because settling hasn't really happened at the sample sizes in
use.

## Where it shows up

**trust intervals and t-tests** assume the sampling distribution of the
mean is normal. That assumption is this theorem.

**A/B testing**: a conversion rate is a mean of Bernoulli draws.

**Bootstrapping** exists partly to avoid needing it when it doesn't hold.

**reading error** is often modelled as normal because it's the sum of many
small free errors.

## Standardising a sample mean

The theorem is used, to turn an seen sample mean into a
chance, and the math is short. Suppose a group has mean 50 and
standard deviation 8, and you take a sample of `n = 16`. By the theorem the sample
mean is about normal, centred at 50, with standard error
`8 / &radic;16 = 2`.

Now you see a sample mean of 54. How surprising is that?

`z = (54 &minus; 50) / 2 = 2.0`

The seen mean is two standard errors above the group mean, and for a
normal spread about 2.3% of samples fall that far above by chance alone.
That single `z` is the engine under a one-sample z-test and a trust interval
alike: the interval `54 &plusmn; 1.96 &times; 2` is `[50.08, 57.92]`, which
&mdash; just barely &mdash; excludes 50. Note which quantity did the work: the
standard error, not the group's own spread. The raw data has sd 8, but the
*mean* of sixteen draws has spread 2, and it's that shrinkage by `&radic;n` that
makes an seen difference of 4 look like a lot rather than a little.

Growing the sample sharpens that verdict fast, through the same square root.
At `n = 64` the standard error falls to `8 / 8 = 1`. The same seen mean of
54 now sits `z = 4` standard errors out. A result that was mildly
surprising at sixteen samples turns overwhelming at sixty-four. Nothing about
the group changed. The larger sample simply pins the mean down four times
more tightly than the raw data's spread of 8 would suggest, and that shrinkage is
the entire hands-on content of the theorem.

## Where it goes wrong

**Applying it to the data instead of the statistic.** Extremely common.

**Trusting n = 30 on skewed data.** Check.

**given it applies to the max or the variance.** It's about sums and
means. Extreme values have their own limit theory, and a different family of
limiting spreads.

**Skipping dependence.** The classical version needs free draws. Time
series data often isn't free, and the effective sample size is
smaller than the row count suggests.

## Questions people ask

<strong>What does the central limit theorem say?</strong> The mean of many independent samples is approximately normal, whatever the shape of the original distribution, provided the variance is finite.

<strong>How large must the sample be?</strong> About 30 is a common rule, but it depends on skew. Symmetric data needs far fewer, heavily skewed data may need hundreds.

<strong>Does the data itself become normal?</strong> No. Only the distribution of the sample mean does. The raw values keep their original shape.

<strong>How does the spread of the mean shrink?</strong> The standard error is the standard deviation divided by the square root of n. To halve the error you need four times as many samples.

<strong>When does the theorem fail?</strong> With heavy tails such as the Cauchy distribution, where the variance is infinite, and with strongly dependent samples.

<strong>Why does it matter in practice?</strong> It justifies normal-based confidence intervals and tests for averages, even when you do not know the data distribution.

## Watch it happen

A on purpose lopsided group, and the means of samples drawn from it. The spread of those means shrinks like one over the square root of the sample size.

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
intro: showing a spread by where its values sit rather than by blending them.

## The definition

The **q-th quantile** is the value below which a fraction `q` of the data falls.
The 0.5 quantile is the median: half below, half above. The 0.9 quantile is the
value 90% of the data sits below.

**Percentiles** are the same idea on a 0&ndash;100 scale &mdash; the 90th
percentile is the 0.9 quantile. **Quartiles** cut at 25, 50 and 75, cutting the
data into four equal groups. **Deciles** cut into ten.

## Why not just use the mean

A mean is a balance point. It moves when any of it moves. A quantile depends
only on **order**, and that makes it solid.

Add a single huge value to a dataset and the mean shifts, possibly a lot.
The median barely moves at all. The new value is simply "one more above
the middle", even so of how far above.

That is why median income is reported rather than mean income, why latency is
reported at percentiles, and why the [box plot](#) below exists.

The **IQR** &mdash; Q3 minus Q1 &mdash; is the spread measure that follows from
the same idea. It covers the middle half of the data, and it's unaffected by
any of it in the tails. Standard deviation, being built from squared distances
from the mean, is the opposite: one extreme value moves it a lot.

## Reading the box plot

The second panel is assembled from the quartiles in the first, and each part
of it has a meaning:

**The box** spans Q1 to Q3. So It holds the middle 50% of the data.

**The line inside** is the median. Its spot within the box shows skew: off
centre means the spread leans.

**The whiskers** reach the furthest data points still within 1.5 &times; IQR of
the box edge.

**The dots** are all beyond that.

The 1.5 is a **rule**, not a test. It comes from Tukey, and for a normal
spread it flags about 0.7% of points. Points beyond it are worth
inspecting, and calling them "outliers" makes a claim the rule can't support
&mdash; a skewed spread makes them by build rather than by
error.

Grow the sample size and the number of flagged points grows roughly in
proportion. That alone shows the rule is descriptive.

## Percentiles in practice

**Latency.** No one reports mean response time, because one slow request buried
in a million is invisible in a mean and obvious at p99. Services are given
at p50, p95, p99 and p999 just because the tail is what users notice.

A trap follows right away: **percentiles don't mean.** The p99 of two
servers isn't the mean of their p99s. Aggregating percentiles needs the
underlying spreads or a structure like a t-digest.

**Quantile regression** predicts a chosen quantile rather than the mean. handy
when the cost of over- and under-guess differ, or when you want a
guess interval right.

**Quantile binning** turns a smooth feature into equal-sized buckets, which
is solid to skew in a way that equal-width binning isn't.

**Feature scaling.** `QuantileTransformer` maps a feature to a uniform or normal
spread through its quantiles, and is unaffected by outliers in a way
standardisation isn't.

## A wrinkle worth knowing

There's no single agreed meaning of a sample quantile. With 10 data points,
"the value below which 25% falls" doesn't land on an reading, and there are
a few defensible interpolations. NumPy offers nine methods. R offers the same
nine. The defaults differ between languages, and between `numpy.percentile` and
some SQL engines.

For large samples the differences are negligible. For small ones they aren't,
and two tools can legitimately report different quartiles for the same data.

## The definition ambiguity, on ten numbers

The wrinkle deserves numbers, because it's where two tools disagree on the same
data. Take the ten values `1, 2, 3, &hellip;, 10` and ask for the 25th
percentile. "The value below which 25% falls" doesn't land on an reading, and
the defensible answers differ:

|method|25th percentile|how|
|---|---|---|
|linear interpolation|3.25|position `(n&minus;1)&middot;0.25 = 2.25`, so a quarter of the way from the 3rd value to the 4th|
|nearest-rank|3|the smallest value with at least 25% at or below it|

Both are correct. They answer slightly different questions about what a
"percentile" of a finite sample means. NumPy's default is the linear method, and
it offers nine in total. Other tools default differently, which is why
`numpy.percentile` and a SQL engine can report different quartiles for the same
column. For a thousand points the gap between methods is negligible. For ten it's
0.25 out of a range of 9. This Is enough to change a choice. State the method
when the sample is small and the number matters.

The reason to care sits in the tail. A service's latency is reported at p95 and
p99 just because one slow request in a thousand is invisible in a mean and
obvious in a high percentile. And those percentiles can't be averaged
across servers, because the p99 of two machines isn't the mean of their p99s.
Aggregating them needs the underlying spreads or a structure like a
t-digest. Blending them understates the tail each time. This Is the one error
this whole topic exists to prevent.

There's also no single agreed meaning of a sample quantile: on ten points the
"value below which 25% falls" is a matter of interpolation, and NumPy alone offers
nine methods. On large samples the choice is negligible. On small ones two honest
tools can report different quartiles for the same data.

## Where it goes wrong

**Blending percentiles.** The single most common error, and it always
understates the tail.

**Reading whisker points as errors.** The rule is a drawing rule.

**Checking box plots of very different sample sizes.** More data means more
flagged points, mechanically.

**given your language's default matches another's.** State the method when it
matters.

## Questions people ask

<strong>What is the difference between a quantile and a percentile?</strong> They are the same idea on different scales. The 0.9 quantile is the 90th percentile: the value below which 90 percent of the data lies.

<strong>Is the median a quantile?</strong> Yes, it is the 0.5 quantile, the 50th percentile and the second quartile.

<strong>Why do different tools give different percentiles?</strong> There are several conventions for interpolating between data points when the position falls between two values. The differences shrink as the sample grows.

<strong>Why use the median instead of the mean?</strong> The median ignores how extreme the extremes are. A single huge outlier moves the mean a lot and the median hardly at all.

<strong>What is the interquartile range?</strong> It is the 75th percentile minus the 25th. It measures spread in the middle half of the data and is the basis of the box plot whiskers.

<strong>How should I report skewed data like latency?</strong> Give percentiles such as p50, p95 and p99. The mean hides the slow tail, which is what users actually feel.

## Nobody experiences the mean

Ten thousand response times with a long tail. The mean and the median tell one story. P95 and p99 tell the one your users live in.

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
intro: The idea that makes each trust interval and each p-value mean a thing.

## The statistic is random too

You draw a sample and find its mean. Draw a different sample and you get a
different mean. The statistic is itself a random quantity, and it has a
spread: the **sampling spread**.

This is the conceptual step all in inference rests on. It's also the one
that is easy to skip, because you only ever draw one sample and
never see the spread at all. You reason about what *would* happen
across the samples you didn't take.

The left panel makes it visible by really doing it: 800 samples drawn, each
mean plotted. That histogram is the sampling distribution of the mean, and it's
the object trust intervals show.

## Standard error

The standard deviation of a sampling spread is the **standard error**. For
a sample mean:

```
SE  =  sigma / sqrt(n)
```

This follows right from the [rules for
variance](expectation_and_variance.html): the variance of a sum of `n`
free draws is `n * sigma^2`, cutting by `n` to make the mean scales
variance by `1/n^2`, leaving `sigma^2 / n`, and the square root gives the
formula.

Watch the readout as you drag `n`: the seen spread of the 800 means tracks
the predicted `sigma / sqrt(n)` closely. That isn't a coincidence being
illustrated &mdash; it's an identity being checked.

## Standard deviation is not standard error

These get confused constantly, and the gap isn't subtle.

**Standard deviation** shows the spread of the **data**. It's a property of
the group, and collecting more data doesn't reduce it &mdash; more careful
reading might, but more readings won't.

**Standard error** shows the spread of an **guess**. It shrinks as `n`
grows, because a larger sample pins the guess down better.

A handy test: if the number would change when you collect more data *of the
same kind*, it's a standard error. If it wouldn't, it's a standard deviation.

An error bar on a chart could be either, and the two say fully different
things. Charts that don't label which are unreadable.

## The square root, again

The right-hand panel plots `sigma / sqrt(n)` against `n`, and its shape is the
hands-on content of this page.

It falls steeply at first. Going from 4 samples to 16 halves the error.
Then it flattens. Going from 100 to 400 halves it again, at the cost of three
hundred more readings.

**each halving of uncertainty costs four times the data.** That is why national
polls settle around 1,000 respondents: the marginal precision per person
merges past that point, and the left error is dominated by sampling bias
rather than sampling noise anyway.

More data can't fix a biased sample. A poll of 100,000 people who all answer
the same badly-worded question is just wrong.

## Beyond the mean

each statistic has a sampling spread, not only the mean. Medians,
variances, links and regression coeffs all have one, and the
formulas are often harder or down.

**The bootstrap** exists for just this. Resample your data with swap,
recompute the statistic, repeat thousands of times, and the spread of the
results guesses the sampling spread &mdash; with no formula and almost
no assumptions. It's the same op this page performs, run on your own
sample instead of on a known group.

## Where it shows up

**trust intervals** are built right from the standard error.

**t-tests and z-tests** compare an seen difference against the standard
error of that difference.

**Cross-validation** variance is the sampling distribution of a speed
guess, which is why a single fold's fit is a point with error bars
around it.

**A/B test duration** is a standard error math before it's any of it
else.

## The cost of precision, tabulated

The `sigma / &radic;n` formula has a consequence worth seeing as a table, because
it governs how big each survey and each A/B test has to be. With a group
standard deviation of 10:

|sample size n|standard error|
|---|---|
|4|5.00|
|16|2.50|
|64|1.25|
|256|0.625|

Each row quadruples `n` and the standard error halves &mdash; the `&radic;n` in
the denominator made literal. Going from 4 to 16 buys a lot. Going from 64 to 256
buys the same *factor* of improvement for four times the abs cost. Precision
has diminishing returns, and they diminish predictably: to add one more decimal
place of fit you need a hundred times the data. This is the whole reason
national polls settle near a thousand respondents rather than ten thousand
&mdash; past that point each extra person shrinks the error by too little to be
worth collecting, and any left error is bias. This More data can't touch.

The table also draws the line between the two quantities people confuse. The
group's own spread &mdash; its standard deviation &mdash; is 10 in each row;
collecting more data never moves it. The standard error is the column that shrinks,
because it shows the *guess*, not the data. A handy test: if a number would
change when you collect more readings of the same kind, it's a standard error;
if it wouldn't, it's a standard deviation. An error bar that doesn't say which
it's could mean either, and the two tell fully different stories.

## Where it goes wrong

**Reporting SD when you mean SE, or the reverse.** Label your error bars.

**given freedom.** The `sqrt(n)` assumes free draws. Clustered or
time-series data has a smaller effective `n`.

**Treating a large sample as accurate.** It's precise. Fit is a separate
question, and bias doesn't shrink with `n`.

**Using the formula for statistics that don't have one.** Bootstrap instead.

**Confusing the spread of the data with the spread of the statistic.** The
data can be wildly scattered and the mean can still be pinned down tightly, as
long as the sample is large enough. The two spreads answer different questions.

## Questions people ask

<strong>What is a sampling distribution?</strong> It is the distribution of a statistic, such as the sample mean, across many repeated samples from the same population.

<strong>What is the standard error?</strong> The standard deviation of a statistic's sampling distribution. For the mean it is sigma divided by the square root of n.

<strong>How is standard error different from standard deviation?</strong> Standard deviation describes the spread of the data. Standard error describes how much an estimate would move between samples, and it shrinks as n grows.

<strong>Why does a bigger sample help only slowly?</strong> Because of the square root. Four times the data halves the error, and a hundred times the data cuts it by ten.

<strong>Can I get a sampling distribution without theory?</strong> Yes, with the bootstrap. Resample your data with replacement many times and look at the spread of the statistic.

<strong>Does this apply to statistics other than the mean?</strong> Yes, every statistic has one, including the median, a correlation or a model coefficient. Their shapes and formulas differ.

## The distribution of a statistic, not of the data

Draw a sample, find its mean, write it down, repeat ten thousand times. What you get is a different spread from the one you sampled.

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
intro: What the ninety-five percent really refers to, shown by drawing a thousand of them.

## The construction

Take a sample, find its mean, and put an interval around it:

```
mean  +/-  z * (sample SD / sqrt(n))
```

The `z` depends on the trust level. 1.96 for 95%. The rest is the
[standard error](sampling_distributions.html).

## What the confidence refers to

Here is the statement people often give: *there's a 95% chance the true
mean lies in this interval.*

That is wrong, and the visualisation shows why. The group mean is fixed at
10 &mdash; the dashed line. It isn't random. Your interval is either side of it
or it isn't. There's no chance left once both are found.

What is random is the **interval**, because it's found from a random sample.
Draw again and you get a different one. The 95% shows how often that
method lands on the truth.

The panel draws forty intervals, from a thousand made. Most cross the
dashed line. The highlighted few don't. Nothing sets apart a missing
interval from a covering one when you can only see it from the inside &mdash;
and you've just one, and no idea which kind you've.

## The count is real

The readout gives the actual coverage of all thousand. At n = 30 with a 95%
level it lands near 94%, and each part of that gap is instructive.

Drag `n` down to 5 and coverage falls to about 89%. That isn't sampling noise.
This page uses a `z` key value with the sample's *guessed* standard
deviation, and at small `n` that estimate is unreliable enough that the interval
comes out too narrow.

**That is just why the t-spread exists.** Gosset's correction widens
the interval to account for having guessed the SD, and the correction is large
at small `n` and negligible past about 30. The multiplier it puts in place of
1.96 is worth seeing, because it shows both halves of that sentence:

|n|t multiplier|wider than z by|
|---|---|---|
|5|2.776|42%|
|10|2.262|15%|
|30|2.045|4%|
|100|1.984|1%|

At n = 5 the honest interval is nearly half as wide again as the one this page
draws, which is where the missing coverage went. By n = 30 the correction is 4%
and the gap stops mattering. This Is where the rule of thumb comes
from. Drag `n` upward and watch the gap
close on its own &mdash; the page is showing the problem the t-spread
solves, rather than quietly using t and hiding it.

## Width and what buys it

Two things set the width.

**The trust level.** Switch from 95% to 99% and the intervals lengthen
noticeably. A higher level doesn't locate the param better. It hedges more.
A 100% interval would be "a place between minus infinity and infinity" &mdash;
just right solid and just right useless.

**The sample size**, through `sqrt(n)`. Quadrupling the sample halves the width.

## Reading one properly

**"Between 42% and 48%"** means the method that made it covers the truth
95% of the time.

**A wide interval is a result.** It says the data doesn't pin the answer down,
which is genuine info rather than a failed test.

**shared intervals don't imply no difference.** Two 95% intervals can
share while a direct test of their difference is major. Test the
difference. Don't eyeball the bars.

**An interval holding zero** matches to a two-sided test not rejecting at
that level. That correspondence is exact, and it's why many people prefer
reporting intervals to reporting
[p-values](hypothesis_testing_and_p_values.html): the interval carries the
effect size and the uncertainty together. Here A p-value carries neither.

## Two intervals that overlap, and a difference that is real

The rule above &mdash; don't eyeball the bars &mdash; is worth doing rather than
taking on trust, because the math is short and the result is truly
counter-natural.

An test with 100 readings in each arm and a standard deviation of 10,
so the standard error in each arm is 10 / &radic;100 = **1**.

|arm|mean|95% interval|
|---|---|---|
|A|10.0|[8.04, 11.96]|
|B|13.2|[11.24, 15.16]|

Those intervals share, between 11.24 and 11.96. Draw them as error bars and
each instinct says the arms are the same.

Now test the difference right. The difference is 3.2, and its standard error
is **not** the two standard errors added:

SE<sub>diff</sub> = &radic;(1&sup2; + 1&sup2;) = &radic;2 = **1.414**, not 2

which gives a 95% interval for the difference of 3.2 &plusmn; 1.96 &times; 1.414
= **[0.43, 5.97]**. That excludes zero, and the matching two-tailed p is
**0.024**. The difference is major while the single intervals share.

The reason is in that square root. Two free errors don't both go the
wrong way at once as often as they each go wrong. They partly cancel, and the
difference is pinned down more tightly than either mean is. Adding the errors
assumes the worst case each time.

The consequence is a whole band where the eye and the math disagree. With
equal standard errors, a difference turns major once it exceeds
1.96&radic;2 = **2.77** standard errors, but the two intervals keep touching
until it exceeds 2 &times; 1.96 = **3.92**. Any gap between those two numbers
shares *and* is major.

|gap between the means|bars overlap?|significant?|
|---|---|---|
|2.0 SE|yes|no|
|3.2 SE|yes|**yes**|
|4.5 SE|no|yes|

The middle row is the one that catches people, and it's why the check you
report has to be a test of the difference rather than a picture of two intervals
side by side. The picture is answering a question no one asked.

## Where it goes wrong

**Saying "95% chance the mean is in here."** The param is fixed. The
interval is random.

**Using z at small n.** Use t. This page shows you the cost of not.

**given freedom.** Clustered or time-series data has a smaller effective
sample size, and the interval will be too narrow.

**Reporting an interval for a biased estimator.** Coverage is about sampling
variability. A systematically wrong reading makes a tight interval around
the wrong answer.

## Questions people ask

<strong>What does a 95 percent confidence interval mean?</strong> If you repeated the study many times and built an interval each time, about 95 percent of those intervals would contain the true value. It is a statement about the procedure.

<strong>Does it mean a 95 percent chance the parameter is inside?</strong> Not strictly. Once computed, the interval either contains the true value or does not. The probability describes the method over repeats.

<strong>How can I make an interval narrower?</strong> Collect more data, reduce the noise in your measurements, or accept a lower confidence level. Width shrinks with the square root of n.

<strong>What is the formula for a mean?</strong> The sample mean plus or minus a critical value times the standard error. The critical value is about 1.96 for 95 percent with a large sample.

<strong>Do overlapping intervals mean no difference?</strong> Not necessarily. Two intervals can overlap and the difference between the means can still be significant. Build an interval for the difference directly.

<strong>When should I use a t value rather than 1.96?</strong> When the sample is small and you estimate the standard deviation from it. The t distribution has heavier tails, so the interval is wider.

## What "95% confident" actually counts

Build a trust interval a thousand times from a known group and count how often it holds the true mean. The number the interval shows is the method, not your one result.

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
print("any single interval contains the mean or it does not -- no 95%% about")
print("it once computed. the 1.96 multiplier assumes a known sd; estimating")
print("it from %d points costs coverage. the t distribution corrects that:" % N)
t39, hits_t = 2.0227, 0
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
intro: The most used and most misread number in statistics, defined just enough to stop misreading it.

## The machinery

**The null hypothesis** is a exact, boring claim: no effect, no difference,
nothing happening. It's exact on purpose, because a exact claim implies a
spread for the test statistic.

That spread is the curve. It's what the statistic would look like across
repeated samples **if the null were true**. each use of a p-value inherits that
if-based.

**The p-value** is the shaded tail: the chance of a statistic at least as
extreme as the one seen, under the null.

Drag the seen statistic and watch the area shrink as it moves outward. A
large statistic is unusual under the null. So Its tail is small &mdash; and a
small tail is what "unlikely, if the null were true" means.

## One test, worked by hand

The modelling below finds a p-value by brute force. It's worth doing one
the plain way first, on numbers small enough to check, so the quantity stops
being what the library returned.

Five readings per group:

|group|values|mean|
|---|---|---|
|control|12, 14, 11, 13, 15|13|
|variant|15, 17, 14, 16, 18|16|

The deviations from the mean are the same five numbers in both groups
&mdash; &minus;1, 1, &minus;2, 0, 2. So each group's sum of squared
deviations is 10, and each sample variance is 10 / 4 = **2.5**. Cutting by
n &minus; 1 rather than n is the correction covered in
[expectation and variance](expectation_and_variance.html).

The difference between the means is 3. What decides whether 3 is a lot is the
standard error of that difference:

SE = &radic;(2.5/5 + 2.5/5) = &radic;1 = **1**

t = 3 / 1 = **3**, on 5 + 5 &minus; 2 = **8** degrees of freedom, which gives a
two-tailed **p = 0.0171**.

Read that last number as the meaning demands: *if the two groups were really
the same*, a gap of 3 or more in either direction would turn up in about one
sample in 59. It says nothing about how likely it's that they're the same, and
nothing about whether a gap of 3 matters to anyone.

Notice which quantity did the work. The difference of 3 was never enough on its
own &mdash; it had to be measured against the SE. The SE fell as the spread
fell and as the sample grew. Quadruple the sample and the SE halves, because it
cuts by &radic;n rather than n. That single square root is why the fourth
hundred readings buy so much less than the first hundred.

## What it is not

Three misreadings, all common enough to have names.

**Not the chance that the null is true.** The p-value is found *given*
the null. It can't then tell you how likely the assumption was. Getting from
`P(data | null)` to `P(null | data)` needs [Bayes'
theorem](bayes_theorem.html) and a prior, and the two quantities can differ by
orders of magnitude.

**Not the chance the result was chance.** Same error, differently worded.

**Not a measure of effect size.** With enough data, a difference of no hands-on
consequence makes a tiny p-value. The p-value answers "is there evidence of
*any* effect", never "is the effect large enough to matter". This is why
[trust intervals](confidence_intervals.html) are increasingly preferred:
they carry the size and the uncertainty in one object.

## Failing to reject is not accepting

Set the seen statistic near zero. The p-value is large, and the conclusion is
that the data is steady with the null.

It's **not** that the null is true. A large p-value is made both by a real
lack of effect and by a study too small to detect one. Distinguishing those
needs [power](type_i_and_type_ii_errors.html), and it's why "no major
difference" in an underpowered study means almost nothing.

## One tail or two

Switch the option. The two-tailed p-value is just double the one-tailed
one for the same statistic. The same area is being counted on both sides.

The choice must be made **before** seeing the data. Deciding afterwards that you
only cared about one direction halves your p-value for free, and that is a
recognised form of cheating rather than a modelling choice.

## Why one in twenty, exactly

The claim that a 0.05 threshold lets one test in twenty through isn't a rough
guess. It's exact, and the reason is a fact about p-values that is rarely
stated: **when the null is true, the p-value is uniformly spread between 0
and 1.** each value is equally likely. A p of 0.03 is just as probable as a
p of 0.87.

Once that is granted, all else follows arithmetically. The chance
that a uniform value falls below &alpha; is &alpha;. So a 0.05 cutoff admits 5%
of true nulls by build. Not as a regrettable side effect, but as
the meaning of what the cutoff is doing. Twenty thousand tests with no effect
in them at all:

|threshold|fraction of nulls below it|uniform predicts|
|---|---|---|
|p &lt; 0.01|0.0111|0.01|
|p &lt; 0.05|0.0520|0.05|
|p &lt; 0.10|0.1003|0.10|
|p &lt; 0.25|0.2492|0.25|
|p &lt; 0.50|0.4953|0.50|
|p &lt; 0.90|0.8968|0.90|

The deciles come out 0.10, 0.20, 0.30, 0.40, 0.50, 0.61, 0.71, 0.81, 0.90 &mdash;
the identity line, which is what a flat spread looks like from the inside.

This is also the mechanism behind p-hacking, and it makes the size of the problem
computable rather than vague. Running k free tests on nothing means
drawing k uniforms and keeping the smallest, and the smallest of k uniforms has
an mean of 1/(k + 1):

|tests run|average smallest p|chance at least one clears 0.05|
|---|---|---|
|5|0.167|1 &minus; 0.95&#8309; = 22.6%|
|20|0.048|1 &minus; 0.95&#178;&#8304; = 64.2%|
|100|0.010|1 &minus; 0.95&#185;&#8304;&#8304; = 99.4%|

Twenty metrics on an test that changed nothing, and the odds are roughly
two in three that one of them looks major. At a hundred it's a near
certainty. No one has to be dishonest for this to happen &mdash; it's what the
math does on its own. This Is why the correction has to be decided before
the tests are run.

## Why 0.05 is under attack

The threshold is a rule. Fisher suggested it as a rough guide and
by name didn't intend it as a choice rule.

The problems are structural.

**p-hacking.** Test enough hypotheses and a thing crosses 0.05 by chance. At
0.05, one test in twenty does so with no effect present at all.

**Publication bias.** Major results get published, so the literature
over-shows them, and the effect sizes it reports are inflated.

**The cliff.** p = 0.049 and p = 0.051 are the same as evidence and are
treated as opposites.

The responses in circulation: report exact p-values rather than thresholds,
report effect sizes and intervals alongside, pre-register the analysis, and
correct for multiple checks. Some fields have moved the threshold to 0.005;
others argue for abandoning the dichotomy fully.

## Where it goes wrong

**Reading p as the chance the null is true.** The central error.

**Treating "not major" as "no effect."** Check the power.

**Choosing the tail after seeing the data.**

**Running many tests without correction.** Bonferroni is crude and better than
nothing. False find rate control is often the better tool.

## Questions people ask

<strong>What is a p-value?</strong> The probability of seeing data at least as extreme as yours if the null hypothesis were true. It is not the probability that the null is true.

<strong>What does it mean to fail to reject the null?</strong> That the data did not give enough evidence against it. It is not proof that the null is correct, since the test may simply lack power.

<strong>Why is 0.05 the usual threshold?</strong> It is a convention that dates back to early statistical practice, not a law of nature. Choose the threshold to match the cost of a wrong decision.

<strong>What is the difference between one-tailed and two-tailed tests?</strong> A one-tailed test looks for a difference in one stated direction. A two-tailed test looks for any difference and is the safer default.

<strong>What is p-hacking?</strong> Running many tests or analyses and reporting the ones that cross the line. With 20 tests at 0.05 you expect one false positive by chance.

<strong>Does a small p-value mean a large effect?</strong> No. With enough data a trivial effect gets a tiny p-value. Always report the effect size and an interval as well.

## Where p-values come from, and what breaks them

A p-value found by modelling rather than looked up in a table, then the same test run two hundred times on data with no effect in it at all.

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
print("it is NOT the chance the null is true; it is the chance of data this")
print("extreme IF the null were true.")
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
print("smallest from that batch:", " ".join("%.4f" % v for v in np.sort(ps)[:5]))
print()
print("a 5%% threshold lets one in twenty through by chance. tighten it")
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
intro: The two ways a test can be wrong, why you can't cut both, and what power really buys.

## Two curves, one line

The grey curve is the test statistic when the null is true. The orange curve is
the same statistic when the effect is real. They share, and the share is the
entire problem.

The dashed line is the threshold: above it you reject the null, below it you do
not.

**Type I error** &mdash; the grey area to the right of the line. The null was
true and you rejected it. A false plus.

**Type II error** &mdash; the orange area to the left. The effect was real and
you missed it. A false minus.

**Power** is what is left of the orange curve: `1 - beta`, the chance of
catching a real effect.

## The trade

Change alpha from 0.05 to 0.01. The threshold moves right, the grey tail
shrinks &mdash; and the orange tail grows. Beta rises, power falls.

Move it the other way and the reverse happens.

**You can't reduce both by moving the line.** That isn't a limitation of the
method. It's what "the spreads share" means. Any threshold is a
statement about which error you'd rather make.

## What actually helps

Two things, and only two.

**More data.** Drag `n` upward. Both curves narrow, because their spread is the
[standard error](sampling_distributions.html) and that falls like `sqrt(n)`. The
share shrinks, and both error rates can fall at once. This is the only lever
that raises both without given any of it.

**A larger true effect.** Drag the effect control. The curves separate. You do
not often control this, but it's why detecting a large effect needs so much
less data than detecting a small one.

## Choosing alpha honestly

The rule is 0.05, and treating it as fixed is the mistake. The right value
depends on which error costs more.

**A screening test for a treatable disease.** A false minus means missing a
case. A false plus means an unneeded follow-up. Loosen alpha, gain power.

**A criminal conviction.** The system by name prefers false negatives, which
is what "beyond reasonable doubt" codes.

**Particle physics.** The five-sigma standard is alpha near 3 in 10 million,
because the field has been burned by fluctuations and there's enough data to
afford it.

**A/B testing a button colour.** A wrong call is cheap. Standard thresholds are
generous, and the real risk is running many tests and picking winners.

## Power, before the experiment

Power analysis is the math no one enjoys and everybody should do: given a
target power &mdash; often 80% &mdash; an alpha, and the smallest effect worth
detecting, how large a sample is needed?

Set the effect to 0.2 and watch what `n` has to be before power reaches 80%. The
needed sample grows roughly with the inverse square of the effect size, which
is why detecting small effects is so costly and why so much published work is
underpowered.

An underpowered study is worse than no study. It often fails to find a real
effect &mdash; and when it does find one, the estimate is inflated, because only
an unusually large sample fluctuation could have crossed the threshold at that
sample size. That is the **winner's curse**, and it's a substantial part of why
published effects shrink on replication.

## The question alpha and power cannot answer alone

Alpha is the chance of a false plus **given that the null is true**, and
power is the chance of a true plus **given that it's false**. Neither of
them answers the question anyone really has after a major result: how
likely is it that *this* finding is real?

That question needs one more number, and it's the one no one reports &mdash; the
proportion of the hypotheses being tested that were true to begin with. Work it
through on a thousand tests, all done right, alpha at 0.05 and power
at a fair 80%, in a field where one hypothesis in ten is true:

|  |true (100)|false (900)|
|---|---|---|
|**significant**|80|45|
|**not significant**|20|855|

There are 125 major results and 45 of them are false. **Thirty-six per cent
of the findings are wrong**, with no p-hacking, no bad faith and no methodological
error &mdash; only 5% of many false hypotheses being larger than 80%
of a small number of true ones.

All follows from the ratio of those two counts:

|true hypotheses|alpha|power|share of significant results that are real|
|---|---|---|---|
|10%|0.05|0.80|64.0%|
|10%|0.05|0.35|43.8%|
|1%|0.05|0.80|13.9%|
|10%|0.005|0.80|94.7%|
|50%|0.05|0.80|94.1%|

Read the third row. In exploratory work where one hypothesis in a hundred is
true &mdash; screening compounds, scanning the genome, trying features &mdash;
about six of each seven major results are false, and the study was
run just right. Read the second: halving the power doesn't halve the errors, it
raises the false share from 36% to 56%. This Is the concrete cost of the
underpowered study given above.

Then read the last two rows, because they're the levers. Tightening alpha
tenfold takes the false share from 36% to 5%. This Is the actual arg
behind moving the threshold to 0.005. Testing better hypotheses does the same
thing &mdash; a field where half the ideas are right barely has the problem.
Neither lever is inside the statistics. They're choices about how hard you're
willing to make it to publish, and about what you bother to test.

## Where it goes wrong

**Reading a non-major result as no effect.** Report the power, or the
interval.

**Running the power analysis afterwards.** Post-hoc power found from the
seen effect is a restatement of the p-value and carries no new info.

**Fixing alpha at 0.05 even so of costs.** It's a rule.

**Peeking at results and stopping when major.** This inflates the true
Type I rate far above the nominal one. Sequential testing methods exist and
correct for it.

## Questions people ask

<strong>What is a Type I error?</strong> Rejecting a true null hypothesis, a false positive. Its probability is the significance level alpha.

<strong>What is a Type II error?</strong> Failing to reject a false null hypothesis, a false negative. Its probability is called beta.

<strong>What is statistical power?</strong> Power is 1 minus beta: the chance of detecting a real effect of a given size. Aim for 80 percent or more before running an experiment.

<strong>How do I reduce both errors at once?</strong> Increase the sample size. With a fixed sample, lowering alpha raises beta, so you have to trade one against the other.

<strong>Which error is worse?</strong> It depends on the cost. A false alarm in a drug trial and a missed disease in screening carry very different consequences, so pick alpha with that in mind.

<strong>How do I compute the sample size I need?</strong> Fix alpha, the desired power and the smallest effect you care about, then use a power calculation. Libraries such as statsmodels provide it.

## Both errors, counted

Lower your threshold and you catch more real effects while raising more false alarms. Here both rates are measured across a sweep. The trade is visible rather than given.

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
intro: Making an unit-perp basis, and the factorisation that makes least squares by number fair.

## The procedure

Start with vectors that span what you want but aren't at right angles. Gram-
Schmidt makes them at right angles without changing what they span.

**First vector**: divide by its length. That is `q1` &mdash; same direction,
length 1.

**Second vector**: it points partly along `q1` and partly perpendicular to it.
[Project](projections.html) it onto `q1`, subtract that projection, and what is
left is at right angles by build. Norm it to get `q2`.

The visualisation draws each step. The dashed grey lines are the originals. The
solid orange segment is the map being removed, and the short dashed line
is the remainder that turns `q2`. The readout gives `q1 . q2` &mdash; zero to
six decimal places, because it can't be any of it else.

For more vectors the pattern repeats: subtract the components along all
already fixed, norm what lives.

## Where R comes from

The maps you subtract aren't discarded. Collect them and you've `R`,
and together:

```
A  =  Q R
```

`Q` has the unit-perp vectors as columns. `R` is upper tri.

`R` is tri for a structural reason worth seeing: the first first
vector is built from `q1` alone, the second from `q1` and `q2`, the third from
the first three. Nothing is ever built from a `q` that comes later, so
all below the main-line is zero.

Drag until the two input vectors nearly align. The remainder shrinks toward zero
and `R` turns nearly singular &mdash; which is the same near-dependence
[the basis module](basis_span_and_orthogonality.html) warns about, showing up as
a small number on the main-line.

## Why least squares uses it

The textbook answer to least squares is the normal equations:

```
x  =  (A'A)^-1 A' b
```

Correct, and by number poor. Forming `A'A` **squares the rule number**.
A mat with rule number 10&#8310. &mdash; plain for real data
&mdash; turns 10&#185;&#178;, and in double precision that has consumed most
of the available fit before the solve begins.

QR avoids it. Substituting `A = QR` and using `Q'Q = I`:

```
R x  =  Q' b
```

`R` is tri, so this is solved by back-substitution in one pass, and the
rule number is never squared. That is why `numpy.linalg.lstsq`, R's `lm`
and each serious least-squares routine uses QR or an
[SVD](singular_value_decomposition.html) rather than the formula in the
textbook.

## Classical against modified Gram-Schmidt

The version given above is *classical* Gram-Schmidt, and it's unstable in
floating point: rounding errors mean the later vectors drift away from
perpness.

*Modified* Gram-Schmidt subtracts each map right away rather than all at
once at the end. Algebraically the same, by number much better behaved.

Serious setups use neither, preferring **Householder reflections**,
which build `Q` from a sequence of reflections and are stable even so of the
input. Gram-Schmidt lives because it's the version you can see, which is why
it's the version on this page.

## Where else it turns up

**The QR method** for eigenvals again and again factors and re-times in the
other order, and the result settles to a tri mat whose main-line
holds the eigenvals. It's one of the most key numeric methods
there's, and it's this breakdown in a loop.

**Orthogonalising features** before regression, to drop collinearity.

**Kalman filters** in square-root form, for the same conditioning reason as
least squares.

## Gram-Schmidt by hand, on two vectors

The editor below runs the full factorisation. The mechanism is clearest on two
vectors small enough to finish on paper. Take `a1 = (1, 1)` and `a2 = (2, 0)`,
which span the plane but meet at 45&deg;, not a right angle.

**q1** is `a1` normed: its length is &radic;2. So `q1 = (1, 1)/&radic;2`.

**q2** drops from `a2` its component along `q1`. The map length is
`a2 &middot; q1 = 2/&radic;2 = &radic;2`. So The map is `&radic;2 &middot;
q1 = (1, 1)`. Subtract it: `a2 &minus; (1, 1) = (1, &minus;1)`. That remainder is
at right angles to `q1` by build, and norming it (length &radic;2 again)
gives `q2 = (1, &minus;1)/&radic;2`.

Check: `q1 &middot; q2 = (1&minus;1)/2 = 0`, just, as it must be. And the
maps you subtracted are `R`:

|R|value|
|---|---|
|R&#8321;&#8321; = &#124;a1&#124;|&radic;2|
|R&#8321;&#8322; = a2 &middot; q1|&radic;2|
|R&#8322;&#8322; = &#124;remainder&#124;|&radic;2|

`R` is upper tri because `a1` was built from `q1` alone and only `a2` ever
used `q2` &mdash; nothing is ever built from a later `q`, so all below the
main-line is zero. That is the whole factorisation, and each larger case is this
one repeated.

The reason least squares reaches for this rather than the textbook normal
equations is visible in the same small picture. Solving `Rx = Q'b` uses the
tri `R` right and never forms `A'A`. This Would square the rule
number &mdash; a mat conditioned at 10&#8310. Turns 10&#185;&#178;, and in
double precision that discards most of the available digits before the solve even
starts. The unit-perp columns are what make `Q'Q` disappear to the identity, so
the substitution costs nothing and the conditioning is left untouched.

The version shown here, subtracting each map at the end, is *classical*
Gram-Schmidt and drifts out of perpness in floating point. The *modified*
form subtracts each map right away and behaves far better, though serious
libraries use Householder reflections instead. Gram-Schmidt lives as the
version you can watch happen. This Is why it's the one worth working by hand.

The same breakdown, run in a loop that factors and re-times in the
opposite order, is the QR method for eigenvals. One of the most
key numeric methods there's, and at heart just this factorisation
repeated until the mat goes tri.

## Where it goes wrong

**Classical Gram-Schmidt on ill-conditioned input.** Use the modified version,
or a library.

**Forming A'A because the formula is shorter.** It squares the conditioning.

**given Q is square.** For a tall thin `A`, the economy QR gives a `Q` with
the same shape as `A`, not a full perp mat.

## Questions people ask

<strong>What does QR decomposition produce?</strong> It writes a matrix A as Q times R, where Q has orthonormal columns and R is upper triangular.

<strong>How is QR computed?</strong> Textbooks show Gram-Schmidt, but libraries use Householder reflections, which are more stable numerically.

<strong>Why use QR for least squares?</strong> Solving R x = Q transpose b avoids forming A transpose A, which squares the condition number. It gives more accurate answers.

<strong>What goes wrong with classical Gram-Schmidt?</strong> Rounding errors accumulate and the columns of Q lose orthogonality when the input columns are nearly dependent. Modified Gram-Schmidt or Householder fixes that.

<strong>What is the QR algorithm?</strong> An iterative method for eigenvalues that repeatedly factors and recombines as RQ. It is the basis of most eigenvalue solvers.

<strong>Does QR work for non-square matrices?</strong> Yes. For a tall matrix, the reduced form gives Q the same shape as A and a square R.

## Orthogonalise a basis, then solve with it

QR turns any set of columns into an unit-perp set plus the bookkeeping needed to get back. It's how least squares is solved .

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
intro: A mat square root, what it needs to exist. Why its failure is more handy than its success.

## The factorisation

For a even plus-definite mat `C` there's a lower tri `L`
with:

```
C  =  L L'
```

`L` is unique if its main-line is taken plus, and it's the nearest thing a
mat has to a square root. For a 2&times;2 it's short enough to write out
whole:

```
L11 = sqrt(C11)
L21 = C21 / L11
L22 = sqrt(C22 - L21^2)
```

That last line carries the whole story. If `C22 - L21^2` is minus there's no
real square root, and the method stops.

## Positive-definite

A even mat is **positive definite** when `x' C x > 0` for each non-zero
`x`, which is equal to all its eigenvals being strictly plus.

For a covariance mat this isn't a detail. `x' C x` is the variance of
the combination `x` of your variables, and a variance can't be minus. A
mat that fails the test isn't showing any spread that exists.

Drag the link control toward &plusmn;1. Past the boundary the readout
reports failure, and a link of 1.2 isn't a thing: no
pair of random variables can be more than just right linked.

**The factorisation failing is the test.** Cholesky costs about `n^3 / 3`
ops, roughly half a general LU factorisation, and about a tenth of what
finding the eigenvals costs. When a routine needs to know whether a mat
is positive definite, it attempts a Cholesky and watches for the minus square
root.

## Generating correlated randomness

This is where the factor earns its keep. Take free standard normals `z`
and find `L z`. The result has covariance:

```
Cov(Lz)  =  L Cov(z) L'  =  L I L'  =  L L'  =  C
```

just the covariance you asked for. The scatter in the visualisation is
made this way, and the two orange segments are the columns of `L` &mdash;
the axes the free noise gets mapped onto.

That single trick underlies Monte Carlo modelling of linked risk factors,
sampling from a multivariate normal, and the reparameterisation trick in
variational autoencoders.

## Where else it appears

**Gaussian processes.** Fitting one needs solving a system with the kernel
mat and finding its log-determinant. Cholesky gives both: the solve by
tri substitution, and the log-determinant as twice the sum of the logs of
`L`'s main-line. It's the math-heavy core of GP regression.

**Linear systems** with a even plus-definite mat &mdash; twice as
fast as LU and by number stable without pivoting.

**Optimisation.** Newton steps need to solve with the
[Hessian](jacobian_and_hessian.html), and a good Cholesky confirms the
Hessian is positive definite. This Confirms the step direction is a descent
direction. A failure signals a saddle, and modified Newton methods react to
just that signal.

**Whitening.** `L^-1 x` transforms linked data into unlinked data with
unit variance.

## When it fails on data that should be fine

An guessed covariance mat can come out not-quite-plus-definite for
reasons that are math rather than conceptual.

**More variables than readings.** The estimate is singular by build:
with 100 variables and 50 samples the mat has rank at most 50.

**just right collinear columns.** One variable is a combination of others, so
some direction has truly zero variance.

**Floating point.** A mat that is positive definite in exact math can
have a tiny minus eigenval after rounding.

The standard repairs: add a small multiple of the identity to the main-line
&mdash; *jitter*, or *ridge*, and the same idea as
[ridge regression](../machine_learning/ridge_and_lasso_regression.html). Use a shrinkage estimator
such as Ledoit-Wolf. Or clip the minus eigenvals to zero and reassemble.

## Cholesky by hand, and the failure

The three formulas are short enough to run on a 2&times;2. Take
`C = [[4, 2], [2, 5]]`:

`L&#8321;&#8321. = &radic;4 = 2`. `L&#8322;&#8321. = 2 / L&#8321;&#8321. = 1`.
`L&#8322;&#8322. = &radic;(5 &minus; 1&sup2;) = &radic;4 = 2`.

So `L = [[2, 0], [1, 2]]`. Timesing back, `L L' = [[4, 2], [2, 5]]` &mdash;
the first. The whole story is in that last square root: `C&#8322;&#8322;`
minus what the first column already accounts for must be non-minus for a real
`L` to exist.

Now feed it a mat that is even but not positive definite,
`B = [[1, 2], [2, 1]]`. The last step asks for `&radic;(1 &minus; 2&sup2;) =
&radic;(&minus;3)`, which has no real value, and the factorisation stops. That is
not a bug &mdash; it's the test. `B` fails because `x = (1, &minus;1)` gives
`x' B x = 1 &minus; 4 + 1 = &minus;2 < 0`. `B` isn't a covariance of any of it:
no set of variables has a minus variance. The cheap `n&sup3;/3` factorisation
is how a routine decides plus-definiteness, just because it breaks
just when the property fails.

That is also why an guessed covariance mat at times fails the factorisation
when it "should" work: with more variables than readings the estimate is
singular by build, and a truly collinear pair gives some direction zero
variance, so the last square root reaches zero or below. The standard repair
&mdash; adding a small multiple of the identity, the same idea as ridge
regression &mdash; nudges each eigenval up just enough to make the square roots
real again, at the cost of admitting you changed the model.

It's worth stressing why the factorisation is the test of choice: at about
`n&sup3;/3` ops it's half the cost of a general LU breakdown and a
fraction of finding the eigenvals. So A routine that needs to know whether a
mat is positive definite simply attempts the Cholesky and watches for the
minus square root.

## Where it goes wrong

**Passing a non-even mat.** Most setups read only one triangle
and will silently return nonsense.

**Treating failure as a bug.** It's often the data telling you a thing.

**Adding jitter without recording it.** You've changed the model. Say by how
much.

**Using it on a mat that is only positive semi-definite.** A zero eigenval
gives a zero on `L`'s main-line. Any of it that then cuts by it fails.

## Questions people ask

<strong>What is a Cholesky decomposition?</strong> It factors a symmetric positive definite matrix A as L times L transpose, where L is lower triangular. It is like a square root for matrices.

<strong>What does positive definite mean?</strong> x transpose A x is positive for every nonzero x. Equivalent tests are all eigenvalues positive, or the Cholesky factorisation succeeding.

<strong>Why use Cholesky to solve systems?</strong> It costs about half as much as LU and needs no pivoting. It is the standard approach for covariance and kernel matrices.

<strong>How do I sample correlated random numbers?</strong> Compute L from the covariance matrix, draw independent standard normals z and use L times z. The result has the covariance you wanted.

<strong>Why does Cholesky fail on my covariance matrix?</strong> Rounding or near-duplicate features make it only semi-definite. Add a small jitter to the diagonal, such as 1e-6, to restore definiteness.

<strong>Can I use it on a matrix that is not symmetric?</strong> No, it assumes symmetry and reads only one triangle. Symmetrise first, or use LU.

## Half a matrix, and what it costs to have one

Cholesky finds a tri L with L @ L.T equal to your mat -- but only if the mat is positive definite. Here is what that rule rules out.

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

Unconstrained: find where the grad is zero.

Constrained: that rule fails right away, because the unconstrained optimum is
often a place the constraint forbids. On the circle above, the goal
grows forever in one direction and its grad is never zero anywhere.

## The condition

Look at where the level lines meet the circle.

At most points they **cross**. Crossing means you can slide along the circle and
move to a better level line. So You aren't at the optimum.

At the optimum they're **tangent** &mdash; touching without crossing. Sliding
either way makes things worse.

Tangency means the two grads are parallel:

```
grad f  =  lambda * grad g
```

That is the method entire. Solve it together with the constraint itself and you
have the pick points.

Drag the goal weights and watch the marked point travel around the circle,
staying just where the family of parallel lines grazes it.

## The multiplier is the interesting part

`lambda` looks like bookkeeping. It isn't: it's the **shadow price** of the
constraint &mdash; the rate at which the best value raises as the
constraint is relaxed.

Drag the radius control. The optimum's value rises, and the readout's `lambda`
says how fast per unit of radius.

In economics that is truly a price: how much more profit one more unit of
room is worth, and so what you should be willing to pay for it. In
machine learning it's the same quantity under different names &mdash; the
smoothing strength in ridge regression, and the dual variables in an SVM
that spot just which points are support vectors.

A `lambda` of zero says the constraint isn't binding: you'd have chosen
that point anyway, and loosening it buys nothing.

## Where it shows up

**Ridge regression.** "Cut error subject to the coeffs being small"
is a constrained problem. The penalised form everyone really writes is its
Lagrangian, and the fine weight is `lambda`.

**Support vector machines.** The dual formulation is Lagrangian, the multipliers
are per-training-point, and the ones that come out non-zero *are* the support
vectors.

**max entropy.** Finding the spread with the most entropy subject to
matching known moments makes the exponential family, and the multipliers
become its natural params.

**PCA.** Raising variance subject to unit-length direction gives
`Cv = lambda v` &mdash; the multiplier turns out to be the
[eigenval](eigenvalues_and_eigenvectors.html).

**Physics and economics** throughout, wherever a thing is optimised under a
budget.

## Inequalities

Real constraints are often `g(x) <= c` rather than `g(x) = c`, and the extension
is the **KKT rules**. The addition worth remembering is *complementary
slackness*: for each constraint, either it's tight and its multiplier may be
non-zero, or it's slack and its multiplier is zero.

That is what makes SVMs sparse. Points comfortably on the correct side of the
margin have slack constraints, so their multipliers are zero, so they contribute
nothing to the answer. Only the points pressed against the margin live.

## The shadow price, worked

The claim that `lambda` is a price is easiest to trust on a case you can check by
hand. Cut `x&sup2; + y&sup2;` &mdash; distance-squared from the origin
&mdash; subject to `3x + 4y = c`. The constraint is a line, and the closest point
on a line `3x + 4y = c` to the origin is at distance `c/5` (because
&radic;(3&sup2;+4&sup2;) = 5), so the min value is `(c/5)&sup2;`.

Now watch what one unit of `c` buys:

|c|minimum `x&sup2;+y&sup2;`|change|
|---|---|---|
|24|23.04||
|25|25.00|+1.96|
|26|27.04|+2.04|

The optimum rises by about 2 per unit of `c`, and the multiplier the method
returns is `lambda = 2c/25 = 2` at `c = 25`. The two agree: `lambda` *is* the
rate at which the best value changes as the constraint moves &mdash; the price
of one more unit of the resource. The small gap between 1.96 and 2.04 is the
curvature of that price across the step. In the limit of an infinitesimal change
it's just `lambda`. This is why, in a real problem, the multiplier is often
worth more than the optimum: it tells you what relaxing the constraint is worth
before you pay to relax it.

This is why the multiplier reappears under other names across machine learning:
it's the smoothing strength in ridge regression (the price of the
coeff-size budget), and it's the per-point dual variable in an SVM, where
the points whose multiplier comes out non-zero are just the support vectors.
In each case `lambda` answers the question the optimum can't: not "what is the
best value" but "what is the constraint costing me". This Is often the number a
choice really turns on.

A multiplier of zero carries its own message: the constraint isn't binding, you
would have chosen that point anyway, and relaxing it buys nothing &mdash; which is
as handy to know as a large multiplier that says the constraint is costly and
worth paying to loosen.

For inequality constraints the same idea extends to the KKT rules, whose
complementary slackness says each constraint is either tight with a possibly
non-zero multiplier or slack with a zero one. Which is just what makes
an SVM sparse, since points comfortably inside the margin contribute nothing.

## Where it goes wrong

**Losing it finds stationary points, not maxima.** The rule holds at
constrained minima and saddles too. Check which you've.

**given a answer exists.** An unbounded goal on an unbounded
constraint set has none.

**Reading lambda's sign carelessly.** It depends on how the Lagrangian was
written, and the sign rule differs between texts.

**Skipping the constraint qualification.** The method assumes the constraint
grads are well behaved at the answer. At a cusp or where constraints are
collapse it can fail.

## Questions people ask

<strong>What problem do Lagrange multipliers solve?</strong> Optimising a function subject to an equality constraint. At the optimum, the gradient of the objective is parallel to the gradient of the constraint.

<strong>What does the multiplier itself mean?</strong> It is the rate at which the optimal value changes if you relax the constraint slightly. Economists call it the shadow price.

<strong>How do I set up the equations?</strong> Form L = f - lambda times g, then set all partial derivatives of L, including the one in lambda, to zero and solve.

<strong>How do inequality constraints change things?</strong> They need the KKT conditions. The multiplier must be non-negative, and either the constraint is active or its multiplier is zero.

<strong>Where are they used in machine learning?</strong> In the SVM derivation, in maximum entropy models, and in constrained optimisation such as regularisation viewed as a budget.

<strong>Does the method find the global optimum?</strong> It finds candidate stationary points. You still have to compare them, or know the problem is convex, to be sure.

## Optimise with a rule you are not allowed to break

The closest point on a line to the origin, found three ways. By brute force, by substitution. By the multiplier rule. All three agree. The multiplier turns out to mean a thing.

```python-run
import numpy as np
# minimise x^2 + y^2  subject to  3x + 4y = 25
def f(x, y):     return x ** 2 + y ** 2
def g(x, y):     return 3 * x + 4 * y - 25
print("brute force along the constraint line:")
xs = np.linspace(-5, 12, 400_001)
ys = (25 - 3 * xs) / 4; vals = f(xs, ys); i = vals.argmin()
print("  best point (%.4f, %.4f)   f = %.4f" % (xs[i], ys[i], vals[i]))
print("by substitution: df/dx = 0 -> x = 3")
x_star, y_star = 3.0, (25 - 9) / 4
print("  x = %.4f, y = %.4f   f = %.4f" % (x_star, y_star, f(x_star, y_star)))
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
print("gradients are parallel: grad f = %s, grad g = %s"
      % (np.round([2*x_l, 2*y_l], 4).tolist(), [3, 4]))
print("lambda is the price of the constraint:")
mins = []
for c in (24.0, 25.0, 26.0):
    xs2 = np.linspace(-5, 12, 200_001)
    best = f(xs2, (c - 3 * xs2) / 4).min()
    mins.append(best)
    print("  3x + 4y = %.0f  ->  minimum f = %.4f" % (c, best))
print("  delta: %.4f then %.4f; lambda is %.4f"
      % (mins[1] - mins[0], mins[2] - mins[1], lam))
print("lambda tells you what the constraint costs -- often more useful than")
print("the optimum itself.")
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
    """title: Jensen's Inequality
intro: Why blending before and after a curve gives different answers. What that difference is used for.

## The statement

For a convex function `f` and a random variable `X`:

```
E[f(X)]  >=  f(E[X])
```

Transform first and mean, and you get at least as much as blending first
and transforming. For a concave function the inequality reverses.

## Why it is obvious once seen

Take a spread that puts half its weight at each of two points &mdash; the
two grey dots in the visualisation.

`f(E[X])` is the curve tested at the midpoint: the orange dot **on** the
curve.

`E[f(X)]` is the mean of the two heights: the midpoint of the **chord**, the
lighter dot above.

Convex means the chord lies above the curve. So the chord's midpoint is above
the curve's point, which is the inequality, drawn.

Two controls change the gap. **Curvature**: flatten the function toward a
straight line and the chord lies on the curve. The gap vanishes &mdash; for a
linear `f`, expectation passes straight through. **Spread**: shrink the
spread to a point and the two dots merge, and the gap vanishes again.

The gap is zero just when the function is linear or the variable is constant,
and grows with both.

## Consequences worth having

**The mean of ratios isn't the ratio of means.** `1/x` is convex on the
positives, so `E[1/X] >= 1/E[X]`. Blending speeds in miles per hour to get
mean pace is wrong in a exact, predictable direction, and the same trap
appears in blending rates, ratios and per-unit costs throughout applied work.

**AM-GM.** Applying Jensen to the concave logarithm gives that the math
mean is at least the geometric mean, right away.

**Log-loss and calibration.** `-log` is convex, so blending log-losses
punishes confident mistakes far more than the raw error rate does. That is a
design choice, and Jensen is why it works.

**Portfolio returns.** Compounding is multiplicative, so the geometric mean is
what you keep and the arithmetic mean is what gets advertised. Volatility drag
is Jensen's gap.

## The one that matters most

Jensen is why **EM** and **variational inference** exist.

Both want to raise a log-likelihood holding a sum inside a logarithm
&mdash; `log sum_z p(x, z)`. Which doesn't break down and can't be
optimised right.

The move is to write that sum as an expectation, then use Jensen on the concave
`log` in the other direction:

```
log E[ ... ]  >=  E[ log ... ]
```

The right-hand side is a **lower bound** on the thing you wanted, it breaks down
into terms you can differentiate, and raising it can't fall the true
goal.

That bound is the ELBO. The evidence lower bound &mdash; and it's the
goal a variational autoencoder trains on. EM alternates between tightening
the bound and raising it. This Is just the two steps in
[the Gaussian mixture module](../machine_learning/gaussian_mixture_models.html).

The gap between the bound and the truth is the KL divergence between the
rough posterior and the real one. This Ties Jensen right to
[cross-entropy and KL](cross_entropy_and_kl_divergence.html): non-negativity of
KL *is* Jensen applied to the log.

## Where it goes wrong

**Blending a transformed quantity and reporting it as the transform of the
mean.** Log-scale means, rates and ratios all bite here.

**Getting the direction wrong.** Convex up, concave down. `log` and `sqrt` are
concave. `exp`, `x^2` and `1/x` (on positives) are convex.

**given the bound is tight.** The ELBO can sit far below the true likelihood,
and a rising ELBO doesn't prove the likelihood rose by as much.

**Losing that equality needs linearity or a constant.** Nothing else gives
it.

## The average speed trap, worked

Drive 60 km at 30 km/h, then another 60 km at 60 km/h. What was the mean
speed?

Almost everyone answers 45. Work it out instead:

```
first leg   60 km at 30 km/h  ->  2 hours
second leg  60 km at 60 km/h  ->  1 hour
                                 --------
            120 km in 3 hours  ->  40 km/h
```

**40, not 45.** The answer is dragged toward the slower speed, because you spend
twice as long travelling at it. The correct mean here is the harmonic mean,
`2 / (1/30 + 1/60) = 40`.

Jensen says this had to happen, and says which direction. Time per kilometre is
`1/X`, and `1/x` is convex on the positives, so:

```
E[1/X]  >=  1/E[X]

E[1/X]  = (1/30 + 1/60)/2 = 0.02500 hours per km
1/E[X]  = 1/45            = 0.02222 hours per km
```

The time you really spend is governed by the left-hand side, and it's
**bigger**. Over 120 km: 3.00 hours actual against 2.67 predicted by the naive
mean. The trip is always at least as slow as the arithmetic mean suggests,
and just as slow only when both speeds are equal &mdash; the equality case,
where the spread merges to a point.

The same shape appears wherever a rate is averaged: cost per unit, latency per
request, price-to-earnings across a portfolio. **Blending a ratio and taking
the ratio of means are different ops**, and Jensen tells you in
advance which one comes out larger, without finding either.

## Questions people ask

**How do I note which way it points?** Picture the chord. Convex means the
curve bends upward and each chord lies above it. So The mean of the heights
(the chord) beats the height of the mean (the curve): `E[f(X)] >= f(E[X])`.
Concave flips the picture and the inequality. If you can recall that `x`&sup2;
is convex, one example settles it. The mean of squares exceeds the square
of the mean, which is just the variance being non-minus.

**When is it an equality?** In just two cases: `f` is linear over the range
the variable really reaches, or the variable is a constant. any of it else and
the gap is strictly plus. This is why linear changes pass cleanly
through an expectation and nothing else does.

**Is AM-GM really the same statement?** Yes. Apply Jensen to `log`, which is
concave, and you get `log` of the mean at least the mean of the `log`s;
exponentiate and that is the arithmetic mean dominating the geometric mean. The
inequality you may have proved by induction at school is one substitution away.

**Does it apply to medians too?** No. Jensen is a statement about expectations,
and the median passes through any *monotone* function untouched &mdash;
`median(f(X)) = f(median(X))` for growing `f`, convex or not. That difference
is one hands-on reason to report a median when a quantity has been through a
nonlinear change.

**Where will this really bite me?** Wherever you mean a thing that was
already a rate or a log. Blending log-chances and exponentiating gives
the geometric mean, not the math one. Which is what perplexity is,
and why it isn't the mean chance.

## The average of the function is not the function of the average

Three concrete cases where swapping those two ops changes the answer, including the one that quietly costs money.

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
intro: Memoryless processes, the spread they settle into, and why so many methods are one.

## The property

A process is **Markov** when the next state depends only on the current state,
not on the path that led there. The present screens off the past.

That is a strong assumption and a liberating one. Instead of a history of
any length you carry one thing &mdash; where you're &mdash; and
all about the future follows from it.

## The transition matrix

Collect the chances into a mat `P`. Here `P[i][j]` is the chance of
moving from state `i` to state `j`. each row sums to 1, because from any state
you go a place, possibly back to where you were.

If the current spread over states is a row vector `d`, then after one step
it's `d P`. After `k` steps, `d P^k`. That is all the math there's, and
the visualisation is doing just it, forty steps at a time.

## Convergence

Watch the three curves. They start apart. All the chance on one
state &mdash; and within a few steps they flatten out and stop moving. The
readout shows the last step changing things by around 10&#8315;&#185;&#8304;.

Now change the starting state. The curves begin a place fully different
and **arrive at the same values**.

That limit is the **stationary spread**: the `pi` with `pi P = pi`. Read
as an eigenvector problem, it's the left eigenvector of `P` with eigenval 1,
and the [eigenval module](eigenvalues_and_eigenvectors.html) is the same
mathematics in another costume.

The settling isn't auto. It needs the chain to be **irreducible** &mdash;
each state reachable from every other. And **aperiodic**, not trapped in
a fixed cycle. Drag a transition chance to its min and settling
slows visibly. A chain that couldn't leave a state at all would never mix.

The speed is governed by the second-largest eigenval: the closer it's to 1,
the slower the mixing. That number has a name, the *spectral gap*, and it's
what people mean by a chain mixing slowly.

## The whole thing on two states

All above fits on a chain with two states, small enough to do on paper and
still large enough to show all three claims.

Weather, where a sunny day is often followed by another and rain clears half
the time:

|from \ to|sunny|rainy|
|---|---|---|
|**sunny**|0.9|0.1|
|**rainy**|0.5|0.5|

**The stationary spread, solved just.** &pi;P = &pi; on two states is
just &pi;<sub>s</sub> = 0.9&pi;<sub>s</sub> + 0.5&pi;<sub>r</sub>, which
rearranges to 0.1&pi;<sub>s</sub> = 0.5&pi;<sub>r</sub>, so
&pi;<sub>s</sub> = 5&pi;<sub>r</sub>. With the two summing to 1 that gives
**&pi; = (5/6, 1/6)**, or (0.8333, 0.1667). No iteration, no eigenval routine
&mdash; two lines of algebra.

**The same answer by iterating.** Start with certainty and times by P
again and again:

|step|from sunny|from rainy|
|---|---|---|
|0|(1.000, 0.000)|(0.000, 1.000)|
|1|(0.900, 0.100)|(0.500, 0.500)|
|2|(0.860, 0.140)|(0.700, 0.300)|
|3|(0.844, 0.156)|(0.780, 0.220)|
|4|(0.838, 0.162)|(0.812, 0.188)|
|5|(0.835, 0.165)|(0.825, 0.175)|

Two starting points that couldn't be further apart, settling on the same
(0.8333, 0.1667). The chain forgets where it began. This Is the whole content of
the claim that the limit doesn't depend on the start.

**And the mixing speed. This Isn't a metaphor.** The eigenvals of a 2&times;2
stochastic mat are 1 and (trace &minus; 1). So Here the second eigenval is
0.9 + 0.5 &minus; 1 = **0.4**. Now measure how far the sunny column is from
0.8333 at each step:

0.1667, 0.0667, 0.0267, 0.0107, 0.0043, 0.0017

Each is just 0.4 times the one before it. The second eigenval isn't merely
*related* to the mixing rate. It **is** the factor by which the left error
shrinks per step. A chain with a second eigenval of 0.99 needs 365
steps to shrink the error as far as this one does in four. This Is why the spectral gap is the
number MCMC practitioners worry about.

One more reading falls out of &pi; for free. It's the one that makes the
numbers concrete. The expected time to return to a state is
**1 / &pi;<sub>i</sub>**, so rain recurs each 1 / (1/6) = **6 days** on average
and sun each 1 / (5/6) = **1.2 days**. The stationary spread isn't only
the long-run share of time spent in each state. It's the reciprocal of how long
you wait to come back to it.

## Where they appear

**PageRank** is the stationary distribution of a random surfer following links.
The damping factor exists to make the chain irreducible. So A page with no
outbound links can't swallow all the chance.

**MCMC** &mdash; Metropolis-Hastings, Gibbs sampling, Hamiltonian Monte Carlo
&mdash; runs the idea backwards: make a chain whose stationary spread
*is* the posterior you want, run it, and treat the states it visits as samples.
Nearly all Bayesian work is this.

**Hidden Markov models** put a Markov chain behind readings you can see, and
were the backbone of speech spotting for decades.

**Reinforcement learning.** A Markov choice process is a Markov chain with
actions and rewards attached. The "Markov" in MDP is this property, and it's
what makes value functions of the state alone enough.

**n-gram language models** are Markov chains over words &mdash; and their
limitation is just the property: a bigram model can't note any of it
beyond the previous word. This Is why long-range coherence needed a thing
else.

## Where it goes wrong

**given the property holds.** Most real processes have memory. Widening the
state to include recent history restores the property at the cost of a much
larger state space.

**given settling.** Check irreducibility and aperiodicity.

**Stopping an MCMC run too early.** Samples before the chain has mixed reflect
where you started, which is what burn-in discards and why settling
diagnostics exist.

**Confusing the stationary spread with the most likely state.** It's the
long-run fraction of time spent in each state, not a guess of where the
chain is now.

## Questions people ask

<strong>What is the Markov property?</strong> The next state depends only on the current state, not on how you got there. History is summarised entirely by where you are now.

<strong>What is a transition matrix?</strong> A matrix whose entry (i, j) is the probability of moving from state i to state j. Each row sums to one.

<strong>What is a stationary distribution?</strong> A distribution pi with pi times P equal to pi. If you start in it, you stay in it as the chain runs.

<strong>When does a chain converge to a steady state?</strong> When it is irreducible and aperiodic: every state can reach every other, and it does not cycle with a fixed period.

<strong>How do I compute the n-step probabilities?</strong> Raise the transition matrix to the n-th power. Entry (i, j) of P to the n is the chance of being in j after n steps from i.

<strong>Where are Markov chains used?</strong> In PageRank, MCMC sampling, language modelling, queues and reinforcement learning, where states form a Markov decision process.

## Walk the chain to its steady state

A three-state weather chain, stepped forward until the spread stops moving, then checked against the eigenvector that predicts it.

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
intro: The short list of identities behind each grad you'll write. The dim check that makes them safe.

## Why it needs its own name

Nothing here is new calculus. Differentiating `x'Ax` is the
[product rule](the_chain_rule.html) and
[partial derivs](partial_derivatives_and_gradient.html) applied to a sum,
and you could always expand into indices and grind it out.

What mat calculus adds is **form that stays compact** as the objects grow,
plus a small collection of identities worth storing so you never expand
any of it.

The demo on this page is on purpose one-dimensional. The calculus
underneath is the same in any number of dims. It's only the shapes that
change, and the shapes are the part you've to be careful about.

## The shape rule

The single most handy fact, and the one that catches almost each mistake:

**The grad of a scalar for a thing has the same shape as that
a thing.**

A loss is a scalar. Differentiate it by a 784&times;128 weight mat and the
result is 784&times;128. By a length-128 bias vector, and it's length 128.

This is why gradient descent can write `W -= lr * dW` at all: the update has to
have the same shape as the thing it updates. It's also the fastest debugging
tool available. If a hand-derived grad comes out the wrong shape, the
derivation is wrong, and you know before running any of it.

Two rules exist for laying out derivs &mdash; numerator layout and
denominator layout &mdash; and they differ by a transpose. Papers rarely say
which they use. The shape rule resolves it each time: whichever orientation
matches the param is the one meant.

## The identities

Almost all reduces to these:

| Expression | Derivative with respect to x |
|---|---|
| `a'x` | `a` |
| `x'a` | `a` |
| `x'x` | `2x` |
| `x'Ax` | `(A + A')x`, which is `2Ax` when A is symmetric |
| `Ax` (Jacobian) | `A` |

And two more, for a mat:

| Expression | Derivative with respect to W |
|---|---|
| `a'Wb` | `ab'` |
| `tr(W'A)` | `A` |

The pattern in the first table is worth noticing: they're the mat versions
of `d(ax)/dx = a` and `d(ax^2)/dx = 2ax`. The `(A + A')` appears because both
copies of `x` in `x'Ax` contribute, and when `A` is even they contribute
the same way.

## Working an example

Least squares, from the identities alone.

```
L = ||Ax - b||^2 = (Ax - b)'(Ax - b)
  = x'A'Ax - 2b'Ax + b'b
```

Differentiate term by term. The first is `x'Mx` with `M = A'A`, which is
even, giving `2A'Ax`. The second is linear in `x`, giving `-2A'b`. The
third has no `x`.

```
dL/dx = 2A'Ax - 2A'b
```

Set it to zero and you've the normal equations, `A'Ax = A'b` &mdash; the
formula [the QR module](qr_decomposition.html) then shows why you shouldn't
solve right.

## The layer everyone needs

For a linear layer `y = Wx + b` with loss `L`:

```
dL/dW  =  (dL/dy) x'        an outer product
dL/db  =  dL/dy
dL/dx  =  W' (dL/dy)        passed back to the previous layer
```

Three lines, and they're the whole of backpropagation through a dense layer.

Check them against the shape rule. If `dL/dy` is `m`-long and `x` is `n`-long,
the outer product is `m`&times;`n`. The shape of `W`. And `W'` is
`n`&times;`m`, so `W'(dL/dy)` is `n`-long, matching `x`. each term lands where
it should, and if it doesn't, a thing is transposed.

The transpose in that last line is why the backward pass is at times given
as running the network in reverse: the same weights, applied the other way
round.

## One gradient, worked and checked

The identities are worth exercising on numbers. Take `f(x) = x'Ax` with
`A = [[2, 1], [1, 3]]` (even) at `x = (1, 2)`. The rule says the grad is
`(A + A')x = 2Ax`:

`2Ax = 2 &middot; (2&middot;1 + 1&middot;2,  1&middot;1 + 3&middot;2) =
2 &middot; (4, 7) = (8, 14)`.

Check it against the meaning by nudging each input. `f(1, 2) =
2 + 2&middot;2 + 3&middot;4 = 18`. Grow `x&#8321;` by a small `h`: the change
in `f` cut by `h` approaches 8. Grow `x&#8322;`: it approaches 14. The
partial derivs are the grad's components, and they match the identity
term for term.

The shape rule catches the error you're most likely to make. `f` is a scalar and
`x` is length 2, so `df/dx` must be length 2. Which `(8, 14)` is. Had a
derivation made a 2&times;2 or a scalar, it would be wrong before any
math was checked. That single check. Does the grad have the shape
of the thing it differentiates &mdash; resolves the numerator-versus-denominator
layout ambiguity each time, because only one orientation matches the param.

The same check scales straight to a network layer. For `y = Wx + b`, the weight
grad is the outer product `(dL/dy) x'`: if the outgoing error is `m`-long and
the input `n`-long, that product is `m&times;n`. The shape of `W` &mdash;
so the update `W -= lr &middot; dW` type-checks by build. Get a transpose
wrong and the shapes stop matching before any number is found. This Is why the
shape rule is the fastest debugging tool a backward pass has.

That transpose in the input grad, `W'(dL/dy)`, is why the backward pass is
given as running the network in reverse: the same weights, applied the other
way round, carrying the error back to the layer before.

None of this is new calculus. Differentiating `x'Ax` is the product rule
applied to a sum &mdash; but the compact form and the handful of stored
identities are what let you write a grad down without expanding into indices
each time.

## Where it goes wrong

**Mixing layout rules mid-derivation.** Pick one, and use the shape rule
to check.

**Losing that `x'Ax` gives `(A + A')x`.** The shortcut `2Ax` is only valid
for even `A`.

**Deriving without checking shapes.** It costs seconds and catches most errors.

**Trusting a hand deriv without a numeric check.** Compare against a
finite difference on a small random input. each framework ships a grad
checker for this, and it's worth using when writing a custom op.

## Questions people ask

<strong>What is the gradient of a scalar with respect to a vector?</strong> A vector of the same shape holding each partial derivative. It points in the direction of steepest increase.

<strong>What is the shape rule?</strong> The derivative of a scalar loss with respect to a matrix has the same shape as that matrix. If your result has a different shape, something is transposed.

<strong>What is the gradient of x transpose A x?</strong> (A + A transpose) times x, which reduces to 2 A x when A is symmetric.

<strong>What is the gradient of the least-squares loss?</strong> For the loss squared norm of (X w - y), it is 2 X transpose (X w - y). Setting it to zero gives the normal equations.

<strong>What is the gradient of a linear layer?</strong> For y = W x + b, the gradient with respect to W is the outer product of the upstream gradient and x. The gradient with respect to x is W transpose times the upstream gradient.

<strong>How can I check my derivation?</strong> Compare with a finite-difference gradient on a small random example. Autodiff libraries also provide gradient check tools.

## The four gradients you keep meeting

each rule here is checked by number rather than quoted. These four cover most of what a backward pass finds.

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
print("now the one that matters: a linear layer's weight gradient.")
W, inp, target = rng.normal(size=(3,4)), rng.normal(size=4), rng.normal(size=3)
def loss(Wm):
    return ((Wm @ inp - target) ** 2).sum()
err = W @ inp - target
closed_w = 2 * np.outer(err, inp)
print("  numeric vs outer(2*error, input): max diff %.2e"
      % np.abs(num_grad(loss, W) - closed_w).max())
print("the gradient has the same shape as W because it is outer(error, input).")
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
    """title: Combinatorics: Permutations and Combinations
intro: The counting that chance is built on. The one question that decides which formula to use.

## The question to ask first

**Does order matter?**

Three medals from eight runners: gold, silver and bronze are different outcomes
based on who gets which. So Order matters. That is a **permutation**.

Three people for a committee from eight: the same three people are the same
committee but you list them. Order doesn't matter. That is a
**combination**.

All else follows from answering that.

## The formulas

**Permutations** of `k` from `n`:

```
P(n, k)  =  n! / (n - k)!
```

There are `n` choices for the first spot, `n - 1` for the second, and so on
for `k` spots. The factorial ratio is just that product written compactly.

**Combinations** of `k` from `n`:

```
C(n, k)  =  n! / ( k! (n - k)! )
```

Count the sorted setups, then divide by `k!` because each unordered
pick was counted once for each order its members could have appeared in.

The readout makes the tie concrete: at n = 12, k = 5 the sorted count
is 95,040 and the unordered is 792. 95,040 / 792 is just 120 = 5!.

## Reading the shape

The bars are `C(n, k)` for each `k` from 0 to n.

**Even.** `C(n, k) = C(n, n-k)`. Choosing which `k` to keep is the
same act as choosing which `n - k` to leave.

**Largest in the middle.** There are far more ways to pick half of a thing
than to pick almost none or almost all.

**Huge quickly.** Drag `n` to 24 and the middle bar passes two and a half
million. This growth is why brute force over subsets is hopeless past small `n`,
and why the readout switches to scientific form.

That row of numbers is a row of Pascal's triangle, and the recurrence
`C(n,k) = C(n-1,k-1) + C(n-1,k)`. Either the last item is in your
pick or it isn't &mdash; is the standard dynamic-programming way to
find them without factorials.

## With repetition

A third case, easy to miss. If the same item can be chosen more than once and
order matters &mdash; a 4-digit PIN. Here Digits may repeat &mdash; the count
is simply `n^k`. The readout gives this alongside.

At n = 10, k = 4 that is 10,000 PINs, against `P(10, 4) = 5,040` if no digit
could repeat.

## Why it matters here

**Binomial chances.** The `C(n, k)` in
[the binomial](bernoulli_binomial_poisson.html) is just this count &mdash;
the number of orders in which `k` successes could have arrived.

**Hypothesis testing.** Permutation tests build a null spread by
enumerating or sampling rearrangements of the labels, and the count above says
whether enumeration is feasible.

**Cross-validation.** The number of ways to split data into folds.

**Feature pick.** Choosing `k` features from `n` is `C(n, k)`, which is why
exhaustive search is abandoned almost right away and greedy or smoothed
methods are used instead.

**cost args.** A great deal of "this is exponential" is this table
growing.

## Where it goes wrong

**Not asking whether order matters.** The commonest error, and it's a factor of
`k!`.

**finding factorials right.** `21!` overflows a 64-bit int, and
`C(n, k)` is often far smaller than the factorials used to define it. Work in
logarithms, or use the multiplicative recurrence. This Is what this page does.

**Losing repetition is allowed.** Passwords, dice and sampling with
swap all permit it.

**Double counting.** When the objects aren't all distinguishable the plain
formulas over-count, and the multiset versions are needed instead.

## A worked example: the birthday problem

In a room of 23 people, the chance that two share a birthday is just over half.
That number is famous for feeling wrong, and working it out teaches the single
most handy counting trick there's.

Counting "at least one shared birthday" right is miserable: one pair, two
pairs, a triple, a triple and a pair. So on, all shared. So count the
opposite &mdash; **all birthdays different** &mdash; which is one clean product,
and subtract from 1. This is **complementary counting**, and reaching for it's
often the whole trouble of a counting problem.

With 365 equally likely days and `k` people, the total number of ways to assign
birthdays is `365^k`. The number of ways with no repeat is `P(365, k)`, the
sorted count from above. So:

```
P(all different)  =  P(365, k) / 365^k
                  =  (365/365)(364/365)(363/365) ... ((366-k)/365)
```

Each new person must dodge each birthday already taken, so each factor is
slightly smaller than the last:

|people|P(all different)|P(a shared birthday)|
|---|---|---|
|10|0.883|11.7%|
|20|0.589|41.1%|
|**23**|**0.493**|**50.7%**|
|30|0.294|70.6%|
|50|0.030|97.0%|
|70|0.0008|99.9%|

The reason 23 feels far too small is that people picture *their own* birthday
being matched, which needs 253 people to reach even odds. The question is
not about you. It's about **pairs**, and 23 people make
`C(23, 2) = 253` of them. Each a separate chance to collide.

That gap between "people" and "pairs" is a quadratic hiding behind a linear
intuition, and it's just why hash collisions arrive far sooner than the
table size suggests. The birthday bound is the reason a 64-bit hash starts
colliding after around 2&sup3;&sup2; items rather than 2&sup4;.

## Questions people ask

**Which of the three formulas do I want?** Two questions settle it each time
&mdash; can an item repeat, and does order matter:

|repeats?|order matters?|count|example|
|---|---|---|---|
|yes|yes|`n^k`|a 4-digit PIN|
|no|yes|`P(n, k)`|gold, silver, bronze|
|no|no|`C(n, k)`|a committee of three|
|yes|no|`C(n+k-1, k)`|scoops of ice cream|

**How do I find C(n, k) without overflowing?** Never build the factorials.
Times and divide alternately &mdash; `C(n,k) = C(n,k-1) * (n-k+1) / k` &mdash;
which keeps each mid an exact int and roughly the size of the
answer. For very large `n`, work with `lgamma` in log space and exponentiate at
the end. Python's `math.comb` already does the safe thing.

**Why is C(n, 0) equal to 1?** There's just one way to choose nothing: take
nothing. It isn't a special case bolted on. It's what makes the
symmetry `C(n,k) = C(n,n-k)` and Pascal's recurrence hold at the edges without
exceptions.

**What if some items are the same?** The plain formulas assume each item is
distinguishable. Arranging the letters of *BANANA* isn't `6!`, because swapping
the two Ns changes nothing. Divide by the factorial of each repeat count,
`6!/(3! 2! 1!) = 60`.

**Is C(n, k) the same as "n choose k"?** Yes. And the same as the
binomial coeff, and the same as a row entry of Pascal's triangle. Three
names, one number, which is a large part of why this topic reads as harder than
it's.

## List them, then count them

Small enough to print each setup. So The formulas are checkable rather than stored.

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
