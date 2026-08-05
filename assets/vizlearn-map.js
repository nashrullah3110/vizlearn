/* /map/ - the concept map.
 *
 * Renders the graph the build derived from tools/sequence.py (shipped next
 * door in map-data.js), then layers this reader's progress on top from the
 * same localStorage store the hub and /practice/ use. The structure is the
 * build's; only the ticks are local.
 */
(function () {
  'use strict';

  var MAP = window.VIZLEARN_MAP || { spine: [], lanes: [] };

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function progress() {
    return (window.VizLearn && window.VizLearn.progress()) || {};
  }

  function chip(mod, done) {
    return '<a class="vz-m-chip' + (done ? ' is-done' : '') + '" href="../' +
      esc(mod.path) + '"' + (done ? ' title="You have opened this"' : '') + '>' +
      esc(mod.title) + '</a>';
  }

  function render() {
    var seen = progress();
    var hideDone = document.getElementById('map-hide-done').checked;

    // --- the spine ---
    document.getElementById('map-spine').innerHTML = MAP.spine.map(function (s) {
      var mods = s.mods.filter(function (m) { return !(hideDone && seen[m.path]); });
      return '<div class="vz-m-stage">' +
        '<p class="vz-m-stage-n">Stage ' + s.n + '</p>' +
        '<h3>' + esc(s.title) + '</h3>' +
        '<p>' + esc(s.blurb) + '</p>' +
        '<div class="vz-m-chips">' +
          (mods.length
            ? mods.map(function (m) { return chip(m, !!seen[m.path]); }).join('')
            : '<span class="vz-m-arrow">all opened</span>') +
        '</div></div>';
    }).join('');

    // --- the lanes ---
    var totalDone = 0, total = 0;
    document.getElementById('map-lanes').innerHTML = MAP.lanes.map(function (lane) {
      var done = lane.mods.filter(function (m) { return seen[m.path]; }).length;
      totalDone += done;
      total += lane.mods.length;

      var shown = lane.mods.filter(function (m) { return !(hideDone && seen[m.path]); });
      var chips = shown.length
        ? shown.map(function (m, i) {
            // The arrow is what carries "builds on" between two chips. It is
            // decoration, so it is hidden from the accessibility tree - the
            // reading order already says the same thing.
            var arrow = i ? '<span class="vz-m-arrow" aria-hidden="true">&rarr;</span>' : '';
            return arrow + chip(m, !!seen[m.path]);
          }).join('')
        : '<span class="vz-m-arrow">every module in this track opened</span>';

      var pct = lane.mods.length ? Math.round(done / lane.mods.length * 100) : 0;
      return '<section class="vz-m-lane">' +
        '<div class="vz-m-lane-top">' +
          '<h3>' + esc(lane.title) + '</h3>' +
          '<span class="vz-m-count">' + done + ' of ' + lane.mods.length + ' opened</span>' +
        '</div>' +
        '<div class="vz-m-chips">' + chips + '</div>' +
        '<div class="vz-m-bar"><div style="width:' + pct + '%"></div></div>' +
      '</section>';
    }).join('');

    var pct = total ? Math.round(totalDone / total * 100) : 0;
    document.getElementById('map-summary').textContent =
      totalDone + ' of ' + total + ' modules opened (' + pct + '%)';
  }

  function init() {
    if (!document.getElementById('map-lanes')) return;
    document.getElementById('map-hide-done').addEventListener('change', render);
    render();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
