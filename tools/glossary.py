"""The site's shared vocabulary: one definition per term, in one place.

Every module defines the terms it introduces, and then every *later* module
uses them bare. A reader who lands on a page from search rather than from the
start of a track meets "IoU", "nDCG" or "logit" with no way back to where it
was explained, short of a site search that returns the whole track.

Each entry is:

    slug: (term, aliases, definition, defining module path or None)

`aliases` are the other spellings the runtime should also match - plurals and
expansions, mostly. The definition is one or two plain sentences: enough to
keep reading, deliberately not enough to replace the module, which is what
`where` links to.

Kept hand-written rather than scraped from the articles. A definition pulled
out of prose reads like a fragment of an argument, because that is what it is,
and it would drift the moment the sentence around it was edited.
"""

# slug -> (term, [aliases], definition, defining module path or None)
TERMS = {
    # --- retrieval ------------------------------------------------------
    "cosine-similarity": (
        "cosine similarity",
        ["cosine similarities"],
        "How closely two vectors point in the same direction, ignoring how "
        "long they are. 1 means identical direction, 0 means unrelated.",
        "gen_ai/dot_product_vs_cosine_similarity.html"),
    "dot-product": (
        "dot product",
        ["dot products"],
        "Multiply two vectors element by element and add the results. Unlike "
        "cosine, it grows with vector length, so a long vector can win on "
        "size rather than on direction.",
        "gen_ai/dot_product_vs_cosine_similarity.html"),
    "bm25": (
        "BM25",
        [],
        "A keyword-matching score that rewards rare query terms and stops "
        "rewarding repetition past a point. The standard sparse-retrieval "
        "baseline.",
        "gen_ai/bm25_and_sparse_retrieval.html"),
    "idf": (
        "IDF",
        ["inverse document frequency"],
        "Inverse document frequency: how rare a term is across the whole "
        "collection. Rare terms say more about a match than common ones.",
        "gen_ai/bm25_and_sparse_retrieval.html"),
    "embedding": (
        "embedding",
        ["embeddings"],
        "A list of numbers standing for a piece of text, arranged so that "
        "things meaning similar things sit near each other.",
        "gen_ai/embeddings_and_vector_search.html"),
    "chunking": (
        "chunking",
        ["chunk", "chunks"],
        "Splitting a document into retrievable pieces. Cut too small and a "
        "piece loses its context; too large and it drags in noise.",
        "gen_ai/chunking_strategies_for_rag.html"),
    "rag": (
        "RAG",
        ["retrieval-augmented generation"],
        "Retrieval-Augmented Generation: fetch relevant passages first, then "
        "put them in the model's prompt so its answer is grounded in them.",
        "gen_ai/rag.html"),
    "rrf": (
        "reciprocal rank fusion",
        ["RRF"],
        "A way to merge two ranked lists using only each document's position "
        "in them, so two scores that are on different scales never have to be "
        "compared directly.",
        "gen_ai/hybrid_search_reciprocal_rank_fusion.html"),
    "ndcg": (
        "nDCG",
        ["normalized discounted cumulative gain"],
        "A ranking score where every relevant result counts, but one near the "
        "top counts far more than one near the bottom.",
        "gen_ai/retrieval_evaluation_metrics.html"),
    "mrr": (
        "MRR",
        ["mean reciprocal rank"],
        "Mean reciprocal rank: one divided by the position of the first "
        "relevant result. It cares only about how long you wait for one good "
        "answer.",
        "gen_ai/retrieval_evaluation_metrics.html"),
    "precision-at-k": (
        "precision@k",
        ["precision at k"],
        "Of the k results you returned, the fraction that were relevant. "
        "Punishes returning junk.",
        "gen_ai/retrieval_evaluation_metrics.html"),
    "recall-at-k": (
        "recall@k",
        ["recall at k"],
        "Of all the relevant results that exist, the fraction your top k "
        "found. Punishes missing things entirely.",
        "gen_ai/retrieval_evaluation_metrics.html"),
    "cross-encoder": (
        "cross-encoder",
        ["cross-encoders"],
        "A model that reads the query and the document together and scores "
        "the pair. Much more accurate than comparing two separate vectors, "
        "and far too slow to run over a whole corpus.",
        "gen_ai/reranking_bi_encoders_vs_cross_encoders.html"),
    "bi-encoder": (
        "bi-encoder",
        ["bi-encoders"],
        "A model that embeds the query and each document separately, so the "
        "document vectors can be computed ahead of time. Fast to search, but "
        "it never sees the two texts side by side.",
        "gen_ai/reranking_bi_encoders_vs_cross_encoders.html"),
    "mmr": (
        "maximal marginal relevance",
        ["MMR"],
        "Picking each next result by relevance minus similarity to what you "
        "already picked, so near-duplicates stop crowding out everything "
        "else.",
        "gen_ai/maximal_marginal_relevance.html"),
    "hyde": (
        "HyDE",
        ["hypothetical document embeddings"],
        "Ask a model to draft a plausible answer, then search using that "
        "draft instead of the question - because an answer resembles an "
        "answer more than a question does.",
        "gen_ai/query_rewriting_and_hyde.html"),

    # --- LLM internals --------------------------------------------------
    "token": (
        "token",
        ["tokens", "tokenization"],
        "The unit a language model actually reads: usually a word piece "
        "rather than a whole word or a single letter.",
        "gen_ai/how_llms_process_text.html"),
    "softmax": (
        "softmax",
        [],
        "Turns a list of arbitrary scores into probabilities that are all "
        "positive and sum to 1, keeping their order.",
        "deep_learning/softmax_and_cross_entropy.html"),
    "attention": (
        "attention",
        ["attention mechanism"],
        "A way for each position in a sequence to look at every other "
        "position and decide, per input, which ones matter.",
        "natural_language_processing/attention_mechanism.html"),
    "kv-cache": (
        "KV cache",
        ["key-value cache"],
        "The stored keys and values for tokens already generated, so each new "
        "token does not re-read the whole sequence from scratch.",
        "gen_ai/context_window_and_kv_cache.html"),
    "quantization": (
        "quantization",
        [],
        "Storing a model's weights at lower numeric precision to shrink it, "
        "trading a little accuracy for a lot of memory.",
        "gen_ai/quantization_in_llms.html"),
    "lora": (
        "LoRA",
        ["low-rank adaptation"],
        "Fine-tuning by training a small pair of extra matrices alongside "
        "frozen weights, instead of updating the whole model.",
        "gen_ai/lora_in_llms.html"),
    "hallucination": (
        "hallucination",
        ["hallucinations"],
        "A fluent, confident answer that is not supported by anything the "
        "model was given or trained on.",
        "gen_ai/hallucination_and_grounding.html"),

    # --- training -------------------------------------------------------
    "gradient-descent": (
        "gradient descent",
        [],
        "Repeatedly nudging parameters in the direction that reduces the "
        "loss fastest.",
        "deep_learning/gradient_descent_training.html"),
    "backpropagation": (
        "backpropagation",
        ["backprop"],
        "Applying the chain rule backwards through a network to get each "
        "parameter's share of the blame for the loss.",
        "deep_learning/backpropagation.html"),
    "learning-rate": (
        "learning rate",
        [],
        "How big a step to take on each update. Too small and training "
        "crawls; too large and it overshoots and never settles.",
        "deep_learning/gradient_descent_training.html"),
    "overfitting": (
        "overfitting",
        ["overfit"],
        "Learning noise specific to the training set, so performance on data "
        "the model has not seen gets worse rather than better.",
        "deep_learning/dropout_in_neural_networks.html"),
    "regularization": (
        "regularization",
        [],
        "Any penalty that discourages a model from fitting its training data "
        "too exactly.",
        "deep_learning/regularization_in_neural_networks.html"),
    "dropout": (
        "dropout",
        [],
        "Randomly switching off units during training so the network cannot "
        "lean on any single one.",
        "deep_learning/dropout_in_neural_networks.html"),
    "batch-normalization": (
        "batch normalization",
        ["batch norm"],
        "Rescaling a layer's outputs using the statistics of the current "
        "batch, which keeps activations in a workable range.",
        "deep_learning/batch_normalization.html"),
    "vanishing-gradient": (
        "vanishing gradient",
        ["vanishing gradients"],
        "When gradients shrink at every layer on the way back, so early "
        "layers receive almost no signal and stop learning.",
        "deep_learning/vanishing_vs_exploding_gradient.html"),
    "residual-connection": (
        "residual connection",
        ["skip connection", "residual connections", "skip connections"],
        "Adding a block's input back onto its output, which gives gradients "
        "an unimpeded route back and stops deep stacks degrading.",
        "deep_learning/residual_connections.html"),
    "epoch": (
        "epoch",
        ["epochs"],
        "One full pass over the training set.",
        "deep_learning/batch_processing_in_neural_networks.html"),
    "logit": (
        "logit",
        ["logits"],
        "A raw, unnormalised score straight out of a model, before softmax "
        "turns it into a probability.",
        "deep_learning/softmax_and_cross_entropy.html"),

    # --- evaluation -----------------------------------------------------
    "cross-entropy": (
        "cross-entropy",
        ["cross entropy"],
        "The standard classification loss: how surprised the model was by the "
        "correct answer.",
        "deep_learning/softmax_and_cross_entropy.html"),
    "kl-divergence": (
        "KL divergence",
        ["Kullback-Leibler divergence"],
        "How far one probability distribution is from another. Zero when they "
        "match, and not symmetric.",
        "maths/cross_entropy_and_kl_divergence.html"),
    "entropy": (
        "entropy",
        [],
        "How uncertain a distribution is - how many bits, on average, it "
        "takes to say which outcome happened.",
        "maths/entropy_and_information.html"),
    "precision": (
        "precision",
        [],
        "Of the things you flagged as positive, the fraction that really "
        "were.",
        "machine_learning/confusion_matrix.html"),
    "recall": (
        "recall",
        [],
        "Of the things that really were positive, the fraction you caught.",
        "machine_learning/confusion_matrix.html"),
    "auc": (
        "AUC",
        ["area under the curve", "ROC AUC"],
        "The chance that the model scores a random positive above a random "
        "negative. 0.5 is coin-flipping.",
        "machine_learning/roc_curve_and_auc.html"),
    "iou": (
        "IoU",
        ["intersection over union"],
        "Intersection over union: the area two boxes share divided by the "
        "area they cover between them. 1 is identical, 0 is no overlap.",
        "computer_vision/iou_and_non_max_suppression.html"),
    "nms": (
        "non-max suppression",
        ["NMS"],
        "Keep the highest-confidence box, throw away everything overlapping "
        "it past a threshold, repeat. How a detector stops returning the same "
        "object several times.",
        "computer_vision/iou_and_non_max_suppression.html"),

    # --- maths ----------------------------------------------------------
    "gradient": (
        "gradient",
        [],
        "The vector of partial derivatives: which way is uphill, and how "
        "steeply, in every direction at once.",
        "maths/partial_derivatives_and_gradient.html"),
    "eigenvector": (
        "eigenvector",
        ["eigenvectors", "eigenvalue", "eigenvalues"],
        "A direction a matrix only stretches or shrinks rather than rotates, "
        "and the factor by which it does so.",
        "maths/eigenvalues_and_eigenvectors.html"),
    "variance": (
        "variance",
        [],
        "How spread out values are around their mean, in squared units.",
        "maths/mean_variance_standard_deviation.html"),
    "pca": (
        "PCA",
        ["principal component analysis"],
        "Finding the directions along which data varies most, and describing "
        "each point by those instead of the original axes.",
        "machine_learning/pca.html"),
    "normalization": (
        "normalization",
        [],
        "Putting features on a comparable scale so no one of them dominates "
        "purely because its units are bigger.",
        "deep_learning/feature_scaling_in_neural_networks.html"),

    # --- databases ------------------------------------------------------
    "index": (
        "index",
        ["database index"],
        "A sorted side structure that lets the database find matching rows "
        "without reading every one.",
        "database/indexes_in_sql.html"),
    "acid": (
        "ACID",
        [],
        "Atomicity, consistency, isolation, durability: the four guarantees a "
        "transaction is expected to hold to.",
        "database/transactions_and_acid.html"),
}


# Terms whose bare form is also ordinary English. Left to match freely they
# produce confident nonsense: the RAG article says "generation becomes reading
# rather than recall" and "costs latency, money and attention", and both were
# marked with their machine learning definitions.
#
# For a slug listed here, only the forms given are ever auto-marked in prose -
# the bare term never is. An empty list means the term is glossary-only, which
# is the right answer for "precision" and "recall": their unambiguous uses are
# already covered by the precision@k and recall@k entries, and no shorter form
# is safe.
STRICT_FORMS = {
    "attention": ["attention mechanism", "self-attention", "attention heads",
                  "attention head"],
    "recall": [],
    "precision": [],
    "index": ["database index", "vector index", "inverted index"],
    "normalization": ["feature scaling"],
    "gradient": ["gradient vector"],
}


def match_forms(slug, term, aliases):
    """Every spelling the runtime may mark for this term, longest usable first."""
    if slug in STRICT_FORMS:
        return list(STRICT_FORMS[slug])
    return [term] + list(aliases)


def entries():
    """[(slug, term, aliases, definition, where)] sorted by term."""
    out = [(slug,) + v for slug, v in TERMS.items()]
    return sorted(out, key=lambda e: e[1].lower())
