/* VizLearn - shared page behaviour.
 *
 *   - progress tracking (which modules you have opened) in localStorage
 *   - the share menu in each module header
 *   - the cheat sheet copy button
 *
 * No backend and no login: everything lives in the visitor's own browser, the
 * same way the theme preference already did.
 */
(function () {
  'use strict';

  var PROGRESS_KEY = 'vizlearn_progress';
  var SAVED_KEY = 'vizlearn_saved';
  var SITE = 'https://vizlearn.in';

  // --- storage -------------------------------------------------------------

  function readJSON(key) {
    try {
      return JSON.parse(localStorage.getItem(key)) || {};
    } catch (e) {
      return {};
    }
  }

  function writeJSON(key, store) {
    try {
      localStorage.setItem(key, JSON.stringify(store));
      return true;
    } catch (e) {
      /* private browsing / quota - this is a nicety, never a hard failure */
      return false;
    }
  }

  function readProgress() { return readJSON(PROGRESS_KEY); }
  function writeProgress(store) { writeJSON(PROGRESS_KEY, store); }

  /* Bookmarks and notes share one record per module, because they are the
   * same gesture from the reader's side: "I want to come back to this". A
   * note implies the bookmark, so removing a bookmark that still has a note
   * keeps the note rather than throwing away something they typed. */
  function readSaved() { return readJSON(SAVED_KEY); }

  function saveEntry(path, patch) {
    if (!path) return null;
    var store = readSaved();
    var cur = store[path] || {};
    var next = {
      marked: patch.marked !== undefined ? patch.marked : !!cur.marked,
      note: patch.note !== undefined ? patch.note : (cur.note || ''),
      at: new Date().toISOString(),
      title: patch.title || cur.title || ''
    };
    if (!next.marked && !next.note) delete store[path];
    else store[path] = next;
    writeJSON(SAVED_KEY, store);
    return store[path] || null;
  }

  /** This page's catalog path ("dsa/binary_search.html"), from its canonical URL. */
  function currentPath() {
    var link = document.querySelector('link[rel="canonical"]');
    if (!link || !link.href) return null;
    var p = link.href.replace(/^https?:\/\/[^/]+\//, '');
    return p && p !== '' ? p : null;
  }

  function markVisited(path) {
    if (!path) return;
    var store = readProgress();
    var prev = store[path];
    store[path] = {
      at: new Date().toISOString(),
      n: (prev && prev.n ? prev.n : 0) + 1
    };
    writeProgress(store);
  }

  // --- icons ---------------------------------------------------------------

  var ICONS = {
    share: '<path d="M4 12v7a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7"/><path d="M16 6l-4-4-4 4"/><path d="M12 2v14"/>',
    link: '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    check: '<path d="m20 6-11 11-5-5"/>',
    x: '<path d="M4 4l16 16M20 4L4 20"/>',
    linkedin: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.01M11 17v-4a2 2 0 0 1 4 0v4"/>',
    whatsapp: '<path d="M21 12a9 9 0 0 1-13.3 7.9L3 21l1.2-4.5A9 9 0 1 1 21 12Z"/><path d="M8.5 9.5c0 3 2 5 5 5.5l1-1.5 2 1c-.5 1.5-2 2-3.5 1.5-2.5-.8-4.7-3-5.5-5.5C7 9 7.5 8 9 7.5l1 2-1.5 1Z"/>',
    reddit: '<circle cx="12" cy="13" r="8"/><circle cx="9" cy="12" r="1"/><circle cx="15" cy="12" r="1"/><path d="M9 16c1.8 1.2 4.2 1.2 6 0"/><path d="M16 5.5a1.5 1.5 0 1 0 1.4 2"/><path d="M12 5l1-3 3.5 1"/>',
    facebook: '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v7h4v-7h3l1-4h-4V8.5A.5.5 0 0 1 14.5 8Z"/>',
    phone: '<rect x="6" y="2" width="12" height="20" rx="2"/><path d="M11 18h2"/>'
  };

  function svg(name, cls) {
    return '<svg class="vz-icon ' + (cls || '') + '" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ' +
      'aria-hidden="true">' + (ICONS[name] || '') + '</svg>';
  }

  // --- toast ---------------------------------------------------------------

  var toastEl = null;
  var toastTimer = null;

  function toast(msg) {
    if (!toastEl) {
      toastEl = document.createElement('div');
      toastEl.className = 'vz-toast';
      toastEl.setAttribute('role', 'status');
      document.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('show'); }, 2200);
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text);
    }
    // Fallback for non-secure contexts, where the async clipboard is unavailable.
    return new Promise(function (resolve, reject) {
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      ok ? resolve() : reject(new Error('copy failed'));
    });
  }

  // --- share ---------------------------------------------------------------

  function shareTargets(url, title) {
    var u = encodeURIComponent(url);
    var t = encodeURIComponent(title);
    return [
      { key: 'x', label: 'X (Twitter)', icon: 'x',
        href: 'https://twitter.com/intent/tweet?url=' + u + '&text=' + t },
      { key: 'linkedin', label: 'LinkedIn', icon: 'linkedin',
        href: 'https://www.linkedin.com/sharing/share-offsite/?url=' + u },
      { key: 'whatsapp', label: 'WhatsApp', icon: 'whatsapp',
        href: 'https://api.whatsapp.com/send?text=' + t + '%20' + u },
      { key: 'reddit', label: 'Reddit', icon: 'reddit',
        href: 'https://www.reddit.com/submit?url=' + u + '&title=' + t },
      { key: 'facebook', label: 'Facebook', icon: 'facebook',
        href: 'https://www.facebook.com/sharer/sharer.php?u=' + u }
    ];
  }

  function buildShareMenu(url, title) {
    var html = '';

    // The OS share sheet is the only route to apps like Instagram, which have
    // no public web intent for sharing an arbitrary link.
    if (navigator.share) {
      html += '<button type="button" class="vz-share-item" data-share="native">' +
        svg('phone') + '<span>Share via device&hellip;</span></button>' +
        '<div class="vz-share-sep"></div>';
    }

    shareTargets(url, title).forEach(function (t) {
      html += '<a class="vz-share-item" data-share="' + t.key + '" href="' + t.href +
        '" target="_blank" rel="noopener noreferrer">' + svg(t.icon) +
        '<span>' + t.label + '</span></a>';
    });

    html += '<div class="vz-share-sep"></div>' +
      '<button type="button" class="vz-share-item" data-share="copy">' +
      svg('link') + '<span>Copy link</span></button>';

    if (!navigator.share) {
      html += '<p class="vz-share-note">For Instagram, copy the link and paste it ' +
        'into your story or bio &mdash; Instagram has no web link-share.</p>';
    }
    return html;
  }

  function initShare() {
    var wrap = document.querySelector('.vz-share-wrap');
    if (!wrap) return;

    var btn = wrap.querySelector('.vz-share-btn');
    var menu = wrap.querySelector('.vz-share-menu');
    if (!btn || !menu) return;

    var link = document.querySelector('link[rel="canonical"]');
    var url = (link && link.href) || window.location.href;
    var ogTitle = document.querySelector('meta[property="og:title"]');
    var title = (ogTitle && ogTitle.content) || document.title.replace(/^VizLearn[\s:-]*/, '');

    menu.innerHTML = buildShareMenu(url, title);

    function close() {
      menu.classList.remove('show');
      btn.setAttribute('aria-expanded', 'false');
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = menu.classList.toggle('show');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    menu.addEventListener('click', function (e) {
      var item = e.target.closest('[data-share]');
      if (!item) return;
      var kind = item.dataset.share;

      if (kind === 'native') {
        e.preventDefault();
        navigator.share({ title: title, text: title, url: url })
          .catch(function () { /* user dismissed the sheet */ });
        close();
        return;
      }

      if (kind === 'copy') {
        e.preventDefault();
        copyText(url).then(function () { toast('Link copied'); },
                           function () { toast('Could not copy link'); });
        close();
        return;
      }

      // A normal target=_blank link; just record it and let it through.
      close();
      if (typeof gtag === 'function') {
        gtag('event', 'share', { method: kind, item_id: currentPath() || url });
      }
    });

    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  }

  // --- bookmark and note ---------------------------------------------------

  function initSave() {
    var wrap = document.querySelector('.vz-save-wrap');
    if (!wrap) return;

    var btn = wrap.querySelector('.vz-save-btn');
    var menu = wrap.querySelector('.vz-save-menu');
    if (!btn || !menu) return;

    var path = currentPath();
    if (!path) return;

    var ogTitle = document.querySelector('meta[property="og:title"]');
    var title = (ogTitle && ogTitle.content) ||
        document.title.replace(/^VizLearn[\s:-]*/, '');

    menu.innerHTML =
      '<label class="vz-save-toggle">' +
        '<input type="checkbox" class="vz-save-check">' +
        '<span>Bookmark this module</span>' +
      '</label>' +
      '<label class="vz-save-note-label" for="vz-save-note">Note</label>' +
      '<textarea id="vz-save-note" class="vz-save-note" rows="4" ' +
        'placeholder="Why you came here, what to revisit&hellip;"></textarea>' +
      '<p class="vz-save-foot">Saved in this browser only. ' +
        '<a class="vz-save-link" href="">All saved</a></p>';

    var check = menu.querySelector('.vz-save-check');
    var note = menu.querySelector('.vz-save-note');
    var link = menu.querySelector('.vz-save-link');
    // Depth-independent: a module is always one directory down.
    link.setAttribute('href', '../saved/');

    function paint() {
      var e = readSaved()[path];
      check.checked = !!(e && e.marked);
      note.value = (e && e.note) || '';
      btn.classList.toggle('is-saved', !!e);
      btn.setAttribute('aria-label', e ? 'Bookmarked - edit note' :
                                         'Bookmark this module or add a note');
    }
    paint();

    function close() {
      menu.classList.remove('show');
      btn.setAttribute('aria-expanded', 'false');
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = menu.classList.toggle('show');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) note.focus();
    });

    check.addEventListener('change', function () {
      saveEntry(path, { marked: check.checked, title: title });
      paint();
      toast(check.checked ? 'Bookmarked' : 'Bookmark removed');
    });

    // Written on the way out rather than on every keystroke: one localStorage
    // write per edit instead of one per character.
    var pending = null;
    note.addEventListener('input', function () {
      clearTimeout(pending);
      pending = setTimeout(function () {
        saveEntry(path, { note: note.value.trim(), title: title });
        paint();
      }, 400);
    });

    menu.addEventListener('click', function (e) { e.stopPropagation(); });
    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
  }

  // --- cheat sheet ---------------------------------------------------------

  function initCheatSheet() {
    var sheet = document.querySelector('.vz-cheatsheet');
    if (!sheet) return;
    var btn = sheet.querySelector('[data-vz-copy]');
    if (!btn) return;

    btn.addEventListener('click', function () {
      var title = (sheet.querySelector('.vz-cheat-title') || {}).textContent || '';
      var body = (sheet.querySelector('.vz-cheat-text') || {}).textContent || '';
      var link = document.querySelector('link[rel="canonical"]');
      var url = (link && link.href) || window.location.href;

      var text = title.trim() + '\n\n' + body.trim() + '\n\n' + url;
      copyText(text).then(function () {
        toast('Cheat sheet copied');
        btn.classList.add('is-done');
        setTimeout(function () { btn.classList.remove('is-done'); }, 2000);
      }, function () {
        toast('Could not copy');
      });
    });
  }

  // --- progress ------------------------------------------------------------

  function initProgress() {
    var path = currentPath();
    // Only module pages self-mark; the hub is not a module.
    if (path && path.indexOf('/') !== -1) markVisited(path);
  }

  /** Decorate any card grid/rail on the page with visited state. */
  function decorateVisited(root) {
    var store = readProgress();
    (root || document).querySelectorAll('[data-vz-path]').forEach(function (el) {
      var p = el.dataset.vzPath;
      if (!p || !store[p]) return;
      if (el.querySelector('.vz-done-badge')) return;
      el.classList.add('is-visited');
      var badge = document.createElement('span');
      badge.className = 'vz-done-badge';
      badge.title = 'You have opened this module';
      badge.innerHTML = svg('check');
      el.appendChild(badge);
    });
  }

  // --- public surface ------------------------------------------------------

  window.VizLearn = {
    progress: readProgress,
    markVisited: markVisited,
    decorateVisited: decorateVisited,
    saved: readSaved,
    save: saveEntry,
    icon: svg,
    toast: toast,
    copyText: copyText,
    site: SITE
  };

  // --- pointer safety net --------------------------------------------------
  // The visualisations use pointer events so touch and stylus work. If the
  // browser cancels a gesture mid-drag (an interruption, a system gesture),
  // `pointerup` never arrives and the page can be left stuck mid-drag. Turning
  // a cancel into a synthetic release keeps that state machine honest.
  function initPointerCancel() {
    window.addEventListener('pointercancel', function (e) {
      var up = new PointerEvent('pointerup', {
        bubbles: true,
        cancelable: true,
        clientX: e.clientX,
        clientY: e.clientY,
        pointerId: e.pointerId,
        pointerType: e.pointerType
      });
      (e.target || window).dispatchEvent(up);
      if (e.target !== window) window.dispatchEvent(up);
    });
  }

  function boot() {
    initProgress();
    initShare();
    initSave();
    initCheatSheet();
    initPointerCancel();
    decorateVisited(document);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
