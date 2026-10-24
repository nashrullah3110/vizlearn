# Article content

Every module page's written article lives here, one file per page:

    content/articles/<track>/<slug>.txt   ->   <track>/<slug>.html

These text files are the editable source of truth for their pages. They began
as extracted page copy, but articles are now actively rewritten and expanded
here; do not use the extraction script to overwrite them. The generated maths
lesson builder preserves existing files and uses its embedded copy only to
bootstrap a source file for a newly added lesson.

## The format

See the docstring of `tools/prose.py`. In short: two optional header lines,
then `## Heading` sections. Paragraphs, `- ` bullets, `1. ` numbered steps,
`|pipe|tables|` and ``` fenced code blocks. `**bold**` and `` `code` `` work,
and any block starting with `<` is passed through as raw HTML.

## Editing

1. Edit the `.txt` file (or splice new sections in, below).
2. `npm run build`.

Never hand-edit the article inside the page's `VIZLEARN:ARTICLE` markers — the
next build overwrites it from here.

## Two sections the build reads

- The **first** section is moved into the Overview lede by
  `tools/build_lede.py`, so keep it short and introductory. By default it sits
  near the title; pages that should show a visualiser before the Overview can
  put `<!-- VIZLEARN:LEDE:AFTER -->` after the complete widget in the HTML.
- The **experiments** section — headed "Guided experiments", "Try this above",
  "Experiments to try" or similar — is parsed by `tools/build_labs.py` to
  build the Run buttons and the presets they drive. The **bold** control names
  in its numbered steps must match real controls on the page. Do not rename
  that heading, and do not paraphrase the control names.

## Adding sections in bulk

`tools/splice.py` inserts new sections into existing files without rewriting
them. Write a batch file:

    ==== machine_learning/k_means @before Guided experiments
    ## An everyday version of the same idea
    ...

    ==== machine_learning/k_means @end
    ## Questions people ask
    ...

`@before <heading>` / `@after <heading>` / `@start` / `@end` place the block;
headings match on a case-insensitive prefix. Re-running a batch replaces
sections with the same heading rather than duplicating them.

    python3 tools/splice.py batch.txt

## Where the work stands

There is no fixed word-count target for articles. Use `tools/wordcount.py` to
find short pages for review, not to decide quality: a low count is a prompt to
check for missing definitions, worked examples, comparisons, use cases, or
limitations. Expand only where the lesson needs more explanation; do not add
padding to reach a number.

    python3 tools/wordcount.py                  # shortest pages first
    python3 tools/wordcount.py maths --all      # one track, including all pages

Two pages have no content file: `computer_vision/cnn.html` and
`natural_language_processing/rnn.html`. Their prose sits directly in the page
rather than in the standard article card, so `build_articles.py` cannot
address them. Edit those two in the HTML itself, inside the
`<main data-vz-prose>` block and outside every `VIZLEARN:*` marker.
