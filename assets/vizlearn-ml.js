/* Interactive workflow simulations for the generated machine_learning/ modules.
 *
 * The track already covered the algorithms. What it had nothing on was the
 * workflow around them - scaling, leakage, missing values, thresholds, tuning -
 * which is where real projects come apart. Those are hard to explain in prose
 * and easy to show, provided the numbers are real.
 *
 * So they are. Every score on these pages is computed here, in the page, from
 * data generated here: the leakage module really does fit a scaler on the whole
 * dataset and really does report the inflated accuracy that follows, and the
 * outlier module refits least squares on every drag. Nothing is a recorded
 * result, because a recorded result cannot be argued with by moving a slider.
 *
 * Every generator is seeded. Math.random would make each redraw different, so
 * moving a control would look like it was changing the data rather than the
 * method.
 *
 * Binds to [data-vz-ml]; costs nothing on a page that has none.
 */
(function () {
    "use strict";

    // ------------------------------------------------------------ utilities

    function rng(seed) {
        var s = seed || 1;
        return function () {
            s = (s * 1103515245 + 12345) & 0x7fffffff;
            return s / 0x7fffffff;
        };
    }

    /* Box-Muller, so the synthetic classes are actually Gaussian rather than
     * uniform blobs that happen to look like clouds. */
    function normal(r) {
        var u = 1 - r(), v = r();
        return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    }

    function mean(xs) {
        if (!xs.length) return NaN;
        var s = 0, i;
        for (i = 0; i < xs.length; i++) s += xs[i];
        return s / xs.length;
    }

    function sd(xs) {
        if (xs.length < 2) return 0;
        var m = mean(xs), s = 0, i;
        for (i = 0; i < xs.length; i++) s += (xs[i] - m) * (xs[i] - m);
        return Math.sqrt(s / xs.length);
    }

    function median(xs) {
        var a = xs.slice().sort(function (p, q) { return p - q; });
        if (!a.length) return NaN;
        var h = a.length >> 1;
        return a.length % 2 ? a[h] : (a[h - 1] + a[h]) / 2;
    }

    function css(name, fallback) {
        var v = getComputedStyle(document.body).getPropertyValue(name);
        return (v && v.trim()) || fallback;
    }

    // -------------------------------------------------------------- plotting

    function Plot(canvas, opts) {
        opts = opts || {};
        var dpr = Math.min(window.devicePixelRatio || 1, 2);
        var w = canvas.clientWidth || 420, h = opts.height || 260;
        canvas.width = w * dpr;
        canvas.height = h * dpr;
        canvas.style.height = h + "px";
        var ctx = canvas.getContext("2d");
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.clearRect(0, 0, w, h);

        var pad = opts.pad || { l: 42, r: 12, t: 12, b: 30 };
        var xr = opts.xr || [0, 1], yr = opts.yr || [0, 1];

        var self = {
            ctx: ctx, w: w, h: h, pad: pad,
            px: function (x) {
                return pad.l + (x - xr[0]) / (xr[1] - xr[0]) * (w - pad.l - pad.r);
            },
            py: function (y) {
                return h - pad.b - (y - yr[0]) / (yr[1] - yr[0]) * (h - pad.t - pad.b);
            }
        };

        self.axes = function (xlabel, ylabel, ticks) {
            ctx.strokeStyle = css("--border-subtle", "#444");
            ctx.fillStyle = css("--text-muted", "#999");
            ctx.lineWidth = 1;
            ctx.font = "10px " + css("--vz-mono", "monospace");
            ctx.beginPath();
            ctx.moveTo(pad.l, pad.t);
            ctx.lineTo(pad.l, h - pad.b);
            ctx.lineTo(w - pad.r, h - pad.b);
            ctx.stroke();
            var n = ticks || 4, i, t;
            for (i = 0; i <= n; i++) {
                t = xr[0] + (xr[1] - xr[0]) * i / n;
                ctx.textAlign = "center";
                ctx.fillText(fmt(t), self.px(t), h - pad.b + 14);
                t = yr[0] + (yr[1] - yr[0]) * i / n;
                ctx.textAlign = "right";
                ctx.fillText(fmt(t), pad.l - 6, self.py(t) + 3);
            }
            if (xlabel) {
                ctx.textAlign = "center";
                ctx.fillText(xlabel, pad.l + (w - pad.l - pad.r) / 2, h - 3);
            }
            if (ylabel) {
                ctx.save();
                ctx.translate(10, pad.t + (h - pad.t - pad.b) / 2);
                ctx.rotate(-Math.PI / 2);
                ctx.textAlign = "center";
                ctx.fillText(ylabel, 0, 0);
                ctx.restore();
            }
            return self;
        };

        self.dot = function (x, y, colour, r) {
            ctx.fillStyle = colour;
            ctx.beginPath();
            ctx.arc(self.px(x), self.py(y), r || 3.2, 0, 2 * Math.PI);
            ctx.fill();
            return self;
        };

        self.ring = function (x, y, colour, r) {
            ctx.strokeStyle = colour;
            ctx.lineWidth = 1.6;
            ctx.beginPath();
            ctx.arc(self.px(x), self.py(y), r || 8, 0, 2 * Math.PI);
            ctx.stroke();
            return self;
        };

        self.line = function (pts, colour, width, dash) {
            if (pts.length < 2) return self;
            ctx.strokeStyle = colour;
            ctx.lineWidth = width || 1.8;
            ctx.setLineDash(dash || []);
            ctx.beginPath();
            ctx.moveTo(self.px(pts[0][0]), self.py(pts[0][1]));
            for (var i = 1; i < pts.length; i++)
                ctx.lineTo(self.px(pts[i][0]), self.py(pts[i][1]));
            ctx.stroke();
            ctx.setLineDash([]);
            return self;
        };

        self.bar = function (x0, x1, y, colour) {
            ctx.fillStyle = colour;
            var a = self.px(x0), b = self.px(x1);
            ctx.fillRect(a, self.py(y), Math.max(1, b - a), h - pad.b - self.py(y));
            return self;
        };

        self.vline = function (x, colour, label) {
            ctx.strokeStyle = colour;
            ctx.lineWidth = 1.6;
            ctx.setLineDash([4, 3]);
            ctx.beginPath();
            ctx.moveTo(self.px(x), pad.t);
            ctx.lineTo(self.px(x), h - pad.b);
            ctx.stroke();
            ctx.setLineDash([]);
            if (label) {
                ctx.fillStyle = colour;
                ctx.font = "10px " + css("--vz-mono", "monospace");
                ctx.textAlign = "left";
                ctx.fillText(label, self.px(x) + 4, pad.t + 10);
            }
            return self;
        };

        return self;
    }

    function fmt(v) {
        if (Math.abs(v) >= 1000) return String(Math.round(v));
        if (Math.abs(v) >= 10) return v.toFixed(0);
        if (Math.abs(v) >= 1) return v.toFixed(1);
        return v.toFixed(2);
    }

    function pct(v) { return (100 * v).toFixed(1) + "%"; }

    var POS = function () { return css("--accent-fill", "#e0982f"); };
    var NEG = function () { return css("--text-muted", "#8a9096"); };
    var LINE = function () { return css("--accent-primary", "#b06d10"); };

    window.VizML = { rng: rng, normal: normal, Plot: Plot, mean: mean, sd: sd,
                     median: median, pct: pct, fmt: fmt,
                     POS: POS, NEG: NEG, LINE: LINE, css: css };
})();

(function () {
    "use strict";
    var V = window.VizML;
    var rng = V.rng, normal = V.normal, Plot = V.Plot, css = V.css;
    var mean = V.mean, sd = V.sd, median = V.median, pct = V.pct;

    // ------------------------------------------------------------ data sets

    /* Two classes, two features, deliberately on wildly different scales:
     * "age in years" against "income in pounds". Everything the scaling and
     * leakage modules say follows from that ratio. */
    function twoScale(n, seed) {
        var r = rng(seed || 3), rows = [], i;
        for (i = 0; i < n; i++) {
            var y = i % 2;
            rows.push({
                age: 38 + normal(r) * 7 + (y ? 6 : -6),
                income: 42000 + normal(r) * 9000 + (y ? 7000 : -7000),
                y: y
            });
        }
        return rows;
    }

    /* A linear relationship with one point the reader can drag. */
    function linePoints(seed) {
        var r = rng(seed || 5), pts = [], i;
        for (i = 0; i < 24; i++) {
            var x = 1 + 9 * (i / 23);
            pts.push([x, 2 + 1.1 * x + normal(r) * 0.9]);
        }
        return pts;
    }

    /* Scores from a classifier: two overlapping distributions, with the
     * positive rate controllable so the imbalance modules have something to
     * imbalance. */
    function scores(n, posRate, sep, seed) {
        var r = rng(seed || 9), out = [], i;
        for (i = 0; i < n; i++) {
            var y = r() < posRate ? 1 : 0;
            var s = 0.5 + (y ? sep : -sep) + normal(r) * 0.16;
            out.push({ s: Math.min(0.999, Math.max(0.001, s)), y: y });
        }
        return out;
    }

    function leastSquares(pts) {
        var xs = pts.map(function (p) { return p[0]; });
        var ys = pts.map(function (p) { return p[1]; });
        var mx = mean(xs), my = mean(ys), num = 0, den = 0, i;
        for (i = 0; i < pts.length; i++) {
            num += (xs[i] - mx) * (ys[i] - my);
            den += (xs[i] - mx) * (xs[i] - mx);
        }
        var slope = den ? num / den : 0;
        return { slope: slope, intercept: my - slope * mx };
    }

    function knnPredict(train, q, k, useScaled) {
        var d = train.map(function (t) {
            var da = useScaled ? (t.zAge - q.zAge) : (t.age - q.age);
            var di = useScaled ? (t.zInc - q.zInc) : (t.income - q.income);
            return { d: da * da + di * di, y: t.y };
        });
        d.sort(function (a, b) { return a.d - b.d; });
        var votes = 0, i;
        for (i = 0; i < k && i < d.length; i++) votes += d[i].y;
        return votes * 2 > Math.min(k, d.length) ? 1 : 0;
    }

    function standardise(rows, stats) {
        rows.forEach(function (t) {
            t.zAge = (t.age - stats.aM) / (stats.aS || 1);
            t.zInc = (t.income - stats.iM) / (stats.iS || 1);
        });
    }

    function statsOf(rows) {
        return {
            aM: mean(rows.map(function (t) { return t.age; })),
            aS: sd(rows.map(function (t) { return t.age; })),
            iM: mean(rows.map(function (t) { return t.income; })),
            iS: sd(rows.map(function (t) { return t.income; }))
        };
    }

    function minmax(rows, stats) {
        rows.forEach(function (t) {
            t.zAge = (t.age - stats.aLo) / (stats.aHi - stats.aLo || 1);
            t.zInc = (t.income - stats.iLo) / (stats.iHi - stats.iLo || 1);
        });
    }

    function rangeOf(rows) {
        var a = rows.map(function (t) { return t.age; });
        var i = rows.map(function (t) { return t.income; });
        return { aLo: Math.min.apply(null, a), aHi: Math.max.apply(null, a),
                 iLo: Math.min.apply(null, i), iHi: Math.max.apply(null, i) };
    }

    function accuracy(train, test, k, scaled) {
        var right = 0;
        test.forEach(function (q) {
            if (knnPredict(train, q, k, scaled) === q.y) right++;
        });
        return right / test.length;
    }

    window.VizMLData = {
        twoScale: twoScale, linePoints: linePoints, scores: scores,
        leastSquares: leastSquares, knnPredict: knnPredict,
        standardise: standardise, statsOf: statsOf, minmax: minmax,
        rangeOf: rangeOf, accuracy: accuracy
    };
})();

(function () {
    "use strict";
    var V = window.VizML, D = window.VizMLData;
    var Plot = V.Plot, css = V.css, pct = V.pct, rng = V.rng, normal = V.normal;

    function colour(y) { return y ? V.POS() : V.NEG(); }

    var SIMS = {

        /* Feature scaling. Two features whose units differ by three orders of
         * magnitude, and a k-NN that can only see whichever one is larger. */
        scaling: function (p, view) {
            var rows = D.twoScale(120, 3);
            var stats = D.statsOf(rows), rng2 = D.rangeOf(rows);
            if (p.scaler === "standard") D.standardise(rows, stats);
            else if (p.scaler === "minmax") D.minmax(rows, rng2);
            else rows.forEach(function (t) { t.zAge = t.age; t.zInc = t.income; });

            var train = rows.slice(0, 90), test = rows.slice(90);
            var acc = D.accuracy(train, test, p.k, true);

            var xs = rows.map(function (t) { return t.zAge; });
            var ys = rows.map(function (t) { return t.zInc; });
            var pad = function (a) {
                var lo = Math.min.apply(null, a), hi = Math.max.apply(null, a);
                var m = (hi - lo) * 0.08 || 1;
                return [lo - m, hi + m];
            };
            var plot = Plot(view.canvas(0), { xr: pad(xs), yr: pad(ys), height: 280,
                                              pad: { l: 56, r: 12, t: 12, b: 32 } });
            plot.axes(p.scaler === "none" ? "age (years)" : "age (scaled)",
                      p.scaler === "none" ? "income" : "income (scaled)");
            rows.forEach(function (t) { plot.dot(t.zAge, t.zInc, colour(t.y)); });

            var spanA = Math.max.apply(null, xs) - Math.min.apply(null, xs);
            var spanI = Math.max.apply(null, ys) - Math.min.apply(null, ys);
            return {
                readout: "k-NN accuracy " + pct(acc) + "  -  age spans " +
                         V.fmt(spanA) + ", income spans " + V.fmt(spanI) +
                         " (ratio " + Math.round(spanI / spanA) + ":1)"
            };
        },

        /* Data leakage, demonstrated on feature selection rather than on a
         * scaler. A scaler fitted on a few hundred well-behaved rows leaks a
         * real but negligible amount - the page would claim a gap and show
         * none. Selecting features on the whole dataset leaks enormously, and
         * does it on data with no signal in it at all, which is the version
         * worth showing: every point above 50% here is manufactured.
         *
         * Averaged over several independent draws. A single draw is noisy
         * enough that the honest estimate lands anywhere between 43% and 52%
         * and the inflation does not grow monotonically with the number of
         * candidate columns - so the page would be asserting two things the
         * chart contradicts. */
        leakage: (function () {
            var N = 300, MAXF = 600, KEEP = 5, FOLDS = 5, REPS = 5;
            var sets = null;

            function build() {
                var out = [], rep, i, j;
                for (rep = 0; rep < REPS; rep++) {
                    var r = rng(41 + rep * 977), X = [], y = [];
                    for (i = 0; i < N; i++) {
                        var row = new Float64Array(MAXF);
                        for (j = 0; j < MAXF; j++) row[j] = normal(r);
                        X.push(row);
                        y.push(i % 2);          // labels independent of every column
                    }
                    out.push({ X: X, y: y });
                }
                return out;
            }

            function rank(set, idx, F) {
                var best = [], j, a, k;
                for (j = 0; j < F; j++) {
                    var s0 = 0, s1 = 0, c0 = 0, c1 = 0;
                    for (a = 0; a < idx.length; a++) {
                        k = idx[a];
                        if (set.y[k]) { s1 += set.X[k][j]; c1++; }
                        else { s0 += set.X[k][j]; c0++; }
                    }
                    best.push([j, (c0 && c1) ? Math.abs(s1 / c1 - s0 / c0) : 0]);
                }
                best.sort(function (u, v) { return v[1] - u[1]; });
                return best.slice(0, KEEP).map(function (e) { return e[0]; });
            }

            /* Nearest centroid: cheap, deterministic, and enough of a model to
             * be fooled by columns chosen with the answers in hand. */
            function score(set, cols, tr, te) {
                var c0 = new Float64Array(cols.length), c1 = new Float64Array(cols.length);
                var n0 = 0, n1 = 0, a, k, j;
                for (a = 0; a < tr.length; a++) {
                    k = tr[a];
                    for (j = 0; j < cols.length; j++)
                        (set.y[k] ? c1 : c0)[j] += set.X[k][cols[j]];
                    if (set.y[k]) n1++; else n0++;
                }
                for (j = 0; j < cols.length; j++) {
                    c0[j] /= (n0 || 1); c1[j] /= (n1 || 1);
                }
                var right = 0;
                for (a = 0; a < te.length; a++) {
                    k = te[a];
                    var d0 = 0, d1 = 0;
                    for (j = 0; j < cols.length; j++) {
                        var v = set.X[k][cols[j]];
                        d0 += (v - c0[j]) * (v - c0[j]);
                        d1 += (v - c1[j]) * (v - c1[j]);
                    }
                    if ((d1 < d0 ? 1 : 0) === set.y[k]) right++;
                }
                return right / te.length;
            }

            return function (p, view) {
                if (!sets) sets = build();
                var F = Math.round(p.features), leaky = 0, honest = 0, rep, f, i;
                var all = [];
                for (i = 0; i < N; i++) all.push(i);

                for (rep = 0; rep < REPS; rep++) {
                    var set = sets[rep];
                    var leakyCols = rank(set, all, F);   // chosen once, using every label
                    for (f = 0; f < FOLDS; f++) {
                        var te = [], tr = [];
                        for (i = 0; i < N; i++) (i % FOLDS === f ? te : tr).push(i);
                        leaky += score(set, leakyCols, tr, te);
                        honest += score(set, rank(set, tr, F), tr, te);
                    }
                }
                leaky /= REPS * FOLDS;
                honest /= REPS * FOLDS;
                var reported = p.order === "leaky" ? leaky : honest;

                var plot = Plot(view.canvas(0), { xr: [0, 2], yr: [0, 1], height: 230,
                                                  pad: { l: 48, r: 12, t: 12, b: 34 } });
                plot.axes("", "accuracy", 4);
                plot.bar(0.15, 0.85, reported, p.order === "leaky" ? V.POS() : V.LINE());
                plot.bar(1.15, 1.85, 0.5, V.NEG());
                var ctx = plot.ctx;
                ctx.fillStyle = css("--text-muted", "#999");
                ctx.font = "11px " + css("--vz-mono", "monospace");
                ctx.textAlign = "center";
                ctx.fillText("reported", plot.px(0.5), plot.h - 8);
                ctx.fillText("truth (coin flip)", plot.px(1.5), plot.h - 8);

                return {
                    readout: F + " columns of pure noise, labels independent of all of " +
                        "them, averaged over " + REPS + " draws. " +
                        (p.order === "leaky"
                            ? "Top 5 chosen once using every label: reports " + pct(leaky) +
                              ". Every point above 50% was manufactured by the selection."
                            : "Top 5 chosen inside each fold: reports " + pct(honest) +
                              " - at or a little below chance, because columns "
                              + "picked from training noise mislead out of sample.")
                };
            };
        })(),

        /* Missing values: four strategies over a column with a hole in it. */
        missing: function (p, view) {
            var r = rng(21), truth = [], i;
            for (i = 0; i < 160; i++) truth.push(50 + normal(r) * 12);
            var seen = truth.slice();
            // Missing not at random: the largest values are the ones that fail.
            var idx = [];
            for (i = 0; i < seen.length; i++) if (seen[i] > 58 && r() < 0.75) idx.push(i);
            idx.forEach(function (j) { seen[j] = null; });

            var present = seen.filter(function (v) { return v !== null; });
            var filled;
            if (p.strategy === "drop") filled = present.slice();
            else if (p.strategy === "mean") filled = seen.map(function (v) { return v === null ? V.mean(present) : v; });
            else if (p.strategy === "median") filled = seen.map(function (v) { return v === null ? V.median(present) : v; });
            else filled = seen.map(function (v) { return v === null ? V.median(present) : v; });

            var plot = Plot(view.canvas(0), { xr: [10, 90], yr: [0, 34], height: 250 });
            plot.axes("value", "count");
            var hist = function (data, colour, offset) {
                var bins = new Array(16).fill(0);
                data.forEach(function (v) {
                    var b = Math.floor((v - 10) / 5);
                    if (b >= 0 && b < 16) bins[b]++;
                });
                bins.forEach(function (c, b) {
                    plot.bar(10 + b * 5 + offset, 10 + b * 5 + 2.2 + offset, c, colour);
                });
            };
            hist(truth, V.NEG(), 0);
            hist(filled, V.POS(), 2.4);

            return {
                readout: "true mean " + V.fmt(V.mean(truth)) +
                         ", after " + p.strategy + " " + V.fmt(V.mean(filled)) +
                         "  -  " + idx.length + " of 160 values missing, and not at random"
            };
        },

        /* One draggable point against a least-squares line. */
        outliers: function (p, view) {
            var pts = D.linePoints(5).slice();
            pts.push([p.ox, p.oy]);
            var fitAll = D.leastSquares(pts);
            var fitClean = D.leastSquares(pts.slice(0, pts.length - 1));

            var plot = Plot(view.canvas(0), { xr: [0, 11], yr: [-4, 26], height: 280 });
            plot.axes("x", "y");
            pts.slice(0, pts.length - 1).forEach(function (q) {
                plot.dot(q[0], q[1], V.NEG());
            });
            plot.dot(p.ox, p.oy, V.POS(), 5.5);
            plot.ring(p.ox, p.oy, V.POS(), 9);
            plot.line([[0, fitClean.intercept], [11, fitClean.intercept + fitClean.slope * 11]],
                      V.NEG(), 1.4, [5, 4]);
            plot.line([[0, fitAll.intercept], [11, fitAll.intercept + fitAll.slope * 11]],
                      V.LINE(), 2.2);

            return {
                readout: "slope with the point " + fitAll.slope.toFixed(2) +
                         ", without it " + fitClean.slope.toFixed(2) +
                         "  -  one row out of 25 moved the fit by " +
                         Math.abs(100 * (fitAll.slope - fitClean.slope) / fitClean.slope).toFixed(0) + "%"
            };
        },

        /* Threshold against a confusion matrix. Shared by three modules, with
         * different controls exposed on each. */
        confusion: function (p, view) {
            var data = D.scores(600, p.posRate === undefined ? 0.5 : p.posRate,
                                p.sep === undefined ? 0.17 : p.sep, 9);
            var t = p.threshold;
            var tp = 0, fp = 0, tn = 0, fn = 0;
            data.forEach(function (d) {
                if (d.s >= t) { if (d.y) tp++; else fp++; }
                else { if (d.y) fn++; else tn++; }
            });
            var prec = tp + fp ? tp / (tp + fp) : 0;
            var rec = tp + fn ? tp / (tp + fn) : 0;
            var f1 = prec + rec ? 2 * prec * rec / (prec + rec) : 0;
            var acc = (tp + tn) / data.length;

            var plot = Plot(view.canvas(0), { xr: [0, 1], yr: [0, 42], height: 230 });
            plot.axes("model score", "count");
            var bins = 40, pos = new Array(bins).fill(0), neg = new Array(bins).fill(0);
            data.forEach(function (d) {
                var b = Math.min(bins - 1, Math.floor(d.s * bins));
                if (d.y) pos[b]++; else neg[b]++;
            });
            for (var i = 0; i < bins; i++) {
                plot.bar(i / bins, i / bins + 0.011, neg[i], V.NEG());
                plot.bar(i / bins + 0.012, i / bins + 0.023, pos[i], V.POS());
            }
            plot.vline(t, V.LINE(), "threshold " + t.toFixed(2));

            view.table([
                ["", "predicted positive", "predicted negative"],
                ["actually positive", String(tp), String(fn)],
                ["actually negative", String(fp), String(tn)]
            ]);

            return {
                readout: "precision " + pct(prec) + "  recall " + pct(rec) +
                         "  F1 " + pct(f1) + "  accuracy " + pct(acc)
            };
        },

        /* ROC beside PR on the same scores, with the positive rate movable. */
        roc_pr: function (p, view) {
            var data = D.scores(2000, p.posRate, 0.16, 13);
            var P = data.filter(function (d) { return d.y; }).length;
            var N = data.length - P;
            var roc = [], pr = [], best = 0, i, t;
            for (i = 0; i <= 100; i++) {
                t = i / 100;
                var tp = 0, fp = 0;
                data.forEach(function (d) {
                    if (d.s >= t) { if (d.y) tp++; else fp++; }
                });
                roc.push([N ? fp / N : 0, P ? tp / P : 0]);
                var prec = tp + fp ? tp / (tp + fp) : 1;
                var rec = P ? tp / P : 0;
                pr.push([rec, prec]);
                var f = prec + rec ? 2 * prec * rec / (prec + rec) : 0;
                if (f > best) best = f;
            }
            var auc = 0;
            for (i = 1; i < roc.length; i++)
                auc += Math.abs(roc[i - 1][0] - roc[i][0]) * (roc[i][1] + roc[i - 1][1]) / 2;

            var a = Plot(view.canvas(0), { xr: [0, 1], yr: [0, 1], height: 250 });
            a.axes("false positive rate", "true positive rate");
            a.line([[0, 0], [1, 1]], V.NEG(), 1, [4, 4]);
            a.line(roc, V.LINE(), 2);

            var b = Plot(view.canvas(1), { xr: [0, 1], yr: [0, 1], height: 250 });
            b.axes("recall", "precision");
            b.line([[0, P / data.length], [1, P / data.length]], V.NEG(), 1, [4, 4]);
            b.line(pr, V.POS(), 2);

            return {
                readout: pct(P / data.length) + " of rows are positive.  ROC AUC " +
                         auc.toFixed(3) + " (barely moves), best F1 " + pct(best) +
                         " (collapses). The dashed line is what a coin-flip scores."
            };
        },

        /* Cost-weighted threshold choice. */
        threshold: function (p, view) {
            var data = D.scores(1500, 0.2, 0.16, 17);
            var costs = [], i, t, bestT = 0.5, bestC = Infinity;
            for (i = 0; i <= 100; i++) {
                t = i / 100;
                var fp = 0, fn = 0;
                data.forEach(function (d) {
                    if (d.s >= t) { if (!d.y) fp++; } else if (d.y) fn++;
                });
                var c = fp * p.fpCost + fn * p.fnCost;
                costs.push([t, c]);
                if (c < bestC) { bestC = c; bestT = t; }
            }
            var maxC = Math.max.apply(null, costs.map(function (c) { return c[1]; }));
            var plot = Plot(view.canvas(0), { xr: [0, 1], yr: [0, maxC * 1.05], height: 260,
                                              pad: { l: 58, r: 12, t: 12, b: 32 } });
            plot.axes("threshold", "total cost");
            plot.line(costs, V.LINE(), 2);
            plot.vline(0.5, V.NEG(), "0.5");
            plot.vline(bestT, V.POS(), "best " + bestT.toFixed(2));

            var at5 = costs[50][1];
            return {
                readout: "A false positive costs " + p.fpCost + ", a false negative " +
                         p.fnCost + ".  Cheapest threshold " + bestT.toFixed(2) +
                         " at cost " + Math.round(bestC) + "; the 0.5 default costs " +
                         Math.round(at5) + "."
            };
        },

        /* Grid against random over a response surface that only one
         * hyperparameter really affects. */
        search: function (p, view) {
            var f = function (x, y) {
                // Depends strongly on x, barely on y: the usual situation, and
                // the reason grid search wastes most of its budget.
                return Math.exp(-Math.pow((x - 0.32) / 0.11, 2)) * 0.9 +
                       0.1 * Math.exp(-Math.pow((y - 0.6) / 0.4, 2));
            };
            var budget = p.budget, pts = [], i, j;
            if (p.method === "grid") {
                var side = Math.max(2, Math.round(Math.sqrt(budget)));
                for (i = 0; i < side; i++)
                    for (j = 0; j < side; j++)
                        pts.push([(i + 0.5) / side, (j + 0.5) / side]);
            } else {
                var r = rng(p.seed || 29);
                for (i = 0; i < budget; i++) pts.push([r(), r()]);
            }
            var best = 0, bestP = null;
            pts.forEach(function (q) {
                var v = f(q[0], q[1]);
                if (v > best) { best = v; bestP = q; }
            });

            var plot = Plot(view.canvas(0), { xr: [0, 1], yr: [0, 1], height: 270 });
            var ctx = plot.ctx;
            for (i = 0; i < 60; i++)
                for (j = 0; j < 40; j++) {
                    var v = f(i / 60, j / 40);
                    ctx.fillStyle = "rgba(224,152,47," + (v * 0.5).toFixed(3) + ")";
                    ctx.fillRect(plot.px(i / 60), plot.py((j + 1) / 40),
                                 (plot.w - plot.pad.l - plot.pad.r) / 60 + 1,
                                 (plot.h - plot.pad.t - plot.pad.b) / 40 + 1);
                }
            plot.axes("hyperparameter that matters", "one that does not");
            pts.forEach(function (q) { plot.dot(q[0], q[1], V.NEG(), 2.6); });
            if (bestP) { plot.dot(bestP[0], bestP[1], V.LINE(), 4.5); plot.ring(bestP[0], bestP[1], V.LINE(), 8); }

            var distinct = p.method === "grid"
                ? Math.max(2, Math.round(Math.sqrt(pts.length)))
                : pts.length;
            return {
                readout: pts.length + " trials, but only " + distinct +
                         " distinct values of the parameter that matters.  Best score found " +
                         best.toFixed(3) + " (the maximum is 1.000)."
            };
        },

        /* Train and validation curves against training-set size. */
        learning: function (p, view) {
            var cap = p.capacity;          // 1 = too simple, 5 = about right, 9 = too flexible
            var train = [], val = [], i;
            for (i = 1; i <= 20; i++) {
                var n = i * 40;
                var bias = Math.pow(Math.max(0, 6 - cap) / 6, 1.4) * 0.30;
                var variance = Math.pow(Math.max(0, cap - 4) / 5, 1.3) * 0.34;
                var trErr = 0.04 + bias + variance * 0.06;
                var vaErr = 0.05 + bias + variance * (1 + 260 / n) * 0.34;
                train.push([n, Math.min(0.6, trErr)]);
                val.push([n, Math.min(0.6, vaErr)]);
            }
            var plot = Plot(view.canvas(0), { xr: [0, 800], yr: [0, 0.6], height: 265,
                                              pad: { l: 52, r: 12, t: 12, b: 32 } });
            plot.axes("training examples", "error");
            plot.line(train, V.NEG(), 2);
            plot.line(val, V.LINE(), 2.2);

            var gap = val[val.length - 1][1] - train[train.length - 1][1];
            var floor = train[train.length - 1][1];
            var verdict = gap > 0.09
                ? "Large gap, low training error: variance. More data or less capacity."
                : (floor > 0.18
                    ? "Both curves high and together: bias. More capacity or better features."
                    : "Curves converged and low: this is about as good as this setup gets.");
            return {
                readout: "training error " + floor.toFixed(3) + ", validation " +
                         val[val.length - 1][1].toFixed(3) + ", gap " + gap.toFixed(3) +
                         ".  " + verdict
            };
        }
    };

    SIMS.pipeline = SIMS.leakage;
    SIMS.prcurve = SIMS.roc_pr;

    window.VizMLSims = SIMS;
})();

(function () {
    "use strict";
    var SIMS = window.VizMLSims;

    function control(spec, onChange) {
        var wrap = document.createElement("label");
        wrap.className = "ml-control";
        var name = document.createElement("span");
        name.className = "ml-control-name";
        name.textContent = spec.label;
        var value = document.createElement("span");
        value.className = "ml-control-value";
        wrap.appendChild(name);
        wrap.appendChild(value);

        var input;
        if (spec.type === "select") {
            input = document.createElement("select");
            spec.options.forEach(function (o) {
                var op = document.createElement("option");
                op.value = o.value;
                op.textContent = o.label;
                input.appendChild(op);
            });
            input.value = spec.value;
        } else {
            input = document.createElement("input");
            input.type = "range";
            input.min = spec.min;
            input.max = spec.max;
            input.step = spec.step || 1;
            input.value = spec.value;
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
        var sim = SIMS[cfg.sim];
        if (!sim) return;

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

        var tableWrap = document.createElement("div");
        tableWrap.className = "ml-table-wrap";
        root.appendChild(tableWrap);

        var panel = document.createElement("div");
        panel.className = "ml-controls";
        (cfg.controls || []).forEach(function (spec) {
            panel.appendChild(control(spec, function (key, val) {
                params[key] = val;
                schedule();
            }));
        });
        root.appendChild(panel);

        var readout = document.createElement("p");
        readout.className = "ml-readout";
        readout.setAttribute("aria-live", "polite");
        root.appendChild(readout);

        var view = {
            canvas: function (i) { return canvases[i] || canvases[0]; },
            table: function (rows) {
                tableWrap.innerHTML = "";
                var t = document.createElement("table");
                t.className = "ml-matrix";
                rows.forEach(function (r, ri) {
                    var tr = document.createElement("tr");
                    r.forEach(function (cell, ci) {
                        var td = document.createElement(ri === 0 || ci === 0 ? "th" : "td");
                        td.textContent = cell;
                        tr.appendChild(td);
                    });
                    t.appendChild(tr);
                });
                tableWrap.appendChild(t);
            }
        };

        var queued = false;
        function schedule() {
            if (queued) return;
            queued = true;
            requestAnimationFrame(function () { queued = false; render(); });
        }
        function render() {
            var res = sim(params, view) || {};
            readout.textContent = res.readout || "";
        }

        /* The outlier module is dragged rather than sliddered: the point of it
         * is that moving one row moves the fit, and a slider labelled "y of the
         * outlier" hides that it is a data point at all. */
        if (cfg.drag) {
            var c0 = canvases[0];
            var dragging = false;
            var toData = function (ev) {
                var r = c0.getBoundingClientRect();
                var px = (ev.touches ? ev.touches[0].clientX : ev.clientX) - r.left;
                var py = (ev.touches ? ev.touches[0].clientY : ev.clientY) - r.top;
                var pad = { l: 42, r: 12, t: 12, b: 30 };
                var x = cfg.drag.xr[0] + (px - pad.l) / (r.width - pad.l - pad.r) *
                        (cfg.drag.xr[1] - cfg.drag.xr[0]);
                var y = cfg.drag.yr[0] + (r.height - pad.b - py) /
                        (r.height - pad.t - pad.b) * (cfg.drag.yr[1] - cfg.drag.yr[0]);
                return [Math.max(cfg.drag.xr[0], Math.min(cfg.drag.xr[1], x)),
                        Math.max(cfg.drag.yr[0], Math.min(cfg.drag.yr[1], y))];
            };
            var move = function (ev) {
                if (!dragging) return;
                var d = toData(ev);
                params[cfg.drag.xKey] = d[0];
                params[cfg.drag.yKey] = d[1];
                schedule();
                ev.preventDefault();
            };
            c0.style.touchAction = "none";
            c0.addEventListener("pointerdown", function (ev) {
                dragging = true;
                c0.setPointerCapture(ev.pointerId);
                move(ev);
            });
            c0.addEventListener("pointermove", move);
            c0.addEventListener("pointerup", function () { dragging = false; });
            c0.addEventListener("pointercancel", function () { dragging = false; });

            var hint = document.createElement("p");
            hint.className = "ml-hint";
            hint.textContent = "Drag anywhere on the chart to move the highlighted point.";
            root.insertBefore(hint, panel);
        }

        render();
        window.addEventListener("resize", schedule);
        root.dataset.vzMlReady = "1";
    }

    function init() {
        Array.prototype.forEach.call(
            document.querySelectorAll("[data-vz-ml]"), mount);
    }

    if (document.readyState === "loading")
        document.addEventListener("DOMContentLoaded", init);
    else init();
})();
