/* In-browser notebook for /notebook/.
 *
 * The labs run one program in a fresh namespace every time. A notebook is the
 * opposite: many small cells sharing one kernel, where cell 4 depends on the
 * name cell 2 bound. That difference goes all the way down, so this does not
 * reuse assets/vizlearn-python.js - it keeps its own worker whose globals
 * persist for the life of the page, and it renders output that is not text:
 * figures as images, DataFrames as tables.
 *
 * Markup the page supplies:
 *
 *   <div class="vz-nb" data-vz-nb data-vz-packages="numpy,pandas,matplotlib">
 *     <template class="vz-nb-template"> ...one cell's markup... </template>
 *     <div class="vz-nb-cells"> ...starter cells, same shape... </div>
 *     <button class="vz-nb-add">, <button class="vz-nb-runall">,
 *     <button class="vz-nb-restart">, <span class="vz-nb-status">
 *   </div>
 *
 * Each cell is
 *
 *   <div class="vz-nb-cell">
 *     <script type="text/plain" class="vz-nb-src">...</script>
 *     <div class="vz-code" data-vz-code="python"> ...textarea.vz-nb-input... </div>
 *     <button class="vz-nb-run">, <button class="vz-nb-del">
 *     <div class="vz-nb-out"></div>
 *   </div>
 */
(function () {
  'use strict';

  var PYODIDE_VERSION = '0.26.4';
  var PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v' + PYODIDE_VERSION + '/full/';
  var LOAD_TIMEOUT = 120000;   // numpy + pandas + matplotlib is a big download
  var RUN_TIMEOUT = 30000;     // a real computation is allowed longer than a lesson

  /* The kernel.
   *
   * Three things here are what make it feel like a notebook rather than a
   * series of scripts:
   *
   *   _ns kept at module level  - the namespace outlives the cell, so a name
   *                               bound in one cell is there in the next. It
   *                               is only rebuilt by Restart.
   *
   *   the trailing expression   - a cell ending in an expression shows its
   *                               value without print(), which is the single
   *                               most notebook-ish behaviour there is. The
   *                               statements before it are exec'd, and only
   *                               the last one is eval'd.
   *
   *   _figures()                - there is no DOM in a worker, so matplotlib
   *                               runs headless and every open figure is
   *                               drawn to PNG after the cell finishes, then
   *                               closed so the next cell starts clean.
   */
  var KERNEL_SRC = [
    'import ast, sys, io, base64, json, traceback, warnings',
    '',
    '_ns = {"__name__": "__main__"}',
    '',
    'def _reset():',
    '    global _ns',
    '    _ns = {"__name__": "__main__"}',
    '',
    'def _figures():',
    '    out = []',
    '    mod = sys.modules.get("matplotlib.pyplot")',
    '    if mod is None:',
    '        return out',
    '    for num in mod.get_fignums():',
    '        fig = mod.figure(num)',
    '        buf = io.BytesIO()',
    '        try:',
    '            fig.savefig(buf, format="png", dpi=110, bbox_inches="tight")',
    '        except Exception:',
    '            continue',
    '        out.append(base64.b64encode(buf.getvalue()).decode("ascii"))',
    '    mod.close("all")',
    '    return out',
    '',
    'def _show(value):',
    '    if value is None:',
    '        return None',
    // A DataFrame knows how to draw itself; anything else falls back to repr,
    // which is what the REPL would have shown.
    '    html = getattr(value, "_repr_html_", None)',
    '    if callable(html):',
    '        try:',
    '            return {"kind": "html", "data": html()}',
    '        except Exception:',
    '            pass',
    '    try:',
    '        return {"kind": "text", "data": repr(value)}',
    '    except Exception as e:',
    '        return {"kind": "text", "data": "<unprintable: %s>" % e}',
    '',
    'def _viz_cell(code):',
    '    result = None',
    '    try:',
    '        tree = ast.parse(code, "<cell>", "exec")',
    '        body = tree.body',
    '        tail = None',
    '        if body and isinstance(body[-1], ast.Expr):',
    '            tail = body.pop()',
    '        if body:',
    '            exec(compile(ast.Module(body=body, type_ignores=[]), "<cell>", "exec"), _ns)',
    '        if tail is not None:',
    '            val = eval(compile(ast.Expression(tail.value), "<cell>", "eval"), _ns)',
    '            result = _show(val)',
    '    except SyntaxError as e:',
    '        sys.stderr.write("SyntaxError: %s (line %s)\\n" % (e.msg, e.lineno))',
    // Same trim as the labs: without it every error opens with five frames of
    // interpreter internals above the one line the reader wrote.
    '    except BaseException as e:',
    '        tb = e.__traceback__',
    '        while tb is not None and tb.tb_frame.f_code.co_filename != "<cell>":',
    '            tb = tb.tb_next',
    '        sys.stderr.write("".join(traceback.format_exception(type(e), e, tb)))',
    '    return json.dumps({"result": result, "figures": _figures()})',
  ].join('\n');

  /* Two warnings that are not the reader's problem and read as errors.
   *
   * pandas prints a DeprecationWarning about pyarrow on first import, which
   * is nine lines of red before the first cell has done anything. And every
   * notebook ends a plot with plt.show(), which on a headless backend warns
   * that it cannot show anything - while the figure is captured and displayed
   * regardless. Silencing show() is a lie only if the figure fails to appear,
   * and it does appear.
   */
  var QUIET_SRC = [
    'import warnings',
    'warnings.filterwarnings("ignore", category=DeprecationWarning)',
    'warnings.filterwarnings("ignore", message=".*non-GUI backend.*")',
    'import matplotlib.pyplot as _plt',
    '_plt.show = lambda *a, **k: None',
  ].join('\n');

  var worker = null;
  var workerReady = null;
  var packages = [];
  var busy = false;

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
      '      postMessage({ type: "loading", names: m.packages });\n' +
      '      return py.loadPackage(m.packages).then(function () {\n' +
      // matplotlib's default Pyodide backend draws into a canvas on the page.
      // There is no page here, so it has to be told to render headless before
      // pyplot is imported for the first time - after that the choice sticks.
      '        return py.runPythonAsync("import os\\nos.environ[\'MPLBACKEND\'] = \'Agg\'\\nimport matplotlib\\nmatplotlib.use(\'Agg\')");\n' +
      '      }).then(function () {\n' +
      '        py.runPython(' + JSON.stringify(KERNEL_SRC) + ');\n' +
      '        py.runPython(' + JSON.stringify(QUIET_SRC) + ');\n' +
      '        postMessage({ type: "ready" });\n' +
      '      });\n' +
      '    }).catch(function (err) { postMessage({ type: "fatal", text: String(err) }); });\n' +
      '  } else if (m.type === "run") {\n' +
      '    try { py.globals.set("__cell__", m.code); }\n' +
      '    catch (err) { postMessage({ type: "err", text: String(err) }); }\n' +
      '    py.runPythonAsync("_viz_cell(__cell__)").then(function (out) {\n' +
      '      postMessage({ type: "cell", payload: out });\n' +
      '    }, function (err) {\n' +
      '      postMessage({ type: "err", text: (err && err.message) || String(err) });\n' +
      '      postMessage({ type: "cell", payload: "{}" });\n' +
      '    });\n' +
      '  } else if (m.type === "reset") {\n' +
      '    try { py.runPython("_reset()"); } catch (err) {}\n' +
      '    postMessage({ type: "reset-done" });\n' +
      '  }\n' +
      '};\n';
    var blob = new Blob([wsrc], { type: 'application/javascript' });
    var url = URL.createObjectURL(blob);
    var w = new Worker(url);
    URL.revokeObjectURL(url);
    return w;
  }

  function ensureWorker(nb) {
    if (worker) return workerReady;
    worker = makeWorker();
    workerReady = new Promise(function (resolve, reject) {
      var settled = false;
      worker.onmessage = function (e) {
        if (e.data.type === 'ready') { settled = true; resolve(); }
        else if (e.data.type === 'loading') {
          setStatus(nb, 'Loading ' + e.data.names.join(', ') + '…');
        } else if (e.data.type === 'fatal') {
          settled = true; reject(new Error(e.data.text));
        }
      };
      worker.onerror = function (e) {
        if (!settled) { settled = true; reject(new Error(e.message || 'worker failed')); }
      };
      worker.postMessage({ type: 'init', packages: packages });
    });
    workerReady.catch(function () { killWorker(); });
    return workerReady;
  }

  function killWorker() {
    if (worker) { worker.terminate(); worker = null; workerReady = null; }
  }

  function setStatus(nb, text) {
    var s = nb.querySelector('.vz-nb-status');
    if (s) s.textContent = text || '';
  }

  // ---------------------------------------------------------------- output

  function outEl(cell) { return cell.querySelector('.vz-nb-out'); }

  function clearOut(cell) {
    var o = outEl(cell);
    o.textContent = '';
    o.classList.remove('is-filled');
  }

  function addText(cell, text, cls) {
    var o = outEl(cell);
    var pre = o.querySelector('pre.' + (cls || 'vz-nb-stdout'));
    if (!pre) {
      pre = document.createElement('pre');
      pre.className = cls || 'vz-nb-stdout';
      o.appendChild(pre);
    }
    pre.appendChild(document.createTextNode(text.endsWith('\n') ? text : text + '\n'));
    o.classList.add('is-filled');
  }

  function addImage(cell, b64) {
    var img = document.createElement('img');
    img.className = 'vz-nb-fig';
    img.alt = 'Figure produced by this cell';
    img.src = 'data:image/png;base64,' + b64;
    outEl(cell).appendChild(img);
    outEl(cell).classList.add('is-filled');
  }

  function addResult(cell, result) {
    if (!result) return;
    var o = outEl(cell);
    if (result.kind === 'html') {
      var box = document.createElement('div');
      box.className = 'vz-nb-table';
      // Pandas writes its own table markup. It is generated here in this tab
      // from data this tab already holds, so there is no foreign HTML in it.
      box.innerHTML = result.data;
      // It also ships a <style> block scoped to .dataframe, which would apply
      // to every table on the page and lands in the cell's text as CSS source.
      // The look comes from this page's own rules, so drop it.
      box.querySelectorAll('style').forEach(function (el) { el.remove(); });
      o.appendChild(box);
    } else {
      addText(cell, result.data, 'vz-nb-value');
    }
    o.classList.add('is-filled');
  }

  // ------------------------------------------------------------- execution

  function runCell(nb, cell) {
    if (busy) return Promise.resolve();
    var input = cell.querySelector('.vz-nb-input');
    var code = input ? input.value : '';
    if (!code.trim()) { clearOut(cell); return Promise.resolve(); }

    busy = true;
    clearOut(cell);
    cell.classList.add('is-running');
    setCount(cell, '*');
    setStatus(nb, worker ? 'Running…' : 'Starting Python…');

    return new Promise(function (resolve) {
      var timedOut = false;
      var timer = setTimeout(function () {
        timedOut = true;
        killWorker();
        addText(cell, 'Stopped: this cell ran too long, or the kernel is still ' +
                      'downloading. The kernel has been restarted, so names from ' +
                      'earlier cells are gone.', 'vz-nb-stderr');
        finish();
      }, LOAD_TIMEOUT);

      function finish() {
        clearTimeout(timer);
        cell.classList.remove('is-running');
        busy = false;
        setStatus(nb, '');
        resolve();
      }

      ensureWorker(nb).then(function () {
        if (timedOut || !worker) return;
        clearTimeout(timer);
        timer = setTimeout(function () {
          timedOut = true;
          killWorker();
          addText(cell, 'Stopped after ' + (RUN_TIMEOUT / 1000) + ' seconds. The ' +
                        'kernel has been restarted, so names from earlier cells ' +
                        'are gone.', 'vz-nb-stderr');
          finish();
        }, RUN_TIMEOUT);
        setStatus(nb, 'Running…');

        worker.onmessage = function (e) {
          if (timedOut) return;
          var m = e.data;
          if (m.type === 'out') addText(cell, m.text);
          else if (m.type === 'err') addText(cell, m.text, 'vz-nb-stderr');
          else if (m.type === 'cell') {
            var payload = {};
            try { payload = JSON.parse(m.payload || '{}'); } catch (err) {}
            (payload.figures || []).forEach(function (b64) { addImage(cell, b64); });
            addResult(cell, payload.result);
            setCount(cell, String(nextCount(nb)));
            finish();
          }
        };
        worker.onerror = function () {
          if (timedOut) return;
          addText(cell, 'The kernel stopped unexpectedly.', 'vz-nb-stderr');
          finish();
        };
        worker.postMessage({ type: 'run', code: code });
      }).catch(function (err) {
        clearTimeout(timer);
        addText(cell, 'Could not start Python: ' + (err.message || err), 'vz-nb-stderr');
        addText(cell, 'Check the connection and try again.', 'vz-nb-stderr');
        finish();
      });
    });
  }

  var counter = 0;
  function nextCount() { return ++counter; }
  function setCount(cell, text) {
    var el = cell.querySelector('.vz-nb-count');
    if (el) el.textContent = '[' + text + ']';
  }

  function runAll(nb) {
    var cells = Array.prototype.slice.call(nb.querySelectorAll('.vz-nb-cell'));
    // Sequential on purpose: a notebook's cells are ordered, and running them
    // in parallel against one namespace would race.
    return cells.reduce(function (chain, cell) {
      return chain.then(function () { return runCell(nb, cell); });
    }, Promise.resolve());
  }

  function restart(nb) {
    counter = 0;
    nb.querySelectorAll('.vz-nb-cell').forEach(function (cell) {
      clearOut(cell);
      setCount(cell, ' ');
    });
    if (!worker) { setStatus(nb, 'Kernel is empty'); return; }
    worker.onmessage = function (e) {
      if (e.data.type === 'reset-done') setStatus(nb, 'Kernel restarted');
    };
    worker.postMessage({ type: 'reset' });
  }

  // ------------------------------------------------------------------- UI

  function wireCell(nb, cell) {
    var src = cell.querySelector('.vz-nb-src');
    var input = cell.querySelector('.vz-nb-input');
    if (input && src) input.value = (src.textContent || '').replace(/^\n+|\s+$/g, '');

    if (input) {
      // Shift+Enter is handled by assets/vizlearn-code.js, which owns the
      // editor and dispatches vz-run. Listening for the key here as well
      // meant two handlers on one textarea and the cell running twice.
      cell.addEventListener('vz-run', function () { runCell(nb, cell); });
      autoGrow(input);
    }

    var run = cell.querySelector('.vz-nb-run');
    if (run) run.addEventListener('click', function () { runCell(nb, cell); });

    var del = cell.querySelector('.vz-nb-del');
    if (del) del.addEventListener('click', function () {
      if (nb.querySelectorAll('.vz-nb-cell').length <= 1) return;
      cell.remove();
    });

    var code = cell.querySelector('[data-vz-code]');
    if (code && typeof window.vzAttachCode === 'function') window.vzAttachCode(code);
  }

  // The editor is a textarea, and a notebook cell should be as tall as what it
  // holds rather than a fixed box with its own scrollbar.
  function autoGrow(input) {
    var grow = function () {
      input.style.height = 'auto';
      input.style.height = Math.max(input.scrollHeight, 44) + 'px';
    };
    input.addEventListener('input', grow);
    setTimeout(grow, 0);
  }

  function addCell(nb, code) {
    var tpl = nb.querySelector('.vz-nb-template');
    if (!tpl) return null;
    var frag = tpl.content.cloneNode(true);
    var cell = frag.querySelector('.vz-nb-cell');
    nb.querySelector('.vz-nb-cells').appendChild(frag);
    if (code) {
      var input = cell.querySelector('.vz-nb-input');
      if (input) input.value = code;
    }
    wireCell(nb, cell);
    var input2 = cell.querySelector('.vz-nb-input');
    if (input2) input2.focus();
    return cell;
  }

  function init() {
    var nb = document.querySelector('.vz-nb');
    if (!nb) return;

    packages = (nb.getAttribute('data-vz-packages') || '')
      .split(',')
      .map(function (n) { return n.trim(); })
      .filter(function (n) { return n.length > 0; });

    nb.querySelectorAll('.vz-nb-cell').forEach(function (cell) { wireCell(nb, cell); });

    var add = nb.querySelector('.vz-nb-add');
    if (add) add.addEventListener('click', function () { addCell(nb); });

    var all = nb.querySelector('.vz-nb-runall');
    if (all) all.addEventListener('click', function () { runAll(nb); });

    var res = nb.querySelector('.vz-nb-restart');
    if (res) res.addEventListener('click', function () { restart(nb); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
