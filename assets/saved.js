/* /saved/ - the bookmarks-and-notes list.
 *
 * Reads the same `vizlearn_saved` store the bookmark control in each module
 * header writes to, and joins it against the module catalog for titles and
 * track names. Nothing is fetched and nothing is uploaded; if the store is
 * empty the page says so rather than rendering an empty box.
 */
(function () {
  'use strict';

  function catalog() {
    var by = {};
    (window.VIZLEARN_MODULES || []).forEach(function (m) { by[m.path] = m; });
    return by;
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function when(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return '';
    var days = Math.floor((Date.now() - d.getTime()) / 86400000);
    if (days <= 0) return 'today';
    if (days === 1) return 'yesterday';
    if (days < 30) return days + ' days ago';
    return d.toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' });
  }

  function render() {
    var store = (window.VizLearn && window.VizLearn.saved()) || {};
    var mods = catalog();
    var list = document.getElementById('saved-list');
    var empty = document.getElementById('saved-empty');
    var count = document.getElementById('saved-count');

    var rows = Object.keys(store).map(function (path) {
      var e = store[path] || {};
      var m = mods[path] || {};
      return {
        path: path,
        // The catalog is the better source, but a module renamed since the
        // bookmark was made would vanish from it - so the title captured at
        // save time is the fallback rather than the other way round.
        title: m.title || e.title || path,
        track: m.category || '',
        note: e.note || '',
        marked: !!e.marked,
        at: e.at || ''
      };
    }).sort(function (a, b) { return (b.at || '').localeCompare(a.at || ''); });

    if (!rows.length) {
      list.innerHTML = '';
      empty.hidden = false;
      count.textContent = '';
      return;
    }
    empty.hidden = true;
    count.textContent = rows.length + (rows.length === 1 ? ' module saved' : ' modules saved');

    list.innerHTML = rows.map(function (r) {
      return '<article class="vz-s-item">' +
        '<div class="vz-s-top">' +
          '<a class="vz-s-title" href="../' + esc(r.path) + '">' + esc(r.title) + '</a>' +
          '<span class="vz-s-track">' + esc(r.track) +
            (r.at ? ' &middot; ' + esc(when(r.at)) : '') + '</span>' +
        '</div>' +
        (r.note ? '<div class="vz-s-note">' + esc(r.note) + '</div>' : '') +
        '<div class="vz-s-actions">' +
          '<button type="button" class="vz-s-btn" data-remove="' + esc(r.path) + '">Remove</button>' +
        '</div>' +
      '</article>';
    }).join('');
  }

  function init() {
    if (!document.getElementById('saved-list')) return;
    render();

    document.getElementById('saved-list').addEventListener('click', function (e) {
      var btn = e.target.closest('[data-remove]');
      if (!btn) return;
      var path = btn.getAttribute('data-remove');
      // Clearing both fields is what deletes the record; saveEntry drops any
      // entry that is neither bookmarked nor annotated.
      window.VizLearn.save(path, { marked: false, note: '' });
      render();
      window.VizLearn.toast('Removed');
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
