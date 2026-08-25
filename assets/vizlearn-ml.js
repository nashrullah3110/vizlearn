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
 * The plotter, the RNG and the numeric helpers live in vizlearn-plot.js, which
 * the maths modules share.
 *
 * Binds to [data-vz-ml]; costs nothing on a page that has none.
 */
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

/* Tier 2: clustering, interpretation and ensembles.
 *
 * Same rule as tier 1 - everything here is computed in the page from data
 * generated in the page. DBSCAN really runs DBSCAN, permutation importance
 * really shuffles a column and re-scores, and the isolation forest really
 * builds trees and averages path lengths. A recorded number would let the
 * reader move a slider and see nothing, which is the one thing these pages
 * cannot afford.
 */
(function () {
    "use strict";
    var V = window.VizML, D = window.VizMLData, SIMS = window.VizMLSims;
    var Plot = V.Plot, rng = V.rng, normal = V.normal, css = V.css, pct = V.pct;

    // ----------------------------------------------------------- datasets

    /* Two interleaved crescents. Chosen because k-means provably cannot
     * separate them and DBSCAN trivially can, which is the whole argument for
     * density-based clustering. */
    function moons(n, noise, seed) {
        var r = rng(seed || 41), pts = [], i;
        for (i = 0; i < n; i++) {
            var t = Math.PI * (i % 2 ? 1 : 0) + Math.PI * r();
            var upper = i % 2 === 0;
            var x = Math.cos(t) + (upper ? 0 : 1);
            var y = Math.sin(t) * (upper ? 1 : -1) + (upper ? 0 : 0.35);
            pts.push([x + normal(r) * noise, y + normal(r) * noise, upper ? 0 : 1]);
        }
        return pts;
    }

    /* Three roughly spherical blobs of unequal size, plus a scatter of points
     * belonging to none of them. */
    function blobs(seed, spread) {
        var r = rng(seed || 47), pts = [], i, k;
        var centres = [[-1.4, 1.0], [1.5, 1.2], [0.2, -1.3]];
        var counts = [45, 30, 38];
        for (k = 0; k < centres.length; k++)
            for (i = 0; i < counts[k]; i++)
                pts.push([centres[k][0] + normal(r) * (spread || 0.34),
                          centres[k][1] + normal(r) * (spread || 0.34), k]);
        for (i = 0; i < 10; i++) pts.push([-3 + 6 * r(), -3 + 5 * r(), -1]);
        return pts;
    }

    function dist2(a, b) {
        var dx = a[0] - b[0], dy = a[1] - b[1];
        return dx * dx + dy * dy;
    }

    function kmeans(pts, k, seed) {
        var r = rng(seed || 5), cent = [], i, j;
        for (i = 0; i < k; i++) cent.push(pts[Math.floor(r() * pts.length)].slice(0, 2));
        var assign = new Array(pts.length).fill(0);
        for (var it = 0; it < 30; it++) {
            for (i = 0; i < pts.length; i++) {
                var best = 0, bd = Infinity;
                for (j = 0; j < k; j++) {
                    var d = dist2(pts[i], cent[j]);
                    if (d < bd) { bd = d; best = j; }
                }
                assign[i] = best;
            }
            for (j = 0; j < k; j++) {
                var sx = 0, sy = 0, n = 0;
                for (i = 0; i < pts.length; i++)
                    if (assign[i] === j) { sx += pts[i][0]; sy += pts[i][1]; n++; }
                if (n) cent[j] = [sx / n, sy / n];
            }
        }
        var inertia = 0;
        for (i = 0; i < pts.length; i++) inertia += dist2(pts[i], cent[assign[i]]);
        return { assign: assign, centroids: cent, inertia: inertia };
    }

    function silhouette(pts, assign, k) {
        var i, j, total = 0, counted = 0;
        for (i = 0; i < pts.length; i++) {
            var own = [], other = [];
            for (j = 0; j < k; j++) other.push([]);
            for (j = 0; j < pts.length; j++) {
                if (i === j) continue;
                var d = Math.sqrt(dist2(pts[i], pts[j]));
                if (assign[j] === assign[i]) own.push(d); else other[assign[j]].push(d);
            }
            if (!own.length) continue;
            var a = V.mean(own), b = Infinity;
            for (j = 0; j < k; j++)
                if (j !== assign[i] && other[j].length) b = Math.min(b, V.mean(other[j]));
            if (!isFinite(b)) continue;
            total += (b - a) / Math.max(a, b);
            counted++;
        }
        return counted ? total / counted : 0;
    }

    // -------------------------------------------------------------- sims

    /* DBSCAN, run for real: region queries, core points, density-reachable
     * expansion, and everything left over labelled noise. */
    SIMS.dbscan = function (p, view) {
        var pts = p.shape === "moons" ? moons(120, 0.09, 41) : blobs(47, 0.34);
        var eps2 = p.eps * p.eps, minPts = p.minPts | 0;
        var n = pts.length, label = new Array(n).fill(undefined), i, j;

        var neighbours = function (i) {
            var out = [];
            for (var j = 0; j < n; j++) if (dist2(pts[i], pts[j]) <= eps2) out.push(j);
            return out;
        };

        var cluster = 0, cores = 0;
        for (i = 0; i < n; i++) {
            if (label[i] !== undefined) continue;
            var nb = neighbours(i);
            if (nb.length < minPts) { label[i] = -1; continue; }   // noise, for now
            cores++;
            label[i] = cluster;
            var queue = nb.slice();
            for (var q = 0; q < queue.length; q++) {
                var m = queue[q];
                if (label[m] === -1) label[m] = cluster;           // border point
                if (label[m] !== undefined) continue;
                label[m] = cluster;
                var nb2 = neighbours(m);
                if (nb2.length >= minPts) { cores++; queue = queue.concat(nb2); }
            }
            cluster++;
        }

        var noise = label.filter(function (l) { return l === -1; }).length;
        var PAL = [V.POS(), css("--accent-primary", "#b06d10"),
                   "#6aa9d8", "#7bbf88", "#c58fd0"];
        var plot = Plot(view.canvas(0), { xr: [-3.2, 3.2], yr: [-2.6, 2.6], height: 300 });
        plot.axes("feature 1", "feature 2");
        for (i = 0; i < n; i++) {
            var l = label[i];
            if (l === -1) plot.ring(pts[i][0], pts[i][1], V.NEG(), 3.4);
            else plot.dot(pts[i][0], pts[i][1], PAL[l % PAL.length], 3.4);
        }
        return {
            readout: cluster + " cluster" + (cluster === 1 ? "" : "s") + " found, " +
                     noise + " points left as noise (drawn hollow).  eps " +
                     p.eps.toFixed(2) + ", minPts " + minPts +
                     " - nothing told it how many clusters to look for."
        };
    };

    /* Agglomerative clustering with a real dendrogram: merge the two closest
     * clusters, record the height, repeat. The linkage choice changes what
     * "closest" means, which is the point. */
    SIMS.hierarchical = function (p, view) {
        var pts = blobs(47, 0.34).filter(function (q) { return q[2] >= 0; }).slice(0, 26);
        var clusters = pts.map(function (q, i) { return { members: [i], x: q[0], y: q[1] }; });
        var merges = [], link = p.linkage;

        var linkDist = function (a, b) {
            var best = link === "single" ? Infinity : (link === "complete" ? 0 : 0);
            var sum = 0, count = 0;
            for (var i = 0; i < a.members.length; i++)
                for (var j = 0; j < b.members.length; j++) {
                    var d = Math.sqrt(dist2(pts[a.members[i]], pts[b.members[j]]));
                    if (link === "single") best = Math.min(best, d);
                    else if (link === "complete") best = Math.max(best, d);
                    sum += d; count++;
                }
            return link === "average" ? sum / count : best;
        };

        while (clusters.length > 1) {
            var bi = 0, bj = 1, bd = Infinity;
            for (var i = 0; i < clusters.length; i++)
                for (var j = i + 1; j < clusters.length; j++) {
                    var d = linkDist(clusters[i], clusters[j]);
                    if (d < bd) { bd = d; bi = i; bj = j; }
                }
            merges.push(bd);
            clusters[bi] = { members: clusters[bi].members.concat(clusters[bj].members) };
            clusters.splice(bj, 1);
        }

        // How many clusters a horizontal cut at this height leaves.
        var cut = p.cut;
        var above = merges.filter(function (h) { return h > cut; }).length;
        var kAtCut = above + 1;

        var maxH = Math.max.apply(null, merges);
        var plot = Plot(view.canvas(0), { xr: [0, merges.length + 1], yr: [0, maxH * 1.08],
                                          height: 280, pad: { l: 52, r: 12, t: 14, b: 34 } });
        plot.axes("merge number", "distance at merge");
        plot.line(merges.map(function (h, i) { return [i + 1, h]; }), V.LINE(), 2);
        merges.forEach(function (h, i) { plot.dot(i + 1, h, V.POS(), 3); });
        plot.ctx.save();
        plot.ctx.strokeStyle = V.POS();
        plot.ctx.setLineDash([5, 4]);
        plot.ctx.beginPath();
        plot.ctx.moveTo(plot.px(0), plot.py(cut));
        plot.ctx.lineTo(plot.px(merges.length + 1), plot.py(cut));
        plot.ctx.stroke();
        plot.ctx.restore();

        return {
            readout: link + " linkage.  A cut at " + cut.toFixed(2) +
                     " leaves " + kAtCut + " cluster" + (kAtCut === 1 ? "" : "s") +
                     " - the tree was built once, and k is chosen afterwards by " +
                     "where you cut."
        };
    };

    /* Elbow and silhouette computed over the same data, side by side, because
     * they frequently disagree and the disagreement is the lesson. */
    SIMS.choosek = function (p, view) {
        var pts = p.shape === "moons" ? moons(110, 0.09, 41)
                                      : blobs(47, p.spread).filter(function (q) { return q[2] >= 0; });
        var inertias = [], sils = [], k;
        for (k = 1; k <= 8; k++) {
            var km = kmeans(pts, k, 5);
            inertias.push([k, km.inertia]);
            sils.push([k, k === 1 ? 0 : silhouette(pts, km.assign, k)]);
        }
        var maxI = inertias[0][1];
        var a = Plot(view.canvas(0), { xr: [1, 8], yr: [0, maxI * 1.05], height: 240,
                                       pad: { l: 56, r: 12, t: 12, b: 32 } });
        a.axes("k", "inertia", 7);
        a.line(inertias, V.LINE(), 2);
        inertias.forEach(function (q) { a.dot(q[0], q[1], V.POS(), 3.4); });

        var b = Plot(view.canvas(1), { xr: [1, 8], yr: [0, 1], height: 240,
                                       pad: { l: 56, r: 12, t: 12, b: 32 } });
        b.axes("k", "silhouette", 7);
        b.line(sils, V.POS(), 2);
        sils.forEach(function (q) { b.dot(q[0], q[1], V.LINE(), 3.4); });

        var bestSil = sils.slice(1).reduce(function (m, q) { return q[1] > m[1] ? q : m; }, sils[1]);
        return {
            readout: "silhouette peaks at k = " + bestSil[0] + " (" + bestSil[1].toFixed(3) +
                     ").  Inertia falls at every k and always will - it cannot pick one, " +
                     "which is why the elbow is judged by eye and the silhouette is not."
        };
    };

    /* A one-dimensional Gaussian mixture fitted by EM, against the hard
     * assignment k-means would make on the same data. */
    SIMS.gmm = function (p, view) {
        var r = rng(53), data = [], i, it;
        for (i = 0; i < 150; i++) data.push(normal(r) * 0.7 + 2.0);
        for (i = 0; i < 110; i++) data.push(normal(r) * p.spread + 4.6);

        var mu = [1.2, 5.4], sg = [1, 1], w = [0.5, 0.5];
        var resp = data.map(function () { return [0, 0]; });
        var g = function (x, m, s) {
            return Math.exp(-(x - m) * (x - m) / (2 * s * s)) / (s * Math.sqrt(2 * Math.PI));
        };
        for (it = 0; it < p.iters; it++) {
            for (i = 0; i < data.length; i++) {                 // E step
                var a = w[0] * g(data[i], mu[0], sg[0]);
                var b = w[1] * g(data[i], mu[1], sg[1]);
                var s = a + b || 1e-9;
                resp[i][0] = a / s; resp[i][1] = b / s;
            }
            for (var k = 0; k < 2; k++) {                        // M step
                var nk = 0, sum = 0, varr = 0;
                for (i = 0; i < data.length; i++) { nk += resp[i][k]; sum += resp[i][k] * data[i]; }
                mu[k] = sum / (nk || 1);
                for (i = 0; i < data.length; i++)
                    varr += resp[i][k] * (data[i] - mu[k]) * (data[i] - mu[k]);
                sg[k] = Math.sqrt(varr / (nk || 1)) || 0.1;
                w[k] = nk / data.length;
            }
        }

        var plot = Plot(view.canvas(0), { xr: [-1, 8], yr: [0, 0.42], height: 270,
                                          pad: { l: 52, r: 12, t: 12, b: 32 } });
        plot.axes("value", "density");
        var bins = 40, hist = new Array(bins).fill(0);
        data.forEach(function (x) {
            var b = Math.floor((x + 1) / 9 * bins);
            if (b >= 0 && b < bins) hist[b]++;
        });
        var scale = 0.42 / Math.max.apply(null, hist);
        hist.forEach(function (c, b) {
            plot.bar(-1 + b * 9 / bins, -1 + (b + 0.85) * 9 / bins, c * scale, V.NEG());
        });
        [0, 1].forEach(function (k) {
            var curve = [];
            for (var x = -1; x <= 8; x += 0.06) curve.push([x, w[k] * g(x, mu[k], sg[k])]);
            plot.line(curve, k ? V.POS() : V.LINE(), 2);
        });

        var ambiguous = resp.filter(function (q) {
            return Math.max(q[0], q[1]) < 0.9;
        }).length;
        return {
            readout: "after " + p.iters + " EM iterations: means " + mu[0].toFixed(2) +
                     " and " + mu[1].toFixed(2) + ", widths " + sg[0].toFixed(2) +
                     " and " + sg[1].toFixed(2) + ".  " + ambiguous +
                     " of " + data.length + " points are assigned with less than 90% " +
                     "confidence - k-means would have to guess for every one of them."
        };
    };

    window.VizMLSims = SIMS;
})();

/* Tier 2, part two: dimensionality reduction, interpretation and ensembles. */
(function () {
    "use strict";
    var V = window.VizML, D = window.VizMLData, SIMS = window.VizMLSims;
    var Plot = V.Plot, rng = V.rng, normal = V.normal, css = V.css, pct = V.pct;

    /* Three well-separated clusters arranged on a line in high-ish dimensions,
     * so that "did the layout keep the global arrangement" has a right answer
     * the reader can check. */
    function structured(seed) {
        var r = rng(seed || 61), pts = [], k, i;
        var centres = [[0, 0, 0], [6, 0.4, 0], [12, -0.3, 0]];
        for (k = 0; k < 3; k++)
            for (i = 0; i < 34; i++)
                pts.push({ v: [centres[k][0] + normal(r) * 0.8,
                               centres[k][1] + normal(r) * 0.8,
                               centres[k][2] + normal(r) * 0.8], c: k });
        return pts;
    }

    function pca2(pts) {
        var n = pts.length, d = 3, i, j, k;
        var mean = [0, 0, 0];
        for (i = 0; i < n; i++) for (j = 0; j < d; j++) mean[j] += pts[i].v[j] / n;
        var X = pts.map(function (p) {
            return p.v.map(function (x, j) { return x - mean[j]; });
        });
        // Power iteration for the top two components - enough for three
        // dimensions and short enough to read.
        var comp = [];
        var C = [];
        for (i = 0; i < d; i++) { C.push([]); for (j = 0; j < d; j++) C[i].push(0); }
        for (k = 0; k < n; k++)
            for (i = 0; i < d; i++) for (j = 0; j < d; j++) C[i][j] += X[k][i] * X[k][j] / n;
        for (var c = 0; c < 2; c++) {
            var v = [Math.random() || 0.5, 0.3, 0.2];
            for (var it = 0; it < 80; it++) {
                var w = [0, 0, 0];
                for (i = 0; i < d; i++) for (j = 0; j < d; j++) w[i] += C[i][j] * v[j];
                comp.forEach(function (u) {
                    var dot = u[0] * w[0] + u[1] * w[1] + u[2] * w[2];
                    for (i = 0; i < d; i++) w[i] -= dot * u[i];
                });
                var norm = Math.hypot(w[0], w[1], w[2]) || 1;
                v = w.map(function (x) { return x / norm; });
            }
            comp.push(v);
        }
        return X.map(function (x, i) {
            return { x: x[0] * comp[0][0] + x[1] * comp[0][1] + x[2] * comp[0][2],
                     y: x[0] * comp[1][0] + x[1] * comp[1][1] + x[2] * comp[1][2],
                     c: pts[i].c };
        });
    }

    /* A neighbour-preserving layout in the spirit of t-SNE: attract points
     * that are close in the original space, repel everything else. It is not
     * t-SNE - no perplexity, no KL divergence - and the page says so. What it
     * reproduces faithfully is the behaviour that matters here: local
     * structure is preserved and the distance BETWEEN clusters stops meaning
     * anything.
     */
    function neighbourLayout(pts, exaggeration, seed) {
        var r = rng(seed || 67), n = pts.length, i, j;
        var pos = pts.map(function () { return [normal(r) * 0.4, normal(r) * 0.4]; });
        var near = [];
        for (i = 0; i < n; i++) {
            var ds = [];
            for (j = 0; j < n; j++) if (i !== j) {
                var s = 0;
                for (var k = 0; k < 3; k++) {
                    var dd = pts[i].v[k] - pts[j].v[k];
                    s += dd * dd;
                }
                ds.push([s, j]);
            }
            ds.sort(function (a, b) { return a[0] - b[0]; });
            near.push(ds.slice(0, 8).map(function (q) { return q[1]; }));
        }
        for (var it = 0; it < 220; it++) {
            var grad = pos.map(function () { return [0, 0]; });
            for (i = 0; i < n; i++) {
                near[i].forEach(function (j) {                       // attract
                    var dx = pos[i][0] - pos[j][0], dy = pos[i][1] - pos[j][1];
                    grad[i][0] -= dx * 0.02 * exaggeration;
                    grad[i][1] -= dy * 0.02 * exaggeration;
                });
                for (j = 0; j < n; j++) {                            // repel
                    if (i === j) continue;
                    var ex = pos[i][0] - pos[j][0], ey = pos[i][1] - pos[j][1];
                    var d2 = ex * ex + ey * ey + 0.06;
                    grad[i][0] += ex / d2 * 0.010;
                    grad[i][1] += ey / d2 * 0.010;
                }
            }
            for (i = 0; i < n; i++) { pos[i][0] += grad[i][0]; pos[i][1] += grad[i][1]; }
        }
        return pos.map(function (q, i) { return { x: q[0], y: q[1], c: pts[i].c }; });
    }

    SIMS.embedding = function (p, view) {
        var pts = structured(61);
        var laid = p.method === "pca" ? pca2(pts)
                                      : neighbourLayout(pts, p.attract, 67);
        var xs = laid.map(function (q) { return q.x; });
        var ys = laid.map(function (q) { return q.y; });
        var pad = function (a) {
            var lo = Math.min.apply(null, a), hi = Math.max.apply(null, a);
            var m = (hi - lo) * 0.1 || 1;
            return [lo - m, hi + m];
        };
        var PAL = [V.POS(), css("--accent-primary", "#b06d10"), "#6aa9d8"];
        var plot = Plot(view.canvas(0), { xr: pad(xs), yr: pad(ys), height: 300 });
        plot.axes(p.method === "pca" ? "component 1" : "dimension 1",
                  p.method === "pca" ? "component 2" : "dimension 2");
        laid.forEach(function (q) { plot.dot(q.x, q.y, PAL[q.c], 3.4); });

        // In the original data the three clusters sit on a line, 6 apart and
        // 12 apart. Does the layout preserve that ratio?
        var centre = [0, 1, 2].map(function (c) {
            var g = laid.filter(function (q) { return q.c === c; });
            return [V.mean(g.map(function (q) { return q.x; })),
                    V.mean(g.map(function (q) { return q.y; }))];
        });
        var d01 = Math.hypot(centre[0][0] - centre[1][0], centre[0][1] - centre[1][1]);
        var d02 = Math.hypot(centre[0][0] - centre[2][0], centre[0][1] - centre[2][1]);
        var ratio = d01 ? d02 / d01 : 0;
        return {
            readout: "In the original data cluster 3 is exactly twice as far from " +
                     "cluster 1 as cluster 2 is (ratio 2.00).  Here that ratio is " +
                     ratio.toFixed(2) + " - " +
                     (p.method === "pca"
                        ? "PCA is a linear projection, so global distances survive."
                        : "a neighbour-preserving layout keeps the groups apart and " +
                          "makes the distance between them meaningless.")
        };
    };

    /* Permutation importance, actually performed: score the model, shuffle one
     * column, score again, report the drop.
     *
     * The model is a small random forest rather than the logistic regression
     * this started as, and the reason is the lesson the page is built around.
     * A linear model given two near-duplicate columns SPLITS its weight
     * between them, so shuffling one still destroys half the signal and both
     * columns score as important - the masking the article describes never
     * appeared on screen. A forest that samples features at each split uses
     * whichever twin it happened to draw, so shuffling one leaves plenty of
     * trees relying on the other, and the drop collapses. That is the real
     * effect, and now the chart shows it.
     */
    SIMS.importance = function (p, view) {
        var r = rng(71), n = 320, rows = [], i;
        for (i = 0; i < n; i++) {
            var a = normal(r), b = normal(r), noise = normal(r);
            var dup = a + normal(r) * 0.04;             // near-duplicate of a
            var y = (2.2 * a + 0.9 * b + normal(r) * 0.6) > 0 ? 1 : 0;
            rows.push({ f: [a, b, noise, dup], y: y });
        }
        var names = ["signal", "weak", "noise", "copy of signal"];
        var NF = 4;

        var forestRng = rng(131);

        /* A depth-limited CART split, choosing the best threshold on a random
         * subset of the features - the feature subsampling is what makes the
         * twins substitutable. */
        var grow = function (idx, depth) {
            var ones = 0;
            idx.forEach(function (i) { ones += rows[i].y; });
            if (depth >= 4 || idx.length < 8 || ones === 0 || ones === idx.length)
                return { leaf: true, p: idx.length ? ones / idx.length : 0.5 };

            var tryFeats = [];
            while (tryFeats.length < 2) {
                var f = Math.floor(forestRng() * NF);
                if (tryFeats.indexOf(f) === -1) tryFeats.push(f);
            }
            var best = null;
            tryFeats.forEach(function (f) {
                var vals = idx.map(function (i) { return rows[i].f[f]; }).sort(function (x, y2) { return x - y2; });
                for (var q = 1; q < 6; q++) {
                    var thr = vals[Math.floor(vals.length * q / 6)];
                    var lo = [], hi = [];
                    idx.forEach(function (i) { (rows[i].f[f] < thr ? lo : hi).push(i); });
                    if (lo.length < 4 || hi.length < 4) continue;
                    var gini = function (set) {
                        var o = 0;
                        set.forEach(function (i) { o += rows[i].y; });
                        var pr = o / set.length;
                        return 2 * pr * (1 - pr) * set.length;
                    };
                    var score = gini(lo) + gini(hi);
                    if (!best || score < best.score)
                        best = { score: score, f: f, thr: thr, lo: lo, hi: hi };
                }
            });
            if (!best) return { leaf: true, p: idx.length ? ones / idx.length : 0.5 };
            return { leaf: false, f: best.f, thr: best.thr,
                     l: grow(best.lo, depth + 1), r: grow(best.hi, depth + 1) };
        };

        var predictTree = function (node, f) {
            while (!node.leaf) node = f[node.f] < node.thr ? node.l : node.r;
            return node.p;
        };

        var TREES = 24, forest = [];
        for (var t = 0; t < TREES; t++) {
            var idx = [];
            for (i = 0; i < n; i++) idx.push(Math.floor(forestRng() * n));   // bootstrap
            forest.push(grow(idx, 0));
        }
        var predict = function (f) {
            var sum = 0;
            for (var t = 0; t < TREES; t++) sum += predictTree(forest[t], f);
            return sum / TREES;
        };
        var score = function (data) {
            var right = 0;
            data.forEach(function (row) {
                if ((predict(row.f) >= 0.5 ? 1 : 0) === row.y) right++;
            });
            return right / data.length;
        };

        var base = score(rows);
        var shuffleSeed = rng(p.seed || 83);
        var drops = [];
        for (var k = 0; k < NF; k++) {
            var reps = [];
            for (var rep = 0; rep < p.repeats; rep++) {
                var copy = rows.map(function (row) { return { f: row.f.slice(), y: row.y }; });
                for (i = copy.length - 1; i > 0; i--) {
                    var j = Math.floor(shuffleSeed() * (i + 1));
                    var tmp = copy[i].f[k]; copy[i].f[k] = copy[j].f[k]; copy[j].f[k] = tmp;
                }
                reps.push(base - score(copy));
            }
            drops.push(V.mean(reps));
        }

        var maxD = Math.max.apply(null, drops.concat([0.02]));
        var minD = Math.min(0, Math.min.apply(null, drops));
        var plot = Plot(view.canvas(0), { xr: [0, 4], yr: [minD - 0.01, maxD * 1.15],
                                          height: 260, pad: { l: 60, r: 12, t: 12, b: 46 } });
        plot.axes("", "accuracy drop when shuffled", 4);
        drops.forEach(function (d, k) {
            plot.bar(k + 0.18, k + 0.82, d, (k === 0 || k === 3) ? V.NEG() : V.POS());
        });
        var ctx = plot.ctx;
        ctx.fillStyle = css("--text-muted", "#999");
        ctx.font = "10px " + css("--vz-mono", "monospace");
        ctx.textAlign = "center";
        names.forEach(function (nm, k) { ctx.fillText(nm, plot.px(k + 0.5), plot.h - 16); });

        var shown = names.map(function (nm, k) {
            return nm + " " + (drops[k] >= 0 ? "+" : "") + (100 * drops[k]).toFixed(1);
        }).join(", ");
        /* Describe the comparison the numbers actually make. An earlier
         * version asserted that both twins score near zero; the forest does
         * not do that - it discounts the copy down to roughly the level of a
         * genuinely weak feature. Saying so is the honest version of the same
         * lesson, and it is checkable against the bars. */
        var ratio = drops[0] > 1e-6 ? drops[3] / drops[0] : 0;
        return {
            readout: "baseline accuracy " + pct(base) + ".  Accuracy drop when shuffled, " +
                     "averaged over " + p.repeats + " shuffle" + (p.repeats === 1 ? "" : "s") +
                     " (percentage points): " + shown +
                     ".  'copy of signal' carries the same information as 'signal' yet " +
                     "scores " + (100 * ratio).toFixed(0) + "% of it, about the level of " +
                     "'weak' - shuffle it and the forest falls back on its twin. Neither " +
                     "number says what that column is worth on its own."
        };
    };

    /* Partial dependence with individual conditional expectation curves, so an
     * averaged-away interaction is visible rather than merely warned about. */
    SIMS.pdp = function (p, view) {
        var r = rng(89), rows = [], i;
        for (i = 0; i < 90; i++) {
            var x = -3 + 6 * r(), g = r() < 0.5 ? 0 : 1;
            rows.push({ x: x, g: g });
        }
        // With interaction on, the effect of x reverses by group. The average
        // of the two is flat, which is exactly the trap.
        var f = function (x, g) {
            return p.interaction
                ? (g ? -0.9 * x : 0.9 * x)
                : 0.9 * x + (g ? 0.6 : -0.6);
        };
        var plot = Plot(view.canvas(0), { xr: [-3, 3], yr: [-3.4, 3.4], height: 280 });
        plot.axes("feature x", "predicted value");
        if (p.showIce)
            rows.forEach(function (row) {
                var curve = [];
                for (var x = -3; x <= 3; x += 0.25) curve.push([x, f(x, row.g)]);
                plot.line(curve, row.g ? V.NEG() : V.NEG(), 0.7);
            });
        var pd = [];
        for (var x = -3; x <= 3; x += 0.15) {
            var vals = rows.map(function (row) { return f(x, row.g); });
            pd.push([x, V.mean(vals)]);
        }
        plot.line(pd, V.LINE(), 3);

        var slope = (pd[pd.length - 1][1] - pd[0][1]) / 6;
        return {
            readout: p.interaction
                ? "The partial dependence line is almost flat (slope " + slope.toFixed(2) +
                  "), which reads as 'x does not matter'. The ICE curves say otherwise: " +
                  "x matters a great deal, in opposite directions per group, and the " +
                  "average cancels them."
                : "No interaction: every ICE curve has the same shape, so the partial " +
                  "dependence line (slope " + slope.toFixed(2) + ") describes each " +
                  "individual as well as the average."
        };
    };

    /* A reliability diagram, with a temperature knob that miscalibrates a
     * model whose ranking never changes. */
    SIMS.calibration = function (p, view) {
        var r = rng(97), n = 1600, rows = [], i;
        for (i = 0; i < n; i++) {
            var t = r();
            var truth = t;                                  // true probability
            var y = r() < truth ? 1 : 0;
            // Temperature scaling in logit space: sharpens or flattens the
            // scores without changing their order at all.
            var logit = Math.log(truth / (1 - truth || 1e-9) || 1e-9);
            var s = 1 / (1 + Math.exp(-logit / p.temperature));
            rows.push({ s: Math.min(0.999, Math.max(0.001, s)), y: y });
        }
        var bins = 10, sum = new Array(bins).fill(0), cnt = new Array(bins).fill(0),
            pos = new Array(bins).fill(0);
        rows.forEach(function (row) {
            var b = Math.min(bins - 1, Math.floor(row.s * bins));
            sum[b] += row.s; cnt[b]++; pos[b] += row.y;
        });
        var pts = [], ece = 0;
        for (i = 0; i < bins; i++) {
            if (!cnt[i]) continue;
            var conf = sum[i] / cnt[i], acc = pos[i] / cnt[i];
            pts.push([conf, acc]);
            ece += cnt[i] / n * Math.abs(conf - acc);
        }
        var plot = Plot(view.canvas(0), { xr: [0, 1], yr: [0, 1], height: 280 });
        plot.axes("predicted probability", "observed frequency");
        plot.line([[0, 0], [1, 1]], V.NEG(), 1.4, [5, 4]);
        plot.line(pts, V.LINE(), 2.2);
        pts.forEach(function (q) { plot.dot(q[0], q[1], V.POS(), 3.6); });

        var verdict = p.temperature > 1.05 ? "under-confident - it hedges when it should not"
                    : (p.temperature < 0.95 ? "over-confident - the usual failure, and the one that matters"
                                            : "well calibrated");
        return {
            readout: "expected calibration error " + ece.toFixed(3) + " - " + verdict +
                     ".  Temperature scaling changes no ranking at all, so AUC is " +
                     "identical at every setting on this slider."
        };
    };

    /* An isolation forest, built for real: each tree is grown from a random
     * subsample, and then EVERY point is dropped through it to find its path
     * length.
     *
     * Scoring only the sampled points was the first attempt and it was wrong:
     * a point missing from a tree contributed nothing that round, so its
     * average path came out short and its anomaly score high. Everything
     * looked like an outlier. A tree is built from a sample and used on all
     * of the data, which is the whole reason subsampling is cheap.
     */
    SIMS.isoforest = function (p, view) {
        var r = rng(101), pts = [], i;
        for (i = 0; i < 150; i++) pts.push([normal(r) * 0.7, normal(r) * 0.7]);
        for (i = 0; i < 8; i++) pts.push([-3 + 6 * r(), -3 + 6 * r()]);

        var forest = rng(p.seed || 103);
        var sample = Math.min(pts.length, p.sample | 0);
        var limit = Math.ceil(Math.log2(sample));

        /* Expected path length of an unsuccessful search in a BST of n nodes -
         * the correction that stops a truncated branch from looking shallow. */
        var cFactor = function (n) {
            if (n <= 1) return 0;
            return 2 * (Math.log(n - 1) + 0.5772156649) - 2 * (n - 1) / n;
        };

        var build = function (subset, depth) {
            if (subset.length <= 1 || depth >= limit)
                return { leaf: true, size: subset.length, depth: depth };
            var dim = forest() < 0.5 ? 0 : 1;
            var vals = subset.map(function (i) { return pts[i][dim]; });
            var lo = Math.min.apply(null, vals), hi = Math.max.apply(null, vals);
            if (hi - lo < 1e-9) return { leaf: true, size: subset.length, depth: depth };
            var split = lo + forest() * (hi - lo);
            return {
                leaf: false, dim: dim, split: split,
                l: build(subset.filter(function (i) { return pts[i][dim] < split; }), depth + 1),
                r: build(subset.filter(function (i) { return pts[i][dim] >= split; }), depth + 1)
            };
        };

        var pathOf = function (node, q, depth) {
            if (node.leaf) return depth + cFactor(node.size);
            return pathOf(q[node.dim] < node.split ? node.l : node.r, q, depth + 1);
        };

        var lengths = new Array(pts.length).fill(0);
        for (var t = 0; t < p.trees; t++) {
            var idx = [];
            for (i = 0; i < pts.length; i++) idx.push(i);
            for (i = idx.length - 1; i > 0; i--) {
                var j = Math.floor(forest() * (i + 1));
                var tmp = idx[i]; idx[i] = idx[j]; idx[j] = tmp;
            }
            var tree = build(idx.slice(0, sample), 0);
            for (i = 0; i < pts.length; i++) lengths[i] += pathOf(tree, pts[i], 0);
        }

        var c = cFactor(sample);
        var scores = lengths.map(function (L) {
            return Math.pow(2, -(L / p.trees) / c);
        });

        var plot = Plot(view.canvas(0), { xr: [-3.4, 3.4], yr: [-3.4, 3.4], height: 300 });
        plot.axes("feature 1", "feature 2");
        var flagged = 0;
        pts.forEach(function (q, i) {
            var anomalous = scores[i] > p.threshold;
            if (anomalous) flagged++;
            if (anomalous) { plot.dot(q[0], q[1], V.POS(), 5); plot.ring(q[0], q[1], V.POS(), 9); }
            else plot.dot(q[0], q[1], V.NEG(), 3);
        });
        var lo = Math.min.apply(null, scores), hi = Math.max.apply(null, scores);
        return {
            readout: p.trees + " trees, " + sample + " points sampled to build each.  " +
                     "Scores run " + lo.toFixed(2) + " to " + hi.toFixed(2) + "; " +
                     flagged + " point" + (flagged === 1 ? "" : "s") + " above " +
                     p.threshold.toFixed(2) + ".  A short average path means a HIGH " +
                     "score - the model never learns what normal looks like, only " +
                     "what is easy to cut off."
        };
    };

    /* Voting and stacking over three deliberately different weak learners. */
    SIMS.ensembles = function (p, view) {
        var r = rng(107), n = 400, rows = [], i;
        for (i = 0; i < n; i++) {
            var a = normal(r), b = normal(r);
            /* A ring, so no straight line separates it, plus 8% label noise so
             * that no rule on this page can be perfect. An earlier version let
             * the radius learner reproduce the boundary exactly, and a 100%
             * "weak" learner makes the whole argument for ensembling vanish. */
            var inside = (a * a + b * b) > 1.6;
            var y = (r() < 0.08 ? !inside : inside) ? 1 : 0;
            rows.push({ a: a, b: b, y: y });
        }
        // Three weak learners, each wrong in a different way.
        var learners = [
            { name: "stump on a", f: function (row) { return row.a > p.t1 ? 1 : 0; } },
            { name: "stump on b", f: function (row) { return row.b > p.t2 ? 1 : 0; } },
            { name: "radius rule", f: function (row) {
                return (row.a * row.a + row.b * row.b) > p.t3 ? 1 : 0; } }
        ];
        var acc = learners.map(function (L) {
            var right = 0;
            rows.forEach(function (row) { if (L.f(row) === row.y) right++; });
            return right / n;
        });
        var voteRight = 0, stackRight = 0;
        // Stacking: a tiny logistic model over the three predictions.
        var w = [0, 0, 0], b0 = 0;
        for (var it = 0; it < 400; it++) {
            var gw = [0, 0, 0], gb = 0;
            rows.forEach(function (row) {
                var f = learners.map(function (L) { return L.f(row); });
                var z = b0 + w[0] * f[0] + w[1] * f[1] + w[2] * f[2];
                var e = 1 / (1 + Math.exp(-z)) - row.y;
                gw[0] += e * f[0]; gw[1] += e * f[1]; gw[2] += e * f[2]; gb += e;
            });
            for (var k = 0; k < 3; k++) w[k] -= 0.3 * gw[k] / n;
            b0 -= 0.3 * gb / n;
        }
        rows.forEach(function (row) {
            var f = learners.map(function (L) { return L.f(row); });
            if ((f[0] + f[1] + f[2] >= 2 ? 1 : 0) === row.y) voteRight++;
            var z = b0 + w[0] * f[0] + w[1] * f[1] + w[2] * f[2];
            if (((z > 0) ? 1 : 0) === row.y) stackRight++;
        });

        var bars = acc.concat([voteRight / n, stackRight / n]);
        var labels = ["stump a", "stump b", "radius", "vote", "stack"];
        var plot = Plot(view.canvas(0), { xr: [0, 5], yr: [0, 1], height: 260,
                                          pad: { l: 52, r: 12, t: 12, b: 46 } });
        plot.axes("", "accuracy", 5);
        bars.forEach(function (v, k) {
            plot.bar(k + 0.16, k + 0.84, v, k < 3 ? V.NEG() : V.POS());
        });
        var ctx = plot.ctx;
        ctx.fillStyle = css("--text-muted", "#999");
        ctx.font = "10px " + css("--vz-mono", "monospace");
        ctx.textAlign = "center";
        labels.forEach(function (nm, k) { ctx.fillText(nm, plot.px(k + 0.5), plot.h - 16); });

        var bestSingle = Math.max.apply(null, acc);
        var vote = voteRight / n, stack = stackRight / n;
        /* Report what happened rather than the story ensembles are usually
         * told with. On this data the vote is regularly WORSE than the best
         * single learner, because two of the three are close to useless and a
         * majority vote has to count them equally. That is the useful lesson
         * here, and overwriting it with "the ensemble wins" would be a lie the
         * reader can check. */
        var verdict = vote < bestSingle
            ? "The vote is WORSE than the best single learner: two of the three are " +
              "near-useless here, and a majority vote has to count them equally."
            : "The vote beats every single learner - the errors were independent " +
              "enough to cancel.";
        var stackNote = stack > bestSingle + 0.005
            ? "  Stacking beat it outright."
            : (stack >= bestSingle - 0.005
                ? "  Stacking matched the best single learner by learning to lean on it."
                : "  Stacking underperformed it, which is what overfitting the combiner looks like.");
        return {
            readout: "single learners " + acc.map(pct).join(" / ") + "; vote " +
                     pct(vote) + "; stacking " + pct(stack) + ".  " + verdict +
                     stackNote + "  Learned weights: " +
                     w.map(function (x) { return x.toFixed(1); }).join(", ") + "."
        };
    };

    window.VizMLSims = SIMS;
})();
