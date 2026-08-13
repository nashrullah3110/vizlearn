/* GENERATED FILE - do not edit by hand.
 * Rebuild: python3 tools/build_pwa.py
 *
 * The site is entirely static, so the caching rules can be simple and honest:
 *
 *   navigations  network first, falling back to the cached copy and then to
 *                offline.html. Content stays fresh when there is a connection
 *                and a page you have already read stays readable when there
 *                is not.
 *   assets       stale-while-revalidate, but only ever against the CURRENT
 *                cache. The lookup used to be a bare caches.match(), which
 *                searches every cache in storage - so the first load after a
 *                deploy paired the new HTML (navigations are network first)
 *                with the previous build's stylesheet, and a page using a
 *                class the old CSS had never heard of rendered unstyled. It
 *                corrected itself on the next reload, which is exactly what
 *                made it hard to believe. Scoping the match to CACHE means a
 *                hit can only ever come from this build.
 *
 * Third-party requests - analytics, ads, fonts - are not touched at all.
 */
const CACHE = 'vizlearn-33fee95a07';
const SHELL = [
  "./",
  "./index.html",
  "./practice/",
  "./offline.html",
  "./assets/vizlearn.css",
  "./assets/modules.js",
  "./assets/search.js",
  "./assets/vizlearn.js",
  "./assets/vizlearn-lab.js",
  "./assets/vizlearn-state.js",
  "./assets/vizlearn-pwa.js",
  "./assets/vizlearn-keys.js",
  "./assets/vizlearn-python.js",
  "./assets/vizlearn-js.js",
  "./assets/vizlearn-html.js",
  "./assets/vizlearn-interview.js",
  "./assets/practice-bank.js",
  "./assets/practice.js",
  "./assets/icons.js",
  "./assets/favicon.svg",
  "./assets/apple-touch-icon.png",
  "./assets/icon-192.png",
  "./assets/icon-512.png",
  "./favicon.ico"
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      // addAll fails the whole install if any single entry 404s, which would
      // leave the site with no service worker at all; add them individually.
      .then((cache) => Promise.all(
        SHELL.map((url) => cache.add(url).catch(() => null))
      ))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k.startsWith('vizlearn-') && k !== CACHE)
            .map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('message', (event) => {
  if (event.data === 'skip-waiting') self.skipWaiting();
});

function isAsset(url) {
  return url.pathname.startsWith('/assets/') ||
         url.pathname === '/favicon.ico' ||
         url.pathname === '/manifest.webmanifest';
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;   // analytics, ads, fonts

  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req)
          .then((hit) => hit || caches.match('./offline.html')))
    );
    return;
  }

  if (isAsset(url)) {
    event.respondWith(
      caches.open(CACHE).then((cache) => cache.match(req).then((hit) => {
        const network = fetch(req).then((res) => {
          cache.put(req, res.clone());
          return res;
        }).catch(() => hit);
        return hit || network;
      }))
    );
  }
});
