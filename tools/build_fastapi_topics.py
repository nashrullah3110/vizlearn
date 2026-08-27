#!/usr/bin/env python3
"""Render the FastAPI modules from tools/fastapi_topics.py.

The shape differs from the Python track's on purpose. There, a module is two
substantial programs beside a notes column. Here a module is a *sequence* of
short steps - heading, one sentence, one small program - because Pydantic is
a set of small rules that interact, and a single long script hides which rule
produced which line of output.

Every editor carries data-vz-packages="pydantic". The blocks on a page share
one interpreter, so the library downloads once however many steps there are.

The article text is written to content/articles/fastapi/ where
build_articles.py picks it up, and the questions reach build_labs.py through
tools/labs.py.

    python3 tools/build_fastapi_topics.py
"""

import html
import json
import os
import sys

import lib_shell as shell
from lib_catalog import ROOT, read_course_data
from lib_pages import last_modified, pretty_date
from fastapi_topics import TOPICS

PREFIX = "../"
DIR = "fastapi"
TOPIC_KEY = "fastapi"

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
    return """                <div class="vz-py" data-vz-py data-vz-packages="pydantic,ssl"%(extra)s data-vz-label="FastAPI">
                    %(pre)s<script type="text/plain" class="py-src">%(code)s</script>
                    <div class="vz-code-bar">
                        <span class="vz-code-dot"></span><span>%(file)s</span>
                        <span class="vz-code-lang">FastAPI</span>
                    </div>
                    <div class="vz-code" data-vz-code="python">
                        <div class="vz-code-gutter" aria-hidden="true"></div>
                        <div class="vz-code-scroll">
                            <pre class="vz-code-hl" aria-hidden="true"></pre>
                            <textarea class="vz-code-input py-editor" aria-label="FastAPI code editor"
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


# Every module here needs the same four wheels and the same test client, so
# unlike the Pydantic track these are defaults rather than per-topic opt-ins.
# The prelude is imported from build_fastapi_lab rather than copied, so the
# lab and the track cannot drift.
WHEELS = ["sniffio-1.3.1-py3-none-any.whl",
          "anyio-4.6.2.post1-py3-none-any.whl",
          "starlette-0.41.3-py3-none-any.whl",
          "fastapi-0.115.6-py3-none-any.whl"]


def page(t):
    rel = rel_for(t)
    iso = last_modified(rel)
    head = shell.head_top("%s | VizLearn" % t["title"], PREFIX).replace(
        "/* page-specific rules go here; the shared system is in vizlearn.css */",
        CSS.strip("\n"))

    from build_fastapi_lab import PRELUDE
    wheels = list(WHEELS) + list(t.get("wheels", ()))
    # `drive` is the lab's internal coroutine runner under a name a lesson can
    # use: one module calls the app through ASGI by hand to show what a server
    # actually does.
    prelude = (t.get("prelude") or PRELUDE) + "\n\ndrive = _drive\n"
    steps = "\n".join(step_card(i + 1, h, b, c, wheels, prelude)
                      for i, (h, b, c) in enumerate(t["steps"]))

    notes = "\n".join('                        <div class="py-note">%s</div>' % n
                      for n in t["notes"])

    main = """
    <main class="flex-1 p-4 md:p-8 max-w-[1600px] mx-auto w-full">
        <div class="mb-8 animate-fade-in">
            %(crumb)s
            <h1 class="text-3xl md:text-4xl font-bold" style="color: var(--text-main)">%(title)s</h1>
            <p class="vz-pt-lead">%(lead)s</p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">
            <div class="lg:col-span-7 space-y-6" data-vz-viz>
%(steps)s
            </div>
            <div class="lg:col-span-5 space-y-6">
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
                                       ("FastAPI", PREFIX + DIR + "/"),
                                       (t["cat"], None)]),
        "title": esc(t["title"]),
        "lead": esc(t["lead"]),
        "steps": steps,
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
             encoding="utf-8").write(t["article"].strip() + "\n")

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
    print("fastapi pages written  : %d" % len(TOPICS))
    print("runnable steps         : %d" % steps)
    print("articles written       : %d" % len(TOPICS))
    print("catalog                : %d added, %d total in the track"
          % (added, len(data[TOPIC_KEY]["courses"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
