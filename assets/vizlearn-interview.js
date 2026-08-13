/* The step-through visualisation on every /interview/ page.
 *
 * The rest of the site hand-builds a visualisation per module, which is right
 * when there are forty of them and each shows a different mechanism. This
 * track has around a hundred pages and most of them show the same half-dozen
 * shapes: a row of cells with pointers moving over it, a string being scanned,
 * a dictionary filling up, two columns of counters diverging. So there is one
 * player here and the pages supply frames.
 *
 * A frame is a snapshot, not a diff. That is deliberate: the generator
 * produces frames by running the real algorithm and recording its state
 * (tools/interview_viz.py), so what is drawn cannot drift from what the
 * editor below it computes. Nothing is animated between frames - the reader
 * steps, and each step is a state the algorithm genuinely passed through.
 *
 * Markup the page supplies:
 *
 *   <div class="vz-iv" data-vz-iv>
 *     <script type="application/json" class="vz-iv-data">{ ... }</script>
 *     <div class="vz-iv-stage"></div>
 *     <div class="vz-iv-caption"></div>
 *     ... controls with .vz-iv-step / .vz-iv-back / .vz-iv-play / .vz-iv-reset
 *     <input class="vz-iv-scrub" type="range">
 *   </div>
 *
 * The data:
 *
 *   { "title": "...", "readouts": ["i", "j"], "frames": [ frame, ... ] }
 *
 *   frame = {
 *     "rows":  [ { "label": "a", "kind": "cells"|"text"|"pairs",
 *                  "items": [ { "v": "12", "k": "lo"|"hi"|"hit"|"done"|"dim",
 *                               "tag": "i=3" } ] } ],
 *     "note":  "what just happened",
 *     "read":  { "i": "3", "j": "7" }
 *   }
 *
 * Every field except `items` is optional, so a page that only wants a row of
 * numbers supplies a row of numbers.
 */
(function () {
  'use strict';

  var STEP_MS = 700;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function parse(block) {
    var tag = block.querySelector('.vz-iv-data');
    if (!tag) return null;
    try {
      return JSON.parse(tag.textContent);
    } catch (err) {
      // A malformed frame set should not take the rest of the page with it.
      if (window.console) console.error('vz-iv: bad frame data', err);
      return null;
    }
  }

  // ---------------------------------------------------------------- drawing

  function drawRow(row) {
    var wrap = el('div', 'vz-iv-row');
    if (row.label) wrap.appendChild(el('span', 'vz-iv-rowlabel', row.label));

    var track = el('div', 'vz-iv-track vz-iv-' + (row.kind || 'cells'));
    (row.items || []).forEach(function (item, i) {
      var cell = el('div', 'vz-iv-cell' + (item.k ? ' is-' + item.k : ''));
      cell.appendChild(el('span', 'vz-iv-v', item.v == null ? '' : String(item.v)));
      // The index strip is what makes an off-by-one visible; without it a row
      // of numbers says nothing about where lo and hi actually are.
      if (row.index !== false && (row.kind || 'cells') !== 'pairs') {
        cell.appendChild(el('span', 'vz-iv-i', String(i)));
      }
      if (item.tag) cell.appendChild(el('span', 'vz-iv-tag', item.tag));
      track.appendChild(cell);
    });
    wrap.appendChild(track);
    return wrap;
  }

  function render(block, data, i) {
    var frame = data.frames[i] || {};
    var stage = block.querySelector('.vz-iv-stage');
    stage.textContent = '';
    (frame.rows || []).forEach(function (row) { stage.appendChild(drawRow(row)); });

    var caption = block.querySelector('.vz-iv-caption');
    if (caption) caption.textContent = frame.note || '';

    var reads = block.querySelector('.vz-iv-reads');
    if (reads) {
      reads.textContent = '';
      var values = frame.read || {};
      Object.keys(values).forEach(function (name) {
        var pill = el('span', 'vz-iv-read');
        pill.appendChild(el('span', 'vz-iv-read-k', name));
        // The id is what tools/build_labs.py picks up as a readout, so the
        // predict-then-reveal panel can measure this page rather than guess.
        var v = el('span', 'vz-iv-read-v', String(values[name]));
        v.id = 'iv-read-' + name.replace(/[^a-z0-9]+/gi, '-');
        pill.appendChild(v);
        reads.appendChild(pill);
      });
    }

    var badge = block.querySelector('.vz-iv-count');
    if (badge) badge.textContent = 'Step ' + (i + 1) + ' of ' + data.frames.length;

    var scrub = block.querySelector('.vz-iv-scrub');
    if (scrub && Number(scrub.value) !== i) scrub.value = String(i);
  }

  // ---------------------------------------------------------------- wiring

  function wire(block) {
    var data = parse(block);
    if (!data || !data.frames || !data.frames.length) return;

    var at = 0;
    var timer = null;
    var play = block.querySelector('.vz-iv-play');

    function show(i) {
      at = Math.max(0, Math.min(data.frames.length - 1, i));
      render(block, data, at);
    }

    function stop() {
      if (timer) clearInterval(timer);
      timer = null;
      if (play) {
        play.textContent = 'Auto-run';
        play.setAttribute('aria-pressed', 'false');
      }
    }

    function start() {
      if (timer) return stop();
      if (at >= data.frames.length - 1) show(0);
      if (play) {
        play.textContent = 'Pause';
        play.setAttribute('aria-pressed', 'true');
      }
      timer = setInterval(function () {
        if (at >= data.frames.length - 1) return stop();
        show(at + 1);
      }, STEP_MS);
    }

    var step = block.querySelector('.vz-iv-step');
    var back = block.querySelector('.vz-iv-back');
    var reset = block.querySelector('.vz-iv-reset');
    var scrub = block.querySelector('.vz-iv-scrub');

    if (step) step.addEventListener('click', function () { stop(); show(at + 1); });
    if (back) back.addEventListener('click', function () { stop(); show(at - 1); });
    if (play) play.addEventListener('click', start);
    if (reset) reset.addEventListener('click', function () { stop(); show(0); });
    if (scrub) {
      scrub.max = String(data.frames.length - 1);
      scrub.addEventListener('input', function () { stop(); show(Number(scrub.value)); });
    }

    // Arrow keys, but only while the block has focus - the page also scrolls
    // with them, and stealing that everywhere would be worse than the feature.
    block.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { stop(); show(at + 1); e.preventDefault(); }
      else if (e.key === 'ArrowLeft') { stop(); show(at - 1); e.preventDefault(); }
    });

    show(0);
  }

  function init() {
    var blocks = document.querySelectorAll('.vz-iv[data-vz-iv]');
    for (var i = 0; i < blocks.length; i++) wire(blocks[i]);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
