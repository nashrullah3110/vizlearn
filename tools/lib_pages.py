"""Metadata for the pages that are not modules.

Until now every routable URL was either index.html or one of the 166 module
pages, so `lib_catalog` was enough. This file adds the two other kinds:

  * **topic landing pages** - one per track, served at `/<dir>/`. Previously a
    track only existed as `index.html#ml`, which is the same URL as the hub as
    far as a crawler is concerned, so no track could ever rank for its own
    subject.
  * **static pages** - about / contact / privacy / terms, at the site root.
    The privacy policy is not optional now that the pages load AdSense, which
    sets cookies.

Copy lives here rather than in the generators so the wording is reviewable in
one place.
"""

import os
import subprocess

from lib_catalog import ROOT, SITE, DIR_META

AUTHOR = "Ashish Jangra"
CONTACT_EMAIL = "zangrajazz@gmail.com"

GITHUB = "https://github.com/AshishJangra27"
LINKEDIN = "https://www.linkedin.com/in/ashish-jangra/"
KAGGLE = "https://www.kaggle.com/ashishjangra27"

# --------------------------------------------------------------------------
# Topic landing pages
# --------------------------------------------------------------------------
# key      : the courseData topic key, so the hub's #hash still matches
# dir      : the directory on disk, which is also the URL segment
# h1/lead  : what the page says
# intro    : two or three paragraphs of real copy, because a page that is only
#            a grid of links has nothing for a search engine to rank.

TOPICS = {
    "maths": {
        "dir": "maths",
        "title": "Maths for Machine Learning",
        "h1": "Maths for Machine Learning",
        "lead": "The vectors, matrices, derivatives and probability that every "
                "machine learning course assumes you already have.",
        "keywords": "maths for machine learning, linear algebra visualization, "
                    "calculus for ML, probability basics, vectors and matrices",
        "intro": [
            "Almost every machine learning explanation stops to say \"recall that the "
            "gradient points uphill\" or \"this is just a dot product\" and moves on. "
            "This track is where you go to actually see those things, one at a time, "
            "with something you can drag.",
            "It starts at the equation of a line and works up through vectors, matrix "
            "multiplication, derivatives and probability distributions. Nothing here "
            "assumes a maths degree, and nothing is left as an exercise for the reader.",
        ],
    },
    "ml": {
        "dir": "machine_learning",
        "title": "Machine Learning",
        "h1": "Machine Learning, Visualised",
        "lead": "Classifiers, regressors, clustering and the evaluation metrics "
                "that tell you whether any of it worked.",
        "keywords": "machine learning visualization, interactive KNN, decision tree "
                    "explained, confusion matrix, cross validation, SVM margin",
        "intro": [
            "A machine learning model is easier to trust once you have watched it get "
            "things wrong. Every module in this track puts the model on screen with the "
            "controls that drive it, so you can push it into failure on purpose: set k "
            "to 1 and watch KNN overfit, unbalance the classes and watch accuracy stay "
            "high while the model becomes useless.",
            "The track runs from splitting data through the classical algorithms - "
            "linear regression, KNN, decision trees, naive Bayes, SVM, k-means - and "
            "ends on the evaluation and drift questions you hit once a model is real.",
        ],
    },
    "dl": {
        "dir": "deep_learning",
        "title": "Deep Learning",
        "h1": "Deep Learning, One Layer at a Time",
        "lead": "From a single perceptron to backpropagation, optimizers, "
                "regularisation and the shape of a training curve.",
        "keywords": "deep learning visualization, neural network explained, "
                    "backpropagation interactive, gradient descent, optimizers, dropout",
        "intro": [
            "Deep learning is a small number of ideas repeated at scale. This track "
            "introduces them in the order they build: one weighted sum, then an "
            "activation, then a layer, then a loss, then the gradient that moves the "
            "weights, then everything people add to stop it going wrong.",
            "Because each page animates a single step, you can see what a learning rate "
            "actually does to a descent path, why a training curve separates from the "
            "validation curve, and what dropout removes on each forward pass.",
        ],
    },
    "dsa": {
        "dir": "dsa",
        "title": "Algorithms & Data Structures",
        "h1": "Algorithms & Data Structures",
        "lead": "Sorting, searching, graphs, trees, recursion and dynamic "
                "programming - animated step by step.",
        "keywords": "algorithm visualization, sorting algorithms animated, binary "
                    "search, dijkstra, dynamic programming, big o notation, data structures",
        "intro": [
            "Algorithms are the one part of computer science where an animation is "
            "obviously better than prose: the whole point is what changes on each step. "
            "This is the largest track on VizLearn, running from Big-O notation through "
            "the sorts, the searches, linked structures, trees, heaps, graphs, and the "
            "recursion-and-memoisation family.",
            "Each page runs the algorithm at your pace, highlighting the comparison or "
            "the pointer move that just happened, with the complexity written out "
            "underneath so the cost is attached to the behaviour rather than memorised "
            "separately.",
        ],
    },
    "nlp": {
        "dir": "natural_language_processing",
        "title": "Natural Language Processing",
        "h1": "Natural Language Processing",
        "lead": "How text becomes numbers: characters, tokens, embeddings, "
                "recurrence and attention.",
        "keywords": "NLP visualization, tokenization explained, word embeddings, "
                    "attention mechanism, transformer explained, TF-IDF, word2vec",
        "intro": [
            "Everything a language model does rests on one uncomfortable fact: the model "
            "never sees words. This track follows a piece of text all the way down - "
            "characters to codes, codes to tokens, tokens to vectors - and then back up "
            "through the architectures that read those vectors in order.",
            "It covers the recurrent family in full: what a recurrent cell holds, why "
            "backpropagation through time makes long sequences hard, and how LSTM's four "
            "gates were designed to fix exactly that. It ends on GRUs and bidirectional "
            "layers.",
        ],
    },
    "computer-vision": {
        "dir": "computer_vision",
        "title": "Computer Vision",
        "h1": "Computer Vision",
        "lead": "Pixels, filters, feature maps and the convolutional stack that "
                "turns an image into a prediction.",
        "keywords": "computer vision visualization, CNN explained, convolution filter, "
                    "feature map, padding and strides, image augmentation, transfer learning",
        "intro": [
            "A convolutional network is usually drawn as a row of coloured boxes that "
            "explains nothing. This track takes the boxes apart: what a filter is, what "
            "it produces, why the output shrinks, what padding restores, and what a "
            "stride costs you.",
            "It starts with how an image is stored at all - grayscale intensities, then "
            "RGB channels - and finishes on the practical layer: augmentation, data "
            "loaders and transfer learning.",
        ],
    },
    "db": {
        "dir": "database",
        "title": "Databases & SQL",
        "h1": "Databases & SQL",
        "lead": "Relational and non-relational models, and the SQL clauses that "
                "actually run against them.",
        "keywords": "SQL visualization, sql joins explained, group by, window functions, "
                    "common table expressions, relational database basics",
        "intro": [
            "SQL is declarative, which is exactly why it is hard to learn: you write what "
            "you want and the engine decides how. These pages show the how. Run a join "
            "and watch rows pair up; run a GROUP BY and watch rows collapse into one.",
            "The track covers the relational model and its NoSQL alternative, then works "
            "through the clauses in the order a query is actually evaluated, ending on "
            "window functions and CTEs.",
        ],
    },
    "gen-ai": {
        "dir": "gen_ai",
        "title": "Generative AI & LLMs",
        "h1": "Generative AI & LLMs",
        "lead": "Tokenizers, next-token prediction, and the techniques that make "
                "large models trainable and servable.",
        "keywords": "LLM explained, how llms predict next word, byte pair encoding, "
                    "LoRA explained, quantization, knowledge distillation, masked language modeling",
        "intro": [
            "A large language model predicts one token at a time. Everything else - the "
            "tokenizer in front of it, the fine-tuning that specialises it, the "
            "quantization that fits it on a smaller card - exists to serve that loop.",
            "This track starts with how text is split and encoded, moves through the two "
            "training objectives that produced most current models, and ends on the "
            "practical techniques: LoRA, quantization and distillation.",
        ],
    },
}

# Display order on the hub and in the footer.
TOPIC_ORDER = ["maths", "ml", "dl", "dsa", "nlp", "computer-vision", "db", "gen-ai"]

DIR_TO_TOPIC = {t["dir"]: k for k, t in TOPICS.items()}


def topic_url(key):
    return "%s/%s/" % (SITE, TOPICS[key]["dir"])


def topic_rel(key):
    """Path on disk, relative to the repo root."""
    return "%s/index.html" % TOPICS[key]["dir"]


# --------------------------------------------------------------------------
# Static pages
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Tool pages
# --------------------------------------------------------------------------
# Neither modules nor landing pages: study tools built on top of the catalog
# and on what the reader's own browser has recorded. Each is served
# directory-style (/practice/, /glossary/) and each needs the same wiring -
# sitemap entry, OG card, breadcrumb, footer link, description - so they are
# declared once here rather than special-cased in six build steps.
#
# `footer` decides whether the page is advertised in the site footer; the
# policy pages already fill that column, so only the tools a reader has a
# reason to open twice go in.

TOOL_PAGES = {
    "practice": {
        "dir": "practice",
        "rel": "practice/index.html",
        "title": "Practice",
        "footer": True,
        "lead": "Questions drawn from the modules you have actually opened, weighted "
                "by what you got wrong and how long ago you saw it.",
        "description": "Spaced practice across every VizLearn module, drawn from the "
                       "checks you have already answered and weighted by what you got "
                       "wrong. Runs entirely in your browser.",
    },
}

TOOL_ORDER = list(TOOL_PAGES)
TOOL_BY_REL = {t["rel"]: t for t in TOOL_PAGES.values()}

# Kept as a name because build_practice.py reads its copy from here.
PRACTICE = TOOL_PAGES["practice"]


def is_tool_page(rel):
    return rel in TOOL_BY_REL


def tool_page(rel):
    """The tool-page record for `rel`, or None if it is not one."""
    return TOOL_BY_REL.get(rel)


def is_practice_page(rel):
    return rel == PRACTICE["rel"]


STATIC_PAGES = ["about.html", "contact.html", "privacy.html", "terms.html"]

STATIC_TITLES = {
    "about.html": "About VizLearn",
    "contact.html": "Contact",
    "privacy.html": "Privacy Policy",
    "terms.html": "Terms of Use",
}

# schema.org @type per static page.
STATIC_LD_TYPE = {
    "about.html": "AboutPage",
    "contact.html": "ContactPage",
    "privacy.html": "PrivacyPolicyPage",
    "terms.html": "WebPage",
}


def is_topic_page(rel):
    return rel.endswith("/index.html") and rel.split("/")[0] in DIR_TO_TOPIC


def is_static_page(rel):
    return rel in STATIC_PAGES


def page_url(rel):
    """Canonical URL for any routable page.

    Topic pages are served directory-style (`/dsa/`, not `/dsa/index.html`) so
    the canonical, the sitemap and the internal links all have to agree on the
    trailing-slash form.
    """
    if rel == "index.html":
        return SITE + "/"
    if is_topic_page(rel) or is_tool_page(rel):
        return "%s/%s/" % (SITE, rel.split("/")[0])
    return SITE + "/" + rel


# --------------------------------------------------------------------------
# Dates
# --------------------------------------------------------------------------

_date_cache = {}


def last_modified(rel):
    """Date of the last commit that touched this file (YYYY-MM-DD).

    Falls back to today for files that are not committed yet, which is what a
    brand-new generated page will be on its first build.
    """
    if rel in _date_cache:
        return _date_cache[rel]
    out = ""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ).stdout.strip()
    except OSError:
        out = ""
    if not out:
        import datetime
        out = datetime.date.today().isoformat()
    _date_cache[rel] = out
    return out


def first_published(rel):
    """Date of the first commit that touched this file (YYYY-MM-DD)."""
    key = "first:" + rel
    if key in _date_cache:
        return _date_cache[key]
    out = ""
    try:
        log = subprocess.run(
            ["git", "log", "--format=%cs", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ).stdout.strip().splitlines()
        if log:
            out = log[-1].strip()
    except OSError:
        out = ""
    if not out:
        out = last_modified(rel)
    _date_cache[key] = out
    return out


def pretty_date(iso):
    """2026-08-01 -> 1 August 2026"""
    import datetime
    try:
        d = datetime.date.fromisoformat(iso)
    except ValueError:
        return iso
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def all_routable(mods):
    """Every URL the site should expose, in sitemap order."""
    rels = ["index.html"]
    rels += [topic_rel(k) for k in TOPIC_ORDER]
    rels += [m["path"] for m in mods]
    rels += STATIC_PAGES
    rels += [TOOL_PAGES[k]["rel"] for k in TOOL_ORDER]
    return rels
