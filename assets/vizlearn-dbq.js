/* Query variants and two-transaction timelines for the generated database/
 * modules.
 *
 * Two jobs, both small, both only meaningful on those pages.
 *
 * 1. Variant buttons. Several of these modules ask one question and answer it
 *    three ways - EXISTS against IN against a JOIN, a correlated subquery
 *    against a window function. Making the reader retype each version is a
 *    tax on the comparison, so each variant is a button that loads its query
 *    into the editor and runs it. The queries are real and the results come
 *    from the same SQLite the lab uses; nothing here is a recording.
 *
 * 2. Concurrency timelines. Isolation levels and deadlocks need two
 *    transactions interleaved, and the in-page database has one connection.
 *    Rather than fake a second one, those modules step through a scripted
 *    timeline and say what each statement would see under the chosen level.
 *    The step is the reader's; only the schedule is fixed.
 *
 * Binds to [data-vz-dbq] and [data-vz-timeline]; costs nothing elsewhere.
 */
(function () {
    "use strict";

    // ------------------------------------------------------------- variants

    function wireVariants(root) {
        var buttons = [].slice.call(root.querySelectorAll(".db-variant"));
        if (!buttons.length) return;

        // The editor and Run button belong to the vizlearn-sql block, which is
        // a sibling rather than a child - the buttons sit above the editor.
        var scope = root.closest("[data-vz-sql]") ||
                    document.querySelector("[data-vz-sql]");
        if (!scope) return;
        var editor = scope.querySelector(".sql-editor");
        var run = scope.querySelector(".sql-run-btn");
        if (!editor || !run) return;

        buttons.forEach(function (btn) {
            btn.addEventListener("click", function () {
                var src = btn.querySelector(".db-variant-sql");
                if (!src) return;
                editor.value = src.textContent.replace(/^\n/, "").replace(/\s+$/, "");
                // vizlearn-code.js repaints the highlight layer from input
                // events, so setting .value alone would leave the old query
                // showing under the caret.
                editor.dispatchEvent(new Event("input", { bubbles: true }));
                buttons.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
                btn.setAttribute("aria-pressed", "true");
                run.click();
            });
        });
        buttons[0].setAttribute("aria-pressed", "true");
    }

    // ------------------------------------------------------------ timelines

    function wireTimeline(root) {
        var cfgEl = root.querySelector(".db-timeline-config");
        if (!cfgEl) return;
        var cfg;
        try { cfg = JSON.parse(cfgEl.textContent); } catch (e) { return; }

        var steps = cfg.steps || [];
        var levels = cfg.levels || [];
        var at = 0, level = levels.length ? levels[0].value : "";

        root.innerHTML = "";

        var picker = document.createElement("div");
        picker.className = "db-tl-levels";
        levels.forEach(function (l) {
            var b = document.createElement("button");
            b.type = "button";
            b.className = "db-tl-level";
            b.textContent = l.label;
            b.addEventListener("click", function () { level = l.value; draw(); });
            picker.appendChild(b);
        });
        if (levels.length) root.appendChild(picker);

        var table = document.createElement("div");
        table.className = "db-tl";
        root.appendChild(table);

        var bar = document.createElement("div");
        bar.className = "db-tl-controls";
        var back = document.createElement("button");
        back.type = "button"; back.className = "db-tl-btn"; back.textContent = "Back";
        var fwd = document.createElement("button");
        fwd.type = "button"; fwd.className = "db-tl-btn db-tl-btn-primary";
        fwd.textContent = "Step";
        var reset = document.createElement("button");
        reset.type = "button"; reset.className = "db-tl-btn"; reset.textContent = "Restart";
        back.addEventListener("click", function () { at = Math.max(0, at - 1); draw(); });
        fwd.addEventListener("click", function () { at = Math.min(steps.length, at + 1); draw(); });
        reset.addEventListener("click", function () { at = 0; draw(); });
        bar.appendChild(back); bar.appendChild(fwd); bar.appendChild(reset);
        root.appendChild(bar);

        var note = document.createElement("p");
        note.className = "db-tl-note";
        note.setAttribute("aria-live", "polite");
        root.appendChild(note);

        function draw() {
            [].slice.call(picker.children).forEach(function (b, i) {
                b.setAttribute("aria-pressed", String(levels[i].value === level));
            });
            table.innerHTML = "";
            var head = document.createElement("div");
            head.className = "db-tl-row db-tl-head";
            ["", cfg.a || "Transaction A", cfg.b || "Transaction B"].forEach(function (h) {
                var c = document.createElement("div");
                c.className = "db-tl-cell";
                c.textContent = h;
                head.appendChild(c);
            });
            table.appendChild(head);

            steps.forEach(function (s, i) {
                var row = document.createElement("div");
                row.className = "db-tl-row" + (i < at ? " is-done" : "") +
                                (i === at - 1 ? " is-current" : "");
                var n = document.createElement("div");
                n.className = "db-tl-cell db-tl-n";
                n.textContent = String(i + 1);
                row.appendChild(n);
                ["a", "b"].forEach(function (who) {
                    var c = document.createElement("div");
                    c.className = "db-tl-cell db-tl-sql";
                    if (s.who === who) c.textContent = s.sql;
                    row.appendChild(c);
                });
                table.appendChild(row);
            });

            back.disabled = at === 0;
            fwd.disabled = at >= steps.length;
            if (at === 0) {
                note.textContent = cfg.intro || "Press Step to run the first statement.";
            } else {
                var s = steps[at - 1];
                note.textContent = (s.says && (s.says[level] || s.says["*"])) || "";
            }
        }

        draw();
        root.dataset.vzTimelineReady = "1";
    }

    function init() {
        [].slice.call(document.querySelectorAll("[data-vz-dbq]")).forEach(wireVariants);
        [].slice.call(document.querySelectorAll("[data-vz-timeline]")).forEach(wireTimeline);
    }

    if (document.readyState === "loading")
        document.addEventListener("DOMContentLoaded", init);
    else init();
})();
