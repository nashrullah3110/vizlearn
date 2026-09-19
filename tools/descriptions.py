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
    "computer_vision/iou_and_non_max_suppression.html":
        "A detector proposes four boxes for two objects. IoU measures the overlap, and Non-Max Suppression uses that number to throw the duplicates away.",
    "computer_vision/object_detection_with_bounding_boxes.html":
        "Drag a predicted box toward the ground truth and watch IoU climb, the loss fall, and the detection flip from a miss to a match at the 0.5 threshold.",
    "computer_vision/resnet_and_identity_shortcuts.html":
        "Push a signal vector through the same contractive layer twenty times, with and without an identity shortcut, and watch one collapse toward zero while the other never can.",
    "computer_vision/semantic_segmentation_unet.html":
        "Downsample a mask to see more context, then upsample it back, and watch the boundary blur unless a skip connection carries the resolution pooling just destroyed.",

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

    "gen_ai/bm25_and_sparse_retrieval.html":
        "The keyword-matching half of search, computed live. Drag length normalization to "
        "zero and watch a verbose repetitive document dominate purely on term count.",

    "gen_ai/chunking_strategies_for_rag.html":
        "Slide the chunk size down and watch fixed-size splitting cut sentences in half, "
        "while semantic chunking respects paragraph boundaries and never does.",

    "gen_ai/retrieval_evaluation_metrics.html":
        "The same five relevant documents out of ten retrieved, in three different orders. "
        "Precision and recall cannot tell them apart - MRR and nDCG can.",

    "gen_ai/hybrid_search_reciprocal_rank_fusion.html":
        "Run vector search and BM25 side by side and watch them disagree, then fuse the two "
        "rankings and see a document neither method alone ranked first win on consensus.",

    "gen_ai/reranking_bi_encoders_vs_cross_encoders.html":
        "Retrieve six candidates fast with a bi-encoder, then re-score them with a slower "
        "cross-encoder that reads query and document together and catches what was missed.",

    "gen_ai/maximal_marginal_relevance.html":
        "Pick the next document by relevance minus similarity to what you already picked, "
        "and watch three near-duplicate chunks stop crowding out everything else.",

    "gen_ai/parent_document_retriever.html":
        "Search small chunks so the match is precise, then hand the model the whole "
        "parent document so the answer has enough context to be worth reading.",
    "gen_ai/multi_query_retriever.html":
        "One question asked several ways. Each phrasing retrieves separately and the "
        "union catches the document a single wording would have missed.",
    "gen_ai/self_query_retriever.html":
        "Split a question into a semantic query and a metadata filter, so \"after 2020\" "
        "becomes a rule that is enforced rather than a phrase that is matched.",
    "gen_ai/query_rewriting_and_hyde.html":
        "A terse question shares almost no vocabulary with the formal passage that answers it. "
        "Expand the query, or embed a hypothetical answer instead, and watch it climb the ranking.",

    # --- Deep Learning, later additions ------------------------------------
    "deep_learning/backpropagation.html":
        "Step forward through a small computational graph, then backward, watching each "
        "local gradient multiply along the chain. Checked against finite differences.",

    # --- Machine Learning, later additions --------------------------------
    "machine_learning/pca.html":
        "Rotate a line through a point cloud and watch the variance it captures peak on "
        "exactly one angle. That angle is PC1, and the rest is what you lose.",

    # --- Python (in-browser interpreter) ----------------------------------
    "python/hello_python.html":
        "Write your first print statement in a real in-browser Python interpreter and watch "
        "strings, numbers and newlines come out the other side.",
    "python/variables_and_types.html":
        "Assign a name and ask Python what it is. See the types Python tracks for you and "
        "why the same value behaves differently depending on what it is.",
    "python/numbers_and_operators.html":
        "Run arithmetic live in the browser: the difference between / and //, what modulo "
        "returns, and how Python rounds when you mix ints and floats.",
    "python/strings_and_slicing.html":
        "Strings are sequences. Index into them, slice them with start:stop:step, and use "
        "the methods that make text manipulation read like English.",
    "python/lists_and_indexing.html":
        "Build a list, reach into it by index, and see why Python counts positions from zero.",
    "python/dictionaries.html":
        "Store values under names instead of positions, look them up by key, and handle the key that is not there.",
    "python/booleans_and_comparisons.html":
        "Compare values, combine them with and, or and not, and see which everyday values Python already treats as false.",
    "python/if_elif_else.html":
        "Branch on a condition, and watch indentation decide which lines belong to which branch.",
    "python/for_loops_and_range.html":
        "Loop over a list, count with range(), and accumulate a result across the passes of a for loop.",
    "python/while_loops_and_control.html":
        "Loop while a condition holds, exit early with break, skip a pass with continue, and see what makes a loop run forever.",
    "python/functions_and_return.html":
        "Define a function, pass it arguments, and see why printing a result is not the same as returning one.",
    "python/reading_errors.html":
        "Read a traceback from the bottom up, recognise the common Python error types, and turn each message into the fix it points at.",
    "concurrency/choosing_threads_processes_or_async.html":
        "Choose between threads, processes, or async based on your I/O pattern and GIL constraints.",
    "concurrency/locks_and_the_ways_they_go_wrong.html":
        "Understand deadlocks, livelocks, race conditions and how to avoid them in concurrent code.",

    # --- Async Python (SEO batch) --------------------------------
    "async_python/coroutines_tasks_and_await.html":
        "Learn why calling an async function returns a coroutine, not a result, and how create_task turns sequential awaits into real overlap.",
    "async_python/event_loop_stepped_through.html":
        "Step through Python's event loop tick by tick. See how one thread, one ready queue and cooperative yields run thousands of coroutines.",
    "async_python/queues_and_backpressure.html":
        "Connect a fast producer to a slow consumer with an asyncio queue and watch one maxsize parameter prevent memory from growing without bound.",
    "async_python/running_work_concurrently.html":
        "Fan out many awaits at once with gather and TaskGroup, collect every result in order, and control what happens when one task fails.",
    "async_python/the_blocking_call_that_freezes_the_loop.html":
        "See how one synchronous call inside a coroutine freezes every other task, then learn the two ways to move blocking work off the loop.",

    # --- Computer Vision (SEO batch) -----------------------------
    "computer_vision/affine_transforms.html":
        "Build a 2x3 affine matrix from rotation, scale, shear and translation, apply it to an image, and see every pixel land in its new position.",
    "computer_vision/anchor_boxes.html":
        "See how anchor boxes turn object detection into a small regression, and follow the IoU-based rule that assigns each ground truth to a box.",
    "computer_vision/blur_gaussian_median_bilateral.html":
        "Apply Gaussian, median and bilateral blur to one noisy image side by side and see which filter removes noise while preserving edges.",
    "computer_vision/colour_spaces_rgb_hsv.html":
        "Convert the same pixel between RGB and HSV, then see how a colour range that needs six RGB inequalities becomes a single HSV threshold.",
    "computer_vision/convolution_kernels.html":
        "Slide a 3x3 kernel across an image by hand, multiply and sum at each position, and watch edge detection and blur fall out of nine numbers.",
    "computer_vision/depthwise_separable_convolution.html":
        "Split a standard convolution into depthwise and pointwise steps, count the multiply-adds saved, and see why mobile models rely on them.",
    "computer_vision/dilated_convolutions.html":
        "Expand a kernel's field of view without adding parameters or pooling, and spot the gridding artefact that appears when rates are wrong.",
    "computer_vision/erosion_and_dilation.html":
        "Apply erosion and dilation to a binary mask, then combine them into opening, closing, gradient and top-hat to clean segmentation output.",
    "computer_vision/global_average_pooling.html":
        "Replace a flatten layer with global average pooling, count the parameters removed, and see why modern CNNs skip the large dense head.",
    "computer_vision/grad_cam.html":
        "Compute a Grad-CAM heatmap from gradients flowing into the last convolutional layer, then overlay it to see which regions drove the prediction.",
    "computer_vision/harris_corners.html":
        "Compute the Harris corner response at every pixel, threshold the result, and see why corners survive rotation and small shifts.",
    "computer_vision/histograms_and_equalisation.html":
        "Plot an image histogram, apply equalisation, and watch a low-contrast photograph spread across the full intensity range in one pass.",
    "computer_vision/mean_average_precision.html":
        "Sort detections by confidence, compute precision and recall at each step, and watch the area under that curve collapse into one mAP number.",
    "computer_vision/one_by_one_convolutions.html":
        "See how a 1x1 convolution mixes channels without touching spatial dimensions, and why it appears in Inception, ResNet and every bottleneck.",
    "computer_vision/receptive_field.html":
        "Trace one unit's receptive field back through conv and pooling layers and see how depth, stride and dilation decide what it can observe.",
    "computer_vision/resizing_and_interpolation.html":
        "Resize an image with nearest, bilinear and bicubic interpolation side by side and see exactly where each method invents or drops detail.",
    "computer_vision/segmentation_tasks.html":
        "Compare semantic, instance and panoptic segmentation on the same scene and see the two questions that separate each task from the others.",
    "computer_vision/template_matching.html":
        "Slide a template across an image, compute the match score at every position, and see why changes in scale and rotation break the method.",
    "computer_vision/thresholding.html":
        "Turn a greyscale image into a binary mask with global and adaptive thresholds, and see where uniform lighting stops being enough.",
    "computer_vision/vision_transformer_patches.html":
        "Split an image into fixed-size patches, project each into a token, and follow the sequence through a transformer to see its quadratic cost.",

    # --- Concurrency (SEO batch) ---------------------------------
    "concurrency/concurrent_futures.html":
        "Submit work to a ThreadPoolExecutor and ProcessPoolExecutor through the same API, then inspect a Future's state transitions step by step.",
    "concurrency/queues_between_threads.html":
        "Pass work between threads with a queue that already wraps a lock and a condition, and see why it replaces most hand-rolled coordination.",
    "concurrency/race_conditions_in_python.html":
        "Run x += 1 from two threads, watch the count drift, and trace the three bytecodes that open the gap where a value goes missing.",
    "concurrency/the_gil_and_what_it_locks.html":
        "See what Python's GIL actually protects, why threads still speed up I/O-bound programs, and why they do nothing for CPU-bound code.",
    "concurrency/threads_or_processes.html":
        "Compare threads and processes side by side: shared memory versus isolation, the GIL constraint, and the real cost of sending data between workers.",

    # --- Database (SEO batch) ------------------------------------
    "database/aggregate_functions_in_sql.html":
        "Run COUNT, SUM, AVG, MIN and MAX on real rows, see how each one handles NULLs, and fix the silent mistake that changes your totals.",
    "database/cap_theorem.html":
        "Walk through the CAP theorem with a two-node example, see which two guarantees you keep, and learn what the theorem does not actually say.",
    "database/composite_and_covering_indexes.html":
        "Build a composite index, reorder the columns, and watch the query plan switch between an index scan and a full table scan on the same query.",
    "database/constraints_in_sql.html":
        "Add UNIQUE, CHECK and NOT NULL constraints to a table and watch the database reject every row that violates a rule you wrote once.",
    "database/deadlocks_in_sql.html":
        "Set up two transactions that lock rows in opposite order, watch the deadlock form, and see the one change in lock order that prevents it.",
    "database/document_model_vs_rows.html":
        "Store the same order as a nested document and as normalised rows, then run the queries each shape handles well and the ones it does not.",
    "database/exists_vs_in_vs_join.html":
        "Write the same question with EXISTS, IN and JOIN, compare the execution plans, and find the version that quietly returns wrong rows.",
    "database/explain_and_query_plans.html":
        "Run EXPLAIN on a slow query, read the plan node by node, and spot the sequential scan or nested loop that accounts for the missing time.",
    "database/isolation_levels.html":
        "Step through read uncommitted, read committed, repeatable read and serializable with two concurrent transactions to see what each one allows.",
    "database/key_value_and_graph_models.html":
        "Compare key-value and graph models against relational tables, see the queries each answers in one hop, and learn when leaving SQL pays off.",
    "database/mvcc_in_databases.html":
        "Watch MVCC serve a reader an older row version while a writer updates the same row, and see why neither transaction has to wait for the other.",
    "database/oltp_vs_olap_columnar.html":
        "Compare row storage and columnar storage on the same table, run an analytical query on each, and see why dashboards need a different engine.",
    "database/partitioning_in_databases.html":
        "Partition a table by range and by hash, run the same query on each layout, and see how the planner skips every partition it does not need.",
    "database/primary_and_foreign_keys.html":
        "Define a primary key and a foreign key, attempt an insert that violates each, and watch the database enforce referential integrity for you.",
    "database/recursive_ctes_in_sql.html":
        "Write a recursive CTE that walks an org chart row by row, follow each iteration of the loop, and see how SQL follows a chain of unknown length.",
    "database/replication_and_lag.html":
        "Set up a primary and a read replica, write to one and read from the other, and measure the lag window where a query returns stale data.",
    "database/self_joins_in_sql.html":
        "Join a table to itself, match employees to managers in the same rows, and walk through the three query patterns that need a self-join.",
    "database/sharding_in_databases.html":
        "Shard a table by a key, route a query to the right partition, and see the four capabilities you lose when data lives on separate machines.",
    "database/sql_injection_and_parameters.html":
        "Build a query with string concatenation, inject a payload that drops a table, then switch to a parameterised query that blocks it completely.",
    "database/star_schema.html":
        "Build a star schema with one fact table and three dimensions, run an analytical query, and see why columnar engines prefer this layout.",

    # --- Deep Learning (SEO batch) -------------------------------
    "deep_learning/autoencoders.html":
        "Train an autoencoder to compress and reconstruct its input, examine the bottleneck, and see why a network that copies is still worth building.",
    "deep_learning/contrastive_learning.html":
        "Train a model to pull matching pairs together and push non-matches apart without labels, and see a useful representation emerge from raw data.",
    "deep_learning/diffusion_models.html":
        "Add noise to an image step by step, train a network to reverse each step, then sample a new image by running the learned reverse chain.",
    "deep_learning/embedding_layers.html":
        "Replace a one-hot vector with a learned embedding lookup, compare the memory and compute saved, and see why every NLP pipeline starts here.",
    "deep_learning/generative_adversarial_networks.html":
        "Train a generator against a discriminator, watch the adversarial loss curves, and see the mode collapse and instability that make GANs hard.",
    "deep_learning/gradient_accumulation.html":
        "Accumulate gradients over several small forward passes before one optimiser step and get large-batch training on a device that cannot hold one.",
    "deep_learning/label_smoothing.html":
        "Change the target from a hard one-hot to a soft distribution, watch the loss curve shift, and measure the calibration improvement it produces.",
    "deep_learning/mixed_precision_training.html":
        "Train in float16, see the underflow that zeros out small gradients, then fix it with a loss scale that fits in one extra line of code.",
    "deep_learning/seq2seq_and_beam_search.html":
        "Feed a sequence into an encoder, decode one token at a time, and compare greedy search with beam search to see how wider beams change output.",
    "deep_learning/variational_autoencoders.html":
        "Add a KL divergence term to an autoencoder loss, sample from the latent space, and see how two competing objectives produce a generative model.",

    # --- Fastapi (SEO batch) -------------------------------------
    "fastapi/apirouter.html":
        "Move endpoints into an APIRouter, mount it with a prefix, and see how a growing FastAPI app stays organised without circular imports.",
    "fastapi/async_vs_sync_endpoints.html":
        "Compare async def and plain def endpoints in FastAPI, see where each one runs, and spot the mistake that turns a fast framework into a slow one.",
    "fastapi/background_tasks.html":
        "Add a BackgroundTasks parameter, schedule work after the response leaves, and see the point where this runner needs replacing with a task queue.",
    "fastapi/class_dependencies.html":
        "Turn a class with __init__ parameters into a FastAPI dependency and see how any callable with the right signature becomes injectable config.",
    "fastapi/dependencies_with_yield.html":
        "Write a dependency that yields a database session, watch FastAPI run setup before the handler and teardown after it, then see the pattern.",
    "fastapi/dependency_injection.html":
        "Declare what an endpoint needs with Depends, let FastAPI resolve and inject it, and see how testing and swapping implementations get simpler.",
    "fastapi/dependency_overrides.html":
        "Swap a real dependency for a test double with dependency_overrides, run the test, and see why the pattern makes FastAPI simple to test.",
    "fastapi/error_handling.html":
        "Raise an HTTPException, register a custom exception handler, and keep HTTP status codes out of the business logic that does the real work.",
    "fastapi/form_data_and_files.html":
        "Accept form fields and file uploads in a FastAPI endpoint, inspect the multipart body, and see why form data is not JSON or a query string.",
    "fastapi/headers_and_cookies.html":
        "Read a request header and a cookie inside a FastAPI endpoint, set a cookie on the response, and see what each transport is properly for.",
    "fastapi/http_methods_and_routing.html":
        "Map GET, POST, PUT and DELETE to handler functions, follow the matching logic, and see what each HTTP method promises to the caller.",
    "fastapi/lifespan_events.html":
        "Write a lifespan context manager that opens a connection pool at startup and closes it on shutdown, and see why per-request setup is wasteful.",
    "fastapi/openapi_and_docs.html":
        "Open the auto-generated Swagger UI, trace every field back to your type annotations, and see how much of an API's usability the schema decides.",
    "fastapi/path_parameters.html":
        "Add a path parameter with a type annotation, send a request with a wrong type, and watch FastAPI extract, convert and validate in one step.",
    "fastapi/project_structure.html":
        "Organise a FastAPI project into routers, models and dependencies across files and see a layout that scales without causing circular imports.",
    "fastapi/query_parameters.html":
        "Add query parameters with defaults and type hints, send a request, and watch FastAPI validate and document them from a single annotation.",
    "fastapi/reading_a_422.html":
        "Read a 422 validation error field by field, trace it back to the Pydantic model, and reshape the response into something callers can use.",
    "fastapi/request_bodies.html":
        "Define a Pydantic model and use it as a request body. One class gives you parsing, validation and OpenAPI documentation in a single declaration.",
    "fastapi/response_models.html":
        "Set a response_model on an endpoint, return a full ORM object, and watch FastAPI strip every field the model does not declare before sending.",
    "fastapi/router_and_global_dependencies.html":
        "Attach a dependency to a router so every endpoint under it runs the same check, and spot the unprotected endpoint the pattern catches.",
    "fastapi/security_basics.html":
        "Add OAuth2PasswordBearer as a dependency, extract and verify a token, and see how authentication fits into FastAPI's dependency injection.",
    "fastapi/status_codes.html":
        "Return the right HTTP status code for each outcome, compare it with 200-for-everything, and see the information the wrong choice discards.",
    "fastapi/sub_dependencies.html":
        "Chain dependencies that depend on other dependencies, follow the resolution order, and see FastAPI call each one correctly before your handler.",
    "fastapi/testing_fastapi.html":
        "Write tests with TestClient, call endpoints without a running server, override dependencies for isolation, and see what good tests assert.",
    "fastapi/what_is_fastapi.html":
        "See what FastAPI actually is: a thin layer over Starlette and Pydantic. Learn the two ideas that explain almost every feature it offers.",
    "fastapi/your_first_endpoint.html":
        "Write a GET handler, run the app, call the endpoint, and see how the decorator, the return value and the route ordering rule fit together.",

    # --- Gen Ai (SEO batch) --------------------------------------
    "gen_ai/ann_indexing_hnsw_and_ivf.html":
        "Build an HNSW graph and an IVF index from the same vectors, run a nearest-neighbour query on each, and compare the recall-speed tradeoff.",
    "gen_ai/annoy_index.html":
        "Build a forest of random projection trees, query a point, and see how Annoy trades tree count for recall when finding nearest neighbours.",
    "gen_ai/caching_in_rag_pipelines.html":
        "Add query, embedding and prompt caches to a RAG pipeline, measure the latency and cost each one removes, and see where staleness matters.",
    "gen_ai/completeness_in_llm_evaluation.html":
        "Score a model answer for completeness against a reference, see why a correct response can still miss required points, and measure the gap.",
    "gen_ai/context_aware_chunking.html":
        "Chunk a document by headings and semantic boundaries instead of fixed token counts and see the retrieval accuracy gained by preserving context.",
    "gen_ai/corrective_rag.html":
        "Add a relevance filter between retrieval and generation, discard off-topic documents, and see how Corrective RAG stops answers built on noise.",
    "gen_ai/correctness_in_llm_evaluation.html":
        "Evaluate a model answer for factual correctness against a reference, compare automated and human scoring, and see why this dimension costs most.",
    "gen_ai/diskann_index.html":
        "Build a DiskANN graph on a billion vectors, serve queries from SSD with a small memory footprint, and see how the alpha parameter controls recall.",
    "gen_ai/distributed_retrieval_and_sharding.html":
        "Scale vector search across machines. Compare sharding strategies, see how routing works, and spot the latency-throughput trade-off at every split.",
    "gen_ai/flat_index.html":
        "Walk through a brute-force flat index, measure its exact-match guarantee, and learn when exhaustive search still beats every approximate method.",
    "gen_ai/groundedness_in_llm_evaluation.html":
        "Measure whether an LLM answer stays within the retrieved context. Compare groundedness to correctness and see how evaluators score each claim.",
    "gen_ai/hit_rate_at_k.html":
        "Calculate Hit Rate at k step by step, compare it to Recall at k, and see when a binary hit-or-miss metric is the right choice for retrieval.",
    "gen_ai/hnsw_index.html":
        "Build an HNSW graph layer by layer, trace a search from the top level down, and see how ef and M shape the speed-vs-recall trade-off.",
    "gen_ai/indexing_in_vector_databases.html":
        "See why brute-force comparison breaks at scale, survey the index families vector databases use, and understand what each one trades for speed.",
    "gen_ai/ivf_flat_index.html":
        "Cluster vectors into Voronoi cells, search only the nearest few, and watch nprobe trade recall for speed inside an inverted file index.",
    "gen_ai/ivf_pq_index.html":
        "Combine inverted file partitioning with product quantization, trace a query through both stages, and see why IVF-PQ scales to a billion vectors.",
    "gen_ai/mean_reciprocal_rank.html":
        "Compute MRR by hand on ranked lists, compare it to Precision at k, and see why the rank of the first correct result is often the right metric.",
    "gen_ai/permission_filtering_in_rag.html":
        "Stop a RAG system from surfacing documents the user cannot see. Compare pre-filter and post-filter approaches and weigh speed against safety.",
    "gen_ai/precision_at_k.html":
        "Calculate Precision at k for a ranked result list, compare it to Recall at k, and see why the fraction of relevant hits matters more in RAG.",
    "gen_ai/product_quantization.html":
        "Split a high-dimensional vector into subvectors, quantize each one separately, and watch product quantization shrink a billion vectors into RAM.",
    "gen_ai/queries_keys_and_values.html":
        "Trace a single attention step: see how a query matches a key, why the dot products are scaled, and what the weighted sum of values produces.",
    "gen_ai/recall_at_k.html":
        "Calculate Recall at k for a retriever, compare it to Precision at k, and understand why recall is usually the metric that gates RAG quality.",
    "gen_ai/recursive_chunking.html":
        "Split a document with recursive character chunking, watch it try each separator in turn, and see why this simple strategy is the default splitter.",
    "gen_ai/relevance_in_llm_evaluation.html":
        "Score whether an LLM answer actually addresses the question asked. Compare answer relevance to context relevance and see how evaluators separate them.",
    "gen_ai/scann_index.html":
        "See how anisotropic vector quantization preserves inner-product rankings better than standard methods, and why ScaNN wins on large-scale benchmarks.",
    "gen_ai/semantic_chunking.html":
        "Split text where the meaning shifts instead of where a character count runs out. Compare semantic chunking to fixed-size splits on real paragraphs.",
    "gen_ai/structure_aware_chunking.html":
        "Parse headings, lists and tables before splitting. See how structure-aware chunking keeps logical sections intact and beats character-based splitters.",
    "gen_ai/tf_idf.html":
        "Compute TF-IDF scores by hand, watch common words shrink and rare words rise, and see how a simple formula still powers keyword-based search.",

    # --- Interview (SEO batch) -----------------------------------
    "interview/accidental-quadratic-complexity.html":
        "Spot the hidden quadratic cost in four common loop patterns. Step through each one, count the real operations, and learn to catch the trap fast.",
    "interview/binary-search-on-the-answer.html":
        "Binary-search the answer space instead of an array. Solve the ship-capacity problem step by step and learn the template that fits dozens of variants.",
    "interview/binary-search-without-an-off-by-one.html":
        "Write binary search that terminates correctly every time. Trace the loop invariant, see where off-by-one errors hide, and fix them before they bite.",
    "interview/climbing-stairs.html":
        "Count the ways to climb n stairs taking 1 or 2 steps at a time. Build the recurrence, spot the Fibonacci pattern, and reduce space to O(1).",
    "interview/closures-and-late-binding.html":
        "Run the classic closure trap: a list of lambdas that all return the same value. See why Python binds late and three clean ways to fix it.",
    "interview/coin-change.html":
        "Find the fewest coins that make a target amount. See why greedy fails on certain denominations, build the DP table cell by cell, and trace back.",
    "interview/counting-with-dictionaries.html":
        "Count item frequencies with a plain dict, then with Counter. Find the k most common elements and see how the data structure choice changes the cost.",
    "interview/daily-temperatures.html":
        "Solve daily temperatures with a monotonic stack. Watch the stack shrink as each warmer day resolves earlier entries, and see why one pass is enough.",
    "interview/design-a-hashmap.html":
        "Build a hash map from scratch with put, get and remove. Choose a hash function, handle collisions with chaining, and test it against edge cases.",
    "interview/design-a-min-stack.html":
        "Design a stack that reports its minimum in O(1). Track the minimum at every push and see why a single extra variable is not enough.",
    "interview/design-an-lru-cache.html":
        "Build an LRU cache with O(1) get and put using a hash map and a doubly linked list. Step through insertions, lookups and evictions one by one.",
    "interview/does-len-count-characters-or-bytes.html":
        "Test len() on str, bytes and emoji. See when it counts characters, when it counts bytes, and why a single emoji can give you more than one.",
    "interview/edit-distance.html":
        "Fill in the edit-distance table for two strings. Watch insertions, deletions and substitutions compete, and trace back the cheapest transformation.",
    "interview/evaluate-reverse-polish-notation.html":
        "Evaluate a postfix expression with a stack. Push operands, pop for each operator, and trace through examples like 4 13 5 / + step by step.",
    "interview/find-the-duplicate-number.html":
        "Find the one duplicate in an array of n+1 integers from 1 to n without extra space. Apply Floyd's cycle detection and see why it works here.",
    "interview/find-versus-index-on-strings.html":
        "Compare str.find, str.index and the in operator side by side. See which raises, which returns -1, and pick the right one for each situation.",
    "interview/first-and-last-position.html":
        "Find the first and last index of a target in a sorted array with duplicates. Run two binary searches and see how each boundary is located.",
    "interview/first-non-repeating-character.html":
        "Find the first character in a string that appears only once. Compare a two-pass dictionary approach to an ordered-dict single-pass solution.",
    "interview/group-anagrams.html":
        "Group words that are anagrams of each other. Sort each word into a canonical key, collect matches in a dictionary, and see the cost of each step.",
    "interview/grouping-and-inverting-dictionaries.html":
        "Group records by a shared field and invert a dictionary so values become keys. See both operations in plain Python and with defaultdict.",
    "interview/house-robber.html":
        "Pick houses to rob without choosing two in a row. Build the DP recurrence, compare rob-or-skip at every step, and read off the maximum take.",
    "interview/how-does-a-python-dict-work.html":
        "Look inside CPython's dict: a hash table with open addressing. See the probe sequence, the compact layout, and why average-case lookup costs O(1).",
    "interview/implement-substring-search.html":
        "Implement strStr without the built-in. Slide a window across the text, compare character by character, and measure the brute-force cost.",
    "interview/is-versus-equals.html":
        "Test is vs == on integers, strings and lists. See the object id behind each, learn the small-integer cache rule, and know when identity matters.",
    "interview/isomorphic-strings.html":
        "Check whether two strings share the same character-to-character pattern. Map characters in both directions, catch conflicts, and handle edge cases.",
    "interview/kth-largest-element.html":
        "Find the kth largest element with a min-heap and with quickselect. Compare both approaches and see when each one wins on time and space.",
    "interview/list-versus-tuple-versus-deque.html":
        "Compare list, tuple, deque and array side by side. See the memory layout, the time cost of each operation, and when to reach for which one.",
    "interview/longest-common-prefix.html":
        "Find the longest common prefix shared by a list of strings. Compare vertical scanning to sorting-based approaches and see which finishes first.",
    "interview/longest-consecutive-sequence.html":
        "Find the longest run of consecutive integers in an unsorted array in O(n). Use a set to start only at sequence beginnings and skip the rest.",
    "interview/longest-increasing-subsequence.html":
        "Find the longest increasing subsequence with O(n squared) DP, then speed it up to O(n log n) with patience sorting and binary search.",
    "interview/longest-palindromic-substring.html":
        "Expand around every centre to find the longest palindromic substring. Handle both odd and even lengths and see why this beats brute-force checking.",
    "interview/longest-substring-without-repeating-characters.html":
        "Slide a window across the string, tracking seen characters in a set. Shrink on repeats, grow on new ones, and record the longest span found.",
    "interview/maximum-subarray-kadane.html":
        "Run Kadane's algorithm step by step. Decide at each element whether to extend or restart, and watch the maximum subarray sum update in real time.",
    "interview/memoisation-with-a-dictionary.html":
        "Cache recursive results in a dictionary to kill recomputation. Watch the call tree shrink from exponential to linear, then switch to lru_cache.",
    "interview/merge-intervals.html":
        "Sort intervals by start time, then merge overlaps in one pass. Trace through examples and see why sorting first makes the rest straightforward.",
    "interview/merge-k-sorted-sequences.html":
        "Merge k sorted lists with a min-heap. Push one element per list, pop the smallest, refill, and see why the total cost is O(n log k).",
    "interview/minimum-window-substring.html":
        "Shrink and expand a sliding window until it holds every character of t. Track character counts in a dictionary and record the smallest valid span.",
    "interview/modifying-a-collection-while-iterating.html":
        "See what breaks when you delete from a list or dict mid-loop. Trace the iterator state, watch the error, and learn the safe alternatives.",
    "interview/product-of-array-except-self.html":
        "Build prefix and suffix products in two passes to get the product of every other element, with no division and O(1) extra space.",
    "interview/queue-from-two-stacks.html":
        "Build a FIFO queue from two stacks. Push onto one, pop from the other, and see why every element moves at most twice for amortized O(1) cost.",
    "interview/remove-duplicates-in-place.html":
        "Walk a slow and fast pointer through a sorted array, overwriting duplicates in place. Return the new length and handle every edge case.",
    "interview/reverse-a-string.html":
        "Reverse a string with slicing, then do it in place on a character list with O(1) extra memory. Compare both approaches step by step.",
    "interview/rotate-an-array.html":
        "Rotate an array right by k positions in place using three reverses. Trace each reverse and see why the trick works without extra memory.",
    "interview/running-median-of-a-stream.html":
        "Keep two heaps as numbers arrive: a max-heap for the lower half and a min-heap for the upper. Report the median after every insertion in O(log n).",
    "interview/search-in-rotated-sorted-array.html":
        "Search a rotated sorted array in O(log n). Identify which half is sorted at each step, decide where the target can hide, and narrow the window.",
    "interview/sets-versus-lists-and-deduplication.html":
        "Switch from a list to a set and watch membership checks drop from O(n) to O(1). Deduplicate a sequence while preserving order with dict.fromkeys.",
    "interview/shallow-versus-deep-copy.html":
        "Copy a nested list with list(), copy() and deepcopy(). Mutate an inner list and see which copies notice the change and which stay independent.",
    "interview/sliding-window-maximum.html":
        "Track the maximum in a sliding window using a monotonic deque. Watch old and small values drop as the window advances, keeping every lookup O(1).",
    "interview/sort-colors-dutch-national-flag.html":
        "Partition an array of 0s, 1s and 2s in one pass using three pointers. Watch low, mid and high converge until the array is sorted in place.",
    "interview/str-versus-bytes-in-python.html":
        "Compare str and bytes objects side by side. Encode a string to bytes, decode it back, and see where the boundary between text and binary sits.",
    "interview/string-compression.html":
        "Compress aabcccccaaa into a2b1c5a3 with a single scan. Count consecutive runs, build the result, and return the original when compression is longer.",
    "interview/string-interning-and-the-is-operator.html":
        "See which strings Python interns and which it does not. Test is on literals and computed strings, and learn why the result is unpredictable.",
    "interview/subarray-sum-equals-k.html":
        "Count subarrays that sum to k using a running prefix sum and a hash map. See why brute force costs O(n squared) and the hash approach costs O(n).",
    "interview/the-mutable-default-argument.html":
        "Call a function with a default list twice and watch the list remember. See why Python evaluates defaults once, and three clean ways to fix it.",
    "interview/the-nested-list-multiplication-bug.html":
        "Create [[0]*3]*3, write to one cell, and watch every row change. See the shared-reference diagram and build the grid the safe way instead.",
    "interview/three-sum.html":
        "Find every unique triple that sums to zero. Sort the array, fix one element, and sweep two pointers inward while skipping duplicates at each step.",
    "interview/top-k-frequent-elements.html":
        "Find the k most frequent elements using a heap and using bucket sort. Compare both approaches and see when each one gives a better time bound.",
    "interview/trapping-rain-water.html":
        "Calculate trapped water bar by bar. Precompute left and right maxima in two passes, then shrink to O(1) space with two converging pointers.",
    "interview/two-sum.html":
        "Solve Two Sum in one pass with a hash map. Store each number's index, check for its complement, and return the pair the moment it appears.",
    "interview/valid-anagram.html":
        "Check whether two strings are anagrams by counting every character in a dictionary. Compare the sorted approach to the counted one and time both.",
    "interview/valid-palindrome.html":
        "Check whether a string is a palindrome after stripping punctuation and lowering case. Walk two pointers inward and compare characters one by one.",
    "interview/valid-parentheses.html":
        "Push openers onto a stack and pop when a closer arrives. Walk through balanced and unbalanced bracket strings to see every edge case handled.",
    "interview/what-a-decorator-replaces.html":
        "See what the @ line does to a function object. Trace the replacement, add functools.wraps, and understand why the original name disappears without it.",
    "interview/what-does-string-slicing-cost.html":
        "Slice a Python string and measure the cost. See that slicing copies the data every time, count the bytes moved, and spot when it hides an O(n) hit.",
    "interview/what-does-yield-actually-do.html":
        "Step through a generator function one yield at a time. See the suspended frame, compare memory use to a list, and chain generators with yield from.",
    "interview/what-is-a-python-list-underneath.html":
        "Look inside CPython's list: a resizable array of pointers. See why append is amortized O(1), insert(0, x) is O(n), and indexing is constant-time.",
    "interview/what-with-guarantees.html":
        "Trace a with block that raises an exception. See the __enter__ and __exit__ calls, check whether the error propagates, and know what is guaranteed.",
    "interview/why-a-comprehension-is-faster.html":
        "Time a list comprehension against the equivalent for-loop. Read the bytecode, count the attribute lookups saved, and see where the speedup lives.",
    "interview/why-are-python-strings-immutable.html":
        "See why Python strings cannot change in place. Trace what happens when you concatenate, check the object id, and understand the hashing guarantee.",
    "interview/why-is-in-slow-on-a-list.html":
        "Time x in my_list versus x in my_set as the collection grows. See the O(n) scan, the O(1) hash lookup, and know when to switch to a set.",
    "interview/why-must-dict-keys-be-hashable.html":
        "Try a list as a dictionary key and watch it fail. See why hash consistency matters for lookups, what makes tuples work, and which objects qualify.",

    # --- Machine Learning (SEO batch) ----------------------------
    "machine_learning/choosing_k.html":
        "Run the Elbow method and the Silhouette score on the same dataset. See what each one measures, where they disagree, and how to pick k when they do.",
    "machine_learning/data_leakage.html":
        "Spot data leakage in a pipeline before it inflates your metrics. See train-test contamination, target leakage, and preprocessing leaks with examples.",
    "machine_learning/dbscan_clustering.html":
        "Set epsilon and minPts, then watch DBSCAN grow clusters by density. See how it finds arbitrary shapes, labels noise, and never asks you to choose k.",
    "machine_learning/feature_scaling.html":
        "Apply min-max and standard scaling to raw features. See which models need scaled inputs, which ignore them, and what happens when one column dominates.",
    "machine_learning/gaussian_mixture_models.html":
        "Fit a Gaussian mixture and watch each point split its membership across clusters. Step through EM iteration by iteration and compare to hard k-means.",
    "machine_learning/grid_vs_random_search.html":
        "Compare grid and random hyperparameter search side by side. See how random sampling covers more of the space with the same trial budget.",
    "machine_learning/handling_missing_values.html":
        "Learn four strategies for handling missing data. Watch each method change predictions on the same dataset and pick the one that fits.",
    "machine_learning/hierarchical_clustering.html":
        "Build a clustering tree from pairwise distances and read a dendrogram to choose the number of clusters after the algorithm finishes.",
    "machine_learning/isolation_forest.html":
        "Watch isolation forest flag anomalies by counting how few random splits isolate a point. Fewer splits means the data point is stranger.",
    "machine_learning/learning_curves.html":
        "Plot training and validation error against dataset size. Read the gap to decide whether more data or more model capacity will help.",
    "machine_learning/ml_pipelines.html":
        "Chain preprocessing and modelling into one pipeline object that prevents data leakage and locks every step into the correct order.",
    "machine_learning/outliers_and_influence.html":
        "Move one data point and watch the regression line follow it. Use Cook's distance and hat values to find the rows that control your model.",
    "machine_learning/partial_dependence_and_shap.html":
        "Plot partial dependence, ICE curves and SHAP values for one feature. See where partial dependence hides interactions the others reveal.",
    "machine_learning/permutation_importance.html":
        "Shuffle one feature at a time and measure the drop in accuracy. See why correlated features split the importance and how to handle it.",
    "machine_learning/precision_recall_and_f1.html":
        "Build a confusion matrix, then adjust the threshold and watch precision trade against recall while F1 tries to balance them both.",
    "machine_learning/precision_recall_vs_roc.html":
        "Draw ROC and precision-recall curves from the same predictions. See why a model that looks strong on ROC can fail on imbalanced classes.",
    "machine_learning/probability_calibration.html":
        "Check whether predicted probabilities match observed frequencies. Apply Platt scaling and isotonic regression to close the gap.",
    "machine_learning/stacking_and_voting.html":
        "Combine trees, linear models and neighbours into one ensemble. Compare hard voting, soft voting and stacking on the same scored data.",
    "machine_learning/threshold_tuning.html":
        "Slide the classification threshold from zero to one and watch precision, recall and cost shift. Find the cutoff that fits your problem.",
    "machine_learning/tsne_and_umap.html":
        "Project high-dimensional data with PCA, t-SNE and UMAP side by side. Learn which visual patterns are real structure and which are artifacts.",

    # --- Maths (SEO batch) ---------------------------------------
    "maths/basis_span_and_orthogonality.html":
        "Add vectors to a set and watch the span grow. See why orthogonal bases make projections simple and what happens when vectors depend.",
    "maths/bernoulli_binomial_poisson.html":
        "Start from a single coin flip and build the binomial and Poisson distributions step by step. See the limit that connects each to the next.",
    "maths/central_limit_theorem.html":
        "Sample from skewed, uniform and bimodal distributions. Watch the sample mean become normal as the sample size grows, and see where it fails.",
    "maths/cholesky_and_positive_definiteness.html":
        "Factor a positive-definite matrix into a lower triangle times its transpose. Watch the decomposition break when definiteness fails.",
    "maths/combinatorics.html":
        "Count arrangements with and without order, with and without replacement. One decision tree picks the right formula every time.",
    "maths/confidence_intervals.html":
        "Draw a thousand confidence intervals and count how many capture the true mean. See what the ninety-five percent actually refers to.",
    "maths/convexity_and_optimisation.html":
        "See why a convex loss surface has one minimum and gradient descent always finds it. Then watch what happens when convexity disappears.",
    "maths/expectation_and_variance.html":
        "Calculate expected value and variance from a probability distribution. Apply the linearity and independence rules that simplify real problems.",
    "maths/hypothesis_testing_and_p_values.html":
        "Run a hypothesis test step by step. See what the p-value actually measures and why a small one does not mean the effect is large.",
    "maths/jacobian_and_hessian.html":
        "Compute the Jacobian and Hessian for small functions. See how optimisers use first and second derivatives to choose direction and step size.",
    "maths/jensens_inequality.html":
        "Apply a convex function before and after averaging and see why the results differ. Trace how this gap appears in KL divergence and the ELBO.",
    "maths/lagrange_multipliers.html":
        "Optimise a function under a constraint by introducing a multiplier. See how the multiplier itself tells you the cost of the constraint.",
    "maths/markov_chains.html":
        "Step through a Markov chain and watch the state distribution converge to steady state. See why MCMC sampling and PageRank are both examples.",
    "maths/matrix_calculus.html":
        "Work through the matrix derivative identities used in backpropagation. Use dimension analysis to verify each gradient before coding it.",
    "maths/qr_decomposition.html":
        "Orthogonalise a set of vectors with Gram-Schmidt and factor the matrix into Q times R. See why this makes least squares numerically stable.",
    "maths/quantiles_and_percentiles.html":
        "Compute quantiles, percentiles and the interquartile range. See why rank-based summaries describe skewed data better than the mean.",
    "maths/sampling_distributions.html":
        "Simulate thousands of samples and plot the distribution of the sample mean. Watch the standard error shrink as the sample size grows.",
    "maths/singular_value_decomposition.html":
        "Factor any matrix into U, Sigma and V-transpose. Truncate to k components and watch the low-rank reconstruction improve as k increases.",
    "maths/taylor_series.html":
        "Expand a function into a polynomial term by term. Watch the approximation improve near the centre and fail past the radius of convergence.",
    "maths/type_i_and_type_ii_errors.html":
        "Adjust significance level and sample size and watch Type I and Type II error rates trade off. See what statistical power actually measures.",

    # --- Matplotlib (SEO batch) ----------------------------------
    "matplotlib/annotations.html":
        "Add text labels, arrows and reference lines to a matplotlib chart. Turn a bare plot into one that tells the reader what to notice.",
    "matplotlib/axis_limits_and_ticks.html":
        "Set axis limits, tick positions, tick labels and log scales in matplotlib. Control exactly what the axis shows and how it reads.",
    "matplotlib/bar_charts.html":
        "Build vertical, horizontal, grouped and stacked bar charts in matplotlib. See why the y-axis must start at zero and when to reorder bars.",
    "matplotlib/box_and_violin.html":
        "Draw box plots and violin plots side by side in matplotlib. Compare what each summary shows and what each one hides about the distribution.",
    "matplotlib/choosing_a_chart.html":
        "Match your data question to the right chart type. Walk through a decision tree that picks between bar, line, scatter and histogram.",
    "matplotlib/colours_and_colormaps.html":
        "Pick colours by name, hex or RGB in matplotlib. Choose a colormap that is perceptually uniform and still readable in greyscale.",
    "matplotlib/common_mistakes.html":
        "Spot the matplotlib mistakes that produce a chart which looks correct but misrepresents the data. Fix truncated axes and dual-axis traps.",
    "matplotlib/dates_on_axes.html":
        "Plot time series in matplotlib with proper date axes. Set locators and formatters so that date labels stay readable without overlapping.",
    "matplotlib/error_bars_and_bands.html":
        "Add error bars and shaded confidence bands to a matplotlib plot. Label whether you are showing standard deviation, standard error or a CI.",
    "matplotlib/histograms.html":
        "Plot a histogram in matplotlib and change the bin count. Watch the same data appear to tell a different story depending on the bins chosen.",
    "matplotlib/images_and_heatmaps.html":
        "Display images and heatmaps with imshow and pcolormesh in matplotlib. Fix the upside-down origin and choose a colormap that reads correctly.",
    "matplotlib/labels_and_legends.html":
        "Add axis labels, a title and a legend to a matplotlib figure. Make a chart that someone else can read without asking what it shows.",
    "matplotlib/layout_and_spacing.html":
        "Set figure size, margins and subplot spacing in matplotlib. Use constrained_layout to stop labels and titles from overlapping automatically.",
    "matplotlib/line_plots.html":
        "Draw single and multiple-line plots with matplotlib's plot function. Set colours, markers, line styles and labels with the arguments that matter.",
    "matplotlib/performance.html":
        "Speed up slow matplotlib figures that render too many points. Use rasterisation, line simplification and collections to stay responsive.",
    "matplotlib/plotting_from_pandas.html":
        "Create charts from a pandas DataFrame in one line with df.plot. See when the shortcut works and when to fall back to raw matplotlib calls.",
    "matplotlib/saving_figures.html":
        "Save matplotlib figures with savefig. Set the DPI, file format and bounding box so the saved image matches what you see on screen.",
    "matplotlib/scatter_plots.html":
        "Build scatter plots with matplotlib's scatter function. Map colour and size to data columns and encode four dimensions in one chart.",
    "matplotlib/styles_and_rcparams.html":
        "Apply built-in styles and set rcParams to restyle every matplotlib chart at once. Create a consistent look without repeating style code.",
    "matplotlib/subplots.html":
        "Create grids of subplots with plt.subplots and GridSpec in matplotlib. Place multiple axes on one figure with controlled sizes and spacing.",
    "matplotlib/twin_axes.html":
        "Add a second y-axis to a matplotlib plot with twinx. See why dual axes can mislead readers and learn the safer alternatives for two scales.",
    "matplotlib/what_is_matplotlib.html":
        "Learn the difference between Figure and Axes in matplotlib. Understand the two APIs, pyplot and object-oriented, and when to use each one.",

    # --- Numpy (SEO batch) ---------------------------------------
    "numpy/aggregations_and_axis.html":
        "Run sum, mean and max on a NumPy array and change the axis argument. See how one parameter decides whether the result is a row, column or scalar.",
    "numpy/boolean_masking.html":
        "Write a comparison on a NumPy array and use the resulting boolean array as an index. Filter, count and replace elements without any loop.",
    "numpy/broadcasting.html":
        "Add a row vector to a column vector and watch NumPy expand the shapes automatically. Learn the two rules that decide when broadcasting works.",
    "numpy/creating_arrays.html":
        "Create NumPy arrays with array, zeros, arange, linspace and random. See which constructor fits each situation and what dtype each one picks.",
    "numpy/dtypes.html":
        "Set and inspect the dtype of a NumPy array. See how integer overflow, float precision and type promotion affect calculations without warning.",
    "numpy/fancy_indexing.html":
        "Index a NumPy array with a list of positions to reorder, repeat or select scattered elements. See how the index shape decides the output shape.",
    "numpy/indexing_and_slicing.html":
        "Slice rows, columns and blocks from a NumPy array. Learn the one slicing behaviour that differs from Python lists and why it matters.",
    "numpy/linear_algebra.html":
        "Multiply matrices, solve linear systems and compute eigenvalues with NumPy. See why you should call solve instead of computing the inverse.",
    "numpy/nan_and_missing_data.html":
        "Work with NaN values in NumPy. Learn why NaN breaks comparisons and aggregations, and switch to nanmean and nansum to handle it correctly.",
    "numpy/performance_and_memory.html":
        "Profile a NumPy workflow to find where time and memory go. Replace Python loops, cut unnecessary copies and pick smaller dtypes.",
    "numpy/random_numbers.html":
        "Generate random integers, floats and samples with NumPy's Generator API. Set a seed for reproducible results and avoid the legacy functions.",
    "numpy/saving_and_loading.html":
        "Save and load NumPy arrays with npy, npz and text formats. Compare speed, file size and portability to choose the right format for your data.",
    "numpy/shape_and_reshape.html":
        "Reshape a NumPy array without copying data. Use reshape, ravel and newaxis to rearrange dimensions while the underlying memory stays put.",
    "numpy/sorting_and_searching.html":
        "Sort a NumPy array, get sorted indices with argsort and find insertion points with searchsorted. See why argsort is usually the more useful call.",
    "numpy/stacking_and_splitting.html":
        "Join NumPy arrays with vstack, hstack and concatenate. Split them with array_split and see when to stack along a new axis instead.",
    "numpy/transpose_and_axes.html":
        "Transpose a NumPy array and reorder its axes with swapaxes and moveaxis. See how the operation changes strides without copying any data.",
    "numpy/unique_and_set_operations.html":
        "Find unique values, counts and set intersections in a NumPy array. Rebuild the original from the unique values and an inverse index.",
    "numpy/vectorised_arithmetic.html":
        "Replace Python loops with NumPy element-wise operations. See the speedup on arrays of every size and avoid the two patterns that lose it.",
    "numpy/views_vs_copies.html":
        "Learn which NumPy operations return a view and which return a copy. Modify a slice and see the change appear, or not, in the original array.",
    "numpy/what_is_numpy.html":
        "See why NumPy stores numbers in one contiguous block of typed memory and how that layout makes array operations orders of magnitude faster.",

    # --- Pandas (SEO batch) --------------------------------------
    "pandas/adding_and_dropping.html":
        "Add, rename and drop columns in a pandas DataFrame with assign and drop. See how index alignment decides what a new column contains.",
    "pandas/apply_and_map.html":
        "Use apply, map and applymap on a pandas DataFrame. Measure the speed cost and see the vectorised alternatives that usually replace them.",
    "pandas/concat.html":
        "Stack DataFrames vertically or horizontally with pandas concat. Control index alignment, handle mismatched columns and reset the index.",
    "pandas/counting_and_binning.html":
        "Count category frequencies with value_counts, bin continuous data with cut and qcut, and build cross-tabulations with crosstab in pandas.",
    "pandas/creating_dataframes.html":
        "Build pandas DataFrames from dictionaries, lists of records, NumPy arrays and CSV files. See which constructor fits each data shape.",
    "pandas/datetimes.html":
        "Parse date strings into pandas datetime, use the dt accessor for components and resample time series. Fix the text dates that break analysis.",
    "pandas/dtypes_and_memory.html":
        "Inspect and convert column dtypes in a pandas DataFrame. Switch object columns to category or nullable types and measure the memory saved.",
    "pandas/duplicates.html":
        "Find, count and remove duplicate rows in a pandas DataFrame. Choose which copy to keep and verify the cleaned result matches expectations.",
    "pandas/filtering_rows.html":
        "Filter pandas rows with boolean masks, isin, between and query. Learn the parenthesis rule for combining conditions that trips every beginner.",
    "pandas/groupby_basics.html":
        "Split a DataFrame by one or more columns, apply aggregations and combine the results. See the split-apply-combine pattern that defines groupby.",
    "pandas/groupby_transform.html":
        "Use transform to broadcast group statistics back to every row and filter to keep only groups that pass a test. Compare both to plain groupby.",
    "pandas/inspecting_data.html":
        "Run shape, dtypes, describe, info, head and value_counts on a new dataset. Build the six-call habit that catches problems before analysis.",
    "pandas/loc_and_iloc.html":
        "Select rows and columns by label with loc and by position with iloc. See the endpoint rule that differs between them and why it matters.",
    "pandas/merge_and_join.html":
        "Join two DataFrames with pandas merge using inner, left, right and outer joins. Spot the duplicate key that silently multiplies your rows.",
    "pandas/method_chaining.html":
        "Write a pandas analysis as one chained expression. Compare chained and step-by-step styles and see when pipe and assign keep the chain clean.",
    "pandas/missing_data.html":
        "Find, count and handle missing values in a pandas DataFrame with isna, dropna and fillna. Pick a strategy based on why the data is missing.",
    "pandas/multiindex.html":
        "Build and slice a pandas MultiIndex on rows or columns. Use xs and IndexSlice for clean lookups and see when to call reset_index instead.",
    "pandas/performance.html":
        "Profile a slow pandas workflow and fix the top bottlenecks. Replace row-level loops, shrink memory with better dtypes and go vectorised.",
    "pandas/pivot_and_melt.html":
        "Reshape a pandas DataFrame from long to wide with pivot_table and back again with melt. See when each shape is the right one for your task.",
    "pandas/reading_and_writing.html":
        "Read CSV files into DataFrames with the right arguments and avoid the silent bugs that wrong defaults let through.",
    "pandas/sorting_and_ranking.html":
        "Sort rows by one column or several, find the top N values with nlargest, and see where NaN lands in each method.",
    "pandas/string_methods.html":
        "Use the .str accessor to split, replace and test text columns, and learn how each method handles missing values.",
    "pandas/the_copy_warning.html":
        "Understand why chained indexing makes assignments silently fail, and how to write the line that actually changes the DataFrame.",
    "pandas/the_index.html":
        "See how the pandas Index labels rows, aligns data during joins and arithmetic, and changes the result of almost every operation.",
    "pandas/time_series.html":
        "Resample timestamps into intervals, compute rolling averages, and shift rows forward or back to compare periods side by side.",
    "pandas/what_is_pandas.html":
        "Learn what pandas adds to NumPy: named columns, typed data, a row index and the operations that make tabular analysis fast.",

    # --- Pydantic (SEO batch) ------------------------------------
    "pydantic/aliases.html":
        "Map camelCase payloads, reserved Python names and legacy fields to clean attribute names using aliases and AliasPath.",
    "pydantic/annotated_and_custom_types.html":
        "Define a validation rule once with Annotated and reuse it across models instead of copying the same constraint into every field.",
    "pydantic/collections_of_models.html":
        "Validate lists, dicts, sets and tuples of models, and get error messages that point to the exact index or key that failed.",
    "pydantic/computed_fields.html":
        "Add read-only fields that compute their value from other attributes and appear in serialized output without being part of input.",
    "pydantic/custom_serializers.html":
        "Control how individual fields or entire models serialize, and understand when leaving the default alone is the better choice.",
    "pydantic/dates_uuids_and_decimals.html":
        "Parse ISO dates, UUIDs and Decimals from raw strings, and avoid the two conversion traps that silently produce wrong numbers.",
    "pydantic/enums_and_literals.html":
        "Restrict a field to a fixed set of values using Enum or Literal, and see when each approach fits your data model best.",
    "pydantic/field_constraints.html":
        "Use Field to set min, max, regex and other constraints that close the gap between what a type allows and what your domain accepts.",
    "pydantic/field_validator.html":
        "Write custom validation and normalisation logic with field_validator, and see exactly where each mode runs in the pipeline.",
    "pydantic/generic_models.html":
        "Build one generic model for paginated responses, wrapped results or envelopes, then reuse it across every resource type.",
    "pydantic/json_schema.html":
        "Generate a JSON Schema from any Pydantic model and see why that automatic document powers OpenAPI, FastAPI and every tool that reads your API.",
    "pydantic/migrating_v1_to_v2.html":
        "Walk through the renames, the silent behaviour changes and the patterns that break when moving a Pydantic v1 codebase to v2.",
    "pydantic/model_config.html":
        "Set model-wide behaviour with model_config: extra keys, frozen instances, strict mode and assignment validation in one place.",
    "pydantic/model_dump_and_model_dump_json.html":
        "Export a model with model_dump and model_dump_json, apply include and exclude filters, and avoid the TypeError most people hit first.",
    "pydantic/model_validator.html":
        "Write validators that compare multiple fields at once using model_validator, and choose between before and after modes.",
    "pydantic/nested_models.html":
        "Compose models inside models so nested JSON validates recursively, with error paths that name the exact field at every depth.",
    "pydantic/parsing_json.html":
        "Parse JSON directly into a model with model_validate_json and see why it is faster and stricter than json.loads plus model_validate.",
    "pydantic/performance_and_pydantic_core.html":
        "See why Pydantic v2 validates at Rust speed, where the time goes, and which three habits make the biggest performance difference.",
    "pydantic/pydantic_vs_dataclasses.html":
        "Compare Pydantic BaseModel with Python dataclasses side by side and see that validation at creation time is the deciding factor.",
    "pydantic/pydantic_with_fastapi.html":
        "See how FastAPI turns Pydantic models into request validation, response shaping and automatic API documentation with no extra code.",
    "pydantic/reading_a_validation_error.html":
        "Read a Pydantic ValidationError line by line, understand loc, msg and type, and turn the report into a message your caller can use.",
    "pydantic/required_optional_and_defaults.html":
        "Learn why Optional does not mean optional in Pydantic, and how to distinguish required, defaulted and nullable fields correctly.",
    "pydantic/settings_management.html":
        "Load configuration from environment variables into a typed Pydantic model that validates every value before your application starts.",
    "pydantic/strict_vs_lax_mode.html":
        "Choose between strict and lax validation per field or per model, and learn where coercion helps at the edge and hides bugs inside.",
    "pydantic/type_adapter.html":
        "Validate any type annotation without building a model, using TypeAdapter for standalone checks on lists, dicts and primitives.",
    "pydantic/types_and_coercion.html":
        "See exactly what Pydantic will and will not convert: the coercion rules for strings, ints, floats and booleans, one example at a time.",
    "pydantic/unions_and_discriminated_unions.html":
        "Handle fields that accept multiple shapes with Union, and add a discriminator so Pydantic picks the right branch without guessing.",
    "pydantic/validator_modes.html":
        "Compare before, after, plain and wrap validator modes, and see how each one interacts with Pydantic's coercion step.",
    "pydantic/what_is_pydantic.html":
        "See how Pydantic turns Python type annotations into runtime checks that reject bad data the moment it arrives.",
    "pydantic/your_first_basemodel.html":
        "Define a Pydantic BaseModel, create an instance from raw data, trigger a validation error on purpose, and export the result as a dict.",

    # --- Python (SEO batch) --------------------------------------
    "python/args_and_kwargs.html":
        "Collect any number of positional arguments with *args and keyword arguments with **kwargs, and see how both work inside a function.",
    "python/classes_and_objects.html":
        "Build a class that bundles data with methods, create instances from it, and see how self connects each object to its own attributes.",
    "python/conditional_comprehensions.html":
        "Add an if clause to a list comprehension in two positions and see how filtering differs from choosing between two values.",
    "python/conditional_expressions.html":
        "Write a conditional expression that picks one of two values in a single line and see where it fits better than a full if/else block.",
    "python/dict_and_set_comprehensions.html":
        "Build dictionaries and sets with comprehension syntax, and see how the same loop-in-an-expression pattern works beyond lists.",
    "python/dictionary_methods.html":
        "Use get, setdefault, update and items to handle dictionaries without the repeated key checks most people write by hand.",
    "python/enumerate_function.html":
        "Loop through a sequence with enumerate to get the index and item together, and stop tracking positions with a counter variable.",
    "python/f_strings_and_formatting.html":
        "Place expressions inside f-strings, apply format specs for alignment and precision, and see how Python turns values into readable text.",
    "python/files_and_with.html":
        "Open, read and write files using the with statement so Python closes them even when your code raises an exception.",
    "python/function_arguments.html":
        "Pass arguments by position or by name, set defaults, and see how Python matches each call to the parameters a function expects.",
    "python/generators_and_yield.html":
        "Write a generator that yields values one at a time instead of building a full list, and see how pausing a function saves memory.",
    "python/inheritance.html":
        "Build a child class that inherits methods and attributes from a parent, override what differs, and call super() to extend behaviour.",
    "python/input_and_output.html":
        "Read user input with input(), print output with print(), and handle the string-to-number conversion that trips up most beginners.",
    "python/lambda_map_filter.html":
        "Write small throwaway functions with lambda, apply them across sequences with map and filter, and see where a comprehension is clearer.",
    "python/list_comprehensions.html":
        "Build a list in one expression using a comprehension, and compare it with the loop-and-append pattern it replaces.",
    "python/loop_else.html":
        "Attach an else clause to a for or while loop so a block of code runs only when the loop finishes without hitting break.",
    "python/match_and_case.html":
        "Use match/case to test a value against patterns instead of chains of if/elif, and see how destructuring pulls values out of the match.",
    "python/modules_and_import.html":
        "Import a module, understand what Python runs when you do, and organise your own code into files that other scripts can reuse.",
    "python/mutability_and_aliasing.html":
        "See why assigning a list to a second name does not copy it, and how mutability makes two variables change the same object at once.",
    "python/nested_conditionals.html":
        "Read and write nested if statements, then refactor the ones that grew too deep into flat guard clauses that are easier to follow.",
    "python/nested_data_structures.html":
        "Work with lists of dictionaries, nested records and mixed structures, and write the loops and lookups that reach any value inside them.",
    "python/nested_for_loops.html":
        "Run a loop inside a loop, trace the execution order step by step, and learn when a product of two ranges is the right structure.",
    "python/none_and_truthiness.html":
        "Learn which values Python treats as false in a condition, how None differs from zero and empty, and why is None beats == None.",
    "python/range_step.html":
        "Generate number sequences with range using start, stop and step, and see why range produces values lazily instead of building a list.",
    "python/sets_and_set_operations.html":
        "Create sets, remove duplicates, and use union, intersection and difference to compare collections without writing nested loops.",
    "python/shallow_and_deep_copy.html":
        "Copy a list with slicing or copy(), see that the inner objects stay shared, and use deepcopy when you need a fully independent clone.",
    "python/slicing_step_negatives.html":
        "Slice sequences with start, stop and step, reverse them with [::-1], and see how negative indices count from the end.",
    "python/sorted_with_key.html":
        "Sort any iterable with sorted(), pass a key function to control the comparison, and see how reverse and stable ordering interact.",
    "python/string_methods.html":
        "Split, join, strip and test strings with Python's built-in methods, and see how each one returns a new string instead of changing the original.",
    "python/try_and_except.html":
        "Catch specific exceptions with try/except, handle them without crashing, and see why bare except clauses hide the bugs you need to find.",
    "python/tuples_and_unpacking.html":
        "Create tuples, unpack them into separate variables, and learn where an immutable sequence fits better than a list.",
    "python/type_conversion.html":
        "Convert between strings, integers and floats with int(), float() and str(), and see the errors Python raises when a conversion is impossible.",
    "python/variable_scope.html":
        "Trace how Python resolves a name through local, enclosing, global and built-in scopes, and see why assigning inside a function creates a new local.",
    "python/zip_function.html":
        "Pair items from two or more sequences with zip, iterate them in lockstep, and see what happens when the sequences have different lengths.",

    # --- Sklearn (SEO batch) -------------------------------------
    "sklearn/a_complete_workflow.html":
        "Follow one dataset through loading, splitting, scaling, encoding, fitting and scoring to see every scikit-learn step in context.",
    "sklearn/class_imbalance.html":
        "Handle datasets where the interesting class is rare, compare four remedies and measure each one with the metric that actually fits.",
    "sklearn/classification_metrics.html":
        "Choose between accuracy, precision, recall and F1 by asking which mistakes matter most, and see why 99 percent accuracy can mean nothing.",
    "sklearn/column_transformer.html":
        "Apply different preprocessing to different columns using ColumnTransformer, so numeric features scale while categoricals encode.",
    "sklearn/confusion_matrix.html":
        "Build a confusion matrix from predictions, name each of the four cells, and compute precision, recall and F1 from them by hand.",
    "sklearn/cross_validation.html":
        "Replace a single train/test split with cross-validation to see the variance behind every score and pick a model you can trust.",
    "sklearn/data_leakage.html":
        "Spot data leakage before it inflates your score: learn the patterns that let test information leak into training and how pipelines prevent them.",
    "sklearn/decision_trees.html":
        "Fit a decision tree, read its splits as plain rules, and see why a single tree overfits and how pruning brings it back.",
    "sklearn/encoding_categoricals.html":
        "Turn categorical columns into numbers with OrdinalEncoder and OneHotEncoder, and learn which choice invents a fact and which does not.",
    "sklearn/hyperparameter_search.html":
        "Search for the best hyperparameters with GridSearchCV and RandomizedSearchCV, and measure each combination fairly with cross-validation.",
    "sklearn/kmeans_clustering.html":
        "Group data points into clusters with k-means, measure fit with inertia and silhouette score, and see how the algorithm converges.",
    "sklearn/linear_regression.html":
        "Fit a linear regression, read its coefficients and intercept, and learn why the numbers are misread more often than any other model's.",
    "sklearn/loading_and_shaping_data.html":
        "Load a dataset into a feature matrix and target vector with the exact shapes scikit-learn expects before any model can be fitted.",
    "sklearn/logistic_regression.html":
        "Train a logistic regression classifier, interpret its coefficients as log-odds, and see why it is the model to try first on any problem.",
    "sklearn/missing_values.html":
        "Fill gaps in your data with SimpleImputer, understand when the gap itself carries information, and keep imputation inside a pipeline.",
    "sklearn/overfitting_and_underfitting.html":
        "Spot overfitting and underfitting from training and test scores, and apply the opposite fix each failure needs to close the gap.",
    "sklearn/pipelines.html":
        "Chain preprocessing and a model into one Pipeline so every transformation fits on training data only and every score stays honest.",
    "sklearn/probabilities_and_thresholds.html":
        "Move the classification threshold away from 0.5, plot a precision-recall curve, and decide the cut-off that matches your cost trade-off.",
    "sklearn/random_forests.html":
        "Combine hundreds of decision trees into a random forest that averages out each tree's instability and resists overfitting.",
    "sklearn/regression_metrics.html":
        "Compare MAE, MSE, RMSE and R-squared on the same predictions, and see why R-squared alone rarely tells you whether a model is good enough.",
    "sklearn/scaling_features.html":
        "Scale features with StandardScaler and MinMaxScaler, and learn which models break without scaling and which ignore it entirely.",
    "sklearn/train_test_split.html":
        "Split data into training and test sets with train_test_split, and see why scoring a model on the data it memorised tells you nothing.",
    "sklearn/what_is_scikit_learn.html":
        "Learn the fit/predict/transform interface that every scikit-learn estimator shares, and see why one API covers two hundred algorithms.",
}

# The named-architecture modules (tools/arch_topics.py) write their own, one
# per entry, so adding a module does not mean remembering to edit this file.
from arch_topics import DESCRIPTIONS as _ARCH_DESCRIPTIONS  # noqa: E402

DESCRIPTIONS.update(_ARCH_DESCRIPTIONS)
