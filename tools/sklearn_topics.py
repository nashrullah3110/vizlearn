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

<strong>Should I use the bundled datasets for anything real?</strong> No. They are for learning the mechanics. Iris in particular is small, clean and nearly separable, which makes almost every method look good on it.

<strong>Can I pass a Python list instead of an array?</strong> Yes, for X and y both - scikit-learn converts them. Arrays and DataFrames are preferable because they carry a dtype and, for frames, the column names.

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
intro: A model's score on the data it learned from tells you how well it memorised, not how well it works. The split is what turns one into the other.

## The problem it solves

A model that has seen a row can reproduce its answer. That is not a discovery about the model; it is a property of having been shown the answer.

So a score computed on the training data measures memorisation, and some models memorise perfectly. An unconstrained decision tree will score 1.0 on its training set essentially every time, because it can keep splitting until every sample sits in its own leaf. Report that number and you are reporting the model's capacity to store data, which is not what anyone wants to know.

The question worth answering is what happens on data the model has never seen, because that is the only situation it will ever face in use. Holding some rows back and never letting the model touch them is the simplest honest way to find out.

## What the call does

`train_test_split` shuffles the rows and cuts them into two groups, returning four objects: the features and target for training, then the features and target for testing.

The return order is `X_train, X_test, y_train, y_test` &mdash; both X pieces before either y piece &mdash; and getting it wrong is the single most common early mistake with this function. The failure is not always loud: swapping `X_test` and `y_train` produces a shape error, which is fine, but swapping `y_train` and `y_test` produces a program that runs and reports a meaningless number.

Any number of arrays can be passed and they are all split the same way, on the same rows, which is what keeps `X` and `y` aligned. That property is the whole reason to use the function rather than slicing by hand.

## random_state, and what reproducibility buys

The split is random, so without a seed each run produces a different one, and therefore a different score.

That matters more than it sounds. If you change a hyperparameter and the score moves from 0.94 to 0.96, you need to know whether the change did that or whether the split did. With a fixed seed, the split is held constant and the difference is attributable. Without one, you are comparing two things that differ in two ways.

It also makes a bug reproducible. A model that fails on one split and not another is telling you something real, and you cannot investigate it if you cannot get back to the split that failed.

Passing an integer is enough. The specific value carries no meaning &mdash; `random_state=0` and `random_state=42` are equally arbitrary &mdash; and the only thing that matters is that it stays the same across the runs you intend to compare.

There is one honest use for leaving it out: measuring how much the score varies between splits, which is a real question and one that a single fixed split cannot answer. The proper tool for that is cross-validation, which repeats the exercise systematically rather than relying on you to run it a few times.

## stratify, and the split that misrepresents the data

A random split does not guarantee the two halves look alike. On a dataset with three equal classes, a plain split can easily hand you a test set with 17 of one and 14 of another, and on a dataset where one class is rare, it can hand you a test set containing none of it at all.

`stratify=y` fixes this by sampling within each class, so both halves carry the same proportions as the original. The cost is nothing, and for classification it should be the default rather than an option you remember on difficult datasets.

Where it becomes essential is imbalance. With 1% positives and a 20% test set, an unstratified split has a real chance of putting so few positives in the test set that the metric computed from them is noise. Stratifying guarantees the proportion, which is the minimum needed for the number to mean anything.

You can stratify on something other than the target by passing a different array &mdash; a group label, say &mdash; which is occasionally what you want when the target is continuous but some categorical variable must stay balanced.

## The split has to come first

The order of operations matters, and getting it wrong is the most common way to produce an inflated score.

Everything learned from data must be learned from the training set alone. That includes the obvious &mdash; the model &mdash; and the less obvious: the mean and standard deviation used for scaling, the categories known to an encoder, the median used to fill missing values, the vocabulary of a text vectoriser, and the feature-selection decision about which columns to keep.

Scale the whole dataset and then split, and the scaler has seen the test set. The test score afterwards is not a score on unseen data, because information from those rows reached the model through the scaler's parameters. The effect is usually small and occasionally enormous, and it is always in the direction of making the model look better than it is.

The rule that follows is short: **split first, and fit every transformer on the training half only**. Pipelines exist largely to make that structurally impossible to get wrong, which is why they arrive later in this track and why they are not optional in real work.

## How big should the test set be

The convention is 20% or 25%, and the convention is a compromise between two things pulling in opposite directions.

A larger test set gives a more reliable estimate, because the score is computed from more samples and is less at the mercy of which particular rows landed there. A smaller test set leaves more data for training, which usually produces a better model.

With a lot of data, the tension disappears: 1% of a million rows is ten thousand test samples, which is plenty. With a few hundred rows, both halves are uncomfortable &mdash; the estimate is noisy and the model is starved &mdash; and that is precisely the situation where a single split should be replaced by cross-validation, which uses every row for both purposes without ever training and testing on the same one.

The other consideration is the rarest class. A test set that contains four examples of something can only report accuracy on it in steps of 25%, and no amount of careful metric choice recovers from that.

## Time changes the rules

When rows are ordered in time, shuffling is wrong.

Shuffling puts rows from after the test period into the training set, so the model learns from the future and is then asked to predict the past. It will do well, and the score will be worthless, because the situation it was scored in cannot occur in use &mdash; in production, the future is exactly what you do not have.

`shuffle=False` keeps the order and takes the last portion as the test set, which is the right shape: train on the past, test on the more recent. Note that `stratify` cannot be used with `shuffle=False`, and the two are conceptually incompatible anyway.

For anything more careful, `TimeSeriesSplit` provides the cross-validation equivalent: a series of splits, each training on everything up to a point and testing on what comes next. The same reasoning applies to any structure with groups that must not be broken across the split &mdash; several rows per patient, per user, per document &mdash; where `GroupShuffleSplit` keeps a group entirely on one side.

## What the test set is for, and what it is not

A held-out set answers one question: how does this model behave on data it has not seen. It stops answering that question the moment you use it to make a decision.

This is the part that gets lost. If you fit five models, look at the test score for each, and pick the best, you have used the test set to choose a model &mdash; and the winner's score is now optimistic, because it was selected for doing well on those particular rows. Do it a dozen times, tweaking as you go, and the test set has been fitted to as surely as if you had trained on it, just more slowly and by hand.

The standard remedy is three sets rather than two. **Train** to fit the model, **validation** to compare models and tune hyperparameters, and **test** touched exactly once at the very end to report a number. In practice the validation half is usually replaced by cross-validation on the training data, which uses the data better, and the test set is still set aside and left alone.

The discipline is easier to state than to keep: every look at the test set costs a little of its honesty. Nested cross-validation exists for the situation where you cannot afford even that, and is the correct answer when the difference between two models is small enough to matter.

## Splits that respect structure

A plain random split assumes rows are independent, and often they are not.

**Several rows per entity.** Ten readings from the same patient, several photographs of the same object, multiple purchases by one customer. A random split puts some of an entity's rows in training and others in test, so the model can recognise the entity rather than learn the pattern, and the score is inflated by an amount nothing in the output reveals. `GroupShuffleSplit` and `GroupKFold` take a `groups` array and keep each group whole.

**Time.** Covered above, and worth repeating because it is so easy to get wrong: `shuffle=False`, or `TimeSeriesSplit`.

**Nested or hierarchical data.** Pupils within schools, measurements within sites. The same reasoning as groups &mdash; if the model can identify the container, it will.

The question to ask before splitting is simply: could two rows on opposite sides of the split share something that would let the model cheat? If the answer is yes, a plain random split will overstate the score, and the amount is unpredictable.

<strong>Is 80/20 a rule?</strong> It is a convention that suits a few thousand rows. With a million, 1% is a fine test set; with two hundred, a single split is the wrong tool and cross-validation is the right one.

<strong>Should the test set be split off before cleaning?</strong> Before anything that <em>learns</em> from the data, yes. Dropping obviously corrupt rows is fine either way; imputing a median is not.

## Things to try

1. <strong>Run the fourth editor.</strong> The training score is 1.0 and the test score is not. That gap is the entire reason this page exists.
2. <strong>Remove random_state.</strong> Run the same editor three times and watch the test score move. Then put it back.
3. <strong>Make a class rare.</strong> Keep only ten samples of class 2, split without `stratify`, and count the classes in the test set a few times with different seeds.
4. <strong>Break the order.</strong> In the last editor, compare the shuffled and unshuffled test rows. The shuffled set contains rows from the beginning of the series.

## Where this leaves you

One line, four objects, and three arguments worth setting deliberately every time: `random_state` so the experiment is repeatable, `stratify` so the halves resemble each other, and `shuffle=False` when the rows are ordered in time. What it gives you is a number you are entitled to report.
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
intro: The model whose parameters you can read, whose failures are visible, and whose coefficients are misread more often than any other number in the library.

## What it is fitting

Linear regression finds one number per feature, plus an intercept, such that adding them up predicts the target as closely as possible.

For one feature that is a straight line through a scatter of points. For three features it is a plane in four dimensions, which nobody can picture and which behaves exactly the same way arithmetically: multiply each feature by its coefficient, add the intercept, and that is the prediction.

"As closely as possible" has a precise meaning: it minimises the sum of the *squared* differences between predictions and actuals. Squaring is what makes the problem solvable in one step rather than by search &mdash; there is a formula, and scikit-learn uses it &mdash; and it is also why the model is sensitive to outliers. A residual of 10 contributes a hundred times more than a residual of 1, so one badly wrong point pulls the line further than a dozen slightly wrong ones.

## Reading the fitted model

`coef_` is an array with one entry per column of `X`, in the same order as the columns. `intercept_` is a single number: the prediction when every feature is zero.

Together they are the entire model. There is nothing else stored, no data kept, no lookup table &mdash; which is why a fitted linear regression is a few numbers regardless of whether it was trained on a hundred rows or a hundred million.

That readability is the model's main practical advantage. A coefficient of 25.2 on `rooms` says: holding the other features fixed, one more room is associated with 25.2 more units of price. The phrase "holding the other features fixed" is doing real work in that sentence and is the part people drop &mdash; a coefficient is not the effect of a feature on its own, it is the effect after the other features in the model have accounted for what they can.

The intercept is often meaningless in isolation. A house with zero rooms and zero area does not exist, so the intercept is where the line happens to cross rather than a prediction anyone would make. It matters for the arithmetic and rarely for the interpretation.

## The coefficient trap

This is the most commonly repeated mistake about linear models, and it is worth being blunt: **the size of a coefficient tells you nothing about the importance of a feature.**

A coefficient is expressed in units of target per unit of feature. Measure area in square metres and the coefficient is some number; measure the same area in hectares and the coefficient is ten thousand times larger. The model is identical, the predictions are identical, the R&sup2; is identical. Only the units changed.

So comparing coefficients across features only means something if the features are on the same scale. Standardising them first &mdash; subtracting the mean and dividing by the standard deviation &mdash; makes the coefficients comparable, and they then answer "how much does the prediction move per standard deviation of this feature", which is a question worth asking.

Even then, "importance" is slippery. Two correlated features share the credit between them in a way that depends on the noise, so a feature can have a small coefficient because a correlated one absorbed the signal rather than because it does not matter. Permutation importance answers the question more honestly, and this track's tree modules cover the alternatives.

## R-squared, and what a negative value means

`score()` on a regressor returns R&sup2;, and its definition is a comparison rather than an absolute measure: how much of the variation in the target the model accounts for, relative to a baseline that always predicts the mean.

1.0 means the predictions are exact. 0.0 means the model does exactly as well as always guessing the average &mdash; which is to say it has learned nothing useful. Values in between are the usual case.

A **negative** R&sup2; surprises people and is entirely possible. It means the model is worse than predicting the mean, which happens routinely on a test set when a model has overfitted, and always indicates something is wrong rather than merely weak.

The number's weakness is that it is unitless and therefore not directly meaningful. An R&sup2; of 0.85 does not tell you whether the predictions are wrong by pounds or by thousands of pounds, and that is usually the question that matters. The next module covers the metrics that answer it.

## What "linear" actually restricts

The name misleads. Linear regression is linear in its *coefficients*, not in the data, and the distinction is what makes it far more flexible than it appears.

Adding `x**2` as an extra column lets a linear model fit a parabola exactly. Adding `x1 * x2` lets it capture an interaction between two features. Adding `log(x)` lets it fit a curve that flattens. In every case the model is still linear &mdash; it is still multiplying each column by a coefficient and adding &mdash; because the non-linearity is in the *feature*, not in the fitting.

`PolynomialFeatures` automates this by generating all the powers and products up to a degree you choose. It is genuinely useful and it grows quickly: degree 3 on ten features produces 286 columns, most of them useless, and the model will happily fit noise with them. Which is the standard trade this track keeps returning to.

## When it is the wrong model

Three situations where linear regression struggles, and knowing them saves fitting it and being puzzled.

**Genuinely non-linear relationships**, unless you construct the features to capture them. A tree-based model finds them without being told what shape to look for, which is why gradient boosting is the usual default on tabular data.

**More features than samples.** The solution is no longer unique &mdash; infinitely many coefficient sets fit the training data perfectly &mdash; and plain linear regression has no principle for choosing between them. Ridge and Lasso add one, which is exactly what regularisation is for.

**Highly correlated features.** Two columns carrying almost the same information make the coefficients unstable: small changes in the data produce large swings in how the credit is divided, and the individual numbers stop being interpretable even though the predictions remain fine.

For the second and third, `Ridge` is the drop-in replacement and is a better default than plain `LinearRegression` for anything with many features. It uses the same interface, adds one hyperparameter, and gives up a little training accuracy for coefficients that do not move around.

## Ridge and Lasso, in one paragraph each

Two variants solve the problems at the end of the previous section, and both are one-line replacements.

**Ridge** adds a penalty proportional to the sum of the squared coefficients. The effect is to shrink them all towards zero, more so as `alpha` increases, which stops any one of them growing large to chase noise. It handles correlated features gracefully &mdash; rather than one coefficient swinging positive and another negative, both end up moderate and stable. `Ridge(alpha=1.0)` is a sensible default and a better starting point than plain `LinearRegression` whenever there are more than a handful of features.

**Lasso** penalises the sum of the *absolute* coefficients instead, and that change has a striking consequence: it drives some coefficients to exactly zero rather than merely small. So it selects features as well as fitting them, and the fitted model names the columns it decided to ignore. The cost is that among correlated features it tends to pick one arbitrarily and zero the rest, which makes the selection unstable even when the predictions are fine.

`ElasticNet` combines the two penalties for when you want both properties. All three take `alpha`, all three need the features scaled first &mdash; a penalty on coefficient size is meaningless when the coefficients are in incomparable units &mdash; and all three are tuned with the cross-validated search covered later in this track.

## The assumptions, and which ones matter in practice

Textbooks list four or five assumptions behind linear regression. For prediction, which is what this library is for, they matter less than the textbooks imply, and it is worth knowing which is which.

**Linearity** is the one that genuinely matters. If the relationship curves and you have not given the model a curved feature, the predictions will be systematically wrong in a pattern &mdash; too low at the ends and too high in the middle, or the reverse. Plotting residuals against predictions makes it obvious: a good fit shows a shapeless cloud, and a missed curve shows an arc.

**Independent errors** matters for time series and grouped data, and is the reason those need different splitting. Nothing about the fit detects it.

**Constant error variance** and **normally distributed errors** are assumptions of the *inference* &mdash; the p-values and confidence intervals that scikit-learn does not compute. If you only want predictions, violating them costs you accuracy in some regions rather than validity. If you want to make a claim about whether a coefficient is significantly different from zero, you want `statsmodels`, and then they matter.

The practical version: look at the residuals for a pattern. A pattern means a missing feature or the wrong shape of model, and no amount of regularisation fixes either.

<strong>Should I use LinearRegression or Ridge by default?</strong> Ridge, for anything with more than a few features. It costs one hyperparameter and removes the instability that plain least squares has when columns are correlated.

<strong>Does it need scaled features?</strong> Plain linear regression does not - the fit is identical either way. Ridge, Lasso and ElasticNet do, because their penalty is on coefficient size.

<strong>Why does fitting take no iterations?</strong> Ordinary least squares has a closed-form solution, so the answer is computed directly rather than searched for. That is why there is no `max_iter` and no convergence warning on this estimator.

<strong>What is `positive=True` for?</strong> It constrains every coefficient to be non-negative, which is occasionally what physics or accounting requires - mixing proportions, for instance, where a negative contribution is meaningless.

<strong>Can it handle missing values?</strong> No. It raises on `NaN`, which is why imputation comes earlier in a pipeline than the model does.

## Things to try

1. <strong>Add an outlier.</strong> In the first editor, change one price to 400 and watch the slope move. Squared errors mean one bad point has a large vote.
2. <strong>Read the units.</strong> The fifth editor makes the coefficient trap concrete. Fit both, then look at the R&sup2; column and note it does not move.
3. <strong>Fit the curve.</strong> In the last editor, try degree three by adding `x ** 3` as a third column and check whether R&sup2; improves on data that is genuinely quadratic.
4. <strong>Break it deliberately.</strong> Give the model two identical columns and look at the two coefficients. The sum is stable; the split between them is not.

## Where this leaves you

Two learned arrays, one formula, and a score that compares the model against guessing the mean. The coefficients are readable, which is the model's great advantage, and readable in a way that requires care about units before any of them can be compared.
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

Every regression metric summarises the same thing &mdash; the gaps between predictions and actuals &mdash; and they differ in how they weigh those gaps. That weighting is not a technical detail. It is a claim about which errors are worse, and the claim should come from the problem rather than from habit.

If being wrong by 10 twice is exactly as bad as being wrong by 20 once, you want MAE. If one large miss is disproportionately damaging, you want RMSE. If a 10% error on a small value matters as much as a 10% error on a large one, you want a percentage metric. These are different situations and they genuinely occur, which is why the library ships several dozen metrics rather than one.

## MAE: the average size of the mistake

Mean absolute error is the average of the absolute differences. Nothing is squared, so every error contributes in proportion to its size.

Its great virtue is that it is expressed in the units of the target. If you are predicting house prices in pounds, an MAE of 5,333 means the typical prediction is out by about five thousand pounds. That sentence can be said to somebody who has never heard of a regression, and they can tell you whether it is acceptable.

That is a genuinely important property. Most of the value of a model is decided by a person who has to judge whether the errors are tolerable, and they cannot judge that from a unitless number. MAE is the default worth reaching for when the answer will be reported to anyone.

It is also robust: a single wild outlier moves it by its own size and no more.

## RMSE: the same idea, with big errors amplified

Root mean squared error squares each error, averages, and takes the square root. The squaring is the whole difference.

Squaring makes a large error count for much more than several small ones adding to the same total. The editors on this page show it exactly: two sets of predictions wrong by 75 in total have the same MAE of 15, and RMSE of 15.00 and 33.54 respectively. The second concentrated its error in one place, and RMSE says so.

Whether that is desirable depends entirely on the application. For predicting delivery times, being an hour late once may be far worse than being twelve minutes late five times &mdash; the customer notices the hour. For predicting daily sales, the total is what matters and the distribution of errors is not especially important.

The square root at the end puts the number back into the units of the target, so RMSE is comparable to MAE in magnitude. RMSE is always at least as large as MAE, and the gap between them tells you how unevenly the errors are distributed &mdash; equal means uniform, a wide gap means a few large misses.

MSE without the square root is the same ranking in squared units, which are uninterpretable. It appears because it is what the fitting minimises and what differentiates cleanly, not because anyone should report it.

## R-squared: a comparison, not a measurement

R&sup2; asks how much of the variation in the target the model accounts for, compared against a model that always predicts the mean.

1.0 is perfect, 0.0 is no better than the mean, and negative means worse than the mean &mdash; which is common on a test set and always a signal rather than a curiosity.

Two things make it popular. It is unitless, so it can be compared across problems with different targets. And it has a built-in baseline, so a value tells you something without a separate comparison run.

Two things make it dangerous. It says nothing about the size of the errors, so an R&sup2; of 0.87 is compatible with being wrong by five pounds or five thousand. And it depends on the variance of the target in the test set, which means the same model scores differently on two test sets drawn from the same data &mdash; a narrow test set makes the model look worse simply because the mean baseline is harder to beat.

Use it for comparing models on the same data. Do not use it to decide whether a model is good enough for a purpose, and do not compare it across datasets.

## MAPE, and why it is both loved and distrusted

Mean absolute percentage error expresses each error as a fraction of the true value and averages those.

Its appeal is obvious: "we are typically 6% out" is a sentence anyone understands, and it is comparable across products, regions or scales in a way an absolute number is not.

Its problems are equally real. It is undefined when any true value is zero, and rather than raising, scikit-learn returns an enormous number &mdash; the editor above shows 1.65e+17 &mdash; which will propagate through an averaging step and produce nonsense nobody notices. It is asymmetric: over-predicting is penalised differently from under-predicting, which biases model selection towards forecasting low. And it explodes for true values that are merely small rather than zero, so a few near-zero rows can dominate the average entirely.

If percentages are what the audience wants, MAPE is usable on strictly positive data with no small values. Otherwise, quote MAE alongside the mean of the target and let the reader do the division.

## Always compare against doing nothing

`DummyRegressor` predicts the mean, or the median, or a constant you choose, ignoring the features entirely. Fitting one takes a line and it is the most valuable line in an evaluation.

The reason is that no metric is interpretable in isolation. An R&sup2; of 0.4 could be an excellent result on a genuinely noisy problem or a terrible one on an easy problem. An MAE of 5,000 is meaningless without knowing that the mean baseline scores 12,000 &mdash; or 5,200, in which case the model has bought almost nothing for its complexity.

That last case is more common than people expect, and it never shows up unless the baseline is run. A model that beats the mean by 4% is not necessarily worth deploying, maintaining and explaining, and the number that tells you so takes two lines to produce.

## The neg_ prefix

`cross_val_score` and every search helper are written to maximise: they assume bigger is better, so that the same code can rank any metric without knowing which one it is.

Error metrics are the wrong way round for that, since smaller is better. Rather than special-case them, scikit-learn negates them: `neg_mean_absolute_error` returns -15 where MAE would return 15, and maximising -15 towards zero is the same as minimising 15.

So the values come back negative and you flip the sign to read them. It is startling the first time, and it is the reason `scoring="mean_absolute_error"` raises an error naming the valid options. `sorted(sklearn.metrics.get_scorer_names())` lists all of them, which is faster than guessing the spelling.

## Errors that are not symmetric

All four metrics on this page treat over- and under-prediction as equally bad. Often they are not.

Under-predicting demand means empty shelves and lost sales; over-predicting means stock that has to be written off. Under-estimating a journey time annoys a customer; over-estimating loses the booking. Under-forecasting a load causes an outage; over-forecasting costs money. In every one of those the two directions have different prices, and a symmetric metric will happily choose a model that is wrong in the expensive direction.

Two ways to handle it. Write a custom scorer with `make_scorer`, which takes a function of `(y_true, y_pred)` and a `greater_is_better` flag, and put the real cost in that function &mdash; if a unit of over-prediction costs three times a unit of under-prediction, say so arithmetically. Or use **quantile regression**, where the model is fitted to predict a chosen percentile rather than the mean: fitting the 80th percentile gives predictions that are deliberately high most of the time, which is what you want when running out is worse than having spare.

`GradientBoostingRegressor(loss="quantile", alpha=0.8)` does the second directly, and the asymmetry then lives in the model rather than only in the report.

## Reading errors as a distribution

A single averaged number hides everything about the shape of the errors, and the shape is usually where the information is.

Two habits repay the minute they cost. **Plot residuals against predictions.** A shapeless cloud means the model has extracted what it can. An arc means a missing non-linearity. A fan that widens to the right means the errors grow with the size of the target, which often argues for predicting the logarithm instead.

**Look at the worst cases.** Sorting by absolute error and reading the ten worst rows tells you more about a model than any summary statistic. Usually they have something in common &mdash; a category the training data barely covered, a period with an unusual event, rows with a missing field imputed to the median &mdash; and that commonality is a feature waiting to be added or a subset the model should not be trusted on.

Neither of these appears in a metric, and both change what you do next.

<strong>Which metric should I optimise during training?</strong> Usually squared error, because it is smooth and fast to fit. You can report a different one - fitting and reporting need not use the same metric, and often should not.

<strong>Is RMSE always bigger than MAE?</strong> Yes, or equal when every error is the same size. The ratio between them measures how uneven the errors are.

<strong>How do I see every valid scoring name?</strong> `sorted(sklearn.metrics.get_scorer_names())`, which is quicker than guessing at the spelling.

## Things to try

1. <strong>Run the second editor.</strong> Same total error, same MAE, RMSE more than twice as large. That single comparison is the whole argument for choosing between them.
2. <strong>Add an outlier.</strong> In the first editor, change one prediction to 400 and watch which metrics move most.
3. <strong>Beat the baseline by less.</strong> In the fifth editor, raise `noise` to 200 and see how much of the model's advantage survives.
4. <strong>Get the spelling wrong.</strong> Ask for `scoring="mae"` and read the error - it lists every valid name.

## Where this leaves you

MAE for reporting to a person, RMSE when large errors are disproportionately costly, R&sup2; for comparing models on identical data, and a dummy baseline underneath all three. Which one you lead with is a decision about the problem, not about the model.
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
