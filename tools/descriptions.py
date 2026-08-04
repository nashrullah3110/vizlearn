# -*- coding: utf-8 -*-
"""Hand-written meta descriptions.

81 pages shared one template ("Learn X with a beginner-friendly interactive
visualization, examples, and guided practice on VizLearn"), which is what
Google sees as the search snippet, what social cards show, and what the site's
own search matches against. Near-identical descriptions across half the site
invite Google to discard them and write its own.

Each entry says what the reader will actually see or do. Aim for 110-165
characters: long enough to fill a result snippet, short enough not to be cut.

Anything absent here keeps whatever the page already declares.
"""

DESCRIPTIONS = {
    # --- Machine Learning -------------------------------------------------
    "machine_learning/confusion_matrix.html":
        "See why accuracy alone misleads. Build a confusion matrix cell by cell and watch precision, recall and F1 shift with every prediction.",
    "machine_learning/cosine_similarity.html":
        "Measure similarity by angle instead of distance. Drag two vectors apart and watch the cosine similarity score respond in real time.",
    "machine_learning/cross_validation.html":
        "Watch data split into k folds, each taking a turn as validation, and see why a single train/test split can flatter a model.",
    "machine_learning/decision_tree.html":
        "Watch a decision tree choose each split by information gain, growing branch by branch until every leaf holds a single class.",
    "machine_learning/k_means.html":
        "Place centroids and watch K-Means alternate between assigning points and recentring clusters until it converges.",
    "machine_learning/knn.html":
        "Drop a new point on the plane and watch KNN classify it by neighbour vote. Change k to see the decision boundary tighten or smooth.",
    "machine_learning/label_encoding.html":
        "Turn categories into integers, and see where label encoding is safe and where it invents an ordering your model will believe.",
    "machine_learning/linear_regression_with_ols.html":
        "Drag a regression line by hand and watch the residuals and mean squared error react, then let least squares find the optimum.",
    "machine_learning/naive_bayes.html":
        "Step through Bayes' theorem on real text and see why a 'naive' independence assumption still classifies spam remarkably well.",
    "machine_learning/one_hot_encoding.html":
        "Expand a categorical column into binary columns and see how one-hot encoding avoids implying an order that was never there.",
    "machine_learning/sliding_window_for_timeseries_data.html":
        "Slide a window across a time series to turn a raw sequence into supervised training rows of features and targets.",
    "machine_learning/svm.html":
        "Add points from two classes and watch a support vector machine find the hyperplane with the widest possible margin between them.",
    "machine_learning/train_test_split.html":
        "See why testing on data you trained on flatters a model, and how holding out a test set gives you an honest score.",
    "machine_learning/bias_vs_variance.html":
        "Dial bias and variance up and down, resample the data, and watch a stable underfit turn into an unstable overfit.",
    "machine_learning/evaluation_metrics_for_regression.html":
        "Compare MAE, MSE, RMSE and R-squared on identical predictions and see which kinds of error each metric punishes hardest.",
    "machine_learning/hard_vs_soft_labelling.html":
        "Compare a single hard label against a probability distribution, and see what a model loses when forced to pick one winner.",
    "machine_learning/label_imbalance_problem.html":
        "See how a model scores 99% accuracy while missing every fraud case, and why imbalance breaks your intuition about metrics.",
    "machine_learning/model_and_data_drift.html":
        "Fast-forward through production and watch a well-trained model decay as incoming data drifts away from what it learned.",
    "machine_learning/training_on_label_imbalanced_dataset.html":
        "Try resampling, class weights and threshold tuning on an imbalanced dataset and watch minority-class recall respond.",

    # --- Deep Learning ----------------------------------------------------
    "deep_learning/activation_functions.html":
        "Compare ReLU, sigmoid, tanh and others on the same input, and see how each one bends the signal passing through a layer.",
    "deep_learning/batch_processing_in_neural_networks.html":
        "Compare stochastic, mini-batch and full-batch training, and see how batch size trades gradient noise against speed.",
    "deep_learning/dropout_in_neural_networks.html":
        "Switch neurons off at random during training and watch dropout stop the network leaning on any single pathway.",
    "deep_learning/batch_normalization.html":
        "Toggle batch normalisation on a deep network and watch it rescale layer outputs to keep gradients stable as they flow back.",
    "deep_learning/data_sparsity.html":
        "Feed mostly-zero inputs through a network and watch entire pathways go dormant, because anything multiplied by zero stays zero.",
    "deep_learning/early_stopping_in_neural_networks.html":
        "Watch validation loss bottom out then start climbing, and see early stopping halt training at the moment generalisation peaks.",
    "deep_learning/feature_scaling_in_neural_networks.html":
        "See what happens when one feature is measured in thousands and another in decimals, and how scaling rebalances the gradients.",
    "deep_learning/gradient_descent_batch_processing.html":
        "Change one control at a time and watch how batch size reshapes the path gradient descent takes toward the minimum.",
    "deep_learning/gradient_descent_training.html":
        "Watch gradient descent step downhill across a loss surface, and see how the learning rate decides between converging and diverging.",
    "deep_learning/how_loss_is_calculated.html":
        "Follow a prediction through to a single loss value, and see how the error signal that drives all learning is actually computed.",
    "deep_learning/hyper-paramter_tuning.html":
        "Run grid search and random search side by side on the same model and see which finds strong hyperparameters in fewer trials.",
    "deep_learning/learning_rate_scheduling.html":
        "Compare a fixed learning rate against a decaying schedule, and watch scheduling rescue a model that would otherwise overshoot.",
    "deep_learning/linear_regression_with_gradient_descent.html":
        "Take gradient descent one step at a time and watch the best-fit line and its mean squared error converge together.",
    "deep_learning/model_training_curve.html":
        "Read training and validation curves like a practitioner: spot underfitting, a healthy fit and overfitting from their shape alone.",
    "deep_learning/reproducibility_of_model.html":
        "Fix the random seed and see exactly what becomes repeatable: initial weights and the order training data is shuffled in.",
    "deep_learning/neural_network.html":
        "Build a neural network layer by layer and watch data flow forward through weights, biases and activations into a prediction.",
    "deep_learning/neural_network_for_regression.html":
        "Adapt a neural network to predict continuous values, and see how its output layer and loss differ from a classifier's.",
    "deep_learning/neural_network_for_unsupervised_learning.html":
        "Train a network with no labels at all and watch it uncover structure by learning to reconstruct its own input.",
    "deep_learning/optimizers_in_3d.html":
        "Race SGD, Momentum, RMSprop and Adam across a 3D loss landscape and watch which of them escape local minima and which get stuck.",
    "deep_learning/optimizers_in_neural_networks.html":
        "Run several optimizers in parallel on one loss surface and see how momentum and adaptive learning rates change the route.",
    "deep_learning/overfitting_vs_underfitting.html":
        "Move model complexity from too simple to too flexible and watch the gap open between training and validation performance.",
    "deep_learning/perceptron.html":
        "Adjust the weights and bias of a single perceptron by hand and watch its decision boundary swing across the data.",
    "deep_learning/regularization_in_neural_networks.html":
        "Compare L1 and L2 penalties, and watch Lasso zero out useless weights while Ridge shrinks all of them smoothly.",
    "deep_learning/vanishing_vs_exploding_gradient.html":
        "Watch gradients shrink to nothing or blow up as they multiply back through layers, and see what keeps them in range.",
    "deep_learning/weight_initialization.html":
        "Compare He, Xavier, random and zero initialisation, and watch poor starting weights kill a deep network before it learns.",
    "deep_learning/weights_and_biases.html":
        "See what the numbers a network learns are actually for: weights scale each input, bias shifts where the neuron fires.",

    # --- Algorithms -------------------------------------------------------
    "dsa/a_star.html":
        "Watch A* combine real distance with a heuristic estimate to reach the goal while exploring far fewer nodes than Dijkstra.",
    "dsa/backtracking.html":
        "Watch backtracking commit to a path, hit a dead end, and unwind to the last decision point until the puzzle resolves.",
    "dsa/binary_search.html":
        "Halve the search space with every comparison and watch binary search locate a target in a sorted array in log n steps.",
    "dsa/bubble_sort.html":
        "Watch adjacent pairs compare and swap, sending the largest value bubbling to the end on every pass through the array.",
    "dsa/counting_sort.html":
        "Sort integers without a single comparison by tallying how often each value occurs, then rebuilding the array in order.",
    "dsa/depth_first_search.html":
        "Follow depth-first search as far down one branch as it goes, then watch it backtrack and take the next unexplored edge.",
    "dsa/dictionaries_in_python.html":
        "Insert, look up and delete key-value pairs in a Python dictionary, and see how hashing makes each operation instant.",
    "dsa/dijkstras.html":
        "Watch Dijkstra's algorithm settle nodes in order of distance and build the shortest path across a weighted graph.",
    "dsa/fibonacci_search.html":
        "Divide a sorted array using Fibonacci numbers rather than midpoints, avoiding the division binary search relies on.",
    "dsa/insertion_sort.html":
        "Build a sorted section one element at a time and watch each new value shift left into the position where it belongs.",
    "dsa/interpolation_search.html":
        "Estimate where a value should sit instead of always splitting the middle, the way you open a phone book near the S pages.",
    "dsa/linear_search.html":
        "Step through an array one element at a time and see exactly when brute-force scanning is genuinely the right choice.",
    "dsa/lists_in_python.html":
        "Index, slice, append and mutate Python lists interactively, and see how the underlying dynamic array grows as you go.",
    "dsa/merge_sort.html":
        "Split an array down to single elements and watch merge sort combine sorted halves back together in n log n time.",
    "dsa/quick_sort.html":
        "Pick a pivot, partition around it, then recurse, and see why the pivot choice decides whether quick sort flies or crawls.",
    "dsa/selection_sort.html":
        "Scan for the smallest remaining value and swap it into place, one position at a time, until the whole array is sorted.",
    "dsa/strings_in_python.html":
        "Slice, index, join and format Python strings interactively, and see how immutability shapes what each operation does.",

    # --- NLP --------------------------------------------------------------
    "natural_language_processing/ascii_codes.html":
        "Type any character and see the ASCII number a computer actually stores, the very first step from text into numbers.",
    "natural_language_processing/how_neural_network_text.html":
        "Follow a sentence from raw characters through tokens and vectors into something a neural network can actually multiply.",
    "natural_language_processing/how_rnn_process_text.html":
        "Feed a sentence word by word into a recurrent network and watch the hidden state carry context from each step to the next.",
    "natural_language_processing/n_gram.html":
        "Slide an n-gram window across text and see how counting short sequences lets a model guess which word comes next.",
    "natural_language_processing/stemming_vs_lemmatization.html":
        "Compare a stemmer chopping suffixes against a lemmatizer resolving proper dictionary forms of the very same words.",
    "natural_language_processing/text_normalization_pipeline.html":
        "Run raw text through lowercasing, punctuation stripping and stop-word removal, and watch each stage clean it further.",
    "natural_language_processing/tokenization.html":
        "Split text into words, characters or sentences and see how the tokenizer you choose changes what a model actually reads.",
    "natural_language_processing/word_cloud.html":
        "Paste any text and watch a word cloud size each term by how often it appears, exposing what a document is really about.",
    "natural_language_processing/how_lstm_processes_text.html":
        "Watch an LSTM carry a cell state for long-term memory and a hidden state for short-term as it reads through a sequence.",

    # --- Computer Vision --------------------------------------------------
    "computer_vision/downsampling_in_cnn.html":
        "Shrink a feature map with max, average or min pooling and see how downsampling keeps the signal but discards the detail.",
    "computer_vision/edge_detection.html":
        "Slide a sensitivity threshold across a real image and watch edges appear wherever brightness changes sharply enough.",
    "computer_vision/feature_map_in_cnn.html":
        "Drag a convolution filter across an image and watch it build a feature map one value at a time, the core operation inside a CNN.",
    "computer_vision/grayscale_image_processing.html":
        "See a grayscale image for what it is: a grid of brightness numbers you can filter, threshold and edit directly.",
    "computer_vision/image_data_augmentation.html":
        "Flip, rotate, zoom and add noise to an image, and see how augmentation multiplies a small training set into a larger one.",
    "computer_vision/rgb_image_processing.html":
        "Split a colour image into red, green and blue channels and see how three grids of numbers combine into every pixel.",

    # --- Database ---------------------------------------------------------
    "database/joins_in_sql.html":
        "Watch INNER, LEFT, RIGHT and FULL joins pull rows from two tables, and see exactly which rows each variant keeps.",
    "database/groupby_in_sql.html":
        "Group rows by a column and watch COUNT, SUM and AVG collapse many rows into one row per group, live against a sample table.",
    "database/window_functions_in_sql.html":
        "Rank, total and compare across rows without collapsing them, using OVER and PARTITION BY on a live result set.",

    # --- Gen AI -----------------------------------------------------------
    "gen_ai/casual_language_modeling.html":
        "See how predicting the next token, over and over, is all it takes for a model like GPT to produce fluent text.",

    "machine_learning/logistic_regression.html":
        "Fit a linear score, squash it through a sigmoid, and read the probability "
        "anywhere on the plot. See why the boundary is always a straight line.",
    "machine_learning/roc_curve_and_auc.html":
        "Drag a threshold through two overlapping score distributions and watch the "
        "ROC curve, AUC and precision respond - including the imbalance trap.",
    "machine_learning/ridge_and_lasso_regression.html":
        "Turn lambda up and watch a wild polynomial calm down. Ridge shrinks every "
        "coefficient; Lasso drives the useless ones to exactly zero.",
    "machine_learning/random_forest.html":
        "Grow one deep tree, then forty, and watch a jagged unstable boundary average "
        "into a smooth one. Bagging and feature subsampling, measured.",
    "machine_learning/gradient_boosting.html":
        "Add one small tree at a time, each fitted to the residuals left by the last. "
        "Watch the errors shrink, and watch it overfit when the trees get too deep.",

    "deep_learning/softmax_and_cross_entropy.html":
        "Drag raw logits and watch softmax turn them into probabilities, then watch "
        "cross-entropy punish a confident mistake. Includes the p - y gradient.",
    "natural_language_processing/attention_mechanism.html":
        "See why a fixed context vector forgets, and how attention lets the decoder "
        "re-weigh every input word at each output step. Full alignment matrix.",
    "natural_language_processing/query_key_value.html":
        "Follow one attention lookup end to end - score, scale, softmax, blend - and "
        "watch softmax saturate when the 1/sqrt(d_k) scaling is removed.",
    "natural_language_processing/self_attention.html":
        "The full n x n attention matrix over one sentence. Watch a pronoun resolve at "
        "layer 2, apply a causal mask, and see why word order needs encoding.",

    "natural_language_processing/positional_encoding.html":
        "Self-attention is blind to word order. See sinusoidal encoding give every "
        "position a bounded unique fingerprint, and watch the naive schemes fail.",

    "natural_language_processing/multi_head_attention.html":
        "Run several attention patterns at once, each tracking a different relationship. "
        "See why more heads cost no extra parameters - the dimension is split, not added.",

    "natural_language_processing/transformer_architecture.html":
        "Attention, add, normalise, feed-forward, add, normalise - stacked. Switch the "
        "residual connections off and watch a 24-layer stack stop being trainable.",

    "maths/entropy_and_information.html":
        "Drag a distribution and watch uncertainty rise and fall. Entropy is the average "
        "surprise, and the quantity every classification loss is built from.",
    "maths/vector_norms.html":
        "Three answers to how big a vector is. See why the L1 diamond's corners make Lasso "
        "produce exact zeros while the L2 circle only shrinks.",

    "maths/matrix_as_transformation.html":
        "Drag four numbers and watch space rotate, stretch and shear. The columns are "
        "where the basis vectors land, and the determinant is the area they span.",

    "maths/eigenvalues_and_eigenvectors.html":
        "Sweep a vector around the circle and find the two directions a matrix does not "
        "rotate. Trace, determinant and the guarantee PCA is built on.",
    "maths/covariance_and_correlation.html":
        "Stretch and tilt a point cloud. Covariance moves with the units, correlation does "
        "not, and neither notices a curve.",

    "maths/maximum_likelihood_estimation.html":
        "Slide a candidate distribution over fixed data and watch the likelihood peak. "
        "Where squared error, log loss and cross-entropy all come from.",

    "maths/conditional_probability.html":
        "Conditioning does not change the outcomes, it discards them. Watch the sample "
        "space shrink, and see why P(A given B) is not P(B given A).",

    "maths/distance_metrics.html":
        "Four answers to how far apart two points are. Watch cosine ignore length entirely "
        "while Euclidean, Manhattan and Chebyshev disagree by shape.",

    # --- Databases & SQL, later additions ---------------------------------
    "database/query_execution_order.html":
        "SQL reads top to bottom but runs FROM first and SELECT second-to-last. Step "
        "through the real order and watch the row count change at every stage.",

    "database/null_handling_in_sql.html":
        "NULL is not a value, so nothing about it compares the way you expect. Pick an "
        "expression and watch COALESCE, NULLIF and IS NULL treat the same rows differently.",

    "database/case_and_views_in_sql.html":
        "Build a CASE expression that turns raw numbers into labels, then save the whole "
        "query as a view and watch it stay a live query, not a snapshot.",

    "database/union_intersect_except_in_sql.html":
        "Combine two result sets instead of two tables. Pick an operator and watch which "
        "rows survive, and see UNION ALL keep the duplicate UNION would quietly drop.",

    "database/normalization_in_sql.html":
        "One table with a multi-valued column, split step by step into 1NF, 2NF and 3NF. "
        "Watch the redundant cells that cause update anomalies drop to zero.",

    "database/transactions_and_acid.html":
        "Step a transfer through BEGIN, two UPDATEs and COMMIT or ROLLBACK, with a second "
        "session watching. Fail it halfway and watch atomicity undo both writes, not one.",

    "database/order_by_in_sql.html":
        "Watch rows slide into their new order as you change the sort key, direction, "
        "tie-breaker and NULLS placement, with the query building live.",

    "database/having_in_sql.html":
        "Rows become groups become filtered groups. Move the same condition between WHERE "
        "and HAVING and watch the answer change, one stage at a time.",

    "database/subqueries_in_sql.html":
        "The inner query runs first and hands its answer to the outer one. Scalar, IN-list, "
        "derived table, and a correlated subquery re-running once per row.",

    "database/indexes_in_sql.html":
        "Walk a B-tree instead of reading every row and watch rows-examined collapse. Then "
        "meet the queries an index cannot help, and what it costs on writes.",

    # --- Maths, later additions --------------------------------------------
    "maths/projections.html":
        "Drag one vector onto another and watch its shadow, plus the perpendicular residual "
        "left behind. The geometric root of least squares.",

    "maths/determinant.html":
        "The determinant is the area the unit square becomes. Sweep it through zero and "
        "watch the plane flatten, then turn itself inside out.",

    "maths/identity_inverse_transpose.html":
        "Apply a transformation, then undo it. Watch the undo fail the moment the "
        "determinant hits zero, and see why the transpose is not an undo at all.",

    "maths/rank_and_linear_independence.html":
        "Drag two columns until one is a multiple of the other and watch the reachable "
        "plane collapse onto a line. That collapse is what rank counts.",

    "maths/cross_entropy_and_kl_divergence.html":
        "Drag one distribution towards another and watch the gap close. Cross-entropy is "
        "the cost of being wrong; KL divergence is how much of it is your fault.",

    "maths/information_gain.html":
        "Move a split through a dataset and watch entropy fall. The threshold that drops "
        "it most is exactly the question a decision tree decides to ask.",

    # --- NLP, later additions ----------------------------------------------
    "natural_language_processing/bert_vs_gpt.html":
        "One change to the attention mask splits the transformer family in two. See what "
        "each token may look at, and which training objective that permits.",

    "deep_learning/gradient_clipping.html":
        "Step a weight down a parabola and inject one exploding gradient. Without clipping "
        "the weight flies off; with it, the update is capped and training survives.",

    "deep_learning/residual_connections.html":
        "Chain the same shrinking layer N times and watch the gradient vanish before it "
        "reaches the input. Add a skip connection to each layer and watch it stop vanishing.",

    "deep_learning/layer_normalization.html":
        "Normalize down each sample's own row instead of across the batch, and watch it "
        "keep working when the batch shrinks to a single example - where BatchNorm breaks.",

    # --- Gen AI, later additions -------------------------------------------
    "gen_ai/embeddings_and_vector_search.html":
        "Meaning becomes geometry. Run an exact nearest-neighbour search, then a "
        "partitioned one, and watch comparisons collapse while recall quietly slips.",

    "gen_ai/context_window_and_kv_cache.html":
        "Fill a context window and watch what gets pushed out, then switch off the KV "
        "cache and watch the work per token go quadratic.",

    "gen_ai/fine_tuning_vs_rlhf.html":
        "Three stages, three jobs. Watch a model's answers move under supervised "
        "fine-tuning, then under preference optimisation, and watch reward hacking happen.",

    "gen_ai/hallucination_and_grounding.html":
        "A model always has probability mass somewhere, even when it knows nothing. Watch "
        "it move as evidence, temperature, retrieval and an abstain option are added.",

    "gen_ai/rag.html":
        "Ask about a product no model has heard of. Watch retrieval score every chunk, "
        "paste the winners into the prompt, and turn a guess into a cited answer.",

    "gen_ai/dot_product_vs_cosine_similarity.html":
        "Stretch one document's vector and watch dot-product ranking promote it purely for "
        "being longer, while cosine ranking never moves. Two different questions, one embedding.",

    # --- Deep Learning, later additions ------------------------------------
    "deep_learning/backpropagation.html":
        "Step forward through a small computational graph, then backward, watching each "
        "local gradient multiply along the chain. Checked against finite differences.",

    # --- Machine Learning, later additions --------------------------------
    "machine_learning/pca.html":
        "Rotate a line through a point cloud and watch the variance it captures peak on "
        "exactly one angle. That angle is PC1, and the rest is what you lose.",
}
