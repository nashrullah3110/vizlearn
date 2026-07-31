# VizLearn build tools

The site is still plain static HTML — it is served straight from the repo root
with no bundler and no framework. These scripts only *generate* the shared
assets and the repeated `<head>` markup, so that things which used to be
copy-pasted into 167 files now live in one place.

## Rebuild everything

```bash
npm run build
```

That runs, in order:

| Step | Script | Produces |
| --- | --- | --- |
| 0 | `tools/apply_sequence.py` | reorders `courseData` to the teaching order in `sequence.py` |
| 1 | `tools/build_catalog.py` | `assets/modules.js` — the module list and the Learning Path |
| 2 | `tools/merge_tw_config.js` | `tailwind.config.js` |
| 3 | `tools/build_icons_js.py` | `assets/icons.js` — SVG for icons chosen at runtime |
| 4 | `tools/build_og_images.py` | `assets/og/*.png` — 1200×630 social previews |
| 5 | `tools/build_articles.py` | written articles from `articles.py` |
| 6 | `tools/build_topics.py` | a landing page per track at `<track>/index.html` |
| 7 | `tools/build_static_pages.py` | `about` / `contact` / `privacy` / `terms` |
| 8 | `tools/build_labs.py` | runnable experiments, prediction, end-of-module check |
| 9 | `tools/build_responsive.py` | mobile grid breakpoints, viz ordering, touch surfaces |
| 10 | `tools/build_footer.py` | the shared footer, on every page |
| 11 | `tools/build_module_ui.py` | cheat sheet, related rail, prev/next, share, byline |
| 12 | `tools/build_seo.py` | canonical / OG / breadcrumbs / JSON-LD, plus the shared `<script>` tags |
| 13 | `tools/build_prerender.py` | static card grid inside `index.html` |
| 14 | `tailwindcss` | `assets/vizlearn.css` |
| 15 | `tools/build_sitemap.py` | `sitemap.xml`, `robots.txt` |
| 16 | `tools/check_inline_js.js` | parses every inline `<script>`; catches unbalanced braces |
| 17 | `tools/audit.py` | fails the build if anything is inconsistent |

Steps 8–13 write into the HTML between `VIZLEARN:*` markers and are idempotent —
re-running replaces the block rather than stacking copies. Don't hand-edit
inside those markers.

**Order is load-bearing in three places.**

- `build_module_ui` must run before `build_seo`, which appends the shared script
  tags last.
- Anything that injects near the end of `<body>` anchors on the
  `VIZLEARN:FOOTER:BEGIN` *marker*, never on the `<footer>` element — the footer
  is generated between markers, so anchoring on the element nests your block
  inside the footer's region and the next `build_footer` run deletes it. That
  bug only shows up on the *second* build, so `audit.py` checks for the nesting
  directly.
- **The stylesheet is built last of the content steps.** Tailwind drops any
  class it cannot find in the content globs, so building the CSS before the
  generators have written their markup produces a stylesheet missing every class
  they are about to emit — and only the second build looks right.

## Page kinds

Four now, where there used to be two:

- **the hub** (`index.html`);
- **166 modules**, hand-written, decorated by the steps above;
- **8 topic landings** (`<track>/index.html`, served at `/<track>/`), generated
  whole on every build. These exist because a track used to be reachable only as
  `index.html#ml` — a fragment, which is the same URL as the hub as far as a
  crawler is concerned, so no track could rank for its own subject;
- **4 static pages** (about / contact / privacy / terms), generated whole from
  `tools/static_pages.py`. The privacy policy is not optional while the pages
  load AdSense; `audit.py` checks that it names the same AdSense and Analytics
  IDs the pages actually carry.

`tools/lib_pages.py` holds what each of these is, and `tools/lib_shell.py` the
HTML frame the generated ones share.

## The lab layer

`tools/build_labs.py` adds three things to every module, driven by JSON it
writes into `#vz-lab-data` and read by `assets/vizlearn-lab.js`.

**Runnable experiments.** `tools/lib_controls.py` reads the page's real controls
out of its markup — id, kind, label, range, options. The written experiments are
then parsed against that list, so "set the *Neighbors (K)* slider to 1" becomes
`{id: "k-slider", value: "1"}` and gets a *Run this* button. A step that does not
resolve gets no button: a button that silently does nothing is worse than none.
213 resolve across 99 pages.

**Predict, then reveal.** The reader commits to what a readout will do, then the
runtime measures it: read the readout, apply the preset to the live
visualisation, read it again, compare. There is no stored answer, so the module
and its answer cannot drift apart. Where no written experiment resolved, a
preset is derived from the controls themselves (push the widest slider to its
far end), which is a real experiment and always a legal value.

**The check.** Multiple choice from `tools/labs.py` where a module has authored
questions (25 modules, 75 questions); retrieval flashcards otherwise, built from
the page's own key takeaways or section headings. Flashcard answers are always
text the page already carries — a machine-written distractor could be wrong, a
machine-selected quotation cannot be.

## Mobile

`tools/build_responsive.py` fixes in the markup what should be fixed in the
markup, because a Tailwind-native fix survives future edits and a stylesheet
override does not:

- bare `grid-cols-2/3` gets a single-column mobile base;
- the visualisation column is tagged `data-vz-viz`, and CSS lifts it above the
  controls under `lg` — the columns stack in source order otherwise, which put
  the controls first, so you moved a slider and the thing it changed was off the
  bottom of the screen;
- every surface with a pointer handler gets `.vz-touch-surface`
  (`touch-action: none`), without which a drag is claimed by the browser as a
  scroll and dies halfway. 45 pages needed it; 41 had it.

The rest — tap-target sizing under `pointer: coarse`, overflow guards,
`prefers-reduced-motion` — is unlayered CSS at the end of `vizlearn.src.css`.

## Module page features

Every module page gets, as real markup so crawlers follow it:

- **Cheat sheet** — the page's own first explanatory paragraph, extracted at
  build time, with a copy button. Paragraphs that wrap interactive controls, or
  that open with an instruction ("Drag the slider…"), are skipped in favour of a
  conceptual one; the meta description is the fallback.
- **Related rail** — the next four modules in the same track, as a horizontal
  slider matching the hub.
- **Prev / next** — the neighbouring modules in the track.
- **Share** — in the header, wired up by `assets/vizlearn.js`.

**Prev/next and related order follows `courseData`**, which
`tools/apply_sequence.py` keeps in sync with `tools/sequence.py`. That file is
where the teaching order lives — edit it, not `index.html`. It also defines
`LEARNING_PATH`, the curated 25-module beginner route rendered on the hub.

`tools/descriptions.py` holds hand-written meta descriptions, which override
whatever a page declares and are written back into its `<meta>` on build.

`tools/fix_touch_input.py` is a one-off that converted mouse listeners to
pointer events so the visualisations work on touchscreens; it is safe to re-run
and reports nothing left to convert.

## Progress tracking

`assets/vizlearn.js` records each module you open in `localStorage`
(`vizlearn_progress`), keyed by the page's canonical URL. The hub reads the same
store to draw checkmarks on visited cards, a percent-complete bar per track, and
the "Continue where you left off" banner. No backend, no login, nothing leaves
the browser.

## Search

`assets/search.js` ranks results with token matching rather than `includes()`,
so word order does not matter, partial words work, small typos are tolerated,
and module descriptions are searched alongside titles. Arrow keys / Home / End
move through results, Enter opens, Escape closes, and `/` focuses the box.

## Adding a new module

1. Create the page under the relevant topic directory.
2. Add one entry to `courseData` in `index.html` (title, path, card `svg`).
3. Slot its path into the right position in `tools/sequence.py`.
4. Optionally add a description to `tools/descriptions.py`.
5. Optionally add end-of-module questions to `tools/labs.py`.
6. `npm run build`.

`index.html`'s `courseData` is the single source of truth. Everything else —
the search catalog on all 167 pages, the sitemap, the OG image, the pre-rendered
grid — is derived from it. Previously each page carried its own copy of the
catalog, which is how twelve of them ended up with a dead search box.

## Requirements

- Node (for Tailwind and the config merge)
- Python 3
- ImageMagick (`magick`) — only for `build_og_images.py`

## Notes

- `assets/vizlearn.css` replaces the `cdn.tailwindcss.com` script, which was the
  in-browser JIT compiler and is not meant for production.
- Font Awesome is gone; its icons were inlined as SVG at build time. Icons that
  page JavaScript picks at runtime go through `vzIcon()` from `assets/icons.js`
  — add the icon name to `NEEDED` in `tools/build_icons_js.py` if you use a new one.
- Keyframes are declared explicitly in `tools/vizlearn.src.css` because many
  pages reference them from their own inline CSS rather than through an
  `animate-*` class, and Tailwind would otherwise purge them.
