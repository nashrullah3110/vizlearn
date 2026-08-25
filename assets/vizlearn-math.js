/* Interactive demonstrations for the generated maths/ modules.
 *
 * The maths track was the thinnest on the site and the one most depended on:
 * PCA assumes an eigendecomposition and an SVD, gradient descent assumes
 * convexity, and half the evaluation pages assume a sampling distribution.
 * Only the first of those was taught anywhere.
 *
 * These are demonstrations rather than simulations. Nothing is fitted; the
 * arithmetic is the subject. The SVD is a real SVD of the matrix the reader
 * is editing, the central limit demonstration really resamples the population
 * on screen, and the Taylor series really sums its terms.
 *
 * The plotter and the RNG come from vizlearn-plot.js, shared with the machine
 * learning harness.
 *
 * Binds to [data-vz-math]; costs nothing on a page that has none.
 */
(function () {
    "use strict";
    var V = window.VizML;
    var Plot = V.Plot, rng = V.rng, normal = V.normal, css = V.css, mean = V.mean;

    var A = function () { return css("--accent-primary", "#b06d10"); };
    var F = function () { return css("--accent-fill", "#e0982f"); };
    var M = function () { return css("--text-muted", "#8a9096"); };

    // ---------------------------------------------------------- linear algebra

    function matmul2(m, v) {
        return [m[0] * v[0] + m[1] * v[1], m[2] * v[0] + m[3] * v[1]];
    }

    /* SVD of a 2x2 by eigendecomposition of A'A. Closed form, because at this
     * size an iterative solver would obscure the thing being demonstrated. */
    function svd2(a, b, c, d) {
        var e = (a + d) / 2, f = (a - d) / 2, g = (c + b) / 2, h = (c - b) / 2;
        var q = Math.hypot(e, h), r = Math.hypot(f, g);
        var s1 = q + r, s2 = Math.abs(q - r);
        var a1 = Math.atan2(g, f), a2 = Math.atan2(h, e);
        var theta = (a2 - a1) / 2, phi = (a2 + a1) / 2;
        return { s: [s1, s2], theta: theta, phi: phi };
    }

    function rot(t) { return [Math.cos(t), -Math.sin(t), Math.sin(t), Math.cos(t)]; }

    // ------------------------------------------------------------- statistics

    /* A population deliberately nothing like a normal: two humps and a tail.
     * The central limit demonstration is only convincing if the thing being
     * sampled is visibly not the thing the sample means turn into. */
    function population(seed) {
        var r = rng(seed || 211), out = [], i;
        for (i = 0; i < 4000; i++) {
            var u = r();
            if (u < 0.45) out.push(1 + r() * 1.2);
            else if (u < 0.85) out.push(5.5 + r() * 1.4);
            else out.push(7 + Math.pow(r(), 0.35) * 4);
        }
        return out;
    }

    function histogram(data, lo, hi, bins) {
        var h = new Array(bins).fill(0), i;
        for (i = 0; i < data.length; i++) {
            var b = Math.floor((data[i] - lo) / (hi - lo) * bins);
            if (b >= 0 && b < bins) h[b]++;
        }
        return h;
    }

    function drawHist(plot, h, lo, hi, colour, scale) {
        var w = (hi - lo) / h.length;
        h.forEach(function (c, i) {
            plot.bar(lo + i * w, lo + (i + 0.86) * w, c * scale, colour);
        });
    }

    function quantile(sorted, q) {
        if (!sorted.length) return NaN;
        var pos = (sorted.length - 1) * q;
        var lo = Math.floor(pos), hi = Math.ceil(pos);
        return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
    }

    // ------------------------------------------------------------------ demos

    var DEMOS = {

        /* Two vectors the reader drags. What they span, and what happens to it
         * when they line up. */
        basis: function (p, view) {
            var v1 = [p.x1, p.y1], v2 = [p.x2, p.y2];
            var plot = Plot(view.canvas(0), { xr: [-4, 4], yr: [-3, 3], height: 300 });
            plot.axes("x", "y");
            var det = v1[0] * v2[1] - v1[1] * v2[0];
            var dot = v1[0] * v2[0] + v1[1] * v2[1];
            var n1 = Math.hypot(v1[0], v1[1]), n2 = Math.hypot(v2[0], v2[1]);
            var cos = (n1 * n2) ? dot / (n1 * n2) : 0;

            // The parallelogram the two vectors span. Its area IS |det|.
            var ctx = plot.ctx;
            ctx.fillStyle = F();
            ctx.globalAlpha = 0.16;
            ctx.beginPath();
            ctx.moveTo(plot.px(0), plot.py(0));
            ctx.lineTo(plot.px(v1[0]), plot.py(v1[1]));
            ctx.lineTo(plot.px(v1[0] + v2[0]), plot.py(v1[1] + v2[1]));
            ctx.lineTo(plot.px(v2[0]), plot.py(v2[1]));
            ctx.closePath();
            ctx.fill();
            ctx.globalAlpha = 1;

            if (Math.abs(det) < 0.12) {
                // Degenerate: the span is a line, so draw the line they share.
                var k = n1 > n2 ? v1 : v2;
                var L = 8 / (Math.hypot(k[0], k[1]) || 1);
                plot.line([[-k[0] * L, -k[1] * L], [k[0] * L, k[1] * L]], M(), 1.4, [5, 4]);
            }
            plot.line([[0, 0], v1], A(), 2.6);
            plot.line([[0, 0], v2], F(), 2.6);
            plot.dot(v1[0], v1[1], A(), 4.5);
            plot.dot(v2[0], v2[1], F(), 4.5);

            var deg = Math.acos(Math.max(-1, Math.min(1, cos))) * 180 / Math.PI;
            var verdict = Math.abs(det) < 0.12
                ? "linearly dependent - they span a line, not the plane"
                : (Math.abs(dot) < 0.08 * n1 * n2
                    ? "orthogonal, and a basis - the cleanest kind"
                    : "a basis, but not an orthogonal one");
            return {
                readout: "angle " + deg.toFixed(1) + " degrees, dot product " + dot.toFixed(2) +
                         ", determinant " + det.toFixed(2) + " (the shaded area).  " + verdict + "."
            };
        },

        /* SVD as rotate, stretch, rotate - performed on a shape, one stage at
         * a time, plus the rank-1 reconstruction. */
        svd: function (p, view) {
            var m = [p.a, p.b, p.c, p.d];
            var f = svd2(m[0], m[1], m[2], m[3]);
            var shape = [], i;
            for (i = 0; i <= 64; i++) {
                var t = i / 64 * 2 * Math.PI;
                shape.push([Math.cos(t), Math.sin(t)]);
            }
            var spokes = [[1, 0], [0, 1]];

            var stage = p.stage;
            var apply = function (v) {
                if (stage === "input") return v;
                var out = matmul2(rot(-f.phi), v);                 // V'
                if (stage === "rotate1") return out;
                out = [out[0] * f.s[0], out[1] * f.s[1]];          // Sigma
                if (stage === "stretch") return out;
                return matmul2(rot(f.theta), out);                 // U
            };
            var lim = Math.max(2, f.s[0] * 1.2);
            var plot = Plot(view.canvas(0), { xr: [-lim, lim], yr: [-lim * 0.75, lim * 0.75],
                                              height: 300 });
            plot.axes("x", "y");
            plot.line(shape.map(apply), A(), 2.2);
            spokes.forEach(function (s, k) {
                plot.line([[0, 0], apply(s)], k ? F() : M(), 2);
            });

            var names = { input: "the unit circle, untouched",
                          rotate1: "after V' - a rotation, so the circle is unchanged",
                          stretch: "after Sigma - stretched by the singular values",
                          full: "after U - rotated into place. This is the full matrix." };
            return {
                readout: "singular values " + f.s[0].toFixed(2) + " and " + f.s[1].toFixed(2) +
                         ", condition number " +
                         (f.s[1] > 1e-6 ? (f.s[0] / f.s[1]).toFixed(1) : "infinite") +
                         ".  " + names[stage]
            };
        },

        /* A surface, its gradient, and the curvature the Hessian records. */
        curvature: function (p, view) {
            var k = p.curve;
            var f = function (x) { return k * x * x + p.slope * x; };
            var df = function (x) { return 2 * k * x + p.slope; };
            var pts = [], x;
            for (x = -3; x <= 3; x += 0.05) pts.push([x, f(x)]);
            var lo = Math.min.apply(null, pts.map(function (q) { return q[1]; }));
            var hi = Math.max.apply(null, pts.map(function (q) { return q[1]; }));
            var plot = Plot(view.canvas(0), { xr: [-3, 3], yr: [lo - 1, hi + 1], height: 290,
                                              pad: { l: 52, r: 12, t: 12, b: 32 } });
            plot.axes("x", "f(x)");
            plot.line(pts, A(), 2.2);
            var at = p.at, y = f(at), g = df(at);
            plot.line([[at - 1.4, y - g * 1.4], [at + 1.4, y + g * 1.4]], F(), 2, [5, 4]);
            plot.dot(at, y, F(), 5);

            var second = 2 * k;
            var what = second > 0.05 ? "positive - a minimum lies this way, and a big step is safe"
                     : (second < -0.05 ? "negative - this is a maximum direction; descent will run away"
                                       : "zero - flat curvature, and no scale to choose a step from");
            return {
                readout: "gradient " + g.toFixed(2) + " (the dashed tangent), second derivative " +
                         second.toFixed(2) + ".  Curvature is " + what + "."
            };
        },

        /* Convex against non-convex, with gradient descent actually run. */
        convexity: function (p, view) {
            var wob = p.bumpiness;
            var f = function (x) { return 0.35 * x * x + wob * Math.sin(3 * x) * 1.4; };
            var df = function (x) { return 0.7 * x + wob * 4.2 * Math.cos(3 * x); };
            var pts = [], x;
            for (x = -5; x <= 5; x += 0.04) pts.push([x, f(x)]);
            var lo = Math.min.apply(null, pts.map(function (q) { return q[1]; }));
            var hi = Math.max.apply(null, pts.map(function (q) { return q[1]; }));
            var plot = Plot(view.canvas(0), { xr: [-5, 5], yr: [lo - 0.6, hi + 0.6], height: 290,
                                              pad: { l: 52, r: 12, t: 12, b: 32 } });
            plot.axes("x", "f(x)");
            plot.line(pts, A(), 2.2);

            var pos = p.start, path = [[pos, f(pos)]], i;
            for (i = 0; i < 80; i++) {
                pos = pos - p.lr * df(pos);
                if (!isFinite(pos)) break;
                path.push([pos, f(pos)]);
            }
            path.forEach(function (q, i) {
                if (i % 4 === 0) plot.dot(q[0], q[1], M(), 2.4);
            });
            plot.dot(path[0][0], path[0][1], F(), 5);
            plot.ring(path[0][0], path[0][1], F(), 8);
            var end = path[path.length - 1];
            plot.dot(end[0], end[1], A(), 5.5);
            plot.ring(end[0], end[1], A(), 9);

            // The true minimum, found by brute force over the same grid.
            var best = pts.reduce(function (m, q) { return q[1] < m[1] ? q : m; }, pts[0]);
            var stuck = Math.abs(end[0] - best[0]) > 0.35;
            return {
                readout: (wob < 0.02
                    ? "Convex: one minimum, and every starting point reaches it."
                    : "Not convex. ") +
                    "  Descent started at " + p.start.toFixed(1) + " and settled at " +
                    end[0].toFixed(2) + "; the true minimum is at " + best[0].toFixed(2) + ". " +
                    (stuck ? " It is stuck in a local minimum - move the start and watch the answer change."
                           : " It found the global minimum this time.")
            };
        },

        /* Taylor series, summed term by term. */
        taylor: function (p, view) {
            var about = p.about, n = p.terms | 0;
            var fn = p.fn;
            var truth = fn === "sin" ? Math.sin
                      : (fn === "exp" ? Math.exp
                                      : function (x) { return 1 / (1 + x * x); });
            // Derivatives at `about`, by repeated central differences - honest,
            // and enough for the handful of terms on offer here.
            var deriv = function (g, order, x) {
                if (order === 0) return g(x);
                var h = 0.02;
                return (deriv(g, order - 1, x + h) - deriv(g, order - 1, x - h)) / (2 * h);
            };
            var coeff = [], fact = 1, k;
            for (k = 0; k <= n; k++) {
                if (k > 0) fact *= k;
                coeff.push(deriv(truth, k, about) / fact);
            }
            var approx = function (x) {
                var s = 0, d = 1;
                for (var k = 0; k <= n; k++) { s += coeff[k] * d; d *= (x - about); }
                return s;
            };
            var T = [], Ap = [], x;
            for (x = -6; x <= 6; x += 0.05) {
                T.push([x, truth(x)]);
                var a = approx(x);
                Ap.push([x, Math.max(-6, Math.min(6, a))]);
            }
            var plot = Plot(view.canvas(0), { xr: [-6, 6], yr: [-3, 4], height: 290 });
            plot.axes("x", "f(x)");
            plot.line(T, M(), 2.4);
            plot.line(Ap, A(), 2.2);
            plot.dot(about, truth(about), F(), 5);

            // Where the approximation is still within 0.1 of the truth.
            var good = 0;
            for (x = 0; x <= 6; x += 0.05)
                if (Math.abs(approx(about + x) - truth(about + x)) < 0.1) good = x; else break;
            return {
                readout: n + (n === 1 ? " term" : " terms") + " about x = " + about.toFixed(1) +
                         ".  The approximation holds to within 0.1 for about " +
                         good.toFixed(2) + " either side - each term buys a little more reach, " +
                         "and never the whole line."
            };
        }
    };

    window.VizMathDemos = DEMOS;
})();

/* The five probability and statistics demonstrations. */
(function () {
    "use strict";
    var V = window.VizML, DEMOS = window.VizMathDemos;
    var Plot = V.Plot, rng = V.rng, normal = V.normal, css = V.css;
    var mean = V.mean, sd = V.sd;

    var A = function () { return css("--accent-primary", "#b06d10"); };
    var F = function () { return css("--accent-fill", "#e0982f"); };
    var M = function () { return css("--text-muted", "#8a9096"); };

    function population(seed) {
        var r = rng(seed || 211), out = [], i;
        for (i = 0; i < 4000; i++) {
            var u = r();
            if (u < 0.45) out.push(1 + r() * 1.2);
            else if (u < 0.85) out.push(5.5 + r() * 1.4);
            else out.push(7 + Math.pow(r(), 0.35) * 4);
        }
        return out;
    }

    function hist(data, lo, hi, bins) {
        var h = new Array(bins).fill(0), i;
        for (i = 0; i < data.length; i++) {
            var b = Math.floor((data[i] - lo) / (hi - lo) * bins);
            if (b >= 0 && b < bins) h[b]++;
        }
        return h;
    }

    function drawHist(plot, h, lo, hi, colour) {
        var max = Math.max.apply(null, h) || 1;
        var w = (hi - lo) / h.length;
        h.forEach(function (c, i) {
            plot.bar(lo + i * w, lo + (i + 0.88) * w, c / max, colour);
        });
    }

    function quantile(sorted, q) {
        if (!sorted.length) return NaN;
        var pos = (sorted.length - 1) * q;
        var lo = Math.floor(pos), hi = Math.ceil(pos);
        return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
    }

    /* Expectation and variance, built from the definition on a die the reader
     * can load. */
    DEMOS.expectation = function (p, view) {
        var faces = [1, 2, 3, 4, 5, 6];
        var w = [p.w1, p.w2, p.w3, p.w4, p.w5, p.w6];
        var total = w.reduce(function (a, b) { return a + b; }, 0) || 1;
        var prob = w.map(function (x) { return x / total; });
        var ev = 0, i;
        for (i = 0; i < 6; i++) ev += faces[i] * prob[i];
        var varr = 0;
        for (i = 0; i < 6; i++) varr += prob[i] * (faces[i] - ev) * (faces[i] - ev);

        var plot = Plot(view.canvas(0), { xr: [0.5, 6.5], yr: [0, Math.max(0.5, Math.max.apply(null, prob) * 1.2)],
                                          height: 270, pad: { l: 54, r: 12, t: 12, b: 34 } });
        plot.axes("face", "probability", 6);
        prob.forEach(function (q, i) { plot.bar(i + 0.75, i + 1.25, q, F()); });
        plot.vline(ev, A(), "E[X] = " + ev.toFixed(2));
        return {
            readout: "E[X] = " + ev.toFixed(3) + ", Var(X) = " + varr.toFixed(3) +
                     ", SD = " + Math.sqrt(varr).toFixed(3) +
                     ".  The expectation need not be a face the die can land on - " +
                     "it is a weighted average, not a prediction."
        };
    };

    /* Bernoulli, binomial and Poisson, drawn from their own formulas. */
    DEMOS.discrete = function (p, view) {
        var kind = p.kind, n = p.n | 0, prob = p.p, lam = p.lam;
        var bars = [], k, hiK;
        var logFact = function (m) { var s = 0, i; for (i = 2; i <= m; i++) s += Math.log(i); return s; };
        if (kind === "bernoulli") {
            bars = [[0, 1 - prob], [1, prob]];
            hiK = 1;
        } else if (kind === "binomial") {
            hiK = n;
            for (k = 0; k <= n; k++) {
                var logp = logFact(n) - logFact(k) - logFact(n - k) +
                           k * Math.log(prob || 1e-12) + (n - k) * Math.log(1 - prob || 1e-12);
                bars.push([k, Math.exp(logp)]);
            }
        } else {
            hiK = Math.max(6, Math.ceil(lam + 4 * Math.sqrt(lam)));
            for (k = 0; k <= hiK; k++)
                bars.push([k, Math.exp(-lam + k * Math.log(lam || 1e-12) - logFact(k))]);
        }
        var top = Math.max.apply(null, bars.map(function (b) { return b[1]; }));
        var plot = Plot(view.canvas(0), { xr: [-0.6, hiK + 0.6], yr: [0, top * 1.15],
                                          height: 270, pad: { l: 58, r: 12, t: 12, b: 34 } });
        plot.axes("k", "P(X = k)");
        var wide = hiK > 24;
        bars.forEach(function (b) {
            plot.bar(b[0] - (wide ? 0.45 : 0.34), b[0] + (wide ? 0.45 : 0.34), b[1], F());
        });
        var ev = kind === "bernoulli" ? prob : (kind === "binomial" ? n * prob : lam);
        var vr = kind === "bernoulli" ? prob * (1 - prob)
               : (kind === "binomial" ? n * prob * (1 - prob) : lam);
        plot.vline(ev, A(), "mean " + ev.toFixed(2));
        var note = kind === "bernoulli"
            ? "One trial. Everything else on this page is built from repeating it."
            : (kind === "binomial"
                ? "n independent Bernoulli trials. Mean np, variance np(1-p)."
                : "The limit of a binomial as n grows and p shrinks with np fixed. Mean and variance are both lambda, which is why a Poisson count has no free spread parameter.");
        return {
            readout: "mean " + ev.toFixed(3) + ", variance " + vr.toFixed(3) + ".  " + note
        };
    };

    /* The central limit theorem, resampled live from a population that is
     * conspicuously not normal. */
    DEMOS.clt = function (p, view) {
        var pop = population(211), n = p.n | 0, draws = 1200;
        var r = rng(p.seed || 223), means = [], i, j;
        for (i = 0; i < draws; i++) {
            var s = 0;
            for (j = 0; j < n; j++) s += pop[Math.floor(r() * pop.length)];
            means.push(s / n);
        }
        var a = Plot(view.canvas(0), { xr: [0, 12], yr: [0, 1.15], height: 230 });
        a.axes("value", "frequency");
        drawHist(a, hist(pop, 0, 12, 44), 0, 12, M());

        var mu = mean(pop), sigma = sd(pop);
        var se = sigma / Math.sqrt(n);
        var lo = mu - 4 * se, hi = mu + 4 * se;
        var b = Plot(view.canvas(1), { xr: [lo, hi], yr: [0, 1.15], height: 230 });
        b.axes("sample mean", "frequency");
        drawHist(b, hist(means, lo, hi, 40), lo, hi, F());
        var curve = [], x;
        for (x = lo; x <= hi; x += (hi - lo) / 160)
            curve.push([x, Math.exp(-(x - mu) * (x - mu) / (2 * se * se))]);
        b.line(curve, A(), 2);

        return {
            readout: "population mean " + mu.toFixed(2) + ", SD " + sigma.toFixed(2) +
                     ".  With n = " + n + ", the sample means have SD " +
                     sd(means).toFixed(3) + " against a predicted " + se.toFixed(3) +
                     " (sigma over root n).  The population is two humps and a tail; " +
                     "the means are a normal curve, and nothing about the population changed."
        };
    };

    /* Quantiles, and the box plot assembled from them. */
    DEMOS.quantiles = function (p, view) {
        var pop = population(211);
        var r = rng(p.seed || 229), sample = [], i;
        for (i = 0; i < (p.n | 0); i++) sample.push(pop[Math.floor(r() * pop.length)]);
        var sorted = sample.slice().sort(function (a, b) { return a - b; });
        var q1 = quantile(sorted, 0.25), q2 = quantile(sorted, 0.5), q3 = quantile(sorted, 0.75);
        var iqr = q3 - q1;
        var loFence = q1 - 1.5 * iqr, hiFence = q3 + 1.5 * iqr;
        var inside = sorted.filter(function (x) { return x >= loFence && x <= hiFence; });
        var whiskLo = inside[0], whiskHi = inside[inside.length - 1];
        var outliers = sorted.filter(function (x) { return x < loFence || x > hiFence; });

        var plot = Plot(view.canvas(0), { xr: [0, 12], yr: [0, 1.15], height: 240 });
        plot.axes("value", "frequency");
        drawHist(plot, hist(sample, 0, 12, 44), 0, 12, M());
        [[q1, "Q1"], [q2, "median"], [q3, "Q3"]].forEach(function (q, i) {
            plot.vline(q[0], i === 1 ? A() : F(), q[1] + " " + q[0].toFixed(2));
        });

        var box = Plot(view.canvas(1), { xr: [0, 12], yr: [0, 1], height: 130,
                                         pad: { l: 42, r: 12, t: 20, b: 30 } });
        box.axes("value", "", 6);
        var ctx = box.ctx;
        ctx.strokeStyle = F(); ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.moveTo(box.px(whiskLo), box.py(0.5)); ctx.lineTo(box.px(q1), box.py(0.5));
        ctx.moveTo(box.px(q3), box.py(0.5)); ctx.lineTo(box.px(whiskHi), box.py(0.5));
        ctx.stroke();
        ctx.fillStyle = F(); ctx.globalAlpha = 0.22;
        ctx.fillRect(box.px(q1), box.py(0.78), box.px(q3) - box.px(q1), box.py(0.22) - box.py(0.78));
        ctx.globalAlpha = 1;
        ctx.strokeRect(box.px(q1), box.py(0.78), box.px(q3) - box.px(q1), box.py(0.22) - box.py(0.78));
        ctx.strokeStyle = A(); ctx.lineWidth = 2.4;
        ctx.beginPath();
        ctx.moveTo(box.px(q2), box.py(0.78)); ctx.lineTo(box.px(q2), box.py(0.22));
        ctx.stroke();
        outliers.forEach(function (x) { box.dot(x, 0.5, A(), 3); });

        return {
            readout: "n = " + sample.length + ".  Q1 " + q1.toFixed(2) + ", median " +
                     q2.toFixed(2) + ", Q3 " + q3.toFixed(2) + ", IQR " + iqr.toFixed(2) +
                     ".  Whiskers reach the furthest points within 1.5 IQR; " +
                     outliers.length + " point" + (outliers.length === 1 ? "" : "s") +
                     " fall outside and are drawn individually."
        };
    };

    /* The sampling distribution of the mean, and the standard error that
     * describes it - resampled rather than asserted. */
    DEMOS.sampling = function (p, view) {
        var pop = population(211), n = p.n | 0, reps = p.reps | 0;
        var r = rng(p.seed || 233), means = [], i, j;
        for (i = 0; i < reps; i++) {
            var s = 0;
            for (j = 0; j < n; j++) s += pop[Math.floor(r() * pop.length)];
            means.push(s / n);
        }
        var mu = mean(pop), sigma = sd(pop), se = sigma / Math.sqrt(n);
        var lo = mu - 4.2 * se, hi = mu + 4.2 * se;
        var a = Plot(view.canvas(0), { xr: [lo, hi], yr: [0, 1.15], height: 250 });
        a.axes("sample mean", "frequency");
        drawHist(a, hist(means, lo, hi, 40), lo, hi, F());
        a.vline(mu, A(), "population mean");

        // How the standard error shrinks with n - the point of the whole page.
        var curve = [], k;
        for (k = 2; k <= 200; k += 2) curve.push([k, sigma / Math.sqrt(k)]);
        var b = Plot(view.canvas(1), { xr: [0, 200], yr: [0, sigma / Math.sqrt(2) * 1.05],
                                       height: 230, pad: { l: 58, r: 12, t: 12, b: 34 } });
        b.axes("sample size n", "standard error");
        b.line(curve, A(), 2.2);
        b.dot(n, se, F(), 5);
        b.ring(n, se, F(), 9);

        return {
            readout: "observed SD of the " + reps + " sample means: " + sd(means).toFixed(3) +
                     ", predicted standard error " + se.toFixed(3) +
                     ".  Quadrupling n halves the standard error, which is why precision " +
                     "gets expensive: the curve flattens and every further gain costs " +
                     "four times as much data."
        };
    };
})();


/* Tier 2: inference, the rest of the linear algebra, and two counting pages.
 *
 * Same rule as tier 1 - the arithmetic is the subject, so it runs here. The
 * confidence-interval page really draws a thousand intervals and really counts
 * how many contain the mean; the Markov page really iterates the transition
 * matrix; Gram-Schmidt really orthogonalises the vectors on screen.
 */
(function () {
    "use strict";
    var V = window.VizML, DEMOS = window.VizMathDemos;
    var Plot = V.Plot, rng = V.rng, normal = V.normal, css = V.css;
    var mean = V.mean, sd = V.sd;

    var A = function () { return css("--accent-primary", "#b06d10"); };
    var F = function () { return css("--accent-fill", "#e0982f"); };
    var M = function () { return css("--text-muted", "#8a9096"); };

    /* Normal CDF via an Abramowitz-Stegun rational approximation. Accurate to
     * about 1e-7, which is well past what any readout here shows. */
    function phi(z) {
        var s = z < 0 ? -1 : 1;
        z = Math.abs(z) / Math.SQRT2;
        var t = 1 / (1 + 0.3275911 * z);
        var y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
                      - 0.284496736) * t + 0.254829592) * t * Math.exp(-z * z);
        return 0.5 * (1 + s * y);
    }

    function gauss(x, mu, sg) {
        return Math.exp(-(x - mu) * (x - mu) / (2 * sg * sg)) / (sg * Math.sqrt(2 * Math.PI));
    }

    /* Look a critical value up by number, not by object key.
     *
     * { 0.80: 1.2816 }[(0.8).toFixed(2)] misses, because JavaScript normalises
     * the literal key 0.80 to the string "0.8" while toFixed produces "0.80".
     * That silently fell back to the 95% value, so the 80% intervals and the
     * alpha = 0.10 threshold were both quietly using the wrong number while
     * looking entirely plausible. Matching numerically cannot do that.
     */
    function lookup(table, value, fallback) {
        for (var i = 0; i < table.length; i++)
            if (Math.abs(table[i][0] - value) < 1e-9) return table[i][1];
        return fallback;
    }

    /* Confidence intervals, by construction: draw many samples, build an
     * interval from each, and count how many cover the true mean. */
    DEMOS.confidence = function (p, view) {
        var mu = 10, sigma = 3, n = p.n | 0, conf = parseFloat(p.conf);
        var z = lookup([[0.80, 1.2816], [0.90, 1.6449], [0.95, 1.9600], [0.99, 2.5758]],
                       conf, 1.96);
        var r = rng(p.seed || 307), shown = 40, total = 1000;
        var covered = 0, bars = [], i, j;
        for (i = 0; i < total; i++) {
            /* Two passes, not the one-pass E[X^2] - E[X]^2 identity. That
             * identity subtracts two nearly equal large numbers here - values
             * around 10, variance 9 - and the cancellation was corrupting the
             * sample SD badly enough to push coverage the wrong way as n grew.
             * The expectation module warns about exactly this; it was worth
             * taking its own advice. */
            var draws = [], m = 0;
            for (j = 0; j < n; j++) { var x = mu + normal(r) * sigma; draws.push(x); m += x; }
            m /= n;
            var ss = 0;
            for (j = 0; j < n; j++) ss += (draws[j] - m) * (draws[j] - m);
            var sampleSd = Math.sqrt(ss / Math.max(1, n - 1));
            var half = z * sampleSd / Math.sqrt(n);
            var ok = (m - half) <= mu && mu <= (m + half);
            if (ok) covered++;
            if (i < shown) bars.push([m - half, m + half, ok]);
        }
        var plot = Plot(view.canvas(0), { xr: [mu - 4, mu + 4], yr: [0, shown + 1],
                                          height: 300, pad: { l: 44, r: 12, t: 12, b: 32 } });
        plot.axes("value", "interval", 4);
        var ctx = plot.ctx;
        bars.forEach(function (b, i) {
            ctx.strokeStyle = b[2] ? M() : A();
            ctx.lineWidth = b[2] ? 1.4 : 2.4;
            ctx.beginPath();
            ctx.moveTo(plot.px(b[0]), plot.py(i + 1));
            ctx.lineTo(plot.px(b[1]), plot.py(i + 1));
            ctx.stroke();
        });
        plot.vline(mu, F(), "true mean");
        /* The coverage comes out below nominal at small n, and that is not a
         * bug to hide: this uses a z critical value with an estimated standard
         * deviation, which is exactly the under-coverage the t-distribution
         * was invented to fix. Naming it is more use than quietly using t. */
        var rate = 100 * covered / total;
        var shortfall = conf * 100 - rate;
        return {
            readout: Math.round(conf * 100) + "% intervals, n = " + n + ".  Of 1000 drawn, " +
                     covered + " contained the true mean - " + rate.toFixed(1) + "%.  " +
                     (shortfall > 1.2
                        ? "Short of the nominal rate, because this uses a z value with an " +
                          "estimated SD; that is what the t-distribution corrects, and the " +
                          "gap shrinks as n grows."
                        : "Close to nominal.") +
                     "  The " + bars.filter(function (b) { return !b[2]; }).length +
                     " highlighted above missed, and nothing about them looks wrong from the inside."
        };
    };

    /* A null distribution, an observed statistic, and the tail area that is
     * the p-value - shaded rather than asserted. */
    DEMOS.pvalue = function (p, view) {
        var obs = p.observed, tail = p.tail;
        var plot = Plot(view.canvas(0), { xr: [-4, 4], yr: [0, 0.45], height: 280,
                                          pad: { l: 54, r: 12, t: 12, b: 32 } });
        plot.axes("test statistic under the null", "density");
        var curve = [], x;
        for (x = -4; x <= 4; x += 0.02) curve.push([x, gauss(x, 0, 1)]);

        var ctx = plot.ctx;
        var shade = function (from, to) {
            ctx.fillStyle = F();
            ctx.globalAlpha = 0.30;
            ctx.beginPath();
            ctx.moveTo(plot.px(from), plot.py(0));
            for (var t = from; t <= to; t += 0.02) ctx.lineTo(plot.px(t), plot.py(gauss(t, 0, 1)));
            ctx.lineTo(plot.px(to), plot.py(0));
            ctx.closePath();
            ctx.fill();
            ctx.globalAlpha = 1;
        };
        var pv;
        if (tail === "two") {
            var a = Math.abs(obs);
            shade(a, 4); shade(-4, -a);
            pv = 2 * (1 - phi(a));
        } else {
            shade(obs, 4);
            pv = 1 - phi(obs);
        }
        plot.line(curve, A(), 2.2);
        plot.vline(obs, A(), "observed " + obs.toFixed(2));

        var verdict = pv < 0.01 ? "strong evidence against the null"
                    : (pv < 0.05 ? "conventionally significant, and 0.05 is a convention"
                                 : "not significant at 0.05 - which is not evidence the null is true");
        return {
            readout: "p = " + pv.toFixed(4) + " (" + (tail === "two" ? "two-tailed" : "one-tailed") +
                     ").  That is the shaded area: the chance of a statistic this extreme " +
                     "IF the null were true.  " + verdict + "."
        };
    };

    /* Two hypotheses, the threshold between them, and the two error rates that
     * trade off across it. */
    DEMOS.power = function (p, view) {
        /* A <select> hands back a string, always. Everything numeric that can
         * arrive from one is parsed here rather than trusted - alpha.toFixed
         * threw on this page for exactly that reason. */
        var effect = p.effect, n = p.n | 0, alpha = parseFloat(p.alpha);
        var se = 1 / Math.sqrt(n);
        var crit = 0;
        // one-sided critical value on the null's scale
        var zAlpha = lookup([[0.01, 2.3263], [0.05, 1.6449], [0.10, 1.2816]], alpha, 1.6449);
        crit = zAlpha * se;
        var power = 1 - phi((crit - effect) / se);
        var beta = 1 - power;

        var lo = -4 * se, hi = effect + 4 * se;
        var top = Math.max(gauss(0, 0, se), gauss(effect, effect, se));
        var plot = Plot(view.canvas(0), { xr: [lo, hi], yr: [0, top * 1.1], height: 280,
                                          pad: { l: 54, r: 12, t: 12, b: 32 } });
        plot.axes("observed effect", "density");
        var ctx = plot.ctx;
        var shade = function (from, to, mu, colour, alphaVal) {
            ctx.fillStyle = colour;
            ctx.globalAlpha = alphaVal;
            ctx.beginPath();
            ctx.moveTo(plot.px(from), plot.py(0));
            for (var t = from; t <= to; t += (hi - lo) / 400)
                ctx.lineTo(plot.px(t), plot.py(gauss(t, mu, se)));
            ctx.lineTo(plot.px(to), plot.py(0));
            ctx.closePath(); ctx.fill(); ctx.globalAlpha = 1;
        };
        shade(crit, hi, 0, A(), 0.35);          // Type I
        shade(lo, crit, effect, M(), 0.45);     // Type II
        var c1 = [], c2 = [], x;
        for (x = lo; x <= hi; x += (hi - lo) / 400) {
            c1.push([x, gauss(x, 0, se)]);
            c2.push([x, gauss(x, effect, se)]);
        }
        plot.line(c1, M(), 2);
        plot.line(c2, F(), 2);
        plot.vline(crit, A(), "threshold");

        return {
            readout: "n = " + n + ", true effect " + effect.toFixed(2) +
                     ".  Type I rate (alpha) " + alpha.toFixed(2) +
                     ", Type II rate (beta) " + beta.toFixed(3) +
                     ", power " + (100 * power).toFixed(1) +
                     "%.  Lowering alpha moves the threshold right and raises beta - " +
                     "the only way to improve both at once is more data."
        };
    };

    /* Gram-Schmidt, performed: take the second vector, remove its component
     * along the first, and normalise what is left. */
    DEMOS.gramschmidt = function (p, view) {
        var a = [p.x1, p.y1], b = [p.x2, p.y2];
        var na = Math.hypot(a[0], a[1]) || 1;
        var q1 = [a[0] / na, a[1] / na];
        var proj = b[0] * q1[0] + b[1] * q1[1];
        var perp = [b[0] - proj * q1[0], b[1] - proj * q1[1]];
        var np = Math.hypot(perp[0], perp[1]);
        var q2 = np > 1e-9 ? [perp[0] / np, perp[1] / np] : [0, 0];

        var plot = Plot(view.canvas(0), { xr: [-3.5, 3.5], yr: [-2.6, 2.6], height: 300 });
        plot.axes("x", "y");
        plot.line([[0, 0], a], M(), 2, [5, 4]);
        plot.line([[0, 0], b], M(), 2, [5, 4]);
        // the projection of b onto q1, and the perpendicular remainder
        plot.line([[0, 0], [proj * q1[0], proj * q1[1]]], F(), 2.4);
        plot.line([[proj * q1[0], proj * q1[1]], b], A(), 2, [3, 3]);
        plot.line([[0, 0], q1], F(), 3);
        plot.line([[0, 0], q2], A(), 3);
        plot.dot(q1[0], q1[1], F(), 4.5);
        plot.dot(q2[0], q2[1], A(), 4.5);

        var dot = q1[0] * q2[0] + q1[1] * q2[1];
        return {
            readout: "b projected onto q1 has length " + proj.toFixed(2) +
                     "; what is left over has length " + np.toFixed(3) +
                     " and becomes q2.  q1 . q2 = " + dot.toFixed(6) +
                     " - orthogonal by construction, and R holds the projections " +
                     "that were subtracted."
        };
    };

    /* A 2x2 covariance matrix, its Cholesky factor, and samples generated by
     * multiplying that factor by independent noise. */
    DEMOS.cholesky = function (p, view) {
        var s1 = p.s1, s2 = p.s2, rho = p.rho;
        var c11 = s1 * s1, c22 = s2 * s2, c12 = rho * s1 * s2;
        // L L' = C, lower triangular
        var l11 = Math.sqrt(c11);
        var l21 = c12 / (l11 || 1);
        var inner = c22 - l21 * l21;
        var ok = inner > 1e-9 && c11 > 0;
        var l22 = ok ? Math.sqrt(inner) : 0;

        var r = rng(p.seed || 311), pts = [], i;
        for (i = 0; i < 420; i++) {
            var z1 = normal(r), z2 = normal(r);
            pts.push([l11 * z1, l21 * z1 + l22 * z2]);
        }
        var lim = Math.max(3.2, s1 * 3, s2 * 3);
        var plot = Plot(view.canvas(0), { xr: [-lim, lim], yr: [-lim * 0.75, lim * 0.75],
                                          height: 300 });
        plot.axes("x", "y");
        pts.forEach(function (q) { plot.dot(q[0], q[1], M(), 2.4); });
        plot.line([[0, 0], [l11, l21]], F(), 2.6);
        plot.line([[0, 0], [0, l22]], A(), 2.6);

        return ok ? {
            readout: "L = [[" + l11.toFixed(2) + ", 0], [" + l21.toFixed(2) + ", " +
                     l22.toFixed(2) + "]].  Multiply independent standard normals by L " +
                     "and they come out with exactly this covariance - that is what a " +
                     "Cholesky factor is for."
        } : {
            readout: "Not positive definite: with correlation " + rho.toFixed(2) +
                     " at these scales the matrix has no real Cholesky factor, because " +
                     "no distribution has that covariance. The factorisation failing " +
                     "IS the test."
        };
    };

    /* A constrained optimum: level sets of an objective, a circular
     * constraint, and the point where they are tangent. */
    DEMOS.lagrange = function (p, view) {
        var ax = p.ax, ay = p.ay, rad = p.r;
        // maximise ax*x + ay*y subject to x^2 + y^2 = r^2
        var na = Math.hypot(ax, ay) || 1;
        var sx = rad * ax / na, sy = rad * ay / na;
        var lam = na / (2 * rad);

        var plot = Plot(view.canvas(0), { xr: [-3.2, 3.2], yr: [-2.4, 2.4], height: 300 });
        plot.axes("x", "y");
        // level sets of the linear objective
        var k;
        for (k = -6; k <= 6; k++) {
            var c = k * 0.8;
            // ax*x + ay*y = c  ->  a line
            var pts = [];
            if (Math.abs(ay) > 1e-6) {
                pts = [[-3.2, (c - ax * -3.2) / ay], [3.2, (c - ax * 3.2) / ay]];
            } else {
                pts = [[c / ax, -2.4], [c / ax, 2.4]];
            }
            plot.line(pts, M(), 0.8);
        }
        var circle = [];
        for (k = 0; k <= 90; k++) {
            var t = k / 90 * 2 * Math.PI;
            circle.push([rad * Math.cos(t), rad * Math.sin(t)]);
        }
        plot.line(circle, A(), 2.4);
        plot.line([[0, 0], [ax / na * 1.2, ay / na * 1.2]], F(), 2);
        plot.dot(sx, sy, F(), 5.5);
        plot.ring(sx, sy, F(), 9);

        return {
            readout: "optimum at (" + sx.toFixed(2) + ", " + sy.toFixed(2) +
                     "), objective value " + (ax * sx + ay * sy).toFixed(2) +
                     ", lambda = " + lam.toFixed(2) +
                     ".  It is where a level line just touches the circle - " +
                     "the two gradients are parallel, which is the whole condition."
        };
    };

    /* Jensen: a convex function, a chord, and the gap between the mean of the
     * outputs and the output of the mean. */
    DEMOS.jensen = function (p, view) {
        var spread = p.spread, curve = p.curve, mu = 1.6;
        var f = function (x) { return curve >= 0 ? Math.exp(curve * x) : Math.log(Math.max(0.05, x)) * -curve * 4; };
        var lo = Math.max(0.1, mu - spread), hi = mu + spread;
        var pts = [], x;
        for (x = 0.1; x <= 4; x += 0.02) pts.push([x, f(x)]);
        var top = Math.max.apply(null, pts.map(function (q) { return q[1]; }));
        var plot = Plot(view.canvas(0), { xr: [0, 4], yr: [Math.min(0, Math.min.apply(null, pts.map(function (q) { return q[1]; }))) - 0.4, top * 1.05],
                                          height: 290, pad: { l: 54, r: 12, t: 12, b: 32 } });
        plot.axes("x", "f(x)");
        plot.line(pts, A(), 2.2);
        // A two-point distribution at lo and hi, each with probability 1/2.
        var efx = (f(lo) + f(hi)) / 2, fex = f(mu);
        plot.line([[lo, f(lo)], [hi, f(hi)]], F(), 2, [5, 4]);
        plot.dot(lo, f(lo), M(), 4.5);
        plot.dot(hi, f(hi), M(), 4.5);
        plot.dot(mu, fex, A(), 5.5);
        plot.dot(mu, efx, F(), 5.5);

        var gap = efx - fex;
        return {
            readout: "E[f(X)] = " + efx.toFixed(3) + ", f(E[X]) = " + fex.toFixed(3) +
                     ", gap " + gap.toFixed(3) + ".  " +
                     (curve >= 0
                        ? "Convex, so the chord sits above the curve and E[f(X)] >= f(E[X])."
                        : "Concave, so the inequality reverses.") +
                     "  Shrink the spread and the gap closes; it is zero only for a constant."
        };
    };

    /* A Markov chain, iterated. The distribution converges to the stationary
     * one regardless of where it starts. */
    DEMOS.markov = function (p, view) {
        // three states; row i is where you go from state i
        var P = [
            [1 - p.a, p.a * 0.6, p.a * 0.4],
            [p.b * 0.5, 1 - p.b, p.b * 0.5],
            [p.c * 0.3, p.c * 0.7, 1 - p.c]
        ];
        var dist = [p.start === "0" ? 1 : 0, p.start === "1" ? 1 : 0, p.start === "2" ? 1 : 0];
        var history = [dist.slice()], i, j, k;
        for (i = 0; i < 40; i++) {
            var next = [0, 0, 0];
            for (j = 0; j < 3; j++)
                for (k = 0; k < 3; k++) next[k] += dist[j] * P[j][k];
            dist = next;
            history.push(dist.slice());
        }
        var plot = Plot(view.canvas(0), { xr: [0, 40], yr: [0, 1], height: 280,
                                          pad: { l: 52, r: 12, t: 12, b: 34 } });
        plot.axes("step", "probability");
        var cols = [A(), F(), M()];
        for (k = 0; k < 3; k++)
            plot.line(history.map(function (h, i) { return [i, h[k]]; }), cols[k], 2.2);

        var last = history[history.length - 1];
        var prev = history[history.length - 2];
        var moved = Math.max.apply(null, last.map(function (v, i) { return Math.abs(v - prev[i]); }));
        return {
            readout: "after 40 steps: " + last.map(function (v) { return v.toFixed(3); }).join(", ") +
                     ".  The last step moved it by " + moved.toExponential(1) +
                     " - this is the stationary distribution, and every starting state " +
                     "reaches the same one."
        };
    };

    /* Counting: permutations against combinations, and the factor between. */
    DEMOS.counting = function (p, view) {
        var n = p.n | 0, k = p.k | 0;
        if (k > n) k = n;
        var logFact = function (m) { var s = 0, i; for (i = 2; i <= m; i++) s += Math.log(i); return s; };
        var perm = Math.exp(logFact(n) - logFact(n - k));
        var comb = Math.exp(logFact(n) - logFact(k) - logFact(n - k));
        var withRep = Math.pow(n, k);

        var rows = [];
        for (var kk = 0; kk <= n; kk++)
            rows.push([kk, Math.exp(logFact(n) - logFact(kk) - logFact(n - kk))]);
        var top = Math.max.apply(null, rows.map(function (r) { return r[1]; }));
        var plot = Plot(view.canvas(0), { xr: [-0.6, n + 0.6], yr: [0, top * 1.12],
                                          height: 270, pad: { l: 64, r: 12, t: 12, b: 34 } });
        plot.axes("k", "C(n, k)");
        rows.forEach(function (r) {
            plot.bar(r[0] - 0.36, r[0] + 0.36, r[1], r[0] === k ? A() : F());
        });

        var fmt = function (v) {
            return v >= 1e6 ? v.toExponential(2) : Math.round(v).toLocaleString();
        };
        return {
            readout: "n = " + n + ", k = " + k + ".  Ordered without repetition: " + fmt(perm) +
                     ".  Unordered: " + fmt(comb) + " - smaller by exactly k! = " +
                     fmt(Math.exp(logFact(k))) + ", the number of orders each selection " +
                     "could have arrived in.  With repetition allowed: " + fmt(withRep) + "."
        };
    };
})();

/* Mount, and it has to be last in this file.
 *
 * These scripts are deferred, so by the time any of this runs the document is
 * already "interactive" - which means init() fires immediately rather than
 * waiting for DOMContentLoaded. When this block sat in the middle of the file
 * it therefore mounted every page BEFORE the tier 2 demonstrations below it
 * had registered themselves, and nine of the ten came up blank while the one
 * that reused a tier 1 demo worked fine.
 *
 * Keeping the mount at the end means every demo is registered before anything
 * looks for one.
 */
(function () {
    "use strict";
    var DEMOS = window.VizMathDemos;

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
        var cfgEl = root.querySelector(".math-config");
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
        root.dataset.vzMathReady = "1";
    }

    function init() {
        Array.prototype.forEach.call(
            document.querySelectorAll("[data-vz-math]"), mount);
    }
    if (document.readyState === "loading")
        document.addEventListener("DOMContentLoaded", init);
    else init();
})();
