# -*- coding: utf-8 -*-
"""Written explanations for the deep-learning modules that were still thin.

A first pass (in articles.py) replaced the generic skeleton on fourteen pages.
Measured afterwards, a further twenty pages were still under 400 words of
prose - enough to look like an article and not enough to be one. The entries
here cover those, and supersede the short versions in articles.py for the
eight pages that appear in both.

Rendered by tools/build_articles.py. Edit here, then `npm run build`.
"""

ARTICLES_DL = {

# ---------------------------------------------------------------------------
"deep_learning/gradient_descent_training.html": {
 "intro": "Follow the slope downhill, one step at a time. Every parameter in every neural network is found this way, and the step size decides whether it works at all.",
 "sections": [
  ("The one rule the whole algorithm follows",
   "<p>You have a loss function that says how wrong the model currently is, and parameters you can change. Gradient descent computes the derivative of the loss with respect to each parameter &mdash; the direction in which loss increases fastest &mdash; and then moves the opposite way:</p>"
   "<p class=\"mono-font\">w &larr; w &minus; &eta; &middot; &part;L/&part;w</p>"
   "<p>&eta; is the learning rate: how far to step. The gradient supplies the direction; the learning rate supplies the distance. That is the entire algorithm, repeated until the loss stops falling.</p>"
   "<p>The reason it works at all is that the gradient is a <em>local</em> answer &mdash; it needs no knowledge of the loss surface beyond the current point. That is what makes it usable on a function with a hundred million parameters that nobody can visualise.</p>"),
  ("Work one step through by hand",
   "<p>Fit <span class=\"mono-font\">y = wx</span> to the single point <span class=\"mono-font\">(2, 6)</span>, starting at <span class=\"mono-font\">w = 1</span>, with squared error loss:</p>"
   "<p class=\"mono-font\">prediction = 1 &times; 2 = 2, target = 6, error = &minus;4</p>"
   "<p class=\"mono-font\">L = (wx &minus; y)&sup2; &nbsp;&rarr;&nbsp; &part;L/&part;w = 2x(wx &minus; y) = 2(2)(&minus;4) = &minus;16</p>"
   "<p>With <span class=\"mono-font\">&eta; = 0.1</span>:</p>"
   "<p class=\"mono-font\">w &larr; 1 &minus; 0.1(&minus;16) = 2.6</p>"
   "<p>The new prediction is 5.2, much closer to 6. Note the gradient was <em>negative</em>, so subtracting it increased w &mdash; the minus sign in the update rule is what turns “direction of steepest increase” into “step downhill”.</p>"),
  ("Batch, stochastic, and mini-batch",
   "<p>The gradient is a sum over training examples, and how many you include before each update defines the three variants:</p>"
   "<ul>"
   "<li><strong>Batch</strong> &mdash; use every example. The gradient is exact, so the path to the minimum is smooth, but one update requires a full pass over the data.</li>"
   "<li><strong>Stochastic (SGD)</strong> &mdash; use one example. Updates are extremely cheap and extremely noisy; the path jitters, which costs precision but can jolt the model out of poor regions.</li>"
   "<li><strong>Mini-batch</strong> &mdash; use 32 to 256 examples. Close to the exact gradient, cheap enough to update often, and the shape that matches how GPUs actually work. This is what essentially all real training uses.</li>"
   "</ul>"),
  ("Try it yourself",
   "<ol>"
   "<li><strong>Find the working range.</strong> Set <strong>Learning Rate</strong> to 0.01 and press <strong>Train</strong>. The line converges smoothly onto the data. This is what a healthy run looks like.</li>"
   "<li><strong>Make it too small.</strong> Set <strong>Learning Rate</strong> to 0.001 and press <strong>Reset</strong>, then <strong>Train</strong>. The line still moves in the right direction but crawls &mdash; correct, and far too slow to be useful.</li>"
   "<li><strong>Make it too large.</strong> Set <strong>Learning Rate</strong> to 0.1 and train again. The fit overshoots the minimum and the loss oscillates or diverges outright. Steps too big do not just slow convergence, they prevent it.</li>"
   "<li><strong>Compare the three methods.</strong> Press <strong>Run All 3</strong> and watch the paths together. Batch is smooth, stochastic is jagged, mini-batch sits between &mdash; and all three end up in roughly the same place.</li>"
   "<li><strong>Add noise.</strong> Raise <strong>Noise</strong> and press <strong>Data</strong>, then train. The loss no longer approaches zero; it flattens out above it. That floor is irreducible error, not a training failure.</li>"
   "</ol>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Learning rate too high.</strong> Loss goes to NaN or oscillates upward. This is the first thing to check when training diverges, and dividing it by 10 is the first thing to try.</li>"
   "<li><strong>Learning rate too low.</strong> Loss falls, painfully slowly, and can stall on a plateau long enough to look converged when it is not.</li>"
   "<li><strong>Unscaled features.</strong> A feature in the tens of thousands and one in decimals produce wildly different gradient magnitudes, so no single learning rate suits both. Scale inputs before training, not after diagnosing.</li>"
   "<li><strong>Reading one noisy step as a trend.</strong> With mini-batches the loss goes up on individual steps all the time. Judge the moving average, not the last value.</li>"
   "</ul>"),
  ("What to remember",
   "<p>Gradient descent repeatedly moves each parameter against its gradient, scaled by a learning rate, and that single rule trains every neural network in use. The gradient is reliable; the learning rate is the choice you have to get right, because too large diverges and too small never arrives. Mini-batches are the standard compromise between the exact-but-expensive batch gradient and the cheap-but-noisy stochastic one.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/hyper-paramter_tuning.html": {
 "intro": "Parameters are learned from data; hyperparameters are chosen before training starts. Searching that second set well is often worth more than any change to the model itself.",
 "sections": [
  ("Two kinds of number",
   "<p>A <strong>parameter</strong> is learned: weights and biases move during training because gradient descent moves them. A <strong>hyperparameter</strong> is fixed before training and never updated by the optimiser &mdash; learning rate, number of layers, neurons per layer, batch size, dropout rate, regularisation strength.</p>"
   "<p>The distinction matters because you cannot use gradient descent to find hyperparameters. There is no derivative of validation accuracy with respect to “number of layers”. The only way to evaluate a hyperparameter setting is to train a model with it and see what happens, which is why tuning is expensive.</p>"),
  ("Grid search, random search, and why random usually wins",
   "<p><strong>Grid search</strong> tries every combination on a predefined grid. With 5 learning rates and 5 layer widths that is 25 runs, and adding a third hyperparameter with 5 values makes it 125. The cost is exponential in the number of hyperparameters.</p>"
   "<p><strong>Random search</strong> samples combinations at random from ranges you specify. Counterintuitively it usually finds better settings for the same budget, and the reason is sharp: not all hyperparameters matter equally. If learning rate dominates and layer width barely matters, a 5&times;5 grid tests only <strong>5 distinct learning rates</strong> across 25 runs. Random search with 25 samples tests <strong>25 distinct learning rates</strong>. You get five times the resolution on the axis that counts, at no extra cost.</p>"
   "<p><strong>Bayesian optimisation</strong> goes further, building a model of which regions look promising and sampling there. It is more efficient per trial and worth the complexity when each run takes hours.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>Run a small search.</strong> Set <strong>N Trials</strong> to 5 and press <strong>Run Trial</strong> repeatedly. Results scatter widely &mdash; five samples is not enough to distinguish a good region from luck.</li>"
   "<li><strong>Give it a real budget.</strong> Press <strong>Reset Search</strong>, set <strong>N Trials</strong> to 20, and run again. A pattern emerges: certain learning-rate bands consistently do better regardless of the other settings.</li>"
   "<li><strong>Compare the strategies.</strong> Switch <strong>Search Strategy</strong> between grid and random at the same <strong>N Trials</strong>. Random covers the learning-rate axis far more finely, because grid keeps re-testing the same few values.</li>"
   "<li><strong>Test which knob matters.</strong> Hold <strong>Learning Rate</strong> fixed and vary <strong>Neurons/Layer</strong> across its range, then do the reverse. The learning rate changes the outcome far more &mdash; that asymmetry is the whole argument for random search.</li>"
   "</ol>"),
  ("Search on a log scale",
   "<p>Learning rate should be sampled logarithmically, not uniformly. Sampling uniformly from 0.0001 to 0.1 puts 90% of the samples above 0.01, leaving the small-rate region &mdash; where the answer usually is &mdash; almost untested.</p>"
   "<p>Sample the exponent instead: draw uniformly from &minus;4 to &minus;1 and use <span class=\"mono-font\">10<sup>x</sup></span>. That gives equal attention to 0.0001&ndash;0.001, 0.001&ndash;0.01, and 0.01&ndash;0.1. The same applies to regularisation strength and any other quantity that spans orders of magnitude.</p>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Tuning on the test set.</strong> The single most damaging mistake. Selecting hyperparameters by test performance leaks the test set into the model and the reported score becomes optimistic. Tune on a validation split and touch test once, at the end.</li>"
   "<li><strong>Sampling learning rate uniformly.</strong> Wastes most of the budget in a range that is almost always too large.</li>"
   "<li><strong>Tuning everything at once with no budget.</strong> Start with learning rate, which usually dominates, then batch size and architecture. Regularisation is worth tuning only once the model can overfit.</li>"
   "<li><strong>Ignoring seed variance.</strong> If two settings differ by less than the run-to-run variation from random initialisation, you have not measured a difference. Repeat the promising ones.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Hyperparameters sit outside gradient descent, so the only way to evaluate them is to train and measure &mdash; which makes the search strategy itself worth thinking about. Random search beats grid search at equal budget because it spends its samples on more distinct values of whichever hyperparameter actually matters, and anything spanning orders of magnitude should be sampled on a log scale. Whatever the strategy, select on validation data and keep the test set untouched.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/reproducibility_of_model.html": {
 "intro": "Train the same model twice on the same data and you get two different results. Controlling the randomness is what turns a demo into an experiment you can trust.",
 "sections": [
  ("Where the randomness comes from",
   "<p>Neural network training is randomised in at least four independent places, and every one of them changes the final weights:</p>"
   "<ul>"
   "<li><strong>Weight initialisation.</strong> Every weight starts as a random draw. Different draws land the optimiser in different basins of the loss surface.</li>"
   "<li><strong>Data shuffling.</strong> Mini-batches are formed from a shuffled dataset, so a different order means different gradients at every step.</li>"
   "<li><strong>Dropout.</strong> Which units are zeroed is resampled on every forward pass during training.</li>"
   "<li><strong>Augmentation.</strong> Random crops, flips and noise mean the model literally never sees the same input twice.</li>"
   "</ul>"
   "<p>None of these is a defect &mdash; each is deliberately there to improve generalisation. But they mean “the model” is a sample from a distribution of models, not a fixed object.</p>"),
  ("Seeding, and what a seed actually fixes",
   "<p>These are all <em>pseudo</em>-random: a deterministic sequence generated from a starting value called the seed. Fix the seed and the sequence is identical every run.</p>"
   "<p class=\"mono-font\">random.seed(42)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Python&rsquo;s own generator<br>"
   "np.random.seed(42)&nbsp;&nbsp;&nbsp;&nbsp;# NumPy<br>"
   "torch.manual_seed(42)&nbsp;# PyTorch, CPU and GPU</p>"
   "<p>The catch is that these are separate generators. Seeding NumPy does nothing for PyTorch’s dropout, and seeding PyTorch does nothing for a shuffle done with Python’s <span class=\"mono-font\">random</span>. Every library that draws a random number needs its own seed, and missing one is the usual reason a “seeded” run is still not reproducible.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Fix the seed and repeat.</strong> Enter a seed value and press <strong>Apply Seed &amp; Init</strong>, note the initial weights, then press it again with the same seed. Identical values &mdash; the initialisation is fully determined by that number.</li>"
   "<li><strong>Change one digit.</strong> Change the seed and re-initialise. Every weight is different. The seed is not a setting with a meaningful scale; it just selects an arbitrary point in the sequence.</li>"
   "<li><strong>Watch the sequence advance.</strong> Press <strong>Next Sample</strong> several times. Each draw differs, but the whole run of draws replays identically after re-applying the same seed &mdash; that is what pseudo-random means.</li>"
   "<li><strong>Stream without reseeding.</strong> Press <strong>Auto Stream</strong> and let it run, then re-apply the seed. The stream restarts from the beginning of the same sequence, not from where it stopped.</li>"
   "</ol>"),
  ("Why the GPU can still be non-deterministic",
   "<p>Seeding every generator can still leave runs that differ, and the reason is floating-point arithmetic rather than randomness. GPU kernels parallelise reductions across thousands of threads, and the order in which partial sums combine varies between runs. Floating-point addition is not associative &mdash; <span class=\"mono-font\">(a + b) + c</span> can differ from <span class=\"mono-font\">a + (b + c)</span> in the last bits &mdash; so identical inputs can give slightly different outputs.</p>"
   "<p>Those differences are around 10<sup>&minus;7</sup>, but training amplifies them: a tiny gradient difference changes the next weights, which changes the next gradient, and after thousands of steps the runs have visibly diverged. Frameworks offer deterministic modes (<span class=\"mono-font\">torch.use_deterministic_algorithms(True)</span>) that force reproducible kernels, typically at a real cost in speed.</p>"),
  ("What usually goes wrong",
   "<ul>"
   "<li><strong>Seeding one library and assuming it covers the rest.</strong> Python, NumPy and the framework each need seeding, plus <span class=\"mono-font\">PYTHONHASHSEED</span> if set ordering matters.</li>"
   "<li><strong>Treating the seed as a hyperparameter.</strong> Searching for a good seed is fitting to noise. If results depend heavily on it, the finding is fragile, not tuned.</li>"
   "<li><strong>Reporting a single run.</strong> A one-run comparison between two methods is uninterpretable when seed variance alone can move accuracy a point or more. Report mean and spread over several seeds.</li>"
   "<li><strong>Expecting reproducibility across machines.</strong> A fixed seed reproduces a run on the same hardware, library versions and thread count. Change the GPU or the cuDNN version and results move again.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Training draws randomness from initialisation, shuffling, dropout and augmentation, each from its own generator, so reproducibility means seeding all of them rather than one. Even then GPU reductions are non-deterministic at the level of floating-point rounding, and training amplifies those differences over thousands of steps. Seed to make a run repeatable for debugging &mdash; and report results over several seeds, because a single run tells you as much about the seed as about the method.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/model_training_on_cpu_vs_gpu.html": {
 "intro": "A GPU is not a faster CPU. It is a wider one - thousands of slow cores instead of a few fast ones - and that shape decides which workloads it transforms and which it does not.",
 "sections": [
  ("Latency versus throughput",
   "<p>A CPU has a handful of cores optimised to finish <em>one</em> instruction stream as fast as possible: high clock speeds, deep pipelines, large caches, aggressive branch prediction. It is built for latency.</p>"
   "<p>A GPU has thousands of much simpler cores running in lockstep on different data. Any single core is slower than a CPU core, and there are so many that the aggregate arithmetic throughput is an order of magnitude higher. It is built for throughput.</p>"
   "<p>Neural network training is almost entirely matrix multiplication, which is the ideal case for that design: every output element is an independent dot product, so there is nothing to serialise and nothing to predict.</p>"),
  ("Why batch size is the variable that matters",
   "<p>Multiplying a 1&times;512 input by a 512&times;512 weight matrix uses a tiny fraction of a GPU’s cores; the rest sit idle. Multiply a 256&times;512 batch by the same weights and the work grows 256-fold while the time barely moves, because that work fills capacity that was already there and already paid for.</p>"
   "<p>This is why batch size dominates GPU utilisation. Below a threshold the GPU is latency-bound and a CPU can genuinely be competitive; above it, throughput takes over and the GPU wins by a wide margin. The same reasoning explains why wider layers use a GPU better than narrow ones.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Start where the CPU can win.</strong> Set <strong>Batch Size</strong> to 1 and press <strong>Start Race</strong>. With one sample the GPU’s parallelism is unused and the launch overhead dominates &mdash; the CPU is competitive or ahead.</li>"
   "<li><strong>Find the crossover.</strong> Raise <strong>Batch Size</strong> to 32 and race again, then 128. Somewhere in that range the GPU pulls decisively ahead; below it the two are close.</li>"
   "<li><strong>Push it wide.</strong> Set <strong>Batch Size</strong> to 512. GPU time barely increases while CPU time scales roughly linearly &mdash; that flatness is unused capacity being filled rather than extra speed appearing.</li>"
   "<li><strong>Widen the layer instead.</strong> Raise <strong>Hidden</strong> to 32 and keep the batch small. More arithmetic per sample helps the GPU too, for the same reason: the bottleneck is occupancy, not the amount of work.</li>"
   "</ol>"),
  ("The transfer cost nobody budgets for",
   "<p>CPU and GPU have separate memory. Every tensor must cross the PCIe bus, and that bus is slow relative to on-device bandwidth &mdash; roughly 16&ndash;32 GB/s against 900+ GB/s of GPU memory bandwidth.</p>"
   "<p>So a computation is only worth moving to the GPU if the arithmetic saved exceeds the transfer cost. Copying a batch across to run one cheap elementwise operation is slower than doing it on the CPU. This is why the standard advice is to move the model and the batch to the device once and keep <em>everything</em> there for the whole step, rather than moving tensors back and forth &mdash; and why an innocuous <span class=\"mono-font\">.cpu()</span> or <span class=\"mono-font\">.item()</span> inside a training loop can dominate the profile, since it also forces a synchronisation that stalls the pipeline.</p>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Batch too small to occupy the device.</strong> The most common reason a GPU shows 15% utilisation. If memory allows, increase the batch before blaming the hardware.</li>"
   "<li><strong>A data loader that cannot keep up.</strong> If preprocessing happens on one CPU thread, the GPU waits. Use multiple worker processes and pinned memory.</li>"
   "<li><strong>Synchronising inside the loop.</strong> Calling <span class=\"mono-font\">.item()</span> on the loss every step forces the CPU to wait for the GPU. Accumulate on device and read occasionally.</li>"
   "<li><strong>Expecting a speedup on small models.</strong> For a small network on tabular data the CPU is often faster outright &mdash; there is not enough parallel work to amortise the launch and transfer overhead.</li>"
   "</ul>"),
  ("In one line",
   "<p>A GPU trades per-core speed for thousands of cores, which suits neural networks because matrix multiplication is embarrassingly parallel. The speedup is real only when there is enough work in flight to occupy the device, so batch size and layer width matter more than anything else, and the separate memory space means transfers and synchronisations can quietly become the bottleneck. Small model, small batch: the CPU may well win.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/dropout_in_neural_networks.html": {
 "intro": "Randomly switch off a fraction of neurons on every training step. It sounds destructive and it is one of the most effective regularisers ever found, because it stops neurons relying on each other.",
 "sections": [
  ("What dropout does",
   "<p>On each training forward pass, each neuron in a dropout layer is independently set to zero with probability p. A different random subset is dropped every step, so the network never trains the same architecture twice.</p>"
   "<p>At <strong>inference</strong> time dropout is switched off entirely and all neurons are used. That asymmetry is the point &mdash; and the source of the most common bug, since a model left in training mode gives different predictions every time it is called.</p>"),
  ("Why removing capacity improves generalisation",
   "<p>The mechanism is the prevention of <strong>co-adaptation</strong>. Without dropout, neurons specialise in tandem: neuron A learns to correct neuron B’s systematic error, which only works while B behaves exactly as it did in training. That partnership is a form of memorisation and it does not survive new data.</p>"
   "<p>With dropout, B may be absent on any given step, so A cannot depend on it. Every neuron is forced to learn a feature that is useful on its own, against a randomly varying set of colleagues. The result is redundant, robust representations rather than brittle chains.</p>"
   "<p>The second reading is that dropout approximates an <strong>ensemble</strong>. A layer of n units has 2<sup>n</sup> possible dropout masks, so training samples from an exponential family of thinned networks sharing one set of weights; using all units at inference approximates averaging their predictions. Ensembles generalise better than single models, and this is an ensemble that costs nothing extra to train.</p>"),
  ("The scaling detail",
   "<p>Dropping units changes the expected magnitude of a layer’s output. If half the inputs are zeroed, the sum arriving at the next layer is about half its usual size &mdash; so a network trained with dropout would see inputs twice as large at inference, when nothing is dropped.</p>"
   "<p>Frameworks fix this with <strong>inverted dropout</strong>: during training, surviving activations are divided by <span class=\"mono-font\">(1 &minus; p)</span>. With p = 0.5 the survivors are doubled, restoring the expected sum, and inference needs no adjustment at all. This is automatic in PyTorch and TensorFlow, and worth knowing about because it explains why a hand-rolled dropout implementation often makes a model worse.</p>"),
  ("Experiments to try",
   "<ol>"
   "<li><strong>Turn it off.</strong> Set <strong>Dropout</strong> to 0 and press <strong>Simulate Flow</strong>. Every neuron participates and signal reaches the output along every path.</li>"
   "<li><strong>Use the standard setting.</strong> Set <strong>Dropout</strong> to 50 and simulate repeatedly. A different half is silenced each time &mdash; the network is a different shape on every pass, which is exactly what breaks co-adaptation.</li>"
   "<li><strong>Push it too far.</strong> Set <strong>Dropout</strong> to 90. So little signal survives that some paths carry nothing at all. Too much dropout does not regularise, it starves the network &mdash; visible here as an underfitting failure.</li>"
   "<li><strong>Change the width.</strong> Raise <strong>Input</strong> and simulate at 50% again. A wider layer keeps more absolute signal at the same rate, which is why large layers tolerate higher dropout than small ones.</li>"
   "</ol>"),
  ("Common mistakes",
   "<ul>"
   "<li><strong>Leaving the model in training mode at inference.</strong> Forgetting <span class=\"mono-font\">model.eval()</span> in PyTorch means dropout stays active and predictions become random. This is the single most common dropout bug, and it also silently affects batch normalisation.</li>"
   "<li><strong>Applying it to a model that is underfitting.</strong> Dropout costs capacity. If training loss is already high, dropout makes both training and validation worse.</li>"
   "<li><strong>Using p = 0.5 everywhere.</strong> That figure comes from large fully connected layers. Convolutional layers usually want 0.1&ndash;0.2, since their weight sharing is already a strong regulariser, and input layers want very little.</li>"
   "<li><strong>Combining it carelessly with batch normalisation.</strong> The two interact badly &mdash; dropout changes the variance batch norm estimated. Common practice is batch norm instead of dropout in convolutional nets, or dropout only after the normalisation layer.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Dropout zeroes a random fraction of units on every training pass and disables itself at inference, which forces each neuron to be independently useful rather than co-adapted to specific partners. Read as an ensemble, it trains exponentially many thinned networks that share weights and averages them for free. It regularises a model that is overfitting and harms one that is not, and the scaling that makes it work is handled by the framework &mdash; provided you remember to switch the model into evaluation mode.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/vanishing_vs_exploding_gradient.html": {
 "intro": "Backpropagation multiplies gradients layer by layer. Multiply enough numbers below one and the signal disappears; enough above one and it blows up. Both failures come from the same chain rule.",
 "sections": [
  ("Where both problems come from",
   "<p>Backpropagation computes the gradient at an early layer by multiplying together the local derivatives of every layer above it. For a network of depth L that is a product of L terms.</p>"
   "<p>Products of many numbers behave exponentially. If each term averages 0.5, then after 10 layers the gradient is scaled by 0.5<sup>10</sup> &asymp; 0.001, and after 30 layers by 10<sup>&minus;9</sup> &mdash; effectively zero. If each term averages 1.5, after 30 layers the factor is around 191,000, and weights update so violently the loss becomes NaN.</p>"
   "<p>So <strong>vanishing</strong> and <strong>exploding</strong> gradients are not two problems. They are one problem &mdash; repeated multiplication &mdash; falling either side of a knife edge at 1.</p>"),
  ("Why sigmoid made it worse",
   "<p>The derivative of the sigmoid is <span class=\"mono-font\">&sigma;(x)(1 &minus; &sigma;(x))</span>, which peaks at <strong>0.25</strong> when x = 0 and falls toward zero for inputs of large magnitude.</p>"
   "<p>Its <em>maximum</em> is 0.25, so every sigmoid layer multiplies the gradient by at most a quarter. Ten layers means a factor of 0.25<sup>10</sup> &asymp; 10<sup>&minus;6</sup> in the best case, and far worse once units saturate. This is the concrete reason deep networks were considered untrainable before roughly 2010: the early layers received no usable learning signal at all.</p>"
   "<p><strong>ReLU</strong> changed that. Its derivative is exactly 1 for positive inputs, so the gradient passes through unattenuated however many layers it crosses. That single property, more than any other, is what made depth practical.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Train without help.</strong> Leave the normalisation and ReLU toggles off and press <strong>Train Network</strong>. Watch the gradient magnitudes at the early layers &mdash; they are orders of magnitude smaller than at the output, so the first layers barely move.</li>"
   "<li><strong>Switch the activation.</strong> Enable the ReLU toggle, press <strong>Reset</strong>, and train again. Gradients now reach the early layers at a usable size, because each layer multiplies by 1 rather than by at most 0.25.</li>"
   "<li><strong>Create a scale mismatch.</strong> Set <strong>Salary</strong> near 200000 while <strong>Age</strong> stays around 30, with normalisation off. One input is thousands of times larger, so its gradients dominate and destabilise training.</li>"
   "<li><strong>Normalise and repeat.</strong> Enable <strong>Normalize Data</strong> and train again with the same inputs. Both features now contribute comparable gradients, and the run is stable &mdash; feature scaling is a gradient problem, not a cosmetic one.</li>"
   "</ol>"),
  ("The fixes that are actually used",
   "<ul>"
   "<li><strong>ReLU and its variants.</strong> A derivative of 1 in the positive region removes the systematic shrinkage. Leaky ReLU and GELU additionally avoid the dead-unit problem of a hard zero.</li>"
   "<li><strong>Careful initialisation.</strong> He initialisation for ReLU and Xavier for tanh set the initial weight variance so that activations and gradients keep roughly constant scale across layers &mdash; deliberately placing the product near 1.</li>"
   "<li><strong>Batch normalisation.</strong> Renormalising each layer’s inputs during training keeps activations out of saturation and gradients in a usable range.</li>"
   "<li><strong>Residual connections.</strong> A skip connection gives the gradient an additive path around each block, so it reaches early layers without passing through every intermediate multiplication. This is what allows networks hundreds of layers deep.</li>"
   "<li><strong>Gradient clipping.</strong> For exploding gradients specifically, capping the gradient norm at a threshold is a blunt fix that works reliably &mdash; standard practice in recurrent networks.</li>"
   "</ul>"),
  ("What trips people up",
   "<ul>"
   "<li><strong>Diagnosing vanishing gradients as a learning-rate problem.</strong> Raising the learning rate to compensate destabilises the layers that <em>were</em> training. Fix the activation and initialisation instead.</li>"
   "<li><strong>Using sigmoid or tanh in deep hidden layers.</strong> Reasonable for a shallow network or an output; a poor default in anything deep.</li>"
   "<li><strong>Ignoring a loss that suddenly becomes NaN.</strong> That is almost always an exploding gradient. Clip the norm and check for unscaled inputs before touching the architecture.</li>"
   "<li><strong>Leaving inputs unscaled.</strong> A feature measured in the tens of thousands injects huge gradients at the first layer regardless of how well the rest is designed.</li>"
   "</ul>"),
  ("What to remember",
   "<p>Backpropagation multiplies per-layer derivatives together, so anything consistently below 1 shrinks the gradient exponentially with depth and anything above 1 amplifies it. Sigmoid’s maximum derivative of 0.25 made deep networks untrainable; ReLU’s derivative of 1 fixed it, and initialisation, normalisation and residual connections keep the product near 1 by design. When training silently stalls suspect vanishing; when the loss becomes NaN suspect exploding, and clip.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/early_stopping_in_neural_networks.html": {
 "intro": "Stop training when validation loss stops improving. It is the cheapest regulariser available - it costs nothing, needs no extra term in the loss, and often works as well as anything else.",
 "sections": [
  ("The shape every training run has",
   "<p>Training loss falls more or less monotonically: the model keeps getting better at the data it can see. Validation loss falls too, up to a point &mdash; then turns and rises.</p>"
   "<p>That turning point is where the model stops learning generalisable structure and starts memorising the training set. Everything after it makes the model worse on new data while the training curve continues to look excellent. Early stopping simply keeps the weights from the bottom of the validation curve and discards everything after.</p>"),
  ("Patience, and why you cannot stop at the first uptick",
   "<p>Validation loss is noisy. Mini-batch sampling, dropout and a finite validation set mean it rises and falls between epochs even while the underlying trend is still improving. Stopping at the first increase would stop almost immediately and almost always too early.</p>"
   "<p><strong>Patience</strong> is the number of epochs to keep training without improvement before giving up. With patience 10, the run continues 10 epochs past the best score and stops only if nothing beats it in that window.</p>"
   "<p>The other half is restoring weights. Because training continued past the best point, the <em>final</em> weights are not the best weights &mdash; the best checkpoint must be saved when it occurs and reloaded at the end. Skipping that gives you a model that is deliberately <span class=\"mono-font\">patience</span> epochs overfit.</p>"),
  ("Interactive Exploration Guide",
   "<ol>"
   "<li><strong>Watch the curves diverge.</strong> Press <strong>Start Training</strong> and follow both lines. They fall together, then separate &mdash; training keeps dropping while validation flattens and turns up. That gap is overfitting, drawn directly.</li>"
   "<li><strong>Stop too eagerly.</strong> Set <strong>Patience (Epochs)</strong> to 5 and press <strong>Reset Model</strong>, then train. The run often halts during a temporary plateau, before the model has finished improving &mdash; underfitting caused by impatience.</li>"
   "<li><strong>Give it room.</strong> Set <strong>Patience (Epochs)</strong> to 60 and train again. Now the run survives noisy stretches and stops near the true minimum, at the cost of extra epochs after the best point.</li>"
   "<li><strong>Find the middle.</strong> Try 20 and compare where it halts against the visible minimum of the validation curve. Patience is a bias&ndash;variance trade of its own: too little stops on noise, too much wastes compute.</li>"
   "</ol>"),
  ("Why it works as regularisation",
   "<p>Early stopping restricts how far the weights can travel from their initialisation. With small initial weights and a bounded number of gradient steps, the reachable region of weight space is limited &mdash; which is a constraint on effective model capacity, not merely a stopping heuristic.</p>"
   "<p>For linear models with gradient descent this can be made precise: early stopping is equivalent to L2 regularisation, with the number of epochs playing the role of 1/&lambda;. Fewer epochs correspond to a stronger penalty. Deep networks are not linear, but the intuition transfers &mdash; which is why early stopping and weight decay are partly redundant.</p>"),
  ("What usually goes wrong",
   "<ul>"
   "<li><strong>Not restoring the best weights.</strong> Stopping is only half the technique. Without <span class=\"mono-font\">restore_best_weights=True</span> or an explicit checkpoint reload, you keep the overfit weights you trained past the minimum.</li>"
   "<li><strong>Monitoring the training loss.</strong> Training loss almost never rises, so it will never trigger a stop. Monitor validation loss, or validation accuracy if that is the deployment metric.</li>"
   "<li><strong>Using the test set as the validation set.</strong> Choosing the stopping epoch by test performance leaks the test set and makes the reported number optimistic.</li>"
   "<li><strong>Patience of 1 or 2.</strong> Guaranteed to stop on noise. Scale patience to how noisy the curve is &mdash; 10 to 20 epochs is a common default.</li>"
   "<li><strong>A validation set too small to be informative.</strong> With a few hundred samples the curve is so noisy that the stopping point is essentially random.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Early stopping monitors validation loss, waits <span class=\"mono-font\">patience</span> epochs after the best score, then halts and restores the best checkpoint. It regularises by limiting how far weights travel from initialisation &mdash; provably equivalent to L2 for linear models &mdash; and it costs nothing beyond the validation split you already have. The two things that make it fail are monitoring the wrong curve and forgetting to restore the best weights.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/data_sparsity.html": {
 "intro": "When most feature values are zero, dense storage and dense arithmetic both stop making sense. Sparsity is normal in real data, and handling it well is mostly about not materialising the zeros.",
 "sections": [
  ("What sparsity means, and where it comes from",
   "<p>A feature vector is <strong>sparse</strong> when most of its entries are zero. This is not an edge case &mdash; it is the default in several of the most common data types:</p>"
   "<ul>"
   "<li><strong>One-hot encoded categories.</strong> A country field with 195 values becomes 195 columns of which exactly one is 1. That is 99.5% zeros by construction.</li>"
   "<li><strong>Bag-of-words text.</strong> A vocabulary of 50,000 words against a 200-word document gives at most 0.4% non-zero.</li>"
   "<li><strong>Recommender matrices.</strong> A user has rated a few dozen of a million items; these are routinely above 99.9% zero.</li>"
   "<li><strong>Interaction and count features</strong> where most combinations simply never occur.</li>"
   "</ul>"),
  ("Why it hurts training",
   "<p>Sparsity causes three separate problems, and they are worth keeping apart:</p>"
   "<p><strong>Memory.</strong> Storing a 100,000&times;50,000 matrix densely at 4 bytes per float is 20 GB, nearly all of it zeros. Sparse formats such as CSR store only the non-zeros plus their indices, typically cutting this by two or three orders of magnitude.</p>"
   "<p><strong>Wasted computation.</strong> A dense matrix multiply performs a multiply-add for every element, and multiplying by zero contributes nothing. Most of the arithmetic produces no information.</p>"
   "<p><strong>Uneven gradients.</strong> This is the subtle one. A weight connected to a feature that is non-zero in 0.1% of samples receives a gradient in only 0.1% of steps. Rare features therefore learn roughly a thousand times more slowly than common ones under a single global learning rate &mdash; which is precisely the problem <strong>Adagrad</strong> and <strong>Adam</strong> solve, by giving each parameter its own effective rate based on how often it has received a gradient. That is why adaptive optimisers are the standard choice on sparse data.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>Start dense.</strong> Set <strong>Input Sparsity Level</strong> to 0 and press <strong>Stream Data</strong>. Every input carries signal and every weight receives a gradient on every sample.</li>"
   "<li><strong>Introduce realistic sparsity.</strong> Set <strong>Input Sparsity Level</strong> to 70 and stream again. Most inputs are now zero, and the connections behind them go quiet &mdash; a weight whose input is zero gets no gradient at all that step.</li>"
   "<li><strong>Push it to the recommender regime.</strong> Set <strong>Input Sparsity Level</strong> to 95 and press <strong>Next Sample</strong> repeatedly. Watch how rarely any particular input activates. Those weights update on a handful of samples in a hundred, which is exactly why they lag.</li>"
   "<li><strong>Compare which weights move.</strong> At high sparsity, note that the weights attached to frequently non-zero inputs converge quickly while the rest barely move. A global learning rate cannot serve both.</li>"
   "</ol>"),
  ("Embeddings, the standard fix",
   "<p>For high-cardinality categorical data the usual answer is not to keep the one-hot vector at all. An <strong>embedding layer</strong> maps each category to a short dense vector &mdash; say 50 dimensions instead of 195 columns &mdash; learned during training.</p>"
   "<p>Mathematically this is identical to multiplying the one-hot vector by a weight matrix, but the implementation is a row lookup instead of a matrix multiply, so it skips the zeros entirely. It also solves a modelling problem: one-hot categories are all equidistant, whereas learned embeddings place similar categories near each other, so information is shared between related values rather than each being learned in isolation.</p>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Densifying a sparse matrix.</strong> Calling <span class=\"mono-font\">.toarray()</span> on a large sparse matrix is the classic out-of-memory error. Keep it sparse through the whole pipeline.</li>"
   "<li><strong>Plain SGD on sparse features.</strong> Rare features learn far too slowly. Use Adam or Adagrad, which adapt per-parameter learning rates to update frequency.</li>"
   "<li><strong>One-hot encoding a high-cardinality column.</strong> Thousands of near-empty columns; use an embedding, target encoding or hashing instead.</li>"
   "<li><strong>Mean-imputing a structural zero.</strong> In sparse data zero usually means “absent”, not “missing”. Replacing it with a column mean invents signal that was never there.</li>"
   "<li><strong>Centring sparse data.</strong> Subtracting the mean makes every zero non-zero and destroys the sparsity outright. Scale without centring.</li>"
   "</ul>"),
  ("What to remember",
   "<p>Sparse data is the norm for one-hot categories, text and recommenders, and it costs memory, wasted arithmetic, and &mdash; least obviously &mdash; badly uneven learning rates, because a weight only updates when its input is non-zero. Keep sparse matrices in sparse formats, replace one-hot encodings of high-cardinality fields with learned embeddings, and use an adaptive optimiser so rare features are not left thousands of steps behind common ones.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/weight_initialization.html": {
 "intro": "The starting values of the weights decide whether a deep network trains at all. Too small and the signal dies; too large and it explodes; all the same and the network never becomes more than one neuron wide.",
 "sections": [
  ("Why not zero, and why not all-equal",
   "<p>Initialising every weight to zero seems harmless and completely breaks the network. If all weights in a layer are identical, every neuron in that layer computes the same output, receives the same gradient, and applies the same update &mdash; so they stay identical forever. A layer of 512 such neurons has the expressive power of one.</p>"
   "<p>This is the <strong>symmetry breaking</strong> problem, and it is why initialisation must be random. Biases can safely start at zero, because the weights already break the symmetry.</p>"),
  ("The variance is what actually matters",
   "<p>Randomness alone is not enough; the <em>scale</em> of the random values decides whether signal survives depth. Each layer multiplies its input by a weight matrix, so the variance of the activations is multiplied layer by layer.</p>"
   "<p>If that per-layer factor is below 1, activations shrink geometrically and the deepest layers see almost nothing. If it is above 1, they grow geometrically and saturate or overflow. The target is a factor of about 1, so activations keep roughly constant scale from the first layer to the last &mdash; and the same for gradients on the way back.</p>"
   "<p>That is the whole design goal, and the named schemes are just different solutions to it:</p>"
   "<ul>"
   "<li><strong>Xavier / Glorot</strong> &mdash; variance <span class=\"mono-font\">2 / (n<sub>in</sub> + n<sub>out</sub>)</span>. Derived for activations symmetric about zero, so it suits tanh and sigmoid.</li>"
   "<li><strong>He / Kaiming</strong> &mdash; variance <span class=\"mono-font\">2 / n<sub>in</sub></span>. ReLU zeroes negative inputs and therefore roughly halves the variance passing through, so He compensates with the extra factor of 2. This is the right default for any ReLU network.</li>"
   "<li><strong>LeCun</strong> &mdash; variance <span class=\"mono-font\">1 / n<sub>in</sub></span>, used with SELU and self-normalising networks.</li>"
   "</ul>"
   "<p>Note that all of them scale with layer width. A 1024-unit layer needs smaller initial weights than a 64-unit one, because it sums many more terms.</p>"),
  ("Exploration guide",
   "<ol>"
   "<li><strong>Train from a reasonable start.</strong> Press <strong>Reset Weights</strong> and then <strong>Train Network</strong>. Activations stay in a usable range across the layers and the loss falls steadily.</li>"
   "<li><strong>Watch the layer-to-layer scale.</strong> During training, compare the activation magnitudes at the first and last layers. When initialisation is right they are comparable; a systematic shrink or growth across depth is the failure this whole topic exists to prevent.</li>"
   "<li><strong>Add normalisation.</strong> Enable the batch-norm toggle and press <strong>Reset Weights</strong>, then train again. Convergence becomes markedly less sensitive to where the weights started &mdash; normalisation rescales each layer regardless.</li>"
   "<li><strong>Reset repeatedly.</strong> Press <strong>Reset Weights</strong> several times and train each time. Runs differ, sometimes noticeably. The initial draw is a genuine source of run-to-run variance, which is why single-run comparisons are unreliable.</li>"
   "</ol>"),
  ("Traps worth knowing",
   "<ul>"
   "<li><strong>Zero initialisation.</strong> Symmetry never breaks and the layer collapses to a single effective neuron. Zero is fine for biases and wrong for weights.</li>"
   "<li><strong>A fixed standard deviation such as 0.01 everywhere.</strong> Ignores layer width, so wide layers explode and deep stacks vanish. This was standard before 2010 and is a large part of why deep networks did not train.</li>"
   "<li><strong>Xavier with ReLU.</strong> Understates the variance by a factor of 2, since Xavier does not account for ReLU discarding half the distribution. Use He for ReLU.</li>"
   "<li><strong>Assuming batch norm makes it irrelevant.</strong> Normalisation reduces the sensitivity but does not remove it, particularly in very deep networks and in the layers before the first normalisation.</li>"
   "<li><strong>Reinitialising a pretrained layer.</strong> When fine-tuning, only the new head should be initialised; overwriting the pretrained weights discards everything transfer learning was for.</li>"
   "</ul>"),
  ("What to remember",
   "<p>Initialisation must be random to break symmetry, and scaled to layer width so activation and gradient variance stay roughly constant with depth. He initialisation is the default for ReLU networks because ReLU halves the variance and He’s factor of 2 restores it; Xavier suits tanh and sigmoid. Get this wrong and a deep network either learns nothing or diverges &mdash; before the optimiser has had any say in the matter.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/regularization_in_neural_networks.html": {
 "intro": "Add a penalty on the size of the weights and the model prefers simpler explanations. L1 drives weights to exactly zero and selects features; L2 shrinks them all smoothly and is the usual default.",
 "sections": [
  ("Penalising complexity",
   "<p>An overfitting model has found a way to fit noise, and doing that almost always requires large weights &mdash; sharp, wiggly functions need big coefficients. Regularisation exploits that by adding the size of the weights to the loss:</p>"
   "<p class=\"mono-font\">total loss = data loss + &lambda; &times; penalty(w)</p>"
   "<p>Now the optimiser has two objectives in tension: fit the data, and keep the weights small. &lambda; sets the exchange rate. At &lambda; = 0 there is no penalty and you are back to plain training; at very large &lambda; the weights are crushed toward zero and the model underfits.</p>"),
  ("L1 and L2, and why one is sparse",
   "<p><strong>L2 (ridge, weight decay)</strong> penalises the sum of squared weights:</p>"
   "<p class=\"mono-font\">penalty = &Sigma; w<sub>i</sub>&sup2; &nbsp;&nbsp;&rarr;&nbsp;&nbsp; gradient = 2w<sub>i</sub></p>"
   "<p><strong>L1 (lasso)</strong> penalises the sum of absolute values:</p>"
   "<p class=\"mono-font\">penalty = &Sigma; |w<sub>i</sub>| &nbsp;&nbsp;&rarr;&nbsp;&nbsp; gradient = sign(w<sub>i</sub>)</p>"
   "<p>The gradients explain the difference completely. L2’s pull is <em>proportional to the weight</em>, so as a weight approaches zero the force pulling it there fades &mdash; weights shrink toward zero and never quite arrive. L1’s pull is <em>constant</em> regardless of size, so a weight near zero is pushed just as hard as a large one and is driven exactly to zero, where it stays.</p>"
   "<p>That is why L1 produces sparse models and performs feature selection, while L2 keeps every feature with a smaller coefficient. <strong>Elastic net</strong> uses both, getting L1’s selection with L2’s stability when features are correlated.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>Train with no penalty.</strong> Set <strong>Penalty Strength (&lambda;)</strong> to its minimum and press <strong>Train Network</strong>. Weights grow freely and the model fits the targets as closely as it can, noise included.</li>"
   "<li><strong>Apply L2.</strong> Enable the L2 toggle, set <strong>Penalty Strength (&lambda;)</strong> to about 0.1, press <strong>Reset &amp; Randomize Targets</strong> and train. Every weight shrinks, and none reaches zero &mdash; that smooth shrinkage is the whole behaviour of L2.</li>"
   "<li><strong>Switch to L1.</strong> Enable the L1 toggle instead at the same &lambda;. Now some weights collapse to exactly zero while others stay large. The model has selected a subset of connections and switched the rest off.</li>"
   "<li><strong>Turn it up too far.</strong> Set <strong>Penalty Strength (&lambda;)</strong> to 0.8 and train. Nearly everything is crushed toward zero and the model can no longer fit even the real structure &mdash; regularisation causing underfitting, which is the failure mode at the far end.</li>"
   "</ol>"),
  ("Weight decay is not quite L2",
   "<p>The two are used interchangeably and are only equivalent for plain SGD. Weight decay multiplies the weights by a factor slightly below 1 at each step; L2 adds a term to the loss, so its contribution passes through the optimiser’s gradient machinery.</p>"
   "<p>With Adam that difference is real. Adam divides each gradient by a running estimate of its magnitude, which also rescales the L2 term &mdash; so parameters with large gradients end up effectively less regularised. <strong>AdamW</strong> fixes this by applying the decay directly to the weights, outside the adaptive step, and it is the reason AdamW is now the default optimiser for transformers.</p>"),
  ("What usually goes wrong",
   "<ul>"
   "<li><strong>Regularising a model that is underfitting.</strong> If training loss is already high, adding a penalty makes both curves worse. Confirm the model can overfit before trying to stop it.</li>"
   "<li><strong>Penalising the biases.</strong> Biases shift the output rather than scale the input, so shrinking them limits what the model can represent without reducing overfitting. Regularise weights only.</li>"
   "<li><strong>Using L2 with Adam and expecting weight decay.</strong> Use AdamW when you want true decay.</li>"
   "<li><strong>Failing to scale features first.</strong> The penalty treats all weights equally, so a feature on a large scale needs a small weight and is under-penalised relative to the rest. Standardise before regularising.</li>"
   "<li><strong>Tuning &lambda; linearly.</strong> It spans orders of magnitude; search it on a log scale, typically 10<sup>&minus;5</sup> to 10<sup>&minus;1</sup>.</li>"
   "</ul>"),
  ("In one line",
   "<p>Regularisation adds a weight-size penalty to the loss so the optimiser trades fit against simplicity, with &lambda; setting the rate. L2 shrinks all weights proportionally and keeps every feature; L1 applies constant pressure and drives weights to exactly zero, producing a sparse, self-selecting model. Use it when the model overfits, scale the features first, and reach for AdamW if the optimiser is Adam.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/feature_scaling_in_neural_networks.html": {
 "intro": "Age runs from 18 to 80; salary runs from 20,000 to 200,000. Feed both into a network unscaled and the salary weight receives gradients thousands of times larger - so no single learning rate can train both.",
 "sections": [
  ("Why scale breaks gradient descent",
   "<p>The gradient of the loss with respect to a weight is proportional to that weight’s <em>input</em>. So a feature measured in hundreds of thousands produces gradients roughly four orders of magnitude larger than a feature measured in tens.</p>"
   "<p>That leaves no workable learning rate. Set it small enough to keep the salary weight stable and the age weight barely moves; set it large enough for age and salary diverges. The loss surface is a long narrow valley, and gradient descent bounces across it instead of running down it.</p>"
   "<p>Scaling makes the valley round. With comparable input ranges the gradients are comparable, one learning rate suits every weight, and convergence takes a fraction of the steps.</p>"),
  ("Standardisation and normalisation",
   "<p><strong>Standardisation (z-score)</strong> centres on zero with unit variance:</p>"
   "<p class=\"mono-font\">x&prime; = (x &minus; &mu;) / &sigma;</p>"
   "<p>Output is unbounded but typically within &minus;3 to +3. It preserves the shape of the distribution and handles outliers without letting them compress everything else. This is the sensible default for neural networks.</p>"
   "<p><strong>Min-max normalisation</strong> maps to a fixed range, usually [0, 1]:</p>"
   "<p class=\"mono-font\">x&prime; = (x &minus; min) / (max &minus; min)</p>"
   "<p>Useful when a bounded input is required, and fragile: a single extreme outlier sets the maximum and squashes every ordinary value into a narrow band near zero.</p>"
   "<p><strong>Robust scaling</strong> uses the median and interquartile range instead of mean and standard deviation, which is the right choice when outliers are present and genuine.</p>"),
  ("Work the numbers",
   "<p>Take age 30 and salary 60,000 with weights of 0.5 each. The salary term contributes 30,000 to the weighted sum and the age term contributes 15 &mdash; the age feature is invisible, and it would take a weight around 1000&times; larger to compete.</p>"
   "<p>Standardise first. If age has mean 45 and standard deviation 15, and salary has mean 80,000 with standard deviation 40,000:</p>"
   "<p class=\"mono-font\">age&prime;&nbsp;&nbsp;&nbsp; = (30 &minus; 45) / 15 = &minus;1.0</p>"
   "<p class=\"mono-font\">salary&prime; = (60000 &minus; 80000) / 40000 = &minus;0.5</p>"
   "<p>Both are now around 1 in magnitude, both contribute comparably, and both weights receive gradients of a similar size.</p>"),
  ("Guided experiments",
   "<ol>"
   "<li><strong>Train unscaled.</strong> Set <strong>Data Normalization Method</strong> to none, put <strong>Salary Input</strong> near 200000 and <strong>Age Input</strong> near 30, and press <strong>Start Training</strong>. Training is unstable or crawls, because one input dominates every gradient.</li>"
   "<li><strong>Standardise and repeat.</strong> Switch <strong>Data Normalization Method</strong> to standardisation, press <strong>Reset Weights</strong> and train again with the same inputs. Convergence is faster and far smoother.</li>"
   "<li><strong>Compare the scalers.</strong> Run min-max against standardisation on the same values. Min-max compresses everything into [0, 1]; standardisation centres on zero and keeps the spread &mdash; which is why it pairs better with activations symmetric about zero.</li>"
   "<li><strong>Change the learning rate under each.</strong> With scaling off, raise <strong>Learning Rate</strong> and watch it diverge. With scaling on, the same rate is stable. Scaling widens the range of learning rates that work at all.</li>"
   "</ol>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Fitting the scaler on the full dataset.</strong> Computing the mean and standard deviation before splitting leaks test information into training. Fit on train, then <span class=\"mono-font\">transform</span> validation and test with those same statistics.</li>"
   "<li><strong>Refitting the scaler at inference.</strong> Production data must use the training statistics. Fitting a new scaler on a single incoming batch produces silently wrong inputs.</li>"
   "<li><strong>Scaling one-hot columns.</strong> They are already on a comparable scale, and standardising them destroys sparsity by making every zero non-zero.</li>"
   "<li><strong>Min-max with outliers.</strong> One extreme value compresses everything else into a sliver of the range. Use standardisation or robust scaling.</li>"
   "<li><strong>Scaling the target without inverting it.</strong> If you scale y for training, predictions come back in scaled units and must be transformed back before they mean anything.</li>"
   "</ul>"),
  ("In one line",
   "<p>Gradients scale with input magnitude, so unscaled features give some weights enormous gradients and others negligible ones, and no single learning rate serves both. Standardisation is the default for neural networks; min-max suits bounded inputs and breaks on outliers. Fit the scaler on the training split only, keep those statistics for validation, test and production, and leave one-hot columns alone.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/batch_processing_in_neural_networks.html": {
 "intro": "Networks process many samples at once, not one at a time. Batching is what makes GPUs worth using - and the batch size quietly changes both how fast you train and how well the result generalises.",
 "sections": [
  ("A batch is a matrix, not a loop",
   "<p>Feeding one sample through a layer is a vector-matrix product. Feeding 32 samples is a <em>matrix</em>-matrix product &mdash; stack the 32 input vectors into a 32&times;n<sub>in</sub> matrix and multiply once by the same n<sub>in</sub>&times;n<sub>out</sub> weights.</p>"
   "<p>Crucially the weights are unchanged. Batching does not alter the model; it changes how many samples pass through it per operation. Because the hardware executes one large matrix multiply far more efficiently than 32 small ones, a batch of 32 costs nothing like 32 times a single sample.</p>"),
  ("Epoch, batch, iteration",
   "<p>These three get muddled constantly:</p>"
   "<ul>"
   "<li><strong>Batch size</strong> &mdash; samples processed before one weight update.</li>"
   "<li><strong>Iteration (step)</strong> &mdash; one forward pass, one backward pass, one update.</li>"
   "<li><strong>Epoch</strong> &mdash; one complete pass over the training set.</li>"
   "</ul>"
   "<p>With 10,000 samples and a batch size of 100, one epoch is 100 iterations, so 10 epochs means 1,000 weight updates. Halving the batch size to 50 doubles the updates per epoch to 200 &mdash; which is why batch size and learning rate cannot be tuned independently.</p>"),
  ("Things to try",
   "<ol>"
   "<li><strong>Watch a single sample flow.</strong> Set <strong>Batch Size</strong> to 1 and press <strong>Simulate Flow</strong>. One activation pattern moves through the network and one update follows &mdash; maximally noisy and maximally frequent.</li>"
   "<li><strong>Batch it up.</strong> Set <strong>Batch Size</strong> to 32 and simulate again. Many samples traverse together and produce a single averaged update. The averaging is where the noise reduction comes from.</li>"
   "<li><strong>Count the updates.</strong> Fix <strong>Epochs</strong> and compare <strong>Batch Size</strong> 1 against 100. The same epoch count gives a hundred times fewer weight updates at the larger batch &mdash; the usual reason a large-batch run appears to underfit.</li>"
   "<li><strong>Widen the network.</strong> Raise <strong>Input</strong> and <strong>Output</strong> and simulate at a large batch. More arithmetic per sample makes the batched matrix multiply proportionally more worthwhile.</li>"
   "</ol>"),
  ("How batch size affects the result, not just the speed",
   "<p>Larger batches give a lower-variance estimate of the true gradient, so the path to the minimum is smoother. That sounds strictly good and is not.</p>"
   "<p>The noise in small-batch gradients acts as a regulariser. It shakes the optimiser out of sharp, narrow minima and toward flat, wide ones &mdash; and flat minima generalise better, because a small shift in the weights or the data distribution barely changes the loss. Large-batch training tends to settle into sharp minima and frequently generalises slightly worse, an effect known as the <strong>generalisation gap</strong>.</p>"
   "<p>The standard mitigation is the <strong>linear scaling rule</strong>: when you multiply the batch size by k, multiply the learning rate by k as well, since each update is now averaged over k times as much data. Combined with a short warmup this makes large-batch training match small-batch accuracy in most settings.</p>"),
  ("Where this goes wrong",
   "<ul>"
   "<li><strong>Raising the batch size and leaving the learning rate alone.</strong> Fewer, no-larger updates per epoch means visibly slower convergence. Scale the rate with the batch.</li>"
   "<li><strong>Choosing the batch size purely by what fits in memory.</strong> The largest batch that fits is not automatically the best one; it is a regularisation choice as well as a throughput one.</li>"
   "<li><strong>Batch normalisation with tiny batches.</strong> Batch norm estimates mean and variance from the batch. At a batch size of 2 or 4 those estimates are noise; use group or layer normalisation instead.</li>"
   "<li><strong>A final partial batch.</strong> When the dataset does not divide evenly the last batch is smaller, which skews batch-norm statistics and any per-batch averaging. Drop it during training if it is much smaller.</li>"
   "<li><strong>Comparing runs by epoch instead of by update.</strong> Two runs at different batch sizes have done very different amounts of optimisation after the same number of epochs.</li>"
   "</ul>"),
  ("Key takeaway",
   "<p>Batching turns many small vector-matrix products into one large matrix-matrix product, which is what makes parallel hardware pay off, without changing the model at all. Batch size sets both the number of updates per epoch and the noise in each gradient, so it trades throughput against a regularising effect that favours flat minima. Change it and change the learning rate with it &mdash; roughly linearly &mdash; or the comparison is not fair.</p>"),
 ]},

}


# ---------------------------------------------------------------------------
# Eight pages already had an entry in articles.py. The writing there is fine,
# there was just not enough of it - around 320 words, which reads as an article
# and is not one. Rather than rewrite what already works, these sections are
# inserted ahead of the "Try this above" block, so each page keeps its existing
# opening and gains the depth underneath it.
# ---------------------------------------------------------------------------

EXTRA_SECTIONS_DL = {

"deep_learning/neural_network.html": [
 ("Why stacking layers buys anything",
  "<p>A layer computes a weighted sum and applies an activation. Stack two <em>linear</em> layers and you have gained nothing at all: the composition of two matrix multiplications is another matrix multiplication, so a hundred linear layers collapse to a single equivalent one.</p>"
  "<p>The activation is what breaks that collapse. Because it is non-linear, the composition cannot be flattened, and each additional layer can express something the previous one could not. This is the entire reason depth exists &mdash; remove the activations and a deep network is exactly as powerful as logistic regression, however many layers it has.</p>"),
 ("What the hidden layers represent",
  "<p>The universal approximation theorem says one sufficiently wide hidden layer can approximate any continuous function to arbitrary accuracy. That is reassuring and almost useless in practice, because “sufficiently wide” can mean exponentially many neurons.</p>"
  "<p>Depth is what makes it tractable. Layers build features hierarchically: in a vision network the first layer responds to edges, the second to corners and textures assembled from those edges, the third to object parts, and so on. Each layer reuses the previous layer’s features rather than rediscovering them, so a deep network needs far fewer neurons than a shallow one to express the same function.</p>"),
 ("Choosing width and depth",
  "<p>There is no formula, but there are reliable starting points. Begin with one or two hidden layers for tabular data; deeper networks rarely help there and images or sequences are better served by architectures designed for them. Set the width somewhere between the input and output sizes, and prefer a rough funnel &mdash; wider near the input, narrowing toward the output.</p>"
  "<p>Then let the training curves decide. If the model cannot drive training loss down it lacks capacity, so widen or deepen it. If training loss is near zero while validation loss climbs, it has too much capacity for the data available, and the answer is regularisation or more data rather than a smaller network. Increase capacity until the model can overfit, then regularise back &mdash; that order is far more reliable than guessing an architecture up front.</p>"),
],

"deep_learning/neural_network_for_regression.html": [
 ("Why the output layer has no activation",
  "<p>A classification network ends in softmax or sigmoid because the output must be a probability, bounded in [0, 1]. A regression network predicts an unbounded quantity &mdash; a price, a temperature, a duration &mdash; so squashing the output would put a ceiling on what it can ever predict.</p>"
  "<p>The final layer is therefore left linear: a plain weighted sum with no activation applied. Putting a sigmoid there caps every prediction at 1, and putting a ReLU there makes negative predictions impossible &mdash; occasionally what you want for a strictly positive target, and a silent bug otherwise.</p>"),
 ("Choosing the loss",
  "<p>The loss encodes what kind of error you care about, and the two standard choices behave very differently:</p>"
  "<ul>"
  "<li><strong>MSE</strong> (mean squared error) squares the error, so an error of 10 counts a hundred times an error of 1. It is smooth and differentiable everywhere, and highly sensitive to outliers.</li>"
  "<li><strong>MAE</strong> (mean absolute error) scales linearly with the error, so outliers do not dominate. Its gradient is constant in magnitude, which converges less cleanly near the minimum.</li>"
  "<li><strong>Huber loss</strong> is quadratic for small errors and linear for large ones, giving MSE’s smooth convergence with MAE’s outlier tolerance. It is the sensible default on noisy data.</li>"
  "</ul>"
  "<p>These are not interchangeable: minimising MSE fits the conditional <em>mean</em> of the target, minimising MAE fits the <em>median</em>. On a skewed target those are different numbers, and the choice of loss is really a choice about which one you want.</p>"),
 ("Scaling the target, not just the inputs",
  "<p>Feature scaling gets the attention, but for regression the target matters just as much. A target in the hundreds of thousands produces enormous initial losses and correspondingly enormous gradients, which either diverges immediately or forces a learning rate so small that nothing else trains.</p>"
  "<p>Standardise the target for training, then invert the transform on the predictions before reporting or using them. Forgetting that inversion produces predictions in standardised units &mdash; numbers around zero where the answer should be 250,000 &mdash; which is one of the more embarrassing bugs to ship, because the model itself is entirely correct.</p>"),
],

"deep_learning/overfitting_vs_underfitting.html": [
 ("The bias-variance decomposition",
  "<p>Expected error on unseen data splits into three parts:</p>"
  "<p class=\"mono-font\">error = bias&sup2; + variance + irreducible noise</p>"
  "<p><strong>Bias</strong> is error from wrong assumptions &mdash; a model too simple to represent the real relationship. High bias is underfitting, and it shows up as poor performance on training <em>and</em> validation data.</p>"
  "<p><strong>Variance</strong> is sensitivity to the particular training sample &mdash; a model flexible enough to fit noise. High variance is overfitting: excellent training performance, poor validation performance.</p>"
  "<p><strong>Irreducible noise</strong> is the part no model can remove. If the same inputs sometimes produce different outputs, no amount of capacity will fix it, and a validation loss that flattens above zero is often this rather than a failure.</p>"
  "<p>Capacity trades the first two against each other: adding it lowers bias and raises variance. The best model sits where their sum is smallest, not where either is minimised.</p>"),
 ("Telling them apart from two numbers",
  "<p>The diagnosis needs only the training and validation loss, compared against each other and against what is achievable:</p>"
  "<ul>"
  "<li><strong>Both high, close together</strong> &mdash; underfitting. The model cannot represent the pattern. Add capacity, train longer, or reduce regularisation.</li>"
  "<li><strong>Training low, validation much higher</strong> &mdash; overfitting. The model has memorised. Add data, add regularisation, or reduce capacity.</li>"
  "<li><strong>Both low, close together</strong> &mdash; this is what you want.</li>"
  "<li><strong>Training loss above validation loss</strong> &mdash; usually not a paradox but an artefact: dropout and batch norm are active during training and disabled at validation, so the training number is measured on a handicapped model.</li>"
  "</ul>"),
 ("Fixes, in the order worth trying",
  "<p>For <strong>overfitting</strong>, more data is the only fix with no downside, and augmentation is the cheap approximation to it. After that: early stopping, which costs nothing; then dropout or weight decay; and only then a smaller model, since shrinking capacity is the bluntest option.</p>"
  "<p>For <strong>underfitting</strong>, first confirm the model is training at all &mdash; a learning rate that is too high or too low looks exactly like insufficient capacity. Then widen or deepen the network, remove regularisation, train for longer, or improve the features. A model that cannot overfit a small subset of the training data has a bug, not a capacity problem, and that is the fastest test to run.</p>"),
],

"deep_learning/activation_functions.html": [
 ("The dying ReLU problem",
  "<p>ReLU outputs zero for any negative input, and its derivative there is also zero. If a neuron’s weights are pushed far enough negative that it outputs zero for <em>every</em> training example, it receives no gradient &mdash; and with no gradient it can never recover. The neuron is permanently dead.</p>"
  "<p>This is not rare. A large learning rate can kill a substantial fraction of a layer in a single update, and dead neurons are invisible in the loss curve; the network simply has less capacity than you think it does.</p>"
  "<p><strong>Leaky ReLU</strong> fixes it by giving negative inputs a small slope, typically 0.01, so the gradient is never exactly zero and a neuron can always climb back. <strong>ELU</strong> and <strong>GELU</strong> do the same with a smooth curve, and GELU is the standard choice in transformers.</p>"),
 ("Which one to use where",
  "<ul>"
  "<li><strong>Hidden layers, general default</strong> &mdash; ReLU. Cheap, no vanishing gradient in the positive region, and works.</li>"
  "<li><strong>Hidden layers, if neurons are dying</strong> &mdash; Leaky ReLU or ELU.</li>"
  "<li><strong>Transformers</strong> &mdash; GELU, essentially universally.</li>"
  "<li><strong>Recurrent networks</strong> &mdash; tanh inside the cell, because bounded outputs keep the recurrent state from growing without limit.</li>"
  "<li><strong>Anywhere deep, with sigmoid</strong> &mdash; avoid. Its maximum derivative of 0.25 shrinks the gradient by at least a factor of four per layer.</li>"
  "</ul>"),
 ("Output activations are a separate decision",
  "<p>Hidden-layer activations exist to introduce non-linearity. Output activations exist to put the prediction in the right range, and the choice is dictated by the task rather than by preference:</p>"
  "<ul>"
  "<li><strong>Regression</strong> &mdash; no activation. The output must be unbounded.</li>"
  "<li><strong>Binary classification</strong> &mdash; sigmoid, giving one probability in [0, 1].</li>"
  "<li><strong>Multi-class, one label</strong> &mdash; softmax, giving probabilities across classes that sum to 1.</li>"
  "<li><strong>Multi-label</strong> &mdash; sigmoid on each output independently, since several labels can be true at once and the outputs should <em>not</em> sum to 1.</li>"
  "</ul>"
  "<p>One practical warning: frameworks usually fold the output activation into the loss for numerical stability, so <span class=\"mono-font\">CrossEntropyLoss</span> in PyTorch expects raw logits and applies softmax itself. Adding your own softmax before it applies the function twice and quietly degrades training.</p>"),
],

"deep_learning/gradient_descent_batch_processing.html": [
 ("Why mini-batch won",
  "<p>Batch gradient descent computes an exact gradient and needs a full pass over the data for a single update. On a million samples that is a million forward passes to move the weights once &mdash; accurate and unusable.</p>"
  "<p>Stochastic gradient descent updates after every sample, so it makes a million updates per epoch, but each gradient is a single-sample estimate and the path jitters badly. It also wastes the hardware: one sample cannot occupy a GPU.</p>"
  "<p>Mini-batches of 32 to 256 sit at the point where both problems disappear. The gradient estimate is close enough to the true one for stable progress, updates are frequent, and the batch is large enough to fill the device. This is not a compromise nobody is happy with &mdash; it is better than either extreme on both axes that matter.</p>"),
 ("Batch size and learning rate move together",
  "<p>These two cannot be tuned independently. The gradient of a batch is an <em>average</em>, so a larger batch gives a lower-variance estimate &mdash; and a more reliable estimate can support a larger step.</p>"
  "<p>The <strong>linear scaling rule</strong> is the standard heuristic: multiply the batch size by k and multiply the learning rate by k. Going from batch 32 at learning rate 0.01 to batch 256 suggests roughly 0.08. Very large batches usually need a warmup period as well, ramping the rate up over the first few epochs, because the scaled rate is unstable while the weights are still random.</p>"
  "<p>The corollary is that comparing two runs at different batch sizes with the same learning rate compares nothing useful.</p>"),
 ("Shuffling is not optional",
  "<p>Mini-batches must be drawn from a shuffled dataset, reshuffled every epoch. If the data arrives sorted by class &mdash; all the cats then all the dogs &mdash; then each batch contains one class, every gradient points toward predicting that class, and the model oscillates instead of converging.</p>"
  "<p>Reshuffling each epoch also means the model never sees the same batch composition twice, which adds a small amount of useful noise. The exception is time series, where shuffling destroys the temporal ordering the model is supposed to learn from; there the batches must be contiguous windows.</p>"),
],

"deep_learning/weights_and_biases.html": [
 ("Why the bias cannot be dropped",
  "<p>Without a bias, the weighted sum is zero whenever every input is zero, so the decision boundary is forced through the origin. That is a severe restriction: a neuron that should fire only when its input exceeds 5 cannot express that threshold at all, because it has no way to shift its output independently of the inputs.</p>"
  "<p>The bias supplies exactly that freedom. In <span class=\"mono-font\">y = wx + b</span>, w tilts the line and b slides it &mdash; and the same is true in a thousand dimensions, where the weights orient a hyperplane and the bias offsets it from the origin. One extra parameter per neuron buys the ability to place the boundary anywhere rather than only through a single fixed point.</p>"),
 ("Counting a layer's parameters",
  "<p>A fully connected layer with n<sub>in</sub> inputs and n<sub>out</sub> outputs has one weight per connection plus one bias per output neuron:</p>"
  "<p class=\"mono-font\">parameters = (n<sub>in</sub> &times; n<sub>out</sub>) + n<sub>out</sub></p>"
  "<p>For 784 inputs and 128 outputs that is 784 &times; 128 + 128 = <strong>100,480</strong>. The biases are 128 of them &mdash; about 0.1% of the total, which is why they are cheap enough to always include and why regularisation normally skips them.</p>"
  "<p>Notice the weight count is a product. Doubling either the input or the output size doubles the parameters; doubling both quadruples them. That quadratic growth is why wide layers dominate a network’s memory footprint.</p>"),
 ("What training actually changes",
  "<p>Training changes nothing about the network except these numbers. The architecture, the activations and the connections are all fixed before the first step; gradient descent only ever adjusts weights and biases.</p>"
  "<p>That is worth holding onto, because it clarifies what a trained model <em>is</em>: a specific set of values for these parameters. Saving a model saves the weights and biases. Transfer learning reuses another model’s weights and biases. A randomly initialised network and a fully trained one differ in no other respect.</p>"),
],

"deep_learning/model_training_curve.html": [
 ("Reading the gap between the curves",
  "<p>The two curves matter less individually than the distance between them, and how that distance changes over time.</p>"
  "<p>A gap that stays narrow while both curves fall is a healthy run. A gap that opens steadily &mdash; training continuing down while validation flattens or rises &mdash; is overfitting, and the epoch where validation turns is where early stopping should trigger. Both curves flat and high means the model has not got started: check the learning rate before assuming the architecture is too small.</p>"
  "<p>The size of the gap is not itself a problem. A large but stable gap on a model whose validation loss is still the best you have achieved is fine; it is the <em>trend</em> in validation loss that decides whether to stop.</p>"),
 ("Curves that mean something is broken",
  "<ul>"
  "<li><strong>Loss becomes NaN.</strong> Exploding gradients or a numerical error such as log(0). Lower the learning rate, clip the gradient norm, and check for unscaled inputs.</li>"
  "<li><strong>Loss is completely flat from step one.</strong> Nothing is learning. Usually a learning rate near zero, a disconnected graph, or gradients not flowing &mdash; verify the optimiser is actually stepping the parameters you think it is.</li>"
  "<li><strong>Loss oscillates violently without trending down.</strong> Learning rate too high. Divide by ten.</li>"
  "<li><strong>Validation loss much lower than training loss.</strong> Normally dropout and batch norm being active during training only. If the gap is large and persistent, suspect a leak or a validation split that is easier than the training set.</li>"
  "<li><strong>Loss drops sharply at each epoch boundary.</strong> The data is not being reshuffled, so the model is memorising batch order.</li>"
  "</ul>"),
 ("What a healthy run looks like",
  "<p>A steep initial drop as the model learns the easy structure, then a long shallow decline as it refines. Validation tracks training closely at first and gradually separates. Both curves are noisy step to step &mdash; that is mini-batch sampling, not instability &mdash; and the trend over a window of epochs is what to judge.</p>"
  "<p>If loss is still falling meaningfully when training ends, you stopped too early. If validation has been flat or rising for many epochs, you trained too long and the useful checkpoint is behind you.</p>"),
],

"deep_learning/optimizers_in_neural_networks.html": [
 ("Momentum, precisely",
  "<p>Plain SGD steps in the direction of the current gradient and forgets everything before it. Momentum keeps a running average of past gradients and steps along that instead:</p>"
  "<p class=\"mono-font\">v &larr; &beta;v + (1 &minus; &beta;)&nabla;L&nbsp;&nbsp;&nbsp;&nbsp;w &larr; w &minus; &eta;v</p>"
  "<p>With the usual &beta; = 0.9 the velocity is an average over roughly the last ten gradients. Consistent directions accumulate and speed up; directions that flip sign each step cancel out. That is exactly the fix for a narrow valley, where the gradient across the valley alternates while the gradient along it stays constant &mdash; the oscillation cancels and the useful direction survives.</p>"),
 ("What Adam actually stores",
  "<p>Adam keeps two running averages per parameter: the mean of the gradients (momentum, as above) and the mean of their <em>squares</em>. It divides the step by the square root of that second average:</p>"
  "<p class=\"mono-font\">w &larr; w &minus; &eta; &middot; m&#770; / (&radic;v&#770; + &epsilon;)</p>"
  "<p>The effect is a per-parameter learning rate. A parameter that has consistently seen large gradients gets a smaller effective step; one that has seen small or infrequent gradients gets a larger one. That is what makes Adam so effective on sparse data, where rare features would otherwise learn thousands of times more slowly than common ones.</p>"
  "<p>The cost is memory: two extra values per parameter, so optimiser state is three times the size of the model. On a large model that is a real constraint, and it is why plain SGD with momentum is still used where memory is tight.</p>"),
 ("Which optimiser to reach for",
  "<ul>"
  "<li><strong>AdamW</strong> &mdash; the default for almost everything now, and the correct choice whenever weight decay is used, because plain Adam’s L2 term gets rescaled by the adaptive step and stops behaving like decay.</li>"
  "<li><strong>SGD with momentum</strong> &mdash; still the best final accuracy on large vision models, given a good learning-rate schedule. It needs more tuning and generalises slightly better.</li>"
  "<li><strong>Adam</strong> &mdash; fine when there is no weight decay; otherwise prefer AdamW.</li>"
  "<li><strong>Adagrad / RMSprop</strong> &mdash; largely superseded by Adam, which combines their ideas with momentum.</li>"
  "</ul>"
  "<p>A practical note: the optimiser is not a substitute for the learning rate. Adam’s default of 0.001 is a reasonable starting point rather than a universal answer, and a badly chosen rate will defeat any optimiser on this list.</p>"),
],

}
