/* Plotting and numeric helpers shared by the generated machine_learning/ and
 * maths/ modules.
 *
 * This was the top of assets/vizlearn-ml.js. The maths harness needs the same
 * canvas plotter, the same seeded RNG and the same Gaussian sampler, and the
 * alternative to sharing them was either a second copy to drift from the
 * first, or making every maths page download 78 KB of workflow simulations to
 * reach a 6 KB plotter.
 *
 * Exports window.VizML. Both harnesses list it before themselves, and the
 * build only sends it to a page that loads one of them.
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
