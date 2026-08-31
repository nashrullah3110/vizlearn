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


# ---------------------------------------------------------------------------
# 8. HTTP methods and routing
# ---------------------------------------------------------------------------
topic(
    "http_methods_and_routing",
    "HTTP Methods and Routing",
    "The Request",
    "What each verb promises, why idempotency is worth caring about, and how the "
    "router decides which handler runs.",
    _svg(_box(12, 16, 60, 18, S) + _txt(42, 29, "GET  safe", M, 7) +
         _box(12, 38, 60, 18, S) + _txt(42, 51, "POST  once", M, 7) +
         _box(88, 16, 60, 18, S, A) + _txt(118, 29, "PUT  again", A, 7) +
         _box(88, 38, 60, 18, S, A) + _txt(118, 51, "DELETE  again", A, 7)),
    [
        ("One path, several methods",
         "The same URL can carry a different handler per verb. That is the shape of "
         "a resource: one name, several things you can do to it.",
         '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
DB = {1: {"id": 1, "title": "Vectors"}}

class ModuleIn(BaseModel):
    title: str

@app.get("/modules/{i}")
def read(i: int):
    return DB.get(i, {"error": "missing"})

@app.put("/modules/{i}")
def replace(i: int, body: ModuleIn):
    DB[i] = {"id": i, "title": body.title}
    return DB[i]

@app.delete("/modules/{i}", status_code=204)
def remove(i: int):
    DB.pop(i, None)
    return None

c = TestClient(app)
print("get   :", c.get("/modules/1").json())
print("put   :", c.put("/modules/1", json={"title": "Norms"}).json())
print("delete:", c.delete("/modules/1").status_code)
print("get   :", c.get("/modules/1").json())'''),

        ("The wrong method is a 405",
         "A path that matches a route registered for another verb gives 405, not "
         "404. The difference tells you the URL was right.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/modules")
def read():
    return []

c = TestClient(app)
print("GET    :", c.get("/modules").status_code)
print("POST   :", c.post("/modules", json={}).status_code, "<- 405, path exists")
print("GET /x :", c.get("/nope").status_code, "<- 404, path does not")
print()
print("405 means: right URL, wrong verb. Worth distinguishing when debugging.")'''),

        ("Idempotency, demonstrated",
         "Sending the same request twice should mean something different for POST "
         "than for PUT. Here is that difference, counted.",
         '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
STORE = {}
NEXT = {"id": 1}

class ModuleIn(BaseModel):
    title: str

@app.post("/modules", status_code=201)
def create(body: ModuleIn):
    i = NEXT["id"]; NEXT["id"] += 1
    STORE[i] = body.title
    return {"id": i}

@app.put("/modules/{i}")
def replace(i: int, body: ModuleIn):
    STORE[i] = body.title
    return {"id": i}

c = TestClient(app)
c.post("/modules", json={"title": "Vectors"})
c.post("/modules", json={"title": "Vectors"})
print("after two POSTs:", STORE, "<- two records")

STORE.clear()
c.put("/modules/9", json={"title": "Norms"})
c.put("/modules/9", json={"title": "Norms"})
print("after two PUTs :", STORE, "<- one record")'''),

        ("Registration order, and how to inspect it",
         "The router walks its table in order and takes the first match. You can "
         "print that table, which settles most routing arguments.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/modules/latest")
def latest(): return {"route": "latest"}

@app.get("/modules/{i}")
def by_id(i: int): return {"route": "by_id", "i": i}

@app.post("/modules")
def create(): return {"route": "create"}

print("the table, in match order:")
for r in app.routes:
    methods = getattr(r, "methods", None)
    if methods:
        print("  %-8s %s" % (",".join(sorted(methods)), r.path))

c = TestClient(app)
print()
print("/modules/latest ->", c.get("/modules/latest").json())
print("/modules/7      ->", c.get("/modules/7").json())'''),

        ("Several methods on one function",
         "<code>api_route</code> registers one handler for a list of verbs, and "
         "<code>Request.method</code> tells you which arrived.",
         '''from fastapi import FastAPI, Request

app = FastAPI()

@app.api_route("/ping", methods=["GET", "HEAD"])
def ping(request: Request):
    return {"method": request.method}

c = TestClient(app)
print("GET  :", c.get("/ping").json())
print("HEAD :", c.request("HEAD", "/ping").status_code)
print()
print("Useful for health checks, and rarely the right tool otherwise -")
print("two verbs usually want two functions.")'''),

        ("A resource, end to end",
         "The five verbs on one collection, with the status codes each should "
         "return. This is the shape most CRUD endpoints converge on.",
         '''from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
DB, NEXT = {}, {"id": 1}

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)

class ModuleOut(ModuleIn):
    id: int

@app.get("/modules", response_model=list[ModuleOut])
def list_all():
    return list(DB.values())

@app.post("/modules", response_model=ModuleOut, status_code=201)
def create(body: ModuleIn):
    i = NEXT["id"]; NEXT["id"] += 1
    DB[i] = {"id": i, **body.model_dump()}
    return DB[i]

@app.get("/modules/{i}", response_model=ModuleOut)
def read(i: int):
    if i not in DB:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Module not found")
    return DB[i]

@app.delete("/modules/{i}", status_code=204)
def remove(i: int):
    if i not in DB:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Module not found")
    del DB[i]
    return None

c = TestClient(app)
print("create :", c.post("/modules", json={"title": "Vectors"}).status_code)
print("list   :", c.get("/modules").json())
print("read   :", c.get("/modules/1").json())
print("missing:", c.get("/modules/99").status_code)
print("delete :", c.delete("/modules/1").status_code)
print("list   :", c.get("/modules").json())'''),
    ],
    [
        "One path can carry a handler per verb. That is what a resource is: one name, several operations.",
        "A known path with an unregistered verb gives <strong>405</strong>, not 404. The distinction tells you the URL was right.",
        "<strong>GET</strong> is safe &mdash; it must not change anything, because browsers prefetch and proxies cache.",
        "<strong>PUT</strong> and <strong>DELETE</strong> are idempotent: repeating them leaves the same result, so a client can safely retry after a timeout. <strong>POST</strong> is not.",
        "Routes match in registration order, first match wins. <code>app.routes</code> prints the table when a route is not behaving.",
        "<code>api_route(methods=[...])</code> registers one function for several verbs. Useful for health checks; two verbs usually deserve two functions.",
    ],
    '''
title: HTTP Methods and Routing
intro: What each verb promises, and how the router decides which handler runs.
## A resource is one name and several operations

The same path with different methods is the central idea of an HTTP API. `/modules/7` names a thing; `GET`, `PUT` and `DELETE` are what you can do to it.

FastAPI gives you a decorator per verb, and registering several against one path is normal rather than a special case.

## The promises each verb makes

These are not conventions you may ignore. Browsers, proxies, CDNs, load balancers and HTTP client libraries all act on them, and breaking one produces behaviour you did not write.

**GET is safe.** It must not change anything. Browsers prefetch links, proxies cache responses, monitoring replays requests, and a "click here to delete" link behind a GET will eventually be followed by something that was not a person.

**POST is not idempotent.** Sending it twice does it twice. That is correct for creating, and it is why a client that times out mid-POST genuinely does not know whether it succeeded.

**PUT is idempotent.** It replaces a resource at a known URL, so repeating it leaves the same state. A client can retry it safely.

**DELETE is idempotent.** Deleting twice leaves the thing deleted. The second call returning 404 is acceptable; many APIs return 204 both times, which is friendlier to a retrying client.

**PATCH is not necessarily idempotent.** "Set the title to X" is; "increment the counter" is not.

That retry property is the practical payoff. It is what lets a client library automatically retry a failed PUT and refuse to retry a POST, without knowing anything about your application.

## 404 versus 405

A path nothing matched is a 404. A path that matched a route registered for a different verb is a **405 Method Not Allowed**.

The distinction is genuinely useful when debugging: a 405 means the URL is right and the method is wrong, which is usually a typo in the decorator or a client sending POST where PUT was meant. A 404 means the path never matched at all, which is a different search.

## Order, and inspecting it

Routes match in registration order and the first match wins &mdash; the rule from the first tier, and the reason a fixed path must be declared before a variable one that would also match.

`app.routes` is worth knowing about, because it settles arguments. Printing the table shows exactly what the router will try and in what order, which is faster than reasoning about it.

Routes registered through an `APIRouter` appear in the order the routers were included, which becomes relevant once an app is split up &mdash; a catch-all in an early router can shadow a specific route in a later one.

## One function, several verbs

`api_route` takes a list of methods:

```python
@app.api_route("/ping", methods=["GET", "HEAD"])
```

The honest use is a health check, where GET and HEAD should behave identically. Beyond that it is usually the wrong tool: two verbs mean two different operations with two different meanings, and one function containing `if request.method == "POST"` is two functions that have not been separated yet.

## Designing the set

Most collections end up with five endpoints, and there is little value in being creative about them.

`GET /modules` lists. `POST /modules` creates and returns 201. `GET /modules/{id}` reads or 404s. `PUT` or `PATCH /modules/{id}` updates. `DELETE /modules/{id}` removes and returns 204.

The temptation is to add verbs to paths for anything that does not fit &mdash; `/modules/{id}/publish`, `/modules/search`. Sometimes that is right: an action that is not a create, read, update or delete genuinely needs a name, and `POST /modules/{id}/publish` is clearer than inventing a field whose mutation has a side effect.

What to avoid is the halfway house: `POST /getModules`, or `GET /modules/delete/{id}`. The first duplicates what the method already says; the second puts a destructive action behind a safe verb, which is the one mistake in this module with real consequences.

## Trailing slashes, once more

`/modules` and `/modules/` are different paths, and FastAPI redirects between them with a 307.

That is mostly invisible. Where it bites is a POST: a 307 preserves the method and body in theory, and some clients drop the body in practice, producing a request that arrives empty for no reason the caller can see. Pick one convention across your API and hold it.


## Mistakes people make

**A mutating GET.** The one with real consequences. Browsers prefetch, proxies cache, monitoring replays, and link scanners follow. A "delete" behind a GET will eventually run without a person involved.

**Using POST for everything.** It works, and it throws away idempotency. A client that times out on a PUT can safely retry; on a POST it genuinely cannot know whether the write landed. Choosing the verb correctly gives every HTTP library in the world useful information for free.

**Verbs in paths.** `POST /createModule` duplicates what the method already says, and `GET /modules/delete/7` puts a destructive action behind a safe verb.

**Assuming 404 means the route is wrong.** A 405 means the path matched and the method did not - usually a typo in the decorator or a client using POST where PUT was meant.

**Registering a variable route before a fixed one.** Still the most common routing bug, and across routers it is harder to see because the two live in different files.

**Inconsistent trailing slashes.** `/modules` and `/modules/` differ, and the 307 between them loses the body in some clients - producing a POST that arrives empty for no visible reason.

## Idempotency in practice

The property is worth one more paragraph because it is the one people skip.

A network is unreliable in a specific way: a request can succeed while the response is lost. The client sees a timeout and has no idea whether the write happened.

For a PUT or DELETE that does not matter - retry, and the end state is the same. For a POST it matters a great deal, and the standard answer is an idempotency key: the client generates one, sends it as a header, and the server records it alongside the result so a repeat returns the original response instead of creating a second record.

Payment APIs all do this, for obvious reasons. Most other APIs should and do not, and it is much easier to add before the duplicates appear than after.


## Designing a URL space

Beyond individual routes, a few decisions shape how an API feels to use.

**Nouns for resources, and plural.** `/modules`, not `/module` or `/getModules`. The method supplies the verb.

**Nest only for ownership.** `/modules/{id}/lessons` is right when a lesson belongs to exactly one module and has no independent identity. When it does have one, `/lessons/{id}` alongside is kinder - deep nesting forces callers to know a parent id they may not have.

**Actions that are not CRUD get a sub-resource.** `POST /modules/{id}/publish` is clearer than inventing a field whose mutation has side effects. Keep them few; an API that is mostly actions is an RPC interface wearing REST's clothes, and would be more honest as one.

**Filters go in the query string.** `/modules?track=maths` narrows a set. `/tracks/maths/modules` claims a module is reachable only through one track.

**Be consistent about case and separators.** Lower case, hyphens where a word break is needed. Paths are case-sensitive in the standard and inconsistently handled in practice, and consistency removes a class of bug that only appears on somebody else's server.

## What the router does not do

Two things worth knowing are absent.

**No automatic redirect between methods.** A GET to a POST-only route is a 405, not a redirect to somewhere sensible.

**No wildcard fallback by default.** An unmatched path is a 404 from the router with a generic body. If you want a catch-all - to serve a single-page app, say - you register one, and it must come last or it shadows everything after it.

That last point is the ordering rule at its most severe: a catch-all in an early router makes every route in every later router unreachable, which is a confusing morning.

## A closing thought

The verbs are the oldest and best-specified part of an HTTP API, and the part most often treated as arbitrary.

Choosing them correctly is not pedantry. It is what lets a client library retry safely, a proxy cache correctly, a monitoring system distinguish a failure from a rejection, and a newcomer guess what an endpoint does before reading its documentation.

None of that requires anything from you except using the verb that matches what the endpoint actually does - which is information you already have.


## The set worth memorising

Five endpoints per collection, and there is little value in deviating.

`GET /things` lists, with filters in the query string and a capped limit. `POST /things` creates, returns 201, and is not idempotent. `GET /things/{id}` reads or 404s. `PUT` or `PATCH /things/{id}` updates - the first replacing, the second partial. `DELETE /things/{id}` removes and returns 204.

Anything that does not fit becomes a sub-resource with a name: `POST /things/{id}/publish`. Keep those few. An API that is mostly named actions is an RPC interface, and would be clearer written as one than disguised as REST.

## Summary

One path, a handler per verb. GET is safe and must change nothing. PUT and DELETE are idempotent, so a client can retry them after a timeout; POST is not, which is why idempotency keys exist.

A known path with an unregistered method is 405, not 404, and the difference tells you the URL was right.

Routes match in registration order and, across routers, in inclusion order. `app.routes` prints the table when something is not behaving.

And design the URL space once: plural nouns, shallow nesting, filters in the query string, and no verbs in paths.

## Next

Headers and cookies come next - the parts of a request that describe the exchange rather than the resource - followed by the two body formats a browser form actually sends, the status codes that report what happened, the error handling that produces them, and the structure that keeps all of it navigable once there is more than one resource.

## One more on safety

The safe-method rule deserves restating because it is the only item here whose violation causes real damage rather than inconvenience.

"Safe" does not mean "harmless to call once". It means the caller has not requested a change, so anything may call it, any number of times, without asking. Link previews in chat applications fetch URLs. Antivirus scanners fetch URLs. Browsers prefetch on hover. Corporate proxies fetch to inspect.

Every one of those will eventually hit a destructive GET, and the resulting incident is difficult to explain because nobody clicked anything. Putting the action behind POST or DELETE removes the entire class.
''',
    [
        {"q": "A GET request is prefetched by a browser and your handler deletes something. Whose bug is it?",
         "options": ["The browser's", "Yours - GET must be safe", "Nobody's", "The proxy's"],
         "answer": 1,
         "why": "Browsers prefetch, proxies cache and monitoring replays, all on the assumption that GET changes nothing. A destructive GET will eventually be called by something that was not a person."},
        {"q": "What does a 405 tell you that a 404 does not?",
         "options": ["Nothing", "The path matched a route, but not for that method", "The server is down", "The body was invalid"],
         "answer": 1,
         "why": "405 means the URL is right and the verb is wrong - usually a typo in the decorator or a client using the wrong method. A 404 means nothing matched at all."},
        {"q": "Why can a client safely retry a failed PUT but not a failed POST?",
         "options": ["PUT is faster", "PUT is idempotent - repeating it leaves the same state", "POST has no body", "It cannot"],
         "answer": 1,
         "why": "A repeated PUT replaces the same resource with the same content. A repeated POST creates a second record, which is why a timed-out POST leaves a client genuinely uncertain."},
        {"q": "Where do routes registered on an APIRouter sit in match order?",
         "options": ["Always first", "In the order the routers were included", "Alphabetically", "Always last"],
         "answer": 1,
         "why": "Inclusion order determines match order, so a catch-all in an early router can shadow a more specific route in a later one."},
    ],
)


# ---------------------------------------------------------------------------
# 9. Headers and cookies
# ---------------------------------------------------------------------------
topic(
    "headers_and_cookies",
    "Headers and Cookies",
    "The Request",
    "The parts of a request that are neither path, query nor body - and what each "
    "is properly for.",
    _svg(_box(14, 18, 132, 18, S) + _txt(80, 31, "X-Token: abc", M, 8) +
         _box(14, 40, 132, 18, S) + _txt(80, 53, "Cookie: session=xyz", M, 8) +
         _arrow(80, 62, 80, 72) + _txt(80, 84, "declared as parameters", A, 8)),
    [
        ("Header() reads one header",
         "Underscores in the parameter name become hyphens automatically, because "
         "<code>x-token</code> is not a valid Python identifier.",
         '''from typing import Optional
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/whoami")
def whoami(x_token: Optional[str] = Header(default=None),
           user_agent: Optional[str] = Header(default=None)):
    return {"x_token": x_token, "user_agent": user_agent}

c = TestClient(app)
print("none    :", c.get("/whoami").json())
print("supplied:", c.request("GET", "/whoami", headers={
    "x-token": "abc123", "user-agent": "vizlearn-test/1.0"}).json())
print()
print("x_token became the header x-token, with no configuration.")'''),

        ("Header names are case-insensitive",
         "HTTP says so, and the client normalises them. Your parameter matches "
         "whatever case arrived.",
         '''from typing import Optional
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/h")
def h(x_token: Optional[str] = Header(default=None)):
    return {"token": x_token}

c = TestClient(app)
for name in ["x-token", "X-Token", "X-TOKEN"]:
    print("%-9s ->" % name, c.request("GET", "/h", headers={name: "abc"}).json())'''),

        ("Required headers, and the 422",
         "A header with no default is required, and its failure reports "
         "<code>header</code> as the source.",
         '''from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/secure")
def secure(x_api_key: str = Header()):
    return {"key_len": len(x_api_key)}

c = TestClient(app)
print("with key:", c.request("GET", "/secure", headers={"x-api-key": "k-123"}).json())

r = c.get("/secure")
err = r.json()["detail"][0]
print()
print("without :", r.status_code)
print("loc     :", err["loc"])
print("type    :", err["type"])'''),

        ("Cookies are read the same way",
         "<code>Cookie()</code> takes one by name. It is a header underneath, parsed "
         "for you.",
         '''from typing import Optional
from fastapi import FastAPI, Cookie

app = FastAPI()

@app.get("/session")
def session(session_id: Optional[str] = Cookie(default=None),
            theme: Optional[str] = Cookie(default="light")):
    return {"session_id": session_id, "theme": theme}

c = TestClient(app)
print("none :", c.get("/session").json())
print("some :", c.request("GET", "/session",
                          headers={"cookie": "session_id=abc; theme=dark"}).json())'''),

        ("Setting headers and cookies on the way out",
         "Declare a <code>Response</code> parameter and FastAPI hands you the one it "
         "is about to send.",
         '''from fastapi import FastAPI, Response

app = FastAPI()

@app.post("/login")
def login(response: Response):
    response.set_cookie("session_id", "abc123", httponly=True, samesite="lax")
    response.headers["X-Request-Id"] = "req-42"
    return {"ok": True}

c = TestClient(app)
r = c.post("/login")
print("body       :", r.json())
print("x-request-id:", r.headers.get("x-request-id"))
print("set-cookie :", r.headers.get("set-cookie"))
print()
print("httponly keeps JavaScript away from it; samesite limits cross-site sending.")'''),

        ("Validating a header like anything else",
         "<code>Header()</code> carries the same constraints as <code>Query()</code>, "
         "so a malformed token fails at the door.",
         '''from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/v")
def v(x_api_key: str = Header(min_length=8, pattern=r"^k-[a-z0-9]+$",
                              description="Issued in the dashboard.")):
    return {"ok": True}

c = TestClient(app)
print("good :", c.request("GET", "/v", headers={"x-api-key": "k-abc123"}).status_code)
for bad in ["k-ab", "nope-abc123"]:
    r = c.request("GET", "/v", headers={"x-api-key": bad})
    print("%-12s %s %s" % (bad, r.status_code, r.json()["detail"][0]["type"]))

print()
print("documented as:", app.openapi()["paths"]["/v"]["get"]["parameters"][0]["name"])'''),
    ],
    [
        "<code>Header()</code> reads one header. Underscores in the parameter name become hyphens, because <code>x-token</code> is not a valid identifier.",
        "Header names are case-insensitive per HTTP, so the case a client sends does not matter.",
        "A header with no default is required, and its 422 carries <code>loc[0] == \"header\"</code>.",
        "<code>Cookie()</code> reads one cookie by name &mdash; a header underneath, parsed for you.",
        "Declaring a <code>Response</code> parameter lets you set outgoing headers and cookies without returning a Response object.",
        "Use <code>httponly=True</code> for a session cookie so page scripts cannot read it, and set <code>samesite</code> deliberately.",
    ],
    '''
title: Headers and Cookies
intro: The parts of a request that are neither path, query nor body, and what each is properly for.

## Reading a header

```python
def whoami(x_token: str = Header(default=None)):
```

FastAPI converts underscores to hyphens, so `x_token` reads the `x-token` header. That conversion exists because most header names contain hyphens and none of them are valid Python identifiers.

If you need the literal name &mdash; a header that genuinely contains an underscore &mdash; `Header(convert_underscores=False)` turns it off.

Header names are case-insensitive in HTTP, and the framework normalises them, so a client sending `X-Token`, `x-token` or `X-TOKEN` all reach the same parameter. That is worth knowing mainly so you do not write code trying to handle the variants.

Everything from the query-parameter module applies: a default makes it optional, no default makes it required, and `Header()` carries the same constraints and metadata, which appear in the schema.

## What headers are for

Headers carry metadata about the request rather than the request's subject.

Authentication (`Authorization`), content negotiation (`Accept`, `Content-Type`), caching (`If-None-Match`), tracing (`X-Request-Id`), and client identification (`User-Agent`) all belong here.

What does not belong is data. A filter, an identifier, a search term &mdash; those are query parameters or a body. A header is invisible in a URL, so anything in one cannot be bookmarked, linked or shared, and callers will not think to look for it.

The `X-` prefix for custom headers was formally deprecated years ago and remains near-universal in practice. Either convention is fine; consistency matters more than which.

## Cookies

`Cookie()` reads one by name. Underneath it is the `Cookie` header, parsed into pairs for you.

Cookies are worth being careful with, because they are sent automatically by browsers on every matching request &mdash; which is what makes them convenient for sessions and what makes them a CSRF vector.

Three flags matter when setting one:

**`httponly=True`** stops page JavaScript reading it. For a session identifier this is close to mandatory; without it, any script that gets injected can read the session.

**`samesite`** controls whether the browser sends it on cross-site requests. `"lax"` is a reasonable default and blocks the most common CSRF shapes; `"strict"` is safer and breaks arriving from an external link; `"none"` requires `secure=True`.

**`secure=True`** sends it only over HTTPS. In production it should always be set.

For an API consumed by a separate front end, tokens in an `Authorization` header are usually the simpler choice, because they are not sent automatically and so CSRF does not arise. Cookies earn their place when the browser is the client and you want the browser's session handling.

## Setting things on the way out

Declaring a `Response` parameter gives you the response object FastAPI is about to send:

```python
def login(response: Response):
    response.set_cookie("session_id", "abc", httponly=True)
    response.headers["X-Request-Id"] = "req-42"
    return {"ok": True}
```

You still return your normal value, and the response model still applies. That is the useful part &mdash; you get header control without giving up serialisation and documentation the way returning a `Response` object does.

## Auth belongs in a dependency

Reading an `Authorization` header in every handler that needs it works and does not scale. The same four lines end up in thirty functions, and the thirty-first forgets them.

That is what dependencies are for, and they are the next tier. A dependency reads the header, validates the token, raises 401 if it is wrong, and returns the user &mdash; and every endpoint that needs authentication declares one parameter.

Worth knowing now so you do not build the habit of doing it by hand.

## What not to do

**Do not put secrets in a URL.** They end up in browser history, server logs, proxy logs and `Referer` headers. That is the argument for an `Authorization` header over an `api_key` query parameter, and it is a strong one.

**Do not trust a client-supplied header for identity.** `X-User-Id` from a caller is a claim, not a fact. Behind a trusted proxy that sets it, it is a fact &mdash; but only if you have confirmed the proxy strips whatever the client sent.

**Do not log headers indiscriminately.** `Authorization` and `Cookie` are exactly the two you least want in a log file, and they are in every request.


## Mistakes people make

**Putting data in a header.** A filter or an identifier in a header cannot be bookmarked, linked or shared, and no caller will think to look for it. Headers carry metadata about the request; the URL and body carry its subject.

**Trusting a client-supplied identity header.** `X-User-Id` from a caller is a claim. It is a fact only behind a proxy that sets it *and* strips whatever the client sent - and you have to have checked the second half.

**A secret in a query parameter.** It lands in browser history, server logs, proxy logs and `Referer` headers. That is the argument for `Authorization` over `?api_key=`, and it is a strong one.

**Logging headers wholesale.** `Authorization` and `Cookie` are the two you least want persisted, and they are in every request.

**A session cookie without `httponly`.** Any injected script can then read the session.

**Reading auth headers in every handler.** The same four lines in thirty functions, and the thirty-first forgets them. That is what a dependency is for.

## Cookies or tokens

Worth being explicit, because it is a decision every API makes once.

**Cookies** are sent automatically by the browser on every matching request. Convenient for a server-rendered app, and the reason CSRF exists - which `samesite` mitigates and a token approach avoids entirely.

**Bearer tokens** in an `Authorization` header are not sent automatically, so CSRF does not arise. The client has to store the token somewhere, and `localStorage` is readable by scripts, which trades one risk for another.

For an API consumed by a separate front end, tokens are usually simpler. For a browser-first application where the server manages the session, cookies with `httponly`, `secure` and `samesite` set are a good answer and a well-understood one.

Neither is universally right. What is universally wrong is choosing without noticing there was a choice.


## Content negotiation, briefly

Two headers decide what format a request and response are in, and FastAPI handles both mostly invisibly.

`Content-Type` on the request says what the body is. It is how the framework knows whether to parse JSON or a form, which is why declaring a model and a `Form()` field together is a contradiction - they imply different values for one header.

`Accept` on the request says what the client would like back. FastAPI does not negotiate on it by default: an endpoint returns JSON regardless. If you need to serve more than one representation, you read the header yourself and return a different response class.

That is a deliberate simplification rather than an omission. Genuine content negotiation is rarer than it looks, and an API that always returns JSON is easier to consume than one whose response shape depends on a header the caller may not have set.

## Caching headers

Worth knowing they exist, because a small amount of effort here removes a large amount of traffic.

`ETag` and `If-None-Match` let a client ask "has this changed?" and receive a 304 with no body when it has not. `Cache-Control` tells intermediaries how long a response may be reused.

Neither is automatic. Both are set through a `Response` parameter, and both only make sense on `GET` - which is another reason the safe-method rule matters, since a cached response to a mutating request would be a genuine problem.

For a read-heavy API serving data that changes rarely, an ETag on the expensive endpoints is often the cheapest performance work available.

## Trusting the proxy

One more note, because it catches people deploying for the first time.

Behind a load balancer or reverse proxy, the client address your app sees is the proxy's, not the caller's. The real one arrives in `X-Forwarded-For`, and the scheme in `X-Forwarded-Proto`.

Those are headers like any other, which means a direct caller can set them to anything. They are trustworthy only if the proxy overwrites rather than appends, and only if nothing can reach your app without going through it.

Getting that wrong is how rate limiting by IP becomes rate limiting by whatever the attacker chose to send.

## Next

The two content types a browser form actually sends, which are neither JSON nor query strings: form data and file uploads.


## A note on CORS

Headers are also where the browser's cross-origin rules live, and it is worth knowing where the boundary is.

When a page on one origin calls an API on another, the browser decides whether the response may be read. That decision is made from response headers - `Access-Control-Allow-Origin` and its relatives - and for anything beyond a simple request the browser first sends an `OPTIONS` preflight asking what is permitted.

The important part: CORS is enforced *by the browser*, for the browser's benefit. It is not a security control on your server. A non-browser client ignores it entirely, so a permissive CORS policy does not expose an API that was otherwise protected, and a strict one does not protect an API that has no authentication.

FastAPI configures this with `CORSMiddleware`, which is the middleware module's subject. The habit to avoid is reaching for `allow_origins=["*"]` because something did not work - it usually does make the error go away, and it also means any page anywhere can call your API with whatever credentials the browser holds.


## Where headers fit in the request

It helps to hold the four sources in one picture, now that all of them have appeared.

The **path** identifies a resource and is always required. The **query string** describes a view of it and is usually optional. The **body** carries the subject of a write. **Headers and cookies** carry everything about the exchange that is not about the resource at all - who is asking, in what format, on behalf of which session, with what caching state.

FastAPI reads all four from one function signature, deciding by where a name appears and what marks it. That uniformity is the framework's main contribution, and it is why a handler taking a path parameter, two query filters, a body and an API key still reads as an ordinary Python function.

The corollary is that putting a value in the wrong place is easy and produces a working endpoint that is awkward to use. An identifier in a header, a session token in the query string, a filter in the body of a GET - each works, and each will confuse whoever integrates with it.

## Summary

`Header()` reads one header, converting underscores to hyphens. `Cookie()` reads one cookie. Both behave like query parameters otherwise: a default makes them optional, constraints and descriptions reach the schema, and a failure reports `header` or `cookie` as the source.

Headers carry metadata about a request - authentication, content negotiation, caching, tracing. Data belongs in the URL or the body, where it can be seen and shared.

Set outgoing headers and cookies through a `Response` parameter, which keeps your response model. Use `httponly`, `secure` and `samesite` on anything that identifies a session, and move authentication into a dependency before the fourth endpoint needs it.
''',
    [
        {"q": "Why does `x_token: str = Header()` read the `x-token` header?",
         "options": ["Coincidence", "Underscores are converted to hyphens, since header names are not valid identifiers", "It reads `x_token` literally", "Only with a config flag"],
         "answer": 1,
         "why": "Most header names contain hyphens and none are valid Python identifiers, so the conversion is automatic. `convert_underscores=False` turns it off."},
        {"q": "What belongs in a header rather than a query parameter?",
         "options": ["A search term", "A filter", "Metadata about the request, like auth or content negotiation", "An identifier"],
         "answer": 2,
         "why": "Headers carry metadata about the request. Data belongs where it can be seen, bookmarked and linked - the URL or the body."},
        {"q": "Why set `httponly=True` on a session cookie?",
         "options": ["It is faster", "Page JavaScript cannot read it, so an injected script cannot steal the session", "It encrypts the value", "It stops CSRF"],
         "answer": 1,
         "why": "It keeps the value out of reach of scripts. CSRF is a different problem, addressed by `samesite`."},
        {"q": "Where should reading an `Authorization` header live?",
         "options": ["In every handler", "In a dependency", "In middleware only", "In the model"],
         "answer": 1,
         "why": "Doing it per handler means the same four lines in thirty functions and the thirty-first forgetting. A dependency does it once and each endpoint declares one parameter."},
    ],
)


# ---------------------------------------------------------------------------
# 10. Form data and file uploads
# ---------------------------------------------------------------------------
topic(
    "form_data_and_files",
    "Form Data and File Uploads",
    "The Request",
    "What a browser form actually sends, and why it is neither JSON nor a query "
    "string.",
    _svg(_box(12, 20, 60, 22, S) + _txt(42, 35, "form fields", M, 8) +
         _box(88, 20, 60, 22, S) + _txt(118, 35, "file parts", M, 8) +
         _arrow(80, 48, 80, 58) +
         _txt(80, 74, "multipart/form-data", A, 8)),
    [
        ("Form() reads a form field",
         "A browser form posts <code>application/x-www-form-urlencoded</code>, which "
         "is not JSON. <code>Form()</code> says so explicitly.",
         '''from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login")
def login(username: str = Form(), password: str = Form()):
    return {"username": username, "password_len": len(password)}

c = TestClient(app)
r = c.post("/login", data={"username": "ada", "password": "hunter2"})
print(r.status_code, r.json())'''),

        ("Form fields validate like anything else",
         "The same constraints, the same 422 &mdash; with <code>body</code> as the "
         "source, because a form is a body.",
         '''from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/signup")
def signup(email: str = Form(pattern=r"^[^@]+@[^@]+\\.[^@]+$"),
           age: int = Form(ge=13)):
    return {"email": email, "age": age, "type": type(age).__name__}

c = TestClient(app)
print("good:", c.post("/signup",
                      data={"email": "ada@vizlearn.in", "age": 36}).json())

r = c.post("/signup", data={"email": "nope", "age": 9})
print("bad :", r.status_code)
for err in r.json()["detail"]:
    print("   ", err["loc"], err["type"])'''),

        ("Form and JSON cannot share a request",
         "One body, one content type. Declaring both a model and a Form field is a "
         "contradiction, and the error is confusing if you do not expect it.",
         '''from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()

class Body(BaseModel):
    title: str

@app.post("/json")
def as_json(body: Body):
    return {"via": "json", "title": body.title}

@app.post("/form")
def as_form(title: str = Form()):
    return {"via": "form", "title": title}

c = TestClient(app)
print(c.post("/json", json={"title": "Vectors"}).json())
print(c.post("/form", data={"title": "Vectors"}).json())
print()
print("A request carries one body. Pick the content type the client sends.")'''),

        ("Uploads arrive as UploadFile",
         "A file part gives you a filename, a content type and a file-like object "
         "&mdash; streamed to disk rather than held in memory.",
         '''from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/upload")
def upload(file: UploadFile):
    data = file.file.read()
    return {"filename": file.filename,
            "content_type": file.content_type,
            "bytes": len(data),
            "head": data[:24].decode("utf-8", "replace")}

r = TestClient(app).post("/upload", files={
    "file": ("notes.txt", b"Vectors have direction and magnitude.", "text/plain")})
print(r.status_code, r.json())'''),

        ("Files and fields together",
         "<code>multipart/form-data</code> carries both, which is what a real upload "
         "form sends.",
         '''from fastapi import FastAPI, Form, UploadFile

app = FastAPI()

@app.post("/modules/{i}/asset")
def add_asset(i: int, caption: str = Form(), file: UploadFile = None):
    return {"module": i, "caption": caption,
            "filename": file.filename if file else None,
            "bytes": len(file.file.read()) if file else 0}

r = TestClient(app).post("/modules/7/asset",
        data={"caption": "A vector diagram"},
        files={"file": ("v.svg", b"<svg/>", "image/svg+xml")})
print(r.status_code, r.json())'''),

        ("Validating an upload is your job",
         "The framework gives you a filename and a declared content type. Neither is "
         "trustworthy, and nothing checks the size.",
         '''from fastapi import FastAPI, HTTPException, UploadFile

app = FastAPI()
MAX = 32
ALLOWED = {"text/plain", "image/png"}

@app.post("/upload")
def upload(file: UploadFile):
    if file.content_type not in ALLOWED:
        raise HTTPException(415, "Unsupported type %r" % file.content_type)
    data = file.file.read(MAX + 1)
    if len(data) > MAX:
        raise HTTPException(413, "File too large (limit %d bytes)" % MAX)
    return {"filename": file.filename, "bytes": len(data)}

c = TestClient(app)
for label, spec in [
    ("ok      ", ("a.txt", b"short", "text/plain")),
    ("too big ", ("a.txt", b"x" * 100, "text/plain")),
    ("bad type", ("a.exe", b"MZ", "application/x-msdownload")),
]:
    r = c.post("/upload", files={"file": spec})
    print(label, r.status_code, r.json())'''),
    ],
    [
        "Form fields need <code>Form()</code>. Without it a plain parameter is read as a query parameter and a model as JSON.",
        "Form data and a JSON body cannot share one request &mdash; there is one body and one content type.",
        "Form and file endpoints need the <code>python-multipart</code> package installed, and FastAPI raises at startup without it.",
        "<code>UploadFile</code> gives a filename, a declared content type and a file-like object. Large files are spooled to disk rather than held in memory.",
        "Neither <code>filename</code> nor <code>content_type</code> is trustworthy &mdash; both come from the client. Never build a path from a filename.",
        "Nothing limits upload size by default. Cap it in the handler, and again in whatever sits in front of the app.",
    ],
    '''
title: Form Data and File Uploads
intro: What a browser form actually sends, and why it is neither JSON nor a query string.
## Three body formats

An HTTP request has one body, and for an API there are three ways it is commonly encoded.

**JSON** (`application/json`) is what a JavaScript client or another service sends. A Pydantic model parameter reads it.

**URL-encoded form** (`application/x-www-form-urlencoded`) is what a plain HTML `<form>` posts. It looks like a query string in the body: `username=ada&password=hunter2`.

**Multipart** (`multipart/form-data`) is what a form with a file input sends. It carries several named parts, each with its own headers, which is how a file and its metadata travel together.

FastAPI needs to be told which. A model parameter means JSON; `Form()` means one of the form encodings; `UploadFile` means a file part in a multipart body.

## Form()

```python
def login(username: str = Form(), password: str = Form()):
```

Without `Form()`, a plain `username: str` parameter would be read as a **query parameter**, and the request would fail with a confusing 422 about a missing query field while the value sits in the body.

That is the one thing to remember here. The marker is not decoration; it is what tells FastAPI where to look.

Everything else behaves as it does elsewhere: constraints, defaults, required-ness and the 422 all work the same way, with `loc[0] == "body"` because a form *is* the body.

## One body, one content type

A request cannot be both JSON and a form. Declaring a model parameter alongside a `Form()` parameter is a contradiction, and the resulting error does not always say so clearly.

Pick the encoding your client actually sends. If it is a browser form, use `Form()`. If it is JavaScript, it is almost certainly sending JSON, and a model is simpler and better documented.

A common middle case: an HTML form that you would rather receive as a model. The clean answer is to have the front end send JSON. Failing that, a dependency can assemble a model from form fields, which keeps the handler tidy.

## python-multipart

Form and file endpoints require the `python-multipart` package. Without it FastAPI raises at startup, and the message names the package rather than the endpoint &mdash; which is helpful once you know, and puzzling the first time.

It is a runtime dependency of the framework's form support rather than something FastAPI bundles, so it has to be installed explicitly.

## UploadFile

```python
def upload(file: UploadFile):
    data = file.file.read()
```

`UploadFile` gives you three things: `filename`, `content_type`, and `file`, a file-like object.

The important property is that a large upload is **spooled to disk** rather than held in memory. A `bytes` parameter would read the whole thing into RAM, which is fine for a small avatar and a denial-of-service vector for anything else. `UploadFile` is the right default.

It also offers `async` methods &mdash; `await file.read()` &mdash; for use in `async def` endpoints, so a slow upload does not block the event loop.

## What the framework does not check

This is the part worth taking seriously, because the defaults are permissive.

**Size is unlimited.** Nothing caps an upload. Check it in the handler by reading with a limit rather than reading everything and then measuring &mdash; and set a limit in whatever sits in front of the app too, since by the time your code runs the bytes have already arrived.

**`content_type` is a claim.** It comes from the client and can say anything. If the type matters, check the actual content: magic bytes for images, parsing for structured formats.

**`filename` is attacker-controlled.** It can contain `..`, absolute paths, null bytes and characters your filesystem treats specially. **Never build a path from it.** Generate your own name &mdash; a UUID &mdash; and keep the original only as metadata if you need it for display.

**The content is unexamined.** An uploaded file is arbitrary bytes. If it will be served back to browsers, serve it from a separate domain or with `Content-Disposition: attachment` and a restrictive `Content-Type`, so an HTML file cannot execute in your origin.

## Documenting them

Form and file endpoints appear in the OpenAPI document, and the interactive docs render a file picker for `UploadFile`, which makes them genuinely testable from the browser.

`Form()` takes `description` like every other parameter, and it is worth writing &mdash; a form field's name is often shorter and less obvious than a JSON key.

## When to use which

Reach for **JSON** by default. It is better documented, better validated, nests properly, and every client can produce it.

Reach for **form data** when a browser form posts directly to your API without JavaScript, or when an existing client already sends it.

Reach for **multipart** when files are involved. That is what it is for, and it is the only one of the three that carries binary content alongside fields.

For anything large, consider not uploading through your API at all: a pre-signed URL to object storage moves the bytes directly and keeps them out of your request path entirely. That is more moving parts, and it is the standard answer once files get big.


## Mistakes people make

**Forgetting `Form()`.** A plain parameter is read as a query parameter, so the request 422s about a missing query field while the value sits in the body. The marker is what tells FastAPI where to look.

**Mixing a model and form fields.** One request, one body, one content type. Declaring both is a contradiction, and the resulting error does not say so clearly.

**Missing `python-multipart`.** FastAPI raises at startup and names the package rather than the endpoint - obvious afterwards, puzzling the first time.

**Reading an upload as `bytes`.** Fine for an avatar, a denial-of-service vector for anything larger. `UploadFile` spools to disk.

**Building a path from `filename`.** It is attacker-controlled and can contain `..`, absolute paths, and characters your filesystem treats specially. Generate your own name.

**Trusting `content_type`.** It is a claim from the client. If the type matters, check the bytes.

**No size limit.** Nothing caps an upload by default, and the bytes arrive before your handler runs - so cap it in the handler *and* in whatever sits in front of the app.

## Serving uploads back

A related risk that is easy to miss.

If uploaded files are served back to browsers from your own domain, an uploaded HTML file executes in your origin - which means it can read cookies, call your API as the viewer, and generally behave as your own page.

The mitigations, in rough order of preference: serve user content from a separate domain; send `Content-Disposition: attachment` so it downloads rather than renders; and set a restrictive `Content-Type` rather than echoing the one the client claimed.

For anything at scale, uploading directly to object storage with a pre-signed URL avoids the problem and keeps the bytes out of your request path entirely.


## Getting a model out of a form

A recurring want: a browser posts a form, and you would rather work with a Pydantic model than six `Form()` parameters.

There is no built-in switch for it, because a model parameter means JSON by definition. The usual answers, in order of how much they cost:

**Have the front end send JSON.** A few lines of JavaScript, and everything downstream becomes simpler - validation, nesting, documentation and error shapes all improve.

**Build the model in the handler.** `ModuleIn(**{"title": title, "minutes": minutes})` after declaring the fields as `Form()`. Honest, and repetitive across several endpoints.

**A dependency that assembles it.** The tidy version: one function declaring the form fields and returning the model, then `module: ModuleIn = Depends(as_form)`. Handlers stay clean and the assembly lives in one place. That is the next tier's material.

What to avoid is a decorator that inspects a model and generates form parameters by reflection. Several exist, they work, and they make the endpoint's signature something a reader cannot see.

## Multiple files

`files: List[UploadFile]` accepts several parts under the same name, which is what a multi-select file input sends.

Two cautions with it. The size limit now applies to the total as well as each item, so a hundred small files can be as expensive as one large one - cap the count with `max_length` as well. And validating each file means doing the work per item, so a slow check multiplies.

For anything where the count could be large, an endpoint that accepts one file and is called repeatedly is easier to reason about, easier to retry, and gives the client better progress reporting.

## A closing thought

Uploads are the part of an API where the defaults are most permissive and the consequences most physical - disk filling, memory exhausting, files being served back and executing in your origin.

None of that is exotic, and none of it is handled for you. A size cap, a type check on the bytes rather than the claim, a generated filename, and a decision about where the file is served from cover nearly all of it.

Four small pieces of care, on the one endpoint type where their absence is genuinely dangerous.


## Where uploads should go

A last architectural note, because the default path is rarely the right one at scale.

Uploading through your API means the bytes travel into your process, through whatever sits in front of it, and often out again to storage. That consumes request capacity, occupies a worker for the duration of a slow connection, and puts a size limit on something that has no natural one.

The alternative is a pre-signed URL: your API issues a short-lived credential, the client uploads directly to object storage, and then tells your API the key. The bytes never touch your application.

It is more moving parts and it is what most systems end up doing, because the failure mode of the simple approach is a worker pool full of slow uploads.

## Summary

`Form()` marks a field as coming from a form-encoded body; without it the parameter is read from the query string. A request has one body, so form fields and a JSON model cannot coexist.

`UploadFile` gives a filename, a declared content type and a file-like object, spooled to disk rather than held in memory. Both the filename and the content type come from the client and neither can be trusted; nothing limits the size unless you do.

Prefer JSON where you have the choice, use multipart when files are involved, and for anything large consider uploading straight to object storage instead of through your API.

## Next

Status codes: which number to return when, why the class matters more than the number, and how returning 200 for everything throws away information that clients, caches and monitoring all already know how to use.

## A final note

If one thing survives this module, make it the filename rule.

Every other risk here degrades gracefully - a large upload is slow, a wrong content type is a bad thumbnail. Building a path from a client-supplied filename is the one that writes a file where you did not intend, and it is a single line to avoid.
''',
    [
        {"q": "You declare `username: str` with no marker on a POST endpoint. Where does FastAPI look?",
         "options": ["The form body", "The query string", "A header", "The JSON body"],
         "answer": 1,
         "why": "A plain parameter defaults to a query parameter. `Form()` is what tells FastAPI the value is in a form-encoded body."},
        {"q": "Why is `UploadFile` preferable to a `bytes` parameter?",
         "options": ["It is faster", "Large uploads are spooled to disk instead of held in memory", "It validates the content", "It is required"],
         "answer": 1,
         "why": "Reading a whole upload into RAM is fine for an avatar and a denial-of-service vector for anything larger."},
        {"q": "Can you safely use `file.filename` to build a save path?",
         "options": ["Yes", "No - it is attacker-controlled and can contain `..` or absolute paths", "Only for images", "Only if it is short"],
         "answer": 1,
         "why": "It comes from the client and can say anything. Generate your own name and keep the original only as display metadata."},
        {"q": "What does FastAPI do about upload size by default?",
         "options": ["Caps it at 1MB", "Nothing - it is unlimited", "Rejects over 10MB", "Streams it away"],
         "answer": 1,
         "why": "Nothing caps it. Read with a limit in the handler, and set one in whatever sits in front of the app, since the bytes arrive before your code runs."},
    ],
)


# ---------------------------------------------------------------------------
# 11. Status codes
# ---------------------------------------------------------------------------
topic(
    "status_codes",
    "Status Codes",
    "The Request",
    "Which number to return when, and why returning 200 for everything throws "
    "away something every client already understands.",
    _svg(_box(10, 20, 44, 20, S, A) + _txt(32, 34, "2xx ok", A, 8) +
         _box(58, 20, 44, 20, S) + _txt(80, 34, "4xx you", M, 8) +
         _box(106, 20, 44, 20, S) + _txt(128, 34, "5xx me", M, 8) +
         _txt(80, 62, "the class is the first thing a client reads", M, 7)),
    [
        ("The route's default, and overriding it",
         "<code>status_code</code> on the decorator sets the default. A "
         "<code>Response</code> parameter lets one call differ.",
         '''from fastapi import FastAPI, Response, status

app = FastAPI()
DB = {}

@app.put("/modules/{i}", status_code=status.HTTP_200_OK)
def upsert(i: int, response: Response):
    created = i not in DB
    DB[i] = {"id": i}
    if created:
        response.status_code = status.HTTP_201_CREATED
    return DB[i]

c = TestClient(app)
print("first  :", c.put("/modules/1").status_code, "<- created")
print("second :", c.put("/modules/1").status_code, "<- already existed")'''),

        ("204 carries nothing",
         "The one rule with teeth. Declare it and return <code>None</code>; anything "
         "else produces a malformed response.",
         '''from fastapi import FastAPI, status

app = FastAPI()
DB = {1: "Vectors"}

@app.delete("/modules/{i}", status_code=status.HTTP_204_NO_CONTENT)
def remove(i: int):
    DB.pop(i, None)
    return None

c = TestClient(app)
r = c.delete("/modules/1")
print("status      :", r.status_code)
print("body        :", repr(r.text), "<- empty, as 204 requires")
print("content-type:", r.headers.get("content-type"))'''),

        ("The named constants",
         "<code>fastapi.status</code> spells every code. Readable at the call site "
         "and autocompleted, which matters for the ones you use rarely.",
         '''from fastapi import status

pairs = [
    ("HTTP_200_OK", status.HTTP_200_OK),
    ("HTTP_201_CREATED", status.HTTP_201_CREATED),
    ("HTTP_202_ACCEPTED", status.HTTP_202_ACCEPTED),
    ("HTTP_204_NO_CONTENT", status.HTTP_204_NO_CONTENT),
    ("HTTP_400_BAD_REQUEST", status.HTTP_400_BAD_REQUEST),
    ("HTTP_401_UNAUTHORIZED", status.HTTP_401_UNAUTHORIZED),
    ("HTTP_403_FORBIDDEN", status.HTTP_403_FORBIDDEN),
    ("HTTP_404_NOT_FOUND", status.HTTP_404_NOT_FOUND),
    ("HTTP_409_CONFLICT", status.HTTP_409_CONFLICT),
    ("HTTP_422_UNPROCESSABLE_ENTITY", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("HTTP_500_INTERNAL_SERVER_ERROR", status.HTTP_500_INTERNAL_SERVER_ERROR),
]
for name, value in pairs:
    print("%-32s %d" % (name, value))'''),

        ("401 and 403 are different questions",
         "One means “I do not know who you are”, the other “I do, and no”. Clients "
         "act on the difference.",
         '''from fastapi import FastAPI, Header, HTTPException, status
from typing import Optional

app = FastAPI()
USERS = {"tok-admin": "admin", "tok-reader": "reader"}

@app.delete("/modules/{i}")
def remove(i: int, authorization: Optional[str] = Header(default=None)):
    if authorization is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sign in first",
                            headers={"WWW-Authenticate": "Bearer"})
    role = USERS.get(authorization.replace("Bearer ", ""))
    if role is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unknown token")
    if role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admins only")
    return {"deleted": i}

c = TestClient(app)
def call(tok):
    h = {"authorization": "Bearer " + tok} if tok else {}
    r = c.request("DELETE", "/modules/1", headers=h)
    return r.status_code, r.json().get("detail")

print("no token   :", call(None))
print("bad token  :", call("nope"))
print("wrong role :", call("tok-reader"))
print("admin      :", call("tok-admin"))'''),

        ("409 for a conflict with current state",
         "Not a validation failure and not a missing thing: the request was fine and "
         "the world disagrees.",
         '''from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()
SLUGS = {"vectors"}

class ModuleIn(BaseModel):
    slug: str

@app.post("/modules", status_code=201)
def create(body: ModuleIn):
    if body.slug in SLUGS:
        raise HTTPException(status.HTTP_409_CONFLICT,
                            "A module with slug %r already exists" % body.slug)
    SLUGS.add(body.slug)
    return {"slug": body.slug}

c = TestClient(app)
print("new      :", c.post("/modules", json={"slug": "norms"}).status_code)
r = c.post("/modules", json={"slug": "vectors"})
print("duplicate:", r.status_code, r.json()["detail"])
print()
print("422 would be wrong - the payload was perfectly valid.")'''),

        ("Documenting the ones that are not 200",
         "<code>responses=</code> puts the failure shapes in the schema, so a "
         "generated client knows what an error looks like.",
         '''import json
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class ModuleOut(BaseModel):
    id: int

class Problem(BaseModel):
    detail: str

@app.get("/modules/{i}", response_model=ModuleOut,
         responses={404: {"model": Problem, "description": "No such module"},
                    410: {"model": Problem, "description": "Withdrawn"}})
def read(i: int):
    if i == 410:
        raise HTTPException(status.HTTP_410_GONE, "Withdrawn")
    if i != 1:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such module")
    return {"id": 1}

c = TestClient(app)
print("ok  :", c.get("/modules/1").status_code)
print("gone:", c.get("/modules/410").status_code, c.get("/modules/410").json())
print()
print("documented responses:",
      sorted(app.openapi()["paths"]["/modules/{i}"]["get"]["responses"]))'''),
    ],
    [
        "The class is the first thing a client reads: <strong>2xx</strong> worked, <strong>4xx</strong> the caller must change something, <strong>5xx</strong> the server must.",
        "<code>status_code=</code> sets the route default; a <code>Response</code> parameter lets one call differ without returning a Response object.",
        "<strong>204</strong> must carry no body. Declare it and return <code>None</code>.",
        "<strong>401</strong> means not authenticated &mdash; who are you? <strong>403</strong> means authenticated and not allowed. Clients act on the difference.",
        "<strong>409</strong> is for a valid request that conflicts with current state, such as a duplicate. A 422 would be wrong, because nothing about the payload was malformed.",
        "<code>responses=</code> documents the non-200 shapes, which is what lets a generated client type its errors.",
    ],
    '''
title: Status Codes
intro: Which number to return when, and why 200-for-everything discards information the client already understands.
## The class matters more than the number

Before the specific code, a client reads the class.

**2xx** &mdash; it worked. **3xx** &mdash; look elsewhere. **4xx** &mdash; the caller must change something. **5xx** &mdash; the server must.

That first digit drives real behaviour in code you did not write: HTTP libraries retry 5xx and not 4xx, caches store 2xx, monitoring alerts on 5xx, and a client's error handling branches on it before looking at anything else.

Returning 200 with `{"error": "not found"}` throws all of that away. Every caller now has to parse your body to discover something the protocol had a field for, retries do the wrong thing, and your error rate looks like zero on every dashboard.

## The 2xx ones worth using

**200 OK** for a successful read or update that returns something.

**201 Created** when something new exists. Conventionally with a `Location` header pointing at it.

**202 Accepted** when you have taken the request but not finished it &mdash; a queued job. The body should say how to check on it.

**204 No Content** for a success with nothing to say. A delete, usually.

204 has the one rule with teeth: **no body at all**. Declare `status_code=204` and return `None`. Returning a value produces a malformed response, and some clients will error on it while others silently ignore the body, which is worse.

## The 4xx ones worth distinguishing

**400 Bad Request** &mdash; malformed in a way your own code determined.

**401 Unauthorized** &mdash; badly named: it means *unauthenticated*. I do not know who you are. Should carry a `WWW-Authenticate` header.

**403 Forbidden** &mdash; I know who you are, and no.

**404 Not Found** &mdash; no such thing.

**409 Conflict** &mdash; the request was fine and conflicts with current state: a duplicate, a version mismatch, an action already taken.

**410 Gone** &mdash; it existed and deliberately does not any more. Rare, and useful when you want callers to stop asking.

**422 Unprocessable Entity** &mdash; well-formed and did not fit the declared shape. FastAPI produces this automatically and you rarely raise it.

**429 Too Many Requests** &mdash; rate limited. Should carry `Retry-After`.

The 401/403 distinction is the one most often collapsed, and it is worth keeping. A client seeing 401 should prompt for credentials or refresh a token; one seeing 403 should not, because retrying with the same identity will fail again. Collapsing them makes a login loop where there should be an error message.

The 404/403 choice has a security dimension. Returning 403 for a resource that exists but is not yours confirms it exists. For anything sensitive, 404 for both is the safer answer &mdash; deliberately, and consistently, or the timing gives it away anyway.

## 422 versus 400 versus 409

These three get confused, and the rule is about *who determined the problem*.

**422** &mdash; validation determined it from your declared types and constraints. Automatic; you do not write it.

**400** &mdash; your code determined the request was malformed in a way the schema could not express.

**409** &mdash; the request was entirely valid and the current state makes it impossible.

A duplicate slug is 409, not 422: nothing about the payload was wrong, and the same payload would have succeeded a minute earlier.

## Setting them

`status_code=` on the decorator sets the route's default, and that default appears in the documentation.

For one call to differ, declare a `Response` parameter and assign to `response.status_code`. That keeps serialisation and the response model, unlike returning a `Response` object.

`HTTPException(status_code, detail)` raises one, and it accepts `headers=` &mdash; which is how you attach `WWW-Authenticate` to a 401 or `Retry-After` to a 429.

Use the `status` module rather than bare integers. `status.HTTP_409_CONFLICT` is readable and autocompleted; `409` requires the reader to know it.

## Documenting the failures

`response_model` describes the success case only. Everything else is undocumented unless you say so:

```python
responses={404: {"model": Problem, "description": "No such module"}}
```

Now the schema describes the error shape, and a generated client can type it. Without this, consumers know they will get *something* on failure and have to discover what by causing one.

Worth doing for the failures a caller is expected to handle &mdash; 404 on a lookup, 409 on a create. Not worth doing for every conceivable code.

## Mistakes people make

**200 with an error body.** The one that costs most. Retries, caches, monitoring and every client's error handling branch on the status class, and a 200 tells all of them the call succeeded.

**A body on a 204.** Malformed. Some clients error, others silently ignore it, which is worse because it works until it does not.

**Collapsing 401 and 403.** A client seeing 401 re-authenticates; seeing 403 it should not. Merging them produces a login loop where there should be a message.

**422 for a missing resource.** The request was well-formed. Nothing with that id exists, which is 404.

**422 for a duplicate.** The payload was valid and would have worked a minute earlier. That is 409.

**500 for a caller's mistake.** If they could have avoided it, it is a 4xx. A 500 should mean your code failed, and should page somebody.

**Bare integers.** `409` requires the reader to know it; `status.HTTP_409_CONFLICT` does not, and your editor completes it.

## The header a status implies

Several codes are incomplete without a header, and omitting it makes a technically-correct response practically useless.

**401** should carry `WWW-Authenticate`, naming the scheme. Without it a client knows it must authenticate and not how.

**429** should carry `Retry-After`. Without it a client's only strategy is guessing, which usually means retrying immediately and making things worse.

**405** should carry `Allow`, listing the methods that do work.

**201** conventionally carries `Location`, pointing at what was created, so a client does not have to construct the URL itself.

`HTTPException` takes `headers=` for exactly this, and it is the sort of detail that separates an API somebody enjoys using from one they merely tolerate.


## Choosing between 404 and 403

A decision with a security dimension, worth making deliberately.

Returning 403 for a resource that exists but is not yours confirms that it exists. For a sequential id that is an enumeration oracle: a caller can walk the range and learn how many records you have and which ids are real.

Returning 404 for both cases hides that, at the cost of a slightly less helpful message for a legitimate user who has genuinely lost access.

For anything sensitive - other users' data, private documents, anything under a permissions model - 404 for both is the safer default. For an internal API where enumeration tells an attacker nothing they do not already have, 403 is friendlier.

Whichever you choose, be consistent. Returning 403 sometimes and 404 other times leaks exactly the information the 404 was meant to hide, and timing differences will give it away even if the status does not.

## Redirects, briefly

The 3xx codes come up less in an API than in a website, and two are worth recognising.

**307** preserves the method and body; **308** is its permanent equivalent. These are the ones FastAPI uses for the trailing-slash redirect, and the reason it matters is that some clients still drop the body, turning a POST into an empty one.

**301** and **302** historically allowed clients to change the method to GET on redirect, which is why they are the wrong choice for anything that is not a plain read.

If an API needs to move a resource permanently, 308 with a `Location` header is the honest answer. More often the better answer is to keep the old path working and document the new one.

## The ones you will not write

Some codes exist and are produced by infrastructure rather than by your handlers.

**502**, **503** and **504** come from a proxy or load balancer when your app is unreachable, overloaded or slow. Seeing them in production means the problem is in front of your code, not in it.

**413** may be returned by a reverse proxy before a request reaches you, which is why an upload limit belongs there as well as in the handler.

Knowing which layer produces which saves time when something breaks: a 500 is yours, a 502 is not.

## A closing thought

A status code is the smallest piece of an API and the one most consumed by machines.

Every client library, cache, proxy, gateway and dashboard reads it, and none of them read your response body. Returning the accurate one costs a keyword argument and buys correct behaviour from all of them.

Returning 200 for everything costs nothing to write and moves the work onto every caller, forever.


## A short reference

**Created** something: 201, with `Location`. **Deleted** something: 204, no body. **Queued** something: 202, with a way to check. **Read** something: 200.

Caller sent nonsense: **422** if validation caught it, **400** if you did. Not signed in: **401** with `WWW-Authenticate`. Signed in, not allowed: **403** - or 404 if existence itself is sensitive. Not there: **404**. Conflicts with current state: **409**. Asking too often: **429** with `Retry-After`.

Your code failed: **500**, logged in full, returned as a generic message with an id.

## Summary

The class is what a client reads first, and it drives retries, caching and alerting in code you did not write. Returning 200 with an error body discards all of it.

201 for created, 204 for done-with-nothing-to-say and no body, 202 for accepted-but-not-finished. 401 for unauthenticated and 403 for not-allowed - they are different questions and clients act on the difference. 404 for missing, 409 for a valid request that conflicts with current state, 422 for a payload that did not fit.

Set the route default with `status_code=`, vary it through a `Response` parameter, attach the headers a status implies, and document the failures with `responses=`.

## Next

The mechanics behind most of the codes above: `HTTPException`, custom exception handlers, and the arrangement that keeps HTTP concerns out of the code that does the actual work.

## A final note

Status codes are also a form of documentation that nobody has to read.

An endpoint returning 201 with a `Location` header has told a caller that something was created and where to find it, without a sentence of prose. One returning 200 with a body they must inspect has told them nothing, and the prose now has to exist.
''',
    [
        {"q": "Why is returning 200 with an error body a problem?",
         "options": ["It is slower", "Retries, caches, monitoring and client error handling all branch on the status class", "It is invalid HTTP", "It breaks JSON"],
         "answer": 1,
         "why": "The first digit drives behaviour in code you did not write. A 200 means every caller must parse your body to learn something the protocol had a field for, and your error rate reads as zero."},
        {"q": "What must a 204 response contain?",
         "options": ["An empty object", "Nothing at all", "A message", "The deleted id"],
         "answer": 1,
         "why": "Declare `status_code=204` and return None. A body makes the response malformed - some clients error, others silently ignore it, which is worse."},
        {"q": "A signed-in reader tries an admin-only delete. Which code?",
         "options": ["401", "403", "422", "404"],
         "answer": 1,
         "why": "401 means unauthenticated - I do not know who you are. Here we do, and they are not allowed, which is 403. Collapsing the two makes clients loop on re-authentication."},
        {"q": "A create request is valid but the slug already exists. Which code?",
         "options": ["422", "400", "409", "404"],
         "answer": 2,
         "why": "Nothing about the payload was malformed - the same body would have worked a minute earlier. That is a conflict with current state, which is 409."},
    ],
)


# ---------------------------------------------------------------------------
# 12. Error handling
# ---------------------------------------------------------------------------
topic(
    "error_handling",
    "Error Handling",
    "The Request",
    "HTTPException, custom handlers, and keeping HTTP concerns out of the code "
    "that does the work.",
    _svg(_box(12, 18, 60, 22, S) + _txt(42, 33, "raise", M, 8) +
         _arrow(76, 29, 88, 29) +
         _box(92, 18, 56, 22, S, A) + _txt(120, 33, "handler", A, 8) +
         _arrow(120, 46, 120, 58) + _txt(120, 72, "JSON response", M, 8)),
    [
        ("HTTPException is the ordinary way",
         "Raise it anywhere in the call stack. FastAPI turns it into a response with "
         "your status and detail.",
         '''from fastapi import FastAPI, HTTPException, status

app = FastAPI()
DB = {1: {"id": 1, "title": "Vectors"}}

@app.get("/modules/{i}")
def read(i: int):
    if i not in DB:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Module not found")
    return DB[i]

c = TestClient(app)
print("found  :", c.get("/modules/1").json())
r = c.get("/modules/99")
print("missing:", r.status_code, r.json())
print("shape  :", list(r.json()), "<- always {'detail': ...}")'''),

        ("It can carry headers",
         "Some statuses are meaningless without one &mdash; 401 wants "
         "<code>WWW-Authenticate</code>, 429 wants <code>Retry-After</code>.",
         '''from fastapi import FastAPI, HTTPException, status

app = FastAPI()

@app.get("/limited")
def limited():
    raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS,
                        "Slow down", headers={"Retry-After": "30"})

r = TestClient(app).get("/limited")
print("status     :", r.status_code)
print("detail     :", r.json()["detail"])
print("retry-after:", r.headers.get("retry-after"))'''),

        ("Your own envelope",
         "Override the handler for <code>HTTPException</code> and every raise in the "
         "app returns the shape your clients expect.",
         '''from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(HTTPException)
async def as_problem(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"status": exc.status_code,
                           "message": exc.detail,
                           "path": request.url.path}},
        headers=getattr(exc, "headers", None) or {})

@app.get("/modules/{i}")
def read(i: int):
    raise HTTPException(status.HTTP_404_NOT_FOUND, "Module not found")

r = TestClient(app).get("/modules/9")
print(r.status_code, r.json())'''),

        ("Domain errors, mapped once",
         "Raise a plain exception from code that knows nothing about HTTP, and "
         "translate it at the edge.",
         '''from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

app = FastAPI()

class ModuleNotFound(Exception):
    def __init__(self, module_id):
        self.module_id = module_id

class SlugTaken(Exception):
    def __init__(self, slug):
        self.slug = slug

@app.exception_handler(ModuleNotFound)
async def not_found(request, exc):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={"detail": "No module %d" % exc.module_id})

@app.exception_handler(SlugTaken)
async def taken(request, exc):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"detail": "Slug %r is taken" % exc.slug})

# The service layer: no HTTP anywhere in it.
def get_module(i):
    raise ModuleNotFound(i)

def create_module(slug):
    raise SlugTaken(slug)

@app.get("/modules/{i}")
def read(i: int):
    return get_module(i)

@app.post("/modules")
def create(slug: str):
    return create_module(slug)

c = TestClient(app)
print(c.get("/modules/9").status_code, c.get("/modules/9").json())
print(c.post("/modules?slug=vectors").status_code, c.post("/modules?slug=vectors").json())'''),

        ("Catching everything else",
         "A handler for <code>Exception</code> turns an unhandled error into a clean "
         "500. Never return the traceback.",
         '''from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()
LOG = []

@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    LOG.append("%s %s -> %s: %s" % (request.method, request.url.path,
                                    type(exc).__name__, exc))
    return JSONResponse(status_code=500,
                        content={"detail": "Something went wrong",
                                 "request_id": "req-42"})

@app.get("/boom")
def boom():
    return 1 / 0

# A handler for the base Exception is special: Starlette builds the 500
# response from it and then RE-RAISES, so the server still logs the real
# failure. A test client that wants to inspect the 500 asks for that with
# raise_server_exceptions=False; here we just catch it.
try:
    r = TestClient(app).get("/boom")
    print("client sees:", r.status_code, r.json())
except ZeroDivisionError:
    print("re-raised to the server, as Starlette intends")

print()
print("our handler still ran:", LOG[0])
print()
print("The traceback stays in the log. It is an information leak in a body.")'''),

        ("Validation errors keep their own handler",
         "<code>RequestValidationError</code> is separate from "
         "<code>HTTPException</code>, so the two can have different shapes.",
         '''from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def invalid(request: Request, exc: RequestValidationError):
    fields = {}
    for err in exc.errors():
        key = ".".join(str(p) for p in err["loc"][1:]) or "_body"
        fields.setdefault(key, []).append(err["msg"])
    return JSONResponse(status_code=422, content={"invalid": fields})

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)

@app.post("/modules")
def create(body: ModuleIn):
    raise HTTPException(404, "Not found")

c = TestClient(app)
print("validation:", c.post("/modules", json={"title": "x"}).json())
print("raised    :", c.post("/modules", json={"title": "Vectors"}).json())'''),
    ],
    [
        "<code>HTTPException(status, detail)</code> can be raised anywhere in the call stack and becomes <code>{\"detail\": ...}</code>.",
        "It takes <code>headers=</code>, which some statuses require &mdash; <code>WWW-Authenticate</code> on a 401, <code>Retry-After</code> on a 429.",
        "<code>@app.exception_handler(HTTPException)</code> replaces the default envelope for every raise in the app.",
        "Custom exception classes with their own handlers keep HTTP out of the service layer: raise <code>ModuleNotFound</code>, map it to a 404 in one place.",
        "A handler for <code>Exception</code> turns an unhandled error into a clean 500. Log the traceback; never return it.",
        "That base-<code>Exception</code> handler is special: Starlette builds the response and then re-raises so the server still logs the failure. <code>TestClient(app, raise_server_exceptions=False)</code> is how a test inspects the 500.",
        "<code>RequestValidationError</code> has its own handler, separate from <code>HTTPException</code>, so validation failures and raised errors can differ.",
    ],
    '''
title: Error Handling
intro: HTTPException, custom handlers, and keeping HTTP out of the code that does the work.
## The ordinary case

```python
raise HTTPException(status.HTTP_404_NOT_FOUND, "Module not found")
```

It can be raised anywhere in the call stack, not just in the handler, and FastAPI turns it into a response with that status and `{"detail": ...}`.

Two properties are worth noticing. It is an **exception**, so it unwinds &mdash; a function five levels deep can refuse the request without every caller checking a return value. And the response shape is consistent, so every client can rely on `detail` being there.

`detail` does not have to be a string. A dict or list is serialised, which is one way to return structured errors without a custom handler.

## Headers on an error

`HTTPException` takes `headers=`, and several statuses are incomplete without one.

A **401** should carry `WWW-Authenticate` describing the scheme. A **429** should carry `Retry-After`. A **405** should carry `Allow`.

Clients act on these automatically. Omitting them makes the response technically correct and practically unhelpful.

## Replacing the envelope

If your API has an established error format, override the default handler:

```python
@app.exception_handler(HTTPException)
async def as_problem(request, exc):
    return JSONResponse(status_code=exc.status_code, content={...})
```

Every `HTTPException` in the app now returns your shape. Two things to remember: pass the status through rather than hard-coding one, and forward `exc.headers`, or the `Retry-After` you carefully set disappears.

Worth doing once, early, if you are going to do it at all. Retrofitting an envelope after clients exist is a breaking change.

## Domain errors, mapped at the edge

This is the pattern that matters most for anything beyond a small app.

Business logic should not import `fastapi`. A function that looks up a module and cannot find one should raise `ModuleNotFound`, not `HTTPException(404)` &mdash; because that function might also be called from a background job, a CLI or a test, none of which have a request to respond to.

Then map it once:

```python
@app.exception_handler(ModuleNotFound)
async def not_found(request, exc):
    return JSONResponse(status_code=404, content={"detail": ...})
```

The benefits compound. The service layer is testable without a client. The HTTP mapping lives in one file where it can be reviewed. Changing 404 to 410 for a case is one edit. And the same service can be exposed over a different transport without rewriting its errors.

The cost is a handler per error class, which is a few lines each and worth it past a handful of endpoints.

## The catch-all

A handler for `Exception` catches anything you did not anticipate:

```python
@app.exception_handler(Exception)
async def unhandled(request, exc):
    logger.exception("unhandled")
    return JSONResponse(status_code=500, content={"detail": "Something went wrong"})
```

Three rules for it.

**Log the real exception**, with a request identifier, so the failure is diagnosable.

**Return something generic.** A traceback in a response body is an information leak &mdash; it names files, line numbers, library versions and sometimes values &mdash; and it is the kind that ends up in a screenshot in a public issue.

**Include a correlation id** the caller can quote. That turns "it broke" into a log line you can find.

Note that this handler does not run in the same way when the app is in debug mode or under some test configurations, where the exception is re-raised so you can see it. That is deliberate and worth knowing when it appears not to work locally.

## Validation stays separate

`RequestValidationError` has its own handler, distinct from `HTTPException`.

That separation is useful: validation failures are structured, mechanical and want a field-oriented shape, while raised errors are single messages. Handling them together forces one envelope onto two different kinds of problem.

There is also `ResponseValidationError` for when your own handler returns something the response model rejects. That one should be loud in logs &mdash; it means your code broke its own contract, and no caller can do anything about it.

## What not to do

**Do not return errors instead of raising them.** A handler that returns `{"error": "..."}` with a 200 defeats every client's error handling.

**Do not catch and swallow.** A bare `except Exception: pass` around a database call turns a failure into a wrong answer.

**Do not leak internals in `detail`.** "Module not found" is right; the SQL that failed is not.

**Do not use 500 for a caller's mistake.** If they could have avoided it, it is a 4xx. A 500 means your code failed, and it should page somebody.

## A worked shape

For an app of any size, the arrangement that stays healthy:

Service functions raise domain exceptions and know nothing about HTTP. One module registers a handler per domain exception, mapping each to a status. A handler for `HTTPException` applies the house envelope. A handler for `RequestValidationError` shapes validation failures. A handler for `Exception` logs and returns a generic 500 with an id.

Five handlers, written once, and every endpoint after that just raises what it means.


## Mistakes people make

**Returning errors instead of raising them.** A handler returning `{"error": ...}` with a 200 defeats every client's error handling, and cannot be produced from four levels down.

**Importing fastapi in the service layer.** A function that raises `HTTPException` can only be used from a request - not from a job, a CLI or a test.

**Swallowing exceptions.** A bare `except Exception: pass` around a database call turns a failure into a wrong answer, which is far worse than an error.

**Returning the traceback.** It names files, line numbers, library versions and sometimes values. Log it; send an id.

**Hard-coding the status in a custom `HTTPException` handler.** Every non-404 then returns the wrong code.

**Dropping `exc.headers` in that handler.** The `Retry-After` you carefully attached silently disappears.

**500 for something the caller did.** If a different request would have worked, it is a 4xx.

## Where the layers sit

It helps to see the whole arrangement at once.

**Service functions** raise domain exceptions - `ModuleNotFound`, `SlugTaken`, `QuotaExceeded` - and import nothing from the web framework.

**One mapping module** registers a handler per domain exception, each choosing a status. This is the only place that knows a missing module is a 404.

**One handler for `HTTPException`** applies the house envelope to everything raised directly.

**One handler for `RequestValidationError`** shapes validation failures, which want a field-oriented format the others do not.

**One handler for `Exception`** logs and returns a generic 500 with a correlation id.

Five handlers written once. After that every endpoint raises what it means and nothing repeats the mapping.


## What the client should see

An error response has one job: let the caller decide what to do next. Three things serve that, and everything else is decoration.

**A status they can branch on.** Retry, re-authenticate, fix the request, or give up.

**A message a person could act on.** "Module not found" is useful; "error" is not; a stack trace is worse than either.

**An identifier they can quote.** When they open a ticket saying it failed, an id turns a search through logs into one lookup.

What does not belong: internal identifiers, SQL, file paths, library versions, or the values of anything sensitive. Each of those helps somebody attacking you more than it helps the caller.

A shape that covers it:

```json
{"detail": "Module not found", "request_id": "req-8f2c"}
```

Small, boring, and enough. If your organisation has an established format - RFC 7807 problem details, say - use it, and use it everywhere rather than on the endpoints somebody remembered.

## Errors during a response

One case that surprises people: an exception raised *after* the response has started streaming cannot become a clean error, because the status line and headers have already been sent.

That is why a `StreamingResponse` whose generator fails mid-way produces a truncated body rather than a 500. The client sees a connection that ended early, which is indistinguishable from a network failure.

The mitigation is to do the work that can fail before you start streaming, and to keep generators simple. It is also a reason not to reach for streaming unless the payload genuinely needs it.

## Testing the failures

Error paths are the least-tested part of most applications, and the easiest to test here.

A test that a missing module gives 404, that a duplicate gives 409, and that a malformed body gives 422 with the right `loc` costs three short functions and covers the branches most likely to be wrong.

Assert on the status and on `type` or a stable key - not on the message, for the same reason as in the Pydantic track. Prose gets reworded, and a suite that fails on wording is a suite people learn to ignore.

## Errors as part of the contract

The failure modes of an API are part of its interface, and treating them as an afterthought shows.

A caller integrating with your service needs to know: which errors are permanent and which are worth retrying; whether a 409 means "try again with different data" or "this already happened, you are done"; and whether an error response is stable enough to branch on.

Answering those in documentation costs little. `responses=` puts the shapes in the schema; a sentence per error class says what a caller should do about it. Both are read far more often than they are written.

The alternative - discovering the error contract by causing failures in production - is what most integrations actually do, and it is why so many clients end up matching on message strings that later change.


## What good error handling feels like

From the outside, an API with good error handling has three properties, none of which is about code.

Failures are **predictable**: the same mistake always produces the same status and shape, so a client can be written once.

They are **actionable**: the message says what to change, and the status says whether changing anything would help.

They are **diagnosable**: when something is genuinely broken, both sides can refer to the same identifier.

Everything in this module is in service of those. The handlers, the domain exceptions, the envelope and the logging are mechanisms; the properties are the point, and they are what a caller notices.

## Summary

`HTTPException` can be raised anywhere in the call stack and becomes a consistent JSON body. It takes headers, which several statuses require.

Business logic should raise domain exceptions and import nothing from the framework; one handler per exception class maps them to statuses at the edge, which keeps the service usable from a job, a CLI or a test.

A handler for `Exception` turns anything unanticipated into a clean 500 - logged in full, returned as a generic message plus an id. Validation keeps its own handler, because field-oriented failures want a different shape from single-message ones.

## Next

Structure comes next: splitting a growing application into routers, so that the error handlers, the models and the endpoints each live somewhere a newcomer can find them - and so that `main.py` stays short enough to read in one screen.

## A final note

The arrangement described here - domain exceptions raised low, mapped once at the edge - is worth adopting earlier than it feels necessary.

Retrofitting it means finding every `HTTPException` scattered through service code and deciding what each should have been, usually while also changing something else. Starting with it costs one extra class and one handler on the first error you need.
''',
    [
        {"q": "Where can `HTTPException` be raised?",
         "options": ["Only in the handler", "Anywhere in the call stack", "Only in dependencies", "Only in middleware"],
         "answer": 1,
         "why": "It is an exception, so it unwinds. A function five levels deep can refuse the request without every caller checking a return value."},
        {"q": "Why raise `ModuleNotFound` in a service rather than `HTTPException(404)`?",
         "options": ["It is faster", "The service may also be called from a job, a CLI or a test, none of which have a request to answer", "HTTPException is deprecated", "No reason"],
         "answer": 1,
         "why": "Business logic that imports fastapi can only be used from a request. Mapping the domain error to a status at the edge keeps the service reusable and testable."},
        {"q": "What should an `Exception` handler return to the client?",
         "options": ["The traceback", "A generic message plus a correlation id", "The exception type", "Nothing"],
         "answer": 1,
         "why": "A traceback names files, versions and sometimes values - an information leak. Log it, and give the caller an id they can quote."},
        {"q": "You override the `HTTPException` handler. What is easy to forget?",
         "options": ["The status code and `exc.headers`", "The detail", "The path", "Async"],
         "answer": 0,
         "why": "Hard-coding a status breaks every non-404, and dropping `exc.headers` silently discards things like `Retry-After` and `WWW-Authenticate`."},
    ],
)


# ---------------------------------------------------------------------------
# 13. APIRouter
# ---------------------------------------------------------------------------
topic(
    "apirouter",
    "APIRouter",
    "The Request",
    "Splitting an app before main.py becomes the file nobody wants to open.",
    _svg(_box(56, 12, 48, 18, S, A) + _txt(80, 25, "app", A, 8) +
         _arrow(70, 34, 40, 46) + _arrow(90, 34, 120, 46) +
         _box(14, 48, 52, 18, S) + _txt(40, 61, "/modules", M, 7) +
         _box(94, 48, 52, 18, S) + _txt(120, 61, "/tracks", M, 7)),
    [
        ("A router is a mini-app",
         "Register routes on it exactly as on an app, then include it. The prefix and "
         "tags apply to everything in it.",
         '''from fastapi import APIRouter, FastAPI

router = APIRouter(prefix="/modules", tags=["modules"])

@router.get("")
def list_modules():
    return ["Vectors", "Norms"]

@router.get("/{i}")
def read(i: int):
    return {"id": i}

app = FastAPI()
app.include_router(router)

c = TestClient(app)
print("/modules   ->", c.get("/modules").json())
print("/modules/7 ->", c.get("/modules/7").json())
print()
for r in app.routes:
    if getattr(r, "methods", None):
        print("  %-6s %s" % (",".join(sorted(r.methods)), r.path))'''),

        ("Several routers, one app",
         "This is the shape a growing project takes: one module per resource, "
         "assembled in one place.",
         '''from fastapi import APIRouter, FastAPI

modules = APIRouter(prefix="/modules", tags=["modules"])
tracks = APIRouter(prefix="/tracks", tags=["tracks"])

@modules.get("")
def list_modules(): return ["Vectors"]

@tracks.get("")
def list_tracks(): return ["maths", "python"]

@tracks.get("/{name}/modules")
def modules_in(name: str): return {"track": name, "modules": ["Vectors"]}

app = FastAPI(title="VizLearn")
app.include_router(modules)
app.include_router(tracks)

c = TestClient(app)
print(c.get("/modules").json())
print(c.get("/tracks").json())
print(c.get("/tracks/maths/modules").json())
print()
print("tags in the docs:", sorted({t for p in app.openapi()["paths"].values()
                                   for op in p.values() for t in op.get("tags", [])}))'''),

        ("Prefixes at include time",
         "The same router can be mounted more than once, which is how versioning is "
         "usually done.",
         '''from fastapi import APIRouter, FastAPI

router = APIRouter(tags=["modules"])

@router.get("/modules")
def list_modules():
    return ["Vectors"]

app = FastAPI()
app.include_router(router, prefix="/v1")
app.include_router(router, prefix="/v2")

c = TestClient(app)
print("/v1/modules ->", c.get("/v1/modules").json())
print("/v2/modules ->", c.get("/v2/modules").json())
print()
print("Same handlers, two paths. Real versioning usually wants two routers,")
print("but the mechanism is this.")'''),

        ("Dependencies for a whole router",
         "A dependency on the router applies to every route in it &mdash; the tidy "
         "way to require a key across a section.",
         '''from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

def require_key(x_api_key: str = Header(default="")):
    if x_api_key != "k-secret":
        raise HTTPException(401, "Bad or missing key")
    return x_api_key

admin = APIRouter(prefix="/admin", tags=["admin"],
                  dependencies=[Depends(require_key)])

@admin.get("/stats")
def stats(): return {"modules": 30}

@admin.delete("/cache")
def clear(): return {"cleared": True}

app = FastAPI()
app.include_router(admin)

c = TestClient(app)
print("no key :", c.get("/admin/stats").status_code)
print("bad key:", c.request("GET", "/admin/stats",
                            headers={"x-api-key": "nope"}).status_code)
print("good   :", c.request("GET", "/admin/stats",
                            headers={"x-api-key": "k-secret"}).json())
print("also   :", c.request("DELETE", "/admin/cache",
                            headers={"x-api-key": "k-secret"}).json())'''),

        ("Shared responses and a nested router",
         "<code>responses=</code> on a router documents a failure for every route in "
         "it, and routers include other routers.",
         '''from fastapi import APIRouter, FastAPI

inner = APIRouter(prefix="/lessons", tags=["lessons"])

@inner.get("")
def lessons(i: int = 0):
    return {"module": i, "lessons": ["Direction"]}

outer = APIRouter(prefix="/modules", tags=["modules"],
                  responses={404: {"description": "No such module"}})

@outer.get("/{i}")
def read(i: int):
    return {"id": i}

outer.include_router(inner)

app = FastAPI()
app.include_router(outer)

c = TestClient(app)
print(c.get("/modules/7").json())
print(c.get("/modules/lessons?i=7").json())
print()
print("documented 404s:", [p for p, spec in app.openapi()["paths"].items()
                           if "404" in spec["get"]["responses"]])'''),

        ("Order across routers",
         "Inclusion order decides match order, so a variable route in an early router "
         "can shadow a fixed one included later.",
         '''from fastapi import APIRouter, FastAPI

generic = APIRouter()
specific = APIRouter()

@generic.get("/modules/{i}")
def by_id(i: str): return {"route": "by_id", "value": i}

@specific.get("/modules/latest")
def latest(): return {"route": "latest"}

wrong = FastAPI()
wrong.include_router(generic)      # included first - wins
wrong.include_router(specific)

right = FastAPI()
right.include_router(specific)     # specific first
right.include_router(generic)

print("wrong order:", TestClient(wrong).get("/modules/latest").json())
print("right order:", TestClient(right).get("/modules/latest").json())'''),
    ],
    [
        "An <code>APIRouter</code> takes the same decorators as an app. <code>app.include_router()</code> merges its routes in.",
        "<code>prefix</code> and <code>tags</code> apply to every route in the router &mdash; tags are what group endpoints in the documentation.",
        "A prefix can be given at include time instead, so one router can be mounted at more than one path.",
        "<code>dependencies=[...]</code> on a router applies to every route in it &mdash; the tidy way to require authentication across a whole section.",
        "Routers include other routers, so a nested resource can live in its own file.",
        "Inclusion order determines match order: a variable route in an early router shadows a fixed one included later.",
    ],
    '''
title: APIRouter
intro: Splitting an app before main.py becomes the file nobody wants to open.

## The problem it solves

Every FastAPI project starts as one file, and one file works for perhaps twenty routes. Past that it becomes the file everybody edits, every change conflicts, and nobody can find anything.

`APIRouter` is the answer, and the useful time to reach for it is *before* you need to.

## A router is a mini-app

```python
router = APIRouter(prefix="/modules", tags=["modules"])

@router.get("")
def list_modules():
    ...

app.include_router(router)
```

The decorators are the same. The prefix is prepended to every path in the router, so `@router.get("")` becomes `/modules`. The tags apply to every route, which is what groups them into a section in the interactive documentation.

Note `@router.get("")` rather than `@router.get("/")` for the collection itself. With a prefix, the empty string gives `/modules` and a slash gives `/modules/`, and the difference is the trailing-slash redirect from earlier. Pick one convention.

## The shape a project takes

One router per resource, one file each, assembled in one place:

```
app/
  main.py            # creates the app, includes routers
  routers/
    modules.py
    tracks.py
    admin.py
```

`main.py` becomes short and boring, which is what you want from the file that wires everything together. Each router file owns one resource and can be read on its own.

The advice worth acting on: create `routers/` on day one, even with two endpoints in it. Moving three routes later is trivial; moving eighty is a weekend, and by then something will depend on the import layout.

## Prefixes at include time

A prefix can be given when including instead of when creating:

```python
app.include_router(router, prefix="/v1")
```

That lets one router be mounted at several paths, which is the mechanism behind version prefixes. Whether you *should* mount the same handlers at two versions is a different question &mdash; usually a new version exists because behaviour differs, and then you want two routers.

Where this genuinely helps is keeping the version out of the router file entirely, so the routes read as `/modules` and the assembly decides they live under `/v1`.

## Dependencies for a section

```python
admin = APIRouter(prefix="/admin", dependencies=[Depends(require_key)])
```

Every route in that router now requires the key. This is the tidy way to protect a section, and it is better than remembering to add a dependency to each endpoint &mdash; because the one you forget is the one that matters.

Note the dependency's return value is not passed to the handlers when declared this way; it runs for its effect. When a handler needs the value, it declares its own `Depends` as well, and the result is cached within the request so the work happens once.

Dependencies get a full tier next, and this is the first genuinely useful thing they do.

## Shared documentation

`responses=` on a router documents a failure shape for every route in it. If every endpoint under `/modules` can 404, saying so once is better than repeating it six times.

`deprecated=True` on a router marks a whole section as deprecated in the docs, which is a civilised way to retire a version.

## Nesting

Routers include routers:

```python
outer.include_router(inner)
```

Prefixes compose, so a nested resource can live in its own file and still appear under its parent's path. Useful for genuine ownership &mdash; lessons within modules &mdash; and easy to overdo. Two levels is usually enough; four produces paths nobody types correctly.

## Order still decides

The rule from the first tier, now with a longer reach: routes match in registration order, and across routers that means **inclusion order**.

A router with `/modules/{id}` included before a router with `/modules/latest` makes the second unreachable, and the mistake is harder to see because the two routes are in different files.

Two habits that avoid it. Keep routes for one path space in one router, so ordering is visible in one place. And annotate path parameters precisely &mdash; `int` rather than `str` &mdash; so a fixed path that gets shadowed fails loudly instead of silently matching.

When something does not route as expected, print `app.routes`. It shows the merged table in match order and settles the question immediately.

## Testing a router alone

A router can be included into a small app built for a test:

```python
app = FastAPI()
app.include_router(modules.router)
client = TestClient(app)
```

That gives a test covering one resource without the rest of the application, its dependencies or its startup. It is one of the quieter benefits of splitting up: the pieces become independently testable.

## What goes in a router file

Routes, and as little else as possible.

The handlers should be thin, calling into a service module. The models can live in their own file, or beside the router if they are only used there. The dependency functions usually deserve their own module, since several routers need the same ones.

What should not be in there is business logic, database access or configuration. A router file that imports your ORM directly works and stops being testable without a database.


## Mistakes people make

**Waiting to split.** Moving three routes is trivial; moving eighty is a weekend, and by then imports depend on the layout. Create `routers/` on day one.

**Business logic in a router file.** A router that imports your ORM directly works and stops being testable without a database. Handlers should be thin and call a service.

**Inconsistent trailing slashes.** With a prefix, `@router.get("")` gives `/modules` and `@router.get("/")` gives `/modules/`. Pick one across the whole app.

**Ignoring inclusion order.** A variable route in an early router shadows a fixed one included later, and the two files make it hard to see. `print(app.routes)` settles it.

**Nesting too deep.** Two levels is usually enough. Four produces paths nobody types correctly and routers nobody wants to trace.

**Forgetting a router-level dependency is not injected.** It runs for its effect; a handler needing the value declares its own `Depends`, and the result is cached within the request.

## What a good layout looks like

For an application of any size the arrangement that holds up is unremarkable, which is the point.

`main.py` creates the app, registers exception handlers and includes routers. It should be short enough to read in one screen.

`routers/` holds one file per resource, each owning its paths and nothing else.

`schemas/` or `models/` holds the Pydantic models - separated by direction, as the response-model module argued.

`services/` holds the functions that do the work, importing nothing from FastAPI.

`dependencies.py` holds the shared `Depends` functions, since several routers need the same ones.

Nothing there is clever. Its value is that a newcomer can guess where anything lives, and that each piece can be tested without starting the whole application.


## Assembling the app

`main.py` in a healthy project does four things and nothing else.

It creates the `FastAPI` instance with a title, version and description - which become the header of your documentation.

It registers exception handlers, so the error contract is declared in one place.

It includes routers, in an order chosen deliberately rather than by accident.

It adds middleware, if any.

Everything else lives somewhere it can be tested. The value of a boring assembly file is that it is the one place to look when asking "what does this application consist of?", and the answer fits on a screen.

## Configuration and startup

Two things commonly end up in `main.py` that are worth separating.

**Settings** belong in their own module - a Pydantic settings model read once. Scattering `os.getenv` through routers makes it impossible to see what the application needs to run.

**Startup work** - opening a connection pool, loading a model - belongs in a lifespan handler rather than at import time. Work done at import happens when a test imports the module, which is how a test suite ends up needing a database to collect.

Both get proper treatment in the runtime tier. The habit worth forming now is not putting either in the file that wires routes together.

## Splitting by resource, not by layer

One structural choice worth stating, because both options look reasonable.

Grouping by **resource** - `routers/modules.py`, `services/modules.py`, `schemas/modules.py` - means a change to one concept touches files with the same name in different directories.

Grouping by **layer alone**, with every router in one file and every schema in another, means those same files grow without bound and every change collides with every other.

For anything past a few resources, resource-first inside a shallow layer structure is what stays navigable. The test is whether a newcomer asked to add a field can guess which files to open. If the answer is "search for the word", the layout has stopped helping.

## Next

That completes the request tier: methods, headers, forms, files, status codes, error handling and structure. The next tier is dependencies &mdash; `Depends`, the feature that makes all of the above composable, and the one that most distinguishes FastAPI from what came before it.


## A closing thought

Structure is the cheapest thing to get right early and among the most expensive to fix late.

A router file created on the first day costs nothing. The same split attempted after eighty endpoints means untangling imports, moving tests, and a diff nobody can review properly - so it does not happen, and the file keeps growing.

The rule of thumb: if you can imagine a second resource, make the directory now.


## One more benefit

Splitting an app makes it testable in pieces, and that is worth more than the tidiness.

A router included into a small `FastAPI()` built for one test file gives you a client that exercises one resource - without the rest of the application, its other routers, its startup work or its unrelated dependencies.

That means a test suite that runs fast, fails specifically, and does not require the whole system to be constructible. It is the difference between "the tests need a database, Redis and three environment variables" and "the tests need the module under test".

## Summary

An `APIRouter` takes the same decorators as an app, carries a prefix and tags, and merges in through `include_router`. Routers nest, accept shared dependencies and responses, and can be mounted at more than one prefix.

Inclusion order is match order, so a variable route in an early router shadows a fixed one included later.

Create the directory on day one. Keep handlers thin and business logic out of router files, so each piece can be tested without starting the whole application - which is the quiet benefit of splitting up, and the reason it is worth doing before it hurts.

## Where this leaves you

That completes the request tier. You can route by path and method, read every source of input a request has, decide what comes back and with which status, produce errors that a caller can act on, and split an application before its main file becomes unmanageable.

What is still missing is the thing that makes all of it composable: a way to declare that an endpoint needs a database session, an authenticated user or a validated set of filters, and have that requirement satisfied, cached and documented automatically. That is `Depends`, and it is the next tier.

## A final note

None of the structure in this module is FastAPI-specific. Grouping by resource, keeping handlers thin, separating configuration and startup, and assembling in a boring file are practices that predate the framework and outlast it.

What FastAPI contributes is that following them costs almost nothing: a router is four lines, inclusion is one, and the documentation reorganises itself around your tags without being asked.
''',
    [
        {"q": "What does `prefix` on an APIRouter do?",
         "options": ["Renames the router", "Prepends to every path in it", "Sets a tag", "Adds a dependency"],
         "answer": 1,
         "why": "It applies to every route in the router, so `@router.get(\"\")` with `prefix=\"/modules\"` becomes `/modules`. Tags, set the same way, group the routes in the docs."},
        {"q": "Why can a fixed route in one router be unreachable?",
         "options": ["A bug", "Inclusion order sets match order, so an earlier router's variable route shadows it", "Routers are unordered", "Prefixes conflict"],
         "answer": 1,
         "why": "Across routers, inclusion order is match order - and the mistake is harder to spot because the two routes live in different files."},
        {"q": "What does `dependencies=[...]` on a router do?",
         "options": ["Nothing", "Applies to every route in it, running for its effect", "Passes the value to each handler", "Only documents them"],
         "answer": 1,
         "why": "It runs for every route in the section. The return value is not injected; a handler that needs it declares its own Depends, and the result is cached within the request."},
        {"q": "When should you create a routers/ directory?",
         "options": ["After 50 endpoints", "On day one, even with two", "Never", "Only for large teams"],
         "answer": 1,
         "why": "Moving three routes is trivial and moving eighty is a weekend - and by then something depends on the import layout."},
    ],
)


# ---------------------------------------------------------------------------
# 14. Dependency injection
# ---------------------------------------------------------------------------
topic(
    "dependency_injection",
    "Dependency Injection",
    "Dependencies",
    "Depends: declaring what an endpoint needs and letting the framework supply "
    "it - the feature that most distinguishes FastAPI.",
    _svg(_box(14, 16, 132, 20, S) + _txt(80, 30, "def endpoint(user = Depends(current_user))", M, 7) +
         _arrow(80, 40, 80, 50) +
         _box(40, 52, 80, 22, S, A) + _txt(80, 67, "resolved, cached", A, 8)),
    [
        ("A dependency is just a function",
         "Declare a parameter as <code>Depends(fn)</code> and FastAPI calls "
         "<code>fn</code> and passes the result. Nothing is registered anywhere.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()

def pagination(limit: int = 10, offset: int = 0):
    return {"limit": min(limit, 100), "offset": offset}

@app.get("/modules")
def list_modules(page: dict = Depends(pagination)):
    return {"page": page}

@app.get("/tracks")
def list_tracks(page: dict = Depends(pagination)):
    return {"page": page}

c = TestClient(app)
print(c.get("/modules").json())
print(c.get("/modules?limit=500&offset=20").json(), "<- capped by the dependency")
print(c.get("/tracks?limit=3").json())'''),

        ("Its parameters are the request, too",
         "A dependency reads query parameters, headers and bodies exactly as a "
         "handler does &mdash; and they appear in the documentation.",
         '''import json
from fastapi import Depends, FastAPI, Header, Query

app = FastAPI()

def search_filters(
    q: str = Query(default="", max_length=50, description="Free-text search."),
    track: str = Query(default=""),
    x_locale: str = Header(default="en"),
):
    return {"q": q, "track": track, "locale": x_locale}

@app.get("/search")
def search(f: dict = Depends(search_filters)):
    return f

c = TestClient(app)
print(c.get("/search?q=vectors&track=maths").json())
print()
params = app.openapi()["paths"]["/search"]["get"]["parameters"]
for p in params:
    print("%-9s in %-6s %s" % (p["name"], p["in"], p["schema"].get("type")))'''),

        ("Raising from a dependency",
         "A dependency that raises stops the request before the handler runs. That "
         "is what makes it the right place for authentication.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException, status

app = FastAPI()
TOKENS = {"tok-ada": "ada", "tok-grace": "grace"}
reached = []

def current_user(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    if token not in TOKENS:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sign in first",
                            headers={"WWW-Authenticate": "Bearer"})
    return TOKENS[token]

@app.get("/me")
def me(user: str = Depends(current_user)):
    reached.append(user)
    return {"user": user}

c = TestClient(app)
def call(tok):
    h = {"authorization": "Bearer " + tok} if tok else {}
    r = c.request("GET", "/me", headers=h)
    return r.status_code, r.json()

print("no token :", call(None))
print("bad token:", call("nope"))
print("good     :", call("tok-ada"))
print()
print("handler ran for:", reached)'''),

        ("Resolved once per request",
         "Two parameters depending on the same function get one call, not two. The "
         "result is cached for the life of the request.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
calls = []

def expensive():
    calls.append(1)
    return {"value": len(calls)}

def wrapper(e: dict = Depends(expensive)):
    return {"wrapped": e}

@app.get("/once")
def once(a: dict = Depends(expensive), b: dict = Depends(wrapper)):
    return {"a": a, "b": b, "calls_this_request": len(calls)}

c = TestClient(app)
print("request 1:", c.get("/once").json())
calls.clear()
print("request 2:", c.get("/once").json())
print()
print("Two references, one call. Caching is per request, not global.")'''),

        ("Turning the cache off",
         "<code>use_cache=False</code> forces a fresh call &mdash; for anything that "
         "should differ per use, such as a generated identifier.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
counter = {"n": 0}

def ticket():
    counter["n"] += 1
    return "T%03d" % counter["n"]

@app.get("/cached")
def cached(a: str = Depends(ticket), b: str = Depends(ticket)):
    return {"a": a, "b": b}

@app.get("/fresh")
def fresh(a: str = Depends(ticket, use_cache=False),
          b: str = Depends(ticket, use_cache=False)):
    return {"a": a, "b": b}

c = TestClient(app)
print("cached:", c.get("/cached").json(), "<- one call, shared")
counter["n"] = 0
print("fresh :", c.get("/fresh").json(), "<- called twice")'''),

        ("What it replaces",
         "The same endpoint written both ways. The dependency version has the "
         "requirement in the signature, where the documentation can see it.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
TOKENS = {"tok-ada": "ada"}

# Without: every handler repeats the check, and the docs know nothing.
@app.get("/by-hand")
def by_hand(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    if token not in TOKENS:
        raise HTTPException(401, "Sign in first")
    user = TOKENS[token]
    return {"user": user}

# With: stated once, declared in the signature.
def current_user(authorization: str = Header(default="")):
    token = authorization.replace("Bearer ", "")
    if token not in TOKENS:
        raise HTTPException(401, "Sign in first")
    return TOKENS[token]

@app.get("/declared")
def declared(user: str = Depends(current_user)):
    return {"user": user}

c = TestClient(app)
h = {"authorization": "Bearer tok-ada"}
print("by hand :", c.request("GET", "/by-hand", headers=h).json())
print("declared:", c.request("GET", "/declared", headers=h).json())
print()
print("Both document the header, because both declare it -")
print("but only one states the requirement once for every endpoint.")'''),
    ],
    [
        "A dependency is an ordinary function. <code>Depends(fn)</code> calls it and passes the result; there is no registry and no container.",
        "Its own parameters are request parameters, so a dependency can read query values, headers and bodies &mdash; and they all appear in the schema.",
        "Raising inside a dependency stops the request before the handler runs, which is why authentication belongs there.",
        "Results are <strong>cached per request</strong>: two parameters depending on the same function produce one call.",
        "<code>Depends(fn, use_cache=False)</code> forces a fresh call each time it is referenced.",
        "The value is not the wiring &mdash; it is that the requirement is in the signature, where the documentation and the reader can both see it.",
    ],
    '''
title: Dependency Injection
intro: Declaring what an endpoint needs and letting the framework supply it.
## The whole idea

```python
def pagination(limit: int = 10, offset: int = 0):
    return {"limit": min(limit, 100), "offset": offset}

@app.get("/modules")
def list_modules(page: dict = Depends(pagination)):
    ...
```

`Depends(fn)` means: call `fn`, and pass what it returns.

There is no registry, no container, no configuration and no base class. A dependency is a function, and declaring one is a default value in a signature. That simplicity is why the feature is worth learning properly &mdash; it is much smaller than "dependency injection" usually implies.

## Dependencies see the request

The important second fact: a dependency's own parameters are request parameters. It can declare query values, headers, cookies, path parameters and a body, using exactly the syntax a handler uses.

So `pagination` above does not receive the request and dig through it. It declares `limit` and `offset`, and FastAPI supplies them from the query string, converted and validated.

That has a consequence people miss: **those parameters appear in the OpenAPI document**. An endpoint depending on `search_filters` documents `q`, `track` and `x-locale` as its own parameters, because as far as a caller is concerned they are. The abstraction does not hide anything from the contract.

## Raising

A dependency that raises stops the request. The handler never runs.

That is what makes it the right home for authentication, authorisation and any precondition:

```python
def current_user(authorization: str = Header(default="")):
    if token not in TOKENS:
        raise HTTPException(401, "Sign in first")
    return TOKENS[token]
```

Every endpoint that needs a user now writes one parameter. There is no possibility of an endpoint forgetting the check and no possibility of two endpoints checking differently &mdash; which is exactly the failure mode of doing it by hand.

## Caching within a request

If two parameters depend on the same function, it is called **once**. The result is cached for the duration of that request and shared.

This matters more than it first appears, because dependencies compose. A handler might depend on `current_user`, and also on `permissions`, which itself depends on `current_user`. Without caching, the token would be decoded twice. With it, once.

The cache is per request. Nothing is shared between requests, which is correct &mdash; a cached user leaking into the next request would be a serious bug rather than an optimisation.

`Depends(fn, use_cache=False)` opts out, for anything that should genuinely differ per reference: a generated identifier, a fresh timestamp, a new random value.

## What it replaces

Compare the two versions in the last editor above. Both work. Both even document the header, because both declare it.

The difference is where the requirement lives. In the hand-written version it is four lines at the top of a handler, repeated in every handler that needs it, and diverging quietly as they are edited. In the dependency version it is one function, and each endpoint declares a parameter.

The scaling difference is the point. Ten endpoints needing a user means ten parameters and one function &mdash; not forty lines that must agree.

## When something is not a dependency

Two habits worth avoiding.

**Wrapping something trivial.** `Depends` on a function that returns a constant is indirection with no benefit. Import the constant.

**Putting business logic in one.** A dependency should produce something the handler needs &mdash; a user, a session, a validated set of filters. A dependency that performs the operation and returns a result has moved the endpoint's work into its signature, where it is harder to find and harder to test.

The test: could you describe it as "this endpoint needs an X"? Then it is a dependency. If it is "this endpoint does Y", it is not.

## Types and the return value

`page: dict = Depends(pagination)` annotates the parameter, and that annotation is documentation for a reader rather than something enforced &mdash; the value is whatever the dependency returned.

For anything real, return a model rather than a dict. `current_user` returning a `User` gives every handler attribute access and editor completion, and makes the dependency's contract explicit.

There is a newer spelling using `Annotated` that is worth adopting:

```python
CurrentUser = Annotated[User, Depends(current_user)]

def me(user: CurrentUser):
    ...
```

The dependency becomes a named type, reusable across every endpoint, and the signature reads as ordinary Python. It is the same idea as the constrained types from the Pydantic track, applied here.

## Where they live

A `dependencies.py` beside your routers is the usual home, for the same reason a `types.py` is: several routers need the same ones, and a shared file is where they can be found.

Reading that file should tell you what the application's endpoints are allowed to assume &mdash; a user, a database session, a tenant, a set of filters. That is a useful summary to have in one place.


## Mistakes people make

**Wrapping something trivial.** `Depends` on a function returning a constant is indirection with no benefit. Import the constant.

**Putting the endpoint's work in a dependency.** A dependency supplies what the endpoint needs; it should not *be* what the endpoint does. The test: can you say "this endpoint needs an X"? Then it is a dependency. "This endpoint does Y" is not.

**Returning a dict where a model belongs.** `user["name"]` has no completion and no checking. A dependency returning a model gives every handler attribute access and states its contract.

**Assuming the cache is global.** It is per request. Nothing survives to the next one - which is correct, because a cached user leaking across requests would be a serious bug.

**Expecting `Depends` to hide parameters.** Everything a dependency declares appears in the endpoint's documented parameters. That is a feature, and it means adding a required parameter to a shared dependency is a breaking change for every endpoint using it.

**Doing slow work without noticing where.** A dependency runs on every request to every endpoint that declares it. A lookup that seemed cheap on one route is multiplied by everything that shares it.

## The Annotated form

Worth adopting early, because it changes how the signatures read:

```python
CurrentUser = Annotated[User, Depends(current_user)]

@app.get("/me")
def me(user: CurrentUser):
    ...
```

The dependency becomes a named type. The signature is ordinary Python with no default-argument trick, the requirement is declared once and reused, and a reader sees a type rather than a call.

It is the same idea as the constrained types from the Pydantic track, and for a codebase with several dependencies it is the tidier spelling.


## What this replaces in other frameworks

It is worth seeing what the same job looks like elsewhere, because it explains why the FastAPI version is so small.

A **decorator** - `@login_required` - is the Flask-shaped answer. It works, and the requirement is invisible to the function's signature, so nothing documents it, the value has to be smuggled in through a global request object, and composing two decorators means caring about their order.

A **container** - the Spring or .NET answer - registers implementations against interfaces and resolves them by type. Powerful, and it needs configuration, wiring and a mental model of its own.

A **base class** - `class MyView(AuthenticatedView)` - ties the requirement to inheritance, so an endpoint needing two unrelated things needs multiple inheritance.

FastAPI's version is a default argument. There is nothing to register, nothing to configure, no ordering to reason about, and the requirement is written where a reader and the schema generator both look. That is a genuinely good trade, and it is why the feature is worth using rather than routed around.

## Testing an endpoint that has dependencies

The payoff arrives in the test file, and it is worth previewing before the overrides module.

An endpoint declaring `Depends(get_db)` and `Depends(current_user)` can be tested without a database and without a token, because both can be replaced at the app level. The handler is unchanged; only what it depends on moves.

That is the practical argument for pushing requirements into dependencies rather than reaching for them inside handlers. A handler that calls `get_session()` directly cannot be tested without a session. One that declares it can.

## One habit worth forming

When you find yourself writing the same four lines at the top of a second handler, that is the moment.

Not the fifth handler, and not after a refactor - the second. Extracting it costs one function and one parameter, and every endpoint after that inherits the rule instead of copying it.

The failure mode of waiting is not the duplication itself. It is that the copies drift: one checks the header case-insensitively, one strips whitespace, one returns a dict where the other returns a model. By the time somebody consolidates them there are four behaviours to reconcile and no way to know which was intended.

## Summary

`Depends(fn)` calls a function and passes the result. The function's own parameters are request parameters, so a dependency can read anything a handler can - and everything it declares appears in the endpoint's documented contract.

Raising inside one stops the request before the handler runs, which is why authentication belongs there rather than in a body somebody can forget to write. Results are cached per request, so a dependency reached by several paths is called once.

Prefer returning a model over a dict, adopt the `Annotated` spelling for anything reused, and keep dependencies to "this endpoint needs an X" rather than "this endpoint does Y".


## Why it is the framework's best idea

Of everything FastAPI adds on top of Starlette and Pydantic, this is the part with no equivalent elsewhere that is this small.

A decorator hides the requirement from the signature. A container needs registration and configuration. A base class ties the requirement to inheritance. Middleware applies to everything and documents nothing.

`Depends` is a default argument. It needs no setup, composes without ordering rules, works with any callable, appears in the generated schema, and can be replaced in a test with one dictionary assignment.

The result is that "what does this endpoint need?" is answerable by reading its signature, and "what happens if it is not there?" is answerable by reading one function. Those two properties are most of what makes a large FastAPI application stay legible.


## A closing thought

The habit this module is really teaching is not `Depends`. It is declaring what you need instead of reaching for it.

A handler that calls `get_session()` in its body has acquired something. A handler that declares `session: Session = Depends(get_session)` has stated a requirement and let something else satisfy it. The first cannot be tested without a database, documented, or reused; the second is all three.

That distinction is older and larger than this framework. FastAPI's contribution is making the declaring version shorter than the acquiring one, which is the only reliable way to get people to prefer it.


## Two rules

**Extract on the second occurrence**, not the fifth. The cost is one function; the cost of waiting is four copies that have quietly diverged.

**Dependencies supply, they do not perform.** "This endpoint needs an X" is a dependency; "this endpoint does Y" is the handler's job.

## Next

Dependencies that need to clean up after themselves - a session that must be closed whether the handler succeeded or raised - which is what `yield` is for, and where the transaction pattern comes from.
''',
    [
        {"q": "What is a FastAPI dependency?",
         "options": ["A registered class", "An ordinary function called by Depends", "A middleware", "A Pydantic model"],
         "answer": 1,
         "why": "No registry, no container, no base class. `Depends(fn)` calls the function and passes the result, and the function's own parameters are request parameters."},
        {"q": "Two parameters depend on the same function. How many times is it called?",
         "options": ["Twice", "Once - the result is cached for the request", "Once globally", "Depends on the type"],
         "answer": 1,
         "why": "Caching is per request, which matters because dependencies compose - a handler and a sub-dependency both needing `current_user` decode the token once, not twice."},
        {"q": "Why is a dependency the right place for authentication?",
         "options": ["It is faster", "Raising there stops the request before the handler runs, and the rule is stated once", "It is required", "It hides the header from the docs"],
         "answer": 1,
         "why": "No endpoint can forget the check and no two can check differently - and the header still appears in the schema, because the dependency declares it."},
        {"q": "Do a dependency's parameters appear in the API documentation?",
         "options": ["No, they are internal", "Yes - as the endpoint's own parameters", "Only headers do", "Only with a flag"],
         "answer": 1,
         "why": "As far as a caller is concerned they are the endpoint's parameters, so the abstraction hides nothing from the contract."},
    ],
)


# ---------------------------------------------------------------------------
# 15. Dependencies with yield
# ---------------------------------------------------------------------------
topic(
    "dependencies_with_yield",
    "Dependencies with yield",
    "Dependencies",
    "Setup before the handler, teardown after it - the shape a database session "
    "needs.",
    _svg(_box(20, 14, 120, 18, S) + _txt(80, 27, "open", A, 8) +
         _arrow(80, 34, 80, 42) +
         _box(20, 44, 120, 18, S) + _txt(80, 57, "handler runs", M, 8) +
         _arrow(80, 64, 80, 72) +
         _box(20, 74, 120, 16, S) + _txt(80, 86, "close", A, 8)),
    [
        ("yield splits it in two",
         "Everything before the <code>yield</code> runs first, the handler gets the "
         "yielded value, and everything after runs when the response is done.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
log = []

def get_session():
    log.append("open")
    try:
        yield {"id": len(log)}
    finally:
        log.append("close")

@app.get("/modules")
def list_modules(db: dict = Depends(get_session)):
    log.append("handler")
    return {"db": db}

print(TestClient(app).get("/modules").json())
print("order:", log)'''),

        ("Teardown runs even on failure",
         "That is the whole point. A session opened before the handler is closed "
         "whether the handler returned or raised.",
         '''from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
log = []

def get_session():
    log.append("open")
    try:
        yield "session"
    finally:
        log.append("close")

@app.get("/ok")
def ok(db: str = Depends(get_session)):
    return {"ok": True}

@app.get("/boom")
def boom(db: str = Depends(get_session)):
    raise HTTPException(404, "Not found")

c = TestClient(app)
c.get("/ok")
print("success :", log)
log.clear()
r = c.get("/boom")
print("failure :", log, "->", r.status_code)
print()
print("Both closed. Without try/finally the second would have leaked.")'''),

        ("Commit on success, roll back on failure",
         "The pattern this exists for: the teardown can see whether the handler "
         "raised, and decide what to do about it.",
         '''from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
events = []

class Session:
    def __init__(self): self.writes = []
    def add(self, x): self.writes.append(x)
    def commit(self): events.append("commit %s" % self.writes)
    def rollback(self): events.append("rollback %s" % self.writes)
    def close(self): events.append("close")

def get_db():
    db = Session()
    try:
        yield db
        db.commit()             # only reached if the handler did not raise
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

@app.post("/good")
def good(db: Session = Depends(get_db)):
    db.add("module"); return {"ok": True}

@app.post("/bad")
def bad(db: Session = Depends(get_db)):
    db.add("module"); raise HTTPException(400, "nope")

c = TestClient(app)
c.post("/good"); print("good:", events)
events.clear()
c.post("/bad");  print("bad :", events)'''),

        ("Order with several of them",
         "Teardowns run in reverse, like nested context managers &mdash; the last "
         "thing opened is the first thing closed.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
log = []

def outer():
    log.append("outer open")
    try: yield "outer"
    finally: log.append("outer close")

def inner(o: str = Depends(outer)):
    log.append("inner open")
    try: yield "inner(%s)" % o
    finally: log.append("inner close")

@app.get("/x")
def x(v: str = Depends(inner)):
    log.append("handler")
    return {"v": v}

print(TestClient(app).get("/x").json())
print()
for step in log:
    print(" ", step)'''),

        ("It is still cached per request",
         "Two references to a yield dependency share one setup and one teardown, "
         "the same as any other.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
log = []

def session():
    log.append("open")
    try: yield "s%d" % log.count("open")
    finally: log.append("close")

def repo(s: str = Depends(session)):
    return "repo(%s)" % s

@app.get("/x")
def x(a: str = Depends(session), b: str = Depends(repo)):
    return {"a": a, "b": b}

print(TestClient(app).get("/x").json())
print("log:", log)
print()
print("One open, one close - even though two parameters wanted it.")'''),

        ("What not to do in the teardown",
         "Raising after the yield happens once the response is already being built, "
         "so it cannot become a clean error for the caller.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
log = []

def risky():
    log.append("open")
    try:
        yield "value"
    finally:
        log.append("close")
        # Anything that can fail here should be caught here.
        try:
            raise RuntimeError("cleanup failed")
        except RuntimeError as e:
            log.append("swallowed: %s" % e)

@app.get("/x")
def x(v: str = Depends(risky)):
    return {"v": v}

r = TestClient(app).get("/x")
print("status:", r.status_code, r.json())
print("log   :", log)
print()
print("The response was already decided. Log the failure; do not raise it.")'''),
    ],
    [
        "Code before <code>yield</code> is setup, the yielded value is what the handler receives, and code after it is teardown.",
        "Teardown runs whether the handler returned or raised, which is why <code>try/finally</code> belongs around the yield.",
        "Putting <code>commit()</code> immediately after the yield and <code>rollback()</code> in an <code>except</code> gives the transaction pattern for free.",
        "With several yield dependencies, teardowns run in reverse order &mdash; last opened, first closed.",
        "They are cached per request like any dependency: two references share one setup and one teardown.",
        "Do not raise in the teardown. The response is already being built, so the error cannot reach the caller cleanly &mdash; catch and log it instead.",
    ],
    '''
title: Dependencies with yield
intro: Setup before the handler, teardown after it, and the transaction pattern that falls out.
## The shape

```python
def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()
```

Everything before the `yield` runs before the handler. The yielded value is what the handler receives. Everything after runs once the response has been produced.

It is a generator, and it behaves like a context manager &mdash; which is exactly the point, because "acquire, use, release" is what a database session, a file handle, a lock or a temporary directory all need.

## Teardown always runs

The reason this exists rather than a plain dependency returning a session: cleanup must happen even when the handler fails.

Without `try/finally`, a handler that raises a 404 would skip the close and leak the connection. With it, the session is returned to the pool either way. In an application handling real traffic, that difference is the gap between a pool that stays healthy and one that is exhausted an hour after deploy.

The rule is simple: if a yield dependency acquires anything, the `yield` belongs inside a `try`, and the release belongs in `finally`.

## The transaction pattern

Because the teardown can observe whether the handler raised, the standard database shape falls out naturally:

```python
def get_db():
    db = Session()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```

`commit()` sits immediately after the `yield`, so it only runs if the handler completed. Any exception &mdash; including an `HTTPException` &mdash; rolls back and re-raises. `close()` runs regardless.

Three lines, and every endpoint using this dependency now has correct transaction handling without writing any. That is a large amount of correctness for very little code, and it is the single most common use of the feature.

Note the `raise` in the `except`. Swallowing there would turn a failed request into a successful-looking one with a rolled-back transaction, which is worse than either outcome alone.

## Nesting and order

A yield dependency can depend on another. Setups run outermost first, teardowns run in reverse &mdash; the same discipline as nested `with` blocks, and for the same reason: the inner thing may need the outer one to still exist while it closes.

The fourth editor above prints the whole sequence. It is worth running once, because the ordering is the sort of thing that is obvious when you see it and easy to get backwards when reasoning about it.

## Caching applies

A yield dependency is cached per request like any other. Two parameters wanting the same session get one session, opened once and closed once.

That matters for correctness rather than just performance: two separate sessions in one request would mean two transactions, and a handler that read through one and wrote through the other would produce results nobody could explain.

## What not to do in teardown

**Do not raise.** By the time the teardown runs, the response has been decided and is being sent. An exception there cannot become a clean error for the caller, and depending on where it happens it may truncate the response or surface as a server error unrelated to anything the client did.

If cleanup can fail, catch it and log it. The request already succeeded or failed on its own terms, and a cleanup problem is an operational issue rather than something the caller can act on.

**Do not do slow work.** The teardown runs after the handler, and for a synchronous dependency it is on the request path. A long-running cleanup delays the response for no benefit to the caller. Anything genuinely slow belongs in a background task.

**Do not rely on the exception being visible.** In older FastAPI versions the exception was not always available to the teardown in the way people expected. The `try/except/finally` shape above works because it wraps the `yield` directly rather than trying to inspect state.

## What belongs here

Anything with a lifetime tied to the request: database sessions, transactions, file handles, temporary directories, locks, an HTTP client that should be closed.

What does not: work that could be done once at startup. A connection *pool* is created at startup and lives for the process; a *session* is taken from it per request. Confusing the two produces either a pool rebuilt on every request or a session shared between them, and both are bad in different ways.

That distinction is the lifespan module's subject.


## Mistakes people make

**No `try/finally`.** The single most consequential omission. A handler that raises then skips the cleanup, and a connection leaks on exactly the requests you most want to survive.

**Committing in `finally`.** It runs on failure too, so a rolled-back-looking request quietly commits. Commit belongs immediately after the `yield`, where only success reaches it.

**Swallowing the exception.** An `except` that rolls back and does not re-raise turns a failed request into one that looks successful with nothing written.

**Raising in the teardown.** The response is already being built. The error cannot reach the caller cleanly and may truncate what was being sent.

**Slow cleanup.** The teardown is on the request path. Anything genuinely slow belongs in a background task.

**Creating the pool per request.** A pool is startup work with a process lifetime; a session is request work. Rebuilding the pool per request is catastrophic for throughput, and sharing a session across requests is catastrophic for correctness.

## Sync or async

Both forms work, and the choice follows the resource.

`def get_session()` runs in the threadpool, which is right for a blocking driver - psycopg2, a synchronous HTTP client, a file.

`async def get_session()` runs on the event loop, which is right for an async driver - asyncpg, httpx's async client.

Mixing is allowed: an async handler may depend on a sync yield dependency and the other way round. What matters is that a blocking call is not made directly on the loop, which is the runtime tier's subject.


## How it works underneath

Knowing the mechanism removes most of the surprises.

A `yield` dependency is a generator. FastAPI wraps it in a context manager and enters it before calling the handler, holding it open in an `AsyncExitStack` that lives for the request. When the response has been produced, the stack unwinds and every context manager exits in reverse order.

That is why teardown ordering is reverse, why teardown runs on failure, and why raising in teardown is awkward: the stack is unwinding while the response is already on its way out.

It also explains the lifetime precisely. The dependency is alive for the whole request, including while the response is being serialised - so a session yielded here is still usable by a response model reading lazy attributes, which is a common source of confusion when it is *not* the case in other frameworks.

## A checklist

Before shipping a yield dependency, four questions.

Does it acquire something? Then the `yield` is inside a `try` and the release is in `finally`.

Can the handler fail? Then anything conditional on success sits between the `yield` and the `except`.

Can the cleanup fail? Then it is caught and logged, not raised.

Is this per-request, or per-process? A session is per request; the pool it comes from is not.

## One more thing to watch

A subtle one, worth knowing before it bites.

The dependency stays open while the **response is serialised**, not just while the handler runs. A session yielded here is still alive when a response model reads an attribute that triggers a lazy load.

That is convenient, and it is also how a single serialisation quietly becomes fifty queries: the model touches a relationship, the session is still open, and the ORM obliges. The fix is on the query side - load what the response needs up front - but the reason it is possible at all is this lifetime.

It is also why closing the session inside the handler is a mistake that appears to work. The handler returns fine; the serialiser then finds a closed session, and the error names neither.

## Summary

Code before the `yield` is setup, the yielded value is what the handler receives, and code after it runs once the response has been produced - on success and on failure alike.

Wrap the `yield` in `try/finally` whenever anything is acquired. Put `commit()` immediately after it and `rollback()` in an `except` that re-raises, and the transaction pattern falls out in three lines.

Teardowns run in reverse order, the per-request cache still applies, and nothing in the teardown should raise or be slow.


## Summary, in one line

Setup before the `yield`, teardown after it, `try/finally` around it whenever anything is acquired - and `commit()` immediately after the `yield` so that only a successful handler reaches it.

Everything else in this module is a consequence of those four facts.


## A closing thought

Almost every resource bug in a web application is a lifetime bug: something opened and not closed, closed too early, or shared between requests that should not share it.

`yield` dependencies exist to make the common lifetime - one request - the easy one to express. Setup, use, teardown, in one function, applied by declaring a parameter.

The failure modes it removes are the ones that do not show up in development: a connection leaked on the error path, a transaction left open, a pool exhausted an hour after deploy under real traffic.


## Two rules

Everything here reduces to two.

**Wrap the `yield` in `try/finally` whenever the dependency acquires anything.** That single line is the difference between a pool that survives a bad afternoon and one that does not.

**Put success-only work between the `yield` and the `except`.** That is where `commit()` goes, and it is why the transaction pattern needs no flag, no inspection of the response, and no cooperation from the handler.


## Where it sits in the tier

Of the five modules here, this is the one whose absence causes production incidents rather than inconvenience.

A missing `Depends` is a repeated four lines. A missing `try/finally` is a connection pool that empties under load on the error path, which is the path that gets busy exactly when everything else is going wrong.

## Next

Dependencies that depend on dependencies, the tree FastAPI resolves before your handler runs, and why a shared node in that tree is still only called once.
''',
    [
        {"q": "When does the code after `yield` run?",
         "options": ["Immediately", "After the response has been produced", "Only on success", "Never"],
         "answer": 1,
         "why": "Setup, then handler, then teardown - which is why it works for anything with a request-scoped lifetime."},
        {"q": "A handler raises a 404. Does the teardown run?",
         "options": ["No", "Yes, if the yield is inside a try/finally", "Only for 500s", "Only for async dependencies"],
         "answer": 1,
         "why": "That is the reason to use yield rather than a plain return. Without `try/finally` a failing handler skips the close and leaks the connection."},
        {"q": "Where does `db.commit()` belong in the transaction pattern?",
         "options": ["Before the yield", "Immediately after the yield", "In finally", "In the handler"],
         "answer": 1,
         "why": "It is only reached when the handler completed without raising. An `except` clause rolls back and re-raises; `finally` closes either way."},
        {"q": "Cleanup itself fails. What should the teardown do?",
         "options": ["Raise", "Catch and log it", "Return a 500", "Retry forever"],
         "answer": 1,
         "why": "The response is already decided and being sent, so an exception there cannot become a clean error - and may truncate the response instead."},
    ],
)


# ---------------------------------------------------------------------------
# 16. Sub-dependencies
# ---------------------------------------------------------------------------
topic(
    "sub_dependencies",
    "Sub-dependencies",
    "Dependencies",
    "Dependencies that depend on dependencies, and the tree FastAPI resolves "
    "before your handler runs.",
    _svg(_box(54, 12, 52, 18, S, A) + _txt(80, 25, "handler", A, 8) +
         _arrow(70, 32, 42, 44) + _arrow(90, 32, 118, 44) +
         _box(16, 46, 52, 18, S) + _txt(42, 59, "user", M, 8) +
         _box(92, 46, 52, 18, S) + _txt(118, 59, "db", M, 8) +
         _arrow(42, 66, 42, 76) + _txt(42, 88, "token", M, 7)),
    [
        ("A dependency can declare its own",
         "Exactly the same syntax, one level down. FastAPI resolves the whole tree "
         "before the handler is called.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
USERS = {"tok-ada": {"name": "ada", "role": "admin"}}

def token(authorization: str = Header(default="")):
    return authorization.replace("Bearer ", "")

def current_user(tok: str = Depends(token)):
    if tok not in USERS:
        raise HTTPException(401, "Sign in first")
    return USERS[tok]

def admin_only(user: dict = Depends(current_user)):
    if user["role"] != "admin":
        raise HTTPException(403, "Admins only")
    return user

@app.delete("/modules/{i}")
def remove(i: int, user: dict = Depends(admin_only)):
    return {"deleted": i, "by": user["name"]}

c = TestClient(app)
print(c.request("DELETE", "/modules/7",
                headers={"authorization": "Bearer tok-ada"}).json())
print("no token:", c.request("DELETE", "/modules/7").status_code)'''),

        ("The tree is resolved once",
         "A shared sub-dependency deep in the tree is still called a single time per "
         "request.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
calls = []

def base():
    calls.append("base")
    return "B"

def left(b: str = Depends(base)):  return "L(%s)" % b
def right(b: str = Depends(base)): return "R(%s)" % b

@app.get("/x")
def x(l: str = Depends(left), r: str = Depends(right), b: str = Depends(base)):
    return {"l": l, "r": r, "b": b, "base_calls": len(calls)}

print(TestClient(app).get("/x").json())
print()
print("Three paths reach base; it ran once. That is why the cache matters.")'''),

        ("Failures short-circuit the tree",
         "If a sub-dependency raises, nothing below it or after it runs &mdash; "
         "including the handler.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
ran = []

def token(authorization: str = Header(default="")):
    ran.append("token")
    tok = authorization.replace("Bearer ", "")
    if not tok:
        raise HTTPException(401, "No token")
    return tok

def profile(tok: str = Depends(token)):
    ran.append("profile")
    return {"tok": tok}

@app.get("/me")
def me(p: dict = Depends(profile)):
    ran.append("handler")
    return p

c = TestClient(app)
r = c.get("/me")
print("no token:", r.status_code, "| ran:", ran)
ran.clear()
r = c.request("GET", "/me", headers={"authorization": "Bearer abc"})
print("token   :", r.status_code, "| ran:", ran)'''),

        ("Layering permissions",
         "The natural use: each level adds one check, and an endpoint declares the "
         "level it needs.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
USERS = {"a": {"name": "ada", "role": "admin"},
         "r": {"name": "rex", "role": "reader"}}

def current_user(x_token: str = Header(default="")):
    if x_token not in USERS:
        raise HTTPException(401, "Sign in")
    return USERS[x_token]

def verified(user: dict = Depends(current_user)):
    return user                      # a real one would check a flag

def admin(user: dict = Depends(verified)):
    if user["role"] != "admin":
        raise HTTPException(403, "Admins only")
    return user

@app.get("/public")
def public(): return {"level": "public"}

@app.get("/account")
def account(u: dict = Depends(verified)): return {"level": "verified", "you": u["name"]}

@app.get("/admin")
def admin_page(u: dict = Depends(admin)): return {"level": "admin", "you": u["name"]}

c = TestClient(app)
for path in ["/public", "/account", "/admin"]:
    for tok in ["", "r", "a"]:
        h = {"x-token": tok} if tok else {}
        print("%-9s tok=%-2s -> %s" % (path, tok or "-",
              c.request("GET", path, headers=h).status_code))'''),

        ("Parameters gather from the whole tree",
         "Every parameter any dependency declares becomes the endpoint's, and every "
         "one is documented.",
         '''from fastapi import Depends, FastAPI, Header, Query

app = FastAPI()

def paging(limit: int = Query(default=10, le=100)):
    return limit

def locale(x_locale: str = Header(default="en")):
    return x_locale

def context(limit: int = Depends(paging), loc: str = Depends(locale),
            q: str = Query(default="")):
    return {"limit": limit, "locale": loc, "q": q}

@app.get("/search")
def search(ctx: dict = Depends(context)):
    return ctx

c = TestClient(app)
print(c.request("GET", "/search?q=vectors&limit=5",
                headers={"x-locale": "fr"}).json())
print()
for p in app.openapi()["paths"]["/search"]["get"]["parameters"]:
    print("  %-9s in %s" % (p["name"], p["in"]))'''),

        ("Depth worth keeping",
         "Three levels reads well. Beyond that the endpoint's signature stops "
         "telling you what it actually needs.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
trace = []

def a():                       trace.append("a"); return "a"
def b(x: str = Depends(a)):    trace.append("b"); return x + "b"
def c_(x: str = Depends(b)):   trace.append("c"); return x + "c"
def d(x: str = Depends(c_)):   trace.append("d"); return x + "d"
def e(x: str = Depends(d)):    trace.append("e"); return x + "e"

@app.get("/deep")
def deep(v: str = Depends(e)):
    return {"value": v, "order": trace}

print(TestClient(app).get("/deep").json())
print()
print("It works. But 'deep' declares one parameter and needs five functions,")
print("and nothing in its signature says so.")'''),
    ],
    [
        "A dependency declares its own dependencies with the same syntax. FastAPI resolves the whole tree before calling the handler.",
        "The per-request cache covers the tree, so a shared node reached by several paths is still called once.",
        "A raise anywhere in the tree short-circuits everything below and after it, including the handler.",
        "Layered permission checks are the natural use: each level adds one rule and an endpoint declares the level it needs.",
        "Every parameter declared anywhere in the tree becomes the endpoint's parameter, and appears in the documentation.",
        "Keep the tree shallow. Three levels reads well; five means the signature no longer tells a reader what the endpoint needs.",
    ],
    '''
title: Sub-dependencies
intro: Dependencies that depend on dependencies, and the tree resolved before your handler runs.
## The same syntax, one level down

A dependency is a function whose parameters are request parameters &mdash; and `Depends` is a request parameter. So a dependency can depend on another:

```python
def token(authorization: str = Header(default="")):
    return authorization.replace("Bearer ", "")

def current_user(tok: str = Depends(token)):
    ...

def admin_only(user: dict = Depends(current_user)):
    ...
```

There is no new mechanism here. FastAPI walks the tree from the handler's signature down, calls each function in dependency order, and passes the results up.

## The cache covers the tree

This is where per-request caching stops being an optimisation and becomes load-bearing.

In a realistic application, `current_user` is depended on by `permissions`, which is depended on by `admin_only`, and the handler may declare two of those directly. Without caching the token would be decoded three or four times per request.

With it, once. The second editor above makes that visible: three separate paths reach `base`, and it runs a single time.

## Failures short-circuit

If any dependency raises, everything below and after it is skipped, including the handler.

That is what makes layered checks safe. `admin_only` can assume `current_user` succeeded, because it only runs if it did. There is no need to check for `None` or re-verify &mdash; the tree guarantees ordering.

It is also why authentication as a dependency is genuinely safer than a check in the handler. A handler can forget to check. A signature cannot: if the endpoint declares `admin_only`, the check ran.

## Layering permissions

The pattern this shape is built for:

`current_user` &mdash; who is this? 401 if unknown.
`verified` &mdash; are they confirmed? 403 if not.
`admin` &mdash; are they an admin? 403 if not.

Each depends on the previous and adds exactly one rule. An endpoint then declares the level it needs, and the level is visible in its signature.

The alternative &mdash; one `check_permissions(level="admin")` function with branching inside &mdash; works and hides the rules in a body rather than showing them in a chain. The layered version is easier to read and much easier to extend, because adding a level is a new function rather than a new branch.

## Parameters gather upward

Every parameter declared anywhere in the tree becomes a parameter of the endpoint.

If `paging` declares `limit`, `locale` declares an `x-locale` header, and `context` declares `q` and depends on both, then an endpoint depending on `context` accepts all three &mdash; validated, converted, and documented.

That is worth appreciating: the abstraction is not opaque. A caller reading your OpenAPI document sees every parameter the endpoint really takes, however deep in the tree it was declared. Nothing is hidden by the indirection.

The corollary is that a dependency adding a parameter changes the public contract of every endpoint using it. Adding a *required* one is a breaking change for all of them at once, which is worth remembering before doing it casually.

## How deep to go

Three levels is comfortable and common. Five is not.

The problem at depth is not correctness &mdash; the last editor above works fine. It is that the endpoint's signature stops being informative. `def deep(v: str = Depends(e))` tells a reader nothing about the five functions that must succeed, the parameters they collectively declare, or the errors they can raise.

Two habits keep it readable.

**Name for the guarantee, not the mechanism.** `admin_only` says what the endpoint gets; `check_role_after_verifying_token` describes plumbing.

**Flatten when a chain has no branch.** If `a` is only ever used by `b` and `b` only by `c`, the three may be one function with a clear name. The chain earns its keep when levels are reused independently.

## Debugging one

When a dependency does not behave as expected, the useful question is *ordering*: what ran before it, and did anything above it raise?

A `print` at the top of each function shows the resolution order immediately, and the order is deterministic &mdash; there is no concurrency within one request's tree.

The other common surprise is caching: a dependency that appears to run once when you expected twice is the cache doing its job, and `use_cache=False` is the switch.


## Mistakes people make

**Building a deep chain because it composes.** It does compose, and five levels means the endpoint's signature no longer says what it needs. Three is comfortable.

**Naming for the mechanism.** `check_role_after_verifying_token` describes plumbing; `admin_only` describes the guarantee the handler receives.

**Flattening nothing.** If `a` is only used by `b` and `b` only by `c`, they are one function with a clear name. A chain earns its keep when the levels are reused independently.

**Adding a required parameter to a shared dependency.** It becomes required on every endpoint in the tree at once - a breaking change for all of them, made in one line that mentions none of them.

**Assuming order without checking.** The resolution order is deterministic, and a `print` at the top of each function shows it in seconds. That is faster than reasoning about it.

**Forgetting the cache when debugging.** A dependency that appears to run once when you expected twice is the cache working. `use_cache=False` is the switch.

## What the tree is really for

The layered-permission shape is the case that justifies the feature.

Each level answers one question and can assume the previous one passed, because a raise short-circuits everything after it. `admin` never has to check whether `current_user` returned `None`, because if it had raised, `admin` would not be running.

That guarantee is what makes it safe to put security in the dependency tree rather than in handlers. A handler can forget a check. A signature cannot: if the endpoint declares `admin`, the whole chain above it ran and passed.


## Reading a tree you did not write

Arriving at an unfamiliar codebase, the dependency tree is one of the fastest ways to understand what the endpoints assume.

Start at a handler's signature and follow the names down. Each level tells you one requirement, and the leaves are where the application touches the outside world - a header, a database, a clock, a configuration value.

Two things that reading reveals quickly. Whether security is enforced consistently: if half the endpoints declare `current_user` and half read the header themselves, the second half are where the bugs are. And where the boundaries are: the leaves of the tree are the places to fake in tests, and if there are many, the application is entangled with more of the world than it needs.

## Cost

Every dependency in the tree is a function call per request, and the tree is resolved before the handler runs.

For the ordinary case - a handful of small functions - the cost is nothing next to a single query. It becomes visible in two situations: a dependency doing real work, such as a lookup, that is now multiplied across every endpoint sharing it; and a very wide tree where the sheer number of calls adds up under load.

Neither is a reason to avoid the feature. Both are reasons to know what is in the tree, because a slow dependency near the root is slow for everything, and its cost does not appear in any single endpoint's code.

## A worked permission chain

Written out in full, because this is the shape most applications converge on.

```python
def bearer_token(authorization: str = Header(default="")) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer token")
    return authorization[7:]

def current_user(token: str = Depends(bearer_token)) -> User:
    user = decode(token)
    if user is None:
        raise HTTPException(401, "Invalid token")
    return user

def active_user(user: User = Depends(current_user)) -> User:
    if user.disabled:
        raise HTTPException(403, "Account disabled")
    return user

def admin(user: User = Depends(active_user)) -> User:
    if not user.is_admin:
        raise HTTPException(403, "Admins only")
    return user
```

Four functions, four rules, each one line of logic. An endpoint declares the level it needs and gets everything below it.

The properties worth noticing: each level has one reason to fail and one status; the token is decoded once however many levels are involved; and adding a rule - two-factor verified, subscription active - is a new function in the chain rather than a new branch inside an existing one.

That is what the tree is for. Not composition for its own sake, but a set of requirements that can be stated separately, reused independently, and read from an endpoint's signature.


## Cost and shape

Every node in the tree is a function call per request, resolved before the handler runs.

For a handful of small functions that is nothing beside a single query. It becomes visible in two situations worth watching: a dependency that does real work sitting near the root, where its cost is multiplied by every endpoint below it; and a very wide tree under load, where the call count itself adds up.

Neither argues against the feature. Both argue for knowing what is in the tree, because a slow dependency high up is slow for everything and its cost appears in no single endpoint's code.

## Reading an unfamiliar one

The tree is also the fastest way into a codebase you did not write.

Start at a handler's signature and follow the names down. Each level names one requirement; the leaves are where the application touches the outside world.

Two things that reading reveals immediately. Whether security is applied consistently - if half the endpoints declare `current_user` and half read the header themselves, the second half is where the bugs live. And how entangled the application is - a wide set of leaves means many things must exist for any endpoint to run.

## Summary

A dependency declares its own dependencies with the same syntax, and FastAPI resolves the tree before the handler runs. The per-request cache covers the whole tree, so a shared node is called once however many paths reach it.

A raise anywhere short-circuits everything after it, which is what lets each level assume the previous one passed - and what makes declaring a check in a signature safer than remembering it in a handler.

Every parameter declared anywhere gathers upward into the endpoint's documented contract. Keep the tree about three levels deep, and name each level for the guarantee it provides.


## Summary, in one line

Dependencies compose with the same syntax, the tree resolves before the handler, a shared node runs once, a raise stops everything after it, and every parameter anywhere in the tree becomes part of the endpoint's public contract.


## A closing thought

A dependency tree is a description of what an endpoint assumes, written in a form the framework enforces.

That is a stronger guarantee than documentation and a cheaper one than tests. If the endpoint declares `admin`, then a request that reaches the handler came from an authenticated, active administrator - not because somebody remembered to check, but because the handler could not have run otherwise.

Keeping the tree shallow and naming each level for its guarantee is what keeps that description readable.


## Two rules

**Name each level for what it guarantees**, not for what it does. `admin` tells a reader what the handler receives; `check_role_after_token` describes the plumbing.

**Stop at about three levels.** The tree stays useful while a signature still implies what the endpoint needs, and stops being useful the moment it does not.

## Next

Attaching a dependency to a router or an application rather than a parameter, which is how a section gets a rule that a new route cannot escape.

A tree that reads well is one where each name is a noun or an adjective describing the caller - a user, an admin, an active account - rather than a verb describing the check. The handler is receiving a guarantee, not commissioning an inspection.
''',
    [
        {"q": "A sub-dependency is reached by three different paths in one request. How many times does it run?",
         "options": ["Three", "Once - the cache covers the whole tree", "Depends on order", "Once per path"],
         "answer": 1,
         "why": "In a real application `current_user` is reached several ways, and without the cache the token would be decoded repeatedly. This is where caching stops being an optimisation."},
        {"q": "A dependency in the middle of the tree raises. What runs after it?",
         "options": ["Everything else", "Nothing below or after it, including the handler", "Only the handler", "Only siblings"],
         "answer": 1,
         "why": "That short-circuit is what lets a later level assume an earlier one succeeded - and why declaring a check in the signature is safer than remembering it in a handler."},
        {"q": "A dependency three levels down declares a `limit` query parameter. Does it appear in the docs?",
         "options": ["No, it is internal", "Yes - as the endpoint's own parameter", "Only if re-declared", "Only headers appear"],
         "answer": 1,
         "why": "Parameters gather upward, so the indirection hides nothing from the contract - and adding a required one is a breaking change for every endpoint using that dependency."},
        {"q": "What is the problem with a five-level dependency chain?",
         "options": ["It is slow", "The endpoint's signature stops telling a reader what it needs", "It breaks caching", "It is not allowed"],
         "answer": 1,
         "why": "It works correctly. But one parameter standing for five functions, their parameters and their possible errors is no longer informative."},
    ],
)


# ---------------------------------------------------------------------------
# 17. Class dependencies
# ---------------------------------------------------------------------------
topic(
    "class_dependencies",
    "Class Dependencies",
    "Dependencies",
    "Anything callable works, which is how a dependency gets configuration of its "
    "own.",
    _svg(_box(14, 18, 60, 22, S) + _txt(44, 33, "Paginate(50)", M, 8) +
         _arrow(78, 29, 92, 29) +
         _box(96, 18, 50, 22, S, A) + _txt(121, 33, "Depends", A, 8) +
         _txt(80, 64, "one class, many configurations", M, 8)),
    [
        ("A class with __init__ is a dependency",
         "FastAPI reads <code>__init__</code>'s signature the way it reads a "
         "function's, and gives the handler the instance.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()

class Pagination:
    def __init__(self, limit: int = 10, offset: int = 0):
        self.limit = min(limit, 100)
        self.offset = offset

    def slice(self, rows):
        return rows[self.offset:self.offset + self.limit]

@app.get("/modules")
def list_modules(page: Pagination = Depends(Pagination)):
    rows = ["m%d" % i for i in range(20)]
    return {"limit": page.limit, "offset": page.offset, "rows": page.slice(rows)}

c = TestClient(app)
print(c.get("/modules?limit=3").json())
print(c.get("/modules?limit=3&offset=5").json())'''),

        ("The shorthand",
         "Because the class is both the type and the callable, "
         "<code>Depends()</code> with no argument uses the annotation.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()

class Pagination:
    def __init__(self, limit: int = 10, offset: int = 0):
        self.limit, self.offset = limit, offset

@app.get("/long")
def long_form(page: Pagination = Depends(Pagination)):
    return {"limit": page.limit}

@app.get("/short")
def short_form(page: Pagination = Depends()):
    return {"limit": page.limit}

c = TestClient(app)
print("long :", c.get("/long?limit=4").json())
print("short:", c.get("/short?limit=4").json())
print()
print("Same thing. The annotation supplies the callable.")'''),

        ("An instance is a configured dependency",
         "Give the class a <code>__call__</code> and instances become dependencies "
         "you can parameterise &mdash; one class, several rules.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
USERS = {"a": "admin", "r": "reader"}

class RequireRole:
    def __init__(self, role: str):
        self.role = role

    def __call__(self, x_token: str = Header(default="")):
        role = USERS.get(x_token)
        if role is None:
            raise HTTPException(401, "Sign in")
        if role != self.role:
            raise HTTPException(403, "Needs role %r" % self.role)
        return role

require_admin = RequireRole("admin")
require_reader = RequireRole("reader")

@app.get("/admin")
def admin(role: str = Depends(require_admin)): return {"role": role}

@app.get("/reading")
def reading(role: str = Depends(require_reader)): return {"role": role}

c = TestClient(app)
for path in ["/admin", "/reading"]:
    for tok in ["", "r", "a"]:
        h = {"x-token": tok} if tok else {}
        print("%-9s tok=%-2s -> %s" % (path, tok or "-",
              c.request("GET", path, headers=h).status_code))'''),

        ("A model as a dependency",
         "The class can be a Pydantic model, which gives the filters validation, "
         "constraints and a documented schema.",
         '''import json
from typing import Literal
from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class Filters(BaseModel):
    q: str = Field(default="", max_length=50)
    limit: int = Field(default=10, ge=1, le=100)
    sort: Literal["title", "minutes"] = "title"

def filters(
    q: str = Query(default="", max_length=50),
    limit: int = Query(default=10, ge=1, le=100),
    sort: Literal["title", "minutes"] = "title",
) -> Filters:
    return Filters(q=q, limit=limit, sort=sort)

@app.get("/modules")
def list_modules(f: Filters = Depends(filters)):
    return f.model_dump()

c = TestClient(app)
print(c.get("/modules?q=vec&limit=5&sort=minutes").json())
print("bad sort:", c.get("/modules?sort=colour").status_code)
print()
for p in app.openapi()["paths"]["/modules"]["get"]["parameters"]:
    print("  %-6s %s" % (p["name"], json.dumps(p["schema"])[:60]))'''),

        ("Configuration decided once",
         "The instance is built at import, so its configuration is not per-request "
         "work &mdash; only <code>__call__</code> runs each time.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
built = []

class RateLimit:
    def __init__(self, per_minute: int):
        built.append(per_minute)           # runs once, at import
        self.per_minute = per_minute
        self.seen = 0

    def __call__(self):
        self.seen += 1
        return {"limit": self.per_minute, "calls": self.seen}

tight = RateLimit(5)
loose = RateLimit(100)

@app.get("/tight")
def a(r: dict = Depends(tight)): return r

@app.get("/loose")
def b(r: dict = Depends(loose)): return r

c = TestClient(app)
print(c.get("/tight").json()); print(c.get("/tight").json())
print(c.get("/loose").json())
print()
print("constructed:", built, "- twice, at import, not per request")'''),

        ("When a function is enough",
         "A class earns its place when there is configuration or state. Without "
         "either, it is a function with extra ceremony.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()

# No configuration, no state - a function says it more plainly.
def pagination(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset}

class PaginationClass:
    def __init__(self, limit: int = 10, offset: int = 0):
        self.limit, self.offset = limit, offset

@app.get("/fn")
def fn(p: dict = Depends(pagination)): return p

@app.get("/cls")
def cls(p: PaginationClass = Depends()): return {"limit": p.limit, "offset": p.offset}

c = TestClient(app)
print("function:", c.get("/fn?limit=3").json())
print("class   :", c.get("/cls?limit=3").json())
print()
print("Identical behaviour. Reach for the class when it holds something.")'''),
    ],
    [
        "Any callable works. A class is a dependency because calling it constructs an instance, and FastAPI reads <code>__init__</code>'s signature for parameters.",
        "<code>Depends()</code> with no argument uses the parameter's annotation as the callable &mdash; the shorthand for a class dependency.",
        "Give a class <code>__call__</code> and its <em>instances</em> become dependencies, which is how one class produces several configured rules.",
        "The instance is built at import, so configuration is not per-request work; only <code>__call__</code> runs each time.",
        "A dependency can return a Pydantic model, which gives the result validation, constraints and a documented schema.",
        "Prefer a function when there is no configuration and no state. A class without either is ceremony.",
    ],
    '''
title: Class Dependencies
intro: Anything callable works, which is how a dependency gets configuration of its own.
## Callables, not functions

`Depends` takes a callable. A function is the obvious one; a class is a callable too, because calling it constructs an instance.

```python
class Pagination:
    def __init__(self, limit: int = 10, offset: int = 0):
        self.limit = min(limit, 100)
        self.offset = offset

def list_modules(page: Pagination = Depends(Pagination)):
    ...
```

FastAPI reads `__init__`'s signature exactly as it reads a function's: `limit` and `offset` become query parameters, validated and documented. The handler receives the instance.

Because the annotation and the callable are the same thing, there is a shorthand:

```python
def list_modules(page: Pagination = Depends()):
```

## What a class buys

Two things a function cannot easily give you.

**Methods.** The instance can carry behaviour, not just data. `page.slice(rows)` keeps the pagination logic with the pagination parameters, rather than repeating the arithmetic in every handler.

**Configuration**, via `__call__`.

## Configured instances

This is the pattern worth knowing, and it is the main reason to reach for a class:

```python
class RequireRole:
    def __init__(self, role: str):
        self.role = role

    def __call__(self, x_token: str = Header(default="")):
        ...

require_admin = RequireRole("admin")
require_reader = RequireRole("reader")
```

Now `Depends(require_admin)` and `Depends(require_reader)` are two dependencies from one class. `__init__` takes your configuration; `__call__` takes the request parameters.

The alternative with plain functions is a factory returning a closure, which works and reads less clearly:

```python
def require_role(role):
    def dep(x_token: str = Header(default="")):
        ...
    return dep
```

Both are used in real code. The class version keeps the configuration visible as attributes and gives you somewhere to put related helpers.

## When the construction happens

Worth being precise about, because it affects what belongs where.

`RequireRole("admin")` runs **at import**, once. `__call__` runs **per request**.

So expensive setup belongs in `__init__` &mdash; compiling a regular expression, loading a rules table, reading configuration. Per-request work belongs in `__call__`.

The instance is shared across requests, which means any state you keep on it is shared too. That is fine for configuration and a genuine hazard for anything mutable: a counter on the instance counts across all requests and all users, and in a multi-worker deployment counts per worker, which is almost never what someone wanted from a rate limiter.

If a dependency needs per-request state, return it from `__call__` rather than storing it on `self`.

## Returning a model

A dependency's return value can be anything, and a Pydantic model is often the right choice for a group of filters:

```python
def filters(q: str = Query(default=""), limit: int = Query(default=10, le=100)) -> Filters:
    return Filters(q=q, limit=limit)
```

The handler then gets attribute access, editor completion and a typed object rather than a dictionary. The parameters are still declared individually, so they still appear in the documentation as query parameters &mdash; which is what a caller needs to see.

There is a temptation to annotate the parameter with the model directly and skip the function. Resist it: a model parameter means a request *body*, and on a GET that is not what you want.

## Function or class?

The question that settles it: **does it hold anything?**

If the dependency is "read these parameters and hand them over", a function is plainer and shorter.

If it has configuration decided at import, methods worth keeping beside the data, or a family of related variants, a class earns its keep.

Most dependencies in most applications are functions. The class form is for the handful that are parameterised &mdash; permissions, rate limits, feature gates &mdash; and it is worth knowing precisely so you recognise the shape when you need it.

## With Annotated

Everything here composes with the `Annotated` spelling:

```python
AdminUser = Annotated[User, Depends(require_admin)]

def remove(i: int, user: AdminUser):
    ...
```

The dependency becomes a named type, the signature reads as ordinary Python, and the requirement is stated in one place that every endpoint can reuse. For a codebase with several permission levels this is the tidiest form available.


## Mistakes people make

**Keeping mutable state on the instance.** It is shared across every request, and in a multi-worker deployment it is per worker. A counter there counts something nobody wanted. Per-request state belongs in what `__call__` returns.

**Expensive work in `__call__`.** That runs per request. Compiling a pattern or loading a table belongs in `__init__`, which runs once at import.

**Annotating the parameter with a Pydantic model directly.** A model annotation means a request *body*. For query filters, declare the parameters in a function and construct the model inside it.

**A class with no configuration and no state.** That is a function with extra ceremony. Reach for the class when it holds something.

**Forgetting `__call__` and wondering why the instance is not a dependency.** `Depends(SomeClass)` calls the class; `Depends(some_instance)` calls the instance, and an instance is only callable if the class defines `__call__`.

## Factory function or class?

Both produce configured dependencies, and both appear in real code.

A **closure factory** is shorter for one small rule:

```python
def require_role(role):
    def dep(x_token: str = Header(default="")):
        ...
    return dep
```

A **class** keeps the configuration visible as attributes, gives related helpers somewhere to live, and is easier to inspect in a debugger.

For one parameter and three lines, the closure. For a family of rules with shared helpers, the class.


## A worked family

The shape that justifies the class form, written out once.

```python
class RequireScope:
    def __init__(self, *scopes):
        self.scopes = set(scopes)

    def __call__(self, user: User = Depends(current_user)):
        missing = self.scopes - set(user.scopes)
        if missing:
            raise HTTPException(403, "Missing scope(s): %s" % ", ".join(sorted(missing)))
        return user

read_modules = RequireScope("modules:read")
write_modules = RequireScope("modules:read", "modules:write")
```

One class, one rule, and as many configured dependencies as the application has permission levels. Each endpoint declares the one it needs, and the declaration is readable: `Depends(write_modules)` says what the endpoint requires without opening anything.

Adding a scope is a new module-level name. Changing how scopes are checked is one method. Neither touches an endpoint.

## Instances are shared

Because `read_modules` is created at import, it is one object shared by every request that reaches an endpoint declaring it.

That is what makes it cheap, and it is the constraint to respect: the instance may hold configuration, and it must not hold anything about a particular request. If you find yourself assigning to `self` inside `__call__`, the value belongs in the return instead.

The same applies across workers. Each process has its own instance, so anything accumulated on `self` is per process rather than per application - which is why an instance attribute is the wrong place for a rate-limit counter, and a shared store is the right one.

## Where the instance lives

One more consequence of construction happening at import, because it decides where these belong in a project.

`require_admin = RequireRole("admin")` is a module-level name. It is created when the module is imported, shared by every request, and referenced by every endpoint that needs it. That makes `dependencies.py` its natural home, beside the plain functions.

Two practical effects follow.

**Import order matters slightly.** Anything the constructor reads - a setting, an environment variable - must be available at import. If it is not, the failure is at startup rather than at request time, which is the better of the two, but it means configuration has to be loaded before dependencies are imported.

**Reloading in development recreates them.** With `--reload`, saving a file rebuilds the instances and discards whatever they held. That is invisible for configuration and confusing for anything stateful, which is one more argument for keeping state off `self`.

## When the parameters differ per endpoint

A related pattern worth recognising: sometimes the configuration is not fixed at import but supplied per route.

The class form handles it, because each endpoint can construct its own:

```python
@app.get("/small", dependencies=[Depends(RateLimit(5))])
@app.get("/large", dependencies=[Depends(RateLimit(500))])
```

Each decorator builds an instance at import, one per route, which is exactly the same mechanism with a shorter lifetime for the name. It reads well for a rule that varies numerically across endpoints, and less well once the configuration is more than a value or two - at which point a named instance is clearer than an inline construction.


## The three forms side by side

All three produce a configured dependency. Choosing between them is mostly about how much the configuration carries.

**A plain function**, when there is nothing to configure. `def pagination(limit: int = 10)` is the whole thing, and any other form is ceremony around it.

**A closure factory**, when one small value varies. Short, and the configuration is a captured local nobody can inspect.

**A class with `__call__`**, when the configuration is worth naming, several rules share helpers, or you want the instance to be inspectable. `RequireScope("modules:write").scopes` is readable in a debugger; a closure's captured variable is not.

The progression is worth following in that order. Start with the function, reach for the factory when a value varies, and reach for the class when the factory starts growing a second function beside it.

## What a class must not do

One rule, stated plainly, because breaking it produces bugs that only appear under load.

The instance is created once and shared by every request in that worker. Anything written to `self` during `__call__` is shared state across concurrent requests and separate state across workers.

For configuration that is exactly right - it is read-only and identical everywhere. For anything per-request it is wrong twice over: two requests interleave, and two workers disagree.

If `__call__` needs to produce something request-specific, it returns it. That is what the handler receives, and it is the only value with the right lifetime.

## Summary

`Depends` takes any callable, so a class is a dependency: FastAPI reads `__init__` for parameters and hands the handler the instance. `Depends()` with no argument uses the annotation.

Give the class `__call__` and its instances become configured dependencies - one class, a family of rules, each declared by name at the endpoints that need it. `__init__` runs once at import; `__call__` runs per request, and nothing request-specific should be stored on `self`.

Reach for a function when there is no configuration, no state and no behaviour to keep beside the data.


## Summary, in one line

Use a function until the dependency has configuration; then use a class whose `__init__` takes the configuration and whose `__call__` takes the request - remembering that the instance is built once and shared, so nothing about a single request may live on it.


## A closing thought

The class form is the least-used part of this tier and the one worth recognising rather than reaching for.

Most dependencies are functions and should stay functions. But when an application grows several variants of one rule - three permission levels, four rate limits, five feature gates - writing five near-identical functions is worse than writing one class and five names.

The signal is duplication with one value changed. That is what `__init__` is for.


## Two rules

**Configuration in `__init__`, request handling in `__call__`.** The first runs once at import; the second runs per request.

**Nothing about a single request on `self`.** The instance is shared across every concurrent request in the worker and duplicated across workers, so anything stored there is both a race and a lie. Return it instead.


## Where it sits in the tier

This is the smallest module of the five, and deliberately so.

Function dependencies cover the overwhelming majority of real use. Sub-dependencies handle composition. `yield` handles lifetime. Router-level handles scope. Overrides handle testing.

The class form fills one specific gap: a rule that is the same shape at several settings. Recognising that gap - and not reaching for a class before you are in it - is the whole lesson.

## Next

Applying a dependency to a whole router or the entire application, so that a section is protected without every endpoint repeating the declaration - and without a route added later quietly missing it.
''',
    [
        {"q": "Why is a class a valid dependency?",
         "options": ["FastAPI special-cases classes", "Depends takes any callable, and calling a class constructs an instance", "Only Pydantic models work", "It is not"],
         "answer": 1,
         "why": "FastAPI reads `__init__`'s signature the way it reads a function's, so its parameters become request parameters and the handler receives the instance."},
        {"q": "What does `Depends()` with no argument use?",
         "options": ["The first dependency", "The parameter's type annotation as the callable", "Nothing", "The handler name"],
         "answer": 1,
         "why": "For a class dependency the annotation and the callable are the same thing, so the argument is redundant."},
        {"q": "When does `RequireRole(\"admin\")` run?",
         "options": ["Per request", "Once at import; only `__call__` runs per request", "Never", "Once per worker per request"],
         "answer": 1,
         "why": "Configuration belongs in `__init__` and per-request work in `__call__`. The instance is shared across requests, so mutable state on `self` is shared too."},
        {"q": "When is a plain function the better choice?",
         "options": ["Always", "When the dependency holds no configuration, state or methods", "Never", "Only for headers"],
         "answer": 1,
         "why": "Most dependencies just read parameters and hand them over. A class without configuration or behaviour is the same thing with more ceremony."},
    ],
)


# ---------------------------------------------------------------------------
# 18. Router and global dependencies
# ---------------------------------------------------------------------------
topic(
    "router_and_global_dependencies",
    "Router and Global Dependencies",
    "Dependencies",
    "Protecting a whole section without every endpoint repeating the declaration - "
    "and the one endpoint that would otherwise forget.",
    _svg(_box(20, 14, 120, 18, S, A) + _txt(80, 27, "APIRouter(dependencies=[...])", A, 7) +
         _arrow(50, 34, 50, 44) + _arrow(110, 34, 110, 44) +
         _box(18, 46, 60, 18, S) + _txt(48, 59, "/admin/stats", M, 7) +
         _box(84, 46, 60, 18, S) + _txt(114, 59, "/admin/cache", M, 7)),
    [
        ("A dependency on the router",
         "Declared once, applied to every route in it. The value is not injected &mdash; "
         "it runs for its effect.",
         '''from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

def require_key(x_api_key: str = Header(default="")):
    if x_api_key != "k-secret":
        raise HTTPException(401, "Bad or missing key")
    return x_api_key

admin = APIRouter(prefix="/admin", dependencies=[Depends(require_key)])

@admin.get("/stats")
def stats(): return {"modules": 30}

@admin.delete("/cache")
def clear(): return {"cleared": True}

app = FastAPI()
app.include_router(admin)

c = TestClient(app)
good = {"x-api-key": "k-secret"}
print("no key   :", c.get("/admin/stats").status_code)
print("bad key  :", c.request("GET", "/admin/stats", headers={"x-api-key": "x"}).status_code)
print("stats    :", c.request("GET", "/admin/stats", headers=good).json())
print("cache    :", c.request("DELETE", "/admin/cache", headers=good).json())'''),

        ("Application-wide",
         "The same list on <code>FastAPI()</code> applies to every route in the app, "
         "including ones added later.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

def require_key(x_api_key: str = Header(default="")):
    if x_api_key != "k-secret":
        raise HTTPException(401, "Bad or missing key")

app = FastAPI(dependencies=[Depends(require_key)])

@app.get("/a")
def a(): return {"route": "a"}

@app.get("/b")
def b(): return {"route": "b"}

c = TestClient(app)
print("no key:", c.get("/a").status_code, c.get("/b").status_code)
h = {"x-api-key": "k-secret"}
print("keyed :", c.request("GET", "/a", headers=h).json(),
      c.request("GET", "/b", headers=h).json())'''),

        ("On a single route",
         "The decorator takes the same list, for a rule that applies to one endpoint "
         "and whose value the handler does not need.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
audit = []

def record(x_actor: str = Header(default="anonymous")):
    audit.append(x_actor)

@app.delete("/modules/{i}", dependencies=[Depends(record)])
def remove(i: int):
    return {"deleted": i}

@app.get("/modules/{i}")
def read(i: int):
    return {"id": i}

c = TestClient(app)
c.request("DELETE", "/modules/1", headers={"x-actor": "ada"})
c.request("DELETE", "/modules/2")
c.get("/modules/3")
print("audit trail:", audit, "<- reads are not recorded")'''),

        ("The value is not passed",
         "That is the trade. A handler needing the user declares its own "
         "<code>Depends</code>, and the cache means it still runs once.",
         '''from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

calls = []

def current_user(x_token: str = Header(default="")):
    calls.append(x_token)
    if x_token != "tok":
        raise HTTPException(401, "Sign in")
    return {"name": "ada"}

router = APIRouter(dependencies=[Depends(current_user)])

@router.get("/who")
def who(user: dict = Depends(current_user)):     # declared again, to use it
    return {"user": user["name"], "auth_calls": len(calls)}

@router.get("/ping")
def ping():                                      # protected, does not need it
    return {"ok": True}

app = FastAPI(); app.include_router(router)
c = TestClient(app)
h = {"x-token": "tok"}
print(c.request("GET", "/who", headers=h).json())
calls.clear()
print(c.request("GET", "/ping", headers=h).json(), "| auth calls:", len(calls))'''),

        ("They stack",
         "App, router and route dependencies all run, outermost first. Each layer "
         "adds a rule rather than replacing one.",
         '''from fastapi import APIRouter, Depends, FastAPI

order = []

def app_level():    order.append("app")
def router_level(): order.append("router")
def route_level():  order.append("route")

router = APIRouter(prefix="/x", dependencies=[Depends(router_level)])

@router.get("/y", dependencies=[Depends(route_level)])
def y():
    order.append("handler")
    return {"order": list(order)}

app = FastAPI(dependencies=[Depends(app_level)])
app.include_router(router)

print(TestClient(app).get("/x/y").json())'''),

        ("The endpoint that would have forgotten",
         "The argument for putting it on the router: a new route added later is "
         "protected without anyone remembering to protect it.",
         '''from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

def require_key(x_api_key: str = Header(default="")):
    if x_api_key != "k":
        raise HTTPException(401, "No key")

# Protected as a group.
grouped = APIRouter(prefix="/g", dependencies=[Depends(require_key)])
@grouped.get("/one")
def g1(): return {"r": 1}
@grouped.get("/two")                      # added later; still protected
def g2(): return {"r": 2}

# Protected one at a time.
each = APIRouter(prefix="/e")
@each.get("/one", dependencies=[Depends(require_key)])
def e1(): return {"r": 1}
@each.get("/two")                         # somebody forgot
def e2(): return {"r": 2}

app = FastAPI(); app.include_router(grouped); app.include_router(each)
c = TestClient(app)
for p in ["/g/one", "/g/two", "/e/one", "/e/two"]:
    print("%-7s no key -> %s" % (p, c.get(p).status_code))'''),
    ],
    [
        "<code>dependencies=[Depends(fn)]</code> on an <code>APIRouter</code> applies to every route in it.",
        "The same argument works on <code>FastAPI()</code> for the whole application, and on a route decorator for one endpoint.",
        "The return value is <strong>not</strong> injected &mdash; these run for their effect. A handler that needs the value declares its own <code>Depends</code>.",
        "Because of per-request caching, declaring it twice still calls the function once.",
        "App, router and route dependencies stack and run outermost first. Each layer adds a rule.",
        "The real argument for the router form: a route added six months later is protected without anyone remembering to protect it.",
    ],
    '''
title: Router and Global Dependencies
intro: Protecting a section without every endpoint repeating itself - and the endpoint that would otherwise be forgotten.
## Three places to declare one

A dependency can be attached at three levels, all with the same argument:

```python
FastAPI(dependencies=[Depends(fn)])                 # every route
APIRouter(dependencies=[Depends(fn)])               # every route in it
@app.get("/x", dependencies=[Depends(fn)])          # one route
```

They stack. All three run for a request that matches, outermost first, and each adds a rule rather than replacing one.

## The value is not injected

This is the difference from a parameter-level `Depends`, and the one thing to remember.

A dependency declared this way runs for its **effect**. It can read headers, validate, raise, record an audit entry &mdash; but whatever it returns is discarded, because there is no parameter to receive it.

So a handler that actually needs the user still declares it:

```python
router = APIRouter(dependencies=[Depends(current_user)])

@router.get("/who")
def who(user: User = Depends(current_user)):
    ...
```

That looks like a duplicate and is not: per-request caching means the function runs **once**. The router-level declaration guarantees the check happens on every route; the parameter-level one gets the value where it is needed.

## The argument for the router form

It is not brevity. It is that a route added later is covered by default.

Protecting endpoints one at a time works perfectly until somebody adds the fourteenth one and does not know the convention, or knows it and is in a hurry. That endpoint is then unprotected, nothing fails, no test covers it because nobody wrote a test for a route they did not know needed one, and the gap is found later by someone who was looking.

The router form inverts that: forgetting is not possible, because the protection is a property of the section rather than of each endpoint. Adding a route to `/admin` makes it an admin route.

The last editor above shows both arrangements side by side, with one endpoint in each. The grouped one is safe; the individual one has a hole.

## When to use which level

**Application-wide** for cross-cutting concerns that genuinely apply to everything: request identifiers, tracing, a global rate limit. Be careful &mdash; a health check that now requires an API key is a common self-inflicted outage, and public endpoints stop being public. If more than a couple of routes need an exemption, this is the wrong level.

**Router-level** for a section with a shared rule. This is the sweet spot, and where most real use lives: `/admin` requires an admin, `/internal` requires a service token.

**Route-level** for a rule genuinely specific to one endpoint whose value the handler does not need &mdash; recording an audit entry, checking a feature flag, enforcing an idempotency key.

## What it does to the documentation

Parameters declared by these dependencies still appear on every affected endpoint, because as far as a caller is concerned the endpoint requires them.

So a router requiring an `x-api-key` header documents that header on all of its routes. That is right, and it is a small argument for the router form over middleware, which would enforce the same rule invisibly.

The `responses=` argument pairs with this: a router that can 401 should say so once, at the router, rather than on each route.

## Dependencies or middleware?

Both can enforce something across many routes, and the choice comes up as soon as either does.

**A dependency** knows about routing, so it applies to a chosen set. It can declare parameters, which appear in the schema. It integrates with the error handling you already have, and it can be overridden in tests. It runs after routing, so it knows which endpoint matched.

**Middleware** runs on every request including unmatched ones, before routing. It cannot declare parameters and does not appear in the documentation.

The rule that follows: if it is about *this endpoint* or *this section* &mdash; authentication, permissions, validation &mdash; it is a dependency. If it is about *every request regardless of route* &mdash; CORS, compression, a request id, timing &mdash; it is middleware.

Reaching for middleware to do authentication is a common early choice and usually regretted, because the rule becomes invisible to the schema, awkward to exempt one route from, and hard to override in a test.

## Testing them

`dependency_overrides` works on these exactly as on parameter-level ones, which is the next module and is what makes a router-wide auth requirement pleasant rather than tiresome to test.


## Mistakes people make

**Application-wide authentication.** It catches the health check, the metrics endpoint and the docs, and the resulting outage is self-inflicted. If more than a couple of routes need an exemption, the level is wrong.

**Expecting the value to be injected.** These run for their effect. A handler that needs the value declares its own `Depends`, and the cache means the function still runs once.

**Using middleware for it instead.** Middleware runs before routing, cannot declare parameters, is invisible to the schema and is awkward to exempt one route from or override in a test.

**Protecting routes one at a time.** It works until the fourteenth route is added by somebody who does not know the convention. Nothing fails and no test covers it.

**Forgetting `responses=` on the router.** A section that can 401 should document it once, at the router, rather than on every route or nowhere.

**Assuming order does not matter.** App, then router, then route. Each layer can rely on the ones outside it having passed, which is what makes layered rules safe.

## Where the boundary sits

The clean division, stated once:

**Dependencies** are about endpoints. They know which route matched, declare parameters that reach the schema, integrate with your exception handlers, and can be overridden in tests. Authentication, permissions, request-scoped resources.

**Middleware** is about requests. It runs on everything including unmatched paths, before routing, and knows nothing about your endpoints. CORS, compression, request identifiers, timing.

Choosing by that question rather than by convenience keeps both simple.


## Choosing the level, concretely

A short decision procedure that avoids the common mistakes.

**Does every route without exception need it, including health checks and docs?** Then application level. Very few things qualify - a request identifier, tracing.

**Does a coherent section need it?** Router level. This is where most real use lives, and it is the level that survives a route being added later.

**Does exactly one endpoint need it, and the handler does not want the value?** Route level.

**Does the handler need the value?** A parameter, not any of these - and if the section also needs the guarantee, declare it in both places and let the cache make it one call.

The mistake worth naming again is the first. An application-level authentication dependency reads as tidy and takes out `/health` with it, which is discovered by a load balancer at the worst possible moment.

## Documenting a protected section

Two arguments belong on the router beside the dependency.

`responses={401: {"description": "Missing or invalid key"}}` documents the failure once for every route in the section.

`tags=["admin"]` groups them, so a reader of the documentation sees the protected endpoints together rather than scattered among the public ones.

Both are single arguments, and together they turn "these routes need a key" from something a caller discovers by being rejected into something the schema states.

## A note on ordering and errors

Because the layers run outermost first, the error a caller sees is from the outermost layer that failed.

That is usually right - a request with no API key should be told that, not told it lacks a permission it could not have been checked for. It does mean the layers should be ordered from most general to most specific, which the app/router/route nesting gives you for free.

Within a single `dependencies=[...]` list, the entries run in order, so a cheap check should come before an expensive one. There is no point querying a permissions table for a request whose token is missing.

## Documenting what a section requires

Worth restating because it is the difference between a section a caller can use and one they have to reverse-engineer.

A protected router should carry three things: the dependency that enforces the rule, a `responses` entry describing the failure, and a `tags` entry grouping the routes.

With those, the generated documentation shows a labelled group of endpoints, each documenting the header it needs and the 401 it can return. Without them the endpoints still work and a caller discovers the requirement by being refused, which is a worse first experience than any amount of prose can make up for.


## The decision in one line

Put it on the router.

Application-level catches the health check. Route-level is forgotten by whoever adds the fourteenth endpoint. The router is the level that matches how people actually think about an API - "everything under `/admin` needs an admin" - and it is the only one of the three where adding a route later cannot create a hole.

Reach past it only when the rule genuinely applies to every request without exception, or genuinely applies to exactly one endpoint.

## And the one to remember

The return value is discarded. These run for their effect.

When a handler needs the value as well, declare it again as a parameter and let the per-request cache collapse the two into one call. That looks redundant the first time you write it and is not: the router declaration guarantees the check on every route, and the parameter gets the value where it is used.

## Summary

`dependencies=[Depends(fn)]` attaches a dependency to one route, a router, or the whole application. They stack and run outermost first, and their return values are discarded - a handler needing the value declares its own, and the cache keeps it to one call.

The router level is where most real use belongs, and the reason is not brevity: a route added later is protected without anyone remembering to protect it.

Keep it out of the application level unless it genuinely applies to the health check too, and use a dependency rather than middleware whenever the rule is about endpoints rather than about every request.


## Summary, in one line

Put shared rules on the router, where a route added next year inherits them; declare the value again as a parameter when the handler needs it, and let the per-request cache make that one call rather than two.


## Two rules

**Prefer the router level.** It is the only one where a route added later cannot escape the rule.

**Declare it again as a parameter when the handler needs the value.** The cache makes that one call, and the two declarations mean two different things: the section's guarantee, and this handler's need.


## Where it sits in the tier

The other modules make a dependency available to an endpoint that asks for it. This one makes it apply to endpoints that did not.

That difference matters most for security, where the failure is silent: nobody notices an unprotected route until somebody is looking for one.

## Next

Replacing a dependency for a test - the piece that makes everything in this tier testable without a database, a token service or a network.
''',
    [
        {"q": "What happens to the return value of a router-level dependency?",
         "options": ["It is injected into every handler", "It is discarded - the dependency runs for its effect", "It becomes a header", "It is cached globally"],
         "answer": 1,
         "why": "There is no parameter to receive it. A handler needing the value declares its own Depends, and per-request caching means the function still runs once."},
        {"q": "What is the main argument for a router-level dependency over per-route?",
         "options": ["Performance", "A route added later is protected without anyone remembering", "Better docs", "It is required"],
         "answer": 1,
         "why": "Per-route protection works until somebody adds one and does not know the convention. Nothing fails, no test covers it, and the gap is found by someone looking."},
        {"q": "In what order do app, router and route dependencies run?",
         "options": ["Route first", "Outermost first - app, then router, then route", "Alphabetically", "Undefined"],
         "answer": 1,
         "why": "They stack rather than replace, so each layer adds a rule and can rely on the ones outside it having passed."},
        {"q": "Authentication across a section: dependency or middleware?",
         "options": ["Middleware - it is cross-cutting", "A dependency - it is about the endpoints, appears in the schema, and can be overridden in tests", "Either is equal", "Neither"],
         "answer": 1,
         "why": "Middleware runs before routing, cannot declare parameters, is invisible to the docs and is awkward to exempt or override. Reserve it for things that apply to every request regardless of route."},
    ],
)


# ---------------------------------------------------------------------------
# 19. Dependency overrides
# ---------------------------------------------------------------------------
topic(
    "dependency_overrides",
    "Dependency Overrides",
    "Dependencies",
    "Swapping a dependency for a test - the piece that makes the rest of this tier "
    "testable without a database or a network.",
    _svg(_box(12, 20, 56, 22, S) + _txt(40, 35, "real db", M, 8) +
         _arrow(72, 31, 88, 31) +
         _box(92, 20, 56, 22, S, A) + _txt(120, 35, "fake db", A, 8) +
         _txt(80, 64, "app.dependency_overrides", M, 8)),
    [
        ("Replacing one for a test",
         "<code>app.dependency_overrides</code> maps the real function to a stand-in. "
         "Every endpoint using it gets the stand-in instead.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()

def get_db():                       # the real one would open a connection
    raise RuntimeError("no database here")

@app.get("/modules")
def list_modules(db=Depends(get_db)):
    return {"rows": db["rows"]}

def fake_db():
    return {"rows": ["Vectors", "Norms"]}

print("without an override:")
try:
    TestClient(app).get("/modules")
except RuntimeError as e:
    print("  ", e)

app.dependency_overrides[get_db] = fake_db
print("with one          :", TestClient(app).get("/modules").json())'''),

        ("Overriding authentication",
         "The common case: tests that exercise an endpoint's logic without "
         "constructing a real token.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

def current_user(x_token: str = Header(default="")):
    if x_token != "a-real-token":
        raise HTTPException(401, "Sign in")
    return {"name": "ada", "role": "reader"}

@app.get("/me")
def me(user: dict = Depends(current_user)):
    return user

c = TestClient(app)
print("no token   :", c.get("/me").status_code)

app.dependency_overrides[current_user] = lambda: {"name": "test", "role": "admin"}
print("overridden :", TestClient(app).get("/me").json())
print()
print("The endpoint is unchanged. Only what it depends on moved.")'''),

        ("It reaches the whole tree",
         "Overriding a sub-dependency changes every dependency built on it, without "
         "touching them.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

def token(x_token: str = Header(default="")):
    if not x_token:
        raise HTTPException(401, "No token")
    return x_token

def current_user(t: str = Depends(token)):
    return {"name": t.upper()}

def admin(user: dict = Depends(current_user)):
    if user["name"] != "ADA":
        raise HTTPException(403, "Admins only")
    return user

@app.get("/admin")
def admin_page(u: dict = Depends(admin)):
    return u

c = TestClient(app)
print("no token      :", c.get("/admin").status_code)

app.dependency_overrides[token] = lambda: "ada"     # bottom of the tree
print("token faked   :", TestClient(app).get("/admin").json())
print()
print("current_user and admin were never mentioned, and both changed.")'''),

        ("Router-level dependencies too",
         "An override replaces the function wherever it is declared, including on a "
         "router.",
         '''from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

def require_key(x_api_key: str = Header(default="")):
    if x_api_key != "k-secret":
        raise HTTPException(401, "Bad key")

router = APIRouter(prefix="/admin", dependencies=[Depends(require_key)])

@router.get("/stats")
def stats(): return {"modules": 30}

app = FastAPI(); app.include_router(router)
c = TestClient(app)
print("locked  :", c.get("/admin/stats").status_code)

app.dependency_overrides[require_key] = lambda: None
print("unlocked:", TestClient(app).get("/admin/stats").json())'''),

        ("Putting it back",
         "Overrides live on the app, so a test that does not clear up leaks into "
         "every test after it.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()

def flag():
    return {"mode": "real"}

@app.get("/x")
def x(f: dict = Depends(flag)):
    return f

c = TestClient(app)
print("before  :", c.get("/x").json())

app.dependency_overrides[flag] = lambda: {"mode": "fake"}
print("during  :", TestClient(app).get("/x").json())

app.dependency_overrides.clear()          # or del [flag]
print("after   :", TestClient(app).get("/x").json())
print()
print("A test that forgets this makes the next one fail for no visible reason.")'''),

        ("A yield dependency can be overridden too",
         "Including with another yield dependency, so a fake session gets the same "
         "setup and teardown.",
         '''from fastapi import Depends, FastAPI

app = FastAPI()
log = []

def get_db():
    raise RuntimeError("no real database in a test")

@app.get("/rows")
def rows(db: list = Depends(get_db)):
    return {"rows": db}

def fake_db():
    log.append("open")
    try:
        yield ["a", "b"]
    finally:
        log.append("close")

app.dependency_overrides[get_db] = fake_db
print(TestClient(app).get("/rows").json())
print("lifecycle:", log)'''),
    ],
    [
        "<code>app.dependency_overrides[real] = fake</code> replaces a dependency everywhere it is used.",
        "The key is the <em>function object</em>, so it must be the same one the endpoints depend on &mdash; importing it twice by different paths is the usual reason an override appears not to work.",
        "Overriding a sub-dependency changes everything built on it, without naming the intermediate ones.",
        "It applies to router- and app-level dependencies as well as parameters.",
        "Overrides live on the app, so clear them between tests &mdash; <code>app.dependency_overrides.clear()</code> &mdash; or one test quietly changes the next.",
        "A yield dependency can be replaced by another, so a fake session still gets setup and teardown.",
    ],
    '''
title: Dependency Overrides
intro: Swapping a dependency for a test, and why that makes the whole tier practical.
## The mechanism

```python
app.dependency_overrides[get_db] = fake_db
```

A dictionary on the app, mapping the real callable to a replacement. When FastAPI resolves a dependency it checks that dictionary first, and uses the stand-in if one is registered.

That is the whole feature. It needs no test framework, no patching, and no change to the endpoints.

## Why it matters

Everything in this tier pushes requirements into dependencies: the database session, the current user, the permission check, the filters. That is good design and it would be a problem if those were hard to replace, because every test would then need a real database and a real token.

Overrides are the release valve. The endpoint keeps declaring `Depends(get_db)`; the test decides what `get_db` means.

Two consequences worth noticing. Tests get faster, because nothing real is constructed. And tests get *narrower* &mdash; a test for a handler's logic is not also a test of authentication, which means a broken token service does not fail two hundred unrelated tests.

## The key is the function object

This is the one thing that goes wrong, and the symptom is confusing: the override appears to be ignored.

The dictionary is keyed by identity, so the object you use as the key must be the same object the endpoints depend on. If your test imports `get_db` from `app.db` and the router imported it from `.db`, and those resolve to two different module objects, you have two different functions and the override targets the wrong one.

The fix is to be consistent about import paths. When an override silently does nothing, compare the two objects before looking anywhere else.

## It reaches the whole tree

Overriding a dependency replaces it wherever it appears, including deep inside a tree.

So overriding `token` at the bottom changes `current_user` and `admin_only` above it, without either being mentioned. That is usually what you want: fake the one thing at the edge &mdash; the network call, the database, the clock &mdash; and let the real logic above it run unchanged.

It is also the reason to fake as low as possible. Overriding `admin_only` skips the permission logic entirely; overriding `token` lets that logic actually be tested.

## Router and app level too

An override replaces the function wherever it is declared, which includes `dependencies=[...]` on a router or the app.

That is what makes a router-wide authentication requirement pleasant to test. Without it, every test of every route under `/admin` would need a valid key.

## Clean up

Overrides live on the app object, which usually outlives a single test.

A test that sets one and does not remove it changes every test that runs afterwards, and the failure appears somewhere unrelated with no obvious cause. In pytest the standard shape is a fixture that sets the override, yields, and clears it &mdash; the same setup/teardown discipline as a `yield` dependency, applied to the test.

`app.dependency_overrides.clear()` removes everything; `del app.dependency_overrides[fn]` removes one.

## Beyond tests

Occasionally useful outside testing.

A **local development** override can swap a real payment provider for a recording stub, or a real mailer for one that writes to a file.

A **demo build** can replace a live data source with fixtures.

Both are legitimate, and both deserve care: an override registered in production code is a piece of behaviour that does not appear in any endpoint's signature. If it is not a test, make it loud &mdash; guarded by an explicit setting, logged at startup, and impossible to enable by accident.

## What this tier gives you

Dependencies let an endpoint declare what it needs. Sub-dependencies let those requirements compose. `yield` gives them a lifetime. Router-level declarations apply them to a section. Overrides let all of it be replaced at the edges.

Together that is most of what separates a FastAPI application that stays testable from one that does not &mdash; and none of it requires anything beyond functions and a default argument.


## Mistakes people make

**Two import paths for one function.** The dictionary is keyed by identity, so `from app.db import get_db` and `from .db import get_db` can be different objects. The override then targets a function nobody depends on, and does nothing, silently.

**Not clearing between tests.** Overrides live on the app. One test that forgets makes a later, unrelated test fail with no visible cause.

**Faking too high in the tree.** Overriding `admin_only` skips the permission logic you meant to test. Override the edge - the token, the database, the clock - and let the real logic run.

**Using them in production without saying so.** An override is behaviour that appears in no endpoint signature. If it is not a test, gate it behind an explicit setting and log it at startup.

**Forgetting they work on router-level dependencies.** They do, which is what makes a section-wide auth requirement testable.

**Overriding instead of designing.** If a test needs six overrides, the endpoint probably depends on six things it should not.

## The shape in pytest

The standard arrangement is a fixture that sets, yields and clears - the same discipline as a `yield` dependency:

```python
@pytest.fixture
def client():
    app.dependency_overrides[get_db] = fake_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

Every test using that fixture gets the fake, and no test can leak it into the next one. It is four lines, and it is the difference between a suite that is trustworthy and one that fails differently depending on ordering.


## What good test structure looks like

Overrides work best with a small amount of structure around them.

**One fixture per fake.** A `fake_db` fixture, a `fake_user` fixture, each setting one override and clearing it. Tests then compose the ones they need rather than sharing a single do-everything client.

**Fake at the edges.** Override the database, the clock, the HTTP client, the token decoder. Do not override the permission logic, the filters, or anything you are trying to test.

**Prefer real objects to mocks.** A `fake_db` returning a dict or an in-memory list exercises more of the real code path than a mock that asserts it was called. The point of overriding is to remove the network, not the logic.

**Keep one test with nothing overridden.** An integration test that exercises the real tree catches the case where the fakes have quietly diverged from what they stand in for - which is the failure mode of heavy faking.

## The limits

Overrides replace a dependency, and that is all they do.

They cannot change what an endpoint declares, so an endpoint depending on something unnecessary still depends on it in tests. They do not apply to code called *inside* a handler - a handler that imports and calls `get_session()` directly is untouched by any override, which is the strongest practical argument for declaring dependencies rather than reaching for them.

And they are per app object. Tests that construct their own `FastAPI()` per module get isolation for free; tests that share one imported app need the discipline of clearing.

## Beyond the test suite

Two uses outside testing are legitimate, and both deserve care.

**Local development.** Swapping a payment provider for a recording stub, or a mailer for one that writes to a file, lets a developer run the whole application without credentials for anything external. It is genuinely useful and it is one setting away from being enabled somewhere it should not be.

**Demonstrations.** Replacing a live data source with fixtures gives a stable demo that does not depend on the state of a shared environment.

The rule for both: an override registered outside a test is behaviour that appears in no endpoint signature and no schema. Gate it behind an explicit setting, log it loudly at startup, and make the default off. A reader of the code should not have to know the overrides exist to understand what an endpoint does.

## What it says about the design

A final observation. If a test needs six overrides to run one endpoint, the overrides are not the problem - the endpoint is depending on six things.

Overrides make dependencies replaceable; they do not make an over-connected endpoint simple. When the fixture list grows, the useful question is whether the handler is doing work that belongs in a service, or depending on things it does not actually need.

Used that way the feature is also a design signal: the number of things you have to fake to test an endpoint is a fair measure of how entangled it is.


## Why this closes the tier

The five modules in this tier fit together, and overrides are what make the arrangement practical rather than merely elegant.

Dependencies let an endpoint declare what it needs. Sub-dependencies let those requirements build on each other. `yield` gives them a lifetime. Router-level declarations apply them to a whole section.

Every one of those pushes real things - a database, a token service, a clock - further from the handler and closer to the edge of the application. Without a way to replace them, that would make the endpoints harder to test rather than easier, and the whole approach would be a net loss.

Overrides invert it. Because the edges are declared rather than reached for, they can be swapped, and a handler that depends on four external things can be tested with none of them present.

That is the trade this tier is really about: declaring requirements instead of acquiring them. Everything else follows from it.

## Summary

`app.dependency_overrides[real] = fake` replaces a dependency everywhere it appears, including in a tree and on a router.

The key is the function object, so inconsistent import paths are the usual reason an override silently does nothing. Overrides live on the app, so clear them between tests or one quietly changes the next.

Fake at the edges - the database, the clock, the token - and let the real logic above run. Keep one test with nothing overridden, so the fakes cannot drift from what they stand in for without something failing.


## Summary, in one line

`app.dependency_overrides[real] = fake` swaps a dependency everywhere it appears - keyed by the function object, cleared between tests, and applied as low in the tree as possible so the logic above it still runs.


## Two rules

**Key on the same object the endpoints use.** Inconsistent imports are the reason an override silently does nothing.

**Clear between tests.** A leaked override fails a later, unrelated test with no visible cause.


## Where it sits in the tier

Last of the five, and the one that justifies the other four.

Pushing requirements into dependencies moves real things - databases, tokens, clocks - to the edge of the application. That would make testing harder if the edge could not be replaced. Overrides are what make it replaceable, and therefore what makes the whole approach pay.

## Next

The runtime: what actually happens when a request arrives, why an `async def` endpoint that makes a blocking call stalls every other request in the process, and the parts of the framework that need a real event loop.

And the failure to watch for is silence: an override that targets a different object than the endpoints use does nothing at all, reports nothing, and leaves the test passing against the real dependency.
''',
    [
        {"q": "What is `app.dependency_overrides` keyed by?",
         "options": ["The dependency's name", "The function object itself", "The route path", "A string id"],
         "answer": 1,
         "why": "It is keyed by identity, so importing the same function by two different paths gives two objects and the override silently targets the wrong one."},
        {"q": "You override a dependency at the bottom of a tree. What happens above it?",
         "options": ["Nothing", "Everything built on it uses the replacement", "It raises", "Only direct users change"],
         "answer": 1,
         "why": "That is why you should fake as low as possible - overriding the top skips the logic you wanted to test, while overriding the edge lets it run."},
        {"q": "Why clear overrides between tests?",
         "options": ["Performance", "They live on the app, so one test silently changes every later one", "They leak memory", "They are read-only"],
         "answer": 1,
         "why": "The failure appears in an unrelated test with no obvious cause. A fixture that sets, yields and clears is the standard shape."},
        {"q": "Can a router-level dependency be overridden?",
         "options": ["No", "Yes - overrides replace the function wherever it is declared", "Only with middleware", "Only at app level"],
         "answer": 1,
         "why": "Which is what makes a router-wide auth requirement testable; otherwise every test of every route in that section would need a valid credential."},
    ],
)


# ---------------------------------------------------------------------------
# 20. async vs sync endpoints
# ---------------------------------------------------------------------------
topic(
    "async_vs_sync_endpoints",
    "async def or def",
    "The Runtime",
    "Where your handler runs, and the one mistake that turns a fast framework "
    "into a slow one.",
    _svg(_box(10, 18, 62, 24, S, A) + _txt(41, 34, "async def", A, 8) +
         _txt(41, 56, "the event loop", M, 7) +
         _box(88, 18, 62, 24, S) + _txt(119, 34, "def", M, 8) +
         _txt(119, 56, "a threadpool", M, 7)),
    [
        ("Both are ordinary endpoints",
         "The framework accepts either, and a caller cannot tell which you wrote. "
         "The difference is where the function runs.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/sync")
def sync_endpoint():
    return {"style": "def"}

@app.get("/async")
async def async_endpoint():
    return {"style": "async def"}

c = TestClient(app)
print("sync :", c.get("/sync").status_code, c.get("/sync").json())
print("async:", c.get("/async").status_code, c.get("/async").json())
print()
print("Identical from outside. The choice is about what the body does.")'''),

        ("A sync handler is moved off the loop",
         "Starlette sends a <code>def</code> endpoint to a threadpool, so a blocking "
         "call in it cannot stall the loop.",
         '''import threading
from fastapi import FastAPI

app = FastAPI()
where = {}

@app.get("/sync")
def sync_endpoint():
    where["sync"] = threading.current_thread().name
    return {"thread": where["sync"]}

@app.get("/async")
async def async_endpoint():
    where["async"] = threading.current_thread().name
    return {"thread": where["async"]}

c = TestClient(app)
print("sync :", c.get("/sync").json())
print("async:", c.get("/async").json())
print()
print("In a real server these differ: the sync one runs on a worker thread,")
print("the async one on the thread owning the event loop.")'''),

        ("The mistake",
         "<code>async def</code> plus a blocking call. Nothing errors, and every "
         "other request in the process waits for it.",
         '''from fastapi import FastAPI

app = FastAPI()

def slow_blocking_call():
    total = 0
    for i in range(200_000):        # stands in for a synchronous DB driver
        total += i
    return total

@app.get("/wrong")
async def wrong():                  # async, but blocks the loop
    return {"total": slow_blocking_call()}

@app.get("/right")
def right():                        # sync, so it runs off the loop
    return {"total": slow_blocking_call()}

c = TestClient(app)
print("both return the same thing:")
print("  /wrong:", c.get("/wrong").json())
print("  /right:", c.get("/right").json())
print()
print("Only one of them let the server keep serving while it worked.")'''),

        ("Awaiting inside an async handler",
         "An <code>async def</code> endpoint earns its keep when it awaits &mdash; "
         "the loop runs something else while it waits.",
         '''from fastapi import FastAPI

app = FastAPI()
order = []

async def fetch(name):
    order.append("start " + name)
    value = await lookup(name)          # awaiting another coroutine
    order.append("done " + name)
    return value

async def lookup(name):
    return name.upper()

@app.get("/chain")
async def chain():
    a = await fetch("a")
    b = await fetch("b")
    return {"results": [a, b], "order": list(order)}

print(TestClient(app).get("/chain").json())
print()
print("An async handler awaiting async functions, all the way down.")
print()
print("Real interleaving - asyncio.gather over calls that actually wait -")
print("needs a running event loop, which this page does not have. The")
print("shape is the same; the concurrency is what a server adds.")'''),

        ("Dependencies follow the same rule",
         "A <code>def</code> dependency goes to the threadpool and an "
         "<code>async def</code> one runs on the loop, independently of the handler.",
         '''import threading
from fastapi import Depends, FastAPI

app = FastAPI()

def sync_dep():
    return {"dep": "sync", "thread": threading.current_thread().name}

async def async_dep():
    return {"dep": "async", "thread": threading.current_thread().name}

@app.get("/mixed")
async def mixed(a: dict = Depends(sync_dep), b: dict = Depends(async_dep)):
    return {"a": a["dep"], "b": b["dep"]}

print(TestClient(app).get("/mixed").json())
print()
print("An async handler may depend on a sync dependency and the reverse.")
print("Each is placed by its own definition, not by the handler's.")'''),

        ("Choosing, mechanically",
         "One question decides it: does the body await anything?",
         '''from fastapi import FastAPI

app = FastAPI()

# Awaits something -> async def.
async def load():
    return "loaded"

@app.get("/awaits")
async def awaits():
    await load()
    return {"rule": "awaits something -> async def"}

# Blocks -> def, and let the threadpool have it.
@app.get("/blocks")
def blocks():
    sum(range(50_000))
    return {"rule": "blocking call -> def"}

# Neither -> either works; def is the safer default.
@app.get("/neither")
def neither():
    return {"rule": "pure computation, no I/O -> def is fine"}

c = TestClient(app)
for p in ["/awaits", "/blocks", "/neither"]:
    print(c.get(p).json())'''),
    ],
    [
        "A <code>def</code> endpoint runs in a threadpool; an <code>async def</code> one runs on the event loop. Callers cannot tell the difference.",
        "The mistake is <code>async def</code> with a blocking call inside: nothing errors, and every other request in the process waits.",
        "If a handler <strong>awaits</strong> something, write <code>async def</code>. If it makes a blocking call, write <code>def</code> and let the threadpool take it.",
        "When it does neither, <code>def</code> is the safer default &mdash; a blocking call added later cannot stall the loop.",
        "Dependencies are placed by their own definition, so an async handler can depend on a sync dependency and the reverse.",
        "The threadpool is finite. A great many slow sync handlers exhaust it, which is a different limit from stalling the loop and looks similar from outside.",
        "The editors here run without a live event loop, so an <code>await</code> that genuinely suspends &mdash; <code>asyncio.sleep</code>, a real network call &mdash; cannot be demonstrated. Awaiting coroutines that complete works, and is the same shape.",
    ],
    '''
title: async def or def
intro: Where your handler runs, and the one mistake that turns a fast framework into a slow one.
## Two placements, one interface

FastAPI accepts both:

```python
@app.get("/a")
def handler(): ...

@app.get("/b")
async def handler(): ...
```

A caller cannot tell the difference. The response is the same, the documentation is the same, validation is the same.

What differs is **where the function runs**. An `async def` endpoint is awaited directly on the event loop, in the same thread that is handling every other concurrent request. A `def` endpoint is handed to a threadpool, so the loop is free while it works.

That single fact explains everything else in this module.

## Why an event loop is fast

An ASGI server handles many requests in one thread by never waiting. When a handler awaits a database query, the loop parks it and runs something else. Thousands of requests can be in flight with almost none of them consuming anything but memory.

That works because awaiting yields control. It stops working the moment something does not.

## The mistake

```python
@app.get("/users")
async def users():
    return db.query(User).all()      # a blocking driver
```

This looks modern and is the single most common performance bug in FastAPI applications.

The function is `async`, so it runs on the loop. The query is synchronous, so it does not yield. For the entire duration of that query the loop is stuck: no other request progresses, no other handler runs, no keepalive is answered. One slow query has stopped the whole process.

Nothing errors. The endpoint returns correctly. It is only under concurrency that the application turns out to handle one request at a time, and the symptom &mdash; everything is slow when the system is busy &mdash; points nowhere useful.

The fix is one keyword:

```python
@app.get("/users")
def users():
    return db.query(User).all()
```

Now Starlette runs it in a threadpool and the loop keeps going.

## The rule

**Does the body await anything?**

Yes &mdash; `async def`. An async database driver, an async HTTP client, `asyncio.sleep`, another async function.

No, and it blocks &mdash; `def`. A synchronous driver, `requests`, file I/O, a CPU-bound computation.

Neither &mdash; either works, and `def` is the safer default, because a blocking call added later cannot stall anything.

The rule to distrust is "async is faster". Async is faster *when it awaits*. An async handler that blocks is slower than the sync version of the same code, because it takes the whole process with it.

## Dependencies follow their own definition

A dependency is placed by how *it* is written, not by the handler.

So an `async def` handler can depend on a `def` dependency &mdash; the dependency goes to the threadpool, the handler stays on the loop &mdash; and the reverse works too. Mixing is normal and correct.

The same rule applies to each: if the dependency opens a connection with a blocking driver, it should be `def`.

## The threadpool is finite

Sync handlers are safe for the loop and not free. Starlette's threadpool has a limited number of workers &mdash; a few dozen by default.

If every request is a slow sync handler, those threads fill up and further requests queue waiting for one. The loop is healthy and the application is still stuck, which looks similar from outside and has a different cause.

That is the real argument for async drivers under high concurrency: not that the syntax is better, but that awaiting costs a coroutine and blocking costs a thread, and there are far more coroutines available than threads.

For most applications, the threadpool is entirely adequate and the simplicity of sync code is worth more than the ceiling.

## Do not mix them badly

Two specific things to avoid.

**Calling a sync function that blocks from inside an async handler.** That is the mistake above wearing a different hat. If you must, `await run_in_threadpool(fn)` moves it off the loop explicitly.

**Calling `asyncio.run()` inside a handler.** There is already a loop running; starting another raises. To call an async function from a sync handler, the honest answer is usually to make the handler async.

## Mistakes people make

**`async def` with a blocking call.** The one that matters. Nothing errors and the whole process serves one request at a time under load, with a symptom - everything is slow when busy - that points nowhere useful.

**Assuming async is faster.** Async is faster when it awaits. An async handler that blocks is worse than the sync version, because it takes every concurrent request with it.

**`asyncio.run()` inside a handler.** There is already a loop; starting another raises. To call an async function from a sync handler, make the handler async.

**Mixing drivers without noticing.** An async endpoint using a synchronous ORM is the same bug wearing different clothes. If the driver blocks, the endpoint should be `def`.

**Ignoring the threadpool ceiling.** Sync handlers are safe for the loop and finite in number. Enough slow ones exhaust the pool, which looks the same from outside and has a different cause.

**Choosing per handler with no rule.** Then nobody can tell whether a given endpoint is safe to add a blocking call to, and eventually somebody adds one to the wrong sort.

## Diagnosing it

Two symptoms distinguish the failures.

**The loop is stalled**: latency rises across every endpoint at once, including trivial ones, and a health check that does nothing takes seconds. Something async is blocking.

**The threadpool is full**: the fast endpoints stay fast while requests to slow sync ones queue. The loop is fine; the workers are all busy.

The fix differs. The first needs the blocking call moved off the loop - change `async def` to `def`, or wrap it in `run_in_threadpool`. The second needs fewer slow synchronous operations, more workers, or async drivers.

## Being consistent

An application that is mostly sync and mostly fast is a perfectly good application. So is one that is async throughout with async drivers. Both scale further than most services ever need.

What causes trouble is a codebase where the choice was made per handler by whoever wrote it. Then nobody can look at an endpoint and tell whether adding a blocking call to it is safe, and eventually somebody adds one to the wrong sort.

Pick a default, write it in the project's README, and make the exception deliberate. "Sync unless it awaits" is a fine rule. So is "async everywhere, and every driver must be async". The rule matters more than which one.


## Where the ceilings are

Two limits, and telling them apart is most of diagnosing a slow FastAPI service.

**The loop** is stalled by any blocking call in an `async def` handler or dependency. One slow query stops every concurrent request in that process. The symptom is that everything gets slow at once, including endpoints that do nothing.

**The threadpool** is exhausted by enough concurrent `def` handlers. The loop stays healthy and fast endpoints stay fast, while requests to slow ones queue for a worker.

The first is a bug and the fix is free: move the blocking call off the loop. The second is a capacity limit, and the fixes are real - fewer slow synchronous operations, more workers, or async drivers so waiting costs a coroutine rather than a thread.

Knowing which you have takes one observation: does a trivial endpoint also get slow? If yes, the loop. If no, the pool.

## What async actually buys

Worth stating plainly, because "async is faster" is both common and wrong.

Async does not make any single request faster. A query takes as long either way.

What it changes is how many requests one process can have **in flight** while waiting. With threads, waiting costs a thread and there are hundreds available. With coroutines, waiting costs a few kilobytes and there are hundreds of thousands available.

For an API that spends most of its time waiting on other systems - which is most APIs - that is the difference between a machine handling a few hundred concurrent requests and one handling many thousands. It is a concurrency win, not a latency one, and only if the waiting is done by awaiting.

## Summary

`def` runs in a threadpool; `async def` runs on the event loop. Callers cannot tell.

Write `async def` when the body awaits, `def` when it blocks, and `def` by default when it does neither - because a blocking call added later cannot then stall anything.

Dependencies are placed by their own definition, so mixing is normal. And remember there are two ceilings: the loop, which one blocking call can stall, and the threadpool, which enough slow sync handlers can exhaust.

## Next

Work that should happen after the response has been sent - what background tasks are for, what they are not, and the point at which they need to become a real queue.


## The rule, once more

Awaits something, `async def`. Blocks, `def`. Neither, `def`.

That covers essentially every case, and the reason the third clause defaults to `def` is that it is the only one that stays correct when somebody later adds a blocking call to a handler that used to do nothing much.


## A closing thought

This is the one place where FastAPI will let you write something that looks right, passes every test, and fails only under load.

Nothing warns about `async def` around a blocking call. The endpoint is correct, the tests pass because they run one request at a time, and the problem appears in production as generalised slowness with no obvious cause.

That asymmetry - easy to write, hard to notice, expensive to diagnose - is why it is worth knowing the rule properly rather than choosing by habit.

## One more diagnostic

If a service is slow and you are not sure which ceiling you have hit, the cheapest test is an endpoint that does nothing:

```python
@app.get("/ping")
def ping():
    return {"ok": True}
```

Under load, hit it. If it is fast while other endpoints crawl, the loop is healthy and the threadpool is saturated. If it is also slow, something is blocking the loop.

That single observation separates a capacity problem from a bug, and the two have entirely different fixes.

## In one line

`async def` when the body awaits, `def` when it blocks, `def` by default when it does neither - because that is the only choice that stays correct when somebody adds a blocking call later.

And if a service is slow and you cannot tell which ceiling you hit, hit an endpoint that does nothing: if it is fast, the pool is full; if it is slow, the loop is blocked.
''',
    [
        {"q": "Where does a `def` endpoint run?",
         "options": ["On the event loop", "In a threadpool", "In a subprocess", "It is rejected"],
         "answer": 1,
         "why": "Starlette moves it off the loop, which is why a blocking call inside a sync handler cannot stall other requests."},
        {"q": "What happens with `async def` plus a blocking database call?",
         "options": ["An error", "Nothing errors - the loop stalls and every other request waits", "It runs in a thread anyway", "It is faster"],
         "answer": 1,
         "why": "The most common performance bug in FastAPI applications. It returns correctly and only fails under concurrency, where the symptom points nowhere useful."},
        {"q": "Your handler makes no I/O calls at all. Which should you write?",
         "options": ["async def, it is more modern", "def - a blocking call added later cannot stall the loop", "Either, it never matters", "Neither"],
         "answer": 1,
         "why": "`async` is faster when it awaits. With nothing to await it gains nothing and leaves a trap for whoever adds a blocking call next."},
        {"q": "An async handler depends on a `def` dependency. What happens?",
         "options": ["An error", "The dependency runs in the threadpool; the handler stays on the loop", "Both run on the loop", "Both run in threads"],
         "answer": 1,
         "why": "Each is placed by its own definition, so mixing is normal - and a dependency using a blocking driver should be `def` regardless of the handler."},
    ],
)


# ---------------------------------------------------------------------------
# 21. Background tasks
# ---------------------------------------------------------------------------
topic(
    "background_tasks",
    "Background Tasks",
    "The Runtime",
    "Work that should happen after the response has gone - and the point at which "
    "it needs a real queue instead.",
    _svg(_box(12, 16, 60, 20, S) + _txt(42, 30, "handler", M, 8) +
         _arrow(76, 26, 90, 26) + _box(94, 16, 54, 20, S, A) + _txt(121, 30, "response", A, 8) +
         _arrow(42, 40, 42, 54) + _box(12, 56, 60, 20, S) + _txt(42, 70, "task runs", M, 8)),
    [
        ("Declare it and add to it",
         "A <code>BackgroundTasks</code> parameter gives you something to schedule "
         "on. The task runs after the response is produced.",
         '''from fastapi import BackgroundTasks, FastAPI

app = FastAPI()
sent = []

def send_welcome(email: str):
    sent.append(email)

@app.post("/signup", status_code=201)
def signup(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_welcome, email)
    return {"queued": True}

c = TestClient(app)
print("response:", c.post("/signup?email=ada@vizlearn.in").json())
print("sent    :", sent)
print()
print("The caller got 201 without waiting for the mail to be handled.")'''),

        ("The response goes first",
         "Ordering is the whole point: the client is answered, then the task runs.",
         '''from fastapi import BackgroundTasks, FastAPI

app = FastAPI()
order = []

def after():
    order.append("task")

@app.get("/x")
def x(tasks: BackgroundTasks):
    order.append("handler")
    tasks.add_task(after)
    order.append("returning")
    return {"order_so_far": list(order)}

r = TestClient(app).get("/x")
print("body seen by the client:", r.json())
print("order after everything  :", order)'''),

        ("Several tasks, in order",
         "They run one after another, in the order added &mdash; not concurrently.",
         '''from fastapi import BackgroundTasks, FastAPI

app = FastAPI()
log = []

def step(name):
    log.append(name)

@app.post("/publish")
def publish(tasks: BackgroundTasks):
    tasks.add_task(step, "reindex")
    tasks.add_task(step, "notify")
    tasks.add_task(step, "audit")
    return {"queued": 3}

print(TestClient(app).post("/publish").json())
print("ran:", log)
print()
print("Sequential. A slow first task delays the second.")'''),

        ("Arguments are passed through",
         "Positional and keyword arguments both work, and the values are captured "
         "when the task is added.",
         '''from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

app = FastAPI()
records = []

def audit(action: str, module_id: int, actor: str = "system"):
    records.append({"action": action, "module": module_id, "actor": actor})

class ModuleIn(BaseModel):
    title: str

@app.post("/modules/{i}", status_code=201)
def create(i: int, body: ModuleIn, tasks: BackgroundTasks):
    tasks.add_task(audit, "create", i, actor="ada")
    tasks.add_task(audit, "index", i)
    return {"id": i, "title": body.title}

print(TestClient(app).post("/modules/7", json={"title": "Vectors"}).json())
for r in records:
    print(" ", r)'''),

        ("A task that raises",
         "The response has already gone, so the failure cannot reach the caller. "
         "Catch it inside the task.",
         '''from fastapi import BackgroundTasks, FastAPI

app = FastAPI()
LOG = []

def risky(name):
    try:
        raise RuntimeError("could not deliver to %s" % name)
    except RuntimeError as e:
        LOG.append("handled: %s" % e)      # log it; nobody is listening

@app.post("/notify", status_code=202)
def notify(tasks: BackgroundTasks):
    tasks.add_task(risky, "ada")
    return {"accepted": True}

r = TestClient(app).post("/notify")
print("client saw:", r.status_code, r.json())
print("log       :", LOG)
print()
print("202 means accepted, not finished - which is the honest status here.")'''),

        ("They can be added from a dependency",
         "Anything with a <code>BackgroundTasks</code> parameter can schedule work, "
         "so cross-cutting jobs need not touch the handler.",
         '''from fastapi import BackgroundTasks, Depends, FastAPI, Header

app = FastAPI()
trail = []

def record_request(tasks: BackgroundTasks, x_actor: str = Header(default="anon")):
    tasks.add_task(trail.append, "seen %s" % x_actor)

@app.get("/a", dependencies=[Depends(record_request)])
def a(): return {"route": "a"}

@app.get("/b", dependencies=[Depends(record_request)])
def b(): return {"route": "b"}

c = TestClient(app)
c.request("GET", "/a", headers={"x-actor": "ada"})
c.request("GET", "/b")
print("trail:", trail)'''),
    ],
    [
        "Declare a <code>BackgroundTasks</code> parameter and call <code>add_task(fn, *args, **kwargs)</code>. The task runs after the response is produced.",
        "Tasks run <strong>in the same process</strong>, sequentially, in the order added &mdash; not concurrently and not on another machine.",
        "A task that raises cannot tell the caller: the response has gone. Catch and log inside the task.",
        "Dependencies can add tasks too, so cross-cutting work does not have to touch the handler.",
        "Anything slow blocks a worker for its duration, and anything in flight is lost if the process restarts.",
        "Use them for short, non-critical, fire-and-forget work. Anything that must not be lost belongs in a real queue.",
    ],
    '''
title: Background Tasks
intro: Work that should happen after the response has gone, and the point at which it needs a real queue instead.
## The mechanism

```python
@app.post("/signup", status_code=201)
def signup(email: str, tasks: BackgroundTasks):
    tasks.add_task(send_welcome, email)
    return {"queued": True}
```

Declare a `BackgroundTasks` parameter, add callables to it, and they run once the response has been produced.

The caller is not waiting for the welcome email. That is the entire value: a request that must do something slow and inessential can answer immediately and do it afterwards.

## Ordering, precisely

The response is produced and sent, then the tasks run, in the order they were added, one after another.

Not concurrently. A slow first task delays the second, and both delay nothing that the client can see &mdash; but they do occupy the worker.

For a sync handler the tasks run in the threadpool; for an async one they run on the loop. The same rule as endpoints applies to a task's own body: a blocking task added by an async handler blocks the loop, after the response, which is easy to miss precisely because nothing appears slow to the caller.

## What they are not

This is the part that matters, and it is where people get hurt.

**They are not durable.** Tasks live in memory in the current process. If the process restarts &mdash; a deploy, a crash, a scale-down &mdash; anything queued is gone, with no record that it existed.

**They are not distributed.** They run in the process that served the request, on the same machine, consuming its capacity.

**They are not retried.** A task that fails has failed. There is no backoff, no dead-letter queue, no visibility.

**They are not observable.** Nothing tracks how many are pending or how long they take unless you build it.

So the honest description is: a convenient way to do a *short, non-critical* piece of work after responding.

## When to use a real queue

Move to Celery, RQ, Dramatiq, or a cloud queue when any of these is true.

The work **must not be lost** &mdash; a payment confirmation, an audit record, anything a user would notice the absence of.

The work is **slow** &mdash; more than a second or two. A background task occupies a worker, and enough of them starve the pool exactly as slow handlers do.

The work should be **retried** on failure.

The work should **scale separately** from the web tier, or run on different hardware.

You need to **see** the queue &mdash; depth, failures, latency.

The rule of thumb: a background task is for work whose loss would be an inconvenience. Anything whose loss would be a bug belongs somewhere durable.

Good uses: writing a log line, warming a cache, sending a non-critical notification, cleaning up a temporary file, firing an analytics event.

## Failure

A task that raises cannot report to the caller, because the caller already has their response. The exception surfaces in the server logs and nowhere else.

So catch inside the task, and log deliberately. A bare exception in a background task is a silent failure by construction.

If the work has a meaningful failure the client should learn about, it is not a background task &mdash; it is either part of the request, or a job with a status the client can poll.

## The right status code

An endpoint that queues work rather than completing it is a good candidate for **202 Accepted** rather than 200 or 201.

202 says exactly what happened: the request was understood and accepted, and it is not finished. If there is anything to poll, the body should say where.

Returning 201 for something that has not been created yet is a small lie that a client may act on.

## From a dependency

Any callable that can declare parameters can declare `BackgroundTasks`, which includes dependencies.

That is a tidy way to attach cross-cutting after-the-fact work &mdash; an audit trail, a metrics event &mdash; to a whole router without touching a single handler. The dependency schedules; the handlers stay unaware.


## Mistakes people make

**Treating them as durable.** They live in memory in the serving process. A deploy discards everything queued, with no record it existed.

**Putting something important in one.** A payment confirmation, an audit record, anything a user would notice missing. Loss is invisible and unrecoverable.

**Long-running work.** A background task occupies a worker for its duration. Enough of them starve the pool exactly as slow handlers do.

**Letting exceptions escape.** The response has gone, so the failure reaches the logs and nobody else. Catch and log inside the task.

**Blocking the loop from an async handler.** A synchronous task added by an async endpoint runs on the loop after the response - stalling everything, while appearing fast to the caller who already left.

**Returning 201 for queued work.** It says something was created. 202 says it was accepted and is not finished, which is what actually happened.

## The line

A background task is for work whose **loss would be an inconvenience**. Anything whose loss would be a bug belongs in a durable queue.

Good: a log line, a cache warm, a non-critical notification, a temporary file cleaned up, an analytics event.

Not: anything with money in it, anything a user is told happened, anything that must be retried, anything that takes more than a second or two.

The upgrade path is Celery, RQ, Dramatiq or a cloud queue, and the moment to take it is when you first find yourself hoping a task did not get lost.

## Where it fits

Background tasks sit between doing the work in the request and running a real queue, and the band they occupy is narrower than it first appears.

Above them: anything durable, retried, observable, slow, or scaled separately. That is a queue, and reaching for one is not over-engineering once the work matters.

Below them: anything the caller needs the result of. That belongs in the request, and if it is slow the honest answer is 202 with something to poll rather than a background task and a hopeful 200.

What is left is genuinely useful - the log line, the cache warm, the notification nobody will chase - and for that they are exactly right, cost nothing to adopt, and need no infrastructure at all.


## A worked upgrade path

The moment to leave background tasks behind is recognisable, and the move is smaller than it looks.

**Stage one** is what this module describes: `tasks.add_task(send_welcome, email)`. No infrastructure, no configuration, and the work is lost on restart.

**Stage two** keeps the same call site and changes what it does. The task becomes `enqueue(send_welcome, email)`, writing a row to a jobs table or a message to a queue. The endpoint is unchanged; the durability arrives underneath it.

**Stage three** is a worker process consuming that queue, with retries, backoff and a dead-letter path for what keeps failing.

Writing stage one so the call site is a single function - not five lines of task construction inline - is what makes stage two a small change rather than a rewrite of every endpoint.

## What the caller should be told

An endpoint that queues work owes the caller two things.

An honest status: **202 Accepted**, not 200 or 201, because nothing is finished.

Somewhere to look, when there is anything to look at. A job id and a `GET /jobs/{id}` is the conventional shape, and it turns "we will get to it" into something a client can act on.

Without those, the caller assumes completion. That assumption is fine for a log line and wrong for anything they will ask about later.

## Summary

Declare `BackgroundTasks`, call `add_task`, and the work happens after the response.

They run in the same process, sequentially, without retries, and are lost on restart. Catch exceptions inside them because nobody is listening. Return 202 when queueing rather than completing. And move to a real queue the first time you find yourself hoping a task did not get lost.

## Next

Work that happens once per process rather than once per request: startup and shutdown, where a connection pool actually belongs, and why anything that must happen exactly once for the application does not belong there either.


## The honest summary

Background tasks are a small, sharp tool with a narrow band of good uses.

They cost nothing to adopt, need no infrastructure, and remove genuinely inessential work from the request path. For a log line, a cache warm or a notification nobody will chase, they are exactly right.

They are also in-memory, in-process, sequential, unretried, unobserved and lost on restart. Every one of those is fine for the uses above and disqualifying for anything else.

The failure is not using them; it is using them for something that matters and discovering the properties afterwards, usually when somebody asks why a confirmation never arrived and there is no record that it was ever attempted.


## A closing thought

The value of background tasks is that they exist at all, for free, with no infrastructure.

Most applications have a handful of things that genuinely should not delay a response and genuinely do not matter enough to build a queue for. Before this feature the choice was to do them in the request anyway, or to introduce a broker for something trivial.

Knowing exactly what they guarantee - which is very little - is what makes them safe to use for that handful, and what stops them being reached for when the guarantee matters.

## One more consideration

Background tasks share the process with the requests they follow, which means they share its limits.

A sync task added by a sync handler runs in the threadpool, occupying a worker that could have served a request. A sync task added by an *async* handler runs on the loop, after the response - stalling every other request in the process while appearing perfectly fast to the caller who has already left.

That second case is worth watching for, because nothing about it looks slow from outside. The endpoint's latency is fine; everything else in the process degrades, and the cause is code that runs after the thing you were measuring.

The rule from the async module applies unchanged: if the task blocks, it should not be running on the loop.

## In one line

A background task is in-memory, in-process, sequential, unretried and lost on restart - which makes it exactly right for the log line and exactly wrong for the confirmation email, and the whole skill is telling those apart before rather than after.

The tell that you have crossed the line is simple: if you would be uncomfortable telling a user "we may have lost this and cannot check", the work does not belong in a background task. That sentence is precisely what the feature guarantees.

A last practical note: write the call site as one function - `enqueue(fn, *args)` rather than task construction spread through the handler. If the work later needs a real queue, that is a one-line change in one place instead of an edit to every endpoint that scheduled anything.
''',
    [
        {"q": "When does a background task run?",
         "options": ["Before the handler", "Concurrently with the handler", "After the response has been produced", "On the next request"],
         "answer": 2,
         "why": "That ordering is the point - the caller is answered without waiting for the slow, inessential part."},
        {"q": "The process restarts with tasks queued. What happens to them?",
         "options": ["They are retried", "They are lost, with no record", "They move to another worker", "They run at startup"],
         "answer": 1,
         "why": "Tasks live in memory in the serving process. That is why anything whose loss would be a bug belongs in a durable queue instead."},
        {"q": "A background task raises. What does the caller see?",
         "options": ["A 500", "Nothing - the response was already sent", "A retry", "A 202"],
         "answer": 1,
         "why": "The failure cannot reach them, so it is silent by construction unless the task catches and logs it deliberately."},
        {"q": "Which status code best fits an endpoint that queues work?",
         "options": ["200", "201", "202 Accepted", "204"],
         "answer": 2,
         "why": "202 says the request was accepted and is not finished. Returning 201 for something not yet created is a small lie a client may act on."},
    ],
)


# ---------------------------------------------------------------------------
# 22. Lifespan events
# ---------------------------------------------------------------------------
topic(
    "lifespan_events",
    "Lifespan Events",
    "The Runtime",
    "Work that happens once per process rather than once per request - and where a "
    "connection pool actually belongs.",
    _svg(_box(20, 12, 120, 18, S, A) + _txt(80, 25, "startup", A, 8) +
         _arrow(80, 32, 80, 42) +
         _box(20, 44, 120, 18, S) + _txt(80, 57, "serving requests", M, 8) +
         _arrow(80, 64, 80, 74) +
         _box(20, 76, 120, 16, S, A) + _txt(80, 88, "shutdown", A, 8)),
    [
        ("The lifespan protocol, driven by hand",
         "A server sends the app a startup message before serving and a shutdown "
         "message after. This is that, without the server.",
         '''from contextlib import asynccontextmanager
from fastapi import FastAPI

events = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    events.append("startup")
    yield                       # the application serves requests here
    events.append("shutdown")

app = FastAPI(lifespan=lifespan)

@app.get("/x")
def x():
    return {"events": list(events)}

def run_lifespan(app, phase):
    """Send one lifespan message, the way uvicorn would."""
    msgs = []
    async def receive(): return {"type": "lifespan." + phase}
    async def send(m):   msgs.append(m["type"])
    drive(app({"type": "lifespan", "asgi": {"version": "3.0"}}, receive, send))
    return msgs

print("startup :", run_lifespan(app, "startup"), events)
print("request :", TestClient(app).get("/x").json())
print("shutdown:", run_lifespan(app, "shutdown"), events)'''),

        ("Sharing state with the handlers",
         "Anything created at startup is put where handlers can reach it &mdash; "
         "<code>app.state</code> is the conventional place.",
         '''from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

opened = []

class Pool:
    def __init__(self): opened.append("pool"); self.n = 0
    def query(self): self.n += 1; return "rows(%d)" % self.n
    def close(self): opened.append("closed")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = Pool()
    yield
    app.state.pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/rows")
def rows(request: Request):
    return {"rows": request.app.state.pool.query()}

def cycle(app, phase):
    async def receive(): return {"type": "lifespan." + phase}
    async def send(m): pass
    drive(app({"type": "lifespan", "asgi": {"version": "3.0"}}, receive, send))

cycle(app, "startup")
c = TestClient(app)
print(c.get("/rows").json())
print(c.get("/rows").json(), "<- same pool, second query")
cycle(app, "shutdown")
print("lifecycle:", opened)'''),

        ("A dependency hands it to the handler",
         "Reaching through <code>request.app.state</code> works and reads poorly. A "
         "dependency gives the handler the thing itself.",
         '''from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request

class Pool:
    def query(self): return ["Vectors", "Norms"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = Pool()
    yield

app = FastAPI(lifespan=lifespan)

def get_pool(request: Request) -> Pool:
    return request.app.state.pool

@app.get("/modules")
def modules(pool: Pool = Depends(get_pool)):
    return {"rows": pool.query()}

async def receive(): return {"type": "lifespan.startup"}
async def send(m): pass
drive(app({"type": "lifespan", "asgi": {"version": "3.0"}}, receive, send))

print(TestClient(app).get("/modules").json())
print()
print("The handler never mentions app.state, so it is trivial to override.")'''),

        ("Per process, not per request",
         "The startup body runs once however many requests arrive. That is the "
         "distinction that decides what belongs here.",
         '''from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, Request

built = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    built.append("pool")                 # once
    app.state.pool = {"id": len(built)}
    yield

app = FastAPI(lifespan=lifespan)

def session(request: Request):
    return {"pool": request.app.state.pool, "session": "fresh"}

@app.get("/x")
def x(s: dict = Depends(session)):
    return s

async def receive(): return {"type": "lifespan.startup"}
async def send(m): pass
drive(app({"type": "lifespan", "asgi": {"version": "3.0"}}, receive, send))

c = TestClient(app)
for _ in range(3):
    print(c.get("/x").json())
print("pools built:", len(built), "<- one, for three requests")'''),

        ("Failing at startup",
         "An exception before the yield stops the application coming up, which is "
         "the right moment to discover a missing setting.",
         '''from contextlib import asynccontextmanager
from fastapi import FastAPI

SETTINGS = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    if "database_url" not in SETTINGS:
        raise RuntimeError("database_url is not configured")
    yield

app = FastAPI(lifespan=lifespan)

async def receive(): return {"type": "lifespan.startup"}
async def send(m): pass

try:
    drive(app({"type": "lifespan", "asgi": {"version": "3.0"}}, receive, send))
except RuntimeError as e:
    print("refused to start:", e)

SETTINGS["database_url"] = "postgres://..."
drive(app({"type": "lifespan", "asgi": {"version": "3.0"}}, receive, send))
print("started once configured")'''),

        ("Startup or import?",
         "Work at import runs whenever the module is imported &mdash; including by a "
         "test collector. Startup runs when the application actually starts.",
         '''from contextlib import asynccontextmanager
from fastapi import FastAPI

log = []

# At import: happens the moment this module is loaded, by anyone.
log.append("import-time work")

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.append("startup work")
    yield
    log.append("shutdown work")

app = FastAPI(lifespan=lifespan)

print("after import  :", log)

async def receive(): return {"type": "lifespan.startup"}
async def send(m): pass
drive(app({"type": "lifespan", "asgi": {"version": "3.0"}}, receive, send))
print("after startup :", log)
print()
print("A test that merely imports the module paid for the first line only.")'''),
    ],
    [
        "A lifespan is an async context manager: everything before the <code>yield</code> runs at startup, everything after at shutdown.",
        "It runs <strong>once per process</strong>, not per request &mdash; and once per worker, so four workers build four pools.",
        "Put what it creates on <code>app.state</code>, and hand it to handlers through a dependency rather than reaching for <code>request.app.state</code> in each one.",
        "Raising before the yield stops the application starting, which is the right moment to find a missing setting.",
        "Prefer startup over import-time work: an import happens whenever anything loads the module, including a test collector.",
        "<code>@app.on_event(\"startup\")</code> is the older spelling and is deprecated. The lifespan context manager replaced it.",
    ],
    '''
title: Lifespan Events
intro: Work that happens once per process rather than once per request, and where a connection pool belongs.
## Two lifetimes

Almost everything in this track has been per request: a body, a session, a user, a background task.

Some things are not. A database connection **pool** is created once and used by every request. So is an HTTP client, a machine-learning model, a cache client, a loaded configuration.

Creating those per request would be absurdly wasteful; creating them at import has its own problems. Lifespan is the third option, and the correct one.

## The shape

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = await create_pool()
    yield
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)
```

An async context manager. Everything before the `yield` runs when the application starts; everything after runs when it stops. In between, it serves requests.

The shape is deliberately the same as a `yield` dependency, with a different lifetime: that one is per request, this one is per process.

## What the server actually does

Before serving anything, uvicorn sends the application a `lifespan.startup` message and waits for it to complete. After the last request, it sends `lifespan.shutdown`.

That is a real protocol, not a framework convention, which is why the editors above can drive it by hand: build the scope, send the message, and watch the same code run that uvicorn would have triggered.

## Once per process, and per worker

The startup body runs **once**, however many requests arrive. That is the distinction that decides what belongs in it.

Worth being precise about the plural: production usually runs several worker processes, and each is a separate process with its own lifespan. Four workers means four pools, four model loads, four caches. Anything expensive is paid for four times, and anything that must be unique across the application &mdash; a scheduler, a migration, a leader election &mdash; must not be in a lifespan, because it will run once per worker rather than once.

That last point catches people. A migration in startup runs concurrently in four processes on the first deploy.

## Getting at it from a handler

What startup creates has to be reachable. The convention is `app.state`:

```python
app.state.pool = pool
```

and in a handler, `request.app.state.pool`.

That works and reads badly, and it couples every handler to the storage location. A dependency fixes both:

```python
def get_pool(request: Request) -> Pool:
    return request.app.state.pool

def modules(pool: Pool = Depends(get_pool)):
    ...
```

Now the handler receives a `Pool`, knows nothing about `app.state`, and can be tested by overriding one dependency. That is the shape worth using.

## Failing loudly

An exception before the `yield` prevents the application from starting.

That is the right behaviour and the right moment. A missing database URL, an unreachable dependency, an invalid configuration &mdash; all are better as a process that refuses to start than as an application that accepts traffic and fails every request.

Validating settings in the lifespan, or importing a settings model that validates itself, turns a class of runtime mystery into a startup error with a message.

## Startup or import time?

Module-level code runs when the module is imported. That sounds equivalent and is not.

A test collector imports your application module to find the app object. So does a documentation generator, a linter with type checking, and anything that inspects routes. If connecting to a database happens at import, all of those need a database.

Startup runs when the application actually starts &mdash; which a test can choose to do, or not.

The practical rule: define things at import, *create* them at startup. `pool = None` at module level and the real construction in the lifespan.

## Shutdown is not guaranteed

Worth knowing before relying on it.

Graceful shutdown runs the code after the `yield`. A `SIGKILL`, a container OOM, or a hardware failure does not. Anything whose absence would corrupt state must not depend on shutdown running.

In practice: close connections there because it is tidy, and do not *rely* on it for correctness. Anything that must be consistent should be consistent at every moment, not reconciled on the way out.

## The older spelling

You will see this in existing code:

```python
@app.on_event("startup")
async def startup(): ...
```

It works and is deprecated. The lifespan context manager replaced it because it keeps setup and teardown in one function, where the relationship between them is visible, and because it can hold state in local variables rather than globals.

New code should use `lifespan`. Old code is worth migrating when touched.


## Mistakes people make

**Connecting at import.** Every test collector, linter and documentation generator then needs a live database. Define at import; create at startup.

**Assuming it runs once per application.** It runs once per **worker**. Four workers means four pools and four model loads - and a migration placed there runs four times concurrently on first deploy.

**Relying on shutdown.** A SIGKILL, an OOM or a hardware failure skips it. Close things there for tidiness; do not depend on it for correctness.

**Reaching for `request.app.state` in every handler.** It couples each one to where the object is stored. A dependency hands over the object itself and can be overridden in a test.

**Swallowing startup failures.** A missing setting should stop the process, not produce an application that accepts traffic and fails every request.

**Using `@app.on_event`.** Deprecated. The lifespan context manager keeps setup and teardown in one function where their relationship is visible.

## In tests

`TestClient(app)` does **not** run the lifespan. Used as a context manager it does:

```python
with TestClient(app) as client:
    ...
```

Both are useful. An isolated unit test with dependencies overridden is faster and cleaner without startup; an integration test that should exercise the real wiring needs it.

Knowing the difference explains the common confusion of a test failing because `app.state.pool` does not exist - the startup that would have created it never ran.

## What belongs in it

A short list, because the boundary is what the module is really about.

**Yes**: connection pools, HTTP clients, loaded models, caches, warmed configuration, anything expensive with a process lifetime.

**No**: anything per request - a session, a transaction, a user. Those are dependencies.

**Definitely not**: anything that must happen exactly once for the whole application. Migrations, scheduled job registration, leader election. With four workers those run four times, concurrently, on every deploy.

That last category is the one that causes incidents, and the fix is not FastAPI's: it belongs in a deployment step that runs once, before the workers start.

## Testing around it

Because the lifespan is opt-in for `TestClient`, most unit tests skip it and are better for skipping it - dependencies are overridden anyway, so the pool never needed to exist.

Where it matters is the integration test that should prove the wiring works: that startup succeeds with real settings, that what it creates is reachable, and that shutdown does not raise. One such test per application is usually enough, and it catches the class of failure where everything passes and the process will not boot.

## Summary

A lifespan is an async context manager: before the `yield` is startup, after it is shutdown, and in between the application serves requests.

It runs once per process - which means once per worker, so four workers build four of everything and anything that must happen exactly once does not belong there.

Create expensive, long-lived things there rather than at import, so a test collector does not need a database. Put them on `app.state` and hand them to handlers through a dependency, so the handlers stay unaware and overridable.

Fail loudly before the `yield` when configuration is missing, and do not depend on shutdown running - a killed process never reaches it.

## Two lifetimes, restated

Almost everything in this track has been per request. This module is the exception, and holding the two apart is what the module is for.

**Per process**: the connection pool, the HTTP client, the loaded model, the cache client, the parsed configuration. Expensive, reusable, created once.

**Per request**: the session taken from that pool, the transaction, the user, the filters. Cheap, disposable, created and released for each caller.

Confusing them produces two distinct failures. A pool created per request is catastrophic for throughput - every caller pays connection setup. A session shared across requests is catastrophic for correctness - two callers inside one transaction, seeing each other's uncommitted work.

The lifespan owns the first category and dependencies own the second, and the `yield` in each has the same shape for the same reason: acquire, use, release.


## Reading a startup that fails

When an application will not boot, the lifespan is usually where to look, and the failure modes are few.

**A missing setting** raises before the `yield`, and the message names the field if configuration is a validated model. This is the good case: loud, early, and specific.

**An unreachable dependency** - a database that is not up yet - raises a connection error. In an orchestrated deployment this is often a race rather than a fault, and the fix is a readiness probe or a retry with backoff rather than removing the check.

**A blocking call in an async lifespan** hangs rather than failing, which is the confusing one. The process starts, never becomes ready, and nothing is logged. The rule from the async module applies here too.

**Work that should have run once** - a migration - appears to succeed on one worker and deadlock on the others.

Knowing that list turns "it will not start" into four things to check in order.

## One habit

Put a log line at the end of startup naming what was created and the settings that matter. It costs nothing and it turns every future boot problem into a question of which line was the last one printed.


## A closing thought

The lifespan is the only place in a FastAPI application that knows about the process rather than the request, and that makes it the natural home for a specific kind of mistake: doing something once that should happen once *per application*.

Four workers is the default shape of a production deployment, and every one of them runs this code. A pool per worker is correct and intended. A migration per worker is a race. A scheduled job registered per worker is four schedulers.

The distinction is not obvious from inside the function, because nothing about `async def lifespan(app)` suggests it will run four times. Knowing that it will is most of using it correctly.

## Next

Testing what has been built - the client that needs no server, the overrides that remove the database, and what a suite should actually assert.

## In one line

Startup and shutdown run once per worker, not once per application - so create expensive long-lived things there, hand them over through a dependency, fail loudly if configuration is missing, and put anything that must happen exactly once somewhere that runs exactly once.

One log line at the end of startup, naming what was created, turns every future boot problem into a question of which line was the last one printed.
''',
    [
        {"q": "How often does a lifespan startup body run?",
         "options": ["Per request", "Once per process - and so once per worker", "Once per route", "Once globally"],
         "answer": 1,
         "why": "Four workers means four pools and four model loads. It also means a migration in startup runs four times concurrently on first deploy, which is why that does not belong there."},
        {"q": "Why prefer startup over import-time work?",
         "options": ["It is faster", "An import happens whenever anything loads the module, including a test collector", "Imports are deprecated", "No difference"],
         "answer": 1,
         "why": "Connecting at import means every test run, linter and documentation generator needs a live database. Define at import, create at startup."},
        {"q": "How should a handler get at a pool created in the lifespan?",
         "options": ["request.app.state.pool directly", "Through a dependency that reads app.state", "A global", "It cannot"],
         "answer": 1,
         "why": "The dependency gives the handler the object itself, keeps it unaware of where it is stored, and makes it replaceable with one override in a test."},
        {"q": "Can you rely on shutdown code always running?",
         "options": ["Yes, always", "No - SIGKILL, an OOM or a hardware failure skips it", "Only in production", "Only for async apps"],
         "answer": 1,
         "why": "Close things there because it is tidy, but anything whose absence would corrupt state must be consistent at every moment rather than reconciled on the way out."},
    ],
)


# ---------------------------------------------------------------------------
# 23. Testing
# ---------------------------------------------------------------------------
topic(
    "testing_fastapi",
    "Testing",
    "In Practice",
    "A client that calls the app directly, no server, and what a good FastAPI test "
    "suite actually asserts.",
    _svg(_box(14, 20, 56, 24, S) + _txt(42, 36, "TestClient", M, 8) +
         _arrow(74, 32, 90, 32) +
         _box(94, 20, 52, 24, S, A) + _txt(120, 36, "app", A, 8) +
         _txt(80, 64, "no socket, no port", M, 8)),
    [
        ("The client calls the app, not a server",
         "There is no network. The client builds the ASGI scope and invokes the "
         "application, which is why tests are fast and need no port.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
DB = {}

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)

@app.post("/modules", status_code=201)
def create(body: ModuleIn):
    i = len(DB) + 1
    DB[i] = body.title
    return {"id": i, "title": body.title}

@app.get("/modules/{i}")
def read(i: int):
    return {"id": i, "title": DB[i]}

client = TestClient(app)
r = client.post("/modules", json={"title": "Vectors"})
print("create:", r.status_code, r.json())
print("read  :", client.get("/modules/1").json())'''),

        ("Assert on status first, body second",
         "The status is the contract; the body is the detail. A test that only "
         "checks the body passes when the endpoint starts failing.",
         '''from fastapi import FastAPI, HTTPException

app = FastAPI()
DB = {1: "Vectors"}

@app.get("/modules/{i}")
def read(i: int):
    if i not in DB:
        raise HTTPException(404, "Module not found")
    return {"id": i, "title": DB[i]}

client = TestClient(app)

def check(path, expected_status):
    r = client.get(path)
    ok = r.status_code == expected_status
    print("%-14s -> %s  %s" % (path, r.status_code, "ok" if ok else "MISMATCH"))
    return r

check("/modules/1", 200)
check("/modules/99", 404)
check("/modules/abc", 422)'''),

        ("Testing validation properly",
         "Assert on <code>loc</code> and <code>type</code>, never on the message "
         "&mdash; prose gets reworded and the suite starts failing for nothing.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class ModuleIn(BaseModel):
    title: str = Field(min_length=3)
    minutes: int = Field(gt=0)

@app.post("/modules")
def create(body: ModuleIn):
    return {"ok": True}

client = TestClient(app)
r = client.post("/modules", json={"title": "x", "minutes": 0})

found = {(tuple(e["loc"]), e["type"]) for e in r.json()["detail"]}
expected = {(("body", "title"), "string_too_short"),
            (("body", "minutes"), "greater_than")}

print("status  :", r.status_code)
for loc, kind in sorted(found):
    print("   ", loc, kind)
print("matches :", found == expected)'''),

        ("Overriding what the endpoint depends on",
         "The point of declaring dependencies: a test replaces the database and the "
         "user without touching the handler.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

def get_db():
    raise RuntimeError("no database in a test")

def current_user(x_token: str = Header(default="")):
    raise HTTPException(401, "Sign in")

@app.get("/mine")
def mine(db=Depends(get_db), user=Depends(current_user)):
    return {"user": user["name"], "rows": db["rows"]}

app.dependency_overrides[get_db] = lambda: {"rows": ["Vectors"]}
app.dependency_overrides[current_user] = lambda: {"name": "test-user"}

print(TestClient(app).get("/mine").json())
app.dependency_overrides.clear()
print("cleared, so the next test starts from the real thing")'''),

        ("Testing one router alone",
         "Include a router into a small app built for the test, and the rest of the "
         "application is not involved.",
         '''from fastapi import APIRouter, FastAPI

# Somewhere in the application:
modules = APIRouter(prefix="/modules", tags=["modules"])

@modules.get("")
def list_modules():
    return ["Vectors", "Norms"]

@modules.get("/{i}")
def read(i: int):
    return {"id": i}

# In the test: an app containing only what is under test.
app = FastAPI()
app.include_router(modules)

c = TestClient(app)
print(c.get("/modules").json())
print(c.get("/modules/7").json())
print()
print("No startup, no other routers, no unrelated dependencies.")'''),

        ("Checking the contract itself",
         "The schema is worth asserting on: a response model quietly removed is a "
         "breaking change no functional test would catch.",
         '''from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ModuleOut(BaseModel):
    id: int
    title: str

@app.get("/modules/{i}", response_model=ModuleOut)
def read(i: int):
    return {"id": i, "title": "Vectors", "internal": "secret"}

spec = app.openapi()
schema = spec["components"]["schemas"]["ModuleOut"]

print("documented fields:", sorted(schema["properties"]))
print("required         :", sorted(schema["required"]))
print()
r = TestClient(app).get("/modules/1")
print("response         :", r.json())
print("no leak          :", "internal" not in r.json())'''),
    ],
    [
        "<code>TestClient</code> builds the ASGI scope and calls the app directly. No server, no port, no network &mdash; which is why the tests are fast.",
        "Assert the status code first. A test that only checks the body passes when the endpoint starts returning the wrong status.",
        "For validation, assert on <code>loc</code> and <code>type</code>. Messages are prose and get reworded.",
        "<code>dependency_overrides</code> is what makes an endpoint testable without a database or a token &mdash; and clearing it between tests is not optional.",
        "A router can be included into a small app built for one test file, so the rest of the application is not involved.",
        "Assert on the generated schema too: a removed <code>response_model</code> is a breaking change that no functional test notices.",
    ],
    '''
title: Testing
intro: A client that calls the app directly, and what a good FastAPI test suite actually asserts.
## No server involved

`TestClient` does not start anything. It builds the ASGI scope a server would build, calls your application, and turns the response messages back into an object with `.status_code` and `.json()`.

That is why FastAPI tests are fast: no socket, no port, no process, no waiting for something to come up. A test suite of several hundred endpoint tests runs in seconds.

It is also why the editors on these pages work at all &mdash; they use the same idea.

In real code the import is `from fastapi.testclient import TestClient`, and it wraps httpx. It needs `httpx` installed, which is the usual reason a first test fails on a fresh environment.

## What to assert

**Status first.** It is the contract, and it is what every client branches on. A test that checks only the body will keep passing when a 200 quietly becomes a 500 with an error body that happens to contain the key you looked for.

**Then the body**, on the fields that matter. Asserting the whole payload makes a test that fails every time an unrelated field is added &mdash; brittle in a way that teaches people to update tests without reading them.

**For validation failures**, assert on `loc` and `type`. Never on `msg`: it is prose, it gets reworded between releases, and a suite that fails on wording is one people learn to ignore.

## Overrides are the point

Everything the dependencies tier argued for pays off here.

An endpoint declaring `Depends(get_db)` and `Depends(current_user)` is tested with neither a database nor a token, because both are replaced at the app level. The handler is unchanged; only what it depends on moves.

Two rules from that module apply directly. Fake at the **edges** &mdash; the database, the clock, the token decoder &mdash; so the real logic above them still runs. And **clear between tests**, or one test silently changes the next and the failure appears somewhere unrelated.

In pytest the shape is a fixture that sets, yields and clears.

## Testing a router alone

A router can be included into an app built for a single test file:

```python
app = FastAPI()
app.include_router(modules.router)
client = TestClient(app)
```

That test exercises one resource, with no other routers, no startup work and no unrelated dependencies. It is the quiet benefit of splitting an application up, and it is the difference between "the tests need a database, Redis and three environment variables" and "the tests need the module under test".

## Lifespan in tests

`TestClient` does not run the lifespan unless you ask. Used as a context manager it does:

```python
with TestClient(app) as client:
    ...
```

Which you want depends on the test. For a unit test of one endpoint with everything overridden, skipping startup is faster and more isolated. For an integration test that should exercise the real wiring, the context-manager form is correct.

Knowing the difference explains a common confusion: a test that fails with `app.state.pool` missing is a test that never ran startup.

## What functional tests miss

Two things worth asserting separately.

**The schema.** Removing a `response_model`, renaming a field, or loosening a type is a breaking change for consumers, and a functional test that checks `r.json()["id"]` will not notice. Asserting on `app.openapi()` &mdash; that a model has the fields it should, that an endpoint documents its 404 &mdash; catches contract changes.

**What is not in the response.** A test that the payload contains `id` and `title` passes just as happily when it also contains `password_hash`. If an endpoint filters something out, assert that it is absent, not merely that the wanted fields are present.

## A suite worth having

For each endpoint: the success case with the values you expect, one validation failure asserting `loc` and `type`, and one domain failure &mdash; the 404 or the 409.

Beyond that: one test per dependency that can reject, so the 401 and 403 paths are covered; and a small number of tests that assert on the schema for endpoints with consumers.

That is a few short functions per endpoint, and between them they cover the branches most likely to be wrong. The parts people skip &mdash; the error paths &mdash; are the parts that get exercised most in production.


## Mistakes people make

**Asserting only on the body.** A 200 that becomes a 500 carrying a similar key keeps the test green. Status first.

**Asserting on `msg`.** It is prose, it gets reworded, and a suite that fails on wording is one people stop reading. Use `loc` and `type`.

**Asserting the whole payload.** Then every unrelated field addition breaks the test, which teaches people to update tests without reading them.

**Forgetting to clear overrides.** One test changes the next, and the failure appears somewhere unrelated with no visible cause.

**Faking too high.** Overriding the permission dependency skips the permission logic you meant to test. Fake the edges.

**Never running the lifespan.** Then `app.state` is empty, and the error names neither the cause nor the fix.

**Only testing the happy path.** The error branches are the ones exercised most in production and least in the suite.

## What a suite should contain

Per endpoint: the success case with the values you expect; one validation failure asserting `loc` and `type`; one domain failure - the 404 or the 409.

Across the application: one test per dependency that can reject, so the 401 and 403 paths are covered; and a handful asserting on `app.openapi()` for endpoints with real consumers, since a removed `response_model` is a breaking change no functional test notices.

That is a few short functions per endpoint, and it covers the branches most likely to be wrong.

## Speed and what it buys

A FastAPI suite is fast by default, and the speed is worth protecting because it changes how the tests get used.

There is no server, so no startup cost per test. With dependencies overridden there is no database, so no fixtures to load or transactions to roll back. Several hundred endpoint tests running in a couple of seconds is normal.

That matters because a suite people run constantly catches things a suite people run at the end does not. The moment it takes a minute, it stops being run between edits.

Two things erode it. Real I/O creeping back in through a dependency somebody forgot to override, and integration tests that construct the whole application per test rather than per module.

Both are worth watching, because the decline is gradual and the point where it stops being run is not announced.

## The parts people skip

Error paths, and they are the ones exercised most in production.

A test that a missing resource gives 404, a duplicate gives 409, a bad payload gives 422 with the right `loc`, and an unauthenticated request gives 401 costs four short functions - and covers the branches most likely to be wrong, because they are the branches nobody exercises by hand.

## Summary

`TestClient` builds the ASGI scope and calls the app directly, so there is no server, no port and no waiting.

Assert the status first and the body second. For validation, assert `loc` and `type` rather than the message. Override dependencies to remove the database and the token, fake at the edges, and clear between tests.

Include a router into a small app to test one resource alone. Use the context-manager form when the test should exercise startup. And assert on the generated schema for anything with consumers, because a removed `response_model` is a breaking change nothing else catches.

## What makes an endpoint hard to test

Worth naming, because the answer is usually a design signal rather than a testing problem.

**Work in the handler.** Logic that only exists inside a request can only be tested through one. Moving it to a service makes it a function call.

**Reaching instead of declaring.** A handler calling `get_session()` in its body cannot be given a fake; one declaring `Depends(get_session)` can.

**Too many dependencies.** If a test needs six overrides, the endpoint is entangled with six things - and the fixture count is a fair measure of that.

**Import-time side effects.** If importing the module connects to something, every test pays, and the suite cannot run without the world being present.

Each of those makes tests awkward and each is fixed by a change to the application rather than to the test. When a test is hard to write, the useful first question is what the endpoint is doing that it should not.


## What to test, and what not to

A suite is a set of choices about what is worth the maintenance, and two extremes are both wrong.

**Testing every branch of every handler** produces a suite that breaks on every refactor and gets updated without being read.

**Testing only the happy paths** leaves the branches that actually run in production - the 404, the 422, the 401 - entirely uncovered.

The middle is per endpoint: the success case, one validation failure, one domain failure. Then, across the application, one test per dependency that can reject, and a few asserting on the schema for anything with consumers.

That is small enough to keep and specific enough to be worth keeping. The measure is whether a failure tells you what broke without opening the test - and asserting on status, `loc` and `type` is what makes it do that.


## A closing thought

The reason FastAPI applications tend to be well tested is not discipline. It is that the framework removed the usual excuses.

There is no server to start, so tests are fast. Dependencies are declared rather than reached for, so they can be replaced. Routers can be included one at a time, so a test can be narrow. Validation happens at the boundary, so handlers have less to test.

What remains is writing the tests, and the shape is small: success, validation failure, domain failure, per endpoint.

## Next

The document all of this generates - and how much of an API's usability is decided by how carefully it was filled in.

## In one line

No server, no port, no network: assert the status first, `loc` and `type` for validation, override at the edges, clear between tests, and cover the error branches, because those are the ones production exercises most and suites cover least.

The measure of a suite is whether a failure tells you what broke without opening the test file. Asserting on the status, the `loc` and the `type` is what makes it do that; asserting on prose and whole payloads is what stops it.

And keep one test with nothing overridden, exercising the real dependency tree. Heavy faking has a failure mode of its own: the fakes quietly stop resembling what they stand in for, and every test keeps passing while the application stops working.
''',
    [
        {"q": "What does TestClient actually do?",
         "options": ["Starts a server on a port", "Builds the ASGI scope and calls the app directly", "Mocks the framework", "Runs uvicorn"],
         "answer": 1,
         "why": "No socket, no process, no waiting for anything to come up - which is why hundreds of endpoint tests run in seconds."},
        {"q": "Why assert on the status code before the body?",
         "options": ["It is faster", "A body-only test keeps passing when a 200 becomes a 500 carrying a similar key", "Bodies are unstable", "It is required"],
         "answer": 1,
         "why": "The status is the contract every client branches on. Checking only the body leaves the most important change undetected."},
        {"q": "Your test fails because `app.state.pool` is missing. What is likely wrong?",
         "options": ["The pool is broken", "The lifespan never ran - TestClient only runs it when used as a context manager", "A missing override", "A bad route"],
         "answer": 1,
         "why": "`with TestClient(app) as client:` runs startup and shutdown. Plain construction does not, which is often what you want for an isolated unit test."},
        {"q": "Which breaking change would a normal functional test miss?",
         "options": ["A 500", "Removing a response_model, so extra fields start leaking", "A wrong status", "A validation failure"],
         "answer": 1,
         "why": "A test checking `r.json()[\"id\"]` passes happily when the payload also gained `password_hash`. Assert on what should be absent, and on the schema."},
    ],
)


# ---------------------------------------------------------------------------
# 24. OpenAPI and the docs
# ---------------------------------------------------------------------------
topic(
    "openapi_and_docs",
    "OpenAPI and the Docs",
    "In Practice",
    "The document your annotations generate, and how much of an API's usability is "
    "decided by it.",
    _svg(_box(14, 18, 52, 22, S, A) + _txt(40, 33, "models", A, 8) +
         _arrow(70, 29, 84, 29) +
         _box(88, 18, 58, 22, S) + _txt(117, 33, "openapi.json", M, 7) +
         _arrow(80, 46, 80, 58) + _txt(80, 74, "/docs  ·  clients  ·  tests", M, 7)),
    [
        ("The document, and where it comes from",
         "<code>app.openapi()</code> assembles one OpenAPI document from every model "
         "and signature. Nothing else was written to produce it.",
         '''import json
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="VizLearn API", version="2.1.0",
              description="Runnable explainers, as an API.")

class ModuleOut(BaseModel):
    id: int
    title: str = Field(description="Shown as the page heading.")

@app.get("/modules/{i}", response_model=ModuleOut, tags=["modules"])
def read(i: int):
    """Return one module by id."""
    return {"id": i, "title": "Vectors"}

spec = app.openapi()
print("openapi :", spec["openapi"])
print("info    :", spec["info"]["title"], spec["info"]["version"])
print("paths   :", list(spec["paths"]))
op = spec["paths"]["/modules/{i}"]["get"]
print("summary :", op["summary"])
print("desc    :", op["description"].strip())
print("tags    :", op["tags"])'''),

        ("Tags organise it",
         "Tags group endpoints into sections, and metadata on the app gives each "
         "section a description.",
         '''from fastapi import APIRouter, FastAPI

tags_meta = [
    {"name": "modules", "description": "Individual explainers."},
    {"name": "tracks", "description": "Ordered collections of modules."},
]

app = FastAPI(openapi_tags=tags_meta)

modules = APIRouter(prefix="/modules", tags=["modules"])
tracks = APIRouter(prefix="/tracks", tags=["tracks"])

@modules.get("")
def list_modules(): return []

@tracks.get("")
def list_tracks(): return []

app.include_router(modules)
app.include_router(tracks)

spec = app.openapi()
for t in spec["tags"]:
    print("%-8s %s" % (t["name"], t["description"]))
print()
for path, ops in spec["paths"].items():
    for method, op in ops.items():
        print("  %-6s %-10s %s" % (method.upper(), path, op["tags"]))'''),

        ("Examples fill the Try it out form",
         "The single highest-value thing you can add: a caller gets a working "
         "request instead of an empty box.",
         '''import json
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()

class ModuleIn(BaseModel):
    model_config = ConfigDict(json_schema_extra={
        "examples": [{"title": "Dot Product", "minutes": 11}]})

    title: str = Field(min_length=3, description="Shown as the page heading.",
                       examples=["Dot Product"])
    minutes: int = Field(default=10, gt=0, le=180,
                         description="Estimated reading time.")

@app.post("/modules", status_code=201)
def create(body: ModuleIn):
    return body

schema = app.openapi()["components"]["schemas"]["ModuleIn"]
print(json.dumps(schema, indent=2))'''),

        ("Documenting the failures",
         "<code>responses=</code> puts the error shapes in the document, so a "
         "generated client can type them.",
         '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ModuleOut(BaseModel):
    id: int

class Problem(BaseModel):
    detail: str

@app.get("/modules/{i}", response_model=ModuleOut,
         responses={404: {"model": Problem, "description": "No such module"},
                    409: {"model": Problem, "description": "Withdrawn"}})
def read(i: int):
    if i != 1:
        raise HTTPException(404, "No such module")
    return {"id": 1}

op = app.openapi()["paths"]["/modules/{i}"]["get"]
for code, spec in sorted(op["responses"].items()):
    print("%-4s %s" % (code, spec.get("description")))'''),

        ("Hiding what should not be published",
         "<code>include_in_schema=False</code> keeps an internal endpoint out of the "
         "document while leaving it working.",
         '''from fastapi import FastAPI

app = FastAPI()

@app.get("/modules")
def public(): return []

@app.get("/internal/flush", include_in_schema=False)
def internal(): return {"flushed": True}

@app.get("/legacy", deprecated=True)
def legacy(): return {"old": True}

spec = app.openapi()
print("documented :", sorted(spec["paths"]))
print("still works:", TestClient(app).get("/internal/flush").json())
print("deprecated :", spec["paths"]["/legacy"]["get"].get("deprecated"))
print()
print("Undocumented is not the same as protected - it is only invisible.")'''),

        ("Reading it as a review",
         "One line, and you see what a consumer sees. It is the fastest review "
         "available for an API model.",
         '''from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class Thing(BaseModel):
    id: int
    weight: float                 # of what? in what unit?

@app.get("/things", response_model=list[Thing])
def things(sort: str = Query(default="id")):   # str, so anything goes
    return []

spec = app.openapi()
props = spec["components"]["schemas"]["Thing"]["properties"]
params = spec["paths"]["/things"]["get"]["parameters"]

print("fields without a description:")
for name, p in props.items():
    if "description" not in p:
        print("   ", name, p.get("type"))
print()
print("parameters with no constrained set:")
for p in params:
    if p["schema"].get("type") == "string" and "enum" not in p["schema"]:
        print("   ", p["name"], "- a Literal would document the options")'''),
    ],
    [
        "<code>app.openapi()</code> assembles the document from your models and signatures. The docs page at <code>/docs</code> renders it.",
        "<code>title</code>, <code>version</code> and <code>description</code> on <code>FastAPI()</code> become the document's header; a function's docstring becomes an endpoint's description.",
        "Tags group endpoints into sections, and <code>openapi_tags</code> gives each section a description.",
        "<code>examples</code> pre-fill the interactive request form &mdash; the difference between a caller's first attempt working and being a guess.",
        "<code>responses=</code> documents the failure shapes, which is what lets a generated client type its errors.",
        "<code>include_in_schema=False</code> hides an endpoint from the document without protecting it. Undocumented is not private.",
    ],
    '''
title: OpenAPI and the Docs
intro: The document your annotations generate, and how much of an API's usability is decided by it.
## What is generated

`app.openapi()` returns one OpenAPI document describing every route: paths, methods, parameters, request bodies, response shapes, status codes, descriptions and examples.

It is assembled from things you already wrote &mdash; the path in the decorator, the parameters in the signature, the models, the constraints, the docstrings. There is no separate specification to maintain and no way for it to drift, because it *is* the code.

FastAPI serves it at `/openapi.json`, renders it at `/docs` (Swagger UI) and `/redoc` (ReDoc).

## The header

`FastAPI(title=..., version=..., description=...)` becomes the top of the document and the top of the docs page.

The `description` supports Markdown and is the one piece of genuine prose in the whole thing. It is worth writing: what the API is for, how authentication works, what the rate limits are, where to get a key. That is the first thing a new consumer reads, and the alternative is that they read nothing.

`version` should be your API's version, not your library's. Consumers pin against it.

## Tags

Tags group endpoints into sections. On a router, `tags=["modules"]` applies to every route in it.

`openapi_tags` on the app gives each tag a description, which becomes a paragraph above that section in the docs.

For an API past a dozen routes this is the difference between a navigable document and a flat alphabetical list. It costs one argument per router.

## Examples are the highest-value addition

Everything else in this module is worth doing. This is the one that changes whether people succeed.

A `Field(examples=[...])` or a model-level `json_schema_extra={"examples": [...]}` pre-fills the interactive form. A developer opens `/docs`, presses **Try it out**, and gets a request that works &mdash; instead of an empty box they have to guess at, with a 422 for their first three attempts.

That difference is measurable in how many integrations get finished.

Write examples that are realistic rather than minimal. `"title": "string"` is what the generator produces without you; `"title": "Dot Product"` shows what the field is actually for.

## Documenting failures

`response_model` covers the success case. Everything else is undocumented unless you say so:

```python
responses={404: {"model": Problem, "description": "No such module"}}
```

Worth doing for the failures a caller is expected to handle. A generated client can then type its errors, and a human reading the docs knows what a rejection looks like before causing one.

## Hiding endpoints

`include_in_schema=False` keeps a route out of the document. Useful for internal endpoints, legacy paths kept for one client, and health checks that would only clutter the page.

One warning worth being explicit about: **this is not access control.** The endpoint still works, still accepts requests, and is exactly as reachable as before. It is invisible, not protected. If it should not be called, it needs a dependency, not a flag.

`deprecated=True` is the other half of retiring something: the endpoint keeps working and the docs show it as deprecated, which gives consumers a signal without breaking them.

## Reading it as a review

The most practical use of this module. One line:

```python
print(json.dumps(app.openapi(), indent=2))
```

and you see exactly what your consumers see.

What it reliably surfaces: fields whose names are not self-explanatory and have no description; a `str` parameter where a `Literal` would have given clients a set of options; a rule enforced by a validator that appears nowhere; a required field you meant to default; an endpoint with no example.

The last editor above automates two of those checks. It is worth running over a real model, because the results are usually uncomfortable and always cheap to fix.

## What it feeds

The document is read by more than the docs page, which is why its quality compounds.

**Client generators** produce typed clients in a dozen languages from it. A vague schema produces a vague client, and every consumer then writes their own guesses.

**Contract tests** can assert that a change did not break the published shape.

**API gateways** can validate requests before they reach you.

**LLM tooling** increasingly reads schemas to decide how to call an API.

None of those read your source. All of them read this.

## The limits

Some things cannot be expressed, and pretending otherwise misleads consumers.

Validator logic, cross-field rules, anything requiring a lookup &mdash; none has a JSON Schema equivalent. Where a rule matters and cannot be declared, put it in the docstring or the model's description, so at least a human reading the documentation learns about it.

An endpoint whose real constraints live in code the schema cannot see is an endpoint whose documentation is quietly incomplete.


## Mistakes people make

**Treating `include_in_schema=False` as security.** The endpoint still works and is exactly as reachable. Invisible is not protected.

**Leaving fields undescribed.** `weight` needs a description - of what, in what unit. A name that is not self-explanatory and has no description produces documentation that technically exists.

**No examples.** The generated placeholder is `"string"`. A caller's first three attempts then return 422, and some of them stop there.

**Documenting only success.** An endpoint that can 404 should say so, or a generated client has no type for failure.

**Using `str` where a `Literal` belongs.** The schema then offers no options, so no client can render a choice and no consumer knows what is valid.

**Never looking at it.** It is one line, and it is the only view of your model that matches what consumers receive.

**Versioning it with the library version.** Consumers pin against your API's version, not your package's.

## The review worth doing

Print the document for a model you have just written and read it as a stranger.

What it surfaces: required fields you meant to default, patterns that should have been enumerations, rules that live in validators and appear nowhere, endpoints with no summary, and fields whose names carry meaning only to whoever wrote them.

Every one of those is cheap to fix at that moment and expensive once clients exist, because by then the shape is a contract.

## Next

Putting the pieces together: how a FastAPI project is laid out once it is more than one file.


## What it costs to skip

An API without a good document still works, and the cost is paid by everyone else.

Every consumer writes their own guesses about shapes. Every generated client is untyped. Every question that could have been answered by reading becomes a message to whoever wrote it. And every change is potentially breaking, because nobody wrote down what the contract was.

The work to avoid that is small and front-loaded: a description on the app, tags on the routers, descriptions on the fields whose names are not obvious, one example per body model, and `responses=` on the failures a caller is expected to handle.

An hour, once, and it is read by every person and tool that touches the API afterwards.

## The chain it feeds

Worth holding in mind, because it explains why small omissions matter.

Your models generate schemas. FastAPI assembles them into one document. That document is read by the interactive docs, by client generators in several languages, by API gateways, by contract-testing tools, and increasingly by LLM tooling deciding how to call you.

A missing description is missing in all of them. So is a `str` that should have been a `Literal`. None of those tools read your source code, and none of them can ask.

## Summary

The document is generated from your models, signatures, decorators and docstrings, and served at `/openapi.json`, `/docs` and `/redoc`.

Give the app a title, version and description; group routes with tags and describe the groups with `openapi_tags`; document failures with `responses=`; and write examples, which are the single highest-value addition because they turn a caller's first attempt from a guess into a working request.

`include_in_schema=False` hides without protecting. And the fastest review available for any API model is printing the document and reading it as a stranger would.

## The limits, stated plainly

Some things cannot be expressed, and knowing which keeps the documentation honest.

**Validator logic** has no schema equivalent. A rule enforced by a `field_validator` is invisible to every consumer.

**Cross-field rules** likewise. "End date must be after start date" appears nowhere.

**Anything needing a lookup** - does this reference exist, is this name taken - is not expressible and should not be attempted.

**Custom serialisation** changes output without changing the schema unless `return_type` is set, which is how a document quietly starts describing something the endpoint no longer returns.

Where a rule matters and cannot be declared, put it in the model's docstring or the field's description. It will not be machine-readable, and a human reading the documentation will at least learn it exists rather than discovering it through a rejection.


## Who reads it

Worth being concrete, because the audience is larger than the docs page.

**A developer integrating with you** opens `/docs`, presses Try it out, and either gets a working request or does not. That first minute decides how the rest goes.

**A client generator** turns the document into a typed library. Its quality is entirely your schema's quality.

**A gateway** may validate requests against it before they reach your process.

**A contract test** can assert that today's document is compatible with yesterday's.

**An LLM** increasingly reads it to decide how to call you, and reads only what is written.

None of them can ask a question, and none of them read your source. Everything they know is in the document, which is why the descriptions and examples are not decoration.


## A closing thought

The generated document is the closest thing an API has to a public interface definition, and it is produced entirely as a side effect of writing types.

That is unusual and worth appreciating. In most stacks the specification is a separate artefact that somebody maintains, and it drifts from the implementation immediately because nothing forces them together.

Here it cannot drift, because there is only one source. What varies is how much you put into that source - and the difference between a document consumers can build against and one they have to guess at is a handful of descriptions, one example per model, and a `Literal` where a `str` would have done.

## In one line

Your annotations already wrote your API documentation; the only question is how much you put into them, and the answer is decided by a handful of descriptions, one example per body model, and a `Literal` wherever a `str` would have left a consumer guessing.

And the cheapest habit available is to print the document once for every model you write. Five minutes, no tooling, and it shows you the API as a stranger receives it rather than as its author remembers it.

One more habit worth the minute it costs: after adding an endpoint, open `/docs` and try it as a stranger would. If your own first attempt returns a 422, so will everybody else's, and you are the only person who can still fix it cheaply.
''',
    [
        {"q": "Where does the OpenAPI document come from?",
         "options": ["A YAML file you maintain", "Your models, signatures, decorators and docstrings", "uvicorn", "A plugin"],
         "answer": 1,
         "why": "It is assembled from code you already wrote, which is why it cannot drift from the implementation - it is the implementation."},
        {"q": "What does `include_in_schema=False` do?",
         "options": ["Blocks the endpoint", "Hides it from the document; it still works and is still reachable", "Requires auth", "Deletes the route"],
         "answer": 1,
         "why": "Undocumented is not protected. If an endpoint should not be called, it needs a dependency, not a visibility flag."},
        {"q": "Which addition most improves a first-time caller's experience?",
         "options": ["A longer description", "Examples, which pre-fill the Try it out form with a working request", "More tags", "A version bump"],
         "answer": 1,
         "why": "The alternative is an empty box and a 422 on their first three attempts. Realistic examples change whether integrations get finished."},
        {"q": "A rule lives in a `field_validator`. What does the schema say about it?",
         "options": ["It appears as a constraint", "Nothing - validator logic has no schema equivalent", "It becomes a description", "It raises at startup"],
         "answer": 1,
         "why": "Which is why constraints are preferred where they can express the rule, and why anything left in code should be mentioned in a docstring or description."},
    ],
)


# ---------------------------------------------------------------------------
# 25. Security basics
# ---------------------------------------------------------------------------
topic(
    "security_basics",
    "Security Basics",
    "In Practice",
    "Authentication as a dependency, what a token actually is, and the handful of "
    "mistakes that matter most.",
    _svg(_box(12, 18, 58, 22, S) + _txt(41, 33, "Authorization", M, 7) +
         _arrow(72, 29, 86, 29) +
         _box(90, 18, 56, 22, S, A) + _txt(118, 33, "current_user", A, 7) +
         _txt(80, 64, "401 unknown  ·  403 not allowed", M, 7)),
    [
        ("Reading a bearer token",
         "The header, parsed in one dependency. Every endpoint that needs a user "
         "declares one parameter.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException, status

app = FastAPI()
TOKENS = {"tok-ada": {"name": "ada", "scopes": ["modules:read"]}}

def current_user(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token",
                            headers={"WWW-Authenticate": "Bearer"})
    user = TOKENS.get(authorization[7:])
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token",
                            headers={"WWW-Authenticate": "Bearer"})
    return user

@app.get("/me")
def me(user: dict = Depends(current_user)):
    return user

c = TestClient(app)
print("none  :", c.get("/me").status_code)
print("wrong :", c.request("GET", "/me", headers={"authorization": "Bearer x"}).status_code)
print("ok    :", c.request("GET", "/me",
                           headers={"authorization": "Bearer tok-ada"}).json())'''),

        ("What a signed token actually is",
         "Payload plus a signature made with a secret. Anyone can read it; only the "
         "holder of the secret can produce one.",
         '''import base64, hashlib, hmac, json

SECRET = b"a-server-side-secret"

def b64(raw):  return base64.urlsafe_b64encode(raw).rstrip(b"=")
def unb64(s):  return base64.urlsafe_b64decode(s + b"=" * (-len(s) % 4))

def sign(payload: dict) -> bytes:
    body = b64(json.dumps(payload, separators=(",", ":")).encode())
    mac = hmac.new(SECRET, body, hashlib.sha256).digest()
    return body + b"." + b64(mac)

def verify(token: bytes):
    body, _, given = token.partition(b".")
    expected = b64(hmac.new(SECRET, body, hashlib.sha256).digest())
    if not hmac.compare_digest(given, expected):     # constant time
        return None
    return json.loads(unb64(body))

tok = sign({"sub": "ada", "scopes": ["modules:read"]})
print("token   :", tok.decode()[:52], "...")
print("readable:", json.loads(unb64(tok.split(b".")[0])))
print("verified:", verify(tok))
print("tampered:", verify(b"eyJzdWIiOiJyb290In0.abc"))
print()
print("Signed, not encrypted. Never put a secret in the payload.")'''),

        ("Expiry has to be checked",
         "A signature says the token is genuine. It says nothing about whether it is "
         "still valid.",
         '''import time
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
ISSUED = {"tok-fresh": {"sub": "ada", "exp": time.time() + 3600},
          "tok-stale": {"sub": "ada", "exp": time.time() - 1}}

def current_user(authorization: str = Header(default="")):
    claims = ISSUED.get(authorization.replace("Bearer ", ""))
    if claims is None:
        raise HTTPException(401, "Invalid token")
    if claims["exp"] < time.time():
        raise HTTPException(401, "Token expired")
    return {"name": claims["sub"]}

@app.get("/me")
def me(user: dict = Depends(current_user)):
    return user

c = TestClient(app)
for tok in ["tok-fresh", "tok-stale"]:
    r = c.request("GET", "/me", headers={"authorization": "Bearer " + tok})
    print("%-10s %s %s" % (tok, r.status_code, r.json()))'''),

        ("Scopes, layered as dependencies",
         "Authentication answers who; authorisation answers whether. They are "
         "different questions and different status codes.",
         '''from fastapi import Depends, FastAPI, Header, HTTPException, status

app = FastAPI()
TOKENS = {"reader": ["modules:read"], "editor": ["modules:read", "modules:write"]}

def current_user(x_token: str = Header(default="")):
    if x_token not in TOKENS:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sign in")
    return {"name": x_token, "scopes": TOKENS[x_token]}

class RequireScope:
    def __init__(self, *scopes): self.scopes = set(scopes)
    def __call__(self, user: dict = Depends(current_user)):
        missing = self.scopes - set(user["scopes"])
        if missing:
            raise HTTPException(status.HTTP_403_FORBIDDEN,
                                "Missing scope: %s" % ", ".join(sorted(missing)))
        return user

can_read = RequireScope("modules:read")
can_write = RequireScope("modules:write")

@app.get("/modules")
def read(u: dict = Depends(can_read)): return {"ok": u["name"]}

@app.post("/modules")
def write(u: dict = Depends(can_write)): return {"ok": u["name"]}

c = TestClient(app)
for tok in ["", "reader", "editor"]:
    h = {"x-token": tok} if tok else {}
    print("%-7s GET %s  POST %s" % (tok or "-",
          c.request("GET", "/modules", headers=h).status_code,
          c.request("POST", "/modules", headers=h).status_code))'''),

        ("Not leaking which one was wrong",
         "A login that says “no such user” tells an attacker which names exist. Say "
         "the same thing either way.",
         '''import hashlib, hmac
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

def digest(password: str, salt: bytes) -> bytes:
    # Illustrative only. A real system uses bcrypt, scrypt or argon2 through
    # a library: those are deliberately SLOW, which is the property that
    # matters and the one a plain hash does not have.
    return hmac.new(salt, password.encode(), hashlib.sha256).digest()

SALT = b"per-user-salt"
USERS = {"ada": digest("correct-horse", SALT)}

class Login(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(body: Login):
    stored = USERS.get(body.username)
    candidate = digest(body.password, SALT)
    # Compare even when the user is unknown, and say one thing either way.
    if stored is None or not hmac.compare_digest(stored, candidate):
        raise HTTPException(401, "Incorrect username or password")
    return {"token": "tok-" + body.username}

c = TestClient(app)
for u, p in [("ada", "correct-horse"), ("ada", "wrong"), ("nobody", "wrong")]:
    r = c.post("/login", json={"username": u, "password": p})
    print("%-8s %-14s %s %s" % (u, p, r.status_code, r.json()))'''),

        ("Keeping secrets out of the response",
         "The response model is the last line of defence, and the one that cannot be "
         "forgotten by a future handler.",
         '''from fastapi import FastAPI
from pydantic import BaseModel, Field, SecretStr

app = FastAPI()

ROW = {"id": 1, "name": "ada", "email": "ada@vizlearn.in",
       "password_hash": "$2b$12$abcdef", "api_token": "tok_live_123"}

class UserOut(BaseModel):
    id: int
    name: str                       # email and secrets simply absent

@app.get("/users/1", response_model=UserOut)
def read():
    return ROW

class UserInternal(BaseModel):
    name: str
    password_hash: str = Field(exclude=True)
    api_token: SecretStr

u = UserInternal(name="ada", password_hash="$2b$12$abcdef", api_token="tok_live_123")

print("public response :", TestClient(app).get("/users/1").json())
print("internal repr   :", u)
print("internal dump   :", u.model_dump())'''),
    ],
    [
        "Authentication belongs in a dependency: stated once, impossible for an endpoint to forget, and it appears in the schema.",
        "<strong>401</strong> means not authenticated and should carry <code>WWW-Authenticate</code>. <strong>403</strong> means authenticated and not allowed. They are different questions.",
        "A signed token is <em>readable</em> by anyone &mdash; signing is not encryption. Never put anything secret in the payload.",
        "A valid signature does not mean a valid token: expiry has to be checked separately, and revocation needs a store.",
        "Compare secrets with <code>hmac.compare_digest</code>, not <code>==</code>, so the comparison does not leak by timing.",
        "A login should say the same thing whether the user is unknown or the password is wrong, or it enumerates accounts.",
    ],
    '''
title: Security Basics
intro: Authentication as a dependency, what a token actually is, and the mistakes that matter most.
## Authentication is a dependency

Everything from the dependencies tier applies here, and this is the case that justifies it.

```python
def current_user(authorization: str = Header(default="")) -> User:
    ...
    raise HTTPException(401, "Invalid token")
```

Stated once. Every endpoint that needs a user declares one parameter, and one that does not, does not. An endpoint cannot forget the check, because if it declares `current_user` then the check ran &mdash; the request could not have reached the handler otherwise.

A section is protected by putting it on the router, so a route added next year inherits it rather than needing somebody to remember.

## 401 and 403

Worth restating because collapsing them is so common.

**401 Unauthorized** actually means *unauthenticated*: I do not know who you are. It should carry a `WWW-Authenticate` header naming the scheme.

**403 Forbidden** means: I know who you are, and no.

A client seeing 401 should obtain credentials or refresh a token. One seeing 403 should not, because retrying as the same person will fail again. Merging them produces a login loop where there should be a message.

Layering them as separate dependencies &mdash; `current_user` raising 401, `require_scope` raising 403 &mdash; makes the distinction structural rather than something each handler decides.

## What a token is

A signed token is a payload plus a signature computed with a server-side secret.

The property that matters, and that people get wrong: **it is signed, not encrypted**. Anyone holding the token can decode and read the payload. The signature proves it was issued by someone with the secret and has not been altered &mdash; nothing more.

So the payload may contain a user id, an expiry, a set of scopes. It must never contain a password, a card number, or anything else that should not be read by whoever holds the token &mdash; which includes anyone who obtains it from a log, a browser's storage, or a proxy.

The second editor above builds and verifies one with nothing but the standard library, because the mechanism is worth seeing once. In production, use a library &mdash; PyJWT or Authlib &mdash; which handles the algorithm choices, the claim conventions and the parsing edge cases that a hand-rolled version gets wrong.

## A signature is not validity

A token can be perfectly signed and still unacceptable.

**Expiry** must be checked explicitly. A signature has no opinion about time.

**Revocation** is harder, and it is the honest weakness of stateless tokens: a signed token stays valid until it expires, so logging out or disabling an account does not stop it. The usual answers are short lifetimes plus refresh tokens, or a denylist &mdash; which reintroduces the state that stateless tokens were meant to avoid.

Pick a short expiry. Fifteen minutes with a refresh flow is a common shape; a token valid for a year is a credential you cannot withdraw.

## Comparing secrets

Use `hmac.compare_digest`, not `==`.

A normal string comparison returns as soon as it finds a difference, so the time it takes reveals how many leading characters were correct. Over enough attempts that is enough to reconstruct a secret. `compare_digest` takes the same time regardless.

This applies to tokens, signatures, API keys and password hashes &mdash; anything an attacker can submit repeatedly.

## Not leaking who exists

A login that returns "no such user" for one input and "wrong password" for another lets anyone enumerate accounts.

Return the same message either way, and perform the hash comparison even when the username is unknown &mdash; otherwise the *timing* difference says what the message did not.

The same reasoning applies to 404 versus 403 on a resource that exists but is not yours: returning 403 confirms it exists. For anything sensitive, 404 for both, consistently.

## Passwords

Two rules, and the second is not optional.

**Never store a password.** Store a hash.

**Never hash it with SHA-256 alone.** General-purpose hashes are designed to be fast, which is exactly the wrong property. Use a deliberately slow, salted algorithm designed for passwords: bcrypt, scrypt or argon2, through a library like `passlib`.

The editor above uses PBKDF2 from the standard library to show the shape without pulling in a dependency. It is better than a bare SHA-256 and it is not what you should ship; the real answer is a library that keeps its parameters current as hardware gets faster.

## Keeping secrets out of responses

The last line of defence, and the one that survives a future handler being careless.

A `response_model` listing only what may be seen cannot leak a field added to the table later. `Field(exclude=True)` keeps a value out of every dump. `SecretStr` keeps it out of `repr`, logs and tracebacks.

Use all three where they fit, and prefer the separate output model, because it is the only one that cannot be forgotten by somebody editing a different file.

## What this module does not cover

Enough to be worth naming: CSRF for cookie-based sessions, CORS configuration, rate limiting, input sanitisation for anything rendered as HTML, dependency scanning, and secrets management.

Each is a real subject. The point of this one is that the *shape* &mdash; authentication as a dependency, authorisation layered on top, secrets kept out of payloads and responses &mdash; is what the framework gives you, and getting that shape right is what makes the rest tractable.


## Mistakes people make

**Putting anything secret in a token payload.** It is signed, not encrypted. Anyone holding it reads it - including from a log, browser storage or a proxy.

**Checking the signature and stopping.** Expiry is a separate check, and a signature has no opinion about whether an account was disabled.

**Long-lived tokens.** A stateless token is valid until it expires, so a year-long token is a credential you cannot withdraw.

**Comparing with `==`.** The timing reveals how many leading characters matched. `hmac.compare_digest` does not.

**Distinct login errors.** "No such user" enumerates accounts - and skipping the hash comparison for an unknown user leaks the same fact through timing.

**Hashing passwords with SHA-256.** Fast is the wrong property. bcrypt, scrypt or argon2, through a library.

**403 on a resource that exists but is not yours.** It confirms existence. For anything sensitive, 404 for both, consistently.

**Trusting a client-supplied identity header.** `X-User-Id` is a claim unless a proxy sets it and strips whatever the client sent.

## What this does not cover

Worth naming so the gaps are known: CSRF for cookie sessions, CORS, rate limiting, sanitising anything rendered as HTML, dependency scanning, and secrets management.

Each is a subject. What this module gives you is the shape - authentication as a dependency, authorisation layered above it, secrets out of payloads and out of responses - and that shape is what makes the rest tractable rather than scattered.

## Where to be careful

Three habits that prevent most of what goes wrong, beyond anything in the editors above.

**Never log credentials.** `Authorization` and `Cookie` are in every request and are the two headers you least want persisted. A logging middleware that dumps headers is a breach waiting for a log aggregator.

**Never put secrets in a URL.** They land in browser history, server logs, proxy logs and `Referer` headers. That is the argument for `Authorization` over `?api_key=`.

**Fail closed.** A permission check that errors should deny, not allow. Code shaped `if not allowed: raise` denies on an exception; code shaped `if denied: raise` permits when the check itself breaks.

## What to reach for

For anything real, use libraries rather than the primitives shown here.

Tokens: PyJWT or Authlib, which handle algorithm choice, claim conventions and the parsing edge cases a hand-rolled version gets wrong - including the `alg: none` family of attacks.

Passwords: passlib with bcrypt or argon2, which keeps its parameters current as hardware gets faster.

OAuth2 and OpenID Connect: FastAPI ships `OAuth2PasswordBearer` and friends, which integrate with the docs so the interactive page can authenticate.

The editors here build things from `hmac` and `hashlib` to show what is underneath. That is worth seeing once and is not what you should ship.

## Summary

Authentication belongs in a dependency: stated once, impossible for an endpoint to forget, and visible in the schema. Authorisation layers above it, and the two produce different status codes for different questions.

A signed token is readable by anyone holding it, so nothing secret goes in the payload. A valid signature is not a valid token - expiry is a separate check and revocation needs state.

Compare secrets in constant time, say the same thing for an unknown user as for a wrong password, hash passwords with something deliberately slow, and let a response model decide what may leave.

## Next

How the pieces are arranged once the application is more than one file: routers per resource, services that know nothing about HTTP, schemas separated by direction, and an assembly file short enough to read at a glance.


## The shape to take away

Authentication is a dependency. Authorisation is a dependency that depends on it. Both raise, so neither can be forgotten by an endpoint that declares them, and both appear in the schema.

Everything else in this module is a detail hung on that frame: what goes in a token, how to compare a secret, what a login should say, what a response model must not contain.

The frame is what the framework gives you. The details are what a review should check before anything real depends on them.


## A closing thought

The most useful thing in this module is not any individual rule. It is that authentication has one place to live.

An application where every endpoint checks a header its own way has as many security models as it has endpoints, and no way to review them. One where every endpoint declares `Depends(current_user)` has one, written down, that a reviewer can read in a minute.

That does not make it correct. It makes it *reviewable*, which is the precondition for it becoming correct.

## A closing note

Security is the area where the framework helps most with shape and least with substance.

`Depends` makes authentication impossible for an endpoint to forget, gives it one place to live, and puts it in the schema. That is genuinely valuable and it is structural - it says nothing about whether your token lifetime is sensible, your hashing is current, or your permission model matches what the business intended.

Those are decisions, and they need review by someone who does this for a living before anything real depends on them. What this module offers is the arrangement that makes such a review possible: rules in one place, expressed once, visible in the signature of every endpoint that relies on them.

## In one line

Authentication is a dependency and authorisation depends on it; a signed token is readable, a valid signature is not a valid token, secrets compare in constant time, logins say one thing either way, and a response model decides what leaves.

And for anything real, use libraries rather than the primitives shown here: they exist because the edge cases are numerous and the consequences of missing one are not proportionate to the effort saved.
''',
    [
        {"q": "Is a signed token encrypted?",
         "options": ["Yes", "No - anyone holding it can read the payload", "Only with HTTPS", "Only the header"],
         "answer": 1,
         "why": "The signature proves origin and integrity, not confidentiality. Nothing secret belongs in the payload, because logs, browser storage and proxies all see it."},
        {"q": "Why use `hmac.compare_digest` instead of `==`?",
         "options": ["It is faster", "`==` returns early, so its timing reveals how many characters were correct", "It handles bytes", "No reason"],
         "answer": 1,
         "why": "Over enough attempts, a timing difference is enough to reconstruct a secret. compare_digest takes constant time."},
        {"q": "A login where the username does not exist. What should it return?",
         "options": ["\"No such user\"", "The same message as a wrong password, after doing the comparison anyway", "A 404", "A 403"],
         "answer": 1,
         "why": "Different messages enumerate accounts - and skipping the hash comparison leaks the same fact through timing even when the message does not."},
        {"q": "A signed token has a valid signature. Is it acceptable?",
         "options": ["Yes", "Not necessarily - expiry and revocation are separate checks", "Only if fresh", "Only with scopes"],
         "answer": 1,
         "why": "A signature has no opinion about time or about whether the account was disabled. That is the honest weakness of stateless tokens, which short lifetimes mitigate."},
    ],
)


# ---------------------------------------------------------------------------
# 26. Project structure
# ---------------------------------------------------------------------------
topic(
    "project_structure",
    "Project Structure",
    "In Practice",
    "How the pieces are arranged once the application is more than one file - and "
    "why the assembly file should be boring.",
    _svg(_box(50, 10, 60, 16, S, A) + _txt(80, 22, "main.py", A, 8) +
         _arrow(64, 28, 36, 40) + _arrow(96, 28, 124, 40) +
         _box(10, 42, 52, 16, S) + _txt(36, 54, "routers", M, 7) +
         _box(98, 42, 52, 16, S) + _txt(124, 54, "services", M, 7) +
         _box(54, 66, 52, 16, S) + _txt(80, 78, "schemas", M, 7)),
    [
        ("A router per resource",
         "The unit that scales. Each file owns one resource's paths and nothing "
         "else.",
         '''from fastapi import APIRouter, FastAPI

# routers/modules.py
modules = APIRouter(prefix="/modules", tags=["modules"])

@modules.get("")
def list_modules(): return ["Vectors"]

@modules.get("/{i}")
def read(i: int): return {"id": i}

# routers/tracks.py
tracks = APIRouter(prefix="/tracks", tags=["tracks"])

@tracks.get("")
def list_tracks(): return ["maths"]

# main.py - assembly, and nothing else
app = FastAPI(title="VizLearn API", version="1.0.0")
app.include_router(modules)
app.include_router(tracks)

c = TestClient(app)
print(c.get("/modules").json(), c.get("/modules/7").json(), c.get("/tracks").json())
print()
for r in app.routes:
    if getattr(r, "methods", None):
        print("  %-6s %s" % (",".join(sorted(r.methods)), r.path))'''),

        ("Handlers stay thin",
         "The handler translates HTTP; the service does the work and imports nothing "
         "from the framework.",
         '''from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field

# services/modules.py - no fastapi import anywhere in here
class ModuleNotFound(Exception):
    def __init__(self, i): self.i = i

DB = {1: {"id": 1, "title": "Vectors"}}

def get_module(i: int) -> dict:
    if i not in DB:
        raise ModuleNotFound(i)
    return DB[i]

def create_module(title: str) -> dict:
    i = max(DB) + 1
    DB[i] = {"id": i, "title": title}
    return DB[i]

# schemas/modules.py
class ModuleIn(BaseModel):
    title: str = Field(min_length=3)

class ModuleOut(BaseModel):
    id: int
    title: str

# routers/modules.py
router = APIRouter(prefix="/modules", tags=["modules"])

@router.get("/{i}", response_model=ModuleOut)
def read(i: int):
    try:
        return get_module(i)
    except ModuleNotFound:
        raise HTTPException(404, "No module %d" % i)

@router.post("", response_model=ModuleOut, status_code=201)
def create(body: ModuleIn):
    return create_module(body.title)

app = FastAPI(); app.include_router(router)
c = TestClient(app)
print(c.post("/modules", json={"title": "Norms"}).json())
print(c.get("/modules/1").json())
print("missing:", c.get("/modules/99").status_code)'''),

        ("Domain errors mapped in one place",
         "Better than the try/except above: the service raises, and one handler "
         "decides the status.",
         '''from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse

class ModuleNotFound(Exception):
    def __init__(self, i): self.i = i

class TitleTaken(Exception):
    def __init__(self, t): self.t = t

DB, TITLES = {1: "Vectors"}, {"Vectors"}

def get_module(i):
    if i not in DB: raise ModuleNotFound(i)
    return {"id": i, "title": DB[i]}

def create_module(title):
    if title in TITLES: raise TitleTaken(title)
    TITLES.add(title); return {"id": 2, "title": title}

router = APIRouter(prefix="/modules")

@router.get("/{i}")
def read(i: int): return get_module(i)          # no try/except

@router.post("")
def create(title: str): return create_module(title)

app = FastAPI()
app.include_router(router)

@app.exception_handler(ModuleNotFound)
async def nf(r: Request, e: ModuleNotFound):
    return JSONResponse(status_code=404, content={"detail": "No module %d" % e.i})

@app.exception_handler(TitleTaken)
async def tt(r: Request, e: TitleTaken):
    return JSONResponse(status_code=409, content={"detail": "%r exists" % e.t})

c = TestClient(app)
print(c.get("/modules/1").json())
print("missing  :", c.get("/modules/99").status_code, c.get("/modules/99").json())
print("duplicate:", c.post("/modules?title=Vectors").status_code)'''),

        ("Settings in one model",
         "Configuration read once and validated, rather than <code>os.getenv</code> "
         "scattered through the routers.",
         '''import os
from fastapi import FastAPI
from pydantic import BaseModel, Field, ValidationError

class Settings(BaseModel):
    app_name: str = "VizLearn API"
    page_size: int = Field(default=20, ge=1, le=100)
    debug: bool = False

def load_settings(env: dict) -> Settings:
    return Settings(**{k[3:].lower(): v for k, v in env.items()
                       if k.startswith("VZ_")})

good = load_settings({"VZ_PAGE_SIZE": "50", "VZ_DEBUG": "yes"})
print("loaded :", good.model_dump())

try:
    load_settings({"VZ_PAGE_SIZE": "5000"})
except ValidationError as e:
    print("refused:", e.errors()[0]["msg"])

app = FastAPI(title=good.app_name)
@app.get("/config")
def config(): return good.model_dump()
print("served :", TestClient(app).get("/config").json())'''),

        ("Dependencies shared across routers",
         "One module holding what several routers need, so the same rule is not "
         "written twice.",
         '''from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

# dependencies.py
def current_user(x_token: str = Header(default="")):
    if x_token != "tok":
        raise HTTPException(401, "Sign in")
    return {"name": "ada"}

def pagination(limit: int = 10, offset: int = 0):
    return {"limit": min(limit, 100), "offset": offset}

# routers/modules.py
modules = APIRouter(prefix="/modules", tags=["modules"])

@modules.get("")
def list_modules(page: dict = Depends(pagination)):
    return {"page": page}

# routers/account.py
account = APIRouter(prefix="/account", tags=["account"],
                    dependencies=[Depends(current_user)])

@account.get("")
def me(user: dict = Depends(current_user)):
    return user

app = FastAPI()
app.include_router(modules); app.include_router(account)

c = TestClient(app)
print(c.get("/modules?limit=500").json())
print("locked:", c.get("/account").status_code)
print("open  :", c.request("GET", "/account", headers={"x-token": "tok"}).json())'''),

        ("The whole shape, assembled",
         "Everything in one place so the arrangement is visible: settings, "
         "dependencies, services, schemas, routers, handlers.",
         '''from fastapi import APIRouter, Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# --- settings ------------------------------------------------------------
class Settings(BaseModel):
    page_size: int = Field(default=2, ge=1, le=100)
settings = Settings()

# --- domain --------------------------------------------------------------
class NotFound(Exception): pass
STORE = {1: "Vectors", 2: "Norms", 3: "Loops"}
def list_modules(limit): return list(STORE.items())[:limit]
def get_module(i):
    if i not in STORE: raise NotFound()
    return {"id": i, "title": STORE[i]}

# --- schemas -------------------------------------------------------------
class ModuleOut(BaseModel):
    id: int
    title: str

# --- dependencies --------------------------------------------------------
def page_limit(limit: int = None):
    return limit or settings.page_size

# --- routers -------------------------------------------------------------
router = APIRouter(prefix="/modules", tags=["modules"])

@router.get("")
def index(limit: int = Depends(page_limit)):
    return [{"id": i, "title": t} for i, t in list_modules(limit)]

@router.get("/{i}", response_model=ModuleOut)
def read(i: int):
    return get_module(i)

# --- assembly ------------------------------------------------------------
app = FastAPI(title="VizLearn API", version="1.0.0")
app.include_router(router)

@app.exception_handler(NotFound)
async def nf(r: Request, e: NotFound):
    return JSONResponse(status_code=404, content={"detail": "Not found"})

c = TestClient(app)
print(c.get("/modules").json())
print(c.get("/modules?limit=3").json())
print(c.get("/modules/2").json())
print("missing:", c.get("/modules/99").status_code)'''),
    ],
    [
        "One router per resource, in its own file. Create the directory on day one, not at the eightieth endpoint.",
        "Handlers translate HTTP and call a service. The service imports nothing from FastAPI, so it works from a job, a CLI or a test.",
        "Domain exceptions raised low and mapped to statuses by one handler keeps HTTP out of the business logic entirely.",
        "Settings belong in one validated model read once, not <code>os.getenv</code> scattered through routers.",
        "Shared dependencies live in one module, because several routers need the same ones.",
        "<code>main.py</code> should be boring: create the app, register handlers, include routers, add middleware. Short enough to read in one screen.",
    ],
    '''
title: Project Structure
intro: How the pieces are arranged once the application is more than one file.
## The layout

Nothing here is clever, and that is the point.

```
app/
  main.py            # create the app, register handlers, include routers
  settings.py        # one validated model
  dependencies.py    # what several routers share
  routers/
    modules.py
    tracks.py
  schemas/
    modules.py       # ModuleCreate, ModuleUpdate, ModuleOut
  services/
    modules.py       # the work; imports nothing from fastapi
```

The test of a layout is whether somebody asked to add a field can guess which files to open. If the answer is "search for the word", the structure has stopped helping.

## main.py should be boring

It does four things: create the `FastAPI` instance, register exception handlers, include routers, add middleware.

If it fits on a screen, it is the one place to answer "what does this application consist of?". If it grows business logic, that answer disappears.

Two things commonly end up there and should not. **Settings** belong in their own module, because scattering `os.getenv` makes it impossible to see what the application needs to run. And **startup work** belongs in a lifespan rather than at import, because work done at import happens when a test collector imports the module.

## Group by resource, inside a shallow layer structure

Both options look reasonable and one degrades.

Grouping by **resource** &mdash; `routers/modules.py`, `services/modules.py`, `schemas/modules.py` &mdash; means a change to one concept touches files with the same name in different directories. Easy to find, easy to review.

Grouping by **layer alone**, with every router in one file, means those files grow without bound and every change collides with every other.

Resource-first inside a shallow layer structure is what stays navigable. Two levels is plenty; deep package trees make imports long and tell you nothing extra.

## Handlers translate, services do

The most valuable boundary in the whole layout.

A handler's job is HTTP: take validated input, call something, turn the result into a response. Everything else belongs in a service that knows nothing about the framework.

The test is whether the service imports `fastapi`. If it raises `HTTPException`, it can only be used from a request &mdash; not from a background job, a management command, a scheduled task or a test. If it raises `ModuleNotFound`, it can be used from all of them, and one exception handler maps that to a 404 at the edge.

That mapping is worth doing early. Retrofitting it means finding every `HTTPException` scattered through service code and deciding what each should have been, usually while changing something else.

## Schemas by direction

From the response-model module, and it belongs in the layout too.

`ModuleCreate` takes what a caller may supply. `ModuleUpdate` has everything optional. `ModuleOut` declares what may be seen. Three small classes in one file, rather than one clever class with everything optional that documents nothing.

Keeping them beside each other makes the differences visible, which is when people notice that the output model still contains a field it should not.

## Dependencies in one module

Several routers need the same ones &mdash; the session, the current user, pagination. A shared `dependencies.py` is where they are found.

Reading that file should tell you what the application's endpoints are allowed to assume. That is a genuinely useful summary, and it is the same argument as the `types.py` from the Pydantic track.

## Settings in one model

A Pydantic model, read once, validated at startup:

```python
class Settings(BaseModel):
    page_size: int = Field(default=20, ge=1, le=100)
    debug: bool = False
```

Two benefits over reading the environment where it is needed. A missing or invalid value fails at startup with a message naming the field, rather than at request time in a handler. And the model is a list of everything the application needs to run, in one place, which is what a deployment checklist wants to be generated from.

`pydantic-settings` does the environment reading properly, including `.env` files and nested configuration.

## When to split

Earlier than feels necessary.

Create `routers/` on day one, even with two endpoints. Moving three routes is trivial; moving eighty means untangling imports and moving tests, and by then it does not happen and the file keeps growing.

The same applies to the service boundary. Extracting the first service when there is one function is a two-minute job. Extracting the twentieth from handlers that have grown around them is a rewrite.

## What this buys

Each piece testable on its own: a router included into a small app, a service called as a plain function, a schema validated against a payload, settings constructed from a dict.

A suite that needs "the module under test" rather than "a database, Redis and three environment variables" is the practical difference, and it comes almost entirely from where things were put.


## Mistakes people make

**Waiting to split.** Moving three routes is trivial; moving eighty is a rewrite that does not happen, so the file keeps growing.

**Business logic in routers.** A router importing your ORM works and stops being testable without a database.

**`HTTPException` in services.** The service can then only run inside a request - not from a job, a CLI or a test.

**`os.getenv` scattered about.** Nothing then says what the application needs to run, and a bad value fails at request time instead of at startup.

**Startup work at import.** Every test collector and linter pays for it.

**Deep package trees.** Two levels is plenty. Long import paths tell you nothing extra.

**Grouping only by layer.** One file with every router grows without bound and every change collides with every other.

## The test of a layout

Ask somebody new to add a field to one resource and watch what they do.

If they open `schemas/modules.py`, `services/modules.py` and `routers/modules.py`, the structure is working. If they search the codebase for a string, it is not.

That test matters more than any particular arrangement. A layout is a guess about where people will look, and the only evidence is whether they find it.

## Growing into it

No project should start with the full layout, and none should wait for it.

**Day one**: `main.py` and `routers/`. Two files, one router, room to grow.

**When a handler grows past a few lines**: extract the service. That is the boundary worth defending earliest, because everything else follows from it.

**When two routers need the same thing**: `dependencies.py`.

**When a model appears in two places**: `schemas/`.

**When configuration appears in two places**: `settings.py`.

Each step is prompted by something real rather than anticipated, and each takes minutes at the moment it is prompted. The alternative - deferring all of them until the file is unmanageable - means doing them all at once, in a diff nobody can review.

## What the layout is for

Not tidiness. Testability, and the ability for somebody new to guess where things are.

Those two are related: code that can be tested in isolation is code whose pieces have clear boundaries, and clear boundaries are what make a layout guessable. A structure that scores well on one usually scores well on the other, which is a convenient property when deciding whether an arrangement is worth the move.

## Summary

One router per resource in its own file, created on day one. Handlers translate HTTP and call services that import nothing from the framework, raising domain exceptions that one handler maps to statuses.

Schemas separated by direction. Shared dependencies in one module. Settings in one validated model read at startup. And a `main.py` short enough to read in a screen, doing nothing but assembly.

The value is not tidiness - it is that each piece becomes testable on its own, so the suite needs the module under test rather than the whole world.

## Where the track leaves you

Routing and the methods. Every source of input a request has, and what each is properly for. The response, its shape and its status. Errors, both automatic and raised. Structure, once one file stops being enough.

The whole dependency system - declaring what an endpoint needs, composing those requirements, giving them a lifetime, applying them to a section, and replacing them at the edges.

The runtime: where a handler runs and why the wrong choice is expensive, work after the response, and work once per process.

And the practices: a suite that runs in seconds, a generated document consumers can build against, and the shape of authentication.

That is enough to build and maintain a real API. What is left is largely not FastAPI - databases, deployment, observability, the operational parts - and each is easier once the layer underneath is arranged so it can be reasoned about a piece at a time.


## A note on imports

One practical detail that decides whether a layout survives.

Circular imports are the failure mode of splitting an application up, and they come from the same place every time: a service importing something from a router, or a schema importing a service.

The dependency direction should be one way. Routers import schemas and services. Services import schemas. Schemas import nothing of yours. Dependencies import schemas and services.

Follow that and cycles are impossible. Break it once - a service that raises `HTTPException`, a schema that calls a service to validate - and the cycle appears later, from a direction nobody expected, usually while adding something unrelated.

The domain-exception pattern is not only about testability. It is also what keeps the arrow pointing one way.


## A closing thought

None of this layout is FastAPI-specific, and none of it is new. Grouping by resource, keeping handlers thin, separating configuration, and assembling in a boring file are practices older than the framework.

What FastAPI contributes is that following them is nearly free. A router is four lines. Inclusion is one. The documentation reorganises itself around your tags without being asked. A dependency is a default argument.

When good structure costs almost nothing, the reason not to have it stops being effort and starts being habit - which is why the advice throughout this module is to do each piece earlier than it feels necessary.

## What was left out, and why

Three subjects have no module here, deliberately.

**Middleware** and **streaming responses** need a real event loop with anyio task groups, which these pages cannot provide. Writing them with code that cannot run would have broken the property every other page on this track has.

**WebSockets** need a real connection, which no amount of cleverness conjures in a browser tab.

They are real parts of the framework and worth learning from the official documentation. The rest of this track runs, which is the trade that was chosen.

## In one line

One router per resource, services that never import the framework, schemas by direction, settings in one validated model, and an assembly file short enough to read at a glance - each introduced the moment it is prompted rather than once the file has become unmanageable.

The arrow points one way - routers to services to schemas - and keeping it pointing that way is what prevents the circular imports that otherwise arrive from a direction nobody expected.
''',
    [
        {"q": "What should `main.py` contain?",
         "options": ["The endpoints", "Create the app, register handlers, include routers, add middleware", "Business logic", "The models"],
         "answer": 1,
         "why": "If it fits on a screen it answers \"what does this application consist of?\". Growing logic there destroys that."},
        {"q": "How do you tell whether the service boundary is right?",
         "options": ["By file size", "Whether the service imports fastapi", "By the number of functions", "By naming"],
         "answer": 1,
         "why": "A service raising HTTPException can only run inside a request. One raising a domain exception works from a job, a CLI or a test, with one handler mapping it at the edge."},
        {"q": "Why put settings in one validated model?",
         "options": ["Style", "A bad value fails at startup with a named field, and the model lists everything the app needs", "It is faster", "It is required"],
         "answer": 1,
         "why": "Scattered `os.getenv` fails at request time inside a handler, and leaves no single place that says what the application needs to run."},
        {"q": "When should you create a routers/ directory?",
         "options": ["At 50 endpoints", "On day one, with two", "Never", "When tests get slow"],
         "answer": 1,
         "why": "Moving three routes is trivial and moving eighty is a rewrite that does not happen - so the file keeps growing instead."},
    ],
)
