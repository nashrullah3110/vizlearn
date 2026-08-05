/* GENERATED FILE - do not edit by hand.
 * Source: tools/glossary.py.  Rebuild: python3 tools/build_glossary.py
 */
window.VIZLEARN_GLOSSARY = [
 {
  "slug": "acid",
  "term": "ACID",
  "match": [
   "ACID"
  ],
  "def": "Atomicity, consistency, isolation, durability: the four guarantees a transaction is expected to hold to.",
  "where": "database/transactions_and_acid.html"
 },
 {
  "slug": "attention",
  "term": "attention",
  "match": [
   "attention mechanism",
   "self-attention",
   "attention heads",
   "attention head"
  ],
  "def": "A way for each position in a sequence to look at every other position and decide, per input, which ones matter.",
  "where": "natural_language_processing/attention_mechanism.html"
 },
 {
  "slug": "auc",
  "term": "AUC",
  "match": [
   "AUC",
   "area under the curve",
   "ROC AUC"
  ],
  "def": "The chance that the model scores a random positive above a random negative. 0.5 is coin-flipping.",
  "where": "machine_learning/roc_curve_and_auc.html"
 },
 {
  "slug": "backpropagation",
  "term": "backpropagation",
  "match": [
   "backpropagation",
   "backprop"
  ],
  "def": "Applying the chain rule backwards through a network to get each parameter's share of the blame for the loss.",
  "where": "deep_learning/backpropagation.html"
 },
 {
  "slug": "batch-normalization",
  "term": "batch normalization",
  "match": [
   "batch normalization",
   "batch norm"
  ],
  "def": "Rescaling a layer's outputs using the statistics of the current batch, which keeps activations in a workable range.",
  "where": "deep_learning/batch_normalization.html"
 },
 {
  "slug": "bi-encoder",
  "term": "bi-encoder",
  "match": [
   "bi-encoder",
   "bi-encoders"
  ],
  "def": "A model that embeds the query and each document separately, so the document vectors can be computed ahead of time. Fast to search, but it never sees the two texts side by side.",
  "where": "gen_ai/reranking_bi_encoders_vs_cross_encoders.html"
 },
 {
  "slug": "bm25",
  "term": "BM25",
  "match": [
   "BM25"
  ],
  "def": "A keyword-matching score that rewards rare query terms and stops rewarding repetition past a point. The standard sparse-retrieval baseline.",
  "where": "gen_ai/bm25_and_sparse_retrieval.html"
 },
 {
  "slug": "chunking",
  "term": "chunking",
  "match": [
   "chunking",
   "chunk",
   "chunks"
  ],
  "def": "Splitting a document into retrievable pieces. Cut too small and a piece loses its context; too large and it drags in noise.",
  "where": "gen_ai/chunking_strategies_for_rag.html"
 },
 {
  "slug": "cosine-similarity",
  "term": "cosine similarity",
  "match": [
   "cosine similarity",
   "cosine similarities"
  ],
  "def": "How closely two vectors point in the same direction, ignoring how long they are. 1 means identical direction, 0 means unrelated.",
  "where": "gen_ai/dot_product_vs_cosine_similarity.html"
 },
 {
  "slug": "cross-encoder",
  "term": "cross-encoder",
  "match": [
   "cross-encoder",
   "cross-encoders"
  ],
  "def": "A model that reads the query and the document together and scores the pair. Much more accurate than comparing two separate vectors, and far too slow to run over a whole corpus.",
  "where": "gen_ai/reranking_bi_encoders_vs_cross_encoders.html"
 },
 {
  "slug": "cross-entropy",
  "term": "cross-entropy",
  "match": [
   "cross-entropy",
   "cross entropy"
  ],
  "def": "The standard classification loss: how surprised the model was by the correct answer.",
  "where": "deep_learning/softmax_and_cross_entropy.html"
 },
 {
  "slug": "dot-product",
  "term": "dot product",
  "match": [
   "dot product",
   "dot products"
  ],
  "def": "Multiply two vectors element by element and add the results. Unlike cosine, it grows with vector length, so a long vector can win on size rather than on direction.",
  "where": "gen_ai/dot_product_vs_cosine_similarity.html"
 },
 {
  "slug": "dropout",
  "term": "dropout",
  "match": [
   "dropout"
  ],
  "def": "Randomly switching off units during training so the network cannot lean on any single one.",
  "where": "deep_learning/dropout_in_neural_networks.html"
 },
 {
  "slug": "eigenvector",
  "term": "eigenvector",
  "match": [
   "eigenvector",
   "eigenvectors",
   "eigenvalue",
   "eigenvalues"
  ],
  "def": "A direction a matrix only stretches or shrinks rather than rotates, and the factor by which it does so.",
  "where": "maths/eigenvalues_and_eigenvectors.html"
 },
 {
  "slug": "embedding",
  "term": "embedding",
  "match": [
   "embedding",
   "embeddings"
  ],
  "def": "A list of numbers standing for a piece of text, arranged so that things meaning similar things sit near each other.",
  "where": "gen_ai/embeddings_and_vector_search.html"
 },
 {
  "slug": "entropy",
  "term": "entropy",
  "match": [
   "entropy"
  ],
  "def": "How uncertain a distribution is - how many bits, on average, it takes to say which outcome happened.",
  "where": "maths/entropy_and_information.html"
 },
 {
  "slug": "epoch",
  "term": "epoch",
  "match": [
   "epoch",
   "epochs"
  ],
  "def": "One full pass over the training set.",
  "where": "deep_learning/batch_processing_in_neural_networks.html"
 },
 {
  "slug": "gradient",
  "term": "gradient",
  "match": [
   "gradient vector"
  ],
  "def": "The vector of partial derivatives: which way is uphill, and how steeply, in every direction at once.",
  "where": "maths/partial_derivatives_and_gradient.html"
 },
 {
  "slug": "gradient-descent",
  "term": "gradient descent",
  "match": [
   "gradient descent"
  ],
  "def": "Repeatedly nudging parameters in the direction that reduces the loss fastest.",
  "where": "deep_learning/gradient_descent_training.html"
 },
 {
  "slug": "hallucination",
  "term": "hallucination",
  "match": [
   "hallucination",
   "hallucinations"
  ],
  "def": "A fluent, confident answer that is not supported by anything the model was given or trained on.",
  "where": "gen_ai/hallucination_and_grounding.html"
 },
 {
  "slug": "hyde",
  "term": "HyDE",
  "match": [
   "HyDE",
   "hypothetical document embeddings"
  ],
  "def": "Ask a model to draft a plausible answer, then search using that draft instead of the question - because an answer resembles an answer more than a question does.",
  "where": "gen_ai/query_rewriting_and_hyde.html"
 },
 {
  "slug": "idf",
  "term": "IDF",
  "match": [
   "IDF",
   "inverse document frequency"
  ],
  "def": "Inverse document frequency: how rare a term is across the whole collection. Rare terms say more about a match than common ones.",
  "where": "gen_ai/bm25_and_sparse_retrieval.html"
 },
 {
  "slug": "index",
  "term": "index",
  "match": [
   "database index",
   "vector index",
   "inverted index"
  ],
  "def": "A sorted side structure that lets the database find matching rows without reading every one.",
  "where": "database/indexes_in_sql.html"
 },
 {
  "slug": "iou",
  "term": "IoU",
  "match": [
   "IoU",
   "intersection over union"
  ],
  "def": "Intersection over union: the area two boxes share divided by the area they cover between them. 1 is identical, 0 is no overlap.",
  "where": "computer_vision/iou_and_non_max_suppression.html"
 },
 {
  "slug": "kl-divergence",
  "term": "KL divergence",
  "match": [
   "KL divergence",
   "Kullback-Leibler divergence"
  ],
  "def": "How far one probability distribution is from another. Zero when they match, and not symmetric.",
  "where": "maths/cross_entropy_and_kl_divergence.html"
 },
 {
  "slug": "kv-cache",
  "term": "KV cache",
  "match": [
   "KV cache",
   "key-value cache"
  ],
  "def": "The stored keys and values for tokens already generated, so each new token does not re-read the whole sequence from scratch.",
  "where": "gen_ai/context_window_and_kv_cache.html"
 },
 {
  "slug": "learning-rate",
  "term": "learning rate",
  "match": [
   "learning rate"
  ],
  "def": "How big a step to take on each update. Too small and training crawls; too large and it overshoots and never settles.",
  "where": "deep_learning/gradient_descent_training.html"
 },
 {
  "slug": "logit",
  "term": "logit",
  "match": [
   "logit",
   "logits"
  ],
  "def": "A raw, unnormalised score straight out of a model, before softmax turns it into a probability.",
  "where": "deep_learning/softmax_and_cross_entropy.html"
 },
 {
  "slug": "lora",
  "term": "LoRA",
  "match": [
   "LoRA",
   "low-rank adaptation"
  ],
  "def": "Fine-tuning by training a small pair of extra matrices alongside frozen weights, instead of updating the whole model.",
  "where": "gen_ai/lora_in_llms.html"
 },
 {
  "slug": "mmr",
  "term": "maximal marginal relevance",
  "match": [
   "maximal marginal relevance",
   "MMR"
  ],
  "def": "Picking each next result by relevance minus similarity to what you already picked, so near-duplicates stop crowding out everything else.",
  "where": "gen_ai/maximal_marginal_relevance.html"
 },
 {
  "slug": "mrr",
  "term": "MRR",
  "match": [
   "MRR",
   "mean reciprocal rank"
  ],
  "def": "Mean reciprocal rank: one divided by the position of the first relevant result. It cares only about how long you wait for one good answer.",
  "where": "gen_ai/retrieval_evaluation_metrics.html"
 },
 {
  "slug": "ndcg",
  "term": "nDCG",
  "match": [
   "nDCG",
   "normalized discounted cumulative gain"
  ],
  "def": "A ranking score where every relevant result counts, but one near the top counts far more than one near the bottom.",
  "where": "gen_ai/retrieval_evaluation_metrics.html"
 },
 {
  "slug": "nms",
  "term": "non-max suppression",
  "match": [
   "non-max suppression",
   "NMS"
  ],
  "def": "Keep the highest-confidence box, throw away everything overlapping it past a threshold, repeat. How a detector stops returning the same object several times.",
  "where": "computer_vision/iou_and_non_max_suppression.html"
 },
 {
  "slug": "normalization",
  "term": "normalization",
  "match": [
   "feature scaling"
  ],
  "def": "Putting features on a comparable scale so no one of them dominates purely because its units are bigger.",
  "where": "deep_learning/feature_scaling_in_neural_networks.html"
 },
 {
  "slug": "overfitting",
  "term": "overfitting",
  "match": [
   "overfitting",
   "overfit"
  ],
  "def": "Learning noise specific to the training set, so performance on data the model has not seen gets worse rather than better.",
  "where": "deep_learning/dropout_in_neural_networks.html"
 },
 {
  "slug": "pca",
  "term": "PCA",
  "match": [
   "PCA",
   "principal component analysis"
  ],
  "def": "Finding the directions along which data varies most, and describing each point by those instead of the original axes.",
  "where": "machine_learning/pca.html"
 },
 {
  "slug": "precision-at-k",
  "term": "precision@k",
  "match": [
   "precision@k",
   "precision at k"
  ],
  "def": "Of the k results you returned, the fraction that were relevant. Punishes returning junk.",
  "where": "gen_ai/retrieval_evaluation_metrics.html"
 },
 {
  "slug": "quantization",
  "term": "quantization",
  "match": [
   "quantization"
  ],
  "def": "Storing a model's weights at lower numeric precision to shrink it, trading a little accuracy for a lot of memory.",
  "where": "gen_ai/quantization_in_llms.html"
 },
 {
  "slug": "rag",
  "term": "RAG",
  "match": [
   "RAG",
   "retrieval-augmented generation"
  ],
  "def": "Retrieval-Augmented Generation: fetch relevant passages first, then put them in the model's prompt so its answer is grounded in them.",
  "where": "gen_ai/rag.html"
 },
 {
  "slug": "recall-at-k",
  "term": "recall@k",
  "match": [
   "recall@k",
   "recall at k"
  ],
  "def": "Of all the relevant results that exist, the fraction your top k found. Punishes missing things entirely.",
  "where": "gen_ai/retrieval_evaluation_metrics.html"
 },
 {
  "slug": "rrf",
  "term": "reciprocal rank fusion",
  "match": [
   "reciprocal rank fusion",
   "RRF"
  ],
  "def": "A way to merge two ranked lists using only each document's position in them, so two scores that are on different scales never have to be compared directly.",
  "where": "gen_ai/hybrid_search_reciprocal_rank_fusion.html"
 },
 {
  "slug": "regularization",
  "term": "regularization",
  "match": [
   "regularization"
  ],
  "def": "Any penalty that discourages a model from fitting its training data too exactly.",
  "where": "deep_learning/regularization_in_neural_networks.html"
 },
 {
  "slug": "residual-connection",
  "term": "residual connection",
  "match": [
   "residual connection",
   "skip connection",
   "residual connections",
   "skip connections"
  ],
  "def": "Adding a block's input back onto its output, which gives gradients an unimpeded route back and stops deep stacks degrading.",
  "where": "deep_learning/residual_connections.html"
 },
 {
  "slug": "softmax",
  "term": "softmax",
  "match": [
   "softmax"
  ],
  "def": "Turns a list of arbitrary scores into probabilities that are all positive and sum to 1, keeping their order.",
  "where": "deep_learning/softmax_and_cross_entropy.html"
 },
 {
  "slug": "token",
  "term": "token",
  "match": [
   "token",
   "tokens",
   "tokenization"
  ],
  "def": "The unit a language model actually reads: usually a word piece rather than a whole word or a single letter.",
  "where": "gen_ai/how_llms_process_text.html"
 },
 {
  "slug": "vanishing-gradient",
  "term": "vanishing gradient",
  "match": [
   "vanishing gradient",
   "vanishing gradients"
  ],
  "def": "When gradients shrink at every layer on the way back, so early layers receive almost no signal and stop learning.",
  "where": "deep_learning/vanishing_vs_exploding_gradient.html"
 },
 {
  "slug": "variance",
  "term": "variance",
  "match": [
   "variance"
  ],
  "def": "How spread out values are around their mean, in squared units.",
  "where": "maths/mean_variance_standard_deviation.html"
 }
];
