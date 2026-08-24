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
spanning roughly 20,000 to 70,000. They describe a person about equally well.

Set the scaler to None and look at the readout. The income range is around a
thousand times the age range. Now consider what k-NN does &mdash; it finds the
nearest points by Euclidean distance:

```
distance^2 = (age1 - age2)^2 + (income1 - income2)^2
```

A ten-year age difference contributes 100 to that sum. A ten-pound income
difference contributes 100 as well. A five-thousand-pound difference contributes
twenty-five million.

The age term is not merely less important. It is numerically irrelevant: any
plausible age difference is lost in the rounding of the income term. The model
is effectively one-dimensional, and nobody asked for that.

## What the scalers do

Switch to **StandardScaler**. Each column has its mean subtracted and is divided
by its standard deviation, so both end up centred on 0 with a spread of about 1.
The scatter becomes roughly circular, both columns contribute comparably, and
the accuracy in the readout moves.

```
z = (x - mean) / std
```

Switch to **MinMaxScaler**. Each column is mapped onto [0, 1] using its minimum
and maximum:

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
crushes every real salary into the bottom half of a per cent of the range.

## Which models care

**Sensitive**, because they measure distance or magnitude:

- k-NN and k-means &mdash; distance is the entire algorithm
- SVM with an RBF or polynomial kernel &mdash; the kernel is a distance
- PCA &mdash; it finds directions of maximum variance, and unscaled variance is
  dominated by whichever column has the biggest units
- Neural networks &mdash; not for correctness, but gradients on wildly different
  scales make optimisation slow and unstable
- Ridge and Lasso &mdash; the penalty is on coefficient size, and coefficient
  size depends on the units of its column

**Not sensitive:**

- Decision trees, random forests, gradient boosting

That last group surprises people, and the reason is worth having. A tree split
asks `is income > 45000`. Rescale the column and the question becomes
`is income' > 0.53`, which partitions the rows into exactly the same two groups.
Any monotonic transformation leaves every possible split unchanged, so the tree
is identical. Scaling before a random forest is not wrong; it is simply a
no-op.

## The rule that matters more than the choice

Fit the scaler on the **training data only**, then apply it to the test data
without refitting.

The mean and standard deviation are learned parameters. Computing them from the
whole dataset lets information about the test set reach the model before it is
evaluated, and the reported score stops being an estimate of anything. That is
[data leakage](data_leakage.html), it is the most common serious mistake in
applied machine learning, and it is why scalers belong inside a
[pipeline](ml_pipelines.html) rather than being applied by hand.

## Where it goes wrong

**Fitting the scaler on everything.** The number you report goes up and the
model does not get better.

**Scaling the target variable and forgetting to invert it.** Predictions come
back in scaled units and the error metric is meaningless.

**MinMax on data with outliers.** The real data ends up in a sliver of the
range.

**Scaling one-hot columns.** They are already 0 and 1. StandardScaler turns them
into two arbitrary values and makes the model harder to read for no gain.
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

Leakage is any route by which information about the data you are evaluating on
reaches the model before the evaluation. The model then answers a question it
was quietly shown the answer to, and the score you report measures nothing you
can act on.

It has no error message. Nothing crashes, nothing warns, and the only symptom is
that the number is better than you expected &mdash; which is not a symptom
anyone investigates.

## Watch it happen, on data with nothing in it

The dataset behind the chart is 300 rows and several hundred columns of pure
noise. The labels are assigned independently of every column. There is no signal
whatsoever, and the only honest score is 50%.

Set the control to **Once, on the whole dataset**. Five columns are picked by
correlating each one with the label across all 300 rows, and only then is the
data cross-validated. The reported accuracy is well above 50%, on data that
contains nothing.

Now set it to **Inside each fold**. The selection is redone within each fold's
training rows, and the reported accuracy falls back to chance &mdash; in fact
slightly below it, which is worth a sentence of its own further down.

Drag the number of columns up. The inflation grows: 40 candidate columns buy a
few points, 600 buy considerably more. With more columns to search there is
always some that correlate with the labels by chance, and the selection was
allowed to see the labels of the rows it was later tested on.

Nothing about the model changed between those two settings. The only difference
is whether the rows being scored had a say in which columns were used.

## Why the honest number lands below 50%

The correct setting reports something like 45%, not 50%, and that is not a bug
in the demonstration.

A column is chosen inside a fold because it happened to separate the classes in
those training rows. On pure noise that separation is entirely accidental, and
an accident large enough to win a search over hundreds of columns is an extreme
one. Extremes regress: on the held-out rows, that column is as likely to lean
the other way as this way, and the centroid built from the training rows then
points slightly the wrong direction.

So selecting features on noise does not merely fail to help. It can actively
mislead, and a model built on selected noise can score worse than one that
ignores the data entirely. That is worth knowing on its own, and it is the
strongest available argument for checking whether a feature-selection step is
earning its place.

## Why a scaler counts as a model

The instinct that makes this feel harmless is that scaling is "just
preprocessing". But `StandardScaler` has parameters &mdash; a mean and a
standard deviation &mdash; and it *learns* them from data. Anything that learns
parameters from data must learn them from training data only.

The same argument applies to every step that looks at the data as a whole:

- imputing missing values with a column mean
- selecting the top *k* features by correlation with the target
- fitting a PCA rotation
- learning target encodings for categorical columns
- computing TF-IDF weights
- resampling to balance classes

Every one of those is fitted, and every one leaks if fitted before the split.

They do not leak equally, and it is worth being straight about that. A scaler
fitted on a few hundred well-behaved rows leaks a real but tiny amount: the mean
barely moves when you add the validation rows to it, and the reported score may
shift by a fraction of a per cent. Feature selection leaks enormously, which is
why it is the demonstration above. The scaler case still matters, because a
fraction of a per cent is enough to change which of two models you ship, and
because the habit that prevents one prevents the other.

## The other kind

The second family has nothing to do with order of operations. It is a feature
that could not exist at prediction time.

A model predicting whether a customer will churn, trained on a table that
includes `cancellation_reason`. A model predicting loan default with a column
for `recovery_amount`. A medical model given a field that is only filled in once
a diagnosis has been made.

These are obvious when written out and very hard to spot in a warehouse table
with three hundred columns, most of them undocumented. The diagnostic question
is not "is this related to the target" but **"would this value be present, and
correct, at the moment I need a prediction?"**

A near-perfect score is the strongest evidence of leakage there is. If a model
reports 99% on a problem people find hard, the correct first response is
suspicion, not celebration.

## Leakage across time and groups

Two subtler cases are worth naming.

**Time.** A random split of time-series data puts future rows in the training
set and past rows in the test set, so the model is asked to predict backwards
after being shown what happened. Split by time, always.

**Groups.** If one patient contributes ten scans, a random split scatters them
across train and test. The model can recognise the patient rather than the
condition, and the score reflects that. Split by group.

## The fix

Put every fitted step inside a [pipeline](ml_pipelines.html) and cross-validate
the pipeline, not the model. Then each fold fits its own scaler, its own imputer
and its own feature selection on that fold's training portion, which is exactly
what you would have to do in production.

This is not a stylistic preference. It is the only arrangement in which the
order of operations cannot be got wrong by accident.

## Where it goes wrong

**Scaling or imputing before `train_test_split`.** The commonest form.

**Selecting features on the full dataset.** Produces plausible scores from noise.

**Random splits on time series or grouped data.**

**Believing a suspiciously good result.** It is nearly always leakage, and
finding out later is much more expensive than checking now.
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

Every tutorial answers "what do I do about NaN". The question that decides the
answer is **why the value is absent**, and there are three cases with three
different consequences.

**Missing completely at random.** The absence has nothing to do with anything.
A form field lost to a transmission error. This is the harmless case, and it is
rare.

**Missing at random.** The absence depends on other columns you have. Younger
respondents skip the income question more often, and you have their age. This is
recoverable, because the information needed to model the absence is present.

**Missing not at random.** The absence depends on the missing value itself.
High earners decline to state their income. This is the hard case, and it is
also the common one.

The data in the visualisation is deliberately the third kind: the largest values
are the ones that failed. Look at the two histograms. The grey distribution is
what existed; the orange one is what each strategy leaves you with.

## Drop the rows

Select **Drop**. The right tail is gone, and the mean in the readout has fallen
well below the true mean.

Nothing about dropping is wrong in principle. It is unbiased when the values are
missing completely at random, and with a handful of affected rows out of many it
is a perfectly reasonable choice.

Here it is a disaster, because the rows removed are not a random sample &mdash;
they are the large ones. Every statistic computed afterwards describes a
population that excludes them.

The other cost is arithmetic. Dropping any row with any missing value across ten
columns each 5% missing removes about 40% of the data, even though 95% of every
individual column is present.

## Fill with the mean, or the median

Select **Mean**, then **Median**. Both put a spike at a single value in the
middle of the distribution, and both leave the mean below the truth.

They differ in robustness. The mean is dragged by extreme values; the median is
not. For a skewed column &mdash; income, house prices, time-to-event &mdash; the
median is the better default, and for a roughly symmetric column the two are
close enough that it rarely matters.

What neither can do is invent information. Imputation makes the dataset
rectangular so the model will accept it. It does not restore what was lost, and
it introduces two distortions worth knowing:

- **Variance shrinks.** A pile of identical values has none.
- **Correlations weaken.** The imputed rows carry no relationship to any other
  column, so they dilute every relationship the column really had.

## Keep the fact that it was missing

Select **Median + indicator**. The imputation is the same; what changes is that
a second column is added, holding 1 where the value was missing and 0 otherwise.

This is usually the best simple answer, because in the third case &mdash;
missing not at random &mdash; **the absence is itself informative**. If high
earners decline to answer, then "declined to answer" predicts high earnings, and
plain imputation throws that signal away while an indicator preserves it.

It costs one column and no assumptions. It is hard to do worse than the
alternatives with it.

| Strategy | Keeps rows | Keeps distribution | Keeps the signal in absence |
|---|---|---|---|
| Drop | no | only if MCAR | no |
| Mean | yes | no, spike at centre | no |
| Median | yes | no, spike at centre | no |
| Median + indicator | yes | no | **yes** |
| Model-based (kNN, MICE) | yes | better | only with an indicator |

## More sophisticated options

**k-NN imputation** fills a value from similar rows. **MICE** models each column
from the others, iteratively. Both preserve relationships better than a constant
and both cost far more computation, and both must be fitted on training data
only &mdash; they are models, so imputing before the split is
[leakage](data_leakage.html).

Also worth knowing: some models handle missing values natively. LightGBM and
XGBoost learn a default direction at each split for rows whose value is absent,
which is frequently better than anything you would impute by hand.

## Where it goes wrong

**Imputing before the split.** The column mean is computed from the test rows
too.

**Filling with zero without thinking.** Zero is a real value in most columns. A
temperature of zero is not a missing temperature.

**Dropping rows across many columns at once.** A little missingness everywhere
removes a lot of data.

**Never checking why.** Ten minutes finding out what caused the gap is worth
more than any choice of strategy.
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
it; the solid line is the fit with it.

Drag the point straight up. The solid line rotates. Drag it to the far right and
up, and the line follows it much further. The readout reports both slopes and
the percentage difference between them, and it does not take much to change the
answer by tens of per cent.

Twenty-four rows are saying one thing. The twenty-fifth overrules them.

## Why squaring does this

Least squares chooses the line minimising the **sum of squared** residuals.
Squaring is what makes a single point so powerful: a point twice as far from the
line contributes four times the penalty, and one ten times as far contributes a
hundred times.

The fit is therefore willing to move a long way to reduce one large residual,
even at the cost of small increases across every other point. That is not a bug
in the implementation; it is what the objective function asks for.

## Leverage: where it sits matters as much as how far off it is

Drag the point up while keeping it near the middle of the x range, then drag it
up while keeping it at the far right. The second position moves the line much
more.

That difference is **leverage**. A regression line pivots roughly about the mean
of x, so a point near that mean is close to the pivot and has little turning
effect no matter how far off it is vertically. A point at the extreme of x sits
at the end of a long lever.

The distinction is worth having in three words:

- **Outlier** &mdash; unusual in y, a large residual.
- **High leverage** &mdash; unusual in x, far from the pivot.
- **Influential** &mdash; both, so removing it changes the model. This is the
  one that matters, and Cook's distance is the standard way to measure it.

A high-leverage point that happens to lie on the trend is harmless. A moderate
outlier in the middle is harmless. The combination is not.

## Before you remove anything

The temptation is to delete the point. Resist it long enough to ask which of
three things it is.

**An error.** A misplaced decimal, a sensor fault, a unit mix-up, a placeholder
like 999 or &minus;1 meaning "unknown". Fix it or remove it, and record that you
did.

**A different population.** The row is correct but does not belong to the
question &mdash; a wholesale order in a table of retail purchases. Exclude it and
say so, or model the groups separately.

**A real, extreme member of the population.** The row is correct and belongs.
This one you keep. Removing genuine extremes because they are inconvenient is
how a result stops describing the world, and it is much more common than
deliberate fraud.

If you cannot tell which, report the analysis both ways. A conclusion that
survives the point and a conclusion that depends on it are different findings,
and the reader is entitled to know which they have.

## Ways to be less fragile

**Robust loss.** Huber loss is squared for small residuals and linear for large
ones, so a distant point pulls hard but not quadratically hard. RANSAC fits on
random subsets and keeps the consensus.

**Quantile regression.** Models the median rather than the mean, and the median
does not move when one point is dragged to infinity.

**Winsorising.** Clip values at, say, the 1st and 99th percentiles. Keeps the
row, caps its influence.

**Use a model that does not care.** Trees split on order, not on distance, so
a value of a million and a value of a thousand are the same split if nothing
lies between them.

**Transform.** A log transform on a skewed positive column often turns
"outliers" into ordinary members of a normal-shaped distribution, which is
usually a sign the column was on the wrong scale.

## Where it goes wrong

**Deleting by rule.** "Beyond three standard deviations" uses the standard
deviation, which the outlier itself has already inflated.

**Treating placeholders as data.** 999 for unknown age, &minus;1 for missing.
These are not outliers; they are missing values wearing a number.

**Removing points until the model fits.** At that stage the model describes the
selection, not the phenomenon.

**Checking only y.** High-leverage points can be unremarkable in y and still
dominate the fit.
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
intro: Not a convenience wrapper. The arrangement in which the order of operations cannot be got wrong.

## The same demonstration, one level up

The chart is the one from the [leakage](data_leakage.html) module, relabelled:
300 rows of pure noise, five columns chosen by their correlation with the label,
and a choice about *when* that choice is made.

By hand, before cross-validation, the reported accuracy sits well above the 50%
the data deserves. Inside a pipeline, where every fold selects its own columns
from its own training rows, it falls to the truth.

The model is identical in both. What changed is which object owns the fitting,
and that is the entire argument for pipelines. It is not about tidiness.

## What goes wrong by hand

The by-hand workflow looks reasonable written out:

```
X = impute(X)
X = scale(X)
X = select_features(X, y)
scores = cross_val_score(model, X, y, cv=5)
```

Every one of those three steps has been fitted on all the data, and
`cross_val_score` then splits data that has already been contaminated. Each fold
was scaled using a mean that included its own validation rows, imputed using a
median that included them, and reduced to features chosen partly because they
correlated with their labels.

Nothing errors. The score is simply too high, by an amount that depends on the
data and cannot be estimated after the fact.

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
the scaler, then the feature selector, then the model &mdash; all on those rows
only. Scoring calls `transform` on the validation rows using the parameters just
learned.

The correct order is not something you remembered to do. It is the only thing
the object can do.

## The three other things it buys

**Hyperparameter search over preprocessing.** Because the steps are part of one
estimator, a grid can range over them:

```
{"impute__strategy": ["mean", "median"],
 "select__k": [10, 20, 40],
 "model__n_neighbors": [3, 5, 11]}
```

Whether the median beats the mean becomes a question the search answers, on the
same footing as the model's own parameters. Doing this by hand correctly is
possible and nobody does it.

**No train/serve gap.** The fitted pipeline is one object. Save it, load it in
the service, call `predict` on raw input. There is no second implementation of
the preprocessing to drift out of step with the first &mdash; which is a real
and common production failure, and a silent one.

**Different columns, different treatment.** `ColumnTransformer` routes numeric
columns to an imputer and scaler, categorical ones to a different imputer and a
one-hot encoder, and text to a vectoriser, then hands the combined result to the
model. That is what an actual table needs, and it stays one object.

## Cross-validation still needs care

A pipeline stops leakage between preprocessing and evaluation. It does not fix
splits that were wrong to begin with.

If rows are grouped &mdash; several scans per patient &mdash; use `GroupKFold`
so a patient cannot appear on both sides. If the data is a time series, use
`TimeSeriesSplit` so training always precedes validation. And if you tune
hyperparameters on the same folds you report, that number is optimistic too;
nested cross-validation is the honest version.

## Where it goes wrong

**Calling `fit` on the test data.** Use `transform`. `fit_transform` on the test
set refits everything and undoes the whole point.

**Steps that are not fitted.** A log transform has no parameters and cannot
leak, so it does not have to be in the pipeline &mdash; but putting it there
keeps the preprocessing in one place, which is worth more than the exemption.

**Resampling inside a plain pipeline.** SMOTE and friends must run on the
training fold only. `imblearn`'s pipeline handles this; scikit-learn's does not.

**Assuming a pipeline validates your splits.** It fits each fold correctly. It
cannot know that your folds mix one patient across both sides.
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
intro: Four counts in a table, three ratios drawn from them, and one slider that moves all of it.

## One model, many scores

A classifier does not output a class. It outputs a **score** &mdash; how
positive it thinks each case is &mdash; and a class only appears once you compare
that score against a threshold.

The histogram shows both distributions: actual negatives in grey, actual
positives in orange, overlapping in the middle because the model is good and not
perfect. The dashed line is the threshold.

Move it. Every number below the chart changes, and the model has not been
retrained. The scores are properties of the threshold as much as of the model,
which is the single most useful thing to understand here.

## The four counts

| | Predicted positive | Predicted negative |
|---|---|---|
| **Actually positive** | True positive | False negative |
| **Actually negative** | False positive | True negative |

Everything else is a ratio of these. The two that matter most divide by
different denominators, which is exactly why they disagree.

**Precision** = TP / (TP + FP) &mdash; of everything you flagged, what fraction
was right. The denominator is what *you* predicted, so precision is damaged by
false alarms.

**Recall** = TP / (TP + FN) &mdash; of everything that was actually there, what
fraction you caught. The denominator is what *reality* contained, so recall is
damaged by misses.

## Why they trade off

Drag the threshold to 0.10. Almost everything is flagged, so almost every real
positive is caught and recall approaches 100%. But the flagged set is now full of
negatives, and precision collapses.

Drag it to 0.90. Only the most confident cases are flagged, nearly all of them
correct, and precision approaches 100%. But most real positives are below the
line, and recall collapses.

You cannot maximise both by moving the threshold. The threshold only chooses
where on the trade-off you sit. Improving both at once requires a better model
&mdash; one whose two distributions overlap less.

## Which one you want depends on the cost

The question is never "which metric is best". It is **which mistake is more
expensive**.

**Recall matters more** when a miss is costly: screening for a serious disease,
detecting fraud, finding safety defects. A false alarm costs a second look. A
miss costs the thing you were trying to prevent.

**Precision matters more** when a false alarm is costly: flagging accounts for
suspension, recommending content, sending an alert that wakes someone. Missing
one is a shame. Being wrong repeatedly destroys trust in the system.

## F1, and why it is a harmonic mean

F1 combines them:

```
F1 = 2 * precision * recall / (precision + recall)
```

That is the harmonic mean, and the choice of mean is the point. Take precision
of 1.0 and recall of 0.01 &mdash; a model that flags exactly one case and gets
it right. The arithmetic mean is 0.505, which sounds respectable. F1 is 0.0198.

The harmonic mean is pulled toward the smaller number, so it stays low unless
both are high. That makes it hard to game with a degenerate model, which is
precisely what a single summary number needs to be.

F1 weights the two equally, which is a decision and often the wrong one. F-beta
lets you weight recall &beta; times as much as precision; F2 favours recall, F0.5
favours precision. If you have a reason to prefer one, use it.

## Why accuracy is on the readout and not in the headline

Accuracy is (TP + TN) / everything. It is the most intuitive metric and it is
close to useless when the classes are unbalanced.

If 1% of transactions are fraudulent, predicting "never fraud" scores 99%
accuracy while catching nothing at all. Precision and recall are both zero, which
is the honest description. [Imbalanced
data](precision_recall_vs_roc.html) is where this matters most.

## Where it goes wrong

**Reporting one number without the threshold.** "Precision 0.9" is
uninterpretable alone; at some threshold nearly every model achieves it.

**Optimising F1 when the costs are not equal.** F1 assumes they are.

**Comparing models at 0.5.** Two models can rank cases equally well and differ
only in calibration. Compare across thresholds, or tune each one.

**Accuracy on imbalanced data.** It measures the class balance more than the
model.
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
intro: Two curves over identical scores, and the reason one of them flatters a model that cannot be deployed.

## Start balanced

Leave the slider at 0.5. Half the rows are positive, and the two curves broadly
agree: ROC bows toward the top left, PR bows toward the top right, and both say
the model is decent.

Now drag the slider down toward 0.02, which is a realistic rate for fraud,
disease screening or ad clicks. Watch the two charts diverge.

**ROC barely moves.** The AUC in the readout stays high.

**PR collapses.** The precision that was achievable at any useful recall falls
away, and the best F1 falls with it.

The scores did not change. The model did not change. Only the proportion of
positives changed, and the two curves disagree about whether that matters.

## Why ROC does not notice

ROC plots true positive rate against false positive rate:

```
TPR = TP / (TP + FN)     denominator: all actual positives
FPR = FP / (FP + TN)     denominator: all actual negatives
```

Each is computed entirely within one class. TPR asks what fraction of positives
were caught; FPR asks what fraction of negatives were wrongly flagged. Adding a
million more negatives leaves TPR untouched and changes FPR only through its own
denominator, which grows in proportion.

That class-independence is often described as a virtue, and for some purposes it
is. It also means ROC cannot see the thing that makes rare-positive problems
hard.

## Why PR does notice

Precision is different:

```
precision = TP / (TP + FP)     denominator: everything you flagged
```

The denominator mixes both classes. When negatives outnumber positives a hundred
to one, even a small false positive *rate* produces a large *number* of false
positives, and those go straight into precision's denominator.

Concretely: 10,000 rows, 100 positive. A model at 90% recall and 5% FPR catches
90 real positives and flags 495 negatives. FPR of 5% sounds excellent and ROC
records it as such. Precision is 90 / 585 = **15%**. Five out of six flagged
cases are wrong, and every one costs somebody an investigation.

## Reading the baselines

Each chart has a dashed no-skill line, and they differ.

For **ROC** it is the diagonal, always. A random classifier gets AUC 0.5
regardless of balance.

For **PR** it is a horizontal line at the **positive rate**. At 50% positives,
random scores 0.5 precision. At 2%, random scores 0.02. Drag the slider and
watch it drop.

This is what makes PR honest and slightly harder to read: there is no fixed
scale. A PR AUC of 0.4 is poor on balanced data and outstanding at a 2% base
rate. The number must always be compared against the baseline, never quoted
alone.

## Which to use

| Situation | Curve | Reason |
|---|---|---|
| Roughly balanced | either | they broadly agree |
| Rare positives | **PR** | ROC hides the false-positive volume |
| You care about ranking overall | ROC | it is what AUC measures |
| Someone acts on each flag | **PR** | precision is that person's experience |
| Comparing across datasets | ROC, carefully | PR baselines differ by base rate |

The practical rule: if a human or a process has to act on every positive
prediction, precision is the thing they experience, and the PR curve is the one
to look at.

## Where it goes wrong

**Reporting ROC AUC alone on imbalanced data.** It is the standard way to make a
model that will drown a team in false positives look ready to ship.

**Comparing PR AUC across datasets with different base rates.** The baselines are
different, so the numbers are not comparable.

**Forgetting that both curves span all thresholds.** Neither tells you which
threshold to deploy &mdash; that is a separate decision, made with
[costs](threshold_tuning.html).
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
intro: Where 0.5 came from, why it is almost never right, and how to find the number that is.

## Where 0.5 comes from

It comes from the library. `predict()` calls `predict_proba()` and cuts at 0.5,
because a default has to be something and 0.5 is the least arbitrary-looking
choice available.

It is optimal under two assumptions that are rarely true together: the classes
are balanced, and the two kinds of mistake cost the same. Change either and 0.5
stops being the right cut.

## Put a price on each mistake

The two sliders set what a false negative and a false positive cost. The curve
is the **total cost** across every threshold, computed over 1,500 cases with 20%
positives. The grey line marks 0.5; the orange line marks the cheapest
threshold.

Start with a miss costing 20 and a false alarm costing 1 &mdash; a screening
problem, where investigating a healthy person is cheap and letting a sick one
through is not. The minimum sits well below 0.5. The model should flag
generously, because the flags are cheap and the misses are not.

Now reverse them: a miss at 1 and a false alarm at 50 &mdash; an automated
account suspension, where a wrong suspension is expensive and a missed offender
is dealt with later. The minimum moves above 0.5.

Set them equal and, with these class proportions, the minimum lands near 0.5 but
not exactly on it, because the balance is 20/80 rather than 50/50.

## The arithmetic

The expected cost of predicting positive on a case with predicted probability
*p* is `(1 - p) x cost_FP`. Predicting negative costs `p x cost_FN`. Flagging is
worth it when

```
(1 - p) * cost_FP  <  p * cost_FN
```

which rearranges to

```
p  >  cost_FP / (cost_FP + cost_FN)
```

With equal costs that is 0.5, which is where the default comes from. With a miss
ten times as expensive as a false alarm it is 1/11, about 0.09 &mdash; and a
default of 0.5 is then five times too strict.

That formula is worth carrying around. It gives a defensible starting threshold
from two numbers a domain expert can usually supply, without any tuning at all.

## When you cannot price the errors

Often nobody can put a number on a miss. Three usable fallbacks:

**Maximise F1**, or F-beta if one error matters more. This is the least
opinionated option and it is what most people do.

**Fix an operating constraint.** "The team can investigate 200 cases a day" sets
the threshold directly: take the top 200 scores. "Precision must be at least
80%" does the same from the other side. These are often more honest than a
metric, because they describe what will actually happen.

**Choose from the curve.** Plot precision and recall against threshold and pick
the point where the trade-off turns. It is a judgement, but an informed one.

## Two things that must be right

**Tune on validation data.** Choosing the threshold on the test set and then
reporting test performance is the same category of error as tuning
hyperparameters there &mdash; the reported number includes the choice you made
to maximise it.

**Do not confuse this with calibration.** Threshold tuning takes the scores as
given and picks a cut. Calibration changes the scores so that a score of 0.8
really means 80% of such cases are positive.

They are independent. A badly calibrated model can rank perfectly, and if the
ranking is right, a tuned threshold works fine. But if the threshold is being
derived from the cost formula above, the *p* in it must mean an actual
probability &mdash; and then calibration matters. Platt scaling and isotonic
regression are the usual tools.

## Where it goes wrong

**Reporting metrics at 0.5 and stopping.** The most common evaluation mistake
after using accuracy.

**Tuning on the test set.** Optimistic by exactly the amount you gained.

**Retuning per fold and averaging.** The thresholds are not comparable across
folds. Tune once on a held-out validation set.

**Forgetting it drifts.** The optimal threshold depends on the class balance,
and that moves in production. It needs rechecking, not setting once.
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

The background shading is the true score surface, and it is deliberately
lopsided. The horizontal axis is a hyperparameter that matters a great deal
&mdash; a learning rate, a regularisation strength &mdash; and the vertical axis
is one that barely does. The optimum is a narrow vertical band.

This lopsidedness is the normal case, not a contrived one. In most models one or
two hyperparameters dominate and the rest are close to noise, and you usually do
not know in advance which is which.

## Count the distinct values

Set the method to **Grid** with 16 trials. Sixteen points appear in a 4&times;4
lattice. Read the line under the chart: 16 trials, **4** distinct values of the
parameter that matters.

Every point in a column shares an x. The other three trials in that column tell
you nothing new about the axis you care about, because they only vary the axis
you do not.

Now switch to **Random**, same 16 trials. Sixteen points scattered, and
**16** distinct values of the parameter that matters. Same cost, four times the
resolution where resolution counts.

Push the budget to 64. Grid gives 8 distinct values from 64 trials; random gives
64. The gap widens as the budget grows, and it widens much faster as dimensions
are added &mdash; a grid over five parameters at four values each is 1,024
trials and still only four values of each.

## The argument in one line

A grid of *n* points per axis over *d* axes costs *n^d* trials and buys *n*
distinct values of each parameter. Random search of the same *n^d* trials buys
*n^d* distinct values of every parameter.

If only one axis matters, grid search has wasted all but *n* of its trials on
that axis. This is Bergstra and Bengio's 2012 result, and it changed default
practice.

## Watch the luck

Move the **seed** slider with random selected. The best point found moves, and
the best score wobbles. Random search is random; a single run can be unlucky.

That is a real cost and a smaller one than it looks. Because the surface is
broad along the unimportant axis, most draws land somewhere reasonable, and the
distribution of outcomes is much better than grid's guaranteed coarseness. But
it does mean a single random run is not a strong claim, and comparisons should
allow for the variation.

## When grid search is still right

**Few parameters, genuinely discrete.** Three kernels, four values of *k*: a
grid is exhaustive and the exhaustiveness is worth having.

**Reproducibility matters more than efficiency.** A grid is deterministic and
easy to describe in a paper.

**You are refining.** Random search to find the region, a small grid to comb it.
This combination is better than either alone.

## What replaced both

**Bayesian optimisation** builds a model of the score surface from the trials so
far and proposes the point most likely to improve. Optuna and Hyperopt do this,
and on expensive objectives &mdash; where one trial takes an hour &mdash; it is
clearly better than either method here.

**Successive halving** and **Hyperband** attack the cost differently: start many
configurations cheaply, kill the worst, give the survivors more budget. When a
trial's early performance predicts its final performance, this is dramatically
more efficient.

For anything cheap, random search remains an excellent default. It has no
hyperparameters of its own, it parallelises perfectly, and it is very hard to
use wrongly.

## Where it goes wrong

**Sampling scale.** A learning rate should be sampled log-uniformly. Uniform
between 0.0001 and 0.1 puts 90% of the draws above 0.01.

**Tuning on the test set.** Same error as everywhere else. Tune on validation.

**Searching a range that excludes the answer.** No search finds what is outside
its bounds. Check whether the best value sits at the edge of the range; if it
does, widen it and search again.

**Not searching preprocessing.** Put the whole [pipeline](ml_pipelines.html) in
the search, so imputation and scaling choices are tuned alongside the model.
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
intro: The plot that answers whether to collect more data, and saves you from collecting it pointlessly.

## What is plotted

Train the model on 40 examples, record the error on those examples and on a
held-out validation set. Repeat with 80, 120, and so on. Plot both against
training-set size.

Grey is training error, orange is validation error. The **shape** of the pair is
the diagnosis, and the diagnosis is more useful than either number alone.

## Underfitting

Set capacity to 1 or 2. Both curves rise quickly to a plateau, sit close
together, and stay high.

Training error is high, which is the tell. The model cannot fit the data it has
already seen, so nothing about unseen data is the problem. This is **bias**: the
model is too simple for the structure present.

The important consequence is negative. **More data will not help.** The curves
have already converged; adding examples moves neither. Money spent on collection
here is wasted, and this plot is the cheapest way to find that out before
spending it.

What helps instead: more capacity, better features, less regularisation, a
different model class.

## Overfitting

Set capacity to 8 or 9. Training error drops close to zero, validation error
stays well above it, and a wide gap opens between them.

The model fits its training data nearly perfectly and generalises poorly. This is
**variance**: capacity is being spent memorising noise.

Here more data *does* help, and the curve says so &mdash; the validation line is
still falling at the right-hand edge. Every additional example makes the noise
harder to memorise. Other options: reduce capacity, add regularisation,
augment the data, or ensemble.

## About right

Set capacity to 4 or 5. The curves converge to a small gap at a low error, and
both have flattened.

The readout says as much. There is no obvious bias and no obvious variance, and
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

That last row is worth keeping. High training error *and* a large gap should not
happen from bias or variance alone, and usually means a bug &mdash; leakage in
reverse, mislabelled data, or a validation set drawn from a different
distribution.

## Where the curve is still falling

The single most valuable thing here is being able to answer "will more data
help" with evidence.

If the validation curve is still descending at your current dataset size,
collecting more will improve the model, and the slope gives a rough sense of how
much. If it has been flat for the last few points, more data buys nothing, and
the effort belongs elsewhere.

That question is otherwise answered by intuition, and it usually involves real
money.

## Practical notes

The curves are noisy at small sizes, because a model trained on 40 examples
depends heavily on which 40. Average over several splits, and plot the spread if
you can.

Use the same validation set at every size. Growing it alongside the training set
confounds two changes.

And do not confuse this with a **validation curve**, which plots error against a
hyperparameter at fixed data size. Both are useful and they answer different
questions: learning curves ask about data, validation curves ask about a setting.

## Where it goes wrong

**Reading a single run.** Small-sample noise looks like structure.

**Plotting accuracy on imbalanced data.** The curves will be flat and
uninformative. Plot the metric you actually care about.

**Concluding 'more data' from a gap alone.** Check the validation curve is still
falling. A converged gap means variance you cannot fix with volume.
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
             "min": 0.10, "max": 0.60, "step": 0.01, "value": 0.22},
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
intro: Clustering by crowding rather than by distance to a centre, and the two parameters that decide everything.

## What k-means cannot do

Set the data control above to **Two crescents**. K-means, which assigns each
point to the nearest of *k* centres, cannot separate these: the boundary it
draws is always a straight line between two centroids, and no straight line
separates two interleaved crescents.

DBSCAN separates them immediately, and does it without being told there are two.

## The definitions

Everything follows from two parameters &mdash; `eps`, a radius, and `minPts`, a
count &mdash; and three definitions:

**Core point.** Has at least `minPts` points within `eps` of it, including
itself. It sits in a crowded place.

**Border point.** Within `eps` of a core point, but not crowded enough to be one
itself. It is on the edge of a cluster.

**Noise.** Neither. It belongs to no cluster, and DBSCAN says so rather than
forcing it somewhere.

A cluster is then a maximal set of points connected through core points. Start at
a core point, take everything within `eps`, and for each of those that is also a
core point, take *its* neighbourhood too, repeating until nothing new arrives.

This is why clusters can be any shape. The cluster spreads wherever the data is
dense, following the crescent around its curve, because at no point does it ask
how far anything is from a centre.

## The two parameters

Drag `eps` in the visualisation and watch the count.

**Too small**, and no point has `minPts` neighbours. Everything is noise, or the
data shatters into many small clusters.

**Too large**, and everything is within reach of everything else. The two
crescents merge into one cluster, which happens above about 0.26 on this data.

The band in between is where DBSCAN works, and on the crescents it is genuinely
narrow. That sensitivity is the honest weakness of the method.

`minPts` is less delicate. Larger values demand denser cores, producing fewer,
tighter clusters and more noise. A common starting rule is `minPts = 2 * number
of dimensions`, and at least 3.

For `eps`, the standard technique is a **k-distance plot**: for every point,
measure the distance to its `minPts`-th nearest neighbour, sort those distances
and plot them. The curve has a knee where distances start rising sharply, and
that knee is a reasonable `eps` &mdash; it is the point at which you leave the
dense region and start crossing gaps.

## What it gives you that k-means does not

**No k.** The number of clusters is discovered, not supplied.

**Arbitrary shapes.** Crescents, rings, spirals, anything connected and dense.

**An explicit noise label.** K-means assigns every point to some cluster, so an
outlier is silently absorbed and drags a centroid with it. DBSCAN sets it aside.
Switch the data to blobs and the scattered points stay hollow.

## Where it fails

**Varying density.** This is the real limitation. One `eps` applies everywhere,
so a dataset with one dense cluster and one sparse cluster cannot be handled: the
`eps` that finds the sparse one merges the dense one into its surroundings.
**HDBSCAN** exists precisely for this, building a hierarchy over `eps` values and
selecting per cluster.

**High dimensions.** Distances concentrate as dimensionality grows, so
"neighbourhood" stops meaning much. Reduce dimensions first.

**Scale sensitivity.** `eps` is an absolute distance, so a feature measured in
thousands dominates one measured in units. [Scale
first](feature_scaling.html) &mdash; this is not optional.

**Cost.** Naively O(n&sup2;) because of the neighbourhood queries. A spatial
index brings it to about O(n log n) in low dimensions.

## Where it goes wrong

**Not scaling the features.** `eps` becomes meaningless.

**Tuning eps by trying numbers.** Use a k-distance plot; it takes a minute and
gives a defensible value.

**Expecting it to work on varying density.** Reach for HDBSCAN instead.

**Reading noise as failure.** Labelling outliers as noise is the feature.
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
intro: Building the whole tree once, and choosing how many clusters you want after seeing it.

## The algorithm

Agglomerative clustering is almost trivially simple:

1. Every point starts as its own cluster.
2. Find the two closest clusters and merge them.
3. Repeat until one cluster remains.

Recording the distance at each merge gives a **dendrogram** &mdash; the chart
above plots exactly that: merge number against the distance at which it
happened.

## The point: k comes last

K-means and DBSCAN both need a decision before they run &mdash; how many
clusters, or how dense. Hierarchical clustering needs neither. It builds one
tree, and a horizontal cut through it produces a clustering.

Drag the cut height and watch the count change. A cut low down leaves many small
clusters, a cut high up leaves few, and the tree itself never changed. That is
genuinely useful when you do not know what structure to expect, because you can
look at the merge distances before committing.

Large jumps in the curve are informative: a merge that costs much more than the
one before it joined two things that were not really close. Cutting just below a
big jump is the dendrogram equivalent of the [elbow](choosing_k.html).

## Linkage changes everything

The algorithm needs a distance between two *clusters*, not two points, and there
is no single right answer. Switch the control and the shape of the curve changes
substantially.

**Single linkage** &mdash; distance between the nearest pair. Merges cheaply
whenever any two members are close, so it can follow elongated shapes. Its
failure mode is **chaining**: two well-separated blobs joined by a thin bridge of
points merge into one, because the bridge provides a short hop at every step.

**Complete linkage** &mdash; distance between the furthest pair. A merge is only
cheap if *every* member of one cluster is close to every member of the other, so
clusters come out compact and roughly equal in diameter. It breaks up elongated
structures that genuinely belong together, and is sensitive to outliers, since
one distant member sets the whole distance.

**Average linkage** &mdash; the mean over all cross-pairs. Between the two, and
the usual default.

**Ward linkage**, not offered here, merges the pair that increases within-cluster
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

**Height is meaningful; horizontal position is not.** The left-to-right order is
chosen to keep the drawing untangled and carries no information. Two adjacent
leaves are not necessarily similar.

**The tree is greedy and permanent.** Once two clusters merge they never
separate, so an early mistake &mdash; two points joined because of noise &mdash;
propagates all the way up. Hierarchical clustering does not revisit decisions.

## Cost

The naive algorithm is O(n&sup3;), and careful implementations reach O(n&sup2;
log n) with O(n&sup2;) memory for the distance matrix. That memory is usually the
binding constraint: 100,000 points is a matrix of ten billion distances.

This is why hierarchical clustering is a small-to-medium-data method. Above a few
tens of thousands of points, k-means or a sampled variant is the practical
choice.

## Where it goes wrong

**Not scaling the features.** As with every distance-based method.

**Using single linkage on data with any bridge between clusters.** Chaining will
merge them.

**Reading meaning into leaf order.** It is a drawing convention.

**Trying it on a large dataset.** The distance matrix will not fit.
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
intro: Two ways of picking the number of clusters, what each actually measures, and why they disagree.

## Why inertia cannot answer the question

**Inertia** is the sum of squared distances from every point to the centroid of
its cluster. K-means minimises it directly, so it is the obvious thing to look at.

It is also useless on its own, and the reason is structural: inertia falls at
every increase in k, always. With k equal to the number of points, every point is
its own centroid and inertia is exactly zero. Watch the left chart as the spread
control moves &mdash; the curve descends monotonically no matter what the data
looks like.

So "choose the k with the lowest inertia" always answers "as many as possible".
The metric measures how tightly points sit around their centres, not whether the
grouping is any good.

## The elbow

The elbow method looks for the k where the curve stops falling steeply &mdash;
where extra clusters stop buying much. On well-separated blobs there is a genuine
bend at the true number, because up to that point each new cluster splits a real
group, and after it each new cluster splits a group that was already coherent.

The problems are practical. The bend is judged by eye and different people pick
different points. Very often, on real data, there simply is no bend &mdash; the
curve is smooth, and reading an elbow into it is wishful. Raise the spread
control until the blobs overlap and the bend disappears in front of you.

There is a formalisation, the **kneedle** algorithm, which finds the point of
maximum curvature. It is better than eyeballing, and it still assumes a knee
exists.

## The silhouette

The silhouette measures something different: not tightness, but **separation
relative to tightness**.

For each point, let *a* be its mean distance to the other members of its own
cluster, and *b* its mean distance to the members of the nearest other cluster.
The silhouette is:

```
s = (b - a) / max(a, b)
```

Near **+1** the point is much closer to its own cluster than to any other. Near
**0** it sits on a boundary. **Negative** means it is closer to a different
cluster than to its own &mdash; it is probably misassigned.

Averaging over all points gives one number per k, and unlike inertia it does not
improve automatically as k grows. Adding clusters eventually forces points close
to a neighbouring cluster, which drives *b* down and the score with it. So the
silhouette has a real maximum, and that maximum is a defensible choice.

The right-hand chart shows this. The peak is at the true number of blobs, and it
is a peak rather than a slope.

The cost is computation: it needs pairwise distances, so O(n&sup2;), against
inertia's O(n).

## When they disagree

They frequently do, and the disagreement is informative rather than a problem to
resolve.

Inertia asks *are the clusters tight*. The silhouette asks *are they separated*.
A dataset can have tight clusters that sit right next to each other, and the two
metrics will point in different directions.

Switch the data to **Two crescents** and watch both. The silhouette does not
recover the two crescents either &mdash; because it is still built on distances
to cluster members, and k-means has not produced the crescents in the first
place. That is the honest limit of both metrics: they evaluate the clustering
you gave them, and cannot tell you the algorithm was wrong.

## The answer that is usually right

Neither metric knows what the clusters are for.

If you are segmenting customers so a marketing team can write one message per
segment, k is roughly how many messages they can write. If you are compressing
colours, k is the palette size you can afford. If clusters feed a downstream
model, the number that makes that model best is the number.

Both metrics are worth computing, and the application usually decides.

## Where it goes wrong

**Choosing k by inertia alone.** It will always say "more".

**Seeing an elbow in a smooth curve.** Check whether the bend survives a change
of scale on the axis.

**Trusting a silhouette on non-spherical clusters.** It is distance-based and
inherits the same assumption k-means makes.

**Forgetting to scale.** Both metrics are distances.
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

K-means gives every point exactly one cluster. For a point sitting squarely
inside a group that is fine. For a point in the overlap between two groups it is
a fabrication: the algorithm had almost no reason to prefer one over the other,
and the output records none of that doubt.

A Gaussian mixture keeps the doubt. It models the data as having come from
several Gaussian distributions mixed together, and reports, for each point, the
probability that it came from each one.

Raise the overlap control above and watch the readout. As the two groups merge,
the number of points assigned with less than 90% confidence climbs &mdash; and
every one of those is a point k-means would have labelled without hesitation.

## The model

Three parameters per component: a mean, a width, and a **mixing weight** saying
what fraction of the data that component accounts for. The density is their
weighted sum, and the two curves in the chart are the fitted components.

Fitting is a chicken-and-egg problem. Knowing which points belong to which
component would make estimating the parameters easy, and knowing the parameters
would make assigning points easy. Neither is known.

## Expectation-Maximisation

EM resolves it by alternating, starting from a guess:

**E step.** With the current parameters, compute each point's
**responsibility** &mdash; the probability that each component produced it.

**M step.** With those responsibilities, re-estimate each component's mean, width
and weight, weighting every point by how much it belongs.

Repeat. Each iteration provably does not decrease the likelihood, so the process
converges.

Drag the iterations control from 1 upward and watch the curves settle. The early
steps move a great deal; the last twenty barely move at all, which is what
convergence looks like.

The guarantee is only about *local* optima. EM converges to a local maximum that
depends on the starting point, which is why implementations run it several times
from different initialisations and keep the best. Scikit-learn's `n_init` exists
for this.

## Why it beats k-means, when it does

**Elliptical clusters.** With a full covariance matrix per component, a GMM fits
stretched and tilted clusters. K-means implicitly assumes spheres, so an
elongated cluster gets cut in half.

**Different sizes.** Mixing weights let one component account for 80% of the data
and another for 20%. K-means has no such notion and tends toward equal-sized
clusters.

**Soft assignment.** Useful in itself when the output feeds something downstream
that can use a probability.

**A likelihood.** Being a proper probabilistic model, a GMM can score how well it
explains the data, which makes **BIC** and **AIC** available for choosing the
number of components &mdash; a principled alternative to
[the elbow](choosing_k.html).

K-means is exactly the limiting case: spherical components of equal weight, with
responsibilities forced to 0 or 1.

## Where it goes wrong

**Assuming Gaussian.** If the clusters are crescents, a mixture of Gaussians is
the wrong model, and it will fit two Gaussians to them anyway.

**Singularities.** A component can collapse onto a single point, driving its
width to zero and the likelihood to infinity. Regularisation &mdash; a small
constant added to the covariance &mdash; prevents it, and is on by default in
most libraries.

**One run from one start.** Local optima are real. Use several initialisations.

**Too many components.** With enough Gaussians you can fit anything, including
the noise. BIC penalises parameter count for this reason.
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
intro: Why neighbour-preserving plots look so much better than PCA, and which parts of them you are not allowed to read.

## A note on what this page runs

The layout here is a **simplified neighbour-preserving optimisation** &mdash;
attract each point toward its nearest neighbours in the original space, repel
everything else. It is not t-SNE: there is no perplexity, no
Student-t kernel, no KL divergence being minimised.

What it reproduces faithfully is the behaviour that matters: local structure is
preserved, and the distances between groups stop meaning anything. The
[PCA module](pca.html) covers the linear method properly.

## Two different jobs

**PCA** finds the directions along which the data varies most and projects onto
them. It is linear, deterministic, invertible, and fast &mdash; and because it is
a projection, distances survive it in a predictable way. Points far apart in the
original space are far apart in the plot, up to the variance the discarded
dimensions held.

**t-SNE and UMAP** do something else entirely. They ask which points are near
each other in the original space, and then *construct* a two-dimensional
arrangement in which those same points are near each other. There is no
projection and no formula mapping one space to the other &mdash; the coordinates
are the output of an optimisation.

## What the readout is checking

The data behind this page has three clusters arranged on a line, with the third
exactly twice as far from the first as the second is. A ratio of 2.00, by
construction.

Switch between the methods and watch the measured ratio.

**PCA** reproduces it closely. It is a linear projection, so the global
arrangement is preserved.

**The neighbour-preserving layout** does not, and the number wanders as you
change the attraction strength. The three groups are cleanly separated &mdash;
visibly better than PCA &mdash; and the distances between them are an artefact of
the optimisation.

That is the whole lesson, and it is the thing most often got wrong when reading
these plots.

## What you may not read from a t-SNE plot

**Distance between clusters.** Two clusters at opposite ends may be more similar
than two that are adjacent. The layout only tried to keep neighbours together.

**Cluster size.** t-SNE expands dense regions and contracts sparse ones, so the
area a cluster occupies says nothing about how many points it has or how spread
out they were.

**Density within a cluster.** Same reason.

**Anything from one run.** t-SNE is stochastic and its result depends on the
random seed and on perplexity. Run it three times and you get three pictures.
Structure that survives all three is real; structure that does not, is not.

## Perplexity and n_neighbors

Both algorithms have a parameter controlling how much neighbourhood to consider
&mdash; **perplexity** in t-SNE, **n_neighbors** in UMAP. Low values emphasise
very local structure and can shatter a genuine cluster into fragments. High
values emphasise broader structure and can merge distinct clusters.

There is no correct value, and the standard advice is to look at several. A
finding that only appears at one setting is a finding about the parameter.

## t-SNE against UMAP

**Speed.** UMAP is substantially faster and scales to larger datasets.

**Global structure.** UMAP claims to preserve more of it, and generally does,
though the caution above still applies &mdash; less meaningless is not
meaningful.

**New points.** UMAP can transform data it did not see during fitting. t-SNE
cannot: adding a point means re-running everything. This matters if the embedding
is part of a pipeline rather than a picture.

**Reproducibility.** Both are stochastic; both take a seed.

## What they are for

Looking. These are visualisation tools, and they are very good at answering "does
my data separate at all", "are my labels consistent", "is there a group I did not
expect".

They are a poor choice as a preprocessing step for a model. The output
coordinates have no meaning outside the plot, the mapping is not stable, and for
t-SNE it cannot be applied to new data at all. If you want dimensionality
reduction inside a pipeline, PCA is the safe default.

## Where it goes wrong

**Measuring distance between clusters.** The single most common error.

**Reading cluster sizes.** Artefacts of the optimisation.

**Running once and believing it.** Vary the seed and the perplexity.

**Feeding t-SNE coordinates into a classifier.** No stable mapping; no way to
transform new data.
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
intro: The most useful model-agnostic importance measure, and the specific way it lies to you.

## The idea

If a feature matters, destroying the information in it should hurt the model. So:

1. Score the model on a dataset.
2. Shuffle one column, breaking its relationship with the target while leaving
   its distribution untouched.
3. Score again.
4. The drop is that feature's importance.
5. Repeat for every column.

Shuffling rather than deleting is the important detail. Deleting a column means
retraining, which gives a different model and answers a different question.
Shuffling keeps the same fitted model and the same input shape, so the only thing
that changed is whether that column carries signal.

Because it needs nothing but predictions, it works on any model at all &mdash;
linear, forest, gradient-boosted, neural network.

## Reading the chart

Four features are fed to a logistic model: a strong signal, a weak one, pure
noise, and a **near-duplicate copy of the strong signal**.

`noise` scores about zero, which is correct and reassuring.

Now compare `signal` with `copy of signal`. They carry the same information
&mdash; either would serve the model about equally well on its own &mdash; and
`copy of signal` scores roughly half what `signal` does, landing at about the
level of `weak`, a feature that is genuinely much less informative.

## Why: correlated features hide each other

The reason is exactly the procedure. The model here is a small random forest,
and each split considers a random subset of the features, so some trees split on
`signal` and others on its copy. Shuffling the copy leaves all the trees that
used `signal` working perfectly, so the measured drop is much smaller than the
column's actual worth.

The metric is measured **one column at a time**, and with correlated features
that is the wrong unit of analysis. The honest reading is not "the copy does not
matter" but "either one largely substitutes for the other, and this method cannot
say that".

The size of the effect depends on the model. A linear model given two duplicate
columns splits its weight between them, so shuffling one still destroys half the
contribution and both score moderately high. A forest can substitute one for the
other outright, which is why the discount is so visible here &mdash; and why the
trap is worst on exactly the tree models where importance charts are most often
drawn.

This is the single most important thing to know about permutation importance,
because the failure is silent and the chart looks perfectly reasonable.

What to do about it:

**Cluster correlated features first** and permute whole groups together. The
group's importance is then meaningful even though its members' are not.

**Check the correlation matrix** before reading any importance chart.

**Use conditional permutation**, which shuffles within strata of the correlated
features rather than globally.

## Held-out data, not training data

Permutation importance computed on the training set measures what the model
*used to fit*, including what it memorised. A feature the model overfitted to
will look highly important because shuffling it destroys memorised training
performance.

On held-out data the same procedure measures what the feature contributes to
performance that generalises. That is almost always the question, and it is why
scikit-learn's documentation is emphatic about it.

Comparing the two is diagnostic in itself: a feature that is very important on
training data and unimportant on validation data is one the model overfitted.

## Against a tree's built-in importance

Random forests and gradient-boosted trees expose `feature_importances_`, usually
mean decrease in impurity. It is free, since it is accumulated during training,
and it has a known bias: it **favours high-cardinality features**. A column with
many distinct values offers more possible split points, so it is chosen more
often and accumulates more credit &mdash; even a random ID column will score
above a useful binary flag.

Permutation importance does not have that bias, costs a re-scoring pass per
feature, and applies to models that have no built-in measure at all.

## Repeats

Shuffling is random, so a single shuffle is a noisy estimate. The repeats control
above averages several, and the wobble as you change the seed at one repeat
shrinks visibly as you raise it. Five to ten is typical.

## Where it goes wrong

**Reading it on correlated features.** The central trap.

**Computing it on training data.** Measures memorisation.

**Treating it as causal.** It says the model used a feature, not that the feature
causes the outcome.

**Comparing across models.** Importance is relative to one fitted model. A
different model can rank the same features differently and both be right about
themselves.
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
intro: Three ways to ask what a model is doing, and the trap in the most popular one.

## Partial dependence

A partial dependence plot answers: as this feature moves across its range, what
happens to the prediction on average?

The procedure is mechanical. Take the dataset. Set the feature to some value for
*every* row, leaving all other columns untouched. Predict, and average. Repeat
across the feature's range, and plot.

It is model-agnostic and easy to read, which is why it is everywhere.

## The trap

Leave the interaction control **on** and look at the thick line. It is nearly
flat, and the readout gives its slope as close to zero. Read on its own, it says
this feature does not matter.

Now the ICE curves underneath tell a completely different story. Every individual
curve has a steep slope &mdash; the feature matters enormously to every single
row. It is just that it slopes **up** for one group and **down** for the other,
and averaging them cancels.

This is not a contrived case. Any feature whose effect reverses by subgroup
behaves like this: a treatment that helps one population and harms another, a
price change that attracts some customers and repels others.

**A flat partial dependence curve does not mean the feature is unimportant.** It
means the average effect is zero, which is a much weaker statement.

Switch the interaction off and the curves stack into a single shape. Now the
average describes each individual well, and the partial dependence line is
trustworthy.

## ICE curves

**Individual Conditional Expectation** curves are partial dependence without the
averaging: one line per row, showing what the model predicts for *that* row as
the feature sweeps.

They cost nothing extra, since partial dependence computes them and then throws
them away. Plotting them is the standard defence against the trap above, and the
diagnostic is simple: if the ICE curves are parallel, the partial dependence line
is a fair summary. If they fan out or cross, it is not, and there is an
interaction worth finding.

## The other assumption

Partial dependence sets a feature to a value for every row regardless of whether
that combination is possible. Sweeping `age` from 18 to 80 across a dataset
creates rows with age 18 and forty years of work experience.

The model is asked to predict for combinations that never occur, and its answer
there is extrapolation with nothing to anchor it. When features are strongly
correlated, part of a partial dependence curve is describing regions of input
space the model has never seen.

**Accumulated Local Effects** plots address this by only varying a feature within
the range of values that actually co-occur with the other features' values.

## SHAP

SHAP answers a different question. Partial dependence and ICE describe the model
across a range; SHAP explains **one prediction**.

For a given row, it assigns each feature a number saying how much that feature
pushed the prediction away from the base value &mdash; the average prediction
over the dataset. The numbers sum exactly to the difference:

```
prediction  =  base value  +  sum of every feature's SHAP value
```

That additivity is what makes it useful for an individual explanation: it
accounts for the whole prediction, with nothing unattributed.

The values come from Shapley values in cooperative game theory, which distribute
credit for a joint outcome fairly among contributors. Computing them exactly
requires evaluating every subset of features, which is exponential, so
implementations approximate &mdash; `TreeSHAP` exactly and quickly for trees,
`KernelSHAP` by sampling for anything else.

| | Answers | Scope |
|---|---|---|
| Partial dependence | how the prediction moves with a feature, on average | global |
| ICE | the same, per row | per row |
| SHAP | how much each feature contributed here | one prediction |
| [Permutation importance](permutation_importance.html) | how much accuracy depends on a feature | global |

## Where it goes wrong

**Reading a flat PD curve as "unimportant".** Plot the ICE curves.

**Ignoring correlated features.** Part of the curve may be extrapolation.

**Treating SHAP as causal.** It attributes a prediction, not an outcome. A model
that uses postcode as a proxy for income will show postcode contributing, and
that is a fact about the model.

**Averaging SHAP values into a global importance and stopping there.** The mean
absolute SHAP value is a reasonable global summary, and it discards the direction
and the interactions that made SHAP worth computing.
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
intro: Whether a model's confidence means anything, and why every ranking metric is blind to it.

## Two different questions

**Discrimination** asks whether the model ranks positives above negatives. AUC
and [ROC](precision_recall_vs_roc.html) measure this.

**Calibration** asks whether the numbers mean what they say. Of all the cases
where the model said 0.8, were about 80% actually positive?

A model can be excellent at one and terrible at the other, and this is not an
edge case &mdash; it is the normal situation.

## The slider proves it

Drag the temperature control and watch the curve deform. That control performs
**temperature scaling**: it divides the logit by a constant before the sigmoid.
Dividing by a number less than one sharpens every score toward 0 or 1; dividing
by a number greater than one flattens them toward 0.5.

Crucially, this is a **monotonic** transformation. It never changes the order of
any two predictions. Every ranking metric &mdash; AUC, average precision,
anything based on ordering &mdash; is **identical at every setting of that
slider**, while the reliability curve swings from badly over-confident to badly
under-confident.

Which is the point. If you only ever look at AUC, you have no information about
calibration at all.

## Reading the diagram

Predictions are binned by confidence, and each bin plots mean confidence against
observed frequency.

**On the diagonal**: calibrated.

**Below the diagonal**: over-confident. The model says 0.9 and is right 70% of
the time. This is the common failure, and the damaging one.

**Above the diagonal**: under-confident. The model hedges when it should not.

**ECE** &mdash; expected calibration error &mdash; is the average vertical
distance, weighted by how many points fall in each bin. It is the number in the
readout, and it is a summary that can hide compensating errors: a curve that is
above the diagonal in one region and below in another can report a small ECE.
Look at the curve, not only the number.

## Why models come out miscalibrated

**Modern neural networks are over-confident**, and increasingly so as they get
larger. Training to minimise cross-entropy on data it can fit perfectly pushes
outputs toward 0 and 1 long after the accuracy has stopped improving.

**Support vector machines** produce distances from a hyperplane, not
probabilities, and passing them through a sigmoid does not make them
probabilities.

**Naive Bayes** is famously over-confident because its independence assumption
multiplies correlated evidence as though it were independent.

**Random forests** tend to be under-confident at the extremes, because averaging
many trees pulls predictions toward the middle.

Logistic regression, fitted on well-specified features, is usually close to
calibrated &mdash; it optimises exactly this.

## Fixing it

All three methods fit a correction on a **held-out** set, never on the training
data.

**Platt scaling.** Fit a logistic regression to map scores to probabilities. One
or two parameters, works on small validation sets, assumes the distortion is
sigmoid-shaped.

**Temperature scaling.** The single-parameter version, and the standard for
neural networks. Because it changes no rankings, accuracy and AUC are guaranteed
untouched &mdash; a rare free lunch.

**Isotonic regression.** Fits any monotonic mapping. More flexible, and needs
considerably more data or it overfits the validation set.

## When it matters

**Whenever a probability feeds a decision with costs.** Expected value is
probability times payoff, so a wrong probability is a wrong decision even when
the ranking is perfect.

**Medical and risk contexts**, where "30% chance" is communicated to a person.

**When scores are combined** across models or over time.

**When a threshold is set from a target rate.** [Choosing a
threshold](threshold_tuning.html) from calibrated probabilities gives the rate
you asked for; from uncalibrated scores it does not.

If all you do is rank &mdash; show the top 100 results &mdash; calibration is
irrelevant.

## Where it goes wrong

**Calibrating on the training set.** It will look perfect and generalise
nothing.

**Isotonic regression on a small validation set.** It overfits.

**Assuming a good AUC implies good probabilities.** The slider on this page
exists to disprove exactly that.

**Recalibrating without re-checking after data drift.** A calibration fitted last
year describes last year's distribution.
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
intro: Anomaly detection that looks for what is easy to cut off, rather than modelling what is normal.

## Inverting the usual approach

Most anomaly detection builds a model of normal &mdash; fit a distribution,
estimate a density, learn a boundary &mdash; and flags whatever falls outside.
That is hard work, and in high dimensions density estimation is very hard work.

Isolation Forest asks a different question: **how much effort does it take to
separate this point from everything else?**

Pick a random feature, pick a random split value between its minimum and maximum,
and divide the data. Repeat on each half until every point sits alone.

A point far from the rest gets cut off almost immediately &mdash; a single random
split has a good chance of landing between it and the crowd. A point in the
middle of a dense cluster survives many splits, because every cut has to be
placed among tightly packed neighbours.

**Path length is the anomaly measure**, and no model of normality was ever built.

## The score

The raw quantity is the average path length across the forest. It is normalised
against the expected path length in a random binary tree of the same size,
because deeper trees naturally have longer paths:

```
score = 2 ^ ( -avg_path / c(n) )
```

The direction catches people out. A **short** path means easy to isolate, which
means **anomalous**, which means a **high** score. Around 0.5 is unremarkable;
above about 0.6 on this page is worth a look.

Drag the threshold and watch the count. The readout gives the range of scores
present, so you can see where the population actually sits rather than guessing.

## Subsampling, and why it helps

Each tree is built from a small random subsample &mdash; 256 points by default in
most libraries &mdash; and this is not only for speed.

With the full dataset, a cluster of anomalies can be dense enough to look normal
locally: its members shield each other and need several splits to separate. Take
a small sample and those anomalies are usually alone in it, so they are isolated
immediately. Subsampling reduces *swamping* (normal points looking anomalous
because the data is crowded) and *masking* (anomalies hiding one another).

The trees control shows the other half of the picture. At five trees the flagged
set jitters as you change the seed; at sixty it is stable. Path length from one
random tree is nearly meaningless, and the average over many is not.

**Each tree is built from a sample and then used to score every point.** Building
and scoring on the same subsample is a mistake worth naming: a point missing from
a tree contributes nothing that round, its average path comes out short, and it
looks like an outlier. Everything ends up flagged.

## What it is good at

**Speed.** Linear in the number of points, and the trees are shallow. It is one
of the few anomaly detectors that is genuinely cheap on large data.

**High dimensions.** No distance metric, so it avoids the concentration problem
that undoes k-nearest-neighbour approaches.

**No labels.** Entirely unsupervised.

**No distributional assumption.** Unlike a Gaussian-based detector, it does not
care what shape normal is.

## What it is bad at

**Local anomalies.** It finds points that are globally easy to separate. A point
sitting in a *low-density gap between two dense clusters* may be perfectly normal
globally and clearly anomalous locally. **Local Outlier Factor** compares each
point's density to its neighbours' and catches these.

**Axis-aligned splits.** Cuts are perpendicular to the axes, which produces
artefacts along diagonals in correlated data. **Extended Isolation Forest** uses
random hyperplanes instead.

**Irrelevant features.** Random feature selection wastes splits on columns that
carry nothing.

**The contamination parameter.** Libraries ask what fraction of the data is
anomalous in order to place a threshold, and if you knew that you would be much
further along. Prefer to look at the score distribution and choose a cut, which
is what the slider here makes you do.

## Where it goes wrong

**Reading the score backwards.** High means anomalous.

**Too few trees.** The estimate is noisy; check by changing the seed.

**Trusting `contamination`.** It is a guess presented as a parameter.

**Expecting it to find local anomalies.** Use LOF for those.
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
intro: Combining unlike models, when it helps, and a live demonstration of it hurting.

## Different from bagging and boosting

[Bagging](random_forest.html) and [boosting](gradient_boosting.html) build many
copies of one kind of model &mdash; hundreds of trees &mdash; and combine them.

Voting and stacking combine models of *different* kinds: a logistic regression, a
gradient-boosted tree and a neural network, say. The hope is that models with
different inductive biases fail on different rows, so their errors partly cancel.

That hope is a condition, not a guarantee, and this page is largely about the
condition failing.

## Voting

**Hard voting** takes the majority label. **Soft voting** averages predicted
probabilities and thresholds the mean, which is generally better because it uses
confidence rather than discarding it &mdash; and which requires
[calibrated](probability_calibration.html) probabilities to be meaningful.

Every member counts equally. That is the strength when the members are comparable
and the weakness when they are not.

Look at the readout with the default settings. Three learners score roughly
62%, 66% and 90%, and the **majority vote scores about 77% &mdash; worse than the
best member alone.** Two weak learners outvote a strong one whenever they agree,
and they agree often enough to drag the result down.

This is not a contrived arrangement. It is what happens whenever an ensemble is
assembled without checking whether the members are of comparable quality, and it
is the reason "just ensemble it" is bad advice.

## Stacking

Stacking replaces the fixed rule with a learned one. Train the base models, take
their predictions as features, and fit a second model &mdash; the **meta-learner**
&mdash; on those.

The meta-learner discovers what a vote cannot: which model to trust, and when.
The learned weights are in the readout, and the strong learner attracts most of
the weight while a weak one can go slightly negative &mdash; meaning the
meta-learner has found that model to be worse than uninformative in some regions.

With the defaults, stacking matches the best single learner rather than beating
it. That is an honest and common outcome, and it is still a gain over the vote:
stacking recovered the best model automatically, where voting destroyed it.

Move the thresholds so that the three learners are closer in quality, and the
picture changes &mdash; the vote catches up, because its assumption is finally
true.

## Getting stacking right

The essential detail is how the meta-learner's training data is produced.

Training the base models and then feeding their predictions **on the same data**
to the meta-learner leaks badly. A model that overfits its training set produces
suspiciously good predictions there, so the meta-learner learns to trust the most
overfitted member.

The fix is **cross-validated predictions**: split the data into folds, and for
each fold predict with base models trained on the other folds. Every prediction
the meta-learner sees is then out-of-sample. This is what scikit-learn's
`StackingClassifier` does, and it is why stacking costs roughly *k* times the
training of its members.

A second convention: keep the meta-learner **simple**. Logistic regression is the
standard choice. It has few base predictions to work with, and a flexible
meta-learner overfits them readily.

## When an ensemble is worth it

**Members must be comparable in quality.** Otherwise voting hurts, as above.

**Members must make different mistakes.** Three models that fail on the same rows
combine into one model that fails on those rows. Checking the correlation of
their errors is the diagnostic, and it is worth doing before building anything.

**The gain must justify the cost.** An ensemble multiplies training time,
inference time, memory and the number of things that can break in production. A
one-point gain on a leaderboard is worth it; a one-point gain in a service
usually is not.

## Where it goes wrong

**Ensembling a strong model with weak ones by vote.** Demonstrated above.

**Fitting the meta-learner on in-sample predictions.** It learns to trust the
most overfitted base model.

**A complex meta-learner.** Few features, plenty of opportunity to overfit.

**Assuming diversity.** Two gradient-boosted models with different seeds are not
diverse; check whether their errors actually differ.
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
