# -*- coding: utf-8 -*-
"""Authored end-of-module questions.

`tools/build_labs.py` gives every module a check. Where a module appears here
it gets these multiple-choice questions; where it does not, the build falls
back to retrieval flashcards generated from the page's own key takeaways.

The 25 modules on the curated Learning Path are covered first, because that is
the route a beginner is steered down and the one place a wrong mental model
does the most damage later.

Writing more: add an entry keyed by the module path. Each question needs `q`,
`options`, a zero-based `answer`, and `why` - the explanation shown after
answering, which is the part that actually teaches. Distractors should be
things people genuinely believe, not obviously silly options; a question
everyone gets right measures nothing.
"""

LABS = {

# =========================================================================
# Groundwork - maths
# =========================================================================

"maths/equation_of_line.html": {"check": [
    {"q": "In y = mx + c, what does c control?",
     "options": ["How steep the line is",
                 "Where the line crosses the y-axis",
                 "How long the line is",
                 "Whether the line is straight"],
     "answer": 1,
     "why": "c is the intercept: it slides the whole line up and down without "
            "rotating it. m is the slope, and it is the only term that changes "
            "the steepness."},
    {"q": "A line has slope m = 0. What does it look like?",
     "options": ["Vertical", "Horizontal", "At 45 degrees", "It does not exist"],
     "answer": 1,
     "why": "Slope is rise over run. A zero rise for any run is a flat, "
            "horizontal line. A vertical line is the case with no defined slope "
            "at all, because the run is zero and you cannot divide by it."},
    {"q": "Why does this one equation matter so much later on?",
     "options": ["It is the simplest thing to plot",
                 "A neuron computes exactly this shape - weights are slopes and "
                 "the bias is an intercept",
                 "Every dataset is a straight line",
                 "It is required for calculus"],
     "answer": 1,
     "why": "w·x + b is y = mx + c with more inputs. Weights play the role of "
            "slopes and the bias plays the role of the intercept, which is why "
            "a perceptron can only ever draw a straight boundary."},
]},

"maths/vectors_and_dot_product.html": {"check": [
    {"q": "Two vectors point in exactly opposite directions. Their dot product is:",
     "options": ["Zero", "Positive", "Negative", "Undefined"],
     "answer": 2,
     "why": "The dot product carries the cosine of the angle between them. At "
            "180 degrees the cosine is -1, so the product is negative. It is "
            "zero only when they are perpendicular."},
    {"q": "What does a dot product of zero tell you?",
     "options": ["The vectors are identical",
                 "The vectors are at right angles",
                 "One vector has zero length",
                 "Both b and c are possible"],
     "answer": 3,
     "why": "Perpendicular vectors give zero, and so does any vector dotted "
            "with the zero vector. Both cases are worth remembering - the "
            "second is a common source of silent bugs."},
    {"q": "Where does the dot product show up in a neural network?",
     "options": ["Only in the loss function",
                 "In every neuron - the weighted sum is a dot product of "
                 "weights and inputs",
                 "Only during backpropagation",
                 "Only in convolutional layers"],
     "answer": 1,
     "why": "w·x is literally a dot product. A layer of neurons is a stack of "
            "them, which is why a layer is implemented as a matrix multiply."},
]},

"maths/derivatives_and_slope.html": {"check": [
    {"q": "The derivative of a function at a point tells you:",
     "options": ["The value of the function there",
                 "The slope of the tangent line there",
                 "The area under the curve up to there",
                 "Whether the function is positive"],
     "answer": 1,
     "why": "A derivative is an instantaneous rate of change - the slope of the "
            "curve at that exact point, which is the tangent line's slope."},
    {"q": "At a minimum of a smooth curve, the derivative is:",
     "options": ["As large as possible", "Zero", "Negative", "Undefined"],
     "answer": 1,
     "why": "The curve is momentarily flat at the bottom. This is exactly what "
            "gradient descent chases: it keeps stepping until the gradient is "
            "near zero and there is no downhill direction left."},
    {"q": "Gradient descent subtracts the gradient rather than adding it. Why?",
     "options": ["To keep the numbers small",
                 "Because the gradient points uphill, and the goal is to go down",
                 "Because loss is always negative",
                 "To avoid dividing by zero"],
     "answer": 1,
     "why": "The gradient points in the direction of steepest increase. To "
            "reduce the loss you move against it - which is the minus sign in "
            "every update rule you will ever see."},
]},

"maths/mean_variance_standard_deviation.html": {"check": [
    {"q": "Every value in a dataset is increased by 10. What happens?",
     "options": ["The mean and the standard deviation both rise by 10",
                 "The mean rises by 10, the standard deviation is unchanged",
                 "Neither changes",
                 "The standard deviation rises, the mean does not"],
     "answer": 1,
     "why": "Shifting everything moves the centre but not the spread. The "
            "distances between points are identical, and spread is all the "
            "standard deviation measures."},
    {"q": "Why is standard deviation usually quoted rather than variance?",
     "options": ["It is easier to compute",
                 "It is in the same units as the data, so it is directly readable",
                 "Variance can be negative",
                 "Variance only works for large samples"],
     "answer": 1,
     "why": "Variance is in squared units - 'seconds squared' means nothing to "
            "a reader. Taking the square root returns it to the original units "
            "so it can be compared against the mean."},
    {"q": "A single extreme outlier is added to a dataset. Which is affected more?",
     "options": ["The mean", "The variance", "Both equally", "Neither"],
     "answer": 1,
     "why": "Variance squares each distance from the mean, so a far-away point "
            "contributes enormously. The mean moves too, but only linearly - "
            "this squaring is why variance-based methods are fragile to outliers."},
]},

"maths/probability_basics.html": {"check": [
    {"q": "Two fair coin flips. What is the probability of two heads?",
     "options": ["1/2", "1/4", "1/3", "3/4"],
     "answer": 1,
     "why": "Independent events multiply: 1/2 x 1/2 = 1/4. The four equally "
            "likely outcomes are HH, HT, TH, TT, and only one of them qualifies."},
    {"q": "P(A|B) means:",
     "options": ["The probability of A and B both happening",
                 "The probability of A, given that B has happened",
                 "The probability of A or B",
                 "The probability of B, given A"],
     "answer": 1,
     "why": "The bar is 'given'. Conditioning narrows the world to the cases "
            "where B is true and asks how often A holds within that smaller set. "
            "Swapping the two sides gives a different number - assuming otherwise "
            "is the base-rate fallacy."},
    {"q": "A test is 99% accurate for a disease affecting 1 in 10,000 people. You "
          "test positive. Roughly how worried should you be?",
     "options": ["99% likely to have it",
                 "About 1% likely to have it",
                 "50/50",
                 "Certain to have it"],
     "answer": 1,
     "why": "Among 10,000 people there is about 1 true case and about 100 false "
            "positives, so a positive result is right roughly 1 time in 100. The "
            "base rate dominates, which is exactly what Bayes' rule formalises."},
]},

# =========================================================================
# Your first models
# =========================================================================

"machine_learning/train_test_split.html": {"check": [
    {"q": "Why hold back a test set at all?",
     "options": ["To speed up training",
                 "To estimate how the model does on data it has never seen",
                 "Because algorithms require it",
                 "To reduce the size of the training data"],
     "answer": 1,
     "why": "Training accuracy measures memorisation as much as learning. The "
            "only honest estimate of future performance comes from data the "
            "model has never been fitted on."},
    {"q": "You scale your features using statistics from the whole dataset, then "
          "split. What have you done?",
     "options": ["Nothing wrong - scaling is not learning",
                 "Leaked information from the test set into training",
                 "Made the model train more slowly",
                 "Guaranteed overfitting"],
     "answer": 1,
     "why": "The scaler saw the test set's mean and range, so the test score is "
            "no longer clean. Fit the scaler on the training split only, then "
            "apply it to the test split."},
    {"q": "Your test set is tiny - say 20 rows. What is the main problem?",
     "options": ["Training will be slow",
                 "The score is so noisy that it barely constrains anything",
                 "The model cannot converge",
                 "There is no problem"],
     "answer": 1,
     "why": "With 20 rows, one extra mistake moves accuracy by five whole "
            "percentage points. The estimate has such wide error bars that it "
            "cannot distinguish a good model from a mediocre one."},
]},

"machine_learning/one_hot_encoding.html": {"check": [
    {"q": "Why not just number categories 1, 2, 3 and feed them in directly?",
     "options": ["Numbers are slower to process",
                 "It invents an order and a distance that the categories do not have",
                 "Models cannot accept integers",
                 "It uses more memory"],
     "answer": 1,
     "why": "Labelling red=1, green=2, blue=3 tells the model green sits between "
            "red and blue, and that blue is three times red. Both are nonsense, "
            "and a linear model will act on them."},
    {"q": "A column has 50,000 distinct values. One-hot encoding it will:",
     "options": ["Work fine",
                 "Create 50,000 mostly-zero columns, which is usually unusable",
                 "Fail with an error",
                 "Automatically group rare values"],
     "answer": 1,
     "why": "High-cardinality columns explode under one-hot encoding. This is "
            "where target encoding, hashing or learned embeddings earn their "
            "keep instead."},
    {"q": "When does label encoding become the right choice?",
     "options": ["Never",
                 "When the categories genuinely have an order, like small/medium/large",
                 "Whenever there are more than 10 categories",
                 "Only for the target variable"],
     "answer": 1,
     "why": "Ordinal data has a real ordering, so encoding it as 1/2/3 preserves "
            "information rather than fabricating it. Tree-based models are also "
            "far more tolerant of integer codes than linear ones."},
]},

"machine_learning/linear_regression_with_ols.html": {"check": [
    {"q": "Ordinary least squares minimises the sum of:",
     "options": ["The residuals",
                 "The squared residuals",
                 "The absolute residuals",
                 "The predicted values"],
     "answer": 1,
     "why": "Squaring makes every error positive so they cannot cancel, and it "
            "gives a smooth function with a closed-form solution. It also "
            "punishes large errors disproportionately."},
    {"q": "Why does OLS react so strongly to a single far-off point?",
     "options": ["Because it uses the mean",
                 "Because squaring makes a distant point dominate the total error",
                 "Because the data must be normal",
                 "It does not - OLS is robust"],
     "answer": 1,
     "why": "An error of 10 contributes 100; an error of 1 contributes 1. One "
            "outlier can outweigh a hundred well-fitted points, which is why "
            "absolute-error methods are preferred when outliers are expected."},
    {"q": "R-squared of 0.0 means:",
     "options": ["The model is perfect",
                 "The model explains no more variance than predicting the mean",
                 "The data has no variance",
                 "The model is broken"],
     "answer": 1,
     "why": "R-squared compares your model against the trivial always-predict-the-"
            "mean baseline. Zero means you have matched that baseline and no more. "
            "It can even go negative if you do worse."},
]},

"machine_learning/knn.html": {"check": [
    {"q": "You set K = 1 and the decision boundary becomes jagged and unstable. "
          "That is a symptom of:",
     "options": ["Underfitting - the model is too simple",
                 "Overfitting - the model is chasing individual points, noise included",
                 "A bug in the distance calculation",
                 "Too little training data"],
     "answer": 1,
     "why": "With K = 1 every single point, including mislabelled ones, gets its "
            "own territory. High variance and a jagged boundary are the classic "
            "signature of overfitting."},
    {"q": "Why does KNN need its features scaled?",
     "options": ["To speed up the distance computation",
                 "Because a feature with a larger numeric range dominates the "
                 "distance, regardless of its importance",
                 "Because KNN assumes normally distributed data",
                 "It does not need scaling"],
     "answer": 1,
     "why": "Distance sums squared differences. A salary in the tens of thousands "
            "swamps an age in the tens, so the model quietly becomes 'nearest by "
            "salary' no matter what you intended."},
    {"q": "KNN is called a lazy learner because:",
     "options": ["It is inaccurate",
                 "It does no work at training time and defers everything to "
                 "prediction time",
                 "It only uses a subset of the data",
                 "It converges slowly"],
     "answer": 1,
     "why": "Training is just storing the dataset. All the cost lands on "
            "prediction, when it must measure the new point against every stored "
            "one - which is why KNN is expensive to serve at scale."},
]},

"machine_learning/confusion_matrix.html": {"check": [
    {"q": "A disease affects 1% of people. A model that always predicts "
          "'healthy' scores 99% accuracy. What does the confusion matrix show?",
     "options": ["A strong model",
                 "Zero true positives - it never catches a single case",
                 "Balanced precision and recall",
                 "A high false positive rate"],
     "answer": 1,
     "why": "The whole top row of the matrix is empty. Accuracy hides this "
            "completely, which is exactly why the matrix is worth reading on any "
            "imbalanced problem."},
    {"q": "For a spam filter, which error is usually more costly?",
     "options": ["A false negative - spam reaching the inbox",
                 "A false positive - a real email sent to the spam folder",
                 "They are equally costly",
                 "Neither matters if accuracy is high"],
     "answer": 1,
     "why": "A missed spam is an annoyance; a lost job offer is a disaster. This "
            "asymmetry is why you tune the threshold toward precision here, and "
            "toward recall for something like cancer screening."},
    {"q": "Recall answers which question?",
     "options": ["Of the cases I flagged, how many were real?",
                 "Of the real cases, how many did I catch?",
                 "How many predictions were correct overall?",
                 "How balanced are the classes?"],
     "answer": 1,
     "why": "Recall divides by the actual positives, so it measures coverage of "
            "the true cases. Precision divides by your predicted positives and "
            "measures how trustworthy a flag is."},
]},

# =========================================================================
# How learning actually works
# =========================================================================

"deep_learning/perceptron.html": {"check": [
    {"q": "A single perceptron cannot learn XOR. Why not?",
     "options": ["XOR needs more training data",
                 "XOR is not linearly separable, and one perceptron draws one "
                 "straight boundary",
                 "XOR requires a sigmoid activation",
                 "The learning rate is always too high"],
     "answer": 1,
     "why": "No single straight line separates XOR's two classes. No choice of "
            "weights and bias fixes that - it is a limit of the shape the model "
            "can express, which is what stacking layers solves."},
    {"q": "What does the bias term let a neuron do?",
     "options": ["Learn faster",
                 "Shift its decision boundary away from the origin",
                 "Rotate its decision boundary",
                 "Handle more inputs"],
     "answer": 1,
     "why": "Weights rotate the boundary; the bias translates it. Without a bias "
            "every boundary is nailed to the origin, which is a severe and "
            "usually pointless restriction."},
    {"q": "Why can a step activation not be trained by backpropagation?",
     "options": ["It is too slow",
                 "Its gradient is zero everywhere it is defined, so there is "
                 "nothing to descend",
                 "It only outputs integers",
                 "It needs too much memory"],
     "answer": 1,
     "why": "Backpropagation moves weights along the gradient. A flat function "
            "gives a gradient of zero everywhere, so no weight ever updates. "
            "This is precisely why sigmoid and then ReLU replaced it."},
]},

"deep_learning/activation_functions.html": {"check": [
    {"q": "Stack 100 linear layers with no activation between them. What can the "
          "result represent?",
     "options": ["Any function at all",
                 "Exactly what a single linear layer can - nothing more",
                 "Only step functions",
                 "Curves, but not corners"],
     "answer": 1,
     "why": "A chain of matrix multiplies collapses into one matrix. Without a "
            "non-linearity, depth buys literally nothing."},
    {"q": "A ReLU unit outputs zero for every input in your dataset and its "
          "gradient never recovers. This is called:",
     "options": ["Vanishing gradient", "A dead ReLU", "Exploding gradient",
                 "Saturation"],
     "answer": 1,
     "why": "ReLU's gradient is exactly zero on the negative side, so a unit "
            "pushed fully negative can never be updated back. Leaky ReLU exists "
            "to keep a small gradient alive there."},
    {"q": "Why do deep sigmoid networks train so badly?",
     "options": ["Sigmoid is slow to compute",
                 "Its gradient is tiny at both ends, and multiplying many tiny "
                 "gradients vanishes the signal",
                 "Sigmoid cannot output negative values",
                 "It requires normalised inputs"],
     "answer": 1,
     "why": "Sigmoid's derivative peaks at 0.25 and falls toward zero at the "
            "tails. Chain a dozen of those together and the gradient reaching "
            "the early layers is effectively zero."},
]},

"deep_learning/how_loss_is_calculated.html": {"check": [
    {"q": "What is a loss function for?",
     "options": ["Measuring how fast the model trains",
                 "Turning 'how wrong is this prediction' into one number that "
                 "can be minimised",
                 "Choosing the architecture",
                 "Preventing overfitting"],
     "answer": 1,
     "why": "Optimisation needs a single scalar to push downhill. The loss is "
            "that scalar, and its choice defines what the model treats as an "
            "error in the first place."},
    {"q": "Why use cross-entropy rather than squared error for classification?",
     "options": ["It is faster",
                 "It punishes confident wrong answers far more sharply, giving "
                 "usable gradients",
                 "It works without probabilities",
                 "It cannot overfit"],
     "answer": 1,
     "why": "Cross-entropy goes to infinity as a confident prediction turns out "
            "wrong. Squared error caps out, so a badly wrong classifier gets only "
            "a weak nudge to fix itself."},
    {"q": "Training loss is falling but validation loss has started to rise. "
          "This means:",
     "options": ["The learning rate is too low",
                 "The model has started overfitting",
                 "The data is corrupted",
                 "Training has converged"],
     "answer": 1,
     "why": "The model is still improving on data it has seen while getting worse "
            "on data it has not. That gap opening up is the definition of "
            "overfitting, and the point early stopping watches for."},
]},

"deep_learning/gradient_descent_training.html": {"check": [
    {"q": "Your loss oscillates wildly and sometimes increases. The most likely "
          "cause is:",
     "options": ["The learning rate is too high",
                 "The learning rate is too low",
                 "Not enough training data",
                 "Too many layers"],
     "answer": 0,
     "why": "Steps large enough to overshoot the minimum bounce from one wall of "
            "the valley to the other. Cutting the learning rate is the first "
            "thing to try."},
    {"q": "The loss decreases, but almost imperceptibly, over thousands of steps. "
          "This suggests:",
     "options": ["The learning rate is too high",
                 "The learning rate is too low",
                 "The model has converged",
                 "The data needs shuffling"],
     "answer": 1,
     "why": "Tiny steps make real but glacial progress. It is the mirror image of "
            "the previous failure, and the reason schedules start high and decay "
            "rather than picking one value forever."},
    {"q": "Why subtract the gradient instead of adding it?",
     "options": ["To keep weights positive",
                 "The gradient points uphill, and the aim is to reduce the loss",
                 "To prevent overfitting",
                 "Because the loss is negative"],
     "answer": 1,
     "why": "The gradient is the direction of steepest increase. Moving against "
            "it is what makes the algorithm gradient *descent*."},
]},

"deep_learning/neural_network.html": {"check": [
    {"q": "What do the hidden layers of a network actually do?",
     "options": ["Store the training data",
                 "Build progressively more useful representations of the input",
                 "Reduce the number of parameters",
                 "Shuffle the inputs"],
     "answer": 1,
     "why": "Each layer re-describes its input in terms the next layer finds "
            "easier. That learned re-description is the thing deep learning buys "
            "you over hand-engineered features."},
    {"q": "Widening a layer from 64 to 512 units mainly increases:",
     "options": ["Training speed",
                 "Capacity - and with it the risk of overfitting",
                 "The learning rate",
                 "The number of layers"],
     "answer": 1,
     "why": "More parameters means more that can be memorised. Extra capacity "
            "with no extra data or regularisation is the standard route into "
            "overfitting."},
    {"q": "All weights are initialised to exactly zero. What happens?",
     "options": ["Training proceeds normally",
                 "Every unit in a layer computes the same thing and stays "
                 "identical forever",
                 "The loss becomes negative",
                 "The network trains faster"],
     "answer": 1,
     "why": "Identical weights get identical gradients, so the units never "
            "differentiate. Random initialisation exists to break exactly this "
            "symmetry."},
]},

# =========================================================================
# Making training behave
# =========================================================================

"deep_learning/overfitting_vs_underfitting.html": {"check": [
    {"q": "Training accuracy 99%, validation accuracy 62%. This is:",
     "options": ["Underfitting", "Overfitting", "A good model", "Data leakage"],
     "answer": 1,
     "why": "The model has learned the training set specifically, including its "
            "noise, and cannot generalise. A large gap between the two scores is "
            "the tell."},
    {"q": "Training accuracy 61%, validation accuracy 60%. This is:",
     "options": ["Underfitting - the model is too simple for the problem",
                 "Overfitting",
                 "Ideal",
                 "Impossible"],
     "answer": 0,
     "why": "Both scores are poor and close together, so nothing is being "
            "memorised - there simply is not enough capacity, or enough training, "
            "to capture the pattern."},
    {"q": "Which change would you expect to reduce overfitting?",
     "options": ["Adding more layers",
                 "Adding more training data",
                 "Training for more epochs",
                 "Raising the learning rate"],
     "answer": 1,
     "why": "More data makes memorisation harder and generalisation easier. The "
            "other three all push capacity or fitting further in the direction "
            "that caused the problem."},
]},

"machine_learning/cross_validation.html": {"check": [
    {"q": "What problem does k-fold cross-validation solve?",
     "options": ["Slow training",
                 "A single train/test split gives one noisy estimate that depends "
                 "on which rows landed where",
                 "Class imbalance",
                 "Missing values"],
     "answer": 1,
     "why": "Every row gets to be in the test set exactly once, so the score is "
            "averaged over k splits instead of resting on one lucky or unlucky "
            "partition."},
    {"q": "For an imbalanced dataset, which variant should you reach for?",
     "options": ["Leave-one-out", "Stratified k-fold", "A single 50/50 split",
                 "More folds"],
     "answer": 1,
     "why": "Stratification preserves the class ratio in every fold. Without it "
            "a rare class can be absent from a fold entirely, making that fold's "
            "score meaningless."},
    {"q": "What is the main cost of cross-validation?",
     "options": ["It needs more data",
                 "You train k models instead of one",
                 "It biases the estimate upward",
                 "It cannot be used with neural networks"],
     "answer": 1,
     "why": "10-fold means ten training runs. That is usually fine for classical "
            "models and often prohibitive for large deep networks, which is why "
            "they typically use a single held-out set."},
]},

"deep_learning/dropout_in_neural_networks.html": {"check": [
    {"q": "What does dropout do during training?",
     "options": ["Removes layers permanently",
                 "Randomly zeroes a fraction of unit outputs on each forward pass",
                 "Reduces the learning rate over time",
                 "Discards the worst training examples"],
     "answer": 1,
     "why": "A different random subset is silenced every pass, so no unit can "
            "rely on any particular other unit being present. That forced "
            "redundancy is what regularises the network."},
    {"q": "Is dropout active at inference time?",
     "options": ["Yes, always",
                 "No - it is disabled, and activations are scaled to compensate",
                 "Only for the last layer",
                 "Only if the model overfits"],
     "answer": 1,
     "why": "You want deterministic predictions when serving. Leaving dropout on "
            "at inference is a classic bug: it makes the same input return "
            "different answers on each call."},
    {"q": "A dropout rate of 0.9 on a small network is likely to cause:",
     "options": ["Faster convergence",
                 "Severe underfitting - too little signal survives each pass",
                 "Perfect generalisation",
                 "No change"],
     "answer": 1,
     "why": "Regularisation is a dial, not a switch. Drop nine units in ten and "
            "there is barely a network left to learn anything."},
]},

"deep_learning/early_stopping_in_neural_networks.html": {"check": [
    {"q": "Early stopping monitors which quantity?",
     "options": ["Training loss", "Validation loss", "The learning rate",
                 "Gradient magnitude"],
     "answer": 1,
     "why": "Training loss almost always keeps falling, so it can never signal "
            "when to stop. Validation loss is the one that turns around when "
            "generalisation starts degrading."},
    {"q": "What does the 'patience' setting control?",
     "options": ["How many epochs to train in total",
                 "How many epochs without improvement to tolerate before stopping",
                 "The size of the validation set",
                 "How much the loss must fall by"],
     "answer": 1,
     "why": "Validation loss is noisy and can tick up for an epoch or two before "
            "improving again. Patience stops you from quitting on a wobble."},
    {"q": "Patience is set to 0. What is the risk?",
     "options": ["Training never stops",
                 "Stopping on the first noisy uptick, well before the real minimum",
                 "The model overfits badly",
                 "The learning rate decays too fast"],
     "answer": 1,
     "why": "With no tolerance at all, one bad epoch ends the run. You get an "
            "undertrained model and a validation curve that had plenty left in it."},
]},

"deep_learning/model_training_curve.html": {"check": [
    {"q": "Training loss keeps falling while validation loss rises. The right "
          "reading is:",
     "options": ["Train longer", "Stop around where they diverged",
                 "Raise the learning rate", "Add more layers"],
     "answer": 1,
     "why": "The divergence point is where the model stopped learning the pattern "
            "and started learning the training set. Everything after it is "
            "overfitting."},
    {"q": "Both curves are flat and high from the very first epoch. Most likely:",
     "options": ["The model has converged",
                 "The model is not learning at all - bad learning rate, bad "
                 "initialisation, or a wiring bug",
                 "The dataset is too large",
                 "Dropout is too low"],
     "answer": 1,
     "why": "A model that never improves has not converged, it has failed to "
            "start. Check the learning rate first, then whether the labels and "
            "the loss are actually connected."},
    {"q": "Validation loss sits consistently *below* training loss. The usual "
          "explanation is:",
     "options": ["A bug - this is impossible",
                 "Regularisation like dropout penalises the training pass but not "
                 "the validation pass",
                 "The model is overfitting",
                 "The validation set is too large"],
     "answer": 1,
     "why": "Dropout is on during training and off during validation, so the "
            "training number is measured under harder conditions. It is normal "
            "early on and not a cause for alarm."},
]},

# =========================================================================
# Pick a specialism
# =========================================================================

"computer_vision/feature_map_in_cnn.html": {"check": [
    {"q": "A feature map is:",
     "options": ["The filter's weights",
                 "The output produced by sliding one filter across the input",
                 "A diagram of the architecture",
                 "The final classification"],
     "answer": 1,
     "why": "The filter is what you slide; the feature map is what comes out - a "
            "record of where in the image that filter found what it responds to."},
    {"q": "Applying a 3x3 filter to a 32x32 image with no padding gives:",
     "options": ["32x32", "30x30", "34x34", "16x16"],
     "answer": 1,
     "why": "The filter cannot centre on the outermost ring of pixels, so you "
            "lose one from each side: 32 - 3 + 1 = 30. Padding exists to hold the "
            "size steady."},
    {"q": "Why do later layers have many more feature maps than early ones?",
     "options": ["To use up GPU memory",
                 "Early layers detect a few generic patterns; later layers combine "
                 "them into many specific ones",
                 "Because the image gets larger",
                 "To speed up training"],
     "answer": 1,
     "why": "There are only so many ways to be an edge. There are a great many "
            "ways to be a combination of edges, so the count of distinct useful "
            "detectors grows with depth as the spatial size shrinks."},
]},

"natural_language_processing/what_are_embeddings.html": {"check": [
    {"q": "What is an embedding?",
     "options": ["A compressed copy of the text",
                 "A dense vector whose position encodes meaning, learned from usage",
                 "A dictionary of definitions",
                 "The tokenizer's vocabulary"],
     "answer": 1,
     "why": "Embeddings place words in a space where distance means something. "
            "Nothing about the meaning is written down - it is inferred entirely "
            "from which contexts a word turns up in."},
    {"q": "Why are embeddings better than one-hot vectors for words?",
     "options": ["They use less memory only",
                 "One-hot makes every pair of words equally distant, so no "
                 "similarity can be expressed",
                 "One-hot vectors cannot be used in networks",
                 "They are easier to compute"],
     "answer": 1,
     "why": "Under one-hot, 'cat' is exactly as far from 'dog' as from "
            "'parliament'. Embeddings can put related words near each other, "
            "which is the whole point."},
    {"q": "Embeddings trained on ordinary web text reliably reproduce:",
     "options": ["Perfect definitions",
                 "The social biases present in that text",
                 "Grammatical rules only",
                 "Nothing beyond word frequency"],
     "answer": 1,
     "why": "The vectors encode how words are actually used, including every "
            "stereotype in the corpus. This is measurable, well documented, and a "
            "real problem in deployed systems."},
]},

"gen_ai/how_llms_predict_next_word.html": {"check": [
    {"q": "At each step, a language model produces:",
     "options": ["A single word",
                 "A probability distribution over the whole vocabulary",
                 "A sentence",
                 "A yes/no decision"],
     "answer": 1,
     "why": "The model scores every token it knows. Which one actually gets "
            "emitted is a separate sampling decision made on top of that "
            "distribution."},
    {"q": "Raising the sampling temperature does what?",
     "options": ["Makes output more deterministic",
                 "Flattens the distribution, so less likely tokens get picked "
                 "more often",
                 "Speeds up generation",
                 "Increases the context length"],
     "answer": 1,
     "why": "Low temperature sharpens toward the top token and reads as safe and "
            "repetitive. High temperature flattens the odds and reads as creative, "
            "or as incoherent once pushed too far."},
    {"q": "Why does a model produce fluent text that is confidently wrong?",
     "options": ["It has a bug",
                 "It is optimised for plausible continuations, not for truth",
                 "Its training data was too small",
                 "The temperature is always too high"],
     "answer": 1,
     "why": "Next-token prediction rewards text that looks like its training "
            "data. A fluent falsehood satisfies that objective just as well as a "
            "fluent fact - there is no separate check for truth."},
]},

"dsa/big_o_notation.html": {"check": [
    {"q": "Big-O describes:",
     "options": ["Exactly how many seconds an algorithm takes",
                 "How the cost grows as the input grows",
                 "How much memory a language uses",
                 "How readable the code is"],
     "answer": 1,
     "why": "It is a statement about growth, not about wall-clock time. Hardware "
            "changes the constant; it does not change the shape of the curve."},
    {"q": "Which is O(1)?",
     "options": ["Scanning a list for a value",
                 "Reading array element 5 by index",
                 "Sorting a list",
                 "Nested loops over the same list"],
     "answer": 1,
     "why": "Indexing computes an address and jumps to it, taking the same time "
            "whether the array holds ten items or ten million."},
    {"q": "For n = 20, an O(n^2) algorithm may well beat an O(n log n) one. Why?",
     "options": ["Big-O is wrong",
                 "Big-O drops constants, and at small n those constants dominate",
                 "O(n log n) is only for sorted data",
                 "It cannot happen"],
     "answer": 1,
     "why": "Asymptotic notation describes behaviour as n grows large. This is "
            "exactly why real sort implementations switch to insertion sort for "
            "small partitions."},
]},

"database/joins_in_sql.html": {"check": [
    {"q": "A LEFT JOIN returns:",
     "options": ["Only rows matching in both tables",
                 "Every row from the left table, with NULLs where the right has "
                 "no match",
                 "Every row from both tables",
                 "Only rows with no match"],
     "answer": 1,
     "why": "The left table is preserved whole. That is what makes LEFT JOIN the "
            "tool for 'show me all customers, including the ones with no orders'."},
    {"q": "You LEFT JOIN, then filter the right table in the WHERE clause. What "
          "usually happens?",
     "options": ["Nothing changes",
                 "The unmatched rows have NULLs, fail the filter, and vanish - "
                 "turning it into an INNER JOIN",
                 "The query errors",
                 "Duplicate rows appear"],
     "answer": 1,
     "why": "NULL fails almost every comparison. Putting that condition in the "
            "ON clause instead keeps the unmatched rows, and this is one of the "
            "most common SQL bugs there is."},
    {"q": "Joining on a column with duplicate values on both sides produces:",
     "options": ["An error",
                 "More rows than either table - every matching pair is returned",
                 "The rows are deduplicated automatically",
                 "Only the first match"],
     "answer": 1,
     "why": "Three matching rows on each side give nine output rows. Unexpected "
            "row multiplication after a join is nearly always a duplicate key on "
            "one side."},
]},

}
