# -*- coding: utf-8 -*-
"""Content for the generated machine learning workflow modules.

Twenty-five modules and nearly all of them were an algorithm: KNN, SVM, PCA,
random forests, gradient boosting. The algorithms were not the gap. The gap was
everything around them - scaling, leakage, missing values, thresholds, tuning,
reading a learning curve - which is where real projects actually fail, and
which is hard to learn from a textbook because the failures are quiet. A leaky
pipeline does not raise an error. It reports a better number.

Every figure on these pages is computed in the browser from data generated in
the browser (assets/vizlearn-ml.js), so the reader can move a control and watch
the claim hold or break rather than being told it.
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
# 1. Feature scaling
# ---------------------------------------------------------------------------
topic(
    "feature_scaling",
    "Feature Scaling",
    "Preprocessing",
    "Two columns measured in different units, and a model that can only see "
    "the larger one. Switch the scaler and watch the accuracy move.",
    _svg(_axes()
         + "".join(_dot(30 + i * 9, 66 - (i % 3) * 3, M) for i in range(12))
         + _txt(84, 30, "income dominates", A, 9)
         + _txt(84, 44, "age is invisible", M, 8)),
    {
        "sim": "scaling",
        "controls": [
            {"key": "scaler", "label": "Scaler", "type": "select", "value": "none",
             "options": [{"value": "none", "label": "None (raw units)"},
                         {"value": "standard", "label": "StandardScaler"},
                         {"value": "minmax", "label": "MinMaxScaler"}]},
            {"key": "k", "label": "k (neighbours)", "type": "range",
             "min": 1, "max": 25, "step": 2, "value": 7},
        ],
    },
    [
        "Any model that measures <em>distance</em> is sensitive to units. "
        "k-NN, SVM with an RBF kernel, k-means and PCA all are.",
        "<code class='mono-font'>StandardScaler</code> subtracts the mean and "
        "divides by the standard deviation. Outliers survive it.",
        "<code class='mono-font'>MinMaxScaler</code> maps to [0, 1]. One extreme "
        "value squashes everything else into a corner.",
        "Trees do not care. A split asks whether a value exceeds a threshold, "
        "and that answer is unchanged by rescaling.",
    ],
    """
title: Feature Scaling
intro: Why a column measured in pounds drowns out a column measured in years, and which models care.

## The problem is the units

The data here has two columns: age, spanning roughly 25 to 55, and income,
spanning roughly 20,000 to 70,000. They show a person about equally well.

Set the scaler to None and look at the readout. The income range is around a
thousand times the age range. Now consider what k-NN does &mdash; it finds the
nearest points by Euclidean distance:

```
distance^2 = (age1 - age2)^2 + (income1 - income2)^2
```

A ten-year age difference adds 100 to that sum. A ten-pound income
difference adds 100 as well. A five-thousand-pound difference adds
twenty-five million.

The age term isn't merely less key. It's by number irrelevant: any
plausible age difference is lost in the rounding of the income term. The model
is in effect one-dimensional, and no one asked for that.

## What the scalers do

Switch to **StandardScaler**. Each column has its mean subtracted and is cut
by its standard deviation, so both end up centred on 0 with a spread of about 1.
The scatter turns roughly circular, both columns contribute comparably, and
the fit in the readout moves.

```
z = (x - mean) / std
```

Switch to **MinMaxScaler**. Each column is mapped onto [0, 1] using its min
and max:

```
x' = (x - min) / (max - min)
```

Both fix the units problem. They differ in how they handle extremes, and that is
the basis for choosing.

| | StandardScaler | MinMaxScaler |
|---|---|---|
| Output range | unbounded, roughly &minus;3 to 3 | exactly [0, 1] |
| Uses | mean, standard deviation | minimum, maximum |
| One extreme value | shifts the mean a little | compresses everything else |
| Good for | most things, especially with outliers | bounded inputs, image pixels, neural nets |

MinMax's weakness is worth stating plainly. Both statistics it uses are the most
outlier-sensitive numbers available. One salary of ten million maps to 1.0 and
crushes each real salary into the bottom half of a per cent of the range.

## Which models care

**Sensitive**, because they measure distance or magnitude:

- k-NN and k-means &mdash; distance is the entire method
- SVM with an RBF or polynomial kernel. The kernel is a distance
- PCA &mdash; it finds directions of max variance, and unscaled variance is
  dominated by whichever column has the biggest units
- Neural networks &mdash; not for correctness. But Grads on wildly different
  scales make optimisation slow and unstable
- Ridge and Lasso &mdash; the fine is on coeff size, and coeff
  size depends on the units of its column

**Not sensitive:**

- choice trees, random forests, grad boosting

That last group surprises people, and the reason is worth having. A tree split
asks `is income > 45000`. Rescale the column and the question turns
`is income' > 0.53`. This Splits the rows into just the same two groups.
Any monotonic change leaves each possible split unchanged, so the tree
is the same. Scaling before a random forest isn't wrong. It's simply a
no-op.

## The rule that matters more than the choice

Fit the scaler on the **training data only**, then apply it to the test data
without refitting.

The mean and standard deviation are learned params. finding them from the
whole dataset lets info about the test set reach the model before it's
tested, and the reported score stops being an guess of any of it. That is
[data leakage](data_leakage.html), it's the most common serious mistake in
applied machine learning, and it's why scalers belong inside a
[pipeline](ml_pipelines.html) rather than being applied by hand.

## Standardising, and why trees do not care

The fix is one formula applied per column, `z = (x - mean) / std`, and working it
shows why some models transform fully and others not at all. Age spanning
25-55 and income spanning 20,000-70,000, standardised:

|raw|z-score|
|---|---|
|age 30 (mean 40, sd 10)|&minus;1.0|
|age 55|+1.5|
|income 25,000 (mean 45k, sd 15k)|&minus;1.3|
|income 70,000|+1.7|

Both columns now live on the same &minus;3-to-3 scale. A year of age and a
standard-deviation of income count comparably in a Euclidean distance &mdash; where
before, the income term's raw spread of 50,000 against age's 30 made age
by number invisible to k-NN, k-means, SVM-RBF and PCA. A choice tree, by
contrast, is fully unmoved: its split asks `is income > 45000`, which after
scaling turns `is income' > 0.53`, and that splits the rows into just the
same two groups. Any monotonic rescaling leaves each possible split unchanged, so
scaling before a random forest is a genuine no-op. Not wrong, just wasted
effort &mdash; while for the distance-based models it's the difference between a
usable model and a one-dimensional one.

The choice between the two common scalers comes down to outliers. StandardScaler
uses the mean and standard deviation. So One extreme value shifts the centre only a
little. MinMaxScaler uses the min and max, the two most outlier-sensitive
numbers there are, so a single salary of ten million maps to 1.0 and crushes each
real salary into the bottom fraction of a per cent of the range. StandardScaler is
the safer default for most data, MinMax suits truly bounded inputs like image
pixels. One thing neither should touch is a one-hot column: it's already 0 and 1,
and standardising it turns two real values into two any ones for no
gain.

And if you scale the target and the features, note to invert the
transform on the guesses, or the error metric comes back in scaled units and
means nothing &mdash; a small bookkeeping step that is easy to forget and quietly
corrupts each reported number.

## Where it goes wrong

**Fitting the scaler on all.** The number you report goes up and the
model doesn't get better.

**Scaling the target variable and losing to invert it.** guesses come
back in scaled units and the error metric is meaningless.

**MinMax on data with outliers.** The real data ends up in a sliver of the
range.

**Scaling one-hot columns.** They're already 0 and 1. StandardScaler turns them
into two any values and makes the model harder to read for no gain.

## Questions people ask

<strong>Which models need feature scaling?</strong> Distance-based and gradient-based models such as k-NN, SVMs, k-means, PCA, neural networks and regularised linear models. Tree-based models do not care.

<strong>Standardisation or min-max?</strong> Standardisation is the safer default, particularly with outliers. Min-max suits bounded inputs, like pixel values, and models that expect a fixed range.

<strong>Should I scale the target too?</strong> Usually not for classification. For regression it can help some models, but you must invert the predictions before computing errors.

<strong>When do I fit the scaler?</strong> On the training data only, then apply it to validation and test data. Fitting on everything leaks test statistics into training.

<strong>Do I scale one-hot columns?</strong> No. They are already 0 or 1, and scaling them makes coefficients harder to read with no gain.

<strong>What if my data has big outliers?</strong> Min-max will squeeze most values into a sliver of the range. Use the median-and-IQR scaler, or clip or transform the feature first.

## Which models care, and which do not

One dataset, one column rescaled by 10,000, five models. Two collapse, two don't move at all. The fifth is the notable case.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = make_classification(n_samples=1500, n_features=8, n_informative=4,
                           random_state=0)
X_big = X.copy()
X_big[:, 0] *= 10_000
print("column 0 now has sd %.0f; the rest are near 1.0" % X_big[:, 0].std())
print()
print("%-24s %12s %12s %10s" % ("model", "raw", "scaled", "change"))
for name, mk in (("k-nearest neighbours", lambda: KNeighborsClassifier()),
                 ("SVM (rbf)",            lambda: SVC()),
                 ("logistic regression",  lambda: LogisticRegression(max_iter=5000)),
                 ("decision tree",        lambda: DecisionTreeClassifier(random_state=0)),
                 ("random forest",        lambda: RandomForestClassifier(n_estimators=100,
                                                                         random_state=0))):
    raw = cross_val_score(mk(), X_big, y, cv=5).mean()
    scaled = cross_val_score(make_pipeline(StandardScaler(), mk()),
                             X_big, y, cv=5).mean()
    print("%-24s %12.4f %12.4f %+10.4f" % (name, raw, scaled, scaled - raw))
print()
print("distance-based models collapse. KNN and the rbf SVM both compute")
print("||a - b||, and one column that is 10,000x larger IS the distance --")
print("the other seven columns stop counting.")
print()
print("trees split one column at a time and never compare across columns,")
print("so a change of unit is invisible to them. that is exact, not approximate.")
```

The next block shows how scaling changes the coefficients of logistic regression, and how the three common scalers handle a column with one outlier.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

X, y = make_classification(n_samples=1500, n_features=8, n_informative=4,
                           random_state=0)
X_big = X.copy()
X_big[:, 0] *= 10_000
raw_c = LogisticRegression(max_iter=5000).fit(X_big, y).coef_[0]
sc_c = LogisticRegression(max_iter=5000).fit(StandardScaler().fit_transform(X_big), y).coef_[0]
print("logistic regression barely lost accuracy, but look at the coefficients:")
print("  unscaled:", np.round(raw_c[:4], 6), "...")
print("  scaled:  ", np.round(sc_c[:4], 6), "...")
print("the first coefficient is %.0fx smaller just to undo the unit."
      % (abs(sc_c[0]) / abs(raw_c[0])))
print("the L2 penalty charges by coefficient size, so it is now charging")
print("that column almost nothing and the rest full price.")
print()
col = np.concatenate([np.random.default_rng(0).normal(50, 5, 200),
                      [400.0]]).reshape(-1, 1)
print("the three scalers, on a column with one outlier:")
for name, sc in (("StandardScaler", StandardScaler()),
                 ("MinMaxScaler",   MinMaxScaler()),
                 ("RobustScaler",   RobustScaler())):
    out = sc.fit_transform(col).ravel()
    print("  %-15s normal rows in [%7.3f, %7.3f], outlier at %8.3f"
          % (name, out[:200].min(), out[:200].max(), out[-1]))
print()
print("MinMaxScaler squeezes every real row into 6%% of its range because one")
print("point defines the other end. RobustScaler uses the median and IQR,")
print("so a single extreme value does not distort the rest.")
print()
print("and always fit the scaler inside a pipeline -- fitting it on all the data")
print("before splitting leaks the test set's mean and sd into training.")
```

""",
    [
        {"q": "Why is k-NN affected by feature scaling but a decision tree is not?",
         "options": ["Trees ignore numeric columns",
                     "k-NN sums squared differences, so the larger-scaled column dominates; a tree's splits are unchanged by any monotonic rescaling",
                     "Trees scale internally",
                     "k-NN requires normalised inputs to run"],
         "answer": 1,
         "why": "Rescaling changes `income > 45000` into `income' > 0.53`, which partitions exactly the same rows. Distance, by contrast, is dominated by whichever column has the biggest numbers."},
        {"q": "What is MinMaxScaler's main weakness compared with StandardScaler?",
         "options": ["It is slower",
                     "It uses the minimum and maximum, so one extreme value compresses all the real data",
                     "It cannot handle negative numbers",
                     "It changes the shape of the distribution"],
         "answer": 1,
         "why": "Min and max are the two most outlier-sensitive statistics there are. One salary of ten million maps to 1.0 and pushes every real salary into a sliver at the bottom."},
        {"q": "Where must a scaler's mean and standard deviation come from?",
         "options": ["The whole dataset", "The training data only",
                     "The test data", "A standard reference table"],
         "answer": 1,
         "why": "They are learned parameters. Computing them across everything lets test-set information reach the model before evaluation, and the reported score stops estimating anything."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Data leakage
# ---------------------------------------------------------------------------
topic(
    "data_leakage",
    "Data Leakage",
    "Preprocessing",
    "Fit the scaler before the split and the accuracy goes up. Nothing got "
    "better; the number just stopped meaning anything.",
    _svg(_box(14, 26, 56, 26, fill=S) + _txt(42, 42, "train", M, 9)
         + _box(90, 26, 56, 26, fill=S) + _txt(118, 42, "test", M, 9)
         + _line(70, 39, 90, 39, A, 1.6, "4 3")
         + _txt(80, 70, "statistics crossing the line", A, 8)),
    {
        "sim": "leakage",
        "controls": [
            {"key": "order", "label": "When features are selected", "type": "select",
             "value": "leaky",
             "options": [{"value": "leaky", "label": "Once, on the whole dataset (leaky)"},
                         {"value": "correct", "label": "Inside each fold (correct)"}]},
            {"key": "features", "label": "Columns of noise to choose from",
             "type": "range", "min": 40, "max": 600, "step": 20, "value": 400},
        ],
        "captions": ["Reported accuracy against the truth"],
    },
    [
        "Leakage is any path by which information about the evaluation data "
        "reaches the model before it is evaluated.",
        "It never raises an error. The only symptom is a score that is better "
        "than it should be, which nobody investigates.",
        "The commonest form is fitting a preprocessing step on the whole "
        "dataset. The mean and standard deviation are learned parameters.",
        "The second commonest is a feature that could not exist at prediction "
        "time &mdash; a field filled in after the outcome was known.",
    ],
    """
title: Data Leakage
intro: The mistake that makes your model look better and your results worthless.

## What it is

Leakage is any route by which info about the data you're testing on
reaches the model before the test. The model then answers a question it
was quietly shown the answer to, and the score you report measures nothing you
can act on.

It has no error message. Nothing crashes, nothing warns, and the only symptom is
that the number is better than you expected. Which isn't a symptom
anyone investigates.

## Watch it happen, on data with nothing in it

The dataset behind the chart is 300 rows and a few hundred columns of pure
noise. The labels are assigned on its own of each column. There's no signal
whatsoever, and the only honest score is 50%.

Set the control to **Once, dataset**. Five columns are picked by
correlating each one with the label across all 300 rows, and only then is the
data cross-validated. The reported fit is well above 50%, on data that
holds nothing.

Now set it to **Inside each fold**. The pick is redone within each fold's
training rows, and the reported fit falls back to chance &mdash; 
slightly below it, which is worth a sentence of its own further down.

Drag the number of columns up. The inflation grows: 40 pick columns buy a
few points, 600 buy a lot more. With more columns to search there's
always some that correlate with the labels by chance, and the pick was
allowed to see the labels of the rows it was later tested on.

Nothing about the model changed between those two settings. The only difference
is whether the rows being scored had a say in which columns were used.

## Why the honest number lands below 50%

The correct setting reports a thing like 45%, not 50%, and that isn't a bug
in the demo.

A column is chosen inside a fold because it happened to separate the classes in
those training rows. On pure noise that gap is fully accidental, and
an accident large enough to win a search over hundreds of columns is an extreme
one. Extremes regress: on the held-out rows, that column is as likely to lean
the other way as this way, and the centroid built from the training rows then
points slightly the wrong direction.

So selecting features on noise doesn't merely fail to help. It can actively
mislead, and a model built on selected noise can score worse than one that
skips the data fully. That is worth knowing on its own, and it's the
strongest available arg for checking whether a feature-pick step is
earning its place.

## Why a scaler counts as a model

The instinct that makes this feel harmless is that scaling is "just
prep". But `StandardScaler` has params &mdash; a mean and a
standard deviation &mdash; and it *learns* them from data. any of it that learns
params from data must learn them from training data only.

The same arg applies to each step that looks at the data as a whole:

- imputing missing values with a column mean
- selecting the top *k* features by link with the target
- fitting a PCA rotation
- learning target encodings for cat columns
- finding TF-IDF weights
- resampling to balance classes

each one of those is fitted, and each one leaks if fitted before the split.

They don't leak equally, and it's worth being straight about that. A scaler
fitted on a few hundred well-behaved rows leaks a real but tiny amount: the mean
barely moves when you add the validation rows to it, and the reported score may
shift by a fraction of a per cent. Feature pick leaks enormously, which is
why it's the demo above. The scaler case still matters, because a
fraction of a per cent is enough to change which of two models you ship, and
because the habit that blocks one blocks the other.

## The other kind

The second family has nothing to do with order of ops. It's a feature
that couldn't exist at guess time.

A model predicting whether a customer will churn, trained on a table that
includes `cancellation_reason`. A model predicting loan default with a column
for `recovery_amount`. A medical model given a field that is only filled in once
a diagnosis has been made.

These are obvious when written out and very hard to spot in a warehouse table
with three hundred columns, most of them undocumented. The diagnostic question
isn't "is this related to the target" but **"would this value be present, and
correct, at the moment I need a guess?"**

A near-perfect score is the strongest evidence of leakage there's. If a model
reports 99% on a problem people find hard, the correct first response is
suspicion, not celebration.

## Leakage across time and groups

Two subtler cases are worth naming.

**Time.** A random split of time-series data puts future rows in the training
set and past rows in the test set. The model is asked to predict backwards
after being shown what happened. Split by time, always.

**Groups.** If one patient adds ten scans, a random split scatters them
across train and test. The model can recognise the patient rather than the
rule, and the score reflects that. Split by group.

## The fix

Put each fitted step inside a [pipeline](ml_pipelines.html) and cross-validate
the pipeline, not the model. Then each fold fits its own scaler, its own imputer
and its own feature pick on that fold's training portion, which is just
what you'd have to do in production.

This isn't a stylistic preference. It's the only setup in which the
order of ops can't be got wrong by accident.

## Where it goes wrong

**Scaling or imputing before `train_test_split`.** The commonest form.

**Selecting features on the full dataset.** makes plausible scores from noise.

**Random splits on time series or grouped data.**

**Believing a oddly good result.** It's nearly always leakage, and
finding out later is much more costly than checking now.

## Questions people ask

<strong>What is data leakage in plain terms?</strong> Information from outside the training set, usually from the test set or the future, sneaks into model fitting. The score looks great and then collapses in production.

<strong>How do I spot leakage?</strong> Be suspicious of scores that are too good to be true, or a single feature with huge importance. Check whether any feature would not be available at prediction time.

<strong>Is fitting a scaler before splitting really leakage?</strong> Yes. The scaler learns the mean and variance of the test rows, so the test set influences training. The effect is often small but it is still a leak, and it can be large for other steps like feature selection.

<strong>Does cross-validation prevent leakage?</strong> Only if every learned step runs inside each fold. Wrap preprocessing and the model in a pipeline so each fold fits its own transforms.

<strong>What is target leakage?</strong> A feature that encodes the answer, such as a refund flag when predicting whether a customer churns. It carries the label because it is recorded after the outcome.

<strong>How does time cause leakage?</strong> Random splits let the model train on rows from after the ones it is tested on. Use time-ordered splits, and group splits when rows from one entity repeat.

## A model that scores well and knows nothing

Select features using the whole dataset, then cross-validate. The score is great and fully fake. The data is pure noise.

```python-run
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(0)
# 3000 columns of noise, a coin-flip label. there is nothing to learn here.
X = rng.normal(size=(180, 3000))
y = rng.integers(0, 2, 180)
print("data: %d rows, %d columns, all noise. the label is a coin flip." % X.shape)
print("an honest model cannot beat 0.5.")
print()

# the wrong way: choose the 20 best columns using every row, then score
picked = SelectKBest(f_classif, k=20).fit(X, y).get_support()
leaked = cross_val_score(LogisticRegression(max_iter=2000), X[:, picked], y,
                         cv=StratifiedKFold(5, shuffle=True, random_state=0))
print("selecting features on the full dataset, then cross-validating:")
print("  fold scores", np.round(leaked, 4))
print("  mean %.4f   <- from noise" % leaked.mean())
print()

# the right way: selection happens inside each fold, on training rows only
pipe = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=2000))
honest = cross_val_score(pipe, X, y, cv=StratifiedKFold(5, shuffle=True,
                                                        random_state=0))
print("selecting inside the pipeline, so each fold only sees its own training rows:")
print("  fold scores", np.round(honest, 4))
print("  mean %.4f   <- the truth" % honest.mean())
print()
print("the gap is %.3f of pure illusion." % (leaked.mean() - honest.mean()))
print()
print("the leak: the selector looked at test-fold labels when choosing columns,")
print("so the 20 'best' columns were the ones that happened to correlate with")
print("the very rows the model was about to be scored on.")
print()
print("this is why every fit-like step belongs inside the pipeline. scalers,")
print("imputers, encoders and selectors all learn from data, and all of them")
print("leak if they learn from rows that are supposed to be unseen.")
```

""",
    [
        {"q": "Why does fitting a StandardScaler before the train/test split count as leakage?",
         "options": ["It slows training down",
                     "The mean and standard deviation are learned parameters, so test rows influence what the model sees",
                     "It changes the test labels",
                     "It only matters for k-NN"],
         "answer": 1,
         "why": "Anything that learns parameters from data must learn them from training data only. Otherwise the reported score stops being an estimate of performance on unseen data."},
        {"q": "What is the right question to ask about a suspicious feature?",
         "options": ["Is it correlated with the target?",
                     "Would this value be present and correct at the moment a prediction is needed?",
                     "Is it numeric or categorical?",
                     "Does removing it hurt the score?"],
         "answer": 1,
         "why": "A cancellation reason correlates beautifully with churn and does not exist before the customer churns. Correlation is exactly what makes leaked features look valuable."},
        {"q": "Why does a random split leak on time-series data?",
         "options": ["The rows are correlated",
                     "Future rows land in training and past rows in test, so the model predicts backwards after seeing what happened",
                     "Time cannot be a feature",
                     "The test set becomes too small"],
         "answer": 1,
         "why": "Production always predicts forward from the past. A random split evaluates a situation that can never occur, so the score does not describe the deployed system."},
    ],
)


# ---------------------------------------------------------------------------
# 3. Handling missing values
# ---------------------------------------------------------------------------
topic(
    "handling_missing_values",
    "Handling Missing Values",
    "Preprocessing",
    "Drop them, fill them with the mean, fill them with the median &mdash; and "
    "watch what each choice does to the distribution it came from.",
    _svg(_axes()
         + "".join(_box(26 + i * 13, 70 - h, 9, h, fill=(S if i != 3 else "none"),
                        stroke=(B if i != 3 else A), sw=1)
                   for i, h in enumerate([8, 20, 34, 30, 18, 9, 4, 2]))
         + _txt(84, 24, "the hole, and what fills it", A, 8)),
    {
        "sim": "missing",
        "controls": [
            {"key": "strategy", "label": "Strategy", "type": "select", "value": "drop",
             "options": [{"value": "drop", "label": "Drop the rows"},
                         {"value": "mean", "label": "Fill with the mean"},
                         {"value": "median", "label": "Fill with the median"},
                         {"value": "indicator", "label": "Median + missing indicator"}]},
        ],
        "captions": ["Grey: the values that existed. Orange: what you are left with."],
    },
    [
        "The first question is never which strategy. It is <em>why</em> the "
        "values are missing.",
        "Mean or median imputation puts a spike at one value, which shrinks the "
        "variance and weakens every correlation the column had.",
        "Dropping rows is only safe when the missingness is unrelated to "
        "anything you care about. It rarely is.",
        "A missing-value indicator column keeps the fact that it was missing, "
        "which is often the most predictive thing about it.",
    ],
    """
title: Handling Missing Values
intro: Four strategies, and why choosing between them starts with a question about the world rather than about the data.

## Why, before what

each tutorial answers "what do I do about NaN". The question that decides the
answer is **why the value is absent**, and there are three cases with three
different consequences.

**Missing fully at random.** The lack has nothing to do with any of it.
A form field lost to a transmission error. This is the harmless case, and it's
rare.

**Missing at random.** The lack depends on other columns you've. Younger
respondents skip the income question more often, and you've their age. This is
recoverable, because the info needed to model the lack is present.

**Missing not at random.** The lack depends on the missing value itself.
High earners decline to state their income. This is the hard case, and it's
also the common one.

The data in the visualisation is on purpose the third kind: the largest values
are the ones that failed. Look at the two histograms. The grey spread is
what existed. The orange one is what each strategy leaves you with.

## Drop the rows

Select **Drop**. The right tail is gone, and the mean in the readout has fallen
well below the true mean.

Nothing about dropping is wrong in principle. It's unbiased when the values are
missing fully at random, and with a handful of affected rows out of many it
is a just right reasonable choice.

Here it's a disaster, because the rows removed aren't a random sample &mdash;
they're the large ones. each statistic found afterwards shows a
group that excludes them.

The other cost is math. Dropping any row with any missing value across ten
columns each 5% missing drops about 40% of the data, though 95% of each
single column is present.

## Fill with the mean, or the median

Select **Mean**, then **Median**. Both put a spike at a single value in the
middle of the spread, and both leave the mean below the truth.

They differ in strength. The mean is dragged by extreme values. The median is
not. For a skewed column. Income, house prices, time-to-event &mdash; the
median is the better default, and for a roughly even column the two are
close enough that it rarely matters.

What neither can do is invent info. Imputation makes the dataset
rectangular so the model will accept it. It doesn't restore what was lost, and
it adds two distortions worth knowing:

- **Variance shrinks.** A pile of the same values has none.
- **Links weaken.** The imputed rows carry no tie to any other
  column, so they dilute each tie the column really had.

## Keep the fact that it was missing

Select **Median + indicator**. The imputation is the same. What changes is that
a second column is added, holding 1 where the value was missing and 0 or else.

This is often the best simple answer, because in the third case &mdash;
missing not at random &mdash; **the lack is itself helpful**. If high
earners decline to answer, then "declined to answer" predicts high earnings, and
plain imputation throws that signal away while an indicator preserves it.

It costs one column and no assumptions. It's hard to do worse than the
options with it.

| Strategy | Keeps rows | Keeps distribution | Keeps the signal in absence |
|---|---|---|---|
| Drop | no | only if MCAR | no |
| Mean | yes | no, spike at centre | no |
| Median | yes | no, spike at centre | no |
| Median + indicator | yes | no | **yes** |
| Model-based (kNN, MICE) | yes | better | only with an indicator |

## More sophisticated options

**k-NN imputation** fills a value from similar rows. **MICE** models each column
from the others, iteratively. Both preserve ties better than a constant
and both cost far more work, and both must be fitted on training data
only &mdash; they're models, so imputing before the split is
[leakage](data_leakage.html).

Also worth knowing: some models handle missing values natively. LightGBM and
XGBoost learn a default direction at each split for rows whose value is absent,
which is often better than any of it you'd impute by hand.

## Why "why" changes the answer

The strategy matters far less than the reason the value is absent, and the same
30%-missing column shows it. When the missing values are the *largest* ones
(missing not at random &mdash; high earners decline to state income), each method
that skips the lack inherits the bias:

|values 1-100, top 30 missing|resulting mean|
|---|---|
|true mean|50.5|
|after dropping the missing rows|35.5|
|after mean/median imputation|~35.5 (a spike at the low centre)|

Dropping or filling both land near 35.5, understating the truth by fifteen, because
the rows removed or flattened are just the high ones. No math on the
values that remain can recover values that were never seen. The one strategy that
helps adds a *missingness indicator*: a second column marking which rows were
absent. In the not-at-random case the lack is itself the signal &mdash; "declined
to answer" predicts high income. So keeping that flag lets the model use what
plain imputation throws away. It costs one column and no assumptions. And dropping
carries a second, math cost: with ten columns each 5% missing,
`1 - 0.95^10 = 40%` of rows have *some* gap. Row-dropping discards 40% of the
data though 95% of each column is present.

## Where it goes wrong

**Imputing before the split.** The column mean is found from the test rows
too.

**Filling with zero without thinking.** Zero is a real value in most columns. A
temperature of zero isn't a missing temperature.

**Dropping rows across many columns at once.** A little missingness all over
drops a lot of data.

**Never checking why.** Ten minutes finding out what caused the gap is worth
more than any choice of strategy.

## Questions people ask

<strong>Should I just drop rows with missing values?</strong> Only when few rows are affected and the values are missing at random. Otherwise you lose data and can bias the sample.

<strong>Mean or median imputation?</strong> Median is safer with skewed data or outliers. Mean is fine for symmetric distributions.

<strong>Why add a missing-value indicator?</strong> The fact that a value is absent often carries signal, such as an unreported income. A binary flag lets the model use that.

<strong>Do I impute before or after splitting?</strong> After. Learn the fill values from the training set only, ideally inside a pipeline, to avoid leakage.

<strong>When should I use model-based imputation?</strong> When many features are missing and related to each other. KNN or iterative imputation can recover the relationships, at higher cost and with more risk of leakage.

<strong>Which models handle missing values natively?</strong> Gradient-boosted trees like HistGradientBoosting, XGBoost and LightGBM do. Most linear models, SVMs and neural networks need imputation first.

## Dropping, filling, and the flag that saves you

Whether a gap can be safely filled depends fully on WHY it's missing. Two datasets with the same 30% hole rate. Only one of them is fixable by imputation.

```python-run
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(0)
n = 700
X = rng.normal(size=(n, 6))
y = 5 * X[:, 0] + 2 * X[:, 1] - X[:, 2] + rng.normal(0, 2.0, n)
print("feature 0 is the dominant predictor. with no gaps at all: R2 %.4f"
      % cross_val_score(Ridge(), X, y, cv=5).mean())
print()
print("CASE 1 -- missing completely at random (a sensor dropped packets).")
Xa = X.copy()
Xa[rng.random(Xa.shape) < 0.30] = np.nan
keep = ~np.isnan(Xa).any(axis=1)
print("  30%% of cells gone, which costs %d of the %d rows entirely."
      % (n - keep.sum(), n))
print("  drop incomplete rows : R2 %7.4f  (on %d rows)"
      % (cross_val_score(Ridge(), Xa[keep], y[keep], cv=5).mean(), keep.sum()))
for name, imp in (("fill with mean  ", SimpleImputer(strategy="mean")),
                  ("fill with median", SimpleImputer(strategy="median")),
                  ("k-NN imputer    ", KNNImputer(n_neighbors=5))):
    print("  %s : R2 %7.4f"
          % (name, cross_val_score(make_pipeline(imp, Ridge()), Xa, y, cv=5).mean()))
print("  HistGradientBoosting : R2 %7.4f   <- takes NaN directly"
      % cross_val_score(HistGradientBoostingRegressor(random_state=0),
                        Xa, y, cv=5).mean())
print()
print("  dropping rows is not WRONG here -- the surviving rows are a fair")
print("  sample. it is just wasteful, and it gets worse as columns multiply:")
for cols in (6, 12, 25, 50):
    print("     %2d columns at 30%% missing -> %.1f%% of rows survive intact"
          % (cols, 100 * 0.7 ** cols))
```

The next block shows what happens when the data is missing for a reason, and why a missing-value indicator flag is the only thing that recovers the lost signal.

```python-run
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(0)
n = 700
X = rng.normal(size=(n, 6))
y = 5 * X[:, 0] + 2 * X[:, 1] - X[:, 2] + rng.normal(0, 2.0, n)
print("CASE 2 -- missing for a reason (high earners skip the income question).")
Xb = X.copy()
hide = X[:, 0] > np.percentile(X[:, 0], 65)
Xb[hide, 0] = np.nan
print("  feature 0 is missing on exactly the %d rows where it is high." % hide.sum())
print("  mean of the values that survived: %7.4f" % np.nanmean(Xb[:, 0]))
print("  mean of the values that vanished: %7.4f" % X[hide, 0].mean())
print("  imputation fills the first number into rows that deserve the second.")
print()
print("  drop incomplete rows  : R2 %7.4f  (on %d rows, all low earners)"
      % (cross_val_score(Ridge(), X[~hide], y[~hide], cv=5).mean(), (~hide).sum()))
print("  mean imputation       : R2 %7.4f"
      % cross_val_score(make_pipeline(SimpleImputer(), Ridge()), Xb, y, cv=5).mean())
flag = np.column_stack([Xb, np.isnan(Xb[:, 0]).astype(float)])
print("  plus a was-missing flag: R2 %7.4f"
      % cross_val_score(make_pipeline(SimpleImputer(), Ridge()), flag, y, cv=5).mean())
print()
print("  the flag is the only thing that lets the model say 'this row is one")
print("  of the hidden ones'. the gap itself carried information, and filling")
print("  it in without a flag throws that information away.")
print("  SimpleImputer(add_indicator=True) adds those columns for you.")
print()
print("so the order of operations is: ask why it is missing, then choose. and")
print("whatever you choose, put it inside the pipeline -- an imputer fitted on")
print("the full dataset has already read the test rows.")
```

""",
    [
        {"q": "What does 'missing not at random' mean?",
         "options": ["The values were lost by a bug",
                     "Whether a value is absent depends on the value itself, such as high earners declining to state income",
                     "The missing rows are scattered evenly",
                     "The column has no default"],
         "answer": 1,
         "why": "It is the hard case and the common one: dropping such rows removes a biased sample, and imputing a central value pulls every statistic toward the middle."},
        {"q": "Why does mean imputation weaken a column's correlations?",
         "options": ["It changes the units",
                     "The imputed rows all carry the same value and no relationship to other columns, diluting the real relationship",
                     "It introduces outliers",
                     "It removes the column's variance entirely"],
         "answer": 1,
         "why": "A pile of identical values has no variance and no covariance with anything, so it drags every measured relationship toward zero."},
        {"q": "Why add a missing-value indicator column?",
         "options": ["To make the imputation reversible",
                     "Because the fact that a value was absent is often predictive in itself",
                     "It is required by scikit-learn",
                     "It speeds up training"],
         "answer": 1,
         "why": "When absence depends on the value - high earners declining to answer - 'declined to answer' predicts the answer. Plain imputation throws that away for free."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Outliers
# ---------------------------------------------------------------------------
topic(
    "outliers_and_influence",
    "Outliers and Influence",
    "Preprocessing",
    "Drag one point around and watch a least-squares line follow it. Twenty-"
    "four rows say one thing; the twenty-fifth overrules them.",
    _svg(_axes()
         + "".join(_dot(30 + i * 11, 64 - i * 4, M) for i in range(9))
         + _dot(132, 24, A, 4)
         + _line(24, 68, 146, 30, B, 1.2, "4 3")
         + _line(24, 66, 146, 22, A, 1.6)),
    {
        "sim": "outliers",
        "drag": {"xr": [0, 11], "yr": [-4, 26], "xKey": "ox", "yKey": "oy"},
        "controls": [],
        "fixed": {"ox": 9.5, "oy": 22},
        "captions": ["Dashed: the fit without the highlighted point. Solid: with it."],
    },
    [
        "Least squares minimises <em>squared</em> error, so a point twice as far "
        "off pulls four times as hard.",
        "An outlier far along the x axis has high <strong>leverage</strong>: it "
        "sits at the end of the lever and moves the line most.",
        "A point can be extreme and correct. Deleting it because it is "
        "inconvenient is how findings stop being true.",
        "Trees, medians and quantile regression are robust to outliers. Means, "
        "least squares and standard deviations are not.",
    ],
    """
title: Outliers and Influence
intro: One row out of twenty-five, and the reason it can decide your answer.

## Drag it

The chart holds twenty-four points along a clear upward line, plus one
highlighted point you can move. The dashed line is the least-squares fit without
it. The solid line is the fit with it.

Drag the point straight up. The solid line rotates. Drag it to the far right and
up, and the line follows it much further. The readout reports both slopes and
the percentage difference between them, and it doesn't take much to change the
answer by tens of per cent.

Twenty-four rows are saying one thing. The twenty-fifth overrules them.

## Why squaring does this

Least squares chooses the line cutting the **sum of squared** residuals.
Squaring is what makes a single point so powerful: a point twice as far from the
line adds four times the fine, and one ten times as far adds a
hundred times.

The fit is so willing to move a long way to reduce one large residual,
even at the cost of small grows across every other point. That isn't a bug
in the setup. It's what the goal function asks for.

## Hat values: where it sits matters as much as how far off it is

Drag the point up while keeping it near the middle of the x range, then drag it
up while keeping it at the far right. The second spot moves the line much
more.

That difference is the **hat value**. A regression line pivots roughly about the
mean of x, so a point near that mean is close to the pivot and has little turning
effect no matter how far off it is vertically. A point at the extreme of x sits
at the end of a long lever.

The gap is worth having in three words:

- **Outlier** &mdash; unusual in y, a large residual.
- **High hat value** &mdash; unusual in x, far from the pivot.
- **Influential** &mdash; both, so dropping it changes the model. This is the
  one that matters, and Cook's distance is the standard way to measure it.

A point with a high hat value that happens to lie on the trend is harmless. A
moderate outlier in the middle is harmless. The combination isn't.

## Before you remove anything

The temptation is to delete the point. Resist it long enough to ask which of
three things it's.

**An error.** A misplaced decimal, a sensor fault, a unit mix-up, a placeholder
like 999 or &minus;1 meaning "unknown". Fix it or drop it, and record that you
did.

**A different group.** The row is correct but doesn't belong to the
question &mdash; a wholesale order in a table of retail purchases. Exclude it and
say so, or model the groups apart.

**A real, extreme member of the group.** The row is correct and belongs.
This one you keep. Dropping genuine extremes because they're inconvenient is
how a result stops showing the world, and it's much more common than
deliberate fraud.

If you can't tell which, report the analysis both ways. A conclusion that
lives the point and a conclusion that depends on it are different findings,
and the reader is entitled to know which they've.

## Ways to be less fragile

**Solid loss.** Huber loss is squared for small residuals and linear for large
ones, so a distant point pulls hard but not as n&sup2; hard. RANSAC fits on
random subsets and keeps the consensus.

**Quantile regression.** Models the median rather than the mean, and the median
doesn't move when one point is dragged to infinity.

**Winsorising.** Clip values at, say, the 1st and 99th percentiles. Keeps the
row, caps its sway.

**Use a model that doesn't care.** Trees split on order, not on distance, so
a value of a million and a value of a thousand are the same split if nothing
lies between them.

**Transform.** A log transform on a skewed plus column often turns
"outliers" into plain members of a normal-shaped spread, which is
often a sign the column was on the wrong scale.

## Why position matters as much as distance

The reason one far-off point wrecks a fit and another leaves it alone is the hat
value, and squared error is what makes it bite. Least squares cuts the *sum of
squared* residuals, so a point twice as far off adds four times the fine
and one ten times as far adds a hundred times. The line will travel a
long way to reduce a single large residual. But a regression line pivots roughly
about the mean of x. So How far a point sits along x decides how much turning force
its vertical error applies:

|the odd point|effect on the slope|
|---|---|
|large residual, near the middle of x|small &mdash; close to the pivot|
|large residual, at the extreme of x|large &mdash; the end of a long lever|

That gives three distinct things worth separating: an **outlier** is unusual in y,
**a high hat value** is unusual in x, and only their combination &mdash;
**influential** &mdash; really moves the model. This is what Cook's distance
measures. A point with a high hat value sitting on the trend is harmless. A mid-range
outlier is harmless. The far-right outlier is the one that quietly rewrites the
answer. Which is also why "delete any of it beyond three standard deviations" is
self-defeating: the outlier has already inflated the standard deviation the rule
depends on.

## Where it goes wrong

**Deleting by rule.** "Beyond three standard deviations" uses the standard
deviation, which the outlier itself has already inflated.

**Treating placeholders as data.** 999 for unknown age, &minus;1 for missing.
These aren't outliers. They're missing values wearing a number.

**Dropping points until the model fits.** At that stage the model shows the
pick, not the effect.

**Checking only y.** Points with high hat values can be plain in y and still
dominate the fit.

## Questions people ask

<strong>Is every outlier a problem?</strong> No. An outlier is an unusual value, and it matters only if it changes the fit. A point that sits on the trend line is harmless.

<strong>What is the difference between an outlier and an influential point?</strong> An outlier has an unusual response given its inputs, while an influential point changes the fitted model when removed. Points far from the other inputs are the usual cause of influence.

<strong>How do I measure influence?</strong> Cook's distance combines residual size and distance from the other inputs in one number. A common rule of thumb flags values above 4/n for a closer look.

<strong>Should I delete outliers?</strong> Only after checking whether they are errors. If the value is real, removing it hides something true about your data, so consider a different model or transform instead.

<strong>What can I do besides removing them?</strong> Use a loss that is less sensitive to large errors, such as Huber or quantile regression. Or transform the target, or use median-based statistics.

<strong>Why does squared error make outliers worse?</strong> Squaring makes one large residual count far more than many small ones, so the fit bends towards the extreme point.

## An outlier and an influential point are not the same thing

One far-out row can leave a fit untouched while another moves it fully. The difference is the hat value, and it is computable.

```python-run
import numpy as np
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(0)
x = np.linspace(0, 10, 60)
y = 2.0 * x + 5.0 + rng.normal(0, 1.5, 60)
X = x.reshape(-1, 1)

def fit(Xa, ya, label):
    m = LinearRegression().fit(Xa, ya)
    print("  %-34s slope %7.4f  intercept %7.4f" % (label, m.coef_[0], m.intercept_))
    return m

print("the true relationship is y = 2x + 5.")
base = fit(X, y, "clean data")

xm, ym = 5.0, 60.0
Xa = np.vstack([X, [[xm]]]); ya = np.r_[y, ym]
mid = fit(Xa, ya, "one wild point at x=5 (middle)")

xe, ye = 10.0, 65.0
Xb = np.vstack([X, [[xe]]]); yb = np.r_[y, ye]
edge = fit(Xb, yb, "one wild point at x=10 (edge)")
print()
print("both sit ~%.0f above the true line." % (ym - (2 * xm + 5)))
print("  x=5  moved the slope by %.4f" % abs(mid.coef_[0] - base.coef_[0]))
print("  x=10 moved the slope by %.4f" % abs(edge.coef_[0] - base.coef_[0]))
print("x=5 is the mean of x, so that point has no lever at all: it pushed")
print("the whole line up without tilting it. the edge point tilted it.")
```

The next block computes hat values and Cook's distance to show how influence is measured.

```python-run
import numpy as np
from sklearn.linear_model import LinearRegression
rng = np.random.default_rng(0)
x = np.linspace(0, 10, 60)
y = 2.0 * x + 5.0 + rng.normal(0, 1.5, 60)
X = x.reshape(-1, 1)
Xa = np.vstack([X, [[5.0]]]); ya = np.r_[y, 60.0]
Xb = np.vstack([X, [[10.0]]]); yb = np.r_[y, 65.0]

def leverage(Xc):
    Z = np.column_stack([np.ones(len(Xc)), Xc])
    H = Z @ np.linalg.solve(Z.T @ Z, Z.T)
    return np.diag(H)

print("leverage depends only on x, never on y:")
for label, Xc in (("point at x=5 ", Xa), ("point at x=10", Xb)):
    h = leverage(Xc)
    print("  %s  leverage %.4f   (average is %.4f)" % (label, h[-1], h.mean()))
print("  far from the mean of x = long lever.")
print()

print("Cook's distance combines both: how far off the line, times leverage.")
def cooks(Xc, yc):
    m = LinearRegression().fit(Xc, yc)
    resid = yc - m.predict(Xc)
    h = leverage(Xc)
    mse = (resid ** 2).sum() / (len(yc) - 2)
    return resid ** 2 * h / (2 * mse * (1 - h) ** 2)

for label, Xc, yc in (("added at x=5 ", Xa, ya), ("added at x=10", Xb, yb)):
    d = cooks(Xc, yc)
    print("  %s  Cook's D %.4f  (investigate above %.4f)" % (label, d[-1], 4/len(yc)))
print()
print("  outlier      -- unusual y for its x. may cost you nothing.")
print("  high leverage -- unusual x. dangerous whether or not y is odd.")
print("  influential  -- actually moved the fit. Cook's D measures this.")
```

The next block shows how resistant estimators handle the same outlier.

```python-run
import numpy as np
from sklearn.linear_model import LinearRegression, HuberRegressor, RANSACRegressor
rng = np.random.default_rng(0)
x = np.linspace(0, 10, 60)
y = 2.0 * x + 5.0 + rng.normal(0, 1.5, 60)
X = x.reshape(-1, 1)
Xb = np.vstack([X, [[10.0]]]); yb = np.r_[y, 65.0]

print("robust fits, on the edge-outlier data:")
edge = LinearRegression().fit(Xb, yb)
print("  ordinary least squares  slope %7.4f" % edge.coef_[0])
print("  Huber                   slope %7.4f"
      % HuberRegressor().fit(Xb, yb).coef_[0])
print("  RANSAC                  slope %7.4f"
      % RANSACRegressor(random_state=0).fit(Xb, yb).estimator_.coef_[0])
print("  true                    slope  2.0000")
print()
print("Huber switches from squared to absolute error past a threshold,")
print("so a far-out point stops getting quadratically more say. RANSAC")
print("fits on random subsets and keeps the fit most points agree with.")
print()
print("deleting the point is a decision about what your data means.")
print("a sensor glitch, delete it. a genuine extreme customer, deleting")
print("means the model no longer covers them.")
```

""",
    [
        {"q": "Why does least squares react so strongly to a single distant point?",
         "options": ["It weights recent points more",
                     "It minimises squared error, so a point twice as far off pulls four times as hard",
                     "It ignores points near the mean",
                     "It fits the maximum rather than the average"],
         "answer": 1,
         "why": "The objective is willing to move a long way to reduce one large residual, even at a small cost to every other point. That is what the loss function asks for."},
        {"q": "What makes a point 'influential' rather than merely an outlier?",
         "options": ["It has a large residual",
                     "It is unusual in x as well as y, so removing it changes the model",
                     "It is the newest observation",
                     "It has a missing value"],
         "answer": 1,
         "why": "The line pivots about the mean of x, so a point far along x sits at the end of a long lever. Extreme in y near the pivot is harmless; the combination is not."},
        {"q": "What is wrong with removing anything beyond three standard deviations?",
         "options": ["Three is too strict",
                     "The outlier has already inflated the standard deviation being used to judge it",
                     "It requires a normal distribution",
                     "It removes too few points"],
         "answer": 1,
         "why": "The rule uses a statistic the outlier corrupts, so a large enough outlier widens the threshold enough to protect itself. Robust measures like the median absolute deviation avoid this."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Pipelines
# ---------------------------------------------------------------------------
topic(
    "ml_pipelines",
    "Pipelines",
    "Workflow",
    "The object that makes leakage impossible by construction, because every "
    "fold fits its own preprocessing.",
    _svg(_box(10, 34, 34, 22, fill=S) + _txt(27, 48, "impute", M, 8)
         + _line(44, 45, 56, 45, A, 1.4)
         + _box(56, 34, 34, 22, fill=S) + _txt(73, 48, "scale", M, 8)
         + _line(90, 45, 102, 45, A, 1.4)
         + _box(102, 34, 44, 22, fill=S) + _txt(124, 48, "model", M, 8)
         + _txt(80, 74, "one object, fitted per fold", M, 7)),
    {
        "sim": "pipeline",
        "controls": [
            {"key": "order", "label": "How the fitted steps are fitted", "type": "select",
             "value": "leaky",
             "options": [{"value": "leaky", "label": "By hand, before cross-validation"},
                         {"value": "correct", "label": "Inside a pipeline, per fold"}]},
            {"key": "features", "label": "Columns of noise to choose from",
             "type": "range", "min": 40, "max": 600, "step": 20, "value": 400},
        ],
        "captions": ["Reported accuracy against the truth"],
    },
    [
        "A pipeline chains transformers and a final estimator into one object "
        "with one <code class='mono-font'>fit</code> and one "
        "<code class='mono-font'>predict</code>.",
        "Cross-validating the pipeline refits every step on each fold's training "
        "portion. That is what makes leakage structurally impossible.",
        "It also removes the train/serve gap: the same object that was fitted is "
        "the thing you save and deploy.",
        "<code class='mono-font'>ColumnTransformer</code> applies different "
        "steps to different columns, which is how real tables get handled.",
    ],
    """
title: Pipelines
intro: Not a convenience wrapper. The setup in which the order of ops can't be got wrong.

## The same demonstration, one level up

The chart is the one from the [leakage](data_leakage.html) module, relabelled:
300 rows of pure noise, five columns chosen by their link with the label,
and a choice about *when* that choice is made.

By hand, before cross-validation, the reported fit sits well above the 50%
the data deserves. Inside a pipeline. Here Each fold selects its own columns
from its own training rows, it falls to the truth.

The model is the same in both. What changed is which object owns the fitting,
and that is the entire arg for pipelines. It isn't about tidiness.

## What goes wrong by hand

The by-hand workflow looks reasonable written out:

```
X = impute(X)
X = scale(X)
X = select_features(X, y)
scores = cross_val_score(model, X, y, cv=5)
```

each one of those three steps has been fitted on all the data, and
`cross_val_score` then splits data that has already been contaminated. Each fold
was scaled using a mean that included its own validation rows, imputed using a
median that included them, and reduced to features chosen partly because they
linked with their labels.

Nothing errors. The score is simply too high, by an amount that depends on the
data and can't be guessed after the fact.

## What a pipeline changes

```
pipe = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale",  StandardScaler()),
    ("select", SelectKBest(k=20)),
    ("model",  KNeighborsClassifier()),
])
scores = cross_val_score(pipe, X, y, cv=5)
```

`cross_val_score` now receives one estimator. On each fold it calls `fit` on the
pipeline with that fold's training rows, and the pipeline fits the imputer, then
the scaler, then the feature selector, then the model. All on those rows
only. Scoring calls `transform` on the validation rows using the params just
learned.

The correct order isn't a thing you remembered to do. It's the only thing
the object can do.

## The three other things it buys

**Setting search over prep.** Because the steps are part of one
estimator, a grid can range over them.

```
{"impute__strategy": ["mean", "median"],
 "select__k": [10, 20, 40],
 "model__n_neighbors": [3, 5, 11]}
```

Whether the median beats the mean turns a question the search answers, on the
same footing as the model's own params. Doing this by hand right is
possible and no one does it.

**No train/serve gap.** The fitted pipeline is one object. Save it, load it in
the service, call `predict` on raw input. There's no second setup of
the prep to drift out of step with the first. Which is a real
and common production failure, and a silent one.

**Different columns, different treatment.** `ColumnTransformer` routes numeric
columns to an imputer and scaler, cat ones to a different imputer and a
one-hot encoder, and text to a vectoriser, then hands the mixed result to the
model. That is what an actual table needs, and it stays one object.

## Cross-validation still needs care

A pipeline stops leakage between prep and test. It doesn't fix
splits that were wrong to begin with.

If rows are grouped &mdash; a few scans per patient &mdash; use `GroupKFold`
so a patient can't appear on both sides. If the data is a time series, use
`TimeSeriesSplit` so training always precedes validation. And if you tune
settings on the same folds you report, that number is optimistic too;
nested cross-validation is the honest version.

## The size of the leak, in accuracy points

The reason to insist on a pipeline is that the leak is large and silent. Take 300
rows of pure noise &mdash; features with no tie to the label at all
&mdash; and select the 20 columns most linked with the label, then
cross-validate:

|when the columns are chosen|reported accuracy|truth|
|---|---|---|
|once, on all the data, before CV|~65%|50%|
|inside each fold, on its training rows only|~50%|50%|

The data can't support better than chance, and the honest pipeline says so. The
by-hand version reports 65% because the feature pick has already seen each
fold's validation rows: it picked the columns that happened to correlate with
those labels too, so each fold is scored on features chosen partly *because* they
match its answers. Nothing errors, and the inflation &mdash; fifteen points here,
more with more pick features. Can't be guessed after the fact,
because it depends on data the leak already consumed. The pipeline makes the
correct order the only order the object can execute. Each fold fits the selector,
the scaler and the model on its own training rows and merely transforms the
validation rows. The number it reports is a real guess.

Beyond stopping the leak, the pipeline buys three things that are awkward by hand.
Setting search can range over the prep &mdash; whether the median
beats the mean turns a tuned choice on the same footing as the model's own
settings. There's no train/serve gap, because the fitted pipeline is one object
saved and loaded whole, so there's no second copy of the prep to drift
out of step. And `ColumnTransformer` routes numeric columns to a scaler,
cats to an encoder, and text to a vectoriser, all inside the same object.
What a pipeline can't do is validate the splits themselves: if rows are grouped by
patient or sorted in time, it still needs `GroupKFold` or `TimeSeriesSplit` to
keep the folds honest.

One special case catches people: resampling. SMOTE and other over-samplers must
run on the training fold only, and scikit-learn's own `Pipeline` doesn't enforce
that &mdash; `imblearn`'s pipeline does. A log transform, by contrast, has no
fitted params and can't leak. So It need not live in the pipeline at all,
though keeping it there's still worth the tidiness of one place for the
prep.

## Where it goes wrong

**Calling `fit` on the test data.** Use `transform`. `fit_transform` on the test
set refits all and undoes the whole point.

**Steps that aren't fitted.** A log transform has no params and can't
leak, so it doesn't have to be in the pipeline. But putting it there
keeps the prep in one place. This Is worth more than the exemption.

**Resampling inside a plain pipeline.** SMOTE and friends must run on the
training fold only. `imblearn`'s pipeline handles this. Scikit-learn's doesn't.

**given a pipeline validates your splits.** It fits each fold right. It
can't know that your folds mix one patient across both sides.

## Questions people ask

<strong>Why use a pipeline instead of separate steps?</strong> A pipeline guarantees every transform is fit only on training data inside each fold. It also makes the whole workflow one object you can save and reuse.

<strong>Does a pipeline prevent leakage?</strong> It prevents the preprocessing kind, when you cross-validate the whole pipeline. It cannot catch target leakage or time-based leakage.

<strong>How do I tune hyperparameters of pipeline steps?</strong> Use the step name, a double underscore, and the parameter, such as svc__C. Pass these to GridSearchCV or RandomizedSearchCV.

<strong>What is ColumnTransformer for?</strong> It applies different preprocessing to different columns, for example scaling numeric columns and one-hot encoding categorical ones, then joins the results.

<strong>Can I put custom code in a pipeline?</strong> Yes. Wrap a function in FunctionTransformer, or write a class with fit and transform methods.

<strong>How do I save a pipeline?</strong> Serialise the fitted pipeline with joblib. Loading it gives you the preprocessing and model together, so production predictions match training.

## The same workflow, wrong then right

prep outside the pipeline scores higher and is a lie. Here are both versions side by side, on the same data.

```python-run
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold

rng = np.random.default_rng(0)
X = rng.normal(size=(200, 800))
y = rng.integers(0, 2, 200)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
print("200 rows, 800 noise columns, a random label. nothing is learnable.")
print()

Xs = StandardScaler().fit_transform(X)
Xk = SelectKBest(f_classif, k=25).fit_transform(Xs, y)
print("preprocessing first, then cross-validating the model:")
print("  cv %.4f" % cross_val_score(LogisticRegression(max_iter=2000),
                                    Xk, y, cv=cv).mean())

pipe = make_pipeline(StandardScaler(), SelectKBest(f_classif, k=25),
                     LogisticRegression(max_iter=2000))
print("the same three steps, inside a Pipeline:")
print("  cv %.4f" % cross_val_score(pipe, X, y, cv=cv).mean())
print()
print("identical code, identical data. the first number is a lie because the")
print("selector saw the test rows' labels. cross_val_score refits every step")
print("of a Pipeline inside each fold, which is the whole reason it exists.")
print()

print("a Pipeline is just a list of (name, step) pairs:")
for name, step in pipe.steps:
    print("   %-16s %s" % (name, type(step).__name__))
print("  every step but the last needs fit_transform. the last needs fit.")
```

The next block shows how to tune parameters through a pipeline and how ColumnTransformer handles mixed column types.

```python-run
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import StratifiedKFold, GridSearchCV
rng = np.random.default_rng(0)
X = rng.normal(size=(200, 800))
y = rng.integers(0, 2, 200)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
pipe = make_pipeline(StandardScaler(), SelectKBest(f_classif, k=25),
                     LogisticRegression(max_iter=2000))
print("you can reach into it to tune any step's parameters:")
grid = GridSearchCV(pipe, {"selectkbest__k": [5, 25, 100],
                           "logisticregression__C": [0.01, 1.0]},
                    cv=cv, n_jobs=1)
grid.fit(X, y)
print("  best params:", grid.best_params_)
print("  best cv score: %.4f  <- still noise, as it should be" % grid.best_score_)
print("  the double underscore is 'step name, then parameter name'.")
print()
print("ColumnTransformer handles mixed column types.")
data = np.column_stack([rng.normal(size=(300, 3)),
                        rng.integers(0, 3, 300).astype(float)])
data[rng.random(300) < 0.08, 0] = np.nan
pre = ColumnTransformer([
    ("numbers", make_pipeline(SimpleImputer(), StandardScaler()), [0, 1, 2]),
    ("category", OneHotEncoder(handle_unknown="ignore"), [3]),
])
out = pre.fit_transform(data)
print("  %d input columns -> %d output columns" % (data.shape[1], out.shape[1]))
print("  numeric: imputed and scaled. category: three indicator columns.")
print("  each transformer only touches its own columns.")
print()
print("one object holds the whole recipe, so the thing you cross-validate")
print("is the thing you deploy. that is the argument -- not tidiness.")
```

""",
    [
        {"q": "What does cross-validating a pipeline do that cross-validating a model does not?",
         "options": ["It runs faster",
                     "It refits every preprocessing step on each fold's training portion",
                     "It uses more folds",
                     "It tunes hyperparameters automatically"],
         "answer": 1,
         "why": "Preprocessing fitted by hand beforehand has already seen every validation row. Inside a pipeline the correct order is the only thing the object can do."},
        {"q": "Why does a pipeline remove the train/serve gap?",
         "options": ["It compresses the model",
                     "The fitted object contains the preprocessing, so there is no second implementation to drift out of step",
                     "It logs predictions",
                     "It validates input types"],
         "answer": 1,
         "why": "Reimplementing preprocessing in the serving code is a common production failure and a silent one - the model receives differently-prepared inputs and quietly degrades."},
        {"q": "What does a pipeline NOT protect you from?",
         "options": ["Fitting a scaler on test data",
                     "Splits that were wrong to begin with, such as one patient appearing on both sides",
                     "Imputing before scaling",
                     "Feature selection leakage"],
         "answer": 1,
         "why": "It fits each fold correctly but cannot know your folds are badly formed. Grouped data needs GroupKFold and time series need TimeSeriesSplit."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Precision, recall and F1
# ---------------------------------------------------------------------------
topic(
    "precision_recall_and_f1",
    "Precision, Recall and F1",
    "Evaluation",
    "Move the threshold and watch the confusion matrix rearrange itself. One "
    "model, and every score in the table changes.",
    _svg(_box(28, 22, 50, 24, fill=S) + _txt(53, 37, "TP", A, 10)
         + _box(82, 22, 50, 24, fill=S) + _txt(107, 37, "FN", M, 10)
         + _box(28, 48, 50, 24, fill=S) + _txt(53, 63, "FP", M, 10)
         + _box(82, 48, 50, 24, fill=S) + _txt(107, 63, "TN", M, 10)),
    {
        "sim": "confusion",
        "controls": [
            {"key": "threshold", "label": "Threshold", "type": "range",
             "min": 0.05, "max": 0.95, "step": 0.01, "value": 0.5},
        ],
        "fixed": {"posRate": 0.5, "sep": 0.17},
        "captions": ["Grey: actual negatives. Orange: actual positives."],
    },
    [
        "<strong>Precision</strong>: of the things you flagged, how many were "
        "right. It punishes false positives.",
        "<strong>Recall</strong>: of the things that were there, how many you "
        "found. It punishes false negatives.",
        "They trade off. Lower the threshold and recall rises while precision "
        "falls; raise it and the reverse.",
        "F1 is their harmonic mean, which stays low unless <em>both</em> are "
        "high. An arithmetic mean would not.",
    ],
    """
title: Precision, Recall and F1
intro: Four counts in a table, three ratios drawn from them. One slider that moves all of it.

## One model, many scores

A classifier doesn't output a class. It outputs a **score** &mdash; how
plus it thinks each case is. And a class only appears once you compare
that score against a threshold.

The histogram shows both spreads: actual negatives in grey, actual
positives in orange, shared in the middle because the model is good and not
perfect. The dashed line is the threshold.

Move it. each number below the chart changes, and the model hasn't been
retrained. The scores are properties of the threshold as much as of the model,
which is the single most handy thing to understand here.

## The four counts

| | Predicted positive | Predicted negative |
|---|---|---|
| **Actually positive** | True positive | False negative |
| **Actually negative** | False positive | True negative |

All else is a ratio of these. The two that matter most divide by
different denominators, which is just why they disagree.

**Precision** = TP / (TP + FP). Of all you flagged, what fraction
was right. The denominator is what *you* predicted. So Precision is damaged by
false alarms.

**Recall** = TP / (TP + FN). Of all that was really there, what
fraction you caught. The denominator is what *reality* held, so recall is
damaged by misses.

## Why they trade off

Drag the threshold to 0.10. Almost all is flagged, so almost each real
plus is caught and recall approaches 100%. But the flagged set is now full of
negatives, and precision merges.

Drag it to 0.90. Only the most confident cases are flagged, nearly all of them
correct, and precision approaches 100%. But most real positives are below the
line, and recall merges.

You can't raise both by moving the threshold. The threshold only chooses
where on the trade-off you sit. Raising both at once needs a better model
&mdash; one whose two spreads share less.

## Which one you want depends on the cost

The question is never "which metric is best". It's **which mistake is more
costly**.

**Recall matters more** when a miss is costly: screening for a serious disease,
detecting fraud, finding safety defects. A false alarm costs a second look. A
miss costs the thing you were trying to prevent.

**Precision matters more** when a false alarm is costly: flagging accounts for
suspension, recommending content, sending an alert that wakes someone. Missing
one is a shame. Being wrong again and again destroys trust in the system.

## F1, and why it is a harmonic mean

F1 mixes them:

```
F1 = 2 * precision * recall / (precision + recall)
```

That is the harmonic mean, and the choice of mean is the point. Take precision
of 1.0 and recall of 0.01. A model that flags just one case and gets
it right. The arithmetic mean is 0.505. This Sounds fair. F1 is 0.0198.

The harmonic mean is pulled toward the smaller number. So It stays low unless
both are high. That makes it hard to game with a collapse model, which is
just what a single summary number needs to be.

F1 weights the two equally. This Is a choice and often the wrong one. F-beta
lets you weight recall &beta; times as much as precision. F2 favours recall, F0.5
favours precision. If you've a reason to prefer one, use it.

## Why accuracy is on the readout and not in the headline

Fit is (TP + TN) / all. It's the most natural metric and it's
close to useless when the classes are unbalanced.

If 1% of transactions are fraudulent, predicting "never fraud" scores 99%
fit while catching nothing at all. Precision and recall are both zero, which
is the honest description. [Imbalanced
data](precision_recall_vs_roc.html) is where this matters most.

## The same model at two thresholds

Precision and recall are properties of the threshold as much as the model, which a
worked confusion mat makes concrete. The same classifier, the same scores, two
cuts:

|threshold|caught (of 100 real)|false alarms|precision|recall|
|---|---|---|---|---|
|0.10 (permissive)|98|300|0.246|0.98|
|0.90 (strict)|40|4|0.909|0.40|

Drop the threshold and recall climbs toward 100% as almost all is flagged,
but the flagged set fills with negatives and precision merges. Raise it and
precision climbs as only confident cases live. But Most real positives fall
below the line and recall merges. The threshold only chooses *where on the
trade-off you sit* &mdash; raising both at once needs a better model, one whose
plus and minus score spreads share less. F1 summarises a single
point as the harmonic mean, `2PR/(P+R)`, and the choice of *harmonic* is the
point: precision 1.0 with recall 0.01 means to a fair-looking 0.505
arithmetically but an F1 of just 0.0198. The harmonic mean is dragged to
the smaller number and refuses to reward a model that flags one case and hides.

Which error to cut is a question about costs, never about which metric is
"best". Recall matters more when a miss is costly. Screening for a serious
disease, catching fraud &mdash; where a false alarm costs only a second look.
Precision matters more when a false alarm is costly &mdash; suspending an
account, paging a human at 3am. Where a miss is merely dealt with later. And
fit, the most natural metric, is close to useless under imbalance: if 1% of
transactions are fraud, predicting "never fraud" scores 99% while catching nothing,
with precision and recall both zero telling the honest story the single fit
number hides.

## Where it goes wrong

**Reporting one number without the threshold.** "Precision 0.9" is
uninterpretable alone. At some threshold nearly each model reaches it.

**Optimising F1 when the costs aren't equal.** F1 assumes they're.

**Checking models at 0.5.** Two models can rank cases equally well and differ
only in calibration. Compare across thresholds, or tune each one.

**Fit on imbalanced data.** It measures the class balance more than the
model.

## Questions people ask

<strong>What is the difference between precision and recall?</strong> Precision is the share of positive predictions that are right. Recall is the share of actual positives you caught.

<strong>When should I favour precision over recall?</strong> When false alarms are costly, such as flagging legitimate transactions as fraud. Favour recall when missing a case is worse, like cancer screening.

<strong>Why does F1 use a harmonic mean?</strong> It is pulled towards the lower of the two values, so a model cannot hide terrible recall behind high precision.

<strong>Why not just use accuracy?</strong> On imbalanced data a model that always predicts the majority class scores high accuracy while catching nothing.

<strong>What are macro, micro and weighted averages?</strong> Macro averages the per-class scores equally, micro pools all the counts, and weighted averages by class size. Macro treats rare classes as equally important.

<strong>Can I raise both precision and recall?</strong> At a fixed model, changing the threshold trades one for the other. To improve both, you need a better model or better features.

## The trade you cannot avoid

Precision and recall pull in opposite directions. Sweeping the choice threshold shows just how much of one each unit of the other costs.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score

X, y = make_classification(n_samples=6000, n_features=15, n_informative=5,
                           weights=[0.9, 0.1], flip_y=0.08, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.35, random_state=0,
                                      stratify=y)
prob = LogisticRegression(max_iter=2000).fit(Xtr, ytr).predict_proba(Xte)[:, 1]

print("%10s %11s %9s %9s %9s %9s"
      % ("threshold", "flagged", "precision", "recall", "F1", "missed"))
for t in (0.05, 0.10, 0.20, 0.35, 0.50, 0.70, 0.90):
    pred = (prob >= t).astype(int)
    print("%10.2f %11d %9.4f %9.4f %9.4f %9d"
          % (t, pred.sum(),
             precision_score(yte, pred, zero_division=0),
             recall_score(yte, pred, zero_division=0),
             f1_score(yte, pred, zero_division=0),
             ((pred == 0) & (yte == 1)).sum()))
print()
print("there are %d real positives in this test set." % (yte == 1).sum())
print()
print("precision: of everything you flagged, how much was right.")
print("recall:    of everything that was right, how much you flagged.")
print("lowering the threshold flags more, so recall rises and precision falls.")
print()
print("F1 is their harmonic mean, which is harsh on imbalance between them:")
for p, r in ((0.9, 0.9), (0.95, 0.85), (1.0, 0.5), (0.5, 1.0)):
    print("  precision %.2f, recall %.2f -> arithmetic %.3f, F1 %.3f"
          % (p, r, (p + r) / 2, 2 * p * r / (p + r)))
print()
print("which one you optimise is a business decision, not a modelling one:")
print("  a spam filter wants precision -- a false alarm loses real mail.")
print("  a cancer screen wants recall  -- a miss is far worse than a recheck.")
```

""",
    [
        {"q": "What happens to precision and recall as the threshold falls?",
         "options": ["Both rise", "Both fall",
                     "Recall rises and precision falls",
                     "They are unaffected by the threshold"],
         "answer": 2,
         "why": "A lower threshold flags more cases, so more real positives are caught (recall up) but the flagged set fills with negatives (precision down). The threshold picks a point on the trade-off, it does not improve the model."},
        {"q": "Why is F1 a harmonic rather than arithmetic mean?",
         "options": ["It is faster to compute",
                     "The harmonic mean is pulled toward the smaller value, so it stays low unless both are high",
                     "It bounds the result to [0, 1]",
                     "It handles zero denominators"],
         "answer": 1,
         "why": "Precision 1.0 with recall 0.01 averages arithmetically to a respectable 0.505 and gives an F1 of 0.0198. The harmonic mean refuses to be gamed by a degenerate model."},
        {"q": "Why is accuracy misleading when 1% of cases are positive?",
         "options": ["It ignores true negatives",
                     "Predicting 'never positive' scores 99% while catching nothing",
                     "It cannot be computed",
                     "It depends on the threshold"],
         "answer": 1,
         "why": "Accuracy measures the class balance more than the model. Precision and recall would both be zero, which is the honest description of that model."},
    ],
)


# ---------------------------------------------------------------------------
# 7. Precision-Recall vs ROC
# ---------------------------------------------------------------------------
topic(
    "precision_recall_vs_roc",
    "Precision-Recall against ROC",
    "Evaluation",
    "The same model on the same scores. Drag the positive rate down and watch "
    "ROC stay flattering while the PR curve tells the truth.",
    _svg(_axes()
         + '<path d="M20 72 C 50 30, 80 22, 148 18" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + _line(20, 72, 148, 18, B, 1, "4 3")
         + _txt(100, 60, "ROC barely moves", M, 8)),
    {
        "sim": "roc_pr",
        "canvases": 2,
        "controls": [
            {"key": "posRate", "label": "Fraction of rows that are positive",
             "type": "range", "min": 0.01, "max": 0.5, "step": 0.01, "value": 0.5},
        ],
        "captions": ["ROC curve", "Precision-Recall curve"],
    },
    [
        "ROC plots true positive rate against false positive rate. Both are "
        "computed <em>within</em> a class, so neither depends on the balance.",
        "That independence is the problem: on imbalanced data ROC looks good "
        "for a model that is not useful.",
        "The PR curve uses precision, whose denominator mixes both classes, so "
        "it falls when positives are rare.",
        "The no-skill baseline is the diagonal for ROC and a horizontal line at "
        "the positive rate for PR.",
    ],
    """
title: Precision-Recall against ROC
intro: Two curves over the same scores. The reason one of them flatters a model that can't be deployed.

## Start balanced

Leave the slider at 0.5. Half the rows are plus, and the two curves broadly
agree: ROC bows toward the top left, PR bows toward the top right, and both say
the model is decent.

Now drag the slider down toward 0.02. This Is a realistic rate for fraud,
disease screening or ad clicks. Watch the two charts diverge.

**ROC barely moves.** The AUC in the readout stays high.

**PR merges.** The precision that was achievable at any handy recall falls
away, and the best F1 falls with it.

The scores didn't change. The model didn't change. Only the proportion of
positives changed, and the two curves disagree about whether that matters.

## Why ROC does not notice

ROC plots true positive rate against false positive rate:

```
TPR = TP / (TP + FN)     denominator: all actual positives
FPR = FP / (FP + TN)     denominator: all actual negatives
```

Each is found fully within one class. TPR asks what fraction of positives
were caught. FPR asks what fraction of negatives were wrongly flagged. Adding a
million more negatives leaves TPR untouched and changes FPR only through its own
denominator, which grows in proportion.

That class-freedom is often given as a virtue, and for some purposes it
is. It also means ROC can't see the thing that makes rare-plus problems
hard.

## Why PR does notice

Precision is different:

```
precision = TP / (TP + FP)     denominator: everything you flagged
```

The denominator mixes both classes. When negatives outnumber positives a hundred
to one, even a small false plus *rate* makes a large *number* of false
positives, and those go straight into precision's denominator.

Concretely: 10,000 rows, 100 plus. A model at 90% recall and 5% FPR catches
90 real positives and flags 495 negatives. FPR of 5% sounds great and ROC
records it as such. Precision is 90 / 585 = **15%**. Five out of six flagged
cases are wrong, and each one costs somebody an investigation.

## Reading the baselines

Each chart has a dashed no-skill line, and they differ.

For **ROC** it's the main-line, always. A random classifier gets AUC 0.5
even so of balance.

For **PR** it's a flat line at the **positive rate**. At 50% positives,
random scores 0.5 precision. At 2%, random scores 0.02. Drag the slider and
watch it drop.

This is what makes PR honest and slightly harder to read: there's no fixed
scale. A PR AUC of 0.4 is poor on weighed data and outstanding at a 2% base
rate. The number must always be checked against the baseline, never quoted
alone.

## Which to use

| Situation | Curve | Reason |
|---|---|---|
| Roughly balanced | either | they broadly agree |
| Rare positives | **PR** | ROC hides the false-positive volume |
| You care about ranking overall | ROC | it is what AUC measures |
| Someone acts on each flag | **PR** | precision is that person's experience |
| Comparing across datasets | ROC, carefully | PR baselines differ by base rate |

The hands-on rule: if a human or a process has to act on each plus
guess, precision is the thing they run into, and the PR curve is the one
to look at.

## Add a million negatives, and watch only one curve move

The divergence is math. Hold the model's rates fixed &mdash; 90% recall, 5%
false-positive rate &mdash; and change only the class balance in 10,000 rows:

|positives|TP|FP|precision|TPR / FPR|
|---|---|---|---|---|
|5,000 (balanced)|4,500|250|0.95|0.90 / 0.05|
|100 (1%)|90|495|**0.15**|0.90 / 0.05|

The ROC coords are the same in both rows. TPR cuts by actual
positives and FPR by actual negatives. Each lives inside one class, so the
balance can't touch them. Precision cuts by all flagged, which mixes
the classes, so when negatives outnumber positives a 5% false-positive rate turns
into 495 false alarms drowning 90 real ones and precision falls to 0.15. Same
model, same scores, and ROC records it as great while five of each six
flagged cases are wrong. That is why ROC AUC alone on rare-plus data is the
standard way to make an undeployable model look ready, and why the PR curve
&mdash; whose no-skill baseline is the positive rate itself, 0.01 here, not a
fixed 0.5 &mdash; is the honest one to quote.

The hands-on rule follows from who acts on the output. If a human or a process
has to deal with each plus guess. An analyst investigating each
flag, a queue of cases to review. Then precision is the run into that
person really has, and the PR curve is the one to read. ROC still has its place:
it's the right tool when you care about ranking quality total, and it's more
close across datasets because its baseline is a fixed 0.5 rather than a
base-rate that shifts. Neither curve, though, tells you which threshold to deploy;
that is a separate choice driven by [costs](threshold_tuning.html).

One more skew is worth stating: because the PR baseline is the positive rate,
a PR AUC has no fixed scale. A PR AUC of 0.4 is poor on weighed data and
outstanding at a 2% base rate. So The number means nothing quoted alone &mdash; it
has to be read against the baseline for that dataset. This Is just why it
can't be checked across datasets with different weighs the way ROC can.

A last check point: the two curves also treat the negatives differently. ROC
rewards a model for right ranking the vast pool of easy negatives, which is
where its optimism on rare-plus data comes from. PR skips true negatives
fully &mdash; they appear in neither precision nor recall &mdash; so it reports
only on the positives you care about and the false alarms among them.

## Where it goes wrong

**Reporting ROC AUC alone on imbalanced data.** It's the standard way to make a
model that will drown a team in false positives look ready to ship.

**Checking PR AUC across datasets with different base rates.** The baselines are
different, so the numbers aren't close.

**Losing that both curves span all thresholds.** Neither tells you which
threshold to deploy &mdash; that is a separate choice, made with
[costs](threshold_tuning.html).

## Questions people ask

<strong>When should I use a precision-recall curve instead of ROC?</strong> When the positive class is rare. ROC can look excellent even when most flagged items are false alarms.

<strong>Why does ROC AUC stay high on imbalanced data?</strong> The false positive rate divides by the huge number of negatives, so many false positives still give a small rate.

<strong>What is the baseline for each curve?</strong> ROC AUC for a random model is 0.5 regardless of balance. For PR it equals the positive rate, so it changes with the data.

<strong>Can I compare PR AUC across datasets?</strong> Only with care, since the baseline differs. Compare against each dataset's positive rate.

<strong>What is average precision?</strong> A summary of the PR curve, the weighted mean of precision at each threshold. It is the usual way to get a single PR number.

<strong>Do the curves change if I change the threshold?</strong> No. Each curve covers all thresholds. The threshold picks a single point on it.

## The same model, two curves, two different stories

ROC and precision-recall are found from the same guesses. On weighed data they agree. On imbalanced data one of them is misleading. It's always the same one.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score

def build(weight, seed=0):
    X, y = make_classification(n_samples=20000, n_features=18, n_informative=10,
                               weights=[weight], flip_y=0.005, class_sep=2.5,
                               random_state=seed)
    a, b, c, d = train_test_split(X, y, test_size=0.4, random_state=0, stratify=y)
    return d, LogisticRegression(max_iter=3000).fit(a, c).predict_proba(b)[:, 1]

print("%14s %10s %12s %12s" % ("positive rate", "ROC AUC", "PR AUC", "PR baseline"))
for w in (0.50, 0.80, 0.95, 0.985):
    yte, p = build(w)
    print("%13.2f%% %10.4f %12.4f %12.4f"
          % (100 * yte.mean(), roc_auc_score(yte, p),
             average_precision_score(yte, p), yte.mean()))
print()
print("ROC AUC drifts. PR AUC falls through the floor -- and its baseline")
print("falls with it, because a random scorer's PR AUC IS the positive rate.")
print("ROC AUC's baseline is 0.5 no matter what, which is exactly the problem:")
print("a number that does not move cannot warn you.")
```

The next block picks one threshold on the most imbalanced data and shows what the false positive rate and precision actually measure.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix

X, y = make_classification(n_samples=20000, n_features=18, n_informative=10,
                           weights=[0.985], flip_y=0.005, class_sep=2.5,
                           random_state=0)
a, b, c, d = train_test_split(X, y, test_size=0.4, random_state=0, stratify=y)
yte, p = d, LogisticRegression(max_iter=3000).fit(a, c).predict_proba(b)[:, 1]

fpr, tpr, rthr = roc_curve(yte, p)
i = int(np.argmin(np.abs(tpr - 0.80)))
t = rthr[i]
tn, fp, fn, tp = confusion_matrix(yte, (p >= t).astype(int)).ravel()
print("on %.1f%% positive data, threshold catching 80%% of positives:" % (100*yte.mean()))
print("  false positive rate  %.4f   <- the ROC curve's x-axis" % (fp / (fp + tn)))
print("  precision            %.4f   <- the PR curve's y-axis" % (tp / (tp + fp)))
print()
print("both describe the SAME %d false positives." % fp)
print("  FPR divides by the %d negatives       -> %.4f" % (fp + tn, fp / (fp + tn)))
print("  precision divides by %d rows flagged   -> %.4f wrong" % (tp + fp, fp / (tp + fp)))
print()
print("AUC %.4f and FPR %.1f%% both read like a working model."
      % (roc_auc_score(yte, p), 100 * fp / (fp + tn)))
print("but a human sees %d items, %d real. %.0f%% of the day is wasted."
      % (tp + fp, tp, 100 * fp / (tp + fp)))
print()
print("the rule:")
print("  balanced classes, both errors matter    -> ROC is fine")
print("  rare positives, you care about alerts   -> precision-recall")
print("  comparing across different base rates   -> ROC, PR baseline moves")
print()
print("always print the base rate beside either. an AUC without it is half a sentence.")
```

""",
    [
        {"q": "Why does ROC stay flattering as positives become rare?",
         "options": ["It uses accuracy",
                     "TPR and FPR are each computed within one class, so neither depends on the balance between them",
                     "It ignores false positives",
                     "It is computed at a single threshold"],
         "answer": 1,
         "why": "Adding a million negatives leaves TPR untouched and changes FPR only through its own proportionally larger denominator. Precision's denominator mixes both classes, so it falls."},
        {"q": "10,000 rows, 100 positive, 90% recall and 5% false positive rate. What is precision?",
         "options": ["90%", "About 15%", "About 50%", "5%"],
         "answer": 1,
         "why": "90 true positives against 495 false positives from the 9,900 negatives gives 90/585, about 15%. A 5% FPR sounds excellent and produces five wrong flags for every right one."},
        {"q": "What is the no-skill baseline on a PR curve?",
         "options": ["The diagonal",
                     "A horizontal line at the positive rate",
                     "Always 0.5",
                     "There is none"],
         "answer": 1,
         "why": "It moves with the base rate, which is why a PR AUC must never be quoted without it. 0.4 is poor on balanced data and outstanding at a 2% positive rate."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Threshold tuning
# ---------------------------------------------------------------------------
topic(
    "threshold_tuning",
    "Threshold Tuning",
    "Evaluation",
    "0.5 is a default, not a decision. Set what each kind of mistake costs and "
    "watch the cheapest threshold move away from it.",
    _svg(_axes()
         + '<path d="M22 26 C 50 66, 90 68, 146 34" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + _line(84, 16, 84, 72, B, 1.2, "3 3")
         + _txt(84, 84, "cheapest, not 0.5", M, 8)),
    {
        "sim": "threshold",
        "controls": [
            {"key": "fnCost", "label": "Cost of a miss (false negative)",
             "type": "range", "min": 1, "max": 50, "step": 1, "value": 20},
            {"key": "fpCost", "label": "Cost of a false alarm (false positive)",
             "type": "range", "min": 1, "max": 50, "step": 1, "value": 1},
        ],
        "captions": ["Total cost against threshold"],
    },
    [
        "0.5 is where <code class='mono-font'>predict()</code> happens to cut. "
        "It is not derived from your problem.",
        "The optimal threshold depends on the cost of each error and on the "
        "class balance, neither of which the model knows.",
        "Tune the threshold on validation data, not on the test set, or you have "
        "tuned on the thing you are reporting.",
        "A model whose scores are not calibrated still ranks correctly, so "
        "threshold tuning works even when the probabilities are wrong.",
    ],
    """
title: Threshold Tuning
intro: Where 0.5 came from, why it's almost never right. How to find the number that is.

## Where 0.5 comes from

It comes from the library. `predict()` calls `predict_proba()` and cuts at 0.5,
because a default has to be a thing and 0.5 is the least any-looking
choice available.

It's best under two assumptions that are rarely true together: the classes
are weighed, and the two kinds of mistake cost the same. Change either and 0.5
stops being the right cut.

## Put a price on each mistake

The two sliders set what a false minus and a false plus cost. The curve
is the **total cost** across each threshold, found over 1,500 cases with 20%
positives. The grey line marks 0.5. The orange line marks the cheapest
threshold.

Start with a miss costing 20 and a false alarm costing 1 &mdash; a screening
problem, where investigating a healthy person is cheap and letting a sick one
through isn't. The min sits well below 0.5. The model should flag
generously, because the flags are cheap and the misses aren't.

Now reverse them: a miss at 1 and a false alarm at 50 &mdash; an automated
account suspension, where a wrong suspension is costly and a missed offender
is dealt with later. The min moves above 0.5.

Set them equal and, with these class proportions, the min lands near 0.5 but
not just on it, because the balance is 20/80 rather than 50/50.

## The arithmetic

The expected cost of predicting plus on a case with predicted chance
*p* is `(1 - p) x cost_FP`. Predicting minus costs `p x cost_FN`. Flagging is
worth it when

```
(1 - p) * cost_FP  <  p * cost_FN
```

which rearranges to

```
p  >  cost_FP / (cost_FP + cost_FN)
```

With equal costs that is 0.5. This Is where the default comes from. With a miss
ten times as costly as a false alarm it's 1/11, about 0.09 &mdash; and a
default of 0.5 is then five times too strict.

That formula is worth carrying around. It gives a defensible starting threshold
from two numbers a domain expert can often supply, without any tuning at all.

## When you cannot price the errors

Often no one can put a number on a miss. Three usable fallbacks:

**Raise F1**, or F-beta if one error matters more. This is the least
opinionated option and it's what most people do.

**Fix an operating constraint.** "The team can investigate 200 cases a day" sets
the threshold right: take the top 200 scores. "Precision must be at least
80%" does the same from the other side. These are often more honest than a
metric, because they show what will really happen.

**Choose from the curve.** Plot precision and recall against threshold and pick
the point where the trade-off turns. It's a judgement, but an informed one.

## Two things that must be right

**Tune on validation data.** Choosing the threshold on the test set and then
reporting test speed is the same category of error as tuning
settings there &mdash; the reported number includes the choice you made
to raise it.

**Don't confuse this with calibration.** Threshold tuning takes the scores as
given and picks a cut. Calibration changes the scores so that a score of 0.8
really means 80% of such cases are plus.

They're free. A badly calibrated model can rank just right, and if the
ranking is right, a tuned threshold works fine. But if the threshold is being
derived from the cost formula above, the *p* in it must mean an actual
chance &mdash; and then calibration matters. Platt scaling and isotonic
regression are the usual tools.

## The threshold the costs imply

The best cut isn't a matter of taste. It drops out of the two error costs.
Flagging a case with predicted chance p is worth it when
`(1 - p) &middot; cost_FP < p &middot; cost_FN`. This Rearranges to a threshold of
`cost_FP / (cost_FP + cost_FN)`:

|a miss costs|a false alarm costs|optimal threshold|
|---|---|---|
|20|1 (screening)|0.048|
|1|1 (symmetric)|0.500|
|1|50 (auto-suspension)|0.980|

The familiar 0.5 is just the middle row. The special case where the two
mistakes cost the same. Move to a screening problem. Here Missing a sick patient
is twenty times worse than a needless second look, and the right cut falls to
0.048: flag almost any of it. Flags are cheap and misses aren't, and the
default of 0.5 is then more than ten times too strict. Reverse the costs and it
climbs to 0.98. The formula needs only two numbers a domain expert can often
supply, and it gives a defensible threshold with no tuning at all &mdash; but the
p in it must be an actual chance. This Is why a cost-derived threshold is
just the case where [calibration](probability_calibration.html) stops being
optional.

When no one can price the errors, three fallbacks are honest. Raise F1 (or
F-beta if one error matters more). This Is the least opinionated option. Fix an
operating constraint &mdash; "the team can investigate 200 cases a day" sets the
threshold right as the top 200 scores, and often shows reality better than
any metric. Or read the precision-recall trade-off off the curve and pick the knee.
Whichever you use, tune it on validation data, never the test set: choosing the
threshold to raise a number and then reporting that number folds the choice into
the result, just as tuning settings on the test set does.

## Where it goes wrong

**Reporting metrics at 0.5 and stopping.** The most common test mistake
after using fit.

**Tuning on the test set.** Optimistic by just the amount you gained.

**Retuning per fold and blending.** The thresholds aren't close across
folds. Tune once on a held-out validation set.

**Losing it drifts.** The best threshold depends on the class balance,
and that moves in production. It needs rechecking, not setting once.

## Questions people ask

<strong>Why is 0.5 not always the right threshold?</strong> It assumes both kinds of error cost the same and the classes are balanced. Neither is usually true.

<strong>How do I pick a threshold?</strong> Assign a cost to false positives and false negatives and choose the threshold that minimises expected cost. If you cannot price them, set a recall or precision target.

<strong>On which data should I tune the threshold?</strong> On validation data or cross-validated predictions, not the test set. Then report the final result on test data once.

<strong>Does threshold tuning change the model?</strong> No. It changes only how scores become labels, so ranking metrics like AUC stay the same.

<strong>Do I need calibrated probabilities?</strong> For thresholds derived from costs, yes. A cost-based threshold assumes the probabilities are real, so calibrate first.

<strong>What happens when class balance shifts in production?</strong> The best threshold moves. Monitor the positive rate and re-tune when the distribution changes.

## 0.5 is a default, not a decision

The threshold is the one setting you can change after training, in production, in a config file. Here is what it costs and what it buys.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_auc_score, precision_recall_curve, f1_score
X, y = make_classification(n_samples=8000, n_features=15, n_informative=6,
                           weights=[0.93, 0.07], flip_y=0.06, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.35, random_state=0, stratify=y)
prob = LogisticRegression(max_iter=3000).fit(Xtr, ytr).predict_proba(Xte)[:, 1]
pos = (yte == 1).sum()
print("%d test rows, %d positive (%.1f%%). AUC %.4f -- model is fine."
      % (len(yte), pos, 100*pos/len(yte), roc_auc_score(yte, prob)))
print("the threshold is what is broken.")
print()
print("%10s %8s %8s %10s %9s %9s" % ("threshold", "TP", "FP", "FN", "prec", "recall"))
for t in (0.50, 0.30, 0.20, 0.10, 0.07, 0.03):
    tn, fp, fn, tp = confusion_matrix(yte, (prob >= t).astype(int)).ravel()
    print("%10.2f %8d %8d %10d %9.4f %9.4f"
          % (t, tp, fp, fn, tp/max(tp+fp,1), tp/max(tp+fn,1)))
print()
print("at 0.50 the model catches %d of %d positives." %
      (confusion_matrix(yte, (prob >= 0.5).astype(int)).ravel()[3], pos))
print("0.50 is not cautious -- it is wrong when only %.1f%% of rows are positive."
      % (100*pos/len(yte)))
prec, rec, thr = precision_recall_curve(yte, prob)
f1 = 2*prec*rec / np.clip(prec+rec, 1e-12, None)
best = thr[np.nanargmax(f1[:-1])]
print("best-F1 threshold: %.4f  (F1 %.4f vs %.4f at 0.50)"
      % (best, f1_score(yte, (prob>=best).astype(int)),
         f1_score(yte, (prob>=0.5).astype(int))))
```

F1 is one way to pick a threshold, but a cost matrix is more honest. The next block shows how the same probabilities produce three different optimal thresholds depending on the price of each mistake.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
X, y = make_classification(n_samples=8000, n_features=15, n_informative=6,
                           weights=[0.93, 0.07], flip_y=0.06, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.35, random_state=0, stratify=y)
prob = LogisticRegression(max_iter=3000).fit(Xtr, ytr).predict_proba(Xte)[:, 1]
print("put money on the two mistakes and the answer changes:")
for fp_cost, fn_cost, label in ((1, 1, "equal cost"),
                                (1, 20, "miss costs 20x false alarm"),
                                (20, 1, "false alarm costs 20x miss")):
    costs = [(t, fp_cost*((prob>=t)&(yte==0)).sum()
                +fn_cost*((prob<t)&(yte==1)).sum())
             for t in np.linspace(0.01, 0.95, 300)]
    t_best, c_best = min(costs, key=lambda kv: kv[1])
    c_def = next(c for t, c in costs if abs(t-0.5) < 0.006)
    print("  %-30s best %.3f, cost %6d (at 0.50: %6d)"
          % (label, t_best, c_best, c_def))
print()
print("same model, three different right answers.")
print("the threshold is where business constraints enter the system.")
print("pick it on a validation split, not the test set. re-check it")
print("when the base rate moves -- that is what invalidates it.")
```

""",
    [
        {"q": "Where does the 0.5 default threshold come from?",
         "options": ["It is derived from the training data",
                     "It is the library's default, optimal only when classes are balanced and both errors cost the same",
                     "It maximises accuracy on any dataset",
                     "It is the median predicted probability"],
         "answer": 1,
         "why": "A default has to be something. Change the balance or the relative cost of the two mistakes and 0.5 stops being the right cut."},
        {"q": "If a miss costs ten times a false alarm, roughly what threshold does the cost formula give?",
         "options": ["0.5", "About 0.09", "0.9", "It depends only on the model"],
         "answer": 1,
         "why": "cost_FP / (cost_FP + cost_FN) = 1/11, about 0.09. The default of 0.5 would be about five times too strict for that problem."},
        {"q": "How does threshold tuning differ from calibration?",
         "options": ["They are the same thing",
                     "Tuning picks a cut on the scores as given; calibration changes the scores so 0.8 really means 80%",
                     "Calibration only applies to trees",
                     "Tuning requires the test set"],
         "answer": 1,
         "why": "They are independent. A badly calibrated model can rank perfectly and a tuned threshold still works - but deriving the threshold from the cost formula needs p to be a real probability."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Grid search vs random search
# ---------------------------------------------------------------------------
topic(
    "grid_vs_random_search",
    "Grid Search against Random Search",
    "Tuning",
    "Same budget, two ways of spending it. Grid search tries nine values of "
    "everything; random search tries every value of the one that matters.",
    _svg("".join(_dot(34 + (i % 4) * 26, 24 + (i // 4) * 16, M, 2.4) for i in range(12))
         + _txt(80, 82, "same budget, different coverage", M, 7)),
    {
        "sim": "search",
        "controls": [
            {"key": "method", "label": "Search", "type": "select", "value": "grid",
             "options": [{"value": "grid", "label": "Grid"},
                         {"value": "random", "label": "Random"}]},
            {"key": "budget", "label": "Trials", "type": "range",
             "min": 4, "max": 64, "step": 1, "value": 16},
            {"key": "seed", "label": "Random seed", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 29},
        ],
        "captions": ["Background: the true score surface. Ring: the best point found."],
    },
    [
        "Hyperparameters are not equally important. Usually one or two dominate "
        "and the rest barely matter.",
        "A grid of n&times;n points tries only n distinct values of each "
        "parameter, however large n&times;n is.",
        "The same budget spent randomly tries n&times;n distinct values of each, "
        "so it explores the important one far more finely.",
        "The gap widens with dimension. Bergstra and Bengio made this argument "
        "in 2012 and it has held up.",
    ],
    """
title: Grid Search against Random Search
intro: Why the same number of trials finds a better answer when you stop being systematic.

## The setup

The background shading is the true score surface, and it's on purpose
lopsided. The flat axis is a setting that matters a great deal
&mdash; a learning rate, a smoothing strength. And the vertical axis
is one that barely does. The optimum is a narrow vertical band.

This lopsidedness is the normal case, not a contrived one. In most models one or
two settings dominate and the rest are close to noise, and you often do
not know in advance which is which.

## Count the distinct values

Set the method to **Grid** with 16 trials. Sixteen points appear in a 4&times;4
lattice. Read the line under the chart: 16 trials, **4** distinct values of the
param that matters.

each point in a column shares an x. The other three trials in that column tell
you nothing new about the axis you care about. They only vary the axis
you don't.

Now switch to **Random**, same 16 trials. Sixteen points scattered, and
**16** distinct values of the param that matters. Same cost, four times the
detail where detail counts.

Push the budget to 64. Grid gives 8 distinct values from 64 trials. Random gives
64. The gap widens as the budget grows, and it widens much faster as dims
are added &mdash; a grid over five params at four values each is 1,024
trials and still only four values of each.

## The argument in one line

A grid of *n* points per axis over *d* axes costs *n^d* trials and buys *n*
distinct values of each param. Random search of the same *n^d* trials buys
*n^d* distinct values of each param.

If only one axis matters, grid search has wasted all but *n* of its trials on
that axis. This is Bergstra and Bengio's 2012 result, and it changed default
practice.

## Watch the luck

Move the **seed** slider with random selected. The best point found moves, and
the best score wobbles. Random search is random. A single run can be unlucky.

That is a real cost and a smaller one than it looks. Because the surface is
broad along the unimportant axis, most draws land a place reasonable, and the
distribution of outcomes is much better than grid's ensured coarseness. But
it does mean a single random run isn't a strong claim, and checks should
allow for the variation.

## When grid search is still right

**Few params, truly discrete.** Three kernels, four values of *k*: a
grid is exhaustive and the exhaustiveness is worth having.

**Reproducibility matters more than speed.** A grid is deterministic and
easy to show in a paper.

**You're refining.** Random search to find the region, a small grid to comb it.
This combination is better than either alone.

## What replaced both

**Bayesian optimisation** builds a model of the score surface from the trials so
far and proposes the point most likely to improve. Optuna and Hyperopt do this,
and on costly goals &mdash; where one trial takes an hour &mdash; it's
clearly better than either method here.

**Successive halving** and **Hyperband** attack the cost differently: start many
configurations cheaply, kill the worst, give the survivors more budget. When a
trial's early speed predicts its final speed, this is sharply
more fast.

For any of it cheap, random search remains an great default. It has no
settings of its own, it parallelises just right, and it's very hard to
use wrongly.

## Why random search reaches the good region

Random search's edge over a grid is that it doesn't spend trials
re-measuring the axis that doesn't matter, and its chance of landing in the good
region follows a simple curve. If the top 5% of the space is what you want, `n`
free random draws miss it only if *all* of them do:

|random trials|P(at least one lands in the top 5%)|
|---|---|
|10|0.40|
|20|0.64|
|60|0.95|

Sixty trials find the good region 95% of the time, with no assumption about which
setting matters. A grid of the same 60 trials over two axes gives about 8
distinct values of each, so if only one axis matters it has spent all but 8 of its
trials varying the one that doesn't. And over five axes at four values
each, a grid is 1,024 trials and still only four values per param. That is
Bergstra and Bengio's result, and it's why random beat grid as the default. The
one place it needs care is the sampling scale: a learning rate must be drawn
log-uniformly, because a uniform draw between 0.0001 and 0.1 puts 90% of its
samples above 0.01 and starves the small values that often matter most.

What replaced both methods for costly goals is Bayesian optimisation
&mdash; Optuna, Hyperopt &mdash; which builds a model of the score surface from the
trials so far and proposes the point most likely to improve, clearly better when a
single trial takes an hour. Successive halving and Hyperband attack the cost from
another angle, starting many configurations cheaply and killing the worst, which
wins when early speed predicts final speed. For any of it cheap, random
search remains an great default: it has no settings of its own, it
parallelises just right, and the one way to misuse it. A linear scale on a
param that should be logarithmic. Is the same trap noted above.

## Where it goes wrong

**Sampling scale.** A learning rate should be sampled log-uniformly. Uniform
between 0.0001 and 0.1 puts 90% of the draws above 0.01.

**Tuning on the test set.** Same error as all over else. Tune on validation.

**Searching a range that excludes the answer.** No search finds what is outside
its bounds. Check whether the best value sits at the edge of the range. If it
does, widen it and search again.

**Not searching prep.** Put the whole [pipeline](ml_pipelines.html) in
the search, so imputation and scaling choices are tuned alongside the model.

## Questions people ask

<strong>Is random search always better than grid search?</strong> Not always, but it usually finds a good setting with fewer fits when only a few hyperparameters matter. Grid search is fine for one or two small, discrete parameters.

<strong>How many random samples do I need?</strong> Around 60 random trials gives a good chance of landing in the top 5 percent of the space. More helps with diminishing returns.

<strong>Should I sample on a log scale?</strong> Yes for parameters like learning rate, C and alpha that span orders of magnitude. Use a log-uniform distribution so each scale gets equal attention.

<strong>Why does grid search waste fits?</strong> It repeats the same few values of each parameter across every combination. If one parameter does not matter, you run many near-duplicate experiments.

<strong>What comes after random search?</strong> Bayesian optimisation and successive halving, which use earlier results to choose where to look next. They are worth it when each fit is expensive.

<strong>Can I tune on the test set?</strong> No. Use cross-validation on the training data for the search, and touch the test set once at the end.

## Why random search finds more with fewer fits

Grid search spends its budget evenly across each param, including the ones that don't matter. Random search doesn't. On the same budget it often wins.

```python-run
import numpy as np
import time
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (GridSearchCV, RandomizedSearchCV,
                                     StratifiedKFold, cross_val_score)
from scipy.stats import randint
X, y = make_classification(n_samples=700, n_features=12, n_informative=5,
                           flip_y=0.10, random_state=0)
cv = StratifiedKFold(3, shuffle=True, random_state=0)
print("baseline, all defaults: cv %.4f"
      % cross_val_score(RandomForestClassifier(random_state=0), X, y, cv=cv).mean())

grid = {"n_estimators": [40, 120], "max_depth": [3, 6, 12, None],
        "max_features": [2, 4, 8]}
total = 2 * 4 * 3
print("grid search over %d combinations x 3 folds = %d fits" % (total, total * 3))
t0 = time.time()
gs = GridSearchCV(RandomForestClassifier(random_state=0), grid, cv=cv).fit(X, y)
print("  best %.4f in %.1fs with %s" % (gs.best_score_, time.time()-t0, gs.best_params_))

dist = {"n_estimators": randint(40, 120), "max_depth": randint(2, 20),
        "max_features": randint(1, 12)}
t0 = time.time()
rs = RandomizedSearchCV(RandomForestClassifier(random_state=0), dist,
                        n_iter=total, cv=cv, random_state=0).fit(X, y)
print("random search, the SAME %d fits" % total)
print("  best %.4f in %.1fs with %s" % (rs.best_score_, time.time()-t0, rs.best_params_))
print()
print("how many DISTINCT values does each parameter get tried at?")
print("  grid   : n_estimators 2, max_depth 4, max_features 3")
print("  random : n_estimators %d, max_depth %d, max_features %d"
      % tuple(len(set(r[k] for r in rs.cv_results_["params"]))
              for k in ("n_estimators", "max_depth", "max_features")))
print("  random gets 24 distinct values of every parameter, so it never")
print("  wastes budget on a parameter that turns out not to matter.")
```

The next block shows why log-uniform distributions matter and demonstrates SVM tuning.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.svm import SVC
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from scipy.stats import loguniform
X, y = make_classification(n_samples=700, n_features=12, n_informative=5,
                           flip_y=0.10, random_state=0)
cv = StratifiedKFold(3, shuffle=True, random_state=0)

print("grids explode. adding one parameter with 4 values multiplies:")
for extra in range(5):
    print("  %d parameters at 4 values each -> %5d combinations"
          % (extra + 1, 4 ** (extra + 1)))
print()
print("scales matter -- C and gamma live on a log scale:")
print("  linear range 0.1 to 100 in 5 steps:", np.round(np.linspace(0.1, 100, 5), 3))
print("  log range,   same endpoints      :", np.round(np.logspace(-1, 2, 5), 3))
print("  the linear one puts 4 of 5 samples above 25, which is almost")
print("  never where the interesting values are.")
print()
svm_rs = RandomizedSearchCV(make_pipeline(StandardScaler(), SVC()),
                            {"svc__C": loguniform(1e-2, 1e3),
                             "svc__gamma": loguniform(1e-4, 1e0)},
                            n_iter=15, cv=cv, random_state=0).fit(X, y)
print("SVM tuned over log-uniform ranges, 15 draws: cv %.4f" % svm_rs.best_score_)
print("  C %.4f, gamma %.5f"
      % (svm_rs.best_params_["svc__C"], svm_rs.best_params_["svc__gamma"]))
print()
print("rule of thumb: grid when you have 2 parameters and know the ranges,")
print("random when you have more than 2 or are still exploring. always")
print("check if the best value landed on the edge -- if it did, the range")
print("was wrong, not the model.")
```

""",
    [
        {"q": "Why does a 4x4 grid of 16 trials explore an important hyperparameter poorly?",
         "options": ["Grids are slower",
                     "All four points in a column share the same value, so 16 trials give only 4 distinct values of that parameter",
                     "It cannot sample the edges",
                     "The lattice is biased toward the centre"],
         "answer": 1,
         "why": "The other trials in a column vary only the axis that does not matter. Random search of the same 16 trials gives 16 distinct values of every parameter."},
        {"q": "How should a learning rate be sampled in a random search?",
         "options": ["Uniformly between the bounds",
                     "Log-uniformly",
                     "Normally around the default",
                     "In equal steps"],
         "answer": 1,
         "why": "Uniform sampling between 0.0001 and 0.1 puts about 90% of the draws above 0.01, which leaves the small-value region essentially unexplored."},
        {"q": "What should you check if the best value found sits at the edge of the search range?",
         "options": ["Nothing, edges are common",
                     "Widen the range - no search finds what lies outside its bounds",
                     "Reduce the number of trials",
                     "Switch to grid search"],
         "answer": 1,
         "why": "A best value at the boundary is evidence the optimum is beyond it. The search reported the best point it was allowed to consider, not the best point."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Learning curves
# ---------------------------------------------------------------------------
topic(
    "learning_curves",
    "Learning Curves",
    "Diagnosis",
    "Two lines that tell you whether to collect more data or change the model "
    "&mdash; and they give different answers.",
    _svg(_axes()
         + '<path d="M24 62 C 60 56, 100 54, 146 53" fill="none" stroke="%s" stroke-width="1.8"/>' % M
         + '<path d="M24 22 C 60 34, 100 44, 146 48" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + _txt(100, 74, "gap = variance", M, 7)),
    {
        "sim": "learning",
        "controls": [
            {"key": "capacity", "label": "Model capacity", "type": "range",
             "min": 1, "max": 9, "step": 1, "value": 2},
        ],
        "captions": ["Grey: training error. Orange: validation error."],
    },
    [
        "Plot training and validation error against the number of training "
        "examples. The shape is the diagnosis.",
        "Both high and converged: <strong>bias</strong>. The model is too simple, "
        "and more data will not help.",
        "Low training error with a large gap: <strong>variance</strong>. More "
        "data or less capacity will help.",
        "A validation curve that has flattened is the honest answer to 'should "
        "we collect more data'. It is no.",
    ],
    """
title: Learning Curves
intro: The plot that answers whether to collect more data. Saves you from collecting it pointlessly.

## What is plotted

A learning curve answers a single question: will more data help? The answer
saves real money. Collecting and labelling another 50,000 rows is expensive.
If the model has already stopped improving, that cost is wasted. The curve
tells you before you spend it.

Train the model on 40 examples, record the error on those examples and on a
held-out validation set. Repeat with 80, 120, and so on. Plot both against
training-set size. Grey is training error, orange is validation error.

The **shape** of the pair is the diagnosis, and the diagnosis is more
useful than either number alone. A gap that keeps closing says more data
will help. A gap that has already flattened says it will not. Two lines
that sit high and close together say the model itself is the problem,
not the data. This page walks through each of those shapes and what to
do about them.

## Underfitting

Set room to 1 or 2. Both curves rise quickly to a plateau, sit close
together, and stay high.

Training error is high. This Is the tell. The model can't fit the data it has
already seen, so nothing about unseen data is the problem. This is **bias**: the
model is too simple for the structure present.

The key consequence is minus. **More data won't help.** The curves
have already settled. Adding examples moves neither. Money spent on collection
here is wasted, and this plot is the cheapest way to find that out before
spending it.

What helps instead: more room, better features, less smoothing, a
different model class.

## Overfitting

Set room to 8 or 9. Training error drops close to zero, validation error
stays well above it, and a wide gap opens between them.

The model fits its training data nearly just right and generalises poorly. This is
**variance**: capacity is being spent memorising noise.

Here more data *does* help, and the curve says so. The validation line is
still falling at the right-hand edge. each extra example makes the noise
harder to store. Other options: reduce room, add smoothing,
boost the data, or ensemble.

## About right

Set room to 4 or 5. The curves settle to a small gap at a low error, and
both have flattened.

The readout says as much. There's no obvious bias and no obvious variance, and
the flattening is the answer to "should we collect more data": no, not for this
model. Improvement would have to come from features or from a different model
class, not from volume.

## The summary

| Training error | Gap | Diagnosis | Do |
|---|---|---|---|
| High | Small | Bias | more capacity, better features |
| Low | Large | Variance | more data, regularisation, less capacity |
| Low | Small | Fine | features or a different model |
| High | Large | Something is wrong | check the split and the labels |

That last row is worth keeping. High training error *and* a large gap shouldn't
happen from bias or variance alone, and often means a bug &mdash; leakage in
reverse, mislabelled data, or a validation set drawn from a different
spread.

## Where the curve is still falling

The single most valuable thing here is being able to answer "will more data
help" with evidence.

If the validation curve is still descending at your current dataset size,
collecting more will improve the model, and the slope gives a rough sense of how
much. If it has been flat for the last few points, more data buys nothing, and
the effort belongs elsewhere.

That question is or else answered by intuition, and it often involves real
money.

## Practical notes

The curves are noisy at small sizes. A model trained on 40 examples
depends heavily on which 40. Mean over a few splits, and plot the spread if
you can.

Use the same validation set at each size. Growing it alongside the training set
confounds two changes.

And don't confuse this with a **validation curve**. This Plots error against a
setting at fixed data size. Both are handy and they answer different
questions: learning curves ask about data, validation curves ask about a setting.

## Reading the four shapes

The diagnosis is the *pair* of curves, not either number, and four combinations
cover each case:

|training error|gap to validation|diagnosis|what helps|
|---|---|---|---|
|high|small|bias (underfit)|more capacity, better features|
|low|large|variance (overfit)|**more data**, regularisation, less capacity|
|low|small|about right|features or a different model, not volume|
|high|large|a bug|check the split, the labels, for leakage|

The one that saves real money is the top row against the second. Both look like a
model that could be better. But They answer "should we collect more data" in
opposite directions. In the bias case both curves have already flattened and sit
close together and high &mdash; the model can't even fit what it has, so more of
the same data moves nothing, and the plot is the cheapest way to learn that before
paying for collection. In the variance case the validation curve is still falling
at the right-hand edge, so each extra example makes the noise harder to store
and the gap narrows. The rule is precise: a *settled* gap is variance you can't
buy your way out of. A still-descending validation curve is the one that justifies
the data budget.

Two hands-on cautions keep the diagnosis honest. The curves are noisy at small
training sizes, because a model fitted on 40 examples depends heavily on *which*
40, so mean over a few splits before reading a shape into them. And use the
same validation set at each training size. Growing it alongside the
training set confounds two changes and muddies the very gap you're trying to read.
The learning curve, which varies the amount of data, is also not to be confused
with a validation curve. This Varies a setting at fixed data size: both are
handy and they answer different questions, one about collection and one about a
setting.

## Where it goes wrong

**Reading a single run.** Small-sample noise looks like structure.

**Plotting fit on imbalanced data.** The curves will be flat and
uninformative. Plot the metric you really care about.

**Concluding 'more data' from a gap alone.** Check the validation curve is still
falling. A settled gap means variance you can't fix with volume.

## Questions people ask

<strong>What does a learning curve show?</strong> Training and validation scores as the training set grows. It tells you whether more data, a bigger model or a simpler model is likely to help.

<strong>How do I recognise overfitting?</strong> Training score stays high while validation score sits well below it. A wide gap that does not close with more data points to overfitting.

<strong>How do I recognise underfitting?</strong> Both scores are low and close together. More data will not help, so try a more flexible model or better features.

<strong>Will more data help?</strong> If the validation curve is still rising at the right edge, yes. If it has flattened, more data of the same kind will give little.

<strong>How is this different from a validation curve?</strong> A learning curve varies training set size. A validation curve varies one hyperparameter, such as tree depth, at a fixed size.

<strong>Why are the curves noisy?</strong> Each point comes from a finite cross-validation run on a small subset. Use more folds or repeats, and look at the shaded spread.

## The chart that tells you whether more data will help

Two models on the same problem, scored as the training set grows. One curve says collect more data. The other says don't bother. Reading the difference is the whole skill.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import learning_curve, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
X, y = make_classification(n_samples=4000, n_features=12, n_informative=6,
                           n_clusters_per_class=2, flip_y=0.08, random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
sizes = np.array([50, 100, 250, 600, 1500, 3200])
def curve(name, model, verdict):
    n, tr, te = learning_curve(model, X, y, train_sizes=sizes, cv=cv,
                               scoring="accuracy")
    print(name)
    print("%10s %10s %10s %8s" % ("rows", "train", "val", "gap"))
    for i in range(len(n)):
        print("%10d %10.4f %10.4f %8.4f"
              % (n[i], tr[i].mean(), te[i].mean(), tr[i].mean()-te[i].mean()))
    print("  verdict: %s" % verdict)
    print()
curve("UNDERFITTING -- linear on a non-linear problem",
      make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
      "both low and flat. more data changes nothing.")
curve("OVERFITTING -- unbounded decision tree",
      DecisionTreeClassifier(random_state=0),
      "train near 1.0, val far behind and still rising. more data helps.")
```

The next block adds a well-fitted model and summarises the three shapes.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import learning_curve, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
X, y = make_classification(n_samples=4000, n_features=12, n_informative=6,
                           n_clusters_per_class=2, flip_y=0.08, random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
sizes = np.array([50, 100, 250, 600, 1500, 3200])
def curve(name, model, verdict):
    n, tr, te = learning_curve(model, X, y, train_sizes=sizes, cv=cv,
                               scoring="accuracy")
    print(name)
    print("%10s %10s %10s %8s" % ("rows", "train", "val", "gap"))
    for i in range(len(n)):
        print("%10d %10.4f %10.4f %8.4f"
              % (n[i], tr[i].mean(), te[i].mean(), tr[i].mean()-te[i].mean()))
    print("  verdict: %s" % verdict)
    print()
curve("GOOD FIT -- degree-2 features on a linear model",
      make_pipeline(StandardScaler(), PolynomialFeatures(2),
                    LogisticRegression(max_iter=5000)),
      "small gap, val flat. you have enough data.")
print("the three shapes:")
print("  both low, together       -> underfitting. get a better model.")
print("  big gap, val still rising -> overfitting. get more data or regularise.")
print("  small gap, both flat      -> done. remaining error is label noise.")
print()
print("plot this BEFORE collecting data. the curve answers 'would another")
print("10,000 rows help' using data you already have.")
```

""",
    [
        {"q": "Training error is high and the two curves have converged. What does that mean?",
         "options": ["Variance - collect more data",
                     "Bias - the model is too simple, and more data will not help",
                     "The split is wrong",
                     "The model is well fitted"],
         "answer": 1,
         "why": "The model cannot fit data it has already seen, so unseen data is not the problem. The curves have already converged, so adding examples moves neither."},
        {"q": "What tells you whether collecting more data will help?",
         "options": ["The size of the gap",
                     "Whether the validation curve is still falling at your current dataset size",
                     "The training error alone",
                     "The number of features"],
         "answer": 1,
         "why": "A still-descending validation curve means more examples will improve the model, and its slope suggests by how much. A flat one means the effort belongs elsewhere."},
        {"q": "High training error AND a large gap suggests what?",
         "options": ["Severe overfitting",
                     "A bug - check the split, the labels, and whether validation comes from a different distribution",
                     "Ideal capacity",
                     "Too much regularisation"],
         "answer": 1,
         "why": "Bias and variance alone do not produce that combination. It usually means mislabelled data or a validation set drawn from somewhere else."},
    ],
)

# ---------------------------------------------------------------------------
# 11. DBSCAN
# ---------------------------------------------------------------------------
topic(
    "dbscan_clustering",
    "DBSCAN: Density-Based Clustering",
    "Clustering",
    "Clusters defined by crowding rather than by distance to a centre, which "
    "is why it finds shapes k-means cannot.",
    _svg(_axes()
         + "".join(_dot(28 + i * 5, 58 - (i % 3) * 4, A) for i in range(9))
         + "".join(_dot(84 + i * 5, 34 + (i % 3) * 4, A) for i in range(9))
         + _dot(70, 20, M) + _dot(126, 62, M)
         + _txt(80, 82, "two shapes, two outliers", M, 7)),
    {
        "sim": "dbscan",
        "controls": [
            {"key": "shape", "label": "Data", "type": "select", "value": "moons",
             "options": [{"value": "moons", "label": "Two crescents"},
                         {"value": "blobs", "label": "Three blobs and some noise"}]},
            {"key": "eps", "label": "eps (neighbourhood radius)", "type": "range",
             "min": 0.10, "max": 0.60, "step": 0.01, "value": 0.24},
            {"key": "minPts", "label": "minPts", "type": "range",
             "min": 2, "max": 12, "step": 1, "value": 5},
        ],
    },
    [
        "A <strong>core point</strong> has at least <code class='mono-font'>minPts</code> "
        "neighbours within <code class='mono-font'>eps</code>. Clusters grow outward from core points.",
        "Points reachable from a core point but not core themselves are "
        "<strong>border</strong> points. Everything else is <strong>noise</strong>.",
        "You never say how many clusters to find. The density parameters decide, "
        "and the count falls out.",
        "Because clusters spread through connected dense regions, they can be any "
        "shape at all &mdash; which is what k-means cannot do.",
    ],
    """
title: DBSCAN: Density-Based Clustering
intro: Clustering by crowding rather than by distance to a centre. The two params that decide all.

## What k-means cannot do

Set the data control above to **Two crescents**. K-means, which assigns each
point to the nearest of *k* centres, can't separate these: the boundary it
draws is always a straight line between two centroids, and no straight line
separates two interleaved crescents.

DBSCAN separates them right away, and does it without being told there are two.

## The definitions

All follows from two params. `eps`, a radius, and `minPts`, a
count &mdash; and three meanings:

**Core point.** Has at least `minPts` points within `eps` of it, including
itself. It sits in a crowded place.

**Border point.** Within `eps` of a core point. But Not crowded enough to be one
itself. It's on the edge of a cluster.

**Noise.** Neither. It belongs to no cluster, and DBSCAN says so rather than
forcing it a place.

A cluster is then a maximal set of points connected through core points. Start at
a core point, take all within `eps`. For each of those that is also a
core point, take *its* zone too, repeating until nothing new arrives.

This is why clusters can be any shape. The cluster spreads wherever the data is
dense, following the crescent around its curve. At no point does it ask
how far any of it's from a centre.

## The two parameters

Drag `eps` in the visualisation and watch the count.

**Too small**, and no point has `minPts` neighbours. All is noise, or the
data shatters into many small clusters.

**Too large**, and all is within reach of all else. The two
crescents merge into one cluster. This Happens just above 0.25 on this data.

The band in between is where DBSCAN works, and on the crescents it's truly
narrow. That sensitivity is the honest weakness of the method.

`minPts` is less delicate. Larger values demand denser cores, making fewer,
tighter clusters and more noise. A common starting rule is `minPts = 2 * number
of dims`, and at least 3.

For `eps`, the standard technique is a **k-distance plot**: for each point,
measure the distance to its `minPts`-th nearest neighbour, sort those distances
and plot them. The curve has a knee where distances start rising sharply, and
that knee is a reasonable `eps`. It's the point at which you leave the
dense region and start crossing gaps.

## What it gives you that k-means does not

**No k.** The number of clusters is found, not supplied.

**Any shapes.** Crescents, rings, spirals, any of it connected and dense.

**An clear noise label.** K-means assigns each point to some cluster, so an
outlier is silently absorbed and drags a centroid with it. DBSCAN sets it aside.
Switch the data to blobs and the scattered points stay hollow.

## Where it fails

**Varying density.** This is the real limitation. One `eps` applies all over,
so a dataset with one dense cluster and one sparse cluster can't be handled: the
`eps` that finds the sparse one merges the dense one into its surroundings.
**HDBSCAN** exists just for this, building a hierarchy over `eps` values and
selecting per cluster.

**High dims.** Distances focus as dimensionality grows, so
"zone" stops meaning much. Reduce dims first.

**Scale sensitivity.** `eps` is an abs distance. So A feature measured in
thousands dominates one measured in units. [Scale
first](feature_scaling.html) &mdash; this isn't optional.

**Cost.** Naively O(n&sup2;) because of the zone queries. A spatial
index brings it to about O(n log n) in low dims.

## Core, border and noise, counted

The three meanings become concrete the moment you apply them. Take eps = 1.5,
minPts = 3, and a point whose 1.5-radius zone is being checked:

|point|neighbours within eps (incl. itself)|type|
|---|---|---|
|in a dense cluster|5|**core** (&ge; minPts)|
|on a cluster edge|2, but one is a core point|**border**|
|off on its own|1|**noise**|

A cluster is then all reachable through core points: start at a core point,
absorb its zone, and for each neighbour that is *also* core, absorb its
zone too, until nothing new arrives. That chain-through-cores rule is why
DBSCAN follows a crescent around its curve. It never measures distance to a
centre, only local crowding &mdash; and why it labels the lone point noise instead
of forcing it into a cluster and dragging a centroid toward it, as k-means must.
The cost is that one eps applies all over: raise it past the gap between two
groups and they merge, drop it below the spacing of a sparse cluster and that
whole cluster turns noise. On data with one dense and one sparse cluster no
single eps works, which is just what HDBSCAN was built to fix.

Choosing eps isn't guesswork either: the standard technique is a k-distance plot,
where you measure each point's distance to its minPts-th nearest neighbour, sort
those distances and look for the knee. The point where they start rising
sharply is where you leave the dense region and begin crossing gaps, and it makes a
defensible eps. minPts is the less delicate of the two, with a common starting rule
of twice the number of dims. The method's real ceiling is high dimensionality:
distances focus as dims grow until "zone" stops meaning much,
so reducing dims first isn't optional, and neither is scaling, since eps is a
single abs distance applied to each feature at once.

## Where it goes wrong

**Not scaling the features.** `eps` turns meaningless.

**Tuning eps by trying numbers.** Use a k-distance plot. It takes a minute and
gives a defensible value.

**Expecting it to work on varying density.** Reach for HDBSCAN instead.

**Reading noise as failure.** Labelling outliers as noise is the feature, not a
bug to fix.

## Questions people ask

<strong>How do I choose eps?</strong> Plot each point's distance to its k-th nearest neighbour, sorted, and pick the value at the bend of the curve. Domain knowledge about what counts as close helps too.

<strong>How do I choose min_samples?</strong> A common start is twice the number of features, or at least 4 or 5 for 2D data. Raise it for noisier data so that small chance groupings do not become clusters.

<strong>What does a label of -1 mean?</strong> It marks noise, a point that is neither a core point nor within eps of one. DBSCAN does not force every point into a cluster.

<strong>Does DBSCAN need feature scaling?</strong> Yes. Eps is a single distance applied to all features, so a large-scale feature will dominate unless you standardise first.

<strong>Why does DBSCAN struggle with varied densities?</strong> One eps cannot fit both a tight cluster and a loose one. Either the loose cluster is split into noise or the tight clusters merge. HDBSCAN handles this better.

<strong>Is DBSCAN better than k-means?</strong> It is better for odd shapes and for flagging outliers, and you do not give it k. K-means is faster and gives every point a cluster, which suits round, similar-sized groups.

## Clusters by density, and the points left over

DBSCAN finds shapes k-means can't, decides the number of clusters itself. Labels outliers as noise instead of forcing them a place.

```python-run
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_moons
from sklearn.metrics import adjusted_rand_score

X, y = make_moons(n_samples=600, noise=0.07, random_state=0)

db = DBSCAN(eps=0.2, min_samples=5).fit(X)
km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
print("two interleaving crescents -- not round, not separable by a line:")
print("  DBSCAN  found %d clusters, agreement %.4f"
      % (len(set(db.labels_)) - (1 if -1 in db.labels_ else 0),
         adjusted_rand_score(y, db.labels_)))
print("  k-means told to find 2, agreement %.4f" % adjusted_rand_score(y, km.labels_))
print("  k-means splits them down the middle. it can only draw straight lines.")
print()

Xn = np.vstack([X, np.random.default_rng(0).uniform(-2, 3, (40, 2))])
db2 = DBSCAN(eps=0.2, min_samples=5).fit(Xn)
print("add 40 scattered junk points:")
print("  DBSCAN labelled %d of them noise (label -1)" % (db2.labels_ == -1).sum())
print("  k-means has no such label. every point joins a cluster.")
print()

print("eps is the radius that defines 'nearby'. it decides everything:")
print("%8s %12s %10s" % ("eps", "clusters", "noise"))
for eps in (0.05, 0.10, 0.20, 0.40, 1.00):
    d = DBSCAN(eps=eps, min_samples=5).fit(X)
    n_clusters = len(set(d.labels_)) - (1 if -1 in d.labels_ else 0)
    print("%8.2f %12d %10d" % (eps, n_clusters, (d.labels_ == -1).sum()))
print("  too small: everything is noise. too large: one blob.")
```

The next block shows how to choose eps from the data and how min_samples affects the result.

```python-run
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons, make_blobs
from sklearn.neighbors import NearestNeighbors

X, _ = make_moons(n_samples=600, noise=0.07, random_state=0)

print("choosing eps -- distance to the 5th nearest neighbour:")
d, _ = NearestNeighbors(n_neighbors=5).fit(X).kneighbors(X)
k_dist = np.sort(d[:, -1])
for q in (50, 75, 90, 95, 99):
    print("  %2dth percentile: %.4f" % (q, np.percentile(k_dist, q)))
print("  the elbow points at roughly 0.10, and eps=0.10 recovers both crescents.")
print("  0.20 also works. you want a plateau, not one correct number.")
print()

print("min_samples sets how crowded a neighbourhood must be:")
for ms in (3, 5, 10, 30, 60, 120):
    d2 = DBSCAN(eps=0.2, min_samples=ms).fit(X)
    print("  min_samples=%2d -> %d clusters, %d noise"
          % (ms, len(set(d2.labels_)) - (1 if -1 in d2.labels_ else 0),
             (d2.labels_ == -1).sum()))
print("  raise it far enough and even the crescents stop counting as dense.")
print()
print("where it struggles: clusters of very different density.")
Xa, _ = make_blobs(n_samples=[300, 300], centers=[[0, 0], [6, 6]],
                   cluster_std=[0.3, 2.0], random_state=0)
for eps in (0.3, 0.8, 1.5):
    d3 = DBSCAN(eps=eps, min_samples=5).fit(Xa)
    print("  eps=%.1f -> %d clusters, %d noise"
          % (eps, len(set(d3.labels_)) - (1 if -1 in d3.labels_ else 0),
             (d3.labels_ == -1).sum()))
```

""",
    [
        {"q": "Why can DBSCAN separate two interleaved crescents when k-means cannot?",
         "options": ["It uses more iterations",
                     "Clusters spread through connected dense regions, so they can be any shape, while k-means draws straight boundaries between centres",
                     "It scales the features first",
                     "It knows the number of clusters"],
         "answer": 1,
         "why": "K-means assigns each point to the nearest centroid, so the boundary is always a straight line. DBSCAN never asks how far anything is from a centre."},
        {"q": "What is a border point?",
         "options": ["A point at the edge of the dataset",
                     "A point within eps of a core point but without enough neighbours to be core itself",
                     "A point equidistant from two clusters",
                     "A point labelled noise"],
         "answer": 1,
         "why": "Core points have at least minPts neighbours within eps and drive the expansion; border points get swept in by them; everything else is noise."},
        {"q": "What is DBSCAN's main structural weakness?",
         "options": ["It needs k in advance",
                     "One eps applies everywhere, so clusters of differing density cannot both be found",
                     "It cannot label outliers",
                     "It only works in two dimensions"],
         "answer": 1,
         "why": "The eps that finds a sparse cluster merges a dense one into its surroundings. HDBSCAN builds a hierarchy over eps values to handle exactly this."},
    ],
)


# ---------------------------------------------------------------------------
# 12. Hierarchical clustering
# ---------------------------------------------------------------------------
topic(
    "hierarchical_clustering",
    "Hierarchical Clustering and Dendrograms",
    "Clustering",
    "Merge the two closest clusters, repeat, and keep the whole tree. Choose "
    "how many clusters you want afterwards.",
    _svg(_line(24, 70, 24, 46, B, 1.2) + _line(44, 70, 44, 46, B, 1.2)
         + _line(24, 46, 44, 46, A, 1.4) + _line(34, 46, 34, 28, A, 1.4)
         + _line(74, 70, 74, 36, B, 1.2) + _line(104, 70, 104, 36, B, 1.2)
         + _line(74, 36, 104, 36, A, 1.4) + _line(89, 36, 89, 28, A, 1.4)
         + _line(34, 28, 89, 28, A, 1.6)
         + _txt(80, 82, "one tree, every k at once", M, 7)),
    {
        "sim": "hierarchical",
        "controls": [
            {"key": "linkage", "label": "Linkage", "type": "select", "value": "average",
             "options": [{"value": "single", "label": "Single (nearest pair)"},
                         {"value": "complete", "label": "Complete (furthest pair)"},
                         {"value": "average", "label": "Average"}]},
            {"key": "cut", "label": "Cut height", "type": "range",
             "min": 0.10, "max": 1.40, "step": 0.02, "value": 0.60},
        ],
    },
    [
        "Start with every point as its own cluster. Repeatedly merge the two "
        "closest, until one remains.",
        "The result is a tree. Cutting it at a height gives a clustering &mdash; "
        "and every height gives a different k.",
        "<strong>Linkage</strong> defines the distance between two clusters, and "
        "changes the answer more than any other choice.",
        "Single linkage chains through bridges; complete linkage insists on tight "
        "clusters; average sits between them.",
    ],
    """
title: Hierarchical Clustering and Dendrograms
intro: Building the whole tree once. Choosing how many clusters you want after seeing it.

## The algorithm

Agglomerative clustering is almost trivially simple:

1. each point starts as its own cluster.
2. Find the two closest clusters and merge them.
3. Repeat until one cluster remains.

Recording the distance at each merge gives a **dendrogram** &mdash; the chart
above plots just that: merge number against the distance at which it
happened.

## The point: k comes last

K-means and DBSCAN both need a choice before they run &mdash; how many
clusters, or how dense. Hierarchical clustering needs neither. It builds one
tree, and a flat cut through it makes a clustering.

Drag the cut height and watch the count change. A cut low down leaves many small
clusters, a cut high up leaves few, and the tree itself never changed. That is
truly handy when you don't know what structure to expect, because you can
look at the merge distances before committing.

Large jumps in the curve are helpful: a merge that costs much more than the
one before it joined two things that weren't really close. Cutting just below a
big jump is the dendrogram equal of the [elbow](choosing_k.html).

## Linkage changes everything

The method needs a distance between two *clusters*, not two points, and there
is no single right answer. Switch the control and the shape of the curve changes
a lot.

**Single linkage** &mdash; distance between the nearest pair. Merges cheaply
when any two members are close. So It can follow elongated shapes. Its
failure mode is **chaining**: two well-separated blobs joined by a thin bridge of
points merge into one, because the bridge gives a short hop at each step.

**Complete linkage** &mdash; distance between the furthest pair. A merge is only
cheap if *each* member of one cluster is close to each member of the other, so
clusters come out compact and roughly equal in diameter. It breaks up elongated
structures that truly belong together, and is sensitive to outliers, since
one distant member sets the whole distance.

**Mean linkage** &mdash; the mean over all cross-pairs. Between the two, and
the usual default.

**Ward linkage**, not offered here, merges the pair that grows within-cluster
variance least. It behaves much like k-means and is the most common choice for
roughly spherical clusters.

| Linkage | Produces | Fails at |
|---|---|---|
| Single | elongated, chain-following | bridges between clusters |
| Complete | compact, similar sized | genuinely elongated clusters |
| Average | a compromise | nothing dramatic |
| Ward | spherical, balanced | non-convex shapes |

## Reading a real dendrogram

A conventional dendrogram draws each merge as a bracket at its height, with the
leaves at the bottom. Two things are worth knowing about reading one.

**Height is real. Flat spot isn't.** The left-to-right order is
chosen to keep the drawing untangled and carries no info. Two adjacent
leaves aren't always similar.

**The tree is greedy and permanent.** Once two clusters merge they never
separate, so an early mistake. Two points joined because of noise &mdash;
passes all the way up. Hierarchical clustering doesn't revisit choices.

## Cost

The naive method is O(n&sup3;), and careful setups reach O(n&sup2;
log n) with O(n&sup2;) memory for the distance mat. That memory is often the
binding constraint: 100,000 points is a mat of ten billion distances.

This is why hierarchical clustering is a small-to-medium-data method. Above a few
tens of thousands of points, k-means or a sampled variant is the hands-on
choice.

## Linkage, on two little clusters

"There's no single right answer" for the distance between two clusters is easiest
to see on numbers. Cluster A = {0, 1}, cluster B = {5, 9}. The four cross-pair
distances are 5, 9, 4, 8, and each linkage reads a different one:

|linkage|cluster distance|from|
|---|---|---|
|single (nearest pair)|4|1 to 5|
|complete (furthest pair)|9|0 to 9|
|average (mean of all four)|6.5|(5+9+4+8)/4|

Single linkage merges as soon as *any* two members are close. This Lets it follow
an elongated shape but also lets a thin bridge of points chain two separate blobs
into one. Complete linkage merges only when *each* member is close, giving compact
clusters but breaking truly stretched ones and taking its distance from a
single furthest outlier. Mean sits between them and is the usual default. The
same three points would cut the tree at three different heights. This Is why the
dendrogram's shape &mdash; and any k read off it &mdash; changes fully with
the linkage rule, before the data has changed at all. And the whole thing carries
an O(n&sup2;) distance mat: 100,000 points is ten billion distances, which is
the memory wall that keeps this a small-to-medium-data method.

Two more properties are worth carrying. The tree is *greedy and permanent*: once
two clusters merge they never separate. So A mistake made early &mdash; two points
joined because of noise &mdash; rides all the way up the dendrogram, because the
method never revisits a choice. And the left-to-right order of the leaves
carries no info. It's chosen only to keep the drawing untangled, so two
adjacent leaves aren't always similar. Height in the diagram is real
&mdash; it's the distance at which a merge happened, and a large vertical jump
means two things that weren't really close were forced together &mdash; but
flat spot is decoration.

Ward linkage, not among the three above, merges the pair that grows
within-cluster variance least. It behaves much like k-means and is the usual choice
for roughly spherical clusters. This Rounds out the rule of thumb &mdash; single
for elongated shapes, complete for compact ones, mean as a safe middle, Ward
when the clusters are blobs.

## Where it goes wrong

**Not scaling the features.** As with each distance-based method.

**Using single linkage on data with any bridge between clusters.** Chaining will
merge them.

**Reading meaning into leaf order.** It's a drawing rule.

**Trying it on a large dataset.** The distance mat won't fit.

## Questions people ask

<strong>What is a dendrogram?</strong> A tree showing the order in which clusters merge and the distance at each merge. Cut it at a height to get a flat set of clusters.

<strong>Which linkage should I use?</strong> Ward is a good default for compact, similar-sized clusters. Single linkage finds chains but is sensitive to noise, and average and complete sit in between.

<strong>How do I choose where to cut the dendrogram?</strong> Look for a long vertical gap with no merges, and cut within it. That gap shows the clusters are well separated at that level.

<strong>Does hierarchical clustering scale to large datasets?</strong> Poorly. It needs the pairwise distance matrix, so memory grows with the square of the number of points. Beyond tens of thousands of rows, use k-means or a sampled subset.

<strong>Do I need to scale features?</strong> Yes, because distances drive every merge. A large-scale feature will dominate otherwise.

<strong>Can I undo a merge?</strong> No. Agglomerative merges are final, so an early bad merge stays in the tree.

## Cluster without choosing k first

Agglomerative clustering merges the two closest groups over and over. You get each k at once. The linkage rule decides what "closest" means. It changes the answer fully.

```python-run
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score, silhouette_score
from scipy.cluster.hierarchy import linkage, fcluster

X, y = make_blobs(n_samples=300, centers=4, cluster_std=1.0, random_state=0)

Z = linkage(X, method="ward")
print("the merge log -- 299 merges, each joining two groups into one.")
print("%8s %8s %8s %12s %10s" % ("step", "group A", "group B", "distance", "size"))
for i in list(range(3)) + list(range(len(Z) - 5, len(Z))):
    a, b, d, n = Z[i]
    print("%8d %8d %8d %12.4f %10d" % (i, a, b, d, n))
print("  first merges: single points at almost no distance.")
print("  last merges: whole clusters across large gaps.")
print()

print("the last few merge distances, and the jump before each:")
for i in range(len(Z) - 6, len(Z) - 1):
    print("  cut here -> %d clusters   next merge costs %8.3f (%.2fx the last)"
          % (len(X) - i - 1, Z[i, 2], Z[i, 2] / Z[i - 1, 2]))
print("  cut here -> 1 cluster    the root, %8.3f" % Z[-1, 2])
print()
print("  'find the biggest jump' always answers 2. the useful reading is")
print("  where the RATIO stops being dramatic -- a judgement call,")
print("  which is why the silhouette column below is worth having.")
print()

print("one tree, every k, no refitting:")
print("%6s %14s %14s" % ("k", "agreement", "silhouette"))
for k in (2, 3, 4, 5, 6):
    labels = fcluster(Z, k, criterion="maxclust")
    print("%6d %14.4f %14.4f"
          % (k, adjusted_rand_score(y, labels), silhouette_score(X, labels)))
print("  k-means has to be rerun from scratch for each k. this is one fit.")
```

The next block compares the four linkage methods and shows where single linkage wins.

```python-run
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.datasets import make_blobs, make_moons
from sklearn.metrics import adjusted_rand_score

X, y = make_blobs(n_samples=300, centers=4, cluster_std=1.0, random_state=0)

print("linkage is the whole personality of the algorithm:")
for method in ("ward", "complete", "average", "single"):
    m = AgglomerativeClustering(n_clusters=4, linkage=method).fit(X)
    print("  %-10s agreement %.4f, cluster sizes %s"
          % (method, adjusted_rand_score(y, m.labels_),
             sorted(np.bincount(m.labels_), reverse=True)))
print()
print("  ward     -- minimise total variance. compact, even sizes.")
print("  complete -- furthest members. compact, sensitive to outliers.")
print("  average  -- mean pairwise distance. a middle ground.")
print("  single   -- closest members. chains through thin bridges.")
print()

Xm, ym = make_moons(n_samples=300, noise=0.06, random_state=0)
print("that chaining is a weakness and a feature. on two crescents:")
for method in ("ward", "single"):
    m = AgglomerativeClustering(n_clusters=2, linkage=method).fit(Xm)
    print("  %-10s agreement %.4f" % (method, adjusted_rand_score(ym, m.labels_)))
print("  single linkage follows the shape. ward cuts straight across it.")
print()
print("the cost is O(n^2) in memory -- a full distance matrix. at")
print("100,000 rows that is 40GB, which is why k-means still exists.")
```

""",
    [
        {"q": "What is the advantage of building the whole tree?",
         "options": ["It is faster than k-means",
                     "k is chosen after seeing the merge distances, rather than decided in advance",
                     "It handles more data",
                     "It labels outliers"],
         "answer": 1,
         "why": "One tree, and a horizontal cut at any height gives a clustering. Cutting just below a large jump in merge distance is the dendrogram's version of the elbow."},
        {"q": "What is chaining, and which linkage causes it?",
         "options": ["Complete linkage merging outliers",
                     "Single linkage joining two separate blobs through a thin bridge of points, because any short hop is enough",
                     "Average linkage producing equal-sized clusters",
                     "Ward linkage minimising variance"],
         "answer": 1,
         "why": "Single linkage uses the nearest pair, so a bridge provides a cheap merge at every step. Complete linkage has the opposite failure: it breaks up genuinely elongated clusters."},
        {"q": "Why is hierarchical clustering impractical for large datasets?",
         "options": ["It needs too many iterations",
                     "It requires an n-by-n distance matrix, so memory grows with the square of the point count",
                     "Linkage cannot be computed at scale",
                     "The dendrogram cannot be drawn"],
         "answer": 1,
         "why": "100,000 points is ten billion distances. Time is O(n^2 log n) at best, but memory is usually what stops you first."},
    ],
)


# ---------------------------------------------------------------------------
# 13. Choosing k
# ---------------------------------------------------------------------------
topic(
    "choosing_k",
    "Choosing k: Elbow and Silhouette",
    "Clustering",
    "Inertia always falls as k rises, so it cannot pick one. The silhouette "
    "can, and the two often disagree.",
    _svg(_axes()
         + '<path d="M22 22 C 40 52, 70 62, 140 66" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + _dot(58, 56, M, 3) + _txt(88, 30, "elbow?", M, 8)),
    {
        "sim": "choosek",
        "canvases": 2,
        "captions": ["Inertia (the elbow method)", "Mean silhouette"],
        "controls": [
            {"key": "shape", "label": "Data", "type": "select", "value": "blobs",
             "options": [{"value": "blobs", "label": "Three blobs"},
                         {"value": "moons", "label": "Two crescents"}]},
            {"key": "spread", "label": "Blob spread", "type": "range",
             "min": 0.15, "max": 0.90, "step": 0.05, "value": 0.34},
        ],
    },
    [
        "<strong>Inertia</strong> is the total squared distance from each point "
        "to its centroid. It falls at every k and reaches zero at k = n.",
        "The <strong>elbow</strong> is where the fall stops being steep. It is "
        "judged by eye, and frequently there is no clear bend.",
        "The <strong>silhouette</strong> compares each point's distance to its "
        "own cluster against the nearest other one. It has a genuine maximum.",
        "Neither is a substitute for knowing what the clusters are for. k is "
        "often decided by the application, not the data.",
    ],
    """
title: Choosing k: Elbow and Silhouette
intro: Two ways of picking the number of clusters, what each really measures, and why they disagree.

## Why inertia cannot answer the question

**Inertia** is the sum of squared distances from each point to the centroid of
its cluster. K-means cuts it right. So It's the obvious thing to look at.

It's also useless on its own, and the reason is structural: inertia falls at
each grow in k, always. With k equal to the number of points, each point is
its own centroid and inertia is just zero. Watch the left chart as the spread
control moves &mdash; the curve descends monotonically no matter what the data
looks like.

So "choose the k with the lowest inertia" always answers "as many as possible".
The metric measures how tightly points sit around their centres, not whether the
grouping is any good.

## The elbow

The elbow method looks for the k where the curve stops falling steeply &mdash;
where extra clusters stop buying much. On well-separated blobs there's a genuine
bend at the true number. Up to that point each new cluster splits a real
group, and after it each new cluster splits a group that was already coherent.

The problems are hands-on. The bend is judged by eye and different people pick
different points. Very often, on real data, there simply is no bend &mdash; the
curve is smooth, and reading an elbow into it's wishful. Raise the spread
control until the blobs share and the bend disappears in front of you.

There's a formalisation, the **kneedle** method. This Finds the point of
max curvature. It's better than eyeballing, and it still assumes a knee
exists.

## The silhouette

The silhouette measures a thing different: not tightness, but **gap
scaled to tightness**.

For each point, let *a* be its mean distance to the other members of its own
cluster, and *b* its mean distance to the members of the nearest other cluster.
The silhouette is:

```
s = (b - a) / max(a, b)
```

Near **+1** the point is much closer to its own cluster than to any other. Near
**0** it sits on a boundary. **Minus** means it's closer to a different
cluster than to its own &mdash; it's probably misassigned.

Blending over all points gives one number per k, and unlike inertia it doesn't
improve automatically as k grows. Adding clusters eventually forces points close
to a neighbouring cluster. This Drives *b* down and the score with it. So the
silhouette has a real max, and that max is a defensible choice.

The right-hand chart shows this. The peak is at the true number of blobs, and it
is a peak rather than a slope.

The cost is work: it needs pairwise distances, so O(n&sup2;), against
inertia's O(n).

## When they disagree

They often do, and the disagreement is helpful rather than a problem to
resolve.

Inertia asks *are the clusters tight*. The silhouette asks *are they separated*.
A dataset can have tight clusters that sit right next to each other, and the two
metrics will point in different directions.

Switch the data to **Two crescents** and watch both. The silhouette doesn't
recover the two crescents either. Because it's still built on distances
to cluster members, and k-means hasn't made the crescents in the first
place. That is the honest limit of both metrics: they test the clustering
you gave them, and can't tell you the method was wrong.

## The answer that is usually right

Neither metric knows what the clusters are for.

If you're segmenting customers so a marketing team can write one message per
segment, k is roughly how many messages they can write. If you're compressing
colours, k is the palette size you can afford. If clusters feed a downstream
model, the number that makes that model best is the number.

Both metrics are worth finding, and the use often decides.

## The silhouette of one point

Where inertia only ever falls as k grows. Reaching zero when each point is
its own cluster &mdash; the silhouette has a real max, because it measures
gap against tightness rather than tightness alone. For one point, let a be
its mean distance to its own cluster and b its mean distance to the nearest other
cluster. `s = (b - a) / max(a, b)`:

|a (own)|b (nearest other)|silhouette|reading|
|---|---|---|---|
|1.0|3.0|0.67|comfortably inside its cluster|
|2.5|3.0|0.17|near the boundary|
|3.0|1.0|&minus;0.67|closer to another cluster &mdash; misassigned|

Blending s over all points gives one number per k, and unlike inertia it doesn't
improve automatically: add too many clusters and points are forced close to a
neighbouring cluster, which drives b down and the score with it, so the curve peaks
at a defensible k rather than sliding forever toward "more". The cost is O(n&sup2;)
pairwise distances against inertia's O(n). Both still test only the clustering
they were handed, though &mdash; on two interleaved crescents that k-means never
separated, the silhouette can't recover them either. This Is the honest shared
limit: these scores judge a split, they don't know the method was the
wrong one.

The honest last word is that neither metric knows what the clusters are *for*. If
you're segmenting customers so a team can write one message per segment, k is
roughly how many messages they can write. If you're quantising colours, k is the
palette you can afford. If the clusters feed a downstream model, the k that makes
that model best is the answer. The elbow and the silhouette are both worth
finding &mdash; the elbow reads tightness, the silhouette reads gap, and
their disagreement is helpful rather than a problem to resolve &mdash; but the
use often decides, and a formalisation like the kneedle method only
helps once you've accepted that a knee exists at all.

## Where it goes wrong

**Choosing k by inertia alone.** It will always say "more".

**Seeing an elbow in a smooth curve.** Check whether the bend lives a change
of scale on the axis.

**Trusting a silhouette on non-spherical clusters.** It's distance-based and
inherits the same assumption k-means makes.

**Losing to scale.** Both metrics are distances.

## Questions people ask

<strong>Is the elbow method reliable?</strong> Only when the curve has a clear bend, which real data often lacks. When the inertia curve falls smoothly, treat the elbow as a hint and confirm with silhouette scores.

<strong>Can inertia pick k on its own?</strong> No. Inertia always drops as k grows and reaches zero when every point is its own cluster, so its minimum is a useless answer.

<strong>What is a good silhouette score?</strong> Above about 0.5 suggests clear structure, 0.25 to 0.5 means weak structure, and below that the clusters are barely separated. Compare scores across k on the same data rather than against a fixed bar.

<strong>What if the elbow and the silhouette disagree?</strong> Look at the clusters at both values of k and ask which one is useful for the job. Disagreement usually means the structure is ambiguous, so the downstream purpose should break the tie.

<strong>Should k be the number of classes I already know?</strong> If you know the true classes and want to recover them, start there. If the goal is finding structure, let the metrics and the use case decide, since natural groups often differ from labels.

<strong>Does k-means need k even if I only want a rough grouping?</strong> Yes, k is a required input. If you do not want to choose it, try hierarchical clustering or DBSCAN, which do not fix k up front.

## Four ways to pick k, on data where you know the answer

The same four pick scores run twice: once on clean, well-separated blobs where they all agree. Once on shared ones where they don't. The disagreement is the handy part.

```python-run
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import (silhouette_score, calinski_harabasz_score,
                             davies_bouldin_score)
from sklearn.mixture import GaussianMixture
TRUE_K = 5
KS = range(2, 11)
def survey(X, label):
    rows = []
    for k in KS:
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
        gm = GaussianMixture(n_components=k, random_state=0).fit(X)
        rows.append((k, km.inertia_, silhouette_score(X, km.labels_),
                     calinski_harabasz_score(X, km.labels_),
                     davies_bouldin_score(X, km.labels_), gm.bic(X)))
    print(label)
    print("%4s %12s %11s %12s %11s %12s"
          % ("k", "inertia", "silhouette", "calinski", "davies", "GMM BIC"))
    for r in rows:
        print("%4d %12.1f %11.4f %12.1f %11.4f %12.1f" % r)
    picks = {
        "silhouette": max(rows, key=lambda r: r[2])[0],
        "calinski":   max(rows, key=lambda r: r[3])[0],
        "davies":     min(rows, key=lambda r: r[4])[0],
        "GMM BIC":    min(rows, key=lambda r: r[5])[0],
    }
    print("  picks: " + ",  ".join("%s k=%d" % (n, v) for n, v in picks.items()))
    print("  the truth is k=%d. agreed: %d of 4."
          % (TRUE_K, sum(v == TRUE_K for v in picks.values())))
    print()
clean, _ = make_blobs(n_samples=900, centers=TRUE_K, cluster_std=0.55,
                      random_state=0)
survey(clean, "WELL SEPARATED blobs (cluster_std 0.55)")
messy, _ = make_blobs(n_samples=900, centers=TRUE_K, cluster_std=1.6,
                      random_state=0)
survey(messy, "OVERLAPPING blobs (cluster_std 1.6), same 5 centres")
print("when the structure is obvious the scores agree and you did not need")
print("them. when it is not, they disagree -- and that disagreement is")
print("information: there is no single k that is clearly right.")
```

The next block shows why inertia alone cannot pick k and what happens on pure noise.

```python-run
import numpy as np
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
TRUE_K = 5
KS = range(2, 11)
clean, _ = make_blobs(n_samples=900, centers=TRUE_K, cluster_std=0.55,
                      random_state=0)
rows = []
for k in KS:
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(clean)
    rows.append((k, km.inertia_, silhouette_score(clean, km.labels_)))
print("why inertia is not on the picks list -- it falls no matter what:")
print("%6s %14s %14s" % ("k", "inertia", "drop"))
for i, r in enumerate(rows):
    d = "%14.1f" % (rows[i - 1][1] - r[1]) if i else "%14s" % "-"
    print("%6d %14.1f %s" % (r[0], r[1], d))
print("  at k = n every point is its own cluster and inertia is exactly 0.")
print("  the elbow method asks where the DROPS stop being dramatic, by eye.")
print()
print("the check nobody runs -- on data with no clusters at all:")
Xr = np.random.default_rng(0).uniform(size=(900, 2))
scores = {k: silhouette_score(Xr, KMeans(n_clusters=k, n_init=10,
                                         random_state=0).fit(Xr).labels_)
          for k in KS}
bk = max(scores, key=scores.get)
best_clean = max(r[2] for r in rows)
print("  900 uniform random points: best silhouette is k=%d at %.4f"
      % (bk, scores[bk]))
print("  the clean blobs scored %.4f. every method returns an answer" % best_clean)
print("  whether or not there is anything there. the SIZE of the score")
print("  is what tells you it was worth asking.")
print()
print("so: run several, check they agree, check the winner is meaningfully")
print("better than what noise scores -- and if you have a downstream task,")
print("score k on that instead. it is the only measure that certainly matters.")
```

""",
    [
        {"q": "Why can inertia alone never choose k?",
         "options": ["It is too slow to compute",
                     "It falls at every increase in k and reaches zero when every point is its own cluster",
                     "It requires spherical clusters",
                     "It ignores cluster separation"],
         "answer": 1,
         "why": "Minimising it always answers 'as many clusters as possible'. It measures tightness around centres, not whether the grouping is good."},
        {"q": "What does a negative silhouette score for a point mean?",
         "options": ["The point is an outlier",
                     "It is closer on average to a different cluster than to its own, so it is probably misassigned",
                     "The clusters overlap",
                     "k is too small"],
         "answer": 1,
         "why": "s = (b - a) / max(a, b), so s goes negative when the mean distance to the nearest other cluster is smaller than the mean distance within its own."},
        {"q": "Why does the silhouette have a genuine maximum while inertia does not?",
         "options": ["It is normalised between -1 and 1",
                     "Adding clusters eventually pushes points close to a neighbouring cluster, which lowers the score",
                     "It uses squared distances",
                     "It is computed per cluster"],
         "answer": 1,
         "why": "It measures separation relative to tightness. Splitting a coherent group hurts the separation term, so the score falls rather than improving automatically."},
    ],
)


# ---------------------------------------------------------------------------
# 14. Gaussian mixture models
# ---------------------------------------------------------------------------
topic(
    "gaussian_mixture_models",
    "Gaussian Mixture Models",
    "Clustering",
    "Clusters as overlapping distributions rather than hard groups, fitted by "
    "alternating between guessing and re-estimating.",
    _svg(_axes()
         + '<path d="M20 66 C 40 66, 44 26, 62 26 C 80 26, 82 66, 96 66" fill="none" stroke="%s" stroke-width="1.6"/>' % A
         + '<path d="M70 66 C 88 66, 94 34, 112 34 C 128 34, 132 66, 146 66" fill="none" stroke="%s" stroke-width="1.6"/>' % M
         + _txt(80, 82, "soft membership, not hard", M, 7)),
    {
        "sim": "gmm",
        "controls": [
            {"key": "iters", "label": "EM iterations", "type": "range",
             "min": 1, "max": 60, "step": 1, "value": 30},
            {"key": "spread", "label": "Overlap of the two groups", "type": "range",
             "min": 0.35, "max": 1.60, "step": 0.05, "value": 0.55},
        ],
    },
    [
        "A GMM assumes the data came from several Gaussians mixed together, and "
        "fits their means, widths and weights.",
        "Each point gets a <strong>probability</strong> of belonging to each "
        "component, not a single label.",
        "<strong>EM</strong> alternates: given the current parameters, compute "
        "responsibilities; given responsibilities, re-estimate the parameters.",
        "K-means is the special case where every component is spherical, equally "
        "sized, and every responsibility is 0 or 1.",
    ],
    """
title: Gaussian Mixture Models
intro: What clustering looks like when a point is allowed to belong partly to two groups.

## Hard labels throw information away

K-means gives each point just one cluster. For a point sitting squarely
inside a group that is fine. For a point in the share between two groups it's
a fabrication: the method had almost no reason to prefer one over the other,
and the output records none of that doubt.

A Gaussian mixture keeps the doubt. It models the data as having come from
a few Gaussian spreads mixed together, and reports, for each point, the
chance that it came from each one.

Raise the share control above and watch the readout. As the two groups merge,
the number of points assigned with less than 90% trust climbs &mdash; and
each one of those is a point k-means would have labelled without hesitation.

## The model

Three params per component: a mean, a width, and a **mixing weight** saying
what fraction of the data that component accounts for. The density is their
weighted sum, and the two curves in the chart are the fitted components.

Fitting is a chicken-and-egg problem. Knowing which points belong to which
component would make guessing the params easy, and knowing the params
would make assigning points easy. Neither is known.

## Expectation-Maximisation

EM resolves it by alternating, starting from a guess:

**E step.** With the current params, find each point's
**job** &mdash; the chance that each component made it.

**M step.** With those jobs, re-guess each component's mean, width
and weight, weighting each point by how much it belongs.

Repeat. Each iteration provably doesn't fall the likelihood, so the process
settles.

Drag the iterations control from 1 upward and watch the curves settle. The early
steps move a great deal. The last twenty barely move at all, which is what
settling looks like.

The ensure is only about *local* optima. EM settles to a local max that
depends on the starting point. This Is why setups run it a few times
from different initialisations and keep the best. Scikit-learn's `n_init` exists
for this.

## Why it beats k-means, when it does

**Elliptical clusters.** With a full covariance mat per component, a GMM fits
stretched and tilted clusters. K-means silently assumes spheres, so an
elongated cluster gets cut in half.

**Different sizes.** Mixing weights let one component account for 80% of the data
and another for 20%. K-means has no such notion and tends toward equal-sized
clusters.

**Soft set.** handy in itself when the output feeds a thing downstream
that can use a chance.

**A likelihood.** Being a proper probabilistic model, a GMM can score how well it
shows the data, which makes **BIC** and **AIC** available for choosing the
number of components &mdash; a principled option to
[the elbow](choosing_k.html).

K-means is just the limiting case: spherical components of equal weight, with
jobs forced to 0 or 1.

## The E-step, worked

The soft set the whole method turns on is one math. Two components,
N(0,1) with weight 0.6 and N(3,1) with weight 0.4, and a point to assign: its
job to each is the weighted density there, normed so the two sum
to 1.

|point|r(component 1)|r(component 2)|
|---|---|---|
|x = 0.5|0.968|0.032|
|x = 1.5|0.600|0.400|

At x = 0.5 the point sits deep in the first component and is assigned to it with
97% trust &mdash; but k-means would have recorded the same hard label with no
hint of the 3% doubt. At x = 1.5, halfway between the means, the jobs
fall back to the mixing weights themselves: the data gives almost no reason to
prefer either component, and the GMM says so where k-means would still pick one.
That preserved doubt is the whole point, and it's why the number of low-trust
sets climbs as the components share. The M-step then re-guesses each
mean, width and weight using each point weighted by its job, and
alternating the two provably never falls the likelihood &mdash; which is also
why a GMM can report one, through BIC, and choose its own number of components
where k-means can't.

What a GMM buys over k-means, when the data suits it, is three things at once:
elliptical clusters, because a full covariance per component fits stretched and
tilted shapes k-means cuts in half. Unequal sizes, because the mixing weights let
one component own 80% of the data. And the soft set itself, handy when
a thing downstream can act on a chance. K-means is just the limiting
case &mdash; spherical components of equal weight with jobs forced to
0 or 1 &mdash; which is why it fabricates the trust a GMM keeps. The costs are
the assumption of Gaussian components (crescents defeat it) and settling only to
a local optimum, which is why libraries run a few initialisations and keep the
best.

The other failure to watch is a singularity: a component can collapse onto a
single point, driving its width toward zero and the likelihood toward infinity.
A small constant added to each covariance. On by default in most libraries
&mdash; blocks it, and it's the same smoothing instinct that stops too many
components fitting the noise. This Is what BIC's fine on param count guards
against when choosing how many components to keep.

## Where it goes wrong

**given Gaussian.** If the clusters are crescents, a mixture of Gaussians is
the wrong model, and it will fit two Gaussians to them anyway.

**Singularities.** A component can collapse onto a single point, driving its
width to zero and the likelihood to infinity. Smoothing &mdash; a small
constant added to the covariance. Blocks it, and is on by default in
most libraries.

**One run from one start.** Local optima are real. Use a few initialisations.

**Too many components.** With enough Gaussians you can fit any of it, including
the noise. BIC punishes param count for this reason.

## Questions people ask

<strong>How is a GMM different from k-means?</strong> A GMM gives each point a probability of belonging to every cluster, and each cluster has its own shape through a covariance matrix. K-means gives hard labels and assumes round clusters.

<strong>How do I choose the number of components?</strong> Fit models for a range of component counts and pick the lowest BIC or AIC. BIC penalises complexity more heavily, so it tends to give simpler models.

<strong>Which covariance type should I use?</strong> Full covariance fits any ellipse but needs more data. Diagonal, spherical or tied reduce parameters, which helps when you have few points or many features.

<strong>Why does my GMM give different results each run?</strong> EM starts from random initial values and only finds a local optimum. Set n_init higher and fix random_state.

<strong>Can a GMM be used for anomaly detection?</strong> Yes. Points with a very low density under the fitted mixture are unusual, so you can threshold score_samples.

<strong>What is the E-step and M-step?</strong> The E-step computes how responsible each component is for each point. The M-step updates means, covariances and weights using those responsibilities, and the two repeat until the likelihood stops improving.

## Soft clusters, and shapes k-means cannot fit

A GMM gives each point a chance of belonging to each cluster. Fits ellipses rather than spheres. Both differences show up on the same data.

```python-run
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score

X, y = make_blobs(n_samples=600, centers=3, cluster_std=0.8,
                  center_box=(-14.0, 14.0), random_state=0)
X = X @ np.array([[1.0, 0.0], [1.2, 0.35]])

gm = GaussianMixture(n_components=3, random_state=0).fit(X)
km = KMeans(n_clusters=3, n_init=10, random_state=0).fit(X)
print("three well-separated blobs, sheared into long tilted ellipses:")
print("  k-means agreement %.4f" % adjusted_rand_score(y, km.labels_))
print("  GMM     agreement %.4f" % adjusted_rand_score(y, gm.predict(X)))
print("  k-means can only draw spheres, so it cuts across the grain")
print("  of the ellipses and splits them in the wrong places.")
print()

print("what a GMM stores per cluster -- weight, centre, covariance:")
for c in range(3):
    print("  cluster %d  weight %.4f  centre %s" % (c, gm.weights_[c],
                                                    np.round(gm.means_[c], 3)))
    print("             covariance %s" % np.round(gm.covariances_[c], 3).tolist())
print()

p = gm.predict_proba(X)
conf = p.max(axis=1)
print("every point gets a probability per cluster, not just a label:")
order = np.argsort(conf)
print("  least certain (border points):")
for i in order[:4]:
    print("    %s  ->  %s" % (np.round(X[i], 2), np.round(p[i], 4)))
print("  most certain (deep inside a component):")
for i in order[-3:]:
    print("    %s  ->  %s" % (np.round(X[i], 2), np.round(p[i], 4)))
print("  %d of %d points are less than 90%% sure." % ((conf < 0.9).sum(), len(X)))
```

The next block compares covariance types and uses BIC to pick the number of components.

```python-run
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.datasets import make_blobs
from sklearn.metrics import adjusted_rand_score

X, y = make_blobs(n_samples=600, centers=3, cluster_std=0.8,
                  center_box=(-14.0, 14.0), random_state=0)
X = X @ np.array([[1.0, 0.0], [1.2, 0.35]])

print("covariance_type trades flexibility for parameters:")
for ct in ("spherical", "diag", "tied", "full"):
    m = GaussianMixture(n_components=3, covariance_type=ct, random_state=0).fit(X)
    print("  %-10s agreement %.4f   BIC %9.1f   parameters %d"
          % (ct, adjusted_rand_score(y, m.predict(X)), m.bic(X),
             m._n_parameters()))
print("  'spherical' is soft k-means. 'full' fits any ellipse.")
print("  'tied' wins on BIC here because all three ellipses share one")
print("  shape, so it gets full's accuracy for spherical's parameter count.")
print()

print("BIC picks the number of components, which k-means cannot do:")
print("%6s %12s %12s" % ("k", "BIC", "AIC"))
for k in range(1, 7):
    m = GaussianMixture(n_components=k, random_state=0).fit(X)
    print("%6d %12.1f %12.1f" % (k, m.bic(X), m.aic(X)))
best = min(range(1, 7), key=lambda k: GaussianMixture(n_components=k,
                                                      random_state=0).fit(X).bic(X))
print("  lowest BIC at k=%d, and the data really has 3 components." % best)
print("  BIC is not infallible -- on overlapping components it under-counts.")
print("  it works because a GMM is a probability model: BIC compares how")
print("  well each k explains the data against how many parameters it spent.")
print()
print("the catch: with enough components a GMM puts one tiny component")
print("on a handful of points and drives variance toward zero, sending")
print("the likelihood to infinity. reg_covar exists to stop that.")
```

""",
    [
        {"q": "What does a GMM report for each point?",
         "options": ["A single cluster label",
                     "A probability of belonging to each component",
                     "A distance to the nearest centroid",
                     "An outlier score"],
         "answer": 1,
         "why": "That is the point: a point in the overlap between two groups records its doubt, where k-means would label it without hesitation."},
        {"q": "What do the two steps of EM do?",
         "options": ["Split and merge clusters",
                     "E computes responsibilities from the current parameters; M re-estimates parameters from those responsibilities",
                     "Estimate then maximise the number of components",
                     "Initialise then converge"],
         "answer": 1,
         "why": "It resolves a chicken-and-egg problem by alternating, and each iteration provably does not decrease the likelihood - though only to a local maximum."},
        {"q": "K-means is the special case of a GMM where:",
         "options": ["There is only one component",
                     "Components are spherical and equally weighted, and responsibilities are forced to 0 or 1",
                     "The covariance is full",
                     "EM is run once"],
         "answer": 1,
         "why": "Which is why a GMM handles elliptical and unequally sized clusters that k-means cuts in half or splits evenly."},
    ],
)


# ---------------------------------------------------------------------------
# 15. t-SNE and UMAP beside PCA
# ---------------------------------------------------------------------------
topic(
    "tsne_and_umap",
    "t-SNE and UMAP beside PCA",
    "Dimensionality",
    "Layouts that preserve who is near whom, at the cost of making the distance "
    "between clusters meaningless.",
    _svg(_axes()
         + "".join(_dot(28 + (i % 4) * 5, 30 + (i // 4) * 5, A) for i in range(12))
         + "".join(_dot(74 + (i % 4) * 5, 52 + (i // 4) * 5, M) for i in range(12))
         + "".join(_dot(116 + (i % 4) * 5, 26 + (i // 4) * 5, A) for i in range(12))
         + _txt(80, 82, "tight groups, arbitrary gaps", M, 7)),
    {
        "sim": "embedding",
        "controls": [
            {"key": "method", "label": "Method", "type": "select", "value": "pca",
             "options": [{"value": "pca", "label": "PCA (linear projection)"},
                         {"value": "neighbour", "label": "Neighbour-preserving layout"}]},
            {"key": "attract", "label": "Attraction strength", "type": "range",
             "min": 0.4, "max": 2.4, "step": 0.1, "value": 1.0},
        ],
    },
    [
        "PCA is a linear projection: it keeps the directions of greatest "
        "variance, so global distances survive.",
        "t-SNE and UMAP optimise a layout so that near neighbours stay near. "
        "Nothing constrains anything else.",
        "The distance <em>between</em> clusters in a t-SNE plot carries no "
        "information. Neither does cluster size.",
        "The layout on this page is a simplified neighbour-preserving "
        "optimisation, not t-SNE itself &mdash; it shows the behaviour, not the algorithm.",
    ],
    """
title: t-SNE and UMAP beside PCA
intro: Why neighbour-preserving plots look so much better than PCA. Which parts of them you aren't allowed to read.

## A note on what this page runs

High-dimensional data is hard to think about. You cannot plot 50
columns on a flat screen. PCA does it by choosing the two directions
with the most spread, but that projection can hide clusters that sit
in the other 48 dimensions. t-SNE and UMAP take a different approach:
they try to keep nearby points nearby, and let everything else land
wherever it lands. The result often shows clusters that PCA misses.

The layout on this page is a **simplified neighbour-preserving
optimisation** &mdash; attract each point toward its nearest neighbours in
the original space, repel all else. It is not t-SNE: there is no
perplexity, no Student-t kernel, no KL divergence being minimised.
What it copies faithfully is the action that matters: local structure
is preserved, and the distances between groups stop meaning anything.
The [PCA module](pca.html) covers the linear method properly. The controls on this page let you watch both approaches side by side.

## Two different jobs

**PCA** finds the directions along which the data varies most and projects onto
them. It's linear, deterministic, invertible, and fast &mdash; and because it's
a map, distances live it in a predictable way. Points far apart in the
first space are far apart in the plot, up to the variance the discarded
dims held.

**t-SNE and UMAP** do a thing else fully. They ask which points are near
each other in the first space, and then *make* a two-dimensional
setup in which those same points are near each other. There's no
map and no formula mapping one space to the other &mdash; the coords
are the output of an optimisation.

## What the readout is checking

The data behind this page has three clusters arranged on a line, with the third
just twice as far from the first as the second is. A ratio of 2.00, by
build.

Switch between the methods and watch the measured ratio.

**PCA** copies it closely. It's a linear map, so the global
setup is preserved.

**The neighbour-preserving layout** doesn't, and the number wanders as you
change the attraction strength. The three groups are cleanly separated &mdash;
visibly better than PCA &mdash; and the distances between them are an artefact of
the optimisation.

That is the whole lesson, and it's the thing most often got wrong when reading
these plots.

## What you may not read from a t-SNE plot

**Distance between clusters.** Two clusters at opposite ends may be more similar
than two that are adjacent. The layout only tried to keep neighbours together.

**Cluster size.** t-SNE expands dense regions and contracts sparse ones, so the
area a cluster occupies says nothing about how many points it has or how spread
out they were.

**Density within a cluster.** Same reason.

**any of it from one run.** t-SNE is stochastic and its result depends on the
random seed and on perplexity. Run it three times and you get three pictures.
Structure that lives all three is real. Structure that doesn't, isn't.

## Perplexity and n_neighbors

Both methods have a param controlling how much zone to consider
&mdash; **perplexity** in t-SNE, **n_neighbors** in UMAP. Low values emphasise
very local structure and can shatter a genuine cluster into fragments. High
values emphasise broader structure and can merge distinct clusters.

There's no correct value, and the standard advice is to look at a few. A
finding that only appears at one setting is a finding about the param.

## t-SNE against UMAP

**Speed.** UMAP is a lot faster and scales to larger datasets.

**Global structure.** UMAP claims to preserve more of it, and often does,
though the caution above still applies &mdash; less meaningless isn't
real.

**New points.** UMAP can transform data it didn't see during fitting. t-SNE
can't: adding a point means re-running all. This matters if the embedding
is part of a pipeline rather than a picture.

**Reproducibility.** Both are stochastic. Both take a seed.

## What they are for

Looking. These are visualisation tools, and they're very good at answering "does
my data separate at all", "are my labels steady", "is there a group I didn't
expect".

They're a poor choice as a prep step for a model. The output
coords have no meaning outside the plot, the mapping isn't stable, and for
t-SNE it can't be applied to new data at all. If you want dimensionality
reduction inside a pipeline, PCA is the safe default.

## The distance you are not allowed to read

The one number that makes the caution concrete: place three clusters on a line so
the third is just twice as far from the first as the second is &mdash; a true
ratio of 2.00 &mdash; and measure it back off each layout:

|method|recovered distance ratio|
|---|---|
|PCA|~2.00|
|neighbour-preserving (t-SNE-like)|arbitrary, and it wanders with the settings|

PCA is a linear map. So Global setup lives it and the 2.00 comes
back. t-SNE and UMAP never project. They *make* a layout that keeps
each point near its first neighbours and nothing else &mdash; so between-cluster
distance is an output of the optimisation, not a property of the data, and it
changes with the seed and the perplexity. That is why three things on such a plot
are unreadable: the distance between clusters, the size of a cluster (dense regions
are expanded and sparse ones contracted), and within-cluster density. What the plot
*is* good for is the local question. Does the data separate at all, are the
labels steady, is there an unexpected group. And the discipline that
keeps it honest is to run it two or three times: structure that lives each seed
is real, structure that moves is an artefact.

On choosing between the two neighbour-preserving methods: UMAP is a lot
faster, scales to larger data, and can transform points it didn't see during
fitting, which t-SNE can't &mdash; adding a point to a t-SNE means re-running
all, so it can never sit inside a pipeline that scores new data. UMAP also
claims to preserve more global structure and often does, though the caution
stands: less meaningless isn't real. Both are stochastic and both take a
seed. And both are the wrong choice as a prep step for a model, because
the coords mean nothing outside the plot and the mapping isn't stable. When
you want dimensionality reduction inside a pipeline, PCA is the safe default.

## Where it goes wrong

**Measuring distance between clusters.** The single most common error.

**Reading cluster sizes.** Artefacts of the optimisation.

**Running once and believing it.** Vary the seed and the perplexity.

**Feeding t-SNE coords into a classifier.** No stable mapping. No way to
transform new data.

## Questions people ask

<strong>Can I trust the distances between clusters in t-SNE?</strong> No. t-SNE preserves local neighbourhoods, not global distances, so the gaps and sizes between clusters can be arbitrary.

<strong>What is perplexity?</strong> Roughly the number of neighbours each point considers. Values from 5 to 50 are typical, and you should try several because the picture changes.

<strong>t-SNE or UMAP?</strong> UMAP is faster and tends to keep more of the global structure. Both are for visualisation, and both are sensitive to their settings.

<strong>Can I use t-SNE output as features for a model?</strong> It is not recommended. The embedding cannot transform new points consistently and depends on the run. UMAP can transform new data and is better suited.

<strong>Why does my plot change every run?</strong> Both start from random initialisation. Set a random seed, and check that the structure you care about appears across seeds.

<strong>Should I reduce dimensions with PCA first?</strong> Often yes, down to about 30 to 50 components. It cuts noise and speeds up the embedding.

## A map you can look at, and must not measure

t-SNE turns high-dimensional data into a picture. The picture is handy and a few things about it aren't true. This This makes concrete.

```python-run
import numpy as np
from sklearn.manifold import TSNE
from sklearn.datasets import make_blobs
from sklearn.metrics import pairwise_distances
rng = np.random.default_rng(0)
X, y = make_blobs(n_samples=600, n_features=30, centers=4, cluster_std=2.0,
                  random_state=0)
X[y == 3] += 40.0
print("600 points in 30 dimensions, 4 groups, one pushed far away.")
cent = np.array([X[y == c].mean(axis=0) for c in range(4)])
D = pairwise_distances(cent)
print("true distances between group centres:")
for i in range(4):
    print("   group %d: %s" % (i, np.round(D[i], 1)))

emb = TSNE(n_components=2, perplexity=30, random_state=0, init="pca").fit_transform(X)
cent2 = np.array([emb[y == c].mean(axis=0) for c in range(4)])
D2 = pairwise_distances(cent2)
print("the same distances in the t-SNE picture:")
for i in range(4):
    print("   group %d: %s" % (i, np.round(D2[i], 1)))

off = ~np.eye(4, dtype=bool)
print("ratio of largest to smallest between-group distance:")
print("   in 30-D  : %.2f" % (D[off].max() / D[off].min()))
print("   in t-SNE : %.2f" % (D2[off].max() / D2[off].min()))
near = D[:3, :3][~np.eye(3, dtype=bool)].mean()
far = D[3, :3].mean()
near2 = D2[:3, :3][~np.eye(3, dtype=bool)].mean()
far2 = D2[3, :3].mean()
print("  in 30-D, group 3 sits %.1fx further. in the picture, %.1fx."
      % (far / near, far2 / near2))
print()
print("cluster SIZES are not preserved either:")
for c in range(4):
    print("   group %d: spread %6.2f in 30-D, %6.2f in the picture"
          % (c, X[y == c].std(), emb[y == c].std()))
print("  t-SNE inflates sparse clusters and compresses dense ones.")
```

The next block measures what t-SNE does preserve and how perplexity changes the result.

```python-run
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.datasets import make_blobs
from sklearn.metrics import pairwise_distances
rng = np.random.default_rng(0)
X, y = make_blobs(n_samples=600, n_features=30, centers=4, cluster_std=2.0,
                  random_state=0)
X[y == 3] += 40.0

def knn_overlap(A, B, k=15):
    da = pairwise_distances(A); db = pairwise_distances(B)
    np.fill_diagonal(da, np.inf); np.fill_diagonal(db, np.inf)
    na = np.argsort(da, axis=1)[:, :k]
    nb = np.argsort(db, axis=1)[:, :k]
    return np.mean([len(set(a) & set(b)) / k for a, b in zip(na, nb)])

emb = TSNE(n_components=2, perplexity=30, random_state=0, init="pca").fit_transform(X)
pca2 = PCA(n_components=2).fit_transform(X)
print("what IS preserved -- who your neighbours are:")
print("   fraction of each point's 15 nearest neighbours that survive:")
print("     t-SNE %.4f" % knn_overlap(X, emb))
print("     PCA   %.4f" % knn_overlap(X, pca2))
print("  t-SNE keeps local neighbourhoods far better, throws away global.")
print()

print("perplexity changes the picture, not just its appearance:")
for perp in (5, 30, 100):
    e = TSNE(n_components=2, perplexity=perp, random_state=0,
             init="pca").fit_transform(X)
    print("   perplexity %3d: neighbour overlap %.4f" % (perp, knn_overlap(X, e)))
print("  roughly 'how many neighbours count'. run two or three values")
print("  before believing any structure you see.")
```

The next block runs t-SNE on pure noise to show it always produces apparent structure.

```python-run
import numpy as np
from sklearn.manifold import TSNE
from sklearn.metrics import pairwise_distances
rng = np.random.default_rng(0)

def knn_overlap(A, B, k=15):
    da = pairwise_distances(A); db = pairwise_distances(B)
    np.fill_diagonal(da, np.inf); np.fill_diagonal(db, np.inf)
    na = np.argsort(da, axis=1)[:, :k]
    nb = np.argsort(db, axis=1)[:, :k]
    return np.mean([len(set(a) & set(b)) / k for a, b in zip(na, nb)])

print("t-SNE on pure noise:")
Xn = rng.normal(size=(600, 30))
en = TSNE(n_components=2, perplexity=30, random_state=0, init="pca").fit_transform(Xn)
print("   neighbour overlap with the real 30-D noise: %.4f" % knn_overlap(Xn, en))
print("   it still produces a picture with apparent blobs in it.")
print("   a shape in a t-SNE plot is a hypothesis, not a finding.")
print()
print("use it to look, never to measure. do not read distances between")
print("clusters or their sizes. cluster in the original space and")
print("colour the picture by it.")
print()
print("UMAP is the usual alternative: much faster, preserves more global")
print("layout, same caveats. it ships as the separate umap-learn package.")
```

""",
    [
        {"q": "Why can you not read the distance between two clusters in a t-SNE plot?",
         "options": ["The axes are unlabelled",
                     "The layout only optimises for keeping near neighbours near; nothing constrains the gaps between groups",
                     "The plot is rotated arbitrarily",
                     "Distances are logarithmic"],
         "answer": 1,
         "why": "Two clusters at opposite ends of the plot may be more similar than two adjacent ones. PCA, being a linear projection, does preserve global distances."},
        {"q": "What can UMAP do that t-SNE cannot?",
         "options": ["Preserve local structure",
                     "Transform data it did not see during fitting",
                     "Run deterministically",
                     "Handle more than three dimensions"],
         "answer": 1,
         "why": "t-SNE has no mapping from the original space to the layout, so adding a point means re-running everything. This matters when the embedding is part of a pipeline."},
        {"q": "Why is PCA the safer choice for dimensionality reduction inside a pipeline?",
         "options": ["It separates clusters better",
                     "It is a stable, invertible linear mapping that applies to new data, whereas t-SNE coordinates have no meaning outside the plot",
                     "It is stochastic",
                     "It preserves cluster density"],
         "answer": 1,
         "why": "t-SNE and UMAP are visualisation tools. They answer 'does my data separate at all' well, and make poor preprocessing steps."},
    ],
)


# ---------------------------------------------------------------------------
# 16. Feature and permutation importance
# ---------------------------------------------------------------------------
topic(
    "permutation_importance",
    "Feature and Permutation Importance",
    "Interpretation",
    "Shuffle one column, re-score the model, and see how much it mattered. "
    "Simple, model-agnostic, and easy to misread.",
    _svg(_axes()
         + _box(26, 30, 14, 36, fill=S, stroke=A, sw=1.4)
         + _box(50, 42, 14, 24, fill=S, stroke=A, sw=1.4)
         + _box(74, 58, 14, 8, fill=S, stroke=B, sw=1.4)
         + _box(98, 56, 14, 10, fill=S, stroke=B, sw=1.4)
         + _txt(80, 82, "how much each column is worth", M, 7)),
    {
        "sim": "importance",
        "controls": [
            {"key": "repeats", "label": "Shuffles per feature", "type": "range",
             "min": 1, "max": 12, "step": 1, "value": 5},
            {"key": "seed", "label": "Shuffle seed", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 12},
        ],
    },
    [
        "Permutation importance breaks the link between one column and the "
        "target by shuffling it, then measures the damage.",
        "It works on any fitted model, because it only needs predictions.",
        "Measure it on <strong>held-out</strong> data. On training data it "
        "reports what the model memorised.",
        "Correlated features hide each other: shuffle one and the model leans on "
        "its twin, so the measured drop is far below what that column is worth.",
    ],
    """
title: Feature and Permutation Importance
intro: The most handy model-agnostic importance measure, and the exact way it lies to you.

## The idea

If a feature matters, destroying the info in it should hurt the model. So:

1. Score the model on a dataset.
2. Shuffle one column, breaking its tie with the target while leaving
   its spread untouched.
3. Score again.
4. The drop is that feature's importance.
5. Repeat for each column.

Shuffling rather than deleting is the key detail. Deleting a column means
retraining, which gives a different model and answers a different question.
Shuffling keeps the same fitted model and the same input shape, so the only thing
that changed is whether that column carries signal.

Because it needs nothing but guesses, it works on any model at all &mdash;
linear, forest, grad-boosted, neural network.

## Reading the chart

Four features are fed to a logistic model: a strong signal, a weak one, pure
noise, and a **near-duplicate copy of the strong signal**.

`noise` scores about zero, which is correct and reassuring.

Now compare `signal` with `copy of signal`. They carry the same info
&mdash; either would serve the model about equally well on its own &mdash; and
`copy of signal` scores roughly half what `signal` does, landing at about the
level of `weak`, a feature that is truly much less helpful.

## Why: correlated features hide each other

The reason is just the method. The model here is a small random forest,
and each split considers a random subset of the features. So Some trees split on
`signal` and others on its copy. Shuffling the copy leaves all the trees that
used `signal` working just right. So The measured drop is much smaller than the
column's actual worth.

The metric is measured **one column at a time**, and with linked features
that is the wrong unit of analysis. The honest reading isn't "the copy doesn't
matter" but "either one largely substitutes for the other, and this method can't
say that".

The size of the effect depends on the model. A linear model given two duplicate
columns splits its weight between them. So Shuffling one still destroys half the
part and both score moderately high. A forest can substitute one for the
other outright, which is why the discount is so visible here &mdash; and why the
trap is worst on just the tree models where importance charts are most often
drawn.

This is the single most key thing to know about permutation importance,
because the failure is silent and the chart looks just right reasonable.

What to do about it:

**Cluster linked features first** and permute whole groups together. The
group's importance is then real though its members' aren't.

**Check the link mat** before reading any importance chart.

**Use if-based permutation**, which shuffles within strata of the linked
features rather than globally.

## Held-out data, not training data

Permutation importance found on the training set measures what the model
*used to fit*, including what it stored. A feature the model overfitted to
will look highly key because shuffling it destroys stored training
speed.

On held-out data the same method measures what the feature adds to
speed that generalises. That is almost always the question, and it's why
scikit-learn's docs is emphatic about it.

Checking the two is diagnostic in itself: a feature that is very key on
training data and unimportant on validation data is one the model overfitted.

## Against a tree's built-in importance

Random forests and grad-boosted trees expose `feature_importances_`, often
mean fall in impurity. It's free, since it's built up during training,
and it has a known bias: it **favours high-cardinality features**. A column with
many distinct values offers more possible split points, so it's chosen more
often and builds up more credit. Even a random ID column will score
above a handy binary flag.

Permutation importance doesn't have that bias, costs a re-scoring pass per
feature, and applies to models that have no built-in measure at all.

## Repeats

Shuffling is random, so a single shuffle is a noisy guess. The repeats control
above means a few, and the wobble as you change the seed at one repeat
shrinks visibly as you raise it. Five to ten is common.

## Two copies of one signal, and the discount

The central trap is measurable. Feed a model four features &mdash; a strong signal,
a weak one, pure noise, and a near-duplicate copy of the strong signal &mdash; and
read the permutation importances:

|feature|importance|
|---|---|
|signal|high|
|copy of signal|~half of signal, level with `weak`|
|weak|low|
|noise|~0|

`noise` scoring zero is correct and reassuring. But `copy of signal` carries the
same info as `signal` &mdash; either alone would serve the model &mdash; and
it scores about half, down at the level of a truly weak feature. The cause is
the method: importance is measured one column at a time. So When the copy is
shuffled each tree that split on the first still works, and the measured drop is
small. The honest reading isn't "the copy doesn't matter" but "either substitutes
for the other, and this method can't say so". And the effect is worst on the
tree models where these charts are drawn most. A forest can swap one
linked column for the other outright. The fixes are to cluster linked
features and permute the group, or to check the link mat before trusting
any importance bar. Find it on held-out data, too: on training data it rewards
what the model stored.

## Where it goes wrong

**Reading it on linked features.** The central trap.

**finding it on training data.** Measures memorisation.

**Treating it as causal.** It says the model used a feature, not that the feature
causes the outcome.

**Checking across models.** Importance is scaled to one fitted model. A
different model can rank the same features differently and both be right about
themselves.

## Questions people ask

<strong>How does permutation importance work?</strong> Shuffle one column in held-out data and measure how much the score drops. A large drop means the model relied on that feature.

<strong>Why use held-out data?</strong> On training data, an overfit model can rely on features that carry only noise. Held-out data shows which features help predictions that generalise.

<strong>Why do correlated features get low scores?</strong> When two columns carry the same signal, shuffling one leaves the other to cover for it. Both look unimportant, so group correlated features or drop one.

<strong>How is it different from tree feature importance?</strong> Tree importance counts how much splits reduce impurity and favours high-cardinality features. Permutation importance measures the effect on actual predictions and works with any model.

<strong>How many repeats should I use?</strong> Ten or more shuffles per feature, so you can see the spread. A feature whose drop is within the noise is not clearly useful.

<strong>Can importance be negative?</strong> Yes, slightly. It means shuffling the feature happened to improve the score, which suggests the feature is not helping.

## Break one column and see what it costs

Permutation importance shuffles a column and measures the damage. It works on any fitted model. It disagrees with a tree's built-in importances in ways worth understanding.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0)
X, y = make_classification(n_samples=3000, n_features=6, n_informative=3,
                           n_redundant=0, flip_y=0.08, shuffle=False,
                           random_state=0)
X = np.column_stack([X, rng.normal(size=len(X)), X[:, 0]])
names = ["real_0", "real_1", "real_2", "filler_3", "filler_4", "filler_5",
         "pure_noise", "copy_of_real_0"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
rf = RandomForestClassifier(n_estimators=250, random_state=0).fit(Xtr, ytr)
print("baseline test accuracy %.4f" % rf.score(Xte, yte))
print()
print("do it by hand on one column -- shuffle it and re-score:")
col = 0
scores = []
for rep in range(10):
    Xs = Xte.copy()
    rng.shuffle(Xs[:, col])
    scores.append(rf.score(Xs, yte))
print("  shuffling %s ten times: accuracy %.4f +/- %.4f"
      % (names[col], np.mean(scores), np.std(scores)))
print("  the drop is %.4f. that is its permutation importance."
      % (rf.score(Xte, yte) - np.mean(scores)))
print()
r = permutation_importance(rf, Xte, yte, n_repeats=10, random_state=0)
print("%-16s %12s %10s %14s" % ("feature", "permutation", "sd", "tree built-in"))
order = np.argsort(-r.importances_mean)
for i in order:
    print("%-16s %12.4f %10.4f %14.4f"
          % (names[i], r.importances_mean[i], r.importances_std[i],
             rf.feature_importances_[i]))
print()
print("filler columns and pure_noise carry nothing. the tree's built-in")
print("importance still scores them above zero because a continuous column")
print("offers many split points. permutation importance, on held-out rows,")
print("puts them at zero where they belong.")
```

The next block shows how correlated features split their importance and how to read the result honestly.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
rng = np.random.default_rng(0)
X, y = make_classification(n_samples=3000, n_features=6, n_informative=3,
                           n_redundant=0, flip_y=0.08, shuffle=False,
                           random_state=0)
X = np.column_stack([X, rng.normal(size=len(X)), X[:, 0]])
names = ["real_0", "real_1", "real_2", "filler_3", "filler_4", "filler_5",
         "pure_noise", "copy_of_real_0"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
rf = RandomForestClassifier(n_estimators=250, random_state=0).fit(Xtr, ytr)
r = permutation_importance(rf, Xte, yte, n_repeats=10, random_state=0)
print("the trap. real_0 and copy_of_real_0 are the same column:")
for i in (0, 7):
    print("  %-16s permutation %.4f" % (names[i], r.importances_mean[i]))
print("  each scores about half. shuffling one leaves the other standing.")
print()
print("drop the copy and refit:")
keep = [i for i in range(8) if i != 7]
rf2 = RandomForestClassifier(n_estimators=250, random_state=0).fit(Xtr[:, keep], ytr)
r2 = permutation_importance(rf2, Xte[:, keep], yte, n_repeats=10, random_state=0)
print("  real_0 importance is now %.4f, up from %.4f."
      % (r2.importances_mean[0], r.importances_mean[0]))
print("  the column did not become more useful. it stopped sharing credit.")
print()
print("correlated features SPLIT their importance. a zero means 'the model")
print("can get by without it', not 'this column is useless'.")
print()
print("measure on held-out data and use the metric you care about:")
r3 = permutation_importance(rf, Xte, yte, n_repeats=10, random_state=0,
                            scoring="roc_auc")
order = np.argsort(-r.importances_mean)
print("  scored by ROC AUC instead of accuracy:")
for i in order[:4]:
    print("    %-16s %.4f" % (names[i], r3.importances_mean[i]))
```

""",
    [
        {"q": "Why shuffle a column rather than delete it?",
         "options": ["Deleting is slower",
                     "Deleting requires retraining, which gives a different model and answers a different question",
                     "Shuffling preserves the correlation with other features",
                     "Deleting breaks the input shape"],
         "answer": 1,
         "why": "Shuffling keeps the same fitted model and the same distribution, so the only thing that changed is whether that column still carries signal."},
        {"q": "Two near-identical informative features both show low importance. Why?",
         "options": ["They cancel each other out",
                     "Shuffling one leaves the other intact, so the model uses the twin and loses almost no accuracy",
                     "The model ignored both",
                     "Their importance was divided between them"],
         "answer": 1,
         "why": "The metric is measured one column at a time. The honest reading is 'either one suffices', which this method cannot express - permute correlated groups together instead."},
        {"q": "What bias does a tree's built-in impurity importance have?",
         "options": ["It favours features used early in the tree",
                     "It favours high-cardinality features, because more distinct values mean more split points to be chosen at",
                     "It favours binary features",
                     "It ignores correlated features"],
         "answer": 1,
         "why": "A random ID column can score above a useful binary flag. Permutation importance does not have this bias, at the cost of a re-scoring pass per feature."},
    ],
)


# ---------------------------------------------------------------------------
# 17. Partial dependence and SHAP
# ---------------------------------------------------------------------------
topic(
    "partial_dependence_and_shap",
    "Partial Dependence, ICE and SHAP",
    "Interpretation",
    "What the model does as one feature moves, and why the average of many "
    "individuals can describe none of them.",
    _svg(_axes()
         + _line(24, 62, 140, 30, M, 1) + _line(24, 34, 140, 62, M, 1)
         + _line(24, 48, 140, 46, A, 2.2)
         + _txt(80, 82, "the average of two opposites", M, 7)),
    {
        "sim": "pdp",
        "controls": [
            {"key": "interaction", "label": "Interaction between x and the group",
             "type": "select", "value": "on",
             "options": [{"value": "on", "label": "On - effect reverses by group"},
                         {"value": "", "label": "Off - same effect for everyone"}]},
            {"key": "showIce", "label": "Show individual curves",
             "type": "select", "value": "yes",
             "options": [{"value": "yes", "label": "Show ICE curves"},
                         {"value": "", "label": "Partial dependence only"}]},
        ],
    },
    [
        "A <strong>partial dependence</strong> curve sweeps one feature across "
        "its range, holding the others as they are, and averages the predictions.",
        "An <strong>ICE</strong> curve does the same for a single row, without "
        "averaging. One line per individual.",
        "When the effect of a feature differs by subgroup, the average can be "
        "flat while no individual is.",
        "<strong>SHAP</strong> answers a different question: how much did each "
        "feature contribute to <em>this one</em> prediction.",
    ],
    """
title: Partial Dependence, ICE and SHAP
intro: Three ways to ask what a model is doing. The trap in the most common one.

## Partial dependence

A partial dependence plot answers: as this feature moves across its range, what
happens to the guess on average?

The method is mechanical. Take the dataset. Set the feature to some value for
*each* row, leaving all other columns untouched. Predict, and mean. Repeat
across the feature's range, and plot.

It's model-agnostic and easy to read. This Is why it's all over.

## The trap

Leave the interplay control **on** and look at the thick line. It's nearly
flat, and the readout gives its slope as close to zero. Read on its own, it says
this feature doesn't matter.

Now the ICE curves underneath tell a fully different story. each single
curve has a steep slope. The feature matters enormously to each single
row. It's just that it slopes **up** for one group and **down** for the other,
and blending them cancels.

This isn't a contrived case. Any feature whose effect reverses by subgroup
behaves like this: a treatment that helps one group and harms another, a
price change that attracts some customers and repels others.

**A flat partial dependence curve doesn't mean the feature is unimportant.** It
means the mean effect is zero. This Is a much weaker statement.

Switch the interplay off and the curves stack into a single shape. Now the
mean shows each single well, and the partial dependence line is
trustworthy.

## ICE curves

**Single if-based Expectation** curves are partial dependence without the
blending: one line per row, showing what the model predicts for *that* row as
the feature sweeps.

They cost nothing extra, since partial dependence finds them and then throws
them away. Plotting them is the standard defence against the trap above, and the
diagnostic is simple: if the ICE curves are parallel, the partial dependence line
is a fair summary. If they fan out or cross, it isn't, and there's an
interplay worth finding.

## The other assumption

Partial dependence sets a feature to a value for each row even so of whether
that combination is possible. Sweeping `age` from 18 to 80 across a dataset
creates rows with age 18 and forty years of work run into.

The model is asked to predict for combinations that never occur, and its answer
there's extrapolation with nothing to anchor it. When features are strongly
linked, part of a partial dependence curve is showing regions of input
space the model has never seen.

**Built up Local Effects** plots address this by only varying a feature within
the range of values that really co-occur with the other features' values.

## SHAP

SHAP answers a different question. Partial dependence and ICE show the model
across a range. SHAP shows **one guess**.

For a given row, it assigns each feature a number saying how much that feature
pushed the guess away from the base value &mdash; the mean guess
over the dataset. The numbers sum just to the difference:

```
prediction  =  base value  +  sum of every feature's SHAP value
```

That additivity is what makes it handy for an single explanation: it
accounts for the whole guess, with nothing unattributed.

The values come from Shapley values in cooperative game theory, which distribute
credit for a joint outcome fairly among contributors. finding them just
needs testing each subset of features. This Is exponential, so
setups rough &mdash; `TreeSHAP` just and quickly for trees,
`KernelSHAP` by sampling for any of it else.

| | Answers | Scope |
|---|---|---|
| Partial dependence | how the prediction moves with a feature, on average | global |
| ICE | the same, per row | per row |
| SHAP | how much each feature contributed here | one prediction |
| [Permutation importance](permutation_importance.html) | how much accuracy depends on a feature | global |

## SHAP adds up, exactly

What makes a SHAP explanation trustworthy for one guess is that the parts sum
to the whole. Each feature gets a value saying how far it pushed this guess
from the base value &mdash; the mean guess over the dataset &mdash; and
those pushes rebuild the guess just:

|term|value|
|---|---|
|base value|0.30|
|age|+0.15|
|income|+0.10|
|region|&minus;0.05|
|**prediction**|**0.50**|

`0.30 + 0.15 + 0.10 - 0.05 = 0.50`, with nothing unattributed &mdash; that
additivity is the property partial dependence and ICE don't have, and it's what
lets SHAP explain a single row rather than the model's mean action. The
values come from Shapley values in cooperative game theory, which distribute credit
for a joint outcome fairly, and finding them just means testing each
subset of features &mdash; exponential. This Is why TreeSHAP (exact, fast, for
trees) and KernelSHAP (sampled, for any of it) exist. The caution is that additivity
isn't causality: a model using postcode as a proxy for income will show postcode
adding, which is a true statement about the model and not about the world.

The flat-curve trap is worth restating because it's silent: a partial dependence
line near zero can hide single effects that are large but cancel &mdash; a
feature that slopes up for one subgroup and down for another means to nothing,
while mattering enormously to each row. Plotting the ICE curves underneath is the
standard defence: parallel curves mean the mean is a fair summary, curves that
fan out or cross mean there's an interplay and the mean is lying. Partial
dependence also quietly assumes the feature can be swept on its own of the
others, so with strongly linked features part of the curve is the model
extrapolating into combinations that never occur &mdash; which is what Built up
Local Effects plots were designed to avoid.

## Where it goes wrong

**Reading a flat PD curve as "unimportant".** Plot the ICE curves.

**Skipping linked features.** Part of the curve may be extrapolation.

**Treating SHAP as causal.** It fields a guess, not an outcome. A model
that uses postcode as a proxy for income will show postcode adding, and
that is a fact about the model.

**Blending SHAP values into a global importance and stopping there.** The mean
abs SHAP value is a reasonable global summary, and it discards the direction
and the interplays that made SHAP worth finding.

## Questions people ask

<strong>What does a partial dependence plot show?</strong> The average predicted outcome as one feature varies while the others keep their observed values. It shows the model's average response to that feature.

<strong>When is partial dependence misleading?</strong> When features are correlated, since averaging creates combinations that never occur in real data. ICE curves help reveal whether the average hides different behaviour.

<strong>What are ICE curves?</strong> One line per row showing how its prediction changes as a feature varies. Spread between the lines indicates interactions.

<strong>What is a SHAP value?</strong> The contribution of a feature to one prediction, relative to the average prediction. The contributions across features add up exactly to the difference.

<strong>Is SHAP the same as feature importance?</strong> Averaging the absolute SHAP values over a dataset gives a global importance. But SHAP also explains each row, which importance scores cannot.

<strong>Does SHAP show causation?</strong> No. It explains how the model uses its inputs, not how the world works. A feature can drive predictions simply because it correlates with the true cause.

## One chart for the model, one number per row

Partial dependence shows the model's mean action. A Shapley value shows a single guess. Both are found from scratch here. Neither is a black box.

```python-run
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import partial_dependence
rng = np.random.default_rng(0)
n = 1500
X = rng.normal(size=(n, 4))
y = (3.0 * np.tanh(2 * X[:, 0]) + 1.5 * X[:, 1] + 2.0 * X[:, 0] * X[:, 2]
     + rng.normal(0, 0.4, n))
model = GradientBoostingRegressor(random_state=0).fit(X, y)
print("model R2: %.4f" % model.score(X, y))
print()
print("PARTIAL DEPENDENCE -- vary one feature, average over everything else.")
grid = np.linspace(-2, 2, 9)
print("%8s %12s %12s %12s" % ("value", "PD on x0", "PD on x1", "PD on x3"))
for v in grid:
    row = []
    for c in (0, 1, 3):
        Xc = X.copy(); Xc[:, c] = v
        row.append(model.predict(Xc).mean())
    print("%8.2f %12.4f %12.4f %12.4f" % (v, row[0], row[1], row[2]))
print()
pd0 = partial_dependence(model, X, [0], grid_resolution=9, method="brute")
mine = []
for v in pd0["grid_values"][0]:
    Xc = X.copy(); Xc[:, 0] = v
    mine.append(model.predict(Xc).mean())
print("scikit-learn:", np.round(pd0["average"][0][:5], 4))
print("hand loop   :", np.round(mine[:5], 4))
print("  identical, because that loop IS the definition.")
print()
print("x0 rises then flattens -- that is the tanh. x1 is a straight")
print("line. x3 is flat, because the model never used it.")
```

The next block shows the averaging trap and why a flat PD line can hide real effects.

```python-run
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.inspection import partial_dependence
rng = np.random.default_rng(0)
n = 1500
X = rng.normal(size=(n, 4))
y = (3.0 * np.tanh(2 * X[:, 0]) + 1.5 * X[:, 1] + 2.0 * X[:, 0] * X[:, 2]
     + rng.normal(0, 0.4, n))
model = GradientBoostingRegressor(random_state=0).fit(X, y)

br = partial_dependence(model, X, [0], grid_resolution=9, method="brute")
rec = partial_dependence(model, X, [0], grid_resolution=9, method="recursion")
print("method='brute' re-predicts all rows. 'recursion' walks the trees:")
print("  brute    :", np.round(br["average"][0][:5], 4))
print("  recursion:", np.round(rec["average"][0][:5], 4))
print("  recursion ignores how the other features are distributed.")
print()
print("the trap: partial dependence AVERAGES, so opposite effects cancel.")
print("x2 only matters through its interaction with x0:")
for v in (-2.0, 0.0, 2.0):
    Xc = X.copy(); Xc[:, 2] = v
    lo = X[:, 0] < 0
    print("  x2=%+.0f -> overall PD %7.4f | x0<0 %7.4f, x0>0 %7.4f"
          % (v, model.predict(Xc).mean(), model.predict(Xc)[lo].mean(),
             model.predict(Xc)[~lo].mean()))
print("  the overall column barely moves while the two halves go in")
print("  opposite directions. a flat PD line does not mean unimportant.")
```

The next block computes exact Shapley values for one row, showing how each feature contributes.

```python-run
import numpy as np
from itertools import combinations
from math import factorial
from sklearn.ensemble import GradientBoostingRegressor
rng = np.random.default_rng(0)
n = 1500
X = rng.normal(size=(n, 4))
names = ["x0", "x1", "x2", "x3"]
y = (3.0 * np.tanh(2 * X[:, 0]) + 1.5 * X[:, 1] + 2.0 * X[:, 0] * X[:, 2]
     + rng.normal(0, 0.4, n))
model = GradientBoostingRegressor(random_state=0).fit(X, y)

print("SHAPLEY VALUES -- explain ONE prediction, exactly.")
row = X[7]
base = model.predict(X).mean()
def value(subset):
    Xc = X.copy()
    for c in subset: Xc[:, c] = row[c]
    return model.predict(Xc).mean()
shap = np.zeros(4)
for c in range(4):
    others = [j for j in range(4) if j != c]
    for size in range(4):
        for sub in combinations(others, size):
            w = factorial(size) * factorial(3 - size) / factorial(4)
            shap[c] += w * (value(list(sub) + [c]) - value(list(sub)))
print("  the row:", np.round(row, 3))
print("  average prediction: %8.4f" % base)
for c in range(4):
    print("  %s contributes %+8.4f" % (names[c], shap[c]))
print("  base + contributions: %8.4f" % (base + shap.sum()))
print("  model's prediction  : %8.4f" % model.predict([row])[0])
print("  they match. contributions add up to exactly the gap between")
print("  this prediction and the average. no other method guarantees that.")
```

The next block explains three different rows and shows the cost of exact computation.

```python-run
import numpy as np
from itertools import combinations
from math import factorial
from sklearn.ensemble import GradientBoostingRegressor
rng = np.random.default_rng(0)
n = 1500
X = rng.normal(size=(n, 4))
names = ["x0", "x1", "x2", "x3"]
y = (3.0 * np.tanh(2 * X[:, 0]) + 1.5 * X[:, 1] + 2.0 * X[:, 0] * X[:, 2]
     + rng.normal(0, 0.4, n))
model = GradientBoostingRegressor(random_state=0).fit(X, y)
print("%8s %10s %10s %10s %10s %12s" % ("row", *names, "prediction"))
for i in (7, 100, 900):
    r = X[i]
    sv = np.zeros(4)
    for c in range(4):
        others = [j for j in range(4) if j != c]
        for size in range(4):
            for sub in combinations(others, size):
                w = factorial(size) * factorial(3 - size) / factorial(4)
                Xa, Xb = X.copy(), X.copy()
                for j in list(sub) + [c]: Xa[:, j] = r[j]
                for j in sub: Xb[:, j] = r[j]
                sv[c] += w * (model.predict(Xa).mean() - model.predict(Xb).mean())
    print("%8d %10.3f %10.3f %10.3f %10.3f %12.4f" % (i, *sv, model.predict([r])[0]))
print()
print("x0's contribution changes sign between rows. PD gives one curve")
print("for the whole model; Shapley gives different numbers per row.")
print()
print("exact Shapley needs 2^k coalitions (16 here, >1M at k=20).")
print("TreeSHAP computes them exactly for tree models in polynomial time.")
print("KernelSHAP approximates by sampling coalitions.")
print()
print("both answer 'what did the MODEL do', not 'what causes what'. a")
print("feature can carry a large Shapley value because it proxies for")
print("something the model was never shown.")
```

""",
    [
        {"q": "A partial dependence curve is flat. What can you conclude?",
         "options": ["The feature does not matter",
                     "Only that the average effect is near zero - it may matter enormously in opposite directions by subgroup",
                     "The model is underfitted",
                     "The feature is correlated with another"],
         "answer": 1,
         "why": "Plotting ICE curves settles it: if they are parallel the average is a fair summary; if they fan out or cross, there is an interaction the average cancels."},
        {"q": "What does the additivity of SHAP values give you?",
         "options": ["Faster computation",
                     "The values sum exactly to the gap between the base value and this prediction, so nothing is unattributed",
                     "Independence from the model type",
                     "Causal interpretation"],
         "answer": 1,
         "why": "That is what makes it usable as an explanation of a single prediction. Exact computation is exponential, so TreeSHAP and KernelSHAP approximate it."},
        {"q": "Why can part of a partial dependence curve be untrustworthy when features are correlated?",
         "options": ["The averaging is biased",
                     "It sets the feature to values that never co-occur with the other columns, so the model is extrapolating",
                     "The curve becomes non-monotonic",
                     "ICE curves cannot be computed"],
         "answer": 1,
         "why": "Sweeping age across every row creates people aged 18 with forty years of experience. ALE plots avoid this by varying a feature only within ranges that actually occur."},
    ],
)


# ---------------------------------------------------------------------------
# 18. Probability calibration
# ---------------------------------------------------------------------------
topic(
    "probability_calibration",
    "Probability Calibration",
    "Evaluation",
    "A model that says 0.8 should be right 80% of the time. Most are not, and "
    "AUC will never tell you.",
    _svg(_axes() + _line(22, 66, 142, 22, B, 1.2, "4 3")
         + '<path d="M22 66 C 60 60, 78 34, 142 22" fill="none" stroke="%s" stroke-width="2"/>' % A
         + _txt(96, 58, "over-confident", M, 7)),
    {
        "sim": "calibration",
        "controls": [
            {"key": "temperature", "label": "Temperature", "type": "range",
             "min": 0.4, "max": 2.2, "step": 0.05, "value": 0.6},
        ],
    },
    [
        "A <strong>reliability diagram</strong> bins predictions by confidence "
        "and plots the observed frequency in each bin.",
        "Perfect calibration is the diagonal. Below it means over-confident; "
        "above it means under-confident.",
        "<strong>ECE</strong> is the average gap between confidence and observed "
        "frequency, weighted by bin size.",
        "Calibration and ranking are independent. The slider changes calibration "
        "dramatically and leaves AUC untouched.",
    ],
    """
title: Probability Calibration
intro: Whether a model's trust means any of it. Why each ranking metric is blind to it.

## Two different questions

**Discrimination** asks whether the model ranks positives above negatives. AUC
and [ROC](precision_recall_vs_roc.html) measure this.

**Calibration** asks whether the numbers mean what they say. Of all the cases
where the model said 0.8, were about 80% really plus?

A model can be great at one and terrible at the other, and this isn't an
edge case &mdash; it's the normal situation.

## The slider proves it

Drag the temperature control and watch the curve deform. That control performs
**temperature scaling**: it divides the logit by a constant before the sigmoid.
Cutting by a number less than one sharpens each score toward 0 or 1. Cutting
by a number greater than one flattens them toward 0.5.

Critically, this is a **monotonic** change. It never changes the order of
any two guesses. each ranking metric &mdash; AUC, mean precision,
any of it based on sorting. Is **the same at each setting of that
slider**, while the trust curve swings from badly too sure to badly
too shy.

Which is the point. If you only ever look at AUC, you've no info about
calibration at all.

## Reading the diagram

guesses are binned by trust, and each bin plots mean trust against
seen rate.

**On the diagonal**: calibrated.

**Below the diagonal**: over-confident. The model says 0.9 and is right 70% of
the time. This is the common failure, and the damaging one.

**Above the diagonal**: under-confident. The model hedges when it should not.

**ECE** &mdash; expected calibration error &mdash; is the mean vertical
distance, weighted by how many points fall in each bin. It's the number in the
readout, and it's a summary that can hide compensating errors: a curve that is
above the main-line in one region and below in another can report a small ECE.
Look at the curve, not only the number.

## Why models come out miscalibrated

**Modern neural networks are too sure**, and increasingly so as they get
larger. Training to cut cross-entropy on data it can fit just right pushes
outputs toward 0 and 1 long after the fit has stopped raising.

**Support vector machines** give distances from a hyperplane, not
chances, and passing them through a sigmoid doesn't make them
chances.

**Naive Bayes** is famously too sure because its freedom assumption
times linked evidence as though it were free.

**Random forests** tend to be too shy at the extremes, because blending
many trees pulls guesses toward the middle.

Logistic regression, fitted on well-given features, is often close to
calibrated &mdash; it optimises just this.

## Fixing it

All three methods fit a correction on a **held-out** set, never on the training
data.

**Platt scaling.** Fit a logistic regression to map scores to chances. One
or two params, works on small validation sets, assumes the distortion is
sigmoid-shaped.

**Temperature scaling.** The single-param version, and the standard for
neural networks. Because it changes no rankings, fit and AUC are ensured
untouched &mdash; a rare free lunch.

**Isotonic regression.** Fits any monotonic mapping. More flexible, and needs
a lot more data or it overfits the validation set.

## When it matters

**When a chance feeds a choice with costs.** Expected value is
chance times payoff, so a wrong chance is a wrong choice even when
the ranking is perfect.

**Medical and risk contexts**. Here "30% chance" is communicated to a person.

**When scores are mixed** across models or over time.

**When a threshold is set from a target rate.** [Choosing a
threshold](threshold_tuning.html) from calibrated chances gives the rate
you asked for. From uncalibrated scores it doesn't.

If all you do is rank. Show the top 100 results &mdash; calibration is
irrelevant.

## Expected calibration error, worked

ECE puts a single number on "do the confidences mean any of it". Bin the
guesses by stated trust, and in each bin compare the mean trust
against the fraction really plus. ECE is the mean gap, weighted by bin
size:

|bin|mean confidence|observed accuracy|gap|
|---|---|---|---|
|high|0.90|0.70|0.20|
|mid|0.70|0.65|0.05|
|low|0.55|0.55|0.00|

With 100 points in each bin the ECE is `(0.20 + 0.05 + 0.00)/3 = 0.083` &mdash;
the model is eight points miscalibrated on average, driven almost fully by the
top bin, where it says 0.90 and is right 70% of the time. That over-trust is
the common and damaging failure, and note what it does *not* touch: each one of
those guesses could still rank right. So AUC and mean precision are
unchanged. Temperature scaling &mdash; cutting the logit by a constant fitted on
held-out data &mdash; pulls the top bin down toward its true fit without
reordering any of it. This Is why it can fix calibration for free while leaving
each ranking metric the same. The one caution is that ECE is an mean and can
hide compensating errors, so a curve above the main-line in one region and below in
another can post a small ECE. Read the trust curve, not only the number.

Why models miscalibrate is worth knowing, because it predicts which fix to reach
for. Modern neural networks are too sure and increasingly so as they grow,
because cutting cross-entropy on data they can fit just right keeps pushing
outputs toward 0 and 1 long after fit has stopped raising. Temperature
scaling is the standard remedy. Naive Bayes is too sure because its
freedom assumption times linked evidence as if it were free.
Random forests are often *under*-confident at the extremes, because blending many
trees pulls guesses toward the middle. Logistic regression on well-given
features tends to come out close to calibrated. That is just what it
optimises.

## Where it goes wrong

**Calibrating on the training set.** It will look perfect and generalise
nothing.

**Isotonic regression on a small validation set.** It overfits.

**given a good AUC implies good chances.** The slider on this page
exists to disprove just that.

**Recalibrating without re-checking after data drift.** A calibration fitted last
year shows last year's spread.

## Questions people ask

<strong>What does calibrated mean?</strong> Among predictions of 0.8, about 80 percent are positive. The output can be read as a real probability.

<strong>Can a model be accurate and miscalibrated?</strong> Yes. Accuracy depends on the ranking and the threshold, while calibration depends on whether the number matches the actual frequency.

<strong>How do I check calibration?</strong> Plot a reliability diagram, binning predictions and comparing the mean prediction with the observed rate. Brier score and expected calibration error give single numbers.

<strong>Platt scaling or isotonic regression?</strong> Platt scaling fits a sigmoid and works with small data. Isotonic is more flexible but can overfit below roughly a thousand samples.

<strong>Which models are usually miscalibrated?</strong> Random forests tend to be under-confident near 0 and 1, boosting and SVMs are distorted, and naive Bayes is often over-confident. Logistic regression is usually close.

<strong>When does calibration matter?</strong> When you use the probability itself, for example expected cost, risk scores or combining with other estimates. If you only rank or classify, it matters less.

## When 0.9 does not mean 90%

A model can rank just right and still lie about its trust. This measures the gap, then closes it two different ways.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.calibration import calibration_curve
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss
X, y = make_classification(n_samples=12000, n_features=15, n_informative=6,
                           flip_y=0.12, random_state=0)
Xtr, Xrest, ytr, yrest = train_test_split(X, y, test_size=0.5, random_state=0)
_, Xte, _, yte = train_test_split(Xrest, yrest, test_size=0.5, random_state=0)
models = {"logistic regression": LogisticRegression(max_iter=3000),
          "random forest": RandomForestClassifier(n_estimators=200, random_state=0),
          "naive bayes": GaussianNB(),
          "SVM (rbf)": SVC(probability=True, random_state=0)}
print("%-22s %9s %9s %10s" % ("", "ROC AUC", "Brier", "log loss"))
probs = {}
for name, m in models.items():
    probs[name] = m.fit(Xtr, ytr).predict_proba(Xte)[:, 1]
    print("%-22s %9.4f %9.4f %10.4f"
          % (name, roc_auc_score(yte, probs[name]),
             brier_score_loss(yte, probs[name]), log_loss(yte, probs[name])))
print()
print("ROC AUC only cares about the ORDER. Brier and log loss care about")
print("the numbers themselves.")
print()
print("the reliability table -- group predictions by confidence:")
for name in ("logistic regression", "naive bayes"):
    print("  %s" % name)
    frac, mean_pred = calibration_curve(yte, probs[name], n_bins=8, strategy="quantile")
    print("     %12s %14s %10s" % ("said", "actually was", "error"))
    for mp, fp in zip(mean_pred, frac):
        print("     %12.4f %14.4f %+10.4f" % (mp, fp, fp - mp))
    print()
print("a perfectly calibrated model has zeros in that last column.")
```

The next block fixes the miscalibration two different ways and shows the reliability table after.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.naive_bayes import GaussianNB
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, brier_score_loss
X, y = make_classification(n_samples=12000, n_features=15, n_informative=6,
                           flip_y=0.12, random_state=0)
Xtr, Xrest, ytr, yrest = train_test_split(X, y, test_size=0.5, random_state=0)
Xcal, Xte, ycal, yte = train_test_split(Xrest, yrest, test_size=0.5, random_state=0)
raw = GaussianNB().fit(Xtr, ytr)
raw_p = raw.predict_proba(Xte)[:, 1]
print("two ways to fix it, both on a held-out calibration split:")
print("  %-26s Brier %.4f" % ("naive bayes, raw", brier_score_loss(yte, raw_p)))
for method in ("sigmoid", "isotonic"):
    cal = CalibratedClassifierCV(raw, method=method, cv="prefit")
    cal.fit(Xcal, ycal)
    p = cal.predict_proba(Xte)[:, 1]
    print("  %-26s Brier %.4f   AUC %.4f"
          % ("naive bayes + " + method, brier_score_loss(yte, p),
             roc_auc_score(yte, p)))
print()
print("reliability table after sigmoid calibration:")
cal = CalibratedClassifierCV(raw, method="sigmoid", cv="prefit").fit(Xcal, ycal)
pc = cal.predict_proba(Xte)[:, 1]
frac, mean_pred = calibration_curve(yte, pc, n_bins=8, strategy="quantile")
print("     %12s %14s %10s" % ("said", "actually was", "error"))
for mp, fp in zip(mean_pred, frac):
    print("     %12.4f %14.4f %+10.4f" % (mp, fp, fp - mp))
f0, m0 = calibration_curve(yte, raw_p, n_bins=8, strategy="quantile")
print("  worst error: %.4f before, %.4f after"
      % (np.abs(f0 - m0).max(), np.abs(frac - mean_pred).max()))
print()
print("sigmoid (Platt) fits a one-parameter squash -- needs little data.")
print("isotonic fits any increasing function, more prone to overfit.")
print("the AUC barely moves: calibration is monotone, so it relabels")
print("confidence without changing the ranking.")
print()
print("this matters when the number leaves the model: thresholds, risk")
print("scores, expected-value calculations. argmax users can ignore it.")
```

""",
    [
        {"q": "Why is AUC unchanged as the temperature slider moves?",
         "options": ["AUC is insensitive to class imbalance",
                     "Temperature scaling is monotonic, so it never changes the order of any two predictions",
                     "The model is retrained each time",
                     "AUC uses only the top predictions"],
         "answer": 1,
         "why": "Every ranking metric is identical at every setting, while calibration swings from badly over-confident to badly under-confident. Looking only at AUC tells you nothing about calibration."},
        {"q": "A reliability curve sits below the diagonal. The model is:",
         "options": ["Under-confident", "Over-confident", "Well calibrated", "Poorly ranked"],
         "answer": 1,
         "why": "It says 0.9 and is right 70% of the time. This is the common failure mode for modern neural networks, and the damaging one when probabilities feed decisions."},
        {"q": "When does calibration not matter?",
         "options": ["When the model is a neural network",
                     "When the output is only used to rank - showing the top 100 results, say",
                     "When the classes are balanced",
                     "When AUC is high"],
         "answer": 1,
         "why": "It matters whenever a probability feeds a decision with costs, because expected value is probability times payoff, so a wrong probability is a wrong decision."},
    ],
)


# ---------------------------------------------------------------------------
# 19. Isolation Forest
# ---------------------------------------------------------------------------
topic(
    "isolation_forest",
    "Isolation Forest",
    "Anomaly Detection",
    "Anomalies are easy to cut off from everything else. Count the cuts, and "
    "you have an anomaly score without ever modelling normal.",
    _svg(_axes()
         + "".join(_dot(66 + (i % 5) * 6, 34 + (i // 5) * 6, M) for i in range(20))
         + _dot(32, 26, A, 4) + _dot(134, 62, A, 4)
         + _line(50, 18, 50, 70, B, 1, "3 3") + _line(20, 44, 148, 44, B, 1, "3 3")
         + _txt(80, 82, "few cuts to isolate", M, 7)),
    {
        "sim": "isoforest",
        "controls": [
            {"key": "trees", "label": "Trees", "type": "range",
             "min": 5, "max": 120, "step": 5, "value": 60},
            {"key": "sample", "label": "Points sampled per tree", "type": "range",
             "min": 16, "max": 128, "step": 8, "value": 64},
            {"key": "threshold", "label": "Score threshold", "type": "range",
             "min": 0.40, "max": 0.72, "step": 0.01, "value": 0.62},
            {"key": "seed", "label": "Forest seed", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 3},
        ],
    },
    [
        "Split the data on a random feature at a random value, repeatedly, until "
        "each point is alone.",
        "Points in sparse regions get cut off in a few splits. Points in dense "
        "regions need many.",
        "The score is the average path length across many trees, normalised. "
        "<strong>Short path, high score.</strong>",
        "It never learns what normal looks like &mdash; only what is easy to "
        "separate, which is why it needs no labels.",
    ],
    """
title: Isolation Forest
intro: Outlier spotting that looks for what is easy to cut off, rather than modelling what is normal.

## Inverting the usual approach

Most outlier spotting builds a model of normal &mdash; fit a spread,
guess a density, learn a boundary. And flags what falls outside.
That is hard work, and in high dims density estimation is very hard work.

Alone Forest asks a different question: **how much effort does it take to
separate this point from all else?**

Pick a random feature, pick a random split value between its min and max,
and divide the data. Repeat on each half until each point sits alone.

A point far from the rest gets cut off almost right away &mdash; a single random
split has a good chance of landing between it and the crowd. A point in the
middle of a dense cluster lives many splits. Each cut has to be
placed among tightly packed neighbours.

**Path length is the outlier measure**, and no model of normality was ever built.

## The score

The raw quantity is the mean path length across the forest. It's normed
against the expected path length in a random binary tree of the same size,
because deeper trees on its own have longer paths:

```
score = 2 ^ ( -avg_path / c(n) )
```

The direction catches people out. A **short** path means easy to isolate, which
means **anomalous**, which means a **high** score. Around 0.5 is plain;
above about 0.6 on this page is worth a look.

Drag the threshold and watch the count. The readout gives the range of scores
present, so you can see where the group really sits rather than guessing.

## Subsampling, and why it helps

Each tree is built from a small random subsample. 256 points by default in
most libraries &mdash; and this isn't only for speed.

With the full dataset, a cluster of outliers can be dense enough to look normal
locally: its members shield each other and need a few splits to separate. Take
a small sample and those outliers are often alone in it, so they're isolated
right away. Subsampling reduces *swamping* (normal points looking anomalous
because the data is crowded) and *masking* (outliers hiding one another).

The trees control shows the other half of the picture. At five trees the flagged
set jitters as you change the seed. At sixty it's stable. Path length from one
random tree is nearly meaningless, and the mean over many isn't.

**Each tree is built from a sample and then used to score each point.** Building
and scoring on the same subsample is a mistake worth naming: a point missing from
a tree adds nothing that round, its mean path comes out short, and it
looks like an outlier. All ends up flagged.

## What it is good at

**Speed.** Linear in the number of points, and the trees are shallow. It's one
of the few outlier finders that is truly cheap on large data.

**High dims.** No distance metric, so it avoids the concentration problem
that undoes k-nearest-neighbour approaches.

**No labels.** fully unsupervised.

**No distributional assumption.** Unlike a Gaussian-based finder, it doesn't
care what shape normal is.

## What it is bad at

**Local outliers.** It finds points that are globally easy to separate. A point
sitting in a *low-density gap between two dense clusters* may be just right normal
globally and clearly anomalous locally. **Local Outlier Factor** checks each
point's density to its neighbours' and catches these.

**Axis-aligned splits.** Cuts are at right angles to the axes, which makes
artefacts along main-lines in linked data. **Extended Alone Forest** uses
random hyperplanes instead.

**Irrelevant features.** Random feature pick wastes splits on columns that
carry nothing.

**The contamination param.** Libraries ask what fraction of the data is
anomalous to place a threshold, and if you knew that you'd be much
further along. Prefer to look at the score spread and choose a cut, which
is what the slider here makes you do.

## The path-length score, worked

The score turns an mean path length into a number between 0 and 1, and working
it shows why the direction is what it's. With a 256-point subsample the expected
path in a random tree is `c(256) &asymp; 10.24`, and `score = 2^(-avg_path / c(n))`:

|average path to isolate the point|score|reading|
|---|---|---|
|3 (cut off early)|0.82|anomalous|
|8 (survived many cuts)|0.58|nearer normal|

A point far from the crowd is separated by one or two random splits &mdash; a
single cut has a good chance of landing in the empty space around it &mdash; so its
path is short, its score high. It's flagged. A point buried in a dense cluster
needs many splits to peel away from its neighbours. Its path is long and its
score low. Short path, high score, anomalous: the tie that catches people
because it runs opposite to the intuition that a bigger number is safer. The
256-point subsample isn't only for speed. A small sample often holds a
would-be outlier alone, so it isolates right away. Here In the full data a tight
clump of outliers can shield each other and live a few cuts (masking). And
the mean is over many trees for a reason: one tree's path length is nearly
meaningless, and the flagged set only settles across dozens.

What Alone Forest is good and bad at both follow from that random-split
mechanism. It's fast &mdash; linear in the points, with shallow trees &mdash; and
indifferent to dimensionality, since it uses no distance metric and so escapes the
concentration that undoes k-nearest-neighbour finders, and it assumes nothing
about the shape of "normal". But it finds only *globally* easy-to-separate points:
a point sitting in a low-density gap between two dense clusters can be just right
plain globally and clearly anomalous locally. This Is what Local Outlier Factor
catches by checking each point's density to its neighbours'. And its
`contamination` param, which asks what fraction of the data is anomalous, is a
guess presented as a setting. Better to read the score spread and cut
it yourself.

## Where it goes wrong

**Reading the score backwards.** High means anomalous.

**Too few trees.** The estimate is noisy. Check by changing the seed.

**Trusting `contamination`.** It's a guess presented as a param.

**Expecting it to find local outliers.** Use LOF for those.

## Questions people ask

<strong>How does Isolation Forest find anomalies?</strong> It builds random trees that split features at random values. Anomalies are few and different, so they are isolated in fewer splits, which gives them a short average path length.

<strong>What does the contamination parameter do?</strong> It sets the fraction of points you expect to be anomalies and so sets the decision threshold. If you do not know it, use the raw scores and choose a cutoff yourself.

<strong>Do I need to scale features?</strong> No. Splits are made on single features, so scale does not matter.

<strong>Why subsample?</strong> Smaller subsamples (256 by default) reduce masking and swamping, where normal points hide anomalies or look like them. It also makes training fast.

<strong>What does Isolation Forest miss?</strong> Anomalies that are only unusual in combinations of features at very high dimension, and local anomalies hidden inside dense regions. Irrelevant features also dilute the score.

<strong>How do I read the score?</strong> Scores near 1 are likely anomalies and scores well under 0.5 are normal. In scikit-learn, score_samples returns the negated version, where lower is more anomalous.

## Finding outliers by how easy they are to separate

Alone Forest splits at random and counts how few cuts it takes to isolate a point. Outliers fall out early. That path length is the entire score.

```python-run
import numpy as np
from sklearn.ensemble import IsolationForest
rng = np.random.default_rng(0)
normal = rng.normal(0, 1, (960, 2))
weird = rng.uniform(-6, 6, (40, 2))
X = np.vstack([normal, weird])
truth = np.r_[np.ones(960), -np.ones(40)]
print("960 normal points and %d scattered ones. no labels." % len(weird))

iso = IsolationForest(contamination=0.04, random_state=0).fit(X)
pred = iso.predict(X)
print("caught %d of the %d planted anomalies"
      % (((pred == -1) & (truth == -1)).sum(), (truth == -1).sum()))
print("false alarms on normal points: %d" % ((pred == -1) & (truth == 1)).sum())
print()

print("the score IS the average path length, rescaled. shorter = weirder:")
s = iso.score_samples(X)
order = np.argsort(s)
print("  five most anomalous points:")
for i in order[:5]:
    print("    %s  score %.4f  %s"
          % (np.round(X[i], 3), s[i], "planted" if truth[i] < 0 else "normal"))
print("  five most normal points:")
for i in order[-5:]:
    print("    %s  score %.4f  %s"
          % (np.round(X[i], 3), s[i], "planted" if truth[i] < 0 else "normal"))
print()

print("distance from the centre, against the score:")
dist = np.linalg.norm(X, axis=1)
for lo, hi in ((0, 1), (1, 2), (2, 3), (3, 8)):
    m = (dist >= lo) & (dist < hi)
    if m.any():
        print("  %d-%d sd from centre: %4d points, mean score %.4f, flagged %d"
              % (lo, hi, m.sum(), s[m].mean(), (pred[m] == -1).sum()))
print("  no distance was computed. random splits isolate far-out points")
print("  in fewer cuts, and that is all the algorithm knows.")
```

The next block shows how the contamination parameter works and compares Isolation Forest against the other unsupervised detectors.

```python-run
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
rng = np.random.default_rng(0)
normal = rng.normal(0, 1, (960, 2))
weird = rng.uniform(-6, 6, (40, 2))
X = np.vstack([normal, weird])
truth = np.r_[np.ones(960), -np.ones(40)]

print("contamination is not a threshold on weirdness -- it is a quota:")
for c in (0.01, 0.04, 0.10, 0.25):
    p = IsolationForest(contamination=c, random_state=0).fit_predict(X)
    print("  contamination=%.2f -> flagged %3d (%.1f%% of %d), caught %2d real"
          % (c, (p == -1).sum(), 100 * (p == -1).mean(), len(X),
             ((p == -1) & (truth == -1)).sum()))
print("  it always flags that fraction, whether or not anything is wrong.")
print()

print("against the other unsupervised detectors, same data:")
for name, m in (("Isolation Forest", IsolationForest(contamination=0.04, random_state=0)),
                ("One-Class SVM", OneClassSVM(nu=0.04, gamma="scale")),
                ("Elliptic Envelope", EllipticEnvelope(contamination=0.04, random_state=0)),
                ("Local Outlier Factor", LocalOutlierFactor(contamination=0.04))):
    p = m.fit_predict(X)
    print("  %-22s caught %2d of %d, %3d false alarms"
          % (name, ((p == -1) & (truth == -1)).sum(), (truth == -1).sum(),
             ((p == -1) & (truth == 1)).sum()))
print()
print("Isolation Forest is the usual first choice: linear in the number")
print("of rows, needs no distance metric, survives high dimensions.")
print("Elliptic Envelope assumes one gaussian blob -- fast when that is")
print("true, useless when it is not.")
```

""",
    [
        {"q": "Why does a short average path length mean a point is anomalous?",
         "options": ["It is close to the root of the tree by chance",
                     "A point far from the rest is separated by a random split quickly, while a point in a dense region needs many splits",
                     "Short paths indicate low variance",
                     "The tree is pruned around outliers"],
         "answer": 1,
         "why": "Path length is the effort required to isolate the point. No model of normality is ever built - the score falls out of how easy separation is."},
        {"q": "Why is each tree built from a small subsample?",
         "options": ["Only for speed",
                     "It also reduces masking - in the full data a cluster of anomalies can shield its own members and look normal",
                     "To avoid overfitting the threshold",
                     "Because trees cannot handle large inputs"],
         "answer": 1,
         "why": "In a small sample those anomalies are usually alone and isolated immediately. It reduces swamping too - normal points looking anomalous because the data is crowded."},
        {"q": "Which anomaly does Isolation Forest tend to miss?",
         "options": ["A point far outside the whole dataset",
                     "A point in a low-density gap between two dense clusters, which is normal globally but anomalous locally",
                     "A duplicate row",
                     "A point with an extreme value in one feature"],
         "answer": 1,
         "why": "It finds points that are globally easy to separate. Local Outlier Factor compares each point's density with its neighbours' and catches these instead."},
    ],
)


# ---------------------------------------------------------------------------
# 20. Stacking and voting
# ---------------------------------------------------------------------------
topic(
    "stacking_and_voting",
    "Stacking and Voting Ensembles",
    "Ensembles",
    "Combining different models rather than many copies of one, and the case "
    "where a majority vote makes things worse.",
    _svg(_box(12, 22, 34, 16, fill=S) + _box(12, 44, 34, 16, fill=S)
         + _box(12, 66, 34, 12, fill=S)
         + _line(46, 30, 74, 46, B, 1) + _line(46, 52, 74, 48, B, 1)
         + _line(46, 72, 74, 52, B, 1)
         + _box(78, 38, 40, 22, fill=S, stroke=A) + _txt(98, 52, "combiner", A, 7)
         + _txt(80, 88, "weights, not votes", M, 7)),
    {
        "sim": "ensembles",
        "controls": [
            {"key": "t1", "label": "Stump on a: threshold", "type": "range",
             "min": -1.5, "max": 1.5, "step": 0.1, "value": 0.9},
            {"key": "t2", "label": "Stump on b: threshold", "type": "range",
             "min": -1.5, "max": 1.5, "step": 0.1, "value": 0.9},
            {"key": "t3", "label": "Radius rule: threshold", "type": "range",
             "min": 0.6, "max": 3.0, "step": 0.1, "value": 1.6},
        ],
    },
    [
        "<strong>Voting</strong> combines predictions by majority, or by "
        "averaging probabilities. Every model counts equally.",
        "<strong>Stacking</strong> trains a second model &mdash; the "
        "meta-learner &mdash; on the base models' predictions, so it can weight them.",
        "Bagging and boosting combine many copies of <em>one</em> model. Voting "
        "and stacking combine <em>different</em> models.",
        "An ensemble helps when the members make <strong>different mistakes</strong>. "
        "Three models that fail on the same rows gain nothing.",
    ],
    """
title: Stacking and Voting Ensembles
intro: Mixing unlike models, when it helps, and a live demo of it hurting.

## Different from bagging and boosting

[Bagging](random_forest.html) and [boosting](gradient_boosting.html) build many
copies of one kind of model. Hundreds of trees &mdash; and combine them.

Voting and stacking combine models of *different* kinds: a logistic regression, a
grad-boosted tree and a neural network, say. The hope is that models with
different inductive biases fail on different rows. So Their errors partly cancel.

That hope is a rule, not a ensure, and this page is largely about the
rule failing.

## Voting

**Hard voting** takes the majority label. **Soft voting** means predicted
chances and thresholds the mean. This Is often better because it uses
trust rather than discarding it &mdash; and which needs
[calibrated](probability_calibration.html) chances to be real.

each member counts equally. That is the strength when the members are close
and the weakness when they aren't.

Look at the readout with the default settings. Three learners score roughly
62%, 66% and 90%, and the **majority vote scores about 77% &mdash; worse than the
best member alone.** Two weak learners outvote a strong one when they agree,
and they agree often enough to drag the result down.

This isn't a contrived setup. It's what happens when an ensemble is
assembled without checking whether the members are of close quality, and it
is the reason "just ensemble it" is bad advice.

## Stacking

Stacking replaces the fixed rule with a learned one. Train the base models, take
their guesses as features, and fit a second model &mdash; the **meta-learner**
&mdash; on those.

The meta-learner discovers what a vote can't: which model to trust, and when.
The learned weights are in the readout, and the strong learner attracts most of
the weight while a weak one can go slightly minus &mdash; meaning the
meta-learner has found that model to be worse than uninformative in some regions.

With the defaults, stacking matches the best single learner rather than beating
it. That is an honest and common outcome. It's still a gain over the vote:
stacking got back the best model automatically. Here Voting destroyed it.

Move the thresholds so that the three learners are closer in quality, and the
picture changes &mdash; the vote catches up, because its assumption is finally
true.

## Getting stacking right

The key detail is how the meta-learner's training data is made.

Training the base models and then feeding their guesses **on the same data**
to the meta-learner leaks badly. A model that overfits its training set makes
oddly good guesses there, so the meta-learner learns to trust the most
overfitted member.

The fix is **cross-validated guesses**: split the data into folds, and for
each fold predict with base models trained on the other folds. each guess
the meta-learner sees is then out-of-sample. This is what scikit-learn's
`StackingClassifier` does, and it's why stacking costs roughly *k* times the
training of its members.

A second rule: keep the meta-learner **simple**. Logistic regression is the
standard choice. It has few base guesses to work with, and a flexible
meta-learner overfits them readily.

## When an ensemble is worth it

**Members must be close in quality.** Or else voting hurts, as above.

**Members must make different mistakes.** Three models that fail on the same rows
combine into one model that fails on those rows. Checking the link of
their errors is the diagnostic, and it's worth doing before building any of it.

**The gain must justify the cost.** An ensemble times training time,
inference time, memory and the number of things that can break in production. A
one-point gain on a leaderboard is worth it. A one-point gain in a service
often isn't.

## When the majority is wrong, in numbers

Majority voting only helps when the members are close, and the math
shows why. For three free classifiers the vote is correct when at least two
are, `P = &Sigma;` over the majority outcomes:

|three members|majority-vote accuracy|
|---|---|
|0.62, 0.66, 0.90|0.83 &mdash; **below the 0.90 member**|
|0.80, 0.80, 0.80|0.90 &mdash; above any member|

Three equal 80% models vote to 90%. This Is the ensemble win everyone hopes for:
free errors partly cancel. But bolt a 90% model to two mediocre ones and
the vote drops it to 83%. When the two weak members happen to agree
they outvote the strong one, and two coin-ish models agree wrongly often enough to
matter. That is voting's built-in assumption &mdash; equal competence &mdash;
failing out loud, and it's why "just ensemble it" is bad advice without checking
the members are close. Stacking fixes just this by learning the weights
instead of fixing them: the meta-learner hands most of the weight to the strong
member and can drive a weak one minus, getting back the best model where the vote
destroyed it. (Real classifiers aren't free, so the true numbers shift
with error link &mdash; which is itself the thing to measure before
mixing any of it.)

Getting stacking right turns on one detail: the meta-learner must be trained on
*out-of-sample* base guesses. Feed it guesses the base models made on their
own training data and it learns to trust whichever member overfitted most, because
an overfitted model looks oddly accurate there. The fix is cross-validated
guesses &mdash; for each fold, predict with base models trained on the other
folds &mdash; which is why stacking costs roughly k times the training of its
members. Keep the meta-learner simple, too. Logistic regression is the standard
choice, because it has few base guesses to work from and a flexible meta-learner
overfits them readily.

## Where it goes wrong

**Ensembling a strong model with weak ones by vote.** Shown above.

**Fitting the meta-learner on in-sample guesses.** It learns to trust the
most overfitted base model.

**A complex meta-learner.** Few features, plenty of opportunity to overfit.

**given range.** Two grad-boosted models with different seeds aren't
diverse. Check whether their errors really differ.

## Questions people ask

<strong>What is the difference between voting and stacking?</strong> Voting combines predictions with a fixed rule, such as majority or average. Stacking trains a meta-model to learn how to combine them.

<strong>Hard or soft voting?</strong> Soft voting averages probabilities and usually does better when models produce reasonable probabilities. Hard voting counts class labels.

<strong>Why does stacking need cross-validated predictions?</strong> If the meta-model trains on predictions the base models made on their own training data, it learns to trust overfit outputs. Out-of-fold predictions avoid that.

<strong>Do ensembles always beat the best single model?</strong> No. If the models make the same mistakes, combining them adds little. The gain comes from diverse errors.

<strong>What should the meta-model be?</strong> Something simple, like logistic regression or ridge. A flexible meta-model overfits easily.

<strong>Is an ensemble worth the complexity?</strong> Sometimes for a small accuracy gain in competitions or high-stakes cases. In production, check that the gain justifies slower inference and harder maintenance.

## Ensembling models that make different mistakes

Mixing models only helps when they're wrong about different rows. This measures that disagreement first, then shows what voting and stacking do with it.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
X, y = make_classification(n_samples=4000, n_features=15, n_informative=6,
                           n_clusters_per_class=2, flip_y=0.12, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
base = [
    ("logistic", make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))),
    ("tree",     DecisionTreeClassifier(max_depth=8, random_state=0)),
    ("knn",      make_pipeline(StandardScaler(), KNeighborsClassifier(15))),
    ("bayes",    GaussianNB()),
]
preds = {}
for name, m in base:
    preds[name] = m.fit(Xtr, ytr).predict(Xte)
    print("%-10s accuracy %.4f" % (name, (preds[name] == yte).mean()))
print()
print("how often each PAIR gets a row wrong at the same time:")
names = list(preds)
wrong = {n: preds[n] != yte for n in names}
print("%-10s %s" % ("", "".join("%10s" % n for n in names)))
for a in names:
    row = ""
    for b in names:
        both = (wrong[a] & wrong[b]).sum() / max(wrong[a].sum(), 1)
        row += "%10.3f" % both
    print("%-10s %s" % (a, row))
print("  (of rows THIS model got wrong, what fraction did THAT one also miss.)")
print()
any_right = (~np.all([wrong[n] for n in names], axis=0)).mean()
all_wrong = np.all([wrong[n] for n in names], axis=0).mean()
print("  at least one model is right on %.4f of rows." % any_right)
print("  all four are wrong together on %.4f." % all_wrong)
print("  that first number is the ceiling any combiner can reach.")
```

The next block compares hard voting, soft voting and stacking on the same data.

```python-run
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import VotingClassifier, StackingClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
X, y = make_classification(n_samples=4000, n_features=15, n_informative=6,
                           n_clusters_per_class=2, flip_y=0.12, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
base = [
    ("logistic", make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000))),
    ("tree",     DecisionTreeClassifier(max_depth=8, random_state=0)),
    ("knn",      make_pipeline(StandardScaler(), KNeighborsClassifier(15))),
    ("bayes",    GaussianNB()),
]
names = [n for n, _ in base]
hard = VotingClassifier(base, voting="hard")
soft = VotingClassifier(base, voting="soft")
stack = StackingClassifier(base,
    final_estimator=LogisticRegression(max_iter=3000), cv=5)
for name, m in (("hard voting (majority)", hard),
                ("soft voting (avg probability)", soft),
                ("stacking (model on outputs)", stack)):
    print("%-34s cv %.4f" % (name, cross_val_score(m, X, y, cv=5).mean()))
print("%-34s cv %.4f"
      % ("best single model",
         max(cross_val_score(m, X, y, cv=5).mean() for _, m in base)))
print()
stack.fit(Xtr, ytr)
print("what stacking learned about which model to trust:")
for name, w in zip(names, stack.final_estimator_.coef_[0]):
    print("   %-10s weight %+7.4f" % (name, w))
print("  a negative weight means the combiner leans against that model.")
print()
print("soft beats hard because 0.51 and 0.99 carry different evidence.")
print("stacking needs cv predictions or training optimism leaks in.")
```

""",
    [
        {"q": "Why can a majority vote score worse than its best member?",
         "options": ["The vote discards probabilities",
                     "Every member counts equally, so two weak learners can outvote a strong one whenever they agree",
                     "Voting requires an odd number of models",
                     "The members were not calibrated"],
         "answer": 1,
         "why": "It is what happens whenever an ensemble is assembled without checking the members are comparable in quality - which is why 'just ensemble it' is bad advice."},
        {"q": "Why must the meta-learner be trained on cross-validated predictions?",
         "options": ["To save computation",
                     "In-sample predictions look suspiciously good for an overfitted base model, so the meta-learner learns to trust it",
                     "To balance the classes",
                     "Because base models need to be retrained anyway"],
         "answer": 1,
         "why": "Every prediction the meta-learner sees has to be out-of-sample. It is why stacking costs roughly k times the training of its members."},
        {"q": "What condition must hold for an ensemble to help at all?",
         "options": ["The members must be the same type of model",
                     "The members must make different mistakes",
                     "There must be an odd number of members",
                     "The members must be calibrated"],
         "answer": 1,
         "why": "Three models that fail on the same rows combine into one model that fails on those rows. Checking the correlation of their errors is the diagnostic to run first."},
    ],
)

CHECKS = {"machine_learning/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS}
