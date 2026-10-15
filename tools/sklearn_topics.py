# -*- coding: utf-8 -*-
"""Content for the scikit-learn track.

Modules of short runnable steps rather than one long program, for the same
reason as the NumPy and matplotlib tracks: a single script hides which line
produced which number, and almost every scikit-learn mistake is a line-level
one - fitting on the wrong data, scaling outside a pipeline, reading accuracy
off an imbalanced set.

The track teaches the estimator API first and the estimators second, because
the API is the part that transfers. Once `fit`, `predict` and `transform` are
familiar, a new model is a new import and nothing else.

Every example is deterministic: `random_state=0` on everything that samples,
and printed numbers rounded explicitly, so the output in the page is the
output the reader gets.

scikit-learn ships with Pyodide (1.4.2 there), so it loads from the same CDN
as the interpreter rather than needing a wheel. It is not a small load - see
_sklearn_prelude in tools/runnable_specs.py for the measurements and for why
the estimator imports are left in the reader's editor rather than hidden in
the prelude.
"""

TOPICS = []
CHECKS = {}

# The editors on the built pages take their prelude from
# tools/runnable_specs.py; importing it here keeps the step-card editors in
# step with them rather than carrying a second, subtly different copy.
from runnable_specs import _sklearn_prelude

PRELUDE = _sklearn_prelude()


def topic(slug, title, cat, lead, svg, steps, notes, article, check):
    """One module. `steps` is a list of (heading, blurb, code) triples."""
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "steps": steps, "notes": notes, "article": article, "check": check,
        "wheels": [], "prelude": PRELUDE,
    })
    CHECKS["sklearn/%s.html" % slug] = {"check": check}


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


def _dots(pts, fill=A, r=3):
    return "".join('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (x, y, r, fill)
                   for x, y in pts)


# ---------------------------------------------------------------------------
# 1. The estimator API
# ---------------------------------------------------------------------------
topic(
    "what_is_scikit_learn",
    "fit, predict, transform",
    "The API",
    "Three method names that every model in the library shares - which is why "
    "swapping one model for another is a one-line change.",
    _svg(_box(10, 26, 40, 30, S, M) + _txt(30, 45, "X, y", M, 9) +
         _arrow(52, 41, 66, 41) + _txt(59, 34, "fit", A, 7) +
         _box(68, 22, 44, 38, S, A) + _txt(90, 38, "estimator", A, 8) +
         _txt(90, 50, "learned", M, 7) +
         _arrow(114, 41, 128, 41) + _txt(121, 34, "predict", A, 7) +
         _box(130, 30, 22, 22, S, M) + _txt(141, 44, "y'", M, 9)),
    [
        ("Every model is the same three methods",
         "The library's whole design is that you learn the interface once, "
         "not once per algorithm.",
         '''from sklearn.linear_model import LinearRegression

# Six houses: one feature (rooms), one target (price in thousands).
X = [[1], [2], [3], [4], [5], [6]]
y = [50, 70, 90, 110, 130, 150]

model = LinearRegression()
print("before fit :", hasattr(model, "coef_"))

model.fit(X, y)
print("after fit  :", hasattr(model, "coef_"))

print("prediction for 7 rooms:", model.predict([[7]]))
'''),

        ("The trailing underscore means learned",
         "Attributes ending in an underscore did not exist until fit ran. It is "
         "a naming convention, and it is the whole story of what fitting does.",
         '''from sklearn.linear_model import LinearRegression

X = [[1], [2], [3], [4], [5], [6]]
y = [50, 70, 90, 110, 130, 150]

model = LinearRegression().fit(X, y)

print("coef_      :", model.coef_)
print("intercept_ :", round(model.intercept_, 6))

# Set before fit, by you. No underscore.
print("fit_intercept (a setting you chose):", model.fit_intercept)
'''),

        ("fit returns the estimator, so it chains",
         "Every fit returns self. That is why you will see .fit(X, y) attached "
         "to the constructor on one line.",
         '''from sklearn.linear_model import LinearRegression

X = [[1], [2], [3]]
y = [2, 4, 6]

model = LinearRegression()
same = model.fit(X, y)

print("fit returned the same object:", same is model)
print("so this one-liner works     :",
      LinearRegression().fit(X, y).predict([[4]]))
'''),

        ("Transformers use transform instead of predict",
         "A model predicts a target. A transformer changes the features. The "
         "fit half is identical.",
         '''from sklearn.preprocessing import StandardScaler

X = [[10], [20], [30], [40]]

scaler = StandardScaler()
scaler.fit(X)

print("mean_  :", scaler.mean_)
print("scale_ :", scaler.scale_)
print()
print("transformed:")
print(scaler.transform(X).ravel())
'''),

        ("Swapping the model is one line",
         "Same data, same calls, different algorithm - which is the payoff for "
         "having one interface.",
         '''from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor

# Deliberately not a straight line, so the three models disagree.
X = [[1], [2], [3], [4], [5], [6]]
y = [50, 62, 90, 96, 130, 150]

for model in [LinearRegression(),
              DecisionTreeRegressor(random_state=0),
              KNeighborsRegressor(n_neighbors=2)]:
    model.fit(X, y)
    guess = model.predict([[3.5]])[0]
    print("%-24s %6.1f" % (type(model).__name__, guess))
'''),

        ("X is always 2-D, y is always 1-D",
         "The single most common error message on this track comes from getting "
         "this wrong, and it tells you exactly what it wanted.",
         '''from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3]])
y = np.array([2, 4, 6])
print("X.shape:", X.shape, " y.shape:", y.shape)

flat = np.array([1, 2, 3])
try:
    LinearRegression().fit(flat, y)
except ValueError as e:
    print()
    print("ValueError:", str(e).splitlines()[0])
    print()
    print("fix: flat.reshape(-1, 1) ->", flat.reshape(-1, 1).shape)
'''),
    ],
    [
        "<strong>fit</strong> learns from data, <strong>predict</strong> "
        "produces a target, <strong>transform</strong> produces new features. "
        "Every object in the library is some combination of those three.",
        "An attribute ending in <code class='mono-font'>_</code> was learned "
        "during fit. One without was set by you.",
        "<code class='mono-font'>X</code> is 2-D with one row per sample and "
        "one column per feature; <code class='mono-font'>y</code> is 1-D with "
        "one entry per sample.",
        "A single feature still needs two dimensions - "
        "<code class='mono-font'>reshape(-1, 1)</code> is the usual fix.",
        "<code class='mono-font'>fit</code> returns the estimator, which is why "
        "<code class='mono-font'>Model().fit(X, y)</code> chains.",
        "Calling <code class='mono-font'>predict</code> before "
        "<code class='mono-font'>fit</code> raises "
        "<code class='mono-font'>NotFittedError</code> rather than guessing.",
    ],
    """title: fit, predict, transform: A Practical Guide
intro: scikit-learn has one interface and about two hundred methods behind it. Learning the interface is most of learning the library.

## The problem it solves

scikit-learn is a Python library for machine learning. It covers classification, regression, clustering, dimensionality reduction and preprocessing. Every algorithm in it follows the same interface: three methods named `fit`, `predict` and `transform`.

That consistency is the library's main contribution. You learn the interface once. After that, switching from a linear regression to a random forest is a one-line change. The surrounding code stays the same.

The library sits on top of NumPy and SciPy. It expects numeric arrays as input and returns numeric arrays as output. It does not handle data loading, feature engineering from raw text, or deep learning. Those boundaries are deliberate. They keep the API small and predictable.

Most mistakes in applied machine learning are not about the algorithm. They are about how data reaches the algorithm and how the result is measured. scikit-learn's design reflects that. It spends more surface area on splitting data, building pipelines and scoring predictions than on any single model.

This page covers the interface itself. The three methods, the naming conventions, the shape rules and the two kinds of estimator. Once those are familiar, each later page adds one estimator or one evaluation technique. None of them changes how you call it.

The library ships with small datasets for testing. It also ships with generators that produce synthetic data of a chosen shape. Both are useful for checking that your code runs before pointing it at real data.

each machine-learning library has to answer the same question. How does a program hand data to an method and get an answer back. scikit-learn answered it once, in 2007. Then made each method in the library answer it the same way.

The result is that `fit`, `predict` and `transform` are almost the whole API. A linear regression, a random forest, a support-vector machine and a k-means clustering all expose the same three methods. The code around a model doesn't change when the model does.

The result is that `fit`, `predict` and `transform` are almost the whole API. A linear regression, a random forest, a support-vector machine and a k-means clustering all expose the same three methods. The code around a model doesn't change when the model does.

## fit learns, predict answers

`fit(X, y)` shows the estimator the data and the answers. It stores what it worked out on the object. `predict(X)` takes new data with no answers and makes them.

The split matters more than it looks. Fitting and predicting are separate calls because they happen at different times on different data. You fit once on data you've. Predict many times on data you didn't have when you fitted.

## The underscore convention

scikit-learn marks learned fields with a trailing underscore. The rule is worth taking seriously because it cuts an estimator into two halves.

Fields without an underscore are **settings**: settings you chose, passed to the constructor, present before any data was seen. `n_neighbors`, `max_depth`, `fit_intercept`.

Fields with a trailing underscore are **learned**: they didn't exist before `fit` and they came from the data. `coef_`, `intercept_`, `feature_importances_`, `classes_`.

Reading an estimator so tells you what it was told and what it worked out. The two never get confused. It also means `hasattr(model, "coef_")` is a solid test for "has this been fitted". This Is just what the library's own `check_is_fitted` does.

## Transformers change features rather than predicting

A transformer is the other half of the library. Instead of `predict` it has `transform`. Instead of making a target it makes a new version of `X`.

`StandardScaler` is the canonical one: `fit` finds the mean and standard deviation of each column, `transform` subtracts and cuts. `OneHotEncoder`, `SimpleImputer` and `PCA` are all the same shape.

`fit_transform` does both in one call and is the one you'll write most often on training data. It isn't merely shorthand. For some transformers it's faster than doing the two apart. This Is why it exists as its own method.

The rule that matters: **fit on training data only, transform all**. A scaler fitted on the test set has learned from data the model is supposed to have never seen. The score you get afterwards isn't a score.

## The shapes

`X` is two-dimensional: rows are samples, columns are features. `y` is one-dimensional: one value per row of `X`.

That holds even when there's one feature. This Is where beginners meet their first error. A list of six numbers is six samples of nothing, not one sample of six features. Scikit-learn refuses to guess which you meant. `reshape(-1, 1)` turns a flat array into a column. The error message says so by name.

## The two kinds of estimator

All in the library is one of two things. Telling them apart tells you which method to call.

A **predictor** ends in a target. `LinearRegression`, `LogisticRegression`, `RandomForestClassifier`, `KMeans`. You `fit` them and then `predict`. Classifiers also offer `predict_proba`. This Returns the chance of each class rather than the winning one.

A **transformer** ends in new features. `StandardScaler`, `OneHotEncoder`, `SimpleImputer`, `PCA`. You `fit` them and then `transform`. There's no target to give. There's no `predict`.

The two compose: a chain of transformers followed by one predictor is the shape of each real scikit-learn program. `Pipeline` exists to hold just that chain and give it the same `fit`/`predict` interface as a single estimator. That is why the API is worth learning first. A whole pipeline is used the same way as the simplest model in the library.

## score, and what it means for each

each predictor has a `score(X, y)` method. The number it returns isn't the same quantity for all of them.

For a **classifier**, `score` is fit: the proportion of guesses that were right. For a **regressor**, it's R&sup2;: how much of the variation in the target the model accounts for. Here 1.0 is perfect and 0.0 is no better than always guessing the mean. R&sup2; can be minus. This Means the model is worse than that guess.

Both are conveniences rather than recommendations. Fit is misleading when the classes are imbalanced. R&sup2; says nothing about whether the errors are large in the units you care about. Later modules replace both with metrics that answer a exact question. The `metrics` module holds a few dozen of them.

What `score` is truly handy for is a quick check on the same data with the same model type. For the cross-validation helpers. This Call it by default when you don't name a metric.

## Hyperparameters are set at construction

The constructor takes the settings, and there are often many of them with sensible defaults. `RandomForestClassifier()` works, and so does `RandomForestClassifier(n_estimators=500, max_depth=8, random_state=0)`.

Two methods make those settings inspectable. `get_params()` returns each setting as a dict, including the defaults you didn't pass. This Is the fastest way to find out what an estimator can be configured with. `set_params(**kw)` changes them on an existing object.

Those two aren't conveniences either. They're what makes automated tuning possible. `GridSearchCV` works by calling `set_params` with each combination in turn. This Is why it can tune any estimator in the library, including ones written after it. Any step inside a pipeline.

The corollary is worth remembering: an estimator is fully given by its settings plus its fitted fields. Nothing else is hidden on it.

## random_state, and reproducibility

any of it in the library that makes a random choice takes a `random_state`. Splitting data, resetting k-means, sampling features in a random forest, shuffling folds &mdash; all of them.

Passing an int makes the run reproducible: the same data and the same seed give the same result, each time, on any machine. Leaving it out gives a different answer on each run. This Makes two scores incomparable and a bug hopeless to copy.

The habit worth forming early is to pass `random_state=0` to all that accepts it while you're learning or debugging. To think carefully before dropping it. The one time you truly want it left out is when you're on purpose measuring how much the result varies between runs. Which is a real question. One that a single seeded number can't answer.

## When an estimator has not been fitted

Calling `predict` before `fit` raises `NotFittedError` rather than returning nonsense. The message names the estimator and tells you to call `fit`.

That check exists because the option is worse. An unfitted model has no coeffs. A library that quietly returned zeros or `None` would give a program that runs, makes numbers, and is fully meaningless.

It's also why the underscore rule matters in practice rather than only stylistically: `check_is_fitted` works by looking for fields ending in an underscore. An estimator you write yourself gets the same action for free by following the same rule.

## Why one interface was the right decision

It's worth appreciating how unusual this is. Most machine-learning code before scikit-learn had a shape per method. One library wanted a mat and a separate label vector, another wanted them mixed, a third wanted a configuration file. Checking two methods meant rewriting the code around them. This Meant people checked far fewer than they should have.

Fixing the interface changed what is cheap. Swapping a model turns one line. Trying five is a loop rather than a project. Cross-validation can be written once and work with any of it. It only needs `fit`, `predict` and `score`. A pipeline can hold any steps, because each step honours `fit` and `transform`. A tuner can search any estimator, because `get_params` and `set_params` are universal.

None of that needed the methods to have any of it in common in math. A choice tree and a linear model share no theory at all. They share three method names. That turned out to be enough to build the entire ecosystem of helpers on top.

The hands-on consequence for someone learning: time spent on the API isn't cost before the notable part. It *is* the part that transfers. The estimators are on their own simple to use once the shape is familiar. The modules that follow spend most of their words on when each one is right and how to tell whether it worked, rather than on how to call it.

## What the library deliberately does not do

Knowing the boundary saves looking for things that aren't there.

scikit-learn doesn't do deep learning. There's a small `MLPClassifier`, handy for a demo and not for real work. Any of it serious belongs in PyTorch or a similar library. It doesn't do GPUs. It doesn't do sequence models, text generation, or any of it with the word "neural" beyond that one estimator.

It doesn't handle data loading, cleaning or plotting. Data arrives as arrays or DataFrames that pandas made. Results are plotted with matplotlib. Those are separate libraries on purpose. The boundary is clean. Scikit-learn takes numeric arrays and returns numeric arrays.

It also doesn't do statistical inference. A linear model gives you coeffs and no p-values, no trust intervals and no hypothesis tests. The library is built around guess rather than explanation. `statsmodels` is the library for that question. Reaching for it's the right answer rather than a workaround.

<strong>Is the API stable?</strong> Remarkably so. Code written against `fit`/`predict` a decade ago still runs. This Is unusual in this field and is a large part of why the library is worth learning properly.

## Things to try

1. <strong>Run the first editor.</strong> `hasattr(model, "coef_")` is False before `fit` and True after. That is the whole of what fitting does, visible in one line.
2. <strong>Change the data.</strong> Make the tie non-linear. `y = [1, 4, 9, 16, 25, 36]`. And watch `coef_` become a compromise rather than an exact fit.
3. <strong>Swap the model.</strong> In the fifth editor, add `from sklearn.svm import SVR` and put `SVR()` in the list. Nothing else changes.
4. <strong>Break the shape.</strong> In the last editor, read the error properly. It names the shape it got and the shape it wanted.

## Where this leaves you

Three method names, one shape rule and one naming rule cover the surface of the entire library. All from here is a choice of estimator and, far more importantly, whether the number it reports can be believed. """,
    [
        {"q": "What does a trailing underscore on an attribute mean?",
         "options": ["It is private",
                     "It was learned during fit",
                     "It is deprecated",
                     "It is a hyperparameter you set"],
         "answer": 1,
         "why": "Attributes like coef_ and classes_ do not exist until fit has run. Names without the underscore are settings you chose."},
        {"q": "What shape must X be?",
         "options": ["1-D, one entry per sample",
                     "2-D, samples as rows and features as columns",
                     "Whatever shape y is",
                     "2-D, features as rows"],
         "answer": 1,
         "why": "One row per sample, one column per feature - which is why a single feature still needs reshape(-1, 1)."},
        {"q": "What does a transformer have instead of predict?",
         "options": ["evaluate", "apply", "transform", "convert"],
         "answer": 2,
         "why": "Transformers produce new features rather than a target, and fit_transform does both steps in one call."},
        {"q": "Why does fit return the estimator?",
         "options": ["To report success",
                     "So that Model().fit(X, y) can be written on one line",
                     "It returns the predictions",
                     "It returns the score"],
         "answer": 1,
         "why": "Every fit returns self, which is what makes the constructor-and-fit one-liner work."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Loading and shaping data
# ---------------------------------------------------------------------------
topic(
    "loading_and_shaping_data",
    "Loading and Shaping Data",
    "The API",
    "Where practice data comes from, what shape the library insists on, and "
    "the two error messages you will meet before anything else works.",
    _svg(_grid(20, 24, 4, 4, 12, S) + _txt(44, 20, "X  (n, features)", M, 7) +
         _grid(84, 24, 1, 4, 12, S) + _txt(90, 20, "y", M, 7) +
         _txt(126, 44, "rows =", M, 7, "start") +
         _txt(126, 56, "samples", A, 7, "start")),
    [
        ("A dataset that ships with the library",
         "Seven small datasets come with scikit-learn, so nothing has to be "
         "downloaded before you can try something.",
         '''from sklearn.datasets import load_iris

data = load_iris()

print("X shape:", data.data.shape)
print("y shape:", data.target.shape)
print("features:", data.feature_names)
print("classes :", list(data.target_names))
print()
print("first row:", data.data[0], "-> class", data.target[0])
'''),

        ("Three ways to take the same data out",
         "The default gives you a Bunch, and two arguments give you the shapes "
         "you usually want instead.",
         '''from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
print("return_X_y gives arrays:", type(X).__name__, X.shape, y.shape)

df = load_iris(as_frame=True).frame
print()
print("as_frame gives a DataFrame:", df.shape)
print(df.head(3))
'''),

        ("Data you make up, with the properties you want",
         "The make_* functions generate data with a known structure, which is "
         "how you test an idea without hunting for a dataset.",
         '''from sklearn.datasets import make_classification, make_regression

Xc, yc = make_classification(n_samples=200, n_features=5, n_informative=3,
                             n_classes=2, random_state=0)
print("classification:", Xc.shape, "classes:", sorted(set(yc)))

Xr, yr = make_regression(n_samples=200, n_features=3, noise=10.0, random_state=0)
print("regression    :", Xr.shape, "y range: %.1f to %.1f" % (yr.min(), yr.max()))
'''),

        ("Your own data, arranged the way the library wants",
         "One row per sample, one column per feature - and the target separate.",
         '''import numpy as np

rows = [
    {"rooms": 2, "area": 55, "price": 180},
    {"rooms": 3, "area": 78, "price": 260},
    {"rooms": 4, "area": 96, "price": 310},
]

X = np.array([[r["rooms"], r["area"]] for r in rows])
y = np.array([r["price"] for r in rows])

print("X:", X.shape)
print(X)
print("y:", y.shape, y)
'''),

        ("X and y must agree on the number of rows",
         "The second error message everyone meets, and it counts both for you.",
         '''from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3]])
y = np.array([10, 20])          # one short

try:
    LinearRegression().fit(X, y)
except ValueError as e:
    print("ValueError:", e)
'''),

        ("A Bunch is a dictionary with attribute access",
         "Which is why you will see both bunch.data and bunch['data'] in "
         "examples, meaning the same thing.",
         '''from sklearn.datasets import load_wine

bunch = load_wine()
print("a Bunch is a dict you can also use with dots")
print("keys:", sorted(k for k in bunch.keys() if k != "DESCR"))
print()
print("bunch.data is bunch['data']:", bunch.data is bunch["data"])
print("samples per class:", [int((bunch.target == c).sum()) for c in range(3)])
'''),
    ],
    [
        "<code class='mono-font'>X</code> is 2-D - rows are samples, columns "
        "are features. <code class='mono-font'>y</code> is 1-D, one entry per "
        "row of X.",
        "<code class='mono-font'>load_*</code> functions ship data with the "
        "library; <code class='mono-font'>fetch_*</code> download it; "
        "<code class='mono-font'>make_*</code> generate it.",
        "<code class='mono-font'>return_X_y=True</code> skips the Bunch and "
        "hands back the two arrays directly.",
        "<code class='mono-font'>as_frame=True</code> gives a DataFrame with "
        "the feature names attached, which is what keeps names alive through a "
        "pipeline.",
        "\"Expected 2D array, got 1D array instead\" means a single feature "
        "needs <code class='mono-font'>reshape(-1, 1)</code>.",
        "\"Found input variables with inconsistent numbers of samples\" means "
        "X and y have different row counts - the message prints both.",
    ],
    """title: Loading and Shaping Data: A Practical Guide
intro: Before any model can be fitted, the data has to be two objects of just the right shape. Almost each first error on this track is one of the two this page ends with.

## The shape the library insists on

Before you can fit any model, the data must be in the shape scikit-learn expects. That shape is rigid and the library will not guess when it is wrong. Understanding the rules up front saves time that would otherwise go to debugging shape errors.

Every estimator in the library receives its data the same way. A features matrix and a target vector. The features matrix is always two-dimensional. The target vector is always one-dimensional. These constraints hold whether you have five rows or five million.

The data can come from a CSV, a database, a pandas DataFrame or one of the bundled toy datasets. The source does not matter. What matters is the final array shape that reaches `fit`. Getting it right is mechanical once you know the two rules.

scikit-learn takes two things: a two-dimensional `X` and a one-dimensional `y`.

`X` has one row per sample and one column per feature. If you've 150 flowers and four readings of each, `X.shape` is `(150, 4)`. The rule is universal across the library. It's the reason a table of data maps onto it so right. Rows are readings, columns are variables. This Is how a spreadsheet is already arranged.

`y` has one entry per row of `X`. For a regression it holds numbers. For a classification it holds labels. This May be ints or strings. `y.shape` is `(150,)`. Note the trailing comma. This Is what a one-dimensional shape looks like in NumPy.

The library won't guess when the shapes are wrong. That refusal is worth appreciating rather than resenting. A list of six numbers could be six samples of one feature or one sample of six features. Those are fully different problems. Rather than pick one, scikit-learn raises and tells you what it received.

## Where practice data comes from

Three families of function, distinguished by their prefix.

`load_*` returns a small dataset that ships inside the installed package. `load_iris`, `load_wine`, `load_digits`, `load_diabetes`, `load_breast_cancer` and a couple more. They're tiny, they need no network. They're what almost each example in the docs uses. Their size is the point. A model fits in milliseconds. You can try a thing and see the result right away.

`fetch_*` downloads a larger, more realistic dataset the first time and caches it. `fetch_california_housing`, `fetch_20newsgroups`, `fetch_openml` for any of it on OpenML. These are the ones to use when the toy datasets stop being lifelike. But they need a network. This Is why this track stays with the bundled ones.

`make_*` makes data with the structure you asked for. `make_classification`, `make_regression`, `make_blobs`, `make_moons`. These are the most underrated of the three. They let you make just the situation you want to study. A dataset with two helpful features and eight useless ones, or classes that are on purpose not linearly separable, or a regression with a known amount of noise. When you're testing whether a technique does what you think, made data with known properties beats real data whose properties you're guessing at.

## The Bunch, and the two ways past it

The `load_*` and `fetch_*` functions return a `Bunch`. This Is a dict that also allows field access. `data.target` and `data["target"]` are the same object. This Is why examples use both spellings alike.

A Bunch carries more than the arrays. `feature_names` gives the column names, `target_names` maps the int labels back to a thing readable. `DESCR` holds a full description of the dataset. Where it came from, what each column means. How many samples there are. Printing `DESCR` is the fastest way to understand an unseen bundled dataset, and it's routinely skipped.

`return_X_y=True` skips the Bunch and returns the two arrays as a tuple. This Is what you want when you already know the dataset and just need the data. It makes the common line short: `X, y = load_iris(return_X_y=True)`.

`as_frame=True` returns pandas objects instead of NumPy arrays: `data.frame` is a DataFrame with the target as a column. `data.data` turns a DataFrame with named columns. This matters more than it first appears. A DataFrame carries its column names into the estimator. This Is what lets a fitted model report `feature_names_in_` and what lets a `ColumnTransformer` select columns by name rather than by spot.

## Turning your own data into X and y

Real data rarely arrives in the right shape, and the conversion is often one comprehension.

From a list of dicts, build `X` by pulling the feature keys in a fixed order and `y` by pulling the target key. The order matters and must be the same for each row. This Is just what a list comprehension ensures and a hand-written loop doesn't.

From a pandas DataFrame it's shorter still: `X = df[["rooms", "area"]]` and `y = df["price"]`. Selecting with a list of column names gives a DataFrame. This Is 2-D and so a valid `X`. Selecting with a single name gives a Series. This Is 1-D and so a valid `y`. Getting those two confused. `df["rooms"]` where `df[["rooms"]]` was meant. Makes the 1-D error message. The doubled brackets are the fix.

The one rule that lives each source: decide the column order once. Keep it. A model fitted on columns in one order and given new data in another won't complain. It will give confident nonsense. Column three is column three what it used to mean.

## The two errors, and what they are telling you

**"Expected 2D array, got 1D array instead."** You passed a thing with one dim where `X` was wanted. The message goes on to suggest `reshape(-1, 1)` if the data has a single feature and `reshape(1, -1)` if it's a single sample. Choosing between those two is choosing what your data means. `-1` tells NumPy to work that dim out from the length.

**"Found input variables with inconsistent numbers of samples: [3, 2]."** `X` and `y` disagree about how many rows there are. The numbers in brackets are the two counts in order. This one almost always means an upstream filter was applied to one and not the other. Dropping rows with missing targets from `y` but not from `X`, say. And the fix belongs there rather than at the call that raised.

Both messages name the shapes involved. This Makes them among the more helpful errors you'll meet. Reading them before changing any of it's faster than guessing. The shape they report is often enough on its own to spot which of the two objects is wrong.

## Sparse matrices, and when one appears

Some transformers don't return a normal array. `OneHotEncoder` and the text vectorisers return a **sparse mat**. This Stores only the non-zero entries and their spots.

The reason is size. One-hot encoding a column with ten thousand distinct values makes ten thousand columns, almost all of them zero on any given row. Stored densely that is huge and almost fully wasted. Stored sparsely it's a list of the few spots that aren't zero.

You'll notice it in three ways. Printing one shows a summary rather than the numbers. Indexing behaves differently from a NumPy array. And some estimators accept it happily while others raise. Not each method can be written to work on that form.

`.toarray()` converts to a dense array. Is the right move only when you're certain the result fits in memory. Which is just the case the sparse form existed to avoid. `sparse_output=False` on the encoder is the better fix when the number of columns is truly small. Most of the time the correct answer is to leave it sparse. The estimators that matter for high-dimensional data all handle it.

## Looking at the data before fitting anything

The step that gets skipped, and the one that catches the problems a model will silently absorb.

Four questions are worth answering before any `fit`. **How many rows and columns**, from `X.shape`. A model with more features than samples behaves quite differently from one with the reverse. **What range each feature covers**. A column measured in millions next to one measured in fractions is the situation that makes scaling needed. **Whether any of it's missing**. `np.isnan(X).sum()` costs nothing and most estimators refuse to fit with `NaN` present. And **how the target is spread**. For a classifier, the count per class, because that single number decides whether fit is a real metric at all.

None of these need plotting or a lengthy exploration. Four lines before the first `fit` catch the majority of problems that would or else appear later as an inexplicable score.

The one that matters most is the class balance. A dataset that is 99% one class will let almost any classifier report 99% fit. A reader who hasn't counted will believe it.

## Feature names, and why they are worth keeping

Passing NumPy arrays works, and passing DataFrames gives you a thing arrays can't: the model remembers what the columns were called.

A fitted estimator that was given a DataFrame gains `feature_names_in_`. A few report results against those names rather than against spots. `feature_importances_` on a tree, `coef_` on a linear model. The output of `get_feature_names_out()` on a transformer are all far easier to read when there's a name attached to each number.

It also adds a safety check. Fit on a DataFrame and then predict on one whose columns are in a different order. Scikit-learn raises rather than silently using the wrong column. Which is the failure mode that arrays can't protect you from at all.

The cost is that a DataFrame is slower than an array and that some ops convert back to arrays anyway, losing the names partway through a pipeline. That is why `get_feature_names_out()` exists on transformers. It rebuilds the names on the other side of a step that dropped them, including the invented names that one-hot encoding makes.

The habit worth adopting: use DataFrames at the boundary where data enters. Stop worrying about whether the middle of the pipeline is arrays or frames.

<strong>Should I use the bundled datasets for any of it real?</strong> No. They're for learning the mechanics. Iris in given is small, clean and nearly separable. This Makes almost each method look good on it.

<strong>Can I pass a Python list instead of an array?</strong> Yes, for X and y both - scikit-learn converts them. Arrays and DataFrames are preferable because they carry a dtype and, for frames, the column names.

## Things to try

1. <strong>Print the description.</strong> Add `print(load_iris().DESCR[:800])` to the first editor. It shows the columns, the classes and where the data came from.
2. <strong>Change the made data.</strong> In the third editor, set `n_informative=1` and see that four of the five features are noise by build. handy when testing whether a model can skip them.
3. <strong>Trigger the shape error on purpose.</strong> Pass `data.data[0]` as `X` and read what it suggests. One sample needs `reshape(1, -1)`, not `reshape(-1, 1)`.
4. <strong>Compare the two forms.</strong> Fit any of it on `as_frame=True` data, then check `model.feature_names_in_`. With plain arrays that field doesn't exist.

## Where this leaves you

Two objects, two shapes, and three prefixes for finding data to practise on. The next module takes that data and does the one thing that has to happen before any score means any of it: splitting it.
""",
    [
        {"q": "What shape must X have?",
         "options": ["1-D, one entry per sample",
                     "2-D, samples as rows and features as columns",
                     "2-D, features as rows and samples as columns",
                     "Any shape - scikit-learn infers it"],
         "answer": 1,
         "why": "Rows are samples and columns are features, which is why a single feature still needs reshape(-1, 1)."},
        {"q": "What does return_X_y=True change?",
         "options": ["It shuffles the data",
                     "It returns the two arrays directly instead of a Bunch",
                     "It splits into train and test",
                     "It returns a DataFrame"],
         "answer": 1,
         "why": "It skips the Bunch wrapper, which is what makes `X, y = load_iris(return_X_y=True)` a one-liner."},
        {"q": "Which prefix generates synthetic data with properties you choose?",
         "options": ["load_", "fetch_", "make_", "build_"],
         "answer": 2,
         "why": "make_classification, make_regression and make_blobs construct data with a known structure, which is ideal for testing whether a technique behaves as expected."},
        {"q": "\"Found input variables with inconsistent numbers of samples\" means what?",
         "options": ["X is 1-D",
                     "X and y have different numbers of rows",
                     "There are missing values",
                     "The features are on different scales"],
         "answer": 1,
         "why": "The numbers in the brackets are the two row counts. It usually means a filter was applied to one of the two and not the other."},
    ],
)


# ---------------------------------------------------------------------------
# 3. train_test_split
# ---------------------------------------------------------------------------
topic(
    "train_test_split",
    "Splitting Train and Test",
    "Honest Numbers",
    "The one line that separates a score you can report from a number that "
    "means nothing at all.",
    _svg(_box(14, 30, 84, 30, S, A) + _txt(56, 49, "train  80%", A, 9) +
         _box(102, 30, 44, 30, S, M) + _txt(124, 49, "test 20%", M, 8) +
         _txt(80, 22, "split once, before anything else", M, 7)),
    [
        ("The split, and the order of the four returns",
         "One call, four objects, and an order that catches everyone the first "
         "time.",
         '''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

print("all      :", X.shape)
print("train    :", X_train.shape, "  (%d%%)" % (100 * len(X_train) / len(X)))
print("test     :", X_test.shape, "   (%d%%)" % (100 * len(X_test) / len(X)))
print()
print("the four returns come back train, test, train, test - in that order")
'''),

        ("random_state makes the split reproducible",
         "Without it, every run is a different experiment and two scores cannot "
         "be compared.",
         '''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)

a = train_test_split(X, y, test_size=0.2, random_state=0)[1]
b = train_test_split(X, y, test_size=0.2, random_state=0)[1]
c = train_test_split(X, y, test_size=0.2, random_state=1)[1]

print("same seed, same split :", (a == b).all())
print("different seed        :", (a == c).all())
print()
print("without random_state you get a different split every run,")
print("so a score you cannot reproduce and cannot compare.")
'''),

        ("stratify keeps the class balance",
         "A random split can hand you a test set whose class proportions differ "
         "from the data it came from.",
         '''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)

def counts(v):
    return [int((v == c).sum()) for c in (0, 1, 2)]

_, _, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=3)
print("plain    - test class counts:", counts(y_te))

_, _, y_tr2, y_te2 = train_test_split(X, y, test_size=0.3, random_state=3,
                                      stratify=y)
print("stratify - test class counts:", counts(y_te2))
print()
print("full set :", counts(y))
'''),

        ("Why the training score is not a score",
         "The same model, measured twice. Only one of the two numbers is "
         "evidence of anything.",
         '''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0)

tree = DecisionTreeClassifier(random_state=0).fit(X_train, y_train)

print("score on the training data:", round(tree.score(X_train, y_train), 3))
print("score on the held-out test:", round(tree.score(X_test, y_test), 3))
print()
print("the first number is not a measure of anything - the model has")
print("seen every one of those rows already.")
'''),

        ("test_size takes a fraction or a count",
         "A float is a proportion, an integer is a number of rows.",
         '''from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

X, y = load_iris(return_X_y=True)

for size in (0.1, 0.2, 0.5):
    X_tr, X_te, _, _ = train_test_split(X, y, test_size=size, random_state=0)
    print("test_size=%.1f -> train %3d, test %3d" % (size, len(X_tr), len(X_te)))

print()
X_tr, X_te, _, _ = train_test_split(X, y, train_size=100, random_state=0)
print("an integer means a count, not a fraction:", len(X_tr), len(X_te))
'''),

        ("Time series must not be shuffled",
         "Shuffling puts future rows in the training set, which is a way of "
         "scoring well and learning nothing.",
         '''from sklearn.model_selection import train_test_split
import numpy as np

# A time series: the order is the meaning.
X = np.arange(10).reshape(-1, 1)
y = np.arange(10)

_, X_te, _, _ = train_test_split(X, y, test_size=0.3, random_state=0)
print("shuffled test rows :", sorted(X_te.ravel()))

_, X_te2, _, _ = train_test_split(X, y, test_size=0.3, shuffle=False)
print("shuffle=False      :", list(X_te2.ravel()))
print()
print("with time, testing on rows that came before the training rows")
print("is predicting the past from the future.")
'''),
    ],
    [
        "The four returns are <strong>X_train, X_test, y_train, y_test</strong> "
        "- both X pieces before either y piece.",
        "<code class='mono-font'>random_state</code> makes the split "
        "reproducible; without it two runs are two different experiments.",
        "<code class='mono-font'>stratify=y</code> keeps each class in the same "
        "proportion in both halves, and matters most when a class is rare.",
        "A score measured on the training data is not a score - the model has "
        "already seen every one of those rows.",
        "<code class='mono-font'>test_size</code> takes a fraction as a float "
        "or a row count as an integer.",
        "<code class='mono-font'>shuffle=False</code> for anything ordered in "
        "time, or the model is trained on the future.",
    ],
    """title: Splitting Train and Test: A Practical Guide
intro: A model's score on the data it learned from tells you how well it stored, not how well it works. The split is what turns one into the other.

## The problem it solves

Every machine-learning model needs to be tested on data it has not seen during training. Without that separation, you cannot tell whether the model has learned a real pattern or simply memorised the answers.

`train_test_split` is the function that creates that separation. It takes your features and targets, shuffles the rows, and returns four arrays: training features, test features, training targets, test targets. One function call replaces several lines of index slicing.

The split must happen before any preprocessing. Scaling, encoding or imputing on the full dataset and then splitting leaks information from the test rows into the training set. That leak inflates the score and hides the true error rate. The order matters more than the split ratio.

This page covers the call itself, the parameters that control the split, and the situations where a random split is not enough. Time-ordered data, grouped observations and stratified sampling each need a different approach. Knowing when the simple split applies and when it does not is half the value.

A model that has seen a row can copy its answer. That isn't a find about the model. It's a property of having been shown the answer.

So a score found on the training data measures memorisation. Some models store just right. An unconstrained choice tree will score 1.0 on its training set each time. It can keep splitting until each sample sits in its own leaf. Report that number and you're reporting the model's room to store data. This Isn't what anyone wants to know.

The question worth answering is what happens on data the model has never seen. That is the only situation it will ever face in use. Holding some rows back and never letting the model touch them is the simplest honest way to find out.

## What the call does

`train_test_split` shuffles the rows and cuts them into two groups, returning four objects. The features and target for training, then the features and target for testing.

The return order is `X_train, X_test, y_train, y_test`. Both X pieces before either y piece. And getting it wrong is the single most common early mistake with this function. The failure isn't always loud. Swapping `X_test` and `y_train` makes a shape error. This Is fine. Swapping `y_train` and `y_test` makes a program that runs and reports a meaningless number.

Any number of arrays can be passed and they're all split the same way, on the same rows. This Is what keeps `X` and `y` aligned. That property is the whole reason to use the function rather than slicing by hand.

## random_state, and what reproducibility buys

The split is random, so without a seed each run makes a different one, and so a different score.

That matters more than it sounds. If you change a setting and the score moves from 0.94 to 0.96, you need to know whether the change did that or whether the split did. With a fixed seed, the split is held constant and the difference is attributable. Without one, you're checking two things that differ in two ways.

It also makes a bug reproducible. A model that fails on one split and not another is telling you a thing real. You can't investigate it if you can't get back to the split that failed.

Passing an int is enough. The exact value carries no meaning. `random_state=0` and `random_state=42` are equally any. And the only thing that matters is that it stays the same across the runs you intend to compare.

There's one honest use for leaving it out. Measuring how much the score varies between splits. This Is a real question and one that a single fixed split can't answer. The proper tool for that is cross-validation. This Repeats the exercise systematically rather than leaning on you to run it a few times.

## stratify, and the split that misrepresents the data

A random split doesn't ensure the two halves look alike. On a dataset with three equal classes, a plain split can easily hand you a test set with 17 of one and 14 of another. On a dataset where one class is rare, it can hand you a test set holding none of it at all.

`stratify=y` fixes this by sampling within each class. Both halves carry the same proportions as the first. The cost is nothing. For classification it should be the default rather than an option you note on hard datasets.

Where it turns key is imbalance. With 1% positives and a 20% test set, an unstratified split has a real chance of putting so few positives in the test set that the metric found from them is noise. Stratifying ensures the proportion. This Is the min needed for the number to mean any of it.

You can stratify on a thing other than the target by passing a different array. A group label, say. Which is at times what you want when the target is smooth but some cat variable must stay weighed.

## The split has to come first

The order of ops matters, and getting it wrong is the most common way to give an inflated score.

All learned from data must be learned from the training set alone. That includes the obvious. The model. And the less obvious. The mean and standard deviation used for scaling, the categories known to an encoder, the median used to fill missing values, the vocab of a text vectoriser. The feature-pick choice about which columns to keep.

Scale the whole dataset and then split. The scaler has seen the test set. The test score afterwards isn't a score on unseen data. Info from those rows reached the model through the scaler's params. The effect is often small and at times huge, and it's always in the direction of making the model look better than it's.

The rule that follows is short: **split first. Fit each transformer on the training half only**. Pipelines exist largely to make that structurally hopeless to get wrong. This Is why they arrive later in this track and why they aren't optional in real work.

## How big should the test set be

The rule is 20% or 25%. The rule is a compromise between two things pulling in opposite directions.

A larger test set gives a more solid guess. The score is found from more samples and is less at the mercy of which given rows landed there. A smaller test set leaves more data for training. This Often makes a better model.

With a lot of data, the tension disappears: 1% of a million rows is ten thousand test samples. This Is plenty. With a few hundred rows, both halves are uncomfortable. The estimate is noisy and the model is starved. And that is just the situation where a single split should be replaced by cross-validation. This Uses each row for both purposes without ever training and testing on the same one.

The other consideration is the rarest class. A test set that holds four examples of a thing can only report fit on it in steps of 25%. No amount of careful metric choice recovers from that.

## Time changes the rules

When rows are sorted in time, shuffling is wrong.

Shuffling puts rows from after the test period into the training set. The model learns from the future and is then asked to predict the past. It will do well. The score will be worthless. The situation it was scored in can't occur in use. In production, the future is just what you don't have.

`shuffle=False` keeps the order and takes the last portion as the test set. This Is the right shape. Train on the past, test on the more recent. Note that `stratify` can't be used with `shuffle=False`. The two are conceptually incompatible anyway.

For any of it more careful, `TimeSeriesSplit` gives the cross-validation equal. A series of splits, each training on all up to a point and testing on what comes next. The same thinking applies to any structure with groups that must not be broken across the split. A few rows per patient, per user, per doc. Where `GroupShuffleSplit` keeps a group fully on one side.

## What the test set is for, and what it is not

A held-out set answers one question: how does this model behave on data it hasn't seen. It stops answering that question the moment you use it to make a choice.

This is the part that gets lost. If you fit five models, look at the test score for each. Pick the best, you've used the test set to choose a model. And the winner's score is now optimistic. It was selected for doing well on those given rows. Do it a dozen times, tweaking as you go. The test set has been fitted to as surely as if you had trained on it, just more slowly and by hand.

The standard remedy is three sets rather than two. **Train** to fit the model, **validation** to compare models and tune settings. **test** touched just once at the very end to report a number. the validation half is often replaced by cross-validation on the training data. This Uses the data better. The test set is still set aside and left alone.

The discipline is easier to state than to keep. Each look at the test set costs a little of its honesty. Nested cross-validation exists for the situation where you can't afford even that. Is the correct answer when the difference between two models is small enough to matter.

## Splits that respect structure

A plain random split assumes rows are free, and often they aren't.

**a few rows per entity.** Ten readings from the same patient, a few photos of the same object, multiple purchases by one customer. A random split puts some of an entity's rows in training and others in test. The model can recognise the entity rather than learn the pattern. The score is inflated by an amount nothing in the output reveals. `GroupShuffleSplit` and `GroupKFold` take a `groups` array and keep each group whole.

**Time.** Covered above, and worth repeating because it's so easy to get wrong: `shuffle=False`, or `TimeSeriesSplit`.

**Nested or hierarchical data.** Pupils within schools, readings within sites. The same thinking as groups. If the model can spot the container, it will.

The question to ask before splitting is simply. Could two rows on opposite sides of the split share a thing that would let the model cheat? If the answer is yes, a plain random split will overstate the score, and the amount is unpredictable.

<strong>Is 80/20 a rule?</strong> It's a rule that suits a few thousand rows. With a million, 1% is a fine test set. With two hundred, a single split is the wrong tool and cross-validation is the right one.

<strong>Should the test set be split off before cleaning?</strong> Before any of it that <em>learns</em> from the data, yes. Dropping obviously corrupt rows is fine either way. Imputing a median isn't.

## Things to try

1. <strong>Run the fourth editor.</strong> The training score is 1.0 and the test score isn't. That gap is the entire reason this page exists.
2. <strong>Drop random_state.</strong> Run the same editor three times and watch the test score move. Then put it back.
3. <strong>Make a class rare.</strong> Keep only ten samples of class 2, split without `stratify`. Count the classes in the test set a few times with different seeds.
4. <strong>Break the order.</strong> In the last editor, compare the shuffled and unshuffled test rows. The shuffled set holds rows from the beginning of the series.

## Where this leaves you

One line, four objects, and three args worth setting on purpose each time: `random_state` so the test is repeatable, `stratify` so the halves resemble each other, and `shuffle=False` when the rows are sorted in time. What it gives you is a number you're entitled to report.
""",
    [
        {"q": "What order does train_test_split return its four objects in?",
         "options": ["X_train, y_train, X_test, y_test",
                     "X_train, X_test, y_train, y_test",
                     "train, test, X, y",
                     "y_train, y_test, X_train, X_test"],
         "answer": 1,
         "why": "Both X pieces come before either y piece. Getting this wrong can produce a program that runs and reports a meaningless number."},
        {"q": "Why pass random_state?",
         "options": ["It improves the score",
                     "It makes the split reproducible, so two runs are comparable",
                     "It stratifies the split",
                     "It is required"],
         "answer": 1,
         "why": "Without it every run is a different split and therefore a different experiment - you cannot tell whether a change or the split moved the score."},
        {"q": "What does stratify=y do?",
         "options": ["Sorts the data by class",
                     "Keeps each class in the same proportion in both halves",
                     "Removes rare classes",
                     "Balances the classes by resampling"],
         "answer": 1,
         "why": "It samples within each class. It matters most when a class is rare, where a plain split can leave almost none of it in the test set."},
        {"q": "Why must scaling happen after the split?",
         "options": ["It is faster that way",
                     "Otherwise the scaler learns from the test rows and the test score is no longer honest",
                     "Scalers cannot handle the full dataset",
                     "It does not matter"],
         "answer": 1,
         "why": "Anything fitted on the whole dataset has seen the test set. Information reaches the model through the transformer's parameters, and the score comes out too high."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Linear regression
# ---------------------------------------------------------------------------
topic(
    "linear_regression",
    "Linear Regression",
    "Regression",
    "The simplest useful model, and the one whose fitted parameters you can "
    "actually read - with one caveat about reading them.",
    _svg(_box(16, 18, 128, 58, S, B) +
         _dots([(30, 66), (50, 58), (70, 47), (90, 40), (110, 30), (130, 24)]) +
         '<path d="M26 70 L136 22" stroke="var(--accent-primary)" '
         'stroke-width="2"/>' + _txt(80, 86, "y = a + b x", A, 8)),
    [
        ("Fitting a line, and reading it back",
         "Two learned numbers, and together they are the whole model.",
         '''from sklearn.linear_model import LinearRegression
import numpy as np

# price = 40 + 25 * rooms, with a little noise
rooms = np.array([[1], [2], [3], [4], [5], [6]])
price = np.array([66, 89, 115, 140, 168, 190])

model = LinearRegression().fit(rooms, price)

print("slope     (coef_)     : %.2f" % model.coef_[0])
print("intercept (intercept_): %.2f" % model.intercept_)
print()
print("so the line it found is: price = %.1f + %.1f * rooms"
      % (model.intercept_, model.coef_[0]))
'''),

        ("More features, more coefficients",
         "One coefficient per column, in the same order as the columns.",
         '''from sklearn.linear_model import LinearRegression
import numpy as np

# two features now: rooms and area
X = np.array([[1, 40], [2, 55], [3, 75], [4, 90], [5, 110], [6, 130]])
y = np.array([66, 89, 115, 140, 168, 190])

model = LinearRegression().fit(X, y)

for name, c in zip(["rooms", "area"], model.coef_):
    print("%-6s coefficient: %8.3f" % (name, c))
print("intercept        : %8.3f" % model.intercept_)
print()
print("one coefficient per column of X, in the same order")
'''),

        ("Predictions and residuals",
         "What the model says, what the data said, and the gap - which is the "
         "thing the fit was minimising.",
         '''from sklearn.linear_model import LinearRegression
import numpy as np

rooms = np.array([[1], [2], [3], [4], [5], [6]])
price = np.array([66, 89, 115, 140, 168, 190])

model = LinearRegression().fit(rooms, price)
pred = model.predict(rooms)

print(" rooms  actual  predicted  residual")
for r, a, p in zip(rooms.ravel(), price, pred):
    print("%6d %7d %10.1f %9.1f" % (r, a, p, a - p))
print()
print("residuals sum to about zero: %.10f" % (price - pred).sum())
'''),

        ("score() on a regressor is R-squared",
         "And it is worth computing once by hand, because the definition "
         "explains what a negative value would mean.",
         '''from sklearn.linear_model import LinearRegression
import numpy as np

rooms = np.array([[1], [2], [3], [4], [5], [6]])
price = np.array([66, 89, 115, 140, 168, 190])
model = LinearRegression().fit(rooms, price)

print("score() on a regressor is R-squared:", round(model.score(rooms, price), 4))

# R-squared compares the model against always predicting the mean.
mean_only = np.full_like(price, price.mean(), dtype=float)
ss_res = ((price - model.predict(rooms)) ** 2).sum()
ss_tot = ((price - mean_only) ** 2).sum()
print("computed by hand              :", round(1 - ss_res / ss_tot, 4))
'''),

        ("A big coefficient does not mean an important feature",
         "The same model twice, with one feature's units changed. Watch the "
         "coefficient move and the fit stay identical.",
         '''from sklearn.linear_model import LinearRegression
import numpy as np

# Same information, different units: area in square metres, then in hectares.
X_m2 = np.array([[40.0], [55.0], [75.0], [90.0], [110.0], [130.0]])
y = np.array([66, 89, 115, 140, 168, 190])

X_ha = X_m2 / 10000.0

for label, X in [("area in m2", X_m2), ("area in hectares", X_ha)]:
    m = LinearRegression().fit(X, y)
    print("%-18s coef_ = %12.4f   R2 = %.4f" % (label, m.coef_[0], m.score(X, y)))

print()
print("identical model, coefficient 10000x apart - size means nothing")
print("until the features are on the same scale.")
'''),

        ("Linear in the coefficients, not in the data",
         "A straight line fits a curve badly, and the same linear model fits it "
         "exactly once you give it the right feature.",
         '''from sklearn.linear_model import LinearRegression
import numpy as np

x = np.arange(1, 11).reshape(-1, 1)
y = (x.ravel() ** 2).astype(float)      # a curve, not a line

lin = LinearRegression().fit(x, y)
print("straight line on a curve, R2 =", round(lin.score(x, y), 3))

# Give it x squared as a feature and the same linear model fits exactly.
X2 = np.hstack([x, x ** 2])
poly = LinearRegression().fit(X2, y)
print("with x**2 as a second feature, R2 =", round(poly.score(X2, y), 3))
print()
print("'linear' means linear in the coefficients, not in the data.")
'''),
    ],
    [
        "<code class='mono-font'>coef_</code> holds one number per feature, in "
        "column order; <code class='mono-font'>intercept_</code> is the value "
        "when every feature is zero.",
        "The fit minimises the sum of the squared residuals - which is why a "
        "single outlier moves the line further than several small errors.",
        "<code class='mono-font'>score()</code> returns R&sup2;: 1.0 is perfect, "
        "0.0 is no better than predicting the mean, and negative is worse than "
        "that.",
        "A coefficient's <em>size</em> depends on the feature's units, so it is "
        "not a measure of importance unless the features were scaled first.",
        "\"Linear\" describes the coefficients, not the data - add "
        "<code class='mono-font'>x**2</code> as a feature and a linear model "
        "fits a curve.",
        "With more features than samples, or perfectly correlated columns, the "
        "solution is not unique and the coefficients become unstable.",
    ],
    """title: Linear Regression: A Practical Guide
intro: The model whose params you can read, whose failures are visible. Whose coeffs are misread more often than any other number in the library.

## What it is fitting

Linear regression is the first model most people try. It is fast, interpretable and often good enough for problems where the relationship between features and target is roughly proportional.

The model assigns one coefficient to each feature. Each coefficient says how much the target changes when that feature increases by one unit, holding everything else constant. That directness is why linear regression remains popular even when fancier models score higher. You can read the fitted model and explain it to someone who has never heard of machine learning.

It also serves as a baseline. If a complex model barely beats a linear one, the extra complexity is probably not worth it. Running linear regression first gives you a floor to compare against.

Linear regression finds one number per feature, plus an intercept, such that adding them up predicts the target as closely as possible.

For one feature that is a straight line through a scatter of points. For three features it's a plane in four dims. This No one can picture and which behaves just the same way arithmetically. Times each feature by its coeff, add the intercept, and that is the guess.

"As closely as possible" has a precise meaning. It cuts the sum of the *squared* differences between guesses and actuals. Squaring is what makes the problem solvable in one step rather than by search. There's a formula. Scikit-learn uses it. And it's also why the model is sensitive to outliers. A residual of 10 adds a hundred times more than a residual of 1. One badly wrong point pulls the line further than a dozen slightly wrong ones.

## Reading the fitted model

`coef_` is an array with one entry per column of `X`, in the same order as the columns. `intercept_` is a single number: the guess when each feature is zero.

Together they're the entire model. There's nothing else stored, no data kept, no lookup table. Which is why a fitted linear regression is a few numbers even so of whether it was trained on a hundred rows or a hundred million.

That readability is the model's main hands-on edge. A coeff of 25.2 on `rooms` says. Holding the other features fixed, one more room is associated with 25.2 more units of price. The phrase "holding the other features fixed" is doing real work in that sentence and is the part people drop. A coeff isn't the effect of a feature on its own, it's the effect after the other features in the model have accounted for what they can.

The intercept is often meaningless in alone. A house with zero rooms and zero area doesn't exist. The intercept is where the line happens to cross rather than a guess anyone would make. It matters for the math and rarely for the reading.

## The coefficient trap

This is the most often repeated mistake about linear models. It's worth being blunt: **the size of a coeff tells you nothing about the importance of a feature.**

A coeff is expressed in units of target per unit of feature. Measure area in square metres and the coeff is some number. Measure the same area in hectares and the coeff is ten thousand times larger. The model is the same, the guesses are the same, the R&sup2; is the same. Only the units changed.

So checking coeffs across features only means a thing if the features are on the same scale. Standardising them first. Subtracting the mean and cutting by the standard deviation. Makes the coeffs close. They then answer "how much does the guess move per standard deviation of this feature". This Is a question worth asking.

Even then, "importance" is slippery. Two linked features share the credit between them in a way that depends on the noise. A feature can have a small coeff because a linked one absorbed the signal rather than because it doesn't matter. Permutation importance answers the question more honestly. This track's tree modules cover the options.

## R-squared, and what a negative value means

`score()` on a regressor returns R&sup2;. Its meaning is a check rather than an abs measure. How much of the variation in the target the model accounts for, scaled to a baseline that always predicts the mean.

1.0 means the guesses are exact. 0.0 means the model does just and always guessing the mean. Which is to say it has learned nothing handy. Values in between are the usual case.

A **minus** R&sup2; surprises people and is fully possible. It means the model is worse than predicting the mean. This Happens routinely on a test set when a model has overfitted. Always shows a thing is wrong rather than merely weak.

The number's weakness is that it's unitless and so not right real. An R&sup2; of 0.85 doesn't tell you whether the guesses are wrong by pounds or by thousands of pounds. That is often the question that matters. The next module covers the metrics that answer it.

## What "linear" actually restricts

The name misleads. Linear regression is linear in its *coeffs*, not in the data. The gap is what makes it far more flexible than it appears.

Adding `x**2` as an extra column lets a linear model fit a parabola just. Adding `x1 * x2` lets it capture an interplay between two features. Adding `log(x)` lets it fit a curve that flattens. In each case the model is still linear. It's still timesing each column by a coeff and adding. Because the non-linearity is in the *feature*, not in the fitting.

`PolynomialFeatures` automates this by making all the powers and products up to a degree you choose. It's truly handy and it grows quickly. Degree 3 on ten features makes 286 columns, most of them useless. The model will happily fit noise with them. Which is the standard trade this track keeps returning to.

## When it is the wrong model

Three situations where linear regression struggles, and knowing them saves fitting it and being puzzled.

**truly non-linear ties**, unless you make the features to capture them. A tree-based model finds them without being told what shape to look for. This Is why grad boosting is the usual default on tabular data.

**More features than samples.** The answer is no longer unique. Infinitely many coeff sets fit the training data just right. And plain linear regression has no principle for choosing between them. Ridge and Lasso add one. This Is just what smoothing is for.

**Highly linked features.** Two columns carrying almost the same info make the coeffs unstable. Small changes in the data give large swings in how the credit is cut. The single numbers stop being readable though the guesses remain fine.

For the second and third, `Ridge` is the drop-in swap and is a better default than plain `LinearRegression` for any of it with many features. It uses the same interface, adds one setting. Gives up a little training fit for coeffs that don't move around.

## Ridge and Lasso, in one paragraph each

Two variants solve the problems at the end of the previous section, and both are one-line swaps.

**Ridge** adds a fine proportional to the sum of the squared coeffs. The effect is to shrink them all towards zero, more so as `alpha` grows. This Stops any one of them growing large to chase noise. It handles linked features gracefully. Rather than one coeff swinging plus and another minus, both end up moderate and stable. `Ridge(alpha=1.0)` is a sensible default and a better starting point than plain `LinearRegression` when there are more than a handful of features.

**Lasso** punishes the sum of the *abs* coeffs instead. That change has a striking consequence. It drives some coeffs to just zero rather than merely small. So it selects features and fitting them. The fitted model names the columns it decided to skip. The cost is that among linked features it tends to pick one arbitrarily and zero the rest. This Makes the pick unstable even when the guesses are fine.

`ElasticNet` mixes the two fines for when you want both properties. All three take `alpha`, all three need the features scaled first. A fine on coeff size is meaningless when the coeffs are in incomparable units. And all three are tuned with the cross-validated search covered later in this track.

## The assumptions, and which ones matter in practice

Textbooks list four or five assumptions behind linear regression. For guess. This Is what this library is for, they matter less than the textbooks imply. It's worth knowing which is which.

**Linearity** is the one that truly matters. If the tie curves and you haven't given the model a curved feature, the guesses will be systematically wrong in a pattern. Too low at the ends and too high in the middle, or the reverse. Plotting residuals against guesses makes it obvious. A good fit shows a shapeless cloud. A missed curve shows an arc.

**Free errors** matters for time series and grouped data. Is the reason those need different splitting. Nothing about the fit detects it.

**Constant error variance** and **most times spread errors** are assumptions of the *inference*. The p-values and trust intervals that scikit-learn doesn't find. If you only want guesses, violating them costs you fit in some regions rather than validity. If you want to make a claim about whether a coeff is much different from zero, you want `statsmodels`, and then they matter.

The hands-on version: look at the residuals for a pattern. A pattern means a missing feature or the wrong shape of model. No amount of smoothing fixes either.

<strong>Should I use LinearRegression or Ridge by default?</strong> Ridge, for any of it with more than a few features. It costs one setting and drops the instability that plain least squares has when columns are linked.

<strong>Does it need scaled features?</strong> Plain linear regression doesn't - the fit is the same either way. Ridge, Lasso and ElasticNet do. Their fine is on coeff size.

<strong>Why does fitting take no iterations?</strong> plain least squares has a closed-form answer. The answer is found right rather than searched for. That is why there's no `max_iter` and no settling warning on this estimator.

<strong>What is `plus=True` for?</strong> It constrains each coeff to be non-minus. This Is at times what physics or accounting needs - mixing proportions, say. Here A minus part is meaningless.

<strong>Can it handle missing values?</strong> No. It raises on `NaN`. This Is why imputation comes earlier in a pipeline than the model does.

## Things to try

1. <strong>Add an outlier.</strong> In the first editor, change one price to 400 and watch the slope move. Squared errors mean one bad point has a large vote.
2. <strong>Read the units.</strong> The fifth editor makes the coeff trap concrete. Fit both, then look at the R&sup2; column and note it doesn't move.
3. <strong>Fit the curve.</strong> In the last editor, try degree three by adding `x ** 3` as a third column and check whether R&sup2; raises on data that is truly quadratic.
4. <strong>Break it on purpose.</strong> Give the model two the same columns and look at the two coeffs. The sum is stable. The split between them isn't.

## Where this leaves you

Two learned arrays, one formula, and a score that checks the model against guessing the mean. The coeffs are readable. This Is the model's great edge, and readable in a way that needs care about units before any of them can be checked.
""",
    [
        {"q": "What does coef_ contain?",
         "options": ["The predictions",
                     "One coefficient per feature, in column order",
                     "The residuals",
                     "The R-squared value"],
         "answer": 1,
         "why": "One number per column of X, in the same order as the columns, plus intercept_ as a single separate number."},
        {"q": "A feature's coefficient is ten times larger than another's. What does that tell you?",
         "options": ["It is ten times more important",
                     "Nothing, until you know the features are on the same scale",
                     "The model is overfitting",
                     "That feature should be removed"],
         "answer": 1,
         "why": "A coefficient is in units of target per unit of feature. Change the feature's units and the coefficient changes while the model stays identical."},
        {"q": "What does a negative R-squared mean?",
         "options": ["An error in the calculation",
                     "The model is worse than always predicting the mean",
                     "The correlation is negative",
                     "R-squared cannot be negative"],
         "answer": 1,
         "why": "R-squared compares the model against the mean baseline. Below zero means the baseline would have done better, which is common on a test set after overfitting."},
        {"q": "Can a linear model fit a curved relationship?",
         "options": ["No, never",
                     "Yes, if you give it a curved feature such as x**2",
                     "Only with a different solver",
                     "Only in one dimension"],
         "answer": 1,
         "why": "\"Linear\" refers to the coefficients. Adding x**2 as a column lets the same model fit a parabola exactly."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Regression metrics
# ---------------------------------------------------------------------------
topic(
    "regression_metrics",
    "Regression Metrics",
    "Regression",
    "Four numbers that answer different questions, and the one property that "
    "decides which of them you should be reporting.",
    _svg(_box(14, 20, 60, 26, S, A) + _txt(44, 37, "MAE", A, 9) +
         _box(86, 20, 60, 26, S, M) + _txt(116, 37, "RMSE", M, 9) +
         _box(14, 54, 60, 26, S, M) + _txt(44, 71, "R2", M, 9) +
         _box(86, 54, 60, 26, S, M) + _txt(116, 71, "MAPE", M, 9)),
    [
        ("The four, on the same predictions",
         "Same errors, four summaries of them - and they do not rank models "
         "identically.",
         '''from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                             r2_score)
import numpy as np

y_true = np.array([100, 120, 140, 160, 180])
y_pred = np.array([110, 115, 145, 150, 185])

mse = mean_squared_error(y_true, y_pred)
print("MAE :", round(mean_absolute_error(y_true, y_pred), 2))
print("MSE :", round(mse, 2))
print("RMSE:", round(np.sqrt(mse), 2))
print("R2  :", round(r2_score(y_true, y_pred), 4))
'''),

        ("MAE and RMSE disagree about big mistakes",
         "Two sets of predictions wrong by the same total amount, and only one "
         "metric notices the difference.",
         '''from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

y_true = np.array([100, 120, 140, 160, 180])

# Both predictions are wrong by 75 in total, spread differently.
spread  = np.array([115, 135, 155, 175, 195])     # 15 out, five times
one_bad = np.array([100, 120, 140, 160, 105])     # 75 out, once

for label, pred in [("15 out, five times", spread), ("75 out, once", one_bad)]:
    err = np.abs(y_true - pred)
    mae = mean_absolute_error(y_true, pred)
    rmse = np.sqrt(mean_squared_error(y_true, pred))
    print("%-20s total error %3d   MAE %5.2f   RMSE %5.2f"
          % (label, err.sum(), mae, rmse))
'''),

        ("MAE is in the units of the target",
         "Which is what makes it the number to put in front of somebody who "
         "has to decide whether the model is good enough.",
         '''from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

y_true = np.array([100000, 120000, 140000])
y_pred = np.array([104000, 117000, 149000])

mae = mean_absolute_error(y_true, y_pred)
print("R2 :", round(r2_score(y_true, y_pred), 3), "- unitless")
print("MAE:", round(mae, 1), "- pounds, the same units as the target")
print()
print("only one of those answers 'is being wrong by this much acceptable?'")
'''),

        ("MAPE, and the division it cannot survive",
         "A percentage error is easy to explain and undefined the moment a true "
         "value is zero.",
         '''from sklearn.metrics import mean_absolute_percentage_error
import numpy as np

y_true = np.array([100.0, 200.0, 400.0])
y_pred = np.array([110.0, 210.0, 410.0])
print("all 10 out, MAPE =", round(mean_absolute_percentage_error(y_true, y_pred), 4))
print("  the same absolute error is a bigger share of a small number")
print()
with_zero = np.array([0.0, 200.0, 400.0])
print("with a zero in y_true, MAPE =",
      mean_absolute_percentage_error(with_zero, y_pred))
print("  not an error, just a meaningless number - check for zeros yourself")
'''),

        ("Compare against the laziest possible model",
         "A score means nothing until you know what doing nothing would have "
         "scored.",
         '''from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

X, y = make_regression(n_samples=200, n_features=4, noise=25.0, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

dummy = DummyRegressor(strategy="mean").fit(X_tr, y_tr)
model = LinearRegression().fit(X_tr, y_tr)

print("always predict the mean, R2 :", round(dummy.score(X_te, y_te), 4))
print("linear regression, R2       :", round(model.score(X_te, y_te), 4))
print()
print("the baseline is what 'good' has to beat.")
'''),

        ("Naming a metric for the cross-validation helpers",
         "And the reason half of them are spelled with a neg_ prefix.",
         '''from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import numpy as np

X, y = make_regression(n_samples=200, n_features=4, noise=25.0, random_state=0)
model = LinearRegression()

r2 = cross_val_score(model, X, y, cv=5, scoring="r2")
mae = cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error")

print("r2                     :", np.round(r2, 3))
print("neg_mean_absolute_error:", np.round(mae, 1))
print()
print("the 'neg_' prefix exists because these helpers always maximise,")
print("so an error metric is negated to make bigger mean better.")
'''),
    ],
    [
        "<strong>MAE</strong> is the average absolute error, in the target's "
        "own units - the one to quote to a person.",
        "<strong>RMSE</strong> squares before averaging, so it punishes a few "
        "large errors far more than many small ones.",
        "<strong>R&sup2;</strong> is unitless and compares the model against "
        "predicting the mean; it says nothing about whether the error is "
        "tolerable.",
        "<strong>MAPE</strong> is a percentage, which is easy to explain and "
        "undefined when any true value is zero.",
        "Always compare against <code class='mono-font'>DummyRegressor</code> - "
        "a score with no baseline is not interpretable.",
        "In <code class='mono-font'>scoring=</code> strings, error metrics carry "
        "a <code class='mono-font'>neg_</code> prefix because the helpers "
        "maximise.",
    ],
    """title: Regression Metrics: A Practical Guide
intro: R-squared is the default and rarely the right answer. Choosing the metric is choosing which mistakes you care about.

## The metric is a statement about what matters

A regression model returns numbers. Judging those numbers requires a metric. The choice of metric is not a formality. Different metrics reward different behaviour, and a model that looks good on one can look poor on another.

scikit-learn ships with a dozen regression metrics. Each one condenses the list of residuals into a single number. The residuals are the same in each case: predicted minus actual, for every row. What changes is how those residuals are combined.

Understanding the main three -- MAE, RMSE and R-squared -- is enough for most work. Each answers a slightly different question. MAE asks how far off the average guess is. RMSE asks the same thing but penalises large misses more heavily. R-squared asks how much better the model is than always guessing the mean.

Choosing the wrong metric does not break anything. It just gives you a number that does not match what you actually care about. A model tuned on RMSE will tolerate many small errors to avoid one large one. A model tuned on MAE will spread the errors more evenly. Neither is better in the abstract. The right choice depends on what a mistake costs in your application.

each regression metric summarises the same thing. The gaps between guesses and actuals. And they differ in how they weigh those gaps. That weighting isn't a technical detail. It's a claim about which errors are worse. The claim should come from the problem rather than from habit.

If being wrong by 10 twice is just as bad as being wrong by 20 once, you want MAE. If one large miss is disproportionately damaging, you want RMSE. If a 10% error on a small value matters as much as a 10% error on a large one, you want a percentage metric. These are different situations and they truly occur. This Is why the library ships a few dozen metrics rather than one.

## MAE: the average size of the mistake

Mean abs error is the mean of the abs differences. Nothing is squared. Each error adds in proportion to its size.

Its great virtue is that it's expressed in the units of the target. If you're predicting house prices in pounds, an MAE of 5,333 means the common guess is out by about five thousand pounds. That sentence can be said to somebody who has never heard of a regression. They can tell you whether it's acceptable.

That is a truly key property. Most of the value of a model is decided by a person who has to judge whether the errors are tolerable. They can't judge that from a unitless number. MAE is the default worth reaching for when the answer will be reported to anyone.

It's also solid: a single wild outlier moves it by its own size and no more.

## RMSE: the same idea, with big errors amplified

Root mean squared error squares each error, means. Takes the square root. The squaring is the whole difference.

Squaring makes a large error count for much more than a few small ones adding to the same total. The editors on this page show it just. Two sets of guesses wrong by 75 in total have the same MAE of 15. RMSE of 15.00 and 33.54 in turn. The second concentrated its error in one place, and RMSE says so.

Whether that is wanted depends fully on the use. For predicting delivery times, being an hour late once may be far worse than being twelve minutes late five times. The customer notices the hour. For predicting daily sales, the total is what matters and the distribution of errors isn't above all key.

The square root at the end puts the number back into the units of the target. RMSE is close to MAE in magnitude. RMSE is always at least as large as MAE. The gap between them tells you how unevenly the errors are spread. Equal means uniform, a wide gap means a few large misses.

MSE without the square root is the same ranking in squared units. This Are uninterpretable. It appears because it's what the fitting cuts and what differentiates cleanly, not because anyone should report it.

## R-squared: a comparison, not a measurement

R&sup2; asks how much of the variation in the target the model accounts for, checked against a model that always predicts the mean.

1.0 is perfect, 0.0 is no better than the mean. Minus means worse than the mean. Which is common on a test set and always a signal rather than a curiosity.

Two things make it common. It's unitless. It can be checked across problems with different targets. And it has a built-in baseline. So A value tells you a thing without a separate check run.

Two things make it dangerous. It says nothing about the size of the errors. An R&sup2; of 0.87 is compatible with being wrong by five pounds or five thousand. And it depends on the variance of the target in the test set. This Means the same model scores differently on two test sets drawn from the same data. A narrow test set makes the model look worse simply because the mean baseline is harder to beat.

Use it for checking models on the same data. Don't use it to decide whether a model is good enough for a purpose. Don't compare it across datasets.

## MAPE, and why it is both loved and distrusted

Mean abs percentage error expresses each error as a fraction of the true value and means those.

Its appeal is obvious: "we are often 6% out" is a sentence anyone understands. It's close across products, regions or scales in a way an abs number isn't.

Its problems are equally real. It's undefined when any true value is zero. Rather than raising, scikit-learn returns an huge number. The editor above shows 1.65e+17. Which will pass through an blending step and give nonsense no one notices. It's skewed. Over-predicting is penalised differently from under-predicting. This Biases model pick towards forecasting low. And it explodes for true values that are merely small rather than zero. A few near-zero rows can dominate the mean fully.

If percentages are what the audience wants, MAPE is usable on strictly plus data with no small values. Or else, quote MAE alongside the mean of the target and let the reader do the division.

## Always compare against doing nothing

`DummyRegressor` predicts the mean, or the median, or a constant you choose, skipping the features fully. Fitting one takes a line and it's the most valuable line in an test.

no metric is readable in alone. An R&sup2; of 0.4 could be an great result on a truly noisy problem or a terrible one on an easy problem. An MAE of 5,000 is meaningless without knowing that the mean baseline scores 12,000. Or 5,200, in which case the model has bought almost nothing for its cost.

That last case is more common than people expect. It never shows up unless the baseline is run. A model that beats the mean by 4% isn't always worth deploying, keeping and showing. The number that tells you so takes two lines to give.

## The neg_ prefix

`cross_val_score` and each search helper are written to raise. They assume bigger is better. That the same code can rank any metric without knowing which one it's.

Error metrics are the wrong way round for that. Smaller is better. Rather than special-case them, scikit-learn negates them: `neg_mean_absolute_error` returns -15 where MAE would return 15. Raising -15 towards zero is the same as cutting 15.

So the values come back minus and you flip the sign to read them. It's startling the first time. It's the reason `scoring="mean_absolute_error"` raises an error naming the valid options. `sorted(sklearn.metrics.get_scorer_names())` lists all of them. This Is faster than guessing the spelling.

## Errors that are not symmetric

All four metrics on this page treat over- and under-guess as equally bad. Often they aren't.

Under-predicting demand means empty shelves and lost sales. Over-predicting means stock that has to be written off. Under-guessing a journey time annoys a customer. Over-guessing loses the booking. Under-forecasting a load causes an outage. Over-forecasting costs money. In each one of those the two directions have different prices. A even metric will happily choose a model that is wrong in the costly direction.

Two ways to handle it. Write a custom scorer with `make_scorer`. This Takes a function of `(y_true, y_pred)` and a `greater_is_better` flag. Put the real cost in that function. If a unit of over-guess costs three times a unit of under-guess, say so arithmetically. Or use **quantile regression**, where the model is fitted to predict a chosen percentile rather than the mean. Fitting the 80th percentile gives guesses that are on purpose high most of the time. This Is what you want when running out is worse than having spare.

`GradientBoostingRegressor(loss="quantile", alpha=0.8)` does the second right. The skew then lives in the model rather than only in the report.

## Reading errors as a distribution

A single averaged number hides all about the shape of the errors. The shape is often where the info is.

Two habits repay the minute they cost. **Plot residuals against guesses.** A shapeless cloud means the model has extracted what it can. An arc means a missing non-linearity. A fan that widens to the right means the errors grow with the size of the target. This Often argues for predicting the logarithm instead.

**Look at the worst cases.** Sorting by abs error and reading the ten worst rows tells you more about a model than any summary statistic. often they've a thing in common. A category the training data barely covered, a period with an unusual event, rows with a missing field imputed to the median. And that commonality is a feature waiting to be added or a subset the model shouldn't be trusted on.

Neither of these appears in a metric, and both change what you do next.

<strong>Which metric should I optimise during training?</strong> often squared error. It's smooth and fast to fit. You can report a different one - fitting and reporting need not use the same metric, and often shouldn't.

<strong>Is RMSE always bigger than MAE?</strong> Yes, or equal when each error is the same size. The ratio between them measures how uneven the errors are.

<strong>How do I see each valid scoring name?</strong> `sorted(sklearn.metrics.get_scorer_names())`. This Is quicker than guessing at the spelling.

<strong>Should I report one metric or a few?</strong> a few. Always with the baseline beside them. MAE answers "how wrong, often", RMSE answers "are there occasional disasters". The dummy answers "checked to what". Any one of the three alone is easy to misread, and together they take one extra line to give.

<strong>My R-squared is high and the guesses look bad. How?</strong> Almost always a target with large variance. Here Beating the mean is easy and still leaves errors that matter in abs terms. Look at MAE next to the mean of the target.

## Things to try

1. <strong>Run the second editor.</strong> Same total error, same MAE, RMSE more than twice as large. That single check is the whole arg for choosing between them.
2. <strong>Add an outlier.</strong> In the first editor, change one guess to 400 and watch which metrics move most.
3. <strong>Beat the baseline by less.</strong> In the fifth editor, raise `noise` to 200 and see how much of the model's edge lives.
4. <strong>Get the spelling wrong.</strong> Ask for `scoring="mae"` and read the error - it lists each valid name.

## Where this leaves you

MAE for reporting to a person, RMSE when large errors are disproportionately costly, R&sup2; for checking models on the same data. A dummy baseline underneath all three. Which one you lead with is a choice about the problem, not about the model.
""",
    [
        {"q": "Which metric is expressed in the target's own units?",
         "options": ["R-squared", "MAE", "MAPE", "MSE"],
         "answer": 1,
         "why": "MAE is an average of absolute differences, so predicting pounds gives an MAE in pounds. RMSE is too, since the square root undoes the squaring."},
        {"q": "Two models have the same total absolute error. Which metric distinguishes them?",
         "options": ["MAE", "RMSE", "Neither", "MAPE"],
         "answer": 1,
         "why": "Squaring makes RMSE larger when the error is concentrated in a few large misses rather than spread evenly."},
        {"q": "What does a negative R-squared mean?",
         "options": ["A bug",
                     "The model is worse than always predicting the mean",
                     "The predictions are negative",
                     "It cannot be negative"],
         "answer": 1,
         "why": "R-squared is measured against the mean baseline, and a model can do worse than that - commonly on a test set after overfitting."},
        {"q": "Why is it spelled neg_mean_absolute_error?",
         "options": ["It returns the negative of the predictions",
                     "The helpers always maximise, so error metrics are negated",
                     "It is a typo kept for compatibility",
                     "It measures negative errors only"],
         "answer": 1,
         "why": "Negating lets one code path rank every metric by taking the largest, without knowing whether bigger or smaller is better for that metric."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Logistic regression
# ---------------------------------------------------------------------------
topic(
    "logistic_regression",
    "Logistic Regression",
    "Classification",
    "A linear model that outputs probabilities - the sensible first classifier "
    "for almost any problem, and the baseline every other one has to beat.",
    _svg(_box(16, 18, 128, 58, S, B) +
         '<path d="M24 68 C60 68, 72 30, 136 26" stroke="var(--accent-primary)" '
         'stroke-width="2" fill="none"/>' +
         _dots([(32, 68), (48, 66), (64, 60)], M) +
         _dots([(96, 32), (112, 28), (128, 26)]) +
         _txt(80, 86, "P(class) between 0 and 1", M, 7)),
    [
        ("Fitting a classifier",
         "The same three calls as a regressor, and a score that means accuracy "
         "rather than R-squared.",
         '''from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          random_state=0, stratify=y)

scaler = StandardScaler().fit(X_tr)
model = LogisticRegression(max_iter=1000).fit(scaler.transform(X_tr), y_tr)

print("classes_ :", model.classes_)
print("accuracy :", round(model.score(scaler.transform(X_te), y_te), 4))
print("first 8 predictions:", model.predict(scaler.transform(X_te))[:8])
'''),

        ("predict_proba is the useful output",
         "predict throws away the confidence. The probabilities are what let "
         "you decide where the line should be.",
         '''from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          random_state=0, stratify=y)
sc = StandardScaler().fit(X_tr)
model = LogisticRegression(max_iter=1000).fit(sc.transform(X_tr), y_tr)

proba = model.predict_proba(sc.transform(X_te))
pred = model.predict(sc.transform(X_te))

print("predict_proba shape:", proba.shape, "- one column per class")
print()
print(" P(class 0)  P(class 1)  predicted")
for p, k in list(zip(proba, pred))[:5]:
    print("%11.4f %11.4f %10d" % (p[0], p[1], k))
print()
print("rows sum to 1:", np.allclose(proba.sum(axis=1), 1.0))
'''),

        ("What the coefficient means",
         "Not a probability, and not a slope in the target - it is a change in "
         "the log of the odds.",
         '''from sklearn.linear_model import LogisticRegression
import numpy as np

# One feature, so the coefficient is readable.
X = np.array([[1], [2], [3], [4], [5], [6], [7], [8]])
y = np.array([0, 0, 0, 0, 1, 1, 1, 1])

model = LogisticRegression().fit(X, y)
print("coef_     :", model.coef_[0].round(4))
print("intercept_:", model.intercept_.round(4))
print()
print("the coefficient is in log-odds per unit of x:")
print("odds multiply by exp(coef) = %.3f for each step of 1"
      % np.exp(model.coef_[0][0]))
'''),

        ("It needs its features scaled",
         "The same data twice. Only one of the two fits converges in the "
         "default number of iterations.",
         '''from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import warnings

X, y = load_breast_cancer(return_X_y=True)

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    LogisticRegression(max_iter=100).fit(X, y)
    names = [w.category.__name__ for w in caught]
print("unscaled, max_iter=100 ->", names or ["no warning"])

Xs = StandardScaler().fit_transform(X)
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    LogisticRegression(max_iter=100).fit(Xs, y)
    names = [w.category.__name__ for w in caught]
print("scaled,   max_iter=100 ->", names or ["no warning"])
'''),

        ("More than two classes, without changing anything",
         "One row of coefficients per class, and probabilities that still sum "
         "to one across them.",
         '''from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

X, y = load_iris(return_X_y=True)
Xs = StandardScaler().fit_transform(X)

model = LogisticRegression(max_iter=1000).fit(Xs, y)

print("classes_ :", model.classes_)
print("coef_    :", model.coef_.shape, "- one row per class")
print()
proba = model.predict_proba(Xs[:3])
print("probabilities for the first three rows:")
print(np.round(proba, 4))
print("each row sums to 1 and the winner is predict()'s answer")
'''),

        ("The boundary is a straight line",
         "Which is the model's one real limitation, and it is easy to "
         "construct data that shows it.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

X, y = make_moons(n_samples=300, noise=0.2, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

for model in [LogisticRegression(), DecisionTreeClassifier(random_state=0)]:
    model.fit(X_tr, y_tr)
    print("%-24s test accuracy %.3f"
          % (type(model).__name__, model.score(X_te, y_te)))
print()
print("two interleaving crescents cannot be separated by a straight line,")
print("which is exactly what logistic regression is limited to.")
'''),
    ],
    [
        "Despite the name it is a <strong>classifier</strong>; the regression "
        "in it is on the log-odds, not on the class.",
        "<code class='mono-font'>predict_proba</code> returns one column per "
        "class, in <code class='mono-font'>classes_</code> order, and each row "
        "sums to 1.",
        "<code class='mono-font'>predict</code> is just "
        "<code class='mono-font'>predict_proba</code> with a 0.5 threshold "
        "applied - which is a choice, not a law.",
        "A coefficient is a change in log-odds per unit of the feature; "
        "<code class='mono-font'>exp(coef)</code> is the odds ratio.",
        "It is fitted by iterative optimisation, so unscaled features produce "
        "a <code class='mono-font'>ConvergenceWarning</code> - scale them.",
        "The decision boundary is linear, so genuinely curved problems need "
        "engineered features or a different model.",
    ],
    """title: Logistic Regression: A Practical Guide
intro: The classifier to try first, what the problem. It's fast, it makes chances rather than bare labels. It gives every other model a number to beat.

## Why it is called regression

Logistic regression is the standard first classifier. It is fast to train, produces probabilities rather than just labels, and its coefficients are interpretable. For many tabular classification tasks it is the right starting point.

Despite the name, logistic regression is a classifier. It predicts which class a sample belongs to. The confusion is that the underlying arithmetic is a linear regression on a transformed target. The transformation is what makes it a classifier rather than a regression model.

The model also serves as a strong baseline. If a random forest or gradient-boosted tree barely beats logistic regression on your data, the extra complexity may not be worth the cost. Running logistic regression first tells you how much room there is for improvement.

This page covers the name, the probabilities, the coefficients, the scaling requirement and the parameters worth knowing. It also covers the multi-class case and the question of whether the probabilities the model outputs can be trusted.

The name is the first confusion and it has a real explanation. Logistic regression is a classifier. It predicts which class a sample belongs to. But the thing being fitted linearly isn't the class.

What it fits is the **log-odds**: the logarithm of the ratio between the chance of the positive class and the chance of the minus one. That quantity runs from minus infinity to plus infinity. This Makes it a thing a linear model can predict sensibly. The logistic function then squashes it back into the range 0 to 1, giving a chance.

So underneath it's a linear regression on a transformed target. The change is what turns an unbounded guess into a chance that can't escape its bounds. Predicting the chance right with linear regression would happily give 1.4 or -0.3. This Is why no one does that.

## Probabilities, not just labels

`predict` returns the class. `predict_proba` returns the chance of each class, as an array with one column per class in the order given by `classes_`.

The second is almost always more handy. `predict` throws away info you needed. A guess of "plus" with chance 0.51 and one with chance 0.99 are wildly different situations, and `predict` reports them the same way.

That matters wherever the two kinds of mistake have different costs. A medical screen that is 51% confident should probably be followed up. One that is 99% confident may warrant immediate action. A fraud check at 51% might ask for a second factor while one at 99% blocks the transaction. None of that is expressible if all you've is the label.

`predict` is just `predict_proba` with a threshold of 0.5. 0.5 is a default rather than a principle. Choosing a different threshold is one of the highest-value adjustments available. It gets its own module later in this track.

## Reading the coefficients

`coef_` has the same shape story as linear regression. One number per feature. But the units are different and the difference is the part people get wrong.

A coeff is the change in log-odds for a one-unit grow in the feature, holding the others fixed. Log-odds aren't natural. The conventional move is to exponentiate: `exp(coef)` is an **odds ratio**, the factor by which the odds times per unit of the feature.

A coeff of 1.17, as in the editor above, means the odds times by about 3.2 for each step of one in that feature. That is a statement about odds, not about chance. The two diverge. Timesing odds by 3.2 moves a chance of 0.1 to about 0.26. Moves 0.5 to about 0.76 and 0.9 to about 0.97. The same coeff has a different effect on chance based on where you start. This Is the whole point of the logistic curve being a curve.

The scale caveat from linear regression applies with equal force. A coeff's size depends on the feature's units. Coeffs are only close to each other when the features were standardised first. And since the model needs scaling anyway, this often comes for free.

## It has to be scaled

Unlike plain linear regression, logistic regression is fitted by iterative optimisation. There's no formula. A solver takes steps towards a min and stops when it stops raising or when it runs out of iterations.

Features on wildly different scales make that surface awkward to descend. The solver takes far more steps and often hits `max_iter` first. When it does, scikit-learn issues a `ConvergenceWarning` and returns the half-finished model anyway. It doesn't raise. The coeffs you get are simply wherever the solver had reached.

The editor above shows both cases on the same data. Unscaled and it warns, scaled and it settles comfortably within the same budget.

The right fix is `StandardScaler`, not a larger `max_iter`. Raising the iteration limit makes the warning go away by letting the solver grind to the same answer more slowly. Scaling makes the problem easy. Raising `max_iter` is the correct response only when the features are already scaled and the model is truly large.

There's a second reason scaling matters here: `LogisticRegression` applies L2 smoothing **by default**, controlled by `C`. A fine on coeff size is meaningless when the coeffs are in incomparable units. An unscaled fit is smoothed unevenly across features without saying so.

## C, and the regularisation nobody notices

`LogisticRegression()` is smoothed out of the box. This Surprises people who expect a plain max-likelihood fit.

The strength is set by `C`. The param is **inverted**. Small `C` means strong smoothing, large `C` means weak. `C=1.0` is the default, `C=0.01` shrinks the coeffs hard, and `C=1000` is close to unregularised. The inversion catches everybody at least once. Every other fine param in the library. `alpha` in Ridge and Lasso. Runs the other way.

The default is often reasonable, and `C` is one of the first things worth tuning. With many features it's often the only setting that matters.

`fine="l1"` gives the Lasso-style action of driving some coeffs to just zero. This Selects features as it fits. It needs a compatible solver such as `liblinear` or `saga`.

## More than two classes

Nothing changes at the call site. Fit on a target with three classes and `predict` returns one of the three, `predict_proba` returns three columns summing to one. `coef_` gains a row per class.

Underneath, recent versions fit a genuine multinomial model when the solver supports it. This Guesses all the classes jointly rather than running a series of one-against-the-rest fits. The hands-on consequence is that the chances are properly normed across classes rather than being separate binary chances rescaled afterwards.

`classes_` is worth reading rather than given. It holds the classes in sorted order. The columns of `predict_proba` follow it. So with string labels, `["cat", "dog", "fish"]`, column 0 is cat. Indexing that array the wrong way round is a quiet way to report the wrong chance.

## What it cannot do

The choice boundary is a straight line. A plane in higher dims. And no amount of tuning changes that.

For data that truly needs a curved boundary, the model will do its honest best and be beaten by any of it that can bend. The editor above makes it concrete. On two interleaving crescents, logistic regression manages 0.84 and a choice tree 0.99. The gap is fully structural.

Two responses. Engineer features that make the problem linear. Adding squares and products via `PolynomialFeatures` lets a linear boundary in the expanded space be a curved one in the first. Or use a model that finds the shape itself. This Is what trees and their ensembles do and why they dominate on tabular data.

Neither makes logistic regression a poor first choice. It fits in milliseconds, needs almost no tuning, makes calibrated-ish chances and coeffs you can read. Tells you right away whether the problem is easy. A grad-boosted ensemble that beats it by two points may not be worth the cost. One that beats it by thirty tells you the structure is truly non-linear.

## Are the probabilities trustworthy?

A model that outputs 0.7 is making a claim. Among the cases it labels 0.7, about 70% should turn out plus. A model whose chances meet that is **calibrated**, and not each classifier is.

Logistic regression is unusually good here. Because it's fitted by raising the likelihood of the seen labels, well-calibrated chances are what it's right optimising for. On reasonable data it makes them. That is a real edge over models that output a score which merely ranks right. A random forest's averaged votes and an SVM's distance from the boundary both rank well and are systematically off as chances, often pushed towards the middle or the extremes.

Two things spoil it even here. Heavy smoothing shrinks the coeffs and pulls the chances towards 0.5. And a badly imbalanced training set, or one resampled to fix imbalance, shifts them wholesale.

`CalibratedClassifierCV` wraps any classifier and fits a correction on held-out data. This Is how you get usable chances out of a model that doesn't give them on its own. Checking calibration is a matter of bucketing guesses and checking the mean predicted chance against the seen rate in each bucket. `calibration_curve` does it in a line. It's worth doing when a chance is going to be used as a number rather than as a ranking.

## Which solver, and when it matters

`LogisticRegression` takes a `solver`, and the default handles most cases. The choice turns relevant in three situations.

`lbfgs` is the default: fast, handles multinomial fits right, supports only L2 and no fine. `liblinear` is the one to use for L1 on a small dataset. It fits one-against-the-rest rather than a true multinomial. `saga` supports L1, L2 and ElasticNet, handles sparse data well. Is the one to reach for on large or high-dimensional problems. Text, in given. `newton-cholesky` is fast when there are many samples and few features.

The hands-on rule: leave it alone until a thing makes you change it. The two things that will are asking for a fine the default can't do. This Raises a clear error naming the compatible solvers. A fit that is slow on a large sparse mat. Here `saga` is the answer.

<strong>Does it work with more than two classes?</strong> Yes, with no change at the call site. `coef_` gains a row per class and `predict_proba` gains a column, in `classes_` order.

<strong>Can the target be strings?</strong> Yes. `classes_` holds them sorted. Guesses come back as the same strings.

<strong>Why is my fit 0.99 and the model useless?</strong> Almost certainly imbalance - if 99% of rows are one class, predicting that class always scores 0.99. The classification metrics module covers what to use instead.

## Where it sits among the alternatives

Three models occupy nearly the same space. Knowing what separates them saves trying all three blindly.

**Linear SVM** draws a straight boundary too. Chooses it by raising the margin between the classes rather than by raising likelihood. It's often marginally more accurate and gives no chances without an extra calibration step. This Is often the deciding factor against it.

**Naive Bayes** is faster still and makes a strong freedom assumption between features. On text it works oddly well despite that assumption being obviously false. It's the right first try for a bag-of-words problem.

**Grad boosting** finds non-linear structure without being told where to look and often wins on tabular data by a clear margin. It costs tuning time, fits slower. Gives up the readable coeffs.

The sequence worth following is: logistic regression first for the number to beat, grad boosting second to find out whether the problem has structure a line can't see. Any of it else only if those two leave a exact gap.

## Things to try

1. <strong>Look at the chances.</strong> In the second editor, find the rows nearest 0.5. Those are the ones where the label is close to any.
2. <strong>Break settling.</strong> In the fourth editor, drop `max_iter` to 20 on the scaled data and watch the warning return.
3. <strong>Turn smoothing up.</strong> Fit with `C=0.001` and compare the coeffs to the default. They shrink towards zero together.
4. <strong>Bend the boundary.</strong> In the last editor, wrap the logistic model in a pipeline with `PolynomialFeatures(degree=3)` and see how much of the gap closes.

## Where this leaves you

A fast linear classifier that returns chances, needs its features scaled, is smoothed by default with an inverted param. Draws a straight boundary. Fit it first on each classification problem. Treat its score as the number any of it more complicated has to justify itself against.
""",
    [
        {"q": "Why is it called regression when it classifies?",
         "options": ["Historical accident with no meaning",
                     "It fits a linear model to the log-odds, then squashes that into a probability",
                     "It can also do regression",
                     "It regresses towards the mean"],
         "answer": 1,
         "why": "The linear part predicts log-odds, which is unbounded and so suitable for a linear fit. The logistic function converts that to a probability between 0 and 1."},
        {"q": "What is predict() doing that predict_proba() is not?",
         "options": ["Fitting again",
                     "Applying a 0.5 threshold and discarding the confidence",
                     "Scaling the features",
                     "Averaging the classes"],
         "answer": 1,
         "why": "predict is predict_proba plus a threshold. The 0.5 is a default choice, and changing it is often the highest-value adjustment available."},
        {"q": "What does a ConvergenceWarning mean here?",
         "options": ["The data has missing values",
                     "The solver hit max_iter before finishing, and returned the model anyway",
                     "The classes are imbalanced",
                     "The model failed to fit"],
         "answer": 1,
         "why": "It does not raise. You get whatever coefficients the solver had reached, which is why scaling the features is the fix rather than raising max_iter."},
        {"q": "In LogisticRegression, what does a small C mean?",
         "options": ["Weak regularisation",
                     "Strong regularisation",
                     "Fewer classes",
                     "Fewer iterations"],
         "answer": 1,
         "why": "C is inverted relative to alpha in Ridge and Lasso: small C penalises coefficient size heavily. It catches almost everyone once."},
    ],
)


# ---------------------------------------------------------------------------
# 7. Cross-validation
# ---------------------------------------------------------------------------
topic(
    "cross_validation",
    "Cross-Validation",
    "Honest Numbers",
    "One split gives you one number and no idea how much to trust it. Five "
    "splits tell you both.",
    _svg("".join(
        _box(16, 18 + i * 14, 128, 10, S, B, 1) +
        _box(16 + i * 25.6, 18 + i * 14, 25.6, 10, S, A, 1)
        for i in range(5)) + _txt(80, 86, "each fold held out once", M, 7)),
    [
        ("Five splits instead of one",
         "The same model fitted five times, each time holding a different fifth "
         "back.",
         '''from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
import numpy as np

X, y = load_breast_cancer(return_X_y=True)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))

scores = cross_val_score(model, X, y, cv=5)

print("one score per fold:", np.round(scores, 4))
print("mean              :", round(scores.mean(), 4))
print("std               :", round(scores.std(), 4))
'''),

        ("Why one number was never enough",
         "Six different single splits of the same data, and the score you would "
         "have reported depends on which one you happened to run.",
         '''from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np

X, y = load_breast_cancer(return_X_y=True)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))

scores = []
for seed in range(6):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                              random_state=seed, stratify=y)
    scores.append(model.fit(X_tr, y_tr).score(X_te, y_te))

print("six single splits:", np.round(scores, 4))
print("lowest %.4f, highest %.4f - a spread of %.4f"
      % (min(scores), max(scores), max(scores) - min(scores)))
print()
print("any one of those could have been 'the' test score.")
'''),

        ("Stratified folds, and what plain folds do instead",
         "Watch the third plain fold: it contains none of the minority class at "
         "all.",
         '''from sklearn.model_selection import KFold, StratifiedKFold
import numpy as np

y = np.array([0] * 15 + [1] * 5)          # 75/25, five in the minority

print("KFold (splits by position, ignoring the classes):")
for _, te in KFold(n_splits=5, shuffle=True, random_state=0).split(y, y):
    print("   test labels:", y[te], " ones:", int(y[te].sum()))

print()
print("StratifiedKFold (each fold mirrors the whole):")
for _, te in StratifiedKFold(n_splits=5, shuffle=True, random_state=0).split(y, y):
    print("   test labels:", y[te], " ones:", int(y[te].sum()))
'''),

        ("Several metrics, and the training score too",
         "cross_validate is the fuller version, and the train column is how you "
         "see overfitting.",
         '''from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_validate
import numpy as np

X, y = load_breast_cancer(return_X_y=True)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))

out = cross_validate(model, X, y, cv=5,
                     scoring=["accuracy", "precision", "recall"],
                     return_train_score=True)

for key in sorted(out):
    print("%-22s %s" % (key, np.round(out[key], 3)))
'''),

        ("Preprocessing outside the loop invents skill",
         "Pure noise, nothing to learn, and one of these two numbers says the "
         "model found something.",
         '''from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
import numpy as np

# Pure noise: there is nothing to learn, so honest accuracy is about 0.5.
rng = np.random.RandomState(0)
X = rng.normal(size=(120, 2000))
y = rng.randint(0, 2, size=120)

# WRONG: choose the best features using every row, then cross-validate.
picked = SelectKBest(f_classif, k=20).fit_transform(X, y)
wrong = cross_val_score(LogisticRegression(max_iter=1000), picked, y, cv=5)

# RIGHT: the selection happens inside each fold, on the training part only.
right = cross_val_score(
    make_pipeline(SelectKBest(f_classif, k=20),
                  LogisticRegression(max_iter=1000)), X, y, cv=5)

print("selected before splitting :", round(wrong.mean(), 3))
print("selected inside the folds :", round(right.mean(), 3))
print()
print("the data is random. one of those numbers is a hallucination.")
'''),

        ("The other splitters",
         "cv= takes a number or a splitter object, and the object is how you "
         "handle time and groups.",
         '''from sklearn.model_selection import LeaveOneOut, KFold, TimeSeriesSplit
import numpy as np

X = np.arange(6).reshape(-1, 1)

print("KFold(3)      :", [list(te) for _, te in KFold(3).split(X)])
print("LeaveOneOut   :", [list(te) for _, te in LeaveOneOut().split(X)])
print()
print("TimeSeriesSplit(3) - train always precedes test:")
for tr, te in TimeSeriesSplit(n_splits=3).split(X):
    print("   train", list(tr), "-> test", list(te))
'''),
    ],
    [
        "<code class='mono-font'>cross_val_score</code> returns one score per "
        "fold - the <strong>spread</strong> matters as much as the mean.",
        "For a classifier, <code class='mono-font'>cv=5</code> uses "
        "<strong>StratifiedKFold</strong> automatically; for a regressor, plain "
        "<code class='mono-font'>KFold</code>.",
        "Every preprocessing step must sit inside a "
        "<code class='mono-font'>Pipeline</code>, or it is fitted on the fold "
        "it is about to be tested on.",
        "<code class='mono-font'>cross_validate</code> takes several metrics at "
        "once and can return training scores, which is how overfitting becomes "
        "visible.",
        "The models fitted during cross-validation are discarded - it estimates "
        "a procedure, it does not produce a model.",
        "<code class='mono-font'>TimeSeriesSplit</code> for ordered data, "
        "<code class='mono-font'>GroupKFold</code> when rows share an entity "
        "that must not straddle the split.",
    ],
    """title: Cross-Validation: A Practical Guide
intro: A single train/test split gives you one number drawn from a spread you never see. Cross-validation shows you the spread.

## The problem with one split

A single train/test split gives you one score. That score depends on which rows happened to land in each set. A different random seed would give a different number. Cross-validation addresses this by running multiple splits and reporting all the scores.

The idea is straightforward. Divide the data into `k` equal parts. Train on `k-1` of them, test on the remaining one. Repeat `k` times, each time holding out a different part. The result is `k` scores instead of one.

This gives you a mean and a spread. The mean is a better estimate of how the model performs in general. The spread tells you how sensitive the score is to which rows were held out. A tight spread means the model is stable. A wide spread means the result depends heavily on the particular data.

Cross-validation does not produce a final trained model. It produces an estimate of how well a model of this type, trained on this much data, tends to perform. You still fit a final model on all the data after deciding which approach to use.

A held-out test set answers the question honestly. It answers it once, on one given random pick of rows.

Run the split again with a different seed and the score moves. The editors on this page show six splits of the same data giving scores from 0.9737 to 0.9912. A spread of nearly two points, on an easy dataset with a few hundred rows. On a smaller or harder dataset the spread is much wider.

That variation isn't noise you can skip. If you compare two models on one split each and they differ by a point, you've learned nothing. The difference is well inside the range a single split makes by chance. Reporting the winner would be reporting which model got the friendlier rows.

Cross-validation fixes this by not choosing. It splits the data into `k` parts, holds each one out in turn, fits on the rest. Returns `k` scores. So each row is tested on just once and trained on `k-1` times.

## What the k numbers tell you

The mean is the headline, and the standard deviation is the part people skip.

A mean of 0.98 with a standard deviation of 0.006 is a stable, believable result. A mean of 0.98 with a standard deviation of 0.09 says the model works well on some subsets and badly on others. This Is a fully different situation and often means either very little data or a subgroup the model handles poorly.

Two models whose ranges share heavily aren't distinguishable by this evidence, what their means. That single habit. Looking at the spread before believing a difference. Blocks a large share of the wasted effort in applied machine learning.

`cross_val_score` returns the array. Printing it rather than only its mean costs nothing and is where the info is.

## How many folds

`cv=5` is the usual default and `cv=10` the other common choice. The trade between them is straightforward.

More folds mean each model trains on more data. Each is closer to the model you'd build dataset. The estimate is less pessimistic. More folds also mean more fits. Ten-fold takes twice if five-fold. And the training sets share more. This Makes the scores more linked and the standard deviation an underestimate of the true variability.

The extreme is `LeaveOneOut`. Here `k` equals the number of samples. each model trains on all but one row. This Is as close to the full-data model as possible. It costs `n` fits. It's worth it only on very small datasets. Its variance estimate is poor for the same link reason.

Five is a reasonable default for most work. Ten when the dataset is small enough that the extra fits are cheap and you want the training sets larger. `RepeatedStratifiedKFold` runs the whole thing a few times with different shuffles when you need a more solid guess of the spread.

## Stratification happens by default, and only for classifiers

Pass an int as `cv` and scikit-learn chooses the splitter for you: `StratifiedKFold` when the estimator is a classifier, plain `KFold` or else.

That default is a good one and worth understanding rather than leaning on blindly. The editor above shows what plain folds do to an imbalanced target. With five minority samples across five folds, the counts come out 2, 1, 0, 1, 1. One fold holds none of the class at all. The recall found on it's undefined and the score for that fold is meaningless. Stratified folds give just one to each.

Note that stratification is on the **target**. When the thing that must stay weighed is a thing else. A site, a batch, a demographic group. You need to pass a splitter object rather than an int.

## The rule that makes it honest

Cross-validation is only honest if all learned from data is learned inside the loop.

That includes the model, obviously. It also includes the scaler's mean and standard deviation, the imputer's median, the encoder's list of categories, the vectoriser's vocab, and. Most damagingly &mdash; any feature pick.

The fifth editor makes the cost concrete. The data is pure random noise with no tie between features and target. The honest fit is 0.5. Selecting the twenty "best" features using the whole dataset and then cross-validating gives **0.825**. The pick looked at the held-out rows, found the columns that happened to correlate with the target in those rows too. Handed the model a shortcut. Doing the pick inside the folds gives 0.45. This Is the truth.

That isn't a small distortion, and it's the single most common way published results turn out to be wrong. With 2000 pick features and 120 samples, some columns correlate with the target by chance. Choosing them using all the data is choosing them partly on the test rows.

`Pipeline` is the mechanism that blocks this. A pipeline is a single estimator as far as `cross_val_score` is concerned. Its `fit`. Including each transformer inside it. Runs on the training part of each fold only. Using one isn't a style preference. It's what makes the number mean what it says.

## What cross-validation does not give you

It doesn't give you a model. The `k` models fitted during the process are scored and thrown away.

What it gives you is an guess of how well **the method** performs. This prep, this estimator, these settings, on data like this. Once you've decided the method is good enough, you fit it once more on all the data. That is the model you keep. `cross_val_predict` returns the out-of-fold guesses if you want them for inspection. It's by name not a way of making a model either.

It also doesn't replace a final held-out test set when you've been using cross-validation to make choices. Checking twenty setting settings by cross-validation and reporting the best one's score is optimistic for the same reason as picking the best of twenty test scores. The winner was selected for doing well on those given folds. Nested cross-validation is the rigorous answer. A separate untouched test set is the hands-on one.

## The splitters worth knowing

`cv` accepts an int or a splitter object. The objects are how you say a thing the int can't.

`StratifiedKFold` and `KFold` are the defaults. Passing them by name lets you set `shuffle=True` and a `random_state`. This The int form doesn't. Note that `KFold` does **not** shuffle by default. Data arriving in a sorted order makes folds that are each a contiguous block. At times a disaster no one notices.

`TimeSeriesSplit` trains on the past and tests on what follows, never the reverse, with a training set that grows each time. It's the only correct choice for sorted data.

`GroupKFold` and `StratifiedGroupKFold` take a `groups` array and keep each row of a group on one side. Use them when a few rows show the same patient, customer, doc or device. Or else the model recognises the entity rather than learning the pattern. The score is inflated by an amount nothing reveals.

`ShuffleSplit` draws random train/test pairs without the each-row-tested-once ensure. This Is handy when you want many guesses from a large dataset cheaply.

## What it costs, and when that matters

Cross-validation fits the model `k` times. It costs roughly `k` times a single fit. For a logistic regression on a few thousand rows that is imperceptible. For a large ensemble on a large dataset it can turn a two-minute test into twenty.

Three ways to keep it affordable. `n_jobs=-1` runs the folds in parallel across cores. Since the folds are free this is close to free speed on any machine with more than one. Fewer folds. Three rather than ten. When you're exploring rather than reporting. And a subsample of the data while you're iterating, with the full run reserved for the result you intend to quote.

The mistake worth avoiding is skipping cross-validation because it's slow and going back to a single split. A single split isn't faster in any way that matters. It's the same fit once. It buys a number you can't calibrate. If the budget is truly tight, three folds on the full data beats one split each time.

Note also that `cross_validate` reports `fit_time` and `score_time` per fold. This Is the cheapest way to find out where the time is really going before optimising any of it.

## Reading the training scores

`return_train_score=True` adds a column that is worth the extra work. The gap between train and test is the clearest diagnostic in the whole library.

**Train high, test high, small gap.** The model has learned a thing that generalises. Nothing to fix.

**Train very high, test much lower.** Overfitting. The model has stored patterns exact to the training rows. The response is more smoothing, a simpler model, or more data.

**Train low, test low, small gap.** Underfitting. The model can't capture the structure even on data it has seen. The response is the opposite. A more flexible model, better features, less smoothing.

**Train lower than test.** Unusual and worth investigating rather than celebrating. It happens legitimately when smoothing or dropout is active during training but not scoring. Illegitimately when the folds aren't close.

The two failure modes need opposite treatments. This Is why guessing between them wastes so much time. One extra arg tells you which one you've.

<strong>Does KFold shuffle by default?</strong> No. Data arriving sorted makes folds that are each a contiguous block. This Can be a silent disaster. Pass a splitter object with `shuffle=True` when the order might mean a thing.

<strong>Can I cross-validate a pipeline?</strong> Yes. You should. A pipeline is a single estimator to `cross_val_score`. This Is just what keeps its transformers inside the folds.

<strong>Why is my cross-validated score lower than my test score?</strong> often because each fold trains on less data than a single 80/20 split does. The estimate is slightly pessimistic. A large gap suggests the split was lucky.

## Things to try

1. <strong>Run the second editor.</strong> Six seeds, six answers. That spread is the reason the rest of the page exists.
2. <strong>Look at the spread.</strong> In the first editor, print `scores.max() - scores.min()` and compare it against the difference between two models you're considering.
3. <strong>Run the leakage demo.</strong> The data is random. Sit with that the wrong version reports 0.825.
4. <strong>Watch overfitting appear.</strong> In the fourth editor, swap the pipeline for `DecisionTreeClassifier()` and compare the train and test columns.

## Where this leaves you

`cross_val_score` for a quick guess with its spread, `cross_validate` when you want a few metrics or the training scores, a `Pipeline` around all that learns. A splitter object when the data has time or groups in it. The mean is the headline. The spread is what tells you whether to believe it.
""",
    [
        {"q": "What does cross_val_score return?",
         "options": ["A fitted model",
                     "One score per fold",
                     "The mean score",
                     "The best model of the k"],
         "answer": 1,
         "why": "An array with one entry per fold. The spread across them matters as much as the mean, and the fitted models are discarded."},
        {"q": "Why must preprocessing go inside a Pipeline for cross-validation?",
         "options": ["It is faster",
                     "Otherwise it is fitted on the fold being held out, inflating the score",
                     "Pipelines are required by cross_val_score",
                     "It avoids a warning"],
         "answer": 1,
         "why": "Anything fitted before the split has seen every fold. With feature selection on noise this took a true 0.45 to a reported 0.825."},
        {"q": "You pass cv=5 with a classifier. Which splitter is used?",
         "options": ["KFold", "StratifiedKFold", "ShuffleSplit", "LeaveOneOut"],
         "answer": 1,
         "why": "scikit-learn picks StratifiedKFold for classifiers and plain KFold otherwise. Pass a splitter object when you need shuffling or a fixed seed."},
        {"q": "After cross-validating, which model do you deploy?",
         "options": ["The best-scoring fold's model",
                     "A new one fitted on all the data",
                     "An average of the k models",
                     "The last fold's model"],
         "answer": 1,
         "why": "Cross-validation estimates how a procedure performs. Once you accept the procedure, refit it once on everything - the k models are thrown away."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Classification metrics
# ---------------------------------------------------------------------------
topic(
    "classification_metrics",
    "Classification Metrics",
    "Classification",
    "Why accuracy is the wrong number more often than it is the right one, and "
    "what to report instead.",
    _svg(_box(14, 20, 60, 24, S, A) + _txt(44, 35, "precision", A, 8) +
         _box(86, 20, 60, 24, S, A) + _txt(116, 35, "recall", A, 8) +
         _box(14, 52, 132, 24, S, M) + _txt(80, 67, "accuracy: often useless", M, 8)),
    [
        ("The 98% model that predicts nothing",
         "A classifier that never says yes, on data where yes is rare - and the "
         "accuracy it reports.",
         '''from sklearn.dummy import DummyClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 99 rows of one class for every 1 of the other.
X, y = make_classification(n_samples=2000, n_features=10, weights=[0.99],
                           random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)

print("positives in the test set:", int(y_te.sum()), "of", len(y_te))
print()
lazy = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
print("always predict the majority:",
      round(accuracy_score(y_te, lazy.predict(X_te)), 4))
print("it never predicts a positive:", int(lazy.predict(X_te).sum()))
'''),

        ("Precision and recall, from their definitions",
         "Two fractions with the same numerator and different denominators, "
         "which is the whole difference between them.",
         '''from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np

# 10 actual positives; the model finds 6 of them and raises 2 false alarms.
y_true = np.array([1]*10 + [0]*90)
y_pred = np.zeros(100, dtype=int)
y_pred[:6] = 1          # 6 true positives
y_pred[10:12] = 1       # 2 false positives

tp = int(((y_true == 1) & (y_pred == 1)).sum())
fp = int(((y_true == 0) & (y_pred == 1)).sum())
fn = int(((y_true == 1) & (y_pred == 0)).sum())
print("true positives %d, false positives %d, false negatives %d" % (tp, fp, fn))
print()
print("precision = tp/(tp+fp) = %d/%d = %.3f"
      % (tp, tp + fp, precision_score(y_true, y_pred)))
print("recall    = tp/(tp+fn) = %d/%d = %.3f"
      % (tp, tp + fn, recall_score(y_true, y_pred)))
print("f1        = harmonic mean       = %.3f" % f1_score(y_true, y_pred))
'''),

        ("You can have either, at the other's expense",
         "Two models on the same data: one flags almost nothing, the other "
         "flags almost everything.",
         '''from sklearn.metrics import precision_score, recall_score
import numpy as np

y_true = np.array([1]*10 + [0]*90)

cautious = np.zeros(100, dtype=int)
cautious[:3] = 1                       # flags 3, all correct

eager = np.zeros(100, dtype=int)
eager[:40] = 1                         # flags 40, catching all 10

for label, pred in [("flags 3 cases", cautious), ("flags 40 cases", eager)]:
    print("%-16s precision %.3f   recall %.3f"
          % (label, precision_score(y_true, pred), recall_score(y_true, pred)))
print()
print("you can have either one at the expense of the other;")
print("which you want is a question about the cost of each mistake.")
'''),

        ("classification_report, the one to print",
         "Per-class precision, recall, f1 and support in a single call.",
         '''from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X, y = make_classification(n_samples=2000, n_features=10, weights=[0.95],
                           random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)

model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
print(classification_report(y_te, model.predict(X_te), digits=3))
'''),

        ("With three classes, the averaging matters",
         "The rare class is never predicted correctly. Two of these three "
         "averages hide that completely.",
         '''from sklearn.metrics import f1_score
import numpy as np

# three classes, very different sizes
y_true = np.array([0]*90 + [1]*8 + [2]*2)
y_pred = np.array([0]*90 + [1]*6 + [0]*2 + [0]*2)

for how in ("macro", "weighted", "micro"):
    print("%-9s %.3f" % (how, f1_score(y_true, y_pred, average=how,
                                       zero_division=0)))
print()
print("the rare class is predicted correctly zero times.")
print("only the macro average makes that visible.")
'''),

        ("balanced_accuracy, when you want one number",
         "The average recall across classes, which the lazy model cannot game.",
         '''from sklearn.metrics import balanced_accuracy_score, accuracy_score
import numpy as np

y_true = np.array([1]*10 + [0]*990)
majority = np.zeros(1000, dtype=int)

print("accuracy of always-say-no          :",
      round(accuracy_score(y_true, majority), 4))
print("balanced accuracy of the same thing:",
      round(balanced_accuracy_score(y_true, majority), 4))
print()
print("balanced accuracy averages the recall of each class,")
print("so ignoring a class entirely scores 0.5 rather than 0.99.")
'''),
    ],
    [
        "<strong>Accuracy</strong> is the fraction predicted correctly, and it "
        "is meaningless when one class dominates.",
        "<strong>Precision</strong> is how many of the flagged cases were real; "
        "<strong>recall</strong> is how many of the real cases were flagged.",
        "<strong>F1</strong> is their harmonic mean - a single number that "
        "punishes a low value on either side.",
        "Always print <code class='mono-font'>classification_report</code>: the "
        "per-class rows are where an ignored class shows up.",
        "For several classes, <strong>macro</strong> averaging treats every "
        "class equally and <strong>weighted</strong> lets the big ones dominate.",
        "<code class='mono-font'>DummyClassifier</code> tells you what the "
        "metric scores for doing nothing - always the first comparison.",
    ],
    """title: Classification Metrics: A Practical Guide
intro: A model can be 99% accurate and fully useless. Which metric you report is a statement about which mistakes you're willing to make.

## Why accuracy misleads

Accuracy is the metric most people reach for first. It counts how many predictions were correct and divides by the total. That simplicity is appealing but misleading on any dataset where the classes are not evenly split.

Classification problems in practice are rarely balanced. Fraud accounts for a fraction of a percent of transactions. Disease affects a small share of screened patients. Equipment fails on a tiny share of cycles. In each case, a model that always predicts the majority class gets a high accuracy while catching none of the cases you actually care about.

The metrics that matter for imbalanced data are precision, recall and F1. Precision answers: of the cases the model flagged, how many were real. Recall answers: of the real cases, how many did the model find. F1 balances the two. Each tells you something accuracy hides.

This page starts with accuracy's failure mode, then covers precision, recall, F1 and the classification report. It also covers the averaging strategies that apply when there are more than two classes.

Fit is the proportion of guesses that were correct. It's the default that `score()` returns. On weighed data it's a reasonable summary. On imbalanced data it's close to worthless.

The editor above makes the case in five lines. With 99 negatives for each plus, a `DummyClassifier` that always predicts the majority scores **0.9867** and never predicts a single plus. It has learned nothing, it would be useless for any purpose. It beats plenty of real models on the metric.

That situation isn't exotic. Fraud, disease screening, equipment failure, click-through, churn, defect spotting. The notable class is rare in nearly each problem worth solving. Rarity is just what breaks fit. The rarer the thing you care about, the higher the score for skipping it.

So the first thing to do with any classification problem is count the classes. The second is fit a dummy. If the dummy's score is close to the model's, the model has added nothing even so of how high the number looks.

## Precision and recall

Both are fractions of the same numerator. The true positives, the cases you flagged that really were plus. And they differ in what they divide by.

**Precision** cuts by all you flagged. It answers: *when this model says yes, how often is it right?* Low precision means false alarms.

**Recall** cuts by all that was really plus. It answers: *of the cases that were really there, how many did we catch?* Low recall means misses.

The two names are unhelpful and the questions aren't. It's worth reading them as those two sentences until the meanings stop needing to be looked up.

Which one matters is decided fully by the cost of each kind of mistake. The costs are often wildly different. A cancer screen that misses cases is far worse than one that makes false alarms sent for a second test. Recall dominates. A spam filter that deletes real mail is far worse than one that lets some spam through. So Precision dominates. An email flagged wrongly is an annoyance. A tumour missed is a catastrophe. No metric knows that, and no default can.

## They trade against each other

You can always have more of one by accepting less of the other. The third editor shows the extremes on the same data. A model flagging 3 cases has precision 1.000 and recall 0.300. One flagging 40 has precision 0.250 and recall 1.000.

Neither is better. They're different operating points on the same underlying model. Choosing between them is the choice the metric exists to inform.

That is why quoting one alone is misleading. A claim of "95% precision" says nothing without the recall beside it. A model that flags one obvious case and nothing else reaches it trivially. The pair together shows the action. Either alone can be manufactured.

**F1** merges the pair into one number by taking their harmonic mean. This Is on purpose unforgiving. Unlike an plain mean, it stays low if either input is low. F1 of a model with precision 1.0 and recall 0.1 is 0.18, not 0.55. That property is what makes it handy as a single summary when you need to rank models. It's still a summary. Two models with the same F1 can behave very differently.

## Print the report

`classification_report` gives precision, recall, F1 and support. The number of true instances. For each class, plus the means. It's one line and it should be the default thing you print after fitting a classifier.

The per-class rows are the point. An aggregate can look healthy while one class is being skipped fully. The row for that class shows it right away. Precision and recall both zero, with a support telling you how many cases that shows.

`support` deserves focus on its own. A class with 4 examples in the test set makes metrics that move in steps of 25%. A difference between two models on that class is noise. Reading the support column before believing a per-class number saves a lot of misplaced trust.

## Averaging across several classes

With more than two classes, the per-class numbers have to be mixed in some way. The choice changes the answer a lot.

**macro** means the per-class scores, treating each class as equally key even so of size. A class with 2 samples counts as much as one with 900.

**weighted** means them in proportion to support, so large classes dominate.

**micro** pools all the guesses before finding. This For single-label classification makes it the same to fit.

The fifth editor shows how far apart they can be. Macro 0.612, weighted 0.949, micro 0.960, on guesses where the rarest class is never once spotted right. Only macro reflects that failure. Weighted and micro report the speed on the big classes and let the small one disappear.

The rule that follows: **use macro when the rare classes matter**. This Is often why they're notable. Use weighted when you truly care about total volume. Never report micro on imbalanced data and call it any of it other than fit.

## balanced_accuracy, for a single honest number

`balanced_accuracy_score` means the recall of each class. It's fit with the class-size distortion removed.

Its virtue is that the lazy model can't game it. Always predicting the majority gives recall 1.0 on that class and 0.0 on the other, blending to just 0.5. Which is what "no skill" should look like. The editor above shows 0.99 against 0.5 for the same guesses.

It's the right default when you want one number for an imbalanced problem and don't want to think about precision and recall apart. It's still one number. It still hides the trade-off. It belongs alongside the report rather than instead of it.

## Choosing, in practice

A short method that covers most cases.

Count the classes first. If they're roughly weighed, fit is fine and the rest of this page is optional. If they aren't, it isn't.

Fit a `DummyClassifier` and record its score on what metric you plan to use. That is the floor. A model that doesn't clear it convincingly hasn't earned any of it.

Decide which mistake is worse in the actual use. Say why in a sentence. If missing a case is worse, lead with recall. If a false alarm is worse, lead with precision. If they're close, F1 or weighed fit.

Print `classification_report` even so, and read the support column before trusting any per-class row.

And note that all of these are found from `predict`. This Applied a 0.5 threshold to a chance. Moving that threshold moves precision and recall in opposite directions without refitting any of it. Which is the subject of the next module. Often the cheapest improvement available.

## Metrics that use the probability rather than the label

All above is found from `predict`. This Has already committed to a label. Two metrics use `predict_proba` instead. They measure a thing different. How well the model *ranks* cases, on its own of where the threshold sits.

**ROC AUC** is the chance that a at random chosen plus is scored higher than a at random chosen minus. 1.0 is perfect ranking, 0.5 is random. Its appeal is that it summarises each possible threshold at once. It checks models without committing to an operating point. Its weakness is that it's found across the whole range including thresholds no one would use. On heavily imbalanced data it stays flatteringly high. The huge number of true negatives dominates the false positive rate.

**Mean precision**, the area under the precision-recall curve, is the better choice when positives are rare. It skips true negatives fully. It can't be inflated by having a great many of them. It moves when the model's action on the class you care about changes.

The hands-on rule: report ROC AUC on roughly weighed problems, mean precision on imbalanced ones. Neither as a substitute for the metric that reflects the actual choice. A high AUC means the ranking is good. It doesn't mean any given threshold makes a handy precision and recall.

## Multi-label and multi-class are different problems

Two situations get confused because both involve more than two labels.

**Multi-class** means each sample belongs to just one of a few classes. A flower is setosa or versicolor or virginica. All on this page applies, with the blending choice being the only addition.

**Multi-label** means each sample can carry a few labels at once. An article tagged both "politics" and "economics". Here `y` is a 2-D binary array rather than a 1-D vector, fit turns exact-set-match and is brutally strict. The blending choices gain a fourth option, `samples`. This Means per row rather than per class.

Confusing the two makes shape errors rather than silent wrongness. This Is fortunate. `MultiLabelBinarizer` is the tool for getting from a list of tag lists to the array the estimators want.

<strong>What is zero_division for?</strong> Precision is undefined when nothing was flagged. Recall when nothing was plus. The arg says what to return instead of raising - `0` is the usual choice. Seeing it fire tells you a class was never predicted.

<strong>Which metric should I optimise in a search?</strong> The one that reflects the choice. Passing `scoring="f1"` or `scoring="balanced_accuracy"` to a grid search changes which model wins. Leaving it at the default optimises fit whether or not that is what you want.

<strong>Can I weight the classes instead of changing the metric?</strong> Yes. Often you should do both. `class_weight="weighed"` changes what the model optimises during fitting. The metric changes what you measure afterwards.

## Reporting a number somebody will act on

The metric that ends up in a slide is rarely the one that should drive the choice. Closing that gap is worth a paragraph.

Precision and recall are ratios, and ratios hide volume. "Recall of 0.6" sounds moderate. "we miss four hundred cases a month" is the same fact and provokes a different conversation. Timesing the rates back into counts. How many caught, how many missed, how many false alarms per week. Turns an abstract score into a thing a person with domain knowledge can judge.

That translation also exposes whether the model is worth deploying at all. A fraud model with precision 0.3 sounds poor until you work out that each investigation costs fifty pounds and each caught case saves two thousand, at which point flagging three cases to catch one is obviously correct. The reverse happens too. An impressive-looking model whose false alarms consume more analyst time than the catches save.

The habit worth forming is to state, alongside each metric, what it means in units of the thing the organisation cares about. It takes one extra line and it's the line that decides whether anyone uses the model.

## Things to try

1. <strong>Run the first editor.</strong> 0.9867. Not one plus predicted. Sit with the number before reading on.
2. <strong>Change the balance.</strong> Set `weights=[0.5]` and re-run. Fit stops flattering the dummy right away.
3. <strong>Read the support column.</strong> In the fourth editor, note how few positives the metrics for class 1 are found from.
4. <strong>Break the macro mean.</strong> In the fifth editor, make the model get the rare class right once and watch macro move far more than weighted.

## Where this leaves you

Fit for weighed problems only. Precision when false alarms cost, recall when misses cost, F1 or weighed fit when you need one number. `classification_report` printed each time so an skipped class can't hide behind an mean.
""",
    [
        {"q": "A classifier scores 99% accuracy on data that is 99% one class. What has it shown?",
         "options": ["It is an excellent model",
                     "Possibly nothing - always predicting the majority scores the same",
                     "The data needs more features",
                     "That accuracy is the right metric here"],
         "answer": 1,
         "why": "A DummyClassifier predicting the majority achieves it without learning anything. Fitting one is how you find out whether a score means anything."},
        {"q": "What does recall measure?",
         "options": ["How many flagged cases were correct",
                     "How many of the real positives were found",
                     "Overall correctness",
                     "The false positive rate"],
         "answer": 1,
         "why": "Recall divides true positives by everything that was actually positive - it is about misses. Precision divides by everything flagged, and is about false alarms."},
        {"q": "Why is F1 a harmonic mean rather than an ordinary one?",
         "options": ["It is faster to compute",
                     "It stays low when either precision or recall is low",
                     "It handles more than two classes",
                     "Convention only"],
         "answer": 1,
         "why": "Precision 1.0 with recall 0.1 gives F1 of 0.18, not 0.55. An ordinary average would let one good half disguise a bad one."},
        {"q": "Which averaging makes an ignored rare class visible?",
         "options": ["micro", "weighted", "macro", "all three equally"],
         "answer": 2,
         "why": "Macro treats every class equally regardless of size. Weighted and micro are dominated by the large classes, and micro equals accuracy for single-label problems."},
    ],
)


# ---------------------------------------------------------------------------
# 9. The confusion matrix
# ---------------------------------------------------------------------------
topic(
    "confusion_matrix",
    "The Confusion Matrix",
    "Classification",
    "The table every classification metric is computed from - and the one place "
    "you can see which mistakes the model is actually making.",
    _svg(_box(40, 22, 40, 26, S, M) + _txt(60, 39, "TN", M, 9) +
         _box(80, 22, 40, 26, S, M) + _txt(100, 39, "FP", M, 9) +
         _box(40, 48, 40, 26, S, M) + _txt(60, 65, "FN", M, 9) +
         _box(80, 48, 40, 26, S, A) + _txt(100, 65, "TP", A, 9) +
         _txt(80, 16, "predicted", M, 7)),
    [
        ("The four counts",
         "Rows are what was true, columns are what was predicted. Everything "
         "else on this page is arithmetic on these four numbers.",
         '''from sklearn.metrics import confusion_matrix
import numpy as np

y_true = np.array([1]*10 + [0]*90)
y_pred = np.zeros(100, dtype=int)
y_pred[:6] = 1          # 6 caught
y_pred[10:12] = 1       # 2 false alarms

cm = confusion_matrix(y_true, y_pred)
print("rows are actual, columns are predicted:")
print(cm)
print()
tn, fp, fn, tp = cm.ravel()
print("true negatives :", tn)
print("false positives:", fp, "- flagged, and wrong")
print("false negatives:", fn, "- missed")
print("true positives :", tp)
'''),

        ("Every metric, derived from the table",
         "Precision, recall and accuracy are three different fractions of the "
         "same four counts.",
         '''from sklearn.metrics import confusion_matrix, precision_score, recall_score
import numpy as np

y_true = np.array([1]*10 + [0]*90)
y_pred = np.zeros(100, dtype=int)
y_pred[:6] = 1
y_pred[10:12] = 1
tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

print("precision = tp/(tp+fp) = %d/%d = %.3f" % (tp, tp + fp, tp / (tp + fp)))
print("recall    = tp/(tp+fn) = %d/%d = %.3f" % (tp, tp + fn, tp / (tp + fn)))
print("accuracy  = (tp+tn)/all = %d/%d = %.3f"
      % (tp + tn, len(y_true), (tp + tn) / len(y_true)))
print()
print("sklearn agrees: %.3f %.3f"
      % (precision_score(y_true, y_pred), recall_score(y_true, y_pred)))
'''),

        ("With several classes it stops being 2x2",
         "And the interesting part is which classes get mistaken for which - "
         "which no single metric can tell you.",
         '''from sklearn.metrics import confusion_matrix
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

data = load_iris()
names = data.target_names
# Sepal measurements only - deliberately not enough to separate the last two.
X, y = data.data[:, :2], data.target
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4,
                                          random_state=1, stratify=y)

model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
cm = confusion_matrix(y_te, model.predict(X_te))

print("            " + "".join("%12s" % n for n in names))
for i, row in enumerate(cm):
    print("%-12s" % names[i] + "".join("%12d" % v for v in row))
print()
print("setosa is never confused; the other two are, and not equally")
'''),

        ("Normalise by row to compare unequal classes",
         "Raw counts are dominated by whichever class is largest. Row "
         "proportions are not.",
         '''from sklearn.metrics import confusion_matrix
import numpy as np

y_true = np.array([1]*10 + [0]*990)
y_pred = np.zeros(1000, dtype=int)
y_pred[:7] = 1
y_pred[10:60] = 1

print("counts:")
print(confusion_matrix(y_true, y_pred))
print()
print("normalised by row (what happened to each actual class):")
print(np.round(confusion_matrix(y_true, y_pred, normalize="true"), 3))
print()
print("row normalisation is the useful one when the classes differ in size")
'''),

        ("labels= fixes the order and the missing classes",
         "Without it, a class the model never predicted can vanish from the "
         "table entirely.",
         '''from sklearn.metrics import confusion_matrix
import numpy as np

y_true = np.array(["cat", "dog", "cat", "fish", "dog", "cat"])
y_pred = np.array(["cat", "dog", "dog", "fish", "dog", "fish"])

labels = ["cat", "dog", "fish"]
cm = confusion_matrix(y_true, y_pred, labels=labels)
print("labels=", labels)
print(cm)
print()
print("passing labels= fixes the order and guarantees every class")
print("appears, even one the model never predicted.")
'''),

        ("Read the rows the model got wrong",
         "The matrix says how many. The rows themselves say why.",
         '''from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np

data = load_iris()
X, y = data.data[:, :2], data.target
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4,
                                          random_state=1, stratify=y)
model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
pred = model.predict(X_te)

wrong = np.flatnonzero(pred != y_te)
print("misclassified:", len(wrong), "of", len(y_te))
print()
print(" sepal_len  sepal_wid   actual        predicted")
for i in wrong[:6]:
    print("%10.1f %10.1f   %-12s %-12s"
          % (X_te[i][0], X_te[i][1], data.target_names[y_te[i]],
             data.target_names[pred[i]]))
'''),
    ],
    [
        "<strong>Rows are the truth, columns are the prediction.</strong> "
        "The diagonal is correct; everything off it is a mistake.",
        "For two classes, <code class='mono-font'>cm.ravel()</code> unpacks to "
        "<code class='mono-font'>tn, fp, fn, tp</code> in that order.",
        "Precision, recall, accuracy and the rest are all arithmetic on these "
        "four counts - the table is the thing they summarise.",
        "<code class='mono-font'>normalize=\"true\"</code> divides by row, "
        "showing what happened to each actual class regardless of its size.",
        "Pass <code class='mono-font'>labels=</code> to fix the order and keep "
        "a never-predicted class in the table.",
        "Confusions are usually <strong>asymmetric</strong>: A mistaken for B "
        "is a different count from B mistaken for A.",
    ],
    """title: The Confusion Matrix: A Practical Guide
intro: each classification metric is a fraction found from four numbers. Looking at the four right tells you things no fraction can.

## What the table is

A single accuracy number hides where the model goes wrong. The confusion matrix shows exactly where each mistake happens. It breaks the predictions down by class and by error type, so you can see whether the model confuses cats with dogs or misses a rare class entirely.

Reading a confusion matrix is a skill worth building early. Every other classification metric -- precision, recall, F1, specificity -- can be computed from the four cells of a binary confusion matrix. Once you can read the table, the formulas follow naturally.

The matrix also helps you decide what to fix. If false positives are high, the model is too aggressive. If false negatives are high, it is too cautious. Adjusting the threshold or rebalancing the classes targets one at the expense of the other. The confusion matrix is what tells you which direction to push.

This page covers the table layout, the naming convention, the multi-class extension and the normalised display that makes comparison easier.

The confusion mat cross-tabulates what was true against what was predicted. Rows are the actual classes, columns are the predicted ones. Each cell counts how many samples fell into that combination.

The main-line is where the two agree. Correct guesses. All off the main-line is a mistake. *which* off-main-line cell it lands in tells you what kind.

For two classes the rule is worth storing because `ravel()` returns it in this order: **true minus, false plus, false minus, true plus**. Reading it as `tn, fp, fn, tp = cm.ravel()` is the standard line.

The naming is easier than it looks once you read it as two words rather than one phrase. The second word is what the model *said*. The first word is whether it was *right*. So a false minus is a case the model called minus and was wrong about &mdash; a miss.

## Why it beats any single number

A metric compresses the table into one figure. Compression loses just the info you need to improve the model.

Fit of 0.94 could be 88 true negatives and 6 true positives with 4 misses and 2 false alarms. Or it could be 94 true negatives, no true positives. 6 misses, with the model never predicting the positive class at all. Those are fully different situations and fit reports them the same way.

The mat sets apart them right away. It does so before you've decided which metric matters. That is the hands-on arg for printing it first. It tells you what the model is doing, and only then do you choose the number that summarises it.

It also tells you which direction to push. Too many false positives and too few false negatives means the threshold is too low. The reverse means it's too high. Both visible at a glance, neither visible in an fit score.

## The multi-class version, and what it reveals

With `k` classes the mat is `k` by `k`. The off-main-line structure carries info that no averaged metric preserves.

The editor above fits iris on sepal readings only. on purpose too little. And the result is instructive. Setosa is classified just right, never confused with any of it. Versicolor and virginica are confused with each other again and again. **not symmetrically**. Versicolor is called virginica 8 times, while virginica is called versicolor 5 times.

That skew is a real finding and it's invisible in an F1 score. It tells you the boundary between those two classes is drawn slightly off centre. It tells you setosa is a solved problem while the other two need better features. A macro F1 of 0.78 tells you none of that.

The general habit: on a multi-class problem, find the largest off-main-line cell. It's almost always one exact pair being confused. It's almost always the most productive thing to work on.

## Normalising, and which way

Raw counts are dominated by class size. On a 99-to-1 problem the true-minus cell is huge and the rest are visually invisible. This Makes the table hard to read though the numbers are correct.

`norm="true"` cuts each row by its total, giving the proportion of each actual class that went to each guess. The main-line then reads as per-class recall. A row that is mostly off the main-line shows a class the model handles badly even so of how few samples it has.

`norm="pred"` cuts by column instead, giving the proportion of each guess that was correct. The main-line reads as per-class precision.

`norm="all"` cuts by the grand total. This Is at times handy and often the least helpful of the three.

Row norming is the default worth reaching for. It answers "what does the model do with each kind of case". This Is the question that lives changes in class balance.

## The labels argument

`confusion_matrix` infers the classes from the data it's given, sorted. Two consequences bite.

A class present in `y_true` but never predicted still appears. But a class absent from both, perhaps because the test split happened to hold none of it, disappears fully. The mat silently turns smaller than expected. Code that indexes into it by class spot then reads the wrong cell.

And the order is sorted. This For string labels is alphabetical: `["cat", "dog", "fish"]`. given a different order and labelling the axes so makes a table that is confidently wrong.

Passing `labels=` fixes both. It ensures the size, ensures the order. Makes the code free of which classes happened to turn up in a given split. It's worth passing habitually rather than when a problem appears.

## From the table to the rows

The mat says how many mistakes of each kind. The next question is always why. Answering it means looking at the samples themselves.

Selecting the misclassified rows takes one line. `np.flatnonzero(pred != y_true)`. And reading a handful of them is always the most helpful ten minutes available. often they've a thing in common. Values near a boundary, a category the training data barely covered, missing fields that were imputed, or labels that are simply wrong in the source data.

Each of those has a different response. None of them is "try a different model". Mislabelled ground truth in given is far more common than people expect, and no amount of tuning fixes it. The model is being penalised for being right.

The editor above does just this for the iris confusion. The misclassified rows are all sepal readings in the shared middle of the two species. That isn't a model problem. It's the honest answer that these two features don't separate those two classes. The fix is petal readings rather than a fancier classifier.

## The other convention, and why it causes trouble

scikit-learn puts truth on the rows and guesses on the columns. A good deal of the statistics literature does the opposite. Some textbooks put the positive class first rather than second.

That means a mat copied from a paper, a blog post or a lecture slide may be transposed scaled to what `confusion_matrix` makes. A transposed mat swaps precision and recall without changing any of it visible. The numbers all look plausible. They're simply answering the other question.

Two habits prevent it. Print the mat with labelled axes rather than as a bare array. This Takes three lines and drops the ambiguity permanently. And sanity-check against a metric you trust. Find recall with `recall_score` and confirm it matches the main-line cell cut by its row total. If it matches the column total instead, the orientation isn't what you assumed.

The same caution applies to the binary case. Here The positive class is whichever label sorts second. `1` before `0` isn't the order, `0` then `1` is. With string labels, `"no"` sorts before `"yes"`. This Often happens to be right. With `"minus"` and `"plus"` it also happens to be right. With `"benign"` and `"malignant"` it's right for the wrong reason. With labels where it isn't, `pos_label=` is the arg that says so by name.

## What it cannot tell you

Two limits worth stating, because the mat is or else so handy that it gets asked questions it can't answer.

It says nothing about trust. each cell counts hard guesses. A case predicted plus at 0.51 and one at 0.99 are the same entry. A model can have an great mat and terrible chances, or the reverse. Only the chance-based metrics set apart them.

And it shows one threshold. Change the threshold and each cell moves. That is the whole mechanism of the precision-recall trade. So a confusion mat is a snapshot of one operating point, not a description of the model. Checking two models by their mats means checking them at what threshold each happened to use.

<strong>Is there a plotting version?</strong> `ConfusionMatrixDisplay.from_estimator(model, X, y)` draws it with matplotlib. This Is worth using once the mat is bigger than about four by four and the numbers stop being readable as text.

<strong>Which class is "plus" in a binary problem?</strong> Whichever label sorts second. `0` then `1` puts `1` plus. Pass `pos_label=` when the sorted order isn't what you mean.

<strong>Can I get one mat per class for a multi-label problem?</strong> Yes - `multilabel_confusion_matrix` returns a stack of 2x2 tables, one per label. This Is the right shape when a sample can carry a few labels at once.

## Putting a cost on each cell

The mat turns a choice tool rather than a diagnostic the moment you attach a number to each kind of mistake.

The four cells rarely cost the same. A false minus on a fraud check is the value of the fraud. A false plus is a few minutes of an analyst's time. A false minus on a medical screen is a missed diagnosis. A false plus is a second test. A false minus on a spam filter is one unwanted email. A false plus is a lost message the recipient never knew about.

Once those numbers exist, the expected cost of a model is the sum of each cell times'd by its price. Checking two models turns math rather than arg. It also settles the threshold question right. Sweep the threshold, find the total cost at each one. Pick the min. That is a better method than choosing a threshold to hit a round-numbered precision, and it takes about the same effort.

The exercise is worth doing even when the costs are rough. Guessing that a miss is roughly ten times worse than a false alarm is enough to rule out most of the range. It forces the conversation with whoever owns the problem. Who often has a much clearer view of the scaled costs than the person building the model, and who is rarely asked.

Where it goes wrong is treating the guessed costs as precise. They aren't. A threshold tuned to the third decimal place of an invented cost ratio is false precision. The handy output is a region rather than a point. Anywhere in this range is sensible, and outside it isn't.

## Things to try

1. <strong>Unpack the four counts.</strong> In the first editor, find precision and recall yourself from `tn, fp, fn, tp` before looking at what the library returns.
2. <strong>Find the worst pair.</strong> In the third editor, locate the largest off-main-line cell and note that it isn't mirrored.
3. <strong>Switch the norming.</strong> In the fourth editor, compare `norm="true"` with `norm="pred"` and work out which main-line is recall and which is precision.
4. <strong>Read the mistakes.</strong> In the last editor, raise the slice to see all thirteen and look for what they've in common.

## Where this leaves you

Four counts for two classes, `k` by `k` for more, rows as truth and columns as guess. Print it before choosing a metric, norm by row when the classes are uneven, pass `labels=` so the shape is ensured. Read the rows behind the largest off-main-line cell before changing any of it.
""",
    [
        {"q": "In a scikit-learn confusion matrix, what do the rows represent?",
         "options": ["The predicted classes",
                     "The actual classes",
                     "The features",
                     "It depends on the argument order"],
         "answer": 1,
         "why": "Rows are the truth and columns the prediction. The diagonal is correct; everything off it is a mistake of a specific kind."},
        {"q": "What does cm.ravel() return for a binary problem?",
         "options": ["tp, fp, fn, tn", "tn, fp, fn, tp", "tp, tn, fp, fn", "fp, fn, tp, tn"],
         "answer": 1,
         "why": "True negative, false positive, false negative, true positive - reading order across the 2x2 table."},
        {"q": "Why pass labels= to confusion_matrix?",
         "options": ["To rename the classes",
                     "To guarantee the order and keep classes that never appear",
                     "To normalise the counts",
                     "It is required for more than two classes"],
         "answer": 1,
         "why": "Without it the classes are inferred and sorted, so a class missing from a split silently shrinks the matrix and code indexing by position reads the wrong cell."},
        {"q": "What does normalize=\"true\" give you on the diagonal?",
         "options": ["Precision per class",
                     "Recall per class",
                     "F1 per class",
                     "Accuracy"],
         "answer": 1,
         "why": "Dividing by row totals gives the proportion of each actual class predicted correctly, which is recall. normalize=\"pred\" divides by column and gives precision."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Scaling features
# ---------------------------------------------------------------------------
topic(
    "scaling_features",
    "Scaling Features",
    "Preparing Data",
    "Which models need it, which are entirely indifferent to it, and the one "
    "rule about when it is allowed to look at your data.",
    _svg(_box(14, 22, 60, 20, S, M) + _txt(44, 36, "1 .. 8000", M, 8) +
         _arrow(78, 32, 92, 32) +
         _box(96, 22, 50, 20, S, A) + _txt(121, 36, "-2 .. 2", A, 8) +
         _txt(80, 62, "mean 0, std 1", M, 8) +
         _txt(80, 76, "fitted on train only", A, 7)),
    [
        ("What StandardScaler learns",
         "Two numbers per column, and the transform is a subtraction and a "
         "division.",
         '''from sklearn.preprocessing import StandardScaler
import numpy as np

X = np.array([[1.0, 2000.0], [2.0, 4000.0], [3.0, 6000.0], [4.0, 8000.0]])

scaler = StandardScaler().fit(X)
Xs = scaler.transform(X)

print("before - column means:", X.mean(axis=0), " stds:", X.std(axis=0))
print("after  - column means:", np.round(Xs.mean(axis=0), 10),
      " stds:", Xs.std(axis=0))
print()
print("learned mean_ :", scaler.mean_)
print("learned scale_:", scaler.scale_)
'''),

        ("What it is worth on a distance-based model",
         "Same data, same model, one line of difference.",
         '''from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)
print("largest feature range is %d times the smallest"
      % int(X.max(axis=0).max() / X.max(axis=0).min()))
print()
raw = cross_val_score(KNeighborsClassifier(), X, y, cv=5)
scaled = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier()),
                         X, y, cv=5)
print("k-NN unscaled:", round(raw.mean(), 4))
print("k-NN scaled  :", round(scaled.mean(), 4))
'''),

        ("Three scalers, one outlier",
         "The choice between them is a choice about what to do with extreme "
         "values.",
         '''from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import numpy as np

X = np.array([[1.0], [2.0], [3.0], [4.0], [100.0]])   # one outlier

for scaler in (StandardScaler(), MinMaxScaler(), RobustScaler()):
    out = scaler.fit_transform(X).ravel()
    print("%-16s %s" % (type(scaler).__name__, np.round(out, 3)))
print()
print("MinMax squashes the four ordinary values into a hundredth of the range.")
print("RobustScaler uses the median and IQR, so they keep a sensible spread")
print("and the outlier is simply far away.")
'''),

        ("Fit on train, transform on both",
         "The test set does not end up centred on zero, and that is the point.",
         '''from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)
X_tr, X_te, _, _ = train_test_split(X, y, test_size=0.3, random_state=0)

scaler = StandardScaler().fit(X_tr)          # training data only

print("train mean after scaling:", round(scaler.transform(X_tr).mean(), 10))
print("test  mean after scaling:", round(scaler.transform(X_te).mean(), 4))
print()
print("the test set is NOT centred on zero, and should not be -")
print("it is transformed with the training set's numbers, not its own.")
'''),

        ("The pipeline does that for you",
         "Which is why scaling and pipelines are taught together and used "
         "together.",
         '''from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression

pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))

print("a pipeline is one estimator:")
print("  steps:", [name for name, _ in pipe.steps])
print()
print("calling pipe.fit(X, y) runs:")
print("  scaler.fit_transform(X)  then  model.fit(scaled, y)")
print("calling pipe.predict(X) runs:")
print("  scaler.transform(X)      then  model.predict(scaled)")
print()
print("which is why the scaler never sees the data it is tested on.")
'''),

        ("Trees do not care at all",
         "One of these two models moves. The other does not move by any amount "
         "at all.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)

for name, model in [("LogisticRegression", LogisticRegression(max_iter=5000)),
                    ("RandomForest", RandomForestClassifier(random_state=0))]:
    raw = cross_val_score(model, X, y, cv=5).mean()
    sca = cross_val_score(make_pipeline(StandardScaler(), model), X, y, cv=5).mean()
    print("%-20s unscaled %.4f   scaled %.4f   change %+.4f"
          % (name, raw, sca, sca - raw))
print()
print("trees split one column at a time, so a monotonic rescaling")
print("cannot change which split they choose.")
'''),
    ],
    [
        "<code class='mono-font'>StandardScaler</code> subtracts the mean and "
        "divides by the standard deviation, learning both from the data it is "
        "fitted on.",
        "Models that measure <strong>distance</strong> or <strong>penalise "
        "coefficients</strong> need it: k-NN, SVM, PCA, k-means, and anything "
        "regularised.",
        "<strong>Trees and their ensembles do not</strong> - they split one "
        "column at a time, so a monotonic rescaling changes nothing.",
        "<code class='mono-font'>MinMaxScaler</code> maps to a fixed range and "
        "is wrecked by outliers; <code class='mono-font'>RobustScaler</code> "
        "uses the median and IQR instead.",
        "Fit the scaler on the <strong>training data only</strong>, then "
        "transform both halves with it - the test set will not be centred, and "
        "should not be.",
        "Put it in a <code class='mono-font'>Pipeline</code> and that rule "
        "becomes impossible to break by accident.",
    ],
    """title: Scaling Features: A Practical Guide
intro: Half the models in the library are seriously damaged by unscaled features and half are fully indifferent. Knowing which is which saves both wasted work and silently bad results.

## What scaling does

Features in a dataset often have different units and different ranges. Age might run from 0 to 100. Income might run from 20,000 to 500,000. A distance-based model like k-nearest neighbours treats both columns equally. Without scaling, the column with the larger numbers dominates every distance calculation.

Scaling puts each column on a comparable range. It does not change the information in the data. It changes the numbers so that no single column drowns out the others by sheer magnitude.

Not every model needs scaling. Tree-based models split on one feature at a time and are unaffected by the scale of the others. Linear models, SVMs and neural networks all benefit from it. Knowing which models need scaling and which do not saves you from both unnecessary work and silent errors.

The most common mistake with scaling is fitting the scaler on the full dataset before splitting. The scaler then learns the mean and standard deviation of the test rows, and the test score is no longer honest. The scaler must be fitted on the training set only. A pipeline handles this automatically.

This page covers what the standard scaler does, why some models need it, and how to apply it without leaking information across the train-test boundary.

`StandardScaler` learns two numbers per column. The mean and the standard deviation. And transforms by subtracting the first and cutting by the second. The result has mean 0 and standard deviation 1 in each column.

That is the entire op. The shape of the spread is unchanged. A skewed column stays skewed, outliers stay outliers. The scaled spots of each value are preserved just. Scaling moves and stretches. It doesn't reshape.

The learned numbers live in `mean_` and `scale_`. This Is worth knowing because those two arrays are the entire fitted state and the thing that must not be learned from the test data.

## Why some models need it

Two families of method are affected, for two different reasons.

**any of it that measures distance.** k-nearest neighbours, SVMs with an RBF kernel, k-means, PCA. These find how far apart two samples are, often by summing squared differences across features. A column measured in thousands adds thousands of times more to that sum than a column measured in single digits. The distance is in effect decided by whichever feature happens to have the largest units. The model isn't weighing the features by importance. It's weighing them by unit.

The editor above shows the cost: k-NN on the wine dataset scores 0.69 unscaled and 0.95 scaled. That isn't a tuning improvement, it's the difference between a model that works and one that doesn't. It comes from one column being measured in hundreds while others are measured in fractions.

**any of it that punishes coeff size.** Ridge, Lasso, ElasticNet. `LogisticRegression`. This Is smoothed by default. The fine is on the magnitude of the coeffs. A coeff's magnitude depends on its feature's units. Without scaling, the fine falls unevenly across features for reasons that have nothing to do with the data.

There's also a hands-on third reason: grad-based solvers settle faster and more well on scaled features. This Is why unscaled logistic regression makes `ConvergenceWarning`.

## Why some models do not

Tree-based models &mdash; choice trees, random forests, grad boosting &mdash; are fully unaffected. The reason is structural rather than rough.

A tree splits on one feature at a time, asking whether a value is above or below a threshold. Rescaling a column monotonically moves the threshold by the same change and leaves the sorting of each sample the same. Just the same split is chosen. The tree that results is the same tree.

The editor above measures it: the random forest changes by `+0.0000`. Not "a little". Not at all.

This matters in practice because scaling a tree model is harmless but pointless. Adding a scaler to a pipeline that ends in a forest is a step that costs time and clarity for no gain. It matters more because people who have learned "always scale" at times conclude that trees must so be doing a thing odd, when this is one of the reasons trees are so convenient on messy tabular data: they need no preparation at all.

## Choosing between the scalers

`StandardScaler` is the default and the right answer most of the time. It assumes nothing about the range and handles roughly even data well.

`MinMaxScaler` maps each column onto a fixed range, often 0 to 1. It's the choice when an method needs bounded input. Its weakness is severe. A single outlier defines the range and compresses all else against the opposite end. The editor above shows four plain values landing in the first hundredth of the range because one value is 100.

`RobustScaler` centres on the median and cuts by the interquartile range. Because both statistics skip the tails, extreme values don't distort the change of the plain ones. In the same demo, the four normal values keep a sensible spread and the outlier simply sits far away. It's the right default when the data has outliers you don't want to drop.

`MaxAbsScaler` cuts by the largest abs value and preserves zeros. This Makes it the one to use on sparse data where centring would destroy the sparsity.

`Normalizer` is the odd one out and a frequent source of confusion. It scales each **row** to unit length rather than each column. It's for making samples close in direction rather than magnitude. Text vectors, mostly. And isn't a substitute for the column scalers.

## The rule that makes it honest

The scaler must be fitted on the training data only. Then used to transform both halves.

The reason is the same as all over else in this track: `mean_` and `scale_` are learned from data. A scaler fitted on all has seen the test set. The score afterwards isn't a score on unseen data.

The consequence surprises people the first time. After scaling right, the **test set isn't centred on zero**. Its mean is what it happens to be scaled to the training spread. The editor above shows 0.0184 rather than 0. That is correct and it's the whole point. The test data is being put through just the change that new data would go through in production. Here You don't get to recompute the mean using the future.

A test set that comes out just right centred is evidence that the scaler was fitted on it. This Means the test is compromised.

The same logic extends to deployment. The scaler is part of the model and has to be saved with it. A model deployed without its scaler, receiving raw features, will give confident nonsense. Which is one more arg for the pipeline. Saving the pipeline saves both.

## Just use a pipeline

each rule above is enforced automatically by putting the scaler in a `Pipeline`.

A pipeline is a single estimator. Its `fit` runs `fit_transform` on each transformer and then `fit` on the final model. Its `predict` runs `transform` and then `predict`. So inside a cross-validation loop, the scaler is refitted on each training fold and the held-out fold is only ever transformed. Which is just the correct action, reached without you having to note it.

`make_pipeline(StandardScaler(), LogisticRegression())` is two words longer than fitting the scaler by hand and drops an entire category of mistake. There's no situation in which scaling outside a pipeline is preferable. The habit is worth forming before the mistakes are.

## Scaling is not the only transformation a column might want

Standardising fixes the *scale* of a feature and leaves its *shape* alone. at times the shape is the problem.

A heavily skewed column &mdash; incomes, groups, response times, any of it where a few values are orders of magnitude above the rest &mdash; stays heavily skewed after standardising. The mean and standard deviation are themselves distorted by the tail. Most of the data ends up squeezed just below zero with a few huge values above it. This Is just the situation that harmed the distance-based models in the first place.

Three responses. A **log transform**, via `FunctionTransformer(np.log1p)`, compresses the tail and often turns a multiplicative tie into an additive one that a linear model can fit. `log1p` rather than `log` because it handles zeros without making minus infinity.

`PowerTransformer` finds a change that makes the column as close to normal as it can. Standardises as it goes. It handles the choice for you and is the reasonable default when you know a column is skewed and don't want to think about which change.

`QuantileTransformer` maps the column onto a uniform or normal spread by rank. It's the most aggressive of the three. It will norm any of it, at the cost of discarding the actual spacing between values and of behaving unpredictably on values outside the training range.

All three are transformers with the usual `fit`/`transform`. They go in a pipeline in the same place a scaler would. They're subject to just the same training-data-only rule.

## The order of the steps

When a few changes apply to the same column, the order isn't any.

Imputation comes before scaling, because a scaler can't find a mean over missing values. It raises. Encoding comes before scaling for the same reason. A scaler can't subtract a mean from a string.

Skew correction comes before standardising, since the point is to fix the shape and then fix the location and spread of the fixed shape.

Feature pick is often last among the transformers and before the model. That the pick sees the features in the form the model will.

A `Pipeline` executes its steps in the order given. Writing them in the wrong order makes either an error or a silently worse model. The sequence that covers most cases is: impute, encode, transform skew, scale, select, fit.

<strong>Should I scale the target as well?</strong> Rarely for regression - it changes the units your errors are reported in. When it truly helps, `TransformedTargetRegressor` does it and inverts the change on `predict`. The guesses come back in the first units.

<strong>Does scaling help fit on trees, ever?</strong> No. just zero. This The last editor shows. It's harmless and pointless.

<strong>What about one-hot columns - do those get scaled?</strong> They're already 0 and 1. Standardising them mostly adds noise to the reading. It's common to scale only the numeric columns. This Is what a `ColumnTransformer` is for.

## Categories of model, and what each one wants

A summary worth keeping, because "does this need scaling" comes up for each new estimator.

**Needs it, badly.** k-nearest neighbours, k-means, SVM with any kernel, PCA and any of it built on it. Neural networks. All of these either measure distance or descend a grad. Both are dominated by whichever feature has the largest units.

**Needs it, for the fine.** Ridge, Lasso, ElasticNet. `LogisticRegression` with its default L2. The fit itself would be unaffected. The smoothing punishes coeff magnitude, and magnitude depends on units.

**Doesn't need it, and gains nothing.** choice trees, random forests, extra trees, grad boosting in all its varieties, and naive Bayes. These either split one column at a time or treat the columns on its own.

**Doesn't need it, but settles faster with it.** Plain `LinearRegression` has a closed-form answer and is truly indifferent. The iterative solvers used for very large problems aren't.

The rule that covers the whole table: if the method ever adds two different features together, checks them, or measures a distance across them, it needs them on a common scale. If it only ever looks at one feature at a time, it doesn't.

## Things to try

1. <strong>Run the second editor.</strong> 0.69 against 0.95, from one line. That is the arg in a single number.
2. <strong>Watch a tree skip it.</strong> The last editor reports a change of just zero for the forest. Try `MinMaxScaler` instead and confirm it's still zero.
3. <strong>Break the range.</strong> In the third editor, change the outlier to 10000 and see how much further MinMax compresses the plain values.
4. <strong>Cheat on purpose.</strong> In the fourth editor, fit the scaler on all of `X` and note that the test mean turns 0 - the signature of a compromised test.

## Where this leaves you

Scale for distance-based and smoothed models, don't bother for trees, prefer `StandardScaler` unless outliers argue for `RobustScaler`. Fit it inside a pipeline so that the training-data-only rule holds without anyone having to note it.
""",
    [
        {"q": "Which of these is unaffected by feature scaling?",
         "options": ["k-nearest neighbours", "Random forest", "SVM with an RBF kernel", "Ridge regression"],
         "answer": 1,
         "why": "Trees split one column at a time on a threshold, and a monotonic rescaling moves the threshold identically. The measured change is exactly zero."},
        {"q": "After scaling correctly, what should the test set's mean be?",
         "options": ["Exactly zero",
                     "Whatever it happens to be - it is transformed with the training set's numbers",
                     "One",
                     "The same as the training mean"],
         "answer": 1,
         "why": "A test set that comes out perfectly centred is evidence the scaler was fitted on it, which compromises the evaluation."},
        {"q": "Why prefer RobustScaler when the data has outliers?",
         "options": ["It removes the outliers",
                     "It centres on the median and divides by the IQR, so extreme values do not distort the rest",
                     "It is faster",
                     "It bounds the output to 0-1"],
         "answer": 1,
         "why": "Median and IQR ignore the tails. MinMaxScaler does the opposite - one outlier defines the range and compresses everything else."},
        {"q": "What does Normalizer do?",
         "options": ["Scales each column to mean 0",
                     "Scales each row to unit length",
                     "Removes outliers",
                     "Maps every column to 0-1"],
         "answer": 1,
         "why": "It works on rows rather than columns, making samples comparable in direction rather than magnitude. It is not a substitute for the column scalers."},
    ],
)


# ---------------------------------------------------------------------------
# 11. Encoding categorical features
# ---------------------------------------------------------------------------
topic(
    "encoding_categoricals",
    "Encoding Categories",
    "Preparing Data",
    "Text columns have to become numbers, and the obvious way of doing it "
    "invents an ordering that is not there.",
    _svg(_box(12, 22, 46, 20, S, M) + _txt(35, 36, "paris", M, 8) +
         _arrow(62, 32, 76, 32) +
         _box(80, 22, 22, 20, S, B) + _txt(91, 36, "0", M, 8) +
         _box(102, 22, 22, 20, S, A) + _txt(113, 36, "1", A, 8) +
         _box(124, 22, 22, 20, S, B) + _txt(135, 36, "0", M, 8) +
         _txt(80, 62, "one column per category", M, 7)),
    [
        ("One column per category",
         "The safe default, and the names it generates.",
         '''from sklearn.preprocessing import OneHotEncoder
import pandas as pd

df = pd.DataFrame({"city": ["london", "paris", "london", "berlin"]})

enc = OneHotEncoder(sparse_output=False)
out = enc.fit_transform(df[["city"]])

print("learned categories:", enc.categories_[0].tolist())
print("column names      :", list(enc.get_feature_names_out()))
print()
print(pd.DataFrame(out, columns=enc.get_feature_names_out()).astype(int))
'''),

        ("The category it has never seen",
         "The default raises. Which of the two behaviours you want is a real "
         "decision.",
         '''from sklearn.preprocessing import OneHotEncoder
import pandas as pd

train = pd.DataFrame({"city": ["london", "paris"]})
new = pd.DataFrame({"city": ["london", "tokyo"]})

strict = OneHotEncoder(sparse_output=False).fit(train[["city"]])
try:
    strict.transform(new[["city"]])
except ValueError as e:
    print("default:", str(e).split("\\n")[0][:90])

print()
safe = OneHotEncoder(sparse_output=False, handle_unknown="ignore").fit(train[["city"]])
print("handle_unknown='ignore' gives all zeros for the unseen value:")
print(safe.transform(new[["city"]]).astype(int))
'''),

        ("Ordinal encoding invents an order",
         "Left to itself it uses alphabetical order, which here makes small "
         "the largest.",
         '''from sklearn.preprocessing import OrdinalEncoder
import pandas as pd

df = pd.DataFrame({"size": ["small", "large", "medium", "small"]})

# Wrong: alphabetical order has no meaning here.
auto = OrdinalEncoder().fit(df[["size"]])
print("default (alphabetical):", auto.categories_[0].tolist())
print("           encoded as:",
      auto.transform(df[["size"]]).ravel().astype(int).tolist())

print()
order = [["small", "medium", "large"]]
told = OrdinalEncoder(categories=order).fit(df[["size"]])
print("with categories= given:", told.categories_[0].tolist())
print("           encoded as:",
      told.transform(df[["size"]]).ravel().astype(int).tolist())
'''),

        ("drop='first', and when it matters",
         "Two columns for a yes/no answer carry the information of one.",
         '''from sklearn.preprocessing import OneHotEncoder
import pandas as pd

df = pd.DataFrame({"answer": ["yes", "no", "yes"]})

full = OneHotEncoder(sparse_output=False).fit(df[["answer"]])
dropped = OneHotEncoder(sparse_output=False, drop="first").fit(df[["answer"]])

print("all columns :", list(full.get_feature_names_out()))
print(full.transform(df[["answer"]]).astype(int))
print()
print("drop='first':", list(dropped.get_feature_names_out()))
print(dropped.transform(df[["answer"]]).astype(int))
print()
print("the dropped column carried no information the other did not:")
print("'not no' and 'yes' are the same statement.")
'''),

        ("What high cardinality does to the matrix",
         "Three cities is three columns. Sixteen hundred users is sixteen "
         "hundred.",
         '''from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

rng = np.random.RandomState(0)
ids = ["user_%04d" % i for i in rng.randint(0, 5000, size=2000)]
df = pd.DataFrame({"user": ids, "city": rng.choice(["a", "b", "c"], 2000)})

for col in ("city", "user"):
    enc = OneHotEncoder(sparse_output=False).fit(df[[col]])
    print("%-6s %5d distinct -> %5d columns"
          % (col, df[col].nunique(), enc.transform(df[[col]]).shape[1]))
print()
print("one-hot encoding a high-cardinality column produces a matrix")
print("that is almost entirely zeros, and a model that memorises ids.")
'''),

        ("Encoding belongs inside the pipeline",
         "The label here is the city, so a perfect score is expected - the "
         "point is that the folds do not crash.",
         '''from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
import pandas as pd
import numpy as np

rng = np.random.RandomState(0)
n = 400
city = rng.choice(["london", "paris", "berlin"], n)
y = (city == "paris").astype(int)        # the answer IS the city
X = pd.DataFrame({"city": city})

pipe = make_pipeline(
    OneHotEncoder(handle_unknown="ignore"),
    LogisticRegression(max_iter=1000))

print("cross-validated accuracy:", round(cross_val_score(pipe, X, y, cv=5).mean(), 4))
print("(1.0 by construction - the task is trivial on purpose)")
print()
print("the encoder is refitted inside each fold, so a category that")
print("appears only in the held-out part is handled, not crashed on.")
'''),
    ],
    [
        "<code class='mono-font'>OneHotEncoder</code> makes one column per "
        "category and is the safe default for <strong>nominal</strong> data - "
        "categories with no order.",
        "<code class='mono-font'>OrdinalEncoder</code> maps categories to "
        "integers, which implies an ordering; use it only when one genuinely "
        "exists, and pass <code class='mono-font'>categories=</code> to say "
        "what it is.",
        "<code class='mono-font'>handle_unknown=\"ignore\"</code> encodes an "
        "unseen category as all zeros instead of raising - almost always what "
        "you want in production.",
        "<code class='mono-font'>get_feature_names_out()</code> recovers the "
        "invented column names, which is how feature importances stay readable.",
        "High-cardinality columns explode into thousands of near-empty columns; "
        "group the rare values or use a different encoding.",
        "<code class='mono-font'>LabelEncoder</code> is for the "
        "<strong>target</strong>, not for features - it accepts only 1-D input.",
    ],
    """title: Encoding Categories: A Practical Guide
intro: each estimator in scikit-learn takes numbers. Turning "london" into a number is easy. Doing it without inventing a fact that isn't in the data takes one choice.

## Why it cannot be skipped

Real-world data almost always contains categorical columns. City names, product types, colour labels, yes/no flags. These columns carry useful information, but scikit-learn cannot accept strings as input. Every column must be numeric before it reaches `fit`.

There are several ways to turn a category into a number. Each one makes a different claim about the data. Setting London=0, Paris=1, Berlin=2 says there is an order. One-hot encoding avoids that by making a new binary column for each category.

The wrong encoding does not raise an error. It runs and gives a model false data. A linear model trained on ordinal city names will treat Berlin as twice Paris. That is nonsense, and the model has no way to know it.

The right choice depends on the column and the model. Ordinal encoding is right for groups that have a real order, like size. One-hot is right for groups with no order. Target encoding helps when there are many groups and one-hot would make too many columns.

This page covers each encoding, the mistakes each one stops, and how to put them in a pipeline. It also covers the `drop` setting in one-hot encoding and why it matters for linear models.

scikit-learn's estimators operate on numeric arrays. A column of strings raises rather than being converted automatically. The error. `couldn't convert string to float`. Is one of the first anyone meets on real data.

The conversion isn't mechanical, because there's more than one way to do it and they encode different claims about the data. Getting it wrong doesn't raise. It makes a model that has been told a thing false.

## The mistake to avoid

The obvious approach is to number the categories. London 0, paris 1, berlin 2. It's one line and it's wrong for most cat columns.

Numbering asserts an **order** and a **spacing**. It says berlin is greater than paris, that paris sits just between london and berlin. That the distance from london to berlin is twice the distance from london to paris. None of that is true of cities. A model that finds with those numbers will use each one of those false ties.

For a linear model the damage is direct. A single coeff is fitted for the column. The model can only express "more city is more target". This Is meaningless. For a distance-based model, berlin and london are found as far apart while london and paris are close. For a tree the damage is milder. A tree can split the numbers into groups and in part recover. But it still has to spend splits undoing an sorting that was invented.

## One-hot encoding

The safe answer is one column per category, each holding 1 when the row is that category and 0 or else.

No sorting is implied, because no two categories share a column. Each gets its own coeff in a linear model. The model can learn that paris raises the target and berlin lowers it. This Numbering could never express.

`OneHotEncoder` learns the categories during `fit` and stores them in `categories_`, sorted. `get_feature_names_out()` returns the made names. `city_london`, `city_paris`. Which is what keeps coeffs and feature importances readable after the change.

By default it returns a sparse mat. With many categories almost each entry is zero. `sparse_output=False` gives a dense array. This Is convenient for looking at and a bad idea when the number of categories is large.

## The unseen category

The most key arg on the encoder is `handle_unknown`. The default is the strict one.

A category present at guess time but absent during training raises `ValueError` by default. That is the right action while you're developing. It tells you the data has changed. And often the wrong action in production. Here A new city appearing shouldn't take the service down.

`handle_unknown="skip"` codes the unknown value as all zeros. Not any of the known categories. This Is an honest form of "a thing I haven't seen". The model then predicts from the left features.

This matters inside cross-validation too. Each fold refits the encoder on its own training part. A category appearing only in the held-out fold is unknown to that fold's encoder. Without `handle_unknown="skip"`, cross-validation on a dataset with rare categories crashes on whichever fold happens to isolate one.

`min_frequency` and `max_categories`, added more recently, are the built-in answer to the same problem from the other end. They fold rare categories into a single "infrequent" column during fitting. The rare values are handled by design rather than by exception.

## When ordering is real

Some categories truly are sorted. Small, medium, large. Bronze, silver, gold. Disagree, neutral, agree. Here an int encoding isn't a lie. It's better than one-hot because it lets the model use the sorting with a single coeff instead of learning three free ones.

`OrdinalEncoder` does it &mdash; and left to itself it sorts alphabetically. This Is almost never the order you meant. The editor above shows the damage. With small, medium and large, alphabetical order makes large 0, medium 1, small 2. The encoding says small is the biggest.

`categories=[["small", "medium", "large"]]` states the order by name. Passing it isn't optional. The list is nested because the encoder handles a few columns at once, one list per column.

The test for whether a column is ordinal. Is there a defensible answer to "which is bigger". Is the gap between back to back values roughly close? Sizes pass the first and often fail the second. This Is why ordinal encoding of survey scales is common and mildly wrong.

## drop, and the collinearity question

With `k` categories, one-hot makes `k` columns of which any one is found by the others. If it isn't london and not paris, it's berlin. That redundancy is called collinearity.

`drop="first"` drops one column per feature. For a plain linear regression this matters. With an intercept, just right collinear columns make the answer non-unique and the single coeffs unstable. For any of it smoothed. Ridge, Lasso, `LogisticRegression` with its default fine. It doesn't. The fine resolves the ambiguity. Dropping a column makes the left coeffs harder to read since they become scaled to the dropped baseline.

`drop="if_binary"` is the sensible middle: it drops the redundant column only for two-category features. Here Two columns are obviously one too many, and leaves multi-category features alone.

For trees, dropping is actively unhelpful. It drops a column the tree might have split on and gains nothing.

## High cardinality

One-hot encoding a column with thousands of distinct values makes thousands of columns, almost all zero. The editor above shows 1639 distinct user ids turning 1639 columns.

Three problems follow. The mat turns huge and mostly empty. Most columns are 1 for only a handful of rows. Any coeff fitted to them is fitted to almost no data. And the model can store single ids. This Looks like skill on the training data and is worthless on anyone new.

Three responses, in growing order of effort. **Group the rare values** into an "other" category. This `min_frequency` does for you. **Encode a thing about the category rather than its identity**. For a postcode, the region. For a product, its price band. Or **target encoding**, replacing each category with the mean target for that category. This Is compact and powerfully prone to leakage. Found dataset it tells the model the answer. It must be found inside the folds, which is what `TargetEncoder` handles.

The question worth asking first is whether the column belongs in the model at all. A user id often carries no generalisable info. What you want is what the user *did*.

## LabelEncoder is not for this

`LabelEncoder` appears in a great deal of example code applied to feature columns. It's documented for encoding the **target**.

It accepts only 1-D input. So Using it on features means looping over columns and applying it one at a time. That works, makes an ordinal encoding with all the problems above, and. The real objection. It has no `handle_unknown`, so a new category at guess time raises with no option to do or else.

Use `OrdinalEncoder` for sorted features, `OneHotEncoder` for unordered ones. `LabelEncoder` only when converting string class labels into ints for `y`. This Most estimators don't even need.

## Categories that arrive as numbers

The hardest cat columns to spot are the ones already stored as ints. Nothing raises and nothing looks wrong.

A postcode district, a product code, a department id, a day-of-week stored as 0 to 6, a survey answer coded 1 to 5. Each is a category wearing a number. A model handed it raw will treat department 7 as greater than department 3 and just twice department 3.5.

Nothing in the data announces this. The column is numeric, the estimator accepts it, the fit succeeds. The model quietly uses an sorting that means nothing. It's the mirror image of the ordinal mistake. There, an order was invented where none existed. Here, an order that happens to exist in the encoding is mistaken for one that exists in the world.

The check is to ask what the math would mean. If the mean of two values is meaningless. The mean of department 2 and department 8. The column is cat even so of its dtype. If it's real, as with an age or a price, it's truly numeric.

Day-of-week is the notable middle case. It has an order, the gaps are equal. It wraps around: Sunday is adjacent to Monday. This No int encoding captures. The usual fix is a pair of features, the sine and cosine of the angle around the week. This Makes the wrap-around clear and is the standard trick for any cyclical quantity. Hours, months, compass bearings.

## Reading the model afterwards

One-hot encoding times the columns, and a fitted model reports one number per column. Keeping the two aligned is what makes the result readable.

`get_feature_names_out()` on the encoder returns the made names in order. On a `Pipeline` or `ColumnTransformer` it returns the names for all the whole chain made. Zipping that against `coef_` or `feature_importances_` gives a labelled result rather than an array of numbers whose spots you've to rebuild.

Two things to note when reading them. The importance of a category is spread across its columns. A feature with twenty categories has its sway cut twenty ways and will look weaker than a single numeric column carrying the same info. Which is a known bias in tree-based feature importances, not a fact about the data. And with `drop="first"`, each left coeff is scaled to the dropped category. So A plus coeff means "higher than the baseline", not "high".

<strong>Do trees need one-hot encoding?</strong> scikit-learn's do. They can't take strings. `HistGradientBoostingClassifier` accepts declared cat features natively. This Is both faster and better than one-hot for high-cardinality columns.

<strong>Should I one-hot encode before or after splitting?</strong> After. Inside a pipeline - or else the encoder learns the category list from the test rows too.

<strong>What about missing values in a cat column?</strong> `OneHotEncoder` treats `NaN` as its own category by default. This Is often the right action: "not stated" is often helpful rather than merely absent.

## Things to try

1. <strong>Read the alphabetical disaster.</strong> The third editor codes small as 2 and large as 0. Look at the numbers before reading the fix.
2. <strong>Meet the unknown category.</strong> In the second editor, drop `handle_unknown="skip"` from the safe encoder and watch it raise on tokyo.
3. <strong>Explode a column.</strong> In the fifth editor, raise the number of distinct users and watch the column count follow it just.
4. <strong>Group the rare ones.</strong> Add `min_frequency=50` to that encoder and see how many columns live.

## Where this leaves you

One-hot for unordered categories with `handle_unknown="skip"`, ordinal with an clear `categories=` when the order is real, `drop="if_binary"` as a reasonable default. A plan for any column with more than a few dozen distinct values before it turns a few dozen columns of nearly nothing.
""",
    [
        {"q": "Why is numbering cities 0, 1, 2 a problem?",
         "options": ["It is slower",
                     "It asserts an order and spacing that do not exist",
                     "scikit-learn rejects it",
                     "It uses more memory"],
         "answer": 1,
         "why": "The numbers claim berlin > paris > london and that the gaps are equal. A linear model fits one coefficient to that invented scale."},
        {"q": "What does handle_unknown=\"ignore\" do?",
         "options": ["Drops the row",
                     "Encodes an unseen category as all zeros",
                     "Adds a new column",
                     "Raises a warning and continues"],
         "answer": 1,
         "why": "All zeros honestly represents \"none of the categories I know\". Without it, cross-validation crashes on any fold that isolates a rare category."},
        {"q": "When is OrdinalEncoder the right choice?",
         "options": ["Always - it is more compact",
                     "When the categories have a genuine order, and you pass categories= to state it",
                     "Only for the target",
                     "When there are more than 100 categories"],
         "answer": 1,
         "why": "Left to itself it sorts alphabetically, which turned small into 2 and large into 0 in the editor above."},
        {"q": "What is LabelEncoder for?",
         "options": ["Encoding feature columns",
                     "Encoding the target",
                     "One-hot encoding",
                     "Handling unknown categories"],
         "answer": 1,
         "why": "It takes only 1-D input and has no handle_unknown, so applying it to features gives an ordinal encoding that raises on any new category."},
    ],
)


# ---------------------------------------------------------------------------
# 12. Pipelines
# ---------------------------------------------------------------------------
topic(
    "pipelines",
    "Pipelines in scikit-learn",
    "Preparing Data",
    "One object holding every step, so that what is fitted on the training "
    "fold stays fitted on the training fold - by construction rather than by "
    "discipline.",
    _svg(_box(10, 30, 34, 26, S, M) + _txt(27, 47, "impute", M, 7) +
         _arrow(46, 43, 54, 43) +
         _box(56, 30, 34, 26, S, M) + _txt(73, 47, "scale", M, 7) +
         _arrow(92, 43, 100, 43) +
         _box(102, 30, 44, 26, S, A) + _txt(124, 47, "model", A, 7) +
         _txt(80, 74, "one fit(), one predict()", M, 7)),
    [
        ("Two ways to build one",
         "The same object; the difference is whether you choose the step names.",
         '''from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

auto = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
named = Pipeline([("scale", StandardScaler()),
                  ("clf", LogisticRegression(max_iter=1000))])

print("make_pipeline names them for you:", [n for n, _ in auto.steps])
print("Pipeline lets you choose        :", [n for n, _ in named.steps])
print()
print("both are a single estimator with fit / predict / score")
print("has fit?", hasattr(auto, "fit"), " has predict?", hasattr(auto, "predict"))
'''),

        ("Reaching inside a fitted pipeline",
         "The steps are still there, fitted, and gettable three different ways.",
         '''from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X, y)

scaler = pipe.named_steps["standardscaler"]
model = pipe.named_steps["logisticregression"]

print("the fitted scaler's first three means:", scaler.mean_[:3].round(3))
print("the fitted model's shape             :", model.coef_.shape)
print()
print("pipe[-1] is the last step:", type(pipe[-1]).__name__)
print("pipe[0]  is the first    :", type(pipe[0]).__name__)
'''),

        ("Three steps, refitted inside every fold",
         "Imputation and scaling both learn from data, and both are inside.",
         '''from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_wine
import numpy as np

X, y = load_wine(return_X_y=True)
X = X.copy()
rng = np.random.RandomState(0)
X[rng.rand(*X.shape) < 0.1] = np.nan          # 10% missing

pipe = make_pipeline(SimpleImputer(strategy="median"),
                     StandardScaler(),
                     LogisticRegression(max_iter=1000))

print("three steps, one call:", [n for n, _ in pipe.steps])
print("cross-validated accuracy:", round(cross_val_score(pipe, X, y, cv=5).mean(), 4))
print()
print("the imputer's medians and the scaler's means are both")
print("recomputed on the training part of every fold.")
'''),

        ("Tuning a parameter inside a step",
         "Two underscores between the step name and the parameter, and a search "
         "can reach anything.",
         '''from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)

pipe = Pipeline([("scale", StandardScaler()),
                 ("clf", LogisticRegression(max_iter=5000))])

# stepname__parameter - two underscores
grid = {"clf__C": [0.01, 0.1, 1, 10],
        "scale__with_mean": [True, False]}

search = GridSearchCV(pipe, grid, cv=5).fit(X, y)
print("best parameters:", search.best_params_)
print("best score     :", round(search.best_score_, 4))
print()
print("the double underscore reaches into a step:")
print("  clf__C  means  the C of the step named clf")
'''),

        ("Saving the whole thing",
         "The preprocessing is part of the model, so it has to travel with it.",
         '''from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
import pickle

X, y = load_wine(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

pipe = make_pipeline(StandardScaler(),
                     LogisticRegression(max_iter=1000)).fit(X_tr, y_tr)

blob = pickle.dumps(pipe)
restored = pickle.loads(blob)

print("saved bytes:", len(blob))
print("same predictions after a round trip:",
      (restored.predict(X_te) == pipe.predict(X_te)).all())
print()
print("the scaler travels with the model, which is the point -")
print("a model saved without it would receive raw features and be wrong.")
'''),

        ("Switching a step off",
         "'passthrough' turns a step into a no-op, which makes the step itself "
         "something a search can choose.",
         '''from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_wine
from sklearn.model_selection import cross_val_score

X, y = load_wine(return_X_y=True)

pipe = Pipeline([("scale", StandardScaler()),
                 ("pca", PCA(n_components=5)),
                 ("clf", LogisticRegression(max_iter=1000))])

print("with PCA   :", round(cross_val_score(pipe, X, y, cv=5).mean(), 4))

pipe.set_params(pca="passthrough")
print("passthrough:", round(cross_val_score(pipe, X, y, cv=5).mean(), 4))
print()
print("'passthrough' disables a step without rebuilding the pipeline,")
print("which is how a search can treat a whole step as a hyperparameter.")
'''),
    ],
    [
        "A pipeline <strong>is an estimator</strong>: it has "
        "<code class='mono-font'>fit</code>, "
        "<code class='mono-font'>predict</code> and "
        "<code class='mono-font'>score</code>, and goes anywhere one goes.",
        "<code class='mono-font'>fit</code> calls "
        "<code class='mono-font'>fit_transform</code> on each step and "
        "<code class='mono-font'>fit</code> on the last; "
        "<code class='mono-font'>predict</code> calls only "
        "<code class='mono-font'>transform</code>.",
        "That asymmetry is the whole point - the held-out fold is transformed, "
        "never fitted on.",
        "<code class='mono-font'>make_pipeline</code> names the steps after "
        "their classes; <code class='mono-font'>Pipeline</code> lets you name "
        "them, which makes the search grid readable.",
        "<code class='mono-font'>step__parameter</code>, with two underscores, "
        "is how a search reaches a setting inside a step.",
        "Pickle the pipeline, not the model - a model deployed without its "
        "preprocessing gets raw features and is confidently wrong.",
    ],
    """title: Pipelines: A Practical Guide
intro: A pipeline isn't a convenience. It's the mechanism that makes each score in this track honest. Using one turns a rule you've to note into a property of the code.

## What it is

Most machine-learning workflows have several preprocessing steps before the model. Imputing missing values, encoding categories, scaling features. Without a pipeline, each step is a separate call. Each call must be applied in the right order, to the right data, at the right time. Mistakes in that sequence are common and hard to spot.

A pipeline bundles those steps into a single object. It applies them in order during `fit` and again during `predict`. Because the whole sequence is one object, it can be passed to `cross_val_score`, `GridSearchCV` or any other tool that expects an estimator. The preprocessing runs inside the cross-validation loop, which is the only way to get an honest score.

The alternative -- scaling the full dataset, then splitting, then fitting -- leaks information from the test set into the training set. That leak inflates the score. A pipeline prevents it by design. Each fold sees only the training rows during `fit_transform` and applies the learned transformation to the test rows during `transform`.

Pipelines also make deployment simpler. You save one object that contains both the preprocessing and the model. At prediction time, you call `predict` on the pipeline and it handles every step. There is no risk of forgetting to scale or encode at serving time.

This page covers building a pipeline, inspecting its steps, and combining it with a column transformer for mixed-type data. It also covers the `make_pipeline` shortcut and the `set_output` method that preserves DataFrame column names.

A `Pipeline` chains transformers together and ends with an estimator. The result behaves as a single estimator.

That last sentence is the key one. A pipeline has `fit`, `predict` and `score`. Anywhere a model can go. `cross_val_score`, `GridSearchCV`, a pickle file, a check loop. A whole pipeline can go instead, with no changes to the nearby code.

What it does inside is straightforward. `fit` calls `fit_transform` on each step in turn, passing the output of one to the next. `fit` on the final estimator. `predict` calls only `transform` on each step, then `predict` on the last.

## The asymmetry is the point

Look again at those two sentences: `fit` **fits** the transformers. `predict` only **transforms**.

That skew is what makes a pipeline more than plumbing. Inside a cross-validation loop, `fit` is called on the training folds. So the scaler finds its mean there, the imputer its median, the encoder its category list. Then `predict` runs on the held-out fold. This Is transformed using those numbers and never adds to them.

Doing the same thing by hand means remembering, each time, to fit each transformer on the training part only. To apply it to the test part without refitting. That is four or five opportunities per test to make a mistake that inflates the score and makes no error.

The cross-validation module measured what that mistake costs. Feature pick applied outside the folds reported 0.825 fit on data that was pure noise. A pipeline makes that given mistake hopeless to write.

## Two constructors

`make_pipeline(StandardScaler(), LogisticRegression())` names the steps automatically, lowercasing the class names. It's shorter and right for quick work.

`Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression())])` lets you name them. The names matter once you're tuning. They appear in each param key: `clf__C` is far more readable than `logisticregression__C`. It doesn't change if you swap the classifier for a different one.

The rule of thumb: `make_pipeline` while exploring, `Pipeline` with short names once there's a search grid.

each step except the last must be a transformer. It must have `transform`. The last can be any of it, including another transformer if the pipeline's purpose is prep rather than guess.

## Getting at the fitted parts

A fitted pipeline still holds its fitted steps, and there are three ways in.

`pipe.named_steps["scale"]` uses the name. `pipe["scale"]` is the shorter form of the same thing. `pipe[0]` and `pipe[-1]` index by spot. `pipe[-1]` for the final estimator is the one you'll write most.

This is how you read `coef_` off the model at the end, or check what the scaler learned, or pull `get_feature_names_out()` from an encoder in the middle. The pipeline hides nothing. It only changes how you reach it.

`pipe[:-1]` slices, returning a new pipeline of all except the last step. At times handy for inspecting what the model really receives.

## Tuning through a pipeline

Settings inside a pipeline are handled as `stepname__parameter`, with **two** underscores.

`{"clf__C": [0.01, 0.1, 1]}` tunes `C` on the step named `clf`. Nesting goes deeper with more underscores. A param inside a step inside a column transformer is `preprocess__num__imputer__strategy`. Which looks unwieldy and is fully mechanical.

The consequence worth appreciating: a search can tune the **prep** and the model. Whether to scale with the mean. This Imputation strategy to use, how many PCA components to keep. How the model is configured, all in one grid, all tested with the same honest cross-validation.

`"passthrough"` extends this to whole steps. Setting a step to that string makes it a no-op. `{"pca": ["passthrough", PCA(5), PCA(10)]}` treats the existence of the PCA step as itself a setting. The same trick lets a search choose between two fully different models in one grid.

## Deployment is where it pays off

A model without its prep isn't a model.

Saving only the estimator and applying scaling by hand at guess time means reimplementing the change a place else, with the numbers copied across. Keeping the two in step forever. each one of those is a place for the training and serving paths to diverge. And when they do, nothing raises. The model receives features on a different scale from the ones it was fitted on and makes confident nonsense.

Pickling the pipeline saves the transformers and their learned params alongside the model. The object that comes back does the whole job from raw features to guess. The editor above round-trips one and confirms the guesses are the same.

Two cautions on pickles that apply to any scikit-learn object. They aren't a secure format. Unpickling untrusted data executes code. And they aren't portable across versions. A pipeline pickled with one scikit-learn and loaded with another may fail or, worse, behave differently. Recording the version alongside the file is the min. `skops` is the option for any of it that has to be shared.

## When not to reach for one

Pipelines handle a sequence of steps applied to all the columns. Two situations need a thing else.

**Different steps for different columns**. Scaling the numeric ones and encoding the cat ones &mdash; is what `ColumnTransformer` is for. It slots into a pipeline as a single step.

**any of it that changes the number of rows.** Dropping outliers, resampling for imbalance, aggregating. Pipelines transform features and pass the target through untouched. A step that removed rows would leave `X` and `y` out of step. The `imbalanced-learn` package gives its own pipeline for just this case. Row-level filtering or else belongs before the pipeline, applied to the training data only.

## Caching, when the fitting gets slow

A grid search over a pipeline refits each step for each combination. Most of that work is repeated. Tuning only the classifier means the scaler and the imputer are refitted the same way for each pick. This Is wasted time on any of it costly.

`Pipeline(steps, memory="./cache")` caches the fitted transformers, keyed on the step and the data they were given. The first combination pays for the prep. The rest reuse it. On a pipeline whose costly part is the prep. Text vectorisation, a costly feature build. This can be the difference between a search that finishes and one that doesn't.

Two caveats. The cache is on disk and isn't cleaned up automatically. A long-running project builds up directories. And it only helps when the transformer's inputs are truly the same. So It does nothing for a grid that tunes an early step.

## Building your own step

A pipeline accepts any of it with `fit` and `transform`. This Includes classes you write.

For a stateless change &mdash; a log, a ratio between two columns, a date part &mdash; `FunctionTransformer(func)` wraps a plain function and needs nothing else. It's the shortest route into a pipeline and covers a surprising amount.

When the step needs to *learn* a thing, subclassing `BaseEstimator` and `TransformerMixin` gives you the rest of the interface for free: `fit` stores what it learned on `self` with a trailing underscore, `transform` applies it. `TransformerMixin` supplies `fit_transform`. `get_params` and `set_params` arrive from `BaseEstimator`. This Is what makes the custom step tunable by a search like any other.

The rule that keeps a custom step honest is the same as for the built-in ones. All learned from data must be learned in `fit`. `transform` must use only what `fit` stored. A transformer that finds a statistic inside `transform` recomputes it on the test fold. This Is the leak the pipeline was supposed to prevent.

<strong>Can a pipeline end in a transformer?</strong> Yes. It then has `transform` rather than `predict`. This Is handy when the pipeline exists to prepare features for a thing else.

<strong>How do I see what the model really receives?</strong> `pipe[:-1].transform(X)` runs each step except the last and hands back the array the estimator was given.

<strong>Does a pipeline slow any of it down?</strong> No. It calls the same methods in the same order. The only cost is a few field lookups.

<strong>Can I add a step to a fitted pipeline?</strong> You can modify `pipe.steps`. The result is unfitted from that point on. Building a new pipeline is clearer.

## Reading a pipeline someone else wrote

An unseen pipeline is quicker to understand than an unseen script. The steps are the structure and they're listed in order.

Three questions cover it. **What are the steps?** `[name for name, _ in pipe.steps]` prints the sequence. The order is the order data flows through. **What does each one learn?** each step's fitted fields end in an underscore. `pipe["scale"].mean_` and `pipe["encode"].categories_` say what it took from the data. **What comes out?** `pipe[:-1].transform(X).shape` tells you how many features the model is really seeing. This Is often surprising after one-hot encoding.

The display helps too. Printing a pipeline in a notebook renders a diagram of the steps. `sklearn.set_config(display="diagram")` makes that the default. In a plain terminal, `print(pipe)` gives the nested repr. This Is dense but complete. each step and each non-default setting.

What to look for when reviewing one: whether any of it that learns from data sits *outside* it. A script that scales, imputes or selects features before building the pipeline has moved that step out of the folds. The pipeline's presence gives a false impression of safety. The pipeline only protects what is inside it.

## The order of the steps, again

Steps run in the order given, and some orders are wrong.

Imputation before scaling, because a scaler can't find a mean across missing values. Encoding before scaling, because a scaler can't subtract a mean from a string. Both before feature pick, because the selector needs numeric, complete columns to score. And pick before the model. The model sees what was chosen.

The sequence that covers most tabular problems is. Impute, encode, transform any skew, scale, select, fit. Not each problem needs all six. The scaled order of the ones you use should follow that list.

Getting it wrong often raises. This Is fortunate. The exception is putting pick before scaling when the selector's criterion is scale-sensitive. That runs. Quietly selects the columns with the largest units.

## Things to try

1. <strong>Confirm the interface.</strong> In the first editor, note that a pipeline has `fit` and `predict`. It's an estimator, not a wrapper you unwrap.
2. <strong>Reach inside.</strong> In the second editor, try `pipe[:-1].transform(X)[:2]` to see just what the model receives.
3. <strong>Tune the prep.</strong> In the fourth editor, add `"scale__with_std": [True, False]` to the grid and see whether it changes the winner.
4. <strong>Break it on purpose.</strong> Fit the scaler outside a pipeline on all of `X`, then cross-validate the model alone. Compare against the pipeline version.

## Where this leaves you

One object, fitted once, holding each step that learns any of it. It makes cross-validation honest, makes the prep tunable. Makes deployment a single file. There's no situation in this track where doing the steps by hand is preferable. Forming the habit early costs nothing.
""",
    [
        {"q": "What does a pipeline's predict() do to the transformers?",
         "options": ["Refits them", "Only calls transform", "Skips them", "Fits and transforms"],
         "answer": 1,
         "why": "fit fits them; predict only transforms. That asymmetry is what stops the held-out data influencing the transformation."},
        {"q": "How do you tune C on a step named clf?",
         "options": ["\"C\"", "\"clf.C\"", "\"clf__C\"", "\"clf-C\""],
         "answer": 2,
         "why": "Two underscores between the step name and the parameter. Nesting goes deeper with more of them."},
        {"q": "What does setting a step to \"passthrough\" do?",
         "options": ["Removes it permanently",
                     "Makes it a no-op, so the step can be tuned in or out",
                     "Runs it twice",
                     "Skips fitting but still transforms"],
         "answer": 1,
         "why": "It turns the step into an identity, which lets a search treat the existence of the step as a hyperparameter."},
        {"q": "Why pickle the pipeline rather than the model?",
         "options": ["It is smaller",
                     "The preprocessing is part of the model - without it the deployed model gets raw features",
                     "Models cannot be pickled",
                     "It is faster to load"],
         "answer": 1,
         "why": "A model fitted on scaled features and served raw ones produces confident nonsense, and nothing raises to tell you."},
    ],
)


# ---------------------------------------------------------------------------
# 13. Data leakage
# ---------------------------------------------------------------------------
topic(
    "data_leakage",
    "Leakage in a scikit-learn Workflow",
    "Preparing Data",
    "The failure that produces excellent scores and useless models, and the "
    "five shapes it comes in.",
    _svg(_box(14, 22, 60, 24, S, B) + _txt(44, 37, "train", M, 8) +
         _box(86, 22, 60, 24, S, B) + _txt(116, 37, "test", M, 8) +
         '<path d="M70 46 C70 62, 90 62, 90 46" stroke="var(--accent-primary)" '
         'stroke-width="2" fill="none"/>' +
         _txt(80, 76, "something crossed over", A, 8)),
    [
        ("A column that was computed from the answer",
         "The purest form: a feature that would not exist at prediction time.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import numpy as np

rng = np.random.RandomState(0)
n = 400
X = rng.normal(size=(n, 4))
y = (X[:, 0] + rng.normal(scale=2.0, size=n) > 0).astype(int)

honest = cross_val_score(LogisticRegression(), X, y, cv=5).mean()

# A column built from the answer - a risk score filled in after the outcome
# was known, say, or a status field the database updates on closure.
leaked = np.column_stack([X, y + rng.normal(scale=0.01, size=n)])
cheating = cross_val_score(LogisticRegression(), leaked, y, cv=5).mean()

print("features that were available beforehand:", round(honest, 3))
print("with one column derived from the answer:", round(cheating, 3))
print()
print("cross-validation cannot catch this: the leak is inside every fold.")
'''),

        ("The same row on both sides",
         "Random data, nothing to learn, and a perfect score - because every "
         "test row has a twin in the training set.",
         '''from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

rng = np.random.RandomState(0)
X = rng.normal(size=(200, 6))
y = rng.randint(0, 2, size=200)          # nothing to learn

clean = cross_val_score(KNeighborsClassifier(1), X, y, cv=5).mean()

# The same rows, twice - as happens after a bad join or a re-import.
Xd = np.vstack([X, X])
yd = np.concatenate([y, y])
duped = cross_val_score(KNeighborsClassifier(1), Xd, yd, cv=5).mean()

print("random data, no duplicates :", round(clean, 3))
print("every row duplicated       :", round(duped, 3))
print()
print("the nearest neighbour of a test row is its own twin in the")
print("training set, so the model looks up the answer.")
'''),

        ("One entity, several rows, both sides of the split",
         "The label is random per person. Anything above chance is the model "
         "recognising people rather than learning anything.",
         '''from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GroupKFold, KFold
import numpy as np

rng = np.random.RandomState(0)
n_people, per_person = 40, 5
groups = np.repeat(np.arange(n_people), per_person)

# Each person has a measurable fingerprint, and a label that has nothing
# to do with it. Nothing here generalises to a new person.
fingerprint = rng.normal(size=n_people)
label = rng.randint(0, 2, size=n_people)

X = fingerprint[groups][:, None] + rng.normal(scale=0.01,
                                              size=(n_people * per_person, 1))
y = label[groups]
model = RandomForestClassifier(random_state=0)

shuffled = cross_val_score(model, X, y,
                           cv=KFold(5, shuffle=True, random_state=0)).mean()
grouped = cross_val_score(model, X, y, cv=GroupKFold(5), groups=groups).mean()

print("shuffled folds - a person appears on both sides:", round(shuffled, 3))
print("GroupKFold     - each person is kept whole     :", round(grouped, 3))
'''),

        ("Shuffling a series that has an order",
         "Interpolating between known points is a much easier job than the one "
         "the model will actually be given.",
         '''from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import cross_val_score, KFold, TimeSeriesSplit
import numpy as np

rng = np.random.RandomState(0)
n = 300
t = np.arange(n).reshape(-1, 1)
y = np.cumsum(rng.normal(size=n))        # a random walk over time

model = KNeighborsRegressor(3)

shuffled = cross_val_score(model, t, y,
                           cv=KFold(5, shuffle=True, random_state=0)).mean()
forward = cross_val_score(model, t, y, cv=TimeSeriesSplit(5)).mean()

print("shuffled folds (R2)   :", round(shuffled, 3))
print("TimeSeriesSplit (R2)  :", round(forward, 3))
print()
print("shuffling lets the model interpolate between points it has seen")
print("on both sides. Predicting forward is the job it will actually have.")
'''),

        ("An encoding that used the target",
         "Target encoding is powerful and leaks by default, because each row "
         "helps compute the number that describes it.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import numpy as np

rng = np.random.RandomState(0)
n, n_cats = 300, 50
cat = rng.randint(0, n_cats, size=n)
y = rng.randint(0, 2, size=n)            # random - unrelated to the category

# Target encoding computed over the whole dataset: each row's own label
# has contributed to the number that describes it.
means = np.array([y[cat == c].mean() if (cat == c).any() else 0.5
                  for c in range(n_cats)])
X_leaky = means[cat].reshape(-1, 1)

print("target-encoded on all rows:",
      round(cross_val_score(LogisticRegression(), X_leaky, y, cv=5).mean(), 3))
print("the truth (labels are random):  0.5")
print()
print("with six rows per category, a row is a sixth of its own encoding.")
'''),

        ("Noticing it",
         "There is no detector. There is a baseline, a suspicion, and two "
         "questions.",
         '''from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import numpy as np

rng = np.random.RandomState(0)
X = rng.normal(size=(300, 5))
y = (X[:, 0] > 0).astype(int)
X = np.column_stack([X, y])              # the answer, as a column

base = cross_val_score(DummyClassifier(strategy="most_frequent"), X, y, cv=5).mean()
real = cross_val_score(LogisticRegression(), X, y, cv=5).mean()

print("dummy baseline :", round(base, 3))
print("the model      :", round(real, 3))
print()
print("a perfect score is not a triumph, it is a symptom.")
print("the checks: is any feature unavailable at prediction time?")
print("            was any column computed after the outcome was known?")
'''),
    ],
    [
        "Leakage is any information reaching the model that it would not have "
        "when actually used - and it always makes the score <em>better</em>.",
        "Cross-validation does not detect it. A leak in the data is inside "
        "every fold.",
        "<strong>Target leakage</strong>: a feature computed from, or after, "
        "the outcome. The most damaging and the least visible.",
        "<strong>Train-test contamination</strong>: preprocessing fitted before "
        "the split, duplicate rows, or one entity's rows on both sides.",
        "<strong>Temporal leakage</strong>: shuffling data that has an order, "
        "so the model trains on the future.",
        "The signals are a suspiciously high score, a dominant feature nobody "
        "expected, and a model that collapses in production.",
    ],
    """title: Data Leakage: A Practical Guide
intro: Every other failure in machine learning makes the score worse. This one makes it better. This Is why it lives review and reaches production.

## What it is

Data leakage is information from the future or from the test set reaching the model during training. It makes the model look better than it actually is. The score goes up, confidence goes up, and the model fails in production.

Leakage is harder to catch than other mistakes because it produces good numbers. A bug that crashes or gives a low score gets noticed quickly. A bug that gives a suspiciously high score gets celebrated. That asymmetry is why leakage causes more real-world damage than any other modelling error.

The most common form is preprocessing before splitting. Scaling the full dataset, imputing with the global median, encoding with frequencies computed on all rows. Each of these lets the test set influence the training process. The resulting score is optimistic by an amount you cannot measure without fixing the leak and rerunning.

A second common form is using features that carry information about the target that would not be available at prediction time. A hospital-readmission model that includes the discharge summary, which was written after the readmission decision, is an example. The feature is predictive precisely because it was created after the event.

This page covers both forms, shows how to detect them, and explains why cross-validation alone does not protect you.

Leakage is info reaching the model during training that it won't have when it's really used.

The defining property is the direction of the error. Overfitting, a bad metric, an unlucky split. These give results that look worse than the model is, or at least ambiguous. Leakage makes results that look *better*. So it doesn't trigger the instinct that a thing is wrong. It triggers satisfaction.

That skew is why it's the most costly mistake in the field. A model with a leak passes each check, gets deployed. Fails on the first real batch. At which point the test that approved it's worthless and no one knows why.

## Cross-validation will not save you

Worth stating plainly, because cross-validation is or else the answer to almost all on this track.

Cross-validation protects against one exact thing: a score that depends on which rows happened to be held out. If the leak is in the *data*. A column derived from the answer. Then each fold holds it, each fold is inflated. The mean of five inflated numbers is an inflated number with a reassuring standard deviation.

The first editor shows it: an honest 0.643 turns 1.000, across all five folds, with no warning of any kind.

## The five shapes

**Target leakage.** A feature that codes the answer, often because it was recorded after the outcome. A `case_closed_date` predicting whether a case closed. A `discount_given` predicting churn, when the discount was offered *because* the customer was leaving. A diagnosis code entered also as the diagnosis. These are the hardest to spot because the column is legitimately in the DB and nothing about its name says when it was written.

**prep before the split.** A scaler, imputer, encoder or feature selector fitted on all the data has seen the test rows. The cross-validation module measured this. Feature pick outside the folds reported 0.825 on pure noise.

**Duplicate rows.** After a bad join, a re-import, or truly repeated records. A duplicate split across train and test means the model has the answer stored. The second editor scores 1.000 on random data for just this reason.

**Group leakage.** a few rows showing one entity. A patient, a customer, a device, a doc. Landing on both sides. The model learns to recognise the entity rather than the pattern. The third editor scores 0.87 where the honest answer is chance.

**Temporal leakage.** Shuffling data that has an order. The training set holds the future. The fourth editor goes from R&sup2; of 0.977 to −2.526 when the split respects time. The second number is the one showing the job the model would really have.

## Target encoding deserves its own warning

It's the most handy high-cardinality encoding and the most solid way to leak.

Replacing a category with the mean target for that category is compact, powerful. Found from `y`. Do it over the whole dataset and each row has contributed to the number that shows it. With a hundred rows per category the part is small. With six, as in the fifth editor, it's a sixth. And a feature built from random labels predicts those labels at 0.71.

The fix is to find the encoding inside the folds, with the row's own part excluded. Which is what scikit-learn's `TargetEncoder` does, using an inner cross-fitting scheme. Hand-rolled target encoding is almost always leaky. The leak is proportional to how rare the categories are. This Is just when the encoding is most tempting.

## How to notice

There's no finder. There's a set of habits.

**Be suspicious of a good score.** Not sceptical of a good model. Suspicious of a *oddly* good one. If the problem is hard and the number is great, the first hypothesis should be a leak, not a breakthrough. Checking against a dummy makes the size of the claim visible.

**Look at feature importances.** A single feature dominating, above all one no one expected to matter, is the classic signature. Ask what it's, when it's written, and by what process.

**Ask the timing question for each column.** *Would this value be known, in this form, at the moment the guess has to be made?* This is the single most effective check available. It needs domain knowledge rather than code. A column that is only populated after the event is a leak even so of how innocent it looks.

**Ask who made the row.** If a few rows can come from one entity, group the split. If rows can be duplicated, check. If the data has a timestamp, respect it.

**Test on truly later data** where possible. A model that scores well in cross-validation and badly on the next month is telling you a thing a random split couldn't.

## The habits that prevent it

Split first, before any of it that learns. Put each transformer in a pipeline so it's refitted inside each fold. Use `GroupKFold` when rows share an entity and `TimeSeriesSplit` when they're sorted. Check for duplicates before splitting. Hold out a final test set and touch it once.

None of these is costly, and together they close each mechanical route. What they can't close is target leakage. That is a fact about the meaning of a column rather than about the code. Which is why the timing question has to be asked of each feature, by someone who knows what the columns mean.

## The famous cases

Leakage isn't a beginner's mistake. It has invalidated published research, contest results and deployed systems. The examples are worth knowing because they're all plausible.

A widely cited early result on detecting a disease from chest scans turned out to be partly detecting *which hospital* the scan came from. Sicker patients were concentrated at one site. The scanner left a signature in the image. The model was great at the task it was really solving and useless at the one it was believed to be solving.

Contest datasets have again and again leaked through row sorting. Here The file happened to be sorted by the target. Through id columns that linked with when a record was created. Both give a model a thing real to learn that has nothing to do with the problem.

A recurring one in industry: a churn model trained on a table where the "customer contacted support" flag was updated during the cancellation call. The feature was truly predictive and truly down at the moment a guess was needed.

The common thread is that none of these look like errors in the code. each one is a fact about how the data came to exist. This Is why reading the code more carefully never finds them and asking where a column comes from often does.

## The cost of being too careful

The opposite failure exists and is worth naming. Leakage anxiety can become its own problem.

Excluding each feature that has any tie with the target drops the signal along with the leak. A feature that is predictive because it's truly causally upstream is just what you want. Dropping it because it's "too predictive" makes the model worse for no reason.

Grouping a split when the rows are truly free throws away detail and gives an needlessly pessimistic guess. Refusing to use any aggregate feature because target encoding can leak rules out a whole class of handy ones that are found right.

The gap isn't how predictive a feature is. It's whether the value would exist, in that form, at the moment the guess has to be made. A feature that passes that test is allowed to be as predictive as it likes.

<strong>Is a highly predictive feature always suspicious?</strong> No. It's worth one question - would this be known at guess time - and if the answer is yes, use it.

<strong>How do I check for duplicates?</strong> `df.duplicated().sum()` before splitting. Consider near-duplicates too. Rows differing only in an id or a timestamp are functionally the same row.

<strong>Does leakage matter if I only care about ranking?</strong> Yes. A leaked feature ranks well in test and is absent in production. The ranking you deploy isn't the one you measured.

<strong>Can I fix a leak by dropping the column?</strong> often. Check what else was derived from it. Aggregates, ratios and encodings built on a leaky column carry the leak with them.

## A checklist before you trust a number

Six questions, in the order they're cheapest to answer. Running through them takes a few minutes and catches the large majority of leaks.

**Did any of it fit before the split?** Scaler, imputer, encoder, selector, vectoriser. If it learned from data and it ran before `train_test_split`, the number is compromised. The fix is a pipeline.

**Are there duplicate rows?** Count them, including near-duplicates that differ only in an id or a timestamp.

**Can one entity give a few rows?** If so, the split must group them. This is the one people most often get wrong on data that looks tabular and free.

**Does the data have an order?** Timestamps, sequence numbers, any of it where later rows couldn't have informed earlier ones. Then the split is forward-only.

**For each feature: would it exist at guess time?** Asked column by column, with someone who knows the source system. This is the slow one and the one that catches target leakage. This Nothing else will.

**Is the score plausible?** Checked against a dummy, against published results on similar problems. Against what a domain expert would guess. Surprise is the signal.

A model that lives all six isn't ensured honest. The left routes are narrow and unusual. A model that hasn't been through them has an unknown chance of being wrong in the most costly direction.

<strong>What if I find a leak after deploying?</strong> Retrain without the leaking feature and re-measure honestly before deciding whether the model is still worth running. The old score should be treated as never having existed rather than as a target to recover.

<strong>Is leakage always accidental?</strong> Mostly, and there's a well-known range that isn't. Tuning against the test set until the number is satisfactory. That is leakage through the researcher rather than through the data, and it makes the same inflated result.

## Things to try

1. <strong>Run the first editor.</strong> 0.643 turns 1.000 from one extra column, and each fold agrees.
2. <strong>Vary the duplication.</strong> In the second editor, duplicate only a quarter of the rows and see how much of the inflation lives.
3. <strong>Change the group size.</strong> In the third editor, set `per_person=2` and watch the gap narrow. The more rows per entity, the worse the leak.
4. <strong>Make the categories rarer.</strong> In the fifth editor, raise `n_cats` to 150 and watch the leaked score climb.

## Where this leaves you

The failure that raises your metrics. Cross-validation can't see it, a good score is evidence for it rather than against it. The only solid defence is asking, of each column, whether it would exist at the moment the guess is needed.
""",
    [
        {"q": "What makes leakage harder to catch than other failures?",
         "options": ["It raises no error",
                     "It makes the score better, so it does not feel like a problem",
                     "It only appears in production",
                     "It requires special tooling"],
         "answer": 1,
         "why": "Every other failure makes results look worse or ambiguous. Leakage makes them look excellent, so it passes review."},
        {"q": "Does cross-validation protect against a leaked column?",
         "options": ["Yes, that is what it is for",
                     "No - the leak is in the data, so it is inside every fold",
                     "Only with enough folds",
                     "Only with stratification"],
         "answer": 1,
         "why": "Cross-validation guards against a score depending on which rows were held out. A column derived from the target inflates all of them equally."},
        {"q": "Rows from one patient appear in both train and test. What is the effect?",
         "options": ["None, if the rows differ",
                     "The model can recognise the patient rather than learn the pattern, inflating the score",
                     "The model underfits",
                     "It only matters for time series"],
         "answer": 1,
         "why": "With a label that is random per person, shuffled folds scored 0.87 and GroupKFold 0.335. The first number was recognition, not learning."},
        {"q": "What is the single most effective check for target leakage?",
         "options": ["Cross-validate with more folds",
                     "Ask whether each feature would be known at prediction time",
                     "Scale the features",
                     "Use a simpler model"],
         "answer": 1,
         "why": "Target leakage is a fact about what a column means and when it is written, so it needs domain knowledge rather than code."},
    ],
)


# ---------------------------------------------------------------------------
# 14. Missing values
# ---------------------------------------------------------------------------
topic(
    "missing_values",
    "Missing Values",
    "Preparing Data",
    "Most estimators refuse to fit with a gap in the data. Filling it is easy; "
    "filling it without throwing away what the gap was telling you is the "
    "part worth learning.",
    _svg(_grid(30, 24, 4, 4, 13, S) +
         _box(56, 37, 13, 13, S, A, 2, 0) + _txt(62, 47, "?", A, 9) +
         _box(43, 50, 13, 13, S, A, 2, 0) + _txt(49, 60, "?", A, 9) +
         _txt(80, 84, "absence is often information", M, 7)),
    [
        ("Most estimators simply refuse",
         "And one family does not, which is worth knowing before reaching for "
         "an imputer at all.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
import numpy as np

X = np.array([[1.0, 2.0], [np.nan, 3.0], [3.0, 4.0], [4.0, 5.0]])
y = np.array([0, 0, 1, 1])

try:
    LogisticRegression().fit(X, y)
except ValueError as e:
    print("LogisticRegression:", str(e).split("\\n")[0][:80])

HistGradientBoostingClassifier(max_iter=10).fit(X, y)
print()
print("HistGradientBoosting: fitted, NaN handled natively")
'''),

        ("The four simple strategies",
         "Note what the outlier does to the mean, and what it does not do to "
         "the median.",
         '''from sklearn.impute import SimpleImputer
import numpy as np

X = np.array([[1.0], [2.0], [100.0], [np.nan]])

for strategy in ("mean", "median", "most_frequent", "constant"):
    imp = SimpleImputer(strategy=strategy, fill_value=-1)
    out = imp.fit_transform(X).ravel()
    print("%-14s filled with %8.2f  ->  %s" % (strategy, out[-1], out))
'''),

        ("Keeping the fact that it was missing",
         "add_indicator appends a column recording where the gaps were.",
         '''from sklearn.impute import SimpleImputer
import numpy as np

X = np.array([[1.0], [2.0], [np.nan], [4.0]])

imp = SimpleImputer(strategy="mean", add_indicator=True)
out = imp.fit_transform(X)

print("columns out:", out.shape[1], "- the value, and a was-it-missing flag")
print(out)
print()
print("the flag lets the model use the fact of absence, which is often")
print("informative in its own right.")
'''),

        ("The fill value is learned, so it obeys the split",
         "The test rows get the training median, not their own.",
         '''from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import numpy as np

rng = np.random.RandomState(0)
X = rng.normal(loc=10.0, size=(200, 1))
X[rng.rand(200) < 0.2] = np.nan
X_tr, X_te = train_test_split(X, test_size=0.5, random_state=0)

imp = SimpleImputer(strategy="median").fit(X_tr)

print("median learned from the training half:", round(imp.statistics_[0], 4))
print("median of the test half (not used)   :",
      round(float(np.nanmedian(X_te)), 4))
print()
print("the test rows are filled with the training median, because that")
print("is the number that would be available in production.")
'''),

        ("Using the other columns to guess",
         "When features are correlated, the column mean is a poor guess and "
         "the neighbouring rows are a good one.",
         '''from sklearn.impute import SimpleImputer, KNNImputer
import numpy as np

# Two correlated columns; the second is missing on one row.
X = np.array([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0], [4.0, np.nan], [5.0, 10.0]])

simple = SimpleImputer(strategy="mean").fit_transform(X)
knn = KNNImputer(n_neighbors=2).fit_transform(X)

print("true value would be about 8.0")
print("SimpleImputer (column mean):", round(simple[3, 1], 3))
print("KNNImputer (similar rows)  :", round(knn[3, 1], 3))
'''),

        ("When the gap is the signal",
         "The value is missing precisely when the answer is yes. Imputing it "
         "away destroys the most useful feature in the data.",
         '''from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
import numpy as np

rng = np.random.RandomState(0)
n = 600
X = rng.normal(size=(n, 3))
y = (X[:, 0] > 0).astype(int)

# Missing NOT at random: the value is absent mostly when y is 1.
Xm = X.copy()
Xm[(y == 1) & (rng.rand(n) < 0.7), 0] = np.nan

plain = make_pipeline(SimpleImputer(), LogisticRegression())
flagged = make_pipeline(SimpleImputer(add_indicator=True), LogisticRegression())

print("impute only        :", round(cross_val_score(plain, Xm, y, cv=5).mean(), 3))
print("impute + indicator :", round(cross_val_score(flagged, Xm, y, cv=5).mean(), 3))
print()
print("when absence itself carries the signal, throwing it away costs you.")
'''),
    ],
    [
        "Most estimators raise on <code class='mono-font'>NaN</code>; the "
        "<code class='mono-font'>HistGradientBoosting</code> pair handle it "
        "natively and often better than any imputation.",
        "<code class='mono-font'>SimpleImputer</code> learns one number per "
        "column - <code class='mono-font'>statistics_</code> - so it must be "
        "fitted on the training data only.",
        "<strong>median</strong> over <strong>mean</strong> for anything skewed "
        "or with outliers; <strong>most_frequent</strong> or a constant for "
        "categorical columns.",
        "<code class='mono-font'>add_indicator=True</code> keeps a flag for "
        "where the value was missing, which is free and frequently the most "
        "useful feature added.",
        "<code class='mono-font'>KNNImputer</code> and "
        "<code class='mono-font'>IterativeImputer</code> use the other columns, "
        "which beats a column constant when features are correlated.",
        "Dropping rows is only safe when values are missing at random and there "
        "are few of them - otherwise it biases the data.",
    ],
    """title: Missing Values: A Practical Guide
intro: A gap in the data is two problems: the estimator won't run. The gap itself may have been telling you a thing.

## Why it has to be handled

Real datasets almost always have missing values. A sensor drops a reading, a survey respondent skips a question, a join produces nulls where records do not match. The gaps are part of the data, and handling them is part of the modelling work.

scikit-learn does not fill missing values for you. Most estimators raise an error when they encounter a NaN. That design is deliberate. There is more than one way to fill a gap, and the choice affects the model. Filling with the mean preserves the column's average but shrinks its variance. Filling with the median is less affected by outliers. Filling with a constant like -1 creates a new category that the model can split on.

The right strategy depends on why the data is missing and what the model will do with it. A column where missingness itself is informative -- for example, income is missing because the respondent refused to answer -- should not be filled with the median. The fact that it is missing carries signal.

This page covers the imputation strategies scikit-learn provides, the tree-based models that handle NaN natively, and the common mistake of imputing before splitting.

Almost each estimator in scikit-learn raises `ValueError: Input X holds NaN` rather than guessing. That refusal is deliberate. There's no universally correct fill. Silently choosing one would hide a choice that changes the model.

The exceptions are worth knowing before you reach for an imputer at all. `HistGradientBoostingClassifier` and its regressor sibling handle missing values natively. At each split, the tree learns which side the missing rows should go. This Is a truly better answer than filling in a number. It lets the missingness itself sway the guess without inventing data. On tabular problems with gaps, starting there and skipping imputation fully is often the right move.

For all else, a thing has to fill the gap.

## The simple strategies, and choosing between them

`SimpleImputer` replaces missing values with one number per column, learned during `fit` and stored in `statistics_`.

**mean** is the default and the wrong default for most real data. The editor above shows why. With values of 1, 2 and 100, the mean is 34.33. A number nothing like any of the readings. Any skew or outlier drags it.

**median** is the safer choice for numeric columns and should probably be your habit. It's unaffected by the tail and always lands on a plausible value.

**most_frequent** works for cat columns and for numeric ones with few distinct values.

**constant** fills with `fill_value` &mdash; handy when there's a real default. Handy with a sentinel like -1 when you want the model to be able to see the imputed rows. For cat data, `fill_value="missing"` makes lack an clear category. This Is often just right.

## The fill value is learned

This is the part that connects back to the rest of the track: `statistics_` is found from data. An imputer fitted on all has seen the test set.

The effect is often small. A median shifts a little &mdash; but the principle is the same as all over else. There's a stronger hands-on reason. In production, the median of the future data isn't available. The model has to fill gaps with a number found at training time. That is the number the test should use.

The editor above shows the training median and the test median differing in the third decimal. The test rows get the training one, which is correct.

`SimpleImputer` inside a `Pipeline` handles this automatically, refitting on each training fold. As with scaling, there's no good reason to do it by hand.

## Missingness is information

The most common mistake isn't choosing the wrong fill value. It's discarding that a value was missing.

Data is rarely missing at random. A blank income field on a loan use, an absent test result, an unrecorded satisfaction score. In each case the lack often correlates with a thing. People decline to answer questions for reasons, tests aren't sorted for reasons. Fields go unfilled for reasons.

`add_indicator=True` appends a binary column marking where each gap was. It costs one column per affected feature and it hands the model the pattern of lack as a feature in its own right.

The last editor makes the size of the effect concrete. With a value missing mostly when the answer is yes, imputing alone scores 0.77. Imputing with an indicator scores 0.987. The imputer filled in a plausible number and erased the most helpful thing in the dataset. The indicator put it back.

The taxonomy is worth knowing by name. **Missing fully at random**. The gap has no tie to any of it. Is the only case where plain imputation loses nothing. It's the rarest. **Missing at random**. Here The gap depends on other seen features, is common and partly recoverable by a model-based imputer. **Missing not at random**. Here The gap depends on the unobserved value itself, is both the most common and the one where the indicator matters most.

## Using the other columns

When features are linked, a column constant is a poor guess. Two better options use the rest of the row.

`KNNImputer` finds the most similar complete rows and means their values for the missing feature. The editor above shows it getting back 8.0 where the column mean gives 5.5. The two columns move together and the neighbours know it. It needs the features scaled. It measures distance. It's costly on large data because it searches for neighbours.

`IterativeImputer` models each column with missing values as a function of the others, in rounds, until the guesses settle. It's the most capable of the three and the slowest. It's still marked experimental. Importing it needs `from sklearn.experimental import enable_iterative_imputer` first. This Catches everyone once.

Both are worth trying when imputation quality matters. Neither is worth the cost when the missingness is light and the model is a grad booster that could have handled it natively.

## Dropping, and when it is allowed

`dropna()` is the tempting one-liner and it's only safe under rules worth checking.

Dropping rows is defensible when the values are truly missing at random and the affected rows are few. It's a mistake when the missingness is helpful. You're deleting just the rows that carry the pattern. And the bias it adds is invisible in each later metric.

Dropping a column is defensible when most of it's missing and no indicator would help. A column that is 95% empty rarely carries enough to be worth imputing, though the 5% pattern at times does. Which is what the indicator would tell you.

The skew to note: you can drop rows from the training data. You can't drop them at guess time. A model that has never seen a missing value in a column will still be handed one eventually. A thing has to happen. Deciding what, during training, is the whole point of having an imputer in the pipeline.

## Categorical columns need a different answer

All above assumes numeric data. Text columns have gaps too. The math strategies don't apply.

`SimpleImputer(strategy="most_frequent")` works and quietly asserts that the missing rows are like the majority. This Is often just the claim that is false. `strategy="constant", fill_value="missing"` is often better. It creates an clear category, the encoder gives it its own column. The model can learn what that column is worth. Lack turns a value rather than a guess.

`OneHotEncoder` also handles `NaN` right, treating it as its own category without any imputation step. This Is the shortest route to the same result.

The reason the clear category often wins is the same as for the indicator. In real data, "not stated" is a fact about the record rather than a hole where a fact should be. A blank employer field, an unselected optional dropdown, a survey question skipped. Each tells you a thing. Folding it into the most common value asserts the opposite.

## How much is too much

A quick rule for triage, applied per column rather than to the dataset as a whole.

**Under about 5% missing.** Almost any reasonable imputation works and the choice barely matters. Use the median, add the indicator, move on.

**Between 5% and 30%.** The choice starts to matter. Compare a couple of strategies by cross-validation. Treat the indicator as compulsory rather than optional.

**Over 30%.** The column is mostly absent. Imputing it means most of it's invented. Consider keeping only the indicator and discarding the values. This At times performs better than either the column or its removal.

**Over 80%.** often drop the column, unless the small present portion is known to be highly helpful.

These are rules of thumb rather than thresholds. The honest way to settle any of them is to try both inside a pipeline and compare cross-validated scores. That takes two lines. This Is less effort than arguing about it.

<strong>Why does IterativeImputer need a special import?</strong> It's still marked experimental. `from sklearn.experimental import enable_iterative_imputer` has to run first. The import looks unused and isn't.

<strong>Should I impute the target?</strong> No. Rows with a missing target carry no info for guided learning - drop them. Check why they're missing before you do.

<strong>Does KNNImputer need scaling?</strong> Yes. It measures distance between rows. A column in thousands dominates the neighbour search just as it would for k-NN itself.

<strong>Can I impute before splitting if I only use the median?</strong> No. The median is learned from data. It carries info from the test rows into training. The effect is small and the habit is what matters.

## Finding out what is actually missing

Before choosing a strategy, two minutes of counting decides most of it.

Count per column rather than in total. `df.isna().sum()` gives the picture. It's often uneven. One or two columns carry nearly all the gaps while the rest are complete. That changes the problem from "how do I impute this dataset" to "what do I do about these two columns". This Is a much easier question.

Then look at whether the gaps coincide. Columns that are missing together often come from the same source. A form section that was skipped, a system that was down, a join that failed for a subset. If three columns are missing on just the same rows, they're one piece of info absent once. One indicator covers all three rather than three separate ones.

Finally, compare the target between rows with and without the gap. A difference in the target rate between present and missing is direct evidence that the missingness is helpful. It takes one line to check. When it's large, the indicator isn't optional and imputation alone will lose most of the signal. Which is what the last editor on this page shows at 0.77 against 0.987.

None of this needs a plot or a library. Three counts and a check, before any choice about strategy.

<strong>What about values that aren't NaN but mean missing?</strong> Sentinels like -999, 0, or an empty string are extremely common in exported data. No imputer recognises them. Convert them to `NaN` first, or the model treats -999 as a very small number.

<strong>Does the order of imputation and encoding matter?</strong> Yes. Impute cat columns before encoding them, or the encoder treats `NaN` as its own category - which is at times what you want and should be a choice rather than an accident.

## Things to try

1. <strong>Compare the strategies.</strong> In the second editor, note that mean fills 34.33 into a column whose other values are 1, 2 and 100.
2. <strong>Recover the link.</strong> The fifth editor has KNNImputer land on 8.0 just. Change the neighbours to 1 and see what happens.
3. <strong>Turn the indicator off.</strong> The last editor drops from 0.987 to 0.77. That gap is the value of one extra column.
4. <strong>Skip imputation fully.</strong> Replace the pipeline in the last editor with `HistGradientBoostingClassifier()` on the raw data with gaps.

## Where this leaves you

Median rather than mean for numeric columns, an clear category for cat ones, `add_indicator=True` almost always, the imputer inside a pipeline so the fill value obeys the split. A check of whether a grad booster could have handled the gaps without any of it.
""",
    [
        {"q": "What does SimpleImputer learn during fit?",
         "options": ["Which rows to drop",
                     "One fill value per column, stored in statistics_",
                     "A model of each column",
                     "Nothing - it fills at transform time"],
         "answer": 1,
         "why": "One number per column, computed from the data it was fitted on - which is why it must be fitted on the training half only."},
        {"q": "Why prefer median over mean for numeric columns?",
         "options": ["It is faster",
                     "It is unaffected by outliers and always lands on a plausible value",
                     "It handles categories",
                     "It is the default"],
         "answer": 1,
         "why": "With values of 1, 2 and 100 the mean is 34.33 - a number nothing like any observation. The median is 2."},
        {"q": "What does add_indicator=True do?",
         "options": ["Marks the imputer as fitted",
                     "Appends a column recording where values were missing",
                     "Raises if too much is missing",
                     "Drops rows with gaps"],
         "answer": 1,
         "why": "It preserves the fact of absence, which is frequently informative. In the last editor it took the score from 0.77 to 0.987."},
        {"q": "Which estimator handles NaN without an imputer?",
         "options": ["LogisticRegression",
                     "HistGradientBoostingClassifier",
                     "KNeighborsClassifier",
                     "RandomForestClassifier"],
         "answer": 1,
         "why": "It learns which side of each split the missing rows belong on, which uses the missingness rather than filling over it."},
    ],
)


# ---------------------------------------------------------------------------
# 15. ColumnTransformer
# ---------------------------------------------------------------------------
topic(
    "column_transformer",
    "Different Columns, Different Treatment",
    "Preparing Data",
    "Real tables mix numbers and categories, and the two need opposite "
    "preparation. One object routes each column to the right transformer.",
    _svg(_box(10, 20, 34, 20, S, M) + _txt(27, 34, "numeric", M, 7) +
         _arrow(46, 30, 58, 30) + _box(60, 20, 34, 20, S, A) +
         _txt(77, 34, "scale", A, 7) +
         _box(10, 50, 34, 20, S, M) + _txt(27, 64, "text", M, 7) +
         _arrow(46, 60, 58, 60) + _box(60, 50, 34, 20, S, A) +
         _txt(77, 64, "one-hot", A, 7) +
         _arrow(96, 45, 108, 45) + _box(110, 34, 38, 22, S, M) +
         _txt(129, 49, "one X", M, 8)),
    [
        ("Two treatments, one object",
         "Each transformer gets the columns it was given, and the results are "
         "stuck side by side.",
         '''from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd

df = pd.DataFrame({"age": [25, 40, 33, 51],
                   "salary": [30000, 55000, 41000, 72000],
                   "city": ["london", "paris", "london", "berlin"]})

pre = ColumnTransformer([
    ("num", StandardScaler(), ["age", "salary"]),
    ("cat", OneHotEncoder(sparse_output=False), ["city"]),
])

out = pre.fit_transform(df)
print("in :", df.shape, " out:", out.shape)
print("names:", list(pre.get_feature_names_out()))
print(out.round(2))
'''),

        ("Selecting by type instead of by hand",
         "So that adding a column to the data does not mean editing the "
         "pipeline.",
         '''from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd

df = pd.DataFrame({"age": [25, 40, 33], "salary": [30000, 55000, 41000],
                   "city": ["london", "paris", "london"],
                   "grade": ["a", "b", "a"]})

pre = ColumnTransformer([
    ("num", StandardScaler(), make_column_selector(dtype_include="number")),
    ("cat", OneHotEncoder(sparse_output=False),
     make_column_selector(dtype_include=object)),
])
pre.fit(df)
print("picked by dtype, not by hand:")
print("  numeric    :", list(pre.transformers_[0][2]))
print("  categorical:", list(pre.transformers_[1][2]))
'''),

        ("What happens to the columns you did not mention",
         "The default is to drop them, silently.",
         '''from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
import pandas as pd

df = pd.DataFrame({"age": [25, 40, 33], "salary": [30000, 55000, 41000],
                   "id": [1, 2, 3]})

drop = ColumnTransformer([("num", StandardScaler(), ["age", "salary"])])
keep = ColumnTransformer([("num", StandardScaler(), ["age", "salary"])],
                         remainder="passthrough")

print("remainder='drop' (the default):", drop.fit_transform(df).shape)
print("remainder='passthrough'       :", keep.fit_transform(df).shape)
print()
print("the default silently discards any column you did not name -")
print("which is usually right, and is worth knowing about.")
'''),

        ("The whole preparation, inside one estimator",
         "Impute, scale, encode and fit - and every step refitted on the "
         "training part of each fold.",
         '''from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import pandas as pd
import numpy as np

rng = np.random.RandomState(0)
n = 300
df = pd.DataFrame({
    "age": rng.normal(40, 10, n),
    "salary": rng.normal(50000, 15000, n),
    "city": rng.choice(["london", "paris", "berlin"], n),
})
df.loc[rng.rand(n) < 0.1, "age"] = np.nan
y = (df["salary"] > 50000).astype(int)

numeric = make_pipeline(SimpleImputer(strategy="median"), StandardScaler())
categorical = OneHotEncoder(handle_unknown="ignore")

pre = ColumnTransformer([("num", numeric, ["age", "salary"]),
                         ("cat", categorical, ["city"])])

model = Pipeline([("pre", pre), ("clf", LogisticRegression(max_iter=1000))])
print("cross-validated accuracy:",
      round(cross_val_score(model, df, y, cv=5).mean(), 4))
print()
print("impute, scale, encode and fit - every step refitted per fold")
'''),

        ("Tuning something four levels down",
         "The underscores compose, so a search can reach the imputation "
         "strategy inside the numeric branch.",
         '''from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np

rng = np.random.RandomState(0)
n = 200
df = pd.DataFrame({"age": rng.normal(40, 10, n),
                   "city": rng.choice(["a", "b"], n)})
df.loc[rng.rand(n) < 0.2, "age"] = np.nan
y = rng.randint(0, 2, n)

numeric = make_pipeline(SimpleImputer(), StandardScaler())
pre = ColumnTransformer([("num", numeric, ["age"]),
                         ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"])])
pipe = Pipeline([("pre", pre), ("clf", LogisticRegression())])

grid = {"pre__num__simpleimputer__strategy": ["mean", "median"],
        "clf__C": [0.1, 1.0]}
search = GridSearchCV(pipe, grid, cv=3).fit(df, y)
print("the key reaches four levels down:")
print("  pre__num__simpleimputer__strategy")
print()
print("best:", search.best_params_)
'''),

        ("A list of names, not a name",
         "The most common error here, and the message says exactly what is "
         "wrong.",
         '''from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import pandas as pd

df = pd.DataFrame({"city": ["london", "paris", "london"]})

ok = ColumnTransformer([("cat", OneHotEncoder(sparse_output=False), ["city"])])
print("a list of names ->", ok.fit_transform(df).shape)

bad = ColumnTransformer([("cat", OneHotEncoder(sparse_output=False), "city")])
try:
    bad.fit_transform(df)
except Exception as e:
    print()
    print("a bare string ->", type(e).__name__)
    print(" ", str(e).split("\\n")[0][:88])
print()
print("a list selects a DataFrame (2-D); a bare name selects a Series (1-D),")
print("and the encoder wants two dimensions.")
'''),
    ],
    [
        "Each entry is <code class='mono-font'>(name, transformer, columns)</code>, "
        "and the outputs are concatenated in the order the transformers are "
        "listed.",
        "Columns not named are <strong>dropped</strong> by default; "
        "<code class='mono-font'>remainder=\"passthrough\"</code> keeps them "
        "untransformed.",
        "<code class='mono-font'>make_column_selector</code> picks columns by "
        "dtype or by a name pattern, so new columns are handled without editing "
        "the pipeline.",
        "A transformer can itself be a <code class='mono-font'>Pipeline</code>, "
        "which is how a column gets imputed <em>and</em> scaled.",
        "<code class='mono-font'>get_feature_names_out()</code> traces names "
        "through the whole thing, prefixed with the transformer's name.",
        "Pass a <strong>list</strong> of column names - a bare string selects a "
        "1-D Series and raises.",
    ],
    """title: Different Columns, Different Treatment: A Practical Guide
intro: A pipeline applies each step to each column. Real tables need scaling on some columns and encoding on others. ColumnTransformer is how you say which is which.

## The problem

Real tables have mixed types. Some columns are numeric, some are categorical, and each type needs different preprocessing. A scaler makes no sense on a city-name column. A one-hot encoder makes no sense on a temperature column. Applying the same transformer to every column either crashes or produces nonsense.

`ColumnTransformer` solves this by routing each group of columns to its own transformer. You specify which columns get which treatment. The transformer applies each sub-pipeline to its columns and concatenates the results into a single array. Because `ColumnTransformer` is itself a transformer, it fits into a `Pipeline` as one step. That keeps the routing inside the cross-validation loop, which prevents the preprocessing leak.

Without a column transformer, the usual workaround is to slice the DataFrame, transform each slice, and concatenate manually. That works for a single train-test split. It breaks under cross-validation because the slicing and transforming happen outside the fold loop. The test-fold statistics leak into the training set.

This page covers building a column transformer, combining it with a pipeline, inspecting the output columns, and handling columns that should be passed through or dropped.

A `Pipeline` is a sequence applied to all of `X`. That works when the columns are homogeneous and breaks right away on a real table.

Numeric columns want imputing with a median and scaling. cat columns want imputing with a constant and one-hot encoding. Applying a scaler to a text column raises. Applying an encoder to a smooth one makes a column per distinct value, which is nonsense.

The manual workaround &mdash; split the frame, transform each part, concatenate &mdash; works and puts the changes outside any pipeline. This Puts them outside the cross-validation folds. This Is the leak this track keeps returning to.

`ColumnTransformer` solves it properly: it routes each subset of columns to its own transformer and concatenates the results. Because it's itself a transformer, the whole thing drops into a pipeline as a single step.

## How it is written

Each entry is a triple: a name, a transformer, and the columns it applies to.

The name is yours to choose and appears in the made feature names and in the param keys for tuning. Short and real pays off. `num` and `cat` rather than `transformer_1`.

The columns can be a list of names, a list of int spots, a boolean mask, or a callable. Passing a **list** matters. A list of one name selects a DataFrame. This Is two-dimensional. A bare string selects a Series. This Is one-dimensional. The transformer raises. The error message says "Expected a 2-dimensional container", which is precise once you know what it refers to.

The outputs are concatenated left to right in the order the transformers are listed, not in the first column order. So the resulting array's columns follow your specification. This Is why `get_feature_names_out()` is the solid way to know what ended up where.

## remainder, and the columns you forgot

By default, any column not named in any transformer is **dropped**.

That is often right &mdash; ids, timestamps and free text often shouldn't reach the model &mdash; and it's silent. This Is the part worth knowing. A column added to the source data will simply not appear in the model, with no warning. The effect is a model quietly skipping a feature somebody thought they had added.

`remainder="passthrough"` keeps the unnamed columns as they're. It's convenient and slightly dangerous. It will happily pass through an id column. This Is just the sort of thing that lets a model store rows.

`remainder=SomeTransformer()` applies a transformer to all left over. This Is at times the tidiest way to say "scale all I haven't or else mentioned".

The habit worth adopting: name each column by name, or use selectors that provably cover all. Treat the default drop as a safety net rather than as the design.

## Selecting by type

Listing column names by hand is fine for a fixed table and a maintenance burden for any of it that changes.

`make_column_selector(dtype_include="number")` selects the numeric columns what they're called. `dtype_include=object` picks up the strings. `pattern="^date_"` selects by name. The selector runs at `fit` time against what frame it's given. A new numeric column is handled without touching the pipeline.

The caution is that dtypes aren't always what you expect. A cat column stored as ints. A postcode district, a department id. Is selected as numeric and scaled. This Is the mistake the encoding module warned about, now happening automatically. Converting such columns to a string or a pandas `category` dtype before the pipeline is what makes dtype-based pick safe.

## Nesting a pipeline inside a branch

A single column group often needs more than one step: numeric columns want imputing *and* scaling.

The transformer in a `ColumnTransformer` entry can be a `Pipeline`. This Is how that is expressed. `make_pipeline(SimpleImputer(strategy="median"), StandardScaler())` turns the numeric branch. The cat branch gets its own with an imputer and an encoder.

The result is a small tree: a pipeline holding a column transformer holding pipelines holding transformers. That sounds elaborate and is the standard shape of each real scikit-learn program. It's the min structure that does the right thing on a mixed table.

The whole tree is one estimator. `fit` on the outer pipeline reaches each leaf. Cross-validation refits all of it on each training fold.

## Reaching into it to tune

The double-underscore rule composes, so params deep in the tree are addressable.

`pre__num__simpleimputer__strategy` reads outside in: the step named `pre`, its branch named `num`, the step named `simpleimputer` in that branch. Its `strategy`. Four levels, one string. A grid search can vary it alongside the model's own settings.

This is more handy than it first appears. Whether to impute with the mean or the median, whether to scale, whether to drop the first one-hot column. These are choices often made by guesswork. They can be made by cross-validation instead, in the same search that tunes the model.

`pipe.get_params().keys()` lists each addressable param. This Is the fastest way to find the right spelling rather than deriving it.

## Getting the names back

After one-hot encoding, the array has more columns than the frame had, with names no one wrote.

`get_feature_names_out()` rebuilds them, prefixed by the transformer name: `num__age`, `cat__city_paris`. Called on the outer pipeline, it traces through each step.

That matters for reading the model. Zipping the names against `coef_` or `feature_importances_` turns an anonymous array into a labelled result. Without it the mapping has to be rebuilt by counting. This Is both tedious and easy to get wrong by one after any change to the prep.

## The shape of a real preprocessing block

Almost each tabular project ends up with the same structure. It's worth having it in mind as a template rather than deriving it each time.

A numeric branch: impute with the median, then scale. A cat branch: impute with a constant such as `"missing"`, then one-hot encode with `handle_unknown="skip"`. A column transformer routing the two by dtype. A model on the end. The whole thing in one `Pipeline`, cross-validated, with the prep choices exposed to a search.

That covers a large majority of tabular problems and is about fifteen lines. What varies between projects is which extra branches appear. A text column going to a vectoriser, a date column going to a custom transformer that extracts the parts, a high-cardinality column going to a target encoder instead of one-hot.

The value of the template isn't the exact steps but that it puts each learned change in one place, inside the folds, addressable by a search. A project that starts from it rarely acquires the leaks that a project assembled step by step does.

One hands-on note: build it up one branch at a time and check the output shape after each. A column transformer that silently drops half the frame makes a model that works and underperforms. The shape is the fastest way to notice.

## When the branches disagree about rows

A limitation worth knowing, because it isn't obvious from the interface.

each transformer in a `ColumnTransformer` receives the same rows and must return the same number of rows, in the same order. The results are concatenated flatly. Any of it that reordered or dropped rows would misalign the columns against each other and against `y`.

That rules out row-level ops inside it: no dropping outliers, no resampling, no aggregating. Those belong before the pipeline, applied to the training data only, or in a library built for it. `imbalanced-learn` gives a pipeline that understands row changes. This Is the right tool when resampling is part of the model rather than part of the data preparation.

It also means a transformer that returns a different number of rows than it received will fail with a shape error rather than a helpful message. A custom transformer that filters is a mistake worth ruling out early.

<strong>Does the output keep my column order?</strong> No. Columns come out in the order the transformers are listed, then within each transformer. `get_feature_names_out()` is the solid way to know what is where.

<strong>Can I use the same column in two transformers?</strong> Yes - a column can appear in more than one entry. Both outputs are kept. That is how you'd scale a column and also bin it.

<strong>Is there a shorthand?</strong> `make_column_transformer((StandardScaler(), ["age"]), (OneHotEncoder(), ["city"]))` skips the names and makes them, in the same way `make_pipeline` does.

<strong>What if a column is numeric but cat in meaning?</strong> Convert it to a string or a pandas `category` dtype before the pipeline, or dtype-based pick will scale it as a number.

## Debugging one that is not working

A column transformer that misbehaves is harder to inspect than a plain pipeline. The branches run in parallel and the output is a single anonymous array. Four things to check, in order.

**The output shape.** `pre.fit_transform(df).shape` against what you expected. Too few columns often means a branch selected nothing. Too many often means a high-cardinality column reached the one-hot encoder.

**What each branch really selected.** After fitting, `pre.transformers_` holds the resolved triples, with the callable selectors already turned into concrete column lists. Printing the third element of each entry says just which columns went where. This Is the fastest way to find a column that fell through to `remainder`.

**The names.** `pre.get_feature_names_out()` lists each output column with its branch prefix. If a name you expected is absent, the column was dropped. If there are hundreds of `cat__` names, an identifier reached the encoder.

**One branch at a time.** `pre.named_transformers_["num"]` gives the fitted branch. This Can be inspected on its own. Its imputer's `statistics_`, its scaler's `mean_`. When the whole thing makes a thing odd, narrowing to one branch often localises it in a minute.

The general lesson is that the object is introspectable at each level. The trouble is only that the handy fields have to be asked for by name.

<strong>Does it work with NumPy arrays?</strong> Yes, selecting by int spot rather than by name. Names are worth the DataFrame. Spots shift when a column is added.

<strong>Can a branch return a sparse mat?</strong> Yes. The result is sparse if enough of it's. `sparse_threshold=0` forces a dense output when the next step needs one.

## Things to try

1. <strong>Watch the shape change.</strong> The first editor turns three columns into five. Read the names to see which came from where.
2. <strong>Lose a column.</strong> In the third editor, note that `id` disappears with no warning under the default.
3. <strong>Add a column.</strong> In the second editor, add another numeric column to the frame and confirm the selector picks it up with no edit to the transformer.
4. <strong>Find the param names.</strong> In the fifth editor, print `sorted(pipe.get_params())` and look for the keys you could tune.

## Where this leaves you

One object that sends each group of columns to the transformer it needs, nests pipelines inside its branches, drops what you didn't mention. Exposes each setting inside it to a search. Together with `Pipeline` it's the shape of each real scikit-learn program on tabular data.
""",
    [
        {"q": "What happens to a column not named in any transformer?",
         "options": ["It is passed through unchanged",
                     "It is dropped, silently",
                     "It raises an error",
                     "It is scaled by default"],
         "answer": 1,
         "why": "remainder defaults to \"drop\". A column added to the source data will simply not reach the model, with no warning."},
        {"q": "Why pass [\"city\"] rather than \"city\"?",
         "options": ["Style only",
                     "A list selects a 2-D DataFrame; a bare string selects a 1-D Series and raises",
                     "Lists are faster",
                     "A string selects every matching column"],
         "answer": 1,
         "why": "The error says \"Expected a 2-dimensional container\". Transformers want two dimensions, which is the same X-must-be-2-D rule from the start of the track."},
        {"q": "How do you impute AND scale the numeric columns only?",
         "options": ["Two ColumnTransformers in sequence",
                     "Put a Pipeline as the transformer for that column group",
                     "It cannot be done",
                     "Use remainder"],
         "answer": 1,
         "why": "A ColumnTransformer entry accepts any transformer, including a Pipeline - which is how a branch gets several steps."},
        {"q": "What does pre__num__simpleimputer__strategy address?",
         "options": ["A column named strategy",
                     "The strategy of the imputer inside the num branch of the step named pre",
                     "The pipeline's own strategy",
                     "Nothing - it is invalid"],
         "answer": 1,
         "why": "The double underscores compose outside in. pipe.get_params().keys() lists every valid key."},
    ],
)


# ---------------------------------------------------------------------------
# 16. Overfitting and underfitting
# ---------------------------------------------------------------------------
topic(
    "overfitting_and_underfitting",
    "Overfitting and Underfitting",
    "Honest Numbers",
    "Two failures that need opposite treatments, and one number that tells you "
    "which one you have.",
    _svg('<path d="M18 68 C50 68, 60 34, 142 26" stroke="var(--accent-primary)" '
         'stroke-width="2" fill="none"/>' +
         '<path d="M18 70 C60 20, 90 78, 142 30" stroke="var(--text-muted)" '
         'stroke-width="2" fill="none" stroke-dasharray="4 3"/>' +
         _dots([(34, 62), (58, 52), (82, 44), (106, 36), (130, 30)], M, 2) +
         _txt(80, 84, "the dashed one memorised the dots", M, 7)),
    [
        ("The gap opening up",
         "One model, six complexities. Watch the training score reach 1.0 and "
         "the test score stop improving.",
         '''from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=500, n_features=20, n_informative=5,
                           random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

print(" depth   train    test     gap")
for depth in (1, 2, 3, 5, 10, None):
    t = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_tr, y_tr)
    tr, te = t.score(X_tr, y_tr), t.score(X_te, y_te)
    print("%6s  %.3f   %.3f   %+.3f" % (depth, tr, te, tr - te))
'''),

        ("validation_curve does the sweep for you",
         "The same picture, cross-validated, in one call.",
         '''from sklearn.model_selection import validation_curve
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=500, n_features=20, n_informative=5,
                           random_state=0)

depths = [1, 2, 3, 5, 8, 12, 20]
train, test = validation_curve(
    DecisionTreeClassifier(random_state=0), X, y,
    param_name="max_depth", param_range=depths, cv=5)

print(" depth   train    test")
for d, tr, te in zip(depths, train.mean(axis=1), test.mean(axis=1)):
    print("%6d  %.3f   %.3f" % (d, tr, te))
print()
print("best depth by cross-validation:", depths[int(np.argmax(test.mean(axis=1)))])
'''),

        ("Would more data help?",
         "learning_curve answers the question that otherwise gets guessed at.",
         '''from sklearn.model_selection import learning_curve
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=2000, n_features=20, n_informative=5,
                           random_state=0)

sizes, train, test = learning_curve(
    LogisticRegression(max_iter=1000), X, y,
    train_sizes=[0.05, 0.1, 0.25, 0.5, 1.0], cv=5)

print("  n_train   train    test")
for n, tr, te in zip(sizes, train.mean(axis=1), test.mean(axis=1)):
    print("%9d  %.3f   %.3f" % (n, tr, te))
print()
print("the two curves converging means more data will not help much;")
print("a wide gap that is still closing means it would.")
'''),

        ("Both failures, on one dataset",
         "The truth is a parabola. Degree 1 cannot bend, and degree 15 bends "
         "to every point it was shown.",
         '''from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import numpy as np

rng = np.random.RandomState(0)
x = np.sort(rng.uniform(-3, 3, 60)).reshape(-1, 1)
y = x.ravel() ** 2 + rng.normal(scale=1.5, size=60)

x_tr, x_te, y_tr, y_te = train_test_split(x, y, test_size=0.4, random_state=0)

print("degree   train R2   test R2")
for deg in (1, 2, 5, 15):
    m = make_pipeline(PolynomialFeatures(deg), LinearRegression()).fit(x_tr, y_tr)
    print("%6d   %8.3f   %7.3f" % (deg, m.score(x_tr, y_tr), m.score(x_te, y_te)))
print()
print("degree 1 underfits, degree 2 is the truth, degree 15 memorises.")
'''),

        ("Variance, measured",
         "How much the model changes when the training data changes - which is "
         "what averaging many models fixes.",
         '''from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import numpy as np

X, y = make_regression(n_samples=300, n_features=10, noise=20.0, random_state=0)

preds = []
for seed in range(5):
    X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.5, random_state=seed)
    preds.append(DecisionTreeRegressor(random_state=0).fit(X_tr, y_tr).predict(X[:5]))
print("one deep tree, 5 refits - spread of the first prediction: %.1f"
      % np.ptp([p[0] for p in preds]))

preds = []
for seed in range(5):
    X_tr, _, y_tr, _ = train_test_split(X, y, test_size=0.5, random_state=seed)
    preds.append(RandomForestRegressor(n_estimators=50, random_state=0)
                 .fit(X_tr, y_tr).predict(X[:5]))
print("a forest of 50,  same 5 refits - spread:                  %.1f"
      % np.ptp([p[0] for p in preds]))
'''),

        ("Three constraints, two of which help",
         "Every one of them lowers the training score. That is the trade, and "
         "it does not always pay.",
         '''from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_validate

X, y = make_classification(n_samples=500, n_features=20, n_informative=5,
                           random_state=0)

settings = [("unconstrained", {}),
            ("max_depth=3", {"max_depth": 3}),
            ("min_samples_leaf=20", {"min_samples_leaf": 20}),
            ("ccp_alpha=0.01", {"ccp_alpha": 0.01})]

print("%-22s %7s %7s %7s" % ("", "train", "test", "gap"))
for label, kw in settings:
    out = cross_validate(DecisionTreeClassifier(random_state=0, **kw), X, y,
                         cv=5, return_train_score=True)
    tr, te = out["train_score"].mean(), out["test_score"].mean()
    print("%-22s %7.3f %7.3f %+7.3f" % (label, tr, te, tr - te))
print()
print("every constraint lowers the training score. Two of them")
print("raise the test score, which is the trade being made.")
'''),
    ],
    [
        "<strong>Overfitting</strong>: training score high, test score much "
        "lower. The model learned the training rows rather than the pattern.",
        "<strong>Underfitting</strong>: both scores low. The model cannot "
        "capture the structure even on data it has seen.",
        "The <strong>gap</strong> between train and test is the diagnostic - "
        "which is why <code class='mono-font'>return_train_score=True</code> is "
        "worth the extra computation.",
        "<code class='mono-font'>validation_curve</code> sweeps one "
        "hyperparameter; <code class='mono-font'>learning_curve</code> sweeps "
        "the amount of data.",
        "More data helps overfitting and does nothing for underfitting - the "
        "learning curve tells you which case you are in.",
        "Every constraint trades training accuracy for generalisation, and the "
        "trade does not always pay.",
    ],
    """title: Overfitting and Underfitting: A Practical Guide
intro: Two failures that look similar in a single number and need opposite treatments. Telling them apart takes one extra column.

## The two failures

Every model sits somewhere on a spectrum between too simple and too complex. Too simple means it cannot capture the pattern in the data. Too complex means it captures the pattern plus the noise. The first is underfitting. The second is overfitting. Telling them apart is the most important diagnostic skill in machine learning.

The fix for overfitting is more constraint: lower depth, stronger regularisation, more data, fewer features. The fix for underfitting is less constraint: higher depth, weaker regularisation, more features, a more flexible model family. Applying the wrong fix makes things worse. Adding regularisation to an underfitting model pushes it further from the pattern.

The diagnostic is the gap between the training score and the test score. A large gap means overfitting. A small gap with a low score means underfitting. This page shows both in practice, with learning curves that make the gap visible as a function of training-set size.

Understanding this trade-off also tells you when to stop tuning. If the training score is high and the test score is close to it, the model is doing as well as it can on this data. More tuning will not help. More or better features might.

**Overfitting** is learning the training data rather than the pattern in it. The model captures noise, coincidences and details exact to the rows it was shown, none of which recur. Training score high, test score much lower.

**Underfitting** is the opposite: the model is too simple, or too constrained, to represent the structure that is there. It does badly on the training data and equally badly on the test data.

Both give a disappointing test score. This Is why a single number can't set apart them. And why the responses are opposite. Overfitting needs a simpler model, more smoothing, or more data. Underfitting needs a more flexible model, better features, or less smoothing. Applying the wrong remedy makes things worse. Guessing is a coin flip.

## The gap is the diagnostic

Compare the training score with the test score.

**Both high, small gap.** Working. Nothing to fix.

**Train high, test much lower.** Overfitting. The size of the gap is roughly how much of the training speed was memorisation.

**Both low, small gap.** Underfitting. The model isn't capturing what is there.

**Train lower than test.** Unusual. Legitimate when smoothing or dropout is active during training but not scoring. Or else a sign the folds aren't close.

`cross_validate(..., return_train_score=True)` gives you both columns. It costs an extra scoring pass per fold and it's the single most helpful arg in the model-pick module. It converts "the score is disappointing" into "the score is disappointing *for this reason*".

The first editor shows the gap opening as a tree is allowed to grow: +0.070 at depth 1, +0.193 unconstrained, with the test score peaking in the middle and then going nowhere while the training score climbs to a perfect 1.000.

## Complexity is the dial

each model has a thing that controls how much structure it can represent.

Tree depth, and the min samples in a leaf. The number of neighbours in k-NN. Fewer neighbours is *more* complex. This Is the one that runs backwards. The degree of a polynomial expansion. The `C` in an SVM or a logistic regression. Here Larger is less smoothed. The number of estimators and the learning rate in a boosting model.

Turn the dial up and the training score rises monotonically. The test score rises, peaks. Falls. The peak is what you're looking for. `validation_curve` finds it by sweeping one param with cross-validation at each setting.

The fourth editor shows both ends on the same data. The truth is a parabola. Degree 1 scores 0.008 on training. It can't bend at all. Degree 2 is right. Degree 15 scores 0.894 on training and **−17.888** on test. This Is far worse than predicting the mean. Is what storing sixty points with sixteen coeffs makes.

## Would more data help?

The question people guess at, and `learning_curve` answers it right by fitting at a few training-set sizes and reporting both scores.

Two shapes matter. **A large gap that is still narrowing** as the training set grows means more data would help. The model has room it can't yet use well. **Two curves that have settled** means more data won't help. The model has extracted what it can. Raising needs a different model or better features.

The third editor shows the settled case: at 80 training samples the gap is 0.900 against 0.798. By 1600 it's 0.844 against 0.838. Collecting another thousand rows would be wasted effort. Knowing that before commissioning the collection is worth a great deal.

The training score falling as the training set grows is normal and often surprises people. Fitting 80 points is easy. Fitting 1600 isn't.

## Bias, variance, and why averaging works

The two failures have formal names. **Bias** is error from a model too rigid to represent the truth. Underfitting. **Variance** is error from a model so flexible that it changes a lot when the training data changes &mdash; overfitting.

Variance is measurable, and the fifth editor measures it. Refitting a single deep choice tree on five different halves of the data moves one guess by 270. The same exercise with a fifty-tree random forest moves it by 48.

That reduction is the entire idea behind ensembles. Each tree is high-variance. The errors are partly free. Blending cancels them. It's why a random forest is almost always better than the tree inside it. Why bagging works on unstable models and does nothing for stable ones.

The classic framing is a trade-off. Modern practice complicates it. Very large models at times improve again past the point of interpolating the training data. For all in this track, the trade-off framing holds. Reducing one often grows the other, and the handy setting is where their sum is smallest.

## The remedies, and that they can fail

For **overfitting**: constrain the model, add smoothing, reduce the number of features, get more data, or use an ensemble to mean the variance away.

For **underfitting**: use a more flexible model, add features or interplays, reduce smoothing, or train for longer if the fit was cut short.

The last editor is worth dwelling on because it shows the trade honestly. Three constraints applied to an overfitting tree. All three lower the training score, as they must. `max_depth=3` and `ccp_alpha=0.01` raise the test score. `min_samples_leaf=20` lowers it, from 0.826 to 0.806. It constrained the model past the handy point and turned overfitting into underfitting.

So "add smoothing" is a direction rather than a fix. The amount has to be found by cross-validation rather than chosen. That is just what the tuning module is for.

## Overfitting the validation set

There's a third failure, and it's the one that catches seen people rather than beginners.

each time you look at a validation score and change a thing in response, you use that score to make a choice. Do it once and the effect is negligible. Do it two hundred times. Trying models, sweeping settings, adding and dropping features, each time keeping what scored better. And the winner has been selected for performing well on those given folds, including on their noise.

The result is a cross-validated score that is optimistic though each single fit was honest. Nothing in the method was wrong. The pick was the leak. It's the same mechanism as picking the best of twenty test scores, just slower and less obviously a mistake.

Three defences. Keep a final test set that is touched just once, at the end, after each choice has been made. Prefer a small number of deliberate checks to a long undirected search. And when the difference between two picks is smaller than the standard deviation across folds, treat them as tied rather than picking a winner. Because at that point you're choosing noise.

Nested cross-validation is the rigorous version: an inner loop tunes and an outer loop scores the whole tuning method. It costs a multiple of the fits and is the right answer when the number being reported matters.

## Signals from the model itself

Besides the gap, three things hint at overfitting before you've measured any of it.

**coeffs that are huge.** A linear model whose coeffs run to thousands is weighing large plus and minus terms that nearly cancel. A fit that is precariously tuned to the training rows. Smoothing exists to prevent just this. The size of the coeffs is a reasonable proxy for how much is needed.

**A tree with as many leaves as samples.** If `tree.get_n_leaves()` is close to the number of training rows, each leaf is one or two samples and the model is a lookup table.

**Scores that move a lot between folds.** A high standard deviation across cross-validation folds means the model is sensitive to which rows it saw. This Is variance by meaning.

None of these is conclusive on its own. All three are cheap to check and worth a glance before the more costly diagnosis.

<strong>Is a perfect training score always bad?</strong> Not by itself. An unconstrained tree reaches 1.0 by build. It's bad when the test score is far below it.

<strong>Does more data ever cause overfitting?</strong> No - more data only ever helps generalisation. More *features* on the same rows is what makes it worse.

<strong>Which comes first, tuning or feature work?</strong> often features. A learning curve that has settled says the model has extracted what it can. No amount of tuning changes that.

<strong>What is ccp_alpha?</strong> Cost-cost pruning: it grows the tree fully and then drops branches whose part isn't worth their cost. Often better than capping the depth. It prunes where pruning helps rather than all over.

## Which dial belongs to which model

The cost control has a different name in each estimator. This Makes the general idea harder to see than it should be. The mapping is worth having in one place.

**choice trees.** `max_depth` caps how many questions can be asked. `min_samples_leaf` and `min_samples_split` stop the tree splitting groups that are already small. Often a better control than depth. It reacts to the data rather than to a fixed count. `ccp_alpha` prunes after growing.

**Random forests.** The same tree params, plus `n_estimators`. This Is the one that does *not* overfit. More trees only ever helps, at the cost of time. `max_features` controls how decorrelated the trees are and is the main variance dial.

**Grad boosting.** `learning_rate` and `n_estimators` trade against each other. A smaller rate needs more trees and generalises better. `max_depth` is kept small, often 3 to 6. The ensemble supplies the flexibility.

**Linear models.** `alpha` in Ridge and Lasso. Here Larger is more smoothed. `C` in `LogisticRegression` and the SVMs. Here Larger is *less* smoothed. The one inversion in the library. The reason to check which you're holding.

**k-NN.** `n_neighbors`, where more neighbours is a simpler model. This runs backwards from most intuitions about "bigger numbers mean more".

**Polynomial features.** `degree`, which grows cost faster than any of it else on this list. Degree 3 on ten features is 286 columns.

The pattern underneath: each one of these controls how much of the training data the model is permitted to represent just.

<strong>Can a model overfit with only a few features?</strong> Yes. Degree-15 polynomial features on one input column scored -17.888 on test in the fourth editor. What matters is flexibility scaled to the number of rows, not the raw column count.

<strong>Do I fix underfitting by dropping smoothing fully?</strong> Try it to confirm the diagnosis, then find the amount by cross-validation. Zero is rarely the best value.

## Things to try

1. <strong>Watch the gap grow.</strong> The first editor's last column goes from +0.070 to +0.193 while the test score stops raising after depth 3.
2. <strong>Find the peak.</strong> In the second editor, note that the training score keeps rising after the test score has stopped. That divergence is the meaning.
3. <strong>Ask whether data would help.</strong> In the third editor, cut `n_samples` to 300 and see whether the curves have settled by then.
4. <strong>Over-constrain on purpose.</strong> In the last editor, try `min_samples_leaf=100` and watch both scores fall together.

## Where this leaves you

One extra column tells you which failure you've. `validation_curve` finds the right cost, `learning_curve` says whether more data would help. Each constraint is a trade that has to be measured rather than assumed.
""",
    [
        {"q": "Training accuracy 1.00, test accuracy 0.72. What is happening?",
         "options": ["Underfitting", "Overfitting", "A bad metric", "Data leakage"],
         "answer": 1,
         "why": "A large gap with a perfect training score means the model learned the rows rather than the pattern. Both scores being low would be underfitting."},
        {"q": "What does return_train_score=True buy you?",
         "options": ["A more accurate model",
                     "The gap, which distinguishes overfitting from underfitting",
                     "Faster cross-validation",
                     "Better hyperparameters"],
         "answer": 1,
         "why": "The two failures look identical in a test score alone and need opposite remedies. The train column is what tells them apart."},
        {"q": "The learning curve's train and test scores have converged. What does that mean?",
         "options": ["The model is overfitting",
                     "More data will not help much",
                     "The model needs more regularisation",
                     "The split is wrong"],
         "answer": 1,
         "why": "Converged curves mean the model has extracted what it can from data of this kind. Improving needs a different model or better features."},
        {"q": "Why does a random forest have lower variance than one deep tree?",
         "options": ["The trees are shallower",
                     "Averaging many partly independent models cancels their errors",
                     "It uses fewer features",
                     "It regularises each tree"],
         "answer": 1,
         "why": "Measured in the editor: one tree's prediction moved by 270 across refits, the forest's by 48. That averaging is the point of bagging."},
    ],
)


# ---------------------------------------------------------------------------
# 17. Decision trees
# ---------------------------------------------------------------------------
topic(
    "decision_trees",
    "Decision Trees",
    "Models",
    "The one model you can read end to end - and the one whose answer changes "
    "when you resample the data.",
    _svg(_box(64, 14, 32, 16, S, A) + _txt(80, 25, "x &lt; 2?", A, 7) +
         _arrow(72, 32, 46, 44) + _arrow(88, 32, 114, 44) +
         _box(30, 46, 32, 16, S, M) + _txt(46, 57, "class 0", M, 7) +
         _box(98, 46, 32, 16, S, M) + _txt(114, 57, "x &lt; 7?", M, 7) +
         _arrow(106, 64, 92, 74) + _arrow(122, 64, 136, 74) +
         _box(76, 74, 32, 14, S, M) + _box(122, 74, 30, 14, S, M)),
    [
        ("The whole model, printed",
         "No other estimator can do this - the fitted model is a set of "
         "questions you can read.",
         '''from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.datasets import load_iris

data = load_iris()
tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(data.data,
                                                               data.target)

print(export_text(tree, feature_names=list(data.feature_names)))
print("that is the entire model - a set of if/else questions")
'''),

        ("Which features it actually used",
         "feature_importances_ sums to 1, and features never split on get "
         "exactly zero.",
         '''from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris

data = load_iris()
tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(data.data,
                                                               data.target)

for name, imp in sorted(zip(data.feature_names, tree.feature_importances_),
                        key=lambda p: -p[1]):
    print("%-22s %.4f" % (name, imp))
print()
print("sum:", round(tree.feature_importances_.sum(), 6))
print("two of the four features are never used at all")
'''),

        ("The split criterion barely matters",
         "Which is worth knowing, because it is the parameter people reach for "
         "first and the one that changes least.",
         '''from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score

X, y = load_iris(return_X_y=True)

print("criterion   accuracy")
for crit in ("gini", "entropy", "log_loss"):
    s = cross_val_score(DecisionTreeClassifier(criterion=crit, random_state=0),
                        X, y, cv=5).mean()
    print("%-11s %.4f" % (crit, s))
print()
print("the split rule almost never matters. depth and leaf size do.")
'''),

        ("One tree is unstable",
         "Six resamples of the same data, six trees, and they do not agree.",
         '''from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
import numpy as np

X, y = make_classification(n_samples=200, n_features=8, n_informative=4,
                           n_redundant=2, random_state=0)
rng = np.random.RandomState(0)

firsts, preds = [], []
for _ in range(6):
    idx = rng.choice(len(X), len(X), replace=True)      # a bootstrap sample
    t = DecisionTreeClassifier(random_state=0).fit(X[idx], y[idx])
    firsts.append(int(t.tree_.feature[0]))
    preds.append(t.predict(X[:40]))

print("feature chosen for the first split, six resamples:", firsts)
disagree = sum(len(set(col)) > 1 for col in zip(*preds))
print("of 40 rows, predictions disagree on:", disagree)
print()
print("resampling the same data changes the tree's structure and")
print("its answers. That instability is what a forest averages away.")
'''),

        ("It cannot extrapolate",
         "A perfectly straight line, and a tree asked about values past the "
         "end of the training range.",
         '''from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
import numpy as np

x = np.arange(0, 20).reshape(-1, 1).astype(float)
y = 3.0 * x.ravel()                    # a perfectly straight line

tree = DecisionTreeRegressor(max_depth=3, random_state=0).fit(x, y)
lin = LinearRegression().fit(x, y)

future = np.array([[25.0], [30.0]])
print("truth at x=25, 30 :", [75.0, 90.0])
print("linear model      :", lin.predict(future).round(1).tolist())
print("decision tree     :", tree.predict(future).round(1).tolist())
print()
print("a tree predicts the average of a training leaf, so it cannot")
print("extrapolate beyond the range it was shown.")
'''),

        ("Units are irrelevant to it",
         "One column multiplied by a million, and the cross-validated score "
         "does not move at all.",
         '''from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=300, n_features=8, n_informative=3,
                           random_state=0)

base = cross_val_score(DecisionTreeClassifier(random_state=0), X, y, cv=5).mean()

X2 = X.copy()
X2[:, 0] *= 1_000_000
scaled = cross_val_score(DecisionTreeClassifier(random_state=0), X2, y, cv=5).mean()

print("original            :", round(base, 4))
print("one column x1000000 :", round(scaled, 4))
print()
print("splits are thresholds on one column, so any monotonic change")
print("of units leaves the tree identical.")
'''),
    ],
    [
        "A tree is a sequence of yes/no questions on one feature at a time; "
        "<code class='mono-font'>export_text</code> prints the whole model.",
        "It needs <strong>no scaling</strong> and handles mixed feature ranges, "
        "because a split is a threshold on a single column.",
        "It captures interactions and non-linearity without being told to look "
        "for them, which is why trees dominate on tabular data.",
        "Left unconstrained it grows until every leaf is pure - a training score "
        "of 1.0 and a lookup table.",
        "It is <strong>unstable</strong>: resampling the data changes the "
        "structure, which is exactly what ensembles average away.",
        "It cannot extrapolate - predictions outside the training range are the "
        "nearest leaf's average, flat forever.",
    ],
    """title: Decision Trees: A Practical Guide
intro: The only model in this track whose fitted form a person can read and check. That readability comes with an instability that shows why trees are almost always used in groups.

## How it works

Decision trees are one of the most interpretable models in machine learning. You can print the tree, read the splits, and explain every prediction to someone with no technical background. That transparency is why they remain popular even when other models score higher.

A decision tree learns a set of if-then rules from the data. Each rule tests one feature against one threshold. The rules are arranged in a tree structure: the first rule splits all the data, each subsequent rule splits a subset. At the bottom, each leaf holds a prediction.

Trees require no scaling and handle both numeric and categorical features naturally. They are fast to train, fast to predict, and easy to visualise. They also overfit aggressively. An unconstrained tree will memorise the training data perfectly. Controlling depth, minimum samples per leaf and minimum impurity decrease is how you trade accuracy for generalisation.

Understanding trees matters even if you plan to use random forests or gradient boosting. Both are built from trees. The parameters that control a single tree -- `max_depth`, `min_samples_leaf`, `min_samples_split` -- are the same parameters that control the trees inside an ensemble.

A choice tree asks a series of yes/no questions about one feature at a time. Each answer sends the sample down a branch. At the bottom, a leaf holds a guess. The majority class for a classifier, the mean target for a regressor.

Fitting means choosing the questions. At each node the method tries each feature and each threshold, scores how well each split separates the classes. Keeps the best. Then it repeats on each side, recursively, until a stopping rule fires.

The scoring function is `criterion`. Gini or entropy for classification, squared error for regression. It's the param people reach for first and the one that matters least. The editor above shows the three classification criteria within half a point of each other. This Is common. Depth and leaf size are the params that change the model.

## What makes trees attractive

**They're readable.** `export_text` prints the entire model. For a shallow tree that output is a thing a domain expert can check line by line. No other model in this track offers that. When somebody has to justify a choice. A loan refusal, a clinical flag. Being able to point at the path a case took is worth a great deal.

**They need no preparation.** No scaling. A split is a threshold on one column and units can't affect which threshold is best. The last editor times a column by a million and the cross-validated score doesn't move by a thousandth. No distributional assumptions. Outliers affect only the leaf they land in.

**They find structure without being told.** Interplays between features come for free. A split lower in the tree is conditioned on each split above it. Non-linear boundaries come for free, because a staircase of thresholds approximates any shape. A linear model needs to be handed `x1 * x2` and `x**2` by name. A tree discovers both.

**They handle mixed data.** Numeric and cat features side by side, no common scale needed.

## What makes one tree a poor final answer

**Left alone, it stores.** The default stopping rule is to keep splitting until each leaf is pure. This On any dataset with noise means one leaf per training row. Training fit 1.0. A lookup table. each tree needs constraining. This Is what `max_depth`, `min_samples_leaf` and `ccp_alpha` are for.

**It's unstable.** This is the deeper problem. The fourth editor takes six bootstrap resamples of the same data, fits a tree to each. Finds them disagreeing on 18 of 40 guesses. With the first split falling on a different feature in one of the six.

The cause is the greedy fitting. The best split is chosen at each node without regard to what comes below. When two pick splits score nearly the same, a handful of resampled rows decides between them. That choice then finds all underneath. A small change at the top rewrites the whole tree.

The consequence is that a single tree's structure shouldn't be over-read. "The model says petal width is the key variable" is a statement about one fit on one sample. A different sample might have said a thing else.

**It can't extrapolate.** A leaf predicts an mean of training values. Beyond the range of the training data a tree returns a constant. The fifth editor fits a perfect straight line and asks for values past the end. The linear model gives 75 and 90, right. The tree gives 54 for both. For any of it with a trend. Time, growth, prices. This is disqualifying on its own.

**Axis-aligned splits.** Each split is on one feature. A main-line boundary has to be approximated by a staircase. Trees handle it, inefficiently. A linear model handles a main-line just.

## Feature importances, and their bias

`feature_importances_` reports how much each feature reduced the impurity across all the splits it appears in, normed to sum to 1. Features never split on get just zero. This Is a truly handy signal. The editor above shows two of iris's four features unused.

Three cautions before trusting the numbers.

**Linked features split the credit arbitrarily.** If two columns carry the same info, whichever is chosen first takes the importance and the other looks worthless. Neither is. The split between them isn't stable.

**High-cardinality features are favoured.** A column with many distinct values offers more pick thresholds and so more chances to look good on the training data. This is the impurity-based measure's known bias. It inflates the apparent importance of ids and smooth variables scaled to binary ones.

**It's measured on the training data.** A feature that helped fit noise still scores.

`permutation_importance` avoids all three by measuring the drop in test-set score when a column is shuffled. It costs more and answers the question people really mean.

## Constraining it

Four params, of which the middle two are often the most handy.

`max_depth` caps the number of questions. Simple, blunt, and the first thing to try.

`min_samples_leaf` refuses to create a leaf with fewer than n samples. This is often better than depth. It reacts to the density of the data rather than imposing a fixed count. A tree can stay deep where there's data to support it.

`min_samples_split` is the related control on splitting rather than on the resulting leaves.

`ccp_alpha` grows the tree fully and then prunes back branches whose part doesn't justify their cost. It's the most principled of the four. The overfitting module found it giving the best test score of three constraints tried.

The right values are found by cross-validation, not chosen. The overfitting module also showed that a constraint can make things worse: `min_samples_leaf=20` lowered the test score on data where `max_depth=3` raised it.

## Where a single tree belongs

Rarely as the final model. A random forest or a grad booster beats it on almost any dataset. The next modules cover both.

It belongs when the model has to be shown. A shallow tree is a flowchart somebody can audit. That is at times the need. It belongs as a fast baseline that tells you whether the problem has non-linear structure. And it belongs as the thing to understand first. Forests and boosting are both built out of trees. Their params are largely tree params.

## Categorical features, and the one that is missing

scikit-learn's `DecisionTreeClassifier` can't take a string column. It needs numbers. This Means cat features have to be coded before they reach it. And the choice of encoding interacts badly with how trees split.

One-hot encoding a category with twenty values gives the tree twenty binary columns. A split on a binary column separates one category from the other nineteen. Isolating a group of three categories then takes three levels of depth. This The depth budget has to pay for. The tree can express it. It's just costly.

Ordinal encoding gives one column and lets a single threshold separate a contiguous run of categories. But the run is contiguous in what any order the encoder chose. The groups it can form cheaply are the wrong groups.

Neither is the native answer. This Is to consider any subsets of categories at each split. `HistGradientBoostingClassifier` supports that through `categorical_features`. It's a genuine reason to prefer it on data with many categories. LightGBM and CatBoost handle it too. It's one of the things they're known for.

For a plain tree with a handful of categories, one-hot and enough depth is fine. For a high-cardinality column, it's a real limitation rather than a detail.

## Reading the structure programmatically

Beyond `export_text`, the fitted tree exposes its structure through `tree_`. A few fields answer handy questions right.

`tree_.node_count` and `get_n_leaves()` say how large the model is. A leaf count approaching the number of training rows is the clearest signal of memorisation available, and it costs one call.

`tree_.feature` and `tree_.threshold` are arrays giving, per node. This Feature was split on and at what value. Which is how the instability demo above read the first split without parsing text.

`get_depth()` says how deep it really grew. This Is often less than `max_depth` when another constraint bound first.

`decision_path(X)` returns which nodes each sample passed through. This Is the basis of any per-guess explanation. For a given row, the path is the reason.

These matter because they turn "the tree looks complicated" into numbers. A tree with 300 leaves on 400 training rows doesn't need a diagnosis. The leaf count is the diagnosis.

<strong>Is gini or entropy better?</strong> Neither, . They agree on almost each split and differ by a fraction of a point. Spend the effort on depth and leaf size.

<strong>Can a tree do regression?</strong> Yes - `DecisionTreeRegressor` predicts the mean of each leaf. The output is a step function. This Is why it can't extrapolate.

<strong>Should I prune or cap the depth?</strong> `ccp_alpha` prunes where pruning helps, rather than truncating all over at the same level. It often does better. It costs one more setting to tune.

<strong>Why is my tree different each run?</strong> Ties between equally good splits are broken at random. `random_state` fixes it. that it matters is the instability in miniature.

## What "greedy" means, and why it matters

The fitting method is greedy: at each node it picks the split that looks best *right now*, without considering what splits become available afterwards.

That is a real limitation rather than an setup shortcut. Finding the truly best tree. The smallest one reaching a given fit. Is computationally unsolvable for any realistic dataset. Each hands-on setup is greedy. The consequence is that a tree can miss structure that needs two splits to reveal. If neither of a pair of features looks handy alone. But Their combination separates the classes just right, the greedy step may never take the first one.

The classic example is exclusive-or. With two binary features where the answer is "one but not both", neither feature alone carries any info at all. The first split scores nothing on either. A tree will eventually get there on real data with noise to guide it. It takes more depth than the structure warrants.

This also shows the instability from the other direction. When two pick splits score nearly the same way, the greedy choice between them is decided by whichever is fractionally better on this given sample. And all below inherits that any choice.

Ensembles help here too, and not only by blending. A random forest restricts each split to a random subset of features. This Forces different trees to take different first steps and at times finds the structure a single greedy path would have missed.

## Things to try

1. <strong>Read the model.</strong> The first editor prints the whole thing. Raise the depth to 4 and watch it stop being readable.
2. <strong>Watch the instability.</strong> In the fourth editor, change `random_state` on the resampler and see how much the six trees disagree this time.
3. <strong>Confirm the flat line.</strong> In the fifth editor, ask for x=100. The tree still says 54.
4. <strong>Compare the importances.</strong> Fit at depth 1 and at depth 5 and see how the numbers redistribute.

## Where this leaves you

A model you can read, that needs no preparation, that finds interplays on its own, that stores unless constrained, that changes when you resample. That can't see past the edge of its training data. The next two modules address the instability by using many of them at once.
""",
    [
        {"q": "Why do decision trees not need feature scaling?",
         "options": ["They scale internally",
                     "A split is a threshold on one column, so units cannot change which split is best",
                     "They only accept scaled input",
                     "They do need it"],
         "answer": 1,
         "why": "Multiplying a column by a million left the cross-validated score identical to the fourth decimal."},
        {"q": "What does an unconstrained decision tree do to the training data?",
         "options": ["Underfits",
                     "Splits until leaves are pure, reaching a training score of 1.0",
                     "Stops at depth 10",
                     "Selects features automatically"],
         "answer": 1,
         "why": "The default stopping rule is purity, which on noisy data means roughly one leaf per row - a lookup table."},
        {"q": "What happens when a tree regressor is asked about values beyond its training range?",
         "options": ["It extrapolates the trend",
                     "It returns the nearest leaf's average, flat forever",
                     "It raises an error",
                     "It returns NaN"],
         "answer": 1,
         "why": "On a perfect straight line the tree predicted 54 for both x=25 and x=30, where the truth was 75 and 90."},
        {"q": "Why is feature_importances_ unreliable for correlated features?",
         "options": ["It is computed on the test set",
                     "Whichever is split on first takes the credit and the other looks worthless",
                     "It does not sum to 1",
                     "It ignores categorical features"],
         "answer": 1,
         "why": "The credit goes to whichever was chosen, and that choice is unstable. permutation_importance measures the question people actually mean."},
    ],
)


# ---------------------------------------------------------------------------
# 18. Random forests
# ---------------------------------------------------------------------------
topic(
    "random_forests",
    "Random Forests",
    "Models",
    "Many unstable trees, deliberately made to disagree, averaged into "
    "something stable - and the strongest default on tabular data.",
    _svg("".join(_box(14 + i * 34, 30, 26, 30, S, A if i == 1 else M, 2)
                 for i in range(4)) +
         _txt(80, 20, "many trees, each on different data", M, 7) +
         _arrow(80, 64, 80, 76) + _txt(80, 86, "average the votes", A, 8)),
    [
        ("More accurate, and far more stable",
         "The accuracy gain is modest. The stability gain is the real one, and "
         "it has to be measured across refits rather than across folds.",
         '''from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
import numpy as np

X, y = make_classification(n_samples=600, n_features=20, n_informative=6,
                           random_state=0)

print("accuracy:")
print("  one tree :", round(cross_val_score(DecisionTreeClassifier(random_state=0),
                                            X, y, cv=5).mean(), 4))
print("  a forest :", round(cross_val_score(RandomForestClassifier(random_state=0),
                                            X, y, cv=5).mean(), 4))

# The variance that averaging removes is in the predictions, not in the
# fold scores - so measure it by refitting on resampled data.
rng = np.random.RandomState(0)
for label, make in [("one tree", lambda: DecisionTreeClassifier(random_state=0)),
                    ("a forest", lambda: RandomForestClassifier(n_estimators=50,
                                                                random_state=0))]:
    preds = []
    for _ in range(5):
        idx = rng.choice(len(X), len(X), replace=True)
        preds.append(make().fit(X[idx], y[idx]).predict(X[:60]))
    disagree = sum(len(set(col)) > 1 for col in zip(*preds))
    print("%-10s disagrees with itself on %2d of 60 rows across refits"
          % (label, disagree))
'''),

        ("n_estimators is the one free parameter",
         "Raising it cannot overfit. It only costs time.",
         '''from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=500, n_features=20, n_informative=5,
                           random_state=0)

print("n_estimators   accuracy")
for n in (1, 5, 25, 100, 300):
    s = cross_val_score(RandomForestClassifier(n_estimators=n, random_state=0),
                        X, y, cv=5).mean()
    print("%12d   %.4f" % (n, s))
print()
print("one tree is much worse; after about 25 the differences are")
print("fold noise. more trees costs time and does not overfit -")
print("it is the one parameter you can raise without a trade.")
'''),

        ("Two importances, one of them misleading",
         "A pure-noise column with many distinct values, and the built-in "
         "measure gives it more credit than the other noise column.",
         '''from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
import numpy as np

rng = np.random.RandomState(0)
n = 500
signal = rng.normal(size=n)
X = np.column_stack([
    signal,                              # genuinely useful
    rng.normal(size=n),                  # noise
    rng.randint(0, 400, size=n),         # noise, many distinct values
])
y = (signal > 0).astype(int)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
rf = RandomForestClassifier(random_state=0).fit(X_tr, y_tr)

names = ["signal", "noise", "noise_many_values"]
perm = permutation_importance(rf, X_te, y_te, n_repeats=10, random_state=0)
print("%-20s %10s %12s" % ("", "impurity", "permutation"))
for i, nm in enumerate(names):
    print("%-20s %10.4f %12.4f"
          % (nm, rf.feature_importances_[i], perm.importances_mean[i]))
print()
print("impurity gives both noise columns a score, and more to the one")
print("with more distinct values. permutation gives both exactly zero.")
'''),

        ("A free estimate, without a second fit",
         "Each tree misses about a third of the rows, so those rows can score "
         "it.",
         '''from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=600, n_features=20, n_informative=6,
                           random_state=0)

rf = RandomForestClassifier(n_estimators=200, oob_score=True,
                            random_state=0).fit(X, y)

print("out-of-bag score      :", round(rf.oob_score_, 4))
print("5-fold cross-validated:",
      round(cross_val_score(RandomForestClassifier(n_estimators=200,
                                                   random_state=0),
                            X, y, cv=5).mean(), 4))
print()
print("each tree is scored on the rows its bootstrap sample left out,")
print("which gives an estimate for the cost of a single fit.")
'''),

        ("max_features is the decorrelation dial",
         "Letting every tree see every feature makes them agree, and agreement "
         "is what averaging cannot fix.",
         '''from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score

X, y = make_classification(n_samples=400, n_features=30, n_informative=8,
                           random_state=0)

print("max_features   accuracy")
for mf in ("sqrt", 0.5, None):
    s = cross_val_score(RandomForestClassifier(n_estimators=50, max_features=mf,
                                               random_state=0), X, y, cv=5).mean()
    print("%12s   %.4f" % (str(mf), s))
print()
print("None means every tree sees every feature, so the trees resemble")
print("each other more and the averaging buys less.")
'''),

        ("Still cannot extrapolate",
         "The one limitation the ensemble inherits whole from its trees.",
         '''from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import numpy as np

x = np.arange(0, 20).reshape(-1, 1).astype(float)
y = 3.0 * x.ravel()

rf = RandomForestRegressor(n_estimators=50, random_state=0).fit(x, y)
lin = LinearRegression().fit(x, y)

future = np.array([[25.0], [40.0]])
print("truth at x=25, 40 :", [75.0, 120.0])
print("linear            :", lin.predict(future).round(1).tolist())
print("random forest     :", rf.predict(future).round(1).tolist())
print()
print("averaging many trees does not fix extrapolation - every tree")
print("is flat past the edge, so the average is too.")
'''),
    ],
    [
        "Each tree is fitted on a <strong>bootstrap sample</strong> and picks "
        "each split from a <strong>random subset of features</strong> - two "
        "sources of disagreement, deliberately introduced.",
        "Averaging cancels errors that are independent, so the more the trees "
        "differ, the more the averaging buys.",
        "<code class='mono-font'>n_estimators</code> cannot overfit; more trees "
        "only cost time.",
        "<code class='mono-font'>oob_score=True</code> gives an estimate from "
        "the rows each tree did not see, for the price of a single fit.",
        "<code class='mono-font'>feature_importances_</code> is biased towards "
        "high-cardinality columns - "
        "<code class='mono-font'>permutation_importance</code> answers the "
        "question people mean.",
        "It inherits the tree's inability to extrapolate: predictions past the "
        "training range are flat.",
    ],
    """title: Random Forests: A Practical Guide
intro: The previous module ended with a model that changes its mind when you resample the data. This one fixes that by building hundreds of them and taking a vote.

## The idea

A random forest is an ensemble of decision trees. It fits many trees on slightly different versions of the data and averages their predictions. The average is almost always more accurate than any single tree.

Random forests are the default first model for many practitioners. They work on classification and regression, handle numeric and categorical features, require little tuning, and resist overfitting better than single trees. On tabular data, they are competitive with gradient-boosted trees and far simpler to configure.

The forest's main parameter is the number of trees. More trees give a better average, up to a point of diminishing returns. The cost is linear in the number of trees, but the trees are independent and can be fitted in parallel across CPU cores.

A single choice tree is unstable: the greedy choice at each node is decided by a handful of rows. A different sample makes a different tree. That instability is variance, and variance is error.

Blending free guesses reduces variance. If the trees made *the same* errors, blending would achieve nothing. If their errors are partly free, the errors cancel and the signal lives. So the whole design problem is making the trees disagree.

A random forest adds disagreement twice.

**Bootstrap sampling.** Each tree is fitted on a sample of the training rows drawn with swap, the same size as the first. About 63% of the rows appear in any given sample. Each tree sees a different subset.

**Random feature subsets.** At each split, the tree considers only a random subset of the features rather than all of them. This is the more key of the two. It's what sets apart a random forest from plain bagging.

The second matters because bootstrapping alone leaves the trees too similar. If one feature is strongly predictive, each tree splits on it first and the trees end up nearly the same. Restricting the choice forces different trees down different paths. This Is just the freedom the blending needs.

## What it buys

The fit improvement is real and often modest. 0.79 to 0.83 in the first editor.

The steadiness improvement is the larger one. It has to be measured properly. Fold-to-fold variation in a cross-validation score is *not* it. That measures how much the score depends on which rows were held out, and a forest isn't above all better there. What blending fixes is how much the *model* changes when the training data changes.

The first editor measures that right: refitting on five bootstrap resamples, one tree disagrees with itself on 14 of 60 rows. A fifty-tree forest on 6. That is the variance reduction. It's why a forest's guesses can be leaned on in a way a single tree's can't.

## The parameters worth setting

`n_estimators` is unusual: **it can't overfit**. More trees means a better guess of the mean. This Settles rather than degrading. The only cost is time and memory. a thing like 100 to 500 is normal. The editor above shows the curve flattening after about 25. Past which the differences are fold noise rather than improvement.

That makes it the one cost-shaped param with no trade-off. This Is worth stating because it runs against the pattern of all else in the track.

`max_features` controls the decorrelation. `"sqrt"` is the default for classification and is often right. Setting it to `None` gives each tree each feature. The third editor shows the cost: 0.8500 against 0.8650. The trees became too alike. Lower values mean more diverse and on their own weaker trees. This Is often a good trade.

`max_depth` and `min_samples_leaf` are inherited from the tree. A forest needs them far less. Single trees are allowed to overfit. Their overfitting is unlinked and means out. Leaving them unconstrained is a reasonable default. Constraining them slightly can help on small or very noisy data.

`n_jobs=-1` fits the trees in parallel across cores. The trees are free. This is close to free.

## Out-of-bag scoring

Because each tree misses about 37% of the rows, those rows can score it. And blending that across trees gives a validation guess without a separate fit.

`oob_score=True` finds it, and `oob_score_` holds the result. The editor above gives 0.8683 against a cross-validated 0.8383. This Is the usual tie: OOB tends to run slightly optimistic scaled to k-fold. Each OOB guess comes from the subset of trees that missed that row rather than from a full forest.

It's truly handy when fitting is costly. It costs nothing beyond the fit you were doing anyway. It isn't a swap for cross-validation when you're checking models or tuning, both because of the optimism and because it only exists for bagged ensembles.

## Feature importances, and the trap

`feature_importances_` is the field people reach for. It has a known bias worth seeing rather than being told about.

The third editor gives a forest three columns. One carrying the signal, one pure noise. One pure noise with 400 distinct values. The impurity-based measure gives the signal 0.89. Correct. And then gives both noise columns a non-zero score, with **more** going to the one with more distinct values.

The cause is that a column with many possible thresholds gets many chances to look good on the training data. Impurity importance is found on the training data. `permutation_importance`. This Measures how much the *test* score drops when a column is shuffled, gives both noise columns just 0.0000.

Two further cautions apply to both measures. Linked features split the credit arbitrarily. A truly key feature can look weak because a linked one absorbed it. And importance isn't causation. It says the model used the column, not that the column drives the outcome.

The hands-on rule: use permutation importance when the answer matters, on the test set. Treat the built-in field as a rough first look.

## What it does not fix

**Extrapolation.** each tree is flat past the edge of its training range. The mean of many trees is flat too. The last editor asks for x=25 and x=40 on a perfect straight line and gets 55.3 for both. No number of trees changes this. It disqualifies forests for any of it with a trend unless the trend is removed first.

**Readability.** A single shallow tree can be printed and audited. Three hundred trees can't. The model turns a black box that happens to be made of transparent parts.

**Size and speed.** A forest holds each tree. A model fitted on a large dataset can be hundreds of megabytes. Guess means traversing each tree.

**Extreme sparsity.** On very high-dimensional sparse data. Text, mostly &mdash; linear models often win.

## Where it sits

A random forest is the strongest thing you can fit with no tuning. That is its main claim. Defaults plus `n_estimators=200` makes a competitive model on most tabular problems, needing no scaling, no encoding choices beyond making the columns numeric, and no search.

Grad boosting often beats it given tuning effort. Grad boosting *needs* that effort. A badly tuned booster is worse than a default forest. The sensible sequence is a linear model for the baseline, a forest for the strong default. Boosting when the difference is worth the work.

## The rest of the bagging family

Three near relatives share the design and differ in one choice each. Knowing what separates them saves trying all four blindly.

`ExtraTreesClassifier` &mdash; extremely randomised trees &mdash; goes further than a forest. Rather than searching for the best threshold on each pick feature, it picks thresholds at random and keeps the best of those. That makes each tree weaker and the trees more different. This At times wins and is always faster to fit. The costly threshold search disappears. It's worth trying when a forest is your best model. It takes one word to swap.

`BaggingClassifier` is the general form: bootstrap samples and blending, wrapped around *any* estimator. A forest is bagging plus feature subsetting, specialised to trees. Bagging a linear model reaches almost nothing. Linear models are stable and there's no variance to mean away. Which is the clearest statement of when the technique applies at all.

`RandomForestRegressor` is the same method predicting the mean of each leaf rather than the majority class. All on this page transfers, including the extrapolation limit. This Bites harder in regression because a flat guess past the training range is more obviously wrong than a class label.

The pattern: bagging reduces variance and does nothing for bias. It helps unstable, low-bias models. Deep trees. And wastes time on stable ones.

## Costs worth knowing before deploying one

A forest is cheap to fit and costly to keep.

**Memory.** each tree is stored in full. A forest of 500 unconstrained trees on a hundred thousand rows can run to hundreds of megabytes. The pickle is the same size. Constraining `max_depth` or `min_samples_leaf` shrinks it a lot at a small fit cost. This Is often the right trade for a thing that has to be shipped.

**guess latency.** each guess traverses each tree. That is fast per tree and adds up: 500 trees is 500 traversals. For batch scoring it's irrelevant. For a request-response service with a latency budget it can decide the design.

**Fitting time** scales with trees times rows times features. Parallelises almost just right with `n_jobs=-1`.

The lever for all three is the same. Fewer, shallower trees. Measuring how much fit that really costs, rather than given, often shows the curve is flat well below the default.

<strong>How many trees should I use?</strong> Enough that the score has flattened - often 100 to 500. Plot it once for your data and stop where the curve does.

<strong>Does a forest need scaling?</strong> No, for just the reason a single tree doesn't: splits are thresholds on one column.

<strong>Are the chances from predict_proba trustworthy?</strong> They're the proportion of trees voting for each class. This Ranks well and is systematically pushed towards the middle. Calibrate if you need them as numbers.

<strong>Can it handle missing values?</strong> Not in scikit-learn - impute first, or use `HistGradientBoosting`. This Handles them natively.

## Why averaging works at all

The mechanism is worth one paragraph of math. It shows just when the technique helps and when it does nothing.

Blending `n` guesses whose errors are fully free cuts the variance by `n`. Blending `n` guesses whose errors are the same cuts it by nothing at all. The mean is the same as any one of them. Real ensembles sit between. The variance falls towards a floor set by how much the members share. No number of extra members goes below that floor.

That single fact shows each design choice in a random forest. Bootstrap sampling and feature subsetting exist to push the link between trees down. The link is what sets the floor. It shows why `max_features=None` performs worse. The trees become too alike and the floor rises. It shows why more trees stop helping. You approach the floor and then sit on it.

It also shows what bagging can't do. Blending drops variance and leaves **bias** untouched. If each tree is systematically wrong in the same direction. Is the mean. That is why a forest can't extrapolate. each tree is flat past the training range, that flatness is bias rather than variance. Blending the same flatness gives flatness.

Boosting attacks the other half of the problem, fitting each new model to what the previous ones got wrong. This Reduces bias and is why it needs more careful tuning to avoid the variance coming back.

## Things to try

1. <strong>Watch the steadiness.</strong> The first editor's last two lines are the point: 14 rows against 6.
2. <strong>Push the trees up.</strong> In the second editor, add 1000 and confirm the score doesn't fall.
3. <strong>Compare the importances.</strong> The third editor's two columns disagree about a column that is pure noise.
4. <strong>Break the decorrelation.</strong> In the fifth editor, try `max_features=1` and see whether so much range starts to hurt.

## Where this leaves you

Many on purpose different trees, averaged. More trees never hurt, `max_features` is the dial that matters, out-of-bag scoring is free, the built-in importances are biased towards many-valued columns. The whole thing still can't see past the edge of its training data.
""",
    [
        {"q": "What are the two sources of randomness in a random forest?",
         "options": ["Random initial weights and random splits",
                     "Bootstrap row samples and a random feature subset at each split",
                     "Random depth and random criterion",
                     "Random test sets"],
         "answer": 1,
         "why": "Bootstrapping alone leaves the trees too similar when one feature dominates; restricting the features at each split is what forces genuine diversity."},
        {"q": "Can raising n_estimators cause overfitting?",
         "options": ["Yes, past a few hundred",
                     "No - more trees only improve the estimate of the average",
                     "Only without max_depth",
                     "Only on small datasets"],
         "answer": 1,
         "why": "It is the one complexity-shaped parameter with no trade-off. The cost is time and memory, not generalisation."},
        {"q": "Why is feature_importances_ misleading?",
         "options": ["It does not sum to 1",
                     "It is computed on training data and favours columns with many distinct values",
                     "It ignores the first feature",
                     "It only works for regression"],
         "answer": 1,
         "why": "In the editor a pure-noise column with 400 distinct values scored higher than another noise column. Permutation importance gave both exactly zero."},
        {"q": "What does a random forest predict beyond its training range?",
         "options": ["It extrapolates the trend",
                     "A flat value - every tree is flat there, so the average is too",
                     "The overall mean",
                     "It raises an error"],
         "answer": 1,
         "why": "It predicted 55.3 for both x=25 and x=40 on a perfect straight line. Averaging does not fix what every member shares."},
    ],
)


# ---------------------------------------------------------------------------
# 19. Hyperparameter search
# ---------------------------------------------------------------------------
topic(
    "hyperparameter_search",
    "Hyperparameter Search",
    "Honest Numbers",
    "Letting cross-validation choose the settings - and understanding why the "
    "number it reports for the winner is too high.",
    _svg(_grid(34, 22, 4, 4, 14, S) +
         _box(62, 50, 14, 14, S, A, 2, 0) +
         _txt(80, 84, "every combination, cross-validated", M, 7)),
    [
        ("The search, and what it leaves you with",
         "Four settings, five folds, twenty fits - and a model already refitted "
         "on everything.",
         '''from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)
pipe = Pipeline([("scale", StandardScaler()),
                 ("clf", LogisticRegression(max_iter=2000))])

search = GridSearchCV(pipe, {"clf__C": [0.01, 0.1, 1, 10]}, cv=5).fit(X, y)

print("best parameters:", search.best_params_)
print("best cv score  :", round(search.best_score_, 4))
print("fits performed :", 4 * 5, "(4 settings x 5 folds)")
print()
print("best_estimator_ has already been refitted on all the data:")
print(" ", type(search.best_estimator_).__name__,
      "->", search.best_estimator_.predict(X[:5]))
'''),

        ("Read the whole table, not just the winner",
         "The top two differ in the fourth decimal, and the standard deviation "
         "is two hundred times that.",
         '''from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)
pipe = Pipeline([("scale", StandardScaler()),
                 ("clf", LogisticRegression(max_iter=2000))])
search = GridSearchCV(pipe, {"clf__C": [0.01, 0.1, 1, 10]}, cv=5).fit(X, y)

r = search.cv_results_
print("%10s %10s %8s %6s" % ("C", "mean", "std", "rank"))
for c, m, s, k in zip(r["param_clf__C"], r["mean_test_score"],
                      r["std_test_score"], r["rank_test_score"]):
    print("%10s %10.4f %8.4f %6d" % (c, m, s, k))
print()
print("the top two are within one standard deviation of each other,")
print("which means the ranking between them is not evidence.")
'''),

        ("Random search finds nearly the same thing, faster",
         "Six samples against sixteen combinations.",
         '''from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from scipy.stats import randint
import time

X, y = make_classification(n_samples=300, n_features=10, n_informative=4,
                           random_state=0)
rf = RandomForestClassifier(n_estimators=20, random_state=0)

grid = {"max_depth": [2, 4, 6, 8], "min_samples_leaf": [1, 3, 5, 7]}
t = time.time()
g = GridSearchCV(rf, grid, cv=3).fit(X, y)
grid_time = time.time() - t

dist = {"max_depth": randint(2, 9), "min_samples_leaf": randint(1, 8)}
t = time.time()
r = RandomizedSearchCV(rf, dist, n_iter=6, cv=3, random_state=0).fit(X, y)
rand_time = time.time() - t

print("grid       : %2d combinations, %.2fs, best %.4f"
      % (16, grid_time, g.best_score_))
print("randomized :  6 samples,      %.2fs, best %.4f"
      % (rand_time, r.best_score_))
'''),

        ("Tuning the preprocessing too",
         "Including whether a step happens at all.",
         '''from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_wine

X, y = load_wine(return_X_y=True)

pipe = Pipeline([("scale", StandardScaler()),
                 ("pca", PCA()),
                 ("clf", LogisticRegression(max_iter=2000))])

# The preprocessing is tuned alongside the model - including whether
# the PCA step happens at all.
grid = {"pca": ["passthrough", PCA(n_components=4), PCA(n_components=8)],
        "clf__C": [0.1, 1.0]}

search = GridSearchCV(pipe, grid, cv=5).fit(X, y)
print("best:", {k: str(v) for k, v in search.best_params_.items()})
print("score:", round(search.best_score_, 4))
'''),

        ("best_score_ is optimistic",
         "Random labels, so the truth is 0.5. The search reports considerably "
         "more than that.",
         '''from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Random labels: the honest score is 0.5, whatever the search reports.
rng = np.random.RandomState(0)
X = rng.normal(size=(120, 20))
y = rng.randint(0, 2, size=120)

grid = {"max_depth": [1, 2, 3, 5, 8]}
search = GridSearchCV(RandomForestClassifier(n_estimators=20, random_state=0),
                      grid, cv=5)

inner = search.fit(X, y).best_score_
outer = cross_val_score(search, X, y, cv=5).mean()

print("best_score_ from the search      :", round(inner, 3))
print("nested cross-validation          :", round(outer, 3))
print("the truth (the labels are random):  0.5")
print()
print("best_score_ is the best of five tries on the same folds,")
print("so it is optimistic by construction.")
'''),

        ("The metric decides the winner",
         "One grid, three metrics, and they do not all choose the same setting.",
         '''from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=800, n_features=10, weights=[0.93],
                           random_state=0)

grid = {"class_weight": [None, "balanced"]}
for metric in ("accuracy", "f1", "balanced_accuracy"):
    s = GridSearchCV(LogisticRegression(max_iter=2000), grid, cv=5,
                     scoring=metric).fit(X, y)
    print("%-19s picks class_weight=%-9s (%.4f)"
          % (metric, str(s.best_params_["class_weight"]), s.best_score_))
print()
print("two of the three keep the default and the third does not.")
print("scoring= is a decision about the problem, not a formality.")
'''),
    ],
    [
        "<code class='mono-font'>GridSearchCV</code> tries every combination; "
        "the number of fits is the product of the grid times the folds.",
        "<code class='mono-font'>RandomizedSearchCV</code> samples "
        "<code class='mono-font'>n_iter</code> combinations, which scales to "
        "large spaces and usually finds nearly as good a setting.",
        "The search refits the winner on all the data - "
        "<code class='mono-font'>best_estimator_</code> is ready to use.",
        "<code class='mono-font'>best_score_</code> is the best of many tries "
        "on the same folds, so it is <strong>optimistic</strong>; a held-out "
        "test set or nested CV gives the honest number.",
        "Read <code class='mono-font'>cv_results_</code>, not just the winner - "
        "settings within one standard deviation of each other are tied.",
        "<code class='mono-font'>scoring=</code> defaults to accuracy, and "
        "changing it can change which setting wins.",
    ],
    """title: Hyperparameter Search: A Practical Guide
intro: Settings have to be chosen by reading rather than by taste. The tools that do it are simple. The number they report is the part that needs care.

## What is being searched

Every estimator has parameters that you set before calling `fit`. These are hyperparameters. The number of neighbours in KNN, the regularisation strength in logistic regression, the maximum depth of a tree. The model does not learn them from the data. You choose them.

Choosing well matters. The right hyperparameters can double a model's score. The wrong ones can make a good algorithm look useless. Manual tuning works for one or two parameters, but it is slow, hard to reproduce, and easy to fool yourself with.

scikit-learn provides two search tools: `GridSearchCV` and `RandomizedSearchCV`. Both try a set of hyperparameter values, evaluate each combination with cross-validation, and keep the best. The difference is how they choose the combinations. Grid search tries every combination on a predefined list. Random search samples from distributions.

Grid search is thorough but expensive. The number of fits is the product of all the list lengths times the number of folds. Three parameters with five values each and five folds means 375 fits. Random search is cheaper and often finds a good setting faster, because it does not waste fits on parameters that turn out not to matter.

Both search objects follow the estimator interface. They have `fit`, `predict` and `score`. You can drop them into a pipeline or use them inside nested cross-validation.

Settings are the settings you pass to the constructor: `C`, `max_depth`, `n_neighbors`, `alpha`. They aren't learned from the data during `fit`. A thing outside the fit has to choose them.

Choosing by hand means changing one, re-running. Keeping what scored better. Which is a search, done slowly and without a record. The search tools do the same thing systematically, with cross-validation at each setting so the check isn't decided by one lucky split.

`GridSearchCV` takes a dict of params to lists of values and tries each combination. The number of fits is the product of the list lengths times the number of folds. It grows alarmingly. Three params with five values each and five folds is 375 fits.

Both search objects are themselves estimators. They've `fit`, `predict` and `score`. A search can go inside a pipeline, inside `cross_val_score`, or anywhere else an estimator goes. Which is what makes nested cross-validation a one-liner.

## Grid or random

`RandomizedSearchCV` samples `n_iter` combinations rather than trying all of them, drawing from lists or from spreads such as `scipy.stats.randint` and `loguniform`.

It's often the better choice, for a reason that isn't obvious. In a common search most params barely matter and one or two dominate. A grid spends its budget evenly. With two params and sixteen combinations it tries only four distinct values of the one that matters. Random search with sixteen samples tries sixteen distinct values of it. Each sample varies all.

The editor above shows six random samples getting within 0.003 of a sixteen-combination grid in 40% of the time. This Is the usual shape of the result.

Grid search remains right when the space is truly small and you want each combination on record. Two or three params with a handful of sensible values each.

`HalvingGridSearchCV` and `HalvingRandomSearchCV` are the middle path: they test many picks on a small subset of the data, discard the worst. Give the survivors more resources. On a large dataset the saving is substantial.

## The number it reports is too high

This is the part that matters most. It's easy to miss because all about the method looks careful.

`best_score_` is the cross-validated score of the winning setting. It's the **max** of many cross-validated scores found on the same folds. Taking a max over noisy guesses selects for luck and quality. The winner is partly the setting that happened to suit those given folds.

The fifth editor makes the size of the effect visible. The labels are random. The honest fit is 0.5. The search reports **0.642**, having picked the best of five depths on the same five folds. Nested cross-validation. Where the whole search is repeated inside each outer fold. Reports 0.575. Even that isn't quite 0.5 with only 120 rows.

So `best_score_` is a pick artefact. The more settings you try the worse it gets. The remedies are a test set held out before the search and touched once afterwards, or nested cross-validation when you need the guess itself to be trustworthy. Reporting `best_score_` as the model's speed is one of the most common ways published numbers turn out to be optimistic.

## Read the table

`cv_results_` holds each setting with its mean score, standard deviation and rank. Reading it rather than only `best_params_` changes what you conclude oddly often.

The second editor is a clean example: `C=0.1` scores 0.9833 and `C=1` scores 0.9832, with standard deviations around 0.02. The winner beat the runner-up by one ten-thousandth, against noise two hundred times larger. Declaring `C=0.1` the best value is reading a coin flip.

Two habits follow. **Compare the gap against the standard deviation**. Any of it inside one is a tie. And **prefer the simpler setting among ties**. More smoothing, shallower trees, fewer components. When two settings are the same on the evidence, the one less likely to have fitted noise is the better bet.

`std_test_score` also flags an unreliable search: large standard deviations mean the folds disagree. No ranking found from them deserves trust.

## Searching the whole pipeline

Because a pipeline is an estimator, a search can tune any of it inside it using the double-underscore path &mdash; `clf__C`, `pre__num__imputer__strategy`.

That makes prep choices measurable rather than assumed. Mean or median imputation, scaled or not, how many PCA components, whether to drop the first one-hot column. All of them can go in the grid. The cross-validation that tests them is the same honest one that tests the model.

A step can be tuned in or out fully by including `"passthrough"` among its values. This The fourth editor uses to discover that PCA doesn't help on that data. The same trick swaps whole models: `{"clf": [LogisticRegression(), RandomForestClassifier()]}` puts the model choice itself in the grid.

The key property is that all of this happens **inside** the folds. A search over prep done by hand, outside cross-validation, is the leak the earlier modules measured.

## The metric decides the answer

`scoring` defaults to fit for classifiers and R&sup2; for regressors. Leaving it there means optimising fit whether or not fit is what you care about.

The last editor searches `class_weight` on imbalanced data under three metrics. Fit and F1 keep the default. Weighed fit chooses `"weighed"`. Same data, same grid, different winner. Because the metrics disagree about what a good model is. This Is just what the metrics modules said they would do.

So `scoring=` is where the choice about which mistakes matter enters the tuning process. Choosing it on purpose isn't optional if the classes are imbalanced or the costs are skewed.

`refit` can name one metric to refit on when a few are being found. This Is how you report a panel of metrics while selecting on one.

## Keeping it affordable

`n_jobs=-1` parallelises across cores, and search is close to just right parallel.

Search coarsely first &mdash; powers of ten &mdash; then refine around what region wins. A logarithmic grid over `C` from 0.001 to 1000 in one pass tells you more than a fine linear grid in the wrong place.

Reduce the folds to 3 while exploring and raise them for the final check. And note that the params worth searching are few: `C` or `alpha` for linear models, `max_depth` and `min_samples_leaf` for trees, `learning_rate` and `n_estimators` for boosting. Searching all a model exposes wastes budget on params that don't move the score.

## Which parameters are worth the budget

Searching all an estimator exposes wastes most of the fits on settings that don't move the score. A short list of what really matters, per model family.

**Linear models.** `C` or `alpha`, over a logarithmic range. That is very nearly all. The fine type (`l1` against `l2`) is worth one check when feature pick is wanted.

**Trees.** `max_depth` and `min_samples_leaf`, or `ccp_alpha` instead of both. The criterion isn't worth searching. The choice-trees module measured the three within half a point of each other.

**Random forests.** `max_features` first, then `min_samples_leaf` on noisy data. `n_estimators` isn't a search param. Set it as high as you can afford, since it can't overfit.

**Grad boosting.** `learning_rate` and `n_estimators` together. They trade against each other, plus `max_depth` in a narrow range of about 3 to 8. This family repays tuning more than any other on this list. Is the reason to keep budget in reserve.

**k-NN.** `n_neighbors`, and `weights` as a two-value check.

**SVM.** `C` and `gamma`, both logarithmic. This pair truly needs a two-dimensional search because they interact strongly.

The general shape: one or two params carry nearly all the improvement. They're often the ones controlling smoothing. Finding them for a new estimator is a matter of reading which param the docs discusses at length.

## What a search cannot fix

Worth stating, because tuning is where effort goes when a model disappoints. It's often the wrong place to spend it.

A search moves a model within its family. It can't make a linear model represent a curve, can't make a tree extrapolate. Can't make up for for features that don't carry the signal. If the learning curve has settled and the model is underfitting, no combination of settings closes the gap. The answer is different features or a different family.

Nor can it fix a metric that measures the wrong thing, a split that leaks, or labels that are wrong. A search will optimise what it's pointed at, including a leak. Report a confident number for it.

The order that wastes least effort: get the split and the metric right, get the features right, pick a model family that can represent the structure. Tune last. Tuning first is the most common way to spend a week moving a score by half a point.

<strong>How many combinations is reasonable?</strong> What finishes in the time you've. Twenty random samples over a sensible range beats an exhaustive grid over the wrong one.

<strong>Can I search two models at once?</strong> Yes - put the estimator itself in the grid: `{"clf": [LogisticRegression(), RandomForestClassifier()]}`, with each model's own params guarded by the step name.

<strong>Does refit cost much?</strong> One extra fit on the full data. This Is negligible next to the search itself. `refit=False` skips it if you only want the table.

<strong>What is `error_score` for?</strong> Some combinations are invalid and raise. The default passes the error. `error_score=np.nan` records the failure and lets the search continue.

## Ranges that are worth searching over

Choosing the values is most of the skill, and two habits cover it.

**Search logarithmically for any of it that scales multiplicatively.** Smoothing strengths, learning rates, gamma. The notable range for `C` spans six orders of magnitude. A linear grid from 1 to 10 explores almost none of it. `np.logspace(-3, 3, 7)` gives 0.001 to 1000 in seven values. `scipy.stats.loguniform(1e-3, 1e3)` is the equal for random search.

**Search linearly for any of it that counts things.** Tree depth, number of neighbours, min samples in a leaf. These are small ints and a linear range over a plausible span is right.

Then check whether the winner sits at the edge of the range. If the best `C` is the largest value tried, the range was too narrow and the search hasn't found the optimum. It has found the boundary. Extending and re-running is a one-line change and is the difference between a tuned model and one that stopped where you happened to stop looking.

The corollary is that a first pass should be on purpose wide and coarse. Powers of ten across the whole plausible range, three folds, few picks. That locates the region in a few seconds. The refined search can then spend its budget a place worth spending it.

## Things to try

1. <strong>Read the table.</strong> The second editor's top two settings are separated by 0.0001. Decide for yourself whether that is a result.
2. <strong>Watch the optimism.</strong> The fifth editor searches random labels and reports 0.642 for a thing whose truth is 0.5.
3. <strong>Tune a step away.</strong> In the fourth editor, note that `passthrough` won. The PCA step wasn't helping.
4. <strong>Change the metric.</strong> In the last editor, add `"recall"` and see which setting it prefers.

## Where this leaves you

Random search over a sensible range, with a pipeline so the prep is tuned honestly, a `scoring` chosen for the problem, `cv_results_` read rather than skimmed. The winner's score treated as optimistic until a held-out set says or else.
""",
    [
        {"q": "Why is best_score_ optimistic?",
         "options": ["It is computed on the training data",
                     "It is the maximum of many noisy estimates on the same folds",
                     "It ignores the standard deviation",
                     "It refits on all the data first"],
         "answer": 1,
         "why": "Taking a maximum selects for luck as well as quality. On random labels a search reported 0.642 where the truth was 0.5."},
        {"q": "When is RandomizedSearchCV usually better than GridSearchCV?",
         "options": ["Never - grid is exhaustive",
                     "When the space is large, since it tries more distinct values of the parameters that matter",
                     "Only for trees",
                     "When there is one parameter"],
         "answer": 1,
         "why": "A grid spends its budget evenly across parameters that mostly do not matter. Random sampling varies everything at once."},
        {"q": "Two settings differ by 0.0001 with a standard deviation of 0.02. What should you conclude?",
         "options": ["The higher one is better",
                     "They are tied - prefer the simpler setting",
                     "The search failed",
                     "Increase the folds until one wins"],
         "answer": 1,
         "why": "A gap far inside one standard deviation is noise. Among ties, the more regularised or simpler setting is the safer bet."},
        {"q": "What does scoring= default to for a classifier?",
         "options": ["f1", "roc_auc", "accuracy", "balanced_accuracy"],
         "answer": 2,
         "why": "Which means an unset scoring silently optimises accuracy - and on imbalanced data that can pick a different winner than the metric you care about."},
    ],
)


# ---------------------------------------------------------------------------
# 20. Probabilities and thresholds
# ---------------------------------------------------------------------------
topic(
    "probabilities_and_thresholds",
    "Probabilities and Thresholds",
    "Classification",
    "predict() makes a decision you did not authorise. Taking it back is the "
    "cheapest improvement available, and it needs no refitting.",
    _svg(_box(14, 30, 132, 22, S, B) +
         '<rect x="14" y="30" width="52" height="22" fill="var(--bg-surface)" '
         'stroke="var(--text-muted)" stroke-width="2"/>' +
         '<path d="M66 24 L66 58" stroke="var(--accent-primary)" '
         'stroke-width="3"/>' + _txt(66, 18, "threshold", A, 7) +
         _txt(38, 45, "no", M, 8) + _txt(106, 45, "yes", M, 8) +
         _txt(80, 76, "0.0                          1.0", M, 7)),
    [
        ("predict is proba plus a hidden decision",
         "The two agree exactly, because one is defined as the other.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=400, n_features=6, random_state=0)
model = LogisticRegression().fit(X, y)

proba = model.predict_proba(X)[:, 1]
manual = (proba >= 0.5).astype(int)

print("predict() equals proba >= 0.5 :", (manual == model.predict(X)).all())
print()
print("the 0.5 is a default, not a law - nothing about the problem")
print("said the boundary belonged there.")
'''),

        ("One model, five classifiers",
         "Look at what the default threshold does to recall on this data.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score, recall_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# A harder problem, so both numbers actually move.
X, y = make_classification(n_samples=3000, n_features=10, n_informative=3,
                           weights=[0.85], flip_y=0.15, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)
model = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
proba = model.predict_proba(X_te)[:, 1]

print("threshold  precision  recall  flagged")
for t in (0.1, 0.2, 0.3, 0.5, 0.7):
    pred = (proba >= t).astype(int)
    print("%9.1f %10.3f %7.3f %8d"
          % (t, precision_score(y_te, pred, zero_division=0),
             recall_score(y_te, pred), int(pred.sum())))
print()
print("one fitted model, five different classifiers - and predict()")
print("silently chose the middle row for you.")
'''),

        ("The curve is every threshold at once",
         "Which is how you pick one to hit a requirement rather than by trying "
         "numbers.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy as np

X, y = make_classification(n_samples=3000, n_features=10, n_informative=3,
                           weights=[0.85], flip_y=0.15, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)
proba = LogisticRegression(max_iter=1000).fit(X_tr, y_tr).predict_proba(X_te)[:, 1]

precision, recall, thresholds = precision_recall_curve(y_te, proba)

for target in (0.70, 0.90):
    ok = np.flatnonzero(recall[:-1] >= target)
    i = ok[-1]
    print("for %d%% recall: threshold <= %.3f, precision %.3f"
          % (target * 100, thresholds[i], precision[i]))
print()
print("the curve is every threshold at once, which is what you read")
print("to pick one deliberately.")
'''),

        ("ROC AUC flatters an imbalanced problem",
         "The same model quality, two class balances, and only one of the two "
         "metrics notices.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

for weight in (0.5, 0.99):
    X, y = make_classification(n_samples=4000, n_features=10,
                               weights=[weight], random_state=0)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                              random_state=0, stratify=y)
    m = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
    p = m.predict_proba(X_te)[:, 1]
    print("positives %5.1f%%   ROC AUC %.3f   average precision %.3f"
          % (100 * (1 - weight), roc_auc_score(y_te, p),
             average_precision_score(y_te, p)))
print()
print("ROC AUC stays high when positives are rare, because the huge")
print("number of true negatives keeps the false positive rate low.")
'''),

        ("Are the probabilities honest?",
         "A calibrated model's 0.7 means seventy per cent of those cases turn "
         "out positive.",
         '''from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import calibration_curve
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy as np

X, y = make_classification(n_samples=3000, n_features=10, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)

for name, m in [("LogisticRegression", LogisticRegression(max_iter=1000)),
                ("RandomForest", RandomForestClassifier(n_estimators=50,
                                                        random_state=0))]:
    p = m.fit(X_tr, y_tr).predict_proba(X_te)[:, 1]
    true, pred = calibration_curve(y_te, p, n_bins=5)
    gap = np.abs(true - pred).mean()
    print("%-20s mean |predicted - observed| = %.4f" % (name, gap))
print()
print("a calibrated model's predicted 0.7 means 70% of those cases")
print("are positive. one of these two is closer to that than the other.")
'''),

        ("Choosing the threshold by cost",
         "When a miss costs ten times a false alarm, the default is not close "
         "to optimal.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy as np

X, y = make_classification(n_samples=2000, n_features=10, weights=[0.9],
                           random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)
proba = LogisticRegression(max_iter=1000).fit(X_tr, y_tr).predict_proba(X_te)[:, 1]

# A miss costs 10, a false alarm costs 1.
best = None
for t in np.arange(0.05, 0.96, 0.05):
    tn, fp, fn, tp = confusion_matrix(y_te, (proba >= t).astype(int)).ravel()
    cost = 10 * fn + 1 * fp
    if best is None or cost < best[1]:
        best = (t, cost, fn, fp)
print("cheapest threshold: %.2f  (cost %d = %d misses x10 + %d false alarms)"
      % best)
tn, fp, fn, tp = confusion_matrix(y_te, (proba >= 0.5).astype(int)).ravel()
print("the default 0.5 would cost:", 10 * fn + fp)
'''),
    ],
    [
        "<code class='mono-font'>predict()</code> is "
        "<code class='mono-font'>predict_proba() >= 0.5</code> - a decision the "
        "library made, not one the problem did.",
        "Moving the threshold trades precision against recall <strong>without "
        "refitting</strong>, which makes it the cheapest adjustment available.",
        "<code class='mono-font'>precision_recall_curve</code> gives every "
        "threshold at once, so you can choose one to meet a requirement.",
        "Choose the threshold on a <strong>validation</strong> set, not on the "
        "test set - it is a parameter like any other.",
        "<strong>ROC AUC</strong> stays high on imbalanced data; "
        "<strong>average precision</strong> is the honest summary when "
        "positives are rare.",
        "Probabilities are only meaningful if the model is "
        "<strong>calibrated</strong>; "
        "<code class='mono-font'>CalibratedClassifierCV</code> fixes one that "
        "is not.",
    ],
    """title: Probabilities and Thresholds: A Practical Guide
intro: each classifier in this track has been making a choice on your behalf at 0.5. Taking that choice back costs nothing and often raises the model more than tuning does.

## The hidden default

Most classifiers in scikit-learn can output probabilities, not just class labels. `predict_proba` returns the estimated chance of each class for every row. `predict` takes those probabilities and applies a threshold to turn them into labels.

The default threshold is 0.5. If the predicted probability of the positive class is above 0.5, the model says positive. Otherwise it says negative. That threshold is baked into `predict` and there is no parameter to change it.

On balanced data with equal misclassification costs, 0.5 is reasonable. On imbalanced data, or when one kind of mistake is more expensive than the other, 0.5 is almost never the right choice. A fraud-detection model at 0.5 will miss most fraud. A medical-screening model at 0.5 will miss most disease. Lowering the threshold catches more positives at the cost of more false alarms.

Moving the threshold does not retrain the model. The fitted probabilities stay the same. You are just changing where the line is drawn between "flag" and "skip". The editors on this page show how the same model produces very different confusion matrices at different thresholds.

`predict()` calls `predict_proba()` and applies a threshold of 0.5. That is the whole of it. The first editor confirms the two are the same.

There's nothing principled about 0.5. It's the point where the two classes are equally likely. This Would be the right cut only if the classes were equally frequent *and* the two kinds of mistake cost the same. Neither is often true.

The consequence on imbalanced data can be severe. The second editor fits a model on data with 15% positives and reports what happens at each threshold. At 0.5 the model flags 5 cases out of 900 and catches **2.2%** of the positives. It isn't a broken model. At a threshold of 0.1 the same fitted model catches 91.6%. It's a model being asked the wrong question.

## Moving it costs nothing

The threshold is applied *after* fitting. Changing it needs no refitting, no search. No extra data. Get the chances once and each operating point is available.

That makes it the cheapest lever in the whole workflow. It's routinely left untouched while big effort goes into tuning settings that move the score far less.

The mechanics are one line: `(proba >= t).astype(int)` instead of `predict(X)`, having taken `proba = model.predict_proba(X)[:, 1]`. Column 1 is the positive class. The columns follow `classes_`. With labels `[0, 1]` the second column is the chance of 1.

## Choosing one deliberately

Three ways, in growing order of rigour.

**To meet a need.** "We must catch 90% of cases" is a recall target. `precision_recall_curve` says what threshold reaches it and what precision you pay. The third editor answers it right: 90% recall needs a threshold of 0.105 and gives precision 0.207. Roughly five false alarms per real case. This The business either accepts or doesn't.

**To balance the metric you chose.** Sweep the threshold, find F1 or weighed fit at each, take the best. Simple. It optimises a proxy rather than the thing you care about.

**To cut cost.** The honest version. Attach a price to a false minus and a false plus, find the total at each threshold, take the min. The last editor does just this with a miss costing ten times a false alarm. The cheapest threshold is 0.15 with a cost of 50, against 90 at the default. Nearly half the cost, from changing one number.

Whichever you use, choose it on a **validation** set. The threshold is a param fitted to data. Choosing it on the test set is the same mistake as tuning on the test set. The resulting precision and recall are optimistic.

## The curve, and its summary

`precision_recall_curve` returns arrays of precision, recall and the thresholds that give them. The trailing element of precision and recall has no matching threshold. This Is why indexing them together needs the `[:-1]` the editor uses.

`average_precision_score` summarises the whole curve as one number. `roc_curve` and `roc_auc_score` are the option pair, plotting the true positive rate against the false positive rate.

The choice between them matters on imbalanced data. The fourth editor shows why. The same kind of model on data with 50% positives scores ROC AUC 0.935 and mean precision 0.919. Close together. At 1% positives it scores ROC AUC 0.825 and mean precision **0.134**.

ROC AUC barely moved because its false-positive rate cuts by the number of true negatives. With 99% negatives that denominator is huge. Even many false alarms barely register. Mean precision skips true negatives fully and reports what really happens to the rare class.

The rule: ROC AUC for roughly weighed problems, mean precision when positives are rare. A high ROC AUC on a 1% problem is close to meaningless.

## Whether the probabilities mean anything

A model outputting 0.7 is making a claim. Among cases it scores 0.7, about 70% should be plus. A model whose output meets that is **calibrated**.

Logistic regression is often well calibrated. Raising the likelihood of the seen labels is close to what calibration asks for. Tree ensembles often aren't. A random forest's output is the proportion of trees voting plus. This Ranks right and is pushed towards the middle. It rarely says 0.01 or 0.99 because rarely do all the trees agree. The fifth editor measures the gap and finds the forest roughly twice as far off as the linear model.

This matters when the chance is used as a number rather than as a ranking. Expected-value maths, risk scores shown to people, thresholds chosen by cost. It doesn't matter if you only ever rank and cut.

`calibration_curve` measures it by bucketing guesses and checking the mean predicted chance against the seen rate in each bucket. `CalibratedClassifierCV` fixes it by fitting a correction on held-out data, using either a sigmoid or an isotonic fit.

## The threshold is part of the model

A subtle point that causes real problems in deployment. Once you choose a threshold, it belongs to the model and has to travel with it.

A pipeline pickled without its threshold will be loaded a place else and used through `predict()`. This Silently reverts to 0.5. And on the imbalanced problem above that is the difference between catching 91% of cases and catching 2%. Nothing raises. The service simply flags almost nothing and everyone assumes the model is weak.

Three ways to keep them together. Record the threshold alongside the model file and apply it by name in the serving code. This Is the most common and leans on discipline. Wrap the model in a small class whose `predict` applies your threshold. The object carries it. Or, from recent scikit-learn versions, use `FixedThresholdClassifier` and `TunedThresholdClassifierCV`. This Are estimators that hold a threshold and expose the plain interface. The second finds it by cross-validation against a metric or a cost function you supply.

The last of those is the tidiest answer. The threshold is then chosen inside the folds like any other param and stored on the fitted object like any other learned value.

## Multi-class is a different question

All on this page assumes two classes. With more, `predict()` takes the highest chance rather than checking against a threshold. There's no single number to move.

The equal adjustments are different. `class_weight` shifts the model's own preferences during fitting. Post-processing the chance mat. Timesing each column by a factor and taking the argmax. Is the closest analogue and has to be tuned per class. And a truly cost-sensitive multi-class choice means writing the expected cost of each guess by name and choosing the min. This Is a few lines and rarely done.

Where a binary threshold *does* reappear is one-versus-rest setups. Here Each class has its own binary choice and each can carry its own threshold. Which is how multi-label problems are often handled.

<strong>Which column of predict_proba is the positive class?</strong> The one matching `classes_`. With labels 0 and 1 that is column 1. With string labels it's whichever sorts second - read `classes_` rather than given.

<strong>What if my model has no predict_proba?</strong> Many have `decision_function` instead. This Returns an unbounded score rather than a chance. Thresholding it works the same way. The numbers are just not chances.

<strong>Should I tune the threshold or use class_weight?</strong> Both. They do different things. `class_weight` changes what the model optimises while fitting. The threshold changes the choice afterwards. Tuning the threshold is cheaper and reversible.

<strong>Does a better threshold improve AUC?</strong> No. AUC summarises each threshold. It's unchanged by picking one. That is just why it can't tell you which to pick.

## Why the default is 0.5 at all

It's worth understanding rather than resenting. The thinking tells you just when it's right.

Under two assumptions, 0.5 is best. The first is that the two classes are equally frequent. A chance above a half truly means "more likely than not". The second is that a false plus and a false minus cost the same. So The choice should go to whichever is more probable.

Both assumptions are defaults in the same sense the threshold is. They're what you get when no one has said or else. And both are wrong on most real problems. Fraud, disease, churn, defects and failures are all rare. In each one of them a miss and a false alarm have quite different prices.

So the library's choice isn't a mistake. It's the only neutral answer available to a thing that knows nothing about your problem. What it can't do is warn you. From inside the estimator there's no way to tell a weighed problem from an imbalanced one that you happen to care about differently.

The hands-on version: on any problem where the classes are uneven or the mistakes cost differently, treat the threshold as unset rather than as set to 0.5. It's a param with a default. The default was chosen in the lack of the info only you've.

## A short procedure

Five steps that turn all of this into a thing routine.

Split off a validation set, or use cross-validation, keeping the test set untouched. Fit the model and take `predict_proba` on the validation part. Sweep thresholds from 0.01 to 0.99 and find, at each, the quantity you really care about. A cost, a metric, or the precision at a needed recall. Choose the threshold that optimises it. Record it with the model. Then measure once on the test set, using that fixed threshold, and report those numbers.

The whole thing is about fifteen lines and it's the difference between a model whose reported speed is achievable and one whose numbers came from a choice no one made.

<strong>Can the threshold be above 0.5?</strong> Yes. It should be when false alarms are the costly mistake - a spam filter that deletes mail, say. Nothing restricts it to the lower half.

<strong>Why does my precision-recall curve have one more point than thresholds?</strong> The curve includes the endpoint where all is predicted minus. This Has no threshold. Index with `[:-1]` when pairing them.

## Things to try

1. <strong>Read the second editor properly.</strong> At the default threshold the model catches 2.2% of positives. It's a good model being asked a bad question.
2. <strong>Set a target.</strong> In the third editor, change the targets to 0.95 and 0.99 and watch the precision collapse.
3. <strong>Change the cost ratio.</strong> In the last editor, make a miss cost 100 and see where the threshold moves.
4. <strong>Calibrate the forest.</strong> Wrap it in `CalibratedClassifierCV` and re-measure the gap.

## Where this leaves you

`predict()` hides a choice. `predict_proba()` gives it back. Choose the threshold from the cost of each mistake, on a validation set, using the precision-recall curve to see the options. And check that the chances are calibrated before treating any of them as a number.
""",
    [
        {"q": "What does predict() do that predict_proba() does not?",
         "options": ["Refit the model",
                     "Apply a 0.5 threshold, discarding the confidence",
                     "Scale the output",
                     "Average across classes"],
         "answer": 1,
         "why": "The two are identical by definition: predict is proba >= 0.5. The 0.5 is a library default, not a property of your problem."},
        {"q": "Does changing the threshold require refitting?",
         "options": ["Yes, the model must be retrained",
                     "No - it is applied after fitting, so every operating point is already available",
                     "Only for tree models",
                     "Only if the classes are imbalanced"],
         "answer": 1,
         "why": "That is what makes it the cheapest adjustment available, and why it is worth doing before tuning hyperparameters."},
        {"q": "Positives are 1% of the data. Which summary should you trust?",
         "options": ["ROC AUC", "Average precision", "Accuracy", "Either equally"],
         "answer": 1,
         "why": "ROC AUC read 0.825 where average precision read 0.134 on the same predictions. The false positive rate divides by an enormous number of true negatives."},
        {"q": "What does it mean for a model to be calibrated?",
         "options": ["Its accuracy is high",
                     "Among cases it scores 0.7, about 70% are actually positive",
                     "Its threshold is 0.5",
                     "Its features are scaled"],
         "answer": 1,
         "why": "It matters whenever the probability is used as a number. Tree ensembles rank well and are usually poorly calibrated; logistic regression usually is not."},
    ],
)


# ---------------------------------------------------------------------------
# 21. Class imbalance
# ---------------------------------------------------------------------------
topic(
    "class_imbalance",
    "Class Imbalance",
    "Classification",
    "When the interesting class is 2% of the data, the default model ignores "
    "it and reports 96% accuracy. Four remedies, and the cheapest is usually "
    "the best.",
    _svg("".join('<rect x="%d" y="46" width="8" height="24" fill="var(--bg-surface)" '
                 'stroke="var(--text-muted)" stroke-width="1"/>' % (16 + i * 11)
                 for i in range(11)) +
         '<rect x="138" y="46" width="8" height="24" fill="var(--accent-primary)"/>' +
         _txt(80, 34, "one of these is the one you care about", M, 7)),
    [
        ("What the default model does",
         "It finds three of the forty-nine positives, and reports 96% accuracy "
         "for it.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, recall_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=4000, n_features=10, n_informative=4,
                           weights=[0.98], flip_y=0.05, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)

m = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
print("positives in the test set:", int(y_te.sum()), "of", len(y_te))
print("accuracy:", round(m.score(X_te, y_te), 4))
print("recall  :", round(recall_score(y_te, m.predict(X_te)), 4))
print()
print("confusion matrix (rows = actual):")
print(confusion_matrix(y_te, m.predict(X_te)))
'''),

        ("class_weight, and what it costs",
         "Recall goes up nine-fold. Precision collapses, and accuracy with it.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, precision_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=4000, n_features=10, n_informative=4,
                           weights=[0.98], flip_y=0.05, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)

print("%-22s %9s %9s %9s" % ("", "accuracy", "precision", "recall"))
for label, cw in [("default", None), ("class_weight=balanced", "balanced")]:
    m = LogisticRegression(max_iter=1000, class_weight=cw).fit(X_tr, y_tr)
    p = m.predict(X_te)
    print("%-22s %9.4f %9.4f %9.4f"
          % (label, m.score(X_te, y_te),
             precision_score(y_te, p, zero_division=0), recall_score(y_te, p)))
'''),

        ("The same model, thresholded",
         "No refitting, no reweighting - the model already knew, and predict() "
         "was throwing it away.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, precision_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=4000, n_features=10, n_informative=4,
                           weights=[0.98], flip_y=0.05, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)

m = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
proba = m.predict_proba(X_te)[:, 1]

print("the same default model, thresholded differently:")
print("%10s %10s %8s" % ("threshold", "precision", "recall"))
for t in (0.5, 0.2, 0.1, 0.05):
    p = (proba >= t).astype(int)
    print("%10.2f %10.4f %8.4f"
          % (t, precision_score(y_te, p, zero_division=0), recall_score(y_te, p)))
'''),

        ("Resampling before the split is a leak",
         "Random labels, so nothing is learnable. One of these two numbers "
         "says otherwise.",
         '''import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import recall_score

rng = np.random.RandomState(0)
X = rng.normal(size=(600, 8))
y = (rng.rand(600) < 0.08).astype(int)      # rare, and unrelated to X

def oversample(Xa, ya, seed):
    r = np.random.RandomState(seed)
    minority = np.flatnonzero(ya == 1)
    extra = r.choice(minority, (ya == 0).sum() - len(minority), replace=True)
    idx = np.concatenate([np.arange(len(ya)), extra])
    return Xa[idx], ya[idx]

# WRONG: duplicate first, then split - copies land on both sides.
Xo, yo = oversample(X, y, 0)
wrong = []
for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(Xo, yo):
    m = LogisticRegression(max_iter=1000).fit(Xo[tr], yo[tr])
    wrong.append(recall_score(yo[te], m.predict(Xo[te])))

# RIGHT: split first, oversample only the training part.
right = []
for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(X, y):
    Xr, yr = oversample(X[tr], y[tr], 0)
    m = LogisticRegression(max_iter=1000).fit(Xr, yr)
    right.append(recall_score(y[te], m.predict(X[te])))

print("labels are random, so honest recall is about 0.5 at best")
print("oversample then split :", round(np.mean(wrong), 3))
print("split then oversample :", round(np.mean(right), 3))
'''),

        ("Three remedies, one table",
         "On F1, the cheapest of the three wins by a wide margin.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy as np

X, y = make_classification(n_samples=4000, n_features=10, n_informative=4,
                           weights=[0.98], flip_y=0.05, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)

def report(label, y_pred):
    print("%-24s %9.4f %8.4f %8.4f"
          % (label, precision_score(y_te, y_pred, zero_division=0),
             recall_score(y_te, y_pred), f1_score(y_te, y_pred, zero_division=0)))

print("%-24s %9s %8s %8s" % ("", "precision", "recall", "f1"))
base = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
report("default", base.predict(X_te))

bal = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_tr, y_tr)
report("class_weight=balanced", bal.predict(X_te))

proba = base.predict_proba(X_te)[:, 1]
best_t = max(np.arange(0.02, 0.6, 0.02),
             key=lambda t: f1_score(y_te, (proba >= t).astype(int),
                                    zero_division=0))
report("threshold %.2f" % best_t, (proba >= best_t).astype(int))
'''),

        ("Imbalance alone is not the problem",
         "The same 2% positives, but classes the features can actually "
         "separate - and no remedy needed.",
         '''from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

# Same 2% imbalance, but the classes are genuinely separable.
X, y = make_classification(n_samples=4000, n_features=10, n_informative=6,
                           weights=[0.98], flip_y=0.0, class_sep=2.0,
                           random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3,
                                          random_state=0, stratify=y)

m = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
print("positives:", int(y_te.sum()), "of", len(y_te))
print("recall with no remedy at all:", round(recall_score(y_te, m.predict(X_te)), 4))
print()
print("imbalance is not the problem by itself. the problem is imbalance")
print("plus classes the features cannot separate.")
'''),
    ],
    [
        "Accuracy is meaningless here - always <code class='mono-font'>stratify</code> "
        "the split and report per-class metrics.",
        "<code class='mono-font'>class_weight=\"balanced\"</code> reweights the "
        "loss so minority errors count more; it raises recall and costs "
        "precision.",
        "<strong>Tuning the threshold</strong> needs no refitting and often "
        "beats every other remedy - try it first.",
        "Resampling must happen <strong>inside</strong> the folds, on the "
        "training part only; doing it first puts copies on both sides.",
        "Oversampling duplicates rows and can overfit them; undersampling "
        "throws away real data. Both are blunter than reweighting.",
        "Imbalance only hurts when the classes are also hard to separate - "
        "check before reaching for a remedy.",
    ],
    """title: Class Imbalance: A Practical Guide
intro: The notable class is often the rare one. Four remedies exist, they aren't equally good. The first thing to check is whether you need one at all.

## What goes wrong

Class imbalance is present in most real classification problems. Fraud is rare. Equipment failure is rare. Disease is rare. Click-through is rare. The class you care about is almost always the minority.

A standard classifier trained on imbalanced data will mostly predict the majority class. It gets a high accuracy by ignoring the minority entirely. The accuracy number looks good, the model is useless, and nothing in the default output warns you.

The issue is not that the algorithm is broken. The algorithm is doing exactly what it was told: minimise the overall error rate. On data with 2% positives, predicting all negative gives 98% accuracy. That is the correct optimum of the wrong objective.

Fixing imbalance requires changing the objective, changing the data, or changing the threshold. scikit-learn supports all three. `class_weight="balanced"` adjusts the loss function. `RandomOverSampler` and `RandomUnderSampler` adjust the data. Moving the decision threshold adjusts the trade-off between false positives and false negatives.

This page covers the symptoms, the diagnostics and the remedies. It also covers why you should check whether imbalance is actually hurting before applying a fix.

When one class is rare, the model has almost no incentive to find it. Predicting the majority for all is right 98% of the time. The loss function. Which counts each row equally. Says that is great.

The first editor shows the result: 96% fit. 3 of 49 positives found. The confusion mat makes it concrete, with 46 misses and zero false alarms. That isn't a broken fit. It's a correct optimisation of the wrong goal.

The problems compound. Fit is uninformative, as the classification-metrics module showed. A random split can leave almost no positives in the test set. The metrics found from them are noise. And the default 0.5 threshold, chosen for weighed classes, is far from where it should be.

## Check whether you have a problem

Before reaching for a remedy, find out whether imbalance is really hurting.

The last editor keeps the same 2% positives but makes the classes truly separable. The default model. No weighting, no resampling, no threshold change. Recalls 70.8%. Nothing needed fixing.

Imbalance by itself isn't the trouble. The trouble is imbalance *plus* classes the features can't set apart. When the signal is strong, a rare class is found easily. When it's weak, the rarity means there's little evidence to learn from and the majority answer is truly hard to beat.

So the first step is a stratified split, a `classification_report`. A `DummyClassifier` for check. If recall on the minority is already acceptable, stop.

## The remedies, cheapest first

**Tune the threshold.** No refitting, no new data, no risk of overfitting duplicates. The third editor takes the *same fitted model* from 6% recall to 41% by moving one number. The fifth editor checks the remedies on F1 and the threshold wins clearly: 0.38 against 0.12 for the default and 0.11 for class weighting.

This should almost always be tried first. It often makes the others unneeded. It's also the most controllable. You pick the operating point rather than accepting what a reweighting makes.

**class_weight="weighed".** Weights each class inversely to its rate. A minority error costs more during fitting. Supported by most classifiers as a constructor arg, and it's one word.

The second editor shows what it does: recall rises from 0.06 to 0.55, precision falls from 1.00 to 0.06. Fit from 0.96 to 0.65. That is a genuine trade rather than an improvement. Whether it's worth it depends fully on the costs. Note that on F1 it didn't beat the default at all.

`class_weight` can also take a dict. This Is how you express a exact cost ratio rather than accepting the inverse-rate default.

**Resample.** Oversample the minority by duplicating rows, or undersample the majority by discarding them, until the classes are weighed.

Both are blunter than the options. Oversampling shows the model the same rows again and again. This Pushes storing them. Undersampling throws away real data. This Is wasteful when the majority isn't huge. SMOTE and its relatives, from the `imbalanced-learn` package, make synthetic minority points between existing ones instead of duplicating. Better in principle. It invents data, which on a truly rare class can invent structure that isn't there.

**Collect more of the minority.** Rarely available and by far the best when it's.

## Resampling has to be inside the folds

This is the mistake that makes the impressive result, and it's worth its own section.

Resampling before splitting means duplicated rows land on both sides. The model then sees, in training, exact copies of rows it will be tested on. The duplicate-row leak from the leakage module, added on purpose.

The fourth editor measures it on data where the labels are random and nothing is learnable. Oversampling before the split reports recall 0.632. Splitting first and oversampling only the training part reports 0.324. Neither is impressive. The first is a fabrication.

The same rule applies to cross-validation. Here The resampling must happen inside each fold. A plain `Pipeline` can't do this. Pipeline steps may not change the number of rows. Which is why `imbalanced-learn` gives its own `Pipeline` that can. That is the main hands-on reason to install it.

And what you do to the training data, **never resample the test data**. The test set must reflect the real spread, or the metrics show a world that doesn't exist.

## What to measure

Fit is out. Beyond that, the choice follows the costs, as the metrics modules argued.

**Recall** when missing a case is costly: disease, fraud, safety. **Precision** when a false alarm is costly. **F1** or **weighed fit** for a single summary. **Mean precision** rather than ROC AUC for the curve summary. ROC AUC stays flatteringly high when negatives dominate. 0.825 against an mean precision of 0.134 in the thresholds module.

Whichever you pick, pass it as `scoring=` to any cross-validation or search. Leaving it at the default tunes for fit. This On this data means tuning towards skipping the minority.

And report counts alongside rates. "Recall 0.55" is abstract. "we catch 27 of 49 cases and raise 400 false alarms" is a thing a person can judge.

## Where the rare class actually comes from

The remedies above treat imbalance as a property of the dataset. Often it's a property of how the dataset was built. That is worth checking before treating it.

**The window is too short.** Events that are rare per day are common per year. Widening the period at times turns a 0.5% problem into a 5% one with no other change.

**The unit of analysis is wrong.** Predicting whether a *transaction* is fraudulent may be a 0.1% problem while predicting whether an *account* has ever been fraudulent is a 5% one. Aggregating to the entity often makes both the imbalance and the guess problem easier. And at times it's the question the business really wanted.

**The negatives were over-collected.** Some datasets include each minus available and only the positives someone bothered to label. Sampling the negatives down is then not undersampling in the statistical sense. It's undoing an artefact of collection.

**The meaning is too narrow.** A stricter positive label means fewer positives. Loosening it. "escalated" rather than "escalated and confirmed". Can give a learnable problem whose output is still handy.

None of these is always available. All of them are worth ten minutes before spending a week on SMOTE variants. A reframing that changes the base rate helps more than any resampling scheme.

## What resampling does to the probabilities

A consequence that catches people after the model is working. Resampling changes the base rate the model believes in, and so its output chances.

Train on data weighed from 2% to 50% and the model learns a world where positives are half of all. Its predicted chances are calibrated to that world, not to yours. A "0.6" from it doesn't mean a 60% chance in production. It's systematically far too high.

For ranking and for thresholding that doesn't matter. Both are rule to a monotonic shift. It matters a great deal if the chance is used as a number. Expected value, risk scores shown to people, cost maths.

`class_weight` has a milder version of the same effect. Threshold tuning has none at all. It leaves the fitted model untouched. One more reason it's the remedy to try first.

If you do resample and need honest chances, recalibrate afterwards on data with the real class balance. This Is what `CalibratedClassifierCV` on an unresampled validation set does.

<strong>How imbalanced is too imbalanced?</strong> There's no threshold. A 1% problem with a strong signal is easy and a 30% problem with a weak one is hard. Measure recall on the minority rather than counting the ratio.

<strong>Is SMOTE worth installing imbalanced-learn for?</strong> Its pipeline is. It can resample inside cross-validation folds. This The scikit-learn one can't. SMOTE itself is often no better than threshold tuning.

<strong>Does class_weight work for regression?</strong> No - there are no classes. The equal is `sample_weight` at fit time. This Most estimators accept.

<strong>Should I resample the test set to make the metrics readable?</strong> No. The test set must reflect the real spread, or the numbers show a world that doesn't exist.

## Which models suffer most

Imbalance doesn't affect each estimator equally, and knowing the pattern saves some experimentation.

**any of it cutting an mean loss** feels it most right. Logistic regression, SVMs, neural networks, grad boosting. each row adds equally to the goal. The rare class adds almost nothing and the fit skips it. All of them accept `class_weight` or `sample_weight`. This Is the direct fix.

**Trees and forests** are affected through the split criterion. A split that isolates a handful of minority rows barely reduces impurity. It's rarely chosen. `min_samples_leaf` can prevent it fully. A leaf size of 20 on a class with 40 members is a severe constraint no one intended. Forests also suffer at the bootstrap stage. Here A rare class can be almost absent from some samples. `class_weight="balanced_subsample"` reweights per bootstrap rather than globally. This Is the version to use there.

**k-NN** is affected geometrically: with 98% negatives, the nearest neighbours of almost any point are minus. A minority point has to be in a very pure pocket to be found. Lowering `n_neighbors` helps, and `weights="distance"` helps more.

**Naive Bayes** is fairly solid. It models each class apart and the prior can simply be adjusted.

The general rule: the more a model means across all rows at once, the more the rare class is drowned out. The more a weight helps.

<strong>Can I combine the remedies?</strong> Yes. It's easy to overshoot. `class_weight="weighed"` plus oversampling plus a lowered threshold corrects three times for the same thing and floods you with false positives. Apply one, measure, then decide.

<strong>What about multi-class imbalance?</strong> The same ideas: stratify, use macro blending so small classes count. Pass `class_weight="weighed"`. This Handles any number of classes.

<strong>My minority class has 30 examples in total. What now?</strong> Very little, honestly. Thirty examples can't support a model of any cost. Each metric found from a handful of test cases moves in large steps. The productive answers are collecting more, widening the meaning, or treating it as outlier spotting rather than classification - `IsolationForest` and `OneClassSVM` model the majority and flag departures from it. This Needs no minority examples at all.

<strong>Why did class_weight make my fit worse?</strong> Because it's supposed to. Reweighting buys recall on the minority with precision and fit on the majority. If fit is what you're judged on, don't reweight - and reconsider whether fit is the right judgement.

## Things to try

1. <strong>Read the confusion mat.</strong> The first editor's model misses 46 of 49 positives and reports 96% fit.
2. <strong>Compare the remedies.</strong> The fifth editor's threshold row beats both others on F1 by a factor of three.
3. <strong>Watch the leak.</strong> In the fourth editor, the labels are random. The first number isn't a result.
4. <strong>Make it separable.</strong> In the last editor, lower `class_sep` to 0.5 and watch the need for a remedy return.

## Where this leaves you

Stratify the split, drop fit, and check whether the model is really struggling before doing any of it. If it's, move the threshold first, reach for `class_weight` second, and resample only inside the folds. Never before the split, and never on the test set.
""",
    [
        {"q": "A model reports 96% accuracy on data with 2% positives. What should you check first?",
         "options": ["Whether it is overfitting",
                     "The confusion matrix - it may be finding almost none of the positives",
                     "The learning rate",
                     "Whether the features are scaled"],
         "answer": 1,
         "why": "In the first editor that model found 3 of 49. Accuracy cannot distinguish it from a model that ignores the class entirely."},
        {"q": "Which remedy needs no refitting?",
         "options": ["class_weight=\"balanced\"",
                     "Moving the decision threshold",
                     "SMOTE",
                     "Undersampling"],
         "answer": 1,
         "why": "The probabilities are already there. In the editor it took the same fitted model from 6% recall to 41%, and it beat the other remedies on F1."},
        {"q": "Where must oversampling happen?",
         "options": ["Before the split, so both halves are balanced",
                     "Inside the folds, on the training part only",
                     "After fitting",
                     "On the test set as well"],
         "answer": 1,
         "why": "Resampling first puts duplicate rows on both sides of the split. On random labels that reported recall of 0.632 against an honest 0.324."},
        {"q": "Is imbalance always a problem?",
         "options": ["Yes, always",
                     "No - it hurts when the classes are also hard to separate",
                     "Only below 1%",
                     "Only for linear models"],
         "answer": 1,
         "why": "With the same 2% positives but separable classes, the untreated default model recalled 70.8%. Check before reaching for a remedy."},
    ],
)


# ---------------------------------------------------------------------------
# 22. k-means clustering
# ---------------------------------------------------------------------------
topic(
    "kmeans_clustering",
    "k-Means Clustering",
    "Models",
    "Grouping data with no labels at all - and the three assumptions it makes "
    "that decide whether the groups mean anything.",
    _svg(_dots([(34, 30), (44, 38), (28, 42), (40, 26)]) +
         _dots([(96, 60), (108, 68), (90, 70), (104, 54)]) +
         _dots([(112, 26), (124, 32), (118, 20)], M) +
         '<circle cx="36" cy="34" r="4" fill="none" stroke="var(--accent-primary)" stroke-width="2"/>' +
         '<circle cx="100" cy="63" r="4" fill="none" stroke="var(--accent-primary)" stroke-width="2"/>' +
         _txt(80, 86, "centres, and the points nearest each", M, 7)),
    [
        ("Fitting without a target",
         "No y anywhere - the estimator is given features and asked to find "
         "groups.",
         '''from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, true_labels = make_blobs(n_samples=300, centers=3, cluster_std=1.0,
                            random_state=0)

km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)

print("labels_ (first 12):", km.labels_[:12])
print("cluster_centers_:")
print(km.cluster_centers_.round(2))
print()
print("no y was passed - this is unsupervised. the labels are")
print("group numbers, and which group got which number is arbitrary.")
'''),

        ("Inertia cannot choose k for you",
         "It falls forever, so its minimum is always the largest k you tried.",
         '''from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=400, centers=4, cluster_std=1.0, random_state=0)

print("  k    inertia")
for k in range(1, 8):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    print("%3d %10.1f" % (k, km.inertia_))
print()
print("inertia always falls as k rises - at k = n it is zero.")
print("the bend is the signal, not the minimum.")
'''),

        ("Silhouette does have a maximum",
         "Which makes it the more useful of the two for choosing k.",
         '''from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=400, centers=4, cluster_std=1.0, random_state=0)

print("  k   silhouette")
best = None
for k in range(2, 8):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    s = silhouette_score(X, km.labels_)
    print("%3d %11.4f" % (k, s))
    if best is None or s > best[1]:
        best = (k, s)
print()
print("highest silhouette at k =", best[0], "- and unlike inertia,")
print("this one has a maximum rather than always falling.")
'''),

        ("Without scaling it clusters the units",
         "One noise column measured in a larger unit, and the grouping it finds "
         "is worthless.",
         '''from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score
import numpy as np

rng = np.random.RandomState(0)
y = np.array([0] * 150 + [1] * 150)

# Column 0 carries the grouping. Column 1 is noise, measured in a unit
# 500 times larger - so it dominates every distance.
signal = np.concatenate([rng.normal(0, 1, 150), rng.normal(5, 1, 150)])
noise = rng.normal(0, 1, 300) * 500.0
X = np.column_stack([signal, noise])

raw = KMeans(2, n_init=10, random_state=0).fit_predict(X)
scaled = KMeans(2, n_init=10, random_state=0).fit_predict(
    StandardScaler().fit_transform(X))

print("agreement with the true grouping (0.0 is chance, 1.0 is perfect):")
print("  unscaled:", round(adjusted_rand_score(y, raw), 4))
print("  scaled  :", round(adjusted_rand_score(y, scaled), 4))
print()
print("unscaled, the clustering is entirely decided by the noise column.")
'''),

        ("It only finds round, similar-sized groups",
         "Two interleaving crescents are the shape it cannot see.",
         '''from sklearn.cluster import KMeans, DBSCAN
from sklearn.datasets import make_moons
from sklearn.metrics import adjusted_rand_score

X, y = make_moons(n_samples=400, noise=0.06, random_state=0)

km = KMeans(2, n_init=10, random_state=0).fit_predict(X)
db = DBSCAN(eps=0.2, min_samples=5).fit_predict(X)

print("agreement with the true crescents:")
print("  KMeans:", round(adjusted_rand_score(y, km), 4))
print("  DBSCAN:", round(adjusted_rand_score(y, db), 4))
print()
print("k-means draws straight boundaries around round blobs, so two")
print("interleaving crescents are exactly what it cannot do.")
'''),

        ("The starting point matters",
         "Eight random starts, and they do not all land in the same place.",
         '''from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

X, _ = make_blobs(n_samples=300, centers=5, cluster_std=1.4, random_state=2)

inertias = []
for seed in range(8):
    km = KMeans(5, n_init=1, init="random", random_state=seed).fit(X)
    inertias.append(km.inertia_)
print("n_init=1, eight seeds:", [round(v, 1) for v in inertias])
print("  best %.1f, worst %.1f" % (min(inertias), max(inertias)))

good = KMeans(5, n_init=10, random_state=0).fit(X)
print()
print("n_init=10 (the default) keeps the best of ten:", round(good.inertia_, 1))
'''),
    ],
    [
        "Unsupervised: <code class='mono-font'>fit(X)</code> with no "
        "<code class='mono-font'>y</code>. The output is a group number per "
        "row, and the numbering is arbitrary.",
        "You must choose <code class='mono-font'>n_clusters</code> - the "
        "algorithm cannot discover how many groups there are.",
        "<code class='mono-font'>inertia_</code> falls monotonically with k, so "
        "look for the bend; <code class='mono-font'>silhouette_score</code> has "
        "an actual maximum.",
        "It measures distance, so it <strong>must</strong> have scaled features "
        "- unscaled, it clusters whichever column has the largest units.",
        "It assumes clusters are round, similar in size and similar in density; "
        "<code class='mono-font'>DBSCAN</code> handles shapes it cannot.",
        "The result depends on the random start, which is why "
        "<code class='mono-font'>n_init</code> repeats it and keeps the best.",
    ],
    """title: k-Means Clustering: A Practical Guide
intro: each model so far was told the answers. This one is given features and asked to find structure - which is a truly different job. One whose results are much harder to check.

## The algorithm

K-means is the most common clustering algorithm. It groups data points into `k` clusters by minimising the distance from each point to its cluster centre. You choose `k` in advance. The algorithm does the rest.

Clustering is unsupervised learning. There is no target column. The model finds structure in the features alone. That makes it useful for segmentation, anomaly detection and exploratory analysis. It also makes it harder to evaluate, because there is no ground truth to compare against.

K-means works best on data where the clusters are roughly spherical and roughly equal in size. It struggles with elongated clusters, clusters of very different densities, and clusters that overlap. Knowing these limits helps you decide whether k-means is the right tool or whether you need something like DBSCAN or Gaussian mixture models instead.

The algorithm is sensitive to feature scales. A column measured in thousands will dominate a column measured in single digits. Scaling before clustering is almost always necessary. It is also sensitive to the initial placement of the centres, which is why scikit-learn runs the algorithm several times with different starting positions and keeps the best result.

Choose `k`. Place `k` centres. Assign each point to its nearest centre, move each centre to the mean of the points assigned to it, and repeat until nothing moves.

That is the whole thing, and it settles quickly. `inertia_` is what it cuts. The total squared distance from each point to its centre.

The interface is the familiar one with a piece missing. `fit(X)` takes no `y`. There's none. `labels_` holds the group number for each training row, `cluster_centers_` holds the centres. `predict` assigns new points to the nearest existing centre.

The labels are any. Cluster 0 in one run may be cluster 2 in the next, with the same grouping. Checking two clusterings so needs a metric that skips the numbering. This Is what `adjusted_rand_score` is for.

## Choosing k is your problem

The method can't tell you how many groups exist. It will happily split one blob into five or merge five into two.

`inertia_` looks like it should help and can't. It falls monotonically. More centres always means points are closer to a centre. At `k = n` it's zero. The second editor shows the curve dropping from 4219 to 469 with no min in sight. The **elbow** is the heuristic. The point where the improvement flattens. And on this data the drops are 2213, 831, 472, 89, 78, 67. This Bends after 4.

`silhouette_score` is the better tool because it has a genuine max. For each point it checks the distance to its own cluster against the distance to the nearest other cluster. Means. Values run from -1 to 1. Higher means better-separated groups. The third editor peaks at k=4. This Is the number of blobs the data was made with.

Neither is authoritative. Both are heuristics on an ill-posed question. The honest answer often comes from outside. How many segments the business can act on, how many categories the taxonomy allows, what the groups turn out to mean when you look at them.

## Scale it, or cluster the units

k-means is fully distance-based, so an unscaled feature with large units decides all.

The fourth editor makes this stark. One column carries a real grouping. The other is pure noise measured in a unit 500 times larger. Unscaled, the match with the true grouping is **-0.0032**. Chance. Scaled, it's 0.9867.

The clustering wasn't merely worse. It was fully found by a column holding nothing. This is the same arg the scaling module made for k-NN. It applies with more force here because there's no label to notice the problem with. A guided model that clusters on noise scores badly and tells you. An unsupervised one makes groups. The groups look like a result.

`StandardScaler` in a pipeline before `KMeans` should be auto.

## What it assumes

Three assumptions, all baked into "assign each point to the nearest centre".

**Clusters are round.** The boundary between two centres is a straight line. Each cluster is a convex region. The fifth editor puts this against two interleaving crescents. K-means scores 0.27 and `DBSCAN` scores 1.00. No amount of tuning fixes it. The shape is outside what the method can express.

**Clusters are similar in size.** k-means tends to split a large cluster and merge small ones. That reduces total squared distance.

**Clusters have similar density.** A tight group and a diffuse one confuse the distance check.

When these hold, k-means is fast, simple and hard to beat. When they don't, the options are `DBSCAN` for any shapes and outliers, `GaussianMixture` for elliptical clusters of different sizes with soft sets. `AgglomerativeClustering` when a hierarchy is more handy than a flat split.

## The random start

The centres are was reset at random, and the method settles to a local min. So different starts give different answers.

The last editor runs eight single-start fits with random init and gets inertias from 1034.9 to 1188.6. Three of the eight found the good answer and five didn't.

`n_init` runs the whole thing a few times and keeps the lowest inertia. This Is why the default is 10 rather than 1. `init="k-means++"`, also the default, spreads the initial centres out rather than placing them at random. This Makes good answers much more likely and is the reason the default configuration mostly avoids this.

Both defaults are sensible and both are worth knowing about. A clustering that changes between runs is often one of these two being overridden.

## What the groups mean

Nothing, until you look.

k-means returns a split whether or not there's structure to find. Ask for four clusters in uniform noise and you get four. So the first question after fitting is always whether the groups are real. The second is what sets apart them.

The hands-on checks are checking the silhouette against what random data of the same shape scores, looking at the cluster centres in the first units to see what characterises each group. Checking the sizes for a cluster holding three rows.

The step that gives clustering its value is naming the groups. showing each in terms someone can act on. A split with no reading is a column of ints. The method can't supply the reading.

## Judging a clustering when there are no labels

Guided models are checked against the truth. Clustering has none. The metrics split into two families and it's worth knowing which you're allowed to use.

**inner** measures use only the data and the labels the method made. `silhouette_score` checks within-cluster distance against nearest-other-cluster distance. `calinski_harabasz_score` and `davies_bouldin_score` are options with different biases. All three reward compact, well-separated groups. Which means they systematically favour just the round, equal-sized clusters that k-means makes. Would score a correct DBSCAN clustering of two crescents poorly. They measure the shape you asked for, not whether the grouping is real.

**External** measures compare against known labels. `adjusted_rand_score` and `normalized_mutual_info_score` both skip the any numbering. This Is what makes them usable at all. Adjusted Rand is adjusted for chance. 0.0 is what random labelling scores and minus values are worse than random. Which is how the unscaled run above landed at -0.0032.

These are for the situation this track has been using throughout. Made data where the truth is known, or a subset somebody has labelled. In genuine unsupervised work there's nothing to compare against. The honest test is whether the groups turn out to be handy.

## Where clustering earns its place

Three uses, of which only one is what people often mean by clustering.

**Segmentation.** Finding groups of customers, docs or sessions that behave alike. That each can be treated differently. This is the familiar use. It's the one where the reading matters more than the method. A split no one can name isn't actionable.

**Compression and feature build.** The cluster label turns a cat feature for a guided model, or the distances to each centre become numeric ones. This often helps. It's subject to the usual rule. The clustering must be fitted inside the folds, or the labels carry info from the test rows.

**Finding what isn't in any group.** Points far from each centre are unusual. This Makes clustering a crude outlier finder. `DBSCAN` does this by name by labelling outliers `-1` rather than forcing them into a cluster. This Is one of its real edges over k-means.

The use to be careful with is treating clusters as though they were found categories. The method splits what it's given. Whether the split matches to any of it real is a separate question that the output can't answer.

<strong>Can I use k-means on cat data?</strong> Not sensibly - the mean of one-hot columns isn't a category. `KModes` outside scikit-learn, or a distance-based method with a cat metric.

<strong>What about many rows?</strong> `MiniBatchKMeans` fits on small random batches and is sharply faster on large data, at a small cost in quality.

<strong>Why does my clustering change between runs?</strong> Either `n_init=1` or no `random_state`. The defaults handle the first. Set the second for reproducibility.

<strong>Should the clustering go in a pipeline?</strong> Yes, if its output feeds a guided model - or else the cluster labels are learned from the test rows too.

## Reading the clusters once you have them

Fitting takes one line. Understanding the result takes rather more. Skipping it's how clustering projects end with a column of ints no one uses.

**Look at the centres in the first units.** `cluster_centers_` is in what space the model was fitted in. This After scaling is standard deviations rather than pounds or minutes. `scaler.inverse_transform(km.cluster_centers_)` puts them back. Reading the result column by column is what turns cluster 2 into "high spend, low rate, recent".

**Check the sizes.** `np.bincount(km.labels_)` in one line. A cluster with four members is often not a segment. It's an outlier group that k-means was forced to place a place because you asked for that many centres.

**Compare each cluster against the total mean.** Which features are most different from the global mean is a faster route to a description than reading the raw centres, above all with many columns.

**Check steadiness.** Refit on a random 80% and see whether the same groups appear. Clusters that dissolve when a fifth of the data changes are artefacts of the split rather than structure in the data. This test costs one loop.

The output of that work is a name and a description per group. That is the deliverable. The labels are an mid.

<strong>Is there a way to have k chosen automatically?</strong> Not by k-means. `DBSCAN` and `HDBSCAN` find the number of groups from the density instead. This Is a genuine edge when you've no prior view.

<strong>Does predict() work on new data?</strong> Yes - it assigns each new point to the nearest existing centre without refitting. This Is what makes a clustering usable as a feature in production.

<strong>Why is my silhouette score low though the clusters look right?</strong> Silhouette rewards compact, well-separated, roughly spherical groups. A correct clustering of elongated or touching groups scores poorly on it. This Is a limitation of the metric rather than of the clustering.

<strong>Does k-means work in high dims?</strong> Less well. Distances between points become more similar as dims grow. "nearest centre" carries less info. Reducing dims first - with PCA, say - is common practice and often helps.

<strong>Can two clusters end up empty?</strong> With random init, yes. Scikit-learn relocates empty clusters rather than leaving them. This Is one more thing `k-means++` makes unlikely.

## Things to try

1. <strong>Watch inertia fail.</strong> The second editor's numbers fall forever. Find the differences and find the bend yourself.
2. <strong>Break it with scale.</strong> The fourth editor's unscaled run scores below chance. Change 500 to 5 and see where the crossover is.
3. <strong>Try the wrong shape.</strong> In the fifth editor, raise `noise` to 0.15 and see whether DBSCAN still manages.
4. <strong>Cluster noise.</strong> Fit k=4 on `np.random.rand(300, 2)` and look at the silhouette. It won't be zero.

## Where this leaves you

Scale first, choose k with silhouette rather than inertia, keep `n_init` at its default. Check that the groups mean a thing before reporting them. When the clusters aren't round, the method is the wrong one rather than badly tuned.
""",
    [
        {"q": "Why can inertia_ not be used to choose k?",
         "options": ["It is not computed by default",
                     "It falls monotonically as k rises, reaching zero at k = n",
                     "It only works for two clusters",
                     "It requires labels"],
         "answer": 1,
         "why": "Its minimum is always the largest k you tried. The elbow is a heuristic on the curve; silhouette has an actual maximum."},
        {"q": "What happens if you run k-means on unscaled features?",
         "options": ["It scales them internally",
                     "The column with the largest units dominates the distance and decides the clustering",
                     "It raises an error",
                     "Nothing - it is scale-invariant"],
         "answer": 1,
         "why": "In the editor, a pure-noise column with a 500x larger unit took the agreement with the true grouping to -0.0032, which is chance."},
        {"q": "Why does k-means fail on two interleaving crescents?",
         "options": ["Too few iterations",
                     "Its boundaries are straight, so every cluster is a convex region",
                     "The data is not scaled",
                     "n_init is too low"],
         "answer": 1,
         "why": "Assigning each point to the nearest centre gives straight boundaries. DBSCAN scored 1.00 where k-means scored 0.27."},
        {"q": "What does n_init do?",
         "options": ["Sets the number of clusters",
                     "Repeats the whole fit from different starts and keeps the lowest inertia",
                     "Sets the iteration limit",
                     "Initialises the random seed"],
         "answer": 1,
         "why": "k-means converges to a local minimum, and eight single starts in the editor ranged from 1034.9 to 1188.6."},
    ],
)


# ---------------------------------------------------------------------------
# 23. A complete workflow
# ---------------------------------------------------------------------------
topic(
    "a_complete_workflow",
    "A Complete Workflow",
    "Models",
    "Every module in this track, applied once to one dataset, in the order you "
    "would actually do it.",
    _svg("".join(_box(8 + i * 30, 34, 24, 22, S, A if i == 5 else M, 2)
                 for i in range(5)) +
         _box(128, 34, 24, 22, S, A, 2) +
         _txt(80, 26, "look  split  build  check  tune  report", M, 7) +
         _txt(80, 76, "the test set opens once, at the end", A, 7)),
    [
        ("Look at the data first",
         "Four counts, before any modelling decision is made.",
         '''import numpy as np
import pandas as pd

def make_customers(n=2000, seed=0):
    """A small churn-shaped dataset: mixed types, gaps, imbalance."""
    rng = np.random.RandomState(seed)
    tenure = rng.randint(1, 72, n)
    monthly = rng.normal(65, 25, n).clip(20, 140)
    plan = rng.choice(["basic", "plus", "premium"], n, p=[0.5, 0.3, 0.2])
    region = rng.choice(["north", "south", "east", "west"], n)
    risk = (-0.04 * tenure + 0.02 * monthly
            + np.where(plan == "basic", 1.2, 0.0) + rng.normal(0, 1.0, n))
    churn = (risk > 2.6).astype(int)
    df = pd.DataFrame({"tenure": tenure, "monthly": monthly.round(2),
                       "plan": plan, "region": region})
    df.loc[rng.rand(n) < 0.08, "monthly"] = np.nan
    return df, pd.Series(churn, name="churn")

X, y = make_customers()
print("shape:", X.shape)
print("dtypes:", dict(X.dtypes.astype(str)))
print("missing:", dict(X.isna().sum()))
print("churn rate: %.3f (%d of %d)" % (y.mean(), y.sum(), len(y)))
'''),

        ("Split, and put the test set away",
         "Stratified, because 8% is not enough to leave to chance.",
         '''from sklearn.model_selection import train_test_split

X_dev, X_test, y_dev, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0, stratify=y)

print("development set:", X_dev.shape, " churn %.3f" % y_dev.mean())
print("test set       :", X_test.shape, " churn %.3f" % y_test.mean())
print()
print("the test set is now put away. everything that follows uses")
print("only the development set, until the very last step.")
'''),

        ("Build the pipeline",
         "Two branches, four learned transformations, one estimator - and "
         "nothing fitted outside it.",
         '''from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

numeric = ["tenure", "monthly"]
categorical = ["plan", "region"]

pre = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                          StandardScaler()), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])

pipe = Pipeline([("pre", pre),
                 ("clf", LogisticRegression(max_iter=1000,
                                            class_weight="balanced"))])

pipe.fit(X_dev, y_dev)
print("features after preprocessing:", pipe[:-1].transform(X_dev).shape[1])
print("names:", list(pipe.named_steps["pre"].get_feature_names_out()))
'''),

        ("Compare against doing nothing",
         "The baseline first, and a metric chosen for an 8% positive rate.",
         '''from sklearn.dummy import DummyClassifier
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, precision_score

# precision is undefined when nothing is predicted positive, which the
# dummy never does - make_scorer says what to return instead of warning.
scoring = {"AP": "average_precision",
           "recall": "recall",
           "precision": make_scorer(precision_score, zero_division=0)}

for label, model in [("dummy", DummyClassifier(strategy="most_frequent")),
                     ("pipeline", pipe)]:
    out = cross_validate(model, X_dev, y_dev, cv=5, scoring=scoring)
    print("%-10s" % label, "  ".join("%s %.3f" % (s, out["test_" + s].mean())
                                     for s in scoring))
print()
print("average precision is the summary to watch here - positives are 8%,")
print("so the dummy scores the base rate and ROC AUC would flatter both.")
'''),

        ("Tune the model and the preprocessing together",
         "Eight random samples, cross-validated, optimising the metric that "
         "matters.",
         '''from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import loguniform

grid = {"clf__C": loguniform(1e-2, 1e2),
        "pre__num__simpleimputer__strategy": ["mean", "median"]}

search = RandomizedSearchCV(pipe, grid, n_iter=8, cv=5,
                            scoring="average_precision",
                            random_state=0).fit(X_dev, y_dev)

print("best parameters:")
for k, v in sorted(search.best_params_.items()):
    print("   %-38s %s" % (k, round(v, 4) if isinstance(v, float) else v))
print("best cross-validated AP: %.4f" % search.best_score_)
print()
print("this number is optimistic - it is the best of eight tries.")
'''),

        ("Choose the threshold, then open the test set",
         "Once. The numbers this prints are the ones you are entitled to "
         "report.",
         '''from sklearn.metrics import (average_precision_score, precision_recall_curve,
                             classification_report)
import numpy as np, pickle

model = search.best_estimator_          # already refitted on all of X_dev

# Choose the threshold on the development set, never on the test set.
dev_proba = model.predict_proba(X_dev)[:, 1]
p, r, t = precision_recall_curve(y_dev, dev_proba)
f1 = 2 * p[:-1] * r[:-1] / np.clip(p[:-1] + r[:-1], 1e-12, None)
threshold = float(t[int(np.argmax(f1))])
print("threshold chosen on the development set: %.3f" % threshold)

# The test set, opened once.
test_proba = model.predict_proba(X_test)[:, 1]
print()
print("average precision on the untouched test set: %.4f"
      % average_precision_score(y_test, test_proba))
print()
print(classification_report(y_test, (test_proba >= threshold).astype(int),
                            digits=3, zero_division=0))

blob = pickle.dumps({"model": model, "threshold": threshold})
print("saved %d bytes - the pipeline and its threshold together" % len(blob))
'''),
    ],
    [
        "The editors on this page run <strong>in order</strong> and share one "
        "interpreter - it is a single script, split into steps.",
        "<strong>Look, split, build, check, tune, report.</strong> The order "
        "matters more than any individual choice in it.",
        "Everything that learns from data lives inside the pipeline, so the "
        "folds and the test set stay honest.",
        "The metric is chosen from the class balance, and the baseline is fitted "
        "before the model is believed.",
        "The threshold is a parameter: chosen on the development set, saved "
        "with the model.",
        "The test set is opened <strong>once</strong>, after every decision has "
        "been made.",
    ],
    """title: A Complete Workflow: A Practical Guide
intro: Twenty-two modules, applied to one small dataset in the order you'd really do it. Nothing here is new. The sequence is the point.

## The order

This page puts the earlier modules together into one end-to-end workflow. The dataset is small and deliberately messy: mixed types, missing values and imbalanced classes. The point is the sequence of steps, not the final score.

Each step in a machine-learning project depends on the one before it. Exploring the data tells you what preprocessing to apply. Splitting comes before preprocessing so the test set stays untouched. A baseline model tells you whether a tuned model is worth the effort. Evaluation on the test set comes last, and happens exactly once.

Skipping a step or reordering the sequence introduces errors that do not raise exceptions. Scaling before splitting leaks test-set statistics. Tuning without a baseline means you cannot tell whether the improvement came from the model or from the hyperparameters. Evaluating on the test set more than once turns it into a validation set.

The six editors on this page are one continuous script. They share a single interpreter. Each one uses variables that the previous one created. Running them out of order raises a `NameError`. That constraint is intentional. It mirrors the dependency structure of a real project.

**Look. Split. Build. Check. Tune. Report.**

Most of what goes wrong in applied machine learning is this sequence performed in a different order. Tuning before checking a baseline, splitting after prep, choosing a metric after seeing the scores. Each of those makes a number that can't be trusted. None of them makes an error.

The dataset here is small and synthetic: four columns of mixed type, 8% missing values in one of them. An 8% positive rate. That combination is on purpose plain. The point is the method rather than the result.

The six editors below are one script, not six examples. They share a single interpreter and each one uses what the last one defined. Run them in order from the top. Starting in the middle raises <code>NameError</code> for a variable an earlier step was supposed to create.

## 1. Look

Four counts, before any choice: the shape, the dtypes, the missing values per column, and the class balance.

Each one finds a later choice. The dtypes say which columns need encoding and which need scaling. The missing count says whether an imputer is needed and in which branch. The class balance. 8% here. Rules out fit as a metric and argues for a stratified split.

This step takes four lines and is the one most often skipped. each choice that follows is made in the dark without it.

## 2. Split

Right away, and stratified.

The test set is set aside now, before any of it has been fitted, scaled, imputed or selected. That is what makes the number at the end mean a thing. It's the single most key line in the script.

Stratifying matters at 8%: an unstratified 20% test set could easily land with a class rate of 5% or 11%. Each metric found from it would be shifted by an amount nothing reveals.

What remains is the **development set**. All up to the final step uses only that. Where this module says "development set", a larger project would cross-validate within it rather than splitting again.

## 3. Build the pipeline

Two branches, because the columns need different treatment.

Numeric columns get an imputer. With `add_indicator=True`. A missing charge may itself be helpful &mdash; and then a scaler. The model is smoothed and a fine on coeff size needs close units. cat columns get one-hot encoding with `handle_unknown="skip"`. A region absent from a training fold doesn't crash the run.

`class_weight="weighed"` goes on the model, because the positives are rare.

The key property is that **nothing is fitted outside this object**. The imputer's median, the scaler's mean, the encoder's category list and the model's coeffs are all learned inside `fit`. This Means they're all refitted on the training part of each cross-validation fold. The leakage module measured what happens or else.

Printing the feature names after prep is a cheap sanity check. Ten columns from four. Reading them confirms the missing indicator survived and the categories expanded as expected.

## 4. Check against a baseline

Two numbers, and the first one is the dummy.

`DummyClassifier(strategy="most_frequent")` scores an mean precision of 0.082. Just the base rate. This Is what mean precision does for a model with no skill. The pipeline scores 0.478. That gap is the evidence that the model has learned a thing. Without the first number the second is uninterpretable.

The metrics are chosen for the problem rather than accepted from the default. Mean precision because positives are rare and ROC AUC would flatter both models. Recall and precision alongside it. The single summary hides the trade.

`make_scorer(precision_score, zero_division=0)` appears because the dummy never predicts a plus. This Makes precision undefined. Saying what to return is better than five warnings in the output.

## 5. Tune

A randomised search over the model's smoothing and the prep's imputation strategy, scored on average precision.

Two things are worth noticing. The search covers a **prep** choice and a model one. This Is possible only because the prep is inside the pipeline. And `scoring="average_precision"` is passed by name. The default would optimise fit. And on 8% positives, fit prefers a model that predicts nothing.

`best_score_` comes out at 0.4829. That number is optimistic. It's the best of eight tries on the same folds. The setting-search module measured how much that inflates things. It's a guide for choosing, not a result to report.

## 6. Choose the threshold, then report

The threshold is a param. So It's chosen on the development set. Here by raising F1 along the precision-recall curve, though a cost math would be better if the costs were known.

Then the test set is opened, once. Mean precision on it's 0.5283. The classification report gives the per-class picture at the chosen threshold. Recall 0.667 and precision 0.468 on the positive class, from 33 positives in 400 rows.

Those numbers are the deliverable. They're honest because nothing about them was chosen after seeing them.

Finally the model is saved **with its threshold**. A pipeline pickled alone would be loaded elsewhere and used through `predict()`, silently reverting to 0.5. Which the thresholds module showed can be the difference between catching most of the positives and almost none.

## What is missing, and would come next

This is a complete workflow, not a complete project.

**A second model family.** Grad boosting would very likely beat this linear one. The whole script would change by one line. The pipeline interface doesn't care what the final estimator is.

**More features.** The learning-curve check from the overfitting module would say whether more data helps. Feature work often beats tuning when it doesn't.

**The timing question.** each column here was known at guess time by build. On real data that has to be asked of each one. It's the check no code performs.

**Monitoring.** A model is fitted on the past and used on the future. The spreads drift. What is measured after deployment matters as much as any of it measured before it.

## The checklist, without the code

The same method, stated so it can be applied to a dataset that looks nothing like this one.

**Before modelling.** Count the rows and columns. List the dtypes. Count missing values per column. Count the classes, or show the target's spread. Ask, of each column, whether it would be known at guess time.

**Splitting.** Stratify for classification. Group when a few rows share an entity. Order forward when the data has a time. Split before any of it learns.

**Building.** One pipeline. Numeric branch: impute, then scale if the model needs it. cat branch: impute, then encode with `handle_unknown="skip"`. Nothing fitted outside.

**Checking.** Fit a dummy. Choose a metric from the class balance and the cost of each mistake. Cross-validate with `return_train_score=True` and read the gap.

**Tuning.** Randomised search over a logarithmic range for smoothing, including prep choices, scored on the metric you chose. Check the winner isn't at the edge of the range. Read `cv_results_` and treat settings within one standard deviation as tied.

**Reporting.** Choose the threshold on development data. Open the test set once. Report the metric, the per-class breakdown, the counts behind the rates. The baseline beside them. Save the model with its threshold and the library version.

Nothing on that list is hard. The discipline is doing it in that order each time, including when the first result already looks good. Which is just when the temptation to skip to the end is strongest.

## When the result is disappointing

The method gives an honest number. The honest number is often lower than hoped. What to do next depends on a diagnosis the workflow has already made.

**Train and test both low.** Underfitting. More flexible model, better features, less smoothing. Tuning won't help.

**Train high, test low.** Overfitting. More smoothing, a simpler model, or more data. And the learning curve says whether more data would work.

**Both reasonable, but not good enough.** The features don't carry enough signal. This is the most common case and the least welcome. The answer is domain work rather than modelling. New features, a different unit of analysis, a reframed target.

**Barely better than the dummy.** Consider that the problem may not be predictable from these features at all. That is a legitimate finding. Reporting it early is far more valuable than six weeks of tuning towards it.

The workflow above is what makes each of those diagnoses available. A script that fits one model and prints one fit supports none of them.

<strong>Why is the test mean precision higher than the cross-validated one?</strong> Fold variation. With 33 positives in the test set the estimate is noisy. A small gap either way carries no info.

<strong>Should I refit on all before deploying?</strong> Yes, once the method is settled and the test score is recorded. More data gives a slightly better model - but the score you report is the one from the test set, not from the refit.

<strong>Where would a second model go?</strong> In the same search: `{"clf": [LogisticRegression(), RandomForestClassifier()]}` puts the choice itself in the grid, tested by the same cross-validation.

<strong>Is pickle the right way to save it?</strong> For your own short-lived use, yes. Record the scikit-learn version beside it. A pickle isn't portable across versions. Prefer `skops` for any of it shared.

## Where the track has taken you

Twenty-three modules, and the shape of them was deliberate.

The **API** came first, because `fit`, `predict` and `transform` are the part that transfers to each estimator in the library and to each one written after it. Learning the interface once is most of learning scikit-learn.

**Honest numbers** came second and took four modules. This Is more than the estimators got. That sorting reflects where the mistakes really are. A model is a few lines. Knowing whether its score is real is the hard part. Splitting, cross-validation, overfitting and the search's optimism are all facets of the same question.

**Preparing data** took six, because that is where leakage lives. Scaling, encoding, imputation and column routing are on their own simple. Each one of them learns a thing from data. Which is why they belong inside a pipeline and why the pipeline isn't a convenience.

**The models** came last and took the fewest. That is the honest proportion. Choosing between logistic regression, a forest and a booster matters far less than all before it. The library makes the choice a one-line change just so that it can.

What you can do now is take a table you've never seen, work out what it needs, build a pipeline that can't cheat. Give a number you'd defend. The left skill is domain knowledge about the columns. This No library supplies.

## Things to try

1. <strong>Swap the model.</strong> Change `LogisticRegression` to `RandomForestClassifier` in step three and re-run all after it. Nothing else needs to change.
2. <strong>Drop the indicator.</strong> Drop `add_indicator=True` and compare the cross-validated mean precision.
3. <strong>Break the order.</strong> Fit the imputer on all of `X` before the split. Watch the test score improve for the wrong reason.

## Where this leaves you

Look at the data, split it away, put all that learns inside a pipeline, compare against a baseline on a metric you chose on purpose, tune with cross-validation, pick the threshold from the cost. Open the test set once. That is the whole of it. The order is what makes the last number worth reporting.
""",
    [
        {"q": "When should the test set be split off?",
         "options": ["After preprocessing, so both halves are prepared the same way",
                     "Immediately, before anything that learns from data",
                     "After tuning",
                     "It does not matter with cross-validation"],
         "answer": 1,
         "why": "Anything fitted before the split - a median, a scaler, a category list - has seen the test rows, and the final number is no longer honest."},
        {"q": "Why fit a DummyClassifier at all?",
         "options": ["It is required by cross_validate",
                     "Its score is the floor that makes the model's score interpretable",
                     "It initialises the pipeline",
                     "It handles the class imbalance"],
         "answer": 1,
         "why": "The dummy scored 0.082 average precision, exactly the base rate. Without it, 0.478 is a number with no scale."},
        {"q": "Why pass scoring=\"average_precision\" to the search?",
         "options": ["It is faster",
                     "The default optimises accuracy, which on 8% positives prefers predicting nothing",
                     "It is required for pipelines",
                     "It avoids a warning"],
         "answer": 1,
         "why": "The metric decides which candidate wins. Leaving it at the default tunes towards ignoring the rare class."},
        {"q": "Why save the threshold alongside the model?",
         "options": ["To document the experiment",
                     "Because predict() reverts to 0.5, which may catch almost nothing",
                     "Pickle requires it",
                     "So the model can be refitted"],
         "answer": 1,
         "why": "The threshold is part of the decision the model makes. Loaded without it, the served model silently uses a default nobody chose."},
    ],
)
