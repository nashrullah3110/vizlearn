/* In-browser Python runner for the python/ track.
 *
 * Real CPython (Pyodide, compiled to WebAssembly) runs student code inside a
 * Web Worker, so an infinite loop is killed by a timeout instead of freezing
 * the page. The interpreter is loaded lazily from the CDN on the first Run and
 * then stays warm for the rest of the visit.
 *
 * Markup the page supplies (one or more per page):
 *
 *   <div class="vz-py" data-vz-py data-vz-packages="pydantic">
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
 *
 * data-vz-packages is an optional comma-separated list of Pyodide packages the
 * block needs - "pydantic" for the Pydantic track. They are fetched from the
 * same CDN as the interpreter on the first Run that asks for them and then
 * stay loaded for the rest of the visit, so a page with four Pydantic editors
 * downloads the library once.
 *
 * data-vz-wheels is the same idea for libraries Pyodide does not ship: a
 * comma-separated list of .whl paths, installed with micropip. They are
 * resolved against the page before being handed to the worker, because the
 * worker is created from a blob: URL and a relative path means nothing there.
 * The wheels are served from this site rather than PyPI, so the versions are
 * pinned and a run does not depend on a third party being up.
 *
 * An optional <script type="text/plain" class="py-prelude"> inside the block
 * is executed in the same namespace immediately before the reader's code and
 * is not shown in the editor. It exists for setup that a library needs but a
 * lesson should not open with - /fastapi-lab/ uses it for the test client.
 * Keep it small: code the reader cannot see is code they cannot debug.
 *
 * data-vz-label names the download in the status line ("Loading FastAPI...")
 * where the bare package list would be four names long.
 */
(function () {
  'use strict';

  var PYODIDE_VERSION = '0.26.4';
  var PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v' + PYODIDE_VERSION + '/full/';
  var RUN_TIMEOUT = 10000;
  // The interpreter is a multi-megabyte download on the first Run of a visit,
  // and on a slow connection that alone can outlast anything a run is allowed.
  // The two are timed separately: sharing one budget meant a first Run on a
  // heavy page reported "the code probably looped forever" while the code had
  // not started.
  var LOAD_TIMEOUT = 60000;

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
    // A program that draws does not print, so without this the editor
    // reports success and shows nothing. Figures are collected after the
    // run, encoded, and handed back for the page to display.
    //
    // pyplot is looked up in sys.modules rather than imported: importing
    // it here would pull matplotlib into every editor on the site.
    'def _viz_figs():',
    '    plt = sys.modules.get("matplotlib.pyplot")',
    '    if plt is None:',
    '        return []',
    '    out = []',
    '    try:',
    '        import io as _io, base64 as _b64',
    '        for num in plt.get_fignums():',
    '            buf = _io.BytesIO()',
    '            plt.figure(num).savefig(buf, format="png", bbox_inches="tight")',
    '            out.append(_b64.b64encode(buf.getvalue()).decode())',
    '        plt.close("all")',
    '    except BaseException:',
    '        pass',
    '    return out',
    // The prelude is executed once and its namespace reused, rather than
    // re-run on every Run. /fastapi/ pages import fastapi and starlette in
    // theirs, and that first import is slow enough that paying it inside the
    // run budget timed the editor out with "the code probably looped
    // forever" - which was both wrong and unfixable by the reader.
    '_viz_prelude_src = None',
    '_viz_prelude_ns = {}',
    'def _viz_prep(prelude):',
    '    global _viz_prelude_src',
    '    if not prelude or _viz_prelude_src == prelude:',
    '        return',
    '    ns = {"__name__": "__main__"}',
    '    exec(compile(prelude, "<prelude>", "exec"), ns)',
    '    _viz_prelude_ns.clear()',
    '    _viz_prelude_ns.update(ns)',
    '    _viz_prelude_src = prelude',
    'def _viz_run(code, prelude=""):',
    '    g = {"__name__": "__main__"}',
    // The prelude shares the namespace, so what it defines is simply there
    // for the reader's code. Its failure is reported as the page's fault,
    // not theirs: nothing they typed can be the cause.
    '    if prelude:',
    '        try:',
    '            _viz_prep(prelude)',
    '            g.update(_viz_prelude_ns)',
    '        except BaseException:',
    '            sys.stderr.write("The page setup for this editor failed:\\n")',
    '            sys.stderr.write(traceback.format_exc())',
    '            return []',
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
    // A figure drawn before the error is still worth showing.
    '    return _viz_figs()',
  ].join('\n');

  var worker = null;
  var workerReady = null;

  function makeWorker() {
    var wsrc =
      'importScripts("' + PYODIDE_URL + 'pyodide.js");\n' +
      'var py = null;\n' +
      'var loaded = {};\n' +
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
      '    var want = m.packages || [];\n' +
      '    var need = [];\n' +
      '    for (var i = 0; i < want.length; i++) {\n' +
      '      if (!loaded[want[i]]) need.push(want[i]);\n' +
      '    }\n' +
      '    var wheels = m.wheels || [];\n' +
      '    var newWheels = [];\n' +
      '    for (var w = 0; w < wheels.length; w++) {\n' +
      '      if (!loaded[wheels[w]]) newWheels.push(wheels[w]);\n' +
      '    }\n' +
      '    if (need.length || newWheels.length) {\n' +
      '      postMessage({ type: "loading", names: m.label ? [m.label] : need });\n' +
      '    }\n' +
      '    if (newWheels.length) need.push("micropip");\n' +
      '    var prep = need.length ? py.loadPackage(need) : Promise.resolve();\n' +
      '    prep.then(function () {\n' +
      '      if (!newWheels.length) return;\n' +
      // micropip resolves dependencies against what is already installed, so
      // the Pyodide-shipped pydantic has to be in place before this runs -
      // otherwise micropip fetches the newest pydantic from PyPI, whose
      // pydantic-core has no wasm build, and the install dies there.
      '      py.globals.set("__wheels__", newWheels);\n' +
      '      return py.runPythonAsync("import micropip\\nawait micropip.install(list(__wheels__))");\n' +
      '    }).then(function () {\n' +
      '      for (var j = 0; j < need.length; j++) loaded[need[j]] = true;\n' +
      '      for (var k = 0; k < newWheels.length; k++) loaded[newWheels[k]] = true;\n' +
      // Executing the prelude here keeps its cost - which for FastAPI is a
      // multi-second first import - inside the load budget rather than the
      // run one.
      '      if (m.prelude) {\n' +
      '        try { py.globals.set("__prelude__", m.prelude); py.runPython("_viz_prep(__prelude__)"); }\n' +
      '        catch (err) { postMessage({ type: "err", text: String(err) }); }\n' +
      '      }\n' +
      // "loaded" is what starts the run budget on the page. It has to be sent
      // after the wheels are in and before the first line executes, or a slow
      // library download is billed to the run timer and reported as an
      // infinite loop.
      '      postMessage({ type: "loaded" });\n' +
      '      try {\n' +
      '        py.globals.set("__code__", m.code);\n' +
      '        py.globals.set("__prelude__", m.prelude || "");\n' +
      '      }\n' +
      '      catch (err) { postMessage({ type: "err", text: String(err) }); }\n' +
      '      return py.runPythonAsync("_viz_run(__code__, __prelude__)");\n' +
      '    }).then(function (figs) {\n' +
      '      try {\n' +
      '        var arr = (figs && figs.toJs) ? figs.toJs() : figs;\n' +
      '        if (arr) {\n' +
      '          for (var f = 0; f < arr.length; f++) {\n' +
      '            postMessage({ type: "img", data: arr[f] });\n' +
      '          }\n' +
      '        }\n' +
      '        if (figs && figs.destroy) figs.destroy();\n' +
      '      } catch (e) {}\n' +
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

  // Editing keys - Tab, Enter, Cmd+/ - belong to assets/vizlearn-code.js,
  // which owns the editor. This file used to add its own Tab and Enter on the
  // same textarea, so Tab inserted six spaces between them and Enter ran
  // twice. What is left here is running the program, which the editor asks
  // for with a vz-run event.

  function setStatus(block, text) {
    var s = els(block).status;
    if (s) s.textContent = text || '';
  }

  // A drawn figure arrives as base64 PNG and is appended to the same console
  // the prints go to, so output and plot stay in the order they were produced.
  function appendImg(block, b64) {
    var out = els(block).output;
    if (!out) return;
    var img = document.createElement('img');
    img.src = 'data:image/png;base64,' + b64;
    img.alt = 'Figure drawn by this program';
    img.className = 'py-figure';
    img.style.maxWidth = '100%';
    img.style.height = 'auto';
    img.style.display = 'block';
    img.style.margin = '8px 0';
    img.style.background = '#fff';
    img.style.borderRadius = '4px';
    out.appendChild(img);
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

  // One worker serves every block on the page, and it has a single
  // onmessage slot. Starting a second run while one was in flight replaced
  // the first block's handler, so its "done" never arrived: its output
  // stayed empty and its Run button stayed disabled for good. Pages now
  // carry seven to twelve editors, so two clicks in quick succession is
  // ordinary rather than exotic.
  //
  // The Python side was never concurrent anyway - one interpreter, one
  // thread - so runs are queued and played one at a time.
  var queue = Promise.resolve();

  function runBlock(block, code, opts) {
    queue = queue.then(function () { return runBlockNow(block, code, opts); },
                       function () { return runBlockNow(block, code, opts); });
    return queue;
  }

  function runBlockNow(block, code, opts) {
    opts = opts || {};
    var parts = els(block);
    var out = parts.output;
    out.textContent = '';
    parts.run.disabled = true;
    setStatus(block, worker ? 'Running\u2026' : 'Loading Python\u2026');

    var timedOut = false;
    var settle;
    var finished = new Promise(function (r) { settle = r; });

    function giveUp(hint) {
      timedOut = true;
      killWorker();
      appendOut(block, 'Execution timed out', 'py-out-err');
      appendOut(block, hint, 'py-out-hint');
      setStatus(block, 'Timed out');
      parts.run.disabled = false;
      settle();
    }

    var timer = setTimeout(function () {
      giveUp('The interpreter did not finish downloading \u2014 check the connection and try again.');
    }, LOAD_TIMEOUT);

    ensureWorker().then(function () {
      // The timeout may already have fired and terminated the worker while
      // this promise was still pending; `worker` is null in that case.
      if (timedOut || !worker) return;
      // The interpreter is up, but a block that asks for a library still has
      // a download in front of it. The load budget therefore stays in force
      // until the worker reports "loaded", which it sends immediately when
      // there is nothing to fetch.
      clearTimeout(timer);
      timer = setTimeout(function () {
        giveUp('A library did not finish downloading \u2014 check the connection and try again.');
      }, LOAD_TIMEOUT);
      var finish = function () {
        clearTimeout(timer);
        if (timedOut) return;
        setStatus(block, '');
        parts.run.disabled = false;
        settle();
      };
      worker.onmessage = function (e) {
        if (timedOut) return;
        if (e.data.type === 'out') appendOut(block, e.data.text);
        else if (e.data.type === 'img') appendImg(block, e.data.data);
        else if (e.data.type === 'err') appendOut(block, e.data.text, 'py-out-err');
        else if (e.data.type === 'loading') {
          setStatus(block, 'Loading ' + e.data.names.join(', ') + '\u2026');
        } else if (e.data.type === 'loaded') {
          // Everything the code imports is in place; the run's own budget
          // starts here.
          clearTimeout(timer);
          timer = setTimeout(function () {
            giveUp('The interpreter was stopped \u2014 the code probably looped forever.');
          }, RUN_TIMEOUT);
          setStatus(block, 'Running\u2026');
        } else if (e.data.type === 'done') finish();
      };
      worker.onerror = function (e) {
        if (timedOut) return;
        appendOut(block, (e && e.message) || 'worker error', 'py-out-err');
        finish();
      };
      try {
        worker.postMessage({
          type: 'run',
          code: code,
          packages: opts.packages || [],
          wheels: opts.wheels || [],
          prelude: opts.prelude || '',
          label: opts.label || ''
        });
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
      settle();
    });

    return finished;
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

        var list = function (attr) {
          return (block.getAttribute(attr) || '')
            .split(',')
            .map(function (n) { return n.trim(); })
            .filter(function (n) { return n.length > 0; });
        };
        var packages = list('data-vz-packages');
        // The worker lives at a blob: URL, where a relative path resolves
        // against nothing useful. Absolutise against the page instead.
        var wheels = list('data-vz-wheels').map(function (u) {
          return new URL(u, document.baseURI).href;
        });
        var preludeEl = block.querySelector('.py-prelude');
        var prelude = preludeEl ? preludeEl.textContent : '';
        var label = block.getAttribute('data-vz-label') || '';

        var start = function () {
          if (parts.run.disabled) return;
          runBlock(block, parts.editor.value, {
            packages: packages, wheels: wheels, prelude: prelude, label: label
          });
        };
        parts.run.addEventListener('click', start);
        // Shift+Enter, from the editor.
        block.addEventListener('vz-run', start);

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
