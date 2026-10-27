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

  function drawPairs(row, previous) {
    var wrap = el('div', 'vz-iv-row vz-iv-row-pairs');
    if (row.label) wrap.appendChild(el('span', 'vz-iv-rowlabel', row.label));
    var table = el('div', 'vz-iv-pair-table');
    table.setAttribute('role', 'table');
    table.setAttribute('aria-label', row.label || 'Current key and value state');
    (row.items || []).forEach(function (item, index) {
      var value = item.v == null ? '' : String(item.v);
      var split = value.indexOf(' : ');
      var key = split >= 0 ? value.slice(0, split) : '';
      var result = split >= 0 ? value.slice(split + 3) : value;
      var old = previous && previous.items ? previous.items[index] : null;
      var state = item.k ? ' is-' + item.k : '';
      var line = el('div', 'vz-iv-pair' + state + (changed(item, old) ? ' is-changed' : ''));
      line.setAttribute('role', 'row');
      line.setAttribute('aria-label', (key ? key + ': ' : '') + result + (item.k ? ', ' + stateText(item.k) : ''));
      line.appendChild(el('span', 'vz-iv-pair-key', key || 'value'));
      line.appendChild(el('span', 'vz-iv-pair-value', result));
      if (item.tag) line.appendChild(el('span', 'vz-iv-tag', item.tag));
      table.appendChild(line);
    });
    wrap.appendChild(table);
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

  function drawIntervals(row) {
    var parsed = (row.items || []).map(function (item) {
      var value = String(item.v == null ? '' : item.v);
      var split = value.indexOf(' : ');
      var range = split < 0 ? value : value.slice(0, split);
      var state = split < 0 ? '' : value.slice(split + 3);
      var match = range.match(/^(-?\d+(?:\.\d+)?)-(-?\d+(?:\.\d+)?)$/);
      return match ? { item: item, start: Number(match[1]), end: Number(match[2]), state: state } : null;
    }).filter(Boolean);
    var wrap = el('div', 'vz-iv-row vz-iv-row-intervals');
    if (row.label) wrap.appendChild(el('span', 'vz-iv-rowlabel', row.label));
    if (!parsed.length) return drawCells(row, 'pairs', null);

    var min = Math.min.apply(null, parsed.map(function (x) { return x.start; }));
    var max = Math.max.apply(null, parsed.map(function (x) { return x.end; }));
    var span = Math.max(1, max - min);
    var left = 48, right = 18, width = 800;
    var lane = 44, top = 10, axis = 28;
    var height = top + parsed.length * lane + axis;
    var svg = svgEl('svg', {
      viewBox: '0 0 ' + width + ' ' + height,
      role: 'img',
      'aria-label': 'Intervals on a shared number line: ' + parsed.map(function (x) {
        return x.start + ' to ' + x.end + (x.state ? ', ' + x.state : '');
      }).join('; ')
    });
    svg.classList.add('vz-iv-intervals-svg');
    var plot = width - left - right;
    var ticks = span <= 8 ? Math.ceil(span) : 4;
    for (var t = 0; t <= ticks; t++) {
      var value = min + span * t / ticks;
      var x = left + plot * t / ticks;
      svg.appendChild(svgEl('line', { x1: x, y1: top, x2: x, y2: height - axis + 1, class: 'vz-iv-interval-guide' }));
      svg.appendChild(svgEl('text', { x: x, y: height - 7, 'text-anchor': 'middle', class: 'vz-iv-interval-tick' },
        Number.isInteger(value) ? String(value) : value.toFixed(1)));
    }
    parsed.forEach(function (entry, index) {
      var y = top + index * lane + 8;
      var x1 = left + (entry.start - min) / span * plot;
      var x2 = left + (entry.end - min) / span * plot;
      var group = svgEl('g', { class: 'vz-iv-interval' + (entry.item.k ? ' is-' + entry.item.k : '') });
      group.appendChild(svgEl('text', { x: 2, y: y + 15, class: 'vz-iv-interval-index' }, String(index + 1)));
      group.appendChild(svgEl('rect', { x: x1, y: y, width: Math.max(8, x2 - x1), height: 22, rx: 6 }));
      group.appendChild(svgEl('text', { x: Math.min(x1 + 7, width - 90), y: y + 15, class: 'vz-iv-interval-label' },
        entry.start + '–' + entry.end));
      svg.appendChild(group);
    });
    wrap.appendChild(svg);
    return wrap;
  }

  function drawMatrix(row, previousFrame) {
    var columns = Math.max(1, Number(row.columns) || 1);
    var items = row.items || [];
    var rowLabels = row.row_labels || [];
    var columnLabels = row.column_labels || [];
    var wrap = el('div', 'vz-iv-row vz-iv-row-matrix');
    if (row.label) wrap.appendChild(el('span', 'vz-iv-rowlabel', row.label));
    var grid = el('div', 'vz-iv-matrix');
    grid.setAttribute('role', 'grid');
    grid.setAttribute('aria-label', row.label || 'Table of algorithm states');
    grid.style.gridTemplateColumns = 'minmax(2rem, .65fr) repeat(' + columns + ', minmax(2.6rem, 1fr))';
    grid.appendChild(el('span', 'vz-iv-matrix-corner', ''));
    columnLabels.forEach(function (label) {
      var head = el('span', 'vz-iv-matrix-head', label);
      head.setAttribute('role', 'columnheader');
      grid.appendChild(head);
    });
    for (var r = 0; r < rowLabels.length; r++) {
      var rowHead = el('span', 'vz-iv-matrix-head vz-iv-matrix-rowhead', rowLabels[r]);
      rowHead.setAttribute('role', 'rowheader');
      grid.appendChild(rowHead);
      for (var c = 0; c < columns; c++) {
        var index = r * columns + c;
        var item = items[index] || { v: '' };
        var previous = findPreviousRow(previousFrame, row);
        var old = previous && previous.items ? previous.items[index] : null;
        var cell = drawCell(item, c, { index: false }, 'matrix', old);
        cell.setAttribute('role', 'gridcell');
        cell.setAttribute('aria-label', 'row ' + rowLabels[r] + ', column ' + columnLabels[c] + ': ' + item.v + (item.k ? ', ' + stateText(item.k) : ''));
        grid.appendChild(cell);
      }
    }
    wrap.appendChild(grid);
    return wrap;
  }

  function drawRow(row, topic, previousFrame) {
    var layout = layoutFor(row, topic);
    var previous = findPreviousRow(previousFrame, row);
    if (layout === 'pairs') return drawPairs(row, previous);
    if (layout === 'heap') return drawHeap(row, previous);
    if (layout === 'bars') return drawBars(row, previous);
    if (layout === 'intervals') return drawIntervals(row);
    if (layout === 'matrix') return drawMatrix(row, previousFrame);
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
    updateTimeline(block, index);
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

  function buildTimeline(block, data, select) {
    var rail = block.querySelector('.vz-iv-timeline');
    if (!rail) return;
    rail.textContent = '';
    (data.frames || []).forEach(function (frame, index) {
      var note = String(frame.note || '').replace(/\s+/g, ' ').trim();
      var button = el('button', 'vz-iv-step-mark', String(index + 1));
      button.type = 'button';
      button.title = note;
      button.setAttribute('aria-label', 'Step ' + (index + 1) + ': ' + note);
      button.addEventListener('click', function () { select(index); });
      rail.appendChild(button);
    });
  }

  function updateTimeline(block, index) {
    var rail = block.querySelector('.vz-iv-timeline');
    if (!rail) return;
    Array.prototype.forEach.call(rail.children, function (button, step) {
      button.classList.toggle('is-complete', step < index);
      button.classList.toggle('is-current', step === index);
      if (step === index) button.setAttribute('aria-current', 'step');
      else button.removeAttribute('aria-current');
    });
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

    buildTimeline(block, data, function (index) { stop(); show(index); });

    if (scrub) {
      scrub.max = String(data.frames.length - 1);
      scrub.addEventListener('input', function () { stop(); show(Number(scrub.value)); });
    }
    if (step) step.addEventListener('click', function () { stop(); show(at + 1); });
    if (back) back.addEventListener('click', function () { stop(); show(at - 1); });
    if (play) play.addEventListener('click', start);
    if (reset) reset.addEventListener('click', function () { stop(); show(0); });

    block.addEventListener('keydown', function (event) {
      if (event.target !== block) return;
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
