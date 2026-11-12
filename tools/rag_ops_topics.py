# -*- coding: utf-8 -*-
"""The RAG operations pages in gen_ai/.

Pages about running a retrieval pipeline rather than scoring one: gating,
abstention, de-duplication, chunk-size sweeps, capacity, latency, failure
handling, ingestion and migration. Same entry shape as tools/rag_topics.py,
and each names a model in assets/vizlearn-ragops.js.

The long-form article for each lives in content/articles/gen_ai/<slug>.txt and
replaces the short `sections` here when build_articles runs, so `sections`
only has to be enough for the page to be valid on its own.
"""

import rag_topics as _rt

_t = _rt._t
WIDGETS = _rt.WIDGETS
ART = _rt.ART

# Two new tags for the card art; both reuse an existing drawing.
ART.setdefault("Operations", ART["Scale"])
ART.setdefault("Ingestion", ART["Chunking"])


def _range(id_, label, lo, hi, step, value):
    return {"id": id_, "label": label, "kind": "range",
            "min": lo, "max": hi, "step": step, "value": value}


def _select(id_, label, options, value=0):
    return {"id": id_, "label": label, "kind": "select", "value": value,
            "options": [{"label": l, "value": v} for l, v in options]}


def _toggle(id_, label, on):
    return {"id": id_, "label": label, "kind": "toggle", "value": 1 if on else 0}


def _topic(slug, group, level, title, asked, desc, lead, say, notice, takeaway):
    _t(slug=slug, group_label=group, level=level, title=title, asked=asked,
       desc=desc, lead=lead, say=say, notice=notice, viz=WIDGETS[slug],
       sections=[("What to remember", "<p>%s</p>" % takeaway)])


# --------------------------------------------------------------------------
# Similarity threshold gating
# --------------------------------------------------------------------------

WIDGETS["similarity_threshold_gating"] = {
    "model": "gate", "ops": True, "controls": [
        _select("strategy", "Strategy", [("absolute floor", "absolute"),
                                         ("score drop", "drop"),
                                         ("calibrated", "calibrated"),
                                         ("layered", "layered")], 0),
        _range("threshold", "Absolute cut-off (x100)", 10, 90, 1, 40),
        _range("minDrop", "Minimum drop (x100)", 0, 30, 1, 10),
        _range("target", "Target recall (%)", 80, 99, 1, 95),
    ], "data": {
        "calibration": [0.84, 0.79, 0.77, 0.74, 0.71, 0.69, 0.68, 0.66, 0.64,
                        0.62, 0.60, 0.58, 0.57, 0.55, 0.53, 0.51, 0.49, 0.48,
                        0.46, 0.42],
        "chunks": [
            {"text": "Refunds are issued within 14 days", "score": 0.84, "relevant": True},
            {"text": "The item must be unused", "score": 0.79, "relevant": True},
            {"text": "Refunds go to the original payment method", "score": 0.77, "relevant": True},
            {"text": "Digital goods are not refundable", "score": 0.74, "relevant": True},
            {"text": "Returns portal user guide", "score": 0.52, "relevant": False},
            {"text": "Exchanges are accepted for 30 days", "score": 0.48, "relevant": True},
            {"text": "Shipping rates by region", "score": 0.45, "relevant": False},
            {"text": "Warranty claims process", "score": 0.38, "relevant": False},
            {"text": "Careers page", "score": 0.31, "relevant": False},
            {"text": "Office relocation notice", "score": 0.24, "relevant": False}]}}

_topic(
    "similarity_threshold_gating", "Retrieval", "Intermediate",
    "Similarity Threshold Gating",
    "How do you stop irrelevant chunks reaching the model when top-k always "
    "returns k results?",
    "Filter retrieved chunks before they reach the model with a fixed floor, a "
    "score-drop cut and a threshold learned from labelled data, and see what "
    "each one keeps and loses.",
    "A retriever always returns k results, even when nothing in the corpus "
    "matches. <strong>A similarity gate sits between the retriever and the "
    "model and decides which chunks are good enough to pass.</strong> A fixed "
    "floor, a cut at the biggest score drop and a threshold learned from "
    "labelled data each fail in a different way, so production systems stack "
    "them.",
    "\"Top-k always returns k, so I gate. A floor removes junk, a score-drop "
    "cut adapts to each query, and a threshold learned from labelled data "
    "fits my domain. I aim for high recall, and if nothing passes I say I do "
    "not know.\"",
    ["Switch between the four strategies and watch which chunks pass.",
     "The absolute cut-off keeps a weak chunk at 0.52 or loses a useful one at "
     "0.48, depending on where it sits.",
     "Raising the target recall lowers the learned cut-off and lets more "
     "noise in."],
    "A retriever returns k chunks even when none are relevant, so put a gate "
    "in front of the model. Stack a floor, a score-drop cut and a learned "
    "threshold, aim for high recall, and say so when nothing passes.")


# --------------------------------------------------------------------------
# Abstention in RAG
# --------------------------------------------------------------------------

WIDGETS["abstention_in_rag"] = {
    "model": "abstain", "ops": True, "controls": [
        _range("top1", "Top retrieval score (x100)", 0, 100, 1, 62),
        _range("minTop1", "Gate 1 minimum (x100)", 20, 80, 1, 45),
        _range("coverage", "Share of the answer in the corpus (%)", 0, 100, 5, 80),
        _toggle("selfAbstain", "Model says it does not know", False),
        _range("unsupported", "Unsupported claims in the answer (%)", 0, 60, 5, 10),
        _range("limit", "Faithfulness limit (%)", 0, 40, 5, 20),
    ], "data": {}}

_topic(
    "abstention_in_rag", "LLM evaluation", "Advanced",
    "Abstention in RAG",
    "How does a RAG system know when to say it cannot answer?",
    "Three gates - retrieval confidence, a prompt that permits \"I do not "
    "know\", and a faithfulness check - and how their thresholds trade "
    "false abstentions against hallucinated answers.",
    "Language models are trained to be helpful, so given weak context they "
    "answer anyway. <strong>Abstention is the system refusing to answer when "
    "the knowledge base cannot support one.</strong> It needs three gates, "
    "ordered by cost, because no single check catches every failure.",
    "\"Three gates, cheapest first. Retrieval confidence stops the call "
    "before the model runs. The prompt lets the model say it does not know. "
    "A faithfulness check catches what it made up anyway. I calibrate the "
    "thresholds on answerable and unanswerable questions.\"",
    ["Lower the top retrieval score below the Gate 1 minimum and the system "
     "stops before any model call.",
     "Set the share of the answer in the corpus to 10 and let every gate "
     "pass: that is a hallucinated answer.",
     "Raise the unsupported claims past the limit and the check rejects "
     "the answer."],
    "Models answer even without evidence. Gate on retrieval confidence, let "
    "the prompt allow \"I do not know\", and check faithfulness afterwards, "
    "tuning the thresholds so false abstentions stay rare.")


# --------------------------------------------------------------------------
# Chunk deduplication
# --------------------------------------------------------------------------

WIDGETS["chunk_deduplication"] = {
    "model": "dedup", "ops": True, "controls": [
        _select("strategy", "Strategy", [("exact copies only", "exact"),
                                         ("near-duplicates", "near"),
                                         ("no deduplication", "none")], 1),
        _range("threshold", "Near-duplicate threshold (x100)", 50, 100, 1, 80),
    ], "data": {"chunks": [
        {"text": "Vector DBs store embeddings (original)", "cluster": 1, "sim": 0.0, "tokens": 64},
        {"text": "Same text, different spacing", "cluster": 1, "sim": 1.0, "tokens": 64},
        {"text": "Same text, one word changed", "cluster": 1, "sim": 0.91, "tokens": 64},
        {"text": "Same text, float32 became float16", "cluster": 1, "sim": 0.82, "tokens": 64, "distinct": True},
        {"text": "Binary trees keep data sorted (original)", "cluster": 2, "sim": 0.0, "tokens": 48},
        {"text": "Binary trees, copied from another wiki", "cluster": 2, "sim": 1.0, "tokens": 48},
        {"text": "Refund policy v1", "cluster": 3, "sim": 0.0, "tokens": 90},
        {"text": "Refund policy v2: window now 30 days", "cluster": 3, "sim": 0.74, "tokens": 90, "distinct": True},
        {"text": "Query planning in SQL", "cluster": 4, "sim": 0.0, "tokens": 70},
        {"text": "Index maintenance in Postgres", "cluster": 5, "sim": 0.0, "tokens": 70}]}}

_topic(
    "chunk_deduplication", "Ingestion", "Intermediate",
    "Chunk Deduplication",
    "How do you stop duplicate and near-duplicate chunks from wasting the "
    "index and the context window?",
    "Remove exact and near-duplicate chunks at ingestion with hashing and "
    "MinHash, and filter repeats at retrieval with MMR, without merging "
    "chunks that state different facts.",
    "Company documents repeat themselves, and each copy costs index space, "
    "embedding money and room in the context window. <strong>Exact copies are "
    "found by hashing cleaned text; near-copies need a similarity test on "
    "word groups, and MinHash makes that fast.</strong> The risk on the other "
    "side is merging two chunks that look alike but disagree.",
    "\"Hash the cleaned text for exact copies, MinHash for near-copies, run "
    "the cheap one first, and use MMR at query time. The threshold has to be "
    "high enough that a chunk with a different fact is not treated as a "
    "copy.\"",
    ["Exact hashing removes the byte-identical chunks and leaves the "
     "near-copies.",
     "Lowering the threshold removes chunks that are not copies at all.",
     "The red rows are distinct chunks that were lost."],
    "Hash cleaned text for exact copies, use MinHash for near-copies, and "
    "filter repeats at retrieval with MMR. Keep the threshold high enough "
    "that a chunk with a different fact survives.")


# --------------------------------------------------------------------------
# Chunk size optimization
# --------------------------------------------------------------------------

WIDGETS["chunk_size_optimization"] = {
    "model": "sweep", "ops": True, "controls": [
        _select("size", "Chunk size (words)", [("8", 8), ("16", 16), ("32", 32),
                                               ("64", 64), ("128", 128)], 1),
        _select("overlap", "Overlap", [("0%", 0), ("25%", 25)], 1),
    ], "data": {
        "k": 3, "sizes": [8, 16, 32, 64, 128],
        "recall0": [0.38, 0.75, 0.75, 0.92, 1.0],
        "recall25": [0.46, 0.96, 1.0, 1.0, 1.0],
        "chunks0": [336, 168, 96, 48, 24],
        "chunks25": [437, 216, 120, 48, 24]}}

_topic(
    "chunk_size_optimization", "Chunking", "Advanced",
    "Chunk Size Optimization",
    "How do you pick a chunk size and overlap without guessing?",
    "Sweep chunk sizes and overlaps on a test set, compare recall against "
    "tokens per query and index size, and choose from the Pareto front.",
    "Chunk size decides what the retriever can find, what it costs and what "
    "the model reads. <strong>Too small and the answer is cut across two "
    "chunks; too large and each chunk blurs several topics and sends more "
    "text to the model.</strong> No number is right for every corpus, so the "
    "method is to measure on your own questions.",
    "\"I build a test set from real questions, sweep sizes and overlaps, "
    "and compare recall against tokens per query and index size. I choose "
    "the cheapest setting that clears my recall bar, and I repeat the sweep "
    "when the model or the data changes.\"",
    ["At 8 words most facts are cut in half and recall collapses.",
     "Overlap rescues cut facts at small sizes and adds only storage at "
     "large ones.",
     "Size 128 matches size 32 with overlap on recall and sends four times "
     "the tokens."],
    "Chunk size is the first setting to tune. Build a test set from real "
    "questions, sweep sizes and overlaps, compare recall against cost, and "
    "pick from the Pareto front.")


# --------------------------------------------------------------------------
# Debugging RAG
# --------------------------------------------------------------------------

WIDGETS["debugging_rag"] = {
    "model": "trace", "ops": True, "controls": [
        _range("rank", "Rank of the correct chunk", 1, 11, 1, 7),
        _range("k", "Chunks in the prompt", 1, 10, 1, 5),
        _range("faithful", "Model uses the context (%)", 0, 100, 5, 90),
        _toggle("truncate", "Output parser truncates the answer", False),
    ], "data": {}}

_topic(
    "debugging_rag", "Evaluation", "Intermediate",
    "Debugging RAG",
    "A RAG system gives the wrong answer when the knowledge base has the "
    "right one. How do you find out why?",
    "Trace a wrong RAG answer through retrieval, context, synthesis and "
    "post-processing, run contrastive experiments, and turn each fix into a "
    "regression test.",
    "Every wrong answer from a RAG system was lost at one of three stages. "
    "<strong>Retrieval did not fetch the chunk, the model did not use it, or "
    "something after the model damaged the answer.</strong> Record a trace, "
    "check the stages in order, and fix the first one that fails.",
    "\"I check retrieval first: where did the right chunk rank? Then whether "
    "it fit in the prompt, then contrastive experiments for the model, then "
    "the raw reply against the final output. Every fix becomes a regression "
    "test.\"",
    ["Move the rank past the number of chunks in the prompt: the chunk was "
     "retrieved and then cut.",
     "Set the rank to 11 and the fault is in retrieval.",
     "A healthy trace with a truncating parser blames post-processing."],
    "A wrong answer was lost at retrieval, synthesis or after the model. "
    "Record a trace, check the stages in order, change one thing at a time "
    "and add a regression test for every fix.")


# --------------------------------------------------------------------------
# Batch embedding generation
# --------------------------------------------------------------------------

WIDGETS["batch_embedding_generation"] = {
    "model": "batch", "ops": True, "controls": [
        _select("batch", "Batch size", [("8", 8), ("16", 16), ("32", 32), ("64", 64),
                                        ("128", 128), ("256", 256), ("512", 512),
                                        ("1024", 1024)], 5),
        _toggle("sorted", "Sort texts by length", False),
        _select("model", "Model", [("MiniLM-L6 (384 dims)", 0), ("mpnet-base (768 dims)", 1)], 0),
        _select("gpu", "GPU memory", [("8 GB", 8), ("16 GB", 16), ("24 GB", 24)], 1),
    ], "data": {"sample": 2000, "texts": 100000, "models": [
        {"name": "all-MiniLM-L6-v2", "hidden": 384, "layers": 6, "gb": 0.1},
        {"name": "all-mpnet-base-v2", "hidden": 768, "layers": 12, "gb": 0.45}]}}

_topic(
    "batch_embedding_generation", "Ingestion", "Intermediate",
    "Batch Embedding Generation",
    "How do you embed 100,000 texts quickly without running out of GPU "
    "memory?",
    "Embed 100,000 texts with Sentence Transformers: pick a model, batch and "
    "sort by length, clean the input, and save the matrix with a row "
    "mapping.",
    "Embedding at scale means turning a pile of text into vectors a search "
    "system can compare. <strong>The gains come from batching, sorting texts "
    "by length so batches carry little padding, and keeping the memory in "
    "budget.</strong> Cleaning the input, normalising the vectors and saving "
    "the row mapping decide whether the result is usable.",
    "\"I encode lists, not single texts, sorted by length so padding stays "
    "small. I check the model's token limit, clean and normalise the text, "
    "keep the row-to-title mapping, and save the matrix in a "
    "memory-mappable format.\"",
    ["Sorting by length cuts the blank tokens a batch carries.",
     "A large batch on a small card runs out of memory.",
     "A bigger model needs more memory for the same batch."],
    "Encode in batches, sort texts by length, clean the input and keep the "
    "row mapping. Normalise the vectors, save them as a memory-mappable "
    "array, and test float16 before relying on it.")


# --------------------------------------------------------------------------
# Embedding resilience and checkpointing
# --------------------------------------------------------------------------

WIDGETS["embedding_resilience_and_checkpointing"] = {
    "model": "retry", "ops": True, "controls": [
        _range("fail", "Failure rate (%)", 0, 80, 5, 30),
        _range("retries", "Retries", 0, 8, 1, 3),
        _range("base", "Base backoff (seconds)", 1, 10, 1, 1),
        _toggle("jitter", "Jitter", True),
        _toggle("checkpoint", "Checkpointing", True),
    ], "data": {"batches": 5000, "batchSec": 0.5}}

_topic(
    "embedding_resilience_and_checkpointing", "Operations", "Advanced",
    "Embedding Resilience and Checkpointing",
    "How do you embed half a million chunks without losing progress to rate "
    "limits and crashes?",
    "A rate limiter, retries with backoff and jitter, and a checkpoint store "
    "make a batch embedding job survive failures and resume without paying "
    "twice.",
    "A large embedding job has to survive rate limits, temporary errors and "
    "crashes. <strong>Three layers do it: a sliding-window rate limiter, "
    "retries with exponential backoff and jitter, and a checkpoint that "
    "records every finished batch.</strong> Together they let a restart "
    "continue instead of starting again.",
    "\"A sliding-window limiter on requests and tokens, retries only for "
    "temporary errors with backoff and jitter, and a crash-safe checkpoint "
    "so a restart skips finished batches. I scope time and cost first and "
    "log progress.\"",
    ["Raise the failure rate with few retries and batches are abandoned.",
     "More retries rescue them and cost extra attempts.",
     "Without a checkpoint, a crash at 70% redoes 70% of the work."],
    "Rate limit with a sliding window, retry only temporary errors with "
    "backoff and jitter, and checkpoint every finished batch so a restart "
    "never pays twice.")


# --------------------------------------------------------------------------
# Document ingestion pipeline
# --------------------------------------------------------------------------

WIDGETS["document_ingestion_pipeline"] = {
    "model": "funnel", "ops": True, "controls": [
        _toggle("ocr", "OCR", True),
        _range("scanned", "Scanned share (%)", 0, 80, 5, 20),
        _range("retry", "Embedding retries", 0, 4, 1, 2),
        _range("workers", "Workers", 1, 32, 1, 4),
    ], "data": {"pdfs": 10000}}

_topic(
    "document_ingestion_pipeline", "Ingestion", "Intermediate",
    "Document Ingestion Pipeline",
    "How do you turn ten thousand PDFs into searchable vectors without "
    "losing documents on the way?",
    "A five-stage ingestion pipeline - extract with OCR, clean, chunk, embed "
    "and store - with deterministic IDs, idempotent upserts and "
    "checkpointing, and a funnel model of what each stage loses.",
    "An ingestion pipeline turns documents into vectors a RAG system can "
    "search. <strong>It has five stages: extract, clean, chunk, embed and "
    "store, and the engineering is in surviving failures and counting what "
    "each stage loses.</strong> Scanned files that skip OCR vanish at stage "
    "one, and nothing downstream says so.",
    "\"Five stages: extract with an OCR fallback, clean, chunk by tokens, "
    "embed in batches and upsert with deterministic IDs. I checkpoint so a "
    "crash costs one batch, and I count documents at every stage so silent "
    "loss shows up.\"",
    ["Turn OCR off and watch scanned files drop out at the first stage.",
     "The slowest stage is marked red; add workers and the time falls.",
     "Fewer embedding retries lose a few documents at stage four."],
    "Ingestion is extract, clean, chunk, embed, store. OCR scans, chunk by "
    "tokens, use deterministic IDs with upserts, checkpoint progress and "
    "count documents at every stage.")


# --------------------------------------------------------------------------
# Distributed ingestion pipeline
# --------------------------------------------------------------------------

WIDGETS["distributed_ingestion_pipeline"] = {
    "model": "idempotency", "ops": True, "controls": [
        _select("delivery", "Delivery", [("at least once", "atleast"),
                                         ("at most once", "atmost")], 0),
        _range("crash", "Worker crash rate (%)", 0, 30, 1, 10),
        _select("layer", "Safety layers", [("random IDs, plain insert", 0),
                                           ("content IDs and upsert", 1),
                                           ("IDs, upsert and cleanup", 2)], 0),
    ], "data": {"chunks": 30000, "edited": 0.10, "changed": 0.4}}

_topic(
    "distributed_ingestion_pipeline", "Operations", "Advanced",
    "Distributed Ingestion Pipeline",
    "How do you ingest thousands of articles a day so a crash or a retry "
    "never leaves duplicates or gaps?",
    "Idempotent workers, deterministic chunk IDs, upserts, stale-chunk "
    "cleanup and a dead-letter queue keep a distributed ingestion pipeline "
    "correct under at-least-once delivery.",
    "A distributed ingestion pipeline is about safety more than speed. "
    "<strong>Delivery is at least once, so every write must be harmless to "
    "repeat: chunk IDs come from the content, writes are upserts, and old "
    "chunks are removed after the new ones land.</strong> Otherwise a crash "
    "leaves duplicates, gaps or stale text.",
    "\"At-least-once delivery with idempotent workers: deterministic chunk "
    "IDs, a version check and upserts. New chunks before deletes, a "
    "dead-letter queue for poison messages, change detection to skip "
    "unchanged articles.\"",
    ["With random IDs, each redelivery adds a duplicate.",
     "At-most-once delivery shows no duplicates and loses chunks.",
     "Only the third safety setting leaves a clean index."],
    "Distribute for safety. Use at-least-once delivery with idempotent "
    "workers, deterministic chunk IDs, upserts and cleanup.")


# --------------------------------------------------------------------------
# Embedding model migration
# --------------------------------------------------------------------------

WIDGETS["embedding_model_migration"] = {
    "model": "migrate", "ops": True, "controls": [
        _select("strategy", "Strategy", [("in place", "inplace"),
                                         ("blue-green", "bluegreen")], 0),
        _range("reembedded", "Documents in the new space (%)", 0, 100, 10, 50),
        _toggle("cutover", "Queries use the new model", False),
    ], "data": {"base": 0.90, "newBase": 0.93, "chance": 0.05}}

_topic(
    "embedding_model_migration", "Operations", "Advanced",
    "Embedding Model Migration",
    "How do you move a vector database to a new embedding model without "
    "downtime or broken search?",
    "Blue-green indexing, shadow validation and a staged cutover move a "
    "vector database to a new embedding model without mixing embedding "
    "spaces or taking search offline.",
    "Vectors from different embedding models cannot be compared, even at the "
    "same dimension. <strong>So a migration builds a complete new index "
    "beside the old one, validates it in shadow mode, and moves traffic "
    "across through a router that can flip back.</strong> Mixing spaces in "
    "one index fails quietly.",
    "\"I never mix embedding spaces. I build a green index with the new "
    "model, run shadow mode and score both on labelled queries, cut over in "
    "stages by hashing a stable ID, keep blue for rollback, and dual-write "
    "new documents during the window.\"",
    ["In place, a half-migrated index loses recall whichever model queries it.",
     "Blue-green keeps the old level until the cutover.",
     "Cutting over before the green index is full loses documents."],
    "Never mix embedding spaces. Build a green index, validate in shadow "
    "mode, cut over in stages, keep blue for rollback, and dual-write new "
    "documents during the migration.")


# --------------------------------------------------------------------------
# Query decomposition
# --------------------------------------------------------------------------

WIDGETS["query_decomposition"] = {
    "model": "plan", "ops": True, "controls": [
        _select("mode", "Mode", [("single pass", "single"),
                                 ("decomposed", "decomposed")], 1),
        _range("workers", "Workers", 1, 4, 1, 1),
    ], "data": {
        "classifyMs": 200, "planMs": 800, "synthMs": 1000, "singleMs": 1200,
        "questions": [
            {"text": "How does service A handle retries?", "ms": 700, "needs": []},
            {"text": "How does service B handle retries?", "ms": 700, "needs": []},
            {"text": "Which service caused Tuesday's outage?", "ms": 700, "needs": []},
            {"text": "Which team owns that service?", "ms": 700, "needs": [2]}]}}

_topic(
    "query_decomposition", "Retrieval", "Advanced",
    "Query Decomposition",
    "How do you answer a question that needs facts from several places when "
    "one retrieval pass cannot reach them all?",
    "Break complex questions into sub-questions with a dependency graph, run "
    "the independent ones in parallel, merge the answers, and know when not "
    "to decompose.",
    "Single-pass retrieval misses questions that need several sources. "
    "<strong>Query decomposition splits them into sub-questions, runs the "
    "independent ones side by side, and merges the answers.</strong> It "
    "costs latency and model calls, so a classifier keeps simple questions "
    "on the fast path.",
    "\"I classify first and decompose only comparisons, multi-hop chains, "
    "aggregations and conditions. The plan is a dependency graph that I "
    "validate for cycles, independent parts run in parallel, and I cap the "
    "depth and merge by question type.\"",
    ["Workers speed up the independent sub-questions.",
     "The owner lookup waits for the outage lookup however many workers "
     "you add.",
     "Single pass is quick and answers only part of a compound question."],
    "Decompose only questions that need it, write the plan as a dependency "
    "graph, reject cycles, run independent parts together and cap the "
    "depth.")


# --------------------------------------------------------------------------
# RAG capacity planning
# --------------------------------------------------------------------------

WIDGETS["rag_capacity_planning"] = {
    "model": "capacity", "ops": True, "controls": [
        _range("articles", "Articles (thousands)", 10, 3000, 10, 200),
        _range("length", "Article length (tokens)", 300, 4000, 100, 1200),
        _range("chunk", "Chunk size (tokens)", 100, 1000, 10, 500),
        _range("overlap", "Overlap (%)", 0, 30, 5, 10),
        _select("dims", "Dimensions", [("384", 384), ("768", 768), ("1536", 1536),
                                       ("3072", 3072)], 1),
        _select("precision", "Precision", [("float32", "float32"), ("float16", "float16"),
                                           ("int8", "int8"), ("binary", "binary")], 0),
        _select("index", "Index", [("none (flat)", "flat"), ("HNSW, M=16", "hnsw"),
                                   ("IVF", "ivf")], 1),
    ], "data": {"ramBudget": 16}}

_topic(
    "rag_capacity_planning", "Operations", "Intermediate",
    "RAG Capacity Planning",
    "How many chunks, gigabytes and how much RAM will a RAG corpus need?",
    "Estimate chunks, vector storage, index overhead and RAM for a RAG "
    "corpus from first principles, and see how quantization, dimension and "
    "overlap move the total.",
    "Capacity planning for RAG is arithmetic: <strong>count the chunks, "
    "multiply by bytes per vector, add text, metadata, the index and "
    "overhead, and compare with the RAM you have.</strong> The raw vectors "
    "turn out to be only about half of the total.",
    "\"I count chunks from a sample of real article lengths, price the "
    "vectors at dimensions times bytes, add text, metadata, the index and "
    "overhead, keep vectors and index in RAM with headroom, quantize to "
    "shrink, and plan for growth.\"",
    ["Switching to float16 halves the embedding bar and the RAM figure.",
     "More overlap means more chunks and a larger total.",
     "At 3072 dimensions the vectors dominate everything else."],
    "Count chunks from real lengths, price the vectors, add text, metadata, "
    "the index and overhead, size RAM with headroom, quantize to shrink and "
    "plan for growth.")


# --------------------------------------------------------------------------
# RAG latency optimization
# --------------------------------------------------------------------------

WIDGETS["rag_latency_optimization"] = {
    "model": "latency", "ops": True, "controls": [
        _select("model", "Model size", [("large", "large"), ("medium", "medium"),
                                        ("small", "small")], 0),
        _toggle("rerank", "Reranker", True),
        _toggle("parallel", "Run searches in parallel", False),
        _range("cacheHit", "Cache hit rate (%)", 0, 60, 5, 0),
    ], "data": {"cacheMs": 8, "stages": [
        ["embed", 100, 160], ["vector", 150, 300], ["keyword", 120, 220],
        ["rerank", 400, 700], ["generate", 2000, 3200]]}}

_topic(
    "rag_latency_optimization", "Operations", "Intermediate",
    "RAG Latency Optimization",
    "A RAG request takes four seconds at p95. How do you find what is slow "
    "and fix it?",
    "Trace each stage of a RAG request, read the latency distribution, and "
    "cut time with streaming, caching, parallel stages and timeouts, "
    "checking what each fix does to the tail.",
    "A slow RAG request is rarely slow everywhere. <strong>Time every "
    "stage, read the distribution, and fix the stage with the biggest share "
    "of the mean.</strong> Percentiles do not add up, and a fix that helps "
    "the average can leave the tail unchanged.",
    "\"I trace every stage and fix the one with the biggest share of the "
    "mean, usually generation. I stream, cap output, cache whole answers, "
    "run independent stages in parallel and put a timeout and a fallback on "
    "each stage. I check what each fix does to the p95.\"",
    ["A smaller model shrinks the generation bar the most.",
     "Running the keyword search in parallel hides it behind the vector path.",
     "A cache lowers the average and leaves the miss path as slow as before."],
    "Measure every stage, fix the biggest share of the mean, stream, cap "
    "output, cache, parallelise and time out each stage, and check what each "
    "fix does to the tail.")


# --------------------------------------------------------------------------
# Production RAG system design
# --------------------------------------------------------------------------

WIDGETS["production_rag_system_design"] = {
    "model": "subsystems", "ops": True, "controls": [
        _select("fail", "What fails", [("nothing", -1), ("ingestion pipeline", 0),
                                       ("vector store", 1), ("keyword search", 2),
                                       ("reranker", 3), ("language model API", 4),
                                       ("cache", 5)], 2),
        _toggle("guard", "Safeguards", False),
    ], "data": {
        "healthy": "Every subsystem is up and answers come from the full pipeline.",
        "systems": [
            {"name": "Ingestion pipeline", "role": "keeps the index fresh",
             "rawServed": True, "rawQuality": 90,
             "rawNote": "Search still works, but new and edited articles are not indexed, so the index goes stale.",
             "guard": "a queue buffers updates", "guardServed": True, "guardQuality": 100,
             "guardNote": "The queue holds the updates and replays them when the pipeline recovers. Users notice nothing."},
            {"name": "Vector store", "role": "semantic search",
             "rawServed": False, "rawQuality": 0,
             "rawNote": "Without a vector store there is no retrieval, so the service has nothing to answer from.",
             "guard": "keyword search and the cache take over", "guardServed": True, "guardQuality": 70,
             "guardNote": "A circuit breaker opens and keyword search plus the cache keep answers flowing at lower quality."},
            {"name": "Keyword search", "role": "exact-term search",
             "rawServed": False, "rawQuality": 0,
             "rawNote": "If fusion waits for both searches, one failing search blocks the whole request.",
             "guard": "vector-only retrieval", "guardServed": True, "guardQuality": 85,
             "guardNote": "The router skips the failed search and fuses a single list. Rare terms are found less often."},
            {"name": "Reranker", "role": "fine relevance scoring",
             "rawServed": False, "rawQuality": 0,
             "rawNote": "Requests wait on a reranker that is not answering, and time out.",
             "guard": "skip it and use retrieval order", "guardServed": True, "guardQuality": 92,
             "guardNote": "Candidates go to the model in retrieval order. Quality dips a little and the service stays up."},
            {"name": "Language model API", "role": "writes the answer",
             "rawServed": False, "rawQuality": 0,
             "rawNote": "Retrieval works but no answer can be written, so users see errors.",
             "guard": "semantic cache, then curated FAQ", "guardServed": True, "guardQuality": 40,
             "guardNote": "Cached answers and curated FAQ pages cover common questions. Anything new is out of reach."},
            {"name": "Cache", "role": "answers repeats cheaply",
             "rawServed": True, "rawQuality": 100,
             "rawNote": "Every request now runs the full pipeline: answers are the same, but slower and more costly.",
             "guard": "scale out the other services", "guardServed": True, "guardQuality": 100,
             "guardNote": "Autoscaling absorbs the extra load while the cache is rebuilt."}]}}

_topic(
    "production_rag_system_design", "Operations", "Advanced",
    "Production RAG System Design",
    "What does a RAG system need beyond retrieve-and-generate to run in "
    "production?",
    "Seven connected subsystems - ingestion, hybrid retrieval, generation, "
    "evaluation, monitoring, scaling and failure recovery - and what "
    "happens when each one fails with and without safeguards.",
    "A demo fetches chunks and writes an answer. <strong>A production RAG "
    "system adds reliable ingestion, hybrid retrieval, evaluation, "
    "monitoring, scaling and failure recovery.</strong> The test of the "
    "design is what happens to users when one part breaks.",
    "\"Seven subsystems: idempotent ingestion, hybrid retrieval with rank "
    "fusion, routed and streamed generation, offline and online "
    "evaluation, three kinds of monitoring, autoscaling, and circuit "
    "breakers with stepwise fallbacks.\"",
    ["Fail the vector store with safeguards off and nothing is served.",
     "Turn safeguards on and answers keep flowing at lower quality.",
     "Some failures, like ingestion, are invisible until the index goes stale."],
    "A production RAG system has seven parts. Make ingestion idempotent, "
    "fuse vector and keyword search, measure recall and faithfulness, watch "
    "speed, quality and cost, and wrap every dependency in a circuit "
    "breaker with a fallback.")
