#!/usr/bin/env python3
"""Generate manifest.webmanifest, sw.js and offline.html.

The site is 200-odd static pages with no backend, which is the easiest thing
in the world to make work offline - and until now it did not, because there
was no manifest and no service worker. Practice mode made that a real gap:
a study page that needs a connection is a study page you cannot use on a
commute.

The cache name embeds a hash of everything precached, so a deploy that
changes any shell file invalidates the old cache instead of serving it
forever. Written whole on every build.
"""

import hashlib
import json
import os
import sys

from lib_catalog import ROOT, SITE

MANIFEST = os.path.join(ROOT, "manifest.webmanifest")
SW = os.path.join(ROOT, "sw.js")
OFFLINE = os.path.join(ROOT, "offline.html")

# What install has to fetch before the service worker is any use offline.
#
# This list used to hold everything - 2.7 MB, fetched on the first visit to
# any page, competing for bandwidth with the page the reader was actually
# looking at. Two of those megabytes were avoidable: "./" and "./index.html"
# are the same 710 KB document requested twice, and practice-bank.js is 482 KB
# for a page most readers never open.
#
# CORE is now the genuine minimum - the shell every page needs, and the
# offline fallback. Small, and worth blocking install for.
CORE = [
    "./offline.html",
    "./assets/vizlearn.css",
    "./assets/search.js",
    "./assets/vizlearn.js",
    "./assets/vizlearn-state.js",
    "./assets/vizlearn-pwa.js",
    "./assets/vizlearn-keys.js",
    "./assets/vizlearn-copy.js",
    "./assets/icons.js",
    "./assets/favicon.svg",
    "./favicon.ico",
]

# Warmed in the background once the worker is active, so nothing here delays
# the first page view. Losing the race costs nothing: the fetch handler
# caches every same-origin asset as it is used, so anything skipped here is
# stored the first time the reader needs it.
EXTRA = [
    # The hub is 710 KB of markup - the largest single document on the site,
    # and the last thing that should be blocking a service worker install.
    # Anyone who gets far enough to install the PWA has almost certainly
    # navigated to it already, and the fetch handler caches navigations.
    "./",
    "./practice/",
    "./assets/modules.js",
    "./assets/practice-bank.js",
    "./assets/practice.js",
    "./assets/vizlearn-lab.js",
    "./assets/vizlearn-glossary.js",
    "./assets/glossary.js",
    "./assets/vizlearn-python.js",
    "./assets/vizlearn-ide.js",
    "./assets/vizlearn-code.js",
    "./assets/vizlearn-js.js",
    "./assets/vizlearn-html.js",
    "./assets/vizlearn-interview.js",
    "./assets/vizlearn-ragviz.js",
    "./assets/vizlearn-cv.js",
    "./assets/vizlearn-dbq.js",
    "./assets/vizlearn-plot.js",
    "./assets/vizlearn-ml.js",
    "./assets/vizlearn-math.js",
    "./assets/vizlearn-dl.js",
    "./assets/vizlearn-rails.js",
    "./assets/apple-touch-icon.png",
    "./assets/icon-192.png",
    "./assets/icon-512.png",
]

# The cache name still has to change when anything cached changes, so the
# hash covers both lists.
SHELL = CORE + EXTRA

# Files whose contents decide the cache version: the ones a deploy actually
# changes. offline.html is excluded on purpose - this script writes it, so
# hashing it would make the version depend on the step's own output and the
# first run would always disagree with the second.
HASHED = [p.lstrip("./") for p in SHELL
          if p not in ("./", "./practice/", "./offline.html")
          and not p.endswith(".png") and not p.endswith(".ico")]


def version():
    h = hashlib.sha256()
    for rel in sorted(HASHED):
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            h.update(rel.encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()[:10]


MANIFEST_DATA = {
    "name": "VizLearn - Interactive AI & Algorithm Visualizations",
    "short_name": "VizLearn",
    "description": "Interactive visual explainers for AI, machine learning, "
                   "algorithms and the maths underneath them.",
    "start_url": "/?src=pwa",
    "scope": "/",
    "display": "standalone",
    "orientation": "any",
    "background_color": "#f0fdf4",
    "theme_color": "#f0fdf4",
    "lang": "en",
    "categories": ["education", "productivity"],
    "icons": [
        {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png",
         "purpose": "any"},
        {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png",
         "purpose": "any"},
        {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png",
         "purpose": "maskable"},
    ],
    "shortcuts": [
        {"name": "Practice", "short_name": "Practice", "url": "/practice/",
         "description": "Spaced practice from the modules you have opened"},
    ],
}

SW_TEMPLATE = """/* GENERATED FILE - do not edit by hand.
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
const CACHE = 'vizlearn-%(version)s';
const CORE = %(core)s;
const EXTRA = %(extra)s;

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      // addAll fails the whole install if any single entry 404s, which would
      // leave the site with no service worker at all; add them individually.
      .then((cache) => Promise.all(
        CORE.map((url) => cache.add(url).catch(() => null))
      ))
      .then(() => self.skipWaiting())
  );
});

// The optional half, fetched once the worker is running and out of the way of
// whatever page the reader opened. Deliberately not inside waitUntil: if the
// browser stops the worker before this finishes, the fetch handler caches
// each of these the first time it is actually asked for.
function warmExtras() {
  caches.open(CACHE).then((cache) => EXTRA.reduce(
    (chain, url) => chain.then(() => cache.match(url)
      .then((hit) => hit || cache.add(url).catch(() => null))),
    Promise.resolve()
  ));
}

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((k) => k.startsWith('vizlearn-') && k !== CACHE)
            .map((k) => caches.delete(k))
      ))
      .then(() => self.clients.claim())
      .then(warmExtras)
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
"""

OFFLINE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Offline | VizLearn</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#f0fdf4">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<style>
  :root { color-scheme: light; }
  body {
    margin: 0; min-height: 100vh; display: flex; align-items: center;
    justify-content: center; background: #f0fdf4; color: #052e16;
    font-family: 'Inter', system-ui, -apple-system, sans-serif; padding: 24px;
  }
  .box { max-width: 460px; text-align: center; }
  .dot {
    width: 12px; height: 12px; border-radius: 999px; background: #15803d;
    display: inline-block; margin-right: 10px; vertical-align: 1px;
  }
  h1 { font-size: 1.6rem; margin: 0 0 4px; letter-spacing: -0.02em; }
  p { color: #374151; line-height: 1.65; font-size: 0.95rem; }
  a {
    display: inline-block; margin-top: 18px; padding: 10px 18px;
    border: 1px solid rgba(22, 163, 74, 0.35); border-radius: 8px;
    color: #15803d; text-decoration: none; font-size: 0.8rem;
    text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700;
  }
</style>
</head>
<body>
  <div class="box">
    <p style="font-size:1.3rem; font-weight:700; color:#052e16; margin-bottom:18px">
      <span class="dot"></span>viz<span style="color:#374151; font-weight:300">learn</span>
    </p>
    <h1>You are offline</h1>
    <p>This page has not been opened on this device yet, so there is no copy to
    read. Modules you have already visited still work, and so does practice
    &mdash; both were saved as you went.</p>
    <a href="/practice/">Go to practice</a>
  </div>
</body>
</html>
"""


def main():
    v = version()

    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(MANIFEST_DATA, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    with open(SW, "w", encoding="utf-8") as fh:
        fh.write(SW_TEMPLATE % {
            "version": v,
            "core": json.dumps(CORE, indent=2),
            "extra": json.dumps(EXTRA, indent=2),
        })

    with open(OFFLINE, "w", encoding="utf-8") as fh:
        fh.write(OFFLINE_HTML)

    print("manifest + service worker : cache vizlearn-%s, %d shell entries"
          % (v, len(SHELL)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
