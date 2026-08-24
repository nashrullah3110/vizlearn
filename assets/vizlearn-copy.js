/* A copy button on every code block.
 *
 * The site has two kinds. Articles carry <pre><code> blocks written by
 * tools/prose.py from fenced source, and the labs and code modules carry a
 * live editor - a .vz-code with a textarea the reader can type into. Both are
 * code somebody would want to take away, so both get a button.
 *
 * The button is added at runtime rather than baked into the markup by the
 * build. A <pre> is whitespace-significant: anything inserted inside it becomes
 * part of what the reader copies when they select the block by hand, which is
 * exactly the text the button is meant to hand over cleanly. Adding it from
 * script keeps the copied text identical to the source.
 *
 * Binds to pre > code and [data-vz-code]; costs nothing on a page with neither.
 */
(function () {
    "use strict";

    var COPY = "Copy";
    var DONE = "Copied";
    var FAIL = "Press Ctrl+C";

    /* Clipboard access needs a secure context. On plain http - a local
     * preview, say - navigator.clipboard is undefined, so fall back to a
     * hidden textarea and execCommand rather than losing the button. */
    function write(text) {
        if (navigator.clipboard && window.isSecureContext)
            return navigator.clipboard.writeText(text);
        return new Promise(function (resolve, reject) {
            var ta = document.createElement("textarea");
            ta.value = text;
            ta.setAttribute("readonly", "");
            ta.style.position = "fixed";
            ta.style.top = "-1000px";
            ta.style.opacity = "0";
            document.body.appendChild(ta);
            ta.select();
            var ok = false;
            try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
            document.body.removeChild(ta);
            ok ? resolve() : reject(new Error("execCommand refused"));
        });
    }

    function icon() {
        return '<svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true" ' +
               'fill="none" stroke="currentColor" stroke-width="1.5" ' +
               'stroke-linecap="round" stroke-linejoin="round">' +
               '<rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/>' +
               '<path d="M10.5 3.5a1.5 1.5 0 0 0-1.5-1.5H4a1.5 1.5 0 0 0-1.5 1.5V9A1.5 1.5 0 0 0 4 10.5"/>' +
               '</svg>';
    }

    function button(getText) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "vz-copy";
        btn.innerHTML = icon() + '<span class="vz-copy-label">' + COPY + "</span>";
        btn.setAttribute("aria-label", "Copy code to clipboard");

        var timer = null;
        btn.addEventListener("click", function () {
            var label = btn.querySelector(".vz-copy-label");
            write(getText()).then(function () {
                btn.classList.add("is-done");
                label.textContent = DONE;
                /* The button announces its own result, so a screen reader is
                 * told the copy happened rather than only sighted users. */
                btn.setAttribute("aria-label", "Code copied to clipboard");
            }, function () {
                btn.classList.add("is-failed");
                label.textContent = FAIL;
            });
            clearTimeout(timer);
            timer = setTimeout(function () {
                btn.classList.remove("is-done", "is-failed");
                label.textContent = COPY;
                btn.setAttribute("aria-label", "Copy code to clipboard");
            }, 1800);
        });
        return btn;
    }

    function wrapPre(pre) {
        if (pre.parentNode && pre.parentNode.classList.contains("vz-copy-wrap")) return;
        var code = pre.querySelector("code");
        if (!code) return;

        var wrap = document.createElement("div");
        wrap.className = "vz-copy-wrap";
        pre.parentNode.insertBefore(wrap, pre);
        wrap.appendChild(pre);
        wrap.appendChild(button(function () {
            /* textContent, not innerText: innerText collapses runs of blank
             * lines and would hand back code that differs from the block. */
            return code.textContent.replace(/\s+$/, "");
        }));
    }

    function wireEditor(block) {
        if (block.querySelector(".vz-copy")) return;
        var input = block.querySelector(".vz-code-input");
        if (!input) return;
        var btn = button(function () { return input.value.replace(/\s+$/, ""); });
        btn.classList.add("vz-copy-editor");

        /* The bar above the editor already names the file and the language, so
         * the button belongs in it. Blocks without a bar get the button
         * floated over the editor's own corner instead. */
        var bar = block.parentNode &&
                  block.parentNode.querySelector(".vz-code-bar");
        if (bar) bar.appendChild(btn);
        else block.appendChild(btn);
    }

    function init() {
        Array.prototype.forEach.call(document.querySelectorAll("pre > code"),
            function (code) { wrapPre(code.parentNode); });
        Array.prototype.forEach.call(document.querySelectorAll("[data-vz-code]"),
            wireEditor);
    }

    if (document.readyState === "loading")
        document.addEventListener("DOMContentLoaded", init);
    else init();
})();
