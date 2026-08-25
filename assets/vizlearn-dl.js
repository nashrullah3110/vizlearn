/* Interactive demonstrations for the generated deep_learning/ modules.
 *
 * The track was strong on training mechanics - gradients, normalisation,
 * regularisation, schedules - and silent on architecture beyond a dense
 * network. Autoencoders, GANs, diffusion and contrastive learning had no page
 * anywhere on the site, and the words were being used regardless.
 *
 * As on the other generated tracks, the arithmetic runs here. The autoencoder
 * really projects onto a k-dimensional subspace and really reconstructs from
 * it; the diffusion page really applies the forward noising schedule and
 * really inverts it; beam search really searches the beam.
 *
 * The plotter and the seeded RNG come from vizlearn-plot.js, shared with the
 * maths and machine learning harnesses.
 *
 * Binds to [data-vz-dl]; costs nothing on a page that has none.
 */
(function () {
    "use strict";
    var V = window.VizML;
    var Plot = V.Plot, rng = V.rng, normal = V.normal, css = V.css, mean = V.mean;

    var A = function () { return css("--accent-primary", "#b06d10"); };
    var F = function () { return css("--accent-fill", "#e0982f"); };
    var M = function () { return css("--text-muted", "#8a9096"); };

    /* A signal with a few strong components and a lot of small ones - the
     * situation every compression argument on these pages depends on. */
    function signal(n, seed) {
        var r = rng(seed || 401), out = [], i, k;
        var comps = [[1.0, 1, 0], [0.55, 2, 1.1], [0.28, 3, 2.2], [0.14, 5, 0.4]];
        for (i = 0; i < n; i++) {
            var t = i / n * 2 * Math.PI, v = 0;
            for (k = 0; k < comps.length; k++)
                v += comps[k][0] * Math.sin(comps[k][1] * t + comps[k][2]);
            out.push(v + normal(r) * 0.06);
        }
        return out;
    }

    /* Reconstruct a signal from its k strongest frequency components. A real
     * autoencoder learns its basis rather than being handed one, but the
     * bottleneck argument - keep k numbers, lose the rest - is identical, and
     * a linear autoencoder provably finds this subspace. */
    function bottleneck(x, k) {
        var n = x.length, comps = [], f, i;
        for (f = 0; f < Math.floor(n / 2); f++) {
            var re = 0, im = 0;
            for (i = 0; i < n; i++) {
                var ang = -2 * Math.PI * f * i / n;
                re += x[i] * Math.cos(ang);
                im += x[i] * Math.sin(ang);
            }
            comps.push({ f: f, re: re / n, im: im / n, mag: Math.hypot(re, im) / n });
        }
        var keep = comps.slice().sort(function (a, b) { return b.mag - a.mag; }).slice(0, k);
        var out = new Array(n).fill(0);
        keep.forEach(function (c) {
            for (i = 0; i < n; i++) {
                var ang = 2 * Math.PI * c.f * i / n;
                out[i] += 2 * (c.re * Math.cos(ang) - c.im * Math.sin(ang));
            }
        });
        return out;
    }

    function mse(a, b) {
        var s = 0, i;
        for (i = 0; i < a.length; i++) s += (a[i] - b[i]) * (a[i] - b[i]);
        return s / a.length;
    }

    var DEMOS = {

        /* An autoencoder as a bottleneck: how much survives k numbers. */
        autoencoder: function (p, view) {
            var n = 128, x = signal(n, 401);
            if (p.noise > 0) {
                var r = rng(409);
                x = x.map(function (v) { return v + normal(r) * p.noise; });
            }
            var k = p.latent | 0;
            var y = bottleneck(x, k);
            var plot = Plot(view.canvas(0), { xr: [0, n], yr: [-2.4, 2.4], height: 280,
                                              pad: { l: 46, r: 12, t: 12, b: 32 } });
            plot.axes("position", "value");
            plot.line(x.map(function (v, i) { return [i, v]; }), M(), 1.6);
            plot.line(y.map(function (v, i) { return [i, v]; }), A(), 2.4);

            var clean = signal(n, 401);
            return {
                readout: "latent size " + k + " for " + n + " inputs - a " +
                         (n / k).toFixed(0) + ":1 squeeze.  Reconstruction error " +
                         mse(x, y).toFixed(4) +
                         (p.noise > 0
                            ? ", but against the CLEAN signal only " + mse(clean, y).toFixed(4) +
                              " - the bottleneck cannot afford to store noise, so it discards it. " +
                              "That is what a denoising autoencoder exploits."
                            : ".  Raise the latent size and the copy tightens; lower it and " +
                              "the network must choose what matters.")
            };
        },

        /* The reparameterisation trick, and what the KL term does to a latent. */
        vae: function (p, view) {
            var r = rng(p.seed || 411), n = 500, pts = [], i;
            var muA = [-p.separation, 0], muB = [p.separation, 0];
            for (i = 0; i < n; i++) {
                var which = i % 2;
                var mu = which ? muB : muA;
                /* z = mu + sigma * epsilon. The randomness enters as epsilon,
                 * which carries no gradient, so mu and sigma stay
                 * differentiable - that is the whole trick. */
                var eps = [normal(r), normal(r)];
                pts.push([mu[0] + p.sigma * eps[0], mu[1] + p.sigma * eps[1], which]);
            }
            var plot = Plot(view.canvas(0), { xr: [-4, 4], yr: [-3, 3], height: 290 });
            plot.axes("latent dimension 1", "latent dimension 2");
            // the prior the KL term pulls towards
            var circle = [], k;
            for (k = 0; k <= 80; k++) {
                var t = k / 80 * 2 * Math.PI;
                circle.push([2 * Math.cos(t), 2 * Math.sin(t)]);
            }
            plot.line(circle, M(), 1.4, [5, 4]);
            pts.forEach(function (q) { plot.dot(q[0], q[1], q[2] ? F() : A(), 2.6); });

            var overlap = p.sigma / Math.max(0.01, p.separation);
            return {
                readout: "sigma " + p.sigma.toFixed(2) + ", class centres " +
                         (2 * p.separation).toFixed(1) + " apart.  The dashed circle is the " +
                         "prior the KL term pulls towards.  " +
                         (overlap > 0.75
                            ? "The two clusters have merged: KL has won, and the decoder cannot tell them apart - posterior collapse."
                            : (overlap < 0.18
                                ? "Tight, separated clusters with gaps between them - good reconstruction, but sampling from the prior lands in empty space."
                                : "Separated but continuous, which is the balance a VAE is trying to strike."))
            };
        },

        /* A GAN as a two-player game on one dimension: the generator's
         * distribution against the real one, and what the discriminator says. */
        gan: function (p, view) {
            var gmu = p.gmu, gsd = p.gsd, rmu = 1.0, rsd = 0.6;
            var gauss = function (x, m, s) {
                return Math.exp(-(x - m) * (x - m) / (2 * s * s)) / (s * Math.sqrt(2 * Math.PI));
            };
            var real = [], fake = [], disc = [], x;
            for (x = -4; x <= 5; x += 0.03) {
                var pr = gauss(x, rmu, rsd), pg = gauss(x, gmu, gsd);
                real.push([x, pr]);
                fake.push([x, pg]);
                /* The optimal discriminator for fixed distributions is
                 * pr / (pr + pg) - this is not learned, it is the closed form
                 * the GAN objective drives towards. */
                disc.push([x, (pr + pg) > 1e-12 ? pr / (pr + pg) : 0.5]);
            }
            var top = Math.max.apply(null, real.concat(fake).map(function (q) { return q[1]; }));
            var a = Plot(view.canvas(0), { xr: [-4, 5], yr: [0, top * 1.1], height: 220,
                                           pad: { l: 52, r: 12, t: 12, b: 30 } });
            a.axes("value", "density");
            a.line(real, M(), 2.2);
            a.line(fake, A(), 2.2);

            var b = Plot(view.canvas(1), { xr: [-4, 5], yr: [0, 1], height: 200,
                                           pad: { l: 52, r: 12, t: 12, b: 32 } });
            b.axes("value", "D(x) - 'this is real'");
            b.line([[-4, 0.5], [5, 0.5]], M(), 1.2, [4, 4]);
            b.line(disc, F(), 2.2);

            // Jensen-Shannon-ish overlap measure
            var ov = 0, step = 0.03;
            for (x = -4; x <= 5; x += step) ov += Math.min(gauss(x, rmu, rsd), gauss(x, gmu, gsd)) * step;
            return {
                readout: "distribution overlap " + (100 * ov).toFixed(1) + "%.  " +
                         (ov < 0.08
                            ? "Almost disjoint: the discriminator is certain everywhere, its gradient is nearly flat, and the generator learns almost nothing. This is why the original GAN loss was replaced."
                            : (ov > 0.9
                                ? "Nearly identical, and D sits at 0.5 everywhere - it cannot tell them apart, which is the equilibrium."
                                : "Partial overlap. D is informative where they differ, and that is where the generator's gradient comes from."))
            };
        },

        /* Diffusion: the forward schedule really applied, and the signal-to-
         * noise ratio it produces at each step. */
        diffusion: function (p, view) {
            var n = 128, x0 = signal(n, 401);
            var T = 60, t = p.t | 0;
            /* Cosine schedule for alpha-bar, as in improved DDPM. The whole
             * forward process is x_t = sqrt(abar) x0 + sqrt(1-abar) eps. */
            var abar = function (s) {
                var f = Math.cos((s / T + 0.008) / 1.008 * Math.PI / 2);
                return Math.max(1e-5, Math.min(1, f * f));
            };
            var r = rng(419), eps = [], i;
            for (i = 0; i < n; i++) eps.push(normal(r));
            var ab = abar(t);
            var xt = x0.map(function (v, i) {
                return Math.sqrt(ab) * v + Math.sqrt(1 - ab) * eps[i];
            });
            /* The reverse step, given a perfect noise prediction: recover x0.
             * A real model predicts eps; this hands it the true one, which is
             * the target it is trained on. */
            var x0hat = xt.map(function (v, i) {
                return (v - Math.sqrt(1 - ab) * eps[i]) / Math.sqrt(ab);
            });

            var a = Plot(view.canvas(0), { xr: [0, n], yr: [-3.4, 3.4], height: 220,
                                           pad: { l: 46, r: 12, t: 12, b: 30 } });
            a.axes("position", "value");
            a.line(x0.map(function (v, i) { return [i, v]; }), M(), 1.5);
            a.line(xt.map(function (v, i) { return [i, v]; }), A(), 1.8);

            var curve = [], s;
            for (s = 0; s <= T; s++) curve.push([s, abar(s)]);
            var b = Plot(view.canvas(1), { xr: [0, T], yr: [0, 1], height: 200,
                                           pad: { l: 52, r: 12, t: 12, b: 32 } });
            b.axes("step t", "alpha-bar (signal kept)");
            b.line(curve, F(), 2.2);
            b.dot(t, ab, A(), 5);
            b.ring(t, ab, A(), 9);

            return {
                readout: "step " + t + " of " + T + ": alpha-bar " + ab.toFixed(3) +
                         ", so " + (100 * Math.sqrt(ab)).toFixed(0) + "% signal and " +
                         (100 * Math.sqrt(1 - ab)).toFixed(0) + "% noise by amplitude.  " +
                         "Recovering x0 from this exact noise gives error " +
                         mse(x0, x0hat).toExponential(1) +
                         " - the forward process is invertible IF you know the noise, " +
                         "and predicting it is the model's entire job."
            };
        }
    };

    window.VizDLDemos = DEMOS;
})();

/* The training-practice half: representation learning, decoding, and the
 * three engineering pages. */
(function () {
    "use strict";
    var V = window.VizML, DEMOS = window.VizDLDemos;
    var Plot = V.Plot, rng = V.rng, normal = V.normal, css = V.css;

    var A = function () { return css("--accent-primary", "#b06d10"); };
    var F = function () { return css("--accent-fill", "#e0982f"); };
    var M = function () { return css("--text-muted", "#8a9096"); };

    /* Contrastive learning: an anchor, its positive, and a field of negatives,
     * with the InfoNCE loss computed over them. */
    DEMOS.contrastive = function (p, view) {
        var r = rng(p.seed || 421), n = p.negatives | 0, tau = p.temperature;
        var anchor = [0.9, 0.4];
        var norm = function (v) { var d = Math.hypot(v[0], v[1]) || 1; return [v[0] / d, v[1] / d]; };
        anchor = norm(anchor);
        var pos = norm([anchor[0] + normal(r) * p.jitter, anchor[1] + normal(r) * p.jitter]);
        /* Negatives are drawn away from the anchor's immediate neighbourhood.
         * On a 2-D circle, random directions crowd: with 24 of them the
         * nearest sits within a couple of degrees of the anchor and is
         * indistinguishable from the positive, which is an artefact of the
         * two dimensions rather than anything contrastive learning does. Real
         * encoders work in hundreds of dimensions, where random vectors are
         * very nearly orthogonal and no such crowding occurs. */
        var negs = [], i, guard = Math.cos(0.55);
        for (i = 0; i < n; i++) {
            var q = norm([normal(r), normal(r)]);
            var tries = 0;
            while (q[0] * anchor[0] + q[1] * anchor[1] > guard && tries++ < 40)
                q = norm([normal(r), normal(r)]);
            negs.push(q);
        }

        var sim = function (a, b) { return a[0] * b[0] + a[1] * b[1]; };
        var sPos = sim(anchor, pos);
        var exps = negs.map(function (q) { return Math.exp(sim(anchor, q) / tau); });
        var denom = Math.exp(sPos / tau) + exps.reduce(function (a, b) { return a + b; }, 0);
        var loss = -Math.log(Math.exp(sPos / tau) / denom);
        var hardest = negs.reduce(function (m, q) { return sim(anchor, q) > sim(anchor, m) ? q : m; }, negs[0]);

        var plot = Plot(view.canvas(0), { xr: [-1.4, 1.4], yr: [-1.15, 1.15], height: 300 });
        plot.axes("dimension 1", "dimension 2");
        var circle = [], k;
        for (k = 0; k <= 90; k++) {
            var t = k / 90 * 2 * Math.PI;
            circle.push([Math.cos(t), Math.sin(t)]);
        }
        plot.line(circle, M(), 1.2, [4, 4]);
        negs.forEach(function (q) { plot.dot(q[0], q[1], M(), 2.8); });
        plot.dot(hardest[0], hardest[1], F(), 4);
        plot.line([[0, 0], anchor], A(), 2.4);
        plot.line([[0, 0], pos], F(), 2.4);
        plot.dot(anchor[0], anchor[1], A(), 5.5);
        plot.ring(anchor[0], anchor[1], A(), 9);
        plot.dot(pos[0], pos[1], F(), 5);

        return {
            readout: "similarity to the positive " + sPos.toFixed(3) +
                     ", to the hardest negative " + sim(anchor, hardest).toFixed(3) +
                     ".  InfoNCE loss " + loss.toFixed(3) + " over " + n + " negatives at " +
                     "temperature " + tau.toFixed(2) + ".  " +
                     (tau < 0.12
                        ? "A low temperature makes the loss dominated by the single hardest negative."
                        : (tau > 0.6
                            ? "A high temperature flattens the comparison until every negative counts about the same, and the loss stops discriminating."
                            : "The temperature sets how much the hardest negatives dominate."))
        };
    };

    /* Beam search, actually searched: a small scored tree, expanded to a
     * chosen beam width, with the greedy path shown against the best. */
    DEMOS.beamsearch = function (p, view) {
        var width = p.width | 0, depth = 5, branch = 3;
        var r = rng(p.seed || 431);
        /* A fixed random scoring tree. Deterministic per seed, so widening the
         * beam is the only thing that changes the answer. */
        var score = {};
        var logp = function (path) {
            if (!(path in score)) score[path] = -Math.abs(normal(rng(hash(path)))) * 1.1 - 0.05;
            return score[path];
        };
        function hash(s) {
            var h = 2166136261, i;
            for (i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
            return (h >>> 0) % 100000 + 1;
        }

        var beams = [{ path: "", total: 0 }], d, history = [];
        for (d = 0; d < depth; d++) {
            var cand = [];
            beams.forEach(function (b) {
                for (var c = 0; c < branch; c++) {
                    var np = b.path + String(c);
                    cand.push({ path: np, total: b.total + logp(np) });
                }
            });
            cand.sort(function (a, b) { return b.total - a.total; });
            beams = cand.slice(0, width);
            history.push(beams.map(function (b) { return b.total; }));
        }
        var best = beams[0];

        // greedy: width 1, same tree
        var g = { path: "", total: 0 };
        for (d = 0; d < depth; d++) {
            var bestC = null;
            for (var c = 0; c < branch; c++) {
                var np = g.path + String(c);
                var t = g.total + logp(np);
                if (!bestC || t > bestC.total) bestC = { path: np, total: t };
            }
            g = bestC;
        }

        var plot = Plot(view.canvas(0), { xr: [1, depth], yr: [-6, 0], height: 280,
                                          pad: { l: 54, r: 12, t: 12, b: 34 } });
        plot.axes("token position", "cumulative log probability", 4);
        var k;
        for (k = 0; k < width; k++) {
            var line = history.map(function (h, i) { return [i + 1, h[k] === undefined ? h[h.length - 1] : h[k]]; });
            plot.line(line, k === 0 ? A() : M(), k === 0 ? 2.4 : 1.2);
        }
        plot.dot(depth, best.total, A(), 5);

        return {
            readout: "beam width " + width + ": best sequence scores " + best.total.toFixed(3) +
                     ".  Greedy decoding scores " + g.total.toFixed(3) +
                     (best.total > g.total + 1e-9
                        ? " - worse, because it committed to a high first token that led nowhere."
                        : " - the same path this time; a wider beam is not always a better answer.") +
                     "  Cost grows linearly with the width, and so does the tendency toward bland, high-probability text."
        };
    };

    /* An embedding layer: one-hot times a matrix, which is a row lookup. */
    DEMOS.embedding = function (p, view) {
        var vocab = p.vocab | 0, dim = p.dim | 0;
        var dense = vocab * dim;
        var onehot = vocab;                    // width of the one-hot input
        var plot = Plot(view.canvas(0), { xr: [0, 3], yr: [0, 1], height: 250,
                                          pad: { l: 54, r: 12, t: 16, b: 40 } });
        plot.axes("", "relative cost", 3);
        var maxc = Math.max(dense, vocab * vocab);
        plot.bar(0.2, 0.8, dense / maxc, F());
        plot.bar(1.2, 1.8, (vocab * vocab) / maxc, M());
        plot.bar(2.2, 2.8, dim / maxc, A());
        var ctx = plot.ctx;
        ctx.fillStyle = css("--text-muted", "#999");
        ctx.font = "10px " + css("--vz-mono", "monospace");
        ctx.textAlign = "center";
        ["embedding table", "one-hot matmul", "one row"].forEach(function (t, i) {
            ctx.fillText(t, plot.px(i + 0.5), plot.h - 18);
        });

        return {
            readout: "vocabulary " + vocab.toLocaleString() + ", dimension " + dim +
                     ".  The table holds " + dense.toLocaleString() + " weights.  " +
                     "Multiplying a one-hot vector by it would touch " +
                     (vocab * dim).toLocaleString() + " numbers to retrieve " + dim +
                     " of them - which is why every framework implements this as a row " +
                     "lookup instead, and why the layer is called an embedding rather " +
                     "than a matmul."
        };
    };

    /* Float16 range and precision, and what loss scaling does about it. */
    DEMOS.precision = function (p, view) {
        var scale = Math.pow(2, p.logScale);
        /* fp16: 5 exponent bits, 10 mantissa bits. Smallest normal 2^-14,
         * smallest subnormal 2^-24, max 65504. */
        var MIN_SUB = Math.pow(2, -24), MIN_NORM = Math.pow(2, -14), MAX = 65504;
        var r = rng(439), grads = [], i;
        for (i = 0; i < 3000; i++) {
            // gradients spread over many orders of magnitude, as they are
            var mag = Math.pow(10, -p.spread * Math.abs(normal(r)) - 2);
            grads.push(mag);
        }
        var under = 0, over = 0;
        grads.forEach(function (g) {
            var s = g * scale;
            if (s < MIN_SUB) under++;
            else if (s > MAX) over++;
        });

        var plot = Plot(view.canvas(0), { xr: [-12, 6], yr: [0, 1], height: 260,
                                          pad: { l: 52, r: 12, t: 12, b: 34 } });
        plot.axes("log10 of the scaled gradient", "frequency");
        var bins = 48, hist = new Array(bins).fill(0);
        grads.forEach(function (g) {
            var b = Math.floor((Math.log10(g * scale) + 12) / 18 * bins);
            if (b >= 0 && b < bins) hist[b]++;
        });
        var max = Math.max.apply(null, hist) || 1;
        hist.forEach(function (c, b) {
            plot.bar(-12 + b * 18 / bins, -12 + (b + 0.86) * 18 / bins, c / max, F());
        });
        plot.vline(Math.log10(MIN_SUB), A(), "fp16 underflow");
        plot.vline(Math.log10(MAX), A(), "fp16 overflow");

        return {
            readout: "loss scale 2^" + p.logScale + " = " + scale.toLocaleString() +
                     ".  Of 3000 gradients, " + under + " underflow to zero and " +
                     over + " overflow to infinity in fp16.  " +
                     /* Any underflow at all is a parameter receiving no
                      * update, so the verdict keys off zero rather than off a
                      * threshold. An earlier version called 43 vanished
                      * gradients "everything fits", which contradicted the
                      * number printed in the same sentence. */
                     (over > 0
                        ? "Too large: some gradients have become infinite, and the step must be skipped."
                        : (under > 0
                            ? "Those " + under + " parameters get no update at all this step - not a small one, none. Raise the scale."
                            : "Nothing lost at either end. Dynamic loss scaling finds this window automatically by raising the scale until an overflow occurs, then backing off."))
        };
    };

    /* Gradient accumulation: the same effective batch, traded against memory. */
    DEMOS.accumulation = function (p, view) {
        var effective = p.effective | 0, micro = p.micro | 0;
        var steps = Math.max(1, Math.round(effective / micro));
        var actual = steps * micro;
        /* Activation memory scales with the micro-batch; parameters and
         * optimiser state do not. */
        var perSample = 42;      // MB of activations per sample, illustrative
        var fixed = 1800;        // MB of weights, gradients and optimiser state
        var memMicro = fixed + micro * perSample;
        var memFull = fixed + effective * perSample;
        var budget = p.budget * 1024;

        var plot = Plot(view.canvas(0), { xr: [0, 2], yr: [0, Math.max(memFull, budget) * 1.1],
                                          height: 260, pad: { l: 66, r: 12, t: 12, b: 40 } });
        plot.axes("", "memory (MB)", 4);
        plot.bar(0.2, 0.8, memFull, memFull > budget ? A() : M());
        plot.bar(1.2, 1.8, memMicro, memMicro > budget ? A() : F());
        var ctx = plot.ctx;
        ctx.fillStyle = css("--text-muted", "#999");
        ctx.font = "10px " + css("--vz-mono", "monospace");
        ctx.textAlign = "center";
        ctx.fillText("batch " + effective + " at once", plot.px(0.5), plot.h - 18);
        ctx.fillText("micro-batch " + micro + " x " + steps, plot.px(1.5), plot.h - 18);
        plot.ctx.strokeStyle = A();
        plot.ctx.setLineDash([5, 4]);
        plot.ctx.beginPath();
        plot.ctx.moveTo(plot.px(0), plot.py(budget));
        plot.ctx.lineTo(plot.px(2), plot.py(budget));
        plot.ctx.stroke();
        plot.ctx.setLineDash([]);

        return {
            readout: steps + " micro-batches of " + micro + " give an effective batch of " +
                     actual + (actual !== effective ? " (rounded from " + effective + ")" : "") +
                     ".  Peak memory " + (memMicro / 1024).toFixed(1) + " GB against " +
                     (memFull / 1024).toFixed(1) + " GB for the whole batch at once, on a " +
                     p.budget + " GB budget.  " +
                     (memFull <= budget
                        ? "The full batch already fits; accumulation would only make it slower."
                        : (memMicro <= budget
                            ? "The full batch does not fit and the micro-batch does - which is the entire reason to accumulate."
                            : "Even the micro-batch does not fit. Reduce it further, or use activation checkpointing."))
        };
    };

    /* Label smoothing: what it does to the target, and to confidence. */
    DEMOS.smoothing = function (p, view) {
        var K = p.classes | 0, eps = p.epsilon;
        var target = [];
        for (var i = 0; i < K; i++) target.push(i === 0 ? 1 - eps + eps / K : eps / K);

        var plot = Plot(view.canvas(0), { xr: [-0.6, K - 0.4], yr: [0, 1.1], height: 250,
                                          pad: { l: 54, r: 12, t: 12, b: 34 } });
        plot.axes("class", "target probability");
        target.forEach(function (t, i) {
            plot.bar(i - 0.36, i + 0.36, t, i === 0 ? F() : M());
        });

        /* The optimal logit gap under a smoothed target is finite, where under
         * a hard target it is unbounded - which is the whole mechanism. */
        var pTrue = target[0], pOther = target[1] || 1e-9;
        var gap = Math.log(pTrue / pOther);
        var loss = -(pTrue * Math.log(pTrue) + (K - 1) * pOther * Math.log(pOther));
        return {
            readout: "epsilon " + eps.toFixed(2) + " over " + K + " classes: target " +
                     pTrue.toFixed(3) + " on the true class, " + pOther.toFixed(4) +
                     " on each of the rest.  " +
                     (eps < 0.005
                        ? "A hard target. The optimal logit gap is infinite, so training pushes confidence up forever and the model ends up badly calibrated."
                        : "The optimal logit gap is now finite at " + gap.toFixed(2) +
                          " - the model has a reason to stop becoming more confident, which is what improves calibration.") +
                     "  Minimum achievable loss " + loss.toFixed(3) + ", not zero."
        };
    };
})();

/* Mount, and it has to be last in this file.
 *
 * These scripts are deferred, so the document is already "interactive" by the
 * time any of this runs and init() fires immediately rather than waiting for
 * DOMContentLoaded. A mount block sitting above a demo registration therefore
 * runs before it, and the page comes up blank. That happened twice on the
 * other two harnesses; the rule since is that the mount goes last.
 */
(function () {
    "use strict";
    var DEMOS = window.VizDLDemos;

    function control(spec, onChange) {
        var wrap = document.createElement("label");
        wrap.className = "ml-control";
        var name = document.createElement("span");
        name.className = "ml-control-name";
        name.textContent = spec.label;
        var value = document.createElement("span");
        value.className = "ml-control-value";
        wrap.appendChild(name); wrap.appendChild(value);

        var input;
        if (spec.type === "select") {
            input = document.createElement("select");
            spec.options.forEach(function (o) {
                var op = document.createElement("option");
                op.value = o.value; op.textContent = o.label;
                input.appendChild(op);
            });
            input.value = spec.value;
        } else {
            input = document.createElement("input");
            input.type = "range";
            input.min = spec.min; input.max = spec.max;
            input.step = spec.step || 1; input.value = spec.value;
            value.textContent = input.value;
        }
        input.className = "ml-input";
        wrap.appendChild(input);

        function read() {
            if (spec.type === "select") return input.value;
            value.textContent = input.value;
            return parseFloat(input.value);
        }
        input.addEventListener("input", function () { onChange(spec.key, read()); });
        input.addEventListener("change", function () { onChange(spec.key, read()); });
        return wrap;
    }

    function mount(root) {
        var cfgEl = root.querySelector(".ml-config");
        if (!cfgEl) return;
        var cfg;
        try { cfg = JSON.parse(cfgEl.textContent); } catch (e) { return; }
        var demo = DEMOS[cfg.demo];
        if (!demo) return;

        var params = {};
        (cfg.controls || []).forEach(function (c) { params[c.key] = c.value; });
        Object.keys(cfg.fixed || {}).forEach(function (k) { params[k] = cfg.fixed[k]; });

        root.innerHTML = "";
        var stage = document.createElement("div");
        stage.className = "ml-stage" + ((cfg.canvases || 1) > 1 ? " ml-stage-2" : "");
        var canvases = [];
        for (var i = 0; i < (cfg.canvases || 1); i++) {
            var fig = document.createElement("figure");
            fig.className = "ml-pane";
            var c = document.createElement("canvas");
            c.className = "ml-canvas";
            fig.appendChild(c);
            if (cfg.captions && cfg.captions[i]) {
                var cap = document.createElement("figcaption");
                cap.textContent = cfg.captions[i];
                fig.appendChild(cap);
            }
            stage.appendChild(fig);
            canvases.push(c);
        }
        root.appendChild(stage);

        var panel = document.createElement("div");
        panel.className = "ml-controls";
        (cfg.controls || []).forEach(function (spec) {
            panel.appendChild(control(spec, function (k, v) { params[k] = v; schedule(); }));
        });

        var readout = document.createElement("p");
        readout.className = "ml-readout";
        readout.setAttribute("aria-live", "polite");

        if (cfg.drag) {
            var hint = document.createElement("p");
            hint.className = "ml-hint";
            hint.textContent = cfg.drag.hint ||
                "Drag on the chart to move the nearer vector.";
            root.appendChild(hint);
        }
        root.appendChild(panel);
        root.appendChild(readout);

        var view = { canvas: function (i) { return canvases[i] || canvases[0]; },
                     table: function () {} };

        var queued = false;
        function schedule() {
            if (queued) return;
            queued = true;
            requestAnimationFrame(function () { queued = false; render(); });
        }
        function render() {
            var res = demo(params, view) || {};
            readout.textContent = res.readout || "";
        }

        /* The basis module is dragged rather than sliddered: the argument is
         * about what two vectors do to each other, and two pairs of sliders
         * hide that they are vectors at all. */
        if (cfg.drag) {
            var c0 = canvases[0], dragging = false;
            var toData = function (ev) {
                var rect = c0.getBoundingClientRect();
                var pad = { l: 42, r: 12, t: 12, b: 30 };
                var px = ev.clientX - rect.left, py = ev.clientY - rect.top;
                var xr = cfg.drag.xr, yr = cfg.drag.yr;
                return [xr[0] + (px - pad.l) / (rect.width - pad.l - pad.r) * (xr[1] - xr[0]),
                        yr[0] + (rect.height - pad.b - py) / (rect.height - pad.t - pad.b) * (yr[1] - yr[0])];
            };
            var move = function (ev) {
                if (!dragging) return;
                var d = toData(ev);
                // Whichever vector tip is nearer is the one being moved.
                var d1 = Math.hypot(d[0] - params.x1, d[1] - params.y1);
                var d2 = Math.hypot(d[0] - params.x2, d[1] - params.y2);
                var k = d1 <= d2 ? ["x1", "y1"] : ["x2", "y2"];
                params[k[0]] = Math.max(cfg.drag.xr[0], Math.min(cfg.drag.xr[1], d[0]));
                params[k[1]] = Math.max(cfg.drag.yr[0], Math.min(cfg.drag.yr[1], d[1]));
                schedule();
                ev.preventDefault();
            };
            c0.style.touchAction = "none";
            c0.addEventListener("pointerdown", function (ev) {
                dragging = true; c0.setPointerCapture(ev.pointerId); move(ev);
            });
            c0.addEventListener("pointermove", move);
            c0.addEventListener("pointerup", function () { dragging = false; });
            c0.addEventListener("pointercancel", function () { dragging = false; });
        }

        render();
        window.addEventListener("resize", schedule);
        root.dataset.vzDlReady = "1";
    }

    function init() {
        Array.prototype.forEach.call(
            document.querySelectorAll("[data-vz-dl]"), mount);
    }
    if (document.readyState === "loading")
        document.addEventListener("DOMContentLoaded", init);
    else init();
})();
