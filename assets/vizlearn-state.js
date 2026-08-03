/* Shareable state URLs.
 *
 * Every module is an interactive page whose whole value is the configuration
 * you arrived at - and until now a shared link always landed on the defaults,
 * because nothing on the site ever read the URL. This syncs the page's real
 * controls with the location hash in both directions.
 *
 * Nothing here knows anything about any particular page. It finds the controls
 * the same way the lab layer does - by walking the DOM - and only ever records
 * a control whose value differs from the one the markup shipped with, so a
 * default view keeps a clean URL and a shared one carries exactly the
 * differences.
 *
 * Format:  #k-slider=3&balls-check=0&metric-select=cosine
 */
(function () {
  'use strict';

  // Controls the page owns. The search box is a text input and the theme
  // toggle is a button, so neither is picked up here.
  var SELECTOR = 'input[type="range"], input[type="checkbox"], input[type="radio"], select';

  // Anything belonging to the shared chrome rather than the visualisation.
  var SKIP_ANCESTORS = '.vz-lab, .vz-extras, .vz-footer, header, .vz-share-menu';

  var initial = {};   // id -> the value the markup shipped with
  var applying = false;

  function controls() {
    var out = [];
    var all = document.querySelectorAll(SELECTOR);
    for (var i = 0; i < all.length; i++) {
      var el = all[i];
      if (!el.id) continue;                    // nothing to name it by
      if (el.closest && el.closest(SKIP_ANCESTORS)) continue;
      out.push(el);
    }
    return out;
  }

  function valueOf(el) {
    if (el.type === 'checkbox') return el.checked ? '1' : '0';
    if (el.type === 'radio') return el.checked ? '1' : '0';
    return el.value;
  }

  function fire(el) {
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
  }

  function setValue(el, raw) {
    if (el.type === 'checkbox' || el.type === 'radio') {
      var on = raw === '1' || raw === 'true';
      if (el.checked === on) return false;
      el.checked = on;
      fire(el);
      return true;
    }
    if (el.tagName === 'SELECT') {
      // Match by value, then by visible text, because a few pages build their
      // options in JavaScript with different casing than the label shows.
      var want = String(raw).toLowerCase();
      for (var i = 0; i < el.options.length; i++) {
        var o = el.options[i];
        if (String(o.value).toLowerCase() === want ||
            String(o.textContent).trim().toLowerCase() === want) {
          if (el.selectedIndex === i) return false;
          el.selectedIndex = i;
          fire(el);
          return true;
        }
      }
      return false;
    }
    if (el.value === String(raw)) return false;
    el.value = raw;
    // A range silently clamps out-of-band values, so read back rather than
    // trusting what the URL asked for.
    if (el.value === '') return false;
    fire(el);
    return true;
  }

  // --- hash <-> state ------------------------------------------------------

  function parseHash() {
    var h = (location.hash || '').replace(/^#/, '');
    if (!h || h.indexOf('=') === -1) return null;
    var out = {};
    h.split('&').forEach(function (pair) {
      var i = pair.indexOf('=');
      if (i <= 0) return;
      out[decodeURIComponent(pair.slice(0, i))] = decodeURIComponent(pair.slice(i + 1));
    });
    return out;
  }

  function currentHash() {
    var parts = [];
    controls().forEach(function (el) {
      var v = valueOf(el);
      if (!(el.id in initial)) return;
      if (v === initial[el.id]) return;        // still the default: leave it out
      parts.push(encodeURIComponent(el.id) + '=' + encodeURIComponent(v));
    });
    return parts.join('&');
  }

  var pending = null;
  function scheduleWrite() {
    if (applying) return;
    if (pending) clearTimeout(pending);
    // Dragging a slider fires continuously; one write when it settles is
    // plenty, and replaceState keeps the back button usable.
    pending = setTimeout(function () {
      pending = null;
      var h = currentHash();
      var url = location.pathname + location.search + (h ? '#' + h : '');
      try {
        history.replaceState(null, '', url);
      } catch (e) {
        /* file:// and some embedded webviews refuse replaceState */
      }
    }, 250);
  }

  function applyHash() {
    var want = parseHash();
    if (!want) return 0;
    applying = true;
    var n = 0;
    controls().forEach(function (el) {
      if (!(el.id in want)) return;
      if (setValue(el, want[el.id])) n++;
    });
    applying = false;
    return n;
  }

  // --- copy this view ------------------------------------------------------

  function shareUrl() {
    var link = document.querySelector('link[rel="canonical"]');
    var base = (link && link.href) || (location.origin + location.pathname);
    var h = currentHash();
    return h ? base + '#' + h : base;
  }

  /* Added to the share menu the moment it is opened, so this file does not
   * have to know when vizlearn.js built it. */
  function hookShareMenu() {
    var menu = document.querySelector('.vz-share-menu');
    var btn = document.querySelector('.vz-share-btn');
    if (!menu || !btn) return;

    btn.addEventListener('click', function () {
      if (menu.querySelector('[data-share="state"]')) return;
      var copy = menu.querySelector('[data-share="copy"]');
      if (!copy) return;
      var item = document.createElement('button');
      item.type = 'button';
      item.className = 'vz-share-item';
      item.setAttribute('data-share', 'state');
      item.innerHTML = copy.innerHTML.replace(/<span>.*?<\/span>/,
        '<span>Copy link to this view</span>');
      copy.parentNode.insertBefore(item, copy.nextSibling);

      item.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var url = shareUrl();
        var done = function (msg) {
          if (window.VizLearn && window.VizLearn.toast) window.VizLearn.toast(msg);
        };
        if (window.VizLearn && window.VizLearn.copyText) {
          window.VizLearn.copyText(url).then(
            function () { done(url === shareUrl() && url.indexOf('#') !== -1
              ? 'Link to this view copied' : 'Link copied'); },
            function () { done('Could not copy link'); });
        }
        menu.classList.remove('show');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // --- boot ----------------------------------------------------------------

  function snapshotDefaults() {
    controls().forEach(function (el) {
      if (!(el.id in initial)) initial[el.id] = valueOf(el);
    });
  }

  function watch() {
    document.addEventListener('input', function (e) {
      if (e.target && e.target.id && e.target.id in initial) scheduleWrite();
    }, true);
    document.addEventListener('change', function (e) {
      if (e.target && e.target.id && e.target.id in initial) scheduleWrite();
    }, true);
  }

  function start() {
    snapshotDefaults();
    if (!Object.keys(initial).length) return;
    applyHash();
    watch();
    hookShareMenu();

    // Some pages build their controls in JavaScript after DOMContentLoaded.
    // One more pass on load picks those up, for both defaults and the hash.
    window.addEventListener('load', function () {
      var before = Object.keys(initial).length;
      snapshotDefaults();
      if (Object.keys(initial).length !== before) applyHash();
    });

    // A hash typed or pasted into an already-open page still works.
    window.addEventListener('hashchange', function () {
      if (!applying) applyHash();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }

  window.VizLearnState = { apply: applyHash, hash: currentHash, url: shareUrl };
})();
