/* Service worker registration.
 *
 * Kept separate from vizlearn.js because it is the one script whose failure
 * must be completely invisible: a browser without service workers, a private
 * window that refuses to register one, or a page served from file:// should
 * all behave exactly as they did before this file existed.
 *
 * The scope root is read from the manifest link rather than hard-coded to
 * "/", so the site still works if it is ever served from a subdirectory.
 */
(function () {
  'use strict';

  if (!('serviceWorker' in navigator)) return;
  if (location.protocol !== 'https:' && location.hostname !== 'localhost' &&
      location.hostname !== '127.0.0.1') return;

  function root() {
    var link = document.querySelector('link[rel="manifest"]');
    if (link && link.href) return new URL('./', link.href).href;
    return new URL('./', location.href).href;
  }

  window.addEventListener('load', function () {
    var base = root();
    navigator.serviceWorker.register(base + 'sw.js', { scope: base })
      .then(function (reg) {
        // A new build is live: take it on the next navigation rather than
        // swapping scripts under a page that is already running.
        reg.addEventListener('updatefound', function () {
          var next = reg.installing;
          if (!next) return;
          next.addEventListener('statechange', function () {
            if (next.state === 'installed' && navigator.serviceWorker.controller) {
              next.postMessage('skip-waiting');
            }
          });
        });
      })
      .catch(function () { /* nothing here is load-bearing */ });
  });
})();
