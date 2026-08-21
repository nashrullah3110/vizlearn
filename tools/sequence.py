# -*- coding: utf-8 -*-
"""Teaching order for each track.

courseData was alphabetical, which meant prev/next, the related rail and the
hub all presented modules in an order nobody would teach in - Maths opened on
Bayes' Theorem, Deep Learning opened on Activation Functions before a
perceptron had been introduced.

This is the intended sequence: each module should only rely on ideas from the
ones above it. Reorder here, run `npm run build`, and prev/next, the related
rail, the Learning Path and the hub all follow.
"""

# The interview track is generated: tools/interview.py already defines the
# questions in teaching order (concepts first, then problems by difficulty),
# and build_interview.py writes courseData in that order. Transcribing the
# slugs here would be a second source of truth that goes stale every time a
# question is added, so derive them instead.
from interview import QUESTIONS as _INTERVIEW_QUESTIONS

_INTERVIEW = ["interview/%s.html" % q["slug"] for q in _INTERVIEW_QUESTIONS]

SEQUENCE = {
    # Foundations the rest of the site quietly assumes.
    "maths": [
        "maths/equation_of_line.html",
        "maths/logarithms.html",
        "maths/exponentials.html",
        "maths/vectors_and_dot_product.html",
        "maths/vector_norms.html",
        "maths/distance_metrics.html",
        "maths/matrix_multiplication.html",
        "maths/matrix_as_transformation.html",
        "maths/projections.html",
        "maths/determinant.html",
        "maths/identity_inverse_transpose.html",
        "maths/rank_and_linear_independence.html",
        "maths/eigenvalues_and_eigenvectors.html",
        "maths/derivatives_and_slope.html",
        "maths/the_chain_rule.html",
        "maths/partial_derivatives_and_gradient.html",
        "maths/mean_mode_and_median.html",
        "maths/mean_variance_standard_deviation.html",
        "maths/covariance_and_correlation.html",
        "maths/probability_basics.html",
        "maths/conditional_probability.html",
        "maths/bayes_theorem.html",
        "maths/the_normal_distribution.html",
        "maths/maximum_likelihood_estimation.html",
        "maths/entropy_and_information.html",
        "maths/cross_entropy_and_kl_divergence.html",
        "maths/information_gain.html",
    ],

    # Prepare data -> fit a first model -> measure it -> more models -> pitfalls.
    "ml": [
        "machine_learning/train_test_split.html",
        "machine_learning/label_encoding.html",
        "machine_learning/one_hot_encoding.html",
        "machine_learning/linear_regression_with_ols.html",
        "machine_learning/evaluation_metrics_for_regression.html",
        "machine_learning/logistic_regression.html",
        "machine_learning/knn.html",
        "machine_learning/confusion_matrix.html",
        "machine_learning/roc_curve_and_auc.html",
        "machine_learning/decision_tree.html",
        "machine_learning/random_forest.html",
        "machine_learning/gradient_boosting.html",
        "machine_learning/naive_bayes.html",
        "machine_learning/svm.html",
        "machine_learning/k_means.html",
        "machine_learning/pca.html",
        "machine_learning/cosine_similarity.html",
        "machine_learning/cross_validation.html",
        "machine_learning/bias_vs_variance.html",
        "machine_learning/ridge_and_lasso_regression.html",
        "machine_learning/label_imbalance_problem.html",
        "machine_learning/training_on_label_imbalanced_dataset.html",
        "machine_learning/hard_vs_soft_labelling.html",
        "machine_learning/sliding_window_for_timeseries_data.html",
        "machine_learning/model_and_data_drift.html",
    ],

    # One neuron -> a network -> how it learns -> what goes wrong -> practice.
    "dl": [
        "deep_learning/perceptron.html",
        "deep_learning/weights_and_biases.html",
        "deep_learning/activation_functions.html",
        "deep_learning/neural_network.html",
        "deep_learning/how_loss_is_calculated.html",
        "deep_learning/softmax_and_cross_entropy.html",
        "deep_learning/backpropagation.html",
        "deep_learning/gradient_descent_training.html",
        "deep_learning/linear_regression_with_gradient_descent.html",
        "deep_learning/optimizers_in_neural_networks.html",
        "deep_learning/optimizers_in_3d.html",
        "deep_learning/learning_rate_scheduling.html",
        "deep_learning/batch_processing_in_neural_networks.html",
        "deep_learning/gradient_descent_batch_processing.html",
        "deep_learning/feature_scaling_in_neural_networks.html",
        "deep_learning/weight_initialization.html",
        "deep_learning/vanishing_vs_exploding_gradient.html",
        "deep_learning/gradient_clipping.html",
        "deep_learning/residual_connections.html",
        "deep_learning/batch_normalization.html",
        "deep_learning/layer_normalization.html",
        "deep_learning/overfitting_vs_underfitting.html",
        "deep_learning/model_training_curve.html",
        "deep_learning/dropout_in_neural_networks.html",
        "deep_learning/regularization_in_neural_networks.html",
        "deep_learning/early_stopping_in_neural_networks.html",
        "deep_learning/hyper-paramter_tuning.html",
        "deep_learning/data_sparsity.html",
        "deep_learning/neural_network_for_regression.html",
        "deep_learning/neural_network_for_unsupervised_learning.html",
        "deep_learning/reproducibility_of_model.html",
        "deep_learning/model_training_on_cpu_vs_gpu.html",
    ],

    # Cost -> built-in types -> search -> sort -> recursion -> structures ->
    # graphs -> techniques.
    "dsa": [
        "dsa/big_o_notation.html",
        "dsa/lists_in_python.html",
        "dsa/strings_in_python.html",
        "dsa/dictionaries_in_python.html",
        "dsa/linear_search.html",
        "dsa/binary_search.html",
        "dsa/interpolation_search.html",
        "dsa/fibonacci_search.html",
        "dsa/bubble_sort.html",
        "dsa/selection_sort.html",
        "dsa/insertion_sort.html",
        "dsa/recursion_and_call_stack.html",
        "dsa/divide_and_conquer.html",
        "dsa/merge_sort.html",
        "dsa/quick_sort.html",
        "dsa/counting_sort.html",
        "dsa/radix_sort.html",
        "dsa/stacks.html",
        "dsa/queues.html",
        "dsa/linked_lists.html",
        "dsa/hash_tables.html",
        "dsa/binary_search_trees.html",
        "dsa/heaps_and_priority_queues.html",
        "dsa/heap_sort.html",
        "dsa/trie_prefix_tree.html",
        "dsa/union_find.html",
        "dsa/graph_representations.html",
        "dsa/breadth_first_search.html",
        "dsa/depth_first_search.html",
        "dsa/cycle_detection.html",
        "dsa/topological_sort.html",
        "dsa/dijkstras.html",
        "dsa/bellman_ford.html",
        "dsa/a_star.html",
        "dsa/minimum_spanning_tree.html",
        "dsa/two_pointers.html",
        "dsa/sliding_window.html",
        "dsa/greedy_algorithms.html",
        "dsa/backtracking.html",
        "dsa/dynamic_programming.html",
        "dsa/kmp_string_matching.html",
    ],

    # Text as numbers -> encodings -> embeddings -> sequences -> RNN -> LSTM.
    "nlp": [
        "natural_language_processing/ascii_codes.html",
        "natural_language_processing/tokenization.html",
        "natural_language_processing/text_normalization_pipeline.html",
        "natural_language_processing/stemming_vs_lemmatization.html",
        "natural_language_processing/n_gram.html",
        "natural_language_processing/word_cloud.html",
        "natural_language_processing/why_text_encoding_is_needed_in_nlp.html",
        "natural_language_processing/text_encoding_techniques_in_nlp.html",
        "natural_language_processing/how_words_are_represented_in_neural_networks.html",
        "natural_language_processing/what_are_embeddings.html",
        "natural_language_processing/how_are_embeddings_generated.html",
        "natural_language_processing/how_neural_network_text.html",
        "natural_language_processing/what_is_a_sequence.html",
        "natural_language_processing/sequential_data_preparation_with_sliding_window.html",
        "natural_language_processing/normalization_techniques_for_sequential_data.html",
        "natural_language_processing/limitations_of_ann_with_sequential_data.html",
        "natural_language_processing/what_is_a_recurrent_cell.html",
        "natural_language_processing/how_rnn_process_text.html",
        "natural_language_processing/rnn_architecture.html",
        "natural_language_processing/rnn.html",
        "natural_language_processing/backpropagation_through_time.html",
        "natural_language_processing/vanishing_gradient_problem_in_rnn.html",
        "natural_language_processing/what_is_lstm.html",
        "natural_language_processing/forget_gate_in_lstm.html",
        "natural_language_processing/input_gate_in_lstm.html",
        "natural_language_processing/candidate_memory_in_lstm.html",
        "natural_language_processing/output_gate_in_lstm.html",
        "natural_language_processing/how_lstm_processes_text.html",
        "natural_language_processing/what_is_a_gru.html",
        "natural_language_processing/what_is_bi_directional_layer.html",
        "natural_language_processing/attention_mechanism.html",
        "natural_language_processing/query_key_value.html",
        "natural_language_processing/self_attention.html",
        "natural_language_processing/multi_head_attention.html",
        "natural_language_processing/positional_encoding.html",
        "natural_language_processing/transformer_architecture.html",
        "natural_language_processing/bert_vs_gpt.html",
    ],

    # Pixels -> one convolution -> its knobs -> a whole CNN -> training it.
    "computer-vision": [
        "computer_vision/how_neural_network_process_images.html",
        "computer_vision/grayscale_image_processing.html",
        "computer_vision/rgb_image_processing.html",
        # The classical floor under the CNN modules, in the order each one
        # depends on the last: colour before histograms, histograms before
        # thresholding, thresholding before the morphology that cleans a mask
        # up, and convolution immediately before the edge detector that is one.
        "computer_vision/colour_spaces_rgb_hsv.html",
        "computer_vision/histograms_and_equalisation.html",
        "computer_vision/thresholding.html",
        "computer_vision/erosion_and_dilation.html",
        "computer_vision/blur_gaussian_median_bilateral.html",
        "computer_vision/convolution_kernels.html",
        "computer_vision/edge_detection.html",
        "computer_vision/resizing_and_interpolation.html",
        "computer_vision/affine_transforms.html",
        "computer_vision/feature_map_in_cnn.html",
        "computer_vision/receptive_field.html",
        "computer_vision/padding_in_cnn.html",
        "computer_vision/strides_in_cnn.html",
        "computer_vision/parameter_sharing_in_cnn.html",
        "computer_vision/how_relu_works_in_cnn.html",
        "computer_vision/downsampling_in_cnn.html",
        "computer_vision/how_dense_layer_works_in_cnn.html",
        "computer_vision/one_by_one_convolutions.html",
        "computer_vision/calculating_parameters_in_cnn.html",
        "computer_vision/cnn.html",
        "computer_vision/data_loaders_in_cnn.html",
        "computer_vision/image_data_augmentation.html",
        "computer_vision/transfer_learning_with_cnn.html",
        "computer_vision/iou_and_non_max_suppression.html",
        "computer_vision/object_detection_with_bounding_boxes.html",
        "computer_vision/resnet_and_identity_shortcuts.html",
        "computer_vision/semantic_segmentation_unet.html",
    ],

    # What a database is -> define -> insert -> query -> aggregate -> advanced.
    "db": [
        "database/what_are_relational_databases.html",
        "database/what_are_non_relational_databases.html",
        "database/datatypes_in_sql.html",
        "database/ddl_in_sql.html",
        # Schema design: what the DDL is for. Keys before constraints
        # because a foreign key is the constraint everything else leans on,
        # and both before normalization, which is an argument about how to
        # arrange tables that already have keys.
        "database/primary_and_foreign_keys.html",
        "database/constraints_in_sql.html",
        "database/normalization_in_sql.html",
        "database/dml_in_sql.html",
        "database/transactions_and_acid.html",
        "database/where_clause_in_sql.html",
        "database/null_handling_in_sql.html",
        "database/order_by_in_sql.html",
        "database/limit_and_offset_in_sql.html",
        "database/case_and_views_in_sql.html",
        "database/aggregate_functions_in_sql.html",
        "database/groupby_in_sql.html",
        "database/having_in_sql.html",
        "database/query_execution_order.html",
        "database/joins_in_sql.html",
        "database/self_joins_in_sql.html",
        "database/union_intersect_except_in_sql.html",
        "database/subqueries_in_sql.html",
        "database/exists_vs_in_vs_join.html",
        "database/common_table_expressions_in_sql.html",
        "database/recursive_ctes_in_sql.html",
        "database/window_functions_in_sql.html",
        "database/regular_expressions_in_sql.html",
        "database/indexes_in_sql.html",
        "database/composite_and_covering_indexes.html",
        "database/explain_and_query_plans.html",
        # Concurrency last: both of these assume transactions, which
        # transactions_and_acid introduces much earlier.
        "database/isolation_levels.html",
        "database/deadlocks_in_sql.html",
    ],

    # How an LLM reads -> how it predicts -> how it is trained -> how it is shrunk.
    "gen-ai": [
        "gen_ai/how_llms_process_text.html",
        "gen_ai/byte_pair_encoding_tokenizer.html",
        "gen_ai/how_llms_predict_next_word.html",
        "gen_ai/queries_keys_and_values.html",
        "gen_ai/casual_language_modeling.html",
        "gen_ai/masked_language_modeling.html",
        "gen_ai/quantization_in_llms.html",
        "gen_ai/lora_in_llms.html",
        "gen_ai/knowledge_distillation_in_llms.html",
        "gen_ai/embeddings_and_vector_search.html",
        "gen_ai/dot_product_vs_cosine_similarity.html",
        "gen_ai/tf_idf.html",
        "gen_ai/bm25_and_sparse_retrieval.html",
        "gen_ai/indexing_in_vector_databases.html",
        "gen_ai/ann_indexing_hnsw_and_ivf.html",
        "gen_ai/chunking_strategies_for_rag.html",
        "gen_ai/recursive_chunking.html",
        "gen_ai/structure_aware_chunking.html",
        "gen_ai/semantic_chunking.html",
        "gen_ai/context_aware_chunking.html",
        "gen_ai/parent_document_retriever.html",
        "gen_ai/rag.html",
        "gen_ai/retrieval_evaluation_metrics.html",
        "gen_ai/hit_rate_at_k.html",
        "gen_ai/recall_at_k.html",
        "gen_ai/precision_at_k.html",
        "gen_ai/mean_reciprocal_rank.html",
        "gen_ai/hybrid_search_reciprocal_rank_fusion.html",
        "gen_ai/reranking_bi_encoders_vs_cross_encoders.html",
        "gen_ai/maximal_marginal_relevance.html",
        "gen_ai/query_rewriting_and_hyde.html",
        "gen_ai/multi_query_retriever.html",
        "gen_ai/self_query_retriever.html",
        "gen_ai/corrective_rag.html",
        "gen_ai/context_window_and_kv_cache.html",
        "gen_ai/fine_tuning_vs_rlhf.html",
        "gen_ai/hallucination_and_grounding.html",
        "gen_ai/groundedness_in_llm_evaluation.html",
        "gen_ai/correctness_in_llm_evaluation.html",
        "gen_ai/relevance_in_llm_evaluation.html",
        "gen_ai/completeness_in_llm_evaluation.html",
        "gen_ai/caching_in_rag_pipelines.html",
        "gen_ai/permission_filtering_in_rag.html",
        "gen_ai/distributed_retrieval_and_sharding.html",
    ],

    # Generated - see _INTERVIEW above.
    "interview": _INTERVIEW,

    # Run it first, then meet the pieces: the track teaches by execution.
    "python": [
        "python/hello_python.html",
        "python/input_and_output.html",
        "python/variables_and_types.html",
        "python/type_conversion.html",
        "python/numbers_and_operators.html",
        "python/strings_and_slicing.html",
        "python/string_methods.html",
        "python/slicing_step_negatives.html",
        "python/f_strings_and_formatting.html",
        "python/lists_and_indexing.html",
        "python/mutability_and_aliasing.html",
        "python/shallow_and_deep_copy.html",
        "python/sorted_with_key.html",
        "python/dictionaries.html",
        "python/dictionary_methods.html",
        "python/nested_data_structures.html",
        "python/tuples_and_unpacking.html",
        "python/sets_and_set_operations.html",
        "python/booleans_and_comparisons.html",
        "python/none_and_truthiness.html",
        "python/if_elif_else.html",
        "python/nested_conditionals.html",
        "python/conditional_expressions.html",
        "python/match_and_case.html",
        "python/try_and_except.html",
        "python/for_loops_and_range.html",
        "python/nested_for_loops.html",
        "python/loop_else.html",
        "python/range_step.html",
        "python/enumerate_function.html",
        "python/zip_function.html",
        "python/list_comprehensions.html",
        "python/conditional_comprehensions.html",
        "python/dict_and_set_comprehensions.html",
        "python/while_loops_and_control.html",
        "python/functions_and_return.html",
        "python/function_arguments.html",
        "python/args_and_kwargs.html",
        "python/lambda_map_filter.html",
        "python/variable_scope.html",
        "python/reading_errors.html",
        "python/files_and_with.html",
        "python/modules_and_import.html",
        "python/generators_and_yield.html",
        "python/classes_and_objects.html",
        "python/inheritance.html",
    ],
}


# A curated cross-track route for someone starting from nothing. Each stage is
# a handful of modules from the sequences above, in the order they build on
# each other.
LEARNING_PATH = [
    {
        "title": "Groundwork",
        "blurb": "The handful of maths ideas everything else leans on.",
        "modules": [
            "maths/equation_of_line.html",
            "maths/vectors_and_dot_product.html",
            "maths/derivatives_and_slope.html",
            "maths/mean_variance_standard_deviation.html",
            "maths/probability_basics.html",
        ],
    },
    {
        "title": "Your first models",
        "blurb": "Split the data, fit something simple, then find out if it worked.",
        "modules": [
            "machine_learning/train_test_split.html",
            "machine_learning/one_hot_encoding.html",
            "machine_learning/linear_regression_with_ols.html",
            "machine_learning/knn.html",
            "machine_learning/logistic_regression.html",
            "machine_learning/confusion_matrix.html",
        ],
    },
    {
        "title": "How learning actually works",
        "blurb": "From one neuron to a network that trains itself downhill.",
        "modules": [
            "deep_learning/perceptron.html",
            "deep_learning/activation_functions.html",
            "deep_learning/how_loss_is_calculated.html",
            "deep_learning/gradient_descent_training.html",
            "deep_learning/neural_network.html",
        ],
    },
    {
        "title": "Making training behave",
        "blurb": "The failure modes every practitioner meets, and their fixes.",
        "modules": [
            "deep_learning/overfitting_vs_underfitting.html",
            "machine_learning/cross_validation.html",
            "deep_learning/dropout_in_neural_networks.html",
            "deep_learning/early_stopping_in_neural_networks.html",
            "deep_learning/model_training_curve.html",
        ],
    },
    {
        "title": "Pick a specialism",
        "blurb": "Same foundations, four directions. Start wherever you like.",
        "modules": [
            "computer_vision/feature_map_in_cnn.html",
            "natural_language_processing/what_are_embeddings.html",
            "gen_ai/how_llms_predict_next_word.html",
            "dsa/big_o_notation.html",
            "database/joins_in_sql.html",
        ],
    },
]


# ---------------------------------------------------------------------------
# Named routes.
#
# LEARNING_PATH above is the cross-track route for someone starting from
# nothing. It is the right answer to "where do I begin" and the wrong answer to
# "I already write Python, take me to LLMs" - which was the only question the
# hub could not answer, because there was exactly one path.
#
# Each route below is ordered so a stage only uses ideas introduced before it,
# and pulls from whichever track has the module rather than staying inside one.
# Every path referenced here is checked against the catalogue at build time.
# ---------------------------------------------------------------------------

LEARNING_PATHS = [
    {
        "key": "start",
        "title": "Start from scratch",
        "blurb": "No background assumed. The maths everything leans on, your first "
                 "models, then enough of each specialism to choose one.",
        "stages": LEARNING_PATH,
    },
    {
        "key": "python",
        "title": "Python",
        "blurb": "The language every other track writes its examples in. Real code, "
                 "run in the browser, from your first print to your own functions.",
        "stages": [
            {
                "title": "First lines",
                "blurb": "Get something running, then learn what a variable actually holds.",
                "modules": [
                    "python/hello_python.html",
                    "python/variables_and_types.html",
                    "python/numbers_and_operators.html",
                ],
            },
            {
                "title": "Working with data",
                "blurb": "The three containers almost every Python program is built from.",
                "modules": [
                    "python/strings_and_slicing.html",
                    "python/lists_and_indexing.html",
                    "python/dictionaries.html",
                ],
            },
            {
                "title": "Making decisions",
                "blurb": "Comparisons produce True and False; branches act on them.",
                "modules": [
                    "python/booleans_and_comparisons.html",
                    "python/if_elif_else.html",
                ],
            },
            {
                "title": "Doing it repeatedly",
                "blurb": "Loops, and knowing which of the two you need.",
                "modules": [
                    "python/for_loops_and_range.html",
                    "python/while_loops_and_control.html",
                ],
            },
            {
                "title": "Your own building blocks",
                "blurb": "Package work behind a name, and read the traceback when it breaks.",
                "modules": [
                    "python/functions_and_return.html",
                    "python/reading_errors.html",
                    "dsa/lists_in_python.html",
                    "dsa/dictionaries_in_python.html",
                ],
            },
        ],
    },
    {
        "key": "ml",
        "title": "Machine Learning",
        "blurb": "Classical models end to end: prepare the data, fit something, and "
                 "find out honestly whether it worked.",
        "stages": [
            {
                "title": "The maths you will actually use",
                "blurb": "Four ideas that turn up in every model on this path.",
                "modules": [
                    "maths/mean_variance_standard_deviation.html",
                    "maths/probability_basics.html",
                    "maths/vectors_and_dot_product.html",
                    "maths/distance_metrics.html",
                ],
            },
            {
                "title": "Getting data ready",
                "blurb": "Everything that has to happen before a model sees a single row.",
                "modules": [
                    "machine_learning/train_test_split.html",
                    "machine_learning/label_encoding.html",
                    "machine_learning/one_hot_encoding.html",
                ],
            },
            {
                "title": "Your first models",
                "blurb": "A line, a probability, and a vote among neighbours.",
                "modules": [
                    "machine_learning/linear_regression_with_ols.html",
                    "machine_learning/logistic_regression.html",
                    "machine_learning/knn.html",
                ],
            },
            {
                "title": "Did it actually work?",
                "blurb": "The half of machine learning that decides whether the other half mattered.",
                "modules": [
                    "machine_learning/evaluation_metrics_for_regression.html",
                    "machine_learning/confusion_matrix.html",
                    "machine_learning/roc_curve_and_auc.html",
                    "machine_learning/cross_validation.html",
                ],
            },
            {
                "title": "Trees, forests and boosting",
                "blurb": "The models that win on tabular data, in the order they were invented.",
                "modules": [
                    "machine_learning/decision_tree.html",
                    "machine_learning/random_forest.html",
                    "machine_learning/gradient_boosting.html",
                ],
            },
            {
                "title": "The rest of the toolbox",
                "blurb": "Margins, probabilities, clusters and dimensions.",
                "modules": [
                    "machine_learning/svm.html",
                    "machine_learning/naive_bayes.html",
                    "machine_learning/k_means.html",
                    "machine_learning/pca.html",
                ],
            },
            {
                "title": "What goes wrong in production",
                "blurb": "The four failures that account for most disappointing models.",
                "modules": [
                    "machine_learning/bias_vs_variance.html",
                    "machine_learning/ridge_and_lasso_regression.html",
                    "machine_learning/training_on_label_imbalanced_dataset.html",
                    "machine_learning/model_and_data_drift.html",
                ],
            },
        ],
    },
    {
        "key": "dl",
        "title": "Deep Learning",
        "blurb": "One neuron to a network that trains itself, then everything that "
                 "makes training behave.",
        "stages": [
            {
                "title": "One neuron",
                "blurb": "A weighted sum, a bias, an activation. Everything deeper is this repeated.",
                "modules": [
                    "deep_learning/perceptron.html",
                    "deep_learning/weights_and_biases.html",
                    "deep_learning/activation_functions.html",
                ],
            },
            {
                "title": "Learning by going downhill",
                "blurb": "Measure the error, follow the slope, and push it back through the layers.",
                "modules": [
                    "deep_learning/how_loss_is_calculated.html",
                    "deep_learning/gradient_descent_training.html",
                    "deep_learning/backpropagation.html",
                ],
            },
            {
                "title": "A whole network",
                "blurb": "Stack the neurons and pick an output that suits the task.",
                "modules": [
                    "deep_learning/neural_network.html",
                    "deep_learning/softmax_and_cross_entropy.html",
                    "deep_learning/neural_network_for_regression.html",
                ],
            },
            {
                "title": "Making training work at all",
                "blurb": "Scale, initialisation, batches and the optimiser - before any clever tricks.",
                "modules": [
                    "deep_learning/feature_scaling_in_neural_networks.html",
                    "deep_learning/weight_initialization.html",
                    "deep_learning/batch_processing_in_neural_networks.html",
                    "deep_learning/optimizers_in_neural_networks.html",
                    "deep_learning/learning_rate_scheduling.html",
                ],
            },
            {
                "title": "When training breaks",
                "blurb": "Reading the curve, and the two ways gradients fail with depth.",
                "modules": [
                    "deep_learning/model_training_curve.html",
                    "deep_learning/overfitting_vs_underfitting.html",
                    "deep_learning/vanishing_vs_exploding_gradient.html",
                    "deep_learning/gradient_clipping.html",
                ],
            },
            {
                "title": "The standard fixes",
                "blurb": "What every modern architecture includes by default, and why.",
                "modules": [
                    "deep_learning/dropout_in_neural_networks.html",
                    "deep_learning/regularization_in_neural_networks.html",
                    "deep_learning/early_stopping_in_neural_networks.html",
                    "deep_learning/batch_normalization.html",
                    "deep_learning/residual_connections.html",
                ],
            },
        ],
    },
    {
        "key": "genai",
        "title": "Generative AI & LLMs",
        "blurb": "How text becomes numbers, how attention replaced recurrence, and "
                 "what it takes to actually serve a model.",
        "stages": [
            {
                "title": "Text into numbers",
                "blurb": "A model never sees words. This is what it sees instead.",
                "modules": [
                    "gen_ai/how_llms_process_text.html",
                    "gen_ai/byte_pair_encoding_tokenizer.html",
                    "natural_language_processing/what_are_embeddings.html",
                    "natural_language_processing/how_are_embeddings_generated.html",
                ],
            },
            {
                "title": "Why sequences were hard",
                "blurb": "The recurrent approach attention replaced - worth seeing before the fix.",
                "modules": [
                    "natural_language_processing/what_is_a_sequence.html",
                    "natural_language_processing/what_is_a_recurrent_cell.html",
                    "natural_language_processing/vanishing_gradient_problem_in_rnn.html",
                    "natural_language_processing/what_is_lstm.html",
                ],
            },
            {
                "title": "Attention",
                "blurb": "The mechanism the whole field now rests on, built up one piece at a time.",
                "modules": [
                    "natural_language_processing/attention_mechanism.html",
                    "natural_language_processing/query_key_value.html",
                    "natural_language_processing/self_attention.html",
                    "natural_language_processing/multi_head_attention.html",
                    "natural_language_processing/positional_encoding.html",
                    "natural_language_processing/transformer_architecture.html",
                ],
            },
            {
                "title": "How a language model is trained",
                "blurb": "Two objectives, and the split between the models they produced.",
                "modules": [
                    "gen_ai/casual_language_modeling.html",
                    "gen_ai/masked_language_modeling.html",
                    "natural_language_processing/bert_vs_gpt.html",
                    "gen_ai/how_llms_predict_next_word.html",
                ],
            },
            {
                "title": "Retrieval, properly",
                "blurb": "Most production LLM work is a retrieval problem wearing a generation hat.",
                "modules": [
                    "gen_ai/embeddings_and_vector_search.html",
                    "gen_ai/chunking_strategies_for_rag.html",
                    "gen_ai/rag.html",
                    "gen_ai/hybrid_search_reciprocal_rank_fusion.html",
                    "gen_ai/reranking_bi_encoders_vs_cross_encoders.html",
                    "gen_ai/retrieval_evaluation_metrics.html",
                ],
            },
            {
                "title": "Making it servable",
                "blurb": "Adaptation and efficiency: what each technique trades away, and for what.",
                "modules": [
                    "gen_ai/context_window_and_kv_cache.html",
                    "gen_ai/quantization_in_llms.html",
                    "gen_ai/lora_in_llms.html",
                    "gen_ai/fine_tuning_vs_rlhf.html",
                    "gen_ai/hallucination_and_grounding.html",
                ],
            },
        ],
    },
    {
        "key": "data-analytics",
        "title": "Data Analytics",
        "blurb": "Get the data out with SQL, describe it honestly with statistics, "
                 "and know where analysis stops and prediction starts.",
        "stages": [
            {
                "title": "Reading data with SQL",
                "blurb": "The clauses that answer most questions anyone will actually ask you.",
                "modules": [
                    "database/what_are_relational_databases.html",
                    "database/datatypes_in_sql.html",
                    "database/where_clause_in_sql.html",
                    "database/order_by_in_sql.html",
                    "database/limit_and_offset_in_sql.html",
                ],
            },
            {
                "title": "Summarising",
                "blurb": "Grouping, filtering groups, and why the clause order explains the errors.",
                "modules": [
                    "database/groupby_in_sql.html",
                    "database/having_in_sql.html",
                    "database/query_execution_order.html",
                    "database/case_and_views_in_sql.html",
                ],
            },
            {
                "title": "Combining tables",
                "blurb": "Where the real data lives: across several tables at once.",
                "modules": [
                    "database/joins_in_sql.html",
                    "database/union_intersect_except_in_sql.html",
                    "database/subqueries_in_sql.html",
                    "database/common_table_expressions_in_sql.html",
                ],
            },
            {
                "title": "Analytical SQL",
                "blurb": "Window functions, missing data, and why a query suddenly got slow.",
                "modules": [
                    "database/window_functions_in_sql.html",
                    "database/null_handling_in_sql.html",
                    "database/indexes_in_sql.html",
                ],
            },
            {
                "title": "Describing what you found",
                "blurb": "The statistics that stop a summary from being misleading.",
                "modules": [
                    "maths/mean_mode_and_median.html",
                    "maths/mean_variance_standard_deviation.html",
                    "maths/covariance_and_correlation.html",
                    "maths/the_normal_distribution.html",
                ],
            },
            {
                "title": "Where analysis becomes prediction",
                "blurb": "The smallest honest step from describing the past to modelling it.",
                "modules": [
                    "machine_learning/train_test_split.html",
                    "machine_learning/linear_regression_with_ols.html",
                    "machine_learning/confusion_matrix.html",
                ],
            },
        ],
    },
]
