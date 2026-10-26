/* Topic-aware, state-faithful step-throughs for /interview/ lessons.
 * Frames are recorded by running each lesson's example algorithm in
 * tools/interview_viz.py. This player changes how that real state is shown;
 * it never invents a result for an input the underlying example did not run.
 */
(function () {
  'use strict';

  var STEP_MS = 850;
  var SVG = 'http://www.w3.org/2000/svg';

  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function svgEl(tag, attrs, text) {
    var node = document.createElementNS(SVG, tag);
    Object.keys(attrs || {}).forEach(function (key) {
      node.setAttribute(key, attrs[key]);
    });
    if (text != null) node.textContent = text;
    return node;
  }

  function parse(block) {
    var tag = block.querySelector('.vz-iv-data');
    if (!tag) return null;
    try {
      return JSON.parse(tag.textContent);
    } catch (err) {
      if (window.console) console.error('vz-iv: bad frame data', err);
      return null;
    }
  }

  function layoutFor(row, topic) {
    if (row.view) return row.view;
    var label = String(row.label || '').toLowerCase();
    if (row.kind === 'pairs') return 'pairs';
    if (row.kind === 'text') return 'text';
    if (/bar heights|histogram/.test(label)) return 'bars';
    if (/\bheap\b/.test(label) || topic === 'heaps' && /half/.test(label)) return 'heap';
    if (/\bstack\b|inbox|outbox|minimums/.test(label)) return 'stack';
    if (/\bqueue\b|\bdeque\b/.test(label)) return 'queue';
    if (/\bslots?\b|\bbuckets?\b/.test(label)) return 'buckets';
    if (/ways to reach|fewest coins|\btails\b|best for the first|base cases/.test(label) || topic === 'dp') return 'dp';
    return 'cells';
  }

  function findPreviousRow(frame, row) {
    if (!frame || !frame.rows) return null;
    var label = row.label || '';
    for (var i = 0; i < frame.rows.length; i++) {
      var candidate = frame.rows[i];
      if ((candidate.label || '') === label && (candidate.kind || 'cells') === (row.kind || 'cells')) {
        return candidate;
      }
    }
    return null;
  }

  function changed(item, previous) {
    if (!previous) return false;
    return String(item.v) !== String(previous.v) || item.k !== previous.k || item.tag !== previous.tag;
  }

  function stateText(state) {
    return {
      lo: 'low marker', hi: 'high marker', hit: 'answer or match',
      done: 'settled', dim: 'outside the active region', bad: 'discarded'
    }[state] || '';
  }

  function drawCell(item, index, row, layout, previous) {
    var state = item.k ? ' is-' + item.k : '';
    var extra = layout === 'buckets' ? ' vz-iv-bucket' : '';
    var cell = el('div', 'vz-iv-cell' + state + extra + (changed(item, previous) ? ' is-changed' : ''));
    var value = item.v == null ? '' : String(item.v);
    if (layout === 'pairs') {
      var split = value.indexOf(' : ');
      if (split >= 0) {
        cell.appendChild(el('span', 'vz-iv-pair-key', value.slice(0, split)));
        cell.appendChild(el('span', 'vz-iv-pair-value', value.slice(split + 3)));
      } else {
        cell.appendChild(el('span', 'vz-iv-pair-value', value));
      }
    } else {
      cell.appendChild(el('span', 'vz-iv-v', value));
    }

    if (layout === 'buckets' || row.index !== false && layout !== 'pairs' && layout !== 'stack') {
      cell.appendChild(el('span', 'vz-iv-i', String(index)));
    }
    if (item.tag) cell.appendChild(el('span', 'vz-iv-tag', item.tag));
    var label = 'Item ' + (index + 1) + ': ' + value;
    if (item.tag) label += ', marker ' + item.tag;
    if (item.k) label += ', ' + stateText(item.k);
    cell.setAttribute('aria-label', label);
    return cell;
  }

  function drawCells(row, layout, previous) {
    var wrap = el('div', 'vz-iv-row vz-iv-row-' + layout);
    if (row.label) wrap.appendChild(el('span', 'vz-iv-rowlabel', row.label));
    var track = el('div', 'vz-iv-track vz-iv-' + layout);
    track.setAttribute('role', 'list');
    (row.items || []).forEach(function (item, i) {
      var old = previous && previous.items ? previous.items[i] : null;
      var cell = drawCell(item, i, row, layout, old);
      cell.setAttribute('role', 'listitem');
      track.appendChild(cell);
    });
    wrap.appendChild(track);
    return wrap;
  }

  function drawStack(row, previous) {
    var wrap = el('div', 'vz-iv-row vz-iv-row-stack');
    if (row.label) wrap.appendChild(el('span', 'vz-iv-rowlabel', row.label));
    var stack = el('div', 'vz-iv-stack');
    stack.appendChild(el('span', 'vz-iv-stack-edge', 'TOP'));
    var track = el('div', 'vz-iv-track vz-iv-stack-track');
    track.setAttribute('role', 'list');
    var items = (row.items || []).filter(function (item) { return String(item.v) !== '(empty)'; });
    items.forEach(function (item, i) {
      var old = previous && previous.items ? previous.items[i] : null;
      var cell = drawCell(item, i, { index: false }, 'stack', old);
      cell.setAttribute('role', 'listitem');
      track.appendChild(cell);
    });
    if (!items.length) {
      track.appendChild(el('span', 'vz-iv-empty', 'empty'));
    }
    stack.appendChild(track);
    stack.appendChild(el('span', 'vz-iv-stack-edge', 'BOTTOM'));
    wrap.appendChild(stack);
    return wrap;
  }

  function drawHeap(row, previous) {
    var items = row.items || [];
    if (!items.length || items.every(function (item) { return String(item.v) === '(empty)'; })) {
      return drawCells(row, 'cells', previous);
    }
    var wrap = el('div', 'vz-iv-row vz-iv-row-heap');
    if (row.label) wrap.appendChild(el('span', 'vz-iv-rowlabel', row.label));
    var scroll = el('div', 'vz-iv-diagram-scroll');
    var depth = Math.floor(Math.log(items.length) / Math.LN2);
    var height = 70 + depth * 88;
    var svg = svgEl('svg', {
      viewBox: '0 0 800 ' + height,
      role: 'img',
      'aria-label': 'Heap shown as a binary tree. Values in level order: ' + items.map(function (it) { return it.v; }).join(', ')
    });
    svg.classList.add('vz-iv-heap-svg');
    if (items.length > 7) svg.style.minWidth = '38rem';

    var positions = items.map(function (_, index) {
      var level = Math.floor(Math.log(index + 1) / Math.LN2);
      var first = Math.pow(2, level) - 1;
      var offset = index - first;
      return { x: 800 * (offset + 0.5) / Math.pow(2, level), y: 34 + level * 88 };
    });
    items.forEach(function (_, index) {
      if (index === 0) return;
      var parent = Math.floor((index - 1) / 2);
      svg.appendChild(svgEl('line', {
        x1: positions[parent].x, y1: positions[parent].y + 23,
        x2: positions[index].x, y2: positions[index].y - 23,
        class: 'vz-iv-heap-edge'
      }));
    });
    items.forEach(function (item, index) {
      var point = positions[index];
      var old = previous && previous.items ? previous.items[index] : null;
      var group = svgEl('g', { class: 'vz-iv-heap-node' + (item.k ? ' is-' + item.k : '') + (changed(item, old) ? ' is-changed' : '') });
      group.appendChild(svgEl('circle', { cx: point.x, cy: point.y, r: 23 }));
      var value = String(item.v);
      group.appendChild(svgEl('text', { x: point.x, y: point.y + 5, 'text-anchor': 'middle' }, value.length > 7 ? value.slice(0, 6) + '…' : value));
      if (item.tag) group.appendChild(svgEl('text', { x: point.x, y: point.y - 30, 'text-anchor': 'middle', class: 'vz-iv-svg-tag' }, item.tag));
      svg.appendChild(group);
    });
    scroll.appendChild(svg);
    wrap.appendChild(scroll);
    return wrap;
  }

  function drawQueue(row, previous) {
    var wrap = el('div', 'vz-iv-row vz-iv-row-queue');
    if (row.label) wrap.appendChild(el('span', 'vz-iv-rowlabel', row.label));
    var line = el('div', 'vz-iv-queue');
    line.appendChild(el('span', 'vz-iv-queue-end', 'FRONT'));
    var track = el('div', 'vz-iv-track vz-iv-queue-track');
    track.setAttribute('role', 'list');
    (row.items || []).filter(function (item) { return String(item.v) !== '(empty)'; }).forEach(function (item, i) {
      var old = previous && previous.items ? previous.items[i] : null;
      var cell = drawCell(item, i, { index: false }, 'queue', old);
      cell.setAttribute('role', 'listitem');
      track.appendChild(cell);
    });
    if (!track.childNodes.length) track.appendChild(el('span', 'vz-iv-empty', 'empty'));
    line.appendChild(track);
    line.appendChild(el('span', 'vz-iv-queue-end', 'REAR'));
    wrap.appendChild(line);
    return wrap;
  }

  function drawBars(row, previous) {
    var items = row.items || [];
    var wrap = el('div', 'vz-iv-row vz-iv-row-bars');
    if (row.label) wrap.appendChild(el('span', 'vz-iv-rowlabel', row.label));
    var scroll = el('div', 'vz-iv-diagram-scroll');
    var width = 800, height = 240, left = 30, right = 20, top = 22, base = 186;
    var plotWidth = width - left - right;
    var max = Math.max.apply(null, items.map(function (item) { return Number(item.v) || 0; }).concat([1]));
    var gap = items.length > 22 ? 3 : 8;
    var barWidth = Math.max(4, (plotWidth - gap * Math.max(0, items.length - 1)) / Math.max(items.length, 1));
    var svg = svgEl('svg', { viewBox: '0 0 ' + width + ' ' + height, role: 'img',
      'aria-label': 'Bar chart of ' + row.label + ': ' + items.map(function (item) { return item.v; }).join(', ') });
    svg.classList.add('vz-iv-bars-svg');
    svg.style.minWidth = items.length > 14 ? '38rem' : '100%';
    svg.appendChild(svgEl('line', { x1: left, y1: base, x2: width - right, y2: base, class: 'vz-iv-chart-axis' }));
    items.forEach(function (item, i) {
      var value = Math.max(0, Number(item.v) || 0);
      var h = value ? Math.max(3, (value / max) * (base - top)) : 2;
      var x = left + i * (barWidth + gap);
      var y = base - h;
      var old = previous && previous.items ? previous.items[i] : null;
      var state = item.k ? ' is-' + item.k : '';
      var group = svgEl('g', { class: 'vz-iv-bar-group' + state + (changed(item, old) ? ' is-changed' : '') });
      group.appendChild(svgEl('rect', { x: x, y: y, width: barWidth, height: h, rx: Math.min(5, barWidth / 3), class: 'vz-iv-bar' }));
      group.appendChild(svgEl('text', { x: x + barWidth / 2, y: Math.max(14, y - 5), 'text-anchor': 'middle', class: 'vz-iv-bar-value' }, String(item.v)));
      group.appendChild(svgEl('text', { x: x + barWidth / 2, y: base + 19, 'text-anchor': 'middle', class: 'vz-iv-bar-index' }, String(i)));
      if (item.tag) group.appendChild(svgEl('text', { x: x + barWidth / 2, y: Math.max(11, y - 19), 'text-anchor': 'middle', class: 'vz-iv-svg-tag' }, item.tag));
      svg.appendChild(group);
    });
    scroll.appendChild(svg);
    wrap.appendChild(scroll);
    return wrap;
  }

  function drawRow(row, topic, previousFrame) {
    var layout = layoutFor(row, topic);
    var previous = findPreviousRow(previousFrame, row);
    if (layout === 'heap') return drawHeap(row, previous);
    if (layout === 'bars') return drawBars(row, previous);
    if (layout === 'stack') return drawStack(row, previous);
    if (layout === 'queue') return drawQueue(row, previous);
    return drawCells(row, layout, previous);
  }

  function renderLegend(block, data) {
    var legend = block.querySelector('.vz-iv-legend');
    if (!legend) {
      legend = el('div', 'vz-iv-legend');
      legend.setAttribute('aria-label', 'Visualization state key');
      var panel = block.querySelector('.vz-iv-panel');
      var reads = panel && panel.querySelector('.vz-iv-reads');
      if (panel) panel.insertBefore(legend, reads || panel.firstChild);
    }
    var used = {};
    (data.frames || []).forEach(function (frame) {
      (frame.rows || []).forEach(function (row) {
        (row.items || []).forEach(function (item) { if (item.k) used[item.k] = true; });
      });
    });
    var names = { lo: 'low marker', hi: 'high marker', hit: 'answer / match', done: 'settled', dim: 'outside range', bad: 'discarded' };
    var keys = Object.keys(names).filter(function (key) { return used[key]; });
    legend.textContent = '';
    if (!keys.length) return;
    legend.appendChild(el('span', 'vz-iv-legend-title', 'State key'));
    keys.forEach(function (key) {
      var entry = el('span', 'vz-iv-legend-item');
      entry.appendChild(el('i', 'vz-iv-legend-swatch is-' + key));
      entry.appendChild(el('span', '', names[key]));
      legend.appendChild(entry);
    });
  }

  function render(block, data, index) {
    var frame = data.frames[index] || {};
    var previous = index > 0 ? data.frames[index - 1] : null;
    var stage = block.querySelector('.vz-iv-stage');
    stage.textContent = '';
    (frame.rows || []).forEach(function (row) { stage.appendChild(drawRow(row, data.topic || '', previous)); });

    var caption = block.querySelector('.vz-iv-caption');
    if (caption) caption.textContent = frame.note || '';

    var reads = block.querySelector('.vz-iv-reads');
    if (reads) {
      reads.textContent = '';
      var values = frame.read || {};
      Object.keys(values).forEach(function (name) {
        var pill = el('span', 'vz-iv-read');
        pill.appendChild(el('span', 'vz-iv-read-k', name));
        var value = el('span', 'vz-iv-read-v', String(values[name]));
        value.id = 'iv-read-' + name.replace(/[^a-z0-9]+/gi, '-');
        pill.appendChild(value);
        reads.appendChild(pill);
      });
    }

    var count = block.querySelector('.vz-iv-count');
    if (count) count.textContent = 'Step ' + (index + 1) + ' of ' + data.frames.length;
    var scrub = block.querySelector('.vz-iv-scrub');
    if (scrub) {
      if (Number(scrub.value) !== index) scrub.value = String(index);
      scrub.setAttribute('aria-valuetext', 'Step ' + (index + 1) + ' of ' + data.frames.length);
    }

    var back = block.querySelector('.vz-iv-back');
    var step = block.querySelector('.vz-iv-step');
    if (back) back.disabled = index === 0;
    if (step) step.disabled = index >= data.frames.length - 1;
  }

  function wire(block) {
    var data = parse(block);
    if (!data || !data.frames || !data.frames.length) return;
    if (data.topic) block.setAttribute('data-vz-topic', data.topic);
    var at = 0;
    var timer = null;
    var play = block.querySelector('.vz-iv-play');
    var step = block.querySelector('.vz-iv-step');
    var back = block.querySelector('.vz-iv-back');
    var reset = block.querySelector('.vz-iv-reset');
    var scrub = block.querySelector('.vz-iv-scrub');

    function show(index) {
      at = Math.max(0, Math.min(data.frames.length - 1, index));
      render(block, data, at);
    }

    function stop() {
      if (timer) window.clearInterval(timer);
      timer = null;
      if (play) {
        play.textContent = 'Auto-run';
        play.setAttribute('aria-pressed', 'false');
      }
    }

    function start() {
      if (timer) { stop(); return; }
      if (at >= data.frames.length - 1) show(0);
      if (play) {
        play.textContent = 'Pause';
        play.setAttribute('aria-pressed', 'true');
      }
      timer = window.setInterval(function () {
        if (at >= data.frames.length - 1) { stop(); return; }
        show(at + 1);
      }, STEP_MS);
    }

    if (scrub) {
      scrub.max = String(data.frames.length - 1);
      scrub.addEventListener('input', function () { stop(); show(Number(scrub.value)); });
    }
    if (step) step.addEventListener('click', function () { stop(); show(at + 1); });
    if (back) back.addEventListener('click', function () { stop(); show(at - 1); });
    if (play) play.addEventListener('click', start);
    if (reset) reset.addEventListener('click', function () { stop(); show(0); });

    block.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowRight') { stop(); show(at + 1); event.preventDefault(); }
      else if (event.key === 'ArrowLeft') { stop(); show(at - 1); event.preventDefault(); }
    });
    document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); });
    renderLegend(block, data);
    show(0);
  }

  function init() {
    var blocks = document.querySelectorAll('.vz-iv[data-vz-iv]');
    for (var i = 0; i < blocks.length; i++) wire(blocks[i]);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
