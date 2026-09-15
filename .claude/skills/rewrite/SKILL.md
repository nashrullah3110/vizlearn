---
name: rewrite
description: Rewrite a VizLearn article so it passes every content, code, UI, interactive, readability and AdSense/SEO gate. Use when asked to rewrite, fix, expand, improve or de-AI an article or module page, or when a page has layout defects, over-long code blocks or broken interactive elements.
---

# Rewrite a VizLearn article

Input: a page as `track/slug` (e.g. `dsa/stacks`). Output: the same page, passing
every gate below, built, verified and reported honestly.

**The bar is not "it reads better". It is: every gate green, every code block
executed in the runtime the reader gets, and its output read line by line
against its own prose.** A demonstration that runs and quietly proves nothing —
or proves the opposite of what the sentence above it claims — is the failure mode
this skill exists to prevent. It has happened repeatedly on this site: a top-k
demo where sorting beat the heap it was advertising, an LIS claim that was
outright false, `array("q")` pickling *larger* than the list it was supposed to
beat.

Run the gates, don't eyeball them:

```bash
python3 .claude/skills/rewrite/check.py all <track>/<slug>
```

`check.py` exits non-zero while any gate is red. Never report success on a red gate.

---

## Phase 1 — Resolve the source, then baseline

```bash
python3 .claude/skills/rewrite/check.py source <track>/<slug>
```

**Do not skip this and do not guess.** For 12 tracks plus the 15 architecture
modules, `content/articles/<track>/<slug>.txt` is *build output*: an edit there
renders correctly, survives until the next `npm run build`, and is then silently
gone. The resolver names the file **and the literal**. Four cases:

| Source | Edit |
|---|---|
| hand-written (`dsa`, `gen_ai`, `interview`, `async_python`, `concurrency`) | the `.txt` directly |
| generated (`maths`, `database`, `numpy`, `pandas`, …) | the `article=` argument of `topic(...)` in `tools/<track>_topics.py` |
| architecture module (`word2vec`, `yolo`, …) | the `article=` argument of `entry(...)` in `tools/arch_{cv,nlp,dl}.py` — these live *inside* otherwise hand-written tracks |
| `python` track | **a new `extend("<slug>", …)` at the END of `tools/python_extra.py`** — the `topic()` literal is only the first third of what ships; `python_extra.py` appends the rest via `add()` and then `extend()` |

Record the baseline (`check.py lint` prints all of it) so "did this improve?" is
answerable rather than asserted. Carry the starting Flesch score forward:

```bash
python3 .claude/skills/rewrite/check.py lint <track>/<slug> --baseline-flesch <n>
```

## Phase 2 — Structure and UI

Three things on this page are load-bearing. Break them and the page still
builds, so nothing tells you.

- **The first section becomes the "Overview" panel.** `tools/build_lede.py`
  lifts it above the visualisation and builds the "In this guide" contents list
  from the headings (needs ≥3). So:
  - **Never title the first section "Overview"/"Introduction"** — the build adds
    that label itself and the page shows it twice.
  - **With ≥10 sections the first section needs ≥110 words.** The panel is a
    2-column grid (`body` | `toc`, 17rem) and the row height follows the
    *taller* column, so a 50-word opener beside a 14-item contents list leaves
    ~600px of blank space. 578 of 635 pages currently have this defect.
- **The experiments section drives real Run buttons.** `build_labs.py` matches
  the heading on a fixed regex (`guided experiment|try this above|things to
  try|experiments to try|…`) and resolves the **bold control names** — written
  either `**like this**` or `<strong>like this</strong>` — against the actual
  controls on the page. Keep the heading verbatim; never paraphrase a control name.
- **Widths must be uniform.** Prose (`.vz-article`, 76ch) and the
  interactive/quiz blocks (`.vz-ivsec`, `.vz-check`, `--vz-page` = 1600px) use
  two different systems, which is why the article column and the quizzes below
  it don't line up. See `reference/ui-rules.md`.

## Phase 3 — Code the reader can actually run

- **No fence over 40 lines.** Today 294 fences exceed it and the longest is 210
  lines. Split long programs into stages that each teach one thing.
- **Every split fence must run standalone.** The reader opens one editor and
  presses Run; they inherit nothing from the fence above. Each needs its own
  imports and setup. (8-of-12 and 2-of-30 split fences raised `NameError` the
  first time this was done by hand.)
- **Every fence must print something.** A runnable example that outputs nothing
  is a button that does nothing.
- A `*-run` fence only becomes an editor on the 17 tracks in
  `tools/runnable_specs.py`. **The `python` track is not one of them** — its
  editors live in committed HTML.

## Phase 4 — Verify against the runtime the reader gets

```bash
python3 .claude/skills/rewrite/check.py fences <track>/<slug> --json /tmp/f.json
SHOW=1 node .claude/skills/rewrite/verify.mjs /tmp/f.json
```

This loads the same Pyodide 0.26.4 (**CPython 3.12.1, wasm32**) the page ships.
The build machine is CPython 3.9.6, so local success proves nothing. Threads,
`multiprocessing`, `fork`, sockets and `time.process_time` all behave
differently there — see `reference/pyodide-limits.md`.

**Then read the output against the prose, claim by claim.** This is the step
that cannot be automated and the one that matters. If a number in the article
doesn't match the number the code printed, the article is wrong until one of
them changes.

## Phase 5 — Voice that isn't AI-shaped

Targets measured across the 635 shipped articles, not invented:

| | site today | target |
|---|---|---|
| Flesch reading ease | median 56.7 | **≥60, and never below this page's baseline** |
| sentence length | median 14 words, p90 29 | keep it there |
| paragraph length | median 31 words | ≤60 |
| second person | 96% of articles | use "you", not "we" |

Banned outright (`check.py` enforces the list). The four that actually infest
this corpus: **essential** (124 hits), **robust** (73), **crucial** (23),
**leverage** (23). Plus the usual tells — *delve, dive into, in today's world,
it's important to note, furthermore, seamless, unlock the, harness, the power
of, demystify, cutting-edge, let's explore*. 23 of 39 checked patterns are
already absent site-wide; keep them absent.

What makes prose here read as human is not vocabulary, it is **specificity**:
a measured number instead of an adjective, a named failure instead of "issues",
the case where the advice is wrong stated plainly. Prefer the sentence that
could only have been written by someone who ran the code.

**Never pad to hit a word count.** Google names *"writing to specific word
counts based on SEO myths"* as a search-engine-first signal. 1,000 words is a
floor for thin pages; depth is the goal.

## Phase 6 — Interactive elements must actually work

Static markup cannot tell you this: the visualisations, schema browsers and
controls mount at runtime. Check them in the browser pane:

1. `preview_start` / `navigate` to the page.
2. `read_console_messages` — must be free of errors.
3. Confirm the widget **mounted**: the canvas has non-blank pixels, or the SVG
   has children, or the readout shows a value.
4. Drive one control (`computer` click) and confirm the readout changes.

**`document.hidden` is true in the pane, so `requestAnimationFrame` never fires
and screenshots come back blank.** Shim rAF and assert programmatically instead
of trusting a screenshot. Details in `reference/ui-rules.md`.

## Phase 7 — SEO and AdSense

```bash
python3 .claude/skills/rewrite/check.py seo <track>/<slug>
```

Already handled site-wide by `tools/build_seo.py`: canonical, robots, og:*,
twitter:*, author, `article:modified_time`, `LearningResource` +
`BreadcrumbList` + `Person` JSON-LD, og:image. Don't re-add these.

What the rewrite is responsible for:

- **A hand-written description in `tools/descriptions.py`.** 385 pages still
  ship the boilerplate frame *"Learn &lt;Title&gt; | VizLearn with a
  beginner-friendly interactive visualization on VizLearn."* — which awkwardly
  embeds the title. 70–165 characters, specific to the page.
- **A "Questions people ask" section.** `tools/build_faq_schema.py` turns it
  into `FAQPage` JSON-LD (345 pages, 2,233 questions). It runs in
  `npm run build`; run it directly for one page while iterating.
- **At least 3 internal cross-links** in the body, all resolving. A page
  reachable from nowhere does not get crawled.
- **Title ≤ 65 characters** so it isn't truncated.

AdSense rejected this site for *"Low value content"*. What answers that is
[Google's own checklist](https://developers.google.com/search/docs/fundamentals/creating-helpful-content):
original analysis, comprehensive coverage, insight beyond the obvious, clear
authorship, no easily-verifiable factual errors, careful production. Trust is
the primary axis — which is why Phase 4 outranks everything in Phase 7.

## Phase 8 — Build, audit, report

```bash
npm run build              # ~10 min, rewrites every page
python3 tools/audit.py
python3 tools/check_content.py          # did the rewrite silently DROP material?
python3 .claude/skills/rewrite/check.py all <track>/<slug>
```

An aborted build leaves the tree half-generated. If one fails:
`git checkout -- '*.html' sitemap.xml robots.txt assets manifest.webmanifest sw.js`
before retrying, rather than building on the wreckage.

Another session may be working in this repo — check `git log` before committing.
Commit prose and any generator change together. **Do not push without being asked.**

Report what the gates say, including anything still red and why. If a gate
cannot be met, say so explicitly rather than quietly lowering it.

## Companions

| file | what it does |
|---|---|
| `check.py` | every static gate: source resolution, lede balance, fence length, readability, banned phrases, markup, depth, SEO, links |
| `verify.mjs` | runs each fence headlessly in Pyodide 3.12.1 and prints its output |
| `../../tools/build_faq_schema.py` | FAQPage JSON-LD from the Q&A section |
| `reference/pyodide-limits.md` | what raises and what works in the reader's runtime |
| `reference/ui-rules.md` | the layout defects, their causes, and the browser-pane recipe |
| `reference/house-voice.md` | the measured distributions the targets come from |
