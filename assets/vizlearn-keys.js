/* Keyboard access for the visualisations.
 *
 * Every module is driven by dragging or clicking something, and until this
 * shipped that was the only way in: measured across the site, the viz layer
 * had no tabindex and no keydown handling anywhere. The sliders beside each
 * visualisation were always keyboard-operable - they are native range inputs -
 * but nothing said so, and the drag surfaces themselves were unreachable.
 *
 * This makes the visualisation a focus stop and wires the keyboard to the
 * page's own controls, which the build picked out and wrote into #vz-lab-data.
 * It drives the real inputs and fires their real events, so a page needs to
 * know nothing about this file: whatever a mouse could do to that control, a
 * keyboard now does identically.
 *
 * Three kinds of route in, in order of preference:
 *
 *   primary/secondary  an axis to nudge - a range, a number, a select, or a
 *                      checkbox. Arrow keys move it.
 *   actions            a list of buttons to step through and press, for the
 *                      31 pages that are driven purely by clicking.
 *   runtime fallback   the same, but discovered from the live DOM, because a
 *                      few pages build their controls in JS and no build-time
 *                      scan of the HTML can ever see them.
 */
(function () {
  'use strict';

  function config() {
    var el = document.getElementById('vz-lab-data');
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (e) { return null; }
  }

  function fire(el) {
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }

  function decimals(step) {
    var s = String(step);
    var dot = s.indexOf('.');
    return dot === -1 ? 0 : s.length - dot - 1;
  }

  /* Nudge a control by n steps and report what it became, so the change can
   * be announced. Handles a range, a number, a select and a checkbox, because
   * between them they are every axis the site has. Returns null when the
   * control has gone from the page. */
  function nudge(target, steps) {
    var el = document.getElementById(target.id);
    if (!el) return null;

    if (el.tagName === 'SELECT') {
      var want = Math.max(0, Math.min(el.options.length - 1,
                                      el.selectedIndex + (steps > 0 ? 1 : -1)));
      if (want === el.selectedIndex) {
        return { label: target.label, value: el.options[el.selectedIndex].text, edge: true };
      }
      el.selectedIndex = want;
      fire(el);
      return { label: target.label, value: el.options[want].text, edge: false };
    }

    if (el.type === 'checkbox') {
      // Right/up turns it on, left/down turns it off. Predictable in a way
      // that "both arrows toggle" is not.
      var next = steps > 0;
      if (el.checked === next) {
        return { label: target.label, value: el.checked ? 'on' : 'off', edge: true };
      }
      el.checked = next;
      fire(el);
      el.dispatchEvent(new Event('click', { bubbles: true }));
      return { label: target.label, value: el.checked ? 'on' : 'off', edge: false };
    }

    var step = target.step || parseFloat(el.step) || 1;
    var min = target.min !== undefined ? target.min : parseFloat(el.min);
    var max = target.max !== undefined ? target.max : parseFloat(el.max);
    var cur = parseFloat(el.value);
    if (isNaN(cur)) return null;

    var nextVal = cur + steps * step;
    if (!isNaN(min)) nextVal = Math.max(min, nextVal);
    if (!isNaN(max)) nextVal = Math.min(max, nextVal);
    nextVal = parseFloat(nextVal.toFixed(decimals(step) + 2));
    if (nextVal === cur) return { label: target.label, value: el.value, edge: true };

    el.value = nextVal;
    fire(el);
    return { label: target.label, value: el.value, edge: false };
  }

  function jump(target, toEnd) {
    var el = document.getElementById(target.id);
    if (!el) return null;

    if (el.tagName === 'SELECT') {
      el.selectedIndex = toEnd ? el.options.length - 1 : 0;
      fire(el);
      return { label: target.label, value: el.options[el.selectedIndex].text, edge: false };
    }
    if (el.type === 'checkbox') return nudge(target, toEnd ? 1 : -1);

    var min = target.min !== undefined ? target.min : parseFloat(el.min);
    var max = target.max !== undefined ? target.max : parseFloat(el.max);
    el.value = toEnd ? max : min;
    fire(el);
    return { label: target.label, value: el.value, edge: false };
  }

  /* --- actions ------------------------------------------------------------
   *
   * Resolved lazily, on the first key press rather than at load. A handful of
   * pages render their buttons from JS after this file has already run, and a
   * list captured at load time would be permanently empty on exactly those
   * pages. Asking the DOM at the moment of the keypress is always right.
   */

  var SKIP = /(^|\s)(vz-|adsbygoogle)/;

  function labelOf(el) {
    var t = (el.textContent || '').replace(/\s+/g, ' ').trim();
    return t || el.getAttribute('aria-label') || 'Button';
  }

  function usable(el) {
    if (el.disabled) return false;
    if (SKIP.test(el.className || '')) return false;
    if (el.id === 'themeToggle') return false;
    if (el.closest('header, footer, .vz-share-wrap, .vz-lab')) return false;
    return el.offsetParent !== null;  // visible
  }

  function resolveActions(cfg) {
    var out = [];

    (cfg.keys.actions || []).forEach(function (a) {
      var els;
      try { els = document.querySelectorAll(a.sel); } catch (e) { return; }
      var el = els[a.i || 0];
      if (el && usable(el)) out.push({ el: el, label: a.label });
    });
    if (out.length) return out;

    // Nothing declared, or everything declared has gone: read the live DOM.
    //
    // Scanned document-wide rather than within the visualisation column,
    // because the column is not reliably where the controls are: on
    // datatypes_in_sql the twelve type buttons sit in <main> but outside the
    // [data-vz-viz] section, and scoping to that section found nothing at
    // all. usable() already rejects everything that is site furniture, so
    // the wider net costs nothing.
    var seen = 0;
    Array.prototype.forEach.call(document.querySelectorAll('button'), function (el) {
      if (seen >= 8 || !usable(el)) return;
      out.push({ el: el, label: labelOf(el) });
      seen++;
    });
    return out;
  }

  /* Pages whose visualisation is a div of cards or a table have no svg or
   * canvas for the build to name, but build_responsive tags every
   * visualisation column with data-vz-viz. Prefer something inside it that is
   * actually the picture; fall back to the column itself. */
  function vizFallback() {
    var col = document.querySelector('[data-vz-viz]');
    if (!col) return null;
    return col.querySelector('svg, canvas, table') || col;
  }

  var retried = false;

  function init() {
    var cfg = config();
    if (!cfg || !cfg.keys) return;

    var primary = cfg.keys.primary &&
        document.getElementById(cfg.keys.primary.id) ? cfg.keys.primary : null;
    var secondary = cfg.keys.secondary &&
        document.getElementById(cfg.keys.secondary.id) ? cfg.keys.secondary : null;
    var hasActions = !!(cfg.keys.actions && cfg.keys.actions.length);

    // Nothing declared. Three pages render their controls from JS, so there
    // was no markup for the build to scan and the declaration is empty on
    // exactly the pages that most need one. Give the page a macrotask to
    // draw itself, then ask the live DOM before concluding it is static -
    // and if it really is static, leave it alone. A focus stop that swallows
    // arrow keys and does nothing is worse than no focus stop.
    if (!primary && !hasActions) {
      if (!retried) { retried = true; setTimeout(init, 0); return; }
      if (!resolveActions(cfg).length) return;
      // Discovered rather than declared, but just as real - and the hint has
      // to say so, or the page offers keys it never mentions.
      hasActions = true;
    }

    var viz = (cfg.viz && document.getElementById(cfg.viz)) || vizFallback();
    if (!viz) return;

    /* --- make it reachable ------------------------------------------------
     *
     * The focus stop is the element wrapping the picture rather than the
     * picture itself. An <svg> with a tabindex is focusable but does not
     * reliably dispatch focus events - programmatic focus moves
     * document.activeElement and fires nothing at all - so the hint would
     * never appear. An HTML wrapper behaves the way the spec suggests
     * everywhere, and a focus ring around the frame is what a reader wants
     * to see anyway.
     *
     * A <canvas> has to be treated the same way even though it is an
     * HTMLElement. Its children are fallback content: a browser that can
     * paint a canvas never paints them, so a hint appended to one measures
     * 0x0 and no sighted keyboard user ever sees it. That was true of every
     * canvas-driven module on the site until this line grew its second
     * condition.
     *
     * A <table> is on the list for the same reason from the other direction:
     * a <p> appended to one is invalid HTML, and the parser foster-parents it
     * somewhere unpredictable. */
    var REPLACED =
        /^(CANVAS|IMG|VIDEO|OBJECT|EMBED|IFRAME|INPUT|TEXTAREA|SELECT|TABLE|THEAD|TBODY|TR)$/;
    var host = (viz instanceof HTMLElement) && !REPLACED.test(viz.tagName)
        ? viz : viz.parentElement;
    if (!host) return;

    host.setAttribute('tabindex', '0');
    host.classList.add('vz-focusable');
    if (!viz.getAttribute('role')) viz.setAttribute('role', 'img');
    var label = viz.getAttribute('aria-label');
    if (label && !host.getAttribute('aria-label')) {
      host.setAttribute('role', 'group');
      host.setAttribute('aria-label', label + ' — interactive, use the arrow keys');
    }

    // Which keys do what depends on what this page actually has, so the hint
    // is assembled rather than fixed.
    var bits = [];
    if (primary) bits.push('<kbd>&larr;</kbd><kbd>&rarr;</kbd> ' + primary.label);
    if (secondary) bits.push('<kbd>&uarr;</kbd><kbd>&darr;</kbd> ' + secondary.label);
    else if (hasActions && primary) bits.push('<kbd>Enter</kbd> run');
    else if (hasActions) bits.push('<kbd>&larr;</kbd><kbd>&rarr;</kbd> pick &nbsp;<kbd>Enter</kbd> run');
    if (primary) bits.push('<kbd>Home</kbd><kbd>End</kbd> ends');
    if (primary && primary.kind !== 'select' && primary.kind !== 'checkbox') {
      bits.push('<kbd>Shift</kbd> ten at a time');
    }

    var hint = document.createElement('p');
    hint.className = 'vz-keyhint';
    hint.id = 'vz-keyhint';
    hint.hidden = true;
    hint.innerHTML = bits.join(' &nbsp;');
    host.appendChild(hint);

    // Screen readers get the change spoken; sighted keyboard users see it in
    // the same line. One element, so the two can never disagree.
    var live = document.createElement('p');
    live.className = 'vz-keylive';
    live.setAttribute('aria-live', 'polite');
    live.hidden = true;
    host.appendChild(live);

    host.setAttribute('aria-describedby', 'vz-keyhint');

    function announce(res) {
      if (!res) return;
      live.hidden = false;
      live.textContent = res.label + ': ' + res.value + (res.edge ? ' (end of range)' : '');
    }

    var cursor = 0;

    function moveCursor(delta) {
      var acts = resolveActions(cfg);
      if (!acts.length) return null;
      cursor = (cursor + delta + acts.length) % acts.length;
      return { label: 'Selected', value: acts[cursor].label, edge: false };
    }

    function press() {
      var acts = resolveActions(cfg);
      if (!acts.length) return null;
      if (cursor >= acts.length) cursor = 0;
      acts[cursor].el.click();
      return { label: 'Ran', value: acts[cursor].label, edge: false };
    }

    // focusin/focusout rather than focus/blur: an <svg> is not a form control
    // and the non-bubbling pair is unreliable on one across browsers.
    host.addEventListener('focusin', function () { hint.hidden = false; });
    host.addEventListener('focus', function () { hint.hidden = false; });
    host.addEventListener('focusout', function () {
      hint.hidden = true;
      live.hidden = true;
    });
    host.addEventListener('blur', function () {
      hint.hidden = true;
      live.hidden = true;
    });

    host.addEventListener('keydown', function (e) {
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      // Belt and braces: a browser that has not delivered a focus event -
      // a background window is enough - should still show the hint the
      // moment a key is pressed.
      hint.hidden = false;
      var big = e.shiftKey ? 10 : 1;
      var res = null;

      switch (e.key) {
        case 'ArrowRight':
          res = primary ? nudge(primary, big) : moveCursor(1);
          break;
        case 'ArrowLeft':
          res = primary ? nudge(primary, -big) : moveCursor(-1);
          break;
        case 'ArrowUp':
          res = secondary ? nudge(secondary, big)
              : (primary ? nudge(primary, big) : moveCursor(-1));
          break;
        case 'ArrowDown':
          res = secondary ? nudge(secondary, -big)
              : (primary ? nudge(primary, -big) : moveCursor(1));
          break;
        case 'Home': res = primary ? jump(primary, false) : moveCursor(-1); break;
        case 'End': res = primary ? jump(primary, true) : moveCursor(1); break;
        case 'Enter':
        case ' ':
          res = press();
          if (!res) return;
          break;
        case 'Escape': host.blur(); return;
        default: return;
      }

      e.preventDefault();
      announce(res);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
