/* The threads-and-processes explorers.
 *
 * Seven widgets, one per module in the concurrency track. Every number is
 * computed here from the controls, so what is on screen is the arithmetic
 * rather than a picture of it - the same guarantee the rest of the site gives.
 *
 * Two of them are schedulers rather than charts: the race stepper reproduces
 * the interleaving the article's simulator prints, and the deadlock stepper
 * walks two threads through two locks until they either finish or wedge.
 *
 * Mount: <div data-vz-con><script type="application/json" class="cc-config">
 */
(function () {
    "use strict";

    var NS = "http://www.w3.org/2000/svg";
    var ACCENT = "var(--accent-primary)";
    var MUTED = "var(--text-muted)";
    var MAIN = "var(--text-main)";
    var SUBTLE = "var(--border-subtle)";
    var BAD = "#dc2626";

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
        var s = e("svg", {viewBox: "0 0 " + w + " " + hgt, class: "vz-cc-svg"});
        s.setAttribute("preserveAspectRatio", "xMidYMid meet");
        return s;
    }

    function rect(x, y, w, hgt, o) {
        o = o || {};
        return e("rect", {x: x, y: y, width: Math.max(0, w),
                          height: Math.max(0, hgt), rx: o.rx == null ? 3 : o.rx,
                          fill: o.fill || "none", stroke: o.stroke,
                          "stroke-width": o.sw, "fill-opacity": o.fo,
                          "stroke-dasharray": o.dash});
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
                           "font-family": "var(--vz-mono)",
                           "font-weight": o.weight});
        t.textContent = str;
        return t;
    }

    function fmt(n, d) {
        var f = Math.pow(10, d == null ? 2 : d);
        return String(Math.round(n * f) / f);
    }

    function commas(n) {
        return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    // ----------------------------------------------------------- controls

    function control(spec, onChange) {
        var wrap = h("label", "vz-cc-control");
        var head = h("div", "vz-cc-chead");
        head.appendChild(h("span", "vz-cc-clabel", spec.label));
        var val = h("span", "vz-cc-cvalue", "");
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
        input.className = "vz-cc-input";
        wrap.appendChild(input);

        function read() {
            if (spec.type === "toggle") {
                val.textContent = spec.fmt ? spec.fmt(input.checked)
                                           : (input.checked ? "on" : "off");
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

    function stats(items) {
        var wrap = h("div", "vz-cc-stats");
        items.forEach(function (it) {
            var box = h("div", "vz-cc-stat" + (it.bad ? " is-bad" : ""));
            box.appendChild(h("span", "vz-cc-stat-value", it.value));
            box.appendChild(h("span", "vz-cc-stat-label", it.label));
            if (it.note) box.appendChild(h("span", "vz-cc-stat-note", it.note));
            wrap.appendChild(box);
        });
        return wrap;
    }

    function caption(str) { return h("p", "vz-cc-caption", str); }

    /* One row per actor, spans in seconds against a shared axis. */
    function timeline(rows, total, opts) {
        opts = opts || {};
        var W = 620, padL = opts.padL || 86, padR = 14;
        var rowH = 26, top = 24;
        var H = top + rows.length * rowH + 28;
        var s = svgRoot(W, H);
        var plotW = W - padL - padR;
        var x = function (t) { return padL + (t / (total || 1)) * plotW; };
        var ticks = opts.ticks || 5, i;
        for (i = 0; i <= ticks; i++) {
            var t = (total / ticks) * i;
            s.appendChild(line(x(t), top - 6, x(t), top + rows.length * rowH,
                               {stroke: SUBTLE, dash: i ? "2 4" : null}));
            s.appendChild(text(x(t), top + rows.length * rowH + 15,
                               opts.unit === "ms" ? Math.round(t * 1000) + "ms"
                                                  : fmt(t, 2) + "s",
                               {size: 8, anchor: "middle"}));
        }
        rows.forEach(function (r, ri) {
            var y = top + ri * rowH;
            s.appendChild(text(padL - 8, y + rowH / 2 + 3, r.label,
                               {size: 9, anchor: "end",
                                fill: r.hot ? ACCENT : MUTED}));
            (r.spans || []).forEach(function (sp) {
                var w = x(sp.t1) - x(sp.t0);
                var fill = sp.kind === "block" ? BAD
                         : sp.kind === "wait" ? SUBTLE : ACCENT;
                s.appendChild(rect(x(sp.t0), y + (sp.kind === "wait" ? 9 : 4),
                                   Math.max(w, 0.7),
                                   sp.kind === "wait" ? 6 : 16,
                                   {fill: fill, fo: sp.kind === "wait" ? 0.5 : 0.9,
                                    rx: 2}));
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
        var cfgEl = root.querySelector(".cc-config");
        if (!cfgEl) return;
        var cfg;
        try { cfg = JSON.parse(cfgEl.textContent); } catch (err) { return; }
        var spec = WIDGETS[cfg.widget];
        if (!spec) return;

        root.innerHTML = "";
        var head = h("div", "vz-cc-head");
        var panel = h("div", "vz-cc-controls");
        var readout = h("p", "vz-cc-readout");
        readout.setAttribute("aria-live", "polite");
        var stage = h("div", "vz-cc-stage");

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

        // Controls above the drawing, as on the architecture and async pages.
        if (panel.childNodes.length) head.appendChild(panel);
        head.appendChild(readout);
        root.appendChild(head);
        root.appendChild(stage);
        draw();
        root.dataset.vzConReady = "1";
    }

    function init() {
        Array.prototype.forEach.call(
            document.querySelectorAll("[data-vz-con]"), mount);
    }

    var C = {
        WIDGETS: WIDGETS, h: h, e: e, rect: rect, line: line, text: text,
        svgRoot: svgRoot, fmt: fmt, commas: commas, stats: stats,
        caption: caption, timeline: timeline,
        ACCENT: ACCENT, MUTED: MUTED, MAIN: MAIN, SUBTLE: SUBTLE, BAD: BAD
    };
    window.VizCon = C;
    C.init = init;

    // ------------------------------------------------------- 1. the GIL
    C.WIDGETS.gil = {
        controls: [
            {key: "iv", label: "Switch interval", type: "range", min: 1, max: 20,
             value: 5, fmt: function (v) { return v + " ms"; }},
            {key: "work", label: "Work per thread", type: "range", min: 10,
             max: 100, step: 10, value: 40,
             fmt: function (v) { return v + " ms"; }},
            {key: "n", label: "Threads", type: "range", min: 2, max: 4, value: 2}
        ],
        build: function (ctx) {
            var NAMES = ["A", "B", "C", "D"];
            var COST = 0.02;        // ms of overhead per switch, as a model
            return function () {
                var p = ctx.params, iv = p.iv, work = p.work, n = p.n;
                var totalWork = work * n;
                var switches = Math.max(0, Math.ceil(totalWork / iv) - 1);
                var wall = totalWork + switches * COST;
                var parallel = work;          // if they could truly overlap

                // Round-robin slices of iv ms until each thread's work is done.
                var left = [], rows = [], i;
                for (i = 0; i < n; i++) { left.push(work); rows.push([]); }
                var t = 0, cur = 0, guard = 0;
                while (left.some(function (l) { return l > 0; }) && guard++ < 4000) {
                    if (left[cur] > 0) {
                        var slice = Math.min(iv, left[cur]);
                        rows[cur].push({t0: t / 1000, t1: (t + slice) / 1000,
                                        kind: "run"});
                        left[cur] -= slice;
                        t += slice;
                    }
                    cur = (cur + 1) % n;
                }
                var rowDefs = rows.map(function (spans, k) {
                    return {label: "thread " + NAMES[k], spans: spans,
                            hot: k === 0};
                });

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(C.timeline(rowDefs, t / 1000,
                    {ticks: 5, unit: "ms", padL: 74}));
                ctx.stage.appendChild(C.stats([
                    {value: Math.round(wall) + " ms", label: "with the GIL",
                     note: "one thread runs at a time"},
                    {value: totalWork + " ms", label: "sequential",
                     note: "the same work, no threads"},
                    {value: parallel + " ms", label: "if truly parallel",
                     note: "what the GIL costs you"},
                    {value: C.commas(switches), label: "switches",
                     note: "every " + iv + " ms"}
                ]));
                ctx.stage.appendChild(C.caption(
                    "Each bar is a slice during which that thread holds the "
                    + "GIL. They tile rather than overlap, which is why the "
                    + "total matches the sequential column and not the "
                    + "parallel one. Lowering the switch interval slices the "
                    + "work more finely and changes nothing about the total, "
                    + "except the overhead of switching more often."));
                ctx.setReadout(n + " threads x " + work + " ms of bytecode: "
                    + Math.round(wall) + " ms wall, against " + totalWork
                    + " ms sequential and " + parallel
                    + " ms if the GIL let them overlap");
            };
        }
    };

    // -------------------------------------------------- 2. race conditions
    /* order = T1[0:k] + T2 + T1[k:]. k = 0 or 3 is a clean run; k = 1 or 2
     * puts the switch between T1's read and its write, and one update is
     * lost - the same result the article's simulator prints. */
    C.WIDGETS.race = {
        controls: [
            {key: "k", label: "Switch to T2 after T1 has done", type: "range",
             min: 0, max: 3, value: 1,
             fmt: function (v) {
                 return ["nothing", "its read", "its read + add",
                         "all three steps"][v];
             }}
        ],
        build: function (ctx) {
            return function () {
                var k = ctx.params.k;
                var STEP = ["read", "add", "write"];
                var t1 = [0, 1, 2].map(function (i) { return {tag: "T1", op: STEP[i]}; });
                var t2 = [0, 1, 2].map(function (i) { return {tag: "T2", op: STEP[i]}; });
                var order = t1.slice(0, k).concat(t2, t1.slice(k));

                var shared = 0, regs = {}, log = [];
                order.forEach(function (s) {
                    if (s.op === "read") {
                        regs[s.tag] = shared;
                        log.push([s.tag, "reads counter = " + shared, false]);
                    } else if (s.op === "add") {
                        regs[s.tag] += 1;
                        log.push([s.tag, "adds -> " + regs[s.tag] + " (own register)", false]);
                    } else {
                        var stale = regs[s.tag] <= shared;
                        shared = regs[s.tag];
                        log.push([s.tag, "writes counter = " + shared, stale]);
                    }
                });
                var lost = 2 - shared;

                var W = 620, s = C.svgRoot(W, 34 + log.length * 19);
                s.appendChild(C.text(14, 16, "EXECUTION ORDER",
                                     {size: 8, weight: 700}));
                s.appendChild(C.text(470, 16, "counter", {size: 8, weight: 700}));
                var running = 0;
                log.forEach(function (row, i) {
                    var y = 34 + i * 19;
                    var isT1 = row[0] === "T1";
                    s.appendChild(C.rect(14, y - 10, 34, 15,
                        {fill: isT1 ? C.ACCENT : C.MUTED, fo: 0.75, rx: 3}));
                    s.appendChild(C.text(31, y + 1, row[0],
                        {size: 8, anchor: "middle", fill: "var(--bg-surface)"}));
                    s.appendChild(C.text(56, y + 1, row[1],
                        {size: 9, fill: row[2] ? C.BAD : C.MAIN}));
                    if (/writes/.test(row[1])) {
                        running = parseInt(row[1].split("= ")[1], 10);
                    }
                    s.appendChild(C.text(500, y + 1, String(running),
                        {size: 9, fill: row[2] ? C.BAD : C.MUTED}));
                    if (row[2]) {
                        s.appendChild(C.text(520, y + 1,
                            "<- did not build on the last write",
                            {size: 8, fill: C.BAD}));
                    }
                });

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(s);
                ctx.stage.appendChild(C.stats([
                    {value: String(shared), label: "final counter",
                     note: "after two increments", bad: lost > 0},
                    {value: "2", label: "expected", note: "1 + 1"},
                    {value: String(lost), label: "updates lost",
                     note: lost ? "a write replaced a write" : "none",
                     bad: lost > 0},
                    {value: lost ? "unsafe" : "safe", label: "this ordering",
                     note: lost ? "legal, and wrong" : "legal, and right",
                     bad: lost > 0}
                ]));
                ctx.stage.appendChild(C.caption(
                    "Every step here is correct on its own. The only thing "
                    + "that changes is where the switch lands: between a read "
                    + "and its write, both threads start from the same value "
                    + "and the second write replaces the first instead of "
                    + "adding to it. Slide to either end and the count is "
                    + "right, which is why the bug is intermittent."));
                ctx.setReadout(lost
                    ? "the switch landed inside T1's read-modify-write: counter = "
                      + shared + ", one increment lost"
                    : "the switch landed between whole increments: counter = 2, "
                      + "nothing lost");
            };
        }
    };

    // --------------------------------------------------------- 3. deadlock
    C.WIDGETS.deadlock = {
        controls: [
            {key: "same", label: "Both threads take the locks in the same order",
             type: "toggle", value: false,
             fmt: function (v) { return v ? "ordered" : "opposite"; }},
            {key: "step", label: "Step", type: "range", min: 0, max: 6, value: 4}
        ],
        build: function (ctx) {
            return function () {
                var same = ctx.params.same;
                // T1 always wants A then B. T2 wants B then A, unless ordered.
                var plan = [
                    {t: "T1", want: "A"}, {t: "T2", want: same ? "A" : "B"},
                    {t: "T1", want: "B"}, {t: "T2", want: same ? "B" : "A"},
                    {t: "T1", want: "done"}, {t: "T2", want: "done"}
                ];
                var step = Math.min(ctx.params.step, plan.length);
                var held = {A: null, B: null};
                var waiting = {T1: null, T2: null};
                var done = {T1: false, T2: false};
                var log = [], i;

                for (i = 0; i < step; i++) {
                    var a = plan[i];
                    if (waiting[a.t] || done[a.t]) { continue; }
                    if (a.want === "done") {
                        // release everything this thread holds
                        Object.keys(held).forEach(function (L) {
                            if (held[L] === a.t) held[L] = null;
                        });
                        done[a.t] = true;
                        log.push(a.t + " finishes and releases its locks");
                        // a waiter can now proceed
                        Object.keys(waiting).forEach(function (T) {
                            if (waiting[T] && !held[waiting[T]]) {
                                held[waiting[T]] = T;
                                log.push(T + " was woken and took lock " + waiting[T]);
                                waiting[T] = null;
                            }
                        });
                    } else if (held[a.want] == null) {
                        held[a.want] = a.t;
                        log.push(a.t + " takes lock " + a.want);
                    } else {
                        waiting[a.t] = a.want;
                        log.push(a.t + " blocks waiting for lock " + a.want
                                 + " (held by " + held[a.want] + ")");
                    }
                }
                var stuck = waiting.T1 && waiting.T2
                    && held[waiting.T1] === "T2" && held[waiting.T2] === "T1";

                var W = 620, s = C.svgRoot(W, 118);
                ["A", "B"].forEach(function (L, k) {
                    var cx = 150 + k * 320;
                    s.appendChild(C.e("circle", {cx: cx, cy: 30, r: 15,
                        fill: held[L] ? C.ACCENT : "none", "fill-opacity": 0.8,
                        stroke: C.SUBTLE, "stroke-width": 2}));
                    s.appendChild(C.text(cx, 34, L,
                        {size: 11, anchor: "middle",
                         fill: held[L] ? "var(--bg-surface)" : C.MUTED,
                         weight: 700}));
                    s.appendChild(C.text(cx, 58,
                        held[L] ? "held by " + held[L] : "free",
                        {size: 8, anchor: "middle"}));
                });
                ["T1", "T2"].forEach(function (T, k) {
                    var y = 84 + k * 16;
                    var state = done[T] ? "finished"
                        : waiting[T] ? "waiting for " + waiting[T]
                        : "running";
                    s.appendChild(C.text(14, y, T + ": " + state,
                        {size: 9, fill: waiting[T] ? C.BAD : C.MUTED}));
                });
                if (stuck) {
                    s.appendChild(C.text(300, 92, "DEADLOCK: each holds what "
                        + "the other is waiting for",
                        {size: 10, fill: C.BAD, weight: 700}));
                }

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(s);
                var logBox = C.h("div", "vz-cc-log");
                log.forEach(function (l) {
                    logBox.appendChild(C.h("div", "vz-cc-log-line", l));
                });
                if (!log.length) {
                    logBox.appendChild(C.h("div", "vz-cc-log-line",
                        "nothing has run yet"));
                }
                ctx.stage.appendChild(logBox);
                ctx.stage.appendChild(C.stats([
                    {value: stuck ? "yes" : "no", label: "deadlocked",
                     note: stuck ? "neither can proceed" : "still moving",
                     bad: stuck},
                    {value: same ? "A then B" : "opposite", label: "lock order",
                     note: same ? "both threads agree" : "T1: A,B  T2: B,A"},
                    {value: String(step) + " / 6", label: "steps taken",
                     note: "one action each"},
                    {value: (done.T1 ? 1 : 0) + (done.T2 ? 1 : 0) + " / 2",
                     label: "threads finished",
                     note: stuck ? "and never will" : ""}
                ]));
                ctx.stage.appendChild(C.caption(
                    "With opposite orders, step 4 is the cycle: T1 holds A and "
                    + "wants B, T2 holds B and wants A, and releasing is the "
                    + "thing each is waiting to be able to do. Turn the toggle "
                    + "on and both take A first, so one simply waits and then "
                    + "proceeds - a global ordering makes the cycle "
                    + "impossible rather than unlikely."));
                ctx.setReadout(stuck
                    ? "deadlocked at step " + step
                      + ": T1 holds A wants B, T2 holds B wants A"
                    : same
                      ? "ordered acquisition: no cycle is possible, whatever the timing"
                      : "step " + step + ": no cycle yet - keep stepping");
            };
        }
    };

    // ------------------------------------------------ 4. the boundary cost
    C.WIDGETS.boundary = {
        controls: [
            {key: "task", label: "Work per task", type: "range", min: 1,
             max: 300, step: 1, value: 80,
             fmt: function (v) { return v + " ms"; }},
            {key: "mb", label: "Arguments per task", type: "range", min: 0.1,
             max: 20, step: 0.1, value: 1,
             fmt: function (v) { return C.fmt(v, 1) + " MB"; }},
            {key: "w", label: "Workers", type: "range", min: 2, max: 8, value: 4}
        ],
        build: function (ctx) {
            var SPAWN = 30;     // ms to start a process
            var RATE = 100;     // MB/s through pickle + pipe + unpickle
            return function () {
                var p = ctx.params, task = p.task, mb = p.mb, w = p.w;
                var copy = (mb / RATE) * 1000;          // ms, each way
                var seq = task * w;
                var thr = task * w;                     // GIL: no overlap
                var pro = task + w * (SPAWN + 2 * copy);
                var best = Math.min(seq, thr, pro);

                var rows = [
                    {label: "sequential", spans: [{t0: 0, t1: seq / 1000,
                      kind: "run", label: Math.round(seq) + " ms"}]},
                    {label: "threads", spans: [{t0: 0, t1: thr / 1000,
                      kind: "run", label: "same, the GIL serialises it"}]},
                    {label: "processes", hot: true, spans: [
                        {t0: 0, t1: (w * (SPAWN + 2 * copy)) / 1000,
                         kind: "block", label: "spawn + copy"},
                        {t0: (w * (SPAWN + 2 * copy)) / 1000, t1: pro / 1000,
                         kind: "run", label: "work"}]}
                ];

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(C.timeline(rows,
                    Math.max(seq, pro) / 1000, {ticks: 5, unit: "ms", padL: 74}));
                ctx.stage.appendChild(C.stats([
                    {value: Math.round(pro) + " ms", label: "processes",
                     note: pro === best ? "the winner" : "slower than sequential",
                     bad: pro > seq},
                    {value: Math.round(thr) + " ms", label: "threads",
                     note: "identical to sequential"},
                    {value: Math.round(2 * copy) + " ms", label: "copy per task",
                     note: C.fmt(mb, 1) + " MB each way at " + RATE + " MB/s"},
                    {value: Math.round(w * (SPAWN + 2 * copy)) + " ms",
                     label: "total overhead",
                     note: w + " x (" + SPAWN + " ms spawn + copy)"}
                ]));
                ctx.stage.appendChild(C.caption(
                    "Threads never beat sequential here, because the work is "
                    + "bytecode. Processes pay a fixed cost per worker and "
                    + "then run the work at once, so they win only when the "
                    + "work is larger than what it costs to ship the "
                    + "arguments. Push the arguments to 20 MB and the "
                    + "overhead swallows the parallelism."));
                ctx.setReadout(pro < seq
                    ? "processes win: " + Math.round(pro) + " ms against "
                      + Math.round(seq) + " ms, after paying "
                      + Math.round(w * (SPAWN + 2 * copy)) + " ms of overhead"
                    : "processes lose: " + Math.round(pro) + " ms against "
                      + Math.round(seq)
                      + " ms - the boundary costs more than the work saves");
            };
        }
    };

    // ------------------------------------------------------- 5. the Future
    C.WIDGETS.future = {
        controls: [
            {key: "step", label: "Advance the future", type: "range", min: 0,
             max: 2, value: 0,
             fmt: function (v) { return ["created", "picked up by a worker",
                                         "settled"][v]; }},
            {key: "fail", label: "The work raises", type: "toggle", value: false},
            {key: "cancel", label: "Call cancel() now", type: "toggle",
             value: false}
        ],
        build: function (ctx) {
            return function () {
                var p = ctx.params;
                var state = ["PENDING", "RUNNING", "FINISHED"][p.step];
                var cancelled = false;
                if (p.cancel && p.step === 0) { state = "CANCELLED"; cancelled = true; }
                var cancelReturns = (p.step === 0);
                var settled = (state === "FINISHED" || state === "CANCELLED");
                var resultBehaviour =
                    state === "PENDING" ? "blocks until it settles"
                  : state === "RUNNING" ? "blocks until it settles"
                  : state === "CANCELLED" ? "raises CancelledError"
                  : p.fail ? "re-raises ValueError" : "returns 42";

                var W = 620, s = C.svgRoot(W, 108);
                var boxes = ["PENDING", "RUNNING", "FINISHED"];
                boxes.forEach(function (name, k) {
                    var x = 30 + k * 150, active = (state === name);
                    s.appendChild(C.rect(x, 24, 118, 30,
                        {fill: active ? C.ACCENT : "none", fo: 0.85,
                         stroke: active ? C.ACCENT : C.SUBTLE, sw: 2,
                         dash: active ? null : "3 3"}));
                    s.appendChild(C.text(x + 59, 44, name,
                        {size: 10, anchor: "middle", weight: 700,
                         fill: active ? "var(--bg-surface)" : C.MUTED}));
                    if (k < 2) {
                        s.appendChild(C.line(x + 118, 39, x + 150, 39,
                            {stroke: C.SUBTLE, sw: 2}));
                    }
                });
                // the cancelled branch hangs off PENDING
                var cx = 30, act = (state === "CANCELLED");
                s.appendChild(C.line(cx + 59, 54, cx + 59, 74,
                    {stroke: act ? C.BAD : C.SUBTLE, sw: 2,
                     dash: act ? null : "3 3"}));
                s.appendChild(C.rect(cx, 74, 118, 26,
                    {fill: act ? C.BAD : "none", fo: 0.85,
                     stroke: act ? C.BAD : C.SUBTLE, sw: 2,
                     dash: act ? null : "3 3"}));
                s.appendChild(C.text(cx + 59, 91, "CANCELLED",
                    {size: 10, anchor: "middle", weight: 700,
                     fill: act ? "var(--bg-surface)" : C.MUTED}));
                s.appendChild(C.text(340, 82,
                    "cancel() only has an effect from PENDING",
                    {size: 9, fill: C.MUTED}));

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(s);
                ctx.stage.appendChild(C.stats([
                    {value: state, label: "state", note: "f._state"},
                    {value: settled ? "True" : "False", label: "done()",
                     note: "settled either way"},
                    {value: cancelReturns ? "True" : "False", label: "cancel()",
                     note: cancelReturns ? "un-queued it"
                                         : "too late, it started",
                     bad: !cancelReturns && p.cancel},
                    {value: settled ? (cancelled ? "raises" : (p.fail ? "raises" : "42"))
                                    : "blocks",
                     label: "result()", note: resultBehaviour,
                     bad: settled && (cancelled || p.fail)}
                ]));
                ctx.stage.appendChild(C.caption(
                    "A future is this and nothing more. The line worth "
                    + "keeping is cancel(): it returns True only from "
                    + "PENDING, because there is no way to interrupt a "
                    + "running Python function - so cancelling a pool drops "
                    + "the queue and lets whatever started run to the end."));
                ctx.setReadout(state === "RUNNING" && p.cancel
                    ? "cancel() returned False: the worker already has it, so it will finish"
                    : "state " + state + ", done() = " + (settled ? "True" : "False")
                      + ", result() " + resultBehaviour);
            };
        }
    };

    // ------------------------------------------ 6. a queue between threads
    C.WIDGETS.tqueue = {
        controls: [
            {key: "max", label: "maxsize", type: "range", min: 1, max: 8,
             value: 2},
            {key: "pi", label: "Producer: one item every", type: "range",
             min: 0.02, max: 0.16, step: 0.02, value: 0.02,
             fmt: function (v) { return C.fmt(v, 2) + "s"; }},
            {key: "ci", label: "Each worker takes", type: "range", min: 0.02,
             max: 0.24, step: 0.02, value: 0.12,
             fmt: function (v) { return C.fmt(v, 2) + "s"; }},
            {key: "w", label: "Workers", type: "range", min: 1, max: 4, value: 2},
            {key: "items", label: "Items", type: "range", min: 4, max: 16,
             value: 9}
        ],
        build: function (ctx) {
            return function () {
                var p = ctx.params;
                var dt = 0.005, t = 0, depth = 0, produced = 0, consumed = 0;
                var prodNext = 0, free = [], waits = 0, peak = 0, i;
                for (i = 0; i < p.w; i++) free.push(0);
                var series = [], guard = 0;
                while (consumed < p.items && guard++ < 30000) {
                    for (i = 0; i < p.w; i++) {
                        if (t >= free[i] && depth > 0) {
                            depth -= 1; consumed += 1; free[i] = t + p.ci;
                        }
                    }
                    if (produced < p.items && t >= prodNext) {
                        if (depth < p.max) {
                            depth += 1; produced += 1; prodNext = t + p.pi;
                        } else { waits += 1; }
                    }
                    peak = Math.max(peak, depth);
                    series.push({t: t, d: depth});
                    t += dt;
                }
                // consumed is incremented when a worker PICKS UP an item, so the
                // loop exits before the last one is finished. The honest total is
                // when the last worker becomes free.
                var total = Math.max.apply(null, [t].concat(free));

                var W = 620, padL = 40, padR = 14, top = 16, plotH = 92;
                var s = C.svgRoot(W, top + plotH + 32);
                var plotW = W - padL - padR;
                var x = function (tt) { return padL + (tt / total) * plotW; };
                var yMax = Math.max(p.max, peak, 1);
                var y = function (d) { return top + plotH - (d / yMax) * plotH; };
                var k;
                for (k = 0; k <= yMax; k++) {
                    s.appendChild(C.line(padL, y(k), W - padR, y(k),
                        {stroke: C.SUBTLE, dash: k ? "2 4" : null}));
                    s.appendChild(C.text(padL - 6, y(k) + 3, String(k),
                        {size: 8, anchor: "end"}));
                }
                s.appendChild(C.line(padL, y(p.max), W - padR, y(p.max),
                    {stroke: C.BAD, sw: 1.4, dash: "5 3"}));
                s.appendChild(C.text(W - padR, y(p.max) - 4, "maxsize",
                    {size: 8, anchor: "end", fill: C.BAD}));

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
                s.appendChild(C.e("path", {d: path, fill: "none",
                    stroke: C.ACCENT, "stroke-width": 1.8}));
                s.appendChild(C.text(padL, top + plotH + 22,
                    "queue depth over time - " + C.fmt(total, 2) + "s to drain "
                    + p.items + " items through " + p.w + " worker"
                    + (p.w > 1 ? "s" : ""), {size: 8}));

                var throttled = waits > 0;
                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(s);
                ctx.stage.appendChild(C.stats([
                    {value: String(peak), label: "peak depth",
                     note: throttled ? "pinned at maxsize" : "never filled"},
                    {value: throttled ? "yes" : "no", label: "producer blocked",
                     note: throttled ? "put() waited" : "never waited"},
                    {value: C.fmt(total, 2) + "s", label: "to drain",
                     note: "the workers set the pace"},
                    {value: C.fmt(p.items * p.ci / p.w, 2) + "s",
                     label: "work alone",
                     note: p.items + " x " + C.fmt(p.ci, 2) + "s / " + p.w}
                ]));
                ctx.stage.appendChild(C.caption(
                    "The red line is maxsize. Where the depth sits on it, "
                    + "put() is blocking and the producer is running at the "
                    + "workers' pace - that is backpressure, and it is the "
                    + "whole reason to bound the queue. Add workers and the "
                    + "queue drains faster until the producer becomes the "
                    + "limit instead."));
                ctx.setReadout(throttled
                    ? "queue pinned at " + peak + " of " + p.max
                      + ": the producer waited, so it ran at the workers' rate"
                    : "peak depth " + peak + " of " + p.max
                      + ": the workers kept up, so put() never blocked");
            };
        }
    };

    // ----------------------------------------------- 7. the speed-up curves
    C.WIDGETS.speedup = {
        controls: [
            {key: "cpu", label: "Time holding the GIL", type: "range", min: 0,
             max: 100, step: 5, value: 30,
             fmt: function (v) { return v + "%"; }},
            {key: "wmax", label: "Workers on the axis", type: "range", min: 4,
             max: 32, step: 4, value: 16},
            {key: "oh", label: "Process overhead per worker", type: "range",
             min: 0, max: 20, step: 1, value: 3,
             fmt: function (v) { return v + "% of one unit"; }}
        ],
        build: function (ctx) {
            return function () {
                var p = ctx.params, c = p.cpu / 100, wmax = p.wmax,
                    oh = p.oh / 100;
                // threads and async: only the waiting overlaps -> Amdahl with s = c
                var thr = function (w) { return 1 / (c + (1 - c) / w); };
                // processes: everything overlaps, but each worker costs
                // Work divides by w; the per-worker overhead adds up, so
                // the curve rises and then falls once overhead dominates.
                var pro = function (w) { return 1 / (1 / w + oh * w); };
                var ceiling = c > 0 ? 1 / c : Infinity;

                var W = 620, padL = 44, padR = 96, top = 14, plotH = 150;
                var s = C.svgRoot(W, top + plotH + 34);
                var plotW = W - padL - padR;
                var sMax = Math.max(thr(wmax), pro(wmax), 2) * 1.12;
                var X = function (w) { return padL + ((w - 1) / (wmax - 1)) * plotW; };
                var Y = function (v) { return top + plotH - (v / sMax) * plotH; };

                var g;
                for (g = 0; g <= 4; g++) {
                    var v = (sMax / 4) * g;
                    s.appendChild(C.line(padL, Y(v), W - padR, Y(v),
                        {stroke: C.SUBTLE, dash: g ? "2 4" : null}));
                    s.appendChild(C.text(padL - 6, Y(v) + 3, C.fmt(v, 1) + "x",
                        {size: 8, anchor: "end"}));
                }
                [1, Math.round(wmax / 2), wmax].forEach(function (w) {
                    s.appendChild(C.text(X(w), top + plotH + 15, String(w),
                        {size: 8, anchor: "middle"}));
                });
                s.appendChild(C.text(padL, top + plotH + 30, "workers",
                    {size: 8}));

                function curve(fn, colour, dash) {
                    var d = "", w;
                    for (w = 1; w <= wmax; w++) {
                        d += (w === 1 ? "M" : " L") + X(w) + " " + Y(fn(w));
                    }
                    return C.e("path", {d: d, fill: "none", stroke: colour,
                                        "stroke-width": 2.2,
                                        "stroke-dasharray": dash});
                }
                if (isFinite(ceiling) && ceiling < sMax) {
                    s.appendChild(C.line(padL, Y(ceiling), W - padR, Y(ceiling),
                        {stroke: C.BAD, sw: 1.3, dash: "6 4"}));
                    s.appendChild(C.text(W - padR + 6, Y(ceiling) + 3,
                        "ceiling " + C.fmt(ceiling, 1) + "x",
                        {size: 8, fill: C.BAD}));
                }
                s.appendChild(curve(pro, C.ACCENT, null));
                s.appendChild(curve(thr, C.MUTED, "5 3"));
                s.appendChild(C.text(W - padR + 6, Y(pro(wmax)) + 3, "processes",
                    {size: 8, fill: C.ACCENT}));
                s.appendChild(C.text(W - padR + 6, Y(thr(wmax)) + 3,
                    "threads / async", {size: 8, fill: C.MUTED}));

                ctx.stage.innerHTML = "";
                ctx.stage.appendChild(s);
                ctx.stage.appendChild(C.stats([
                    {value: isFinite(ceiling) ? C.fmt(ceiling, 1) + "x" : "none",
                     label: "thread ceiling",
                     note: c > 0 ? "1 / " + C.fmt(c, 2) + ", any number of threads"
                                 : "pure waiting, no ceiling"},
                    {value: C.fmt(thr(wmax), 1) + "x", label: "threads at " + wmax,
                     note: "same for async"},
                    {value: C.fmt(pro(wmax), 1) + "x", label: "processes at " + wmax,
                     note: oh ? "after overhead" : "no overhead assumed"},
                    {value: C.fmt(thr(4), 1) + "x", label: "threads at 4",
                     note: "most of the ceiling already"}
                ]));
                ctx.stage.appendChild(C.caption(
                    "Threads and async share one curve, because both run one "
                    + "thread: only the waiting overlaps, so the GIL-holding "
                    + "fraction is the serial part and 1/c is the hard "
                    + "ceiling. Processes overlap the computing too and bend "
                    + "the other way once the per-worker overhead bites. Set "
                    + "the GIL time to 100% and the thread curve flattens at "
                    + "1x, which is the two-threads-on-CPU-work measurement "
                    + "from the first page of this track."));
                ctx.setReadout(c === 0
                    ? "pure waiting: threads and async scale with workers, and processes buy nothing extra"
                    : c === 1
                    ? "pure computing: threads and async are stuck at 1.0x however many you add"
                    : C.fmt(c * 100, 0) + "% of the time holds the GIL, so threads cannot beat "
                      + C.fmt(ceiling, 1) + "x, and reach " + C.fmt(thr(4), 1)
                      + "x by four");
            };
        }
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
