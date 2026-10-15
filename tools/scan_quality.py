#!/usr/bin/env python3
"""Measure every page the way a JavaScript-running crawler sees it, and tier
the modules for the AdSense re-application.

Read-only: it changes no page. It writes two files:

    content/tiers.json          per-module tier + the numbers behind it, the
                                input the indexing step reads
    content/quality-report.md   the site-wide findings, for a person to read

Pages are rendered in Chromium (tools/scan_render.js) because most of what a
reviewer's crawler objects to only exists after the scripts run: the homepage
catalogue is drawn from modules.js, and the glossary cards that bleed into the
prose are inserted by vizlearn-glossary.js. Reading the HTML files alone would
miss both.

    python3 tools/scan_quality.py            render everything, then score
    python3 tools/scan_quality.py --reuse    score the last render again
                                             (for tuning the thresholds)

Needs Playwright for Node, resolved from the global install.
"""

import argparse
import datetime as dt
import functools
import hashlib
import http.server
import json
import os
import re
import subprocess
import sys
import threading
from collections import Counter, defaultdict

from lib_catalog import DIR_META, ROOT, modules

CACHE = os.path.join(ROOT, "_verify", "render.json")  # _verify/ is gitignored
TIERS = os.path.join(ROOT, "content", "tiers.json")
REPORT = os.path.join(ROOT, "content", "quality-report.md")

# ---------------------------------------------------------------- thresholds
# Tier 1 is the set kept indexable and carrying the ad script during review.
# These are the only knobs; change them and rerun with --reuse.
TIER1_MIN_PROSE = 800       # words of article prose, code/tables/figures excluded
BORDERLINE_MIN_PROSE = 650  # reported separately: an edit away from Tier 1
TIER1_MAX_SHARED = 0.20     # max share of prose paragraphs also found on 3+ other pages
BOILERPLATE_SHARE = 0.05    # a heading on more than 5% of modules counts as template
SHARED_PARA_PAGES = 3       # a paragraph this many pages repeat is template text
SHARED_PARA_MIN_WORDS = 20

SKIP_DIRS = {"node_modules", "tools", "_verify", ".git", "assets", "content"}
LAB_DIRS = {"python-lab", "sql-lab", "js-lab", "html-lab", "pydantic-lab", "fastapi-lab", "notebook"}
UTILITY_DIRS = {"saved", "practice", "map", "glossary", "whats-new"}
TRUST_PAGES = {"about.html", "contact.html", "privacy.html", "terms.html", "author.html"}
SYSTEM_PAGES = {"404.html", "offline.html"}

WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’.-]*")


def words(s):
    return len(WORD.findall(s or ""))


def norm(s):
    return " ".join(WORD.findall((s or "").lower()))


# ---------------------------------------------------------------- discovery
def all_html():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for f in filenames:
            if f.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, f), ROOT).replace(os.sep, "/"))
    return sorted(out)


def kind_of(path, module_paths):
    if path in module_paths:
        return "module"
    if path == "index.html":
        return "home"
    top = path.split("/")[0]
    if path in TRUST_PAGES:
        return "trust"
    if path in SYSTEM_PAGES:
        return "system"
    if top in LAB_DIRS:
        return "lab"
    if top in UTILITY_DIRS:
        return "utility"
    if path.endswith("/index.html") and top in DIR_META:
        return "hub"
    return "other"


# ---------------------------------------------------------------- rendering
def render(pages):
    handler = functools.partial(_QuietHandler, directory=ROOT)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d/" % server.server_address[1]
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    listing = CACHE + ".pages"
    with open(listing, "w") as fh:
        json.dump(pages, fh)
    env = dict(os.environ)
    try:
        groot = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        env["NODE_PATH"] = os.pathsep.join(p for p in (env.get("NODE_PATH"), groot) if p)
    except OSError:
        pass
    print("rendering %d pages in Chromium..." % len(pages), file=sys.stderr)
    try:
        subprocess.run(
            ["node", os.path.join(ROOT, "tools", "scan_render.js"), base, listing, CACHE],
            check=True, env=env,
        )
    finally:
        server.shutdown()
        os.remove(listing)


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


# ---------------------------------------------------------------- scoring
def shingles(text, n=5):
    w = norm(text).split()
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def copied(answer, page_text, page_shingles):
    """True when an end-of-module answer is the page's own prose again."""
    a = norm(answer)
    if words(a) < 8:
        return False
    if a in page_text:
        return True
    sh = shingles(answer)
    return bool(sh) and len(sh & page_shingles) / len(sh) >= 0.8


def label_share(pre):
    """Share of the words before the article that sit on 1-3 word lines:
    control labels, readout values, keyboard hints, the TOC."""
    lines = [l.strip() for l in pre.split("\n") if l.strip()]
    total = sum(words(l) for l in lines)
    short = sum(words(l) for l in lines if words(l) <= 3)
    return (short / total if total else 0.0), total


def para_key(p):
    return hashlib.sha1(norm(p).encode()).hexdigest()


def score(rows, kinds, today):
    mods = [r for r in rows if kinds[r["path"]] == "module" and not r.get("failed")]
    n_mod = max(1, len(mods))

    heading_pages = Counter()
    for r in mods:
        for h in set(r.get("articleH2", [])):
            heading_pages[h] += 1
    boiler = {h for h, c in heading_pages.items() if c / n_mod > BOILERPLATE_SHARE}

    para_pages = defaultdict(set)
    para_text = {}
    for r in mods:
        for p in r.get("proseParas", []):
            if words(p) >= SHARED_PARA_MIN_WORDS:
                k = para_key(p)
                para_pages[k].add(r["path"])
                para_text.setdefault(k, p)
    shared = {k for k, s in para_pages.items() if len(s) >= SHARED_PARA_PAGES}

    out = {}
    for r in rows:
        path = r["path"]
        errs = r.get("errors", [])
        # The scan cannot reach the library CDNs, so "Chart is not defined"
        # on a page that loads Chart.js from one is the scan, not the site.
        lib_errs = [e for e in errs if r.get("blockedLibs") and re.search(r"\b(Chart|THREE|MathJax)\b", e)]
        m = {"kind": kinds[path], "status": r.get("status"),
             "jsErrors": [e for e in errs if e not in lib_errs], "libErrors": lib_errs}
        if r.get("failed"):
            m["failed"] = True
            out[path] = m
            continue
        page_text = norm(r.get("lede", "") + " " + r.get("prose", ""))
        page_sh = shingles(page_text)
        answers = r.get("checkAnswers", [])
        dup = sum(1 for a in answers if copied(a, page_text, page_sh))
        cheat_dup = bool(r.get("cheatText")) and copied(r["cheatText"], page_text, page_sh)
        ls, pre_words = label_share(r.get("preArticle", ""))
        paras = [p for p in r.get("proseParas", []) if words(p) >= SHARED_PARA_MIN_WORDS]
        shared_n = sum(1 for p in paras if para_key(p) in shared)

        bad_dates = []
        for d in r.get("dates", []):
            v = (d.get("value") or "")[:10]
            try:
                when = dt.date.fromisoformat(v)
            except ValueError:
                bad_dates.append("%s unparseable: %r" % (d["field"], d.get("value")))
                continue
            if when > today:
                bad_dates.append("%s in the future: %s" % (d["field"], v))
        pub = [d["value"][:10] for d in r.get("dates", []) if "ublished" in d["field"]]
        mod = [d["value"][:10] for d in r.get("dates", []) if "odified" in d["field"]]
        if pub and mod and min(mod) < max(pub):
            bad_dates.append("modified %s before published %s" % (min(mod), max(pub)))

        m.update({
            "hasArticle": r.get("hasArticle", False),
            "proseWords": r.get("proseWords", 0),
            "ledeWords": words(r.get("lede", "")),
            "worked": {"tables": r.get("hasTable", 0), "code": r.get("hasCode", 0), "math": r.get("hasMath", 0)},
            "glossaryCards": r.get("glossaryCards", 0),
            "glossaryHiddenChars": r.get("glossaryHiddenChars", 0),
            "checkTitle": r.get("checkTitle", ""),
            "checkAnswers": len(answers),
            "checkAnswersCopied": dup,
            "cheatSheetCopied": cheat_dup,
            "boilerplateHeadings": sorted(h for h in set(r.get("articleH2", [])) if h in boiler),
            "sharedParas": shared_n,
            "sharedParaShare": round(shared_n / len(paras), 2) if paras else 0.0,
            "preArticleWords": pre_words,
            "preArticleLabelShare": round(ls, 2),
            "links": r.get("links", 0),
            "uniqueLinks": r.get("uniqueLinks", 0),
            "bodyWords": r.get("bodyWords", 0),
            "longParas": r.get("longParas", 0),
            "badDates": bad_dates,
            "robots": r.get("robots", ""),
            "adsense": r.get("adsense", False),
            "ldTypes": sorted(set(r.get("ldTypes", []))),
        })
        if m["kind"] == "module":
            m["tier"], m["why"] = tier(m)
        out[path] = m
    return out, heading_pages, boiler, {k: (para_text[k], sorted(para_pages[k])) for k in shared}


def tier(m):
    if m.get("status") != 200:
        return 2, "did not load (HTTP %s)" % m.get("status")
    if not m["hasArticle"]:
        return 2, "no written article on the page (no .vz-article)"
    w = m["proseWords"]
    worked = sum(m["worked"].values())
    reasons = []
    if w < TIER1_MIN_PROSE:
        reasons.append("%d prose words (< %d)" % (w, TIER1_MIN_PROSE))
    if not worked:
        reasons.append("no table, code or worked maths in the article")
    if m["sharedParaShare"] > TIER1_MAX_SHARED:
        reasons.append("%d%% of paragraphs repeated on other pages" % round(100 * m["sharedParaShare"]))
    if reasons:
        return 2, "; ".join(reasons)
    return 1, "%d prose words, %d worked-example elements" % (w, worked)


# ---------------------------------------------------------------- report
def pct(a, b):
    return "%d%%" % round(100 * a / b) if b else "-"


def write_report(scored, rows_by_path, heading_pages, boiler, shared, today):
    mods = {p: m for p, m in scored.items() if m["kind"] == "module" and not m.get("failed")}
    n = len(mods)
    t1 = sorted((p for p, m in mods.items() if m["tier"] == 1), key=lambda p: -mods[p]["proseWords"])
    t2 = sorted((p for p, m in mods.items() if m["tier"] == 2), key=lambda p: -mods[p]["proseWords"])
    border = [p for p in t2 if mods[p]["proseWords"] >= BORDERLINE_MIN_PROSE]
    L = []
    a = L.append

    a("# Site quality scan - %s" % today.isoformat())
    a("")
    a("Generated by `python3 tools/scan_quality.py`. Read-only: nothing on the site was changed.")
    a("Every page was rendered in Chromium, so these numbers include what the scripts add")
    a("(the homepage catalogue, glossary cards), which is what Google's crawler sees too.")
    a("")
    a("## Summary")
    a("")
    a("| | |")
    a("|---|---|")
    a("| Pages scanned | %d |" % len(scored))
    for k in ("module", "hub", "home", "lab", "utility", "trust", "system", "other"):
        c = sum(1 for m in scored.values() if m["kind"] == k)
        if c:
            a("| %s pages | %d |" % (k, c))
    failed = [p for p, m in scored.items() if m.get("failed") or m.get("status") != 200]
    a("| Failed to load | %d |" % len(failed))
    a("| **Tier 1 modules** (index + ads during review) | **%d** |" % len(t1))
    a("| Tier 2 modules (noindex during review) | %d |" % len(t2))
    a("| of which borderline (%d-%d prose words) | %d |" % (BORDERLINE_MIN_PROSE, TIER1_MIN_PROSE - 1, len(border)))
    a("")
    a("Tier 1 rule: at least %d words of article prose (code, tables, the code lab and" % TIER1_MIN_PROSE)
    a("glossary cards excluded), at least one table, code block or worked formula, and no more")
    a("than %d%% of its paragraphs repeated on %d+ other pages. Thresholds are constants at the" % (100 * TIER1_MAX_SHARED, SHARED_PARA_PAGES))
    a("top of the script; change them and rerun with `--reuse`.")
    a("")

    # prose distribution
    buckets = [(0, 400), (400, 650), (650, 800), (800, 1200), (1200, 2000), (2000, 10 ** 9)]
    a("### Article prose length, all modules")
    a("")
    a("| Prose words | Modules |")
    a("|---|---|")
    for lo, hi in buckets:
        c = sum(1 for m in mods.values() if lo <= m["proseWords"] < hi)
        a("| %s | %d |" % ("%d+" % lo if hi > 10 ** 8 else "%d-%d" % (lo, hi - 1), c))
    a("")

    a("### By track")
    a("")
    a("| Track | Modules | Tier 1 | Tier 2 | Median prose words |")
    a("|---|---|---|---|---|")
    by_dir = defaultdict(list)
    for p, m in mods.items():
        by_dir[p.split("/")[0]].append(m)
    for d in sorted(by_dir, key=lambda d: -len(by_dir[d])):
        ms = by_dir[d]
        ws = sorted(m["proseWords"] for m in ms)
        a("| %s | %d | %d | %d | %d |" % (DIR_META.get(d, (d,))[0], len(ms),
          sum(m["tier"] == 1 for m in ms), sum(m["tier"] == 2 for m in ms), ws[len(ws) // 2]))
    a("")

    # findings
    a("## Findings (site-wide, fixed in Stage 2-4 regardless of tier)")
    a("")
    g = [p for p, m in mods.items() if m["glossaryCards"]]
    a("### 1. Glossary text bleeding into the prose")
    a("")
    a("%d of %d modules (%s) carry hidden glossary cards inside the article - %d cards," % (
        len(g), n, pct(len(g), n), sum(mods[p]["glossaryCards"] for p in g)))
    a("%d characters of definition text in total. Read as page text, a sentence becomes:" % sum(mods[p]["glossaryHiddenChars"] for p in g))
    a("")
    for p in g[:1]:
        for s in rows_by_path[p].get("bleedSamples", [])[:2]:
            a("> `%s`" % s.replace("`", "'"))
        a("")
        a("(from `%s`)" % p)
    a("")

    c = [p for p, m in mods.items() if m["checkAnswersCopied"]]
    tot_ans = sum(m["checkAnswers"] for m in mods.values())
    tot_dup = sum(m["checkAnswersCopied"] for m in mods.values())
    titles = Counter(m["checkTitle"] for m in mods.values() if m["checkTitle"])
    cheat = sum(1 for m in mods.values() if m["cheatSheetCopied"])
    a("### 2. End-of-module answers copied from the page")
    a("")
    a("%d of %d end-of-module answers (%s) repeat the page's own prose word for word, on %d modules." % (
        tot_dup, tot_ans, pct(tot_dup, tot_ans), len(c)))
    a("The cheat-sheet summary repeats the page's prose on %d modules." % cheat)
    a("Section titles: %s." % ", ".join("\"%s\" x%d" % t for t in titles.most_common()))
    a("")

    a("### 3. Template headings")
    a("")
    a("Headings inside the article that appear on more than %d%% of modules:" % (100 * BOILERPLATE_SHARE))
    a("")
    a("| Heading | Modules |")
    a("|---|---|")
    for h, k in heading_pages.most_common():
        if h in boiler:
            a("| %s | %d |" % (h, k))
    bp = sum(1 for m in mods.values() if m["boilerplateHeadings"])
    a("")
    a("%d modules carry at least one of them." % bp)
    a("")

    a("### 4. Paragraphs repeated across pages")
    a("")
    a("%d distinct paragraphs of %d+ words appear on %d or more modules." % (len(shared), SHARED_PARA_MIN_WORDS, SHARED_PARA_PAGES))
    top = sorted(shared.values(), key=lambda v: -len(v[1]))[:8]
    if top:
        a("")
        a("| Pages | Paragraph (start) |")
        a("|---|---|")
        for text, pages in top:
            a("| %d | %s |" % (len(pages), text[:110].replace("|", "/") + "..."))
    a("")

    ls = sorted(m["preArticleLabelShare"] for m in mods.values())
    hi = [p for p, m in mods.items() if m["preArticleLabelShare"] >= 0.5]
    a("### 5. What comes before the article")
    a("")
    a("Median: %d words of text before the article starts, %d%% of them on 1-3 word lines" % (
        sorted(m["preArticleWords"] for m in mods.values())[n // 2], round(100 * ls[n // 2])))
    a("(control labels, readouts, key hints, the table of contents). %d modules are at 50%% or more." % len(hi))
    a("")

    bd = {p: m["badDates"] for p, m in scored.items() if m.get("badDates")}
    a("### 6. Dates")
    a("")
    if bd:
        a("%d pages have a date problem:" % len(bd))
        a("")
        for p, v in sorted(bd.items())[:40]:
            a("- `%s`: %s" % (p, "; ".join(v)))
    else:
        a("No date in the future, unparseable, or modified-before-published, on any page.")
    a("")

    errs = {p: m["jsErrors"] for p, m in scored.items() if m.get("jsErrors")}
    a("### 7. Load failures and script errors")
    a("")
    lib = [p for p, m in scored.items() if m.get("libErrors")]
    if lib:
        a("%d pages threw an error only because the scan could not load their library from a CDN" % len(lib))
        a("(Chart.js, three.js, MathJax - this sandbox's network blocks those hosts). Not a site bug;")
        a("listed so a rerun on an open network can confirm: %s." % ", ".join("`%s`" % p for p in lib))
        a("")
    if failed or errs:
        for p in failed:
            a("- `%s`: failed to load (status %s)" % (p, scored[p].get("status")))
        for p, e in sorted(errs.items())[:40]:
            a("- `%s`: %s" % (p, e[0]))
    else:
        a("None. Every page loaded with HTTP 200 and no uncaught script error.")
    a("")

    # non-module pages
    a("## Non-module pages")
    a("")
    a("| Page | Kind | Words | Links | Paragraphs of 2+ sentences | robots | Ad script |")
    a("|---|---|---|---|---|---|---|")
    for p, m in sorted(scored.items(), key=lambda kv: (kv[1]["kind"], kv[0])):
        if m["kind"] == "module" or m.get("failed"):
            continue
        a("| `%s` | %s | %d | %d | %d | %s | %s |" % (p, m["kind"], m["bodyWords"], m["links"],
          m["longParas"], m["robots"] or "-", "yes" if m["adsense"] else "no"))
    a("")
    trust = {p: m for p, m in scored.items() if m["kind"] in ("trust", "home")}
    a("Structured data on the trust pages and homepage:")
    a("")
    for p, m in sorted(trust.items()):
        a("- `%s`: %s" % (p, ", ".join(m["ldTypes"]) or "none"))
    a("")

    # tier lists
    a("## Borderline modules (%d)" % len(border))
    a("")
    a("Tier 2 on length alone and within %d words of the cut. Each is a short expansion away from Tier 1." % (TIER1_MIN_PROSE - BORDERLINE_MIN_PROSE))
    a("")
    a("| Module | Prose words | Why Tier 2 |")
    a("|---|---|---|")
    for p in border:
        a("| `%s` | %d | %s |" % (p, mods[p]["proseWords"], mods[p]["why"]))
    a("")
    a("## Tier 1 modules (%d)" % len(t1))
    a("")
    a("| Module | Prose words | Tables / code / maths |")
    a("|---|---|---|")
    for p in t1:
        w = mods[p]["worked"]
        a("| `%s` | %d | %d / %d / %d |" % (p, mods[p]["proseWords"], w["tables"], w["code"], w["math"]))
    a("")
    a("## Tier 2 modules (%d)" % len(t2))
    a("")
    a("| Module | Prose words | Why |")
    a("|---|---|---|")
    for p in t2:
        a("| `%s` | %d | %s |" % (p, mods[p]["proseWords"], mods[p]["why"]))
    a("")
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--reuse", action="store_true", help="score the last render without re-rendering")
    args = ap.parse_args()

    mod_paths = {m["path"] for m in modules(with_desc=False)}
    pages = all_html()
    kinds = {p: kind_of(p, mod_paths) for p in pages}
    missing = sorted(mod_paths - set(pages))
    if missing:
        print("catalog lists %d modules with no file: %s" % (len(missing), missing[:5]), file=sys.stderr)

    if not args.reuse or not os.path.exists(CACHE):
        render(pages)
    with open(CACHE, encoding="utf-8") as fh:
        rows = [r for r in json.load(fh) if r["path"] in kinds]

    today = dt.date.today()
    scored, heading_pages, boiler, shared = score(rows, kinds, today)
    rows_by_path = {r["path"]: r for r in rows}

    tiers = {
        "generated": today.isoformat(),
        "rule": {
            "tier1_min_prose_words": TIER1_MIN_PROSE,
            "tier1_needs_worked_example": True,
            "tier1_max_shared_paragraph_share": TIER1_MAX_SHARED,
        },
        "modules": {
            p: {k: m[k] for k in ("tier", "why", "proseWords", "worked", "glossaryCards",
                                  "checkAnswersCopied", "boilerplateHeadings", "sharedParaShare")}
            for p, m in sorted(scored.items()) if m["kind"] == "module" and not m.get("failed")
        },
        "pages": {p: m["kind"] for p, m in sorted(scored.items()) if m["kind"] != "module"},
    }
    with open(TIERS, "w", encoding="utf-8") as fh:
        json.dump(tiers, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    write_report(scored, rows_by_path, heading_pages, boiler, shared, today)

    t = Counter(m["tier"] for m in tiers["modules"].values())
    print("tier 1: %d   tier 2: %d   -> %s, %s" % (t[1], t[2], os.path.relpath(TIERS, ROOT), os.path.relpath(REPORT, ROOT)))


if __name__ == "__main__":
    main()
