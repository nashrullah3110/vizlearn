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


# =========================================================================
# Chunking
# =========================================================================

TEXT = ("# Refund policy\n\nRefunds are issued within 14 days of purchase. "
        "The item must be unused.\n\n## Exceptions\n\nDigital goods are "
        "non-refundable once downloaded.")


def _chunk_frames(rows, note_first, note_last):
    out = [frame(pairs([("source", TEXT[:52] + "...")], {}, label="input"),
                 note_first, {"chunks": 0})]
    for i, (label, body) in enumerate(rows):
        out.append(frame(pairs(rows[:i + 1], {rows[i][0]: "hit"},
                               label="chunks so far"),
                         "%s -> %s" % (label, body[:64]),
                         {"chunks": i + 1}))
    out.append(frame(pairs(rows, {r[0]: "done" for r in rows}, label="result"),
                     note_last, {"chunks": len(rows)}))
    return viz(out)


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
    viz=_chunk_frames(
        [("chunk 1", "# Refund policy / Refunds are issued within 14 days..."),
         ("chunk 2", "## Exceptions / Digital goods are non-refundable...")],
        "Recursive splitting starts with the largest separator and only "
        "descends when a piece is still over the limit.",
        "Two chunks, both broken at paragraph boundaries. Nothing was cut "
        "mid-sentence."),
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
    ],
    code={
        "file": "recursive_chunking.py",
        "intro": "A recursive splitter written out in full, run against a "
                 "fixed-size splitter on the same text so you can see which one "
                 "cuts mid-sentence, plus what overlap adds to the index.",
        "code": '''# Recursive chunking: split on the biggest separator that fits.

TEXT = """# Refund policy

Refunds are issued within 14 days of purchase. The item must be unused and in
its original packaging. Shipping costs are not refunded.

## Exceptions

Digital goods are non-refundable once downloaded."""

SEPARATORS = ["\\n\\n", "\\n", ". ", " ", ""]     # largest to smallest


def recursive_split(text, limit=120, separators=None):
    separators = SEPARATORS if separators is None else separators
    if len(text) <= limit:
        return [text]
    for i, sep in enumerate(separators):
        if sep == "":
            return [text[j:j + limit] for j in range(0, len(text), limit)]
        parts = text.split(sep)
        if len(parts) == 1:
            continue                              # this separator is absent
        out, buffer = [], ""
        for part in parts:
            candidate = (buffer + sep + part) if buffer else part
            if len(candidate) <= limit:
                buffer = candidate
            else:
                if buffer:
                    out.append(buffer)
                # still too big on its own: fall to the next separator down
                buffer = part if len(part) <= limit else None
                if buffer is None:
                    out.extend(recursive_split(part, limit, separators[i + 1:]))
                    buffer = ""
        if buffer:
            out.append(buffer)
        return out
    return [text]


def fixed_split(text, limit=120):
    return [text[i:i + limit] for i in range(0, len(text), limit)]


print("recursive:")
for i, c in enumerate(recursive_split(TEXT)):
    print(f"  [{i}] {len(c):>3} chars | {c.strip()[:58]!r}")

print()
print("fixed size:")
for i, c in enumerate(fixed_split(TEXT)):
    print(f"  [{i}] {len(c):>3} chars | {c.strip()[:58]!r}")

print()
print("The fixed splitter cuts wherever it lands. Look at where chunk 1 begins.")

# --- overlap, and what it costs ----------------------------------------
def with_overlap(chunks, overlap=25):
    out = []
    for i, c in enumerate(chunks):
        tail = chunks[i - 1][-overlap:] if i else ""
        out.append((tail + c).strip())
    return out

base = recursive_split(TEXT)
overlapped = with_overlap(base)
print()
print(f"chunks           : {len(base)}")
print(f"characters stored: {sum(len(c) for c in base)} without overlap, "
      f"{sum(len(c) for c in overlapped)} with")
print("Overlap buys boundary safety and inflates the index. 10-20% is typical.")
''',
        "walk": [
            ("for i, sep in enumerate(separators)",
             "The priority list. Each level is only reached when the level above "
             "left a piece over the limit, so most chunks break at paragraphs."),
            ("recursive_split(part, limit, separators[i + 1:])",
             "The recursion: a single part that is still too large is re-split "
             "with the remaining, smaller separators. Passing the tail of the "
             "list is what stops it retrying a separator that already failed."),
            ("if sep == \"\": return [text[j:j + limit] ...]",
             "The last resort, and the only branch that cuts mid-word. It fires "
             "only on text with no whitespace &mdash; a base64 blob, a minified "
             "file."),
            ("with_overlap",
             "Boundary insurance at the cost of index size and near-duplicate "
             "chunks competing in the results. 10&ndash;20% is the usual "
             "compromise."),
        ],
        "try": [
            "Set <code>limit=40</code>. More pieces fall through to sentence and "
            "word level &mdash; watch the recursion descend.",
            "Replace the separator list with code-aware ones "
            "(<code>\"\\nclass \"</code>, <code>\"\\ndef \"</code>) and feed it "
            "a Python file. Same splitter, far better chunks.",
        ],
    },
    check=[
        {"q": "Recursive chunking descends to the next separator when:",
         "options": ["Every time", "A piece is still larger than the limit",
                     "The text contains headings", "Overlap is enabled"],
         "answer": 1,
         "why": "Each fallback loses a little more meaning, so it only happens "
                "when the larger boundary failed to get under the size limit."},
        {"q": "The cheapest large improvement to a recursive splitter is usually:",
         "options": ["A bigger chunk size", "Tailoring the separator list to the "
                     "document type",
                     "More overlap", "A better embedding model"],
         "answer": 1,
         "why": "Code, Markdown and prose have different natural boundaries, and "
                "the separator list is almost always left at the default."},
        {"q": "The cost of chunk overlap is:",
         "options": ["Slower retrieval only", "A larger index, and near-duplicate "
                     "chunks competing in the results",
                     "Lost sentences", "Nothing"],
         "answer": 1,
         "why": "Duplicated text can crowd out genuinely different chunks in the "
                "top-k, which is why 10-20% is the usual ceiling."},
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
    viz=viz([
        frame(pairs([("s1 -> s2", "0.81  same topic"),
                     ("s2 -> s3", "0.78  same topic"),
                     ("s3 -> s4", "0.24  TOPIC CHANGE"),
                     ("s4 -> s5", "0.85  same topic")],
                    {"s3 -> s4": "hit"}, label="similarity between neighbours"),
              "Embed each sentence, then compare each with the next. The drop is "
              "the signal.",
              {"sentences": 5}),
        frame(pairs([("chunk 1", "s1 s2 s3"), ("chunk 2", "s4 s5")],
                    {"chunk 1": "done", "chunk 2": "done"}, label="split at the trough"),
              "Two chunks of unequal length, each internally coherent. A "
              "fixed-size splitter would have cut inside one of them.",
              {"sentences": 5}),
        frame(pairs([("cost", "one embedding per sentence, at index time"),
                     ("benefit", "coherent chunks, fewer split answers"),
                     ("when", "long unstructured prose"),
                     ("when not", "documents that already have headings")],
                    {"when not": "bad"}, label="the trade"),
              "On text that already carries structure, headings are a better and "
              "free signal.",
              {"sentences": 5}),
    ]),
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
    ],
    code={
        "file": "semantic_chunking.py",
        "intro": "Semantic chunking on a passage that changes subject halfway, "
                 "with the similarity between every consecutive sentence printed "
                 "so you can see the trough the boundary is placed at.",
        "code": '''# Semantic chunking: cut where the meaning changes.
import math

SENTENCES = [
    "Refunds are issued within fourteen days of purchase.",
    "The item must be unused and in its original packaging.",
    "Shipping costs are not included in the refund amount.",
    "Our data centres run on renewable energy contracts.",
    "Carbon reporting is published each quarter.",
]

VOCAB_TOPICS = {
    "refund": 0, "refunds": 0, "purchase": 0, "item": 0, "unused": 0,
    "packaging": 0, "shipping": 0, "costs": 0, "days": 0, "amount": 0,
    "data": 1, "centres": 1, "renewable": 1, "energy": 1, "carbon": 1,
    "reporting": 1, "quarter": 1, "contracts": 1, "published": 1,
}


def embed(sentence):
    """Stand-in for a real model: a two-dimensional topic histogram."""
    vec = [0.0, 0.0]
    for word in sentence.lower().strip(".").split():
        topic = VOCAB_TOPICS.get(word)
        if topic is not None:
            vec[topic] += 1.0
    norm = math.hypot(*vec) or 1.0
    return [v / norm for v in vec]


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))


vectors = [embed(s) for s in SENTENCES]
gaps = [cosine(vectors[i], vectors[i + 1]) for i in range(len(vectors) - 1)]

print("similarity between consecutive sentences:")
for i, g in enumerate(gaps):
    marker = "   <-- boundary" if g < 0.5 else ""
    print(f"  s{i + 1} -> s{i + 2}: {g:.3f}{marker}")

# A percentile of THIS document, not a global constant.
ordered = sorted(gaps)
threshold = ordered[max(0, int(len(ordered) * 0.25) - 1)]
print(f"\\n25th-percentile threshold for this document: {threshold:.3f}")

chunks, current = [], [SENTENCES[0]]
for i, gap in enumerate(gaps):
    if gap <= threshold:
        chunks.append(" ".join(current))
        current = []
    current.append(SENTENCES[i + 1])
chunks.append(" ".join(current))

print()
for i, c in enumerate(chunks):
    print(f"chunk {i} ({len(c)} chars): {c[:70]}...")

print()
print("Two chunks of different lengths, each on one subject. A 120-character")
print("splitter would have cut inside the refund policy.")

# --- the short-sentence problem ----------------------------------------
print()
noisy = ["Yes.", "See above.", "Refunds take fourteen days."]
for s in noisy:
    v = embed(s)
    print(f"  {s!r:>28} -> {[round(x, 2) for x in v]}")
print("Sentences with no topic words embed to zero and produce meaningless")
print("similarities. Buffering each sentence with its neighbours is the fix.")
''',
        "walk": [
            ("cosine(vectors[i], vectors[i + 1])",
             "The signal. High while the text stays on subject, low where it "
             "turns &mdash; and the turn is exactly where a chunk boundary "
             "belongs."),
            ("threshold from a percentile",
             "Relative, not absolute. A fixed 0.7 means something different in "
             "every corpus; a percentile of the gaps in <em>this</em> document "
             "adapts to how varied the writing is."),
            ("one embed() per sentence",
             "The cost. Alternatives embed once per chunk; this embeds once per "
             "sentence, at index time. Paid once, but it is a real bill on a "
             "large corpus."),
            ("the noisy short sentences",
             "\"Yes.\" carries no topic words and embeds to zero, so its "
             "similarities are meaningless. Real implementations buffer each "
             "sentence with its neighbours before embedding."),
        ],
        "try": [
            "Add a third topic and a sentence about it. A second boundary "
            "appears without any threshold being retuned.",
            "Set the threshold to a fixed 0.5 and add a document where every "
            "sentence is closely related. It splits nothing, or everything "
            "&mdash; which is the argument for a percentile.",
        ],
    },
    check=[
        {"q": "Semantic chunking places a boundary where:",
         "options": ["The character limit is reached", "The similarity between "
                     "consecutive sentences drops",
                     "A heading appears", "A paragraph ends"],
         "answer": 1,
         "why": "The dip in similarity is the signal that the subject has "
                "changed, which is where a chunk should end."},
        {"q": "Why should the threshold be a percentile rather than a fixed "
              "number?",
         "options": ["It is faster", "A fixed value means something different in "
                     "every corpus",
                     "Percentiles are more accurate", "To handle short sentences"],
         "answer": 1,
         "why": "A percentile of the gaps observed in this document adapts to "
                "how varied the writing is."},
        {"q": "When is semantic chunking usually NOT worth the cost?",
         "options": ["On long documents", "When the document already has "
                     "headings and structure",
                     "On technical text", "When using a small embedding model"],
         "answer": 1,
         "why": "Headings are an explicit, author-provided topic boundary and "
                "are free. Structure-aware chunking beats it at a fraction of "
                "the cost."},
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
    viz=viz([
        frame(pairs([("# Refund policy", "H1"),
                     ("Refunds are issued...", "body"),
                     ("## Exceptions", "H2"),
                     ("Digital goods are...", "body")],
                    {"# Refund policy": "lo", "## Exceptions": "lo"},
                    label="the document's own markup"),
              "Headings are explicit boundaries. No inference and no embedding "
              "call is needed to find them.",
              {"chunks": 0}),
        frame(pairs([("chunk 1", "[Refund policy] Refunds are issued within 14 days..."),
                     ("chunk 2", "[Refund policy > Exceptions] Digital goods are...")],
                    {"chunk 2": "hit"}, label="chunks with the heading path"),
              "The heading path is prepended. Chunk 2 retrieved alone still says "
              "which section it belongs to.",
              {"chunks": 2}),
        frame(pairs([("naive split of a table", "row 3 | row 4  (headers lost)"),
                     ("structure-aware", "headers + rows kept together"),
                     ("naive split of code", "half a function"),
                     ("structure-aware", "whole function")],
                    {"naive split of a table": "bad", "naive split of code": "bad"},
                    label="what a character splitter destroys"),
              "Tables and code are the clearest case: a mid-way cut leaves "
              "something that cannot be read at all.",
              {"chunks": 2}),
    ]),
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
    ],
    code={
        "file": "structure_aware_chunking.py",
        "intro": "A Markdown-aware chunker that tracks the heading path, run "
                 "against a character splitter on the same document &mdash; "
                 "including a table, so you can see what the naive version does "
                 "to it.",
        "code": '''# Structure-aware chunking: split on the author's own boundaries.

DOC = """# Refund policy

Refunds are issued within 14 days of purchase.

## Exceptions

Digital goods are non-refundable once downloaded.

## Fees by region

| region | fee |
| ------ | --- |
| UK     | 0   |
| EU     | 5   |
| US     | 8   |
"""


def structure_chunks(markdown):
    chunks, path, buffer = [], [], []

    def flush():
        if buffer and any(line.strip() for line in buffer):
            heading = " > ".join(path)
            body = "\\n".join(buffer).strip()
            chunks.append({"path": heading, "text": f"[{heading}]\\n{body}"})
        buffer.clear()

    for line in markdown.splitlines():
        if line.startswith("#"):
            flush()
            level = len(line) - len(line.lstrip("#"))
            del path[level - 1:]                  # pop back to this depth
            path.append(line.lstrip("# ").strip())
        else:
            buffer.append(line)
    flush()
    return chunks


def character_chunks(text, limit=110):
    return [text[i:i + limit] for i in range(0, len(text), limit)]


print("structure-aware:")
for i, c in enumerate(structure_chunks(DOC)):
    preview = c["text"].replace("\\n", " ")[:72]
    print(f"  [{i}] {preview}")

print()
print("character splitter:")
for i, c in enumerate(character_chunks(DOC)):
    print(f"  [{i}] {c.strip().replace(chr(10), ' ')[:72]!r}")

print()
print("Look at the table. The character splitter cuts between the header row")
print("and the data, so a retrieved chunk of '| US | 8 |' has no column names.")

# --- the heading path is why a chunk stands alone ----------------------
print()
fragment = "Digital goods are non-refundable once downloaded."
with_path = "[Refund policy > Exceptions]\\n" + fragment
print("without a path:", fragment)
print("with a path   :", with_path.replace("\\n", " "))
print("The second answers 'exceptions to what?' - and the heading words are")
print("now in the embedded text, so they match queries too.")

# --- structure first, then recursion for anything oversized ------------
print()
for c in structure_chunks(DOC):
    size = len(c["text"])
    note = "ok" if size <= 160 else "-> hand to a recursive splitter"
    print(f"  {c['path']:>28}: {size:>3} chars  {note}")
''',
        "walk": [
            ("del path[level - 1:]",
             "Maintains the heading stack. An <code>##</code> after an "
             "<code>###</code> pops back to depth two, which is what keeps the "
             "path correct through arbitrary nesting."),
            ("f\"[{heading}]\\n{body}\"",
             "The path is prepended to the chunk text, not just stored beside "
             "it. That puts the section's vocabulary into the embedded text, so "
             "it improves retrieval as well as readability."),
            ("the table in the output",
             "The character splitter cuts between the header row and the data. "
             "A retrieved chunk of <code>| US | 8 |</code> has no column names "
             "and cannot be interpreted at all."),
            ("-> hand to a recursive splitter",
             "Structure gives boundaries, not size control. Sections vary "
             "wildly, so the two techniques are combined: split on structure "
             "first, then recursively split anything still oversized."),
        ],
        "try": [
            "Add a <code>###</code> subsection and check the path pops "
            "correctly when the next <code>##</code> arrives.",
            "Feed it HTML instead and split on <code>&lt;h1&gt;</code> and "
            "<code>&lt;h2&gt;</code>. Same algorithm, different parser &mdash; "
            "which is the whole per-format cost.",
        ],
    },
    check=[
        {"q": "The main advantage of structure-aware chunking is that the "
              "boundaries are:",
         "options": ["Evenly spaced", "Placed by the author, so no inference is "
                     "needed",
                     "Smaller", "Computed from embeddings"],
         "answer": 1,
         "why": "A heading is an explicit statement that the subject changes. "
                "Semantic chunking spends an embedding per sentence to infer "
                "what the markup already says."},
        {"q": "Why prepend the heading path to each chunk?",
         "options": ["To make chunks longer", "So a chunk retrieved alone is "
                     "self-describing, and its section words are searchable",
                     "To help the splitter", "For deduplication"],
         "answer": 1,
         "why": "'Must be requested within 14 days' is useless in isolation. The "
                "path also puts section vocabulary into the embedded text."},
        {"q": "Structure-aware chunking is usually combined with recursive "
              "splitting because:",
         "options": ["Structure is unreliable", "Sections vary wildly in size, so "
                     "oversized ones still need splitting",
                     "Recursion is faster", "It reduces overlap"],
         "answer": 1,
         "why": "Structure gives good boundaries but no size control. Split on "
                "structure first, then recursively, keeping the heading path."},
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
    viz=viz([
        frame(pairs([("raw chunk", "It must be requested within 14 days of it."),
                     ("query", "how long do I have to return an item?"),
                     ("similarity", "0.11  - will not be retrieved")],
                    {"similarity": "bad"}, label="the chunk as cut"),
              "Two pronouns and no nouns. The chunk is about refunds and says so "
              "nowhere, so it cannot be found.",
              {"score": 0.11}),
        frame(pairs([("+ document title", "Customer returns handbook"),
                     ("+ heading path", "Refund policy > Time limits"),
                     ("+ resolved text", "A refund must be requested within 14 "
                                         "days of purchase.")],
                    {"+ resolved text": "hit"}, label="context added back"),
              "The same span, enriched. Nothing about the boundary changed.",
              {"score": 0.11}),
        frame(pairs([("query", "how long do I have to return an item?"),
                     ("similarity", "0.68  - retrieved at rank 1"),
                     ("cost", "one LLM call per chunk, at index time")],
                    {"similarity": "hit", "cost": "lo"}, label="after enrichment"),
              "Retrievable now, and usable by the generator without the "
              "surrounding document.",
              {"score": 0.68}),
    ]),
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
    ],
    code={
        "file": "context_aware_chunking.py",
        "intro": "A chunk full of dangling pronouns scored against a realistic "
                 "query before and after enrichment, then the dilution effect "
                 "shown by over-enriching until distinct chunks stop being "
                 "distinguishable.",
        "code": '''# Context-aware chunking: fix what the chunk lost, not where it was cut.
import math
from collections import Counter

TITLE = "Customer returns handbook"
PATH = "Refund policy > Time limits"

RAW = "It must be requested within 14 days of it, and it must be unused."
RESOLVED = ("A refund must be requested within 14 days of purchase, "
            "and the item must be unused.")

QUERY = "how long do I have to return an item for a refund"


def embed(text):
    return Counter(w.strip(".,").lower() for w in text.split())


def cosine(a, b):
    shared = set(a) & set(b)
    num = sum(a[w] * b[w] for w in shared)
    den = math.hypot(*a.values()) * math.hypot(*b.values())
    return num / den if den else 0.0


q = embed(QUERY)
variants = {
    "raw chunk": RAW,
    "+ title": f"{TITLE}\\n{RAW}",
    "+ title + path": f"{TITLE}\\n{PATH}\\n{RAW}",
    "+ resolved pronouns": f"{TITLE}\\n{PATH}\\n{RESOLVED}",
}

print(f"query: {QUERY!r}\\n")
print(f"{'variant':>22} {'similarity':>11}")
for name, text in variants.items():
    print(f"{name:>22} {cosine(q, embed(text)):>11.3f}")

print()
print("The raw chunk is about refunds and never says so. Resolving 'it' is")
print("what puts the searchable words into the text.")

# --- dilution: enrichment can go too far -------------------------------
BOILERPLATE = ("This document is the customer returns handbook covering "
               "refunds exchanges shipping and warranty for all regions "
               "and product lines across the company. ") * 3

chunk_a = f"{TITLE}\\n{PATH}\\n{RESOLVED}"
chunk_b = f"{TITLE}\\nRefund policy > Exceptions\\nDigital goods are non-refundable once downloaded."

print()
print("distinguishability of two different chunks:")
print(f"  lightly enriched : {cosine(embed(chunk_a), embed(chunk_b)):.3f}")
over_a = BOILERPLATE + chunk_a
over_b = BOILERPLATE + chunk_b
print(f"  over-enriched    : {cosine(embed(over_a), embed(over_b)):.3f}")
print()
print("Two chunks on different subjects now look nearly identical. The")
print("retriever cannot tell them apart, which is the cost of over-enriching.")
''',
        "walk": [
            ("the raw chunk's similarity",
             "Near zero against a query it should match perfectly. The chunk is "
             "about refunds and contains neither \"refund\" nor \"return\" "
             "&mdash; only pronouns."),
            ("f\"{TITLE}\\n{PATH}\\n{RAW}\"",
             "The free enrichment: title and heading path, prepended, no model "
             "call. Usually the largest single improvement available."),
            ("RESOLVED",
             "Pronouns replaced with their referents. This is what an LLM does "
             "in contextual retrieval, and it is what puts searchable nouns into "
             "the text."),
            ("the over-enriched comparison",
             "Two chunks on different subjects become nearly identical once the "
             "shared boilerplate dominates. Keep enrichment short relative to "
             "the chunk."),
        ],
        "try": [
            "Add a third chunk from a different section and compare all three "
            "lightly and heavily enriched. Dilution gets worse as the corpus "
            "grows.",
            "Enrich only the stored text and not the embedded text. Retrieval "
            "does not improve &mdash; which shows the gain comes from what is "
            "embedded, not what is displayed.",
        ],
    },
    check=[
        {"q": "Context-aware chunking differs from the other strategies in that "
              "it changes:",
         "options": ["Where the boundaries fall", "What is stored with each "
                     "chunk, not where it was cut",
                     "The embedding model", "The retrieval algorithm"],
         "answer": 1,
         "why": "The boundary is unchanged. What changes is the context added "
                "back to compensate for extraction."},
        {"q": "Why does a chunk full of pronouns fail at retrieval, not just at "
              "generation?",
         "options": ["It is too short", "Its embedding lacks the words a user "
                     "would search for",
                     "Pronouns are stopwords", "It is deduplicated"],
         "answer": 1,
         "why": "The chunk is about refunds and never says 'refund', so nothing "
                "in its vector matches the query."},
        {"q": "The risk of over-enriching each chunk is:",
         "options": ["Slower indexing", "Chunks from the same section become "
                     "hard to tell apart",
                     "Larger storage", "Worse generation"],
         "answer": 1,
         "why": "If the shared context dominates the embedding, the retriever "
                "loses the ability to distinguish chunks. Keep it short relative "
                "to the chunk."},
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
    viz=viz([
        frame(pairs([("corpus", "1,000,000 vectors x 768 dims"),
                     ("exact search", "1,000,000 comparisons per query"),
                     ("latency", "~600 ms, single-threaded")],
                    {"latency": "bad"}, label="flat index: no index at all"),
              "Exact and simple: compare with everything. Correct, and it does "
              "not survive contact with a real corpus.",
              {"compared": 1000000}),
        frame(pairs([("index", "graph or cluster structure"),
                     ("visited", "~2,000 vectors"),
                     ("latency", "~3 ms"), ("recall@10", "0.95")],
                    {"visited": "hit", "recall@10": "lo"},
                    label="approximate index"),
              "Two thousand comparisons instead of a million, and one true "
              "neighbour in twenty is missed.",
              {"compared": 2000}),
        frame(pairs([("more accurate", "raise the search effort -> slower"),
                     ("faster", "lower the effort -> worse recall"),
                     ("less memory", "compress the vectors -> worse recall")],
                    {}, label="the three-way trade"),
              "Every index type exposes these same three knobs under different "
              "names.",
              {"compared": 2000}),
        frame(pairs([("flat", "exact, O(n), small corpora and ground truth"),
                     ("IVF", "cluster then search a few clusters"),
                     ("HNSW", "navigable graph, best recall/latency, most memory"),
                     ("+ PQ", "compress vectors, big memory saving, lower recall")],
                    {"HNSW": "hit"}, label="the families"),
              "HNSW is the usual default; IVF and product quantization are what "
              "you reach for when memory becomes the binding constraint.",
              {"compared": 2000}),
    ]),
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
    ],
    code={
        "file": "vector_indexing.py",
        "intro": "An exact search and a simple cluster-based index over the same "
                 "vectors, with comparisons counted and recall measured against "
                 "the exact answer &mdash; so the trade is a number rather than a "
                 "claim.",
        "code": '''# Why vector databases index: exact search does not scale.
import math, random, time

random.seed(7)
DIM, N, K = 24, 4_000, 10
corpus = [[random.gauss(0, 1) for _ in range(DIM)] for _ in range(N)]
query = [random.gauss(0, 1) for _ in range(DIM)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


# --- exact: compare with everything ------------------------------------
start = time.time()
exact = sorted(range(N), key=lambda i: -dot(query, corpus[i]))[:K]
exact_ms = (time.time() - start) * 1000
print(f"exact search   : {N:,} comparisons, {exact_ms:.0f} ms")

# --- a toy IVF: cluster, then search only the nearest clusters ---------
CLUSTERS = 32
centroids = [corpus[random.randrange(N)] for _ in range(CLUSTERS)]

def assign(centroids):
    groups = [[] for _ in centroids]
    for i, vec in enumerate(corpus):
        best = max(range(len(centroids)), key=lambda c: dot(vec, centroids[c]))
        groups[best].append(i)
    return groups

# A few k-means passes. Random centroids give a poor partition, and a poor
# partition understates what IVF actually achieves.
for _ in range(2):
    assignment = assign(centroids)
    for c, members in enumerate(assignment):
        if members:
            centroids[c] = [sum(corpus[i][d] for i in members) / len(members)
                            for d in range(DIM)]
assignment = assign(centroids)


def ivf_search(query, probe):
    """Search only the `probe` nearest clusters."""
    order = sorted(range(CLUSTERS), key=lambda c: -dot(query, centroids[c]))
    candidates = [i for c in order[:probe] for i in assignment[c]]
    ranked = sorted(candidates, key=lambda i: -dot(query, corpus[i]))[:K]
    return ranked, len(candidates)


print()
print(f"{'probes':>7} {'compared':>10} {'recall@%d' % K:>10} {'ms':>7}")
for probe in (1, 4, 12, 32):
    start = time.time()
    got, compared = ivf_search(query, probe)
    ms = (time.time() - start) * 1000
    recall = len(set(got) & set(exact)) / K
    print(f"{probe:>7} {compared:>10,} {recall:>10.2f} {ms:>7.0f}")

print()
print("More probes: better recall, more comparisons, more latency. That is the")
print("entire trade, and every index type exposes it under a different name.")
print()
print("At 32 probes it searches every cluster, so recall is 1.0 and it has")
print("become an exact search with extra steps.")
''',
        "walk": [
            ("exact = sorted(range(N), key=...)",
             "The ground truth, and the only way to measure any index's recall. "
             "It is also O(n&middot;d) per query, which is why it does not "
             "survive a real corpus."),
            ("assignment[best].append(i)",
             "The index: each vector is filed under its nearest centroid. "
             "Building it is a one-off cost; the saving is paid back on every "
             "query."),
            ("order[:probe]",
             "The pruning. Searching one cluster is fast and misses a lot; "
             "searching more improves recall and costs comparisons. This one "
             "parameter <em>is</em> the trade-off."),
            ("recall = len(set(got) & set(exact)) / K",
             "Recall@k, measured rather than assumed. A vector index is a "
             "lossy structure and the loss has to be quantified against exact "
             "results."),
        ],
        "try": [
            "Raise <code>CLUSTERS</code> to 256 with <code>probe=4</code>. "
            "Finer clusters mean fewer comparisons and lower recall &mdash; the "
            "same trade from a different direction.",
            "Set <code>DIM = 512</code>. Every comparison gets more expensive "
            "and the exact search degrades faster than the index does.",
        ],
    },
    check=[
        {"q": "A flat (unindexed) vector search is:",
         "options": ["Approximate and fast", "Exact and O(n) per query",
                     "Exact and O(log n)", "Approximate and memory-efficient"],
         "answer": 1,
         "why": "It compares the query with every vector. That makes it the "
                "ground truth for measuring recall, and unusable at scale."},
        {"q": "What does an approximate index trade away?",
         "options": ["Memory only", "Recall - it may miss true neighbours",
                     "Precision of the vectors", "Nothing"],
         "answer": 1,
         "why": "It prunes most of the corpus without comparing, so a genuine "
                "neighbour can be routed around. recall@k is how you measure it."},
        {"q": "recall@10 of 0.95 means:",
         "options": ["95% of queries succeed", "On average 9.5 of the 10 true "
                     "nearest neighbours were returned",
                     "The vectors are 95% accurate", "95% of the corpus was searched"],
         "answer": 1,
         "why": "Usually fine for RAG, where a reranker sees the top 50 anyway - "
                "and not fine for deduplication or exact matching."},
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
    viz=viz([
        frame(pairs([("layer 2", "8 nodes, long edges"),
                     ("layer 1", "600 nodes"),
                     ("layer 0", "1,000,000 nodes, all of them")],
                    {"layer 2": "lo"}, label="HNSW layers"),
              "Each node appears in layer 0; a random few also appear higher. "
              "Sparse at the top, complete at the bottom.",
              {"layer": 2, "visited": 0}),
        frame(pairs([("enter at layer 2", "greedy hop to the closest neighbour"),
                     ("visited", "6 nodes"),
                     ("effect", "crossed most of the space")],
                    {"effect": "hit"}, label="descend: coarse"),
              "Long edges at the top cover distance cheaply - a handful of hops "
              "gets near the right region.",
              {"layer": 2, "visited": 6}),
        frame(pairs([("drop to layer 0", "dense edges, short hops"),
                     ("visited", "1,840 nodes total"),
                     ("recall@10", "0.96")],
                    {"recall@10": "hit"}, label="descend: fine"),
              "The bottom layer refines within the neighbourhood. Under two "
              "thousand comparisons out of a million.",
              {"layer": 0, "visited": 1840}),
        frame(pairs([("efSearch 32", "recall 0.87, 0.9 ms"),
                     ("efSearch 128", "recall 0.96, 2.6 ms"),
                     ("efSearch 512", "recall 0.99, 9.1 ms"),
                     ("M (edges/node)", "build-time: more memory, better graph")],
                    {"efSearch 128": "lo"}, label="the knobs"),
              "efSearch is tuned per query at runtime; M is fixed when the index "
              "is built.",
              {"layer": 0, "visited": 1840}),
    ]),
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
    ],
    code={
        "file": "ann_indexing.py",
        "intro": "A miniature HNSW &mdash; layered proximity graph, greedy "
                 "descent, a real candidate list &mdash; with the nodes visited "
                 "per layer printed and recall measured against exact search at "
                 "several efSearch values.",
        "code": '''# A small HNSW: layered proximity graph, greedy descent.
import heapq, math, random, time

random.seed(3)
DIM, N, K = 24, 2_500, 10
corpus = [[random.gauss(0, 1) for _ in range(DIM)] for _ in range(N)]


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


# --- build: assign layers geometrically, link nearest neighbours -------
M, LAYERS = 8, 3
layer_of = [min(LAYERS - 1, int(-math.log(random.random()) * 0.6)) for _ in range(N)]
members = [[i for i in range(N) if layer_of[i] >= L] for L in range(LAYERS)]

graph = [{} for _ in range(LAYERS)]
for L in range(LAYERS):
    pool = members[L]
    for i in pool:
        # A real build searches the graph; sampling keeps this readable.
        sample = random.sample(pool, min(len(pool), 40))
        near = sorted(sample, key=lambda j: dist(corpus[i], corpus[j]))
        graph[L][i] = [j for j in near if j != i][:M]

print(f"{N:,} vectors, {LAYERS} layers")
for L in range(LAYERS - 1, -1, -1):
    print(f"  layer {L}: {len(members[L]):>5} nodes, {M} edges each")


def search(query, ef=64, trace=False):
    entry = members[LAYERS - 1][0]
    visited_total = 0
    current = entry
    for L in range(LAYERS - 1, 0, -1):           # coarse layers: pure greedy
        improved, visits = True, 0
        while improved:
            improved = False
            for j in graph[L].get(current, []):
                visits += 1
                if dist(query, corpus[j]) < dist(query, corpus[current]):
                    current, improved = j, True
        visited_total += visits
        if trace:
            print(f"    layer {L}: {visits} nodes visited")

    # bottom layer: a beam of width ef rather than a single greedy walk
    seen = {current}
    candidates = [(dist(query, corpus[current]), current)]
    best = [(-dist(query, corpus[current]), current)]
    while candidates:
        d, node = heapq.heappop(candidates)
        if -best[0][0] < d and len(best) >= ef:
            break
        for j in graph[0].get(node, []):
            if j in seen:
                continue
            seen.add(j)
            visited_total += 1
            dj = dist(query, corpus[j])
            if len(best) < ef or dj < -best[0][0]:
                heapq.heappush(candidates, (dj, j))
                heapq.heappush(best, (-dj, j))
                if len(best) > ef:
                    heapq.heappop(best)
    if trace:
        print(f"    layer 0: beam of {ef}")
    ranked = sorted((-d, i) for d, i in best)[:K]
    return [i for _, i in ranked], visited_total


query = [random.gauss(0, 1) for _ in range(DIM)]
exact = sorted(range(N), key=lambda i: dist(query, corpus[i]))[:K]

print()
print("one search, layer by layer:")
search(query, ef=64, trace=True)

print()
print(f"{'efSearch':>9} {'visited':>9} {'recall@%d' % K:>10} {'ms':>7}")
for ef in (8, 32, 128, 512):
    start = time.time()
    got, visited = search(query, ef=ef)
    ms = (time.time() - start) * 1000
    recall = len(set(got) & set(exact)) / K
    print(f"{ef:>9} {visited:>9,} {recall:>10.2f} {ms:>7.1f}")

print()
print(f"exact search compares all {N:,} vectors every time.")
print("efSearch is the runtime knob: wider beam, better recall, more work.")
''',
        "walk": [
            ("layer_of = ... -log(random()) ...",
             "Layers are assigned geometrically, so each is a sparse random "
             "sample of the one below. That is what gives the top layer long "
             "edges and the bottom layer complete coverage."),
            ("the greedy loop on coarse layers",
             "Move to whichever neighbour is closer, until none is. A handful of "
             "hops at the top crosses most of the space, which is the whole "
             "reason for the hierarchy."),
            ("the beam of width ef on layer 0",
             "The bottom layer keeps a candidate list rather than a single "
             "position. That is what recovers from a greedy walk heading "
             "slightly wrong &mdash; and <code>ef</code> is how wide the "
             "recovery net is."),
            ("the efSearch table",
             "The knob you actually tune. Recall and latency both rise with it, "
             "and it can be set per query &mdash; wide for an important search, "
             "narrow for an autocomplete."),
        ],
        "try": [
            "Set <code>M = 3</code> and rebuild. A poorly connected graph loses "
            "recall no matter how large <code>efSearch</code> gets &mdash; "
            "build-time damage cannot be fixed at query time.",
            "Set <code>LAYERS = 1</code>. It becomes a flat proximity graph, and "
            "the visit count rises sharply for the same recall.",
        ],
    },
    check=[
        {"q": "What do HNSW's upper layers provide?",
         "options": ["Higher precision", "Long edges, so a few hops cross most "
                     "of the space",
                     "Compression", "Deduplication"],
         "answer": 1,
         "why": "Sparse upper layers cover distance cheaply; the dense bottom "
                "layer refines. It is the skip-list idea applied to geometry."},
        {"q": "Which parameter is tuned at query time?",
         "options": ["M", "efConstruction", "efSearch", "The number of layers"],
         "answer": 2,
         "why": "M and efConstruction are fixed when the index is built. "
                "efSearch widens the candidate list per query, trading latency "
                "for recall."},
        {"q": "IVF's characteristic failure is:",
         "options": ["Running out of memory", "Missing a neighbour that sits "
                     "just across a cluster boundary",
                     "Returning duplicates", "Slow builds"],
         "answer": 1,
         "why": "Probing more clusters fixes it at the cost of latency. IVF is "
                "cheaper to build and update than HNSW, which is why it survives "
                "alongside it."},
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
    viz=viz([
        frame(pairs([("top-10 by similarity", "8 restricted, 2 permitted"),
                     ("after post-filter", "2 results"),
                     ("answer quality", "poor - thin evidence")],
                    {"after post-filter": "bad"}, label="post-filtering"),
              "Ask for ten, get ten, drop eight. The system did not fail loudly; "
              "it just answered from two chunks.",
              {"returned": 2}),
        frame(pairs([("candidate set", "only documents this user may see"),
                     ("top-10 within it", "10 permitted results"),
                     ("answer quality", "full evidence")],
                    {"top-10 within it": "hit"}, label="pre-filtering"),
              "The filter is applied before ranking, so the top-k is ten "
              "permitted documents rather than whatever survived.",
              {"returned": 10}),
        frame(pairs([("filter after generation", "the model already read it"),
                     ("leak surface", "summary, citation, refusal wording"),
                     ("verdict", "not a control")],
                    {"verdict": "bad"}, label="the anti-pattern"),
              "A model that has read a restricted document leaks it through "
              "paraphrase even when the text is stripped from the response.",
              {"returned": 0}),
        frame(pairs([("ACLs in the index", "fast, and stale when access changes"),
                     ("ACLs at query time", "correct, and needs a fast lookup"),
                     ("practice", "index a group id, resolve groups per query")],
                    {"practice": "hit"}, label="where the permissions live"),
              "Indexing a stable group id and resolving membership per request "
              "is the usual compromise.",
              {"returned": 10}),
    ]),
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
    ],
    code={
        "file": "permission_filtering.py",
        "intro": "The same query run three ways over a corpus where most "
                 "documents are restricted, so the result counts show what "
                 "post-filtering silently does to a user with narrow access.",
        "code": '''# Permission filtering: inside the search, not around it.
import random

random.seed(11)

# 200 chunks; most belong to groups this user is not in.
CHUNKS = []
for i in range(200):
    group = random.choice(["finance", "finance", "finance", "hr", "public"])
    CHUNKS.append({"id": i, "group": group,
                   "score": round(random.uniform(0.2, 0.95), 3)})

USER_GROUPS = {"public", "hr"}
K = 10


def post_filter(chunks, k=K):
    """Rank everything, then drop what the user cannot see."""
    top = sorted(chunks, key=lambda c: -c["score"])[:k]
    return [c for c in top if c["group"] in USER_GROUPS]


def post_filter_overfetch(chunks, k=K, fetch=100):
    top = sorted(chunks, key=lambda c: -c["score"])[:fetch]
    return [c for c in top if c["group"] in USER_GROUPS][:k]


def pre_filter(chunks, k=K):
    """Restrict the candidate set, THEN rank."""
    allowed = [c for c in chunks if c["group"] in USER_GROUPS]
    return sorted(allowed, key=lambda c: -c["score"])[:k]


visible = sum(1 for c in CHUNKS if c["group"] in USER_GROUPS)
print(f"corpus: {len(CHUNKS)} chunks, {visible} visible to this user "
      f"({visible / len(CHUNKS):.0%})")
print(f"asked for k = {K}\\n")

for name, fn in (("post-filter", post_filter),
                 ("post-filter, fetch 100", post_filter_overfetch),
                 ("pre-filter", pre_filter)):
    got = fn(CHUNKS)
    print(f"{name:>24}: {len(got):>2} results  "
          f"top score {got[0]['score'] if got else 0:.3f}")

print()
print("Post-filtering asked for 10 and returned fewer. Nothing raised an")
print("error - the generator simply answered from less evidence.")

# --- the failure is worst for the most restricted user -----------------
print()
print(f"{'user sees':>12} {'post-filter':>12} {'pre-filter':>11}")
for groups in ({"public"}, {"public", "hr"}, {"public", "hr", "finance"}):
    USER_GROUPS = groups
    print(f"{'+'.join(sorted(groups)):>12} "
          f"{len(post_filter(CHUNKS)):>12} {len(pre_filter(CHUNKS)):>11}")

print()
print("The narrower the access, the worse post-filtering gets - which is the")
print("opposite of what a security control should do.")

# --- permissions must be resolved at query time ------------------------
print()
indexed_acl = {"alice", "bob"}                  # baked in at index time
current_members = {"alice"}                     # bob left the team today
print("chunk ACL as indexed :", sorted(indexed_acl))
print("group membership now  :", sorted(current_members))
print("bob still passes an indexed-ACL filter:", "bob" in indexed_acl)
print("Indexing a GROUP id and resolving membership per request avoids this;")
print("stale permissions fail open, which is the wrong direction to fail.")
''',
        "walk": [
            ("post_filter",
             "Ranks first, filters second. It asked for ten and returned "
             "fewer, with nothing raised &mdash; the result set collapsed "
             "silently."),
            ("post_filter_overfetch",
             "Fetching 100 makes the failure less likely and cannot remove it. "
             "A user with access to a tiny slice of the corpus still comes up "
             "short."),
            ("pre_filter",
             "Restricts the candidate set before ranking, so k means k "
             "permitted results. This is the correct behaviour and the one that "
             "fights the ANN index."),
            ("the per-user table",
             "Post-filtering degrades fastest for the most restricted user, "
             "which is the opposite of how a security control should behave."),
        ],
        "try": [
            "Give the user only <code>public</code> and re-run. Post-filtering "
            "can return nothing at all while the corpus contains perfectly good "
            "permitted chunks.",
            "Add a <code>deleted</code> flag and filter on it. Note that "
            "filtering is not deletion &mdash; a removed document has to leave "
            "the index.",
        ],
    },
    check=[
        {"q": "Why does post-filtering break recall?",
         "options": ["It is slower", "Permitted documents may never have entered "
                     "the top-k, so the result set silently shrinks",
                     "It filters the wrong field", "It duplicates results"],
         "answer": 1,
         "why": "You ask for 10, get 10, drop 8, and answer from 2 - with no "
                "error raised. Over-fetching reduces the odds without fixing it."},
        {"q": "Filtering restricted content out of the model's response is:",
         "options": ["Equivalent to pre-filtering", "Not a control - the model "
                     "already read it and can paraphrase it",
                     "The recommended approach", "Sufficient with a good prompt"],
         "answer": 1,
         "why": "Leakage survives through summaries, citations and even the "
                "wording of a refusal. The document must never reach the model."},
        {"q": "Why index a group id rather than a resolved list of users?",
         "options": ["It is smaller", "Membership can be resolved per request, "
                     "so access changes take effect without re-indexing",
                     "Groups are hashable", "It improves recall"],
         "answer": 1,
         "why": "A baked-in user list goes stale the moment someone leaves a "
                "team, and stale permissions fail open."},
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
    viz=viz([
        frame(pairs([("shard 1", "returns local top-5"),
                     ("shard 2", "returns local top-5"),
                     ("shard 3", "returns local top-5"),
                     ("coordinator", "merges 15 -> global top-5")],
                    {"coordinator": "hit"}, label="scatter-gather"),
              "Each shard ranks its own slice. The coordinator only has to merge "
              "already-sorted lists.",
              {"shards": 3, "returned": 5}),
        frame(pairs([("random sharding", "relevant docs spread across shards"),
                     ("each shard's top-5", "contains some of them"),
                     ("recall", "0.98")],
                    {"recall": "hit"}, label="sharding at random"),
              "Spreading the corpus evenly means no single shard holds all the "
              "answers, so a per-shard k is enough.",
              {"shards": 3, "returned": 5}),
        frame(pairs([("semantic sharding", "all finance docs on shard 2"),
                     ("shard 2's top-5", "holds ranks 1-40 of the true results"),
                     ("recall", "0.40 - the rest were truncated")],
                    {"recall": "bad"}, label="sharding by topic"),
              "A finance query concentrates every good document in one shard, "
              "and its local k throws most of them away.",
              {"shards": 3, "returned": 5}),
        frame(pairs([("shard latency", "40, 45, 210 ms"),
                     ("response", "210 ms - the slowest"),
                     ("more shards", "more chances of a slow one"),
                     ("mitigation", "hedged requests, or ignore a late shard")],
                    {"response": "bad"}, label="tail latency"),
              "Scatter-gather waits for everyone. Adding shards adds tail risk, "
              "which is the cost nobody mentions.",
              {"shards": 3, "returned": 5}),
    ]),
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
    ],
    code={
        "file": "distributed_retrieval.py",
        "intro": "Scatter-gather over three shards, with recall measured against "
                 "a single-index search, run once with random sharding and once "
                 "with semantic sharding so the recall collapse is a number.",
        "code": '''# Scatter-gather retrieval, and why sharding strategy decides recall.
import random

random.seed(5)

TOPICS_ = ["finance", "hr", "legal"]
CORPUS = []
for i in range(900):
    topic = TOPICS_[i % 3]
    CORPUS.append({"id": i, "topic": topic,
                   # documents on the query's topic score higher
                   "score": round(random.uniform(0.6, 0.99) if topic == "finance"
                                  else random.uniform(0.1, 0.55), 4)})

K = 10
ground_truth = [c["id"] for c in sorted(CORPUS, key=lambda c: -c["score"])[:K]]


def scatter_gather(shards, k=K, per_shard=None):
    per_shard = per_shard or k
    local = []
    for shard in shards:
        local += sorted(shard, key=lambda c: -c["score"])[:per_shard]
    merged = sorted(local, key=lambda c: -c["score"])[:k]
    return [c["id"] for c in merged]


def recall(got):
    return len(set(got) & set(ground_truth)) / len(ground_truth)


random_shards = [[] for _ in range(3)]
for c in CORPUS:
    random_shards[random.randrange(3)].append(c)

semantic_shards = [[c for c in CORPUS if c["topic"] == t] for t in TOPICS_]

print(f"corpus {len(CORPUS)}, 3 shards, k={K}, query is finance-flavoured\\n")
print(f"{'strategy':>20} {'per-shard k':>12} {'recall@%d' % K:>10}")
for name, shards in (("random", random_shards), ("semantic", semantic_shards)):
    for per_shard in (K, K * 5):
        got = scatter_gather(shards, per_shard=per_shard)
        print(f"{name:>20} {per_shard:>12} {recall(got):>10.2f}")

print()
print("Semantic sharding puts every good document on one shard, and that")
print("shard's local top-10 throws the rest away. Over-fetching recovers it,")
print("at the bandwidth cost the routing was supposed to save.")

# --- tail latency ------------------------------------------------------
print()
random.seed(2)
def response_time(n_shards):
    latencies = [random.gauss(40, 8) if random.random() > 0.02
                 else random.gauss(220, 30) for _ in range(n_shards)]
    return max(latencies)                        # you wait for the slowest

for n in (1, 3, 10, 30):
    runs = [response_time(n) for _ in range(2000)]
    runs.sort()
    print(f"  {n:>2} shards: median {runs[len(runs)//2]:>6.0f} ms   "
          f"p99 {runs[int(len(runs) * 0.99)]:>6.0f} ms")

print()
print("The median barely moves; p99 climbs with every shard added, because")
print("scatter-gather waits for whichever shard happened to be slow.")
''',
        "walk": [
            ("sorted(shard, ...)[:per_shard]",
             "Each shard ranks only its own slice. The coordinator never sees "
             "the corpus, which is what makes this scale &mdash; and what makes "
             "the per-shard k a real decision."),
            ("semantic_shards",
             "All finance documents on one shard. Its local top-10 holds ranks "
             "1&ndash;40 of the true results and discards thirty of them, which "
             "the recall column shows."),
            ("per_shard = K * 5",
             "Over-fetching recovers the recall lost to semantic sharding, at "
             "the bandwidth and latency the topic routing was meant to save."),
            ("max(latencies)",
             "Scatter-gather waits for everyone, so response time is the maximum "
             "not the mean. The p99 column is why adding shards can make a "
             "system slower."),
        ],
        "try": [
            "Raise the slow-shard probability from 2% to 10%. The p99 column "
            "degrades sharply while the median barely moves &mdash; which is why "
            "averages hide this.",
            "Shard by tenant and query within one tenant only. Semantic sharding "
            "is correct there, because the query never needs the other shards.",
        ],
    },
    check=[
        {"q": "The difference between a shard and a replica is:",
         "options": ["Replicas are smaller", "A shard holds a slice of the data; "
                     "a replica holds a full copy",
                     "Shards are read-only", "There is none"],
         "answer": 1,
         "why": "Sharding solves data that will not fit; replication solves "
                "query volume and failure. If the index fits on one machine you "
                "want replicas and no sharding."},
        {"q": "Why does semantic sharding hurt recall?",
         "options": ["Topics overlap", "Relevant documents concentrate in one "
                     "shard, whose local top-k discards most of them",
                     "Scores become incomparable", "It needs more machines"],
         "answer": 1,
         "why": "Random sharding spreads them evenly, so a modest per-shard k "
                "captures nearly all of them."},
        {"q": "In scatter-gather, the query's latency is:",
         "options": ["The average shard latency", "The slowest shard's latency",
                     "The fastest shard's latency", "Independent of shard count"],
         "answer": 1,
         "why": "You wait for everyone, so p99 climbs as shards are added. "
                "Hedged requests and deadlines are the usual mitigations."},
    ],
)
