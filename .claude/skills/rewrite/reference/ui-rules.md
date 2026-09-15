# Layout and interactive rules

Four defects, each with a measured cause. Three have a site-wide fix that should
be made once in CSS; the skill's job is to *verify* them, not re-fix them on
every article.

## 1. The blank area at the top of an article

**Cause.** `tools/build_lede.py` renders the article's first section as the
"Overview" panel with the contents list beside it. `.vz-lede` is a two-column
grid (`body` | `toc`, the TOC fixed at 17rem) and a grid row is as tall as its
**tallest** column. A 14-item contents list is ~600px; a 50-word opening
section is ~90px. The difference is empty space.

**Measured: 578 of 635 pages have a TOC taller than their lede body.**

**Content fix (per article, gate `lede`):** with ≥10 sections the first section
needs **≥15 words per section** (so 14 sections → ~210 words). Measured in the
browser at 1440px on `dsa/strings_in_python` (14 sections), growing only the
opening section:

| opener | body height | blank space left |
|---|---|---|
| 51 words (as shipped) | 142px | **452px** |
| 101 words | 253px | 341px |
| 151 words | 376px | 219px |
| 201 words | 498px | **96px** |

A contents item costs ~38px of column; a word of opening prose buys ~2.5px.

**Also:** never title the first section "Overview" or "Introduction".
`build_lede.py` adds an `<h2>Overview</h2>` itself, so the page renders the word
twice — visible on `dsa/strings_in_python`, whose first section is literally
`## Overview` with 50 words.

**CSS fix: there isn't a good one.** `columns: 2` on the list was tried and
measured: the list stayed **527px** — identical — because `.vz-lede-toc ol` is
`display: grid`, and a grid container ignores CSS multi-column outright. (The
browser kept reporting `columnCount: 2` from a service-worker-cached
stylesheet after the rule was removed, which is worth knowing: verify CSS
against the built file, not a browser read.) Widening the track to 28rem got it to
411px but narrows the opening prose from 674px to ~480px, which trades one
readability problem for another. Capping the list with `overflow-y: auto` gets
the waste to 177px but hides navigation. **So this is a content constraint, not
a CSS one**, and the `lede` gate is the fix. The dead rule was removed rather
than shipped; the measurement is recorded in `tools/vizlearn.src.css` beside
`.vz-lede-toc` so nobody tries it again.

## 2. Code blocks that are too long

**Measured:** median fence is 19 lines, but p90 is **87** and the longest is
**210**. 294 fences exceed 40 lines; 129 exceed 100.

A 99-line editor — `dsa/strings_in_python` fence 1 — asks the reader to scroll a
code box inside a scrolling page, and if it fails they have 99 lines to bisect.

**Rule:** ≤40 lines per fence; split into stages that each teach one thing and
each run standalone, with their own imports. Verify with `verify.mjs` — a split
that shares state raises `NameError` for the reader, who never ran the fence above.

## 3. Mismatched widths between prose and interactive blocks

**FIXED.** `[data-vz-prose]` had been deliberately narrowed from `--vz-page`
to 1080px so the article card came in to meet its text — and its own comment
said it stayed "wide enough to look related to the bands below it". The bands
below kept `--vz-page: 1600px`, so they ran proud of the article on both sides.
`.vz-lab`'s comment shows the same intent going stale: "at the old 1400px the
lab block was wider than the article it sits under".

Measured on the live site at 1265px, before the fix:

| block | left edge | width |
|---|---|---|
| prose `.vz-article` | 268px | 730px |
| check / quiz cards | 32px | 1201px |

There is now one token, `--vz-measure: 1080px`, used by `[data-vz-prose]`,
`.vz-lab`, `.vz-codelab`, `.vz-ivsec` and `main.prose`. Verified locally at
1440px afterwards — the article card, the check card and the predict card are
**all left 205px, width 1016px**, pixel-identical. The duplicate `.vz-article`
declaration (`78ch` then `76ch`) was also collapsed to one.

Use `--vz-page` only for bands that are genuinely page-wide furniture; anything
in the reading flow takes `--vz-measure`.

## 4. Broken or unstyled interactive elements

Two different failure modes, and only one is visible in the markup.

**Static:** `.vz-py-inline` — the frame around an inline editor — is defined
**only inside the inline `<style>` of six builders** (`build_pandas_topics.py`,
`build_numpy_topics.py`, `build_fastapi_topics.py`, `build_pydantic_topics.py`,
`build_matplotlib_topics.py`, `build_sklearn_topics.py`). **377 of the 524 pages
that use the class never ship its CSS**, so the editor loses its border and
padding on every `interview`, `dsa`, `maths`, `gen_ai`, `deep_learning`,
`machine_learning`, `computer_vision`, `nlp`, `async_python` and `concurrency`
page — no border, no radius, and no `border-top` separating the Run controls
from the code. **FIXED:** those rules now live in `tools/vizlearn.src.css`, so
all 524 pages get them.

Note the class is only *partly* unstyled: `.py-controls` itself is global, so
the buttons keep their flex layout. What was missing is the frame.

**Runtime:** visualisations, schema browsers and control readouts are built by
JS after load, so they are not in the HTML at all and cannot be checked by
grepping. Use the browser pane:

1. `preview_start` / `navigate` to the page
2. `read_console_messages` — must have no errors
3. confirm the widget **mounted** — canvas has non-blank pixels, or the SVG has
   child nodes, or the readout shows a value
4. click one control with `computer` and confirm the readout changes

**`document.hidden` is true in the pane, so `requestAnimationFrame` never
fires**: widgets that draw on rAF never paint and screenshots come back blank.
Shim rAF before asserting, and prefer `read_page` / `javascript_tool` over a
screenshot. Note that some widgets latch a `queued` flag, so a fresh page load
is needed rather than a re-run.

### A trap when auditing class names

Most `vz-*` classes with no CSS rule are **JS query hooks**, not style classes —
`vizlearn-interview.js` does `querySelector('.vz-iv-play')`, and
`build_labs.py` emits `.vz-predict-readout` purely for `vizlearn-lab.js` to find.
A "class with no CSS" audit that doesn't exclude hooks reports them as broken.
It flagged 9 on one page; 8 were fine.

## The one UI rule already fixed, worth not regressing

Interactive controls go **above** the stage, not below it. `assets/vizlearn-arch.js`
builds an `.arch-head` wrapper holding the control panel and readout and appends
it before the stage. Before that fix the sliders sat under a 3,800px canvas
(9,984px on the autoencoders page) and were unreachable without scrolling past
the thing they controlled.
