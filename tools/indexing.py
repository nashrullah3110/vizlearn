"""Which pages Google may index, and which carry the AdSense loader.

One answer, read by every step that cares: build_seo.py writes the robots
meta and the ad script from it, build_ads.py places ad units from it,
build_sitemap.py lists URLs from it and audit.py checks all three agree.

The policy, while the site is under AdSense review:

  indexed, with ads   the homepage, the track hubs and every Tier 1 module
  indexed, no ads     about, author, contact, privacy, terms, What's New -
                      real pages, but not ones an ad belongs on
  noindex, no ads     Tier 2 modules, the seven code labs, and the app pages
                      (saved, practice, concept map, glossary): an editor, a
                      quiz queue or a list held in the reader's browser has no
                      editorial content of its own for an ad to sit beside

Tiers come from content/tiers.json, written by tools/scan_quality.py from a
rendered crawl. A module missing from it (added since the last scan) is
treated as Tier 1 and reported, so a new page is never hidden by accident -
rerun `npm run scan` to place it.

"follow" stays on every noindex page: their links are the site's own
navigation, and there is nothing to gain by telling Google not to follow
them to the modules.
"""

import json
import os

from lib_catalog import DIR_META, ROOT, modules

TIERS = os.path.join(ROOT, "content", "tiers.json")

ROBOTS_NOINDEX = "noindex, follow"

LABS = {
    "python-lab/index.html",
    "sql-lab/index.html",
    "js-lab/index.html",
    "html-lab/index.html",
    "pydantic-lab/index.html",
    "fastapi-lab/index.html",
    "notebook/index.html",
}

APP_PAGES = {
    "saved/index.html",
    "practice/index.html",
    "map/index.html",
    "glossary/index.html",
}


def _tiers():
    try:
        with open(TIERS, encoding="utf-8") as fh:
            return {p: m["tier"] for p, m in json.load(fh)["modules"].items()}
    except (OSError, ValueError, KeyError):
        return {}


_TIER = _tiers()
_MODULES = {m["path"] for m in modules(with_desc=False)}
_HUBS = {"%s/index.html" % d for d in DIR_META}


def tier(rel):
    """1 or 2 for a module, None for anything else."""
    if rel not in _MODULES:
        return None
    return _TIER.get(rel, 1)


def unscanned():
    """Modules with no entry in tiers.json, defaulted to Tier 1."""
    return sorted(_MODULES - set(_TIER))


def robots(rel):
    """The robots meta content for `rel`, or None to leave it indexable."""
    if rel in LABS or rel in APP_PAGES or tier(rel) == 2:
        return ROBOTS_NOINDEX
    return None


def indexed(rel):
    return robots(rel) is None


def ads(rel):
    """Whether `rel` loads the AdSense script and gets ad placements."""
    return rel == "index.html" or rel in _HUBS or tier(rel) == 1


def noindex_pages():
    return {p for p in _MODULES | LABS | APP_PAGES if not indexed(p)}
