/* The async-programming explorers.
 *
 * Five widgets, one per module in the async_python track. Every number on
 * screen is computed here from the controls rather than drawn from a stored
 * picture, which is the same guarantee the rest of the site's visualisations
 * give: what you are looking at is the arithmetic.
 *
 * The event-loop widget is the odd one out - it is a stepper over a simulated
 * scheduler rather than a timeline - and it deliberately reproduces the
 * interleaving the article's first editor prints, so the drawing and the real
 * interpreter agree.
 *
 * Mount: <div data-vz-async><script type="application/json" class="as-config">
 */
(function () {
    "use strict";

    var NS = "http://www.w3.org/2000/svg";
    var ACCENT = "var(--accent-primary)";
    var MUTED = "var(--text-muted)";
    var MAIN = "var(--text-main)";
    var SUBTLE = "var(--border-subtle)";

    function h(tag, cls, text) {
        var n = document.createElement(tag);
        if (cls) n.className = cls;
        if (text != null) n.textContent = text;
        return n;
    }

    function e(tag, attrs) {
        var n = document.createElementNS(NS, tag), k;
        for (k in attrs) if (attrs[k] != null) n.setAttribute(k, attrs[k]);
        return n;
    }

    function svgRoot(w, hgt) {
        var s = e("svg", {viewBox: "0 0 " + w + " " + hgt, class: "vz-as-svg"});
        s.setAttribute("preserveAspectRatio", "xMidYMid meet");
        return s;
    }

    function rect(x, y, w, hgt, o) {
        o = o || {};
        return e("rect", {x: x, y: y, width: Math.max(0, w), height: Math.max(0, hgt),
                          rx: o.rx == null ? 3 : o.rx, fill: o.fill || "none",
                          stroke: o.stroke, "stroke-width": o.sw,
                          "fill-opacity": o.fo, "stroke-dasharray": o.dash});
    }

    function line(x1, y1, x2, y2, o) {
        o = o || {};
        return e("line", {x1: x1, y1: y1, x2: x2, y2: y2,
                          stroke: o.stroke || SUBTLE, "stroke-width": o.sw || 1,
                          "stroke-dasharray": o.dash});
    }

    function text(x, y, str, o) {
        o = o || {};
        var t = e("text", {x: x, y: y, fill: o.fill || MUTED,
                           "font-size": o.size || 9,
                           "text-anchor": o.anchor || "start",
                           "font-family": o.mono === false ? null : "var(--vz-mono)",
                           "font-weight": o.weight});
        t.textContent = str;
        return t;
    }

    function fmt(n, d) {
        var f = Math.pow(10, d == null ? 2 : d);
        return String(Math.round(n * f) / f);
    }

    // ----------------------------------------------------------- controls

    function control(spec, onChange) {
        var wrap = h("label", "vz-as-control");
        var head = h("div", "vz-as-chead");
        var name = h("span", "vz-as-clabel", spec.label);
        var val = h("span", "vz-as-cvalue", "");
        head.appendChild(name);
        head.appendChild(val);
        wrap.appendChild(head);

        var input;
        if (spec.type === "toggle") {
            input = h("input");
            input.type = "checkbox";
            input.checked = !!spec.value;
        } else {
            input = h("input");
            input.type = "range";
            input.min = spec.min; input.max = spec.max;
            input.step = spec.step || 1; input.value = spec.value;
        }
        input.className = "vz-as-input";
        wrap.appendChild(input);

        function read() {
            if (spec.type === "toggle") {
                val.textContent = input.checked ? "on" : "off";
                return input.checked;
            }
            var v = parseFloat(input.value);
            val.textContent = spec.fmt ? spec.fmt(v) : String(v);
            return v;
        }
        input.addEventListener("input", function () { onChange(spec.key, read()); });
        input.addEventListener("change", function () { onChange(spec.key, read()); });
        read();
        return {el: wrap, read: read};
    }

    // ------------------------------------------------------ shared pieces

    function stats(items) {
        var wrap = h("div", "vz-as-stats");
        items.forEach(function (it) {
            var box = h("div", "vz-as-stat");
            box.appendChild(h("span", "vz-as-stat-value", it.value));
            box.appendChild(h("span", "vz-as-stat-label", it.label));
            if (it.note) box.appendChild(h("span", "vz-as-stat-note", it.note));
            wrap.appendChild(box);
        });
        return wrap;
    }

    function caption(str) { return h("p", "vz-as-caption", str); }

    /* A time axis with one row per actor. spans are {t0, t1, kind, label}.
     * kind: "run" (solid accent), "wait" (hollow), "block" (hatched red),
     * "idle" (nothing drawn). Times are seconds; the axis scales to `total`. */
    function timeline(rows, total, opts) {
        opts = opts || {};
        var W = 620, padL = opts.padL || 96, padR = 14;
        var rowH = 26, top = 26;
        var H = top + rows.length * rowH + 30;
        var s = svgRoot(W, H);
        var plotW = W - padL - padR;
        var x = function (t) { return padL + (t / total) * plotW; };

        // axis
        var ticks = opts.ticks || 5, i;
        for (i = 0; i <= ticks; i++) {
            var t = (total / ticks) * i;
            s.appendChild(line(x(t), top - 8, x(t), top + rows.length * rowH,
                               {stroke: SUBTLE, dash: i ? "2 4" : null}));
            s.appendChild(text(x(t), top + rows.length * rowH + 16,
                               fmt(t, 2) + "s", {size: 8, anchor: "middle"}));
        }

        rows.forEach(function (r, ri) {
            var y = top + ri * rowH;
            s.appendChild(text(padL - 8, y + rowH / 2 + 3, r.label,
                               {size: 9, anchor: "end",
                                fill: r.hot ? ACCENT : MUTED}));
            (r.spans || []).forEach(function (sp) {
                var w = x(sp.t1) - x(sp.t0);
                if (sp.kind === "wait") {
                    s.appendChild(rect(x(sp.t0), y + 9, w, 6,
                                       {fill: SUBTLE, fo: 0.55, rx: 2}));
                } else if (sp.kind === "block") {
                    s.appendChild(rect(x(sp.t0), y + 4, w, 16,
                                       {fill: "#dc2626", fo: 0.8, rx: 2}));
                } else if (sp.kind === "run") {
                    s.appendChild(rect(x(sp.t0), y + 4, w, 16,
                                       {fill: ACCENT, fo: 0.9, rx: 2}));
                } else if (sp.kind === "tick") {
                    s.appendChild(line(x(sp.t0), y + 3, x(sp.t0), y + 21,
                                       {stroke: ACCENT, sw: 2}));
                }
                if (sp.label && w > 26) {
                    s.appendChild(text(x(sp.t0) + w / 2, y + 16, sp.label,
                                       {size: 8, anchor: "middle", fill: MAIN}));
                }
            });
        });
        return s;
    }

    // --------------------------------------------------------- the mount

    var WIDGETS = {};

    function mount(root) {
        var cfgEl = root.querySelector(".as-config");
        if (!cfgEl) return;
        var cfg;
        try { cfg = JSON.parse(cfgEl.textContent); } catch (err) { return; }
        var spec = WIDGETS[cfg.widget];
        if (!spec) return;

        root.innerHTML = "";
        var head = h("div", "vz-as-head");
        var panel = h("div", "vz-as-controls");
        var readout = h("p", "vz-as-readout");
        readout.setAttribute("aria-live", "polite");
        var stage = h("div", "vz-as-stage");

        var params = {};
        var queued = false;
        function schedule() {
            if (queued) return;
            queued = true;
            requestAnimationFrame(function () { queued = false; draw(); });
        }
        var ctx = {
            stage: stage, params: params, redraw: schedule,
            setReadout: function (t) { readout.textContent = t; }
        };

        (spec.controls || []).forEach(function (cs) {
            var c = control(cs, function (k, v) { params[k] = v; schedule(); });
            params[cs.key] = c.read();
            panel.appendChild(c.el);
        });

        var draw = spec.build(ctx);

        // Controls above the drawing: the same decision as the architecture
        // explorers, for the same reason - you cannot read a change you
        // cannot see while you are making it.
        if (panel.childNodes.length) head.appendChild(panel);
        head.appendChild(readout);
        root.appendChild(head);
        root.appendChild(stage);
        draw();
        root.dataset.vzAsyncReady = "1";
    }

    function init() {
        Array.prototype.forEach.call(
            document.querySelectorAll("[data-vz-async]"), mount);
    }

    var A = {
        WIDGETS: WIDGETS, h: h, e: e, rect: rect, line: line, text: text,
        svgRoot: svgRoot, fmt: fmt, stats: stats, caption: caption,
        timeline: timeline, ACCENT: ACCENT, MUTED: MUTED, MAIN: MAIN,
        SUBTLE: SUBTLE
    };
    window.VizAsync = A;
    A.init = init;

    // ------------------------------------------------- 1. the event loop
    /* A stepper over a simulated scheduler. Replayed from turn 0 every draw,
     * so the slider is a position rather than accumulated state, and the
     * emitted order matches what the article's first editor actually prints. */
    A.WIDGETS.loop = {
        controls: [
            {key: "n", label: "Coroutines", type: "range", min: 2, max: 4, value: 2},
            {key: "steps", label: "Steps each", type: "range", min: 1, max: 4, value: 3},
            {key: "turn", label: "Loop turn", type: "range", min: 0, max: 16, value: 0}
        ],
        build: function (ctx) {
            var NAMES = ["A", "B", "C", "D"];
            return function () {
                var p = ctx.params, n = p.n, steps = p.steps;
                var totalTurns = n * steps;
                var turn = Math.min(p.turn, totalTurns);

                var ready = [], left = [], i;
                for (i = 0; i < n; i++) { ready.push(i); left.push(steps); }
                var log = [], running = null, waiting = [];
                for (i = 0; i < turn; i++) {
                    running = ready.shift();
                    if (running == null) break;
                    log.push(NAMES[running] + " step " + (steps - left[running]));
                    left[running] -= 1;
                    if (left[running] > 0) ready.push(running);
                }
                waiting = [];
                for (i = 0; i < n; i++) {
                    if (left[i] === 0 && ready.indexOf(i) < 0) waiting.push(i);
                }

                ctx.stage.innerHTML = "";
                var W = 620, s = A.svgRoot(W, 150);

                s.appendChild(A.text(14, 18, "RUNNING", {size: 8, weight: 700}));
                var rx = 14, rw = 120;
                s.appendChild(A.rect(rx, 24, rw, 26,
                    {fill: turn ? A.ACCENT : "none", fo: 0.85,
                     stroke: A.SUBTLE, sw: 1.2, dash: turn ? null : "3 3"}));
                s.appendChild(A.text(rx + rw / 2, 41,
                    turn && running != null ? NAMES[running] : "—",
                    {size: 12, anchor: "middle", fill: A.MAIN, weight: 700}));
                s.appendChild(A.text(rx, 62,
                    turn ? "between two awaits" : "loop not started",
                    {size: 8}));

                s.appendChild(A.text(200, 18, "READY QUEUE (front on the left)",
                                     {size: 8, weight: 700}));
                if (!ready.length) {
                    s.appendChild(A.text(200, 41, "empty", {size: 9}));
                }
                ready.forEach(function (idx, k) {
                    var bx = 200 + k * 52;
                    s.appendChild(A.rect(bx, 24, 44, 26,
                        {fill: A.ACCENT, fo: 0.28, stroke: A.SUBTLE, sw: 1}));
                    s.appendChild(A.text(bx + 22, 41, NAMES[idx],
                        {size: 11, anchor: "middle", fill: A.MAIN}));
                    s.appendChild(A.text(bx + 22, 60, left[idx] + " left",
                        {size: 7, anchor: "middle"}));
                });

                s.appendChild(A.text(14, 88, "DONE (nothing left to await)",
                                     {size: 8, weight: 700}));
                if (!waiting.length) s.appendChild(A.text(14, 106, "none", {size: 9}));
                waiting.forEach(function (idx, k) {
                    var bx = 14 + k * 52;
                    s.appendChild(A.rect(bx, 94, 44, 22,
                        {fill: "none", stroke: A.SUBTLE, sw: 1, dash: "3 3"}));
                    s.appendChild(A.text(bx + 22, 109, NAMES[idx],
                        {size: 10, anchor: "middle"}));
                });

                s.appendChild(A.text(300, 88, "PRINTED SO FAR", {size: 8, weight: 700}));
                var shown = log.slice(-4);
                shown.forEach(function (lineStr, k) {
                    s.appendChild(A.text(300, 102 + k * 12, lineStr,
                        {size: 9, fill: k === shown.length - 1 ? A.ACCENT : A.MUTED}));
                });

                ctx.stage.appendChild(s);
                ctx.stage.appendChild(A.stats([
                    {value: turn + " / " + totalTurns, label: "loop turns",
                     note: "one turn = one step, then an await"},
                    {value: String(ready.length), label: "ready",
                     note: "queued for a turn"},
                    {value: String(log.length), label: "lines printed",
                     note: "in emission order"},
                    {value: n + " × " + steps, label: "total steps",
                     note: "one thread, taken in turns"}
                ]));
                ctx.stage.appendChild(A.caption(
                    "Each turn takes the coroutine at the front of the ready "
                    + "queue, runs it to its next await, and pushes it to the "
                    + "back. That round-robin is why the printed order "
                    + "interleaves rather than finishing one coroutine first."));
                ctx.setReadout(turn === 0
                    ? "turn 0: nothing has run; both coroutines are queued"
                    : "turn " + turn + ": ran " + log[log.length - 1]
                      + ", ready queue now [" + ready.map(function (i2) {
                          return NAMES[i2]; }).join(", ") + "]");
            };
        }
    };

    // -------------------------------------------- 2. sequential vs tasks
    A.WIDGETS.overlap = {
        controls: [
            {key: "n", label: "Waits", type: "range", min: 2, max: 8, value: 3},
            {key: "d", label: "Each wait", type: "range", min: 0.05, max: 0.4,
             step: 0.05, value: 0.2, fmt: function (v) { return fmt(v, 2) + "s"; }}
        ],
        build: function (ctx) {
            return function () {
                var p = ctx.params, n = p.n, d = p.d;
                var seq = n * d, con = d;
                var rows = [], i;
                var seqSpans = [], conSpans = [];
                for (i = 0; i < n; i++) {
                    seqSpans.push({t0: i * d, t1: (i + 1) * d, kind: "run",
                                   label: "w" + (i + 1)});
                    conSpans.push({t0: 0, t1: d, kind: "run"});
                }
                rows.push({label: "await, await, …", spans: seqSpans});
                for (i = 0; i < n; i++) {
                    rows.push({label: "task " + (i + 1), spans: [conSpans[i]],
                               hot: true});
                }
                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(A.timeline(rows, seq, {ticks: 4}));
                ctx.stage.appendChild(A.stats([
                    {value: fmt(seq, 2) + "s", label: "awaited in turn",
                     note: n + " × " + fmt(d, 2) + "s"},
                    {value: fmt(con, 2) + "s", label: "as tasks",
                     note: "the longest single wait"},
                    {value: fmt(seq / con, 1) + "×", label: "faster",
                     note: "equals the number of waits"},
                    {value: "0", label: "extra threads",
                     note: "still one thread"}
                ]));
                ctx.stage.appendChild(A.caption(
                    "Nothing runs faster. The top row is one wait after "
                    + "another; the rows below are the same waits overlapping, "
                    + "which is all a task buys you — and why the speed-up "
                    + "is exactly the number of waits and never more."));
                ctx.setReadout(n + " waits of " + fmt(d, 2) + "s: "
                    + fmt(seq, 2) + "s awaited in turn, " + fmt(con, 2)
                    + "s as tasks");
            };
        }
    };

    // ------------------------------------------------ 3. bounded fan-out
    A.WIDGETS.limit = {
        controls: [
            {key: "jobs", label: "Jobs", type: "range", min: 3, max: 15, value: 9},
            {key: "cap", label: "Concurrency limit", type: "range", min: 1, max: 8,
             value: 3},
            {key: "d", label: "Each job", type: "range", min: 0.05, max: 0.3,
             step: 0.05, value: 0.05,
             fmt: function (v) { return fmt(v, 2) + "s"; }}
        ],
        build: function (ctx) {
            return function () {
                var p = ctx.params, jobs = p.jobs, cap = Math.min(p.cap, p.jobs),
                    d = p.d;
                var rounds = Math.ceil(jobs / cap);
                var makespan = rounds * d;
                var rows = [], i;
                for (i = 0; i < jobs; i++) {
                    var r = Math.floor(i / cap);
                    rows.push({label: "job " + (i + 1),
                               spans: [{t0: r * d, t1: (r + 1) * d, kind: "run"}],
                               hot: r === 0});
                }
                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(A.timeline(rows, makespan,
                    {ticks: Math.min(rounds, 6), padL: 66}));
                ctx.stage.appendChild(A.stats([
                    {value: String(cap), label: "most in flight",
                     note: "the semaphore's count"},
                    {value: String(rounds), label: "rounds",
                     note: "ceil(jobs / limit)"},
                    {value: fmt(makespan, 2) + "s", label: "total",
                     note: "rounds × " + fmt(d, 2) + "s"},
                    {value: fmt(d, 2) + "s", label: "if unbounded",
                     note: "all " + jobs + " at once"}
                ]));
                ctx.stage.appendChild(A.caption(
                    "All " + jobs + " coroutines are scheduled at once; the "
                    + "semaphore only governs how many are past its "
                    + "async with at a time. Drag the limit to 1 and it is a "
                    + "sequential loop; drag it to " + jobs + " and the bound "
                    + "stops binding."));
                ctx.setReadout(jobs + " jobs at " + cap + " at a time: "
                    + rounds + " rounds, " + fmt(makespan, 2) + "s, against "
                    + fmt(d, 2) + "s unbounded and "
                    + fmt(jobs * d, 2) + "s sequential");
            };
        }
    };

    // ------------------------------------------------- 4. the freeze
    A.WIDGETS.freeze = {
        controls: [
            {key: "iv", label: "Heartbeat interval", type: "range", min: 0.05,
             max: 0.2, step: 0.05, value: 0.1,
             fmt: function (v) { return fmt(v, 2) + "s"; }},
            {key: "len", label: "Blocking call", type: "range", min: 0, max: 0.5,
             step: 0.05, value: 0.3,
             fmt: function (v) { return v ? fmt(v, 2) + "s" : "none"; }},
            {key: "at", label: "It starts at", type: "range", min: 0.05, max: 0.3,
             step: 0.05, value: 0.1,
             fmt: function (v) { return fmt(v, 2) + "s"; }}
        ],
        build: function (ctx) {
            return function () {
                var p = ctx.params, iv = p.iv, len = p.len, at = p.at;
                var ticks = 6, freezeEnd = at + len, i;
                var due = [], actual = [], lag = 0;
                for (i = 0; i < ticks; i++) {
                    var dueAt = i * iv;
                    // The loop cannot act between `at` and freezeEnd, so a tick
                    // due inside that window fires the moment the thread is free.
                    var act = (len > 0 && dueAt > at && dueAt < freezeEnd)
                        ? freezeEnd : dueAt;
                    due.push(dueAt); actual.push(act);
                    lag = Math.max(lag, act - dueAt);
                }
                var total = Math.max(actual[actual.length - 1], freezeEnd) + iv;
                var rows = [
                    {label: "due", spans: due.map(function (t) {
                        return {t0: t, t1: t, kind: "tick"}; })},
                    {label: "tick actually fires", hot: true,
                     spans: actual.map(function (t) {
                        return {t0: t, t1: t, kind: "tick"}; })},
                    {label: "blocking call",
                     spans: len > 0 ? [{t0: at, t1: freezeEnd, kind: "block",
                                        label: "thread held"}] : []}
                ];
                var delayed = 0;
                for (i = 0; i < ticks; i++) if (actual[i] > due[i] + 1e-9) delayed++;

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(A.timeline(rows, total, {ticks: 5}));
                ctx.stage.appendChild(A.stats([
                    {value: Math.round(lag * 1000) + " ms", label: "peak lag",
                     note: "worst late tick"},
                    {value: String(delayed), label: "ticks delayed",
                     note: "of " + ticks},
                    {value: len ? fmt(len, 2) + "s" : "none", label: "thread held",
                     note: len ? "nothing else can run" : "loop is free"},
                    {value: delayed > 1 ? "burst" : "steady", label: "recovery",
                     note: delayed > 1 ? "backlog fires at once" : "on schedule"}
                ]));
                ctx.stage.appendChild(A.caption(
                    "The top row is when each tick was due, the second when it "
                    + "actually fired. Every tick due inside the red block "
                    + "lands at the same instant — the moment the blocking "
                    + "call returns — which is the burst the article's "
                    + "first editor prints. Set the blocking call to none and "
                    + "the two rows line up."));
                ctx.setReadout(len === 0
                    ? "no blocking call: every tick fires when it is due"
                    : "a " + fmt(len, 2) + "s blocking call delays " + delayed
                      + " of " + ticks + " ticks; peak lag "
                      + Math.round(lag * 1000) + " ms");
            };
        }
    };

    // ------------------------------------------- 5. queue and backpressure
    A.WIDGETS.queue = {
        controls: [
            {key: "max", label: "maxsize", type: "range", min: 1, max: 8, value: 2,
             fmt: function (v) { return v >= 8 ? "8 (roomy)" : String(v); }},
            {key: "pi", label: "Producer: one item every", type: "range",
             min: 0.02, max: 0.16, step: 0.02, value: 0.02,
             fmt: function (v) { return fmt(v, 2) + "s"; }},
            {key: "ci", label: "Consumer: one item every", type: "range",
             min: 0.02, max: 0.2, step: 0.02, value: 0.1,
             fmt: function (v) { return fmt(v, 2) + "s"; }},
            {key: "items", label: "Items", type: "range", min: 4, max: 14, value: 5}
        ],
        build: function (ctx) {
            return function () {
                var p = ctx.params;
                var dt = 0.005, t = 0, depth = 0, produced = 0, consumed = 0;
                var prodNext = 0, consFree = 0, waits = 0, peak = 0;
                var series = [], guard = 0;
                while (consumed < p.items && guard++ < 20000) {
                    if (t >= consFree && depth > 0) {
                        depth -= 1; consumed += 1; consFree = t + p.ci;
                    }
                    if (produced < p.items && t >= prodNext) {
                        if (depth < p.max) {
                            depth += 1; produced += 1; prodNext = t + p.pi;
                        } else {
                            waits += 1;             // put() is suspended here
                        }
                    }
                    peak = Math.max(peak, depth);
                    series.push({t: t, d: depth});
                    t += dt;
                }
                // consumed is incremented when the consumer TAKES an item, so the
                // loop exits before the last one is finished; consFree is when it is.
                var total = Math.max(t, consFree);

                // depth step chart
                var W = 620, padL = 40, padR = 14, top = 18, plotH = 96;
                var s = A.svgRoot(W, top + plotH + 34);
                var plotW = W - padL - padR;
                var x = function (tt) { return padL + (tt / total) * plotW; };
                var yMax = Math.max(p.max, peak, 1);
                var y = function (dd) { return top + plotH - (dd / yMax) * plotH; };
                var k;
                for (k = 0; k <= yMax; k++) {
                    s.appendChild(A.line(padL, y(k), W - padR, y(k),
                        {stroke: A.SUBTLE, dash: k ? "2 4" : null}));
                    s.appendChild(A.text(padL - 6, y(k) + 3, String(k),
                        {size: 8, anchor: "end"}));
                }
                s.appendChild(A.line(padL, y(p.max), W - padR, y(p.max),
                    {stroke: "#dc2626", sw: 1.4, dash: "5 3"}));
                s.appendChild(A.text(W - padR, y(p.max) - 4, "maxsize",
                    {size: 8, anchor: "end", fill: "#dc2626"}));

                var path = "", prev = null;
                series.forEach(function (pt) {
                    if (prev === null) { path = "M" + x(pt.t) + " " + y(pt.d); }
                    else if (pt.d !== prev) {
                        path += " L" + x(pt.t) + " " + y(prev)
                             +  " L" + x(pt.t) + " " + y(pt.d);
                    }
                    prev = pt.d;
                });
                path += " L" + x(total) + " " + y(prev);
                s.appendChild(A.e("path", {d: path, fill: "none",
                    stroke: A.ACCENT, "stroke-width": 1.8}));
                s.appendChild(A.text(padL, top + plotH + 22,
                    "queue depth over time · " + fmt(total, 2) + "s total",
                    {size: 8}));

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(s);
                var throttled = waits > 0;
                ctx.stage.appendChild(A.stats([
                    {value: String(peak), label: "peak depth",
                     note: throttled ? "pinned at maxsize" : "never filled"},
                    {value: throttled ? "yes" : "no", label: "producer throttled",
                     note: throttled ? "put() suspended" : "never waited"},
                    {value: fmt(total, 2) + "s", label: "to drain " + p.items,
                     note: "consumer sets the pace"},
                    {value: String(p.items), label: "if unbounded",
                     note: "the whole backlog in memory"}
                ]));
                ctx.stage.appendChild(A.caption(
                    "The red line is maxsize. When the depth reaches it, "
                    + "await q.put(...) suspends the producer until the "
                    + "consumer takes one out — that flat stretch is "
                    + "backpressure. Make the producer slower than the "
                    + "consumer and the queue never fills, so the bound "
                    + "costs nothing."));
                ctx.setReadout(throttled
                    ? "queue pinned at " + peak + " of " + p.max
                      + ": the producer waited, so it ran at the consumer's rate"
                    : "peak depth " + peak + " of " + p.max
                      + ": the consumer kept up, so put() never suspended");
            };
        }
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
