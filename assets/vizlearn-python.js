/* In-browser Python runner for the python/ track.
 *
 * Real CPython (Pyodide, compiled to WebAssembly) runs student code inside a
 * Web Worker, so an infinite loop is killed by a timeout instead of freezing
 * the page. The interpreter is loaded lazily from the CDN on the first Run and
 * then stays warm for the rest of the visit.
 *
 * Markup the page supplies (one or more per page):
 *
 *   <div class="vz-py" data-vz-py>
 *     <script type="text/plain" class="py-src">print("Hello, Python!")</script>
 *     <textarea class="py-editor" aria-label="Python code editor"></textarea>
 *     <button type="button" class="py-run-btn">Run</button>
 *     <button type="button" class="py-reset-btn">Reset</button>
 *     <pre class="py-output" aria-live="polite"></pre>
 *     <span class="py-status"></span>
 *   </div>
 *
 * Nothing here knows which module it is on; it finds every .vz-py block on the
 * page and wires each independently, sharing the single interpreter.
 */
(function () {
  'use strict';

  var PYODIDE_VERSION = '0.26.4';
  var PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v' + PYODIDE_VERSION + '/full/';
  var RUN_TIMEOUT = 10000;

  // Runs the student's code inside Pyodide. A single-expression program is
  // evaluated so its value is shown REPL-style; anything longer is exec'd so
  // it behaves exactly like a .py script.
  //
  // Three things here are load-bearing and were each a bug:
  //
  //   ast.Expression(...)  ast.parse() returns a Module, and compiling a
  //                        Module in "eval" mode raises "expected Expression
  //                        node, got Module". Every single-expression program
  //                        failed - including print("Hello, Python!"), the
  //                        default code on the first module of the track.
  //
  //   the `g` dict         exec(code) with no namespace runs in _viz_run's
  //                        *locals*, but a function defined by that code
  //                        resolves names against module globals. So
  //                        `x = 10` then `def show(): print(x)` raised
  //                        NameError - the single most common shape of
  //                        beginner Python there is. Passing one dict as the
  //                        namespace makes user code behave like a module,
  //                        which is what a .py file does.
  //
  //   the traceback trim   an error otherwise showed five frames of Pyodide
  //                        internals (_pyodide/_base.py, eval_code_async)
  //                        above the one line the reader actually wrote.
  //
  // `g` is rebuilt per run, so a name left over from a previous Run can never
  // make a later one appear to work.
  var RUNNER_SRC = [
    'import ast, sys, traceback',
    'def _viz_run(code):',
    '    g = {"__name__": "__main__"}',
    '    try:',
    '        tree = ast.parse(code, "<user>", "exec")',
    '        if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):',
    '            expr = ast.Expression(tree.body[0].value)',
    '            val = eval(compile(expr, "<user>", "eval"), g)',
    '            if val is not None:',
    '                print(repr(val))',
    '        else:',
    '            exec(compile(tree, "<user>", "exec"), g)',
    '    except SyntaxError as e:',
    '        sys.stderr.write("SyntaxError: %s (line %s)\\n" % (e.msg, e.lineno))',
    '    except BaseException as e:',
    '        tb = e.__traceback__',
    '        while tb is not None and tb.tb_frame.f_code.co_filename != "<user>":',
    '            tb = tb.tb_next',
    '        sys.stderr.write("".join(traceback.format_exception(type(e), e, tb)))',
  ].join('\n');

  var worker = null;
  var workerReady = null;

  function makeWorker() {
    var wsrc =
      'importScripts("' + PYODIDE_URL + 'pyodide.js");\n' +
      'var py = null;\n' +
      'self.onmessage = function (e) {\n' +
      '  var m = e.data;\n' +
      '  if (m.type === "init") {\n' +
      '    loadPyodide({ indexURL: "' + PYODIDE_URL + '" }).then(function (p) {\n' +
      '      py = p;\n' +
      '      py.setStdout({ batched: function (s) { postMessage({ type: "out", text: s }); } });\n' +
      '      py.setStderr({ batched: function (s) { postMessage({ type: "err", text: s }); } });\n' +
      '      try { py.runPython(' + JSON.stringify(RUNNER_SRC) + '); }\n' +
      '      catch (err) { postMessage({ type: "err", text: String(err) }); }\n' +
      '      postMessage({ type: "ready" });\n' +
      '    }).catch(function (err) { postMessage({ type: "fatal", text: String(err) }); });\n' +
      '  } else if (m.type === "run") {\n' +
      '    try { py.globals.set("__code__", m.code); }\n' +
      '    catch (err) { postMessage({ type: "err", text: String(err) }); }\n' +
      '    py.runPythonAsync("_viz_run(__code__)").then(function () {\n' +
      '      postMessage({ type: "done" });\n' +
      '    }, function (err) {\n' +
      '      var msg = (err && (err.message || err.toString())) || String(err);\n' +
      '      postMessage({ type: "err", text: msg });\n' +
      '      postMessage({ type: "done" });\n' +
      '    });\n' +
      '  }\n' +
      '};\n';
    var blob = new Blob([wsrc], { type: 'application/javascript' });
    var url = URL.createObjectURL(blob);
    var w = new Worker(url);
    URL.revokeObjectURL(url);
    return w;
  }

  function ensureWorker() {
    if (worker) return workerReady;
    worker = makeWorker();
    workerReady = new Promise(function (resolve, reject) {
      var settled = false;
      worker.onmessage = function (e) {
        if (e.data.type === 'ready') { settled = true; resolve(); }
        else if (e.data.type === 'fatal') { settled = true; reject(new Error(e.data.text)); }
      };
      worker.onerror = function (e) {
        if (!settled) { settled = true; reject(new Error(e.message || 'worker failed')); }
      };
      worker.postMessage({ type: 'init' });
    });
    workerReady.catch(function () {
      worker.terminate();
      worker = null;
      workerReady = null;
    });
    return workerReady;
  }

  function els(block) {
    return {
      editor: block.querySelector('.py-editor'),
      output: block.querySelector('.py-output'),
      run: block.querySelector('.py-run-btn'),
      reset: block.querySelector('.py-reset-btn'),
      status: block.querySelector('.py-status'),
      src: block.querySelector('.py-src'),
    };
  }

  function indentOnTab(editor) {
    editor.addEventListener('keydown', function (e) {
      if (e.key === 'Tab') {
        e.preventDefault();
        var start = editor.selectionStart;
        var end = editor.selectionEnd;
        editor.value = editor.value.slice(0, start) + '  ' + editor.value.slice(end);
        editor.selectionStart = editor.selectionEnd = start + 2;
      } else if (e.key === 'Enter') {
        var lineStart = editor.value.lastIndexOf('\n', editor.selectionStart - 1) + 1;
        var line = editor.value.slice(lineStart, editor.selectionStart);
        var ws = /^[ \t]*/.exec(line);
        var padding = ws ? ws[0] : '';
        // Keep a colon-line indented one level deeper.
        if (/:\s*$/.test(line)) padding += '  ';
        e.preventDefault();
        editor.value = editor.value.slice(0, editor.selectionStart) +
          '\n' + padding + editor.value.slice(editor.selectionEnd);
        editor.selectionStart = editor.selectionEnd =
          editor.selectionStart + 1 + padding.length;
      }
    });
  }

  function setStatus(block, text) {
    var s = els(block).status;
    if (s) s.textContent = text || '';
  }

  function appendOut(block, text, cls) {
    var out = els(block).output;
    if (!out) return;
    var placeholder = out.querySelector('.py-placeholder');
    if (placeholder) placeholder.remove();
    if (cls) {
      var span = document.createElement('span');
      span.className = cls;
      span.textContent = text;
      out.appendChild(span);
    } else {
      out.appendChild(document.createTextNode(text));
    }
    if (!text.endsWith('\n')) out.appendChild(document.createTextNode('\n'));
    out.scrollTop = out.scrollHeight;
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
      appendOut(block, 'Execution timed out', 'py-out-err');
      appendOut(block, 'The interpreter was stopped \u2014 the code probably looped forever.', 'py-out-hint');
      setStatus(block, 'Timed out');
      parts.run.disabled = false;
    }, RUN_TIMEOUT);

    ensureWorker().then(function () {
      // The timeout may already have fired and terminated the worker while
      // this promise was still pending; `worker` is null in that case.
      if (timedOut || !worker) return;
      setStatus(block, 'Running\u2026');
      var finish = function () {
        clearTimeout(timer);
        if (timedOut) return;
        setStatus(block, '');
        parts.run.disabled = false;
      };
      worker.onmessage = function (e) {
        if (timedOut) return;
        if (e.data.type === 'out') appendOut(block, e.data.text);
        else if (e.data.type === 'err') appendOut(block, e.data.text, 'py-out-err');
        else if (e.data.type === 'done') finish();
      };
      worker.onerror = function (e) {
        if (timedOut) return;
        appendOut(block, (e && e.message) || 'worker error', 'py-out-err');
        finish();
      };
      try {
        worker.postMessage({ type: 'run', code: code });
      } catch (err) {
        appendOut(block, String(err), 'py-out-err');
        finish();
      }
    }).catch(function (err) {
      clearTimeout(timer);
      appendOut(block, 'Could not load the Python interpreter.', 'py-out-err');
      appendOut(block, String(err.message || err), 'py-out-hint');
      appendOut(block, 'Check the connection and try again.', 'py-out-hint');
      setStatus(block, 'Offline?');
      parts.run.disabled = false;
    });
  }

  function killWorker() {
    if (worker) {
      worker.terminate();
      worker = null;
      workerReady = null;
    }
  }

  function init() {
    var blocks = document.querySelectorAll('.vz-py');
    for (var i = 0; i < blocks.length; i++) {
      (function (block) {
        var parts = els(block);
        if (!parts.editor || !parts.run) return;
        if (parts.src) {
          parts.editor.value = (parts.src.textContent || '').replace(/^\n+|\s+$/g, '');
        }
        indentOnTab(parts.editor);

        parts.run.addEventListener('click', function () {
          if (parts.run.disabled) return;
          runBlock(block, parts.editor.value);
        });

        // Guarded: this used to be unconditional, so a block authored without
        // a Reset button would throw here and, because init() wires blocks in
        // a plain loop, every *later* block on the page silently stayed dead.
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

  function makePlaceholder() {
    var span = document.createElement('span');
    span.className = 'py-placeholder';
    span.textContent = 'Press Run to execute this code.';
    return span;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
