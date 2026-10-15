# -*- coding: utf-8 -*-
"""Prose for the homepage: one paragraph per track, and the featured modules.

The homepage used to be the whole catalogue - 637 module cards, 748 links and
not one paragraph of two sentences - which reads as a directory rather than a
page. It now shows each track as a card with a short paragraph, linking to
the track's own page where the full module list lives, plus a short list of
featured modules with a sentence or two each.

Every paragraph here is written for the homepage, not copied from the track
pages or the module pages, so the same text does not appear on two URLs.

Read by tools/build_prerender.py (TRACK_BLURBS) and tools/build_hub.py
(FEATURED).
"""

# Keyed by lib_pages.TOPICS key. 40-50 words each.
TRACK_BLURBS = {
    "maths": (
        "The maths machine learning quietly assumes, taught by moving it: drag a "
        "vector and watch the dot product change sign, sweep a matrix until its "
        "eigenvectors appear, shrink a secant into a derivative. Linear algebra, "
        "calculus, probability and statistics, from the equation of a line to SVD."
    ),
    "ml": (
        "Classical machine learning end to end. Split and scale the data, fit "
        "regressions, trees, SVMs and clusters on the page, then measure them "
        "honestly with confusion matrices, ROC curves and cross-validation - "
        "including the leakage and threshold mistakes that make a good score "
        "untrustworthy."
    ),
    "dl": (
        "Neural networks from a single perceptron upward. Build layers, watch "
        "loss fall, step through backpropagation one local gradient at a time, "
        "and see what optimizers, normalisation, dropout and early stopping each "
        "change about a training curve - and what goes wrong without them."
    ),
    "dsa": (
        "Algorithms and data structures animated one step at a time: searches "
        "and sorts with their real comparison counts, stacks, heaps, hash tables "
        "and tries, graph traversals and shortest paths, then the patterns - two "
        "pointers, sliding windows, greedy, backtracking and dynamic programming."
    ),
    "nlp": (
        "How text becomes something a network can compute with. Characters and "
        "tokens, normalisation and n-grams, one-hot vectors and learned "
        "embeddings, then the sequence models that read them - recurrent cells, "
        "LSTM and GRU gates, encoder-decoders - ending at attention."
    ),
    "computer-vision": (
        "Images as arrays of numbers, and what you can do to them. Classical "
        "operations first - thresholds, blurs, kernels, edges and keypoints - "
        "then the convolutional network layer by layer: padding, strides, "
        "pooling, parameter counts, named architectures and object detection."
    ),
    "db": (
        "Relational databases and the SQL that runs on them, with every query "
        "executed on the page. Schema design, keys and normalisation, then "
        "filtering, grouping, joins, subqueries and window functions, then what "
        "happens underneath: indexes, query plans, transactions, isolation and "
        "locking."
    ),
    "gen-ai": (
        "The machinery behind large language models and the systems built on "
        "them. Tokenisation and next-token prediction, attention's queries and "
        "keys, fine-tuning and quantisation, then retrieval: embeddings, vector "
        "indexes, chunking strategies and the metrics that tell you whether RAG "
        "found anything."
    ),
    "python": (
        "Python from a first print statement to functions, with every example "
        "running in your browser on a real interpreter. Types, strings, lists and "
        "dictionaries, control flow, comprehensions and errors - including the "
        "aliasing and copying surprises that catch people long after they start."
    ),
    "async_python": (
        "A short track on asyncio built from the event loop up. Step the loop "
        "tick by tick, turn sequential awaits into overlapping tasks, watch one "
        "blocking call freeze everything, and bound a producer with a queue - "
        "each example runnable on the page."
    ),
    "concurrency": (
        "Threads, processes and the GIL, explained at the level of bytecode. See "
        "why x += 1 can lose a count, what a lock prevents and how it deadlocks, "
        "what a process can and cannot share, and how to choose between threads, "
        "processes and async."
    ),
    "pydantic": (
        "Pydantic v2 one feature at a time, each example validated live. Models, "
        "coercion and constraints, reading a ValidationError, nested and "
        "discriminated models, validators and serialisers, then JSON Schema, "
        "settings, FastAPI integration and the move from v1 to v2."
    ),
    "fastapi": (
        "Building an API with FastAPI, with the app running in your browser. "
        "Paths, query parameters and request bodies, response models and the 422 "
        "they produce, routers and dependency injection, then background tasks, "
        "lifespan events, testing, security basics and project layout."
    ),
    "numpy": (
        "Arrays instead of loops. Shapes, dtypes and reshaping, indexing that "
        "returns views and indexing that returns copies, the two broadcasting "
        "rules, masking and aggregation along an axis, then the linear algebra "
        "and memory behaviour every numerical library inherits."
    ),
    "pandas": (
        "Labelled data with pandas, every example run on the page. The index and "
        "how loc and iloc use it, filtering without the copy warning, missing "
        "values and dtypes, group-by and transform, merges and reshaping, then "
        "time series, file formats and method chaining."
    ),
    "matplotlib": (
        "Plotting with matplotlib, every figure drawn live. Figures and axes and "
        "the two APIs that use them, the core chart types, labels, scales and "
        "subplots, colour and annotation, then dates, heatmaps, styles, layout "
        "and the mistakes that make a chart mislead."
    ),
    "sklearn": (
        "The scikit-learn workflow as a beginner actually meets it. One "
        "fit-predict-transform interface, splitting and scaling, linear and "
        "tree models, metrics and thresholds, then pipelines and column "
        "transformers that stop leakage, and hyperparameter search done "
        "honestly."
    ),
    "interview": (
        "Interview questions on Python strings, lists and dictionaries, each "
        "answered with code you can run and change. Why strings are immutable, "
        "what a list is underneath, and classic problems from two-sum and "
        "valid parentheses to the minimum window substring."
    ),
}

# The featured modules, in the order shown. Two sentences each: what you do
# on the page, then what it shows you.
FEATURED = [
    ("maths/vectors_and_dot_product.html",
     "Drag two vectors around the plane and read their magnitude, angle and "
     "projection as they move. The dot product turns negative the moment the "
     "angle passes 90 degrees, and you can watch it happen."),
    ("maths/bayes_theorem.html",
     "A positive result from a 99% accurate test can still mean you are "
     "probably fine. Adjust the base rate on a grid of real people and the "
     "paradox stops being one."),
    ("machine_learning/train_test_split.html",
     "Score a model on the data it was trained on, then on data it has never "
     "seen, and compare. The gap between the two numbers is the whole reason "
     "a test set exists."),
    ("machine_learning/knn.html",
     "Drop a point on the plane and let its nearest neighbours vote on its "
     "class. Change k and the decision boundary goes from jagged to smooth in "
     "front of you."),
    ("machine_learning/pca.html",
     "Rotate a line through a cloud of points until it captures the most "
     "variance it can. That angle is the first principal component, and what "
     "the line misses is what you lose."),
    ("deep_learning/neural_network.html",
     "Add layers and neurons and watch the parameter count climb with each "
     "choice. Then follow one input forward through weights, biases and "
     "activations to a prediction."),
    ("deep_learning/backpropagation.html",
     "Run a small computational graph forward, then backward, one local "
     "gradient at a time. Every gradient is checked against a finite "
     "difference, so you can see the chain rule is not hand-waving."),
    ("dsa/big_o_notation.html",
     "Put constant, logarithmic, linear, n log n, quadratic and exponential "
     "growth on the same axes. Real operation counts sit beside the curves, so "
     "the notation turns into numbers."),
    ("dsa/dijkstras.html",
     "Watch Dijkstra's algorithm settle one node at a time, always the closest "
     "unsettled one. The shortest-path tree grows outward until the "
     "destination is reached."),
    ("natural_language_processing/attention_mechanism.html",
     "See why squeezing a whole sentence into one context vector loses "
     "information. Attention lets the decoder re-weigh every input word at "
     "each step, shown as a full alignment matrix."),
    ("gen_ai/embeddings_and_vector_search.html",
     "Run an exact nearest-neighbour search, then a partitioned one, on the "
     "same embeddings. Comparisons collapse while recall slips a little - the "
     "trade every vector database makes."),
    ("gen_ai/rag.html",
     "Ask about a product no model has heard of and watch retrieval score "
     "every chunk. The winners go into the prompt, and a guess becomes an "
     "answer with sources."),
    ("database/joins_in_sql.html",
     "Join two tables with INNER, LEFT, RIGHT and FULL, and see exactly which "
     "rows each one keeps. The NULLs a LEFT join produces stop being a "
     "surprise."),
    ("computer_vision/convolution_kernels.html",
     "Slide a 3x3 kernel across an image by hand, multiplying and summing at "
     "each position. Blur and edge detection fall out of nine numbers."),
    ("numpy/broadcasting.html",
     "Add a row to a column and watch NumPy stretch both into a grid without "
     "copying either. Two rules decide when that works, and when it quietly "
     "builds an array far larger than you meant."),
    ("python/list_comprehensions.html",
     "Rewrite a loop that appends to a list as one expression, and run both. "
     "Then add a condition and a transformation, and see where a comprehension "
     "stops being the clearer choice."),
]
