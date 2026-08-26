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

"machine_learning/pca.html": {"check": [
    {"q": "What does the first principal component point along?",
     "options": ["The direction that best separates the classes",
                 "The direction the data varies along most",
                 "The column with the largest values",
                 "The line minimising vertical distance to the target"],
     "answer": 1,
     "why": "PC1 maximises uᵀΣu - the variance measured along the direction u. "
            "It has never seen your labels, which is why it is unsupervised and "
            "why it can happily discard the direction that separates the classes."},
    {"q": "Two features are almost perfectly correlated. What happens to the "
          "second eigenvalue?",
     "options": ["It grows", "It stays the same",
                 "It collapses towards zero",
                 "It becomes negative"],
     "answer": 2,
     "why": "Perfect correlation means the cloud lies on a line: there is no "
            "spread in the perpendicular direction, so λ₂ is zero and PC1 "
            "explains 100%. Two columns, one dimension of information."},
    {"q": "Why must you usually standardise the columns before running PCA?",
     "options": ["Otherwise the maths is undefined",
                 "Because variance carries units, so a column measured in "
                 "large numbers dominates the first component",
                 "To make the components interpretable",
                 "To speed up the eigen-decomposition"],
     "answer": 1,
     "why": "PCA maximises variance, and variance is in squared units. Income in "
            "rupees next to age in years makes income the first component no "
            "matter what the data means."},
]},

# =========================================================================
# Python - the language the other tracks assume
# =========================================================================

"python/hello_python.html": {"check": [
    {"q": "What does print(\"Hello\") send to the screen?",
     "options": ["Hello", "\"Hello\" with quotes", "Hello\\n", "Nothing"],
     "answer": 0,
     "why": "print() writes the value, not its source text. The quotes are "
            "part of the code that made the string; they are not part of the "
            "string."},
    {"q": "print(2 + 3) prints:",
     "options": ["2 + 3", "\"2 + 3\"", "5", "23"],
     "answer": 2,
     "why": "Python evaluates the expression before printing, so print(2 + 3) "
            "is exactly print(5)."}, 
    {"q": "A program is just:",
     "options": ["A text file of instructions the interpreter reads top to bottom",
                 "A compiled binary",
                 "A list of files",
                 "A single function"],
     "answer": 0,
     "why": "Python reads your .py file from top to bottom and runs each "
            "statement in turn. That ordering matters - a line can use a name "
            "only after the line that defined it."},
]},

"python/variables_and_types.html": {"check": [
    {"q": "x = \"10\" makes x:",
     "options": ["The number 10", "The string \"10\"",
                 "An error", "A list"],
     "answer": 1,
     "why": "Python guesses the type from the value. 10 with quotes is a "
            "string; without them it is an integer, and the two behave "
            "completely differently even though they look alike."},
    {"q": "Which of these is NOT a built-in Python type?",
     "options": ["int", "str", "list", "integer"],
     "answer": 3,
     "why": "The type is spelled int, not integer. Being able to ask type(x) "
            "and read the answer is a core skill on this track."},
    {"q": "You reuse a variable name for a new value. The old value:",
     "options": ["Still exists under that name",
                 "Is gone from that name (unless something else still "
                 "references it)",
                 "Moves to another variable automatically",
                 "Causes an error"],
     "answer": 1,
     "why": "A name is a label pointing at a value. Rebinding it points the "
            "label at something else; the old value is discarded once nothing "
            "references it. Names do not hold values, they label them."},
]},

"python/numbers_and_operators.html": {"check": [
    {"q": "7 / 2 in Python 3 gives:",
     "options": ["3", "3.5", "3 remainder 1", "An error"],
     "answer": 1,
     "why": "Python 3's / is true division and always returns a float when "
            "the division is not exact. The old integer-truncating behaviour "
            "lives on as //."},
    {"q": "7 % 3 evaluates to:",
     "options": ["2", "1", "2.33", "7"],
     "answer": 1,
     "why": "The modulo operator returns the remainder after division: 7 = "
            "2×3 + 1, so 7 % 3 is 1. It is the operator behind 'is n even?' "
            "checks and clock arithmetic."},
    {"q": "2 ** 10 evaluates to:",
     "options": ["20", "1024", "12", "200"],
     "answer": 1,
     "why": "** is exponentiation, not multiplication. 2 ** 10 means 2 raised "
            "to the power 10, which is 1024."},
]},

"python/strings_and_slicing.html": {"check": [
    {"q": "len(\"hello\") returns:",
     "options": ["4", "5", "6", "An error"],
     "answer": 1,
     "why": "len() counts characters. \"hello\" has five of them. It counts "
            "spaces too - len(\"a b\") is 3."},
    {"q": "s = \"python\"; s[0] is:",
     "options": ["\"p\"", "\"y\"", "\"t\"", "\"n\""],
     "answer": 0,
     "why": "Indexing starts at 0 in Python, not 1. s[0] is the first "
            "character, and s[-1] is a convenient way to reach the last one."},
    {"q": "\"hello\".upper() returns:",
     "options": ["\"HELLO\"", "\"hello\"", "5", "An error"],
     "answer": 0,
     "why": "Strings are objects with methods, and most return a NEW string "
            "rather than editing the one in place - \"hello\" is unchanged "
            "after the call."},
]},

"python/lists_and_indexing.html": {"check": [
    {"q": "colours = [\"red\", \"green\", \"blue\"]. What is colours[1]?",
     "options": ["\"red\"", "\"green\"", "\"blue\"", "An error"],
     "answer": 1,
     "why": "Indexes count from 0, so index 1 is the SECOND item. Read an "
            "index as \"how far from the start\" and this stops being a trap."},
    {"q": "That same three-item list. What does colours[3] do?",
     "options": ["Returns \"blue\"", "Returns None", "Raises IndexError",
                 "Adds a fourth item"],
     "answer": 2,
     "why": "Three items occupy indexes 0, 1 and 2. Asking for 3 is out of "
            "range, and Python raises rather than inventing a value."},
    {"q": "After nums = [3, 1, 2] and sorted(nums), what is nums?",
     "options": ["[1, 2, 3]", "[3, 1, 2]", "None", "An error"],
     "answer": 1,
     "why": "sorted() returns a NEW sorted list and leaves the original "
            "alone. nums.sort() is the one that reorders in place - and it "
            "returns None, which is where the confusion usually starts."},
]},

"python/dictionaries.html": {"check": [
    {"q": "person = {\"name\": \"Ada\"}. What does person[\"age\"] do?",
     "options": ["Returns None", "Returns \"\"", "Raises KeyError",
                 "Creates the key"],
     "answer": 2,
     "why": "Square brackets on a missing key raise KeyError. Assigning to a "
            "missing key creates it, but reading one does not."},
    {"q": "What does person.get(\"age\", 0) return when there is no age key?",
     "options": ["0", "None", "KeyError", "\"age\""],
     "answer": 0,
     "why": "get() takes an optional fallback and returns it instead of "
            "raising. With no fallback given it returns None."},
    {"q": "Looping with `for x in person:` gives you:",
     "options": ["The keys", "The values", "Key-value pairs", "Nothing"],
     "answer": 0,
     "why": "Iterating a dictionary yields its keys. Use .items() when you "
            "want both halves, or .values() for just the values."},
]},

"python/booleans_and_comparisons.html": {"check": [
    {"q": "What does bool(\"\") return?",
     "options": ["True", "False", "\"\"", "An error"],
     "answer": 1,
     "why": "Empty things are falsy: \"\", 0, [], {} and None. Everything "
            "else is truthy, which is why `if name:` reads as \"if name is "
            "not empty\"."},
    {"q": "age = 20. What is the value of `age > 18`?",
     "options": ["A bool", "A string", "An int", "Nothing - it is a statement"],
     "answer": 0,
     "why": "A comparison is an expression that produces a real bool value. "
            "You can print it, store it, or pass it around - not only put it "
            "in an if."},
    {"q": "Which operator asks whether two values are equal?",
     "options": ["=", "==", ":=", "==="],
     "answer": 1,
     "why": "= assigns, == compares. Python raises a SyntaxError if you use "
            "= inside an if, which catches the typo early."},
]},

"python/if_elif_else.html": {"check": [
    {"q": "score = 95, and the branches check >= 70, then >= 80, then >= 90 in "
          "that order. What prints?",
     "options": ["The >= 90 branch", "The >= 70 branch", "All three",
                 "Nothing"],
     "answer": 1,
     "why": "Only the FIRST true branch runs. 95 satisfies >= 70, so that one "
            "wins and the rest are skipped - which is why specific conditions "
            "must come before general ones."},
    {"q": "What decides which lines belong to an if branch?",
     "options": ["Curly braces", "The indentation", "A blank line",
                 "The end keyword"],
     "answer": 1,
     "why": "Python uses indentation as real syntax. Moving a line in or out "
            "by four spaces genuinely changes which branch it belongs to."},
    {"q": "How many else clauses can one if statement have?",
     "options": ["As many as you like", "Exactly one", "At most one", "None"],
     "answer": 2,
     "why": "else is optional, and there can be at most one. elif is the "
            "clause you can repeat."},
]},

"python/for_loops_and_range.html": {"check": [
    {"q": "What does range(5) produce?",
     "options": ["1,2,3,4,5", "0,1,2,3,4", "0,1,2,3,4,5", "5"],
     "answer": 1,
     "why": "range stops BEFORE its endpoint, giving five numbers starting at "
            "0. That lines up with zero-based indexing."},
    {"q": "You want a running total. Where does `total = 0` belong?",
     "options": ["Before the loop", "Inside the loop body",
                 "After the loop", "It does not matter"],
     "answer": 0,
     "why": "Inside the body it resets on every pass, so the final answer is "
            "just the last item. The loop runs, no error appears, and the "
            "number is quietly wrong."},
    {"q": "Can you loop over a string with a for loop?",
     "options": ["Yes - it yields characters", "No - only lists work",
                 "Only with range()", "Only if you call list() first"],
     "answer": 0,
     "why": "Strings are iterable, so a for loop walks them one character at "
            "a time."},
]},

"python/while_loops_and_control.html": {"check": [
    {"q": "A while loop whose condition never becomes false will:",
     "options": ["Stop after 100 passes", "Run forever",
                 "Raise an error immediately", "Skip its body"],
     "answer": 1,
     "why": "Nothing stops it but you. On this site the interpreter runs in a "
            "Web Worker and is killed after ten seconds, so the page survives "
            "the mistake."},
    {"q": "What does break do?",
     "options": ["Skips to the next pass", "Leaves the loop entirely",
                 "Restarts the loop", "Pauses execution"],
     "answer": 1,
     "why": "break exits the whole loop immediately. continue is the one that "
            "skips only the current pass."},
    {"q": "When is a while loop's condition checked?",
     "options": ["Before every pass", "After every pass", "Only once",
                 "Halfway through the body"],
     "answer": 0,
     "why": "It is tested before each pass, so a while loop whose condition "
            "starts false never runs its body at all."},
]},

"python/functions_and_return.html": {"check": [
    {"q": "A function that prints but never returns gives its caller:",
     "options": ["The printed value", "None", "An empty string", "An error"],
     "answer": 1,
     "why": "Printing puts characters on the screen; returning hands a value "
            "back. Without a return the call evaluates to None, which is why "
            "adding to the result raises TypeError."},
    {"q": "In `def area(width, height):`, width and height are:",
     "options": ["Arguments", "Parameters", "Return values", "Globals"],
     "answer": 1,
     "why": "The names in the def line are parameters. The values you pass "
            "when calling are the arguments."},
    {"q": "What does `def greet(name, greeting=\"Hello\")` let you do?",
     "options": ["Call greet with one argument", "Call greet with none",
                 "Return two values", "Skip the return"],
     "answer": 0,
     "why": "A default makes that parameter optional, so greet(\"Ada\") works "
            "and greet(\"Ada\", \"Hi\") overrides it."},
]},

"python/reading_errors.html": {"check": [
    {"q": "Which line of a traceback names the actual problem?",
     "options": ["The first", "The last", "The middle", "It varies"],
     "answer": 1,
     "why": "Read bottom-up. The last line is the error type and a "
            "plain-English description; the line above it points at your code."},
    {"q": "print(totl) when you meant total raises:",
     "options": ["TypeError", "ValueError", "NameError", "SyntaxError"],
     "answer": 2,
     "why": "NameError means Python has never seen that name. It is almost "
            "always a typo or a variable used before it was assigned."},
    {"q": "int(\"twelve\") raises ValueError rather than TypeError because:",
     "options": ["The type is wrong", "The type is right but the value is not",
                 "int takes no arguments", "Strings cannot be converted"],
     "answer": 1,
     "why": "int() accepts strings, so the type is fine - but \"twelve\" is "
            "not a string that represents a number. Right type, impossible "
            "value."},
]},

"gen_ai/parent_document_retriever.html": {"check": [
    {"q": "In a parent document retriever, what is actually indexed and scored?",
     "options": ["The whole parent documents", "The small child chunks",
                 "Both, separately", "Only the document titles"],
     "answer": 1,
     "why": "Children are indexed so the match is precise. The parent is what "
            "gets returned - the score decides WHICH document, the parent "
            "decides how much text the model sees."},
    {"q": "Two retrieved child chunks belong to the same parent. How many "
          "passages go to the model?",
     "options": ["One", "Two", "Three", "It depends on the scores"],
     "answer": 0,
     "why": "Parents are deduplicated. Without that, a document with three good "
            "chunks would be sent three times and burn the context window."},
    {"q": "Why not simply index large chunks instead?",
     "options": ["They are slower to embed", "The query terms get diluted",
                 "They cannot be embedded", "They break the tokenizer"],
     "answer": 1,
     "why": "A large chunk spreads the query's terms among hundreds of unrelated "
            "words, so its similarity score drops and it may not be retrieved at "
            "all - even though it holds the answer."},
]},

"gen_ai/multi_query_retriever.html": {"check": [
    {"q": "How are the results of the separate queries combined?",
     "options": ["Union, deduplicated", "Intersection", "Only the best query's "
                 "results are kept", "Averaged scores"],
     "answer": 0,
     "why": "Every document any phrasing found is kept. A document is missed "
            "only if EVERY phrasing misses it, which is the whole point."},
    {"q": "Multi-query retrieval mainly improves:",
     "options": ["Precision", "Recall", "Latency", "Index size"],
     "answer": 1,
     "why": "It trades a longer and noisier candidate list for a much lower "
            "chance of missing the right document - recall up, precision down, "
            "deliberately."},
    {"q": "Why is multi-query usually followed by reranking or MMR?",
     "options": ["To translate the query", "To clean up the larger, noisier list",
                 "To compress the documents", "To generate more queries"],
     "answer": 1,
     "why": "Raising recall pulls in irrelevant documents too. Something "
            "downstream has to reorder or diversify before the list reaches the "
            "model."},
]},

"gen_ai/self_query_retriever.html": {"check": [
    {"q": "Why can plain similarity search not honour \"published after 2020\"?",
     "options": ["Dates are not embeddable", "A cosine score has no notion of a "
                 "constraint", "The index is too small", "Years are stopwords"],
     "answer": 1,
     "why": "Embeddings compare meaning. The phrase is treated as more subject "
            "matter to match, not as a rule, so a 2017 paper about attention can "
            "still win."},
    {"q": "A self-query retriever splits the question into:",
     "options": ["Two semantic queries", "A semantic query and a metadata filter",
                 "Keywords and embeddings", "A question and an answer"],
     "answer": 1,
     "why": "One half is embedded and compared; the other becomes a structured "
            "predicate like year > 2020 that is executed against the metadata."},
    {"q": "In what order do the two halves run?",
     "options": ["Filter first, then rank the survivors",
                 "Rank first, then filter the top results",
                 "Both at once, scores averaged", "Whichever is faster"],
     "answer": 0,
     "why": "The filter removes documents that break the constraint, and "
            "similarity only ranks what survived. Filtering after ranking would "
            "let a top-k full of excluded documents leave nothing behind."},
]},

# =========================================================================
# Algorithms and data structures
#
# Every module on this track carries a runnable implementation of its own
# algorithm (tools/code_dsa.py). Where a question can be settled by reading
# or running that program rather than by recalling a sentence, it is written
# that way - a reader who has actually pressed Run should have an advantage
# over one who has only scrolled.
# =========================================================================

"dsa/linear_search.html": {"check": [
    {"q": "Linear search needs the data to be:",
     "options": ["Sorted", "Numeric", "Nothing in particular - any sequence",
                 "Stored in a hash table"],
     "answer": 2,
     "why": "It compares each item in turn, so it has no precondition at all. "
            "That is its one real advantage: every faster search buys its speed "
            "with an assumption about the data."},
    {"q": "The program prints an average of comparisons over every value in the "
          "list. What does it land on?",
     "options": ["n", "(n + 1) / 2", "log n", "n / 4"],
     "answer": 1,
     "why": "Finding item i takes i + 1 comparisons, and averaged over all "
            "positions that is (n + 1) / 2 - about half the list, which is where "
            "the usual rule of thumb comes from."},
    {"q": "Which case costs the full n comparisons?",
     "options": ["Only the last item", "Only a missing item",
                 "Both the last item and a missing item", "Neither"],
     "answer": 2,
     "why": "The loop only stops early on a hit. A miss has to rule out every "
            "element, so failure always costs the worst case."},
]},

"dsa/binary_search.html": {"check": [
    {"q": "Binary search on unsorted data:",
     "options": ["Raises an error", "Returns the wrong answer without complaining",
                 "Falls back to a linear scan", "Sorts the data first"],
     "answer": 1,
     "why": "Nothing checks the precondition. It compares against the middle, "
            "discards a half on the strength of that comparison, and returns "
            "something plausible - which is far more dangerous than a crash."},
    {"q": "Why is the midpoint written mid = lo + (hi - lo) // 2?",
     "options": ["It is faster", "It avoids overflow when lo + hi is large",
                 "It rounds differently", "It handles empty lists"],
     "answer": 1,
     "why": "Arithmetically identical to (lo + hi) // 2, but that form overflows "
            "in fixed-width integers. The bug lived in the JDK's binary search "
            "for nine years."},
    {"q": "Change hi = mid - 1 to hi = mid and run the program. What happens?",
     "options": ["It returns the wrong index", "It skips the last element",
                 "It loops forever and the interpreter kills it",
                 "Nothing - both are correct"],
     "answer": 2,
     "why": "mid has already been compared and ruled out. Leaving it in the "
            "window means a two-item window stops shrinking, so the loop never "
            "ends."},
]},

"dsa/interpolation_search.html": {"check": [
    {"q": "Interpolation search improves on binary search by:",
     "options": ["Sorting as it goes",
                 "Guessing where the target should be from its value",
                 "Checking both ends first", "Using a hash of the target"],
     "answer": 1,
     "why": "It interpolates a position from the value's distance between the "
            "endpoints, instead of always probing the middle. That one line is "
            "the whole difference."},
    {"q": "The program runs it on [1,2,3,4,5,6,7,8,9,5000] looking for 9. Why "
          "does it take so many steps?",
     "options": ["The list is too short", "9 is not in the list",
                 "The outlier flattens the estimate, so the probe advances one "
                 "index at a time",
                 "It has to sort first"],
     "answer": 2,
     "why": "The computed fraction is nearly zero because 5000 dominates the "
            "value range, so each probe lands next to the previous one and the "
            "search degenerates to O(n)."},
    {"q": "Its O(log log n) figure assumes the data is:",
     "options": ["Sorted only", "Sorted and roughly uniformly distributed",
                 "All positive", "In a contiguous array"],
     "answer": 1,
     "why": "Sortedness alone is not enough - the estimate is a straight-line "
            "guess, so it needs the values to rise at a roughly steady rate."},
]},

"dsa/fibonacci_search.html": {"check": [
    {"q": "What does Fibonacci search avoid that binary search needs?",
     "options": ["Sorted input", "Division", "Extra memory", "Comparisons"],
     "answer": 1,
     "why": "The split points come from adding and subtracting Fibonacci "
            "numbers, so no division or bit-shift is required. On hardware "
            "without cheap division that mattered."},
    {"q": "Its step count compared with binary search is:",
     "options": ["Much better", "About the same - both O(log n)",
                 "Much worse", "Depends on the target"],
     "answer": 1,
     "why": "Both are logarithmic and Fibonacci search is slightly worse by a "
            "constant. The win was never the step count."},
    {"q": "Why does the probe use min(offset + f2, n - 1)?",
     "options": ["To skip duplicates",
                 "Because the covering Fibonacci number overshoots the array",
                 "To keep the search stable", "To handle negative numbers"],
     "answer": 1,
     "why": "The sequence jumps 8, 13, 21 - it rarely equals the array length, "
            "so the first probe can point past the end and has to be clamped."},
]},

"dsa/bubble_sort.html": {"check": [
    {"q": "What does the swapped flag buy?",
     "options": ["Fewer swaps", "A best case of O(n) on sorted input",
                 "Stability", "Less memory"],
     "answer": 1,
     "why": "A pass with no swaps proves the list is sorted, so it stops. "
            "Without it, sorted input still costs the full n passes."},
    {"q": "Why does the inner loop run to n - 1 - i rather than n - 1?",
     "options": ["To avoid an index error",
                 "Because after pass i the last i items are already final",
                 "To keep it stable", "It makes it O(n)"],
     "answer": 1,
     "why": "Each pass carries the largest remaining value to the end, so that "
            "tail never needs looking at again. It saves comparisons, not "
            "complexity."},
    {"q": "The program's swap count for a given list equals:",
     "options": ["The number of items", "The number of passes",
                 "The number of inversions in the input", "n log n"],
     "answer": 2,
     "why": "Each swap fixes exactly one inverted pair, so the totals match "
            "exactly. That is why [1,2,3,4,5,0] is so expensive - one item out "
            "of place at the wrong end is five inversions."},
]},

"dsa/selection_sort.html": {"check": [
    {"q": "How many comparisons does selection sort make on an already sorted "
          "list of n items?",
     "options": ["n - 1", "About n log n", "The same n(n-1)/2 as always", "0"],
     "answer": 2,
     "why": "There is no early exit available: you cannot know an item is the "
            "minimum without checking every remaining one. The count is fixed by "
            "n alone."},
    {"q": "What selection sort is genuinely good at:",
     "options": ["Nearly sorted data", "Making at most n - 1 swaps",
                 "Being stable", "Large datasets"],
     "answer": 1,
     "why": "One swap per position, whatever the input. Where writes are "
            "expensive - flash memory, or records much larger than the key - "
            "that is a real advantage."},
    {"q": "Sorting [2, 2, 1] with this implementation:",
     "options": ["Keeps the two 2s in their original order",
                 "Swaps their order, so the sort is not stable",
                 "Raises an error", "Skips the duplicate"],
     "answer": 1,
     "why": "The first 2 is swapped with the 1 at the far end, jumping it past "
            "the second 2. Selection sort is not stable; insertion sort is."},
]},

"dsa/insertion_sort.html": {"check": [
    {"q": "Insertion sort's running time is driven by:",
     "options": ["The size of the list alone",
                 "How many inversions the input has",
                 "The largest value", "Whether the values are unique"],
     "answer": 1,
     "why": "Each shift fixes one inversion, so a nearly sorted list is nearly "
            "free. \"Nearly sorted\" is a measurable quantity here, not a vague "
            "description."},
    {"q": "Why does the inner loop shift items rather than swap them?",
     "options": ["Swapping would be wrong",
                 "A shift is one write instead of three",
                 "It keeps the sort stable", "It avoids recursion"],
     "answer": 1,
     "why": "The item being placed is held in key, so the hole can simply be "
            "moved. That constant-factor saving is why insertion sort beats "
            "bubble sort in practice."},
    {"q": "Real sort implementations switch to insertion sort for small "
          "partitions because:",
     "options": ["It is stable", "It uses no extra memory",
                 "Its constant factor is small, and big-O ignores constants",
                 "It is easier to write"],
     "answer": 2,
     "why": "At n around 16 the O(n²) with a tiny constant beats the O(n log n) "
            "with a heavier one. CPython's own sort does exactly this."},
]},

"dsa/merge_sort.html": {"check": [
    {"q": "Where does the actual sorting happen in merge sort?",
     "options": ["In the split", "In the merge",
                 "In the base case", "In the recursion"],
     "answer": 1,
     "why": "Splitting a list in half is positional and does no comparing. All "
            "the ordering work is in combining two sorted halves."},
    {"q": "In merge, why is the comparison left[i] <= right[j] rather than < ?",
     "options": ["It is faster", "It keeps the sort stable",
                 "It avoids an index error", "It handles empty lists"],
     "answer": 1,
     "why": "On a tie the left half wins, and the left half held the earlier "
            "items. Changing it to < breaks stability silently, with no other "
            "visible symptom."},
    {"q": "Merge sort's worst case compared with its best case:",
     "options": ["Much worse", "Slightly worse",
                 "The same - O(n log n) either way", "Depends on the pivot"],
     "answer": 2,
     "why": "It has no pivot to choose badly and no early exit to hit. That "
            "predictability is exactly why it is used where worst-case latency "
            "matters."},
]},

"dsa/quick_sort.html": {"check": [
    {"q": "With a last-element pivot, which input is quicksort's worst case?",
     "options": ["Random data", "Already sorted data",
                 "Data with duplicates", "Very short lists"],
     "answer": 1,
     "why": "Each partition peels off one element instead of halving, so the "
            "recursion goes n deep. The program prints depth 8 for a sorted "
            "9-item list against 4 for a shuffled one."},
    {"q": "After partition returns p, why do the recursive calls skip index p?",
     "options": ["To save a comparison",
                 "The pivot is already in its final sorted position",
                 "To keep the sort stable", "To avoid infinite recursion"],
     "answer": 1,
     "why": "Everything left of p is smaller and everything right is larger, so "
            "p cannot move again. That is the one guaranteed piece of progress "
            "each partition makes."},
    {"q": "Quicksort's advantage over merge sort is mainly:",
     "options": ["Better worst case", "Stability",
                 "It sorts in place, needing O(log n) extra space rather than O(n)",
                 "Fewer comparisons"],
     "answer": 2,
     "why": "Its worst case is worse and it is not stable. The memory profile, "
            "plus good cache behaviour, is what keeps it in use."},
]},

"dsa/heap_sort.html": {"check": [
    {"q": "After the heapify phase, the list is:",
     "options": ["Sorted", "Reverse sorted",
                 "A valid heap, which is a much weaker ordering than sorted",
                 "Unchanged"],
     "answer": 2,
     "why": "A heap only promises each parent beats its children. Nothing is "
            "claimed about siblings - and that weakness is why it can be built "
            "in O(n)."},
    {"q": "Building the heap bottom-up, starting at the last parent, costs:",
     "options": ["O(n log n)", "O(n)", "O(log n)", "O(n²)"],
     "answer": 1,
     "why": "Most nodes are near the leaves and sift down barely at all. The "
            "sum works out linear, which surprises people who expect n sifts of "
            "log n each."},
    {"q": "Why does the extraction phase swap the root with the last item?",
     "options": ["To keep the sort stable",
                 "It both removes the maximum and puts it in its final position, "
                 "with no extra memory",
                 "To rebalance the tree", "To avoid recursion"],
     "answer": 1,
     "why": "One swap does both jobs, which is how heap sort sorts in place. "
            "The heap then shrinks by one and is repaired with a single sift."},
]},

"dsa/counting_sort.html": {"check": [
    {"q": "How does counting sort beat the O(n log n) lower bound?",
     "options": ["It is parallel", "It never compares two elements",
                 "It uses more memory", "It only works on small lists"],
     "answer": 1,
     "why": "The bound applies to comparison sorts. Counting sort uses the value "
            "as an array index, so the proof simply does not cover it."},
    {"q": "Why does the final loop iterate over reversed(a)?",
     "options": ["It is faster", "To keep the sort stable",
                 "To handle negatives", "To avoid an off-by-one"],
     "answer": 1,
     "why": "Walking backwards while decrementing before writing keeps equal "
            "items in their original order. Radix sort depends on that, so "
            "getting it wrong breaks the algorithm built on top."},
    {"q": "The program sorts [5, 100000, 3]. What is the problem?",
     "options": ["The list is too short", "The values are too far apart, so k "
                 "dwarfs n",
                 "It is not sorted first", "Counting sort cannot handle 100000"],
     "answer": 1,
     "why": "O(n + k) is linear only when k is comparable to n. Three items and "
            "a hundred thousand counters is the case that makes the cost "
            "obvious."},
]},

"dsa/radix_sort.html": {"check": [
    {"q": "Why must each digit pass be stable?",
     "options": ["To keep it fast", "Otherwise the previous pass's ordering is "
                 "destroyed",
                 "To handle negative numbers", "It does not have to be"],
     "answer": 1,
     "why": "Sorting by tens must preserve the ones ordering among items with "
            "equal tens digits. An unstable pass silently produces a wrong "
            "final answer."},
    {"q": "Radix sort's cost is O(d · n), where d is:",
     "options": ["The number of items", "The number of digits in the largest value",
                 "The number of distinct values", "log n"],
     "answer": 1,
     "why": "One pass per digit position, each pass linear in n. Adding a single "
            "very wide value adds passes over the entire list."},
    {"q": "After only the ones-digit pass, the list:",
     "options": ["Is sorted", "Is sorted by last digit and otherwise scrambled",
                 "Is unchanged", "Is reverse sorted"],
     "answer": 1,
     "why": "Every intermediate state looks broken, which is what makes LSD "
            "radix sort hard to debug by eye. Only the final pass makes it "
            "correct."},
]},

"dsa/graph_representations.html": {"check": [
    {"q": "For a sparse graph, an adjacency matrix wastes space because it "
          "stores:",
     "options": ["Every node twice", "V² cells regardless of how many edges exist",
                 "The edge weights", "A copy of each edge list"],
     "answer": 1,
     "why": "The grid is allocated up front. A million users with a few hundred "
            "million friendships would need 10¹² cells to hold them."},
    {"q": "\"Is there an edge between A and D?\" is answered fastest by:",
     "options": ["An adjacency list", "An adjacency matrix",
                 "An edge list", "All three are the same"],
     "answer": 1,
     "why": "One indexed read. The list has to scan A's neighbours and the edge "
            "list has to scan everything."},
    {"q": "BFS, DFS and Dijkstra all assume an adjacency list because they ask:",
     "options": ["\"Are these two connected?\"",
                 "\"Who does this node reach?\"",
                 "\"How many edges are there?\"", "\"Is the graph directed?\""],
     "answer": 1,
     "why": "Traversals iterate a node's neighbours, which a list returns "
            "directly and a matrix only finds by scanning a whole row of V "
            "cells."},
]},

"dsa/breadth_first_search.html": {"check": [
    {"q": "Turning BFS into DFS requires changing:",
     "options": ["The visited set", "popleft() to pop() - the container",
                 "The graph representation", "The order of the neighbour list"],
     "answer": 1,
     "why": "FIFO gives breadth-first, LIFO gives depth-first. The rest of the "
            "loop is identical, which is the clearest way to see that the "
            "container is the algorithm."},
    {"q": "Why does the code mark a node visited when it is enqueued rather "
          "than when it is dequeued?",
     "options": ["It is tidier", "Otherwise a node with several neighbours "
                 "already queued gets added more than once",
                 "To keep distances correct", "To detect cycles"],
     "answer": 1,
     "why": "Marking late lets the same node be queued repeatedly before it is "
            "ever processed, which blows up the queue on dense graphs."},
    {"q": "BFS gives shortest paths on an unweighted graph because:",
     "options": ["It uses a priority queue",
                 "Nodes are dequeued in order of distance, so the first arrival "
                 "is by a shortest path",
                 "It visits every node", "It sorts the neighbours"],
     "answer": 1,
     "why": "The frontier expands one full level at a time. On weighted graphs "
            "that no longer holds and you need Dijkstra."},
]},

"dsa/depth_first_search.html": {"check": [
    {"q": "Without the visited set, DFS on a graph containing a cycle:",
     "options": ["Returns the wrong order", "Recurses forever",
                 "Skips some nodes", "Works fine"],
     "answer": 1,
     "why": "A graph is not a tree. The visited set is the only thing that "
            "terminates the traversal - the program adds a G to A edge to "
            "demonstrate exactly this."},
    {"q": "Why does the iterative version also check 'if node in visited' after "
          "popping?",
     "options": ["To avoid infinite loops",
                 "A node can be pushed by several neighbours before it is popped",
                 "To match the recursive order", "To count the nodes"],
     "answer": 1,
     "why": "Duplicates on the stack are harmless but wasteful; without the "
            "check the same node is expanded twice."},
    {"q": "Work that belongs on the \"leave\" line - after the recursive calls "
          "return - includes:",
     "options": ["Marking visited", "Printing the node",
                 "Topological ordering and subtree sizes", "Choosing the start"],
     "answer": 2,
     "why": "Post-order work needs the whole subtree already processed. "
            "Topological sort by DFS is exactly this, reversed."},
]},

"dsa/dijkstras.html": {"check": [
    {"q": "With one negative edge, Dijkstra:",
     "options": ["Raises an error", "Loops forever",
                 "Returns a wrong answer without complaining", "Still works"],
     "answer": 2,
     "why": "The program finalises C at 2, then discovers a route through B "
            "worth -2 and never revisits it. Correctness rests on no edge ever "
            "making a finalised node cheaper."},
    {"q": "Why does the code push a new heap entry instead of updating an "
          "existing one?",
     "options": ["It is more accurate", "heapq cannot decrease a key in place, "
                 "so stale entries are skipped when popped",
                 "To keep the heap sorted", "To count relaxations"],
     "answer": 1,
     "why": "Lazy deletion: cheaper and far easier to get right than a "
            "decrease-key structure, at the cost of a heap larger than the node "
            "count."},
    {"q": "Replacing the heap with a linear scan for the nearest node gives:",
     "options": ["Wrong answers", "The same answers at O(V²) instead of "
                 "O(E log V)",
                 "A faster algorithm", "Bellman-Ford"],
     "answer": 1,
     "why": "The heap is an accelerator, not part of the logic. On a dense "
            "graph the O(V²) version is actually competitive."},
]},

"dsa/bellman_ford.html": {"check": [
    {"q": "Why exactly V - 1 rounds?",
     "options": ["It is a safety margin",
                 "A shortest path visits each node once, so it has at most V - 1 "
                 "edges",
                 "It matches the edge count", "To detect cycles"],
     "answer": 1,
     "why": "Each round settles at least one more edge of any shortest path, so "
            "V - 1 rounds is enough and one more would be wasted."},
    {"q": "How does the algorithm detect a negative cycle?",
     "options": ["It counts the edges", "It checks for negative weights up front",
                 "One extra relaxation round still improves something",
                 "The distances go to negative infinity"],
     "answer": 2,
     "why": "After V - 1 rounds the distances are final if they exist. A further "
            "improvement proves you can keep going round and getting cheaper, so "
            "no shortest path exists."},
    {"q": "Compared with Dijkstra, Bellman-Ford is:",
     "options": ["Faster and more general", "Slower but handles negative weights",
                 "Faster but needs sorted edges", "The same algorithm"],
     "answer": 1,
     "why": "O(V·E) against O(E log V). You pay for the generality, which is why "
            "Dijkstra remains the default when weights are non-negative."},
]},

"dsa/a_star.html": {"check": [
    {"q": "Setting the heuristic to zero turns A* into:",
     "options": ["BFS", "Dijkstra", "Greedy best-first search", "DFS"],
     "answer": 1,
     "why": "f = g + h collapses to f = g, which is Dijkstra's priority exactly. "
            "The program runs the identical function both ways to show it."},
    {"q": "An admissible heuristic is one that:",
     "options": ["Is fast to compute", "Never overestimates the remaining cost",
                 "Is always exact", "Ignores obstacles"],
     "answer": 1,
     "why": "Overestimating lets A* commit to a route before a cheaper one is "
            "examined, so the path it returns can be longer than the shortest."},
    {"q": "Both searches in the program return a path of the same length. What "
          "differs?",
     "options": ["The path itself", "The number of cells expanded",
                 "The memory used", "Nothing"],
     "answer": 1,
     "why": "136 cells against 90 on this grid. A* is not more correct - it is "
            "the same answer reached without looking away from the goal."},
]},

"dsa/topological_sort.html": {"check": [
    {"q": "Kahn's algorithm starts from the nodes whose in-degree is:",
     "options": ["Highest", "Zero", "One", "Equal to their out-degree"],
     "answer": 1,
     "why": "In-degree zero means nothing has to happen first, so those can be "
            "taken immediately - and in any order among themselves."},
    {"q": "The program detects a cycle by noticing that:",
     "options": ["A node repeats", "The output is shorter than the node count",
                 "The queue empties", "An in-degree goes negative"],
     "answer": 1,
     "why": "Nodes in a cycle wait on each other forever, so their in-degree "
            "never reaches zero and they never enter the queue. The short output "
            "is the detection - it costs nothing extra."},
    {"q": "A directed acyclic graph has:",
     "options": ["Exactly one topological order",
                 "Usually many valid topological orders",
                 "None unless it is a tree", "One per starting node"],
     "answer": 1,
     "why": "Swapping popleft() for pop() produces a different, equally correct "
            "order. Where a specific one is needed, a heap gives the "
            "lexicographically smallest."},
]},

"dsa/cycle_detection.html": {"check": [
    {"q": "Floyd's tortoise and hare uses how much extra memory?",
     "options": ["O(n) for a visited set", "O(log n)", "O(1) - two pointers",
                 "O(n) for the path"],
     "answer": 2,
     "why": "That is the entire point of it. A visited set also works and is "
            "easier, but it costs memory proportional to the list."},
    {"q": "Why does the comparison use 'slow is fast' rather than '==' ?",
     "options": ["It is faster", "Two different nodes holding equal values would "
                 "fool ==",
                 "== does not work on objects", "To avoid a type error"],
     "answer": 1,
     "why": "The question is whether the two pointers are on the same node, "
            "which is identity, not equality of contents."},
    {"q": "Why does directed-graph cycle detection need three colours rather "
          "than a plain visited set?",
     "options": ["To find the cycle's length",
                 "Because reaching an already-finished node is fine, while "
                 "reaching one still on the current path is a cycle",
                 "To handle disconnected graphs", "To make it iterative"],
     "answer": 1,
     "why": "With two states, any diamond shape - two paths meeting at one node - "
            "is reported as a cycle. GREY versus BLACK is what distinguishes "
            "them."},
]},

"dsa/minimum_spanning_tree.html": {"check": [
    {"q": "A spanning tree of a graph with V nodes always has:",
     "options": ["V edges", "V - 1 edges", "E - V edges", "As few as possible"],
     "answer": 1,
     "why": "Exactly enough to connect everything with no cycle. Both Kruskal "
            "and Prim stop at that count in the program."},
    {"q": "The difference between Kruskal and Prim is that Kruskal:",
     "options": ["Is faster", "Sorts all edges globally, while Prim only "
                 "considers edges leaving the tree it has grown",
                 "Handles negative weights", "Needs a starting node"],
     "answer": 1,
     "why": "Kruskal works from a global sort and needs union-find to reject "
            "cycles; Prim grows locally from one node with a priority queue."},
    {"q": "Kruskal uses union-find to:",
     "options": ["Sort the edges", "Track the tree's weight",
                 "Check in near-constant time whether an edge would close a cycle",
                 "Find the starting node"],
     "answer": 2,
     "why": "Both endpoints already in the same component means the edge adds "
            "only a cycle. Without union-find that check would need a traversal "
            "per edge."},
]},

"dsa/union_find.html": {"check": [
    {"q": "What does path compression do?",
     "options": ["Removes duplicate elements",
                 "Re-points every node touched on the way up straight at the root",
                 "Merges the two smallest trees", "Sorts the parent array"],
     "answer": 1,
     "why": "The walk pays for the next walk. Every node on the path becomes one "
            "hop from the root, so repeat queries are effectively free."},
    {"q": "Union by rank exists to prevent:",
     "options": ["Duplicate unions", "Trees degenerating into long chains",
                 "Cycles", "Memory growth"],
     "answer": 1,
     "why": "Attaching blindly, as the naive version does, builds a linked list "
            "wearing a tree's name - and find degrades to O(n), which the "
            "program's hop counts show directly."},
    {"q": "With both optimisations, the amortised cost per operation is:",
     "options": ["O(log n)", "O(1) exactly",
                 "O(α(n)), which is below 5 for any real n", "O(n)"],
     "answer": 2,
     "why": "The inverse Ackermann function grows so slowly that it is a "
            "constant for practical purposes - but it is not literally O(1)."},
]},

"dsa/stacks.html": {"check": [
    {"q": "Why does the balanced-brackets check test that the stack is empty at "
          "the end?",
     "options": ["To free memory", "To catch openers that were never closed",
                 "To reset for the next call", "It is not necessary"],
     "answer": 1,
     "why": "\"((()\" has every closer matched and is still unbalanced. Without "
            "the final check it passes."},
    {"q": "In the postfix evaluator, why is it 'b, a = stack.pop(), stack.pop()' "
          "in that order?",
     "options": ["It reads better", "The second operand was pushed last, so it "
                 "comes off first",
                 "To avoid an index error", "The order does not matter"],
     "answer": 1,
     "why": "Swap the names and + and * still look right while - and / silently "
            "invert - the worst kind of bug to find."},
    {"q": "A stack built on a Python list uses append and pop with no index "
          "because:",
     "options": ["It is more readable", "Both act on the end, so both are O(1)",
                 "pop(0) is not allowed", "It keeps the order correct"],
     "answer": 1,
     "why": "insert(0, x) and pop(0) shift every other element. Same stack, every "
            "operation turned into O(n)."},
]},

"dsa/queues.html": {"check": [
    {"q": "Why is a queue built on list.pop(0) slow?",
     "options": ["Lists cannot grow", "Removing the first item shifts every "
                 "remaining item one place left",
                 "It copies the list", "It is not slow"],
     "answer": 1,
     "why": "O(n) per dequeue, so O(n²) to drain the queue. The program times "
            "30,000 dequeues both ways."},
    {"q": "collections.deque gives O(1) at both ends because it is:",
     "options": ["A sorted array", "A doubly linked list of blocks",
                 "A hash table", "A binary heap"],
     "answer": 1,
     "why": "There is no contiguous array to shift, so appending or popping at "
            "either end is a pointer update."},
    {"q": "A circular buffer must track its size separately because:",
     "options": ["It grows", "Head meeting tail is ambiguous between full and "
                 "empty",
                 "The modulo is expensive", "It stores None"],
     "answer": 1,
     "why": "Both states have head == tail. Getting this wrong silently "
            "overwrites the oldest entry."},
]},

"dsa/linked_lists.html": {"check": [
    {"q": "In reverse(), why is 'nxt = node.next' saved before 'node.next = "
          "prev'?",
     "options": ["For readability", "Otherwise the rest of the list becomes "
                 "unreachable",
                 "To count the nodes", "To handle the empty list"],
     "answer": 1,
     "why": "Overwriting the only pointer to the remainder loses it - not "
            "corrupted, just gone. Delete the line and the list comes back one "
            "node long."},
    {"q": "What is the dummy head in delete() for?",
     "options": ["Marking the end", "Removing the special case of deleting the "
                 "first node",
                 "Counting nodes", "Making it doubly linked"],
     "answer": 1,
     "why": "Without a previous node to re-point, deleting the head needs its own "
            "branch - and that branch is where the bug always is."},
    {"q": "Compared with a Python list, a linked list is better at:",
     "options": ["Random access", "Inserting at the front",
                 "Memory use", "Cache behaviour"],
     "answer": 1,
     "why": "O(1) with no shifting. It loses on everything else, including "
            "sequential scans, because the nodes are scattered in memory."},
]},

"dsa/hash_tables.html": {"check": [
    {"q": "The program replaces the hash function with 'lambda k: 1'. What "
          "happens?",
     "options": ["It raises an error", "Keys are lost",
                 "Everything lands in one bucket and every lookup becomes O(n)",
                 "It gets faster"],
     "answer": 2,
     "why": "The structure still works perfectly and every guarantee evaporates. "
            "O(1) was always conditional on the hash spreading keys out."},
    {"q": "Why does a resize have to rehash every key?",
     "options": ["The hashes change", "The index is hash % size, and size just "
                 "changed",
                 "To keep insertion order", "To free memory"],
     "answer": 1,
     "why": "The hash is stable; the fold into a bucket index is not. Doubling "
            "the table moves nearly everything."},
    {"q": "The load factor threshold exists because:",
     "options": ["Memory is limited", "Collisions rise sharply as the table "
                 "fills, so it grows before that happens",
                 "Python requires it", "It keeps buckets sorted"],
     "answer": 1,
     "why": "Past about three-quarters full the chains get long fast. Resizing "
            "is O(n), but amortised over the inserts that caused it it is O(1) "
            "each."},
]},

"dsa/binary_search_trees.html": {"check": [
    {"q": "Inserting sorted keys into a plain BST produces:",
     "options": ["A balanced tree", "A tree of height n - effectively a linked "
                 "list",
                 "An error", "A heap"],
     "answer": 1,
     "why": "Every key goes right, so the tree is one spine and search degrades "
            "to O(n). The program prints height 7 for seven sorted keys."},
    {"q": "An in-order traversal of a BST emits the keys:",
     "options": ["In insertion order", "In sorted order",
                 "Level by level", "In reverse"],
     "answer": 1,
     "why": "Left, self, right. It comes out sorted for free, without sorting "
            "anything - which is the structure's whole selling point over a hash "
            "table."},
    {"q": "Deleting a node with two children works by:",
     "options": ["Deleting both subtrees",
                 "Copying up the in-order successor and deleting that instead",
                 "Rotating the tree", "Marking it deleted"],
     "answer": 1,
     "why": "The leftmost node of the right subtree has at most one child, so "
            "the hard case reduces to an easy one."},
]},

"dsa/heaps_and_priority_queues.html": {"check": [
    {"q": "In an array-backed heap, the children of index i are at:",
     "options": ["i-1 and i+1", "2i+1 and 2i+2", "i/2 and i/2+1", "0 and n-1"],
     "answer": 1,
     "why": "The tree is arithmetic, not structure. No node objects and no "
            "pointers are stored at all."},
    {"q": "After several pushes, the underlying list is:",
     "options": ["Sorted", "Sorted except the last item",
                 "Only guaranteed to have the smallest item at index 0",
                 "In insertion order"],
     "answer": 2,
     "why": "A heap promises each parent beats its children and nothing about "
            "siblings. Expecting more is the usual misunderstanding."},
    {"q": "heapq.nlargest(k, data) is O(n log k) rather than O(n log n) because "
          "it:",
     "options": ["Sorts first", "Keeps a heap of only k items",
                 "Uses C code", "Samples the data"],
     "answer": 1,
     "why": "For \"top 10 of a billion\" that is the difference between "
            "practical and not."},
]},

"dsa/trie_prefix_tree.html": {"check": [
    {"q": "What does the is_word flag distinguish?",
     "options": ["Leaves from internal nodes",
                 "\"ca\", which is only a prefix, from \"do\", which is a stored "
                 "word with more beyond it",
                 "Uppercase from lowercase", "Full from partial branches"],
     "answer": 1,
     "why": "Without it a trie can only answer prefix questions - and \"do\" "
            "being a word while \"dog\" continues past it has nothing to do with "
            "being a leaf."},
    {"q": "Trie lookup costs O(length of the word) because:",
     "options": ["The words are sorted",
                 "It walks one node per character, and the number of stored "
                 "words never enters into it",
                 "Hashing is O(1)", "It is a balanced tree"],
     "answer": 1,
     "why": "A million stored words cost the same as ten. A hash table is also "
            "roughly O(length), because it must hash the whole string."},
    {"q": "The operation a hash table cannot do at all is:",
     "options": ["Exact lookup", "Insert", "List everything starting with \"car\"",
                 "Delete"],
     "answer": 2,
     "why": "Hashing destroys the relationship between \"car\" and \"card\". "
            "Autocomplete is a DFS from the prefix node, which needs the shared "
            "structure a trie keeps."},
]},

"dsa/recursion_and_call_stack.html": {"check": [
    {"q": "What does a stack frame hold?",
     "options": ["The function's source",
                 "Its arguments, its locals and where to return to",
                 "The whole call tree", "Only the return value"],
     "answer": 1,
     "why": "That is why recursion depth is a memory cost: a thousand pending "
            "calls means a thousand of these alive at once."},
    {"q": "In 'return n * factorial(n - 1)', why can the frame not be discarded "
          "at the recursive call?",
     "options": ["Python does not support it",
                 "The multiplication still has to happen after the call returns",
                 "The argument might change", "It is discarded"],
     "answer": 1,
     "why": "Pending work after the call is exactly what keeps a frame alive. "
            "Writing it so the call is the last thing done is tail recursion - "
            "which CPython still will not optimise away."},
    {"q": "The program prints call counts for naive fib. What is the shape?",
     "options": ["Linear in n", "Roughly doubling for each +1 in n",
                 "n log n", "Constant"],
     "answer": 1,
     "why": "177 calls for fib(10) and 242,785 for fib(25). Recursion is not "
            "slow; recursion that recomputes the same subproblems is."},
]},

"dsa/dynamic_programming.html": {"check": [
    {"q": "Dynamic programming needs subproblems that:",
     "options": ["Are independent", "Overlap, so an answer is reused many times",
                 "Are all the same size", "Can be sorted"],
     "answer": 1,
     "why": "If each subproblem were needed once, a table would buy nothing over "
            "plain recursion. The reuse is what pays for the storage."},
    {"q": "Top-down memoisation and bottom-up tabulation differ in that "
          "tabulation:",
     "options": ["Gives different answers", "Is always faster",
                 "Fills the small cases first and uses no call stack",
                 "Needs less memory"],
     "answer": 2,
     "why": "Same complexity, no recursion limit, and usually a better constant. "
            "Memoisation is normally the easier one to write, because the code "
            "still mirrors the recurrence."},
    {"q": "For coins [1, 3, 4] and target 6, greedy takes 4+1+1. What does the "
          "DP table give?",
     "options": ["The same 3 coins", "2 coins - two 3s",
                 "4 coins", "It cannot be made"],
     "answer": 1,
     "why": "The table computes every amount up to the target, so it finds the "
            "combination greedy's one-way choice never considers."},
]},

"dsa/greedy_algorithms.html": {"check": [
    {"q": "Greedy coin change works for [1, 5, 10, 25] but fails for [1, 3, 4]. "
          "What does that show?",
     "options": ["Greedy never works",
                 "Correctness depends on the denominations, not on the algorithm",
                 "The coins must be sorted", "It only fails on small targets"],
     "answer": 1,
     "why": "Familiarity with real currency is why people assume greedy is "
            "generally optimal. Nothing about the code changed - only the input."},
    {"q": "Activity selection is provably optimal when the meetings are sorted "
          "by:",
     "options": ["Start time", "Finish time", "Duration", "Number of attendees"],
     "answer": 1,
     "why": "Taking the meeting that frees the room earliest can never shut out "
            "a better schedule. Sorted by start time, one long early meeting "
            "blocks several short ones."},
    {"q": "The practical way to test a greedy idea is to:",
     "options": ["Prove it formally first", "Compare it with brute force on "
                 "small inputs",
                 "Try it on the largest case", "Check the complexity"],
     "answer": 1,
     "why": "The program runs a DP check alongside so the verdict is computed "
            "rather than asserted. A counterexample is usually small when it "
            "exists at all."},
]},

"dsa/divide_and_conquer.html": {"check": [
    {"q": "Why does exponentiation by squaring make ONE recursive call and reuse "
          "the result?",
     "options": ["It is tidier", "Two calls would recompute the same value and "
                 "lose the entire saving",
                 "It avoids overflow", "Python requires it"],
     "answer": 1,
     "why": "power(b, n//2) * power(b, n//2) looks identical and is exponentially "
            "slower. The saving is in reusing the value, not in the halving."},
    {"q": "Counting inversions during a merge is O(n log n) because, when an "
          "item from the right half wins:",
     "options": ["It is discarded", "Every remaining item on the left is counted "
                 "in one addition",
                 "The halves are swapped", "The count is estimated"],
     "answer": 1,
     "why": "The left half is sorted, so all of its remainder is greater. "
            "Counting in blocks rather than pairs is the whole trick."},
    {"q": "Divide and conquer proves its answer complete by showing every case "
          "falls into:",
     "options": ["The base case", "Left, right, or across the split",
                 "A sorted region", "One recursive call"],
     "answer": 1,
     "why": "Every inversion is within one half or spans both, and never "
            "anything else. That decomposition is the pattern in general, not "
            "just here."},
]},

"dsa/backtracking.html": {"check": [
    {"q": "What is the 'backtrack' in the N-queens program?",
     "options": ["The recursive call", "queens.pop() - undoing the placement",
                 "The safe() check", "Returning the solution"],
     "answer": 1,
     "why": "Place, explore, undo. Delete the pop and the state leaks into "
            "sibling branches, so the search finds nothing while looking like an "
            "optimisation."},
    {"q": "Why is state stored as one column per row rather than as a board?",
     "options": ["It is smaller", "It makes 'two queens in the same row' "
                 "impossible by construction",
                 "It is faster to print", "The board would be too large"],
     "answer": 1,
     "why": "Encoding removes an entire class of conflict for free, and the "
            "recursion depth becomes the row being filled."},
    {"q": "Backtracking beats brute force because it:",
     "options": ["Is not exponential",
                 "Abandons a partial placement before generating any of its "
                 "completions",
                 "Uses less memory", "Checks solutions in a better order"],
     "answer": 1,
     "why": "It is still exponential in the worst case, just over a far smaller "
            "space - the program prints the percentage of positions pruned."},
]},

"dsa/two_pointers.html": {"check": [
    {"q": "Pair-sum with two pointers requires the list to be:",
     "options": ["Unique", "Sorted", "Positive", "Even length"],
     "answer": 1,
     "why": "Moving a pointer is only justified because sortedness proves the "
            "discarded element cannot be part of any solution. Shuffle the input "
            "and it returns None for a pair that exists."},
    {"q": "When the sum is too small, why is it safe to move lo right rather "
          "than hi left?",
     "options": ["It is arbitrary", "a[hi] is the largest available partner, so "
                 "a[lo] cannot work with anything",
                 "It keeps the loop terminating", "hi might be negative"],
     "answer": 1,
     "why": "Each step eliminates a whole row or column of the pair table, which "
            "is how n² candidates are covered in n steps."},
    {"q": "In the in-place dedupe, why does the function return a length instead "
          "of a list?",
     "options": ["It is faster", "Nothing was reallocated, so the tail still "
                 "holds stale data",
                 "The list is sorted", "To avoid copying"],
     "answer": 1,
     "why": "The point of the technique is O(1) extra memory. The caller uses "
            "a[:n] and ignores whatever is past it."},
]},

"dsa/sliding_window.html": {"check": [
    {"q": "The fixed-size window updates its sum with one line. Which?",
     "options": ["total = sum(window)", "total += a[i] - a[i - k]",
                 "total = max(total, a[i])", "total *= 2"],
     "answer": 1,
     "why": "Add what entered, subtract what left. Carrying the value forward "
            "instead of rebuilding it is what turns O(n·k) into O(n)."},
    {"q": "In the longest-unique-substring window, why is the check 'ch in seen "
          "and seen[ch] >= start' rather than just 'ch in seen'?",
     "options": ["To handle the first character",
                 "An earlier occurrence may already have fallen off the left edge",
                 "To count repeats", "To keep it O(n)"],
     "answer": 1,
     "why": "Only a repeat inside the current window matters. Drop the second "
            "condition and \"abba\" gives the wrong answer."},
    {"q": "Storing the last index of each character rather than a count lets the "
          "left edge:",
     "options": ["Move backwards", "Jump straight past the previous occurrence",
                 "Stay fixed", "Be recomputed"],
     "answer": 1,
     "why": "Both approaches are correct; jumping keeps the scan clearly linear "
            "and the code short."},
]},

"dsa/kmp_string_matching.html": {"check": [
    {"q": "What does lps[i] store?",
     "options": ["The character at i",
                 "The length of the longest proper prefix of pattern[:i+1] that "
                 "is also its suffix",
                 "The number of matches so far", "The next index to check"],
     "answer": 1,
     "why": "That overlap is the only information needed to know how far the "
            "pattern may safely slide after a mismatch."},
    {"q": "In the search loop, what never happens?",
     "options": ["j decreases", "i decreases", "The pattern slides", "A hit"],
     "answer": 1,
     "why": "The text index only moves forward, which is the O(n + m) guarantee. "
            "Naive matching restarts at i - j + 1 and re-reads characters."},
    {"q": "After a full match, the code sets j = lps[j - 1] rather than 0. Why?",
     "options": ["To reset faster", "To find overlapping occurrences",
                 "To avoid an index error", "To count the matches"],
     "answer": 1,
     "why": "Set it to 0 and searching \"aa\" in \"aaaa\" reports fewer matches "
            "than there are."},
]},

"dsa/lists_in_python.html": {"check": [
    {"q": "Indexing a Python list is O(1) because the list stores:",
     "options": ["A hash of each item", "References contiguously, so the address "
                 "is computed",
                 "The items in sorted order", "A linked chain of nodes"],
     "answer": 1,
     "why": "One multiplication and one read. This is the whole difference "
            "between a list and a linked list."},
    {"q": "What does [[0] * 3] * 3 build?",
     "options": ["A 3x3 grid of independent rows",
                 "Three references to one row, so writing to one writes to all",
                 "A flat list of nine zeros", "An error"],
     "answer": 1,
     "why": "Multiplying repeats the reference, not the object. This is the most "
            "common Python bug in grid and matrix code."},
    {"q": "sys.getsizeof shows a list's size jumping in steps rather than per "
          "item because:",
     "options": ["The report is approximate", "CPython over-allocates on growth "
                 "so most appends need no reallocation",
                 "Items vary in size", "Small lists are cached"],
     "answer": 1,
     "why": "That is what \"amortised O(1) append\" means concretely: most "
            "appends are free, and occasionally one pays for a copy."},
]},

"dsa/dictionaries_in_python.html": {"check": [
    {"q": "Why must dictionary keys be hashable?",
     "options": ["To keep them sorted", "Because a key that changed after "
                 "insertion would no longer hash to the slot it lives in",
                 "To save memory", "To allow duplicates"],
     "answer": 1,
     "why": "It would become unreachable. In practice this means immutable: "
            "tuples work as keys, lists do not."},
    {"q": "{1: 'a', 1.0: 'b', True: 'c'} produces a dict with how many entries?",
     "options": ["3", "2", "1", "It raises an error"],
     "answer": 2,
     "why": "1 == 1.0 == True and all three hash identically, so each assignment "
            "overwrites the previous value while the first key object stays."},
    {"q": "Replacing 'x in a_big_list' with 'x in a_big_set' changes the cost "
          "from:",
     "options": ["O(1) to O(n)", "O(n) to roughly O(1)",
                 "O(log n) to O(1)", "Nothing changes"],
     "answer": 1,
     "why": "The list compares against every element; the hash table computes "
            "where the answer would be. It is the highest-value one-line "
            "optimisation in most beginner Python."},
]},

"dsa/strings_in_python.html": {"check": [
    {"q": "Building a string by += in a loop is O(n²) because each step:",
     "options": ["Reallocates the list", "Allocates a new string and copies "
                 "everything so far",
                 "Re-encodes to UTF-8", "Sorts the characters"],
     "answer": 1,
     "why": "Strings are immutable, so there is nothing to append to. "
            "\"\".join(parts) does one length calculation, one allocation and "
            "one copy."},
    {"q": "The program accumulates into an object attribute rather than a local "
          "variable. Why?",
     "options": ["It is more realistic", "CPython has an in-place resize "
                 "special case for locals that would hide the quadratic",
                 "Locals are faster", "To avoid a NameError"],
     "answer": 1,
     "why": "The optimisation only fires under specific conditions and varies by "
            "build - which is itself the argument for using join rather than "
            "relying on it."},
    {"q": "Immutability is also what allows strings to be:",
     "options": ["Sliced", "Used as dictionary keys", "Concatenated", "Iterated"],
     "answer": 1,
     "why": "Hashability requires that the value cannot change underneath the "
            "table. A mutable string could not be a key."},
]},

}


# The /interview/ track authors its questions alongside the rest of each page
# (tools/interview.py), because a question there is written against the exact
# program and visualisation on that page. Merged in here so build_labs.py and
# the practice bank see one dictionary rather than two sources.
from interview import CHECKS as _INTERVIEW_CHECKS  # noqa: E402

LABS.update(_INTERVIEW_CHECKS)

# The generated Python modules author their questions beside the programs they
# are about (tools/python_topics.py), for the same reason the interview track
# does: a question written against the exact code on the page cannot drift
# from it.
from python_topics import CHECKS as _PYTHON_CHECKS  # noqa: E402
from pydantic_topics import CHECKS as _PYDANTIC_CHECKS  # noqa: E402

LABS.update(_PYTHON_CHECKS)
LABS.update(_PYDANTIC_CHECKS)

# The generated classical image-processing modules do the same
# (tools/cv_topics.py). A question there is written against the exact operation
# the page lets you drive, so it belongs next to the controls rather than here.
from cv_topics import CHECKS as _CV_CHECKS  # noqa: E402

LABS.update(_CV_CHECKS)

# And the generated database modules (tools/db_topics.py), where a question is
# written against the exact query and seed data on the page.
from db_topics import CHECKS as _DB_CHECKS  # noqa: E402

LABS.update(_DB_CHECKS)

# And the generated machine learning workflow modules (tools/ml_topics.py),
# where a question is written against the exact simulation on the page.
from ml_topics import CHECKS as _ML_CHECKS  # noqa: E402

LABS.update(_ML_CHECKS)

# The generated maths modules keep their questions beside the demonstration
# they are about (tools/math_topics.py), for the same reason every other
# generated track does.
from math_topics import CHECKS as _MATH_CHECKS  # noqa: E402

LABS.update(_MATH_CHECKS)

# The generated deep learning modules, same arrangement as the rest.
from dl_topics import CHECKS as _DL_CHECKS  # noqa: E402

LABS.update(_DL_CHECKS)
