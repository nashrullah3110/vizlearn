---
name: rewrite
description: Rewrite one VizLearn article so it passes every content, code, UI, interactive, readability and SEO gate. Use when asked to rewrite, fix, improve, expand, de-AI or clean up an article or module page, or when a page has layout problems, over-long code blocks, or a broken visualisation.
---

# Rewrite one VizLearn article

You are rewriting **one** article. The content already exists — you are not
inventing a topic. Your job is to make the existing material clearer, shorter
per idea, correctly structured, and provably correct.

**Do exactly the steps below, in order. Do not skip a step. Do not decide a
step is unnecessary.** A checker program tells you what is wrong; you fix what
it reports and run it again.

Throughout, `ARTICLE` means the page id in the form `track/slug`, for example
`dsa/stacks` or `numpy/broadcasting`. No `.html`, no `.txt`, no leading slash.

---

## STEP 0 — Get the article id

If the user gave you a URL like `https://vizlearn.in/dsa/stacks.html`, the
ARTICLE is `dsa/stacks`. If they gave a file path like
`content/articles/dsa/stacks.txt`, the ARTICLE is `dsa/stacks`.

If you cannot work out a single ARTICLE, stop and ask the user which page.

---

## STEP 1 — Find out which file to edit

Run this:

```bash
python3 .claude/skills/rewrite/check.py source ARTICLE
```

It prints a line beginning `EDIT :`. **That is the only file you may edit for
prose.** Read what it says and obey it.

**This step is not optional and you must not guess.** Here is why it matters:
for most tracks, the file `content/articles/<track>/<slug>.txt` is *generated*.
If you edit that file, the page will look correct, and then the next time
anyone runs `npm run build` your entire rewrite is deleted with no error
message. The checker tells you the real source.

There are four possible answers:

| What it says | What you do |
|---|---|
| `content/articles/... (hand-written)` | Edit that `.txt` file. |
| `tools/<x>_topics.py (topic(...) for 'slug')` | Edit the long triple-quoted string inside that `topic(` call. |
| `tools/arch_*.py (entry(...) for 'slug')` | Edit the long triple-quoted string inside that `entry(` call. |
| `tools/python_extra.py` | Add a **new** `extend("slug", """...""")` block at the **very end** of `tools/python_extra.py`. Do not edit the `topic()` string in `python_topics.py` — it is only the first third of the article, and text added there lands in the middle of the finished page. |

---

## STEP 2 — Read the article and record the starting numbers

Read the file from step 1. Then run:

```bash
python3 .claude/skills/rewrite/check.py all ARTICLE
```

Write down the Flesch number it prints on the `[read]` line. You will pass it
back in step 8 so the checker can confirm you did not make the article harder
to read.

Everything the checker prints as `FAIL` is something you must fix. Everything
it prints as `ok` is something you must not break.

---

## STEP 3 — Fix the opening section

The site's build turns the article's **first section** into the "Overview"
panel at the top of the page, with a numbered contents list beside it.

Do these three things:

1. **The first section must not be called `## Overview`, `## Introduction` or
   `## Intro`.** The page prints the word "Overview" above it automatically, so
   those titles make the page say "Overview" twice. Give it a real title that
   says what the reader will learn, for example `## What a stack actually is`.

2. **The first section must be long enough.** Count the `##` headings in the
   article. The first section needs about **15 words per heading**. So an
   article with 14 sections needs a first section of about 210 words. If it is
   shorter, the panel leaves a large blank area on the page, because the
   contents list beside it is taller than the text.

3. **Keep it introductory.** It is the first thing the reader sees. Say what
   the thing is and why it matters, in plain words. Do not put code in it.

The checker's `[lede]` line tells you exactly how many words you need.

---

## STEP 4 — Do not break the experiments section

Look for a section whose heading is one of: **Experiments to try**, **Things to
try**, **Guided experiments**, **Try this above**, **Try it yourself**,
**Exploration guide**.

If the article has one:

- **Do not rename that heading.** The build searches for those exact words to
  create the page's "Run this" buttons. A different heading means every button
  disappears.
- **Do not reword the bold names inside it.** They look like
  `**Case Transformations:**` or `<strong>Case Transformations:</strong>`.
  Those names are matched against real controls on the page. If you reword one,
  its button stops working.

You may rewrite the explanation *after* each bold name. You may not touch the
heading or the bold names.

---

## STEP 5 — Break up the code

Find every code block that starts with three backticks followed by a language
and `-run`, like ```` ```python-run ````. These are the runnable editors.

**No code block may be longer than 40 lines.** Many are currently 100–200
lines. A reader cannot scroll a 200-line box, and if it fails they have no idea
which line broke.

To split one long block into several short ones:

1. Decide what the long block teaches. It is usually 3–5 separate ideas.
2. Make one block per idea, each under 40 lines.
3. **Each block must work completely on its own.** The reader opens one editor
   and presses Run. They did not run the block above it. So every block needs
   its own `import` lines and its own setup — its own variables, its own data.
   This is the single most common mistake: a split block that uses a variable
   defined in the previous block raises `NameError` for every reader.
4. **Each block must print something.** A Run button that produces no output
   looks broken.
5. Put a sentence of prose before each block saying what it will show.

Keep the code simple. Small numbers, short names, obvious data. If an example
needs a paragraph of explanation before the reader can follow it, the example
is too clever — replace it with a simpler one.

---

## STEP 6 — Run the code and read its output

This is the most important step in the whole process.

```bash
python3 .claude/skills/rewrite/check.py fences ARTICLE --json /tmp/f.json
SHOW=1 node .claude/skills/rewrite/verify.mjs /tmp/f.json
```

This runs every code block in the *same Python the reader gets* (Pyodide,
Python 3.12.1). The computer you are on runs Python 3.9, so testing there
proves nothing.

**If anything says `RAISED`, the rewrite is not finished.** Fix the code and
run it again.

**Then read the printed output line by line, and compare it to the sentences
around the code.** For every claim the article makes, ask: does the output
actually show that?

This matters because it has gone wrong many times on this site:

- An article said a heap was faster than sorting. The output showed sorting
  winning.
- An article said a list of tuples was bigger than an array. The output showed
  it was 1.84 times *smaller*.
- An article said a generator expression was faster. It was slower — the real
  benefit was memory.

If the output does not match the sentence, **one of them is wrong and you must
change it.** Never leave a number in the prose that the code did not print.

Some Python does not work in the reader's browser at all. Before writing an
example that uses threads, processes, files over the network, or CPU timing,
read `.claude/skills/rewrite/reference/pyodide-limits.md`. It lists exactly
what raises an error and what silently returns a useless value.

---

## STEP 7 — Rewrite the prose

The goal is that a reader finishes the page understanding the idea, and never
suspects a machine wrote it.

### Rules you must follow

**Write to the reader as "you".** Not "we". 96 of every 100 articles on this
site do this.

**Keep sentences short.** Aim for about 14 words. If a sentence has more than
about 30 words, split it into two.

**Keep paragraphs short.** About 30 words, three or four sentences at most.
One idea per paragraph.

**One idea per section.** The heading says what the idea is. If a section
covers two ideas, split it into two sections.

**Delete these words and phrases entirely.** The checker will fail the article
if any survive:

> essential, essentially, robust, crucial, leverage, delve, dive into, deep
> dive, in today's world, it's important to note, it's worth noting, in
> conclusion, furthermore, moreover, seamless, game-changer, unlock the,
> harness, plethora, myriad, realm, landscape of, pivotal, vital, when it comes
> to, whether you're, the power of, demystify, cutting-edge, ever-evolving,
> simply put, let's explore

**Replace vague words with the actual number or name.** This is what makes
writing sound human and expert:

| Do not write | Write instead |
|---|---|
| "much faster" | "155.9 ms against 11.9 ms" |
| "this is inefficient" | "`+=` copies everything accumulated so far" |
| "there are issues" | "it raises `KeyError` on the second call" |
| "a robust solution" | "it keeps working when the list is empty" |

**Say when the advice is wrong.** Every real technique has a case where it
loses. Naming that case is the strongest signal that a person wrote the page.
For example: "On data with only a handful of distinct values, the plain sort
won."

**Do not pad the article to reach a word count.** A shorter article that
answers the question is better than a longer one that circles it. If the
article is already over 1,000 words, do not add words for their own sake.

### Shapes to avoid

Do not open by saying the topic is important. Open with the thing itself.
Do not end a section by restating what the reader just read.
Do not write transitions like "Now that we have covered...".
Do not hedge a claim until it means nothing.

More detail, with the measured numbers behind these rules, is in
`.claude/skills/rewrite/reference/house-voice.md`.

---

## STEP 8 — Add the search-engine pieces

Two things are your responsibility:

1. **A "Questions people ask" section**, if the article has none. Write 5–6
   real questions a learner would ask, each as `<strong>The question?</strong>`
   followed by a direct answer in one or two sentences. The build turns these
   into Google's FAQ rich result automatically. Do not invent questions nobody
   asks; take them from the confusions the article already addresses.

2. **A description in `tools/descriptions.py`.** Add an entry keyed
   `"track/slug.html"` with a specific sentence of 70–165 characters. Without
   this the page falls back to a template sentence that 385 pages share.

Also make sure the article links to **at least 3 other pages on the site**,
using markdown links like `[binary search](binary_search.html)` for a page in
the same track, or `[the GIL](../concurrency/the_gil_and_what_it_locks.html)`
for another track. Only link to pages that exist — check with `ls`.

Then run the checker again, passing the Flesch number you wrote down in
step 2 so it can confirm the article did not get harder to read:

```bash
python3 .claude/skills/rewrite/check.py all ARTICLE --baseline-flesch 56.3
```

Replace `56.3` with your own number from step 2.

---

## STEP 9 — Build the site

```bash
npm run build
```

This takes about 10 minutes and rewrites every page. Wait for it.

If it fails partway, run this before trying again, or the next build will be
built on top of broken files:

```bash
git checkout -- '*.html' sitemap.xml robots.txt assets manifest.webmanifest sw.js
```

Then:

```bash
python3 tools/audit.py
python3 tools/check_content.py
```

`audit.py` must say "all checks passed". `check_content.py` tells you if your
rewrite accidentally deleted material that used to be on the page — if it
reports your article, check whether you meant to remove that.

---

## STEP 10 — Check the visualisation still works

Start the preview and open your page:

1. Call `preview_start` with `{name: "vizlearn"}`.
2. Call `resize_window` with `{width: 1440, height: 900}`. **You must do this.**
   Without it the page has no width and every measurement reads zero.
3. Call `navigate` to `http://localhost:8642/ARTICLE.html?fresh=1`.
   **Always add `?fresh=1`** — the site installs a service worker that serves
   an old copy of the stylesheet, which produces failures that are not real.
4. Call `javascript_tool` with exactly this text:

```js
const r=JSON.parse(await eval(await (await fetch('/.claude/skills/rewrite/liveness.js')).text())); ({page:location.pathname, verdict:r.verdict, failed:(r.checks||[]).filter(c=>!c.pass).map(c=>c.name+': '+c.detail), notes:r.notes})
```

5. Read the `verdict`:
   - `PASS` — the visualisation mounted, drew itself, and responded to a
     control. Go to step 11.
   - `NO-WIDGET` — this page has no visualisation. That is allowed. Go to
     step 11.
   - `FAIL` — read the `failed` list. Each entry names the problem. Fix it and
     repeat from step 3 of this list.

6. Also call `read_console_messages` with `{onlyErrors: true}`. There must be
   no errors. Ignore errors whose stack says `<anonymous>` — those come from
   your own pasted snippet, not the page.

Do not use a screenshot to judge the visualisation. The preview reports itself
as hidden, so animated widgets never paint there and a screenshot of a
perfectly healthy page comes back blank. The snippet above works around this.

---

## STEP 11 — Report, then stop

Run the checker one last time:

```bash
python3 .claude/skills/rewrite/check.py all ARTICLE
```

Tell the user:

- the article's word count and Flesch score, before and after
- how many code blocks there are now, and the longest one in lines
- that every code block ran, and one example of a number you checked against
  its output
- the visualisation verdict from step 10
- **anything still failing, and why**

Commit the changes:

```bash
git add -A && git commit -m "<your message>"
```

**Do not run `git push` unless the user asks you to.**

### Never say the rewrite is done if any gate is red

If you cannot make a gate pass, say so plainly: which gate, what you tried,
and what you think is needed. Do not lower a threshold in `check.py` to make a
failure disappear. Do not describe a red gate as a minor issue.

---

## Quick command reference

```bash
# which file do I edit?
python3 .claude/skills/rewrite/check.py source dsa/stacks

# what is wrong with this article?
python3 .claude/skills/rewrite/check.py all dsa/stacks

# just one group of gates
python3 .claude/skills/rewrite/check.py lint dsa/stacks
python3 .claude/skills/rewrite/check.py seo  dsa/stacks

# run the code blocks in the reader's Python
python3 .claude/skills/rewrite/check.py fences dsa/stacks --json /tmp/f.json
SHOW=1 node .claude/skills/rewrite/verify.mjs /tmp/f.json

# rebuild and check the whole site
npm run build && python3 tools/audit.py
```

## Reference files

- `reference/pyodide-limits.md` — what Python works in the reader's browser
- `reference/ui-rules.md` — the layout rules and why they exist
- `reference/house-voice.md` — the measured writing targets
- `liveness.js` — the visualisation checker used in step 10
- `probe.mjs` — regenerates `pyodide-limits.md` after a Pyodide upgrade
