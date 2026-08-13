# -*- coding: utf-8 -*-
"""Extra prose for the track landing pages.

Each /<track>/ page was a heading, two paragraphs and a grid of links - between
70 and 112 words of prose. That is the shape of a navigation page, and a
reviewer landing on one has nothing to read.

lib_pages.TOPICS keeps the lead and the "About this track" paragraphs. This
file adds the three sections underneath: what the track lets you do, how it is
ordered and what it assumes, and where it leads afterwards.

Keyed by the same topic key as TOPICS. Rendered by tools/build_topics.py.
"""

# Each entry: extra "About this track" paragraph, then the three sections.
TOPIC_SECTIONS = {

"maths": {
 "more": "The order matters more here than anywhere else on the site. Each page is "
         "built only from ideas introduced before it, so the track can be read straight "
         "through without ever hitting a symbol that has not been explained.",
 "learn": [
  "Read a vector as both a list of numbers and a direction, and say what a dot product measures.",
  "Multiply matrices by hand, and explain why the inner dimensions have to agree.",
  "Interpret a derivative as a slope and a gradient as the direction of steepest increase.",
  "Tell a probability distribution from a likelihood, and read what a standard deviation claims.",
  "Recognise these objects when they appear unannounced in a machine learning paper.",
 ],
 "order": "Start at the equation of a line, because every later idea is a generalisation of it: "
          "a slope becomes a gradient, a line becomes a plane, and a coefficient becomes a weight. "
          "From there the track splits into three strands that meet at the end - linear algebra "
          "(vectors, dot products, matrices as transformations), calculus (derivatives, partial "
          "derivatives, the chain rule), and probability (distributions, expectation, Bayes). "
          "Nothing assumes a maths degree. If you can rearrange an equation and read a graph, "
          "you have the prerequisites.",
 "next": "Once the gradient and the dot product are familiar, the machine learning and deep "
         "learning tracks stop being notation and start being mechanisms. Gradient descent is "
         "a derivative followed downhill; a neuron is a dot product with a bias. Most people "
         "find those tracks considerably easier after this one, which is why it is first on "
         "the learning path.",
},

"ml": {
 "more": "Nothing here requires a library. Each model is implemented in the page itself and "
         "run in front of you, so the numbers in the readout are computed by the same code "
         "that draws the picture rather than quoted from somewhere else.",
 "learn": [
  "Choose between regression, classification and clustering for a given problem.",
  "Explain what a decision boundary is and why some models can only draw a straight one.",
  "Read a confusion matrix and pick the metric that matches what the errors actually cost.",
  "Recognise overfitting from a train/validation gap rather than from a single score.",
  "Split data so that the number you report survives contact with new data.",
 ],
 "order": "The track opens with the two things that come before any model: how to split data, "
          "and how to tell whether a result means anything. Then it works through the classical "
          "algorithms roughly in order of how much machinery they need - linear and logistic "
          "regression, KNN, naive Bayes, decision trees, random forests, SVM - and finishes on "
          "unsupervised methods and the evaluation metrics that apply across all of them. "
          "It assumes you are comfortable with a graph and an equation; the maths track covers "
          "anything heavier.",
 "next": "Logistic regression is a single neuron, so the deep learning track continues directly "
         "from here. If the modelling is clear but the data handling is not, the databases track "
         "covers where the data comes from, and the algorithms track covers the complexity "
         "arguments that decide whether a method scales.",
},

"dl": {
 "more": "Because every page animates one step rather than a whole system, you can watch a "
         "single quantity move - a learning rate stretching a descent path, a validation curve "
         "turning upward, a gradient thinning out as it travels back through the layers.",
 "learn": [
  "Trace a forward pass by hand: weighted sum, bias, activation, output.",
  "Say what backpropagation actually computes, and why the chain rule makes depth expensive.",
  "Diagnose a training run from its curves - underfitting, overfitting, or a broken learning rate.",
  "Choose an activation, an initialisation and an optimiser, and justify each choice.",
  "Recognise vanishing and exploding gradients, and name the fixes that address each.",
 ],
 "order": "The track builds strictly upward. One perceptron first - a weighted sum, a bias, an "
          "activation - because everything afterwards is that repeated. Then loss functions, then "
          "gradient descent, then backpropagation, which is where the earlier pieces combine. "
          "After that come the practical concerns that make deep networks trainable at all: "
          "initialisation, normalisation, dropout, regularisation, optimisers and learning-rate "
          "schedules. A working knowledge of derivatives helps from the backpropagation module "
          "onward; the maths track covers what is needed.",
 "next": "The convolutional and sequence architectures are specialisations of what is here, so "
         "computer vision and natural language processing both follow naturally. The generative "
         "AI track then picks up where sequence modelling ends, with the training objectives and "
         "serving techniques behind current large models.",
},

"dsa": {
 "more": "Every page reports the operation count as it runs, so the complexity written at the "
         "top is something you can check rather than something you have to take on trust - and "
         "the difference between O(n) and O(log n) becomes a number you watched accumulate.",
 "learn": [
  "Derive a complexity rather than memorise it, by counting the work each step does.",
  "Choose a sorting algorithm from the constraints - stability, memory, and how sorted the input already is.",
  "Explain why binary search needs sorted data, and what breaks silently when it is not.",
  "Pick between breadth-first and depth-first search from what the problem is asking.",
  "Recognise when a hash table turns an accidental O(n squared) loop into a linear one.",
 ],
 "order": "Big-O comes first, because every page afterwards refers back to it. Then the linear "
          "structures - arrays, linked lists, stacks and queues - followed by searching and "
          "sorting, which is where complexity differences first become dramatic. Trees, heaps "
          "and hash tables come next, then graphs and their traversals, and finally the "
          "strategies that cut across all of them: recursion, divide and conquer, greedy "
          "methods, dynamic programming and backtracking. No prior computer science is assumed, "
          "though the Python pages in this track help if you want to run the code yourself.",
 "next": "These are the foundations interviews test and the reason some machine learning methods "
         "scale and others do not. The databases track applies the same thinking to indexes and "
         "query plans, where a B-tree and a query execution order are exactly the ideas from "
         "this track under different names.",
},

"nlp": {
 "more": "The track follows one piece of text the whole way down, so each stage is visibly the "
         "input to the next: characters become tokens, tokens become ids, ids become vectors, "
         "and vectors become the thing a model can actually compute with.",
 "learn": [
  "Explain why a model never sees words, and what a tokenizer does about it.",
  "Say what an embedding encodes, and why one-hot vectors cannot encode it.",
  "Trace a recurrent cell across timesteps and explain what its hidden state holds.",
  "Describe why long sequences are hard, and how gating in an LSTM addresses it.",
  "Read self-attention as a weighted lookup rather than as a formula to memorise.",
 ],
 "order": "Text first: how it is normalised, split and counted, including the n-gram models that "
          "preceded neural approaches and still explain why sparsity is the central problem. "
          "Then representation - what embeddings are and how they are trained. Then the recurrent "
          "family in full, from a bare cell through backpropagation through time to LSTM and "
          "bidirectional layers. Attention and positional encoding come last, because they are "
          "best understood as answers to the specific limitations the recurrent pages establish. "
          "The deep learning track is the useful prerequisite.",
 "next": "Attention is the bridge to the generative AI track, which covers what transformers are "
         "trained to do and how they are made small and fast enough to serve. The computer vision "
         "track is the parallel specialisation, applying the same base ideas to images instead of "
         "sequences.",
},

"computer-vision": {
 "more": "The stack is taken apart rather than drawn as coloured boxes: what a filter contains, "
         "what a feature map records, what pooling discards, and how many parameters each of "
         "those choices actually costs.",
 "learn": [
  "Explain what a convolutional filter is and why it spans every input channel.",
  "Compute a layer's output size from the input, kernel, padding and stride.",
  "Count a convolutional layer's parameters, and say why the image size never appears.",
  "Describe what pooling buys and what it destroys.",
  "Say why weight sharing gives both a parameter saving and translation equivariance.",
 ],
 "order": "It starts below the network, with how an image is stored at all - grayscale "
          "intensities, then RGB channels - because a filter's depth only makes sense once "
          "channels do. Then the convolution itself: edge detection by hand, feature maps, "
          "padding, stride, pooling and parameter counting. After that the components that make "
          "a real network work, including ReLU, dense layers and residual connections, and "
          "finally the applied layer: augmentation, data loaders, transfer learning, object "
          "detection and segmentation. The deep learning track is assumed.",
 "next": "Transfer learning is where most practical vision work actually starts, and the "
         "generative AI track covers the modern architectures that now compete with "
         "convolutional networks on the same tasks.",
},

"db": {
 "more": "SQL is declarative, which is exactly what makes it hard to learn: you write what you "
         "want and the engine decides how. These pages show the how - which rows survive each "
         "clause, in the order the database actually applies them.",
 "learn": [
  "Write queries with confidence about which clause runs when, and why that decides where an alias is legal.",
  "Choose the right join, and predict how many rows come back before running it.",
  "Tell WHERE from HAVING by what each one filters, and pick the faster of the two.",
  "Explain what an index costs on write and what it saves on read.",
  "Say what a transaction guarantees, and what normalisation is trading away.",
 ],
 "order": "The relational model comes first, along with its non-relational alternative, so the "
          "later clauses have something to act on. Then SQL itself, worked through in the order "
          "a query is actually evaluated - FROM and JOIN, WHERE, GROUP BY, HAVING, SELECT, "
          "ORDER BY - which is deliberately not the order it is written in, and explains most of "
          "the errors beginners hit. Subqueries, CTEs and window functions follow, and the track "
          "ends on the engine's own concerns: indexes, transactions and normalisation. No prior "
          "database experience is needed.",
 "next": "Indexes are B-trees, and query execution order is a plan over set operations, so the "
         "algorithms track explains the machinery underneath. If you are heading toward machine "
         "learning, this is where the training data comes from and where most feature engineering "
         "actually happens.",
},

"gen-ai": {
 "more": "A large language model predicts one token at a time, and everything around it exists "
         "to make that prediction useful: the tokenizer in front, the training objective behind, "
         "the retrieval that grounds it, and the quantisation that makes it servable.",
 "learn": [
  "Explain how text is split into tokens and why byte-pair encoding handles unseen words.",
  "Distinguish causal from masked language modelling, and say which models each produced.",
  "Describe what a context window costs and what a KV cache is caching.",
  "Build a retrieval pipeline and evaluate it with the metric that matches the task.",
  "Say what LoRA, quantisation and distillation each trade away in exchange for what.",
 ],
 "order": "Tokenization first, because it determines what the model can represent. Then the two "
          "training objectives - causal and masked - that account for most current models, "
          "followed by the mechanics of generation: next-token prediction, context windows and "
          "KV caching. Retrieval comes next and takes up much of the track, from embeddings and "
          "vector search through chunking, hybrid retrieval, reranking and the retriever variants, "
          "ending on how to evaluate any of it. Adaptation and efficiency - fine-tuning, RLHF, "
          "LoRA, quantisation, distillation - close the track. The NLP track is the prerequisite.",
 "next": "Retrieval quality is mostly an embeddings-and-evaluation problem, so the NLP and "
         "machine learning tracks both feed back into it. If you are building rather than "
         "studying, the retrieval modules are the ones that change day-to-day results the most.",
},

"python": {
 "more": "Every page runs real Python in the browser, with no installation and no setup. The "
         "code on screen is the code that executes, so an error you cause is a real traceback "
         "rather than a description of one.",
 "learn": [
  "Write and run a program that takes input, decides something, and prints a result.",
  "Choose between a list, a dictionary and a string for a given job.",
  "Use loops and conditionals without guessing at indentation or off-by-one bounds.",
  "Write functions that return values, and explain why a missing return gives you None.",
  "Read a traceback and find the line that actually caused it.",
 ],
 "order": "The track starts at your first print statement and adds one idea at a time: variables "
          "and types, numbers and operators, strings and slicing, lists and indexing, booleans "
          "and comparisons, conditionals, loops, dictionaries, and functions. It ends on reading "
          "errors, which is the skill that makes everything else self-teachable. Nothing is "
          "assumed - not a prior language, not an installed interpreter, not a terminal.",
 "next": "Every other track on this site writes Python in its examples and assumes you can read "
         "it. Once functions and dictionaries are comfortable, the algorithms track is the "
         "natural next step, since its data structure pages are the same objects examined more "
         "carefully.",
},

}

TOPIC_SECTIONS["interview"] = {
 "more": "Every other track is organised around ideas. This one is organised around "
         "questions, because that is the shape the pressure arrives in: someone asks "
         "why your loop is quadratic, and you have thirty seconds. Each page is one "
         "question, answered in full and then demonstrated by code you can run.",
 "learn": [
  "Answer the immutability, hashability and complexity questions without hedging.",
  "Reach for the right technique on sight - two pointers, sliding window, prefix sums, a counter.",
  "State the time and space cost of your own solution before being asked for it.",
  "Recognise the traps: `in` on a list, `+=` on a string, `pop(0)` as a queue.",
  "Show your working - the pages measure their claims, and so can you.",
 ],
 "order": "The track runs strings, then lists and arrays, then dictionaries, hashing and "
          "the crossover problems, finishing on the complexity traps. Within each group "
          "the conceptual questions come before the coding problems that lean on them, "
          "because \"why is `in` slow on a list?\" is the answer to half the coding "
          "questions that follow it. Nothing here assumes you have read the rest of the "
          "site, though the algorithms track covers the same techniques at more length.",
 "next": "The Algorithms and Data Structures track is the long-form version of this one: "
         "same techniques, one page per algorithm rather than one page per question, with "
         "the visualisation carrying more of the explanation. If a question here lands on "
         "something unfamiliar - binary search bounds, hash collisions, dynamic programming "
         "- that track has the full treatment.",
}
