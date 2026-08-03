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

# The app shell: what has to be present for the site to work at all, plus the
# two pages worth having available cold - the hub and practice.
SHELL = [
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
    "./assets/practice-bank.js",
    "./assets/practice.js",
    "./assets/icons.js",
    "./assets/favicon.svg",
    "./assets/apple-touch-icon.png",
    "./assets/icon-192.png",
    "./assets/icon-512.png",
    "./favicon.ico",
]

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
    "background_color": "#050505",
    "theme_color": "#050505",
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
 *   assets       stale-while-revalidate. The stylesheet and scripts are
 *                versioned by the cache name, so a stale one is never wrong
 *                for long and never blocks a paint.
 *
 * Third-party requests - analytics, ads, fonts - are not touched at all.
 */
const CACHE = 'vizlearn-%(version)s';
const SHELL = %(shell)s;

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
      caches.match(req).then((hit) => {
        const network = fetch(req).then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return res;
        }).catch(() => hit);
        return hit || network;
      })
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
<meta name="theme-color" content="#050505">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<style>
  :root { color-scheme: dark; }
  body {
    margin: 0; min-height: 100vh; display: flex; align-items: center;
    justify-content: center; background: #050505; color: #f0fdf4;
    font-family: 'Inter', system-ui, -apple-system, sans-serif; padding: 24px;
  }
  .box { max-width: 460px; text-align: center; }
  .dot {
    width: 12px; height: 12px; border-radius: 999px; background: #4ade80;
    display: inline-block; margin-right: 10px; vertical-align: 1px;
  }
  h1 { font-size: 1.6rem; margin: 0 0 4px; letter-spacing: -0.02em; }
  p { color: #86efac; line-height: 1.65; font-size: 0.95rem; }
  a {
    display: inline-block; margin-top: 18px; padding: 10px 18px;
    border: 1px solid rgba(74, 222, 128, 0.35); border-radius: 8px;
    color: #4ade80; text-decoration: none; font-size: 0.8rem;
    text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700;
  }
</style>
</head>
<body>
  <div class="box">
    <p style="font-size:1.3rem; font-weight:700; color:#f0fdf4; margin-bottom:18px">
      <span class="dot"></span>viz<span style="color:#86efac; font-weight:300">learn</span>
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
            "shell": json.dumps(SHELL, indent=2),
        })

    with open(OFFLINE, "w", encoding="utf-8") as fh:
        fh.write(OFFLINE_HTML)

    print("manifest + service worker : cache vizlearn-%s, %d shell entries"
          % (v, len(SHELL)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
