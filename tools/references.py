# -*- coding: utf-8 -*-
"""Further reading, per module.

A technical explainer with no sources asks to be taken on trust. These are the
primary references for each topic - the paper an idea came from, or the
official documentation for the thing being described.

Two rules, because a fabricated citation is worse than none:

  * A URL appears only where it is a stable, well-known address (arXiv abs
    pages, JMLR, official docs). Anything I could not vouch for is cited by
    title, author and venue with no link, which is still a real citation.
  * Pages with nothing genuine to cite get no section at all rather than a
    filler link to a search result or a general-interest article.

Coverage is therefore partial by design. Rendered by build_module_ui.py.
"""

# path -> [(title, source, url or None), ...]
REFERENCES = {

# ------------------------------------------------------------ deep learning
"deep_learning/dropout_in_neural_networks.html": [
    ("Dropout: A Simple Way to Prevent Neural Networks from Overfitting",
     "Srivastava, Hinton, Krizhevsky, Sutskever & Salakhutdinov, JMLR 2014",
     "https://jmlr.org/papers/v15/srivastava14a.html"),
    ("torch.nn.Dropout", "PyTorch documentation",
     "https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html"),
],
"deep_learning/batch_normalization.html": [
    ("Batch Normalization: Accelerating Deep Network Training by Reducing "
     "Internal Covariate Shift", "Ioffe & Szegedy, 2015",
     "https://arxiv.org/abs/1502.03167"),
],
"deep_learning/layer_normalization.html": [
    ("Layer Normalization", "Ba, Kiros & Hinton, 2016",
     "https://arxiv.org/abs/1607.06450"),
],
"deep_learning/optimizers_in_neural_networks.html": [
    ("Adam: A Method for Stochastic Optimization", "Kingma & Ba, ICLR 2015",
     "https://arxiv.org/abs/1412.6980"),
    ("Decoupled Weight Decay Regularization (AdamW)",
     "Loshchilov & Hutter, ICLR 2019", "https://arxiv.org/abs/1711.05101"),
],
"deep_learning/optimizers_in_3d.html": [
    ("Adam: A Method for Stochastic Optimization", "Kingma & Ba, ICLR 2015",
     "https://arxiv.org/abs/1412.6980"),
],
"deep_learning/residual_connections.html": [
    ("Deep Residual Learning for Image Recognition", "He, Zhang, Ren & Sun, 2015",
     "https://arxiv.org/abs/1512.03385"),
],
"deep_learning/weight_initialization.html": [
    ("Delving Deep into Rectifiers: Surpassing Human-Level Performance on "
     "ImageNet Classification (He initialisation)", "He, Zhang, Ren & Sun, 2015",
     "https://arxiv.org/abs/1502.01852"),
    ("Understanding the difficulty of training deep feedforward neural networks "
     "(Xavier initialisation)", "Glorot & Bengio, AISTATS 2010", None),
],
"deep_learning/vanishing_vs_exploding_gradient.html": [
    ("On the difficulty of training Recurrent Neural Networks",
     "Pascanu, Mikolov & Bengio, ICML 2013", "https://arxiv.org/abs/1211.5063"),
],
"deep_learning/gradient_clipping.html": [
    ("On the difficulty of training Recurrent Neural Networks",
     "Pascanu, Mikolov & Bengio, ICML 2013", "https://arxiv.org/abs/1211.5063"),
],
"deep_learning/backpropagation.html": [
    ("Learning representations by back-propagating errors",
     "Rumelhart, Hinton & Williams, Nature 1986", None),
],
"deep_learning/perceptron.html": [
    ("The Perceptron: A Probabilistic Model for Information Storage and "
     "Organization in the Brain", "Rosenblatt, Psychological Review 1958", None),
],
"deep_learning/batch_processing_in_neural_networks.html": [
    ("Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour "
     "(the linear scaling rule)", "Goyal et al., 2017",
     "https://arxiv.org/abs/1706.02677"),
],
"deep_learning/early_stopping_in_neural_networks.html": [
    ("Early Stopping - But When?", "Prechelt, Neural Networks: Tricks of the "
     "Trade, 1998", None),
],
"deep_learning/hyper-paramter_tuning.html": [
    ("Random Search for Hyper-Parameter Optimization",
     "Bergstra & Bengio, JMLR 2012",
     "https://jmlr.org/papers/v13/bergstra12a.html"),
],
"deep_learning/activation_functions.html": [
    ("Gaussian Error Linear Units (GELUs)", "Hendrycks & Gimpel, 2016",
     "https://arxiv.org/abs/1606.08415"),
],

# ---------------------------------------------------------------------- NLP
"natural_language_processing/self_attention.html": [
    ("Attention Is All You Need", "Vaswani et al., NeurIPS 2017",
     "https://arxiv.org/abs/1706.03762"),
],
"natural_language_processing/positional_encoding.html": [
    ("Attention Is All You Need", "Vaswani et al., NeurIPS 2017",
     "https://arxiv.org/abs/1706.03762"),
],
"natural_language_processing/what_is_lstm.html": [
    ("Long Short-Term Memory", "Hochreiter & Schmidhuber, Neural Computation 1997",
     None),
],
"natural_language_processing/what_are_embeddings.html": [
    ("Efficient Estimation of Word Representations in Vector Space (word2vec)",
     "Mikolov, Chen, Corrado & Dean, 2013", "https://arxiv.org/abs/1301.3781"),
    ("GloVe: Global Vectors for Word Representation",
     "Pennington, Socher & Manning, EMNLP 2014", None),
],
"natural_language_processing/how_are_embeddings_generated.html": [
    ("Distributed Representations of Words and Phrases and their "
     "Compositionality (negative sampling)", "Mikolov et al., NeurIPS 2013",
     "https://arxiv.org/abs/1310.4546"),
],
"natural_language_processing/rnn_architecture.html": [
    ("On the difficulty of training Recurrent Neural Networks",
     "Pascanu, Mikolov & Bengio, ICML 2013", "https://arxiv.org/abs/1211.5063"),
],
"natural_language_processing/normalization_techniques_for_sequential_data.html": [
    ("Layer Normalization", "Ba, Kiros & Hinton, 2016",
     "https://arxiv.org/abs/1607.06450"),
],

# ------------------------------------------------------------------- gen ai
"gen_ai/rag.html": [
    ("Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
     "Lewis et al., NeurIPS 2020", "https://arxiv.org/abs/2005.11401"),
],
"gen_ai/lora_in_llms.html": [
    ("LoRA: Low-Rank Adaptation of Large Language Models", "Hu et al., 2021",
     "https://arxiv.org/abs/2106.09685"),
],
"gen_ai/byte_pair_encoding_tokenizer.html": [
    ("Neural Machine Translation of Rare Words with Subword Units",
     "Sennrich, Haddow & Birch, ACL 2016", "https://arxiv.org/abs/1508.07909"),
],
"gen_ai/masked_language_modeling.html": [
    ("BERT: Pre-training of Deep Bidirectional Transformers for Language "
     "Understanding", "Devlin, Chang, Lee & Toutanova, 2018",
     "https://arxiv.org/abs/1810.04805"),
],
"gen_ai/knowledge_distillation_in_llms.html": [
    ("Distilling the Knowledge in a Neural Network",
     "Hinton, Vinyals & Dean, 2015", "https://arxiv.org/abs/1503.02531"),
],
"gen_ai/query_rewriting_and_hyde.html": [
    ("Precise Zero-Shot Dense Retrieval without Relevance Labels (HyDE)",
     "Gao, Ma, Lin & Callan, 2022", "https://arxiv.org/abs/2212.10496"),
],
"gen_ai/bm25_and_sparse_retrieval.html": [
    ("The Probabilistic Relevance Framework: BM25 and Beyond",
     "Robertson & Zaragoza, Foundations and Trends in IR, 2009", None),
],
"gen_ai/maximal_marginal_relevance.html": [
    ("The Use of MMR, Diversity-Based Reranking for Reordering Documents and "
     "Producing Summaries", "Carbonell & Goldstein, SIGIR 1998", None),
],
"gen_ai/fine_tuning_vs_rlhf.html": [
    ("Training language models to follow instructions with human feedback",
     "Ouyang et al., 2022", "https://arxiv.org/abs/2203.02155"),
],

# ------------------------------------------------------------ machine learning
"machine_learning/random_forest.html": [
    ("Random Forests", "Breiman, Machine Learning 45, 2001", None),
],
"machine_learning/svm.html": [
    ("Support-Vector Networks", "Cortes & Vapnik, Machine Learning 20, 1995",
     None),
],
"machine_learning/cross_validation.html": [
    ("Cross-validation: evaluating estimator performance",
     "scikit-learn user guide",
     "https://scikit-learn.org/stable/modules/cross_validation.html"),
],
"machine_learning/k_means.html": [
    ("k-means++: The Advantages of Careful Seeding",
     "Arthur & Vassilvitskii, SODA 2007", None),
    ("Clustering", "scikit-learn user guide",
     "https://scikit-learn.org/stable/modules/clustering.html"),
],
"machine_learning/roc_curve_and_auc.html": [
    ("An introduction to ROC analysis", "Fawcett, Pattern Recognition Letters 2006",
     None),
],
"machine_learning/training_on_label_imbalanced_dataset.html": [
    ("SMOTE: Synthetic Minority Over-sampling Technique",
     "Chawla, Bowyer, Hall & Kegelmeyer, JAIR 2002",
     "https://arxiv.org/abs/1106.1813"),
],
"machine_learning/ridge_and_lasso_regression.html": [
    ("Regression Shrinkage and Selection via the Lasso",
     "Tibshirani, JRSS-B 1996", None),
],
"machine_learning/confusion_matrix.html": [
    ("Metrics and scoring: quantifying the quality of predictions",
     "scikit-learn user guide",
     "https://scikit-learn.org/stable/modules/model_evaluation.html"),
],

# --------------------------------------------------------- computer vision
"computer_vision/resnet_and_identity_shortcuts.html": [
    ("Deep Residual Learning for Image Recognition", "He, Zhang, Ren & Sun, 2015",
     "https://arxiv.org/abs/1512.03385"),
],
"computer_vision/semantic_segmentation_unet.html": [
    ("U-Net: Convolutional Networks for Biomedical Image Segmentation",
     "Ronneberger, Fischer & Brox, MICCAI 2015",
     "https://arxiv.org/abs/1505.04597"),
],
"computer_vision/iou_and_non_max_suppression.html": [
    ("You Only Look Once: Unified, Real-Time Object Detection",
     "Redmon, Divvala, Girshick & Farhadi, 2015",
     "https://arxiv.org/abs/1506.02640"),
],
"computer_vision/transfer_learning_with_cnn.html": [
    ("How transferable are features in deep neural networks?",
     "Yosinski, Clune, Bengio & Lipson, NeurIPS 2014",
     "https://arxiv.org/abs/1411.1792"),
],

# ------------------------------------------------------------------ database
"database/indexes_in_sql.html": [
    ("Indexes", "PostgreSQL documentation",
     "https://www.postgresql.org/docs/current/indexes.html"),
    ("The Ubiquitous B-Tree", "Comer, ACM Computing Surveys 1979", None),
],
"database/transactions_and_acid.html": [
    ("Transaction Isolation", "PostgreSQL documentation",
     "https://www.postgresql.org/docs/current/transaction-iso.html"),
],
"database/normalization_in_sql.html": [
    ("A Relational Model of Data for Large Shared Data Banks",
     "Codd, Communications of the ACM 1970", None),
],
"database/what_are_relational_databases.html": [
    ("A Relational Model of Data for Large Shared Data Banks",
     "Codd, Communications of the ACM 1970", None),
],
"database/window_functions_in_sql.html": [
    ("Window Functions", "PostgreSQL documentation",
     "https://www.postgresql.org/docs/current/tutorial-window.html"),
],
"database/query_execution_order.html": [
    ("SELECT", "PostgreSQL documentation",
     "https://www.postgresql.org/docs/current/sql-select.html"),
],

# -------------------------------------------------------------------- python
"python/lists_and_indexing.html": [
    ("Data Structures", "The Python Tutorial",
     "https://docs.python.org/3/tutorial/datastructures.html"),
],
"python/dictionaries.html": [
    ("Mapping Types - dict", "Python Standard Library reference",
     "https://docs.python.org/3/library/stdtypes.html#mapping-types-dict"),
],
"python/strings_and_slicing.html": [
    ("Text Sequence Type - str", "Python Standard Library reference",
     "https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str"),
],
"python/functions_and_return.html": [
    ("Defining Functions", "The Python Tutorial",
     "https://docs.python.org/3/tutorial/controlflow.html#defining-functions"),
],
"python/for_loops_and_range.html": [
    ("The range() type", "Python Standard Library reference",
     "https://docs.python.org/3/library/stdtypes.html#range"),
],
"python/if_elif_else.html": [
    ("if Statements", "The Python Tutorial",
     "https://docs.python.org/3/tutorial/controlflow.html#if-statements"),
],
"python/reading_errors.html": [
    ("Errors and Exceptions", "The Python Tutorial",
     "https://docs.python.org/3/tutorial/errors.html"),
],

# --------------------------------------------------------------------- dsa
"dsa/dictionaries_in_python.html": [
    ("Mapping Types - dict", "Python Standard Library reference",
     "https://docs.python.org/3/library/stdtypes.html#mapping-types-dict"),
],
"dsa/lists_in_python.html": [
    ("Data Structures", "The Python Tutorial",
     "https://docs.python.org/3/tutorial/datastructures.html"),
    ("TimeComplexity", "Python wiki - operation costs by container type",
     "https://wiki.python.org/moin/TimeComplexity"),
],
"dsa/quick_sort.html": [
    ("Quicksort", "Hoare, The Computer Journal 1962", None),
    ("Engineering a Sort Function", "Bentley & McIlroy, Software: Practice and "
     "Experience 1993", None),
],
"dsa/dijkstras.html": [
    ("A Note on Two Problems in Connexion with Graphs",
     "Dijkstra, Numerische Mathematik 1959", None),
],
"dsa/a_star.html": [
    ("A Formal Basis for the Heuristic Determination of Minimum Cost Paths",
     "Hart, Nilsson & Raphael, IEEE Transactions on SSC 1968", None),
],
"dsa/kmp_string_matching.html": [
    ("Fast Pattern Matching in Strings",
     "Knuth, Morris & Pratt, SIAM Journal on Computing 1977", None),
],
"dsa/bellman_ford.html": [
    ("On a Routing Problem", "Bellman, Quarterly of Applied Mathematics 1958",
     None),
],
"dsa/union_find.html": [
    ("Efficiency of a Good But Not Linear Set Union Algorithm",
     "Tarjan, Journal of the ACM 1975", None),
],
"dsa/big_o_notation.html": [
    ("Introduction to Algorithms, chapter 3: Growth of Functions",
     "Cormen, Leiserson, Rivest & Stein", None),
],

}
