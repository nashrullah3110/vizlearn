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
intro: scikit-learn has one interface and about two hundred algorithms behind it. Learning the interface is most of learning the library.

## The problem it solves

Every machine-learning library has to answer the same question: how does a program hand data to an algorithm and get an answer back. scikit-learn answered it once, in 2007, and then made every algorithm in the library answer it the same way.

The result is that `fit`, `predict` and `transform` are almost the whole API. A linear regression, a random forest, a support-vector machine and a k-means clustering all expose the same three methods, so the code around a model does not change when the model does.

## fit learns, predict answers

`fit(X, y)` shows the estimator the data and the answers, and it stores what it worked out on the object. `predict(X)` takes new data with no answers and produces them.

The split matters more than it looks. Fitting and predicting are separate calls because they happen at different times on different data &mdash; you fit once on data you have, and predict many times on data you did not have when you fitted.

## The underscore convention

scikit-learn marks learned attributes with a trailing underscore, and the convention is worth taking seriously because it divides an estimator into two halves.

Attributes without an underscore are **hyperparameters**: settings you chose, passed to the constructor, present before any data was seen. `n_neighbors`, `max_depth`, `fit_intercept`.

Attributes with a trailing underscore are **learned**: they did not exist before `fit` and they came from the data. `coef_`, `intercept_`, `feature_importances_`, `classes_`.

Reading an estimator therefore tells you what it was told and what it worked out, and the two never get confused. It also means `hasattr(model, "coef_")` is a reliable test for "has this been fitted", which is exactly what the library's own `check_is_fitted` does.

## Transformers change features rather than predicting

A transformer is the other half of the library. Instead of `predict` it has `transform`, and instead of producing a target it produces a new version of `X`.

`StandardScaler` is the canonical one: `fit` computes the mean and standard deviation of each column, `transform` subtracts and divides. `OneHotEncoder`, `SimpleImputer` and `PCA` are all the same shape.

`fit_transform` does both in one call and is the one you will write most often on training data. It is not merely shorthand &mdash; for some transformers it is faster than doing the two separately, which is why it exists as its own method.

The rule that matters: **fit on training data only, transform everything**. A scaler fitted on the test set has learned from data the model is supposed to have never seen, and the score you get afterwards is not a score.

## The shapes

`X` is two-dimensional: rows are samples, columns are features. `y` is one-dimensional: one value per row of `X`.

That holds even when there is one feature, which is where beginners meet their first error. A list of six numbers is six samples of nothing, not one sample of six features, and scikit-learn refuses to guess which you meant. `reshape(-1, 1)` turns a flat array into a column, and the error message says so explicitly.

## The two kinds of estimator

Everything in the library is one of two things, and telling them apart tells you which method to call.

A **predictor** ends in a target. `LinearRegression`, `LogisticRegression`, `RandomForestClassifier`, `KMeans` &mdash; you `fit` them and then `predict`. Classifiers additionally offer `predict_proba`, which returns the probability of each class rather than the winning one.

A **transformer** ends in new features. `StandardScaler`, `OneHotEncoder`, `SimpleImputer`, `PCA` &mdash; you `fit` them and then `transform`. There is no target to produce, so there is no `predict`.

The two compose: a chain of transformers followed by one predictor is the shape of essentially every real scikit-learn program, and `Pipeline` exists to hold exactly that chain and give it the same `fit`/`predict` interface as a single estimator. That is why the API is worth learning first &mdash; a whole pipeline is used the same way as the simplest model in the library.

## score, and what it means for each

Every predictor has a `score(X, y)` method, and the number it returns is not the same quantity for all of them.

For a **classifier**, `score` is accuracy: the proportion of predictions that were right. For a **regressor**, it is R&sup2;: how much of the variation in the target the model accounts for, where 1.0 is perfect and 0.0 is no better than always guessing the mean. R&sup2; can be negative, which means the model is worse than that guess.

Both are conveniences rather than recommendations. Accuracy is misleading whenever the classes are imbalanced, and R&sup2; says nothing about whether the errors are large in the units you care about. Later modules replace both with metrics that answer a specific question, and the `metrics` module holds several dozen of them.

What `score` is genuinely useful for is a quick comparison on the same data with the same model type, and for the cross-validation helpers, which call it by default when you do not name a metric.

## Hyperparameters are set at construction

The constructor takes the settings, and there are usually many of them with sensible defaults. `RandomForestClassifier()` works, and so does `RandomForestClassifier(n_estimators=500, max_depth=8, random_state=0)`.

Two methods make those settings inspectable. `get_params()` returns every hyperparameter as a dictionary, including the defaults you did not pass, which is the fastest way to find out what an estimator can be configured with. `set_params(**kw)` changes them on an existing object.

Those two are not conveniences either &mdash; they are what makes automated tuning possible. `GridSearchCV` works by calling `set_params` with each combination in turn, which is why it can tune any estimator in the library, including ones written after it, and any step inside a pipeline.

The corollary is worth remembering: an estimator is fully described by its hyperparameters plus its fitted attributes. Nothing else is hidden on it.

## random_state, and reproducibility

Anything in the library that makes a random choice takes a `random_state`. Splitting data, initialising k-means, sampling features in a random forest, shuffling folds &mdash; all of them.

Passing an integer makes the run reproducible: the same data and the same seed give the same result, every time, on any machine. Leaving it out gives a different answer on each run, which makes two scores incomparable and a bug impossible to reproduce.

The habit worth forming early is to pass `random_state=0` to everything that accepts it while you are learning or debugging, and to think carefully before removing it. The one time you genuinely want it left out is when you are deliberately measuring how much the result varies between runs &mdash; which is a real question, and one that a single seeded number cannot answer.

## When an estimator has not been fitted

Calling `predict` before `fit` raises `NotFittedError` rather than returning nonsense, and the message names the estimator and tells you to call `fit`.

That check exists because the alternative is worse. An unfitted model has no coefficients, and a library that quietly returned zeros or `None` would produce a program that runs, produces numbers, and is entirely meaningless.

It is also why the underscore convention matters practically rather than only stylistically: `check_is_fitted` works by looking for attributes ending in an underscore. An estimator you write yourself gets the same behaviour for free by following the same convention.

## Why one interface was the right decision

It is worth appreciating how unusual this is. Most machine-learning code before scikit-learn had a shape per algorithm: one library wanted a matrix and a separate label vector, another wanted them combined, a third wanted a configuration file. Comparing two algorithms meant rewriting the code around them, which meant people compared far fewer than they should have.

Fixing the interface changed what is cheap. Swapping a model becomes one line, so trying five is a loop rather than a project. Cross-validation can be written once and work with anything, because it only needs `fit`, `predict` and `score`. A pipeline can hold arbitrary steps, because every step honours `fit` and `transform`. A tuner can search any estimator, because `get_params` and `set_params` are universal.

None of that required the algorithms to have anything in common mathematically. A decision tree and a linear model share no theory at all; they share three method names, and that turned out to be enough to build the entire ecosystem of helpers on top.

The practical consequence for someone learning: time spent on the API is not overhead before the interesting part. It *is* the part that transfers. The estimators are individually simple to use once the shape is familiar, and the modules that follow spend most of their words on when each one is appropriate and how to tell whether it worked, rather than on how to call it.

## What the library deliberately does not do

Knowing the boundary saves looking for things that are not there.

scikit-learn does not do deep learning. There is a small `MLPClassifier`, useful for a demonstration and not for real work; anything serious belongs in PyTorch or a similar library. It does not do GPUs. It does not do sequence models, text generation, or anything with the word "neural" beyond that one estimator.

It does not handle data loading, cleaning or plotting. Data arrives as arrays or DataFrames that pandas produced, and results are plotted with matplotlib. Those are separate libraries on purpose, and the boundary is clean: scikit-learn takes numeric arrays and returns numeric arrays.

It also does not do statistical inference. A linear model gives you coefficients and no p-values, no confidence intervals and no hypothesis tests, because the library is built around prediction rather than explanation. `statsmodels` is the library for that question, and reaching for it is the right answer rather than a workaround.

<strong>Is the API stable?</strong> Remarkably so. Code written against `fit`/`predict` a decade ago still runs, which is unusual in this field and is a large part of why the library is worth learning properly.

## Things to try

1. <strong>Run the first editor.</strong> `hasattr(model, "coef_")` is False before `fit` and True after. That is the whole of what fitting does, visible in one line.
2. <strong>Change the data.</strong> Make the relationship non-linear &mdash; `y = [1, 4, 9, 16, 25, 36]` &mdash; and watch `coef_` become a compromise rather than an exact fit.
3. <strong>Swap the model.</strong> In the fifth editor, add `from sklearn.svm import SVR` and put `SVR()` in the list. Nothing else changes.
4. <strong>Break the shape.</strong> In the last editor, read the error properly. It names the shape it got and the shape it wanted.

## Where this leaves you

Three method names, one shape convention and one naming convention cover the surface of the entire library. Everything from here is a choice of estimator and, far more importantly, whether the number it reports can be believed. """,
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
intro: Before any model can be fitted, the data has to be two objects of exactly the right shape. Almost every first error on this track is one of the two this page ends with.

## The shape the library insists on

scikit-learn takes two things: a two-dimensional `X` and a one-dimensional `y`.

`X` has one row per sample and one column per feature. If you have 150 flowers and four measurements of each, `X.shape` is `(150, 4)`. The convention is universal across the library, and it is the reason a table of data maps onto it so directly &mdash; rows are observations, columns are variables, which is how a spreadsheet is already arranged.

`y` has one entry per row of `X`. For a regression it holds numbers; for a classification it holds labels, which may be integers or strings. `y.shape` is `(150,)` &mdash; note the trailing comma, which is what a one-dimensional shape looks like in NumPy.

The library will not guess when the shapes are wrong, and that refusal is worth appreciating rather than resenting. A list of six numbers could be six samples of one feature or one sample of six features, and those are entirely different problems. Rather than pick one, scikit-learn raises and tells you what it received.

## Where practice data comes from

Three families of function, distinguished by their prefix.

`load_*` returns a small dataset that ships inside the installed package. `load_iris`, `load_wine`, `load_digits`, `load_diabetes`, `load_breast_cancer` and a couple more. They are tiny, they need no network, and they are what almost every example in the documentation uses. Their size is the point: a model fits in milliseconds, so you can try something and see the result immediately.

`fetch_*` downloads a larger, more realistic dataset the first time and caches it. `fetch_california_housing`, `fetch_20newsgroups`, `fetch_openml` for anything on OpenML. These are the ones to use when the toy datasets stop being convincing &mdash; but they need a network, which is why this track stays with the bundled ones.

`make_*` generates data with the structure you asked for. `make_classification`, `make_regression`, `make_blobs`, `make_moons`. These are the most underrated of the three, because they let you construct exactly the situation you want to study: a dataset with two informative features and eight useless ones, or classes that are deliberately not linearly separable, or a regression with a known amount of noise. When you are testing whether a technique does what you think, generated data with known properties beats real data whose properties you are guessing at.

## The Bunch, and the two ways past it

The `load_*` and `fetch_*` functions return a `Bunch`, which is a dictionary that also allows attribute access. `data.target` and `data["target"]` are the same object, which is why examples use both spellings interchangeably.

A Bunch carries more than the arrays. `feature_names` gives the column names, `target_names` maps the integer labels back to something readable, and `DESCR` holds a full description of the dataset &mdash; where it came from, what each column means, and how many samples there are. Printing `DESCR` is the fastest way to understand an unfamiliar bundled dataset, and it is routinely ignored.

`return_X_y=True` skips the Bunch and returns the two arrays as a tuple, which is what you want when you already know the dataset and just need the data. It makes the common line short: `X, y = load_iris(return_X_y=True)`.

`as_frame=True` returns pandas objects instead of NumPy arrays: `data.frame` is a DataFrame with the target as a column, and `data.data` becomes a DataFrame with named columns. This matters more than it first appears, because a DataFrame carries its column names into the estimator, which is what lets a fitted model report `feature_names_in_` and what lets a `ColumnTransformer` select columns by name rather than by position.

## Turning your own data into X and y

Real data rarely arrives in the right shape, and the conversion is usually one comprehension.

From a list of dictionaries, build `X` by pulling the feature keys in a fixed order and `y` by pulling the target key. The order matters and must be the same for every row, which is exactly what a list comprehension guarantees and a hand-written loop does not.

From a pandas DataFrame it is shorter still: `X = df[["rooms", "area"]]` and `y = df["price"]`. Selecting with a list of column names gives a DataFrame, which is 2-D and therefore a valid `X`; selecting with a single name gives a Series, which is 1-D and therefore a valid `y`. Getting those two confused &mdash; `df["rooms"]` where `df[["rooms"]]` was meant &mdash; produces the 1-D error message, and the doubled brackets are the fix.

The one rule that survives every source: decide the column order once, and keep it. A model fitted on columns in one order and given new data in another will not complain. It will produce confident nonsense, because column three is column three whatever it used to mean.

## The two errors, and what they are telling you

**"Expected 2D array, got 1D array instead."** You passed something with one dimension where `X` was wanted. The message goes on to suggest `reshape(-1, 1)` if the data has a single feature and `reshape(1, -1)` if it is a single sample, and choosing between those two is choosing what your data means. `-1` tells NumPy to work that dimension out from the length.

**"Found input variables with inconsistent numbers of samples: [3, 2]."** `X` and `y` disagree about how many rows there are, and the numbers in brackets are the two counts in order. This one almost always means an upstream filter was applied to one and not the other &mdash; dropping rows with missing targets from `y` but not from `X`, say &mdash; and the fix belongs there rather than at the call that raised.

Both messages name the shapes involved, which makes them among the more helpful errors you will meet. Reading them before changing anything is faster than guessing, and the shape they report is usually enough on its own to identify which of the two objects is wrong.

## Sparse matrices, and when one appears

Some transformers do not return a normal array. `OneHotEncoder` and the text vectorisers return a **sparse matrix**, which stores only the non-zero entries and their positions.

The reason is size. One-hot encoding a column with ten thousand distinct values produces ten thousand columns, almost all of them zero on any given row. Stored densely that is enormous and almost entirely wasted; stored sparsely it is a list of the few positions that are not zero.

You will notice it in three ways. Printing one shows a summary rather than the numbers. Indexing behaves differently from a NumPy array. And some estimators accept it happily while others raise, because not every algorithm can be written to work on that representation.

`.toarray()` converts to a dense array, and is the right move only when you are certain the result fits in memory &mdash; which is exactly the case the sparse representation existed to avoid. `sparse_output=False` on the encoder is the better fix when the number of columns is genuinely small. Most of the time the correct answer is to leave it sparse, because the estimators that matter for high-dimensional data all handle it.

## Looking at the data before fitting anything

The step that gets skipped, and the one that catches the problems a model will silently absorb.

Four questions are worth answering before any `fit`. **How many rows and columns**, from `X.shape` &mdash; a model with more features than samples behaves quite differently from one with the reverse. **What range each feature covers**, because a column measured in millions next to one measured in fractions is the situation that makes scaling necessary. **Whether anything is missing**, since `np.isnan(X).sum()` costs nothing and most estimators refuse to fit with `NaN` present. And **how the target is distributed** &mdash; for a classifier, the count per class, because that single number decides whether accuracy is a meaningful metric at all.

None of these require plotting or a lengthy exploration. Four lines before the first `fit` catch the majority of problems that would otherwise appear later as an inexplicable score.

The one that matters most is the class balance. A dataset that is 99% one class will let almost any classifier report 99% accuracy, and a reader who has not counted will believe it.

## Feature names, and why they are worth keeping

Passing NumPy arrays works, and passing DataFrames gives you something arrays cannot: the model remembers what the columns were called.

A fitted estimator that was given a DataFrame gains `feature_names_in_`, and several report results against those names rather than against positions. `feature_importances_` on a tree, `coef_` on a linear model, and the output of `get_feature_names_out()` on a transformer are all far easier to read when there is a name attached to each number.

It also adds a safety check. Fit on a DataFrame and then predict on one whose columns are in a different order, and scikit-learn raises rather than silently using the wrong column &mdash; which is the failure mode that arrays cannot protect you from at all.

The cost is that a DataFrame is slower than an array and that some operations convert back to arrays anyway, losing the names partway through a pipeline. That is why `get_feature_names_out()` exists on transformers: it reconstructs the names on the other side of a step that dropped them, including the invented names that one-hot encoding produces.

The habit worth adopting: use DataFrames at the boundary where data enters, and stop worrying about whether the middle of the pipeline is arrays or frames.

## Things to try

1. <strong>Print the description.</strong> Add `print(load_iris().DESCR[:800])` to the first editor. It explains the columns, the classes and where the data came from.
2. <strong>Change the generated data.</strong> In the third editor, set `n_informative=1` and see that four of the five features are noise by construction &mdash; useful when testing whether a model can ignore them.
3. <strong>Trigger the shape error deliberately.</strong> Pass `data.data[0]` as `X` and read what it suggests. One sample needs `reshape(1, -1)`, not `reshape(-1, 1)`.
4. <strong>Compare the two representations.</strong> Fit anything on `as_frame=True` data, then check `model.feature_names_in_`. With plain arrays that attribute does not exist.

## Where this leaves you

Two objects, two shapes, and three prefixes for finding data to practise on. The next module takes that data and does the one thing that has to happen before any score means anything: splitting it.
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
