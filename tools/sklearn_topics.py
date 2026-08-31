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

<strong>Should I report one metric or several?</strong> Several, and always with the baseline beside them. MAE answers "how wrong, typically", RMSE answers "are there occasional disasters", and the dummy answers "compared to what". Any one of the three alone is easy to misread, and together they take one extra line to produce.

<strong>My R-squared is high and the predictions look bad. How?</strong> Almost always a target with large variance, where beating the mean is easy and still leaves errors that matter in absolute terms. Look at MAE next to the mean of the target.

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
intro: The classifier to try first, whatever the problem. It is fast, it produces probabilities rather than bare labels, and it gives every other model a number to beat.

## Why it is called regression

The name is the first confusion and it has a real explanation. Logistic regression is a classifier &mdash; it predicts which class a sample belongs to &mdash; but the thing being fitted linearly is not the class.

What it fits is the **log-odds**: the logarithm of the ratio between the probability of the positive class and the probability of the negative one. That quantity runs from minus infinity to plus infinity, which makes it something a linear model can predict sensibly. The logistic function then squashes it back into the range 0 to 1, giving a probability.

So underneath it is a linear regression on a transformed target, and the transformation is what turns an unbounded prediction into a probability that cannot escape its bounds. Predicting the probability directly with linear regression would happily produce 1.4 or -0.3, which is why nobody does that.

## Probabilities, not just labels

`predict` returns the class. `predict_proba` returns the probability of each class, as an array with one column per class in the order given by `classes_`.

The second is almost always more useful, and the reason is that `predict` throws away information you needed. A prediction of "positive" with probability 0.51 and one with probability 0.99 are wildly different situations, and `predict` reports them identically.

That matters wherever the two kinds of mistake have different costs. A medical screen that is 51% confident should probably be followed up; one that is 99% confident may warrant immediate action. A fraud check at 51% might ask for a second factor while one at 99% blocks the transaction. None of that is expressible if all you have is the label.

`predict` is exactly `predict_proba` with a threshold of 0.5, and 0.5 is a default rather than a principle. Choosing a different threshold is one of the highest-value adjustments available, and it gets its own module later in this track.

## Reading the coefficients

`coef_` has the same shape story as linear regression &mdash; one number per feature &mdash; but the units are different and the difference is the part people get wrong.

A coefficient is the change in log-odds for a one-unit increase in the feature, holding the others fixed. Log-odds are not intuitive, so the conventional move is to exponentiate: `exp(coef)` is an **odds ratio**, the factor by which the odds multiply per unit of the feature.

A coefficient of 1.17, as in the editor above, means the odds multiply by about 3.2 for each step of one in that feature. That is a statement about odds, not about probability, and the two diverge: multiplying odds by 3.2 moves a probability of 0.1 to about 0.26, but moves 0.5 to about 0.76 and 0.9 to about 0.97. The same coefficient has a different effect on probability depending on where you start, which is the whole point of the logistic curve being a curve.

The scale caveat from linear regression applies with equal force. A coefficient's size depends on the feature's units, so coefficients are only comparable to each other when the features were standardised first &mdash; and since the model needs scaling anyway, this usually comes for free.

## It has to be scaled

Unlike ordinary linear regression, logistic regression is fitted by iterative optimisation. There is no formula; a solver takes steps towards a minimum and stops when it stops improving or when it runs out of iterations.

Features on wildly different scales make that surface awkward to descend, so the solver takes far more steps and often hits `max_iter` first. When it does, scikit-learn issues a `ConvergenceWarning` and returns the half-finished model anyway &mdash; it does not raise, and the coefficients you get are simply wherever the solver had reached.

The editor above shows both cases on the same data: unscaled and it warns, scaled and it converges comfortably within the same budget.

The right fix is `StandardScaler`, not a larger `max_iter`. Raising the iteration limit makes the warning go away by letting the solver grind to the same answer more slowly; scaling makes the problem easy. Raising `max_iter` is the correct response only when the features are already scaled and the model is genuinely large.

There is a second reason scaling matters here: `LogisticRegression` applies L2 regularisation **by default**, controlled by `C`. A penalty on coefficient size is meaningless when the coefficients are in incomparable units, so an unscaled fit is regularised unevenly across features without saying so.

## C, and the regularisation nobody notices

`LogisticRegression()` is regularised out of the box, which surprises people who expect a plain maximum-likelihood fit.

The strength is set by `C`, and the parameter is **inverted**: small `C` means strong regularisation, large `C` means weak. `C=1.0` is the default, `C=0.01` shrinks the coefficients hard, and `C=1000` is close to unregularised. The inversion catches everybody at least once, because every other penalty parameter in the library &mdash; `alpha` in Ridge and Lasso &mdash; runs the other way.

The default is usually reasonable, and `C` is one of the first things worth tuning. With many features it is often the only hyperparameter that matters.

`penalty="l1"` gives the Lasso-style behaviour of driving some coefficients to exactly zero, which selects features as it fits; it requires a compatible solver such as `liblinear` or `saga`.

## More than two classes

Nothing changes at the call site. Fit on a target with three classes and `predict` returns one of the three, `predict_proba` returns three columns summing to one, and `coef_` gains a row per class.

Underneath, recent versions fit a genuine multinomial model when the solver supports it, which estimates all the classes jointly rather than running a series of one-against-the-rest fits. The practical consequence is that the probabilities are properly normalised across classes rather than being separate binary probabilities rescaled afterwards.

`classes_` is worth reading rather than assuming. It holds the classes in sorted order, and the columns of `predict_proba` follow it &mdash; so with string labels, `["cat", "dog", "fish"]`, column 0 is cat. Indexing that array the wrong way round is a quiet way to report the wrong probability.

## What it cannot do

The decision boundary is a straight line &mdash; a plane in higher dimensions &mdash; and no amount of tuning changes that.

For data that genuinely needs a curved boundary, the model will do its honest best and be beaten by anything that can bend. The editor above makes it concrete: on two interleaving crescents, logistic regression manages 0.84 and a decision tree 0.99, and the gap is entirely structural.

Two responses. Engineer features that make the problem linear &mdash; adding squares and products via `PolynomialFeatures` lets a linear boundary in the expanded space be a curved one in the original. Or use a model that finds the shape itself, which is what trees and their ensembles do and why they dominate on tabular data.

Neither makes logistic regression a poor first choice. It fits in milliseconds, needs almost no tuning, produces calibrated-ish probabilities and coefficients you can read, and tells you immediately whether the problem is easy. A gradient-boosted ensemble that beats it by two points may not be worth the complexity; one that beats it by thirty tells you the structure is genuinely non-linear.

## Are the probabilities trustworthy?

A model that outputs 0.7 is making a claim: among the cases it labels 0.7, about 70% should turn out positive. A model whose probabilities satisfy that is **calibrated**, and not every classifier is.

Logistic regression is unusually good here. Because it is fitted by maximising the likelihood of the observed labels, well-calibrated probabilities are what it is directly optimising for, and on reasonable data it produces them. That is a real advantage over models that output a score which merely ranks correctly &mdash; a random forest's averaged votes and an SVM's distance from the boundary both rank well and are systematically off as probabilities, usually pushed towards the middle or the extremes.

Two things spoil it even here. Heavy regularisation shrinks the coefficients and pulls the probabilities towards 0.5. And a badly imbalanced training set, or one resampled to fix imbalance, shifts them wholesale.

`CalibratedClassifierCV` wraps any classifier and fits a correction on held-out data, which is how you get usable probabilities out of a model that does not produce them naturally. Checking calibration is a matter of bucketing predictions and comparing the average predicted probability against the observed rate in each bucket &mdash; `calibration_curve` does it in a line, and it is worth doing whenever a probability is going to be used as a number rather than as a ranking.

## Which solver, and when it matters

`LogisticRegression` takes a `solver`, and the default handles most cases, but the choice becomes relevant in three situations.

`lbfgs` is the default: fast, handles multinomial fits directly, supports only L2 and no penalty. `liblinear` is the one to use for L1 on a small dataset, and it fits one-against-the-rest rather than a true multinomial. `saga` supports L1, L2 and ElasticNet, handles sparse data well, and is the one to reach for on large or high-dimensional problems &mdash; text, in particular. `newton-cholesky` is efficient when there are many samples and few features.

The practical rule: leave it alone until something makes you change it. The two things that will are asking for a penalty the default cannot do, which raises a clear error naming the compatible solvers, and a fit that is slow on a large sparse matrix, where `saga` is the answer.

<strong>Does it work with more than two classes?</strong> Yes, with no change at the call site. `coef_` gains a row per class and `predict_proba` gains a column, in `classes_` order.

<strong>Can the target be strings?</strong> Yes. `classes_` holds them sorted, and predictions come back as the same strings.

<strong>Why is my accuracy 0.99 and the model useless?</strong> Almost certainly imbalance - if 99% of rows are one class, predicting that class always scores 0.99. The classification metrics module covers what to use instead.

## Where it sits among the alternatives

Three models occupy nearly the same space, and knowing what separates them saves trying all three blindly.

**Linear SVM** draws a straight boundary too, and chooses it by maximising the margin between the classes rather than by maximising likelihood. It is often marginally more accurate and gives no probabilities without an extra calibration step, which is usually the deciding factor against it.

**Naive Bayes** is faster still and makes a strong independence assumption between features. On text it works surprisingly well despite that assumption being obviously false, and it is the right first try for a bag-of-words problem.

**Gradient boosting** finds non-linear structure without being told where to look and generally wins on tabular data by a clear margin. It costs tuning time, fits slower, and gives up the readable coefficients.

The sequence worth following is: logistic regression first for the number to beat, gradient boosting second to find out whether the problem has structure a line cannot see, and anything else only if those two leave a specific gap.

## Things to try

1. <strong>Look at the probabilities.</strong> In the second editor, find the rows nearest 0.5. Those are the ones where the label is close to arbitrary.
2. <strong>Break convergence.</strong> In the fourth editor, drop `max_iter` to 20 on the scaled data and watch the warning return.
3. <strong>Turn regularisation up.</strong> Fit with `C=0.001` and compare the coefficients to the default. They shrink towards zero together.
4. <strong>Bend the boundary.</strong> In the last editor, wrap the logistic model in a pipeline with `PolynomialFeatures(degree=3)` and see how much of the gap closes.

## Where this leaves you

A fast linear classifier that returns probabilities, needs its features scaled, is regularised by default with an inverted parameter, and draws a straight boundary. Fit it first on every classification problem, and treat its score as the number anything more complicated has to justify itself against.
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
intro: A single train/test split gives you one number drawn from a distribution you never see. Cross-validation shows you the distribution.

## The problem with one split

A held-out test set answers the question honestly, and it answers it once, on one particular random selection of rows.

Run the split again with a different seed and the score moves. The editors on this page show six splits of the same data giving scores from 0.9737 to 0.9912 &mdash; a spread of nearly two points, on an easy dataset with several hundred rows. On a smaller or harder dataset the spread is much wider.

That variation is not noise you can ignore. If you compare two models on one split each and they differ by a point, you have learned nothing: the difference is well inside the range a single split produces by chance. Reporting the winner would be reporting which model got the friendlier rows.

Cross-validation fixes this by not choosing. It splits the data into `k` parts, holds each one out in turn, fits on the rest, and returns `k` scores &mdash; so every row is tested on exactly once and trained on `k-1` times.

## What the k numbers tell you

The mean is the headline, and the standard deviation is the part people skip.

A mean of 0.98 with a standard deviation of 0.006 is a stable, believable result. A mean of 0.98 with a standard deviation of 0.09 says the model works well on some subsets and badly on others, which is a completely different situation and usually means either very little data or a subgroup the model handles poorly.

Two models whose ranges overlap heavily are not distinguishable by this evidence, whatever their means. That single habit &mdash; looking at the spread before believing a difference &mdash; prevents a large share of the wasted effort in applied machine learning.

`cross_val_score` returns the array. Printing it rather than only its mean costs nothing and is where the information is.

## How many folds

`cv=5` is the usual default and `cv=10` the other common choice, and the trade between them is straightforward.

More folds mean each model trains on more data, so each is closer to the model you would build on the whole dataset, and the estimate is less pessimistic. More folds also mean more fits &mdash; ten-fold takes twice as long as five-fold &mdash; and the training sets overlap more, which makes the scores more correlated and the standard deviation an underestimate of the true variability.

The extreme is `LeaveOneOut`, where `k` equals the number of samples. Every model trains on everything but one row, which is as close to the full-data model as possible, and it costs `n` fits. It is worth it only on very small datasets, and its variance estimate is poor for the same correlation reason.

Five is a reasonable default for most work. Ten when the dataset is small enough that the extra fits are cheap and you want the training sets larger. `RepeatedStratifiedKFold` runs the whole thing several times with different shuffles when you need a more reliable estimate of the spread.

## Stratification happens by default, and only for classifiers

Pass an integer as `cv` and scikit-learn chooses the splitter for you: `StratifiedKFold` when the estimator is a classifier, plain `KFold` otherwise.

That default is a good one and worth understanding rather than relying on blindly. The editor above shows what plain folds do to an imbalanced target: with five minority samples across five folds, the counts come out 2, 1, 0, 1, 1 &mdash; one fold contains none of the class at all, so the recall computed on it is undefined and the score for that fold is meaningless. Stratified folds give exactly one to each.

Note that stratification is on the **target**. When the thing that must stay balanced is something else &mdash; a site, a batch, a demographic group &mdash; you need to pass a splitter object rather than an integer.

## The rule that makes it honest

Cross-validation is only honest if everything learned from data is learned inside the loop.

That includes the model, obviously. It also includes the scaler's mean and standard deviation, the imputer's median, the encoder's list of categories, the vectoriser's vocabulary, and &mdash; most damagingly &mdash; any feature selection.

The fifth editor makes the cost concrete. The data is pure random noise with no relationship between features and target, so the honest accuracy is 0.5. Selecting the twenty "best" features using the whole dataset and then cross-validating gives **0.825**. The selection looked at the held-out rows, found the columns that happened to correlate with the target in those rows too, and handed the model a shortcut. Doing the selection inside the folds gives 0.45, which is the truth.

That is not a small distortion, and it is the single most common way published results turn out to be wrong. With 2000 candidate features and 120 samples, some columns correlate with the target by chance; choosing them using all the data is choosing them partly on the test rows.

`Pipeline` is the mechanism that prevents this. A pipeline is a single estimator as far as `cross_val_score` is concerned, so its `fit` &mdash; including every transformer inside it &mdash; runs on the training part of each fold only. Using one is not a style preference; it is what makes the number mean what it says.

## What cross-validation does not give you

It does not give you a model. The `k` models fitted during the process are scored and thrown away.

What it gives you is an estimate of how well **the procedure** performs &mdash; this preprocessing, this estimator, these hyperparameters, on data like this. Once you have decided the procedure is good enough, you fit it once more on all the data, and that is the model you keep. `cross_val_predict` returns the out-of-fold predictions if you want them for inspection, and it is explicitly not a way of producing a model either.

It also does not replace a final held-out test set when you have been using cross-validation to make choices. Comparing twenty hyperparameter settings by cross-validation and reporting the best one's score is optimistic for the same reason as picking the best of twenty test scores: the winner was selected for doing well on those particular folds. Nested cross-validation is the rigorous answer, and a separate untouched test set is the practical one.

## The splitters worth knowing

`cv` accepts an integer or a splitter object, and the objects are how you say something the integer cannot.

`StratifiedKFold` and `KFold` are the defaults, and passing them explicitly lets you set `shuffle=True` and a `random_state`, which the integer form does not. Note that `KFold` does **not** shuffle by default, so data arriving in a sorted order produces folds that are each a contiguous block &mdash; occasionally a disaster nobody notices.

`TimeSeriesSplit` trains on the past and tests on what follows, never the reverse, with a training set that grows each time. It is the only correct choice for ordered data.

`GroupKFold` and `StratifiedGroupKFold` take a `groups` array and keep every row of a group on one side. Use them whenever several rows describe the same patient, customer, document or device &mdash; otherwise the model recognises the entity rather than learning the pattern, and the score is inflated by an amount nothing reveals.

`ShuffleSplit` draws random train/test pairs without the every-row-tested-once guarantee, which is useful when you want many estimates from a large dataset cheaply.

## What it costs, and when that matters

Cross-validation fits the model `k` times, so it costs roughly `k` times a single fit. For a logistic regression on a few thousand rows that is imperceptible. For a large ensemble on a large dataset it can turn a two-minute experiment into twenty.

Three ways to keep it affordable. `n_jobs=-1` runs the folds in parallel across cores, and since the folds are independent this is close to free speed on any machine with more than one. Fewer folds &mdash; three rather than ten &mdash; when you are exploring rather than reporting. And a subsample of the data while you are iterating, with the full run reserved for the result you intend to quote.

The mistake worth avoiding is skipping cross-validation because it is slow and going back to a single split. A single split is not faster in any way that matters; it is the same fit once, and it buys a number you cannot calibrate. If the budget is genuinely tight, three folds on the full data beats one split every time.

Note also that `cross_validate` reports `fit_time` and `score_time` per fold, which is the cheapest way to find out where the time is actually going before optimising anything.

## Reading the training scores

`return_train_score=True` adds a column that is worth the extra computation, because the gap between train and test is the clearest diagnostic in the whole library.

**Train high, test high, small gap.** The model has learned something that generalises. Nothing to fix.

**Train very high, test much lower.** Overfitting. The model has memorised patterns specific to the training rows. The response is more regularisation, a simpler model, or more data.

**Train low, test low, small gap.** Underfitting. The model cannot capture the structure even on data it has seen. The response is the opposite: a more flexible model, better features, less regularisation.

**Train lower than test.** Unusual and worth investigating rather than celebrating. It happens legitimately when regularisation or dropout is active during training but not scoring, and illegitimately when the folds are not comparable.

The two failure modes need opposite treatments, which is why guessing between them wastes so much time. One extra argument tells you which one you have.

<strong>Does KFold shuffle by default?</strong> No. Data arriving sorted produces folds that are each a contiguous block, which can be a silent disaster. Pass a splitter object with `shuffle=True` when the order might mean something.

<strong>Can I cross-validate a pipeline?</strong> Yes, and you should. A pipeline is a single estimator to `cross_val_score`, which is exactly what keeps its transformers inside the folds.

<strong>Why is my cross-validated score lower than my test score?</strong> Usually because each fold trains on less data than a single 80/20 split does, so the estimate is slightly pessimistic. A large gap suggests the split was lucky.

## Things to try

1. <strong>Run the second editor.</strong> Six seeds, six answers. That spread is the reason the rest of the page exists.
2. <strong>Look at the spread.</strong> In the first editor, print `scores.max() - scores.min()` and compare it against the difference between two models you are considering.
3. <strong>Run the leakage demo.</strong> The data is random. Sit with the fact that the wrong version reports 0.825.
4. <strong>Watch overfitting appear.</strong> In the fourth editor, swap the pipeline for `DecisionTreeClassifier()` and compare the train and test columns.

## Where this leaves you

`cross_val_score` for a quick estimate with its spread, `cross_validate` when you want several metrics or the training scores, a `Pipeline` around everything that learns, and a splitter object whenever the data has time or groups in it. The mean is the headline; the spread is what tells you whether to believe it.
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
intro: A model can be 99% accurate and completely useless. Which metric you report is a statement about which mistakes you are willing to make.

## Why accuracy misleads

Accuracy is the proportion of predictions that were correct, and it is the default that `score()` returns. On balanced data it is a reasonable summary. On imbalanced data it is close to worthless.

The editor above makes the case in five lines. With 99 negatives for every positive, a `DummyClassifier` that always predicts the majority scores **0.9867** and never predicts a single positive. It has learned nothing, it would be useless for any purpose, and it beats plenty of real models on the metric.

That situation is not exotic. Fraud, disease screening, equipment failure, click-through, churn, defect detection &mdash; the interesting class is rare in nearly every problem worth solving, and rarity is precisely what breaks accuracy. The rarer the thing you care about, the higher the score for ignoring it.

So the first thing to do with any classification problem is count the classes, and the second is fit a dummy. If the dummy's score is close to the model's, the model has added nothing regardless of how high the number looks.

## Precision and recall

Both are fractions of the same numerator &mdash; the true positives, the cases you flagged that really were positive &mdash; and they differ in what they divide by.

**Precision** divides by everything you flagged. It answers: *when this model says yes, how often is it right?* Low precision means false alarms.

**Recall** divides by everything that was actually positive. It answers: *of the cases that were really there, how many did we catch?* Low recall means misses.

The two names are unhelpful and the questions are not. It is worth reading them as those two sentences until the definitions stop needing to be looked up.

Which one matters is decided entirely by the cost of each kind of mistake, and the costs are usually wildly different. A cancer screen that misses cases is far worse than one that produces false alarms sent for a second test, so recall dominates. A spam filter that deletes real mail is far worse than one that lets some spam through, so precision dominates. An email flagged wrongly is an annoyance; a tumour missed is a catastrophe. No metric knows that, and no default can.

## They trade against each other

You can always have more of one by accepting less of the other, and the third editor shows the extremes on identical data: a model flagging 3 cases has precision 1.000 and recall 0.300; one flagging 40 has precision 0.250 and recall 1.000.

Neither is better. They are different operating points on the same underlying model, and choosing between them is the decision the metric exists to inform.

That is why quoting one alone is misleading. A claim of "95% precision" says nothing without the recall beside it &mdash; a model that flags one obvious case and nothing else achieves it trivially. The pair together describes the behaviour; either alone can be manufactured.

**F1** collapses the pair into one number by taking their harmonic mean, which is deliberately unforgiving: unlike an ordinary average, it stays low if either input is low. F1 of a model with precision 1.0 and recall 0.1 is 0.18, not 0.55. That property is what makes it useful as a single summary when you need to rank models, and it is still a summary &mdash; two models with the same F1 can behave very differently.

## Print the report

`classification_report` gives precision, recall, F1 and support &mdash; the number of true instances &mdash; for every class, plus the averages. It is one line and it should be the default thing you print after fitting a classifier.

The per-class rows are the point. An aggregate can look healthy while one class is being ignored completely, and the row for that class shows it immediately: precision and recall both zero, with a support telling you how many cases that represents.

`support` deserves attention on its own. A class with 4 examples in the test set produces metrics that move in steps of 25%, so a difference between two models on that class is noise. Reading the support column before believing a per-class number saves a lot of misplaced confidence.

## Averaging across several classes

With more than two classes, the per-class numbers have to be combined somehow, and the choice changes the answer substantially.

**macro** averages the per-class scores, treating every class as equally important regardless of size. A class with 2 samples counts as much as one with 900.

**weighted** averages them in proportion to support, so large classes dominate.

**micro** pools all the predictions before computing, which for single-label classification makes it identical to accuracy.

The fifth editor shows how far apart they can be: macro 0.612, weighted 0.949, micro 0.960, on predictions where the rarest class is never once identified correctly. Only macro reflects that failure. Weighted and micro report the performance on the big classes and let the small one disappear.

The rule that follows: **use macro when the rare classes matter**, which is usually why they are interesting. Use weighted when you genuinely care about overall volume. Never report micro on imbalanced data and call it anything other than accuracy.

## balanced_accuracy, for a single honest number

`balanced_accuracy_score` averages the recall of each class. It is accuracy with the class-size distortion removed.

Its virtue is that the lazy model cannot game it: always predicting the majority gives recall 1.0 on that class and 0.0 on the other, averaging to exactly 0.5 &mdash; which is what "no skill" should look like. The editor above shows 0.99 against 0.5 for the same predictions.

It is the right default when you want one number for an imbalanced problem and do not want to think about precision and recall separately. It is still one number, and it still hides the trade-off, so it belongs alongside the report rather than instead of it.

## Choosing, in practice

A short procedure that covers most cases.

Count the classes first. If they are roughly balanced, accuracy is fine and the rest of this page is optional. If they are not, it is not.

Fit a `DummyClassifier` and record its score on whatever metric you plan to use. That is the floor, and a model that does not clear it convincingly has not earned anything.

Decide which mistake is worse in the actual application, and say why in a sentence. If missing a case is worse, lead with recall. If a false alarm is worse, lead with precision. If they are comparable, F1 or balanced accuracy.

Print `classification_report` regardless, and read the support column before trusting any per-class row.

And remember that all of these are computed from `predict`, which applied a 0.5 threshold to a probability. Moving that threshold moves precision and recall in opposite directions without refitting anything &mdash; which is the subject of the next module, and often the cheapest improvement available.

## Metrics that use the probability rather than the label

Everything above is computed from `predict`, which has already committed to a label. Two metrics use `predict_proba` instead, and they measure something different: how well the model *ranks* cases, independently of where the threshold sits.

**ROC AUC** is the probability that a randomly chosen positive is scored higher than a randomly chosen negative. 1.0 is perfect ranking, 0.5 is random. Its appeal is that it summarises every possible threshold at once, so it compares models without committing to an operating point. Its weakness is that it is computed across the whole range including thresholds nobody would use, and on heavily imbalanced data it stays flatteringly high &mdash; the enormous number of true negatives dominates the false positive rate.

**Average precision**, the area under the precision-recall curve, is the better choice when positives are rare. It ignores true negatives entirely, so it cannot be inflated by having a great many of them, and it moves when the model's behaviour on the class you care about changes.

The practical rule: report ROC AUC on roughly balanced problems, average precision on imbalanced ones, and neither as a substitute for the metric that reflects the actual decision. A high AUC means the ranking is good; it does not mean any particular threshold produces a useful precision and recall.

## Multi-label and multi-class are different problems

Two situations get confused because both involve more than two labels.

**Multi-class** means each sample belongs to exactly one of several classes &mdash; a flower is setosa or versicolor or virginica. Everything on this page applies, with the averaging choice being the only addition.

**Multi-label** means each sample can carry several labels at once &mdash; an article tagged both "politics" and "economics". Here `y` is a 2-D binary array rather than a 1-D vector, accuracy becomes exact-set-match and is brutally strict, and the averaging choices gain a fourth option, `samples`, which averages per row rather than per class.

Confusing the two produces shape errors rather than silent wrongness, which is fortunate. `MultiLabelBinarizer` is the tool for getting from a list of tag lists to the array the estimators want.

<strong>What is zero_division for?</strong> Precision is undefined when nothing was flagged, and recall when nothing was positive. The argument says what to return instead of raising - `0` is the usual choice, and seeing it fire tells you a class was never predicted.

<strong>Which metric should I optimise in a search?</strong> The one that reflects the decision. Passing `scoring="f1"` or `scoring="balanced_accuracy"` to a grid search changes which model wins, and leaving it at the default optimises accuracy whether or not that is what you want.

<strong>Can I weight the classes instead of changing the metric?</strong> Yes, and often you should do both. `class_weight="balanced"` changes what the model optimises during fitting; the metric changes what you measure afterwards.

## Reporting a number somebody will act on

The metric that ends up in a slide is rarely the one that should drive the decision, and closing that gap is worth a paragraph.

Precision and recall are ratios, and ratios hide volume. "Recall of 0.6" sounds moderate; "we miss four hundred cases a month" is the same fact and provokes a different conversation. Multiplying the rates back into counts &mdash; how many caught, how many missed, how many false alarms per week &mdash; turns an abstract score into something a person with domain knowledge can judge.

That translation also exposes whether the model is worth deploying at all. A fraud model with precision 0.3 sounds poor until you work out that each investigation costs fifty pounds and each caught case saves two thousand, at which point flagging three cases to catch one is obviously correct. The reverse happens too: an impressive-looking model whose false alarms consume more analyst time than the catches save.

The habit worth forming is to state, alongside every metric, what it means in units of the thing the organisation cares about. It takes one extra line and it is the line that decides whether anyone uses the model.

## Things to try

1. <strong>Run the first editor.</strong> 0.9867, and not one positive predicted. Sit with the number before reading on.
2. <strong>Change the balance.</strong> Set `weights=[0.5]` and re-run. Accuracy stops flattering the dummy immediately.
3. <strong>Read the support column.</strong> In the fourth editor, note how few positives the metrics for class 1 are computed from.
4. <strong>Break the macro average.</strong> In the fifth editor, make the model get the rare class right once and watch macro move far more than weighted.

## Where this leaves you

Accuracy for balanced problems only. Precision when false alarms cost, recall when misses cost, F1 or balanced accuracy when you need one number, and `classification_report` printed every time so an ignored class cannot hide behind an average.
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
intro: Every classification metric is a fraction computed from four numbers. Looking at the four directly tells you things no fraction can.

## What the table is

The confusion matrix cross-tabulates what was true against what was predicted. Rows are the actual classes, columns are the predicted ones, and each cell counts how many samples fell into that combination.

The diagonal is where the two agree &mdash; correct predictions. Everything off the diagonal is a mistake, and *which* off-diagonal cell it lands in tells you what kind.

For two classes the convention is worth memorising because `ravel()` returns it in this order: **true negative, false positive, false negative, true positive**. Reading it as `tn, fp, fn, tp = cm.ravel()` is the standard line.

The naming is easier than it looks once you read it as two words rather than one phrase. The second word is what the model *said*. The first word is whether it was *right*. So a false negative is a case the model called negative and was wrong about &mdash; a miss.

## Why it beats any single number

A metric compresses the table into one figure, and compression loses exactly the information you need to improve the model.

Accuracy of 0.94 could be 88 true negatives and 6 true positives with 4 misses and 2 false alarms &mdash; or it could be 94 true negatives, no true positives, and 6 misses, with the model never predicting the positive class at all. Those are completely different situations and accuracy reports them identically.

The matrix distinguishes them immediately, and it does so before you have decided which metric matters. That is the practical argument for printing it first: it tells you what the model is doing, and only then do you choose the number that summarises it.

It also tells you which direction to push. Too many false positives and too few false negatives means the threshold is too low. The reverse means it is too high. Both visible at a glance, neither visible in an accuracy score.

## The multi-class version, and what it reveals

With `k` classes the matrix is `k` by `k`, and the off-diagonal structure carries information that no averaged metric preserves.

The editor above fits iris on sepal measurements only &mdash; deliberately insufficient &mdash; and the result is instructive. Setosa is classified perfectly, never confused with anything. Versicolor and virginica are confused with each other repeatedly, and **not symmetrically**: versicolor is called virginica 8 times, while virginica is called versicolor 5 times.

That asymmetry is a real finding and it is invisible in an F1 score. It tells you the boundary between those two classes is drawn slightly off centre, and it tells you setosa is a solved problem while the other two need better features. A macro F1 of 0.78 tells you none of that.

The general habit: on a multi-class problem, find the largest off-diagonal cell. It is almost always one specific pair being confused, and it is almost always the most productive thing to work on.

## Normalising, and which way

Raw counts are dominated by class size. On a 99-to-1 problem the true-negative cell is enormous and the rest are visually invisible, which makes the table hard to read even though the numbers are correct.

`normalize="true"` divides each row by its total, giving the proportion of each actual class that went to each prediction. The diagonal then reads as per-class recall, and a row that is mostly off the diagonal shows a class the model handles badly regardless of how few samples it has.

`normalize="pred"` divides by column instead, giving the proportion of each prediction that was correct &mdash; the diagonal reads as per-class precision.

`normalize="all"` divides by the grand total, which is occasionally useful and usually the least informative of the three.

Row normalisation is the default worth reaching for. It answers "what does the model do with each kind of case", which is the question that survives changes in class balance.

## The labels argument

`confusion_matrix` infers the classes from the data it is given, sorted. Two consequences bite.

A class present in `y_true` but never predicted still appears &mdash; but a class absent from both, perhaps because the test split happened to contain none of it, disappears entirely, and the matrix silently becomes smaller than expected. Code that indexes into it by class position then reads the wrong cell.

And the order is sorted, which for string labels is alphabetical: `["cat", "dog", "fish"]`. Assuming a different order and labelling the axes accordingly produces a table that is confidently wrong.

Passing `labels=` fixes both. It guarantees the size, guarantees the order, and makes the code independent of which classes happened to turn up in a particular split. It is worth passing habitually rather than when a problem appears.

## From the table to the rows

The matrix says how many mistakes of each kind. The next question is always why, and answering it means looking at the samples themselves.

Selecting the misclassified rows takes one line &mdash; `np.flatnonzero(pred != y_true)` &mdash; and reading a handful of them is consistently the most informative ten minutes available. Usually they have something in common: values near a boundary, a category the training data barely covered, missing fields that were imputed, or labels that are simply wrong in the source data.

Each of those has a different response, and none of them is "try a different model". Mislabelled ground truth in particular is far more common than people expect, and no amount of tuning fixes it &mdash; the model is being penalised for being right.

The editor above does exactly this for the iris confusion, and the misclassified rows are all sepal measurements in the overlapping middle of the two species. That is not a model problem; it is the honest answer that these two features do not separate those two classes, and the fix is petal measurements rather than a fancier classifier.

## The other convention, and why it causes trouble

scikit-learn puts truth on the rows and predictions on the columns. A good deal of the statistics literature does the opposite, and some textbooks put the positive class first rather than second.

That means a matrix copied from a paper, a blog post or a lecture slide may be transposed relative to what `confusion_matrix` produces, and a transposed matrix swaps precision and recall without changing anything visible. The numbers all look plausible; they are simply answering the other question.

Two habits prevent it. Print the matrix with labelled axes rather than as a bare array, which takes three lines and removes the ambiguity permanently. And sanity-check against a metric you trust: compute recall with `recall_score` and confirm it matches the diagonal cell divided by its row total. If it matches the column total instead, the orientation is not what you assumed.

The same caution applies to the binary case, where the positive class is whichever label sorts second &mdash; `1` before `0` is not the order, `0` then `1` is. With string labels, `"no"` sorts before `"yes"`, which usually happens to be right, and with `"negative"` and `"positive"` it also happens to be right. With `"benign"` and `"malignant"` it is right for the wrong reason, and with labels where it is not, `pos_label=` is the argument that says so explicitly.

## What it cannot tell you

Two limits worth stating, because the matrix is otherwise so useful that it gets asked questions it cannot answer.

It says nothing about confidence. Every cell counts hard predictions, so a case predicted positive at 0.51 and one at 0.99 are the same entry. A model can have an excellent matrix and terrible probabilities, or the reverse, and only the probability-based metrics distinguish them.

And it describes one threshold. Change the threshold and every cell moves &mdash; that is the whole mechanism of the precision-recall trade. So a confusion matrix is a snapshot of one operating point, not a description of the model, and comparing two models by their matrices means comparing them at whatever threshold each happened to use.

<strong>Is there a plotting version?</strong> `ConfusionMatrixDisplay.from_estimator(model, X, y)` draws it with matplotlib, which is worth using once the matrix is bigger than about four by four and the numbers stop being readable as text.

<strong>Which class is "positive" in a binary problem?</strong> Whichever label sorts second, so `0` then `1` puts `1` positive. Pass `pos_label=` when the sorted order is not what you mean.

<strong>Can I get one matrix per class for a multi-label problem?</strong> Yes - `multilabel_confusion_matrix` returns a stack of 2x2 tables, one per label, which is the right shape when a sample can carry several labels at once.

## Putting a cost on each cell

The matrix becomes a decision tool rather than a diagnostic the moment you attach a number to each kind of mistake.

The four cells rarely cost the same. A false negative on a fraud check is the value of the fraud; a false positive is a few minutes of an analyst's time. A false negative on a medical screen is a missed diagnosis; a false positive is a second test. A false negative on a spam filter is one unwanted email; a false positive is a lost message the recipient never knew about.

Once those numbers exist, the expected cost of a model is the sum of each cell multiplied by its price, and comparing two models becomes arithmetic rather than argument. It also settles the threshold question directly: sweep the threshold, compute the total cost at each one, and pick the minimum. That is a better procedure than choosing a threshold to hit a round-numbered precision, and it takes about the same effort.

The exercise is worth doing even when the costs are rough. Estimating that a miss is roughly ten times worse than a false alarm is enough to rule out most of the range, and it forces the conversation with whoever owns the problem &mdash; who usually has a much clearer view of the relative costs than the person building the model, and who is rarely asked.

Where it goes wrong is treating the estimated costs as precise. They are not, and a threshold tuned to the third decimal place of an invented cost ratio is false precision. The useful output is a region rather than a point: anywhere in this range is sensible, and outside it is not.

## Things to try

1. <strong>Unpack the four counts.</strong> In the first editor, compute precision and recall yourself from `tn, fp, fn, tp` before looking at what the library returns.
2. <strong>Find the worst pair.</strong> In the third editor, locate the largest off-diagonal cell and note that it is not mirrored.
3. <strong>Switch the normalisation.</strong> In the fourth editor, compare `normalize="true"` with `normalize="pred"` and work out which diagonal is recall and which is precision.
4. <strong>Read the mistakes.</strong> In the last editor, raise the slice to see all thirteen and look for what they have in common.

## Where this leaves you

Four counts for two classes, `k` by `k` for more, rows as truth and columns as prediction. Print it before choosing a metric, normalise by row when the classes are uneven, pass `labels=` so the shape is guaranteed, and read the rows behind the largest off-diagonal cell before changing anything.
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
intro: Half the models in the library are seriously damaged by unscaled features and half are completely indifferent. Knowing which is which saves both wasted work and silently bad results.

## What scaling does

`StandardScaler` learns two numbers per column &mdash; the mean and the standard deviation &mdash; and transforms by subtracting the first and dividing by the second. The result has mean 0 and standard deviation 1 in every column.

That is the entire operation. The shape of the distribution is unchanged: a skewed column stays skewed, outliers stay outliers, and the relative positions of every value are preserved exactly. Scaling moves and stretches; it does not reshape.

The learned numbers live in `mean_` and `scale_`, which is worth knowing because those two arrays are the entire fitted state and the thing that must not be learned from the test data.

## Why some models need it

Two families of algorithm are affected, for two different reasons.

**Anything that measures distance.** k-nearest neighbours, SVMs with an RBF kernel, k-means, PCA. These compute how far apart two samples are, usually by summing squared differences across features. A column measured in thousands contributes thousands of times more to that sum than a column measured in single digits, so the distance is effectively decided by whichever feature happens to have the largest units. The model is not weighing the features by importance; it is weighing them by unit.

The editor above shows the cost: k-NN on the wine dataset scores 0.69 unscaled and 0.95 scaled. That is not a tuning improvement, it is the difference between a model that works and one that does not, and it comes from one column being measured in hundreds while others are measured in fractions.

**Anything that penalises coefficient size.** Ridge, Lasso, ElasticNet, and `LogisticRegression`, which is regularised by default. The penalty is on the magnitude of the coefficients, and a coefficient's magnitude depends on its feature's units. Without scaling, the penalty falls unevenly across features for reasons that have nothing to do with the data.

There is also a practical third reason: gradient-based solvers converge faster and more reliably on scaled features, which is why unscaled logistic regression produces `ConvergenceWarning`.

## Why some models do not

Tree-based models &mdash; decision trees, random forests, gradient boosting &mdash; are completely unaffected, and the reason is structural rather than approximate.

A tree splits on one feature at a time, asking whether a value is above or below a threshold. Rescaling a column monotonically moves the threshold by the same transformation and leaves the ordering of every sample identical, so exactly the same split is chosen. The tree that results is the same tree.

The editor above measures it: the random forest changes by `+0.0000`. Not "a little"; not at all.

This matters practically because scaling a tree model is harmless but pointless, and adding a scaler to a pipeline that ends in a forest is a step that costs time and clarity for no benefit. It matters more because people who have learned "always scale" sometimes conclude that trees must therefore be doing something odd, when in fact this is one of the reasons trees are so convenient on messy tabular data: they need no preparation at all.

## Choosing between the scalers

`StandardScaler` is the default and the right answer most of the time. It assumes nothing about the range and handles roughly symmetric data well.

`MinMaxScaler` maps each column onto a fixed range, usually 0 to 1. It is the choice when an algorithm requires bounded input, and its weakness is severe: a single outlier defines the range and compresses everything else against the opposite end. The editor above shows four ordinary values landing in the first hundredth of the range because one value is 100.

`RobustScaler` centres on the median and divides by the interquartile range. Because both statistics ignore the tails, extreme values do not distort the transformation of the ordinary ones &mdash; in the same demonstration, the four normal values keep a sensible spread and the outlier simply sits far away. It is the right default when the data has outliers you do not want to remove.

`MaxAbsScaler` divides by the largest absolute value and preserves zeros, which makes it the one to use on sparse data where centring would destroy the sparsity.

`Normalizer` is the odd one out and a frequent source of confusion: it scales each **row** to unit length rather than each column. It is for making samples comparable in direction rather than magnitude &mdash; text vectors, mostly &mdash; and is not a substitute for the column scalers.

## The rule that makes it honest

The scaler must be fitted on the training data only, and then used to transform both halves.

The reason is the same as everywhere else in this track: `mean_` and `scale_` are learned from data, so a scaler fitted on everything has seen the test set, and the score afterwards is not a score on unseen data.

The consequence surprises people the first time. After scaling correctly, the **test set is not centred on zero** &mdash; its mean is whatever it happens to be relative to the training distribution. The editor above shows 0.0184 rather than 0. That is correct and it is the whole point: the test data is being put through exactly the transformation that new data would go through in production, where you do not get to recompute the mean using the future.

A test set that comes out perfectly centred is evidence that the scaler was fitted on it, which means the evaluation is compromised.

The same logic extends to deployment. The scaler is part of the model and has to be saved with it. A model deployed without its scaler, receiving raw features, will produce confident nonsense &mdash; which is one more argument for the pipeline, since saving the pipeline saves both.

## Just use a pipeline

Every rule above is enforced automatically by putting the scaler in a `Pipeline`.

A pipeline is a single estimator. Its `fit` runs `fit_transform` on each transformer and then `fit` on the final model; its `predict` runs `transform` and then `predict`. So inside a cross-validation loop, the scaler is refitted on each training fold and the held-out fold is only ever transformed &mdash; which is exactly the correct behaviour, achieved without you having to remember it.

`make_pipeline(StandardScaler(), LogisticRegression())` is two words longer than fitting the scaler by hand and removes an entire category of mistake. There is essentially no situation in which scaling outside a pipeline is preferable, and the habit is worth forming before the mistakes are.

## Scaling is not the only transformation a column might want

Standardising fixes the *scale* of a feature and leaves its *shape* alone. Sometimes the shape is the problem.

A heavily skewed column &mdash; incomes, populations, response times, anything where a few values are orders of magnitude above the rest &mdash; stays heavily skewed after standardising. The mean and standard deviation are themselves distorted by the tail, so most of the data ends up squeezed just below zero with a few enormous values above it, which is exactly the situation that harmed the distance-based models in the first place.

Three responses. A **log transform**, via `FunctionTransformer(np.log1p)`, compresses the tail and often turns a multiplicative relationship into an additive one that a linear model can fit. `log1p` rather than `log` because it handles zeros without producing negative infinity.

`PowerTransformer` finds a transformation that makes the column as close to normal as it can, and standardises as it goes. It handles the choice for you and is the reasonable default when you know a column is skewed and do not want to think about which transformation.

`QuantileTransformer` maps the column onto a uniform or normal distribution by rank. It is the most aggressive of the three: it will normalise anything, at the cost of discarding the actual spacing between values and of behaving unpredictably on values outside the training range.

All three are transformers with the usual `fit`/`transform`, so they go in a pipeline in the same place a scaler would, and they are subject to exactly the same training-data-only rule.

## The order of the steps

When several transformations apply to the same column, the order is not arbitrary.

Imputation comes before scaling, because a scaler cannot compute a mean over missing values &mdash; it raises. Encoding comes before scaling for the same reason, since a scaler cannot subtract a mean from a string.

Skew correction comes before standardising, since the point is to fix the shape and then fix the location and spread of the fixed shape.

Feature selection is usually last among the transformers and before the model, so that the selection sees the features in the form the model will.

A `Pipeline` executes its steps in the order given, so writing them in the wrong order produces either an error or a silently worse model. The sequence that covers most cases is: impute, encode, transform skew, scale, select, fit.

<strong>Should I scale the target as well?</strong> Rarely for regression - it changes the units your errors are reported in. When it genuinely helps, `TransformedTargetRegressor` does it and inverts the transformation on `predict`, so the predictions come back in the original units.

<strong>Does scaling help accuracy on trees, ever?</strong> No. Exactly zero, which the last editor demonstrates. It is harmless and pointless.

<strong>What about one-hot columns - do those get scaled?</strong> They are already 0 and 1, so standardising them mostly adds noise to the interpretation. It is common to scale only the numeric columns, which is what a `ColumnTransformer` is for.

## Categories of model, and what each one wants

A summary worth keeping, because "does this need scaling" comes up for every new estimator.

**Needs it, badly.** k-nearest neighbours, k-means, SVM with any kernel, PCA and anything built on it, and neural networks. All of these either measure distance or descend a gradient, and both are dominated by whichever feature has the largest units.

**Needs it, for the penalty.** Ridge, Lasso, ElasticNet, and `LogisticRegression` with its default L2. The fit itself would be unaffected, but the regularisation penalises coefficient magnitude, and magnitude depends on units.

**Does not need it, and gains nothing.** Decision trees, random forests, extra trees, gradient boosting in all its varieties, and naive Bayes. These either split one column at a time or treat the columns independently.

**Does not need it, but converges faster with it.** Plain `LinearRegression` has a closed-form solution and is genuinely indifferent; the iterative solvers used for very large problems are not.

The rule that covers the whole table: if the algorithm ever adds two different features together, compares them, or measures a distance across them, it needs them on a common scale. If it only ever looks at one feature at a time, it does not.

## Things to try

1. <strong>Run the second editor.</strong> 0.69 against 0.95, from one line. That is the argument in a single number.
2. <strong>Watch a tree ignore it.</strong> The last editor reports a change of exactly zero for the forest. Try `MinMaxScaler` instead and confirm it is still zero.
3. <strong>Break the range.</strong> In the third editor, change the outlier to 10000 and see how much further MinMax compresses the ordinary values.
4. <strong>Cheat deliberately.</strong> In the fourth editor, fit the scaler on all of `X` and note that the test mean becomes 0 - the signature of a compromised evaluation.

## Where this leaves you

Scale for distance-based and regularised models, do not bother for trees, prefer `StandardScaler` unless outliers argue for `RobustScaler`, and fit it inside a pipeline so that the training-data-only rule holds without anyone having to remember it.
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
intro: Every estimator in scikit-learn takes numbers. Turning "london" into a number is easy; doing it without inventing a fact that is not in the data takes one decision.

## Why it cannot be skipped

scikit-learn's estimators operate on numeric arrays. A column of strings raises rather than being converted automatically, and the error &mdash; `could not convert string to float` &mdash; is one of the first anyone meets on real data.

The conversion is not mechanical, because there is more than one way to do it and they encode different claims about the data. Getting it wrong does not raise; it produces a model that has been told something false.

## The mistake to avoid

The obvious approach is to number the categories: london 0, paris 1, berlin 2. It is one line and it is wrong for most categorical columns.

Numbering asserts an **order** and a **spacing**. It says berlin is greater than paris, that paris sits exactly between london and berlin, and that the distance from london to berlin is twice the distance from london to paris. None of that is true of cities, and a model that computes with those numbers will use every one of those false relationships.

For a linear model the damage is direct: a single coefficient is fitted for the column, so the model can only express "more city is more target", which is meaningless. For a distance-based model, berlin and london are computed as far apart while london and paris are close. For a tree the damage is milder &mdash; a tree can split the numbers into groups and partially recover &mdash; but it still has to spend splits undoing an ordering that was invented.

## One-hot encoding

The safe answer is one column per category, each holding 1 when the row is that category and 0 otherwise.

No ordering is implied, because no two categories share a column. Each gets its own coefficient in a linear model, so the model can learn that paris raises the target and berlin lowers it, which numbering could never express.

`OneHotEncoder` learns the categories during `fit` and stores them in `categories_`, sorted. `get_feature_names_out()` returns the generated names &mdash; `city_london`, `city_paris` &mdash; which is what keeps coefficients and feature importances readable after the transformation.

By default it returns a sparse matrix, because with many categories almost every entry is zero. `sparse_output=False` gives a dense array, which is convenient for looking at and a bad idea when the number of categories is large.

## The unseen category

The most important argument on the encoder is `handle_unknown`, and the default is the strict one.

A category present at prediction time but absent during training raises `ValueError` by default. That is the right behaviour while you are developing &mdash; it tells you the data has changed &mdash; and usually the wrong behaviour in production, where a new city appearing should not take the service down.

`handle_unknown="ignore"` encodes the unknown value as all zeros: not any of the known categories, which is an honest representation of "something I have not seen". The model then predicts from the remaining features.

This matters inside cross-validation too. Each fold refits the encoder on its own training part, so a category appearing only in the held-out fold is unknown to that fold's encoder. Without `handle_unknown="ignore"`, cross-validation on a dataset with rare categories crashes on whichever fold happens to isolate one.

`min_frequency` and `max_categories`, added more recently, are the built-in answer to the same problem from the other end: they fold rare categories into a single "infrequent" column during fitting, so the rare values are handled by design rather than by exception.

## When ordering is real

Some categories genuinely are ordered. Small, medium, large. Bronze, silver, gold. Disagree, neutral, agree. Here an integer encoding is not a lie, and it is better than one-hot because it lets the model use the ordering with a single coefficient instead of learning three independent ones.

`OrdinalEncoder` does it &mdash; and left to itself it sorts alphabetically, which is almost never the order you meant. The editor above shows the damage: with small, medium and large, alphabetical order produces large 0, medium 1, small 2, so the encoding says small is the biggest.

`categories=[["small", "medium", "large"]]` states the order explicitly, and passing it is not optional. The list is nested because the encoder handles several columns at once, one list per column.

The test for whether a column is ordinal: is there a defensible answer to "which is bigger", and is the gap between consecutive values roughly comparable? Sizes pass the first and often fail the second, which is why ordinal encoding of survey scales is common and mildly wrong.

## drop, and the collinearity question

With `k` categories, one-hot produces `k` columns of which any one is determined by the others &mdash; if it is not london and not paris, it is berlin. That redundancy is called collinearity.

`drop="first"` removes one column per feature. For a plain linear regression this matters: with an intercept, perfectly collinear columns make the solution non-unique and the individual coefficients unstable. For anything regularised &mdash; Ridge, Lasso, `LogisticRegression` with its default penalty &mdash; it does not, because the penalty resolves the ambiguity, and dropping a column makes the remaining coefficients harder to interpret since they become relative to the dropped baseline.

`drop="if_binary"` is the sensible middle: it drops the redundant column only for two-category features, where two columns are obviously one too many, and leaves multi-category features alone.

For trees, dropping is actively unhelpful &mdash; it removes a column the tree might have split on and gains nothing.

## High cardinality

One-hot encoding a column with thousands of distinct values produces thousands of columns, almost all zero, and the editor above shows 1639 distinct user ids becoming 1639 columns.

Three problems follow. The matrix becomes enormous and mostly empty. Most columns are 1 for only a handful of rows, so any coefficient fitted to them is fitted to almost no data. And the model can memorise individual ids, which looks like skill on the training data and is worthless on anyone new.

Three responses, in increasing order of effort. **Group the rare values** into an "other" category, which `min_frequency` does for you. **Encode something about the category rather than its identity** &mdash; for a postcode, the region; for a product, its price band. Or **target encoding**, replacing each category with the mean target for that category, which is compact and powerfully prone to leakage: computed on the whole dataset it tells the model the answer, so it must be computed inside the folds, which is what `TargetEncoder` handles.

The question worth asking first is whether the column belongs in the model at all. A user id usually carries no generalisable information; what you want is what the user *did*.

## LabelEncoder is not for this

`LabelEncoder` appears in a great deal of example code applied to feature columns, and it is documented for encoding the **target**.

It accepts only 1-D input, so using it on features means looping over columns and applying it one at a time. That works, produces an ordinal encoding with all the problems above, and &mdash; the real objection &mdash; it has no `handle_unknown`, so a new category at prediction time raises with no option to do otherwise.

Use `OrdinalEncoder` for ordered features, `OneHotEncoder` for unordered ones, and `LabelEncoder` only when converting string class labels into integers for `y`, which most estimators do not even require.

## Categories that arrive as numbers

The hardest categorical columns to spot are the ones already stored as integers, because nothing raises and nothing looks wrong.

A postcode district, a product code, a department id, a day-of-week stored as 0 to 6, a survey answer coded 1 to 5. Each is a category wearing a number, and a model handed it raw will treat department 7 as greater than department 3 and exactly twice department 3.5.

Nothing in the data announces this. The column is numeric, the estimator accepts it, the fit succeeds, and the model quietly uses an ordering that means nothing. It is the mirror image of the ordinal mistake: there, an order was invented where none existed; here, an order that happens to exist in the encoding is mistaken for one that exists in the world.

The check is to ask what the arithmetic would mean. If the average of two values is meaningless &mdash; the average of department 2 and department 8 &mdash; the column is categorical regardless of its dtype. If it is meaningful, as with an age or a price, it is genuinely numeric.

Day-of-week is the interesting middle case. It has an order, the gaps are equal, and it wraps around: Sunday is adjacent to Monday, which no integer encoding captures. The usual fix is a pair of features, the sine and cosine of the angle around the week, which makes the wrap-around explicit and is the standard trick for any cyclical quantity &mdash; hours, months, compass bearings.

## Reading the model afterwards

One-hot encoding multiplies the columns, and a fitted model reports one number per column. Keeping the two aligned is what makes the result readable.

`get_feature_names_out()` on the encoder returns the generated names in order, and on a `Pipeline` or `ColumnTransformer` it returns the names for everything the whole chain produced. Zipping that against `coef_` or `feature_importances_` gives a labelled result rather than an array of numbers whose positions you have to reconstruct.

Two things to remember when reading them. The importance of a category is spread across its columns, so a feature with twenty categories has its influence divided twenty ways and will look weaker than a single numeric column carrying the same information &mdash; which is a known bias in tree-based feature importances, not a fact about the data. And with `drop="first"`, every remaining coefficient is relative to the dropped category, so a positive coefficient means "higher than the baseline", not "high".

<strong>Do trees need one-hot encoding?</strong> scikit-learn's do, because they cannot take strings. `HistGradientBoostingClassifier` accepts declared categorical features natively, which is both faster and better than one-hot for high-cardinality columns.

<strong>Should I one-hot encode before or after splitting?</strong> After, and inside a pipeline - otherwise the encoder learns the category list from the test rows too.

<strong>What about missing values in a categorical column?</strong> `OneHotEncoder` treats `NaN` as its own category by default, which is often the right behaviour: "not stated" is frequently informative rather than merely absent.

## Things to try

1. <strong>Read the alphabetical disaster.</strong> The third editor encodes small as 2 and large as 0. Look at the numbers before reading the fix.
2. <strong>Meet the unknown category.</strong> In the second editor, remove `handle_unknown="ignore"` from the safe encoder and watch it raise on tokyo.
3. <strong>Explode a column.</strong> In the fifth editor, raise the number of distinct users and watch the column count follow it exactly.
4. <strong>Group the rare ones.</strong> Add `min_frequency=50` to that encoder and see how many columns survive.

## Where this leaves you

One-hot for unordered categories with `handle_unknown="ignore"`, ordinal with an explicit `categories=` when the order is real, `drop="if_binary"` as a reasonable default, and a plan for any column with more than a few dozen distinct values before it becomes a few dozen columns of nearly nothing.
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
intro: A pipeline is not a convenience. It is the mechanism that makes every score in this track honest, and using one turns a rule you have to remember into a property of the code.

## What it is

A `Pipeline` chains transformers together and ends with an estimator, and the result behaves as a single estimator.

That last sentence is the important one. A pipeline has `fit`, `predict` and `score`, so anywhere a model can go &mdash; `cross_val_score`, `GridSearchCV`, a pickle file, a comparison loop &mdash; a whole pipeline can go instead, with no changes to the surrounding code.

What it does internally is straightforward. `fit` calls `fit_transform` on each step in turn, passing the output of one to the next, and `fit` on the final estimator. `predict` calls only `transform` on each step, then `predict` on the last.

## The asymmetry is the point

Look again at those two sentences: `fit` **fits** the transformers; `predict` only **transforms**.

That asymmetry is what makes a pipeline more than plumbing. Inside a cross-validation loop, `fit` is called on the training folds &mdash; so the scaler computes its mean there, the imputer its median, the encoder its category list. Then `predict` runs on the held-out fold, which is transformed using those numbers and never contributes to them.

Doing the same thing by hand means remembering, every time, to fit each transformer on the training part only, and to apply it to the test part without refitting. That is four or five opportunities per experiment to make a mistake that inflates the score and produces no error.

The cross-validation module measured what that mistake costs: feature selection applied outside the folds reported 0.825 accuracy on data that was pure noise. A pipeline makes that particular mistake impossible to write.

## Two constructors

`make_pipeline(StandardScaler(), LogisticRegression())` names the steps automatically, lowercasing the class names. It is shorter and right for quick work.

`Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression())])` lets you name them. The names matter once you are tuning, because they appear in every parameter key: `clf__C` is far more readable than `logisticregression__C`, and it does not change if you swap the classifier for a different one.

The rule of thumb: `make_pipeline` while exploring, `Pipeline` with short names once there is a search grid.

Every step except the last must be a transformer &mdash; it must have `transform`. The last can be anything, including another transformer if the pipeline's purpose is preprocessing rather than prediction.

## Getting at the fitted parts

A fitted pipeline still contains its fitted steps, and there are three ways in.

`pipe.named_steps["scale"]` uses the name. `pipe["scale"]` is the shorter form of the same thing. `pipe[0]` and `pipe[-1]` index by position, and `pipe[-1]` for the final estimator is the one you will write most.

This is how you read `coef_` off the model at the end, or check what the scaler learned, or pull `get_feature_names_out()` from an encoder in the middle. The pipeline hides nothing; it only changes how you reach it.

`pipe[:-1]` slices, returning a new pipeline of everything except the last step &mdash; occasionally useful for inspecting what the model actually receives.

## Tuning through a pipeline

Hyperparameters inside a pipeline are addressed as `stepname__parameter`, with **two** underscores.

`{"clf__C": [0.01, 0.1, 1]}` tunes `C` on the step named `clf`. Nesting goes deeper with more underscores &mdash; a parameter inside a step inside a column transformer is `preprocess__num__imputer__strategy` &mdash; which looks unwieldy and is entirely mechanical.

The consequence worth appreciating: a search can tune the **preprocessing** as well as the model. Whether to scale with the mean, which imputation strategy to use, how many PCA components to keep, and how the model is configured, all in one grid, all evaluated with the same honest cross-validation.

`"passthrough"` extends this to whole steps. Setting a step to that string makes it a no-op, so `{"pca": ["passthrough", PCA(5), PCA(10)]}` treats the existence of the PCA step as itself a hyperparameter. The same trick lets a search choose between two entirely different models in one grid.

## Deployment is where it pays off

A model without its preprocessing is not a model.

Saving only the estimator and applying scaling by hand at prediction time means reimplementing the transformation somewhere else, with the numbers copied across, and keeping the two in step forever. Every one of those is a place for the training and serving paths to diverge &mdash; and when they do, nothing raises. The model receives features on a different scale from the ones it was fitted on and produces confident nonsense.

Pickling the pipeline saves the transformers and their learned parameters alongside the model, so the object that comes back does the whole job from raw features to prediction. The editor above round-trips one and confirms the predictions are identical.

Two cautions on pickles that apply to any scikit-learn object. They are not a secure format &mdash; unpickling untrusted data executes code &mdash; and they are not portable across versions, so a pipeline pickled with one scikit-learn and loaded with another may fail or, worse, behave differently. Recording the version alongside the file is the minimum, and `skops` is the alternative for anything that has to be shared.

## When not to reach for one

Pipelines handle a sequence of steps applied to all the columns. Two situations need something else.

**Different steps for different columns** &mdash; scaling the numeric ones and encoding the categorical ones &mdash; is what `ColumnTransformer` is for, and it slots into a pipeline as a single step.

**Anything that changes the number of rows.** Dropping outliers, resampling for imbalance, aggregating. Pipelines transform features and pass the target through untouched, so a step that removed rows would leave `X` and `y` out of step. The `imbalanced-learn` package provides its own pipeline for exactly this case, and row-level filtering otherwise belongs before the pipeline, applied to the training data only.

## Caching, when the fitting gets slow

A grid search over a pipeline refits every step for every combination, and most of that work is repeated. Tuning only the classifier means the scaler and the imputer are refitted identically for each candidate, which is wasted time on anything expensive.

`Pipeline(steps, memory="./cache")` caches the fitted transformers, keyed on the step and the data they were given. The first combination pays for the preprocessing; the rest reuse it. On a pipeline whose expensive part is the preprocessing &mdash; text vectorisation, a costly feature construction &mdash; this can be the difference between a search that finishes and one that does not.

Two caveats. The cache is on disk and is not cleaned up automatically, so a long-running project accumulates directories. And it only helps when the transformer's inputs are genuinely identical, so it does nothing for a grid that tunes an early step.

## Building your own step

A pipeline accepts anything with `fit` and `transform`, which includes classes you write.

For a stateless transformation &mdash; a log, a ratio between two columns, a date part &mdash; `FunctionTransformer(func)` wraps a plain function and needs nothing else. It is the shortest route into a pipeline and covers a surprising amount.

When the step needs to *learn* something, subclassing `BaseEstimator` and `TransformerMixin` gives you the rest of the interface for free: `fit` stores what it learned on `self` with a trailing underscore, `transform` applies it, and `TransformerMixin` supplies `fit_transform`. `get_params` and `set_params` arrive from `BaseEstimator`, which is what makes the custom step tunable by a search like any other.

The rule that keeps a custom step honest is the same as for the built-in ones: everything learned from data must be learned in `fit`, and `transform` must use only what `fit` stored. A transformer that computes a statistic inside `transform` recomputes it on the test fold, which is the leak the pipeline was supposed to prevent.

<strong>Can a pipeline end in a transformer?</strong> Yes. It then has `transform` rather than `predict`, which is useful when the pipeline exists to prepare features for something else.

<strong>How do I see what the model actually receives?</strong> `pipe[:-1].transform(X)` runs every step except the last and hands back the array the estimator was given.

<strong>Does a pipeline slow anything down?</strong> No. It calls the same methods in the same order; the only overhead is a few attribute lookups.

<strong>Can I add a step to a fitted pipeline?</strong> You can modify `pipe.steps`, and the result is unfitted from that point on. Building a new pipeline is clearer.

## Reading a pipeline someone else wrote

An unfamiliar pipeline is quicker to understand than an unfamiliar script, because the steps are the structure and they are listed in order.

Three questions cover it. **What are the steps?** `[name for name, _ in pipe.steps]` prints the sequence, and the order is the order data flows through. **What does each one learn?** Every step's fitted attributes end in an underscore, so `pipe["scale"].mean_` and `pipe["encode"].categories_` say what it took from the data. **What comes out?** `pipe[:-1].transform(X).shape` tells you how many features the model is actually seeing, which is often surprising after one-hot encoding.

The display helps too. Printing a pipeline in a notebook renders a diagram of the steps, and `sklearn.set_config(display="diagram")` makes that the default. In a plain terminal, `print(pipe)` gives the nested repr, which is dense but complete &mdash; every step and every non-default hyperparameter.

What to look for when reviewing one: whether anything that learns from data sits *outside* it. A script that scales, imputes or selects features before building the pipeline has moved that step out of the folds, and the pipeline's presence gives a false impression of safety. The pipeline only protects what is inside it.

## The order of the steps, again

Steps run in the order given, and some orders are wrong.

Imputation before scaling, because a scaler cannot compute a mean across missing values. Encoding before scaling, because a scaler cannot subtract a mean from a string. Both before feature selection, because the selector needs numeric, complete columns to score. And selection before the model, so the model sees what was chosen.

The sequence that covers most tabular problems is: impute, encode, transform any skew, scale, select, fit. Not every problem needs all six, and the relative order of the ones you use should follow that list.

Getting it wrong usually raises, which is fortunate. The exception is putting selection before scaling when the selector's criterion is scale-sensitive &mdash; that runs, and quietly selects the columns with the largest units.

## Things to try

1. <strong>Confirm the interface.</strong> In the first editor, note that a pipeline has `fit` and `predict` &mdash; it is an estimator, not a wrapper you unwrap.
2. <strong>Reach inside.</strong> In the second editor, try `pipe[:-1].transform(X)[:2]` to see exactly what the model receives.
3. <strong>Tune the preprocessing.</strong> In the fourth editor, add `"scale__with_std": [True, False]` to the grid and see whether it changes the winner.
4. <strong>Break it deliberately.</strong> Fit the scaler outside a pipeline on all of `X`, then cross-validate the model alone, and compare against the pipeline version.

## Where this leaves you

One object, fitted once, holding every step that learns anything. It makes cross-validation honest, makes the preprocessing tunable, and makes deployment a single file. There is no situation in this track where doing the steps by hand is preferable, and forming the habit early costs nothing.
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
intro: Every other failure in machine learning makes the score worse. This one makes it better, which is why it survives review and reaches production.

## What it is

Leakage is information reaching the model during training that it will not have when it is actually used.

The defining property is the direction of the error. Overfitting, a bad metric, an unlucky split &mdash; these produce results that look worse than the model is, or at least ambiguous. Leakage produces results that look *better*. So it does not trigger the instinct that something is wrong; it triggers satisfaction.

That asymmetry is why it is the most expensive mistake in the field. A model with a leak passes every check, gets deployed, and fails on the first real batch &mdash; at which point the evaluation that approved it is worthless and nobody knows why.

## Cross-validation will not save you

Worth stating plainly, because cross-validation is otherwise the answer to almost everything on this track.

Cross-validation protects against one specific thing: a score that depends on which rows happened to be held out. If the leak is in the *data* &mdash; a column derived from the answer &mdash; then every fold contains it, every fold is inflated, and the mean of five inflated numbers is an inflated number with a reassuring standard deviation.

The first editor shows it: an honest 0.643 becomes 1.000, across all five folds, with no warning of any kind.

## The five shapes

**Target leakage.** A feature that encodes the answer, usually because it was recorded after the outcome. A `case_closed_date` predicting whether a case closed. A `discount_given` predicting churn, when the discount was offered *because* the customer was leaving. A diagnosis code entered at the same time as the diagnosis. These are the hardest to spot because the column is legitimately in the database and nothing about its name says when it was written.

**Preprocessing before the split.** A scaler, imputer, encoder or feature selector fitted on all the data has seen the test rows. The cross-validation module measured this: feature selection outside the folds reported 0.825 on pure noise.

**Duplicate rows.** After a bad join, a re-import, or genuinely repeated records. A duplicate split across train and test means the model has the answer memorised. The second editor scores 1.000 on random data for exactly this reason.

**Group leakage.** Several rows describing one entity &mdash; a patient, a customer, a device, a document &mdash; landing on both sides. The model learns to recognise the entity rather than the pattern. The third editor scores 0.87 where the honest answer is chance.

**Temporal leakage.** Shuffling data that has an order, so the training set contains the future. The fourth editor goes from R&sup2; of 0.977 to −2.526 when the split respects time, and the second number is the one describing the job the model would actually have.

## Target encoding deserves its own warning

It is the most useful high-cardinality encoding and the most reliable way to leak.

Replacing a category with the mean target for that category is compact, powerful, and computed from `y`. Do it over the whole dataset and every row has contributed to the number that describes it. With a hundred rows per category the contribution is small; with six, as in the fifth editor, it is a sixth &mdash; and a feature built from random labels predicts those labels at 0.71.

The fix is to compute the encoding inside the folds, with the row's own contribution excluded &mdash; which is what scikit-learn's `TargetEncoder` does, using an internal cross-fitting scheme. Hand-rolled target encoding is almost always leaky, and the leak is proportional to how rare the categories are, which is exactly when the encoding is most tempting.

## How to notice

There is no detector. There is a set of habits.

**Be suspicious of a good score.** Not sceptical of a good model &mdash; suspicious of a *surprisingly* good one. If the problem is hard and the number is excellent, the first hypothesis should be a leak, not a breakthrough. Comparing against a dummy makes the size of the claim visible.

**Look at feature importances.** A single feature dominating, especially one nobody expected to matter, is the classic signature. Ask what it is, when it is written, and by what process.

**Ask the timing question for every column.** *Would this value be known, in this form, at the moment the prediction has to be made?* This is the single most effective check available, and it requires domain knowledge rather than code. A column that is only populated after the event is a leak regardless of how innocent it looks.

**Ask who produced the row.** If several rows can come from one entity, group the split. If rows can be duplicated, check. If the data has a timestamp, respect it.

**Test on genuinely later data** where possible. A model that scores well in cross-validation and badly on the next month is telling you something a random split could not.

## The habits that prevent it

Split first, before anything that learns. Put every transformer in a pipeline so it is refitted inside each fold. Use `GroupKFold` when rows share an entity and `TimeSeriesSplit` when they are ordered. Check for duplicates before splitting. Hold out a final test set and touch it once.

None of these is expensive, and together they close every mechanical route. What they cannot close is target leakage, because that is a fact about the meaning of a column rather than about the code &mdash; which is why the timing question has to be asked of every feature, by someone who knows what the columns mean.

## The famous cases

Leakage is not a beginner's mistake. It has invalidated published research, competition results and deployed systems, and the examples are worth knowing because they are all plausible.

A widely cited early result on detecting a disease from chest scans turned out to be partly detecting *which hospital* the scan came from &mdash; sicker patients were concentrated at one site, and the scanner left a signature in the image. The model was excellent at the task it was actually solving and useless at the one it was believed to be solving.

Competition datasets have repeatedly leaked through row ordering, where the file happened to be sorted by the target, and through id columns that correlated with when a record was created. Both give a model something real to learn that has nothing to do with the problem.

A recurring one in industry: a churn model trained on a table where the "customer contacted support" flag was updated during the cancellation call. The feature was genuinely predictive and genuinely unavailable at the moment a prediction was needed.

The common thread is that none of these look like errors in the code. Every one is a fact about how the data came to exist, which is why reading the code more carefully never finds them and asking where a column comes from usually does.

## The cost of being too careful

The opposite failure exists and is worth naming, because leakage anxiety can become its own problem.

Excluding every feature that has any relationship with the target removes the signal along with the leak. A feature that is predictive because it is genuinely causally upstream is exactly what you want, and dropping it because it is "too predictive" makes the model worse for no reason.

Grouping a split when the rows are genuinely independent throws away resolution and gives an unnecessarily pessimistic estimate. Refusing to use any aggregate feature because target encoding can leak rules out a whole class of useful ones that are computed correctly.

The distinction is not how predictive a feature is. It is whether the value would exist, in that form, at the moment the prediction has to be made. A feature that passes that test is allowed to be as predictive as it likes.

<strong>Is a highly predictive feature always suspicious?</strong> No. It is worth one question - would this be known at prediction time - and if the answer is yes, use it.

<strong>How do I check for duplicates?</strong> `df.duplicated().sum()` before splitting, and consider near-duplicates too: rows differing only in an id or a timestamp are functionally the same row.

<strong>Does leakage matter if I only care about ranking?</strong> Yes. A leaked feature ranks well in evaluation and is absent in production, so the ranking you deploy is not the one you measured.

<strong>Can I fix a leak by removing the column?</strong> Usually, and check what else was derived from it. Aggregates, ratios and encodings built on a leaky column carry the leak with them.

## A checklist before you trust a number

Six questions, in the order they are cheapest to answer. Running through them takes a few minutes and catches the large majority of leaks.

**Did anything fit before the split?** Scaler, imputer, encoder, selector, vectoriser. If it learned from data and it ran before `train_test_split`, the number is compromised. The fix is a pipeline.

**Are there duplicate rows?** Count them, including near-duplicates that differ only in an id or a timestamp.

**Can one entity produce several rows?** If so, the split must group them. This is the one people most often get wrong on data that looks tabular and independent.

**Does the data have an order?** Timestamps, sequence numbers, anything where later rows could not have informed earlier ones. Then the split is forward-only.

**For every feature: would it exist at prediction time?** Asked column by column, with someone who knows the source system. This is the slow one and the one that catches target leakage, which nothing else will.

**Is the score plausible?** Compared against a dummy, against published results on similar problems, and against what a domain expert would guess. Surprise is the signal.

A model that survives all six is not guaranteed honest, but the remaining routes are narrow and unusual. A model that has not been through them has an unknown probability of being wrong in the most expensive direction.

<strong>What if I find a leak after deploying?</strong> Retrain without the leaking feature and re-measure honestly before deciding whether the model is still worth running. The old score should be treated as never having existed rather than as a target to recover.

<strong>Is leakage always accidental?</strong> Mostly, and there is a well-known variety that is not: tuning against the test set until the number is satisfactory. That is leakage through the researcher rather than through the data, and it produces the same inflated result.

## Things to try

1. <strong>Run the first editor.</strong> 0.643 becomes 1.000 from one extra column, and every fold agrees.
2. <strong>Vary the duplication.</strong> In the second editor, duplicate only a quarter of the rows and see how much of the inflation survives.
3. <strong>Change the group size.</strong> In the third editor, set `per_person=2` and watch the gap narrow &mdash; the more rows per entity, the worse the leak.
4. <strong>Make the categories rarer.</strong> In the fifth editor, raise `n_cats` to 150 and watch the leaked score climb.

## Where this leaves you

The failure that improves your metrics. Cross-validation cannot see it, a good score is evidence for it rather than against it, and the only reliable defence is asking, of every column, whether it would exist at the moment the prediction is needed.
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
intro: A gap in the data is two problems: the estimator will not run, and the gap itself may have been telling you something.

## Why it has to be handled

Almost every estimator in scikit-learn raises `ValueError: Input X contains NaN` rather than guessing. That refusal is deliberate &mdash; there is no universally correct fill, and silently choosing one would hide a decision that changes the model.

The exceptions are worth knowing before you reach for an imputer at all. `HistGradientBoostingClassifier` and its regressor sibling handle missing values natively: at each split, the tree learns which side the missing rows should go, which is a genuinely better answer than filling in a number, because it lets the missingness itself influence the prediction without inventing data. On tabular problems with gaps, starting there and skipping imputation entirely is often the right move.

For everything else, something has to fill the gap.

## The simple strategies, and choosing between them

`SimpleImputer` replaces missing values with one number per column, learned during `fit` and stored in `statistics_`.

**mean** is the default and the wrong default for most real data. The editor above shows why: with values of 1, 2 and 100, the mean is 34.33 &mdash; a number nothing like any of the observations. Any skew or outlier drags it.

**median** is the safer choice for numeric columns and should probably be your habit. It is unaffected by the tail and always lands on a plausible value.

**most_frequent** works for categorical columns and for numeric ones with few distinct values.

**constant** fills with `fill_value` &mdash; useful when there is a meaningful default, and useful with a sentinel like -1 when you want the model to be able to see the imputed rows. For categorical data, `fill_value="missing"` makes absence an explicit category, which is often exactly right.

## The fill value is learned

This is the part that connects back to the rest of the track: `statistics_` is computed from data, so an imputer fitted on everything has seen the test set.

The effect is usually small &mdash; a median shifts a little &mdash; but the principle is the same as everywhere else, and there is a stronger practical reason. In production, the median of the future data is not available. The model has to fill gaps with a number computed at training time, so that is the number the evaluation should use.

The editor above shows the training median and the test median differing in the third decimal. The test rows get the training one, which is correct.

`SimpleImputer` inside a `Pipeline` handles this automatically, refitting on each training fold. As with scaling, there is no good reason to do it by hand.

## Missingness is information

The most common mistake is not choosing the wrong fill value. It is discarding the fact that a value was missing.

Data is rarely missing at random. A blank income field on a loan application, an absent test result, an unrecorded satisfaction score &mdash; in each case the absence usually correlates with something. People decline to answer questions for reasons, tests are not ordered for reasons, and fields go unfilled for reasons.

`add_indicator=True` appends a binary column marking where each gap was. It costs one column per affected feature and it hands the model the pattern of absence as a feature in its own right.

The last editor makes the size of the effect concrete. With a value missing mostly when the answer is yes, imputing alone scores 0.77; imputing with an indicator scores 0.987. The imputer filled in a plausible number and erased the most informative thing in the dataset; the indicator put it back.

The taxonomy is worth knowing by name. **Missing completely at random** &mdash; the gap has no relationship to anything &mdash; is the only case where plain imputation loses nothing, and it is the rarest. **Missing at random**, where the gap depends on other observed features, is common and partly recoverable by a model-based imputer. **Missing not at random**, where the gap depends on the unobserved value itself, is both the most common and the one where the indicator matters most.

## Using the other columns

When features are correlated, a column constant is a poor guess. Two better options use the rest of the row.

`KNNImputer` finds the most similar complete rows and averages their values for the missing feature. The editor above shows it recovering 8.0 where the column mean gives 5.5, because the two columns move together and the neighbours know it. It needs the features scaled, since it measures distance, and it is expensive on large data because it searches for neighbours.

`IterativeImputer` models each column with missing values as a function of the others, in rounds, until the estimates settle. It is the most capable of the three and the slowest, and it is still marked experimental &mdash; importing it requires `from sklearn.experimental import enable_iterative_imputer` first, which catches everyone once.

Both are worth trying when imputation quality matters. Neither is worth the complexity when the missingness is light and the model is a gradient booster that could have handled it natively.

## Dropping, and when it is allowed

`dropna()` is the tempting one-liner and it is only safe under conditions worth checking.

Dropping rows is defensible when the values are genuinely missing at random and the affected rows are few. It is a mistake when the missingness is informative, because you are deleting exactly the rows that carry the pattern &mdash; and the bias it introduces is invisible in every subsequent metric.

Dropping a column is defensible when most of it is missing and no indicator would help. A column that is 95% empty rarely carries enough to be worth imputing, though the 5% pattern occasionally does &mdash; which is what the indicator would tell you.

The asymmetry to remember: you can drop rows from the training data, but you cannot drop them at prediction time. A model that has never seen a missing value in a column will still be handed one eventually, and something has to happen. Deciding what, during training, is the whole point of having an imputer in the pipeline.

## Categorical columns need a different answer

Everything above assumes numeric data. Text columns have gaps too, and the arithmetic strategies do not apply.

`SimpleImputer(strategy="most_frequent")` works and quietly asserts that the missing rows are like the majority, which is often exactly the claim that is false. `strategy="constant", fill_value="missing"` is usually better: it creates an explicit category, the encoder gives it its own column, and the model can learn whatever that column is worth. Absence becomes a value rather than a guess.

`OneHotEncoder` also handles `NaN` directly, treating it as its own category without any imputation step, which is the shortest route to the same result.

The reason the explicit category usually wins is the same as for the indicator: in real data, "not stated" is a fact about the record rather than a hole where a fact should be. A blank employer field, an unselected optional dropdown, a survey question skipped &mdash; each tells you something, and folding it into the most common value asserts the opposite.

## How much is too much

A quick rule for triage, applied per column rather than to the dataset as a whole.

**Under about 5% missing.** Almost any reasonable imputation works and the choice barely matters. Use the median, add the indicator, move on.

**Between 5% and 30%.** The choice starts to matter. Compare a couple of strategies by cross-validation, and treat the indicator as compulsory rather than optional.

**Over 30%.** The column is mostly absent, and imputing it means most of it is invented. Consider keeping only the indicator and discarding the values, which sometimes performs better than either the column or its removal.

**Over 80%.** Usually drop the column, unless the small present portion is known to be highly informative.

These are rules of thumb rather than thresholds, and the honest way to settle any of them is to try both inside a pipeline and compare cross-validated scores. That takes two lines, which is less effort than arguing about it.

<strong>Why does IterativeImputer need a special import?</strong> It is still marked experimental, so `from sklearn.experimental import enable_iterative_imputer` has to run first. The import looks unused and is not.

<strong>Should I impute the target?</strong> No. Rows with a missing target carry no information for supervised learning - drop them, and check why they are missing before you do.

<strong>Does KNNImputer need scaling?</strong> Yes. It measures distance between rows, so a column in thousands dominates the neighbour search exactly as it would for k-NN itself.

<strong>Can I impute before splitting if I only use the median?</strong> No. The median is learned from data, so it carries information from the test rows into training. The effect is small and the habit is what matters.

## Finding out what is actually missing

Before choosing a strategy, two minutes of counting decides most of it.

Count per column rather than in total. `df.isna().sum()` gives the picture, and it is usually uneven &mdash; one or two columns carry nearly all the gaps while the rest are complete. That changes the problem from "how do I impute this dataset" to "what do I do about these two columns", which is a much easier question.

Then look at whether the gaps coincide. Columns that are missing together usually come from the same source: a form section that was skipped, a system that was down, a join that failed for a subset. If three columns are missing on exactly the same rows, they are one piece of information absent once, and one indicator covers all three rather than three separate ones.

Finally, compare the target between rows with and without the gap. A difference in the target rate between present and missing is direct evidence that the missingness is informative, and it takes one line to check. When it is large, the indicator is not optional and imputation alone will lose most of the signal &mdash; which is what the last editor on this page demonstrates at 0.77 against 0.987.

None of this requires a plot or a library. Three counts and a comparison, before any decision about strategy.

<strong>What about values that are not NaN but mean missing?</strong> Sentinels like -999, 0, or an empty string are extremely common in exported data, and no imputer recognises them. Convert them to `NaN` first, or the model treats -999 as a very small number.

<strong>Does the order of imputation and encoding matter?</strong> Yes. Impute categorical columns before encoding them, or the encoder treats `NaN` as its own category - which is sometimes what you want and should be a decision rather than an accident.

## Things to try

1. <strong>Compare the strategies.</strong> In the second editor, note that mean fills 34.33 into a column whose other values are 1, 2 and 100.
2. <strong>Recover the correlation.</strong> The fifth editor has KNNImputer land on 8.0 exactly. Change the neighbours to 1 and see what happens.
3. <strong>Turn the indicator off.</strong> The last editor drops from 0.987 to 0.77. That gap is the value of one extra column.
4. <strong>Skip imputation entirely.</strong> Replace the pipeline in the last editor with `HistGradientBoostingClassifier()` on the raw data with gaps.

## Where this leaves you

Median rather than mean for numeric columns, an explicit category for categorical ones, `add_indicator=True` almost always, the imputer inside a pipeline so the fill value obeys the split, and a check of whether a gradient booster could have handled the gaps without any of it.
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
intro: A pipeline applies every step to every column. Real tables need scaling on some columns and encoding on others, and ColumnTransformer is how you say which is which.

## The problem

A `Pipeline` is a sequence applied to all of `X`. That works when the columns are homogeneous and breaks immediately on a real table.

Numeric columns want imputing with a median and scaling. Categorical columns want imputing with a constant and one-hot encoding. Applying a scaler to a text column raises; applying an encoder to a continuous one produces a column per distinct value, which is nonsense.

The manual workaround &mdash; split the frame, transform each part, concatenate &mdash; works and puts the transformations outside any pipeline, which puts them outside the cross-validation folds, which is the leak this track keeps returning to.

`ColumnTransformer` solves it properly: it routes each subset of columns to its own transformer and concatenates the results, and because it is itself a transformer, the whole thing drops into a pipeline as a single step.

## How it is written

Each entry is a triple: a name, a transformer, and the columns it applies to.

The name is yours to choose and appears in the generated feature names and in the parameter keys for tuning, so short and meaningful pays off &mdash; `num` and `cat` rather than `transformer_1`.

The columns can be a list of names, a list of integer positions, a boolean mask, or a callable. Passing a **list** matters: a list of one name selects a DataFrame, which is two-dimensional; a bare string selects a Series, which is one-dimensional, and the transformer raises. The error message says "Expected a 2-dimensional container", which is precise once you know what it refers to.

The outputs are concatenated left to right in the order the transformers are listed, not in the original column order. So the resulting array's columns follow your specification, which is why `get_feature_names_out()` is the reliable way to know what ended up where.

## remainder, and the columns you forgot

By default, any column not named in any transformer is **dropped**.

That is usually right &mdash; ids, timestamps and free text usually should not reach the model &mdash; and it is silent, which is the part worth knowing. A column added to the source data will simply not appear in the model, with no warning, and the effect is a model quietly ignoring a feature somebody thought they had added.

`remainder="passthrough"` keeps the unnamed columns as they are. It is convenient and slightly dangerous: it will happily pass through an id column, which is exactly the sort of thing that lets a model memorise rows.

`remainder=SomeTransformer()` applies a transformer to everything left over, which is occasionally the tidiest way to say "scale everything I have not otherwise mentioned".

The habit worth adopting: name every column explicitly, or use selectors that provably cover everything, and treat the default drop as a safety net rather than as the design.

## Selecting by type

Listing column names by hand is fine for a fixed table and a maintenance burden for anything that changes.

`make_column_selector(dtype_include="number")` selects the numeric columns whatever they are called. `dtype_include=object` picks up the strings. `pattern="^date_"` selects by name. The selector runs at `fit` time against whatever frame it is given, so a new numeric column is handled without touching the pipeline.

The caution is that dtypes are not always what you expect. A categorical column stored as integers &mdash; a postcode district, a department id &mdash; is selected as numeric and scaled, which is the mistake the encoding module warned about, now happening automatically. Converting such columns to a string or a pandas `category` dtype before the pipeline is what makes dtype-based selection safe.

## Nesting a pipeline inside a branch

A single column group usually needs more than one step: numeric columns want imputing *and* scaling.

The transformer in a `ColumnTransformer` entry can be a `Pipeline`, which is how that is expressed. `make_pipeline(SimpleImputer(strategy="median"), StandardScaler())` becomes the numeric branch, and the categorical branch gets its own with an imputer and an encoder.

The result is a small tree: a pipeline containing a column transformer containing pipelines containing transformers. That sounds elaborate and is the standard shape of every real scikit-learn program, because it is the minimum structure that does the right thing on a mixed table.

The whole tree is one estimator. `fit` on the outer pipeline reaches every leaf, and cross-validation refits all of it on each training fold.

## Reaching into it to tune

The double-underscore convention composes, so parameters deep in the tree are addressable.

`pre__num__simpleimputer__strategy` reads outside in: the step named `pre`, its branch named `num`, the step named `simpleimputer` in that branch, and its `strategy`. Four levels, one string, and a grid search can vary it alongside the model's own hyperparameters.

This is more useful than it first appears. Whether to impute with the mean or the median, whether to scale, whether to drop the first one-hot column &mdash; these are choices usually made by guesswork, and they can be made by cross-validation instead, in the same search that tunes the model.

`pipe.get_params().keys()` lists every addressable parameter, which is the fastest way to find the right spelling rather than deriving it.

## Getting the names back

After one-hot encoding, the array has more columns than the frame had, with names nobody wrote.

`get_feature_names_out()` reconstructs them, prefixed by the transformer name: `num__age`, `cat__city_paris`. Called on the outer pipeline, it traces through every step.

That matters for reading the model. Zipping the names against `coef_` or `feature_importances_` turns an anonymous array into a labelled result, and without it the mapping has to be reconstructed by counting, which is both tedious and easy to get wrong by one after any change to the preprocessing.

## The shape of a real preprocessing block

Almost every tabular project ends up with the same structure, and it is worth having it in mind as a template rather than deriving it each time.

A numeric branch: impute with the median, then scale. A categorical branch: impute with a constant such as `"missing"`, then one-hot encode with `handle_unknown="ignore"`. A column transformer routing the two by dtype. A model on the end. The whole thing in one `Pipeline`, cross-validated, with the preprocessing choices exposed to a search.

That covers a large majority of tabular problems and is about fifteen lines. What varies between projects is which extra branches appear: a text column going to a vectoriser, a date column going to a custom transformer that extracts the parts, a high-cardinality column going to a target encoder instead of one-hot.

The value of the template is not the specific steps but that it puts every learned transformation in one place, inside the folds, addressable by a search. A project that starts from it rarely acquires the leaks that a project assembled step by step does.

One practical note: build it up one branch at a time and check the output shape after each. A column transformer that silently drops half the frame produces a model that works and underperforms, and the shape is the fastest way to notice.

## When the branches disagree about rows

A limitation worth knowing, because it is not obvious from the interface.

Every transformer in a `ColumnTransformer` receives the same rows and must return the same number of rows, in the same order. The results are concatenated horizontally, so anything that reordered or dropped rows would misalign the columns against each other and against `y`.

That rules out row-level operations inside it: no dropping outliers, no resampling, no aggregating. Those belong before the pipeline, applied to the training data only, or in a library built for it &mdash; `imbalanced-learn` provides a pipeline that understands row changes, which is the right tool when resampling is part of the model rather than part of the data preparation.

It also means a transformer that returns a different number of rows than it received will fail with a shape error rather than a helpful message, so a custom transformer that filters is a mistake worth ruling out early.

<strong>Does the output keep my column order?</strong> No. Columns come out in the order the transformers are listed, then within each transformer. `get_feature_names_out()` is the reliable way to know what is where.

<strong>Can I use the same column in two transformers?</strong> Yes - a column can appear in more than one entry, and both outputs are kept. That is how you would scale a column and also bin it.

<strong>Is there a shorthand?</strong> `make_column_transformer((StandardScaler(), ["age"]), (OneHotEncoder(), ["city"]))` skips the names and generates them, in the same way `make_pipeline` does.

<strong>What if a column is numeric but categorical in meaning?</strong> Convert it to a string or a pandas `category` dtype before the pipeline, or dtype-based selection will scale it as a number.

## Debugging one that is not working

A column transformer that misbehaves is harder to inspect than a plain pipeline, because the branches run in parallel and the output is a single anonymous array. Four things to check, in order.

**The output shape.** `pre.fit_transform(df).shape` against what you expected. Too few columns usually means a branch selected nothing; too many usually means a high-cardinality column reached the one-hot encoder.

**What each branch actually selected.** After fitting, `pre.transformers_` holds the resolved triples, with the callable selectors already turned into concrete column lists. Printing the third element of each entry says exactly which columns went where, which is the fastest way to find a column that fell through to `remainder`.

**The names.** `pre.get_feature_names_out()` lists every output column with its branch prefix. If a name you expected is absent, the column was dropped; if there are hundreds of `cat__` names, an identifier reached the encoder.

**One branch at a time.** `pre.named_transformers_["num"]` gives the fitted branch, which can be inspected on its own &mdash; its imputer's `statistics_`, its scaler's `mean_`. When the whole thing produces something odd, narrowing to one branch usually localises it in a minute.

The general lesson is that the object is introspectable at every level; the difficulty is only that the useful attributes have to be asked for by name.

<strong>Does it work with NumPy arrays?</strong> Yes, selecting by integer position rather than by name. Names are worth the DataFrame, since positions shift whenever a column is added.

<strong>Can a branch return a sparse matrix?</strong> Yes, and the result is sparse if enough of it is. `sparse_threshold=0` forces a dense output when the next step needs one.

## Things to try

1. <strong>Watch the shape change.</strong> The first editor turns three columns into five. Read the names to see which came from where.
2. <strong>Lose a column.</strong> In the third editor, note that `id` disappears with no warning under the default.
3. <strong>Add a column.</strong> In the second editor, add another numeric column to the frame and confirm the selector picks it up with no edit to the transformer.
4. <strong>Find the parameter names.</strong> In the fifth editor, print `sorted(pipe.get_params())` and look for the keys you could tune.

## Where this leaves you

One object that sends each group of columns to the transformer it needs, nests pipelines inside its branches, drops what you did not mention, and exposes every setting inside it to a search. Together with `Pipeline` it is the shape of essentially every real scikit-learn program on tabular data.
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

**Overfitting** is learning the training data rather than the pattern in it. The model captures noise, coincidences and details specific to the rows it was shown, none of which recur. Training score high, test score much lower.

**Underfitting** is the opposite: the model is too simple, or too constrained, to represent the structure that is there. It does badly on the training data and equally badly on the test data.

Both produce a disappointing test score, which is why a single number cannot distinguish them &mdash; and why the responses are opposite. Overfitting needs a simpler model, more regularisation, or more data. Underfitting needs a more flexible model, better features, or less regularisation. Applying the wrong remedy makes things worse, and guessing is a coin flip.

## The gap is the diagnostic

Compare the training score with the test score.

**Both high, small gap.** Working. Nothing to fix.

**Train high, test much lower.** Overfitting. The size of the gap is roughly how much of the training performance was memorisation.

**Both low, small gap.** Underfitting. The model is not capturing what is there.

**Train lower than test.** Unusual. Legitimate when regularisation or dropout is active during training but not scoring; otherwise a sign the folds are not comparable.

`cross_validate(..., return_train_score=True)` gives you both columns. It costs an extra scoring pass per fold and it is the single most informative argument in the model-selection module, because it converts "the score is disappointing" into "the score is disappointing *for this reason*".

The first editor shows the gap opening as a tree is allowed to grow: +0.070 at depth 1, +0.193 unconstrained, with the test score peaking in the middle and then going nowhere while the training score climbs to a perfect 1.000.

## Complexity is the dial

Every model has something that controls how much structure it can represent.

Tree depth, and the minimum samples in a leaf. The number of neighbours in k-NN &mdash; fewer neighbours is *more* complex, which is the one that runs backwards. The degree of a polynomial expansion. The `C` in an SVM or a logistic regression, where larger is less regularised. The number of estimators and the learning rate in a boosting model.

Turn the dial up and the training score rises monotonically; the test score rises, peaks, and falls. The peak is what you are looking for, and `validation_curve` finds it by sweeping one parameter with cross-validation at each setting.

The fourth editor shows both ends on the same data. The truth is a parabola. Degree 1 scores 0.008 on training &mdash; it cannot bend at all. Degree 2 is right. Degree 15 scores 0.894 on training and **−17.888** on test, which is far worse than predicting the mean, and is what memorising sixty points with sixteen coefficients produces.

## Would more data help?

The question people guess at, and `learning_curve` answers it directly by fitting at several training-set sizes and reporting both scores.

Two shapes matter. **A large gap that is still narrowing** as the training set grows means more data would help &mdash; the model has capacity it cannot yet use reliably. **Two curves that have converged** means more data will not help; the model has extracted what it can, and improving requires a different model or better features.

The third editor shows the converged case: at 80 training samples the gap is 0.900 against 0.798, and by 1600 it is 0.844 against 0.838. Collecting another thousand rows would be wasted effort, and knowing that before commissioning the collection is worth a great deal.

The training score falling as the training set grows is normal and often surprises people. Fitting 80 points is easy; fitting 1600 is not.

## Bias, variance, and why averaging works

The two failures have formal names. **Bias** is error from a model too rigid to represent the truth &mdash; underfitting. **Variance** is error from a model so flexible that it changes substantially when the training data changes &mdash; overfitting.

Variance is measurable, and the fifth editor measures it: refitting a single deep decision tree on five different halves of the data moves one prediction by 270. The same exercise with a fifty-tree random forest moves it by 48.

That reduction is the entire idea behind ensembles. Each tree is high-variance; the errors are partly independent; averaging cancels them. It is why a random forest is almost always better than the tree inside it, and why bagging works on unstable models and does nothing for stable ones.

The classic framing is a trade-off, and modern practice complicates it &mdash; very large models sometimes improve again past the point of interpolating the training data. For everything in this track, the trade-off framing holds: reducing one usually increases the other, and the useful setting is where their sum is smallest.

## The remedies, and that they can fail

For **overfitting**: constrain the model, add regularisation, reduce the number of features, get more data, or use an ensemble to average the variance away.

For **underfitting**: use a more flexible model, add features or interactions, reduce regularisation, or train for longer if the fit was cut short.

The last editor is worth dwelling on because it shows the trade honestly. Three constraints applied to an overfitting tree: all three lower the training score, as they must. `max_depth=3` and `ccp_alpha=0.01` raise the test score. `min_samples_leaf=20` lowers it, from 0.826 to 0.806 &mdash; it constrained the model past the useful point and turned overfitting into underfitting.

So "add regularisation" is a direction rather than a fix, and the amount has to be found by cross-validation rather than chosen. That is precisely what the tuning module is for.

## Overfitting the validation set

There is a third failure, and it is the one that catches experienced people rather than beginners.

Every time you look at a validation score and change something in response, you use that score to make a decision. Do it once and the effect is negligible. Do it two hundred times &mdash; trying models, sweeping hyperparameters, adding and removing features, each time keeping what scored better &mdash; and the winner has been selected for performing well on those particular folds, including on their noise.

The result is a cross-validated score that is optimistic even though every individual fit was honest. Nothing in the procedure was wrong; the selection was the leak. It is the same mechanism as picking the best of twenty test scores, just slower and less obviously a mistake.

Three defences. Keep a final test set that is touched exactly once, at the end, after every decision has been made. Prefer a small number of deliberate comparisons to a long undirected search. And when the difference between two candidates is smaller than the standard deviation across folds, treat them as tied rather than picking a winner &mdash; because at that point you are choosing noise.

Nested cross-validation is the rigorous version: an inner loop tunes and an outer loop scores the whole tuning procedure. It costs a multiple of the fits and is the right answer when the number being reported matters.

## Signals from the model itself

Besides the gap, three things hint at overfitting before you have measured anything.

**Coefficients that are enormous.** A linear model whose coefficients run to thousands is balancing large positive and negative terms that nearly cancel &mdash; a fit that is precariously tuned to the training rows. Regularisation exists to prevent exactly this, and the size of the coefficients is a reasonable proxy for how much is needed.

**A tree with as many leaves as samples.** If `tree.get_n_leaves()` is close to the number of training rows, every leaf is one or two samples and the model is a lookup table.

**Scores that move a lot between folds.** A high standard deviation across cross-validation folds means the model is sensitive to which rows it saw, which is variance by definition.

None of these is conclusive on its own. All three are cheap to check and worth a glance before the more expensive diagnosis.

<strong>Is a perfect training score always bad?</strong> Not by itself. An unconstrained tree reaches 1.0 by construction. It is bad when the test score is far below it.

<strong>Does more data ever cause overfitting?</strong> No - more data only ever helps generalisation. More *features* on the same rows is what makes it worse.

<strong>Which comes first, tuning or feature work?</strong> Usually features. A learning curve that has converged says the model has extracted what it can, and no amount of tuning changes that.

<strong>What is ccp_alpha?</strong> Cost-complexity pruning: it grows the tree fully and then removes branches whose contribution is not worth their complexity. Often better than capping the depth, because it prunes where pruning helps rather than everywhere.

## Which dial belongs to which model

The complexity control has a different name in every estimator, which makes the general idea harder to see than it should be. The mapping is worth having in one place.

**Decision trees.** `max_depth` caps how many questions can be asked. `min_samples_leaf` and `min_samples_split` stop the tree splitting groups that are already small &mdash; often a better control than depth, because it responds to the data rather than to a fixed count. `ccp_alpha` prunes after growing.

**Random forests.** The same tree parameters, plus `n_estimators`, which is the one that does *not* overfit &mdash; more trees only ever helps, at the cost of time. `max_features` controls how decorrelated the trees are and is the main variance dial.

**Gradient boosting.** `learning_rate` and `n_estimators` trade against each other: a smaller rate needs more trees and generalises better. `max_depth` is kept small, typically 3 to 6, because the ensemble supplies the flexibility.

**Linear models.** `alpha` in Ridge and Lasso, where larger is more regularised. `C` in `LogisticRegression` and the SVMs, where larger is *less* regularised &mdash; the one inversion in the library, and the reason to check which you are holding.

**k-NN.** `n_neighbors`, where more neighbours is a simpler model. This runs backwards from most intuitions about "bigger numbers mean more".

**Polynomial features.** `degree`, which increases complexity faster than anything else on this list &mdash; degree 3 on ten features is 286 columns.

The pattern underneath: every one of these controls how much of the training data the model is permitted to represent exactly.

<strong>Can a model overfit with only a few features?</strong> Yes. Degree-15 polynomial features on one input column scored -17.888 on test in the fourth editor. What matters is flexibility relative to the number of rows, not the raw column count.

<strong>Do I fix underfitting by removing regularisation entirely?</strong> Try it to confirm the diagnosis, then find the amount by cross-validation. Zero is rarely the best value.

## Things to try

1. <strong>Watch the gap grow.</strong> The first editor's last column goes from +0.070 to +0.193 while the test score stops improving after depth 3.
2. <strong>Find the peak.</strong> In the second editor, note that the training score keeps rising after the test score has stopped &mdash; that divergence is the definition.
3. <strong>Ask whether data would help.</strong> In the third editor, cut `n_samples` to 300 and see whether the curves have converged by then.
4. <strong>Over-constrain deliberately.</strong> In the last editor, try `min_samples_leaf=100` and watch both scores fall together.

## Where this leaves you

One extra column tells you which failure you have. `validation_curve` finds the right complexity, `learning_curve` says whether more data would help, and every constraint is a trade that has to be measured rather than assumed.
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
    _svg(_box(64, 14, 32, 16, S, A) + _txt(80, 25, "x < 2?", A, 7) +
         _arrow(72, 32, 46, 44) + _arrow(88, 32, 114, 44) +
         _box(30, 46, 32, 16, S, M) + _txt(46, 57, "class 0", M, 7) +
         _box(98, 46, 32, 16, S, M) + _txt(114, 57, "x < 7?", M, 7) +
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
intro: The only model in this track whose fitted form a person can read and check. That readability comes with an instability that explains why trees are almost always used in groups.

## How it works

A decision tree asks a series of yes/no questions about one feature at a time, and each answer sends the sample down a branch. At the bottom, a leaf holds a prediction: the majority class for a classifier, the mean target for a regressor.

Fitting means choosing the questions. At each node the algorithm tries every feature and every threshold, scores how well each split separates the classes, and keeps the best. Then it repeats on each side, recursively, until a stopping rule fires.

The scoring function is `criterion` &mdash; gini or entropy for classification, squared error for regression. It is the parameter people reach for first and the one that matters least: the editor above shows the three classification criteria within half a point of each other, which is typical. Depth and leaf size are the parameters that change the model.

## What makes trees attractive

**They are readable.** `export_text` prints the entire model, and for a shallow tree that output is something a domain expert can check line by line. No other model in this track offers that. When somebody has to justify a decision &mdash; a loan refusal, a clinical flag &mdash; being able to point at the path a case took is worth a great deal.

**They need no preparation.** No scaling, because a split is a threshold on one column and units cannot affect which threshold is best. The last editor multiplies a column by a million and the cross-validated score does not move by a thousandth. No distributional assumptions, and outliers affect only the leaf they land in.

**They find structure without being told.** Interactions between features come for free, because a split lower in the tree is conditioned on every split above it. Non-linear boundaries come for free, because a staircase of thresholds approximates any shape. A linear model needs to be handed `x1 * x2` and `x**2` explicitly; a tree discovers both.

**They handle mixed data.** Numeric and categorical features side by side, no common scale needed.

## What makes one tree a poor final answer

**Left alone, it memorises.** The default stopping rule is to keep splitting until every leaf is pure, which on any dataset with noise means one leaf per training row. Training accuracy 1.0, and a lookup table. Every tree needs constraining, which is what `max_depth`, `min_samples_leaf` and `ccp_alpha` are for.

**It is unstable.** This is the deeper problem. The fourth editor takes six bootstrap resamples of the same data, fits a tree to each, and finds them disagreeing on 18 of 40 predictions &mdash; with the first split falling on a different feature in one of the six.

The cause is the greedy fitting. The best split is chosen at each node without regard to what comes below, and when two candidate splits score nearly the same, a handful of resampled rows decides between them. That choice then determines everything underneath, so a small change at the top rewrites the whole tree.

The consequence is that a single tree's structure should not be over-interpreted. "The model says petal width is the key variable" is a statement about one fit on one sample, and a different sample might have said something else.

**It cannot extrapolate.** A leaf predicts an average of training values, so beyond the range of the training data a tree returns a constant. The fifth editor fits a perfect straight line and asks for values past the end: the linear model gives 75 and 90, correctly, and the tree gives 54 for both. For anything with a trend &mdash; time, growth, prices &mdash; this is disqualifying on its own.

**Axis-aligned splits.** Each split is on one feature, so a diagonal boundary has to be approximated by a staircase. Trees handle it, inefficiently, and a linear model handles a diagonal exactly.

## Feature importances, and their bias

`feature_importances_` reports how much each feature reduced the impurity across all the splits it appears in, normalised to sum to 1. Features never split on get exactly zero, which is a genuinely useful signal &mdash; the editor above shows two of iris's four features unused.

Three cautions before trusting the numbers.

**Correlated features split the credit arbitrarily.** If two columns carry the same information, whichever is chosen first takes the importance and the other looks worthless. Neither is, and the split between them is not stable.

**High-cardinality features are favoured.** A column with many distinct values offers more candidate thresholds and so more chances to look good on the training data. This is the impurity-based measure's known bias, and it inflates the apparent importance of ids and continuous variables relative to binary ones.

**It is measured on the training data.** A feature that helped fit noise still scores.

`permutation_importance` avoids all three by measuring the drop in test-set score when a column is shuffled. It costs more and answers the question people actually mean.

## Constraining it

Four parameters, of which the middle two are usually the most useful.

`max_depth` caps the number of questions. Simple, blunt, and the first thing to try.

`min_samples_leaf` refuses to create a leaf with fewer than n samples. This is often better than depth, because it responds to the density of the data rather than imposing a fixed count &mdash; a tree can stay deep where there is data to support it.

`min_samples_split` is the related control on splitting rather than on the resulting leaves.

`ccp_alpha` grows the tree fully and then prunes back branches whose contribution does not justify their complexity. It is the most principled of the four, and the overfitting module found it giving the best test score of three constraints tried.

The right values are found by cross-validation, not chosen. The overfitting module also showed that a constraint can make things worse: `min_samples_leaf=20` lowered the test score on data where `max_depth=3` raised it.

## Where a single tree belongs

Rarely as the final model. A random forest or a gradient booster beats it on almost any dataset, and the next modules cover both.

It belongs when the model has to be explained &mdash; a shallow tree is a flowchart somebody can audit, and that is occasionally the requirement. It belongs as a fast baseline that tells you whether the problem has non-linear structure. And it belongs as the thing to understand first, because forests and boosting are both built out of trees, and their parameters are largely tree parameters.

## Categorical features, and the one that is missing

scikit-learn's `DecisionTreeClassifier` cannot take a string column. It requires numbers, which means categorical features have to be encoded before they reach it &mdash; and the choice of encoding interacts badly with how trees split.

One-hot encoding a category with twenty values gives the tree twenty binary columns, and a split on a binary column separates one category from the other nineteen. Isolating a group of three categories then takes three levels of depth, which the depth budget has to pay for. The tree can express it; it is just expensive.

Ordinal encoding gives one column and lets a single threshold separate a contiguous run of categories &mdash; but the run is contiguous in whatever arbitrary order the encoder chose, so the groups it can form cheaply are the wrong groups.

Neither is the native answer, which is to consider arbitrary subsets of categories at each split. `HistGradientBoostingClassifier` supports that through `categorical_features`, and it is a genuine reason to prefer it on data with many categories. LightGBM and CatBoost handle it too, and it is one of the things they are known for.

For a plain tree with a handful of categories, one-hot and enough depth is fine. For a high-cardinality column, it is a real limitation rather than a detail.

## Reading the structure programmatically

Beyond `export_text`, the fitted tree exposes its structure through `tree_`, and a few attributes answer useful questions directly.

`tree_.node_count` and `get_n_leaves()` say how large the model is. A leaf count approaching the number of training rows is the clearest signal of memorisation available, and it costs one call.

`tree_.feature` and `tree_.threshold` are arrays giving, per node, which feature was split on and at what value &mdash; which is how the instability demonstration above read the first split without parsing text.

`get_depth()` says how deep it actually grew, which is often less than `max_depth` when another constraint bound first.

`decision_path(X)` returns which nodes each sample passed through, which is the basis of any per-prediction explanation: for a given row, the path is the reason.

These matter because they turn "the tree looks complicated" into numbers. A tree with 300 leaves on 400 training rows does not need a diagnosis; the leaf count is the diagnosis.

<strong>Is gini or entropy better?</strong> Neither, in practice. They agree on almost every split and differ by a fraction of a point. Spend the effort on depth and leaf size.

<strong>Can a tree do regression?</strong> Yes - `DecisionTreeRegressor` predicts the mean of each leaf. The output is a step function, which is why it cannot extrapolate.

<strong>Should I prune or cap the depth?</strong> `ccp_alpha` prunes where pruning helps, rather than truncating everywhere at the same level. It usually does better, and it costs one more hyperparameter to tune.

<strong>Why is my tree different each run?</strong> Ties between equally good splits are broken randomly. `random_state` fixes it, and the fact that it matters is the instability in miniature.

## What "greedy" means, and why it matters

The fitting algorithm is greedy: at every node it picks the split that looks best *right now*, without considering what splits become available afterwards.

That is a real limitation rather than an implementation shortcut. Finding the genuinely optimal tree &mdash; the smallest one achieving a given accuracy &mdash; is computationally intractable for any realistic dataset, so every practical implementation is greedy. The consequence is that a tree can miss structure that requires two splits to reveal: if neither of a pair of features looks useful alone, but their combination separates the classes perfectly, the greedy step may never take the first one.

The classic example is exclusive-or. With two binary features where the answer is "one but not both", neither feature alone carries any information at all, so the first split scores nothing on either. A tree will eventually get there on real data with noise to guide it, and it takes more depth than the structure warrants.

This also explains the instability from the other direction. When two candidate splits score nearly identically, the greedy choice between them is decided by whichever is fractionally better on this particular sample &mdash; and everything below inherits that arbitrary decision.

Ensembles help here too, and not only by averaging. A random forest restricts each split to a random subset of features, which forces different trees to take different first steps and occasionally finds the structure a single greedy path would have missed.

## Things to try

1. <strong>Read the model.</strong> The first editor prints the whole thing. Raise the depth to 4 and watch it stop being readable.
2. <strong>Watch the instability.</strong> In the fourth editor, change `random_state` on the resampler and see how much the six trees disagree this time.
3. <strong>Confirm the flat line.</strong> In the fifth editor, ask for x=100. The tree still says 54.
4. <strong>Compare the importances.</strong> Fit at depth 1 and at depth 5 and see how the numbers redistribute.

## Where this leaves you

A model you can read, that needs no preparation, that finds interactions on its own, that memorises unless constrained, that changes when you resample, and that cannot see past the edge of its training data. The next two modules address the instability by using many of them at once.
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
