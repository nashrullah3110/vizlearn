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
intro: A network trained to reproduce its input, and why that pointless-sounding task is useful.

## The apparently useless task

An autoencoder has two halves. The **encoder** maps an input to a smaller
representation; the **decoder** maps it back. The loss is the difference between
the output and the input.

Copy the input to the output. Stated like that it sounds like a null task &mdash;
the identity function scores perfectly.

Except it cannot, because the representation in the middle is smaller than the
input. The network has to throw information away, and the training objective
forces it to throw away the least costly information. **What survives the
bottleneck is what the data was mostly made of.**

## Watch the squeeze

The grey line is the input; the orange line is what comes back out.

At a latent size of 1 the reconstruction keeps only the largest structure and
misses everything else. Raise it and the copy tightens. Past a certain point
extra dimensions buy almost nothing, because the remaining detail is noise
rather than signal.

That flattening is the useful observation: it says roughly how many numbers the
data really needs, which is its **intrinsic dimensionality**.

## The relationship to PCA

A linear autoencoder trained with squared error finds the same subspace as
[PCA](../machine_learning/pca.html). Not something similar &mdash; provably the
same span, though the individual directions need not be the principal
components in order.

So a linear autoencoder is PCA with extra steps. What makes them worth having is
**non-linearity**: with non-linear activations the encoder can learn a curved
manifold, which no linear projection can follow. An image dataset lives on a
wildly curved surface in pixel space, and that is the case where an autoencoder
earns its keep.

## Denoising

Raise the noise control. Now the input is corrupted and the target is still the
clean signal.

The reconstruction error against the *noisy* input goes up, and against the
*clean* signal it goes down. The readout gives both.

The reason is the bottleneck again. Noise is, by construction, the part of the
signal with no structure to compress, so a narrow code cannot afford to store
it. Forcing the network to reconstruct through the bottleneck forces it to
discard exactly what noise is.

**Denoising autoencoders** make this the training procedure: corrupt the input
deliberately, ask for the clean version. It also prevents the degenerate
solution where a wide code just learns the identity, which is why the trick
appears even when denoising is not the goal.

## What they are used for

**Dimensionality reduction** where the structure is non-linear.

**Anomaly detection.** Train on normal data; anything that reconstructs badly is
unlike what was seen. It works because the model has only learned to compress
one kind of thing.

**Pretraining.** Historically the standard way to initialise deep networks
before better initialisation and normalisation made it unnecessary.

**Generation** &mdash; but not directly. A plain autoencoder's latent space has
gaps, so a random code usually decodes to nothing meaningful. Fixing that is
what [the VAE](variational_autoencoders.html) is for.

## Where it goes wrong

**A bottleneck that is too wide.** With enough capacity the network learns the
identity and nothing is discovered. Constrain it, or use denoising, or add a
sparsity penalty.

**Expecting a usable generative model.** Sample from a plain autoencoder's
latent space and you will mostly get nonsense.

**Reading the reconstruction error as a quality score.** It measures pixel
agreement, not perceptual similarity, which is why autoencoder outputs look
blurred.

**Assuming the latent dimensions mean anything individually.** They are not
ordered or disentangled unless something in the training made them so.
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
intro: Turning an autoencoder into something you can sample from, and the two forces that have to be balanced to do it.

## The problem with a plain autoencoder

An [autoencoder](autoencoders.html) maps each input to a single point in the
latent space, and nothing organises those points. Nearby codes need not decode
to similar things, and the space between clusters is undefined territory.

So you cannot generate. Pick a random latent vector and decode it, and you
almost certainly land somewhere the decoder was never trained, and the output is
noise.

A VAE fixes this by making the latent space **continuous and bounded** &mdash;
by construction, not by hope.

## Encoding to a distribution

The encoder outputs a mean and a standard deviation rather than a point, and the
code is *sampled* from that distribution during training.

That single change does the work. Because the same input produces different
codes on different passes, the decoder must handle a whole neighbourhood, not a
point. Neighbourhoods overlap and the space fills in.

Drag the sigma control and watch the clusters spread. At small sigma you have a
plain autoencoder again, with tight clumps and gaps between them. At large sigma
the neighbourhoods swallow each other.

## The reparameterisation trick

There is an obstacle: you cannot backpropagate through a sampling operation.
Sampling is not a differentiable function of the parameters that produced the
distribution.

The trick is to move the randomness out of the path:

```
z  =  mu  +  sigma * epsilon        with epsilon ~ N(0, 1)
```

Now the random part, `epsilon`, is an input rather than an operation. The
gradient flows to `mu` and `sigma` normally, because with `epsilon` fixed the
expression is an ordinary differentiable function of them.

That is the whole trick, it is two lines of code, and VAEs were not trainable
without it. It reappears in other places where a sample must be differentiated
through &mdash; the Gumbel-softmax does the same job for discrete variables.

## Two terms in tension

```
loss  =  reconstruction error  +  KL( encoder distribution || prior )
```

The **reconstruction** term wants tight, well-separated codes: the easiest thing
to decode accurately.

The **KL** term wants every encoded distribution to look like the prior &mdash;
the dashed circle. It is what makes the space samplable, because if every code
looks like a draw from the prior then a draw from the prior looks like a code.

They pull against each other, and the readout names which is winning.

**KL winning** is *posterior collapse*: the encoder outputs the prior regardless
of input, the clusters merge, and the decoder ignores the latent entirely.
Raise sigma or lower the separation to see it.

**Reconstruction winning** gives tight clusters with empty space between them
&mdash; excellent reconstruction, and sampling lands in the gaps.

The usual control is **beta-VAE**, which weights the KL term explicitly. High
beta pushes towards disentangled but blurry; low beta towards sharp but not
samplable. Many implementations also *anneal* beta from zero, letting
reconstruction establish itself before the KL pressure arrives.

## Jensen, and where the loss comes from

That loss is not arbitrary. The quantity you actually want to maximise is
`log p(x)`, which contains an intractable integral over the latent.

[Jensen's inequality](../maths/jensens_inequality.html) converts it into a lower
bound &mdash; the **ELBO** &mdash; which decomposes into exactly the two terms
above. Maximising the bound cannot decrease the true likelihood, and the gap
between them is a KL divergence.

## Against GANs

VAEs give a principled objective, a meaningful latent space, stable training and
a likelihood bound. Their samples are **blurry**, because the pixel-wise
reconstruction term rewards hedging: when uncertain, the average of the
possibilities scores better than any single one.

[GANs](generative_adversarial_networks.html) produce sharp samples and are far
harder to train. Diffusion models have largely displaced both for image
generation, and the VAE survives inside them &mdash; latent diffusion runs the
diffusion process in a VAE's latent space rather than in pixels.

## Where it goes wrong

**Posterior collapse**, especially with a powerful decoder that can do well
without the latent. Anneal the KL, or weaken the decoder.

**Expecting sharp samples.** The blur is structural.

**Forgetting the reparameterisation trick.** Without it there is no gradient.

**Reading latent dimensions as meaningful.** A plain VAE is not disentangled;
beta-VAE encourages it and does not guarantee it.
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
intro: A generator and a critic pushed against each other, and the specific way that arrangement fails.

## The setup

Two networks, one loss.

The **generator** maps random noise to samples, trying to make them
indistinguishable from real data. The **discriminator** takes a sample and
estimates whether it is real, trying to be right.

They optimise the same objective in opposite directions. That makes it a
**minimax game**, and it is why GAN training is unlike anything else: there is
no loss that decreases, and a falling generator loss might mean the generator is
improving or the discriminator is losing.

## The second panel is not learned

For fixed real and generated distributions, the optimal discriminator has a
closed form:

```
D*(x)  =  p_real(x) / ( p_real(x) + p_fake(x) )
```

The lower panel plots exactly that. It is not a trained network; it is what
training drives towards, and its shape is what makes the failure mode legible.

## Where the gradient goes

Drag the generator's mean far from the real distribution. The overlap in the
readout collapses toward zero, and the discriminator's curve becomes flat
&mdash; near 1 where the real data lives, near 0 where the fakes are, with a
steep cliff between.

**Flat means no gradient.** The generator improves by following the slope of the
discriminator's opinion, and if that opinion is constant everywhere the fakes
live, there is nothing to follow. The better the discriminator, the worse this
gets, which is a genuinely awkward property: your generator's learning signal
degrades as its opponent improves.

Now bring the mean back. Where the distributions overlap the curve slopes, and
that slope is the generator's gradient.

At full overlap the discriminator sits at 0.5 everywhere &mdash; it cannot tell
them apart, which is the equilibrium the whole arrangement targets.

## The failures

**Vanishing gradients**, as above. The non-saturating loss helps; the deeper fix
was **Wasserstein GAN**, which replaces the classifier with a critic estimating
earth-mover distance. That distance is informative even for disjoint
distributions, so the gradient survives.

**Mode collapse.** The generator finds a narrow region that fools the
discriminator and stays there. Shrink the generator's spread until it is a
spike inside the real distribution: it is fooling the discriminator locally
while representing almost none of the data. Nothing in the objective directly
punishes this, because the discriminator judges samples one at a time and never
sees the lack of variety.

**Non-convergence.** The two can cycle indefinitely, each undoing the other.
Two-timescale learning rates, spectral normalisation and gradient penalties are
all responses to it.

**No usable progress metric.** The loss does not say whether samples are
improving. FID and Inception Score exist because of this, and both are proxies.

## Against the alternatives

**Sharp samples.** GANs produce them where
[VAEs](variational_autoencoders.html) blur, because nothing rewards averaging
&mdash; a hedged sample is exactly what the discriminator catches.

**No likelihood.** A GAN cannot say how probable a given sample is, which rules
out several uses.

**Hard to train**, as above.

[Diffusion models](diffusion_models.html) have largely displaced GANs for image
generation, trading sampling speed for training stability. GANs remain
competitive where inference must be a single forward pass, and the adversarial
idea itself survives everywhere &mdash; in domain adaptation, in perceptual
losses, in super-resolution.

## Where it goes wrong

**Reading the loss curves.** They mostly say who is winning, not whether the
samples are good. Look at samples.

**Letting the discriminator win.** A perfect discriminator gives no gradient.

**Ignoring mode collapse** because the samples look fine individually. Check the
variety, not the quality.

**Expecting a likelihood.** There is not one.
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
intro: Learning to reverse a process that is trivial to run forwards, and why that turned out to work so much better than the alternatives.

## Forwards is free

Take data and add a little Gaussian noise. Repeat. After enough steps nothing of
the original remains and you have pure noise.

This **forward process** has no parameters and nothing to learn. Better still, it
has a closed form: you can jump straight to any step without simulating the ones
before it.

```
x_t  =  sqrt(abar_t) * x_0  +  sqrt(1 - abar_t) * epsilon
```

`abar_t` is the fraction of the original signal still present, and it decreases
along a fixed **schedule**. The second panel plots the cosine schedule used
here, and the readout gives the signal and noise proportions at whatever step
you select.

That closed form is why training is cheap: pick a random `t`, jump there
directly, and train on that one step. No simulation.

## Backwards is the model

The generative process runs the other way: start from pure noise and undo one
step at a time until an image appears.

Each reverse step needs to know what noise was added, and that is the entire
learned component. The network takes `x_t` and `t` and predicts `epsilon`.

Given the noise, recovering the original is rearranging the equation above:

```
x_0  =  ( x_t  -  sqrt(1 - abar_t) * epsilon )  /  sqrt(abar_t)
```

The demonstration does exactly this with the *true* noise &mdash; the target the
model is trained on &mdash; and the readout gives the recovery error, which is
essentially zero at every step. **The forward process is exactly invertible if
you know the noise.** Predicting it is the whole job, and it is why the loss is
a plain squared error on a noise vector rather than anything adversarial.

## Why this beats what came before

**A stable objective.** Predicting noise is ordinary supervised regression. No
minimax game, no [discriminator to balance](generative_adversarial_networks.html),
no mode collapse. Training a diffusion model is boring in a way GAN training
never was, and that is the point.

**Coverage.** GANs can ignore parts of the distribution. A diffusion model is
trained to denoise every example, so it cannot quietly drop a mode.

**Sharpness.** Unlike a [VAE](variational_autoencoders.html), there is no
pixel-averaging term rewarding a blurred hedge.

The cost is **sampling speed**. Generation is many sequential passes &mdash;
originally a thousand, now often ten to fifty with a better sampler &mdash;
where a GAN needs one. DDIM and distillation methods have shortened this
considerably, and it remains the main disadvantage.

## The schedule matters

Drag `t` from 0 to 60 and watch how quickly the signal disappears. The original
DDPM used a linear schedule, which destroys the signal too fast at the end
&mdash; the last steps are all noise and contribute nothing to learning. The
cosine schedule shown here keeps more signal for longer and trains better.

Schedule design is a real part of the field, and so is the choice of what the
model predicts: the noise, the original, or a mixture called `v`, all of which
are algebraically equivalent and behave differently in practice.

## In practice

**Latent diffusion** runs the whole process in a
[VAE's](variational_autoencoders.html) latent space rather than in pixels,
cutting the cost enormously. Stable Diffusion is this.

**Classifier-free guidance** trains the model both with and without a text
condition, then extrapolates away from the unconditioned prediction at sampling
time. It is what makes prompts actually steer the output, and turning it up
trades diversity for prompt adherence.

## Where it goes wrong

**Expecting fast sampling.** It is the known weakness.

**A schedule that destroys the signal too early.** Wasted steps.

**Guidance turned up too high.** Saturated, oversimplified images and collapsed
diversity.

**Assuming the model predicts the image.** Most predict the noise, and confusing
the two makes the sampling code nonsense.
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
intro: Getting a useful representation out of unlabelled data by turning the data into its own supervision.

## The pretext

Labels are expensive and unlabelled data is not. Self-supervised learning
invents a task from the data itself, so that solving it requires understanding
the content.

The contrastive version is stark: take an image, produce two augmented views,
and require their representations to be close. Require every other image's views
to be far away.

If a model can recognise that a crop and a colour-jittered version of the same
photograph belong together, while distinguishing them from a thousand other
photographs, it has had to learn what the photograph is *of*.

## InfoNCE

The loss is a softmax over similarities:

```
loss  =  -log[  exp(sim(a, p) / tau)
              / ( exp(sim(a, p) / tau) + sum over negatives exp(sim(a, n) / tau) ) ]
```

It is exactly cross-entropy, where the classes are "which of these candidates is
the match" and the correct answer is the positive. That framing is worth
keeping: everything you know about cross-entropy applies here.

The visualisation puts the anchor and its positive on the unit circle with the
negatives scattered around, and computes the real loss. Move the jitter control
and the positive drifts from the anchor &mdash; more aggressive augmentation
makes the task harder, and the loss rises.

## Temperature

`tau` is small and it matters more than anything else in the loss.

**Low temperature** sharpens the softmax, so the sum is dominated by the single
most similar negative. The gradient concentrates on the hardest case, which
learns fine distinctions quickly and is unstable.

**High temperature** flattens everything until all negatives count about the
same, and the loss stops discriminating.

Drag it across its range and watch the loss move by an order of magnitude with
no change to the geometry at all.

## Negatives, and doing without them

More negatives generally means better representations &mdash; the task is
harder, so the answer is more informative. The readout shows the loss rising
with the count for exactly that reason.

That created an engineering problem, since negatives usually come from the
batch and batches have limits. **SimCLR** used very large batches. **MoCo** kept
a queue of representations from previous batches with a slowly-updated encoder.

Then a second family showed negatives were not required at all. **BYOL** and
**SimSiam** use only positive pairs, avoiding the collapse everyone expected
&mdash; where the encoder maps everything to one point and scores perfectly
&mdash; through an asymmetry: a predictor head on one branch and a stop-gradient
on the other. **Barlow Twins** and **VICReg** instead add a term that decorrelates
the representation's dimensions.

That negatives turned out to be optional was a genuine surprise, and why it
works is still argued over.

## Augmentation is the design

The augmentations decide what the model learns to ignore, and therefore what it
learns.

Colour jitter teaches colour invariance &mdash; excellent for object recognition
and wrong for a task where colour is the label. Random cropping teaches that
parts imply the whole, which is most of what makes contrastive learning work on
images and is also why it can learn to match textures rather than objects.

SimCLR's ablations found the augmentation choice mattered more than the
architecture, which is an unusual finding and a durable one.

## Where it is used

**Pretraining** on unlabelled data, then fine-tuning on a small labelled set.
This is the main use, and it is why the field cared.

**CLIP** contrasts images against their captions rather than against other
views, which is what produced a model that can be prompted in language.

**Sentence embeddings.** SimCSE contrasts a sentence against itself under
dropout.

**Recommendation and retrieval**, where "these two things go together" is the
native form of the data.

## Where it goes wrong

**Augmentations that destroy the label.** Colour jitter on a task about colour.

**Temperature left at a default.** Tune it; it does more than the architecture.

**Too few negatives** without one of the methods designed to work that way.

**False negatives.** Two different images of the same class are pushed apart by
the loss, which is a real cost of not having labels, and what supervised
contrastive learning fixes when labels are available.
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
intro: How a model that emits one token at a time chooses a whole sequence, and why the obvious method is not the best one.

## The architecture

Encoder-decoder handles the case where input and output are both sequences and
their lengths differ &mdash; translation, summarisation, speech to text.

The **encoder** reads the input and produces a representation. The **decoder**
emits output tokens one at a time, each conditioned on the representation and on
everything it has emitted so far.

The original version compressed the whole input into a single fixed vector,
which became the bottleneck that motivated
[attention](../natural_language_processing/attention_mechanism.html): let the
decoder look back at every input position rather than at one summary. That is
the change the field turned on, and the transformer is its conclusion.

Autoregressive decoding is not specific to that architecture. Any model that
emits one token at a time faces the same question: at each step you have a
probability over the vocabulary, and you have to choose.

## Greedy decoding, and its regret

Take the most probable token each time.

Fast, simple, and it optimises the wrong thing. You want the most probable
*sequence*, and the highest-probability first token can lead into a region where
everything that follows is bad.

The chart shows the cumulative log probability of the beam's paths. With the
width at 1 you get greedy decoding, and the readout compares it against the best
sequence a wider beam found. It is frequently worse, and the reason is always
the same: it committed early to something that looked good and did not pay off.

## Beam search

Keep the `k` best partial sequences. At each step, expand all of them, score
every continuation, keep the best `k` overall, and continue. At the end, take
the best complete sequence.

Drag the width from 1 upward and watch the best score improve.

It is still a heuristic. It does **not** find the globally best sequence &mdash;
that would require searching an exponentially large tree &mdash; and a path
discarded early because it looked weak can never come back, even if it led
somewhere excellent. Beam search only reduces how often that happens.

## The length problem

Sequence probability is a product of per-token probabilities, so every extra
token multiplies by something less than 1. Longer sequences have lower
probability, always, and unnormalised beam search therefore has a systematic
bias toward stopping early.

The standard fix divides the log probability by the length, sometimes raised to
a tunable power. It is a correction with no principled derivation, it is
necessary, and every production decoder has one.

## Wider is not always better

Raise the width past about 5 and translation quality often *falls*. This is
called the **beam search curse**, and it is well documented.

The explanation is that a wider beam finds sequences the model genuinely
considers more probable, and the model's notion of probable is not the same as
good. Very high-probability text is bland: it is the safe, generic continuation.
A wider search is a more faithful search of a flawed objective.

That is also why open-ended generation abandons beam search entirely. Sampling
methods &mdash; temperature, top-k, nucleus &mdash; deliberately do not take the
most probable path, because for creative text the most probable path is the
boring one. Beam search survives where there is a right answer: translation,
speech recognition, constrained generation.

## Where it goes wrong

**No length normalisation.** Everything comes out truncated.

**A very wide beam on open-ended text.** Blander, not better.

**Using beam search for creative generation.** Use sampling.

**Forgetting the cost.** Width `k` multiplies both computation and memory by
`k`, and for a large model that is the binding constraint.
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
intro: The layer that turns discrete symbols into vectors, and the optimisation that makes it practical.

## The problem

Neural networks consume numbers. A word, a user id or a product code is a
symbol, and there is no meaningful number to assign it &mdash; encoding "cat" as
7 and "dog" as 8 would tell the network they are adjacent, which is a claim
nobody made.

**One-hot encoding** avoids that: a vector of zeros with a single 1 at the
token's index. No false ordering, and no useful structure either. Every pair of
tokens is equally distant, and the vector is as long as the vocabulary.

An **embedding layer** maps each token to a dense learned vector instead. The
vector has a few hundred dimensions rather than fifty thousand, and its contents
are parameters, so training can put similar tokens near each other.

## The matmul that is a lookup

The formal definition is a one-hot vector multiplied by a weight matrix. Write it
out and the reason nobody does it becomes obvious: multiplying a vector that is
all zeros except one position by a matrix selects a single row and multiplies
everything else by zero.

The readout does the arithmetic. At a 50,000-token vocabulary and 512
dimensions, the honest matmul touches **25.6 million** numbers to retrieve
**512** of them.

So every framework implements the layer as an indexing operation. `nn.Embedding`
in PyTorch and `tf.keras.layers.Embedding` are table lookups with a backward
pass that scatters gradients to the rows that were used.

That is also why only the rows appearing in a batch receive a gradient. An
embedding table is a very large parameter tensor that is almost entirely idle on
any given step, which has consequences for optimisers keeping per-parameter
state and for anyone writing distributed training.

## The table is the model, mostly

Drag the vocabulary and dimension controls and watch the count. The table alone
is `vocab * dim` parameters, and for large vocabularies that is a substantial
fraction of the entire model &mdash; often more than any other single layer.

Two standard responses:

**Weight tying.** In a language model the output layer also has one row per
token. Sharing it with the input embedding halves the cost and usually improves
quality, since both are learning what tokens mean.

**Subword tokenisation.** [Byte-pair
encoding](../gen_ai/byte_pair_encoding_tokenizer.html) keeps the vocabulary in
the tens of thousands rather than the millions a word-level vocabulary would
need, and removes the out-of-vocabulary problem entirely.

## What the vectors learn

Nothing is imposed on the geometry. The rows start random and become whatever
minimises the loss, and the useful structure is a consequence rather than a
design.

Word2vec's famous arithmetic &mdash; king minus man plus woman &mdash; is that
consequence showing. Nobody built the analogy in; it fell out of a training
objective about predicting neighbouring words.

Which also means the structure reflects the training data, including its biases.
Embeddings trained on a corpus inherit that corpus's associations, and a great
deal of fairness work in NLP is about that fact.

## Beyond words

**Categorical features** in tabular models. A user id, a postcode, a product
category &mdash; all embed, and this is why neural networks became competitive on
tabular data with high-cardinality categories.

**Positional embeddings** in transformers, which embed a position rather than a
symbol.

**Recommendation.** Users and items each get a table, and their dot product is a
predicted affinity. Matrix factorisation is exactly this.

## Where it goes wrong

**Implementing the one-hot matmul literally.** Correct, and enormously wasteful.

**Choosing the dimension by feel.** A rule of thumb is the fourth root of the
vocabulary size, and it is worth tuning.

**Forgetting an out-of-vocabulary row.** Something has to handle unseen tokens;
subword tokenisation avoids the question.

**Reading similarity as meaning.** Embedding proximity reflects co-occurrence in
the training data, which is not the same thing.
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
intro: Training in half the bits, the failure that causes, and the one-line trick that removes it.

## Why bother

Modern accelerators run half-precision matrix multiplies several times faster
than single-precision ones, and half-precision tensors take half the memory.
That means bigger batches, bigger models, and a real speed-up on the same
hardware.

The catch is the format. **fp32** has 8 exponent bits and 23 mantissa bits.
**fp16** has 5 and 10, giving a smallest normal value around
10&#8315;&#8309; and a maximum of 65,504.

Both ends of that range are a problem, and the small end is the one that bites.

## Watch the gradients disappear

The histogram is gradient magnitudes spread over several orders of magnitude,
which is what a real network produces. The two marked lines are fp16's floor and
ceiling.

With the loss scale at 2&#8304; &mdash; that is, no scaling &mdash; the readout
reports how many of the 3,000 gradients round to **zero**. Those parameters
receive no update at all. Not a small update; none.

This is the failure that made early fp16 training unreliable. The model trains,
the loss goes down, and a fraction of the network is silently frozen.

## Loss scaling

The fix is almost embarrassingly simple. Multiply the loss by a large constant
before the backward pass. By the chain rule every gradient is multiplied by the
same constant, so the whole distribution shifts up into the representable range.
Then divide by that constant before the optimiser steps.

Drag the loss scale upward and watch the underflow count fall to zero.

The update is mathematically unchanged. The scaling exists purely so the numbers
survive the trip through fp16 &mdash; it is a change of units, not a change of
algorithm.

Push it too far and the readout starts reporting **overflow**: gradients that
have become infinite. That is a failure too, and it is where the automatic
version comes from.

## Dynamic loss scaling

Nobody tunes the constant by hand. The standard algorithm starts high,
multiplies by two whenever a stretch of steps completes without overflow, and
halves it and **skips the step** whenever an infinity or NaN appears.

Skipping is the important part: an overflowed gradient is not clipped or
repaired, it is discarded, because there is no way to recover what it should
have been. A few skipped steps early in training cost nothing.

This is what `torch.cuda.amp.GradScaler` does, and it is why mixed precision is
now a decorator rather than a project.

## What stays in fp32

"Mixed" is the operative word. In a standard setup:

**Weights** are kept in an fp32 master copy. Updates are frequently far smaller
than the weights themselves, and adding a tiny number to a large one in fp16
rounds to no change at all.

**Matrix multiplies and convolutions** run in fp16, where the speed is.

**Reductions** &mdash; sums, means, softmax, normalisation statistics &mdash;
accumulate in fp32, because adding many small numbers is exactly where limited
mantissa bits go wrong.

**Loss** is computed in fp32.

## bfloat16

The newer alternative has 8 exponent bits and 7 mantissa bits &mdash; the same
range as fp32, with less precision.

That trade removes this entire page. Range was the problem; precision, for
gradients, mostly was not. **bfloat16 needs no loss scaling**, which is why it
is the default on hardware that supports it, and why large-model training
largely stopped talking about GradScaler.

## Where it goes wrong

**fp16 without loss scaling.** Silent underflow, and a partly frozen model.

**A fixed scale.** Use the dynamic version.

**Reductions in fp16.** Softmax and layer norm in half precision produce
mysterious NaNs.

**Assuming a speed-up.** It comes from the tensor cores. Layers that are
memory-bound rather than compute-bound gain little.
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
intro: Getting the effect of a large batch out of a device that cannot hold one.

## Why it works

The loss over a batch is the mean of the per-example losses, and differentiation
is linear. So the gradient of the batch is the mean of the per-example
gradients.

That means the sum can be built in pieces. Run a forward and backward pass on 16
examples, keep the gradients, run another 16, add to them, and after 16 rounds
you have exactly the gradient of a 256-example batch. Step the optimiser once.

**The resulting update is identical** &mdash; not similar, identical up to
floating-point ordering &mdash; to what a single 256-example batch would have
produced.

## What actually consumes the memory

The bars separate the two cases at the memory budget you choose.

Training memory is roughly:

**Fixed costs.** Weights, their gradients, and the optimiser state. Adam keeps
two extra tensors per parameter, so this is around four times the model size,
and it does not depend on the batch at all.

**Activations.** Every intermediate value from the forward pass has to be kept
for the backward pass. This scales linearly with the batch size, and for a deep
model it dominates.

Accumulation attacks only the second, which is why it works. Drag the
micro-batch down and watch the second bar fall while the fixed part stays put.

The dashed line is the budget. When the full batch crosses it and the micro-batch
does not, that gap is the entire reason the technique exists.

## What it costs

**Time.** Sixteen sequential passes take about as long as sixteen passes.
Accumulation does not make anything faster; it makes something possible.

There is a small efficiency loss too, since very small micro-batches use the
accelerator less well. A micro-batch of 1 is usually much less than a sixteenth
as efficient as a micro-batch of 16.

## The one thing that is not identical

**Batch normalisation.** Its statistics are computed over whatever is in the
forward pass, which is the micro-batch, not the accumulated total.

So a model with batch norm trained with a micro-batch of 4 behaves like one
trained with a batch of 4, however many accumulation steps follow. The
normalisation is noisier, and at very small micro-batches it degrades badly.

This is a real reason to prefer
[layer normalisation](layer_normalization.html) or group normalisation, both of
which normalise per example and are indifferent to the batch. It is not a
coincidence that transformers use layer norm and are the architectures trained
with the most aggressive accumulation.

## Getting it right

Two details cause most of the bugs.

**Divide the loss by the number of accumulation steps** before the backward
pass, or the accumulated gradient is a sum where the optimiser expects a mean,
and your effective learning rate is multiplied by the step count.

**Zero the gradients at the right time** &mdash; after the optimiser step, not
after every backward pass. Zeroing every pass defeats the whole thing, and it
fails silently: training still runs, just with the small batch you were trying
to avoid.

## Alongside

**Activation checkpointing** trades compute for memory in the other direction:
discard activations during the forward pass and recompute them in the backward
pass, for roughly 30% more time and a large memory saving. The two combine.

**Mixed precision** halves activation memory outright, and combines with both.

**Model parallelism and ZeRO** attack the fixed costs, which accumulation cannot
touch. When the weights alone do not fit, accumulation is not the answer.

## Where it goes wrong

**Forgetting to divide the loss.** Silently multiplies the learning rate.

**Zeroing gradients every pass.** Silently defeats the technique.

**Using it with batch norm at a tiny micro-batch.** Real quality loss.

**Expecting a speed-up.** It buys capability, not throughput.
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
intro: A one-line change to the target that improves calibration, and the reason the loss no longer reaches zero.

## The problem with a hard target

Cross-entropy with a one-hot target asks the model to put probability 1 on the
correct class and 0 on everything else.

Softmax cannot produce exactly 1. It approaches it as the correct logit runs
away from the others, and reaches it only in the limit. So the target is
unattainable, the gradient never vanishes, and training keeps pushing the logit
gap wider for as long as you let it.

The consequences are familiar. The model becomes **overconfident**, reporting
0.99 on cases it gets wrong. It **overfits**, because widening logits on training
examples is always an available way to reduce the loss. And it is **badly
calibrated**, in exactly the way
[the calibration module](../machine_learning/probability_calibration.html)
measures.

## The change

Move a little probability off the correct class and spread it over the others:

```
target[correct]  =  1 - eps + eps/K
target[others]   =  eps/K
```

Drag epsilon and watch the bars. At 0 you have the one-hot target. At 0.1 the
true class asks for 0.91 and each of nine others asks for about 0.011.

That is the entire technique.

## Why it fixes the problem

The readout gives the **optimal logit gap**: how far apart the logits have to be
to match the target exactly.

At epsilon 0 it is infinite, which is the problem restated. At epsilon 0.1 it is
a specific finite number, and once the model reaches it the gradient is zero.
The model now has a reason to *stop*.

That is the mechanism. Not noise, not regularisation in the weight-decay sense
&mdash; a reachable target where before there was none.

## The loss will not reach zero

The readout also gives the minimum achievable loss, which is the entropy of the
smoothed target.

A model matching the smoothed target perfectly still reports a loss around 0.5
at typical settings. This surprises people who expect training loss to approach
zero, and it is not a bug: you changed what perfect means.

It also means training and validation losses are no longer comparable with runs
that did not use smoothing. Compare accuracy, or compare like with like.

## What it buys, and what it costs

**Better calibration.** The headline benefit. Confidences become closer to
observed accuracies.

**Better generalisation.** Consistent small gains across image classification
and translation. It was in the Inception-v3 paper and in the original
Transformer, at 0.1 in both, and 0.1 has been the default ever since.

**Tighter class clusters.** Representations of a class group more tightly, with
more even distances between classes.

That last one has a cost. **Label smoothing hurts distillation.** A student
learns from the teacher's full output distribution, and the informative part is
the relative sizes of the *wrong* classes &mdash; that this dog was slightly cat
and not at all lorry. Smoothing deliberately flattens exactly that, erasing what
the student was supposed to learn. If a model is going to be a distillation
teacher, train it without.

## Where it goes wrong

**Epsilon too large.** Past about 0.2 you are actively teaching the model that
wrong answers are plausible, and accuracy falls. Drag it up and watch the target
flatten.

**Comparing losses across runs.** The floor moved.

**Using it on a teacher model.** It removes the dark knowledge distillation
depends on.

**Applying it to regression.** It is a change to a categorical target and has no
meaning without one.

**Expecting it to fix a badly calibrated model on its own.** It helps; explicit
[temperature
scaling](../machine_learning/probability_calibration.html) on a validation set
helps more, and the two combine.
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
