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

from interview_viz import frame, marked, pairs, viz

TOPICS = []


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


ART = {"Retrieval": _art_retrieval, "Chunking": _art_chunking,
       "Caching": _art_cache, "Scale": _art_scale}


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

def _tfidf_frames():
    docs = ["the cat sat on the mat", "the dog sat on the log",
            "quantum entanglement in the lab"]
    out = [frame(pairs([("doc %d" % i, d) for i, d in enumerate(docs)], {},
                       label="corpus"),
                 "Three documents. 'the' is in all of them; 'quantum' is in one.",
                 {"docs": 3})]
    out.append(frame(pairs([("the", "in 3 of 3 docs -> idf 0.00"),
                            ("sat", "in 2 of 3 docs -> idf 0.18"),
                            ("quantum", "in 1 of 3 docs -> idf 0.48")],
                           {"quantum": "hit", "the": "bad"},
                           label="inverse document frequency"),
                     "A term in every document carries no information, so its "
                     "idf is zero. A rare term scores high.",
                     {"docs": 3}))
    out.append(frame(pairs([("tf('the', doc0)", "2 occurrences"),
                            ("x idf('the')", "x 0.00"),
                            ("= weight", "0.00")],
                           {"= weight": "bad"}, label="frequent term"),
                     "'the' appears twice and still contributes nothing. The "
                     "multiplication is what cancels it.",
                     {"docs": 3}))
    out.append(frame(pairs([("tf('quantum', doc2)", "1 occurrence"),
                            ("x idf('quantum')", "x 0.48"),
                            ("= weight", "0.48")],
                           {"= weight": "hit"}, label="rare term"),
                     "One occurrence of a rare term outweighs two of a common "
                     "one. That is the whole idea.",
                     {"docs": 3}))
    return viz(out)


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
    viz=_tfidf_frames(),
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
    ],
    code={
        "file": "tf_idf.py",
        "intro": "TF-IDF built from scratch on a small corpus, with the idf of "
                 "each term printed so the stopword cancellation is visible, and "
                 "a query ranked against the documents.",
        "code": '''# TF-IDF from scratch: frequent here, rare everywhere else.
import math
from collections import Counter

corpus = [
    "the cat sat on the mat",
    "the dog sat on the log",
    "the cat chased the dog",
    "quantum entanglement in the lab",
]
docs = [d.split() for d in corpus]
N = len(docs)

# --- document frequency: how many documents contain each term ----------
df = Counter()
for words in docs:
    for term in set(words):
        df[term] += 1

def idf(term):
    return math.log(N / df[term]) if df[term] else 0.0

print(f"{'term':>14} {'df':>4} {'idf':>7}")
for term in ["the", "sat", "cat", "quantum"]:
    print(f"{term:>14} {df[term]:>4} {idf(term):>7.3f}")
print("'the' is in every document, so log(N/N) = 0 - it cancels itself out.")

# --- tf-idf for one document -------------------------------------------
def tf_idf(words):
    counts = Counter(words)
    return {t: (1 + math.log(n)) * idf(t) for t, n in counts.items()}

print()
print("weights for", corpus[0])
for term, weight in sorted(tf_idf(docs[0]).items(), key=lambda kv: -kv[1]):
    print(f"  {term:>6}: {weight:>6.3f}")

# --- ranking a query ---------------------------------------------------
def score(query, words):
    weights = tf_idf(words)
    return sum(weights.get(t, 0.0) for t in query.split())

print()
for query in ("cat", "the", "quantum lab"):
    ranked = sorted(((score(query, d), corpus[i]) for i, d in enumerate(docs)),
                    reverse=True)
    print(f"query {query!r}:")
    for s, text in ranked[:2]:
        print(f"    {s:>6.3f}  {text}")

print()
print("Querying 'the' scores every document at 0.000 - the ranking is")
print("undefined, and correctly so: the word distinguishes nothing.")
''',
        "walk": [
            ("math.log(N / df[term])",
             "The inverse document frequency. When a term is in every document "
             "the ratio is 1 and the log is 0, so stopwords are removed by "
             "arithmetic rather than by a list."),
            ("(1 + math.log(n))",
             "Damped term frequency. Twenty occurrences are not twenty times as "
             "relevant, and without the damping one repeated word dominates a "
             "document's whole vector."),
            ("sum(weights.get(t, 0.0) for t in query.split())",
             "The query's score is the sum of the matching terms' weights. "
             "Nothing about word meaning enters into it &mdash; a synonym scores "
             "zero."),
            ("querying 'the'",
             "Every document scores 0.000. That is the correct answer to a "
             "query that carries no information, and it is what dense retrieval "
             "handles differently."),
        ],
        "try": [
            "Add a fifth document that repeats \"cat\" ten times. Its score "
            "climbs without bound &mdash; the saturation BM25 adds is what stops "
            "that.",
            "Search for a synonym: <code>\"feline\"</code> scores zero "
            "everywhere. That single line is the argument for dense retrieval "
            "alongside it.",
        ],
    },
    check=[
        {"q": "Why does a word appearing in every document score zero?",
         "options": ["It is filtered by a stopword list",
                     "log(N / df) is log(1) = 0 when df equals N",
                     "Term frequency is capped", "It is a rounding artefact"],
         "answer": 1,
         "why": "The maths removes stopwords without a per-language list, which "
                "is one of TF-IDF's neatest properties."},
        {"q": "What does BM25 add that plain TF-IDF lacks?",
         "options": ["Word meaning", "Saturating term frequency and tunable "
                     "length normalisation",
                     "Faster indexing", "Support for multiple languages"],
         "answer": 1,
         "why": "The tenth occurrence of a term should add much less than the "
                "second, and long documents should not win by containing more "
                "of everything."},
        {"q": "Why keep a lexical scorer in a modern RAG pipeline?",
         "options": ["It is cheaper", "Exact terms - error codes, identifiers, "
                     "rare jargon - are where embeddings are weakest",
                     "It handles longer documents", "It needs no index"],
         "answer": 1,
         "why": "A vector-only pipeline reliably fails on queries like 'error "
                "TS2345'. It is also the honest baseline for evaluating a dense "
                "retriever."},
    ],
)


def _corrective_frames():
    out = [frame(pairs([("query", "who wrote the 2019 safety memo?"),
                        ("retrieved 1", "score 0.31  (off topic)"),
                        ("retrieved 2", "score 0.28  (off topic)")],
                       {"retrieved 1": "bad", "retrieved 2": "bad"},
                       label="first retrieval"),
                 "Retrieval returned something, as it always does. Nothing here "
                 "is relevant - but naive RAG would answer from it anyway.",
                 {"grade": "-", "action": "-"})]
    out.append(frame(pairs([("grader verdict", "INCORRECT"),
                            ("confidence", "0.31 - below threshold"),
                            ("action", "discard and rewrite the query")],
                           {"grader verdict": "bad", "action": "hit"},
                           label="grade the evidence"),
                     "The corrective step: judge the retrieved documents BEFORE "
                     "generating. Low relevance triggers a different path.",
                     {"grade": "incorrect", "action": "rewrite"}))
    out.append(frame(pairs([("rewritten", "2019 internal security policy author"),
                            ("retrieved 1", "score 0.79  (on topic)"),
                            ("grader verdict", "CORRECT")],
                           {"retrieved 1": "hit", "grader verdict": "hit"},
                           label="second retrieval"),
                     "Rewritten query, better evidence, grader satisfied. Only "
                     "now does generation happen.",
                     {"grade": "correct", "action": "generate"}))
    out.append(frame(pairs([("all retrievals fail", "-> web search fallback"),
                            ("still nothing", "-> say 'I don't know'"),
                            ("never", "-> answer from bad evidence")],
                           {"never": "bad"}, label="the escape hatches"),
                     "The point is having a path that is not 'answer anyway'. "
                     "Abstaining is a valid outcome.",
                     {"grade": "ambiguous", "action": "fallback"}))
    return viz(out)


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
    viz=_corrective_frames(),
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
    ],
    code={
        "file": "corrective_rag.py",
        "intro": "A miniature pipeline with a similarity threshold as the "
                 "grader, run over queries that hit, miss and partly match, so "
                 "you can watch naive RAG answer from evidence the corrective "
                 "version rejects.",
        "code": '''# Corrective RAG: grade the evidence before you generate from it.

CORPUS = {
    "doc1": "The 2019 internal security policy was authored by Priya Nair.",
    "doc2": "Quarterly revenue for 2019 grew by eleven percent.",
    "doc3": "The office relocated to the Bristol site in March 2021.",
}

def similarity(query, text):
    """Stand-in for an embedding model: overlap of the words involved."""
    q, t = set(query.lower().split()), set(text.lower().split())
    return len(q & t) / len(q | t) if q | t else 0.0


def retrieve(query, k=2):
    scored = sorted(((similarity(query, t), name, t)
                     for name, t in CORPUS.items()), reverse=True)
    return scored[:k]


def grade(results, good=0.20, poor=0.10):
    """Correct / ambiguous / incorrect, from the best score available."""
    best = results[0][0] if results else 0.0
    if best >= good:
        return "correct"
    if best >= poor:
        return "ambiguous"
    return "incorrect"


def rewrite(query):
    """A real system asks an LLM. This maps user words to corpus words."""
    swaps = {"memo": "policy", "wrote": "authored", "who": ""}
    return " ".join(swaps.get(w, w) for w in query.lower().split()).strip()


def naive_rag(query):
    results = retrieve(query)
    return f"answered from {results[0][1]} (score {results[0][0]:.2f})"


def corrective_rag(query, depth=0):
    results = retrieve(query)
    verdict = grade(results)
    print(f"    retrieve {query!r} -> best {results[0][0]:.2f} [{verdict}]")

    if verdict == "correct":
        keep = [r for r in results if r[0] >= 0.20]     # drop the distractors
        return f"answered from {[r[1] for r in keep]}"
    if depth == 0:
        rewritten = rewrite(query)
        if rewritten != query:
            print(f"    rewriting -> {rewritten!r}")
            return corrective_rag(rewritten, depth + 1)
    if verdict == "ambiguous":
        return "answered from partial evidence, flagged as low confidence"
    return "declined: nothing relevant in the corpus"


for query in ["who wrote the 2019 security memo",
              "what was 2019 revenue",
              "what is the capital of Peru"]:
    print(f"query: {query!r}")
    print("  naive     :", naive_rag(query))
    print("  corrective:", corrective_rag(query))
    print()

print("The last query has no answer in the corpus. Naive RAG still cites a")
print("document; the corrective pipeline declines, which is the correct output.")
''',
        "walk": [
            ("grade(results)",
             "The step naive RAG lacks entirely. It runs between retrieval and "
             "generation, and its verdict decides which path the query takes."),
            ("if verdict == \"correct\": keep = [r for r in results if ...]",
             "Even on the good path the low-scoring documents are dropped. "
             "Irrelevant context measurably degrades generation, so passing all "
             "k through is a mistake of its own."),
            ("return corrective_rag(rewritten, depth + 1)",
             "One retry, not unlimited. Without the depth guard a query the "
             "rewriter cannot fix loops, and each iteration costs a retrieval "
             "and a model call."),
            ("\"declined: nothing relevant in the corpus\"",
             "The output naive RAG cannot produce. Abstaining is a valid answer, "
             "and a system without that path will always fabricate instead."),
        ],
        "try": [
            "Raise the <code>good</code> threshold to 0.5. More queries take the "
            "corrective path &mdash; grading is a precision/recall trade like "
            "any other classifier.",
            "Remove the <code>depth</code> guard and query something absent. The "
            "rewrite loop is the failure mode this parameter prevents.",
        ],
    },
    check=[
        {"q": "What failure is corrective RAG designed to prevent?",
         "options": ["Slow retrieval", "Generating a confident answer from "
                     "documents that are not relevant",
                     "Running out of context window", "Duplicate chunks"],
         "answer": 1,
         "why": "Vector search always returns its k nearest chunks, so a query "
                "with no good match still produces fluent, sourced-looking "
                "nonsense."},
        {"q": "Where does the grader run?",
         "options": ["Before retrieval", "Between retrieval and generation",
                     "After generation", "During indexing"],
         "answer": 1,
         "why": "That position is the whole design: it can still change what "
                "happens, which a post-generation check cannot."},
        {"q": "Which corrective action do implementations most often omit?",
         "options": ["Query rewriting", "Abstaining - answering that the "
                     "information is not available",
                     "Web search fallback", "Reranking"],
         "answer": 1,
         "why": "A pipeline with no way to decline will always fabricate "
                "instead, which is worse than an unhelpful but honest answer."},
    ],
)


# --------------------------------------------------------------------------

CHECKS = {
    "gen_ai/%s.html" % t["slug"]: {"check": t["check"]}
    for t in TOPICS if t.get("check")
}


# =========================================================================
# Caching
# =========================================================================

def _qkv_frames():
    out = [frame(pairs([("token", "'sat'"),
                        ("query  (Q)", "what am I looking for?"),
                        ("key    (K)", "what do I offer to others?"),
                        ("value  (V)", "what do I actually pass on?")],
                       {"query  (Q)": "hit"}, label="three projections of one token"),
                 "Every token produces all three, from three learned weight "
                 "matrices applied to the same embedding.",
                 {"tokens": 1})]
    out.append(frame(pairs([("Q('sat') . K('cat')", "8.2  -> high"),
                            ("Q('sat') . K('the')", "1.1  -> low"),
                            ("Q('sat') . K('mat')", "3.4  -> medium")],
                           {"Q('sat') . K('cat')": "hit", "Q('sat') . K('the')": "bad"},
                           label="scores: query against every key"),
                     "The dot product of one query with every key is the "
                     "attention score. 'sat' is looking for its subject.",
                     {"tokens": 4}))
    out.append(frame(pairs([("softmax", "cat 0.71, mat 0.21, the 0.08"),
                            ("output", "0.71*V(cat) + 0.21*V(mat) + 0.08*V(the)")],
                           {"output": "hit"}, label="weights, then a weighted sum"),
                     "Softmax turns scores into weights that sum to 1, and the "
                     "output is the weighted sum of the VALUES - not the keys.",
                     {"tokens": 4}))
    out.append(frame(pairs([("K and V", "depend only on past tokens -> CACHEABLE"),
                            ("Q", "is new for the token being generated"),
                            ("consequence", "the KV cache")],
                           {"K and V": "hit", "consequence": "done"},
                           label="why this matters at serving time"),
                     "K and V for a token never change once computed. That single "
                     "fact is what makes generation O(n) instead of O(n^2).",
                     {"tokens": 4}))
    return viz(out)


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
    viz=_qkv_frames(),
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
    ],
    code={
        "file": "qkv.py",
        "intro": "Attention computed by hand on a four-token sentence, with the "
                 "score matrix and the softmax weights printed, then the same "
                 "computation done twice to show K and V are identical the "
                 "second time &mdash; which is the cache's whole premise.",
        "code": '''# Q, K and V: three projections, two roles, one weighted sum.
import math

# Four tokens, three dimensions each. Real models use thousands.
EMBED = {
    "the": [0.1, 0.0, 0.2],
    "cat": [0.9, 0.2, 0.1],
    "sat": [0.2, 0.8, 0.3],
    "mat": [0.7, 0.1, 0.6],
}
tokens = ["the", "cat", "sat", "mat"]

# Three DIFFERENT learned matrices. That they differ is the whole point.
W_Q = [[1.0, 0.2, 0.0], [0.0, 0.9, 0.1], [0.1, 0.0, 0.8]]
W_K = [[0.8, 0.0, 0.3], [0.2, 1.0, 0.0], [0.0, 0.1, 0.9]]
W_V = [[0.5, 0.5, 0.0], [0.0, 0.6, 0.4], [0.3, 0.0, 0.7]]

def project(vec, matrix):
    return [sum(vec[i] * matrix[i][j] for i in range(len(vec)))
            for j in range(len(matrix[0]))]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def softmax(scores):
    top = max(scores)
    exps = [math.exp(s - top) for s in scores]        # shift: avoids overflow
    total = sum(exps)
    return [e / total for e in exps]


Q = {t: project(EMBED[t], W_Q) for t in tokens}
K = {t: project(EMBED[t], W_K) for t in tokens}
V = {t: project(EMBED[t], W_V) for t in tokens}

focus = "sat"
d = len(Q[focus])
scores = [dot(Q[focus], K[t]) / math.sqrt(d) for t in tokens]
weights = softmax(scores)

print(f"attention from {focus!r}:")
print(f"{'token':>6} {'Q.K/sqrt(d)':>12} {'weight':>8}")
for t, s, w in zip(tokens, scores, weights):
    print(f"{t:>6} {s:>12.3f} {w:>8.3f}")
print("weights sum to", round(sum(weights), 6))

output = [sum(w * V[t][i] for t, w in zip(tokens, weights)) for i in range(d)]
print()
print("output = weighted sum of the VALUES:", [round(x, 3) for x in output])
print("Note it uses V, not K. Keys decide attention; values carry content.")

# --- why K and V are cacheable -----------------------------------------
print()
first_pass = {t: (K[t], V[t]) for t in tokens}
second_pass = {t: (project(EMBED[t], W_K), project(EMBED[t], W_V)) for t in tokens}
print("K and V recomputed for the same tokens are identical:",
      first_pass == second_pass)
print("They depend only on the token and the weights, never on what comes")
print("after - which is precisely why they can be cached across steps.")

# --- what separate Q and K buys ----------------------------------------
print()
same = [dot(EMBED[focus], EMBED[t]) for t in tokens]
print("if a token searched with its own embedding:", [round(s, 2) for s in same])
print("with separate Q and K projections        :", [round(s, 2) for s in scores])
print("The first is just self-similarity. The second can learn to look for")
print("something different from itself - a verb seeking its subject.")
''',
        "walk": [
            ("W_Q, W_K, W_V",
             "Three different matrices applied to the same embedding. If they "
             "were one matrix, attention would reduce to similarity and a token "
             "could only attend to tokens like itself."),
            ("dot(Q[focus], K[t]) / math.sqrt(d)",
             "The score. The division by &radic;d keeps the values small enough "
             "that softmax stays in its responsive range &mdash; without it "
             "large dimensions saturate it and gradients vanish."),
            ("output uses V[t], not K[t]",
             "Keys decide <em>how much</em> to attend; values decide "
             "<em>what</em> is contributed. Collapsing them would tie relevance "
             "to content."),
            ("first_pass == second_pass",
             "K and V for a token depend only on that token and the fixed "
             "weights. Recomputing gives the identical result, which is the "
             "argument for the KV cache in one line."),
        ],
        "try": [
            "Set <code>W_Q = W_K</code> and re-run. A token now attends most "
            "strongly to itself, which is what the separate projections exist to "
            "avoid.",
            "Remove the <code>/ sqrt(d)</code> and scale the embeddings up by "
            "ten. The softmax collapses to nearly one-hot &mdash; the saturation "
            "the scaling prevents.",
        ],
    },
    check=[
        {"q": "The output of attention is a weighted sum of:",
         "options": ["The keys", "The values", "The queries", "The raw embeddings"],
         "answer": 1,
         "why": "Keys decide how much to attend; values are what gets "
                "contributed. Separating the two lets relevance and content be "
                "learned independently."},
        {"q": "Why are Q, K and V three separate projections rather than one "
              "vector?",
         "options": ["For speed", "So a token can look for something different "
                     "from itself",
                     "To reduce memory", "To allow multiple heads"],
         "answer": 1,
         "why": "With one vector, attention collapses into self-similarity. A "
                "verb could not learn to seek its subject."},
        {"q": "What makes the KV cache possible?",
         "options": ["Keys and values are small", "K and V for a token depend "
                     "only on that token, so they never change",
                     "Queries are cached too", "The softmax is deterministic"],
         "answer": 1,
         "why": "Each depends only on tokens up to that point, so once computed "
                "they are fixed - turning generation from quadratic into linear."},
    ],
)


def _cache_layers_frames():
    out = [frame(pairs([("prompt cache", "the model's KV for a shared prefix"),
                        ("query cache", "a finished answer, keyed on the question"),
                        ("embedding cache", "a vector, keyed on the text")],
                       {}, label="three different caches, three different keys"),
                 "All three are called 'caching' and none of them caches the "
                 "same thing. The key tells them apart.",
                 {"layer": "-"})]
    out.append(frame(pairs([("request", "'what is our refund policy?'"),
                            ("embedding cache", "MISS -> embed (18ms)"),
                            ("query cache", "MISS -> full pipeline (2.4s)")],
                           {"embedding cache": "bad", "query cache": "bad"},
                           label="cold: nothing is cached"),
                     "First time. Everything is computed, and the total is the "
                     "sum of every stage.",
                     {"layer": "cold", "ms": 2400}))
    out.append(frame(pairs([("request", "'what is our refund policy?'"),
                            ("query cache", "HIT -> return stored answer (3ms)")],
                           {"query cache": "hit"}, label="exact repeat"),
                     "The same question again. The query cache short-circuits "
                     "the entire pipeline - retrieval, generation, all of it.",
                     {"layer": "query", "ms": 3}))
    out.append(frame(pairs([("request", "'how do refunds work?'"),
                            ("query cache", "MISS - different wording"),
                            ("embedding cache", "MISS - different text"),
                            ("prompt cache", "HIT on the shared system prefix")],
                           {"prompt cache": "hit"}, label="similar, not identical"),
                     "Different wording defeats the exact-match caches, and the "
                     "prompt cache still helps because the system prompt is "
                     "unchanged.",
                     {"layer": "prompt", "ms": 900}))
    return viz(out)


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
    viz=_cache_layers_frames(),
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
    ],
    code={
        "file": "rag_caching.py",
        "intro": "A pipeline with all three caches and simulated stage timings, "
                 "run over a realistic traffic pattern so each cache's hit rate "
                 "and saving are counted &mdash; including the staleness the "
                 "query cache introduces when a document changes.",
        "code": '''# Three caches, three keys, three different things saved.
import hashlib

COST_MS = {"embed": 18, "retrieve": 120, "rerank": 210, "generate": 2100}
FULL = sum(COST_MS.values())

docs = {"refunds": "Refunds are issued within 14 days."}

embedding_cache, query_cache = {}, {}
stats = {"embed_hits": 0, "query_hits": 0, "prompt_hits": 0, "ms": 0}
seen_prefixes = set()

SYSTEM_PROMPT = "You are a support assistant. Answer only from the documents."


def key(text, model="embed-v1"):
    return hashlib.sha256(f"{model}:{text}".encode()).hexdigest()[:12]


def embed(text):
    k = key(text)
    if k in embedding_cache:
        stats["embed_hits"] += 1
        return embedding_cache[k], 0
    embedding_cache[k] = [len(text) % 7, len(set(text)) % 5]
    return embedding_cache[k], COST_MS["embed"]


def answer(question):
    # 1. query cache: keyed on the question, skips everything
    qk = key(question, "query")
    if qk in query_cache:
        stats["query_hits"] += 1
        stats["ms"] += 3
        return query_cache[qk], 3

    spent = 0
    _, embed_ms = embed(question)              # 2. embedding cache
    spent += embed_ms
    spent += COST_MS["retrieve"] + COST_MS["rerank"]

    # 3. prompt cache: provider-side, and only for a shared PREFIX
    if SYSTEM_PROMPT in seen_prefixes:
        stats["prompt_hits"] += 1
        spent += int(COST_MS["generate"] * 0.55)   # prefill largely skipped
    else:
        seen_prefixes.add(SYSTEM_PROMPT)
        spent += COST_MS["generate"]

    result = f"answer about {list(docs)[0]}"
    query_cache[qk] = result
    stats["ms"] += spent
    return result, spent


traffic = ["what is the refund policy",
           "what is the refund policy",       # exact repeat
           "how do refunds work",             # same intent, different words
           "what is the refund policy",
           "how do refunds work"]

print(f"{'request':>28} {'ms':>7}  cache")
for q in traffic:
    before = dict(stats)
    _, ms = answer(q)
    hit = ("query" if stats["query_hits"] > before["query_hits"]
           else "prompt" if stats["prompt_hits"] > before["prompt_hits"]
           else "cold")
    print(f"{q:>28} {ms:>7}  {hit}")

print()
print(f"uncached total would be : {FULL * len(traffic):,} ms")
print(f"actual total            : {stats['ms']:,} ms")
print(f"query cache hits        : {stats['query_hits']}/{len(traffic)}")
print(f"prompt cache hits       : {stats['prompt_hits']}/{len(traffic)}")

# --- the invalidation problem ------------------------------------------
print()
docs["refunds"] = "Refunds are issued within 30 days."     # the policy changed
cached, _ = answer("what is the refund policy")
print("document updated to 30 days; cached answer still served:", cached)
print("Nothing in the query cache knows a document changed. A TTL or an")
print("explicit flush on re-index is the only practical defence.")
''',
        "walk": [
            ("key(text, model=\"embed-v1\")",
             "The model goes in the cache key. Vectors from two models are not "
             "comparable, and a cache that mixes them returns results that look "
             "plausible and mean nothing."),
            ("if qk in query_cache",
             "The query cache short-circuits the whole pipeline &mdash; "
             "retrieval, reranking and generation. The largest saving and the "
             "riskiest cache, because it stores a conclusion rather than an "
             "input."),
            ("if SYSTEM_PROMPT in seen_prefixes",
             "Prompt caching is prefix-based. It only helps when the shared text "
             "comes first, which is why the system prompt goes at the front and "
             "the retrieved chunks after it."),
            ("docs[\"refunds\"] = ... then answer(...)",
             "The staleness problem, demonstrated. The document changed and the "
             "cache has no idea; a TTL or a flush on re-index is the only "
             "practical defence."),
        ],
        "try": [
            "Add a semantic query cache: embed the question and accept a hit "
            "above a similarity threshold. The hit rate rises and so does the "
            "risk of answering a subtly different question.",
            "Move <code>SYSTEM_PROMPT</code> to the end of the prompt. Prefix "
            "caching stops firing entirely &mdash; order is the whole "
            "constraint.",
        ],
    },
    check=[
        {"q": "Which cache saves the most per hit, and carries the most risk?",
         "options": ["Embedding cache", "Query cache", "Prompt cache",
                     "They are equivalent"],
         "answer": 1,
         "why": "It skips retrieval, reranking and generation - but it stores a "
                "conclusion, so any document change can silently invalidate it."},
        {"q": "Why must the embedding model be part of the embedding cache key?",
         "options": ["To save space", "Vectors from different models are not "
                     "comparable",
                     "Models expire", "For auditing"],
         "answer": 1,
         "why": "Mixing them produces retrieval results that look plausible and "
                "are meaningless."},
        {"q": "Prompt caching only helps when the shared text is:",
         "options": ["Short", "At the start of the prompt", "Repeated verbatim "
                     "anywhere", "Below the token limit"],
         "answer": 1,
         "why": "It caches attention state for a prefix, so putting the variable "
                "part first defeats it entirely."},
    ],
)
