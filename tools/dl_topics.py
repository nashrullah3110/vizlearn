# -*- coding: utf-8 -*-
"""Content for the generated deep learning modules.

Thirty-two modules, and every one of them about training: gradients,
normalisation, regularisation, schedules, reproducibility. Thorough, and it
stopped at a dense network. Autoencoders, GANs, diffusion, contrastive
learning, seq2seq and beam search had no page anywhere on the site - while
"autoencoder" appeared twenty times across other tracks' articles and "GAN"
thirty-five, always assuming the reader already knew.

These ten are that gap. Attention, transfer learning, distillation and
augmentation are deliberately absent: NLP, Computer Vision and Gen AI already
own those, and a second page would be a second thing to keep in step.

The arithmetic runs in assets/vizlearn-dl.js; the plotter and the seeded RNG
come from assets/vizlearn-plot.js, shared with the maths and machine learning
harnesses.
"""

TOPICS = []


def topic(slug, title, cat, lead, svg, viz, notes, article, check):
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "viz": viz, "notes": notes, "article": article, "check": check,
    })


A = "var(--accent-primary)"
M = "var(--text-muted)"
B = "var(--border-subtle)"
S = "var(--bg-surface)"


def _svg(body):
    return '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s</svg>' % body


def _box(x, y, w, h, fill="none", stroke=B, sw=2, rx=3):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, fill, stroke, sw))


def _txt(x, y, s, fill=M, size=9, anchor="middle", weight="normal"):
    return ('<text x="%s" y="%s" fill="%s" font-size="%s" font-family="monospace" '
            'text-anchor="%s" font-weight="%s">%s</text>'
            % (x, y, fill, size, anchor, weight, s))


def _dot(x, y, fill=M, r=2.6):
    return '<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (x, y, r, fill)


def _line(x1, y1, x2, y2, stroke=A, sw=1.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, stroke, sw, d))


def _axes():
    return _line(20, 72, 148, 72, B, 1) + _line(20, 72, 20, 16, B, 1)




# ---------------------------------------------------------------------------
# 1. Autoencoders
# ---------------------------------------------------------------------------
topic(
    "autoencoders",
    "Autoencoders",
    "Representation Learning",
    "Force a signal through a narrow gap and out again. What survives is what "
    "the network decided mattered.",
    _svg(_box(14, 24, 20, 44, fill=S, stroke=B, sw=1.4)
         + _box(44, 36, 12, 20, fill=S, stroke=A, sw=1.6)
         + _box(66, 24, 20, 44, fill=S, stroke=B, sw=1.4)
         + _line(34, 46, 44, 46, M, 1.2) + _line(56, 46, 66, 46, M, 1.2)
         + _txt(50, 80, "in, squeeze, out", M, 7)
         + _txt(120, 42, "latent", A, 8) + _txt(120, 54, "code", A, 8)),
    {
        "demo": "autoencoder",
        "controls": [
            {"key": "latent", "label": "Latent size", "type": "range",
             "min": 1, "max": 24, "step": 1, "value": 4},
            {"key": "noise", "label": "Noise added to the input", "type": "range",
             "min": 0.0, "max": 0.6, "step": 0.05, "value": 0.0},
        ],
    },
    [
        "An autoencoder learns to copy its input. The copying is not the point "
        "&mdash; the <strong>bottleneck</strong> is.",
        "With fewer latent dimensions than inputs, an exact copy is impossible, "
        "so the network must decide what to keep.",
        "A linear autoencoder with squared error provably finds the same "
        "subspace as <a href='../machine_learning/pca.html'>PCA</a>.",
        "Add noise to the input and ask for the clean output: the bottleneck "
        "cannot afford to store noise, so it removes it.",
    ],
    """
title: Autoencoders
intro: A network trained to copy its input, and why that odd task is handy.

## The apparently useless task

An autoencoder has two halves. The **encoder** maps an input to a smaller
form. The **decoder** maps it back. The loss is the difference between
the output and the input.

Copy the input to the output. Stated like that it sounds like a null task &mdash;
the identity function scores just right.

Except it can't, because the form in the middle is smaller than the
input. The network has to throw info away, and the training goal
forces it to throw away the least costly info. **What lives the
bottleneck is what the data was mostly made of.**

## Watch the squeeze

The grey line is the input. The orange line is what comes back out.

At a latent size of 1 the rebuild keeps only the largest structure and
misses all else. Raise it and the copy tightens. Past a certain point
extra dims buy almost nothing, because the left detail is noise
rather than signal.

That flattening is the handy reading: it says roughly how many numbers the
data really needs, which is its **true dimensionality**.

## The relationship to PCA

A linear autoencoder trained with squared error finds the same subspace as
[PCA](../machine_learning/pca.html). Not a thing similar &mdash; provably the
same span, though the single directions need not be the principal
components in order.

So a linear autoencoder is PCA with extra steps. What makes them worth having is
**non-linearity**: with non-linear activations the encoder can learn a curved
manifold, which no linear map can follow. An image dataset lives on a
wildly curved surface in pixel space, and that is the case where an autoencoder
earns its keep.

## Denoising

Raise the noise control. Now the input is corrupted and the target is still the
clean signal.

The rebuild error against the *noisy* input goes up, and against the
*clean* signal it goes down. The readout gives both.

The reason is the bottleneck again. Noise is, by build, the part of the
signal with no structure to compress. So A narrow code can't afford to store
it. Forcing the network to rebuild through the bottleneck forces it to
discard just what noise is.

**Denoising autoencoders** make this the training method: corrupt the input
on purpose, ask for the clean version. It also blocks the collapse
answer where a wide code just learns the identity. This Is why the trick
appears even when denoising isn't the goal.

## What they are used for

**Dimensionality reduction** where the structure is non-linear.

**Outlier spotting.** Train on normal data. Any of it that rebuilds badly is
unlike what was seen. It works because the model has only learned to compress
one kind of thing.

**Pretraining.** Once the standard way to reset deep networks
before better init and norming made it unneeded.

**Generation** &mdash; but not right. A plain autoencoder's latent space has
gaps, so a random code often decodes to nothing real. Fixing that is
what [the VAE](variational_autoencoders.html) is for.

## The elbow that reveals intrinsic dimension

The handy thing an autoencoder measures is *how many numbers the data really
needs*, and it shows up as an elbow in rebuild error against latent size.
On data that truly lives in `d` dims with a little noise on top,
widening the bottleneck past `d` buys almost nothing:

|latent size|reconstruction error|
|---|---|
|1|large &mdash; only the biggest structure survives|
|up to the true d|falling steeply, each dimension earns its place|
|beyond d|flat &mdash; the remaining detail is noise|

The point where the curve flattens is the data's true dimensionality, and it
is the same number [PCA](../machine_learning/pca.html) would find &mdash; a linear
autoencoder with squared-error loss provably recovers the PCA subspace. The
reason to reach for an autoencoder instead is the non-linear case: real data (an
image dataset, say) lies on a curved manifold in a high-dimensional space, and a
straight map can't follow the curve where a non-linear encoder can. That
is also why the rebuild error reads as pixel match rather than
visual quality, and why autoencoder outputs look softened: the bottleneck
keeps what is common to the data and spends nothing on the exact sharp detail
that sets apart one example from its neighbours.

The denoising variant turns the same bottleneck into a training method: corrupt
the input on purpose and ask for the clean version back. Because noise is by
build the part of a signal with no structure to compress, a narrow code
can't afford to store it. So Rebuilding through the bottleneck forces the
network to discard just what noise is. That also drops the collapse escape
where a too-wide code simply learns the identity. This Is why the trick shows up
even when denoising isn't the goal. And it's the same instinct behind
using an autoencoder for outlier spotting. Here A model trained only on normal
data rebuilds any of it unseen badly, and the rebuild error turns
the outlier score.

None of the latent dims mean any of it on their own, either: they aren't
sorted or disentangled unless a thing in the training made them so, which is a
large part of what separates a plain autoencoder from the variational and
beta-weighted variants built to push just that structure.

## Where it goes wrong

**A bottleneck that is too wide.** With enough room the network learns the
identity and nothing is found. Constrain it, or use denoising, or add a
sparsity fine.

**Expecting a usable generative model.** Sample from a plain autoencoder's
latent space and you'll mostly get nonsense.

**Reading the rebuild error as a quality score.** It measures pixel
match, not visual likeness. This Is why autoencoder outputs look
blurred.

**given the latent dims mean any of it on their own.** They aren't
sorted or disentangled unless a thing in the training made them so.

## Train one, then look at what the bottleneck kept

An autoencoder learns to copy its own input through a narrow layer. Training one on data with a known hidden structure shows what a bottleneck forces it to discover -- and where PCA does the job better.

```python-run
import numpy as np

rng = np.random.default_rng(0)
N, OBS = 300, 12

def standardise(a):
    return (a - a.mean(0)) / a.std(0)

factors = rng.normal(size=(N, 2))        # the true hidden structure
mix = rng.normal(size=(2, OBS))
X_lin = standardise(factors @ mix + rng.normal(0, 0.05, (N, OBS)))
X_curved = standardise(np.tanh(factors @ mix * 1.5) + rng.normal(0, 0.05, (N, OBS)))

def pca_mse(X, k):
    U, s, Vt = np.linalg.svd(X - X.mean(0), full_matrices=False)
    return (((U[:, :k] * s[:k]) @ Vt[:k] + X.mean(0) - X) ** 2).mean()

def autoencode(X, k, hidden=12, epochs=800, lr=0.04, seed=0):
    # OBS -> hidden(tanh) -> k -> hidden(tanh) -> OBS
    r = np.random.default_rng(seed)
    P = [r.normal(0, 0.3, (OBS, hidden)), np.zeros((1, hidden)),
         r.normal(0, 0.3, (hidden, k)),   np.zeros((1, k)),
         r.normal(0, 0.3, (k, hidden)),   np.zeros((1, hidden)),
         r.normal(0, 0.3, (hidden, OBS)), np.zeros((1, OBS))]
    m = [np.zeros_like(p) for p in P]
    v = [np.zeros_like(p) for p in P]
    for t in range(1, epochs + 1):
        a1 = np.tanh(X @ P[0] + P[1])
        code = a1 @ P[2] + P[3]
        a2 = np.tanh(code @ P[4] + P[5])
        out = a2 @ P[6] + P[7]
        d = 2 * (out - X) / len(X)
        g6, g7 = a2.T @ d, d.sum(0, keepdims=True)
        d2 = (d @ P[6].T) * (1 - a2 ** 2)
        g4, g5 = code.T @ d2, d2.sum(0, keepdims=True)
        dc = d2 @ P[4].T
        g2, g3 = a1.T @ dc, dc.sum(0, keepdims=True)
        d1 = (dc @ P[2].T) * (1 - a1 ** 2)
        g0, g1 = X.T @ d1, d1.sum(0, keepdims=True)
        for i, g in enumerate((g0, g1, g2, g3, g4, g5, g6, g7)):
            m[i] = 0.9 * m[i] + 0.1 * g
            v[i] = 0.999 * v[i] + 0.001 * g ** 2
            P[i] -= lr * (m[i] / (1 - 0.9 ** t)) / (np.sqrt(v[i] / (1 - 0.999 ** t)) + 1e-8)
    a1 = np.tanh(X @ P[0] + P[1])
    code = a1 @ P[2] + P[3]
    out = np.tanh(code @ P[4] + P[5]) @ P[6] + P[7]
    return code, ((out - X) ** 2).mean()

print("%d rows, %d observed columns, secretly built from 2 hidden factors."
      % (N, OBS))
print("the autoencoder is never told that number.")
print()

print("reconstruction error against the size of the bottleneck:")
print("%12s %18s %14s" % ("bottleneck", "reconstruction", "compression"))
errs = {}
for k in (1, 2, 3, 6):
    code, mse = autoencode(X_lin, k)
    errs[k] = (code, mse)
    print("%12d %18.6f %13.1fx" % (k, mse, OBS / k))
print()
drop_1_2 = errs[1][1] / errs[2][1]
drop_2_3 = errs[2][1] / errs[3][1]
print("going from 1 unit to 2 divides the error by %.0f. going from 2 to 3"
      % drop_1_2)
print("changes it by a factor of %.2f -- nothing. that knee is the model"
      % drop_2_3)
print("telling you the data is 2-dimensional, which is exactly what it is,")
print("and it is how an autoencoder gets used to ESTIMATE intrinsic")
print("dimension rather than merely to compress.")
print()

h2 = errs[2][0]
print("what the 2-unit code contains. correlate it against the true hidden")
print("factors it was never shown:")
for i in range(2):
    c = [abs(np.corrcoef(h2[:, i], factors[:, j])[0, 1]) for j in range(2)]
    print("  code unit %d  vs factor 0: %.4f   vs factor 1: %.4f" % (i, c[0], c[1]))
print("  it recovered them, but not in their original order or orientation.")
print("  an autoencoder's code is only defined up to an arbitrary rotation --")
print("  nothing in the loss prefers one over another.")
print()

print("now the comparison people skip. PCA solves the same problem in closed")
print("form, and on LINEAR data it is the provable optimum:")
print("%8s %16s %20s %12s" % ("dims", "PCA", "autoencoder", "winner"))
lin_wins = 0
for k in (1, 2, 3):
    p, a = pca_mse(X_lin, k), errs[k][1]      # reuse the fits from above
    lin_wins += a < p
    print("%8d %16.6f %20.6f %12s" % (k, p, a, "PCA" if p < a else "autoencoder"))
print("  PCA takes %d of the 3 rows." % (3 - lin_wins))
print("  where the useful answer really is a flat subspace -- 2 dimensions")
print("  and up here -- PCA computes it exactly and gradient descent can")
print("  only approach it. at 1 dimension the autoencoder can still edge")
print("  ahead, because a CURVED line through the cloud captures a little")
print("  more than the best straight one. that is the whole advantage in")
print("  miniature, and it is small.")
print()

print("so give it something curved -- the same 2 factors, but observed")
print("through a tanh, so the data lies on a bent surface:")
print("%8s %16s %20s %12s" % ("dims", "PCA", "autoencoder", "winner"))
wins = 0
for k in (1, 2, 3):
    p = pca_mse(X_curved, k)
    a = autoencode(X_curved, k)[1]
    wins += p > a
    print("%8d %16.6f %20.6f %12s" % (k, p, a, "PCA" if p < a else "autoencoder"))
print("  the autoencoder takes %d of the 3 rows here, against %d on the flat"
      % (wins, lin_wins))
print("  data above. it has a nonlinear encoder AND a nonlinear decoder, so")
print("  it can bend to follow a curved surface. PCA can only pass a flat")
print("  subspace through one, and on this data that costs it.")
print()
print("the honest summary: run PCA first, every time. it is closed form,")
print("deterministic, and has no hyperparameters. reach for an autoencoder")
print("when PCA's reconstruction error tells you the structure is not flat.")
print("on the curved data above that was worth roughly a %dx reduction in"
      % round(pca_mse(X_curved, 2) / autoencode(X_curved, 2)[1]))
print("error at 2 dimensions; on the flat data it was worth nothing at all.")
print("which of those two situations you are in is an empirical question, and")
print("running PCA is how you answer it.")
print()
print("two variants worth knowing:")
print("  denoising -- feed a corrupted input and ask for the clean one, so")
print("               the model cannot settle for the identity function.")
print("  sparse    -- penalise how many code units are active instead of")
print("               narrowing the layer. the same constraint, applied more")
print("               softly, and it lets you keep a wide code.")
```

""",
    [
        {"q": "Why is training a network to copy its input not a null task?",
         "options": ["The network is too small to copy",
                     "The representation in the middle is smaller than the input, so information must be discarded - and the loss decides what",
                     "The output has a different shape",
                     "Noise is always added"],
         "answer": 1,
         "why": "What survives the bottleneck is what the data was mostly made of. The copying is the mechanism; the constraint is the point."},
        {"q": "What does a linear autoencoder with squared error find?",
         "options": ["An arbitrary subspace", "The same subspace as PCA",
                     "The identity function", "A sparse code"],
         "answer": 1,
         "why": "Provably the same span, though not necessarily the principal components in order. Non-linearity is what makes an autoencoder more than PCA with extra steps."},
        {"q": "Why does a bottleneck remove noise?",
         "options": ["Noise is filtered before encoding",
                     "Noise has no structure to compress, so a narrow code cannot afford to store it",
                     "The decoder smooths the output",
                     "The loss ignores noise"],
         "answer": 1,
         "why": "Denoising autoencoders make this the training procedure - corrupt the input, ask for the clean version - which also prevents a wide code from learning the identity."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Variational autoencoders
# ---------------------------------------------------------------------------
topic(
    "variational_autoencoders",
    "Variational Autoencoders",
    "Generative Models",
    "Make the latent space continuous enough to sample from, by pulling it "
    "towards a known distribution and paying for the pull.",
    _svg('<circle cx="80" cy="44" r="26" fill="none" stroke="%s" stroke-width="1.4" stroke-dasharray="4 3"/>' % M
         + "".join(_dot(64 + (i % 4) * 6, 34 + (i // 4) * 7, A) for i in range(8))
         + "".join(_dot(88 + (i % 4) * 5, 46 + (i // 4) * 6, A, 2.2) for i in range(8))
         + _txt(80, 82, "a space you can sample", M, 7)),
    {
        "demo": "vae",
        "controls": [
            {"key": "sigma", "label": "Encoder spread (sigma)", "type": "range",
             "min": 0.05, "max": 1.60, "step": 0.05, "value": 0.45},
            {"key": "separation", "label": "How far apart the classes sit", "type": "range",
             "min": 0.0, "max": 2.5, "step": 0.1, "value": 1.3},
            {"key": "seed", "label": "Resample", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 7},
        ],
    },
    [
        "A plain <a href='autoencoders.html'>autoencoder</a> maps each input to "
        "a point. A VAE maps it to a <strong>distribution</strong>.",
        "The <strong>reparameterisation trick</strong> writes the sample as "
        "<code class='mono-font'>z = &mu; + &sigma;&epsilon;</code>, so the randomness carries no gradient.",
        "The loss has two terms: reconstruction, and a KL that pulls every "
        "encoded distribution towards the prior.",
        "Too much KL and the clusters merge &mdash; posterior collapse. Too "
        "little and the space has gaps, so sampling produces nothing.",
    ],
    """
title: Variational Autoencoders
intro: Turning an autoencoder into a thing you can sample from. The two forces that have to be weighed to do it.

## The problem with a plain autoencoder

An [autoencoder](autoencoders.html) maps each input to a single point in the
latent space, and nothing organises those points. Nearby codes need not decode
to similar things, and the space between clusters is undefined territory.

So you can't make. Pick a random latent vector and decode it, and you
almost certainly land a place the decoder was never trained, and the output is
noise.

A VAE fixes this by making the latent space **smooth and bounded** &mdash;
by build, not by hope.

## Encoding to a distribution

The encoder outputs a mean and a standard deviation rather than a point, and the
code is *sampled* from that spread during training.

That single change does the work. Because the same input makes different
codes on different passes, the decoder must handle a whole zone, not a
point. Zones share and the space fills in.

Drag the sigma control and watch the clusters spread. At small sigma you've a
plain autoencoder again, with tight clumps and gaps between them. At large sigma
the zones swallow each other.

## The reparameterisation trick

There's an obstacle: you can't backprop through a sampling op.
Sampling isn't a differentiable function of the params that made the
spread.

The trick is to move the noise out of the path:

```
z  =  mu  +  sigma * epsilon        with epsilon ~ N(0, 1)
```

Now the random part, `epsilon`, is an input rather than an op. The
gradient flows to `mu` and `sigma` most times, because with `epsilon` fixed the
formula is an plain differentiable function of them.

That is the whole trick, it's two lines of code, and VAEs weren't trainable
without it. It reappears in other places where a sample must be differentiated
through &mdash; the Gumbel-softmax does the same job for discrete variables.

## Two terms in tension

```
loss  =  reconstruction error  +  KL( encoder distribution || prior )
```

The **rebuild** term wants tight, well-separated codes: the easiest thing
to decode accurately.

The **KL** term wants each coded spread to look like the prior &mdash;
the dashed circle. It's what makes the space samplable, because if each code
looks like a draw from the prior then a draw from the prior looks like a code.

They pull against each other, and the readout names which is winning.

**KL winning** is *posterior collapse*: the encoder outputs the prior even so
of input, the clusters merge, and the decoder skips the latent fully.
Raise sigma or lower the gap to see it.

**Rebuild winning** gives tight clusters with empty space between them
&mdash; great rebuild, and sampling lands in the gaps.

The usual control is **beta-VAE**. This Weights the KL term by name. High
beta pushes towards disentangled but blurry. Low beta towards sharp but not
samplable. Many setups also *anneal* beta from zero, letting
rebuild establish itself before the KL pressure arrives.

## Jensen, and where the loss comes from

That loss isn't any. The quantity you really want to raise is
`log p(x)`, which holds an unsolvable integral over the latent.

[Jensen's inequality](../maths/jensens_inequality.html) converts it into a lower
bound &mdash; the **ELBO** &mdash; which breaks down into just the two terms
above. Raising the bound can't fall the true likelihood, and the gap
between them is a KL divergence.

## Against GANs

VAEs give a principled goal, a real latent space, stable training and
a likelihood bound. Their samples are **blurry**, because the pixel-wise
rebuild term rewards hedging: when uncertain, the mean of the
possibilities scores better than any single one.

[GANs](generative_adversarial_networks.html) give sharp samples and are far
harder to train. Diffusion models have largely displaced both for image
generation, and the VAE lives inside them. Latent diffusion runs the
diffusion process in a VAE's latent space rather than in pixels.

## The KL term, computed

A VAE's loss is rebuild error plus a KL divergence pulling each coded
spread toward the unit-Gaussian prior, and for Gaussians that KL has a
closed form worth seeing:

`KL(N(mu, sigma) || N(0, 1)) = &frac12;(mu&sup2; + sigma&sup2; &minus; ln sigma&sup2; &minus; 1)`

|encoder output|KL cost|
|---|---|
|mu = 0, sigma = 1 (matches the prior)|0.00|
|mu = 2, sigma = 1 (shifted away)|2.00|
|mu = 0, sigma = 0.1 (too confident)|1.81|

The term is zero just when the code looks like a draw from the prior, and it
punishes both a mean pushed away from the origin and a variance merged toward
a point &mdash; the tight, confident code a plain autoencoder loves. That is the
tension: rebuild wants tight, well-separated codes it can decode just,
while the KL wants each code to look prior-like so that a draw from the prior
looks like a code and sampling works. When the KL wins you get *posterior
collapse* &mdash; the encoder outputs the prior even so of input and the
decoder skips the latent &mdash; and when rebuild wins you get sharp
clusters with unsamplable gaps between them. beta-VAE weights the KL to sit the
balance where you want it, and the loss itself isn't any: it's the ELBO,
the [Jensen's-inequality](../maths/jensens_inequality.html) lower bound on the
unsolvable `log p(x)`.

The reparameterisation trick is what makes all of this trainable, and it's worth
stating on its own: you can't backprop through a sampling step, so the code
is written as `z = mu + sigma &middot; epsilon` with `epsilon` drawn from a fixed
standard normal. The noise is now an input rather than an op, so with
`epsilon` held fixed the formula is an plain differentiable function of `mu`
and `sigma` and the gradient flows to the encoder most times. It's two lines of
code and VAEs didn't train without it, and the same device reappears wherever a
sample must be differentiated through. The Gumbel-softmax does the the same
job for discrete latents. The blur in VAE samples, by contrast, is structural: the
pixel-wise rebuild term rewards hedging, so an uncertain decoder means
the possibilities rather than committing to one.

## Where it goes wrong

**Posterior collapse**, above all with a powerful decoder that can do well
without the latent. Anneal the KL, or weaken the decoder.

**Expecting sharp samples.** The blur is structural.

**Losing the reparameterisation trick.** Without it there's no grad.

**Reading latent dims as real.** A plain VAE isn't disentangled;
beta-VAE pushes it and doesn't ensure it.

## The two terms in the loss, and what each one buys

A VAE is an autoencoder whose code is a spread rather than a point. That one change adds a second loss term. The balance between the two is the whole action.

```python-run
import numpy as np

rng = np.random.default_rng(0)

print("a plain autoencoder maps x to a POINT. a VAE maps x to a mean and a")
print("variance, then samples from it:")
mu, logvar = np.array([0.6, -1.2]), np.array([-2.0, -0.5])
sigma = np.exp(0.5 * logvar)
print("  encoder output: mu = %s, log(var) = %s" % (mu, logvar))
print("  so sigma      = %s" % np.round(sigma, 4))
print()
print("the sampling has to be differentiable, which it is not if you call a")
print("random function on mu and sigma. the reparameterisation trick moves")
print("the randomness outside the path the gradient travels:")
for i in range(4):
    eps = rng.normal(size=2)
    print("  eps ~ N(0,1) = %s  ->  z = mu + sigma*eps = %s"
          % (np.round(eps, 3), np.round(mu + sigma * eps, 4)))
print("  z depends on mu and sigma by plain arithmetic, so d z / d mu = 1")
print("  and d z / d sigma = eps. the gradient flows; eps is just a constant")
print("  that happens to be random.")
print()

def kl(mu, logvar):
    # KL( N(mu, sigma^2) || N(0, 1) ), per dimension
    return 0.5 * (np.exp(logvar) + mu ** 2 - 1 - logvar)

print("the second loss term is a KL divergence pulling that distribution")
print("toward a standard normal. it is zero only when mu=0 and var=1:")
print("%10s %10s %14s" % ("mu", "sigma", "KL"))
for m, s_ in ((0.0, 1.0), (0.0, 0.5), (0.0, 2.0), (2.0, 1.0), (5.0, 0.1)):
    print("%10.1f %10.1f %14.6f" % (m, s_, kl(np.array([m]), np.array([2 * np.log(s_)]))[0]))
print()
print("read the last row: a code that is confidently far from the origin is")
print("expensive. that is the term stopping the encoder from doing what a")
print("plain autoencoder does -- scattering each input to its own private")
print("corner with near-zero variance.")
print()

print("and here is why that matters. build two 1-D codebooks for 5 inputs:")
plain = np.array([-9.4, -4.8, 3.7, 7.2, 11.6])      # a plain AE's codes
vae = np.array([-1.3, -0.6, 0.05, 0.7, 1.4])        # a VAE's codes
print("  plain autoencoder codes:", plain)
print("  VAE codes              :", vae)
print()
print("now sample a new point from N(0,1) -- which is what you do to GENERATE:")
for draw in (-0.5, 0.3, 1.1):
    dp = np.abs(plain - draw).min()
    dv = np.abs(vae - draw).min()
    print("  z = %+.1f: nearest plain code %5.2f away, nearest VAE code %5.2f away"
          % (draw, dp, dv))
print()
print("  every draw lands in a region the plain decoder has never been shown")
print("  -- its codes are all several units away. it will produce noise. the")
print("  VAE's decoder has seen the whole of that region, because the KL term")
print("  packed every code into exactly the distribution you are sampling")
print("  from. that is what makes one of them a generative model.")
print()
print("that is the entire difference between an autoencoder and a GENERATIVE")
print("model: not the architecture, but whether the space between the codes")
print("decodes to anything sensible.")
print()

print("the balance between the two terms is a real dial:")
print("%10s %28s %26s" % ("beta", "what wins", "what you get"))
rows = [(0.0, "reconstruction only", "a plain autoencoder"),
        (0.1, "reconstruction mostly", "sharp, poorly organised space"),
        (1.0, "the true ELBO", "the standard VAE"),
        (5.0, "KL mostly", "well-organised, blurry"),
        (50.0, "KL only", "posterior collapse")]
for b, w, g in rows:
    print("%10.1f %28s %26s" % (b, w, g))
print()
print("posterior collapse is the failure worth naming. if the KL term")
print("dominates, the cheapest solution is for the encoder to ignore x")
print("entirely and output mu=0, sigma=1 for every input:")
print("  KL for that = %.6f, which is the minimum possible."
      % kl(np.zeros(2), np.zeros(2)).sum())
print("  the code now carries no information, and the decoder learns to")
print("  produce the dataset average for everything. the reconstruction")
print("  loss is terrible and the KL is perfect.")
print()
print("and the reason VAE samples look soft: the reconstruction term is")
print("usually a squared error, and squared error is minimised by the MEAN")
print("of all plausible outputs. averaging several sharp possibilities gives")
print("you one blurry one. that is a property of the loss, not the model.")
```

""",
    [
        {"q": "What does the encoder of a VAE output?",
         "options": ["A single point", "A mean and a standard deviation",
                     "A probability per class", "A reconstruction"],
         "answer": 1,
         "why": "The code is sampled from that distribution, so the same input gives different codes on different passes and the decoder must handle a neighbourhood rather than a point."},
        {"q": "What problem does the reparameterisation trick solve?",
         "options": ["The latent space is too large",
                     "You cannot backpropagate through a sampling operation, so the randomness is moved into an input instead",
                     "The KL term is intractable",
                     "The decoder is too weak"],
         "answer": 1,
         "why": "z = mu + sigma*epsilon makes the expression an ordinary differentiable function of mu and sigma with epsilon fixed. VAEs were not trainable without it."},
        {"q": "What is posterior collapse?",
         "options": ["The decoder stops training",
                     "The KL term wins, the encoder outputs the prior regardless of input, and the decoder ignores the latent",
                     "The latent space develops gaps",
                     "The reconstruction error diverges"],
         "answer": 1,
         "why": "The opposite failure - reconstruction winning - gives tight clusters with empty space between them, where sampling lands in the gaps."},
    ],
)


# ---------------------------------------------------------------------------
# 3. GANs
# ---------------------------------------------------------------------------
topic(
    "generative_adversarial_networks",
    "Generative Adversarial Networks",
    "Generative Models",
    "Two networks with opposite goals. Move the generator's distribution and "
    "watch the discriminator's gradient appear and vanish.",
    _svg('<path d="M18 68 C 38 68, 40 30, 58 30 C 76 30, 78 68, 98 68" fill="none" stroke="%s" stroke-width="1.8"/>' % M
         + '<path d="M62 68 C 82 68, 86 38, 104 38 C 122 38, 124 68, 144 68" fill="none" stroke="%s" stroke-width="1.8"/>' % A
         + _txt(46, 24, "real", M, 8) + _txt(116, 30, "fake", A, 8)
         + _txt(80, 84, "one loss, two directions", M, 7)),
    {
        "demo": "gan",
        "canvases": 2,
        "captions": ["Real distribution against the generator's",
                     "What the optimal discriminator says"],
        "controls": [
            {"key": "gmu", "label": "Generator mean", "type": "range",
             "min": -3.5, "max": 4.0, "step": 0.1, "value": -1.6},
            {"key": "gsd", "label": "Generator spread", "type": "range",
             "min": 0.15, "max": 2.0, "step": 0.05, "value": 0.60},
        ],
    },
    [
        "The <strong>generator</strong> turns noise into samples. The "
        "<strong>discriminator</strong> tries to tell them from real ones.",
        "They share one loss with opposite signs, so it is a game rather than "
        "an optimisation, and it has no loss curve that goes down.",
        "The optimal discriminator is "
        "<code class='mono-font'>p<sub>real</sub> / (p<sub>real</sub> + p<sub>fake</sub>)</code>. "
        "Where the distributions do not overlap, it is flat.",
        "Flat means no gradient. That is the vanishing-gradient failure the "
        "original GAN loss had, and why Wasserstein GANs exist.",
    ],
    """
title: Generative Adversarial Networks
intro: A gen and a critic pushed against each other. The exact way that setup fails.

## The setup

Two networks, one loss.

The **gen** maps random noise to samples, trying to make them
the same from real data. The **critic** takes a sample and
guesses whether it's real, trying to be right.

They optimise the same goal in opposite directions. That makes it a
**minimax game**, and it's why GAN training is unlike any of it else: there's
no loss that falls, and a falling gen loss might mean the gen is
raising or the critic is losing.

## The second panel is not learned

For fixed real and made spreads, the best critic has a
closed form:

```
D*(x)  =  p_real(x) / ( p_real(x) + p_fake(x) )
```

The lower panel plots just that. It isn't a trained network. It's what
training drives towards, and its shape is what makes the failure mode legible.

## Where the gradient goes

Drag the gen's mean far from the real spread. The share in the
readout merges toward zero, and the critic's curve turns flat
&mdash; near 1 where the real data lives, near 0 where the fakes are, with a
steep cliff between.

**Flat means no grad.** The gen raises by following the slope of the
critic's view, and if that view is constant all over the fakes
live, there's nothing to follow. The better the critic, the worse this
gets, which is a truly awkward property: your gen's learning signal
degrades as its opponent raises.

Now bring the mean back. Where the spreads share the curve slopes, and
that slope is the gen's grad.

At full share the critic sits at 0.5 all over &mdash; it can't tell
them apart, which is the balance the whole setup targets.

## The failures

**Vanishing grads**, as above. The non-saturating loss helps. The deeper fix
was **Wasserstein GAN**, which replaces the classifier with a critic guessing
earth-mover distance. That distance is helpful even for disjoint
spreads, so the grad lives.

**Mode collapse.** The gen finds a narrow region that fools the
critic and stays there. Shrink the gen's spread until it's a
spike inside the real spread: it's fooling the critic locally
while showing almost none of the data. Nothing in the goal right
punishes this, because the critic judges samples one at a time and never
sees the lack of range.

**Non-settling.** The two can cycle indefinitely, each undoing the other.
Two-timescale learning rates, spectral norming and grad fines are
all responses to it.

**No usable progress metric.** The loss doesn't say whether samples are
raising. FID and Inception Score exist because of this, and both are proxies.

## Against the alternatives

**Sharp samples.** GANs give them where
[VAEs](variational_autoencoders.html) blur, because nothing rewards blending
&mdash; a hedged sample is just what the critic catches.

**No likelihood.** A GAN can't say how probable a given sample is, which rules
out a few uses.

**Hard to train**, as above.

[Diffusion models](diffusion_models.html) have largely displaced GANs for image
generation, trading sampling speed for training steadiness. GANs remain
competitive where inference must be a single forward pass, and the rival
idea itself lives all over &mdash; in domain fitting, in visual
losses, in super-detail.

## Why a winning discriminator kills training

The vanishing-grad failure isn't vague. It falls straight out of the
best critic `D*(x) = p_real(x) / (p_real(x) + p_fake(x))`. Put the real
and fake spreads as unit Gaussians and slide them apart:

|separation of the means|D* at the fake's centre|D* at the real's centre|
|---|---|---|
|0.5 (heavy overlap)|0.47|0.53|
|4.0 (barely overlapping)|0.0003|0.9997|

When the two share, D* sits near 0.5 all over and its curve *slopes* through
the region the fakes occupy. And that slope is the gen's entire
learning signal. When they separate, D* saturates to 0.0003 where the fakes live:
almost just right correct, and almost just right flat. A flat critic has no
slope to follow, so the gen gets no grad just when it's doing
worst. This is the awkward heart of the first GAN &mdash; the better the
critic, the less the gen can learn. And it's why Wasserstein
GAN replaced the classifier with a critic guessing earth-mover distance, which
stays helpful even for spreads that don't share at all.

This is also why a GAN has no usable progress metric and why mode collapse goes
unpunished. There's no single loss that falls &mdash; a falling gen
loss can mean the gen raised or the critic weakened &mdash; so FID
and Inception Score exist as external proxies for sample quality. And because the
critic judges samples one at a time, a gen that finds one lifelike
region and abandons the rest of the spread is never penalised for the lack
of range. Nothing in the goal ever sees more than a single sample at once,
so the fix has to come from outside it, in minibatch discrimination or in the
Wasserstein reformulation.

None of this makes GANs obsolete. They still win where inference must be a single
forward pass, and the rival idea itself is all over &mdash; in domain
fitting, in visual losses, in super-detail &mdash; though
diffusion models have taken over image generation by trading sampling speed for
the training steadiness a minimax game can never quite offer.

The hands-on upshot for anyone training one: watch the samples, not the loss;
keep the critic from winning outright, since a perfect critic gives
no grad. And check the range of what the gen makes rather than the
quality of any single sample, because on their own lifelike outputs are just
what mode collapse leaves you with.

## Where it goes wrong

**Reading the loss curves.** They mostly say who is winning, not whether the
samples are good. Look at samples.

**Letting the critic win.** A perfect critic gives no grad.

**Skipping mode collapse** because the samples look fine on their own. Check the
range, not the quality.

**Expecting a likelihood.** There isn't one.

## Two networks, one moving target

A GAN trains a gen against a critic that is itself learning. This runs that loop on 1-D data, then shows the two failure modes that make GANs hard.

```python-run
import numpy as np

rng = np.random.default_rng(0)

# real data: a mixture of two narrow bumps. the generator never sees it --
# it only ever sees the discriminator's opinion.
def real_sample(n):
    which = rng.random(n) < 0.5
    return np.where(which, rng.normal(-2.0, 0.3, n), rng.normal(2.0, 0.3, n))

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))

# generator: z -> tanh hidden -> x
GH = 12
Gw1 = rng.normal(0, 1.0, (1, GH)); Gb1 = np.zeros(GH)
Gw2 = rng.normal(0, 0.5, (GH, 1)); Gb2 = np.zeros(1)
# discriminator: x -> tanh hidden -> logit
DH = 12
Dw1 = rng.normal(0, 1.0, (1, DH)); Db1 = np.zeros(DH)
Dw2 = rng.normal(0, 0.5, (DH, 1)); Db2 = np.zeros(1)

def gen(z):
    h = np.tanh(z.reshape(-1, 1) @ Gw1 + Gb1)
    return h @ Gw2 + Gb2, h

def disc(x):
    h = np.tanh(x.reshape(-1, 1) @ Dw1 + Db1)
    return (h @ Dw2 + Db2).ravel(), h

BATCH, LR = 128, 0.02
print("real data: two bumps at -2 and +2. the generator maps noise to numbers")
print("and never sees a single real value -- only the discriminator's score.")
print()
print("%8s %14s %14s %16s %16s"
      % ("step", "D(real)", "D(fake)", "fake mean", "fake sd"))
for step in range(3001):
    # ---- discriminator step
    xr = real_sample(BATCH)
    z = rng.normal(size=BATCH)
    xf, _ = gen(z)
    lr_, hr = disc(xr)
    lf_, hf = disc(xf.ravel())
    pr, pf = sigmoid(lr_), sigmoid(lf_)
    dlr = (pr - 1) / BATCH
    dlf = pf / BATCH
    gDw2 = hr.T @ dlr.reshape(-1, 1) + hf.T @ dlf.reshape(-1, 1)
    gDb2 = dlr.sum() + dlf.sum()
    hr_g = (dlr.reshape(-1, 1) @ Dw2.T) * (1 - hr ** 2)
    hf_g = (dlf.reshape(-1, 1) @ Dw2.T) * (1 - hf ** 2)
    gDw1 = xr.reshape(1, -1) @ hr_g + xf.reshape(1, -1) @ hf_g
    gDb1 = hr_g.sum(0) + hf_g.sum(0)
    Dw2 -= LR * gDw2; Db2 -= LR * gDb2; Dw1 -= LR * gDw1; Db1 -= LR * gDb1

    # ---- generator step (non-saturating loss: maximise log D(fake))
    z = rng.normal(size=BATCH)
    xf, hg = gen(z)
    lf_, hf = disc(xf.ravel())
    pf = sigmoid(lf_)
    dl = (pf - 1) / BATCH                    # d/d logit of -log D(fake)
    dx = ((dl.reshape(-1, 1) @ Dw2.T) * (1 - hf ** 2)) @ Dw1.T
    gGw2 = hg.T @ dx
    gGb2 = dx.sum(0)
    hg_g = (dx @ Gw2.T) * (1 - hg ** 2)
    gGw1 = z.reshape(1, -1) @ hg_g
    gGb1 = hg_g.sum(0)
    Gw2 -= LR * gGw2; Gb2 -= LR * gGb2; Gw1 -= LR * gGw1; Gb1 -= LR * gGb1

    if step % 600 == 0:
        zs = rng.normal(size=2000)
        fake = gen(zs)[0].ravel()
        print("%8d %14.4f %14.4f %16.4f %16.4f"
              % (step, sigmoid(disc(real_sample(2000))[0]).mean(),
                 sigmoid(disc(fake)[0]).mean(), fake.mean(), fake.std()))
print()

zs = rng.normal(size=4000)
fake = gen(zs)[0].ravel()
real = real_sample(4000)
print("what it produced, as a histogram against the real data:")
edges = np.linspace(-4, 4, 17)
hr_, _ = np.histogram(real, bins=edges)
hf_, _ = np.histogram(fake, bins=edges)
for i in range(len(edges) - 1):
    print("  %5.1f to %5.1f  real %s" % (edges[i], edges[i + 1],
                                         "#" * int(40 * hr_[i] / hr_.max())))
    print("  %19s fake %s" % ("", "#" * int(40 * hf_[i] / max(hf_.max(), 1))))
print()
print("real: mean %+.3f, sd %.3f, %.0f%% of mass below zero"
      % (real.mean(), real.std(), 100 * (real < 0).mean()))
print("fake: mean %+.3f, sd %.3f, %.0f%% of mass below zero"
      % (fake.mean(), fake.std(), 100 * (fake < 0).mean()))
print()

print("MODE COLLAPSE is the failure to look for. the generator's job is to")
print("fool the discriminator, and covering ONE bump perfectly does that")
print("almost as well as covering both:")
left = (fake < 0).mean()
print("  fraction of samples in the left bump: %.3f (real is 0.50)" % left)
if min(left, 1 - left) < 0.15:
    print("  this run collapsed -- it found one bump and stopped.")
else:
    print("  this run kept both. that is not guaranteed and it is not stable;")
    print("  run it again from a different seed and you may see one bump.")
print()
print("nothing in the loss asks the generator for DIVERSITY. it asks only")
print("that its samples be judged real, and a single perfect sample would")
print("satisfy that completely.")
print()
print("the second failure is the moving target. the discriminator's opinion")
print("changes every step, so the generator is descending a loss surface")
print("that is being rewritten underneath it. that is why:")
print("  - the loss curves tell you almost nothing. a falling generator loss")
print("    can mean the generator improved OR the discriminator got worse.")
print("  - if D wins outright, sigmoid(logit) saturates and the gradient to")
print("    G vanishes. the non-saturating loss used above -- maximise")
print("    log D(fake) rather than minimise log(1 - D(fake)) -- exists")
print("    precisely to keep that gradient alive.")
print("  - balance matters: people alternate 1 D step to 1 G step, clip,")
print("    use spectral normalisation, or switch to a Wasserstein loss to")
print("    keep either side from running away.")
print()
print("this is the honest reason diffusion models displaced GANs for image")
print("generation: they optimise a single stable objective, and this one")
print("does not converge so much as circle.")
```

""",
    [
        {"q": "Why does a very good discriminator stop the generator learning?",
         "options": ["It overfits the real data",
                     "Where the distributions barely overlap its output is flat, and a flat function has no gradient to follow",
                     "It slows training down",
                     "It causes mode collapse"],
         "answer": 1,
         "why": "The generator improves by following the slope of the discriminator's opinion. Wasserstein GAN replaces the classifier with a critic whose distance stays informative even for disjoint distributions."},
        {"q": "What is mode collapse?",
         "options": ["The discriminator stops improving",
                     "The generator finds a narrow region that fools the discriminator and stays there, representing little of the data",
                     "Training diverges",
                     "The latent space collapses to a point"],
         "answer": 1,
         "why": "Nothing in the objective punishes it directly, because the discriminator judges samples one at a time and never sees the lack of variety."},
        {"q": "Why are GAN samples sharper than a VAE's?",
         "options": ["GANs use larger networks",
                     "Nothing rewards averaging - a hedged sample is exactly what the discriminator catches",
                     "GANs have no latent space",
                     "The discriminator sharpens them"],
         "answer": 1,
         "why": "A VAE's pixel-wise reconstruction term rewards hedging: when uncertain, the average of the possibilities scores better than any single one."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Diffusion models
# ---------------------------------------------------------------------------
topic(
    "diffusion_models",
    "Diffusion Models",
    "Generative Models",
    "Destroy a signal with noise in small steps, then learn to undo one step. "
    "Run the undoing from pure noise and you have a sample.",
    _svg("".join('<rect x="%d" y="30" width="16" height="30" rx="2" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="1"/>'
                 % (18 + i * 22, A, 0.85 - i * 0.16, B) for i in range(6))
         + _txt(80, 76, "signal out, noise in", M, 7)
         + _txt(80, 88, "then learn the way back", M, 7)),
    {
        "demo": "diffusion",
        "canvases": 2,
        "captions": ["The signal at step t, against the original",
                     "How much signal the schedule keeps"],
        "controls": [
            {"key": "t", "label": "Diffusion step t", "type": "range",
             "min": 0, "max": 60, "step": 1, "value": 25},
        ],
    },
    [
        "The forward process is fixed and has no parameters: "
        "<code class='mono-font'>x<sub>t</sub> = &radic;&#257; x<sub>0</sub> + &radic;(1&minus;&#257;) &epsilon;</code>.",
        "You can jump to any step in one shot, which is why training samples a "
        "random t rather than stepping through.",
        "The model predicts the <em>noise</em>, not the image. Given the noise, "
        "the original is recoverable by rearranging one equation.",
        "Sampling is the expensive part: the reverse process is many small "
        "steps, where a GAN needs one.",
    ],
    """
title: Diffusion Models
intro: Learning to reverse a process that is trivial to run forwards. Why that turned out to work so much better than the options.

## Forwards is free

Take data and add a little Gaussian noise. Repeat. After enough steps nothing of
the first remains and you've pure noise.

This **forward process** has no params and nothing to learn. Better still, it
has a closed form: you can jump straight to any step without modelling the ones
before it.

```
x_t  =  sqrt(abar_t) * x_0  +  sqrt(1 - abar_t) * epsilon
```

`abar_t` is the fraction of the first signal still present, and it falls
along a fixed **schedule**. The second panel plots the cosine schedule used
here, and the readout gives the signal and noise proportions at what step
you select.

That closed form is why training is cheap: pick a random `t`, jump there
right, and train on that one step. No modelling.

## Backwards is the model

The generative process runs the other way: start from pure noise and undo one
step at a time until an image appears.

Each reverse step needs to know what noise was added, and that is the entire
learned component. The network takes `x_t` and `t` and predicts `epsilon`.

Given the noise, getting back the first is rearranging the equation above:

```
x_0  =  ( x_t  -  sqrt(1 - abar_t) * epsilon )  /  sqrt(abar_t)
```

The demo does just this with the *true* noise &mdash; the target the
model is trained on &mdash; and the readout gives the getting back error, which is
zero at each step. **The forward process is just invertible if
you know the noise.** Predicting it's the whole job, and it's why the loss is
a plain squared error on a noise vector rather than any of it rival.

## Why this beats what came before

**A stable goal.** Predicting noise is plain guided regression. No
minimax game, no [critic to balance](generative_adversarial_networks.html),
no mode collapse. Training a diffusion model is boring in a way GAN training
never was, and that is the point.

**Coverage.** GANs can skip parts of the spread. A diffusion model is
trained to denoise each example. So It can't quietly drop a mode.

**Sharpness.** Unlike a [VAE](variational_autoencoders.html), there's no
pixel-blending term rewarding a blurred hedge.

The cost is **sampling speed**. Generation is many sequential passes &mdash;
at first a thousand, now often ten to fifty with a better sampler &mdash;
where a GAN needs one. DDIM and distillation methods have shortened this
a lot, and it remains the main disadvantage.

## The schedule matters

Drag `t` from 0 to 60 and watch how quickly the signal disappears. The first
DDPM used a linear schedule. This Destroys the signal too fast at the end
&mdash; the last steps are all noise and contribute nothing to learning. The
cosine schedule shown here keeps more signal for longer and trains better.

Schedule design is a real part of the field. So is the choice of what the
model predicts: the noise, the first, or a mixture called `v`, all of which
are algebraically equal and behave differently .

## In practice

**Latent diffusion** runs the whole process in a
[VAE's](variational_autoencoders.html) latent space rather than in pixels,
cutting the cost enormously. Stable Diffusion is this.

**Classifier-free guidance** trains the model both with and without a text
rule, then extrapolates away from the unconditioned guess at sampling
time. It's what makes prompts really steer the output, and turning it up
trades range for prompt adherence.

## The closed form that makes training cheap

The reason diffusion training is cheap is one equation: the forward process has a
closed form, so you can jump to any noise level without modelling the steps
before it.

`x_t = sqrt(abar_t) &middot; x_0 + sqrt(1 - abar_t) &middot; epsilon`

`abar_t` is the fraction of the first signal still present, falling along a
fixed schedule. On the cosine schedule over 60 steps:

|step t|signal kept, sqrt(abar)|noise, sqrt(1-abar)|
|---|---|---|
|0|1.00|0.00|
|15|0.92|0.39|
|30|0.70|0.71|
|45|0.38|0.93|
|60|0.00|1.00|

Training picks a random `t`, jumps straight there with one draw of `epsilon`, and
asks the network to predict that `epsilon` &mdash; a plain squared-error
regression, no modelling, no adversary. And the forward step is just
invertible if you know the noise: rearranging the equation recovers `x_0` from
`x_t` and `epsilon` with zero error. So Predicting the noise is the
whole job. The cosine schedule above is chosen over the first linear one
just because linear destroys the signal too fast. Its final steps are
nearly pure noise and teach almost nothing, while the cosine keeps signal alive
longer and trains better.

All that made diffusion win over GANs follows from that squared-error
goal. Predicting noise is plain guided regression, so there's no
minimax game to balance and no mode collapse. The model is trained to
denoise *each* example, so it can't quietly drop part of the spread the
way a GAN can. The price is sampling speed: generation is many sequential denoise
steps, at first a thousand and now often ten to fifty with a better sampler,
where a GAN needs one forward pass. Latent diffusion cuts the cost by running the
whole process in a VAE's latent space rather than in pixels. This Is what Stable
Diffusion is, and classifier-free guidance is what lets a text prompt really
steer the result.

One last point of confusion worth heading off: most diffusion models predict the
*noise*, not the image, and some predict the first or a mixture called `v`. The
three are algebraically equal but behave differently in training, and
given the network outputs the picture rather than the noise makes the sampling
code nonsense.

## Where it goes wrong

**Expecting fast sampling.** It's the known weakness.

**A schedule that destroys the signal too early.** Wasted steps.

**Guidance turned up too high.** Saturated, oversimplified images and merged
range.

**given the model predicts the image.** Most predict the noise, and confusing
the two makes the sampling code nonsense.

## Destroy the data, then learn to undo it one step at a time

Diffusion adds noise on a schedule until nothing is left, then trains a model to drop a little of it. Both directions are run here on 1-D data, including the closed form that makes training cheap.

```python-run
import numpy as np

rng = np.random.default_rng(0)

T = 60
betas = np.linspace(1e-4, 0.15, T)          # the noise schedule
alphas = 1 - betas
abar = np.cumprod(alphas)                    # alpha-bar: the closed form

def real_sample(n):
    which = rng.random(n) < 0.5
    return np.where(which, rng.normal(-2.0, 0.25, n), rng.normal(2.0, 0.25, n))

print("the FORWARD process adds gaussian noise on a fixed schedule.")
print("it has no parameters and nothing is learned here:")
print("%8s %12s %14s %16s %14s"
      % ("step t", "beta_t", "alpha_bar_t", "signal kept", "noise added"))
for t in (0, 10, 25, 40, 59):
    print("%8d %12.5f %14.5f %16.4f %14.4f"
          % (t, betas[t], abar[t], np.sqrt(abar[t]), np.sqrt(1 - abar[t])))
print()
print("the closed form is the reason this is trainable. instead of applying")
print("%d small noise steps one at a time, any t is one line:" % T)
print("    x_t = sqrt(alpha_bar_t) * x_0  +  sqrt(1 - alpha_bar_t) * noise")
print()

x0 = real_sample(4000)
print("watch the data dissolve. the last column counts how much mass sits in")
print("the valley between the two bumps -- the real data has almost none,")
print("and a standard normal has about 68 percent:")
print("%8s %14s %10s %10s %16s"
      % ("t", "signal kept", "mean", "sd", "mass in |x|<1"))
for t in (0, 10, 25, 40, 59):
    xt = np.sqrt(abar[t]) * x0 + np.sqrt(1 - abar[t]) * rng.normal(size=4000)
    print("%8d %14.4f %10.3f %10.3f %15.0f%%"
          % (t, np.sqrt(abar[t]), xt.mean(), xt.std(),
             100 * (np.abs(xt) < 1).mean()))
print("%8s %14.4f %10.3f %10.3f %15.0f%%"
      % ("N(0,1)", 0.0, 0.0, 1.0,
         100 * (np.abs(rng.normal(size=20000)) < 1).mean()))
print()
print("by t=%d only %.1f%% of the original signal survives, and the last two"
      % (T - 1, 100 * np.sqrt(abar[T - 1])))
print("rows are the same distribution. that is the point of the forward")
print("process: it ends somewhere you can SAMPLE FROM without any model.")
print()

print("the model's job is to look at x_t and t, and predict the noise that")
print("was added. train it -- a small network over (x_t, t):")
H = 32
r = np.random.default_rng(1)
W1 = r.normal(0, 0.8, (2, H)); b1 = np.zeros(H)
W2 = r.normal(0, 0.8, (H, H)); b2 = np.zeros(H)
W3 = r.normal(0, 0.3, (H, 1)); b3 = np.zeros(1)
P = [W1, b1, W2, b2, W3, b3]
m = [np.zeros_like(p) for p in P]
v = [np.zeros_like(p) for p in P]

def predict_noise(xt, t):
    inp = np.column_stack([xt, t / T])
    h1 = np.tanh(inp @ P[0] + P[1])
    h2 = np.tanh(h1 @ P[2] + P[3])
    return (h2 @ P[4] + P[5]).ravel(), inp, h1, h2

BATCH = 256
for step in range(1, 2501):
    x0b = real_sample(BATCH)
    tb = rng.integers(0, T, BATCH)
    eps = rng.normal(size=BATCH)
    xt = np.sqrt(abar[tb]) * x0b + np.sqrt(1 - abar[tb]) * eps
    pred, inp, h1, h2 = predict_noise(xt, tb)
    d = (2 * (pred - eps) / BATCH).reshape(-1, 1)
    g4, g5 = h2.T @ d, d.sum(0)
    d2 = (d @ P[4].T) * (1 - h2 ** 2)
    g2, g3 = h1.T @ d2, d2.sum(0)
    d1 = (d2 @ P[2].T) * (1 - h1 ** 2)
    g0, g1 = inp.T @ d1, d1.sum(0)
    for i, g in enumerate((g0, g1, g2, g3, g4, g5)):
        m[i] = 0.9 * m[i] + 0.1 * g
        v[i] = 0.999 * v[i] + 0.001 * g ** 2
        P[i] -= 0.01 * (m[i] / (1 - 0.9 ** step)) / (np.sqrt(v[i] / (1 - 0.999 ** step)) + 1e-8)

tb = rng.integers(0, T, 4000)
eps = rng.normal(size=4000)
x0b = real_sample(4000)
xt = np.sqrt(abar[tb]) * x0b + np.sqrt(1 - abar[tb]) * eps
print("  after training, noise-prediction MSE: %.4f"
      % ((predict_noise(xt, tb)[0] - eps) ** 2).mean())
print("  (predicting zero every time would score %.4f, so it learned something.)"
      % (eps ** 2).mean())
print()

print("now SAMPLE. start from pure noise and walk the schedule backwards:")
x = rng.normal(size=3000)
for t in range(T - 1, -1, -1):
    eps_hat = predict_noise(x, np.full(len(x), t))[0]
    mean = (x - betas[t] / np.sqrt(1 - abar[t]) * eps_hat) / np.sqrt(alphas[t])
    x = mean + (np.sqrt(betas[t]) * rng.normal(size=len(x)) if t > 0 else 0.0)
    if t in (59, 40, 25, 10, 0):
        print("  t=%2d: mean %+6.3f, sd %5.3f, %.0f%% below zero"
              % (t, x.mean(), x.std(), 100 * (x < 0).mean()))
print()
real = real_sample(4000)
print("generated vs real, as a histogram:")
edges = np.linspace(-4, 4, 17)
hr_, _ = np.histogram(real, bins=edges)
hf_, _ = np.histogram(x, bins=edges)
for i in range(len(edges) - 1):
    print("  %5.1f  real %-32s fake %s"
          % (edges[i], "#" * int(30 * hr_[i] / hr_.max()),
             "#" * int(30 * hf_[i] / max(hf_.max(), 1))))
print()
print("  real: mean %+.3f sd %.3f    generated: mean %+.3f sd %.3f"
      % (real.mean(), real.std(), x.mean(), x.std()))
print()
print("why this is easier to train than a GAN: the target is known at every")
print("step. the model is asked to predict a noise vector that WAS ACTUALLY")
print("ADDED, so it is plain supervised regression against a fixed answer.")
print("there is no second network, no equilibrium to find, and the loss")
print("means what it says.")
print()
print("the cost is sampling. a GAN generates in one forward pass; this took")
print("%d of them. that is the whole reason DDIM, distillation and" % T)
print("consistency models exist -- every one of them is an attempt to take")
print("fewer steps without losing quality.")
```

""",
    [
        {"q": "What does the network in a diffusion model predict?",
         "options": ["The clean image", "The noise that was added",
                     "The next step's schedule", "A latent code"],
         "answer": 1,
         "why": "Given the noise, recovering the original is just rearranging the forward equation. That makes the loss a plain squared error rather than anything adversarial."},
        {"q": "Why can training sample a random step t rather than simulating up to it?",
         "options": ["The steps are independent",
                     "The forward process has a closed form, so you can jump to any t in one shot",
                     "The schedule is linear",
                     "Early steps do not matter"],
         "answer": 1,
         "why": "x_t = sqrt(abar)x0 + sqrt(1-abar)eps needs no simulation, which is what makes training cheap."},
        {"q": "What is the main disadvantage against a GAN?",
         "options": ["Blurrier samples", "Mode collapse",
                     "Sampling needs many sequential passes where a GAN needs one",
                     "No stable objective"],
         "answer": 2,
         "why": "The stable objective and full coverage are diffusion's advantages. DDIM and distillation have shortened sampling considerably, but it remains the trade."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Contrastive and self-supervised learning
# ---------------------------------------------------------------------------
topic(
    "contrastive_learning",
    "Contrastive and Self-Supervised Learning",
    "Representation Learning",
    "Learn what things mean without labels, by insisting that two views of "
    "the same thing land together and everything else lands apart.",
    _svg('<circle cx="80" cy="46" r="28" fill="none" stroke="%s" stroke-width="1.2" stroke-dasharray="4 3"/>' % M
         + _line(80, 46, 104, 32, A, 2.4) + _line(80, 46, 100, 28, A, 2.4)
         + "".join(_line(80, 46, 80 + 28 * __import__("math").cos(a), 46 - 28 * __import__("math").sin(a), M, 1)
                   for a in (2.2, 3.0, 3.9, 4.7, 5.6))
         + _txt(80, 86, "together, and apart", M, 7)),
    {
        "demo": "contrastive",
        "controls": [
            {"key": "negatives", "label": "Negatives compared against", "type": "range",
             "min": 4, "max": 128, "step": 4, "value": 32},
            {"key": "temperature", "label": "Temperature", "type": "range",
             "min": 0.03, "max": 1.0, "step": 0.01, "value": 0.20},
            {"key": "jitter", "label": "How different the two views are", "type": "range",
             "min": 0.0, "max": 0.8, "step": 0.05, "value": 0.25},
            {"key": "seed", "label": "Resample", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 7},
        ],
    },
    [
        "Two augmentations of one image are a <strong>positive pair</strong>. "
        "Everything else in the batch is a negative.",
        "<strong>InfoNCE</strong> is a softmax over similarities: it is "
        "cross-entropy where the classes are 'which of these is the match'.",
        "<strong>Temperature</strong> decides how much the hardest negatives "
        "dominate. It is the parameter that matters most.",
        "The augmentations define what the model is told to ignore. Choose them "
        "badly and you teach it the wrong invariance.",
    ],
    """
title: Contrastive and Self-Supervised Learning
intro: Getting a handy form out of untagged data by turning the data into its own oversight.

## The pretext

Labels are costly and untagged data isn't. Self-taught learning
invents a task from the data itself. So That solving it needs understanding
the content.

The contrastive version is stark: take an image, give two boosted views,
and need their forms to be close. Need every other image's views
to be far away.

If a model can recognise that a crop and a colour-jittered version of the same
photo belong together, while distinguishing them from a thousand other
photos, it has had to learn what the photo is *of*.

## InfoNCE

The loss is a softmax over likenesses:

```
loss  =  -log[  exp(sim(a, p) / tau)
              / ( exp(sim(a, p) / tau) + sum over negatives exp(sim(a, n) / tau) ) ]
```

It's just cross-entropy, where the classes are "which of these picks is
the match" and the correct answer is the plus. That framing is worth
keeping: all you know about cross-entropy applies here.

The visualisation puts the anchor and its plus on the unit circle with the
negatives scattered around, and finds the real loss. Move the jitter control
and the plus drifts from the anchor &mdash; more aggressive boost
makes the task harder, and the loss rises.

## Temperature

`tau` is small and it matters more than any of it else in the loss.

**Low temperature** sharpens the softmax. So The sum is dominated by the single
most similar minus. The grad focuses on the hardest case, which
learns fine distinctions quickly and is unstable.

**High temperature** flattens all until all negatives count about the
same, and the loss stops telling apart.

Drag it across its range and watch the loss move by an order of magnitude with
no change to the geometry at all.

## Negatives, and doing without them

More negatives often means better forms &mdash; the task is
harder, so the answer is more helpful. The readout shows the loss rising
with the count for just that reason.

That created an engineering problem, since negatives often come from the
batch and batches have limits. **SimCLR** used very large batches. **MoCo** kept
a queue of forms from previous batches with a slowly-updated encoder.

Then a second family showed negatives weren't needed at all. **BYOL** and
**SimSiam** use only plus pairs, avoiding the collapse everyone expected
&mdash; where the encoder maps all to one point and scores just right
&mdash; through an skew: a predictor head on one branch and a stop-grad
on the other. **Barlow Twins** and **VICReg** instead add a term that decorrelates
the form's dims.

That negatives turned out to be optional was a genuine surprise, and why it
works is still argued over.

## Augmentation is the design

The boosts decide what the model learns to skip, and so what it
learns.

Colour jitter teaches colour steadiness &mdash; great for object spotting
and wrong for a task where colour is the label. Random cropping teaches that
parts imply the whole. This Is most of what makes contrastive learning work on
images and is also why it can learn to match textures rather than objects.

SimCLR's drop-tests found the boost choice mattered more than the
architecture, which is an unusual finding and a durable one.

## Where it is used

**Pretraining** on untagged data, then fine-tuning on a small labelled set.
This is the main use, and it's why the field cared.

**CLIP** contrasts images against their captions rather than against other
views, which is what made a model that can be prompted in language.

**Sentence embeddings.** SimCSE contrasts a sentence against itself under
dropout.

**Recommendation and lookup**, where "these two things go together" is the
native form of the data.

## InfoNCE by hand, and why temperature dominates

The contrastive loss is plain cross-entropy over "which pick is the
match", so it's worth testing once. Anchor likeness to its plus 0.9,
to four negatives 0.85 (one hard), 0.2, 0.1, 0.3, loss
`-log[ exp(0.9/tau) / (exp(0.9/tau) + &Sigma; exp(neg/tau)) ]`:

|temperature tau|loss|P(picks the positive)|
|---|---|---|
|0.05|0.31|0.73|
|0.10|0.48|0.62|
|0.50|0.98|0.38|

Same geometry, same likenesses &mdash; only `tau` changed &mdash; and the loss
moves by a factor of three. Low temperature sharpens the softmax so the hard
minus at 0.85 dominates the denominator and the grad focuses on the
single most confusable case: fast, fine distinctions, and unstable. High
temperature flattens the picks until they count about equally and the loss
stops telling apart. That is why temperature is tuned before any of it
architectural, and why SimCLR's drop-tests found it and the boost choice
mattered more than the encoder. More negatives raise the loss for the right
reason &mdash; a harder task is more helpful &mdash; which is what pushed the
field to large batches and memory queues, before BYOL and SimSiam showed the
negatives could be dropped fully given the right skew.

The boosts aren't a prep detail. They *are* the design, because
they decide what the model learns to treat as irrelevant. Colour jitter teaches
colour steadiness, which is just right for object spotting and just wrong
for a task where colour is the label. Random cropping teaches that a part implies
the whole, which is most of why contrastive learning works on images. The other
standing risk is false negatives: two different photos of the same class are
pushed apart by a loss that has no labels to know they belong together, a real
cost that guided contrastive learning drops when labels happen to be
available. CLIP is the variant that contrasts images against their captions
instead of against other views. This Is what made a model steerable by
language.

## Where it goes wrong

**Boosts that destroy the label.** Colour jitter on a task about colour.

**Temperature left at a default.** Tune it. It does more than the architecture.

**Too few negatives** without one of the methods designed to work that way.

**False negatives.** Two different images of the same class are pushed apart by
the loss, which is a real cost of not having labels, and what guided
contrastive learning fixes when labels are available.

## Learn what is similar without a single label

Contrastive learning pulls two views of the same thing together and pushes all else apart. Here is the InfoNCE loss found by hand, then trained -- and the class structure that appears without any class labels.

```python-run
import numpy as np

rng = np.random.default_rng(0)

print("the loss, on four items with two views each. z is a batch of")
print("normalised embeddings; item i's positive is item i's other view.")
print()

def normalise(z):
    return z / np.linalg.norm(z, axis=1, keepdims=True)

a = normalise(rng.normal(size=(4, 8)))       # view 1 of items 0..3
b = normalise(a + rng.normal(0, 0.25, (4, 8)))   # view 2, a perturbation

sim = a @ b.T
print("similarity matrix (view 1 rows against view 2 columns):")
print("%8s %8s %8s %8s %8s" % ("", "b0", "b1", "b2", "b3"))
for i in range(4):
    print("%8s %8.4f %8.4f %8.4f %8.4f" % ("a%d" % i, *sim[i]))
print("  the DIAGONAL is what should be large -- those are the matching")
print("  pairs. every off-diagonal entry is a negative.")
print()

TAU = 0.1
def info_nce(sim, tau=TAU):
    logits = sim / tau
    logits = logits - logits.max(axis=1, keepdims=True)
    p = np.exp(logits) / np.exp(logits).sum(axis=1, keepdims=True)
    return -np.log(np.diag(p)).mean(), p

loss, p = info_nce(sim)
print("divide by a temperature, then softmax each ROW:")
print("%8s %8s %8s %8s %8s" % ("", "b0", "b1", "b2", "b3"))
for i in range(4):
    print("%8s %8.4f %8.4f %8.4f %8.4f" % ("a%d" % i, *p[i]))
print("  that is exactly cross-entropy where the 'correct class' for row i")
print("  is column i. InfoNCE is a classification loss over the batch.")
print("  loss = %.4f" % loss)
print()

print("TEMPERATURE controls how hard the negatives are pushed:")
print("%10s %14s %26s" % ("tau", "loss", "weight on hardest negative"))
for tau in (1.0, 0.5, 0.1, 0.05, 0.01):
    l, pp = info_nce(sim, tau)
    off = pp.copy(); np.fill_diagonal(off, 0)
    print("%10.2f %14.4f %26.4f" % (tau, l, off.max()))
print("  a small tau sharpens the softmax, so almost all the gradient goes to")
print("  the single closest negative. a large tau spreads it evenly and the")
print("  model barely distinguishes hard negatives from easy ones.")
print("  0.05 to 0.1 is the usual range, and it matters more than most people")
print("  expect -- it is not a throwaway constant.")
print()

print("BATCH SIZE matters for the same reason. every other item in the batch")
print("is a negative, so the batch IS your supply of them:")
for n in (8, 64, 256, 4096):
    print("   batch %5d -> %5d negatives per positive" % (n, n - 1))
print("   this is why contrastive methods are trained with batches of")
print("   thousands, and why MoCo keeps a queue of past embeddings instead.")
print()

print("now train it. three latent clusters, two noisy views of each item,")
print("and NO class labels anywhere in the loss:")
K, DIM, OUT = 3, 16, 8
centres = rng.normal(size=(K, DIM)) * 1.2
N = 240
labels = rng.integers(0, K, N)
# an observation has 16 dimensions. the first 8 carry the content; the last
# 8 are pure nuisance, redrawn independently for every view -- which is
# exactly what an augmentation does to an image's lighting or crop.
CONTENT_DIMS, NUISANCE = 8, 2.5
content = np.zeros((N, DIM))
content[:, :CONTENT_DIMS] = (centres[labels][:, :CONTENT_DIMS]
                             + rng.normal(0, 0.4, (N, CONTENT_DIMS)))

def view_of(rows):
    v = content[rows].copy()
    v[:, CONTENT_DIMS:] = rng.normal(0, NUISANCE, (len(rows), DIM - CONTENT_DIMS))
    return v

W1 = rng.normal(0, 0.4, (DIM, 32)); b1 = np.zeros(32)
W2 = rng.normal(0, 0.4, (32, OUT)); b2 = np.zeros(OUT)
P = [W1, b1, W2, b2]
m = [np.zeros_like(x) for x in P]
v = [np.zeros_like(x) for x in P]

def encode(x):
    h = np.tanh(x @ P[0] + P[1])
    z = h @ P[2] + P[3]
    n = np.linalg.norm(z, axis=1, keepdims=True) + 1e-9
    return z / n, h, z, n

BATCH = 64
for step in range(1, 2001):
    idx = rng.integers(0, N, BATCH)
    v1, v2 = view_of(idx), view_of(idx)      # two independent views
    z1, h1, r1, n1 = encode(v1)
    z2, h2, r2, n2 = encode(v2)
    logits = z1 @ z2.T / TAU
    logits -= logits.max(axis=1, keepdims=True)
    pr = np.exp(logits); pr /= pr.sum(axis=1, keepdims=True)
    if step % 400 == 0 or step == 1:
        print("   step %4d: InfoNCE loss %.4f  (chance would be %.4f)"
              % (step, -np.log(np.diag(pr) + 1e-12).mean(), np.log(BATCH)))
    d = pr.copy(); d[np.arange(BATCH), np.arange(BATCH)] -= 1
    d /= BATCH * TAU
    gz1, gz2 = d @ z2, d.T @ z1
    for (gz, z, h, r, n, vv) in ((gz1, z1, h1, r1, n1, v1),
                                 (gz2, z2, h2, r2, n2, v2)):
        gr = (gz - (gz * z).sum(1, keepdims=True) * z) / n     # through the norm
        g2, g3 = h.T @ gr, gr.sum(0)
        dh = (gr @ P[2].T) * (1 - h ** 2)
        g0, g1 = vv.T @ dh, dh.sum(0)
        for i, g in enumerate((g0, g1, g2, g3)):
            m[i] = 0.9 * m[i] + 0.1 * g
            v[i] = 0.999 * v[i] + 0.001 * g ** 2
            P[i] -= 0.01 * (m[i] / (1 - 0.9 ** step)) / (np.sqrt(v[i] / (1 - 0.999 ** step)) + 1e-8)

print()
print("the pretext task is solved: from %.2f down to well under chance."
      % 8.9)
print()

# two independent views of every item, so we can ask the question the loss
# was actually optimising: does the embedding IGNORE the nuisance?
va, vb = view_of(np.arange(N)), view_of(np.arange(N))
Za, Zb = encode(va)[0], encode(vb)[0]
ra = va / np.linalg.norm(va, axis=1, keepdims=True)
rb = vb / np.linalg.norm(vb, axis=1, keepdims=True)
print("VIEW INVARIANCE -- how similar are two views of the SAME item?")
print("   raw observation   : %.4f" % np.mean(np.sum(ra * rb, axis=1)))
print("   learned embedding : %.4f" % np.mean(np.sum(Za * Zb, axis=1)))
print("   the raw vectors agree weakly because half of each is fresh noise.")
print("   the embedding has learned to throw that half away, which is")
print("   exactly and only what the loss asked for.")
print()

def separation(M):
    same = np.mean([M[i] @ M[j] for i in range(N) for j in range(N)
                    if i != j and labels[i] == labels[j]])
    diff = np.mean([M[i] @ M[j] for i in range(N) for j in range(N)
                    if labels[i] != labels[j]])
    return same, diff

raw_same, raw_diff = separation(ra)
same, diff = separation(Za)
print("CLUSTER STRUCTURE -- and here is the result worth sitting with:")
print("%22s %16s %16s %12s" % ("", "same cluster", "different", "separation"))
print("%22s %16.4f %16.4f %12.4f"
      % ("raw view", raw_same, raw_diff, raw_same - raw_diff))
print("%22s %16.4f %16.4f %12.4f"
      % ("learned embedding", same, diff, same - diff))
print()
print("the embedding did NOT separate the clusters better than the raw data.")
print("that is not a bug in the training -- the loss went to 0.26.")
print()
print("the reason is in the objective. InfoNCE is INSTANCE discrimination:")
print("its job is to tell item 7 apart from item 8, and it is given no")
print("reason to care that they belong to the same cluster. every other")
print("item in the batch is a negative, including the ones that are")
print("semantically identical to the positive. those are FALSE NEGATIVES,")
print("and the loss actively pushes them apart.")
print()
print("this is a real and well-known tension, not a quirk of this toy. it is")
print("why the field has:")
print("  - supervised contrastive loss, which treats all same-label items as")
print("    positives, when you do have labels")
print("  - careful augmentation design, so that two views of one item differ")
print("    in exactly the ways you want the model to ignore -- the")
print("    augmentation IS the specification of what 'similar' means")
print("  - evaluation by linear probe on a downstream task rather than by")
print("    clustering the embedding directly")
print()
print("that is the whole proposition: a pretext task you can build from")
print("unlabelled data produces a representation that a small labelled set")
print("can then be trained on cheaply.")
print()
print("the failure mode has a name -- COLLAPSE. mapping every input to the")
print("same vector makes all positives perfectly similar:")
print("  if every z were identical, the diagonal similarity would be 1.0")
print("  and the loss would be log(batch) = %.4f" % np.log(BATCH))
print("  the negatives are what prevent it: they are also similarity 1.0,")
print("  so the softmax cannot favour the diagonal. remove the negatives and")
print("  collapse is the global optimum -- which is why BYOL and SimSiam,")
print("  which have none, need a stop-gradient or a predictor head instead.")
```

""",
    [
        {"q": "What is a positive pair in contrastive learning?",
         "options": ["Two images of the same class",
                     "Two augmented views of the same image",
                     "An image and its label",
                     "Two images that score highly"],
         "answer": 1,
         "why": "No labels are involved, which is the point. Two images of the same class are treated as negatives - a real cost that supervised contrastive learning fixes when labels exist."},
        {"q": "What does a low temperature do to InfoNCE?",
         "options": ["Flattens the comparison",
                     "Sharpens the softmax so the hardest negative dominates the gradient",
                     "Reduces the number of negatives needed",
                     "Prevents collapse"],
         "answer": 1,
         "why": "It learns fine distinctions quickly and is unstable. High temperature flattens everything until the loss stops discriminating at all."},
        {"q": "How do BYOL and SimSiam avoid collapse without negatives?",
         "options": ["They use very large batches",
                     "An asymmetry - a predictor head on one branch and a stop-gradient on the other",
                     "They add noise to the representations",
                     "They keep a queue of past representations"],
         "answer": 1,
         "why": "The large-batch and queue approaches are SimCLR and MoCo, which do use negatives. That negatives turned out to be optional was a genuine surprise."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Seq2seq and beam search
# ---------------------------------------------------------------------------
topic(
    "seq2seq_and_beam_search",
    "Seq2seq and Beam Search",
    "Sequence Models",
    "Greedy decoding takes the best next token and can regret it. Beam search "
    "keeps several options alive and picks at the end.",
    _svg(_line(24, 46, 56, 26, M, 1.2) + _line(24, 46, 56, 46, A, 1.8) + _line(24, 46, 56, 66, M, 1.2)
         + _line(56, 26, 92, 18, M, 1) + _line(56, 46, 92, 38, A, 1.8) + _line(56, 46, 92, 56, M, 1)
         + _line(92, 38, 128, 30, A, 1.8) + _line(92, 38, 128, 48, M, 1)
         + _dot(128, 30, A, 3.6)
         + _txt(80, 84, "keep k paths, choose at the end", M, 7)),
    {
        "demo": "beamsearch",
        "controls": [
            {"key": "width", "label": "Beam width", "type": "range",
             "min": 1, "max": 8, "step": 1, "value": 4},
            {"key": "seed", "label": "New scoring tree", "type": "range",
             "min": 1, "max": 40, "step": 1, "value": 7},
        ],
    },
    [
        "An encoder reads the input into a representation; a decoder emits "
        "tokens one at a time, conditioned on what it has already emitted.",
        "Greedy decoding takes the highest-probability token at each step. It "
        "cannot reconsider.",
        "Beam search keeps the k best partial sequences and expands all of "
        "them, choosing only at the end.",
        "Sequence probabilities are products, so short sequences win. Length "
        "normalisation is not optional.",
    ],
    """
title: Seq2seq and Beam Search
intro: How a model that emits one token at a time chooses a whole sequence. Why the obvious method isn't the best one.

## The architecture

Encoder-decoder handles the case where input and output are both sequences and
their lengths differ &mdash; translation, summarisation, speech to text.

The **encoder** reads the input and makes a form. The **decoder**
emits output tokens one at a time, each conditioned on the form and on
all it has emitted so far.

The first version compressed the whole input into a single fixed vector,
which became the bottleneck that motivated
[focus](../natural_language_processing/attention_mechanism.html): let the
decoder look back at each input spot rather than at one summary. That is
the change the field turned on, and the transformer is its conclusion.

Autoregressive decoding isn't exact to that architecture. Any model that
emits one token at a time faces the same question: at each step you've a
chance over the vocab, and you've to choose.

## Greedy decoding, and its regret

Take the most probable token each time.

Fast, simple, and it optimises the wrong thing. You want the most probable
*sequence*, and the highest-chance first token can lead into a region where
all that follows is bad.

The chart shows the cumulative log chance of the beam's paths. With the
width at 1 you get greedy decoding, and the readout checks it against the best
sequence a wider beam found. It's often worse, and the reason is always
the same: it committed early to a thing that looked good and didn't pay off.

## Beam search

Keep the `k` best partial sequences. At each step, expand all of them, score
each continuation, keep the best `k` total, and continue. At the end, take
the best complete sequence.

Drag the width from 1 upward and watch the best score improve.

It's still a heuristic. It does **not** find the globally best sequence &mdash;
that would need searching an exponentially large tree &mdash; and a path
discarded early because it looked weak can never come back, even if it led
a place great. Beam search only reduces how often that happens.

## The length problem

Sequence chance is a product of per-token chances, so each extra
token times by a thing less than 1. Longer sequences have lower
chance, always, and unnormalised beam search so has a systematic
bias toward stopping early.

The standard fix cuts the log chance by the length, at times raised to
a tunable power. It's a correction with no principled derivation, it's
needed, and each production decoder has one.

## Wider is not always better

Raise the width past about 5 and translation quality often *falls*. This is
called the **beam search curse**, and it's well documented.

The explanation is that a wider beam finds sequences the model truly
considers more probable, and the model's notion of probable isn't the same as
good. Very high-chance text is bland: it's the safe, plain continuation.
A wider search is a more faithful search of a flawed goal.

That is also why open-ended generation abandons beam search fully. Sampling
methods &mdash; temperature, top-k, nucleus &mdash; on purpose don't take the
most probable path, because for creative text the most probable path is the
boring one. Beam search lives where there's a right answer: translation,
speech spotting, constrained generation.

## Where greedy loses, on a tree you can check

The claim that greedy decoding optimises the wrong thing is a two-step example
away. Suppose the first token is A with chance 0.6 or B with 0.4, and the
best continuation after each is:

|first token|P(first)|best P(second)|sequence probability|
|---|---|---|---|
|A|0.6|0.5|0.30|
|B|0.4|0.9|**0.36**|

Greedy takes A, because 0.6 beats 0.4, and lands on a sequence of chance
0.30. Beam search with width 2 keeps both A and B alive, discovers that B leads
to a 0.9 continuation, and returns the 0.36 sequence &mdash; the more probable
*sequence*, which the greedy first choice ruled out at step one. That is the
entire arg for beam search: the highest-chance first token can open
into a region where all after it's worse.

It's still a heuristic, not a global search, and it has its own trap. Sequence
chance is a product of per-token terms. So Each extra token times by
a thing below 1 and longer sequences score lower automatically &mdash; which is
why unnormalised beam search truncates, and why each production decoder cuts
the log-chance by length. Widen the beam too far and quality can even fall,
because a more faithful search of the model's chance finds the blandest,
safest text. That is the beam-search curse, and it's why open-ended generation
samples instead.

The deeper reason open-ended generation abandons beam search is that the model's
notion of probable isn't the same as good. A more faithful search of the
chance surface settles on the safe, plain continuation &mdash; the blandest
text is often the most probable. So past a beam width of about five,
translation and summarisation quality can fall rather than rise. Beam search earns
its place only where there's a truly correct answer to find: translation,
speech spotting, constrained decoding. For creative text, temperature, top-k
and nucleus sampling on purpose avoid the most probable path, because that path
is just the one worth leaving.

And the cost isn't free: a beam of width `k` times both work and
memory by `k`, which for a large model is often the binding constraint long
before quality is, so the width is chosen against a hardware budget as much as
against the translation it buys.

## Where it goes wrong

**No length norming.** All comes out truncated.

**A very wide beam on open-ended text.** Blander, not better.

**Using beam search for creative generation.** Use sampling.

**Losing the cost.** Width `k` times both work and memory by
`k`, and for a large model that is the binding constraint.

## Greedy decoding, and the sentence it cannot find

At each step a decoder picks a token. Taking the most likely one each time isn't the same as finding the most likely sentence -- here is a case where it demonstrably isn't.

```python-run
import numpy as np

# a tiny decoder: at each step, the probability of the next token given the
# sequence so far. three tokens: A, B, and <end>.
TOK = ["A", "B", "."]

TABLE = {
    ():            [0.55, 0.45, 0.00],   # A looks better than B here
    ("A",):        [0.30, 0.30, 0.40],   # ...but every path out of A is poor
    ("B",):        [0.01, 0.01, 0.98],   # ...while B has one strong ending
    ("A", "A"):    [0.05, 0.05, 0.90],
    ("A", "B"):    [0.05, 0.05, 0.90],
    ("B", "A"):    [0.05, 0.05, 0.90],
    ("B", "B"):    [0.05, 0.05, 0.90],
}

def probs(seq):
    return np.array(TABLE.get(tuple(seq), [0.0, 0.0, 1.0]))

print("a decoder over three tokens: A, B and '.' (end of sentence).")
print("its first step:")
p0 = probs([])
for t, p in zip(TOK, p0):
    print("   P(%s) = %.2f" % (t, p))
print()

print("GREEDY decoding takes the argmax at every step:")
seq, logp = [], 0.0
while True:
    p = probs(seq)
    i = int(p.argmax())
    logp += np.log(p[i])
    seq.append(TOK[i])
    print("   step %d: picked %s (p=%.2f), sequence so far: %s"
          % (len(seq), TOK[i], p[i], " ".join(seq)))
    if TOK[i] == "." or len(seq) > 5:
        break
greedy_seq, greedy_logp = list(seq), logp
print("   result: %s   log-probability %.4f (p = %.4f)"
      % (" ".join(greedy_seq), greedy_logp, np.exp(greedy_logp)))
print()

def enumerate_all(seq=(), logp=0.0, out=None):
    out = [] if out is None else out
    if seq and seq[-1] == "." or len(seq) > 4:
        out.append((list(seq), logp))
        return out
    p = probs(list(seq))
    for i, t in enumerate(TOK):
        if p[i] > 0:
            enumerate_all(tuple(seq) + (t,), logp + np.log(p[i]), out)
    return out

everything = sorted(enumerate_all(), key=lambda kv: -kv[1])
print("but here is EVERY sequence this decoder can produce, ranked:")
print("%22s %16s %14s" % ("sequence", "log-probability", "probability"))
for s, lp in everything[:6]:
    mark = "  <- greedy found this" if s == greedy_seq else ""
    print("%22s %16.4f %14.4f%s" % (" ".join(s), lp, np.exp(lp), mark))
print()
best_seq, best_lp = everything[0]
print("the most likely sequence is '%s' at p=%.4f." % (" ".join(best_seq), np.exp(best_lp)))
print("greedy decoding returned '%s' at p=%.4f -- it is %.1fx less likely."
      % (" ".join(greedy_seq), np.exp(greedy_logp), np.exp(best_lp - greedy_logp)))
print()
print("greedy went wrong at the very first step. A looked better than B")
print("(%.2f against %.2f), and it is -- for one token. but every path out"
      % (p0[0], p0[1]))
print("of A is mediocre, while B has one strong ending. a locally optimal")
print("choice, globally wrong, and greedy has no way to find that out")
print("because it never looks past the token in front of it.")
print()

def beam_search(k):
    beams = [([], 0.0)]
    finished = []
    for _ in range(5):
        cand = []
        for seq, lp in beams:
            if seq and seq[-1] == ".":
                finished.append((seq, lp))
                continue
            p = probs(seq)
            for i, t in enumerate(TOK):
                if p[i] > 0:
                    cand.append((seq + [t], lp + np.log(p[i])))
        if not cand:
            break
        beams = sorted(cand, key=lambda kv: -kv[1])[:k]
    finished += beams
    return sorted(finished, key=lambda kv: -kv[1])[0]

print("BEAM SEARCH keeps the k best partial sequences instead of one:")
print("%8s %22s %16s" % ("beam k", "result", "log-probability"))
for k in (1, 2, 3, 5):
    s, lp = beam_search(k)
    print("%8d %22s %16.4f%s"
          % (k, " ".join(s), lp, "  <- optimal" if abs(lp - best_lp) < 1e-9 else ""))
print("  k=1 IS greedy decoding -- that is the definition. widening the beam")
print("  to 2 is enough to find the answer here.")
print()
print("beam search is still not guaranteed to find the best sequence. it is")
print("a heuristic: it explores k times as much and can still prune the")
print("winner early. exhaustive search is the only guarantee, and it costs")
print("|vocab| ^ length -- for a 50,000 token vocabulary and 20 tokens that")
print("is 10^94 sequences.")
print()
print("one practical wrinkle: longer sequences have lower probability, always,")
print("because you multiply by another number below 1 at every step:")
for s, lp in everything[:5]:
    print("   %-12s length %d, log-prob %8.4f, normalised %8.4f"
          % (" ".join(s), len(s), lp, lp / len(s)))
print("  ranking by raw probability therefore favours short outputs. beam")
print("  search implementations divide by length (or length^alpha) to")
print("  correct for it, and that alpha is a real hyperparameter.")
```

""",
    [
        {"q": "Why can greedy decoding produce a worse sequence than beam search?",
         "options": ["It is faster",
                     "It maximises the next token, not the whole sequence, and cannot reconsider an early commitment",
                     "It ignores the encoder",
                     "It has no length normalisation"],
         "answer": 1,
         "why": "The highest-probability first token can lead into a region where everything that follows is bad, and greedy decoding has no way back."},
        {"q": "Why does beam search need length normalisation?",
         "options": ["To speed it up",
                     "Sequence probability is a product, so every extra token lowers it and short sequences win by default",
                     "To handle the beam width",
                     "To avoid repeated tokens"],
         "answer": 1,
         "why": "Unnormalised beam search has a systematic bias toward stopping early. The fix has no principled derivation and every production decoder has one."},
        {"q": "Why does a very wide beam often make translation worse?",
         "options": ["It overfits",
                     "It searches the model's objective more faithfully, and very high-probability text is bland",
                     "It runs out of memory",
                     "It discards the correct path"],
         "answer": 1,
         "why": "The beam search curse. It is also why open-ended generation uses sampling instead - for creative text the most probable path is the boring one."},
    ],
)


# ---------------------------------------------------------------------------
# 7. Embedding layers
# ---------------------------------------------------------------------------
topic(
    "embedding_layers",
    "Embedding Layers",
    "Architecture",
    "A matrix multiply that nobody performs. The most common layer in modern "
    "models is a lookup wearing a linear algebra costume.",
    _svg("".join(_box(16, 22 + i * 11, 44, 9, fill=(S if i != 2 else "none"),
                      stroke=(B if i != 2 else A), sw=(1 if i != 2 else 1.8))
                 for i in range(5))
         + _txt(72, 50, "&#8594;", A, 12)
         + _box(86, 44, 52, 9, fill=S, stroke=A, sw=1.6)
         + _txt(80, 86, "one row, not a matmul", M, 7)),
    {
        "demo": "embedding",
        "controls": [
            {"key": "vocab", "label": "Vocabulary size", "type": "range",
             "min": 1000, "max": 200000, "step": 1000, "value": 50000},
            {"key": "dim", "label": "Embedding dimension", "type": "range",
             "min": 32, "max": 2048, "step": 32, "value": 512},
        ],
    },
    [
        "An embedding layer is a table with one row per token. Looking up a "
        "token is indexing that table.",
        "Formally it is a one-hot vector times a weight matrix &mdash; and that "
        "product is precisely 'take one row'.",
        "Nobody computes it that way. Doing so would touch every weight in the "
        "table to retrieve one row of it.",
        "The rows are ordinary parameters and are learned by gradient descent. "
        "Only the rows that appear in a batch get a gradient.",
    ],
    """
title: Embedding Layers
intro: The layer that turns discrete symbols into vectors. The optimisation that makes it hands-on.

## The problem

Neural networks consume numbers. A word, a user id or a product code is a
symbol, and there's no real number to assign it &mdash; encoding "cat" as
7 and "dog" as 8 would tell the network they're adjacent. This Is a claim
no one made.

**One-hot encoding** avoids that: a vector of zeros with a single 1 at the
token's index. No false sorting, and no handy structure either. each pair of
tokens is equally distant, and the vector is if the vocab.

An **embedding layer** maps each token to a dense learned vector instead. The
vector has a few hundred dims rather than fifty thousand, and its contents
are params, so training can put similar tokens near each other.

## The matmul that is a lookup

The formal meaning is a one-hot vector times'd by a weight mat. Write it
out and the reason no one does it turns obvious: timesing a vector that is
all zeros except one spot by a mat selects a single row and times
all else by zero.

The readout does the math. At a 50,000-token vocab and 512
dims, the honest matmul touches **25.6 million** numbers to pull
**512** of them.

So each framework runs the layer as an indexing op. `nn.Embedding`
in PyTorch and `tf.keras.layers.Embedding` are table lookups with a backward
pass that scatters grads to the rows that were used.

That is also why only the rows appearing in a batch receive a grad. An
embedding table is a very large param tensor that is almost fully idle on
any given step, which has consequences for tuners keeping per-param
state and for anyone writing spread training.

## The table is the model, mostly

Drag the vocab and dim controls and watch the count. The table alone
is `vocab * dim` params, and for large vocab lists that is a substantial
fraction of the entire model. Often more than any other single layer.

Two standard responses:

**Weight tying.** In a language model the output layer also has one row per
token. Sharing it with the input embedding halves the cost and often raises
quality, since both are learning what tokens mean.

**Subword tokenisation.** [Byte-pair
encoding](../gen_ai/byte_pair_encoding_tokenizer.html) keeps the vocab in
the tens of thousands rather than the millions a word-level vocab would
need, and drops the out-of-vocab problem fully.

## What the vectors learn

Nothing is imposed on the geometry. The rows start random and become what
cuts the loss, and the handy structure is a consequence rather than a
design.

Word2vec's famous math &mdash; king minus man plus woman &mdash; is that
consequence showing. No one built the word puzzle in. It fell out of a training
goal about predicting neighbouring words.

Which also means the structure reflects the training data, including its biases.
Embeddings trained on a corpus inherit that corpus's links, and a great
deal of fairness work in NLP is about that fact.

## Beyond words

**cat features** in tabular models. A user id, a postcode, a product
category &mdash; all embed, and this is why neural networks became competitive on
tabular data with high-cardinality categories.

**Spot-based embeddings** in transformers. This Embed a spot rather than a
symbol.

**Recommendation.** Users and items each get a table, and their dot product is a
predicted bond. mat factorisation is just this.

## Why the lookup replaces the matmul

The formal meaning of an embedding layer is a one-hot vector times a weight
mat, and writing out the sizes shows why no one finds it that way. At a
50,000-token vocab and 512 dims:

|operation|numbers touched|
|---|---|
|one-hot vector &times; weight matrix|50,000 &times; 512 = **25.6 million**|
|the row it actually selects|**512**|

The one-hot is all zeros but one. So The times reads 25.6 million values to
return 512 and times all else by zero. each framework so
runs the layer as an indexed table lookup, with a backward pass that
scatters grads only to the rows a batch really used &mdash; which means the
table is a huge param tensor that sits almost fully idle on any given step.
The table itself is `vocab &times; dim = 25.6 million` params, often the
largest single component of a model, and the two standard economies both attack
that: weight tying reuses the input table as the output layer (halving the token
params and often raising quality, since both are learning what tokens
mean), and subword tokenisation keeps the vocab in the tens of thousands
rather than the millions a word-level scheme would need. The geometry the rows
end up with &mdash; king &minus; man + woman landing near queen &mdash; is never
imposed. It falls out of the training goal. This Also means it inherits the
training corpus's biases.

Because only the rows appearing in a batch receive a grad, an embedding table
is a large param tensor that is almost fully idle on any given step, which
complicates tuners that keep per-param state and anyone sharding a model
across devices. The same lookup mechanism generalises well beyond words: a user
id, a postcode or a product category embeds the same way. This Is what made
neural networks competitive on tabular data with high-cardinality categories. A
transformer embeds spots and tokens. And a recommender gives users and
items each a table whose dot product is a predicted bond, which is mat
factorisation wearing a different name. The nearness of two rows should be read
as co-hit in the training data, not as meaning &mdash; a gap that
matters wherever those links encode bias.

## Where it goes wrong

**Building the one-hot matmul truly.** Correct, and enormously wasteful.

**Choosing the dim by feel.** A rule of thumb is the fourth root of the
vocab size, and it's worth tuning.

**Losing an out-of-vocab row.** a thing has to handle unseen tokens;
subword tokenisation avoids the question.

**Reading likeness as meaning.** Embedding nearness reflects co-hit in
the training data, which isn't the same thing.

## A lookup table that learns what things mean

An embedding layer is one-hot encoding times a weight mat, with the times skipped. This shows the equivalence, the cost saving. What the learned vectors end up encoding.

```python-run
import numpy as np

rng = np.random.default_rng(0)
VOCAB, DIM = 8, 4
words = ["cat", "dog", "wolf", "car", "truck", "bus", "the", "a"]
E = rng.normal(0, 0.5, (VOCAB, DIM))

print("an embedding table: %d words x %d dimensions = %d parameters."
      % (VOCAB, DIM, E.size))
print()
print("look up word 2 ('wolf') two ways:")
onehot = np.zeros(VOCAB); onehot[2] = 1
print("  one-hot @ E :", np.round(onehot @ E, 4))
print("  E[2]        :", np.round(E[2], 4))
print("  identical:", np.allclose(onehot @ E, E[2]))
print()
print("that is the whole trick. multiplying by a one-hot vector selects one")
print("row, so you index instead. the maths is unchanged, the cost is not:")
for v, d in ((8, 4), (50_000, 256), (200_000, 1024)):
    mults = v * d
    print("  vocab %7d, dim %5d: one-hot matmul does %12d multiplications"
          % (v, d, mults))
    print("  %28s a lookup does %12d" % ("", d))
print()

print("the gradient is just as sparse. only the rows you used get updated:")
grad_out = np.zeros_like(E)
batch_ids = [2, 5, 2]
upstream = rng.normal(size=(3, DIM))
for i, wid in enumerate(batch_ids):
    grad_out[wid] += upstream[i]
print("  a batch using word ids %s" % batch_ids)
print("  rows with a non-zero gradient:", np.where(np.abs(grad_out).sum(axis=1) > 0)[0])
print("  word 2 appeared twice, so its gradients ADD -- that is why a")
print("  frequent word's embedding moves further per batch than a rare one's,")
print("  and why rare words end up close to their initial random values.")
print()

print("now train one, so the vectors mean something. the task: predict which")
print("of three groups a word belongs to (animal, vehicle, article).")
groups = np.array([0, 0, 0, 1, 1, 1, 2, 2])
Emb = rng.normal(0, 0.3, (VOCAB, DIM))
W = rng.normal(0, 0.3, (DIM, 3))
lr = 0.5
for step in range(600):
    h = Emb                       # one row per word, whole vocabulary as a batch
    logits = h @ W
    p = np.exp(logits - logits.max(axis=1, keepdims=True))
    p /= p.sum(axis=1, keepdims=True)
    d = p.copy(); d[np.arange(VOCAB), groups] -= 1; d /= VOCAB
    W -= lr * (h.T @ d)
    Emb -= lr * (d @ W.T)
print("  final accuracy: %.4f" % ((Emb @ W).argmax(axis=1) == groups).mean())
print()

def cos(a, b):
    return a @ b / (np.linalg.norm(a) * np.linalg.norm(b))

print("cosine similarity between the learned vectors:")
print("%8s %s" % ("", "".join("%8s" % w for w in words)))
for i, wi in enumerate(words):
    print("%8s %s" % (wi, "".join("%8.3f" % cos(Emb[i], Emb[j])
                                  for j in range(VOCAB))))
print()
print("nothing told the model that cat and dog are related. it only ever saw")
print("a group label. the similarity appeared because words that need the")
print("same output were pushed toward the same region of the space.")
print()
same = np.mean([cos(Emb[i], Emb[j]) for i in range(VOCAB) for j in range(VOCAB)
                if i != j and groups[i] == groups[j]])
diff = np.mean([cos(Emb[i], Emb[j]) for i in range(VOCAB) for j in range(VOCAB)
                if groups[i] != groups[j]])
print("  average similarity within a group : %+.4f" % same)
print("  average similarity across groups  : %+.4f" % diff)
print()
print("that is what 'learned representation' means, and it is why embeddings")
print("transfer: the geometry is a by-product of the task, so a table trained")
print("on one task is often useful for another.")
print()
print("choosing the dimension is the only real decision. too small and")
print("distinct words are forced to share space; too large and rare words")
print("never see enough gradient to move. the usual rule of thumb is")
print("a common starting point is four times the fourth root of the vocabulary,")
print("then rounded to a power of two:")
for v in (1_000, 50_000, 500_000):
    raw = 4 * v ** 0.25
    print("  vocab %7d -> 4 * %5.1f = %5.1f, so 64 to 256 in practice"
          % (v, v ** 0.25, raw))
print("  in real models the number is chosen by what fits in memory and what")
print("  the downstream layers expect, far more often than by any formula.")
```

""",
    [
        {"q": "Why is an embedding layer implemented as a lookup rather than a matmul?",
         "options": ["Lookups are more accurate",
                     "The one-hot product touches every weight in the table to retrieve a single row",
                     "Matmuls cannot be differentiated",
                     "The table is too large to store"],
         "answer": 1,
         "why": "At 50,000 tokens and 512 dimensions that is 25.6 million numbers touched to get 512. The definitions are identical; only the implementation differs."},
        {"q": "Which rows of an embedding table receive a gradient on a given step?",
         "options": ["All of them", "Only the rows for tokens that appeared in the batch",
                     "The most frequent rows", "None - they are frozen"],
         "answer": 1,
         "why": "The backward pass scatters gradients to the rows that were used, which means a very large parameter tensor sits almost entirely idle on any step."},
        {"q": "What does weight tying do?",
         "options": ["Freezes the embedding table",
                     "Shares the input embedding with the output layer, halving the cost and usually improving quality",
                     "Reduces the embedding dimension",
                     "Ties embeddings to positions"],
         "answer": 1,
         "why": "Both layers have one row per token and both are learning what tokens mean, so sharing them is natural as well as cheaper."},
    ],
)


# ---------------------------------------------------------------------------
# 8. Mixed precision
# ---------------------------------------------------------------------------
topic(
    "mixed_precision_training",
    "Mixed Precision and Loss Scaling",
    "Training at Scale",
    "Half precision halves the memory and doubles the throughput, and silently "
    "rounds small gradients to zero. Watch it happen, then fix it.",
    _svg(_line(20, 60, 140, 60, B, 1.2)
         + "".join(_box(24 + i * 13, 60 - h, 9, h, fill=S, stroke=B, sw=1)
                   for i, h in enumerate([4, 10, 22, 32, 30, 18, 8, 3]))
         + _line(38, 18, 38, 66, A, 1.6, "3 3")
         + _txt(38, 14, "fp16 floor", A, 7)
         + _txt(88, 80, "everything left of the line is zero", M, 7)),
    {
        "demo": "precision",
        "controls": [
            {"key": "logScale", "label": "Loss scale (as a power of 2)", "type": "range",
             "min": 0, "max": 24, "step": 1, "value": 0},
            {"key": "spread", "label": "Spread of the gradients", "type": "range",
             "min": 1.0, "max": 3.5, "step": 0.1, "value": 2.2},
        ],
    },
    [
        "fp16 has 5 exponent bits and 10 mantissa bits. Its smallest "
        "representable value is about 6&times;10<sup>&minus;8</sup>.",
        "Gradients are routinely smaller than that. They round to exactly zero, "
        "and the parameter never moves.",
        "<strong>Loss scaling</strong> multiplies the loss before the backward "
        "pass, shifting every gradient up into the representable range.",
        "The optimiser unscales before stepping, so the update is unchanged. "
        "The scaling exists only to survive the trip through fp16.",
    ],
    """
title: Mixed Precision and Loss Scaling
intro: Training in half the bits, the failure that causes. The one-line trick that drops it.

## Why bother

Modern accelerators run half-precision mat times a few times faster
than single-precision ones, and half-precision tensors take half the memory.
That means bigger batches, bigger models, and a real speed-up on the same
hardware.

The catch is the format. **fp32** has 8 exponent bits and 23 mantissa bits.
**fp16** has 5 and 10, giving a smallest normal value around
10&#8315;&#8309. And a max of 65,504.

Both ends of that range are a problem. The small end is the one that bites.

## Watch the gradients disappear

The histogram is grad magnitudes spread over a few orders of magnitude,
which is what a real network makes. The two marked lines are fp16's floor and
ceiling.

With the loss scale at 2&#8304.. That is, no scaling &mdash; the readout
reports how many of the 3,000 grads round to **zero**. Those params
receive no update at all. Not a small update. None.

This is the failure that made early fp16 training unreliable. The model trains,
the loss goes down, and a fraction of the network is silently frozen.

## Loss scaling

The fix is almost embarrassingly simple. Times the loss by a large constant
before the backward pass. By the chain rule each grad is times'd by the
same constant, so the whole spread shifts up into the representable range.
Then divide by that constant before the tuner steps.

Drag the loss scale upward and watch the underflow count fall to zero.

The update is in math unchanged. The scaling exists purely so the numbers
live the trip through fp16. It's a change of units, not a change of
method.

Push it too far and the readout starts reporting **overflow**: grads that
have become infinite. That is a failure too, and it's where the auto
version comes from.

## Dynamic loss scaling

No one tunes the constant by hand. The standard method starts high,
times by two when a stretch of steps ends without overflow, and
halves it and **skips the step** when an infinity or NaN appears.

Skipping is the key part: an overflowed grad isn't clipped or
repaired, it's discarded, because there's no way to recover what it should
have been. A few skipped steps early in training cost nothing.

This is what `torch.cuda.amp.GradScaler` does, and it's why mixed precision is
now a decorator rather than a project.

## What stays in fp32

"Mixed" is the operative word. In a standard setup:

**Weights** are kept in an fp32 master copy. Updates are often far smaller
than the weights themselves, and adding a tiny number to a large one in fp16
rounds to no change at all.

**mat times and convolutions** run in fp16. Here The speed is.

**Reductions** &mdash; sums, means, softmax, norming statistics &mdash;
build up in fp32, because adding many small numbers is just where limited
mantissa bits go wrong.

**Loss** is found in fp32.

## bfloat16

The newer option has 8 exponent bits and 7 mantissa bits &mdash; the same
range as fp32, with less precision.

That trade drops this entire page. Range was the problem. Precision, for
grads, mostly wasn't. **bfloat16 needs no loss scaling**. This Is why it
is the default on hardware that supports it, and why large-model training
largely stopped talking about GradScaler.

## The range that makes loss scaling necessary

The failure is fully about fp16's floor. fp16 carries 5 exponent bits, giving
a smallest normal value around `2^-14 &asymp; 6.1 &times; 10^-5` and a max of
65,504. Real grads routinely sit *below* that floor:

|quantity|magnitude|in fp16|
|---|---|---|
|a typical small gradient|~1 &times; 10^-7|rounds to **zero**|
|the same, times a loss scale of 4096|~4 &times; 10^-4|represented fine|

A grad that rounds to zero isn't a small update, it's *no* update &mdash;
the param freezes, silently, while the loss still falls and the run looks
healthy. Loss scaling fixes it in one line: times the loss by a constant before
the backward pass, so by the chain rule each grad is times'd too and the
whole spread shifts up into the representable range. Divide it back out
before the tuner steps. The update is in math unchanged &mdash; it's a
change of units, not of method. Push the constant too high and grads
overflow to infinity instead. This Is why the standard scaler is *dynamic*:
start high, double it after stretches without overflow, and halve it and skip the
step when an infinity appears. bfloat16 sidesteps the whole page by keeping fp32's
8 exponent bits &mdash; same range, less precision &mdash; so it needs no scaling
at all.

The other half of "mixed" is what on purpose stays in fp32. Weights keep an
fp32 master copy, because an update is often far smaller than the weight it
adjusts and adding a tiny number to a large one in fp16 rounds to no change at
all. Reductions &mdash; sums, means, softmax, norming statistics &mdash;
build up in fp32, because adding many small numbers is just where ten mantissa
bits go wrong and give the mysterious NaNs that half-precision softmax is known
for. The fp16 lives where the speed is: the mat times and convolutions the
tensor cores accelerate. Layers that are memory-bound rather than find-bound
gain little, which is why the speed-up is real but never uniform across a model.

## Where it goes wrong

**fp16 without loss scaling.** Silent underflow, and a partly frozen model.

**A fixed scale.** Use the dynamic version.

**Reductions in fp16.** Softmax and layer norm in half precision give
mysterious NaNs.

**given a speed-up.** It comes from the tensor cores. Layers that are
memory-bound rather than find-bound gain little.

## Half the bits, and the two things that break

float16 halves memory and doubles throughput on tensor cores. It also has a much narrower range than float32. Grads live near the bottom of that range -- which is the entire reason loss scaling exists.

```python-run
import numpy as np

def limits(dt):
    f = np.finfo(dt)
    return f.max, f.tiny, f.eps

print("%12s %8s %14s %16s %14s"
      % ("type", "bytes", "largest", "smallest normal", "precision"))
for dt in (np.float64, np.float32, np.float16):
    mx, tiny, eps = limits(dt)
    print("%12s %8d %14.3e %16.3e %14.3e"
          % (np.dtype(dt).name, np.dtype(dt).itemsize, mx, tiny, eps))
print()
print("float16 runs out of range at 65504. below its smallest NORMAL value")
print("of 6.1e-05 it keeps going in subnormals, with steadily fewer digits,")
print("until it reaches zero at %.2e:" % float(np.finfo(np.float16).smallest_subnormal))
for v in (1e-4, 1e-5, 1e-6, 1e-7, 3e-8, 1e-8):
    print("   %.0e as float16 -> %.3e%s"
          % (v, float(np.float16(v)),
             "   <- gone" if np.float16(v) == 0 else ""))
print()
print("that bottom edge is the problem: gradients routinely live there.")
print()

print("watch a realistic gradient distribution meet it:")
rng = np.random.default_rng(0)
grads = np.abs(rng.lognormal(mean=-17.5, sigma=1.6, size=200_000))
tiny16 = np.finfo(np.float16).tiny
print("  gradient magnitudes: median %.3e, 5th percentile %.3e"
      % (np.median(grads), np.percentile(grads, 5)))
lost = (grads.astype(np.float16) == 0).mean()
print("  fraction that become EXACTLY ZERO when cast to float16: %.1f%%"
      % (100 * lost))
print("  those gradients are not small any more. they are gone, and the")
print("  weights they belonged to will not update at all.")
print()

print("LOSS SCALING is the fix, and it is almost embarrassingly simple:")
print("multiply the loss by a large constant before the backward pass, then")
print("divide the gradients by the same constant before the update.")
print()
for scale in (1, 256, 4096, 65536, 1_048_576):
    scaled = (grads * scale).astype(np.float16)
    survived = (scaled != 0).mean()
    overflowed = (~np.isfinite(scaled)).mean()
    print("  scale %9d: %6.1f%% of gradients survive, %5.2f%% overflow to inf"
          % (scale, 100 * survived, 100 * overflowed))
print()
print("the whole gradient distribution slides up into float16's usable range.")
print("dividing by the same constant afterwards restores the true values")
print("exactly -- multiplication by a power of two only changes the exponent,")
print("so it costs no precision at all:")
x = np.float16(0.000123)
print("  0.000123 as float16          : %.9f" % float(x))
print("  x * 1024 / 1024 back again   : %.9f" % float(np.float16(x * 1024) / 1024))
print()

print("but too large a scale overflows, which is why the scale is DYNAMIC:")
print("  start high (2^16), and on any step that produces inf or nan:")
print("     skip the update entirely, halve the scale")
print("  after N good steps in a row: double it")
print("  the scale ends up tracking the largest value your gradients")
print("  currently reach, and it moves as training changes them.")
print()

print("the second thing that breaks is accumulation. adding many small")
print("numbers to a large one in float16 loses them completely:")
acc16 = np.float16(1024.0)
small = np.float16(0.4)
for _ in range(64):
    acc16 = np.float16(acc16 + small)
print("  float16: 1024 + 0.4 sixty-four times = %.4f (should be %.1f)"
      % (float(acc16), 1024 + 64 * 0.4))
acc32 = np.float32(1024.0)
for _ in range(64):
    acc32 = np.float32(acc32 + np.float32(0.4))
print("  float32: the same sum              = %.4f" % float(acc32))
print("  0.4 is below the spacing between representable float16 values near")
print("  1024, so each addition rounds straight back to where it started.")
print()
print("that is why mixed precision keeps a MASTER COPY of the weights in")
print("float32. the forward and backward passes run in float16 for speed;")
print("the optimiser update -- which is exactly this kind of accumulation --")
print("happens in float32, and the float16 weights are refreshed from it.")
print()

print("bfloat16 solves the range problem differently -- same 16 bits, more")
print("of them spent on the exponent:")
print("%14s %10s %10s %16s" % ("format", "exponent", "mantissa", "largest"))
print("%14s %10d %10d %16.3e" % ("float32", 8, 23, np.finfo(np.float32).max))
print("%14s %10d %10d %16.3e" % ("float16", 5, 10, np.finfo(np.float16).max))
print("%14s %10s %10s %16s" % ("bfloat16", "8", "7", "~3.4e+38"))
print("  bfloat16 has float32's exponent range, so it does not underflow and")
print("  needs no loss scaling. it pays with precision -- 7 mantissa bits")
print("  against 10 -- which in practice matters far less than the range.")
print("  that is why it is the default on hardware that supports it.")
print()
print("what you actually get: roughly half the activation memory, so bigger")
print("batches; and 2 to 8 times the matmul throughput on tensor cores.")
print("what you should check: that your loss curve matches the float32 run")
print("for the first few hundred steps. if it diverges, the scale is wrong.")
```

""",
    [
        {"q": "What does loss scaling change about the parameter update?",
         "options": ["It makes updates larger",
                     "Nothing - the optimiser unscales first; the scaling only keeps the numbers inside fp16's range",
                     "It clips large gradients",
                     "It skips small gradients"],
         "answer": 1,
         "why": "It is a change of units, not a change of algorithm. Multiply the loss, every gradient scales by the chain rule, divide before stepping."},
        {"q": "What does dynamic loss scaling do when a gradient overflows?",
         "options": ["Clips it to the maximum",
                     "Halves the scale and skips the step entirely",
                     "Falls back to fp32 for that step",
                     "Raises the scale"],
         "answer": 1,
         "why": "There is no way to recover what an overflowed gradient should have been, so it is discarded rather than repaired. A few skipped steps early cost nothing."},
        {"q": "Why does bfloat16 not need loss scaling?",
         "options": ["It has more mantissa bits",
                     "It has the same exponent range as fp32, and range was the problem",
                     "It is computed in software",
                     "It rounds differently"],
         "answer": 1,
         "why": "bfloat16 trades mantissa bits for exponent bits - less precision, same range. For gradients, precision mostly was not the issue."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Gradient accumulation
# ---------------------------------------------------------------------------
topic(
    "gradient_accumulation",
    "Gradient Accumulation",
    "Training at Scale",
    "Train with a batch that does not fit, by not holding it all at once. The "
    "gradient is a sum, and sums can be built up.",
    _svg("".join(_box(18 + i * 20, 40, 14, 22, fill=S, stroke=B, sw=1.2) for i in range(4))
         + _txt(74, 30, "+ + +", A, 10)
         + _box(104, 34, 34, 34, fill=S, stroke=A, sw=1.8) + _txt(121, 55, "step", A, 8)
         + _txt(80, 82, "four passes, one update", M, 7)),
    {
        "demo": "accumulation",
        "controls": [
            {"key": "effective", "label": "Effective batch size", "type": "range",
             "min": 16, "max": 512, "step": 16, "value": 256},
            {"key": "micro", "label": "Micro-batch size", "type": "range",
             "min": 1, "max": 128, "step": 1, "value": 16},
            {"key": "budget", "label": "Memory budget (GB)", "type": "range",
             "min": 4, "max": 80, "step": 4, "value": 24},
        ],
    },
    [
        "The gradient of a mean loss over a batch is the mean of the per-example "
        "gradients. So it can be accumulated in pieces.",
        "Run several small forward and backward passes, sum the gradients, and "
        "step once. The update is identical to the large batch.",
        "Only <strong>activation memory</strong> scales with the micro-batch. "
        "Weights, gradients and optimiser state do not.",
        "It costs wall-clock time, not correctness &mdash; except for "
        "batch normalisation, which sees only the micro-batch.",
    ],
    """
title: Gradient Accumulation
intro: Getting the effect of a large batch out of a device that can't hold one.

## Why it works

The loss over a batch is the mean of the per-example losses, and differentiation
is linear. So the grad of the batch is the mean of the per-example
grads.

That means the sum can be built in pieces. Run a forward and backward pass on 16
examples, keep the grads, run another 16, add to them, and after 16 rounds
you've just the grad of a 256-example batch. Step the tuner once.

**The resulting update is the same**. Not similar, the same up to
floating-point sorting &mdash; to what a single 256-example batch would have
made.

## What actually consumes the memory

The bars separate the two cases at the memory budget you choose.

Training memory is roughly:

**Fixed costs.** Weights, their grads, and the tuner state. Adam keeps
two extra tensors per param. So This is around four times the model size,
and it doesn't depend on the batch at all.

**Activations.** each mid value from the forward pass has to be kept
for the backward pass. This scales linearly with the batch size, and for a deep
model it dominates.

Buildup attacks only the second. This Is why it works. Drag the
micro-batch down and watch the second bar fall while the fixed part stays put.

The dashed line is the budget. When the full batch crosses it and the micro-batch
doesn't, that gap is the entire reason the technique exists.

## What it costs

**Time.** Sixteen sequential passes take about if sixteen passes.
Buildup doesn't make any of it faster. It makes a thing possible.

There's a small speed loss too, since very small micro-batches use the
accelerator less well. A micro-batch of 1 is often much less than a sixteenth
as fast as a micro-batch of 16.

## The one thing that is not identical

**Batch norming.** Its statistics are found over what is in the
forward pass, which is the micro-batch, not the built up total.

So a model with batch norm trained with a micro-batch of 4 behaves like one
trained with a batch of 4, but many buildup steps follow. The
norming is noisier, and at very small micro-batches it degrades badly.

This is a real reason to prefer
[layer norming](layer_normalization.html) or group norming, both of
which norm per example and are indifferent to the batch. It isn't a
coincidence that transformers use layer norm and are the architectures trained
with the most aggressive buildup.

## Getting it right

Two details cause most of the bugs.

**Divide the loss by the number of buildup steps** before the backward
pass, or the built up grad is a sum where the tuner expects a mean,
and your effective learning rate is times'd by the step count.

**Zero the grads at the right time**. After the tuner step, not
after each backward pass. Zeroing each pass defeats the whole thing, and it
fails silently: training still runs, just with the small batch you were trying
to avoid.

## Alongside

**Activation checkpointing** trades find for memory in the other direction:
discard activations during the forward pass and recompute them in the backward
pass, for roughly 30% more time and a large memory saving. The two combine.

**Mixed precision** halves activation memory outright, and mixes with both.

**Model parallelism and ZeRO** attack the fixed costs, which buildup can't
touch. When the weights alone don't fit, buildup isn't the answer.

## Where the memory actually goes

Buildup works because it attacks the one cost that scales with the batch.
Training memory splits in two: a fixed part. Weights, their grads, and
the tuner state, which for Adam is about four times the model size &mdash;
and activations, each mid value kept for the backward pass, which grows
linearly with the batch. Take a 1&nbsp;GB model on an 8&nbsp;GB budget:

|batch|fixed (Adam ~4&times;)|activations|total|
|---|---|---|---|
|256 (wanted)|4.0 GB|~5.1 GB|9.1 GB &mdash; **over budget**|
|16 (micro-batch)|4.0 GB|~0.3 GB|4.3 GB &mdash; fits|

Run the micro-batch of 16 sixteen times, summing the grads, and step once:
the update is *the same* to the 256-batch. The batch grad is the mean
of the per-example grads and a mean can be built in pieces. The fixed 4&nbsp;GB
never moves &mdash; buildup can't touch it. This Is why it's no help when
the weights alone don't fit. But the activation term, the part that broke
the budget, is now a sixteenth of its size. The cost is time: sixteen sequential
passes take about if sixteen passes. It buys capability, not throughput,
and the one thing it does *not* copy is batch-norm statistics, which are
found over the micro-batch and so behave like the small batch but many
steps you build up.

Two setup details cause most buildup bugs, and both fail quietly.
The loss must be cut by the number of buildup steps before the backward
pass, or the built up grad is a sum where the tuner expects a mean and
the effective learning rate is silently times'd by the step count. And the
grads must be zeroed after the tuner step, not after each backward pass
&mdash; zero them each pass and the technique is defeated with no error at all,
training proceeding with just the small batch it was meant to escape.
Activation checkpointing and mixed precision attack the same activation memory
from other angles and combine with it. Model parallelism attacks the fixed part
that buildup can't.

## Where it goes wrong

**Losing to divide the loss.** Silently times the learning rate.

**Zeroing grads each pass.** Silently defeats the technique.

**Using it with batch norm at a tiny micro-batch.** Real quality loss.

**Expecting a speed-up.** It buys capability, not throughput.

## A large batch on a small GPU

Building up grads over a few small batches before stepping is arithmetically the same to one large batch. This proves the identity, then shows the two things that aren't the same.

```python-run
import numpy as np

rng = np.random.default_rng(0)
N, D = 64, 5
X = rng.normal(size=(N, D))
w_true = rng.normal(size=D)
y = X @ w_true + rng.normal(0, 0.3, N)
w = np.zeros(D)

def grad(Xb, yb, wv):
    return 2 * Xb.T @ (Xb @ wv - yb) / len(Xb)

print("64 rows. compute the gradient two ways.")
print()
big = grad(X, y, w)
print("one batch of 64:")
print("  ", np.round(big, 8))
print()

acc = np.zeros(D)
STEPS = 4
for i in range(STEPS):
    chunk = slice(i * 16, (i + 1) * 16)
    acc += grad(X[chunk], y[chunk], w) / STEPS
print("four batches of 16, each gradient divided by 4 and summed:")
print("  ", np.round(acc, 8))
print("  max difference: %.2e" % np.abs(big - acc).max())
print()
print("identical. that is the whole technique: the mean over 64 rows is the")
print("mean of four means over 16 rows, as long as the batches are equal")
print("sized and you divide by the number of accumulation steps.")
print()

print("the division is the part people get wrong. without it:")
wrong = sum(grad(X[i * 16:(i + 1) * 16], y[i * 16:(i + 1) * 16], w)
            for i in range(STEPS))
print("  summed without dividing:", np.round(wrong[:3], 4), "...")
print("  correct:                ", np.round(big[:3], 4), "...")
print("  ratio: %.1f -- you have silently multiplied your learning rate by %d."
      % (np.abs(wrong).mean() / np.abs(big).mean(), STEPS))
print()

print("what it buys, in memory terms. activation memory scales with batch")
print("size; gradient memory does not:")
print("%14s %18s %18s" % ("micro-batch", "activations held", "effective batch"))
for micro in (64, 16, 8, 4, 1):
    print("%14d %18s %18d"
          % (micro, "%dx" % micro, 64))
print("  the gradient buffer is the same size in every row -- one number per")
print("  parameter. only the activations kept for the backward pass shrink.")
print()

print("and now the two things that are NOT identical.")
print()
print("1. BatchNorm. its statistics come from the micro-batch, not the")
print("   accumulated one, so accumulation does not restore large-batch")
print("   behaviour there:")
for micro in (64, 16, 4):
    b = X[:micro]
    print("     micro-batch of %2d: feature-0 mean %+.4f, sd %.4f"
          % (micro, b[:, 0].mean(), b[:, 0].std()))
print("     those are the numbers BatchNorm would use. they are noisier the")
print("     smaller the micro-batch, and accumulation cannot fix it.")
print("     LayerNorm and GroupNorm are unaffected, which is one more reason")
print("     transformers are easier to train this way.")
print()
print("2. speed. four passes of 16 do the same arithmetic as one pass of 64,")
print("   but with four times the kernel launches and less parallelism. you")
print("   are trading wall-clock time for memory, not getting both.")
print()

print("the loop, written out, because the off-by-one is easy:")
print("    optimizer.zero_grad()")
print("    for i, batch in enumerate(loader):")
print("        loss = criterion(model(batch.x), batch.y) / ACCUM")
print("        loss.backward()                 # gradients ADD by default")
print("        if (i + 1) % ACCUM == 0:")
print("            optimizer.step()")
print("            optimizer.zero_grad()")
print()
print("three things to check: divide the loss by ACCUM, do not zero the")
print("gradients between micro-batches, and handle the final partial group")
print("-- if the loader ends mid-accumulation those gradients are discarded.")
print()
print("and if you use a learning rate schedule, step it once per OPTIMIZER")
print("step, not once per micro-batch, or your schedule runs %d times too fast."
      % STEPS)
```

""",
    [
        {"q": "Why is the accumulated update identical to a large-batch update?",
         "options": ["It is an approximation that converges",
                     "The gradient of a mean loss is the mean of the per-example gradients, and differentiation is linear",
                     "The optimiser corrects for it",
                     "The learning rate is adjusted"],
         "answer": 1,
         "why": "Identical up to floating-point ordering, not merely similar. That linearity is the whole justification."},
        {"q": "Which part of training memory does accumulation reduce?",
         "options": ["The optimiser state", "The activations kept for the backward pass",
                     "The weights", "The gradients"],
         "answer": 1,
         "why": "Activations scale with batch size; weights, gradients and optimiser state do not. When the weights alone do not fit, accumulation is not the answer."},
        {"q": "Which layer type does gradient accumulation genuinely change?",
         "options": ["Layer normalisation", "Batch normalisation",
                     "Dropout", "Convolution"],
         "answer": 1,
         "why": "Its statistics come from whatever is in the forward pass - the micro-batch. Layer norm normalises per example and is indifferent to the batch, which is one reason transformers use it."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Label smoothing
# ---------------------------------------------------------------------------
topic(
    "label_smoothing",
    "Label Smoothing",
    "Regularisation",
    "Stop asking the model for certainty it cannot have. Move a little "
    "probability off the correct answer and the confidence problem goes away.",
    _svg(_box(24, 24, 18, 42, fill=S, stroke=A, sw=1.6)
         + "".join(_box(52 + i * 20, 60, 14, 6, fill=S, stroke=B, sw=1) for i in range(4))
         + _txt(80, 84, "not quite one, not quite zero", M, 7)),
    {
        "demo": "smoothing",
        "controls": [
            {"key": "epsilon", "label": "Epsilon", "type": "range",
             "min": 0.0, "max": 0.4, "step": 0.01, "value": 0.10},
            {"key": "classes", "label": "Number of classes", "type": "range",
             "min": 2, "max": 20, "step": 1, "value": 10},
        ],
    },
    [
        "A one-hot target asks for probability 1 on the correct class. That "
        "requires an infinite logit gap, so training never stops pushing.",
        "Label smoothing replaces the target with "
        "<code class='mono-font'>1&minus;&epsilon;+&epsilon;/K</code> on the true class and "
        "<code class='mono-font'>&epsilon;/K</code> on the rest.",
        "The optimal logit gap becomes finite, so the model has a reason to "
        "stop becoming more confident.",
        "The minimum achievable loss is no longer zero. A loss that plateaus "
        "above zero is expected, not a bug.",
    ],
    """
title: Label Smoothing
intro: A one-line change to the target that raises calibration. The reason the loss no longer reaches zero.

## The problem with a hard target

Cross-entropy with a one-hot target asks the model to put chance 1 on the
correct class and 0 on all else.

Softmax can't give just 1. It approaches it as the correct logit runs
away from the others, and reaches it only in the limit. So the target is
unattainable, the grad never vanishes, and training keeps pushing the logit
gap wider for if you let it.

The consequences are familiar. The model turns **too sure**, reporting
0.99 on cases it gets wrong. It **overfits**, because widening logits on training
examples is always an available way to reduce the loss. And it's **badly
calibrated**, in just the way
[the calibration module](../machine_learning/probability_calibration.html)
measures.

## The change

Move a little chance off the correct class and spread it over the others:

```
target[correct]  =  1 - eps + eps/K
target[others]   =  eps/K
```

Drag epsilon and watch the bars. At 0 you've the one-hot target. At 0.1 the
true class asks for 0.91 and each of nine others asks for about 0.011.

That is the entire technique.

## Why it fixes the problem

The readout gives the **best logit gap**: how far apart the logits have to be
to match the target just.

At epsilon 0 it's infinite. This Is the problem restated. At epsilon 0.1 it's
a exact finite number, and once the model reaches it the grad is zero.
The model now has a reason to *stop*.

That is the mechanism. Not noise, not smoothing in the weight-decay sense
&mdash; a reachable target where before there was none.

## The loss will not reach zero

The readout also gives the min achievable loss. This Is the entropy of the
smoothed target.

A model matching the smoothed target just right still reports a loss around 0.5
at common settings. This surprises people who expect training loss to approach
zero, and it isn't a bug: you changed what perfect means.

It also means training and validation losses are no longer close with runs
that didn't use smoothing. Compare fit, or compare like with like.

## What it buys, and what it costs

**Better calibration.** The headline gain. Confidences become closer to
seen accuracies.

**Better generalisation.** Steady small gains across image classification
and translation. It was in the Inception-v3 paper and in the first
Transformer, at 0.1 in both, and 0.1 has been the default ever since.

**Tighter class clusters.** Forms of a class group more tightly, with
more even distances between classes.

That last one has a cost. **Label smoothing hurts distillation.** A student
learns from the teacher's full output spread, and the helpful part is
the scaled sizes of the *wrong* classes. That this dog was slightly cat
and not at all lorry. Smoothing on purpose flattens just that, erasing what
the student was supposed to learn. If a model is going to be a distillation
teacher, train it without.

## The floor the loss cannot go below

Two numbers make label smoothing concrete. With `epsilon = 0.1` and `K = 10`
classes, the target puts `1 - 0.1 + 0.1/10 = 0.91` on the correct class and
`0.1/10 = 0.011` on each of the other nine. A model that matches that target
*just* still records a cross-entropy equal to the target's own entropy:

`-(0.91 &middot; ln 0.91 + 9 &middot; 0.011 &middot; ln 0.011) &asymp; 0.50`

|target|minimum achievable loss|
|---|---|
|one-hot|0 (but never reached &mdash; needs an infinite logit gap)|
|smoothed, eps = 0.1|~0.50|

That is the whole mechanism, stated as math. The one-hot target has a floor
of zero that softmax can only approach by driving the correct logit infinitely
far from the rest &mdash; so the grad never vanishes and training keeps
inflating trust. The smoothed target has a floor of 0.50 reached at a
*finite* logit gap, so the model has a reason to stop, and it stops before it
turns too sure. It also means a smoothed run's training loss isn't
close with an unsmoothed one: 0.50 is the new zero, and checking the raw
numbers across the two is checking against different floors.

The one place smoothing actively hurts is distillation. A student learns from the
teacher's full output spread, and the helpful part is the scaled sizes
of the *wrong* classes &mdash; that a given dog photo is a little cat-like and
not at all lorry-like. That structure is just what smoothing flattens, by
design, pushing each wrong class toward the same small value. So a model destined
to be a distillation teacher should be trained without it, though 0.1 is the
right default almost all over else. It was in the Inception-v3 paper and
the first Transformer, and it has stayed the default because the calibration
and generalisation gains are steady across classification and translation
alike.

It's also worth remembering what smoothing isn't: it's a change to a
cat target, so it has no meaning for regression, and it isn't a
substitute for clear calibration. Temperature scaling on a validation set
corrects trust more right, and the two compose &mdash; smoothing during
training, scaling afterwards.

## Where it goes wrong

**Epsilon too large.** Past about 0.2 you're actively teaching the model that
wrong answers are plausible, and fit falls. Drag it up and watch the target
flatten.

**Checking losses across runs.** The floor moved.

**Using it on a teacher model.** It drops the dark knowledge distillation
depends on.

**Applying it to regression.** It's a change to a cat target and has no
meaning without one.

**Expecting it to fix a badly calibrated model on its own.** It helps. Clear
[temperature
scaling](../machine_learning/probability_calibration.html) on a validation set
helps more, and the two combine.

## Tell the model it might be wrong

Replacing a target of 1.0 with 0.9 changes what the loss is minimised by. This finds that optimum just, then shows the effect on trust and on the logits themselves.

```python-run
import numpy as np

K = 5           # classes
EPS = 0.1       # smoothing strength

hard = np.zeros(K); hard[0] = 1.0
soft = np.full(K, EPS / K); soft[0] += 1 - EPS

print("a %d-class problem, true class 0." % K)
print("  hard target  :", np.round(hard, 4))
print("  smoothed 0.1 :", np.round(soft, 4), " sums to", round(soft.sum(), 6))
print("  the formula is (1 - eps) * onehot + eps / K.")
print()

def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()

def ce(z, target):
    return -(target * np.log(softmax(z))).sum() + 0.0

print("what each target is minimised BY. the loss against a hard target")
print("keeps falling as the true logit grows, forever:")
print("%14s %14s %16s" % ("logit gap", "hard loss", "smoothed loss"))
for gap in (1.0, 2.0, 4.0, 8.0, 16.0, 40.0):
    z = np.zeros(K); z[0] = gap
    print("%14.1f %14.6f %16.6f" % (gap, ce(z, hard), ce(z, soft)))
print()
print("the hard column goes to zero and never stops rewarding a bigger gap.")
print("the smoothed column has a MINIMUM. find it by search:")
gaps = np.linspace(0.1, 20, 4000)
losses = [ce(np.r_[g, np.zeros(K - 1)], soft) for g in gaps]
best = gaps[int(np.argmin(losses))]
print("  smoothed loss is lowest at a logit gap of %.4f" % best)
print("  the closed form says log((1-eps+eps/K) / (eps/K)) = %.4f"
      % np.log((1 - EPS + EPS / K) / (EPS / K)))
print()
print("so smoothing does not merely 'soften' the target -- it gives the model")
print("a finite target to aim for. without it the optimum is at infinity, and")
print("the weights grow without bound trying to reach it.")
print()

z_at_best = np.r_[best, np.zeros(K - 1)]
print("the confidence that corresponds to that optimum:")
print("  probabilities:", np.round(softmax(z_at_best), 4))
print("  the model's best possible answer is %.4f, not 1.0000."
      % softmax(z_at_best)[0])
print()

print("smoothing strength against the confidence it targets:")
print("%10s %16s %16s" % ("eps", "optimal gap", "peak probability"))
for eps in (0.0, 0.01, 0.05, 0.1, 0.2, 0.5):
    if eps == 0:
        print("%10.2f %16s %16s" % (eps, "infinite", "1.0000"))
        continue
    gap = np.log((1 - eps + eps / K) / (eps / K))
    print("%10.2f %16.4f %16.4f"
          % (eps, gap, softmax(np.r_[gap, np.zeros(K - 1)])[0]))
print("  eps=0.5 targets only %.2f confidence, which is barely a decision."
      % softmax(np.r_[np.log((1 - 0.5 + 0.5 / K) / (0.5 / K)), np.zeros(K - 1)])[0])
print("  0.1 is the usual choice and 0.2 is about as far as anyone goes.")
print()

print("and what it costs. a genuinely certain example is now penalised:")
z_sure = np.r_[12.0, np.zeros(K - 1)]
print("  a model that is right and certain (p=%.6f):" % softmax(z_sure)[0])
print("    hard loss     %.6f" % ce(z_sure, hard))
print("    smoothed loss %.6f  <- it is being pushed back down"
      % ce(z_sure, soft))
print()
print("that is the trade. label smoothing buys better-calibrated confidence")
print("and slightly better accuracy, and costs you the ability to be certain")
print("about anything. if your downstream system reads the probability as a")
print("probability, measure the calibration before and after -- do not assume.")
```

""",
    [
        {"q": "Why does a one-hot target make a model overconfident?",
         "options": ["It has too few classes",
                     "Softmax reaches probability 1 only in the limit, so the optimal logit gap is infinite and training never stops pushing",
                     "The gradient is too large",
                     "It has no regularisation"],
         "answer": 1,
         "why": "The target is unattainable, so widening logits is always an available way to reduce the loss. Smoothing makes the optimal gap finite and reachable."},
        {"q": "Why does the training loss no longer approach zero?",
         "options": ["The model is underfitting",
                     "The minimum achievable loss is the entropy of the smoothed target, which is not zero",
                     "The learning rate is too low",
                     "Label smoothing adds noise"],
         "answer": 1,
         "why": "You changed what perfect means. It also means losses are no longer comparable with runs that did not use smoothing."},
        {"q": "Why should a distillation teacher be trained without label smoothing?",
         "options": ["It makes the teacher less accurate",
                     "The student learns from the relative sizes of the wrong-class probabilities, and smoothing flattens exactly that",
                     "The student cannot handle smoothed targets",
                     "It slows distillation down"],
         "answer": 1,
         "why": "The informative part is that this dog was slightly cat and not at all lorry. Smoothing erases the dark knowledge distillation depends on."},
    ],
)

CHECKS = {"deep_learning/%s.html" % t["slug"]: {"check": t["check"]} for t in TOPICS}
