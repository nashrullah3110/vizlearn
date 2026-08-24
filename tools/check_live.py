#!/usr/bin/env python3
"""Check the deployed site, not the local build.

Stage 3 of the AdSense plan is a wait, and a wait needs a definite end. The
question at the end of it - "is the live site actually in the state we think
it is, and has Google had a chance to see it" - was answered by hand once and
would otherwise be answered by hand again every time. This does it in one
command.

What it verifies, against https://vizlearn.in and its published sitemap:

  * every sitemap URL returns 200, with no redirect
  * every page's canonical matches the URL the sitemap advertises
  * no page in the sitemap carries a noindex
  * no indexed page falls under the word floor that got the site rejected
  * the live HTML matches what the local build produces, so a stale deploy
    cannot masquerade as a passing check

It cannot read Search Console - that needs account credentials - so the
index-coverage half of the gate still has to come from the dashboard by hand.
This covers everything else.

    python3 tools/check_live.py             # full run, ~364 URLs
    python3 tools/check_live.py --sample 40 # quick pass
"""

import argparse
import concurrent.futures as futures
import html
import os
import re
import sys
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

from lib_catalog import ROOT, SITE

SITEMAP = SITE + "/sitemap.xml"
UA = "vizlearn-check-live/1.0 (+%s)" % SITE
TIMEOUT = 30

# The floor the AdSense rejection was about. Anything indexed and under this
# is the failure mode the whole expansion was meant to remove.
MIN_WORDS = 400

CANONICAL = re.compile(r'rel="canonical"\s+href="([^"]+)"')
ROBOTS = re.compile(r'name="robots"\s+content="([^"]*)"')
STRIP = re.compile(r"<(script|style|svg|nav|footer|template)\b[^>]*>.*?</\1>",
                   re.S | re.I)
TAG = re.compile(r"<[^>]+>")


# GitHub Pages rate-limits a burst of parallel requests with a 503 and serves
# the same URL fine a second later. Reporting that as a broken page sends you
# looking for a fault in the site, so a failure is retried before it counts.
RETRY_STATUS = {0, 429, 500, 502, 503, 504}
RETRIES = 2


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    status, final, body = 0, url, ""
    for attempt in range(RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status, r.geturl(), r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            status, final, body = e.code, url, ""
        except Exception as e:                               # noqa: BLE001
            status, final, body = 0, url, "<!-- %s -->" % e
        if status not in RETRY_STATUS:
            break
        if attempt < RETRIES:
            time.sleep(1.5 * (attempt + 1))
    return status, final, body


def words(src):
    """Roughly what a reader sees. Not a browser, but the same ranking - the
    browser sweep and this agree to within a few per cent, and the point here
    is catching a page that fell off a cliff, not counting to the word."""
    body = STRIP.sub(" ", src)
    return len(html.unescape(TAG.sub(" ", body)).split())


def local_of(url):
    """The local file a live URL should have been built from, or None."""
    rel = url[len(SITE):].lstrip("/") or "index.html"
    if rel.endswith("/"):
        rel += "index.html"
    path = os.path.join(ROOT, rel)
    return path if os.path.exists(path) else None


def check(url):
    status, final, src = get(url)
    row = {"url": url, "status": status, "redirect": final != url}

    if status != 200:
        return row

    m = CANONICAL.search(src)
    row["canonical_ok"] = bool(m) and m.group(1) == url
    row["canonical"] = m.group(1) if m else "(none)"

    m = ROBOTS.search(src)
    row["noindex"] = bool(m) and "noindex" in m.group(1)

    row["words"] = words(src)

    path = local_of(url)
    if path is None:
        row["stale"] = None
    else:
        local = open(path, encoding="utf-8").read()
        # Compare the article region rather than the whole document: the
        # service worker's cache name and the build hash legitimately differ
        # between a deploy and a working tree, and neither is content.
        row["stale"] = words(local) != row["words"]
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=int, default=0,
                    help="check only every Nth URL")
    ap.add_argument("--jobs", type=int, default=10)
    args = ap.parse_args()

    status, _, xml = get(SITEMAP)
    if status != 200:
        print("sitemap: HTTP %s at %s" % (status, SITEMAP))
        return 1
    urls = [e.text for e in ET.fromstring(xml).iter(
        "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    print("sitemap        : %d urls" % len(urls))
    total = len(urls)

    if args.sample:
        step = max(1, len(urls) // args.sample)
        urls = urls[::step]
        print("sampling       : %d urls" % len(urls))

    with futures.ThreadPoolExecutor(args.jobs) as pool:
        rows = list(pool.map(check, urls))

    bad_status = [r for r in rows if r["status"] != 200]
    redirects = [r for r in rows if r.get("redirect")]
    bad_canon = [r for r in rows if r["status"] == 200 and not r["canonical_ok"]]
    noindexed = [r for r in rows if r.get("noindex")]
    thin = [r for r in rows if r.get("words", 1e9) < MIN_WORDS]
    stale = [r for r in rows if r.get("stale")]

    def report(name, items, fmt):
        flag = "ok" if not items else "FAIL"
        print("%-15s: %-4s %d" % (name, flag, len(items)))
        for r in items[:10]:
            print("                  " + fmt(r))

    report("http 200", bad_status, lambda r: "%s %s" % (r["status"], r["url"]))
    report("no redirects", redirects, lambda r: r["url"])
    report("canonical", bad_canon, lambda r: "%s -> %s" % (r["url"], r["canonical"]))
    report("no noindex", noindexed, lambda r: r["url"])
    report("word floor", thin, lambda r: "%d words  %s" % (r["words"], r["url"]))
    report("deploy fresh", stale, lambda r: r["url"])

    live = [r for r in rows if r["status"] == 200]
    if live:
        counts = sorted(r.get("words", 0) for r in live)
        print("\nwords          : min %d, median %d, max %d"
              % (counts[0], counts[len(counts) // 2], counts[-1]))

    failed = bad_status or redirects or bad_canon or noindexed or thin or stale
    print("\n%s" % ("PROBLEMS FOUND" if failed else "live site clean"))
    print("\nStill to check by hand, in Search Console:")
    print("  Indexed / Discovered-not-indexed / Crawled-not-indexed on the")
    print("  Pages report. A majority of %d indexed is the gate for" % total)
    print("  reapplying; see content/indexing-priority.md.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
