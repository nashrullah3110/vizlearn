/* In-browser HTML runner for /html-lab/.
 *
 * Your markup is rendered by the browser's own engine - no tooling, no CDN -
 * into a sandboxed <iframe> (`sandbox="allow-scripts"` only), so the preview
 * is fully isolated: it cannot reach the page around it, and it cannot reach
 * the network. console.log from your page's scripts is forwarded to the lab's
 * console panel so you can debug exactly like a real page.
 *
 * Markup the page supplies (one or more per page):
 *
 *   <div class="vz-html" data-vz-html>
 *     <script type="text/plain" class="html-src"><h1>Hi</h1></script>
 *     <textarea class="html-editor" aria-label="HTML code editor"></textarea>
 *     <button type="button" class="html-run-btn">Run</button>
 *     <button type="button" class="html-reset-btn">Reset</button>
 *     <iframe class="html-preview" sandbox="allow-scripts" title="HTML preview"></iframe>
 *     <pre class="html-console" aria-live="polite"></pre>
 *     <span class="html-status"></span>
 *   </div>
 *
 * Nothing here knows which page it is on; it wires every .vz-html block.
 *
 * A short markup fragment (<h1>Hi</h1>) is wrapped into a full document; a
 * complete document (<!DOCTYPE html> ... </html>) is used as-is, with the
 * console forwarder injected at the top of its <head>. Either way every Run
 * writes a fresh srcdoc, so nothing leaks between runs.
 */
(function () {
  'use strict';

  var PROLOGUE = [
    '(function () {',
    '  function fmt(v) {',
    '    if (typeof v === "string") return v;',
    '    if (v instanceof Error) return (v.stack || (v.name + ": " + v.message));',
    '    if (v !== null && typeof v === "object") {',
    '      try { return JSON.stringify(v, null, 2); } catch (e) { return String(v); }',
    '    }',
    '    return String(v);',
    '  }',
    '  function pipe(cls) {',
    '    return function () {',
    '      var parts = [];',
    '      for (var i = 0; i < arguments.length; i++) parts.push(fmt(arguments[i]));',
    '      parent.postMessage({ type: "out", text: parts.join(" "), cls: cls }, "*");',
    '    };',
    '  }',
    '  console.log = pipe("");',
    '  console.info = pipe("");',
    '  console.debug = pipe("");',
    '  console.warn = pipe("warn");',
    '  console.error = pipe("err");',
    '  console.clear = function () { parent.postMessage({ type: "clear" }, "*"); };',
    '  window.onerror = function (msg, src, line) {',
    '    parent.postMessage({ type: "out", text: String(msg) + " (line " + line + ")", cls: "err" }, "*");',
    '  };',
    '})();'
  ].join('\n');

  var SCRIPT = '<script>\n' + PROLOGUE + '\n<\/script>';

  function wrapFragment(code) {
    return '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n' +
      SCRIPT + '\n</head>\n<body>\n' + code + '\n</body>\n</html>';
  }

  function buildDocument(code) {
    var hasDoc = /<!doctype\s+html/i.test(code) || /<html\b/i.test(code);
    if (!hasDoc) return wrapFragment(code);
    var headEnd = /<head\b[^>]*>/i.exec(code);
    if (headEnd) {
      var at = headEnd.index + headEnd[0].length;
      return code.slice(0, at) + '\n' + SCRIPT + code.slice(at);
    }
    // A full document with no <head> tag at all.
    var htmlStart = /<html\b[^>]*>/i.exec(code);
    if (htmlStart) {
      var at2 = htmlStart.index + htmlStart[0].length;
      return code.slice(0, at2) + '\n' + SCRIPT + code.slice(at2);
    }
    var doctype = /<!doctype\s+html[^>]*>/i.exec(code);
    if (doctype) {
      var at3 = doctype.index + doctype[0].length;
      return code.slice(0, at3) + '\n' + SCRIPT + code.slice(at3);
    }
    return SCRIPT + '\n' + code;
  }

  function els(block) {
    return {
      editor: block.querySelector('.html-editor'),
      preview: block.querySelector('.html-preview'),
      console: block.querySelector('.html-console'),
      run: block.querySelector('.html-run-btn'),
      reset: block.querySelector('.html-reset-btn'),
      status: block.querySelector('.html-status'),
      src: block.querySelector('.html-src'),
    };
  }

  function setStatus(block, text) {
    var s = els(block).status;
    if (s) s.textContent = text || '';
  }

  function makePlaceholder() {
    var span = document.createElement('span');
    span.className = 'html-placeholder';
    span.textContent = 'console output from your page appears here.';
    return span;
  }

  function appendOut(block, text, cls) {
    var c = els(block).console;
    if (!c) return;
    var placeholder = c.querySelector('.html-placeholder');
    if (placeholder) placeholder.remove();
    if (cls) {
      var span = document.createElement('span');
      span.className = 'html-out-' + cls;
      span.textContent = text;
      c.appendChild(span);
    } else {
      c.appendChild(document.createTextNode(text));
    }
    if (!text.endsWith('\n')) c.appendChild(document.createTextNode('\n'));
    c.scrollTop = c.scrollHeight;
  }

  function runBlock(block, code) {
    var parts = els(block);
    var doc = buildDocument(code);
    parts.run.disabled = true;
    if (parts.console) {
      parts.console.textContent = '';
      parts.console.appendChild(makePlaceholder());
    }
    setStatus(block, 'Rendering\u2026');

    // Detach the previous frame's message hook (if any) so stale frames can't
    // write into this run's console.
    if (parts.preview._vzOldSource) {
      if (window.removeEventListener) {
        window.removeEventListener('message', parts.preview._vzOldHook);
      }
      parts.preview._vzOldSource = null;
      parts.preview._vzOldHook = null;
    }

    var hook = function (e) {
      if (e.source !== parts.preview.contentWindow) return;
      if (e.data.type === 'clear') {
        parts.console.textContent = '';
        parts.console.appendChild(makePlaceholder());
      } else if (e.data.type === 'out') {
        appendOut(block, e.data.text, e.data.cls || null);
      }
    };
    window.addEventListener('message', hook);
    parts.preview._vzOldSource = parts.preview;
    parts.preview._vzOldHook = hook;

    try {
      parts.preview.srcdoc = doc;
    } catch (err) {
      appendOut(block, String(err), 'err');
    }
    setStatus(block, '');
    parts.run.disabled = false;
  }


  function srcText(block) {
    var s = els(block).src;
    if (!s) return '';
    return (s.textContent || '').replace(/^\n+|\s+$/g, '')
                                 .replace(/<\\\/script>/g, '</script>');
  }

  function init() {
    var blocks = document.querySelectorAll('.vz-html');
    for (var i = 0; i < blocks.length; i++) {
      (function (block) {
        var parts = els(block);
        if (!parts.editor || !parts.run) return;
        if (parts.src) {
          parts.editor.value = srcText(block);
        }

        var start = function () {
          if (parts.run.disabled) return;
          runBlock(block, parts.editor.value);
        };
        parts.run.addEventListener('click', start);
        block.addEventListener('vz-run', start);   // Shift+Enter

        if (parts.reset) parts.reset.addEventListener('click', function () {
          if (parts.src) parts.editor.value = srcText(block);
          parts.run.disabled = false;
          setStatus(block, '');
        });

        // Render once on load so the preview is never empty.
        runBlock(block, parts.editor.value);
      })(blocks[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
