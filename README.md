# VizLearn

**[vizlearn.in](https://vizlearn.in)** — 166 interactive visual explainers for AI,
Machine Learning, Algorithms and the maths underneath them.

Free, no ads, no login.

---

## What it is

Most explanations of these topics are either a wall of equations or a wall of
prose. VizLearn is the third option: something you can poke. Drag a support
vector and watch the margin move. Change `k` and watch the decision boundary
breathe. Step gradient descent one iteration at a time and watch the line fit.

Every module is a single self-contained page — an interactive visualisation, the
controls that drive it, and a written explanation underneath.

## Tracks

| Track | Modules | Starts at |
| --- | --- | --- |
| [Maths](https://vizlearn.in/#maths) | 13 | Equation of a Line |
| [Machine Learning](https://vizlearn.in/#ml) | 19 | Train-Test Split |
| [Deep Learning](https://vizlearn.in/#dl) | 27 | Perceptron |
| [Algorithms & Data Structures](https://vizlearn.in/#dsa) | 41 | Big-O Notation |
| [NLP](https://vizlearn.in/#nlp) | 30 | ASCII Character Codes |
| [Computer Vision](https://vizlearn.in/#computer-vision) | 16 | How Networks Process Images |
| [Databases & SQL](https://vizlearn.in/#db) | 12 | What are Relational Databases |
| [Gen AI](https://vizlearn.in/#gen-ai) | 8 | How LLMs Process Text |

Modules within a track are ordered so each one only leans on ideas from the ones
before it, and every page links to the previous and next step.

New here? The [Learning Path](https://vizlearn.in/#learning-path) is a curated
25-module route across tracks, from the maths everything assumes through to
picking a specialism.

## Features

- **Prev/next navigation** through every track, plus a related-modules rail.
- **Progress tracking** — visited modules get a checkmark, each track shows a
  percentage, and the hub offers to resume where you left off. Stored in your
  own browser; nothing is sent anywhere.
- **Cheat sheet** on every module: the one-paragraph takeaway, copy-pasteable.
- **Search** that tolerates typos and word order and matches descriptions as
  well as titles. Press `/` to focus it, arrow keys to move through results.
- **Light and dark themes**, remembered between visits.
- **Works on touch** — the visualisations respond to finger and stylus, not just
  a mouse.

## Running it locally

It is a static site; any web server will do.

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>.

## Adding a module

`index.html`'s `courseData` is the single source of truth for the catalog.

1. Add the page under the relevant track directory.
2. Add one entry to `courseData` (title, path, card SVG).
3. Slot its path into the right position in `tools/sequence.py`.
4. Run `npm run build`.

That regenerates the shared catalog, the social preview image, the sitemap, the
prev/next links and the related rail, then runs an audit that fails on anything
inconsistent. See [tools/README.md](tools/README.md) for what each step does.

## Licence

MIT — see [LICENSE](LICENSE).

## Contact

Ashish Jangra — [GitHub](https://github.com/AshishJangra27) ·
[LinkedIn](https://www.linkedin.com/in/ashish-jangra/) ·
[Kaggle](https://www.kaggle.com/ashishjangra27)
