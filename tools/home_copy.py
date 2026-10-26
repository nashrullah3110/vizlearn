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

# Keyed by lib_pages.TOPICS key. Short card summaries; track pages provide detail.
TRACK_BLURBS = {
    "maths": "Build intuition for linear algebra, calculus, probability, and statistics with visual examples.",
    "ml": "Explore regression, trees, SVMs, clustering, and model evaluation through hands-on experiments.",
    "dl": "Trace neural networks, backpropagation, optimizers, and training behaviour one step at a time.",
    "dsa": "Explore data structures, searches, sorts, graph algorithms, and problem-solving patterns.",
    "nlp": "Follow how text becomes tokens and vectors, then see how sequence models use attention.",
    "computer-vision": "Work from image filters and edges through CNNs, object detection, and segmentation.",
    "db": "Practice SQL, schema design, joins, indexes, query plans, and transactions with examples.",
    "gen-ai": "Explore LLMs, tokenization, embeddings, vector search, and retrieval-augmented generation.",
    "python": "Learn Python fundamentals with runnable examples covering data types, collections, and functions.",
    "async_python": "See asyncio tasks overlap, blocking calls stall the loop, and queues coordinate work.",
    "concurrency": "Understand threads, processes, the GIL, locks, race conditions, and deadlocks.",
    "pydantic": "Validate data with Pydantic models, constraints, custom validators, settings, and JSON Schema.",
    "fastapi": "Build API examples with FastAPI: routes, validation, dependencies, security, and testing.",
    "numpy": "Understand array shapes, indexing, broadcasting, vectorized operations, and linear algebra.",
    "pandas": "Work with labelled data, filtering, missing values, grouping, joins, and time series.",
    "matplotlib": "Create readable charts and learn axes, scales, labels, subplots, and annotation.",
    "sklearn": "Follow scikit-learn workflows from data splits and scaling through pipelines and model tuning.",
    "interview": "Practice coding interview patterns with runnable Python examples, from two-sum to graph search.",
}

# The featured modules, in the order shown. One concise interaction hook per
# card; the illustration carries the visual preview and each linked lesson
# provides the full explanation.
FEATURED = [
    ("maths/bayes_theorem.html",
     "Set the base rate for a rare condition and see what a positive test really means."),
    ("machine_learning/knn.html",
     "Move a query point; its k nearest labelled neighbours vote on the class."),
    ("deep_learning/backpropagation.html",
     "Run a small network and follow each gradient back through the graph."),
    ("dsa/big_o_notation.html",
     "Compare operation counts as input size grows, from constant to exponential."),
    ("natural_language_processing/attention_mechanism.html",
     "Change attention weights and see which input words shape the context."),
    ("gen_ai/rag.html",
     "Rank document chunks by similarity and inspect what retrieval sends to the model."),
]
