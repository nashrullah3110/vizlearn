/* VizLearn - shared "search all articles" dropdown.
 *
 * Replaces the copy of this logic that used to be pasted into every module
 * page. Reads the catalog from assets/modules.js (window.VIZLEARN_MODULES).
 *
 * Matching is token-based rather than a single substring test, so word order
 * does not matter ("matrix confusion" finds "Confusion Matrix Analysis"),
 * partial words work, small typos are tolerated, and module descriptions are
 * searched alongside titles.
 *
 * Works from any directory depth and from any deployment root, because the
 * site root is derived from this script's own URL rather than guessed from
 * window.location.
 */
(function () {
  'use strict';

  // --- site root, derived from this script's own src -----------------------
  var self = document.currentScript;
  if (!self) {
    var all = document.getElementsByTagName('script');
    for (var i = all.length - 1; i >= 0; i--) {
      if (/search\.js(\?|$)/.test(all[i].src)) { self = all[i]; break; }
    }
  }
  var ROOT = self ? self.src.replace(/assets\/search\.js(\?.*)?$/, '') : '';

  var MAX_RESULTS = 12;

  // --- icons (inline SVG; no icon font needed) -----------------------------
  var ICON_PATHS = {
    brain: '<path d="M12 5a3 3 0 0 0-6 0v.1A2.5 2.5 0 0 0 4 7.6a2.5 2.5 0 0 0 .5 1.5A2.5 2.5 0 0 0 4 12a2.5 2.5 0 0 0 1 2 2.5 2.5 0 0 0 2 4 2.5 2.5 0 0 0 5 0V5Z"/><path d="M12 5a3 3 0 0 1 6 0v.1a2.5 2.5 0 0 1 2 2.5 2.5 2.5 0 0 1-.5 1.5A2.5 2.5 0 0 1 20 12a2.5 2.5 0 0 1-1 2 2.5 2.5 0 0 1-2 4 2.5 2.5 0 0 1-5 0"/>',
    network: '<rect x="9" y="2" width="6" height="5" rx="1"/><rect x="2" y="17" width="6" height="5" rx="1"/><rect x="16" y="17" width="6" height="5" rx="1"/><path d="M12 7v5M5 17v-2h14v2"/>',
    layers: '<path d="m12 2 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5"/><path d="m3 17 9 5 9-5"/>',
    comments: '<path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 9 9 0 0 1-3.8-.8L3 21l1.9-5.2A8.4 8.4 0 0 1 4 11.5a8.4 8.4 0 0 1 9-8.4 8.4 8.4 0 0 1 8 8.4Z"/>',
    eye: '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    database: '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
    robot: '<rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 8V4M9 2h6"/><circle cx="9" cy="13" r="1"/><circle cx="15" cy="13" r="1"/><path d="M9 17h6"/>',
    sigma: '<path d="M18 5H6l6 7-6 7h12"/>',
    book: '<path d="M4 4a2 2 0 0 1 2-2h13v18H6a2 2 0 0 0-2 2V4Z"/><path d="M4 20a2 2 0 0 0 2 2h13"/>',
    arrow: '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    check: '<path d="m20 6-11 11-5-5"/>',
    interview: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2Z"/><path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>'
  };

  function icon(name, cls) {
    var d = ICON_PATHS[name] || ICON_PATHS.book;
    return '<svg class="' + cls + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
      'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>';
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function normalise(s) {
    return String(s).toLowerCase().replace(/[^a-z0-9\s]+/g, ' ').replace(/\s+/g, ' ').trim();
  }

  // --- fuzzy matching ------------------------------------------------------

  /** Levenshtein distance, abandoned once it exceeds `max`. */
  function editDistance(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var prev = [], cur = [], i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur[0] = i;
      var best = cur[0];
      for (j = 1; j <= b.length; j++) {
        cur[j] = Math.min(
          prev[j] + 1,
          cur[j - 1] + 1,
          prev[j - 1] + (a.charAt(i - 1) === b.charAt(j - 1) ? 0 : 1)
        );
        if (cur[j] < best) best = cur[j];
      }
      if (best > max) return max + 1;
      for (j = 0; j <= b.length; j++) prev[j] = cur[j];
    }
    return prev[b.length];
  }

  /**
   * How well one query token matches one field.
   * Returns 0 (no match) to 1 (whole word).
   */
  function tokenScore(token, words, joined) {
    var i, w, best = 0;
    for (i = 0; i < words.length; i++) {
      w = words[i];
      if (w === token) return 1;
      if (w.indexOf(token) === 0) { best = Math.max(best, 0.9); continue; }
      if (w.indexOf(token) > 0) { best = Math.max(best, 0.7); continue; }
    }
    if (best) return best;
    // token spanning a word boundary, e.g. "binarysearch"
    if (joined.indexOf(token) !== -1) return 0.6;
    // small typos, only for tokens long enough that it is not just noise
    if (token.length >= 4) {
      var allow = token.length >= 7 ? 2 : 1;
      for (i = 0; i < words.length; i++) {
        if (editDistance(token, words[i], allow) <= allow) return 0.35;
        if (words[i].length > token.length &&
            editDistance(token, words[i].slice(0, token.length), allow) <= allow) return 0.3;
      }
    }
    return 0;
  }

  var FIELD_WEIGHT = { title: 100, category: 35, desc: 18 };

  function scoreModule(mod, tokens, rawQuery) {
    var total = 0, matchedInTitle = 0;
    for (var t = 0; t < tokens.length; t++) {
      var token = tokens[t];
      var tScore = tokenScore(token, mod._titleWords, mod._titleJoined);
      var cScore = tokenScore(token, mod._catWords, mod._catJoined);
      var dScore = tokenScore(token, mod._descWords, mod._descJoined);

      var best = Math.max(
        tScore * FIELD_WEIGHT.title,
        cScore * FIELD_WEIGHT.category,
        dScore * FIELD_WEIGHT.desc
      );
      // every token has to land somewhere, otherwise this is not a match
      if (best === 0) return 0;
      if (tScore > 0) matchedInTitle++;
      total += best;
    }
    // whole phrase present in the title beats scattered token hits
    if (mod._title.indexOf(rawQuery) !== -1) total += 120;
    if (mod._title.indexOf(rawQuery) === 0) total += 60;
    // prefer concise titles when scores are otherwise close
    total -= mod._title.length * 0.12;
    return { score: total, titleHits: matchedInTitle };
  }

  /**
   * Wrap matching tokens in <mark>. Sentinels go in first and escaping happens
   * afterwards, so a token that happens to match inside an HTML entity (say
   * "amp") cannot corrupt the output.
   */
  function highlight(text, tokens) {
    var OPEN = '\u0001', CLOSE = '\u0002';
    var out = String(text);
    var seen = {};
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (t.length < 2 || seen[t]) continue;
      seen[t] = 1;
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
      out = out.replace(re, OPEN + '$1' + CLOSE);
    }
    return escapeHtml(out)
      .split(OPEN).join('<mark class="vz-mark">')
      .split(CLOSE).join('</mark>');
  }

  /** A short window of the description around the first matching token. */
  function snippet(desc, tokens) {
    if (!desc) return '';
    var lower = desc.toLowerCase(), at = -1;
    for (var i = 0; i < tokens.length; i++) {
      var p = lower.indexOf(tokens[i]);
      if (p !== -1 && (at === -1 || p < at)) at = p;
    }
    if (at === -1) return desc.slice(0, 90) + (desc.length > 90 ? '…' : '');
    var start = Math.max(0, at - 30);
    var end = Math.min(desc.length, at + 70);
    return (start ? '…' : '') + desc.slice(start, end).trim() + (end < desc.length ? '…' : '');
  }

  function init() {
    var input = document.getElementById('appSearchInput') || document.getElementById('searchInput');
    var dropdown = document.getElementById('searchDropdown');
    if (!input || !dropdown) return;

    var modules = (window.VIZLEARN_MODULES || []).map(function (m) {
      var title = normalise(m.title);
      var cat = normalise(m.category);
      var desc = normalise(m.desc || '');
      return {
        title: m.title,
        category: m.category,
        desc: m.desc || '',
        icon: m.icon,
        url: ROOT + m.path,
        path: m.path,
        _title: title,
        _titleWords: title.split(' '),
        _titleJoined: title.replace(/ /g, ''),
        _catWords: cat.split(' '),
        _catJoined: cat.replace(/ /g, ''),
        _descWords: desc.split(' '),
        _descJoined: desc.replace(/ /g, '')
      };
    });

    var results = [];
    var tokens = [];
    var active = -1;

    function search(raw) {
      var q = normalise(raw);
      tokens = q.split(' ').filter(Boolean);
      if (!tokens.length) return [];
      var scored = [];
      for (var i = 0; i < modules.length; i++) {
        var r = scoreModule(modules[i], tokens, q);
        if (r && r.score > 0) scored.push({ mod: modules[i], score: r.score, titleHits: r.titleHits });
      }
      scored.sort(function (a, b) {
        if (b.titleHits !== a.titleHits) return b.titleHits - a.titleHits;
        return b.score - a.score;
      });
      return scored.slice(0, MAX_RESULTS).map(function (s) { return s.mod; });
    }

    function render() {
      if (!results.length) {
        dropdown.innerHTML = '<div class="dropdown-no-results">No modules found</div>';
        return;
      }
      dropdown.innerHTML = results.map(function (m, i) {
        // Show a description snippet only when the title alone does not
        // explain why this result matched.
        var titleMatched = tokens.some(function (t) { return m._title.indexOf(t) !== -1; });
        var extra = titleMatched ? '' :
          '<span class="dropdown-item-snippet">' + highlight(snippet(m.desc, tokens), tokens) + '</span>';
        return '<a href="' + m.url + '" class="search-dropdown-item' +
          (i === active ? ' is-active' : '') + '" style="text-decoration:none"' +
          (i === active ? ' aria-selected="true"' : '') + '>' +
          '<span class="dropdown-item-main">' +
          icon(m.icon, 'dropdown-item-icon') +
          '<span class="dropdown-item-text">' +
          '<span class="dropdown-item-title">' + highlight(m.title, tokens) + '</span>' +
          '<span class="dropdown-item-path">' + escapeHtml(m.category.toUpperCase()) + '</span>' +
          extra +
          '</span></span>' +
          icon('arrow', 'dropdown-item-arrow') +
          '</a>';
      }).join('');
    }

    function close() {
      dropdown.classList.remove('show');
      active = -1;
      input.setAttribute('aria-expanded', 'false');
    }

    function open() {
      dropdown.classList.add('show');
      input.setAttribute('aria-expanded', 'true');
    }

    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-expanded', 'false');
    dropdown.setAttribute('role', 'listbox');

    input.addEventListener('input', function (e) {
      if (!e.target.value.trim()) { close(); return; }
      results = search(e.target.value);
      active = -1;
      render();
      open();
    });

    // Full keyboard control of the result list.
    input.addEventListener('keydown', function (e) {
      var isOpen = dropdown.classList.contains('show');
      if (e.key === 'Escape') { close(); input.blur(); return; }
      if (!isOpen || !results.length) return;

      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        active += (e.key === 'ArrowDown' ? 1 : -1);
        if (active < 0) active = results.length - 1;
        if (active >= results.length) active = 0;
      } else if (e.key === 'Home') {
        e.preventDefault(); active = 0;
      } else if (e.key === 'End') {
        e.preventDefault(); active = results.length - 1;
      } else if (e.key === 'Enter') {
        e.preventDefault();
        window.location.href = results[active >= 0 ? active : 0].url;
        return;
      } else if (e.key === 'Tab') {
        close();
        return;
      } else {
        return;
      }
      render();
      var el = dropdown.children[active];
      if (el && el.scrollIntoView) el.scrollIntoView({ block: 'nearest' });
    });

    input.addEventListener('focus', function () {
      if (input.value.trim() && results.length) open();
    });

    document.addEventListener('click', function (e) {
      if (!input.parentElement.contains(e.target)) close();
    });

    // "/" focuses search, the way most docs sites behave.
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && document.activeElement !== input &&
          !/^(INPUT|TEXTAREA|SELECT)$/.test((document.activeElement || {}).tagName || '')) {
        e.preventDefault();
        input.focus();
      }
    });

    // Exposed so other page scripts (and tests) can reuse the ranking.
    window.vizlearnSearch = search;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
