# -*- coding: utf-8 -*-
"""Content for the FastAPI track.

Every page runs against a real FastAPI app. There is no server - a browser
tab cannot listen on a port - so a `client` defined before the reader's code
calls the app through ASGI, which is the same interface uvicorn uses. Routing,
validation, status codes and schema generation therefore behave exactly as
they do in production, because they are the same code.

That client is the prelude from tools/build_fastapi_lab.py, imported rather
than copied. Getting it to cover the whole framework took some work: the
threadpool shims it installs are what make Depends, yield dependencies and
background tasks run at all in a runtime with no threads.

Two things it cannot do, and the pages that touch them say so: streaming
responses and middleware need a real event loop, and WebSockets need a real
connection.

Examples use VizLearn's own domain - tracks, modules, readers - so the data
has a shape worth arguing about.
"""

TOPICS = []
CHECKS = {}


def topic(slug, title, cat, lead, svg, steps, notes, article, check,
          wheels=None, prelude=None):
    """One module. `steps` is a list of (heading, blurb, code) triples."""
    TOPICS.append({
        "slug": slug, "title": title, "cat": cat, "lead": lead, "svg": svg,
        "steps": steps, "notes": notes, "article": article, "check": check,
        "wheels": wheels or [], "prelude": prelude or "",
    })
    CHECKS["fastapi/%s.html" % slug] = {"check": check}


A = "var(--accent-primary)"
M = "var(--text-muted)"
B = "var(--border-subtle)"
S = "var(--bg-surface)"


def _svg(body):
    return '<svg aria-hidden="true" viewBox="0 0 160 90" class="w-full h-full">%s</svg>' % body


def _box(x, y, w, h, fill="none", stroke=B, sw=2, rx=3):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
            'stroke="%s" stroke-width="%s"/>' % (x, y, w, h, rx, fill, stroke, sw))


def _txt(x, y, s, fill=M, size=9, anchor="middle", weight="normal"):
    return ('<text x="%s" y="%s" fill="%s" font-size="%s" font-family="monospace" '
            'text-anchor="%s" font-weight="%s">%s</text>'
            % (x, y, fill, size, anchor, weight, s))


def _arrow(x1, y1, x2, y2, stroke=M):
    return '<path d="M%s %s L%s %s" stroke="%s" stroke-width="2"/>' % (x1, y1, x2, y2, stroke)


# ---------------------------------------------------------------------------
# 1. What FastAPI is
# ---------------------------------------------------------------------------
topic(
    "what_is_fastapi",
    "What FastAPI Is",
    "Foundations",
    "A thin layer over two ideas - ASGI and Pydantic - and almost nothing that "
    "looks like magic is anything else.",
    _svg(_box(10, 20, 44, 24, S) + _txt(32, 36, "request", M, 8) +
         _arrow(56, 32, 70, 32) +
         _box(74, 20, 48, 24, S, A) + _txt(98, 36, "FastAPI", A, 8) +
         _arrow(98, 48, 98, 58) +
         _txt(80, 74, "validate  -  route  -  document", M, 8)),
    [
        ("Four lines is a working API",
         "A function, a decorator and a type annotation. Everything else on this "
         "page is an elaboration of these.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"track": "FastAPI", "modules": 30}

# There is no server here, so `client` calls the app directly.
r = TestClient(app).get("/")
print(r.status_code, r.json())'''),

        ("The annotation does the work",
         "The same argument, twice: once as a plain string, once annotated. Only "
         "one of them is checked and converted.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/untyped/{value}")
def untyped(value):
    return {"value": value, "type": type(value).__name__}

@app.get("/typed/{value}")
def typed(value: int):
    return {"value": value, "type": type(value).__name__}

c = TestClient(app)
print("untyped:", c.get("/untyped/42").json())
print("typed  :", c.get("/typed/42").json())
print()
r = c.get("/typed/abc")
print("typed, bad input:", r.status_code, r.json()["detail"][0]["msg"])'''),

        ("Underneath it is one async function",
         "An ASGI app takes a request as a dictionary and sends the response back "
         "as messages. uvicorn's whole job is translating sockets into that.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"hello": "world"}

# Calling the app the way a server would, by hand.
scope = {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
         "method": "GET", "scheme": "http", "path": "/hello",
         "raw_path": b"/hello", "query_string": b"", "root_path": "",
         "headers": [(b"host", b"testserver")],
         "client": ("test", 1), "server": ("testserver", 80)}

messages = []
async def receive():
    return {"type": "http.request", "body": b"", "more_body": False}
async def send(m):
    messages.append(m)

drive(app(scope, receive, send))

for m in messages:
    print(m["type"], "->", {k: v for k, v in m.items() if k != "type"})'''),

        ("The docs are generated, not written",
         "The annotations become a JSON Schema, which becomes an OpenAPI document, "
         "which becomes the page at <code>/docs</code>.",
         '''import json
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="VizLearn API", version="1.0.0")

class Module(BaseModel):
    title: str = Field(min_length=3, description="Shown as the page heading.")
    minutes: int = Field(default=10, gt=0, le=180)

@app.post("/modules/", status_code=201)
def create(module: Module):
    return module

spec = app.openapi()
print("title  :", spec["info"]["title"], spec["info"]["version"])
print("paths  :", list(spec["paths"]))
print()
for name, prop in spec["components"]["schemas"]["Module"]["properties"].items():
    print("%-8s %s" % (name, json.dumps(prop)))'''),

        ("Errors before your code runs",
         "A request that does not fit never reaches the handler. The 422 is "
         "produced by validation, not by anything you wrote.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
reached = []

class Module(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

@app.post("/modules/")
def create(module: Module):
    reached.append(module.title)          # only runs if validation passed
    return {"ok": True}

c = TestClient(app)
print("good:", c.post("/modules/", json={"title": "Vectors", "minutes": 8}).status_code)
print("bad :", c.post("/modules/", json={"title": "no", "minutes": -1}).status_code)
print()
print("handler ran for:", reached, "<- the bad request never got there")'''),

        ("Sync and async both work",
         "A <code>def</code> endpoint and an <code>async def</code> one are both "
         "ordinary here. Which to use is a real decision, and gets its own module.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/sync")
def sync_endpoint():
    return {"style": "def"}

@app.get("/async")
async def async_endpoint():
    return {"style": "async def"}

c = TestClient(app)
print("sync :", c.get("/sync").json())
print("async:", c.get("/async").json())
print()
print("Same response. The difference is where the function runs,")
print("which matters once it starts doing real work.")'''),
    ],
    [
        "FastAPI has no validation layer of its own. It hands request data to Pydantic and turns the resulting <code>ValidationError</code> into a 422.",
        "Underneath, an app is one async function taking <code>(scope, receive, send)</code>. That interface is ASGI, and uvicorn exists to translate sockets into it.",
        "Because the interface is a plain function call, an app can be exercised without a network &mdash; which is what the editors on this page do.",
        "The interactive docs are generated from <code>model_json_schema()</code> for every model you used. Writing a <code>description</code> is writing documentation.",
        "Validation happens <em>before</em> your handler. A 422 means the function never ran.",
        "Both <code>def</code> and <code>async def</code> endpoints are supported, and the choice has real consequences &mdash; covered in the runtime tier.",
    ],
    '''
title: What FastAPI Is, and What It Is Not
intro: A thin layer over two ideas you can learn separately - and almost nothing that looks like magic is anything else.

## Two libraries wearing one name

A great deal of what people call "FastAPI magic" is not FastAPI at all.

**Pydantic** does the validation. FastAPI has no validation code of its own: it reads your annotations, hands the request body to a model, and converts the resulting `ValidationError` into a 422 response. Every coercion rule, every error `type`, every constraint you can write is Pydantic's.

**Starlette** does the HTTP. Routing, requests, responses, middleware, background tasks and the ASGI plumbing are Starlette's, which FastAPI builds on rather than replaces.

What FastAPI itself contributes is the join: reading a function's signature to work out which parameters come from the path, the query string, the body, a header or a dependency &mdash; and generating an OpenAPI document from the same information.

That is a small amount of code doing something valuable, and knowing where the seams are makes both debugging and reading the source much easier. A 422 you disagree with is a Pydantic question. A route that does not match is a Starlette question. A parameter arriving from the wrong place is a FastAPI question.

## Underneath: one async function

An ASGI application is a callable:

```python
async def app(scope, receive, send):
    ...
```

`scope` is a dictionary describing the request. `receive` is an awaitable that returns incoming messages. `send` is an awaitable that takes outgoing ones. That is the entire interface, and a FastAPI app satisfies it.

uvicorn's job is to accept a TCP connection, parse HTTP, build that `scope`, call your app, and write the response messages back to the socket. It is a translator between sockets and function calls.

The third editor above does the translation by hand: it builds a scope, calls the app, and prints the messages that come back. Two of them &mdash; `http.response.start` with the status and headers, `http.response.body` with the content &mdash; and that is a complete HTTP response.

This matters practically. Because the interface is a plain function call, you can exercise an entire application without a network, which is what makes fast tests possible and what makes the editors on this page work at all.

## The annotation is the contract

```python
@app.get("/modules/{module_id}")
def read(module_id: int):
    ...
```

The path says there is a `module_id` in the URL. The annotation says it is an integer. From those two facts FastAPI extracts the value, asks Pydantic to convert it, rejects the request with a 422 if it cannot, and records in the OpenAPI document that this endpoint takes an integer path parameter.

Remove the annotation and you get a string, unvalidated and undocumented. The second editor above shows both side by side: `/untyped/42` gives you `"42"` and `/typed/42` gives you `42`.

That single difference is most of the value proposition. You were going to write the annotation anyway; the framework decided to act on it.

## Validation happens first

A request that does not fit never reaches your function.

This is worth stating plainly because it changes how handlers are written. There is no defensive checking at the top of the function, no `if not isinstance(...)`, no `try: int(...)`. By the time your code runs, every parameter is the type you declared and every constraint has passed.

The fifth editor above demonstrates it by recording which requests reached the handler: the invalid one is simply absent.

## What you get without asking

Because the annotations describe the data precisely, several things follow for free.

**Interactive documentation** at `/docs`, generated from the OpenAPI schema, with the descriptions and examples you wrote on your fields.

**A machine-readable contract** at `/openapi.json`, from which clients can be generated in a dozen languages.

**Editor support**, because your handler's parameters have real types.

None of that is a separate feature you enable. It is a consequence of the schema, which is a consequence of the annotations.

## What it is not

**It is not async-only.** A `def` endpoint is fully supported and is often the right choice. The framework runs it in a threadpool so it cannot block the event loop.

**It is not a full-stack framework.** There is no ORM, no admin, no template convention, no migrations. Django gives you all of that; FastAPI gives you an API layer and leaves the rest to you. That is a trade, not a ranking.

**It is not fast because of its own code.** The speed comes from Starlette's ASGI design and from Pydantic v2's Rust core. FastAPI's contribution is not getting in the way.

**It is not a replacement for understanding HTTP.** Status codes, methods, headers and caching are still yours to get right, and the framework will happily let you return 200 for a failure.

## A note on these pages

There is no server here, and there cannot be: a browser tab cannot listen on a port.

What runs instead is the app itself, called through ASGI by a `client` defined before your code. That is the same interface uvicorn uses, so routing, validation, status codes, dependencies and the generated schema all behave exactly as they do in production &mdash; because they are the same code paths, with the network removed.

Two things genuinely differ, and the modules that touch them say so. Streaming responses and middleware need a real event loop. And WebSockets need a real connection, which no amount of cleverness will conjure in a sandbox.

Everything else on this track is the real thing.

## How a request actually travels

Tracing one request end to end makes the layers concrete.

A client opens a TCP connection and sends bytes. **uvicorn** parses them into an HTTP request and builds a `scope` dictionary: method, path, query string, headers, client address.

It calls your app with `(scope, receive, send)`. **Starlette's router** walks its route table in registration order, comparing the path and method, and finds a match &mdash; extracting any path parameters as strings along the way.

**FastAPI's dependency resolution** then runs. It works out, from the handler's signature, where each parameter comes from: this one from the path, that one from the query string, this one is a body, that one is a dependency to call first. Anything needing conversion goes to **Pydantic**, and a failure here becomes a 422 without your function ever being called.

Your handler runs, with real Python objects as arguments.

The return value goes through the **response model** if you declared one, then is serialised to JSON, and Starlette sends `http.response.start` followed by `http.response.body`. uvicorn turns those back into bytes on the socket.

Every step in that chain is ordinary Python. Nothing is hidden, and each layer can be exercised on its own &mdash; which is why testing a FastAPI app needs no server.

## Why it is fast

Three reasons, none of which is FastAPI's own code.

**ASGI is asynchronous.** A WSGI server handles one request per worker thread while that request waits on a database. An ASGI server can have thousands of requests in flight, each parked at an `await`. For an API that spends most of its time waiting on I/O &mdash; which is most APIs &mdash; that is a large difference in how much hardware you need.

**Pydantic v2 validates in Rust.** Validation used to be a measurable fraction of request time in v1. In v2 it usually is not.

**Starlette is thin.** Its routing and request handling do very little per request.

FastAPI's contribution is not adding overhead on top. That is a real achievement and it is worth being clear that the framework is not itself doing anything clever with speed.

The caveat that matters: none of this helps if your handler blocks. An `async def` endpoint that makes a synchronous database call stops the entire event loop, and one slow query can stall every concurrent request in the process. That trap has a module of its own in the runtime tier, and it is the single most common way a fast framework is made slow.

## What to read when something goes wrong

Knowing the seams tells you where to look.

A **404 you did not expect** is routing &mdash; check registration order and trailing slashes.

A **422 you disagree with** is Pydantic &mdash; look at the model, not the endpoint.

A **500 mentioning serialisation** is usually the response model, or a type your model does not know.

A **parameter arriving as `None`** is FastAPI's signature analysis deciding it came from somewhere other than you assumed &mdash; commonly a body treated as a query parameter.

**Nothing happening at all** is uvicorn, or a route registered on a router that was never included.

That mapping saves more time than any amount of framework documentation, because it turns "FastAPI is broken" into a specific question about a specific library.


## Mistakes people make

**Blocking the event loop.** Writing `async def` and then making a synchronous database or HTTP call inside it. The whole process stalls, and the framework's headline benefit is gone. If a function does blocking work, declare it `def` and let FastAPI put it on a threadpool.

**Assuming FastAPI validates.** It does not; Pydantic does. When a 422 surprises you, the model is the thing to read, and every rule from the Pydantic track applies unchanged.

**Fighting the schema.** People sometimes work around the generated documentation instead of improving the annotations that produce it. A vague schema almost always means vague types &mdash; a `str` that should be a `Literal`, a missing constraint, an absent response model.

**Treating it as a full-stack framework.** There is no ORM, no admin, no migrations. That is a deliberate scope, and expecting Django's batteries leads to a lot of disappointed searching.

**Putting business logic in handlers.** A handler should translate between HTTP and your application. Logic inside one cannot be tested without building a request or reused from a background job.

**Ignoring the seams.** Knowing that routing is Starlette, validation is Pydantic and signature analysis is FastAPI turns most debugging from guesswork into a specific question about a specific library.

## Where to go next

The next module builds a first endpoint properly and looks at what the decorator actually does. After that come the three places data arrives from &mdash; the path, the query string and the body &mdash; which between them account for most of what an API takes in.

## Why the seams are worth knowing

Most frameworks ask you to learn *the framework*. FastAPI is unusual in that most of what you learn transfers.

Pydantic is used far beyond web APIs &mdash; configuration, LLM structured output, data pipelines, CLI arguments. Everything from the Pydantic track applies here unchanged, and everything you learn here about models applies back there.

ASGI is a standard, not a FastAPI invention. Starlette, Django's async stack, Litestar and Quart all speak it, and an ASGI middleware written for one works with the others.

So the framework-specific surface is genuinely small: the decorators, the way a signature is analysed, and `Depends`. Everything else is two libraries and a protocol you would benefit from knowing regardless.

That is the argument for learning the layers rather than the recipes. A tutorial teaches you what to type; knowing which library owns which behaviour tells you what to do when the typing does not work.

## In one paragraph

FastAPI reads the annotations you were going to write anyway, uses Pydantic to enforce them, uses Starlette to move the bytes, and generates an OpenAPI document from the same information. The layer it adds is thin and mostly consists of working out where each of your function's parameters should come from. Learn the two libraries underneath and the framework itself takes an afternoon.

## A closing thought

The most useful thing to carry out of this module is not a fact about FastAPI but a habit of asking which layer you are in.

Routing, validation, signature analysis, serialisation and transport are five different concerns owned by three different libraries. Nearly every confusing behaviour becomes obvious once you know which one is responsible, and nearly every search becomes productive once you search for that library instead of for the framework.
''',
    [
        {"q": "Which library does FastAPI use for validation?",
         "options": ["Its own", "Pydantic", "Starlette", "marshmallow"],
         "answer": 1,
         "why": "FastAPI has no validation code of its own. It hands data to Pydantic and converts the resulting ValidationError into a 422, which is why everything you know about Pydantic applies directly."},
        {"q": "What is an ASGI application?",
         "options": ["A web server", "An async callable taking (scope, receive, send)", "A Pydantic model", "A router"],
         "answer": 1,
         "why": "That is the entire interface. uvicorn translates sockets into those three arguments, which is also why an app can be called directly, with no network, for tests."},
        {"q": "A request fails validation. Does your handler run?",
         "options": ["Yes, with None values", "No - validation happens before it", "Only for GET", "It depends on the model"],
         "answer": 1,
         "why": "The 422 is produced before the function is called. That is why handlers need no defensive type checking at the top."},
        {"q": "Where does the interactive documentation come from?",
         "options": ["A separate file you write", "The JSON Schema generated from your annotations", "uvicorn", "A decorator argument"],
         "answer": 1,
         "why": "Your models generate schemas, FastAPI assembles them into an OpenAPI document, and the docs page renders it. Writing a field description is writing documentation."},
    ],
)


# ---------------------------------------------------------------------------
# 2. Your first endpoint
# ---------------------------------------------------------------------------
topic(
    "your_first_endpoint",
    "Your First Endpoint",
    "Foundations",
    "What the decorator does, what the return value becomes, and how a function "
    "turns into a route.",
    _svg(_box(16, 18, 128, 22, S, A) + _txt(80, 32, '@app.get("/modules")', A, 8) +
         _arrow(80, 44, 80, 54) +
         _box(16, 56, 128, 22, S) + _txt(80, 70, "def read_modules(): ...", M, 8)),
    [
        ("The decorator registers a route",
         "It does not wrap the function. It records the path, the method and the "
         "signature in the app's routing table.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/modules")
def read_modules():
    return [{"title": "Vectors"}, {"title": "Norms"}]

print("routes registered:")
for route in app.routes:
    methods = getattr(route, "methods", None)
    if methods:
        print("  %-8s %s" % (",".join(sorted(methods)), route.path))

print()
print("the function is untouched:", read_modules())'''),

        ("The return value becomes JSON",
         "Dicts, lists, models, primitives &mdash; all serialised for you. The "
         "default status is 200.",
         '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Module(BaseModel):
    title: str
    minutes: int

@app.get("/dict")
def a(): return {"kind": "dict"}

@app.get("/list")
def b(): return [1, 2, 3]

@app.get("/model")
def c(): return Module(title="Vectors", minutes=8)

@app.get("/scalar")
def d(): return "just a string"

client = TestClient(app)
for path in ["/dict", "/list", "/model", "/scalar"]:
    r = client.get(path)
    print("%-8s %s  %-14s %s" % (path, r.status_code,
                                 r.headers.get("content-type"), r.text))'''),

        ("Choosing the status code",
         "<code>status_code</code> on the decorator sets the default for that route. "
         "The <code>status</code> module names them so you do not have to remember "
         "numbers.",
         '''from fastapi import FastAPI, status

app = FastAPI()

@app.post("/modules", status_code=status.HTTP_201_CREATED)
def create():
    return {"created": True}

@app.delete("/modules/{i}", status_code=status.HTTP_204_NO_CONTENT)
def delete(i: int):
    return None                       # 204 means "nothing to say"

client = TestClient(app)
r1 = client.post("/modules")
r2 = client.delete("/modules/1")
print("create :", r1.status_code, r1.json())
print("delete :", r2.status_code, repr(r2.text), "<- 204 has no body")'''),

        ("Order matters when paths overlap",
         "Routes are matched in the order they were registered, so a fixed path must "
         "come before a variable one that would also match it.",
         '''from fastapi import FastAPI

wrong = FastAPI()

@wrong.get("/modules/{module_id}")
def by_id(module_id: str):
    return {"matched": "by_id", "value": module_id}

@wrong.get("/modules/latest")            # registered second - never reached
def latest_wrong():
    return {"matched": "latest"}

right = FastAPI()

@right.get("/modules/latest")            # fixed path first
def latest_right():
    return {"matched": "latest"}

@right.get("/modules/{module_id}")
def by_id2(module_id: str):
    return {"matched": "by_id", "value": module_id}

print("wrong order:", TestClient(wrong).get("/modules/latest").json())
print("right order:", TestClient(right).get("/modules/latest").json())
print("still works:", TestClient(right).get("/modules/7").json())'''),

        ("Describing the endpoint",
         "<code>summary</code>, <code>description</code> and <code>tags</code> shape "
         "the documentation. The docstring becomes the description if you do not "
         "supply one.",
         '''import json
from fastapi import FastAPI

app = FastAPI()

@app.get("/modules", summary="List modules", tags=["modules"])
def read_modules():
    """Return every published module, newest first.

    Unpublished drafts are excluded.
    """
    return []

spec = app.openapi()["paths"]["/modules"]["get"]
print("summary    :", spec["summary"])
print("tags       :", spec["tags"])
print("description:")
print(spec["description"])'''),

        ("A whole small API",
         "Everything so far in one app: two routes, a model, a status code and an "
         "in-memory store.",
         '''from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="VizLearn")
DB = {1: {"id": 1, "title": "Vectors", "minutes": 8}}

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(default=10, gt=0)

@app.get("/modules", tags=["modules"])
def list_modules():
    return list(DB.values())

@app.post("/modules", status_code=status.HTTP_201_CREATED, tags=["modules"])
def create_module(module: ModuleIn):
    new_id = max(DB) + 1
    DB[new_id] = {"id": new_id, **module.model_dump()}
    return DB[new_id]

client = TestClient(app)
print("before :", client.get("/modules").json())
r = client.post("/modules", json={"title": "Eigenvalues", "minutes": 14})
print("created:", r.status_code, r.json())
print("after  :", client.get("/modules").json())'''),
    ],
    [
        "The decorator registers a route; it does not wrap your function. Calling the function directly still works exactly as before.",
        "Whatever you return is serialised to JSON &mdash; dicts, lists, models and primitives all work. The default status is 200.",
        "<code>status_code=</code> on the decorator sets that route's default. The <code>status</code> module gives every code a readable name.",
        "Routes match in <strong>registration order</strong>, so <code>/modules/latest</code> must be declared before <code>/modules/{id}</code> or it will never be reached.",
        "<code>summary</code>, <code>tags</code> and the function's docstring all flow into the OpenAPI document and the docs page.",
        "A 204 response must have no body. Declare <code>status_code=204</code> and return <code>None</code> &mdash; returning a value with a 204 produces a malformed response.",
    ],
    '''
title: Your First Endpoint, and What the Decorator Really Does
intro: How a function becomes a route, what happens to the return value, and the ordering rule that catches everyone once.

## The decorator does not wrap anything

```python
@app.get("/modules")
def read_modules():
    return [{"title": "Vectors"}]
```

The instinct is that `@app.get` wraps the function in something. It does not. It **registers** it: the app records the path, the HTTP method and the function's signature in a routing table, and returns the function unchanged.

You can verify that, and the first editor above does &mdash; `read_modules()` called directly still returns the list. This is worth knowing because it means an endpoint is an ordinary function, testable on its own, with no framework machinery attached to it.

What the app records from the signature is more than the name. It notes which parameters correspond to placeholders in the path, which have defaults, and what each is annotated as. That analysis happens once, at import, which is why routing is cheap at request time.

## The return value

Whatever you return is converted to JSON: dictionaries, lists, Pydantic models, and primitives like strings and numbers. The default status is 200 and the content type is `application/json`.

Returning a model is the most useful case, because the model decides the shape. Returning a bare string produces `"just a string"` &mdash; valid JSON, with the quotes &mdash; which occasionally surprises people expecting plain text. If you want plain text, say so with `PlainTextResponse`.

For anything you care about, declare a `response_model` rather than relying on what the handler happens to return. That gets a module of its own shortly, and it is the difference between an endpoint that documents its output and one that does not.

## Status codes

The decorator takes `status_code`:

```python
@app.post("/modules", status_code=status.HTTP_201_CREATED)
```

That sets the *default* for the route. A handler can still override it per response when it needs to.

The `status` module is worth using over bare integers. `status.HTTP_201_CREATED` says what it means, and your editor will autocomplete it, which matters more than it sounds for the codes people reach for less often.

One rule that bites: **a 204 must have no body.** Returning a dict with `status_code=204` produces a malformed response. Declare `status_code=204` and return `None`.

Worth getting right, briefly: 200 for a successful read, 201 for something created, 204 for a successful action with nothing to say, 202 for accepted-but-not-done. Returning 200 for everything is common and throws away information every HTTP client already knows how to act on.

## Route order

This is the mistake almost everyone makes once.

Routes are matched **in registration order**, first match wins. So:

```python
@app.get("/modules/{module_id}")   # registered first
@app.get("/modules/latest")        # never reached
```

A request for `/modules/latest` matches the first route, with `module_id="latest"`. If `module_id` is annotated `int`, the caller gets a confusing 422 about `latest` not being an integer. If it is annotated `str`, they get a successful lookup for a module that does not exist.

The fix is to declare fixed paths before variable ones. The fourth editor above shows both orders side by side.

The `int` annotation does soften this: a genuinely numeric path still routes correctly, and `/modules/latest` fails loudly rather than silently. That is one more small argument for annotating path parameters precisely.

## Describing what you built

Three things shape the documentation, and all are free.

`summary` is the short label in the docs list. Without one, FastAPI generates a title from the function name, which is usually worse than a sentence you write.

`tags` group endpoints into sections. On an API of any size this is the difference between a navigable document and a flat list of forty routes.

The **docstring** becomes the description. That is a nice property: documentation written where a Python developer would naturally write it also appears in the API docs, and Markdown is rendered.

`response_description` and `deprecated=True` are there too, the latter being the polite way to retire an endpoint &mdash; it still works and the docs show it as deprecated.

## Path design, briefly

FastAPI does not enforce a convention, and one is worth having.

Use plural nouns for collections: `/modules`, not `/module` or `/getModules`. The method already says what you are doing, so putting a verb in the path duplicates it.

Nest only where there is genuine ownership: `/modules/{id}/lessons` is reasonable; `/tracks/{t}/modules/{m}/lessons/{l}/comments/{c}` is a URL nobody will type correctly.

Keep the identifier in the path and the filtering in the query string. `/modules/7` identifies a thing; `/modules?track=maths` narrows a set. Which is which is the subject of the next two modules.

## What running these means

The editors call the app through ASGI rather than over a network, so everything you can observe &mdash; status codes, headers, JSON bodies, routing decisions, validation &mdash; is the real behaviour.

`client.get("/modules")` here does what the same line does in a real test file using `fastapi.testclient.TestClient`. The code you are reading is the code you would write.

## The other methods

`@app.get` has siblings for every HTTP method: `post`, `put`, `patch`, `delete`, `head`, `options`, `trace`.

They are not interchangeable, and choosing correctly gives you behaviour from the wider web for free.

**GET** reads and must not change anything. It is cacheable, retryable and safe to repeat, and browsers, proxies and CDNs all assume that. A GET that mutates state will eventually be replayed by something and cause a problem you did not write.

**POST** creates, or performs an action that is not idempotent. Sending it twice does it twice.

**PUT** replaces a resource at a known URL. Sending it twice leaves the same result, which makes it safe for a client to retry after a timeout.

**PATCH** updates part of one.

**DELETE** removes. Also idempotent: deleting twice leaves the thing deleted.

That idempotency property is the practical payoff. A client whose connection drops mid-request can safely retry a PUT or DELETE and cannot safely retry a POST, and every HTTP library in the world already knows this.

## Trailing slashes

`/modules` and `/modules/` are different paths, and FastAPI redirects between them with a 307 by default.

That is usually invisible and occasionally maddening: a 307 preserves the method and body, but some clients drop the body on redirect, and a POST that mysteriously arrives empty is often this. Being consistent in your own routes &mdash; pick no trailing slash and stay with it &mdash; avoids the whole category.

## Returning a Response directly

Sometimes you need control over the exact response: a specific content type, a header, a status the route's default does not cover.

Returning a `Response` object bypasses serialisation and the response model entirely. `JSONResponse`, `PlainTextResponse`, `HTMLResponse` and `RedirectResponse` are all available.

The trade is that you have opted out of the machinery. Nothing validates what you sent and nothing documents it, so the schema no longer describes the endpoint. Do it for the genuine exceptions &mdash; a redirect, a file, a bespoke content type &mdash; and let the normal path handle everything else.

## Where handlers should stop

A recurring question with a stable answer: how much logic belongs in the handler?

As little as possible. A handler's job is to translate between HTTP and your application &mdash; take validated input, call something that does the work, turn the result into a response. Business logic inside a handler cannot be tested without constructing a request, cannot be reused by a background job or a CLI, and tends to accumulate.

The shape that stays healthy is a thin handler calling a plain function:

```python
@app.post("/modules", status_code=201)
def create(module: ModuleCreate) -> ModuleOut:
    return service.create_module(module)
```

Everything HTTP-specific is in the decorator and the signature. Everything else is a function you could call from anywhere.


## Mistakes people make

**Declaring a variable route before a fixed one.** `/modules/{id}` before `/modules/latest` makes the second unreachable. Fixed segments first, always.

**Returning a body with a 204.** It produces a malformed response. Declare the status and return `None`.

**Using 200 for everything.** A creation is a 201, a successful delete is a 204, an accepted-but-unfinished job is a 202. Clients already know how to act on these, and returning 200 throws that away.

**Mutating state in a GET.** Browsers prefetch, proxies cache, and monitoring replays. A GET that changes something will eventually be called when nobody asked.

**Forgetting the response model.** Without one the handler's return value is sent verbatim, including any field a future migration adds to the underlying row.

**Inconsistent trailing slashes.** `/modules` and `/modules/` differ, and the 307 between them loses the body in some clients. Pick one convention and hold it.

## Next

Three modules on where data comes from: the path, the query string and the body. Between them they cover almost everything an API accepts, and each has rules worth knowing precisely.

## A shape worth copying

By the end of a first pass, a healthy endpoint looks like this:

```python
@app.post("/modules", response_model=ModuleOut,
          status_code=status.HTTP_201_CREATED, tags=["modules"])
def create_module(module: ModuleCreate) -> ModuleOut:
    """Create a module and return it with its assigned id."""
    return service.create_module(module)
```

Every line is doing something. The path names a collection. The response model states what leaves. The status code says what happened. The tag groups it in the docs. The input model states what may be sent. The docstring becomes the description. And the body is one call into code that knows nothing about HTTP.

Nothing there is clever, and that is the point &mdash; the interesting parts are in the models and the service, where they can be tested without constructing a request.

## Where routes live as an app grows

One file works until it does not. The usual progression is a single `main.py`, then a hundred routes in it, then a rewrite nobody enjoys.

`APIRouter` is the answer and it gets a full module later, but it is worth knowing the shape now so the first file is written in a way that can grow. A router is a mini-app you register routes on and then include into the main one with a prefix and tags:

```python
router = APIRouter(prefix="/modules", tags=["modules"])

@router.get("")
def list_modules(): ...

app.include_router(router)
```

The practical advice for a new project: create the router file on day one, even with two routes in it. Moving three endpoints later is trivial; moving eighty is a weekend.

## Reloading while you work

`uvicorn main:app --reload` restarts the process whenever a file changes, which is what you want in development and never in production &mdash; the reloader spawns an extra process and watches the filesystem.

Two things people trip on. Module-level state resets on every reload, so anything held in a global disappears when you save. And an import error leaves the previous version running, so a change that "does nothing" is sometimes a syntax error scrolled off the top of the terminal.

## The one-line summary

The decorator registers a function as a route without changing it. The return value becomes JSON. `status_code` sets the route's default and a 204 must carry nothing. Fixed paths go before variable ones. And the docstring you were going to write anyway becomes the description in your API documentation.

## A closing thought

The endpoints in this module are four lines each, and that is representative rather than simplified. A well-factored FastAPI handler usually is short, because everything it would otherwise contain has moved somewhere better: the validation into a model, the shape of the response into another model, and the work into a function that knows nothing about HTTP.

If a handler is growing, that is usually the signal &mdash; not that the endpoint is complicated, but that something in it belongs elsewhere.

## What to check before shipping one

A short list, all of which this module has covered.

Does it declare a response model? Is the status code right for what it does? Does the method match its effect &mdash; nothing mutating behind a GET? Is a fixed path registered before any variable one that would shadow it? Does it have a summary and a tag, so the documentation is navigable? And is the handler thin enough that the logic could be tested without a request?

Six questions, most answerable in seconds, and between them they catch nearly everything this module described.
''',
    [
        {"q": "What does `@app.get(\"/x\")` do to the function?",
         "options": ["Wraps it in a handler", "Registers it as a route and returns it unchanged", "Makes it async", "Adds validation code to it"],
         "answer": 1,
         "why": "The decorator records the path, method and signature in the routing table. The function itself is untouched and still callable directly."},
        {"q": "Why is `/modules/latest` unreachable when declared after `/modules/{module_id}`?",
         "options": ["A bug", "Routes match in registration order, first match wins", "Fixed paths are lower priority", "It needs a tag"],
         "answer": 1,
         "why": "The variable route matches first, with module_id=\"latest\". Declare fixed paths before variable ones - and annotating the parameter `int` makes the failure loud rather than silent."},
        {"q": "What must a 204 response contain?",
         "options": ["An empty dict", "Nothing - no body at all", "A message", "The created object"],
         "answer": 1,
         "why": "204 means success with nothing to say. Returning a value with status_code=204 produces a malformed response; return an explicit `Response(status_code=204)`."},
        {"q": "Where does an endpoint's description in the docs come from?",
         "options": ["A separate file", "The function's docstring, unless you pass `description`", "The route path", "The response model"],
         "answer": 1,
         "why": "The docstring becomes the description and Markdown is rendered - so documentation written where a Python developer naturally writes it also reaches the API docs."},
    ],
)


# ---------------------------------------------------------------------------
# 3. Path parameters
# ---------------------------------------------------------------------------
topic(
    "path_parameters",
    "Path Parameters",
    "Foundations",
    "Values taken from the URL itself - converted, validated, and documented from "
    "one annotation.",
    _svg(_txt(80, 26, "/modules/{module_id}", M, 9) +
         _arrow(80, 36, 80, 48) +
         _box(30, 50, 100, 24, S, A) + _txt(80, 66, "module_id: int", A, 8)),
    [
        ("A placeholder becomes an argument",
         "Whatever is in braces in the path is matched to a parameter of the same "
         "name. The annotation decides what it becomes.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/modules/{module_id}")
def read(module_id: int):
    return {"module_id": module_id, "type": type(module_id).__name__}

client = TestClient(app)
print(client.get("/modules/7").json())
print(client.get("/modules/0042").json(), "<- leading zeros gone; it is an int")

r = client.get("/modules/seven")
print()
print("not a number:", r.status_code, r.json()["detail"][0]["msg"])'''),

        ("The error names the path",
         "<code>loc</code> starts with <code>path</code>, so a caller knows the "
         "problem is in the URL rather than in what they sent.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/modules/{module_id}/lessons/{lesson_id}")
def read(module_id: int, lesson_id: int):
    return {"module": module_id, "lesson": lesson_id}

client = TestClient(app)
print("valid  :", client.get("/modules/7/lessons/2").json())

r = client.get("/modules/7/lessons/two")
for err in r.json()["detail"]:
    print("loc    :", err["loc"])
    print("type   :", err["type"])
    print("msg    :", err["msg"])'''),

        ("Constraining the value",
         "<code>Path()</code> carries the same constraints as Pydantic's "
         "<code>Field</code>, and they reach the documentation.",
         '''import json
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/modules/{module_id}")
def read(module_id: int = Path(ge=1, le=9999,
                               description="Identifier of the module.")):
    return {"module_id": module_id}

client = TestClient(app)
print("ok :", client.get("/modules/7").json())
r = client.get("/modules/0")
print("0  :", r.status_code, r.json()["detail"][0]["msg"])
print()
spec = app.openapi()["paths"]["/modules/{module_id}"]["get"]["parameters"][0]
print("documented as:", json.dumps(spec))'''),

        ("A closed set of values",
         "An <code>Enum</code> in the path gives you validation, a readable error and "
         "a set of choices in the docs.",
         '''from enum import Enum
from fastapi import FastAPI

class Track(str, Enum):
    MATHS = "maths"
    PYTHON = "python"
    DSA = "dsa"

app = FastAPI()

@app.get("/tracks/{track}")
def read(track: Track):
    return {"track": track.value, "label": track.name.title()}

client = TestClient(app)
print("valid  :", client.get("/tracks/maths").json())

r = client.get("/tracks/astrology")
print("invalid:", r.status_code, r.json()["detail"][0]["msg"])
print()
print("in the schema:", app.openapi()["components"]["schemas"]["Track"])'''),

        ("Paths that contain slashes",
         "A normal parameter stops at the next slash. The <code>:path</code> "
         "converter lets one swallow the rest.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/files/{name}")
def one_segment(name: str):
    return {"kind": "single", "name": name}

@app.get("/assets/{full_path:path}")
def whole_path(full_path: str):
    return {"kind": "path", "full_path": full_path}

client = TestClient(app)
print(client.get("/files/logo.png").json())
print(client.get("/assets/og/maths/vectors.png").json())
print()
r = client.get("/files/og/maths.png")
print("single segment cannot match a slash:", r.status_code)'''),

        ("Order still decides",
         "The rule from the last module, in its most common form: a fixed segment "
         "must be registered before a parameter that would also match it.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/modules/latest")
def latest():
    return {"route": "latest"}

@app.get("/modules/{module_id}")
def by_id(module_id: int):
    return {"route": "by_id", "id": module_id}

client = TestClient(app)
print("/modules/latest ->", client.get("/modules/latest").json())
print("/modules/7      ->", client.get("/modules/7").json())
print()
r = client.get("/modules/oldest")
print("/modules/oldest ->", r.status_code,
      "- no fixed route, and 'oldest' is not an int")'''),
    ],
    [
        "A name in braces in the path becomes a parameter of the same name. The annotation decides the type it arrives as.",
        "Path parameters are always required &mdash; they are part of the URL, so there is no way to omit one.",
        "Errors carry <code>loc</code> beginning with <code>path</code>, which tells the caller the problem is in the URL rather than the body.",
        "<code>Path()</code> takes the same constraints as Pydantic's <code>Field</code> &mdash; <code>ge</code>, <code>le</code>, <code>min_length</code>, <code>pattern</code> &mdash; and they appear in the schema.",
        "An <code>Enum</code> gives a closed set: a clear error listing the options, and a documented enumeration a client can render.",
        "<code>{name:path}</code> matches across slashes. A plain parameter stops at the next one.",
    ],
    '''
title: Path Parameters: Values From the URL
intro: One annotation gives you extraction, conversion, validation and documentation.

## The mechanism

A name in braces in the route path becomes an argument to your function:

```python
@app.get("/modules/{module_id}")
def read(module_id: int):
    ...
```

Three things happen from those two lines. The router matches the URL and pulls out the segment. Pydantic converts it according to the annotation. And the OpenAPI document records that this endpoint takes an integer path parameter.

The name has to match. `{module_id}` in the path and `module_id` in the signature are connected by name, not position, and a mismatch is an error at import rather than at request time &mdash; which is the right moment to find out.

## They are always required

There is no such thing as an optional path parameter, and the reason is structural: the parameter is part of the URL. A request that omits it is a request to a different URL, which either matches another route or does not match at all.

So a default on a path parameter does nothing useful. If you want "with an id, or without", that is two routes: `/modules` and `/modules/{module_id}`.

## Everything from the coercion rules applies

The segment arrives as text &mdash; a URL has nothing else &mdash; and the annotation says what it should become. All the Pydantic rules hold: `"7"` becomes `7`, `"0042"` becomes `42`, and `"seven"` raises.

`UUID` is worth annotating properly rather than leaving as `str`. A malformed identifier is then rejected at the door with a clear message, instead of reaching a database query as an arbitrary string. The same applies to `date`.

## Reading the error

A failure produces a 422 whose `loc` is `("path", "module_id")`.

That first element matters. A client receiving a 422 needs to know whether the problem is in the URL, the query string, a header or the body, and `loc[0]` says which. Code that only looks at `loc[-1]` throws that away.

## Constraints with Path()

`Path()` carries the same arguments as Pydantic's `Field`:

```python
module_id: int = Path(ge=1, le=9999, description="Identifier of the module.")
```

`ge=1` is worth more than it looks. Without it, `/modules/-5` is a valid request that reaches your handler, and something downstream deals with a negative identifier. With it, the router rejects it and the documented minimum appears in the schema.

The same argument from the Pydantic track applies here: a constraint reaches the documentation and a validator does not. `Path(ge=1)` tells every consumer the floor; an `if module_id < 1` in the handler tells nobody.

## Enums for a closed set

When a path segment can only be one of a few values, an `Enum` is the right annotation:

```python
class Track(str, Enum):
    MATHS = "maths"
    PYTHON = "python"
```

Three benefits. The error lists the permitted values instead of saying something vague. The schema contains an enumeration, so the docs render a dropdown and a generated client gets a real type. And inside your handler the value is an enum member, so comparisons are checked by your editor rather than being string equality you can typo.

Inherit from `str` as well as `Enum`, for the reasons the Pydantic track set out: members then compare equal to their strings and serialise as plain text.

## Paths inside paths

A parameter matches one segment. `/files/{name}` will not match `/files/og/maths.png`, because the slash ends the match.

When you genuinely want the rest of the URL &mdash; a file path, a nested key, a proxied route &mdash; the `:path` converter does it:

```python
@app.get("/assets/{full_path:path}")
def serve(full_path: str):
    ...
```

One warning that matters. A `:path` parameter can contain `..`, and using it to build a filesystem path without checking is a directory-traversal vulnerability. Resolve the path and confirm it is inside the directory you meant before opening anything. Validation says the value is a string; it says nothing about whether it is safe.

## Ordering, again

The rule from the previous module is felt most sharply here, because path parameters are where overlaps arise:

```python
@app.get("/modules/latest")        # must come first
@app.get("/modules/{module_id}")
```

Registered the other way round, `/modules/latest` matches the variable route and either 422s confusingly or, if the parameter is a `str`, succeeds with a lookup for a module called "latest".

Annotating the parameter `int` limits the damage: a non-numeric segment then fails loudly rather than quietly. It is one more reason to be precise.

## Designing them

Path parameters identify a **thing**. Query parameters describe a **view** of a collection. That distinction resolves most design arguments about where a value belongs.

`/modules/7` identifies module seven. `/modules?track=maths` narrows a set. `/modules/7?verbose=true` identifies a thing and adjusts how it is presented. Putting `track` in the path would imply that a module belongs to exactly one track and can only be addressed through it, which may not be true.

Nest only for genuine ownership, and keep it shallow. `/modules/{id}/lessons` is reasonable. Four levels of nesting produces URLs nobody types correctly and routes nobody can maintain.

## Types worth annotating

Beyond `int` and `str`, several standard types earn their place in a path.

**`UUID`** rejects a malformed identifier at the router rather than passing an arbitrary string to a database query. That is a genuine safety improvement when the id comes from a URL somebody can edit.

**`date`** accepts `2026-08-26` and gives you a real `date`, so `/reports/{day}` needs no parsing in the handler.

**`Enum`** for a closed set, as above.

**`float`** exists and is usually wrong in a path. Identifiers are not floating point, and `/items/1.0` matching `/items/1` is rarely what anyone wants.

The general rule is the same one from the Pydantic track: annotate as narrowly as the domain allows. Each narrowing removes a class of bad input at the door and documents itself in the schema.

## Multiple parameters and their order

A route can have several placeholders, and the order in the *function signature* does not matter &mdash; matching is by name.

```python
@app.get("/tracks/{track}/modules/{module_id}")
def read(module_id: int, track: str):     # order differs, works fine
```

That is worth knowing because it means you can order a signature for readability rather than to mirror the URL. Path parameters first, then query, then body, then dependencies is a common convention and none of it is required.

## What a 404 means here

A path that matches no route at all gives a 404 from the router, before any of your code runs. That is a different thing from a 404 you raise because a lookup found nothing, even though the status is the same.

The distinction shows up in the response body: the router's 404 is `{"detail": "Not Found"}`, and yours is whatever you passed to `HTTPException`. If you are debugging and see the generic one, the request never matched a route &mdash; check the path, the method and the trailing slash before looking at your handler.

## Encoding

Path segments are URL-encoded, and FastAPI decodes them before you see them. A module titled `Vectors & Norms` reaches you as `Vectors & Norms`, not `Vectors%20%26%20Norms`.

That mostly just works. The case to be careful with is a value that can itself contain a slash &mdash; an encoded `%2F` is decoded to `/` and can change how the path is interpreted. For anything that might contain one, either use a `:path` parameter deliberately or move the value to the query string, where the ambiguity does not arise.

## Summary

A braces name in the path becomes an argument, converted by its annotation. Path parameters are always required, because they are part of the URL.

`Path()` adds constraints and metadata that reach the schema. Enums give closed sets a real type and a good error. `:path` matches across slashes, and needs care if it reaches a filesystem.

And the ordering rule, once more: fixed segments before variable ones.


## Mistakes people make

**Leaving an identifier as `str`.** A `UUID` or `int` annotation rejects malformed input at the router instead of passing an arbitrary string to a query.

**No lower bound.** `/modules/{id}` with a plain `int` accepts `-5`, and something downstream deals with a negative identifier. `Path(ge=1)` costs one argument.

**Building a filesystem path from a `:path` parameter.** It can contain `..`. Resolve it and confirm it is inside the directory you intended before opening anything &mdash; validation says it is a string, not that it is safe.

**Expecting a plain parameter to match a slash.** It stops at the next segment; `:path` is the opt-in.

**Confusing the two kinds of 404.** The router's generic `{"detail": "Not Found"}` means no route matched at all. Yours means the route matched and the lookup found nothing.

**Putting a filter in the path.** `/modules/maths/vectors` implies a module can only be addressed through one track. If it is narrowing a set rather than identifying a thing, it belongs in the query string.

## Next

Query parameters, which are the opposite in almost every respect: optional by default, unordered, and the place most of an API's flexibility lives.

## What good path design buys

A well-designed path is a promise about identity: this URL names this thing, and will keep naming it.

That is what makes bookmarking, caching, linking and logging work. A URL that means something different depending on a query parameter, or that encodes a filter as a segment, breaks all four quietly.

The test is simple. Read the path aloud without the query string. If it names one identifiable thing, or one named collection, it is right. If you have to explain what it returns, something belonging in the query string has ended up in the path.

## Versioning and stability

Paths are the most public part of an API, and the hardest to change once anyone depends on them.

The common approach is a version prefix &mdash; `/v1/modules` &mdash; which is honest and coarse: it lets you make breaking changes by publishing a new version, at the cost of maintaining two.

The alternative is to avoid breaking changes: add fields rather than removing them, add parameters rather than changing defaults, and deprecate before deleting. Most APIs need far fewer versions than they expect if they hold that line.

What is worth deciding early is where the version lives, because retrofitting a prefix touches every route, every client and every piece of documentation. A router with `prefix="/v1"` costs nothing on day one.

## Identifiers people can see

A last design note. Sequential integer ids in a public URL leak information: how many modules exist, roughly when one was created, and whether the id next to yours exists.

For anything where that matters, a UUID or a short opaque id is worth the small inconvenience &mdash; and annotating it `UUID` gives you validation for free. For an internal API it rarely matters, and integers are easier to read in logs.

## The one-line summary

A path parameter identifies a thing, is always required, arrives as text and becomes whatever you annotate it as. Annotate it narrowly, constrain it with `Path()`, declare fixed routes before variable ones, and treat a `:path` value as untrusted the moment it touches a filesystem.

## A closing thought

The path is the part of an API that outlives everything else. Response shapes change, parameters come and go, but a URL somebody bookmarked, logged, cached or hard-coded is forever.

That asymmetry is worth remembering when designing one. A few minutes deciding whether a value identifies a resource or merely filters a collection is cheap now and unrecoverable later.

## Two small conventions

**Singular or plural.** Collections are plural &mdash; `/modules`, `/tracks` &mdash; and an item is that collection plus an identifier. Mixing `/module/7` and `/modules` in one API is the kind of inconsistency that costs a caller a request every time they guess wrong.

**Lower case, hyphens if needed.** Paths are case-sensitive in the standard and inconsistently handled in practice. Sticking to lower case removes a class of bug that only appears on somebody else's server.

Neither is enforced and both are worth deciding once, because the alternative is deciding per endpoint and getting it wrong somewhere.

## Where this fits

Path parameters are the smallest of the three input sources and the one with the least room for opinion: a segment of the URL, required, converted by annotation.

That simplicity is why they are worth getting exactly right. There is nothing to configure and nothing to trade off &mdash; only the choice of how narrowly to annotate, and whether the value belongs in the path at all. Both decisions are made once per endpoint and last as long as the URL does.
''',
    [
        {"q": "Can a path parameter be optional?",
         "options": ["Yes, with a default", "No - it is part of the URL, so omitting it is a different URL", "Only with Path()", "Only if it is a string"],
         "answer": 1,
         "why": "A request without the segment is a request to a different path. If you want both shapes, declare two routes."},
        {"q": "What is `loc` for a failed path parameter?",
         "options": ["('body', 'module_id')", "('path', 'module_id')", "('module_id',)", "()"],
         "answer": 1,
         "why": "The first element names which part of the request failed - path, query, header or body - which is what lets a client point the user at the right thing."},
        {"q": "Why annotate a path parameter as `Enum` rather than `str`?",
         "options": ["It is faster", "Clear error listing the options, an enumeration in the schema, and checked comparisons in your handler", "It is required", "To allow slashes"],
         "answer": 1,
         "why": "A `str` accepts anything and documents nothing. The enum gives the caller the permitted values and gives a generated client a real type."},
        {"q": "What does `{full_path:path}` do that a plain parameter does not?",
         "options": ["Makes it optional", "Matches across slashes", "Validates it as a file", "Makes it required"],
         "answer": 1,
         "why": "A plain parameter stops at the next slash. Note that a `:path` value can contain `..`, so building a filesystem path from one without checking is a traversal vulnerability."},
    ],
)


# ---------------------------------------------------------------------------
# 4. Query parameters
# ---------------------------------------------------------------------------
topic(
    "query_parameters",
    "Query Parameters",
    "Foundations",
    "Everything after the question mark: optional by default, converted by "
    "annotation, and where most of an API's flexibility lives.",
    _svg(_txt(80, 24, "?track=maths&amp;limit=10", M, 8) +
         _arrow(80, 34, 80, 46) +
         _box(14, 48, 62, 24, S) + _txt(45, 64, "track: str", M, 8) +
         _box(84, 48, 62, 24, S) + _txt(115, 64, "limit: int", M, 8)),
    [
        ("Anything not in the path is a query parameter",
         "A function argument that is not a path placeholder and is not a model is "
         "read from the query string.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/modules")
def list_modules(track: str = "maths", limit: int = 10, verbose: bool = False):
    return {"track": track, "limit": limit, "verbose": verbose,
            "types": [type(v).__name__ for v in (track, limit, verbose)]}

client = TestClient(app)
print("defaults :", client.get("/modules").json())
print("supplied :", client.get("/modules?track=python&limit=3&verbose=yes").json())'''),

        ("Required, optional and nullable",
         "A default makes it optional. No default makes it required. "
         "<code>Optional</code> only says it may be null.",
         '''from typing import Optional
from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
def search(q: str,                       # required
           track: Optional[str] = None,  # optional, may be absent
           limit: int = 10):             # optional, has a default
    return {"q": q, "track": track, "limit": limit}

client = TestClient(app)
print("minimum :", client.get("/search?q=vectors").json())
print("full    :", client.get("/search?q=vectors&track=maths&limit=3").json())

r = client.get("/search")
print()
print("missing q:", r.status_code, r.json()["detail"][0]["loc"],
      r.json()["detail"][0]["type"])'''),

        ("Constraints and metadata",
         "<code>Query()</code> carries the same arguments as <code>Field</code>, and "
         "they land in the documentation.",
         '''import json
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/modules")
def list_modules(
    q: str = Query(default="", max_length=50, description="Free-text search."),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return {"q": q, "limit": limit, "offset": offset}

client = TestClient(app)
print("ok  :", client.get("/modules?limit=25").json())
r = client.get("/modules?limit=500")
print("over:", r.status_code, r.json()["detail"][0]["msg"])
print()
for p in app.openapi()["paths"]["/modules"]["get"]["parameters"]:
    print("%-7s %s" % (p["name"], json.dumps(p["schema"])))'''),

        ("Repeated parameters become a list",
         "<code>?tag=a&amp;tag=b</code> is how a query string expresses more than one "
         "value. Annotate it as a list and you get one.",
         '''from typing import List
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/modules")
def list_modules(tag: List[str] = Query(default=[]),
                 id: List[int] = Query(default=[])):
    return {"tag": tag, "id": id}

client = TestClient(app)
print("none    :", client.get("/modules").json())
print("one     :", client.get("/modules?tag=maths").json())
print("several :", client.get("/modules?tag=maths&tag=vectors&id=1&id=2").json())
print()
print("note the ids are ints, converted item by item")'''),

        ("Booleans, and what counts as true",
         "Query strings are text, so a flag arrives as a word. Pydantic reads the "
         "meaning rather than the emptiness.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/flag")
def flag(on: bool = False):
    return {"on": on}

client = TestClient(app)
for value in ["true", "True", "yes", "on", "1", "false", "no", "off", "0"]:
    print("%-6s -> %s" % (value, client.get("/flag?on=" + value).json()["on"]))

r = client.get("/flag?on=maybe")
print()
print("maybe  ->", r.status_code, r.json()["detail"][0]["type"])
print()
print('In plain Python bool("false") is', bool("false"), "- which is why this matters.")'''),

        ("A realistic listing endpoint",
         "Search, filter, sort and paginate: the shape almost every collection "
         "endpoint ends up with.",
         '''from typing import List, Literal, Optional
from fastapi import FastAPI, Query

app = FastAPI()
DB = [
    {"id": 1, "title": "Vectors", "track": "maths", "minutes": 8},
    {"id": 2, "title": "Norms", "track": "maths", "minutes": 6},
    {"id": 3, "title": "Loops", "track": "python", "minutes": 12},
]

@app.get("/modules")
def list_modules(
    q: Optional[str] = Query(default=None, max_length=50),
    track: List[str] = Query(default=[]),
    sort: Literal["title", "minutes"] = "title",
    limit: int = Query(default=10, ge=1, le=100),
):
    rows = DB
    if q:
        rows = [r for r in rows if q.lower() in r["title"].lower()]
    if track:
        rows = [r for r in rows if r["track"] in track]
    rows = sorted(rows, key=lambda r: r[sort])[:limit]
    return {"count": len(rows), "items": rows}

client = TestClient(app)
print(client.get("/modules").json())
print(client.get("/modules?track=maths&sort=minutes").json())
print(client.get("/modules?q=loop").json())
print()
print("bad sort:", client.get("/modules?sort=colour").status_code)'''),
    ],
    [
        "Any function argument that is not a path placeholder, a body model or a dependency is read from the query string.",
        "A default makes a query parameter optional; no default makes it required. <code>Optional[str]</code> alone only says it may be null.",
        "<code>Query()</code> takes the same constraints and metadata as <code>Field</code>, and they appear in the schema as documented limits.",
        "A repeated key &mdash; <code>?tag=a&amp;tag=b</code> &mdash; becomes a list when the parameter is annotated as one. Items are converted individually.",
        "Everything arrives as text, so booleans are read as words: <code>true/yes/on/1</code> and <code>false/no/off/0</code>. Anything else is a 422.",
        "<code>Literal</code> is better than <code>str</code> for a sort key or a mode: a clear error, and a set of choices in the docs.",
    ],
    '''
title: Query Parameters: Everything After the Question Mark
intro: Optional by default, converted by annotation, and where most of an API's flexibility lives.

## How FastAPI decides

Look at a handler's signature and FastAPI classifies each parameter:

If the name appears in the route path, it is a **path parameter**.

If it is a Pydantic model, it is the **request body**.

If it is a dependency, a `Header`, a `Cookie`, or one of the other explicit markers, it is that.

Otherwise it is a **query parameter**.

That last rule is the default, and it is why a handler with a plain `limit: int = 10` works with no annotation ceremony at all.

## Required versus optional

The rule is the same one from the Pydantic track, and it is worth restating because it is the most common confusion here too.

**A default makes it optional.** `limit: int = 10` may be omitted.

**No default makes it required.** `q: str` must be supplied, and a request without it gets a 422 whose `loc` is `("query", "q")`.

**`Optional[str]` alone does not make it optional.** It says the value may be null. To make it omissible you also need `= None`.

Most query parameters should be optional with a sensible default, because a query string is where flexibility lives &mdash; but a required one is legitimate. A search endpoint with no search term usually has nothing to do.

## Constraints with Query()

`Query()` carries the same arguments as Pydantic's `Field`:

```python
limit: int = Query(default=10, ge=1, le=100)
```

The upper bound is not decoration. Without it, `?limit=1000000` is a valid request that your database will attempt to satisfy. A cap is the cheapest denial-of-service protection available, and it becomes a documented limit rather than a surprise.

`description` matters more for query parameters than almost anywhere else, because they are what a caller experiments with. A parameter called `expand` needs a sentence saying what it expands.

## Lists

A query string expresses multiple values by repeating the key: `?tag=maths&tag=vectors`. Annotate the parameter as a list and you get one:

```python
tag: List[str] = Query(default=[])
```

The `Query(default=[])` is needed rather than a bare `= []`, because without the explicit marker FastAPI would read a list annotation as a request body.

Items are converted individually, so `List[int]` given `?id=1&id=2` gives you `[1, 2]` and `?id=abc` gives a 422 pointing at the offending item.

Comma-separated values &mdash; `?tags=a,b,c` &mdash; are **not** handled automatically. They are one string containing commas. If your API takes that form, split it in a validator, and be aware you are choosing a convention that the repeated-key form already solves.

## Booleans

This catches people, and the behaviour is right.

A query string is text, so a flag arrives as a word. `?on=true`, `?on=yes`, `?on=1` and `?on=on` all give `True`; `false`, `no`, `0` and `off` give `False`; anything else is a 422.

Compare with plain Python, where `bool("false")` is `True` because the string is non-empty. Pydantic reads the meaning of the word rather than the emptiness of the container, which is exactly what a checkbox or a `?verbose=false` needs.

## Closed sets

For a sort key, a mode or a format, `Literal` beats `str`:

```python
sort: Literal["title", "minutes"] = "title"
```

An unrecognised value is a 422 listing the options, instead of silently falling through to a default and returning data ordered in a way the caller did not ask for. And the docs show the choices.

That silent fallback is the real risk. `?sort=colour` with a plain `str` parameter typically means somebody's code has a typo and their results have been subtly wrong for weeks.

## The shape of a listing endpoint

Most collection endpoints converge on the same four concerns, and the fifth editor above puts them together: a search term, one or more filters, a sort key, and a limit.

A few habits worth carrying into your own.

**Always cap the limit.** `le=100` on the parameter, and a default well below it.

**Return the count alongside the items**, so a client knows whether to keep paging.

**Prefer explicit filters to a general query language.** `?track=maths` is easy to document and hard to abuse; a parameter that accepts arbitrary filter expressions is neither.

**Keep defaults sensible for a caller who reads nothing.** A bare `GET /modules` should return something reasonable rather than an error.

## Path or query?

The distinction that resolves most arguments: a path parameter **identifies** a resource; a query parameter **describes a view** of one or of a collection.

`/modules/7` is a thing. `/modules?track=maths` is a filtered set. `/modules/7?verbose=true` is a thing, presented differently.

If removing the value would leave you addressing a different resource, it belongs in the path. If it would leave you addressing the same resource with different presentation or filtering, it belongs in the query string.

One practical consequence: query parameters are the right place for anything optional, because a URL with an optional path segment is really two routes.

## Aliases for names Python cannot use

A query parameter is sometimes named something that is not a valid Python identifier, or is camelCase when your code is not.

`alias` handles it:

```python
item_query: str = Query(default=None, alias="item-query")
```

The URL uses `item-query`; your function uses `item_query`. The schema documents the alias, because the alias is what the wire actually carries.

This is the same mechanism as Pydantic's field aliases, applied to parameters, and it is the clean way to consume an existing API's convention without contorting your own code.

## Deprecating one

`Query(deprecated=True)` marks a parameter as deprecated in the documentation while continuing to accept it.

That is the polite way to retire a parameter: the docs show it as deprecated, existing clients keep working, and you can measure whether anyone is still sending it before removing it. Together with `AliasChoices` from the Pydantic track it makes renaming a live parameter a non-event.

## Hiding one from the docs

`Query(include_in_schema=False)` accepts a parameter without documenting it.

Use it sparingly and for good reasons &mdash; an internal debugging flag, a parameter kept only for a legacy client. An undocumented parameter that consumers are expected to use is a trap, and the fact that it works is not discoverable.

## Validation you cannot express as a constraint

Some rules span parameters: `offset` must be a multiple of `limit`, or `from` must precede `to`. A single parameter's constraints cannot say that, for the same reason a Pydantic field validator cannot see its siblings.

Two options. A dependency that takes both parameters and validates the pair &mdash; which is the idiomatic FastAPI answer, and gets its own tier. Or a model with a `model_validator`, if the parameters genuinely belong together.

What you should avoid is checking in the handler and raising a 400. It works, and it puts the rule somewhere the schema cannot see and the docs cannot show.

## Pagination, concretely

Two conventions, and the trade between them is worth knowing.

**Offset and limit** is simple and universally understood. `?offset=40&limit=20`. It degrades on large datasets, because the database still walks the skipped rows, and it can miss or duplicate items if the underlying data changes between pages.

**Cursor pagination** passes an opaque token pointing at the last item seen. It is stable under concurrent writes and stays fast at any depth, at the cost of not being able to jump to page 40.

For most APIs offset is fine and honest. For a large or busy dataset, cursors are the right answer and are much easier to introduce at the start than to retrofit.

Either way: cap the limit, return the count, and document both.

## Summary

Query parameters are the default classification, optional when they have a default, required when they do not. `Query()` adds constraints, metadata and aliases, all of which reach the schema.

Lists come from repeated keys. Booleans read words, not emptiness. `Literal` beats `str` for anything with a fixed set of values, because the alternative is a silent fallback nobody notices.

And always cap the limit.


## Mistakes people make

**An uncapped `limit`.** `?limit=1000000` is a valid request your database will try to satisfy. `le=100` is the cheapest protection available.

**A bare `= []` for a list.** Without `Query(default=[])` the list annotation is read as a request body, and the parameter silently never arrives.

**Using `str` for a sort key.** `?sort=colour` then falls through to whatever your code does with an unknown value, and nobody is told. `Literal` makes it a 422.

**Expecting comma-separated values to split.** `?tags=a,b` is one string containing commas. Repeated keys are the convention that already works.

**Assuming `Optional` makes it optional.** It only permits null. The default is what makes a parameter omissible.

**Validating a relationship in the handler.** Two parameters that must agree belong in a dependency or a model, where the rule can be documented, rather than in an `if` that raises a 400 the schema knows nothing about.

## Next

The third source of input, and the one with the most structure: the request body, where a Pydantic model does the work.

## The parameter you did not add

A last observation. Most APIs accumulate query parameters faster than they remove them, and each one is a permanent commitment: somebody will use it, and removing it later breaks them.

So the useful discipline is at the point of adding. Is this a genuine view of the collection, or is it a special case one caller asked for? Could it be a separate endpoint with a clearer name? Will it still make sense combined with the six that already exist?

An endpoint with four well-chosen parameters is easy to document and hard to misuse. One with fifteen has combinations nobody has tested, and probably some that contradict each other.

## Filtering, and where it stops

There is a gravitational pull towards making a listing endpoint do everything: more filters, then ranges, then combinations, then a small query language expressed in parameters.

It is worth resisting past a point, for two reasons. Every parameter multiplies the combinations you have not tested, and a filter language in a query string is a filter language you now maintain, document and secure.

Two better answers when the pull gets strong. A separate endpoint with a name that says what it does &mdash; `/modules/recommended` beats six parameters that together mean "recommended". Or a POST with a body, when the query genuinely is structured data; it loses cacheability and gains validation, documentation and a schema.

Neither is a failure. An endpoint that does one thing well is easier to use than one that can be persuaded to do anything.

## Defaults are an interface decision

The defaults on a listing endpoint are the behaviour most callers will ever see, because most callers send no parameters at all.

`GET /modules` with nothing else should return something useful: a sensible page size, a sensible ordering, and no filters. If the bare call returns an error, or ten thousand rows, or an arbitrary ordering that changes between requests, that is the first impression your API makes.

Choosing those defaults deliberately costs nothing and is worth more than any individual parameter you might add later.

## A closing thought

Query parameters are where an API is most flexible and therefore where it most easily becomes incoherent.

Each one is easy to add, hard to remove, and interacts with every other. The discipline that keeps a listing endpoint healthy is not technical &mdash; constraints and `Literal` handle the mechanics &mdash; but editorial: deciding what this endpoint is *for*, and declining the parameters that belong to a different question.

## One more on naming

Parameter names are part of the public interface and are read far more often than they are written.

Prefer full words to abbreviations &mdash; `limit` over `lim`, `offset` over `off`. Prefer the noun a caller would use over the one your database uses. And keep the same name for the same concept across every endpoint: an API where one route takes `limit` and another takes `page_size` makes every caller check.

`alias` exists for when the wire name and the Python name must differ. It is not a licence to have three names for the same idea.
''',
    [
        {"q": "How does FastAPI decide a parameter is a query parameter?",
         "options": ["It must be declared with Query()", "By elimination - not in the path, not a model, not a dependency", "By its type", "It must have a default"],
         "answer": 1,
         "why": "Query is the fallback classification, which is why `limit: int = 10` works with no ceremony. `Query()` is only needed to add constraints or to disambiguate a list."},
        {"q": "Why does a list query parameter need `Query(default=[])` rather than `= []`?",
         "options": ["Style", "Without the marker a list annotation is read as a request body", "Lists are not supported otherwise", "To make it required"],
         "answer": 1,
         "why": "The explicit marker tells FastAPI where the value comes from. Without it, the list annotation is classified as a body."},
        {"q": "What does `?on=false` give a `bool` parameter?",
         "options": ["True, because the string is non-empty", "False", "A 422", "None"],
         "answer": 1,
         "why": "Pydantic reads the word's meaning, not the container's emptiness - unlike `bool(\"false\")` in plain Python, which is True. That is what makes query flags work."},
        {"q": "Why use `Literal` for a `sort` parameter instead of `str`?",
         "options": ["It is faster", "An unrecognised value fails loudly instead of silently falling back to a default", "It is required", "To allow lists"],
         "answer": 1,
         "why": "A plain `str` accepts `?sort=colour`, falls through to whatever your code does with an unknown key, and nobody is told. That is how results end up subtly wrong for weeks."},
    ],
)


# ---------------------------------------------------------------------------
# 5. Request bodies
# ---------------------------------------------------------------------------
topic(
    "request_bodies",
    "Request Bodies",
    "Foundations",
    "A Pydantic model as a parameter, and everything the Pydantic track taught "
    "applied to an HTTP request.",
    _svg(_box(12, 20, 52, 24, S) + _txt(38, 36, "JSON", M, 8) +
         _arrow(66, 32, 82, 32) +
         _box(86, 20, 60, 24, S, A) + _txt(116, 36, "BaseModel", A, 8) +
         _txt(80, 66, "parsed, coerced, checked", M, 8)),
    [
        ("A model parameter is the body",
         "Annotate a parameter with a model and FastAPI parses the JSON, validates "
         "it, and hands you an object.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(default=10, gt=0, le=180)
    published: bool = False

@app.post("/modules", status_code=201)
def create(module: ModuleIn):
    return {"title": module.title, "minutes": module.minutes,
            "type": type(module.minutes).__name__}

client = TestClient(app)
r = client.post("/modules", json={"title": "Vectors", "minutes": "8"})
print(r.status_code, r.json())
print()
print("the string 8 became an int before the handler ran")'''),

        ("Failures never reach your code",
         "Every field is checked and the 422 carries the whole list, with "
         "<code>loc</code> starting at <code>body</code>.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
reached = []

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

@app.post("/modules")
def create(module: ModuleIn):
    reached.append(module.title)
    return {"ok": True}

client = TestClient(app)
r = client.post("/modules", json={"title": "no", "minutes": -1})
print("status:", r.status_code)
for err in r.json()["detail"]:
    print("  %-22s %-18s %s" % (".".join(str(p) for p in err["loc"]),
                                err["type"], err["msg"]))
print()
print("handler ran for:", reached)'''),

        ("Nested and repeated structure",
         "A model can contain models and lists of them. The error path reaches all "
         "the way down.",
         '''from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Lesson(BaseModel):
    name: str
    minutes: int = Field(gt=0)

class ModuleIn(BaseModel):
    title: str
    lessons: List[Lesson] = Field(min_length=1)

@app.post("/modules", status_code=201)
def create(module: ModuleIn):
    return {"title": module.title,
            "total": sum(l.minutes for l in module.lessons)}

client = TestClient(app)
print(client.post("/modules", json={"title": "Vectors", "lessons": [
    {"name": "Direction", "minutes": 4}, {"name": "Magnitude", "minutes": "6"}]}).json())

r = client.post("/modules", json={"title": "Vectors", "lessons": [
    {"name": "Direction", "minutes": 4}, {"name": "Magnitude", "minutes": "soon"}]})
print()
print("bad item:", r.json()["detail"][0]["loc"])'''),

        ("Body plus path plus query",
         "One handler can take all three. FastAPI works out where each comes from "
         "and the error says which.",
         '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ModuleIn(BaseModel):
    title: str
    minutes: int

@app.put("/tracks/{track}/modules/{module_id}")
def replace(track: str, module_id: int, module: ModuleIn, notify: bool = False):
    return {"track": track, "module_id": module_id,
            "title": module.title, "notify": notify}

client = TestClient(app)
r = client.put("/tracks/maths/modules/7?notify=yes",
               json={"title": "Vectors", "minutes": 8})
print(r.json())

bad = client.put("/tracks/maths/modules/seven", json={"title": "V", "minutes": "x"})
print()
print("failures name their source:")
for err in bad.json()["detail"]:
    print("  ", err["loc"])'''),

        ("Two models in one body",
         "Two model parameters make FastAPI nest them under their names, which is "
         "occasionally what you want.",
         '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Module(BaseModel):
    title: str

class Author(BaseModel):
    name: str

@app.post("/publish")
def publish(module: Module, author: Author, notify: bool = False):
    return {"module": module.title, "author": author.name, "notify": notify}

client = TestClient(app)
r = client.post("/publish?notify=1", json={
    "module": {"title": "Vectors"},
    "author": {"name": "Ada"},
})
print(r.json())
print()
print("body schema:", list(app.openapi()["paths"]["/publish"]["post"]
                           ["requestBody"]["content"]["application/json"]["schema"]))'''),

        ("Rejecting keys you did not declare",
         "By default unknown keys are ignored, which hides typos. "
         "<code>extra=\"forbid\"</code> turns them into errors.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI()

class Lenient(BaseModel):
    title: str
    minutes: int = 10

class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str
    minutes: int = 10

@app.post("/lenient")
def a(m: Lenient): return m.model_dump()

@app.post("/strict")
def b(m: Strict): return m.model_dump()

payload = {"title": "Vectors", "minuets": 30}     # typo

client = TestClient(app)
print("lenient:", client.post("/lenient", json=payload).json(),
      "<- typo vanished, minutes is the default")
r = client.post("/strict", json=payload)
print("strict :", r.status_code, r.json()["detail"][0]["loc"],
      r.json()["detail"][0]["type"])'''),
    ],
    [
        "A parameter annotated with a Pydantic model is the request body. FastAPI parses the JSON and validates it before your handler runs.",
        "The 422's <code>detail</code> is essentially <code>e.errors()</code>, with <code>loc</code> beginning <code>body</code> so a caller knows which part of the request failed.",
        "Nesting works to any depth, and the error path names the exact item: <code>('body', 'lessons', 1, 'minutes')</code>.",
        "A handler can take path, query and body parameters together &mdash; FastAPI decides each by where its name appears and what it is annotated as.",
        "Two model parameters are nested under their names in the body rather than merged.",
        "Unknown keys are ignored by default, which hides a typo as a silently-defaulted field. <code>extra=\"forbid\"</code> makes it an error.",
    ],
    '''
title: Request Bodies: A Model Is the Contract
intro: Everything the Pydantic track taught, applied to an HTTP request.

## One annotation

```python
@app.post("/modules", status_code=201)
def create(module: ModuleIn):
    ...
```

A parameter annotated with a Pydantic model is the request body. FastAPI reads the raw bytes, validates them with `model_validate_json`, and calls your handler with an object.

By the time the function runs, `module.minutes` is an integer &mdash; even if the client sent `"8"` &mdash; and every constraint on the model has passed. There is nothing to check at the top of the handler, which is the point.

This is also the moment where the whole Pydantic track becomes directly applicable. Field constraints, nested models, validators, aliases, enums, `Literal`, strict mode: all of it works here, unchanged, because this *is* Pydantic.

## Failures happen first

If the body does not fit the model, your handler is never called. FastAPI returns 422 with a `detail` that is essentially `e.errors()`.

The `loc` begins with `body`, then names the field, then the path within it. So `("body", "lessons", 1, "minutes")` is the `minutes` field of the second lesson. For a payload of any size that is the whole diagnosis.

Every field is checked, so a client with four mistakes learns about all four at once rather than one resubmission at a time. This matters most for forms, where the alternative is a genuinely unpleasant experience.

## Structure

Bodies nest as deeply as your models do. A `List[Lesson]` inside a `Module` validates each lesson with its own rules, and errors keep their index.

Two things worth carrying over from the Pydantic track.

**Constrain collections.** `Field(min_length=1)` says a module must have at least one lesson; `max_length` caps how many, which is a cheap protection against a caller sending a hundred thousand.

**Extract models that repeat.** If `Address` appears in three request bodies, it is a model, and the rules then live in one place.

## Path, query and body together

A handler can take all three, and FastAPI decides which is which by the rules from the previous modules: names in the route path are path parameters, Pydantic models are the body, everything else is a query parameter.

```python
def replace(track: str, module_id: int, module: ModuleIn, notify: bool = False):
```

The signature reads as documentation, and the 422 for a bad request names each source separately &mdash; `("path", "module_id")` and `("body", "minutes")` are different problems for the caller to fix.

## Two models

If you annotate two parameters with models, FastAPI nests them under their parameter names rather than merging:

```json
{"module": {...}, "author": {...}}
```

That is occasionally what you want. More often it is a sign that the two belong in one model, because the client now has to know a structure that exists only because of how your function was written. A single model that contains both is usually clearer, and easier to document.

`Body(embed=True)` forces the same nesting for a single model, when an existing API expects it.

## Unknown keys

By default Pydantic ignores keys it does not recognise. A client sending `minuets` instead of `minutes` gets no error and no field &mdash; `minutes` takes its default, and the bug shows up later as a duration nobody set.

`model_config = ConfigDict(extra="forbid")` makes that a 422 naming the offending key.

Which to choose is a real decision. For an internal API, forbid: a typo should be loud. For a public one, the argument for ignoring is forward compatibility, since a client sending fields from a newer version should not break against an older server.

What you should not do is leave it unconsidered, which is what usually happens.

## Which methods take a body

`POST`, `PUT` and `PATCH` do. `GET` and `DELETE` conventionally do not, and while FastAPI will let you declare a body on a GET, many clients, proxies and caches will drop it. If a GET needs structured input, that is a sign it wants query parameters, or that it is really a POST.

The distinction between the three that do:

**POST** creates something, and the server decides its identity.

**PUT** replaces a resource entirely at a known URL &mdash; so a PUT body should contain every field, and omitting one means clearing it.

**PATCH** updates part of one, which is where `exclude_unset` from the Pydantic track earns its place: dump only what the caller supplied, so untouched fields stay untouched.

Getting PUT and PATCH backwards is common and produces the bug where an update wipes fields the client never mentioned.

## Raw bodies

Not everything is JSON. `Request` gives you the raw object, with `await request.body()` for the bytes &mdash; needed for a webhook whose signature is computed over the exact payload, since re-serialising a parsed model produces different bytes.

`Body(media_type="text/plain")` handles a plain-text body. Form data and file uploads have their own module in the next tier.

Reach for these deliberately. A raw body means no validation, no schema, and no documentation, so it should be a considered exception rather than a way of avoiding writing a model.

## Designing the model

Two habits, both from the Pydantic track and both worth repeating because bodies are where they pay off most.

**A separate model per direction.** `ModuleCreate` takes what a caller may supply, with no server-assigned id. `ModuleUpdate` has everything optional. `ModuleOut` declares exactly what may be seen. One model with everything optional documents nothing and guarantees nothing.

**Describe the fields.** A `description` on a body field appears next to it in the docs, and an `examples` entry pre-fills the interactive request form &mdash; which is the difference between a first-time caller succeeding and guessing.

## Documenting the body

Everything the Pydantic track said about schema metadata applies, and bodies are where it pays off most.

`description` on a field appears beside it in the interactive docs. `examples` pre-fills the request form, which is the difference between a first-time caller pressing "Try it out" and getting a working request, or an empty box they have to guess at.

Model-level examples are even better for a body:

```python
model_config = ConfigDict(
    json_schema_extra={"examples": [{"title": "Vectors", "minutes": 8}]})
```

Now the docs show a complete sample payload somebody can copy.

`Body(embed=True)` and `Body(examples=[...])` do the same at the parameter level when you need to override what the model says.

## Size limits

FastAPI does not cap request body size by default. That is worth knowing, because an endpoint accepting JSON will attempt to parse whatever arrives.

The cap normally belongs upstream &mdash; in nginx, in your ingress, in the platform &mdash; and it is one of the standard things to check before an API is public. Within the app, `max_length` on collections limits how many items a body may contain, which handles the common case of a bulk endpoint being handed a hundred thousand records.

## Validation that needs the whole body

A rule spanning two fields belongs in a `model_validator(mode="after")`, exactly as in the Pydantic track. The error arrives with `loc: ["body"]` &mdash; no field, because it belongs to the object &mdash; and a client needs somewhere to display it.

A rule spanning the body *and* a path parameter is different: no model can see both. That is a dependency, or a check at the top of the handler raising a 400 or 409. It is one of the few cases where logic in the handler is the honest answer, because the relationship is between HTTP concerns rather than within the data.

## Idempotency, briefly

A POST that creates something is not idempotent: a client that times out and retries may create two.

The usual answer is an idempotency key &mdash; a header the client generates, which the server records alongside the result, returning the original response on a repeat. That is beyond a first tier, but it is worth knowing the problem exists before an API is handling anything that matters, because retrofitting it after the duplicates appear is much harder.

## Summary

A model parameter is the body. Everything from Pydantic applies: constraints, nesting, validators, aliases, strict mode.

Validation runs before your handler, and a 422 carries every problem with `loc` starting at `body`. Unknown keys are ignored unless you forbid them. Separate models per direction, and describe the fields &mdash; the docs are generated from them, and a good example is the cheapest thing you can do for whoever calls you.


## Mistakes people make

**Reusing one model for input and output.** The result is a model where everything is optional, which documents nothing and guarantees nothing in either direction.

**Leaving `extra` at the default on an internal API.** A misspelt key silently becomes a defaulted field, and the bug appears later as a value nobody set.

**Treating PUT as PATCH.** A PUT body should be complete; an omitted field means clearing it. Using PUT for partial updates is how an edit wipes six columns the client never mentioned.

**Declaring a body on a GET.** Some clients and proxies drop it. If a read needs structured input, it wants query parameters, or it is really a POST.

**Two model parameters where one model belongs.** It forces callers to learn a nesting that exists only because of how your function was written.

**No cap on collection size.** `max_length` on a list field is what stops a bulk endpoint being handed a hundred thousand records.

**Re-serialising a body you needed verbatim.** A webhook signature is computed over the exact bytes; `await request.body()` is the only thing that gives you those.

## Next

The other half of the exchange: `response_model`, which decides what comes back and, just as importantly, what cannot leak.

## The body is the contract

Of everything an endpoint declares, the body model is the part consumers read most carefully, because it is what they have to construct.

Which makes it worth more care than the rest. Field names that read well. Descriptions on anything not self-evident. A complete example. Constraints that state the real limits rather than leaving them to be discovered by rejection. Required fields that are genuinely required, and defaults that are genuinely sensible.

None of that changes behaviour. All of it changes how long somebody spends getting their first successful request, which is the number that decides whether they enjoy using your API.

## Accepting change from clients

The mirror of the previous point: how a body model can evolve without breaking senders.

**Adding an optional field is safe.** Old clients omit it and get the default.

**Adding a required field is breaking.** Every existing client immediately starts getting 422s. If a field must become required, give it a default first, deprecate the absence, then tighten.

**Loosening a constraint is safe.** Tightening one is not &mdash; a `max_length` reduced from 100 to 50 rejects requests that worked yesterday.

**Renaming is breaking**, unless you accept both names for a while, which is exactly what `AliasChoices` from the Pydantic track is for.

This is why `extra="ignore"` is defensible on a public API even though `forbid` catches typos: a client sending fields from a newer version keeps working against an older server. It is a trade between catching mistakes and tolerating drift, and which side you want depends on who is calling.

## What the model is really doing

A body model is doing three jobs that would otherwise be three separate pieces of code.

It **parses**, turning bytes into typed values. It **validates**, rejecting anything that does not fit before your logic sees it. And it **documents**, appearing in the schema so callers know what to send without reading your source.

Written by hand those drift apart: the parser accepts something the validator rejects, and the documentation describes a shape neither of them implements. One class keeps all three in agreement because they are all generated from it.

## A closing thought

Almost every question about request bodies turns out to be a Pydantic question wearing an HTTP hat: what will it coerce, what is required, how do I express this rule, why did that fail.

Which is good news, because it means the body is the part of an API where the least framework-specific knowledge is needed. Get the models right and the endpoints are a formality.
''',
    [
        {"q": "How does FastAPI know a parameter is the request body?",
         "options": ["It must be called `body`", "It is annotated with a Pydantic model", "It uses Body()", "It is the last parameter"],
         "answer": 1,
         "why": "A model annotation is the signal. Path names come from the route, and anything else defaults to a query parameter."},
        {"q": "What is `loc` for a bad field inside the second item of a list in the body?",
         "options": ["('minutes',)", "('body', 'minutes')", "('body', 'lessons', 1, 'minutes')", "()"],
         "answer": 2,
         "why": "The path names the source, the field, the index and the inner field - which for a large payload is the entire diagnosis."},
        {"q": "A client sends `minuets` instead of `minutes`. What happens by default?",
         "options": ["422", "The key is ignored and `minutes` takes its default", "The value is stored anyway", "A warning"],
         "answer": 1,
         "why": "Pydantic ignores unknown keys unless told otherwise. `extra=\"forbid\"` makes it a 422 - usually right for an internal API, weighed against forward compatibility for a public one."},
        {"q": "What distinguishes PUT from PATCH?",
         "options": ["Nothing", "PUT replaces the whole resource; PATCH updates part of it", "PUT is for creation", "PATCH cannot take a body"],
         "answer": 1,
         "why": "A PUT body should be complete, and an omitted field means clearing it. PATCH updates only what was sent, which is what `model_dump(exclude_unset=True)` is for."},
    ],
)


# ---------------------------------------------------------------------------
# 6. Response models
# ---------------------------------------------------------------------------
topic(
    "response_models",
    "Response Models",
    "Foundations",
    "Declaring what comes back - which documents the endpoint and, more usefully, "
    "decides what cannot leak.",
    _svg(_box(12, 22, 56, 24, S) + _txt(40, 38, "row", M, 8) +
         _arrow(70, 34, 86, 34) +
         _box(90, 22, 56, 24, S, A) + _txt(118, 38, "ModuleOut", A, 8) +
         _txt(80, 66, "filtered  -  validated  -  documented", M, 8)),
    [
        ("Without one, whatever you return is sent",
         "A handler returning an internal row sends every key in it, including the "
         "ones nobody outside should see.",
         '''from fastapi import FastAPI

app = FastAPI()

ROW = {"id": 1, "title": "Vectors", "minutes": 8,
       "internal_notes": "needs a diagram",
       "author_email": "ada@vizlearn.in"}

@app.get("/modules/1")
def read():
    return ROW

print(TestClient(app).get("/modules/1").json())
print()
print("Two fields there were never meant for a caller.")'''),

        ("response_model decides the shape",
         "Declare it and the return value is filtered through the model. Anything "
         "not declared is dropped.",
         '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

ROW = {"id": 1, "title": "Vectors", "minutes": 8,
       "internal_notes": "needs a diagram",
       "author_email": "ada@vizlearn.in"}

class ModuleOut(BaseModel):
    id: int
    title: str
    minutes: int

@app.get("/modules/1", response_model=ModuleOut)
def read():
    return ROW                      # extra keys are removed, not sent

print(TestClient(app).get("/modules/1").json())
print()
print("The handler still returns the whole row. The model decides what leaves.")'''),

        ("The return annotation works too",
         "Annotating the return type does the same job and reads better. FastAPI "
         "treats it as the response model.",
         '''from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ModuleOut(BaseModel):
    id: int
    title: str

DB = [{"id": 1, "title": "Vectors", "secret": "x"},
      {"id": 2, "title": "Norms", "secret": "y"}]

@app.get("/modules")
def list_modules() -> List[ModuleOut]:
    return DB

client = TestClient(app)
print(client.get("/modules").json())
print()
print("A list works the same way, filtered item by item.")'''),

        ("It validates your own output",
         "The response is checked against the model. A handler that returns the wrong "
         "shape fails loudly instead of shipping it.",
         '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ModuleOut(BaseModel):
    id: int
    title: str

@app.get("/good", response_model=ModuleOut)
def good():
    return {"id": 1, "title": "Vectors"}

@app.get("/bad", response_model=ModuleOut)
def bad():
    return {"id": "not-a-number", "title": "Vectors"}

client = TestClient(app)
print("good:", client.get("/good").status_code, client.get("/good").json())
try:
    r = client.get("/bad")
    print("bad :", r.status_code)
except Exception as e:
    print("bad : raised", type(e).__name__)
    print("      ", str(e).splitlines()[-1][:90])
print()
print("A broken response is a 500 - your bug, not the caller's.")'''),

        ("Dropping unset and null fields",
         "<code>response_model_exclude_none</code> and its siblings trim the output "
         "without a second model.",
         '''from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ModuleOut(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    tags: list = []

ROW = {"id": 1, "title": "Vectors"}

@app.get("/plain", response_model=ModuleOut)
def plain(): return ROW

@app.get("/tight", response_model=ModuleOut, response_model_exclude_none=True)
def tight(): return ROW

@app.get("/unset", response_model=ModuleOut, response_model_exclude_unset=True)
def unset(): return ROW

client = TestClient(app)
print("plain :", client.get("/plain").json())
print("none  :", client.get("/tight").json())
print("unset :", client.get("/unset").json())'''),

        ("Input and output are different shapes",
         "Separate models for what you accept and what you return &mdash; the pattern "
         "almost every real endpoint ends up with.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
DB = {}

class ModuleCreate(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(default=10, gt=0)

class ModuleOut(BaseModel):
    id: int
    title: str
    minutes: int

@app.post("/modules", response_model=ModuleOut, status_code=201)
def create(module: ModuleCreate):
    new_id = len(DB) + 1
    DB[new_id] = {"id": new_id, **module.model_dump(),
                  "created_by": "internal-service"}
    return DB[new_id]

client = TestClient(app)
r = client.post("/modules", json={"title": "Eigenvalues", "minutes": 14})
print("returned:", r.json())
print("stored  :", DB[1])
print()
print("created_by is in the store and not in the response.")'''),
    ],
    [
        "Without a <code>response_model</code>, whatever the handler returns is serialised &mdash; including keys that were never meant to leave.",
        "With one, the return value is filtered through the model. Undeclared fields are dropped rather than sent.",
        "A return-type annotation (<code>-&gt; ModuleOut</code>) does the same job and usually reads better.",
        "The response is validated too. A handler returning the wrong shape produces a 500, which is correct &mdash; it is your bug, not the caller's.",
        "<code>response_model_exclude_none</code>, <code>_exclude_unset</code> and <code>_exclude</code> trim output without needing a second model.",
        "Separate input and output models are the norm: what a caller may send and what they may see are different questions.",
    ],
    '''
title: Response Models: Deciding What Leaves
intro: Declaring the response documents the endpoint and, more usefully, stops things escaping.

## The default is generous

Without a response model, FastAPI serialises whatever your handler returns.

That is convenient and it is how data leaks. A handler that returns a database row returns *all* of it: internal notes, an email address, a password hash, a flag nobody outside should know exists. Nothing warns you, because from the framework's point of view you asked for exactly that.

The failure mode is quiet and it compounds. A column added to a table six months later silently starts appearing in an API response, because the endpoint was never told what it was allowed to send.

## Declaring the shape

```python
@app.get("/modules/1", response_model=ModuleOut)
def read():
    return ROW
```

Now the return value is passed through `ModuleOut`. Fields the model declares are kept; everything else is dropped.

The handler is unchanged &mdash; it still returns the whole row &mdash; but the model decides what leaves. That separation is the useful part: your data access can return whatever is natural, and the contract with the outside world is stated once, in a class, where it can be reviewed.

The modern spelling is a return annotation:

```python
def list_modules() -> List[ModuleOut]:
```

Same behaviour, and it reads as Python rather than as framework configuration. Use `response_model=` when the two need to differ &mdash; returning a `Response` directly, for instance, while still documenting the shape.

## It checks your work

The response is validated against the model, which is worth appreciating.

If a handler returns `{"id": "not-a-number"}` for a field declared `int`, that is a 500. The caller sent nothing wrong; your code produced something that does not match its own contract, and the framework refuses to ship it.

That is the right behaviour and it catches real bugs &mdash; a query returning a string where a number was expected, a field renamed in one place and not another, a `None` where the model promised a value. Without a response model, all of those reach the client and become their problem to diagnose.

## Trimming the output

Three arguments handle the common adjustments without a second model.

`response_model_exclude_none=True` drops fields that are `None`. Useful for a sparse response where nulls carry no information.

`response_model_exclude_unset=True` drops fields that were never set, keeping explicit nulls. This is the one that matters for anything update-shaped, for the reasons the Pydantic track laid out.

`response_model_exclude={"field"}` removes named fields.

They are convenient and they are a slope. Once you are passing two of them plus an exclusion set, a dedicated output model is clearer, appears correctly in the schema, and cannot silently start including a field that was renamed.

## Input and output are different questions

The pattern almost every endpoint converges on is separate models per direction.

**Create** takes what a caller may supply. No id, because the server assigns it. No `created_by`, because the server knows it.

**Out** declares what a caller may see. It includes the id, excludes anything internal, and is required to be complete &mdash; by the time you are returning one, those fields exist.

**Update** has everything optional, and is applied with `exclude_unset`.

Three small classes instead of one clever one. The temptation is always to reuse a single model with optional fields, and it produces an API that documents nothing: every field might be missing, so no client can tell what is guaranteed either way.

## What it does for the documentation

The response model is what makes the generated docs describe the response, not just the request.

Without one, the OpenAPI document says the endpoint returns "anything". Every generated client then produces an untyped result, and every consumer writes their own guess at the shape.

With one, the schema describes the response precisely, and clients get a real type. That is the difference between an API somebody can build against confidently and one they have to explore by trial.

Descriptions and examples on output fields are worth writing for the same reason they are on inputs &mdash; they appear in the docs next to the field.

## A few practical notes

**Status codes.** `response_model` describes the success response. Error shapes are documented separately with `responses={404: {...}}`, which is worth doing for an API with consumers.

**Lists.** `-> List[ModuleOut]` filters each item. There is no extra work for collections.

**ORM objects.** If the handler returns an ORM row rather than a dict, the output model needs `from_attributes=True` so it can read attributes. That is the setting called `orm_mode` in Pydantic v1, and it is the usual reason a response model raises when it looks like it should work.

**Performance.** Filtering costs a validation pass per response. It is cheap, and for a large list it is not free &mdash; but shipping fields you did not intend to is a worse problem than a few microseconds.

## The habit worth forming

Declare a response model on every endpoint that returns data, even when it looks identical to what you are returning anyway.

The value is not in today's filtering; it is that the endpoint now has a written contract. When a column is added to the underlying table next year, the response does not change, because something declared what the response is.

## Documenting the errors too

`response_model` describes the success case. An endpoint that can return a 404 says nothing about it by default, so a generated client has no idea what shape an error takes.

`responses=` fills the gap:

```python
@app.get("/modules/{id}", response_model=ModuleOut,
         responses={404: {"description": "Module not found"}})
```

For an API with consumers this is worth doing on every endpoint that can fail in a meaningful way. It costs a line and it turns "you will get something on failure" into a documented contract.

## Status codes and the response model

The declared model describes the route's *default* status. A handler returning a different status with a different shape &mdash; a 202 with a job id rather than a 201 with the object &mdash; is returning something the schema does not describe.

`responses=` can document those alternatives with their own models, which keeps the document honest. The alternative, an endpoint whose real behaviour is broader than its schema, is the thing that makes generated clients untrustworthy.

## Response models and inheritance

A common shape is a base model with the shared fields and variants that add to it:

```python
class ModuleBase(BaseModel):
    title: str
    minutes: int

class ModuleOut(ModuleBase):
    id: int
```

Worth knowing: if a field is annotated with the base and the handler returns a subclass instance, the extra fields are **not** serialised. The response contains what was promised, not what the object happened to carry.

That is a safety property rather than a limitation &mdash; it stops a richer internal object leaking through an endpoint documented as returning the base &mdash; and it surprises people who expected the subclass's data. `SerializeAsAny` opts out where the richer output is genuinely intended and everything in it is safe to expose.

## The cost

Filtering runs a validation pass per response. For a single object it is nothing. For a list of ten thousand it is measurable, and it is doing real work &mdash; checking every field of every item against the model.

Two honest options if it ever matters. Return fewer items, which is usually the right answer and is what pagination is for. Or, for a genuinely hot endpoint, return a `Response` with pre-serialised content and document the shape with `responses=` &mdash; accepting that you have opted out of the checking.

Measure before doing the second. The cost of shipping a field you did not intend is higher than a few milliseconds.

## Summary

Declare a response model on every endpoint that returns data. It filters the output, validates your own work, and gives the documentation something to describe.

Separate input and output models, because what a caller may send and what they may see are different questions. Use `responses=` for the failure shapes. And remember `from_attributes=True` when the handler returns an ORM row rather than a dict.


## Mistakes people make

**Not declaring one.** The most consequential omission in this module. Whatever the handler returns is sent, and a column added to a table next year silently joins the response.

**Filtering with arguments instead of a model.** Once you are passing `exclude_none` plus an exclusion set, a dedicated output model is clearer and cannot silently start including a renamed field.

**Forgetting `from_attributes=True`.** The usual reason a response model raises on an ORM row when it looks like it should work.

**Documenting only the happy path.** An endpoint that can 404 should say so with `responses=`, or a generated client has no idea what failure looks like.

**Expecting a subclass's extra fields to appear.** Serialisation follows the declared type, deliberately &mdash; it stops a richer internal object leaking through an endpoint documented as returning the base.

**Putting secrets in a model and excluding them.** `Field(exclude=True)` works and depends on nobody removing it. A separate output model that simply has no such field cannot fail that way.

## Next

What happens when the input does not fit: the 422, where it comes from, and how to turn it into something a caller can act on.

## Two directions, two contracts

The symmetry is worth stating plainly.

The request model is a promise to your own code: past validation, the data is this shape.

The response model is a promise to everybody else: this is what you will receive, and nothing more.

Both are enforced. Both appear in the documentation. Both are one class each, and the discipline they buy &mdash; knowing exactly what crosses each boundary in each direction &mdash; is most of what separates an API that stays maintainable from one that accumulates surprises.

## Evolving a response safely

Once clients exist, the response is a contract, and the rules for changing it are asymmetric.

**Adding a field is safe.** A well-written client ignores what it does not recognise.

**Removing one is breaking.** So is renaming, which is a removal and an addition.

**Changing a type is breaking**, including narrowing &mdash; a field that was sometimes null and is now always present will be fine, but the reverse will not.

The practical sequence for removing a field: mark it deprecated in the docs, keep returning it, measure whether anyone reads it if you can, then remove it in a new version.

A response model makes all of this visible, which is the underrated part. Without one, nobody can say what the contract was, so nobody can say whether a change breaks it.

## The question to ask each endpoint

For every endpoint that returns data, one question: **could this ever contain something a caller should not see?**

If the answer is no with certainty, a response model is still worth declaring for the documentation.

If the answer is anything else &mdash; and for anything reading from a database it usually is &mdash; the model is the only thing standing between your storage and your consumers. Not a code review, not a convention, not the discipline of whoever writes the next handler. A class that says what may leave.

## A closing thought on trust

An API's consumers cannot read your handlers. Everything they know comes from the schema and from what the endpoint actually returns, and when those two disagree the schema loses &mdash; they will build against the observed behaviour, including the fields you did not mean to send.

That is the real reason to declare the response. Not tidiness, and not the small validation benefit, but that it makes the documented contract and the actual behaviour the same object. Once they are the same object they cannot drift, and a consumer reading your docs is reading the truth rather than an intention.

## The cost of not having one

It is worth being concrete about what goes wrong, because the failure is never immediate.

An endpoint returns a row. Six months later a column is added &mdash; an internal flag, a partner's reference, an audit field. Nobody edits the endpoint, because nobody needs to. The field starts appearing in every response.

If it is harmless, a consumer eventually builds against it and you can no longer remove it. If it is not harmless, you have been leaking it for however long it takes somebody to notice.

Neither outcome involves anyone making a mistake. That is what makes the response model worth declaring on endpoints that appear not to need one.
''',
    [
        {"q": "What happens without a `response_model`?",
         "options": ["Nothing is returned", "Whatever the handler returns is serialised, including internal fields", "A 500", "Only declared fields are sent"],
         "answer": 1,
         "why": "The framework sends what you gave it. That is how a column added to a table later silently starts appearing in an API response."},
        {"q": "A handler returns `{\"id\": \"abc\"}` where the response model declares `id: int`. What does the caller get?",
         "options": ["The string", "A 422", "A 500", "None"],
         "answer": 2,
         "why": "The caller sent nothing wrong; your code broke its own contract, so it is a server error. Without a response model that malformed value would have shipped."},
        {"q": "Why use separate Create and Out models?",
         "options": ["Performance", "What a caller may send and what they may see are different questions", "It is required", "To avoid validation"],
         "answer": 1,
         "why": "A single model with everything optional documents nothing - no client can tell what is guaranteed in either direction."},
        {"q": "Your handler returns an ORM row and the response model raises. What is usually missing?",
         "options": ["response_model_exclude_none", "`from_attributes=True` on the output model", "A status code", "An alias"],
         "answer": 1,
         "why": "By default a model validates from a mapping. `from_attributes=True` - `orm_mode` in Pydantic v1 - lets it read attributes off an object instead."},
    ],
)


# ---------------------------------------------------------------------------
# 7. Reading a 422
# ---------------------------------------------------------------------------
topic(
    "reading_a_422",
    "Reading a 422",
    "Foundations",
    "Where the validation error comes from, what each part of it means, and how to "
    "turn it into something a caller can act on.",
    _svg(_box(14, 18, 132, 20, S, A) + _txt(80, 32, "422 Unprocessable Entity", A, 8) +
         _box(14, 44, 132, 14, S) + _txt(80, 54, "loc  -  where in the request", M, 7) +
         _box(14, 60, 132, 14, S) + _txt(80, 70, "type  -  which rule", M, 7)),
    [
        ("It is a Pydantic error in an HTTP envelope",
         "The <code>detail</code> list is essentially <code>e.errors()</code>, with "
         "one addition: <code>loc</code> starts with the part of the request.",
         '''import json
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

@app.post("/modules")
def create(module: ModuleIn):
    return {"ok": True}

r = TestClient(app).post("/modules", json={"title": "no", "minutes": -1})
print("status:", r.status_code)
print(json.dumps(r.json(), indent=2))'''),

        ("loc says which part of the request",
         "Path, query, header, body &mdash; the first element tells the caller where "
         "to look, which a bare field name cannot.",
         '''from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class Body(BaseModel):
    minutes: int

@app.post("/tracks/{track_id}/modules")
def create(track_id: int, body: Body,
           limit: int = 10, x_token: str = Header()):
    return {"ok": True}

client = TestClient(app)
r = client.post("/tracks/abc/modules?limit=lots", json={"minutes": "soon"})

for err in r.json()["detail"]:
    print("%-10s %-14s %s" % (err["loc"][0], ".".join(str(p) for p in err["loc"][1:]),
                              err["type"]))'''),

        ("Every failure, in one response",
         "Validation does not stop at the first problem, so a caller can fix "
         "everything in one pass.",
         '''from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Lesson(BaseModel):
    name: str = Field(min_length=2)
    minutes: int = Field(gt=0)

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    lessons: List[Lesson]

@app.post("/modules")
def create(m: ModuleIn):
    return {"ok": True}

r = TestClient(app).post("/modules", json={
    "title": "x",
    "lessons": [{"name": "Direction", "minutes": 4},
                {"name": "M", "minutes": -1},
                {"minutes": 5}],
})
print("problems:", len(r.json()["detail"]))
for err in r.json()["detail"]:
    print("  ", ".".join(str(p) for p in err["loc"]), "->", err["type"])'''),

        ("422 is not the same as 400 or 404",
         "Validation produces a 422 automatically. Anything your own code decides is "
         "wrong is an <code>HTTPException</code> you raise.",
         '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
DB = {1: {"id": 1, "title": "Vectors"}}

class ModuleIn(BaseModel):
    title: str

@app.get("/modules/{module_id}")
def read(module_id: int):
    if module_id not in DB:
        raise HTTPException(status_code=404, detail="Module not found")
    return DB[module_id]

client = TestClient(app)
print("found     :", client.get("/modules/1").status_code, client.get("/modules/1").json())
r = client.get("/modules/99")
print("missing   :", r.status_code, r.json())
r = client.get("/modules/abc")
print("malformed :", r.status_code, r.json()["detail"][0]["type"])
print()
print("404 is a fact about the world; 422 is a fact about the request.")'''),

        ("Turning it into your own shape",
         "A custom handler for <code>RequestValidationError</code> lets you return "
         "the error format your clients already expect.",
         '''import json
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

MESSAGES = {
    "missing": "This field is required.",
    "string_too_short": "Needs at least {min_length} characters.",
    "greater_than": "Must be more than {gt}.",
    "int_parsing": "Please enter a whole number.",
}

@app.exception_handler(RequestValidationError)
async def tidy(request: Request, exc: RequestValidationError):
    problems = {}
    for err in exc.errors():
        field = ".".join(str(p) for p in err["loc"][1:]) or "_body"
        template = MESSAGES.get(err["type"])
        msg = template.format(**err.get("ctx", {})) if template else err["msg"]
        problems.setdefault(field, []).append(msg)
    return JSONResponse(status_code=422, content={"errors": problems})

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

@app.post("/modules")
def create(m: ModuleIn):
    return {"ok": True}

r = TestClient(app).post("/modules", json={"title": "x", "minutes": 0})
print(json.dumps(r.json(), indent=2))'''),

        ("Testing that a request is rejected",
         "Assert on <code>loc</code> and <code>type</code>, never on the message &mdash; "
         "prose gets reworded.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

@app.post("/modules")
def create(m: ModuleIn):
    return {"ok": True}

client = TestClient(app)

def problems(payload):
    r = client.post("/modules", json=payload)
    return r.status_code, {(tuple(e["loc"]), e["type"]) for e in r.json()["detail"]}

status, found = problems({"title": "x", "minutes": 0})
print("status:", status)
for loc, kind in sorted(found):
    print("  ", loc, kind)

expected = {(("body", "title"), "string_too_short"),
            (("body", "minutes"), "greater_than")}
print()
print("matches what we expected:", found == expected)'''),
    ],
    [
        "A 422's <code>detail</code> is Pydantic's <code>e.errors()</code>, with <code>loc</code> prefixed by the part of the request: <code>path</code>, <code>query</code>, <code>header</code>, <code>cookie</code> or <code>body</code>.",
        "Every field is checked, so one response carries every problem &mdash; a caller can fix them all in one pass.",
        "422 means the request did not fit the declared shape. It is produced before your handler runs.",
        "404, 403 and 409 are facts your code establishes, so they are <code>HTTPException</code>s you raise. Do not conflate them with 422.",
        "An <code>@app.exception_handler(RequestValidationError)</code> lets you return whatever error envelope your clients expect.",
        "In tests, assert on <code>loc</code> and <code>type</code>. Messages are prose and get reworded between releases.",
    ],
    '''
title: Reading a 422, and Making It Useful
intro: Where the validation error comes from, what each part means, and how to reshape it for your callers.

## Where it comes from

A 422 is not something FastAPI invents. It is a Pydantic `ValidationError`, caught at the boundary and rendered as JSON.

The `detail` array is essentially `e.errors()` from the Pydantic track, with one addition: `loc` is prefixed by the part of the request the value came from. So a field error in the body has `loc: ["body", "minutes"]` rather than just `["minutes"]`.

Everything the Pydantic track said about reading these applies directly. `loc` is a path. `type` is a stable machine code. `msg` is prose. `input` is what actually arrived. `ctx` carries the rule's parameters.

## The first element is the useful addition

`path`, `query`, `header`, `cookie` or `body`.

That tells a caller *where to look*, which a bare field name cannot. A client receiving "minutes is invalid" does not know whether to fix the URL, a query parameter or the JSON they posted. `["query", "limit"]` versus `["body", "minutes"]` resolves it immediately.

It also means code that reads `loc[0]` as the field name is wrong here in a way it was not in plain Pydantic. Skip the first element when you want the field, and use it when you want the source.

## Everything at once

Validation checks every parameter and every field, then raises once.

For a form, that is the difference between highlighting four broken inputs immediately and revealing them one submission at a time. For a machine client, it is one round trip instead of four.

Errors from different sources arrive together, too. A request with a bad path parameter, a bad query parameter and two bad body fields produces one response listing all four, each labelled with its source.

## 422 versus everything else

This distinction is worth being precise about, because conflating the codes makes an API harder to use.

**422** means the request did not fit the declared shape. It is produced automatically, before your handler runs, and it is always the caller's mistake.

**400** means the request was syntactically fine but wrong in some way your own code determined. It is one you raise.

**404** means the thing is not there. That is a fact about the world, not about the request &mdash; `/modules/99` is a perfectly well-formed request. Your code looks, does not find, and raises.

**409** means the request conflicts with current state: a duplicate, a version mismatch, an already-completed action.

**403** means understood, well-formed, and not allowed.

The rule: if validation can determine it from the declared types and constraints, it is a 422 and you do not write it. If it requires knowing something about the world &mdash; existence, permission, current state &mdash; it is an `HTTPException` you raise.

A common mistake is returning 422 for a missing resource because "the id was invalid". The id was fine; nothing with that id exists. That is a 404.

## Reshaping it

The default envelope is a list of objects with `loc`, `type`, `msg` and `input`. It is precise and it is not what most front ends want, which is usually a map of field to messages.

An exception handler converts it:

```python
@app.exception_handler(RequestValidationError)
async def tidy(request, exc):
    problems = {}
    for err in exc.errors():
        field = ".".join(str(p) for p in err["loc"][1:]) or "_body"
        problems.setdefault(field, []).append(err["msg"])
    return JSONResponse(status_code=422, content={"errors": problems})
```

A list per field, because one field can break several rules at once. The `or "_body"` catches model-level errors from cross-field validators, whose `loc` is just `["body"]` &mdash; and something has to display those, since they are not attached to any input.

Combine it with the message table from the Pydantic track and you get copy a person can read, driven by `type` rather than by matching on prose, with `ctx` filling in the actual limits.

Two cautions. Keep the status at 422 rather than inventing your own; clients and tooling recognise it. And log the original `exc.errors()` even while returning your tidied version &mdash; when a caller says "it rejected my email and it was fine", the `input` value settles it.

## Testing rejections

Validation deserves tests, and the useful ones assert on `loc` and `type`:

```python
expected = {(("body", "title"), "string_too_short"),
            (("body", "minutes"), "greater_than")}
```

Asserting on `msg` makes the suite fail whenever Pydantic rewords something, which teaches people to distrust it. Asserting on the pair tests what you actually care about: that the right rule fired on the right field.

Testing the *positive* case matters too. A test that a valid payload gives 201 and the coerced values you expect documents an intention that is otherwise invisible.

## What a good error experience looks like

Three things, and they are cheap.

**Constrain in the model**, so the rule appears in the schema. A caller reading your docs learns the limit before sending anything.

**Give fields descriptions and examples**, so the interactive docs show a working request rather than an empty box.

**Translate `type` codes** into sentences your users can act on, falling back to `msg` for anything unmapped so nothing renders blank.

Most APIs do none of these and return the raw envelope. It is usable, and the gap between usable and good here is about twenty lines.

## Other errors FastAPI produces

Validation is not the only automatic failure, and recognising the others saves time.

**405 Method Not Allowed** means the path matched a route registered for a different method. Usually a POST to a GET-only route, or a typo in the decorator.

**307 Temporary Redirect** is the trailing-slash redirect. Harmless until a client drops the body following it, which turns into a POST that arrives mysteriously empty.

**500** with a serialisation message is the response model rejecting what your handler produced.

**422 on something you thought was a query parameter** usually means FastAPI classified it as a body &mdash; a list annotation without `Query()` is the common cause.

## Handling everything else

`RequestValidationError` covers input. Two more handlers complete the picture.

`HTTPException` has a default handler you can override, if you want your own envelope for the 404s and 403s you raise as well as for validation.

A handler for `Exception` catches everything unexpected, which is where you turn an unhandled error into a clean 500 rather than a traceback. Log the real exception there, return something generic to the caller, and never include the traceback in the response &mdash; it is an information leak, and it is the sort that ends up in a screenshot.

Custom exception classes with their own handlers are worth it once an app has real domain errors. Raising `ModuleNotFound` from a service and mapping it to a 404 in one handler keeps HTTP concerns out of your business logic entirely.

## Why 422 rather than 400

Some APIs use 400 for validation failures, and people occasionally want to change FastAPI's default.

422 means "I understood the request and cannot process the entity" &mdash; the syntax was fine, the content was not. 400 means the request itself was malformed. For a well-formed JSON body with a field out of range, 422 is the more precise statement.

The practical argument for leaving it alone is that clients and tooling recognise the FastAPI convention, and changing it gains nothing except matching a preference. If you must, an exception handler can return 400 with the same body &mdash; but do it consistently across every endpoint or you have made things worse.

## What to log

Log the full `exc.errors()` with a request identifier, and return your tidied version.

The reason is a conversation that happens with every API: a caller reports that a valid request was rejected. The `input` field settles it in seconds &mdash; it shows exactly what arrived, which is frequently not what they believe they sent. Without it, you are asking them to reproduce something they cannot see either.

Do not log the whole body indiscriminately. It may contain passwords, tokens or personal data, and a log is a place things persist. The error entries carry the offending values only, which is usually the right amount.

## Summary

A 422 is a Pydantic error with an HTTP envelope. `loc` names the source and the path; `type` is the stable code to match on; `input` is what actually arrived.

Every problem arrives at once. Validation failures are 422s you never write; facts about the world &mdash; missing, forbidden, conflicting &mdash; are exceptions you raise. Reshape the envelope with an exception handler if your clients expect something else, keep the status, and log the original.


## Mistakes people make

**Reading `loc[0]` as the field name.** Here the first element is the source &mdash; `body`, `query`, `path`, `header`. The field starts at index one.

**Returning 422 for a missing resource.** The request was well-formed; nothing with that id exists. That is a 404 you raise.

**Asserting on `msg` in tests.** Prose gets reworded and the suite fails for no real reason, which teaches people to ignore it. Assert on `loc` and `type`.

**Assuming `loc` always has a field.** A cross-field validator produces `["body"]` with nothing after it, and code indexing past the end raises the first time such a rule is added.

**Returning the traceback on a 500.** An information leak, and the sort that ends up in a screenshot in a public issue.

**Not logging the original errors.** When a caller insists their request was valid, the `input` value settles it in seconds. Without it, you are both guessing.

**Silencing validation errors.** Catching them and substituting defaults means the caller sent something wrong and will never find out.

## Next

That is the foundation: routing, the three sources of input, the shape of the response, and what happens when something does not fit. The next tier goes deeper into the request &mdash; methods, headers, cookies, forms, files, status codes, error handling, and splitting an app into routers.

## What the tier covered

Seven modules: what the framework actually is, how a function becomes a route, the three places input comes from, what the response declares, and what happens when something does not fit.

That is enough to build a real API. Everything past it is refinement &mdash; better organisation, more of the request, dependencies, the runtime, and the practices that keep an application maintainable once it has more than a handful of endpoints.

The next tier goes deeper into the request itself: the methods and what each promises, headers and cookies, form data and file uploads, status codes, error handling, and splitting a growing app into routers before it becomes one very long file.

## One habit to take away

Read the errors your own API produces before anybody else has to.

Send a deliberately broken request to each endpoint and look at what comes back. Is the message something a caller could act on? Does the `loc` point at the right thing? Is a cross-field rule producing an error with nowhere to display it? Is anything sensitive echoed back in `input`?

It takes minutes per endpoint and it is the only way to see your API the way somebody failing to use it does. Almost every API has at least one error that makes perfect sense to its author and none at all to anyone else.

## The shape of a good failure

Every rejection an API produces answers three questions, and the default envelope answers all three: what was wrong, where it was, and what was received.

Most hand-rolled validation answers one. That gap is the argument for letting the framework produce these rather than writing checks in handlers &mdash; not that the code is shorter, though it is, but that the caller is told enough to fix the problem without asking anyone.

Whatever envelope you settle on, keep those three. A friendlier message that drops the location has made things worse.

## A closing thought

Errors are the part of an API that gets the least design attention and the most use by anyone struggling with it.

A caller who succeeds first time never reads one. A caller who does not is reading nothing else, and what they find there decides whether they work it out in a minute or give up and open a ticket. It is worth twenty lines.
''',
    [
        {"q": "What is the first element of `loc` in a FastAPI validation error?",
         "options": ["The field name", "The part of the request - path, query, header, cookie or body", "The model name", "The status code"],
         "answer": 1,
         "why": "It tells the caller where to look. Code that reads `loc[0]` as a field name is wrong here in a way it was not in plain Pydantic."},
        {"q": "A request for `/modules/99` is well-formed but no module 99 exists. What should it return?",
         "options": ["422", "404", "400", "409"],
         "answer": 1,
         "why": "The request fitted the declared shape perfectly. Nothing with that id exists, which is a fact about the world - so your code raises HTTPException(404)."},
        {"q": "Why assert on `type` rather than `msg` in a test?",
         "options": ["type is shorter", "Messages are prose and get reworded between releases", "msg is always empty", "No difference"],
         "answer": 1,
         "why": "Type codes are stable identifiers. Matching on prose makes the suite fail on a wording change, which teaches a team to distrust it."},
        {"q": "How do you return a different error envelope for validation failures?",
         "options": ["Change the model", "An `@app.exception_handler(RequestValidationError)`", "A middleware", "You cannot"],
         "answer": 1,
         "why": "The handler receives the exception and returns whatever JSON shape your clients expect - keeping the 422 status, and logging the original errors for diagnosis."},
    ],
)
