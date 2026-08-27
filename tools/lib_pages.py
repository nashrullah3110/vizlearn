"""Metadata for the pages that are not modules.

Until now every routable URL was either index.html or one of the module
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
import re
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
    "python": {
        "dir": "python",
        "title": "Python",
        "h1": "Python, by Running It",
        "lead": "The language every other track assumes. Real code, run in your "
                "browser, from your first print to your first functions.",
        "keywords": "learn python interactively, python basics, python variables, "
                    "python loops, python functions, run python in browser",
        "intro": [
            "Every other track on this site writes Python in its examples, and every one "
            "of them assumes you already speak it. This is where you learn it - not from "
            "reading, but from running. Every module embeds a real Python interpreter, "
            "so the code on the page is not a screenshot: you can change it and press "
            "Run and see what actually happens.",
            "The track starts at your first print statement and works up through "
            "variables, numbers, strings, lists, conditionals and functions - the "
            "handful of ideas every later module leans on.",
        ],
    },
    "pydantic": {
        "dir": "pydantic",
        "title": "Pydantic",
        "h1": "Pydantic, by Running It",
        "lead": "Type annotations that actually do something. Validation, coercion "
                "and serialisation, each one runnable on the page.",
        "keywords": "pydantic tutorial, pydantic basemodel, pydantic validation, "
                    "pydantic v2, python data validation, pydantic field",
        "intro": [
            "A Python type annotation does nothing at runtime. Write "
            "<code>def price(x: int)</code> and Python will hand your function the "
            "string \"cat\" without a word of complaint. Pydantic is the library that "
            "makes those annotations real - it reads them, checks the data against "
            "them, and tells you precisely what was wrong when it does not fit.",
            "This track works up from a first model to validators, serialisation and "
            "schemas. Every idea arrives as a small program you can run and edit on "
            "the page, because the fastest way to settle what Pydantic does with a "
            "value is to hand it one and look.",
        ],
    },
    "fastapi": {
        "dir": "fastapi",
        "title": "FastAPI",
        "h1": "FastAPI, by Calling It",
        "lead": "Routes, validation and documentation that come from the same "
                "annotations - each one runnable on the page.",
        "keywords": "fastapi tutorial, fastapi path parameters, fastapi dependencies, "
                    "fastapi response model, python api framework, fastapi testing",
        "intro": [
            "FastAPI is a thin, well-chosen layer over two ideas you can learn "
            "separately: ASGI, which is what a Python web application actually is, "
            "and Pydantic, which turns your annotations into validation. Almost "
            "everything that looks like framework magic is one of those two doing "
            "its job.",
            "This track works up from a first route to dependencies, middleware and "
            "testing. There is no server on these pages - a browser tab cannot "
            "listen on a port - so a test client calls the app the way a server "
            "would, which means routing, validation, status codes and the generated "
            "schema all behave exactly as they do in production.",
        ],
    },
    "interview": {
        "dir": "interview",
        "title": "Interview Questions",
        "h1": "Interview Questions, Answered by Running Them",
        "lead": "The questions actually asked about strings, lists and "
                "dictionaries - each with the code, run in your browser.",
        "keywords": "python interview questions, dsa interview questions, string "
                    "interview questions, list interview questions, dictionary "
                    "interview questions, two pointers, sliding window, time complexity",
        "intro": [
            "Interview answers are not recall problems. \"Why is this O(n²)?\" is "
            "answered properly by showing the count, and \"which is faster?\" by "
            "measuring both - which is what every page here does. Each question "
            "gets its own page: the answer in prose, a visualisation that steps "
            "through the mechanism, and a real Python interpreter with the "
            "implementation already in it.",
            "The track is organised the way the questions are asked - strings, "
            "then lists and arrays, then dictionaries, hashing and the "
            "complexity traps that catch most candidates. Conceptual questions "
            "and coding problems sit side by side, because interviews mix them.",
        ],
    },
}

# Display order on the hub and in the footer.
TOPIC_ORDER = ["maths", "ml", "dl", "dsa", "nlp", "computer-vision", "db",
               "gen-ai", "python", "pydantic", "fastapi", "interview"]

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
    "map": {
        "dir": "map",
        "rel": "map/index.html",
        "title": "Concept Map",
        "footer": True,
        "lead": "How the tracks connect - what each module builds on, and where "
                "you have got to.",
        "description": "An interactive map of every VizLearn track in teaching "
                       "order, showing what each module builds on and how the "
                       "tracks connect to one another.",
    },
    "whats-new": {
        "dir": "whats-new",
        "rel": "whats-new/index.html",
        "title": "What's New",
        "footer": True,
        "lead": "Everything added to VizLearn, newest first.",
        "description": "A running log of the modules and features added to "
                       "VizLearn, newest first, read straight from the "
                       "repository history.",
    },
    "glossary": {
        "dir": "glossary",
        "rel": "glossary/index.html",
        "title": "Glossary",
        "footer": True,
        "lead": "Every term the modules assume you already know, defined once "
                "and linked back to the module that teaches it properly.",
        "description": "A plain-English glossary of the machine learning, deep "
                       "learning, retrieval and SQL terms used across VizLearn, "
                       "each linked to the interactive module that explains it.",
    },
    "python-lab": {
        "dir": "python-lab",
        "rel": "python-lab/index.html",
        "title": "Python Compiler",
        "footer": True,
        "lead": "Write Python and run it. Real CPython in your browser - no install, "
                "no account, nothing sent to a server.",
        "description": "A free online Python compiler. Write and run real Python 3 in "
                       "your browser with no setup - CPython compiled to WebAssembly, "
                       "running entirely on your own machine.",
    },
    "sql-lab": {
        "dir": "sql-lab",
        "rel": "sql-lab/index.html",
        "title": "SQL Playground",
        "footer": True,
        "lead": "Create tables, insert rows and query them. A real SQLite database "
                "living in your browser tab, with the schema and results shown as you go.",
        "description": "A free online SQL playground. Run CREATE, INSERT and SELECT "
                       "against a real SQLite database in your browser, and see the "
                       "tables and query results immediately.",
    },
    "js-lab": {
        "dir": "js-lab",
        "rel": "js-lab/index.html",
        "title": "JavaScript Compiler",
        "footer": True,
        "lead": "Write JavaScript and run it. Your browser's own engine in a worker "
                "thread - no install, no account, nothing sent to a server.",
        "description": "A free online JavaScript compiler. Write and run real "
                       "JavaScript in your browser with no setup - the engine runs "
                       "in a Web Worker, entirely on your own machine.",
    },
    "html-lab": {
        "dir": "html-lab",
        "rel": "html-lab/index.html",
        "title": "HTML Playground",
        "footer": True,
        "lead": "Write HTML, CSS and inline scripts and see them render instantly "
                "in a sandboxed preview - no tooling, nothing uploaded.",
        "description": "A free online HTML playground. Write HTML with CSS and "
                       "inline JavaScript, and see a live sandboxed preview in your "
                       "browser - entirely offline, with console output shown as you go.",
    },
    "pydantic-lab": {
        "dir": "pydantic-lab",
        "rel": "pydantic-lab/index.html",
        "title": "Pydantic Compiler",
        "footer": True,
        "lead": "Write Pydantic models and run them. Real Pydantic v2 on real CPython, "
                "in your browser - no install, no account, nothing sent to a server.",
        "description": "A free online Pydantic compiler. Define BaseModel classes and "
                       "run them against real data in your browser - Pydantic v2 on "
                       "CPython compiled to WebAssembly, with full validation errors.",
    },
    "fastapi-lab": {
        "dir": "fastapi-lab",
        "rel": "fastapi-lab/index.html",
        "title": "FastAPI Compiler",
        "footer": True,
        "lead": "Define routes and call them. A real FastAPI app running in your "
                "browser - no server, no install, nothing sent anywhere.",
        "description": "A free online FastAPI compiler. Write real FastAPI routes and "
                       "call them in your browser - path and query validation, Pydantic "
                       "request bodies, status codes and the generated OpenAPI schema.",
    },
    "notebook": {
        "dir": "notebook",
        "rel": "notebook/index.html",
        "title": "Python Notebook",
        "footer": True,
        "lead": "Cells that share one kernel, with NumPy, pandas and Matplotlib "
                "loaded. Charts and DataFrames render inline - no install, nothing "
                "sent to a server.",
        "description": "A free online Python notebook with NumPy, pandas and "
                       "Matplotlib. Run cells that share state, and see DataFrames "
                       "as tables and plots as charts - entirely in your browser.",
    },
    "saved": {
        "dir": "saved",
        "rel": "saved/index.html",
        "title": "Saved",
        "footer": True,
        "lead": "The modules you bookmarked and the notes you left on them.",
        "description": "Your bookmarked VizLearn modules and the notes you left "
                       "on them, kept in your browser and nowhere else.",
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
_dirty = None


# The date a page advertises is written into the page, so "has this file
# changed since HEAD" is circular: stamping today's date makes the file
# differ from HEAD, which makes it look changed, which stamps today's date.
# Normalising every date out of both sides before comparing breaks the loop -
# what is left is the actual content, and only a change to that counts.
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_LONG_DATE = re.compile(
    r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|"
    r"September|October|November|December) \d{4}\b")


def _undated(text):
    return _LONG_DATE.sub("D", _ISO_DATE.sub("D", text))


def _uncommitted():
    """Paths whose content differs from HEAD, ignoring dates.

    The build runs before the commit, so asking git for "the last commit that
    touched this file" gives the date of the change *before* the one being
    built. That silently backdated every page a build had just rewritten:
    contact.html went from 283 to 650 words and the sitemap still advertised
    the previous day's lastmod, which is the opposite of what it should say
    when the point is to get the page recrawled.

    Read from a single `git diff HEAD -U0` rather than a `git show` per file.
    Every one of the ~35 build steps is its own process and so builds this set
    from scratch; at one subprocess per changed page that was thousands of
    git invocations per build, and the build stopped finishing.

    A file whose non-date lines differ from HEAD changed today, whether or not
    it has been committed yet. A file where only the dates moved did not - and
    that distinction has to be made, because the date a page advertises is
    written into the page, so "has this file changed" is otherwise circular:
    stamping today makes the file differ, which makes it look changed, which
    stamps today.
    """
    global _dirty
    if _dirty is not None:
        return _dirty
    _dirty = set()
    try:
        diff = subprocess.run(
            ["git", "diff", "HEAD", "-U0", "--no-color"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        ).stdout
    except OSError:
        return _dirty

    rel, minus, plus = None, [], []

    def settle():
        if rel is None:
            return
        if sorted(_undated(x) for x in minus) != sorted(_undated(x) for x in plus):
            _dirty.add(rel)

    for line in diff.split("\n"):
        if line.startswith("diff --git "):
            settle()
            # "diff --git a/path b/path" - take the b-side, which is correct
            # for renames as well.
            rel = line.split(" b/", 1)[-1]
            minus, plus = [], []
        elif line.startswith("Binary files") or line.startswith("new file mode"):
            if rel:
                _dirty.add(rel)
        elif line.startswith("+") and not line.startswith("+++"):
            plus.append(line[1:])
        elif line.startswith("-") and not line.startswith("---"):
            minus.append(line[1:])
    settle()
    return _dirty


def last_modified(rel):
    """Date this page's content last changed (YYYY-MM-DD).

    The last commit that touched the file, unless the working tree has since
    changed it - an uncommitted change is today's change, and dating it to
    the previous commit would tell a crawler nothing had happened.
    """
    if rel in _date_cache:
        return _date_cache[rel]
    import datetime
    if rel in _uncommitted():
        out = datetime.date.today().isoformat()
    else:
        out = ""
        try:
            out = subprocess.run(
                ["git", "log", "-1", "--format=%cs", "--", rel],
                cwd=ROOT, capture_output=True, text=True, check=False,
            ).stdout.strip()
        except OSError:
            out = ""
    if not out:
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
