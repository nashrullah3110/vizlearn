# -*- coding: utf-8 -*-
"""Written explanations for the deep-learning modules that shipped with a
generic placeholder article.

Fourteen pages carried a fill-in-the-blank skeleton ("This topic strongly
influences convergence speed, generalization, and training reliability") where
the same sentences appeared on a dozen pages and nothing was specific to the
topic. Measured, over half of each of those pages' sentences appeared verbatim
elsewhere on the site.

Everything here is written for its own page: real numbers, the actual control
names on that page, and failure modes that only apply to that technique.

Rendered by tools/build_articles.py into the <!-- auto-article-vizlearn -->
section. Edit here, then `npm run build`.
"""

# Each entry: intro paragraph, then (heading, html) sections.
ARTICLES = {

# ---------------------------------------------------------------------------
"deep_learning/perceptron.html": {
 "intro": "A perceptron is the smallest complete unit of a neural network: one weighted sum, one bias, one activation. Everything deeper is this repeated.",
 "sections": [
  ("The whole computation, in one line",
   "<p>A perceptron takes each input, multiplies it by a weight, adds them all up, adds a bias, and pushes the result through an activation function:</p>"
   "<p class=\"mono-font\">z = w<sub>1</sub>x<sub>1</sub> + w<sub>2</sub>x<sub>2</sub> + &hellip; + w<sub>n</sub>x<sub>n</sub> + b &nbsp;&nbsp;&rarr;&nbsp;&nbsp; output = f(z)</p>"
   "<p>That is the entire model. The weights decide how much each input matters and in which direction; the bias decides how large the sum has to be before the neuron responds at all.</p>"),
  ("Work one through by hand",
   "<p>Take two inputs with weights <span class=\"mono-font\">w = [0.6, &minus;0.4]</span> and bias <span class=\"mono-font\">b = 0.1</span>. Feed it <span class=\"mono-font\">x = [1.0, 0.5]</span>:</p>"
   "<p class=\"mono-font\">z = (0.6 &times; 1.0) + (&minus;0.4 &times; 0.5) + 0.1 = 0.6 &minus; 0.2 + 0.1 = 0.5</p>"
   "<p>With a <strong>Step</strong> activation the output is 1, because z is above zero. With <strong>Sigmoid</strong> the same z gives 1 / (1 + e<sup>&minus;0.5</sup>) = <strong>0.62</strong> &mdash; the same decision, but now with a sense of how confident it is. That difference is the whole reason step activations were abandoned.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Set <strong>Number of Inputs</strong> to 2 and pick <strong>Step (Binary)</strong>. The output can only ever be 0 or 1.</li>"
   "<li>Switch to <strong>Sigmoid (Smooth)</strong> without changing anything else. Same weighted sum, but the output now slides continuously.</li>"
   "<li>Switch to <strong>ReLU (Rectified)</strong> and make z negative. The output pins to exactly 0 and stays there.</li>"
   "<li>Raise <strong>Number of Inputs</strong> to 5 and count the weights &mdash; one per input, plus a single bias regardless.</li>"
   "</ol>"),
  ("Where a single perceptron fails",
   "<p>One perceptron draws exactly one straight boundary. That is enough for AND and OR, and famously not enough for XOR &mdash; no single line separates XOR's two classes, so no assignment of weights and bias will ever solve it. This limitation stalled neural network research for years; the answer was to stack perceptrons into layers.</p>"
   "<p>The other trap is the Step activation itself. Its gradient is zero everywhere it is defined, so gradient descent has nothing to follow. You cannot train a step-activated network by backpropagation, which is why sigmoid and later ReLU took over.</p>"),
  ("In one line",
   "<p>One weighted sum, one bias, one activation, one straight boundary &mdash; and a hard ceiling on what that can express.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/weights_and_biases.html": {
 "intro": "Weights and biases are the numbers a network actually learns. Every other setting you choose is in service of finding good values for these two.",
 "sections": [
  ("What each one does geometrically",
   "<p>A neuron computes <span class=\"mono-font\">z = w &middot; x + b</span>. Those two terms do different jobs, and it is worth separating them:</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Weights rotate.</strong> They set the orientation of the decision boundary &mdash; which direction in input space the neuron is sensitive to, and how strongly.</li>"
   "<li><strong>The bias translates.</strong> It slides the boundary without turning it. Without a bias every boundary is forced through the origin, which is a severe and usually pointless restriction.</li>"
   "</ul>"),
  ("A concrete example",
   "<p>One input, weight <span class=\"mono-font\">w = 2.0</span>, bias <span class=\"mono-font\">b = 0</span>. At <span class=\"mono-font\">x = 0.5</span> you get <span class=\"mono-font\">z = 1.0</span> &mdash; the neuron fires.</p>"
   "<p>Now set <span class=\"mono-font\">b = &minus;1.5</span> and leave everything else alone: <span class=\"mono-font\">z = 1.0 &minus; 1.5 = &minus;0.5</span>. Same input, same weight, opposite decision. The bias moved the threshold from <span class=\"mono-font\">x &gt; 0</span> to <span class=\"mono-font\">x &gt; 0.75</span>.</p>"
   "<p>This is why a bias is not optional detail. It is the difference between \"is this input positive?\" and \"is this input above the level that actually matters?\"</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Set <strong>Number of Inputs</strong> to 1 so there is a single weight to watch.</li>"
   "<li>Change that weight and watch the response curve steepen and flip direction. Negative weights invert the neuron's opinion of that feature.</li>"
   "<li>Now change only the bias. The shape stays identical; it slides sideways.</li>"
   "<li>Switch <strong>Activation Function</strong> between Step and Sigmoid and repeat &mdash; the geometry is the same, only the sharpness changes.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Wildly different weight magnitudes</strong> are almost always a symptom of unscaled inputs rather than a real finding. If one feature is measured in thousands and another in decimals, the network compensates with tiny and huge weights, and gradient descent struggles to move both usefully. Scale the inputs instead.</p>"
   "<p><strong>Reading a single weight as feature importance</strong> is unreliable in anything deeper than one layer. In a multi-layer network a feature's influence is spread across many paths, and a small first-layer weight can still matter enormously downstream.</p>"),
  ("In one line",
   "<p>Weights decide direction and strength; the bias decides where the threshold sits.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/activation_functions.html": {
 "intro": "Without a non-linearity between layers, stacking them is pointless: any chain of linear maps collapses into a single linear map. Activations are what make depth mean something.",
 "sections": [
  ("Why depth needs a bend",
   "<p>Two linear layers in a row compute <span class=\"mono-font\">W<sub>2</sub>(W<sub>1</sub>x) = (W<sub>2</sub>W<sub>1</sub>)x</span>, which is just another single matrix. A hundred stacked linear layers still only draw a straight boundary. Inserting a non-linear function between them is what lets a network represent curves, corners and disjoint regions.</p>"),
  ("The four you will actually meet",
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Sigmoid</strong> &mdash; <span class=\"mono-font\">1 / (1 + e<sup>&minus;x</sup>)</span>, output in (0, 1). Reads as a probability, which is why it survives at the output of binary classifiers.</li>"
   "<li><strong>Tanh</strong> &mdash; output in (&minus;1, 1) and centred on zero, which tends to train better than sigmoid in hidden layers.</li>"
   "<li><strong>ReLU</strong> &mdash; <span class=\"mono-font\">max(0, x)</span>. Gradient is exactly 1 for positive input and exactly 0 otherwise. Cheap, and the default for hidden layers.</li>"
   "<li><strong>Leaky ReLU</strong> &mdash; <span class=\"mono-font\">max(0.01x, x)</span>. Keeps a small gradient alive on the negative side.</li>"
   "</ul>"),
  ("Numbers at three inputs",
   "<p>Set the same x through each function and the differences become obvious:</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><span class=\"mono-font\">x = 2</span> &rarr; sigmoid <strong>0.881</strong>, tanh <strong>0.964</strong>, ReLU <strong>2.0</strong></li>"
   "<li><span class=\"mono-font\">x = &minus;2</span> &rarr; sigmoid <strong>0.119</strong>, tanh <strong>&minus;0.964</strong>, ReLU <strong>0</strong></li>"
   "<li><span class=\"mono-font\">x = 10</span> &rarr; sigmoid <strong>0.99995</strong>, and its slope there is about <strong>0.000045</strong></li>"
   "</ul>"
   "<p>That last figure is the problem in a nutshell. A neuron sitting at x = 10 with a sigmoid has effectively stopped learning: the gradient flowing back through it is almost zero.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Drag <strong>Input Value (x)</strong> to around 6 and look at sigmoid and tanh. Both are pinned near their ceiling and the curve is nearly flat &mdash; that flatness is saturation.</li>"
   "<li>Bring x back toward 0. Both functions are at their steepest here, which is where they learn fastest.</li>"
   "<li>Set x to &minus;3 and note ReLU outputs exactly 0, not a small number.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Sigmoid in deep hidden layers.</strong> Its derivative peaks at 0.25, so gradients shrink by at least 4&times; per layer. Five layers of sigmoid multiplies the gradient by roughly 0.25<sup>5</sup> &asymp; 0.001 in the best case &mdash; the early layers barely move. This is the vanishing gradient problem, and it is why ReLU became standard.</p>"
   "<p><strong>Dying ReLU.</strong> A neuron pushed firmly negative outputs 0 and has zero gradient, so nothing ever pulls it back. It is dead for the rest of training. Leaky ReLU exists precisely to leave a small escape route.</p>"),
  ("In one line",
   "<p>ReLU in the hidden layers by default; sigmoid or softmax only at the output, where the bounded range is the point.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/how_loss_is_calculated.html": {
 "intro": "The loss is the single number that training is allowed to care about. Every gradient in the network is a derivative of this one value.",
 "sections": [
  ("What a loss function has to do",
   "<p>A loss collapses a whole batch of predictions into one scalar, and it has to do so in a way that is differentiable &mdash; otherwise there is nothing to descend. Which function you pick depends on what you are predicting.</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Regression</strong> &mdash; mean squared error: <span class=\"mono-font\">MSE = mean((y &minus; &#375;)<sup>2</sup>)</span></li>"
   "<li><strong>Classification</strong> &mdash; cross-entropy: <span class=\"mono-font\">&minus;&Sigma; y log(&#375;)</span></li>"
   "</ul>"),
  ("Both, with real numbers",
   "<p><strong>MSE.</strong> Predictions <span class=\"mono-font\">[2.5, 0.0, 2.0]</span> against targets <span class=\"mono-font\">[3.0, &minus;0.5, 2.0]</span>. The errors are 0.5, 0.5 and 0. Squared: 0.25, 0.25, 0. Mean: <strong>0.167</strong>. Squaring means one error of 2.0 costs more than four errors of 0.5.</p>"
   "<p><strong>Cross-entropy.</strong> If the model gives the correct class a probability of 0.7, the loss is <span class=\"mono-font\">&minus;ln(0.7) = 0.357</span>. If it gives that class only 0.05, the loss is <span class=\"mono-font\">&minus;ln(0.05) = 3.00</span> &mdash; roughly eight times worse. Being confidently wrong is punished far harder than being uncertain.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Raise <strong>Batch Size</strong> and watch the reported loss steady. Averaging over more samples reduces the sample-to-sample swing without changing what is being measured.</li>"
   "<li>Increase <strong>Dropout</strong> and note training loss climbing. That is expected &mdash; you are deliberately handicapping the network during training.</li>"
   "<li>Add hidden capacity with <strong>Hidden</strong> and watch how quickly loss falls across <strong>Epochs</strong>.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Comparing loss values that are not comparable.</strong> A loss summed over a batch and a loss averaged over a batch differ by a factor of the batch size. Two runs with different batch sizes or different reduction settings are not measuring the same thing, and neither is a run that changed loss function mid-experiment.</p>"
   "<p><strong>MSE on a classifier.</strong> It technically works and trains badly. When the model is confidently wrong, cross-entropy produces a large gradient and MSE produces a small one, so the model is slowest to fix exactly the errors that matter most.</p>"
   "<p><strong>Unscaled regression targets.</strong> Squared error on values around 300,000 produces enormous gradients. Scale the target, or the first update will destroy the weights.</p>"),
  ("In one line",
   "<p>The loss is the only thing the network is optimising &mdash; if it does not measure what you care about, nothing downstream can fix that.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/linear_regression_with_gradient_descent.html": {
 "intro": "Fitting a straight line is the smallest problem that still uses the real training loop. Two parameters, a real loss, real gradients &mdash; everything a deep network does, at a scale you can follow by hand.",
 "sections": [
  ("The two gradients",
   "<p>You are fitting <span class=\"mono-font\">y = mx + c</span> by minimising mean squared error. The partial derivatives are:</p>"
   "<p class=\"mono-font\">&part;L/&part;m = &minus;(2/n) &Sigma; x(y &minus; &#375;)<br>&part;L/&part;c = &minus;(2/n) &Sigma; (y &minus; &#375;)</p>"
   "<p>and each step is <span class=\"mono-font\">m &larr; m &minus; &eta; &middot; &part;L/&part;m</span>, likewise for c. That is the same update rule a network with millions of parameters uses.</p>"),
  ("One step, worked out",
   "<p>Three points: (1, 2), (2, 4), (3, 6). The answer is obviously m = 2, c = 0, but start from m = 0, c = 0 and let the maths find it.</p>"
   "<p>With m = c = 0 every prediction is 0, so the residuals are 2, 4 and 6.</p>"
   "<p class=\"mono-font\">&part;L/&part;m = &minus;(2/3)[(1&times;2) + (2&times;4) + (3&times;6)] = &minus;(2/3)(28) = &minus;18.67<br>"
   "&part;L/&part;c = &minus;(2/3)(2 + 4 + 6) = &minus;8.00</p>"
   "<p>At a learning rate of 0.01: <span class=\"mono-font\">m &larr; 0 + 0.187</span> and <span class=\"mono-font\">c &larr; 0 + 0.08</span>. The line has tilted slightly toward the data. Repeat a few hundred times and it lands on m = 2, c = 0.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Turn on <strong>Show Target OLS Fit</strong> so you can see where gradient descent should end up.</li>"
   "<li>Set the learning rate very small and step repeatedly &mdash; correct direction, painfully slow.</li>"
   "<li>Raise it steadily. There is a point where each step overshoots the minimum and lands further away than it started; the loss rises instead of falling.</li>"
   "<li>Set m and c by hand to something far from the answer and watch how the first few steps are large and later ones shrink &mdash; the gradient itself gets smaller as you approach.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Divergence from too high a learning rate</strong> is the classic failure, and its signature is unmistakable: the loss increases every step, often to infinity within a dozen iterations. If you see that, the fix is almost always &eta;, not the model.</p>"
   "<p><strong>Unscaled x values</strong> cause a subtler problem. If x is in the thousands, <span class=\"mono-font\">&part;L/&part;m</span> is thousands of times larger than <span class=\"mono-font\">&part;L/&part;c</span>, so a learning rate that suits one wrecks the other and the path zig-zags down a narrow valley.</p>"),
  ("In one line",
   "<p>Two parameters, the same optimiser as a deep network, and slow enough to watch every step.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/gradient_descent_batch_processing.html": {
 "intro": "Batch size decides how many examples the model looks at before it changes its mind. It is the quietest hyperparameter with the widest effect on how training feels.",
 "sections": [
  ("Three regimes",
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Batch size 1 (stochastic).</strong> One sample per update. Very noisy gradient, very many updates, and the noise itself sometimes helps escape bad regions.</li>"
   "<li><strong>Full batch.</strong> The whole dataset per update. The gradient is exact, but you get one update per epoch and it is slow.</li>"
   "<li><strong>Mini-batch (32&ndash;256).</strong> What essentially everyone uses. Enough samples for a usable gradient estimate, enough updates to make progress, and it fits on a GPU.</li>"
   "</ul>"),
  ("How the numbers work out",
   "<p>With 1,024 training samples:</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li>Batch size 32 &rarr; <strong>32 updates</strong> per epoch</li>"
   "<li>Batch size 256 &rarr; <strong>4 updates</strong> per epoch</li>"
   "</ul>"
   "<p>Gradient noise falls roughly with the square root of batch size. Going from 32 to 128 &mdash; a 4&times; increase &mdash; halves the noise, not quarters it. That diminishing return is why batch sizes stop growing well before memory runs out.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Drag <strong>Batch Size</strong> to its minimum. The descent path visibly jitters &mdash; each step is reacting to one or two samples.</li>"
   "<li>Raise it toward the maximum. The path straightens out, but notice it also takes fewer, larger steps to cover the same ground.</li>"
   "<li>Now hold batch size high and lower <strong>Learning Rate</strong>. Progress stalls &mdash; a big smooth gradient with a tiny step size wastes the smoothness.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Raising batch size without touching the learning rate.</strong> You get fewer updates per epoch, each no larger than before, so training slows down and people conclude the larger batch \"trains worse\". The usual remedy is the linear scaling rule: double the batch, double the learning rate, within reason.</p>"
   "<p><strong>Comparing runs by epoch count.</strong> An epoch at batch size 512 contains a fraction of the updates an epoch at batch size 32 does. Compare by number of updates, or by wall-clock time, not by epochs.</p>"),
  ("In one line",
   "<p>Batch size trades gradient noise against how many times per epoch you get to move.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/optimizers_in_neural_networks.html": {
 "intro": "Every optimiser here computes the same gradient. They differ entirely in how much they remember about the gradients that came before.",
 "sections": [
  ("What each one adds",
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>SGD</strong> &mdash; <span class=\"mono-font\">&theta; &larr; &theta; &minus; &eta;g</span>. No memory at all. Each step depends only on the current gradient.</li>"
   "<li><strong>Momentum</strong> &mdash; <span class=\"mono-font\">v &larr; &beta;v + g</span>, then <span class=\"mono-font\">&theta; &larr; &theta; &minus; &eta;v</span> with &beta; around 0.9. Builds up velocity in consistent directions and cancels out oscillation.</li>"
   "<li><strong>RMSprop</strong> &mdash; divides each parameter's step by a running root-mean-square of its recent gradients, so every parameter gets a step size suited to its own scale.</li>"
   "<li><strong>Adam</strong> &mdash; momentum and RMSprop together, plus a correction for the fact that both averages start at zero.</li>"
   "</ul>"),
  ("Why plain SGD zig-zags",
   "<p>Picture a long narrow valley where the gradient across the valley is 10 and along it is 0.1. With &eta; = 0.01, SGD steps 0.1 across and 0.001 along &mdash; a hundred to one. It bounces off the steep walls while creeping toward the actual minimum.</p>"
   "<p>Momentum fixes this by accumulation: the across-valley components alternate sign and cancel, while the along-valley components all point the same way and add up. RMSprop fixes it differently, by normalising both directions to roughly equal step sizes.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Select <strong>All (Compare)</strong> and run. Watch SGD (red) oscillate while Adam (green) takes a far more direct route.</li>"
   "<li>Raise <strong>Learning Rate</strong> gradually. There is a value where SGD diverges outright but the adaptive methods still converge.</li>"
   "<li>Now drop the learning rate very low and run again. SGD's path becomes clean &mdash; it was never the algorithm's fault, it was the step size.</li>"
   "<li>Use <strong>Sim Speed</strong> to slow it right down and watch Momentum overshoot the minimum and come back.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Carrying a learning rate between optimisers.</strong> A good SGD learning rate is often 0.01&ndash;0.1; Adam's usual default is 0.001. Swapping optimiser while keeping &eta; is one of the most common reasons a switch to Adam appears to make things worse.</p>"
   "<p><strong>Assuming Adam always wins.</strong> It usually converges fastest, but well-tuned SGD with momentum frequently generalises better on vision tasks, and a good deal of published work still uses it for exactly that reason. Fast to a worse minimum is not a win.</p>"),
  ("In one line",
   "<p>Same downhill direction, different memory &mdash; and memory is what stops you bouncing off the walls.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/optimizers_in_3d.html": {
 "intro": "A loss surface in three dimensions is the only version you can actually look at. The features that decide which optimiser wins &mdash; ravines, plateaus, saddle points &mdash; are all visible here.",
 "sections": [
  ("What the terrain is made of",
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Ravines</strong> &mdash; steep in one direction, nearly flat in another. Plain SGD ricochets between the walls.</li>"
   "<li><strong>Plateaus</strong> &mdash; large regions where the gradient is tiny. Progress crawls because there is almost nothing to follow.</li>"
   "<li><strong>Saddle points</strong> &mdash; the gradient is close to zero but you are not at a minimum: the surface curves up in some directions and down in others.</li>"
   "</ul>"),
  ("Saddles matter more than local minima",
   "<p>The folk explanation of training failure is \"it got stuck in a local minimum\". In high dimensions that is mostly wrong. For a point to be a local minimum, the surface must curve upward in <em>every</em> direction at once &mdash; and with millions of parameters that is vanishingly unlikely. Saddle points, where it curves up in some directions and down in others, are enormously more common.</p>"
   "<p>This is a practical difference. A local minimum is a trap. A saddle is not &mdash; there is a way down, and an optimiser with momentum carries enough velocity from earlier steps to keep moving across the flat region until it finds one.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Run <strong>SGD (Red)</strong> alone and watch it stall when it reaches a flat region &mdash; near-zero gradient means near-zero step.</li>"
   "<li>Switch to <strong>Momentum (Blue)</strong> from the same start. It coasts across the flat section on accumulated velocity.</li>"
   "<li>Select <strong>All (Compare)</strong> and note the arrival order, then change <strong>Learning Rate</strong> and see whether the order holds. It often does not.</li>"
   "<li>Slow <strong>Sim Speed</strong> right down at the moment each optimiser crosses the ridge &mdash; that is where the differences are widest.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Over-reading the picture.</strong> This surface has two parameters. A real network has millions, and its loss landscape has properties that genuinely do not exist in 3D. Use this to build intuition about momentum and adaptive step sizes; do not use it to conclude anything about how many minima a real network has.</p>"
   "<p><strong>Judging an optimiser from one starting point.</strong> Change where the run begins and the ranking often changes with it. A single trajectory is an anecdote.</p>"),
  ("In one line",
   "<p>The shape of the surface, not the cleverness of the algorithm, decides which optimiser looks good.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/neural_network.html": {
 "intro": "A neural network is one operation repeated: multiply by a matrix, add a bias, bend the result. Depth is just how many times you do it.",
 "sections": [
  ("One layer, written out",
   "<p>Each layer takes the previous layer's output and applies</p>"
   "<p class=\"mono-font\">a<sup>(l)</sup> = f(W<sup>(l)</sup> a<sup>(l&minus;1)</sup> + b<sup>(l)</sup>)</p>"
   "<p>where W is a weight matrix, b is a bias vector, and f is the activation. Stack these and the network can represent increasingly complex functions &mdash; but only because f is non-linear. Remove it and the whole stack collapses into a single matrix.</p>"),
  ("Counting the parameters",
   "<p>Take 4 input features &rarr; one hidden layer of 8 &rarr; 3 output classes.</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li>Input to hidden: <span class=\"mono-font\">4 &times; 8 = 32</span> weights, plus 8 biases = <strong>40</strong></li>"
   "<li>Hidden to output: <span class=\"mono-font\">8 &times; 3 = 24</span> weights, plus 3 biases = <strong>27</strong></li>"
   "<li>Total: <strong>67 learnable parameters</strong></li>"
   "</ul>"
   "<p>Add a second hidden layer of 8 and you insert another <span class=\"mono-font\">8 &times; 8 + 8 = 72</span> &mdash; more than doubling the model. Parameter count grows with the <em>product</em> of adjacent layer widths, which is why wide layers next to each other get expensive fast.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Set <strong>Input Features</strong> to 4, one <strong>Hidden Layer</strong> of 8, and <strong>Output Classes</strong> to 3, then count the connections against the arithmetic above.</li>"
   "<li>Add a second hidden layer and watch the connection count jump rather than creep.</li>"
   "<li>Widen one hidden layer and note that the layers on <em>both</em> sides of it grow, because it participates in two weight matrices.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Depth without non-linearity.</strong> Stacking linear layers gains you nothing at all mathematically &mdash; it is the single most common misunderstanding about why deep networks work.</p>"
   "<p><strong>A first hidden layer far wider than the input.</strong> Four inputs into a 512-unit layer adds thousands of parameters without adding any information; there were only ever four numbers to work with. Width is worth adding where there is signal to spread out, not at the front by default.</p>"),
  ("In one line",
   "<p>Multiply, add a bias, bend &mdash; repeated, with the bend being the part that matters.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/neural_network_for_regression.html": {
 "intro": "A regression network is a classifier with two changes: nothing squashes the output, and the loss measures distance instead of disagreement.",
 "sections": [
  ("The two differences that matter",
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Linear output layer.</strong> No sigmoid, no softmax. The final neuron emits whatever value it computes, so the network can predict 3.7, &minus;120 or 275,000.</li>"
   "<li><strong>Distance-based loss.</strong> Mean squared error, or mean absolute error when outliers should not dominate.</li>"
   "</ul>"
   "<p>Everything else &mdash; hidden layers, ReLU, backpropagation, the optimiser &mdash; is unchanged from a classifier.</p>"),
  ("A concrete architecture",
   "<p>Predicting house price from three features: 3 inputs &rarr; 16 hidden with ReLU &rarr; 1 linear output. That is <span class=\"mono-font\">(3&times;16 + 16) + (16&times;1 + 1) = 81</span> parameters.</p>"
   "<p>The output neuron is where regression and classification part ways. Leave a sigmoid on it and the largest value the network can ever predict is 1.0 &mdash; every house is priced somewhere between nothing and one. It is a surprisingly easy mistake to make when adapting a classifier.</p>"
   "<p>Use several output neurons when you have several continuous targets: predicting an (x, y, z) position is three linear outputs and one shared body.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Set <strong>Output Neurons</strong> to 1. That is the standard single-target regression head.</li>"
   "<li>Change it to 3 &mdash; multi-target regression, where one network predicts several related numbers from shared hidden features.</li>"
   "<li>Vary <strong>Hidden Layers</strong> and note the output layer's shape never changes. The head is decided by the task, not the depth.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>A squashing activation left on the output.</strong> Caps the prediction range and flattens the gradient for any target outside it, so the model cannot learn its way out.</p>"
   "<p><strong>Unscaled targets.</strong> Squared error on values near 300,000 produces gradients around 10<sup>11</sup>. The first update destroys the weights and the loss becomes NaN. Standardise the target and invert the scaling afterwards.</p>"
   "<p><strong>Reporting accuracy.</strong> There is no such thing for continuous output. Report MAE or RMSE in the target's own units, so \"off by £18,000 on average\" is something a reader can actually judge.</p>"),
  ("In one line",
   "<p>Classifier body, linear head, distance-based loss &mdash; and scale your targets.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/neural_network_for_unsupervised_learning.html": {
 "intro": "With no labels to learn from, you make the input its own target. Squeeze it through a narrow layer and the network has to work out what was worth keeping.",
 "sections": [
  ("The autoencoder trick",
   "<p>An autoencoder is trained to reproduce its own input. On its own that is trivial &mdash; copy the input to the output and the loss is zero. The trick is the bottleneck: a hidden layer narrower than the input, which the data must pass through.</p>"
   "<p>Because the bottleneck cannot carry everything, the network is forced to decide what matters. What survives the squeeze is a learned, compressed representation, and it is learned without a single label.</p>"),
  ("A worked shape",
   "<p>8 input features &rarr; 3-unit bottleneck &rarr; 8 reconstruction outputs. The encoder must express 8 numbers using 3, and the decoder must rebuild all 8 from those 3.</p>"
   "<p>If those 8 features are genuinely independent, the reconstruction will be poor &mdash; there is nothing to compress. If several are correlated, as real features usually are, the network finds those relationships and reconstruction gets surprisingly close. The loss is simply <span class=\"mono-font\">MSE(input, reconstruction)</span>.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Set <strong>Input Features</strong> to 8 and squeeze the hidden layer to 2. A hard compression &mdash; only the strongest structure survives.</li>"
   "<li>Widen the hidden layer until it matches the input width. Reconstruction becomes near-perfect and completely uninformative: the network has learned to copy.</li>"
   "<li>Check that <strong>Reconstruction Output</strong> always matches <strong>Input Features</strong>. It must &mdash; the output is being compared against the input.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>A bottleneck as wide as the input.</strong> The network learns the identity function, the loss looks excellent, and you have learned nothing about the data. If reconstruction is perfect, suspect this first.</p>"
   "<p><strong>Reading reconstruction loss as quality.</strong> Low loss only means the input was reproducible, which says nothing about whether the compressed representation is useful for anything else. Judge it by how well the bottleneck features perform on a downstream task.</p>"),
  ("In one line",
   "<p>No labels needed &mdash; make the input the target and let a narrow layer decide what was worth keeping.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/model_training_curve.html": {
 "intro": "Two lines tell you almost everything about a training run. Learning to read the gap between them is the fastest diagnostic skill in machine learning.",
 "sections": [
  ("The four shapes",
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Both high and flat</strong> &mdash; underfitting. The model has not got enough capacity, or has not trained long enough, to capture the pattern.</li>"
   "<li><strong>Both falling and close together</strong> &mdash; healthy. Keep going.</li>"
   "<li><strong>Training falling, validation turning upward</strong> &mdash; overfitting. The turning point is where you should have stopped.</li>"
   "<li><strong>Validation below training</strong> &mdash; usually not a miracle. Dropout is active during training but not evaluation, or the validation split happens to be easier.</li>"
   "</ul>"),
  ("Reading real numbers",
   "<p>Training loss 0.08, validation loss 0.34. The gap of 0.26 is the model's memorisation of the training set &mdash; that is overfitting, no matter how good 0.08 looks in isolation.</p>"
   "<p>Training loss 0.31, validation loss 0.33. A tiny gap, but both are high. The model is not overfitting; it simply is not good enough yet. These two situations need opposite responses, which is exactly why looking at one curve is not enough.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Set <strong>Model Complexity</strong> low and <strong>Data Noise</strong> low. Both curves flatten out high &mdash; the underfitting signature.</li>"
   "<li>Raise <strong>Model Complexity</strong> and let it run the full <strong>Total Epochs</strong>. Find the epoch where validation stops falling and starts to climb.</li>"
   "<li>Raise <strong>Data Noise</strong> and repeat. The turning point arrives earlier, because there is more noise available to memorise.</li>"
   "<li>Set <strong>Learning Rate</strong> too high and watch both curves become jagged rather than smooth.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Judging on training loss alone.</strong> It almost always keeps falling. A model can drive training loss to nearly zero while getting steadily worse at its actual job.</p>"
   "<p><strong>Training for a fixed epoch count.</strong> The right number is wherever validation loss bottoms out, and that moves with every change to the data, the model or the learning rate.</p>"
   "<p><strong>Reading noise as trend.</strong> With a small validation set, a wobble of a couple of percent between epochs is sampling noise. Wait for a sustained rise before concluding anything.</p>"),
  ("In one line",
   "<p>The gap between the curves is the diagnosis; either curve alone is not.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/overfitting_vs_underfitting.html": {
 "intro": "Both failures look like poor performance and need opposite fixes. Telling them apart is a question of whether the model can even represent the pattern, or whether it has memorised the noise around it.",
 "sections": [
  ("A concrete demonstration",
   "<p>Fit ten data points that follow a gentle curve with a little noise on top.</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Degree 1</strong> (a straight line) cannot bend at all. It misses the shape everywhere &mdash; high error on training data <em>and</em> new data. Underfitting.</li>"
   "<li><strong>Degree 9</strong> through ten points passes exactly through every one. Training error is zero, and between the points the curve swings wildly to values the real pattern never produces. Overfitting.</li>"
   "<li><strong>Degree 3</strong> follows the trend and ignores the jitter. Slightly worse on the training set than degree 9, considerably better on anything new.</li>"
   "</ul>"
   "<p>The degree-9 model is not \"more accurate\". It has memorised the noise, and noise does not repeat.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Set <strong>Model Complexity</strong> to its minimum. The fitted curve cannot follow the data no matter how many <strong>Target Epochs</strong> you allow &mdash; more training will never fix underfitting.</li>"
   "<li>Push complexity to maximum and watch the curve thread every single point, including the ones that are clearly noise.</li>"
   "<li>Now raise <strong>Data Noise</strong> and repeat both. The high-complexity model gets dramatically worse; the low-complexity one barely changes, because it was never paying attention to the noise.</li>"
   "<li>Use <strong>Sim Speed</strong> to slow the fit and watch the moment the curve starts chasing individual points.</li>"
   "</ol>"),
  ("Which lever to pull",
   "<p>They need opposite treatment, which is why diagnosing correctly matters more than any individual fix.</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Underfitting</strong> &mdash; more capacity, better features, train longer, reduce regularisation.</li>"
   "<li><strong>Overfitting</strong> &mdash; more data, less capacity, more regularisation (dropout, weight decay), early stopping.</li>"
   "</ul>"),
  ("What usually goes wrong",
   "<p><strong>Treating overfitting by training less.</strong> Early stopping helps, but if a model overfits after two epochs the real problem is capacity against data volume, not epoch count.</p>"
   "<p><strong>Adding data to fix underfitting.</strong> More data does not help a model that lacks the capacity to represent the pattern in the first place. It is the standard remedy for overfitting and close to useless for the opposite.</p>"),
  ("In one line",
   "<p>Too little capacity misses the signal; too much memorises the noise &mdash; and the cures point in opposite directions.</p>"),
 ]},

# ---------------------------------------------------------------------------
"deep_learning/learning_rate_scheduling.html": {
 "intro": "A single fixed learning rate has to be two things at once: big enough to cross the landscape early, small enough to settle at the end. A schedule lets it be both in turn.",
 "sections": [
  ("Why one value cannot serve both phases",
   "<p>Early in training you are far from any good solution and want large steps. Late in training you are close, and large steps make you bounce around the minimum without ever landing in it. A fixed rate forces a compromise that is wrong at both ends.</p>"
   "<p>The common schedules:</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>Step decay</strong> &mdash; multiply by 0.1 every k epochs. Blunt, predictable, still widely used.</li>"
   "<li><strong>Exponential</strong> &mdash; <span class=\"mono-font\">&eta; = &eta;<sub>0</sub> e<sup>&minus;kt</sup></span>, smooth throughout.</li>"
   "<li><strong>Cosine annealing</strong> &mdash; a smooth curve down to nearly zero, currently the most common default.</li>"
   "</ul>"),
  ("Step decay, concretely",
   "<p>Start at <span class=\"mono-font\">&eta;<sub>0</sub> = 0.1</span> and multiply by 0.1 every 30 epochs:</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li>Epochs 0&ndash;29: <span class=\"mono-font\">&eta; = 0.1</span> &mdash; covering ground fast</li>"
   "<li>Epochs 30&ndash;59: <span class=\"mono-font\">&eta; = 0.01</span> &mdash; refining</li>"
   "<li>Epochs 60+: <span class=\"mono-font\">&eta; = 0.001</span> &mdash; settling</li>"
   "</ul>"
   "<p>The characteristic sign that it is working is a visible drop in loss immediately after each decay step: the model had been oscillating around a minimum it could not land in, and a smaller step lets it descend the rest of the way.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Set <strong>Initial LR</strong> high and run to the full <strong>Target Epochs</strong>. The fixed run makes rapid early progress then hovers, never quite settling.</li>"
   "<li>Compare against the scheduled run from the same start &mdash; same early progress, but it converges instead of hovering.</li>"
   "<li>Now set Initial LR very low. The schedule barely helps, because you never had steps large enough to need shrinking.</li>"
   "<li>Raise <strong>Complexity (Degree)</strong> and watch how a harder fitting problem makes the difference between the two more pronounced.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Decaying too early.</strong> Shrink the step before the model has reached a good region and it will crawl the rest of the way, converging neatly to somewhere mediocre.</p>"
   "<p><strong>Scheduling on epochs when the real unit is updates.</strong> Change the batch size and an epoch contains a different number of steps, so a schedule tuned at one batch size silently becomes a different schedule at another.</p>"
   "<p><strong>Tuning the schedule before the initial rate.</strong> The starting value matters more than the decay shape. Find a good &eta;<sub>0</sub> first, then decide how it should come down.</p>"),
  ("In one line",
   "<p>Big steps to travel, small steps to arrive &mdash; and get the starting size right before tuning the decay.</p>"),
 ]},

# ---------------------------------------------------------------------------
"maths/equation_of_line.html": {
 "intro": "Every straight line is two numbers: how steeply it climbs, and where it crosses the vertical axis. Fitting a line to data, and a neuron's decision boundary, are both this equation wearing different vocabulary.",
 "sections": [
  ("The two numbers",
   "<p class=\"mono-font\">y = mx + c</p>"
   "<ul class=\"list-disc pl-5 space-y-2\">"
   "<li><strong>m is the slope</strong> &mdash; how much y changes for every 1 you move along x. Positive climbs left to right, negative falls, zero is flat.</li>"
   "<li><strong>c is the y-intercept</strong> &mdash; the value of y when x is 0, which is exactly where the line crosses the vertical axis.</li>"
   "</ul>"
   "<p>Slope is rise over run: take any two points on the line and divide the change in y by the change in x. Any two points give the same answer, which is what makes it a straight line.</p>"),
  ("Finding a line through two points",
   "<p>Given (1, 5) and (3, 11):</p>"
   "<p class=\"mono-font\">m = (11 &minus; 5) / (3 &minus; 1) = 6 / 2 = 3</p>"
   "<p>Now substitute either point back in to find c. Using (1, 5):</p>"
   "<p class=\"mono-font\">5 = 3(1) + c &nbsp;&rarr;&nbsp; c = 2</p>"
   "<p>So the line is <span class=\"mono-font\">y = 3x + 2</span>. Check it against the other point: 3(3) + 2 = 11. Correct.</p>"),
  ("Why this shows up everywhere later",
   "<p>Linear regression fits exactly this equation &mdash; it searches for the m and c that put the line closest to a cloud of points.</p>"
   "<p>A single neuron computes <span class=\"mono-font\">z = wx + b</span>. That is the same equation: the weight <em>is</em> the slope and the bias <em>is</em> the intercept. When you read that a bias &quot;shifts the decision boundary&quot;, this is the shift being described.</p>"
   "<p>In three dimensions the same idea becomes a plane, <span class=\"mono-font\">z = m<sub>1</sub>x + m<sub>2</sub>y + c</span>, and beyond that a hyperplane. The intuition does not change; only the number of slopes does.</p>"),
  ("Try this above",
   "<ol class=\"list-decimal pl-5 space-y-2\">"
   "<li>Press <strong>Horizontal</strong>. The slope is 0, so y never changes no matter how far along x you travel.</li>"
   "<li>Press <strong>Negative</strong> and watch the line fall left to right &mdash; the sign of m is direction, not size.</li>"
   "<li>Press <strong>Fractional</strong> for a slope between 0 and 1: a gentle climb rather than a steep one.</li>"
   "<li>Change <strong>c</strong> on its own and watch the line slide vertically without ever tilting.</li>"
   "<li>Switch to <strong>3D Space</strong> and add a second slope. The line becomes a plane, and there are now two directions to climb in.</li>"
   "</ol>"),
  ("What usually goes wrong",
   "<p><strong>Confusing sign with steepness.</strong> A slope of &minus;5 is steeper than a slope of 2. The minus sign only says which way it leans.</p>"
   "<p><strong>Expecting every line to fit this form.</strong> A vertical line has an undefined slope &mdash; x never changes, so the run is zero and you would be dividing by it. Vertical lines are written <span class=\"mono-font\">x = k</span> instead, which is why regression cannot fit perfectly vertical relationships.</p>"),
  ("In one line",
   "<p>m tilts, c slides &mdash; and a neuron\u2019s weight and bias are the same two numbers under different names.</p>"),
 ]},
}
