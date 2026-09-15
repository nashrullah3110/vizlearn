# The house voice, measured

Every target in `check.py` comes from the 635 articles already shipped, so a
rewrite is held to this site's standard rather than to a general idea of good
writing. Regenerate these numbers with `check.py` on a sample, or re-run the
measurement in this file's history.

## Distributions across 635 article files

| | value |
|---|---|
| words per article | median **1,637**, mean 1,540 |
| `##` sections | median **14**, range 7–29 |
| sentence length | median **14** words, mean 16.3, p90 **29** |
| paragraph length | median **31** words, p90 **61** |
| uses "you" | **608 of 635** (96%) |
| uses "we" | 55 of 635 (9%) |
| Flesch reading ease | median **56.7**, p10 49.3, p90 63.9 |

The readability gate is **≥60**, above the current median: "easy to read and
digest" is the explicit goal of a rewrite, and 56.7 is "fairly hard".

Hardest pages today: `embedding_layers` (38), `probability_calibration` (41),
`generative_adversarial_networks` (41). Easiest: `equation_of_line` (72),
`aggregate_functions_in_sql` (71), `heap_sort` (70).

## Banned phrases, with live counts

23 of the 39 patterns checked are **already absent site-wide**. Keep them that
way. The four that actually infest this corpus:

| phrase | hits | files |
|---|---|---|
| `essential` / `essentially` | 124 | 104 |
| `robust` | 73 | 44 |
| `crucial` | 23 | 19 |
| `leverage` | 23 | 3 |

Lower but present: `the power of` (7), `dive into` / `deep dive` (8),
`demystify` (4), `unlock the` (3), `whether you're` (3), `seamless` (2),
`landscape of` (2), and one each of `furthermore`, `ever-evolving`,
`let's explore`, `simply put`.

## What actually makes this read as human

Not vocabulary — **specificity**. The corpus reads as written by someone who ran
the code because it keeps doing these things:

- **A measured number instead of an adjective.** Not "much faster" but "155.9 ms
  versus 11.9 ms".
- **Naming the case where the advice is wrong.** "On data with only a handful of
  distinct values, the sort *won*."
- **Stating the mechanism, not the label.** Not "this is inefficient" but
  "`+=` copies everything accumulated so far".
- **Admitting the environment.** "In this sandbox: can't start new thread."
- **One idea per section**, with the heading saying which idea.

And it avoids the shapes that read as generated:

- opening with the topic's importance rather than with the thing itself
- a summary paragraph that restates the section just read
- lists of three adjectives where one number would do
- transitions that announce structure ("Now that we have covered…")
- hedging every claim into unfalsifiability

## Two rules that outrank style

1. **Never pad to a word count.** Google names *"writing to specific word counts
   based on SEO myths"* as a search-engine-first signal. `tools/wordcount.py`
   prints a 2,000-word target; treat 1,000 as a floor for thin pages and depth
   as the goal. A 1,600-word article that answers the question beats a 2,400-word
   one that circles it.
2. **A claim with no evidence gets cut, not softened.** If the code didn't print
   it, don't write it.
