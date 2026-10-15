# -*- coding: utf-8 -*-
"""The four named-architecture modules in the Deep Learning track.

Two of these are generative - a GAN and an autoencoder - and two are about
recommendation, which is where most people's first production model actually
lives.

The GAN page is deliberately not a training run. Almost every GAN
visualisation on the internet is one, which means it demonstrates whether that
particular run converged rather than what the model is. Here the optimal
discriminator is computed in closed form, so the reader can be the generator
and every number responds instantly and exactly. The autoencoder page does the
same thing with a different theorem.
"""

from arch_common import (entry, svg, box, txt, line, circle, path, stack, A, M, B, S)

TOPICS = []


# ---------------------------------------------------------------------------
# 1. GANs
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "gan_architecture",
    "deep_learning",
    "GAN Architecture and Equilibrium",
    "Generative models",
    "Be the generator; the discriminator is exact",
    "The optimal discriminator has a closed form, so no training run is "
    "needed. Move the generator and watch the value function, the divergence "
    "and the gradient respond.",
    svg(box(12, 24, 34, 18, fill=S) + txt(29, 36, "z", M, 9)
        + line(46, 33, 60, 33, B, 1.2)
        + box(60, 24, 34, 18, fill=S) + txt(77, 36, "G", A, 9)
        + box(60, 52, 34, 18, fill=S) + txt(77, 64, "D", A, 9)
        + line(77, 42, 77, 52, B, 1.2)
        + box(108, 52, 40, 18, fill=S) + txt(128, 64, "real / fake", M, 7)
        + line(94, 61, 108, 61, B, 1.2)
        + txt(128, 33, "real data", M, 7)
        + line(128, 40, 90, 52, B, 1, "3 2")),
    {"widget": "gan"},
    [
        "For a fixed generator the best possible discriminator is "
        "<code class='mono-font'>p_data / (p_data + p_g)</code>. No training "
        "needed &mdash; it is a formula.",
        "Substituting it turns the game into a Jensen-Shannon divergence. "
        "The equilibrium value is exactly &minus;log 4.",
        "When the two distributions barely overlap the minimax gradient "
        "vanishes and the non-saturating one does not. Same fixed point, "
        "different trainability.",
        "Mode collapse is not a bug in the optimiser. Nothing in the objective "
        "as written penalises producing one excellent sample forever.",
    ],
    r"""
title: GAN Architecture and Equilibrium
intro: Two networks with opposite goals, one closed-form answer for the critic. A divergence that shows all that goes wrong.

## The game

Generative adversarial networks learn to produce data without ever being
shown what a correct output looks like. Instead, a second network judges
whether each sample is real or fake, and the generator learns by trying to
fool that judge. The result is a training loop where both networks improve
together &mdash; or, if things go wrong, neither does. This page works
through the math behind that loop, the fixed point it aims for, and the
failure modes that make GANs famously hard to train.

A generator maps noise to samples. A critic receives a sample and
guesses the chance that it came from the real data rather than the
generator. They are trained against each other:

```
min over G   max over D   E_data[log D(x)]  +  E_z[log(1 - D(G(z)))]
```

The critic wants that formula large. The gen wants it small.
There's no target output for the gen anywhere. No one says what a
good sample looks like &mdash; only a second network's view, which raises
as the gen does. That is what makes the approach notable, and it's
also the source of each trouble in the rest of this page.

## The discriminator has a closed form

Here is that makes this page exact rather than a demo. Hold the
gen fixed. The goal is a sum over `x` of

```
p_data(x) log D(x) + p_g(x) log(1 - D(x))
```

and each `x` is free of the others. So You can raise pointwise.
Differentiating `a log d + b log(1 - d)` and setting it to zero gives
`d = a / (a + b)`, so:

```
D*(x) = p_data(x) / (p_data(x) + p_g(x))
```

The blue curve in the explorer is that formula. It needs no training, no seed
and no learning rate. Where only real data lives it's 1. Where only made
samples live it's 0. Where the two densities are equal it's just 0.5.

## Substituting it turns the game into a divergence

Put `D*` back into the goal and the algebra merges to:

```
V(D*, G) = -log 4 + 2 * JSD(p_data || p_g)
```

The Jensen-Shannon divergence is even, non-minus, and zero only when
the two spreads are the same. So the gen is cutting a genuine
distance between spreads, and the game has a **unique global optimum** at
`p_g = p_data`, where the value is `-log 4 = -1.386` and the critic is
reduced to answering 0.5 all over. Not because it's bad, but because
there's nothing left to set apart.

Both numbers are on screen. Set the target to one mode and drag the gen's
mean and spread until the divergence reaches 0. The value function arrives at
&minus;1.386 at the same moment. That is the theorem, and it's being checked
by number as you move the slider.

## Where the gradient goes

Now set the gen's mean far from the data so the spreads barely
share, and read the two grad figures.

With almost no share the best critic is correct about all.
Under the gen, `D* ~ 0`, and `log(1 - D*)` is flat there &mdash; it's
already almost `log 1 = 0` and moving the gen slightly doesn't change it.
**The grad vanishes just when the gen is worst.**

This is the trap. The better the critic, the more just right it separates
the two, and the less the gen can learn. It isn't an optimisation
failure. It's a property of the loss.

The first paper's own fix is in the same section that derives the problem.
Instead of cutting `log(1 - D(G(z)))`, **raise `log D(G(z))`** &mdash; the
non-saturating form. Same fixed point, fully different grad magnitude
in just the regime where it matters. Switch the loss control in the explorer
with the spreads separated and compare the two numbers. The ratio is the
whole reason each setup uses the second form.

Later work went further: Wasserstein GAN replaced the divergence fully,
because the JSD between two spreads on disjoint supports is a constant
(log 2) and so has no grad at all, while the earth-mover distance
still knows which direction is closer.

## Mode collapse, exactly

Set the target spread to **two modes** and leave the gen narrow.

The gen here is a single Gaussian. So It truly can't cover two
separated modes. Sitting on one of them scores far better than straddling the
gap. The explorer says so, and there's a reason for copying the failure in
a model too simple to avoid it: it isolates the part of mode collapse that has
nothing to do with room.

A real gen has ample room to cover both modes and merges anyway.
The goal is the reason. The critic judges **one sample at a time**.
It can say "this looks real" or "this looks fake". It has no way to say "these
are all the same". So a gen that finds one output the critic
accepts and makes it forever is scoring just right by the stated goal.
Nothing in the equation at the top of this page mentions range.

The fixes all amount to giving the critic batch-level info:
minibatch discrimination gives it statistics across the batch, unrolled GANs
let the gen see the critic's future response, and WGAN-GP changes
the distance so the grad keeps pointing at the uncovered mode.

## The architecture

The theory is spread-shaped. The practice is a pair of convolutional
networks. The DCGAN table in the explorer builds both at 64&times;64 and counts
their params as you change the base width.

Read the gen top to bottom: a 100-dimensional noise vector is projected
and reshaped to 4&times;4&times;1024, then four transposed convolutions double
the detail each time to 64&times;64&times;3. The critic is the same
thing reversed, strided convolutions halving the detail down to a single
logit.

The near-symmetry is deliberate and it's the hands-on heart of GAN training.
If the critic is much stronger it wins right away and the gen's
grad disappears. Much weaker and its judgement is noise. DCGAN's other
rules are all steadiness patches on the same problem: strided convolutions
rather than pooling, batch norm in both networks, no fully-connected hidden
layers, ReLU in the gen and LeakyReLU in the critic.

```python
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, z=100, base=64, out_ch=3):
        super().__init__()
        def up(cin, cout, first=False, last=False):
            layers = [nn.ConvTranspose2d(cin, cout, 4,
                                         stride=1 if first else 2,
                                         padding=0 if first else 1, bias=False)]
            if last:
                return nn.Sequential(*layers, nn.Tanh())
            return nn.Sequential(*layers, nn.BatchNorm2d(cout), nn.ReLU(True))

        self.net = nn.Sequential(
            up(z, base * 8, first=True),   # 1x1   -> 4x4
            up(base * 8, base * 4),        # 4x4   -> 8x8
            up(base * 4, base * 2),        # 8x8   -> 16x16
            up(base * 2, base),            # 16x16 -> 32x32
            up(base, out_ch, last=True))   # 32x32 -> 64x64

    def forward(self, z):
        return self.net(z.view(z.size(0), -1, 1, 1))
```

`Tanh` on the output isn't decoration: it bounds the gen's range to
[&minus;1, 1], and the real images must be normed to the same range or the
critic can separate real from fake on scale alone and learns nothing
about content. It's the most common first bug.

## Reading the training curves, and why they tell you nothing

One consequence of the theory above is worth stating on its own, because it
catches everyone who trains a GAN for the first time.

**The loss values don't show progress.** In plain guided training a
falling loss means the model is raising. Here the two losses are measured
against each other, and both networks are moving. A critic loss near
`log 2` means it can't tell real from fake. Which is either the
balance you wanted or a critic that has merged. A gen loss
that falls steadily often means the critic is losing, not that the
samples are good.

The value function in the explorer is the exception, and only because it's
found against the *best* critic rather than a network being
trained alongside. In a real run you don't have `D*`, you've what your
critic currently is, and the number it makes isn't close
between steps.

So GAN progress is measured by looking at samples, or by a sample-based metric.
**FID** &mdash; the Frechet Inception Distance &mdash; passes made and real
images through an Inception network, fits a Gaussian to each set of activations,
and reports the distance between them. It isn't a loss, it can't be optimised
right, and it's the number papers really report. It also has the property
the training loss lacks: it punishes a gen that makes great
samples with no range, because a merged set of activations has the wrong
covariance.

## Where GANs stand now

Diffusion models displaced GANs as the default for image generation, and the
reason is on this page. A diffusion model has a **stable regression goal**
&mdash; predict the noise that was added. With no second network to
balance against, no balance to reach and no mode collapse to detect. Trading
rival training for a simple loss and more sampling steps turned out to be
the right trade at scale.

GANs remain the right tool where a single forward pass is needed: real-time
super-detail, image-to-image translation, on-device generation. And the
rival idea itself long outgrew image synthesis &mdash; domain-rival
training, rival strength and the critic in a visual loss are
all this page's structure, applied to a thing else.
## Questions people ask

<strong>My critic loss went to zero. Is that good?</strong> It's the failure mode, not success. With the supports barely shared the best critic is right about all, `log(1 - D)` is flat there. The gen's grad vanishes just when it's worst. Use the non-saturating form. If it persists, weaken the critic. Fewer updates, a lower learning rate. Or change the goal to WGAN-GP, whose grad doesn't die on disjoint supports.

<strong>What should the losses look like when training is healthy?</strong> There's no target curve. Both losses are measured against a moving opponent. A critic loss near `log 2 = 0.693` means it can't separate real from fake. This Is either the balance you wanted or a critic that has given up. The two look the same on the plot. Judge by samples and by FID.

<strong>How do I tell mode collapse from merely bad samples?</strong> By range rather than quality. Make a few hundred samples from different noise and look for repeats. FID catches it because a merged set of activations has the wrong covariance. Here Any per-sample quality score won't. The critic only ever judges one sample at a time. Nothing in the goal mentions range at all.

<strong>Why `Tanh` on the gen, and what breaks without it?</strong> It bounds the output to [&minus;1, 1], and the real images must be normed to that same range. Or else the critic can separate real from fake on scale alone and never has to learn any of it about content. It's the most common first bug and it presents as "training looks fine, samples are noise".

<strong>Should I train the critic more than the gen?</strong> The first method allows k critic steps per gen step and used k = 1. A stronger critic gives a better grad *direction* and a vanished one under the saturating loss. The two networks are often kept close in room. With WGAN-GP extra critic steps truly help. This Is a consequence of the different distance rather than a general rule.

<strong>Are GANs still worth learning now that diffusion has won?</strong> For two reasons. A GAN makes in a single forward pass. This Still decides the matter for real-time super-detail, image-to-image translation and on-device generation. And the rival structure long outgrew image synthesis. Domain-rival training, rival strength and the critic inside a visual loss are all this page applied elsewhere.

## Recap in one screen

- A min-max game with no target output for the gen anywhere. Only a second network's view. This Raises as the gen does.
- Hold the gen fixed and the best critic has a closed form, `D*(x) = p_data / (p_data + p_g)`. This Needs no training at all.
- Substituting it turns the game into `2 . JSD - log 4`. There's a unique optimum at `p_g = p_data` where the value is &minus;1.386 and `D = 0.5` all over.
- Where the spreads barely share the saturating loss has almost no grad. This Is just why each setup raises `log D(G(z))` instead.
- Mode collapse is the goal, not the room. A gen that finds one accepted output and repeats it forever is scoring just right by the stated goal.
- The loss values don't measure progress. Samples do. FID does. It punishes a gen with no range.
""",
    [
        {"q": "For a fixed generator, what is the optimal discriminator?",
         "options": ["A network trained to convergence",
                     "p_data(x) / (p_data(x) + p_g(x)) - a closed form, no "
                     "training required",
                     "Always 0.5",
                     "The likelihood ratio p_data / p_g"],
         "answer": 1,
         "why": "The objective decomposes pointwise, so maximising a log d + "
                "b log(1 - d) at each x gives d = a / (a + b). Substituting it "
                "back turns the game into a Jensen-Shannon divergence with a "
                "unique optimum at p_g = p_data."},
        {"q": "Why does the minimax generator loss vanish when the generator "
              "is bad?",
         "options": ["The learning rate is too small",
                     "With almost no overlap D* is near 0 under the generator, "
                     "and log(1 - D*) is flat there - so there is no gradient "
                     "exactly when it is most needed",
                     "The discriminator overfits",
                     "The noise distribution is wrong"],
         "answer": 1,
         "why": "A better discriminator means a worse generator gradient. The "
                "non-saturating form - maximise log D(G(z)) - has the same "
                "fixed point and a usable gradient in that regime, which is "
                "why every implementation uses it."},
        {"q": "Why does the objective as written not penalise mode collapse?",
         "options": ["It does, through the divergence term",
                     "The discriminator judges one sample at a time, so it can "
                     "say 'this looks fake' but never 'these are all the same'",
                     "Because the generator has too little capacity",
                     "Because the noise is Gaussian"],
         "answer": 1,
         "why": "Nothing in the equation mentions diversity. A generator that "
                "finds one accepted output and repeats it is scoring perfectly. "
                "The fixes - minibatch discrimination, unrolled GANs, WGAN-GP - "
                "all give the discriminator batch-level information or change "
                "the distance."},
        {"q": "At the global optimum, what does the discriminator output?",
         "options": ["1 for real and 0 for fake",
                     "0.5 everywhere, because the two distributions are "
                     "identical and there is nothing to distinguish",
                     "It diverges",
                     "It depends on the architecture"],
         "answer": 1,
         "why": "D* = p_data / (p_data + p_g), so if the two are equal it is "
                "0.5 at every x, and V(D*, G) is exactly -log 4. A "
                "discriminator stuck at 0.5 is the success condition, not a "
                "failure to learn."},
    ],
    refs=[("Generative Adversarial Nets", "Goodfellow et al., NeurIPS 2014",
           "https://arxiv.org/abs/1406.2661"),
          ("Unsupervised Representation Learning with Deep Convolutional "
           "Generative Adversarial Networks", "Radford, Metz & Chintala, "
           "ICLR 2016", "https://arxiv.org/abs/1511.06434"),
          ("Wasserstein GAN", "Arjovsky, Chintala & Bottou, ICML 2017",
           "https://arxiv.org/abs/1701.07875")],
    description="Be the generator: move the distribution and watch the exact "
                "optimal discriminator, the -log 4 equilibrium and the "
                "vanishing gradient respond."))


# ---------------------------------------------------------------------------
# 2. Autoencoders
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "autoencoders_conceptual_and_pytorch",
    "deep_learning",
    "Autoencoders in Depth",
    "Representation learning",
    "Encode, bottleneck, decode - computed exactly",
    "A linear autoencoder provably learns the PCA subspace, so this one is "
    "solved in closed form. Move the bottleneck and watch the reconstruction "
    "and the error curve respond with no random seed anywhere.",
    svg(stack(16, 28, 12, [34, 24, 14], gap=5)
        + box(72, 38, 14, 14, fill=A, sw=0)
        + stack(96, 28, 12, [14, 24, 34], gap=5)
        + txt(79, 66, "z", A, 8)
        + txt(80, 84, "narrow enough to force a choice", M, 7)),
    {"widget": "autoencoder"},
    [
        "The bottleneck is the whole architecture. Without it, the identity "
        "function is a perfect solution and nothing is learned.",
        "A <em>linear</em> autoencoder trained to convergence spans the same "
        "subspace as the top principal components. That is a theorem, and it "
        "is what this page computes.",
        "Reconstruction error against bottleneck size is the tail sum of the "
        "eigenvalues &mdash; which is why the curve is smooth, not noisy.",
        "A plain autoencoder's latent space has no structure between the "
        "points it saw. That gap is what a VAE exists to close.",
    ],
    r"""
title: Autoencoders in Depth
intro: An encoder, a decoder, and a on purpose narrow gap between them - with the linear case solved just so the mechanism is visible.

## The trick is the constraint

An autoencoder is trained to copy its input. Stated like that it's
absurd: the identity function scores just right and learns nothing.

The constraint is what makes it a model. Force the network through a
form smaller than the input. 64 pixels into 4 numbers &mdash;
and perfect rebuild turns hopeless. The network has to decide what
is worth keeping, and that choice *is* the learned form.

Three parts, and only one of them matters:

- the **encoder** maps input to a code `z`;
- the **bottleneck** is `z` itself, whose width you choose;
- the **decoder** maps `z` back to a thing the size of the input.

Move the bottleneck slider in the explorer and watch the rebuild. At
k = 1 the network has one number per image and all looks like the same
mean shape. By k = 4 the six shapes are distinguishable. By k = 16 the
rebuild is close, and the compression is only 4&times;.

## Why this page can be exact

A linear autoencoder &mdash; no activation functions, just two mats &mdash;
trained to settling on squared error provably spans the same subspace as the
top-k principal components. Baldi and Hornik proved it in 1989: the squared
rebuild error has no local minima that aren't global, and each global
min spans the principal subspace.

So the explorer doesn't train any of it. It finds the principal components
of the dataset right and uses them as the encoder and decoder. There's no
seed, no learning rate and no run-to-run variation, and each number on the
page is exact.

Two things follow right away, and both are visible.

**The error curve is the eigenval tail.** Rebuild error at bottleneck
k equals the sum of the eigenvals from k+1 onward. That is why the curve in
the explorer is smooth and monotone rather than jagged &mdash; it isn't a
training result, it's math.

**The decoder columns are readable.** The six small tiles show what each
latent dim adds to the rebuild when it's set to +1. Blue is
minus. The first accounts for the most variance in the dataset, the second
for the most of what is left. So on. The percentages are printed on them.

## The latent space is a space

Set the two latent sliders to a coord no real image made and watch the
decoder draw a thing anyway.

That is worth pausing on. The decoder is a function defined latent
space, not a lookup table of the training set. Feeding it a point between two
training images gives a thing between them. Feeding it a point far outside
gives a thing, though often not a thing you want.

This is just where a plain autoencoder stops and a variational autoencoder
begins. Nothing in the rebuild goal pushes the latent space to
be *filled in*. The encoder can scatter the training data into isolated islands
with nonsense between them, and the loss won't object &mdash; it only ever
asks about points that came from real data. A VAE adds a KL term pushing the
encoder's output spread toward a standard normal, which pressures the
codes to occupy a connected region and makes sampling from the latent space
give plausible output. That is the difference between a compressor and a
generative model.

## Denoising, without asking for it

Turn the corruption slider up. The input tile gets noisy. The rebuild
mostly doesn't.

Nothing here was trained to drop noise. The mechanism is the bottleneck: the
noise is spread across all 64 directions of pixel space, the bottleneck keeps
only k of them, and most of the noise has nowhere to go. The two error figures
in the explorer make it concrete. At a narrow bottleneck the
rebuild is closer to the *clean* image than the corrupted input was.

A **denoising autoencoder** makes this the clear goal: corrupt the
input, ask for the clean target. It's a stronger idea than it first appears,
because it drops the last excuse for learning the identity &mdash; the
identity is now actively wrong. And it forces the network to learn
a thing about the structure of the data rather than about the data itself. It
is also, in retrospect, the direct ancestor of masked language modelling and of
diffusion models, both of which are "corrupt the input, predict what it was".

## Non-linear, and what it buys

If linear autoencoders are PCA, why build a deep one?

Because the principal subspace is a **flat** subspace, and the structure in
real data often isn't flat. Images of a rotating object trace a curve
through pixel space. The best 2-plane through that curve is a poor description
of it. A non-linear encoder can follow the curve, and a convolutional encoder
can also exploit that a shifted image is the same image
&mdash; a thing a dense linear map has no way to know.

The architecture stays the same three parts. The layer table in the explorer
gives a convolutional autoencoder for 28&times;28 input, and the param
counts update with the bottleneck you've selected.

```python
import torch
import torch.nn as nn

class ConvAutoencoder(nn.Module):
    def __init__(self, latent=16):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(1, 16, 3, stride=2, padding=1), nn.ReLU(True),   # 28 -> 14
            nn.Conv2d(16, 32, 3, stride=2, padding=1), nn.ReLU(True),  # 14 -> 7
            nn.Flatten(),
            nn.Linear(32 * 7 * 7, latent))
        self.decoder = nn.Sequential(
            nn.Linear(latent, 32 * 7 * 7), nn.ReLU(True),
            nn.Unflatten(1, (32, 7, 7)),
            nn.ConvTranspose2d(32, 16, 3, stride=2, padding=1,
                               output_padding=1), nn.ReLU(True),       # 7 -> 14
            nn.ConvTranspose2d(16, 1, 3, stride=2, padding=1,
                               output_padding=1),                      # 14 -> 28
            nn.Sigmoid())

    def forward(self, x):
        return self.decoder(self.encoder(x))

model = ConvAutoencoder(latent=16)
opt = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

for images, _ in loader:          # the labels are not used at all
    out = model(images)
    loss = loss_fn(out, images)   # the target IS the input
    opt.zero_grad(); loss.backward(); opt.step()
```

Three details that cause real trouble. `output_padding=1` is needed on the
transposed convolutions or 7 turns 13 instead of 14 &mdash; stride-2
downsampling isn't just invertible and the ambiguity has to be resolved
by name. `Sigmoid` on the output must match the input range: pair it with
`MSELoss` or `BCELoss` on data in [0, 1], and if your data is normed to
[&minus;1, 1] use `Tanh` instead. And `for images, _ in loader` is the whole
point of the method &mdash; the labels are discarded, because the oversight
is the input itself.

For the denoising variant, change one line:

```python
    noisy = images + 0.3 * torch.randn_like(images)
    out = model(noisy.clamp(0, 1))
    loss = loss_fn(out, images)     # corrupted in, clean out
```

## Choosing the bottleneck

The bottleneck size is the one real setting, and the error curve in the
explorer is the tool for choosing it.

The curve is the tail sum of the eigenvals. So Its shape says a thing
precise: how much of the dataset's variance is left unexplained after k
directions. Where it drops steeply, each new dim is buying a lot. Where
it flattens, the left directions are showing noise and per-example
detail rather than structure.

The elbow is where to sit. Move the slider on this dataset and the curve falls
sharply to about k = 5 and then flattens. Six shapes with a little
spot-based and thickness variation truly need about that many numbers.
Choosing k = 12 doesn't make the model better. It makes it a slightly lossy
copy machine, and the variance-retained figure will read close to 100% while
the form has stopped meaning any of it.

Two symptoms tell you which side of the elbow you're on. Too narrow and each
rebuild looks like the dataset mean. Watch k = 1 in the
explorer. Too wide and the rebuild is great while the latent space
is useless for any of it downstream. The encoder has been allowed to
pass the input through nearly unchanged rather than show it.

## What autoencoders are actually used for

Not compression. JPEG is better, faster and doesn't need a GPU or a training
set, and an autoencoder only compresses data resembling what it was trained on.

What they're used for:

- **Outlier spotting.** Train on normal data only. Any of it the model
  rebuilds badly is unlike what it saw. This is a truly common
  production use in making and monitoring, and it works because the
  bottleneck refuses to represent what it has no basis for.
- **The latent space of a diffusion model.** Stable Diffusion doesn't diffuse
  in pixel space. It diffuses in the latent space of a trained autoencoder, at
  roughly 1/8 the detail per side. The autoencoder is what makes
  high-detail generation affordable.
- **Pretraining and form learning**, where masked autoencoders (MAE)
  brought the idea back for vision transformers. Mask 75% of the patches
  and rebuild them, which is the denoising goal at an extreme.

The through-line is the same in all three: an autoencoder is a way to find out
what a dataset's structure is, by forcing a thing to show it in fewer
numbers than it came in.
## Questions people ask

<strong>If a linear autoencoder is PCA, is it truly PCA?</strong> It spans the same *subspace*. This Isn't the same as finding the same axes. Nothing in the goal makes the encoder's directions perp or orders them by variance. A trained linear autoencoder's units are often rotations and mixtures of principal components. This page uses the actual components. This Is why its per-dim tiles are readable and a trained model's wouldn't be.

<strong>Why is my autoencoder just copying the input?</strong> Because the bottleneck isn't binding. If the code is as wide as the input, or the decoder can simply undo the encoder, the identity is available and it's the optimum. The loss is doing what you asked. Narrow the code, or switch to a denoising goal where the identity is actively wrong.

<strong>Autoencoder or VAE?</strong> Compressor or generative model. Nothing in the rebuild loss asks the latent space to be filled in. A plain autoencoder is free to scatter codes into isolated islands with nonsense in between. The loss only ever asks about points that came from real data. If you intend to sample from the latent space, you need the KL term that pushes the codes toward a connected region.

<strong>Why does the transposed convolution need `output_padding=1`?</strong> Because stride-2 downsampling isn't just invertible. Inputs of 13 and 14 both map to 7. Going back up the ambiguity has to be resolved by name. Leave it out and 7 turns 13 rather than 14. The shape error surfaces a place further down the decoder.

<strong>Which output activation and loss go together?</strong> Match the data range. `Sigmoid` with `MSELoss` or `BCELoss` for data in [0, 1]. `Tanh` with `MSELoss` for data in [&minus;1, 1]. Mismatch them and part of the target sits outside the activation's range. The model spends its room saturating instead of rebuilding.

<strong>Is it really any good for compression?</strong> No. JPEG is better, faster, needs no GPU and no training set. An autoencoder only compresses data that resembles what it was trained on. The real uses are outlier spotting, supplying the latent space a diffusion model works in, and form pretraining.

## Recap in one screen

- The constraint is the model. Forcing the input through a narrower code makes perfect rebuild hopeless. What the network chooses to keep *is* the form.
- A linear autoencoder trained to settling spans the top-k principal subspace. This Is why this page is exact math rather than a training run with a seed.
- The error curve is the eigenval tail. Error at bottleneck k is the sum of eigenvals from k+1 onward. So the elbow is a real thing to read, not a heuristic.
- Denoising falls out of the bottleneck for free. Noise spreads across each direction and only k of them live. Making it the clear goal is the direct ancestor of masked language modelling and of diffusion.
- Non-linearity buys the ability to follow curved structure. This A flat principal subspace shows badly.
- Too narrow and each rebuild is the dataset mean. Too wide and the rebuild is great while the code has stopped meaning any of it.
""",
    [
        {"q": "Why does an autoencoder need a bottleneck?",
         "options": ["To reduce training time",
                     "Without one the identity function is a perfect solution "
                     "and nothing is learned",
                     "To make the decoder differentiable",
                     "To prevent vanishing gradients"],
         "answer": 1,
         "why": "The constraint is the model. Forcing the data through fewer "
                "numbers than it arrived in is what makes the network choose "
                "what to keep, and that choice is the representation."},
        {"q": "What is the relationship between a linear autoencoder and PCA?",
         "options": ["They are unrelated",
                     "A linear autoencoder trained to convergence spans the "
                     "same subspace as the top-k principal components",
                     "PCA is a special case with one component",
                     "PCA is always better"],
         "answer": 1,
         "why": "Baldi and Hornik proved it in 1989 - the squared "
                "reconstruction error has no non-global local minima, and "
                "every global minimum spans the principal subspace. It is why "
                "this page can compute the answer exactly instead of training."},
        {"q": "Turning up the input corruption often gives a reconstruction "
              "closer to the CLEAN image than the input was. Why?",
         "options": ["The network was trained to denoise",
                     "The noise is spread across all input directions and the "
                     "bottleneck only keeps a few of them, so most of it has "
                     "nowhere to go",
                     "The sigmoid clips it",
                     "It is a numerical artefact"],
         "answer": 1,
         "why": "Nothing on the page was trained to denoise. A denoising "
                "autoencoder makes it the explicit objective - corrupt the "
                "input, ask for the clean target - which pushes the same effect "
                "much further and is the ancestor of masked language modelling."},
        {"q": "What does a VAE add that a plain autoencoder lacks?",
         "options": ["A deeper decoder",
                     "A KL term pushing the encoder's output toward a standard "
                     "normal, so the latent space is filled in and can be "
                     "sampled from",
                     "Convolutional layers",
                     "A smaller bottleneck"],
         "answer": 1,
         "why": "The reconstruction loss only ever asks about points that came "
                "from real data, so a plain autoencoder is free to scatter "
                "codes into islands with nonsense between them. The KL term is "
                "what turns a compressor into a generative model."},
    ],
    refs=[("Neural Networks and Principal Component Analysis: Learning from "
           "Examples Without Local Minima", "Baldi & Hornik, Neural Networks "
           "1989", None),
          ("Reducing the Dimensionality of Data with Neural Networks",
           "Hinton & Salakhutdinov, Science 2006", None),
          ("Auto-Encoding Variational Bayes", "Kingma & Welling, ICLR 2014",
           "https://arxiv.org/abs/1312.6114"),
          ("Masked Autoencoders Are Scalable Vision Learners",
           "He et al., CVPR 2022", "https://arxiv.org/abs/2111.06377")],
    description="Move an autoencoder's bottleneck and watch the reconstruction, "
                "the learned components and the exact error curve respond - no "
                "training run, no seed."))


# ---------------------------------------------------------------------------
# 3. Collaborative filtering
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "collaborative_filtering",
    "deep_learning",
    "Collaborative Filtering",
    "Recommenders",
    "Four methods, one matrix, the same held-out ratings",
    "Click any cell of a ten-by-twelve ratings matrix and watch four methods "
    "predict it, with the neighbour arithmetic printed and every method scored "
    "on data none of them fitted.",
    svg("".join(box(18 + c * 13, 14 + r * 13, 12, 12,
                    fill=(S if (r * 5 + c) % 4 else A), sw=0.7, rx=1)
                for r in range(4) for c in range(6))
        + box(31, 27, 12, 12, fill="none", stroke=A, sw=2, rx=1)
        + txt(118, 34, "?", A, 14)
        + circle(118, 46, 1.4, M, M, 0)
        + txt(80, 82, "predict the empty cell", M, 7)),
    {"widget": "collaborative"},
    [
        "The only input is who rated what. No genres, no descriptions, no "
        "demographics &mdash; and the methods still find the genres.",
        "Deviations are averaged, not ratings. Someone who rates everything 4 "
        "and someone who rates everything 2 can agree perfectly about "
        "<em>order</em>.",
        "Matrix factorisation's two bias terms carry most of the signal in a "
        "real dataset before any latent factor is consulted.",
        "Every method here is scored on the same held-out cells, so the "
        "comparison is real. The matrix is printed in full so you can check it.",
    ],
    r"""
title: Collaborative Filtering
intro: Predict what someone will think of a thing they've never seen, using nothing but who rated what.

## The only input is the matrix

Content-based recommendation shows the items &mdash; genre, director,
keywords &mdash; and matches them to a profile. Collaborative filtering has
none of that. It has one thing: a mat with users down the side, items across
the top, and a rating in the cells that are filled.

The mat in the explorer is printed in full: sixteen people, fifteen titles,
138 training ratings, and 37 more held back so that each method is scored on
data none of them fitted. Click any cell and four methods will predict it.

Two properties of that mat drive all.

**It's mostly empty.** Here about a quarter of the cells are missing. On a real
catalogue it's 99.9% or worse, because no one has watched more than a
vanishing fraction of a million titles. each method below is a way of guessing
a missing entry from the present ones.

**Nothing in it says what an item is.** The words "sci-fi" and "romance" appear
in the explorer for your gain. No method reads them. That the methods
recover the genre groups anyway is the point of the field.

## User-based neighbours

Find people who agreed with you in the past, and mean what they thought of
the thing you haven't seen.

Select **user-based kNN**, click an empty cell, and the neighbour table appears
with the math. Read the columns carefully, because one of them is where
the method's real content lives.

Likeness is **Pearson link over the items both people rated**. It's a
link, not an share count. So It asks whether two people's ratings move
together rather than whether they're by number close.

Then the guess:

```
prediction = your average
           + sum over neighbours of  sim * (their rating - their average)
             divided by  sum of |sim|
```

It means **deviations**, not ratings. That matters more than it looks.
Someone who rates all 4 and someone who rates all 2 can agree
just right about which titles are better. Centring each on their own mean is
what lets the method notice that, and it's what stops a generous rater from
dragging each guess upward.

Move the **k** slider. At k = 1 the guess is one person's view and the
error is high. Raising k means more people and smooths, until eventually you
are including neighbours who barely correlate and the extra noise costs more
than the extra evidence buys.

Click a cell where no neighbour has rated the item and the method falls back to
the mean, with a note. That isn't a bug in the setup &mdash; it's
the **sparsity problem**, and on a real catalogue it's the common case rather
than the exception.

## Item-based neighbours

Switch to **item-based kNN**. Instead of "people like you also liked", it's
"people who liked this also liked", and the guess mixes your own
ratings of similar items.

Amazon's 2003 paper made this the industry default, for reasons that are
hands-on rather than statistical. Item-item likenesses are far more stable
than user-user ones &mdash; a film's audience changes slowly, a person's taste
and rating history change constantly. So the likeness mat can be
found offline overnight and served from a cache. And it shows itself:
"because you watched X" is a sentence you can put in the interface.

On this mat the two methods score likewise. On a real system with many more
users than items, item-based wins on operational grounds before fit is
discussed.

## Matrix factorisation

Both zone methods are local: they look at a handful of rows or
columns. mat factorisation is global. It assumes the whole mat is
about low rank:

```
rating(u, i) ~ mu + b_u + b_i + p_u . q_i
```

each user gets a vector `p_u`, each item a vector `q_i`, and the guess is
their dot product plus three offsets. The vectors are learned by grad
descent on the seen entries only. The missing ones aren't treated as
zero, they're simply not in the sum.

Select it and look at the math line for your chosen cell. The three terms
before the dot product are doing an huge amount of work: `mu` is the global
mean, `b_u` is "this person rates generously", `b_i` is "this title is well
liked". On real ratings data those three explain most of the variance before any
latent factor is consulted. This Is why a bias-only model is a truly
strong baseline and why leaving the biases out is a common way to build a
disappointing recommender.

Then look at the item factor table. Sort it by any factor column and the three
genres separate. No one supplied a genre. A factor is what direction best
shows who rated what, and on this data that turns out to be genre &mdash; on
a real catalogue the factors match to nothing nameable, which is the
trade: fit for the ability to say why.

Now move the **smoothing** slider with 5 or more factors selected. At 0.02
the test RMSE is clearly worse than at 0.2. With 138 training ratings and eight
factors for each of 31 users and items, the model carries nearly twice as many
latent params as it has readings, and will fit the noise just unless
a thing stops it. This is the clearest possible
demo of why the Netflix Prize answers were as much about
smoothing as about factorisation.

## Reading the comparison

The bars at the bottom score each method on the same 37 held-out cells.
Lower is better and the bars are drawn to scale. A longer bar is a worse
method.

The sorting is the notable part. The global mean, at about 1.34, is the
floor. The user's own mean is *worse* than that. This Is a real effect of a
small sample: an mean over eight or nine ratings is a noisy guess, and a
noisy personalised guess can be worse than an accurate impersonal one. Both
zone methods beat both baselines clearly, landing near 0.9. mat
factorisation, smoothed sensibly, goes lower again, to about 0.78.

Thirty-seven test cells is still a small sample and the caption says so &mdash;
treat small differences as noise. The gap to the baselines isn't small.

One setup detail that is easy to omit and worth about a tenth of an
RMSE point: **clip the guess to the rating scale**. A zone method
extrapolates past the ends routinely. A user mean of 4.2 plus a plus
deviation lands at 5.4 &mdash; and 5.4 isn't a rating. each guess on this
page is clipped to [1, 5] before it's shown or scored.

```python
import numpy as np

# ratings: [U, I]; mask: [U, I] with 1 where a rating is observed.
def sgd_factorise(ratings, mask, factors=8, steps=400, lr=0.02, reg=0.1, seed=0):
    rng = np.random.default_rng(seed)
    U, I = ratings.shape
    P = rng.normal(0, 0.1, (U, factors))
    Q = rng.normal(0, 0.1, (I, factors))
    bu, bi = np.zeros(U), np.zeros(I)
    mu = ratings[mask == 1].mean()
    observed = list(zip(*np.nonzero(mask)))

    for _ in range(steps):
        for u, i in observed:                 # observed entries ONLY
            pred = mu + bu[u] + bi[i] + P[u] @ Q[i]
            err = ratings[u, i] - pred
            bu[u] += lr * (err - reg * bu[u])
            bi[i] += lr * (err - reg * bi[i])
            pu = P[u].copy()
            P[u] += lr * (err * Q[i] - reg * pu)
            Q[i] += lr * (err * pu - reg * Q[i])
    return P, Q, bu, bi, mu
```

The line to look at is `pu = P[u].copy()`. Update `P[u]` first and the `Q[i]`
update uses the already-changed value. This Isn't the grad you derived. It
often still trains, slightly worse. This Is what makes it hard to notice.

## What this cannot do

**Cold start.** A new user has no ratings. So There are no neighbours and no
learned vector. A new item has no one who has rated it. Collaborative filtering
is silent on both, and each production system pairs it with a content-based
fallback for just this reason.

**Popularity bias.** common items have more ratings. So They appear in more
zones and get recommended more. This Earns them more ratings. The
feedback loop is real, measurable, and the reason "range" and "serendipity"
are metrics people really track.

**The missing entries aren't missing at random.** People rate what they chose
to consume, and they chose it because they expected to like it. The seen
ratings are a biased sample of all possible ratings, and each method on this
page quietly assumes they aren't.

The next page takes the same mat and replaces the dot product with a neural
network, which handles none of these three. But does open the door to
the side info that fixes the first.
## Questions people ask

<strong>Pearson or cosine likeness?</strong> Pearson centres each person on their own mean. It asks whether two people's ratings move together rather than whether they're by number close. Which is what you want when one rater is generous and another is harsh. On silent plus-only data there's no mean to centre against. Cosine is the standard choice instead.

<strong>User-based or item-based?</strong> Item-based, often, and on operational grounds before fit is discussed. Item-item likenesses are far more stable. A title's audience changes slowly where a person's history changes constantly. So the mat can be found offline and served from a cache, and "because you watched X" is a sentence that fits in the interface.

<strong>Why is the user's own mean worse than the global mean?</strong> Small-sample noise. An mean over eight or nine ratings is a poor guess of any of it. A noisy personalised guess truly can lose to an accurate impersonal one. It's worth remembering as the cheapest available proof that personalisation isn't automatically an improvement.

<strong>How many latent factors should I use?</strong> Fewer than you'd guess on small data. The smoothing matters more than the count. With 138 training ratings and eight factors across 31 users and items the model carries nearly twice as many latent params as it has readings. It will fit the noise just unless a thing stops it. Which is why the Netflix Prize answers were as much about smoothing as about factorisation.

<strong>Should I fill the missing entries with zeros?</strong> No. A missing rating isn't a rating of zero. Treating it as one tells the model that all unseen is terrible. The loss is summed over seen entries only. This Is what makes this the factorisation of a in part-seen mat rather than of a mostly-zero one.

<strong>Why clip the guesses?</strong> Because zone methods extrapolate past the ends of the scale routinely. A user mean of 4.2 plus a plus deviation lands at 5.4. 5.4 isn't a rating anyone can give. Clipping to the scale is one line and worth roughly a tenth of an RMSE point.

## Recap in one screen

- The only input is who rated what. Nothing tells any method what an item *is*. That the factors recover the genre groups anyway is the whole point of the field.
- Zone methods mean **deviations** from each person's own mean. This Is what lets a generous rater and a harsh one be recognised as agreeing.
- Item-based is the industry default because item-item likeness is stable enough to precompute and explainable enough to show the user.
- Factorisation is global and low-rank. Its three offsets. Global, user, item. Explain most of the variance before a single latent factor is consulted.
- When latent params outnumber readings, smoothing is the difference between a model and a memoriser.
- Cold start, popularity bias, and ratings that aren't missing at random are the three problems none of this handles.
""",
    [
        {"q": "Why do neighbourhood methods average deviations from each "
              "person's mean rather than raw ratings?",
         "options": ["To keep the numbers small",
                     "Because a generous rater and a harsh rater can agree "
                     "perfectly about the ordering, and centring is what lets "
                     "the method see that",
                     "To handle missing values",
                     "Because Pearson correlation requires it"],
         "answer": 1,
         "why": "Someone who rates everything 4 and someone who rates "
                "everything 2 have identical preferences and very different "
                "numbers. Without centring, the generous rater drags every "
                "prediction upward."},
        {"q": "In matrix factorisation, what do mu, b_u and b_i capture before "
              "any latent factor is used?",
         "options": ["Nothing useful",
                     "The global average, how generously this person rates, "
                     "and how well liked this item is - which explains most of "
                     "the variance in real ratings data",
                     "The number of ratings",
                     "The regularisation"],
         "answer": 1,
         "why": "A bias-only model is a strong baseline. Only what the biases "
                "cannot explain is handed to the latent factors, and that "
                "residual is the part that encodes taste."},
        {"q": "With 8 factors and 138 training ratings, low regularisation "
              "gives a much worse test RMSE. Why?",
         "options": ["The learning rate is too high",
                     "There are nearly twice as many latent parameters as "
                     "observations, so the model fits the noise exactly unless "
                     "something penalises large weights",
                     "The factors are correlated",
                     "The biases interfere"],
         "answer": 1,
         "why": "Sixteen users and fifteen items at 8 factors each is 248 "
                "latent parameters for 138 observations. Regularisation is not "
                "a refinement here, it is what makes the model usable - which "
                "is why the Netflix Prize work was as much about it as about "
                "factorisation."},
        {"q": "Why is item-based kNN the industry default over user-based?",
         "options": ["It is more accurate",
                     "Item-item similarities change slowly, so they can be "
                     "precomputed offline and cached, and 'because you watched "
                     "X' explains itself",
                     "It handles cold start",
                     "It needs less memory"],
         "answer": 1,
         "why": "The reasons are operational. A film's audience is stable; a "
                "person's rating history changes with every session, so "
                "user-user similarities would have to be recomputed constantly."},
    ],
    refs=[("Matrix Factorization Techniques for Recommender Systems",
           "Koren, Bell & Volinsky, IEEE Computer 2009", None),
          ("Amazon.com Recommendations: Item-to-Item Collaborative Filtering",
           "Linden, Smith & York, IEEE Internet Computing 2003", None),
          ("The BellKor Solution to the Netflix Grand Prize",
           "Koren, 2009", None)],
    description="Click any cell of a ratings matrix and watch user-kNN, "
                "item-kNN and matrix factorisation predict it, all scored on "
                "the same held-out ratings."))


# ---------------------------------------------------------------------------
# 4. Deep learning for recommendation systems
# ---------------------------------------------------------------------------
TOPICS.append(entry(
    "deep_learning_for_recommendation_systems",
    "deep_learning",
    "Deep Learning for Recommendation Systems",
    "Recommenders",
    "Two towers, and where the parameters really are",
    "A user tower, an item tower, and an interaction. Switch between a dot "
    "product and an MLP, then look at what fraction of the model is lookup "
    "tables.",
    svg(box(12, 14, 44, 16, fill=S) + txt(34, 25, "user id", M, 7)
        + box(104, 14, 44, 16, fill=S) + txt(126, 25, "item id", M, 7)
        + box(12, 36, 44, 16, fill="none", stroke=A) + txt(34, 47, "embed", A, 7)
        + box(104, 36, 44, 16, fill="none", stroke=A) + txt(126, 47, "embed", A, 7)
        + line(34, 30, 34, 36, B, 1) + line(126, 30, 126, 36, B, 1)
        + line(34, 52, 74, 62, B, 1) + line(126, 52, 86, 62, B, 1)
        + box(56, 62, 48, 14, fill=S) + txt(80, 72, "score", M, 7)),
    {"widget": "recsys"},
    [
        "Almost none of a neural recommender's parameters are in the neural "
        "network. They are in two lookup tables that grow with the catalogue.",
        "The two towers are kept separate until the last step so item vectors "
        "can be computed once and retrieved by approximate nearest neighbour.",
        "The 2019 reproducibility study found a well-tuned matrix "
        "factorisation matching or beating neural collaborative filtering.",
        "What deep models genuinely add is <em>side information</em> &mdash; "
        "text, images, context, sequence &mdash; which a dot product between "
        "two id embeddings cannot accept.",
    ],
    r"""
title: Deep Learning for Recommendation Systems
intro: The network is the small part. All that makes a production recommender hard follows from where the params really live.

## An id is not a feature

The first problem is one that doesn't exist in vision or language. A user id
is an any int. So is an item id. Neither has any numeric meaning
&mdash; user 4,192 isn't "between" users 4,191 and 4,193 &mdash; so they
can't be fed to a network right.

An **embedding table** is the answer: a mat with one learned row per id. The
model looks up the row and works with that. This is the same op as a
word embedding, and it's doing the same job. Turning a symbol into a
vector whose geometry means a thing.

The consequence is the whole page. The table has one row per user and one per
item, so **its size is set by the catalogue, not by the model design**.

## The two towers

Look at the diagram in the explorer. A user tower turns a user id into a
vector, an item tower turns an item id into a vector, and an interplay
mixes them into a score.

The tower structure isn't stylistic. Keeping the two sides separate until the
final step means the item tower can be run **once per item, offline**, and its
outputs stored in a vector index. At request time only the user tower runs, and
finding the best items turns an rough nearest-neighbour query rather
than five million forward passes.

If the two ids were concatenated at the input and fed to a single network, that
would be hopeless: each (user, item) pair would need its own forward pass.
The two-tower shape is what makes lookup tractable, and it's why it's the
standard for the pick-generation stage of each large system.

## Three ways to interact

Switch the model control and watch the diagram and the numbers change.

**mat factorisation** takes the dot product. One number, no params in
the interplay at all. It says the score is high when the two vectors point
the same way.

**MLP** concatenates the two vectors and passes them through dense layers. In
principle this can learn any interplay. A dot product is a very exact one.

**NeuMF** does both and fuses them, with *separate* embedding tables for each
path &mdash; note the param count doubling when you select it. The paper's
arg is that the best embedding for a dot product and for an MLP aren't
the same, so forcing them to share is a constraint neither wants.

Then look at the check bars. On this data the dot product wins: mat
factorisation reaches about 0.76 RMSE where the MLP settles near 0.83 &mdash;
and pushing the MLP's epoch count past 300 makes it *worse*, which is the
overfitting you'd expect from 444 params and 138 ratings.

That isn't a quirk of a small page. In 2019 Dacrema, Cremonesi and Jannach
copied the published neural recommendation results and found that a
properly tuned mat factorisation matched or beat most of them on the
standard benchmarks &mdash; the neural models had been checked against weak
baselines. It's worth knowing about, because "we replaced the dot product with
an MLP" isn't on its own a reason to expect an improvement.

## So what does deep learning actually buy?

Not a better interplay function. a thing more basic: **the ability to
accept any of it other than an id.**

A dot product between two id embeddings can only ever use who rated what. A
network can take, alongside the embeddings:

- item **text and images**. So A title with no ratings still has a vector
  &mdash; which is the item cold-start problem solved;
- **context** &mdash; time of day, device, what the session has already
  held;
- **sequence** &mdash; a transformer over the user's recent history, so the
  model shows "what they're doing now" rather than "what they like in
  general", which is what SASRec and BERT4Rec are for;
- **multiple goals** at once, since clicks, watch time and purchases are
  different heads on shared towers.

each one of those is a genuine capability that factorisation doesn't have.
None of them is "the MLP learns a better interplay".

## The parameter budget

Set the catalogue-size control to a large service and read the table. This is
that shapes each production system.

At 50 million users and 5 million items with 64-dimensional embeddings, the
tables hold about 3.5 billion params. The network on top &mdash; a couple
of dense layers &mdash; holds a few thousand. The ratio is on screen and it's
not close.

All follows from that:

- **Sharding.** The tables don't fit on one machine, so they're split across
  param servers while the network is replicated. This is the reason
  large-scale recommender training infrastructure looks nothing like
  large-scale vision training infrastructure.
- **Hashing.** Ids are hashed into a fixed number of buckets to cap the table
  size, accepting collisions as the price. Two rare items sharing a row is
  often cheaper than a table that grows forever.
- **Sparse grads.** One training example touches two rows. A dense
  tuner update over three billion params per step would be absurd, so
  the embedding grads are sparse and only the touched rows move.
- **lookup and ranking as separate stages.** A cheap two-tower model
  pulls a few hundred picks from millions by nearest neighbour. An
  costly model with full cross-features ranks those few hundred. Nothing
  large ever scores the whole catalogue.

## Implicit feedback, which is what you will actually have

This page and the previous one use clear ratings, because they're easy to
reason about. Almost no real system has them. What it has is clicks, plays,
purchases and dwell time &mdash; **silent feedback**, which is plus-only.

That changes the problem. There are no negatives, only absences, and an lack
is ambiguous: the user disliked it, or never saw it. Training needs sampled
negatives, and the sampling strategy matters more than the architecture
&mdash; uniform sampling makes the task too easy, popularity-based sampling
makes it harder and often better, and in-batch negatives are what large
two-tower systems really use because they're free.

The loss changes too. Squared error on a rating turns a ranking loss: BPR
raises the margin between a plus and a sampled minus, and sampled
softmax treats lookup as classification over the catalogue.

```python
import torch
import torch.nn as nn

class TwoTower(nn.Module):
    def __init__(self, n_users, n_items, dim=64, hidden=128):
        super().__init__()
        self.user_emb = nn.Embedding(n_users, dim)
        self.item_emb = nn.Embedding(n_items, dim)
        # Towers stay separate: item vectors are precomputed and indexed.
        self.user_tower = nn.Sequential(nn.Linear(dim, hidden), nn.ReLU(),
                                        nn.Linear(hidden, dim))
        self.item_tower = nn.Sequential(nn.Linear(dim, hidden), nn.ReLU(),
                                        nn.Linear(hidden, dim))

    def user_vec(self, u):
        return nn.functional.normalize(self.user_tower(self.user_emb(u)), dim=-1)

    def item_vec(self, i):
        return nn.functional.normalize(self.item_tower(self.item_emb(i)), dim=-1)

    def forward(self, u, i):
        return (self.user_vec(u) * self.item_vec(i)).sum(-1)

# Every other item in the batch is a negative. Free negatives.
def in_batch_softmax(model, users, items, temperature=0.05):
    U = model.user_vec(users)                 # [B, D]
    I = model.item_vec(items)                 # [B, D]
    logits = U @ I.T / temperature            # [B, B]
    target = torch.arange(len(users), device=logits.device)
    return nn.functional.cross_entropy(logits, target)
```

The `norm` calls are what make the final score a cosine likeness, which
is what nearest-neighbour indexes are built for. Skip them and your
lookup index no longer matches your training goal. The `temperature`
is a real setting: too high and each item looks equally good, too low
and training destabilises.

`in_batch_softmax` is the trick worth remembering. The main-line of the
likeness mat is the true pairs and all off it's a minus, so a
batch of 1,024 gives 1,023 negatives per example at no extra cost. Its one
weakness is that common items appear in more batches and so are sampled as
negatives more often, which suppresses them &mdash; production systems correct
for that with a logQ term.

## The order to learn this in

Start with mat factorisation and get the biases and smoothing right,
because it's a strong baseline that a lot of published neural work failed to
beat. Move to a two-tower model when you've side info for it to use,
or when you need to pull from millions of items by nearest neighbour. Reach
for sequence models when the recent session matters more than the long-run
profile. And measure ranking metrics on held-out interplays throughout,
because RMSE on a rating isn't what a recommender is for.
## Questions people ask

<strong>Does replacing the dot product with an MLP help?</strong> On its own, often not. In 2019 Dacrema, Cremonesi and Jannach copied the published neural recommendation results and found a properly tuned mat factorisation matched or beat most of them. The neural models had been measured against weak baselines. On this page's data factorisation reaches about 0.76 RMSE where the MLP settles near 0.83.

<strong>Then what does deep learning really buy?</strong> The ability to accept any of it other than an id. Item text and images. This Solves item cold start. Context such as time and device. The recent session through a sequence model. And a few goals at once as separate heads on shared towers. each one is a capability factorisation lacks. None of them is "the MLP learns a better interplay".

<strong>Why keep the two towers separate?</strong> So the item tower can be run once per item, offline, with its outputs stored in a vector index. Leaving only the user tower to run per request. Turning "find the best items" into a nearest-neighbour query. Concatenate the two ids at the input instead and each (user, item) pair needs its own forward pass. This Makes lookup from millions hopeless.

<strong>Why norm the tower outputs?</strong> Because it makes the final score a cosine likeness. This Is what nearest-neighbour indexes are built for. Skip the norming and the index no longer matches the training goal. The model is trained under one geometry and served under another. The lookup quality quietly drops.

<strong>Where do negatives come from with silent feedback?</strong> You sample them. The strategy matters more than the architecture. Uniform sampling makes the task too easy, popularity-based sampling is harder and often better. In-batch negatives are what large two-tower systems use because a batch of 1,024 supplies 1,023 negatives at no cost. In-batch sampling does over-punish common items. This Production systems correct with a logQ term.

<strong>Why does recommender training infrastructure look nothing like vision's?</strong> Because the params are in the embedding tables rather than the network. At 50 million users and 5 million items with 64 dims the tables hold about 3.5 billion params against a few thousand in the dense layers. Sharded param servers, id hashing, sparse grads and the lookup/ranking split all follow from that one ratio.

## Recap in one screen

- An id has no numeric meaning. It goes through an embedding table. And that table's size is set by the catalogue, not by any modelling choice.
- Two towers joined only at the last step is what makes lookup a nearest-neighbour query instead of millions of forward passes.
- The interplay function is the least key choice on the page. A tuned dot product is a strong baseline that a good deal of published neural work failed to beat.
- What deep learning truly adds is side info, context, sequence and multiple goals.
- Almost no real system has ratings. silent feedback is plus-only. Negatives are sampled and squared error gives way to a ranking loss.
- The params live in the tables. This Is the single fact behind sharding, hashing, sparse grads and staged lookup.
""",
    [
        {"q": "In a production neural recommender, where are almost all the "
              "parameters?",
         "options": ["In the dense layers",
                     "In the two embedding tables, which grow with the number "
                     "of users and items rather than with the model design",
                     "In the output layer",
                     "In the optimiser state"],
         "answer": 1,
         "why": "At 50 M users and 5 M items with 64-dimensional embeddings "
                "the tables are about 3.5 billion parameters and the network "
                "is a few thousand. Sharding, hashing and sparse gradients all "
                "follow from that ratio."},
        {"q": "Why are the two towers kept separate until the final "
              "interaction?",
         "options": ["It trains faster",
                     "Item vectors can then be computed once offline and "
                     "retrieved by approximate nearest neighbour, instead of "
                     "running a forward pass per (user, item) pair",
                     "It reduces overfitting",
                     "The embeddings would collide otherwise"],
         "answer": 1,
         "why": "If both ids went into one network at the input, scoring a "
                "catalogue would need one forward pass per item. The two-tower "
                "shape is what makes retrieval from millions of items "
                "tractable at request time."},
        {"q": "A 2019 reproducibility study found tuned matrix factorisation "
              "matching or beating neural collaborative filtering. What is the "
              "right conclusion?",
         "options": ["Deep learning does not work for recommendation",
                     "Replacing a dot product with an MLP is not by itself a "
                     "reason to expect an improvement; what deep models add is "
                     "the ability to use side information",
                     "The study was flawed",
                     "Embeddings should be removed"],
         "answer": 1,
         "why": "The neural results had been compared against weak baselines. "
                "Text, images, context and sequence are things a dot product "
                "between two id embeddings genuinely cannot accept - and that, "
                "not the interaction function, is the real gain."},
        {"q": "What is the appeal of in-batch negatives?",
         "options": ["They are more informative than sampled ones",
                     "Every other item in the batch serves as a negative at no "
                     "extra cost - a batch of 1,024 gives 1,023 negatives per "
                     "example",
                     "They avoid the cold-start problem",
                     "They remove the need for a temperature"],
         "answer": 1,
         "why": "The similarity matrix is computed anyway; the diagonal is the "
                "true pairs and everything off it is free supervision. The "
                "known weakness is that popular items appear in more batches "
                "and get over-penalised, which a logQ correction addresses."},
    ],
    refs=[("Neural Collaborative Filtering", "He et al., WWW 2017",
           "https://arxiv.org/abs/1708.05031"),
          ("Are We Really Making Much Progress? A Worrying Analysis of Recent "
           "Neural Recommendation Approaches",
           "Dacrema, Cremonesi & Jannach, RecSys 2019",
           "https://arxiv.org/abs/1907.06902"),
          ("Sampling-Bias-Corrected Neural Modeling for Large Corpus Item "
           "Recommendations", "Yi et al., RecSys 2019", None),
          ("Deep Neural Networks for YouTube Recommendations",
           "Covington, Adams & Sargin, RecSys 2016", None)],
    description="Two towers, an embedding table and an MLP: see why 99% of a "
                "neural recommender is lookup tables and what deep learning "
                "actually buys."))
