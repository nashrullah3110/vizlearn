/* Resizable split for the four labs.
 *
 * The labs used to stack the editor above its output with a help column beside
 * them, which is a document layout wearing an editor's clothes. They are split
 * panes now - code one side, result the other - because that is what every
 * tool people already know looks like, and because on a wide screen the
 * stacked version wasted the entire right half of the page.
 *
 * The divider is a real separator: draggable, focusable, and driven by the
 * arrow keys, since a control you can only operate by dragging is a control
 * some people cannot operate at all. Where the split sits is remembered per
 * lab, so it survives a reload.
 *
 * No dependencies, and nothing here assumes which lab it is running in.
 */
(function () {
  'use strict';

  var MIN = 20;   // percent - below this a pane is too narrow to be useful
  var MAX = 80;
  var STEP = 2;   // percent per arrow press

  function clamp(v) { return Math.max(MIN, Math.min(MAX, v)); }

  function keyFor(ide) {
    return 'vz-split:' + (ide.getAttribute('data-vz-ide') || location.pathname);
  }

  function apply(ide, pct) {
    ide.style.setProperty('--vz-split', pct + '%');
    var sep = ide.querySelector('.vz-ide-split');
    if (sep) sep.setAttribute('aria-valuenow', Math.round(pct));
  }

  function save(ide, pct) {
    try { localStorage.setItem(keyFor(ide), String(Math.round(pct))); } catch (e) {}
  }

  function restore(ide) {
    var pct = 50;
    try {
      var raw = localStorage.getItem(keyFor(ide));
      if (raw !== null && !isNaN(parseFloat(raw))) pct = clamp(parseFloat(raw));
    } catch (e) {}
    apply(ide, pct);
    return pct;
  }

  // Below this width the panes stack, and dragging a vertical divider would
  // move the wrong axis, so the separator is inert.
  function stacked(ide) {
    return window.matchMedia('(max-width: 900px)').matches;
  }

  function wire(ide) {
    var sep = ide.querySelector('.vz-ide-split');
    if (!sep) return;
    var pct = restore(ide);

    function fromPointer(clientX) {
      var r = ide.getBoundingClientRect();
      if (!r.width) return pct;
      return clamp(((clientX - r.left) / r.width) * 100);
    }

    var dragging = false;

    function move(e) {
      if (!dragging) return;
      var x = e.touches ? e.touches[0].clientX : e.clientX;
      pct = fromPointer(x);
      apply(ide, pct);
      // Stops the browser selecting text in the editor while dragging.
      if (e.cancelable) e.preventDefault();
    }

    function stop() {
      if (!dragging) return;
      dragging = false;
      ide.classList.remove('is-dragging');
      document.body.style.userSelect = '';
      save(ide, pct);
    }

    function start(e) {
      if (stacked(ide)) return;
      dragging = true;
      ide.classList.add('is-dragging');
      document.body.style.userSelect = 'none';
      move(e);
    }

    sep.addEventListener('mousedown', start);
    sep.addEventListener('touchstart', start, { passive: false });
    window.addEventListener('mousemove', move);
    window.addEventListener('touchmove', move, { passive: false });
    window.addEventListener('mouseup', stop);
    window.addEventListener('touchend', stop);

    // Keyboard: the separator is the control, so it answers to the arrows.
    sep.addEventListener('keydown', function (e) {
      if (stacked(ide)) return;
      var next = null;
      if (e.key === 'ArrowLeft') next = pct - STEP;
      else if (e.key === 'ArrowRight') next = pct + STEP;
      else if (e.key === 'Home') next = 25;
      else if (e.key === 'End') next = 75;
      else if (e.key === 'Enter' || e.key === ' ') next = 50;
      if (next === null) return;
      e.preventDefault();
      pct = clamp(next);
      apply(ide, pct);
      save(ide, pct);
    });

    // Double-click the divider to go back to even.
    sep.addEventListener('dblclick', function () {
      pct = 50; apply(ide, pct); save(ide, pct);
    });
  }

  function init() {
    var list = document.querySelectorAll('[data-vz-ide]');
    for (var i = 0; i < list.length; i++) wire(list[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
