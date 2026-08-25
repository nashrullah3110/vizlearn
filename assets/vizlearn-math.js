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

/* Mount: controls, canvases, readout, and the draggable vectors on the basis
 * module. Deliberately the same shape as the machine learning harness, so a
 * reader moving between the two tracks meets one set of habits. */
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
