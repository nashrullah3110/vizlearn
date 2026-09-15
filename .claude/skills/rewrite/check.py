#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The gates the /rewrite skill has to pass, as one command.

Written for Python 3.9: the build machine runs 3.9.6 even though the articles'
runnable code runs on Pyodide's 3.12.1. No walrus in a comprehension, no match,
no `X | Y` annotations.

    python3 .claude/skills/rewrite/check.py source dsa/stacks
    python3 .claude/skills/rewrite/check.py lint   dsa/stacks
    python3 .claude/skills/rewrite/check.py fences dsa/stacks --json out.json
    python3 .claude/skills/rewrite/check.py seo    dsa/stacks
    python3 .claude/skills/rewrite/check.py all    dsa/stacks

`lint`, `seo` and `all` exit non-zero when a gate fails, so the skill cannot
report success on an article that still has defects.
"""

import argparse
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

# --------------------------------------------------------------------------
# Thresholds. Every number here was measured across the 635 shipped articles
# rather than chosen, so a rewrite is held to the site's own standard and not
# to a guess. See reference/house-voice.md for the distributions.
# --------------------------------------------------------------------------
MAX_FENCE_LINES = 40          # p90 today is 87, max 210; 294 fences exceed 40
MIN_FLESCH = 60.0             # corpus median is 56.7 ("fairly hard")
MIN_SECTIONS = 3              # build_lede.py only renders a TOC at >= 3
LONG_TOC = 10
# The lede panel is a two-column grid and its row is as tall as the taller
# column, so a short opening section beside a long contents list is blank
# space. Measured in the browser at 1440px on a 14-item list: a contents item
# costs ~38px of column and a word of opening prose buys ~2.5px, so it takes
# about 15 words per section to balance. Confirmed by measurement - the waste
# fell 452px -> 341 -> 219 -> 96 as the opener went 51 -> 101 -> 151 -> 201
# words. A `columns: 2` on the list was tried and did nothing at 17rem.
LEDE_WORDS_PER_SECTION = 15
WORD_FLOOR = 1000             # nothing on the site ships under this
SENTENCE_P90 = 34             # corpus p90 is 29; allow some headroom

# The four tells that actually appear in this corpus, with their live counts.
# A rewrite must not add to them. Generic AI-slop phrases are listed second;
# 23 of the 39 patterns checked are already absent site-wide and must stay so.
BANNED = [
    (r"\bessential(ly)?\b", "essential"),
    (r"\brobust\b", "robust"),
    (r"\bcrucial\b", "crucial"),
    (r"\bleverage\b", "leverage"),
    (r"in today's (world|digital)", "in today's world"),
    (r"\bdelve\b", "delve"),
    (r"\bdive (in|into)\b", "dive into"),
    (r"\bdeep dive\b", "deep dive"),
    (r"it('s| is) important to note", "it's important to note"),
    (r"\bin conclusion\b", "in conclusion"),
    (r"\b(furthermore|moreover)\b", "furthermore/moreover"),
    (r"\bseamless", "seamless"),
    (r"game.?chang", "game-changer"),
    (r"\bunlock(s|ing)? the\b", "unlock the"),
    (r"\bharness(ing)?\b", "harness"),
    (r"\b(plethora|myriad|realm)\b", "plethora/myriad/realm"),
    (r"\blandscape of\b", "landscape of"),
    (r"\b(pivotal|vital)\b", "pivotal/vital"),
    (r"when it comes to", "when it comes to"),
    (r"\bwhether you('re| are)\b", "whether you're"),
    (r"\bthe power of\b", "the power of"),
    (r"\bdemystif", "demystify"),
    (r"\bcutting.edge\b", "cutting-edge"),
    (r"\bever.(evolving|changing)\b", "ever-evolving"),
    (r"\bsimply put\b", "simply put"),
    (r"\bit('s| is) worth noting\b", "it's worth noting"),
    (r"\blet('s| us) (explore|take a look|examine)\b", "let's explore"),
]

# build_labs.py matches the experiments section on this; renaming the heading
# silently kills every Run button on the page.
EXP_HEADING = re.compile(
    r"(interactive exploration guide|exploration guide|guided experiment|"
    r"try this above|try it yourself|experiments to try|things to try|"
    r"experiment with the visuali|guided tour|try this|explore the visuali)",
    re.I)

FENCE = re.compile(r"```([a-z0-9+-]*)\n(.*?)```", re.S)
RUN_FENCE = re.compile(r"```([a-z]+)-run\n(.*?)```", re.S)
TAG = re.compile(r"<[^>]+>")

# Tracks whose .txt is build output. Editing it there is wiped by the next
# build; the prose lives in tools/<x>_topics.py. Measured against the repo,
# not remembered - see `source` below, which verifies rather than trusts this.
GENERATED = {
    "maths": "math_topics.py", "database": "db_topics.py",
    "computer_vision": "cv_topics.py", "machine_learning": "ml_topics.py",
    "deep_learning": "dl_topics.py", "python": "python_topics.py",
    "pydantic": "pydantic_topics.py", "fastapi": "fastapi_topics.py",
    "numpy": "numpy_topics.py", "pandas": "pandas_topics.py",
    "matplotlib": "matplotlib_topics.py", "sklearn": "sklearn_topics.py",
}
ARCH = ("arch_cv.py", "arch_nlp.py", "arch_dl.py")

FAILURES = []


def fail(gate, msg):
    FAILURES.append((gate, msg))
    print("  FAIL [%s] %s" % (gate, msg))


def ok(gate, msg):
    print("  ok   [%s] %s" % (gate, msg))


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def txt_path(rel):
    track, slug = rel.split("/", 1)
    return os.path.join(ROOT, "content", "articles", track, slug + ".txt")


def read(rel):
    p = txt_path(rel)
    if not os.path.exists(p):
        sys.exit("no article file: %s" % p)
    return io.open(p, encoding="utf-8").read()


def sections(src):
    """[(heading, body)] for the ## sections, code fences left in place."""
    out = []
    for part in re.split(r"^## ", src, flags=re.M)[1:]:
        lines = part.splitlines()
        out.append((lines[0].strip(), "\n".join(lines[1:])))
    return out


def prose_of(body):
    """Body text with fences, tags and table rows removed."""
    body = FENCE.sub(" ", body)
    body = TAG.sub(" ", body)
    return "\n".join(l for l in body.splitlines() if not l.startswith("|"))


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1:
        n -= 1
    return max(1, n)


def flesch(text):
    sents = [x for x in re.split(r"(?<=[.!?])\s+", text) if len(x.split()) > 2]
    words = [w for w in text.split() if re.search(r"[a-z]", w, re.I)]
    if len(sents) < 5 or len(words) < 100:
        return None
    syl = sum(syllables(w) for w in words)
    return (206.835 - 1.015 * (len(words) / len(sents))
            - 84.6 * (syl / len(words)))


def rendered_words(rel):
    """Word count the way the site counts it (editors excluded)."""
    try:
        import prose
        import wordcount
        entry = prose.load(ROOT).get(rel + ".html")
        if entry:
            return wordcount.count(entry)
    except Exception:
        pass
    src = read(rel)
    return len(prose_of(src).split())


# --------------------------------------------------------------------------
# G1  source resolution
# --------------------------------------------------------------------------

def cmd_source(rel):
    """Say which file and which literal actually feed this page.

    This is gate one because getting it wrong is silent: the rewrite renders
    correctly, survives until the next `npm run build`, and is then gone.
    """
    track, slug = rel.split("/", 1)
    tools = os.path.join(ROOT, "tools")
    print("article : %s" % rel)

    # An arch module can live inside an otherwise hand-written track, so check
    # the three arch files by slug before trusting the per-track rule.
    for name in ARCH:
        p = os.path.join(tools, name)
        if os.path.exists(p) and ('"%s"' % slug) in io.open(p, encoding="utf-8").read():
            print("source  : tools/%s   (entry(...) for %r)" % (name, slug))
            print("EDIT    : the article= argument of that entry call")
            print("note    : content/articles/%s.txt is BUILD OUTPUT" % rel)
            return 0

    gen = GENERATED.get(track)
    if gen and os.path.exists(os.path.join(tools, gen)):
        src = io.open(os.path.join(tools, gen), encoding="utf-8").read()
        if ('"%s"' % slug) in src:
            print("source  : tools/%s   (topic(...) for %r)" % (gen, slug))
            # python's article literal is only the first third of what ships:
            # python_extra.py appends the rest via add() and then extend().
            extra = os.path.join(tools, "%s_extra.py" % track)
            if os.path.exists(extra):
                es = io.open(extra, encoding="utf-8").read()
                has_add = ('add("%s"' % slug) in es
                has_ext = ('extend("%s"' % slug) in es
                if has_add or has_ext:
                    print("        + tools/%s_extra.py  (add=%s extend=%s)"
                          % (track, has_add, has_ext))
                    print("EDIT    : append with a NEW extend(%r, ...) at the"
                          % slug)
                    print("          END of %s_extra.py - the topic() literal"
                          % track)
                    print("          is only the FIRST part of the article." )
                    print("note    : content/articles/%s.txt is BUILD OUTPUT" % rel)
                    return 0
            print("EDIT    : the article= argument of that topic call")
            print("note    : content/articles/%s.txt is BUILD OUTPUT" % rel)
            return 0

    p = txt_path(rel)
    if os.path.exists(p):
        print("source  : content/articles/%s.txt   (hand-written)" % rel)
        print("EDIT    : that file directly")
        return 0
    print("source  : UNKNOWN - do not guess, inspect before editing")
    return 1


# --------------------------------------------------------------------------
# G2-G7  static gates
# --------------------------------------------------------------------------

def cmd_lint(rel, baseline=None):
    src = read(rel)
    secs = sections(src)
    body_all = prose_of(src)
    print("lint %s" % rel)

    # --- structure -----------------------------------------------------
    if len(secs) < MIN_SECTIONS:
        fail("toc", "%d sections; build_lede.py needs >= %d for a contents list"
             % (len(secs), MIN_SECTIONS))
    else:
        ok("toc", "%d sections" % len(secs))

    if not secs:
        return 1

    head0, body0 = secs[0]
    lede_words = len(prose_of(body0).split())
    if head0.strip().lower() in ("overview", "introduction", "intro"):
        fail("lede", "first section is named %r - build_lede.py adds its own "
                     "'Overview' heading, so the page shows the label twice"
             % head0)
    need = LEDE_WORDS_PER_SECTION * len(secs)
    if len(secs) >= LONG_TOC and lede_words < need:
        fail("lede", "first section is %d words beside a %d-item contents "
                     "list; the grid row follows the taller column, so this "
                     "leaves roughly %dpx of blank space. Need >= %d words."
             % (lede_words, len(secs),
                max(0, int(38 * len(secs) - 2.5 * lede_words)), need))
    else:
        ok("lede", "first section %d words for %d sections (need %d)"
           % (lede_words, len(secs), need if len(secs) >= LONG_TOC else 0))

    # --- the experiments section drives real Run buttons ---------------
    exp = [(h, b) for h, b in secs if EXP_HEADING.search(h)]
    if exp:
        # build_labs.py's TERM_SPLIT reads the RENDERED html, so a control name
        # is valid written either as **bold** or as raw <strong> - most of the
        # seeded articles use the latter.
        controls = (re.findall(r"\*\*(.+?)\*\*", exp[0][1])
                    + re.findall(r"<strong\b[^>]*>(.+?)</strong>", exp[0][1]))
        if not controls:
            fail("labs", "experiments section has no bold control names "
                         "(**bold** or <strong>), so build_labs.py can "
                         "resolve no presets and every Run button dies")
        else:
            ok("labs", "experiments section %r with %d bold control names"
               % (exp[0][0], len(controls)))
    else:
        ok("labs", "no experiments section (not every page has one)")

    # --- code ----------------------------------------------------------
    runs = list(RUN_FENCE.finditer(src))
    plain = [m for m in FENCE.finditer(src) if not m.group(1).endswith("-run")]
    long_runs = []
    for i, m in enumerate(runs, 1):
        n = len(m.group(2).rstrip().splitlines())
        if n > MAX_FENCE_LINES:
            long_runs.append((i, n))
    if long_runs:
        for i, n in long_runs:
            fail("fence", "runnable fence %d is %d lines (max %d) - split it "
                          "into stages that each run on their own"
                 % (i, n, MAX_FENCE_LINES))
    elif runs:
        ok("fence", "%d runnable fences, longest %d lines"
           % (len(runs), max(len(m.group(2).rstrip().splitlines()) for m in runs)))
    else:
        ok("fence", "no runnable fences")
    for m in plain:
        n = len(m.group(2).rstrip().splitlines())
        if n > MAX_FENCE_LINES:
            fail("fence", "a static ```%s block is %d lines (max %d)"
                 % (m.group(1) or "text", n, MAX_FENCE_LINES))

    track = rel.split("/")[0]
    try:
        import runnable_specs
        if runs and track not in runnable_specs.resolve():
            fail("fence", "track %r has no runnable_specs entry, so a "
                          "```*-run fence renders as static code" % track)
    except Exception:
        pass

    # --- voice ---------------------------------------------------------
    score = flesch(body_all)
    if score is None:
        ok("read", "too short to score")
    elif score < MIN_FLESCH:
        fail("read", "Flesch reading ease %.1f (need >= %.0f)" % (score, MIN_FLESCH))
    else:
        ok("read", "Flesch reading ease %.1f" % score)
    if baseline is not None and score is not None and score < baseline - 0.5:
        fail("read", "readability went DOWN: %.1f vs baseline %.1f"
             % (score, baseline))

    low = body_all.lower()
    hits = []
    for pat, label in BANNED:
        n = len(re.findall(pat, low))
        if n:
            hits.append((label, n))
    if hits:
        for label, n in sorted(hits, key=lambda x: -x[1]):
            fail("voice", "banned phrase %r x%d" % (label, n))
    else:
        ok("voice", "no banned phrases")

    sents = [x for x in re.split(r"(?<=[.!?])\s+", body_all)
             if 2 < len(x.split()) < 200]
    if sents:
        lens = sorted(len(x.split()) for x in sents)
        p90 = lens[int(len(lens) * 0.9)]
        if p90 > SENTENCE_P90:
            fail("voice", "sentence length p90 is %d words (corpus p90 is 29)" % p90)
        else:
            ok("voice", "sentence length median %d, p90 %d"
               % (lens[len(lens) // 2], p90))

    if re.search(r"\bwe\b", body_all, re.I) and not re.search(r"\byou\b", body_all, re.I):
        fail("voice", "written in 'we' with no 'you'; 96%% of the corpus "
                      "addresses the reader directly")

    # --- depth ---------------------------------------------------------
    words = rendered_words(rel)
    if words < WORD_FLOOR:
        fail("depth", "%d rendered words, under the %d floor" % (words, WORD_FLOOR))
    else:
        ok("depth", "%d rendered words" % words)
    if baseline is not None:
        pass

    # --- markup --------------------------------------------------------
    # Fences are stripped first: code legitimately contains ** (an f-string
    # fill character, `**kwargs`, exponentiation), and matching across a fence
    # reports a mismatch thousands of characters away that does not exist.
    # The patterns are line-bounded for the same reason.
    nofence = FENCE.sub("\n", src)
    for bad, why in [(r"\*\*[^*\n]*</strong>", "mismatched **/<strong>"),
                     (r"<strong>[^<\n]*\*\*", "mismatched <strong>/**"),
                     (r"## .*## ", "two headings welded on one line"),
                     (r"&[a-z]+(?![a-z]*;)", "an & entity missing its ;")]:
        m = re.search(bad, nofence)
        if m:
            fail("markup", "%s: %r" % (why, m.group(0)[:60]))
    if not re.search(r"^title:", src, re.M):
        fail("markup", "no title: header line")
    if not re.search(r"^intro:", src, re.M):
        fail("markup", "no intro: header line")
    return 1 if FAILURES else 0


# --------------------------------------------------------------------------
# G6  fence extraction for the Pyodide runner
# --------------------------------------------------------------------------

def cmd_fences(rel, out):
    src = read(rel)
    track = rel.split("/")[0]
    spec = {}
    try:
        import runnable_specs
        spec = runnable_specs.resolve().get(track, {})
    except Exception as e:
        print("  (no runnable_specs: %s)" % e)
    packages = [p for p in (spec.get("packages") or "").split(",") if p]
    job = [{
        "rel": rel,
        "packages": packages,
        "prelude": spec.get("prelude") or "",
        "fences": [m.group(2) for m in RUN_FENCE.finditer(src)],
    }]
    io.open(out, "w", encoding="utf-8").write(json.dumps(job))
    print("  %d fences, packages=%s -> %s"
          % (len(job[0]["fences"]), packages or "none", out))
    return 0


# --------------------------------------------------------------------------
# G9  SEO surface
# --------------------------------------------------------------------------

def cmd_seo(rel):
    page = os.path.join(ROOT, rel + ".html")
    print("seo %s" % rel)
    if not os.path.exists(page):
        fail("seo", "page not built yet - run npm run build first")
        return 1
    s = io.open(page, encoding="utf-8").read()
    head = s[:s.find("</head>")]

    # A robots meta is NOT required: it is absent on 490 of the 667 pages and
    # the 174 that have one just restate the index,follow default. What matters
    # is that a module page never carries noindex - only /practice/, /saved/
    # and /map/ do, deliberately.
    if re.search(r'name="robots"[^>]*noindex', head):
        fail("seo", "page is noindex - it will not be indexed at all")
    else:
        ok("seo", "not noindex")

    for pat, name in [(r'<link rel="canonical"', "canonical"),
                      (r'property="og:title"', "og:title"),
                      (r'property="og:image"', "og:image"),
                      (r'name="twitter:card"', "twitter:card"),
                      (r'name="author"', "author"),
                      (r'property="article:modified_time"', "article:modified_time")]:
        if re.search(pat, head):
            ok("seo", name)
        else:
            fail("seo", "missing %s" % name)

    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', head)
    desc = m.group(1) if m else ""
    if not desc:
        fail("seo", "no meta description")
    elif "beginner-friendly interactive visualization on VizLearn" in desc:
        fail("seo", "still on the boilerplate description template (385 pages "
                    "share this frame) - add a hand-written entry to "
                    "tools/descriptions.py for %r" % rel)
    elif not (70 <= len(desc) <= 165):
        fail("seo", "description is %d chars; aim for 70-165" % len(desc))
    else:
        ok("seo", "description %d chars, hand-written" % len(desc))

    t = re.search(r"<title>(.*?)</title>", head, re.S)
    if t and len(t.group(1)) > 65:
        fail("seo", "title is %d chars; over ~60 gets truncated" % len(t.group(1)))
    elif t:
        ok("seo", "title %d chars" % len(t.group(1)))

    # FAQPage: 352 articles have a parseable Q&A section and 0 pages emit the
    # schema, so this is the one rich result the site is leaving on the table.
    src = read(rel)
    faq = [b for h, b in sections(src)
           if re.search(r"(questions people ask|common questions|faq)", h, re.I)]
    if faq:
        qs = re.findall(r"<strong>(.+?)</strong>", faq[0])
        if "FAQPage" in s:
            ok("seo", "FAQPage schema present (%d questions)" % len(qs))
        else:
            fail("seo", "%d Q&As in the article but no FAQPage JSON-LD on the "
                        "page - run faq_schema.py" % len(qs))
    else:
        fail("seo", "no 'Questions people ask' section; 352 of 635 articles "
                    "have one and it is what feeds FAQPage")

    body = s[s.find("</head>"):]
    internal = set(re.findall(r'href="\.\./([a-z_]+/[a-z0-9_-]+\.html)"', body))
    if len(internal) < 3:
        fail("seo", "only %d distinct internal cross-links in the body; a new "
                    "page reachable from nowhere does not get crawled"
             % len(internal))
    else:
        ok("seo", "%d distinct internal cross-links" % len(internal))
    for href in sorted(internal):
        if not os.path.exists(os.path.join(ROOT, href)):
            fail("seo", "broken internal link -> %s" % href)
    return 1 if FAILURES else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["source", "lint", "fences", "seo", "all"])
    ap.add_argument("article", help="track/slug, e.g. dsa/stacks")
    ap.add_argument("--json", default=os.path.join(HERE, "fences.json"))
    ap.add_argument("--baseline-flesch", type=float, default=None)
    a = ap.parse_args()
    rel = a.article.rstrip("/").replace(".html", "").replace(".txt", "")

    if a.cmd == "source":
        return cmd_source(rel)
    if a.cmd == "lint":
        return cmd_lint(rel, a.baseline_flesch)
    if a.cmd == "fences":
        return cmd_fences(rel, a.json)
    if a.cmd == "seo":
        return cmd_seo(rel)
    cmd_source(rel)
    print()
    cmd_lint(rel, a.baseline_flesch)
    print()
    cmd_seo(rel)
    print()
    if FAILURES:
        print("%d gate(s) failed:" % len(FAILURES))
        for gate, msg in FAILURES:
            print("  [%s] %s" % (gate, msg))
        return 1
    print("all static gates passed (run verify.mjs and liveness.mjs too)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
