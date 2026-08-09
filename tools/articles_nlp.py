# -*- coding: utf-8 -*-
"""Written explanations for the NLP track.

Nine pages here were under 400 words of prose. The recurrent-network pages in
particular carried a heavy visualisation and two paragraphs of text, which is
the wrong way round for the ideas involved.

Rendered by tools/build_articles.py. Edit here, then `npm run build`.
"""

ARTICLES_NLP = {

# ---------------------------------------------------------------------------
"natural_language_processing/what_is_a_recurrent_cell.html": {
 "intro": "A recurrent cell is a small network that runs once per token and passes a summary of everything it has seen to its future self. That loop is what lets a fixed-size model read a sequence of any length.",
 "sections": [
  ("The problem with feeding a sentence to a normal network",
   "<p>A feedforward network has a fixed number of inputs. A sentence does not have a fixed number of words. You can pad everything to a maximum length, but then the model has no notion that word 3 comes before word 4 &mdash; each position gets its own independent weights, so “dog bites man” and “man bites dog” are unrelated inputs as far as it is concerned.</p>"
   "<p>A recurrent cell solves both problems with one idea: process <em>one</em> token at a time, and carry a running summary forward.</p>"),
  ("The recurrence, written out",
   "<p>At each timestep t the cell takes the current input <span class=\"mono-font\">x<sub>t</sub></span> and the previous hidden state <span class=\"mono-font\">h<sub>t&minus;1</sub></span>, and produces a new hidden state:</p>"
   "<p class=\"mono-font\">h<sub>t</sub> = tanh(W<sub>x</sub>x<sub>t</sub> + W<sub>h</sub>h<sub>t&minus;1</sub> + b)</p>"
   "<p>Three things are worth noticing. The hidden state is the <strong>memory</strong> &mdash; a fixed-size vector holding everything the cell has decided is worth keeping from the sequence so far. The weights <span class=\"mono-font\">W<sub>x</sub></span>, <span class=\"mono-font\">W<sub>h</sub></span> and <span class=\"mono-font\">b</span> are the <strong>same at every timestep</strong>; the cell is one small network applied repeatedly, not a chain of different networks. And because the weights do not depend on position, the same cell handles a sequence of 5 tokens or 500.</p>"
   "<p>That weight sharing is what makes the parameter count independent of sequence length &mdash; and it is exactly the same trick a convolution uses across space.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>Feed one token at a time.</strong> Press <strong>Feed Next Token</strong> and watch the hidden state change. Each press mixes new input into the existing memory rather than replacing it.</li>"
   "<li><strong>Watch old information fade.</strong> Keep pressing and follow the contribution of the first token. It does not vanish at once; it is progressively diluted as later tokens are folded in. That gradual decay is exactly why plain recurrent cells struggle with long-range dependencies.</li>"
   "<li><strong>Reset and compare.</strong> Press <strong>Reset Memory</strong> and feed the same tokens in a different order. The final state differs &mdash; unlike a bag-of-words model, order genuinely changes the representation.</li>"
   "<li><strong>Run it continuously.</strong> Press <strong>Auto Run</strong> and note that no new parameters appear as the sequence lengthens. One cell, applied repeatedly.</li>"
   "</ol>"),
  ("Why the simple cell is not enough",
   "<p>The hidden state is overwritten at every step. Information from token 1 survives to token 50 only by passing through 49 successive multiplications by <span class=\"mono-font\">W<sub>h</sub></span> and 49 tanh nonlinearities.</p>"
   "<p>That is the vanishing gradient problem in its original setting. The gradient reaching timestep 1 is a product of 49 terms, and since tanh’s derivative is at most 1 and typically well below it, the product decays geometrically. In practice a simple recurrent cell reliably remembers about 10 timesteps and loses anything much further back.</p>"
   "<p>The fix is to give the cell an explicit, <em>additive</em> memory channel with learned gates controlling what enters and leaves it &mdash; which is precisely what LSTM and GRU do.</p>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Expecting long-range memory.</strong> A vanilla recurrent cell does not have it. If dependencies span more than a handful of tokens, use an LSTM, a GRU, or attention.</li>"
   "<li><strong>Exploding gradients.</strong> If <span class=\"mono-font\">W<sub>h</sub></span> has eigenvalues above 1 the repeated multiplication amplifies instead of decaying, and the loss becomes NaN. Gradient clipping is standard practice for recurrent models for exactly this reason.</li>"
   "<li><strong>Confusing the hidden state with the output.</strong> They coincide in the simplest cell, but in an LSTM the cell state and hidden state are different objects, and mixing them up is a common implementation bug.</li>"
   "<li><strong>Forgetting to reset state between sequences.</strong> Carrying the hidden state from one unrelated example into the next leaks information and quietly corrupts training.</li>"
   "</ul>"),
  ("In one line",
   "<p>A recurrent cell applies one small network at every timestep, combining the current token with a hidden state that summarises everything before it, using the same weights throughout. That gives a fixed-size model the ability to read arbitrary-length sequences and to be sensitive to order. Its weakness is that memory is overwritten multiplicatively at each step, so information decays after roughly ten timesteps &mdash; the limitation that gated cells were invented to remove.</p>"),
 ]},

# ---------------------------------------------------------------------------
"natural_language_processing/rnn_architecture.html": {
 "intro": "Unrolling a recurrent cell across time gives a network as deep as the sequence is long - sharing one set of weights the whole way. That is what makes RNNs efficient, and what makes them hard to train.",
 "sections": [
  ("Unrolling",
   "<p>An RNN is usually drawn as a cell with an arrow looping back to itself. That is compact and slightly misleading. To understand training, unroll it: draw one copy of the cell per timestep, with the hidden state flowing left to right between copies.</p>"
   "<p>Unrolled, an RNN over a 50-token sentence is a <strong>50-layer deep network</strong>. Every layer is the same layer &mdash; identical weights &mdash; but the computational graph really is that deep, and the gradient really does have to travel all the way back through it.</p>"),
  ("Counting the parameters",
   "<p>A recurrent cell with input size d and hidden size h has:</p>"
   "<p class=\"mono-font\">W<sub>x</sub>: d &times; h&nbsp;&nbsp;&nbsp;&nbsp;W<sub>h</sub>: h &times; h&nbsp;&nbsp;&nbsp;&nbsp;b: h</p>"
   "<p class=\"mono-font\">total = dh + h&sup2; + h</p>"
   "<p>With d = 100 and h = 128 that is 12,800 + 16,384 + 128 = <strong>29,312</strong> parameters &mdash; and that number does not change whether the sequence is 5 tokens or 5,000. The <span class=\"mono-font\">h&sup2;</span> term usually dominates, which is why hidden size is the expensive dimension and doubling it roughly quadruples the recurrent weights.</p>"),
  ("Backpropagation through time",
   "<p>Training unrolls the network, runs a normal forward pass, then backpropagates from the loss all the way back to timestep 1. Because the same weights appear at every step, the gradient for <span class=\"mono-font\">W<sub>h</sub></span> is the <em>sum</em> of its gradient contributions from all timesteps.</p>"
   "<p>This is called backpropagation through time, and it has two practical consequences. Memory grows linearly with sequence length, since every intermediate hidden state must be kept for the backward pass. And the gradient reaching early timesteps is a long product, so it vanishes or explodes exactly as depth causes it to in a feedforward network.</p>"
   "<p><strong>Truncated BPTT</strong> is the standard mitigation: backpropagate only k steps back, typically 20 to 50, and treat anything earlier as constant. It bounds memory and gradient depth at the cost of never learning dependencies longer than k.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>See where the parameters live.</strong> Press <strong>Parameters</strong> and read the breakdown. The recurrent matrix is the largest block, because it is h &times; h while the input matrix is only d &times; h.</li>"
   "<li><strong>Grow the hidden state.</strong> Raise <strong>Hidden State</strong> from 10 to 40 and check the parameter count again. It grows roughly with the square, not linearly &mdash; the h&sup2; term taking over.</li>"
   "<li><strong>Grow the input instead.</strong> Raise <strong>Input Vector</strong> by the same amount. The parameter count rises far less, because that dimension only appears in the d &times; h term.</li>"
   "<li><strong>Watch one step execute.</strong> Press <strong>Simulate Cell Operation</strong> and follow the two matrix multiplications combining and passing through tanh. That single operation is what gets repeated once per token, with the same weights every time.</li>"
   "</ol>"),
  ("The sequence shapes an RNN can be wired into",
   "<ul>"
   "<li><strong>Many-to-one</strong> &mdash; read the whole sequence, use only the final hidden state. Sentiment classification.</li>"
   "<li><strong>Many-to-many, aligned</strong> &mdash; one output per input. Part-of-speech tagging and named entity recognition.</li>"
   "<li><strong>Many-to-many, unaligned</strong> &mdash; an encoder reads the input into a state and a decoder generates a different-length output. Translation, and the architecture attention was invented to improve.</li>"
   "<li><strong>One-to-many</strong> &mdash; a single input generates a sequence. Image captioning.</li>"
   "</ul>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Not clipping gradients.</strong> The repeated multiplication makes explosion common. Clipping the global norm at around 1.0 is close to mandatory for recurrent models.</li>"
   "<li><strong>Padding without masking.</strong> Batching requires equal lengths, so short sequences are padded &mdash; and unless those positions are masked, the model learns from the padding and the loss is computed over meaningless tokens.</li>"
   "<li><strong>Running out of memory on long sequences.</strong> Every hidden state is retained for the backward pass. Truncate the BPTT window rather than reducing the batch to one.</li>"
   "<li><strong>Expecting parallelism.</strong> Timestep t needs the state from t&minus;1, so an RNN is inherently sequential and cannot use a GPU the way a transformer can. That, more than accuracy, is why transformers displaced them.</li>"
   "</ul>"),
  ("In one line",
   "<p>An RNN is one cell unrolled across time, sharing weights at every step, so its parameter count is fixed at dh + h&sup2; + h regardless of sequence length. Training backpropagates through the whole unrolled graph, which makes the effective depth equal to the sequence length &mdash; hence vanishing gradients, mandatory gradient clipping, and truncated BPTT. The sequential dependency is also what stops it parallelising, which is what eventually made attention the better architecture.</p>"),
 ]},

# ---------------------------------------------------------------------------
"natural_language_processing/what_is_lstm.html": {
 "intro": "An LSTM adds a separate memory channel that information can travel along unchanged, plus three learned gates deciding what to erase, what to add, and what to reveal. That additive path is why it remembers hundreds of steps.",
 "sections": [
  ("Two states, not one",
   "<p>A simple recurrent cell has one hidden state, and it is completely rewritten at every timestep. An LSTM has two:</p>"
   "<ul>"
   "<li><strong>Cell state</strong> <span class=\"mono-font\">C<sub>t</sub></span> &mdash; the long-term memory. It is modified only by addition and elementwise multiplication by a gate, never by a full matrix multiply.</li>"
   "<li><strong>Hidden state</strong> <span class=\"mono-font\">h<sub>t</sub></span> &mdash; the working output, a filtered view of the cell state, passed to the next layer and the next timestep.</li>"
   "</ul>"
   "<p>The cell state is the important one. Because it is updated additively, information placed there at timestep 1 can reach timestep 500 essentially untouched &mdash; there is no repeated matrix multiplication to shrink it.</p>"),
  ("The three gates",
   "<p>Each gate is a small sigmoid layer producing values in [0, 1], which then multiply a vector elementwise &mdash; 0 blocks completely, 1 passes completely, and everything between is a partial pass.</p>"
   "<p class=\"mono-font\">f<sub>t</sub> = &sigma;(W<sub>f</sub>&middot;[h<sub>t&minus;1</sub>, x<sub>t</sub>] + b<sub>f</sub>)&nbsp;&nbsp;&nbsp;forget</p>"
   "<p class=\"mono-font\">i<sub>t</sub> = &sigma;(W<sub>i</sub>&middot;[h<sub>t&minus;1</sub>, x<sub>t</sub>] + b<sub>i</sub>)&nbsp;&nbsp;&nbsp;input</p>"
   "<p class=\"mono-font\">o<sub>t</sub> = &sigma;(W<sub>o</sub>&middot;[h<sub>t&minus;1</sub>, x<sub>t</sub>] + b<sub>o</sub>)&nbsp;&nbsp;&nbsp;output</p>"
   "<p>The cell state update is then two operations &mdash; erase, then write:</p>"
   "<p class=\"mono-font\">C<sub>t</sub> = f<sub>t</sub> &odot; C<sub>t&minus;1</sub> + i<sub>t</sub> &odot; C&#771;<sub>t</sub></p>"
   "<p class=\"mono-font\">h<sub>t</sub> = o<sub>t</sub> &odot; tanh(C<sub>t</sub>)</p>"
   "<p>In a language model the forget gate might drop the previous subject’s gender when a new subject appears, the input gate writes the new one, and the output gate exposes it only when a pronoun actually needs to agree.</p>"),
  ("Why the gradient survives",
   "<p>The whole design rests on the additive update. Differentiating <span class=\"mono-font\">C<sub>t</sub></span> with respect to <span class=\"mono-font\">C<sub>t&minus;1</sub></span> gives <span class=\"mono-font\">f<sub>t</sub></span> &mdash; the forget gate itself, not a weight matrix.</p>"
   "<p>So the gradient flowing back through the cell state is multiplied by the forget gate at each step. When the network learns to keep something, the forget gate sits near 1, and multiplying by roughly 1 many times preserves the gradient. Compare that with a simple RNN, where the same path is multiplied by <span class=\"mono-font\">W<sub>h</sub></span> and a tanh derivative every step and decays geometrically.</p>"
   "<p>This is the same principle as a residual connection: give the gradient an uninterrupted additive route, and depth stops destroying it.</p>"),
  ("Experiments to try",
   "<ol>"
   "<li><strong>Count the cost of gating.</strong> Press <strong>Parameters</strong> and compare with a plain RNN of the same size. An LSTM has four weight matrices instead of one &mdash; three gates plus the candidate &mdash; so it needs roughly <strong>four times</strong> the parameters.</li>"
   "<li><strong>Grow the state.</strong> Raise <strong>State Size</strong> and watch the count climb. Each of the four blocks is (d + h) &times; h, so the total is 4[(d + h)h + h].</li>"
   "<li><strong>Follow one timestep.</strong> Press <strong>Simulate Cell Operation</strong> and trace the cell state along the top. It passes straight through, touched only by a multiply and an add &mdash; that unbroken line is the long-term memory path.</li>"
   "<li><strong>Watch the gates open and close.</strong> During the simulation note that gate values are between 0 and 1 rather than binary. Gating is continuous, which is what makes it differentiable and therefore learnable.</li>"
   "</ol>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>Initialising the forget-gate bias at zero.</strong> That puts the gate at 0.5, halving the cell state every step and destroying memory before training can fix it. Initialise it to 1 or 2 so the cell starts out remembering.</li>"
   "<li><strong>Reaching for an LSTM by default.</strong> A GRU merges the forget and input gates into one, uses about 25% fewer parameters, trains faster, and performs comparably on most tasks. Try it first.</li>"
   "<li><strong>Confusing cell state with hidden state.</strong> PyTorch returns both as a tuple; passing the wrong one to the next layer is a common and quiet bug.</li>"
   "<li><strong>Using an LSTM where attention belongs.</strong> For long documents a transformer both remembers further and parallelises, which an LSTM cannot.</li>"
   "</ul>"),
  ("In one line",
   "<p>An LSTM separates long-term memory (the cell state) from working output (the hidden state) and controls the flow between them with three learned sigmoid gates. Because the cell state is updated by addition and gated multiplication rather than a matrix multiply, the gradient travels back through it multiplied only by the forget gate &mdash; so when the model chooses to remember, it genuinely can, for hundreds of steps. The cost is four times the parameters of a simple cell, and a GRU usually gets most of the benefit for less.</p>"),
 ]},

# ---------------------------------------------------------------------------
"natural_language_processing/what_is_bi_directional_layer.html": {
 "intro": "Run one recurrent pass forward and another backward, then concatenate. Every position gets context from both sides - which is a large accuracy win, and rules the model out of any task that generates text.",
 "sections": [
  ("Why one direction is not enough",
   "<p>A forward RNN at position t has seen tokens 1 to t and nothing after. That is a real handicap, because disambiguation frequently depends on what comes next.</p>"
   "<p>Take “The <strong>bank</strong> was steep and muddy.” At the word <em>bank</em> a forward-only model has seen only “The”, and must commit to a representation before <em>steep and muddy</em> arrives to settle the meaning. A backward pass has that information immediately.</p>"),
  ("How the two passes combine",
   "<p>A bidirectional layer runs two entirely separate recurrent cells with their own weights. The forward cell reads left to right; the backward cell reads the same sequence right to left. At each position their hidden states are concatenated:</p>"
   "<p class=\"mono-font\">h<sub>t</sub> = [h&rarr;<sub>t</sub> ; h&larr;<sub>t</sub>]</p>"
   "<p>Two consequences follow immediately. The output at each position is <strong>twice as wide</strong>, so the next layer’s input size doubles &mdash; a frequent shape-mismatch bug. And there are <strong>twice the parameters</strong>, since nothing is shared between the two directions.</p>"
   "<p>Note the passes are independent: the backward cell does not see the forward cell’s states. They are computed separately and only joined at the end, which also means they can run in parallel.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>Watch both passes.</strong> Press <strong>Simulate Dual Passes</strong> and follow the two chains. One advances left to right, the other right to left, and they meet only where the outputs concatenate.</li>"
   "<li><strong>Confirm the doubling.</strong> Press <strong>Parameters</strong> and compare with a unidirectional cell of the same <strong>Hidden Size (Per Dir)</strong>. Exactly twice as many &mdash; two independent sets of weights.</li>"
   "<li><strong>Check the output width.</strong> Set <strong>Hidden Size (Per Dir)</strong> to 20 and note the layer emits 40 values per position. The next layer must be built for 40, not 20.</li>"
   "<li><strong>Grow the input.</strong> Raise <strong>Input Vector</strong> and watch both directions scale together. The two passes are symmetric in cost; nothing is shared or saved.</li>"
   "</ol>"),
  ("When you cannot use it",
   "<p>A bidirectional layer requires the <em>entire</em> sequence before it can produce any output, because the backward pass starts at the end. That rules it out whenever the future genuinely is not available:</p>"
   "<ul>"
   "<li><strong>Language modelling and text generation.</strong> Predicting the next token while having already read it is not a prediction. A bidirectional model here achieves perfect accuracy and learns nothing &mdash; the answer leaks in through the backward pass.</li>"
   "<li><strong>Real-time and streaming applications.</strong> Live transcription cannot wait for the end of the utterance.</li>"
   "<li><strong>Autoregressive decoding of any kind</strong>, where output is produced one token at a time.</li>"
   "</ul>"
   "<p>Where the full sequence <em>is</em> available &mdash; classification, tagging, named entity recognition, and the encoder half of a translation model &mdash; bidirectionality is close to free accuracy. This is exactly the split between BERT, which is bidirectional and cannot generate, and GPT, which is unidirectional and can.</p>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>Forgetting the output doubles.</strong> The most common bug: the following layer is sized for h instead of 2h and the shapes do not match.</li>"
   "<li><strong>Using it for generation.</strong> Training looks superb and the model is useless, because it has been shown the answer.</li>"
   "<li><strong>Padding without masking.</strong> Worse here than in a unidirectional model &mdash; the backward pass <em>starts</em> in the padding, so an unmasked model begins reading noise.</li>"
   "<li><strong>Assuming it doubles quality.</strong> It doubles cost. The accuracy gain is real but usually a few points, and on some tasks a wider unidirectional layer is the better use of the same parameters.</li>"
   "</ul>"),
  ("The short version",
   "<p>A bidirectional layer runs independent forward and backward recurrent passes and concatenates them, so every position is represented with context from both sides &mdash; at twice the parameters and twice the output width. It is the right default for classification and tagging, where the whole sequence is available, and impossible for generation or streaming, where the backward pass would be reading the future it is meant to predict.</p>"),
 ]},

# ---------------------------------------------------------------------------
"natural_language_processing/what_are_embeddings.html": {
 "intro": "An embedding maps each word to a dense vector positioned so that similar words sit close together. That geometry is what lets a model generalise from words it has seen to words it has not.",
 "sections": [
  ("What one-hot encoding cannot express",
   "<p>The obvious way to feed a word to a network is a one-hot vector: one dimension per vocabulary word, all zeros except a single 1. With a 50,000-word vocabulary each word is a 50,000-dimensional vector.</p>"
   "<p>Two problems. It is enormous and almost entirely zeros. And &mdash; the real issue &mdash; every pair of words is exactly equidistant. The vectors for <em>cat</em> and <em>kitten</em> are precisely as far apart as <em>cat</em> and <em>bulldozer</em>, because any two distinct one-hot vectors differ in exactly two positions. The representation contains no information about meaning whatsoever, so nothing learned about one word transfers to a related one.</p>"),
  ("A dense vector with learned geometry",
   "<p>An embedding replaces that with a short dense vector &mdash; typically 100 to 300 dimensions &mdash; learned during training. Now <em>cat</em> and <em>kitten</em> can be near each other while <em>bulldozer</em> is far away, and “near” is measured by cosine similarity between the vectors.</p>"
   "<p>The consequence is generalisation. If the model has learned something about sentences containing <em>cat</em>, and <em>kitten</em> sits nearby in the space, that knowledge partially transfers without <em>kitten</em> ever appearing in the same context. One-hot vectors make this structurally impossible.</p>"),
  ("The famous analogy, and what it actually shows",
   "<p>Trained embeddings encode relationships as consistent <em>directions</em>, which is why vector arithmetic works:</p>"
   "<p class=\"mono-font\">king &minus; man + woman &asymp; queen</p>"
   "<p>Subtracting <em>man</em> from <em>king</em> isolates a direction that roughly means royalty-without-gender; adding <em>woman</em> moves along the gender axis, landing near <em>queen</em>. The same holds for <span class=\"mono-font\">Paris &minus; France + Italy &asymp; Rome</span> and for grammatical relations such as singular to plural.</p>"
   "<p>Worth being precise: the result is not exactly <em>queen</em>, it is a point whose nearest neighbour is <em>queen</em>, and the effect is weaker on rare words. But it demonstrates the real claim &mdash; that these dimensions carry semantic structure learned entirely from co-occurrence, with no one ever labelling a “gender axis”.</p>"),
  ("Try it yourself",
   "<ol>"
   "<li><strong>Run the analogy.</strong> Press <strong>Run the Famous Analogy</strong> and follow the vector arithmetic. The result is a point in space, and the answer is whichever word happens to lie nearest to it.</li>"
   "<li><strong>Look at what is near what.</strong> Note which words cluster. Related terms group together not because anyone grouped them, but because they appeared in similar contexts during training.</li>"
   "<li><strong>Watch the direction, not the position.</strong> The vector from <em>man</em> to <em>woman</em> points much the same way as the vector from <em>king</em> to <em>queen</em>. It is that parallelism, repeated across many pairs, that makes the arithmetic work at all.</li>"
   "</ol>"),
  ("Static and contextual",
   "<p>Word2Vec, GloVe and FastText produce <strong>static</strong> embeddings: one fixed vector per word, forever. That breaks on polysemy &mdash; <em>bank</em> gets a single vector that averages the riverside and the financial senses, serving neither.</p>"
   "<p>BERT and every modern language model produce <strong>contextual</strong> embeddings instead: the vector for a word is computed from the sentence it appears in, so <em>bank</em> in “river bank” and “bank account” gets genuinely different representations. This is the single biggest improvement in word representation since embeddings were introduced, and it is why static embeddings are now mostly of historical and pedagogical interest.</p>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Using cosine similarity on unnormalised vectors and calling it distance.</strong> Cosine measures angle and ignores magnitude, which is usually what you want &mdash; but it is not Euclidean distance and the two rank neighbours differently.</li>"
   "<li><strong>Expecting a static embedding to handle ambiguity.</strong> One vector per word cannot represent two senses.</li>"
   "<li><strong>Ignoring inherited bias.</strong> Embeddings learn the statistical associations of their training corpus, including the prejudiced ones, and those propagate into anything built on top.</li>"
   "<li><strong>Over-large embedding dimensions on small vocabularies.</strong> 300 dimensions for 500 words is mostly free parameters to overfit with.</li>"
   "</ul>"),
  ("The short version",
   "<p>An embedding replaces a sparse, meaningless one-hot vector with a short dense one whose position encodes meaning, so similar words end up nearby and knowledge transfers between them. Relationships appear as consistent directions, which is what makes vector analogies work. Static embeddings give each word one vector and cannot handle ambiguity; contextual embeddings compute the vector from the surrounding sentence, and that is what modern models use.</p>"),
 ]},

# ---------------------------------------------------------------------------
"natural_language_processing/how_are_embeddings_generated.html": {
 "intro": "Nobody hand-labels an embedding space. It falls out of a simple prediction task: guess a word from its neighbours, and the vectors that make you good at guessing turn out to encode meaning.",
 "sections": [
  ("The distributional hypothesis",
   "<p>The whole field rests on one claim: a word is characterised by the company it keeps. Words appearing in similar contexts tend to mean similar things.</p>"
   "<p>It is easy to check. <em>Cat</em> and <em>dog</em> both appear near <em>pet</em>, <em>feed</em>, <em>vet</em> and <em>fur</em>. <em>Bulldozer</em> does not. So if you build vectors that predict a word’s context well, words with similar contexts must end up with similar vectors &mdash; the semantic structure is a by-product of the prediction task, never an objective in itself.</p>"),
  ("Skip-gram and CBOW",
   "<p>Word2Vec offers two ways to set up the prediction:</p>"
   "<ul>"
   "<li><strong>Skip-gram</strong> &mdash; given the centre word, predict the surrounding words. From “the cat sat on the mat”, given <em>sat</em>, predict <em>the</em>, <em>cat</em>, <em>on</em>, <em>the</em>. Slower, and better on rare words because each occurrence generates several training examples.</li>"
   "<li><strong>CBOW</strong> &mdash; given the surrounding words, predict the centre. Faster, and better on frequent words.</li>"
   "</ul>"
   "<p>The architecture is deliberately trivial: an input embedding layer, no hidden layer, and an output projection. The embedding matrix is the only thing anybody wants; the output layer is discarded after training. The vectors are a side effect of a task nobody cares about the answers to.</p>"),
  ("Negative sampling",
   "<p>The naive setup predicts a probability distribution over the whole vocabulary, which means a softmax over 50,000 words for every training example. That is prohibitively expensive.</p>"
   "<p><strong>Negative sampling</strong> replaces it with a much cheaper question. Instead of “which of 50,000 words is the context?”, ask “is this pair a real (word, context) pair or a fabricated one?” &mdash; a binary classification. For each true pair, draw perhaps 5 to 20 random words as negatives and train the model to score the real pair high and the fakes low.</p>"
   "<p>Cost drops from 50,000 output computations to about 20, and quality is comparable. This is what made training on billions of words practical.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>Start from noise.</strong> Press <strong>Re-randomize</strong> and look at the layout. Vectors are random, so the arrangement is meaningless &mdash; no structure exists before training.</li>"
   "<li><strong>Train one epoch.</strong> Press <strong>Train 1 Epoch</strong> and watch points shift slightly. Each step nudges words that co-occur closer together and pushes unrelated ones apart.</li>"
   "<li><strong>Let clusters form.</strong> Press <strong>Train 20 Epochs</strong>. Related words gather into groups. Nothing told the model these words were related &mdash; it only ever tried to predict context.</li>"
   "<li><strong>Re-randomize and train again.</strong> The clusters re-form, but in different positions and orientations. The absolute coordinates are arbitrary; only the relative geometry carries meaning, which is why you cannot compare vectors from two separately trained models.</li>"
   "</ol>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Comparing vectors across models.</strong> Two training runs produce different, incompatible spaces. Vectors are only meaningful relative to others from the same run.</li>"
   "<li><strong>Too little data.</strong> These methods need tens of millions of tokens. On a small corpus the vectors are noise, and a pretrained set is almost always better.</li>"
   "<li><strong>Leaving frequent words unsubsampled.</strong> <em>The</em> and <em>of</em> co-occur with everything and carry almost no information. Word2Vec subsamples them aggressively, which improves both speed and quality.</li>"
   "<li><strong>Assuming a bigger window is better.</strong> Small windows (2&ndash;5) capture syntactic similarity; large windows (10+) capture topical relatedness. They are different notions of “similar” and the right one depends on the task.</li>"
   "</ul>"),
  ("What to remember",
   "<p>Embeddings are learned by training a deliberately simple model on a proxy task &mdash; predict a word from its context, or the context from the word &mdash; and keeping the embedding matrix while discarding everything else. Semantic structure emerges because words in similar contexts need similar vectors to make the prediction work. Negative sampling replaces the vocabulary-wide softmax with a cheap binary decision, which is what made the whole approach scale.</p>"),
 ]},

# ---------------------------------------------------------------------------
"natural_language_processing/n_gram.html": {
 "intro": "Predict the next word from the previous n-1 words, by counting how often that sequence appeared. Simple, fast, interpretable - and defeated by the fact that most valid sentences have never been written down.",
 "sections": [
  ("Counting, not learning",
   "<p>An n-gram model estimates the probability of a word from the n&minus;1 words before it, using nothing but counts from a corpus:</p>"
   "<p class=\"mono-font\">P(w<sub>t</sub> | w<sub>t&minus;1</sub>, &hellip;) &asymp; count(w<sub>t&minus;n+1</sub> &hellip; w<sub>t</sub>) / count(w<sub>t&minus;n+1</sub> &hellip; w<sub>t&minus;1</sub>)</p>"
   "<p>If “the cat sat” appears 100 times and “the cat sat on” appears 60, then P(on | the cat, sat) = 0.6. There is no training in the gradient-descent sense &mdash; the model is a table of counts, built in one pass.</p>"
   "<p>The underlying simplification is the <strong>Markov assumption</strong>: that only the last n&minus;1 words matter. It is plainly false for language and works surprisingly well anyway.</p>"),
  ("Choosing n",
   "<ul>"
   "<li><strong>n = 1 (unigram)</strong> &mdash; no context at all, just word frequency. Generates word salad.</li>"
   "<li><strong>n = 2 (bigram)</strong> &mdash; one word of context. Locally plausible, globally incoherent.</li>"
   "<li><strong>n = 3 (trigram)</strong> &mdash; the traditional sweet spot, and the workhorse of speech recognition for decades.</li>"
   "<li><strong>n = 5+</strong> &mdash; better context in principle, and almost every 5-gram you meet at test time was never seen in training.</li>"
   "</ul>"
   "<p>This is a bias&ndash;variance trade in a very concrete form. Small n generalises but ignores context; large n captures context but has seen almost nothing.</p>"),
  ("The sparsity wall",
   "<p>The counts grow catastrophically. With a 50,000-word vocabulary there are 2.5 billion possible bigrams, 1.25 &times; 10<sup>14</sup> trigrams, and 3 &times; 10<sup>23</sup> 5-grams. No corpus covers a meaningful fraction of them.</p>"
   "<p>So most n-grams have a count of zero, and a zero count means a probability of zero &mdash; the model declares a perfectly ordinary sentence impossible because it happens not to have seen one four-word span before. Worse, one zero anywhere makes the probability of the whole sentence zero.</p>"
   "<p>The fixes are all forms of <strong>smoothing</strong>. Add-one (Laplace) smoothing adds a pseudocount to everything, which is simple and crude. <strong>Backoff</strong> falls back to a shorter n-gram when the longer one is unseen. <strong>Kneser-Ney</strong>, the best of the classical methods, discounts observed counts and redistributes the mass according to how many distinct contexts a word appears in &mdash; capturing that <em>Francisco</em> is common but only ever after <em>San</em>.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Start at n = 1.</strong> Set the n slider to 1 and read the output. With no context the model produces frequency-ordered nonsense.</li>"
   "<li><strong>Step up to 2 and 3.</strong> Raise n and watch local fluency appear. Pairs and triples look like real language, even though the sentence as a whole still drifts.</li>"
   "<li><strong>Push to 6.</strong> Set n to 6. Now most contexts have been seen once or not at all, so the model either repeats the training text verbatim or has nothing to offer &mdash; overfitting and sparsity in the same picture.</li>"
   "<li><strong>Scroll through the corpus.</strong> Use the view slider and watch which sequences have high counts. Almost all the probability mass sits on a small number of common patterns; the tail is enormous and nearly empty.</li>"
   "</ol>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>No smoothing.</strong> Any unseen n-gram makes the whole sentence probability zero. Smoothing is not optional.</li>"
   "<li><strong>Multiplying raw probabilities.</strong> Multiplying hundreds of small numbers underflows to zero in floating point. Sum log-probabilities instead.</li>"
   "<li><strong>Raising n to fix quality.</strong> It usually makes things worse by increasing sparsity. Better smoothing beats a larger n.</li>"
   "<li><strong>Forgetting sentence boundaries.</strong> Without explicit start and end tokens the model cannot represent which words begin or end a sentence.</li>"
   "</ul>"),
  ("In one line",
   "<p>An n-gram model estimates the next word by counting how often each continuation followed the previous n&minus;1 words, which makes it fast, interpretable, and trainable in a single pass. It is defeated by sparsity: the number of possible n-grams grows exponentially with n, so most sequences are never observed and smoothing is mandatory. Neural language models replaced it precisely because embeddings let them generalise across similar contexts rather than requiring each one to have been seen.</p>"),
 ]},

# ---------------------------------------------------------------------------
"natural_language_processing/normalization_techniques_for_sequential_data.html": {
 "intro": "Batch normalisation works beautifully on images and badly on sequences. Layer normalisation is what replaced it, and the reason is entirely about which axis the statistics are computed over.",
 "sections": [
  ("Normalising over the wrong axis",
   "<p>Every normalisation layer does the same arithmetic &mdash; subtract a mean, divide by a standard deviation, then apply a learned scale and shift. What differs is <em>which</em> values are pooled to compute that mean and deviation.</p>"
   "<p><strong>Batch normalisation</strong> computes statistics per feature, across the batch: for feature 3, average over all samples in the batch. <strong>Layer normalisation</strong> computes statistics per sample, across the features: for sample 3, average over all of its features.</p>"
   "<p>On images batch norm is excellent. On sequences it breaks, for three separate reasons.</p>"),
  ("Why batch norm fails on sequences",
   "<p><strong>Variable length.</strong> Sequences in a batch have different lengths, so timestep 50 might have 32 real values in one batch and 3 in another, with the rest padding. Statistics computed over that are unstable, and computed over padding they are simply wrong.</p>"
   "<p><strong>Per-timestep statistics.</strong> A recurrent network applies the same cell at every step, but batch norm would need separate running statistics for each timestep &mdash; and at inference on a sequence longer than anything seen in training, there are no statistics for those positions at all.</p>"
   "<p><strong>Batch dependence.</strong> A sample’s normalised representation depends on the other samples it happens to be batched with. For generation, where inference often runs one sequence at a time, the batch statistics are meaningless.</p>"
   "<p>Layer norm sidesteps all three. It uses only the sample’s own features, so it is independent of batch size, identical at training and inference, and unaffected by how many other sequences are present or how long they are.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Look at the unnormalised distribution.</strong> With the outlier toggle off, note the spread of the raw values &mdash; features on different scales pull the layer’s activations around.</li>"
   "<li><strong>Introduce an outlier.</strong> Enable the outlier toggle. Watch how a single extreme value shifts the computed mean and inflates the standard deviation, dragging every other value with it.</li>"
   "<li><strong>Compare the axes.</strong> Note which values get pooled. Normalising across the batch means one sample’s statistics depend on its neighbours; normalising across features means each sample is self-contained.</li>"
   "<li><strong>Toggle back and forth.</strong> The sensitivity to a single outlier is the practical argument for robust preprocessing before the layer ever sees the data.</li>"
   "</ol>"),
  ("The variants worth knowing",
   "<ul>"
   "<li><strong>Batch norm</strong> &mdash; per feature, across the batch. Convolutional networks with reasonable batch sizes.</li>"
   "<li><strong>Layer norm</strong> &mdash; per sample, across features. Transformers and recurrent networks, essentially universally.</li>"
   "<li><strong>Group norm</strong> &mdash; per sample, across groups of channels. Vision with small batches, where batch norm’s estimates go noisy.</li>"
   "<li><strong>RMSNorm</strong> &mdash; layer norm without the mean subtraction, dividing by the root mean square only. Slightly cheaper, works as well, and is what most recent large language models use.</li>"
   "</ul>"
   "<p>The placement matters too. Original transformers put layer norm after the residual addition (post-norm); modern ones put it before the sublayer (pre-norm), which makes deep stacks far easier to train and often removes the need for a learning-rate warmup.</p>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Batch norm with a batch size of 1 or 2.</strong> The variance estimate is meaningless. Use layer or group norm.</li>"
   "<li><strong>Forgetting eval mode.</strong> Batch norm uses batch statistics in training and running averages at inference. Leaving the model in training mode makes predictions depend on whatever else is in the batch.</li>"
   "<li><strong>Normalising over padded positions.</strong> Pollutes the statistics with zeros that carry no information.</li>"
   "<li><strong>Adding a bias before a normalisation layer.</strong> The mean subtraction cancels it exactly, so those parameters do nothing. Disable the bias on a layer feeding into a norm.</li>"
   "</ul>"),
  ("The short version",
   "<p>All normalisation layers subtract a mean and divide by a deviation; they differ only in which values are pooled. Batch norm pools across the batch, which makes it unusable for sequences of varying length and inference on single examples. Layer norm pools across each sample’s own features, so it is independent of batch size and identical at training and inference &mdash; which is why every transformer uses it.</p>"),
 ]},

# ---------------------------------------------------------------------------
"natural_language_processing/word_cloud.html": {
 "intro": "A word cloud sizes each word by how often it appears. It is genuinely useful for a first look at a corpus, and it is a frequency chart with the axes removed - which is worth knowing before drawing conclusions from one.",
 "sections": [
  ("What the picture encodes",
   "<p>Font size maps to frequency: the most common word is largest, and everything else is scaled relative to it. Position, colour and rotation almost always carry <em>no</em> information &mdash; they are chosen by a layout algorithm packing shapes into a space without overlap.</p>"
   "<p>That is the first thing to know about reading one. Two words next to each other are not related; they simply fitted. Any interpretation based on adjacency or colour is reading structure that was never encoded.</p>"),
  ("Why stopwords have to go",
   "<p>Run a word cloud on raw English text and you get <em>the</em>, <em>of</em>, <em>and</em>, <em>to</em>, <em>a</em> in enormous type. These are the most frequent words in almost any corpus and they tell you nothing about the subject.</p>"
   "<p>Removing them is what makes the visualisation informative, and it is a genuine editorial choice rather than a technical detail. Standard stopword lists are a reasonable default; domain-specific ones usually matter more. In a corpus of medical papers, <em>patient</em> and <em>study</em> may be so ubiquitous that they crowd out everything that distinguishes one paper from another.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Turn the filter off.</strong> Disable <strong>Stopwords Filter</strong> and press <strong>Generate</strong>. The cloud fills with function words and says nothing about the content &mdash; raw frequency is dominated by grammar, not meaning.</li>"
   "<li><strong>Turn it back on.</strong> Enable the filter and regenerate. Content words emerge, and the picture becomes about the subject matter.</li>"
   "<li><strong>Restrict the vocabulary.</strong> Set <strong>Max Words</strong> to 10 and generate. Only the strongest signals survive. Now raise it to 100 &mdash; the long tail of near-equal words adds visual noise without adding information.</li>"
   "<li><strong>Regenerate without changing anything.</strong> Press <strong>Generate</strong> twice at the same settings. The layout shifts while the sizes stay the same, which shows directly that position carries no meaning.</li>"
   "</ol>"),
  ("Where raw frequency misleads, and what to use instead",
   "<p>Frequency alone conflates “important in this document” with “common in general”. The standard correction is <strong>TF-IDF</strong>, which weights a word by how often it appears in this document and divides by how many documents contain it at all:</p>"
   "<p class=\"mono-font\">tf-idf = tf(word, doc) &times; log(N / df(word))</p>"
   "<p>A word appearing in every document gets an IDF near zero and drops out; a word frequent here and rare elsewhere scores highly. That is much closer to what people actually want a word cloud to show &mdash; what is <em>distinctive</em> about this text, not merely what is in it.</p>"
   "<p>The other limitation is that area is a poor visual encoding. People judge length far more accurately than area, so a bar chart conveys the same data more precisely. The word cloud’s advantage is that it is quick to scan and shows many terms at once &mdash; useful for exploration, weak for comparison.</p>"),
  ("What usually goes wrong",
   "<ul>"
   "<li><strong>Skipping normalisation.</strong> Without lowercasing and lemmatising, <em>Run</em>, <em>run</em>, <em>running</em> and <em>ran</em> are four separate entries splitting one word’s weight.</li>"
   "<li><strong>Comparing two clouds.</strong> Each is scaled to its own maximum, so a word the same size in two clouds may have very different counts. Comparison needs a shared scale, which means a chart.</li>"
   "<li><strong>Reading meaning into layout.</strong> Position and colour are decoration. Adjacency implies nothing.</li>"
   "<li><strong>Using raw counts on documents of different lengths.</strong> A longer document has larger counts throughout; normalise by length or use TF-IDF.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>A word cloud encodes frequency as font size and nothing else &mdash; position, colour and rotation are layout, not data. It needs stopword removal to say anything at all, and TF-IDF rather than raw frequency to show what is distinctive rather than merely common. Treat it as a fast exploratory glance at a corpus, and reach for a bar chart whenever the question is how much bigger one term is than another.</p>"),
 ]},

}
