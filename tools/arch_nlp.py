# -*- coding: utf-8 -*-
"""The four named-architecture modules in the NLP track.

word2vec and GloVe are the two answers to the same question - how do you get a
vector per word out of raw text - and they answer it from opposite ends, one
window at a time against one global count matrix. seq2seq and neural machine
translation are the two halves of the encoder-decoder story: the model, and
then what it takes to actually emit a sentence with it.

The word-vector pages train a real model in the tab on a nineteen-sentence
corpus that is printed in full. It is small enough that a reader can check a
co-occurrence count by hand, and honest about what a corpus that size can and
cannot support.
"""

from arch_common import (entry, svg, box, txt, line, circle, path, stack, A, M, B, S)

TOPICS = []


# ---------------------------------------------------------------------------
# 1. word2vec
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "word2vec",
    "natural_language_processing",
    "Word2Vec",
    "Word vectors",
    "Train skip-gram in the page",
    "Pairs generated from a window, vectors pulled together by negative "
    "sampling, and a nearest-neighbour table that changes as you push the "
    "step count.",
    svg(txt(30, 26, "the", M, 8) + txt(56, 26, "king", A, 9)
        + txt(88, 26, "rules", M, 8) + txt(120, 26, "the", M, 8)
        + box(44, 16, 28, 14, fill="none", stroke=A, sw=1.4)
        + line(56, 32, 40, 48, B, 1) + line(56, 32, 72, 48, B, 1)
        + line(56, 32, 104, 48, B, 1)
        + circle(40, 54, 4) + circle(72, 54, 4) + circle(104, 54, 4)
        + txt(80, 80, "centre predicts context", M, 7)),
    {"widget": "word2vec"},
    [
        "There is no labelled data. The corpus supplies its own labels: each "
        "word is asked to predict the words beside it.",
        "Negative sampling replaces a softmax over the whole vocabulary with a "
        "handful of binary decisions &mdash; that is the speed-up that made it "
        "trainable on billions of words.",
        "Two matrices are learned, not one: every word has a centre vector and "
        "a context vector. Most implementations keep only the first.",
        "A window of &plusmn;2 over the nineteen sentences below gives about "
        "300 training pairs. Real corpora give billions.",
    ],
    r"""
title: Word2Vec
intro: A model with no hidden layer and no labels that learns, from nothing but adjacency, that "king" belongs next to "queen".

## The setup: text labels itself

Supervised learning needs labels. Text has none, and annotating enough of it to
learn word meanings is not a project anyone was going to finish.

The distributional hypothesis supplies the way out: **words that appear in
similar contexts have similar meanings**. That is not a claim about semantics,
it is a claim about statistics, and it turns an unlabelled corpus into a
supervised dataset. Every position in every sentence becomes a training example
where the input is one word and the target is its neighbour.

Look at the token strip in the explorer. With a window of &plusmn;2 around
`king` in "the king rules the kingdom", the model is asked to associate `king`
with `the`, `rules`, and the second `the`. Slide the window control and the
pair list under it changes. Nineteen sentences with a window of 2 give about
300 pairs; the original paper's Google News corpus gave roughly 100 billion.

## Two directions through the same window

**Skip-gram** takes the centre word and predicts each context word separately.
One centre with four neighbours becomes four training pairs.

**CBOW** goes the other way: average the context vectors and predict the centre
from them. One position becomes one training example.

CBOW is faster, because it makes one update per position instead of 2&times;window,
and it smooths over the context, which suits frequent words. Skip-gram makes
many more updates from the same text, which is what lets it learn decent
vectors for rare words &mdash; a rare word appears in few positions, and
skip-gram wrings more gradient out of each one. In practice skip-gram with
negative sampling is the default, and it is what the toggle in the explorer
starts on.

## The problem with the obvious objective

Written as a proper probabilistic model, skip-gram wants:

```
P(context | centre) = exp(u_c . v_w) / sum over EVERY word in V of exp(u_k . v_w)
```

The denominator is the problem. Every gradient step requires a dot product
against every word in the vocabulary. At |V| = 100,000 and a corpus of a
billion tokens, that is the difference between a model you can train and one
you cannot.

## Negative sampling

The fix is to stop asking a multi-class question. Instead of "which of 100,000
words comes next", ask a much easier one: **"did this pair really occur, or did
I make it up?"**

For each real pair, draw k fake ones by sampling random words, and train a
logistic classifier:

```
maximise   log sigma(u_context . v_centre)
         + sum over k negatives of  log sigma(-u_negative . v_centre)
```

Each step now costs k+1 dot products instead of |V|. The explorer prints the
arithmetic for one real pair: the dot product, the sigmoid of it, and the fact
that it is being pushed toward 1 while k sampled words are pushed toward 0.

Two details matter. The negatives are drawn from the unigram distribution
**raised to the power 0.75**, not from the raw frequencies &mdash; a piece of
tuning the authors report as working better than either the raw or the uniform
distribution, and which has the effect of sampling common words often but not
as often as they occur. And the paper pairs this with **subsampling**, which
discards frequent tokens like `the` with high probability before pairs are even
generated, so the model does not spend most of its updates learning that
everything is near `the`.

## What is actually learned

There are **two** embedding matrices, and this surprises people. Every word has
a vector for when it is the centre and a different vector for when it is
context. The dot product in the objective is always between one of each.

The reason is structural. If a single matrix were used, a word's similarity
with itself would be its own squared norm, which the objective would then try
to make large &mdash; and a word does not usually appear next to itself. Two
matrices break that. Almost every implementation throws away the context matrix
at the end and keeps the centre vectors, which is a convention rather than a
derivation; GloVe, on the next page, sums the two instead.

Push the step slider in the explorer from 0 upward and watch the neighbour
table settle. At 0 the nearest word to `king` is whatever the random
initialisation happened to put nearby. By a few thousand steps `queen` has
arrived, and it arrived because those two words genuinely appear in the same
positions in this corpus &mdash; `the ___ rules the kingdom` fits both.

The scatter plot is a projection, and the caption says so. With 8 dimensions
trained and 2 drawn, points that look adjacent may not be; the cosine table
below it is the real answer. Set the dimension slider to 2 and the projection
becomes the space itself &mdash; and the vectors get noticeably worse, because
2 dimensions cannot hold enough distinct directions.

## The analogy result, and how much to believe

`king - man + woman ~ queen` is the demonstration that made word2vec famous.
The geometry is real: consistent differences between related word pairs do show
up as roughly parallel offsets in the space, because those pairs really do
differ in their contexts in consistent ways.

It is also weaker than the headline suggests. The standard evaluation excludes
the three input words from the answer candidates, and without that exclusion the
nearest vector to `king - man + woman` is very often `king` itself. Analogies
work well for frequent, well-attested relations and poorly for rare ones. The
corpus here is far too small to show the effect at all, which is the honest
outcome and is why the explorer does not offer an analogy box.

The other well-documented finding is that these vectors absorb the biases in
the text they were trained on, in exactly the same geometry: occupational
analogies from news corpora reproduce the gender distribution of those
occupations in the corpus. That is not a flaw in the algorithm. The algorithm
is doing its job; it is reporting what the corpus contains.

```python
from gensim.models import Word2Vec

sentences = [s.split() for s in corpus]

model = Word2Vec(
    sentences,
    vector_size=100,   # 100-300 is the usual range
    window=5,          # +/- 5 tokens
    sg=1,              # 1 = skip-gram, 0 = CBOW
    negative=5,        # negative samples per positive pair
    ns_exponent=0.75,  # the unigram^0.75 noise distribution
    sample=1e-3,       # subsample tokens more frequent than this
    min_count=5,       # ignore words seen fewer than five times
    epochs=5,
)

model.wv.most_similar("king", topn=5)
```

`min_count=5` is the setting people regret leaving at 1. A word seen once has a
vector determined almost entirely by its initialisation, and keeping thousands
of them adds noise to every nearest-neighbour query while inflating the model.

## Choosing the window, and what it changes

The window size is not a tuning knob in the usual sense. It changes what kind
of similarity the vectors encode.

A **small window** (1&ndash;2) makes a word's context almost entirely
syntactic: what can grammatically appear beside it. Vectors trained this way
put words of the same part of speech together, and the nearest neighbours of a
verb are other verbs in the same tense.

A **large window** (8&ndash;10) makes the context topical: what tends to appear
in the same passage. Neighbours become words about the same subject regardless
of grammatical role, so `doctor` sits near `hospital` and `patient` rather than
near other nouns in general.

Neither is correct. If the vectors feed a parser, small is right; if they feed
a topic classifier or a retrieval system, large is. Move the window control in
the explorer and watch the pair count change &mdash; and note that on nineteen
sentences even a window of 4 is reaching most of the way across a sentence, so
the distinction only appears at a realistic corpus size.

The related setting is what counts as a context at all. word2vec uses linear
context &mdash; the tokens either side. Replacing that with **dependency
context**, the words a syntactic parse links to, produces vectors whose
neighbours are functionally rather than topically similar; that is the
Levy and Goldberg result, and it is the clearest demonstration that "similar"
in a word vector means "similar under whatever context you defined".

## Where this leads

Word2vec vectors are **static**: one vector per word type, so `bank` in "river
bank" and "bank account" get the same one. That single limitation is what the
next decade of the field was about. ELMo made the vector depend on the
sentence; BERT made it depend on the whole sentence in both directions; every
transformer since produces contextual embeddings by construction.

The idea that survived intact is the one at the top of this page: **define a
prediction task that the raw data already answers, and the representation falls
out as a side effect**. Masked language modelling is that idea. So is next-token
prediction, and so is contrastive learning in vision. Word2vec is where it was
first made to work at scale.
""",
    [
        {"q": "Why is negative sampling used instead of the full softmax?",
         "options": ["It gives better vectors",
                     "The softmax denominator requires a dot product against "
                     "every word in the vocabulary on every step; negative "
                     "sampling costs k+1 dot products",
                     "It avoids overfitting",
                     "It removes the need for two embedding matrices"],
         "answer": 1,
         "why": "It replaces one multi-class question over 100,000 words with "
                "k+1 binary questions: is this pair real or invented. That is "
                "what made training on billions of tokens feasible."},
        {"q": "What supplies the labels for word2vec training?",
         "options": ["Human annotation",
                     "The corpus itself - each word's neighbours are its "
                     "targets, so unlabelled text becomes a supervised dataset",
                     "A pretrained model",
                     "A dictionary"],
         "answer": 1,
         "why": "This is the distributional hypothesis turned into a training "
                "objective, and it is the same idea that masked language "
                "modelling and next-token prediction later scaled up."},
        {"q": "Why does word2vec learn two vectors per word?",
         "options": ["One for training and one for inference",
                     "A centre vector and a context vector; with a single "
                     "matrix a word's similarity with itself would be its own "
                     "squared norm, which the objective would push upward",
                     "To support both skip-gram and CBOW",
                     "For numerical stability"],
         "answer": 1,
         "why": "The dot product in the objective is always between a centre "
                "vector and a context vector. Most implementations discard the "
                "context matrix at the end - a convention, not a derivation. "
                "GloVe sums them instead."},
        {"q": "What is the fundamental limitation these vectors have?",
         "options": ["They are too large",
                     "They are static: one vector per word type, so 'bank' has "
                     "the same vector in 'river bank' and 'bank account'",
                     "They cannot be trained on large corpora",
                     "They require labelled data"],
         "answer": 1,
         "why": "One vector per type, no matter the sentence. Removing that "
                "limitation - making the vector depend on context - is what "
                "ELMo, BERT and every transformer since are for."},
    ],
    refs=[("Efficient Estimation of Word Representations in Vector Space",
           "Mikolov, Chen, Corrado & Dean, 2013",
           "https://arxiv.org/abs/1301.3781"),
          ("Distributed Representations of Words and Phrases and their "
           "Compositionality", "Mikolov, Sutskever, Chen, Corrado & Dean, "
           "NeurIPS 2013", "https://arxiv.org/abs/1310.4546"),
          ("gensim: Word2Vec", "gensim documentation",
           "https://radimrehurek.com/gensim/models/word2vec.html")],
    description="Train skip-gram with negative sampling in the page and watch "
                "the nearest neighbour of 'king' become 'queen' as the step "
                "count rises."))


# ---------------------------------------------------------------------------
# 2. GloVe
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "glove",
    "natural_language_processing",
    "GloVe",
    "Word vectors",
    "Counts, ratios, and a weighted least-squares fit",
    "Build the co-occurrence matrix from the corpus, then see the probability "
    "ratio that motivates the whole objective computed from those counts.",
    svg("".join(box(20 + c * 12, 16 + r * 12, 11, 11,
                    fill=(A if (r + c) % 3 == 0 else S), sw=0.8, rx=0)
                for r in range(4) for c in range(5))
        + line(86, 40, 100, 40, A, 1.4)
        + txt(128, 32, "log X", A, 9)
        + txt(128, 46, "w . w~ + b", M, 8)
        + txt(80, 80, "fit vectors to the counts", M, 7)),
    {"widget": "glove"},
    [
        "word2vec never sees a corpus-level number. GloVe starts from one: the "
        "full co-occurrence count matrix.",
        "The motivating quantity is a <em>ratio</em> of conditional "
        "probabilities, because a raw probability is dominated by how common "
        "the word is.",
        "<code class='mono-font'>f(x)</code> is zero at zero, which is the "
        "only reason the objective can be a sum over counts at all &mdash; "
        "log 0 is undefined.",
        "The released vectors are 6B to 840B tokens and 50 to 300 dimensions. "
        "Nineteen sentences is not global statistics, and the page says so.",
    ],
    r"""
title: GloVe
intro: Start from the corpus-wide count matrix instead of one window at a time, and fit vectors to the logarithm of it.

## Two families, one goal

By 2014 there were two ways to get word vectors and they came from different
traditions.

**Count-based** methods build a word-by-word co-occurrence matrix over the
whole corpus and factorise it &mdash; LSA and its relatives. They use the
global statistics efficiently, and they had historically done badly on analogy
tasks.

**Prediction-based** methods slide a window and train on local pairs &mdash;
word2vec. They did well on analogies, and they never look at a corpus-level
number: the same pair seen in ten thousand windows produces ten thousand
separate gradient steps, and the model never learns the count itself.

GloVe is the argument that this is a false choice. Its name is short for
*global vectors*, and it takes the count matrix as its starting point while
keeping the vector arithmetic that made word2vec work.

## Counting

The matrix `X` has `X_ij` = the number of times word j appears in the context
of word i. The heatmap in the explorer is that matrix for the corpus below,
restricted to fifteen readable words. Click any cell to see its value.

One refinement: neighbours are weighted by **1/d**, so a word four positions
away contributes a quarter of what an adjacent word does. That is why the cells
hold fractions rather than integers. It encodes something obviously true &mdash;
proximity is evidence, and distance weakens it &mdash; without the hard cutoff
that a plain window imposes.

Move the window slider and watch the matrix fill in. This is already a
difference in kind from word2vec: the entire corpus has been summarised into
one object before any learning starts, and the training loop never touches the
text again.

## The idea: ratios, not probabilities

Here is the observation the paper is built on. Take the conditional probability
`P(k | c)` &mdash; how often word k appears near word c &mdash; and look at the
table in the explorer for `cat` against `dog`:

| word k | P(k \| cat) | P(k \| dog) | ratio |
|---|---|---|---|
| mouse | large | zero | very large |
| bread | zero | large | very small |
| sits | moderate | moderate | about 1 |
| the | large | large | about 1 |

The individual probabilities are useless. `P(the | cat)` is large, and so is
`P(the | dog)`, and so is `P(the | anything)`, because `the` is everywhere. Its
size tells you about `the`, not about cats.

The **ratio** cancels that out. Words that both cats and dogs occur near give a
ratio near 1 and are correctly reported as uninformative. Words specific to one
give a ratio far from 1. The signal you want is not in either probability; it
is in their quotient.

This is the paper's own worked example with `ice` and `steam` against `solid`,
`gas`, `water` and `fashion`, recomputed here on a corpus you can read in full.
Switch the probe pair to `king` / `queen` or `paris` / `berlin` to see the same
structure appear elsewhere.

## From ratios to an objective

The derivation asks: what function of word vectors depends on a ratio of
probabilities? Ratios divide, and the natural vector operation that turns
division into subtraction is the logarithm, so a function of `w_i - w_j` dotted
with a context vector is the shape to aim for. Following that requirement
through &mdash; and requiring the answer to be symmetric under swapping the
roles of centre and context, since the choice is arbitrary &mdash; lands on:

```
w_i . w~_j + b_i + b~_j = log X_ij
```

Vectors and biases whose dot product reproduces the log of the count. That is a
least-squares problem, and the explorer prints it for the cell you click.

The bias terms are doing real work: they absorb the fact that a common word has
large counts with everything, so the dot product does not have to encode
frequency alongside meaning.

## The weighting function does two jobs

A plain least-squares fit over all of `X` fails for two reasons, and one
function fixes both:

```
f(x) = (x / x_max)^alpha   if x < x_max,   otherwise 1
```

**It is zero at zero.** Most of the matrix is zeros &mdash; most word pairs
never co-occur &mdash; and `log 0` is undefined. Weighting those terms by zero
removes them from the sum entirely. Click a cell in the explorer with a count
of zero and the note tells you the term is dropped; without `f(0) = 0` there
would be no objective to optimise.

**It stops rising past x_max.** Without a cap, the handful of enormous counts
involving `the` and `of` would dominate the entire loss and every other word
pair would be fitted incidentally. Capping the weight bounds their influence.

The paper's values are `x_max = 100` and `alpha = 0.75` &mdash; and that 0.75
is the same exponent word2vec uses on its noise distribution, arrived at
independently for the same underlying reason. Both controls are sliders in the
explorer, and the curve redraws as you move them.

## Honest results on a tiny corpus

The training section fits the objective with AdaGrad, exactly as the paper
does, and then shows the nearest neighbours. Some are right &mdash;
`man`/`woman`, `paris`/`berlin` &mdash; and some are noise.

That is not a bug in the page. It is what a global-statistics method does with
nineteen sentences: it can only know what the counts know, and a pair seen once
contributes one term to a least-squares fit and is then done. Word2vec is
comparatively more robust on tiny data because the same pair gets many
independent gradient steps. The released GloVe vectors were trained on between
6 billion and 840 billion tokens, and the gap between that and this page is the
gap between "global statistics" and "a handful of counts".

The final vectors are `w + w~`, summing the two sets rather than discarding
one. The paper reports this as a small consistent gain, on the argument that
the two sets differ only by their random initialisation and averaging them
reduces noise.

```python
import numpy as np

# The released vectors are a plain text file: word, then the components.
vectors = {}
with open("glove.6B.100d.txt", encoding="utf-8") as fh:
    for row in fh:
        parts = row.rstrip().split(" ")
        vectors[parts[0]] = np.asarray(parts[1:], dtype=np.float32)

def nearest(word, n=5):
    v = vectors[word]
    v = v / np.linalg.norm(v)
    scored = []
    for other, u in vectors.items():
        if other == word:
            continue
        scored.append((float(v @ (u / np.linalg.norm(u))), other))
    scored.sort(reverse=True)
    return scored[:n]
```

Normalise before comparing. Cosine similarity is the standard measure for these
vectors and the raw dot product is not the same thing &mdash; vector norm
correlates with word frequency, so an unnormalised comparison quietly ranks
common words higher.

## What the biases are for

The two bias terms in the objective are easy to skip past and they are doing
something specific.

Write the objective again:

```
w_i . w~_j + b_i + b~_j = log X_ij
```

Without `b_i` and `b~_j`, the dot product would have to account for the fact
that `the` co-occurs enormously with everything &mdash; not because it is
related to everything, but because it is common. The vector for `the` would be
pushed to have a large component in every direction, which is both meaningless
and destructive: it distorts every other vector fitted against it.

The biases absorb exactly that. `b_i` learns "word i is frequent", `b~_j`
learns the same for the context role, and the dot product is left to explain
only what those cannot &mdash; the part of the count that is specific to the
*pair*. This is the same decomposition that appears in the recommender
literature as user and item biases, and for the same reason: the main effects
should be modelled separately from the interaction, or the interaction spends
its capacity re-learning them.

Click a row of the matrix in the explorer for a common word and then for a rare
one, and compare the `log X` values the fit is being asked to reproduce. The
range across a real corpus spans several orders of magnitude, and no bounded
dot product would cover it on its own.

## Which to use

For most purposes: neither, on their own. Contextual embeddings from a
transformer are better at nearly everything, because a static vector per word
type cannot represent a word with two senses.

Static vectors still earn their place where the constraints are tight. They are
a lookup table &mdash; no forward pass, no GPU, microseconds per word. They are
interpretable enough to debug. And they are a reasonable initialisation for the
embedding layer of a small model trained on little data. Between the two, GloVe
and skip-gram perform similarly on most benchmarks once the corpus and
dimension are matched, and the practical difference is that GloVe's training
parallelises trivially over the count matrix while word2vec streams text.
""",
    [
        {"q": "Why does GloVe's derivation start from a ratio of probabilities "
              "rather than a probability?",
         "options": ["Ratios are easier to compute",
                     "A raw conditional probability is dominated by how common "
                     "the word is; the ratio cancels that and leaves only what "
                     "distinguishes the two contexts",
                     "Probabilities can be zero",
                     "It makes the objective convex"],
         "answer": 1,
         "why": "P(the | cat) and P(the | dog) are both large and tell you "
                "about 'the'. Their ratio is about 1, correctly reporting that "
                "'the' distinguishes nothing. P(mouse | cat) / P(mouse | dog) "
                "is enormous, and that is the signal."},
        {"q": "What is the weighting function f(x) for?",
         "options": ["Normalising the vectors",
                     "It is zero at zero, so pairs that never co-occur are "
                     "dropped rather than requiring log 0; and it caps the "
                     "influence of very frequent pairs",
                     "Preventing overfitting",
                     "Setting the learning rate"],
         "answer": 1,
         "why": "Both jobs at once. Most of the count matrix is zeros, so f(0) "
                "= 0 is what makes the sum well defined at all, and the cap "
                "stops 'the' and 'of' from dominating the loss."},
        {"q": "What is the main structural difference from word2vec?",
         "options": ["GloVe uses a neural network",
                     "GloVe fits corpus-wide co-occurrence counts once; "
                     "word2vec makes a gradient step per window and never sees "
                     "a corpus-level number",
                     "GloVe needs labelled data",
                     "GloVe produces contextual embeddings"],
         "answer": 1,
         "why": "That is the 'global' in global vectors. It also means GloVe "
                "training parallelises over the count matrix, while word2vec "
                "streams text - and that GloVe is weaker on tiny corpora, "
                "where a pair seen once contributes one term and is done."},
        {"q": "The final GloVe vector for a word is w + w~. Why sum them?",
         "options": ["To double the dimension",
                     "The two sets differ mainly by their random "
                     "initialisation, so averaging them reduces noise - the "
                     "paper reports a small consistent gain",
                     "Because the biases require it",
                     "To make the vectors unit length"],
         "answer": 1,
         "why": "The objective is symmetric in the two roles, so neither set is "
                "privileged. word2vec discards the context matrix instead, "
                "which is a convention rather than a result."},
    ],
    refs=[("GloVe: Global Vectors for Word Representation",
           "Pennington, Socher & Manning, EMNLP 2014",
           "https://nlp.stanford.edu/pubs/glove.pdf"),
          ("GloVe project page", "Stanford NLP",
           "https://nlp.stanford.edu/projects/glove/")],
    description="Build the co-occurrence matrix, see the probability ratio "
                "that motivates GloVe computed from real counts, and fit the "
                "log-bilinear objective."))


# ---------------------------------------------------------------------------
# 3. Seq2Seq
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "seq2seq_architecture",
    "natural_language_processing",
    "Seq2Seq",
    "Encoder-decoder",
    "The encoder, the decoder, and the vector between them",
    "The fixed-vector bottleneck, measured rather than asserted: perturb each "
    "input token and see how much of it survives to the final state.",
    svg(stack(14, 30, 14, [22, 22, 22, 22], gap=4)
        + box(78, 34, 20, 14, fill=A, sw=0)
        + stack(106, 30, 14, [22, 22, 22], gap=4)
        + txt(45, 24, "encoder", M, 7) + txt(122, 24, "decoder", M, 7)
        + txt(88, 62, "one vector", A, 7)
        + txt(80, 82, "everything must fit through it", M, 7)),
    {"widget": "seq2seq"},
    [
        "The encoder's job is to end in a state that contains the sentence. "
        "The decoder's job is to unpack it.",
        "Without attention, the only thing crossing the middle is the final "
        "hidden state &mdash; a fixed number of floats, whatever the sentence "
        "length.",
        "The influence bars are measured, not drawn: each token is perturbed "
        "and the shift in the final state is the bar.",
        "Attention does not replace the encoder. It keeps the per-step states "
        "the encoder was already computing and discarding.",
    ],
    r"""
title: Seq2Seq
intro: Two recurrent networks and a vector between them - and a measurement of exactly how much the sentence loses on the way through.

## Why a new architecture was needed

A plain recurrent network maps a sequence to a sequence of the same length. It
tags parts of speech well and it labels named entities well, because those
tasks have one output per input.

Translation does not. "I do not speak French" is five English words and four
French ones; the verb moves; the negation is one word in one language and two
in the other. The output length is not known until the output is produced, and
the alignment is not monotonic.

Sutskever, Vinyals and Le's answer in 2014 was to split the problem. One
network **reads** the source and stops, leaving its final hidden state. A
second network **writes** the target, starting from that state, one token at a
time, each token conditioned on the ones already emitted. Reading and writing
are decoupled, so the lengths need not match.

The training signal is the same one a language model uses: at each decoder
step, predict the next target token, with the loss being cross-entropy against
the real one. During training the decoder is fed the *true* previous token
rather than its own guess &mdash; **teacher forcing** &mdash; which makes the
gradient well behaved and creates the exposure-bias problem, because at
inference the decoder must consume its own mistakes.

## The bottleneck, measured

The objection is immediate. A fifty-word sentence and a five-word sentence both
have to be compressed into the same fixed vector. Where does the extra
information go?

Most explanations stop at asserting that it is lost. The explorer measures it.

The encoder is a real recurrent network with fixed weights, so its hidden
states are genuine computed values. To find out how much a given input token
still matters at the end, the widget flips that token's embedding, re-runs the
encoder, and measures how far the final state moved. That distance is the bar
under each word.

Watch two things:

- **Push the sentence length up.** The bars at the front of the sentence
  flatten toward nothing. The statistic reports the ratio of average influence
  in the last third against the first third; at length 7 it is close to 1, and
  by length 40 it is large.
- **Push the hidden size down.** The same decay happens faster, because there
  are fewer directions in the state to keep things separate in.

The mechanism is not mysterious. The state is overwritten at every token, and
whatever an early word contributed has been multiplied by the recurrent weight
matrix once per subsequent token. If that matrix contracts &mdash; and a stable
recurrence generally does &mdash; then a hundred multiplications is
annihilation. LSTM and GRU gates were designed to hold a value against exactly
this, and they push the horizon out considerably, but they do not remove it.

The original paper's own workaround is worth knowing because it is so blunt:
they **reversed the source sentence**. Feeding "sentence the reversed" puts the
first source words nearest the end of the encoding, next to the first target
words the decoder must produce, and this alone improved BLEU by several points.
That a trick like that works is the clearest possible evidence that the
bottleneck was real.

## Attention, as a small change

Turn **Attention** on in the explorer and look at what actually changed. The
encoder is identical. It still reads left to right, still produces one hidden
state per token.

The difference is that those per-step states are **kept** rather than discarded.
At each decoder step, the decoder computes a score against every encoder state,
softmaxes the scores into weights that sum to 1, and reads a weighted average
&mdash; the *context vector* &mdash; which it uses alongside its own state.

```
score_j   = f(decoder state, encoder state j)
weight_j  = softmax over j of score_j
context   = sum over j of weight_j * encoder state j
```

Nothing has to survive to the end of the sentence any more, because nothing has
to travel. The channel between the two networks stops being H numbers and
becomes n&times;H numbers, growing with the input rather than being fixed
against it. The statistic in the explorer reports both.

The attention bars for the current decoder step show which source words that
step is reading. The weights sum to 1 by construction, so attention is always a
question of *allocation*: attending more to one word necessarily means
attending less to another.

## What this became

Read the attention equation again with the encoder removed and it is the whole
of a transformer. Bahdanau's attention computes a compatibility between one
query and a set of keys, softmaxes it, and averages the values. Scaled
dot-product attention is that with `f` fixed to a dot product and divided by
&radic;d&#8342;, and self-attention is that with the query coming from the same
sequence as the keys.

The 2017 paper's title &mdash; "Attention Is All You Need" &mdash; is a claim
about this page: that once you have attention, the recurrence it was bolted
onto is not carrying its weight. Removing it makes the whole sequence
computable in parallel rather than one step at a time, which is the change that
made scale possible.

```python
import torch
import torch.nn as nn

class Encoder(nn.Module):
    def __init__(self, vocab, emb=256, hidden=512):
        super().__init__()
        self.embed = nn.Embedding(vocab, emb)
        self.rnn = nn.GRU(emb, hidden, batch_first=True, bidirectional=True)

    def forward(self, src):
        # outputs: the per-step states attention needs, [B, T, 2H]
        # h: the final state, all the no-attention decoder ever gets, [2, B, H]
        outputs, h = self.rnn(self.embed(src))
        return outputs, h

class Attention(nn.Module):
    def __init__(self, hidden=512):
        super().__init__()
        self.project = nn.Linear(hidden * 2, hidden)

    def forward(self, query, keys, mask):
        # query [B, H], keys [B, T, 2H]
        scores = torch.bmm(self.project(keys), query.unsqueeze(2)).squeeze(2)
        scores = scores.masked_fill(mask == 0, float("-inf"))   # ignore padding
        weights = torch.softmax(scores, dim=1)
        return torch.bmm(weights.unsqueeze(1), keys).squeeze(1), weights
```

The `masked_fill` line is the one that is quietly essential. Batched sequences
are padded to equal length, and without the mask the softmax spreads probability
onto padding tokens &mdash; the model learns to attend to nothing, and the bug
shows up as mysteriously poor translation of short sentences in a batch of long
ones.

## Teacher forcing and the gap it leaves

One detail of how these models are trained shapes how they fail, and it is
invisible in the architecture diagram.

During training the decoder is fed the **true** previous target token at every
step. Feeding it its own previous prediction instead would mean that early in
training it conditions on nonsense, and learning never gets started. Teacher
forcing avoids that and makes every step's gradient independent of the
others, which is also what lets the whole target sequence be processed in
parallel.

At inference there is no true previous token. The decoder must consume its own
output, which means it is operating on a distribution of prefixes it never saw
during training &mdash; **exposure bias**. One mistake shifts the context away
from anything familiar, and the errors compound: a model that is 95% accurate
per token is far worse than 95% accurate per twenty-token sentence.

The mitigations are all partial. **Scheduled sampling** mixes in the model's
own predictions during training with a probability that rises over time.
Sequence-level training optimises a metric like BLEU on generated output
directly, using reinforcement learning because the metric is not
differentiable. And in practice, **beam search** helps more than either,
because keeping several hypotheses alive means one bad token does not
irrecoverably determine the rest &mdash; which is the subject of the next
module.

## What to carry forward

Three ideas from this architecture outlived it entirely. **Encoder-decoder** as
a shape, for any task where input and output are both sequences of unrelated
length. **Teacher forcing** and its exposure-bias problem, which is why
scheduled sampling and reinforcement-learning fine-tuning exist. And
**attention**, which started as a patch for a fixed vector that was too small
and ended up replacing the network it was patching.
""",
    [
        {"q": "What exactly is the bottleneck in a seq2seq model without "
              "attention?",
         "options": ["The vocabulary size",
                     "The decoder only ever sees the encoder's final hidden "
                     "state - a fixed number of values regardless of how long "
                     "the source was",
                     "Teacher forcing",
                     "The embedding dimension"],
         "answer": 1,
         "why": "A five-word and a fifty-word sentence are compressed into the "
                "same H numbers. The explorer measures the consequence: early "
                "tokens have progressively less influence on that final state "
                "as the sentence grows."},
        {"q": "The original paper reversed the source sentence and gained "
              "several BLEU points. What does that tell you?",
         "options": ["Reversal is a general preprocessing win",
                     "The bottleneck was real and position-dependent - putting "
                     "the first source words nearest the decoder helped because "
                     "distant tokens were being forgotten",
                     "The model was overfitting",
                     "The decoder was too small"],
         "answer": 1,
         "why": "It is a blunt workaround that only makes sense if information "
                "decays with distance from the end of the encoding. That is "
                "exactly what the influence bars in the explorer show."},
        {"q": "What does adding attention change about the encoder?",
         "options": ["It becomes bidirectional",
                     "Nothing - the encoder runs identically; its per-step "
                     "states are kept rather than discarded",
                     "It stops being recurrent",
                     "It shares weights with the decoder"],
         "answer": 1,
         "why": "The states were always being computed. Attention is the "
                "decision to keep them and read a weighted average at each "
                "decoder step, so the channel between the networks grows with "
                "the input instead of being fixed."},
        {"q": "Why do attention weights sum to 1?",
         "options": ["To keep the magnitudes stable",
                     "They come from a softmax, so attention is always an "
                     "allocation: attending more to one source word means "
                     "attending less to another",
                     "Because the encoder states are normalised",
                     "It is an arbitrary convention"],
         "answer": 1,
         "why": "The softmax makes the weights a distribution over source "
                "positions. The context vector is therefore a convex "
                "combination of encoder states - an average, never a sum that "
                "can grow without bound."},
    ],
    refs=[("Sequence to Sequence Learning with Neural Networks",
           "Sutskever, Vinyals & Le, NeurIPS 2014",
           "https://arxiv.org/abs/1409.3215"),
          ("Neural Machine Translation by Jointly Learning to Align and "
           "Translate", "Bahdanau, Cho & Bengio, ICLR 2015",
           "https://arxiv.org/abs/1409.0473")],
    description="Measure the seq2seq bottleneck directly: perturb each source "
                "token and watch how little of the early sentence survives to "
                "the final state."))


# ---------------------------------------------------------------------------
# 4. Machine translation with an encoder-decoder
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "machine_translation_encoder_decoder",
    "natural_language_processing",
    "Machine Translation with an Encoder-Decoder",
    "Encoder-decoder",
    "Alignment, then search",
    "Greedy decoding drops the negation and translates “je ne parle pas "
    "français” as “i speak french”. Widen the beam and watch it come back.",
    svg("".join(box(24 + c * 15, 14 + r * 12, 14, 11,
                    fill=(A if r == c or (r == 1 and c == 2) or (r == 2 and c == 1) else S),
                    sw=0.6, rx=0)
                for r in range(4) for c in range(4))
        + txt(52, 74, "alignment", M, 7)
        + line(96, 26, 112, 20, B, 1) + line(96, 26, 112, 34, B, 1)
        + line(112, 20, 128, 16, A, 1.4) + line(112, 20, 128, 26, B, 1)
        + line(112, 34, 128, 40, B, 1)
        + txt(120, 74, "beam", A, 7)),
    {"widget": "translation"},
    [
        "Attention weights are a soft alignment. Nobody supervised them; they "
        "fall out of translating well.",
        "Greedy decoding takes the best next token. That is not the same as "
        "the first token of the best sequence, and the difference can be the "
        "meaning.",
        "Every extra token adds a negative log-probability, so an unnormalised "
        "search prefers short output. That is what the length penalty is for.",
        "Beam search is still a heuristic. Widening the beam past about 10 "
        "usually makes translations <em>worse</em>, not better.",
    ],
    r"""
title: Machine Translation with an Encoder-Decoder
intro: Two problems, not one - deciding what each output word depends on, and deciding which output sequence to emit.

## Alignment, without an alignment model

Statistical machine translation before 2014 had an explicit alignment
component: a separate model, trained separately, deciding which source words
each target word came from. It was a whole subfield.

Neural translation deleted it, and got alignment for free. The attention
weights &mdash; trained on nothing but "predict the next target token" &mdash;
turn out to concentrate on the source words a translator would point at.

The heatmap in the explorer shows this. Every row is one target word, every
column one source word, and the row sums to 1. Look at the first sentence: `le
chat noir` becomes `the black cat`, and the alignment **crosses**, because
French puts the adjective after the noun. Target word 2 (`black`) attends to
source word 3 (`noir`). No rule encoded that; a model that mis-aligned it would
translate badly and be penalised.

The second sentence shows the harder cases. French negation wraps the verb in
two words, `ne ... pas`, where English uses one, `not` &mdash; so `not` attends
to both. And `do` has nothing at all to align to: it exists only because English
requires an auxiliary in negated sentences. Its attention is diffuse, which is
the model correctly reporting that there is no source word to point at.

The **entropy** statistic quantifies that. A sharp alignment is under about 0.6
bits; a diffuse one is higher, and the "effective sources" figure converts it
back into a count of words. Sliding the temperature control shows the two
failure modes: flatten the distribution and the context vector becomes an
average of the whole sentence, sharpen it too far and a word that genuinely
depends on two source words can only look at one.

## The second problem: which sequence?

The model gives you a probability distribution over the next token, conditioned
on the source and everything emitted so far. It does *not* give you a
translation. Turning one into the other is a search over an exponentially large
space, and it is a separate algorithm with its own settings.

**Greedy decoding** takes the highest-probability token at each step. It is
cheap, it is what people implement first, and it is wrong in a specific and
damaging way.

Select the second sentence in the explorer and set the beam width to 1. The
model's own next-token table gives, after `i`:

| next token | log p |
|---|---|
| speak | &minus;0.60 |
| do | &minus;0.70 |
| don't | &minus;1.50 |

Greedy takes `speak`, and the output is **"i speak french"** &mdash; a fluent
sentence with the opposite meaning, because the negation is gone and there is
no way back. Widen the beam to 3 and `do` stays alive; it leads to `not`,
`speak`, `french`, and a total log-probability of &minus;1.22 against greedy's
&minus;2.25.

That is the entire argument for beam search, and the example is chosen because
the failure is *semantic*. Greedy decoding does not produce noticeably worse
grammar. It produces confident, well-formed sentences that mean something else.

## How beam search works

Keep the k best partial sequences at every step. Expand each with every
possible next token, score all the candidates, keep the best k again, and
continue until they have all emitted end-of-sequence.

The tree in the explorer draws this. Each row is one step, the surviving beams
are the boxes, and the edges show which parent each came from. The best-scoring
beam is highlighted, and you can watch it change parent partway down &mdash;
which is exactly the moment beam search does something greedy cannot.

Two things are worth knowing about the width. It is *not* exact search: beam
search offers no guarantee of finding the highest-probability sequence, because
a sequence whose prefix falls out of the top k at any step is gone forever. And
increasing it does not monotonically help. Past roughly 10, translation quality
measured by BLEU typically *degrades*, which is a well-documented and slightly
uncomfortable result: the model's true highest-probability output tends to be
short and dull, and a narrow beam's failure to find it is doing useful work.
The statistic in the explorer comparing your beam against beam 5 is there to
make the point that wider is often just the same answer for more compute.

## The length penalty

Every token multiplies another probability below 1, so a longer sequence has a
lower total probability, always. Unnormalised, the search therefore prefers to
stop early &mdash; it will truncate rather than finish the sentence.

Set the length penalty **alpha to 0** in the explorer on the first sentence.
The winning beam becomes "the cat", with a total log-probability of
&minus;1.72, beating the full "the black cat sleeps on the mat" at &minus;2.10.
The short output is not better; it is shorter.

The standard fix divides the score by a function of length:

```
score = (sum of log probabilities) / ((5 + |Y|) / 6) ^ alpha
```

At alpha = 0.7 the full sentence scores &minus;1.225 against the truncation's
&minus;1.409, and wins. Push alpha past 1 and the correction over-corrects: the
model starts padding, because length is now rewarded on its own.

This is a genuine hyperparameter with no principled value, tuned on a
development set, and it is the reason two implementations of "the same" model
produce different output.

```python
import torch

def beam_search(model, src, beam=4, alpha=0.7, max_len=64, eos=2):
    beams = [([bos], 0.0)]
    finished = []
    for _ in range(max_len):
        candidates = []
        for seq, logp in beams:
            if seq[-1] == eos:
                finished.append((seq, logp)); continue
            logits = model(src, torch.tensor([seq]))[0, -1]
            for tok, lp in zip(*logits.log_softmax(-1).topk(beam)):
                candidates.append((seq + [int(tok)], logp + float(lp)))
        if not candidates:
            break
        # Normalise by length BEFORE ranking, or short sequences always win.
        candidates.sort(key=lambda c: c[1] / ((5 + len(c[0])) / 6) ** alpha,
                        reverse=True)
        beams = candidates[:beam]
    finished.extend(beams)
    return max(finished, key=lambda c: c[1] / ((5 + len(c[0])) / 6) ** alpha)[0]
```

The comment marks the mistake that is easiest to make: normalising after
selection rather than before means the pruning at every step still has the
short-sequence bias, and the penalty only affects the final pick.

## Why it stops

One mechanical detail decides how long the output is, and it is not a length
parameter.

The target vocabulary contains a special end-of-sequence token, and it is
predicted like any other word. The model has learned, from the training data,
that after a complete sentence the most likely next token is the one that ends
it. Generation stops when that token is emitted &mdash; or when a maximum
length is hit, which is a safety net rather than the intended path.

This is why the length penalty operates where it does. The competition is
between emitting end-of-sequence now and emitting another content word, and
both are just entries in the same distribution. When the accumulated
log-probability is the score, stopping is always locally attractive, because it
is the only choice that stops making the score worse.

Watch the beam table with the first sentence and alpha at 0: the winning
sequence ends after two words, with `</s>` scoring &minus;0.95 against
continuing. It is not that the model does not know the rest of the sentence; it
is that the search prefers not to say it.

The same mechanism produces the opposite failure in a badly-trained model.
If end-of-sequence is under-predicted &mdash; common when training data has few
short examples &mdash; generation runs to the length cap and produces a
sentence that trails off mid-clause. Both failures look like decoder problems
and are, at bottom, arithmetic about one token.

## What changed, and what did not

The recurrence in this architecture is gone &mdash; a transformer encoder and
decoder replaced it, and the attention that was one component became the whole
model. Word-level vocabularies are gone too, replaced by subword tokenisation,
which is what stopped translations containing `<unk>` for every rare name.

Everything on the second half of this page survived unchanged. A transformer
still produces a distribution over the next token and still needs a search over
sequences to turn that into output. Beam width and length penalty are still
tuned per model. And a large language model generating text is doing exactly
this, usually with sampling instead of beam search &mdash; temperature, top-k
and nucleus sampling are alternative answers to the same question this page
asks: given a next-token distribution, which sequence do you actually emit?
""",
    [
        {"q": "Greedy decoding translates “je ne parle pas français” as “i "
              "speak french”. What went wrong?",
         "options": ["The attention weights were wrong",
                     "It took the highest-probability second token, which is "
                     "not the first token of the highest-probability sequence, "
                     "and there is no way back",
                     "The model was undertrained",
                     "The length penalty was too high"],
         "answer": 1,
         "why": "'speak' scores better than 'do' at that step. But 'do' leads "
                "to 'do not speak french', which is a far better sequence "
                "overall. Greedy search cannot see past one step, and the "
                "resulting error is semantic, not grammatical."},
        {"q": "Why does an unnormalised beam search prefer short output?",
         "options": ["Short sentences are more common in training",
                     "Every additional token adds another negative log "
                     "probability, so longer sequences always score lower",
                     "The end-of-sequence token has high probability",
                     "The beam fills up"],
         "answer": 1,
         "why": "It is arithmetic, not a modelling issue. Dividing by "
                "((5 + |Y|) / 6)^alpha compensates; alpha is tuned on a "
                "development set and has no principled value."},
        {"q": "Where do the attention alignments come from?",
         "options": ["A separate alignment model trained on word pairs",
                     "They emerge from training on next-token prediction alone "
                     "- nothing supervises them",
                     "Hand-written rules per language pair",
                     "The tokeniser"],
         "answer": 1,
         "why": "Classical statistical MT had an explicit alignment component. "
                "Neural MT deleted it and got alignment as a side effect of "
                "translating well - which is why the French adjective-after-noun "
                "order shows up as a crossing in the heatmap."},
        {"q": "Increasing the beam width past about 10 usually makes BLEU "
              "worse. Why is that surprising?",
         "options": ["It is not surprising - wider beams are slower",
                     "A wider beam is strictly better at finding "
                     "high-probability sequences, so it means the model's "
                     "highest-probability output is not its best output",
                     "Because the length penalty compensates",
                     "Because attention degrades"],
         "answer": 1,
         "why": "Search is doing its job better and the result gets worse, "
                "which points at the model rather than the search: the true "
                "mode of the distribution tends to be short and generic, and a "
                "narrow beam's failure to find it is accidentally helpful."},
    ],
    refs=[("Neural Machine Translation by Jointly Learning to Align and "
           "Translate", "Bahdanau, Cho & Bengio, ICLR 2015",
           "https://arxiv.org/abs/1409.0473"),
          ("Google's Neural Machine Translation System: Bridging the Gap "
           "between Human and Machine Translation", "Wu et al., 2016",
           "https://arxiv.org/abs/1609.08144"),
          ("Six Challenges for Neural Machine Translation",
           "Koehn & Knowles, First Workshop on Neural Machine Translation 2017",
           "https://arxiv.org/abs/1706.03872")],
    description="Watch attention align a French sentence to its English "
                "translation, then see greedy decoding drop the negation and "
                "beam search recover it."))
