#!/usr/bin/env python3
"""Render the NumPy modules from tools/matplotlib_topics.py.

The shape differs from the Python track's on purpose. There, a module is two
substantial programs beside a notes column. Here a module is a *sequence* of
short steps - heading, one sentence, one small program - because Pydantic is
a set of small rules that interact, and a single long script hides which rule
produced which line of output.

Every editor carries data-vz-packages="matplotlib". The blocks on a page share
one interpreter, so the library downloads once however many steps there are.

The article text is written to content/articles/matplotlib/ where
build_articles.py picks it up, and the questions reach build_labs.py through
tools/labs.py.

    python3 tools/build_matplotlib_topics.py
"""

import html
import json
import os
import re
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data
from lib_pages import last_modified, pretty_date
from matplotlib_topics import TOPICS

PREFIX = "../"
DIR = "matplotlib"
TOPIC_KEY = "matplotlib"

CSS = """
        .py-note {
            border-left: 2px solid var(--border-subtle);
            padding-left: 0.9rem;
            line-height: 1.7;
        }
        .py-note code { color: var(--accent-primary); }
        .vz-pt-lead { margin-top: 0.5rem; max-width: 60ch; color: var(--text-muted); }

        /* A step is numbered so the sequence reads as a sequence rather than
           as six unrelated demos. */
        .vz-step-head { display: flex; align-items: baseline; gap: 0.6rem; }
        .vz-step-n {
            font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
            font-weight: 700; color: var(--accent-primary);
            border: 1px solid var(--border-subtle); border-radius: 5px;
            padding: 0.1rem 0.4rem; flex: none;
        }
        .vz-step-blurb {
            margin: 0.55rem 0 0.9rem; line-height: 1.7;
            color: var(--text-muted); max-width: 68ch;
        }
        .vz-step-blurb code {
            font-family: 'JetBrains Mono', monospace; font-size: 0.85em;
            color: var(--accent-primary);
        }

        /* The walkthrough now lives inside the article, so the notes card is
           the only thing left up here. */
        .vz-notes-wrap { max-width: 1100px; margin: 0 auto; }

        /* An inline editor is part of the prose, not a card floating beside
           it: full reading width, its own breathing room, and the same
           border language as the article's static code blocks. */
        .vz-py-inline {
            margin: 1.4rem 0;
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            overflow: hidden;
        }
        .vz-py-inline .vz-code { border: 0; border-radius: 0; }
        .vz-py-inline .py-controls {
            display: flex; align-items: center; gap: 0.5rem;
            padding: 0.5rem 0.7rem;
            border-top: 1px solid var(--border-subtle);
        }
        .vz-py-inline .vz-console { border-top: 1px solid var(--border-subtle); }
        .vz-py-inline .py-output { min-height: 0; }
"""


def rel_for(t):
    return "%s/%s.html" % (DIR, t["slug"])


def esc(s):
    return html.escape(s, quote=False)


def editor(filename, code, wheels=(), prelude=""):
    """One runnable program, wired to assets/vizlearn-python.js.

    The source is emitted raw. <script> content is raw text, so entities are
    not decoded inside it - escaping would turn `n > 3` into `n &gt; 3` and
    break the program. The only sequence that would need escaping is a
    literal </script>, which is checked for instead.
    """
    if "</script" in code.lower():
        raise SystemExit("%s contains </script and would break out of the tag" % filename)
    extra = ""
    if wheels:
        extra += ' data-vz-wheels="%s"' % ",".join("../assets/wheels/" + w for w in wheels)
    pre = ""
    if prelude:
        pre = ('<script type="text/plain" class="py-prelude">%s</script>\n                    '
               % prelude.strip())
    return """                <div class="vz-py" data-vz-py data-vz-packages="matplotlib"%(extra)s data-vz-label="matplotlib">
                    %(pre)s<script type="text/plain" class="py-src">%(code)s</script>
                    <div class="vz-code-bar">
                        <span class="vz-code-dot"></span><span>%(file)s</span>
                        <span class="vz-code-lang">NumPy</span>
                    </div>
                    <div class="vz-code" data-vz-code="python">
                        <div class="vz-code-gutter" aria-hidden="true"></div>
                        <div class="vz-code-scroll">
                            <pre class="vz-code-hl" aria-hidden="true"></pre>
                            <textarea class="vz-code-input py-editor" aria-label="NumPy code editor"
                                      spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>
                        </div>
                    </div>
                    <div class="py-controls">
                        <button type="button" class="py-run-btn">Run</button>
                        <button type="button" class="py-reset-btn">Reset</button>
                        <span class="py-status"></span>
                    </div>
                    <div class="vz-console">
                        <div class="vz-console-bar">Output</div>
                        <pre class="vz-console-body py-output" aria-live="polite"
                             data-empty="Press Run to execute this code."></pre>
                    </div>
                </div>
""" % {"code": code.rstrip(), "file": esc(filename), "extra": extra, "pre": pre}


def step_card(n, heading, blurb, code, wheels=(), prelude=""):
    return """            <div class="card-container">
                <div class="card-header">
                    <div class="vz-step-head">
                        <span class="vz-step-n">%(n)02d</span>
                        <h2 class="font-bold text-lg" style="color: var(--text-main)">%(head)s</h2>
                    </div>
                </div>
                <div class="p-4 md:p-5">
                    <p class="vz-step-blurb">%(blurb)s</p>
%(editor)s                </div>
            </div>""" % {
        "n": n, "head": esc(heading), "blurb": blurb,
        "editor": editor("step_%02d.py" % n, code, wheels, prelude),
    }



def merged_article(t):
    """The article with the walkthrough steps folded into it.

    The steps used to sit in a column above the article, which meant a reader
    met six programs before any prose explained them and then read an article
    repeating similar code that could not be run. They are now sections of
    the article itself, each a heading, a sentence and a runnable editor.

    They go *after* the article's opening section rather than before it, for
    two reasons: build_lede.py lifts the first section out as the Overview,
    which should stay introductory; and the prose written after them refers
    to "the editor above", which is still true once they sit above it.
    """
    text = t["article"].strip()

    # A step title sometimes matches a heading the article already uses, which
    # would put the same "## Combining conditions" on the page twice. When that
    # happens the prose section is lifted out and folded in under the step's
    # heading instead, after the editor -- so there is one section, and prose
    # that says "the editor above" is talking about the editor directly above.
    def take_section(title):
        m = re.search(r"(?m)^## %s[ \t]*$" % re.escape(title), text)
        if not m:
            return None, text
        end = text.find("\n## ", m.end())
        end = len(text) if end == -1 else end
        return text[m.end():end].strip(), text[:m.start()].rstrip() + text[end:]

    blocks = []
    for heading, blurb, code in t["steps"]:
        body, text = take_section(heading)
        block = ("## %s\n\n%s\n\n```python-run\n%s\n```"
                 % (heading, blurb.strip(), code.rstrip()))
        if body:
            block += "\n\n" + body
        blocks.append(block)
    steps = "\n\n".join(blocks)

    # Split after the first "## " section so the lede is untouched.
    first = text.find("\n## ")
    if first == -1:
        return text + "\n\n" + steps
    second = text.find("\n## ", first + 1)
    if second == -1:
        return text + "\n\n" + steps
    return text[:second] + "\n\n" + steps + text[second:]

def page(t):
    rel = rel_for(t)
    iso = last_modified(rel)
    head = shell.head_top("%s | VizLearn" % t["title"], PREFIX).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        CSS.strip("\n"))


    notes = "\n".join('                        <div class="py-note">%s</div>' % n
                      for n in t["notes"])

    main = """
    <main class="flex-1 p-4 md:p-8 max-w-[1600px] mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="vz-pt-lead">%(lead)s</p>
        </div>
        <div class="animate-fade-in" data-vz-viz>
            <div class="vz-notes-wrap">
                <div class="card-container">
                    <div class="card-header"><h3 class="font-bold text-sm uppercase tracking-wide" style="color: var(--text-muted)">Worth knowing</h3></div>
                    <div class="p-5 space-y-4 text-sm" style="color: var(--text-muted)">
%(notes)s
                    </div>
                </div>
            </div>
        </div>
    </main>
""" % {
        "crumb": shell.breadcrumb_bar([("Home", PREFIX + "index.html"),
                                       ("matplotlib", PREFIX + DIR + "/"),
                                       (t["cat"], None)]),
        "title": esc(t["title"]),
        "lead": esc(t["lead"]),
        "notes": notes,
    }
    mount = """    <!-- auto-article-vizlearn -->
    <section class="px-4 md:px-8 pb-8 max-w-[1600px] mx-auto w-full" data-vz-prose>
        <div class="card-container animate-fade-in">
        </div>
    </section>
"""
    return head + shell.header(PREFIX) + main + mount + shell.close(PREFIX)


def catalog_entry(existing):
    generated = {rel_for(t): {"title": t["title"], "path": rel_for(t), "svg": t["svg"]}
                 for t in TOPICS}
    courses, seen = [], set()
    for course in existing.get("courses", []):
        path = course.get("path", "").lstrip("./")
        courses.append(generated.get(path, course))
        seen.add(path)
    for path, course in generated.items():
        if path not in seen:
            courses.append(course)
    out = dict(existing)
    out["courses"] = courses
    return out, len([p for p in generated if p not in seen])


def main():
    os.makedirs(os.path.join(ROOT, DIR), exist_ok=True)
    for t in TOPICS:
        open(os.path.join(ROOT, rel_for(t)), "w", encoding="utf-8").write(page(t))

    art_dir = os.path.join(ROOT, "content", "articles", DIR)
    os.makedirs(art_dir, exist_ok=True)
    for t in TOPICS:
        open(os.path.join(art_dir, "%s.txt" % t["slug"]), "w",
             encoding="utf-8").write(merged_article(t) + "\n")

    index = os.path.join(ROOT, "index.html")
    src = open(index, encoding="utf-8").read()
    data, start, end = read_course_data(index)
    if TOPIC_KEY not in data:
        raise SystemExit("courseData has no %r topic - add it to index.html first"
                         % TOPIC_KEY)
    data[TOPIC_KEY], added = catalog_entry(data[TOPIC_KEY])
    block = json.dumps(data, indent=4, ensure_ascii=False)
    open(index, "w", encoding="utf-8").write(src[:start] + block + src[end:])

    steps = sum(len(t["steps"]) for t in TOPICS)
    print("matplotlib pages written    : %d" % len(TOPICS))
    print("runnable steps         : %d" % steps)
    print("articles written       : %d" % len(TOPICS))
    print("catalog                : %d added, %d total in the track"
          % (added, len(data[TOPIC_KEY]["courses"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
