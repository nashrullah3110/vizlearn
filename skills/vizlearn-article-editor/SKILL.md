---
name: vizlearn-article-editor
description: Rewrite and redesign VizLearn learning articles for clear, original teaching, topic-fit interactive layouts, reliable citations, and AdSense policy alignment. Use for article-wide content or article UI/UX work in this repository.
---

# VizLearn article editor

Use this skill when the user asks to rewrite, improve, audit, or redesign the learning modules in the VizLearn repository. The goal is a genuinely useful, accurate learning experience with clear editorial value. Align the work with Google's published publisher and Search guidance, but never promise AdSense approval: Google makes the review decision and does not publish a checklist that guarantees acceptance.

## Editorial outcome

Make every page answer a real learner need. Prefer a short, complete explanation over long prose written to meet a word target. Preserve the site's distinctive interactive lessons, runnable examples, and learning paths; improve the teaching around them rather than replacing them with generic blog articles.

For each page:

- Remove duplicated or boilerplate introductions, repeated definitions, generic conclusions, and sections that merely restate the visualisation or code.
- Keep a brief opening only when it gives the learner useful orientation: what the idea is, why it matters, and what to notice. Do not repeat the title, page description, control instructions, and article intro in four forms.
- Explain the topic in a logical sequence. Use only the sections that serve that topic; do not force every page into the same headings or FAQ pattern.
- Include a worked example when it helps a reader understand or apply the idea. Use the page's own visualisation, runnable code, data, or a small hand calculation where appropriate.
- Explain meaningful assumptions, limitations, edge cases, and common mistakes. Do not pad a simple topic with shallow sections.
- Add a small number of relevant primary sources and internal links at the point they help. Link to the original paper, official documentation, standards, or authoritative source for claims that need attribution or are easy to get wrong. Do not add citations decoratively.
- Ensure prose, code, diagrams, controls, readouts, worked examples, and answer keys agree with one another.

Google does not set a preferred word count. Do not treat the repository's old 2,000-word target, the quality scanner's 800-word threshold, or the presence of a table/code/formula as a definition of quality. A concise page can be complete; a long page can still be thin or repetitive.

## Choose the teaching layout per page

Do not force every page to begin with a full-screen visualiser. Identify the page's teaching mode and select the layout that lets a learner understand and use its central idea quickly. The shared site chrome can stay consistent while the content sequence varies.

### Visualiser-led

Use when changing a parameter or stepping through a process is the clearest way to understand the concept. Keep the visualisation prominent near the top, after the title and a concise orientation. Give the learner one specific thing to try or observe. Put the explanation immediately before or after the relevant interaction; do not make the reader search below a long prose block to learn what the controls mean.

Choose whether the Overview belongs before or after the visualisation based on the teaching sequence. When the learner can understand the opening idea better by manipulating the visualiser first, put the Overview and its contents list directly below the complete visualiser. In this repository, `tools/build_lede.py` supports the page marker `<!-- VIZLEARN:LEDE:AFTER -->` for that placement; insert it after the widget and keep the normal generated lede markers intact. Keep the title and one-sentence orientation above the widget so the page is not an unexplained tool.

### Code-led

Use when the goal is to write, read, debug, or compare code. Put a runnable, minimal example near the explanation it teaches. Introduce what to run and what output or behavior to notice. Explain important lines and show a useful variation or failure case where relevant. Do not show the same full code once in a static block and again in an editor unless the two views have distinct purposes.

### Mixed visualiser and code

Choose which element carries the central teaching point. Put that element first; place the supporting element beside it on wide screens only when both remain readable, and stack them in a sensible reading order on narrow screens. Explicitly connect them: explain whether the code implements the displayed result, provides a second view of it, or demonstrates a related case. Avoid two disconnected demos competing for attention.

### Concept-first

Use when neither a large visualiser nor a code editor is the best opening—for example, a definition, proof, design choice, or comparison. Start with the concise explanation, then introduce the interaction or code at the point it clarifies the concept. Do not enlarge a small supporting widget into a full-screen hero.

### Responsive and accessible behavior

- On phones, show the page title and enough orientation to explain the lesson before a large interactive area. Do not let a tall canvas or editor bury the teaching objective.
- Keep controls usable with touch, keyboard, and assistive technology. Give inputs descriptive labels; expose changing results as readable text where appropriate; do not rely on color alone.
- Preserve focus visibility, readable contrast, meaningful heading order, and reduced-motion preferences. Avoid horizontal overflow from code or tables; provide a usable scroll container when needed.
- Prefer a readable text measure and clear spacing over maximising the amount of content visible at once. Keep code and its explanation close together.
- Preserve working module navigation, experiments, checks, and app features unless the user asks to change them or they actively obstruct the lesson.

### Page width and mathematical readability

- Align the visualiser and article's **outer bands** to the same content container. Do not let a global prose-width cap shrink the whole article card when the visualiser is intentionally full width.
- Keep running paragraphs at a comfortable measure (roughly 65–90 characters per line where practical), even when the article card spans the visualiser's width. Let diagrams, tables, code, and display equations use the wider band when that improves comprehension.
- Set important equations apart from prose when they need more room. Use consistent spacing, a readable math/monospace face, clear operator and subscript rendering, and sufficient contrast. Long equations must wrap or scroll within their own container on narrow screens; they must never widen the page.
- Use inline notation only for short expressions that remain easy to scan. Explain symbols near the equation, and provide an accessible text equivalent when the markup uses visual-only notation.
- Review the rendered page at desktop and phone widths. Check that the article card and visualiser align edge to edge, paragraph lines remain readable, display equations are visually distinct, and no formula or control causes horizontal page overflow.

## Research and citations

Verify claims against sources appropriate to the topic. Prefer primary sources in this order when available: original papers or standards; official project/library documentation; reputable textbooks or institutions. Use a paper to support the original method or result, and current official docs for API behavior that may change. Browse when facts are time-sensitive, niche, uncertain, or policy-related.

- Never invent a citation, quote, statistic, author credential, test result, or claim of first-hand use.
- Cite specific claims, not entire paragraphs by attaching an unrelated link.
- Keep citations usable in the rendered article. Use the article source format's Markdown links, and verify their targets. Add a short “Sources” section only when several sources are useful to the learner; otherwise cite inline.
- Add internal links to prerequisites, relevant follow-on lessons, or a closely related contrast. Keep links contextual, with descriptive text. Avoid sitewide cross-link stuffing or linking every keyword.
- Distinguish established fact from simplification, analogy, or uncertainty. State version and date when technical behavior depends on a library release.

Useful policy references (re-check these when doing policy-sensitive work):

- [AdSense: Your account wasn't approved](https://support.google.com/adsense/answer/81904?hl=en)
- [Google Publisher Policies](https://support.google.com/adsense/answer/10502938?hl=en)
- [Google Search: Creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search spam policies](https://developers.google.com/search/docs/essentials/spam-policies)

These pages describe policy and quality guidance; they do not guarantee acceptance into AdSense. Do not write to a supposed minimum word count or claim that passing a local audit means Google will approve the site.

## Repository-specific editing rules

The generated HTML is not generally the source of truth. Before editing, inspect repository instructions, Git status, the page's generation markers, and the current article pipeline.

- The article sources live in `content/articles/<track>/<slug>.txt` when that file exists. The text format is parsed by `tools/prose.py`; it supports headings, paragraphs, lists, tables, inline links, code, and selected runnable-code fences.
- Some articles are still declared in `tools/articles.py`. Check that source before editing a generated HTML page. The article builder renders content into `VIZLEARN:ARTICLE` markers; a later build can overwrite direct HTML edits.
- Some pages have article prose directly in their HTML and may not be handled by the normal article generator. Follow the source path documented in `content/README.md` and the page's markers before changing them.
- `tools/build_lede.py` moves the first article section into the page's Overview/lede area. By default it places the Overview near the title; use the optional `<!-- VIZLEARN:LEDE:AFTER -->` marker after a visualiser when the lesson should move from title/orientation to interaction and then to Overview. Keep the first section concise and non-duplicative; preserve it as useful orientation rather than deleting the only explanation.
- Experiment sections are parsed to create runnable buttons. Preserve recognized experiment headings and bold control labels exactly as they appear in the page's real controls. Do not silently rename a control or change its valid range.
- Generated content lives between `VIZLEARN:*` markers. Edit the source, then use the documented build workflow when the user has requested repository changes. Do not hand-edit generated blocks as a substitute for source edits.
- Protect existing user work. Inspect `git status` first, preserve uncommitted edits and untracked article sources, and do not reset, overwrite, or discard them. Do not run extract/seed commands with force or generators that rewrite unrelated pages without first establishing their effects.
- The repository's current article documentation may contain old targets or counts. Treat the page catalog and actual source files as authoritative, verify the live count from the catalog, and correct stale public descriptions or build documentation only when that is within the requested scope.

## Workflow for a site-wide rewrite

1. **Establish the current state.** Read `AGENTS.md` and relevant repository instructions, inspect `git status`, catalog counts, source-of-truth files, generators, and any existing quality reports. Note untracked work and avoid disturbing it. Do not infer that an old report covers recently added pages.
2. **Inventory pages by teaching mode and risk.** Classify modules as visualiser-led, code-led, mixed, or concept-first. Record for each page its source file, overview/lede, main sections, interactive/code elements, citations, internal links, and any duplication or factual concerns. Flag pages with errors or missing content rather than making up material.
3. **Settle representative patterns.** Revise a small, varied sample: at least one visualiser-led page, one code-led page, one mixed page, and one concept-first page. Inspect the rendered pages at desktop and mobile sizes. Use those examples to settle content order and visual treatment; do not impose one full-screen hero layout on all modules.
4. **Rewrite in manageable batches.** Work track by track or in similarly reviewable groups. Remove repeated intros and filler; teach the idea plainly; add an example only when it clarifies; research and link important claims; add relevant internal links; and retain valid interactive hooks. Keep an audit trail of pages completed, uncertain facts, broken demos, and source gaps.
5. **Improve the UI in shared components where possible.** Make article typography, line length, spacing, heading hierarchy, code treatment, tables, equations, and demo placement readable. Align the article and visualiser outer widths where intended while preserving a comfortable paragraph measure. Prefer shared CSS/components for common behavior, with page-level choices for the teaching mode. Avoid altering unrelated hub or application UI.
6. **Resolve sitewide contradictions in scope.** Derive the module count from the actual catalog rather than hardcoding it in multiple places. Reconcile the hero statistic, track totals, descriptions, sitemap/build copy, and repository README when those surfaces are included in the requested task.
7. **Review the rendered outcome.** Use the site's actual build process and inspect representative output from every layout pattern. Verify content is not duplicated between the lede and article, links resolve, code fences and citations render correctly, experiments still match controls, mobile order is understandable, and shared styles work. Report anything that could not be checked. Do not equate an internal word-count or build audit with AdSense approval.
8. **Report honestly.** Summarize the kinds of changes made, pages covered, checks performed, exceptions, and remaining uncertain or unsupported claims. State clearly that approval depends on Google's review and cannot be guaranteed.

## Quality bar

Before calling a page finished, ask:

- Can a learner state what they learned and why it matters after reading it?
- Does each section add something new, or does it repeat the overview, demo, or another section?
- Does the chosen opening element fit the teaching goal, and is its purpose clear?
- Are the example, explanation, code, interaction, and answer key consistent and correct?
- Are citations authoritative and attached to the claims they support? Do internal links genuinely help the learning path?
- Is the page readable on mobile and usable without a mouse?
- Do the article and visualiser align at their outer edges, and do display equations remain legible without causing page overflow?
- Did the edit add real explanatory value instead of length, keyword variants, or template sections?

If a fact cannot be verified or a demo appears wrong, mark it for investigation and avoid presenting a guess as fact.
