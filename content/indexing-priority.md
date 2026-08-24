# Stage 2 — Search Console indexing priority

Companion to the AdSense re-application plan. Everything here has to be done
by hand in the Search Console UI at
<https://search.google.com/search-console> — there is no API path for it that
does not require account credentials, and Google retired the sitemap ping
endpoint in 2023.

Written 21 August 2026 against a 364-URL sitemap; revised 24 August 2026, after the CV, Database and ML tiers took it to **424**.

## What changed since this was written

The sitemap has grown from 364 URLs to 424. Sixty of those are modules Google
has never seen, because they were committed after the last crawl. That does not
change the running order below - it makes the hubs-first rule matter more, since
each track hub is now the only route to a larger set of new pages.

Re-run `npm run checklive` before submitting; it verifies the deployed site
against the published sitemap in one command.

## Pre-flight (verified 21 August 2026, re-verify with npm run checklive)

All of this was checked against the live site, not the local build:

| Check | Result |
|---|---|
| Sitemap URLs | 424, valid XML, served as `application/xml` |
| HTTP status | all return **200** — no 404s, no redirects |
| Canonical | matches the sitemap URL exactly on every one |
| `noindex` inside the sitemap | **0** |
| `robots.txt` | allows everything except `/tools/` and `/node_modules/`, and points at the sitemap |
| `lastmod` | 159 URLs at 2026-08-21, 205 at 2026-08-19 — derived from git, not blanket-stamped |
| Stage 1 deployed | confirmed live: `/whats-new/` indexable, `contact.html` expanded, ad markers present |

So there is nothing left to fix before submitting. Submit it.

## Step 1 — Resubmit the sitemap

Sitemaps → enter `sitemap.xml` → Submit. Even if it is already listed,
resubmitting re-queues discovery for the 364 URLs.

## Step 2 — Record the baseline

Pages report → write down three numbers:

- **Indexed**
- **Discovered – currently not indexed**
- **Crawled – currently not indexed**

This baseline is the whole point of stage 2. Stage 3's gate is a *majority of
424 indexed*, and that is unreadable without knowing where it started.

The distinction matters more than the total. *Discovered – not indexed* means
Google knows the URL exists and has not bothered to fetch it, which is a
crawl-budget and site-authority signal. *Crawled – not indexed* means it
fetched the page and chose not to index it, which is a content-quality
judgement — that is the bucket the thin pages would have landed in, and the
one that should shrink now that they are expanded.

## Step 3 — Request indexing, hubs first

Use URL Inspection → Request Indexing. The quota is roughly ten a day, so
this is spread over three days. **Hubs before articles**, deliberately: a
track hub links to every module in its track, so getting one hub recrawled
pulls Google toward 20–50 articles on its own. Requesting individual articles
first spends the daily quota on leaves instead of branches.

### Day 1 — the homepage and the two tracks that changed most

```
https://vizlearn.in/
https://vizlearn.in/python/
https://vizlearn.in/interview/
https://vizlearn.in/whats-new/
https://vizlearn.in/glossary/
```

`/python/` and `/interview/` lead first because those two tracks hold every
page Google still has a stale, thin copy of — the 34 expanded Python articles
and the 49 interview pages whose written answers the build had been silently
discarding. `/whats-new/` has never been crawled at all; it was `noindex`
until stage 1.

### Day 2 — the remaining track hubs

The first three lead: Computer Vision, Databases and machine learning each
gained twenty modules that have never been crawled, and their hub is the only
internal route to them.

```
https://vizlearn.in/computer_vision/
https://vizlearn.in/database/
https://vizlearn.in/machine_learning/
https://vizlearn.in/maths/
https://vizlearn.in/deep_learning/
https://vizlearn.in/dsa/
https://vizlearn.in/natural_language_processing/
https://vizlearn.in/gen_ai/
```

### Day 3 — the labs and a sample of expanded articles

The four labs went from ~270 rendered words to 690–790 and need recrawling on
their own; they are not linked from any track hub.

```
https://vizlearn.in/python-lab/
https://vizlearn.in/sql-lab/
https://vizlearn.in/js-lab/
https://vizlearn.in/html-lab/
```

Then a sample of the brand-new modules, as a spot check that the recent work is
being picked up at all:

```
https://vizlearn.in/computer_vision/convolution_kernels.html
https://vizlearn.in/computer_vision/grad_cam.html
https://vizlearn.in/database/isolation_levels.html
https://vizlearn.in/database/sql_injection_and_parameters.html
https://vizlearn.in/machine_learning/data_leakage.html
https://vizlearn.in/machine_learning/probability_calibration.html
```

## Step 4 — Set a reminder, then stop

Do not reapply to AdSense yet. Stage 3 is a wait with a gate, and the gate is
the index count, not the calendar. Come back in two weeks, re-read the Pages
report, and compare against the baseline from step 2.

The spot check that actually matters: search
`site:vizlearn.in/machine_learning/probability_calibration.html` and confirm it
appears at all — that page did not exist at the last crawl. For a page that did,
`site:vizlearn.in/python/generators_and_yield.html` should show the **expanded**
article rather than the old short one. If Google is still showing the old short
version, the index has not caught up and reapplying would be judged against
content that no longer exists.
