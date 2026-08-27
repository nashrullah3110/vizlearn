#!/usr/bin/env python3
"""Render /fastapi-lab/ - a full-page FastAPI editor.

FastAPI is harder than the other labs, and it is worth writing down why.

A browser has no sockets, so uvicorn cannot run and there is nothing to
listen on a port. What a browser *can* do is call the app the way a server
would: ASGI is a plain async function taking (scope, receive, send), so a
request is a dictionary and a response is a list of messages. The prelude
wraps that in a TestClient with the shape the real one has, and the reader
writes `client.get("/items/7")` exactly as they would in a test file.

Three things are load-bearing, and each was a failure first:

  the wheels        FastAPI is not in the Pyodide lockfile. micropip can
                    fetch it, but resolving `fastapi` from PyPI pulls the
                    newest pydantic with it, whose pydantic-core has no wasm
                    build - so the install dies on a Rust wheel. Pinned
                    wheels served from this site fix the version and remove
                    the dependency on PyPI being up. pydantic itself still
                    comes from Pyodide, and must be loaded *first* so
                    micropip sees the requirement as already satisfied.

  ssl               anyio imports it at module scope. It is unvendored from
                    the Pyodide stdlib and has to be asked for by name, or
                    `from fastapi import FastAPI` fails on the import.

  run_in_threadpool Starlette sends a sync `def` endpoint to a threadpool,
                    and this runtime cannot start a thread. Un-patched, the
                    endpoint shape that every FastAPI tutorial opens with
                    fails with "can't start new thread" - so the prelude runs
                    those inline instead. It is the one place the sandbox
                    diverges from a real server, and the page says so.

Written whole on every build; no hand-edited regions.
"""

import sys

import lib_tool_page as tool

KEY = "fastapi-lab"

WHEELS = ",".join("%%(p)sassets/wheels/%s" % w for w in (
    "sniffio-1.3.1-py3-none-any.whl",
    "anyio-4.6.2.post1-py3-none-any.whl",
    "starlette-0.41.3-py3-none-any.whl",
    "fastapi-0.115.6-py3-none-any.whl",
))

CSS = """
        .vz-lab-grid { display: grid; gap: 1.25rem; grid-template-columns: 1fr; }
        @media (min-width: 1024px) {
            .vz-lab-grid { grid-template-columns: minmax(0, 1fr) 19rem; align-items: start; }
        }
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

# Runs before the reader's code, in the same namespace. Kept as small as it
# can be while still letting the editor read like a test file.
PRELUDE = '''
import json as _json
from contextlib import asynccontextmanager

# Starlette hands a sync `def` endpoint to a threadpool. There are no threads
# here, so run it inline. This is the one behaviour that differs from a real
# server: a blocking call in a `def` endpoint blocks everything.
# anyio refuses to do anything until sniffio can name the running async
# library, and sniffio looks for a real running loop. There is none here -
# coroutines are stepped by hand - so every path through anyio raised
# AsyncLibraryNotFoundError, which took yield dependencies and background
# tasks with it. Declaring the library directly is enough: nothing below
# actually needs a loop once the threadpool calls run inline.
import sniffio as _sniffio
try:
    _sniffio.current_async_library_cvar.set("asyncio")
except Exception:
    pass


async def _inline(func, *args, **kwargs):
    return func(*args, **kwargs)

# `from X import run_in_threadpool` binds the name at import time, so every
# module that imported it needs patching - not just the one it came from.
# Missing fastapi.dependencies.utils is why Depends used to fail here with
# "can't start new thread": the dependency solver had its own bound copy.
import starlette.concurrency, starlette.background, starlette.responses
import starlette.routing
import fastapi.concurrency, fastapi.routing
import fastapi.dependencies.utils as _deps

for _mod in (starlette.concurrency, starlette.background, starlette.routing,
             fastapi.concurrency, fastapi.routing, _deps):
    if hasattr(_mod, "run_in_threadpool"):
        _mod.run_in_threadpool = _inline

# anyio.to_thread is what the patched helpers above would otherwise reach.
try:
    import anyio.to_thread as _to_thread
    _to_thread.run_sync = _inline
except Exception:
    pass


@asynccontextmanager
async def _inline_cm(cm):
    """Stands in for contextmanager_in_threadpool - runs a sync CM inline.

    This is what makes a `yield` dependency work, teardown included.
    """
    value = cm.__enter__()
    try:
        yield value
    except Exception as e:
        if not cm.__exit__(type(e), e, e.__traceback__):
            raise
    else:
        cm.__exit__(None, None, None)


async def _inline_iter(it):
    """Stands in for iterate_in_threadpool - drives a sync iterator inline."""
    for item in it:
        yield item


for _mod in (fastapi.concurrency, _deps):
    if hasattr(_mod, "contextmanager_in_threadpool"):
        _mod.contextmanager_in_threadpool = _inline_cm
for _mod in (starlette.concurrency, starlette.responses):
    if hasattr(_mod, "iterate_in_threadpool"):
        _mod.iterate_in_threadpool = _inline_iter


def _drive(coro):
    """Run an ASGI coroutine to completion without an event loop.

    Nothing in a request that never touches real I/O suspends, so one send()
    carries it to StopIteration. If it does suspend there is no loop to hand
    it to, and saying so is better than hanging.
    """
    try:
        coro.send(None)
    except StopIteration as stop:
        return stop.value
    coro.close()
    raise RuntimeError(
        "This endpoint awaited real I/O (a network call, a sleep), which the "
        "browser sandbox cannot run. Remove the await and try again.")


class _ClientResponse:
    """The part of httpx.Response that a FastAPI example actually touches.

    Deliberately *not* called Response. FastAPI has its own Response class
    that readers import and construct, and a test-client class sitting on
    that name in their namespace is a trap - the failure is a confusing
    AttributeError deep in starlette rather than anything that names the
    collision.
    """

    def __init__(self, status_code, headers, content):
        self.status_code = status_code
        self.headers = headers
        self.content = content
        self.text = content.decode("utf-8", "replace")

    def json(self):
        return _json.loads(self.text)

    def __repr__(self):
        return "<Response [%s]>" % self.status_code


class TestClient:
    """Calls the app through ASGI - the same path a real server would use."""

    def __init__(self, app, base_url="http://testserver"):
        self.app = app
        self.base_url = base_url

    def request(self, method, url, json=None, content=None, data=None,
                files=None, headers=None):
        path, _, query = url.partition("?")
        body = b""
        hdrs = [(b"host", b"testserver")]
        if files is not None:
            # multipart, spelled the way httpx spells it: files={"f": (name,
            # content, type)} with data={} for the ordinary fields alongside.
            # Hand-building a multipart body in a lesson teaches the wire
            # format instead of the endpoint, which is the wrong subject.
            #
            # Built with chr(13)+chr(10) and concatenation rather than escape
            # sequences: this whole module is itself a Python string literal,
            # so a backslash here has to survive two rounds of parsing and
            # silently became a real newline the first time it was written.
            boundary = "vizlearnboundary"
            crlf = chr(13) + chr(10)
            parts = []
            for key, value in (data or {}).items():
                head = "--" + boundary + crlf
                head += 'Content-Disposition: form-data; name="' + key + '"'
                head += crlf + crlf
                parts.append((head + str(value) + crlf).encode())
            for key, spec in files.items():
                if isinstance(spec, (bytes, str)):
                    filename, payload, ctype = key, spec, "application/octet-stream"
                elif len(spec) == 2:
                    filename, payload = spec
                    ctype = "application/octet-stream"
                else:
                    filename, payload, ctype = spec
                if isinstance(payload, str):
                    payload = payload.encode()
                head = "--" + boundary + crlf
                head += ('Content-Disposition: form-data; name="' + key +
                         '"; filename="' + filename + '"' + crlf)
                head += "Content-Type: " + ctype + crlf + crlf
                parts.append(head.encode() + payload + crlf.encode())
            parts.append(("--" + boundary + "--" + crlf).encode())
            body = b"".join(parts)
            hdrs.append((b"content-type",
                         ("multipart/form-data; boundary=" + boundary).encode()))
        elif data is not None and isinstance(data, dict):
            from urllib.parse import urlencode as _urlencode
            body = _urlencode(data).encode()
            hdrs.append((b"content-type", b"application/x-www-form-urlencoded"))
        elif data is not None:
            body = data if isinstance(data, bytes) else str(data).encode()
        elif json is not None:
            body = _json.dumps(json).encode()
            hdrs.append((b"content-type", b"application/json"))
        elif content is not None:
            body = content if isinstance(content, bytes) else str(content).encode()
        for key, value in (headers or {}).items():
            hdrs.append((key.lower().encode(), value.encode()))
        hdrs.append((b"content-length", str(len(body)).encode()))

        scope = {
            "type": "http", "asgi": {"version": "3.0", "spec_version": "2.3"},
            "http_version": "1.1", "method": method.upper(), "scheme": "http",
            "path": path, "raw_path": path.encode(), "query_string": query.encode(),
            "root_path": "", "headers": hdrs,
            "client": ("testclient", 50000), "server": ("testserver", 80),
        }

        # After the body, report a disconnect. A streaming response starts a
        # listener that waits for one, and a receive() that never sends it
        # spins forever - which used to hang the worker rather than fail.
        state = {"delivered": False}

        async def receive():
            if state["delivered"]:
                return {"type": "http.disconnect"}
            state["delivered"] = True
            return {"type": "http.request", "body": body, "more_body": False}

        messages = []

        async def send(message):
            messages.append(message)

        _drive(self.app(scope, receive, send))

        status, out_headers, chunks = None, {}, b""
        for message in messages:
            if message["type"] == "http.response.start":
                status = message["status"]
                out_headers = {k.decode(): v.decode()
                               for k, v in message.get("headers", [])}
            elif message["type"] == "http.response.body":
                chunks += message.get("body", b"")
        return _ClientResponse(status, out_headers, chunks)

    def get(self, url, **kw):
        return self.request("GET", url, **kw)

    def post(self, url, **kw):
        return self.request("POST", url, **kw)

    def put(self, url, **kw):
        return self.request("PUT", url, **kw)

    def patch(self, url, **kw):
        return self.request("PATCH", url, **kw)

    def delete(self, url, **kw):
        return self.request("DELETE", url, **kw)
'''

STARTER = '''# Real FastAPI, running in your browser. There is no server and no port -
# `client` calls the app through ASGI, exactly as uvicorn would.
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Bookshop")

BOOKS = {1: {"title": "Dune", "price": 9.99}}


class Book(BaseModel):
    title: str
    price: float = Field(gt=0, description="Must be positive")


@app.get("/books/{book_id}")
def read_book(book_id: int, verbose: Optional[bool] = False):
    if book_id not in BOOKS:
        raise HTTPException(status_code=404, detail="Book not found")
    book = BOOKS[book_id]
    return {"id": book_id, **book} if verbose else {"title": book["title"]}


@app.post("/books/", status_code=201)
def create_book(book: Book):
    new_id = max(BOOKS) + 1
    BOOKS[new_id] = book.model_dump()
    return {"id": new_id, **book.model_dump()}


client = TestClient(app)

# 1. A normal request, and the same one with a query parameter.
print("GET  /books/1          ", client.get("/books/1").json())
print("GET  /books/1?verbose=1", client.get("/books/1?verbose=1").json())
print()

# 2. Creating something. Note the 201, which the decorator asked for.
r = client.post("/books/", json={"title": "Neuromancer", "price": 7.50})
print("POST /books/           ", r.status_code, r.json())
print()

# 3. The three ways it says no.
print("missing  ->", client.get("/books/99").status_code,
      client.get("/books/99").json())
r = client.get("/books/abc")
print("bad path ->", r.status_code, r.json()["detail"][0]["msg"])
r = client.post("/books/", json={"title": "Free", "price": -1})
print("bad body ->", r.status_code, r.json()["detail"][0]["msg"])
print()

# 4. The schema FastAPI generated from the annotations above.
print("routes   :", list(app.openapi()["paths"]))

# Try editing this, or delete it and write your own API.
'''


def body():
    return """
            <div class="vz-py vz-ide" data-vz-py data-vz-packages="pydantic,ssl"
                 data-vz-wheels="%(wheels)s" data-vz-label="FastAPI"
                 data-vz-ide="fastapi-lab">
                <div class="vz-ide-pane vz-ide-code">
                <!-- Runs before the code in the editor, in the same namespace.
                     It is what provides TestClient; see build_fastapi_lab.py. -->
                <script type="text/plain" class="py-prelude">%(prelude)s</script>
                <script type="text/plain" class="py-src">%(starter)s</script>
                <div class="vz-code-bar">
                    <span class="vz-code-dot"></span><span>main.py</span>
                    <span class="vz-code-lang">FastAPI</span>
                </div>
                <!-- The textarea keeps .py-editor: assets/vizlearn-python.js reads
                     .value off it. The highlighter only layers a <pre> behind it. -->
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
                    <p>FastAPI 0.115 on Pydantic 2.7 and CPython 3.12, all compiled to
                    WebAssembly and running on your own machine. Nothing is uploaded and
                    no server is involved.</p>
                    <p>The first <code>Run</code> takes a few seconds while the
                    interpreter and the library download. After that it is immediate.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Where is the server?</h2>
                    <p>There isn't one, and there cannot be: a browser tab cannot listen
                    on a port. But a server is not what makes FastAPI work.</p>
                    <p>Underneath, a FastAPI app is one async function that takes a
                    request as a dictionary and sends a response back as messages. That
                    interface is called <strong>ASGI</strong>, and uvicorn's whole job is
                    to translate real network traffic into it. Skip the network and call
                    the app directly and everything above that line &mdash; routing, type
                    coercion, validation, status codes, the OpenAPI schema &mdash; behaves
                    exactly as it does in production, because it is the same code.</p>
                    <p>That is what <code>client</code> does. It is defined for you before
                    your code runs, and it has the shape of
                    <code>fastapi.testclient.TestClient</code>, so what you write here is
                    what you would write in a test file.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>What works</h2>
                    <ul>
                        <li>Path and query parameters, with the coercion and the 422 that
                            follow from the annotations.</li>
                        <li>Pydantic request bodies and <code>response_model</code>.</li>
                        <li><code>HTTPException</code>, <code>status_code</code>,
                            custom headers, <code>Depends</code>.</li>
                        <li><code>APIRouter</code>, middleware, exception handlers.</li>
                        <li><code>app.openapi()</code> &mdash; the schema that becomes the
                            interactive docs.</li>
                        <li>Both <code>def</code> and <code>async def</code> endpoints.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>What does not</h2>
                    <ul>
                        <li><code>uvicorn.run(...)</code> and anything else that needs a
                            socket. Use <code>client</code> instead.</li>
                        <li>Real I/O inside an endpoint &mdash; a network call, an
                            <code>asyncio.sleep</code>, a database driver. There is no
                            event loop to suspend into, and you will get a clear error
                            rather than a hang.</li>
                        <li>The <code>/docs</code> page, which needs a browser pointed at
                            a running server. <code>app.openapi()</code> gives you the
                            schema behind it.</li>
                        <li>WebSockets, background tasks that outlive the request, and
                            file uploads &mdash; <code>python-multipart</code> is not
                            loaded.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>One honest difference</h2>
                    <p>In a real server a <code>def</code> endpoint is handed to a thread
                    pool so it cannot block the event loop, while an
                    <code>async def</code> one runs on the loop itself. That distinction
                    is most of what "should this be async?" is about.</p>
                    <p>This runtime cannot start threads, so <code>def</code> endpoints
                    are run inline here. Everything you can observe &mdash; the response,
                    the status, the validation &mdash; is identical, and the difference
                    only shows up in a blocking call, which cannot happen here anyway. It
                    is worth knowing about before you reason about performance from what
                    you see on this page.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Reading a 422</h2>
                    <p>422 is FastAPI telling you the request never reached your function.
                    The body it returns is a Pydantic error list, and the useful field is
                    <code>loc</code> &mdash; the path to the thing it rejected.</p>
                    <p><code>["path", "book_id"]</code> means the URL, and
                    <code>["query", "verbose"]</code> means the query string. Anything
                    starting <code>["body", ...]</code> is inside the JSON you sent, with
                    the rest of the list naming the field &mdash; so
                    <code>["body", "price"]</code> is one level in. A 422 you did not
                    expect is nearly always an annotation promising something the caller
                    did not send.</p>
                </section>

                <section class="vz-lab-side">
                    <h2>Things worth trying</h2>
                    <ul>
                        <li>Add <code>response_model=Book</code> to a route, then return a
                            dict with an extra key and see it filtered out.</li>
                        <li>Write a dependency with <code>Depends</code> and use it in two
                            routes.</li>
                        <li>Print <code>app.openapi()</code> in full and find the
                            constraint you wrote with <code>Field(gt=0)</code>.</li>
                        <li>Change a parameter's annotation from <code>int</code> to
                            <code>str</code> and watch which requests start passing.</li>
                        <li>Add a second router with <code>APIRouter(prefix="/v2")</code>
                            and include it.</li>
                    </ul>
                </section>

                <section class="vz-lab-side">
                    <h2>The layer below</h2>
                    <p>Most of what FastAPI does with your annotations is Pydantic doing
                    it. The <a href="%(p)spydantic-lab/">Pydantic compiler</a> is the same
                    editor with just that library, and the
                    <a href="%(p)spython-lab/">Python compiler</a> is the language on its
                    own.</p>
                </section>
            </div>
        </div>

""" % {
    # render() runs one more %-format over the whole page, so a literal % in
    # the code being embedded has to survive it. `"<Response [%s]>"` in the
    # prelude is a real one, and it took the build down.
    "starter": STARTER.strip().replace("%", "%%"),
    "prelude": PRELUDE.strip().replace("%", "%%"),
    "wheels": WHEELS,
    "p": "%(p)s",
}


def main():
    # The prelude is a Python module living inside a Python string literal,
    # so a stray backslash in it survives one round of parsing and breaks the
    # next. That failure is invisible here and shows up as a SyntaxError in
    # every editor on every page that uses it, which is a long way from the
    # cause. Compiling it now turns that into a build failure.
    compile(PRELUDE, "<prelude>", "exec")

    rel = tool.write(KEY, tool.render(KEY, CSS, body(), wide=True, app=True))
    print("fastapi lab page          : %s" % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
