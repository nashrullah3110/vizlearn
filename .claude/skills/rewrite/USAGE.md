# How to use the rewrite skill

## Running it

In Claude Code, from the repo root:

```
/rewrite dsa/stacks
```

One article per run. The argument is `track/slug` — no `.html`, no path. If you
paste a URL like `https://vizlearn.in/dsa/stacks.html` the skill works out the
id itself.

It works with a small model (Haiku). Every judgement call has been turned into
a command that prints `ok` or `FAIL`, so the model's job is to fix what the
checker reports rather than to decide what "good" means. The article's content
already exists; the skill is a rewriting pass, not a research pass.

## What it does, in order

1. Works out which file actually feeds the page — this is the step that stops a
   rewrite being silently deleted by the next build.
2. Records the starting word count and readability.
3. Fixes the opening section (length, and not calling it "Overview").
4. Leaves the experiments section's heading and bold control names alone.
5. Splits every code block over 40 lines into blocks that each run on their own.
6. Runs every code block in the reader's actual Python and compares the output
   to the prose.
7. Rewrites the prose to the site's measured voice.
8. Adds the FAQ section, a real meta description, and internal links.
9. Builds the site and runs the audit.
10. Checks the visualisation mounted, drew, and responded to a control.
11. Reports, commits, and stops without pushing.

## Checking a page yourself, without the skill

```bash
# which file do I edit for this page?
python3 .claude/skills/rewrite/check.py source gen_ai/tf_idf

# what is wrong with it?
python3 .claude/skills/rewrite/check.py all gen_ai/tf_idf
```

`all` exits non-zero if anything failed, so it works in a shell loop:

```bash
for a in dsa/stacks dsa/queues numpy/broadcasting; do
  python3 .claude/skills/rewrite/check.py lint "$a" || echo "^ $a needs work"
done
```

## Running the code blocks

```bash
python3 .claude/skills/rewrite/check.py fences dsa/stacks --json /tmp/f.json
SHOW=1 node .claude/skills/rewrite/verify.mjs /tmp/f.json
```

This uses Pyodide 0.26.4 — CPython 3.12.1 on wasm32, the same build the page
loads in the browser. The machine you are on runs Python 3.9.6, so running a
snippet locally does not tell you what the reader sees.

Drop `SHOW=1` for a summary instead of full output. Exit code is non-zero if
any block raised.

First run for a track that needs numpy, pandas, scikit-learn or matplotlib
downloads the wheel and caches it in `node_modules`, so it is slow once and
fast afterwards.

## Checking a visualisation

Needs the preview running. Three things trip people up, in this order:

1. **Set a window size first.** `resize_window` to 1440x900. Without it the
   page has no width and every measurement reads 0.
2. **Add `?fresh=1` to the URL.** The site registers a service worker that
   serves a cached stylesheet, so CSS changes appear not to have worked. This
   wasted real time during development — the built file was correct and the
   browser was showing an old copy.
3. **Do not use a screenshot.** The preview pane reports
   `document.visibilityState === "hidden"`, and browsers do not run
   `requestAnimationFrame` on a hidden page. Every canvas widget here draws in
   a rAF callback, so a screenshot of a healthy page is blank.
   `liveness.js` shims rAF and measures the DOM instead.

Then run this in `javascript_tool`:

```js
const r=JSON.parse(await eval(await (await fetch('/.claude/skills/rewrite/liveness.js')).text())); ({verdict:r.verdict, failed:(r.checks||[]).filter(c=>!c.pass).map(c=>c.name+': '+c.detail)})
```

`verdict` is `PASS`, `FAIL` or `NO-WIDGET`. All eleven visualisation engines on
the site were checked this way and all eleven pass: arch, async, con, rv, iv,
ml, math, cv, db, dl, sql.

## What the gates are

| gate | what it checks | threshold, and where it came from |
|---|---|---|
| `source` | the file you are about to edit is the real source | 12 tracks + 15 arch modules have generated `.txt` |
| `toc` | enough sections for a contents list | ≥3, required by `build_lede.py` |
| `lede` | opening section long enough, not named "Overview" | ~15 words per section; measured, see below |
| `labs` | experiments heading and control names intact | matched by `build_labs.py` |
| `fence` | no code block over 40 lines | site p90 is 87 lines, max was 210 |
| `read` | Flesch reading ease | ≥60, and never below the page's own baseline. Site median is 56.7 |
| `voice` | no banned phrases, sentence length | p90 ≤34 words; site p90 is 29 |
| `depth` | rendered word count | ≥1,000 |
| `markup` | no mismatched `**`/`<strong>`, no broken entities | — |
| `seo` | description, title length, FAQ schema, ≥3 working internal links | description 70–165 chars |

## Why the opening section has to be long

The Overview panel is a two-column grid: your first section on the left, the
contents list on the right. A grid row is as tall as its taller column, so a
short opening section beside a long contents list leaves the rest blank.
Measured at 1440px on a 14-section page, changing only the opening section:

| opening section | blank space left |
|---|---|
| 51 words | 452px |
| 101 words | 341px |
| 151 words | 219px |
| 201 words | 96px |

A CSS fix was tried (`columns: 2` on the list) and did nothing, because that
list is a grid container and grid ignores CSS multi-column. So the fix is the
content, which is why it is a gate.

## The current backlog

Against the articles as they stand today:

- **518 of 635** fail the `lede` gate
- **286 of 635** fail the `fence` gate
- **232** fail both
- **63** are clean on both

That is not a bug in the gates. The site was written before either rule
existed. Expect most pages to report several failures on the first run.

## Things the skill will not do

- Push to git. It commits and stops.
- Invent content that is not in the source article.
- Pad an article to hit a word count. Google names writing to a word count as a
  search-engine-first signal, so the 2,000-word figure in `tools/wordcount.py`
  is a ceiling to ignore, not a target. 1,000 words is the floor.
- Lower a threshold to make a failure disappear. If a gate cannot pass, the
  skill says so.

## If something looks wrong with the skill itself

Three of the original gates were wrong when first written and were corrected
after being measured:

- `<strong>` is a valid control name, not just `**bold**` — it is what
  `build_labs.py` actually matches.
- A `**` inside a code fence is not a mismatched bold marker. The markup check
  strips fences first.
- A missing `robots` meta tag is fine — 174 of the 177 pages that have one just
  restate the `index, follow` default. The gate now only catches an accidental
  `noindex`.

If a gate reports something you believe is correct, measure it before changing
the article. And if the gate turns out to be wrong, fix the gate and record the
measurement in the reference file, the way those three were.
