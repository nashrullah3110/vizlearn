/* In-browser JavaScript runner for /js-lab/.
 *
 * Your code runs on the real JavaScript engine of the browser - no VM, no
 * interpreter to download - inside a Web Worker so that an infinite loop is
 * killed by a timeout instead of freezing the page. A fresh Worker is created
 * for every run that times out; the rest of the time the engine is already
 * warm.
 *
 * Markup the page supplies (one or more per page):
 *
 *   <div class="vz-js" data-vz-js>
 *     <script type="text/plain" class="js-src">console.log("hi")</script>
 *     <textarea class="js-editor" aria-label="JavaScript code editor"></textarea>
 *     <button type="button" class="js-run-btn">Run</button>
 *     <button type="button" class="js-reset-btn">Reset</button>
 *     <pre class="js-output" aria-live="polite"></pre>
 *     <span class="js-status"></span>
 *   </div>
 *
 * Nothing here knows which page it is on; it wires every .vz-js block.
 *
 * What gets captured:
 *   - console.log / info / warn / error / debug output, in the order written
 *   - an alias `print` for console.log, so the page reads like the Python lab
 *   - uncaught errors (synchronous and, via the Worker's onerror, any that
 *     leak out of a timer or promise)
 *
 * Each Run evaluates the code through a fresh `new Function`, so names left
 * over from a previous Run can never make a later one appear to work.
 */
(function () {
  'use strict';

  var RUN_TIMEOUT = 10000;

  var RUNNER_SRC = [
    'function emit(text, cls) { postMessage({ type: "out", text: text, cls: cls || "" }); }',
    'function fmt(v) {',
    '  if (typeof v === "string") return v;',
    '  if (v instanceof Error) return (v.stack || (v.name + ": " + v.message));',
    '  if (typeof v === "function") return String(v);',
    '  if (v !== null && typeof v === "object") {',
    '    try { return JSON.stringify(v, null, 2); } catch (e) { return String(v); }',
    '  }',
    '  return String(v);',
    '}',
    'function pipe(cls) {',
    '  return function () {',
    '    var parts = [];',
    '    for (var i = 0; i < arguments.length; i++) parts.push(fmt(arguments[i]));',
    '    emit(parts.join(" "), cls);',
    '  };',
    '}',
    'console.log = pipe("");',
    'console.info = pipe("");',
    'console.debug = pipe("");',
    'console.warn = pipe("warn");',
    'console.error = pipe("err");',
    'console.clear = function () { emit("", "clear"); };',
    'var print = function () { console.log.apply(null, arguments); };',
    'self.onerror = function (e) {',
    '  emit(e && (e.message || e.error) ? String(e.message || e.error) : "Uncaught error", "err");',
    '};',
    'self.onmessage = function (e) {',
    '  var m = e.data;',
    '  if (m.type !== "run") return;',
    '  try {',
    '    var fn = new Function(m.code);',
    '    fn();',
    '  } catch (err) {',
    '    emit(String((err && err.stack) || err), "err");',
    '  }',
    '  emit("", "done");',
    '};'
  ].join('\n');

  var worker = null;

  function makeWorker() {
    var blob = new Blob([RUNNER_SRC], { type: 'application/javascript' });
    var url = URL.createObjectURL(blob);
    var w = new Worker(url);
    URL.revokeObjectURL(url);
    return w;
  }

  function ensureWorker() {
    if (!worker) worker = makeWorker();
    return worker;
  }

  function killWorker() {
    if (worker) {
      worker.terminate();
      worker = null;
    }
  }

  function els(block) {
    return {
      editor: block.querySelector('.js-editor'),
      output: block.querySelector('.js-output'),
      run: block.querySelector('.js-run-btn'),
      reset: block.querySelector('.js-reset-btn'),
      status: block.querySelector('.js-status'),
      src: block.querySelector('.js-src'),
    };
  }

  function setStatus(block, text) {
    var s = els(block).status;
    if (s) s.textContent = text || '';
  }

  function makePlaceholder() {
    var span = document.createElement('span');
    span.className = 'js-placeholder';
    span.textContent = 'Press Run to execute this code.';
    return span;
  }

  function appendOut(block, text, cls) {
    var out = els(block).output;
    if (!out) return;
    var placeholder = out.querySelector('.js-placeholder');
    if (placeholder) placeholder.remove();
    if (cls) {
      var span = document.createElement('span');
      span.className = 'js-out-' + cls;
      span.textContent = text;
      out.appendChild(span);
    } else {
      out.appendChild(document.createTextNode(text));
    }
    if (!text.endsWith('\n')) out.appendChild(document.createTextNode('\n'));
    out.scrollTop = out.scrollHeight;
  }

  function indentOnEnter(editor) {
    editor.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      var lineStart = editor.value.lastIndexOf('\n', editor.selectionStart - 1) + 1;
      var line = editor.value.slice(lineStart, editor.selectionStart);
      var ws = /^[ \t]*/.exec(line);
      var padding = ws ? ws[0] : '';
      // Keep a line that ends in `{` indented one level deeper, and drop a
      // level for a line that begins with `}`.
      if (/\{\s*$/.test(line)) padding += '  ';
      if (/^\s*[\}\]]/.test(line)) {
        padding = padding.replace(/ {2}$/, '');
      }
      e.preventDefault();
      editor.value = editor.value.slice(0, editor.selectionStart) +
        '\n' + padding + editor.value.slice(editor.selectionEnd);
      editor.selectionStart = editor.selectionEnd =
        editor.selectionStart + 1 + padding.length;
    });
  }

  function runBlock(block, code) {
    var parts = els(block);
    var out = parts.output;
    out.textContent = '';
    parts.run.disabled = true;
    setStatus(block, 'Running\u2026');

    var timedOut = false;
    var timer = setTimeout(function () {
      timedOut = true;
      killWorker();
      appendOut(block, 'Execution timed out', 'js-out-err');
      appendOut(block, 'The engine was stopped \u2014 the code probably looped forever.', 'js-out-hint');
      setStatus(block, 'Timed out');
      parts.run.disabled = false;
    }, RUN_TIMEOUT);

    try {
      var w = ensureWorker();
      setStatus(block, 'Running\u2026');
      var finish = function () {
        clearTimeout(timer);
        if (timedOut) return;
        setStatus(block, '');
        parts.run.disabled = false;
      };
      w.onmessage = function (e) {
        if (timedOut) return;
        if (e.data.type === 'clear') {
          out.textContent = '';
        } else if (e.data.type === 'out') {
          appendOut(block, e.data.text, e.data.cls || null);
        } else if (e.data.type === 'done') {
          finish();
        }
      };
      w.onerror = function (e) {
        if (timedOut) return;
        appendOut(block, (e && e.message) || 'worker error', 'js-out-err');
        finish();
      };
      w.postMessage({ type: 'run', code: code });
    } catch (err) {
      clearTimeout(timer);
      appendOut(block, String(err), 'js-out-err');
      finish();
    }
  }

  function init() {
    var blocks = document.querySelectorAll('.vz-js');
    for (var i = 0; i < blocks.length; i++) {
      (function (block) {
        var parts = els(block);
        if (!parts.editor || !parts.run) return;
        if (parts.src) {
          parts.editor.value = (parts.src.textContent || '').replace(/^\n+|\s+$/g, '');
        }
        indentOnEnter(parts.editor);

        parts.run.addEventListener('click', function () {
          if (parts.run.disabled) return;
          runBlock(block, parts.editor.value);
        });

        if (parts.reset) parts.reset.addEventListener('click', function () {
          if (parts.src) parts.editor.value = (parts.src.textContent || '').trim();
          parts.output.textContent = '';
          parts.output.appendChild(makePlaceholder());
          setStatus(block, '');
        });

        if (parts.output) {
          parts.output.appendChild(makePlaceholder());
        }
      })(blocks[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
