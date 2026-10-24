# -*- coding: utf-8 -*-
"""Content for 20 generated lessons in the 47-page maths track.

This module stores each lesson's visualisation and article source. The other
27 lessons are authored in the same track's content/articles/maths directory.
Together they provide the linear algebra, calculus, probability, and
statistics used by later machine-learning modules.

These are demonstrations rather than simulations - nothing is fitted, and
the arithmetic is the point. The SVD on the page is a real decomposition of
the matrix the reader is editing, and the central-limit page resamples the
population it draws.

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
    """title: Basis, Span and Orthogonality
intro: Span describes what vectors can build; a basis gives each point one unambiguous set of coordinates.

## Span and dimension

The span of vectors is the set of all linear combinations of them. In the plane, two non-parallel vectors span every point; if they lie on the same line, their combinations reach only that line. The visualiser makes this loss of a direction visible as the parallelogram collapses.

<div class="vz-math-block" role="math" aria-label="the span of v one through v k is all linear combinations c one v one through c k v k">span(v₁, …, vₖ) = {c₁v₁ + ··· + cₖvₖ}</div>

## When vectors form a basis

A basis both spans the space and is linearly independent: none of its vectors can be made from the others. These conditions mean every point has exactly one coordinate representation in that basis. A two-dimensional space needs two basis vectors; a three-dimensional space needs three. The number is the dimension, independent of which basis you choose.

For example, (2, 1) and (1, 3) form a basis of the plane. To express (5, 5), solve 2a + b = 5 and a + 3b = 5, giving a = 2 and b = 1.

## Orthogonality simplifies coordinates

Nonzero orthogonal vectors are independent, but a basis need not be orthogonal. In an orthonormal basis (orthogonal unit vectors), each coordinate is just a dot product with its basis vector. This is why QR decomposition and PCA use orthogonal directions; see [vectors and the dot product](vectors_and_dot_product.html), [QR decomposition](qr_decomposition.html), and [PCA's use of SVD](singular_value_decomposition.html).

Orthogonality does not fix every numerical problem: nearly dependent vectors can still make coordinate calculations sensitive to rounding. For a square matrix of basis columns, a zero determinant means dependence; a small determinant alone is not a reliable condition test in higher dimensions.

## Try this above

Drag one basis vector toward the other and watch the reachable region flatten. Then restore a non-parallel pair and compare the span with the whole plane.

## Sources and next steps

- [MIT OpenCourseWare: Linear Algebra](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) develops span, independence, bases, and orthogonality.
- Continue with [matrix transformations](matrix_as_transformation.html) to see how a basis records where a linear map sends space.""",
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
    """title: Singular Value Decomposition
intro: SVD factors any real matrix into rotations or reflections and axis-wise scaling, exposing its most important directions.

## The factorisation

Every real m × n matrix A can be written as A = UΣVᵀ. The columns of U and V are orthonormal directions; the nonnegative diagonal entries of Σ are singular values, ordered from largest to smallest. Right singular vectors in V describe input directions; the matching columns of U show their output directions.

<div class="vz-math-block" role="math" aria-label="A equals U Sigma V transpose">A = UΣVᵀ</div>

A vector along a right singular direction is mapped to the matching left direction, scaled by its singular value. A zero singular value marks a collapsed direction. Unlike eigendecomposition, SVD applies to rectangular matrices and does not require the matrix to be symmetric.

## Low-rank approximation

Keeping only the k largest singular values gives the best rank-k approximation to A in the usual Frobenius and spectral norms. This supports compression and denoising, but small singular values are not automatically noise: choosing k requires evidence from the data and task. The rank is the number of nonzero singular values (or values above a numerical tolerance).

For a small example, A = [[3, 0], [0, 1]] already has singular values 3 and 1: its first axis is stretched three times as much as the second. See [rank](rank_and_linear_independence.html), [projections](projections.html), and [PCA](eigenvalues_and_eigenvectors.html).

## Try this above

Reduce the number of retained singular directions and compare the reconstructed matrix with the original. Observe which structure disappears first.

## Sources and next steps

- [NumPy linalg.svd](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html) documents the computed factorisation and conventions.
- See [QR decomposition](qr_decomposition.html) for a related factorisation used in solving least-squares problems.""",
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
    """title: Jacobian and Hessian
intro: The Jacobian collects first derivatives of a vector function; the Hessian collects second derivatives of a scalar function.

## First derivatives as a matrix

For f: ℝⁿ → ℝᵐ, the Jacobian has one row per output and one column per input. Its entry Jᵢⱼ is ∂fᵢ/∂xⱼ. For a scalar output (m = 1), it contains the gradient components, with row-versus-column convention depending on notation.

<div class="vz-math-block" role="math" aria-label="Jacobian entry i j is partial f i by partial x j">Jᵢⱼ = ∂fᵢ / ∂xⱼ</div>

For f(x,y) = (x² + y, xy), the Jacobian is [[2x, 1], [y, x]]. It describes the best local linear approximation to the function near a point. The multivariable chain rule multiplies Jacobians in composition order; see [the chain rule](the_chain_rule.html).

## Curvature as a second-derivative matrix

For scalar f, the Hessian Hᵢⱼ = ∂²f/(∂xᵢ∂xⱼ). For f(x,y) = x² + 3y², H = [[2, 0], [0, 6]], so curvature is stronger along y. Positive curvature in every direction indicates a strict local minimum; mixed positive and negative curvature indicates a saddle, under the usual smoothness conditions.

Newton's method uses curvature to choose a step, but a neural-network Hessian is enormous and can be indefinite. Large-scale optimisers therefore use approximations or first-order methods. See [matrix calculus](matrix_calculus.html) and [convexity](convexity_and_optimisation.html).

## Try this above

Compare the Jacobian entries as you move the input, then inspect how the Hessian changes the local curvature estimate.

## Sources and next steps

- [MIT OpenCourseWare: Multivariable Calculus](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/) covers multivariable derivatives and local approximations.
- See [matrix calculus](matrix_calculus.html) for derivative shapes used in machine-learning code.""",
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
    """title: Convexity and Optimisation
intro: Convexity rules out hidden local minima: for a convex objective, every local minimum is global.

## The chord condition

A set is convex when the line segment between any two of its points stays inside it. A function f is convex when its graph lies at or below every chord between two points:

<div class="vz-math-block" role="math" aria-label="f of t x plus one minus t y is at most t f x plus one minus t f y for t between zero and one">f(tx + (1−t)y) ≤ tf(x) + (1−t)f(y), &nbsp; 0 ≤ t ≤ 1</div>

For a twice-differentiable one-variable function, f″(x) ≥ 0 everywhere on an interval is sufficient for convexity there. For a multivariable function, the Hessian must be positive semidefinite throughout the convex domain.

## Why it helps—and what it cannot promise

For a convex objective, any local minimum is global. This makes optimisation easier to reason about, though a minimum may still be non-unique and an algorithm may converge slowly. Many deep-learning objectives are non-convex; gradient methods can still find useful solutions, but convex guarantees do not apply. See [gradients](partial_derivatives_and_gradient.html) and [Hessians](jacobian_and_hessian.html).

A learning rate controls update size, not convexity. On a simple quadratic, too large a step can oscillate or diverge even though the objective is convex.

## Try this above

Compare a bowl-shaped curve with a curve that has multiple dips. Move the optimiser step size and observe convergence separately from the shape of the objective.

## Sources and next steps

- [MIT OpenCourseWare: Convex Analysis and Optimization](https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/) covers convex sets and functions.
- See [Lagrange multipliers](lagrange_multipliers.html) for constrained optimisation.""",
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
intro: A Taylor polynomial approximates a smooth function near a chosen point using its derivatives there.

## Build the approximation

Around x = a, the degree-n Taylor polynomial is a sum of derivative terms:

<div class="vz-math-block" role="math" aria-label="Taylor polynomial sum from k zero to n of f kth derivative at a times x minus a to k divided by k factorial">Tₙ(x) = Σₖ₌₀ⁿ f⁽ᵏ⁾(a)(x−a)ᵏ/k!</div>

For eˣ around a = 0, every derivative equals 1, so T₃(x) = 1 + x + x²/2 + x³/6. At x = 0.1 this gives 1.10517, close to e^0.1 ≈ 1.10517. Near the expansion point, higher-degree terms often improve the approximation.

## Local does not mean universal

The error depends on the function, expansion point, and distance from that point. A Taylor series may converge only within a limited interval; a finite polynomial can become inaccurate far away. Use the remainder bound or compare with the original function over the range where the approximation will be used.

Optimisers use first- and second-order Taylor approximations to estimate how a loss changes after a parameter step. Newton's method uses local curvature; see [Jacobians and Hessians](jacobian_and_hessian.html). The derivative definition is the first-order version; see [derivatives and slope](derivatives_and_slope.html).

## Try this above

Increase the polynomial degree and move x farther from the expansion point. Compare the approximation error near and far from that point.

## Sources and next steps

- [MIT OpenCourseWare: Single Variable Calculus](https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/) covers Taylor polynomials and error.
- Continue with [the chain rule](the_chain_rule.html) for derivatives of composed functions.""",
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
intro: Expectation is a distribution’s long-run average; variance measures how far values spread around that average.

## Average and spread

For a discrete random variable X, the expected value weights each outcome by its probability: E[X] = Σₓ xP(X=x). Variance is the expected squared deviation from the mean, and standard deviation is its square root:

<div class="vz-math-block" role="math" aria-label="variance of X equals expected value of X minus expected X squared; standard deviation is square root variance">Var(X) = E[(X−E[X])²] &nbsp; σ = √Var(X)</div>

For a fair six-sided die, E[X] = 3.5 and Var(X) = 35/12. The mean need not be a possible outcome; it summarises the distribution, not a prediction of one roll.

## Rules that simplify calculations

Expectation is linear: E[aX+bY] = aE[X]+bE[Y], whether or not X and Y are independent. Variance is different: Var(X+Y) = Var(X)+Var(Y)+2Cov(X,Y). Only when covariance is zero does it reduce to the sum of variances; independence is sufficient but not necessary. See [covariance and correlation](covariance_and_correlation.html).

Variance is measured in squared units, while standard deviation returns to the original units. The [mean, variance, and standard deviation lesson](mean_variance_standard_deviation.html) shows how these summaries are calculated from data.

## Try this above

Change the probability assigned to each outcome. Watch the mean move and compare the spread with the distribution’s shape.

## Sources and next steps

- [OpenStax: Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e) covers expected value and variance.
- Continue with [sampling distributions](sampling_distributions.html) to see how these quantities vary across samples.""",
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
    """title: Bernoulli, Binomial and Poisson Distributions
intro: These discrete models describe one binary trial, successes across fixed trials, and event counts over a fixed interval.

## From one trial to a count

A Bernoulli variable is 1 with probability p and 0 with probability 1−p. Its mean is p and variance p(1−p). The sum of n independent Bernoulli trials with the same p is binomial:

<div class="vz-math-block" role="math" aria-label="binomial probability of k successes equals n choose k times p to k times one minus p to n minus k">P(X=k) = C(n,k)pᵏ(1−p)ⁿ⁻ᵏ</div>

For n = 5 and p = 0.2, the chance of exactly one success is 5(0.2)(0.8)⁴ = 0.4096. The model requires a fixed number of independent trials with the same success probability; if those assumptions fail, the binomial calculation may not fit.

## Poisson event counts

A Poisson variable with rate λ has P(X=k) = e⁻λ λᵏ/k!. It models counts over a fixed interval under assumptions such as a stable rate and independent events in disjoint intervals. Its mean and variance are both λ. It can approximate a binomial distribution when n is large, p is small, and λ = np is held fixed; the approximation is not an identity.

See [combinatorics](combinatorics.html) for the binomial coefficient and [expectation and variance](expectation_and_variance.html) for the moments.

## Try this above

Change n and p separately while holding np fixed. Compare the binomial and Poisson probabilities, especially for small p and larger n.

## Sources and next steps

- [OpenStax: Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e) covers discrete random variables and binomial and Poisson models.
- Continue with [sampling distributions](sampling_distributions.html) to see how statistics vary across repeated samples.""",
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
    """title: Central Limit Theorem
intro: Under suitable conditions, sums and averages of many independent contributions become approximately normal after standardisation.

## What the theorem says

For independent, identically distributed variables with finite mean μ and finite variance σ², the standardised sample mean approaches a standard normal distribution as sample size grows:

<div class="vz-math-block" role="math" aria-label="square root n times sample mean minus mu divided by sigma converges in distribution to standard normal">√n(x̄−μ)/σ → N(0,1) in distribution</div>

The theorem explains why normal approximations appear in inference even when individual observations are not normal. It concerns the distribution of a sum or average across repeated samples, not the shape of the raw data itself.

## Conditions and practical limits

There is no universal sample size that guarantees a good approximation. Strong skew, heavy tails, dependence, or rare events can require much larger samples or invalidate the simple form. If variance is infinite, the usual result does not apply. The [sampling-distributions lesson](sampling_distributions.html) distinguishes this distribution from population spread.

The theorem does not claim every statistic is normal. Medians, maxima, and ratios can have different limiting behavior. Check the statistic and assumptions used by the approximation before applying normal-based intervals or tests.

## Try this above

Compare repeated sample means as n grows for both a symmetric and a skewed population. Look at the mean’s distribution, not just the original observations.

## Sources and next steps

- [OpenStax: Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e) introduces the central limit theorem and sampling distributions.
- Continue with [confidence intervals](confidence_intervals.html) to see one practical use of the approximation.""",
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
    """title: Quantiles and Percentiles
intro: A quantile marks a position in an ordered distribution; a percentile expresses that position on a 0–100 scale.

## Read a quantile

The p-quantile is a value with roughly proportion p of observations at or below it. The median is the 0.5 quantile; the 25th and 75th percentiles are the first and third quartiles. For 1, 2, 4, 7, 9, the median is 4.5 under the common “average the two middle values” convention.

<div class="vz-math-block" role="math" aria-label="the p quantile has approximately p proportion of observations at or below it">Q(p): approximately p of the distribution lies at or below Q(p)</div>

There are several accepted sample-quantile conventions, especially for small datasets. Software may interpolate between adjacent observations differently, so name the convention when exact reproducibility matters.

## Why quantiles are useful

Quantiles describe location without assuming a symmetric distribution and are less affected by extreme observations than the mean. The interquartile range, Q(0.75) − Q(0.25), measures the middle half of the data. A percentile rank is not the same as a percentage of correct answers; it describes relative position in a reference distribution.

Use quantiles to report skewed measurements, thresholds, and prediction intervals. See [mean, median, and mode](mean_mode_and_median.html) and [confidence intervals](confidence_intervals.html).

## Try this above

Change the requested percentile and inspect which observations fall below it. Try a small sample to see where software conventions can differ.

## Sources and next steps

- [NIST: Quantiles and Percentiles](https://www.itl.nist.gov/div898/handbook/prc/section2/prc262.htm) discusses quantile definitions.
- Continue with [mean, median, and mode](mean_mode_and_median.html) to compare location summaries.""",
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
    """title: Sampling Distributions
intro: A sampling distribution describes how a statistic varies across repeated samples from the same population.

## The statistic is random too

A sample mean changes from sample to sample, even when the population stays fixed. Its sampling distribution is the distribution of those possible means. For independent observations with population mean μ and variance σ², the sample mean has expectation μ and standard error σ/√n.

<div class="vz-math-block" role="math" aria-label="standard error of the sample mean equals population standard deviation divided by square root n">SE(x̄) = σ/√n</div>

Standard deviation describes variation among individual observations; standard error describes variation of an estimator across samples. Increasing sample size shrinks the standard error at a square-root rate under the stated assumptions, not the spread of the underlying population.

## Shape depends on the statistic and data

The sampling distribution of the mean becomes approximately normal under central-limit conditions, but small samples from skewed or heavy-tailed populations may not. Dependence between observations changes the calculation. See [the central limit theorem](central_limit_theorem.html), [normal distribution](the_normal_distribution.html), and [confidence intervals](confidence_intervals.html).

## Try this above

Draw repeated samples at two sample sizes. Compare the distribution of individual observations with the distribution of sample means.

## Sources and next steps

- [OpenStax: Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e) covers sampling distributions and standard error.
- Continue with [confidence intervals](confidence_intervals.html) to use sampling variability for estimation.""",
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
    """title: Confidence Intervals
intro: A confidence interval is a procedure that uses sample data to produce a range for an unknown population quantity.

## Construct and interpret the interval

For a sample mean with known population standard deviation under a normal model (or an appropriate large-sample approximation), a two-sided confidence interval is x̄ ± z*σ/√n. In practice, σ is often unknown and a t critical value with estimated standard error is used under the relevant assumptions.

<div class="vz-math-block" role="math" aria-label="estimate plus or minus critical value times standard error">estimate ± critical value × standard error</div>

A 95% confidence procedure produces intervals that contain the fixed parameter in about 95% of repeated samples under the model. After one interval is calculated, frequentist interpretation does not assign a 95% probability to the fixed parameter being inside that particular interval.

## Width and assumptions

Larger samples usually narrow the interval because standard error shrinks; greater variability or higher confidence widens it. The interval’s validity depends on the sampling design, model, and method. A narrow interval from biased or dependent data is not reliable. See [sampling distributions](sampling_distributions.html), [standard deviation](mean_variance_standard_deviation.html), and [hypothesis testing](hypothesis_testing_and_p_values.html).

## Try this above

Increase the sample size and then the confidence level. Observe how each change affects the interval width.

## Sources and next steps

- [NIST: Confidence Intervals](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm) explains interval estimation.
- Continue with [hypothesis tests and p-values](hypothesis_testing_and_p_values.html) to compare interval and test interpretations.""",
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
    """title: Hypothesis Testing and P-values
intro: A p-value measures how surprising the observed data would be if the null model were true; it is not the probability the null is true.

## Specify the test

A hypothesis test starts with a null hypothesis H₀ and an alternative H₁, then chooses a test statistic and a reference distribution under H₀. The p-value is the probability, assuming H₀ and the model assumptions, of observing a statistic at least as incompatible with H₀ as the one measured.

<div class="vz-math-block" role="math" aria-label="p value is probability under the null of a test statistic at least as extreme as observed">p-value = P(statistic at least as extreme as observed | H₀)</div>

For a two-sided test of a normal mean with known standard error, the statistic is z = (x̄−μ₀)/SE; evidence in either tail contributes to the p-value. A one-sided test counts one specified direction. The direction must be chosen before inspecting results.

## What a p-value cannot tell you

A small p-value is evidence against the null under the test model, not the probability that H₀ is true, the size of an effect, or its practical importance. A large p-value does not prove no effect; the data may be imprecise. Report effect estimates and uncertainty too. Multiple testing and optional stopping can make nominal p-values misleading.

See [confidence intervals](confidence_intervals.html) and [Type I and Type II errors](type_i_and_type_ii_errors.html).

## Try this above

Move the observation farther from the null while keeping the standard error fixed, then change the sample size. Compare the p-value with the effect size.

## Sources and next steps

- [American Statistical Association: Statement on P-values](https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf) explains proper interpretation.
- Continue with [Type I and Type II errors](type_i_and_type_ii_errors.html) for long-run test error rates.""",
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
    """title: Type I and Type II Errors
intro: A decision threshold trades off false alarms against missed effects; power is the chance to detect a specified effect.

## The two error rates

A Type I error rejects a true null hypothesis; its long-run probability is the significance level α under the test procedure. A Type II error fails to reject a false null; its probability β depends on the alternative effect and study design. Power is 1−β.

<div class="vz-math-block" role="math" aria-label="power equals one minus beta, the probability of rejecting the null under a specified alternative">Power = 1 − β = P(reject H₀ | specified alternative)</div>

Lowering the decision threshold often reduces false positives while increasing missed effects, for a fixed design. Increasing sample size can improve power, but power also depends on variability, effect size, test direction, and α. There is no single power value independent of the alternative being considered.

## Choose the design before collecting data

Set α and choose a scientifically meaningful effect size in advance. A test with low power may miss a real effect; a statistically significant result can still be too small to matter. “Fail to reject” is not proof that the null is true. See [hypothesis testing and p-values](hypothesis_testing_and_p_values.html) and [confidence intervals](confidence_intervals.html).

## Try this above

Change the threshold and sample size while holding the alternative fixed. Compare the false-alarm region and probability of detecting the effect.

## Sources and next steps

- [NIST: Quantitative Techniques](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35.htm) explains Type I and Type II error probabilities.
- Review [sampling distributions](sampling_distributions.html) to understand the uncertainty behind these error rates.""",
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
    """title: QR Decomposition
intro: QR writes a matrix as an orthonormal basis times a triangular matrix, making least-squares problems easier to solve.

## What Q and R contain

For a real matrix A, QR factorisation writes A = QR. The columns of Q are orthonormal; R is upper triangular. For a full-column-rank matrix, the reduced factorisation keeps only the columns needed for its column space. Signs of paired columns in Q and rows in R may vary while their product stays the same.

To solve a least-squares problem min‖Ax − b‖₂, substitute A = QR. Since QᵀQ = I, solve the triangular system Rx = Qᵀb. This avoids forming AᵀA, which can worsen conditioning. See [projections](projections.html) for the geometric view and [matrix multiplication](matrix_multiplication.html) for the products involved.

## A two-vector illustration

Start with a₁ = (1, 1) and a₂ = (1, 0). Normalise a₁ to get q₁ = (1, 1)/√2. Subtract from a₂ its component along q₁; the remaining vector is perpendicular to q₁. Normalising that residual gives q₂. The columns q₁ and q₂ form Q, and the coefficients used in these steps fill R.

Classical Gram–Schmidt can lose orthogonality in floating-point arithmetic for nearly dependent columns. Stable QR implementations use Householder reflections or reorthogonalisation. QR is useful, but it does not make an ill-conditioned problem well-conditioned.

## Try this above

Compare the original columns with the orthogonalised directions and inspect QᵀQ. Nearly dependent inputs make the numerical challenge visible.

## Sources and next steps

- [NumPy linalg.qr](https://numpy.org/doc/stable/reference/generated/numpy.linalg.qr.html) documents QR modes and outputs.
- Continue with [Cholesky factorisation](cholesky_and_positive_definiteness.html) for a specialised factorisation of positive-definite matrices.""",
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
    """title: Cholesky Factorisation and Positive Definiteness
intro: A symmetric positive-definite matrix factors as LLᵀ, enabling efficient solves and correlated sampling.

## Positive definiteness

A real symmetric matrix A is positive-definite when xᵀAx > 0 for every nonzero x. Geometrically, its quadratic form is an upward bowl in every direction. Positive-definiteness implies positive eigenvalues and makes many optimisation and probability calculations well behaved.

The Cholesky factorisation writes A = LLᵀ, where L is lower triangular with positive diagonal entries. For a 2 × 2 example, A = [[4, 2], [2, 3]] factors as L = [[2, 0], [1, √2]], since LLᵀ = A. Solving Ax = b then becomes two triangular solves rather than a general matrix solve.

## Where it is used—and where it fails

Cholesky is used to sample multivariate normal data and to solve symmetric positive-definite systems. A covariance matrix is positive semidefinite in exact arithmetic; it may be singular when variables are redundant, so ordinary Cholesky can fail. Round-off or noisy estimates can also make a theoretically valid matrix appear slightly indefinite. Diagnose the matrix and the model before adding a small diagonal term; regularisation changes the problem.

See [covariance and correlation](covariance_and_correlation.html), [matrix transformations](matrix_as_transformation.html), and [QR decomposition](qr_decomposition.html) for related tools.

## Try this above

Adjust the matrix entries until the quadratic form stops being positive in every direction. Compare the positive-definite case with a singular or indefinite example.

## Sources and next steps

- [NumPy linalg.cholesky](https://numpy.org/doc/stable/reference/generated/numpy.linalg.cholesky.html) states the factorisation and positive-definite requirement.
- Review [eigenvalues](eigenvalues_and_eigenvectors.html) to connect positive definiteness with positive eigenvalues.""",
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
    """title: Lagrange Multipliers
intro: At a smooth constrained optimum, the objective’s gradient is aligned with the constraint’s gradient.

## The tangency condition

To optimise f(x,y) subject to g(x,y) = c, form the Lagrangian L = f − λ(g − c). At a regular constrained optimum, the gradients satisfy ∇f = λ∇g. The constraint curve and a level curve of f are tangent there: moving along the constraint gives no first-order improvement.

<div class="vz-math-block" role="math" aria-label="gradient f equals lambda times gradient g, with g equals c">∇f = λ∇g, &nbsp; g = c</div>

Example: maximise xy subject to x + y = 10 with x,y > 0. Set ∇(xy) = (y,x) and ∇(x+y) = (1,1), so y = λ and x = λ; hence x = y = 5 and the maximum product is 25. The boundary condition and positivity are part of the problem, not optional details.

## What the multiplier means

When the optimum changes smoothly as c changes, λ measures the local change in the optimal objective per unit change in the constraint. This interpretation is often called a shadow price. It can fail at nonsmooth points or when the active constraint set changes. Inequality constraints require the Karush–Kuhn–Tucker conditions, not just this equality rule.

See [convexity and optimisation](convexity_and_optimisation.html) for global guarantees and [derivatives](derivatives_and_slope.html) for the gradient condition.

## Try this above

Move the constraint and watch where it touches a level curve of the objective. Compare the optimum and multiplier as the constraint value changes.

## Sources and next steps

- [MIT OpenCourseWare: Convex Analysis and Optimization](https://ocw.mit.edu/courses/6-253-convex-analysis-and-optimization-spring-2012/) covers constrained optimisation and Lagrange multipliers.
- Continue with [convexity](convexity_and_optimisation.html) to understand when a stationary solution is globally optimal.""",
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
    """title: Jensen’s Inequality
intro: For a convex function, the function of an average is no greater than the average of the function values.

## The inequality

If f is convex and X has a finite expectation, Jensen’s inequality states:

<div class="vz-math-block" role="math" aria-label="f of expected X is less than or equal to expected f of X">f(E[X]) ≤ E[f(X)]</div>

For f(x) = x², this says (E[X])² ≤ E[X²]. The difference is Var(X) ≥ 0. Equality holds when X is constant with probability one, or more generally when f is affine over the values X can take.

## Why averages can mislead

A convex penalty makes large deviations count disproportionately: applying the penalty after averaging is smaller than averaging the penalties. For concave functions the inequality reverses. This is useful in probability, statistics, and machine learning, but first check that the function is convex on the relevant domain and that the expectations exist.

For example, because log(x) is concave on x > 0, E[log X] ≤ log(E[X]). It is not valid to switch these expressions freely. See [expectation and variance](expectation_and_variance.html) and [convexity](convexity_and_optimisation.html).

## Try this above

Compare f at the mean with the mean of f-values as the spread changes. For a convex curve, the latter should stay at least as large.

## Sources and next steps

- [MIT OpenCourseWare: Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2014/) covers expectations and inequalities.
- Review [expectation and variance](expectation_and_variance.html) before applying Jensen’s inequality to random variables.""",
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
    """title: Markov Chains
intro: A Markov chain models step-by-step movement between states when the next state depends on the current one.

## Transition probabilities

A chain has a state space and transition probabilities. With a row-vector convention, a transition matrix P has entries Pᵢⱼ = P(next state = j | current state = i); each row sums to 1. If πₜ is the row vector of state probabilities at time t, then πₜ₊₁ = πₜP.

For two states, sunny and rainy, a matrix such as [[0.8, 0.2], [0.4, 0.6]] says that a sunny day is followed by a sunny day with probability 0.8, while a rainy day is followed by a sunny day with probability 0.4. Starting from π₀ = [1, 0], after one step π₁ = [0.8, 0.2].

## The Markov assumption and long-run behavior

The Markov property says the next state is conditionally independent of earlier history once the current state is known. It is a modelling assumption; if relevant history is omitted, the model may be inadequate.

A stationary distribution satisfies π = πP. Some chains converge to one from many starting states, but convergence is not automatic: reducible or periodic chains can behave differently. See [conditional probability](conditional_probability.html) for transition probabilities and [matrix multiplication](matrix_multiplication.html) for repeated transitions.

## Try this above

Change one transition probability and keep each row normalised. Track how the state distribution evolves over several steps and whether it settles.

## Sources and next steps

- [MIT OpenCourseWare: Introduction to Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2014/) covers conditional probability and stochastic models.
- Continue with [eigenvalues](eigenvalues_and_eigenvectors.html) to understand stationary distributions algebraically.""",
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
    """title: Matrix Calculus
intro: Matrix calculus keeps track of both derivative values and their shapes when functions take vectors and matrices.

## Start with a scalar loss

Let x be a column vector and A a fixed matrix. For f(x) = ½xᵀAx, the gradient is ½(A + Aᵀ)x. If A is symmetric, this simplifies to Ax. The symmetry condition matters; writing Ax without it is a common error.

<div class="vz-math-block" role="math" aria-label="gradient with respect to x of one half x transpose A x equals one half A plus A transpose times x">∇ₓ(½xᵀAx) = ½(A + Aᵀ)x</div>

For A = I, f(x) = ½‖x‖² and ∇f = x. A gradient descent step is x ← x − ηx, where η is the learning rate. The gradient has the same shape as x, which is a useful implementation check.

## Shapes and conventions

A scalar differentiated with respect to a vector gives a vector; a vector-valued function differentiated with respect to a vector gives a Jacobian matrix. Authors differ on whether gradients are written as rows or columns, so read the convention and verify dimensions before multiplying. The [Jacobian and Hessian lesson](jacobian_and_hessian.html) defines these arrays; the [chain rule](the_chain_rule.html) explains how they compose.

In a neural network, matrix calculus expresses how a scalar loss changes through matrix multiplications and activation functions. Derivatives must flow through the transpose implied by the chosen vector convention; shape checking catches many mistakes, but it cannot replace checking the mathematical definition.

## Try this above

Change the vector and matrix entries and compare the displayed derivative with the symmetric and nonsymmetric cases.

## Sources and next steps

- [MIT OpenCourseWare: Matrix Calculus for Machine Learning and Beyond](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/) discusses matrix derivatives and conventions.
- Review [matrix multiplication](matrix_multiplication.html) before tracing a derivative through a layer.""",
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
    """title: Combinatorics
intro: Count outcomes by deciding whether order matters and whether items can repeat.

## Choose the counting rule

For ordered selections of k distinct items from n, the count is n!/(n−k)!. If order does not matter, divide by k! to get the number of combinations, n choose k. If each of k positions can independently take any of n values, repetition is allowed and there are nᵏ sequences.

For a five-card hand from a 52-card deck, order does not matter and cards cannot repeat, so there are 52 choose 5 hands. If instead a five-character code can reuse any of ten digits, there are 10⁵ codes. The problem statement determines the model; choosing a formula before clarifying order and repetition is a common source of errors.

<div class="vz-math-block" role="math" aria-label="n choose k equals n factorial divided by k factorial times n minus k factorial">C(n,k) = n! / [k!(n−k)!]</div>

## Connection to probability

When outcomes are equally likely, probability can be found as favourable outcomes divided by total outcomes. This shortcut does not apply when outcomes have unequal probabilities. The [binomial distribution](bernoulli_binomial_poisson.html) uses combinations to count which k trials succeed; [probability basics](probability_basics.html) explains the assumptions.

## Try this above

Choose a small n and k, then compare ordered selections with combinations. Toggle repetition and verify how the outcome count changes.

## Sources and next steps

- [OpenStax: Introductory Statistics 2e](https://openstax.org/details/books/introductory-statistics-2e) introduces counting rules and combinations.
- Continue with [Bernoulli, binomial, and Poisson models](bernoulli_binomial_poisson.html) to use these counts in probability.""",
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
