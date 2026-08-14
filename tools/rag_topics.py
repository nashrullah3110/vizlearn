# -*- coding: utf-8 -*-
"""The generated RAG and LLM-serving pages in gen_ai/.

Same entry shape as tools/interview.py - see that file for the fields - with
one addition: `group_label`, the tag shown beside the title, because these are
grouped by subject rather than by data structure.

Seven requested topics are deliberately absent because the track already
covers them as hand-written modules: naive RAG (rag.html), parent-child
retrieval (parent_document_retriever.html), hybrid search
(hybrid_search_reciprocal_rank_fusion.html), BM25 (bm25_and_sparse_retrieval.html),
the multi-query retriever (multi_query_retriever.html), the KV cache
(context_window_and_kv_cache.html) and chunking strategies
(chunking_strategies_for_rag.html). Adding a second page on any of them would
split the search results and the internal links for no gain.
"""


TOPICS = []


# --------------------------------------------------------------------------
# The interactive visualisation on each page.
#
# The hand-written modules in this track put a Parameters panel beside a
# visualisation that recomputes as you move a control, and these have to match.
# Each spec names a model in assets/vizlearn-ragviz.js and supplies its
# controls and data; the arithmetic happens in the reader's browser, so the
# numbers on screen are computed rather than baked in here.
# --------------------------------------------------------------------------

WIDGETS = {

"hit_rate_at_k": {"model": "ranking", "controls": [
    {"id": "k", "label": "k (results examined)", "kind": "range",
     "min": 1, "max": 10, "step": 1, "value": 3},
], "data": {"focus": "hit", "results": [
        {"text": "Refund window is 14 days from delivery", "relevant": True},
        {"text": "Returns portal user guide", "relevant": False},
        {"text": "Exchanges are processed within 14 days", "relevant": True},
        {"text": "Shipping rates by region", "relevant": False},
        {"text": "Warranty claims take 30 days", "relevant": False},
        {"text": "Refunds for digital goods: not available", "relevant": True},
        {"text": "Office relocation notice, 2021", "relevant": False},
        {"text": "Payment methods accepted", "relevant": False},
        {"text": "Late refund escalation process", "relevant": True},
        {"text": "Careers page", "relevant": False}]}},

"recall_at_k": {"model": "ranking", "controls": [
    {"id": "k", "label": "k (results examined)", "kind": "range",
     "min": 1, "max": 10, "step": 1, "value": 5},
], "data": {"focus": "recall", "results": [
        {"text": "Refund window is 14 days from delivery", "relevant": True},
        {"text": "Returns portal user guide", "relevant": False},
        {"text": "Exchanges are processed within 14 days", "relevant": True},
        {"text": "Shipping rates by region", "relevant": False},
        {"text": "Warranty claims take 30 days", "relevant": False},
        {"text": "Refunds for digital goods: not available", "relevant": True},
        {"text": "Office relocation notice, 2021", "relevant": False},
        {"text": "Payment methods accepted", "relevant": False},
        {"text": "Late refund escalation process", "relevant": True},
        {"text": "Careers page", "relevant": False}]}},

"precision_at_k": {"model": "ranking", "controls": [
    {"id": "k", "label": "k (results examined)", "kind": "range",
     "min": 1, "max": 10, "step": 1, "value": 5},
], "data": {"focus": "precision", "results": [
        {"text": "Refund window is 14 days from delivery", "relevant": True},
        {"text": "Returns portal user guide", "relevant": False},
        {"text": "Exchanges are processed within 14 days", "relevant": True},
        {"text": "Shipping rates by region", "relevant": False},
        {"text": "Warranty claims take 30 days", "relevant": False},
        {"text": "Refunds for digital goods: not available", "relevant": True},
        {"text": "Office relocation notice, 2021", "relevant": False},
        {"text": "Payment methods accepted", "relevant": False},
        {"text": "Late refund escalation process", "relevant": True},
        {"text": "Careers page", "relevant": False}]}},

"mean_reciprocal_rank": {"model": "ranking", "controls": [
    {"id": "k", "label": "k (results examined)", "kind": "range",
     "min": 1, "max": 10, "step": 1, "value": 10},
], "data": {"focus": "mrr", "results": [
        {"text": "Refund window is 14 days from delivery", "relevant": True},
        {"text": "Returns portal user guide", "relevant": False},
        {"text": "Exchanges are processed within 14 days", "relevant": True},
        {"text": "Shipping rates by region", "relevant": False},
        {"text": "Warranty claims take 30 days", "relevant": False},
        {"text": "Refunds for digital goods: not available", "relevant": True},
        {"text": "Office relocation notice, 2021", "relevant": False},
        {"text": "Payment methods accepted", "relevant": False},
        {"text": "Late refund escalation process", "relevant": True},
        {"text": "Careers page", "relevant": False}]}},

"correctness_in_llm_evaluation": {"model": "judge", "controls": [], "data": {
    "focus": "correctness", "requiredPoints": 4, "claims": [
        {"text": "Refunds are issued within 14 days of delivery.",
         "supported": True, "correct": True, "onTopic": True, "required": True},
        {"text": "The item must be unused and in its original packaging.",
         "supported": True, "correct": True, "onTopic": True, "required": True},
        {"text": "Digital goods are refundable within 30 days.",
         "supported": False, "correct": False, "onTopic": True, "required": False},
        {"text": "Our returns team is available 24/7 by phone.",
         "supported": False, "correct": True, "onTopic": False, "required": False},
        {"text": "Refunds are returned to the original payment method.",
         "supported": True, "correct": True, "onTopic": True, "required": True}]}},

"groundedness_in_llm_evaluation": {"model": "judge", "controls": [], "data": {
    "focus": "groundedness", "requiredPoints": 4, "claims": [
        {"text": "Refunds are issued within 14 days of delivery.",
         "supported": True, "correct": True, "onTopic": True, "required": True},
        {"text": "The item must be unused and in its original packaging.",
         "supported": True, "correct": True, "onTopic": True, "required": True},
        {"text": "Digital goods are refundable within 30 days.",
         "supported": False, "correct": False, "onTopic": True, "required": False},
        {"text": "Our returns team is available 24/7 by phone.",
         "supported": False, "correct": True, "onTopic": False, "required": False},
        {"text": "Refunds are returned to the original payment method.",
         "supported": True, "correct": True, "onTopic": True, "required": True}]}},

"relevance_in_llm_evaluation": {"model": "judge", "controls": [], "data": {
    "focus": "relevance", "requiredPoints": 4, "claims": [
        {"text": "Refunds are issued within 14 days of delivery.",
         "supported": True, "correct": True, "onTopic": True, "required": True},
        {"text": "The item must be unused and in its original packaging.",
         "supported": True, "correct": True, "onTopic": True, "required": True},
        {"text": "Digital goods are refundable within 30 days.",
         "supported": False, "correct": False, "onTopic": True, "required": False},
        {"text": "Our returns team is available 24/7 by phone.",
         "supported": False, "correct": True, "onTopic": False, "required": False},
        {"text": "Refunds are returned to the original payment method.",
         "supported": True, "correct": True, "onTopic": True, "required": True}]}},

"completeness_in_llm_evaluation": {"model": "judge", "controls": [], "data": {
    "focus": "completeness", "requiredPoints": 4, "claims": [
        {"text": "Refunds are issued within 14 days of delivery.",
         "supported": True, "correct": True, "onTopic": True, "required": True},
        {"text": "The item must be unused and in its original packaging.",
         "supported": True, "correct": True, "onTopic": True, "required": True},
        {"text": "Digital goods are refundable within 30 days.",
         "supported": False, "correct": False, "onTopic": True, "required": False},
        {"text": "Our returns team is available 24/7 by phone.",
         "supported": False, "correct": True, "onTopic": False, "required": False},
        {"text": "Refunds are returned to the original payment method.",
         "supported": True, "correct": True, "onTopic": True, "required": True}]}},

"tf_idf": {"model": "tfidf", "controls": [
    {"id": "query", "label": "Query", "kind": "select", "value": 0,
     "options": [{"label": "cat"}, {"label": "the"}, {"label": "the cat"},
                 {"label": "quantum lab"}]},
    {"id": "useIdf", "label": "Weight by idf", "kind": "toggle", "value": 1},
    {"id": "dampTf", "label": "Damp term frequency", "kind": "toggle", "value": 1},
], "data": {
    "queries": ["cat", "the", "the cat", "quantum lab"],
    "docs": [{"text": "the cat sat on the mat"},
             {"text": "the dog sat on the log"},
             {"text": "the cat chased the cat"},
             {"text": "quantum entanglement in the lab"}],
}},

"corrective_rag": {"model": "crag", "controls": [
    {"id": "query", "label": "Query", "kind": "select", "value": 0,
     "options": [{"label": "who wrote the 2019 memo"},
                 {"label": "what was 2019 revenue"},
                 {"label": "capital of Peru"}]},
    {"id": "good", "label": "Relevance threshold", "kind": "range",
     "min": 0.1, "max": 0.9, "step": 0.05, "value": 0.45},
    {"id": "poor", "label": "Ambiguous floor", "kind": "range",
     "min": 0.05, "max": 0.5, "step": 0.05, "value": 0.2},
], "data": {"queries": [
    {"results": [{"text": "2019 security policy, authored by Priya Nair", "score": 0.72},
                 {"text": "2019 revenue grew eleven percent", "score": 0.31},
                 {"text": "office relocated to Bristol in 2021", "score": 0.12}]},
    {"results": [{"text": "2019 revenue grew eleven percent", "score": 0.68},
                 {"text": "2019 security policy, authored by Priya Nair", "score": 0.35},
                 {"text": "office relocated to Bristol in 2021", "score": 0.10}]},
    {"results": [{"text": "office relocated to Bristol in 2021", "score": 0.14},
                 {"text": "2019 revenue grew eleven percent", "score": 0.11},
                 {"text": "2019 security policy, authored by Priya Nair", "score": 0.09}]},
]}},

"queries_keys_and_values": {"model": "attention", "controls": [
    {"id": "focus", "label": "Attending from", "kind": "select", "value": 2,
     "options": [{"label": "the"}, {"label": "cat"}, {"label": "sat"}, {"label": "mat"}]},
    {"id": "sharpness", "label": "Score scale (1/sqrt(d))", "kind": "range",
     "min": 0.5, "max": 4, "step": 0.25, "value": 1},
], "data": {
    "tokens": ["the", "cat", "sat", "mat"],
    "affinity": {"the": {"the": 2.0, "cat": 1.2, "sat": 0.6, "mat": 1.0},
                 "cat": {"the": 1.1, "cat": 2.0, "sat": 1.6, "mat": 1.3},
                 "sat": {"the": 0.5, "cat": 2.4, "sat": 1.0, "mat": 1.7},
                 "mat": {"the": 1.0, "cat": 1.4, "sat": 1.5, "mat": 2.0}},
}},

"caching_in_rag_pipelines": {"model": "caching", "controls": [
    {"id": "repeatRate", "label": "Exact repeats (%)", "kind": "range",
     "min": 0, "max": 80, "step": 5, "value": 30},
    {"id": "rewordRate", "label": "Reworded repeats (%)", "kind": "range",
     "min": 0, "max": 60, "step": 5, "value": 30},
    {"id": "promptCache", "label": "Prompt caching", "kind": "toggle", "value": 1},
], "data": {"stages": [["embed", 18], ["retrieve", 120], ["rerank", 210],
                        ["generate", 2100]]}},

"recursive_chunking": {"model": "chunking", "controls": [
    {"id": "size", "label": "Chunk size (chars)", "kind": "range",
     "min": 40, "max": 260, "step": 10, "value": 120},
    {"id": "strategy", "label": "Separators", "kind": "select", "value": 0,
     "options": [{"label": "recursive"}, {"label": "sentence only"},
                 {"label": "fixed size"}]},
], "data": {"text": "Refunds are issued within 14 days of purchase. The item "
                    "must be unused and in its original packaging.\n\nShipping "
                    "costs are not refunded. Digital goods are non-refundable "
                    "once downloaded."}},

"semantic_chunking": {"model": "semantic", "controls": [
    {"id": "percentile", "label": "Split percentile", "kind": "range",
     "min": 10, "max": 80, "step": 5, "value": 25},
], "data": {"sentences": 6, "gaps": [0.81, 0.78, 0.24, 0.85, 0.31]}},

"structure_aware_chunking": {"model": "chunking", "controls": [
    {"id": "size", "label": "Chunk size (chars)", "kind": "range",
     "min": 40, "max": 260, "step": 10, "value": 110},
    {"id": "strategy", "label": "Separators", "kind": "select", "value": 0,
     "options": [{"label": "structure first"}, {"label": "sentence only"},
                 {"label": "fixed size"}]},
], "data": {"text": "# Refund policy\n\nRefunds are issued within 14 days.\n\n"
                    "## Exceptions\n\nDigital goods are non-refundable once "
                    "downloaded."}},

"context_aware_chunking": {"model": "enrichment", "controls": [
    {"id": "title", "label": "Prepend document title", "kind": "toggle", "value": 0},
    {"id": "path", "label": "Prepend heading path", "kind": "toggle", "value": 0},
    {"id": "resolve", "label": "Resolve pronouns", "kind": "toggle", "value": 0},
    {"id": "boilerplate", "label": "Over-enrich", "kind": "toggle", "value": 0},
], "data": {
    "chunk": ["it", "must", "be", "requested", "within", "14", "days", "of", "it"],
    "resolved": ["a", "refund", "must", "be", "requested", "within", "14", "days",
                 "of", "purchase"],
    "title": ["customer", "returns", "handbook"],
    "path": ["refund", "policy", "time", "limits"],
    "queryTerms": ["how", "long", "to", "return", "an", "item", "for", "a", "refund"],
    "sibling": ["digital", "goods", "are", "non", "refundable", "once", "downloaded"],
    "boilerplate": ["customer", "returns", "handbook", "refunds", "exchanges",
                    "shipping", "warranty", "regions"],
}},

"indexing_in_vector_databases": {"model": "ivf", "controls": [
    {"id": "clusters", "label": "Clusters", "kind": "range",
     "min": 8, "max": 256, "step": 8, "value": 64},
    {"id": "probe", "label": "Clusters probed", "kind": "range",
     "min": 1, "max": 64, "step": 1, "value": 4},
], "data": {"corpus": 1000000}},

"ann_indexing_hnsw_and_ivf": {"model": "hnsw", "controls": [
    {"id": "ef", "label": "efSearch (query time)", "kind": "range",
     "min": 8, "max": 512, "step": 8, "value": 128},
    {"id": "M", "label": "M, edges per node (build time)", "kind": "range",
     "min": 4, "max": 48, "step": 2, "value": 16},
], "data": {"corpus": 1000000}},

"permission_filtering_in_rag": {"model": "permissions", "controls": [
    {"id": "visible", "label": "Corpus visible to this user (%)", "kind": "range",
     "min": 1, "max": 100, "step": 1, "value": 20},
    {"id": "k", "label": "Results requested (k)", "kind": "range",
     "min": 5, "max": 30, "step": 1, "value": 10},
    {"id": "fetch", "label": "Over-fetch before filtering", "kind": "range",
     "min": 10, "max": 500, "step": 10, "value": 100},
], "data": {}},

"distributed_retrieval_and_sharding": {"model": "sharding", "controls": [
    {"id": "shards", "label": "Shards", "kind": "range",
     "min": 1, "max": 40, "step": 1, "value": 4},
    {"id": "perShard", "label": "Per-shard k", "kind": "range",
     "min": 2, "max": 60, "step": 2, "value": 10},
    {"id": "strategy", "label": "Sharding strategy", "kind": "select", "value": 0,
     "options": [{"label": "random"}, {"label": "semantic"}]},
], "data": {}},

}

# The select controls arrive as an index; the models want the value.
for _spec in WIDGETS.values():
    for _c in _spec["controls"]:
        if _c["kind"] == "select":
            _c.setdefault("options", [])



# --------------------------------------------------------------------------
# Card art: one motif per group, varied by index so a grid is scannable.
# The opening tag must stay `<svg aria-hidden="true"` - index.html only
# inlines card art that starts that way, and anything else is wrapped in a
# data-URI <img> where var(--accent-primary) resolves to nothing.
# --------------------------------------------------------------------------

def _art_retrieval(v):
    bars = []
    for i in range(5):
        h = 10 + ((i * 9 + v * 6) % 26)
        bars.append('<rect x="%d" y="%d" width="14" height="%d" rx="2" '
                    'fill="var(--accent-primary)" opacity="%.2f"/>'
                    % (28 + i * 22, 60 - h, h, 0.3 + 0.13 * ((i + v) % 5)))
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">'
            '<circle cx="18" cy="45" r="7" fill="none" stroke="var(--accent-primary)" '
            'stroke-width="2"/><line x1="23" y1="50" x2="28" y2="56" '
            'stroke="var(--accent-primary)" stroke-width="2"/>%s</svg>' % "".join(bars))


def _art_chunking(v):
    blocks = []
    y = 20
    for i in range(4):
        h = 8 + ((i + v) % 3) * 5
        blocks.append('<rect x="30" y="%d" width="100" height="%d" rx="3" '
                      'fill="var(--accent-primary)" opacity="%.2f"/>'
                      % (y, h, 0.25 + 0.18 * ((i + v) % 4)))
        y += h + 4
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">'
            '%s</svg>' % "".join(blocks))


def _art_cache(v):
    cells = []
    for i in range(6):
        hit = (i + v) % 3 != 1
        cells.append('<rect x="%d" y="34" width="16" height="22" rx="3" fill="%s" '
                     'stroke="var(--accent-primary)" stroke-width="2" opacity="%s"/>'
                     % (22 + i * 21,
                        "var(--accent-primary)" if hit else "var(--input-bg)",
                        "0.8" if hit else "1"))
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s'
            '<text x="80" y="74" text-anchor="middle" font-size="8" '
            'font-family="monospace" fill="var(--text-muted)">hit / miss</text>'
            '</svg>' % "".join(cells))


def _art_scale(v):
    nodes = []
    for i in range(3):
        on = (i + v) % 3 == 0
        nodes.append('<rect x="%d" y="46" width="30" height="22" rx="4" fill="%s" '
                     'stroke="var(--accent-primary)" stroke-width="2" opacity="%s"/>'
                     % (24 + i * 44, "var(--accent-primary)" if on else "var(--input-bg)",
                        "0.75" if on else "1"))
        nodes.append('<line x1="80" y1="34" x2="%d" y2="46" '
                     'stroke="var(--border-subtle)" stroke-width="2"/>' % (39 + i * 44))
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">'
            '<rect x="62" y="16" width="36" height="18" rx="4" fill="var(--input-bg)" '
            'stroke="var(--text-muted)" stroke-width="2"/>%s</svg>' % "".join(nodes))


def _art_eval(v):
    bars = []
    for i in range(6):
        hit = (i + v) % 4 != 2
        bars.append('<rect x="%d" y="%d" width="15" height="%d" rx="2" fill="%s" '
                    'opacity="%s"/>'
                    % (22 + i * 21, 30 if hit else 44, 26 if hit else 12,
                       "var(--accent-primary)" if hit else "var(--text-muted)",
                       "0.85" if hit else "0.35"))
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s'
            '<line x1="14" y1="62" x2="146" y2="62" stroke="var(--border-subtle)" '
            'stroke-width="2"/>'
            '<text x="80" y="76" text-anchor="middle" font-size="8" '
            'font-family="monospace" fill="var(--text-muted)">@k</text></svg>'
            % "".join(bars))


def _art_judge(v):
    rows = []
    for i in range(4):
        ok = (i + v) % 4 != 1
        rows.append('<rect x="40" y="%d" width="80" height="10" rx="2" '
                    'fill="var(--accent-primary)" opacity="%s"/>'
                    % (22 + i * 15, "0.8" if ok else "0.2"))
        rows.append('<circle cx="28" cy="%d" r="4" fill="%s"/>'
                    % (27 + i * 15,
                       "var(--accent-primary)" if ok else "var(--text-muted)"))
    return ('<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">'
            '%s</svg>' % "".join(rows))


ART = {"Retrieval": _art_retrieval, "Chunking": _art_chunking,
       "Caching": _art_cache, "Scale": _art_scale,
       "Evaluation": _art_eval, "LLM evaluation": _art_judge}


def _t(**kw):
    """Register a topic. The card art is assigned here rather than in a pass
    at the end, because a pass at the end silently misses anything defined
    below it."""
    kw.setdefault("kind", None)
    kw["svg"] = ART[kw["group_label"]](len(TOPICS))
    TOPICS.append(kw)



# =========================================================================
# Retrieval scoring
# =========================================================================



_t(
    slug="tf_idf",
    group_label="Retrieval",
    level="Beginner",
    title="TF-IDF",
    asked="How does TF-IDF decide which words in a document actually matter?",
    desc="TF-IDF weights a term by how often it appears in a document against "
         "how rare it is across the corpus - the scoring behind classical "
         "search and the foundation BM25 improves on.",
    lead="Two numbers multiplied. <strong>Term frequency</strong> rewards a word "
         "for appearing often in <em>this</em> document; <strong>inverse "
         "document frequency</strong> punishes it for appearing in "
         "<em>every</em> document. The product is high only for words that are "
         "frequent here and rare elsewhere &mdash; which is a workable "
         "definition of \"what this document is about\".",
    say="\"Term frequency times inverse document frequency. TF says the word "
        "matters here, IDF says it distinguishes this document from the rest. "
        "Stopwords get an IDF near zero and cancel out without a stopword "
        "list.\"",
    notice=[
        "A term in every document scores zero &mdash; the log sees to that.",
        "One occurrence of a rare word beats two of a common one.",
        "No stopword list is needed; the maths removes them.",
    ],
    viz=WIDGETS["tf_idf"],
    sections=[
        ("The two halves",
         "<p><strong>Term frequency</strong> is how often a term occurs in a "
         "document, usually damped &mdash; a word appearing twenty times is not "
         "twenty times as relevant, so implementations take a logarithm or "
         "normalise by document length.</p>"
         "<p><strong>Inverse document frequency</strong> is "
         "<code>log(N / df)</code>, where <code>df</code> is the number of "
         "documents containing the term. When a term is in every document that "
         "ratio is 1 and the log is 0, so the term contributes nothing at "
         "all.</p>"
         "<p>That zero is the elegant part: stopwords are removed by the "
         "arithmetic rather than by a list you have to maintain per "
         "language.</p>"),
        ("Where it falls short",
         "<p><strong>No length normalisation by default.</strong> A long "
         "document contains more of everything, so raw TF favours it. Dividing "
         "by length overcorrects and favours very short ones. BM25's "
         "<code>b</code> parameter exists to tune between the two.</p>"
         "<p><strong>Unbounded term frequency.</strong> TF keeps growing with "
         "repetition. BM25 saturates it, so the tenth occurrence adds far less "
         "than the second &mdash; which matches how relevance actually "
         "behaves.</p>"
         "<p><strong>No understanding of meaning.</strong> \"car\" and "
         "\"automobile\" are unrelated terms. That is what dense embeddings "
         "fix, and why modern retrieval runs both and fuses the results &mdash; "
         "see <a href=\"hybrid_search_reciprocal_rank_fusion.html\">hybrid "
         "search</a>.</p>"),
        ("Why it still matters in a RAG system",
         "<p>Exact terms still win on identifiers, error codes, product names "
         "and rare jargon &mdash; precisely the queries where an embedding model "
         "has seen too little to place the token meaningfully. A vector-only "
         "pipeline reliably fails on \"error TS2345\".</p>"
         "<p>TF-IDF is also the honest baseline. If a dense retriever cannot "
         "beat it on your evaluation set, the problem is the embedding model or "
         "the chunking, not the ranking.</p>"),
    
        ("Things to try",
         "<ol><li>Turn <strong>idf</strong> off and query <em>the</em>. Every document scores, and the ranking is driven by a word that distinguishes nothing.</li><li>Query <em>the cat</em> with idf on. Only <em>cat</em> contributes &mdash; the stopword cancels itself without a stopword list.</li><li>Turn <strong>tf damping</strong> off and watch the document that repeats a term run away with the score. That runaway is what BM25's saturation fixes.</li></ol>"),
        ("What to remember",
         "<p>TF-IDF weights a term by how often it appears here times how rare it is everywhere. A term in every document has an idf of zero and drops out by arithmetic rather than by a list. It knows nothing about meaning, which is why a synonym scores zero and why dense retrieval runs alongside it.</p>"),
    ],
)




_t(
    slug="corrective_rag",
    group_label="Retrieval",
    level="Intermediate",
    title="Corrective RAG (CRAG)",
    asked="What is Corrective RAG, and how does it stop a model answering from "
          "irrelevant documents?",
    desc="Corrective RAG grades retrieved documents before generation and takes "
         "a different path - rewrite, fall back, or abstain - when the evidence "
         "is poor.",
    lead="Naive RAG retrieves, then generates, whatever came back. Retrieval "
         "always returns <em>something</em>, so a query with no good match still "
         "produces a confident answer built on irrelevant text. Corrective RAG "
         "adds a <strong>grader between the two steps</strong>: judge the "
         "evidence first, and when it is poor, rewrite the query, fall back to "
         "another source, or decline to answer.",
    say="\"CRAG grades the retrieved documents before generating. If they're "
        "irrelevant it rewrites the query or falls back to another source rather "
        "than answering from bad evidence - and abstaining is an allowed "
        "outcome, which naive RAG has no way to express.\"",
    notice=[
        "Retrieval never fails loudly &mdash; it returns the nearest thing it has.",
        "The grader runs <em>before</em> generation, which is the whole design.",
        "\"I don't know\" is one of the paths, not a failure of the system.",
    ],
    viz=WIDGETS["corrective_rag"],
    sections=[
        ("The failure it fixes",
         "<p>A vector search returns the k nearest chunks whether or not any of "
         "them is relevant. There is no null result: ask about something absent "
         "from the corpus and you still get five chunks, at low similarity, and "
         "the generator dutifully writes an answer from them.</p>"
         "<p>That is the most damaging RAG failure in production, because the "
         "answer is fluent, sourced-looking and wrong. The user has no signal "
         "that the retrieval missed.</p>"),
        ("The three verdicts",
         "<p>A grader &mdash; a small model, a cross-encoder, or a similarity "
         "threshold &mdash; labels the retrieved set:</p>"
         "<p><strong>Correct.</strong> At least one document is relevant. "
         "Proceed, often after stripping the irrelevant ones so they do not "
         "distract the generator.</p>"
         "<p><strong>Incorrect.</strong> Nothing is relevant. Discard "
         "everything and take a corrective action rather than generating.</p>"
         "<p><strong>Ambiguous.</strong> Something is partly relevant. Combine "
         "what you have with an external source.</p>"),
        ("What correction actually means",
         "<p><strong>Query rewriting</strong> is the cheapest: the user's "
         "phrasing may simply not match the corpus vocabulary. See "
         "<a href=\"query_rewriting_and_hyde.html\">query rewriting and "
         "HyDE</a>.</p>"
         "<p><strong>Fallback to another source</strong> &mdash; web search, a "
         "second index, a keyword search when the dense one missed.</p>"
         "<p><strong>Abstain.</strong> The one people leave out, and often the "
         "correct behaviour. A system that answers \"that is not in the "
         "documents I have\" is more useful than one that invents a citation.</p>"
         "<p>The cost is latency and tokens: every query pays for grading, and "
         "corrected queries pay for a second retrieval. Grade cheaply, and "
         "consider skipping it when the top similarity is already "
         "unambiguous.</p>"),
    
        ("Things to try",
         "<ol><li>Select <em>capital of Peru</em>. Nothing clears the threshold, and the pipeline declines &mdash; the answer naive RAG cannot give.</li><li>Raise the <strong>relevance threshold</strong> to 0.8 on a query that was working. More queries take the corrective path; grading is a precision/recall trade like any other classifier.</li><li>Lower the <strong>ambiguous floor</strong> to 0.05. Weak evidence is now treated as partial rather than absent, which changes which path a borderline query takes.</li></ol>"),
        ("What to remember",
         "<p>Corrective RAG grades retrieved documents before generating, and takes a different path when they are poor: rewrite the query, fall back to another source, or decline. Retrieval never fails loudly &mdash; it always returns its nearest k &mdash; so without a grader a query with no answer still produces a confident, sourced-looking one.</p>"),
    ],
)


# --------------------------------------------------------------------------



# =========================================================================
# Caching
# =========================================================================



_t(
    slug="queries_keys_and_values",
    group_label="Caching",
    level="Intermediate",
    title="What are Queries, Keys and Values in an LLM?",
    asked="What do Q, K and V actually mean in attention, and why are they three "
          "separate things?",
    desc="Queries, keys and values as three learned projections of the same "
         "token: what each one asks and answers, and why K and V being fixed is "
         "what makes the KV cache possible.",
    lead="Three learned projections of the same token embedding. The "
         "<strong>query</strong> is what this token is looking for; the "
         "<strong>key</strong> is what it advertises to others; the "
         "<strong>value</strong> is what it hands over when attended to. Scores "
         "come from query&nbsp;&middot;&nbsp;key; the output is a weighted sum "
         "of <em>values</em>.",
    say="\"Three projections of the same embedding. Q is what I'm looking for, K "
        "is what I advertise, V is what I contribute. Q dot K gives the scores, "
        "softmax turns them into weights, and the output is a weighted sum of the "
        "V vectors. K and V don't change once computed, which is exactly why the "
        "KV cache works.\"",
    notice=[
        "All three come from one embedding through three different matrices.",
        "The score uses K; the output uses V &mdash; they are deliberately separate.",
        "K and V for a past token are fixed forever, which is the cache's premise.",
    ],
    viz=WIDGETS["queries_keys_and_values"],
    sections=[
        ("Why three and not one",
         "<p>If a token used the same vector to search with and to be found by, "
         "attention would collapse into plain similarity: tokens would attend to "
         "tokens like themselves. Separating query from key lets a token look "
         "for something <em>different</em> from itself &mdash; a verb seeking "
         "its subject, a pronoun seeking its referent.</p>"
         "<p>Separating value from key matters just as much. What makes a token "
         "worth attending to is not necessarily what it should contribute once "
         "attended to. The key is the address; the value is the payload.</p>"),
        ("The mechanism in one line",
         "<p><code>softmax(QK<sup>T</sup> / &radic;d) V</code>. The dot products "
         "score every query against every key; the division keeps the softmax "
         "out of its saturated region, where gradients vanish; softmax turns "
         "scores into weights summing to one; and those weights are applied to "
         "the values.</p>"
         "<p>In self-attention all three come from the same sequence. In "
         "cross-attention the queries come from one sequence and the keys and "
         "values from another &mdash; which is how a decoder reads an encoder, "
         "and the same shape as retrieval: a query against a set of keys.</p>"),
        ("Why this is a serving question too",
         "<p>Generating token <em>n</em> needs the keys and values of all "
         "previous tokens &mdash; and those never change, because each depends "
         "only on tokens before it. So they are computed once and kept: the "
         "<a href=\"context_window_and_kv_cache.html\">KV cache</a>.</p>"
         "<p>Without it every new token would recompute K and V for the whole "
         "prefix, making generation quadratic. With it, each step is linear in "
         "the context length. The cost is memory: the cache grows with sequence "
         "length &times; layers &times; heads, and it is usually what limits how "
         "many requests a GPU can serve at once.</p>"),
    
        ("Things to try",
         "<ol><li>Attend from <em>sat</em>. It puts most of its weight on <em>cat</em>, its subject &mdash; which a token searching with its own embedding could never do.</li><li>Raise the <strong>score scale</strong> to 4. The softmax collapses to nearly one-hot; that saturation is what dividing by &radic;d exists to prevent.</li><li>Switch the focus token and watch the whole distribution move. Each token's query is asking a different question of the same keys.</li></ol>"),
        ("What to remember",
         "<p>Q, K and V are three learned projections of one embedding. The query is what a token looks for, the key is what it advertises, the value is what it contributes. Scores come from Q&middot;K and the output is a weighted sum of V. Because K and V for a token never change once computed, they can be cached &mdash; which is what makes generation linear rather than quadratic.</p>"),
    ],
)




_t(
    slug="caching_in_rag_pipelines",
    group_label="Caching",
    level="Intermediate",
    title="Query, embedding and prompt caching",
    asked="What are the different caches in a RAG system, and what does each one "
          "actually save?",
    desc="Three distinct caches in a RAG pipeline - query, embedding and prompt - "
         "what each is keyed on, what it saves, and the invalidation problem "
         "each one creates.",
    lead="Three different caches with the same name. A <strong>query "
         "cache</strong> stores the finished answer, keyed on the question. An "
         "<strong>embedding cache</strong> stores a vector, keyed on the text. A "
         "<strong>prompt cache</strong> stores the model's internal KV state for "
         "a shared prefix. They save different things and go stale in different "
         "ways.",
    say="\"Three layers. Query cache keyed on the question, saves the whole "
        "pipeline. Embedding cache keyed on the text, saves an API call. Prompt "
        "cache lives in the provider and saves recomputing attention over a "
        "shared prefix. The hard part is invalidation - the query cache goes "
        "stale the moment a document changes.\"",
    notice=[
        "Each cache is keyed on something different, so each has a different "
        "hit rate.",
        "An exact repeat hits the query cache and skips everything.",
        "A reworded question misses both exact caches and can still hit the "
        "prompt cache.",
    ],
    viz=WIDGETS["caching_in_rag_pipelines"],
    sections=[
        ("Embedding cache: the easy one",
         "<p>Keyed on a hash of the text and the model name. Embedding is "
         "deterministic, so the same text always gives the same vector &mdash; "
         "which makes this cache both trivially correct and permanently valid, "
         "until you change models.</p>"
         "<p>Include the model identifier in the key. Vectors from different "
         "models are not comparable, and a cache that silently mixes them "
         "produces retrieval results that look plausible and are meaningless. "
         "The biggest win is at indexing time: re-indexing a corpus after a "
         "chunking tweak re-embeds only the chunks that actually changed.</p>"),
        ("Query cache: the highest saving, and the highest risk",
         "<p>Keyed on the question, storing the final answer. A hit skips "
         "retrieval, reranking and generation &mdash; often seconds and most of "
         "the cost. Real traffic is heavily repetitive, so hit rates can be "
         "high.</p>"
         "<p>Two problems. <strong>Staleness:</strong> the answer was correct "
         "for the corpus as it was, so any document update can invalidate it, "
         "and there is no cheap way to know which entries. Most systems use a "
         "short TTL and flush on re-index. <strong>Exact matching:</strong> "
         "\"what is the refund policy\" and \"how do refunds work\" are one "
         "question and two keys. Semantic caching &mdash; keying on the "
         "embedding and accepting a near match &mdash; raises the hit rate and "
         "introduces the risk of returning the answer to a subtly different "
         "question.</p>"),
        ("Prompt caching: inside the model",
         "<p>Provider-side, and a different mechanism entirely: the model keeps "
         "the attention state (the "
         "<a href=\"context_window_and_kv_cache.html\">KV cache</a>) for a "
         "prefix it has already processed. Send the same long system prompt and "
         "the prefill for that portion is skipped.</p>"
         "<p>It is prefix-based, so it only helps if the shared part comes "
         "<em>first</em>. Put the system prompt and any fixed instructions at "
         "the front and the retrieved chunks and the question after them; "
         "putting the variable part first defeats it entirely. Typical savings "
         "are large on time-to-first-token and on input cost, and nothing about "
         "correctness changes &mdash; the model computes the same thing.</p>"),
    
        ("Things to try",
         "<ol><li>Push <strong>exact repeats</strong> to 70%. The query cache dominates &mdash; and it is the cache that goes stale the moment a document changes.</li><li>Set exact repeats to 0 and reworded to 60%. The exact caches stop helping entirely; only the prompt cache, which keys on the shared prefix, still does.</li><li>Turn <strong>prompt caching</strong> off. Reworded queries lose their only remaining saving, which is why prompt order matters.</li></ol>"),
        ("What to remember",
         "<p>Three different caches share the name. The query cache stores a finished answer keyed on the question and saves the most per hit, at the risk of serving a stale one. The embedding cache stores a vector keyed on the text and is permanently valid until the model changes. Prompt caching lives in the provider and only helps when the shared text comes first in the prompt.</p>"),
    ],
)


# =========================================================================
# Chunking
# =========================================================================

TEXT = ("# Refund policy\n\nRefunds are issued within 14 days of purchase. "
        "The item must be unused.\n\n## Exceptions\n\nDigital goods are "
        "non-refundable once downloaded.")




_t(
    slug="recursive_chunking",
    group_label="Chunking",
    level="Beginner",
    title="Recursive chunking",
    asked="What is recursive character chunking, and why is it the default?",
    desc="Recursive chunking splits on a priority list of separators - "
         "paragraphs, then sentences, then words - falling through only when a "
         "piece is still too large.",
    lead="Split on the <strong>largest natural boundary that fits</strong>. Try "
         "paragraphs; if a piece is still over the limit, split it on sentences; "
         "then on words; then, as a last resort, mid-word. Every fallback loses "
         "a little more meaning, so the recursion only descends when it has to.",
    say="\"Recursive character splitting: an ordered list of separators, "
        "paragraph down to character. It splits on the biggest one that gets "
        "under the size limit, so most chunks break at paragraphs and only "
        "pathological text falls through to a hard cut.\"",
    notice=[
        "Each level is tried only when the level above left something too big.",
        "Fixed-size splitting cuts mid-sentence; this cuts at a boundary.",
        "The separator list is where domain knowledge goes.",
    ],
    viz=WIDGETS["recursive_chunking"],
    sections=[
        ("Why not just split every N characters",
         "<p>Fixed-size splitting is one line and cuts wherever it lands "
         "&mdash; mid-sentence, mid-word, mid-number. The retrieved chunk then "
         "starts halfway through a thought, and the generator has to answer "
         "from a fragment.</p>"
         "<p>Recursive splitting keeps the size limit and spends it on the best "
         "boundary available. Chunks vary in length, which is fine: a chunk is "
         "a unit of meaning, not a unit of storage.</p>"),
        ("The separator list is the whole configuration",
         "<p>The default is roughly <code>[\"\\n\\n\", \"\\n\", \". \", \" \", "
         "\"\"]</code> &mdash; paragraph, line, sentence, word, character. It "
         "descends only when a piece still exceeds the limit, so the last entry "
         "fires only on text with no whitespace at all.</p>"
         "<p>Change the list to match the document type. Code wants "
         "<code>[\"\\nclass \", \"\\ndef \", \"\\n\\n\"]</code>; Markdown wants "
         "heading markers first. That is the cheapest large improvement "
         "available to a RAG pipeline, and it is usually left at the "
         "default.</p>"),
        ("Overlap, and what it costs",
         "<p>Chunks usually overlap by 10&ndash;20% so a sentence spanning a "
         "boundary appears whole in at least one of them. The cost is real: "
         "overlap inflates the index, and duplicated text means near-identical "
         "chunks compete in the results, crowding out genuinely different "
         "ones.</p>"
         "<p>Recursive chunking is the right default and it is still "
         "structure-blind &mdash; it does not know a heading from a sentence. "
         "That is what the structure-aware and semantic variants address.</p>"),
    
        ("Things to try",
         "<ol><li>Drop the <strong>chunk size</strong> to 60. More pieces fall through to sentence and then word level, and chunks start ending mid-sentence.</li><li>Switch <strong>separators</strong> to <em>fixed size</em>. Every boundary lands wherever the character count ran out &mdash; watch the mid-sentence count climb.</li><li>Raise the size to 260 with recursive separators. One chunk holds the whole passage, which retrieves as a single coarse unit.</li></ol>"),
        ("What to remember",
         "<p>Recursive chunking splits on the largest natural boundary that fits, descending through a priority list of separators only when a piece is still oversized. The separator list is the whole configuration, and tailoring it to the document type is the cheapest large improvement available to a RAG pipeline.</p>"),
    ],
)


_t(
    slug="semantic_chunking",
    group_label="Chunking",
    level="Intermediate",
    title="Semantic chunking",
    asked="What is semantic chunking, and when is it worth the extra cost?",
    desc="Semantic chunking places boundaries where the meaning changes, by "
         "embedding sentences and cutting where consecutive similarity drops.",
    lead="Put the boundary where the <strong>topic changes</strong>, not where "
         "the character count runs out. Embed each sentence, measure the "
         "similarity between consecutive ones, and cut at the troughs. Chunks "
         "come out semantically coherent and wildly variable in length.",
    say="\"Embed sentence by sentence, look at the similarity between "
        "neighbours, and split where it drops below a threshold - usually a "
        "percentile of the observed distribution rather than a fixed number. It "
        "costs an embedding call per sentence at index time.\"",
    notice=[
        "The boundary lands at the similarity trough, not at a size limit.",
        "Chunk lengths become uneven, which is the point.",
        "The threshold is a percentile of this document, not a global constant.",
    ],
    viz=WIDGETS["semantic_chunking"],
    sections=[
        ("How the boundary is chosen",
         "<p>Split into sentences, embed each one, and compute the similarity "
         "between each consecutive pair. Where the text stays on topic the "
         "similarity is high; where the subject changes it dips. Cut at the "
         "dips.</p>"
         "<p>The threshold should be relative. A fixed number like 0.7 means "
         "something different in every corpus, so implementations use a "
         "percentile of the similarities observed in <em>this</em> document "
         "&mdash; the 5th percentile of gaps, say &mdash; which adapts "
         "automatically to how varied the writing is.</p>"),
        ("What it costs",
         "<p>One embedding call per sentence at index time, against one per "
         "chunk for the alternatives. On a large corpus that is a real bill and "
         "a slow re-index, though it is paid once rather than per query.</p>"
         "<p>It is also brittle on short sentences. \"Yes.\" and \"See "
         "above.\" have unstable embeddings, so a document full of them "
         "produces noisy similarity and boundaries in odd places. Buffering "
         "each sentence with its neighbours before embedding is the usual "
         "mitigation.</p>"),
        ("When to reach for it",
         "<p>Worth it for long unstructured prose &mdash; transcripts, "
         "interviews, reports without headings &mdash; where no formatting "
         "signal exists and a fixed-size split reliably cuts mid-argument.</p>"
         "<p>Not worth it when the document already carries structure. If there "
         "are headings, they are an explicit, author-provided, free topic "
         "boundary, and structure-aware chunking will beat semantic chunking at "
         "a fraction of the cost. Measure before adopting: on a retrieval "
         "evaluation set the gain over a well-tuned recursive splitter is often "
         "small.</p>"),
    
        ("Things to try",
         "<ol><li>Raise the <strong>split percentile</strong> to 70. It splits almost everywhere, producing chunks too small to carry an idea.</li><li>Drop it to 10. Only the single largest topic change survives as a boundary.</li><li>Note that the threshold is derived from this document's own gaps &mdash; a fixed number would behave differently on every corpus.</li></ol>"),
        ("What to remember",
         "<p>Semantic chunking embeds each sentence and cuts where the similarity between neighbours drops, so boundaries land at topic changes rather than at character counts. It costs one embedding per sentence at index time, and it is usually not worth it on documents that already carry headings.</p>"),
    ],
)


_t(
    slug="structure_aware_chunking",
    group_label="Chunking",
    level="Intermediate",
    title="Structure-aware chunking",
    asked="What is structure-aware chunking, and why does it beat a character "
          "splitter on real documents?",
    desc="Structure-aware chunking splits along a document's own markup - "
         "headings, list items, table rows, code blocks - and carries the "
         "heading path into each chunk as metadata.",
    lead="Split along the document's <strong>own structure</strong>. Headings, "
         "list items, table rows and code fences are boundaries the author "
         "already placed, and they are free. The second half matters as much: "
         "carry the heading path into each chunk, so a fragment still knows "
         "which section it came from.",
    say="\"Parse the markup and split on it - headings, list items, table rows - "
        "instead of on character counts. And I'd prepend the heading path to "
        "each chunk, because 'within 14 days' retrieved on its own is useless "
        "without knowing it's under Refunds.\"",
    notice=[
        "The boundaries were written by the author, not inferred.",
        "Each chunk carries its heading path, so it is self-describing.",
        "Splitting a table or a code block mid-way destroys it.",
    ],
    viz=WIDGETS["structure_aware_chunking"],
    sections=[
        ("Boundaries you do not have to guess",
         "<p>A Markdown heading, an HTML <code>&lt;section&gt;</code>, a PDF "
         "outline entry, a slide break: each is a statement by the author that "
         "the subject changes here. Semantic chunking spends an embedding per "
         "sentence to infer what the markup already says.</p>"
         "<p>Some structures must not be split at all. A table split down the "
         "middle loses its header row and becomes unreadable; a code block cut "
         "in half is not code. These are kept whole even when they exceed the "
         "size limit, or summarised separately.</p>"),
        ("Carrying the heading path",
         "<p>The half that gets missed. A chunk reading \"must be requested "
         "within 14 days\" is useless in isolation &mdash; 14 days of what? "
         "Prepending the heading path &mdash; <code>Refund policy &gt; "
         "Exceptions</code> &mdash; makes the chunk self-describing.</p>"
         "<p>It improves retrieval as well as generation, because the heading "
         "words are now in the embedded text and match queries that use the "
         "section's vocabulary. Store the path as metadata too, so it can be "
         "filtered and displayed as a citation.</p>"),
        ("What it needs from you",
         "<p>A parser per format. Markdown is easy, HTML is manageable, PDF is "
         "genuinely hard &mdash; a PDF has no structure, only positioned glyphs, "
         "so headings must be inferred from font size and spacing. Most RAG "
         "quality problems on PDFs are really extraction problems.</p>"
         "<p>Sections also vary wildly in length, so structure-aware chunking is "
         "usually combined with a recursive splitter: split on structure first, "
         "then recursively split any section still over the limit, keeping the "
         "heading path on every resulting piece.</p>"),
    
        ("Things to try",
         "<ol><li>Compare <em>structure first</em> with <em>fixed size</em> at the same chunk size. The character splitter cuts through the heading; the structure-aware one does not.</li><li>Lower the <strong>chunk size</strong> until a section still exceeds it. Structure gives boundaries, not size control, so a recursive splitter has to finish the job.</li><li>Note the heading path on each chunk. A fragment retrieved alone still says which section it belongs to.</li></ol>"),
        ("What to remember",
         "<p>Structure-aware chunking splits along the document's own markup &mdash; headings, list items, table rows &mdash; because those boundaries were placed by the author and cost nothing to find. Carrying the heading path into each chunk is the half people miss: it makes a fragment self-describing and puts the section's vocabulary into the embedded text.</p>"),
    ],
)


_t(
    slug="context_aware_chunking",
    group_label="Chunking",
    level="Advanced",
    title="Context-aware chunking",
    asked="What is context-aware chunking, and what problem does it solve that "
          "the other strategies do not?",
    desc="Context-aware chunking enriches each chunk with the context it lost by "
         "being extracted - document title, section path, a generated summary or "
         "resolved pronouns - so the chunk stands alone.",
    lead="Every chunking strategy answers \"where do I cut?\". This one answers "
         "a different question: <strong>what did this chunk lose by being "
         "cut?</strong> A fragment full of \"it\" and \"the above\" is "
         "unretrievable and unusable, so context is added back &mdash; a title, "
         "a heading path, a generated summary, resolved pronouns.",
    say="\"Context-aware chunking is about enrichment, not boundaries. Each "
        "chunk gets prepended with document title, section path, and often an "
        "LLM-generated sentence explaining what it covers. It fixes the case "
        "where a chunk is meaningless out of context - which is most chunks.\"",
    notice=[
        "The boundary is unchanged; what is <em>stored</em> changes.",
        "Pronouns and back-references are what make a raw chunk unusable.",
        "The enrichment goes into the embedded text, so retrieval improves too.",
    ],
    viz=WIDGETS["context_aware_chunking"],
    sections=[
        ("The problem is coreference, not boundaries",
         "<p>Prose is written to be read in order, so it leans on everything "
         "before it: \"it\", \"this policy\", \"as described above\", \"the "
         "latter\". Cut one paragraph out and those references dangle.</p>"
         "<p>Two consequences. The generator cannot answer from the chunk "
         "because it does not know what \"it\" is. And retrieval never surfaces "
         "the chunk in the first place, because the embedding is of text that "
         "does not contain the words a user would search for.</p>"),
        ("What gets added",
         "<p><strong>Cheap and free:</strong> document title and heading path, "
         "prepended. Deterministic, no model call, and usually the largest "
         "single improvement.</p>"
         "<p><strong>Neighbour context:</strong> the previous and next chunk, "
         "or a window around the chunk, stored for generation but not embedded "
         "&mdash; the "
         "<a href=\"parent_document_retriever.html\">parent document "
         "retriever</a> is exactly this idea, retrieving small and returning "
         "large.</p>"
         "<p><strong>Generated context:</strong> an LLM writes a sentence "
         "situating the chunk in the document, prepended before embedding. "
         "Anthropic's \"contextual retrieval\" is this, and it works well. It "
         "costs one model call per chunk at index time, which prompt caching "
         "over the shared document makes affordable.</p>"),
        ("What it costs, and what to watch",
         "<p>Index time and money, both once. The subtler cost is dilution: "
         "prepending 200 tokens of context to a 300-token chunk means the "
         "embedding is largely <em>about the context</em>, so chunks from the "
         "same section start looking alike and the retriever loses its ability "
         "to distinguish them.</p>"
         "<p>Keep the enrichment short relative to the chunk, and measure on a "
         "retrieval evaluation set rather than assuming. This is the strategy "
         "with the best evidence behind it and it is not free of "
         "trade-offs.</p>"),
    
        ("Things to try",
         "<ol><li>Start with everything off. The raw chunk is about refunds, never says so, and cannot be retrieved.</li><li>Turn on <strong>resolve pronouns</strong>. Similarity jumps, because the searchable nouns are now in the text.</li><li>Turn on <strong>over-enrich</strong>. The chunk stays findable and stops being distinguishable from its sibling &mdash; the cost of adding too much shared context.</li></ol>"),
        ("What to remember",
         "<p>Context-aware chunking changes what is stored rather than where the cut falls. A chunk full of pronouns and back-references is unusable by the generator and invisible to retrieval, so title, heading path and resolved references are added back. Keep the enrichment short relative to the chunk, or shared context dominates the embedding and chunks stop being distinguishable.</p>"),
    ],
)


# =========================================================================
# Indexing and scale
# =========================================================================

_t(
    slug="indexing_in_vector_databases",
    group_label="Scale",
    level="Intermediate",
    title="Indexing in vector databases",
    asked="What does a vector database index actually do, and why can't it just "
          "compare every vector?",
    desc="Why exact nearest-neighbour search does not scale, what an index trades "
         "away to fix it, and the three costs every index type balances.",
    lead="Without an index, finding the nearest vector means comparing the query "
         "against <strong>every</strong> stored vector &mdash; linear in the "
         "corpus and hopeless past a few hundred thousand. An index organises "
         "the vectors so most of them are never examined, and pays for that with "
         "<strong>recall</strong>: it may miss a true neighbour.",
    say="\"A flat index is exact and O(n) per query. Any real index is "
        "approximate - it prunes most of the corpus and accepts missing some "
        "true neighbours. The three knobs are always the same: recall, latency "
        "and memory, and you can have two.\"",
    notice=[
        "Exact search touches every vector; the cost is linear in the corpus.",
        "An index skips most of them, and can miss a true neighbour.",
        "Recall, latency and memory &mdash; pick two.",
    ],
    viz=WIDGETS["indexing_in_vector_databases"],
    sections=[
        ("Why exact search stops working",
         "<p>A flat index stores the vectors and compares the query with every "
         "one. It is exact, trivially correct, and the right answer for small "
         "collections &mdash; and the cost is O(n&middot;d) per query, so a "
         "million 768-dimensional vectors is around 768 million multiply-adds "
         "for a single search.</p>"
         "<p>It is also the ground truth. To measure any approximate index's "
         "recall you need the true neighbours, and a flat search over a sample "
         "is how you get them.</p>"),
        ("What an index buys and what it costs",
         "<p>Every approximate index prunes: it organises vectors so that most "
         "can be skipped without being compared. That turns a linear scan into "
         "something closer to logarithmic, and introduces the possibility of "
         "missing a genuine neighbour because the structure routed the search "
         "elsewhere.</p>"
         "<p>So the metric is <strong>recall@k</strong>: of the k true nearest "
         "neighbours, how many did the index return? 0.95 is typical and "
         "usually fine for RAG, where a reranker sees the top 50 anyway. It is "
         "not fine for deduplication or exact matching.</p>"),
        ("The families, briefly",
         "<p><strong>IVF</strong> clusters the vectors and searches only the "
         "nearest few clusters. Cheap to build, and it misses neighbours that "
         "sit just across a cluster boundary.</p>"
         "<p><strong>HNSW</strong> builds a navigable small-world graph and "
         "walks it greedily. Best recall-for-latency, and the highest memory "
         "&mdash; it stores the graph as well as the vectors. This is the "
         "default in most vector databases; see "
         "<a href=\"ann_indexing_hnsw_and_ivf.html\">ANN indexing</a>.</p>"
         "<p><strong>Product quantization</strong> compresses each vector into "
         "a short code, cutting memory by an order of magnitude at some cost to "
         "recall. Usually combined with IVF rather than used alone.</p>"
         "<p>Also note what an index does <em>not</em> do: filtering by metadata "
         "is a separate problem, and combining it with vector search is where "
         "most vector databases differ from each other &mdash; see "
         "<a href=\"permission_filtering_in_rag.html\">permission "
         "filtering</a>.</p>"),
    
        ("Things to try",
         "<ol><li>Set <strong>clusters probed</strong> to 1. Recall collapses &mdash; most true neighbours live in clusters the search never opened.</li><li>Raise probes until recall reaches 1.0. You are now comparing against the whole corpus: an exact search with extra steps.</li><li>Raise <strong>clusters</strong> with probes fixed. Finer clusters mean fewer comparisons and lower recall &mdash; the same trade from the other direction.</li></ol>"),
        ("What to remember",
         "<p>Without an index, finding the nearest vector means comparing against every stored vector. An index prunes most of them and pays for it in recall, so the metric is recall@k measured against an exact search. Recall, latency and memory are the three knobs, and every index type exposes them under different names.</p>"),
    ],
)


_t(
    slug="ann_indexing_hnsw_and_ivf",
    group_label="Scale",
    level="Advanced",
    title="ANN indexing: HNSW and IVF",
    asked="How does approximate nearest neighbour search actually work? Explain "
          "HNSW.",
    desc="How HNSW's layered navigable graph and IVF's cluster-and-probe reach "
         "sublinear search, the parameters that matter, and how each fails.",
    lead="Two ideas. <strong>IVF</strong> clusters the vectors and searches only "
         "the nearest few clusters. <strong>HNSW</strong> builds a layered graph "
         "&mdash; sparse at the top for long hops, dense at the bottom for "
         "precision &mdash; and walks greedily downwards. Both skip most of the "
         "corpus; they differ in how they choose what to skip.",
    say="\"HNSW is a multi-layer proximity graph. The top layer is sparse so you "
        "cross the space in a few hops, and each layer down is denser, so you "
        "descend into the neighbourhood and refine. Greedy search with a "
        "candidate list - efSearch controls the recall/latency trade. IVF is "
        "simpler: cluster, then probe the nearest few.\"",
    notice=[
        "The top layer covers distance; the bottom layer covers precision.",
        "Search is greedy &mdash; it can settle in a local minimum and miss.",
        "<code>efSearch</code> widens the beam: better recall, more time.",
    ],
    viz=WIDGETS["ann_indexing_hnsw_and_ivf"],
    sections=[
        ("HNSW: skip lists, in vector space",
         "<p>Take a proximity graph &mdash; each vector linked to its nearest "
         "neighbours &mdash; and stack several, each a random sample of the one "
         "below. Search enters at the sparse top layer and greedily moves to "
         "whichever neighbour is closer to the query, until no neighbour "
         "improves. Then it drops a layer and repeats.</p>"
         "<p>The top layers have long edges, so a few hops cross most of the "
         "space; the bottom layer has short edges, so the final steps are "
         "precise. It is the skip-list idea applied to geometry, and it is the "
         "reason HNSW dominates: excellent recall at low latency.</p>"),
        ("The parameters worth naming",
         "<p><strong>M</strong> &mdash; edges per node, fixed at build time. "
         "Higher means a better-connected graph, better recall, more memory. "
         "The graph itself is a real memory cost on top of the vectors, which "
         "is HNSW's main drawback.</p>"
         "<p><strong>efConstruction</strong> &mdash; how hard the builder works "
         "to find good neighbours. Build-time only: slower indexing, better "
         "graph forever.</p>"
         "<p><strong>efSearch</strong> &mdash; the size of the candidate list "
         "during a query. The runtime knob: raise it for recall, lower it for "
         "latency, per query if you like. This is the one to mention, because "
         "it is the one you actually tune in production.</p>"),
        ("How each one fails",
         "<p>HNSW's search is greedy, so it can settle in a local minimum and "
         "return a neighbourhood that is good but not the best. A wider "
         "<code>efSearch</code> makes that less likely without eliminating it. "
         "Deletion is also awkward &mdash; removing a node can disconnect the "
         "graph &mdash; so most implementations tombstone and rebuild "
         "periodically.</p>"
         "<p>IVF's failure is cleaner: a true neighbour sitting just across a "
         "cluster boundary is missed unless that cluster is probed. More probes "
         "fixes it and costs latency. IVF is cheaper to build and to update, "
         "which is why it survives alongside HNSW &mdash; and combined with "
         "product quantization it is what runs when memory, not latency, is the "
         "binding constraint.</p>"),
    
        ("Things to try",
         "<ol><li>Sweep <strong>efSearch</strong> from 8 to 512. Recall and latency both climb &mdash; this is the knob you tune in production, and it can differ per query.</li><li>Drop <strong>M</strong> to 4. Recall is capped no matter how large efSearch gets: build-time damage cannot be repaired at query time.</li><li>Raise M to 48 and watch the index memory. The graph is stored alongside the vectors, which is HNSW's main cost.</li></ol>"),
        ("What to remember",
         "<p>HNSW stacks proximity graphs: sparse upper layers with long edges to cross the space, a dense bottom layer to refine. Search is greedy with a candidate list of width efSearch, which is the runtime recall/latency knob. M and efConstruction are fixed at build time. IVF is the simpler alternative &mdash; cluster then probe &mdash; cheaper to build and update, and it misses neighbours across cluster boundaries.</p>"),
    ],
)


_t(
    slug="permission_filtering_in_rag",
    group_label="Scale",
    level="Advanced",
    title="Permission filtering in RAG retrieval",
    asked="How do you stop a RAG system retrieving documents the user is not "
          "allowed to see?",
    desc="Pre-filtering, post-filtering and the recall trap between them - and "
         "why filtering after generation is not filtering at all.",
    lead="Filter <strong>inside</strong> the search, not around it. Post-filtering "
         "&mdash; retrieve k, then drop what the user cannot see &mdash; is the "
         "obvious approach and it silently returns fewer results, sometimes "
         "none, because the permitted documents were never in the top k. And "
         "filtering after generation is not filtering: the model already read "
         "the text.",
    say="\"Pre-filter inside the index, so the ANN search only ever traverses "
        "documents the user can see. Post-filtering breaks recall - you ask for "
        "10, get 10, drop 8, and answer from 2. And the ACL has to be evaluated "
        "at query time, because permissions change after indexing.\"",
    notice=[
        "Post-filtering removes results <em>after</em> the top-k is chosen.",
        "The permitted documents may never have entered the top-k at all.",
        "Filtering after generation is too late &mdash; the model already saw it.",
    ],
    viz=WIDGETS["permission_filtering_in_rag"],
    sections=[
        ("Why post-filtering quietly fails",
         "<p>Retrieve the top 10 by similarity, then remove what the user may "
         "not see. If eight were restricted you return two, and nothing "
         "reports that the result set collapsed. The generator answers from "
         "thin evidence and sounds no less confident.</p>"
         "<p>Over-fetching &mdash; retrieve 100, filter, keep 10 &mdash; makes "
         "it less likely and never fixes it. A user with access to 0.1% of the "
         "corpus needs an enormous k, and the failure is worst exactly for the "
         "most restricted users.</p>"),
        ("Pre-filtering, and why it is harder than it looks",
         "<p>Pre-filtering restricts the candidate set before ranking, so the "
         "top k is k <em>permitted</em> results. That is the correct behaviour "
         "and it fights the index: an HNSW graph is built over all vectors, and "
         "walking it while skipping most nodes can disconnect the search "
         "&mdash; you traverse into a region where everything is filtered out "
         "and the walk stalls.</p>"
         "<p>Vector databases handle this differently, which is one of the real "
         "differences between them. Options include filtered graph traversal, "
         "per-tenant sub-indexes (clean, and costly at many tenants), and "
         "falling back to a flat scan when the filter is very selective "
         "&mdash; which is often genuinely fastest, because the permitted set "
         "is small.</p>"),
        ("Where the permissions live",
         "<p>Baking an access list into each chunk's metadata at index time is "
         "fast and goes stale the moment someone leaves a group &mdash; and "
         "stale permissions fail open, which is the wrong direction.</p>"
         "<p>The usual compromise: index a stable <em>group</em> identifier "
         "with each chunk, resolve the user's groups per request from the "
         "identity system, and filter on the intersection. Group membership "
         "changes are then reflected immediately without re-indexing "
         "anything.</p>"
         "<p>Two more things to say. Deleted documents must leave the index, "
         "not just be filtered out. And the filter belongs on the server, "
         "derived from the authenticated session &mdash; never from a "
         "client-supplied user id, which is trivially forged.</p>"),
    
        ("Things to try",
         "<ol><li>Drop <strong>corpus visible</strong> to 5%. Post-filtering returns almost nothing while pre-filtering still returns k &mdash; the control fails worst for the most restricted user.</li><li>Raise <strong>over-fetch</strong> to 500. The shortfall shrinks and never disappears, which is why over-fetching is a mitigation rather than a fix.</li><li>Set visibility to 100%. All three strategies agree, which is exactly why this bug survives testing on an admin account.</li></ol>"),
        ("What to remember",
         "<p>Permission filtering has to happen inside the search, not around it. Post-filtering ranks first and drops afterwards, so it silently returns fewer results than requested and degrades worst for the most restricted users. Filtering after generation is not a control at all &mdash; the model has already read the text. Index a group id and resolve membership per request, because stale permissions fail open.</p>"),
    ],
)


_t(
    slug="distributed_retrieval_and_sharding",
    group_label="Scale",
    level="Advanced",
    title="Distributed retrieval and sharding",
    asked="How do you scale retrieval past one machine? What are the trade-offs "
          "between sharding strategies?",
    desc="Scatter-gather across shards, why random sharding beats semantic "
         "sharding for recall, the tail-latency problem, and how replicas differ "
         "from shards.",
    lead="Split the index across machines and query them all: "
         "<strong>scatter-gather</strong>. Each shard returns its own top k and "
         "a coordinator merges them. Two things decide whether it works: "
         "<em>how</em> you shard, and the fact that your latency is now the "
         "slowest shard's, not the average.",
    say="\"Scatter-gather: every shard searches its slice, returns local top-k, "
        "and a coordinator merges. Shard randomly, not by topic - semantic "
        "sharding concentrates the relevant documents in one shard and wrecks "
        "recall when you only take k from each. And p99 latency is the slowest "
        "shard, so tail latency gets worse with every shard you add.\"",
    notice=[
        "Every shard is queried; the coordinator merges local top-k lists.",
        "Random sharding spreads relevant documents evenly &mdash; that is the point.",
        "Latency is the <em>slowest</em> shard, not the average.",
    ],
    viz=WIDGETS["distributed_retrieval_and_sharding"],
    sections=[
        ("Shards and replicas are different things",
         "<p>A <strong>shard</strong> holds a slice of the corpus. Sharding "
         "handles data that will not fit &mdash; memory or index build time "
         "&mdash; and every query must visit every shard.</p>"
         "<p>A <strong>replica</strong> holds a complete copy of a shard. "
         "Replication handles query volume and failure, and a query goes to one "
         "replica of each shard.</p>"
         "<p>They solve different problems and are often confused. If the index "
         "fits on one machine and you are simply serving too many queries, you "
         "need replicas and no sharding at all &mdash; which is much simpler, "
         "because there is nothing to merge.</p>"),
        ("Shard randomly",
         "<p>The instinct is to shard by topic or tenant so a query only "
         "touches one shard. For a multi-tenant system where every query is "
         "scoped to one tenant, that is right &mdash; it is really many small "
         "indexes.</p>"
         "<p>For a general corpus it is a mistake. If all the finance documents "
         "live on shard 2, a finance query's true top 50 are all there, and "
         "taking only the local top 5 discards forty-five of them. Random "
         "sharding spreads relevant documents evenly so a modest per-shard k "
         "captures nearly all of them.</p>"
         "<p>The fix if you must shard semantically is to over-fetch from every "
         "shard, which costs the bandwidth and latency the routing was meant to "
         "save.</p>"),
        ("Tail latency, and the merge",
         "<p>Scatter-gather waits for the slowest shard, so p99 response time is "
         "roughly the p99 of <em>any</em> shard. Add shards and the chance one "
         "is slow rises &mdash; the classic result is that latency gets worse as "
         "you scale out, not better.</p>"
         "<p>Mitigations: hedged requests (ask two replicas, take the first "
         "answer), a deadline after which a late shard is dropped and the "
         "degraded result served, and keeping shard counts modest.</p>"
         "<p>The merge itself needs care. Scores must be comparable across "
         "shards &mdash; fine for cosine similarity, not fine for BM25, whose "
         "IDF depends on corpus statistics that differ per shard unless they "
         "are shared globally. That is a real bug in hand-rolled distributed "
         "lexical search.</p>"),
    
        ("Things to try",
         "<ol><li>Switch to <em>semantic</em> sharding. Recall collapses: every relevant document is on one shard, whose local top-k discards the rest.</li><li>With semantic sharding, raise <strong>per-shard k</strong> until recall recovers. You have paid back the bandwidth the topic routing was meant to save.</li><li>Raise <strong>shards</strong> to 40 with random sharding. Recall is fine and p99 latency climbs, because scatter-gather waits for whichever shard was slow.</li></ol>"),
        ("What to remember",
         "<p>Scatter-gather sends the query to every shard, takes a local top-k from each and merges. Shard randomly rather than by topic, or the relevant documents concentrate in one shard and its local k throws most of them away. Latency becomes the slowest shard's, not the average, so p99 gets worse with every shard added. Shards solve data that will not fit; replicas solve query volume.</p>"),
    ],
)


# =========================================================================
# Ranking metrics
# =========================================================================

_SHARED_RANKING = (
    "<p>All four of these read the same object: an ordered list of retrieved "
    "results, with each one labelled relevant or not by a human or a strong "
    "model. They differ only in what they choose to notice about it &mdash; "
    "which is why quoting one without saying which is close to meaningless, and "
    "why the visualisation above shows all four at once.</p>"
    "<p>The labels are the expensive part. A relevance judgement per "
    "query-document pair is human work, and an evaluation set of fifty queries "
    "with judged results is worth more than any amount of metric sophistication "
    "on top of unjudged data. Build the set first.</p>")

_t(
    slug="hit_rate_at_k",
    group_label="Evaluation",
    level="Beginner",
    title="What is Hit Rate@k?",
    asked="What does Hit Rate@k measure, and when is it the right metric for a "
          "retriever?",
    desc="Hit Rate@k asks one binary question - was anything relevant in the top "
         "k? - which makes it the right first metric for a RAG retriever and a "
         "poor one for ranking quality.",
    lead="The bluntest of the ranking metrics, and often the most useful one to "
         "start with. <strong>Hit Rate@k is 1 if at least one relevant document "
         "appears in the top k, and 0 otherwise.</strong> It does not care how "
         "many relevant documents there were, or where in the top k they landed. "
         "Averaged over a query set, it answers a single question: how often "
         "does retrieval put <em>something</em> useful in front of the "
         "generator?",
    notice=[
        "Click any result to flip whether it is relevant.",
        "Hit Rate jumps to 1 the moment one relevant item enters the top k.",
        "Move k below the first relevant rank and it collapses to 0.",
    ],
    viz=WIDGETS["hit_rate_at_k"],
    sections=[
        ("The definition, and the averaging that hides in it",
         "<p>For a single query, Hit Rate@k is binary: 1 if any of the top k "
         "results is relevant, 0 if none is. There is no partial credit. A query "
         "whose top 3 contains five relevant documents and a query whose top 3 "
         "contains exactly one both score 1.</p>"
         "<p>What people usually mean by \"our hit rate is 0.82\" is the mean of "
         "that binary value across an evaluation set: 82% of queries had "
         "something useful in the top k. That framing is worth saying out loud, "
         "because it makes the metric's shape obvious &mdash; it is a proportion "
         "of queries, not a proportion of documents.</p>"
         "<p>You will also see it called <em>recall@k with a single relevant "
         "document</em>, and in recommender literature simply <em>hit "
         "rate</em>. When every query has exactly one correct answer, Hit "
         "Rate@k and Recall@k are the same number, which is why the two get "
         "confused.</p>"),
        ("Why it is the right first metric for RAG",
         "<p>A RAG generator does not need every relevant document. It needs "
         "enough grounding to answer, and for most factual questions one good "
         "chunk is enough. If the answer is in the context, the model can use "
         "it; if it is not, no amount of prompt engineering will recover it.</p>"
         "<p>That makes Hit Rate@k a measure of the <strong>ceiling</strong> on "
         "your whole pipeline. A hit rate of 0.7 at your context budget means "
         "30% of queries are unanswerable no matter how good the generator is, "
         "and every hour spent tuning prompts against those queries is wasted. "
         "It is the number to establish before anything else, because it tells "
         "you whether your problem is retrieval or generation.</p>"
         "<p>It is also cheap to label. Deciding \"is there anything useful "
         "here?\" is much faster for a human annotator than grading every "
         "document on a five-point scale, so a hit-rate evaluation set can be "
         "built in an afternoon.</p>"),
        ("What it deliberately ignores",
         "<p><strong>Position.</strong> A relevant document at rank 1 and at "
         "rank k score identically. That matters more than it sounds: models "
         "attend unevenly across a long context, and evidence buried at the "
         "bottom of ten chunks is measurably less likely to be used. Hit rate "
         "will not show you that; MRR will.</p>"
         "<p><strong>Quantity.</strong> One relevant document scores the same "
         "as five. For a question needing several sources &mdash; \"compare our "
         "refund policy across regions\" &mdash; hit rate can be 1.0 while the "
         "answer is hopelessly incomplete. Recall@k is the metric that "
         "notices.</p>"
         "<p><strong>Noise.</strong> Nine irrelevant results alongside one good "
         "one still scores 1. Irrelevant context measurably degrades generation "
         "and inflates cost, so a high hit rate with low precision is a real "
         "failure mode that this metric reports as success.</p>"),
        ("Choosing k, and reading the curve",
         "<p>k should be the number of chunks you actually put in the prompt. "
         "Evaluating at k=10 when you pass 3 to the model measures a system you "
         "are not running. This is the single most common mistake with @k "
         "metrics.</p>"
         "<p>Plotting hit rate against k is more informative than any single "
         "value. If it climbs steeply from k=1 to k=5 and then flattens, your "
         "retriever finds the right documents but ranks them poorly &mdash; a "
         "reranker will help a lot. If it is flat and low from the start, the "
         "documents are not being retrieved at all, and the problem is your "
         "embeddings, your chunking, or the fact that the answer is not in the "
         "corpus.</p>"
         "<p>That diagnostic split is the most valuable thing hit rate gives "
         "you, and it costs one evaluation run.</p>"),
        ("Things to try",
         "<ol><li>Set <strong>k</strong> to 1. Hit rate is 1 only if the very "
         "first result is relevant &mdash; this is the strictest possible "
         "reading, and the closest to what a single-chunk pipeline "
         "experiences.</li>"
         "<li>Click the top result to mark it irrelevant, then lower k to 2. "
         "Watch hit rate fall to 0 while recall and precision degrade "
         "gradually &mdash; the binary metric is far more brittle.</li>"
         "<li>Mark every result irrelevant, then mark just the last one "
         "relevant. Hit rate stays 0 until k reaches 10, then snaps to 1: no "
         "partial credit anywhere along the way.</li></ol>"),
        ("What to remember",
         "<p>Hit Rate@k is the proportion of queries with at least one relevant "
         "result in the top k. It is binary per query, ignores position and "
         "quantity, and measures the ceiling on your pipeline &mdash; if the "
         "evidence never reaches the model, nothing downstream can fix it. Use "
         "it as the first number you establish, set k to the number of chunks "
         "you actually pass to the generator, and plot it against k to tell a "
         "ranking problem from a retrieval problem. Then reach for "
         "<a href=\"recall_at_k.html\">Recall@k</a> when queries need several "
         "documents, and <a href=\"mean_reciprocal_rank.html\">MRR</a> when "
         "position matters.</p>" + _SHARED_RANKING),
    ],
)

_t(
    slug="recall_at_k",
    group_label="Evaluation",
    level="Beginner",
    title="What is Recall@k?",
    asked="What does Recall@k measure, and why is it usually the metric that "
          "matters most for a RAG retriever?",
    desc="Recall@k is the fraction of all relevant documents that made it into "
         "the top k - the metric that decides whether the generator has the "
         "evidence it needs.",
    lead="Of all the documents that <em>should</em> have been retrieved, what "
         "fraction actually made the top k? <strong>Recall@k = relevant "
         "retrieved in top k &divide; total relevant in the corpus.</strong> It "
         "is the metric that answers the question a RAG pipeline actually cares "
         "about &mdash; did the evidence reach the model? &mdash; and the only "
         "one of the four that can be improved simply by looking deeper.",
    notice=[
        "Click results to change which are relevant; the denominator moves too.",
        "Raising k can only ever increase recall, never decrease it.",
        "Recall reaches 1.0 only when every relevant document is inside k.",
    ],
    viz=WIDGETS["recall_at_k"],
    sections=[
        ("The definition, and the denominator people forget",
         "<p>Recall@k is the number of relevant documents in the top k divided "
         "by the <strong>total number of relevant documents that exist</strong>. "
         "The numerator is easy; the denominator is where the difficulty "
         "lives.</p>"
         "<p>Knowing it requires knowing every relevant document in the corpus "
         "for every evaluation query. On a corpus of a hundred documents you can "
         "label exhaustively. On a million you cannot, so the denominator is "
         "estimated &mdash; usually by pooling: run several different retrievers, "
         "judge the union of everything any of them returned, and treat that "
         "pool as the ground truth. It is the standard approach and it is "
         "biased, because a document no retriever surfaced is silently counted "
         "as irrelevant.</p>"
         "<p>Be honest about this when you report recall. \"Recall@5 is 0.83 "
         "against a pooled judgement set\" is a defensible claim; \"recall@5 is "
         "0.83\" without qualification implies exhaustive labelling you almost "
         "certainly do not have.</p>"),
        ("Why it is the retrieval metric for RAG",
         "<p>The generator can ignore an irrelevant chunk. It cannot invent a "
         "relevant one that was never retrieved. That asymmetry is the whole "
         "argument: <strong>recall failures are unrecoverable, precision "
         "failures are merely expensive</strong>.</p>"
         "<p>So the usual configuration is to retrieve generously &mdash; a "
         "large k, favouring recall &mdash; and then let a reranker or the "
         "model's own attention handle precision. Retrieve 50, rerank to 5, pass "
         "5. Recall@50 is the number that bounds what the reranker can possibly "
         "achieve, and precision@5 is what the generator actually sees.</p>"
         "<p>This is also why hybrid search exists. Dense and sparse retrievers "
         "fail on different queries, so taking the union of both raises recall "
         "well above either alone &mdash; see "
         "<a href=\"hybrid_search_reciprocal_rank_fusion.html\">hybrid "
         "search</a>. Fusing two retrievers is a recall strategy first and a "
         "ranking strategy second.</p>"),
        ("The monotonicity that makes it easy to game",
         "<p>Recall@k never decreases as k grows. Retrieve the entire corpus "
         "and recall is exactly 1.0. That makes it trivially gameable and means "
         "a recall number without its k is not a number at all.</p>"
         "<p>It also means recall must always be read alongside a cost. In "
         "classical IR that partner is precision, and the two are combined into "
         "F1. In RAG the more meaningful partner is your context budget: recall "
         "at the k you can actually afford to put in the prompt. Recall@100 is "
         "irrelevant if you pass three chunks.</p>"
         "<p>The useful diagnostic is the gap between recall at a large k and "
         "recall at your real k. A large gap means the documents are being "
         "found but ranked badly, which is exactly what a cross-encoder "
         "reranker fixes. A small gap means better ranking will not help and the "
         "problem is upstream &mdash; embeddings, chunking, or coverage.</p>"),
        ("Where recall is the wrong metric",
         "<p><strong>When one document suffices.</strong> If a query has a "
         "single correct answer, recall@k collapses into "
         "<a href=\"hit_rate_at_k.html\">Hit Rate@k</a> and the extra machinery "
         "buys nothing.</p>"
         "<p><strong>When context is tight.</strong> Optimising recall pushes k "
         "up, and a long context of mostly-irrelevant chunks measurably degrades "
         "generation quality and inflates cost. Past a point, more recall makes "
         "answers worse.</p>"
         "<p><strong>When relevance is graded rather than binary.</strong> "
         "Recall treats a perfect document and a marginally useful one "
         "identically. If your judgements have degrees, nDCG uses them and "
         "recall throws them away.</p>"),
        ("Things to try",
         "<ol><li>Drag <strong>k</strong> from 1 to 10 and watch recall climb "
         "and never fall. That monotonicity is why a recall figure without its k "
         "means nothing.</li>"
         "<li>Mark one more result relevant. Recall <em>drops</em> even though "
         "nothing about the ranking changed &mdash; the denominator grew. This "
         "is what makes an incomplete judgement set flatter your system.</li>"
         "<li>Set k to 3 and compare recall with precision. They move in "
         "opposite directions as k changes, which is the trade the whole field "
         "is organised around.</li></ol>"),
        ("What to remember",
         "<p>Recall@k is the fraction of all relevant documents that reached the "
         "top k. It is the metric that bounds a RAG pipeline, because a document "
         "that was never retrieved cannot be used, while an irrelevant one can "
         "be ignored. It rises monotonically with k, so it is meaningless "
         "without its k and must be read against a cost &mdash; usually your "
         "context budget. Its denominator requires knowing every relevant "
         "document, which on a real corpus means pooled judgements and an "
         "honest caveat.</p>" + _SHARED_RANKING),
    ],
)


_t(
    slug="precision_at_k",
    group_label="Evaluation",
    level="Beginner",
    title="What is Precision@k?",
    asked="What does Precision@k measure, and why does it matter more in RAG "
          "than people expect?",
    desc="Precision@k is the fraction of the top k results that are relevant - "
         "the metric that measures how much noise you are paying to send to the "
         "generator.",
    lead="Of the k documents you returned, what fraction were actually useful? "
         "<strong>Precision@k = relevant in top k &divide; k.</strong> Where "
         "recall asks whether the evidence arrived, precision asks how much "
         "rubbish arrived with it &mdash; and in a RAG system that rubbish costs "
         "tokens, latency, and measurable answer quality.",
    notice=[
        "The denominator is always k, whatever the corpus contains.",
        "Precision usually falls as k rises &mdash; the best results are at the top.",
        "Click results to see precision and recall move in opposite directions.",
    ],
    viz=WIDGETS["precision_at_k"],
    sections=[
        ("The definition, and the denominator that never moves",
         "<p>Precision@k is the number of relevant documents in the top k "
         "divided by k. Not by the number of relevant documents in the corpus, "
         "and not by the number retrieved &mdash; by k, always.</p>"
         "<p>That fixed denominator is what makes precision cheap to measure. "
         "You only need judgements for the k results you actually returned, not "
         "for the whole corpus. An evaluation set for precision can be built by "
         "judging a few hundred query-document pairs; one for recall needs "
         "exhaustive or pooled labelling. If you can only afford one, precision "
         "is the affordable one.</p>"
         "<p>The consequence of the fixed denominator: if fewer than k documents "
         "are relevant in total, precision@k <em>cannot</em> reach 1.0. With two "
         "relevant documents and k=5, the ceiling is 0.4. A low precision score "
         "is sometimes a property of the query, not a failure of the "
         "retriever.</p>"),
        ("Why noise is not free in a RAG pipeline",
         "<p>The old intuition &mdash; \"the model can just ignore irrelevant "
         "chunks\" &mdash; is not quite true, and the ways it fails are "
         "worth naming.</p>"
         "<p><strong>Cost and latency.</strong> Every retrieved chunk is input "
         "tokens on every request. Halving the number of chunks halves that bill "
         "and shortens time to first token.</p>"
         "<p><strong>Distraction.</strong> Irrelevant context measurably reduces "
         "answer quality. A plausible-but-wrong passage is worse than no passage "
         "&mdash; the model has been handed a reason to be confidently "
         "incorrect, and it is grounded in a real retrieved document, which "
         "makes the error harder to spot.</p>"
         "<p><strong>Position effects.</strong> Attention over a long context is "
         "uneven, with the middle attended least. Padding the prompt with "
         "irrelevant chunks pushes good evidence into that dead zone.</p>"
         "<p>So precision is not merely an efficiency metric here. Past a point, "
         "improving precision improves the answers.</p>"),
        ("The trade with recall, and where each belongs",
         "<p>Precision and recall pull against each other as k moves. Raising k "
         "can only help recall and usually hurts precision, because the highest-"
         "scoring results were already at the top and what follows is "
         "progressively worse.</p>"
         "<p>The standard combination is F1, the harmonic mean, which punishes "
         "an imbalance &mdash; a system with precision 1.0 and recall 0.1 scores "
         "0.18, not 0.55. The harmonic mean is used precisely because it refuses "
         "to let one strong number hide a weak one.</p>"
         "<p>In a modern RAG stack the two are usually optimised at different "
         "stages. The retriever runs at high k for recall; the "
         "<a href=\"reranking_bi_encoders_vs_cross_encoders.html\">reranker</a> "
         "cuts that to a handful for precision. Measuring recall@50 and "
         "precision@5 in the same evaluation tells you which of the two stages "
         "is failing, and they are fixed by completely different work.</p>"),
        ("What precision cannot see",
         "<p><strong>Order within k.</strong> Relevant documents at ranks 1 and "
         "2 score the same as relevant documents at ranks 4 and 5. For a "
         "generator, that difference is real; precision is blind to it and "
         "<a href=\"mean_reciprocal_rank.html\">MRR</a> or nDCG is not.</p>"
         "<p><strong>What was missed.</strong> A retriever that returns three "
         "perfect documents and misses seven more scores precision 1.0. The "
         "metric is silent about the corpus it did not touch, which is exactly "
         "why it is never reported alone.</p>"
         "<p><strong>Degrees of usefulness.</strong> Binary relevance forces a "
         "yes/no on documents that are genuinely partial. If your judgements are "
         "graded, nDCG uses that information and precision discards it.</p>"),
        ("Things to try",
         "<ol><li>Drag <strong>k</strong> up from 1. Precision generally falls "
         "while recall rises &mdash; that opposition is the whole reason both "
         "numbers are quoted together.</li>"
         "<li>Set k to 10 with four relevant documents. Precision cannot exceed "
         "0.4 however good the ranking is; the ceiling is set by the query, not "
         "the retriever.</li>"
         "<li>Mark the two lowest results relevant and watch precision@5 stay "
         "put. Improving what sits below k does nothing for it &mdash; which is "
         "why k must match what you actually send to the model.</li></ol>"),
        ("What to remember",
         "<p>Precision@k is the fraction of the returned k that was relevant, "
         "with k always as the denominator. It is the cheap metric to label, "
         "because it needs judgements only for what you returned. In a RAG "
         "pipeline it is not just about efficiency: irrelevant context costs "
         "tokens, pushes good evidence into the least-attended part of the "
         "prompt, and gives the model plausible material to be wrong with. "
         "Optimise recall at the retriever and precision at the reranker, and "
         "report both with their k.</p>" + _SHARED_RANKING),
    ],
)

_t(
    slug="mean_reciprocal_rank",
    group_label="Evaluation",
    level="Intermediate",
    title="What is MRR (Mean Reciprocal Rank)?",
    asked="What does MRR measure, and when is the position of the first correct "
          "result the thing that matters?",
    desc="MRR averages 1/rank of the first relevant result across queries - the "
         "metric for systems where the user or the model looks at the top of the "
         "list and stops.",
    lead="For one query, find the rank of the <strong>first</strong> relevant "
         "result and take its reciprocal: rank 1 scores 1.0, rank 2 scores 0.5, "
         "rank 5 scores 0.2, nothing relevant scores 0. Average that across your "
         "queries and you have MRR. Everything after the first hit is ignored "
         "entirely &mdash; which is the point, and the limitation.",
    notice=[
        "Only the first relevant result contributes; the rest are ignored.",
        "The reciprocal drops steeply: rank 1 to rank 2 halves the score.",
        "Click the top result on and off to see the whole metric swing.",
    ],
    viz=WIDGETS["mean_reciprocal_rank"],
    sections=[
        ("The definition, and the shape of the curve",
         "<p>Reciprocal rank for a query is 1/(rank of the first relevant "
         "result). MRR is the mean of that over an evaluation set. The name is "
         "worth reading literally: it is a <em>mean</em> of <em>reciprocal</em> "
         "<em>ranks</em>, and each word matters.</p>"
         "<p>The reciprocal makes the curve steep at the top and flat at the "
         "bottom. Moving a result from rank 2 to rank 1 gains 0.5. Moving one "
         "from rank 10 to rank 9 gains about 0.011 &mdash; forty-five times "
         "less. That shape encodes an assumption: users and models care "
         "enormously about the top of the list and barely at all about the "
         "bottom.</p>"
         "<p>Because it is a mean of per-query scores, a single query can move "
         "it noticeably on a small evaluation set. Report the number of queries "
         "alongside it, and be suspicious of MRR differences on fewer than a "
         "hundred.</p>"),
        ("When position is the whole question",
         "<p>MRR is the right metric when the consumer stops at the first good "
         "result. Question answering with a single correct answer, "
         "\"I'm feeling lucky\" search, entity lookup, a code assistant jumping "
         "to a definition &mdash; in all of these the second correct result is "
         "worth nothing.</p>"
         "<p>It also matters inside RAG more than it first appears. Attention "
         "over a long context is uneven, and evidence placed first is more "
         "likely to be used than evidence placed eighth. Two retrievers with "
         "identical recall@5 can produce measurably different answers if one "
         "puts the key chunk at the top and the other buries it. Recall cannot "
         "see that difference; MRR can.</p>"
         "<p>The practical use: track recall@k to know whether the evidence "
         "arrives, and MRR to know whether it arrives somewhere the model will "
         "actually look. A reranker that leaves recall unchanged while lifting "
         "MRR is doing real work.</p>"),
        ("What it ignores, and when that is wrong",
         "<p><strong>Every relevant result after the first.</strong> A query "
         "with one relevant document at rank 1 and a query with ten relevant "
         "documents at ranks 1 to 10 both score 1.0. If your questions need "
         "multiple sources &mdash; comparisons, summaries, anything aggregative "
         "&mdash; MRR is close to blind to what you care about, and "
         "<a href=\"recall_at_k.html\">Recall@k</a> is the metric to use.</p>"
         "<p><strong>Degrees of relevance.</strong> A marginally useful document "
         "at rank 1 outscores a perfect one at rank 2. MAP averages precision "
         "over every relevant position and nDCG additionally uses graded "
         "judgements; both are strictly more informative and both cost more to "
         "label.</p>"
         "<p><strong>The zero.</strong> Queries with no relevant result "
         "contribute 0, which is correct and worth watching: a system with "
         "excellent MRR on the queries it answers and a large silent tail of "
         "zeros has a coverage problem that the average partially conceals. "
         "Report the proportion of zero-score queries next to it.</p>"),
        ("Reading MRR against the alternatives",
         "<p>The family is easiest to keep straight by what each one uses:</p>"
         "<p><strong>Hit Rate@k</strong> &mdash; is there anything relevant in "
         "the top k? Binary, ignores position entirely.</p>"
         "<p><strong>MRR</strong> &mdash; where is the <em>first</em> relevant "
         "result? Uses position, ignores everything after it.</p>"
         "<p><strong>MAP</strong> &mdash; where is <em>every</em> relevant "
         "result? Uses all positions, still binary relevance.</p>"
         "<p><strong>nDCG</strong> &mdash; where is every relevant result, and "
         "how relevant is each? Uses positions and grades, and is the most "
         "informative and most expensive.</p>"
         "<p>They are a ladder of increasing information and increasing "
         "labelling cost. Climb it only as far as your judgements can honestly "
         "support: nDCG computed from binary labels guessed by a weak model is "
         "not better than a hit rate from careful human ones.</p>"),
        ("Things to try",
         "<ol><li>Click result #1 on and off. MRR swings between 1.0 and 0.33 "
         "on a single change, while recall moves a fraction &mdash; MRR is by "
         "far the most position-sensitive of the four.</li>"
         "<li>Mark only the last result relevant. RR is 0.1, and no amount of "
         "additional relevant documents further down would improve it.</li>"
         "<li>Mark results 1 and 2 both relevant, then mark only result 1. MRR "
         "is identical either way &mdash; everything after the first hit is "
         "invisible to it.</li></ol>"),
        ("What to remember",
         "<p>MRR averages 1/rank of the first relevant result. It is the metric "
         "for systems where the consumer stops at the first good answer, and it "
         "is far more sensitive to the top of the ranking than recall or "
         "precision. It ignores every relevant result after the first, so it is "
         "the wrong choice for questions needing several sources. Inside RAG it "
         "is a useful companion to recall: recall says the evidence arrived, MRR "
         "says whether it arrived where the model will actually attend to "
         "it.</p>" + _SHARED_RANKING),
    ],
)


# =========================================================================
# LLM answer-quality dimensions
# =========================================================================

_SHARED_JUDGE = (
    "<p>These four are usually measured with an <strong>LLM as judge</strong>: a "
    "strong model is shown the question, the retrieved context, the answer and "
    "sometimes a reference, and asked to score one dimension at a time. Judging "
    "one dimension per call is not a stylistic choice &mdash; a single prompt "
    "asking for all four produces correlated, mushy scores, because the model "
    "settles on a general impression and applies it everywhere.</p>"
    "<p>Two habits make judge scores trustworthy. Ask for a decision and a "
    "justification, so a human can audit disagreements. And calibrate against a "
    "small human-labelled set before believing any of it &mdash; a judge that "
    "agrees with your annotators 70% of the time is not measuring what you think "
    "it is measuring.</p>")

_t(
    slug="groundedness_in_llm_evaluation",
    group_label="LLM evaluation",
    level="Intermediate",
    title="Groundedness in LLM evaluation",
    asked="What is groundedness, and how is it different from correctness?",
    desc="Groundedness measures whether every claim in an answer is supported by "
         "the retrieved context - the direct measure of hallucination in a RAG "
         "system, and independent of whether the claims are true.",
    lead="Every claim in the answer should trace back to something in the "
         "retrieved context. <strong>Groundedness measures how much of the "
         "answer is actually supported by the evidence the model was given.</strong> "
         "It is the direct, automatable measure of hallucination &mdash; and it "
         "is deliberately blind to whether those claims are true, which is what "
         "separates it from correctness.",
    notice=[
        "Click a claim to flip whether the context supports it.",
        "A claim can be true and ungrounded &mdash; the model knew it, the "
        "context did not say it.",
        "Groundedness needs no reference answer, only the context.",
    ],
    viz=WIDGETS["groundedness_in_llm_evaluation"],
    sections=[
        ("What it measures, claim by claim",
         "<p>The answer is decomposed into atomic claims &mdash; individual "
         "assertions that could each be checked independently &mdash; and each "
         "is tested against the retrieved context. Groundedness is the "
         "proportion that are supported.</p>"
         "<p>The decomposition matters. Scoring a whole paragraph as \"grounded "
         "or not\" throws away the most useful information a groundedness "
         "evaluation produces: <em>which</em> sentence was invented. A per-claim "
         "score points you at the exact span to investigate, and lets you "
         "distinguish an answer that is 90% supported with one fabricated detail "
         "from one that is wholly invented.</p>"
         "<p>\"Supported\" should mean entailed by the context, not merely "
         "consistent with it. A claim the context neither states nor contradicts "
         "is ungrounded, even if it is plausible and even if it is true. That "
         "strictness is the whole value of the metric.</p>"),
        ("Why it is independent of correctness",
         "<p>This is the distinction people collapse, and the four combinations "
         "are all real:</p>"
         "<p><strong>Grounded and correct.</strong> The context said it and it "
         "is true. What you want.</p>"
         "<p><strong>Grounded and wrong.</strong> The context said it and the "
         "context is out of date or simply incorrect. The model behaved "
         "perfectly; your corpus is the problem. Groundedness scores 1.0 and the "
         "user is misinformed.</p>"
         "<p><strong>Ungrounded and correct.</strong> The model knew the answer "
         "from pretraining and the context never mentioned it. Harmless-looking, "
         "and it is the failure mode that erodes trust in a RAG system: you have "
         "no idea which answers came from your documents and which came from the "
         "model's memory, so the citations mean nothing.</p>"
         "<p><strong>Ungrounded and wrong.</strong> A hallucination, in the "
         "ordinary sense.</p>"
         "<p>Groundedness catches rows three and four without needing to know "
         "the truth of anything. That is why it is cheap: it requires the "
         "context and the answer, and no reference and no domain expert.</p>"),
        ("How it is measured in practice",
         "<p><strong>LLM-as-judge, per claim.</strong> Split the answer into "
         "claims, then for each ask a strong model whether the context entails "
         "it, with the answer justified. This is the standard approach and it "
         "works well, because entailment against a supplied passage is a much "
         "easier task than open-ended judgement.</p>"
         "<p><strong>Natural-language inference models.</strong> A dedicated NLI "
         "classifier scores entailment between context and claim. Cheaper and "
         "faster than a large judge, weaker on long or technical passages.</p>"
         "<p><strong>Citation checking.</strong> Require the model to cite a "
         "chunk id per sentence, then verify the cited chunk actually supports "
         "it. This has the useful property of being auditable by a human in "
         "seconds, and it changes the generator's behaviour for the better even "
         "before you measure anything.</p>"),
        ("What a low score is actually telling you",
         "<p>A groundedness problem is often a retrieval problem wearing a "
         "generation costume. If the context did not contain the answer, a model "
         "asked to answer anyway will fill the gap from memory &mdash; so low "
         "groundedness correlates with low "
         "<a href=\"recall_at_k.html\">recall@k</a>, and the fix is upstream.</p>"
         "<p>The other common cause is a prompt that does not permit abstention. "
         "A model told to \"answer the question using the context\" will answer; "
         "one told \"if the context does not contain the answer, say so\" will "
         "often decline correctly. That single sentence moves groundedness more "
         "than most model changes, and it is why "
         "<a href=\"corrective_rag.html\">corrective RAG</a> treats declining as "
         "a first-class outcome.</p>"
         "<p>Watch for the degenerate optimum, too. An answer that quotes the "
         "context verbatim and says nothing else scores 1.0 on groundedness and "
         "may be useless. Groundedness has to be read next to "
         "<a href=\"completeness_in_llm_evaluation.html\">completeness</a> and "
         "<a href=\"relevance_in_llm_evaluation.html\">relevance</a>, or you "
         "will optimise your way into a system that recites.</p>"),
        ("Things to try",
         "<ol><li>Click the digital-goods claim, which the context does not "
         "support. Groundedness falls while correctness is unaffected &mdash; "
         "the two dimensions move independently.</li>"
         "<li>Flip every claim to supported. Groundedness reaches 1.0 while "
         "relevance and completeness stay where they were: a perfectly grounded "
         "answer can still be padded and incomplete.</li>"
         "<li>Note that the 24/7 phone claim is marked correct but off topic. "
         "True, plausible, and not what was asked &mdash; groundedness alone "
         "would not catch it.</li></ol>"),
        ("What to remember",
         "<p>Groundedness is the proportion of an answer's claims that the "
         "retrieved context actually supports. It is the direct measure of "
         "hallucination, it needs no reference answer, and it is independent of "
         "truth &mdash; a claim can be grounded and wrong, or true and "
         "ungrounded. Measure it per claim rather than per answer so it tells "
         "you which span to look at. A low score usually means a retrieval "
         "failure or a prompt that does not allow the model to decline. Never "
         "optimise it alone, because verbatim quotation scores perfectly.</p>"
         + _SHARED_JUDGE),
    ],
)

_t(
    slug="correctness_in_llm_evaluation",
    group_label="LLM evaluation",
    level="Intermediate",
    title="Correctness in LLM evaluation",
    asked="What is correctness, and why is it the most expensive dimension to "
          "measure?",
    desc="Correctness compares an answer against a reference or the world - the "
         "dimension that needs ground truth, and the one that cannot be inferred "
         "from the retrieved context alone.",
    lead="Is the answer <em>right</em>? <strong>Correctness compares the "
         "answer's claims against a reference answer or against verifiable "
         "fact.</strong> It is the dimension users care about most and the one "
         "that is hardest to automate, because unlike groundedness it cannot be "
         "checked against the context &mdash; it needs a ground truth that "
         "someone has to produce.",
    notice=[
        "Correctness is judged against a reference, not against the context.",
        "A grounded claim can still be wrong if the source document is wrong.",
        "Click claims to see correctness and groundedness diverge.",
    ],
    viz=WIDGETS["correctness_in_llm_evaluation"],
    sections=[
        ("Correct against what, exactly",
         "<p>Correctness is only defined relative to a reference, and choosing "
         "that reference is most of the work:</p>"
         "<p><strong>A written gold answer.</strong> The usual approach. A human "
         "writes the ideal answer per evaluation query and a judge compares. "
         "Precise, and expensive enough that evaluation sets stay small &mdash; "
         "which is why fifty carefully written references beat five hundred "
         "sloppy ones.</p>"
         "<p><strong>A key-facts list.</strong> Rather than prose, the reference "
         "is a set of facts the answer must state. Easier to write, much easier "
         "to judge consistently, and it composes naturally with "
         "<a href=\"completeness_in_llm_evaluation.html\">completeness</a>.</p>"
         "<p><strong>Verifiable computation.</strong> Where the answer is code, "
         "a number or a query, correctness can be executed rather than judged. "
         "This is the gold standard when it is available and it almost never is "
         "for open-ended questions.</p>"),
        ("Why exact match fails, and what replaces it",
         "<p>The obvious automation &mdash; string comparison against the "
         "reference &mdash; fails immediately on natural language. \"14 days\", "
         "\"fourteen days\" and \"two weeks\" are the same answer and share no "
         "characters. Exact match systematically punishes fluent phrasing.</p>"
         "<p>The n-gram metrics inherited from translation (BLEU, ROUGE) are "
         "only a partial improvement: they reward surface overlap, so a wrong "
         "answer phrased like the reference can outscore a right answer phrased "
         "differently. They remain in use because they are cheap and "
         "deterministic, and they should not be trusted as a primary signal for "
         "factual correctness.</p>"
         "<p>What works is claim-level judging: decompose both the answer and "
         "the reference into atomic facts, then check each answer claim against "
         "the reference. That handles paraphrase, gives partial credit, and "
         "tells you <em>which</em> fact was wrong &mdash; which a single "
         "similarity score never will.</p>"),
        ("The failure this dimension exists to catch",
         "<p>The important case is the <strong>grounded but wrong</strong> "
         "answer. The model faithfully reports what a retrieved document says, "
         "and that document is out of date, contradicted by a newer one, or "
         "simply mistaken.</p>"
         "<p>Groundedness scores this perfectly. Relevance scores it perfectly. "
         "The answer is fluent, cited, and misinforms the user. No amount of "
         "prompt engineering fixes it, because the model did exactly what it was "
         "asked; the corpus is the defect.</p>"
         "<p>That makes correctness the dimension that audits your <em>data</em> "
         "rather than your model. When correctness is low while groundedness is "
         "high, stop looking at the pipeline and go and look at the documents: "
         "stale versions, superseded policies, and duplicate chunks disagreeing "
         "with each other are the usual culprits.</p>"),
        ("Judging it without fooling yourself",
         "<p><strong>Show the judge the reference.</strong> A model asked "
         "\"is this answer correct?\" with no ground truth is being asked to "
         "recall the fact itself, and will confidently score wrong answers as "
         "right in exactly the domains where you needed evaluation most.</p>"
         "<p><strong>Ask for partial credit.</strong> Binary correct/incorrect "
         "throws away the difference between an answer with one wrong detail and "
         "one that is entirely wrong. Per-claim scoring gives a proportion.</p>"
         "<p><strong>Calibrate against humans.</strong> Have annotators label a "
         "sample and measure agreement with your judge. If the judge agrees 70% "
         "of the time, a 3-point movement in your correctness score is "
         "noise.</p>"
         "<p><strong>Watch for self-preference.</strong> A judge tends to favour "
         "answers written in its own style, and to prefer longer answers. Both "
         "biases are documented and both inflate scores in ways that have "
         "nothing to do with being right.</p>"),
        ("Things to try",
         "<ol><li>Click the digital-goods claim to mark it supported by the "
         "context. Groundedness rises to 1.0 and correctness does not move "
         "&mdash; it is still contradicted by the reference.</li>"
         "<li>That single claim is the grounded-but-wrong case: cited, "
         "confident, and misinforming. It is why correctness cannot be inferred "
         "from the context.</li>"
         "<li>Compare correctness with completeness. An answer can state only "
         "true things and still omit half of what was asked.</li></ol>"),
        ("What to remember",
         "<p>Correctness compares the answer against a reference or verifiable "
         "fact, which makes it the only one of the four dimensions that requires "
         "ground truth someone has to write. Exact match and n-gram overlap fail "
         "on paraphrase; claim-level judging against a key-facts reference is "
         "what works. Its distinctive value is catching the grounded-but-wrong "
         "answer, where the model faithfully reports a document that is itself "
         "out of date &mdash; a defect in your corpus that every other dimension "
         "scores as a success.</p>" + _SHARED_JUDGE),
    ],
)


_t(
    slug="relevance_in_llm_evaluation",
    group_label="LLM evaluation",
    level="Intermediate",
    title="Relevance in LLM evaluation",
    asked="What is answer relevance, and how does it differ from context "
          "relevance?",
    desc="Relevance measures whether the answer addresses the question that was "
         "actually asked - the dimension that catches padding, hedging and "
         "confident answers to a different question.",
    lead="Does the answer address <em>the question that was asked</em>? "
         "<strong>Relevance measures how much of the answer is on point</strong> "
         "&mdash; and it is the dimension that catches the failure the other "
         "three are blind to: a response that is entirely true, fully grounded, "
         "and quietly about something else.",
    notice=[
        "The 24/7 phone claim is true and grounded and still off topic.",
        "Padding is scored here and nowhere else.",
        "Click claims to see relevance move independently of the rest.",
    ],
    viz=WIDGETS["relevance_in_llm_evaluation"],
    sections=[
        ("Two different things are called relevance",
         "<p>The word is used for two distinct measurements and conflating them "
         "makes evaluation results incomparable.</p>"
         "<p><strong>Context relevance</strong> scores the retrieved chunks "
         "against the query. It is a <em>retrieval</em> metric, closely related "
         "to <a href=\"precision_at_k.html\">precision@k</a>, and it tells you "
         "whether your retriever is sending noise to the generator.</p>"
         "<p><strong>Answer relevance</strong> scores the generated answer "
         "against the query. It is a <em>generation</em> metric, and it is what "
         "this page is about.</p>"
         "<p>They fail independently. Perfect context and an irrelevant answer "
         "means the generator wandered; irrelevant context and a relevant answer "
         "usually means the model answered from memory, which "
         "<a href=\"groundedness_in_llm_evaluation.html\">groundedness</a> will "
         "catch. Always say which one you mean.</p>"),
        ("The failures it exists to catch",
         "<p><strong>Padding.</strong> The answer contains the requested "
         "information plus three paragraphs of adjacent context nobody asked "
         "for. Every claim is true and grounded, and the user has to hunt for "
         "the answer. Models trained to be helpful pad heavily, and no other "
         "dimension penalises it.</p>"
         "<p><strong>Answering a nearby question.</strong> Asked how long "
         "refunds take, the answer explains how to request one. Fluent, "
         "grounded, correct, and not responsive.</p>"
         "<p><strong>Hedging.</strong> Several paragraphs of caveats and "
         "conditions with no actual answer inside them. Technically nothing is "
         "wrong; nothing is useful either.</p>"
         "<p><strong>Restating the question.</strong> The degenerate answer that "
         "echoes the query back. It scores oddly well on naive similarity-based "
         "relevance measures, which is a good reason not to use them.</p>"),
        ("How to measure it without measuring similarity",
         "<p>The tempting approach &mdash; embed the question and the answer and "
         "take cosine similarity &mdash; is bad. It rewards vocabulary overlap, "
         "so restating the question scores highly and a correct answer that "
         "shares no words with the question scores poorly. \"When are refunds "
         "issued?\" answered with \"Within a fortnight of delivery\" is perfect "
         "and lexically distant.</p>"
         "<p>The approach that works is <strong>question generation</strong>: "
         "ask a model to write the questions this answer would be a good "
         "response to, then compare those against the real question. If the "
         "generated questions match, the answer is on point; if they are broader "
         "or different, it is padded or off target. It measures what relevance "
         "actually means rather than a proxy for it.</p>"
         "<p>The alternative is claim-level judging, as in the visualisation "
         "above: split the answer into claims and mark each as responsive or "
         "not. Relevance is then the supported proportion, and you can see "
         "exactly which sentence was padding.</p>"),
        ("The tension with completeness, and how to resolve it",
         "<p>Relevance and "
         "<a href=\"completeness_in_llm_evaluation.html\">completeness</a> pull "
         "in opposite directions, and optimising either alone produces a bad "
         "system.</p>"
         "<p>Maximise relevance alone and answers get terse to the point of "
         "being unhelpful &mdash; every qualification stripped out because "
         "qualifications are not strictly what was asked. Maximise completeness "
         "alone and answers sprawl, because adding material can only help.</p>"
         "<p>The resolution is to score both and watch them together, the same "
         "way precision and recall are read as a pair. An answer that is 0.95 "
         "relevant and 0.6 complete is leaving things out; one that is 0.6 "
         "relevant and 1.0 complete is burying the answer in padding. Neither "
         "single number would tell you which problem you have.</p>"
         "<p>Note also that relevance is the dimension most affected by your "
         "prompt rather than your retrieval. \"Answer in at most three "
         "sentences, addressing only what was asked\" moves it substantially, "
         "and costs nothing.</p>"),
        ("Things to try",
         "<ol><li>The 24/7 phone claim is marked correct but off topic. "
         "Relevance drops while correctness and groundedness stay put &mdash; "
         "this is the padding case, visible only here.</li>"
         "<li>Click that claim to flip its grounding. Groundedness moves and "
         "relevance does not: whether the context supports a claim has nothing "
         "to do with whether it answers the question.</li>"
         "<li>Compare relevance and completeness across the claim list. The "
         "off-topic claim hurts one and does nothing for the other, which is "
         "why they have to be read as a pair.</li></ol>"),
        ("What to remember",
         "<p>Answer relevance measures how much of the answer addresses the "
         "question asked. Distinguish it from context relevance, which scores "
         "retrieved chunks and is a retrieval metric. It is the only dimension "
         "that penalises padding, hedging and confidently answering a nearby "
         "question &mdash; all of which score perfectly on correctness and "
         "groundedness. Do not measure it with question-answer embedding "
         "similarity, which rewards restating the question; use generated "
         "questions or per-claim judging. Read it alongside completeness, "
         "because optimising either alone makes answers worse.</p>"
         + _SHARED_JUDGE),
    ],
)

_t(
    slug="completeness_in_llm_evaluation",
    group_label="LLM evaluation",
    level="Intermediate",
    title="Completeness in LLM evaluation",
    asked="What is completeness, and why can a perfectly correct answer still "
          "fail on it?",
    desc="Completeness measures how much of what the question required the "
         "answer actually covered - the dimension a fluent, correct, grounded "
         "answer can still fail entirely.",
    lead="Did the answer cover <em>everything</em> the question required? "
         "<strong>Completeness measures the proportion of the required points "
         "that the answer actually states.</strong> It is the dimension a "
         "confident, correct, perfectly grounded answer can fail outright "
         "&mdash; and the one users notice last, because a partial answer looks "
         "exactly like a full one until you act on it.",
    notice=[
        "Completeness counts required points covered, not claims made.",
        "Adding true, grounded, on-topic claims does not raise it.",
        "It is the mirror image of relevance &mdash; read them together.",
    ],
    viz=WIDGETS["completeness_in_llm_evaluation"],
    sections=[
        ("Complete relative to what",
         "<p>Completeness is undefined without a statement of what the answer "
         "<em>needed</em> to contain, so the reference is not optional. In "
         "practice that means a <strong>key-points list</strong> per evaluation "
         "query: the facts a good answer must include, written by whoever "
         "understands the domain.</p>"
         "<p>Writing that list is the real work, and it is worth doing carefully "
         "because it is reusable. The same list drives "
         "<a href=\"correctness_in_llm_evaluation.html\">correctness</a> "
         "(are the stated facts right?) and completeness (were they all "
         "stated?), so one artefact serves two dimensions.</p>"
         "<p>It also forces a decision your users have already made "
         "implicitly: is the caveat about digital goods a required point or a "
         "nice-to-have? Teams often discover during this exercise that they do "
         "not agree on what a good answer is, which is more valuable than any "
         "score.</p>"),
        ("Why the other dimensions cannot see it",
         "<p>Consider an answer that states only \"Refunds are issued within 14 "
         "days.\" when the question was about the full refund policy. It is "
         "correct. It is grounded. It is entirely relevant. It scores 1.0 on "
         "three dimensions and leaves out the condition that makes it "
         "actionable.</p>"
         "<p>This asymmetry is the reason completeness is worth measuring "
         "separately. The other three dimensions all penalise <em>saying the "
         "wrong thing</em>. Only completeness penalises <em>not saying the right "
         "thing</em>, and omission is the harder failure to notice, because "
         "there is nothing on the screen to catch your eye.</p>"
         "<p>It is also the failure with the worst consequences in practice. A "
         "user who reads a wrong answer may check it. A user who reads a partial "
         "answer has no signal that anything is missing and acts on it.</p>"),
        ("Where incompleteness comes from",
         "<p><strong>Retrieval, most often.</strong> If a required point was "
         "never in the retrieved context, the model cannot state it without "
         "hallucinating. Low completeness alongside low "
         "<a href=\"recall_at_k.html\">recall@k</a> is a retrieval problem, and "
         "no prompt change will fix it. This is the single most common "
         "cause.</p>"
         "<p><strong>Chunking.</strong> A policy split across two chunks where "
         "only one was retrieved gives a confidently half-right answer &mdash; "
         "which is exactly what "
         "<a href=\"parent_document_retriever.html\">parent-document "
         "retrieval</a> and generous chunk overlap exist to prevent.</p>"
         "<p><strong>Length limits.</strong> A max-tokens cap or a \"be "
         "concise\" instruction trades completeness for brevity, usually without "
         "anyone deciding to.</p>"
         "<p><strong>The model stopping early.</strong> Given ten chunks, models "
         "reliably use the first few more than the rest. A required point in "
         "chunk eight is retrieved, in context, and still absent from the answer "
         "&mdash; which is why <a href=\"mean_reciprocal_rank.html\">MRR</a> is "
         "worth tracking next to recall.</p>"),
        ("Measuring it, and the trap in optimising it",
         "<p>The measurement is mechanical once the key-points list exists: for "
         "each required point, ask a judge whether the answer states it, and "
         "take the proportion. Per point rather than per answer, so the output "
         "tells you <em>which</em> point was dropped &mdash; that is the "
         "actionable part.</p>"
         "<p>The trap is that completeness is trivially gamed by verbosity. An "
         "answer that dumps the entire retrieved context scores 1.0. If "
         "completeness is the only dimension you optimise, you will get long, "
         "hedged, exhaustive answers that score beautifully and that nobody "
         "wants to read.</p>"
         "<p>Which is why it is read against "
         "<a href=\"relevance_in_llm_evaluation.html\">relevance</a>. The pair "
         "behaves like precision and recall: completeness is the recall of "
         "required information, relevance is its precision, and a system is only "
         "good when both are high. Reporting either alone is the same mistake as "
         "reporting recall without k.</p>"),
        ("Things to try",
         "<ol><li>Three of the five claims are required points and the "
         "reference lists four. Completeness is 0.75 &mdash; one required point "
         "is simply absent from the answer.</li>"
         "<li>Click the off-topic phone claim on and off. Completeness does not "
         "move at all: adding material that was not required cannot improve "
         "it.</li>"
         "<li>Compare with relevance on the same claim list. The claims that "
         "hurt relevance are exactly the ones completeness ignores, which is why "
         "the pair has to be read together.</li></ol>"),
        ("What to remember",
         "<p>Completeness is the proportion of required points an answer "
         "actually states, and it needs a key-points reference to be defined at "
         "all. It is the one dimension that penalises omission rather than "
         "error, which makes it the failure users notice last and act on "
         "first. Low completeness is usually a retrieval or chunking problem "
         "rather than a generation one. Measure it per point so you know what "
         "was dropped, and always read it against relevance &mdash; optimised "
         "alone it rewards dumping the entire context into the answer.</p>"
         + _SHARED_JUDGE),
    ],
)
