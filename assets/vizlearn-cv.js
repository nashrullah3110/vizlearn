/* Interactive image-processing harness for the computer_vision/ modules.
 *
 * Ten of these modules are the same page with a different kernel: a source
 * image, a control or two, and the result beside it. Writing them ten times
 * would be ten chances for the maths to drift, so the operations live here
 * together where they can be read against each other, and each page carries
 * only which one it wants and what its controls are.
 *
 * The source images are drawn in code rather than loaded. Nothing is fetched,
 * so the pages work offline and there is no image whose licence has to be
 * tracked - and a synthetic image can be built to contain exactly the feature
 * a module is about: a hard edge for Sobel, flat regions for thresholding,
 * salt-and-pepper for the median filter.
 *
 * Binds to [data-vz-cv]; costs nothing on a page that has none.
 */
(function () {
    "use strict";

    var W = 192, H = 144;

    // ---------------------------------------------------------------- images

    function blank() {
        return { w: W, h: H, d: new Uint8ClampedArray(W * H * 4) };
    }

    function set(img, x, y, r, g, b) {
        if (x < 0 || y < 0 || x >= img.w || y >= img.h) return;
        var i = (y * img.w + x) * 4;
        img.d[i] = r; img.d[i + 1] = g; img.d[i + 2] = b; img.d[i + 3] = 255;
    }

    function get(img, x, y) {
        x = x < 0 ? 0 : (x >= img.w ? img.w - 1 : x);
        y = y < 0 ? 0 : (y >= img.h ? img.h - 1 : y);
        return (y * img.w + x) * 4;
    }

    /* A deterministic pseudo-random source. Math.random would make every
     * redraw different, so a slider would look like it was changing the noise
     * rather than the filter. */
    function rng(seed) {
        var s = seed || 1;
        return function () {
            s = (s * 1103515245 + 12345) & 0x7fffffff;
            return s / 0x7fffffff;
        };
    }

    function disc(img, cx, cy, r, col) {
        for (var y = cy - r; y <= cy + r; y++) {
            for (var x = cx - r; x <= cx + r; x++) {
                var dx = x - cx, dy = y - cy;
                if (dx * dx + dy * dy <= r * r) set(img, x, y, col[0], col[1], col[2]);
            }
        }
    }

    function rect(img, x0, y0, w, h, col) {
        for (var y = y0; y < y0 + h; y++)
            for (var x = x0; x < x0 + w; x++) set(img, x, y, col[0], col[1], col[2]);
    }

    function tri(img, x0, y0, size, col) {
        for (var k = 0; k < size; k++)
            for (var x = x0 - k; x <= x0 + k; x++) set(img, x, y0 + k, col[0], col[1], col[2]);
    }

    var SOURCES = {
        /* Hard edges, flat interiors, a smooth background: everything a
         * convolution, a threshold or a morphological operator needs to show
         * its behaviour on. */
        shapes: function () {
            var img = blank(), x, y;
            for (y = 0; y < H; y++)
                for (x = 0; x < W; x++) {
                    var v = 40 + Math.round(70 * (x / W) + 40 * (y / H));
                    set(img, x, y, v, v, v);
                }
            disc(img, 58, 62, 26, [235, 235, 235]);
            rect(img, 104, 34, 46, 40, [20, 20, 20]);
            tri(img, 130, 88, 26, [180, 180, 180]);
            rect(img, 12, 116, 60, 8, [250, 250, 250]);
            return img;
        },
        /* Isolated bright and dark pixels on top of the shapes: the median
         * filter removes them completely and the Gaussian only smears them,
         * which is the entire point of that comparison. */
        saltpepper: function () {
            var img = SOURCES.shapes(), r = rng(7), i, x, y;
            for (i = 0; i < 900; i++) {
                x = Math.floor(r() * W); y = Math.floor(r() * H);
                var v = r() < 0.5 ? 0 : 255;
                set(img, x, y, v, v, v);
            }
            return img;
        },
        /* Gaussian-ish additive noise - the kind a blur is actually good at. */
        noisy: function () {
            var img = SOURCES.shapes(), r = rng(11), x, y, i;
            for (y = 0; y < H; y++)
                for (x = 0; x < W; x++) {
                    i = (y * W + x) * 4;
                    var n = (r() + r() + r() - 1.5) * 60;
                    img.d[i] += n; img.d[i + 1] += n; img.d[i + 2] += n;
                }
            return img;
        },
        /* Everything squeezed into the middle of the range, so the histogram
         * is a narrow spike and equalisation has something to do. */
        lowcontrast: function () {
            var img = SOURCES.shapes(), i;
            for (i = 0; i < img.d.length; i += 4) {
                img.d[i] = 96 + img.d[i] * 0.24;
                img.d[i + 1] = 96 + img.d[i + 1] * 0.24;
                img.d[i + 2] = 96 + img.d[i + 2] * 0.24;
            }
            return img;
        },
        /* Saturated colour, for the RGB/HSV module. */
        colour: function () {
            var img = blank(), x, y;
            for (y = 0; y < H; y++)
                for (x = 0; x < W; x++) {
                    var t = x / W;
                    set(img, x, y,
                        Math.round(30 + 200 * t),
                        Math.round(70 + 90 * (y / H)),
                        Math.round(210 - 160 * t));
                }
            disc(img, 52, 50, 24, [220, 40, 40]);
            disc(img, 100, 84, 24, [40, 190, 90]);
            disc(img, 148, 46, 22, [250, 210, 40]);
            return img;
        },
        /* A small, blocky pattern - the one case where the interpolation
         * choice is unmistakable once it is scaled up. */
        blocks: function () {
            var img = blank(), x, y;
            for (y = 0; y < H; y++)
                for (x = 0; x < W; x++) {
                    var v = ((x >> 4) + (y >> 4)) % 2 ? 210 : 45;
                    set(img, x, y, v, v, v);
                }
            disc(img, 96, 72, 30, [250, 160, 40]);
            return img;
        }
    };

    // ------------------------------------------------------------ operations

    function grey(img, i) {
        return 0.299 * img.d[i] + 0.587 * img.d[i + 1] + 0.114 * img.d[i + 2];
    }

    function toGrey(img) {
        var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) }, i, v;
        for (i = 0; i < img.d.length; i += 4) {
            v = grey(img, i);
            out.d[i] = out.d[i + 1] = out.d[i + 2] = v;
            out.d[i + 3] = 255;
        }
        return out;
    }

    var KERNELS = {
        identity: [0, 0, 0, 0, 1, 0, 0, 0, 0],
        blur: [1, 1, 1, 1, 1, 1, 1, 1, 1],
        gaussian: [1, 2, 1, 2, 4, 2, 1, 2, 1],
        sharpen: [0, -1, 0, -1, 5, -1, 0, -1, 0],
        emboss: [-2, -1, 0, -1, 1, 1, 0, 1, 2],
        sobelx: [-1, 0, 1, -2, 0, 2, -1, 0, 1],
        sobely: [-1, -2, -1, 0, 0, 0, 1, 2, 1],
        laplacian: [0, 1, 0, 1, -4, 1, 0, 1, 0],
        outline: [-1, -1, -1, -1, 8, -1, -1, -1, -1]
    };

    function convolve(img, k, normalise) {
        var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) };
        var sum = 0, i;
        for (i = 0; i < 9; i++) sum += k[i];
        var div = (normalise && sum !== 0) ? sum : 1;
        var bias = (sum === 0 && normalise) ? 128 : 0;
        for (var y = 0; y < img.h; y++) {
            for (var x = 0; x < img.w; x++) {
                var acc = 0, n = 0;
                for (var dy = -1; dy <= 1; dy++)
                    for (var dx = -1; dx <= 1; dx++, n++)
                        acc += grey(img, get(img, x + dx, y + dy)) * k[n];
                var v = acc / div + bias;
                var o = (y * img.w + x) * 4;
                out.d[o] = out.d[o + 1] = out.d[o + 2] = v;
                out.d[o + 3] = 255;
            }
        }
        return out;
    }

    function histogram(img) {
        var h = new Uint32Array(256), i;
        for (i = 0; i < img.d.length; i += 4) h[Math.round(grey(img, i))]++;
        return h;
    }

    var OPS = {
        kernel: function (img, p) {
            var k = p.matrix || KERNELS[p.preset] || KERNELS.identity;
            return { image: convolve(img, k, p.normalise !== false),
                     readout: "kernel sum " + k.reduce(function (a, b) { return a + b; }, 0) };
        },

        threshold: function (img, p) {
            var g = toGrey(img), out = { w: g.w, h: g.h, d: new Uint8ClampedArray(g.d.length) };
            var t = p.threshold, on = 0, i, v;
            if (p.method === "otsu") t = otsu(histogram(img), img.w * img.h);
            for (i = 0; i < g.d.length; i += 4) {
                v = g.d[i] >= t ? 255 : 0;
                if (v) on++;
                out.d[i] = out.d[i + 1] = out.d[i + 2] = v;
                out.d[i + 3] = 255;
            }
            return { image: out,
                     readout: "threshold " + Math.round(t) + " - " +
                              Math.round(100 * on / (img.w * img.h)) + "% foreground" };
        },

        equalise: function (img, p) {
            var g = toGrey(img);
            if (!p.on) return { image: g, readout: "original, not equalised" };
            var h = histogram(g), total = g.w * g.h, cdf = new Float64Array(256);
            var run = 0, i;
            for (i = 0; i < 256; i++) { run += h[i]; cdf[i] = run / total; }
            var out = { w: g.w, h: g.h, d: new Uint8ClampedArray(g.d.length) };
            for (i = 0; i < g.d.length; i += 4) {
                var v = Math.round(cdf[g.d[i]] * 255);
                out.d[i] = out.d[i + 1] = out.d[i + 2] = v;
                out.d[i + 3] = 255;
            }
            return { image: out, readout: "equalised - the flat regions separate" };
        },

        smooth: function (img, p) {
            var r = p.radius || 1;
            if (p.method === "median") return { image: median(img, r), readout: "median, radius " + r };
            if (p.method === "bilateral") return { image: bilateral(img, r, p.sigma || 30),
                                                   readout: "bilateral, edge sigma " + (p.sigma || 30) };
            return { image: gaussian(img, r), readout: "gaussian, radius " + r };
        },

        morphology: function (img, p) {
            var g = toGrey(img), t = OPS.threshold(g, { threshold: p.threshold || 128 }).image;
            var r = p.radius || 1, out = t, label = p.method;
            if (p.method === "erode") out = rank(t, r, 0);
            else if (p.method === "dilate") out = rank(t, r, 1);
            else if (p.method === "open") out = rank(rank(t, r, 0), r, 1);
            else if (p.method === "close") out = rank(rank(t, r, 1), r, 0);
            return { image: out, readout: label + ", structuring element " +
                                          (2 * r + 1) + "x" + (2 * r + 1) };
        },

        channel: function (img, p) {
            var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) }, i;
            for (i = 0; i < img.d.length; i += 4) {
                var hsv = rgb2hsv(img.d[i], img.d[i + 1], img.d[i + 2]);
                var v = 0;
                if (p.channel === "r") v = img.d[i];
                else if (p.channel === "g") v = img.d[i + 1];
                else if (p.channel === "b") v = img.d[i + 2];
                else if (p.channel === "h") v = hsv[0] / 360 * 255;
                else if (p.channel === "s") v = hsv[1] * 255;
                else v = hsv[2] * 255;
                out.d[i] = out.d[i + 1] = out.d[i + 2] = v;
                out.d[i + 3] = 255;
            }
            return { image: out, readout: "showing the " + p.channel.toUpperCase() + " channel alone" };
        },

        resample: function (img, p) {
            var f = p.factor || 4;
            var small = box(img, Math.max(2, Math.round(img.w / f)), Math.max(2, Math.round(img.h / f)));
            var up = p.method === "nearest" ? nearest(small, img.w, img.h)
                                            : bilinear(small, img.w, img.h);
            return { image: up,
                     readout: small.w + "x" + small.h + " upscaled to " + img.w + "x" + img.h +
                              " by " + p.method };
        },

        affine: function (img, p) {
            var m = [p.a, p.b, p.c, p.d, p.e, p.f];
            var det = m[0] * m[3] - m[1] * m[2];
            if (Math.abs(det) < 1e-6) return { image: img, readout: "determinant 0 - not invertible" };
            var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) };
            var cx = img.w / 2, cy = img.h / 2;
            for (var y = 0; y < img.h; y++) {
                for (var x = 0; x < img.w; x++) {
                    var px = x - cx - m[4], py = y - cy - m[5];
                    var sx = (m[3] * px - m[2] * py) / det + cx;
                    var sy = (-m[1] * px + m[0] * py) / det + cy;
                    var o = (y * img.w + x) * 4;
                    if (sx < 0 || sy < 0 || sx >= img.w || sy >= img.h) {
                        out.d[o] = out.d[o + 1] = out.d[o + 2] = 18; out.d[o + 3] = 255;
                    } else {
                        var s = get(img, Math.round(sx), Math.round(sy));
                        out.d[o] = img.d[s]; out.d[o + 1] = img.d[s + 1];
                        out.d[o + 2] = img.d[s + 2]; out.d[o + 3] = 255;
                    }
                }
            }
            return { image: out, readout: "determinant " + det.toFixed(2) +
                                          " - area scales by that factor" };
        }
    };

    // --------------------------------------------------------------- helpers

    function otsu(h, total) {
        var sum = 0, i;
        for (i = 0; i < 256; i++) sum += i * h[i];
        var sumB = 0, wB = 0, best = 0, bestT = 128;
        for (i = 0; i < 256; i++) {
            wB += h[i];
            if (!wB) continue;
            var wF = total - wB;
            if (!wF) break;
            sumB += i * h[i];
            var mB = sumB / wB, mF = (sum - sumB) / wF;
            var between = wB * wF * (mB - mF) * (mB - mF);
            if (between > best) { best = between; bestT = i; }
        }
        return bestT;
    }

    function gaussian(img, r) {
        var size = 2 * r + 1, k = [], i, j, s = r / 2 || 0.5, sum = 0;
        for (j = -r; j <= r; j++)
            for (i = -r; i <= r; i++) {
                var v = Math.exp(-(i * i + j * j) / (2 * s * s));
                k.push(v); sum += v;
            }
        var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) };
        for (var y = 0; y < img.h; y++)
            for (var x = 0; x < img.w; x++) {
                var acc = [0, 0, 0], n = 0;
                for (j = -r; j <= r; j++)
                    for (i = -r; i <= r; i++, n++) {
                        var p = get(img, x + i, y + j);
                        acc[0] += img.d[p] * k[n];
                        acc[1] += img.d[p + 1] * k[n];
                        acc[2] += img.d[p + 2] * k[n];
                    }
                var o = (y * img.w + x) * 4;
                out.d[o] = acc[0] / sum; out.d[o + 1] = acc[1] / sum;
                out.d[o + 2] = acc[2] / sum; out.d[o + 3] = 255;
            }
        return out;
    }

    function median(img, r) {
        var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) };
        var buf = [];
        for (var y = 0; y < img.h; y++)
            for (var x = 0; x < img.w; x++) {
                buf.length = 0;
                for (var j = -r; j <= r; j++)
                    for (var i = -r; i <= r; i++) buf.push(grey(img, get(img, x + i, y + j)));
                buf.sort(function (a, b) { return a - b; });
                var v = buf[buf.length >> 1], o = (y * img.w + x) * 4;
                out.d[o] = out.d[o + 1] = out.d[o + 2] = v;
                out.d[o + 3] = 255;
            }
        return out;
    }

    function bilateral(img, r, sigma) {
        var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) };
        var ss = r / 2 || 0.5;
        for (var y = 0; y < img.h; y++)
            for (var x = 0; x < img.w; x++) {
                var centre = grey(img, get(img, x, y)), acc = 0, wsum = 0;
                for (var j = -r; j <= r; j++)
                    for (var i = -r; i <= r; i++) {
                        var v = grey(img, get(img, x + i, y + j));
                        var wS = Math.exp(-(i * i + j * j) / (2 * ss * ss));
                        var wR = Math.exp(-((v - centre) * (v - centre)) / (2 * sigma * sigma));
                        acc += v * wS * wR; wsum += wS * wR;
                    }
                var o = (y * img.w + x) * 4;
                out.d[o] = out.d[o + 1] = out.d[o + 2] = acc / wsum;
                out.d[o + 3] = 255;
            }
        return out;
    }

    /* rank 0 = minimum (erosion), rank 1 = maximum (dilation). On a binary
     * image those are exactly erode and dilate, which is the cleanest way to
     * say what a structuring element does. */
    function rank(img, r, max) {
        var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) };
        for (var y = 0; y < img.h; y++)
            for (var x = 0; x < img.w; x++) {
                var best = max ? 0 : 255;
                for (var j = -r; j <= r; j++)
                    for (var i = -r; i <= r; i++) {
                        var v = img.d[get(img, x + i, y + j)];
                        best = max ? Math.max(best, v) : Math.min(best, v);
                    }
                var o = (y * img.w + x) * 4;
                out.d[o] = out.d[o + 1] = out.d[o + 2] = best;
                out.d[o + 3] = 255;
            }
        return out;
    }

    function box(img, w, h) {
        var out = { w: w, h: h, d: new Uint8ClampedArray(w * h * 4) };
        var fx = img.w / w, fy = img.h / h;
        for (var y = 0; y < h; y++)
            for (var x = 0; x < w; x++) {
                var acc = [0, 0, 0], n = 0;
                for (var j = 0; j < fy; j++)
                    for (var i = 0; i < fx; i++, n++) {
                        var p = get(img, Math.floor(x * fx + i), Math.floor(y * fy + j));
                        acc[0] += img.d[p]; acc[1] += img.d[p + 1]; acc[2] += img.d[p + 2];
                    }
                var o = (y * w + x) * 4;
                out.d[o] = acc[0] / n; out.d[o + 1] = acc[1] / n;
                out.d[o + 2] = acc[2] / n; out.d[o + 3] = 255;
            }
        return out;
    }

    function nearest(img, w, h) {
        var out = { w: w, h: h, d: new Uint8ClampedArray(w * h * 4) };
        for (var y = 0; y < h; y++)
            for (var x = 0; x < w; x++) {
                var p = get(img, Math.floor(x * img.w / w), Math.floor(y * img.h / h));
                var o = (y * w + x) * 4;
                out.d[o] = img.d[p]; out.d[o + 1] = img.d[p + 1];
                out.d[o + 2] = img.d[p + 2]; out.d[o + 3] = 255;
            }
        return out;
    }

    function bilinear(img, w, h) {
        var out = { w: w, h: h, d: new Uint8ClampedArray(w * h * 4) };
        for (var y = 0; y < h; y++)
            for (var x = 0; x < w; x++) {
                var gx = (x + 0.5) * img.w / w - 0.5, gy = (y + 0.5) * img.h / h - 0.5;
                var x0 = Math.floor(gx), y0 = Math.floor(gy);
                var tx = gx - x0, ty = gy - y0, o = (y * w + x) * 4;
                for (var c = 0; c < 3; c++) {
                    var a = img.d[get(img, x0, y0) + c], b = img.d[get(img, x0 + 1, y0) + c];
                    var d = img.d[get(img, x0, y0 + 1) + c], e = img.d[get(img, x0 + 1, y0 + 1) + c];
                    out.d[o + c] = (a * (1 - tx) + b * tx) * (1 - ty) +
                                   (d * (1 - tx) + e * tx) * ty;
                }
                out.d[o + 3] = 255;
            }
        return out;
    }

    function rgb2hsv(r, g, b) {
        r /= 255; g /= 255; b /= 255;
        var mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn, h = 0;
        if (d) {
            if (mx === r) h = 60 * (((g - b) / d) % 6);
            else if (mx === g) h = 60 * ((b - r) / d + 2);
            else h = 60 * ((r - g) / d + 4);
        }
        if (h < 0) h += 360;
        return [h, mx ? d / mx : 0, mx];
    }

    // ------------------------------------------------------------------ view

    function paint(canvas, img) {
        canvas.width = img.w; canvas.height = img.h;
        var ctx = canvas.getContext("2d");
        var id = ctx.createImageData(img.w, img.h);
        id.data.set(img.d);
        ctx.putImageData(id, 0, 0);
    }

    function drawHistogram(canvas, img) {
        var h = histogram(img), max = 0, i;
        for (i = 0; i < 256; i++) if (h[i] > max) max = h[i];
        canvas.width = 256; canvas.height = 64;
        var ctx = canvas.getContext("2d");
        var css = getComputedStyle(document.body);
        ctx.fillStyle = css.getPropertyValue("--bg-surface") || "#242728";
        ctx.fillRect(0, 0, 256, 64);
        ctx.fillStyle = css.getPropertyValue("--accent-primary") || "#eaa94a";
        for (i = 0; i < 256; i++) {
            var bar = max ? Math.round(62 * h[i] / max) : 0;
            ctx.fillRect(i, 64 - bar, 1, bar);
        }
    }

    function control(spec, onChange) {
        var wrap = document.createElement("label");
        wrap.className = "cv-control";
        var name = document.createElement("span");
        name.className = "cv-control-name";
        name.textContent = spec.label;
        var value = document.createElement("span");
        value.className = "cv-control-value";
        wrap.appendChild(name);
        wrap.appendChild(value);

        var input;
        if (spec.type === "select") {
            input = document.createElement("select");
            spec.options.forEach(function (o) {
                var op = document.createElement("option");
                op.value = o.value; op.textContent = o.label;
                input.appendChild(op);
            });
            input.value = spec.value;
            value.textContent = "";
        } else if (spec.type === "toggle") {
            input = document.createElement("input");
            input.type = "checkbox";
            input.checked = !!spec.value;
        } else {
            input = document.createElement("input");
            input.type = "range";
            input.min = spec.min; input.max = spec.max;
            input.step = spec.step || 1; input.value = spec.value;
            value.textContent = spec.value;
        }
        input.className = "cv-input";
        wrap.appendChild(input);

        function read() {
            if (spec.type === "toggle") return input.checked;
            if (spec.type === "select") return input.value;
            value.textContent = input.value;
            return parseFloat(input.value);
        }
        input.addEventListener("input", function () { onChange(spec.key, read()); });
        input.addEventListener("change", function () { onChange(spec.key, read()); });
        return { el: wrap, read: read };
    }

    function mount(root) {
        var cfgEl = root.querySelector(".cv-config");
        if (!cfgEl) return;
        var cfg;
        try { cfg = JSON.parse(cfgEl.textContent); } catch (e) { return; }

        var op = OPS[cfg.op];
        var makeSource = SOURCES[cfg.source] || SOURCES.shapes;
        if (!op) return;

        var srcImg = makeSource();
        var params = {};
        (cfg.controls || []).forEach(function (c) { params[c.key] = c.value; });
        Object.keys(cfg.fixed || {}).forEach(function (k) { params[k] = cfg.fixed[k]; });

        root.innerHTML = "";

        var stage = document.createElement("div");
        stage.className = "cv-stage";
        var before = document.createElement("figure");
        before.className = "cv-pane";
        var beforeCanvas = document.createElement("canvas");
        beforeCanvas.className = "cv-canvas";
        var beforeCap = document.createElement("figcaption");
        beforeCap.textContent = "Input";
        before.appendChild(beforeCanvas); before.appendChild(beforeCap);

        var after = document.createElement("figure");
        after.className = "cv-pane";
        var afterCanvas = document.createElement("canvas");
        afterCanvas.className = "cv-canvas";
        var afterCap = document.createElement("figcaption");
        afterCap.textContent = "Output";
        after.appendChild(afterCanvas); after.appendChild(afterCap);

        stage.appendChild(before); stage.appendChild(after);
        root.appendChild(stage);

        var hist = null;
        if (cfg.histogram) {
            var hwrap = document.createElement("div");
            hwrap.className = "cv-hist-row";
            hist = [document.createElement("canvas"), document.createElement("canvas")];
            hist.forEach(function (c, i) {
                var f = document.createElement("figure");
                f.className = "cv-hist";
                c.className = "cv-hist-canvas";
                var cap = document.createElement("figcaption");
                cap.textContent = i ? "Output histogram" : "Input histogram";
                f.appendChild(c); f.appendChild(cap);
                hwrap.appendChild(f);
            });
            root.appendChild(hwrap);
        }

        var readout = document.createElement("p");
        readout.className = "cv-readout";
        readout.setAttribute("aria-live", "polite");

        var panel = document.createElement("div");
        panel.className = "cv-controls";
        (cfg.controls || []).forEach(function (spec) {
            var c = control(spec, function (key, val) {
                params[key] = val;
                schedule();
            });
            panel.appendChild(c.el);
        });
        root.appendChild(panel);
        root.appendChild(readout);

        var queued = false;
        function schedule() {
            if (queued) return;
            queued = true;
            requestAnimationFrame(function () { queued = false; render(); });
        }

        function render() {
            var res = op(srcImg, params);
            paint(beforeCanvas, srcImg);
            paint(afterCanvas, res.image);
            if (hist) { drawHistogram(hist[0], srcImg); drawHistogram(hist[1], res.image); }
            readout.textContent = res.readout || "";
        }

        render();
        root.dataset.vzCvReady = "1";
    }

    function init() {
        Array.prototype.forEach.call(
            document.querySelectorAll("[data-vz-cv]"), mount);
    }

    if (document.readyState === "loading")
        document.addEventListener("DOMContentLoaded", init);
    else init();
})();
