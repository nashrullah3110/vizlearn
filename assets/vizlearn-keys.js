/* Keyboard access for the visualisations.
 *
 * Every module is driven by dragging something, and until now that was the
 * only way in: measured across the site, the viz layer had no tabindex and no
 * keydown handling anywhere. The sliders beside each visualisation were always
 * keyboard-operable - they are native range inputs - but nothing said so, and
 * the drag surfaces themselves were unreachable.
 *
 * This makes the visualisation a focus stop and wires the arrow keys to the
 * page's own controls, which the build picked out and wrote into #vz-lab-data.
 * It drives the real inputs and fires their real events, so a page needs to
 * know nothing about this file: whatever a mouse could do to that slider, a
 * keyboard now does identically.
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
   * be announced. Handles both a range and a select, because half the site's
   * visualisations are driven by a select rather than a slider. Returns null
   * when the control has gone from the page. */
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

    var step = target.step || parseFloat(el.step) || 1;
    var min = target.min !== undefined ? target.min : parseFloat(el.min);
    var max = target.max !== undefined ? target.max : parseFloat(el.max);
    var cur = parseFloat(el.value);
    if (isNaN(cur)) return null;

    var next = cur + steps * step;
    if (!isNaN(min)) next = Math.max(min, next);
    if (!isNaN(max)) next = Math.min(max, next);
    next = parseFloat(next.toFixed(decimals(step) + 2));
    if (next === cur) return { label: target.label, value: el.value, edge: true };

    el.value = next;
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
    var min = target.min !== undefined ? target.min : parseFloat(el.min);
    var max = target.max !== undefined ? target.max : parseFloat(el.max);
    el.value = toEnd ? max : min;
    fire(el);
    return { label: target.label, value: el.value, edge: false };
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

  function init() {
    var cfg = config();
    if (!cfg || !cfg.keys || !cfg.keys.primary) return;
    var viz = (cfg.viz && document.getElementById(cfg.viz)) || vizFallback();
    if (!viz) return;
    if (!document.getElementById(cfg.keys.primary.id)) return;

    var primary = cfg.keys.primary;
    var secondary = cfg.keys.secondary &&
        document.getElementById(cfg.keys.secondary.id) ? cfg.keys.secondary : null;

    /* --- make it reachable ------------------------------------------------
     *
     * The focus stop is the element wrapping the picture rather than the
     * picture itself. An <svg> with a tabindex is focusable but does not
     * reliably dispatch focus events - programmatic focus moves
     * document.activeElement and fires nothing at all - so the hint would
     * never appear. An HTML wrapper behaves the way the spec suggests
     * everywhere, and a focus ring around the frame is what a reader wants
     * to see anyway. */
    var host = (viz instanceof HTMLElement) ? viz : viz.parentElement;
    if (!host) return;

    host.setAttribute('tabindex', '0');
    host.classList.add('vz-focusable');
    if (!viz.getAttribute('role')) viz.setAttribute('role', 'img');
    var label = viz.getAttribute('aria-label');
    if (label && !host.getAttribute('aria-label')) {
      host.setAttribute('role', 'group');
      host.setAttribute('aria-label', label + ' — interactive, use the arrow keys');
    }

    var hint = document.createElement('p');
    hint.className = 'vz-keyhint';
    hint.id = 'vz-keyhint';
    hint.hidden = true;
    hint.innerHTML = '<kbd>&larr;</kbd><kbd>&rarr;</kbd> ' + primary.label +
      (secondary ? ' &nbsp;<kbd>&uarr;</kbd><kbd>&darr;</kbd> ' + secondary.label : '') +
      ' &nbsp;<kbd>Home</kbd><kbd>End</kbd> ends &nbsp;<kbd>Shift</kbd> ten at a time';
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
        case 'ArrowRight': res = nudge(primary, big); break;
        case 'ArrowLeft': res = nudge(primary, -big); break;
        case 'ArrowUp': res = secondary ? nudge(secondary, big) : nudge(primary, big); break;
        case 'ArrowDown': res = secondary ? nudge(secondary, -big) : nudge(primary, -big); break;
        case 'Home': res = jump(primary, false); break;
        case 'End': res = jump(primary, true); break;
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
