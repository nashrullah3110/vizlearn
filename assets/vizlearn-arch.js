/* Interactive architecture explorers for the named-model modules.
 *
 * Fifteen modules on this site are about a *named architecture* rather than a
 * single operation: VGG-16, Inception, ResNet-50, U-Net, YOLO, Mask R-CNN,
 * word2vec, GloVe, seq2seq, a GAN, an autoencoder, a recommender. A reader
 * meets those as a block diagram in a paper and a wall of layer names in a
 * framework summary, and neither tells them what actually flows through the
 * thing.
 *
 * So every module here is a playground rather than a picture. The tensor
 * shapes are computed, not typed: change the input resolution and the whole
 * column of shapes and parameter counts recomputes from the same convolution
 * arithmetic the model really uses. Where a model has a decision in it -
 * Inception's 1x1 bottleneck, U-Net's skip connections, NMS's IoU threshold,
 * a bottleneck's width - that decision is a control, and the number it moves
 * is on screen beside it.
 *
 * Nothing is fetched and no model is loaded. Every image is drawn in code and
 * every number is arithmetic done here, which is the point: a reader can read
 * this file against the diagram and find the same formula.
 *
 * Binds to [data-vz-arch]; costs nothing on a page that has none.
 */
(function () {
    "use strict";

    var NS = "http://www.w3.org/2000/svg";

    // ------------------------------------------------------------- elements

    function h(tag, cls, text) {
        var n = document.createElement(tag);
        if (cls) n.className = cls;
        if (text !== undefined && text !== null) n.textContent = text;
        return n;
    }

    function e(tag, attrs) {
        var n = document.createElementNS(NS, tag);
        for (var k in attrs) if (attrs.hasOwnProperty(k)) {
            if (attrs[k] === null || attrs[k] === undefined) continue;
            n.setAttribute(k, attrs[k]);
        }
        return n;
    }

    function svg(w, hgt, cls) {
        var n = e("svg", {
            viewBox: "0 0 " + w + " " + hgt,
            class: "arch-svg" + (cls ? " " + cls : ""),
            preserveAspectRatio: "xMidYMid meet"
        });
        n.setAttribute("aria-hidden", "true");
        return n;
    }

    function text(x, y, str, o) {
        o = o || {};
        var n = e("text", {
            x: x, y: y,
            fill: o.fill || "var(--text-muted)",
            "font-size": o.size || 10,
            "font-family": o.family || "var(--vz-mono)",
            "text-anchor": o.anchor || "middle",
            "font-weight": o.weight || "normal",
            opacity: o.opacity
        });
        n.textContent = str;
        return n;
    }

    function rect(x, y, w, hgt, o) {
        o = o || {};
        return e("rect", {
            x: x, y: y, width: Math.max(0, w), height: Math.max(0, hgt),
            rx: o.rx === undefined ? 3 : o.rx,
            fill: o.fill || "none",
            stroke: o.stroke || "var(--border-subtle)",
            "stroke-width": o.sw === undefined ? 1.4 : o.sw,
            "fill-opacity": o.fo,
            "stroke-dasharray": o.dash,
            opacity: o.opacity
        });
    }

    function line(x1, y1, x2, y2, o) {
        o = o || {};
        return e("line", {
            x1: x1, y1: y1, x2: x2, y2: y2,
            stroke: o.stroke || "var(--border-subtle)",
            "stroke-width": o.sw === undefined ? 1.3 : o.sw,
            "stroke-dasharray": o.dash,
            "stroke-linecap": o.cap,
            opacity: o.opacity
        });
    }

    function path(d, o) {
        o = o || {};
        return e("path", {
            d: d,
            fill: o.fill || "none",
            stroke: o.stroke || "var(--border-subtle)",
            "stroke-width": o.sw === undefined ? 1.3 : o.sw,
            "stroke-dasharray": o.dash,
            "stroke-linejoin": "round",
            "fill-opacity": o.fo,
            opacity: o.opacity
        });
    }

    function circle(cx, cy, r, o) {
        o = o || {};
        return e("circle", {
            cx: cx, cy: cy, r: r,
            fill: o.fill || "none",
            stroke: o.stroke || "var(--border-subtle)",
            "stroke-width": o.sw === undefined ? 1.3 : o.sw,
            "fill-opacity": o.fo,
            opacity: o.opacity
        });
    }

    /* An arrowhead drawn as a path rather than a marker: markers inherit the
     * line's stroke, and every diagram here wants heads in two colours. */
    function arrow(x1, y1, x2, y2, o) {
        o = o || {};
        var g = e("g", {});
        g.appendChild(line(x1, y1, x2, y2, o));
        var a = Math.atan2(y2 - y1, x2 - x1), s = o.head || 4;
        g.appendChild(path(
            "M" + x2 + " " + y2 +
            "L" + (x2 - s * Math.cos(a - 0.45)) + " " + (y2 - s * Math.sin(a - 0.45)) +
            "L" + (x2 - s * Math.cos(a + 0.45)) + " " + (y2 - s * Math.sin(a + 0.45)) + "Z",
            { fill: o.stroke || "var(--border-subtle)", stroke: "none", sw: 0 }));
        return g;
    }

    var ACCENT = "var(--accent-primary)";
    /* A second and third hue for diagrams that need to distinguish two things
     * neither of which is "the accent" - the discriminator against the
     * distributions, one detected class against another, the rounded region
     * against the true one. Tokens rather than hexes: a blue that reads as
     * 9px text on the dark ground is illegible on the light one. */
    var SERIES2 = "var(--vz-series-2)";
    var SERIES3 = "var(--vz-series-3)";
    var WARN = "var(--vz-series-warn)";
    var FILL = "var(--accent-fill)";
    var MUTED = "var(--text-muted)";
    var MAIN = "var(--text-main)";
    var BORDER = "var(--border-subtle)";
    var SURFACE = "var(--bg-surface)";

    // -------------------------------------------------------------- numbers

    /* 1_234_567 -> "1.23 M". Parameter counts are the whole point of several
     * of these pages, and a raw digit string is unreadable at a glance. */
    function fmt(n) {
        var a = Math.abs(n);
        if (a >= 1e9) return (n / 1e9).toFixed(a >= 1e11 ? 0 : (a >= 1e10 ? 1 : 2)) + " G";
        if (a >= 1e6) return (n / 1e6).toFixed(a >= 1e8 ? 0 : (a >= 1e7 ? 1 : 2)) + " M";
        if (a >= 1e3) return (n / 1e3).toFixed(a >= 1e5 ? 0 : 1) + " K";
        return String(Math.round(n));
    }

    function commas(n) {
        return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    /* Deterministic pseudo-random source. Math.random would redraw differently
     * on every frame, so a slider would look like it was changing the noise
     * rather than the thing it controls. Mulberry32. */
    function rng(seed) {
        var st = (seed || 1) >>> 0;
        return function () {
            st = (st + 0x6D2B79F5) >>> 0;
            var t = st;
            t = Math.imul(t ^ (t >>> 15), t | 1);
            t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
            return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        };
    }

    function gauss(r) {
        var u = 1 - r(), v = r();
        return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
    }

    function clamp(v, lo, hi) { return v < lo ? lo : (v > hi ? hi : v); }

    // ------------------------------------------------- convolution arithmetic

    /* The one formula every convolutional module on this site depends on.
     * Written once here so the fifteen pages cannot disagree about it. */
    function convOut(inSize, k, stride, pad, dil) {
        dil = dil || 1;
        return Math.floor((inSize + 2 * pad - (dil * (k - 1) + 1)) / stride) + 1;
    }

    function convParams(cin, cout, k, groups, bias) {
        groups = groups || 1;
        return cout * (cin / groups) * k * k + (bias ? cout : 0);
    }

    /* Multiply-accumulates, the unit everyone means when they say "FLOPs" for
     * a conv net and then quote half the number. One MAC is two FLOPs. */
    function convMacs(cin, cout, k, outSize, groups) {
        groups = groups || 1;
        return cout * outSize * outSize * (cin / groups) * k * k;
    }

    // ------------------------------------------------------------- controls

    function control(spec, onChange) {
        var wrap = h("label", "arch-control");
        var name = h("span", "arch-control-name", spec.label);
        var value = h("span", "arch-control-value", "");
        wrap.appendChild(name);
        wrap.appendChild(value);

        var input, fmtv = spec.fmt;
        if (spec.type === "select") {
            input = h("select");
            spec.options.forEach(function (o) {
                var op = h("option", null, o.label);
                op.value = o.value;
                input.appendChild(op);
            });
            input.value = spec.value;
        } else if (spec.type === "toggle") {
            input = h("input");
            input.type = "checkbox";
            input.checked = !!spec.value;
        } else {
            input = h("input");
            input.type = "range";
            input.min = spec.min; input.max = spec.max;
            input.step = spec.step || 1; input.value = spec.value;
        }
        input.className = "arch-input";
        if (spec.id) input.id = spec.id;
        wrap.appendChild(input);

        function read() {
            if (spec.type === "toggle") {
                value.textContent = input.checked ? "on" : "off";
                return input.checked;
            }
            if (spec.type === "select") {
                value.textContent = "";
                return input.value;
            }
            var v = parseFloat(input.value);
            value.textContent = fmtv ? fmtv(v) : String(v);
            return v;
        }
        input.addEventListener("input", function () { onChange(spec.key, read()); });
        input.addEventListener("change", function () { onChange(spec.key, read()); });
        read();
        return { el: wrap, read: read, input: input };
    }

    // --------------------------------------------------- shared sub-widgets

    /* A proportional bar with a label and a figure. Used wherever a page is
     * making the point that one part of a model dominates a budget. */
    function bars(rows, opts) {
        opts = opts || {};
        var total = 0, i;
        for (i = 0; i < rows.length; i++) total += rows[i].value;
        var max = 0;
        for (i = 0; i < rows.length; i++) max = Math.max(max, rows[i].value);
        var wrap = h("div", "arch-bars");
        rows.forEach(function (r) {
            var row = h("div", "arch-bar-row" + (r.hot ? " is-hot" : ""));
            row.appendChild(h("span", "arch-bar-label", r.label));
            var track = h("div", "arch-bar-track");
            var fill = h("div", "arch-bar-fill");
            fill.style.width = (max ? (100 * r.value / max) : 0).toFixed(2) + "%";
            track.appendChild(fill);
            row.appendChild(track);
            row.appendChild(h("span", "arch-bar-value",
                opts.format ? opts.format(r.value, total) : fmt(r.value)));
            wrap.appendChild(row);
        });
        return wrap;
    }

    /* A stat strip. Every page carries three or four headline numbers that
     * have to move when a control moves, or the control is decorative. */
    function stats(items) {
        var wrap = h("div", "arch-stats");
        items.forEach(function (it) {
            var box = h("div", "arch-stat");
            box.appendChild(h("span", "arch-stat-value", it.value));
            box.appendChild(h("span", "arch-stat-label", it.label));
            if (it.note) box.appendChild(h("span", "arch-stat-note", it.note));
            wrap.appendChild(box);
        });
        return wrap;
    }

    /* The layer table. Rows are selectable; selecting one is how a reader asks
     * "where did that number come from", and the answer is the detail line
     * below it rather than a tooltip nobody finds on a phone. */
    function layerTable(cols, rows, onPick, selected) {
        var wrap = h("div", "arch-table-wrap");
        var t = h("table", "arch-table");
        var thead = h("thead"), tr = h("tr");
        cols.forEach(function (c) { tr.appendChild(h("th", null, c)); });
        thead.appendChild(tr);
        t.appendChild(thead);
        var tb = h("tbody");
        rows.forEach(function (r, i) {
            var row = h("tr", (i === selected ? "is-selected " : "") +
                              (r.stage ? "is-stage" : ""));
            r.cells.forEach(function (c) {
                var td = h("td", null, c);
                row.appendChild(td);
            });
            if (onPick) {
                row.tabIndex = 0;
                row.addEventListener("click", function () { onPick(i); });
                row.addEventListener("keydown", function (ev) {
                    if (ev.key === "Enter" || ev.key === " ") {
                        ev.preventDefault(); onPick(i);
                    }
                });
            }
            tb.appendChild(row);
        });
        t.appendChild(tb);
        wrap.appendChild(t);
        return wrap;
    }

    /* Pointer dragging that survives the stage being rebuilt.
     *
     * Every widget redraws by clearing its stage, which detaches whatever the
     * pointer was captured on - and removing a capturing element from the
     * document releases the capture, so the drag died on the first frame.
     * Listening on `window` for the duration of the gesture sidesteps that
     * entirely: the window is never replaced. The element only has to survive
     * long enough to receive the pointerdown, which it does, because widgets
     * move their canvas rather than recreating it.
     */
    function drag(target, onMove) {
        target.addEventListener("pointerdown", function (ev) {
            onMove(ev);
            ev.preventDefault();
            function moved(e) { onMove(e); e.preventDefault(); }
            function done() {
                window.removeEventListener("pointermove", moved);
                window.removeEventListener("pointerup", done);
                window.removeEventListener("pointercancel", done);
            }
            window.addEventListener("pointermove", moved, { passive: false });
            window.addEventListener("pointerup", done);
            window.addEventListener("pointercancel", done);
        });
    }

    function note(str) {
        var p = h("p", "arch-note");
        p.innerHTML = str;
        return p;
    }

    function caption(str) {
        return h("p", "arch-caption", str);
    }

    function section(title) {
        return h("h4", "arch-sub", title);
    }

    // -------------------------------------------------------------- the mount

    var WIDGETS = {};

    function mount(root) {
        var cfgEl = root.querySelector(".arch-config");
        if (!cfgEl) return;
        var cfg;
        try { cfg = JSON.parse(cfgEl.textContent); } catch (err) { return; }
        var spec = WIDGETS[cfg.widget];
        if (!spec) return;

        root.innerHTML = "";

        var stage = h("div", "arch-stage");
        var readoutEl = h("p", "arch-readout");
        readoutEl.setAttribute("aria-live", "polite");
        var panel = h("div", "arch-controls");

        var params = {};
        var specs = (spec.controls || []).concat(cfg.controls || []);
        Object.keys(cfg.fixed || {}).forEach(function (k) { params[k] = cfg.fixed[k]; });

        var queued = false;
        function schedule() {
            if (queued) return;
            queued = true;
            requestAnimationFrame(function () { queued = false; draw(); });
        }

        var ctx = {
            stage: stage,
            params: params,
            cfg: cfg,
            redraw: schedule,
            setReadout: function (str) { readoutEl.textContent = str; }
        };

        specs.forEach(function (cs) {
            var c = control(cs, function (key, val) {
                params[key] = val;
                schedule();
            });
            params[cs.key] = c.read();
            panel.appendChild(c.el);
        });

        var draw = spec.build(ctx);

        root.appendChild(stage);
        root.appendChild(panel);
        root.appendChild(readoutEl);
        draw();
        root.dataset.vzArchReady = "1";
    }

    function init() {
        Array.prototype.forEach.call(
            document.querySelectorAll("[data-vz-arch]"), mount);
    }

    /* Exposed so the widget definitions below - which are separate blocks in
     * this same file - can register themselves against one shared toolkit.
     * init() is called by the boot block at the very end of the file, after
     * every widget has registered: calling it here would run the mount before
     * WIDGETS held anything to mount. */
    window.VizArch = {
        WIDGETS: WIDGETS,
        init: init,
        h: h, e: e, svg: svg, text: text, rect: rect, line: line,
        path: path, circle: circle, arrow: arrow,
        fmt: fmt, commas: commas, rng: rng, gauss: gauss, clamp: clamp,
        convOut: convOut, convParams: convParams, convMacs: convMacs,
        bars: bars, stats: stats, layerTable: layerTable, drag: drag,
        note: note, caption: caption, section: section,
        ACCENT: ACCENT, FILL: FILL, MUTED: MUTED, MAIN: MAIN,
        BORDER: BORDER, SURFACE: SURFACE,
        SERIES2: SERIES2, SERIES3: SERIES3, WARN: WARN
    };
})();

/* ===========================================================================
 * VGG-16
 *
 * The point of the page is that VGG is two models bolted together: a small,
 * cheap, uniform convolutional tower and an enormous fully-connected head.
 * The tower holds 14.7 M of the 138 M parameters and does essentially all of
 * the arithmetic; the head holds the other 123 M and does almost none. You
 * cannot see that in a block diagram, so here both budgets are drawn.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, line = A.line;

    /* Configuration D from the paper: (channels, count) per block. */
    var BLOCKS = [
        { name: "block1", ch: 64, convs: 2 },
        { name: "block2", ch: 128, convs: 2 },
        { name: "block3", ch: 256, convs: 3 },
        { name: "block4", ch: 512, convs: 3 },
        { name: "block5", ch: 512, convs: 3 }
    ];

    function model(p) {
        var size = p.input, cin = 3, layers = [], i, b, j;
        for (i = 0; i < BLOCKS.length; i++) {
            b = BLOCKS[i];
            for (j = 0; j < b.convs; j++) {
                layers.push({
                    kind: "conv", block: i,
                    name: "conv3-" + b.ch,
                    inCh: cin, outCh: b.ch, size: size, out: size, k: 3,
                    params: A.convParams(cin, b.ch, 3, 1, true),
                    macs: A.convMacs(cin, b.ch, 3, size, 1)
                });
                cin = b.ch;
            }
            var half = Math.floor(size / 2);
            layers.push({
                kind: "pool", block: i, name: "maxpool 2x2 /2",
                inCh: cin, outCh: cin, size: size, out: half,
                params: 0, macs: 0
            });
            size = half;
        }
        var flat = cin * size * size;
        if (p.gap) {
            layers.push({
                kind: "gap", block: 5, name: "global average pool",
                inCh: cin, outCh: cin, size: size, out: 1, params: 0,
                macs: cin * size * size
            });
            layers.push({
                kind: "fc", block: 5, name: "FC-1000", inCh: cin, outCh: 1000,
                size: 1, out: 1, params: cin * 1000 + 1000, macs: cin * 1000
            });
        } else {
            layers.push({
                kind: "fc", block: 5, name: "FC-4096", inCh: flat, outCh: 4096,
                size: size, out: 1, params: flat * 4096 + 4096, macs: flat * 4096
            });
            layers.push({
                kind: "fc", block: 5, name: "FC-4096", inCh: 4096, outCh: 4096,
                size: 1, out: 1, params: 4096 * 4096 + 4096, macs: 4096 * 4096
            });
            layers.push({
                kind: "fc", block: 5, name: "FC-1000", inCh: 4096, outCh: 1000,
                size: 1, out: 1, params: 4096 * 1000 + 1000, macs: 4096 * 1000
            });
        }
        return { layers: layers, flat: flat, finalSize: size, finalCh: cin };
    }

    function diagram(m, p, sel, pick) {
        var W = 640, H = 210;
        var s = svg(W, H, "arch-svg-wide");
        var convs = m.layers.filter(function (l) { return l.kind === "conv"; });
        var x = 24, gap = 4;
        var maxSize = p.input;
        convs.forEach(function (l, i) {
            var idx = m.layers.indexOf(l);
            var hgt = 20 + 110 * (l.size / maxSize);
            var w = 8 + 16 * (Math.log2(l.outCh) - 5) / 4;
            var y = 30 + (140 - hgt) / 2;
            var hot = idx === sel;
            var r = rect(x, y, w, hgt, {
                fill: hot ? A.FILL : A.SURFACE,
                fo: hot ? 0.85 : 1,
                stroke: hot ? A.ACCENT : A.BORDER,
                sw: hot ? 2 : 1.2, rx: 2
            });
            r.style.cursor = "pointer";
            r.addEventListener("click", function () { pick(idx); });
            s.appendChild(r);
            if (i === 0 || convs[i - 1].outCh !== l.outCh)
                s.appendChild(text(x + w / 2, y - 6, String(l.outCh),
                    { size: 8, fill: A.MUTED }));
            x += w + gap;
            /* the pool that follows the last conv of a block */
            var next = m.layers[idx + 1];
            if (next && next.kind === "pool") {
                s.appendChild(line(x + 2, y + hgt / 2 - 6, x + 2, y + hgt / 2 + 6,
                    { stroke: A.ACCENT, sw: 2 }));
                s.appendChild(text(x + 2, 178, String(next.out),
                    { size: 7, fill: A.MUTED }));
                x += 9;
            }
        });

        /* the head */
        var hx = x + 14;
        var heads = m.layers.filter(function (l) {
            return l.kind === "fc" || l.kind === "gap";
        });
        heads.forEach(function (l) {
            var idx = m.layers.indexOf(l);
            var hot = idx === sel;
            var hgt = l.kind === "gap" ? 26 : 86;
            var w = l.outCh === 1000 ? 14 : (l.kind === "gap" ? 14 : 26);
            var y = 30 + (140 - hgt) / 2;
            var r = rect(hx, y, w, hgt, {
                fill: hot ? A.FILL : A.SURFACE, fo: hot ? 0.85 : 1,
                stroke: hot ? A.ACCENT : A.BORDER, sw: hot ? 2 : 1.2, rx: 2
            });
            r.style.cursor = "pointer";
            r.addEventListener("click", function () { pick(idx); });
            s.appendChild(r);
            s.appendChild(text(hx + w / 2, y - 6,
                l.kind === "gap" ? "GAP" : String(l.outCh),
                { size: 8, fill: A.MUTED }));
            hx += w + 6;
        });

        s.appendChild(text(24, 22, "convolutional tower  -  " +
            A.fmt(m.layers.reduce(function (a, l) {
                return a + (l.kind === "conv" ? l.params : 0);
            }, 0)) + " parameters", { size: 9, fill: A.MUTED, anchor: "start" }));
        s.appendChild(text(x + 14, 22, "classifier head  -  " +
            A.fmt(m.layers.reduce(function (a, l) {
                return a + (l.kind === "fc" ? l.params : 0);
            }, 0)), { size: 9, fill: A.ACCENT, anchor: "start" }));
        s.appendChild(text(24, 196, "bar height = spatial size, bar width = log channels; " +
            "tick marks are the max-pools", { size: 8, fill: A.MUTED, anchor: "start" }));
        return s;
    }

    A.WIDGETS.vgg16 = {
        controls: [
            { key: "input", label: "Input resolution", type: "range",
              min: 96, max: 320, step: 32, value: 224, id: "vgg-input",
              fmt: function (v) { return v + " x " + v; } },
            { key: "gap", label: "Swap the FC head for global average pooling",
              type: "toggle", value: false, id: "vgg-gap" }
        ],
        build: function (ctx) {
            var sel = 0;
            function pick(i) { sel = i; ctx.redraw(); }
            return function draw() {
                var p = ctx.params;
                var m = model(p);
                var totalP = 0, totalM = 0, towerP = 0, headP = 0, towerM = 0, headM = 0;
                m.layers.forEach(function (l) {
                    totalP += l.params; totalM += l.macs;
                    if (l.kind === "fc") { headP += l.params; headM += l.macs; }
                    else { towerP += l.params; towerM += l.macs; }
                });
                if (sel >= m.layers.length) sel = 0;

                ctx.stage.innerHTML = "";
                var scroll = h("div", "arch-scroll");
                scroll.appendChild(diagram(m, p, sel, pick));
                ctx.stage.appendChild(scroll);

                ctx.stage.appendChild(A.stats([
                    { value: A.fmt(totalP), label: "parameters",
                      note: A.commas(totalP) },
                    { value: A.fmt(totalM), label: "MACs / image",
                      note: A.fmt(totalM * 2) + " FLOPs" },
                    { value: (100 * headP / totalP).toFixed(1) + "%",
                      label: "params in the head",
                      note: (100 * headM / totalM).toFixed(1) + "% of the work" },
                    { value: m.finalCh + " x " + m.finalSize + "x" + m.finalSize,
                      label: "tower output", note: A.commas(m.flat) + " values" }
                ]));

                ctx.stage.appendChild(A.section("Where the parameters are"));
                ctx.stage.appendChild(A.bars([
                    { label: "conv tower (13 layers)", value: towerP },
                    { label: "classifier head", value: headP, hot: true }
                ], { format: function (v) {
                    return A.fmt(v) + "  (" + (100 * v / totalP).toFixed(0) + "%)"; } }));

                ctx.stage.appendChild(A.section("Where the arithmetic is"));
                ctx.stage.appendChild(A.bars([
                    { label: "conv tower (13 layers)", value: towerM, hot: true },
                    { label: "classifier head", value: headM }
                ], { format: function (v) {
                    return A.fmt(v) + "  (" + (100 * v / totalM).toFixed(0) + "%)"; } }));

                var rows = m.layers.map(function (l, i) {
                    var shape = l.kind === "fc" || l.kind === "gap"
                        ? String(l.outCh)
                        : l.outCh + " x " + l.out + "x" + l.out;
                    return {
                        cells: [l.name, shape, l.params ? A.fmt(l.params) : "-",
                                l.macs ? A.fmt(l.macs) : "-"],
                        stage: l.kind === "pool"
                    };
                });
                ctx.stage.appendChild(A.section("Every layer, in order"));
                ctx.stage.appendChild(
                    A.layerTable(["layer", "output", "params", "MACs"], rows, pick, sel));

                var l = m.layers[sel];
                var detail;
                if (l.kind === "conv") {
                    detail = "<strong>" + l.name + "</strong>: a 3&times;3 kernel over " +
                        l.inCh + " input channels, " + l.outCh + " times over, plus one bias " +
                        "each &mdash; " + l.outCh + " &times; " + l.inCh + " &times; 3 &times; 3 + " +
                        l.outCh + " = <strong>" + A.commas(l.params) + "</strong> parameters. " +
                        "Applied at every one of " + l.out + "&times;" + l.out + " positions, that is " +
                        A.fmt(l.macs) + " multiply-accumulates.";
                } else if (l.kind === "pool") {
                    detail = "<strong>" + l.name + "</strong>: no parameters at all. It halves " +
                        "the map from " + l.size + "&times;" + l.size + " to " + l.out + "&times;" +
                        l.out + ", which quarters the cost of every layer after it.";
                } else if (l.kind === "gap") {
                    detail = "<strong>Global average pooling</strong>: each of the " + l.inCh +
                        " maps collapses to its own mean, so a " + l.inCh + "&times;" + l.size +
                        "&times;" + l.size + " tensor becomes " + l.inCh + " numbers with no " +
                        "parameters and no dependence on input resolution.";
                } else {
                    detail = "<strong>" + l.name + "</strong>: a dense layer, " + A.commas(l.inCh) +
                        " in &rarr; " + l.outCh + " out. Every input is wired to every output: " +
                        A.commas(l.inCh) + " &times; " + l.outCh + " + " + l.outCh + " = <strong>" +
                        A.commas(l.params) + "</strong> parameters, used once per image.";
                }
                ctx.stage.appendChild(A.note(detail));

                ctx.setReadout(
                    (p.gap ? "with GAP head" : "with the original FC head") +
                    " at " + p.input + "x" + p.input + ": " + A.commas(totalP) +
                    " parameters, " + A.fmt(totalM) + " MACs per image");
            };
        }
    };
})();

/* ===========================================================================
 * InceptionNet - the inception module and the 1x1 bottleneck
 *
 * The module is four convolutions run in parallel on the same input and
 * concatenated. That is easy to draw and easy to believe. What is not obvious
 * is that the naive version is unaffordable, and that one 1x1 convolution in
 * front of each expensive branch is what makes the whole network cheaper than
 * VGG despite being far deeper. So the toggle here rebuilds both and puts the
 * two multiply-accumulate counts side by side.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, arrow = A.arrow;

    /* GoogLeNet, table 1 of the paper. Nine modules, and the widths are not
     * a pattern - they were tuned, which is itself worth seeing. */
    var MODULES = [
        { name: "3a", inCh: 192, size: 28, c1: 64, r3: 96, c3: 128, r5: 16, c5: 32, pp: 32 },
        { name: "3b", inCh: 256, size: 28, c1: 128, r3: 128, c3: 192, r5: 32, c5: 96, pp: 64 },
        { name: "4a", inCh: 480, size: 14, c1: 192, r3: 96, c3: 208, r5: 16, c5: 48, pp: 64 },
        { name: "4b", inCh: 512, size: 14, c1: 160, r3: 112, c3: 224, r5: 24, c5: 64, pp: 64 },
        { name: "4c", inCh: 512, size: 14, c1: 128, r3: 128, c3: 256, r5: 24, c5: 64, pp: 64 },
        { name: "4d", inCh: 512, size: 14, c1: 112, r3: 144, c3: 288, r5: 32, c5: 64, pp: 64 },
        { name: "4e", inCh: 528, size: 14, c1: 256, r3: 160, c3: 320, r5: 32, c5: 128, pp: 128 },
        { name: "5a", inCh: 832, size: 7, c1: 256, r3: 160, c3: 320, r5: 32, c5: 128, pp: 128 },
        { name: "5b", inCh: 832, size: 7, c1: 384, r3: 192, c3: 384, r5: 48, c5: 128, pp: 128 }
    ];

    function scale(m, w) {
        var r = { name: m.name, size: m.size, inCh: m.inCh };
        ["c1", "r3", "c3", "r5", "c5", "pp"].forEach(function (k) {
            r[k] = Math.max(1, Math.round(m[k] * w / 8) * 8);
        });
        return r;
    }

    /* Both costings for one module. `bn` false is the naive version: no
     * reductions, and the pool branch passes its input straight through. */
    function cost(m, bn) {
        var s = m.size, br = [];
        br.push({
            label: "1x1  ->  " + m.c1,
            params: A.convParams(m.inCh, m.c1, 1, 1, true),
            macs: A.convMacs(m.inCh, m.c1, 1, s, 1),
            out: m.c1
        });
        if (bn) {
            br.push({
                label: "1x1 -> " + m.r3 + "  then  3x3 -> " + m.c3,
                params: A.convParams(m.inCh, m.r3, 1, 1, true) +
                        A.convParams(m.r3, m.c3, 3, 1, true),
                macs: A.convMacs(m.inCh, m.r3, 1, s, 1) +
                      A.convMacs(m.r3, m.c3, 3, s, 1),
                out: m.c3
            });
            br.push({
                label: "1x1 -> " + m.r5 + "  then  5x5 -> " + m.c5,
                params: A.convParams(m.inCh, m.r5, 1, 1, true) +
                        A.convParams(m.r5, m.c5, 5, 1, true),
                macs: A.convMacs(m.inCh, m.r5, 1, s, 1) +
                      A.convMacs(m.r5, m.c5, 5, s, 1),
                out: m.c5
            });
            br.push({
                label: "3x3 pool  then  1x1 -> " + m.pp,
                params: A.convParams(m.inCh, m.pp, 1, 1, true),
                macs: A.convMacs(m.inCh, m.pp, 1, s, 1),
                out: m.pp
            });
        } else {
            br.push({
                label: "3x3 -> " + m.c3 + "  (no reduction)",
                params: A.convParams(m.inCh, m.c3, 3, 1, true),
                macs: A.convMacs(m.inCh, m.c3, 3, s, 1),
                out: m.c3
            });
            br.push({
                label: "5x5 -> " + m.c5 + "  (no reduction)",
                params: A.convParams(m.inCh, m.c5, 5, 1, true),
                macs: A.convMacs(m.inCh, m.c5, 5, s, 1),
                out: m.c5
            });
            br.push({
                label: "3x3 pool, passed through",
                params: 0, macs: 0, out: m.inCh
            });
        }
        var p = 0, mc = 0, out = 0;
        br.forEach(function (b) { p += b.params; mc += b.macs; out += b.out; });
        return { branches: br, params: p, macs: mc, out: out };
    }

    function diagram(m, bn, c) {
        var W = 620, H = 250;
        var s = svg(W, H, "arch-svg-wide");
        var cx = W / 2;
        s.appendChild(rect(cx - 90, 8, 180, 26, { fill: A.SURFACE, stroke: A.BORDER }));
        s.appendChild(text(cx, 25, "input   " + m.inCh + " x " + m.size + "x" + m.size,
            { size: 10, fill: A.MAIN }));

        var lanes = [0, 1, 2, 3], laneW = 140, x0 = 12;
        var names = bn
            ? ["1x1", "1x1 reduce", "1x1 reduce", "3x3 max pool"]
            : ["1x1", "3x3", "5x5", "3x3 max pool"];
        var second = bn ? [null, "3x3 conv", "5x5 conv", "1x1 project"] : [null, null, null, null];
        var chFirst = bn ? [m.c1, m.r3, m.r5, m.inCh] : [m.c1, m.c3, m.c5, m.inCh];
        var chSecond = bn ? [null, m.c3, m.c5, m.pp] : [null, null, null, null];

        lanes.forEach(function (i) {
            var x = x0 + i * (laneW + 12);
            s.appendChild(arrow(cx, 34, x + laneW / 2, 62,
                { stroke: A.BORDER, sw: 1.1 }));
            var hot = bn && (i === 1 || i === 2 || i === 3);
            s.appendChild(rect(x, 64, laneW, 30, {
                fill: hot ? A.FILL : A.SURFACE, fo: hot ? 0.2 : 1,
                stroke: hot ? A.ACCENT : A.BORDER
            }));
            s.appendChild(text(x + laneW / 2, 83, names[i] + "  ->  " + chFirst[i],
                { size: 9, fill: hot ? A.ACCENT : A.MAIN }));
            var bottomY = 94;
            if (second[i]) {
                s.appendChild(arrow(x + laneW / 2, 94, x + laneW / 2, 112,
                    { stroke: A.BORDER, sw: 1.1 }));
                s.appendChild(rect(x, 114, laneW, 30, { fill: A.SURFACE, stroke: A.BORDER }));
                s.appendChild(text(x + laneW / 2, 133, second[i] + "  ->  " + chSecond[i],
                    { size: 9, fill: A.MAIN }));
                bottomY = 144;
            }
            s.appendChild(arrow(x + laneW / 2, bottomY, x + laneW / 2, 168,
                { stroke: A.BORDER, sw: 1.1 }));
            s.appendChild(text(x + laneW / 2, 163, A.fmt(c.branches[i].macs) + " MACs",
                { size: 8, fill: A.MUTED }));
        });

        s.appendChild(rect(x0, 170, 4 * laneW + 3 * 12, 28,
            { fill: A.FILL, fo: 0.16, stroke: A.ACCENT }));
        s.appendChild(text(cx, 189, "concatenate along channels  ->  " + c.out +
            " x " + m.size + "x" + m.size, { size: 10, fill: A.ACCENT }));
        s.appendChild(text(cx, 218,
            "every branch keeps the map at " + m.size + "x" + m.size +
            ", which is the only reason they can be concatenated",
            { size: 8.5, fill: A.MUTED }));
        s.appendChild(text(cx, 234,
            bn ? "the highlighted 1x1 layers are the bottleneck"
               : "naive: each large kernel reads all " + m.inCh + " input channels",
            { size: 8.5, fill: bn ? A.ACCENT : A.MUTED }));
        return s;
    }

    A.WIDGETS.inception = {
        controls: [
            { key: "module", label: "Inception module", type: "select", value: "3a",
              id: "inc-module",
              options: MODULES.map(function (m) {
                  return { value: m.name, label: "inception " + m.name +
                           "  (" + m.inCh + " ch @ " + m.size + "x" + m.size + ")" };
              }) },
            { key: "bottleneck", label: "1x1 bottleneck before the big kernels",
              type: "toggle", value: true, id: "inc-bottleneck" },
            { key: "width", label: "Width multiplier", type: "range",
              min: 0.5, max: 2, step: 0.25, value: 1, id: "inc-width",
              fmt: function (v) { return v.toFixed(2) + "x"; } }
        ],
        build: function (ctx) {
            return function draw() {
                var p = ctx.params;
                var base = MODULES.filter(function (m) { return m.name === p.module; })[0]
                        || MODULES[0];
                var m = scale(base, p.width);
                var withBn = cost(m, true), naive = cost(m, false);
                var c = p.bottleneck ? withBn : naive;

                ctx.stage.innerHTML = "";
                var scroll = h("div", "arch-scroll");
                scroll.appendChild(diagram(m, p.bottleneck, c));
                ctx.stage.appendChild(scroll);

                ctx.stage.appendChild(A.stats([
                    { value: A.fmt(c.macs), label: "MACs for this module",
                      note: A.commas(Math.round(c.macs)) },
                    { value: A.fmt(c.params), label: "parameters",
                      note: A.commas(Math.round(c.params)) },
                    { value: (naive.macs / withBn.macs).toFixed(1) + "x",
                      label: "naive / bottleneck", note: "arithmetic saved" },
                    { value: c.out, label: "output channels",
                      note: "at " + m.size + "x" + m.size }
                ]));

                ctx.stage.appendChild(A.section("Cost of each branch"));
                ctx.stage.appendChild(A.bars(c.branches.map(function (b, i) {
                    return { label: b.label, value: b.macs, hot: i === 2 && !p.bottleneck };
                }), { format: function (v, t) {
                    return A.fmt(v) + "  (" + (t ? (100 * v / t).toFixed(0) : 0) + "%)";
                } }));

                ctx.stage.appendChild(A.section("The same module, both ways"));
                ctx.stage.appendChild(A.bars([
                    { label: "naive - big kernels read every input channel",
                      value: naive.macs, hot: true },
                    { label: "with 1x1 reductions", value: withBn.macs }
                ], { format: function (v) { return A.fmt(v) + " MACs"; } }));

                /* the whole network, so the module is seen in context */
                var totP = 0, totM = 0;
                var rows = MODULES.map(function (mm) {
                    var sm = scale(mm, p.width);
                    var cc = cost(sm, p.bottleneck);
                    totP += cc.params; totM += cc.macs;
                    return {
                        cells: ["inception " + mm.name,
                                sm.inCh + " x " + sm.size + "x" + sm.size,
                                cc.out + " x " + sm.size + "x" + sm.size,
                                A.fmt(cc.params), A.fmt(cc.macs)],
                        stage: mm.name === p.module
                    };
                });
                ctx.stage.appendChild(A.section("All nine modules of GoogLeNet"));
                ctx.stage.appendChild(A.layerTable(
                    ["module", "input", "output", "params", "MACs"], rows, null, -1));

                ctx.stage.appendChild(A.note(
                    "The nine modules together hold <strong>" + A.fmt(totP) +
                    "</strong> parameters and do <strong>" + A.fmt(totM) +
                    "</strong> multiply-accumulates. VGG-16's classifier head alone holds " +
                    "123 M parameters, and GoogLeNet has no such head at all &mdash; it " +
                    "ends in a global average pool and one 1024&rarr;1000 layer."));

                ctx.setReadout("inception " + p.module + ", " +
                    (p.bottleneck ? "with" : "without") + " 1x1 reductions: " +
                    A.fmt(c.macs) + " MACs, " + A.fmt(c.params) + " parameters, " +
                    c.out + " output channels");
            };
        }
    };
})();

/* ===========================================================================
 * ResNet - the whole family, from one description
 *
 * ResNet-18, -34, -50, -101 and -152 are not five architectures. They are one
 * architecture with two block types and a list of four numbers, and the
 * parameter counts everyone quotes fall out of that description exactly:
 * 11.69 M, 21.80 M, 25.56 M, 44.55 M, 60.19 M. Building them here from the
 * same code is the point - a reader can change the block counts and watch a
 * published figure move.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, arrow = A.arrow, path = A.path;

    var FAMILY = {
        "18": { blocks: [2, 2, 2, 2], bottleneck: false },
        "34": { blocks: [3, 4, 6, 3], bottleneck: false },
        "50": { blocks: [3, 4, 6, 3], bottleneck: true },
        "101": { blocks: [3, 4, 23, 3], bottleneck: true },
        "152": { blocks: [3, 8, 36, 3], bottleneck: true }
    };
    var CHANS = [64, 128, 256, 512];

    /* Every conv in a ResNet is bias-free with a batch norm after it, so the
     * 2 x channels of BN scale and shift are counted here too. Leave them out
     * and ResNet-50 comes to 25.50 M rather than the 25.56 M every framework
     * prints, which is exactly the kind of small unexplained gap that makes a
     * reader distrust the rest of the page. */
    function conv(ci, co, k, stride, outSize, tag) {
        return {
            tag: tag, ci: ci, co: co, k: k, stride: stride, out: outSize,
            params: co * ci * k * k + 2 * co,
            macs: co * outSize * outSize * ci * k * k
        };
    }

    function model(p) {
        var f = FAMILY[String(p.depth)] || FAMILY["50"];
        var exp = f.bottleneck ? 4 : 1;
        var layers = [], stages = [];
        var size = Math.floor(p.input / 2);
        layers.push(conv(3, 64, 7, 2, size, "conv1  7x7, 64, /2"));
        size = Math.floor(size / 2);
        layers.push({ tag: "max pool 3x3 /2", ci: 64, co: 64, k: 3, stride: 2,
                      out: size, params: 0, macs: 0 });

        var cin = 64;
        for (var st = 0; st < 4; st++) {
            var c = CHANS[st], stride = st === 0 ? 1 : 2;
            var stageP = 0, stageM = 0, first = null;
            for (var b = 0; b < f.blocks[st]; b++) {
                var s = b === 0 ? stride : 1;
                var osz = b === 0 ? Math.floor(size / stride) : size;
                var inner = [];
                if (f.bottleneck) {
                    inner.push(conv(cin, c, 1, 1, b === 0 ? size : osz, "1x1 reduce"));
                    inner.push(conv(c, c, 3, s, osz, "3x3" + (s > 1 ? " /2" : "")));
                    inner.push(conv(c, c * 4, 1, 1, osz, "1x1 expand"));
                } else {
                    inner.push(conv(cin, c, 3, s, osz, "3x3" + (s > 1 ? " /2" : "")));
                    inner.push(conv(c, c, 3, 1, osz, "3x3"));
                }
                var shortcut = null;
                if (b === 0 && (cin !== c * exp || s !== 1)) {
                    shortcut = conv(cin, c * exp, 1, s, osz, "1x1 projection shortcut");
                    inner.push(shortcut);
                }
                var bp = 0, bm = 0;
                inner.forEach(function (l) { bp += l.params; bm += l.macs; });
                stageP += bp; stageM += bm;
                if (b === 0) {
                    first = { inner: inner, params: bp, macs: bm, shortcut: shortcut,
                              inCh: cin, outCh: c * exp, inSize: size, outSize: osz };
                    size = osz;
                }
                cin = c * exp;
            }
            stages.push({
                idx: st + 1, width: c, blocks: f.blocks[st], size: size,
                inCh: st === 0 ? 64 : CHANS[st - 1] * exp, outCh: c * exp,
                params: stageP, macs: stageM, first: first
            });
        }
        var fc = { tag: "fc  " + cin + " -> 1000", ci: cin, co: 1000, k: 1,
                   stride: 1, out: 1, params: cin * 1000 + 1000, macs: cin * 1000 };
        var total = fc.params, macs = fc.macs;
        layers.forEach(function (l) { total += l.params; macs += l.macs; });
        stages.forEach(function (s) { total += s.params; macs += s.macs; });
        return { stem: layers, stages: stages, fc: fc, params: total, macs: macs,
                 bottleneck: f.bottleneck, exp: exp, finalCh: cin, finalSize: size };
    }

    /* The block, opened up. This is the diagram the paper is famous for, and
     * the only thing that matters in it is that the curved line skips the
     * convolutions entirely and lands on an addition. */
    function blockDiagram(st, bottleneck) {
        var W = 560, H = 250;
        var s = svg(W, H, "arch-svg-wide");
        var f = st.first, cx = 190;
        s.appendChild(rect(cx - 80, 8, 160, 24, { fill: A.SURFACE, stroke: A.BORDER }));
        s.appendChild(text(cx, 24, f.inCh + " x " + f.inSize + "x" + f.inSize,
            { size: 9.5, fill: A.MAIN }));

        var y = 46;
        var main = f.inner.filter(function (l) {
            return l.tag.indexOf("shortcut") === -1;
        });
        main.forEach(function (l) {
            s.appendChild(arrow(cx, y - 14, cx, y, { stroke: A.BORDER, sw: 1.1 }));
            s.appendChild(rect(cx - 80, y, 160, 30, { fill: A.SURFACE, stroke: A.BORDER }));
            s.appendChild(text(cx, y + 13, l.tag + ", " + l.co, { size: 9, fill: A.MAIN }));
            s.appendChild(text(cx, y + 25, "BN + ReLU  -  " + A.fmt(l.params) + " params",
                { size: 7.5, fill: A.MUTED }));
            s.appendChild(text(cx + 92, y + 18,
                l.co + " x " + l.out + "x" + l.out, { size: 8, fill: A.MUTED, anchor: "start" }));
            y += 46;
        });

        var addY = y + 8;
        s.appendChild(arrow(cx, y - 14, cx, addY - 10, { stroke: A.BORDER, sw: 1.1 }));
        s.appendChild(A.circle(cx, addY, 11, { stroke: A.ACCENT, sw: 1.8,
                                               fill: A.FILL, fo: 0.18 }));
        s.appendChild(text(cx, addY + 4, "+", { size: 14, fill: A.ACCENT }));

        /* the shortcut */
        var sx = cx - 150;
        s.appendChild(path("M" + cx + " 32 L" + sx + " 32 L" + sx + " " + addY +
                           " L" + (cx - 12) + " " + addY,
            { stroke: A.ACCENT, sw: 1.8, dash: f.shortcut ? "5 3" : null }));
        s.appendChild(text(sx - 6, (32 + addY) / 2,
            f.shortcut ? "1x1 /" + f.shortcut.stride + " projection" : "identity",
            { size: 9, fill: A.ACCENT, anchor: "end" }));
        if (f.shortcut)
            s.appendChild(text(sx - 6, (32 + addY) / 2 + 12,
                A.fmt(f.shortcut.params) + " params",
                { size: 7.5, fill: A.MUTED, anchor: "end" }));

        s.appendChild(arrow(cx, addY + 11, cx, addY + 26, { stroke: A.BORDER, sw: 1.1 }));
        s.appendChild(rect(cx - 80, addY + 28, 160, 24,
            { fill: A.FILL, fo: 0.16, stroke: A.ACCENT }));
        s.appendChild(text(cx, addY + 44, "ReLU  ->  " + f.outCh + " x " +
            f.outSize + "x" + f.outSize, { size: 9.5, fill: A.ACCENT }));

        s.appendChild(text(W - 12, 60,
            bottleneck ? "bottleneck block" : "basic block",
            { size: 10, fill: A.ACCENT, anchor: "end" }));
        s.appendChild(text(W - 12, 76,
            bottleneck ? "1x1 down, 3x3 at the narrow width, 1x1 back up"
                       : "two 3x3 convolutions at full width",
            { size: 8, fill: A.MUTED, anchor: "end" }));
        s.appendChild(text(W - 12, 92, A.fmt(f.params) + " parameters in this block",
            { size: 8, fill: A.MUTED, anchor: "end" }));
        s.appendChild(text(W - 12, 108, "x " + st.blocks + " blocks in stage " + st.idx,
            { size: 8, fill: A.MUTED, anchor: "end" }));
        return s;
    }

    A.WIDGETS.resnet = {
        controls: [
            { key: "depth", label: "Depth", type: "select", value: "50", id: "rn-depth",
              options: [
                  { value: "18", label: "ResNet-18  (basic blocks)" },
                  { value: "34", label: "ResNet-34  (basic blocks)" },
                  { value: "50", label: "ResNet-50  (bottleneck blocks)" },
                  { value: "101", label: "ResNet-101" },
                  { value: "152", label: "ResNet-152" }] },
            { key: "stage", label: "Open a block from stage", type: "select",
              value: "2", id: "rn-stage",
              options: [
                  { value: "1", label: "stage 1  (64 wide, 56x56)" },
                  { value: "2", label: "stage 2  (128 wide, 28x28)" },
                  { value: "3", label: "stage 3  (256 wide, 14x14)" },
                  { value: "4", label: "stage 4  (512 wide, 7x7)" }] },
            { key: "input", label: "Input resolution", type: "range",
              min: 128, max: 448, step: 32, value: 224, id: "rn-input",
              fmt: function (v) { return v + " x " + v; } }
        ],
        build: function (ctx) {
            return function draw() {
                var p = ctx.params;
                var m = model(p);
                var st = m.stages[parseInt(p.stage, 10) - 1] || m.stages[1];
                var depth = 1 + m.stages.reduce(function (a, s) {
                    return a + s.blocks * (m.bottleneck ? 3 : 2);
                }, 0) + 1;

                ctx.stage.innerHTML = "";
                var scroll = h("div", "arch-scroll");
                scroll.appendChild(blockDiagram(st, m.bottleneck));
                ctx.stage.appendChild(scroll);

                ctx.stage.appendChild(A.stats([
                    { value: A.fmt(m.params), label: "parameters",
                      note: A.commas(m.params) },
                    { value: A.fmt(m.macs), label: "MACs / image",
                      note: A.fmt(m.macs * 2) + " FLOPs" },
                    { value: depth, label: "weighted layers",
                      note: (m.bottleneck ? "3" : "2") + " convs per block" },
                    { value: m.finalCh + " x " + m.finalSize + "x" + m.finalSize,
                      label: "before the pool", note: "then GAP, then 1000" }
                ]));

                ctx.stage.appendChild(A.section("The four stages"));
                var rows = m.stages.map(function (s) {
                    return {
                        cells: ["stage " + s.idx + "  (" + s.blocks + " blocks)",
                                s.outCh + " x " + s.size + "x" + s.size,
                                A.fmt(s.params), A.fmt(s.macs),
                                s.first.shortcut ? "1x1 projection" : "identity"],
                        stage: s.idx === parseInt(p.stage, 10)
                    };
                });
                rows.push({ cells: ["stem  conv1 + max pool",
                                    "64 x " + m.stem[1].out + "x" + m.stem[1].out,
                                    A.fmt(m.stem[0].params), A.fmt(m.stem[0].macs),
                                    "-"] });
                rows.push({ cells: ["global average pool + fc",
                                    "1000", A.fmt(m.fc.params), A.fmt(m.fc.macs), "-"] });
                ctx.stage.appendChild(A.layerTable(
                    ["stage", "output", "params", "MACs", "shortcut"], rows, null, -1));

                ctx.stage.appendChild(A.section("Where the arithmetic goes"));
                ctx.stage.appendChild(A.bars(m.stages.map(function (s) {
                    return { label: "stage " + s.idx + " - " + s.size + "x" + s.size +
                                    ", " + s.outCh + " ch", value: s.macs,
                             hot: s.idx === parseInt(p.stage, 10) };
                }), { format: function (v) { return A.fmt(v) + " MACs"; } }));

                ctx.stage.appendChild(A.note(
                    "Each stage halves the map and doubles the width, so the MAC count " +
                    "per stage stays roughly level while the parameter count quadruples. " +
                    "That is deliberate: the early layers are cheap to store and expensive " +
                    "to run, the late layers the other way round."));

                ctx.setReadout("ResNet-" + p.depth + " at " + p.input + "x" + p.input +
                    ": " + A.commas(m.params) + " parameters, " + A.fmt(m.macs) +
                    " MACs, " + depth + " weighted layers");
            };
        }
    };
})();

/* ===========================================================================
 * U-Net
 *
 * Two things about U-Net are hard to get from the picture. The first is that
 * the skip connections are not decoration - remove them and the decoder is
 * asked to invent boundary detail that was thrown away by pooling, which it
 * cannot. The second is that the original network uses *unpadded*
 * convolutions, so 572x572 in gives 388x388 out and every skip has to be
 * cropped. Both are controls here.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, arrow = A.arrow, line = A.line;

    function model(p) {
        var valid = p.padding === "valid";
        var trim = valid ? 2 : 0;      /* per 3x3 conv, per side x2 */
        var levels = [], size = p.input, cin = p.inCh || 1, ch = p.base;
        var params = 0, macs = 0, i;

        function conv(a, b, k, sz) {
            var pr = b * a * k * k + b;
            params += pr;
            macs += b * sz * sz * a * k * k;
            return pr;
        }

        /* contracting path */
        for (i = 0; i < p.depth; i++) {
            var s1 = size - trim, s2 = s1 - trim;
            var pr = conv(cin, ch, 3, s1) + conv(ch, ch, 3, s2);
            levels.push({ level: i, ch: ch, inSize: size, convSize: s2,
                          poolSize: Math.floor(s2 / 2), params: pr });
            cin = ch;
            size = Math.floor(s2 / 2);
            ch *= 2;
        }
        /* the bottom */
        var b1 = size - trim, b2 = b1 - trim;
        var bottomP = conv(cin, ch, 3, b1) + conv(ch, ch, 3, b2);
        var bottom = { ch: ch, inSize: size, convSize: b2, params: bottomP };
        cin = ch; size = b2;

        /* expanding path */
        var ups = [];
        for (i = p.depth - 1; i >= 0; i--) {
            var skip = levels[i];
            var upCh = cin / 2;
            var upP = upCh * cin * 2 * 2 + upCh;   /* 2x2 transposed conv */
            params += upP;
            macs += upCh * (size * 2) * (size * 2) * cin * 4;
            size = size * 2;
            var concatCh = p.skips ? upCh + skip.ch : upCh;
            var crop = skip.convSize - size;
            var u1 = size - trim, u2 = u1 - trim;
            var cp = conv(concatCh, upCh, 3, u1) + conv(upCh, upCh, 3, u2);
            ups.push({ level: i, upCh: upCh, size: size, concatCh: concatCh,
                       crop: crop, outSize: u2, params: upP + cp,
                       skipCh: skip.ch });
            cin = upCh; size = u2;
        }
        var head = conv(cin, p.classes, 1, size);
        return { levels: levels, bottom: bottom, ups: ups, head: head,
                 outSize: size, params: params, macs: macs, valid: valid };
    }

    function diagram(m, p) {
        var W = 620, H = 60 + p.depth * 46 + 60;
        var s = svg(W, H, "arch-svg-wide");
        var lx = 70, rx = W - 70, i;

        for (i = 0; i < m.levels.length; i++) {
            var L = m.levels[i], U = m.ups[m.ups.length - 1 - i];
            var y = 34 + i * 46;
            var w = 96 - i * 8;
            /* encoder box */
            s.appendChild(rect(lx - w / 2, y, w, 26, { fill: A.SURFACE, stroke: A.BORDER }));
            s.appendChild(text(lx, y + 12, L.ch + " ch", { size: 9, fill: A.MAIN }));
            s.appendChild(text(lx, y + 22, L.convSize + "x" + L.convSize,
                { size: 7.5, fill: A.MUTED }));
            /* decoder box */
            s.appendChild(rect(rx - w / 2, y, w, 26, { fill: A.SURFACE, stroke: A.BORDER }));
            s.appendChild(text(rx, y + 12, U.upCh + " ch", { size: 9, fill: A.MAIN }));
            s.appendChild(text(rx, y + 22, U.outSize + "x" + U.outSize,
                { size: 7.5, fill: A.MUTED }));
            /* skip */
            if (p.skips) {
                s.appendChild(arrow(lx + w / 2 + 2, y + 13, rx - w / 2 - 2, y + 13,
                    { stroke: A.ACCENT, sw: 1.4, dash: m.valid ? "4 3" : null }));
                s.appendChild(text((lx + rx) / 2, y + 9,
                    "copy " + L.ch + " ch" + (m.valid && U.crop > 0
                        ? ", crop " + L.convSize + " -> " + U.size : ""),
                    { size: 7.5, fill: A.ACCENT }));
            } else {
                s.appendChild(text((lx + rx) / 2, y + 17, "skip removed",
                    { size: 7.5, fill: A.MUTED, opacity: 0.6 }));
            }
            /* down / up arrows */
            if (i < m.levels.length) {
                s.appendChild(arrow(lx, y + 26, lx, y + 46, { stroke: A.BORDER, sw: 1.1 }));
                s.appendChild(text(lx - 34, y + 40, "pool /2",
                    { size: 7, fill: A.MUTED, anchor: "end" }));
                s.appendChild(arrow(rx, y + 46, rx, y + 26, { stroke: A.BORDER, sw: 1.1 }));
                s.appendChild(text(rx + 34, y + 40, "up x2",
                    { size: 7, fill: A.MUTED, anchor: "start" }));
            }
        }
        var by = 34 + p.depth * 46;
        s.appendChild(rect((lx + rx) / 2 - 90, by, 180, 28,
            { fill: A.FILL, fo: 0.16, stroke: A.ACCENT }));
        s.appendChild(text((lx + rx) / 2, by + 13, "bottom  " + m.bottom.ch + " channels",
            { size: 9.5, fill: A.ACCENT }));
        s.appendChild(text((lx + rx) / 2, by + 24,
            m.bottom.convSize + "x" + m.bottom.convSize + "  -  " +
            A.fmt(m.bottom.params) + " params here alone", { size: 7.5, fill: A.MUTED }));

        s.appendChild(text(lx, 22, "contracting", { size: 9, fill: A.MUTED }));
        s.appendChild(text(rx, 22, "expanding", { size: 9, fill: A.MUTED }));
        s.appendChild(text(W / 2, H - 8,
            "input " + p.input + "x" + p.input + "  ->  output " + m.outSize + "x" +
            m.outSize + (m.valid ? "  (unpadded convolutions shrink every map)" : ""),
            { size: 8.5, fill: A.MUTED }));
        return s;
    }

    A.WIDGETS.unet = {
        controls: [
            { key: "input", label: "Input tile", type: "range",
              min: 128, max: 640, step: 4, value: 572, id: "unet-input",
              fmt: function (v) { return v + " x " + v; } },
            { key: "depth", label: "Levels (times it halves)", type: "range",
              min: 2, max: 5, step: 1, value: 4, id: "unet-depth" },
            { key: "base", label: "Channels at the top", type: "select",
              value: "64", id: "unet-base",
              options: [{ value: "16", label: "16  (a small U-Net)" },
                        { value: "32", label: "32" },
                        { value: "64", label: "64  (the paper)" }] },
            { key: "padding", label: "Convolution padding", type: "select",
              value: "valid", id: "unet-padding",
              options: [{ value: "valid", label: "valid - the original, output shrinks" },
                        { value: "same", label: "same - what most code does" }] },
            { key: "skips", label: "Skip connections", type: "toggle",
              value: true, id: "unet-skips" }
        ],
        build: function (ctx) {
            return function draw() {
                var p = {
                    input: ctx.params.input,
                    depth: ctx.params.depth,
                    base: parseInt(ctx.params.base, 10),
                    padding: ctx.params.padding,
                    skips: ctx.params.skips,
                    classes: 2, inCh: 1
                };
                var m = model(p);
                var withSkips = model({ input: p.input, depth: p.depth, base: p.base,
                                        padding: p.padding, skips: true,
                                        classes: 2, inCh: 1 });
                var lost = p.input * p.input - m.outSize * m.outSize;

                ctx.stage.innerHTML = "";
                if (m.outSize < 4) {
                    ctx.stage.appendChild(A.note(
                        "At " + p.input + "x" + p.input + " with " + p.depth +
                        " levels of unpadded convolutions the map runs out before the " +
                        "bottom. That is a real constraint of the original design: the " +
                        "input tile has to be chosen so every pooling step divides evenly. " +
                        "Raise the tile size or drop a level."));
                    ctx.setReadout("tile too small for " + p.depth + " levels");
                    return;
                }
                var scroll = h("div", "arch-scroll");
                scroll.appendChild(diagram(m, p));
                ctx.stage.appendChild(scroll);

                ctx.stage.appendChild(A.stats([
                    { value: A.fmt(m.params), label: "parameters",
                      note: A.commas(m.params) },
                    { value: A.fmt(m.macs), label: "MACs / tile",
                      note: "at " + p.input + "x" + p.input },
                    { value: m.outSize + " x " + m.outSize, label: "output map",
                      note: m.valid ? A.commas(lost) + " pixels lost at the border"
                                    : "same size as the input" },
                    { value: m.bottom.ch, label: "widest layer",
                      note: "at " + m.bottom.convSize + "x" + m.bottom.convSize }
                ]));

                ctx.stage.appendChild(A.section("Level by level"));
                var rows = m.levels.map(function (L, i) {
                    var U = m.ups[m.ups.length - 1 - i];
                    return { cells: [
                        "level " + (i + 1),
                        L.ch + " ch @ " + L.convSize + "x" + L.convSize,
                        p.skips ? (m.valid && U.crop > 0
                                     ? L.ch + " ch, cropped " + U.crop + " px"
                                     : L.ch + " ch, copied whole")
                                : "none",
                        U.concatCh + " -> " + U.upCh + " ch",
                        A.fmt(L.params + U.params)] };
                });
                rows.push({ cells: ["bottom", m.bottom.ch + " ch @ " +
                                    m.bottom.convSize + "x" + m.bottom.convSize,
                                    "-", "-", A.fmt(m.bottom.params)], stage: true });
                ctx.stage.appendChild(A.layerTable(
                    ["level", "encoder", "skip carries", "decoder input", "params"],
                    rows, null, -1));

                ctx.stage.appendChild(A.section("What the skips cost, and what they carry"));
                ctx.stage.appendChild(A.bars([
                    { label: "with skip connections", value: withSkips.params, hot: p.skips },
                    { label: "without them", value: model({
                        input: p.input, depth: p.depth, base: p.base,
                        padding: p.padding, skips: false, classes: 2, inCh: 1 }).params,
                      hot: !p.skips }
                ], { format: function (v) { return A.fmt(v) + " params"; } }));

                ctx.stage.appendChild(A.note(p.skips
                    ? "Each skip doubles the channel count entering the decoder block, " +
                      "which is why turning them off saves parameters. It is a bad trade: " +
                      "the pooled path knows <em>what</em> is in the tile and has lost " +
                      "<em>where</em>, and only the skip still holds the boundary at full " +
                      "resolution."
                    : "With the skips off, the finest spatial detail the decoder can draw " +
                      "on is whatever survived " + p.depth + " rounds of pooling &mdash; a " +
                      m.bottom.convSize + "&times;" + m.bottom.convSize + " map. The mask " +
                      "comes back blobby, and no amount of decoder capacity fixes it, " +
                      "because the information is gone rather than hidden."));

                if (m.valid)
                    ctx.stage.appendChild(A.note(
                        "Unpadded convolutions are why the paper predicts on <em>tiles</em> " +
                        "with overlap rather than on a whole image: every 3&times;3 " +
                        "convolution eats one pixel from each border, so the network only " +
                        "outputs a mask for the region it saw full context for. " +
                        p.input + "&times;" + p.input + " in, " + m.outSize + "&times;" +
                        m.outSize + " out."));

                ctx.setReadout(p.input + "x" + p.input + " tile, " + p.depth +
                    " levels, base " + p.base + ", " + p.padding + " padding, skips " +
                    (p.skips ? "on" : "off") + ": " + A.commas(m.params) +
                    " parameters, output " + m.outSize + "x" + m.outSize);
            };
        }
    };
})();

/* ===========================================================================
 * Haar cascade detection
 *
 * Viola-Jones is three ideas, and only the third is usually explained. The
 * features are rectangle differences; the integral image makes any rectangle
 * sum cost four lookups no matter how large it is; and the cascade spends
 * almost nothing on the 99.9% of windows that are obviously not faces.
 *
 * The image here is drawn in code so it can be built to contain exactly the
 * structure the classic features were designed to find: an eye band darker
 * than the cheeks below it, and a nose bridge lighter than the eyes on either
 * side. Drag the feature over those and the response is large; drag it onto
 * the flat background and it collapses. That is the entire feature.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text;

    var IW = 256, IH = 192;

    /* A face-like intensity field. Deliberately not a photograph: every
     * structure in it is one the Haar features were designed to catch. */
    function scene() {
        var g = new Float32Array(IW * IH), x, y;
        var r = A.rng(7);
        for (y = 0; y < IH; y++) for (x = 0; x < IW; x++) {
            var v = 62 + 10 * Math.sin(x * 0.05) + 6 * r();
            g[y * IW + x] = v;
        }
        function ell(cx, cy, rx, ry, val, soft) {
            for (y = 0; y < IH; y++) for (x = 0; x < IW; x++) {
                var dx = (x - cx) / rx, dy = (y - cy) / ry;
                var d = dx * dx + dy * dy;
                if (d <= 1) {
                    var w = soft ? (1 - d) : 1;
                    var i = y * IW + x;
                    g[i] = g[i] * (1 - w) + val * w;
                }
            }
        }
        function box(x0, y0, w, hh, val) {
            for (y = y0; y < y0 + hh; y++) for (x = x0; x < x0 + w; x++)
                if (x >= 0 && y >= 0 && x < IW && y < IH) g[y * IW + x] = val;
        }
        ell(128, 98, 58, 74, 176, true);      /* the face, lit */
        box(92, 74, 26, 12, 58);              /* left eye */
        box(140, 74, 26, 12, 58);             /* right eye */
        box(120, 70, 16, 34, 198);            /* nose bridge, bright */
        box(108, 132, 40, 9, 74);             /* mouth */
        ell(128, 46, 52, 22, 205, true);      /* forehead highlight */
        for (var i = 0; i < g.length; i++) g[i] = Math.max(0, Math.min(255, g[i]));
        return g;
    }

    /* The integral image, and the four-lookup sum it exists for. */
    function integral(g) {
        var ii = new Float64Array((IW + 1) * (IH + 1));
        for (var y = 1; y <= IH; y++) {
            var rowsum = 0;
            for (var x = 1; x <= IW; x++) {
                rowsum += g[(y - 1) * IW + (x - 1)];
                ii[y * (IW + 1) + x] = ii[(y - 1) * (IW + 1) + x] + rowsum;
            }
        }
        return ii;
    }

    function boxSum(ii, x0, y0, w, hh) {
        var x1 = Math.min(IW, x0 + w), y1 = Math.min(IH, y0 + hh);
        x0 = Math.max(0, x0); y0 = Math.max(0, y0);
        var S = IW + 1;
        var D = ii[y1 * S + x1], B = ii[y0 * S + x1];
        var C = ii[y1 * S + x0], Aa = ii[y0 * S + x0];
        return { sum: D - B - C + Aa, D: D, B: B, C: C, A: Aa,
                 n: Math.max(1, (x1 - x0) * (y1 - y0)) };
    }

    /* The five prototypes from the paper, as (x, y, w, h, sign) in units of
     * the feature box. Sign +1 is the light half, -1 the dark half. */
    var FEATURES = {
        edge_v: { label: "two-rectangle, stacked - a horizontal edge",
                  parts: [[0, 0, 1, 0.5, -1], [0, 0.5, 1, 0.5, 1]] },
        edge_h: { label: "two-rectangle, side by side - a vertical edge",
                  parts: [[0, 0, 0.5, 1, 1], [0.5, 0, 0.5, 1, -1]] },
        line_h: { label: "three-rectangle - a light band between two dark ones",
                  parts: [[0, 0, 1 / 3, 1, -1], [1 / 3, 0, 1 / 3, 1, 1],
                          [2 / 3, 0, 1 / 3, 1, -1]] },
        line_v: { label: "three-rectangle, stacked",
                  parts: [[0, 0, 1, 1 / 3, -1], [0, 1 / 3, 1, 1 / 3, 1],
                          [0, 2 / 3, 1, 1 / 3, -1]] },
        four: { label: "four-rectangle - a diagonal structure",
                parts: [[0, 0, 0.5, 0.5, 1], [0.5, 0, 0.5, 0.5, -1],
                        [0, 0.5, 0.5, 0.5, -1], [0.5, 0.5, 0.5, 0.5, 1]] }
    };

    /* Viola-Jones, table 2 and section 5: 38 stages, 6061 features, and a
     * first stage of two features that discards about half of everything. */
    var CASCADE = [
        { stage: 1, feats: 2, pass: 0.50 },
        { stage: 2, feats: 10, pass: 0.40 },
        { stage: 3, feats: 25, pass: 0.30 },
        { stage: 4, feats: 25, pass: 0.30 },
        { stage: 5, feats: 50, pass: 0.30 },
        { stage: 6, feats: 50, pass: 0.35 },
        { stage: 7, feats: 100, pass: 0.35 },
        { stage: 8, feats: 200, pass: 0.40 }
    ];

    A.WIDGETS.haar = {
        controls: [
            { key: "feature", label: "Feature", type: "select", value: "edge_v",
              id: "haar-feature",
              options: Object.keys(FEATURES).map(function (k) {
                  return { value: k, label: FEATURES[k].label };
              }) },
            { key: "fw", label: "Feature width", type: "range",
              min: 12, max: 120, step: 2, value: 72, id: "haar-fw",
              fmt: function (v) { return v + " px"; } },
            { key: "fh", label: "Feature height", type: "range",
              min: 8, max: 120, step: 2, value: 36, id: "haar-fh",
              fmt: function (v) { return v + " px"; } },
            { key: "stages", label: "Cascade stages evaluated", type: "range",
              min: 1, max: 8, step: 1, value: 8, id: "haar-stages" }
        ],
        build: function (ctx) {
            var g = scene(), ii = integral(g);
            var pos = { x: 92, y: 68 };

            var canvas = h("canvas", "arch-canvas vz-touch-surface");
            canvas.width = IW; canvas.height = IH;
            var overlay = null;

            function toLocal(ev) {
                var r = canvas.getBoundingClientRect();
                return {
                    x: Math.round((ev.clientX - r.left) / r.width * IW),
                    y: Math.round((ev.clientY - r.top) / r.height * IH)
                };
            }
            function place(ev) {
                var p = toLocal(ev);
                pos.x = A.clamp(p.x - ctx.params.fw / 2, 0, IW - ctx.params.fw);
                pos.y = A.clamp(p.y - ctx.params.fh / 2, 0, IH - ctx.params.fh);
                ctx.redraw();
            }
            A.drag(canvas, place);

            function paint() {
                var cx = canvas.getContext("2d");
                var id = cx.createImageData(IW, IH);
                for (var i = 0; i < IW * IH; i++) {
                    var v = g[i];
                    id.data[i * 4] = v; id.data[i * 4 + 1] = v;
                    id.data[i * 4 + 2] = v; id.data[i * 4 + 3] = 255;
                }
                cx.putImageData(id, 0, 0);
            }

            return function draw() {
                var p = ctx.params;
                pos.x = A.clamp(pos.x, 0, IW - p.fw);
                pos.y = A.clamp(pos.y, 0, IH - p.fh);
                paint();

                var f = FEATURES[p.feature];
                var light = 0, dark = 0, lightN = 0, darkN = 0, parts = [];
                f.parts.forEach(function (q) {
                    var rx = Math.round(pos.x + q[0] * p.fw);
                    var ry = Math.round(pos.y + q[1] * p.fh);
                    var rw = Math.round(q[2] * p.fw), rh = Math.round(q[3] * p.fh);
                    var s = boxSum(ii, rx, ry, rw, rh);
                    parts.push({ x: rx, y: ry, w: rw, h: rh, sign: q[4], s: s });
                    if (q[4] > 0) { light += s.sum; lightN += s.n; }
                    else { dark += s.sum; darkN += s.n; }
                });
                /* Means, not raw sums: the halves of a three-rectangle feature
                 * are not the same area, and comparing raw sums would make the
                 * answer depend on the shape rather than the image. */
                var meanL = light / Math.max(1, lightN), meanD = dark / Math.max(1, darkN);
                var response = meanL - meanD;

                ctx.stage.innerHTML = "";
                var wrap = h("div", "arch-canvas-wrap");
                wrap.appendChild(canvas);
                var ov = svg(IW, IH, "arch-overlay");
                ov.setAttribute("viewBox", "0 0 " + IW + " " + IH);
                parts.forEach(function (q) {
                    ov.appendChild(rect(q.x, q.y, q.w, q.h, {
                        fill: q.sign > 0 ? "#ffffff" : "#000000",
                        fo: 0.55, stroke: A.ACCENT, sw: 1, rx: 0
                    }));
                });
                ov.appendChild(rect(pos.x - 1, pos.y - 1, p.fw + 2, p.fh + 2,
                    { stroke: A.ACCENT, sw: 1.6, rx: 0 }));
                wrap.appendChild(ov);
                ctx.stage.appendChild(wrap);
                ctx.stage.appendChild(A.caption(
                    "Drag the feature anywhere on the image. White rectangles are added, " +
                    "black ones subtracted."));

                ctx.stage.appendChild(A.stats([
                    { value: Math.round(meanL), label: "mean under white",
                      note: A.commas(Math.round(light)) + " total" },
                    { value: Math.round(meanD), label: "mean under black",
                      note: A.commas(Math.round(dark)) + " total" },
                    { value: (response >= 0 ? "+" : "") + response.toFixed(1),
                      label: "feature response",
                      note: Math.abs(response) > 40 ? "a strong edge"
                            : (Math.abs(response) > 15 ? "some structure" : "nearly flat") },
                    { value: parts.length * 4, label: "array lookups",
                      note: "regardless of feature size" }
                ]));

                /* the integral-image arithmetic for the first rectangle */
                var q0 = parts[0];
                ctx.stage.appendChild(A.section("How that rectangle sum was computed"));
                ctx.stage.appendChild(A.note(
                    "The first rectangle is " + q0.w + "&times;" + q0.h + " = " +
                    A.commas(q0.w * q0.h) + " pixels, and none of them were read. " +
                    "The integral image holds, at every point, the sum of everything above " +
                    "and to its left, so the sum inside any rectangle is four lookups:<br>" +
                    "<span class='arch-mono'>D &minus; B &minus; C + A = " +
                    A.commas(Math.round(q0.s.D)) + " &minus; " +
                    A.commas(Math.round(q0.s.B)) + " &minus; " +
                    A.commas(Math.round(q0.s.C)) + " + " +
                    A.commas(Math.round(q0.s.A)) + " = <strong>" +
                    A.commas(Math.round(q0.s.sum)) + "</strong></span><br>" +
                    "A rectangle ten times the area costs exactly the same four lookups. " +
                    "That is what makes evaluating thousands of features per window, at " +
                    "every scale, affordable at all."));

                /* the cascade */
                var stages = CASCADE.slice(0, p.stages);
                var windows = 1, surviving = [], evaluated = 0, feats = 0;
                var start = 24000;
                var live = start;
                stages.forEach(function (s) {
                    evaluated += live * s.feats;
                    feats += s.feats;
                    live = live * s.pass;
                    surviving.push({ label: "after stage " + s.stage +
                                     "  (" + s.feats + " features)", value: live });
                });
                var naive = start * feats;
                ctx.stage.appendChild(A.section("The cascade, on 24,000 candidate windows"));
                ctx.stage.appendChild(A.bars(
                    [{ label: "windows entering stage 1", value: start }].concat(surviving),
                    { format: function (v) { return A.commas(Math.round(v)); } }));
                ctx.stage.appendChild(A.note(
                    "Evaluating all " + feats + " features on every window would be " +
                    A.fmt(naive) + " feature evaluations. Ordering them as a cascade, so a " +
                    "window is dropped the moment a cheap stage rejects it, costs " +
                    A.fmt(evaluated) + " &mdash; <strong>" +
                    (naive / evaluated).toFixed(1) + "&times;</strong> less. The real " +
                    "detector has 38 stages and 6,061 features, and the average window is " +
                    "rejected after about ten of them."));

                ctx.setReadout(f.label + " at (" + Math.round(pos.x) + ", " +
                    Math.round(pos.y) + "), " + p.fw + "x" + p.fh + ": response " +
                    (response >= 0 ? "+" : "") + response.toFixed(1));
            };
        }
    };
})();

/* ===========================================================================
 * YOLO v8
 *
 * A one-stage detector emits every box it will ever consider in a single
 * forward pass - 8,400 of them at 640x640 - and then throws almost all of
 * them away. The interesting part is the throwing away, because the two
 * numbers that control it are the two numbers people get wrong: the
 * confidence threshold and the NMS IoU threshold. Both are sliders here, over
 * a fixed set of raw predictions, so the effect of each is separable.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, line = A.line;

    var VW = 320, VH = 240;

    var SCENES = [
        { name: "three objects, well separated", seed: 11, objs: [
            { x: 30, y: 60, w: 62, h: 130, cls: "person", conf: 0.93 },
            { x: 150, y: 120, w: 130, h: 72, cls: "car", conf: 0.88 },
            { x: 190, y: 30, w: 58, h: 46, cls: "dog", conf: 0.71 }] },
        { name: "two overlapping people", seed: 23, objs: [
            { x: 84, y: 52, w: 70, h: 150, cls: "person", conf: 0.91 },
            { x: 122, y: 62, w: 70, h: 142, cls: "person", conf: 0.84 },
            { x: 232, y: 130, w: 72, h: 56, cls: "car", conf: 0.66 }] },
        { name: "a crowd - where NMS starts to hurt", seed: 41, objs: [
            { x: 24, y: 70, w: 52, h: 120, cls: "person", conf: 0.90 },
            { x: 62, y: 66, w: 52, h: 126, cls: "person", conf: 0.87 },
            { x: 100, y: 72, w: 52, h: 120, cls: "person", conf: 0.83 },
            { x: 140, y: 68, w: 52, h: 124, cls: "person", conf: 0.79 },
            { x: 200, y: 96, w: 96, h: 74, cls: "car", conf: 0.75 }] }
    ];

    function iou(a, b) {
        var x0 = Math.max(a.x, b.x), y0 = Math.max(a.y, b.y);
        var x1 = Math.min(a.x + a.w, b.x + b.w), y1 = Math.min(a.y + a.h, b.y + b.h);
        var inter = Math.max(0, x1 - x0) * Math.max(0, y1 - y0);
        var uni = a.w * a.h + b.w * b.h - inter;
        return uni > 0 ? inter / uni : 0;
    }

    /* The raw head output, faked but with the right statistics: a cluster of
     * near-duplicate boxes around every object, plus a tail of low-confidence
     * background boxes. A real head gives exactly this shape. */
    function predictions(scene) {
        var r = A.rng(scene.seed), out = [];
        scene.objs.forEach(function (o, oi) {
            var n = 9 + Math.floor(r() * 7);
            for (var i = 0; i < n; i++) {
                var jx = (r() - 0.5) * o.w * 0.34, jy = (r() - 0.5) * o.h * 0.34;
                var jw = 1 + (r() - 0.5) * 0.3, jh = 1 + (r() - 0.5) * 0.3;
                var d = Math.abs(jx) / o.w + Math.abs(jy) / o.h +
                        Math.abs(jw - 1) + Math.abs(jh - 1);
                out.push({
                    x: o.x + jx, y: o.y + jy, w: o.w * jw, h: o.h * jh,
                    cls: o.cls, obj: oi,
                    conf: A.clamp(o.conf * Math.exp(-2.1 * d) + 0.02 * r(), 0.02, 0.99)
                });
            }
        });
        for (var i = 0; i < 26; i++) {
            out.push({
                x: r() * (VW - 50), y: r() * (VH - 50),
                w: 22 + r() * 70, h: 22 + r() * 70,
                cls: ["person", "car", "dog"][Math.floor(r() * 3)],
                obj: -1, conf: 0.03 + r() * 0.26
            });
        }
        return out.sort(function (a, b) { return b.conf - a.conf; });
    }

    function nms(boxes, thr) {
        var keep = [], sup = [];
        boxes.forEach(function (b) {
            for (var i = 0; i < keep.length; i++) {
                if (keep[i].cls === b.cls && iou(keep[i], b) > thr) {
                    sup.push(b); return;
                }
            }
            keep.push(b);
        });
        return { keep: keep, sup: sup };
    }

    var CLS_COLOR = { person: "var(--accent-primary)", car: A.SERIES2, dog: A.SERIES3 };

    A.WIDGETS.yolo = {
        controls: [
            { key: "scene", label: "Scene", type: "select", value: "0", id: "yolo-scene",
              options: SCENES.map(function (s, i) {
                  return { value: String(i), label: s.name }; }) },
            { key: "conf", label: "Confidence threshold", type: "range",
              min: 0.02, max: 0.9, step: 0.01, value: 0.25, id: "yolo-conf",
              fmt: function (v) { return v.toFixed(2); } },
            { key: "iou", label: "NMS IoU threshold", type: "range",
              min: 0.1, max: 0.95, step: 0.05, value: 0.7, id: "yolo-iou",
              fmt: function (v) { return v.toFixed(2); } },
            { key: "nms", label: "Non-maximum suppression", type: "toggle",
              value: true, id: "yolo-nms" },
            { key: "grid", label: "Show the prediction grid", type: "select",
              value: "none", id: "yolo-grid",
              options: [{ value: "none", label: "off" },
                        { value: "8", label: "P3 - stride 8, 80x80 cells" },
                        { value: "16", label: "P4 - stride 16, 40x40 cells" },
                        { value: "32", label: "P5 - stride 32, 20x20 cells" }] }
        ],
        build: function (ctx) {
            return function draw() {
                var p = ctx.params;
                var scene = SCENES[parseInt(p.scene, 10)] || SCENES[0];
                var raw = predictions(scene);
                var above = raw.filter(function (b) { return b.conf >= p.conf; });
                var res = p.nms ? nms(above, p.iou) : { keep: above, sup: [] };

                ctx.stage.innerHTML = "";
                var s = svg(VW, VH, "arch-scene");
                s.appendChild(rect(0, 0, VW, VH, { fill: A.SURFACE, stroke: A.BORDER, rx: 4 }));

                /* the grid, at the chosen stride, scaled to this canvas */
                if (p.grid !== "none") {
                    var stride = parseInt(p.grid, 10);
                    var cell = stride * VW / 640;
                    for (var gx = cell; gx < VW; gx += cell)
                        s.appendChild(line(gx, 0, gx, VH,
                            { stroke: A.BORDER, sw: 0.4, opacity: 0.7 }));
                    for (var gy = cell; gy < VH; gy += cell)
                        s.appendChild(line(0, gy, VW, gy,
                            { stroke: A.BORDER, sw: 0.4, opacity: 0.7 }));
                }

                /* ground truth, faint, so a reader can see what the boxes chase */
                scene.objs.forEach(function (o) {
                    s.appendChild(rect(o.x, o.y, o.w, o.h,
                        { stroke: A.MUTED, sw: 1, dash: "3 3", opacity: 0.5 }));
                });
                /* suppressed and below-threshold boxes */
                if (p.nms) res.sup.forEach(function (b) {
                    s.appendChild(rect(b.x, b.y, b.w, b.h,
                        { stroke: A.MUTED, sw: 0.7, opacity: 0.28 }));
                });
                res.keep.forEach(function (b) {
                    s.appendChild(rect(b.x, b.y, b.w, b.h, {
                        stroke: CLS_COLOR[b.cls] || A.ACCENT, sw: 1.8,
                        fill: CLS_COLOR[b.cls] || A.ACCENT, fo: 0.07
                    }));
                    s.appendChild(text(b.x + 2, b.y - 3, b.cls + " " + b.conf.toFixed(2),
                        { size: 8, anchor: "start", fill: CLS_COLOR[b.cls] || A.ACCENT }));
                });
                var wrap = h("div", "arch-scroll");
                wrap.appendChild(s);
                ctx.stage.appendChild(wrap);
                ctx.stage.appendChild(A.caption(
                    "Dashed grey: the true objects. Faint: boxes the head produced and the " +
                    "filters discarded. Solid: what the detector returns."));

                var found = {}, dup = 0;
                res.keep.forEach(function (b) {
                    if (b.obj < 0) return;
                    if (found[b.obj]) dup++; else found[b.obj] = 1;
                });
                var missed = scene.objs.length - Object.keys(found).length;
                var ghosts = res.keep.filter(function (b) { return b.obj < 0; }).length;

                ctx.stage.appendChild(A.stats([
                    { value: raw.length, label: "raw predictions kept here",
                      note: "8,400 in the real head" },
                    { value: above.length, label: "survive the confidence cut",
                      note: "at " + p.conf.toFixed(2) },
                    { value: res.keep.length, label: "survive NMS",
                      note: p.nms ? "IoU > " + p.iou.toFixed(2) + " suppressed"
                                  : "NMS is off" },
                    { value: missed + " / " + dup + " / " + ghosts,
                      label: "missed / duplicate / false",
                      note: missed || dup || ghosts ? "not a clean detection"
                                                    : "one box per object" }
                ]));

                ctx.stage.appendChild(A.note(
                    p.conf > 0.55
                        ? "A high confidence threshold is the quiet way to lose objects. " +
                          "Every box below it is gone before NMS ever sees it, and a hard " +
                          "example - small, occluded, unusual pose - is exactly the one " +
                          "with a low score."
                        : (p.iou < 0.35
                            ? "A low NMS IoU threshold suppresses aggressively. Two people " +
                              "standing close genuinely overlap by more than this, so the " +
                              "second one is deleted as a duplicate of the first."
                            : (p.nms
                                ? "The head emits a cluster of near-identical boxes per " +
                                  "object because several nearby cells all decide the object " +
                                  "is theirs. NMS keeps the highest-scoring one and deletes " +
                                  "anything overlapping it by more than " + p.iou.toFixed(2) + "."
                                : "With NMS off you are looking at what the network actually " +
                                  "outputs: every confident cell reports the object it can " +
                                  "see, and nothing reconciles them."))));

                ctx.stage.appendChild(A.section("Where the 8,400 predictions come from"));
                ctx.stage.appendChild(A.layerTable(
                    ["level", "stride", "grid", "predictions", "detects objects of size"],
                    [{ cells: ["P3", "8", "80 x 80", A.commas(6400), "roughly 8-64 px"],
                       stage: p.grid === "8" },
                     { cells: ["P4", "16", "40 x 40", A.commas(1600), "roughly 32-192 px"],
                       stage: p.grid === "16" },
                     { cells: ["P5", "32", "20 x 20", A.commas(400), "192 px and up"],
                       stage: p.grid === "32" },
                     { cells: ["total", "-", "-", A.commas(8400),
                               "one prediction per cell, no anchors"] }],
                    null, -1));

                ctx.stage.appendChild(A.section("The head, per cell"));
                ctx.stage.appendChild(A.note(
                    "v8 is <strong>anchor-free</strong> and <strong>decoupled</strong>. Each " +
                    "cell predicts, from two separate branches, a class vector of length " +
                    "<span class='arch-mono'>nc</span> and a box as four distributions of " +
                    "16 bins each &mdash; <span class='arch-mono'>4 &times; 16 = 64</span> " +
                    "channels &mdash; over the distance from the cell centre to each of the " +
                    "four edges. The distribution is collapsed to a number by taking its " +
                    "expectation, which is what the DFL loss trains. There is no objectness " +
                    "score and no anchor box: the older versions needed anchors precisely " +
                    "because the box was predicted as an offset from one."));

                ctx.setReadout(scene.objs.length + " objects, " + raw.length +
                    " raw boxes -> " + above.length + " above " + p.conf.toFixed(2) +
                    " -> " + res.keep.length + " after " +
                    (p.nms ? "NMS at IoU " + p.iou.toFixed(2) : "no NMS") +
                    (p.grid === "none" ? ""
                        : "; grid shown at stride " + p.grid));
            };
        }
    };
})();

/* ===========================================================================
 * Mask R-CNN, and the RoIAlign that made it work
 *
 * Mask R-CNN is Faster R-CNN plus a third head. The paper's own ablation says
 * the third head only works because of one change: RoIPool rounds the region
 * of interest to whole feature cells twice, and at stride 16 a rounding error
 * of half a cell is eight input pixels. Classification never noticed. A mask,
 * which is a per-pixel answer, notices immediately.
 *
 * So the whole misalignment is drawn: the true region, the rounded one, the
 * bins, the sample points, and the two pooled outputs side by side.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, circle = A.circle, line = A.line;

    var FM = 16;   /* the feature map is FM x FM cells */

    /* A smooth feature-map channel: something with structure, so pooling it
     * two different ways gives two different answers. */
    function featureMap() {
        var m = new Float64Array(FM * FM);
        for (var y = 0; y < FM; y++) for (var x = 0; x < FM; x++) {
            var a = Math.exp(-(Math.pow(x - 6.3, 2) + Math.pow(y - 7.1, 2)) / 9);
            var b = 0.6 * Math.exp(-(Math.pow(x - 10.7, 2) + Math.pow(y - 5.4, 2)) / 5);
            var c = 0.25 * Math.sin(x * 0.9) * Math.cos(y * 0.7);
            m[y * FM + x] = A.clamp(a + b + c + 0.15, 0, 1.4);
        }
        return m;
    }

    function at(m, x, y) {
        x = A.clamp(x, 0, FM - 1); y = A.clamp(y, 0, FM - 1);
        return m[Math.round(y) * FM + Math.round(x)];
    }

    /* Bilinear read at a fractional location - the operation RoIAlign adds
     * and RoIPool does not have. */
    function bilinear(m, x, y) {
        x = A.clamp(x, 0, FM - 1); y = A.clamp(y, 0, FM - 1);
        var x0 = Math.floor(x), y0 = Math.floor(y);
        var x1 = Math.min(FM - 1, x0 + 1), y1 = Math.min(FM - 1, y0 + 1);
        var fx = x - x0, fy = y - y0;
        return m[y0 * FM + x0] * (1 - fx) * (1 - fy) +
               m[y0 * FM + x1] * fx * (1 - fy) +
               m[y1 * FM + x0] * (1 - fx) * fy +
               m[y1 * FM + x1] * fx * fy;
    }

    function roiPool(m, roi, bins) {
        /* Quantisation one: the region snaps to whole cells. */
        var x0 = Math.floor(roi.x), y0 = Math.floor(roi.y);
        var x1 = Math.floor(roi.x + roi.w), y1 = Math.floor(roi.y + roi.h);
        var w = Math.max(1, x1 - x0), hh = Math.max(1, y1 - y0);
        var out = new Float64Array(bins * bins);
        for (var by = 0; by < bins; by++) for (var bx = 0; bx < bins; bx++) {
            /* Quantisation two: the bin edges snap as well. */
            var sx = x0 + Math.floor(bx * w / bins), ex = x0 + Math.ceil((bx + 1) * w / bins);
            var sy = y0 + Math.floor(by * hh / bins), ey = y0 + Math.ceil((by + 1) * hh / bins);
            var best = -1e9;
            for (var y = sy; y < Math.max(sy + 1, ey); y++)
                for (var x = sx; x < Math.max(sx + 1, ex); x++)
                    best = Math.max(best, at(m, x, y));
            out[by * bins + bx] = best;
        }
        return { out: out, snapped: { x: x0, y: y0, w: w, h: hh } };
    }

    function roiAlign(m, roi, bins) {
        var out = new Float64Array(bins * bins), samples = [];
        var bw = roi.w / bins, bh = roi.h / bins;
        for (var by = 0; by < bins; by++) for (var bx = 0; bx < bins; bx++) {
            var acc = 0;
            for (var iy = 0; iy < 2; iy++) for (var ix = 0; ix < 2; ix++) {
                var sx = roi.x + bx * bw + (ix + 0.5) * bw / 2;
                var sy = roi.y + by * bh + (iy + 0.5) * bh / 2;
                acc += bilinear(m, sx - 0.5, sy - 0.5);
                if (bins <= 7) samples.push({ x: sx, y: sy });
            }
            out[by * bins + bx] = acc / 4;
        }
        return { out: out, samples: samples };
    }

    function heat(vals, bins, size, label, max) {
        var pad = 14;
        var s = svg(size, size + pad + 4, "arch-heat");
        var cell = size / bins;
        for (var y = 0; y < bins; y++) for (var x = 0; x < bins; x++) {
            var v = vals[y * bins + x] / (max || 1);
            s.appendChild(rect(x * cell, pad + y * cell, cell, cell, {
                fill: A.FILL, fo: A.clamp(v, 0, 1), stroke: A.BORDER, sw: 0.4, rx: 0
            }));
        }
        s.appendChild(text(size / 2, 10, label, { size: 8.5, fill: A.MUTED }));
        return s;
    }

    A.WIDGETS.maskrcnn = {
        controls: [
            { key: "stride", label: "Backbone stride at this level", type: "select",
              value: "16", id: "mr-stride",
              options: [{ value: "8", label: "P2 - stride 4, fine" },
                        { value: "16", label: "P4 - stride 16, the classic case" },
                        { value: "32", label: "P5 - stride 32, coarse" }] },
            { key: "bins", label: "Pooled output", type: "select", value: "7",
              id: "mr-bins",
              options: [{ value: "7", label: "7 x 7  - the box head" },
                        { value: "14", label: "14 x 14  - the mask head" }] },
            { key: "w", label: "Proposal width", type: "range",
              min: 2.5, max: 12, step: 0.1, value: 7.3, id: "mr-w",
              fmt: function (v) { return v.toFixed(1) + " cells"; } },
            { key: "hh", label: "Proposal height", type: "range",
              min: 2.5, max: 12, step: 0.1, value: 6.7, id: "mr-h",
              fmt: function (v) { return v.toFixed(1) + " cells"; } }
        ],
        build: function (ctx) {
            var m = featureMap();
            var pos = { x: 3.4, y: 4.6 };
            var S = 300;      /* pixels per side of the drawn feature map */

            /* The stage is rebuilt on every draw and a drag outlives several
             * draws, so the element carrying the pointer handlers has to be
             * one that survives. Capture on a node that is about to be
             * replaced and the drag dies at the first redraw - which looks
             * exactly like a broken pointer implementation and is not. */
            var s = svg(S, S, "arch-scene vz-touch-surface");
            var host = h("div", "arch-scroll");
            host.appendChild(s);

            function move(ev) {
                var r = s.getBoundingClientRect();
                var fx = (ev.clientX - r.left) / r.width * FM;
                var fy = (ev.clientY - r.top) / r.height * FM;
                pos.x = A.clamp(fx - ctx.params.w / 2, 0, FM - ctx.params.w);
                pos.y = A.clamp(fy - ctx.params.hh / 2, 0, FM - ctx.params.hh);
                ctx.redraw();
            }

            A.drag(s, move);

            return function draw() {
                var p = ctx.params;
                var bins = parseInt(p.bins, 10), stride = parseInt(p.stride, 10);
                pos.x = A.clamp(pos.x, 0, FM - p.w);
                pos.y = A.clamp(pos.y, 0, FM - p.hh);
                var roi = { x: pos.x, y: pos.y, w: p.w, h: p.hh };
                var pooled = roiPool(m, roi, bins);
                var aligned = roiAlign(m, roi, bins);

                var k = S / FM;
                while (s.firstChild) s.removeChild(s.firstChild);

                /* the feature map itself */
                for (var y = 0; y < FM; y++) for (var x = 0; x < FM; x++) {
                    s.appendChild(rect(x * k, y * k, k, k, {
                        fill: A.FILL, fo: A.clamp(m[y * FM + x] / 1.4, 0, 1) * 0.7,
                        stroke: A.BORDER, sw: 0.4, rx: 0
                    }));
                }
                /* the region the RPN actually proposed, at full precision */
                s.appendChild(rect(roi.x * k, roi.y * k, roi.w * k, roi.h * k,
                    { stroke: A.ACCENT, sw: 2 }));
                /* the region RoIPool would use instead */
                var sn = pooled.snapped;
                s.appendChild(rect(sn.x * k, sn.y * k, sn.w * k, sn.h * k,
                    { stroke: A.WARN, sw: 1.6, dash: "5 3" }));
                /* the bins, and where RoIAlign samples inside them */
                var bw = roi.w / bins, bh = roi.h / bins, i;
                for (i = 1; i < bins; i++) {
                    s.appendChild(line((roi.x + i * bw) * k, roi.y * k,
                                       (roi.x + i * bw) * k, (roi.y + roi.h) * k,
                                       { stroke: A.ACCENT, sw: 0.5, opacity: 0.55 }));
                    s.appendChild(line(roi.x * k, (roi.y + i * bh) * k,
                                       (roi.x + roi.w) * k, (roi.y + i * bh) * k,
                                       { stroke: A.ACCENT, sw: 0.5, opacity: 0.55 }));
                }
                aligned.samples.forEach(function (pt) {
                    s.appendChild(circle(pt.x * k, pt.y * k, 1.6,
                        { fill: A.ACCENT, stroke: "none", sw: 0 }));
                });

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(host);
                ctx.stage.appendChild(A.caption(
                    "Drag the proposal. Solid orange: what the RPN proposed. Dashed red: " +
                    "what RoIPool rounds it to. Dots: where RoIAlign samples."));

                var dx = roi.x - sn.x, dy = roi.y - sn.y;
                var shift = Math.sqrt(dx * dx + dy * dy);

                ctx.stage.appendChild(A.stats([
                    { value: roi.x.toFixed(2) + ", " + roi.y.toFixed(2),
                      label: "proposal corner", note: "in feature cells" },
                    { value: sn.x + ", " + sn.y, label: "after rounding",
                      note: "RoIPool works on this" },
                    { value: (shift * stride).toFixed(1) + " px",
                      label: "misalignment in the image",
                      note: shift.toFixed(2) + " cells x stride " + stride },
                    { value: bins + " x " + bins, label: "pooled output",
                      note: bins === 14 ? "then deconv to 28 x 28" : "then the box head" }
                ]));

                var maxv = 0, diff = 0;
                for (i = 0; i < bins * bins; i++) {
                    maxv = Math.max(maxv, pooled.out[i], aligned.out[i]);
                    diff += Math.abs(pooled.out[i] - aligned.out[i]);
                }
                diff /= bins * bins;

                ctx.stage.appendChild(A.section("The same region, pooled two ways"));
                var row = h("div", "arch-pair");
                row.appendChild(heat(pooled.out, bins, 150, "RoIPool  (rounded twice)", maxv));
                row.appendChild(heat(aligned.out, bins, 150, "RoIAlign  (bilinear)", maxv));
                ctx.stage.appendChild(row);
                ctx.stage.appendChild(A.note(
                    "Mean absolute difference between the two pooled maps: <strong>" +
                    diff.toFixed(3) + "</strong>. Slide the proposal width by a tenth of a " +
                    "cell and the RoIPool map jumps while the RoIAlign map moves smoothly " +
                    "&mdash; rounding is a step function, and a step function has no useful " +
                    "gradient with respect to the box coordinates either."));

                ctx.stage.appendChild(A.section("The three heads, on the same features"));
                ctx.stage.appendChild(A.layerTable(
                    ["head", "input", "layers", "output", "params"],
                    [{ cells: ["classification", "7x7x256", "fc 12544->1024, fc 1024->1024",
                               "81 scores", "13.9 M"] },
                     { cells: ["box regression", "7x7x256", "shares the two fc layers",
                               "4 x 80 offsets", "0.33 M"] },
                     { cells: ["mask", "14x14x256",
                               "4 x conv3x3(256), deconv 2x2, conv1x1",
                               "80 x 28 x 28", "2.64 M"], stage: bins === 14 }],
                    null, -1));

                ctx.stage.appendChild(A.note(
                    "The mask head is <strong>fully convolutional</strong> and predicts one " +
                    "28&times;28 mask <em>per class</em>, not one mask with a class label. " +
                    "Decoupling them is the second design decision in the paper: the mask " +
                    "loss for a region is only taken on the channel of its ground-truth " +
                    "class, so the mask branch never has to compete between classes and " +
                    "never learns to suppress one to favour another."));

                ctx.setReadout("proposal (" + roi.x.toFixed(2) + ", " + roi.y.toFixed(2) +
                    ") " + roi.w.toFixed(1) + "x" + roi.h.toFixed(1) + " cells  ->  rounding " +
                    "moves it " + (shift * stride).toFixed(1) + " pixels in the input");
            };
        }
    };
})();

/* ===========================================================================
 * A small corpus, shared by the word2vec and GloVe modules.
 *
 * Nineteen sentences with three deliberate topical groups - royalty, animals,
 * capitals - and one deliberate analogy pair. It is small enough that a
 * reader can read the whole thing and check the co-occurrence counts by hand,
 * and structured enough that a model trained on it in a browser tab produces
 * neighbours that are obviously right rather than obviously noise.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;

    var SENTENCES = [
        "the king rules the kingdom",
        "the queen rules the kingdom",
        "the king is a man",
        "the queen is a woman",
        "a man walks to the market",
        "a woman walks to the market",
        "the king and the queen sit on the throne",
        "the cat sits on the mat",
        "the dog sits on the mat",
        "the cat chases the mouse",
        "the dog chases the cat",
        "the cat drinks milk",
        "the dog eats bread",
        "paris is the capital of france",
        "berlin is the capital of germany",
        "france and germany are countries",
        "paris and berlin are cities",
        "the man walks to paris",
        "the woman walks to berlin"
    ];

    var TOKENS = SENTENCES.map(function (s) { return s.split(" "); });
    var VOCAB = [];
    var INDEX = {};
    TOKENS.forEach(function (t) {
        t.forEach(function (w) {
            if (!(w in INDEX)) { INDEX[w] = VOCAB.length; VOCAB.push(w); }
        });
    });
    var COUNT = new Array(VOCAB.length);
    for (var i = 0; i < COUNT.length; i++) COUNT[i] = 0;
    TOKENS.forEach(function (t) {
        t.forEach(function (w) { COUNT[INDEX[w]]++; });
    });

    /* Words worth offering as a focus: the content words, not "the" and "a". */
    var INTERESTING = ["king", "queen", "man", "woman", "cat", "dog", "mouse",
                       "paris", "berlin", "france", "germany", "market",
                       "kingdom", "capital", "walks", "chases"];

    function cosine(a, b) {
        var d = 0, na = 0, nb = 0;
        for (var i = 0; i < a.length; i++) {
            d += a[i] * b[i]; na += a[i] * a[i]; nb += b[i] * b[i];
        }
        return d / (Math.sqrt(na * nb) + 1e-9);
    }

    /* Top-2 principal components by power iteration, so an 8- or 16-dimensional
     * embedding can be drawn on a page. Deterministic: the same vectors always
     * project to the same picture. */
    function pca2(X) {
        var n = X.length, d = X[0].length, i, j;
        var mean = new Array(d);
        for (i = 0; i < d; i++) mean[i] = 0;
        X.forEach(function (v) { for (i = 0; i < d; i++) mean[i] += v[i] / n; });
        var Y = X.map(function (v) {
            return v.map(function (x, k) { return x - mean[k]; });
        });
        var C = [];
        for (i = 0; i < d; i++) { C.push(new Array(d)); for (j = 0; j < d; j++) C[i][j] = 0; }
        Y.forEach(function (v) {
            for (i = 0; i < d; i++) for (j = 0; j < d; j++) C[i][j] += v[i] * v[j] / n;
        });
        var r = A.rng(3);
        function power(M) {
            var v = [], k, it;
            for (k = 0; k < d; k++) v.push(r() - 0.5);
            for (it = 0; it < 160; it++) {
                var w = new Array(d);
                for (i = 0; i < d; i++) {
                    w[i] = 0;
                    for (j = 0; j < d; j++) w[i] += M[i][j] * v[j];
                }
                var nn = 0;
                for (i = 0; i < d; i++) nn += w[i] * w[i];
                nn = Math.sqrt(nn) || 1;
                for (i = 0; i < d; i++) v[i] = w[i] / nn;
            }
            var lam = 0;
            for (i = 0; i < d; i++) for (j = 0; j < d; j++) lam += v[i] * M[i][j] * v[j];
            return { v: v, lam: lam };
        }
        var p1 = power(C);
        var C2 = C.map(function (row, a2) {
            return row.map(function (x, b2) { return x - p1.lam * p1.v[a2] * p1.v[b2]; });
        });
        var p2 = power(C2);
        return Y.map(function (v) {
            var x = 0, y = 0;
            for (i = 0; i < d; i++) { x += v[i] * p1.v[i]; y += v[i] * p2.v[i]; }
            return [x, y];
        });
    }

    /* A scatter of labelled points, autoscaled. Used by three modules. */
    function scatter(points, labels, highlight, width, height) {
        var s = A.svg(width, height, "arch-scene");
        var xs = points.map(function (p) { return p[0]; });
        var ys = points.map(function (p) { return p[1]; });
        var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs);
        var y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
        var pad = 26;
        function px(x) { return pad + (x - x0) / ((x1 - x0) || 1) * (width - 2 * pad); }
        function py(y) { return height - pad - (y - y0) / ((y1 - y0) || 1) * (height - 2 * pad); }
        s.appendChild(A.rect(0.5, 0.5, width - 1, height - 1,
            { fill: A.SURFACE, stroke: A.BORDER, rx: 4 }));
        points.forEach(function (p, i) {
            var hot = highlight && highlight[labels[i]];
            s.appendChild(A.circle(px(p[0]), py(p[1]), hot ? 3.4 : 2, {
                fill: hot ? A.ACCENT : A.MUTED, stroke: "none", sw: 0,
                fo: hot ? 1 : 0.6
            }));
            s.appendChild(A.text(px(p[0]) + 5, py(p[1]) + 3, labels[i], {
                size: hot ? 9.5 : 8, anchor: "start",
                fill: hot ? A.ACCENT : A.MUTED, opacity: hot ? 1 : 0.75
            }));
        });
        return s;
    }

    window.VizArchCorpus = {
        SENTENCES: SENTENCES, TOKENS: TOKENS, VOCAB: VOCAB, INDEX: INDEX,
        COUNT: COUNT, INTERESTING: INTERESTING,
        cosine: cosine, pca2: pca2, scatter: scatter
    };
})();

/* ===========================================================================
 * word2vec - skip-gram and CBOW, with negative sampling
 *
 * The model really is trained here, in the tab, from the corpus above: the
 * training pairs are generated from the window you set, the vectors start
 * random, and every step is one SGD update of the same objective the paper
 * describes. Push the step slider from 0 and the nearest-neighbour table
 * changes under you - "king" starts next to nothing in particular and ends up
 * next to "queen".
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch, K = window.VizArchCorpus;
    var h = A.h;

    function pairsFor(window) {
        var out = [];
        K.TOKENS.forEach(function (t, si) {
            t.forEach(function (w, i) {
                for (var d = -window; d <= window; d++) {
                    var j = i + d;
                    if (d === 0 || j < 0 || j >= t.length) continue;
                    out.push({ c: K.INDEX[w], o: K.INDEX[t[j]], sent: si, at: i, ctx: j });
                }
            });
        });
        return out;
    }

    /* The unigram^0.75 noise distribution, exactly as in the paper: frequent
     * words are sampled as negatives more often, but not as much more often
     * as their raw frequency would say. */
    function noiseTable() {
        var pw = K.COUNT.map(function (c) { return Math.pow(c, 0.75); });
        var tot = 0, cum = [], acc = 0, i;
        for (i = 0; i < pw.length; i++) tot += pw[i];
        for (i = 0; i < pw.length; i++) { acc += pw[i] / tot; cum.push(acc); }
        return cum;
    }

    var CACHE = {};

    function train(p) {
        var key = [p.model, p.window, p.dim, p.neg, p.steps, p.lr].join("|");
        if (CACHE[key]) return CACHE[key];
        var r = A.rng(42), V = K.VOCAB.length, i, d;
        var W = [], C = [];
        for (i = 0; i < V; i++) {
            var a = [], b = [];
            for (d = 0; d < p.dim; d++) { a.push((r() - 0.5) * 0.6); b.push((r() - 0.5) * 0.6); }
            W.push(a); C.push(b);
        }
        var P = pairsFor(p.window), cum = noiseTable();
        function sample() {
            var u = r(), lo = 0, hi = V - 1;
            while (lo < hi) { var m = (lo + hi) >> 1; if (cum[m] < u) lo = m + 1; else hi = m; }
            return lo;
        }
        function sig(x) { return 1 / (1 + Math.exp(-x)); }
        var losses = [], run = 0;
        for (var s = 0; s < p.steps; s++) {
            var pr = P[Math.floor(r() * P.length)];
            /* CBOW predicts the centre from the average of its context; the
             * only difference in code is which side of the pair is averaged. */
            var centre = p.model === "cbow" ? pr.o : pr.c;
            var target = p.model === "cbow" ? pr.c : pr.o;
            var targets = [[target, 1]];
            for (var n = 0; n < p.neg; n++) targets.push([sample(), 0]);
            var gw = new Array(p.dim);
            for (d = 0; d < p.dim; d++) gw[d] = 0;
            for (var t = 0; t < targets.length; t++) {
                var ti = targets[t][0], label = targets[t][1], dot = 0;
                for (d = 0; d < p.dim; d++) dot += W[centre][d] * C[ti][d];
                var pv = sig(dot);
                run += -(label ? Math.log(pv + 1e-9) : Math.log(1 - pv + 1e-9));
                var g = (pv - label) * p.lr;
                for (d = 0; d < p.dim; d++) {
                    gw[d] += g * C[ti][d];
                    C[ti][d] -= g * W[centre][d];
                }
            }
            for (d = 0; d < p.dim; d++) W[centre][d] -= gw[d];
            if (s % 200 === 199) { losses.push(run / (200 * (p.neg + 1))); run = 0; }
        }
        var res = { W: W, C: C, pairs: P, losses: losses };
        CACHE[key] = res;
        return res;
    }

    A.WIDGETS.word2vec = {
        controls: [
            { key: "model", label: "Objective", type: "select", value: "skipgram",
              id: "w2v-model",
              options: [{ value: "skipgram", label: "skip-gram - centre predicts context" },
                        { value: "cbow", label: "CBOW - context predicts centre" }] },
            { key: "focus", label: "Focus word", type: "select", value: "king",
              id: "w2v-focus",
              options: K.INTERESTING.map(function (w) {
                  return { value: w, label: w }; }) },
            { key: "window", label: "Context window", type: "range",
              min: 1, max: 4, step: 1, value: 2, id: "w2v-window",
              fmt: function (v) { return "+/- " + v; } },
            { key: "dim", label: "Embedding dimensions", type: "range",
              min: 2, max: 16, step: 2, value: 8, id: "w2v-dim" },
            { key: "neg", label: "Negative samples per pair", type: "range",
              min: 1, max: 12, step: 1, value: 5, id: "w2v-neg" },
            { key: "steps", label: "Training steps", type: "range",
              min: 0, max: 24000, step: 500, value: 12000, id: "w2v-steps",
              fmt: function (v) { return A.commas(v); } }
        ],
        build: function (ctx) {
            return function draw() {
                var p = {
                    model: ctx.params.model, window: ctx.params.window,
                    dim: ctx.params.dim, neg: ctx.params.neg,
                    steps: ctx.params.steps, lr: 0.05
                };
                var res = train(p);
                var focus = ctx.params.focus;
                var fi = K.INDEX[focus];

                ctx.stage.innerHTML = "";

                /* 1. the pairs this window generates */
                var demo = res.pairs.filter(function (q) { return q.c === fi; }).slice(0, 8);
                var sent = demo.length ? demo[0].sent : 0;
                var toks = K.TOKENS[sent];
                var strip = h("div", "arch-tokens");
                toks.forEach(function (w, i) {
                    var centreAt = demo.length ? demo[0].at : -1;
                    var cls = "arch-token";
                    if (i === centreAt) cls += " is-centre";
                    else if (centreAt >= 0 && Math.abs(i - centreAt) <= p.window)
                        cls += " is-context";
                    strip.appendChild(h("span", cls, w));
                });
                ctx.stage.appendChild(A.section("One centre word, and the pairs it makes"));
                ctx.stage.appendChild(strip);
                var plist = h("p", "arch-mono arch-pairs");
                plist.textContent = demo.map(function (q) {
                    return "(" + K.VOCAB[q.c] + ", " + K.VOCAB[q.o] + ")";
                }).join("   ");
                ctx.stage.appendChild(plist);
                ctx.stage.appendChild(A.caption(
                    "A window of +/-" + p.window + " over " + K.SENTENCES.length +
                    " sentences gives " + A.commas(res.pairs.length) +
                    " training pairs. There is no labelled data anywhere: the corpus " +
                    "labels itself."));

                var nearest = null;

                /* 2. the embedding space */
                var proj = K.pca2(res.W);
                var hot = {};
                hot[focus] = 1;
                var sims = K.VOCAB.map(function (w, i) {
                    return { w: w, s: K.cosine(res.W[fi], res.W[i]) };
                }).filter(function (x) { return x.w !== focus; })
                  .sort(function (a, b) { return b.s - a.s; });
                sims.slice(0, 3).forEach(function (x) { hot[x.w] = 1; });

                nearest = sims[0];
                ctx.stage.appendChild(A.stats([
                    { value: K.VOCAB.length, label: "vocabulary",
                      note: K.SENTENCES.length + " sentences" },
                    { value: A.commas(res.pairs.length), label: "training pairs",
                      note: "window +/-" + p.window },
                    { value: A.commas(K.VOCAB.length * p.dim * 2), label: "parameters",
                      note: "two matrices of " + K.VOCAB.length + " x " + p.dim },
                    { value: nearest ? nearest.s.toFixed(3) : "-",
                      label: "cos(" + focus + ", " + (nearest ? nearest.w : "-") + ")",
                      note: p.steps ? "after " + A.commas(p.steps) + " steps"
                                    : "untrained - this is the initialisation" }
                ]));

                ctx.stage.appendChild(A.section(
                    "The vectors, projected to two dimensions"));
                var wrap = h("div", "arch-scroll");
                wrap.appendChild(K.scatter(proj, K.VOCAB, hot, 560, 300));
                ctx.stage.appendChild(wrap);
                ctx.stage.appendChild(A.caption(
                    p.dim === 2 ? "Trained in 2 dimensions, so this is the space itself."
                                : "Trained in " + p.dim + " dimensions and projected onto " +
                                  "its two principal components - the picture is a shadow " +
                                  "of the real space, not the space."));

                /* 3. what it learned */
                ctx.stage.appendChild(A.section("Nearest neighbours of “" + focus + "”"));
                ctx.stage.appendChild(A.layerTable(
                    ["word", "cosine similarity", "corpus count"],
                    sims.slice(0, 6).map(function (x, i) {
                        return { cells: [x.w, x.s.toFixed(3),
                                         String(K.COUNT[K.INDEX[x.w]])], stage: i === 0 };
                    }), null, -1));

                /* 4. the arithmetic of one update */
                var q = demo[0];
                if (q) {
                    var dot = 0;
                    for (var d = 0; d < p.dim; d++) dot += res.W[q.c][d] * res.C[q.o][d];
                    var pv = 1 / (1 + Math.exp(-dot));
                    ctx.stage.appendChild(A.section("One update, in full"));
                    ctx.stage.appendChild(A.note(
                        "For the pair <span class='arch-mono'>(" + K.VOCAB[q.c] + ", " +
                        K.VOCAB[q.o] + ")</span> the model takes the dot product of the " +
                        "centre vector with the context vector, " +
                        "<span class='arch-mono'>v&middot;u = " + dot.toFixed(3) +
                        "</span>, squashes it, " +
                        "<span class='arch-mono'>&sigma;(" + dot.toFixed(3) + ") = " +
                        pv.toFixed(3) + "</span>, and pushes it toward 1. It then draws " +
                        p.neg + " words from the corpus at random and pushes those toward " +
                        "0. That is the whole loss. Nothing is normalised over the " +
                        "vocabulary, which is what made word2vec fast enough to train on " +
                        "billions of words in 2013."));
                }

                if (res.losses.length > 2) {
                    var first = res.losses[0], last = res.losses[res.losses.length - 1];
                    ctx.stage.appendChild(A.bars([
                        { label: "loss over the first 200 steps", value: first },
                        { label: "loss over the last 200 steps", value: last, hot: true }
                    ], { format: function (v) { return v.toFixed(3); } }));
                }

                ctx.setReadout(p.model + ", window +/-" + p.window + ", " + p.dim +
                    "d, " + p.neg + " negatives, " + A.commas(p.steps) + " steps: " +
                    "nearest to “" + focus + "” is “" +
                    (sims[0] ? sims[0].w : "-") + "” at " +
                    (sims[0] ? sims[0].s.toFixed(3) : "-"));
            };
        }
    };
})();

/* ===========================================================================
 * GloVe
 *
 * word2vec learns from one window at a time and never sees a corpus-level
 * number. GloVe starts from the corpus-level number - the co-occurrence
 * count - and fits vectors to its logarithm. The paper motivates that with a
 * table of probability ratios, and that table is computed here from the real
 * counts of the corpus above rather than quoted: P(mouse | cat) is large,
 * P(mouse | dog) is zero, and P(the | anything) is the same either way, which
 * is precisely the signal a ratio keeps and a raw probability does not.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch, K = window.VizArchCorpus;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, path = A.path, line = A.line;

    var SHOWN = ["king", "queen", "man", "woman", "cat", "dog", "mouse", "mat",
                 "milk", "bread", "paris", "berlin", "france", "germany", "the"];

    var PROBES = [
        { a: "cat", b: "dog", ks: ["mouse", "milk", "bread", "mat", "sits", "chases", "the"] },
        { a: "king", b: "queen", ks: ["man", "woman", "rules", "kingdom", "throne", "the"] },
        { a: "paris", b: "berlin", ks: ["france", "germany", "capital", "cities", "is"] }
    ];

    var COOC = {};
    function cooccurrence(win) {
        if (COOC[win]) return COOC[win];
        var V = K.VOCAB.length, X = [], i;
        for (i = 0; i < V; i++) X.push(new Float64Array(V));
        K.TOKENS.forEach(function (t) {
            t.forEach(function (w, j) {
                for (var d = 1; d <= win; d++) {
                    var kk = j + d;
                    if (kk >= t.length) break;
                    var a = K.INDEX[w], b = K.INDEX[t[kk]];
                    /* 1/d: a word four away is weaker evidence than a word
                     * next door, and the paper weights it exactly this way. */
                    X[a][b] += 1 / d; X[b][a] += 1 / d;
                }
            });
        });
        COOC[win] = X;
        return X;
    }

    var TCACHE = {};
    function train(win, dim, epochs, xmax, alpha) {
        var key = [win, dim, epochs, xmax, alpha].join("|");
        if (TCACHE[key]) return TCACHE[key];
        var X = cooccurrence(win), V = K.VOCAB.length, r = A.rng(5);
        var W = [], Wt = [], b = new Float64Array(V), bt = new Float64Array(V);
        var gW = [], gWt = [], gb = new Float64Array(V), gbt = new Float64Array(V);
        var i, j, d;
        for (i = 0; i < V; i++) {
            var a1 = [], a2 = [], g1 = new Float64Array(dim), g2 = new Float64Array(dim);
            for (d = 0; d < dim; d++) {
                a1.push((r() - 0.5) / dim); a2.push((r() - 0.5) / dim);
                g1[d] = 1; g2[d] = 1;
            }
            W.push(a1); Wt.push(a2); gW.push(g1); gWt.push(g2);
            gb[i] = 1; gbt[i] = 1;
        }
        var ent = [];
        for (i = 0; i < V; i++) for (j = 0; j < V; j++)
            if (X[i][j] > 0) ent.push([i, j, X[i][j]]);
        function f(x) { return x < xmax ? Math.pow(x / xmax, alpha) : 1; }
        var loss = 0, first = 0, lr = 0.05;
        for (var ep = 0; ep < epochs; ep++) {
            loss = 0;
            for (var n = 0; n < ent.length; n++) {
                var ii = ent[n][0], jj = ent[n][1], x = ent[n][2];
                var dot = b[ii] + bt[jj];
                for (d = 0; d < dim; d++) dot += W[ii][d] * Wt[jj][d];
                var diff = dot - Math.log(x), fw = f(x);
                loss += fw * diff * diff;
                var g = fw * diff * lr;
                for (d = 0; d < dim; d++) {
                    var gi = g * Wt[jj][d], gj = g * W[ii][d];
                    W[ii][d] -= gi / Math.sqrt(gW[ii][d]);
                    Wt[jj][d] -= gj / Math.sqrt(gWt[jj][d]);
                    gW[ii][d] += gi * gi; gWt[jj][d] += gj * gj;
                }
                b[ii] -= g / Math.sqrt(gb[ii]); bt[jj] -= g / Math.sqrt(gbt[jj]);
                gb[ii] += g * g; gbt[jj] += g * g;
            }
            loss /= ent.length;
            if (ep === 0) first = loss;
        }
        /* The paper's final vectors are the sum of the two sets, which is
         * worth a sentence of its own: a word has a role as a centre and a
         * role as a context, and adding them averages the two. */
        var F = W.map(function (w, k) {
            return w.map(function (v, dd) { return v + Wt[k][dd]; });
        });
        var res = { W: W, Wt: Wt, F: F, b: b, bt: bt, loss: loss, first: first,
                    entries: ent.length, X: X };
        TCACHE[key] = res;
        return res;
    }

    function matrix(X, sel, pick) {
        var n = SHOWN.length, cell = 26, pad = 62;
        var S = svg(pad + n * cell + 8, pad + n * cell + 8, "arch-scene");
        var max = 0, i, j;
        for (i = 0; i < n; i++) for (j = 0; j < n; j++)
            max = Math.max(max, X[K.INDEX[SHOWN[i]]][K.INDEX[SHOWN[j]]]);
        for (i = 0; i < n; i++) {
            S.appendChild(text(pad - 5, pad + i * cell + 17, SHOWN[i],
                { size: 8.5, anchor: "end", fill: A.MUTED }));
            var t = text(pad + i * cell + 13, pad - 6, SHOWN[i],
                { size: 8.5, anchor: "start", fill: A.MUTED });
            t.setAttribute("transform", "rotate(-55 " + (pad + i * cell + 13) +
                " " + (pad - 6) + ")");
            S.appendChild(t);
        }
        for (i = 0; i < n; i++) for (j = 0; j < n; j++) {
            var v = X[K.INDEX[SHOWN[i]]][K.INDEX[SHOWN[j]]];
            var hot = sel && sel[0] === i && sel[1] === j;
            var r = rect(pad + j * cell, pad + i * cell, cell - 1, cell - 1, {
                fill: A.FILL, fo: max ? Math.pow(v / max, 0.55) * 0.9 : 0,
                stroke: hot ? A.ACCENT : A.BORDER, sw: hot ? 2 : 0.4, rx: 0
            });
            r.style.cursor = "pointer";
            (function (a, b) {
                r.addEventListener("click", function () { pick(a, b); });
            })(i, j);
            S.appendChild(r);
        }
        return S;
    }

    function weightPlot(xmax, alpha) {
        var W = 380, H = 150, pad = 30;
        var S = svg(W, H, "arch-scene");
        S.appendChild(rect(0.5, 0.5, W - 1, H - 1,
            { fill: A.SURFACE, stroke: A.BORDER, rx: 4 }));
        var xhi = Math.max(20, xmax * 2);
        var d = "", i;
        for (i = 0; i <= 120; i++) {
            var x = i / 120 * xhi;
            var y = x < xmax ? Math.pow(x / xmax, alpha) : 1;
            d += (i ? "L" : "M") + (pad + x / xhi * (W - 2 * pad)) + " " +
                 (H - pad - y * (H - 2 * pad));
        }
        S.appendChild(line(pad, H - pad, W - pad, H - pad, { stroke: A.BORDER }));
        S.appendChild(line(pad, pad, pad, H - pad, { stroke: A.BORDER }));
        S.appendChild(path(d, { stroke: A.ACCENT, sw: 2 }));
        S.appendChild(line(pad + xmax / xhi * (W - 2 * pad), pad,
                           pad + xmax / xhi * (W - 2 * pad), H - pad,
            { stroke: A.MUTED, dash: "4 3", sw: 1 }));
        S.appendChild(text(pad + xmax / xhi * (W - 2 * pad), pad - 4,
            "x_max = " + xmax, { size: 8, fill: A.MUTED }));
        S.appendChild(text(pad - 6, H - pad + 3, "0", { size: 8, anchor: "end" }));
        S.appendChild(text(pad - 6, pad + 4, "1", { size: 8, anchor: "end" }));
        S.appendChild(text(W / 2, H - 8, "co-occurrence count x",
            { size: 8.5, fill: A.MUTED }));
        return S;
    }

    A.WIDGETS.glove = {
        controls: [
            { key: "probe", label: "Probability ratio for", type: "select",
              value: "0", id: "glove-probe",
              options: PROBES.map(function (p, i) {
                  return { value: String(i), label: p.a + "  vs  " + p.b }; }) },
            { key: "win", label: "Co-occurrence window", type: "range",
              min: 1, max: 5, step: 1, value: 4, id: "glove-win",
              fmt: function (v) { return "+/- " + v; } },
            { key: "xmax", label: "Weighting cutoff x_max", type: "range",
              min: 2, max: 40, step: 1, value: 10, id: "glove-xmax" },
            { key: "alpha", label: "Weighting exponent alpha", type: "range",
              min: 0.25, max: 1.5, step: 0.05, value: 0.75, id: "glove-alpha",
              fmt: function (v) { return v.toFixed(2); } },
            { key: "epochs", label: "Training epochs", type: "range",
              min: 0, max: 600, step: 25, value: 300, id: "glove-epochs" }
        ],
        build: function (ctx) {
            var sel = [4, 6];   /* cat x mouse */
            function pick(i, j) { sel = [i, j]; ctx.redraw(); }
            return function draw() {
                var p = ctx.params;
                var X = cooccurrence(p.win);
                var probe = PROBES[parseInt(p.probe, 10)] || PROBES[0];

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(A.section(
                    "The co-occurrence matrix X, counted from the corpus"));
                var wrap = h("div", "arch-scroll");
                wrap.appendChild(matrix(X, sel, pick));
                ctx.stage.appendChild(wrap);

                var wi = SHOWN[sel[0]], wj = SHOWN[sel[1]];
                var xv = X[K.INDEX[wi]][K.INDEX[wj]];
                ctx.stage.appendChild(A.note(
                    "Cell (<strong>" + wi + "</strong>, <strong>" + wj + "</strong>) = " +
                    "<span class='arch-mono'>" + xv.toFixed(2) + "</span>" +
                    (xv > 0
                        ? ", so GloVe asks its vectors to satisfy <span class='arch-mono'>" +
                          "w<sub>" + wi + "</sub> &middot; w&#771;<sub>" + wj + "</sub> + " +
                          "b<sub>" + wi + "</sub> + b&#771;<sub>" + wj + "</sub> &asymp; log " +
                          xv.toFixed(2) + " = " + Math.log(xv).toFixed(3) + "</span>. " +
                          "Neighbours count fractionally: a word <em>d</em> places away " +
                          "contributes 1/<em>d</em>."
                        : ". The pair never co-occurs, so the term is dropped entirely " +
                          "&mdash; log 0 is undefined, and this is exactly why the " +
                          "weighting function has to be zero at zero.") +
                    " Click any cell."));

                /* the ratio table - the paper's motivating argument, recomputed */
                function cond(k, c) {
                    var row = X[K.INDEX[c]], tot = 0;
                    for (var i = 0; i < row.length; i++) tot += row[i];
                    return tot ? row[K.INDEX[k]] / tot : 0;
                }
                ctx.stage.appendChild(A.section(
                    "Why a ratio and not a probability"));
                ctx.stage.appendChild(A.layerTable(
                    ["word k", "P(k | " + probe.a + ")", "P(k | " + probe.b + ")",
                     "ratio", "what the ratio says"],
                    probe.ks.map(function (k) {
                        var pa = cond(k, probe.a), pb = cond(k, probe.b);
                        var ratio = pb > 0 ? pa / pb : (pa > 0 ? Infinity : NaN);
                        var verdict = isNaN(ratio) ? "neither, no evidence"
                            : (!isFinite(ratio) ? "only " + probe.a
                            : (ratio > 2.5 ? "leans " + probe.a
                            : (ratio < 0.4 ? "leans " + probe.b
                            : "shared - tells you nothing")));
                        return { cells: [k, pa.toFixed(4), pb.toFixed(4),
                                         isNaN(ratio) ? "-" :
                                         (isFinite(ratio) ? ratio.toFixed(2) : "inf"),
                                         verdict],
                                 stage: isFinite(ratio) && (ratio > 2.5 || ratio < 0.4) };
                    }), null, -1));
                ctx.stage.appendChild(A.note(
                    "Both <em>" + probe.a + "</em> and <em>" + probe.b + "</em> are common " +
                    "next to <span class='arch-mono'>the</span>, so the raw probabilities " +
                    "are large for both and say nothing. The <em>ratio</em> of the two is " +
                    "near 1 for the words they share and far from 1 for the words that " +
                    "distinguish them. GloVe's whole derivation is the search for a vector " +
                    "function whose value depends on that ratio, and the answer &mdash; " +
                    "differences of dot products &mdash; is what fixes the objective to " +
                    "log-counts."));

                /* the weighting function */
                ctx.stage.appendChild(A.section("The weighting function f(x)"));
                var w2 = h("div", "arch-scroll");
                w2.appendChild(weightPlot(p.xmax, p.alpha));
                ctx.stage.appendChild(w2);
                ctx.stage.appendChild(A.note(
                    "Each squared error is multiplied by <span class='arch-mono'>f(x) = " +
                    "min(1, (x / " + p.xmax + ")<sup>" + p.alpha.toFixed(2) + "</sup>)" +
                    "</span>. It does two jobs. It is 0 at x = 0, so pairs that never " +
                    "co-occur contribute nothing rather than dominating the sum with their " +
                    "sheer number. And it stops rising past x_max, so <span class='arch-mono'>" +
                    "the</span> next to everything is not allowed to outvote every content " +
                    "word in the corpus. Drop alpha toward 0.25 and rare pairs count for " +
                    "more; raise x_max and frequent ones keep gaining influence for longer."));

                /* the fit */
                var res = train(p.win, 12, p.epochs, p.xmax, p.alpha);
                var sims = K.VOCAB.map(function (w, i) {
                    return { w: w, s: K.cosine(res.F[K.INDEX[probe.a]], res.F[i]) };
                }).filter(function (x) { return x.w !== probe.a; })
                  .sort(function (a, b) { return b.s - a.s; });

                ctx.stage.appendChild(A.section("Fitting vectors to those counts"));
                ctx.stage.appendChild(A.stats([
                    { value: A.commas(res.entries), label: "non-zero cells fitted",
                      note: "of " + A.commas(K.VOCAB.length * K.VOCAB.length) + " in X" },
                    { value: res.loss.toFixed(4), label: "weighted least-squares loss",
                      note: p.epochs ? "from " + res.first.toFixed(3) : "untrained" },
                    { value: sims[0] ? sims[0].s.toFixed(2) : "-",
                      label: "cos(" + probe.a + ", " + (sims[0] ? sims[0].w : "-") + ")",
                      note: "nearest neighbour" },
                    { value: "12", label: "dimensions", note: "300 in the released vectors" }
                ]));
                if (p.epochs > 0) {
                    var proj = K.pca2(res.F);
                    var hot = {};
                    hot[probe.a] = 1; hot[probe.b] = 1;
                    var w3 = h("div", "arch-scroll");
                    w3.appendChild(K.scatter(proj, K.VOCAB, hot, 560, 280));
                    ctx.stage.appendChild(w3);
                }
                ctx.stage.appendChild(A.note(
                    "Nineteen sentences are not global statistics, and it shows: " +
                    "<em>man</em>/<em>woman</em> and <em>paris</em>/<em>berlin</em> come out " +
                    "cleanly because the corpus states those relations several times, while " +
                    "anything seen once lands wherever the initialisation left it. That is " +
                    "the honest failure mode of a count-based method &mdash; it can only " +
                    "know what the counts know, and unlike word2vec it does not get a second " +
                    "chance to see the same pair in a new window."));

                ctx.setReadout("window +/-" + p.win + ", x_max " + p.xmax + ", alpha " +
                    p.alpha.toFixed(2) + ", " + p.epochs + " epochs: " + res.entries +
                    " non-zero cells, loss " + res.loss.toFixed(4));
            };
        }
    };
})();

/* ===========================================================================
 * Sequence pairs and an attention mechanism, shared by the seq2seq and
 * machine-translation modules.
 *
 * The key and query vectors below are stated, not learned. That is a
 * deliberate choice and it is said on the page: a randomly initialised
 * attention layer aligns nothing, and pretending otherwise would be a lie
 * dressed as a demonstration. What *is* real is every number computed from
 * them - the scaled dot products, the softmax, the context vector - so a
 * reader can check the mechanism by hand even though the vectors were chosen
 * rather than trained.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;

    /* A tiny concept space. Each dimension is a meaning; a token's vector
     * says which meanings it carries. */
    var CONCEPTS = ["det", "cat", "black", "sleep", "on", "mat",
                    "i", "speak", "neg", "french", "do"];

    function vec(parts, pos) {
        var v = [];
        for (var i = 0; i < CONCEPTS.length; i++) v.push(parts[CONCEPTS[i]] || 0);
        v.push(pos === undefined ? 0 : pos * 0.12);
        return v;
    }

    var PAIRS = [
        {
            name: "le chat noir dort sur le tapis  ->  the black cat sleeps on the mat",
            src: ["le", "chat", "noir", "dort", "sur", "le", "tapis"],
            tgt: ["the", "black", "cat", "sleeps", "on", "the", "mat"],
            keys: [vec({ det: 1 }, 0), vec({ cat: 1 }, 1), vec({ black: 1 }, 2),
                   vec({ sleep: 1 }, 3), vec({ on: 1 }, 4), vec({ det: 1 }, 5),
                   vec({ mat: 1 }, 6)],
            queries: [vec({ det: 1 }, 0), vec({ black: 1 }, 2), vec({ cat: 1 }, 1),
                      vec({ sleep: 1 }, 3), vec({ on: 1 }, 4), vec({ det: 1 }, 5),
                      vec({ mat: 1 }, 6)],
            note: "French puts the adjective after the noun, so the alignment crosses: " +
                  "target word 2 attends to source word 3."
        },
        {
            name: "je ne parle pas francais  ->  i do not speak french",
            src: ["je", "ne", "parle", "pas", "francais"],
            tgt: ["i", "do", "not", "speak", "french"],
            keys: [vec({ i: 1 }, 0), vec({ neg: 0.8 }, 1), vec({ speak: 1 }, 2),
                   vec({ neg: 0.8 }, 3), vec({ french: 1 }, 4)],
            queries: [vec({ i: 1 }, 0), vec({ speak: 0.35, i: 0.2 }, 1),
                      vec({ neg: 1 }, 2), vec({ speak: 1 }, 2), vec({ french: 1 }, 4)],
            note: "French negation is two words wrapped around the verb, English is one. " +
                  "“not” attends to both “ne” and “pas”, and “do” has nothing to align to " +
                  "at all - it exists only because English needs it."
        }
    ];

    function softmax(xs, temp) {
        var t = temp || 1, m = -Infinity, i, out = [], sum = 0;
        for (i = 0; i < xs.length; i++) m = Math.max(m, xs[i] / t);
        for (i = 0; i < xs.length; i++) { out.push(Math.exp(xs[i] / t - m)); sum += out[i]; }
        for (i = 0; i < out.length; i++) out[i] /= sum;
        return out;
    }

    function dot(a, b) {
        var d = 0;
        for (var i = 0; i < a.length; i++) d += a[i] * b[i];
        return d;
    }

    /* Scaled dot-product attention, one query at a time. */
    function attend(query, keys, temp) {
        var dk = keys[0].length, scores = keys.map(function (k) {
            return dot(query, k) / Math.sqrt(dk);
        });
        return { scores: scores, weights: softmax(scores, temp) };
    }

    function alignment(pair, temp) {
        return pair.queries.map(function (q) { return attend(q, pair.keys, temp); });
    }

    /* A target-by-source heatmap. Both modules draw one. */
    function heatmap(pair, rows, sel, width) {
        var n = pair.src.length, m = pair.tgt.length;
        var cell = Math.min(34, (width - 96) / n);
        var padL = 88, padT = 26;
        var S = A.svg(padL + n * cell + 10, padT + m * cell + 26, "arch-scene");
        var i, j;
        for (j = 0; j < n; j++) {
            var t = A.text(padL + j * cell + cell / 2, padT - 6, pair.src[j],
                { size: 9, fill: A.MUTED, anchor: "start" });
            t.setAttribute("transform", "rotate(-50 " +
                (padL + j * cell + cell / 2) + " " + (padT - 6) + ")");
            S.appendChild(t);
        }
        for (i = 0; i < m; i++) {
            S.appendChild(A.text(padL - 6, padT + i * cell + cell * 0.65, pair.tgt[i],
                { size: 9.5, anchor: "end",
                  fill: sel === i ? A.ACCENT : A.MUTED }));
            for (j = 0; j < n; j++) {
                var w = rows[i].weights[j];
                S.appendChild(A.rect(padL + j * cell, padT + i * cell, cell - 1, cell - 1, {
                    fill: A.FILL, fo: Math.pow(w, 0.6),
                    stroke: sel === i ? A.ACCENT : A.BORDER,
                    sw: sel === i ? 1.2 : 0.3, rx: 0
                }));
                if (w > 0.18)
                    S.appendChild(A.text(padL + j * cell + cell / 2 - 0.5,
                        padT + i * cell + cell * 0.65, w.toFixed(2),
                        { size: 7, fill: A.MAIN }));
            }
        }
        S.appendChild(A.text(padL + n * cell / 2, padT + m * cell + 18,
            "rows sum to 1 - every target word spends all its attention somewhere",
            { size: 8, fill: A.MUTED }));
        return S;
    }

    window.VizArchSeq = {
        PAIRS: PAIRS, softmax: softmax, dot: dot, attend: attend,
        alignment: alignment, heatmap: heatmap
    };
})();

/* ===========================================================================
 * Seq2seq - the encoder, the decoder, and the vector between them
 *
 * The original 2014 model compressed the whole source sentence into one fixed
 * vector and decoded from that. The obvious objection - that a fixed vector
 * cannot hold an arbitrarily long sentence - is usually stated and rarely
 * shown. It is measured here: the encoder is a real recurrent network, and
 * the influence of each input token on the final state is computed by
 * perturbing that token and measuring how far the final state moves. Shorten
 * the hidden size or lengthen the sentence and the early tokens flatten to
 * nothing, which is the bottleneck, in numbers.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch, Q = window.VizArchSeq;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, arrow = A.arrow, path = A.path;

    /* A real Elman RNN with fixed random weights. Untrained, and said to be:
     * what is being demonstrated is how information decays through a
     * recurrence, which does not depend on the weights being good. */
    function encode(tokens, embed, H, seed) {
        var r = A.rng(seed || 9), D = embed[0].length, i, j;
        var Wx = [], Wh = [];
        for (i = 0; i < H; i++) {
            var a = [], b = [];
            for (j = 0; j < D; j++) a.push(A.gauss(r) * 0.9 / Math.sqrt(D));
            for (j = 0; j < H; j++) b.push(A.gauss(r) * 0.95 / Math.sqrt(H));
            Wx.push(a); Wh.push(b);
        }
        var hs = [], hprev = new Float64Array(H);
        tokens.forEach(function (_t, ti) {
            var hn = new Float64Array(H);
            for (i = 0; i < H; i++) {
                var s = 0;
                for (j = 0; j < D; j++) s += Wx[i][j] * embed[ti][j];
                for (j = 0; j < H; j++) s += Wh[i][j] * hprev[j];
                hn[i] = Math.tanh(s);
            }
            hs.push(hn); hprev = hn;
        });
        return hs;
    }

    function dist(a, b) {
        var s = 0;
        for (var i = 0; i < a.length; i++) s += (a[i] - b[i]) * (a[i] - b[i]);
        return Math.sqrt(s);
    }

    function stateBar(vec, x, y, w, hgt) {
        var g = A.e("g", {});
        var n = vec.length, cw = w / n;
        for (var i = 0; i < n; i++) {
            var v = (vec[i] + 1) / 2;
            g.appendChild(rect(x + i * cw, y, Math.max(0.8, cw - 0.5), hgt, {
                fill: A.FILL, fo: 0.15 + 0.8 * v, stroke: "none", sw: 0, rx: 0
            }));
        }
        g.appendChild(rect(x, y, w, hgt, { stroke: A.BORDER, sw: 0.6, rx: 1 }));
        return g;
    }

    A.WIDGETS.seq2seq = {
        controls: [
            { key: "pair", label: "Sentence", type: "select", value: "0", id: "s2s-pair",
              options: Q.PAIRS.map(function (p, i) {
                  return { value: String(i), label: p.name }; }) },
            { key: "step", label: "Decoder step", type: "range",
              min: 0, max: 6, step: 1, value: 2, id: "s2s-step" },
            { key: "hidden", label: "Hidden size", type: "range",
              min: 4, max: 64, step: 4, value: 16, id: "s2s-hidden",
              fmt: function (v) { return v + " units"; } },
            { key: "repeat", label: "Sentence length", type: "range",
              min: 1, max: 6, step: 1, value: 1, id: "s2s-repeat",
              fmt: function (v) { return "x" + v + " the source"; } },
            { key: "attn", label: "Attention", type: "toggle", value: false, id: "s2s-attn" }
        ],
        build: function (ctx) {
            return function draw() {
                var p = ctx.params;
                var pair = Q.PAIRS[parseInt(p.pair, 10)] || Q.PAIRS[0];
                var H = p.hidden;

                /* the source, optionally repeated, to make length a control */
                var src = [], emb = [], i, k;
                for (k = 0; k < p.repeat; k++)
                    for (i = 0; i < pair.src.length; i++) {
                        src.push(pair.src[i]); emb.push(pair.keys[i]);
                    }
                var hs = encode(src, emb, H, 9);
                var thought = hs[hs.length - 1];

                /* how much does each input token still matter at the end? */
                var influence = src.map(function (_t, ti) {
                    var e2 = emb.map(function (v, j) {
                        return j === ti ? v.map(function (x) { return -x; }) : v;
                    });
                    var h2 = encode(src, e2, H, 9);
                    return dist(thought, h2[h2.length - 1]);
                });
                var maxInf = Math.max.apply(null, influence) || 1;

                var step = Math.min(p.step, pair.tgt.length - 1);
                var rows = Q.alignment(pair, 0.35);

                ctx.stage.innerHTML = "";

                /* the unrolled diagram */
                var n = src.length;
                var cw = Math.max(52, Math.min(74, 560 / Math.max(n, pair.tgt.length)));
                var W = Math.max(560, 40 + Math.max(n, pair.tgt.length) * cw);
                var s = svg(W, 260, "arch-svg-wide");
                s.appendChild(text(14, 16, "encoder",
                    { size: 9.5, fill: A.MUTED, anchor: "start" }));
                for (i = 0; i < n; i++) {
                    var x = 26 + i * cw;
                    s.appendChild(text(x + cw / 2 - 6, 36, src[i],
                        { size: 9, fill: A.MAIN }));
                    s.appendChild(rect(x, 44, cw - 8, 26,
                        { fill: A.SURFACE, stroke: A.BORDER }));
                    s.appendChild(stateBar(hs[i], x + 3, 48, cw - 14, 18));
                    if (i) s.appendChild(arrow(x - 8, 57, x, 57,
                        { stroke: A.BORDER, sw: 1 }));
                    /* influence of this token on the final state */
                    var inf = influence[i] / maxInf;
                    s.appendChild(rect(x, 76, cw - 8, 16 * inf + 1, {
                        fill: A.FILL, fo: 0.55, stroke: "none", sw: 0, rx: 1
                    }));
                    s.appendChild(text(x + (cw - 8) / 2, 104, inf.toFixed(2),
                        { size: 7, fill: A.MUTED }));
                }
                s.appendChild(text(14, 96, "influence on",
                    { size: 7.5, fill: A.MUTED, anchor: "start" }));
                s.appendChild(text(14, 105, "the final state",
                    { size: 7.5, fill: A.MUTED, anchor: "start" }));

                /* the vector in the middle */
                var tx = 26 + (n - 1) * cw + (cw - 8) / 2;
                s.appendChild(rect(W / 2 - 90, 122, 180, 28,
                    { fill: A.FILL, fo: p.attn ? 0.08 : 0.2,
                      stroke: p.attn ? A.BORDER : A.ACCENT }));
                s.appendChild(text(W / 2, 140,
                    "thought vector  -  " + H + " numbers",
                    { size: 9.5, fill: p.attn ? A.MUTED : A.ACCENT }));
                s.appendChild(arrow(tx, 108, W / 2, 122, { stroke: A.BORDER, sw: 1 }));

                /* decoder */
                s.appendChild(text(14, 176, "decoder",
                    { size: 9.5, fill: A.MUTED, anchor: "start" }));
                for (i = 0; i < pair.tgt.length; i++) {
                    var dx = 26 + i * cw;
                    var hot = i === step;
                    s.appendChild(rect(dx, 186, cw - 8, 26, {
                        fill: hot ? A.FILL : A.SURFACE, fo: hot ? 0.25 : 1,
                        stroke: hot ? A.ACCENT : A.BORDER
                    }));
                    s.appendChild(text(dx + (cw - 8) / 2, 203, pair.tgt[i],
                        { size: 9, fill: hot ? A.ACCENT : A.MAIN }));
                    if (i) s.appendChild(arrow(dx - 8, 199, dx, 199,
                        { stroke: A.BORDER, sw: 1 }));
                    if (!p.attn)
                        s.appendChild(arrow(W / 2, 150, dx + (cw - 8) / 2, 186,
                            { stroke: A.BORDER, sw: 0.8, opacity: 0.5 }));
                }
                if (p.attn && p.repeat === 1) {
                    /* one line per source position, thickness = attention weight */
                    var wts = rows[step].weights;
                    for (i = 0; i < pair.src.length; i++) {
                        if (wts[i] < 0.02) continue;
                        s.appendChild(path("M" + (26 + i * cw + (cw - 8) / 2) + " 70 " +
                            "C" + (26 + i * cw + (cw - 8) / 2) + " 140 " +
                            (26 + step * cw + (cw - 8) / 2) + " 130 " +
                            (26 + step * cw + (cw - 8) / 2) + " 186", {
                                stroke: A.ACCENT, sw: 0.5 + 3.5 * wts[i],
                                opacity: 0.3 + 0.7 * wts[i]
                            }));
                    }
                }
                s.appendChild(text(W / 2, 240, p.attn
                    ? "with attention, every decoder step reads the encoder states directly"
                    : "without attention, this one vector is all the decoder ever sees",
                    { size: 8.5, fill: p.attn ? A.ACCENT : A.MUTED }));

                var wrap = h("div", "arch-scroll");
                wrap.appendChild(s);
                ctx.stage.appendChild(wrap);

                var early = influence.slice(0, Math.max(1, Math.floor(n / 3)));
                var late = influence.slice(-Math.max(1, Math.floor(n / 3)));
                var avg = function (a) {
                    return a.reduce(function (x, y) { return x + y; }, 0) / a.length;
                };
                var ratio = avg(late) / (avg(early) || 1e-9);

                ctx.stage.appendChild(A.stats([
                    { value: n, label: "source tokens",
                      note: "into " + H + " numbers" },
                    { value: (n * Math.log2(32)).toFixed(0) + " bits",
                      label: "information in the source",
                      note: "at a 32-word vocabulary" },
                    { value: ratio.toFixed(1) + "x", label: "last third vs first third",
                      note: "influence on the final state" },
                    { value: p.attn ? "n x H" : "H", label: "what the decoder can read",
                      note: p.attn ? n * H + " numbers" : H + " numbers" }
                ]));

                ctx.stage.appendChild(A.note(p.attn
                    ? "With attention the encoder still runs exactly as before &mdash; the " +
                      "change is that its <em>per-step</em> states are kept rather than " +
                      "discarded. Decoder step " + (step + 1) + " computes a score against " +
                      "each of them, softmaxes the scores into weights, and reads a weighted " +
                      "average. Nothing has to survive to the end of the sentence any more, " +
                      "so the length of the source stops being a capacity problem."
                    : "The recurrence overwrites its state at every token, so the trace left " +
                      "by an early word has been multiplied by the recurrent matrix " +
                      (n - 1) + " times before the decoder sees it. The bars above are that " +
                      "decay measured directly: the last third of the sentence has <strong>" +
                      ratio.toFixed(1) + "&times;</strong> the influence of the first third. " +
                      "Push <em>Sentence length</em> up and watch the front of the sentence " +
                      "flatten out."));

                if (p.attn && p.repeat === 1) {
                    ctx.stage.appendChild(A.section(
                        "Attention weights at decoder step " + (step + 1) +
                        "  (“" + pair.tgt[step] + "”)"));
                    ctx.stage.appendChild(A.bars(pair.src.map(function (w, j) {
                        return { label: w, value: rows[step].weights[j],
                                 hot: rows[step].weights[j] > 0.4 };
                    }), { format: function (v) { return v.toFixed(3); } }));
                    ctx.stage.appendChild(A.note(pair.note));
                }

                ctx.setReadout(n + " source tokens, hidden size " + H +
                    (p.attn ? ", attention on" : ", one fixed vector") +
                    ": decoder step " + (step + 1) + " emits \u201c" + pair.tgt[step] +
                    "\u201d; influence ratio late/early " + ratio.toFixed(2));
            };
        }
    };
})();

/* ===========================================================================
 * Machine translation with an encoder-decoder
 *
 * Two things separate a translation model from a classifier, and both are
 * about the *output* being a sequence. Attention decides which source words a
 * target word is allowed to look at, and search decides which of the
 * exponentially many output sequences is returned. Greedy decoding is the
 * search that takes the best word at every step, and on the second sentence
 * here it drops the negation entirely - "i speak french" instead of "i do not
 * speak french" - because "speak" is the better second word and there is no
 * way back. Beam search keeps the alternative alive and recovers it.
 *
 * The next-word distributions below are hand-written, small, and printed on
 * the page. That is on purpose: every number in the beam table can be checked
 * with a calculator, which is not true of any real model's logits.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch, Q = window.VizArchSeq;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, path = A.path;

    var MODELS = [
        {   /* le chat noir dort sur le tapis */
            "": [["the", -0.22], ["a", -1.90], ["black", -2.60]],
            "the": [["cat", -0.55], ["black", -0.90], ["dark", -2.40]],
            "the cat": [["</s>", -0.95], ["is", -1.10], ["black", -1.35],
                        ["sleeps", -1.60]],
            "the black": [["cat", -0.15], ["cats", -2.60], ["one", -3.10]],
            "the cat is": [["black", -0.60], ["sleeping", -1.40], ["on", -2.60]],
            "the cat black": [["sleeps", -1.20], ["</s>", -2.00]],
            "the black cat": [["sleeps", -0.25], ["is", -2.00], ["naps", -2.60]],
            "the cat is black": [["</s>", -1.20], ["and", -1.80], ["on", -2.10]],
            "the black cat sleeps": [["on", -0.18], ["in", -2.20], ["</s>", -3.40]],
            "the black cat sleeps on": [["the", -0.12], ["a", -2.40]],
            "the black cat sleeps on the": [["mat", -0.20], ["rug", -2.10],
                                            ["carpet", -2.80]],
            "the black cat sleeps on the mat": [["</s>", -0.08]]
        },
        {   /* je ne parle pas francais */
            "": [["i", -0.15], ["we", -2.30]],
            "i": [["speak", -0.60], ["do", -0.70], ["don't", -1.50]],
            "i speak": [["french", -0.90], ["not", -1.90]],
            "i speak french": [["</s>", -0.60]],
            "i do": [["not", -0.10], ["speak", -2.50]],
            "i do not": [["speak", -0.12], ["talk", -2.60]],
            "i do not speak": [["french", -0.10], ["it", -3.00]],
            "i do not speak french": [["</s>", -0.05]],
            "i don't": [["speak", -0.20]],
            "i don't speak": [["french", -0.15]],
            "i don't speak french": [["</s>", -0.10]]
        }
    ];

    function penalty(len, alpha) {
        return Math.pow((5 + len) / 6, alpha);
    }

    function beamSearch(model, width, alpha, maxSteps) {
        var beams = [{ seq: [], lp: 0, done: false }];
        var history = [];
        for (var step = 0; step < maxSteps; step++) {
            var cand = [], any = false;
            beams.forEach(function (b) {
                if (b.done) {
                    /* Carry it forward linked to its own previous row, so the
                     * tree draws a straight continuation rather than an edge
                     * back to whatever its parent was two steps ago. */
                    cand.push({ seq: b.seq, lp: b.lp, done: true,
                                from: b.seq.join(" "), word: "\u2014",
                                stepLp: 0 });
                    return;
                }
                var next = model[b.seq.join(" ")] || [["</s>", -1.5]];
                next.forEach(function (nx) {
                    any = true;
                    var seq = b.seq.concat([nx[0]]);
                    cand.push({
                        seq: seq, lp: b.lp + nx[1], done: nx[0] === "</s>",
                        from: b.seq.join(" "), word: nx[0], stepLp: nx[1]
                    });
                });
            });
            if (!any) break;
            cand.forEach(function (c) {
                c.score = c.lp / penalty(c.seq.length, alpha);
            });
            cand.sort(function (a, b) { return b.score - a.score; });
            var kept = cand.slice(0, width);
            history.push({ step: step + 1, all: cand, kept: kept });
            beams = kept;
            if (beams.every(function (b) { return b.done; })) break;
        }
        beams.sort(function (a, b) { return b.score - a.score; });
        return { beams: beams, history: history };
    }

    function tree(history, width) {
        var rows = history.length;
        var W = 600, H = 40 + rows * 52;
        var s = svg(W, H, "arch-svg-wide");
        var prev = [{ x: W / 2, seq: "" }];
        history.forEach(function (hh, ri) {
            var y = 34 + ri * 52;
            var n = hh.kept.length;
            var here = [];
            hh.kept.forEach(function (b, i) {
                var x = W / (n + 1) * (i + 1);
                var parent = prev.filter(function (q) { return q.seq === b.from; })[0]
                          || prev[0];
                if (parent && b.word)
                    s.appendChild(path("M" + parent.x + " " + (y - 34) +
                        " C" + parent.x + " " + (y - 12) + " " + x + " " + (y - 20) +
                        " " + x + " " + (y - 4), { stroke: A.BORDER, sw: 1 }));
                var top = i === 0;
                s.appendChild(rect(x - 52, y - 4, 104, 30, {
                    fill: top ? A.FILL : A.SURFACE, fo: top ? 0.2 : 1,
                    stroke: top ? A.ACCENT : A.BORDER
                }));
                s.appendChild(text(x, y + 9, b.word + (b.done ? "  [end]" : ""),
                    { size: 9, fill: top ? A.ACCENT : A.MAIN }));
                s.appendChild(text(x, y + 20, "score " + b.score.toFixed(3),
                    { size: 7.5, fill: A.MUTED }));
                here.push({ x: x, seq: b.seq.join(" ") });
            });
            prev = here;
        });
        s.appendChild(text(W / 2, 14,
            "the " + width + " sequences alive at each step, best on the left",
            { size: 8.5, fill: A.MUTED }));
        return s;
    }

    A.WIDGETS.translation = {
        controls: [
            { key: "pair", label: "Sentence", type: "select", value: "1", id: "mt-pair",
              options: Q.PAIRS.map(function (p, i) {
                  return { value: String(i), label: p.name }; }) },
            { key: "width", label: "Beam width", type: "range",
              min: 1, max: 5, step: 1, value: 3, id: "mt-width",
              fmt: function (v) { return v === 1 ? "1  (greedy)" : String(v); } },
            { key: "alpha", label: "Length penalty alpha", type: "range",
              min: 0, max: 1.4, step: 0.1, value: 0.7, id: "mt-alpha",
              fmt: function (v) { return v.toFixed(1); } },
            { key: "temp", label: "Attention temperature", type: "range",
              min: 0.15, max: 2, step: 0.05, value: 0.35, id: "mt-temp",
              fmt: function (v) { return v.toFixed(2); } },
            { key: "row", label: "Target word to inspect", type: "range",
              min: 1, max: 7, step: 1, value: 3, id: "mt-row" }
        ],
        build: function (ctx) {
            return function draw() {
                var p = ctx.params;
                var pi = parseInt(p.pair, 10);
                var pair = Q.PAIRS[pi] || Q.PAIRS[0];
                var rows = Q.alignment(pair, p.temp);
                var sel = Math.min(p.row, pair.tgt.length) - 1;

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(A.section("Which source words each target word reads"));
                var wrap = h("div", "arch-scroll");
                wrap.appendChild(Q.heatmap(pair, rows, sel, 560));
                ctx.stage.appendChild(wrap);

                var r = rows[sel], best = 0, j;
                for (j = 1; j < r.weights.length; j++)
                    if (r.weights[j] > r.weights[best]) best = j;
                var entropy = 0;
                r.weights.forEach(function (w) {
                    if (w > 1e-9) entropy -= w * Math.log2(w);
                });

                ctx.stage.appendChild(A.stats([
                    { value: "“" + pair.tgt[sel] + "”", label: "target word",
                      note: "position " + (sel + 1) },
                    { value: "“" + pair.src[best] + "”", label: "attends most to",
                      note: "weight " + r.weights[best].toFixed(3) },
                    { value: entropy.toFixed(2) + " bits", label: "attention entropy",
                      note: entropy < 0.6 ? "sharp - it has decided"
                                          : "diffuse - it is hedging" },
                    { value: (Math.pow(2, entropy)).toFixed(1), label: "effective sources",
                      note: "of " + pair.src.length }
                ]));
                ctx.stage.appendChild(A.note(
                    "The weight on source word <em>j</em> is <span class='arch-mono'>" +
                    "softmax<sub>j</sub>(q &middot; k<sub>j</sub> / &radic;d<sub>k</sub>)" +
                    "</span>. Raising the temperature divides the scores before the " +
                    "softmax, which flattens the distribution toward a plain average of " +
                    "the whole sentence; lowering it drives the attention to a single " +
                    "word. Neither extreme translates well: a flat distribution loses the " +
                    "alignment, and a one-hot one cannot handle a target word that " +
                    "genuinely depends on two source words. " + pair.note));

                /* --- search --- */
                var model = MODELS[pi] || MODELS[0];
                var res = beamSearch(model, p.width, p.alpha, 9);
                var greedy = beamSearch(model, 1, p.alpha, 9);
                var wide = beamSearch(model, 5, p.alpha, 9);

                ctx.stage.appendChild(A.section("Searching for the output sequence"));
                var w2 = h("div", "arch-scroll");
                w2.appendChild(tree(res.history, p.width));
                ctx.stage.appendChild(w2);

                function show(b) {
                    return b.seq.filter(function (w) { return w !== "</s>"; }).join(" ");
                }
                ctx.stage.appendChild(A.layerTable(
                    ["rank", "sequence", "sum log p", "length", "normalised score"],
                    res.beams.slice(0, 5).map(function (b, i) {
                        return { cells: [String(i + 1), show(b), b.lp.toFixed(3),
                                         String(b.seq.length), b.score.toFixed(3)],
                                 stage: i === 0 };
                    }), null, -1));

                var g = greedy.beams[0], bst = res.beams[0];
                ctx.stage.appendChild(A.stats([
                    { value: "“" + show(g) + "”", label: "greedy output",
                      note: "score " + g.score.toFixed(3) },
                    { value: "“" + show(bst) + "”", label: "beam " + p.width + " output",
                      note: "score " + bst.score.toFixed(3) },
                    { value: p.width === 1 ? "1" : A.commas(res.history.reduce(
                        function (a, hh) { return a + hh.all.length; }, 0)),
                      label: "sequences scored", note: "beam width " + p.width },
                    { value: show(bst) === show(wide.beams[0]) ? "yes" : "no",
                      label: "same as beam 5?",
                      note: "wider is not always different" }
                ]));

                ctx.stage.appendChild(A.note(show(g) === show(bst)
                    ? "At this width greedy and beam agree. Drop the beam to 1 and raise it " +
                      "again on the second sentence to see them disagree: greedy takes the " +
                      "best <em>next</em> word, which is not the first word of the best " +
                      "<em>sequence</em>."
                    : "Greedy returns <strong>&ldquo;" + show(g) + "&rdquo;</strong> and beam " +
                      "search returns <strong>&ldquo;" + show(bst) + "&rdquo;</strong>. " +
                      "Greedy committed to the highest-scoring second word and could not " +
                      "take it back; the sequence it needed started with a word that " +
                      "looked worse at the time."));

                ctx.stage.appendChild(A.note(
                    "The <strong>length penalty</strong> exists because every extra token " +
                    "adds a negative log-probability, so an unnormalised search prefers " +
                    "short output &mdash; it will happily stop early rather than say the " +
                    "rest of the sentence. Dividing by " +
                    "<span class='arch-mono'>((5 + |Y|) / 6)<sup>&alpha;</sup></span> with " +
                    "&alpha; = " + p.alpha.toFixed(1) + " undoes that. Set &alpha; to 0 and " +
                    "watch the model start truncating; push it past 1 and it starts padding."));

                ctx.setReadout("beam " + p.width + ", alpha " + p.alpha.toFixed(1) +
                    ": “" + show(bst) + "”  (log p " + bst.lp.toFixed(2) +
                    ", normalised " + bst.score.toFixed(3) + ")");
            };
        }
    };
})();

/* ===========================================================================
 * Generative adversarial networks
 *
 * Almost every GAN visualisation is a training run, which means it is a
 * demonstration of whether that particular run converged. This one is the
 * theory instead, and it is exact.
 *
 * For any generator, the *optimal* discriminator has a closed form:
 * D*(x) = p_data(x) / (p_data(x) + p_g(x)). No training, no seeds, no
 * instability. Substituting it into the value function turns the game into a
 * Jensen-Shannon divergence between the two distributions, whose minimum is
 * -log 4 exactly when they match. So here you *are* the generator: move the
 * distribution, and watch the optimal discriminator, the value function and
 * the divergence respond. Every number is a Riemann sum over the grid the
 * curves are drawn from, so the picture and the figures cannot disagree.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, path = A.path, line = A.line;

    var N = 481, LO = -6, HI = 6, DX = (HI - LO) / (N - 1);

    function grid() {
        var xs = [];
        for (var i = 0; i < N; i++) xs.push(LO + i * DX);
        return xs;
    }
    var XS = grid();

    function normal(mu, sd) {
        return XS.map(function (x) {
            return Math.exp(-0.5 * Math.pow((x - mu) / sd, 2)) /
                   (sd * Math.sqrt(2 * Math.PI));
        });
    }

    function mix(parts) {
        var out = new Array(N), i, k;
        for (i = 0; i < N; i++) out[i] = 0;
        parts.forEach(function (p) {
            var d = normal(p[0], p[1]);
            for (i = 0; i < N; i++) out[i] += p[2] * d[i];
        });
        return out;
    }

    var TARGETS = {
        one: { label: "one mode  -  N(1.2, 0.5)", parts: [[1.2, 0.5, 1]] },
        two: { label: "two modes  -  the mode-collapse case",
               parts: [[-1.8, 0.45, 0.5], [1.8, 0.45, 0.5]] },
        skew: { label: "two unequal modes",
                parts: [[-1.2, 0.4, 0.3], [1.5, 0.7, 0.7]] }
    };

    function stats(pd, pg) {
        var V = 0, jsd = 0, i;
        for (i = 0; i < N; i++) {
            var a = pd[i], b = pg[i], m = 0.5 * (a + b);
            if (m > 1e-12) {
                var D = a / (a + b + 1e-300);
                V += (a * Math.log(Math.max(D, 1e-300)) +
                      b * Math.log(Math.max(1 - D, 1e-300))) * DX;
                if (a > 1e-12) jsd += 0.5 * a * Math.log(a / m) * DX;
                if (b > 1e-12) jsd += 0.5 * b * Math.log(b / m) * DX;
            }
        }
        return { V: V, jsd: jsd / Math.log(2) };
    }

    /* The gradient the generator actually receives, both ways round. The
     * minimax form differentiates log(1 - D) and the non-saturating form
     * differentiates -log D; they have the same fixed point and wildly
     * different magnitudes when the two distributions barely overlap. */
    function pull(pd, mu, sd, form) {
        var eps = 0.01;
        function loss(m) {
            var pg = normal(m, sd), s = 0, i;
            for (i = 0; i < N; i++) {
                var a = pd[i], b = pg[i];
                if (a + b < 1e-12) continue;
                var D = a / (a + b);
                s += (form === "minimax"
                        ? b * Math.log(Math.max(1 - D, 1e-300))
                        : -b * Math.log(Math.max(D, 1e-300))) * DX;
            }
            return s;
        }
        return -(loss(mu + eps) - loss(mu - eps)) / (2 * eps);
    }

    function plot(pd, pg, W, H) {
        var s = svg(W, H, "arch-scene");
        var pad = 34, i;
        s.appendChild(rect(0.5, 0.5, W - 1, H - 1,
            { fill: A.SURFACE, stroke: A.BORDER, rx: 4 }));
        var maxp = 0;
        for (i = 0; i < N; i++) maxp = Math.max(maxp, pd[i], pg[i]);
        maxp = maxp || 1;
        function px(i) { return pad + i / (N - 1) * (W - 2 * pad); }
        function py(v) { return H - pad - v / maxp * (H - 2 * pad); }
        function pyD(v) { return H - pad - v * (H - 2 * pad); }

        /* the optimal discriminator, as a curve on its own 0-1 scale */
        var dd = "";
        for (i = 0; i < N; i++) {
            var t = pd[i] + pg[i];
            var D = t > 1e-12 ? pd[i] / t : 0.5;
            dd += (i ? "L" : "M") + px(i) + " " + pyD(D);
        }
        s.appendChild(line(pad, pyD(0.5), W - pad, pyD(0.5),
            { stroke: A.BORDER, dash: "4 4", sw: 0.8 }));
        s.appendChild(path(dd, { stroke: A.SERIES2, sw: 1.6 }));

        var da = "M" + px(0) + " " + py(0);
        for (i = 0; i < N; i++) da += "L" + px(i) + " " + py(pd[i]);
        da += "L" + px(N - 1) + " " + py(0) + "Z";
        s.appendChild(path(da, { fill: A.FILL, fo: 0.22, stroke: "none", sw: 0 }));

        var dg = "";
        for (i = 0; i < N; i++) dg += (i ? "L" : "M") + px(i) + " " + py(pg[i]);
        s.appendChild(path(dg, { stroke: A.ACCENT, sw: 2 }));

        s.appendChild(line(pad, H - pad, W - pad, H - pad, { stroke: A.BORDER }));
        s.appendChild(text(pad, H - 10, String(LO), { size: 8, fill: A.MUTED }));
        s.appendChild(text(W - pad, H - 10, String(HI), { size: 8, fill: A.MUTED }));
        s.appendChild(text(W - pad + 4, pyD(0.5) + 3, "0.5",
            { size: 7.5, fill: A.SERIES2, anchor: "start" }));
        s.appendChild(text(pad + 4, 16, "filled: real data     line: generator     " +
            "blue: the optimal discriminator",
            { size: 8, fill: A.MUTED, anchor: "start" }));
        return s;
    }

    /* DCGAN, so the page carries a real architecture next to the theory. */
    function dcgan(base, zdim) {
        var gen = [], dis = [], size = 4, ch = base * 8, p, i;
        var gp = zdim * (4 * 4 * ch) + 4 * 4 * ch;
        gen.push({ name: "project z and reshape", out: ch + " x 4x4", params: gp });
        while (size < 64) {
            var nch = size === 32 ? 3 : ch / 2;
            p = nch * ch * 16 + nch;
            gen.push({ name: "convT 4x4 stride 2  ->  " + nch,
                       out: nch + " x " + (size * 2) + "x" + (size * 2), params: p });
            ch = nch; size *= 2;
        }
        ch = base; size = 32;
        dis.push({ name: "conv 4x4 stride 2  ->  " + base,
                   out: base + " x 32x32", params: base * 3 * 16 + base });
        while (size > 4) {
            p = (ch * 2) * ch * 16 + ch * 2;
            dis.push({ name: "conv 4x4 stride 2  ->  " + (ch * 2),
                       out: (ch * 2) + " x " + (size / 2) + "x" + (size / 2), params: p });
            ch *= 2; size /= 2;
        }
        dis.push({ name: "conv 4x4 valid  ->  1 logit", out: "1", params: ch * 16 + 1 });
        var gt = 0, dt = 0;
        gen.forEach(function (l) { gt += l.params; });
        dis.forEach(function (l) { dt += l.params; });
        return { gen: gen, dis: dis, gp: gt, dp: dt };
    }

    A.WIDGETS.gan = {
        controls: [
            { key: "target", label: "Real distribution", type: "select", value: "two",
              id: "gan-target",
              options: Object.keys(TARGETS).map(function (k) {
                  return { value: k, label: TARGETS[k].label }; }) },
            { key: "mu", label: "Generator mean", type: "range",
              min: -4, max: 4, step: 0.05, value: 1.8, id: "gan-mu",
              fmt: function (v) { return v.toFixed(2); } },
            { key: "sd", label: "Generator spread", type: "range",
              min: 0.15, max: 3, step: 0.05, value: 0.45, id: "gan-sd",
              fmt: function (v) { return v.toFixed(2); } },
            { key: "form", label: "Generator loss", type: "select", value: "ns",
              id: "gan-form",
              options: [{ value: "ns", label: "non-saturating  -  maximise log D(G(z))" },
                        { value: "minimax", label: "minimax  -  minimise log(1 - D(G(z)))" }] },
            { key: "base", label: "DCGAN base channels", type: "range",
              min: 16, max: 128, step: 16, value: 64, id: "gan-base" }
        ],
        build: function (ctx) {
            return function draw() {
                var p = ctx.params;
                var tgt = TARGETS[p.target] || TARGETS.two;
                var pd = mix(tgt.parts), pg = normal(p.mu, p.sd);
                var st = stats(pd, pg);
                var grad = pull(pd, p.mu, p.sd, p.form);
                var gradOther = pull(pd, p.mu, p.sd,
                    p.form === "minimax" ? "ns" : "minimax");

                ctx.stage.innerHTML = "";
                var wrap = h("div", "arch-scroll");
                wrap.appendChild(plot(pd, pg, 560, 260));
                ctx.stage.appendChild(wrap);
                ctx.stage.appendChild(A.caption(
                    "You are the generator. Move it and the optimal discriminator " +
                    "re-derives itself instantly, because it has a closed form."));

                var atEq = Math.abs(st.V + Math.log(4)) < 0.02;
                ctx.stage.appendChild(A.stats([
                    { value: st.V.toFixed(3), label: "V(D*, G)",
                      note: atEq ? "-log 4, the equilibrium" : "-log 4 = -1.386 is the floor" },
                    { value: st.jsd.toFixed(3) + " bits", label: "Jensen-Shannon divergence",
                      note: st.jsd < 0.02 ? "the distributions match" : "0 when they match" },
                    { value: (grad >= 0 ? "+" : "") + grad.toFixed(3),
                      label: "gradient pulling the mean",
                      note: Math.abs(grad) < 0.02 ? "no signal at all" : "toward the data" },
                    { value: Math.abs(grad) > 1e-9
                             ? (Math.abs(gradOther) / Math.abs(grad)).toFixed(2) + "x"
                             : "-",
                      label: "the other loss, relative",
                      note: p.form === "ns" ? "minimax vs this" : "non-saturating vs this" }
                ]));

                var overlap = 0;
                for (var i = 0; i < N; i++) overlap += Math.min(pd[i], pg[i]) * DX;

                ctx.stage.appendChild(A.note(
                    "Substituting the optimal discriminator into the value function gives " +
                    "<span class='arch-mono'>V(D*, G) = &minus;log 4 + 2 &middot; JSD(p<sub>" +
                    "data</sub> &#8214; p<sub>g</sub>)</span>. The generator is therefore " +
                    "minimising a Jensen-Shannon divergence, and the game's equilibrium is " +
                    "not a compromise &mdash; it is the single point where the two " +
                    "distributions are identical and the discriminator is reduced to " +
                    "answering 0.5 everywhere. Right now the overlap is <strong>" +
                    (100 * overlap).toFixed(1) + "%</strong> and the divergence is " +
                    st.jsd.toFixed(3) + " bits."));

                if (overlap < 0.06)
                    ctx.stage.appendChild(A.note(
                        "This is the <strong>vanishing gradient</strong> everyone hits. With " +
                        "almost no overlap the optimal discriminator is right about " +
                        "everything, <span class='arch-mono'>D* &asymp; 0</span> under the " +
                        "generator, and <span class='arch-mono'>log(1 &minus; D*)</span> is " +
                        "flat there &mdash; so the minimax gradient is " +
                        Math.abs(pull(pd, p.mu, p.sd, "minimax")).toFixed(4) +
                        " while the non-saturating one is " +
                        Math.abs(pull(pd, p.mu, p.sd, "ns")).toFixed(4) +
                        ". Same fixed point, and only one of them can be trained from here. " +
                        "That single change is why the original paper recommends the " +
                        "non-saturating form in the same section that derives the other."));

                if (p.target !== "one" && p.sd < 0.9 && st.jsd > 0.15)
                    ctx.stage.appendChild(A.note(
                        "<strong>Mode collapse, exactly.</strong> The generator here is a " +
                        "single Gaussian, so it <em>cannot</em> cover two separated modes; " +
                        "sitting on one of them scores far better than straddling the gap " +
                        "between them. A real generator has the capacity to cover both and " +
                        "collapses anyway, for the same reason: the discriminator only ever " +
                        "says how real a sample looks, never that the samples are all the " +
                        "same, so nothing in the objective as written punishes producing one " +
                        "excellent output forever."));

                /* the architecture, so the theory has a body */
                var m = dcgan(p.base, 100);
                ctx.stage.appendChild(A.section("A DCGAN at 64 x 64, layer by layer"));
                ctx.stage.appendChild(A.layerTable(
                    ["generator", "output", "params"],
                    m.gen.map(function (l) {
                        return { cells: [l.name, l.out, A.fmt(l.params)] };
                    }).concat([{ cells: ["total", "3 x 64x64", A.fmt(m.gp)], stage: true }]),
                    null, -1));
                ctx.stage.appendChild(A.layerTable(
                    ["discriminator", "output", "params"],
                    m.dis.map(function (l) {
                        return { cells: [l.name, l.out, A.fmt(l.params)] };
                    }).concat([{ cells: ["total", "1 logit", A.fmt(m.dp)], stage: true }]),
                    null, -1));
                ctx.stage.appendChild(A.note(
                    "The two networks are near mirror images, which is not a coincidence: " +
                    "if the discriminator is much stronger it wins immediately and the " +
                    "generator's gradient vanishes; much weaker and its judgement is noise. " +
                    "Here they are " + A.fmt(m.gp) + " and " + A.fmt(m.dp) +
                    " parameters. DCGAN's other rules &mdash; strided convolutions instead " +
                    "of pooling, batch norm in both, no fully-connected hidden layers, " +
                    "LeakyReLU in the discriminator &mdash; are all stability patches on " +
                    "the same problem."));

                ctx.setReadout("generator N(" + p.mu.toFixed(2) + ", " + p.sd.toFixed(2) +
                    "): V(D*,G) = " + st.V.toFixed(3) + ", JSD = " + st.jsd.toFixed(3) +
                    " bits, overlap " + (100 * overlap).toFixed(1) + "%");
            };
        }
    };
})();

/* ===========================================================================
 * Autoencoders
 *
 * A linear autoencoder trained to convergence spans exactly the same subspace
 * as the top principal components (Baldi & Hornik, 1989). That is not a
 * simplification made for a web page - it is a theorem, and it means the
 * whole encoder-bottleneck-decoder story can be computed here in closed form
 * instead of trained. Move the bottleneck and the reconstruction changes with
 * no random seed anywhere; the error curve is the tail sum of the eigenvalues,
 * which is why it is smooth rather than noisy.
 *
 * The non-linear case is what a real autoencoder buys, and the page says so
 * rather than pretending PCA is the whole subject.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, path = A.path, line = A.line;

    var G = 8, D = G * G;

    /* Six shapes, jittered - a dataset with obvious low-dimensional structure
     * so the reader can see what each component picked up. */
    function dataset() {
        var r = A.rng(17), X = [], labels = [];
        var shapes = ["bar |", "bar -", "cross", "diagonal", "ring", "corner"];
        for (var n = 0; n < 90; n++) {
            var k = n % 6, img = new Float64Array(D);
            var ox = Math.floor(r() * 3) - 1, oy = Math.floor(r() * 3) - 1;
            var t = r() < 0.5 ? 1 : 2;
            function set(x, y, v) {
                x += ox; y += oy;
                if (x >= 0 && y >= 0 && x < G && y < G)
                    img[y * G + x] = Math.max(img[y * G + x], v === undefined ? 1 : v);
            }
            var i, j;
            if (k === 0) for (i = 1; i < 7; i++) for (j = 0; j < t; j++) set(3 + j, i);
            if (k === 1) for (i = 1; i < 7; i++) for (j = 0; j < t; j++) set(i, 3 + j);
            if (k === 2) for (i = 1; i < 7; i++) { set(3, i); set(i, 3); }
            if (k === 3) for (i = 1; i < 7; i++) { set(i, i); if (t > 1) set(i, i + 1); }
            if (k === 4) for (i = 1; i < 7; i++) { set(i, 1); set(i, 6); set(1, i); set(6, i); }
            if (k === 5) for (i = 1; i < 5; i++) { set(1, i); set(i, 1); }
            for (i = 0; i < D; i++) img[i] += 0.04 * r();
            X.push(img); labels.push(shapes[k]);
        }
        return { X: X, labels: labels };
    }

    var DATA = dataset();

    /* Principal components by power iteration with deflation - the same
     * routine the word-vector modules use, on a 64-dimensional covariance. */
    var PCACACHE = null;
    function pca(kmax) {
        if (PCACACHE && PCACACHE.k >= kmax) return PCACACHE;
        var X = DATA.X, n = X.length, i, j, k;
        var mean = new Float64Array(D);
        X.forEach(function (v) { for (i = 0; i < D; i++) mean[i] += v[i] / n; });
        var Y = X.map(function (v) {
            var o = new Float64Array(D);
            for (i = 0; i < D; i++) o[i] = v[i] - mean[i];
            return o;
        });
        var C = [];
        for (i = 0; i < D; i++) C.push(new Float64Array(D));
        Y.forEach(function (v) {
            for (i = 0; i < D; i++) for (j = 0; j < D; j++) C[i][j] += v[i] * v[j] / n;
        });
        var total = 0;
        for (i = 0; i < D; i++) total += C[i][i];
        var r = A.rng(11), comps = [], lams = [];
        for (k = 0; k < Math.max(kmax, 16); k++) {
            var v = new Float64Array(D);
            for (i = 0; i < D; i++) v[i] = r() - 0.5;
            for (var it = 0; it < 220; it++) {
                var w = new Float64Array(D), nn = 0;
                for (i = 0; i < D; i++) {
                    for (j = 0; j < D; j++) w[i] += C[i][j] * v[j];
                }
                for (i = 0; i < D; i++) nn += w[i] * w[i];
                nn = Math.sqrt(nn) || 1;
                for (i = 0; i < D; i++) v[i] = w[i] / nn;
            }
            var lam = 0;
            for (i = 0; i < D; i++) for (j = 0; j < D; j++) lam += v[i] * C[i][j] * v[j];
            comps.push(v); lams.push(Math.max(0, lam));
            for (i = 0; i < D; i++) for (j = 0; j < D; j++) C[i][j] -= lam * v[i] * v[j];
        }
        PCACACHE = { k: comps.length, mean: mean, comps: comps, lams: lams, total: total };
        return PCACACHE;
    }

    function encode(x, P, k) {
        var z = [], i, d;
        for (i = 0; i < k; i++) {
            var s = 0;
            for (d = 0; d < D; d++) s += (x[d] - P.mean[d]) * P.comps[i][d];
            z.push(s);
        }
        return z;
    }

    function decode(z, P) {
        var out = new Float64Array(D), i, d;
        for (d = 0; d < D; d++) out[d] = P.mean[d];
        for (i = 0; i < z.length; i++)
            for (d = 0; d < D; d++) out[d] += z[i] * P.comps[i][d];
        return out;
    }

    function tile(img, size, label, signed) {
        var pad = label ? 14 : 0;
        var s = svg(size, size + pad, "arch-tile");
        var c = size / G, lo = 0, hi = 0, i;
        for (i = 0; i < D; i++) { lo = Math.min(lo, img[i]); hi = Math.max(hi, img[i]); }
        var span = Math.max(Math.abs(lo), Math.abs(hi)) || 1;
        for (var y = 0; y < G; y++) for (var x = 0; x < G; x++) {
            var v = img[y * G + x];
            var o = signed ? Math.abs(v) / span : A.clamp(v / (hi || 1), 0, 1);
            s.appendChild(rect(x * c, pad + y * c, c, c, {
                fill: signed && v < 0 ? A.SERIES2 : A.FILL,
                fo: o * 0.95, stroke: A.BORDER, sw: 0.25, rx: 0
            }));
        }
        if (label) s.appendChild(text(size / 2, 10, label, { size: 8, fill: A.MUTED }));
        return s;
    }

    function errorCurve(P, kNow) {
        var W = 380, H = 160, pad = 32;
        var s = svg(W, H, "arch-scene");
        s.appendChild(rect(0.5, 0.5, W - 1, H - 1,
            { fill: A.SURFACE, stroke: A.BORDER, rx: 4 }));
        var kmax = 16, tail = [], i, j;
        for (i = 0; i <= kmax; i++) {
            /* Residual variance after k components is the trace minus the
             * first k eigenvalues, which is the reconstruction MSE times D. */
            var t = P.total;
            for (j = 0; j < i; j++) t -= P.lams[j];
            tail.push(Math.max(0, t) / D);
        }
        var max = tail[0] || 1, d = "";
        for (i = 0; i <= kmax; i++) {
            var x = pad + i / kmax * (W - 2 * pad);
            var y = H - pad - tail[i] / max * (H - 2 * pad);
            d += (i ? "L" : "M") + x + " " + y;
            if (i === kNow)
                s.appendChild(A.circle(x, y, 3.2,
                    { fill: A.ACCENT, stroke: "none", sw: 0 }));
        }
        s.appendChild(path(d, { stroke: A.ACCENT, sw: 1.8 }));
        s.appendChild(line(pad, H - pad, W - pad, H - pad, { stroke: A.BORDER }));
        s.appendChild(text(W / 2, H - 8, "bottleneck size k", { size: 8.5, fill: A.MUTED }));
        s.appendChild(text(pad - 4, pad, "MSE", { size: 8, fill: A.MUTED, anchor: "end" }));
        return s;
    }

    A.WIDGETS.autoencoder = {
        controls: [
            { key: "k", label: "Bottleneck size", type: "range",
              min: 1, max: 16, step: 1, value: 4, id: "ae-k",
              fmt: function (v) { return v + " of " + D; } },
            { key: "sample", label: "Input", type: "select", value: "0", id: "ae-sample",
              options: [0, 1, 2, 3, 4, 5].map(function (i) {
                  return { value: String(i), label: DATA.labels[i] }; }) },
            { key: "noise", label: "Corrupt the input", type: "range",
              min: 0, max: 0.8, step: 0.05, value: 0, id: "ae-noise",
              fmt: function (v) { return v.toFixed(2); } },
            { key: "z1", label: "Latent 1", type: "range",
              min: -3, max: 3, step: 0.1, value: 0, id: "ae-z1",
              fmt: function (v) { return v.toFixed(1); } },
            { key: "z2", label: "Latent 2", type: "range",
              min: -3, max: 3, step: 0.1, value: 0, id: "ae-z2",
              fmt: function (v) { return v.toFixed(1); } }
        ],
        build: function (ctx) {
            return function draw() {
                var p = ctx.params, k = p.k;
                var P = pca(k);
                var idx = parseInt(p.sample, 10);
                var clean = DATA.X[idx];
                var r = A.rng(101 + idx), i;
                var noisy = new Float64Array(D);
                for (i = 0; i < D; i++)
                    noisy[i] = A.clamp(clean[i] + p.noise * (r() - 0.5) * 2, 0, 1.2);
                var z = encode(noisy, P, k);
                var recon = decode(z, P);

                var mseIn = 0, mseOut = 0;
                for (i = 0; i < D; i++) {
                    mseIn += Math.pow(noisy[i] - clean[i], 2) / D;
                    mseOut += Math.pow(recon[i] - clean[i], 2) / D;
                }
                /* The denominator is the covariance trace, not the sum of the
                 * components we happened to extract - otherwise "variance
                 * retained" is measured against 16 directions rather than 64
                 * and reads far too high. */
                var kept = 0, tot = P.total;
                for (i = 0; i < k; i++) kept += P.lams[i];

                ctx.stage.innerHTML = "";

                /* the pipeline, as tiles */
                var row = h("div", "arch-pair arch-pair-4");
                row.appendChild(tile(clean, 92, "original"));
                row.appendChild(tile(noisy, 92, p.noise > 0 ? "corrupted input" : "input"));
                var zt = h("div", "arch-latent");
                zt.appendChild(h("span", "arch-latent-label", "z  (" + k + " numbers)"));
                var bars = h("div", "arch-latent-bars");
                z.forEach(function (v) {
                    var b = h("div", "arch-latent-bar");
                    var f = h("div", "arch-latent-fill");
                    var mag = Math.min(1, Math.abs(v) / 3);
                    f.style.height = (8 + 84 * mag).toFixed(1) + "%";
                    f.style.opacity = String(0.35 + 0.65 * mag);
                    b.appendChild(f);
                    b.title = v.toFixed(3);
                    bars.appendChild(b);
                });
                zt.appendChild(bars);
                row.appendChild(zt);
                row.appendChild(tile(recon, 92, "reconstruction"));
                ctx.stage.appendChild(row);

                ctx.stage.appendChild(A.stats([
                    { value: (D / k).toFixed(1) + "x", label: "compression",
                      note: D + " numbers into " + k },
                    { value: (100 * kept / tot).toFixed(1) + "%",
                      label: "variance retained", note: "sum of the top " + k + " eigenvalues" },
                    { value: mseOut.toFixed(4), label: "reconstruction MSE",
                      note: "against the clean image" },
                    { value: p.noise > 0 ? mseIn.toFixed(4) : "-",
                      label: "MSE of the corrupted input",
                      note: p.noise > 0 && mseOut < mseIn
                            ? "the bottleneck removed noise" : "no corruption" }
                ]));

                if (p.noise > 0)
                    ctx.stage.appendChild(A.note(mseOut < mseIn
                        ? "The reconstruction is <strong>closer to the clean image than the " +
                          "input was</strong> (" + mseOut.toFixed(4) + " against " +
                          mseIn.toFixed(4) + "). Nothing here was trained to remove noise. " +
                          "The noise is spread across all " + D + " directions, the " +
                          "bottleneck keeps only " + k + " of them, and so most of it has " +
                          "nowhere to go. A denoising autoencoder makes this the explicit " +
                          "objective &mdash; corrupt the input, ask for the clean target " +
                          "&mdash; which pushes the same effect much further."
                        : "At k = " + k + " the bottleneck is wide enough to pass a good " +
                          "deal of the noise through with the signal. Narrow it and the " +
                          "noise is the first thing to go, because it is the part of the " +
                          "image that no principal direction accounts for."));

                /* what the encoder learned */
                ctx.stage.appendChild(A.section("What each latent dimension encodes"));
                var comps = h("div", "arch-pair arch-pair-6");
                for (i = 0; i < Math.min(6, k); i++)
                    comps.appendChild(tile(P.comps[i], 74,
                        "z" + (i + 1) + "  " + (100 * P.lams[i] / tot).toFixed(0) + "%", true));
                ctx.stage.appendChild(comps);
                ctx.stage.appendChild(A.caption(
                    "Each is one decoder column: the image added to the reconstruction when " +
                    "that latent is +1. Blue is negative. The reconstruction is the mean " +
                    "image plus these, weighted by z."));

                /* the traversal */
                var trav = decode([p.z1, p.z2].slice(0, Math.min(2, k)), P);
                ctx.stage.appendChild(A.section("Decoding a latent you choose"));
                var t2 = h("div", "arch-pair arch-pair-3");
                t2.appendChild(tile(P.mean, 92, "z = 0  (the mean)"));
                t2.appendChild(tile(trav, 92,
                    "z = (" + p.z1.toFixed(1) + ", " + p.z2.toFixed(1) + ")"));
                t2.appendChild(errorCurve(P, k));
                ctx.stage.appendChild(t2);
                ctx.stage.appendChild(A.caption(
                    "The decoder is a function you can evaluate anywhere, not only at points " +
                    "that came from real data. The curve on the right is reconstruction error " +
                    "against bottleneck size - the tail sum of the eigenvalues, exactly."));

                ctx.stage.appendChild(A.note(
                    "A <strong>linear</strong> autoencoder trained to convergence spans the " +
                    "same subspace as the top-k principal components, which is why this page " +
                    "can compute it in closed form. Everything a real autoencoder adds comes " +
                    "from breaking that linearity: with non-linear layers the latent space can " +
                    "curve to follow a manifold that no straight subspace fits, and the " +
                    "encoder can be convolutional so that a shifted image is not a completely " +
                    "different vector. The <em>architecture</em> is the same three parts " +
                    "either way &mdash; encoder, bottleneck, decoder &mdash; and the " +
                    "bottleneck is the only one doing the work."));

                ctx.stage.appendChild(A.section("A convolutional autoencoder, 28 x 28"));
                ctx.stage.appendChild(A.layerTable(
                    ["stage", "layer", "output", "params"],
                    [{ cells: ["encoder", "conv 3x3 s2, 1 -> 16", "16 x 14x14", "160"] },
                     { cells: ["encoder", "conv 3x3 s2, 16 -> 32", "32 x 7x7", "4,640"] },
                     { cells: ["encoder", "flatten + fc 1568 -> " + k,
                               String(k), A.commas(1568 * k + k)], stage: true },
                     { cells: ["decoder", "fc " + k + " -> 1568",
                               "32 x 7x7", A.commas(k * 1568 + 1568)], stage: true },
                     { cells: ["decoder", "convT 3x3 s2, 32 -> 16", "16 x 14x14", "4,624"] },
                     { cells: ["decoder", "convT 3x3 s2, 16 -> 1", "1 x 28x28", "145"] }],
                    null, -1));

                ctx.setReadout("k = " + k + " of " + D + ", " +
                    (100 * kept / tot).toFixed(1) + "% of the variance kept, " +
                    "reconstruction MSE " + mseOut.toFixed(4));
            };
        }
    };
})();

/* ===========================================================================
 * A ratings matrix, shared by the collaborative-filtering and deep-recommender
 * modules.
 *
 * Ten people, twelve titles, three genres, and a fifth of the observed
 * ratings held out so that every method on both pages is scored on data none
 * of them fitted. It is small enough to print in full - which is the point,
 * because a reader who can see the whole matrix can check by eye whether a
 * "similar user" really is similar.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch;

    /* Sixteen people and fifteen titles rather than the ten by twelve this
     * started as. The smaller matrix left only seventeen held-out ratings,
     * and at that size the difference between two methods was inside the
     * noise - the ordering of the comparison bars changed with the random
     * seed, which is worse than useless on a page whose point is that the
     * comparison is real. Forty test cells is still small and the page says
     * so, but the ordering is stable. */
    var USERS = ["Ada", "Bala", "Chen", "Dara", "Eze", "Fay", "Gil", "Hana",
                 "Ivo", "Juno", "Kai", "Lena", "Mira", "Noor", "Omar", "Pia"];
    var ITEMS = ["Nebula", "Starfall", "Void Run", "Ion", "Orbit",
                 "Two Hearts", "June", "Sweet Hour", "Postcards", "Letters",
                 "Deep Ice", "Wildlife", "The Reef", "Volcano", "Tide"];
    var GENRE = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2];
    var GENRES = ["sci-fi", "romance", "documentary"];
    var TASTE = [
        [1, .1, .3], [.9, .2, .4], [.2, 1, .2], [.1, .9, .3],
        [.3, .2, 1], [.2, .3, .9], [1, .8, .1], [.15, .95, .85],
        [.85, .15, .2], [.25, .85, .25], [.95, .25, .35], [.3, .95, .15],
        [.2, .35, .95], [.9, .3, .85], [.35, .15, .9], [.15, .8, .4]];

    /* Ratings live on a 1-5 scale, so a prediction outside it is not a
     * prediction. Neighbourhood methods extrapolate past the ends routinely -
     * a user mean of 4.2 plus a positive deviation lands at 5.4 - and every
     * real implementation clips. Leaving it out costs about a tenth of an
     * RMSE point and puts numbers on screen that cannot be ratings. */
    function clip(v) { return v < 1 ? 1 : (v > 5 ? 5 : v); }

    var NU = USERS.length, NI = ITEMS.length;
    var R = [], OBS = [], TRAIN = [], TEST = [];
    (function () {
        var r = A.rng(31), u, i;
        for (u = 0; u < NU; u++) {
            R.push(new Float64Array(NI));
            OBS.push(new Uint8Array(NI));
            for (i = 0; i < NI; i++) {
                var a = TASTE[u][GENRE[i]] + 0.12 * (r() - 0.5) * 2;
                R[u][i] = Math.max(1, Math.min(5, Math.round(1 + 4 * a)));
                OBS[u][i] = r() < 0.72 ? 1 : 0;
            }
        }
        var r2 = A.rng(77);
        for (u = 0; u < NU; u++) TRAIN.push(Uint8Array.from(OBS[u]));
        for (u = 0; u < NU; u++) for (i = 0; i < NI; i++)
            if (OBS[u][i] && r2() < 0.22) { TEST.push([u, i]); TRAIN[u][i] = 0; }
    })();

    function userMeans() {
        var out = [], u, i;
        for (u = 0; u < NU; u++) {
            var s = 0, n = 0;
            for (i = 0; i < NI; i++) if (TRAIN[u][i]) { s += R[u][i]; n++; }
            out.push(n ? s / n : 3);
        }
        return out;
    }
    function itemMeans() {
        var out = [], u, i;
        for (i = 0; i < NI; i++) {
            var s = 0, n = 0;
            for (u = 0; u < NU; u++) if (TRAIN[u][i]) { s += R[u][i]; n++; }
            out.push(n ? s / n : 3);
        }
        return out;
    }
    var UMEAN = userMeans(), IMEAN = itemMeans();
    var GLOBAL = (function () {
        var s = 0, n = 0, u, i;
        for (u = 0; u < NU; u++) for (i = 0; i < NI; i++)
            if (TRAIN[u][i]) { s += R[u][i]; n++; }
        return s / n;
    })();

    function rmse(predict) {
        var se = 0;
        TEST.forEach(function (t) {
            var d = clip(predict(t[0], t[1])) - R[t[0]][t[1]];
            se += d * d;
        });
        return Math.sqrt(se / TEST.length);
    }

    window.VizArchRatings = {
        USERS: USERS, ITEMS: ITEMS, GENRE: GENRE, GENRES: GENRES,
        NU: NU, NI: NI, R: R, OBS: OBS, TRAIN: TRAIN, TEST: TEST,
        UMEAN: UMEAN, IMEAN: IMEAN, GLOBAL: GLOBAL, rmse: rmse, clip: clip
    };
})();

/* ===========================================================================
 * Collaborative filtering
 *
 * Four methods on one matrix, all scored on the same held-out ratings, with
 * the arithmetic for the selected cell printed underneath. The point a table
 * of formulas cannot make is that the neighbour weights are doing something
 * you can check: Ada's nearest neighbour by Pearson correlation really is the
 * other person who liked the same four sci-fi titles, and you can see both
 * rows on screen.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch, T = window.VizArchRatings;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text;

    function pearson(xs, ys, mx, my) {
        var sab = 0, sa = 0, sb = 0, n = xs.length, i;
        for (i = 0; i < n; i++) {
            var x = xs[i] - mx, y = ys[i] - my;
            sab += x * y; sa += x * x; sb += y * y;
        }
        if (n < 2 || sa <= 0 || sb <= 0) return 0;
        return sab / Math.sqrt(sa * sb);
    }

    function cosine(xs, ys) {
        var sab = 0, sa = 0, sb = 0, i;
        for (i = 0; i < xs.length; i++) {
            sab += xs[i] * ys[i]; sa += xs[i] * xs[i]; sb += ys[i] * ys[i];
        }
        if (sa <= 0 || sb <= 0) return 0;
        return sab / Math.sqrt(sa * sb);
    }

    function userSim(a, b, kind) {
        var xs = [], ys = [], i;
        for (i = 0; i < T.NI; i++) if (T.TRAIN[a][i] && T.TRAIN[b][i]) {
            xs.push(T.R[a][i]); ys.push(T.R[b][i]);
        }
        if (xs.length < 2) return 0;
        return kind === "cosine" ? cosine(xs, ys)
                                 : pearson(xs, ys, T.UMEAN[a], T.UMEAN[b]);
    }

    function itemSim(a, b, kind) {
        var xs = [], ys = [], u;
        for (u = 0; u < T.NU; u++) if (T.TRAIN[u][a] && T.TRAIN[u][b]) {
            xs.push(T.R[u][a]); ys.push(T.R[u][b]);
        }
        if (xs.length < 2) return 0;
        return kind === "cosine" ? cosine(xs, ys)
                                 : pearson(xs, ys, T.IMEAN[a], T.IMEAN[b]);
    }

    function neighboursU(u, i, k, kind) {
        var c = [], v;
        for (v = 0; v < T.NU; v++) {
            if (v === u || !T.TRAIN[v][i]) continue;
            var s = userSim(u, v, kind);
            if (s > 0) c.push({ id: v, sim: s, rating: T.R[v][i] });
        }
        c.sort(function (a, b) { return b.sim - a.sim; });
        return c.slice(0, k);
    }

    function neighboursI(u, i, k, kind) {
        var c = [], j;
        for (j = 0; j < T.NI; j++) {
            if (j === i || !T.TRAIN[u][j]) continue;
            var s = itemSim(i, j, kind);
            if (s > 0) c.push({ id: j, sim: s, rating: T.R[u][j] });
        }
        c.sort(function (a, b) { return b.sim - a.sim; });
        return c.slice(0, k);
    }

    var MFC = {};
    function mf(f, reg, steps) {
        var key = f + "|" + reg + "|" + steps;
        if (MFC[key]) return MFC[key];
        var r = A.rng(5), P = [], Q = [], u, i, d;
        var bu = new Float64Array(T.NU), bi = new Float64Array(T.NI);
        for (u = 0; u < T.NU; u++) {
            var a = [];
            for (d = 0; d < f; d++) a.push((r() - 0.5) * 0.2);
            P.push(a);
        }
        for (i = 0; i < T.NI; i++) {
            var b = [];
            for (d = 0; d < f; d++) b.push((r() - 0.5) * 0.2);
            Q.push(b);
        }
        var ent = [];
        for (u = 0; u < T.NU; u++) for (i = 0; i < T.NI; i++)
            if (T.TRAIN[u][i]) ent.push([u, i]);
        var lr = 0.02;
        for (var s = 0; s < steps; s++) {
            for (var n = 0; n < ent.length; n++) {
                u = ent[n][0]; i = ent[n][1];
                var p = T.GLOBAL + bu[u] + bi[i];
                for (d = 0; d < f; d++) p += P[u][d] * Q[i][d];
                var e = T.R[u][i] - p;
                bu[u] += lr * (e - reg * bu[u]);
                bi[i] += lr * (e - reg * bi[i]);
                for (d = 0; d < f; d++) {
                    var pu = P[u][d];
                    P[u][d] += lr * (e * Q[i][d] - reg * pu);
                    Q[i][d] += lr * (e * pu - reg * Q[i][d]);
                }
            }
        }
        var res = {
            P: P, Q: Q, bu: bu, bi: bi,
            predict: function (uu, ii) {
                var p = T.GLOBAL + bu[uu] + bi[ii];
                for (var dd = 0; dd < f; dd++) p += P[uu][dd] * Q[ii][dd];
                return p;
            }
        };
        MFC[key] = res;
        return res;
    }

    function matrix(sel, pick) {
        var cw = 42, rh = 22, padL = 54, padT = 58;
        var s = svg(padL + T.NI * cw + 8, padT + T.NU * rh + 24, "arch-scene");
        var u, i;
        for (i = 0; i < T.NI; i++) {
            var t = text(padL + i * cw + cw / 2, padT - 6, T.ITEMS[i],
                { size: 8, fill: A.MUTED, anchor: "start" });
            t.setAttribute("transform", "rotate(-52 " + (padL + i * cw + cw / 2) +
                " " + (padT - 6) + ")");
            s.appendChild(t);
        }
        for (u = 0; u < T.NU; u++) {
            s.appendChild(text(padL - 6, padT + u * rh + 15, T.USERS[u],
                { size: 8.5, anchor: "end",
                  fill: sel[0] === u ? A.ACCENT : A.MUTED }));
            for (i = 0; i < T.NI; i++) {
                var known = T.TRAIN[u][i], isTest = T.OBS[u][i] && !known;
                var hot = sel[0] === u && sel[1] === i;
                var r = rect(padL + i * cw, padT + u * rh, cw - 2, rh - 2, {
                    fill: known ? A.FILL : "none",
                    fo: known ? 0.12 + 0.19 * T.R[u][i] : 0,
                    stroke: hot ? A.ACCENT : (isTest ? A.SERIES2 : A.BORDER),
                    sw: hot ? 2 : (isTest ? 1.1 : 0.4), rx: 2
                });
                r.style.cursor = "pointer";
                (function (a, b) {
                    r.addEventListener("click", function () { pick(a, b); });
                })(u, i);
                s.appendChild(r);
                s.appendChild(text(padL + i * cw + (cw - 2) / 2, padT + u * rh + 14,
                    known ? String(T.R[u][i]) : (isTest ? "?" : "·"),
                    { size: 9, fill: known ? A.MAIN : (isTest ? A.SERIES2 : A.MUTED) }));
            }
        }
        s.appendChild(text(padL, padT + T.NU * rh + 16,
            "blue: held out for testing        dot: never rated        click any cell",
            { size: 8, fill: A.MUTED, anchor: "start" }));
        return s;
    }

    A.WIDGETS.collaborative = {
        controls: [
            { key: "method", label: "Method", type: "select", value: "userknn",
              id: "cf-method",
              options: [{ value: "userknn", label: "user-based k nearest neighbours" },
                        { value: "itemknn", label: "item-based k nearest neighbours" },
                        { value: "mf", label: "matrix factorisation" },
                        { value: "usermean", label: "the user's own average" },
                        { value: "global", label: "the global average" }] },
            { key: "sim", label: "Similarity", type: "select", value: "pearson",
              id: "cf-sim",
              options: [{ value: "pearson", label: "Pearson - centred on each mean" },
                        { value: "cosine", label: "cosine - raw ratings" }] },
            { key: "k", label: "Neighbours k", type: "range",
              min: 1, max: 9, step: 1, value: 3, id: "cf-k" },
            { key: "factors", label: "Latent factors", type: "range",
              min: 1, max: 8, step: 1, value: 3, id: "cf-factors" },
            { key: "reg", label: "Regularisation", type: "range",
              min: 0.01, max: 0.4, step: 0.01, value: 0.12, id: "cf-reg",
              fmt: function (v) { return v.toFixed(2); } }
        ],
        build: function (ctx) {
            var sel = [0, 0];
            function pick(u, i) { sel = [u, i]; ctx.redraw(); }
            return function draw() {
                var p = ctx.params;
                var model = mf(p.factors, p.reg, 400);

                function predict(u, i) {
                    if (p.method === "global") return T.GLOBAL;
                    if (p.method === "usermean") return T.UMEAN[u];
                    if (p.method === "mf") return model.predict(u, i);
                    var nb = p.method === "itemknn"
                        ? neighboursI(u, i, p.k, p.sim)
                        : neighboursU(u, i, p.k, p.sim);
                    var base = p.method === "itemknn" ? T.IMEAN[i] : T.UMEAN[u];
                    var num = 0, den = 0;
                    nb.forEach(function (q) {
                        var centre = p.method === "itemknn" ? T.IMEAN[q.id] : T.UMEAN[q.id];
                        num += q.sim * (q.rating - centre);
                        den += Math.abs(q.sim);
                    });
                    return den > 0 ? base + num / den : base;
                }

                ctx.stage.innerHTML = "";
                var wrap = h("div", "arch-scroll");
                wrap.appendChild(matrix(sel, pick));
                ctx.stage.appendChild(wrap);

                var u = sel[0], i = sel[1];
                var pred = T.clip(predict(u, i));
                var truth = T.OBS[u][i] ? T.R[u][i] : null;

                ctx.stage.appendChild(A.stats([
                    { value: T.USERS[u] + " / " + T.ITEMS[i], label: "selected cell",
                      note: T.GENRES[T.GENRE[i]] },
                    { value: pred.toFixed(2), label: "predicted rating",
                      note: p.method },
                    { value: truth === null ? "unknown" : String(truth),
                      label: "actual rating",
                      note: truth === null ? "never rated"
                            : (T.TRAIN[u][i] ? "in the training set" : "held out") },
                    { value: T.rmse(predict).toFixed(3), label: "test RMSE",
                      note: "over " + T.TEST.length + " held-out ratings" }
                ]));

                if (p.method === "userknn" || p.method === "itemknn") {
                    var nb = p.method === "itemknn"
                        ? neighboursI(u, i, p.k, p.sim)
                        : neighboursU(u, i, p.k, p.sim);
                    ctx.stage.appendChild(A.section(
                        p.method === "itemknn"
                            ? "Items " + T.USERS[u] + " rated, most like " + T.ITEMS[i]
                            : "People most like " + T.USERS[u] + " who rated " + T.ITEMS[i]));
                    if (!nb.length) {
                        ctx.stage.appendChild(A.note(
                            "No positively-correlated neighbour has rated this. The " +
                            "prediction falls back to the average, which is the honest " +
                            "answer &mdash; and this is exactly the sparsity problem that " +
                            "makes neighbourhood methods fragile on real catalogues, where " +
                            "any two users have almost nothing in common."));
                    } else {
                        var base = p.method === "itemknn" ? T.IMEAN[i] : T.UMEAN[u];
                        var num = 0, den = 0;
                        ctx.stage.appendChild(A.layerTable(
                            [p.method === "itemknn" ? "item" : "person", "similarity",
                             "their rating", "deviation from their mean", "contribution"],
                            nb.map(function (q, ix) {
                                var centre = p.method === "itemknn"
                                    ? T.IMEAN[q.id] : T.UMEAN[q.id];
                                num += q.sim * (q.rating - centre);
                                den += Math.abs(q.sim);
                                return { cells: [
                                    p.method === "itemknn" ? T.ITEMS[q.id] : T.USERS[q.id],
                                    q.sim.toFixed(3), String(q.rating),
                                    (q.rating - centre >= 0 ? "+" : "") +
                                        (q.rating - centre).toFixed(2),
                                    (q.sim * (q.rating - centre)).toFixed(3)],
                                    stage: ix === 0 };
                            }), null, -1));
                        ctx.stage.appendChild(A.note(
                            "<span class='arch-mono'>prediction = " + base.toFixed(2) +
                            " + (" + num.toFixed(3) + ") / " + den.toFixed(3) + " = " +
                            pred.toFixed(2) + "</span><br>" +
                            "The deviations, not the ratings, are averaged. Someone who " +
                            "rates everything 4 and someone who rates everything 2 can still " +
                            "agree perfectly about which titles they prefer, and centring " +
                            "each on their own mean is what lets the method notice that."));
                    }
                } else if (p.method === "mf") {
                    ctx.stage.appendChild(A.section("The factorisation for this cell"));
                    var terms = [];
                    for (var d = 0; d < p.factors; d++)
                        terms.push((model.P[u][d] * model.Q[i][d]).toFixed(3));
                    ctx.stage.appendChild(A.note(
                        "<span class='arch-mono'>" + pred.toFixed(2) + " = &mu; " +
                        T.GLOBAL.toFixed(2) + "  +  b<sub>" + T.USERS[u] + "</sub> " +
                        (model.bu[u] >= 0 ? "+" : "") + model.bu[u].toFixed(2) +
                        "  +  b<sub>" + T.ITEMS[i] + "</sub> " +
                        (model.bi[i] >= 0 ? "+" : "") + model.bi[i].toFixed(2) +
                        "  +  p&middot;q (" + terms.join(" + ") + ")</span><br>" +
                        "The two bias terms carry “this person rates generously” and “this " +
                        "title is well liked”, which between them explain most of the " +
                        "variance in any real ratings set. Only what is left over is handed " +
                        "to the " + p.factors + " latent factors, and that is the part that " +
                        "encodes taste."));
                    ctx.stage.appendChild(A.section("Latent factors, per item"));
                    ctx.stage.appendChild(A.layerTable(
                        ["title", "genre", "bias"].concat(
                            (function () {
                                var a = [];
                                for (var dd = 0; dd < Math.min(3, p.factors); dd++)
                                    a.push("factor " + (dd + 1));
                                return a;
                            })()),
                        T.ITEMS.map(function (name, ii) {
                            var cells = [name, T.GENRES[T.GENRE[ii]],
                                         (model.bi[ii] >= 0 ? "+" : "") +
                                         model.bi[ii].toFixed(2)];
                            for (var dd = 0; dd < Math.min(3, p.factors); dd++)
                                cells.push(model.Q[ii][dd].toFixed(2));
                            return { cells: cells, stage: ii === i };
                        }), null, -1));
                    ctx.stage.appendChild(A.note(
                        "Nobody told the model what a genre is. Sort the factor columns and " +
                        "the three groups separate anyway, because a factor is whatever " +
                        "direction best explains who rated what &mdash; and on this matrix " +
                        "that is genre. On a real catalogue the factors correspond to " +
                        "nothing nameable, which is the trade: accuracy for the ability to " +
                        "say why."));
                }

                /* every method, on the same held-out ratings */
                function score(m, extra) {
                    var save = p.method;
                    p.method = m;
                    var v = T.rmse(function (uu, ii) {
                        if (m === "global") return T.GLOBAL;
                        if (m === "usermean") return T.UMEAN[uu];
                        if (m === "mf") return model.predict(uu, ii);
                        var nb2 = m === "itemknn" ? neighboursI(uu, ii, p.k, p.sim)
                                                  : neighboursU(uu, ii, p.k, p.sim);
                        var base2 = m === "itemknn" ? T.IMEAN[ii] : T.UMEAN[uu];
                        var n2 = 0, d2 = 0;
                        nb2.forEach(function (q) {
                            var c2 = m === "itemknn" ? T.IMEAN[q.id] : T.UMEAN[q.id];
                            n2 += q.sim * (q.rating - c2); d2 += Math.abs(q.sim);
                        });
                        return d2 > 0 ? base2 + n2 / d2 : base2;
                    });
                    p.method = save;
                    return v;
                }
                ctx.stage.appendChild(A.section("Every method, same held-out ratings"));
                ctx.stage.appendChild(A.bars([
                    { label: "global average", value: score("global") },
                    { label: "the user's own average", value: score("usermean") },
                    { label: "user-based kNN, k = " + p.k, value: score("userknn"),
                      hot: p.method === "userknn" },
                    { label: "item-based kNN, k = " + p.k, value: score("itemknn"),
                      hot: p.method === "itemknn" },
                    { label: "matrix factorisation, " + p.factors + " factors",
                      value: score("mf"), hot: p.method === "mf" }
                ], { format: function (v) { return "RMSE " + v.toFixed(3); } }));
                ctx.stage.appendChild(A.caption(
                    "Lower is better, and the bars are drawn to scale so a longer bar is a " +
                    "worse method. Only " + T.TEST.length + " held-out ratings, so treat " +
                    "small differences as noise - but the gap to the average baseline is not " +
                    "small."));

                ctx.setReadout(p.method + ": " + T.USERS[u] + " / " + T.ITEMS[i] +
                    " predicted " + pred.toFixed(2) +
                    (truth === null ? "" : ", actual " + truth) +
                    "  -  test RMSE " + T.rmse(predict).toFixed(3));
            };
        }
    };
})();

/* ===========================================================================
 * Deep learning for recommender systems
 *
 * The interesting thing about a neural recommender is not the network. It is
 * that almost none of the parameters are in the network: they are in the two
 * embedding tables, which grow with the catalogue and not with the depth. A
 * three-layer MLP here has a few thousand weights; the tables at production
 * scale have hundreds of millions, and every engineering decision in the area
 * - hashing, sharding, negative sampling, two towers that can be indexed
 * separately - follows from that one fact.
 *
 * All three models below are trained here on the same ratings and scored on
 * the same held-out cells as the collaborative-filtering module, so the
 * comparison between "classical" and "deep" is a real one.
 * ======================================================================== */
(function () {
    "use strict";
    var A = window.VizArch, T = window.VizArchRatings, K = window.VizArchCorpus;
    var h = A.h, svg = A.svg, rect = A.rect, text = A.text, arrow = A.arrow;

    function zeros(n) { return new Float64Array(n); }

    function randMat(rows, cols, r, scale) {
        var m = [];
        for (var i = 0; i < rows; i++) {
            var row = new Float64Array(cols);
            for (var j = 0; j < cols; j++) row[j] = A.gauss(r) * scale;
            m.push(row);
        }
        return m;
    }

    var CACHE = {};

    function fit(kind, f, H, epochs) {
        var key = [kind, f, H, epochs].join("|");
        if (CACHE[key]) return CACHE[key];
        var r = A.rng(23), u, i, d, k;
        var P = randMat(T.NU, f, r, 0.25), Q = randMat(T.NI, f, r, 0.25);
        var Pm = randMat(T.NU, f, r, 0.25), Qm = randMat(T.NI, f, r, 0.25);
        var din = 2 * f, H2 = Math.max(2, Math.round(H / 2));
        var W1 = randMat(H, din, r, 1 / Math.sqrt(din)), b1 = zeros(H);
        var W2 = randMat(H2, H, r, 1 / Math.sqrt(H)), b2 = zeros(H2);
        var headIn = (kind === "neumf") ? H2 + f : (kind === "mlp" ? H2 : f);
        var W3 = randMat(1, headIn, r, 1 / Math.sqrt(headIn)), b3 = zeros(1);
        var bu = zeros(T.NU), bi = zeros(T.NI);

        var ent = [];
        for (u = 0; u < T.NU; u++) for (i = 0; i < T.NI; i++)
            if (T.TRAIN[u][i]) ent.push([u, i]);

        var lr = kind === "mf" ? 0.02 : 0.01;
        /* Two decay rates, because the two kinds of parameter are touched at
         * wildly different rates. An embedding row is updated once per rating
         * that mentions it - a few hundred times over the run - so a decay of
         * 0.05 per update is the mild L2 that matrix factorisation wants. A
         * dense weight is updated on EVERY example, tens of thousands of
         * times, and the same coefficient multiplies it by e^-20: the network
         * is driven to exactly zero and the model silently degrades to
         * biases-only, which shows up as a test RMSE that does not move when
         * you change the epoch count. */
        var reg = 0.05, regNet = 0.0004;

        function forward(u, i) {
            var gmf = null, x = null, h1 = null, h2 = null, out;
            if (kind === "mf") {
                out = T.GLOBAL + bu[u] + bi[i];
                for (d = 0; d < f; d++) out += P[u][d] * Q[i][d];
                return { out: out };
            }
            if (kind === "neumf") {
                gmf = new Float64Array(f);
                for (d = 0; d < f; d++) gmf[d] = P[u][d] * Q[i][d];
            }
            x = new Float64Array(2 * f);
            for (d = 0; d < f; d++) { x[d] = Pm[u][d]; x[f + d] = Qm[i][d]; }
            h1 = new Float64Array(H);
            for (k = 0; k < H; k++) {
                var s = b1[k];
                for (d = 0; d < 2 * f; d++) s += W1[k][d] * x[d];
                h1[k] = s > 0 ? s : 0.01 * s;
            }
            h2 = new Float64Array(H2);
            for (k = 0; k < H2; k++) {
                var s2 = b2[k];
                for (d = 0; d < H; d++) s2 += W2[k][d] * h1[d];
                h2[k] = s2 > 0 ? s2 : 0.01 * s2;
            }
            var head = kind === "neumf" ? new Float64Array(H2 + f) : h2;
            if (kind === "neumf") {
                for (d = 0; d < H2; d++) head[d] = h2[d];
                for (d = 0; d < f; d++) head[H2 + d] = gmf[d];
            }
            out = b3[0] + T.GLOBAL + bu[u] + bi[i];
            for (d = 0; d < head.length; d++) out += W3[0][d] * head[d];
            return { out: out, x: x, h1: h1, h2: h2, head: head, gmf: gmf };
        }

        for (var ep = 0; ep < epochs; ep++) {
            for (var n = 0; n < ent.length; n++) {
                u = ent[n][0]; i = ent[n][1];
                var st = forward(u, i);
                var e = st.out - T.R[u][i];       /* dL/dout for squared error */
                bu[u] -= lr * (e + reg * bu[u]);
                bi[i] -= lr * (e + reg * bi[i]);
                if (kind === "mf") {
                    for (d = 0; d < f; d++) {
                        var pu = P[u][d];
                        P[u][d] -= lr * (e * Q[i][d] + reg * pu);
                        Q[i][d] -= lr * (e * pu + reg * Q[i][d]);
                    }
                    continue;
                }
                var dHead = new Float64Array(st.head.length);
                for (d = 0; d < st.head.length; d++) {
                    dHead[d] = e * W3[0][d];
                    W3[0][d] -= lr * (e * st.head[d] + regNet * W3[0][d]);
                }
                b3[0] -= lr * e;
                if (kind === "neumf") {
                    for (d = 0; d < f; d++) {
                        var g = dHead[H2 + d];
                        var pu2 = P[u][d];
                        P[u][d] -= lr * (g * Q[i][d] + reg * pu2);
                        Q[i][d] -= lr * (g * pu2 + reg * Q[i][d]);
                    }
                }
                var dh2 = new Float64Array(H2);
                for (d = 0; d < H2; d++)
                    dh2[d] = dHead[d] * (st.h2[d] > 0 ? 1 : 0.01);
                var dh1 = new Float64Array(H);
                for (k = 0; k < H2; k++) {
                    for (d = 0; d < H; d++) {
                        dh1[d] += dh2[k] * W2[k][d];
                        W2[k][d] -= lr * (dh2[k] * st.h1[d] + regNet * W2[k][d]);
                    }
                    b2[k] -= lr * dh2[k];
                }
                for (d = 0; d < H; d++) dh1[d] *= (st.h1[d] > 0 ? 1 : 0.01);
                var dx = new Float64Array(2 * f);
                for (k = 0; k < H; k++) {
                    for (d = 0; d < 2 * f; d++) {
                        dx[d] += dh1[k] * W1[k][d];
                        W1[k][d] -= lr * (dh1[k] * st.x[d] + regNet * W1[k][d]);
                    }
                    b1[k] -= lr * dh1[k];
                }
                for (d = 0; d < f; d++) {
                    Pm[u][d] -= lr * (dx[d] + reg * Pm[u][d]);
                    Qm[i][d] -= lr * (dx[f + d] + reg * Qm[i][d]);
                }
            }
        }
        var res = {
            predict: function (u, i) { return forward(u, i).out; },
            P: P, Q: Q, Pm: Pm, Qm: Qm,
            /* the parameter budget, split the way it actually splits */
            embParams: (kind === "mf" ? (T.NU + T.NI) * f
                        : (kind === "mlp" ? (T.NU + T.NI) * f
                           : (T.NU + T.NI) * f * 2)) + T.NU + T.NI,
            netParams: kind === "mf" ? 0
                : H * (2 * f) + H + H2 * H + H2 +
                  ((kind === "neumf" ? H2 + f : H2) + 1)
        };
        CACHE[key] = res;
        return res;
    }

    function towers(kind, f, H) {
        var W = 560, Hh = 250;
        var s = svg(W, Hh, "arch-svg-wide");
        var lx = 140, rx = W - 140;
        s.appendChild(rect(lx - 78, 10, 156, 26, { fill: A.SURFACE, stroke: A.BORDER }));
        s.appendChild(text(lx, 27, "user id  ->  one row", { size: 9, fill: A.MAIN }));
        s.appendChild(rect(rx - 78, 10, 156, 26, { fill: A.SURFACE, stroke: A.BORDER }));
        s.appendChild(text(rx, 27, "item id  ->  one row", { size: 9, fill: A.MAIN }));

        s.appendChild(arrow(lx, 36, lx, 54, { stroke: A.BORDER, sw: 1 }));
        s.appendChild(arrow(rx, 36, rx, 54, { stroke: A.BORDER, sw: 1 }));
        s.appendChild(rect(lx - 78, 56, 156, 28, { fill: A.FILL, fo: 0.15, stroke: A.ACCENT }));
        s.appendChild(text(lx, 74, "user embedding  " + T.NU + " x " + f,
            { size: 9, fill: A.ACCENT }));
        s.appendChild(rect(rx - 78, 56, 156, 28, { fill: A.FILL, fo: 0.15, stroke: A.ACCENT }));
        s.appendChild(text(rx, 74, "item embedding  " + T.NI + " x " + f,
            { size: 9, fill: A.ACCENT }));

        var mid = W / 2;
        s.appendChild(arrow(lx, 84, mid - 40, 110, { stroke: A.BORDER, sw: 1 }));
        s.appendChild(arrow(rx, 84, mid + 40, 110, { stroke: A.BORDER, sw: 1 }));

        var label = kind === "mf" ? "dot product  ->  one number"
                  : (kind === "mlp" ? "concatenate  ->  " + (2 * f) + " numbers"
                                    : "dot product AND concatenate");
        s.appendChild(rect(mid - 110, 112, 220, 26, { fill: A.SURFACE, stroke: A.BORDER }));
        s.appendChild(text(mid, 129, label, { size: 9, fill: A.MAIN }));

        var y = 138;
        if (kind !== "mf") {
            [["dense " + (2 * f) + " -> " + H + ", ReLU", H],
             ["dense " + H + " -> " + Math.max(2, Math.round(H / 2)) + ", ReLU",
              Math.max(2, Math.round(H / 2))]].forEach(function (l) {
                s.appendChild(arrow(mid, y, mid, y + 14, { stroke: A.BORDER, sw: 1 }));
                s.appendChild(rect(mid - 110, y + 16, 220, 24,
                    { fill: A.SURFACE, stroke: A.BORDER }));
                s.appendChild(text(mid, y + 32, l[0], { size: 9, fill: A.MAIN }));
                y += 42;
            });
        }
        s.appendChild(arrow(mid, y, mid, y + 14, { stroke: A.BORDER, sw: 1 }));
        s.appendChild(rect(mid - 110, y + 16, 220, 26,
            { fill: A.FILL, fo: 0.16, stroke: A.ACCENT }));
        s.appendChild(text(mid, y + 34, "predicted rating  +  user bias  +  item bias",
            { size: 8.5, fill: A.ACCENT }));
        return s;
    }

    A.WIDGETS.recsys = {
        controls: [
            { key: "model", label: "Model", type: "select", value: "mlp", id: "rs-model",
              options: [{ value: "mf", label: "matrix factorisation - a dot product" },
                        { value: "mlp", label: "MLP over the concatenated embeddings" },
                        { value: "neumf", label: "NeuMF - both paths, fused" }] },
            { key: "user", label: "Recommend for", type: "select", value: "0",
              id: "rs-user",
              options: T.USERS.map(function (n, i) {
                  return { value: String(i), label: n }; }) },
            { key: "f", label: "Embedding dimensions", type: "range",
              min: 2, max: 12, step: 1, value: 4, id: "rs-f" },
            { key: "H", label: "Hidden width", type: "range",
              min: 4, max: 32, step: 4, value: 16, id: "rs-H" },
            { key: "epochs", label: "Training epochs", type: "range",
              min: 0, max: 600, step: 25, value: 300, id: "rs-epochs" },
            { key: "catalogue", label: "Catalogue size, for the budget", type: "select",
              value: "1", id: "rs-cat",
              options: [{ value: "0", label: "this page - 10 users, 12 items" },
                        { value: "1", label: "a small service - 100 K users, 10 K items" },
                        { value: "2", label: "a large one - 50 M users, 5 M items" }] }
        ],
        build: function (ctx) {
            return function draw() {
                var p = ctx.params;
                var m = fit(p.model, p.f, p.H, p.epochs);
                var u = parseInt(p.user, 10);

                ctx.stage.innerHTML = "";
                var wrap = h("div", "arch-scroll");
                wrap.appendChild(towers(p.model, p.f, p.H));
                ctx.stage.appendChild(wrap);

                var mine = T.rmse(m.predict);
                var mfRef = fit("mf", p.f, p.H, p.epochs);

                ctx.stage.appendChild(A.stats([
                    { value: mine.toFixed(3), label: "test RMSE",
                      note: "on " + T.TEST.length + " held-out ratings" },
                    { value: A.commas(m.embParams), label: "parameters in the tables",
                      note: "grow with the catalogue" },
                    { value: A.commas(m.netParams), label: "parameters in the network",
                      note: "fixed, whatever the catalogue" },
                    { value: m.netParams
                             ? (100 * m.embParams / (m.embParams + m.netParams)).toFixed(0) + "%"
                             : "100%",
                      label: "of the model is lookup tables", note: "at this size" }
                ]));

                /* recommendations */
                var recs = [];
                for (var i = 0; i < T.NI; i++) {
                    if (T.TRAIN[u][i]) continue;
                    recs.push({ i: i, score: T.clip(m.predict(u, i)) });
                }
                recs.sort(function (a, b) { return b.score - a.score; });
                ctx.stage.appendChild(A.section(
                    "What it would put in front of " + T.USERS[u]));
                ctx.stage.appendChild(A.layerTable(
                    ["rank", "title", "genre", "predicted", "actually rated"],
                    recs.slice(0, 6).map(function (rc, ix) {
                        return { cells: [String(ix + 1), T.ITEMS[rc.i],
                                         T.GENRES[T.GENRE[rc.i]], rc.score.toFixed(2),
                                         T.OBS[u][rc.i] ? String(T.R[u][rc.i]) + "  (held out)"
                                                        : "never rated"],
                                 stage: ix === 0 };
                    }), null, -1));

                var liked = [];
                for (i = 0; i < T.NI; i++)
                    if (T.TRAIN[u][i] && T.R[u][i] >= 4) liked.push(T.GENRES[T.GENRE[i]]);
                ctx.stage.appendChild(A.caption(
                    liked.length
                        ? T.USERS[u] + " rated " + liked.join(", ") +
                          " highly in the training data. The model was never told what a " +
                          "genre is."
                        : T.USERS[u] + " has no strong ratings in the training data, so the " +
                          "model has very little to go on - the cold-start case."));

                /* the item space */
                if (p.epochs > 0) {
                    var emb = (p.model === "mf" ? m.Q : m.Qm).map(function (v) {
                        return Array.prototype.slice.call(v);
                    });
                    var proj = p.f >= 2 ? K.pca2(emb) : emb.map(function (v) {
                        return [v[0], 0];
                    });
                    ctx.stage.appendChild(A.section("The item embeddings it learned"));
                    var w2 = h("div", "arch-scroll");
                    w2.appendChild(K.scatter(proj, T.ITEMS.map(function (n, ii) {
                        return n + "  (" + T.GENRES[T.GENRE[ii]].slice(0, 3) + ")";
                    }), null, 560, 280));
                    ctx.stage.appendChild(w2);
                    ctx.stage.appendChild(A.caption(
                        "Titles of the same genre end up near each other because the same " +
                        "people rated them the same way, not because anything in the input " +
                        "said so."));
                }

                ctx.stage.appendChild(A.section("Against the classical baseline"));
                ctx.stage.appendChild(A.bars([
                    { label: "global average", value: T.rmse(function () { return T.GLOBAL; }) },
                    { label: "matrix factorisation, " + p.f + " factors",
                      value: T.rmse(mfRef.predict), hot: p.model === "mf" },
                    { label: (p.model === "mf" ? "MLP" : "this model") + ", " + p.f +
                             "d embeddings, " + p.H + " hidden",
                      value: p.model === "mf"
                             ? T.rmse(fit("mlp", p.f, p.H, p.epochs).predict) : mine,
                      hot: p.model !== "mf" }
                ], { format: function (v) { return "RMSE " + v.toFixed(3); } }));
                ctx.stage.appendChild(A.note(
                    "On 80-odd ratings a dot product is hard to beat, and that is not a " +
                    "quirk of this page: the neural collaborative filtering results were " +
                    "re-examined in 2019 and a properly tuned matrix factorisation matched " +
                    "or beat the MLP on the standard benchmarks. What deep models actually " +
                    "buy is <em>side information</em> &mdash; text, images, context, " +
                    "sequence &mdash; which a dot product between two id embeddings has no " +
                    "way to accept."));

                /* the budget at scale, which is the real architectural point */
                var scales = [[T.NU, T.NI], [100000, 10000], [50000000, 5000000]];
                var sc = scales[parseInt(p.catalogue, 10)] || scales[1];
                var tables = (sc[0] + sc[1]) * p.f * (p.model === "neumf" ? 2 : 1);
                ctx.stage.appendChild(A.section("The same architecture at catalogue scale"));
                ctx.stage.appendChild(A.layerTable(
                    ["part", "size", "parameters", "grows with"],
                    [{ cells: ["user embedding table",
                               A.commas(sc[0]) + " x " + p.f,
                               A.fmt(sc[0] * p.f), "users"] },
                     { cells: ["item embedding table",
                               A.commas(sc[1]) + " x " + p.f,
                               A.fmt(sc[1] * p.f), "catalogue"] },
                     { cells: ["the network itself",
                               p.model === "mf" ? "-" : (2 * p.f) + " -> " + p.H + " -> " +
                                   Math.max(2, Math.round(p.H / 2)) + " -> 1",
                               A.commas(m.netParams), "nothing"], stage: true },
                     { cells: ["total", "-", A.fmt(tables + m.netParams),
                               A.fmt(4 * (tables + m.netParams)) + "B in fp32"] }],
                    null, -1));
                ctx.stage.appendChild(A.note(
                    "At the selected scale the tables are <strong>" +
                    (m.netParams ? A.fmt(tables / m.netParams) : "-") +
                    " times</strong> the size of the network. That ratio is why production " +
                    "recommenders look the way they do: the tables are sharded across " +
                    "machines while the network is replicated, ids are hashed into a fixed " +
                    "number of buckets to cap the table, and the two towers are kept " +
                    "<em>separate</em> until the final interaction so item vectors can be " +
                    "computed once, indexed, and retrieved by approximate nearest neighbour " +
                    "instead of scoring five million items per request."));

                ctx.setReadout(p.model + ", " + p.f + "d embeddings, " + p.H +
                    " hidden, " + p.epochs + " epochs: test RMSE " + mine.toFixed(3) +
                    ", " + A.commas(m.embParams + m.netParams) + " parameters");
            };
        }
    };
})();

/* The boot block. Every widget above has registered by the time this runs,
 * which is why the core does not start the mount itself. */
(function () {
    "use strict";
    function go() { window.VizArch.init(); }
    if (document.readyState === "loading")
        document.addEventListener("DOMContentLoaded", go);
    else go();
})();
