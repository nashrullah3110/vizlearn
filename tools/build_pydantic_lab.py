#!/usr/bin/env python3
"""Render /pydantic-lab/ - a full-page Pydantic editor.

Same contract as /python-lab/: one large `.vz-py` block, and
assets/vizlearn-python.js does the work. The one difference is the
`data-vz-packages` attribute, which tells the shared worker to load a library
before it executes.

Pydantic is not installed from PyPI at run time. Pyodide ships pydantic 2.7.0
and a prebuilt pydantic_core wasm32 wheel in its own lockfile, on the same CDN
the interpreter comes from, so `loadPackage("pydantic")` is one more fetch
against a host the page already talks to - no micropip, no PyPI, no CORS.

The starter is written to fail on purpose in its last block. A validator you
never see reject anything is indistinguishable from a type annotation, and the
error is the thing worth reading.

Written whole on every build; no hand-edited regions.
"""

import sys

import lib_tool_page as tool

KEY = "pydantic-lab"

CSS = """
        .vz-lab-grid { display: grid; gap: 1.25rem; grid-template-columns: 1fr; }
        @media (min-width: 1024px) {
            .vz-lab-grid { grid-template-columns: minmax(0, 1fr) 19rem; align-items: start; }
        }
        /* The editor is the point of the page, so it gets real height rather
           than the few lines a module needs beside its prose. */
        .vz-lab-grid .py-output { min-height: 150px; }

        .vz-lab-side {
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            background: var(--card-bg);
            padding: 1rem 1.1rem;
        }
        .vz-lab-side h2 {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem; font-weight: 700;
            letter-spacing: 0.16em; text-transform: uppercase;
            color: var(--accent-primary); margin-bottom: 0.6rem;
        }
        .vz-lab-side p, .vz-lab-side li {
            font-size: 0.86rem; line-height: 1.6; color: var(--text-muted);
        }
        .vz-lab-side ul { list-style: disc; padding-left: 1.15rem; display: grid; gap: 0.4rem; }
        .vz-lab-side + .vz-lab-side { margin-top: 1rem; }
        .vz-lab-side code {
            font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
            background: var(--input-bg); border: 1px solid var(--border-subtle);
            border-radius: 4px; padding: 0.05em 0.3em; color: var(--text-main);
        }
        .vz-lab-side a { color: var(--accent-primary); text-decoration: none; }
        .vz-lab-side a:hover { text-decoration: underline; }
"""

STARTER = '''# Real Pydantic v2, running in your browser. Nothing is sent to a server.
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator
import pydantic

print("pydantic", pydantic.VERSION)
print()


class Address(BaseModel):
    city: str
    pin: str = Field(min_length=6, max_length=6)


class User(BaseModel):
    name: str
    age: int = Field(ge=0, le=130)
    email: Optional[str] = None
    tags: List[str] = []
    address: Optional[Address] = None

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name cannot be blank")
        return v.strip().title()


# 1. Coercion. Note what happens to the string "36" and to age's type.
u = User(name="  ada lovelace  ", age="36", tags=["maths", "engine"])
print("model  :", u)
print("age is :", type(u.age).__name__)
print("json   :", u.model_dump_json())
print()

# 2. Nested models are built from plain dicts.
u2 = User(name="Grace", age=45, address={"city": "New York", "pin": "100011"})
print("nested :", u2.address)
print("dict   :", u2.model_dump(exclude_none=True))
print()

# 3. Now the part worth reading: what a failure looks like.
try:
    User(name="", age=200, tags="not-a-list", address={"city": "Delhi", "pin": "11"})
except ValidationError as e:
    print("errors :", e.error_count())
    print(e)

# Try editing this, or delete it and write your own models.
'''


def body():
    return """
            <div class="vz-py vz-ide" data-vz-py data-vz-packages="pydantic" data-vz-ide="pydantic-lab">
                <div class="vz-ide-pane vz-ide-code">
                <script type="text/plain" class="py-src">%(starter)s</script>
                <div class="vz-code-bar">
                    <span class="vz-code-dot"></span><span>models.py</span>
                    <span class="vz-code-lang">Pydantic v2</span>
                </div>
                <!-- The textarea keeps .py-editor: assets/vizlearn-python.js reads
                     .value off it. The highlighter only layers a <pre> behind it. -->
                <div class="vz-code" data-vz-code="python">
                    <div class="vz-code-gutter" aria-hidden="true"></div>
                    <div class="vz-code-scroll">
                        <pre class="vz-code-hl" aria-hidden="true"></pre>
                        <textarea class="vz-code-input py-editor" aria-label="Pydantic code editor"
                                  spellcheck="false" autocapitalize="off" autocomplete="off"></textarea>
                    </div>
                </div>
                <div class="py-controls">
                    <button type="button" class="py-run-btn">Run</button>
                    <button type="button" class="py-reset-btn">Reset</button>
                    <span class="py-status"></span>
                </div>
                </div>
                <div class="vz-ide-split" role="separator" tabindex="0"
                     aria-orientation="vertical" aria-label="Resize editor and output"
                     aria-valuemin="20" aria-valuemax="80" aria-valuenow="50"></div>
                <div class="vz-ide-pane vz-ide-out">
                <div class="vz-console">
                    <div class="vz-console-bar">Output</div>
                    <!-- .py-output stays: vizlearn-python.js writes into it. -->
                    <pre class="vz-console-body py-output" aria-live="polite"
                         data-empty="Press Run to execute this code."></pre>
                </div>
                </div>
            </div>

        <div class="vz-lab-docs">
                <section class="vz-lab-side">
                    <h2>What this is</h2>
                    <p>Pydantic v2 &mdash; the real library, not a reimplementation &mdash;
                    running on CPython compiled to WebAssembly, on your own machine. Your
                    code is never uploaded.</p>
                    <p>The first <code>Run</code> takes a few seconds: it downloads the
                    interpreter and then Pydantic. Every run after that is immediate, and
                    the library stays loaded for the rest of your visit.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>What works</h2>
                    <ul>
                        <li><code>BaseModel</code>, <code>Field</code>, and the whole
                            constraint set &mdash; <code>ge</code>, <code>le</code>,
                            <code>min_length</code>, <code>pattern</code>.</li>
                        <li><code>field_validator</code> and <code>model_validator</code>,
                            in both <code>before</code> and <code>after</code> mode.</li>
                        <li>Nested models, <code>List</code>, <code>Dict</code>,
                            <code>Optional</code>, <code>Union</code>, <code>Literal</code>
                            and discriminated unions.</li>
                        <li><code>model_dump</code>, <code>model_dump_json</code>,
                            <code>model_validate</code> and
                            <code>model_validate_json</code>.</li>
                        <li><code>ValidationError</code> in full &mdash; every error, with
                            its location, type and input value.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>What does not</h2>
                    <ul>
                        <li><code>input()</code> &mdash; there is no stdin to read from.</li>
                        <li>Network calls, so no fetching a schema or a payload from a URL.</li>
                        <li>Packages beyond the standard library and Pydantic itself.
                            <code>pydantic-settings</code> and <code>email-validator</code>
                            are separate distributions and are not loaded here.</li>
                        <li>Reading or writing files on your computer. There is an in-memory
                            filesystem, so <code>open</code> works, but the files vanish
                            with the run.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>How it runs</h2>
                    <p>This is not a validator written in JavaScript to look like Pydantic.
                    It is Pydantic 2.7 on CPython 3.12, both compiled to WebAssembly by the
                    Pyodide project, including <code>pydantic-core</code> &mdash; the Rust
                    engine that does the actual validating. Behaviour matches a normal
                    install because it is one.</p>
                    <p>It runs in a worker thread, separate from the page, so an accidental
                    infinite loop freezes the output rather than the tab. A run that has not
                    finished within ten seconds is stopped and reported.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Reading a ValidationError</h2>
                    <p>Pydantic does not stop at the first problem. It checks every field
                    and raises once, so the report you get back is the complete list &mdash;
                    which is why the count on the first line is often greater than one.</p>
                    <p>Each entry has three parts worth reading separately. The
                    <strong>location</strong> is a path, not a name: <code>address.pin</code>
                    means the failure is one level down, and <code>tags.0</code> means the
                    first element of a list. The <strong>type</strong> is a stable machine
                    code such as <code>greater_than_equal</code> or
                    <code>string_too_short</code>, and it is what you match on if you are
                    turning errors into an API response. The <strong>input value</strong> is
                    what was actually received, which is usually the fastest way to see that
                    a caller sent a string where a number was meant.</p>
                    <p><code>e.errors()</code> gives you all of that as a list of
                    dictionaries rather than as text.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Coercion is the thing to test</h2>
                    <p>Most surprises with Pydantic are about what it will quietly convert.
                    In the default lax mode the string <code>"36"</code> becomes the integer
                    <code>36</code>, but <code>"thirty-six"</code> raises. A float
                    <code>36.0</code> becomes <code>36</code>; <code>36.5</code> does not.</p>
                    <p>This is exactly the sort of thing that is faster to settle by running
                    it than by reading about it. Change a value in the starter, press
                    <code>Run</code>, and see which way it goes. If you want the strict
                    answer instead, try <code>model_config = ConfigDict(strict=True)</code>
                    on the model and run the same inputs again.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Things worth trying</h2>
                    <ul>
                        <li>Feed a model a JSON string with
                            <code>User.model_validate_json(...)</code> and see the same
                            validation apply.</li>
                        <li>Add <code>model_config = ConfigDict(extra="forbid")</code> and
                            pass a key the model does not declare.</li>
                        <li>Print <code>User.model_json_schema()</code> &mdash; the JSON
                            Schema that FastAPI turns into your API documentation.</li>
                        <li>Write a <code>model_validator(mode="after")</code> that compares
                            two fields, which a per-field validator cannot do.</li>
                        <li>Break something deliberately and read the error. Recognising the
                            error types is most of using this library.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>Want plain Python?</h2>
                    <p>The <a href="%(p)spython-lab/">Python compiler</a> is the same editor
                    without the library, and the <a href="%(p)spython/">Python track</a>
                    teaches the language one idea at a time &mdash; starting at
                    <a href="%(p)spython/hello_python.html">your first print
                    statement</a>.</p>
                </section>
            </div>
        </div>

""" % {"starter": STARTER.strip(), "p": "%(p)s"}


def main():
    rel = tool.write(KEY, tool.render(KEY, CSS, body(), wide=True, app=True))
    print("pydantic lab page         : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
