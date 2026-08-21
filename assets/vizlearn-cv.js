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
        },

        /* Template matching: normalised cross-correlation of a patch cut from
         * the image against every position in it. The response map is the
         * output, and its brightest point is where the patch was found. */
        template: function (img, p) {
            var g = toGrey(img);
            var ts = p.size | 0;
            /* Keep the patch wholly inside the image. get() clamps at the
             * border, so a template hanging off the edge is mostly repeated
             * pixels - which correlates perfectly with every other flat region
             * and makes the reported match meaningless. */
            var tx = Math.max(0, Math.min(g.w - ts, p.tx | 0));
            var ty = Math.max(0, Math.min(g.h - ts, p.ty | 0));
            var tpl = [], i, j, tSum = 0, tN = ts * ts;
            for (j = 0; j < ts; j++)
                for (i = 0; i < ts; i++) {
                    var v = g.d[get(g, tx + i, ty + j)];
                    tpl.push(v); tSum += v;
                }
            var tMean = tSum / tN, tVar = 0;
            for (i = 0; i < tN; i++) tVar += (tpl[i] - tMean) * (tpl[i] - tMean);
            tVar = Math.sqrt(tVar);
            /* A template cut from a flat region has no pattern, so normalised
             * correlation is 0/0 and every position ties. Saying so is more
             * use than reporting a match at (0, 0) with correlation zero -
             * it is a real limitation of the method, not a glitch. */
            if (tVar < 1e-6) {
                var flat = { w: g.w, h: g.h, d: new Uint8ClampedArray(g.d.length) };
                for (i = 0; i < flat.d.length; i += 4) {
                    flat.d[i] = flat.d[i + 1] = flat.d[i + 2] = 128;
                    flat.d[i + 3] = 255;
                }
                frame(flat, tx, ty, ts, [255, 190, 60]);
                return { image: flat,
                         readout: "the template is a flat patch - no pattern to " +
                                  "correlate, so every position ties. Move it onto " +
                                  "an edge or a corner." };
            }

            var out = { w: g.w, h: g.h, d: new Uint8ClampedArray(g.d.length) };
            var bx = 0, by = 0, best = -2;
            // Only positions where the window is wholly inside the image.
            for (var y = 0; y <= g.h - ts; y++)
                for (var x = 0; x <= g.w - ts; x++) {
                    var wSum = 0, n = 0;
                    for (j = 0; j < ts; j++)
                        for (i = 0; i < ts; i++) wSum += g.d[get(g, x + i, y + j)];
                    var wMean = wSum / tN, sum = 0, wVar = 0;
                    n = 0;
                    for (j = 0; j < ts; j++)
                        for (i = 0; i < ts; i++, n++) {
                            var wv = g.d[get(g, x + i, y + j)] - wMean;
                            sum += (tpl[n] - tMean) * wv;
                            wVar += wv * wv;
                        }
                    var ncc = sum / (tVar * (Math.sqrt(wVar) || 1));
                    if (ncc > best) { best = ncc; bx = x; by = y; }
                    var o = (y * g.w + x) * 4;
                    var shade = (ncc + 1) / 2 * 255;
                    out.d[o] = out.d[o + 1] = out.d[o + 2] = shade;
                    out.d[o + 3] = 255;
                }
            frame(out, tx, ty, ts, [110, 110, 110]);
            frame(out, bx, by, ts, [255, 190, 60]);
            return { image: out,
                     readout: "best match at (" + bx + ", " + by + "), correlation " +
                              best.toFixed(3) + " - template cut from (" + tx +
                              ", " + ty + ")" };
        },

        /* Harris corner response. The structure tensor over a window says
         * whether the gradient has one dominant direction (an edge) or two
         * (a corner), and R combines its eigenvalues without computing them. */
        harris: function (img, p) {
            var g = toGrey(img), w = g.w, h = g.h;
            var Ix = new Float32Array(w * h), Iy = new Float32Array(w * h);
            var x, y, i;
            for (y = 0; y < h; y++)
                for (x = 0; x < w; x++) {
                    i = y * w + x;
                    Ix[i] = (g.d[get(g, x + 1, y)] - g.d[get(g, x - 1, y)]) / 2;
                    Iy[i] = (g.d[get(g, x, y + 1)] - g.d[get(g, x, y - 1)]) / 2;
                }
            var r = p.window | 0, k = p.k;
            var out = { w: w, h: h, d: new Uint8ClampedArray(g.d.length) };
            var resp = new Float32Array(w * h), maxR = 1e-6;
            for (y = 0; y < h; y++)
                for (x = 0; x < w; x++) {
                    var a = 0, b = 0, c = 0;
                    for (var dy = -r; dy <= r; dy++)
                        for (var dx = -r; dx <= r; dx++) {
                            var xx = Math.min(w - 1, Math.max(0, x + dx));
                            var yy = Math.min(h - 1, Math.max(0, y + dy));
                            var jj = yy * w + xx;
                            a += Ix[jj] * Ix[jj]; b += Ix[jj] * Iy[jj]; c += Iy[jj] * Iy[jj];
                        }
                    var det = a * c - b * b, tr = a + c;
                    var R = det - k * tr * tr;
                    resp[y * w + x] = R;
                    if (R > maxR) maxR = R;
                }
            var corners = 0;
            for (y = 0; y < h; y++)
                for (x = 0; x < w; x++) {
                    i = y * w + x;
                    var o = i * 4;
                    var base = g.d[o] * 0.45;
                    var hit = resp[i] > maxR * p.threshold;
                    if (hit) corners++;
                    out.d[o] = hit ? 255 : base;
                    out.d[o + 1] = hit ? 185 : base;
                    out.d[o + 2] = hit ? 55 : base;
                    out.d[o + 3] = 255;
                }
            return { image: out,
                     readout: corners + " pixels above threshold - window " +
                              (2 * r + 1) + "x" + (2 * r + 1) + ", k = " + k.toFixed(2) };
        },

        /* Vision Transformer patching: cut the image into a grid, which is the
         * whole of what a ViT does to an image before it is a sequence. */
        patches: function (img, p) {
            var n = p.patch | 0;
            var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) };
            out.d.set(img.d);
            var x, y;
            for (y = 0; y < img.h; y++)
                for (x = 0; x < img.w; x++)
                    if (x % n === 0 || y % n === 0) set(out, x, y, 24, 24, 24);
            var across = Math.ceil(img.w / n), down = Math.ceil(img.h / n);
            return { image: out,
                     readout: n + "x" + n + " patches - " + across + "x" + down + " = " +
                              (across * down) + " tokens, each a vector of " +
                              (n * n * 3) + " numbers before projection" };
        },

        /* The three segmentation tasks over one known scene. Nothing is
         * predicted: the regions are given, and the point is what each task is
         * asked to say about them. */
        segmentation: function (img, p) {
            var out = { w: img.w, h: img.h, d: new Uint8ClampedArray(img.d.length) };
            var THING = [[236, 152, 47], [120, 190, 235], [150, 220, 150]];
            var STUFF = [70, 78, 84];
            var discs = [{ cx: 58, cy: 62, r: 26 }, { cx: 130, cy: 96, r: 22 }];
            var x, y, i, k;
            for (y = 0; y < img.h; y++)
                for (x = 0; x < img.w; x++) {
                    var cls = null, inst = -1;
                    if (x >= 104 && x < 150 && y >= 34 && y < 74) { cls = 1; inst = 2; }
                    for (k = 0; k < discs.length; k++) {
                        var dx = x - discs[k].cx, dy = y - discs[k].cy;
                        if (dx * dx + dy * dy <= discs[k].r * discs[k].r) { cls = 0; inst = k; }
                    }
                    var c;
                    if (cls === null) c = (p.task === "instance") ? [26, 28, 30] : STUFF;
                    else if (p.task === "semantic") c = THING[cls === 1 ? 1 : 0];
                    else c = THING[inst % THING.length];
                    i = (y * img.w + x) * 4;
                    out.d[i] = c[0]; out.d[i + 1] = c[1]; out.d[i + 2] = c[2];
                    out.d[i + 3] = 255;
                }
            var says = {
                semantic: "every pixel gets a class, and the two discs share one - " +
                          "they are a single region",
                instance: "each object gets its own id, and the background is not " +
                          "labelled at all",
                panoptic: "every pixel gets a class and the two discs keep separate " +
                          "ids - both at once"
            };
            return { image: out, readout: p.task + ": " + says[p.task] };
        }
    };

    // --------------------------------------------------------------- helpers

    /* A one-pixel border, used to mark where a template came from and where it
     * was found. Drawn into the response map rather than the source, because
     * the response map is what the reader is being asked to read. */
    function frame(img, x0, y0, size, col) {
        for (var i = 0; i < size; i++) {
            set(img, x0 + i, y0, col[0], col[1], col[2]);
            set(img, x0 + i, y0 + size - 1, col[0], col[1], col[2]);
            set(img, x0, y0 + i, col[0], col[1], col[2]);
            set(img, x0 + size - 1, y0 + i, col[0], col[1], col[2]);
        }
    }

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

    // -------------------------------------------------------------- diagrams

    /* Two of the Tier 1 modules are about what a convolution does to shape and
     * to channels rather than to pixels, so there is no image to show. They
     * get an SVG diagram driven by the same controls and readout as everything
     * else, which keeps one mental model for the whole track. */

    var SVGNS = "http://www.w3.org/2000/svg";

    function el(name, attrs) {
        var n = document.createElementNS(SVGNS, name);
        Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
        return n;
    }

    function svgRoot(w, h) {
        var s = el("svg", { viewBox: "0 0 " + w + " " + h, class: "cv-diagram" });
        s.setAttribute("role", "img");
        return s;
    }

    var DIAGRAMS = {
        /* One output pixel, traced back through however many layers, to the
         * patch of the input it can actually see. The point the diagram has to
         * make is that the growth is additive per layer and multiplicative in
         * stride, which a formula states and a picture shows. */
        receptive: function (p) {
            var layers = p.layers, k = p.kernel, stride = p.stride;
            var W = 620, rowH = 96, H = rowH * (layers + 1) + 34;
            var svg = svgRoot(W, H);

            // Receptive field size, layer by layer, and the jump between
            // adjacent output positions.
            var sizes = [1], jump = 1, r = 1, i;
            for (i = 0; i < layers; i++) {
                r = r + (k - 1) * jump;
                jump = jump * stride;
                sizes.push(r);
            }

            var cells = 25, cell = 22, x0 = 26;
            for (i = layers; i >= 0; i--) {
                var y = 20 + (layers - i) * rowH;
                /* sizes is indexed by distance from the output, so the row
                 * for the output itself is sizes[0] = 1 and the input row is
                 * sizes[layers] = the full receptive field. Indexing by the
                 * layer number instead put the wide band at the top and the
                 * single cell at the bottom, which is the diagram upside
                 * down. */
                var size = sizes[layers - i];
                var lo = Math.round((cells - size) / 2), hi = lo + size - 1;
                var g = el("g", {});
                for (var c = 0; c < cells; c++) {
                    var lit = c >= lo && c <= hi;
                    g.appendChild(el("rect", {
                        x: x0 + c * cell, y: y, width: cell - 2, height: cell - 2, rx: 2,
                        fill: lit ? "var(--accent-fill)" : "var(--bg-surface)",
                        stroke: "var(--border-subtle)", "stroke-width": 1,
                        "fill-opacity": lit ? (i === layers ? 1 : 0.55) : 1
                    }));
                }
                var label = i === 0 ? "input"
                          : (i === layers ? "output" : "layer " + i);
                var t = el("text", {
                    x: x0, y: y - 5, fill: "var(--text-muted)",
                    "font-size": 11, "font-family": "var(--vz-mono)"
                });
                t.textContent = label + "  -  " + size + " position" +
                                (size === 1 ? "" : "s") + " wide";
                g.appendChild(t);
                svg.appendChild(g);
            }
            return {
                svg: svg,
                readout: layers + " layers of " + k + "x" + k + " at stride " +
                         stride + " - receptive field " + r + "x" + r
            };
        },

        /* A 1x1 convolution has no spatial extent, so every interesting thing
         * about it is in the channel dimension. The diagram is the channel
         * mixing matrix, and the readout is the parameter count against the
         * 3x3 that people reach for instead. */
        channels: function (p) {
            var cin = p.cin, cout = p.cout;
            var W = 620, H = 300, svg = svgRoot(W, H);
            var box = 26, gap = 6;
            var leftX = 40, rightX = W - 40 - box;
            var lh = cin * (box + gap) - gap, rh = cout * (box + gap) - gap;
            var ly = (H - lh) / 2, ry = (H - rh) / 2, i, j;

            for (i = 0; i < cin; i++)
                for (j = 0; j < cout; j++)
                    svg.appendChild(el("line", {
                        x1: leftX + box, y1: ly + i * (box + gap) + box / 2,
                        x2: rightX, y2: ry + j * (box + gap) + box / 2,
                        stroke: "var(--accent-primary)", "stroke-width": 0.6,
                        "stroke-opacity": 0.35
                    }));

            for (i = 0; i < cin; i++)
                svg.appendChild(el("rect", {
                    x: leftX, y: ly + i * (box + gap), width: box, height: box, rx: 3,
                    fill: "var(--bg-surface)", stroke: "var(--border-subtle)",
                    "stroke-width": 1
                }));
            for (j = 0; j < cout; j++)
                svg.appendChild(el("rect", {
                    x: rightX, y: ry + j * (box + gap), width: box, height: box, rx: 3,
                    fill: "var(--accent-fill)", "fill-opacity": 0.5,
                    stroke: "var(--border-subtle)", "stroke-width": 1
                }));

            [[leftX + box / 2, cin + " input channels"],
             [rightX + box / 2, cout + " output channels"]].forEach(function (pair) {
                var t = el("text", {
                    x: pair[0], y: H - 8, fill: "var(--text-muted)",
                    "font-size": 11, "font-family": "var(--vz-mono)",
                    "text-anchor": "middle"
                });
                t.textContent = pair[1];
                svg.appendChild(t);
            });

            var one = cin * cout, three = cin * cout * 9;
            return {
                svg: svg,
                readout: one + " weights as 1x1, " + three + " as 3x3 - " +
                         "a factor of 9, and no spatial mixing either way"
            };
        },

        /* Depthwise separable convolution against the full one, counted. The
         * saving is the whole argument for MobileNet, and it is arithmetic. */
        separable: function (p) {
            var cin = p.cin, cout = p.cout, k = p.kernel;
            var full = k * k * cin * cout;
            var depth = k * k * cin, point = cin * cout;
            var sep = depth + point;
            var W = 620, H = 250, svg = svgRoot(W, H);
            var bar = function (x, label, value, max, colour) {
                var wpx = Math.max(2, (W - 200) * value / max);
                svg.appendChild(el("rect", { x: 170, y: x, width: wpx, height: 34, rx: 4,
                                             fill: colour, "fill-opacity": 0.55,
                                             stroke: "var(--border-subtle)", "stroke-width": 1 }));
                var t = el("text", { x: 160, y: x + 22, fill: "var(--text-muted)",
                                     "font-size": 12, "font-family": "var(--vz-mono)",
                                     "text-anchor": "end" });
                t.textContent = label;
                svg.appendChild(t);
                var n = el("text", { x: 178 + wpx, y: x + 22, fill: "var(--text-main)",
                                     "font-size": 12, "font-family": "var(--vz-mono)" });
                n.textContent = value.toLocaleString();
                svg.appendChild(n);
            };
            bar(30, "full " + k + "x" + k, full, full, "var(--accent-fill)");
            bar(88, "depthwise", depth, full, "var(--accent-primary)");
            bar(146, "pointwise 1x1", point, full, "var(--accent-primary)");
            bar(204, "separable total", sep, full, "var(--accent-fill)");
            return {
                svg: svg,
                readout: full.toLocaleString() + " weights against " + sep.toLocaleString() +
                         " - " + (full / sep).toFixed(1) + "x fewer, for the same input " +
                         "and output shape"
            };
        },

        /* Dilated convolution: the same nine weights, spread out. */
        dilated: function (p) {
            var d = p.dilation, k = 3, layers = p.layers;
            var cells = 33, cell = 17, x0 = 20;
            var W = 620, H = 60 + layers * 78, svg = svgRoot(W, H);
            var r = 1, jump = 1, i;
            // With dilation the effective kernel is k + (k-1)(d-1) wide.
            var eff = k + (k - 1) * (d - 1);
            for (i = 0; i < layers; i++) r = r + (eff - 1);
            var lit = [];
            for (i = 0; i < layers; i++) {
                var y = 34 + i * 78;
                var size = 1 + (eff - 1) * (i + 1);
                var lo = Math.round((cells - size) / 2), hi = lo + size - 1;
                var g = el("g", {});
                for (var c = 0; c < cells; c++) {
                    var inSpan = c >= lo && c <= hi;
                    // Which cells the dilated kernel actually reads at this level.
                    var touched = inSpan && ((c - lo) % d === 0 || i > 0);
                    g.appendChild(el("rect", {
                        x: x0 + c * cell, y: y, width: cell - 2, height: cell - 2, rx: 2,
                        fill: touched ? "var(--accent-fill)" : "var(--bg-surface)",
                        "fill-opacity": touched ? (inSpan ? 0.6 : 1) : 1,
                        stroke: "var(--border-subtle)", "stroke-width": 1
                    }));
                }
                var t = el("text", { x: x0, y: y - 6, fill: "var(--text-muted)",
                                     "font-size": 11, "font-family": "var(--vz-mono)" });
                t.textContent = "after layer " + (i + 1) + " - " + size + " positions wide";
                g.appendChild(t);
                svg.appendChild(g);
                lit.push(size);
            }
            return {
                svg: svg,
                readout: "dilation " + d + ": three weights spanning " + eff +
                         " positions.  " + layers + " layers reach " +
                         lit[lit.length - 1] + " input positions, with " +
                         (9 * layers) + " weights per channel pair"
            };
        },

        /* Global average pooling against flatten, in parameters. */
        gap: function (p) {
            var side = p.side, ch = p.channels, classes = p.classes;
            var flat = side * side * ch * classes;
            var pooled = ch * classes;
            var W = 620, H = 230, svg = svgRoot(W, H);
            var box = function (x, y, w, h, label, sub) {
                svg.appendChild(el("rect", { x: x, y: y, width: w, height: h, rx: 5,
                                             fill: "var(--bg-surface)",
                                             stroke: "var(--border-subtle)", "stroke-width": 1 }));
                var t = el("text", { x: x + w / 2, y: y + h / 2 - 2, fill: "var(--text-main)",
                                     "font-size": 12, "font-family": "var(--vz-mono)",
                                     "text-anchor": "middle" });
                t.textContent = label;
                svg.appendChild(t);
                var u = el("text", { x: x + w / 2, y: y + h / 2 + 16, fill: "var(--text-muted)",
                                     "font-size": 11, "font-family": "var(--vz-mono)",
                                     "text-anchor": "middle" });
                u.textContent = sub;
                svg.appendChild(u);
            };
            box(24, 30, 150, 60, side + "x" + side + "x" + ch, "feature map");
            box(24, 130, 150, 60, side + "x" + side + "x" + ch, "feature map");
            box(240, 30, 150, 60, "flatten", side * side * ch + " values");
            box(240, 130, 150, 60, "global avg pool", ch + " values");
            box(440, 30, 155, 60, "dense -> " + classes, flat.toLocaleString() + " weights");
            box(440, 130, 155, 60, "dense -> " + classes, pooled.toLocaleString() + " weights");
            [[174, 60, 240], [174, 160, 240], [390, 60, 440], [390, 160, 440]].forEach(function (a) {
                svg.appendChild(el("line", { x1: a[0], y1: a[1], x2: a[2], y2: a[1],
                                             stroke: "var(--accent-primary)", "stroke-width": 1.4 }));
            });
            return {
                svg: svg,
                readout: flat.toLocaleString() + " weights against " + pooled.toLocaleString() +
                         " - " + Math.round(flat / pooled) + "x fewer, and the pooled " +
                         "version works at any input size"
            };
        },

        /* Anchor boxes over a grid, with IoU against one ground-truth box. */
        anchors: function (p) {
            var W = 620, H = 320, svg = svgRoot(W, H);
            var sx = 3.2, gx = 30, gy = 20;
            var cellsX = 6, cellsY = 4, cw = 90, ch = 68;
            var gt = { x: 150, y: 90, w: 190, h: 130 };
            var i, j;
            for (j = 0; j < cellsY; j++)
                for (i = 0; i < cellsX; i++)
                    svg.appendChild(el("rect", {
                        x: gx + i * cw, y: gy + j * ch, width: cw, height: ch,
                        fill: "none", stroke: "var(--border-subtle)",
                        "stroke-width": 0.7, "stroke-dasharray": "3 3" }));

            var cx = gx + (p.cell % cellsX) * cw + cw / 2;
            var cy = gy + Math.floor(p.cell / cellsX) * ch + ch / 2;
            var base = p.scale, ratios = [0.5, 1, 2];
            var best = 0, bestR = 1;
            ratios.forEach(function (ar) {
                var w = base * Math.sqrt(1 / ar), h = base * Math.sqrt(ar);
                var bx = cx - w / 2, by = cy - h / 2;
                var ix = Math.max(0, Math.min(bx + w, gt.x + gt.w) - Math.max(bx, gt.x));
                var iy = Math.max(0, Math.min(by + h, gt.y + gt.h) - Math.max(by, gt.y));
                var inter = ix * iy;
                var iou = inter / (w * h + gt.w * gt.h - inter);
                if (iou > best) { best = iou; bestR = ar; }
                svg.appendChild(el("rect", {
                    x: bx, y: by, width: w, height: h, fill: "none",
                    stroke: "var(--accent-primary)", "stroke-width": iou === best ? 2 : 1,
                    "stroke-opacity": 0.35 + iou }));
            });
            svg.appendChild(el("rect", { x: gt.x, y: gt.y, width: gt.w, height: gt.h,
                                         fill: "var(--accent-fill)", "fill-opacity": 0.16,
                                         stroke: "var(--accent-fill)", "stroke-width": 2.2 }));
            svg.appendChild(el("circle", { cx: cx, cy: cy, r: 3.5, fill: "var(--accent-primary)" }));
            var t = el("text", { x: gt.x + 6, y: gt.y - 6, fill: "var(--accent-fill)",
                                 "font-size": 11, "font-family": "var(--vz-mono)" });
            t.textContent = "ground truth";
            svg.appendChild(t);
            var label = best >= 0.5 ? "positive (>= 0.5)"
                      : (best < 0.3 ? "negative (< 0.3)" : "ignored (between)");
            return {
                svg: svg,
                readout: "best IoU " + best.toFixed(2) + " at aspect ratio " +
                         (bestR === 1 ? "1:1" : (bestR < 1 ? "2:1 wide" : "1:2 tall")) +
                         " - this anchor is " + label
            };
        },

        /* Average precision: one PR curve, and the area under it. */
        map: function (p) {
            var W = 620, H = 300, svg = svgRoot(W, H);
            var pad = { l: 54, r: 20, t: 18, b: 40 };
            var px = function (v) { return pad.l + v * (W - pad.l - pad.r); };
            var py = function (v) { return H - pad.b - v * (H - pad.t - pad.b); };
            svg.appendChild(el("path", {
                d: "M" + pad.l + " " + pad.t + " L" + pad.l + " " + (H - pad.b) +
                   " L" + (W - pad.r) + " " + (H - pad.b),
                fill: "none", stroke: "var(--border-subtle)", "stroke-width": 1 }));

            // A detector's ranked list: high-confidence hits first, then a
            // tail that gets steadily worse. The threshold controls how much
            // of the tail is kept.
            var n = 24, hits = [], i;
            for (i = 0; i < n; i++) hits.push(i < 5 ? 1 : (((i * 7) % 5) < 2 ? 1 : 0));
            var total = hits.reduce(function (a, b) { return a + b; }, 0);
            var tp = 0, pts = [], ap = 0, prevR = 0;
            for (i = 0; i < n; i++) {
                if (hits[i]) tp++;
                var prec = tp / (i + 1), rec = tp / total;
                pts.push([rec, prec]);
                ap += (rec - prevR) * prec;
                prevR = rec;
            }
            var d = pts.map(function (q, k) {
                return (k ? "L" : "M") + px(q[0]) + " " + py(q[1]);
            }).join(" ");
            svg.appendChild(el("path", { d: d, fill: "none",
                                         stroke: "var(--accent-primary)", "stroke-width": 2 }));
            pts.forEach(function (q) {
                svg.appendChild(el("circle", { cx: px(q[0]), cy: py(q[1]), r: 2.6,
                                               fill: "var(--accent-fill)" }));
            });
            [["recall", W / 2, H - 10], ["precision", 0, 0]].forEach(function (a, k) {
                var t = el("text", { fill: "var(--text-muted)", "font-size": 11,
                                     "font-family": "var(--vz-mono)", "text-anchor": "middle" });
                t.textContent = a[0];
                if (k === 0) { t.setAttribute("x", a[1]); t.setAttribute("y", a[2]); }
                else { t.setAttribute("transform", "translate(16," + (H / 2) + ") rotate(-90)"); }
                svg.appendChild(t);
            });
            return {
                svg: svg,
                readout: "AP " + ap.toFixed(3) + " over " + total + " ground-truth boxes.  " +
                         "mAP is this, averaged over every class - and at IoU " +
                         p.iou.toFixed(2) + " a different set of detections would count as hits"
            };
        },

        /* Grad-CAM: weight each feature map by how much the score responds to
         * it, sum, keep the positive part. The maps here are synthetic, and
         * the weighting is the real arithmetic. */
        gradcam: function (p) {
            var W = 620, H = 260, svg = svgRoot(W, H);
            var maps = [
                { cx: 0.28, cy: 0.42, label: "map 1" },
                { cx: 0.62, cy: 0.30, label: "map 2" },
                { cx: 0.48, cy: 0.72, label: "map 3" }
            ];
            var w = [p.w1, p.w2, p.w3];
            var cellW = 130, cellH = 92, gx = 24, gy = 26;
            maps.forEach(function (m, i) {
                var x = gx, y = gy + i * (cellH - 10);
                for (var a = 0; a < 13; a++)
                    for (var b = 0; b < 8; b++) {
                        var dx = a / 12 - m.cx, dy = b / 7 - m.cy;
                        var v = Math.exp(-(dx * dx + dy * dy) / 0.05);
                        svg.appendChild(el("rect", {
                            x: x + a * 9, y: y + b * 8, width: 8, height: 7,
                            fill: "var(--accent-fill)", "fill-opacity": (v * 0.85).toFixed(3) }));
                    }
                var t = el("text", { x: x + 130, y: y + 34, fill: "var(--text-muted)",
                                     "font-size": 11, "font-family": "var(--vz-mono)" });
                t.textContent = m.label + "  x  " + w[i].toFixed(1);
                svg.appendChild(t);
            });
            var ox = 330, oy = 46;
            for (var a = 0; a < 26; a++)
                for (var b = 0; b < 17; b++) {
                    var acc = 0;
                    maps.forEach(function (m, i) {
                        var dx = a / 25 - m.cx, dy = b / 16 - m.cy;
                        acc += w[i] * Math.exp(-(dx * dx + dy * dy) / 0.05);
                    });
                    acc = Math.max(0, acc);      // the ReLU in Grad-CAM
                    svg.appendChild(el("rect", {
                        x: ox + a * 10, y: oy + b * 9, width: 9, height: 8,
                        fill: "var(--accent-fill)",
                        "fill-opacity": Math.min(1, acc / 2.2).toFixed(3) }));
                }
            var lbl = el("text", { x: ox, y: oy - 8, fill: "var(--text-muted)",
                                   "font-size": 11, "font-family": "var(--vz-mono)" });
            lbl.textContent = "weighted sum, then ReLU";
            svg.appendChild(lbl);
            var neg = w.filter(function (v) { return v < 0; }).length;
            return {
                svg: svg,
                readout: "weights " + w.map(function (v) { return v.toFixed(1); }).join(", ") +
                         (neg ? "  -  " + neg + " negative, and the ReLU discards what they " +
                                "contribute: Grad-CAM shows evidence for the class, not against it"
                              : "  -  all positive, so every map contributes to the heatmap")
            };
        }
    };

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

    function panelFor(cfg, params, schedule) {
        var panel = document.createElement("div");
        panel.className = "cv-controls";
        (cfg.controls || []).forEach(function (spec) {
            var c = control(spec, function (key, val) {
                params[key] = val;
                schedule();
            });
            panel.appendChild(c.el);
        });
        return panel;
    }

    function mountDiagram(root, cfg, diagram, params) {
        var stage = document.createElement("div");
        stage.className = "cv-diagram-stage";
        root.appendChild(stage);

        var readout = document.createElement("p");
        readout.className = "cv-readout";
        readout.setAttribute("aria-live", "polite");

        var queued = false;
        function schedule() {
            if (queued) return;
            queued = true;
            requestAnimationFrame(function () { queued = false; render(); });
        }
        function render() {
            var res = diagram(params);
            stage.innerHTML = "";
            stage.appendChild(res.svg);
            readout.textContent = res.readout || "";
        }

        root.appendChild(panelFor(cfg, params, schedule));
        root.appendChild(readout);
        render();
        root.dataset.vzCvReady = "1";
    }

    // Exposed for tooling; the page itself never reads it.
    window.VizCVDiagrams = DIAGRAMS;
    window.VizCVOps = OPS;

    function mount(root) {
        var cfgEl = root.querySelector(".cv-config");
        if (!cfgEl) return;
        var cfg;
        try { cfg = JSON.parse(cfgEl.textContent); } catch (e) { return; }

        var diagram = cfg.diagram ? DIAGRAMS[cfg.diagram] : null;
        var op = cfg.op ? OPS[cfg.op] : null;
        var makeSource = SOURCES[cfg.source] || SOURCES.shapes;
        if (!op && !diagram) return;

        var srcImg = makeSource();
        var params = {};
        (cfg.controls || []).forEach(function (c) { params[c.key] = c.value; });
        Object.keys(cfg.fixed || {}).forEach(function (k) { params[k] = cfg.fixed[k]; });

        root.innerHTML = "";

        if (diagram) return mountDiagram(root, cfg, diagram, params);

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
