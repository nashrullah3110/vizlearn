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
| 1 | `tools/build_catalog.py` | `assets/modules.js` — the module list every page's search reads |
| 2 | `tools/merge_tw_config.js` | `tailwind.config.js` |
| 3 | `tailwindcss` | `assets/vizlearn.css` |
| 4 | `tools/build_icons_js.py` | `assets/icons.js` — SVG for icons chosen at runtime |
| 5 | `tools/build_og_images.py` | `assets/og/*.png` — 1200×630 social previews |
| 6 | `tools/build_module_ui.py` | cheat sheet, related rail, prev/next and share control in every module |
| 7 | `tools/build_seo.py` | canonical / OG / Twitter / JSON-LD, plus the shared `<script>` tags |
| 8 | `tools/build_prerender.py` | static card grid inside `index.html` |
| 9 | `tools/build_sitemap.py` | `sitemap.xml`, `robots.txt` |
| 10 | `tools/audit.py` | fails the build if anything is inconsistent |

Steps 6–8 write into the HTML between `VIZLEARN:*` markers and are idempotent —
re-running replaces the block rather than stacking copies. Don't hand-edit
inside those markers. `build_module_ui` must run before `build_seo`, which
appends the shared script tags last.

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

**Prev/next and related order follows `courseData` order within a topic**, so
reordering a topic's `courses` array in `index.html` is how you define the
learning sequence. Today that order is roughly alphabetical.

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
3. `npm run build`.

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
